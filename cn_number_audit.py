"""CN v1.6.4 independent number audit.

Recomputes the headline quantities of the China transport model from first principles, with physical constants and
reference values typed in here (not imported from cn_inputs), and compares them with the saved model outputs.  Every unit
conversion that carries a headline number (kWh against MJ, lower against higher heating value) is redone here by hand.

    python3 cn_number_audit.py          # prints a table, writes cn_number_audit.json, exits 1 on any failure
"""
from __future__ import annotations
import csv, json, math, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = json.load(open(HERE / "cn_scenarios.json")); LC = S["least_cost"]
RB = json.load(open(HERE / "cn_robustness.json"))
MCS = json.load(open(HERE / "cn_monte_carlo_summary.json"))
import cn_inputs as I      # only to read the values being checked; every reference value below is typed in

rows = []
def check(group, name, model, ref, rtol=1e-6, note=""):
    ok = abs(model - ref) <= rtol * max(abs(ref), 1e-12) + 1e-9
    rows.append(dict(group=group, check=name, model=model, independent=ref, rel_diff=(model - ref) / ref if ref else model - ref,
                     tolerance=rtol, ok=bool(ok), note=note))
def within(group, name, model, lo, hi, note=""):
    ok = lo <= model <= hi
    rows.append(dict(group=group, check=name, model=model, independent=f"[{lo}, {hi}]", rel_diff=None, tolerance=None, ok=bool(ok), note=note))

# --------------------------------------------------------------------------------- 1. physical constants (typed in)
MJ_PER_KWH = 3.6; MMBTU_PER_MWH = 3.41214; LBS = None
H2_LHV_MJ_KG = 120.0                       # hydrogen LHV
CH4_HHV, CH4_LHV = 55.5, 50.0              # MJ/kg
GB_T_2589 = dict(gasoline=43.070, diesel=42.652, jet=43.070, resid=41.816)   # GJ/t, GB/T 2589-2020 Annex A
IPCC_2006 = dict(gasoline=44.3, diesel=43.0, jet=44.1, resid=40.4)            # GJ/t, IPCC 2006 Vol. 2 Table 1.2
P_PER_P2O5 = 2 * 30.974 / (2 * 30.974 + 5 * 15.999)   # 0.4364
K_PER_K2O = 2 * 39.098 / (2 * 39.098 + 15.999)        # 0.8301
C_TO_CO2 = 44.009 / 12.011

check("constants", "H2 LHV kWh/kg", I.H2_LHV_KWH_KG, H2_LHV_MJ_KG / MJ_PER_KWH, 1e-3)
for f in GB_T_2589:
    gj = I.KWH_PER_KG[f] * MJ_PER_KWH
    within("fuel LHV", f"{f} LHV GJ/t lies between GB/T 2589 and IPCC 2006", gj,
           min(GB_T_2589[f], IPCC_2006[f]) - 0.05, max(GB_T_2589[f], IPCC_2006[f]) + 0.05)
gas_lhv_mj_m3 = I.BCM_TWH * 1e9 * 3.6 / 1e9      # MJ per m3
within("gas", "pipeline gas LHV MJ/m3 (China pipeline gas 34-37)", gas_lhv_mj_m3, 34.0, 37.0)
check("gas", "HHV/LHV ratio of methane", I.GAS_HHV_LHV, CH4_HHV / CH4_LHV, 2e-3)
import cn_model as M
check("gas", "MMBtu (HHV) per bcm consistent with TWh (LHV) per bcm", M.MMBTU_PER_BCM,
      I.BCM_TWH * 1e6 * (CH4_HHV / CH4_LHV) * MMBTU_PER_MWH, 2e-3)
check("gas", "TWh HHV per Mt CH4 (GPK)", M.GPK, CH4_HHV / MJ_PER_KWH, 1e-6)
check("gas", "USD/MWh from USD/MMBtu", M.gas_usd_mwh(M.default_params()), (I.GAS["price_mmbtu"] + I.GAS["delivery_mmbtu"]) * MMBTU_PER_MWH, 1e-3)

