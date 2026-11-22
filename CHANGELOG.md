# CN v1.3 — 22 November 2026 (response to third referee report)

**Model and code**
- Steam-electrolysis heat inputs are now derived, not assumed: `cn_htse_heat.py` computes a temperature-enthalpy balance
  per kg H2 (800 C stack, 0.5 MPa, 80% steam utilisation, counterflow high-temperature recuperator with a 25 K minimum
  approach checked along the exchanger, low-temperature recovery by sensible cooling and condensation; NIST Shomate gas
  enthalpies, steam-table water properties). External steam-raising heat 6.87 kWh/kg at <= 152 C (v1.2: 6.4), electric
  topping 0.68 kWh/kg (v1.2: 1.0 with reactor steam, 2.0 without), recuperator and heater cost +USD 0.035/kg added to
  the electrolyser capital charge. Table S16, fig. S7. New cases: 3 kWh/kg topping; no low-temperature recovery.
- Stylised wind-lull adequacy screen (`lull_screen()`, `LULL` inputs, table S17): a windless, overcast 7-day winter
  period with flexible loads stopped and hub heat sent to turbines; shortfall priced as hydrogen-fired backup.
  Distinguishes annual resource adequacy from operational feasibility; it is not an hourly dispatch model.
- New tests: heat-balance closure, recuperator approach, derived inputs used, lull-screen ordering, new sensitivities.
- `CITATION.cff` added for the fixed release.

**Manuscript and submission**
- Electrolyser heat integration documented (methods 2.3, SM S8); HTR-PM process steam "up to about 500 C" cited.
- Abstract and discussion state that the model tests annual resource adequacy, not hourly operation, and give the
  least favourable car ownership-cost result; average transaction prices described as not like-for-like.
- Wind-lull results in section 3.2; limitations sharpened.
- Cover letter encloses a copy of the related U.S. manuscript for the editors and the draft correction notice, and no
  longer states that Science has been informed. Title page gives the repository URL and planned release tag.
- Supplementary Word file images compressed to keep it under the journal's advisory 2 MB.

# CN v1.2 — 22 November 2026 (response to second referee report)

**Accounting corrections (all results regenerated)**
- Steam-electrolysis heat by temperature: the 6.4 kWh_th/kg for water heating and evaporation now comes from the
  process-steam (mid) tier or electric boilers (0.98), not the drying tier that heat pumps (COP 2.5) could supply; a net
  superheat of 1.0 kWh/kg (2.0 without reactor steam) lifts steam to the ~800 C stack inlet with electric heaters (0.95),
  or with top-tier reactor heat when the outlet is >= 850 C (`htse_superheat_elec()`).
- Heat sold to food production has no value inside the transport boundary (v1.1 credited USD 8/MWh); its gross value is
  reported separately (`food_heat_value_outside_boundary_bn`) and the v1.1 accounting is kept as a sensitivity case.
- 2050 vehicle stocks are no longer multiplied by service growth (v1.1 annualised 483 instead of 420 million cars, and
  scaled truck and machine fleets the same way); stocks now scale only with departures from central growth (Monte Carlo).
- New cases: `least_cost_us_v84_htse_rule` (replaces the stale v1.0 comparison in SM S15), `least_cost_no_nuclear_alkaline`,
  `least_cost_food_credit`.
- U.S. cross-check made reproducible: unmodified U.S. v8.4 source files (us2_model.py, us2_inputs.py) are included and
  their SHA-256 hashes are checked by `cn_us_crosscheck.py`, which `run_all.sh` now runs.
- New tests for the three corrections, the after-gas fossil-gas boundary and the pinned U.S. hashes.

**Manuscript**
- Abstract states the Monte Carlo median next to the central value; "four questions" corrected to five; regional results
  described as screening allocations; gas-era use of fossil gas for pyrolysis and pipeline compression stated; Fig. 8 alt
  text generated from outputs; Fig. 2 labels adjusted. Submission files (anonymised manuscript, title page, supplementary
  materials, cover letter) are included in the package.

# CN v1.1 — 22 November 2026 (response to referee report)

**Model and code**
- Car ownership cost is now derived, not assumed: purchase-price difference (annualised, 12 yr, 5%), expected battery
  replacement, maintenance and repair, and insurance (`LDV_TCO`, `ldv_bev_net()` in `cn_inputs.py`; table S2b). Central
  value -93.3 USD/car/yr (v1.0: -100); low -389.6, high +503.9 set the Monte Carlo triangle (v1.0: -400/-100/+400).
- Stress cases (re-optimised): BEV net cost 0, +100 USD/yr, high and low derivations; car stock 350 and 500 million; no
  carbon-product revenue; commodity carbon markets only; residues -25% and -50%; at most 60 or 30 hubs; tighter grid and
  firming costs; BEV +100 with no carbon revenue; moderate and severe combinations (also after gas). Written to
  `cn_robustness.json`; table 2, table S15, fig. S5.
- Emissions-boundary sensitivities (electricity 25 g/kWh, 3% methane leakage, residue soil-carbon losses of 20 and 40 g/MJ,
  reactor construction and fuel cycle 3 g/kWh of hub heat; table S12) via `EMIS` parameters and `emissions_boundary()`.
