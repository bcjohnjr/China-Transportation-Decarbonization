"""Inputs, China transport-energy model CN v1.6.2 (USD 2026).  Tags: [S] sourced, [A] modeller assumption (varied in the
Monte Carlo where it matters), [U] carried over unchanged from the U.S. model v8.4 (bcjohnjr/United-States-...).
Not forecasts.

Study area: mainland China including the five autonomous regions (Guangxi, Inner Mongolia, Ningxia, Xizang/Tibet,
Xinjiang), the Hong Kong and Macau Special Administrative Regions (supplied through the Guangdong grid and refineries,
so modelled inside the mainland system) and Taiwan (a separate island grid, modelled as its own system).

Scope (same as the U.S. model): all aviation and on-road transport, rail, domestic and bunkered marine fuel, farm
machinery, construction and mining machinery, industrial trucks and pipeline compression.  2026 U.S. dollars.

Sources used for the 2025 baseline (see SUPPLEMENTARY_MATERIALS_CN_V1.6.2.md, table S1):
  CAPE/SunSirs 2025 review: gasoline 155 Mt, diesel 203 Mt, kerosene/jet 40.21 Mt; gas 426.6 bcm, import share 41.3%.
  ICIS: transport gas 44.14 bcm in 2026, +3.5% y/y -> 42.6 bcm in 2025.  Zhoushan/customs: ~20 Mt bonded bunkers.
  EIA Taiwan brief (2026): gasoline 188 kb/d, diesel 116 kb/d, jet 68.8 kb/d (2024).
"""
QUAD_TWH = 293.07; TCF_TWH = 302.0; TCF_MT_CH4 = 19.3; H2_LHV_KWH_KG = 33.33
BCM_TCF = 0.035315                     # 1 bcm = 0.0353 Tcf
BCM_TWH = 9.9                          # LHV of Chinese pipeline gas, ~35.6 MJ/m3 [A]
GAS_HHV_LHV = 1.109                    # methane 55.5/50.0 MJ/kg; prices are per MMBtu HHV
DIESEL_LHV_HHV = 128450.0 / 137381.0     # 0.935: diesel LHV/HHV per gallon [S: GREET; EIA]
KWH_PER_KG = dict(gasoline=12.06, diesel=11.89, jet=12.00, resid=11.22)   # LHV, 43.4/42.8/43.2/40.4 GJ/t [A: between
# GB/T 2589-2020 (43.07/42.65/43.07/41.82) and IPCC 2006 defaults (44.3/43.0/44.1/40.4); residual oil = IPCC]
WACC = 0.05                            # [A] state-owned infrastructure finance in China (U.S. model: 7%); MC 4-8%
FX = dict(late_2025=7.08, nov_2026=6.71)   # CNY per USD [S: PBoC central parity 25 Nov 2025; 18 Nov 2026]

# ------------------------------------------------------------------------------------------------ 1. demand base (2025)
# Million tonnes of fuel per year unless noted.  Mainland split of the 203 Mt diesel total is an assumption [A].
BASE_MAINLAND = dict(
    gasoline_mt=155.0 + 0.60 + 0.12,          # mainland [S] + Hong Kong [A] + Macau [A]
    onroad_diesel_mt=120.0 + 1.10 + 0.08,     # trucks, buses, light commercial [A: ~59% of 203 Mt]
    road_gas_bcm=42.6,                        # LNG/CNG trucks, buses, taxis [S: ICIS]
    rail_diesel_mt=3.5,                       # [A] ~75% of route-km already electrified
    marine_diesel_mt=12.0 + 0.30,             # inland/coastal shipping and fishing [A]
    marine_resid_mt=20.0 + 4.5 + 3.0,         # bonded bunkers [S ~20 Mt] + Hong Kong bunkers [A] + domestic fuel oil [A]
    jet_mt=40.21 + 5.6 + 0.15,                # mainland kerosene [S] + Hong Kong uplift [S-order: 3.4 Mkl H1 2024] + Macau [A]
    farm_diesel_mt=25.0,                      # [A]
    construction_mining_diesel_mt=25.1,       # [A] incl. open-pit coal and metal mines
    industrial_trucks_mt=3.0,                 # forklifts, port and airport equipment [A]
    pipeline_gas_bcm=5.0,                     # compressor fuel [A]
    non_transport_diesel_mt=14.5,             # excluded from scope (industry, buildings, power) [A]
)
BASE_TAIWAN = dict(
    gasoline_mt=188e3 * 158.987 * 365 * 0.737 / 1e9,        # 188 kb/d [S: EIA] -> ~8.0 Mt
    onroad_diesel_mt=116e3 * 158.987 * 365 * 0.835 / 1e9 * 0.60,   # 60% of 116 kb/d on-road [A]
    road_gas_bcm=0.0, rail_diesel_mt=0.05, marine_diesel_mt=0.35, marine_resid_mt=1.5,   # [A]
    jet_mt=68.8e3 * 158.987 * 365 * 0.80 / 1e9,             # 68.8 kb/d [S: EIA] -> ~3.2 Mt
    farm_diesel_mt=0.30, construction_mining_diesel_mt=0.40, industrial_trucks_mt=0.15, pipeline_gas_bcm=0.1,
    non_transport_diesel_mt=0.0)

# Reporting shares of mainland demand by region [A: proxies from 2024 GDP, sown area, vehicle and mining shares].
# Order: gasoline+road, freight road, air, farm, construction/mining.  "rest" = rest of mainland incl. HK/Macau.
REGIONS = {
    "guangxi":        dict(name="Guangxi Zhuang AR", capital="Nanning", pop_m=50.3, road=0.033, air=0.020, farm=0.036, mine=0.025, lonlat=(108.3, 22.8)),
    "inner_mongolia": dict(name="Inner Mongolia AR", capital="Hohhot", pop_m=24.0, road=0.026, air=0.012, farm=0.059, mine=0.090, lonlat=(111.7, 40.8)),
    "ningxia":        dict(name="Ningxia Hui AR", capital="Yinchuan", pop_m=7.3, road=0.006, air=0.004, farm=0.007, mine=0.012, lonlat=(106.2, 38.5)),
    "xizang":         dict(name="Xizang (Tibet) AR", capital="Lhasa", pop_m=3.7, road=0.003, air=0.004, farm=0.002, mine=0.004, lonlat=(91.1, 29.65)),
    "xinjiang":       dict(name="Xinjiang Uyghur AR", capital="Urumqi", pop_m=26.2, road=0.024, air=0.015, farm=0.043, mine=0.050, lonlat=(87.6, 43.8)),
    "hong_kong":      dict(name="Hong Kong SAR", capital="Hong Kong", pop_m=7.5, road=0.0105, air=0.122, farm=0.0, mine=0.004, lonlat=(114.17, 22.3)),
    "macau":          dict(name="Macau SAR", capital="Macau", pop_m=0.7, road=0.0012, air=0.003, farm=0.0, mine=0.0, lonlat=(113.55, 22.2)),
}
# regional renewable technical potential, TWh/yr [A: order-of-magnitude, schematic; desert bases in the northwest]
REGION_RESOURCE_TWH = {
    "guangxi": dict(wind=300, solar=600, csp=0), "inner_mongolia": dict(wind=6000, solar=9000, csp=3000),
    "ningxia": dict(wind=200, solar=900, csp=200), "xizang": dict(wind=400, solar=7000, csp=4000),
    "xinjiang": dict(wind=4000, solar=12000, csp=6000), "hong_kong": dict(wind=1, solar=6, csp=0),
    "macau": dict(wind=0, solar=0.3, csp=0)}

