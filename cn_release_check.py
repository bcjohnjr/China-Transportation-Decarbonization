"""Release check for CN v1.6.2: does this copy of the code reproduce the submitted numbers?

    python3 cn_release_check.py            # check (run after run_all.sh, or alone for the code-hash and re-solve checks)
    python3 cn_release_check.py --write    # write cn_release_manifest.json (done once, by the authors, at release)

The manifest holds the SHA-256 of every code and input file, and the headline numbers of the submitted release.  The
check (1) compares the file hashes, (2) re-solves the central, after-gas, 230 GW offshore and biological soil-carbon cases
from the code (not from saved outputs) and (3) compares cn_scenarios.json, cn_monte_carlo_summary.json and
cn_robustness.json, if present, with the manifest.  Flat layout: run in the folder that holds the files.
"""
import hashlib, json, sys
from pathlib import Path

H = Path(__file__).resolve().parent
MAN = H / "cn_release_manifest.json"
CODE = sorted([p.name for p in H.glob("*.py")] + ["run_all.sh", "requirements.txt"])
KEY_CASES = ("least_cost", "post_gas_least_cost", "design_half_offshore", "least_cost_biological_soc")
TOL_BN = 0.05; TOL_PCT = 0.05


def sha(name):
    return hashlib.sha256((H / name).read_bytes()).hexdigest()


def headline(r):
    return dict(transport_cost_bn=r["transport_cost_bn"], saving_pct=r["saving_vs_late_2025_pct"], hubs=r["hubs"],
                h2_pyrolysis_mt=r["h2_mt"]["pyrolysis"], gas_for_pyrolysis_bcm=r["gas_for_pyrolysis_bcm"], emissions_mt=r["emissions"]["total_mt"])


def saved_numbers():
    out = {}
    S = json.load(open(H / "cn_scenarios.json"))
    out["scenarios"] = {k: headline(S[k]) for k in KEY_CASES + ("least_cost_no_nutrient_balance", "least_cost_no_nuclear", "tw_least_cost")}
    if (H / "cn_monte_carlo_summary.json").exists():
        M = json.load(open(H / "cn_monte_carlo_summary.json"))
        out["monte_carlo_median_saving_pct"] = {k: M[k]["saving_pct"]["p50"] for k in ("least_cost", "half_offshore", "post_gas") if k in M}
    if (H / "cn_robustness.json").exists():
        RB = json.load(open(H / "cn_robustness.json"))
        if "lull_bracket" in RB:
            out["backup_saving_pct"] = {k: RB["lull_bracket"]["least_cost"][k]["saving_pct"] for k in ("lower_bound", "plausible", "high")}
    return out


def write():
    man = dict(release="CN v1.6.2", files={n: sha(n) for n in CODE if (H / n).exists()}, numbers=saved_numbers())
    json.dump(man, open(MAN, "w"), indent=1); print(f"wrote {MAN.name}: {len(man['files'])} files")


def check():
    if not MAN.exists():
        print("cn_release_check: no manifest (cn_release_manifest.json) - nothing to compare"); return 0
    man = json.load(open(MAN)); fails = []
    for n, h in man["files"].items():
        if n == Path(__file__).name: continue
        if not (H / n).exists(): fails.append(f"missing file {n}")
        elif sha(n) != h: fails.append(f"file differs from the release: {n}")
    import cn_model as M
    for k in KEY_CASES:   # fresh solves from the code
        kw = dict(M.CASES[k]); kw.pop("max_hubs", None)
        r = headline(M.solve_fleet(M.case_params(k), **kw)); ref = man["numbers"]["scenarios"][k]
        if abs(r["transport_cost_bn"] - ref["transport_cost_bn"]) > TOL_BN or abs(r["saving_pct"] - ref["saving_pct"]) > TOL_PCT:
            fails.append(f"re-solve {k}: {r['transport_cost_bn']:.2f} bn / {r['saving_pct']:.2f}% vs release {ref['transport_cost_bn']:.2f} / {ref['saving_pct']:.2f}")
        else: print(f"re-solve {k}: {r['transport_cost_bn']:.2f} bn, {r['saving_pct']:.2f}% - matches the release")
    if (H / "cn_scenarios.json").exists():
        now = saved_numbers()
        for k, ref in man["numbers"]["scenarios"].items():
            v = now["scenarios"].get(k)
            if v is None or abs(v["transport_cost_bn"] - ref["transport_cost_bn"]) > TOL_BN: fails.append(f"saved output {k} differs from the release")
        for k, ref in man["numbers"].get("monte_carlo_median_saving_pct", {}).items():
            v = now.get("monte_carlo_median_saving_pct", {}).get(k)
            if v is None or abs(v - ref) > 0.5: fails.append(f"Monte Carlo median {k}: {v} vs release {ref:.1f} (seeded; should match)")
        for k, ref in man["numbers"].get("backup_saving_pct", {}).items():
            v = now.get("backup_saving_pct", {}).get(k)
            if v is None or abs(v - ref) > TOL_PCT: fails.append(f"backup bracket {k} differs from the release")
    for f in fails: print("FAIL:", f)
    print(f"cn_release_check: {'PASS' if not fails else 'FAIL'} ({len(fails)} problems)")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--write" in sys.argv: write()
    else: sys.exit(check())
