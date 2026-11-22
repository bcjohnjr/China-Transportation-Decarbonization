"""China transport-energy system, CN v1.3: reactor heat cascade (HTR-PM-class hubs, with thorium molten-salt, sodium-fast,
very-high-temperature and light-water SMR alternatives) + methane pyrolysis while gas lasts, steam electrolysis after it
+ electric expressways and battery-electric vehicles + wind, solar, concentrated solar and offshore wind with region-
specific seaweeds harvested by Grid Harvesters + crop residues, bamboo, hemp and the autonomous regions' energy crops
(cassava, sugarcane, sweet sorghum, Jerusalem artichoke, sweet potato, jatropha, cotton stalks) + food from the heat
cascade.  USD 2026.  Structure follows the U.S. model v8.4 (us2_model.py); differences are listed in CHANGELOG.md.

    python3 cn_model.py [n_monte_carlo]      -> *.json, *.csv in this folder

Annual least-cost linear programme (HiGHS via SciPy) for 2050 plus accounting modules.  Screening model, not a forecast.
"""
from __future__ import annotations
import copy, json, math, csv
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

import cn_inputs as I
from grid_harvester import fleet_sizing, energy as gh_energy, turning as gh_turning

OUT = Path(__file__).resolve().parent
crf = lambda r, n: r / (1 - (1 + r) ** -n)
MMBTU_PER_BCM = 36.0e6                       # HHV basis, ~38 MJ/m3 [A]
HX_EFF, HX_COST = 0.95, 2.0


# ============================================================================================= parameters
def default_params(system="mainland"):
    names = ["ENDUSE", "ELEC", "HTGR", "PYRO", "GAS", "ELECTROLYSIS", "H2_DELIVERY", "BIOMASS", "BAMBOO", "HEMP", "ROUTES",
             "SEAWEED_PROCESS", "LOGISTICS", "VEH", "FOOD", "NUCLEAR_H2", "AG", "FERT_PRICE", "VEHICLE_CARBON", "EMIS"]
    p = {n: copy.deepcopy(getattr(I, n)) for n in names}
    p["BASE"] = copy.deepcopy(I.BASE_MAINLAND)
    p["SEAWEED"] = copy.deepcopy(I.SEAWEED)
    p["ETHANOL_FEEDS"] = [list(r) for r in I.ETHANOL_FEEDS]
    p["OIL_FEEDS"] = [list(r) for r in I.OIL_FEEDS]
    p["CARBON"] = [list(m) for m in I.CARBON_MARKETS]
    p["WACC"] = I.WACC; p["yield_level"] = 1; p["reactor_case"] = "central"; p["osw_scale"] = 0.0
    p["system"] = system; p["capex_mult"] = 1.0; p["reactor_type"] = "htr_pm"
    p["food_credit_in_transport"] = False   # CN v1.2: heat sold to food is outside the transport cost boundary
    if system == "taiwan":
        T = I.TAIWAN
        p["BASE"] = copy.deepcopy(T["BASE"]); p["ELEC"].update(T["ELEC"]); p["BIOMASS"] = copy.deepcopy(T["BIOMASS"])
        p["ETHANOL_FEEDS"] = [list(r) for r in T["ETHANOL_FEEDS"]]; p["OIL_FEEDS"] = [list(r) for r in T["OIL_FEEDS"]]
        p["BAMBOO"]["regions"] = [("Taiwan hill land", T["BAMBOO_MHA"], "taiwan")]
        p["HEMP"]["max_mha"] = T["HEMP_MAX"]; p["HEMP"]["regions"] = [("none", 0.0, "taiwan")]
        p["GAS"].update(T["GAS"]); p["VEH"].update(T["VEH"]); p["SEAWEED"] = copy.deepcopy(I.SEAWEED_TAIWAN)
        p["CARBON"] = [[m[0], m[1] * T["CARBON_SCALE"] if j < len(p["CARBON"]) - 1 else m[1], m[2]] for j, m in enumerate(p["CARBON"])]
        for k in ("greenhouse_market_mt", "ras_market_mt", "grain_near_hub_mt", "seaweed_food_dry_mt"):
            p["FOOD"][k] *= T["FOOD_SCALE"]
        for k in ("head_feedlot_m", "head_dairy_m", "head_grazing_m"): p["AG"][k] *= 0.01
        p["AG"]["enteric_mt"] *= 0.01
        p["VEHICLE_CARBON"]["cars_m"] = 0.4; p["VEHICLE_CARBON"]["trucks_m"] = 0.05
        p["capex_mult"] = T["REACTOR_COST_MULT"]
    p["g_ref"] = p["ENDUSE"]["service_growth_2050"]   # vehicle stocks are specified for this (central) growth
    return p


def apply_reactor_type(p, rtype):
    """Hub built from one of the reactor technologies in I.REACTOR_TYPES (outlet temperature, efficiency, cost, fuel)."""
    p = copy.deepcopy(p); R = I.REACTOR_TYPES[rtype]; H = p["HTGR"]
    H["outlet_c"] = R["outlet_c"]; H["eta_cond"] = R["eta"]; H["fuel_mwhth"] = R["fuel_mwhth"]; H["f_pyro"] = R["f_pyro"]
    p["capex_mult"] = p.get("capex_mult", 1.0) * R["cost_mult"]; p["reactor_type"] = rtype
    p["PYRO"]["config"] = "vhtr" if R["outlet_c"] >= 900 else "preheat"
    return p


# ============================================================================================= reactor cost (learning)
def reactor_cost(case="central", n_units=500, mwe_per_unit=100.0):
    """Wright's-law learning per reactor module: cost(n) = FOAK * n^b, b = log2(1 - learning rate)."""
    c = I.REACTOR_COST[case]; foak = c["boak_kwe"] * c["foak_mult"]; b = math.log2(1 - c["learning"]); n = max(n_units, 1)
    avg = foak * (n ** (b + 1)) / ((b + 1) * n); unit = lambda k: foak * k ** b
    k2t = I.HTGR["kwe_per_kwt"]
    return dict(case=case, n_units=n, foak_kwe=foak, unit10_kwe=unit(10), unit100_kwe=unit(100), last_kwe=unit(n),
                fleet_avg_kwe=avg, fleet_avg_kwe_with_idc=avg * (1 + c["idc"]), fleet_avg_kwt_with_idc=avg * (1 + c["idc"]) * k2t,
                learning=c["learning"], fleet_capex_bn=avg * (1 + c["idc"]) * n * mwe_per_unit * 1000 / 1e9)


# ============================================================================================= demand
def base_demand(p):
    B = p["BASE"]; g = p["ENDUSE"]["service_growth_2050"]; K = I.KWH_PER_KG
    d = dict(ldv=B["gasoline_mt"] * K["gasoline"],
             hdv=B["onroad_diesel_mt"] * K["diesel"] + B["road_gas_bcm"] * I.BCM_TWH,
             rail=B["rail_diesel_mt"] * K["diesel"], air=B["jet_mt"] * K["jet"],
             marine=B["marine_diesel_mt"] * K["diesel"] + B["marine_resid_mt"] * K["resid"],
             pipeline=B["pipeline_gas_bcm"] * I.BCM_TWH, farm=B["farm_diesel_mt"] * K["diesel"],
             construction=B["construction_mining_diesel_mt"] * K["diesel"], industrial=B["industrial_trucks_mt"] * K["diesel"])
    return {k: v * g for k, v in d.items()}, d


def enduse_2050(p):
    d, base = base_demand(p); E = p["ENDUSE"]; rf = E["re_fuel_share"]; VC = p["VEHICLE_CARBON"]; lw = p.get("lightweight", True)
    f_car = 1 - VC["mass_saving_car"] * VC["energy_per_mass"] if lw else 1.0
    f_trk = 1 - VC["mass_saving_truck"] * VC["energy_per_mass"] if lw else 1.0
    el, h2, liq = {}, {}, {}
    L = E["ldv"]
    el["ldv"] = d["ldv"] * (L["bev"] + L["re"] * (1 - rf)) * E["r_ldv_bev"] * f_car
    h2["ldv"] = d["ldv"] * L["fcev"] * E["r_ldv_fcev"] * f_car
    liq["ldv"] = d["ldv"] * (L["liquid"] + L["re"] * rf)
    H = E["hdv"]; re_ = E["r_hdv_elec"] * f_trk
    el["hdv_ers_wire"] = d["hdv"] * H["ers"] * E["ers_on_wire"] * re_
    el["hdv_ers_battery"] = d["hdv"] * H["ers"] * (1 - E["ers_on_wire"]) * re_
    el["hdv_bev"] = d["hdv"] * H["bev"] * re_
    el["hdv_re"] = d["hdv"] * H["re"] * (1 - rf) * re_
    h2["hdv"] = d["hdv"] * H["fcev"] * E["r_hdv_fcev"] * f_trk
    liq["hdv"] = d["hdv"] * (H["liquid"] + H["re"] * rf)
    for seg in ("farm", "construction"):
        S = E[seg]; el[seg] = d[seg] * (S["bev"] + S["re"] * (1 - rf)) * E["r_offroad_elec"]; liq[seg] = d[seg] * (S["liquid"] + S["re"] * rf)
    el["industrial"] = d["industrial"] * E["industrial"]["bev"] * E["r_fork_elec"]; h2["industrial"] = d["industrial"] * E["industrial"]["fcev"] * 0.55
    R = E["rail"]; el["rail"] = d["rail"] * (R["elec"] + R["re"] * (1 - rf)) * E["r_rail_elec"]; liq["rail"] = d["rail"] * (R["liquid"] + R["re"] * rf)
    h2["air"] = d["air"] * E["air"]["h2"]; liq["air"] = d["air"] * E["air"]["saf"]
    el["marine"] = d["marine"] * E["marine"]["elec"] * 0.40; h2["marine"] = d["marine"] * E["marine"]["h2"]; liq["marine"] = d["marine"] * E["marine"]["liquid"]
    el["pipeline"] = d["pipeline"] * E["pipeline"]["elec"] * E["r_pipe_elec"]
    return dict(demand=d, base=base, el=el, h2_twh=h2, liq=liq, gas_resid_twh=d["pipeline"] * E["pipeline"]["gas"],
                el_total=sum(el.values()), h2_mt_direct=sum(h2.values()) / I.H2_LHV_KWH_KG, liq_total=sum(liq.values()), jet=liq["air"])


def blend_h2(p, vol_frac):
    if vol_frac <= 0: return dict(h2_mt=0.0, gas_displaced_bcm=0.0, energy_share=0.0, co2_avoided_burner_mt=0.0)
    share = vol_frac * 10.8 / (vol_frac * 10.8 + (1 - vol_frac) * 35.8)
    h2_twh = share * I.NG["res_com_bcm"] * I.BCM_TWH
    disp = h2_twh / I.BCM_TWH
    return dict(h2_mt=h2_twh / I.H2_LHV_KWH_KG, gas_displaced_bcm=disp, energy_share=share, co2_avoided_burner_mt=disp * 0.72 * 44 / 16)


# ============================================================================================= hub
def hub(p, capex_kwt):
    H = p["HTGR"]; hrs = 8760 * H["cf"]; W = p["WACC"]
    q_pyro, q_mid, q_dry = H["mwt"] * H["f_pyro"], H["mwt"] * H["f_mid"], H["mwt"] * H["f_dry"]
    steam = H["mwt"] - q_pyro
    mwe = H["eta_cond"] * steam - H["z_mid"] * q_mid - H["z_dry"] * q_dry
    reject = steam - mwe - q_mid - q_dry
    cost = (H["mwt"] * 1000 * capex_kwt * crf(W, H["life"]) + H["mwt"] * 1000 * H["fom_kwt_yr"] + H["mwt"] * hrs * H["fuel_mwhth"]) / 1e9
    return dict(mwt=H["mwt"], q_pyro_mw=q_pyro, q_mid_mw=q_mid, q_dry_mw=q_dry, mwe=mwe, reject_mw=reject, low_used_mw=reject * H["f_low_use"],
                pyro_twh=q_pyro * hrs / 1e6, mid_twh=q_mid * hrs / 1e6, dry_twh=q_dry * hrs / 1e6, el_twh=mwe * hrs / 1e6,
                low_twh=reject * H["f_low_use"] * hrs / 1e6, cost_bn=cost, capex_kwt=capex_kwt)


def htse_superheat_elec(p, with_reactor=True):
    """Electricity (kWh/kg H2) for electric superheating of steam to the stack inlet temperature."""
    h = p["NUCLEAR_H2"]["htse"]
    if with_reactor and p["HTGR"].get("outlet_c", 750) >= 850: return 0.0
    return (h["superheat_kwh_kg"] if with_reactor else h["superheat_noreactor_kwh_kg"]) / h["heater_eff"]