# ------------------------------------------------------------------------------------------------ 2. 2050 end-use mix
# 're' = battery-electric with a biofuel range-extender (extended-range EVs are ~1/3 of China's NEV stock today [S]).
ENDUSE = dict(
    ldv=dict(bev=0.95, re=0.03, fcev=0.01, liquid=0.01),
    hdv=dict(ers=0.35, bev=0.45, re=0.08, fcev=0.08, liquid=0.04), ers_on_wire=0.80,
    farm=dict(bev=0.35, re=0.45, liquid=0.20),
    construction=dict(bev=0.55, re=0.30, liquid=0.15),     # electric mine haul trucks already common in Inner Mongolia
    industrial=dict(bev=0.95, fcev=0.05),
    rail=dict(elec=0.90, re=0.05, liquid=0.05),
    air=dict(saf=0.97, h2=0.03),
    marine=dict(liquid=0.80, elec=0.10, h2=0.10),          # electric inland vessels on the Yangtze/Pearl [A]
    pipeline=dict(elec=0.60, gas=0.40),
    re_fuel_share=0.25,
    # Energy at the meter (or H2 LHV) per unit of displaced liquid-fuel energy.  CN v1.0 corrects the U.S. v8.4 heavy-truck
    # ratios, which divided kWh/mi by MJ/mi: 2.40 kWh/mi / (21.1 MJ/mi / 3.6) = 0.41, and 4.44 kWh_H2/mi -> 0.76.
    # CN v1.6.2: 21.1 MJ/mi is 144.9 MJ/gal (EIA heat content, a higher heating value) / 6.87 mpg, but the model's diesel
    # demand is on a lower-heating-value basis (Mt x 42.8 GJ/t).  On the LHV basis (128,450 / 137,381 Btu/gal [S: GREET;
    # EIA]) the diesel truck uses 19.7 MJ/mi, so the ratios are 0.44 and 0.81.  The U.S. cross-check keeps 0.41/0.76
    # because U.S. demand is in EIA (HHV) quads.
    r_ldv_bev=0.33 / 1.41, r_ldv_fcev=0.55 / 1.41,
    r_hdv_elec=2.40 * 3.6 / (21.1 * DIESEL_LHV_HHV), r_hdv_fcev=4.44 * 3.6 / (21.1 * DIESEL_LHV_HHV),
    r_offroad_elec=0.36, r_rail_elec=0.33, r_pipe_elec=0.35, r_fork_elec=0.30,
    service_growth_2050=1.15,          # [A] more cars and flights, less freight intensity; MC 1.00-1.40
)
# ------------------------------------------------------------------------------------------------ 3. electricity
ELEC = dict(onshore_wind=30.0, solar=36.0,              # [S: IRENA 2025, China USD 27 and 36/MWh] +11% 2026 adj. for wind
            osw_fixed=60.0, osw_floating=90.0,          # [S: SGERI 2026, 0.335-0.453 CNY/kWh fixed]; floating [A]
            csp=95.0,                                   # [S: Wang et al., 0.684 CNY/kWh weighted] with 8-12 h salt storage
            lwr=65.0,                                   # Hualong One / ACP100 mix [A: ~0.43 CNY/kWh benchmark]
            cf_onw=0.33, cf_pv=0.20, cf_fixed=0.38, cf_float=0.42, cf_csp=0.50,
            td_adder=22.0, vre_firming=20.0, charge_ldv=25.0, charge_hdv=18.0,
            cap_onw_twh=1200.0, cap_onw2_twh=5000.0, onw2_adder=15.0,   # best sites, then remoter/lower-wind sites [A]
             cap_pv_twh=8000.0, cap_csp_twh=600.0, cap_lwr_twh=2500.0,
            max_pv_share=0.40, min_firm_share=0.15, csp_firm_credit=1.0,
            export_value=30.0, export_cap_twh=4000.0,
            liq_import_usd_mwh=170.0, liq_import_cap_twh=0.0)   # imported renewable fuel (Taiwan only by default) [A]
# ------------------------------------------------------------------------------------------------ 4. reactors
# Hub = six 250-MWt HTR-PM modules feeding one turbine island (the HTR-PM600 layout) [S: WNN 2023].
HTGR = dict(outlet_c=750, mwt=1500.0, modules=6, mwe_module=100.0, cf=0.93, f_pyro=0.30, f_mid=0.075, f_dry=0.10,
            eta_cond=0.40, z_mid=0.30, z_dry=0.15, f_low_use=0.35, fom_kwt_yr=30.0, fuel_mwhth=9.0, life=60,
            kwe_per_kwt=0.40, capex_kwt=None)