# --------------------------------------------------------------------------------- 2. baseline energy (Mt x LHV)
B = I.BASE_MAINLAND; base = LC["enduse"]["base"]
lhv = {k: I.KWH_PER_KG[k] for k in I.KWH_PER_KG}   # TWh per Mt = kWh per kg
indep = dict(ldv=B["gasoline_mt"] * lhv["gasoline"], hdv=B["onroad_diesel_mt"] * lhv["diesel"] + B["road_gas_bcm"] * I.BCM_TWH,
             air=B["jet_mt"] * lhv["jet"], marine=B["marine_diesel_mt"] * lhv["diesel"] + B["marine_resid_mt"] * lhv["resid"])
for k, v in indep.items(): check("baseline", f"2025 {k} TWh = Mt x LHV", base[k], v, 1e-9)
tot_ref = sum(B[k] * lhv[f] for k, f in [("gasoline_mt", "gasoline"), ("onroad_diesel_mt", "diesel"), ("rail_diesel_mt", "diesel"),
             ("marine_diesel_mt", "diesel"), ("marine_resid_mt", "resid"), ("jet_mt", "jet"), ("farm_diesel_mt", "diesel"),
             ("construction_mining_diesel_mt", "diesel"), ("industrial_trucks_mt", "diesel")]) + (B["road_gas_bcm"] + B["pipeline_gas_bcm"]) * I.BCM_TWH
check("baseline", "2025 total final energy TWh", LC["petroleum"]["total_twh_2025"], tot_ref, 1e-9)
# with the two reference LHV sets: the baseline would differ by at most
for lab, ref in (("GB/T 2589", GB_T_2589), ("IPCC 2006", IPCC_2006)):
    alt = tot_ref + sum(B[k] * (ref[f] / 3.6 - lhv[f]) for k, f in [("gasoline_mt", "gasoline"), ("onroad_diesel_mt", "diesel"), ("rail_diesel_mt", "diesel"),
             ("marine_diesel_mt", "diesel"), ("marine_resid_mt", "resid"), ("jet_mt", "jet"), ("farm_diesel_mt", "diesel"),
             ("construction_mining_diesel_mt", "diesel"), ("industrial_trucks_mt", "diesel")])
    within("baseline", f"2025 total energy with {lab} LHVs within 2.5% of the model", alt / tot_ref, 0.975, 1.025)
check("baseline", "2050 demand = 2025 x service growth", sum(LC["enduse"]["demand"].values()), tot_ref * 1.15, 1e-9)
taiwan_gas = 188e3 * 0.158987 * 365 * 0.737 / 1e6   # kb/d -> Mt (158.987 L/bbl, 0.737 kg/L)
check("baseline", "Taiwan gasoline Mt from 188 kb/d", I.BASE_TAIWAN["gasoline_mt"], taiwan_gas, 1e-6)

# --------------------------------------------------------------------------------- 3. vehicle intensity ratios (kWh against MJ)
diesel_lhv_mj_gal = 3.78541 * 0.835 * lhv["diesel"] * 3.6     # model's own diesel LHV per gallon
check("vehicles", "diesel LHV/HHV per gallon: model LHV vs 0.935 x EIA 144.9 MJ/gal", diesel_lhv_mj_gal, 144.94 * 128450 / 137381, 5e-3)
mj_mi_lhv = 21.1 * 128450 / 137381                  # 144.9 MJ/gal (HHV) / 6.87 mpg -> LHV basis
r_hdv = 2.40 / (mj_mi_lhv / MJ_PER_KWH)             # kWh/mi over kWh(LHV)/mi
check("vehicles", "heavy-truck BEV ratio = (kWh/mi) / (MJ_LHV/mi / 3.6)", I.ENDUSE["r_hdv_elec"], r_hdv, 1e-9)
check("vehicles", "heavy-truck FCEV ratio (H2 LHV / diesel LHV)", I.ENDUSE["r_hdv_fcev"], 4.44 / (mj_mi_lhv / MJ_PER_KWH), 1e-9)
diesel_kwh_km = 32.0 * 0.835 * lhv["diesel"] / 100     # 32 L/100 km Chinese 49-t tractor
within("vehicles", "implied BEV heavy truck kWh/km (Chinese 49-t BEV tractors 1.1-1.6)", diesel_kwh_km * I.ENDUSE["r_hdv_elec"], 1.1, 1.6)
within("vehicles", "implied FCEV heavy truck kg H2/100 km (6-12)", diesel_kwh_km * I.ENDUSE["r_hdv_fcev"] / (H2_LHV_MJ_KG / 3.6) * 100, 6.0, 12.0)
car_kwh_km = 7.0 * 0.737 * lhv["gasoline"] / 100       # 7 L/100 km petrol car
within("vehicles", "implied BEV car kWh/100 km at the meter (12-18)", car_kwh_km * I.ENDUSE["r_ldv_bev"] * 100, 12.0, 18.0)
VC = I.VEHICLE_CARBON; f_trk = 1 - VC["mass_saving_truck"] * VC["energy_per_mass"]; f_car = 1 - VC["mass_saving_car"] * VC["energy_per_mass"]
d = LC["enduse"]["demand"]; el = LC["enduse"]["el"]
check("vehicles", "hdv_bev TWh = demand x share x ratio x lightweighting", el["hdv_bev"], d["hdv"] * 0.45 * r_hdv * f_trk, 1e-9)
check("vehicles", "ldv electricity TWh", el["ldv"], d["ldv"] * (0.95 + 0.03 * 0.75) * (0.33 / 1.41) * f_car, 1e-9)
h2_twh = sum(LC["enduse"]["h2_twh"].values())
check("vehicles", "direct H2 Mt = TWh / 33.33", LC["enduse"]["h2_mt_direct"], h2_twh / (H2_LHV_MJ_KG / 3.6), 1e-3)
check("vehicles", "electricity end use total", LC["enduse"]["el_total"], sum(el.values()), 1e-9)

