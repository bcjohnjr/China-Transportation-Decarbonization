---
title: "Electrification, reactor heat and regional biofuels for a petroleum-free transport system in the world's largest emitter: costs, conditions and limits"
---

**Research Article**

**Jonathan Karl Bily^1,\*^, Christoph Pahl^2^ and Patricia Valdes Bacallao^3^**

^1^Cloud Wash Laundry Corporation, Teruel, Spain

^2^Technical University of Munich, Munich, Germany

^3^University of Málaga, Málaga, Spain

\*Corresponding author. E-mail: jonathan@cloudwashlaundry.com. ORCID: 0009-0004-3526-7271

## Abstract

China emits about one-third of the world's fossil carbon dioxide; its transport fuels add about 1.8 billion tonnes of carbon dioxide equivalent a year, well to wheel. We built an open annual least-cost model of a petroleum-free transport system for mainland China, including the five autonomous regions, Hong Kong and Macau, and for Taiwan. It links electric vehicles and expressways, reactor hubs whose heat cascades from hydrogen production to fuel upgrading and food production, and liquid fuels from residues, bamboo, hemp, regional crops and seaweed. Fields that supply biomass must get back the nitrogen, phosphorus, potassium and stable soil carbon that harvesting removes. The model tests annual resource adequacy, not hourly operation. In the central 2050 configuration the system costs 314.1 billion United States dollars per year, 21.5% less than the same services supplied with petroleum at late-2025 pre-tax prices, and cuts well-to-wheel emissions by 93.7%. This is an optimistic point: across 1,000 draws the median saving is 3.3%, and plausible wind-lull backup lowers the central saving to 19.8%. The saving rests mainly on battery-electric cars costing no more to own than petrol cars: without that advantage it falls to 12.2%, and with the least favourable ownership-cost derivation the system costs 38% more than petroleum. Moderately adverse assumptions taken together make it 15% dearer than petroleum at late-2025 prices, though cheaper at November 2026 prices. Closing the nutrient and soil-carbon balance adds 5.1 billion dollars a year; replacing soil carbon from biological sources alone, with green manure and manure compost instead of pyrolysis carbon, adds 1.6 billion. Pyrolysis uses 48 billion cubic metres of gas a year; after gas the saving is 18.6%. All five autonomous regions are net suppliers of renewable liquid fuel; Taiwan's island system costs more than petroleum.

**Keywords:** China; transport decarbonization; high-temperature gas-cooled reactor; steam electrolysis; biofuels; electric vehicles; robustness analysis

**Teaser text:** This study models a petroleum-free transport system for China, its autonomous regions, Hong Kong, Macau and Taiwan. Electrification, reactor heat and regional biofuels could cost about one-fifth less than petroleum if electric cars stay no more expensive to own than petrol cars, while returning to fields the nutrients and soil carbon that biofuel harvests remove; vehicle costs, carbon markets, biomass supply and build rates set the limits.

## 1 Introduction

China is the largest emitter of carbon dioxide. The Global Carbon Project attributes about 32% of the 38.1 Gt of fossil CO~2~ projected for 2025 to China [1]. Its transport sector is a smaller share of national emissions than in the United States, about 0.9 to 1.1 Gt CO~2~ at the tailpipe [2, 3], but it is large in absolute terms and, unlike power, is still dominated by oil. In 2025 China consumed about 155 Mt of gasoline, 203 Mt of diesel and 40 Mt of jet fuel [4], and used around 43 billion cubic metres (bcm) of natural gas in trucks and buses [5]. Including fuel production and refining, we estimate the well-to-wheel emissions of the transport services in our scope at 1,804 Mt CO~2~e in 2025.

China is also further along in transport electrification than any other large economy. New-energy vehicles were 49% of new car registrations in 2025, and the stock reached 44 million [6]. Zero-emission trucks were a quarter of medium and heavy truck sales [7], and gasoline and diesel demand has started to fall [8]. What remains is harder: aviation, shipping, off-road machinery and the long tail of heavy freight still need dense fuels or very large electricity and hydrogen supplies. Studies that treat one mode or one fuel at a time can miss the shared limits on biomass, hydrogen, heat and electricity [9, 10].

A related open model of United States transport [11] uses high-temperature reactor hubs to supply heat and hydrogen, electric roads and vehicles to carry most road travel, and land and ocean biomass to supply liquids. Here we build the equivalent model for China with Chinese data and technologies: the pebble-bed high-temperature gas-cooled reactor now operating at Shidaowan [12], the thorium molten-salt reactor programme at Wuwei [13], the sodium fast reactor at Xiapu [14], light-water small modular reactors [15], the world's largest offshore wind fleet [16] and seaweed industry [17], and the energy crops of the five autonomous regions (section 2.5).

We ask six questions. First, can a least-cost petroleum-free system serve all 2050 transport services in mainland China, Hong Kong and Macau for less than petroleum,  Second, how much natural gas would methane pyrolysis consume, and what does hydrogen cost once gas is no longer used? Third, which reactor technology suits the hubs, and is start-up fissile material, including plutonium that might be released by arms reductions, a constraint? Fourth, how do the autonomous regions, the two special administrative regions and Taiwan differ? Fifth, how robust is the result to vehicle ownership costs, carbon co-product markets, residue supply and limits on how fast reactors and grids can be built? Sixth, can the fields that supply biomass keep their nutrients and soil carbon, and can seaweed farmed in nutrient-polluted coastal water help? We also report the food that reactor heat could grow and how by-products of one farmed species can feed another, keeping these outside the transport cost. All results are conditional screening estimates, not forecasts.

## 2 Materials and methods

### 2.1 Scope and study area

The model covers on-road vehicles, aviation, rail, domestic and bunkered marine fuel, farm machinery, construction and mining machinery, industrial trucks and pipeline compression. Mainland China, including the five autonomous regions, is modelled together with Hong Kong and Macau, which draw electricity and refined fuels from Guangdong. Taiwan has its own grid, refineries and fuel market and is modelled as a separate island system. The 2025 baseline (table S1) uses fuel consumption from the China Association of Petroleum Enterprises' 2025 review [4], transport gas from industry estimates [5], bunker sales [18], Hong Kong jet-fuel imports [19] and, for Taiwan, United States Energy Information Administration data [20]. Diesel is split between on-road, rail, marine, farm, construction and mining, and non-transport uses by assumption; the excluded non-transport share is 14.5 Mt. Baseline transport energy is 19.7 EJ. Services grow by 15% to 2050 in the central case (range 0 to 40%).

### 2.2 End uses in 2050

Technology shares by segment are fixed for 2050 (table S2). Cars are 95% battery-electric, 3% extended-range electric, 1% fuel-cell and 1% liquid-fuelled. Heavy and medium road freight is 35% on overhead-catenary expressways, 45% battery-electric (including battery swapping), 8% extended-range, 8% fuel-cell and 4% liquid. Rail is 90% electric, and aviation uses 97% drop-in jet fuel and 3% hydrogen. Electric and fuel-cell energy use is computed from the displaced fuel energy with drivetrain ratios. For heavy trucks we use 2.40 kWh per mile for battery-electric and 21.1 MJ per mile for diesel. The diesel figure is on a higher-heating-value basis; on the lower-heating-value basis of our fuel data it is 19.7 MJ per mile, so the ratio is 0.44 kWh per kWh of diesel (0.81 kWh of hydrogen for fuel-cell trucks), about 1.4 kWh per km for a Chinese heavy tractor. The United States model divided the same two numbers without converting MJ to kWh. This gave a ratio of 0.11 and understated heavy-truck electricity and hydrogen by a factor of 3.6 (section 3.9 and supplementary section S15).

Vehicle costs enter as the net annual cost of each electric or fuel-cell vehicle relative to a combustion equivalent, excluding energy, which the model costs separately. For cars this term is derived from four components (table S2b): the purchase-price difference annualised over a 12-year life at the discount rate, expected battery replacement, maintenance and repair, and insurance. The average new-energy car sold in China in August 2025 cost about 90% as much as the average petrol car [21], and parity for mid-range battery-electric cars was projected for 2026 to 2029 [22]. Averages mix sizes and segments, so we assume a smaller central difference, battery-electric cars USD 1,000 cheaper in 2050, and test a case in which they are USD 500 dearer. Maintenance is taken as 35% lower than for petrol cars, less than the roughly 40% reported per mile [23]. Insurance is the least favourable term. The average new-energy car premium was 4,360 yuan (about USD 610) in 2025 [24], but like-for-like premiums are only about 20% higher than for petrol cars [25]. We use USD 100 per year in the central case and USD 300, about half of today's average premium, in the high case. The resulting central value is a net saving of USD 93 per car per year, with a range from a saving of USD 390 to an extra cost of USD 504. Vehicle stocks are specified for 2050 and are not scaled again by service growth. With 420 million cars in 2050, every USD 100 per car per year changes system cost by about USD 40 billion; table S2b reconciles each component with the system cost.

### 2.3 Optimization model

The model is an annual linear programme solved with HiGHS through SciPy [26, 27]. It minimizes the 2050 annual cost

$$C = \sum_i c_i x_i + F,$$

where $x_i$ are activity levels (generation, hydrogen production, biomass purchases, conversion routes, carbon sales), $c_i$ their unit costs and $F$ the costs fixed by the end-use mix (grids, charging, electric expressways, vehicles). Constraints balance electricity, hydrogen, liquid fuel, jet fuel and three tiers of reactor heat; bound biomass tiers, crops, land and renewable capacity; and limit solar to 40% of supply with at least 15% firm supply (table S3; supplementary section S3). The model balances energy annually and has no hourly dispatch.