REACTOR_COST = {   # BOAK overnight cost USD/kWe, FOAK multiplier, learning rate, interest during construction [A]
    "low":     dict(boak_kwe=2500.0, foak_mult=1.3, learning=0.12, idc=0.08),
    "central": dict(boak_kwe=3500.0, foak_mult=1.5, learning=0.08, idc=0.12),
    "high":    dict(boak_kwe=5000.0, foak_mult=2.0, learning=0.04, idc=0.18),
}
REACTOR_ANCHORS = {   # public reference points, order of magnitude only
    "Hualong One (HPR1000), Changjiang phase II, 2 x 1,200 MWe, CNY 40 bn (USD 5.9 bn)": dict(total_bn_usd=5.9, mwe=2400),
    "HTR-PM chief designer target, USD 2,000-3,000/kWe at series build": dict(target_kwe=(2000, 3000)),
}
# Reactor technologies China is building or testing, used as alternative hub designs (S12 of the SM).
# outlet_c sets the methane preheat the reactor can supply; eta = condensing-turbine efficiency; cost_mult on the HTGR
# fleet cost; fuel_mwhth = fuel-cycle cost; fissile = start-up material class (resource accounting only).
REACTOR_TYPES = {
    "htr_pm":  dict(label="HTR-PM pebble-bed HTGR (Shidaowan, operating)", outlet_c=750, eta=0.40, cost_mult=1.00, fuel_mwhth=9.0, fissile="LEU 8.5%", f_pyro=0.30),
    "vhtr":    dict(label="Very-high-temperature gas reactor, 950 C (future)", outlet_c=950, eta=0.45, cost_mult=1.10, fuel_mwhth=10.0, fissile="LEU/HALEU", f_pyro=0.30),
    "tmsr":    dict(label="Thorium molten-salt reactor (TMSR-LF1 lineage, 700 C)", outlet_c=700, eta=0.44, cost_mult=1.20, fuel_mwhth=6.0, fissile="HALEU start, U-233 bred from Th", f_pyro=0.28),
    "cfr":     dict(label="Sodium fast reactor (CFR-600 lineage, 550 C)", outlet_c=550, eta=0.40, cost_mult=1.25, fuel_mwhth=12.0, fissile="Pu (MOX/metal)", f_pyro=0.22),
    "acp100":  dict(label="Light-water SMR (ACP100 Linglong One, ~320 C)", outlet_c=320, eta=0.33, cost_mult=0.85, fuel_mwhth=7.0, fissile="LEU <5%", f_pyro=0.08),
}
PYRO = dict(kg_ch4_per_kg_h2=4.0 / 0.98, heat_kwh_kg=8.3, elec_kwh_kg=3.0, capex_kw_h2=750.0, fom=0.04, life=25,
            c_per_h2=3.0, leak_upstream=0.015, upstream_co2_frac=0.05, h2_leak=0.02, gwp_h2=11.6, gwp_ch4=29.8,
            config="xe100", reactor_preheat_kwh_kg=2.5, boost_eff=0.95, boost_heater_cost_kg=0.02, cp_ch4=3.3)
GAS = dict(price_mmbtu=8.5, delivery_mmbtu=0.8)        # [A] city-gate ~2.5 CNY/m3 ex-VAT; LNG $10-14 in 2026; MC 6-13
ELECTROLYSIS = dict(kwh_kg=52.0, capex_cost_kg=0.6)     # alkaline stacks made in China [A]
# Steam electrolysis (solid oxide, ~800 C stack).  CN v1.3: the heat inputs come from the temperature-enthalpy balance in
# cn_htse_heat.py rather than being assumed.  kwh_e_kg: stack and balance of plant [U: INL].  kwh_th_kg: external
# steam-raising heat at <= 152 C (feed-water preheat not covered by recovery, plus evaporation at 0.5 MPa), drawn from the
# reactor's process-steam (mid) tier or from electric boilers (0.98), never from heat pumps.  superheat_kwh_kg: electric
# topping above what the high-temperature recuperator supplies (final 25 K lift plus stack heat loss), supplied by
# electric heaters (0.95) unless the reactor outlet is >= 850 C.  Recuperation does not depend on the heat source, so the
# same topping applies without reactor steam.  Recuperator and heater costs are added to the capital charge.
import cn_htse_heat as _hb
_HB = _hb.balance()
NUCLEAR_H2 = dict(htse=dict(kwh_e_kg=36.8, kwh_th_kg=round(_HB["external_heat_kwh_kg"], 3), superheat_kwh_kg=round(_HB["topping_kwh_kg"], 3),
                            superheat_noreactor_kwh_kg=round(_HB["topping_kwh_kg"], 3), heater_eff=0.95,
                            capex_cost_kg=round(0.6 + _HB["recuperator_usd_kg"] + _HB["topping_heater_usd_kg"], 4)),   # [U: INL] capex lower in China [A]
                  sulfur_iodine=dict(kwh_e_kg=2.0, kwh_th_kg=39.4 / 0.45, capex_cost_kg=1.2))
FUEL = dict(haleu_enrich=0.155, feed_assay=0.00711, tails=0.0025, haleu_burnup_gwd_t=90.0,   # HTR-PM 8.5%/90 GWd/t [S]
            fission_mwd_per_g=0.95, closed_cycle_loss=0.02,
            cn_uranium_identified_t=250_000.0,        # [A, order of NEA/IAEA Red Book RAR+IR for China]
            cn_depleted_u_t=120_000.0,                # [A]
            cn_thorium_identified_t=100_000.0,        # [S: IAEA/NEA compilation, 'possibly many hundred thousand t']
            cn_thorium_bayan_obo_t=1_000_000.0,       # [S: 2020 survey reported by SCMP, 2025; unverified]
            world_identified_u_t=8.1e6, world_thorium_t=6.4e6, seawater_u_t=4.5e9,
            gwe_per_gwt=0.40, startup_pu_t_per_gwe=10.0,
            startup_msr_fissile_t_per_gwe=1.5,        # [A] thermal-spectrum MSR fissile inventory
            cn_snf_thm_2024=11_000.0, cn_snf_thm_2050=111_290.0, snf_pu_frac=0.01,   # [S: WNTI 2025; Stimson 2020]
            cn_military_pu_t=2.9, cn_military_pu_unc_t=0.6)   # [S: IPFM 2025, as of Jan 2024]
H2_DELIVERY = dict(vehicle=2.0, onsite=0.15, blend=0.3)
# ------------------------------------------------------------------------------------------------ 5. land biomass
# Residue tiers: (name, region, cap Mt dry/yr, delivered USD/t).  China produces ~860-900 Mt of crop straw a year [S: RMI
# 2026]; agronomic removal limits of 19-45% [S: Shi et al. 2025] bound the collectable surplus.
BIOMASS = dict(tiers=[
    ("Crop straw, North China Plain and Northeast (maize, wheat)", "rest", 110.0, 40.0),
    ("Crop straw, Yangtze and South China (rice)", "rest", 55.0, 45.0),
    ("Inner Mongolia maize stover and crop stalks", "inner_mongolia", 25.0, 38.0),
    ("Xinjiang cotton stalks and crop residues", "xinjiang", 20.0, 40.0),
    ("Guangxi sugarcane bagasse surplus and cassava residues", "guangxi", 8.0, 35.0),
    ("Ningxia crop residues (Loess Plateau)", "ningxia", 2.0, 42.0),
    ("Xizang alpine grassland biomass and forestry residues", "xizang", 1.5, 75.0),
    ("Forestry and wood-processing residues", "rest", 70.0, 55.0),
    ("Existing bamboo-stand residues and thinnings (Fujian, Zhejiang, Jiangxi, Hunan)", "rest", 30.0, 45.0),
    ("Crop straw tier 2 (higher removal, longer haul)", "rest", 60.0, 65.0)], hhv_gj_t=18.0)
