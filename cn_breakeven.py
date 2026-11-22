"""Petroleum-price break-even analysis (same method as us8_petroleum_breakeven.py in the U.S. model v8.4).

For a system cost C and the petroleum comparator P (late-2025 pre-tax fuel, road gas and pipeline gas for the same 2050
services), the break-even multiple is m* = C / P: petroleum is cheaper only if its prices fall below m* times their
late-2025 level.  The saving against late-2025 prices is 1 - m*; the U.S. v8.4 headline was 23.2% (m* = 0.77).
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
US_V84_SAVING = 23.2


def pct(xs, q):
    s = sorted(xs); k = (len(s) - 1) * q; f = int(k); c = min(f + 1, len(s) - 1); return s[f] + (s[c] - s[f]) * (k - f)


def main():
    sc = json.loads((ROOT / "cn_scenarios.json").read_text())
    pet = sc["least_cost"]["petroleum"]; P = pet["late_2025_bn"]; nov = pet["nov_2026_bn"] / P
    pre = I.PRICES_USD_T["late_2025"]
    out = dict(basis=dict(petroleum_late_2025_bn=P, petroleum_nov_2026_bn=pet["nov_2026_bn"], nov_2026_multiple=nov,
                          late_2025_pretax_usd_t={k: v for k, v in pre.items()}, us_v84_saving_pct=US_V84_SAVING), deterministic={}, monte_carlo={})
    for k in DET:
        c = sc[k]["transport_cost_bn"]; Pk = sc[k]["petroleum"]["late_2025_bn"]; m = c / Pk
        out["deterministic"][k] = dict(cost_bn=c, petroleum_bn=Pk, breakeven_multiple=m, saving_pct=100 * (1 - m),
                                       matches_us_23pct=(100 * (1 - m)) >= US_V84_SAVING,
                                       breakeven_gasoline_pretax_usd_t=m * pre["gasoline"], breakeven_diesel_pretax_usd_t=m * pre["diesel"],
                                       breakeven_jet_pretax_usd_t=m * pre["jet"])
    rows = []
    for name, fn in MC_FILES.items():
        draws = list(csv.DictReader(open(ROOT / fn))); ms = [float(d["transport_cost_bn"]) / float(d["petro_2025"]) for d in draws]; n = len(ms)
        out["monte_carlo"][name] = dict(n=n, breakeven_p5=pct(ms, 0.05), breakeven_p50=pct(ms, 0.5), breakeven_p95=pct(ms, 0.95),
                                        share_cheaper={"0.7x": sum(x < 0.7 for x in ms) / n, "1.0x": sum(x < 1.0 for x in ms) / n, "1.5x": sum(x < 1.5 for x in ms) / n},
                                        share_cheaper_nov_2026=sum(x < nov for x in ms) / n,
                                        share_saving_ge_us_23pct=sum((1 - x) * 100 >= US_V84_SAVING for x in ms) / n)
        for m in GRID: rows.append(dict(case=name, petroleum_price_multiple=m, share_cheaper=round(sum(x < m for x in ms) / n, 4)))
    (ROOT / "cn_breakeven.json").write_text(json.dumps(out, indent=1))
    with open(ROOT / "cn_breakeven.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    mcs = json.loads((ROOT / "cn_monte_carlo_summary.json").read_text())
    for name, key in (("least_cost", "least_cost"), ("half_offshore_230gw", "half_offshore"), ("post_gas", "post_gas")):
        assert abs(out["monte_carlo"][name]["share_cheaper"]["1.0x"] - mcs[key]["p_cheaper_2025"]) < 1e-9, name
    d = out["deterministic"]["least_cost"]
    print(f"PASS: break-even; least cost {d['cost_bn']:.1f} vs {d['petroleum_bn']:.1f} bn -> {d['saving_pct']:.1f}% saving "
          f"(U.S. v8.4: {US_V84_SAVING}%), break-even {d['breakeven_multiple']:.2f}x")


if __name__ == "__main__":
    main()