def pyro_reactor_heat(p):
    """kWh of reactor heat per kg H2 for pyrolysis: methane sensible preheat to ~50 C below the reactor outlet, or the
    full 8.3 kWh/kg for a >=900 C reactor."""
    P = p["PYRO"]; T = p["HTGR"]["outlet_c"]
    if P.get("config") == "vhtr" or T >= 900: return P["heat_kwh_kg"]
    return min(P["cp_ch4"] * max(T - 75, 0) * P["kg_ch4_per_kg_h2"] / 3600, P["heat_kwh_kg"])


def pyro_elec(p):
    P = p["PYRO"]; return P["elec_kwh_kg"] + (P["heat_kwh_kg"] - pyro_reactor_heat(p)) / P["boost_eff"]


def pyro_cost_per_kg(p):
    P = p["PYRO"]; kw = I.H2_LHV_KWH_KG / (8760 * 0.93)
    boost = 0.0 if pyro_reactor_heat(p) >= P["heat_kwh_kg"] else P["boost_heater_cost_kg"]
    plant = kw * P["capex_kw_h2"] * (crf(p["WACC"], P["life"]) + P["fom"]) + boost
    gas = P["kg_ch4_per_kg_h2"] * 55.5 / 1055.06 * (p["GAS"]["price_mmbtu"] + p["GAS"]["delivery_mmbtu"])
    return plant, gas


def h2_ci(p, elec_ci=0.0):
    P = p["PYRO"]; ch4 = P["kg_ch4_per_kg_h2"]; L = P["leak_upstream"]
    return ch4 * L / (1 - L) * P["gwp_ch4"] + ch4 * P["upstream_co2_frac"] * 44 / 16 + (ch4 - 4.0) * 44 / 16 + P["h2_leak"] * P["gwp_h2"] + pyro_elec(p) * elec_ci


# ============================================================================================= seaweed and bamboo costs
def seaweed_zone_economics(p, z):
    S, L = p["SEAWEED_PROCESS"], p["LOGISTICS"]; W = p["WACC"]
    y = z[5][p["yield_level"]]; km = z[10]
    farm = S["farm_cost_ref_t"] * (0.4 + 0.6 * S["ref_yield"] / y) * (1 - S["shared_mooring_saving"]); farm_ex = farm * 0.80
    ha_per_t = 1 / y
    passes = 3.0 if "giant" in z[12] else (2.0 if ("rotation" in z[12] or "red" in z[12]) else 1.0)
    unit_ha_yr = 3.333 * L["gh_hours"]
    gh_cost_t = L["gh_unit_capex"] * (crf(W, L["gh_life"]) + 0.05) * ha_per_t * passes / unit_ha_yr
    gh_kwh_t = L["gh_kwh_per_ha_pass"] * passes * ha_per_t
    wet_t = 1 / L["press_to_dm"]
    trip_h = 2 * km / (L["vessel_kn"] * 1.852) + L["load_hours"]; trips_yr = L["vessel_days"] * 24 / trip_h
    t_dry_per_vessel_yr = trips_yr * L["vessel_t"] * L["press_to_dm"]
    vessel_cost_t = L["vessel_capex"] * (crf(W, L["vessel_life"]) + L["vessel_om"]) / t_dry_per_vessel_yr
    vessel_kwh_t = wet_t * 2 * km * L["vessel_kwh_tkm"] * (1 - L["vessel_sail_share"]) * 0.6
    drone_cost_t = ha_per_t / 100 / L["drone_km2"] * (L["drone_capex"] * crf(W, L["drone_life"]) + L["drone_om_yr"])
    F = p["FERT_PRICE"]; fert = z[7] * S["n_rec"] * F["n"] + S["p"] * S["p_rec"] * F["p"] + S["k"] * S["k_rec"] * F["k"]
    return dict(yield_t_ha=y, farm_t=farm_ex, harvester_t=gh_cost_t, vessel_t=vessel_cost_t, drones_t=drone_cost_t, fert_credit_t=fert,
                biomass_cost_t=farm_ex + gh_cost_t + vessel_cost_t + drone_cost_t, harvester_kwh_t=gh_kwh_t, vessel_kwh_t=vessel_kwh_t,
                t_dry_per_vessel_yr=t_dry_per_vessel_yr, passes=passes)


def bamboo_cost_t(p):
    B = p["BAMBOO"]; y = B["yield_t_ha"][p["yield_level"]]
    return (B["establish_usd_ha"] * crf(p["WACC"], B["establish_life"]) + B["land_rent_usd_ha"]) / y + B["harvest_usd_t"] + B["haul_usd_t"], y


# ============================================================================================= LP
def solve(p, scenario="design", blend_vol=0.0, capex_kwt=1300.0, osw_scale=None, kelp_force=None, allow_ely=None,
          flex_heat=False, post_gas=False, allow_si=False, fixed_hubs=None):
    if osw_scale is None: osw_scale = p["osw_scale"] if scenario.startswith("design") else 0.0
    if kelp_force is None: kelp_force = scenario.startswith("design")
    if allow_ely is None: allow_ely = True
    eu = enduse_2050(p); E = p["ELEC"]; R = p["ROUTES"]; S = p["SEAWEED_PROCESS"]; hb = hub(p, capex_kwt); bl = blend_h2(p, blend_vol)
    pl, pg = pyro_cost_per_kg(p); bam_cost, bam_y = bamboo_cost_t(p); HM = p["HEMP"]; Z = p["SEAWEED"]
    zec = {z[0]: seaweed_zone_economics(p, z) for z in Z}
    tiers = p["BIOMASS"]["tiers"]; EF = p["ETHANOL_FEEDS"]; OF = p["OIL_FEEDS"]
    names = ["onw", "onw2", "pv", "csp", "lwr", "export", "liq_import", "hubs", "hp2e", "h_pyro", "h_ely", "bamboo", "hemp_mha", "htl", "pbtl",
             "cel", "atj", "etoh_ldv", "hemp_oil_fuel", "e_heat", "e_dry", "heat_sold", "t2mid", "t2dry", "m2dry", "h_htse", "h_si", "m2e", "d2e"]
    names += [f"b{j}" for j in range(len(tiers))] + [f"eth_{f[0]}" for f in EF] + [f"oil_{f[0]}" for f in OF]
    names += [f"osw_{z[0]}" for z in Z] + [f"kh_{z[0]}" for z in Z] + [f"kp_{z[0]}" for z in Z] + [f"c{j}" for j in range(len(p["CARBON"]))]
    ix = {n: i for i, n in enumerate(names)}; nv = len(names); c = np.zeros(nv); firm = E["vre_firming"]; onsite = p["H2_DELIVERY"]["onsite"]
    c[ix["onw"]] = (E["onshore_wind"] + firm) / 1e3; c[ix["onw2"]] = (E["onshore_wind"] + E["onw2_adder"] + firm) / 1e3; c[ix["pv"]] = (E["solar"] + 1.25 * firm) / 1e3
    c[ix["csp"]] = E["csp"] / 1e3; c[ix["lwr"]] = E["lwr"] / 1e3; c[ix["export"]] = -E["export_value"] / 1e3
    c[ix["liq_import"]] = E["liq_import_usd_mwh"] / 1e3
    c[ix["hubs"]] = hb["cost_bn"]; c[ix["h_pyro"]] = pl + pg; c[ix["h_ely"]] = p["ELECTROLYSIS"]["capex_cost_kg"]
    for j, t in enumerate(tiers): c[ix[f"b{j}"]] = t[3] / 1e3
    for f in EF: c[ix[f"eth_{f[0]}"]] = f[4]
    for f in OF: c[ix[f"oil_{f[0]}"]] = (f[4] + R["hefa"]["conv_t"] + onsite * R["hefa"]["h2_kg_t"]) / 1e3
    c[ix["bamboo"]] = bam_cost / 1e3
    c[ix["hemp_mha"]] = (HM["cost_usd_ha"] - HM["seed_t_ha"] * (1 - HM["oil_frac"]) * HM["meal_value_usd_t"]) * 1e6 / 1e9
    c[ix["htl"]] = (R["htl"]["cost_t"] + onsite * R["htl"]["h2_kg_t"]) / 1e3; c[ix["pbtl"]] = (R["pbtl"]["cost_t"] + onsite * R["pbtl"]["h2_kg_t"]) / 1e3
    c[ix["cel"]] = R["ethanol"]["cellulosic_gal_per_t"] * R["ethanol"]["cellulosic_conv_per_gal"] / 1e3
    c[ix["atj"]] = R["atj"]["conv_per_bgal"] / 1e9
    c[ix["hemp_oil_fuel"]] = (R["hefa_conv_only"] + onsite * R["hefa"]["h2_kg_t"]) / 1e3
    c[ix["e_heat"]] = 2.0 / 1e3; c[ix["e_dry"]] = 8.0 / 1e3; c[ix["heat_sold"]] = -8.0 / 1e3 if p.get("food_credit_in_transport", False) else 0.0
    for k in ("t2mid", "t2dry", "m2dry"): c[ix[k]] = HX_COST / 1e3
    c[ix["h_htse"]] = p["NUCLEAR_H2"]["htse"]["capex_cost_kg"]; c[ix["h_si"]] = p["NUCLEAR_H2"]["sulfur_iodine"]["capex_cost_kg"]
    for z in Z:
        lcoe = E["osw_fixed"] if z[1] == "fixed" else E["osw_floating"]; c[ix[f"osw_{z[0]}"]] = (lcoe + 0.5 * firm) / 1e3
        e = zec[z[0]]
        c[ix[f"kh_{z[0]}"]] = (e["biomass_cost_t"] - e["fert_credit_t"] + S["htl_cost_t"] + onsite * S["htl_h2_kg_t"]) / 1e3
        c[ix[f"kp_{z[0]}"]] = (e["biomass_cost_t"] - e["fert_credit_t"] + S["pbtl_cost_t"] + onsite * S["pbtl_h2_kg_t"]) / 1e3
    for j, m in enumerate(p["CARBON"]): c[ix[f"c{j}"]] = -m[2] / 1e3
    A, b, Aeq, beq, labels = [], [], [], [], []
    def row(d):
        r = np.zeros(nv)
        for k, v in d.items(): r[ix[k]] += v
        return r
    def le(d, rhs, lab=""): A.append(row(d)); b.append(rhs); labels.append(lab)
    def eq(d, rhs): Aeq.append(row(d)); beq.append(rhs)
    osw = [f"osw_{z[0]}" for z in Z]; kh = [f"kh_{z[0]}" for z in Z]; kp = [f"kp_{z[0]}" for z in Z]
    oils = [f"oil_{f[0]}" for f in OF]; eths = [f"eth_{f[0]}" for f in EF]
    NH = p["NUCLEAR_H2"]; HT = p["HTGR"]
    # electricity
    load = {"h_pyro": pyro_elec(p), "h_ely": p["ELECTROLYSIS"]["kwh_kg"], "h_htse": NH["htse"]["kwh_e_kg"] + htse_superheat_elec(p, with_reactor=(fixed_hubs is None or fixed_hubs > 0)), "h_si": NH["sulfur_iodine"]["kwh_e_kg"],
            "htl": R["htl"]["el_mwh_t"], "pbtl": R["pbtl"]["el_mwh_t"], "hemp_oil_fuel": R["hefa"]["el_mwh_t"], "e_heat": 1.0, "e_dry": 1.0,
            "export": 1.0, "cel": 0.25}
    for o in oils: load[o] = R["hefa"]["el_mwh_t"]
    for z in Z:
        load[f"kh_{z[0]}"] = S["htl_el_mwh_t"] + zec[z[0]]["vessel_kwh_t"] / 1000; load[f"kp_{z[0]}"] = S["pbtl_el_mwh_t"] + zec[z[0]]["vessel_kwh_t"] / 1000
    r_ = dict(load)
    for s_ in ["onw", "onw2", "pv", "csp", "lwr"] + osw: r_[s_] = r_.get(s_, 0) - 1
    r_["hubs"] = -hb["el_twh"]; r_["hp2e"] = -HT["eta_cond"]; r_["m2e"] = -HT["z_mid"]; r_["d2e"] = -HT["z_dry"]
    le(r_, -eu["el_total"], "electricity")
    sup = ["onw", "onw2", "pv", "csp", "lwr"] + osw
    r_ = {s_: -E["max_pv_share"] for s_ in sup}; r_["pv"] += 1; r_["hubs"] = -E["max_pv_share"] * hb["el_twh"]; le(r_, 0.0, "pv_share")
    le({"lwr": -1, "csp": -E["csp_firm_credit"], "hubs": -hb["el_twh"], "hp2e": -HT["eta_cond"]}, -E["min_firm_share"] * eu["el_total"], "firm")
    # heat tiers
    le({"h_pyro": pyro_reactor_heat(p), "hp2e": 1.0, "hubs": -hb["pyro_twh"], "t2mid": 1.0, "t2dry": 1.0, "h_si": NH["sulfur_iodine"]["kwh_th_kg"],
        "h_htse": NH["htse"]["superheat_kwh_kg"] if HT.get("outlet_c", 750) >= 850 else 0.0}, 0.0, "top_heat")
    r_ = {"htl": R["htl"]["heat_mwh_t"], "hemp_oil_fuel": R["hefa"]["heat_mwh_t"], "hubs": -hb["mid_twh"], "e_heat": -0.98, "t2mid": -HX_EFF, "m2dry": 1.0, "m2e": 1.0,
          "h_htse": NH["htse"]["kwh_th_kg"]}   # CN v1.2: steam generation for electrolysis is process-steam (mid-tier) heat
    for o in oils: r_[o] = R["hefa"]["heat_mwh_t"]
    for k in kh: r_[k] = S["htl_heat_mwh_t"]
    le(r_, 0.0, "mid_heat")
    r_ = {k: S["pbtl_dry_mwh_t"] for k in kp}; r_.update({"hubs": -hb["dry_twh"], "e_dry": -2.5, "cel": 0.6, "t2dry": -HX_EFF, "m2dry": -HX_EFF,
                                                         "d2e": 1.0}); le(r_, 0.0, "dry_heat")
    # hydrogen
    r_ = {"h_pyro": -1, "h_ely": -1, "h_htse": -1, "h_si": -1, "htl": R["htl"]["h2_kg_t"] / 1e3, "pbtl": R["pbtl"]["h2_kg_t"] / 1e3,
          "hemp_oil_fuel": R["hefa"]["h2_kg_t"] / 1e3}
    for o in oils: r_[o] = R["hefa"]["h2_kg_t"] / 1e3
    for k in kh: r_[k] = S["htl_h2_kg_t"] / 1e3
    for k in kp: r_[k] = S["pbtl_h2_kg_t"] / 1e3
    le(r_, -(eu["h2_mt_direct"] + bl["h2_mt"]), "hydrogen")
    # liquids and jet
    mw = {"htl": R["htl"]["mwh_t"], "pbtl": R["pbtl"]["mwh_t"], "hemp_oil_fuel": R["hefa"]["mwh_t"], "atj": R["atj"]["mwh_per_bgal"], "etoh_ldv": R["ethanol"]["mwh_per_bgal"]}
    jf = {"htl": R["htl"]["jet"], "pbtl": R["pbtl"]["jet"], "hemp_oil_fuel": R["hefa"]["jet"], "atj": R["atj"]["jet"], "etoh_ldv": 0.0}
    for o in oils: mw[o] = R["hefa"]["mwh_t"]; jf[o] = R["hefa"]["jet"]
    for k in kh: mw[k] = S["htl_mwh_t"]; jf[k] = R["htl"]["jet"]
    for k in kp: mw[k] = S["pbtl_mwh_t"]; jf[k] = R["pbtl"]["jet"]
    r_ = {k: -v for k, v in mw.items()}; r_["liq_import"] = -1.0; le(r_, -eu["liq_total"], "liquids")
    r_ = {k: -mw[k] * jf[k] for k in mw}; r_["liq_import"] = -1.0; le(r_, -eu["jet"], "jet")
    le({"etoh_ldv": mw["etoh_ldv"]}, eu["liq"]["ldv"], "ethanol_ldv")
    r_ = {e: 1 for e in eths}; r_.update({"cel": R["ethanol"]["cellulosic_gal_per_t"] / 1e3, "atj": -1, "etoh_ldv": -1}); eq(r_, 0.0)
    r_ = {"htl": 1, "pbtl": 1, "cel": 1, "bamboo": -1, "hemp_mha": -HM["stalk_t_ha"]}
    for j in range(len(tiers)): r_[f"b{j}"] = -1
    for f in EF:
        if f[5] > 0: r_[f"eth_{f[0]}"] = -f[5]
    eq(r_, 0.0)
    le({"hemp_oil_fuel": 1, "hemp_mha": -HM["seed_t_ha"] * HM["oil_frac"]}, 0.0, "hemp_oil")
    cfz = lambda z: E["cf_fixed"] if z[1] == "fixed" else E["cf_float"]
    for z in Z:
        km2_per_twh = 1000 / S["mw_per_km2"] / (8.76 * cfz(z)) * z[4]; mt_per_twh = km2_per_twh * 100 * zec[z[0]]["yield_t_ha"] / 1e6
        d_ = {f"kh_{z[0]}": 1, f"kp_{z[0]}": 1, f"osw_{z[0]}": -mt_per_twh}
        if kelp_force: eq(d_, 0.0)
        else: le(d_, 0.0, f"seaweed_{z[0]}")
    le({"heat_sold": 1, "hubs": -hb["low_twh"]}, 0.0, "heat_hubs"); le({"heat_sold": 1}, food_heat_market_twh(p), "heat_market")
    r_ = {f"c{j}": 1 for j in range(len(p["CARBON"]))}; r_["h_pyro"] = -p["PYRO"]["c_per_h2"]; eq(r_, 0.0)
    # bounds
    bounds = [(0, None)] * nv
    if fixed_hubs is not None: bounds[ix["hubs"]] = (float(fixed_hubs), float(fixed_hubs))
    for j, m in enumerate(p["CARBON"]): bounds[ix[f"c{j}"]] = (0, m[1])
    for j, t in enumerate(tiers): bounds[ix[f"b{j}"]] = (0, t[2])
    for f in EF: bounds[ix[f"eth_{f[0]}"]] = (0, f[3])
    for f in OF: bounds[ix[f"oil_{f[0]}"]] = (0, f[3])
    bounds[ix["bamboo"]] = (0, sum(r[1] for r in p["BAMBOO"]["regions"]) * bam_y); bounds[ix["hemp_mha"]] = (0, HM["max_mha"])
    bounds[ix["onw"]] = (0, E["cap_onw_twh"]); bounds[ix["onw2"]] = (0, E["cap_onw2_twh"]); bounds[ix["pv"]] = (0, E["cap_pv_twh"]); bounds[ix["csp"]] = (0, E["cap_csp_twh"])
    bounds[ix["lwr"]] = (0, E["cap_lwr_twh"]); bounds[ix["export"]] = (0, E["export_cap_twh"]); bounds[ix["liq_import"]] = (0, E["liq_import_cap_twh"])
    vre_ok = E.get("allow_vre", True)
    if not vre_ok:
        for k in ("onw", "onw2", "pv", "csp"): bounds[ix[k]] = (0, 0)
    for z in Z:
        gw2twh = 8.76 * cfz(z); sc = osw_scale.get(z[0], 0.0) if isinstance(osw_scale, dict) else osw_scale
        lo = z[9] * sc * gw2twh; bounds[ix[f"osw_{z[0]}"]] = (lo, max(lo, z[9] * 1.5 * gw2twh)) if vre_ok else (0, 0)
    if not allow_ely: bounds[ix["h_ely"]] = (0, 0)
    if not flex_heat:
        for k in ("t2mid", "t2dry", "m2dry"): bounds[ix[k]] = (0, 0)
    # Steam electrolysis is available in both eras (CN v1.0 fix: the U.S. v8.4 code allowed it only after gas, which
    # excluded a cheaper option from gas-era cases); pyrolysis is removed after gas.
    if post_gas: bounds[ix["h_pyro"]] = (0, 0)
    if (not post_gas and not p.get("htse_gas_era", True)) or not p.get("allow_htse", True): bounds[ix["h_htse"]] = (0, 0)
    if not HT.get("return_unused_steam", False):
        for k in ("m2e", "d2e"): bounds[ix[k]] = (0, 0)
    if not (post_gas and allow_si and HT.get("outlet_c", 750) >= 900): bounds[ix["h_si"]] = (0, 0)
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=bounds, method="highs")
    if res.status != 0: raise RuntimeError(res.message)
    x = {n: float(res.x[i]) for n, i in ix.items()}
    out = post(p, x, float(res.fun), eu, bl, hb, zec, scenario, blend_vol, osw_scale, res, labels)
    out["flex_heat"] = bool(flex_heat); out["post_gas"] = bool(post_gas)
    return out


