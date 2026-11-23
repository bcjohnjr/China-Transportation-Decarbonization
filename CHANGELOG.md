# CN v1.6.3 — 23 November 2026 (project and owner costs separated; figures rebuilt from code with a layout check)

**Cost boundary.** Vehicles and machines are bought and run by households, fleets, farms and contractors, not by the
energy project, and China's fleet is already electrifying. Their net extra cost (USD 20.8 bn/yr in the central case: cars
-32.4 bn, trucks, tractors, construction machines and forklifts +53.2 bn) is now reported as a cost to owners, separate
from the energy-system (project) cost, which is the headline. Every solution and Monte Carlo draw carries
`energy_system_cost_bn`, `consumer_vehicle_cost_bn` and `saving_energy_system_pct`; `transport_cost_bn` keeps the total
including owners' costs. Farm charging infrastructure (USD 2.0 bn) moves from the vehicle line to the project. The LP
solution is unchanged (vehicle costs are fixed by the end-use mix); break-even, robustness, backup bracket, regional and
SM tables report both bases. New tests (2,765) and audit checks (138) confirm the split in every case and draw.

**Headline (energy system).** Least cost USD 293.2 bn, 26.7% saving (break-even 0.73; 46.4% at November 2026 prices);
Monte Carlo median 19.7% (9.1-29.7), cheaper than late-2025 petroleum in 99.8% of draws; after gas 23.8%; 230 GW
offshore 20.7%; plausible wind-lull backup 25.0%; moderate stress combination level with petroleum (-0.4%). Including
owners' vehicle costs the numbers of v1.6.2 are unchanged (USD 314.1 bn, 21.5%; Monte Carlo median 3.3%).

**Figures.** `cn_layout_check.py` renders each figure with all text hidden and fails the build if any text or legend
lies on bars, lines, markers, outlines or other text, or two labels overlap (16 figures, 0 problems). Fig. 2: labels
placed in clear space, leaders where a label cannot sit in its area, hub markers moved off the city squares, the
Guangzhou label dropped (no clear space in the Pearl River Delta). Fig. 3: energy-system costs; panel B shows savings
with and without owners' vehicle costs; the U.S. bars and the uncorrected 23% line are removed. Fig. 4: energy-system
distributions, with the total including vehicle costs dashed; no U.S. line. Fig. 6: the shortfall label sits above the
panel at the shortfall year. Figs. 1, 5, 9, S1, S3, S4, S5, S7 and the graphical abstract: labels and legends moved
off the data; Figs. 5, S1, S3 and S5 on the energy-system basis.

**Documents.** Manuscript, supplement, cover letter and title page updated to the new basis (main text 7,955 words);
table S11 caption states the correct comparator (USD 400.2 bn, v1.6.2 said 399.3); Fig. S6 caption describes its four
panels; author name removed from the properties of the anonymised files.

# CN v1.6.2 — 23 November 2026 (referee round 7: independent number audit; three input corrections, all results re-run)

**Number audit.** New `cn_number_audit.py` (120 checks, run by `run_all.sh`) recomputes, from reference values typed into
the script rather than read from `cn_inputs.py`, every unit conversion behind the headline numbers: fuel LHVs against
GB/T 2589-2020 and IPCC 2006, gas volume/energy/price bases, vehicle intensity ratios and their implied kWh/km and
kg H2/100 km, pre-tax fuel prices, the petroleum comparator, well-to-wheel emissions, the cost reconciliation, reactor
learning, pyrolysis gas and carbon, nutrient removals, fertiliser prices on an elemental basis, and the Monte Carlo
percentiles from the raw draws. It found three errors, all corrected:

1. **Heavy-truck ratios mixed heating-value bases.** 21.1 MJ/mi is 144.9 MJ/gal (EIA heat content, HHV) / 6.87 mpg, but
   the model's diesel demand is LHV (42.8 GJ/t). On the LHV basis (x 128,450/137,381 = 0.935) the ratios are 0.438
   (electric) and 0.810 (fuel cell), not 0.410 and 0.758: heavy-truck electricity and hydrogen were 6.5% too low.
   Effect alone: saving 22.8% -> 21.4%. The U.S. cross-check keeps 0.41/0.76, since U.S. demand is in EIA (HHV) quads.