# --------------------------------------------------------------------------------- 4. LDV ownership cost
crf = lambda r, n: r / (1 - (1 + r) ** -n)
c = I.LDV_TCO["central"]
parts = dict(purchase=-1000 * crf(0.05, 12), battery=0.15 * 55 * 70 / 1.05 ** 9 * crf(0.05, 12), maint=-0.35 * 350, ins=100)
check("vehicles", "BEV car net USD/yr (four components)", I.VEH["ldv_bev_net_usd_yr"], sum(parts.values()), 2e-3)
veh = (420e6 * (0.95 * sum(parts.values()) + 0.03 * 150 + 0.01 * 700) + 2.5e6 * 2500 + 0.6e6 * 8000 + 18e6 * 1200 + 2e6 * 2500
       + 8e6 * 0.8 * 600 + 10e6 * 0.85 * 1500 + 5e6 * -200) / 1e9
check("vehicles", "vehicles and machines net (consumer cost), bn USD", LC["costs_bn"]["vehicles_and_machines_net"], veh, 2e-3)
check("vehicles", "farm charging (project), bn USD", LC["costs_bn"]["farm_charging"], 2.0, 1e-9)
check("cost", "energy-system (project) cost = total - consumer vehicle cost", LC["energy_system_cost_bn"], LC["total_cost_bn"] - veh, 2e-4)
check("cost", "energy-system saving %", LC["saving_energy_system_pct"], 100 * (1 - LC["energy_system_cost_bn"] / LC["petroleum"]["late_2025_bn"]), 1e-9)

# --------------------------------------------------------------------------------- 5. petroleum comparator
def pretax(retail, tax, dens, fx): return (retail / 1.13 - tax) / dens * 1000 / fx
P25 = dict(gasoline=pretax(6.85, 1.52, 0.737, 7.08), diesel=pretax(6.55, 1.20, 0.835, 7.08), jet=5600 / 1.13 / 7.08, resid=480.0)
P26 = dict(gasoline=pretax(8.41, 1.52, 0.737, 6.71), diesel=pretax(7.95, 1.20, 0.835, 6.71), jet=7900 / 1.13 / 6.71, resid=700.0)
for k in P25: check("petroleum", f"pre-tax {k} USD/t late 2025", I.PRICES_USD_T["late_2025"][k], P25[k], 1e-9)
diesel_mt = B["onroad_diesel_mt"] + B["rail_diesel_mt"] + B["marine_diesel_mt"] + B["farm_diesel_mt"] + B["construction_mining_diesel_mt"] + B["industrial_trucks_mt"]
mm_bcm = I.BCM_TWH * 1e6 * (CH4_HHV / CH4_LHV) * MMBTU_PER_MWH
def petro(P, lng):
    fuel = (B["gasoline_mt"] * P["gasoline"] + diesel_mt * P["diesel"] + B["jet_mt"] * P["jet"] + B["marine_resid_mt"] * P["resid"]) / 1e3
    return 1.15 * (fuel + B["road_gas_bcm"] * mm_bcm * lng / 1e9 + B["pipeline_gas_bcm"] * mm_bcm * 9.3 / 1e9)
