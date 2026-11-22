# China transport decarbonisation model — CN v1.3

Code and data for J. K. Bily, C. Pahl and P. Valdes Bacallao, *Electrification, reactor heat and regional biofuels for a petroleum-free transport system in the world's largest emitter: costs, conditions and limits* (prepared for submission to *Clean Energy*, Oxford University Press).

Contact: Jonathan Karl Bily, jonathan@cloudwashlaundry.com

The model asks whether all transport energy in mainland China (including the Guangxi, Inner Mongolia, Ningxia, Xizang/Tibet and Xinjiang autonomous regions), Hong Kong and Macau could be supplied without petroleum in 2050, at what annual cost, and what happens once natural gas is no longer used for hydrogen. Taiwan is modelled as a separate island system. It is the China counterpart of the United States model v8.4 and keeps its structure:

- **Reactor hubs.** Six-module HTR-PM-class hubs run a heat cascade: steam electrolysis and methane pyrolysis (steam electrolysis only after gas), electricity, biocrude upgrading, drying, then greenhouses and fish farms. Thorium molten-salt, sodium fast, 950°C and light-water SMR alternatives are tested.
- **Electricity.** Onshore wind (two cost tiers), solar, concentrated solar with storage, light-water reactors, offshore wind.
- **Land biomass.** Crop straw by region, forestry and bamboo residues, new bamboo and hemp, and the autonomous regions' crops: Guangxi cassava, molasses, bagasse and jatropha; sweet sorghum in Inner Mongolia, Xinjiang and Ningxia; Jerusalem artichoke; cotton stalks; Ningxia sweet potato; Xizang grassland and forestry residues.
- **Electric expressways** on 60,000 km of freight corridors, plus battery-electric vehicles and machines.
- **Optional offshore wind with seaweed** from Liaoning to Hainan and the Taiwan Strait, harvested by Grid Harvesters.
- **Pyrolysis carbon** sold to capped markets; **food** from reactor heat with **seafood cross-feeding** (reported outside the transport cost; heat sold to food earns nothing in the transport boundary).

## Main results (2050, 2026 US$ per year, pre-tax, transport-only)

| Case | Cost | Oil | Saving | MC median (5–95%) | MC cheaper | Break-even | Hubs | CO~2~e |
|:------------------|---------:|-------------:|----------:|:---------------:|-----------:|------------:|--------:|-------------:|
| Least cost, gas era | 303.4 | 399.3 | 24.0% | 382 (256–543) | 65% | 0.76 | 239 | 109 |
| Gas era, 230 GW offshore wind with seaweed | 327.5 | 399.3 | 18.0% | 413 (291–575) | 48% | 0.82 | 239 | 108 |
| Gas era, 460 GW offshore wind with seaweed | 357.7 | 399.3 | 10.4% | — | — | 0.90 | 52 | 120 |
| Gas era, high reactor cost | 317.4 | 399.3 | 20.5% | — | — | 0.79 | 12 | 134 |
| Gas era, no nuclear | 354.3 | 399.3 | 11.3% | — | — | 0.89 | 0 | 96 |
| Gas era, thorium molten-salt hubs | 286.9 | 399.3 | 28.2% | — | — | 0.72 | 405 | 109 |
| After gas, steam electrolysis | 329.7 | 399.3 | 17.4% | 412 (279–572) | 51% | 0.83 | 283 | 90 |
| After gas, no nuclear | 359.5 | 399.3 | 10.0% | — | — | 0.90 | 0 | 91 |
| Closed thorium cycle (hypothetical) | 306.0 | 399.3 | 23.4% | — | — | 0.77 | 424 | 90 |
| Closed thorium cycle, cost premium | 332.1 | 399.3 | 16.8% | — | — | 0.83 | 424 | 90 |
| Taiwan island system | 17.7 | 15.6 | -13.2% | — | — | 1.13 | 7 | 8 |
| Taiwan island system, no nuclear | 20.3 | 15.6 | -29.9% | — | — | 1.30 | 0 | 8 |

