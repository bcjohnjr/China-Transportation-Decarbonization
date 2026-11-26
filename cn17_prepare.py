"""Prepare province-level inputs from published workbook extracts shipped in the delta."""
from pathlib import Path
from collections import defaultdict
import csv,openpyxl
P=Path(__file__).resolve().parent

def main():
 # Rebuild the 93 province/scenario rows directly from the original city tables.
 province=[]
 for scenario in ('min','mean','max'):
  ww=openpyxl.load_workbook(P/f'cn17_source_straw_{scenario}.xlsx',read_only=True,data_only=True)
  rr=list(ww.active.values);cols=[str(x).strip() for x in rr[0]];agg=defaultdict(lambda:[0.0]*27);seen=set()
  for x in rr[1:]:
   code=int(x[2]);assert code not in seen;seen.add(code)
   if code>=700000:continue
   assert all(isinstance(v,(float,int)) and v>=0 for v in x[3:30])
   k=(str(code)[:2],x[0]);agg[k]=[a+v for a,v in zip(agg[k],x[3:30])]
  for (code,pr),v in sorted(agg.items()):province.append(dict(zip(['province_code','province','scenario','year']+cols[3:30],[code,pr,scenario,2022]+v)))
 assert len(province)==93
 with (P/'cn17_straw_province.csv').open('w',encoding='utf-8-sig',newline='') as f:
  wr=csv.DictWriter(f,fieldnames=list(province[0]));wr.writeheader();wr.writerows(province)
 ww=openpyxl.load_workbook(P/'cn17_source_biomass_energy.xlsx',read_only=True,data_only=True);en=[]
 for sn in ('2020','2050'):
  for r in list(ww[sn].values)[1:]:
   if r[0] and all(isinstance(x,(float,int)) for x in r[1:6]):en.append(dict(zip(['year','province','agricultural_residues_PJ','forestry_residues_PJ','energy_crops_PJ','animal_manure_PJ','municipal_waste_PJ'],[int(sn),*r[:6]])))
 assert len(en)==62
 with (P/'cn17_energy_province.csv').open('w',encoding='utf-8-sig',newline='') as f:
  wr=csv.DictWriter(f,fieldnames=list(en[0]));wr.writeheader();wr.writerows(en)
 w=openpyxl.load_workbook(P/'cn17_source_biomass_resources.xlsx',read_only=True,data_only=True); data=defaultdict(lambda:dict(manure_collectable_dry_mt=0.,manure_ch4_mt=0.,enteric_ch4_mt=0.,cattle_total_ch4_mt=0.))
 for r in list(w['anim _man-2020'].values)[1:]:
  if all(isinstance(x,(float,int)) for x in r[2:7]):data[r[0].strip()]['manure_collectable_dry_mt']+=r[2]*1e4*r[3]*r[4]*r[5]*r[6]/1e9
 for name,k in [('cn17_source_manure_methane.xlsx','manure_ch4_mt'),('cn17_source_enteric_methane.xlsx','enteric_ch4_mt')]:
  w=openpyxl.load_workbook(P/name,read_only=True,data_only=True)
  for r in list(w.active.values)[1:]:
   if isinstance(r[16],(float,int)):data[r[2].strip()][k]+=r[16]/100
 w=openpyxl.load_workbook(P/'cn17_source_livestock_categories.xlsx',read_only=True,data_only=True)
 for r in list(w.active.values)[1:]:
  if r[2]==2020:data[r[0].strip()]['cattle_total_ch4_mt']+=sum(r[3:6])/1e6
 with (P/'cn17_waste_province.csv').open('w',encoding='utf-8',newline='') as f:
  fields=['province',*next(iter(data.values()))];wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader();wr.writerows(dict(province=k,**v) for k,v in sorted(data.items()))
 print('manure dry resource Mt',sum(v['manure_collectable_dry_mt'] for v in data.values()),'manure methane Mt',sum(v['manure_ch4_mt'] for v in data.values()),'enteric methane Mt',sum(v['enteric_ch4_mt'] for v in data.values()),'cattle all methane Mt',sum(v['cattle_total_ch4_mt'] for v in data.values()))
if __name__=='__main__':main()
