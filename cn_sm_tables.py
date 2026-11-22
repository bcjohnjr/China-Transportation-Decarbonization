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
    # separator dash counts set pandoc's relative column widths (wide text columns, narrow numbers)
    cells = [head] + [[str(x) for x in r] for r in rows]
    wid = [max(11, max(len(w) for w in str(head[i]).split()) + 3, min(22, max(len(c[i]) for c in cells[1:]) if len(cells) > 1 else 8))
           for i in range(len(head))]
    L.append(f"**{title}**\n"); L.append("| " + " | ".join(head) + " |")
    L.append("|" + "|".join([":" + "-" * wid[0]] + ["-" * wid[i] + ":" for i in range(1, len(head))]) + "|")
    for r in cells[1:]: L.append("| " + " | ".join(r) + " |")
    L.append("")

f = lambda v, d=1: f"{v:,.{d}f}"
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
    ["Electric/diesel energy ratio, heavy trucks", f"{E['r_hdv_elec']:.3f} (= 2.40 kWh/mi x 3.6 / 21.1 MJ/mi)"],
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
   ["Inputs: maintenance saving vs 350 USD/yr", f"{I.LDV_TCO['low']['maint_saving']:.0%}", f"{I.LDV_TCO['central']['maint_saving']:.0%}", f"{I.LDV_TCO['high']['maint_saving']:.0%}"]])
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
                 f(S[f'type_{k}']['transport_cost_bn']), f(S[f'post_gas_type_{k}']['transport_cost_bn'])])
t("Table S4b. Reactor technologies tested as hub designs, with 2050 transport cost (USD bn).", ["Technology", "Outlet °C", "Turbine efficiency", "Cost multiplier", "Fuel USD/MWh_th", "Top-tier heat share", "Start-up fissile", "Gas era", "After gas"], rows)
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
   ["Reactor cost case (low/central/high)", "p=0.25", "p=0.5", "p=0.25"]])
rows = []
for k, v in S.items():
    rows.append([k, f(v["transport_cost_bn"]), f(v["petroleum"]["late_2025_bn"]), f(v["saving_vs_late_2025_pct"]), f(v["breakeven_multiple"], 2),
                 f(v["hubs"], 0), f(v["gw"]["onshore_wind"], 0), f(v["gw"]["solar"], 0), f(v["gw"]["csp"], 0), f(v["gw"]["offshore_wind"], 0),
                 f(max(v["h2_mt"]["pyrolysis"], 0.0) + 0.0), f(v["h2_mt"]["steam_electrolysis"] + v["h2_mt"]["electrolysis"]), f(v["emissions"]["total_mt"], 0), f(v["emissions"]["reduction_pct"])])
rows = [[r[0], r[1], r[3], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12]] for r in rows]
t("Table S11. All deterministic cases (2050). Cost in USD bn per year; saving against late-2025 petroleum (USD 399.3 bn for mainland cases); capacities in GW; hydrogen in Mt; CO2e in Mt per year.",
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
            long_term="Long-term (asphalt, concrete, permanent storage)", uncertain="Uncertain (soil amendment)")
t("Table S13. Destination and durability of pyrolysis carbon, least-cost case (Mt C per year). None is counted as an emission reduction.",
  ["Durability class", "Mt C", "Markets"],
  [[_dur[k], f(v, 1), "; ".join(m[0] for m, d in zip(I.CARBON_MARKETS, I.CARBON_DURABILITY) if d == k)] for k, v in RB["carbon_by_durability_mt"].items()])
_fe = dict(least_cost="Central least cost", post_gas_least_cost="After gas", least_cost_hub_cap_60="At most 60 hubs", least_cost_stress_moderate="Moderate stress")
t("Table S14. Build-rate and system-structure screen (reactor modules built 2032-2050; wind 2026-2050).",
  ["Case", "Hubs", "Modules", "Per yr", "GWt/yr", "Wind GW", "Wind/yr", "Solar GW", "Firm %", "Variable %"],
  [[_fe[k], f(v["modules"] / 6, 0), f(v["modules"], 0), f(v["modules_per_yr"], 0), f(v["gwt_per_yr"], 1), f(v["wind_gw"], 0), f(v["wind_gw_per_yr"], 0),
    f(v["solar_gw"], 0), f(100 * v["firm_share"], 0), f(100 * v["vre_share"], 0)] for k, v in RB["feasibility"].items()])
t("Table S15. Stress-test cases (2050; USD bn per year; each re-optimised).", ["Case", "Cost", "Saving %", "Hubs", "Pyrolysis H2 Mt", "Emissions Mt"],
  [[v["label"].replace("BEV net cost", "Electric-car net cost").replace("BEV", "electric-car"), f(v["transport_cost_bn"]), f(v["saving_pct"]), f(v["hubs"], 0), f(max(v["h2_pyro_mt"], 0.0) + 0.0), f(v["emissions_mt"], 0)] for v in RB["cases"].values()])
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
t("Table S17. Stylised wind-lull adequacy screen: a windless, overcast 7-day winter period with all flexible loads stopped. Load = inflexible transport load (GW); Firm = hubs with all heat to turbines plus light-water reactors (GW); Lull VRE = wind, solar and CSP output in the lull (GW); Short = shortfall (GW, and TWh over the week); Backup = indicative annual cost of hydrogen-fired backup (USD bn and % of system cost); H2 lost = electrolytic hydrogen not produced during the week (Mt).",
  ["Case", "Load", "Firm", "Lull VRE", "Short GW", "Short TWh", "Backup bn", "% cost", "H2 lost"],
  [[_ls[k], f(v["inflexible_gw"], 0), f(v["hub_firm_gw"] + v["lwr_gw"], 0), f(v["variable_in_lull_gw"], 0), f(v["shortfall_gw"], 0), f(v["shortfall_twh"], 1),
    f(v["indicative_cost_bn"], 1), f(v["indicative_cost_pct"], 1), f(v["h2_production_lost_mt"], 2)] for k, v in LSJ.items()])
(H / "cn_sm_tables.md").write_text("\n".join(L))
print("cn_sm_tables.md written")