- Least cost saves **24.0%** against late-2025 pre-tax petroleum (break-even at 0.76 × late-2025 prices), matching the 23.2% of the U.S. v8.4 headline. **The result is conditional:** with no ownership-cost advantage for battery-electric cars the saving is 14.7%, at +100 USD/car/yr it is 4.7%, without carbon-product revenue 17.4%, and a moderate combination of adverse assumptions costs 12% more than late-2025 petroleum (Table 2 of the manuscript; `cn_robustness.json`). November 2026 prices are 1.37 × late-2025.
- **U.S. cross-check:** v8.4's heavy-truck ratios (`r_hdv_elec = 2.40/21.1`, `r_hdv_fcev = 4.44/21.1`) divide kWh/mi by MJ/mi. Corrected (× 3.6), the U.S. least-cost saving falls from 23.2% to **12.0%** and the post-gas saving from 16.4% to 4.7% (`cn_us_crosscheck.py`, `us_truck_ratio_crosscheck.json`). CN v1.0 and v1.1 use the corrected ratios; with the uncorrected ratios the China saving would be 38.3%.
- Emissions fall from 2,074 to 109 Mt CO2e/yr (94.8%) in the gas era and to 90 Mt after gas. China emitted about 32% of world fossil CO2 in 2025.
- Pyrolysis needs 33 bcm/yr of gas (8% of 2025 consumption); first gas shortfall 2141 (range 2101–2175); import share peaks at 37%.
- A closed thorium molten-salt fleet (424 hubs) costs USD 306.0 bn but needs ~380 t of start-up fissile material; China's military plutonium (IPFM 2.9 ± 0.6 t) would start ~0.3 GWe of fast reactors.
- All five autonomous regions produce more renewable liquids than they use; Hong Kong, Macau and Taiwan depend on outside supply; Taiwan's island system costs 13% more than petroleum.
- Conditional Monte Carlo (1,000 independent draws from assumed ranges): least cost cheaper than late-2025 petroleum in 65% of draws, median saving 8%. This is a sensitivity result, not a probability.
- Build-rate screen: 1,434 modules of 250 MWt, about 75 a year from 2032; with at most 30 hubs the saving is still 21.5%. Wider life-cycle boundaries raise residual emissions from 109 to as much as 309 Mt.

## Reproduce

Every file sits in the folder root; there are no sub-folders. Scripts read and write in the folder they are in.

```
pip install -r requirements.txt
bash run_all.sh                     # full model, tests and figures (1,000 Monte Carlo draws per case, ~25 min)
bash run_all.sh 100 --no-figures    # quick check
```

Seeds: 11 (least cost), 13 (230 GW offshore), 17 (after gas). `cn_us_crosscheck.py` needs the U.S. v8.4 files (`us2_model.py`, `us2_inputs.py`) in the same folder; without them it prints the stored result.

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
| `cn_test.py` | Consistency and regression tests |
| `cn_htse_heat.py`, `cn_htse_heat.json` | Steam-electrolysis temperature–enthalpy balance that sets the electrolyser heat inputs (table S16, fig. S7) |
| `CITATION.cff` | Citation metadata for the release |
| `cn_robustness.json` | Car ownership-cost derivation, stress cases, emissions-boundary sensitivities, carbon durability and build-rate screen |
| `cn_sm_tables.py`, `cn_sm_tables.md` | Supplementary tables generated from inputs and outputs |
| `cn_figures.py`, `cn_basemap.py` | Figures and schematic map (hand-digitised outline; not authoritative boundaries) |
| `grid_harvester.py`, `grid_harvester_*.jpg` | Grid Harvester screen (from the U.S. model) |
| `run_all.sh`, `requirements.txt` | Runner and Python packages |
| `cn_*.json`, `cn_*.csv`, `*run_log*.txt` | Results of the published run; `cn_manuscript_numbers.json` holds every number quoted in the manuscript |
| `Fig*.png/.tif`, `FigS*.png/.tif` | Figures (PNG for the manuscript, 300-dpi TIFF for submission) |
| `MANUSCRIPT_CN_V1.3.md` | Manuscript master with author details |
| `Manuscript_Anonymised_CleanEnergy_CN_V1.3.docx`, `Title_Page_CleanEnergy_CN_V1.3.docx`, `Supplementary_Materials_Anonymised_CN_V1.3.docx`, `Cover_Letter_CleanEnergy_CN_V1.3.docx` | Submission files for *Clean Energy* (double-anonymised manuscript and supplement, separate title page, cover letter) |
| `SUPPLEMENTARY_MATERIALS_CN_V1.3.md` | Supplementary materials |
| `CHANGELOG.md` | Differences from the U.S. model and version history |

## Limits

Annual energy balance: it shows annual resource adequacy, not operational feasibility; there is no hourly dispatch, reserve, transmission or stability analysis (build rates and one stylised wind-lull week are screened, not modelled); national optimisation with a regional reporting split; many segment splits are assumptions; biomass conversion at scale, offshore seaweed harvesting, advanced reactor costs and closed fuel cycles are not demonstrated; petroleum prices are historical snapshots. Fissile accounting is inventory-level only. The map is schematic.