Electricity comes from onshore wind in two cost tiers (USD 30 and 45 per MWh, plus a USD 20 per MWh firming charge), solar photovoltaics (USD 36 per MWh plus 1.25 times the firming charge), concentrated solar power with storage (USD 95 per MWh), light-water reactors (USD 65 per MWh), offshore wind and reactor hubs. Renewable costs follow the International Renewable Energy Agency's 2025 cost report and Chinese grid research [28, 29]. Hydrogen comes from methane pyrolysis, alkaline electrolysis, steam electrolysis at the hubs (in both eras) and, for 950°C reactors, the sulfur–iodine cycle. Steam electrolysis uses 36.8 kWh of electricity per kg of hydrogen for the stack and balance of plant [30]. Its heat inputs come from a temperature–enthalpy balance per kilogram of hydrogen (supplementary section S8, table S16, fig. S7) for an 800°C stack at 0.5 MPa and 80% steam utilisation. A recuperator heated by the streams leaving the stack superheats the steam, and their residual heat preheats the feed water, leaving 6.87 kWh of external heat per kg, needed at no more than 152°C, and 0.68 kWh per kg of electric topping, consistent with [30]. The external heat comes from the reactor's process-steam tier [31] or from electric boilers, never from heat pumps; recuperators (about USD 0.03 per kg of hydrogen) are added to the electrolyser capital charge. All costs are in 2026 US dollars at a 5% discount rate (range 4 to 8%).

### 2.4 Reactor hubs and technology alternatives

The reference hub has six 250 MWt pebble-bed modules feeding one turbine island, the layout planned for the HTR-PM600 [12]. Its heat is split in a cascade: 30% at the 750°C top tier for methane preheat, 7.5% as process steam for biocrude upgrading and steam raising for electrolysis, 10% for drying, the rest to a turbine whose low-grade heat goes to greenhouses and recirculating aquaculture. Module cost follows Wright's law [32],

$$k(n) = k_{\mathrm{FOAK}}\, n^{\log_2(1-\lambda)},$$

with a first-of-a-kind cost $k_{\mathrm{FOAK}}$ of USD 5,250 per kWe and a learning rate $\lambda$ of 8% in the central case (table S4a). Because fleet cost is not convex in fleet size, every published case is solved for every hub count from 0 to 1,500; Monte Carlo draws use a 25-hub grid, then single hubs.

We tested five hub technologies (table S4b): the HTR-PM high-temperature gas-cooled reactor (750°C), a 950°C very-high-temperature reactor, a thorium molten-salt reactor of the TMSR-LF1 lineage (700°C) [13], a sodium-cooled fast reactor of the CFR-600 lineage (550°C) [14] and the ACP100 light-water small modular reactor (about 320°C) [15]. Outlet temperature sets how much of the 8.3 kWh per kg of pyrolysis heat the reactor can supply as methane preheat; the rest is supplied electrically. Efficiencies and costs by type are assumptions.

### 2.5 Biomass, regional crops and fuel routes

Crop straw is limited to the collectable surplus implied by agronomic removal limits of 19 to 45% [33, 34]. China produces about 860 Mt of straw a year [34], and the model can use 272 Mt in tiered regional bins at USD 38 to 65 per dry tonne. Forestry and existing bamboo-stand residues add 100 Mt (table S5). New clumping bamboo is limited to 3.0 Mha of hill land in the south and southwest; China already has about 7 Mha of bamboo forest [35]. Hemp is limited to 2.0 Mha in Heilongjiang, Jilin, eastern Inner Mongolia, Yunnan, Shanxi and Gansu (table S6c). The straw bins are net of straw already used for feed, bedding, mushrooms and existing power plants. The nutrients and soil carbon removed with the biomass must be returned (section 2.6). Effects on soil structure and moisture and collection radii are not modelled, so we also test residue supply 25% and 50% lower (section 3.2).

The autonomous regions contribute specific crops (table S6a,b). Guangxi grows more than 60% of China's cassava and about 60% of its cane sugar [36, 37], and supplies cassava ethanol, molasses ethanol, bagasse and jatropha oil from hill slopes. Inner Mongolia, Xinjiang and Ningxia supply sweet sorghum and other crops on marginal land, and Xizang only grassland and forestry residues. Yak-dung biogas enters the gas balance rather than the liquid fuels. Used cooking oil (5 Mt per year) and woody oil crops supply hydroprocessed fuels.

Residues, bamboo, hemp stalks and sorghum bagasse are converted by hydrothermal liquefaction with hydrotreating, or by gasification and Fischer–Tropsch synthesis with added hydrogen. Starch and sugar ethanol becomes jet fuel through alcohol-to-jet. Conversion yields, hydrogen use, heat demand and jet-fuel fractions are those of the United States model, with Chinese capital costs [11]. Liquefaction splits its feed into biocrude, an aqueous phase (the process wastewater) and a solid hydrochar. The aqueous phase is not biochar: it holds most of the potassium and about half of the nitrogen in solution, with water-soluble organics. The model digests it anaerobically, which yields biomethane (0.35 MWh per t of feed, consistent with the 217–314 mL of methane per g of chemical oxygen demand measured for rice-straw liquefaction wastewater [38]) and a digestate from which nitrogen and potassium are recovered. The hydrochar carries most of the phosphorus and the most stable carbon.

### 2.6 Nutrient and soil-carbon balance

For each nutrient the linear programme requires that what is returned to the land, plus mineral fertiliser bought at Chinese farm-gate prices (USD 700, 2,600 and 1,000 per t of elemental N, P and K, equivalent to about USD 1,130 per t of P~2~O~5~ and 830 per t of K~2~O), is at least what is removed (table S20). Straw contents follow a national compilation for rice, wheat and maize straw: N 0.64–0.85%, P~2~O~5~ 0.27–0.53% and K~2~O 1.53–2.31% [39]. Returns come from digested liquefaction wastewater, hydrochar, gasifier ash, ethanol stillage and seaweed, with the partitioning and recovery shares in table S21; potassium goes almost entirely to the liquefaction aqueous phase [40]. Surplus recovered nutrients can be sold at 70% of fertiliser prices. Mineral fertiliser carries production emissions of 8, 2 and 0.5 t CO~2~e per t of N, P and K.

Soil carbon is balanced in the same way. The requirement is the carbon the removed biomass would have added to stable soil organic carbon had it stayed on the field: its carbon content times a humification coefficient of 0.15 for straw and grass and 0.10 to 0.12 for wood and bamboo. It can be met by the stable fractions of returned hydrochar (half its carbon), digestate (30%), seaweed (10%) and pyrolysis carbon spread as a soil amendment (90%). Pyrolysis carbon is inert and does not feed soil organisms, so at least half of the requirement must come from the biogenic sources. Two biological options can also add soil carbon and nutrients: winter legume green manure on up to 6.7 Mha of fields now fallow in winter, and compost from up to 50 Mt a year of livestock manure not now returned to fields (table S25). If no feasible solution replaces all the soil carbon, a gap is allowed at USD 500 per t of carbon and counted as an emission; it is an accounting entry, not material returned to soil, and no reported case uses it. A separate case requires the whole replacement to come from biological sources, with pyrolysis carbon not counted and no gap allowed. After gas, pyrolysis may run on biomethane from the digesters. These coefficients are assumptions with wide ranges: the Monte Carlo draws vary humification, hydrochar stability, fertiliser prices and the cost of green manure and compost, and stress cases test the balance itself (Table 2).

### 2.7 Offshore wind, seaweed and nearshore bioextraction

Eight mainland zones and one Taiwan Strait zone pair offshore wind with species already farmed in China (table S7): Saccharina japonica off Liaoning and Shandong, Pyropia and Gracilaria rotations off Jiangsu, Zhejiang and Fujian, Gracilaria and Ulva off Guangdong and Guangxi (the Beibu Gulf), and tropical red seaweeds off Hainan. China grew about 60% of the world's farmed seaweed in 2022 [17]. Seaweed is harvested by Grid Harvesters (fig. S6), solar-powered heads that cut and pump seaweed between the long-lines, and hauled by battery and wing-sail vessels, using the U.S. model's engineering screen [11]; harvesting at this scale has not been tested.

Separately, the model can farm seaweed in six nearshore zones where nitrate and phosphate are high (table S19). China's coastal waters worse than Grade IV lie mainly in Liaodong Bay, the Yangtze estuary, Hangzhou Bay and the Pearl River estuary [41]. Species follow each water's temperature range and proven farming: Saccharina japonica in winter and Gracilariopsis lemaneiformis in summer from Liaodong Bay to the clearer island waters of the Yangtze plume (the turbid inner estuary and Hangzhou Bay are excluded), with Gracilaria bailinae added for the Fujian summer, and the heat-tolerant G. bailinae [42] and G. tenuistipitata in the Pearl River estuary and Qinzhou Bay, which are too warm for kelp. Pyropia is not expanded on the Subei shoal, because Ulva fouling its rafts seeds the Yellow Sea green tides [43], and Ulva itself is not farmed. Tissue nitrogen is taken as 2.8 to 3.2% of dry weight, below the 3.71% mean for Chinese farms [44]. Harvests go to liquefaction or, washed and screened for heavy metals, to fields; farming costs USD 3,500 per ha per year, and the same Grid Harvesters, vessels and drones as offshore harvest and haul the crop. Removal of nitrogen and phosphorus from the water is unpaid in the central case; stress cases pay USD 10 or 30 per kg of N and three times as much per kg of P.

### 2.8 Petroleum comparator and emissions

The petroleum comparator prices the same 2050 services with the 2025 fuel mix at pre-tax prices. Retail gasoline and diesel caps set by the National Development and Reform Commission are converted to pre-tax prices by removing 13% value-added tax and the consumption tax of 1.52 yuan per litre on gasoline and 1.20 yuan per litre on diesel [45, 46]. In late 2025, 92-octane gasoline sold for about 6.85 yuan per litre. On 13 November 2026 it was 8.41 yuan per litre, after the 2026 Middle East conflict raised oil prices [47] (table S8). Late-2025 prices are the reference; November 2026 prices are 1.37 times higher. The break-even multiple is $m^* = C/P$, where $P$ is the petroleum cost at late-2025 prices; the saving is $1 - m^*$.

