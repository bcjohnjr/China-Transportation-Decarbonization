---
title: "Supplementary materials for: Electrification, reactor heat and regional biofuels for a petroleum-free transport system in the world's largest emitter: costs, conditions and limits"
---

Model version CN v1.3 (22 November 2026). All tables in this document are generated from the model inputs and outputs by `cn_sm_tables.py`; numbers in the text are read from `cn_manuscript_numbers.json`.

**Contents.** Supplementary text S1 to S18; figures S1 to S7; tables S1 to S17.

# Supplementary text

## S1. Scope, study area and system boundary

The model represents one annual energy balance for 2050 for mainland China, including the Guangxi Zhuang, Inner Mongolia, Ningxia Hui, Xizang (Tibet) and Xinjiang Uyghur autonomous regions, and the Hong Kong and Macau Special Administrative Regions. Hong Kong imports electricity from the Daya Bay nuclear plant and Guangdong, and Macau imports most of its electricity from Guangdong; both draw refined fuels from regional refineries, so they are modelled inside the mainland system. Taiwan has a separate grid, refineries and fuel market and is modelled as an island system with its own demand, resources and costs (S14). Transport scope matches the United States model v8.4: road (cars, two- and three-wheelers within gasoline demand, trucks and buses including LNG and CNG vehicles), aviation including international departures, rail, domestic shipping and fishing vessels, bonded international bunkers, farm machinery, construction and mining machinery, industrial trucks and pipeline compression. Costs are annualised 2050 costs in 2026 US dollars at a 5% real discount rate, pre-tax, and transport-only: food, nutrient and livestock outcomes are reported separately and not credited. Unlike the United States model, low-grade heat sold to food uses earns nothing inside the transport boundary (CN v1.2); its gross value at USD 8 per MWh is reported separately, and a sensitivity case restores the credit.

## S2. Baseline demand and 2050 technology shares

Table S1 lists the 2025 baseline. China's 2025 consumption of gasoline (155 Mt), diesel (203 Mt) and kerosene and jet fuel (40.21 Mt) follows the China Association of Petroleum Enterprises' 2025 review, reported by SunSirs; transport natural gas (42.6 bcm) is derived from ICIS's 2026 estimate of 44.14 bcm and its 3.5% growth. The split of diesel between segments is an assumption: on-road 120 Mt, rail 3.5 Mt, marine 12 Mt, farm 25 Mt, construction and mining 25 Mt, industrial trucks 3 Mt and non-transport uses 14.5 Mt (excluded). Hong Kong jet fuel (5.6 Mt) is consistent with imports of 3.4 million kilolitres in the first half of 2024; Hong Kong gasoline, diesel and bunkers and all Macau quantities are assumptions. Taiwan uses EIA 2024 consumption (gasoline 188 kb/d, diesel 116 kb/d with 60% assumed on-road, jet 68.8 kb/d). Energy contents are IPCC default net calorific values (gasoline 12.06, diesel 11.89, jet 12.00, fuel oil 11.22 kWh/kg; gas 9.9 kWh/m^3^). Service demand in 2050 is 1.15 times 2025 in the central case.

Technology shares (table S2) reflect China's trajectory: new-energy vehicles were 49% of 2025 car registrations and zero-emission vehicles 25% of medium and heavy truck sales. Heavy-truck drivetrain ratios use 2.40 kWh per mile (battery-electric tractor) and 21.1 MJ per mile (diesel tractor at about 6.9 mpg, 144.9 MJ per gallon), giving 2.40 × 3.6 / 21.1 = 0.41 kWh of electricity per kWh of displaced diesel; for fuel-cell trucks 4.44 kWh of hydrogen per mile gives 0.76. The United States model v8.4 divided the same numbers without the factor 3.6 (S15).

Table S2b derives the net annual ownership cost of a battery-electric car relative to a comparable petrol car in 2050, excluding energy. The purchase-price difference is annualised over 12 years at the 5% discount rate. Expected battery replacement assumes a 55 kWh pack replaced at year 9 with the stated probability. Maintenance and repair for a petrol car is taken as USD 350 per year and the electric saving as 15 to 45%. The insurance penalty ranges from USD 40 to 300 per year; the 2025 average new-energy car premium was about USD 610, with like-for-like premiums about 20% above petrol cars. The central value of -93 USD per year replaces the v1.0 assumption of -100 USD; the low and high values set the Monte Carlo triangle. The car stock (420 million in 2050) is tested at 350 and 500 million.

## S3. Decision variables, objective and constraints

Decision variables (all non-negative): onshore wind in two cost tiers, solar, concentrated solar, light-water reactors, offshore wind by zone, surplus electricity exported to the wider grid, imported renewable liquids (Taiwan only), number of reactor hubs, top-tier heat to the turbine, hydrogen from pyrolysis, alkaline electrolysis, steam electrolysis and sulfur–iodine, ten residue tiers, new bamboo, hemp area, liquefaction and gasification–synthesis throughput, cellulosic ethanol, eight starch and sugar ethanol feedstocks, alcohol-to-jet, direct ethanol, four oil feedstocks and hemp oil to hydroprocessing, electric heat and drying, heat sold to food uses, optional heat-exchanger transfers between tiers, seaweed to liquefaction or gasification by zone, and carbon sold to eight markets. The objective is

$$\min C = \sum_i c_i x_i + F,$$

with $F$ the costs fixed by the end-use mix (grids, charging, electric expressways, rail electrification, vehicles and machines, hydrogen delivery to vehicles, residual pipeline gas). Constraints: electricity supply ≥ transport demand plus process loads; solar ≤ 40% of supply; firm supply (light-water reactors, concentrated solar with storage and hub electricity) ≥ 15% of transport electricity; top-tier, process-steam and drying heat used ≤ heat available from hubs (plus electric heat); hydrogen made ≥ hydrogen used; liquids ≥ liquid demand; jet-range liquids ≥ jet demand; ethanol made = ethanol used; residue pool used = residues + bamboo + hemp stalks + sorghum bagasse; seaweed tied to the wind area of each zone; heat sold ≤ hub low-grade heat and ≤ the food market; carbon sold = carbon made. A reconciliation check confirms that the reported cost equals the LP objective plus fixed terms to 10^-6^ billion dollars in every case.

## S4. Power and reactor parameters

Table S3 gives power and hydrogen parameters, table S4a reactor cost cases. The hub has six 250 MWt modules (1,500 MWt), 93% capacity factor, 60-year life, USD 30 per kWt-year fixed operation and USD 9 per MWh of heat fuel. Heat tiers: 30% at the top tier (750°C helium for methane preheat), 7.5% as process steam (biocrude upgrading and steam raising for electrolysis) and 10% for drying, each withdrawn with a turbine penalty (0.30 and 0.15 MWh of electricity per MWh), the rest to a 40%-efficient turbine, 35% of whose rejected heat is usable at 35–70°C. Fleet cost follows Wright's law per module. Because the cost curve makes total cost non-convex in hub count, the published cases are solved at every integer number of hubs from 0 to 1,500 at the matching fleet-average cost; none of the optima lies at the bound. Monte Carlo draws use every 25th hub count, refined to single hubs around the best. The central fleet-average cost, including interest during construction, is USD 2,788 per kWe for the least-cost fleet of 1,434 modules (fig. S4).

## S5. Reactor technology alternatives

