"""Regression and consistency tests for CN v1.6.4.  Run after cn_model.py, cn_gas.py, cn_regions.py, cn_crossfeed.py and
cn_breakeven.py.  Exits non-zero on failure."""
import csv, json, math
from pathlib import Path
import cn_inputs as I
import cn_model as M

H = Path(__file__).resolve().parent
S = json.load(open(H / "cn_scenarios.json")); ok = []


def check(name, cond):
    ok.append((name, bool(cond)))
    if not cond: print("FAIL:", name)


for k, r in S.items():
    eu = r["enduse"]
    # CN v1.6.3: project (energy-system) cost + consumer vehicle cost = cost including vehicles
    check(f"{k}: energy-system + consumer vehicle cost = total", abs(r["energy_system_cost_bn"] + r["consumer_vehicle_cost_bn"] - r["transport_cost_bn"]) < 1e-9)
    check(f"{k}: consumer vehicle cost is the vehicles-and-machines line", abs(r["consumer_vehicle_cost_bn"] - r["costs_bn"]["vehicles_and_machines_net"]) < 1e-12)
    check(f"{k}: energy-system saving consistent", abs(r["saving_energy_system_pct"] - 100 * (1 - r["energy_system_cost_bn"] / r["petroleum"]["late_2025_bn"])) < 1e-9)
    check(f"{k}: objective reconciliation residual < 1e-6 bn", abs(r["objective_reconciliation"]["residual_bn"]) < 1e-6)
    liq = sum(r["liquids_twh"].values())
    check(f"{k}: liquids supplied >= demand", liq >= eu["liq_total"] - 1e-3)
    el = sum(r["el_supply_twh"].values())
    check(f"{k}: electricity supplied >= transport demand", el >= eu["el_total"] - 1e-3)
    check(f"{k}: emissions fall", 0 < r["emissions"]["total_mt"] < r["emissions"]["baseline_wtw_mt"])
    if r["post_gas"]: check(f"{k}: no fossil gas to pyrolysis after gas", r["gas_for_pyrolysis_bcm"] < 1e-6)
    if r["post_gas"] and r["h2_mt"]["pyrolysis"] > 1e-6: check(f"{k}: post-gas pyrolysis is fully biogenic", r["pyrolysis_biogenic_share"] > 1 - 1e-6)
    nu = r.get("nutrients")
    if nu:   # nutrient and soil-carbon balance (CN v1.5)
        P_ = M.case_params(k) if k in M.CASES or k in M.TAIWAN_CASES or k in M.ROBUST else None
        bal_on = P_["nutrient_balance"] if P_ else True; soc_on = P_["soc_balance"] if P_ else True
        for el in "npk":
            e = nu[el]; tot = sum(e["returned_mt"].values()) - e["sold_mt"] - e["removed_mt"]
            check(f"{k}: {el.upper()} balance reported consistently", abs(tot - e["balance_mt"]) < 1e-9)
            if bal_on: check(f"{k}: {el.upper()} returned >= removed", e["balance_mt"] >= -1e-6)
            check(f"{k}: {el.upper()} returns non-negative", all(v >= -1e-9 for v in e["returned_mt"].values()))
        sc = nu["soil_carbon"]; sup = sum(sc["stable_soc_supplied_mt"].values())
        if soc_on and (P_ is None or P_.get("pyro_carbon_in_soc", True)):
            check(f"{k}: stable SOC supplied + priced deficit >= required", sup + sc["deficit_mt"] >= sc["stable_soc_required_mt"] - 1e-6)
            bio = sup - sc["stable_soc_supplied_mt"]["pyrolysis_carbon"]
            check(f"{k}: biogenic SOC share >= minimum", bio >= I.NUTRIENTS["biogenic_min_share"] * (sc["stable_soc_required_mt"] - sc["deficit_mt"]) - 1e-6)
        bm = nu["biomethane_twh"]
        check(f"{k}: biomethane used <= made", bm["to_pyrolysis"] + bm["sold"] <= bm["made"] + 1e-6)
        rt = nu["returns_mt_feed"]
        check(f"{k}: digested and returned HTL streams <= HTL feed", rt["digested"] <= r["routes_mt"]["htl"] + 1e-6 and rt["hydrochar"] <= r["routes_mt"]["htl"] + 1e-6)
        for b in r.get("bioextraction", []):
            check(f"{k}: {b['zone']} farm area within screened cap", b["km2"] <= b["cap_km2"] * (1 + 1e-6))
    check(f"{k}: carbon allocated = carbon made", abs(sum(a["mt"] for a in r["carbon_alloc"]) - r["carbon_mt"]) < 1e-6)
