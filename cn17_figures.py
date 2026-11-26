"""Evidence-constrained figures; never overwrites CN v1.6.4 reference plots or corrected maps."""
from pathlib import Path
import csv,json
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
P=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':150})
def save(fig,name):
 fig.savefig(P/(name+'.tif'),dpi=600,pil_kwargs={'compression':'tiff_lzw'},facecolor='white');fig.savefig(P/(name+'.png'),dpi=240,facecolor='white');plt.close(fig)
def main():
 with (P/'cn17_cases.csv').open() as f:cases=list(csv.DictReader(f))
 with (P/'cn17_uncertainty.csv').open() as f:draws=list(csv.DictReader(f))
 j=json.loads((P/'cn17_summary.json').read_text());c=j['central'];v=lambda r,k:float(r[k]);pet=c['petroleum_late2025_bn'];names=['Reference\ntransport','Evidence\ntransport','Evidence +\nagriculture','Conservative\nresources','No carbon\nrevenue','After gas +\nagriculture'];cost=[j['baseline_total_cost_bn'],c['transport_cost_bn'],c['combined_cost_bn'],v(cases[1],'combined_cost_bn'),v(cases[4],'combined_cost_bn'),v(cases[3],'combined_cost_bn')]
 fig,ax=plt.subplots(1,2,figsize=(12.8,5.1),gridspec_kw={'width_ratios':[1.3,1]});fig.subplots_adjust(left=.09,right=.97,bottom=.20,top=.86,wspace=.39)
 a=ax[0];bars=a.bar(range(len(cost)),cost,color=['#858c95','#236799','#16856d','#ad8050','#ad8050','#236799']);a.axhline(pet,color='#444444',ls='--',lw=1.4,label=f'Continued petroleum: ${pet:.1f}B');a.set_ylim(0,450);a.set_xticks(range(len(cost)),names,fontsize=9);[a.text(b.get_x()+b.get_width()/2,h-13 if abs(h-pet)<20 else h+7,f'{h:.1f}',ha='center',va='top' if abs(h-pet)<20 else 'bottom',color='white' if abs(h-pet)<20 else '#222',fontsize=10) for b,h in zip(bars,cost)];a.legend(loc='upper left',bbox_to_anchor=(0,1.13),frameon=False,fontsize=10);a.set_ylabel('Annual cost (billion 2026 USD)');a.set_title('A  |  Evidence-constrained expenditure',loc='left',fontweight='bold',pad=31)
 a=ax[1];labs=['Petroleum transport','Evidence transport','Additional agriculture\n(net reduction)'];vals=[c['transport_avoided_mt']+c['transport_emissions_mt'],c['transport_emissions_mt'],c['additional_net_avoided_mtco2e']];bars=a.barh([2,1,0],vals,color=['#858c95','#236799','#16856d']);a.set_yticks([2,1,0],labs,fontsize=10);a.set_xlim(0,2500);a.bar_label(bars,fmt='%.1f',padding=4);a.set_xlabel('Million metric tons CO₂e/year');a.set_title('B  |  Emissions and separate mitigation',loc='left',fontweight='bold',pad=16);a.text(.03,-.27,'Agricultural reduction is additional to transport abatement;\nno fossil displacement credit is assumed.',transform=a.transAxes,fontsize=9)
 save(fig,'CN17_Fig10_evidence_results')
 fig,ax=plt.subplots(1,2,figsize=(12.5,5.1));fig.subplots_adjust(left=.11,right=.97,bottom=.16,top=.86,wspace=.35)
 a=ax[0];labs=['Collectable straw\n(mean, 2022)','New eligible\nstraw tiers','Historical manure\ndry collection','New digester\nfeed'];vals=[790.4467006972,c['straw_cap_mt'],c['manure_collectable_dry_mt'],c['manure_digested_dry_mt']];bars=a.barh(range(4),vals,color=['#b2bac3','#236799','#b2bac3','#16856d']);a.invert_yaxis();a.set_yticks(range(4),labs,fontsize=10);a.set_xlim(0,910);a.bar_label(bars,fmt='%.1f',padding=4);a.set_xlabel('Million metric tons/year (source or dry basis)');a.set_title('A  |  Resource screening',loc='left',fontweight='bold');a.text(0,-.19,'Physical collection estimates are not unused sustainable supply.',transform=a.transAxes,fontsize=9)
 a=ax[1];costs=[float(x['combined_cost_bn']) for x in draws];a.hist(costs,bins=16,color='#236799',edgecolor='white');a.axvline(np.median(costs),color='#16856d',lw=2,label=f'Median ${np.median(costs):.1f}B');a.axvline(pet,color='#444',ls='--',label=f'Petroleum ${pet:.1f}B');a.set_xlim(300,410);a.set_xlabel('Combined annual cost (billion 2026 USD)');a.set_ylabel('Conditional draws');a.legend(frameon=False,fontsize=10,loc='upper center',bbox_to_anchor=(.66,.96));a.set_title('B  |  Resource and methane sensitivities (128 draws)',loc='left',fontweight='bold',fontsize=10);a.text(0,-.19,'Fixed transport technology and vehicle assumptions.',transform=a.transAxes,fontsize=9)
 save(fig,'CN17_FigS8_resources_uncertainty')
 # Current graphical abstract: text-first, no speculative placement or route redraw.
 fig=plt.figure(figsize=(12.5,5));fig.patch.set_facecolor('white');fig.text(.035,.88,'CHINA  |  EVIDENCE-CONSTRAINED PETROLEUM-FREE TRANSPORT, 2050',fontsize=17,weight='bold',color='#17374b');fig.text(.035,.79,'Electrification • reactor heat • regional biomass • agricultural methane mitigation',fontsize=12,color='#365567')
 for i,(title,num,sub) in enumerate([('TRANSPORT ENERGY','$301.44B','Annual energy-system expenditure'),('TRANSPORT GHG','93.68%','Reduction against continued petroleum'),('INTEGRATED SCREEN','$330.06B','Includes vehicle and agricultural costs')]):
  x=.035+i*.325;fig.text(x,.58,title,fontsize=10,weight='bold',color='#365567');fig.text(x,.40,num,fontsize=31,weight='bold',color='#16856d');fig.text(x,.30,sub,fontsize=9,color='#333')
 fig.text(.035,.15,'Conditional annual screen: 1.966 Gt CO₂e/year avoided across transport and additional agriculture.',fontsize=12,weight='bold');fig.text(.035,.06,'No additional gas sales or fossil displacement credit; not an hourly reliability or 2050 business-as-usual forecast.',fontsize=9,color='#555')
 save(fig,'CN17_graphical_abstract')
if __name__=='__main__':main()