Table S4b lists the five hub technologies and their 2050 transport costs. The HTR-PM is in commercial operation at Shidaowan (two 250 MWt modules, 210 MWe) [S1]. TMSR-LF1 is a 2 MWt experimental thorium molten-salt reactor at Wuwei, Gansu, which loaded thorium in October 2024 and reported thorium-to-uranium conversion in November 2025 with a conversion ratio of about 0.1 [S2]. The CFR-600 sodium-cooled fast reactor at Xiapu, Fujian, began low-power operation in 2023 with highly enriched uranium fuel [S3]. The ACP100 (Linglong One) light-water SMR at Changjiang, Hainan, completed its non-nuclear turbine test in December 2025 [S4]. The 950°C reactor is a future concept. Outlet temperature sets the methane preheat the reactor can supply, $q = c_p (T - 75) m_{\mathrm{CH_4}} / 3600$ kWh per kg H~2~ with $c_p$ = 3.3 kJ/kg·K and 4.08 kg of methane per kg of hydrogen, capped at the full 8.3 kWh per kg; the balance is supplied by electric heaters at 95% efficiency. Efficiencies, cost multipliers and fuel costs are assumptions and are the main reason for the ranking.

## S6. Land biomass and regional crops

Tables S5 and S6 give the residue tiers, the autonomous-region crops, oil feedstocks, bamboo and hemp limits and their use in the least-cost case. Straw caps reflect China's ~860 Mt annual straw production and agronomic removal limits of 45% for rice, 19% for wheat and 42% for maize [S5], net of feed, mushroom substrate and existing uses. These limits are intended to protect soil organic carbon and limit erosion, and removed nutrients are replaced by purchased fertiliser at cost. The model does not represent the loss of soil carbon that removal can still cause, nor effects on soil structure, moisture and erosion beyond the removal limit, nor collection radii, which enter only through the tier prices. Residue supply is therefore tested at 75% and 50% of the caps (table S15), and soil-carbon losses of 20 and 40 g CO~2~e per MJ of residue-derived fuel are added as a boundary sensitivity (table S12). Guangxi: cassava ethanol (Guangxi grows more than 60% of China's cassava), molasses from about 6.4 Mt of cane sugar per season, surplus bagasse and cassava residues, jatropha on hill slopes (40% of jatropha oil assigned to Guangxi, the rest to Yunnan, Sichuan and Guizhou) and clumping bamboo. Inner Mongolia: maize stover and crop stalks, sweet sorghum on saline–alkaline land (4,500 L of ethanol and 8 t of bagasse per hectare), Jerusalem artichoke on sandy land and hemp in the east. Xinjiang: cotton stalks, drip-irrigated sweet sorghum and cottonseed and non-edible oilseed residues. Ningxia: Loess Plateau crop residues, sweet sorghum and sweet potato. Xizang: alpine grassland and forestry residues only (1.5 Mt at USD 75 per tonne), reflecting its short growing season; yak-dung biogas is counted in the gas balance. Conversion routes, yields and hydrogen needs are those of the United States model; Chinese capital costs are lower (liquefaction USD 130 per tonne, gasification–synthesis USD 230 per tonne).

## S7. Offshore wind, seaweed and the Grid Harvester

Table S7 gives the nine zones. Yields at three levels (demonstrated, design, learning) are per hectare of farmed area between turbines, which is a fraction of the wind-farm area. Chinese nearshore kelp farms reach far higher yields per hectare of farm, but offshore yields between turbines are not demonstrated. Logistics use the U.S. model's Grid Harvester (fig. S6), battery and wing-sail haul vessels and inspection drones with Chinese capital costs. Seaweed fuel costs USD 180–260 per MWh of liquid (table S7; fig. S1). Seaweed also yields recoverable nitrogen, phosphorus and potassium credited at Chinese fertiliser prices.

## S8. Carbon markets, emissions and petroleum comparator

Pyrolysis carbon (3 kg per kg of hydrogen) is sold in eight capped markets: vehicle structures and hydrogen tanks (1.5 Mt at USD 3,500 per tonne), battery anode graphite (4 Mt at USD 2,500), carbon black (7 Mt at USD 800), specialty carbon, metallurgical carbon, construction additives, soil amendment and permanent storage (USD –20 per tonne). Emission intensities follow the U.S. model: petroleum well-to-wheel 89–96 g CO~2~e/MJ, gas 70 g/MJ, liquids by route 6–40 g/MJ, electricity 10 g/kWh life-cycle, pyrolysis hydrogen with 1.5% upstream leakage and 2% hydrogen leakage at a hydrogen GWP of 11.6. Table S8 gives the pre-tax prices. Retail gasoline and diesel caps are converted by dividing by 1.13 (value-added tax) and subtracting the consumption tax (1.52 yuan/L gasoline, 1.20 yuan/L diesel) at exchange rates of 7.08 yuan per dollar (25 November 2025) and 6.71 (18 November 2026). Jet fuel is priced ex-refinery net of value-added tax; bunker fuel at Singapore-type VLSFO prices; road gas at USD 11 and 14 per MMBtu. The petroleum comparator applies the same service growth as the system.

The carbon values assume that pyrolysis carbon can be purified, graphitised or otherwise qualified for each market; purification, graphitisation, quality control and certification costs are included only through the assumed net values. The stress cases remove that revenue (all carbon to paid permanent storage) or keep only the commodity markets (carbon black, metallurgy, construction, soil, storage). Table S13 shows where the carbon goes and how long it would stay out of the atmosphere: none of the least-cost carbon goes to long-term storage, and none is counted as an emission reduction. Table S12 recomputes least-cost emissions with wider life-cycle boundaries; these parameters do not enter the cost, so the solution is not re-optimised.

Steam electrolysis heat (CN v1.3). `cn_htse_heat.py` computes a temperature–enthalpy balance per kg of hydrogen (table S16, fig. S7). Feed water at 20°C is preheated, evaporated at 0.5 MPa (152°C) and superheated to the 800°C stack inlet; 11.2 kg of steam is fed for 80% utilisation. The cathode (hydrogen and unconverted steam) and anode (oxygen, no sweep gas) streams leave at 800°C. A counterflow high-temperature recuperator superheats the steam to 775°C (25 K minimum approach, checked along the exchanger), cooling the hot streams to 274°C; their remaining sensible heat preheats feed water to 127°C, and condensation of 90% of the unconverted steam below its 100°C dew point preheats feed water to 75°C. The external heat is then 6.87 kWh per kg, all needed at or below 152°C, close to the 6.4 kWh per kg of the Idaho National Laboratory reference design; without the low-temperature recovery it would be 8.26 kWh per kg. Electric topping is 0.68 kWh per kg: 0.18 kWh for the final 25 K and 0.50 kWh of stack and hot-box heat loss (1.5% of stack electricity). Gas enthalpies use NIST Shomate equations (ideal gas) and water properties steam-table values at 0.5 MPa. The recuperator needs 1.1 m² per kg per hour of hydrogen capacity (overall coefficient 60 W/m²K, mean temperature difference 61 K), which at USD 3,000 per m² installed adds USD 0.03 per kg to the capital charge. Because the high-temperature duty is met by recuperation, the reactor (or boiler) only has to raise steam, which the HTR-PM's process steam can do with a large margin; the same topping applies with and without reactor steam. Sensitivity cases with 3 kWh per kg of topping and with no low-temperature recovery are in table S15. This is a flowsheet-level balance; stack degradation, pressure drop, start-up heating and part-load operation are not modelled.

## S9. Natural-gas supply