# corrected heavy-truck ratios
p = M.default_params()
check("heavy-truck electric ratio is kWh/kWh on the LHV basis (0.44)", abs(p["ENDUSE"]["r_hdv_elec"] - 2.40 * 3.6 / (21.1 * 128450 / 137381)) < 1e-12)
check("heavy-truck fuel-cell ratio on the LHV basis (0.81)", abs(p["ENDUSE"]["r_hdv_fcev"] - 4.44 * 3.6 / (21.1 * 128450 / 137381)) < 1e-12)
# demand baseline reproduces the 2025 inputs
d = M.enduse_2050(p)["base"]
check("2025 gasoline energy = 155.72 Mt x 12.06 kWh/kg", abs(d["ldv"] - 155.72 * 12.06) < 1e-6)
check("2025 jet energy = 45.96 Mt x 12.0", abs(d["air"] - 45.96 * 12.0) < 1e-6)
# prices
pre = I.PRICES_USD_T["late_2025"]
check("late-2025 pre-tax gasoline 800-950 USD/t", 800 < pre["gasoline"] < 950)
check("Nov-2026 / late-2025 petroleum multiple 1.2-1.6", 1.2 < S["least_cost"]["petroleum"]["nov_2026_bn"] / S["least_cost"]["petroleum"]["late_2025_bn"] < 1.6)
# hub search
check("least-cost hub search not at upper bound", not S["least_cost"]["learning_search"]["at_upper_bound"])
check("sustainable fission nuclear-only uses no wind/solar", S["sustainable_fission_tmsr_nuclear_only"]["el_supply_twh"]["onshore_wind"] < 1e-6)
# gas module
g = json.load(open(H / "cn_gas_depletion.json"))
check("programme brings shortfall earlier or equal", g["summary"]["programme"]["first_shortfall_year"] <= g["summary"]["no_programme"]["first_shortfall_year"])
check("lower recovery brings shortfall earlier", g["summary"]["programme_rec40"]["first_shortfall_year"] < g["summary"]["programme"]["first_shortfall_year"])
# regions
R = json.load(open(H / "cn_regional_screen.json"))["rows"]
mainland = [r for r in R if not r["region"].startswith("tw_")]
check("regional demand sums to national", abs(sum(r["demand_2050_twh"] for r in mainland) - sum(S["least_cost"]["enduse"]["demand"].values())) < 1e-6)
check("all five autonomous regions reported", {"guangxi", "inner_mongolia", "ningxia", "xizang", "xinjiang"} <= {r["region"] for r in R})
# cross-feed
cf = json.load(open(H / "cn_crossfeed.json"))["least_cost"]
check("cross-feed shares within [0,1]", 0 <= cf["marine_protein_need_met_internally"] <= 1 and 0 <= cf["feed_protein_met_internally"] <= 1)
# break-even
be = json.load(open(H / "cn_breakeven.json"))
check("break-even saving consistent", abs(be["deterministic"]["least_cost"]["saving_pct"] - S["least_cost"]["saving_vs_late_2025_pct"]) < 1e-9)
check("break-even energy-system saving consistent", abs(be["deterministic"]["least_cost"]["saving_energy_system_pct"] - S["least_cost"]["saving_energy_system_pct"]) < 1e-9)
check("vehicle-cost cases change only the consumer cost, not the energy system",
      all(abs(S[n]["energy_system_cost_bn"] - S["least_cost"]["energy_system_cost_bn"]) < 1e-6 for n in
          ("least_cost_bev_net_zero", "least_cost_bev_plus100", "least_cost_bev_tco_high", "least_cost_bev_tco_low", "least_cost_fleet_350", "least_cost_fleet_500")))