2. **Phosphorus and potassium fertiliser were priced per t of P2O5 and per t of KCl product** (USD 1,100 and 500) while
   every nutrient flow is elemental. Now USD 2,600 per t P and 1,000 per t K (N unchanged at 700). Effect alone: -0.1 pp.
3. **Road and pipeline gas were priced on 36.0 million MMBtu per bcm (~38 MJ/m3 HHV)**, 4% below the HHV matching the
   9.9 TWh/bcm (LHV) used for gas energy. Now 37.5 million MMBtu/bcm (HHV/LHV 1.109). Effect alone: +0.15 pp (petroleum
   comparator USD 399.3 -> 400.2 bn).

Also: LHV source label corrected (values lie between GB/T 2589 and IPCC 2006; only fuel oil is the IPCC value); reactor
approvals restated as about 32 GWt (12 GWe at ~37% efficiency), not 30.

**Headline changes (v1.6.1 -> v1.6.2).** Least cost USD 308.2 -> 314.1 bn, saving 22.8% -> 21.5%; hubs 201 -> 221;
pyrolysis H2 10.8 -> 8.4 Mt and gas 61 -> 48 bcm; emissions 136 -> 130 Mt (93.7%). After gas 19.8% -> 18.6%. 230 GW
offshore 16.7% -> 15.4%. Biological soil carbon 22.3% -> 21.1%. Monte Carlo median saving 4.5% -> 3.3% (least cost),
0.8% -> -0.5% (after gas). Plausible backup saving 20.9% -> 19.8%. Nutrient and soil-carbon balance now costs USD 5.1 bn.

**Documents.** Reference 11 (the related U.S. manuscript) now reads "unpublished manuscript, withdrawn; supplied
confidentially to the editor" in both versions; cover letter, title page and data-availability statements say the code
will be deposited as release tag CN-v1.6.2 at submission rather than that it is already public; the U.S. manuscript is an
editor-only confidential file. Pinned regression test for the no-nutrient case updated (303.4 -> 309.0). Manifest
regenerated.

# CN v1.6.1 — 23 November 2026 (referee round 6: pre-submission corrections; model and results unchanged)

- The United States correction notice for *Science* is removed from the package: the United States manuscript has been
  withdrawn by the authors. The cover letter and title page now describe it as withdrawn; it is still disclosed to the
  editors as a confidential, editor-only file because the present paper reuses its model structure. The manuscript no
  longer calls it "under review".
- Supplementary tables S22-S24 laid out to fit a portrait page: S22 has nutrient sources as rows and cases x elements as
  columns (and now includes green manure and compost); S23 has shorter headings and moves gas use to table S15; S24 has
  short zone names and cost headings. Negative zeros removed from all tables.
- Main text shortened by about 160 words (7,792 words) for a safer margin under the 8,000-word limit.
- README: step-by-step instructions to replace the public repository with this exact release, tag `CN-v1.6.1` and
  archive it with a Zenodo DOI.
- Release manifest regenerated; the model code and all numerical results are identical to CN v1.6.

# CN v1.6 — 23 November 2026 (referee round 5: reproducibility, biological soil carbon, backup bracket, Grid Harvester)

**Model**
- Biological soil-carbon options available in every case: winter legume green manure on up to 6.7 Mha of winter-fallow
  fields (0.29 t stable C and 60 kg fixed N per ha, USD 200/ha) and compost from up to 50 Mt DM a year of livestock
  manure not now returned to fields (0.105 t stable C per t; N, P, K returned; USD 60/t; 0.1 t CO2e/t). Table S25.
- New strict case `least_cost_biological_soc` (and after-gas, cost x2 and no-compost variants): pyrolysis carbon not
  counted, the whole requirement biogenic, priced gap not allowed (`soc_gap_allowed`). Without compost the liquids the
  domestic system cannot then supply are reported as a shortfall priced at USD 400/MWh.