# Starch/sugar ethanol feedstocks: (key, name, region, cap bn gal ethanol/yr, USD per gal incl. conversion,
# Mt dry bagasse/stalk to the residue pool per bn gal) [A unless noted]
ETHANOL_FEEDS = [
    ("cassava", "Guangxi cassava (non-grain fuel ethanol)", "guangxi", 0.35, 2.4, 0.0),          # Guangxi >60% of China's cassava [S]
    ("molasses", "Guangxi sugarcane molasses", "guangxi", 0.21, 1.6, 0.0),                       # 6.4 Mt sugar, 2024/25 [S]
    ("sorghum_im", "Inner Mongolia sweet sorghum (saline-alkaline land)", "inner_mongolia", 0.71, 2.0, 6.7),
    ("sorghum_xj", "Xinjiang sweet sorghum (drip-irrigated saline land)", "xinjiang", 0.59, 2.0, 6.7),
    ("sorghum_nx", "Ningxia sweet sorghum (Loess Plateau)", "ningxia", 0.12, 2.1, 6.7),
    ("artichoke", "Inner Mongolia Jerusalem artichoke (sandy land)", "inner_mongolia", 0.16, 2.6, 0.0),
    ("sweet_potato", "Ningxia sweet potato", "ningxia", 0.05, 2.5, 0.0),
    ("grain", "Aged-grain ethanol, existing plants", "rest", 1.20, 2.2, 0.0)]
# Oil feedstocks for hydroprocessing (HEFA): (key, name, region, cap Mt oil/yr, delivered USD/t)
OIL_FEEDS = [
    ("uco", "Used cooking oil and trap grease (collected)", "rest", 5.0, 800.0),     # China exported ~2.9 Mt UCO in 2024 [S-order]
    ("jatropha", "Jatropha curcas on marginal slopes (Guangxi, Yunnan, Sichuan)", "guangxi", 0.5, 900.0),
    ("cottonseed", "Xinjiang cottonseed and non-edible oilseed residues", "xinjiang", 0.4, 700.0),
    ("woody_oil", "Woody oil crops (Xanthoceras, Pistacia) in the north", "rest", 0.5, 1000.0)]
JATROPHA_GUANGXI_SHARE = 0.4          # share of the jatropha oil grown in Guangxi (rest Yunnan/Sichuan/Guizhou) [A]
BAMBOO = dict(  # new clumping-bamboo plantations on marginal hill land (Dendrocalamus, Bambusa) [A]
    yield_t_ha=(10.0, 15.0, 22.0), establish_usd_ha=2000.0, establish_life=20, land_rent_usd_ha=150.0,
    harvest_usd_t=15.0, haul_usd_t=10.0,
    regions=[("Guangxi hills (clumping Dendrocalamus, Bambusa)", 0.6, "guangxi"), ("Guangdong", 0.4, "rest"),
             ("Sichuan basin and Chongqing", 0.5, "rest"), ("Yunnan", 0.5, "rest"), ("Guizhou", 0.3, "rest"),
             ("Fujian, Jiangxi, Hunan (clumping species only)", 0.7, "rest")])
HEMP = dict(seed_t_ha=0.9, oil_frac=0.30, stalk_t_ha=7.0, protein_frac_meal=0.33,
            cost_usd_ha=600.0, meal_value_usd_t=550.0, max_mha=2.0,
            regions=[("Heilongjiang", 0.8, "rest"), ("Jilin", 0.3, "rest"), ("Inner Mongolia (east)", 0.4, "inner_mongolia"),
                     ("Yunnan", 0.3, "rest"), ("Shanxi and Gansu", 0.2, "rest")])
ROUTES = dict(
    htl=dict(mwh_t=2.6, h2_kg_t=13.5, el_mwh_t=0.15, heat_mwh_t=0.35, cost_t=130.0, jet=0.45, ci_g_mj=12.0, char_t_t=0.12),
    pbtl=dict(mwh_t=4.44, h2_kg_t=110.0, el_mwh_t=0.60, heat_mwh_t=0.0, cost_t=230.0, jet=0.65, ci_g_mj=6.0, char_t_t=0.0),
    hefa=dict(mwh_t=10.1, h2_kg_t=35.0, el_mwh_t=0.10, heat_mwh_t=0.30, conv_t=90.0, jet=0.55, ci_g_mj=30.0),
    hefa_conv_only=90.0,
    atj=dict(mwh_per_bgal=19.8, conv_per_bgal=0.40 * 1.1e9, jet=0.85, ci_g_mj=40.0),
    ethanol=dict(mwh_per_bgal=22.37, cellulosic_gal_per_t=85.0, cellulosic_conv_per_gal=1.00),
)
# ------------------------------------------------------------------------------------------------ 6. seaweed by region
# (key, wind type, region, species, usable share, yields dem/design/learning t dry/ha/yr, DM, N%, land-N share,
#  GW in the large build, port km, map box lon0,lat0,w,h, colour key, reporting region)
# China grew ~60% of the world's farmed seaweed in 2022 [S: FAO via Liu et al. 2025]; Saccharina japonica dominates.
SEAWEED = [
    ("liaoning", "fixed", "Liaodong peninsula (Dalian, Yellow Sea)", "Saccharina japonica + Undaria pinnatifida",
     0.45, (6.0, 12.0, 18.0), 0.12, 0.020, 0.25, 40.0, 40.0, (122.4, 38.0, 1.5, 0.8), "cold_kelp", "rest"),
    ("shandong", "fixed", "Shandong peninsula (Rongcheng, Weihai)", "Saccharina japonica (China's kelp centre)",
     0.45, (7.0, 13.0, 19.0), 0.12, 0.020, 0.30, 60.0, 40.0, (122.9, 35.7, 1.3, 1.3), "cold_kelp", "rest"),
    ("jiangsu", "fixed", "Jiangsu radial sand ridges (Rudong, Yancheng)", "Pyropia yezoensis (nori) winter + Gracilaria summer",
     0.50, (2.0, 4.0, 6.0), 0.12, 0.050, 0.50, 70.0, 50.0, (121.9, 32.2, 1.3, 1.6), "kelp_red_rotation", "rest"),
    ("zhejiang", "fixed", "Zhejiang (Zhoushan, Wenzhou)", "Sargassum fusiforme + Pyropia haitanensis + winter Saccharina",
     0.45, (4.0, 8.0, 12.0), 0.13, 0.025, 0.60, 50.0, 45.0, (122.4, 27.9, 1.1, 1.9), "kelp_red_rotation", "rest"),
    ("fujian", "fixed", "Fujian, Taiwan Strait (Xiapu, Pingtan)", "Winter Saccharina + summer Gracilaria lemaneiformis + Pyropia",
     0.45, (6.0, 12.0, 18.0), 0.12, 0.022, 0.35, 80.0, 40.0, (120.1, 24.5, 1.0, 1.7), "kelp_red_rotation", "rest"),
    ("guangdong", "float", "Guangdong (Yangjiang, Shanwei, Zhanjiang)", "Gracilaria lemaneiformis + Ulva + Sargassum",
     0.40, (3.0, 6.0, 9.0), 0.14, 0.025, 0.55, 90.0, 60.0, (111.5, 20.6, 4.0, 0.9), "red_green", "rest"),
    ("guangxi", "fixed", "Beibu Gulf (Guangxi: Beihai, Qinzhou, Fangchenggang)", "Gracilaria + Ulva; Kappaphycus trials",
     0.45, (3.0, 6.0, 9.0), 0.14, 0.025, 0.40, 30.0, 45.0, (107.9, 20.6, 1.6, 0.9), "red_green", "guangxi"),
    ("hainan", "float", "Hainan (Wanning, Lingshui, Danzhou)", "Kappaphycus alvarezii / Eucheuma + Gracilaria (tropical reds)",
     0.40, (4.0, 8.0, 12.0), 0.12, 0.020, 0.20, 40.0, 50.0, (110.4, 17.6, 1.8, 0.8), "tropical_red", "rest"),
]
SEAWEED_TAIWAN = [
    ("taiwan", "fixed", "Taiwan Strait (Changhua, Miaoli)", "Gracilaria + Ulva (warm water)",
     0.45, (3.0, 6.0, 9.0), 0.14, 0.025, 0.30, 25.0, 40.0, (119.3, 22.9, 0.6, 1.2), "red_green", "taiwan")]