# CN v1.1 robustness file
RB = json.load(open(H / "cn_robustness.json")); C = RB["cases"]; lc = S["least_cost"]["transport_cost_bn"]
check("BEV derivation: central value used in the model", abs(I.VEH["ldv_bev_net_usd_yr"] - round(RB["ldv_tco"]["central"]["net_usd_yr"], 1)) < 1e-9)
check("BEV derivation ordered low < central < high", RB["ldv_tco"]["low"]["net_usd_yr"] < RB["ldv_tco"]["central"]["net_usd_yr"] < RB["ldv_tco"]["high"]["net_usd_yr"])
for n in ("least_cost_bev_net_zero", "least_cost_bev_plus100", "least_cost_bev_tco_high", "least_cost_no_carbon_revenue",
          "least_cost_carbon_commodity", "least_cost_residues_75", "least_cost_residues_50", "least_cost_hub_cap_60",
          "least_cost_hub_cap_30", "least_cost_grid_tight", "least_cost_stress_moderate", "least_cost_stress_severe"):
    check(f"robustness: {n} costs at least the central case", C[n]["transport_cost_bn"] >= lc - 1e-6)
check("robustness: BEV cost monotone (0 < +100 < high derivation)", C["least_cost_bev_net_zero"]["transport_cost_bn"] < C["least_cost_bev_plus100"]["transport_cost_bn"] < C["least_cost_bev_tco_high"]["transport_cost_bn"])
check("robustness: residues monotone", C["least_cost_residues_75"]["transport_cost_bn"] <= C["least_cost_residues_50"]["transport_cost_bn"])
check("robustness: hub caps respected", C["least_cost_hub_cap_60"]["hubs"] <= 60 and C["least_cost_hub_cap_30"]["hubs"] <= 30)
check("robustness: no-carbon-revenue case has no carbon sales revenue", S["least_cost_no_carbon_revenue"]["carbon_revenue_bn"] <= 1e-9)
EB = RB["emissions_boundary"]
check("emissions boundary: central matches headline", abs(EB["central"]["total_mt"] - S["least_cost"]["emissions"]["total_mt"]) < 1e-9)
check("emissions boundary: every wider boundary raises emissions", all(v["total_mt"] >= EB["central"]["total_mt"] - 1e-9 for v in EB.values()))
check("carbon durability sums to carbon made", abs(sum(RB["carbon_by_durability_mt"].values()) - S["least_cost"]["carbon_mt"]) < 1e-6)
check("feasibility: modules = 6 x hubs", abs(RB["feasibility"]["least_cost"]["modules"] - 6 * S["least_cost"]["hubs"]) < 1e-9)
# CN v1.2 accounting corrections
for k, r in S.items():
    check(f"{k}: food-heat credit outside the transport boundary", abs(r["credits_bn"]["low_grade_heat_to_food"]) < 1e-12 or k == "least_cost_food_credit")
check("food-credit case only differs by the credit", S["least_cost_food_credit"]["transport_cost_bn"] <= S["least_cost"]["transport_cost_bn"] + 1e-6)
pc = M.default_params(); V = pc["VEH"]; E_ = pc["ENDUSE"]
veh_expected = (V["ldv_stock_m"] * 1e6 * (E_["ldv"]["bev"] * V["ldv_bev_net_usd_yr"] + E_["ldv"]["re"] * V["ldv_re_net_usd_yr"] + E_["ldv"]["fcev"] * V["ldv_fcev_net_usd_yr"])
                + V["ers_trucks_m"] * 1e6 * V["ers_truck_net_usd_yr"] + V["fcev_trucks_m"] * 1e6 * V["fcev_truck_net_usd_yr"] + V["bev_trucks_m"] * 1e6 * V["bev_truck_net_usd_yr"]
                + V["re_trucks_m"] * 1e6 * V["re_truck_net_usd_yr"] + V["tractors_m"] * 1e6 * 0.8 * V["tractor_net_usd_yr"] + V["constr_m"] * 1e6 * 0.85 * V["constr_net_usd_yr"]
                + V["forklifts_m"] * 1e6 * V["forklift_net_usd_yr"]) / 1e9
