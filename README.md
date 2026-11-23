# China transport decarbonisation model — CN v1.6.2

Repository: https://github.com/bcjohnjr/China-Transportation-Decarbonization

Code and data for J. K. Bily, C. Pahl and P. Valdes Bacallao, *Electrification, reactor heat and regional biofuels for a petroleum-free transport system in the world's largest emitter: costs, conditions and limits* (prepared for submission to *Clean Energy*, Oxford University Press).

Contact: Jonathan Karl Bily, jonathan@cloudwashlaundry.com

The model asks whether all transport energy in mainland China (including the Guangxi, Inner Mongolia, Ningxia, Xizang/Tibet and Xinjiang autonomous regions), Hong Kong and Macau could be supplied without petroleum in 2050, at what annual cost, and what happens once natural gas is no longer used for hydrogen. Taiwan is modelled as a separate island system. It is the China counterpart of the United States model v8.4 and keeps its structure:

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

| Case | Cost | Oil | Saving | MC median (5–95%) | MC cheaper | Break-even | Hubs | CO~2~e |
|:------------------|---------:|-------------:|----------:|:---------------:|-----------:|------------:|--------:|-------------:|
| Least cost, gas era | 314.1 | 400.2 | 21.5% | 400 (273–558) | 54% | 0.78 | 221 | 130 |
| Gas era, 230 GW offshore wind with seaweed | 338.4 | 400.2 | 15.4% | 425 (304–585) | 44% | 0.85 | 227 | 124 |
| Gas era, 460 GW offshore wind with seaweed | 369.0 | 400.2 | 7.8% | — | — | 0.92 | 57 | 130 |
| Gas era, high reactor cost | 328.3 | 400.2 | 18.0% | — | — | 0.82 | 12 | 150 |
| Gas era, no nuclear | 367.5 | 400.2 | 8.2% | — | — | 0.92 | 0 | 106 |
| Gas era, thorium molten-salt hubs | 297.9 | 400.2 | 25.6% | — | — | 0.74 | 404 | 129 |
| After gas | 325.8 | 400.2 | 18.6% | 414 (285–585) | 49% | 0.81 | 268 | 99 |
| After gas, no nuclear | 372.9 | 400.2 | 6.8% | — | — | 0.93 | 0 | 101 |
| Closed thorium cycle (hypothetical) | 302.3 | 400.2 | 24.5% | — | — | 0.76 | 423 | 100 |
| Closed thorium cycle, cost premium | 328.2 | 400.2 | 18.0% | — | — | 0.82 | 421 | 99 |
| Taiwan island system | 17.9 | 15.6 | -14.3% | — | — | 1.14 | 7 | 8 |
| Taiwan island system, no nuclear | 20.5 | 15.6 | -31.4% | — | — | 1.31 | 0 | 8 |