SEAWEED_PROCESS = dict(
    htl_mwh_t=1.9, htl_h2_kg_t=6.8, htl_el_mwh_t=0.12, htl_heat_mwh_t=0.30, htl_cost_t=200.0, htl_ci=15.0,
    pbtl_mwh_t=3.5, pbtl_h2_kg_t=90.0, pbtl_el_mwh_t=0.5, pbtl_dry_mwh_t=1.4, pbtl_cost_t=270.0, pbtl_ci=10.0,
    farm_cost_ref_t=260.0, ref_yield=15.0, shared_mooring_saving=0.15, mw_per_km2=4.0,   # Chinese longline costs [A]
    p=0.003, k=0.045, n_rec=0.60, p_rec=0.80, k_rec=0.80, meal_share=0.05)
# CN v1.6.2: mineral fertiliser priced per tonne of ELEMENTAL N, P and K, the basis of every nutrient flow in the model
# (straw P and K are elemental: 1.8 kg P/t = 0.41% P2O5, 15.3 kg K/t = 1.84% K2O).  CN v1.6.1 used 1,100 and 500, which
# are prices per t of P2O5 and per t of KCl product, understating P by 2.3x and K by about 2x.  Farm-gate, late 2025:
# urea ~2,000 CNY/t (46% N) -> ~USD 620-700/t N; 11-44 MAP ~4,000 CNY/t less its N -> ~USD 1,130/t P2O5 = ~2,600/t P
# (P = 0.4364 P2O5); KCl ~3,500 CNY/t (60% K2O) -> ~USD 820/t K2O = ~1,000/t K (K = 0.8301 K2O), at 7.08 CNY/USD [S: NBS
# and SunSirs benchmark prices, Nov 2025-Nov 2026; A: distribution to farm gate]
FERT_PRICE = dict(n=700.0, p=2600.0, k=1000.0)     # USD per t elemental nutrient
LOGISTICS = dict(   # solar/wind-powered Grid Harvesters, battery-sail vessels, drones [U: geometry and energy]
    gh_kwh_per_ha_pass=6.5, gh_unit_capex=4.0e6, gh_life=20, gh_pv_kw=150.0, gh_hours=4000.0, press_to_dm=0.30,
    vessel_t=2500.0, vessel_kn=10.0, vessel_kwh_tkm=0.06, vessel_capex=18.0e6, vessel_life=25, vessel_days=300,
    vessel_sail_share=0.25, vessel_om=0.04, load_hours=5.0,
    drone_km2=15.0, drone_capex=30_000.0, drone_life=5, drone_om_yr=5000.0)
# ------------------------------------------------------------------------------------------------ 7. carbon markets
CARBON_MARKETS = [   # (market, cap Mt C/yr, net value USD/t) [A]; China makes most of the world's anode graphite
    ("Vehicle structures and H2 tanks (methane-derived carbon fibre/CNT)", 1.5, 3500.0),
    ("Battery anode graphite (after graphitisation)", 4.0, 2500.0),
    ("Carbon black: tyres and rubber", 7.0, 800.0),
    ("Specialty carbon (conductive additive, fibre precursors)", 0.8, 1500.0),
    ("Metallurgical: electrodes, recarburiser, Al anodes", 4.0, 400.0),
    ("Construction: asphalt and concrete additive", 20.0, 60.0),
    ("Soil amendment (pyrolysis carbon; counts toward the soil-carbon balance)", 100.0, 0.0),   # CN v1.5: net of spreading [A]
    ("Permanent storage (mine voids, monofill)", 1e4, -20.0)]