check("farm charging is a project (infrastructure) cost line", abs(S["least_cost"]["costs_bn"]["farm_charging"] - V["farm_charging_bn_yr"]) < 1e-12)
check("2050 vehicle stocks are not multiplied by service growth (central case)", abs(S["least_cost"]["costs_bn"]["vehicles_and_machines_net"] - veh_expected) < 1e-6)
import inspect
src = inspect.getsource(M.solve)
check("solve(): h_htse appears in mid_heat row and not in dry_heat row", '"h_htse": NH["htse"]["kwh_th_kg"]}' in src and '"h_htse": NH["htse"]["kwh_th_kg"], "d2e"' not in src)
check("superheat electricity charged below 850 C outlet", M.htse_superheat_elec(pc) > 0 and M.htse_superheat_elec(M.apply_reactor_type(pc, "vhtr")) == 0.0)
check("steam electrolysis restricted to after gas costs at least the central case", S["least_cost_htse_after_gas_only"]["transport_cost_bn"] >= S["least_cost"]["transport_cost_bn"] - 1e-6)
check("alkaline-only no-nuclear case costs at least the no-nuclear case", S["least_cost_no_nuclear_alkaline"]["transport_cost_bn"] >= S["least_cost_no_nuclear"]["transport_cost_bn"] - 1e-6)
check("after gas: no fossil gas for pyrolysis or pipeline compression", all(S[k]["costs_bn"]["residual_pipeline_gas"] == 0 and abs(S[k]["costs_bn"]["natural_gas"]) < 1e-9 for k in S if k.startswith("post_gas")))
# CN v1.3 steam-electrolysis heat balance and lull screen
import cn_htse_heat as HB
hb = HB.balance(); d = hb["duties_kwh_kg"]
cold = d["feed_water_preheat"] + d["evaporation"] + d["superheat_total"]
supplied = hb["external_heat_kwh_kg"] + d["preheat_recovered_sensible"] + d["preheat_recovered_condensing"] + d["superheat_by_recuperator"] + d["electric_trim"]
check("HTSE heat balance closes (cold-side duty = external + recovered + recuperator + trim)", abs(cold - supplied) < 1e-9)
check("HTSE recuperator respects the minimum approach temperature", hb["recuperator_min_approach_c"] >= HB.P["dT_min"] - 0.5)
check("HTSE external heat is needed only up to the saturation temperature", hb["external_heat_max_temp_c"] < 200)
check("model uses the derived HTSE heat inputs", abs(I.NUCLEAR_H2["htse"]["kwh_th_kg"] - round(hb["external_heat_kwh_kg"], 3)) < 1e-9 and abs(I.NUCLEAR_H2["htse"]["superheat_kwh_kg"] - round(hb["topping_kwh_kg"], 3)) < 1e-9)
check("feed steam = water split / utilisation", abs(hb["feed_steam_kg"] - hb["water_split_kg"] / HB.P["steam_utilisation"]) < 1e-9)
LS = RB["lull_screen"]
check("lull screen: shortfalls are non-negative", all(v["shortfall_gw"] >= 0 for v in LS.values()))
check("lull screen: no-nuclear shortfall exceeds central", LS["least_cost_no_nuclear"]["shortfall_gw"] >= LS["least_cost"]["shortfall_gw"])
check("HTSE topping 3 kWh/kg costs at least the central case", S["least_cost_htse_topping_3"]["transport_cost_bn"] >= S["least_cost"]["transport_cost_bn"] - 1e-6)
check("HTSE without low-temperature recovery costs at least the central case", S["least_cost_htse_no_lowT_recovery"]["transport_cost_bn"] >= S["least_cost"]["transport_cost_bn"] - 1e-6)
# CN v1.4 lull sensitivities
LV = RB["lull_sensitivity"]["least_cost"]
check("lull: zero wind raises the shortfall", LV["zero_wind"]["shortfall_gw"] >= LV["submitted"]["shortfall_gw"])
check("lull: lower availability raises it further", LV["zero_wind_availability_80"]["shortfall_gw"] >= LV["zero_wind"]["shortfall_gw"])
check("lull: smaller turbines raise it further", LV["zero_wind_turbines_60pct"]["shortfall_gw"] >= LV["zero_wind"]["shortfall_gw"])
check("lull: longer lull needs more energy", LV["zero_wind_14_days"]["shortfall_twh"] >= LV["zero_wind"]["shortfall_twh"])
check("lull: submitted variant equals the headline screen", abs(LV["submitted"]["shortfall_gw"] - RB["lull_screen"]["least_cost"]["shortfall_gw"]) < 1e-9)
# CN v1.5 nutrient cases
NB = RB["nutrients"]
check("without nutrient/SOC constraints the pre-nutrient central cost is reproduced (309.0 in v1.6.2: 303.4 before the elemental fertiliser, gas-HHV and LHV truck-ratio corrections)", abs(S["least_cost_no_nutrient_balance"]["transport_cost_bn"] - 309.0) < 0.2)
check("nutrient balance alone costs more than none", S["least_cost_no_soc_balance"]["transport_cost_bn"] >= S["least_cost_no_nutrient_balance"]["transport_cost_bn"] - 1e-6)
check("adding the SOC balance costs more again", lc >= S["least_cost_no_soc_balance"]["transport_cost_bn"] - 1e-6)
check("design forces every eutrophic zone to its screened area", all(abs(b["km2"] - b["cap_km2"]) < 1e-3 for b in S["design_half_offshore"]["bioextraction"]))
check("N payment lowers the cost of full bioextraction", S["least_cost_bioextraction_n_credit_30"]["transport_cost_bn"] < S["least_cost_bioextraction_full"]["transport_cost_bn"])
check("full bioextraction costs at least the least-cost case", S["least_cost_bioextraction_full"]["transport_cost_bn"] >= lc - 1e-6)
check("central case replaces all removed soil carbon", S["least_cost"]["nutrients"]["soil_carbon"]["deficit_mt"] < 1e-6 and S["post_gas_least_cost"]["nutrients"]["soil_carbon"]["deficit_mt"] < 1e-6)
_bo = S["least_cost_soc_no_pyro_carbon"]["nutrients"]["biological_options"]
check("without pyrolysis carbon counted, green manure or compost close the balance", (_bo["green_manure_mha"] + _bo["compost_mt"]) > 1e-3
      and S["least_cost_soc_no_pyro_carbon"]["nutrients"]["soil_carbon"]["deficit_mt"] < 1e-9)