Emissions use well-to-wheel intensities for petroleum fuels and road gas, life-cycle intensities for each biofuel route and 1.5% upstream methane leakage for pyrolysis gas [48]. Pyrolysis carbon in products or soil, hydrochar and livestock methane reductions are not counted against transport emissions; the soil-carbon balance replaces soil carbon but is not credited as a removal. Emissions from mineral fertiliser production, digester methane slip (1% of the methane made) and any priced soil-carbon gap are counted.

### 2.9 Natural gas, fissile material, regions and food

A separate gas balance (supplementary section S9) tracks China's demand against domestic production from remaining technically recoverable conventional, tight, shale and coalbed-methane gas [49], pipeline imports rising to the land-import capacity targeted for 2030 and beyond [50], and liquefied natural gas imports up to a ceiling. Reactor fuel is accounted for at inventory level (section S10). We compare the heavy metal needed with China's uranium and thorium resources [51, 52]. Start-up fissile material is compared with plutonium in spent fuel [53, 54] and in China's military stock [55]. The food module allocates low-grade reactor heat to greenhouses, recirculating fish and shrimp farms and Asparagopsis tanks [56]. A cross-feed balance routes fish processing by-products to shrimp feed, shrimp by-products to fish feed, effluent nitrogen to Ulva and kelp to abalone and sea cucumbers (section S12).

### 2.10 Conditional uncertainty analysis

We drew 1,000 triangular parameter sets for each of three cases: least cost, 230 GW of offshore wind with seaweed, and after gas (table S10). The draws cover technology costs, the discount rate, reactor cost case, seaweed yields, biomass and ethanol prices, carbon-market size and value, vehicle costs, service growth, humification, hydrochar stability and fertiliser prices. Parameters are drawn independently, and the ranges are modelling assumptions. The share of draws in which the system is cheaper than petroleum is therefore a conditional sensitivity result, not a probability that China's transport costs will fall. Structural uncertainties, such as build rates, adoption, grid reinforcement and policy, are not sampled.

### 2.11 Stress tests and feasibility screens

Because independent draws understate the chance that several unfavourable outcomes occur together, we also solve deterministic stress cases (Table 2): car ownership costs with no electric advantage, USD 100 per year more, and the high derivation; a car stock of 350 or 500 million; no carbon co-product revenue (carbon goes to paid permanent storage), or commodity carbon markets only; residue supply 25% or 50% lower; at most 60 or 30 reactor hubs; transmission and firming costs 60 to 75% higher; two combinations; and variations of the nutrient and soil-carbon balance and of nearshore seaweed farming. The moderate combination joins no electric-car advantage, commodity carbon markets only, 25% less residue, high reactor costs and the tighter grid; the severe combination uses the high car-cost derivation and no carbon revenue instead. A build-rate screen compares the reactor modules and wind capacity that the solutions require each year with current Chinese construction. Life-cycle emissions are recomputed with wider boundaries: 25 g CO~2~e per kWh for all electricity, 3% upstream methane leakage, soil-carbon losses of 20 or 40 g CO~2~e per MJ of residue-derived fuel and 3 g CO~2~e per kWh of hub heat for reactor construction and fuel supply. A stylised wind-lull screen asks whether the inflexible transport load can be carried through a windless, overcast winter week when all flexible loads stop and reactor heat goes entirely to the turbines; any shortfall is priced as hydrogen-fired backup. That is a lower bound, so we also estimate plausible and high costs that add a reserve margin, hydrogen storage, replacement hydrogen production and transmission (supplementary section S16). Sensitivities set wind to zero, reduce reactor availability to 80%, size turbines for 60% of reactor heat or double the lull to 14 days. These screens are not an hourly dispatch, reserve or stability analysis and do not establish operational feasibility.

### 2.12 Use of artificial intelligence

Artificial Inventor/Synthetic Scientist V63 assisted with writing model code, collecting and checking input data, running analyses, preparing figures and drafting text. The authors reviewed all outputs and take responsibility for the content.

## 3 Results

### 3.1 The central least-cost system

The least-cost 2050 system costs USD 314.1 billion per year (Fig. 3A). The same services cost USD 400.2 billion with petroleum at late-2025 pre-tax prices and USD 547.0 billion at November 2026 prices. The saving against late-2025 prices is 21.5%, a break-even multiple of 0.78. Petroleum would have to fall 22% below late-2025 prices to match the system.

Final energy falls from 5,469 TWh in 2025 to 3,119 TWh in 2050 despite 15% more service (Fig. 1A). Electricity is 1,494 TWh and hydrogen for vehicles, ships and aircraft is 6.5 Mt; renewable liquids are 1,387 TWh, of which 615 TWh is jet fuel. Onshore wind supplies 994 TWh from 344 GW. In all, 221 reactor hubs (332 GW of heat) supply 971 TWh of electricity and the heat for 8.2 Mt of hydrogen from steam electrolysis and 8.4 Mt from methane pyrolysis, for biocrude upgrading and for drying. The optimizer builds no new solar, concentrated solar or offshore wind in this case: at the assumed costs, firmed solar (USD 61 per MWh) is dearer than the hubs and the best wind sites. Solar enters when reactor costs are high (section 3.6) or nuclear power is excluded.

Electricity, grids, charging, electric expressways and rail electrification cost USD 119 billion. Reactor hubs, hydrogen plants, natural gas and hydrogen delivery cost USD 93 billion. Land biofuels cost USD 97 billion, and the net extra cost of electric and fuel-cell vehicles and machines is USD 23 billion. Pyrolysis makes 25.2 Mt of carbon a year: 17.3 Mt earns USD 24 billion in capped markets for vehicle structures, battery anode graphite, tyre carbon black, specialty carbon and metallurgy, and 7.9 Mt goes unpaid to fields as a soil amendment (section 3.4). These values assume that pyrolysis carbon can be purified, graphitised or otherwise qualified for each use; section 3.2 shows the cost without them. Liquid fuels are expensive: the marginal liquid costs USD 210 per MWh, more than three times the pre-tax price of diesel, and every land-biomass tier in the model is used.

Well-to-wheel emissions fall from 2,074 Mt CO~2~e for petroleum in 2050 to 130 Mt, a reduction of 93.7% (Fig. 1B). Liquid fuels account for 83 Mt of what remains, mineral fertiliser for the nutrient balance 11 Mt and digester methane slip 2.8 Mt. Pyrolysis keeps carbon equivalent to 92 Mt CO~2~ in solid form, which we do not count as a further reduction. Little of it would stay out of the atmosphere for long: 6.3 Mt of carbon goes to products that last one product life, 7.0 Mt to tyre carbon black that is lost as wear particles or burned, and 4.0 Mt to electrodes and recarburiser that are oxidised in use. Only carbon placed in asphalt, concrete or permanent storage, none in this case, would count as durable storage; the carbon spread on fields replaces soil carbon lost with the residues rather than adding to it. A logistic transition starting in 2026 avoids about 29 Gt CO~2~e by 2050 (fig. S2). Widening the life-cycle boundary raises residual emissions (table S12): to 158 Mt with 25 g CO~2~e per kWh of electricity, 146 Mt with 3% methane leakage, 206 and 281 Mt if residue removal still lost 20 or 40 g per MJ of residue fuel despite the soil-carbon balance, and 334 Mt with all of these and reactor construction, a reduction of 84%. Soil carbon is the largest of these uncertainties; some studies estimate larger near-term losses from residue removal [57].

### 3.2 Conditional uncertainty and stress tests

Across 1,000 draws from the assumed ranges, the least-cost system had a median cost of USD 400 billion (5th to 95th percentile 273 to 558) and was cheaper than late-2025 petroleum in 54% of draws (Fig. 4). The median saving was 3.3% (-33 to 32), and 14% of draws saved at least 23%. At November 2026 prices the system was cheaper in 97% of draws. The median draw costs more than the central case because the assumed ranges extend further above central values than below. Cost was most sensitive to the net cost of battery-electric cars (Spearman ρ = 0.84), service growth (Spearman ρ = 0.42) and the net cost of battery-electric trucks (Spearman ρ = 0.17) (fig. S3). These shares describe the model's response to the assumed ranges, not the probability of an outcome, and they are conditional on one petroleum price; the break-even curve shows how they change with it (Fig. 4B).

The deterministic stress cases show which assumptions the result depends on (Table 2, fig. S5). The ownership cost of electric cars dominates. With no ownership advantage the saving falls to 12.2%; at USD 100 per year more than petrol cars it is 2.3%; and with the high derivation, which combines a dearer purchase, frequent battery replacement and a USD 300 insurance penalty, the system costs 38% more than petroleum. Removing carbon co-product revenue costs USD 26.7 billion (14.9% saving), and pyrolysis then runs mainly to supply soil carbon; commodity carbon markets alone give 16.1%. Combining USD 100 per year dearer electric cars with no carbon revenue makes the system 4.4% dearer than petroleum. Residue supply 25% and 50% lower gives savings of 13.9% and 2.8%, as the model replaces residues with more bamboo, hemp, energy crops and hub hydrogen. With half the residue, green manure and compost help replace the soil carbon. Limiting the fleet to 60 or 30 hubs costs little (19.6% and 18.9%), because pyrolysis, wind and, at 30 hubs, 244 GW of solar replace reactor heat and power; on an annual-cost basis reactor hubs lower cost but the result does not depend on them, although fewer hubs leave the system much less firm (section 3.2, wind-lull screen). Higher transmission and firming costs give 16.2%. The moderate combination costs USD 460 billion, 15% more than petroleum at late-2025 prices but 16% less at November 2026 prices; after gas it costs USD 486 billion. The severe combination costs USD 668 billion, above petroleum at either price.

