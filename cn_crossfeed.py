"""Reactor-heated seafood cascade with cross-feeding: by-product meals from one farmed species feed another.

Streams (all t/yr, dry or as stated).  Production levels come from the least-cost case: fish and shrimp from
reactor-heated recirculating aquaculture (RAS); feed-grade kelp from China's existing seaweed industry (~20% of kelp
goes to aquaculture feed [S: Submariner 2018]); hemp press meal from the land-biomass solution.
  1. RAS fish (tilapia, grouper, large yellow croaker): processing by-products -> fishmeal + fish oil -> shrimp feed.
  2. RAS whiteleg shrimp: heads and shells -> shrimp meal -> fish feed (replacing fishmeal), chitin co-product.
  3. Dissolved nitrogen in RAS effluent -> Ulva tanks (heated by the same low-grade reactor heat) -> Ulva meal ->
     abalone and fish feed.
  4. Kelp and Gracilaria -> abalone and sea cucumber (herbivores that already eat macroalgae in Chinese farms).
  5. Greenhouse vegetable waste -> black soldier fly larvae -> insect meal -> fish feed.
  6. Hemp press meal -> fish feed (plant protein).
The balance reports how much of each species' feed (and of the fishmeal requirement) is met inside the loop.  All
coefficients are screening assumptions [A] from the aquafeed literature; feed approvals, contaminant limits (e.g. on
recycled animal protein) and digestibility must be checked before any claim.  Not part of the transport cost.

Writes cn_crossfeed.json.  Run after cn_model.py.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
C = dict(
    fish=dict(fcr=1.4, protein=0.32, fishmeal_incl=0.10, oil_incl=0.03, max_shrimpmeal=0.08, max_insect=0.10, max_hemp=0.12, max_ulva=0.05,
              byproduct=0.45, meal_yield=0.21, oil_yield=0.05),
    shrimp=dict(fcr=1.3, protein=0.38, fishmeal_incl=0.20, oil_incl=0.02, byproduct=0.40, meal_yield=0.25, chitin_yield=0.05),
    abalone=dict(production_t=300_000.0, algae_dry_per_kg=2.4, max_ulva_share=0.30),      # ~20 kg wet algae per kg abalone
    sea_cucumber=dict(production_t=300_000.0, algae_dry_per_kg=1.5),
    protein=dict(fishmeal=0.62, shrimpmeal=0.40, insect=0.45, hemp=0.33, ulva=0.20),
    ras_n=dict(retention=0.30, dissolved=0.50, recovery=0.60, ulva_n=0.035),
    bsf=dict(veg_waste_frac=0.15, meal_per_t_wet=0.03),
    kelp_feed_t=300_000.0)


def balance(fish_t, shrimp_t, veg_t, hemp_meal_t):
    F, S = C["fish"], C["shrimp"]; P = C["protein"]
    feed_f = fish_t * F["fcr"]; feed_s = shrimp_t * S["fcr"]
    fm_need = feed_f * F["fishmeal_incl"] + feed_s * S["fishmeal_incl"]
    fishmeal = fish_t * F["byproduct"] * F["meal_yield"]; fishoil = fish_t * F["byproduct"] * F["oil_yield"]
    shrimpmeal = shrimp_t * S["byproduct"] * S["meal_yield"]; chitin = shrimp_t * S["byproduct"] * S["chitin_yield"]
    # fishmeal goes to shrimp first (the species most dependent on marine protein); shrimp meal to fish
    fm_to_shrimp = min(fishmeal, feed_s * S["fishmeal_incl"]); fm_to_fish = min(fishmeal - fm_to_shrimp, feed_f * F["fishmeal_incl"])
    sm_to_fish = min(shrimpmeal, feed_f * F["max_shrimpmeal"])
    insect = veg_t * C["bsf"]["veg_waste_frac"] * C["bsf"]["meal_per_t_wet"]; insect_to_fish = min(insect, feed_f * F["max_insect"])
    hemp_to_fish = min(hemp_meal_t, feed_f * F["max_hemp"])
    # nitrogen from fish and shrimp feed not retained, dissolved and recovered by Ulva
    feed_n = (feed_f * F["protein"] + feed_s * S["protein"]) / 6.25
    n_rec = feed_n * (1 - C["ras_n"]["retention"]) * C["ras_n"]["dissolved"] * C["ras_n"]["recovery"]
    ulva = n_rec / C["ras_n"]["ulva_n"]
    A, SC = C["abalone"], C["sea_cucumber"]
    alg_need = A["production_t"] * A["algae_dry_per_kg"] + SC["production_t"] * SC["algae_dry_per_kg"]
    ulva_to_abalone = min(ulva, A["production_t"] * A["algae_dry_per_kg"] * A["max_ulva_share"]); ulva_to_fish = min(ulva - ulva_to_abalone, feed_f * F["max_ulva"])
    alg_supply = C["kelp_feed_t"] + ulva_to_abalone
    internal_protein = (fm_to_shrimp + fm_to_fish) * P["fishmeal"] + sm_to_fish * P["shrimpmeal"] + insect_to_fish * P["insect"] + hemp_to_fish * P["hemp"] + ulva_to_fish * P["ulva"]
    feed_protein = feed_f * F["protein"] + feed_s * S["protein"]
    internal_marine = fm_to_shrimp + fm_to_fish + sm_to_fish
    return dict(inputs=dict(fish_t=fish_t, shrimp_t=shrimp_t, vegetables_t=veg_t, hemp_meal_t=hemp_meal_t),
                feed_t=dict(fish=feed_f, shrimp=feed_s), fishmeal_requirement_t=fm_need,
                produced_t=dict(fishmeal=fishmeal, fish_oil=fishoil, shrimp_meal=shrimpmeal, chitin=chitin, insect_meal=insect, ulva_dry=ulva),
                flows_t=dict(fishmeal_to_shrimp=fm_to_shrimp, fishmeal_to_fish=fm_to_fish, shrimpmeal_to_fish=sm_to_fish, insect_to_fish=insect_to_fish,
                             hemp_meal_to_fish=hemp_to_fish, ulva_to_abalone=ulva_to_abalone, ulva_to_fish=ulva_to_fish,
                             kelp_to_abalone_and_sea_cucumber=C["kelp_feed_t"]),
                marine_protein_need_met_internally=min((internal_marine) / fm_need, 1.0) if fm_need else 0.0,
                feed_protein_met_internally=internal_protein / feed_protein if feed_protein else 0.0,
                herbivore_algae_need_t=alg_need, herbivore_algae_met=min(alg_supply / alg_need, 1.0) if alg_need else 0.0,
                nitrogen_recovered_t=n_rec, external_fishmeal_displaced_t=internal_marine,
                external_protein_displaced_t=internal_protein, coefficients=C)


def main():
    S = json.load(open(HERE / "cn_scenarios.json")); f = S["least_cost"]["food"]
    out = dict(least_cost=balance(f["fish_mt"] * 1e6, f["shrimp_mt"] * 1e6, f["vegetables_mt"] * 1e6, f["hemp_meal_mt"] * 1e6),
               post_gas=balance(S["post_gas_least_cost"]["food"]["fish_mt"] * 1e6, S["post_gas_least_cost"]["food"]["shrimp_mt"] * 1e6,
                                S["post_gas_least_cost"]["food"]["vegetables_mt"] * 1e6, S["post_gas_least_cost"]["food"]["hemp_meal_mt"] * 1e6))
    json.dump(out, open(HERE / "cn_crossfeed.json", "w"), indent=1)
    b = out["least_cost"]
    print(f"fish {b['inputs']['fish_t']/1e6:.2f} Mt, shrimp {b['inputs']['shrimp_t']/1e6:.2f} Mt; marine protein met internally "
          f"{100*b['marine_protein_need_met_internally']:.0f}%, feed protein {100*b['feed_protein_met_internally']:.0f}%, "
          f"N recovered {b['nitrogen_recovered_t']/1e3:.0f} kt, Ulva {b['produced_t']['ulva_dry']/1e3:.0f} kt")


if __name__ == "__main__":
    main()
