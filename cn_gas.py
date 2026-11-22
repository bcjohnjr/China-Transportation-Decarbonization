"""How long can natural gas supply methane pyrolysis in China, and what changes the date?

Year-by-year balance of China's gas demand against domestic production, pipeline imports and LNG imports:
  * domestic: remaining technically recoverable conventional+tight, shale and coalbed-methane resources (national
    assessments) times a recovery haircut; production capacity grows ~3%/yr from 261.9 bcm (2025) to a plateau, then a
    15-year reserves-to-production floor;
  * pipelines: Power of Siberia, Central Asia and Myanmar capacity rising from 81 bcm (2025) to the 15th Five-Year Plan
    land-import target (114 bcm, 2030) and ~150 bcm with Power of Siberia 2; drawn from a pool of exporter gas dedicated to
    China, with the same R/P floor;
  * LNG: up to an import ceiling (infrastructure and policy), default 140 bcm/yr (~100 Mt).
The pyrolysis programme ramps 2030-2050 to the gas use of the gas-era least-cost case; road gas (LNG trucks) and gas for
pipeline compressors phase down with electrification.  Biogas and building heat pumps are tested as extensions.
"First shortfall" = first year demand exceeds domestic + pipeline + LNG-ceiling supply.

Flat layout: reads cn_scenarios.json, writes cn_gas_depletion.json.  Run after cn_model.py.
"""
import json, math
from pathlib import Path
import cn_inputs as I

HERE = Path(__file__).resolve().parent
TCM_BCM = 1000.0
BIOGAS_BCM_2045 = dict(low=10.0, central=30.0, high=80.0)     # biomethane potential reached by 2045 [A: China livestock, straw, waste]
HP = dict(space_water_share=0.70, adoption_2050=0.90, cop=3.0, eff_gas=0.85)   # building gas to heat pumps [A]


def ramp(y, a, b): return min(max((y - a) / (b - a), 0.0), 1.0)
def logistic(t, mid, w): return 1 / (1 + math.exp(-(t - mid) / w))


def depletion(program_bcm=0.0, rec_frac=0.6, lng_cap=None, pipe_pool_tcm=None, biogas_bcm=0.0, heat_pumps=False,
              road_gas_phaseout=True, start=2026, end=2250):
    N = I.NG; lng_cap = N["lng_cap_bcm"] if lng_cap is None else lng_cap
    pipe_pool = (N["pipeline_pool_tcm"] if pipe_pool_tcm is None else pipe_pool_tcm) * TCM_BCM
    R_dom = (N["trr_conventional_tight_tcm"] + N["trr_shale_tcm"] + N["trr_cbm_tcm"] - N["cumulative_produced_tcm"]) * TCM_BCM * rec_frac
    B = I.BASE_MAINLAND; road0 = B["road_gas_bcm"]; pipe0 = B["pipeline_gas_bcm"]
    non_t0 = N["consumption_bcm_2025"] - road0 - pipe0
    hp_save = I.NG["res_com_bcm"] * HP["space_water_share"] * HP["adoption_2050"] if heat_pumps else 0.0
    hp_el_twh = hp_save * I.BCM_TWH * HP["eff_gas"] / HP["cop"]
    rows = []; short = None; lng_needed = None; dom_cap = N["prod_bcm_2025"]
    for y in range(start, end + 1):
        non_t = non_t0 * (1 + N["non_transport_growth"]) ** (min(y, N["non_transport_growth_until"]) - 2025)
        a_hdv = (logistic(y, 2034, 3.0) - logistic(2025, 2034, 3.0)) / (logistic(2050, 2034, 3.0) - logistic(2025, 2034, 3.0))
        road = road0 * (1 - min(max(a_hdv, 0), 1)) if road_gas_phaseout else road0
        pipe_fuel = pipe0 * (1 - 0.6 * ramp(y, 2030, 2050)) if road_gas_phaseout else pipe0
        prog = program_bcm * ramp(y, 2030, 2050)
        demand = non_t + road + pipe_fuel + prog - hp_save * ramp(y, 2028, 2050) - biogas_bcm * ramp(y, 2028, 2045)
        demand = max(demand, 0.0)
        dom_cap = min(N["prod_bcm_2025"] * (1 + N["domestic_cap_growth"]) ** (y - 2025), N["domestic_plateau_bcm"])
        if R_dom / max(dom_cap, 1e-9) < N["rp_floor_years"]: dom_cap = R_dom / N["rp_floor_years"]
        dom = min(demand, dom_cap)
        pcap = N["pipeline_import_bcm_2025"] + (N["pipeline_cap_bcm_2030"] - N["pipeline_import_bcm_2025"]) * ramp(y, 2025, 2030) \
            + (N["pipeline_cap_bcm_2035"] - N["pipeline_cap_bcm_2030"]) * ramp(y, 2030, 2035)
        if pipe_pool / max(pcap, 1e-9) < N["rp_floor_years"]: pcap = pipe_pool / N["rp_floor_years"]
        pipe = min(max(demand - dom, 0.0), pcap)
        lng = min(max(demand - dom - pipe, 0.0), lng_cap)
        gap = demand - dom - pipe - lng
        if gap > 1e-6 and short is None: short = y
        R_dom = max(R_dom - dom, 0.0); pipe_pool = max(pipe_pool - pipe, 0.0)
        rows.append(dict(year=y, demand_bcm=demand, domestic_bcm=dom, pipeline_bcm=pipe, lng_bcm=lng, shortfall_bcm=max(gap, 0.0),
                         import_share=(pipe + lng) / demand if demand else 0.0, domestic_remaining_tcm=R_dom / TCM_BCM,
                         pipeline_pool_remaining_tcm=pipe_pool / TCM_BCM, program_bcm=prog))
        if y > 2120 and R_dom < 1 and pipe_pool < 1: break
    peak_import = max(r["import_share"] for r in rows if r["year"] <= 2100)
    return dict(first_shortfall_year=short, peak_import_share_to_2100=peak_import, heat_pump_electricity_twh=hp_el_twh, rows=rows)