The central solution needs 1,326 reactor modules of 250 MWt. Built from 2032 to 2050, that is about 70 modules, or 17 GW of heat, a year. China approved at least ten large reactors a year from 2022 to 2025 [58], about 12 GW of electric capacity, or roughly 32 GW of heat. The hub programme needs about 55% of that heat capacity but about 7 times as many units, so serial factory production of modules would have to be demonstrated first. The 344 GW of onshore wind needs about 14 GW a year until 2050, against 120 GW of wind added in China in 2025 [59], but it comes on top of wind built for other sectors. Firm supply from hubs and light-water reactors is 49% of electricity in the central case. In the wind-lull screen, the central system's hubs can deliver 123 GW against an inflexible load of 196 GW; with residual wind the shortfall is 45 GW (table S17), and hydrogen-fired backup would add at least USD 4.7 billion a year (1.5% of system cost). With no wind the shortfall rises to 73 GW (USD 7.5 billion; other variants in table S18). Without nuclear power it is 102 GW (USD 10.5 billion) and with at most 30 hubs 114 GW (USD 11.9 billion), so capping the hub fleet costs little on an annual basis but much in adequacy. These are lower bounds. Adding a 15% reserve margin, hydrogen storage, make-up hydrogen production and transmission gives a plausible central backup cost of USD 7.1 billion, which lowers the saving to 19.8%; a 14-day windless lull with dearer storage gives USD 31.5 billion and 13.7% (table S26). With at most 30 hubs the plausible saving is 14.6%.

### 3.3 Offshore wind and seaweed raise cost

Forcing half of each zone's large build-out, 230 GW of offshore wind with 28 Mt of dry seaweed, raises cost to USD 338.4 billion, a saving of 15.4% (median -3% across draws, cheaper in 44%). The full 460 GW build costs USD 369.0 billion (7.8% saving). Seaweed fuel costs USD 180 to 260 per MWh by zone. It is cheapest off Shandong, Liaoning and Fujian, where Saccharina yields are high, and dearest off Jiangsu, where nori yields are low (table S7, fig. S1). On cost grounds alone, though, offshore wind with seaweed does not pay. It would need benefits the model does not price, such as supply diversity or fishery co-production. Nearshore farming in nutrient-polluted bays is a different case (section 3.4).

### 3.4 Nutrients, soil carbon and eutrophic coastal waters

Harvesting the least-cost biomass removes 2.93 Mt of nitrogen, 0.62 Mt of phosphorus and 4.98 Mt of potassium a year (Fig. 9A, table S22). Returned process streams replace 53% of the nitrogen, 94% of the phosphorus and 91% of the potassium; the rest, 1.38 Mt of N, 0.04 Mt of P and 0.46 Mt of K, is bought as mineral fertiliser. Digested liquefaction wastewater is the main return. It carries 1.25 Mt of nitrogen and 3.8 Mt of potassium, and its digestion yields 144 TWh of biomethane (12.9 bcm), worth USD 4.6 billion a year at the gas price. Hydrochar carries most of the returned phosphorus (0.45 Mt).

Left on the fields, the residues would have added 27.4 Mt of stable carbon a year to soils (Fig. 9B, table S23). Returned hydrochar supplies 14.8 Mt and digestate 5.5 Mt. All of the hydrochar is returned, and pyrolysis carbon, cheaper at the margin than more biogenic carbon, supplies the rest: 7.9 Mt of it supplies 7.1 Mt, so the biogenic share is 74%, above its 50% floor. The soil-carbon balance therefore changes the hydrogen mix. Without the balance, pyrolysis makes 5.8 Mt of hydrogen from 33 bcm of gas with 241 hubs; with it, 8.4 Mt from 48 bcm with 221 hubs. In all, the nutrient and soil-carbon balance costs USD 5.1 billion a year, of which USD 3.7 billion is for nutrients; without it the system would cost USD 309.0 billion (22.8% saving). Pyrolysis carbon is inert and may not do what organic matter does for soil organisms and structure, so we also require the whole replacement to come from biological sources. The optimizer then returns 100% of the hydrochar, grows green manure on 6.1 Mha and spreads 50 Mt of manure compost, while still harvesting 382 Mt of residues; the system costs USD 315.7 billion (21.1% saving) with 5.8 Mt of pyrolysis hydrogen. Compost is the decisive option: without it, even the full green-manure area and less residue harvest cannot close the balance at full liquid demand, and 385 TWh of liquids (28%) could not be supplied domestically. Higher humification, less stable hydrochar, dearer fertiliser and doubled compost and green-manure costs give USD 315.4, 314.6, 314.7 and 319.8 billion.

After gas the balance closes without fossil carbon. Pyrolysis runs on 13.1 bcm a year of biomethane from the digesters and makes 2.3 Mt of hydrogen, and hydrochar, green manure (5.7 Mha) and compost (50 Mt) supply the soil carbon. Forbidding pyrolysis after gas raises the cost to USD 342.1 billion.

The six nearshore zones cover 3,600 km² (Fig. 9C, table S24). Farmed in full, they produce 6.2 Mt of dry seaweed and remove 184 kt of nitrogen and 25 kt of phosphorus a year, 2.5 and 2.6 times the removal by China's seaweed farms in the mid-2010s [44]. The seaweed costs USD 182 to 242 per t and, liquefied, yields 12 TWh of fuel. Harvested by Grid Harvesters, the seaweed is cheap enough that the least-cost solution farms 1.4 Mt in the gas era and 5.3 Mt after gas, and farming every zone in full adds only USD 0.1 billion a year. A payment of USD 10 per kg of nitrogen removed raises the saving to 22.1%, and USD 30 per kg to 23.4%. The seaweed's value is as liquefaction feed whose wastewater returns nitrogen and phosphorus from polluted bays to farmland.

### 3.5 Natural gas for pyrolysis and hydrogen after gas

Pyrolysis runs only as far as its solid carbon has a use. The capped carbon markets and the soil-carbon balance together take 25.2 Mt of carbon, which fixes pyrolysis at 8.4 Mt of hydrogen, 51% of the hydrogen made; beyond that, at China's gas price of USD 9.3 per MMBtu, steam electrolysis at the hubs is cheaper. Pyrolysis would then consume 48 bcm of natural gas a year by 2050, 11% of China's 2025 consumption (Fig. 6). With high reactor costs the optimizer uses more pyrolysis (16.6 Mt of hydrogen) and fewer hubs. In our gas balance, demand first exceeds domestic production, pipeline imports and a 140 bcm ceiling on liquefied gas imports in 2141 with the programme, against 2144 without it. With uncertain resources the date ranges from 2100 to 2175. The gas date is less binding than the import share: total imports reach 37% of supply.

In the gas era the system still burns fossil gas for pyrolysis and for part of pipeline compression. After gas it uses none: compressors are electric, steam electrolysis at the hubs makes 14.1 Mt of hydrogen and pyrolysis of biomethane 2.3 Mt (section 3.4). The system then costs USD 325.8 billion with 268 hubs and 344 GW of wind, a saving of 18.6% (median -1% across draws, cheaper in 49%). Loss of pyrolysis carbon revenue explains most of the USD 11.7 billion increase. Emissions fall to 99 Mt (95.2%). With high steam-electrolysis electricity use (48 kWh per kg) the cost is USD 333.6 billion.

### 3.6 Reactor technologies and start-up fuel

The reactor comparison is a prospective sensitivity: the headline results use the HTR-PM, the only one of the five in commercial operation, and none of the conclusions above depends on the other four. Under those assumptions, the thorium molten-salt reactor has the lowest cost of the five technologies in both eras (Fig. 5A and table S4b): USD 298 billion in the gas era and USD 307 billion after gas. This reflects its assumed high turbine efficiency and low fuel-cycle cost, the least certain of our inputs. Among reactor parameters, capital cost matters most: low and high cost cases give USD 293.6 and 328.3 billion. At high cost the optimizer builds only 12 hubs and adds 254 GW of solar. Without any nuclear power, wind, solar and concentrated solar supply everything for USD 367.5 billion, a saving of 8.2%, with steam electrolysis heated by electric boilers and superheaters; with alkaline electrolysis only it is USD 374.4 billion (6.5%).

A speculative closed-cycle thorium molten-salt fleet, with no gas, is cheapest with 423 hubs at USD 302.3 billion (24.5% saving). It builds no wind or solar, so restricting it to nuclear power gives the same solution. With 25% higher capital and USD 9 per MWh of heat for fuel recycling, the cost is USD 328.2 billion. The fleet needs 231 t of heavy metal a year. China's identified thorium of about 100,000 t [52] would last about 430 years at that rate, and a reported one million tonnes at Bayan Obo in Inner Mongolia about 4,300 years [60]. Start-up material is the constraint (Fig. 5B). A thermal-spectrum molten-salt fleet of 254 GWe would need about 380 t of fissile material. As high-assay low-enriched uranium, that takes about 82,000 t of natural uranium. A sodium fast fleet of 133 GWe would need about 1,330 t of plutonium, 1.2 times the plutonium projected in China's spent fuel by 2050 [54]. Military plutonium, estimated at 2.9 ± 0.6 t [55], could start about 0.3 GWe of fast reactors. Its release through arms reductions would matter little for energy supply.

### 3.7 Autonomous regions, Hong Kong, Macau and Taiwan