- Least cost saves **21.5%** against late-2025 pre-tax petroleum (break-even at 0.78 × late-2025 prices), close to the 23.2% of the U.S. v8.4 headline. **The result is conditional:** with no ownership-cost advantage for battery-electric cars the saving is 12.2%, at +100 USD/car/yr it is 2.3%, without carbon-product revenue 14.9%, and a moderate combination of adverse assumptions costs 15% more than late-2025 petroleum (Table 2 of the manuscript; `cn_robustness.json`). November 2026 prices are 1.37 × late-2025.
- **U.S. cross-check:** v8.4's heavy-truck ratios (`r_hdv_elec = 2.40/21.1`, `r_hdv_fcev = 4.44/21.1`) divide kWh/mi by MJ/mi. Corrected (× 3.6), the U.S. least-cost saving falls from 23.2% to **12.0%** and the post-gas saving from 16.4% to 4.7% (`cn_us_crosscheck.py`, `us_truck_ratio_crosscheck.json`). All CN versions use the corrected ratios; with the uncorrected ratios the China saving would be 37.2%.
- **Nutrients and soil carbon:** harvesting removes 2.93 Mt N, 0.62 Mt P and 4.98 Mt K a year; process streams return 53%, 94% and 91% and mineral fertiliser the rest. 27.4 Mt C/yr of stable soil carbon is replaced by hydrochar (14.8), digestate (5.5) and pyrolysis carbon (7.1). The balance costs USD 5.1 bn/yr. Nearshore farms on 3,600 km² would remove 184 kt N and 25 kt P a year for USD 0.1 bn/yr more.
- Emissions fall from 2,074 to 130 Mt CO2e/yr (93.7%) in the gas era and to 99 Mt after gas. China emitted about 32% of world fossil CO2 in 2025.
- Pyrolysis needs 48 bcm/yr of gas (11% of 2025 consumption); first gas shortfall 2141 (range 2100–2175); import share peaks at 37%.
- A closed thorium molten-salt fleet (423 hubs) costs USD 302.3 bn but needs ~380 t of start-up fissile material; China's military plutonium (IPFM 2.9 ± 0.6 t) would start ~0.3 GWe of fast reactors.
- All five autonomous regions produce more renewable liquids than they use; Hong Kong, Macau and Taiwan depend on outside supply; Taiwan's island system costs 14% more than petroleum.
- Conditional Monte Carlo (1,000 independent draws from assumed ranges): least cost cheaper than late-2025 petroleum in 54% of draws, median saving 3.3%. This is a sensitivity result, not a probability.
- Build-rate screen: 1,326 modules of 250 MWt, about 70 a year from 2032; with at most 30 hubs the saving is still 18.9%. Wider life-cycle boundaries raise residual emissions from 130 to as much as 334 Mt.

## Updating the GitHub repository to v1.6.2

The public repository must hold exactly this release before the manuscript is submitted; reviewers and editors will follow the link on the title page.

1. Upload every file in this flat folder to the repository root, replacing files with the same names. No folders are needed.
2. Delete every older versioned document still in the repository: `MANUSCRIPT_CN_V1.*.md`, `SUPPLEMENTARY_MATERIALS_CN_V1.*.md` and `*_CN_V1.*.docx` for V1.3, V1.4, V1.4.1, V1.5 and V1.6. Only the V1.6.2 files should remain.
3. Check that `README.md`, `CHANGELOG.md` and `CITATION.cff` on GitHub show CN v1.6.2, and that `cn_release_manifest.json` is present.
4. Create a release with tag `CN-v1.6.2`.
5. Archive the release with a DOI: connect the repository to Zenodo (zenodo.org, sign in with GitHub, switch the repository on), then publish the GitHub release; Zenodo mints the DOI. Add the DOI to `CITATION.cff` and the title page.
6. After submission, do not overwrite the release; record any later change as a new tagged version.

New in v1.6.2: an independent number audit (`cn_number_audit.py`, run by `run_all.sh`) that recomputes every unit conversion behind the headline numbers from typed-in reference values. It found three input errors, all corrected: the heavy-truck electric and fuel-cell ratios divided by a diesel energy per mile on a higher-heating-value basis while the model's diesel demand is on a lower-heating-value basis (now 0.44 and 0.81 instead of 0.41 and 0.76; this lowers the central saving by about 1.4 points); mineral phosphorus and potassium had been priced per tonne of P~2~O~5~ and of KCl product while the model's nutrient flows are elemental (now USD 2,600 per t P and 1,000 per t K), and the volumetric heating value used to price road and pipeline gas was 4% below the energy basis of the gas balance (now consistent at 37.5 million MMBtu per bcm). The LHV source label was also corrected. All results were re-run.

## Reproduce

Every file sits in the folder root; there are no sub-folders. Scripts read and write in the folder they are in.

```
pip install -r requirements.txt
bash run_all.sh                     # full model, tests and figures (1,000 Monte Carlo draws per case, ~25 min)
bash run_all.sh 100 --no-figures    # quick check
python3 cn_release_check.py         # compare with the submitted release (hashes, fresh re-solves, saved numbers)
python3 cn_number_audit.py          # independent recomputation of unit conversions and headline arithmetic
```

`cn_release_manifest.json` holds the SHA-256 of every code and input file and the headline numbers of the submitted release. After the full run, `run_all.sh` calls `cn_release_check.py`, which must print PASS. The release was rebuilt this way from an empty folder before submission.