def post(p, x, lp_cost, eu, bl, hb, zec, scenario, blend_vol, osw_scale, res, labels):
    E = p["ELEC"]; R = p["ROUTES"]; S = p["SEAWEED_PROCESS"]; V = p["VEH"]; HM = p["HEMP"]; Z = p["SEAWEED"]; W = p["WACC"]
    tiers = p["BIOMASS"]["tiers"]; EF = p["ETHANOL_FEEDS"]; OF = p["OIL_FEEDS"]; HT = p["HTGR"]
    out = dict(system=p["system"], reactor_type=p["reactor_type"], scenario=scenario, blend_vol=blend_vol, osw_scale=osw_scale, x=x, hub_spec=hb)
    cfz = lambda z: E["cf_fixed"] if z[1] == "fixed" else E["cf_float"]
    out["osw_gw"] = {z[0]: x[f"osw_{z[0]}"] / (8.76 * cfz(z)) for z in Z}
    out["gw"] = dict(onshore_wind=(x["onw"] + x["onw2"]) / (8.76 * E["cf_onw"]), solar=x["pv"] / (8.76 * E["cf_pv"]), csp=x["csp"] / (8.76 * E["cf_csp"]),
                     lwr=x["lwr"] / (8.76 * 0.92), offshore_wind=sum(out["osw_gw"].values()))
    hub_el = x["hubs"] * hb["el_twh"] + x["hp2e"] * HT["eta_cond"] + x["m2e"] * HT["z_mid"] + x["d2e"] * HT["z_dry"]
    out["el_supply_twh"] = dict(onshore_wind=x["onw"] + x["onw2"], solar=x["pv"], csp=x["csp"], lwr=x["lwr"], offshore_wind=sum(x[f"osw_{z[0]}"] for z in Z), reactor_hubs=hub_el)
    out["el_export_twh"] = x["export"]; out["liq_import_twh"] = x["liq_import"]
    out["hubs"] = x["hubs"]; out["reactors"] = HT["modules"] * x["hubs"]; out["hub_gwt"] = x["hubs"] * hb["mwt"] / 1e3
    sw_h = sum(x[f"kh_{z[0]}"] for z in Z); sw_p = sum(x[f"kp_{z[0]}"] for z in Z); oil_tot = sum(x[f"oil_{f[0]}"] for f in OF)
    out["h2_mt"] = dict(pyrolysis=x["h_pyro"], electrolysis=x["h_ely"], steam_electrolysis=x["h_htse"], sulfur_iodine=x["h_si"],
                        direct_vehicles=eu["h2_mt_direct"], blending=bl["h2_mt"], htl=x["htl"] * R["htl"]["h2_kg_t"] / 1e3,
                        pbtl=x["pbtl"] * R["pbtl"]["h2_kg_t"] / 1e3, hefa=(oil_tot + x["hemp_oil_fuel"]) * R["hefa"]["h2_kg_t"] / 1e3,
                        seaweed=(sw_h * S["htl_h2_kg_t"] + sw_p * S["pbtl_h2_kg_t"]) / 1e3)
    out["gas_for_pyrolysis_bcm"] = x["h_pyro"] * p["PYRO"]["kg_ch4_per_kg_h2"] / 0.72      # 0.72 kg CH4 per m3
    out["blend"] = bl
    carbon = x["h_pyro"] * p["PYRO"]["c_per_h2"]; out["carbon_mt"] = carbon
    out["carbon_alloc"] = [dict(market=m[0], mt=x[f"c{j}"], value_usd_t=m[2], cap_mt=m[1]) for j, m in enumerate(p["CARBON"])]
    out["carbon_revenue_bn"] = sum(a["mt"] * a["value_usd_t"] for a in out["carbon_alloc"]) / 1e3
    out["carbon_value_per_t"] = out["carbon_revenue_bn"] * 1e3 / carbon if carbon else 0.0
    dur = dict(zip([m[0] for m in I.CARBON_MARKETS], I.CARBON_DURABILITY)); out["carbon_by_durability_mt"] = {}
    for a in out["carbon_alloc"]:
        k = dur.get(a["market"], "uncertain"); out["carbon_by_durability_mt"][k] = out["carbon_by_durability_mt"].get(k, 0.0) + a["mt"]
    # feedstocks and liquids by source
    stalk = x["hemp_mha"] * HM["stalk_t_ha"]; bag = {f[0]: x[f"eth_{f[0]}"] * f[5] for f in EF}
    pool = sum(x[f"b{j}"] for j in range(len(tiers))) + x["bamboo"] + stalk + sum(bag.values())
    pool_liq = x["htl"] * R["htl"]["mwh_t"] + x["pbtl"] * R["pbtl"]["mwh_t"] + x["cel"] * R["ethanol"]["cellulosic_gal_per_t"] / 1e3 * 0  # cel counted with ethanol
    share = lambda v: v / pool if pool > 1e-12 else 0.0
    eth_total = sum(x[f"eth_{f[0]}"] for f in EF) + x["cel"] * R["ethanol"]["cellulosic_gal_per_t"] / 1e3
    eth_liq = x["atj"] * R["atj"]["mwh_per_bgal"] + x["etoh_ldv"] * R["ethanol"]["mwh_per_bgal"]
    eth_share = lambda v: v / eth_total if eth_total > 1e-12 else 0.0
    cel_bgal = x["cel"] * R["ethanol"]["cellulosic_gal_per_t"] / 1e3
    pool_twh = lambda mt: pool_liq * share(mt) + eth_liq * eth_share(cel_bgal) * share(mt)
    L = dict(residues=pool_twh(sum(x[f"b{j}"] for j in range(len(tiers)))), bamboo=pool_twh(x["bamboo"]),
             hemp=pool_twh(stalk) + x["hemp_oil_fuel"] * R["hefa"]["mwh_t"], sorghum_bagasse=pool_twh(sum(bag.values())),
             seaweed=sw_h * S["htl_mwh_t"] + sw_p * S["pbtl_mwh_t"], oils_hefa=oil_tot * R["hefa"]["mwh_t"],
             sugar_starch_ethanol=eth_liq * eth_share(sum(x[f"eth_{f[0]}"] for f in EF)), imported=x["liq_import"])
    out["liquids_twh"] = L
    out["routes_mt"] = dict(htl=x["htl"], pbtl=x["pbtl"], cellulosic_ethanol_feed=x["cel"], seaweed_htl=sw_h, seaweed_pbtl=sw_p)
    out["biomass_mt"] = dict(residues=sum(x[f"b{j}"] for j in range(len(tiers))), bamboo=x["bamboo"], hemp_stalk=stalk,
                             hemp_seed=x["hemp_mha"] * HM["seed_t_ha"], sorghum_bagasse=sum(bag.values()), seaweed=sw_h + sw_p, oils=oil_tot,
                             ethanol_bgal=eth_total, atj_ethanol_bgal=x["atj"], cellulosic_ethanol_bgal=cel_bgal)
    out["tiers_mt"] = [dict(name=t[0], region=t[1], cap=t[2], used=x[f"b{j}"], usd_t=t[3]) for j, t in enumerate(tiers)]
    out["ethanol_feeds"] = [dict(key=f[0], name=f[1], region=f[2], cap_bgal=f[3], used_bgal=x[f"eth_{f[0]}"], usd_gal=f[4],
                                 liquid_twh=eth_liq * eth_share(x[f"eth_{f[0]}"]) + (pool_twh(bag[f[0]]) if f[5] > 0 else 0.0)) for f in EF]
    out["oil_feeds"] = [dict(key=f[0], name=f[1], region=f[2], cap_mt=f[3], used_mt=x[f"oil_{f[0]}"], usd_t=f[4],
                             liquid_twh=x[f"oil_{f[0]}"] * R["hefa"]["mwh_t"]) for f in OF]
    bc, by = bamboo_cost_t(p)
    out["bamboo"] = dict(mt=x["bamboo"], mha=x["bamboo"] / by, yield_t_ha=by, cost_t=bc)
    out["hemp"] = dict(mha=x["hemp_mha"], seed_mt=x["hemp_mha"] * HM["seed_t_ha"], oil_mt=x["hemp_mha"] * HM["seed_t_ha"] * HM["oil_frac"],
                       meal_mt=x["hemp_mha"] * HM["seed_t_ha"] * (1 - HM["oil_frac"]), stalk_mt=stalk)
    out["biochar_mt"] = x["htl"] * R["htl"]["char_t_t"]
    sz = []
    for z in Z:
        e = zec[z[0]]; gw = out["osw_gw"][z[0]]; km2 = gw * 1000 / S["mw_per_km2"]; mt = x[f"kh_{z[0]}"] + x[f"kp_{z[0]}"]
        sz.append(dict(zone=z[0], region=z[2], species=z[3], type=z[1], wind_gw=gw, wind_km2=km2, seaweed_km2=km2 * z[4] if mt > 1e-9 else 0.0,
                       yield_t_ha=e["yield_t_ha"], dry_mt=mt, htl_mt=x[f"kh_{z[0]}"], pbtl_mt=x[f"kp_{z[0]}"], wet_mt=mt / z[6], n_kt=mt * z[7] * 1e3,
                       land_n_kt=mt * z[7] * 1e3 * z[8], fuel_twh=x[f"kh_{z[0]}"] * S["htl_mwh_t"] + x[f"kp_{z[0]}"] * S["pbtl_mwh_t"],
                       vessels=mt * 1e6 / e["t_dry_per_vessel_yr"], drones=(km2 * z[4] if mt > 1e-9 else 0) / p["LOGISTICS"]["drone_km2"],
                       harvester_mwh=mt * e["harvester_kwh_t"] * 1e3, vessel_mwh=mt * e["vessel_kwh_t"] * 1e3, port_km=z[10],
                       report_region=z[13], **{f"cost_{k}": v for k, v in e.items() if k.endswith("_t")}, color=z[12], box=z[11]))
    out["seaweed"] = sz
    tot_sw = sum(s["dry_mt"] for s in sz)
    out["grid_harvester"] = fleet_sizing({s["zone"]: s["seaweed_km2"] for s in sz}, tot_sw / 0.12, pacific_passes=3.0, other_passes=2.0) if tot_sw > 0 else {}
    out["fleet"] = dict(vessels=sum(s["vessels"] for s in sz), drones=sum(s["drones"] for s in sz),
                        vessel_energy_gwh=sum(s["vessel_mwh"] for s in sz) / 1e3, harvester_energy_gwh=sum(s["harvester_mwh"] for s in sz) / 1e3)
    # costs
    pl, pg = pyro_cost_per_kg(p); firm = E["vre_firming"]
    gen = (x["onw"] * (E["onshore_wind"] + firm) + x["onw2"] * (E["onshore_wind"] + E["onw2_adder"] + firm) + x["pv"] * (E["solar"] + 1.25 * firm) + x["csp"] * E["csp"] + x["lwr"] * E["lwr"]
           + sum(x[f"osw_{z[0]}"] * ((E["osw_fixed"] if z[1] == "fixed" else E["osw_floating"]) + 0.5 * firm) for z in Z)) / 1e3
    ers = V["ers_km"] * V["ers_capex_m_per_km"] * 1e6 * (crf(W, V["ers_life"]) + V["ers_om"]) / 1e9
    Eu = p["ENDUSE"]
    # CN v1.2: vehicle stocks in VEH are 2050 stocks at the central service growth; they scale only with the departure of
    # service growth from its central value (Monte Carlo), not with growth itself.
    g = Eu["service_growth_2050"] / (p.get("g_ref") or Eu["service_growth_2050"])
    veh = g * (V["ldv_stock_m"] * 1e6 * (Eu["ldv"]["bev"] * V["ldv_bev_net_usd_yr"] + Eu["ldv"]["re"] * V["ldv_re_net_usd_yr"] + Eu["ldv"]["fcev"] * V["ldv_fcev_net_usd_yr"])
               + V["ers_trucks_m"] * 1e6 * V["ers_truck_net_usd_yr"] + V["fcev_trucks_m"] * 1e6 * V["fcev_truck_net_usd_yr"]
               + V["bev_trucks_m"] * 1e6 * V["bev_truck_net_usd_yr"] + V["re_trucks_m"] * 1e6 * V["re_truck_net_usd_yr"]
               + V["tractors_m"] * 1e6 * 0.8 * V["tractor_net_usd_yr"] + V["constr_m"] * 1e6 * 0.85 * V["constr_net_usd_yr"]
               + V["forklifts_m"] * 1e6 * V["forklift_net_usd_yr"]) / 1e9
    el = eu["el"]
    sw_bio = sum(s["dry_mt"] * (s["cost_farm_t"] + s["cost_harvester_t"] + s["cost_vessel_t"] + s["cost_drones_t"]) for s in sz) / 1e3
    sw_ref = sum(s["htl_mt"] * S["htl_cost_t"] + s["pbtl_mt"] * S["pbtl_cost_t"] for s in sz) / 1e3
    costs = dict(
        electricity_generation=gen, transmission_distribution=eu["el_total"] * E["td_adder"] / 1e3,
        charging=(el["ldv"] * E["charge_ldv"] + (el["hdv_bev"] + el["hdv_ers_battery"] + el["hdv_re"] + el["farm"] + el["construction"] + el["industrial"]) * E["charge_hdv"]) / 1e3,
        electric_highways=ers, rail_electrification=V["rail_elec_capex_bn"] * crf(W, V["rail_life"]) * 1.02,
        reactor_hubs=x["hubs"] * hb["cost_bn"], pyrolysis_plants=x["h_pyro"] * pl, natural_gas=x["h_pyro"] * pg,
        electrolysis=x["h_ely"] * p["ELECTROLYSIS"]["capex_cost_kg"] + x["h_htse"] * p["NUCLEAR_H2"]["htse"]["capex_cost_kg"]
                    + x["h_si"] * p["NUCLEAR_H2"]["sulfur_iodine"]["capex_cost_kg"],
        h2_delivery=eu["h2_mt_direct"] * p["H2_DELIVERY"]["vehicle"] + bl["h2_mt"] * p["H2_DELIVERY"]["blend"]
                    + (out["h2_mt"]["htl"] + out["h2_mt"]["pbtl"] + out["h2_mt"]["hefa"] + out["h2_mt"]["seaweed"]) * p["H2_DELIVERY"]["onsite"],
        land_biomass=(sum(x[f"b{j}"] * t[3] for j, t in enumerate(tiers)) + x["bamboo"] * bc) / 1e3,
        hemp_net_of_meal=x["hemp_mha"] * 1e6 * (HM["cost_usd_ha"] - HM["seed_t_ha"] * (1 - HM["oil_frac"]) * HM["meal_value_usd_t"]) / 1e9,
        biorefineries=(x["htl"] * R["htl"]["cost_t"] + x["pbtl"] * R["pbtl"]["cost_t"] + x["cel"] * R["ethanol"]["cellulosic_gal_per_t"] * R["ethanol"]["cellulosic_conv_per_gal"]
                       + x["hemp_oil_fuel"] * R["hefa_conv_only"]) / 1e3,
        seaweed_farms_harvest_haul=sw_bio, seaweed_refining=sw_ref,
        hefa_oils=sum(x[f"oil_{f[0]}"] * (f[4] + R["hefa"]["conv_t"]) for f in OF) / 1e3,
        sugar_starch_ethanol=sum(x[f"eth_{f[0]}"] * f[4] for f in EF) + x["atj"] * R["atj"]["conv_per_bgal"] / 1e9,
        imported_renewable_fuel=x["liq_import"] * E["liq_import_usd_mwh"] / 1e3,
        vehicles_and_machines_net=veh + V["farm_charging_bn_yr"],
        process_heat_equipment=(x["e_heat"] * 2.0 + x["e_dry"] * 8.0 + (x["t2mid"] + x["t2dry"] + x["m2dry"]) * HX_COST) / 1e3,
        residual_pipeline_gas=eu["gas_resid_twh"] / I.BCM_TWH * MMBTU_PER_BCM * (p["GAS"]["price_mmbtu"] + p["GAS"]["delivery_mmbtu"]) / 1e9)
    fd = food(p, out); heat_used = fd["low_grade_twh"] - fd["unused_low_grade_twh"]; out["low_grade_heat_used_twh"] = heat_used
    credits = dict(carbon_products=-out["carbon_revenue_bn"], seaweed_fertiliser=-sum(s["dry_mt"] * s["cost_fert_credit_t"] for s in sz) / 1e3,
                   surplus_electricity_sold=-x["export"] * E["export_value"] / 1e3, low_grade_heat_to_food=-heat_used * 8.0 / 1e3 if p.get("food_credit_in_transport", False) else 0.0)
    out["food_heat_value_outside_boundary_bn"] = heat_used * 8.0 / 1e3   # gross value at USD 8/MWh, before distribution costs
    out["costs_bn"] = costs; out["credits_bn"] = credits; out["total_cost_bn"] = sum(costs.values()) + sum(credits.values())
    sb = bl["h2_mt"] / max(x["h_pyro"] + x["h_ely"] + x["h_htse"] + x["h_si"], 1e-9); out["blend_share_of_h2"] = sb
    hub_blend = sb * (costs["reactor_hubs"] + costs["pyrolysis_plants"] + costs["natural_gas"] + credits["carbon_products"]) + bl["h2_mt"] * p["H2_DELIVERY"]["blend"]
    out["blending_cost_bn"] = hub_blend; out["transport_cost_bn"] = out["total_cost_bn"] - hub_blend
    const = dict(transmission_distribution=costs["transmission_distribution"], charging=costs["charging"], electric_highways=ers,
                 rail_electrification=costs["rail_electrification"], vehicles_and_machines_net=costs["vehicles_and_machines_net"],
                 residual_pipeline_gas=costs["residual_pipeline_gas"],
                 h2_delivery_vehicles_and_blend=eu["h2_mt_direct"] * p["H2_DELIVERY"]["vehicle"] + bl["h2_mt"] * p["H2_DELIVERY"]["blend"])
    heat_adj = credits["low_grade_heat_to_food"] - (-x["heat_sold"] * (8.0 if p.get("food_credit_in_transport", False) else 0.0) / 1e3)
    out["objective_reconciliation"] = dict(lp_objective_bn=lp_cost, fixed_terms_total_bn=sum(const.values()), heat_credit_adjustment_bn=heat_adj,
                                           reported_total_bn=out["total_cost_bn"], residual_bn=out["total_cost_bn"] - (lp_cost + sum(const.values()) + heat_adj))
    marg = res.ineqlin.marginals
    out["shadow_usd"] = {lab: -float(marg[i]) * 1e3 for i, lab in enumerate(labels) if lab in ("electricity", "hydrogen", "liquids", "jet", "top_heat", "mid_heat", "dry_heat")}
    thermal = x["hubs"] * HT["mwt"] * HT["cf"] * 8.76 / 1e3
    out["hub_heat_twh"] = dict(thermal=thermal, top_tier=x["hubs"] * hb["pyro_twh"], to_pyrolysis=x["h_pyro"] * pyro_reactor_heat(p),
                               to_turbine_from_top=x["hp2e"], electricity=hub_el, low_grade_to_food=heat_used,
                               pyrolysis_electric_boost=x["h_pyro"] * (pyro_elec(p) - p["PYRO"]["elec_kwh_kg"]))
    out["enduse"] = eu; out["petroleum"] = petroleum_baseline(p, eu); out["emissions"] = emissions_2050(p, out, eu, bl); out["food"] = fd
    pet = out["petroleum"]["late_2025_bn"]
    out["saving_vs_late_2025_pct"] = 100 * (1 - out["transport_cost_bn"] / pet)
    out["breakeven_multiple"] = out["transport_cost_bn"] / pet
    out["regional_supply"] = regional_supply(p, out)
    return out