The regional results are screening allocations of the national solution by fixed shares, not a transmission-constrained regional optimisation. On that basis, all five autonomous regions supply more renewable liquids than their own 2050 demand (Fig. 7A). Inner Mongolia supplies 101 TWh from maize stover, sweet sorghum, Jerusalem artichoke and hemp, about 4.0 times its demand. Xinjiang supplies 83 TWh from cotton stalks, sweet sorghum and oilseed residues (3.8 times), and Guangxi 61 TWh from cassava, molasses, bagasse, jatropha and bamboo (1.7 times). Ningxia supplies 11 TWh and Xizang 4.1 TWh, 2.2 and 1.2 times their small demands. Together the five regions cut well-to-wheel emissions from 189 to 12 Mt CO~2~e per year (Fig. 7B).

Hong Kong is dominated by aviation and bunker fuel. Of its 189 TWh of 2050 transport demand, 128 TWh are liquids that must come from the mainland. Taiwan, as a separate island system, has little land biomass and imports 60 of its 69 TWh of liquids in the least-cost case at an assumed USD 170 per MWh. Its system costs USD 17.9 billion against USD 15.6 billion for petroleum, 14% more. Without nuclear power it costs USD 20.5 billion. Imported liquids account for USD 10 billion of Taiwan's cost; at about USD 130 per MWh instead of 170, Taiwan's system would match petroleum.

### 3.8 Food and cross-feeding

Low-grade heat from the least-cost hubs (267 TWh) could heat 75,000 ha of greenhouses producing 30.0 Mt of vegetables, and recirculating farms producing 3.0 Mt of fish and 2.0 Mt of shrimp. Drying heat could dry 80 Mt of grain and 0.5 Mt of food seaweed (Fig. 8A). In the cross-feed balance (Fig. 8B), fishmeal from fish by-products, shrimp meal, insect meal grown on greenhouse waste, and Ulva grown on effluent nitrogen meet 51% of the marine protein needed in fish and shrimp feed and 23% of total feed protein, recover 78 kt of nitrogen, and displace 484 kt of imported fishmeal. Asparagopsis grown with reactor heat could reduce enteric methane by up to 58 Mt CO~2~e per year, a scenario multiplier subject to dose–response uncertainty [61, 62]. None of this enters the transport cost. Valued at USD 8 per MWh before distribution costs, the 193 TWh used would be worth about USD 1.5 billion a year.

### 3.9 Comparison with the United States

The China least-cost saving of 21.5% is close to the 23.2% reported for the United States [11]. But the United States model's heavy-truck ratios divided kWh per mile by MJ per mile, understating heavy-truck electricity by a factor of 3.6. With corrected ratios and nothing else changed, the United States least-cost saving falls to 12.0%, and its post-gas saving from 16.4% to 4.7% (section S15). With the United States' uncorrected ratios, the China saving would be 37.2%. Measured consistently, the China system's saving is about twice that of the United States. Cheaper wind, solar and reactors, a lower discount rate, cheap electric cars and larger residue supplies outweigh China's lower pre-tax fuel prices and costlier gas. The United States code also allowed steam electrolysis only after gas; in China that restriction would raise cost by USD 0.6 billion and gas use from 48 to 94 bcm a year (section S15).

## 4 Discussion

In the central case, China could replace petroleum in transport for about one-fifth less than petroleum at late-2025 prices, and for more than 40% less at November 2026 prices. This is a favourable modelled scenario, not a demonstrated transition. The saving depends above all on electric cars costing no more to own than petrol cars, and to a lesser degree on carbon co-product markets that do not yet exist at this scale and on residue collection on a scale not yet attempted. In the conditional Monte Carlo analysis the median saving is only 3.3%, and the system is dearer than late-2025 petroleum in about 46% of draws, but cheaper at November 2026 prices in 97% of draws. The central saving is not reliability-adjusted: with plausible wind-lull backup it falls to 19.8%, and to 13.7% with a high estimate. Most of the saving comes from electrifying road transport, which China is already doing faster than other large economies [6–8]. The more novel elements play supporting roles. Reactor hubs supply firm electricity, process heat and hydrogen, from steam electrolysis and from pyrolysis, whose carbon finds buyers or replaces soil carbon. The autonomous regions' crops and China's crop residues supply the liquids that aviation, shipping and off-road machinery still need.

The binding resources are liquids and start-up fissile material, not electricity. Every land-biomass tier is used, and the marginal liquid costs about USD 210 per MWh. Better conversion yields, cheaper residue collection or lower liquid demand through further electrification of ships and machines would therefore lower cost most. Pyrolysis would add about 48 bcm a year to China's gas demand, and because it is limited by uses for its carbon rather than by gas, it brings the first gas shortfall forward by only 3 years. Import dependence matters more than the date: imports already approach 37% of supply without the programme. After gas, steam electrolysis, biomethane pyrolysis and biological soil carbon keep the system cheaper than petroleum. A closed thorium cycle would make the fuel supply effectively unlimited, but it is constrained by start-up fissile material and is not yet demonstrated beyond the 2 MWt TMSR-LF1, which reached a conversion ratio of about 0.1 [13]. Weapons plutonium is too small to matter: the energy case for a breeder fleet does not depend on it.

Returning the nutrients and soil carbon that harvesting removes costs little, about USD 5.1 billion a year, because liquefaction already concentrates them in streams that can go back to fields: the wastewater holds potassium and nitrogen, and the hydrochar phosphorus and stable carbon. Inert pyrolysis carbon is the cheapest way to replace stable soil carbon, but the result does not depend on it: replacing soil carbon from biological sources alone costs USD 1.6 billion more, provided manure compost is available at the assumed scale. Without compost the balance closes only by harvesting less residue and supplying less liquid fuel. Whether pyrolysis carbon behaves in soil like biochar, and whether hydrochar, digestate and compost maintain fertility at this scale, are field questions the model cannot answer. Nearshore seaweed in nutrient-polluted bays is close to break-even as fuel feed and would remove about 2.5 times the nitrogen that China's seaweed farms now remove. It is better seen as a water-quality measure that also yields fuel than as an energy resource.

The autonomous regions export liquid fuels and power to the eastern provinces and the special administrative regions. Taiwan shows the limits of island systems: with little land biomass, liquid fuels must be imported or made from seaweed, at more than petroleum's cost. These results carry no judgement on governance.

Several limits apply. The model balances energy annually and cannot show hourly adequacy, storage, ramping, transmission or system stability; the firm-share and solar-share constraints are surrogates, and the build-rate screen is not a deployment model. Construction rates, permitting, siting, biomass logistics and the qualification of pyrolysis carbon for battery and fibre markets are not modelled. Nutrient partitioning, humification and amendment stability coefficients are assumptions, soil-carbon losses beyond the modelled balance are treated only as a life-cycle boundary sensitivity, and the Monte Carlo draws are independent, so correlated adverse outcomes are represented only by the stress cases. Biomass availability, conversion yields at national scale, jet-fuel certification, reactor costs and learning are uncertain. Many baseline splits are assumptions (table S1), and petroleum prices are historical snapshots, not forecasts.

## 5 Conclusions

An open annual model of a petroleum-free transport system for mainland China, its five autonomous regions, Hong Kong and Macau finds a central least-cost 2050 system costing USD 314.1 billion per year, 21.5% less than petroleum at late-2025 pre-tax prices, with a cut of 93.7% in well-to-wheel emissions (84% with the widest life-cycle boundary tested). The result is conditional: the median saving across draws is 3.3%, and plausible backup for wind lulls lowers the central saving to 19.8%. It holds if battery-electric cars cost no more to own than petrol cars; without that advantage the saving falls to 12.2%, and moderately adverse assumptions taken together make the system dearer than petroleum at late-2025 prices but not at November 2026 prices. Reactor hubs lower cost and, more importantly, firm the system: with at most 30 hubs the saving is still 18.9% on an annual basis, but backup for wind lulls then costs at least USD 11.9 billion a year. Hydrogen comes from pyrolysis and steam electrolysis at the hubs; pyrolysis, limited by markets and soil uses for its carbon, needs about 48 bcm of gas a year, and after gas the central system remains 18.6% cheaper than petroleum. Returning the nutrients and stable soil carbon that harvesting removes costs about USD 5.1 billion a year. Replacing soil carbon from biological sources alone, with green manure and manure compost, costs USD 1.6 billion more. Seaweed farmed in China's eutrophic bays and harvested by Grid Harvesters could remove 184 kt of nitrogen a year at little net cost. A thorium molten-salt reactor has the lowest cost under assumed inputs, but start-up fissile material limits a breeder fleet, and weapons plutonium is negligible for this purpose. The autonomous regions are net suppliers of renewable fuel; Taiwan's island system costs more than petroleum unless imported renewable liquids become cheaper. Corrected for a unit error in heavy-truck energy, the related United States model gives about half China's saving. The results establish annual resource adequacy, not operational feasibility. Hourly dispatch, reserves and transmission, deployment trajectories, residue sustainability at field scale, carbon-product qualification, field trials of hydrochar, digestate and pyrolysis-carbon amendments, and demonstration of biomass conversion, seaweed harvesting and advanced reactors at scale are the next steps.

## Nomenclature

| Symbol | Meaning | Unit |
|:--|:--|:--|
| $C$ | Annual cost of the transport energy system in 2050 | billion USD (2026) per year |
| $c_i$ | Unit cost of activity $i$ | USD per unit |
| $x_i$ | Level of activity $i$ (generation, production, purchase or conversion) | TWh, Mt or Mha per year |
| $F$ | Costs fixed by the 2050 end-use mix | billion USD per year |
| $P$ | Cost of the same services with petroleum at late-2025 pre-tax prices | billion USD per year |
| $m^*$ | Break-even multiple of late-2025 petroleum prices, $C/P$ | dimensionless |
| $k(n)$ | Overnight cost of the $n$-th reactor module | USD per kWe |
| $k_{\mathrm{FOAK}}$ | First-of-a-kind module cost | USD per kWe |
| $\lambda$ | Learning rate per doubling of modules built | dimensionless |