def main():
    S = json.load(open(HERE / "cn_scenarios.json"))
    prog = S["least_cost"]["gas_for_pyrolysis_bcm"]
    cases = dict(
        no_programme=depletion(0.0), programme=depletion(prog),
        programme_heat_pumps=depletion(prog, heat_pumps=True),
        programme_biogas=depletion(prog, biogas_bcm=BIOGAS_BCM_2045["central"]),
        programme_heat_pumps_biogas_high=depletion(prog, heat_pumps=True, biogas_bcm=BIOGAS_BCM_2045["high"]),
        programme_no_lng_growth=depletion(prog, lng_cap=I.NG["lng_import_mt_2025"] * 1.36),
        programme_lng_200=depletion(prog, lng_cap=200.0),
        programme_rec40=depletion(prog, rec_frac=0.4), programme_rec80=depletion(prog, rec_frac=0.8),
        programme_pipe_pool10=depletion(prog, pipe_pool_tcm=10.0), programme_pipe_pool40=depletion(prog, pipe_pool_tcm=40.0))
    grid = {}
    for rf in (0.4, 0.6, 0.8):
        for lc in (100.0, 140.0, 200.0):
            for pool in (10.0, 20.0, 40.0):
                for nm, pr in (("none", 0.0), ("programme", prog)):
                    grid[f"rec{rf}|lng{int(lc)}|pool{int(pool)}|{nm}"] = depletion(pr, rec_frac=rf, lng_cap=lc, pipe_pool_tcm=pool)["first_shortfall_year"]
    out = dict(programme_gas_bcm_2050=prog, programme_share_of_2025_consumption=prog / I.NG["consumption_bcm_2025"],
               summary={k: dict(first_shortfall_year=v["first_shortfall_year"], peak_import_share_to_2100=v["peak_import_share_to_2100"])
                        for k, v in cases.items()}, grid=grid,
               rows={k: v["rows"] for k, v in cases.items() if k in ("no_programme", "programme", "programme_heat_pumps")},
               heat_pump_electricity_twh=cases["programme_heat_pumps"]["heat_pump_electricity_twh"])
    json.dump(out, open(HERE / "cn_gas_depletion.json", "w"), indent=1)
    print(json.dumps(out["summary"], indent=0))


if __name__ == "__main__":
    main()
