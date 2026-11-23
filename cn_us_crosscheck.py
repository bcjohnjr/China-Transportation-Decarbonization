"""Cross-check of the U.S. model v8.4 heavy-truck efficiency ratios (documented in CN v1.4, CHANGELOG and SM S2).

us2_inputs.py v8.4 sets r_hdv_elec = 2.40/21.1 and r_hdv_fcev = 4.44/21.1.  2.40 is kWh per mile for a battery-electric
Class 8 truck; 21.1 is MJ per mile for a ~6.9 mpg diesel truck (144.9 MJ/gal / 6.87 mpg).  Dividing kWh by MJ makes an
electric truck use 11% of the diesel energy instead of 41% (2.40 x 3.6 / 21.1), so U.S. truck electricity and hydrogen
are understated by a factor of 3.6.  This script reruns the U.S. least-cost and post-gas cases with corrected ratios.
Unmodified copies of the U.S. v8.4 source (us2_model.py, us2_inputs.py, grid_harvester.py) are included in this folder;
their SHA-256 hashes are checked against the pinned values below and written to us_truck_ratio_crosscheck.json.
"""
import hashlib, json
from pathlib import Path

H = Path(__file__).resolve().parent
US_V84_SHA256 = {"us2_model.py": "66f59eef3d8c4db8e2c86a7a539d54c668c3b7f7de86b4021ac914ae18ddbdec",
                 "us2_inputs.py": "5abaebf83c4b019ff0660a423dc26dfdba45a3bdf5c794de30ca8c0b62abda20",
                 "grid_harvester.py": "fcf78c3803f1bef4c32c88437589ccd41f450d9318019fc26fdc9e6b702ead29"}


def main():
    try:
        import us2_model as M
    except ImportError:
        print(json.dumps(json.load(open(H / "us_truck_ratio_crosscheck.json")), indent=1)); return
    found = {f: hashlib.sha256(open(H / f, "rb").read()).hexdigest() for f in US_V84_SHA256}
    assert found == US_V84_SHA256, f"U.S. source files differ from the pinned v8.4 copies: {found}"
    out = {"us_source": {"version": "8.4 (as submitted)", "sha256": found}}
    for lab, fix in (("as_submitted", False), ("corrected_truck_ratios", True)):
        p = M.default_params()
        if fix: p["ENDUSE"]["r_hdv_elec"] = 2.40 * 3.6 / 21.1; p["ENDUSE"]["r_hdv_fcev"] = 4.44 * 3.6 / 21.1
        r = M.solve_learning(p, scenario="least_cost", blend_vol=0.20)
        pet = r["petroleum"]["prices"]["late_2025"]["pretax_bn"] + r["petroleum"]["pipeline_gas_bn"]
        r2 = M.solve_learning(M.post_gas_params(p), scenario="least_cost", blend_vol=0.0, post_gas=True)
        out[lab] = dict(r_hdv_elec=p["ENDUSE"]["r_hdv_elec"], r_hdv_fcev=p["ENDUSE"]["r_hdv_fcev"], electricity_twh=r["enduse"]["el_total"],
                        least_cost_bn=r["transport_cost_bn"], petroleum_late_2025_bn=pet, saving_pct=100 * (1 - r["transport_cost_bn"] / pet),
                        post_gas_bn=r2["transport_cost_bn"], post_gas_saving_pct=100 * (1 - r2["transport_cost_bn"] / pet),
                        emissions_reduction_pct=r["emissions"]["reduction_pct"])
    json.dump(out, open(H / "us_truck_ratio_crosscheck.json", "w"), indent=1); print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