- With these options no reported case uses the priced soil-carbon gap; a test enforces this for the headline cases.
  This also removes the inconsistency in which the nuclear-only thorium fleet looked cheaper than the unrestricted one
  (it had used the priced gap); the two are now identical (USD 297.7 bn, no wind or solar built).
- Grid Harvester restored for the nearshore bioextraction farms: harvest, haul and drone costs are now computed with the
  same Grid Harvester, vessel and drone logistics as the offshore zones (`bioextract_economics`), replacing the generic
  USD 25/t; vessel electricity is in the electricity balance and the Grid Harvester fleet is sized for offshore and
  nearshore areas together (`grid_harvester["nearshore_units"]`).
- Wind-lull backup bracket (`lull_bracket`, table S26): lower bound vs plausible (15% reserve margin, H2 storage at
  USD 25/kg, make-up H2 production, USD 150/kW transmission) vs high (14-day windless lull, 20% reserve, USD 100/kg,
  USD 300/kW). Central saving: 21.5% / 20.9% / 14.5%.
- Monte Carlo adds the green manure and compost cost scale (0.7-1-2).
- Case renamed without version labels: `post_gas_fossil_rule_v14` -> `post_gas_no_biomethane_pyrolysis`.

**Reproducibility**
- `cn_release_check.py` and `cn_release_manifest.json`: SHA-256 of every code and input file, fresh re-solves of the
  central, after-gas, 230 GW offshore and biological soil-carbon cases, and comparison of saved scenario, Monte Carlo and
  backup numbers with the release. `run_all.sh` runs it after a full run. The release was rebuilt from an empty folder.

**Results**
- Central least cost unchanged: USD 308.2 bn, 22.8% (compost and green manure are not needed
  when pyrolysis carbon counts). Biological soil carbon only: USD 310.5 bn, 22.2%.
- After gas: USD 320.5 bn, 19.7% (v1.5: 337.0 bn, 15.6%), because green manure and compost
  close the soil-carbon balance more cheaply than additional biomethane pyrolysis.
- Nearshore seaweed is cheaper with Grid Harvesters (USD 182-242/t) and is now farmed in the least-cost solution.

**Documents and figures**
- Fig. 3 legend lists every cost group (the offshore-seaweed group was missing). Fig. 9B shows the biological cases.
  Graphical abstract added (`graphical_abstract.tif`, 5:2, 300 dpi). Supplementary figures S6 (Grid Harvester) and S7
  (steam-electrolysis heat) now appear in order; supplementary sections renumbered S17-S19.
- Manuscript: carbon split stated as total / sold / to soil; thorium nuclear-only result explained; Monte Carlo median
  saving explained in the Table 1 note; median saving and backup bracket stated in the abstract, discussion and
  conclusions; version labels replaced by physical descriptions; vehicle ownership-cost table S2b reconciled to the
  fleet and system cost.

# CN v1.5 — 22 November 2026 (nutrient and soil-carbon balance; nearshore bioextraction)

**Model**
- Nitrogen, phosphorus and potassium balance (`nutrient_n/p/k` LP rows): nutrients removed with residues, bamboo, hemp
  stalk and bagasse must be returned by digested HTL wastewater, HTL hydrochar, gasifier ash, ethanol stillage,
  offshore or nearshore seaweed, or bought as mineral fertiliser (production emissions counted). Surplus recovered
  nutrients may be sold at 70% of fertiliser prices. Inputs in `NUTRIENTS` (tables S20-S21).
- HTL product streams made explicit: the aqueous phase (process wastewater, not biochar) is digested to biomethane
  (0.35 MWh CH4/t feed, 1% slip) and a nutrient-rich digestate; the solids are hydrochar. Biomethane can be sold or fed
  to pyrolysis, displacing fossil gas. Methane is valued on the same HHV basis as `pyro_cost_per_kg`.