def emissions_2050(p, out, eu, bl, elec_ci=None):
    R, S = p["ROUTES"], p["SEAWEED_PROCESS"]; L = out["liquids_twh"]; H = out["h2_mt"]; P = p["PYRO"]
    EM = p.get("EMIS", I.EMIS); elec_ci = EM["elec_ci"] if elec_ci is None else elec_ci
    made = H["pyrolysis"] + H["electrolysis"] + H["steam_electrolysis"] + H["sulfur_iodine"]; water_ci = P["h2_leak"] * P["gwp_h2"]
    h2ci = ((H["pyrolysis"] * h2_ci(p, elec_ci) + H["electrolysis"] * (water_ci + p["ELECTROLYSIS"]["kwh_kg"] * elec_ci)
             + H["steam_electrolysis"] * (water_ci + (p["NUCLEAR_H2"]["htse"]["kwh_e_kg"] + htse_superheat_elec(p, out["hubs"] > 0) + p["NUCLEAR_H2"]["htse"]["kwh_th_kg"] * (out["hubs"] < 1e-9) / 0.98) * elec_ci)
             + H["sulfur_iodine"] * (water_ci + p["NUCLEAR_H2"]["sulfur_iodine"]["kwh_e_kg"] * elec_ci)) / made) if made > 1e-9 else water_ci
    ci = dict(residues=10.0 + EM.get("residue_soc_g_mj", 0.0), bamboo=12.0, hemp=20.0, sorghum_bagasse=12.0, seaweed=12.0, oils_hefa=R["hefa"]["ci_g_mj"],
              sugar_starch_ethanol=R["atj"]["ci_g_mj"], imported=30.0)
    h2_liq = (H["htl"] + H["pbtl"] + H["hefa"] + H["seaweed"]) * h2ci
    mt = dict(electricity_lifecycle=eu["el_total"] * elec_ci, h2_direct=eu["h2_mt_direct"] * h2ci,
              liquid_fuels=sum(L[k] * 3.6 * ci[k] for k in L) / 1e3 + h2_liq, pipeline_gas_residual=eu["gas_resid_twh"] * 3.6 * I.PETRO_CI["ng"] / 1e3,
              hub_construction_fuel_cycle=out["hubs"] * p["HTGR"]["mwt"] * p["HTGR"]["cf"] * 8.76 / 1e3 * EM.get("hub_heat_ci", 0.0))
    base = petroleum_baseline(p, eu); tot = sum(mt.values())
    return dict(by_source_mt=mt, total_mt=tot, baseline_wtw_mt=base["wtw_mt"], baseline_2025_wtw_mt=base["wtw_2025_mt"],
                reduction_pct=100 * (1 - tot / base["wtw_mt"]), avoided_mt=base["wtw_mt"] - tot, h2_ci_kg_per_kg=h2ci,
                biochar_removal_mt=out["biochar_mt"] * 0.6 * 44 / 12, solid_carbon_kept_out_mtco2=out["carbon_mt"] * 44 / 12)