`cn_gas.py` balances China's gas demand year by year (table S9). Domestic remaining technically recoverable resources are 40 tcm conventional and tight, 25 tcm shale and 11 tcm coalbed methane, less 3.2 tcm already produced, times a recovery factor (central 0.6). Domestic production capacity grows 3% a year from 261.9 bcm to a 360 bcm plateau, subject to a 15-year reserves-to-production floor. Pipeline imports rise from 81 bcm (2025) to 114 bcm (2030) and 150 bcm (2035), drawn from a 20 tcm pool of exporter gas with the same floor. Liquefied natural gas imports are capped at 140 bcm. Non-transport demand grows 1.5% a year to 2040; road gas and compressor gas phase down with electrification; the pyrolysis programme ramps from 2030 to 33 bcm in 2050. Heat pumps replace 90% of space and water heating gas by 2050 (COP 3), and biomethane reaches 30 bcm (central) or 80 bcm (high) by 2045. First shortfall: 2141 (central), 2144 without the programme, and 2101–2175 across sensitivities; peak import share 37%. The 81-case grid over recovery, LNG ceiling and pipeline pool is in `cn_gas_depletion.json`.

## S10. After gas, closed fuel cycles and fissile accounting

After gas, pyrolysis is unavailable, pipeline compressors are fully electric and vehicle-structure carbon is unavailable; hydrogen comes from steam electrolysis at 36.8 kWh~e~ and 6.4 kWh~th~ per kg (or sulfur–iodine for 950°C reactors). The closed-cycle cases assume breeding thorium molten-salt or sodium fast hubs that fission 0.95 MWd per gram of heavy metal with 2% recycling loss. Fuel accounting is at inventory level only: once-through HTR-PM fuel at 8.5% enrichment and 90 GWd/t; closed-cycle heavy metal per year; start-up fissile inventory of 10 t plutonium per GWe for fast reactors and 1.5 t fissile per GWe for thermal molten-salt reactors (assumptions). Pools: plutonium in China's spent fuel (about 11,000 tHM discharged by end-2024 and a projected 111,290 tHM by 2050 at about 1% plutonium [S6, S7]) and the IPFM estimate of military plutonium (2.9 ± 0.6 t) [S8]. These pools are not separated or qualified fuel, and no fuel-cycle process is modelled. For the closed thorium fleet: 254 GWe, 232 t of heavy metal a year, 380 t of start-up fissile material (about 82,000 t of natural uranium if supplied as 19.75% enriched uranium), and about 430 years of China's identified thorium (100,000 t) at the annual rate.

## S11. Regional screen

`cn_regions.py` splits mainland demand, emissions and costs with fixed regional shares (road, air, farm and mining shares in `cn_inputs.REGIONS`, from 2024 GDP, sown area, mining and airport traffic) and assigns least-cost feedstock use to regions by the location of each resource. Regional renewable potentials are order-of-magnitude values for comparison only. This is a reporting split, not a regional optimisation; transmission and inter-regional fuel trade are implied, not costed.

## S12. Heat cascade, food and cross-feeding

Low-grade heat first heats Asparagopsis tanks, then greenhouses (220 kWh per m^2^, 40 kg per m^2^, market up to 30 Mt of vegetables), then recirculating fish and shrimp farms (4 kWh per kg, market up to 5 Mt, 40% shrimp). Drying heat dries 0.5 Mt of food seaweed and up to 80 Mt of grain near hubs. `cn_crossfeed.py` balances feed flows with the coefficients in the script: fish and shrimp feed conversion ratios of 1.4 and 1.3; fishmeal inclusion of 10% and 20%; processing by-products of 45% (fish) and 40% (shrimp) yielding 21% fishmeal and 25% shrimp meal; insect meal at 3% of wet greenhouse waste (15% of output); hemp meal up to 12% and Ulva up to 5% of fish feed; 30% nitrogen retention, 50% of the remainder dissolved and 60% recovered by Ulva at 3.5% nitrogen; abalone eating 2.4 kg and sea cucumber 1.5 kg of dry algae per kg of growth, with 0.3 Mt of each and 0.3 Mt of feed kelp from the existing industry. Results: 51% of marine protein and 23% of feed protein met internally; 78 kt nitrogen recovered.

## S13. Conditional Monte Carlo, sensitivity and stress tests

Table S10 lists the 30 uncertain parameters. Each case uses 1,000 draws with fixed seeds (11 least cost, 13 offshore, 17 after gas). Spearman rank correlations with least-cost system cost are shown in fig. S3. Break-even multiples and the share of draws cheaper than petroleum at multiples 0.5–2.0 are in `cn_breakeven.json` and `cn_breakeven.csv`. Parameters are drawn independently, so the share of draws cheaper than petroleum is a conditional sensitivity result, not a probability. Correlated adverse outcomes are represented by the deterministic stress cases in table S15 and fig. S5, each re-optimised with the bounded exhaustive hub search; results are in `cn_robustness.json`.

## S14. Taiwan island system

Taiwan's LP uses its own demand (table S1 note), onshore wind (15 TWh cap), solar (60 TWh), a 25 GW Taiwan Strait offshore zone, 2.5 Mt of residues, 0.05 Mha of bamboo and 0.1 Mt of used cooking oil, liquefied natural gas at USD 12 per MMBtu delivered, a 1.4 times reactor-cost multiplier for a small first fleet, and imported renewable liquids at USD 170 per MWh. Cases: least cost (nuclear hubs and light-water reactors allowed), no nuclear (with batteries replacing firm supply at a USD 35 per MWh firming charge), after gas, and with the 25 GW offshore zone forced. Taiwan's nuclear policy is a matter for Taiwan; the model reports both cases.

## S15. Cross-check of the United States model v8.4

`cn_us_crosscheck.py` reruns the United States least-cost and post-gas cases with corrected heavy-truck ratios (0.41 and 0.76 instead of 0.114 and 0.210). U.S. transport electricity rises from 1,377 to 1,837 TWh, least-cost cost from USD 455.2 to 521.4 billion, and the saving against late-2025 petroleum falls from 23.2% to 12.0%; after gas, from 16.4% to 4.7%. Emission reductions are almost unchanged (93.8% to 93.4%). In the China model, the uncorrected ratios would raise the least-cost saving to 38.3%. The United States v8.4 code also disables steam electrolysis before gas runs out. Re-solving the United States least-cost case with it enabled gives the same result (pyrolysis remains cheaper at United States gas prices), so the restriction does not affect the published United States numbers. In this China model steam electrolysis is available in both eras; with the v8.4 restriction and otherwise identical v1.2 inputs, the China least-cost case would cost USD 304.4 billion instead of 303.4 billion and use 93 bcm of gas for 16.5 Mt of pyrolysis hydrogen. The source files of the United States v8.4 model used for this cross-check are included unchanged (us2_model.py, us2_inputs.py, grid_harvester.py), and `cn_us_crosscheck.py` verifies their SHA-256 hashes before running.

## S16. Build-rate, system-structure and wind-lull screens

Table S14 reports the reactor modules, heat capacity and wind capacity that each solution needs per year, and the shares of firm and variable electricity. Modules are assumed to be built from 2032 to 2050 and wind from 2026 to 2050. For comparison, China approved at least ten large reactors a year from 2022 to 2025 (about 12 GWe, or about 30 GWt) and added about 120 GW of wind in 2025. The screen does not test hourly adequacy, ramping, storage, transmission or stability. Controllable loads (steam electrolysis, drying, managed charging and hydrogen storage) are large in the solutions and would support balancing, but an hourly dispatch and network study is required to show that the annual solution is operable.