- Carbon durability classes for each carbon market (`CARBON_DURABILITY`; table S13).
- Build-rate and system-structure screen (`feasibility()`; table S14). Not an hourly dispatch model.
- New tests (robustness ordering, hub caps, boundary monotonicity, carbon durability balance, derivation used).
- Figures: Fig. 2 map labels repositioned with halos; Fig. 3 says "as submitted" for the U.S. model; Fig. 5 legend
  names both gas-era hydrogen routes; new fig. S5 (stress tests); Grid Harvester becomes fig. S6.

**Manuscript**
- Retitled to state costs, conditions and limits; abstract, discussion and conclusions now lead with the conditions
  (car ownership cost, carbon markets, residues) and the stress-test results; Monte Carlo results described as
  conditional sensitivity outcomes, not probabilities; reactor comparison labelled a prospective technology sensitivity.
- New methods sections 2.10 (stress tests and feasibility screens) and car-cost derivation in 2.2; residue sustainability
  in 2.5; carbon durability and life-cycle boundary results in 3.1; stress tests and build rates in 3.2; table 2.
- Double-anonymized submission: author details moved to a separate title page; the related U.S. manuscript is cited
  anonymously and disclosed in the cover letter. CRediT roles listed on the title page.
- References renumbered in order of citation; eight references added; an access date in the future corrected.

# CN v1.0 — 22 November 2026 (first China release)

China counterpart of the United States model v8.4, prepared for *Clean Energy* (Oxford University Press). Structure, cost
accounting, heat cascade, Grid Harvester screen, carbon markets, emissions method, petroleum break-even and food
accounting follow v8.4. Differences:

**Scope and data**
- Study area: mainland China with the five autonomous regions, plus Hong Kong and Macau in one system; Taiwan as a
  separate island system (own demand, resources, prices and LP).
- 2025 baseline from Chinese fuel statistics (gasoline 155 Mt, diesel 203 Mt, jet 40.2 Mt, transport gas 42.6 bcm), bonded
  bunkers, Hong Kong jet imports and EIA Taiwan data. LNG/CNG trucks included in heavy road demand and the comparator.
- Pre-tax petroleum prices from NDRC retail caps minus 13% VAT and consumption tax, at 2025 and 2026 exchange rates.
- 5% discount rate (U.S.: 7%); Chinese capital costs for renewables, reactors, conversion, vehicles and seaweed logistics.

**Model changes**
- Heavy-truck drivetrain ratios corrected to kWh/kWh: `r_hdv_elec = 2.40 × 3.6 / 21.1 = 0.41` and
  `r_hdv_fcev = 4.44 × 3.6 / 21.1 = 0.76`. U.S. v8.4 used 0.114 and 0.210 (kWh/mi divided by MJ/mi). A sensitivity
  case (`least_cost_us_truck_ratios`) and `cn_us_crosscheck.py` quantify the effect on both models.
- Extended-range share added for cars; fuel-cell truck energy also lightweighting-adjusted.
- Concentrated solar power with storage (counts as firm), a second onshore wind cost tier, and an imported-renewable-liquid
  option (Taiwan only).
- Hub = six 250-MWt modules (HTR-PM600 layout), 1,500 MWt. Methane preheat is computed from the reactor outlet
  temperature. Five reactor technologies (HTR-PM, 950°C VHTR, thorium MSR, sodium fast, ACP100) as alternative hubs.
- Reactor learning: every published case is solved at every integer hub count 0–1,500 (bounded exhaustive search, as v5+
  used for sustainable fission); Monte Carlo uses a 25-hub grid refined to single hubs.
- Biomass: regional residue tiers; autonomous-region ethanol feedstocks (cassava, molasses, sweet sorghum with bagasse to
  the residue pool, Jerusalem artichoke, sweet potato, aged grain) and oil feedstocks (UCO, jatropha, cottonseed residues,
  woody oils) replace U.S. corn ethanol and the single HEFA oil pool.
- Nine Chinese and Taiwan Strait seaweed zones with species farmed in China.
- No hydrogen blending into building gas in the headline cases (transport-only boundary without allocation); a 20% blend
  is a sensitivity (`least_cost_blend20`).
- New modules: `cn_gas.py` (China gas balance with domestic, pipeline and LNG supply), `cn_regions.py` (regional screen),
  `cn_crossfeed.py` (seafood cross-feeding), fissile accounting including spent-fuel and military plutonium pools
  (inventory level only), `cn_sm_tables.py` (tables generated from code).
- Petroleum comparator scales with service growth in deterministic cases as well as in the Monte Carlo.
- Steam electrolysis at the hubs is available in the gas era as well as after gas (U.S. v8.4 allowed it only after gas).
  At China's gas price it becomes the main gas-era hydrogen route; pyrolysis is then limited by the capped carbon markets.
  Effect on the China least-cost case: USD 303.0 → 300.4 bn, pyrolysis gas 93 → 33 bcm. Re-solving the U.S. v8.4
  least-cost case with the same change gives an identical result, so U.S. numbers are unaffected.
- Supplementary tables use separator widths proportional to content so that Word output keeps text columns readable.