# ------------------------------------------------------------------------------------------------ 7b. nutrient and soil-carbon balance (CN v1.5)
# Every tonne of biomass taken from fields or forests removes N, P, K and the carbon that would have built soil organic
# carbon (SOC).  The LP must put back at least what it removes, from (in merit order chosen by the optimiser):
# HTL hydrochar (P, stable C), digested HTL wastewater (N, K, some C; the digestion also yields biomethane), gasifier
# and ethanol-plant ash and stillage (P, K), seaweed (fertiliser and organic matter), pyrolysis carbon (stable C only),
# or purchased mineral fertiliser (N, P, K; with production emissions).
# Straw contents: N 0.78/0.64/0.85%, P2O5 0.42/0.27/0.53%, K2O 2.31/1.53/1.59% for rice/wheat/maize straw [S: Scientia
# Agricultura Sinica 2020]; weighted for China's straw mix and converted to elemental P and K.  C contents and SOC
# humification coefficients (share of residue C that would have become stable SOC) are assumptions [A].
NUTRIENTS = dict(
    content=dict(   # kg per t dry matter: N, P, K, C
        straw=dict(n=7.6, p=1.8, k=15.3, c=430.0, humif=0.15),
        forest=dict(n=4.0, p=0.5, k=2.0, c=500.0, humif=0.10),
        bamboo=dict(n=5.0, p=0.6, k=4.0, c=470.0, humif=0.12),
        grass=dict(n=12.0, p=1.5, k=12.0, c=440.0, humif=0.15),
        hemp=dict(n=5.0, p=1.0, k=8.0, c=450.0, humif=0.15)),
    # where each element ends up, as shares of the feed (HTL: P mostly to solids, K to the aqueous phase; N split between
    # biocrude and aqueous phase) [S: Conti et al. 2018, K > 88% to the aqueous phase; A for the other shares]
    htl_to_aqueous=dict(n=0.55, p=0.15, k=0.88, c=0.25), htl_to_solids=dict(n=0.10, p=0.80, k=0.08),
    hydrochar_c=0.60,   # t C per t hydrochar; hydrochar yield is ROUTES['htl']['char_t_t'] [A]
    aqueous_recovery=dict(n=0.85, p=0.90, k=0.95),      # digestion, ammonia stripping, struvite; returned as digestate [A]
    solids_recovery=dict(n=1.0, p=1.0, k=1.0),
    pbtl_ash=dict(n=0.0, p=0.85, k=0.80),               # gasifier ash/slag; N leaves as N2/NH3 [A]
    cel_stillage=dict(n=0.60, p=0.85, k=0.90),          # lignin and stillage from cellulosic ethanol [A]
    seaweed_htl=dict(n=0.60, p=0.80, k=0.30),           # saline aqueous phase: N by stripping, P by struvite; little K [A]
    seaweed_pbtl=dict(n=0.0, p=0.60, k=0.50),
    seaweed_soil=dict(n=1.0, p=1.0, k=0.70),            # washed (salt removal leaches some K) [A]
    # soil-carbon sources: fraction of applied C that becomes stable SOC [A]
    stab_hydrochar=0.50, hum_digestate=0.30, digestate_c_after_ad=0.40, hum_seaweed=0.10, stab_pyro_carbon=0.90,
    seaweed_c=300.0,                                     # kg C per t dry seaweed [A]
    # CN v1.6 biological soil-carbon options, available in every case and chosen by the LP when they pay:
    # winter legume green manure on fields that are now fallow in winter (Chinese milk vetch, hairy vetch), and compost
    # from livestock manure that is not now returned to fields [A]
    green_manure=dict(max_mha=6.7, cost_usd_ha=200.0, dm_t_ha=3.5, c=420.0, humif=0.20, n_fixed_kg_ha=60.0),
    compost=dict(max_mt=50.0, cost_usd_t=60.0, c=300.0, humif=0.35, n=15.0, p=6.0, k=12.0, ci_t=0.10),
    soc_deficit_usd_t_c=500.0,  # soil carbon that is not replaced is allowed only at this price (~USD 136/t CO2) and is counted
                                # as an emission; it keeps cases without pyrolysis carbon feasible and shows the cost of the gap [A]
    biogenic_min_share=0.50,   # at least half of the stable SOC replacement must come from biogenic organic matter, which also
                               # feeds soil organisms; pyrolysis carbon is inert and can cover at most the other half [A]
    # costs, USD per t of feed (or of dry seaweed) [A]
    cost_hydrochar_return_t=6.0, cost_ad_t=12.0, cost_ash_return_t=1.0, cost_stillage_return_t=4.0, cost_seaweed_to_soil_t=70.0,
    fert_sale_share=0.70,      # surplus recovered nutrients sold at 70% of mineral fertiliser prices
    # biomethane from digesting HTL wastewater of rice straw: 217-314 mL CH4 per g COD [S: Chen et al. 2017]; about 0.35 MWh
    # of methane per t of feed (roughly 7% of feed energy) [A]
    ad_mwh_ch4_per_t=0.35, ad_ch4_slip=0.01,
    # mineral fertiliser production emissions, t CO2e per t nutrient (coal-based ammonia in China) [A]
    fert_ci=dict(n=8.0, p=2.0, k=0.5))
# Nearshore seaweed farms in eutrophic waters (bioextraction).  Waters worse than Grade IV are mainly in Liaodong Bay, the
# Yangtze River estuary, Hangzhou Bay and the Pearl River estuary [S: MEE 2023 bulletin].  Species are chosen for each
# water's temperature range, for proven nutrient uptake and for low bloom and contaminant risk; Ulva and new Pyropia rafts
# on the Subei shoal are excluded (source of Yellow Sea green tides), as is Sargassum for soil use (arsenic).  Tissue N and
# P are higher in nutrient-rich water (Chinese farm mean 3.71% N, 0.52% P [S: Xiao et al. 2017]).
# (key, region, species, water status, max km2, yield t DW/ha/yr (low, central, high), N%, P%, K%, port km, lon, lat,
#  report region, soil use allowed)
BIOEXTRACT = [
    ("liaodong_bay", "Liaodong Bay, Bohai (Yingkou, Jinzhou, Huludao)", "Saccharina japonica (Nov-May) + Gracilariopsis lemaneiformis (Jun-Oct)",
     "worse than Grade IV near estuaries", 600.0, (10.0, 16.0, 22.0), 2.8, 0.40, 3.5, 15.0, 121.2, 40.3, "rest", True),
    ("haizhou_bay", "Haizhou Bay (Lianyungang, northern Jiangsu)", "Saccharina japonica (winter) + Gracilariopsis lemaneiformis (spring, autumn)",
     "eutrophic; Subei shoal Pyropia expansion excluded", 300.0, (10.0, 15.0, 20.0), 2.8, 0.40, 3.0, 15.0, 119.6, 34.8, "rest", True),
    ("yangtze_plume", "Yangtze plume: Zhoushan islands and Xiangshan Bay (turbid inner estuary and Hangzhou Bay excluded)",
     "Gracilariopsis lemaneiformis (spring, autumn) + Saccharina japonica (winter)", "worse than Grade IV", 900.0, (10.0, 18.0, 26.0), 3.2, 0.40, 2.5, 15.0, 122.1, 29.8, "rest", True),
    ("fujian_bays", "Fujian bays: Sansha, Luoyuan, Xiamen-Jiulong River estuary", "Gracilariopsis lemaneiformis (Nov-May) + Saccharina japonica (winter) + Gracilaria bailinae (summer)",
     "eutrophic bays", 700.0, (12.0, 20.0, 28.0), 3.0, 0.42, 2.5, 10.0, 119.9, 26.6, "rest", True),
    ("pearl_river", "Pearl River estuary outer waters and Daya Bay (Guangdong, Hong Kong boundary)", "Gracilaria bailinae + Gracilaria tenuistipitata (heat-tolerant, year-round)",
     "worse than Grade IV", 800.0, (10.0, 16.0, 24.0), 3.0, 0.40, 2.0, 10.0, 114.2, 22.3, "rest", True),
    ("beibu_qinzhou", "Qinzhou Bay and Fangchenggang, Beibu Gulf (Guangxi)", "Gracilaria bailinae (heat-tolerant)",
     "eutrophic inner bay", 300.0, (10.0, 15.0, 22.0), 2.8, 0.38, 2.0, 10.0, 108.6, 21.7, "guangxi", True)]