Table S17 reports a stylised wind-lull screen. During a windless, overcast winter week (7 days; onshore wind at 8%, offshore wind at 10%, solar at 8% and concentrated solar at 30% of capacity), all flexible loads stop (electrolysis, electric process heat and fuel-conversion plants, whose products are stored) and hub heat goes entirely to the turbines (40% efficiency, 93% availability). The inflexible load is direct transport electricity at 115% of its annual average. Any shortfall is covered by hydrogen-fired backup (USD 750 per kW, 25 years, 40% efficient) burning hydrogen valued at USD 2 per kg for two such weeks a year. The screen distinguishes annual resource adequacy from operational feasibility: it says nothing about ramping, reserves, inertia, network congestion or the daily shape of charging, and its parameters are assumptions.

## S17. Reproducibility

All files sit in one flat folder. `bash run_all.sh 1000` runs the model, Monte Carlo, gas, regional and cross-feed modules, break-even, tests and figures in about 25 minutes on one core; `cn_test.py` runs 429 consistency checks (objective reconciliation, balances, emissions, regional sums, break-even consistency). Requirements: Python 3 with NumPy, SciPy (HiGHS) and Matplotlib.

## S18. Limitations

Annual energy balance without hourly dispatch, storage, transmission or stability analysis; build rates screened but not modelled; carbon-product qualification and market absorption assumed; soil-carbon effects of residue removal treated only as an emissions sensitivity; independent Monte Carlo draws; fixed technology shares; national LP with a regional reporting split; assumed segment splits for diesel and for Hong Kong, Macau and Taiwan; uncertain biomass availability, conversion yields and jet-fuel certification; untested offshore seaweed harvesting; reactor costs, learning and technology parameters for demonstration-scale designs; historical petroleum prices; inventory-level fissile accounting only; schematic maps.

# Supplementary figures

![](FigS1_offshore_merit.png){width="4.4in"}

**Fig. S1.** Offshore wind with seaweed added zone by zone in merit order: 2050 system cost for design and learning yields in the gas era and design yields after gas.

![](FigS2_transition.png){width="4.4in"}

**Fig. S2.** Well-to-wheel emissions of the petroleum baseline and a phased logistic transition, 2025–2060.

![](FigS3_sensitivity.png){width="4.4in"}

**Fig. S3.** Spearman rank correlation of Monte Carlo parameters with least-cost system cost.

![](FigS4_reactor_learning.png){width="4.4in"}

**Fig. S4.** Reactor module cost with learning for the three cost cases; dotted line, least-cost fleet.

![](FigS5_robustness.png){width="5.2in"}

**Fig. S5.** Stress tests of the central least-cost case: 2050 annual cost of each re-optimised case against petroleum at late-2025 (dashed) and November 2026 (dotted) pre-tax prices. Bars in red cost more than petroleum at late-2025 prices.

![](FigS7_htse_heat.png){width="3.3in"}

**Fig. S7.** Temperature–heat diagram of steam electrolysis per kg of hydrogen: feed water (blue) is preheated, evaporated at 0.5 MPa and superheated to 800°C; the hydrogen–steam and oxygen streams leaving the stack (orange) supply the high-temperature superheat through a recuperator. Shaded areas show heat recovered for preheat, external steam-raising heat and electric topping.

![](grid_harvester_top.jpg){width="3.2in"}

**Fig. S6.** Grid Harvester concept used for the offshore seaweed screen (reproduced from the United States model v8.4).

# Supplementary tables

**Table S1. 2025 baseline fuel use (mainland China, Hong Kong and Macau) and its energy.**

| Segment | Fuel | Quantity | TWh (LHV) | Basis |
|:----------------------|------------------:|-----------:|-----------:|----------------------:|
| Light-duty road | Gasoline | 155.72 Mt | 1,878 | CAPE 2025 review [S]; HK, Macau [A] |
| Heavy and medium road | Diesel | 121.18 Mt | 1,441 | 59% of 203 Mt diesel [A] |
| Heavy and medium road | LNG/CNG | 42.6 bcm | 422 | ICIS transport gas [S] |
| Rail | Diesel | 3.5 Mt | 42 | [A] |
| Marine | Diesel | 12.3 Mt | 146 | [A] |
| Marine | Fuel oil (bunkers) | 27.5 Mt | 309 | ~20 Mt bonded bunkers [S]; HK [A] |
| Aviation | Jet fuel | 45.96 Mt | 552 | CAPE 2025 [S]; HK imports [S-order] |
| Farm machinery | Diesel | 25.0 Mt | 297 | [A] |
| Construction and mining | Diesel | 25.1 Mt | 298 | [A] |
| Industrial trucks | Diesel-equivalent | 3.0 Mt | 36 | [A] |
| Pipelines | Natural gas | 5.0 bcm | 50 | [A] |
| Total |  |  | 5,469 | 19.69 EJ |

**Table S2. 2050 technology shares by segment (share of 2025 service).**

| Segment | Shares |
|:----------------------|----------------------:|
| ldv | bev 0.95, re 0.03, fcev 0.01, liquid 0.01 |
| hdv | ers 0.35, bev 0.45, re 0.08, fcev 0.08, liquid 0.04 |
| farm | bev 0.35, re 0.45, liquid 0.20 |
| construction | bev 0.55, re 0.30, liquid 0.15 |
| industrial | bev 0.95, fcev 0.05 |
| rail | elec 0.90, re 0.05, liquid 0.05 |
| air | saf 0.97, h2 0.03 |
| marine | liquid 0.80, elec 0.10, h2 0.10 |
| pipeline | elec 0.60, gas 0.40 |
| Range-extender fuel share | 0.25 |
| Service growth to 2050 | 1.15 |
| Electric/diesel energy ratio, heavy trucks | 0.409 (= 2.40 kWh/mi x 3.6 / 21.1 MJ/mi) |
| Fuel-cell/diesel energy ratio, heavy trucks | 0.758 |
| Electric/gasoline ratio, cars | 0.234 |

**Table S2b. Net annual ownership cost of a battery-electric car relative to a petrol car in 2050, excluding energy (USD per car per year).**

| Component | Low | Central | High |
|:----------------------|-----------:|-----------:|-----------:|
| Purchase-price difference, annualised (12 yr, 5%) | -282 | -113 | 56 |
| Expected battery replacement | 10 | 42 | 200 |
| Maintenance and repair | -158 | -122 | -52 |
| Insurance | 40 | 100 | 300 |
| Net (used in the model) | -390 | -93 | 504 |
| Inputs: price difference (USD) | -2,500 | -1,000 | 500 |
| Inputs: replacements per car; pack USD/kWh | 0.05; 50 | 0.15; 70 | 0.5; 100 |
| Inputs: maintenance saving vs 350 USD/yr | 45% | 35% | 15% |

**Table S3. Electricity and hydrogen parameters (central values; Monte Carlo ranges in table S10).**

| Parameter | Value |
|:----------------------|----------------------:|
| Onshore wind, best sites / remoter sites (USD/MWh) | 30 / 45, capped at 1,200 / 5,000 TWh |
| Solar PV (USD/MWh) | 36 (+1.25 x firming) |
| Firming adder (USD/MWh) | 20 |
| Offshore wind fixed / floating (USD/MWh) | 60 / 90 |
| Concentrated solar with storage (USD/MWh) | 95, firm |
| Light-water reactors (USD/MWh) | 65 |
| Transmission and distribution adder (USD/MWh) | 22 |
| Charging, cars / trucks and machines (USD/MWh) | 25 / 18 |
| Maximum PV share; minimum firm share | 0.40; 0.15 |
| Natural gas for pyrolysis (USD/MMBtu) | 8.5 + 0.8 delivery |
| Pyrolysis capital (USD/kW H2) | 750 |
| Alkaline electrolysis | 52.0 kWh/kg, USD 0.6/kg |
| Steam electrolysis | 36.8 kWh_e + 6.868 kWh_th per kg, USD 0.635/kg |
| Discount rate | 0.05 |

