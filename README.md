# CN v1.7 — Evidence-constrained agricultural extension (26 November 2026)

Apply this delta to the existing flat CN v1.6.4 repository root. Do not delete the reference files. Only README.md replaces an existing file; new filenames are versioned. Python 3.13 recommended. Install `python -m pip install -r requirements-cn17.txt`, then run `RUN_CN17.bat` on Windows or `sh RUN_CN17.sh` on Linux. All data needed for this extension are included. No network access needed after dependency installation. The runner regenerates the province inputs, inventory, seven cases, 128 conditional draws, figures and verifies against a fixed release regression. Native Windows execution not independently tested. The old `run_all.sh` regenerates only the reference model, not the new extension.

Main result (annual 2050 screen, 2026 USD): energy system $301.44bn; including vehicle owners $322.28bn; transport emissions 131.17 Mt CO2e (93.68% reduction). Incremental agricultural account $7.77bn, 22.41 Mt avoided; combined $330.06bn and 1.966 Gt avoided. Continued petroleum comparator $400.20bn at inherited late-2025 prices. The incremental methane screen is not a joint optimization or a credit within the original transport LP. At 1% fugitive methane leakage, manure digestion alone has negative net mitigation without displacement credit. No incremental sewage or municipal waste supply credited. See CN17_DATA_AND_METHODS.md. The reference 1,000-draw study is not rerun; 128 new draws fix transport technology and ownership assumptions. No hourly reliability or partially electrified future reference is established. Xizang is not a net liquid supplier in the revised regional reporting screen.

The original solver and source reference outputs remain intact. Original reference figures are explicitly identified as such in the editorial materials; the new Fig10, FigS8 and graphical abstract carry the updated numbers. CN17_Fig2_corrected_routes.tif preserves the user-corrected route artwork at native resolution. Do not confuse the original v1.6.4 figures with the new headline case.

---

## Archived CN v1.6.4 reference instructions (unchanged)

# China transport decarbonisation model — CN v1.6.4

Repository: https://github.com/bcjohnjr/China-Transportation-Decarbonization

Code and data for J. K. Bily, C. Pahl and P. Valdes Bacallao, *Electrification, reactor heat and regional biofuels for a petroleum-free transport system in the world's largest emitter: costs, conditions and limits* (prepared for submission to *Clean Energy*, Oxford University Press).

Contact: Jonathan Karl Bily, jonathan@cloudwashlaundry.com

The model asks whether all transport energy in mainland China (including the Guangxi, Inner Mongolia, Ningxia, Xizang/Tibet and Xinjiang autonomous regions), Hong Kong and Macau could be supplied without petroleum in 2050, at what annual cost, and what happens once natural gas is no longer used for hydrogen. Taiwan is modelled as a separate island system. Its components:

- **Reactor hubs.** Six-module HTR-PM-class hubs run a heat cascade: steam electrolysis in both eras, plus methane pyrolysis while gas lasts, electricity, biocrude upgrading, drying, then greenhouses and fish farms. Thorium molten-salt, sodium fast, 950°C and light-water SMR alternatives are tested.
- **Electricity.** Onshore wind (two cost tiers), solar, concentrated solar with storage, light-water reactors, offshore wind.
- **Land biomass.** Crop straw by region, forestry and bamboo residues, new bamboo and hemp, and the autonomous regions' crops: Guangxi cassava, molasses, bagasse and jatropha; sweet sorghum in Inner Mongolia, Xinjiang and Ningxia; Jerusalem artichoke; cotton stalks; Ningxia sweet potato; Xizang grassland and forestry residues.
- **Electric expressways** on 60,000 km of freight corridors, plus battery-electric vehicles and machines.
- **Optional offshore wind with seaweed** from Liaoning to Hainan and the Taiwan Strait, harvested by Grid Harvesters (solar-powered harvesting heads that cut and pump seaweed between the long-lines; `grid_harvester.py`).
- **Nutrient and soil-carbon balance (since v1.5).** For N, P and K, what harvesting removes must come back to the land: digested HTL wastewater (the aqueous phase, which also yields biomethane), HTL hydrochar, gasifier ash, ethanol stillage, seaweed, or bought mineral fertiliser. Stable soil carbon must also be replaced, at least half from biogenic sources (hydrochar, digestate, seaweed) and the rest optionally from pyrolysis carbon. After gas, pyrolysis may run on biomethane.
- **Nearshore bioextraction (since v1.5)**: seaweed farms in six eutrophic coastal zones (Liaodong Bay, Haizhou Bay, the Yangtze plume, the Fujian bays, the Pearl River estuary, Qinzhou Bay), with species chosen for each water (Saccharina, Gracilariopsis lemaneiformis, Gracilaria bailinae, G. tenuistipitata), harvested by the same Grid Harvesters, vessels and drones as the offshore farms (v1.6).
- **Biological soil-carbon options (new in v1.6)**: winter legume green manure (up to 6.7 Mha) and manure compost (up to 50 Mt DM a year); a strict case replaces soil carbon from biological sources only, without pyrolysis carbon and without the priced gap.
- **Backup bracket for wind lulls (new in v1.6)**: lower bound, plausible and high backup costs (`cn_robustness.json["lull_bracket"]`, table S26).
- **Pyrolysis carbon** sold to capped markets or spread on fields as soil carbon; **food** from reactor heat with **seafood cross-feeding** (reported outside the transport cost; heat sold to food earns nothing in the transport boundary).

## Main results (2050, 2026 US$ per year, pre-tax, transport-only)

Energy system = the project cost (supply, conversion, grids, charging, electric expressways, rail electrification, hydrogen delivery, net of co-product credits). With vehicles adds the net extra cost of electric and fuel-cell vehicles and machines, which their owners pay (USD 20.8 bn in mainland cases, 1.0 bn for Taiwan). Petroleum at late-2025 pre-tax prices: USD 400.2 bn (mainland), 15.6 bn (Taiwan). Saving, MC and break-even are for the energy system.

| Case | Energy system | With vehicles | Saving | MC median cost (5–95%) | MC cheaper | Break-even | Hubs | CO~2~e |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| Least cost, gas era | 293.2 | 314.1 | 26.7% | 328 (273–402) | 99.8% | 0.73 | 221 | 130 |
| Gas era, 230 GW offshore wind with seaweed | 317.5 | 338.4 | 20.7% | 361 (309–433) | 98% | 0.79 | 227 | 124 |
| Gas era, 460 GW offshore wind with seaweed | 348.1 | 369.0 | 13.0% | — | — | 0.87 | 57 | 130 |
| Gas era, high reactor cost | 307.5 | 328.3 | 23.2% | — | — | 0.77 | 12 | 150 |
| Gas era, no nuclear | 346.7 | 367.5 | 13.4% | — | — | 0.87 | 0 | 106 |
| Gas era, thorium molten-salt hubs | 277.0 | 297.9 | 30.8% | — | — | 0.69 | 404 | 129 |
| After gas | 305.0 | 325.8 | 23.8% | 346 (281–439) | 96% | 0.76 | 268 | 99 |
| After gas, no nuclear | 352.0 | 372.9 | 12.0% | — | — | 0.88 | 0 | 101 |
| Closed thorium cycle (hypothetical) | 281.4 | 302.3 | 29.7% | — | — | 0.70 | 423 | 100 |
| Closed thorium cycle, cost premium | 307.3 | 328.2 | 23.2% | — | — | 0.77 | 421 | 99 |
| Taiwan island system | 16.9 | 17.9 | −8.0% | — | — | 1.08 | 7 | 8 |
| Taiwan island system, no nuclear | 19.5 | 20.5 | −25.1% | — | — | 1.25 | 0 | 8 |