check("unreplaced soil carbon counted as emissions", all(abs(r["emissions"]["by_source_mt"].get("soil_carbon_not_replaced", 0.0) - r["nutrients"]["soil_carbon"]["deficit_mt"] * 44 / 12) < 1e-9 for r in S.values() if r.get("nutrients")))
check("a higher deficit price does not lower cost", S["least_cost_soc_deficit_price_1000"]["transport_cost_bn"] >= lc - 1e-6)
check("after gas, forbidding biomethane pyrolysis costs at least as much", S["post_gas_no_biomethane_pyrolysis"]["transport_cost_bn"] >= S["post_gas_least_cost"]["transport_cost_bn"] - 1e-6)
check("mineral fertiliser emissions counted", S["least_cost"]["emissions"]["by_source_mt"]["mineral_fertiliser"] >= 0)
check("pyrolysis CI falls with biogenic share", M.h2_ci(p, 0.0, 1.0) < M.h2_ci(p, 0.0, 0.0))
check("biomethane valued on the same basis as pyrolysis gas", abs(p["PYRO"]["kg_ch4_per_kg_h2"] * M.GPK * M.gas_usd_mwh(p) / 1e3 - M.pyro_cost_per_kg(p)[1]) < 1e-9)
# CN v1.6: biological soil carbon, Grid Harvester nearshore logistics, backup bracket, thorium consistency
for k in ("least_cost_biological_soc", "post_gas_biological_soc", "least_cost_biological_soc_compost_cost_high"):
    sc = S[k]["nutrients"]["soil_carbon"]
    check(f"{k}: no pyrolysis carbon counted", sc["stable_soc_supplied_mt"]["pyrolysis_carbon"] == 0.0)
    check(f"{k}: no priced gap", sc["deficit_mt"] < 1e-9 and not S[k]["soc_fallback"])
    check(f"{k}: biological sources meet the full requirement", sum(sc["stable_soc_supplied_mt"].values()) >= sc["stable_soc_required_mt"] - 1e-6)