**Table S4a. Reactor cost cases (per 250-MWt module; Wright learning).**

| Case | BOAK USD/kWe | FOAK multiplier | Learning rate | Interest during construction |
|:-----------|-----------:|-------------:|-----------:|---------------:|
| low | 2,500 | 1.3 | 12% | 8% |
| central | 3,500 | 1.5 | 8% | 12% |
| high | 5,000 | 2.0 | 4% | 18% |

**Table S4b. Reactor technologies tested as hub designs, with 2050 transport cost (USD bn).**

| Technology | Outlet °C | Turbine efficiency | Cost multiplier | Fuel USD/MWh_th | Top-tier heat share | Start-up fissile | Gas era | After gas |
|:----------------------|-----------:|-------------:|-------------:|-------------:|-----------:|----------------------:|-----------:|-----------:|
| HTR-PM pebble-bed HTGR (Shidaowan, operating) | 750 | 0.4 | 1.0 | 9.0 | 0.3 | LEU 8.5% | 303.4 | 329.7 |
| Very-high-temperature gas reactor, 950 C (future) | 950 | 0.45 | 1.1 | 10.0 | 0.3 | LEU/HALEU | 299.5 | 326.1 |
| Thorium molten-salt reactor (TMSR-LF1 lineage, 700 C) | 700 | 0.44 | 1.2 | 6.0 | 0.28 | HALEU start, U-233 bred from Th | 286.9 | 310.9 |
| Sodium fast reactor (CFR-600 lineage, 550 C) | 550 | 0.4 | 1.25 | 12.0 | 0.22 | Pu (MOX/metal) | 313.4 | 345.4 |
| Light-water SMR (ACP100 Linglong One, ~320 C) | 320 | 0.33 | 0.85 | 7.0 | 0.08 | LEU <5% | 304.9 | 331.2 |

**Table S5. Residue tiers and use in the least-cost case.**

| Resource | Region | Cap (Mt dry/yr) | USD/t | Used (Mt) |
|:----------------------|--------------:|-----------:|-----------:|-----------:|
| Crop straw, North China Plain and Northeast (maize, wheat) | rest | 110.0 | 40 | 110.0 |
| Crop straw, Yangtze and South China (rice) | rest | 55.0 | 45 | 55.0 |
| Inner Mongolia maize stover and crop stalks | inner_mongolia | 25.0 | 38 | 25.0 |
| Xinjiang cotton stalks and crop residues | xinjiang | 20.0 | 40 | 20.0 |
| Guangxi sugarcane bagasse surplus and cassava residues | guangxi | 8.0 | 35 | 8.0 |
| Ningxia crop residues (Loess Plateau) | ningxia | 2.0 | 42 | 2.0 |
| Xizang alpine grassland biomass and forestry residues | xizang | 1.5 | 75 | 1.5 |
| Forestry and wood-processing residues | rest | 70.0 | 55 | 70.0 |
| Existing bamboo-stand residues and thinnings (Fujian, Zhejiang, Jiangxi, Hunan) | rest | 30.0 | 45 | 30.0 |
| Crop straw tier 2 (higher removal, longer haul) | rest | 60.0 | 65 | 60.0 |

**Table S6a. Sugar and starch ethanol feedstocks (autonomous-region crops) and use.**

| Feedstock | Region | Cap (bn gal) | USD/gal | Used (bn gal) |
|:----------------------|--------------:|-----------:|-----------:|-----------:|
| Guangxi cassava (non-grain fuel ethanol) | guangxi | 0.35 | 2.40 | 0.35 |
| Guangxi sugarcane molasses | guangxi | 0.21 | 1.60 | 0.21 |
| Inner Mongolia sweet sorghum (saline-alkaline land) | inner_mongolia | 0.71 | 2.00 | 0.71 |
| Xinjiang sweet sorghum (drip-irrigated saline land) | xinjiang | 0.59 | 2.00 | 0.59 |
| Ningxia sweet sorghum (Loess Plateau) | ningxia | 0.12 | 2.10 | 0.12 |
| Inner Mongolia Jerusalem artichoke (sandy land) | inner_mongolia | 0.16 | 2.60 | 0.16 |
| Ningxia sweet potato | ningxia | 0.05 | 2.50 | 0.05 |
| Aged-grain ethanol, existing plants | rest | 1.20 | 2.20 | 1.20 |

**Table S6b. Oil feedstocks for hydroprocessing and use.**

| Feedstock | Region | Cap (Mt) | USD/t | Used (Mt) |
|:----------------------|-----------:|-----------:|-----------:|-----------:|
| Used cooking oil and trap grease (collected) | rest | 5.00 | 800 | 5.00 |
| Jatropha curcas on marginal slopes (Guangxi, Yunnan, Sichuan) | guangxi | 0.50 | 900 | 0.50 |
| Xinjiang cottonseed and non-edible oilseed residues | xinjiang | 0.40 | 700 | 0.40 |
| Woody oil crops (Xanthoceras, Pistacia) in the north | rest | 0.50 | 1,000 | 0.50 |

**Table S6c. New bamboo and hemp land (Mha).**

| Crop | Region | Max Mha |
|:-----------|----------------------:|-----------:|
| Bamboo | Guangxi hills (clumping Dendrocalamus, Bambusa) | 0.60 |
| Bamboo | Guangdong | 0.40 |
| Bamboo | Sichuan basin and Chongqing | 0.50 |
| Bamboo | Yunnan | 0.50 |
| Bamboo | Guizhou | 0.30 |
| Bamboo | Fujian, Jiangxi, Hunan (clumping species only) | 0.70 |
| Hemp | Heilongjiang | 0.80 |
| Hemp | Jilin | 0.30 |
| Hemp | Inner Mongolia (east) | 0.40 |
| Hemp | Yunnan | 0.30 |
| Hemp | Shanxi and Gansu | 0.20 |

**Table S7. Offshore wind and seaweed zones.**