def petroleum_baseline(p, eu):
    """Cost and well-to-wheel emissions of delivering the same 2050 services with petroleum and road gas (2025 fuel mix
    scaled by service growth).  Pre-tax prices."""
    B = p["BASE"]; g = p["ENDUSE"]["service_growth_2050"]; d = eu["demand"]; d0 = eu["base"]
    diesel_mt = B["onroad_diesel_mt"] + B["rail_diesel_mt"] + B["marine_diesel_mt"] + B["farm_diesel_mt"] + B["construction_mining_diesel_mt"] + B["industrial_trucks_mt"]
    gas_bcm = B["road_gas_bcm"]; pipe_bcm = B["pipeline_gas_bcm"]
    res = {}
    for case, pr in I.PRICES_USD_T.items():
        fuel = (B["gasoline_mt"] * pr["gasoline"] + diesel_mt * pr["diesel"] + B["jet_mt"] * pr["jet"] + B["marine_resid_mt"] * pr["resid"]) / 1e3
        road_gas = gas_bcm * MMBTU_PER_BCM * pr["road_gas_mmbtu"] / 1e9
        res[case] = dict(fuel_pretax_bn=fuel * g, road_gas_bn=road_gas * g)
    pipe = pipe_bcm * MMBTU_PER_BCM * (p["GAS"]["price_mmbtu"] + p["GAS"]["delivery_mmbtu"]) / 1e9 * g
    hdv_gas_share = B["road_gas_bcm"] * I.BCM_TWH / max(d0["hdv"], 1e-9)
    def wtw(dd):
        hdv_ci = (1 - hdv_gas_share) * I.PETRO_CI["diesel"] + hdv_gas_share * I.PETRO_CI["ng"]
        mar_resid_share = B["marine_resid_mt"] * I.KWH_PER_KG["resid"] / max(d0["marine"], 1e-9)
        mar_ci = mar_resid_share * I.PETRO_CI["resid"] + (1 - mar_resid_share) * I.PETRO_CI["diesel"]
        return (dd["ldv"] * I.PETRO_CI["gasoline"] + dd["hdv"] * hdv_ci + (dd["rail"] + dd["farm"] + dd["construction"] + dd["industrial"]) * I.PETRO_CI["diesel"]
                + dd["air"] * I.PETRO_CI["jet"] + dd["marine"] * mar_ci + dd["pipeline"] * I.PETRO_CI["ng"]) * 3.6 / 1e3
    out = dict(prices=res, pipeline_gas_bn=pipe, wtw_mt=wtw(d), wtw_2025_mt=wtw(d0), total_twh=sum(d.values()), total_twh_2025=sum(d0.values()),
               total_ej_2025=sum(d0.values()) * 3.6e-3)
    for case in res: out[f"{case}_bn"] = res[case]["fuel_pretax_bn"] + res[case]["road_gas_bn"] + pipe
    return out


# ============================================================================================= regional accounting
def regional_supply(p, out):
    """Feedstock use, liquid fuel output and seaweed by reporting region (autonomous regions, SARs, rest of mainland)."""
    reg = {}
    def add(r, k, v): reg.setdefault(r, {}); reg[r][k] = reg[r].get(k, 0.0) + v
    for t in out["tiers_mt"]: add(t["region"], "residues_mt", t["used"])
    for f in out["ethanol_feeds"]: add(f["region"], "ethanol_bgal", f["used_bgal"]); add(f["region"], "liquid_twh", f["liquid_twh"])
    for f in out["oil_feeds"]:
        if f["key"] == "jatropha":
            add("guangxi", "oil_mt", f["used_mt"] * I.JATROPHA_GUANGXI_SHARE); add("rest", "oil_mt", f["used_mt"] * (1 - I.JATROPHA_GUANGXI_SHARE))
            add("guangxi", "liquid_twh", f["liquid_twh"] * I.JATROPHA_GUANGXI_SHARE); add("rest", "liquid_twh", f["liquid_twh"] * (1 - I.JATROPHA_GUANGXI_SHARE))
        else:
            add(f["region"], "oil_mt", f["used_mt"]); add(f["region"], "liquid_twh", f["liquid_twh"])
    cap = sum(r[1] for r in p["BAMBOO"]["regions"])
    for nm, mha, r in p["BAMBOO"]["regions"]:
        if cap > 0: add(r, "bamboo_mt", out["bamboo"]["mt"] * mha / cap)
    hcap = sum(r[1] for r in p["HEMP"]["regions"])
    for nm, mha, r in p["HEMP"]["regions"]:
        if hcap > 0: add(r, "hemp_mha", out["hemp"]["mha"] * mha / hcap)
    for s in out["seaweed"]: add(s["report_region"], "seaweed_mt", s["dry_mt"]); add(s["report_region"], "offshore_gw", s["wind_gw"])
    # residue-pool liquids allocated in proportion to each region's residue/bamboo/hemp-stalk tonnage
    pool_twh = out["liquids_twh"]["residues"] + out["liquids_twh"]["bamboo"]
    pool_mt = out["biomass_mt"]["residues"] + out["biomass_mt"]["bamboo"]
    for r, v in reg.items():
        mt = v.get("residues_mt", 0.0) + v.get("bamboo_mt", 0.0)
        if pool_mt > 0: v["liquid_twh"] = v.get("liquid_twh", 0.0) + pool_twh * mt / pool_mt
    return reg


# ============================================================================================= food from the cascade
def food_heat_market_twh(p):
    F = p["FOOD"]; asp = asparagopsis(p)
    return (asp["seaweed_mt_dry"] * F["asparagopsis_heat_mwh_t"] + F["greenhouse_market_mt"] * 1e9 / F["greenhouse_yield_kg_m2"] * F["greenhouse_heat_kwh_m2"] / 1e9
            + F["ras_market_mt"] * 1e9 * F["ras_heat_kwh_kg"] / 1e9)


def food(p, out):
    F = p["FOOD"]; hb = out["hub_spec"]; n = out["hubs"]; low = n * hb["low_twh"]
    dry_left = max(n * hb["dry_twh"] - sum(s["pbtl_mt"] for s in out["seaweed"]) * p["SEAWEED_PROCESS"]["pbtl_dry_mwh_t"], 0)
    asp = asparagopsis(p); asp_heat = min(asp["seaweed_mt_dry"] * F["asparagopsis_heat_mwh_t"], low); left = max(low - asp_heat, 0)
    gh_cap = F["greenhouse_market_mt"] * 1e9 / F["greenhouse_yield_kg_m2"] * F["greenhouse_heat_kwh_m2"] / 1e9
    gh_heat = min(left * 0.85, gh_cap); left -= gh_heat
    ras_heat = min(left, F["ras_market_mt"] * 1e9 * F["ras_heat_kwh_kg"] / 1e9); left -= ras_heat
    gh_m2 = gh_heat * 1e9 / F["greenhouse_heat_kwh_m2"]; veg = gh_m2 * F["greenhouse_yield_kg_m2"] / 1e9; fish = ras_heat * 1e9 / F["ras_heat_kwh_kg"] / 1e9
    sw_food_dry = min(F["seaweed_food_dry_mt"], dry_left / F["seaweed_food_dry_mwh_t"]); dry_left2 = dry_left - sw_food_dry * F["seaweed_food_dry_mwh_t"]
    grain = min(max(dry_left2, 0) / F["grain_dry_mwh_t"], F["grain_near_hub_mt"])
    den = F["kcal_per_person_day"] * 365 * 1e6
    edible = (veg * 1e9 * F["kcal_per_kg_veg"] * F["vegetable_edible_fraction"] + fish * 1e9 * F["kcal_per_kg_fish"] * F["fish_shrimp_edible_fraction"]) / den
    return dict(low_grade_twh=low, asparagopsis=asp, asparagopsis_heat_twh=asp_heat, greenhouse_ha=gh_m2 / 1e4, greenhouse_heat_twh=gh_heat,
                vegetables_mt=veg, vegetables_value_bn=veg * F["greenhouse_value_usd_t"] / 1e3, fish_shrimp_mt=fish,
                fish_mt=fish * (1 - F["ras_shrimp_share"]), shrimp_mt=fish * F["ras_shrimp_share"], fish_value_bn=fish * F["ras_value_usd_t"] / 1e3,
                ras_heat_twh=ras_heat, seaweed_food_dried_mt=sw_food_dry, grain_dried_mt=grain, hemp_meal_mt=out["hemp"]["meal_mt"],
                hemp_protein_mt=out["hemp"]["meal_mt"] * p["HEMP"]["protein_frac_meal"], unused_low_grade_twh=left,
                greenhouse_seafood_edible_calorie_equiv_m=edible)