check("biological soil carbon costs at least the least-cost case", S["least_cost_biological_soc"]["transport_cost_bn"] >= lc - 1e-6)
nc = S["least_cost_biological_soc_no_compost"]
check("without compost the strict balance needs a priced liquid shortfall", nc["liq_import_twh"] > 1.0)
for k, r in S.items():
    nu = r.get("nutrients")
    if not nu: continue
    bo = nu["biological_options"]
    check(f"{k}: green manure within its area cap", bo["green_manure_mha"] <= I.NUTRIENTS["green_manure"]["max_mha"] + 1e-6)
    check(f"{k}: compost within its cap", bo["compost_mt"] <= I.NUTRIENTS["compost"]["max_mt"] + 1e-6)
    for b in r.get("bioextraction", []):
        check(f"{k}: {b['zone']} cost = farm + Grid Harvester + vessel + drones",
              abs(b["cost_t"] - (b["farm_t"] + b["harvester_t"] + b["vessel_t"] + b["drones_t"])) < 1e-9)
bxd = S["design_half_offshore"]
check("Grid Harvester fleet includes nearshore farms in the design", bxd["grid_harvester"].get("nearshore_units", 0) > 0)
check("thorium: nuclear-only costs at least the unrestricted fleet",
      S["sustainable_fission_tmsr_nuclear_only"]["transport_cost_bn"] >= S["sustainable_fission_tmsr"]["transport_cost_bn"] - 1e-6)
check("no headline case relies on the priced soil-carbon gap", not any(S[k]["soc_fallback"] for k in ("least_cost", "post_gas_least_cost", "design_half_offshore",
      "least_cost_no_nuclear", "sustainable_fission_tmsr", "sustainable_fission_tmsr_nuclear_only")))
BR = RB["lull_bracket"]
for k, v in BR.items():
    check(f"{k}: backup bracket ordered lower <= plausible <= high", v["lower_bound"]["cost_bn"] <= v["plausible"]["cost_bn"] + 1e-9 <= v["high"]["cost_bn"] + 2e-9)
    check(f"{k}: lower bound equals the lull screen", abs(v["lower_bound"]["cost_bn"] - RB["lull_screen"][k]["indicative_cost_bn"]) < 1e-9 if k in RB["lull_screen"] else True)
# Monte Carlo files
for fn in ("cn_monte_carlo_least_cost.csv", "cn_monte_carlo_half_offshore.csv", "cn_monte_carlo_post_gas.csv"):
    rows = list(csv.DictReader(open(H / fn))); check(f"{fn} has draws", len(rows) > 0)
n_fail = sum(1 for _, c in ok if not c)
print(f"cn_test: {len(ok) - n_fail}/{len(ok)} checks passed")
raise SystemExit(1 if n_fail else 0)
