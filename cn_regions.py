"""Regional screen: the five autonomous regions, Hong Kong, Macau, the rest of the mainland and Taiwan.

The mainland LP is national (one annual balance, like the U.S. model).  This script splits its 2050 demand, baseline
emissions and petroleum comparator by region with fixed shares (cn_inputs.REGIONS, from GDP, sown area, mining and
airport shares), reports the feedstocks each region supplies in the least-cost solution, and compares each region's
2050 transport demand with its renewable technical potential.  Taiwan comes from its own island LP.  Shares are
reporting assumptions, not a regional optimisation; inter-regional transmission and fuel trade are implied, not costed
separately.

Writes cn_regional_screen.json and cn_regional_screen.csv.  Run after cn_model.py.
"""
import csv, json
from pathlib import Path
import cn_inputs as I

HERE = Path(__file__).resolve().parent
MARINE_SHARE = dict(hong_kong=4.8 / 39.8, guangxi=0.03, macau=0.0)        # HK bunkers + harbour craft, share of marine fuel mass [A]
SEG_KEY = dict(ldv="road", hdv="road", rail="road", air="air", marine=None, pipeline="road", farm="farm", construction="mine", industrial="road")


def shares(rk):
    R = I.REGIONS[rk]; s = {}
    for seg, key in SEG_KEY.items():
        s[seg] = MARINE_SHARE.get(rk, 0.0) if key is None else R[key]
    return s


def split(case, rk):
    eu = case["enduse"]; sh = shares(rk)
    dem2050 = sum(eu["demand"][k] * sh[k] for k in sh)
    el = sum(v * sh["hdv" if k.startswith("hdv") else k] for k, v in eu["el"].items())
    h2 = sum(v * sh[k] for k, v in eu["h2_twh"].items())
    liq = sum(v * sh[k] for k, v in eu["liq"].items())
    tot_d = sum(eu["demand"].values())
    w = dem2050 / tot_d if tot_d else 0
    return dict(demand_2050_twh=dem2050, electricity_twh=el, hydrogen_twh=h2, liquids_twh=liq, share_of_mainland_demand=w,
                baseline_wtw_mt=case["emissions"]["baseline_wtw_mt"] * w, system_emissions_mt=case["emissions"]["total_mt"] * w,
                petroleum_late_2025_bn=case["petroleum"]["late_2025_bn"] * w, system_cost_bn=case["transport_cost_bn"] * w,
                energy_system_cost_bn=case["energy_system_cost_bn"] * w)


def main():
    S = json.load(open(HERE / "cn_scenarios.json")); lc = S["least_cost"]; reg_supply = lc["regional_supply"]
    rows = []
    for rk, R in I.REGIONS.items():
        r = dict(region=rk, name=R["name"], capital=R["capital"], population_m=R["pop_m"], **split(lc, rk))
        sup = reg_supply.get(rk, {})
        r.update({f"supply_{k}": v for k, v in sup.items()})
        res = I.REGION_RESOURCE_TWH[rk]; r["renewable_potential_twh"] = sum(res.values())
        r["potential_over_electricity_demand"] = r["renewable_potential_twh"] / r["electricity_twh"] if r["electricity_twh"] else None
        r["local_liquids_over_liquid_demand"] = sup.get("liquid_twh", 0.0) / r["liquids_twh"] if r["liquids_twh"] else None
        rows.append(r)
    # rest of mainland = national minus listed regions
    tot = split(lc, "guangxi")  # template keys
    rest = {k: 0.0 for k in tot}
    eu = lc["enduse"]
    for k in rest:
        rest[k] = {"demand_2050_twh": sum(eu["demand"].values()), "electricity_twh": eu["el_total"], "hydrogen_twh": sum(eu["h2_twh"].values()),
                   "liquids_twh": eu["liq_total"], "share_of_mainland_demand": 1.0, "baseline_wtw_mt": lc["emissions"]["baseline_wtw_mt"],
                   "system_emissions_mt": lc["emissions"]["total_mt"], "petroleum_late_2025_bn": lc["petroleum"]["late_2025_bn"],
                   "system_cost_bn": lc["transport_cost_bn"], "energy_system_cost_bn": lc["energy_system_cost_bn"]}[k] - sum(r[k] for r in rows)
    sup = reg_supply.get("rest", {})
    rows.append(dict(region="rest_of_mainland", name="Rest of mainland (27 provinces and municipalities)", capital="", population_m=1408.3 - sum(R["pop_m"] for k, R in I.REGIONS.items() if k not in ("hong_kong", "macau")),
                     **rest, **{f"supply_{k}": v for k, v in sup.items()},
                     local_liquids_over_liquid_demand=sup.get("liquid_twh", 0.0) / rest["liquids_twh"] if rest["liquids_twh"] else None))
    for tw_key, label in (("tw_least_cost", "Taiwan (island system, nuclear hubs allowed)"), ("tw_no_nuclear", "Taiwan (island system, no nuclear)")):
        t = S[tw_key]; eu = t["enduse"]
        rows.append(dict(region=tw_key, name=label, capital="Taipei", population_m=23.4, demand_2050_twh=sum(eu["demand"].values()),
                         electricity_twh=eu["el_total"], hydrogen_twh=sum(eu["h2_twh"].values()), liquids_twh=eu["liq_total"],
                         baseline_wtw_mt=t["emissions"]["baseline_wtw_mt"], system_emissions_mt=t["emissions"]["total_mt"],
                         petroleum_late_2025_bn=t["petroleum"]["late_2025_bn"], system_cost_bn=t["transport_cost_bn"],
                         energy_system_cost_bn=t["energy_system_cost_bn"], saving_energy_system_pct=t["saving_energy_system_pct"],
                         saving_vs_late_2025_pct=t["saving_vs_late_2025_pct"], imported_liquids_twh=t["liq_import_twh"],
                         local_liquids_over_liquid_demand=1 - t["liq_import_twh"] / eu["liq_total"]))
    json.dump(dict(case="least_cost", rows=rows, note="reporting split of a national LP; Taiwan from its own LP"), open(HERE / "cn_regional_screen.json", "w"), indent=1)
    keys = sorted({k for r in rows for k in r})
    with open(HERE / "cn_regional_screen.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
    for r in rows:
        print(f"{r['name'][:44]:44s} demand {r['demand_2050_twh']:7.0f} TWh  el {r['electricity_twh']:6.0f}  liq {r['liquids_twh']:6.0f}  "
              f"local liquids {100*(r.get('local_liquids_over_liquid_demand') or 0):5.0f}%  WTW base {r['baseline_wtw_mt']:6.0f} Mt")


if __name__ == "__main__":
    main()