def asparagopsis(p):
    A = p["AG"]; tot_s = tot_c = 0.0; g = {}
    for k, heads in dict(feedlot=A["head_feedlot_m"], dairy=A["head_dairy_m"], grazing=A["head_grazing_m"]).items():
        kg = heads * 1e6 * A["dmi_kg_d"][k] * 365 * A["dose_dm"] * A["adoption"][k]
        cut = A["enteric_mt"] * A["enteric_share"][k] * A["cut"][k] * A["adoption"][k]
        g[k] = dict(seaweed_kt=kg / 1e6, mtco2e_cut=cut); tot_s += kg / 1e9; tot_c += cut
    return dict(groups=g, seaweed_mt_dry=tot_s, mtco2e_cut=tot_c, share_of_enteric=tot_c / A["enteric_mt"] if A["enteric_mt"] else 0,
                tank_ha=tot_s * 1e6 / A["tank_yield_t_ha"], cost_bn=tot_s * 1e6 * A["tank_cost_t"] / 1e9,
                usd_per_tco2e=tot_s * A["tank_cost_t"] / tot_c if tot_c else 0)


# ============================================================================================= after natural gas, fission
def post_gas_params(p):
    p = copy.deepcopy(p); p["ENDUSE"]["pipeline"] = dict(elec=1.0, gas=0.0); p["lightweight"] = False; return p


def vhtr_params(p): return apply_reactor_type(p, "vhtr")


def sustainable_fission_params(p, rtype="tmsr", nuclear_only=False, capex_mult=1.0, fuel_mwhth=None):
    """Theoretical future: closed-cycle breeding hubs (thorium molten salt or sodium fast) with no gas.  VHTR-type heat is
    not assumed: the hub keeps the outlet temperature of its own technology."""
    p = apply_reactor_type(post_gas_params(p), rtype); p["capex_mult"] *= capex_mult
    if fuel_mwhth is not None: p["HTGR"]["fuel_mwhth"] = fuel_mwhth
    p["ELEC"]["cap_lwr_twh"] = 0.0; p["HTGR"]["return_unused_steam"] = True
    if nuclear_only: p["ELEC"]["allow_vre"] = False
    return p


def fuel_supply(r, p):
    """Heavy-metal demand, years of resource and start-up fissile requirement (inventory-level accounting only)."""
    F = I.FUEL; H = p["HTGR"]
    twh_th = r["hubs"] * H["mwt"] * H["cf"] * 8.76 / 1e3 + r["el_supply_twh"]["lwr"] / 0.33
    feed = (0.085 - F["tails"]) / (F["feed_assay"] - F["tails"])          # HTR-PM 8.5% LEU
    once_t = twh_th * 1e6 / 24 / (F["haleu_burnup_gwd_t"] * 1e3) * feed
    closed_t = twh_th * 1e6 / 24 / (F["fission_mwd_per_g"] * 1e6) / (1 - F["closed_cycle_loss"])
    gwe = twh_th / 8.76 / H["cf"] * F["gwe_per_gwt"]
    pu_fast = gwe * F["startup_pu_t_per_gwe"]; msr_fissile = gwe * F["startup_msr_fissile_t_per_gwe"]
    haleu_natu_per_t_fissile = 1 / 0.1975 * (0.1975 - F["tails"]) / (F["feed_assay"] - F["tails"])
    snf_pu_2050 = F["cn_snf_thm_2050"] * F["snf_pu_frac"]
    return dict(thermal_twh=twh_th, fleet_gwe_equivalent=gwe, once_through_natural_u_t_yr=once_t, closed_cycle_heavy_metal_t_yr=closed_t,
                startup_fast_pu_t=pu_fast, startup_msr_fissile_t=msr_fissile,
                startup_msr_natural_u_t=msr_fissile * haleu_natu_per_t_fissile,
                china_snf_pu_2024_t=F["cn_snf_thm_2024"] * F["snf_pu_frac"], china_snf_pu_2050_t=snf_pu_2050,
                china_military_pu_t=F["cn_military_pu_t"],
                fast_startup_share_snf_2050=pu_fast / snf_pu_2050 if snf_pu_2050 else None,
                gwe_startable_by_military_pu=F["cn_military_pu_t"] / F["startup_pu_t_per_gwe"],
                gwe_startable_by_snf_pu_2050=snf_pu_2050 / F["startup_pu_t_per_gwe"],
                years=dict(once_through_china_identified_u=F["cn_uranium_identified_t"] / once_t if once_t else None,
                           once_through_world_identified_u=F["world_identified_u_t"] / once_t if once_t else None,
                           closed_china_thorium_identified=F["cn_thorium_identified_t"] / closed_t if closed_t else None,
                           closed_china_thorium_bayan_obo=F["cn_thorium_bayan_obo_t"] / closed_t if closed_t else None,
                           closed_china_depleted_u=F["cn_depleted_u_t"] / closed_t if closed_t else None,
                           closed_world_thorium=F["world_thorium_t"] / closed_t if closed_t else None))


def solve_learning(p, **kw):
    mult = p.get("capex_mult", 1.0); capex = p["HTGR"]["capex_kwt"] or 1300.0 * mult; r = None
    for _ in range(5):
        r = solve(p, capex_kwt=capex, **kw)
        rc = reactor_cost(p["reactor_case"], max(int(round(r["reactors"])), 1)); new = rc["fleet_avg_kwt_with_idc"] * mult
        if p["HTGR"]["capex_kwt"] or abs(new - capex) < 10: break
        capex = new
    r["reactor_cost"] = reactor_cost(p["reactor_case"], max(int(round(r["reactors"])), 1)); r["capex_kwt_used"] = capex
    return r


MAX_HUBS = 1500
def solve_bounded_learning(p, max_hubs=MAX_HUBS, coarse=1, refine=1, **kw):
    """Fleet cost with module learning is not convex in hub count, so the hub count is chosen by search: every
    `coarse`-th integer from 0 to max_hubs, then every `refine`-th integer within one coarse step of the best.  With
    coarse=1 this is the exhaustive bounded search of the U.S. model v5+."""
    mult = p.get("capex_mult", 1.0); mods = p["HTGR"]["modules"]; seen = {}; landscape = []
    def run(n):
        if n in seen: return seen[n]
        rc = reactor_cost(p["reactor_case"], max(mods * n, 1)); capex = rc["fleet_avg_kwt_with_idc"] * mult
        try: r = solve(p, capex_kwt=capex, fixed_hubs=n, **kw); r["reactor_cost"] = rc; r["capex_kwt_used"] = capex
        except RuntimeError: r = None
        seen[n] = r; return r
    grid = list(range(0, max_hubs + 1, coarse))
    for n in grid:
        r = run(n)
        if r is not None and n % 25 == 0: landscape.append(dict(hubs=n, transport_cost_bn=r["transport_cost_bn"]))
    ok = {n: r for n, r in seen.items() if r is not None}
    nb = min(ok, key=lambda n: ok[n]["total_cost_bn"])
    if coarse > 1:
        for n in range(max(nb - coarse, 0), min(nb + coarse, max_hubs) + 1, refine): run(n)
        ok = {n: r for n, r in seen.items() if r is not None}; nb = min(ok, key=lambda n: ok[n]["total_cost_bn"])
    best = ok[nb]
    best["learning_search"] = dict(method="bounded_integer_hub_search", max_hubs=max_hubs, coarse_step=coarse, refine_step=refine,
                                   solves=len(seen), feasible=len(ok), at_upper_bound=nb >= max_hubs - coarse, samples=landscape)
    return best


def solve_fleet(p, mc=False, **kw):
    """Headline solver.  Fixed hubs (e.g. no-nuclear cases) or fixed capex use the direct LP; otherwise the bounded hub
    search (exhaustive for the published cases, coarse-then-refine for Monte Carlo draws)."""
    if kw.get("fixed_hubs") is not None:
        r = solve(p, capex_kwt=1300.0 * p.get("capex_mult", 1.0), **kw); r["capex_kwt_used"] = None; r["reactor_cost"] = None; return r
    return solve_bounded_learning(p, coarse=25 if mc else 1, refine=1, **kw)


# ============================================================================================= sweeps
def zone_merit(p):
    out = []; S = p["SEAWEED_PROCESS"]
    for z in p["SEAWEED"]:
        e = seaweed_zone_economics(p, z); net_t = e["biomass_cost_t"] - e["fert_credit_t"]
        htl = (net_t + S["htl_cost_t"]) / S["htl_mwh_t"]; pb = (net_t + S["pbtl_cost_t"] + S["pbtl_h2_kg_t"] * 1.8 + S["pbtl_el_mwh_t"] * 55) / S["pbtl_mwh_t"]
        out.append(dict(zone=z[0], region=z[2], species=z[3], yield_t_ha=e["yield_t_ha"], net_biomass_t=net_t, htl_usd_mwh=htl, pbtl_usd_mwh=pb,
                        best_usd_mwh=min(htl, pb), gw=z[9]))
    return sorted(out, key=lambda r: r["best_usd_mwh"])


def sweep_merit(yield_level=1, post_gas=False):
    p0 = default_params(); p0["yield_level"] = yield_level; order = [m["zone"] for m in zone_merit(p0)]; rows = []
    for k in range(len(order) + 1):
        p = default_params(); p["yield_level"] = yield_level
        if post_gas: p = post_gas_params(p)
        sc = {z: (1.0 if z in order[:k] else 0.0) for z in order}
        r = solve_fleet(p, mc=True, scenario="design", osw_scale=sc, post_gas=post_gas)
        rows.append(dict(yield_level=yield_level, post_gas=post_gas, n_zones=k, last_zone=order[k - 1] if k else "", osw_gw=r["gw"]["offshore_wind"],
                         cost_bn=r["transport_cost_bn"], seaweed_mt=r["biomass_mt"]["seaweed"], seaweed_twh=r["liquids_twh"]["seaweed"],
                         export_twh=r["el_export_twh"], land_n_kt=sum(s["land_n_kt"] for s in r["seaweed"]), hubs=r["hubs"]))
    for i in range(1, len(rows)):
        dc = rows[i]["cost_bn"] - rows[i - 1]["cost_bn"]; dt = rows[i]["seaweed_twh"] - rows[i - 1]["seaweed_twh"]
        rows[i]["marginal_usd_per_mwh_seaweed"] = dc * 1e3 / dt if dt > 0 else None
    rows[0]["marginal_usd_per_mwh_seaweed"] = None
    return rows


# ============================================================================================= transition
def logistic(t, mid, w): return 1 / (1 + math.exp(-(t - mid) / w))


def transition(p, design):
    """Year-by-year emissions with logistic adoption by segment; China's NEV share of new cars was ~49% in 2025, so
    light-duty adoption is earlier than in the U.S. model."""
    eu = design["enduse"]; d = eu["base"]; g = p["ENDUSE"]["service_growth_2050"]; tot_2050 = design["emissions"]["total_mt"]
    B = p["BASE"]; hdv_gas = B["road_gas_bcm"] * I.BCM_TWH / max(d["hdv"], 1e-9)
    ci = dict(ldv=I.PETRO_CI["gasoline"], hdv=(1 - hdv_gas) * I.PETRO_CI["diesel"] + hdv_gas * I.PETRO_CI["ng"], rail=I.PETRO_CI["diesel"],
              farm=I.PETRO_CI["diesel"], construction=I.PETRO_CI["diesel"], industrial=I.PETRO_CI["diesel"], air=I.PETRO_CI["jet"],
              marine=I.PETRO_CI["resid"], pipeline=I.PETRO_CI["ng"])
    mids = dict(ldv=(2031, 3.0), hdv=(2034, 3.0), rail=(2036, 3.0), farm=(2039, 3.5), construction=(2036, 3.5), industrial=(2032, 3.0),
                air=(2041, 3.5), marine=(2041, 3.5), pipeline=(2037, 3.0))
    seg = {k: d[k] * ci[k] for k in ci}; segsum = sum(seg.values()); rows = []; cb = cc = 0
    for y in range(2025, 2061):
        gy = 1 + (g - 1) * min(max((y - 2025) / 25, 0), 1)
        a = {k: min(max((logistic(y, m, w) - logistic(2025, m, w)) / (logistic(2050, m, w) - logistic(2025, m, w)), 0), 1) for k, (m, w) in mids.items()}
        base = segsum * 3.6 / 1e3 * gy
        petro = sum(seg[k] * (1 - a[k]) for k in seg) * 3.6 / 1e3 * gy
        new = tot_2050 * sum(seg[k] * a[k] for k in seg) / segsum * gy / g
        rows.append(dict(year=y, baseline_mt=base, case_mt=petro + new, **{f"adopt_{k}": v for k, v in a.items()}))
    s = lambda y0, y1: sum(r["baseline_mt"] - r["case_mt"] for r in rows if y0 <= r["year"] <= y1)
    return dict(rows=rows, cum_avoided_2026_2050=s(2026, 2050), cum_avoided_2026_2060=s(2026, 2060))