- Stable soil-carbon balance (`soil_carbon` and `soil_carbon_biogenic` rows): residue carbon times humification
  coefficients must be replaced by stable hydrochar, digestate and seaweed carbon (at least half) and optionally
  pyrolysis carbon spread as a soil amendment (90% stable; the soil-amendment market is now unpaid and counts toward
  the balance). If no feasible solution closes it, the LP is re-solved with a gap priced at USD 500/t C and counted as
  an emission; the hub search prefers hub counts that close the balance.
- After gas, pyrolysis may run on biomethane only (`biogenic_pyrolysis`); `gas_for_pyrolysis_bcm` now reports fossil
  gas only. Pyrolysis hydrogen carbon intensity scales the fossil-methane terms by the fossil share.
- Nearshore bioextraction (`BIOEXTRACT`, table S19): six eutrophic coastal zones (Liaodong Bay, Haizhou Bay, Yangtze
  plume at Zhoushan-Xiangshan, Fujian bays, Pearl River estuary, Qinzhou Bay) with species chosen for each water
  (Saccharina japonica, Gracilariopsis lemaneiformis, Gracilaria bailinae, G. tenuistipitata); Pyropia expansion on
  the Subei shoal, Ulva and Sargassum-for-soil excluded. Seaweed goes to HTL or, washed, to soil. Optional payment for
  N and P removed. In design scenarios every zone is farmed to its cap.
- The seaweed fertiliser credit is removed (nutrients now enter the balance, so they are not counted twice).
- Monte Carlo adds humification, hydrochar stability and fertiliser price ranges.
- New cases: no nutrient/soil-carbon balance (v1.4 accounting), nutrient balance only, pyrolysis carbon not counted,
  humification x1.5, hydrochar stability 0.3, fertiliser x1.5, bays farmed in full, N payment USD 10 and 30/kg,
  after gas without biomethane pyrolysis (v1.4 rule), soil-carbon gap priced at USD 1000/t C.

**Results (central least cost)**
- USD 308.2 bn/yr, 22.8% saving (v1.4: 303.4 bn, 24.0%); the v1.4 number is reproduced exactly when the
  balance is switched off. Pyrolysis rises to 10.8 Mt H2 because its carbon replaces soil carbon; hubs 201.

**Outputs, tests and documents**
- `nutrients`, `bioextraction`, `hydrochar_mt`, `biomethane_to_pyrolysis_bcm`, `pyrolysis_biogenic_share`,
  `soc_fallback` in every solution; `cn_robustness.json["nutrients"]`; regional nearshore seaweed.
- Fig. 9 (nutrient and soil-carbon balance, nearshore N removal); nearshore zones on Fig. 2; tables S19-S24;
  supplementary section S19; manuscript sections 2.6, 3.4.
- New tests: N, P, K balances close; returns non-negative; SOC requirement met (or priced gap); biogenic share;
  biomethane use <= production; HTL returns <= HTL feed; nearshore areas within caps; no fossil gas after gas;
  v1.4 reproduced with the balance off; design farms every zone; emissions of fertiliser and gaps counted.

# CN v1.4.1 — 22 November 2026

- Repository address updated to https://github.com/bcjohnjr/China-Transportation-Decarbonization (title page, README, CITATION.cff); release tag CN-v1.4.1.
- Model code, inputs and results are unchanged from CN v1.4.

# CN v1.4 — 22 November 2026 (response to fourth referee report)

- Wind-lull screen: sensitivities with no wind, reactor availability 80%, turbines sized for 60% of reactor heat and a
  14-day lull (`LULL_VARIANTS`, `lull_sensitivity()`, new `cn_lull.py`, table S18); backup costs labelled lower bounds
  (hydrogen storage, replacement electrolyser capacity and delivery not priced); turbine-sizing assumption stated.
- Supplementary S10 gives the derived steam-electrolysis heat inputs instead of the superseded 6.4 kWh_th/kg; "published"
  U.S. numbers now "submitted"; version-history remarks removed from the publication text.
- README: steam electrolysis is available in both eras; U.S. cross-check files described as included and hash-checked.
- Cover letter lists the editor-only enclosures; a separate submission package (not the public code repository) contains
  the related U.S. manuscript and the correction notice.
- New tests for the lull sensitivities.

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