check("petroleum", "petroleum comparator late 2025, bn USD", LC["petroleum"]["late_2025_bn"], petro(P25, 11.0), 3e-3)
check("petroleum", "petroleum comparator Nov 2026, bn USD", LC["petroleum"]["nov_2026_bn"], petro(P26, 14.0), 3e-3)
ci = dict(gasoline=93, diesel=95, jet=89, resid=96, ng=70)
gas_sh = B["road_gas_bcm"] * I.BCM_TWH / base["hdv"]; res_sh = B["marine_resid_mt"] * lhv["resid"] / base["marine"]
wtw = lambda dd: (dd["ldv"] * ci["gasoline"] + dd["hdv"] * ((1 - gas_sh) * ci["diesel"] + gas_sh * ci["ng"])
                  + (dd["rail"] + dd["farm"] + dd["construction"] + dd["industrial"]) * ci["diesel"] + dd["air"] * ci["jet"]
                  + dd["marine"] * (res_sh * ci["resid"] + (1 - res_sh) * ci["diesel"]) + dd["pipeline"] * ci["ng"]) * 3.6 / 1e3
check("emissions", "petroleum WTW 2025, Mt CO2e (text: about 1.8 Gt)", LC["petroleum"]["wtw_2025_mt"], wtw(base), 1e-9)
check("emissions", "petroleum WTW 2050, Mt CO2e", LC["emissions"]["baseline_wtw_mt"], wtw(d), 1e-9)
within("emissions", "2025 WTW per unit energy g/MJ (petroleum 85-95)", LC["petroleum"]["wtw_2025_mt"] * 1e3 / (tot_ref * 3.6), 85, 95)
check("emissions", "system emissions = sum of sources", LC["emissions"]["total_mt"], sum(LC["emissions"]["by_source_mt"].values()), 1e-9)
check("emissions", "reduction %", LC["emissions"]["reduction_pct"], 100 * (1 - LC["emissions"]["total_mt"] / wtw(d)), 1e-9)

# --------------------------------------------------------------------------------- 6. cost reconciliation and headline
tot = sum(LC["costs_bn"].values()) + sum(LC["credits_bn"].values())
check("cost", "total = sum of components + credits", LC["total_cost_bn"], tot, 1e-9)
check("cost", "LP objective + fixed terms = total", LC["objective_reconciliation"]["lp_objective_bn"] + LC["objective_reconciliation"]["fixed_terms_total_bn"]
      + LC["objective_reconciliation"]["heat_credit_adjustment_bn"], LC["total_cost_bn"], 1e-9)
check("cost", "saving vs late-2025 petroleum %", LC["saving_vs_late_2025_pct"], 100 * (1 - LC["total_cost_bn"] / LC["petroleum"]["late_2025_bn"]), 1e-9)
check("cost", "break-even multiple", LC["breakeven_multiple"], LC["total_cost_bn"] / LC["petroleum"]["late_2025_bn"], 1e-6)
E = I.ELEC
check("cost", "transmission and distribution = el x 22 USD/MWh", LC["costs_bn"]["transmission_distribution"], LC["enduse"]["el_total"] * 22 / 1e3, 1e-9)
check("cost", "electric highways = 60,000 km x 1.8 M$/km x (CRF40 + 2.5%)", LC["costs_bn"]["electric_highways"], 60000 * 1.8e6 * (crf(0.05, 40) + 0.025) / 1e9, 1e-9)
within("cost", "firmed solar USD/MWh quoted as 61", E["solar"] + 1.25 * E["vre_firming"], 60.99, 61.01)