# ============================================================================================= Monte Carlo
MC = [(("ELEC", "onshore_wind"), 22, 30, 48), (("ELEC", "solar"), 26, 36, 55), (("ELEC", "osw_fixed"), 48, 60, 95),
      (("ELEC", "osw_floating"), 70, 90, 140), (("ELEC", "lwr"), 50, 65, 100), (("ELEC", "csp"), 70, 95, 140), (("ELEC", "vre_firming"), 10, 20, 40),
      (("ELEC", "td_adder"), 15, 22, 35), (("ELEC", "charge_ldv"), 15, 25, 45), (("ELEC", "export_value"), 15, 30, 45),
      (("PYRO", "capex_kw_h2"), 500, 750, 1600), (("GAS", "price_mmbtu"), 6.0, 8.5, 13.0), (("PYRO", "leak_upstream"), 0.005, 0.015, 0.03),
      (("ROUTES", "htl", "cost_t"), 100, 130, 210), (("ROUTES", "pbtl", "cost_t"), 180, 230, 350),
      (("SEAWEED_PROCESS", "farm_cost_ref_t"), 200, 260, 450), (("VEH", "ldv_bev_net_usd_yr"), round(I.ldv_bev_net("low"), 1), round(I.ldv_bev_net("central"), 1), round(I.ldv_bev_net("high"), 1)),
      (("VEH", "bev_truck_net_usd_yr"), 0, 1200, 3500), (("VEH", "ers_capex_m_per_km"), 1.2, 1.8, 3.5), (("H2_DELIVERY", "vehicle"), 1.2, 2.0, 3.5),
      (("ENDUSE", "service_growth_2050"), 1.00, 1.15, 1.40), (("HEMP", "cost_usd_ha"), 450, 600, 900),
      (("BAMBOO", "establish_usd_ha"), 1200, 2000, 4000), (("WACC",), 0.04, 0.05, 0.08)]


def set_path(p, path, v):
    d = p
    for k in path[:-1]: d = d[k]
    d[path[-1]] = v


def monte_carlo(n=1000, seed=7, scenario="least_cost", osw_scale=None, post_gas=False):
    rng = np.random.default_rng(seed); rows = []
    for i in range(n):
        p = default_params(); dr = {}
        for path, lo, mo, hi in MC:
            v = float(rng.triangular(lo, mo, hi)); set_path(p, path, v); dr["/".join(path)] = v
        bm = float(rng.triangular(0.8, 1.0, 1.4)); p["BIOMASS"]["tiers"] = [(t[0], t[1], t[2], t[3] * bm) for t in p["BIOMASS"]["tiers"]]; dr["biomass_price_scale"] = bm
        em = float(rng.triangular(0.85, 1.0, 1.3)); p["ETHANOL_FEEDS"] = [[f[0], f[1], f[2], f[3], f[4] * em, f[5]] for f in p["ETHANOL_FEEDS"]]; dr["ethanol_cost_scale"] = em
        p["yield_level"] = int(rng.choice([0, 1, 2], p=[0.3, 0.5, 0.2])); dr["yield_level"] = p["yield_level"]
        p["reactor_case"] = str(rng.choice(["low", "central", "high"], p=[0.25, 0.5, 0.25])); dr["reactor_case"] = {"low": 0, "central": 1, "high": 2}[p["reactor_case"]]
        cm, cv = float(rng.triangular(0.5, 1.0, 1.5)), float(rng.triangular(0.5, 1.0, 1.3))
        p["CARBON"] = [[m[0], m[1] * (cm if j < len(p["CARBON"]) - 1 else 1), m[2] * (cv if m[2] > 0 else 1)] for j, m in enumerate(p["CARBON"])]
        dr["carbon_market_scale"] = cm; dr["carbon_value_scale"] = cv
        if post_gas: p = post_gas_params(p)
        if osw_scale is not None: p["osw_scale"] = osw_scale
        try: r = solve_fleet(p, mc=True, scenario=scenario, post_gas=post_gas)
        except RuntimeError: continue
        pet = r["petroleum"]
        rows.append(dict(**dr, transport_cost_bn=r["transport_cost_bn"], hubs=r["hubs"], capex_kwt=r["capex_kwt_used"], h2_pyro_mt=r["h2_mt"]["pyrolysis"],
                         seaweed_mt=r["biomass_mt"]["seaweed"], bamboo_mt=r["biomass_mt"]["bamboo"], hemp_mha=r["hemp"]["mha"],
                         emissions_mt=r["emissions"]["total_mt"], reduction_pct=r["emissions"]["reduction_pct"],
                         petro_2025=pet["late_2025_bn"], petro_2026=pet["nov_2026_bn"], saving_pct=100 * (1 - r["transport_cost_bn"] / pet["late_2025_bn"])))
    return rows


def slim(r):
    keep = {k: v for k, v in r.items() if k not in ("x", "enduse")}
    eu = r["enduse"]; keep["enduse"] = {k: eu[k] for k in ("el", "el_total", "h2_twh", "h2_mt_direct", "liq", "liq_total", "jet", "demand", "base", "gas_resid_twh")}
    return keep


OSW_HALF = 0.5          # half of every zone's large build (~230 GW)
CASES = dict(
    least_cost=dict(scenario="least_cost"),
    least_cost_blend20=dict(scenario="least_cost", blend_vol=0.20),
    least_cost_flex_heat=dict(scenario="least_cost", flex_heat=True),
    design_half_offshore=dict(scenario="design"), design=dict(scenario="design"),
    least_cost_reactor_low=dict(scenario="least_cost"), least_cost_reactor_high=dict(scenario="least_cost"),
    least_cost_no_nuclear=dict(scenario="least_cost", fixed_hubs=0),
    least_cost_no_vehicle_carbon=dict(scenario="least_cost"),
    least_cost_demonstrated_yields=dict(scenario="least_cost"), least_cost_us_truck_ratios=dict(scenario="least_cost"),
    post_gas_least_cost=dict(scenario="least_cost", post_gas=True),
    post_gas_half_offshore=dict(scenario="design", post_gas=True),
    post_gas_reactor_low=dict(scenario="least_cost", post_gas=True), post_gas_reactor_high=dict(scenario="least_cost", post_gas=True),
    post_gas_no_nuclear=dict(scenario="least_cost", post_gas=True, fixed_hubs=0),
    post_gas_htse_48kwh=dict(scenario="least_cost", post_gas=True),
    post_gas_vhtr_si=dict(scenario="least_cost", post_gas=True, allow_si=True))
# CN v1.1 robustness and feasibility cases (referee report): vehicle costs, carbon markets, residues, build limits
ROBUST = dict(
    least_cost_bev_net_zero="BEV net cost 0 USD/yr (no advantage)", least_cost_bev_plus100="BEV net cost +100 USD/yr",
    least_cost_bev_tco_high="BEV net cost, high derivation", least_cost_bev_tco_low="BEV net cost, low derivation",
    least_cost_fleet_350="Car stock 350 million", least_cost_fleet_500="Car stock 500 million",
    least_cost_no_carbon_revenue="No carbon-product revenue", least_cost_carbon_commodity="Commodity carbon markets only",
    least_cost_residues_75="Collectable residues -25%", least_cost_residues_50="Collectable residues -50%",
    least_cost_hub_cap_60="At most 60 hubs (360 modules)", least_cost_hub_cap_30="At most 30 hubs (180 modules)",
    least_cost_grid_tight="Grid and firming costs +60-75%",
    least_cost_bev_plus100_no_carbon="BEV +100 USD/yr and no carbon revenue",
    least_cost_stress_moderate="Combined: no BEV advantage, commodity carbon only, residues -25%, high reactor cost, tight grid",
    post_gas_stress_moderate="Combined (moderate) after gas",
    least_cost_stress_severe="Combined: BEV high derivation, no carbon revenue, residues -25%, high reactor cost, tight grid",
    least_cost_us_v84_htse_rule="Steam electrolysis only after gas (U.S. v8.4 rule)",
    least_cost_no_nuclear_alkaline="No nuclear, alkaline electrolysis only",
    least_cost_food_credit="Food-heat credit inside the transport boundary (v1.1 accounting)",
    least_cost_htse_topping_3="Steam electrolysis: 3 kWh/kg electric topping",
    least_cost_htse_no_lowT_recovery="Steam electrolysis: no low-temperature heat recovery")
for _n in ROBUST:
    CASES[_n] = dict(scenario="least_cost", post_gas=_n.startswith("post_gas"))
CASES["least_cost_no_nuclear_alkaline"]["fixed_hubs"] = 0
CASES["least_cost_hub_cap_60"]["max_hubs"] = 60; CASES["least_cost_hub_cap_30"]["max_hubs"] = 30
for _t in I.REACTOR_TYPES:
    CASES[f"type_{_t}"] = dict(scenario="least_cost"); CASES[f"post_gas_type_{_t}"] = dict(scenario="least_cost", post_gas=True, allow_si=True)
TAIWAN_CASES = dict(tw_least_cost=dict(scenario="least_cost"), tw_no_nuclear=dict(scenario="least_cost", fixed_hubs=0),
                    tw_post_gas=dict(scenario="least_cost", post_gas=True), tw_post_gas_no_nuclear=dict(scenario="least_cost", post_gas=True, fixed_hubs=0),
                    tw_offshore_25gw=dict(scenario="design"))


def case_params(name):
    if name.startswith("tw_"):
        p = default_params("taiwan")
        if name.startswith("tw_post_gas"): p = post_gas_params(p)
        if name.endswith("no_nuclear"):   # no firm nuclear or CSP on the island: battery-firmed wind/solar instead [A]
            p["ELEC"]["cap_lwr_twh"] = 0.0; p["ELEC"]["min_firm_share"] = 0.0; p["ELEC"]["vre_firming"] = 35.0
        if name == "tw_offshore_25gw": p["osw_scale"] = 1.0
        return p
    p = default_params()
    if name.startswith("post_gas"): p = post_gas_params(p)
    if name.endswith("half_offshore"): p["osw_scale"] = OSW_HALF
    if name == "design": p["osw_scale"] = 1.0
    if name.endswith("reactor_low"): p["reactor_case"] = "low"
    if name.endswith("reactor_high"): p["reactor_case"] = "high"
    if name.endswith("no_nuclear"): p["ELEC"]["cap_lwr_twh"] = 0.0
    if name == "least_cost_no_vehicle_carbon": p["lightweight"] = False; p["CARBON"] = p["CARBON"][1:]
    if name == "least_cost_demonstrated_yields": p["yield_level"] = 0
    if name == "least_cost_us_truck_ratios": p["ENDUSE"]["r_hdv_elec"] = 2.40 / 21.1; p["ENDUSE"]["r_hdv_fcev"] = 4.44 / 21.1
    if name == "post_gas_htse_48kwh": p["NUCLEAR_H2"]["htse"]["kwh_e_kg"] = 48.0
    if name == "post_gas_vhtr_si": p = vhtr_params(p)
    if "type_" in name: p = apply_reactor_type(p, name.split("type_")[1])
    stress = "_stress_" in name; severe = name.endswith("stress_severe")
    if name.endswith("us_v84_htse_rule"): p["htse_gas_era"] = False
    if name.endswith("no_nuclear_alkaline"): p["ELEC"]["cap_lwr_twh"] = 0.0; p["allow_htse"] = False
    if name.endswith("food_credit"): p["food_credit_in_transport"] = True
    if name.endswith("htse_topping_3"): p["NUCLEAR_H2"]["htse"]["superheat_kwh_kg"] = 3.0; p["NUCLEAR_H2"]["htse"]["superheat_noreactor_kwh_kg"] = 3.0
    if name.endswith("htse_no_lowT_recovery"): p["NUCLEAR_H2"]["htse"]["kwh_th_kg"] = round(I._HB["no_lowT_recovery_external_heat_kwh_kg"], 3)
    if name.endswith("bev_net_zero"): p["VEH"]["ldv_bev_net_usd_yr"] = 0.0
    if "bev_plus100" in name: p["VEH"]["ldv_bev_net_usd_yr"] = 100.0
    if name.endswith("bev_tco_high") or severe: p["VEH"]["ldv_bev_net_usd_yr"] = I.ldv_bev_net("high")
    if stress and not severe: p["VEH"]["ldv_bev_net_usd_yr"] = 0.0
    if name.endswith("bev_tco_low"): p["VEH"]["ldv_bev_net_usd_yr"] = I.ldv_bev_net("low")
    if name.endswith("fleet_350"): p["VEH"]["ldv_stock_m"] = 350.0
    if name.endswith("fleet_500"): p["VEH"]["ldv_stock_m"] = 500.0
    if "no_carbon" in name or severe:      # carbon must still go somewhere: only paid permanent storage remains
        p["CARBON"] = [[m[0], m[1], min(m[2], 0.0) if j < len(p["CARBON"]) - 1 else m[2]] for j, m in enumerate(p["CARBON"])]
        p["lightweight"] = False
    if name.endswith("carbon_commodity") or (stress and not severe):  # no carbon fibre, anode graphite or specialty carbon
        p["CARBON"] = [m for m in p["CARBON"] if not any(w in m[0] for w in ("Vehicle structures", "anode", "Specialty"))]
        p["lightweight"] = False
    for frac in (75, 50):
        if name.endswith(f"residues_{frac}") or (stress and frac == 75):
            p["BIOMASS"]["tiers"] = [(t[0], t[1], t[2] * frac / 100, t[3]) for t in p["BIOMASS"]["tiers"]]
    if name.endswith("grid_tight") or stress:
        p["ELEC"]["td_adder"] = 35.0; p["ELEC"]["vre_firming"] = 35.0
    if stress: p["reactor_case"] = "high"
    return p


