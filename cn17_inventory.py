"""Audit additional V3 infrastructure evidence; no additional supply or emissions credit is assigned."""
from pathlib import Path
import csv,json,openpyxl
P=Path(__file__).resolve().parent

def main():
 w=openpyxl.load_workbook(P/'cn17_source_wastewater.xlsx',read_only=True,data_only=True)
 rows=[]
 for s in w:
  r=[x for x in list(s.values)[1:] if x[1] and x[2]]
  rows.append(dict(sheet=s.title,facilities=len(r),reported_numeric_scale=sum(isinstance(x[6],(int,float)) for x in r),numeric_COD_samples=sum(isinstance(x[10],(int,float)) for x in r)))
 w=openpyxl.load_workbook(P/'cn17_source_waste_energy.xlsx',read_only=True,data_only=True)
 prop=next(r for r in w['Waste property (national)'].values if r[0]==2020); energy=next(r for r in w['Energy–carbon (national)'].values if r[0]==2020)
 out=dict(wastewater_records=rows,municipal_waste_2020_food_share_pct=prop[1],municipal_waste_to_energy_2020_processed_mt=energy[4]/1000,municipal_waste_to_energy_2020_power_twh=energy[6],municipal_waste_food_share_times_processed_mt=energy[4]/1000*prop[1]/100,interpretation='The food-share product is a composition proxy for already treated waste, not a recoverable supply estimate. Wastewater scale units and treatment throughput not used; no new food waste or sewage gas or avoided emissions credited.')
 (P/'cn17_inventory.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(out)
if __name__=='__main__':main()
