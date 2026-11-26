"""CN v1.7 evidence-constrained extension. Uses unchanged CN v1.6.4 solver; flat offline inputs.
Additional agricultural mitigation is a separate incremental screening account, not a transport credit.
"""
from pathlib import Path
import csv,json,math,copy,hashlib,os
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import cn_model as M
P=Path(__file__).resolve().parent

def rows(name):
 with (P/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,rr):
 with (P/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
STR=rows('cn17_straw_province.csv'); EN=rows('cn17_energy_province.csv'); W=rows('cn17_waste_province.csv')
# Historical collection potential, not unused supply. Additional fraction and dry-matter factors are scenarios.
# Region groups use province codes (GB/T 2260); rest straw pools are disjoint.
REG={15:'inner_mongolia',65:'xinjiang',45:'guangxi',64:'ningxia',54:'xizang'}
NORTH={11,12,13,14,21,22,23,37,41,61,62,63}
COLS=[k for k in STR[0] if k.startswith('straw_') and k.endswith('_t') and k not in ('straw_total_t','straw_total_no_veg_fruit_t','straw_vegetable_t','straw_fruit_melon_t','straw_sugarcane_t','straw_cassava_t','straw_sorghum_t','straw_sweet_potato_t')]
# Feedstock cost screen based on Xu et al. 2024 Supplement Table S14 (2015 USD), not an observed 2026 supply curve.
def logistics(distance,scale=1.30,farmgate=15):
 return (farmgate+scale*(11.09/1.67+5*.88+.13*11.09+.10+.32+2.86+.35+.18+.29+.14+(.06+.04)*5*.88+(.0125+.0083)*distance*.88))/.95

def parameters(scenario='mean',fraction=.50,dry=.85,forest_fraction=.30,oil_fraction=.25,price_factor=1.0):
 p=M.default_params(); caps=defaultdict(float); province=[]
 for r in STR:
  if r['scenario']!=scenario:continue
  code=int(r['province_code']);reg=REG.get(code,'rest');q={k:float(r[k]) if r[k] else 0 for k in COLS};factor=fraction*dry/1e6
  if reg=='guangxi': a=(float(r['straw_sugarcane_t'])+float(r['straw_cassava_t']))*factor;caps[4]+=a
  elif reg=='inner_mongolia': a=sum(q.values())*factor;caps[2]+=a
  elif reg=='xinjiang': a=sum(q.values())*factor;caps[3]+=a
  elif reg=='ningxia': a=sum(q.values())*factor;caps[5]+=a
  elif reg=='xizang': a=0
  else:
   # Primary tiers may use only corresponding crops. Residual allocated to tier 2 after first-tier cap allocation.
   primary=(q['straw_maize_t']+q['straw_wheat_t']) if code in NORTH else q['straw_rice_t'];a=sum(q.values())*factor;idx=0 if code in NORTH else 1
   caps[idx]+=primary*factor;caps[9]+=(sum(q.values())-primary)*factor
  province.append(dict(province_code=code,province=r['province'],region=reg,eligible_dry_mt=a))
 orig=p['BIOMASS']['tiers'];caps[9]+=max(0,caps[0]-orig[0][2])+max(0,caps[1]-orig[1][2]);
 # Forestry and existing bamboo share one historical energy ceiling; Xizang excluded from rest.
 forest=sum(float(r['forestry_residues_PJ']) for r in EN if str(r['year'])=='2020' and 'tibet' not in r['province'].lower() and 'xizang' not in r['province'].lower())*forest_fraction/18
 # PJ / GJ/t = Mt; existing woody resource ceiling is scenario-based, not measured dry tonnage.
 caps[7]=forest*.7;caps[8]=forest*.3
 tib=sum(float(r['forestry_residues_PJ']) for r in EN if str(r['year'])=='2020' and ('tibet' in r['province'].lower() or 'xizang' in r['province'].lower()))*forest_fraction/18
 caps[6]=tib
 p['BIOMASS']['tiers']=[(t[0],t[1],min(t[2],caps[j]),max(t[3],logistics(100 if j==9 else 50))*price_factor) for j,t in enumerate(orig)]
 # USDA FAS 2025: 11 billion L estimated supply capacity vs 5.2 billion L already collected; do not divert existing uses.
 # 0.90 kg/L and recovery fraction are assumed; 1 billion L * kg/L = Mt.
 for f in p['OIL_FEEDS']:
  if f[0]=='uco': f[3]=min(f[3],(11-5.2)*.90*oil_fraction)
 return p,province

def agriculture(r,elig=.25,yield_ch4=.18,leak=.01,adoption_scale=1,ad_cost=65):
 # Reserve the full original compost capacity (dry Mt proxy); no HTL wastewater, existing collected UCO or straw enters this account.
 total=sum(float(x['manure_collectable_dry_mt']) for x in W);pool=total*elig;reserve=min(pool,50.0);feed=max(0,pool-reserve)
 gross=feed*yield_ch4;flare=gross*.02;lost=gross*leak;own=(gross-flare-lost)*.10;delivered=gross-flare-lost-own
 # Existing manuscript uses GWP100 29.8 for methane. Biogenic 27.2 applied to BOTH incremental avoided and fugitive CH4.
 # Historical baseline is geographically aggregated, capped by fraction of physical manure assigned to new digesters.
 manure_baseline=sum(float(x['manure_ch4_mt']) for x in W);avoided_ch4=min(gross,manure_baseline*(feed/total)*.60)
 ad_process=gross*50/3.6*.025 # 25 kg CO2e per gross LHV MWh
 ad_net=(avoided_ch4-lost)*27.2-ad_process
 ad_bn=gross*50/3.6*(ad_cost+4)/1000 # $/MWh gross + monitoring
 # Cattle-only upper limit: category dataset includes enteric + manure; subtract ALL national manure CH4 conservatively.
 # Inherited cattle groups are a scenario, not measured headcounts; use conservative baseline cap and no grazing deployment.
 cattle=sum(float(x['cattle_total_ch4_mt']) for x in W);cattle_enteric=max(0,cattle-manure_baseline)
 A=M.default_params()['AG'];seaweed=0;gross_cut=0
 for k in ('feedlot','dairy'):
  heads=A['head_'+k+'_m'];adopt=A['adoption'][k]*adoption_scale
  seaweed+=heads*A['dmi_kg_d'][k]*365*A['dose_dm']*adopt/1000
  # Shares refer to inherited total enteric; use a capped cattle-only base, normalized to all cattle groups.
  gross_cut+=cattle_enteric*27.2*A['enteric_share'][k]*A['cut'][k]*adopt
 # Feasible within annual heat available after existing food allocations? existing food module allocates Asparagopsis FIRST.
 heat_cap=r['food']['low_grade_twh'];heat=seaweed*25;ratio=min(1,heat_cap/heat) if heat else 1;seaweed*=ratio;gross_cut*=ratio;heat*=ratio
 asp_process=seaweed*5 # assumed 5 tCO2e/t dry, incl production/delivery; no free emissions claim
 asp_net=gross_cut-asp_process;asp_bn=seaweed*5000/1000
 return dict(manure_collectable_dry_mt=total,manure_eligible_dry_mt=pool,compost_reserved_dry_mt=reserve,manure_digested_dry_mt=feed,gross_methane_mt=gross,leaked_methane_mt=lost,flared_methane_mt=flare,own_use_methane_mt=own,delivered_methane_mt=delivered,delivered_biomethane_lhv_twh=delivered*50/3.6,manure_historical_ch4_mt=manure_baseline,avoided_baseline_ch4_mt=avoided_ch4,manure_net_avoided_mtco2e=ad_net,manure_cost_bn=ad_bn,cattle_enteric_lower_bound_mtch4=cattle_enteric,asparagopsis_dry_mt=seaweed,asparagopsis_heat_twh=heat,asparagopsis_gross_avoided_mtco2e=gross_cut,asparagopsis_net_avoided_mtco2e=asp_net,asparagopsis_cost_bn=asp_bn,additional_net_avoided_mtco2e=ad_net+asp_net,additional_cost_bn=ad_bn+asp_bn,break_even_leak_share_no_gas_credit=(avoided_ch4-ad_process/27.2)/gross if gross else 0.0,conditional_fossil_displacement_upper_mtco2e=min(delivered*50/3.6, r['gas_for_pyrolysis_bcm']*9.9)*.252)

def solve_case(args):
 name,sc,frac,dry,ff,oil,pf,post,mc,elig,yld,leak,adopt,adc,no_carbon=args
 p,prov=parameters(sc,frac,dry,ff,oil,pf)
 if no_carbon:
  p['CARBON']=[[m[0],m[1],min(m[2],0)] for m in p['CARBON']];p['lightweight']=False
 if post:p=M.post_gas_params(p)
 # Match physical heat allocation to the incremental cattle screen; no inherited grazing credit.
 cattle=sum(float(x['cattle_total_ch4_mt']) for x in W); manure=sum(float(x['manure_ch4_mt']) for x in W)
 p['AG']['enteric_mt']=max(0,cattle-manure)*27.2
 p['AG']['adoption']['grazing']=0.0
 for k in ('feedlot','dairy'):p['AG']['adoption'][k]*=adopt
 # Explicit expensive renewable-liquid import / shortfall proxy, reported separately; not evidence of domestic feasibility.
 p['ELEC']['liq_import_cap_twh']=1e4;p['ELEC']['liq_import_usd_mwh']=400
 r=M.solve_fleet(p,scenario='least_cost',post_gas=post,mc=mc)
 a=agriculture(r,elig,yld,leak,adopt,adc);pet=r['petroleum']['late_2025_bn'];cost=r['transport_cost_bn'];comb=cost+a['additional_cost_bn'];e=r['emissions'];
 s=dict(case=name,straw_scenario=sc,available_share=frac,dry_factor=dry,forest_fraction=ff,uco_fraction=oil,cost_multiplier=pf,post_gas=post,no_carbon=no_carbon,energy_cost_bn=r['energy_system_cost_bn'],vehicle_cost_bn=r['consumer_vehicle_cost_bn'],transport_cost_bn=cost,petroleum_late2025_bn=pet,petroleum_nov2026_bn=r['petroleum']['nov_2026_bn'],transport_savings_pct=100*(1-cost/pet),transport_emissions_mt=e['total_mt'],transport_avoided_mt=e['avoided_mt'],transport_reduction_pct=e['reduction_pct'],hubs=r['hubs'],straw_and_forest_cap_mt=sum(t[2] for t in p['BIOMASS']['tiers']),straw_cap_mt=sum(t[2] for t in p['BIOMASS']['tiers'] if M.tier_profile(t[0])=='straw'),tiers_used_mt=sum(x['used'] for x in r['tiers_mt']),liquid_import_proxy_twh=r['liq_import_twh'],soc_deficit_mt=r['nutrients']['soil_carbon']['deficit_mt'],uco_cap_mt=next(f[3] for f in p['OIL_FEEDS'] if f[0]=='uco'),**a,combined_cost_bn=comb,combined_avoided_mt=e['avoided_mt']+a['additional_net_avoided_mtco2e'],combined_savings_pct=100*(1-comb/pet))
 assert abs(r['objective_reconciliation']['residual_bn'])<1e-5
 assert abs(a['gross_methane_mt']-sum(a[k] for k in ['leaked_methane_mt','flared_methane_mt','own_use_methane_mt','delivered_methane_mt']))<1e-9
 assert all(t['used']<=t['cap']+1e-6 for t in r['tiers_mt'])
 return s,r,prov

def main():
 base=M.solve_fleet(M.default_params(),scenario='least_cost');assert abs(base['energy_system_cost_bn']-293.21815047182287)<1e-5
 specs=[('evidence_central','mean',.5,.85,.30,.25,1,False,False,.25,.18,.01,1,65,False),('conservative','min',.35,.80,.20,.10,1.2,False,False,.15,.12,.03,.6,90,False),('upper','max',.65,.90,.40,.50,.9,False,False,.40,.22,.005,1,45,False),('post_gas','mean',.5,.85,.30,.25,1,True,False,.25,.18,.01,1,65,False),('no_carbon_revenue','mean',.5,.85,.30,.25,1,False,False,.25,.18,.01,1,65,True),('advanced_leak_control','mean',.5,.85,.30,.25,1,False,False,.25,.18,.002,1,65,False),('no_new_manure','mean',.5,.85,.30,.25,1,False,False,0,.18,.01,1,65,False)]
 with ProcessPoolExecutor(max_workers=4) as ex: out=list(ex.map(solve_case,specs))
 write('cn17_cases.csv',[x[0] for x in out]);write('cn17_regional_screen.csv',out[0][2]);(P/'cn17_details.json').write_text(json.dumps({x[0]['case']:M.slim(x[1]) for x in out},indent=2),encoding='utf-8')
 rng=np.random.default_rng(1704);t=lambda a,b,c:float(rng.triangular(a,b,c)); jobs=[]
 for j in range(128):
  jobs.append((f'draw_{j:03}',str(rng.choice(['min','mean','max'],p=[.25,.5,.25])),t(.35,.5,.65),t(.8,.85,.9),t(.2,.3,.4),t(.1,.25,.5),t(.9,1,1.2),False,True,t(.15,.25,.4),t(.12,.18,.22),t(.005,.01,.03),t(.6,.85,1),t(45,65,90),False))
 with ProcessPoolExecutor(max_workers=4) as ex: draws=[x[0] for x in ex.map(solve_case,jobs)]
 write('cn17_uncertainty.csv',draws)
 summary={'baseline_energy_cost_bn':base['energy_system_cost_bn'],'baseline_total_cost_bn':base['transport_cost_bn'],'central':out[0][0],'draws':len(draws),'combined_cost_quantiles_bn':[float(x) for x in np.quantile([r['combined_cost_bn'] for r in draws],[.05,.5,.95])],'domestic_feasible_draws':sum(r['liquid_import_proxy_twh']<1e-6 and r['soc_deficit_mt']<1e-6 for r in draws),'cheaper_and_domestic_draws':sum(r['combined_savings_pct']>0 and r['liquid_import_proxy_twh']<1e-6 and r['soc_deficit_mt']<1e-6 for r in draws)}
 (P/'cn17_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