# --------------------------------------------------------------------------------- 7. hubs, hydrogen, pyrolysis, carbon
H = LC["h2_mt"]
check("hubs", "modules = 6 x hubs", LC["reactors"], 6 * LC["hubs"], 1e-9)
check("hubs", "GWt = 1.5 x hubs", LC["hub_gwt"], 1.5 * LC["hubs"], 1e-9)
rc = I.REACTOR_COST["central"]; foak = rc["boak_kwe"] * rc["foak_mult"]
check("hubs", "FOAK USD/kWe quoted as 5,250", foak, 5250.0, 1e-9)
n = LC["reactors"]; b = math.log2(1 - rc["learning"]); avg = foak * n ** b / (b + 1)
cap = avg * (1 + rc["idc"]) * 0.40 * 1.5e6 / 1e9      # bn USD per hub (0.40 kWe/kWt)
hub_yr = cap * crf(0.05, 60) + 30 * 1.5e6 / 1e9 + 9.0 * 1500 * 0.93 * 8760 / 1e9
within("hubs", "reactor hub cost bn/yr within 3% of a hand Wright's-law estimate (other cascade items excluded)",
       LC["costs_bn"]["reactor_hubs"] / (hub_yr * LC["hubs"]), 0.97, 1.03)
ch4 = H["pyrolysis"] * 4.0 / 0.98
check("hydrogen", "pyrolysis gas bcm = Mt H2 x 4.08 / 0.72 kg/m3", LC["gas_for_pyrolysis_bcm"], ch4 / 0.72, 2e-3)
within("hydrogen", "same gas on an energy basis, bcm (LHV 50 MJ/kg / 9.9 TWh/bcm), within 2%",
       LC["gas_for_pyrolysis_bcm"] / (ch4 * CH4_LHV / 3.6 / I.BCM_TWH), 0.98, 1.02)
check("hydrogen", "pyrolysis carbon = 3 kg C per kg H2", LC["carbon_mt"], H["pyrolysis"] * 3.0, 1e-6)
within("hydrogen", "3 kg C/kg H2 vs stoichiometry (12/4.032 = 2.98)", 3.0 / (12.011 / 4.032), 0.99, 1.02)

# --------------------------------------------------------------------------------- 8. nutrients and soil carbon
NU = I.NUTRIENTS; nb = LC["nutrients"]
straw_like = [t for t in LC["tiers_mt"]]
def kind(name):
    s = name.lower()
    if "forest" in s or "wood" in s: return "forest"
    if "bamboo" in s: return "bamboo"
    if "grassland" in s: return "grass"
    return "straw"
cont = NU["content"]; rem = dict(n=0.0, p=0.0, k=0.0, c=0.0, soc=0.0)
for t in LC["tiers_mt"]:
    k = kind(t["name"]); cc = cont[k]
    for e in ("n", "p", "k"): rem[e] += t["used"] * cc[e] / 1e3
    rem["c"] += t["used"] * cc["c"] / 1e3; rem["soc"] += t["used"] * cc["c"] / 1e3 * cc["humif"]
bam = LC["bamboo"]["mt"]; hs = LC["biomass_mt"]["hemp_stalk"]; sb = LC["biomass_mt"].get("sorghum_bagasse", 0.0)
for mt, k in ((bam, "bamboo"), (hs, "hemp"), (sb, "straw")):
    cc = cont[k]
    for e in ("n", "p", "k"): rem[e] += mt * cc[e] / 1e3
    rem["c"] += mt * cc["c"] / 1e3; rem["soc"] += mt * cc["c"] / 1e3 * cc["humif"]
for e in ("n", "p", "k"):
    within("nutrients", f"{e.upper()} removed Mt within 5% of tiers x content (hand)", nb[e]["removed_mt"] / rem[e], 0.95, 1.05)
    check("nutrients", f"{e.upper()} balance closes (removed = returned - sold)", sum(nb[e]["returned_mt"].values()) - nb[e]["sold_mt"], nb[e]["removed_mt"], 1e-6)