## Acknowledgements

Artificial Inventor/Synthetic Scientist V63 assisted with writing model code, collecting and checking input data, running analyses, preparing figures and drafting text (section 2.12). The authors reviewed all outputs and take responsibility for the content.

## Funding

This work received no funding.

## Conflict of interest statement

None declared.

## Data availability

All model code, inputs, outputs, tests and figure scripts (release CN v1.6.2, with a manifest of file hashes, a check, `cn_release_check.py`, that re-solves the headline cases and compares them with the submitted numbers, and an independent audit of unit conversions, `cn_number_audit.py`) are deposited in a GitHub repository as release tag CN-v1.6.2, which will be public, with an archived DOI, before publication; the repository link is given to the editor on the title page and withheld here for double-anonymized review. The repository runs as a flat folder and `bash run_all.sh 1000` regenerates every result.

## References

[1] Global Carbon Project. Global Carbon Budget 2025: key findings. 13 November 2025. https://globalcarbonbudget.org/ (22 November 2026, date last accessed).

[2] Climate Analytics. 1.5°C national pathways explorer: China, transport. 2025. https://1p5ndc-pathways.climateanalytics.org/countries/china/ (22 November 2026, date last accessed).

[3] International Energy Agency. Oil demand for fuels in China has reached a plateau. Paris: IEA, 2025. https://www.iea.org/commentaries/oil-demand-for-fuels-in-china-has-reached-a-plateau (22 November 2026, date last accessed).

[4] China Association of Petroleum Enterprises. China's energy structure continues to optimize and adjust: 2025 consumption of refined oil and natural gas (as reported by SunSirs, 2026). https://www.sunsirs.com/uk/detail_news-32560.html (22 November 2026, date last accessed).

[5] ICIS. China policies reshape gas demand outlook across transport, industry and heating (Hellenic Shipping News, 2026). https://www.hellenicshippingnews.com/?p=1139868 (22 November 2026, date last accessed).

[6] Ministry of Public Security of China. National motor vehicle ownership reached 469 million at end-2025 (as reported by China EV Home, 26 January 2026). https://chinaevhome.com/2026/01/26/chinas-nev-fleet-tops-43-9-million-by-end-2025-penetration-exceeds-12-1/ (22 November 2026, date last accessed).

[7] International Council on Clean Transportation. Zero-emission medium- and heavy-duty vehicle market in China: a 2025 update. Washington, DC: ICCT, 2026. https://theicct.org/publication/zero-emission-medium-and-heavy-duty-vehicle-market-in-china-a-2025-update-may26/ (22 November 2026, date last accessed).

[8] S&P Global Commodity Insights. Chinese refiners urged to streamline with domestic fuel demand at risk. 9 September 2025. https://www.spglobal.com/energy/en/news-research/latest-news/crude-oil/090925-appec-chinese-refiners-urged-to-streamline-with-domestic-fuel-demand-at-risk (22 November 2026, date last accessed).

[9] Davis SJ, Lewis NS, Shaner M et al. Net-zero emissions energy systems. Science 2018;360:eaas9793. https://doi.org/10.1126/science.aas9793

[10] Jaramillo P, Kahn Ribeiro S, Newman P et al. Transport. In: Shukla PR, Skea J, Slade R et al. (eds). Climate Change 2022: Mitigation of Climate Change. Cambridge: Cambridge University Press, 2022, 1049–1160. https://doi.org/10.1017/9781009157926.012

[11] Bily JK, Pahl C, Valdes Bacallao P. Reactor heat, electrification and renewable fuels could replace U.S. transport petroleum at lower annual cost (model version 8.4). Unpublished manuscript, withdrawn by the authors; supplied confidentially to the editor. Model code: https://github.com/bcjohnjr/United-States-Nuclear-Renewable-Transportation-Decarbonization (22 November 2026, date last accessed).

[12] World Nuclear News. China's demonstration HTR-PM enters commercial operation. 6 December 2023. https://www.world-nuclear-news.org/articles/chinese-HTR-PM-Demo-begins-commercial-operation (22 November 2026, date last accessed).

[13] World Nuclear News. Chinese molten salt reactor achieves conversion of thorium-uranium fuel. November 2025. https://world-nuclear-news.org/articles/chinese-msr-achieves-conversion-of-thorium-uranium-fuel (22 November 2026, date last accessed).

[14] Zhang H. China started operation of its first CFR-600 breeder reactor. International Panel on Fissile Materials blog, 15 December 2023. https://fissilematerials.org/blog/2023/12/china_started_operation_o.html (22 November 2026, date last accessed).

[15] World Nuclear News. Chinese SMR completes non-nuclear steam start up test. December 2025. https://world-nuclear-news.org/articles/chinese-smr-completes-non-nuclear-steam-start-up-test (22 November 2026, date last accessed).

[16] CGTN. China leads global offshore wind with 78% of new capacity in 2025. 18 June 2026. https://news.cgtn.com/news/2026-06-18/China-leads-global-offshore-wind-with-78-of-new-capacity-in-2025-1O4AKaDVF60/p.html (22 November 2026, date last accessed).

[17] Liu J, Liu W, Xia J. Perplexity and choice: challenges and future development of laver cultivation in Jiangsu Province, China. Front Mar Sci 2025;12:1526933. https://doi.org/10.3389/fmars.2025.1526933

[18] China Daily. Zhoushan bonded bunker fuel supply reaches 8.03 million tonnes in 2025. 7 January 2026. https://regional.chinadaily.com.cn/ezhejiang/zhoushan/2026-01/07/c_1153389.htm (22 November 2026, date last accessed).

[19] S&P Global Commodity Insights. Cathay Pacific H1 2024 passenger traffic rises 36% on year; Hong Kong's jet fuel demand bolstered. 7 August 2024. https://www.spglobal.com/energy/en/news-research/latest-news/crude-oil/080724-cathay-pacific-h1-2024-passenger-traffic-rises-36-on-year-hong-kongs-jet-fuel-demand-bolstered (22 November 2026, date last accessed).

[20] U.S. Energy Information Administration. Taiwan analysis brief. Washington, DC: EIA, April 2026. https://www.eia.gov/international/content/analysis/countries_short/Taiwan/Taiwan.pdf (22 November 2026, date last accessed).

[21] Bloomberg News. China's EV boom saddles its auto insurers with chronic losses (average new-energy vehicle price 158,900 yuan in August 2025, about 90% of the price of fuel cars, Autohome Research Institute). Carrier Management, 22 September 2025. https://www.carriermanagement.com/news/2025/09/22/279683.htm (22 November 2026, date last accessed).

[22] International Council on Clean Transportation. Evaluating Electric Vehicle Costs and Benefits in China in the 2020–2035 Time Frame. Washington, DC: ICCT, 2021. https://theicct.org/sites/default/files/publications/EV-costs-benefits-china-EN-apr2021.pdf (22 November 2026, date last accessed).

[23] International Council on Clean Transportation. Cheaper than you think, sooner than you think: the cost of owning an electric car. ICCT staff blog, July 2026. https://theicct.org/cheaper-than-you-think-sooner-than-you-think-jul26/ (22 November 2026, date last accessed).

[24] Caixin Global. China's average new-energy vehicle insurance premium falls. 2 April 2026. https://www.caixinglobal.com/2026-04-02/chinas-average-new-energy-vehicle-insurance-premium-falls-102430278.html (22 November 2026, date last accessed).

[25] CNBC. China's flood of new electric cars cost 20% more to insure than fuel-powered cars (S&P Global Ratings). 2022, syndicated by NBC DFW. https://nbcdfw.com/news/business/money-report/chinas-flood-of-new-electric-cars-cost-20-more-to-insure-than-fuel-powered-cars/3081968 (22 November 2026, date last accessed).

[26] Virtanen P, Gommers R, Oliphant TE et al. SciPy 1.0: fundamental algorithms for scientific computing in Python. Nat Methods 2020;17:261–72. https://doi.org/10.1038/s41592-019-0686-2

[27] Huangfu Q, Hall JAJ. Parallelizing the dual revised simplex method. Math Program Comput 2018;10:119–42. https://doi.org/10.1007/s12532-017-0130-5

[28] International Renewable Energy Agency. Renewable Power Generation Costs in 2025. Abu Dhabi: IRENA, 2026. https://www.irena.org/ (22 November 2026, date last accessed).

[29] State Grid Energy Research Institute. China New Energy Power Generation Analysis Report 2026 (as reported by China Daily, 13 June 2026). https://www.chinadaily.com.cn/a/202606/13/WS6a2cad00a310986e2b45fb8c.html (22 November 2026, date last accessed).

[30] Wendt DS, Knighton LT, Boardman RD. High Temperature Steam Electrolysis Process Performance and Cost Estimates. INL/RPT-22-66117, Revision 0. Idaho Falls, ID: Idaho National Laboratory, 2022. https://inldigitallibrary.inl.gov/sites/sti/sti/Sort_60759.pdf (22 November 2026, date last accessed).

[31] World Nuclear News. China's demonstration HTR-PM enters commercial operation. 6 December 2023. https://world-nuclear-news.org/articles/chinese-htr-pm-demo-begins-commercial-operation (22 November 2026, date last accessed).

[32] Wright TP. Factors affecting the cost of airplanes. J Aeronaut Sci 1936;3:122–8. https://doi.org/10.2514/8.155

[33] Shi W, Tan T, Fang Y et al. Quantifying reasonable straw removal rate to achieve food security, bioenergy transition and climate mitigation in China. Resour Conserv Recycl 2025;215:108114. https://doi.org/10.1016/j.resconrec.2024.108114

[34] RMI. Unlocking the Value of Crop Straw in China. Basalt, CO: RMI, 2026. https://rmi.org/insight/unlocking-the-value-of-crop-straw-in-china (22 November 2026, date last accessed).