- The least-cost energy system costs **USD 293.2 bn**, **26.7%** less than late-2025 pre-tax petroleum (break-even at 0.73 × late-2025 prices; 46.4% less at November 2026 prices, 1.37 × late-2025). **Vehicles are a cost to their owners, not to the project:** the net extra cost of electric and fuel-cell vehicles and machines is USD 20.8 bn/yr (cars save owners 32.4 bn; trucks, tractors and construction machines cost 53.2 bn more); including it the total is USD 314.1 bn, a 21.5% saving. Car-cost assumptions change only the owners' share (with no ownership advantage for battery-electric cars the saving including owners' costs is 12.2%; at +100 USD/car/yr 2.3%). On the energy-system basis, no carbon-product revenue gives 20.1%, residues −50% 8.0%, and a moderate combination of adverse assumptions (commodity carbon only, residues −25%, high reactor cost, tight grid) brings the system level with late-2025 petroleum (−0.4%) (Table 2 of the manuscript; `cn_robustness.json`).
- **Who pays, and which saving to quote.** The energy-system saving is the project comparison. For China's total transport cost, the saving including owners' vehicle costs is the relevant measure (21.5% central; Monte Carlo median 3.3%, 54% of draws cheaper).
- **Carbon co-products are assumed markets.** The central case fills the 1.5 Mt/yr carbon-fibre and hydrogen-tank cap and the 4 Mt/yr anode-graphite cap; world carbon-fibre demand in 2025 was about 149–225 kt and China's anode shipments about 2.9 Mt. Without any carbon revenue the energy-system saving is 20.1%; with commodity markets only, 21.3%.
- **Nutrients and soil carbon:** harvesting removes 2.93 Mt N, 0.62 Mt P and 4.98 Mt K a year; process streams return 53%, 94% and 91% and mineral fertiliser the rest. 27.4 Mt C/yr of stable soil carbon is replaced by hydrochar (14.8), digestate (5.5) and pyrolysis carbon (7.1). The modelled annual replacement costs USD 5.1 bn/yr; it is not a demonstration of long-term soil health. Nearshore farms on 3,600 km² have a modelled potential to remove 184 kt N and 25 kt P a year for USD 0.1 bn/yr more.
- Emissions fall from 2,074 to 130 Mt CO2e/yr (93.7%) in the gas era and to 99 Mt after gas. China emitted about 32% of world fossil CO2 in 2025.
- Pyrolysis needs 48 bcm/yr of gas (11% of 2025 consumption); first gas shortfall 2141 (range 2100–2175); import share peaks at 37%.
- A closed thorium molten-salt fleet (423 hubs) has an energy-system cost of USD 281.4 bn but needs ~380 t of start-up fissile material; China's military plutonium (IPFM 2.9 ± 0.6 t) would start ~0.3 GWe of fast reactors.
- All five autonomous regions produce more renewable liquids than they use; Hong Kong, Macau and Taiwan depend on outside supply; Taiwan's island energy system costs 8% more than petroleum (14% with owners' vehicle costs).
- Conditional Monte Carlo (1,000 independent draws from assumed ranges): the least-cost energy system is cheaper than late-2025 petroleum in 99.8% of draws, median saving 19.7% (5–95%: 9.1 to 29.7). Including owners' vehicle costs, whose ranges are wide, the median is 3.3% and 54% of draws are cheaper. This is a sensitivity result, not a probability.
- Build-rate screen: 1,326 modules of 250 MWt, about 70 a year from 2032; with at most 30 hubs the energy-system saving is still 24.1%. Wider life-cycle boundaries raise residual emissions from 130 to as much as 334 Mt.

## Updating the GitHub repository to v1.6.4

The public repository must hold exactly this release before the manuscript is submitted; reviewers and editors will follow the link on the title page.

