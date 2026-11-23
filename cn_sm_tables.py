"""Writes the supplementary tables (markdown) straight from the inputs and stored outputs, so the tables in the
supplementary materials cannot drift from the code.  Output: cn_sm_tables.md.  Run after the other scripts."""
import csv, json
from pathlib import Path
import cn_inputs as I
import cn_model as M

H = Path(__file__).resolve().parent
S = json.load(open(H / "cn_scenarios.json"))
L = []
def t(title, head, rows):
    # separator dash counts set pandoc's relative column widths.  CN v1.6.1: numeric columns are right-aligned and sized to
    # their longest header word; text columns are left-aligned and widened with the length of their text
    import re as _re
    cells = [head] + [[str(x) for x in r] for r in rows]
    body = cells[1:]
    def _num(s): return s.strip() == "" or _re.fullmatch(r"[-+]?[\d,]*\.?\d*%?", s.replace(" ", "")) is not None
    numcol = [i > 0 and all(_num(c[i]) for c in body) for i in range(len(head))]
    hw = [max(len(w) for w in str(h).split()) + 2 for h in head]
    ml = [max((len(c[i]) for c in body), default=8) for i in range(len(head))]
    wid = [max(10, hw[i], ml[i] + 3) if numcol[i] else max(10, hw[i], min(30, ml[i] // 5 + 8)) for i in range(len(head))]
    if len(head) >= 8 and body: wid[0] = max(wid[0], min(24, ml[0] + 5))   # wide tables: room for row labels
    L.append(f"**{title}**\n"); L.append("| " + " | ".join(head) + " |")
    L.append("|" + "|".join((("-" * wid[i] + ":") if numcol[i] else (":" + "-" * wid[i])) for i in range(len(head))) + "|")
    for r in body: L.append("| " + " | ".join(r) + " |")
    L.append("")

f = lambda v, d=1: f"{(0.0 if abs(v) < 0.5 * 10 ** -d else v):,.{d}f}"   # no negative zero
B, K = I.BASE_MAINLAND, I.KWH_PER_KG
eu = S["least_cost"]["enduse"]
t("Table S1. 2025 baseline fuel use (mainland China, Hong Kong and Macau) and its energy.", ["Segment", "Fuel", "Quantity", "TWh (LHV)", "Basis"], [
    ["Light-duty road", "Gasoline", f"{f(B['gasoline_mt'],2)} Mt", f(eu['base']['ldv'],0), "CAPE 2025 review [S]; HK, Macau [A]"],
    ["Heavy and medium road", "Diesel", f"{f(B['onroad_diesel_mt'],2)} Mt", f(B['onroad_diesel_mt'] * K['diesel'], 0), "59% of 203 Mt diesel [A]"],
    ["Heavy and medium road", "LNG/CNG", f"{f(B['road_gas_bcm'])} bcm", f(B['road_gas_bcm'] * I.BCM_TWH, 0), "ICIS transport gas [S]"],
    ["Rail", "Diesel", f"{f(B['rail_diesel_mt'])} Mt", f(eu['base']['rail'], 0), "[A]"],
    ["Marine", "Diesel", f"{f(B['marine_diesel_mt'])} Mt", f(B['marine_diesel_mt'] * K['diesel'], 0), "[A]"],
    ["Marine", "Fuel oil (bunkers)", f"{f(B['marine_resid_mt'])} Mt", f(B['marine_resid_mt'] * K['resid'], 0), "~20 Mt bonded bunkers [S]; HK [A]"],
    ["Aviation", "Jet fuel", f"{f(B['jet_mt'],2)} Mt", f(eu['base']['air'], 0), "CAPE 2025 [S]; HK imports [S-order]"],
    ["Farm machinery", "Diesel", f"{f(B['farm_diesel_mt'])} Mt", f(eu['base']['farm'], 0), "[A]"],
    ["Construction and mining", "Diesel", f"{f(B['construction_mining_diesel_mt'])} Mt", f(eu['base']['construction'], 0), "[A]"],
    ["Industrial trucks", "Diesel-equivalent", f"{f(B['industrial_trucks_mt'])} Mt", f(eu['base']['industrial'], 0), "[A]"],
    ["Pipelines", "Natural gas", f"{f(B['pipeline_gas_bcm'])} bcm", f(eu['base']['pipeline'], 0), "[A]"],
    ["Total", "", "", f(sum(eu['base'].values()), 0), f"{f(sum(eu['base'].values()) * 3.6e-3, 2)} EJ"]])
E = I.ENDUSE
t("Table S2. 2050 technology shares by segment (share of 2025 service).", ["Segment", "Shares"], [
    [k, ", ".join(f"{a} {b:.2f}" for a, b in v.items())] for k, v in E.items() if isinstance(v, dict)] + [
    ["Range-extender fuel share", f(E['re_fuel_share'], 2)], ["Service growth to 2050", f(E['service_growth_2050'], 2)],
    ["Electric/diesel energy ratio, heavy trucks", f"{E['r_hdv_elec']:.3f} (= 2.40 kWh/mi x 3.6 / (21.1 MJ/mi HHV x 0.935 LHV/HHV))"],
    ["Fuel-cell/diesel energy ratio, heavy trucks", f"{E['r_hdv_fcev']:.3f}"], ["Electric/gasoline ratio, cars", f"{E['r_ldv_bev']:.3f}"]])
El = I.ELEC
RB = json.load(open(H / "cn_robustness.json"))
_lab = dict(purchase="Purchase-price difference, annualised (12 yr, 5%)", battery_replacement="Expected battery replacement",
            maintenance="Maintenance and repair", insurance="Insurance")
t("Table S2b. Net annual ownership cost of a battery-electric car relative to a petrol car in 2050, excluding energy (USD per car per year).",
  ["Component", "Low", "Central", "High"],
  [[_lab[k], f(RB["ldv_tco"]["low"]["parts"][k], 0), f(RB["ldv_tco"]["central"]["parts"][k], 0), f(RB["ldv_tco"]["high"]["parts"][k], 0)] for k in _lab] +
  [["Net (used in the model)", f(RB["ldv_tco"]["low"]["net_usd_yr"], 0), f(RB["ldv_tco"]["central"]["net_usd_yr"], 0), f(RB["ldv_tco"]["high"]["net_usd_yr"], 0)],
   ["Inputs: price difference (USD)", f(I.LDV_TCO["low"]["purchase_diff_usd"], 0), f(I.LDV_TCO["central"]["purchase_diff_usd"], 0), f(I.LDV_TCO["high"]["purchase_diff_usd"], 0)],
   ["Inputs: replacements per car; pack USD/kWh", f"{I.LDV_TCO['low']['repl_prob']}; {I.LDV_TCO['low']['pack_usd_kwh']:.0f}", f"{I.LDV_TCO['central']['repl_prob']}; {I.LDV_TCO['central']['pack_usd_kwh']:.0f}", f"{I.LDV_TCO['high']['repl_prob']}; {I.LDV_TCO['high']['pack_usd_kwh']:.0f}"],
   ["Inputs: maintenance saving vs 350 USD/yr", f"{I.LDV_TCO['low']['maint_saving']:.0%}", f"{I.LDV_TCO['central']['maint_saving']:.0%}", f"{I.LDV_TCO['high']['maint_saving']:.0%}"],
   ["Inputs: extra insurance (USD/yr)", f(I.LDV_TCO["low"]["insurance_extra_usd_yr"], 0), f(I.LDV_TCO["central"]["insurance_extra_usd_yr"], 0), f(I.LDV_TCO["high"]["insurance_extra_usd_yr"], 0)],
   ["Annualisation: capital recovery factor (12 yr, 5%); replacement in year 9, discounted", f"{0.05 / (1 - 1.05 ** -12):.4f}", "", ""]] +
  # CN v1.6 reconciliation from the per-car figure to the system cost
  [["Cars in 2050 (million) x battery-electric share", f"{I.VEH['ldv_stock_m']:.0f} x {I.ENDUSE['ldv']['bev']:.2f}", "", ""],
   ["Fleet net ownership cost (USD bn/yr)"] + [f(I.VEH["ldv_stock_m"] * I.ENDUSE["ldv"]["bev"] * RB["ldv_tco"][c]["net_usd_yr"] / 1e3, 1) for c in ("low", "central", "high")],
   ["Energy-system (project) saving vs late-2025 petroleum (%); vehicles excluded", f(S["least_cost_bev_tco_low"]["saving_energy_system_pct"], 1), f(S["least_cost"]["saving_energy_system_pct"], 1), f(S["least_cost_bev_tco_high"]["saving_energy_system_pct"], 1)],
   ["Saving including vehicle costs paid by owners (%)", f(S["least_cost_bev_tco_low"]["saving_vs_late_2025_pct"], 1), f(S["least_cost"]["saving_vs_late_2025_pct"], 1), f(S["least_cost_bev_tco_high"]["saving_vs_late_2025_pct"], 1)],
   ["Each USD 100 per car per year changes owners' costs by (USD bn)", f(I.VEH["ldv_stock_m"] * I.ENDUSE["ldv"]["bev"] * 100 / 1e3, 1), "", ""]])
t("Table S3. Electricity and hydrogen parameters (central values; Monte Carlo ranges in table S10).", ["Parameter", "Value"], [
    ["Onshore wind, best sites / remoter sites (USD/MWh)", f"{El['onshore_wind']:.0f} / {El['onshore_wind'] + El['onw2_adder']:.0f}, capped at {El['cap_onw_twh']:,.0f} / {El['cap_onw2_twh']:,.0f} TWh"],
    ["Solar PV (USD/MWh)", f"{El['solar']:.0f} (+1.25 x firming)"], ["Firming adder (USD/MWh)", f"{El['vre_firming']:.0f}"],
    ["Offshore wind fixed / floating (USD/MWh)", f"{El['osw_fixed']:.0f} / {El['osw_floating']:.0f}"],
    ["Concentrated solar with storage (USD/MWh)", f"{El['csp']:.0f}, firm"], ["Light-water reactors (USD/MWh)", f"{El['lwr']:.0f}"],
    ["Transmission and distribution adder (USD/MWh)", f"{El['td_adder']:.0f}"], ["Charging, cars / trucks and machines (USD/MWh)", f"{El['charge_ldv']:.0f} / {El['charge_hdv']:.0f}"],
    ["Maximum PV share; minimum firm share", f"{El['max_pv_share']:.2f}; {El['min_firm_share']:.2f}"],
    ["Natural gas for pyrolysis (USD/MMBtu)", f"{I.GAS['price_mmbtu']} + {I.GAS['delivery_mmbtu']} delivery"],
    ["Pyrolysis capital (USD/kW H2)", f"{I.PYRO['capex_kw_h2']:.0f}"], ["Alkaline electrolysis", f"{I.ELECTROLYSIS['kwh_kg']} kWh/kg, USD {I.ELECTROLYSIS['capex_cost_kg']}/kg"],
    ["Steam electrolysis", f"{I.NUCLEAR_H2['htse']['kwh_e_kg']} kWh_e + {I.NUCLEAR_H2['htse']['kwh_th_kg']} kWh_th per kg, USD {I.NUCLEAR_H2['htse']['capex_cost_kg']}/kg"],
    ["Discount rate", f"{I.WACC:.2f}"]])
rows = []
for c, v in I.REACTOR_COST.items(): rows.append([c, f"{v['boak_kwe']:,.0f}", f"{v['foak_mult']}", f"{100*v['learning']:.0f}%", f"{100*v['idc']:.0f}%"])
t("Table S4a. Reactor cost cases (per 250-MWt module; Wright learning).", ["Case", "BOAK USD/kWe", "FOAK multiplier", "Learning rate", "Interest during construction"], rows)
rows = []
for k, v in I.REACTOR_TYPES.items():
    rows.append([v["label"], v["outlet_c"], v["eta"], v["cost_mult"], v["fuel_mwhth"], v["f_pyro"], v["fissile"],
                 f(S[f'type_{k}']['energy_system_cost_bn']), f(S[f'post_gas_type_{k}']['energy_system_cost_bn'])])
t("Table S4b. Reactor technologies tested as hub designs, with 2050 energy-system (project) cost (USD bn; vehicle costs paid by owners, USD 20.8 bn, excluded).", ["Technology", "Outlet °C", "Turbine efficiency", "Cost multiplier", "Fuel USD/MWh_th", "Top-tier heat share", "Start-up fissile", "Gas era", "After gas"], rows)
lc = S["least_cost"]
t("Table S5. Residue tiers and use in the least-cost case.", ["Resource", "Region", "Cap (Mt dry/yr)", "USD/t", "Used (Mt)"],
  [[r["name"], r["region"], f(r["cap"]), f(r["usd_t"], 0), f(r["used"])] for r in lc["tiers_mt"]])
t("Table S6a. Sugar and starch ethanol feedstocks (autonomous-region crops) and use.", ["Feedstock", "Region", "Cap (bn gal)", "USD/gal", "Used (bn gal)"],
  [[r["name"], r["region"], f(r["cap_bgal"], 2), f(r["usd_gal"], 2), f(r["used_bgal"], 2)] for r in lc["ethanol_feeds"]])
t("Table S6b. Oil feedstocks for hydroprocessing and use.", ["Feedstock", "Region", "Cap (Mt)", "USD/t", "Used (Mt)"],
  [[r["name"], r["region"], f(r["cap_mt"], 2), f(r["usd_t"], 0), f(r["used_mt"], 2)] for r in lc["oil_feeds"]])
t("Table S6c. New bamboo and hemp land (Mha).", ["Crop", "Region", "Max Mha"],
  [["Bamboo", r[0], f(r[1], 2)] for r in I.BAMBOO["regions"]] + [["Hemp", r[0], f(r[1], 2)] for r in I.HEMP["regions"]])
mer = {m["zone"]: m for m in json.load(open(H / "cn_seaweed_merit.json"))["design"]}
t("Table S7. Offshore wind and seaweed zones.", ["Zone", "Species", "Yield t/ha (dem./design/learning)", "GW (large build)", "Port km", "Seaweed fuel USD/MWh"],
  [[z[2], z[3], "/".join(str(v) for v in z[5]), f(z[9], 0), f(z[10], 0), f(mer[z[0]]["best_usd_mwh"], 0) if z[0] in mer else "Taiwan system"] for z in I.SEAWEED + I.SEAWEED_TAIWAN])
P = I.PRICES_USD_T
t("Table S8. Pre-tax petroleum prices used for the comparator (USD per tonne; road gas USD/MMBtu).", ["Fuel", "Late 2025", "November 2026"],
  [[k, f(P["late_2025"][k], 0), f(P["nov_2026"][k], 0)] for k in P["late_2025"]] +
  [["Petroleum comparator, 2050 services (USD bn)", f(lc["petroleum"]["late_2025_bn"]), f(lc["petroleum"]["nov_2026_bn"])]])
N = I.NG
t("Table S9. Natural-gas supply inputs.", ["Input", "Value"], [[k, v] for k, v in N.items()])
t("Table S10. Monte Carlo parameters (triangular low/mode/high).", ["Parameter", "Low", "Mode", "High"],
  [["/".join(pth), lo, mo, hi] for pth, lo, mo, hi in M.MC] + [["Biomass price scale", 0.8, 1.0, 1.4], ["Ethanol cost scale", 0.85, 1.0, 1.3],
   ["Carbon market size scale", 0.5, 1.0, 1.5], ["Carbon value scale", 0.5, 1.0, 1.3], ["Yield level (0/1/2)", "p=0.3", "p=0.5", "p=0.2"],
   ["Reactor cost case (low/central/high)", "p=0.25", "p=0.5", "p=0.25"], ["Residue humification scale", 0.7, 1.0, 1.4],
   ["Hydrochar carbon stability", 0.3, 0.5, 0.7], ["Mineral fertiliser price scale", 0.8, 1.0, 1.5], ["Green manure and compost cost scale", 0.7, 1.0, 2.0]])
rows = []
for k, v in S.items():
    rows.append([k, f(v["energy_system_cost_bn"]), f(v["petroleum"]["late_2025_bn"]), f(v["saving_energy_system_pct"]), f(v["breakeven_energy_system"], 2),
                 f(v["hubs"], 0), f(v["gw"]["onshore_wind"], 0), f(v["gw"]["solar"], 0), f(v["gw"]["csp"], 0), f(v["gw"]["offshore_wind"], 0),
                 f(max(v["h2_mt"]["pyrolysis"], 0.0) + 0.0), f(v["h2_mt"]["steam_electrolysis"] + v["h2_mt"]["electrolysis"]), f(v["emissions"]["total_mt"], 0), f(v["emissions"]["reduction_pct"])])
rows = [[r[0], r[1], r[3], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12]] for r in rows]
_vm = S["least_cost"]["consumer_vehicle_cost_bn"]; _vt = S["tw_least_cost"]["consumer_vehicle_cost_bn"]
t(f"Table S11. All deterministic cases (2050). Cost = energy-system (project) cost in USD bn per year; saving against late-2025 petroleum (USD {S['least_cost']['petroleum']['late_2025_bn']:.1f} bn for mainland cases, {S['tw_least_cost']['petroleum']['late_2025_bn']:.1f} bn for Taiwan). The net cost of electric and fuel-cell vehicles and machines, paid by their owners, adds USD {_vm:.1f} bn to every mainland case except the vehicle-cost cases (table S15) and USD {_vt:.1f} bn to Taiwan. Capacities in GW; hydrogen in Mt; CO2e in Mt per year.",
  ["Case", "Cost", "Save %", "Hubs", "Wind", "PV", "CSP", "Offsh.", "Pyro H2", "Elec. H2", "CO2e"], rows)
EB = RB["emissions_boundary"]
_eb = dict(central="Central boundary", elec_ci_25g="Electricity 25 g CO2e/kWh (vs 10)", methane_leak_3pct="Upstream methane leakage 3% (vs 1.5%)",
           residue_soil_carbon_20g="Residue soil-carbon loss 20 g CO2e/MJ", residue_soil_carbon_40g="Residue soil-carbon loss 40 g CO2e/MJ",
           hub_construction_fuel_3g="Reactor construction and fuel cycle 3 g CO2e/kWh of hub heat", all_high="All of the above (40 g soil carbon)")
t("Table S12. Least-cost 2050 well-to-wheel emissions under wider life-cycle boundaries (Mt CO2e per year; no re-optimisation).",
  ["Boundary", "Emissions", "Reduction %", "Liquid fuels", "Electricity", "Hub construction/fuel"],
  [[_eb[k], f(v["total_mt"], 0), f(v["reduction_pct"]), f(v["by_source_mt"]["liquid_fuels"], 0), f(v["by_source_mt"]["electricity_lifecycle"], 0),
    f(v["by_source_mt"].get("hub_construction_fuel_cycle", 0.0), 0)] for k, v in EB.items()])
_dur = dict(product_life="One product life (10-20 years)", short="Short-lived (tyre wear, end-of-life combustion)", oxidised="Oxidised in use (metallurgy)",
            long_term="Long-term (asphalt, concrete, permanent storage)", uncertain="Soil amendment (counted toward the soil-carbon balance at 90% stability)")
t("Table S13. Destination and durability of pyrolysis carbon, least-cost case (Mt C per year). None is counted as an emission reduction.",
  ["Durability class", "Mt C", "Markets"],
  [[_dur[k], f(v, 1), "; ".join(m[0] for m, d in zip(I.CARBON_MARKETS, I.CARBON_DURABILITY) if d == k)] for k, v in RB["carbon_by_durability_mt"].items()])
_fe = dict(least_cost="Central least cost", post_gas_least_cost="After gas", least_cost_hub_cap_60="At most 60 hubs", least_cost_stress_moderate="Moderate stress")
t("Table S14. Build-rate and system-structure screen (reactor modules built 2032-2050; wind 2026-2050).",
  ["Case", "Hubs", "Modules", "Per yr", "GWt/yr", "Wind GW", "Wind/yr", "Solar GW", "Firm %", "Variable %"],
  [[_fe[k], f(v["modules"] / 6, 0), f(v["modules"], 0), f(v["modules_per_yr"], 0), f(v["gwt_per_yr"], 1), f(v["wind_gw"], 0), f(v["wind_gw_per_yr"], 0),
    f(v["solar_gw"], 0), f(100 * v["firm_share"], 0), f(100 * v["vre_share"], 0)] for k, v in RB["feasibility"].items()])
t("Table S15. Stress-test cases (2050; USD bn per year; each re-optimised). Project = energy-system cost; With vehicles adds the net cost of electric and fuel-cell vehicles and machines paid by their owners.",
  ["Case", "Project cost", "Saving %", "With vehicles", "Saving %", "Hubs", "Pyrolysis H2 Mt", "Emissions Mt"],
  [[v["label"].replace("BEV net cost", "Electric-car net cost").replace("BEV", "electric-car").replace(" (v1.1 accounting)", " (USD 8/MWh)"), f(v["energy_system_cost_bn"]), f(v["saving_energy_system_pct"]),
    f(v["transport_cost_bn"]), f(v["saving_pct"]), f(v["hubs"], 0), f(max(v["h2_pyro_mt"], 0.0) + 0.0), f(v["emissions_mt"], 0)] for v in RB["cases"].values()])
HBJ = json.load(open(H / "cn_htse_heat.json")); dd = HBJ["duties_kwh_kg"]
t("Table S16. Steam-electrolysis heat balance per kg of hydrogen (800 C stack, 0.5 MPa, 80% steam utilisation, no sweep gas).",
  ["Item", "kWh/kg", "Temperature range (C)", "Supplied by"],
  [["Feed-water preheat (total)", f(dd["feed_water_preheat"], 2), "20 to 152", "recovered heat, then external"],
   ["  recovered from hot-stream sensible heat", f(dd["preheat_recovered_sensible"], 2), "75 to 127", f"hot streams {HBJ['hot_outlet_after_recuperator_c']:.0f} to {HBJ['cathode_dew_point_c']:.0f} C"],
   ["  recovered by condensing unconverted steam", f(dd["preheat_recovered_condensing"], 2), "20 to 75", f"below the {HBJ['cathode_dew_point_c']:.0f} C dew point"],
   ["Evaporation", f(dd["evaporation"], 2), "152", "external"],
   ["External steam-raising heat (model input)", f(HBJ["external_heat_kwh_kg"], 2), "up to 152", "reactor process steam or electric boiler"],
   ["Superheat (total)", f(dd["superheat_total"], 2), "152 to 800", ""],
   ["  by high-temperature recuperator", f(dd["superheat_by_recuperator"], 2), "152 to 775", f"hot streams 800 to {HBJ['hot_outlet_after_recuperator_c']:.0f} C"],
   ["  electric trim", f(dd["electric_trim"], 2), "775 to 800", "electric heater"],
   ["Stack and hot-box heat loss", f(dd["stack_heat_loss"], 2), "800", "electric heater"],
   ["Electric topping (model input)", f(HBJ["topping_kwh_kg"], 2), "", ""],
   ["Recuperator area, m2 per kg/h", f(HBJ["recuperator_m2_per_kg_h"], 2), f"LMTD {HBJ['recuperator_lmtd_c']:.0f} K", f"USD {HBJ['recuperator_usd_kg']:.3f} per kg H2"],
   ["Without low-temperature recovery: external heat", f(HBJ["no_lowT_recovery_external_heat_kwh_kg"], 2), "up to 152", "sensitivity case"]])
_ls = dict(least_cost="Central least cost", post_gas_least_cost="After gas", least_cost_no_nuclear="No nuclear", least_cost_hub_cap_30="At most 30 hubs",
           least_cost_reactor_high="High reactor cost")
LSJ = RB["lull_screen"]
t("Table S17. Stylised wind-lull adequacy screen: a windless, overcast 7-day winter period with all flexible loads stopped. Load = inflexible transport load (GW); Firm = hubs with all heat to turbines plus light-water reactors (GW); Lull VRE = wind, solar and CSP output in the lull (GW); Short = shortfall (GW, and TWh over the week); Backup = indicative annual cost of hydrogen-fired backup (USD bn and % of energy-system cost); H2 lost = electrolytic hydrogen not produced during the week (Mt).",
  ["Case", "Load", "Firm", "Lull VRE", "Short GW", "Short TWh", "Backup bn", "% cost", "H2 lost"],
  [[_ls[k], f(v["inflexible_gw"], 0), f(v["hub_firm_gw"] + v["lwr_gw"], 0), f(v["variable_in_lull_gw"], 0), f(v["shortfall_gw"], 0), f(v["shortfall_twh"], 1),
    f(v["indicative_cost_bn"], 1), f(100 * v["indicative_cost_bn"] / S[k]["energy_system_cost_bn"], 1), f(v["h2_production_lost_mt"], 2)] for k, v in LSJ.items()])
_lv = dict(submitted="As in table S17", zero_wind="No wind", zero_wind_availability_80="No wind, reactor availability 80%",
           zero_wind_turbines_60pct="No wind, turbines for 60% of reactor heat", zero_wind_14_days="No wind, 14-day lull")
_lc = dict(least_cost="Central", post_gas_least_cost="After gas", least_cost_no_nuclear="No nuclear")
t("Table S18. Wind-lull screen sensitivities. Short = shortfall (GW, and TWh over the lull); Backup = indicative annual cost of hydrogen-fired backup (USD bn and % of energy-system cost), a lower bound that excludes hydrogen storage, replacement electrolyser capacity and delivery.",
  ["Case", "Variant", "Short GW", "Short TWh", "Backup bn", "% cost"],
  [[_lc[c], _lv[k], f(v["shortfall_gw"], 0), f(v["shortfall_twh"], 1), f(v["indicative_cost_bn"], 1), f(100 * v["indicative_cost_bn"] / S[c]["energy_system_cost_bn"], 1)]
   for c, d in RB["lull_sensitivity"].items() for k, v in d.items()])
# ---------------------------------------------------------------- CN v1.5 nutrient and soil-carbon balance, bioextraction
NU = I.NUTRIENTS; NB = RB["nutrients"]
_why = dict(
    liaodong_bay="Winter water 0-12 °C suits kelp; summer 22-26 °C suits G. lemaneiformis. Both are already farmed in the Bohai and Yellow Sea, so the rotation farms the bay year-round.",
    haizhou_bay="Same temperature range as Liaodong Bay. Pyropia is not expanded here, because Pyropia rafts on the nearby Subei shoal seed the Yellow Sea Ulva green tides.",
    yangtze_plume="The highest nitrate and phosphate on the coast. Farms sit in the clearer island waters, because the turbid inner estuary and Hangzhou Bay cut light. G. lemaneiformis takes up N quickly; kelp is grown in winter.",
    fujian_bays="China's main G. lemaneiformis-kelp rotation is already practised here. G. bailinae covers the summer, when water above 26 °C stops G. lemaneiformis.",
    pearl_river="Too warm for kelp. G. bailinae and G. tenuistipitata tolerate 15-33 °C and estuarine salinity and remove N and P year-round. Harvest goes to HTL; it goes to soil only if a metals screen is passed.",
    beibu_qinzhou="Warm (16-32 °C) and eutrophic in the inner bay. G. bailinae is the established local farm species.")
t("Table S19. Nearshore seaweed farms in nutrient-polluted coastal waters (bioextraction): species chosen and why. km2 = maximum farmed area; t/ha = dry-weight yield per ha per year (low / central / high); tissue N and P are % of dry weight.",
  ["Zone", "Water", "Species", "Why these species", "km2", "t/ha", "N %", "P %"],
  [[z[1], z[3], z[2], _why[z[0]], f(z[4], 0), " / ".join(f(v, 0) for v in z[5]), f(z[6], 1), f(z[7], 2)] for z in I.BIOEXTRACT])
CT = NU["content"]
t("Table S20. Nutrient, carbon and humification parameters (kg per t dry matter; humification = share of the carbon that would have become stable soil carbon if left on the field).",
  ["Biomass", "N", "P", "K", "C", "Humification"], [[k, f(v["n"]), f(v["p"]), f(v["k"]), f(v["c"], 0), f(v["humif"], 2)] for k, v in CT.items()])
t("Table S21. Where nutrients go in each conversion route and how much is recovered (shares).", ["Stream", "N", "P", "K", "Basis"], [
    ["HTL aqueous phase (share of feed)", f(NU["htl_to_aqueous"]["n"], 2), f(NU["htl_to_aqueous"]["p"], 2), f(NU["htl_to_aqueous"]["k"], 2), "Bao et al. 2025; Conti et al. 2018 [S/A]"],
    ["HTL solids, hydrochar (share of feed)", f(NU["htl_to_solids"]["n"], 2), f(NU["htl_to_solids"]["p"], 2), f(NU["htl_to_solids"]["k"], 2), "[S/A]"],
    ["Recovery from digested aqueous phase", f(NU["aqueous_recovery"]["n"], 2), f(NU["aqueous_recovery"]["p"], 2), f(NU["aqueous_recovery"]["k"], 2), "digestion, stripping, struvite [A]"],
    ["Gasifier ash (share of feed)", f(NU["pbtl_ash"]["n"], 2), f(NU["pbtl_ash"]["p"], 2), f(NU["pbtl_ash"]["k"], 2), "N lost as N2/NH3 [A]"],
    ["Cellulosic-ethanol stillage", f(NU["cel_stillage"]["n"], 2), f(NU["cel_stillage"]["p"], 2), f(NU["cel_stillage"]["k"], 2), "[A]"],
    ["Seaweed to HTL", f(NU["seaweed_htl"]["n"], 2), f(NU["seaweed_htl"]["p"], 2), f(NU["seaweed_htl"]["k"], 2), "saline aqueous phase [A]"],
    ["Seaweed to soil (washed)", f(NU["seaweed_soil"]["n"], 2), f(NU["seaweed_soil"]["p"], 2), f(NU["seaweed_soil"]["k"], 2), "[A]"]])
# CN v1.6.1: tables S22-S24 laid out to fit a portrait page (sources as rows; short headings)
_nc = dict(least_cost="LC", post_gas_least_cost="AG", least_cost_biological_soc="BIO")
SRCN = dict(hydrochar="HTL hydrochar", digestate="Digested HTL wastewater", gasifier_ash="Gasifier ash", ethanol_stillage="Ethanol stillage",
            offshore_seaweed="Offshore seaweed", nearshore_seaweed="Nearshore seaweed", green_manure="Green manure", compost="Manure compost",
            mineral_fertiliser="Mineral fertiliser bought")
hd = ["Mt per year"] + [f"{lab} {el.upper()}" for lab in _nc.values() for el in "npk"]
rows = [["Removed by harvest"] + [f(NB[k]["nutrients"][el]["removed_mt"], 3) for k in _nc for el in "npk"]]
for s, lab in SRCN.items():
    rows.append([lab] + [f(NB[k]["nutrients"][el]["returned_mt"].get(s, 0.0), 3) for k in _nc for el in "npk"])
rows.append(["Recovered nutrients sold"] + [f(NB[k]["nutrients"][el]["sold_mt"], 3) for k in _nc for el in "npk"])
t("Table S22. Nitrogen (N), phosphorus (P) and potassium (K) balance of the land that supplies biomass (Mt of element per year). LC = least cost; AG = after gas; BIO = soil carbon from biological sources only. Removed = nutrients in harvested residues, bamboo, hemp stalk and bagasse; returns plus fertiliser bought, less nutrients sold, must be at least this amount.",
  hd, rows)
_sc = dict(least_cost="Least cost", post_gas_least_cost="After gas", design_half_offshore="230 GW offshore", least_cost_bioextraction_full="All bays farmed",
           least_cost_soc_no_pyro_carbon="Pyrolysis C not counted", post_gas_no_biomethane_pyrolysis="After gas, no CH4 pyrolysis",
           least_cost_biological_soc="Biological only", post_gas_biological_soc="After gas, biological", least_cost_no_nutrient_balance="Unconstrained (not enforced)")
rows = []
for k, lab in _sc.items():
    d = NB[k]; sc = d["nutrients"]["soil_carbon"]; ss = sc["stable_soc_supplied_mt"]
    rows.append([lab, f(sc["stable_soc_required_mt"], 1), f(ss["hydrochar"], 1), f(ss["digestate"], 1),
                 f(ss.get("green_manure", 0.0), 1), f(ss.get("compost", 0.0), 1), f(ss["pyrolysis_carbon"], 1),
                 f(100 * sc["biogenic_share"], 0), f(S[k]["energy_system_cost_bn"], 0)])
_maxsw = max(NB[k]["nutrients"]["soil_carbon"]["stable_soc_supplied_mt"]["seaweed"] for k in _sc)
_maxgap = max(NB[k]["nutrients"]["soil_carbon"].get("deficit_mt", 0.0) for k in _sc)
_res = sorted({round(NB[k]["residues_mt"]) for k in _sc})
t(f"Table S23. Soil-carbon balance (Mt C per year) and energy-system cost (USD bn per year). Req. = required: residue carbon that would have become stable soil carbon; the sources are the stable fractions of what is returned or added (hydrochar, digestate, green manure, compost, pyrolysis carbon); Bio. % = share from biological sources. Every case harvests {', '.join(str(r) for r in _res)} Mt of residues; seaweed sent to soil supplies at most {_maxsw:.2f} Mt C; and the priced gap (soil carbon not replaced, an accounting entry rather than material returned to soil) is {_maxgap:.1f} Mt in every case. In the unconstrained case the requirement is reported but not enforced. Gas use for pyrolysis is in table S15 and Fig. 6.",
  ["Case", "Req.", "Hydro-char", "Digest-ate", "Green man.", "Com-post", "Pyro. C", "Bio. %", "Cost"], rows)
bx = S["design_half_offshore"]["bioextraction"]
_zn = {"liaodong_bay": "Liaodong Bay", "haizhou_bay": "Haizhou Bay", "yangtze_plume": "Yangtze plume", "fujian_bays": "Fujian bays",
       "pearl_river": "Pearl River", "beibu_qinzhou": "Qinzhou Bay"}
t("Table S24. Nearshore bioextraction farms in the 230 GW offshore design, in which every eutrophic zone is farmed to its screened area and all the harvest goes to liquefaction. Costs in USD per t of dry seaweed: farm (lines, seeding, upkeep), Grid Harvester, and haul (battery-sail vessels and drones). China's seaweed farms now remove about 75 kt N per year (Xiao et al. 2017).",
  ["Zone", "km2", "Dry Mt", "N kt", "P kt", "Fuel TWh", "Farm", "Grid Harv.", "Haul", "Total"],
  [[_zn.get(z["zone"], z["zone"]), f(z["km2"], 0), f(z["dry_mt"], 2), f(z["n_removed_kt"], 0), f(z["p_removed_kt"], 1), f(z["fuel_twh"], 1),
    f(z["farm_t"], 0), f(z["harvester_t"], 1), f(z["vessel_t"] + z["drones_t"], 1), f(z["cost_t"], 0)] for z in bx] +
  [["Total", f(sum(z["km2"] for z in bx), 0), f(sum(z["dry_mt"] for z in bx), 2), f(sum(z["n_removed_kt"] for z in bx), 0), f(sum(z["p_removed_kt"] for z in bx), 1),
    f(sum(z["fuel_twh"] for z in bx), 1), "", "", "", ""]])
gh = S["design_half_offshore"]["grid_harvester"]
L.append(f"\nGrid Harvester fleet in the 230 GW design: {gh.get('engineering_units', 0):,.0f} units in all, of which {gh.get('nearshore_units', 0):,.0f} serve the nearshore farms.\n")
GM, CMP = NU["green_manure"], NU["compost"]
t("Table S25. Biological soil-carbon options, available in every case and used by the LP when they are the cheapest way to close the balance [A].",
  ["Option", "Cap", "Cost", "Stable C added", "Nutrients added", "Basis"], [
    ["Winter legume green manure (Chinese milk vetch, hairy vetch) on winter-fallow fields", f"{GM['max_mha']} Mha", f"USD {GM['cost_usd_ha']:.0f}/ha",
     f"{GM['dm_t_ha'] * GM['c'] / 1e3 * GM['humif']:.2f} t C/ha ({GM['dm_t_ha']} t DM/ha, {GM['c'] / 10:.0f}% C, humification {GM['humif']})", f"{GM['n_fixed_kg_ha']:.0f} kg N/ha fixed",
     "About 9.3 Mha of winter fields underused, 72% readily available"],
    ["Compost from livestock manure not now returned to fields", f"{CMP['max_mt']:.0f} Mt DM", f"USD {CMP['cost_usd_t']:.0f}/t DM",
     f"{CMP['c'] / 1e3 * CMP['humif']:.3f} t C/t DM ({CMP['c'] / 10:.0f}% C, humification {CMP['humif']})", f"N {CMP['n']:.0f}, P {CMP['p']:.0f}, K {CMP['k']:.0f} kg/t DM",
     "About 22% of 3.8-4 bn t/yr of manure is not utilised; composting emissions 0.1 t CO2e/t DM"]])
BRK = RB["lull_bracket"]; _bn = dict(least_cost="Least cost", post_gas_least_cost="After gas", least_cost_hub_cap_30="At most 30 hubs",
                                      least_cost_no_nuclear="No nuclear", design_half_offshore="230 GW offshore")
rows = []
for k, v in BRK.items():
    rows.append([_bn.get(k, k), f(v["lower_bound"]["cost_bn"], 1), f(v["plausible"]["cost_bn"], 1), f(v["high"]["cost_bn"], 1),
                 f(v["lower_bound"]["saving_energy_system_pct"], 1), f(v["plausible"]["saving_energy_system_pct"], 1), f(v["high"]["saving_energy_system_pct"], 1)])
t(f"Table S26. Backup cost for the wind lull (USD bn per year) and the energy-system saving against late-2025 petroleum once it is included (%); including the vehicle costs paid by owners lowers each mainland saving by {100 * _vm / S['least_cost']['petroleum']['late_2025_bn']:.1f} points. Lower bound: backup plant and the hydrogen it burns. Plausible: adds a 15% reserve margin, hydrogen storage at USD 25/kg for one lull's backup fuel and the vehicles' hydrogen during the lull, extra hydrogen-production capacity to make up output lost in lulls, and USD 150/kW of transmission. High: a 14-day lull with no wind, 20% reserve, storage at USD 100/kg and USD 300/kW of transmission. Components in table S27. Not an hourly dispatch or reliability study.",
  ["Case", "Cost: lower", "Cost: plausible", "Cost: high", "Saving: lower", "Saving: plausible", "Saving: high"], rows)
_cp = dict(capacity_bn="Backup plant (incl. reserve margin)", fuel_bn="Hydrogen burned", storage_bn="Hydrogen storage", production_makeup_bn="Make-up hydrogen production",
           transmission_bn="Transmission", cost_bn="Total")
_ck = [k for k in ("least_cost", "post_gas_least_cost", "least_cost_hub_cap_30") if k in BRK]
t("Table S27. Components of the plausible and high backup costs in table S26 (USD bn per year).",
  ["Component"] + [f"{_bn[k]}: {lv}" for k in _ck for lv in ("plausible", "high")],
  [[lab] + [f(BRK[k][lv][c], 2) for k in _ck for lv in ("plausible", "high")] for c, lab in _cp.items()])
(H / "cn_sm_tables.md").write_text("\n".join(L))
print("cn_sm_tables.md written")