[35] China Daily. China pushes for bamboo to replace plastics (National Forestry and Grassland Administration: 7.01 million hectares of bamboo forest). 10 February 2025. https://govt.chinadaily.com.cn/s/202502/10/WS67a9c1d4498eec7e1f72ee7a/china-pushes-for-bamboo-to-replace-plastics.html (22 November 2026, date last accessed).

[36] Tian Y, Jin S, Lin X. Present situation and future potential of cassava in China. 2017. FAO AGRIS record 64746b6b79cbb2c2c1afb257. https://agris.fao.org/search/en/records/64746b6b79cbb2c2c1afb257 (22 November 2026, date last accessed).

[37] Bernama. "Double the sweetness": a new chapter for Guangxi's sugar industry. 27 August 2025. https://www.bernama.com/en/press/news.php?id=2461226 (22 November 2026, date last accessed).

[38] Chen H, Zhang C, Rao Y et al. Methane potentials of wastewater generated from hydrothermal liquefaction of rice straw: focusing on the wastewater characteristics and microbial community compositions. Biotechnol Biofuels 2017;10:140. https://doi.org/10.1186/s13068-017-0830-0

[39] Li T, Wang Y, Wang J et al. Nutrient resource quantity from main grain crop straw incorporation and its enlightenment on chemical fertilizer reduction in wheat production in China. Sci Agric Sin 2020;53:4835–54. https://doi.org/10.3864/j.issn.0578-1752.2020.23.010

[40] Conti F, Toor SS, Pedersen TH et al. Biocrude production and nutrients recovery through hydrothermal liquefaction of wastewater irrigated willow. Biomass Bioenergy 2018;118:24–31.

[41] Ministry of Ecology and Environment of China. 2023 Bulletin on the State of Marine Ecology and Environment of China (as summarised by China Water Risk, 25 June 2024). https://cwrrr.org/resources/analysis-reviews/2023-marine-ecology-environment-status-review/ (22 November 2026, date last accessed).

[42] Huang Y, Cui J, Wang S et al. Transcriptome analysis reveals the molecular mechanisms of adaptation to high temperatures in Gracilaria bailinae. Front Plant Sci 2023;14:1125324. https://doi.org/10.3389/fpls.2023.1125324

[43] Han H, Fan S, Song W et al. The contribution of attached Ulva prolifera on Pyropia aquaculture rafts to green tides in the Yellow Sea. Acta Oceanol Sin 2020;39:101–6. https://doi.org/10.1007/s13131-019-1452-0

[44] Xiao X, Agusti S, Lin F et al. Nutrient removal from Chinese coastal waters by large-scale seaweed aquaculture. Sci Rep 2017;7:46613. https://doi.org/10.1038/srep46613

[45] International Energy Agency. Fuel excise tax (China). Policies database, 2023. https://www.iea.org/policies/16905-fuel-excise-tax (22 November 2026, date last accessed).

[46] National Development and Reform Commission, via Xinhua. Gasoline and diesel prices cut (12 November 2026). https://www.news.cn/fortune/20261112/7ce2362ff2814b06a05934ed9ba0322e/c.html (22 November 2026, date last accessed).

[47] IT Home / ifeng. National average retail prices of 92-octane gasoline after each 2026 adjustment. 12 November 2026. https://tech.ifeng.com/c/8xzeMnpmEw0 (22 November 2026, date last accessed).

[48] Alvarez RA, Zavala-Araiza D, Lyon DR et al. Assessment of methane emissions from the U.S. oil and gas supply chain. Science 2018;361:186–8. https://doi.org/10.1126/science.aar7204

[49] Shell International, Development Research Center of the State Council. China's natural gas resource potential and production trends. In: China's Gas Development Strategies. Advances in Oil and Gas Exploration & Production. Cham: Springer, 2017. https://doi.org/10.1007/978-3-319-59734-8_7

[50] Kpler. China's 15th Five-Year Plan lifts 2027 LNG imports by 0.5 mt, with little impact on Asian prices. 2026. https://www.kpler.com/blog/chinas-15th-five-year-plan-lifts-2027-lng-imports-by-0-5-mt-with-little-impact-on-asian-prices (22 November 2026, date last accessed).

[51] OECD Nuclear Energy Agency, International Atomic Energy Agency. Uranium 2024: Resources, Production and Demand. NEA No. 7683. Paris: OECD Publishing, 2025.

[52] International Atomic Energy Agency. World Thorium Occurrences, Deposits and Resources. IAEA-TECDOC-1877. Vienna: IAEA, 2019.

[53] Stimson Center. Spent nuclear fuel in China: fact sheet. 2020. https://www.stimson.org/2020/spent-nuclear-fuel-china/ (22 November 2026, date last accessed).

[54] World Nuclear Transport Institute. Development of civil nuclear power in China (cumulative spent fuel 11,000 tHM at end-2024). November 2025. https://www.wnti.co.uk/wp-content/uploads/2025/12/WNTI-Rep-Update-China.pdf (22 November 2026, date last accessed).

[55] International Panel on Fissile Materials. The 2025 update on fissile material stocks. June 2026. https://fissilematerials.org/blog/2026/06/the_2025_update_on_fissil.html (22 November 2026, date last accessed).

[56] Gupta S, Makridis P, Henry I et al. Recent developments in recirculating aquaculture systems: a review. Aquac Res 2024;2024:6096671. https://doi.org/10.1155/2024/6096671

[57] Liska AJ, Yang H, Milner M et al. Biofuels from crop residue can reduce soil carbon and increase CO~2~ emissions. Nat Clim Change 2014;4:398–401. https://doi.org/10.1038/nclimate2187

[58] World Nuclear News. Ten new reactors approved in China. 28 April 2025. https://world-nuclear-news.org/articles/ten-new-reactors-approved-in-china (22 November 2026, date last accessed).

[59] Global Wind Energy Council. Global Wind Report 2026 (as reported by Eco-Business: China leads global wind power installations, as additions surge 40 per cent in 2025). April 2026. https://www.eco-business.com/news/china-leads-global-wind-power-installations-as-additions-surge-40-per-cent-in-2025/ (22 November 2026, date last accessed).

[60] South China Morning Post. China's thorium survey finds 'endless' energy source right under our feet. 2025. https://www.scmp.com/news/china/science/article/3300360/chinas-thorium-survey-finds-endless-energy-source-right-under-our-feet (22 November 2026, date last accessed).

[61] Roque BM, Venegas M, Kinley RD et al. Red seaweed (Asparagopsis taxiformis) supplementation reduces enteric methane by over 80 percent in beef steers. PLoS One 2021;16:e0247820. https://doi.org/10.1371/journal.pone.0247820

[62] Kebreab E, Pressman EM, Ramirez-Agudelo JF et al. A meta-analysis of effects of seaweed and other bromoform-containing feed ingredients on methane production, yield, and intensity in cattle. J Dairy Sci 2025;108:11071–93. https://doi.org/10.3168/jds.2025-26960

## Figure captions

**Fig. 1.** Transport energy and emissions. (A) Final energy in 2025 by fuel and in the 2050 least-cost system by carrier, for mainland China, Hong Kong and Macau. (B) China's fossil CO~2~ emissions in 2025 (all sectors; 32% of 38.1 Gt [1]) compared with transport well-to-wheel emissions in 2025, the 2050 petroleum baseline and the 2050 system before and after natural gas.

Alt text: Two-panel chart. Left: stacked bars show 2025 transport final energy of about 5,470 TWh, mostly diesel and gasoline, falling to about 3,119 TWh in 2050, made up of electricity, renewable liquids and a small amount of hydrogen. Right: bars show China's total fossil carbon dioxide of about 12.2 billion tonnes, transport well-to-wheel emissions of about 1.8 billion tonnes in 2025 and 2.1 in a 2050 petroleum baseline, and about 0.13 and 0.10 billion tonnes for the modelled system before and after gas.

**Fig. 2.** Schematic of the modelled system: electric expressway corridors, representative reactor heat hubs, desert wind, solar and concentrated solar bases, offshore wind and seaweed zones by species group, nearshore seaweed zones in nutrient-polluted bays (triangles), and the main biomass feedstocks of each region. The five autonomous regions are shaded. Boundaries are generalised and not authoritative; locations are illustrative, not a siting study.

Alt text: Schematic map of China, Hong Kong, Macau and Taiwan with the five autonomous regions shaded. Blue lines show electric expressway corridors linking major cities from Urumqi and Lhasa to Beijing, Shanghai and Guangzhou. Red dots mark reactor hubs along the coast and inland. Orange stars mark desert renewable bases in the northwest. Coloured boxes off the coast mark offshore wind and seaweed zones from Liaoning to Hainan and the Taiwan Strait, and green triangles mark six nearshore seaweed zones in polluted bays from Liaodong Bay to Qinzhou Bay. Green labels name regional biomass crops.

**Fig. 3.** Annual 2050 cost compared with petroleum. (A) Cost by component for five system cases, against petroleum at late-2025 and November 2026 pre-tax prices; black lines mark the net cost after credits. (B) Saving against late-2025 petroleum for China cases, Taiwan, and the United States model as submitted (version 8.4) and with corrected heavy-truck ratios; the dashed line marks the 23% U.S. saving.

Alt text: Left: stacked bars show petroleum costs of about 399 and 546 billion dollars and system costs between about 314 and 367 billion dollars, split into electricity and grids, reactor hubs and hydrogen, land biofuels, offshore seaweed, vehicles, and nutrient and soil-carbon returns. Right: horizontal bars show savings of about 22% for China's least-cost case, 15% and 19% for the offshore and after-gas cases, 8% with no nuclear, a negative saving of 14% for Taiwan, and 23.2% and 12.0% for the United States model as submitted and corrected.