| Zone | Species | Yield t/ha (dem./design/learning) | GW (large build) | Port km | Seaweed fuel USD/MWh |
|:----------------------|----------------------:|-------------------------:|-----------:|-----------:|-------------:|
| Liaodong peninsula (Dalian, Yellow Sea) | Saccharina japonica + Undaria pinnatifida | 6.0/12.0/18.0 | 40 | 40 | 183 |
| Shandong peninsula (Rongcheng, Weihai) | Saccharina japonica (China's kelp centre) | 7.0/13.0/19.0 | 60 | 40 | 180 |
| Jiangsu radial sand ridges (Rudong, Yancheng) | Pyropia yezoensis (nori) winter + Gracilaria summer | 2.0/4.0/6.0 | 70 | 50 | 261 |
| Zhejiang (Zhoushan, Wenzhou) | Sargassum fusiforme + Pyropia haitanensis + winter Saccharina | 4.0/8.0/12.0 | 50 | 45 | 204 |
| Fujian, Taiwan Strait (Xiapu, Pingtan) | Winter Saccharina + summer Gracilaria lemaneiformis + Pyropia | 6.0/12.0/18.0 | 80 | 40 | 184 |
| Guangdong (Yangjiang, Shanwei, Zhanjiang) | Gracilaria lemaneiformis + Ulva + Sargassum | 3.0/6.0/9.0 | 90 | 60 | 224 |
| Beibu Gulf (Guangxi: Beihai, Qinzhou, Fangchenggang) | Gracilaria + Ulva; Kappaphycus trials | 3.0/6.0/9.0 | 30 | 45 | 224 |
| Hainan (Wanning, Lingshui, Danzhou) | Kappaphycus alvarezii / Eucheuma + Gracilaria (tropical reds) | 4.0/8.0/12.0 | 40 | 50 | 204 |
| Taiwan Strait (Changhua, Miaoli) | Gracilaria + Ulva (warm water) | 3.0/6.0/9.0 | 25 | 40 | Taiwan system |

**Table S8. Pre-tax petroleum prices used for the comparator (USD per tonne; road gas USD/MMBtu).**

| Fuel | Late 2025 | November 2026 |
|:----------------------|-----------:|-----------:|
| gasoline | 870 | 1,198 |
| diesel | 778 | 1,042 |
| jet | 700 | 1,042 |
| resid | 480 | 700 |
| road_gas_mmbtu | 11 | 14 |
| Petroleum comparator, 2050 services (USD bn) | 399.3 | 546.0 |

**Table S9. Natural-gas supply inputs.**

| Input | Value |
|:----------------------|-----------:|
| prod_bcm_2025 | 261.9 |
| consumption_bcm_2025 | 426.6 |
| import_share_2025 | 0.413 |
| pipeline_import_bcm_2025 | 81.0 |
| lng_import_mt_2025 | 68.43 |
| pipeline_cap_bcm_2030 | 114.0 |
| pipeline_cap_bcm_2035 | 150.0 |
| trr_conventional_tight_tcm | 40.0 |
| trr_shale_tcm | 25.0 |
| trr_cbm_tcm | 11.0 |
| cumulative_produced_tcm | 3.2 |
| domestic_cap_growth | 0.03 |
| domestic_plateau_bcm | 360.0 |
| pipeline_pool_tcm | 20.0 |
| lng_cap_bcm | 140.0 |
| non_transport_growth | 0.015 |
| non_transport_growth_until | 2040 |
| rp_floor_years | 15.0 |
| res_com_bcm | 110.0 |

**Table S10. Monte Carlo parameters (triangular low/mode/high).**

| Parameter | Low | Mode | High |
|:----------------------|-----------:|-----------:|-----------:|
| ELEC/onshore_wind | 22 | 30 | 48 |
| ELEC/solar | 26 | 36 | 55 |
| ELEC/osw_fixed | 48 | 60 | 95 |
| ELEC/osw_floating | 70 | 90 | 140 |
| ELEC/lwr | 50 | 65 | 100 |
| ELEC/csp | 70 | 95 | 140 |
| ELEC/vre_firming | 10 | 20 | 40 |
| ELEC/td_adder | 15 | 22 | 35 |
| ELEC/charge_ldv | 15 | 25 | 45 |
| ELEC/export_value | 15 | 30 | 45 |
| PYRO/capex_kw_h2 | 500 | 750 | 1600 |
| GAS/price_mmbtu | 6.0 | 8.5 | 13.0 |
| PYRO/leak_upstream | 0.005 | 0.015 | 0.03 |
| ROUTES/htl/cost_t | 100 | 130 | 210 |
| ROUTES/pbtl/cost_t | 180 | 230 | 350 |
| SEAWEED_PROCESS/farm_cost_ref_t | 200 | 260 | 450 |
| VEH/ldv_bev_net_usd_yr | -389.6 | -93.3 | 503.9 |
| VEH/bev_truck_net_usd_yr | 0 | 1200 | 3500 |
| VEH/ers_capex_m_per_km | 1.2 | 1.8 | 3.5 |
| H2_DELIVERY/vehicle | 1.2 | 2.0 | 3.5 |
| ENDUSE/service_growth_2050 | 1.0 | 1.15 | 1.4 |
| HEMP/cost_usd_ha | 450 | 600 | 900 |
| BAMBOO/establish_usd_ha | 1200 | 2000 | 4000 |
| WACC | 0.04 | 0.05 | 0.08 |
| Biomass price scale | 0.8 | 1.0 | 1.4 |
| Ethanol cost scale | 0.85 | 1.0 | 1.3 |
| Carbon market size scale | 0.5 | 1.0 | 1.5 |
| Carbon value scale | 0.5 | 1.0 | 1.3 |
| Yield level (0/1/2) | p=0.3 | p=0.5 | p=0.2 |
| Reactor cost case (low/central/high) | p=0.25 | p=0.5 | p=0.25 |

**Table S11. All deterministic cases (2050). Cost in USD bn per year; saving against late-2025 petroleum (USD 399.3 bn for mainland cases); capacities in GW; hydrogen in Mt; CO2e in Mt per year.**

| Case | Cost | Save % | Hubs | Wind | PV | CSP | Offsh. | Pyro H2 | Elec. H2 | CO2e |
|:----------------------|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|
| least_cost | 303.4 | 24.0 | 239 | 322 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| least_cost_blend20 | 303.0 | 24.1 | 256 | 326 | 0 | 0 | 0 | 5.8 | 13.0 | 107 |
| least_cost_flex_heat | 303.4 | 24.0 | 239 | 322 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| design_half_offshore | 327.5 | 18.0 | 239 | 20 | 0 | 0 | 230 | 5.8 | 8.6 | 108 |
| design | 357.7 | 10.4 | 52 | 0 | 0 | 0 | 460 | 11.8 | 1.0 | 120 |
| least_cost_reactor_low | 282.6 | 29.2 | 449 | 0 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| least_cost_reactor_high | 317.4 | 20.5 | 12 | 415 | 228 | 0 | 0 | 16.5 | 0.0 | 134 |
| least_cost_no_nuclear | 354.3 | 11.3 | 0 | 426 | 551 | 49 | 0 | 0.0 | 16.5 | 96 |
| least_cost_no_vehicle_carbon | 312.9 | 21.6 | 243 | 336 | 0 | 0 | 0 | 5.3 | 11.3 | 108 |
| least_cost_demonstrated_yields | 308.5 | 22.8 | 239 | 348 | 0 | 0 | 0 | 5.8 | 12.6 | 110 |
| least_cost_us_truck_ratios | 246.2 | 38.3 | 218 | 135 | 0 | 0 | 0 | 5.8 | 7.9 | 102 |
| post_gas_least_cost | 329.7 | 17.4 | 283 | 328 | 0 | 0 | 0 | 0.0 | 16.6 | 90 |
| post_gas_half_offshore | 353.8 | 11.4 | 284 | 25 | 0 | 0 | 230 | 0.0 | 14.6 | 89 |
| post_gas_reactor_low | 306.5 | 23.3 | 497 | 0 | 0 | 0 | 0 | 0.0 | 16.6 | 90 |
| post_gas_reactor_high | 352.8 | 11.6 | 0 | 415 | 563 | 0 | 0 | 0.0 | 16.6 | 91 |
| post_gas_no_nuclear | 359.5 | 10.0 | 0 | 435 | 563 | 51 | 0 | 0.0 | 16.6 | 91 |
| post_gas_htse_48kwh | 339.0 | 15.1 | 283 | 393 | 0 | 0 | 0 | 0.0 | 16.6 | 92 |
| post_gas_vhtr_si | 326.1 | 18.3 | 435 | 1 | 0 | 0 | 0 | 0.0 | 16.6 | 90 |
| least_cost_bev_net_zero | 340.6 | 14.7 | 239 | 322 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| least_cost_bev_plus100 | 380.5 | 4.7 | 239 | 322 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| least_cost_bev_tco_high | 541.7 | -35.7 | 239 | 322 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| least_cost_bev_tco_low | 185.2 | 53.6 | 239 | 322 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| least_cost_fleet_350 | 308.8 | 22.7 | 239 | 322 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| least_cost_fleet_500 | 297.2 | 25.6 | 239 | 322 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| least_cost_no_carbon_revenue | 329.9 | 17.4 | 283 | 326 | 0 | 0 | 0 | 0.0 | 16.6 | 96 |
| least_cost_carbon_commodity | 324.9 | 18.6 | 265 | 331 | 0 | 0 | 0 | 2.4 | 14.2 | 101 |
| least_cost_residues_75 | 333.9 | 16.4 | 288 | 415 | 0 | 0 | 0 | 5.8 | 22.4 | 117 |
| least_cost_residues_50 | 376.0 | 5.8 | 239 | 401 | 0 | 0 | 192 | 5.8 | 31.6 | 124 |
| least_cost_hub_cap_60 | 310.9 | 22.2 | 60 | 415 | 184 | 0 | 0 | 16.5 | 0.0 | 134 |
| least_cost_hub_cap_30 | 313.6 | 21.5 | 30 | 415 | 219 | 0 | 0 | 16.5 | 0.0 | 134 |
| least_cost_grid_tight | 323.9 | 18.9 | 449 | 0 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| least_cost_bev_plus100_no_carbon | 407.0 | -1.9 | 283 | 326 | 0 | 0 | 0 | 0.0 | 16.6 | 96 |
| least_cost_stress_moderate | 448.9 | -12.4 | 20 | 415 | 0 | 0 | 0 | 28.3 | 0.0 | 170 |
| post_gas_stress_moderate | 468.7 | -17.4 | 0 | 157 | 0 | 0 | 0 | 0.0 | 28.3 | 100 |
| least_cost_stress_severe | 657.4 | -64.6 | 20 | 415 | 0 | 0 | 0 | 28.3 | 0.0 | 170 |
| least_cost_us_v84_htse_rule | 304.4 | 23.8 | 159 | 343 | 0 | 0 | 0 | 16.5 | 0.0 | 134 |
| least_cost_no_nuclear_alkaline | 361.3 | 9.5 | 0 | 451 | 579 | 49 | 0 | 0.0 | 16.5 | 98 |
| least_cost_food_credit | 301.9 | 24.4 | 239 | 322 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| least_cost_htse_topping_3 | 304.4 | 23.8 | 188 | 339 | 0 | 0 | 0 | 12.5 | 3.9 | 125 |
| least_cost_htse_no_lowT_recovery | 303.6 | 24.0 | 255 | 297 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| type_htr_pm | 303.4 | 24.0 | 239 | 322 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| post_gas_type_htr_pm | 329.7 | 17.4 | 283 | 328 | 0 | 0 | 0 | 0.0 | 16.6 | 90 |
| type_vhtr | 299.5 | 25.0 | 390 | 0 | 0 | 0 | 0 | 5.8 | 10.7 | 108 |
| post_gas_type_vhtr | 326.1 | 18.3 | 435 | 1 | 0 | 0 | 0 | 0.0 | 16.6 | 90 |
| type_tmsr | 286.9 | 28.2 | 405 | 0 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| post_gas_type_tmsr | 310.9 | 22.1 | 448 | 0 | 0 | 0 | 0 | 0.0 | 16.6 | 90 |
| type_cfr | 313.4 | 21.5 | 122 | 414 | 0 | 0 | 0 | 16.5 | 0.0 | 134 |
| post_gas_type_cfr | 345.4 | 13.5 | 236 | 415 | 1 | 0 | 0 | 0.0 | 16.6 | 90 |
| type_acp100 | 304.9 | 23.6 | 239 | 395 | 0 | 0 | 0 | 5.8 | 10.7 | 109 |
| post_gas_type_acp100 | 331.2 | 17.1 | 283 | 412 | 0 | 0 | 0 | 0.0 | 16.6 | 90 |
| tw_least_cost | 17.7 | -13.2 | 7 | 5 | 1 | 0 | 0 | 0.3 | 0.0 | 8 |
| tw_no_nuclear | 20.3 | -29.9 | 0 | 5 | 13 | 0 | 6 | 0.0 | 0.2 | 8 |
| tw_post_gas | 18.9 | -21.2 | 9 | 5 | 1 | 0 | 0 | 0.0 | 0.3 | 8 |
| tw_post_gas_no_nuclear | 20.6 | -31.6 | 0 | 5 | 13 | 0 | 6 | 0.0 | 0.2 | 8 |
| tw_offshore_25gw | 22.4 | -43.4 | 1 | 0 | 0 | 0 | 25 | 0.2 | 0.5 | 8 |
| sustainable_fission_tmsr | 306.0 | 23.4 | 424 | 0 | 0 | 0 | 0 | 0.0 | 16.6 | 90 |
| sustainable_fission_cfr | 343.1 | 14.1 | 229 | 414 | 0 | 0 | 0 | 0.0 | 16.6 | 90 |
| sustainable_fission_tmsr_nuclear_only | 306.1 | 23.4 | 425 | 0 | 0 | 0 | 0 | 0.0 | 16.6 | 90 |
| sustainable_fission_tmsr_premium | 332.1 | 16.8 | 424 | 0 | 0 | 0 | 0 | 0.0 | 16.6 | 90 |

**Table S12. Least-cost 2050 well-to-wheel emissions under wider life-cycle boundaries (Mt CO2e per year; no re-optimisation).**

| Boundary | Emissions | Reduction % | Liquid fuels | Electricity | Hub construction/fuel |
|:----------------------|------------:|------------:|-----------:|--------------:|--------------------:|
| Central boundary | 109 | 94.8 | 80 | 14 | 0 |
| Electricity 25 g CO2e/kWh (vs 10) | 137 | 93.4 | 84 | 36 | 0 |
| Upstream methane leakage 3% (vs 1.5%) | 120 | 94.2 | 87 | 14 | 0 |
| Residue soil-carbon loss 20 g CO2e/MJ | 185 | 91.1 | 156 | 14 | 0 |
| Residue soil-carbon loss 40 g CO2e/MJ | 261 | 87.4 | 232 | 14 | 0 |
| Reactor construction and fuel cycle 3 g CO2e/kWh of hub heat | 117 | 94.3 | 80 | 14 | 9 |
| All of the above (40 g soil carbon) | 309 | 85.1 | 243 | 36 | 9 |

**Table S13. Destination and durability of pyrolysis carbon, least-cost case (Mt C per year). None is counted as an emission reduction.**

| Durability class | Mt C | Markets |
|:----------------------|-----------:|----------------------:|
| One product life (10-20 years) | 6.3 | Vehicle structures and H2 tanks (methane-derived carbon fibre/CNT); Battery anode graphite (after graphitisation); Specialty carbon (conductive additive, fibre precursors) |
| Short-lived (tyre wear, end-of-life combustion) | 7.0 | Carbon black: tyres and rubber |
| Oxidised in use (metallurgy) | 4.0 | Metallurgical: electrodes, recarburiser, Al anodes |
| Long-term (asphalt, concrete, permanent storage) | 0.0 | Construction: asphalt and concrete additive; Permanent storage (mine voids, monofill) |
| Uncertain (soil amendment) | 0.0 | Soil amendment (agronomic benefit unproven) |

**Table S14. Build-rate and system-structure screen (reactor modules built 2032-2050; wind 2026-2050).**

| Case | Hubs | Modules | Per yr | GWt/yr | Wind GW | Wind/yr | Solar GW | Firm % | Variable % |
|:------------------|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|
| Central least cost | 239 | 1,434 | 75 | 18.9 | 322 | 13 | 0 | 53 | 47 |
| After gas | 283 | 1,698 | 89 | 22.3 | 328 | 13 | 0 | 57 | 43 |
| At most 60 hubs | 60 | 360 | 19 | 4.7 | 415 | 17 | 184 | 14 | 86 |
| Moderate stress | 20 | 120 | 6 | 1.6 | 415 | 17 | 0 | 38 | 62 |

**Table S15. Stress-test cases (2050; USD bn per year; each re-optimised).**

| Case | Cost | Saving % | Hubs | Pyrolysis H2 Mt | Emissions Mt |
|:----------------------|-----------:|-----------:|-----------:|------------:|------------:|
| Electric-car net cost 0 USD/yr (no advantage) | 340.6 | 14.7 | 239 | 5.8 | 109 |
| Electric-car net cost +100 USD/yr | 380.5 | 4.7 | 239 | 5.8 | 109 |
| Electric-car net cost, high derivation | 541.7 | -35.7 | 239 | 5.8 | 109 |
| Electric-car net cost, low derivation | 185.2 | 53.6 | 239 | 5.8 | 109 |
| Car stock 350 million | 308.8 | 22.7 | 239 | 5.8 | 109 |
| Car stock 500 million | 297.2 | 25.6 | 239 | 5.8 | 109 |
| No carbon-product revenue | 329.9 | 17.4 | 283 | 0.0 | 96 |
| Commodity carbon markets only | 324.9 | 18.6 | 265 | 2.4 | 101 |
| Collectable residues -25% | 333.9 | 16.4 | 288 | 5.8 | 117 |
| Collectable residues -50% | 376.0 | 5.8 | 239 | 5.8 | 124 |
| At most 60 hubs (360 modules) | 310.9 | 22.2 | 60 | 16.5 | 134 |
| At most 30 hubs (180 modules) | 313.6 | 21.5 | 30 | 16.5 | 134 |
| Grid and firming costs +60-75% | 323.9 | 18.9 | 449 | 5.8 | 109 |
| electric-car +100 USD/yr and no carbon revenue | 407.0 | -1.9 | 283 | 0.0 | 96 |
| Combined: no electric-car advantage, commodity carbon only, residues -25%, high reactor cost, tight grid | 448.9 | -12.4 | 20 | 28.3 | 170 |
| Combined (moderate) after gas | 468.7 | -17.4 | 0 | 0.0 | 100 |
| Combined: electric-car high derivation, no carbon revenue, residues -25%, high reactor cost, tight grid | 657.4 | -64.6 | 20 | 28.3 | 170 |
| Steam electrolysis only after gas (U.S. v8.4 rule) | 304.4 | 23.8 | 159 | 16.5 | 134 |
| No nuclear, alkaline electrolysis only | 361.3 | 9.5 | 0 | 0.0 | 98 |
| Food-heat credit inside the transport boundary (v1.1 accounting) | 301.9 | 24.4 | 239 | 5.8 | 109 |
| Steam electrolysis: 3 kWh/kg electric topping | 304.4 | 23.8 | 188 | 12.5 | 125 |
| Steam electrolysis: no low-temperature heat recovery | 303.6 | 24.0 | 255 | 5.8 | 109 |

**Table S16. Steam-electrolysis heat balance per kg of hydrogen (800 C stack, 0.5 MPa, 80% steam utilisation, no sweep gas).**

| Item | kWh/kg | Temperature range (C) | Supplied by |
|:----------------------|-----------:|--------------:|----------------------:|
| Feed-water preheat (total) | 1.73 | 20 to 152 | recovered heat, then external |
|   recovered from hot-stream sensible heat | 0.69 | 75 to 127 | hot streams 274 to 100 C |
|   recovered by condensing unconverted steam | 0.71 | 20 to 75 | below the 100 C dew point |
| Evaporation | 6.54 | 152 | external |
| External steam-raising heat (model input) | 6.87 | up to 152 | reactor process steam or electric boiler |
| Superheat (total) | 4.26 | 152 to 800 |  |
|   by high-temperature recuperator | 4.08 | 152 to 775 | hot streams 800 to 274 C |
|   electric trim | 0.18 | 775 to 800 | electric heater |
| Stack and hot-box heat loss | 0.50 | 800 | electric heater |
| Electric topping (model input) | 0.68 |  |  |
| Recuperator area, m2 per kg/h | 1.11 | LMTD 61 K | USD 0.034 per kg H2 |
| Without low-temperature recovery: external heat | 8.26 | up to 152 | sensitivity case |

**Table S17. Stylised wind-lull adequacy screen: a windless, overcast 7-day winter period with all flexible loads stopped. Load = inflexible transport load (GW); Firm = hubs with all heat to turbines plus light-water reactors (GW); Lull VRE = wind, solar and CSP output in the lull (GW); Short = shortfall (GW, and TWh over the week); Backup = indicative annual cost of hydrogen-fired backup (USD bn and % of system cost); H2 lost = electrolytic hydrogen not produced during the week (Mt).**

| Case | Load | Firm | Lull VRE | Short GW | Short TWh | Backup bn | % cost | H2 lost |
|:------------------|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|
| Central least cost | 189 | 133 | 26 | 30 | 5.1 | 3.1 | 1.0 | 0.21 |
| After gas | 196 | 158 | 26 | 12 | 2.0 | 1.2 | 0.4 | 0.32 |
| No nuclear | 189 | 0 | 93 | 97 | 16.2 | 10.0 | 2.8 | 0.32 |
| At most 30 hubs | 189 | 28 | 51 | 111 | 18.6 | 11.5 | 3.7 | 0.00 |
| High reactor cost | 189 | 27 | 51 | 111 | 18.6 | 11.5 | 3.6 | 0.00 |


# Supplementary references

[S1] World Nuclear News. China's demonstration HTR-PM enters commercial operation. 6 December 2023. https://www.world-nuclear-news.org/articles/chinese-HTR-PM-Demo-begins-commercial-operation (22 November 2026, date last accessed).

[S2] World Nuclear News. Chinese molten salt reactor achieves conversion of thorium-uranium fuel. November 2025. https://world-nuclear-news.org/articles/chinese-msr-achieves-conversion-of-thorium-uranium-fuel (22 November 2026, date last accessed).

[S3] Zhang H. China started operation of its first CFR-600 breeder reactor. IPFM blog, 15 December 2023. https://fissilematerials.org/blog/2023/12/china_started_operation_o.html (22 November 2026, date last accessed).

[S4] World Nuclear News. Chinese SMR completes non-nuclear steam start up test. December 2025. https://world-nuclear-news.org/articles/chinese-smr-completes-non-nuclear-steam-start-up-test (22 November 2026, date last accessed).

[S5] Shi W, Tan T, Fang Y et al. Quantifying reasonable straw removal rate to achieve food security, bioenergy transition and climate mitigation in China. Resour Conserv Recycl 2025;215:108114. https://doi.org/10.1016/j.resconrec.2024.108114

[S6] World Nuclear Transport Institute. Development of civil nuclear power in China. November 2025. https://www.wnti.co.uk/wp-content/uploads/2025/12/WNTI-Rep-Update-China.pdf (22 November 2026, date last accessed).

[S7] Stimson Center. Spent nuclear fuel in China: fact sheet. 2020. https://www.stimson.org/2020/spent-nuclear-fuel-china/ (22 November 2026, date last accessed).

[S8] International Panel on Fissile Materials. The 2025 update on fissile material stocks. June 2026. https://fissilematerials.org/blog/2026/06/the_2025_update_on_fissil.html (22 November 2026, date last accessed).