BIOEXTRACT_COST = dict(farm_usd_ha_yr=3500.0, passes=2.0)   # Chinese nearshore longline farms (lines, seeding, upkeep) [A];
# CN v1.6: harvest by the same solar-powered Grid Harvesters, battery-sail vessels and drones as the offshore zones (LOGISTICS),
# with the zone's port distance; 2 harvest passes a year for the kelp/Gracilaria rotations

# How long carbon sold to each market stays out of the atmosphere [A]: tyre carbon black is lost as wear particles or
# burned at end of life; electrodes and recarburiser are oxidised in use; anode graphite and fibres last one product
# life (10-20 years) unless recycled to landfill; asphalt/concrete additives and mine-void storage are long-term.
CARBON_DURABILITY = ["product_life", "product_life", "short", "product_life", "oxidised", "long_term", "uncertain", "long_term"]
# CN v1.3 stylised wind-lull adequacy screen (not an hourly dispatch model).  During a windless, overcast winter week the
# flexible loads (electrolysis, electric process heat, fuel-conversion plants with product storage) stop, reactor heat
# goes entirely to the turbines, and the remaining inflexible transport load must be met by firm plant, residual wind and
# sun, or backup.  All values [A].
LULL = dict(days=7.0, wind_cf=0.08, offshore_cf=0.10, solar_cf=0.08, csp_cf=0.30, hub_availability=0.93, lwr_availability=0.90,
            load_factor=1.15, backup_capex_usd_kw=750.0, backup_life_yr=25, h2_to_power_eff=0.40, events_per_yr=2.0,
            h2_value_usd_kg=2.0)
# Emissions-boundary parameters (central values reproduce the headline; alternatives in cn_model.emissions_boundary)
EMIS = dict(elec_ci=0.010, residue_soc_g_mj=0.0, hub_heat_ci=0.0)
VEHICLE_CARBON = dict(cars_m=25.0, trucks_m=3.0, kg_car=40.0, kg_truck=150.0, mass_saving_car=0.10,
                      mass_saving_truck=0.06, energy_per_mass=0.45)
# ------------------------------------------------------------------------------------------------ 8. vehicles (2050 stock)
# Net annualised cost of electric or fuel-cell drive vs. a combustion equivalent, excluding energy [A].  Chinese BEVs
# already sell at or below combustion-car prices (BYD and others), so the central LDV value is negative.
# Derivation of the net annual cost of a battery-electric car vs a comparable petrol car in 2050, excluding energy
# (energy is costed in the system).  Purchase: the average NEV sold in China in August 2025 cost about 90% of the average
# petrol car (Autohome), and ICCT projects price parity for 300-400 km range cars by 2026-2029 [S]; the central -1,000 USD
# is more conservative than today's average gap.  Insurance: the 2025 average NEV premium was 4,360 CNY, nearly double
# the petrol average, but much of the gap reflects younger drivers, ride-hailing use and newer cars; like-for-like
# premiums are about 20% higher (S&P) [S]; central +100 USD/yr, high case keeps today's ~300 USD gap.  Maintenance and
# repair: petrol car 350 USD/yr [A], BEV 35% lower net of higher Chinese repair costs (ICCT ~40% lower per mile) [S/A].
# Battery replacement: expected replacements per car over a 12-year life, at year 9 [A].
LDV_TCO = dict(
    central=dict(purchase_diff_usd=-1000.0, life_yr=12, repl_prob=0.15, pack_kwh=55.0, pack_usd_kwh=70.0, repl_year=9,
                 maint_ice_usd_yr=350.0, maint_saving=0.35, insurance_extra_usd_yr=100.0),
    low=dict(purchase_diff_usd=-2500.0, life_yr=12, repl_prob=0.05, pack_kwh=55.0, pack_usd_kwh=50.0, repl_year=9,
             maint_ice_usd_yr=350.0, maint_saving=0.45, insurance_extra_usd_yr=40.0),
    high=dict(purchase_diff_usd=500.0, life_yr=12, repl_prob=0.50, pack_kwh=55.0, pack_usd_kwh=100.0, repl_year=9,
              maint_ice_usd_yr=350.0, maint_saving=0.15, insurance_extra_usd_yr=300.0))


def ldv_bev_net(case="central", wacc=0.05, parts=False):
    """Annualised net cost (USD/yr) of a BEV car vs a petrol car, excluding energy."""
    d = LDV_TCO[case]; crf = wacc / (1 - (1 + wacc) ** -d["life_yr"])
    c = dict(purchase=d["purchase_diff_usd"] * crf,
             battery_replacement=d["repl_prob"] * d["pack_kwh"] * d["pack_usd_kwh"] / (1 + wacc) ** d["repl_year"] * crf,
             maintenance=-d["maint_saving"] * d["maint_ice_usd_yr"], insurance=d["insurance_extra_usd_yr"])
    return c if parts else sum(c.values())


VEH = dict(ldv_stock_m=420.0, ldv_bev_net_usd_yr=round(ldv_bev_net("central"), 1), ldv_re_net_usd_yr=150.0, ldv_fcev_net_usd_yr=700.0,
           ers_trucks_m=2.5, fcev_trucks_m=0.6, bev_trucks_m=18.0, re_trucks_m=2.0,
           ers_truck_net_usd_yr=2500.0, fcev_truck_net_usd_yr=8000.0, bev_truck_net_usd_yr=1200.0, re_truck_net_usd_yr=2500.0,
           tractors_m=8.0, tractor_net_usd_yr=600.0, constr_m=10.0, constr_net_usd_yr=1500.0, forklifts_m=5.0, forklift_net_usd_yr=-200.0,
           ers_km=60000.0, ers_capex_m_per_km=1.8, ers_om=0.025, ers_life=40,   # main freight corridors of the 199,000 km expressways
           rail_elec_capex_bn=40.0, rail_life=40, farm_charging_bn_yr=2.0)