Seeds: 11 (least cost), 13 (230 GW offshore), 17 (after gas). `cn_us_crosscheck.py` runs the unmodified U.S. v8.4 files included here (`us2_model.py`, `us2_inputs.py`, `grid_harvester.py`) after checking their SHA-256 hashes.

## Files

| File | Contents |
| --- | --- |
| `cn_inputs.py` | All assumptions, tagged [S] sourced / [A] assumption / [U] from the U.S. model |
| `cn_model.py` | Transport LP, reactor learning and bounded hub search, reactor types, post-gas and closed-cycle cases, fuel and fissile accounting, regional supply, Monte Carlo, transition |
| `cn_gas.py` | China gas balance: domestic, pipeline and LNG supply, pyrolysis programme, heat pumps, biogas |
| `cn_regions.py` | Regional screen: five autonomous regions, Hong Kong, Macau, rest of mainland, Taiwan |
| `cn_crossfeed.py` | Seafood cross-feeding balance (fishmeal, shrimp meal, insect meal, Ulva, kelp, hemp meal) |
| `cn_breakeven.py` | Petroleum break-even multiples and shares of draws cheaper at each price |
| `cn_us_crosscheck.py`, `us_truck_ratio_crosscheck.json` | U.S. v8.4 heavy-truck ratio cross-check (checks SHA-256 of the U.S. files) |
| `us2_model.py`, `us2_inputs.py` | Unmodified U.S. model v8.4 source, used only by the cross-check |
| `cn_test.py` | Consistency and regression tests (including nutrient, soil-carbon, biomethane and bioextraction checks) |
| `cn_lull.py` | Wind-lull adequacy screen and sensitivities (tables S17–S18) |
| `cn_htse_heat.py`, `cn_htse_heat.json` | Steam-electrolysis temperature–enthalpy balance that sets the electrolyser heat inputs (table S16, fig. S7) |
| `CITATION.cff` | Citation metadata for the release |
| `cn_robustness.json` | Car ownership-cost derivation, stress cases, emissions-boundary sensitivities, carbon durability, build-rate screen, and nutrient, soil-carbon and bioextraction results |
| `cn_sm_tables.py`, `cn_sm_tables.md` | Supplementary tables generated from inputs and outputs |
| `cn_figures.py`, `cn_basemap.py` | Figures and schematic map (hand-digitised outline; not authoritative boundaries) |
| `grid_harvester.py`, `grid_harvester_*.jpg` | Grid Harvester turning, energy and fleet-sizing screen (offshore and nearshore farms); drawings by the authors |
| `cn_release_check.py`, `cn_release_manifest.json` | Release check: file hashes, fresh re-solves and saved numbers against the submitted release |
| `run_all.sh`, `requirements.txt` | Runner and Python packages |
| `cn_*.json`, `cn_*.csv`, `*run_log*.txt` | Results of the reported run; `cn_manuscript_numbers.json` holds every number quoted in the manuscript |
| `Fig*.png/.tif`, `FigS*.png/.tif` | Figures (PNG for the manuscript, 300-dpi TIFF for submission) |
| `MANUSCRIPT_CN_V1.6.2.md` | Manuscript master with author details |
| `Manuscript_Anonymised_CleanEnergy_CN_V1.6.2.docx`, `Title_Page_CleanEnergy_CN_V1.6.2.docx`, `Supplementary_Materials_Anonymised_CN_V1.6.2.docx`, `Cover_Letter_CleanEnergy_CN_V1.6.2.docx` | Submission files for *Clean Energy* (double-anonymised manuscript and supplement, separate title page, cover letter) |
| `SUPPLEMENTARY_MATERIALS_CN_V1.6.2.md` | Supplementary materials |
| `CHANGELOG.md` | Differences from the U.S. model and version history |

## Limits

Annual energy balance: it shows annual resource adequacy, not operational feasibility; there is no hourly dispatch, reserve, transmission or stability analysis (build rates and one stylised wind-lull week are screened, not modelled); national optimisation with a regional reporting split; many segment splits are assumptions; biomass conversion at scale, offshore seaweed harvesting, advanced reactor costs and closed fuel cycles are not demonstrated; petroleum prices are historical snapshots. Fissile accounting is inventory-level only. The map is schematic.
