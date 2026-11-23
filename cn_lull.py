"""Wind-lull adequacy screen and its sensitivities, recomputed from the saved solutions (CN v1.6).

Adds `lull_screen` and `lull_sensitivity` to cn_robustness.json without re-solving the model.  Screening calculation only:
not an hourly dispatch, reserve or stability analysis; backup costs are lower bounds (see cn_model.lull_screen)."""
import json
from pathlib import Path
import cn_model as M

H = Path(__file__).resolve().parent
S = json.load(open(H / "cn_scenarios.json")); RB = json.load(open(H / "cn_robustness.json"))
RB["lull_screen"] = {n: M.lull_screen(S[n], M.case_params(n)) for n in ("least_cost", "post_gas_least_cost", "least_cost_no_nuclear",
                                                                       "least_cost_hub_cap_30", "least_cost_reactor_high")}
RB["lull_sensitivity"] = M.lull_sensitivity(S)
RB["lull_bracket"] = {n: M.lull_bracket(S[n], M.case_params(n)) for n in ("least_cost", "post_gas_least_cost", "least_cost_hub_cap_30",
                                                                         "least_cost_no_nuclear", "design_half_offshore")}
for n, v in RB["lull_bracket"].items():
    print("bracket", n, {k: (round(x["cost_bn"], 2), round(x["saving_pct"], 1)) for k, x in v.items()})
json.dump(RB, open(H / "cn_robustness.json", "w"), indent=1, default=float)
for c, v in RB["lull_sensitivity"].items():
    print(c, {k: (round(x["shortfall_gw"], 1), round(x["indicative_cost_bn"], 2)) for k, x in v.items()})