**Fig. 4.** Uncertainty. (A) Distribution of the saving against late-2025 petroleum over 1,000 draws for the least-cost, 230 GW offshore and after-gas cases. (B) Share of draws cheaper than petroleum as a function of the petroleum price, expressed as a multiple of late-2025 pre-tax prices; dotted line, November 2026 prices.

Alt text: Left: three overlapping step histograms of percentage savings spread over several tens of percentage points either side of zero, with medians of 3.3, -3 and -1 percent. Right: three rising curves showing the share of draws cheaper than petroleum climbing from near zero at half of late-2025 prices to nearly all draws at one and a half times those prices.

**Fig. 5.** Reactor technologies and start-up fissile material. (A) 2050 cost with hubs built from each technology, in the gas era and after gas, against petroleum. (B) Fissile material needed to start closed-cycle fleets compared with plutonium in China's spent fuel and the International Panel on Fissile Materials' estimate of China's military plutonium (log scale).

Alt text: Left: paired bars for five reactor types show costs between about 298 and 341 billion dollars, all below a dashed petroleum line at 400 billion; the thorium molten-salt reactor is lowest. Right: horizontal bars on a log scale show about 1,330 tonnes of plutonium needed to start a sodium fast fleet and about 380 tonnes of fissile material for a thorium molten-salt fleet, against about 1,100 tonnes of plutonium in spent fuel by 2050, 110 tonnes in 2024 and 2.9 tonnes of military plutonium.

**Fig. 6.** Natural gas supply. (A) Demand with and without the pyrolysis programme against domestic production, pipeline imports and liquefied natural gas imports, central case. (B) First shortfall year across resource, import and demand-side sensitivities.

Alt text: Left: a stacked area chart from 2026 to 2160 shows domestic gas production as the largest source, with pipeline and liquefied gas imports above it, meeting demand until the first shortfall in 2141. Right: horizontal bars show first shortfall years ranging from about 2100 to 2175.

**Fig. 7.** Autonomous regions, special administrative regions and Taiwan. (A) 2050 liquid-fuel demand and liquids produced from each region's own feedstocks in the least-cost case. (B) Well-to-wheel emissions with petroleum and with the system in 2050. The rest of the mainland is omitted for scale.

Alt text: Two horizontal bar charts for Guangxi, Inner Mongolia, Ningxia, Xizang, Xinjiang, Hong Kong, Macau and Taiwan. In the left chart the five autonomous regions produce more liquid fuel than they use, while Hong Kong, Macau and Taiwan produce little or none. In the right chart, emissions for every region fall to a small fraction of the petroleum baseline.

**Fig. 8.** Food from reactor heat and seafood cross-feeding. (A) Annual food output supported by low-grade and drying heat in the least-cost case (log scale). (B) Cross-feed flows between farmed species, in thousand tonnes per year.

Alt text: Left: bars on a log scale show about 30 million tonnes of greenhouse vegetables, 80 million tonnes of grain dried, 3.0 million tonnes of fish, 2.0 million tonnes of shrimp, 1.3 million tonnes of hemp meal and 0.5 million tonnes of dried seaweed. Right: horizontal bars show hundreds of thousands of tonnes of fishmeal, shrimp meal, insect meal, hemp meal, Ulva and kelp moving between farmed species.

**Fig. 9.** Nutrient and soil-carbon balance. (A) Nitrogen, phosphorus and potassium returned to the land by source, as a share of what harvesting removes, in the least-cost and after-gas cases; numbers above the bars are the amounts removed (Mt per year); bars above 100% mean compost returns more than was removed. (B) Stable soil carbon supplied by source against the requirement (red line) in the least-cost and after-gas cases and with biological sources only, with and without manure compost; labels give the residue tonnage used and any liquid fuel the domestic system cannot then supply. No case uses the priced soil-carbon gap, which would be an accounting entry, not material returned to soil. (C) Nitrogen and phosphorus removed from the water by nearshore seaweed farms, harvested by Grid Harvesters, in six eutrophic zones when all are farmed (230 GW offshore case).

Alt text: Three panels. Left: stacked bars for nitrogen, phosphorus and potassium each reach 100% of the amount removed, made up mostly of digested liquefaction wastewater and hydrochar, with mineral fertiliser making up the rest. Middle: stacked bars of stable soil carbon by source for four cases reach a red requirement line of about 27.4 million tonnes of carbon; with biological sources only, green manure and manure compost replace pyrolysis carbon, and without compost less residue is harvested and some liquid fuel cannot be supplied. Right: horizontal bars show nitrogen removed by six nearshore zones from Liaodong Bay to Qinzhou Bay, totalling about 184 thousand tonnes a year.

## Tables

**Table 1.** Annual cost, petroleum break-even and emissions of the principal cases (2050; billions of 2026 US dollars per year). Monte Carlo (MC) columns give the median (5th to 95th percentile) of 1,000 draws and the share of draws cheaper than late-2025 petroleum. Break-even is the multiple of late-2025 pre-tax petroleum prices at which petroleum costs the same as the system. Oil is the cost of the same services with petroleum at late-2025 pre-tax prices; CO~2~e is well-to-wheel emissions in Mt per year. The median MC saving is the median of each draw's own saving: service growth varies between draws and changes the petroleum comparator with it, so it cannot be computed from the median cost and the central petroleum cost.

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

**Table 2.** Stress tests of the central least-cost case (2050; billions of 2026 US dollars per year). Each case is re-optimised. Saving is against petroleum at late-2025 pre-tax prices (USD 400.2 billion); negative values mean the system costs more. The last column is the saving against November 2026 prices (USD 547.0 billion).

| Case | Cost | Saving | Hubs | Pyrolysis H~2~ (Mt) | CO~2~e | Saving, Nov 2026 |
|:------------------------|---------:|----------:|--------:|------------:|----------:|------------:|
| Central least-cost case | 314.1 | 21.5% | 221 | 8.4 | 130 | 42.6% |
| Electric-car net cost, low derivation | 195.9 | 51.1% | 221 | 8.4 | 130 | 64.2% |
| Car stock 500 million | 307.9 | 23.1% | 221 | 8.4 | 130 | 43.7% |
| Car stock 350 million | 319.5 | 20.2% | 221 | 8.4 | 130 | 41.6% |
| At most 60 hubs (360 modules) | 321.8 | 19.6% | 60 | 16.6 | 150 | 41.2% |
| At most 30 hubs (180 modules) | 324.5 | 18.9% | 30 | 16.6 | 150 | 40.7% |
| Grid and firming costs +60–75% | 335.4 | 16.2% | 444 | 8.4 | 129 | 38.7% |
| Commodity carbon markets only | 335.8 | 16.1% | 248 | 5.0 | 122 | 38.6% |
| No carbon-product revenue | 340.7 | 14.9% | 265 | 2.7 | 117 | 37.7% |
| Collectable residues −25% | 344.4 | 13.9% | 274 | 9.8 | 140 | 37.0% |
| Collectable residues −50% | 389.0 | 2.8% | 220 | 8.7 | 138 | 28.9% |
| Electric-car net cost 0 USD/yr (no advantage) | 351.3 | 12.2% | 221 | 8.4 | 130 | 35.8% |
| Electric-car net cost +100 USD/yr | 391.2 | 2.3% | 221 | 8.4 | 130 | 28.5% |
| Electric-car +100 USD/yr and no carbon revenue | 417.8 | -4.4% | 265 | 2.7 | 117 | 23.6% |
| Electric-car net cost, high derivation | 552.4 | -38.0% | 221 | 8.4 | 130 | -1.0% |
| Combined: no electric-car advantage, commodity carbon only, residues −25%, high reactor cost, tight grid | 459.9 | -14.9% | 20 | 28.3 | 184 | 15.9% |
| Combined (moderate) after gas | 486.5 | -21.6% | 1 | 1.2 | 105 | 11.1% |
| Combined: electric-car high derivation, no carbon revenue, residues −25%, high reactor cost, tight grid | 667.7 | -66.8% | 20 | 28.3 | 184 | -22.1% |
| Without nutrient or soil-carbon constraints | 309.0 | 22.8% | 241 | 5.8 | 109 | 43.5% |
| Nutrient balance only, no soil-carbon balance | 312.6 | 21.9% | 241 | 5.8 | 127 | 42.9% |
| Soil carbon replaced by biological sources only (no pyrolysis carbon, no priced gap) | 315.7 | 21.1% | 241 | 5.8 | 119 | 42.3% |
| Biological soil carbon only, compost and green manure costs x2 | 319.8 | 20.1% | 241 | 5.8 | 118 | 41.5% |
| Biological soil carbon only, without compost (liquid shortfall priced at USD 400/MWh) | 455.9 | -13.9% | 169 | 5.8 | 136 | 16.7% |
| Residue humification coefficients x1.5 | 315.4 | 21.2% | 184 | 13.4 | 141 | 42.3% |
| Hydrochar carbon stability 0.3 (central 0.5) | 314.6 | 21.4% | 204 | 10.7 | 135 | 42.5% |
| Mineral fertiliser prices x1.5 | 314.7 | 21.4% | 232 | 6.9 | 125 | 42.5% |
| Nearshore farms in eutrophic bays at full screened area | 314.2 | 21.5% | 222 | 8.3 | 128 | 42.6% |
| Nearshore N removal paid USD 10/kg N (P USD 30/kg) | 311.6 | 22.1% | 222 | 8.3 | 128 | 43.0% |
| Nearshore N removal paid USD 30/kg N (P USD 90/kg) | 306.4 | 23.4% | 222 | 8.3 | 128 | 44.0% |
| After gas, without biomethane pyrolysis | 342.1 | 14.5% | 285 | 0.0 | 100 | 37.5% |