1. Upload every file in this flat folder to the repository root, replacing files with the same names. No folders are needed.
2. Delete every older versioned document still in the repository: `MANUSCRIPT_CN_V1.*.md`, `SUPPLEMENTARY_MATERIALS_CN_V1.*.md` and `*_CN_V1.*.docx` for V1.3 to V1.6.3. Only the V1.6.4 files should remain. Also delete `cn_us_crosscheck.py`, `cn_us_crosscheck_log.txt`, `us2_model.py`, `us2_inputs.py` and `us_truck_ratio_crosscheck.json`, which are no longer part of the release.
3. Check that `README.md`, `CHANGELOG.md` and `CITATION.cff` on GitHub show CN v1.6.4, and that `cn_release_manifest.json` is present.
4. Create a release with tag `CN-v1.6.4` (the cover letter and title page cite this tag).
5. Archive the release with a DOI: connect the repository to Zenodo (zenodo.org, sign in with GitHub, switch the repository on), then publish the GitHub release; Zenodo mints the DOI. Add the DOI to `CITATION.cff` and the title page.
6. After submission, do not overwrite the release; record any later change as a new tagged version.

New in v1.6.4: the United States cross-check and the U.S. model files are removed; submission TIFFs are RGB at 300 dpi and checked by `cn_figures.py`; the manuscript discusses carbon-product commercialisation and labels the reactor-learning, heat-recovery and nutrient assumptions; the release was rebuilt from an empty folder (see CHANGELOG.md).

In v1.6.3: the net cost of electric and fuel-cell vehicles and machines is reported as a cost to their owners, separate from the energy-system (project) cost, which is now the headline (`energy_system_cost_bn`, `consumer_vehicle_cost_bn`, `saving_energy_system_pct` in every solution and Monte Carlo draw; the optimal system is unchanged because vehicle costs are fixed by the end-use mix). Farm charging infrastructure moves from the vehicle line to the project. Every figure is generated by the scripts and checked by `cn_layout_check.py`, which fails the build if any text lies on bars, lines, markers, outlines or other text (`cn_figure_layout_check.json`); the map labels sit in clear space or are joined to their place by leaders. Supplementary table S11 states the correct comparator (USD 400.2 bn).

Also in v1.6.2: an independent number audit (`cn_number_audit.py`, run by `run_all.sh`) that recomputes every unit conversion behind the headline numbers from typed-in reference values. It found three input errors, all corrected: the heavy-truck electric and fuel-cell ratios divided by a diesel energy per mile on a higher-heating-value basis while the model's diesel demand is on a lower-heating-value basis (now 0.44 and 0.81 instead of 0.41 and 0.76; this lowers the central saving by about 1.4 points); mineral phosphorus and potassium had been priced per tonne of P~2~O~5~ and of KCl product while the model's nutrient flows are elemental (now USD 2,600 per t P and 1,000 per t K), and the volumetric heating value used to price road and pipeline gas was 4% below the energy basis of the gas balance (now consistent at 37.5 million MMBtu per bcm). The LHV source label was also corrected. All results were re-run

## Reproduce

Every file sits in the folder root; there are no sub-folders. Scripts read and write in the folder they are in.

```
pip install -r requirements.txt
bash run_all.sh                     # full model, tests and figures (1,000 Monte Carlo draws per case, ~30 min on one core)
bash run_all.sh 100 --no-figures    # quick check
python3 cn_release_check.py         # compare with the submitted release (hashes, fresh re-solves, saved numbers)
python3 cn_number_audit.py          # independent recomputation of unit conversions and headline arithmetic
```

`cn_release_manifest.json` holds the SHA-256 of every code and input file and the headline numbers of the submitted release. After the full run, `run_all.sh` calls `cn_release_check.py`, which must print PASS. Release CN v1.6.4 was rebuilt this way from an empty folder holding only the code, `requirements.txt`, `CITATION.cff` and the two Grid Harvester drawings (29 min; console output in `cn_clean_rebuild_log.txt`), and every output matched v1.6.3 apart from the removed and renamed cases.

Seeds: 11 (least cost), 13 (230 GW offshore), 17 (after gas).

## Files