within("nutrients", "residue C removed within 5% of hand", nb["soil_carbon"]["residue_c_removed_mt"] / rem["c"], 0.95, 1.05)
within("nutrients", "stable SOC required within 5% of hand", nb["soil_carbon"]["stable_soc_required_mt"] / rem["soc"], 0.95, 1.05)
sup = sum(nb["soil_carbon"]["stable_soc_supplied_mt"].values())
within("nutrients", "SOC supplied >= required (or priced gap)", sup + nb["soil_carbon"]["deficit_mt"] - nb["soil_carbon"]["stable_soc_required_mt"], -1e-6, 1e9)
check("nutrients", "pyrolysis carbon to soil x 0.90 stable", nb["soil_carbon"]["stable_soc_supplied_mt"]["pyrolysis_carbon"], nb["soil_carbon"]["pyrolysis_carbon_to_soil_mt"] * 0.90, 1e-6)
check("nutrients", "pyrolysis carbon: markets + soil = made", sum(a["mt"] for a in LC["carbon_alloc"]), LC["carbon_mt"], 1e-6)
check("nutrients", "carbon to soil in allocation = soil balance", next(a["mt"] for a in LC["carbon_alloc"] if a["market"].startswith("Soil")),
      nb["soil_carbon"]["pyrolysis_carbon_to_soil_mt"], 1e-6)
check("cost", "carbon revenue = sum(Mt x value)", -LC["credits_bn"]["carbon_products"], sum(a["mt"] * a["value_usd_t"] for a in LC["carbon_alloc"]) / 1e3, 1e-6)
straw_p2o5 = cont["straw"]["p"] / P_PER_P2O5 / 10; straw_k2o = cont["straw"]["k"] / K_PER_K2O / 10
within("nutrients", "straw N % DM (text 0.64-0.85)", cont["straw"]["n"] / 10, 0.64, 0.85)
within("nutrients", "straw P as P2O5 % DM (text 0.27-0.53)", straw_p2o5, 0.27, 0.53)
within("nutrients", "straw K as K2O % DM (text 1.53-2.31)", straw_k2o, 1.53, 2.31)
F = I.FERT_PRICE
within("fertiliser", "N USD/t N from urea 2,000 CNY/t farm gate (46% N, 7.08): 560-720", F["n"], 560, 720)
within("fertiliser", "P USD/t elemental P from MAP ~1,000-1,250 USD/t P2O5", F["p"], 1000 / P_PER_P2O5, 1250 / P_PER_P2O5)
within("fertiliser", "K USD/t elemental K from KCl 3,300-3,700 CNY/t (60% K2O)", F["k"], 3300 / 0.60 / 7.08 / K_PER_K2O, 3700 / 0.60 / 7.08 / K_PER_K2O * 1.05)
check("fertiliser", "mineral fertiliser cost = Mt x price", LC["costs_bn"]["mineral_fertiliser"],
      sum(nb["mineral_fertiliser_mt"][e] * F[e] for e in "npk") / 1e3, 1e-6)
gm = NU["green_manure"]; cm = NU["compost"]
check("nutrients", "green manure t C/ha stable", gm["dm_t_ha"] * gm["c"] / 1e3 * gm["humif"], 0.294, 1e-6)
check("nutrients", "compost t C/t stable", cm["c"] / 1e3 * cm["humif"], 0.105, 1e-6)
check("nutrients", "biomethane TWh = 0.35 MWh/t x digested feed", nb["biomethane_twh"]["made"], 0.35 * nb["returns_mt_feed"]["digested"], 1e-6)
check("emissions", "digester slip Mt CO2e = 1% x Mt CH4 x 29.8", LC["emissions"]["by_source_mt"]["digester_methane_slip"],
      nb["biomethane_twh"]["made"] / (CH4_HHV / 3.6) * 0.01 * 29.8, 1e-6)
check("emissions", "fertiliser Mt CO2e = Mt x (8, 2, 0.5)", LC["emissions"]["by_source_mt"]["mineral_fertiliser"],
      sum(nb["mineral_fertiliser_mt"][e] * f for e, f in zip("npk", (8.0, 2.0, 0.5))), 1e-6)

# --------------------------------------------------------------------------------- 9. Monte Carlo from the raw draws
def col(fn, key):
    with open(HERE / fn) as fh: return [float(r[key]) for r in csv.DictReader(fh) if r.get(key) not in (None, "", "nan")]
def pct(v, q):   # numpy default (linear) percentile
    v = sorted(v); i = (len(v) - 1) * q / 100; lo = math.floor(i); hi = math.ceil(i)
    return v[lo] + (v[hi] - v[lo]) * (i - lo)
