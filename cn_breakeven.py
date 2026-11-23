"""Petroleum-price break-even analysis.

For a system cost C and the petroleum comparator P (late-2025 pre-tax fuel, road gas and pipeline gas for the same 2050
services), the break-even multiple is m* = C / P: petroleum is cheaper only if its prices fall below m* times their
late-2025 level.  The saving against late-2025 prices is 1 - m*.  CN v1.6.3: computed for the energy-system (project) cost,
which excludes the net cost of owning electric vehicles and machines (paid by their owners), and for the cost including it.
Reads stored outputs only.  Writes cn_breakeven.json and cn_breakeven.csv.
"""
import csv, json
from pathlib import Path
import cn_inputs as I

ROOT = Path(__file__).resolve().parent
MC_FILES = {"least_cost": "cn_monte_carlo_least_cost.csv", "half_offshore_230gw": "cn_monte_carlo_half_offshore.csv",
            "post_gas": "cn_monte_carlo_post_gas.csv"}
DET = ["least_cost", "design_half_offshore", "design", "least_cost_no_nuclear", "least_cost_reactor_high", "post_gas_least_cost",
       "post_gas_half_offshore", "post_gas_no_nuclear", "post_gas_reactor_high", "type_tmsr", "type_vhtr", "type_cfr", "type_acp100",
       "sustainable_fission_tmsr", "sustainable_fission_tmsr_nuclear_only", "sustainable_fission_tmsr_premium", "sustainable_fission_cfr",
       "tw_least_cost", "tw_no_nuclear", "tw_post_gas"]
GRID = [round(0.50 + 0.05 * i, 2) for i in range(31)]


def pct(xs, q):
    s = sorted(xs); k = (len(s) - 1) * q; f = int(k); c = min(f + 1, len(s) - 1); return s[f] + (s[c] - s[f]) * (k - f)


def main():
    sc = json.loads((ROOT / "cn_scenarios.json").read_text())
    pet = sc["least_cost"]["petroleum"]; P = pet["late_2025_bn"]; nov = pet["nov_2026_bn"] / P
    pre = I.PRICES_USD_T["late_2025"]
    out = dict(basis=dict(petroleum_late_2025_bn=P, petroleum_nov_2026_bn=pet["nov_2026_bn"], nov_2026_multiple=nov,
                          late_2025_pretax_usd_t={k: v for k, v in pre.items()}), deterministic={}, monte_carlo={}, monte_carlo_energy_system={})
    for k in DET:
        c = sc[k]["transport_cost_bn"]; Pk = sc[k]["petroleum"]["late_2025_bn"]; m = c / Pk
        ce = sc[k]["energy_system_cost_bn"]; me = ce / Pk
        out["deterministic"][k] = dict(cost_bn=c, petroleum_bn=Pk, breakeven_multiple=m, saving_pct=100 * (1 - m),
                                       energy_system_cost_bn=ce, breakeven_energy_system=me, saving_energy_system_pct=100 * (1 - me),
                                       consumer_vehicle_cost_bn=c - ce,
                                       breakeven_gasoline_pretax_usd_t=me * pre["gasoline"], breakeven_diesel_pretax_usd_t=me * pre["diesel"],
                                       breakeven_jet_pretax_usd_t=me * pre["jet"])
    rows = []
    for name, fn in MC_FILES.items():
        draws = list(csv.DictReader(open(ROOT / fn)))
        for basis, col, key in (("with_vehicles", "transport_cost_bn", "monte_carlo"), ("energy_system", "energy_system_cost_bn", "monte_carlo_energy_system")):
            ms = [float(d[col]) / float(d["petro_2025"]) for d in draws]; n = len(ms)
            out[key][name] = dict(n=n, breakeven_p5=pct(ms, 0.05), breakeven_p50=pct(ms, 0.5), breakeven_p95=pct(ms, 0.95),
                                  share_cheaper={"0.7x": sum(x < 0.7 for x in ms) / n, "1.0x": sum(x < 1.0 for x in ms) / n, "1.5x": sum(x < 1.5 for x in ms) / n},
                                  share_cheaper_nov_2026=sum(x < nov for x in ms) / n)
            for m in GRID: rows.append(dict(case=name, basis=basis, petroleum_price_multiple=m, share_cheaper=round(sum(x < m for x in ms) / n, 4)))
    (ROOT / "cn_breakeven.json").write_text(json.dumps(out, indent=1))
    with open(ROOT / "cn_breakeven.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    mcs = json.loads((ROOT / "cn_monte_carlo_summary.json").read_text())
    for name, key in (("least_cost", "least_cost"), ("half_offshore_230gw", "half_offshore"), ("post_gas", "post_gas")):
        assert abs(out["monte_carlo"][name]["share_cheaper"]["1.0x"] - mcs[key]["p_cheaper_2025"]) < 1e-9, name
        assert abs(out["monte_carlo_energy_system"][name]["share_cheaper"]["1.0x"] - mcs[key]["p_energy_system_cheaper_2025"]) < 1e-9, name
    d = out["deterministic"]["least_cost"]
    print(f"PASS: break-even; least cost energy system {d['energy_system_cost_bn']:.1f} vs {d['petroleum_bn']:.1f} bn -> "
          f"{d['saving_energy_system_pct']:.1f}% saving, break-even {d['breakeven_energy_system']:.2f}x; with consumer vehicle costs "
          f"{d['cost_bn']:.1f} bn -> {d['saving_pct']:.1f}%")


if __name__ == "__main__":
    main()