| File | Contents |
| --- | --- |
| `cn_inputs.py` | All assumptions, tagged [S] sourced / [A] assumption / [G] generic engineering value |
| `cn_model.py` | Transport LP, reactor learning and bounded hub search, reactor types, post-gas and closed-cycle cases, fuel and fissile accounting, regional supply, Monte Carlo, transition |
| `cn_gas.py` | China gas balance: domestic, pipeline and LNG supply, pyrolysis programme, heat pumps, biogas |
| `cn_regions.py` | Regional screen: five autonomous regions, Hong Kong, Macau, rest of mainland, Taiwan |
| `cn_crossfeed.py` | Seafood cross-feeding balance (fishmeal, shrimp meal, insect meal, Ulva, kelp, hemp meal) |
| `cn_breakeven.py` | Petroleum break-even multiples and shares of draws cheaper at each price |
| `cn_test.py` | Consistency and regression tests (including nutrient, soil-carbon, biomethane and bioextraction checks) |
| `cn_lull.py` | Wind-lull adequacy screen and sensitivities (tables S17–S18) |
| `cn_htse_heat.py`, `cn_htse_heat.json` | Steam-electrolysis temperature–enthalpy balance that sets the electrolyser heat inputs (table S16, fig. S7) |
| `CITATION.cff` | Citation metadata for the release |
| `cn_robustness.json` | Car ownership-cost derivation, stress cases, emissions-boundary sensitivities, carbon durability, build-rate screen, and nutrient, soil-carbon and bioextraction results |
| `cn_sm_tables.py`, `cn_sm_tables.md` | Supplementary tables generated from inputs and outputs |
| `cn_figures.py`, `cn_basemap.py` | Figures and schematic map (hand-digitised outline; not authoritative boundaries) |
| `cn_layout_check.py`, `cn_figure_layout_check.json` | Figure layout check: no text on bars, lines, markers, outlines or other text (run by `cn_figures.py`; the build fails otherwise) |
| `grid_harvester.py`, `grid_harvester_*.jpg` | Grid Harvester turning, energy and fleet-sizing screen (offshore and nearshore farms); drawings by the authors |
| `cn_release_check.py`, `cn_release_manifest.json` | Release check: file hashes, fresh re-solves and saved numbers against the submitted release |
| `run_all.sh`, `requirements.txt` | Runner and Python packages |
| `cn_*.json`, `cn_*.csv`, `*run_log*.txt` | Results of the reported run; `cn_manuscript_numbers.json` holds every number quoted in the manuscript |
| `cn_clean_rebuild_log.txt` | Console output of the v1.6.4 rebuild from an empty folder |
| `Fig*.png/.tif`, `FigS*.png/.tif` | Figures (PNG for the manuscript; RGB, 300-dpi LZW TIFF for submission) |
| `MANUSCRIPT_CN_V1.6.4.md` | Manuscript master with author details |
| `Manuscript_Anonymised_CleanEnergy_CN_V1.6.4.docx`, `Title_Page_CleanEnergy_CN_V1.6.4.docx`, `Supplementary_Materials_Anonymised_CN_V1.6.4.docx`, `Cover_Letter_CleanEnergy_CN_V1.6.4.docx` | Submission files for *Clean Energy* (double-anonymised manuscript and supplement, separate title page, cover letter) |
| `SUPPLEMENTARY_MATERIALS_CN_V1.6.4.md` | Supplementary materials |
| `CHANGELOG.md` | Version history |

## Limits

Annual energy balance: it shows annual resource adequacy, not operational feasibility; there is no hourly dispatch, reserve, transmission or stability analysis (build rates and one stylised wind-lull week are screened, not modelled); national optimisation with a regional reporting split; many segment splits are assumptions; biomass conversion at scale, offshore seaweed harvesting, advanced reactor costs and closed fuel cycles are not demonstrated; petroleum prices are historical snapshots. Fissile accounting is inventory-level only. The map is schematic.