# Pre-tax petroleum prices, USD per tonne.  Retail = NDRC cap; pre-tax = retail/1.13 VAT minus consumption tax
# (1.52 CNY/L gasoline, 1.20 CNY/L diesel) [S: IEA/OECD tax notes; NDRC 24 Nov 2025 and 12 Nov 2026 adjustments].
#   late 2025: 92# 6.85 CNY/L, 0# diesel 6.55 CNY/L, jet 5,600 CNY/t [A], VLSFO bunker 480 USD/t [A], LNG 11 USD/MMBtu [A]
#   Nov 2026:  92# 8.41 CNY/L [S], 0# diesel 7.95 CNY/L [A], jet 7,900 CNY/t [A, 8,150 in Sept S], bunker 700 USD/t [A],
#              LNG 14 USD/MMBtu [A]; Brent ~95 USD/bbl in mid-November 2026 [S]
def _pretax_usd_t(retail_cny_l, tax_cny_l, density, fx):
    return (retail_cny_l / 1.13 - tax_cny_l) / density * 1000 / fx
PRICES_USD_T = {
    "late_2025": dict(gasoline=_pretax_usd_t(6.85, 1.52, 0.737, FX["late_2025"]), diesel=_pretax_usd_t(6.55, 1.20, 0.835, FX["late_2025"]),
                      jet=5600 / 1.13 / FX["late_2025"], resid=480.0, road_gas_mmbtu=11.0),
    "nov_2026": dict(gasoline=_pretax_usd_t(8.41, 1.52, 0.737, FX["nov_2026"]), diesel=_pretax_usd_t(7.95, 1.20, 0.835, FX["nov_2026"]),
                     jet=7900 / 1.13 / FX["nov_2026"], resid=700.0, road_gas_mmbtu=14.0),
}
RETAIL_CNY_L = {"late_2025": dict(gasoline=6.85, diesel=6.55), "nov_2026": dict(gasoline=8.41, diesel=7.95)}
PETRO_CI = dict(gasoline=93.0, diesel=95.0, jet=89.0, resid=96.0, ng=70.0)     # g CO2e/MJ WTW [U]
ETHANOL_CI = dict(today=55.0, ccs=30.0)
# ------------------------------------------------------------------------------------------------ 9. gas resource (China)
NG = dict(
    prod_bcm_2025=261.9, consumption_bcm_2025=426.6, import_share_2025=0.413,          # [S: CAPE Blue Book 2025]
    pipeline_import_bcm_2025=81.0, lng_import_mt_2025=68.43,                           # [S: Kpler; customs]
    pipeline_cap_bcm_2030=114.0, pipeline_cap_bcm_2035=150.0,                          # [S: 15th FYP land-import target; +PoS-2 A]
    trr_conventional_tight_tcm=40.0, trr_shale_tcm=25.0, trr_cbm_tcm=11.0,              # [S: national assessments, Springer 2017]
    cumulative_produced_tcm=3.2,                                                       # [A]
    domestic_cap_growth=0.03, domestic_plateau_bcm=360.0,                              # [A] Kpler: 297 bcm in 2028
    pipeline_pool_tcm=20.0,                                                            # Russian/Central Asian gas dedicated to China [A]
    lng_cap_bcm=140.0,                                                                 # ~100 Mt/yr LNG import ceiling [A]
    non_transport_growth=0.015, non_transport_growth_until=2040,
    rp_floor_years=15.0, res_com_bcm=110.0)
# ------------------------------------------------------------------------------------------------ 10. food from the cascade
FOOD = dict(
    greenhouse_heat_kwh_m2=220.0, greenhouse_yield_kg_m2=40.0, greenhouse_market_mt=30.0,   # northern solar greenhouses [A]
    greenhouse_value_usd_t=900.0, kcal_per_kg_veg=200.0,
    ras_heat_kwh_kg=4.0, ras_market_mt=5.0, ras_value_usd_t=4500.0, kcal_per_kg_fish=1200.0, ras_shrimp_share=0.40,
    asparagopsis_heat_mwh_t=25.0, grain_dry_mwh_t=0.08, grain_near_hub_mt=80.0, seaweed_food_dry_mwh_t=1.2,
    seaweed_food_dry_mt=0.5, kcal_per_person_day=2200.0, hemp_kcal_per_kg_seed=5500.0,
    vegetable_edible_fraction=0.85, fish_shrimp_edible_fraction=0.60)
AG = dict(head_feedlot_m=20.0, head_dairy_m=6.4, head_grazing_m=70.0, dmi_kg_d=dict(feedlot=9.0, dairy=20.0, grazing=8.0),
          dose_dm=0.0025, cut=dict(feedlot=0.60, dairy=0.60, grazing=0.35), adoption=dict(feedlot=0.8, dairy=0.8, grazing=0.2),
          enteric_mt=286.0, enteric_share=dict(feedlot=0.20, dairy=0.12, grazing=0.68),   # ~9.6 Mt CH4 x 29.8 [A]
          tank_yield_t_ha=30.0, tank_cost_t=3000.0)
# ------------------------------------------------------------------------------------------------ 11. Taiwan overrides
TAIWAN = dict(
    BASE=BASE_TAIWAN,
    ELEC=dict(cap_onw_twh=15.0, cap_onw2_twh=0.0, cap_pv_twh=60.0, cap_csp_twh=0.0, cap_lwr_twh=60.0, liq_import_cap_twh=1e4,
              onshore_wind=45.0, solar=50.0, osw_fixed=95.0, osw_floating=120.0, lwr=90.0, td_adder=25.0, export_cap_twh=20.0,
              export_value=40.0),
    BIOMASS=dict(tiers=[("Taiwan rice straw and crop residues", "taiwan", 2.0, 50.0),
                        ("Taiwan forestry and wood residues", "taiwan", 0.5, 70.0)], hhv_gj_t=18.0),
    ETHANOL_FEEDS=[("tw_molasses", "Taiwan sugarcane molasses", "taiwan", 0.01, 2.0, 0.0)],
    OIL_FEEDS=[("tw_uco", "Taiwan used cooking oil", "taiwan", 0.1, 850.0)],
    BAMBOO_MHA=0.05, HEMP_MAX=0.0,
    GAS=dict(price_mmbtu=11.0, delivery_mmbtu=1.0),
    VEH=dict(ldv_stock_m=8.5, ers_trucks_m=0.05, fcev_trucks_m=0.02, bev_trucks_m=0.9, re_trucks_m=0.05, tractors_m=0.1,
             constr_m=0.1, forklifts_m=0.1, ers_km=1000.0, ers_capex_m_per_km=3.0, rail_elec_capex_bn=1.0, farm_charging_bn_yr=0.02),
    CARBON_SCALE=0.05, FOOD_SCALE=0.03,
    REACTOR_COST_MULT=1.4,     # small first fleet, imported technology [A]
)