def emissions_boundary(r, p):
    """Well-to-wheel emissions of a solved case under wider life-cycle boundaries (no re-optimisation: these parameters
    do not enter the cost)."""
    out = {}
    variants = dict(central={}, elec_ci_25g=dict(elec_ci=0.025), methane_leak_3pct=dict(leak=0.03),
                    residue_soil_carbon_20g=dict(residue_soc_g_mj=20.0), residue_soil_carbon_40g=dict(residue_soc_g_mj=40.0),
                    hub_construction_fuel_3g=dict(hub_heat_ci=3.0e-3),
                    all_high=dict(elec_ci=0.025, leak=0.03, residue_soc_g_mj=40.0, hub_heat_ci=3.0e-3))
    for k, v in variants.items():
        q = copy.deepcopy(p); q["EMIS"] = {**I.EMIS, **{a: b for a, b in v.items() if a != "leak"}}
        if "leak" in v: q["PYRO"]["leak_upstream"] = v["leak"]
        e = emissions_2050(q, r, r["enduse"], r["blend"])
        out[k] = dict(total_mt=e["total_mt"], reduction_pct=e["reduction_pct"], by_source_mt=e["by_source_mt"])
    return out


def lull_screen(r, p):
    """Stylised wind-lull adequacy screen (CN v1.3): can firm plant plus residual wind and sun carry the inflexible
    transport load through a windless week once all flexible loads stop?  Returns the shortfall, the energy and backup
    capacity needed to cover it and an indicative cost that the annual optimisation does not include."""
    L = I.LULL; g = r["gw"]; eu = r["enduse"]; HT = p["HTGR"]
    inflex = eu["el_total"] / 8.76 * L["load_factor"]                                   # GW
    hub_gw = r["hubs"] * HT["mwt"] * HT.get("eta_cond", 0.40) * L["hub_availability"] / 1e3
    lwr_gw = r["el_supply_twh"]["lwr"] / 8.76 / 0.90 * L["lwr_availability"] if r["el_supply_twh"]["lwr"] > 0 else 0.0
    var = g["onshore_wind"] * L["wind_cf"] + g.get("offshore_wind", 0.0) * L["offshore_cf"] + g["solar"] * L["solar_cf"] + g["csp"] * L["csp_cf"]
    short = max(0.0, inflex - hub_gw - lwr_gw - var); e_twh = short * 24 * L["days"] / 1e3
    crf = 0.05 / (1 - 1.05 ** -L["backup_life_yr"])
    cap_bn = short * L["backup_capex_usd_kw"] * crf / 1e3
    h2_mt = e_twh * L["events_per_yr"] / L["h2_to_power_eff"] / 33.3                   # Mt H2 per year burned for backup
    fuel_bn = h2_mt * L["h2_value_usd_kg"]
    h2_lost = (r["h2_mt"]["steam_electrolysis"] + r["h2_mt"]["electrolysis"]) * L["days"] / 365.0
    return dict(inflexible_gw=inflex, hub_firm_gw=hub_gw, lwr_gw=lwr_gw, variable_in_lull_gw=var, shortfall_gw=short,
                shortfall_twh=e_twh, backup_capacity_bn=cap_bn, backup_h2_mt=h2_mt, backup_fuel_bn=fuel_bn,
                indicative_cost_bn=cap_bn + fuel_bn, indicative_cost_pct=100 * (cap_bn + fuel_bn) / r["transport_cost_bn"],
                h2_production_lost_mt=h2_lost)


def feasibility(r, p, build_start=2032, end=2050, wind_start=2026):
    """Build-rate and system-structure screen for a solved case (not an hourly dispatch model)."""
    yrs = end - build_start + 1; modules = r["hubs"] * p["HTGR"]["modules"] if "modules" in p["HTGR"] else r["hubs"] * 6
    el = r["el_supply_twh"]; tot = sum(el.values())
    firm = el["reactor_hubs"] + el["lwr"] + el["csp"]; vre = el["onshore_wind"] + el["solar"] + el["offshore_wind"]
    return dict(modules=modules, modules_per_yr=modules / yrs, gwt_per_yr=r["hubs"] * p["HTGR"]["mwt"] / 1e3 / yrs,
                hub_gwt=r["hubs"] * p["HTGR"]["mwt"] / 1e3, build_years=yrs,
                wind_gw=r["gw"]["onshore_wind"] + r["gw"].get("offshore_wind", 0.0), wind_gw_per_yr=(r["gw"]["onshore_wind"] + r["gw"].get("offshore_wind", 0.0)) / (end - wind_start + 1),
                solar_gw=r["gw"]["solar"], firm_share=firm / tot, vre_share=vre / tot, electricity_twh=tot,
                ers_km_per_yr=p["VEH"]["ers_km"] / (end - wind_start + 1))


def main(n_mc=1000):
    res = {}
    for name, kw in list(CASES.items()) + list(TAIWAN_CASES.items()):
        p = case_params(name); res[name] = solve_fleet(p, **kw); res[name]["fuel_supply"] = fuel_supply(res[name], p)
    # theoretical closed-cycle fleets (bounded exhaustive search over hub counts)
    for name, rtype, kwx in (("sustainable_fission_tmsr", "tmsr", {}), ("sustainable_fission_cfr", "cfr", {}),
                             ("sustainable_fission_tmsr_nuclear_only", "tmsr", dict(nuclear_only=True)),
                             ("sustainable_fission_tmsr_premium", "tmsr", dict(capex_mult=1.25, fuel_mwhth=9.0))):
        p = sustainable_fission_params(default_params(), rtype, **kwx)
        res[name] = solve_bounded_learning(p, scenario="least_cost", post_gas=True)
        res[name]["fuel_supply"] = fuel_supply(res[name], p)
    json.dump({k: slim(v) for k, v in res.items()}, open(OUT / "cn_scenarios.json", "w"), indent=1, default=float)
    lc_p = case_params("least_cost")
    rob = dict(ldv_tco={c: dict(net_usd_yr=I.ldv_bev_net(c), parts=I.ldv_bev_net(c, parts=True), inputs=I.LDV_TCO[c]) for c in ("low", "central", "high")},
               cases={n: dict(label=lab, transport_cost_bn=res[n]["transport_cost_bn"], saving_pct=res[n]["saving_vs_late_2025_pct"],
                              breakeven=res[n]["breakeven_multiple"], hubs=res[n]["hubs"], emissions_mt=res[n]["emissions"]["total_mt"],
                              petroleum_2025_bn=res[n]["petroleum"]["late_2025_bn"], petroleum_2026_bn=res[n]["petroleum"]["nov_2026_bn"],
                              h2_pyro_mt=res[n]["h2_mt"]["pyrolysis"], solar_gw=res[n]["gw"]["solar"], wind_gw=res[n]["gw"]["onshore_wind"])
                      for n, lab in ROBUST.items()},
               emissions_boundary=emissions_boundary(res["least_cost"], lc_p),
               lull_screen={n: lull_screen(res[n], case_params(n)) for n in ("least_cost", "post_gas_least_cost", "least_cost_no_nuclear",
                                                                            "least_cost_hub_cap_30", "least_cost_reactor_high")},
               feasibility={n: feasibility(res[n], case_params(n)) for n in ("least_cost", "post_gas_least_cost", "least_cost_hub_cap_60", "least_cost_stress_moderate")},
               carbon_by_durability_mt=res["least_cost"]["carbon_by_durability_mt"])
    json.dump(rob, open(OUT / "cn_robustness.json", "w"), indent=1, default=float)
    d = res["least_cost"]; p = default_params()
    json.dump({c: reactor_cost(c, max(int(round(d["reactors"])), 1)) for c in ("low", "central", "high")} | {"anchors": I.REACTOR_ANCHORS,
              "types": I.REACTOR_TYPES}, open(OUT / "cn_reactor_costs.json", "w"), indent=1, default=str)
    json.dump(dict(design=zone_merit(p), learning=zone_merit({**p, "yield_level": 2})), open(OUT / "cn_seaweed_merit.json", "w"), indent=1)
    sm = sweep_merit(1) + sweep_merit(2) + sweep_merit(1, post_gas=True)
    with open(OUT / "cn_sweep_merit.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sm[0].keys())); w.writeheader(); w.writerows(sm)
    json.dump(transition(p, d), open(OUT / "cn_transition.json", "w"))
    json.dump(dict(turning=gh_turning(), energy=gh_energy(), fleet_half_offshore=res["design_half_offshore"]["grid_harvester"],
                   fleet=res["design_half_offshore"]["fleet"]), open(OUT / "cn_grid_harvester.json", "w"), indent=1)
    mcl = monte_carlo(n_mc, seed=11, scenario="least_cost"); mch = monte_carlo(n_mc, seed=13, scenario="design", osw_scale=OSW_HALF)
    mcp = monte_carlo(n_mc, seed=17, scenario="least_cost", post_gas=True)
    for nm, rows in (("cn_monte_carlo_least_cost.csv", mcl), ("cn_monte_carlo_half_offshore.csv", mch), ("cn_monte_carlo_post_gas.csv", mcp)):
        with open(OUT / nm, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    q = lambda rows, k: {f"p{pp}": float(np.percentile([r[k] for r in rows], pp)) for pp in (5, 50, 95)}
    summ = {}
    for nm, rows in (("least_cost", mcl), ("half_offshore", mch), ("post_gas", mcp)):
        summ[nm] = {k: q(rows, k) for k in ("transport_cost_bn", "hubs", "capex_kwt", "h2_pyro_mt", "seaweed_mt", "emissions_mt", "reduction_pct", "saving_pct")}
        summ[nm]["p_cheaper_2025"] = float(np.mean([r["transport_cost_bn"] < r["petro_2025"] for r in rows]))
        summ[nm]["p_cheaper_2026"] = float(np.mean([r["transport_cost_bn"] < r["petro_2026"] for r in rows]))
        summ[nm]["p_saving_ge_23pct"] = float(np.mean([r["saving_pct"] >= 23.0 for r in rows])); summ[nm]["n"] = len(rows)
    from scipy.stats import spearmanr
    keys = [k for k in mcl[0] if "/" in k or k in ("WACC", "yield_level", "reactor_case", "carbon_market_scale", "carbon_value_scale", "biomass_price_scale", "ethanol_cost_scale")]
    y = [r["transport_cost_bn"] for r in mcl]
    summ["sensitivity_least_cost"] = {k: float(spearmanr([r[k] for r in mcl], y)[0]) for k in keys}
    json.dump(summ, open(OUT / "cn_monte_carlo_summary.json", "w"), indent=1)
    print(json.dumps({k: dict(cost=round(v["transport_cost_bn"], 1), petro=round(v["petroleum"]["late_2025_bn"], 1), save=round(v["saving_vs_late_2025_pct"], 1),
                              hubs=round(v["hubs"], 1), h2pyro=round(v["h2_mt"]["pyrolysis"], 1), osw=round(v["gw"]["offshore_wind"]),
                              red=round(v["emissions"]["reduction_pct"], 1)) for k, v in res.items()}, indent=0))
    return res


if __name__ == "__main__":
    import sys
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1000)