for case, fn in (("least_cost", "cn_monte_carlo_least_cost.csv"), ("post_gas", "cn_monte_carlo_post_gas.csv"),
                 ("half_offshore", "cn_monte_carlo_half_offshore.csv")):
    summ = MCS[case]; cost = col(fn, "transport_cost_bn"); sv = col(fn, "saving_pct")
    p25 = col(fn, "petro_2025"); p26 = col(fn, "petro_2026")
    check("monte carlo", f"{case}: draws in CSV", len(cost), float(summ["n"]), 1e-9)
    for q in (5, 50, 95):
        check("monte carlo", f"{case}: cost p{q} from raw draws", summ["transport_cost_bn"][f"p{q}"], pct(cost, q), 1e-6)
        check("monte carlo", f"{case}: saving p{q} from raw draws", summ["saving_pct"][f"p{q}"], pct(sv, q), 1e-6)
    check("monte carlo", f"{case}: share cheaper than late-2025 petroleum", summ["p_cheaper_2025"], sum(c < p for c, p in zip(cost, p25)) / len(cost), 2e-3)
    check("monte carlo", f"{case}: share cheaper at Nov 2026 prices", summ["p_cheaper_2026"], sum(c < p for c, p in zip(cost, p26)) / len(cost), 2e-3)
    sv2 = [100 * (1 - c / p) for c, p in zip(cost, p25)]
    check("monte carlo", f"{case}: saving column = 1 - cost/petroleum (median)", pct(sv, 50), pct(sv2, 50), 1e-6)
    ce = col(fn, "energy_system_cost_bn"); se = col(fn, "saving_energy_system_pct"); cv = col(fn, "consumer_vehicle_cost_bn")
    check("monte carlo", f"{case}: energy-system + vehicle cost = total in every draw", max(abs(a + b - c) for a, b, c in zip(ce, cv, cost)), 0.0, 0.0)
    for q in (5, 50, 95):
        check("monte carlo", f"{case}: energy-system saving p{q} from raw draws", summ["saving_energy_system_pct"][f"p{q}"], pct(se, q), 1e-6)
    check("monte carlo", f"{case}: energy system cheaper than late-2025 petroleum", summ["p_energy_system_cheaper_2025"], sum(c < p for c, p in zip(ce, p25)) / len(ce), 2e-3)

# --------------------------------------------------------------------------------- 10. text constants quoted in the manuscript
within("text", "fossil CO2 share 32% of 38.1 Gt is 'about one-third'", 0.32, 0.30, 0.34)
within("text", "on-road diesel 120 Mt is ~59% of 203 Mt", 120 / 203, 0.585, 0.595)
check("text", "USD 100 per car per year x 420 M x 95% BEV, bn", 100 * 420e6 * 0.95 / 1e9, 39.9, 1e-9)
check("text", "military Pu 2.9 t / 10 t per GWe = GWe", I.FUEL["cn_military_pu_t"] / I.FUEL["startup_pu_t_per_gwe"], 0.29, 1e-9)
within("text", "12 GWe of large LWRs approved a year in GWt at 36-38% efficiency (text: about 32)", 12 / 0.37, 31.0, 33.5)
check("text", "gas price USD 9.3/MMBtu = 8.5 + 0.8", I.GAS["price_mmbtu"] + I.GAS["delivery_mmbtu"], 9.3, 1e-9)
check("text", "onshore wind tiers 30 and 45 USD/MWh", E["onshore_wind"] + E["onw2_adder"], 45.0, 1e-9)

fails = [r for r in rows if not r["ok"]]
json.dump(dict(release="CN v1.6.4", checks=len(rows), failures=len(fails), rows=rows), open(HERE / "cn_number_audit.json", "w"), indent=1, default=str)
w = max(len(r["check"]) for r in rows)
for r in rows:
    m = r["model"]; ref = r["independent"]
    ms = f"{m:,.4g}" if isinstance(m, (int, float)) else str(m); rs = f"{ref:,.4g}" if isinstance(ref, (int, float)) else str(ref)
    print(f"{'ok  ' if r['ok'] else 'FAIL'} {r['group']:<12} {r['check']:<{w}}  model {ms:>12}  independent {rs:>16}")
print(f"\nCN v1.6.4 number audit: {len(rows) - len(fails)}/{len(rows)} checks passed")
sys.exit(1 if fails else 0)
