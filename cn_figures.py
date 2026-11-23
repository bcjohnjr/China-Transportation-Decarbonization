"""Figures for CN v1.6.3 (Clean Energy format: 177 mm wide, 300 dpi; PNG for the manuscript, TIFF for submission).
Reads the stored outputs in this folder.  Colours: validated categorical palette, fixed slot order."""
import csv, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import cn_inputs as I
import cn_basemap as BM

H = Path(__file__).resolve().parent
S = json.load(open(H / "cn_scenarios.json"))
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
GREY, INK, INK2, GRID = "#8a8985", "#0b0b0b", "#52514e", "#e4e3df"
W = 177 / 25.4
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "axes.axisbelow": True, "legend.frameon": False, "savefig.dpi": 300})


LAYOUT = {}   # CN v1.6.3: every figure is checked for text on graphics and overlapping text before it is saved


def save(fig, name, tight=True):
    from cn_layout_check import check
    LAYOUT[name] = check(fig, name)
    kw = dict(bbox_inches="tight") if tight else {}
    fig.savefig(H / f"{name}.png", **kw); fig.savefig(H / f"{name}.tif", pil_kwargs={"compression": "tiff_lzw"}, **kw)
    plt.close(fig)


def panel(ax, letter): ax.text(-0.08, 1.04, letter, transform=ax.transAxes, fontweight="bold", fontsize=10, va="bottom")


# ------------------------------------------------------------------ Fig 1: energy and emissions
def fig1():
    lc, pg = S["least_cost"], S["post_gas_least_cost"]; eu = lc["enduse"]; B = I.BASE_MAINLAND; K = I.KWH_PER_KG
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, 2.9), gridspec_kw=dict(width_ratios=[1.1, 1]))
    fuels = [("Gasoline", B["gasoline_mt"] * K["gasoline"]),
             ("Diesel", (B["onroad_diesel_mt"] + B["rail_diesel_mt"] + B["marine_diesel_mt"] + B["farm_diesel_mt"] + B["construction_mining_diesel_mt"] + B["industrial_trucks_mt"]) * K["diesel"]),
             ("Jet fuel", B["jet_mt"] * K["jet"]), ("Fuel oil (bunkers)", B["marine_resid_mt"] * K["resid"]),
             ("Natural gas (trucks, pipelines)", (B["road_gas_bcm"] + B["pipeline_gas_bcm"]) * I.BCM_TWH)]
    carriers = [("Electricity", eu["el_total"]), ("Hydrogen", sum(eu["h2_twh"].values())), ("Renewable liquids", eu["liq_total"]),
                ("Residual pipeline gas", eu["gas_resid_twh"])]
    x0 = 0; bottom = 0
    for i, (nm, v) in enumerate(fuels):
        a.bar(0, v, 0.6, bottom=bottom, color=C[i], edgecolor="white", linewidth=1.0, label=nm); bottom += v
    tot25 = bottom; bottom = 0; h25 = a.get_legend_handles_labels()
    cc = [C[5], C[6], C[7], GREY]
    for i, (nm, v) in enumerate(carriers):
        a.bar(1, v, 0.6, bottom=bottom, color=cc[i], edgecolor="white", linewidth=1.0, label=nm); bottom += v
    a.text(0, tot25 + 80, f"{tot25:,.0f} TWh", ha="center", color=INK); a.text(1, bottom + 80, f"{bottom:,.0f} TWh", ha="center", color=INK)
    a.set_xticks([0, 1], ["2025\nfuel use", "2050 least cost\n(+15% services)"], fontsize=6.8); a.set_ylabel("Final energy (TWh/yr)"); a.set_xlim(-0.5, 3.3)
    hh, ll = a.get_legend_handles_labels()
    l1 = a.legend(hh[:5], ll[:5], loc="upper left", fontsize=6.2, title="2025", title_fontsize=6.5, alignment="left", bbox_to_anchor=(0.53, 1.0)); a.add_artist(l1)
    a.legend(hh[5:], ll[5:], loc="upper left", fontsize=6.2, title="2050", title_fontsize=6.5, alignment="left", bbox_to_anchor=(0.53, 0.52))
    a.grid(axis="x", visible=False); panel(a, "A")
    vals = [("All China\nfossil CO$_2$\n2025", 0.32 * 38.1), ("Transport\nWTW\n2025", lc["emissions"]["baseline_2025_wtw_mt"] / 1e3),
            ("Petroleum\nbaseline\n2050", lc["emissions"]["baseline_wtw_mt"] / 1e3), ("System,\ngas era\n2050", lc["emissions"]["total_mt"] / 1e3),
            ("System,\nafter gas\n2050", pg["emissions"]["total_mt"] / 1e3)]
    col = [GREY, INK2, INK2, C[0], C[2]]
    b.bar(range(len(vals)), [v for _, v in vals], 0.6, color=col, edgecolor="white")
    for i, (_, v) in enumerate(vals): b.text(i, v + 0.15, f"{v:.2f}", ha="center", color=INK)
    b.set_xticks(range(len(vals)), [n for n, _ in vals], fontsize=6.5); b.set_ylabel("Gt CO$_2$e per year"); b.grid(axis="x", visible=False); panel(b, "B")
    fig.tight_layout(); save(fig, "Fig1_energy_and_emissions")


# ------------------------------------------------------------------ Fig 2: schematic map
# CN v1.6.3: every label sits in clear space (checked by cn_layout_check); labels that cannot sit inside their area are
# joined to it by a thin leader.  (text, x, y, ha, kind, leader-to (lon, lat) or None)
MAP_LABELS = [
    ('Xinjiang\nUyghur AR', 86.15, 45.14, 'center', 'region', None),
    ('Xizang\n(Tibet) AR', 89.50, 32.80, 'center', 'region', None),
    ('Inner Mongolia AR', 101.50, 44.40, 'center', 'region', (103.00, 41.60)),
    ('Ningxia Hui AR', 99.00, 35.40, 'center', 'region', (105.90, 36.60)),
    ('Guangxi Zhuang AR', 101.87, 20.73, 'center', 'region', (107.60, 23.90)),
    ('sweet sorghum,\nsweet potato', 99.24, 33.92, 'center', 'biomass', None),
    ('cassava, sugarcane,\njatropha, bamboo', 101.97, 19.30, 'center', 'biomass', None),
    ('cotton stalks,\nsweet sorghum,\noilseed residues', 84.00, 39.00, 'center', 'biomass', None),
    ('grassland and forestry\nresidues, yak-dung biogas', 85.20, 26.80, 'center', 'biomass', (86.50, 31.50)),
    ('sweet sorghum,\nmaize stover,\nJerusalem artichoke,\nhemp', 110.72, 47.84, 'center', 'biomass', (111.00, 41.60)),
    ('crop straw\n(maize, wheat)', 126.02, 34.69, 'center', 'biomass', (116.00, 35.50)),
    ('rice straw,\nbamboo', 116.00, 27.30, 'center', 'biomass', None),
    ('hemp, maize stover', 127.50, 47.50, 'center', 'biomass', None),
    ('Beijing', 115.50, 39.50, 'right', 'city', None),
    ('Shanghai', 121.95, 31.20, 'left', 'city', None),
    ('Taipei', 121.95, 25.05, 'left', 'city', None),
    ('Hohhot', 110.69, 41.58, 'right', 'city', None),
    ('Lhasa', 91.55, 29.65, 'left', 'city', None),
    ('Urumqi', 90.20, 43.80, 'left', 'city', (87.60, 43.80)),
    ('Chengdu', 103.78, 30.45, 'right', 'city', None),
    ('Wuhan', 114.57, 29.83, 'left', 'city', None),
    ('Yinchuan', 104.90, 40.23, 'right', 'city', (106.20, 38.50)),
    ('Nanning', 107.70, 24.20, 'left', 'city', None),
    ('Hong Kong', 114.91, 21.73, 'left', 'city', None),
    ('Macau', 113.40, 21.10, 'center', 'city', (113.55, 22.20)),
]


MAP_BOX = {"guangdong": (111.5, 19.7, 4.0, 0.9)}   # schematic zone box drawn a little offshore to leave room for the Pearl River Delta labels


def map_label_style(kind):
    return dict(region=dict(fontsize=6.5, color=INK, style="italic"), city=dict(fontsize=6, color=INK),
                biomass=dict(fontsize=5.6, color=C[5]))[kind]


def fig2(labels=True):
    fig, ax = plt.subplots(figsize=(W, W * 0.86)); ax.grid(False)
    ax.add_patch(Polygon(BM.OUTLINE, closed=True, fc="#f4f3ef", ec=INK2, lw=0.6))
    for poly in (BM.HAINAN, BM.TAIWAN): ax.add_patch(Polygon(poly, closed=True, fc="#f4f3ef", ec=INK2, lw=0.6))
    for k, poly in BM.AUTONOMOUS_REGIONS.items():
        ax.add_patch(Polygon(poly, closed=True, fc=C[3], alpha=0.18, ec=C[3], lw=0.8, gid="bg"))
    for a_, b_ in BM.ERS_CORRIDORS:
        p, q = BM.CITIES[a_], BM.CITIES[b_]; ax.plot([p[0], q[0]], [p[1], q[1]], color=C[0], lw=1.4, solid_capstyle="round", zorder=3)
    for nm, (x, y) in BM.HUBS.items(): ax.plot(x, y, "o", ms=6, mfc=C[7], mec="white", mew=1.0, zorder=5)
    for x, y in BM.SOLAR_BASES: ax.plot(x, y, "*", ms=10, mfc=C[1], mec="white", mew=0.6, zorder=4)
    colmap = {"cold_kelp": C[2], "kelp_red_rotation": C[6], "red_green": C[5], "tropical_red": C[4]}
    for z in I.SEAWEED + I.SEAWEED_TAIWAN:
        x0, y0, w, h = MAP_BOX.get(z[0], z[11]); ax.add_patch(Rectangle((x0, y0), w, h, fc=colmap[z[12]], alpha=0.75, ec="white", lw=0.6, zorder=4))
    for z in I.BIOEXTRACT:   # CN v1.5 nearshore farms in nutrient-polluted bays
        ax.plot(z[10], z[11], "^", ms=6.5, mfc=C[5], mec=INK, mew=0.6, zorder=6)
    for nm in ("Beijing", "Shanghai", "Hong Kong", "Macau", "Taipei", "Nanning", "Hohhot", "Yinchuan", "Lhasa", "Urumqi", "Chengdu", "Wuhan"):
        x, y = BM.CITIES[nm]; ax.plot(x, y, "s", ms=2.5, color=INK, zorder=6)
    if labels:
        for txt, x, y, ha, kind, lead in MAP_LABELS:
            st = map_label_style(kind)
            if lead is None: ax.text(x, y, txt, ha=ha, va="center", zorder=8, **st)
            else: ax.annotate(txt, lead, (x, y), ha=ha, va="center", zorder=8, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.5, shrinkA=1.5, shrinkB=1.5), **st)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    hl = [Line2D([], [], color=C[0], lw=1.4, label="Electric expressway corridors"),
          Line2D([], [], ls="", marker="o", mfc=C[7], mec="white", ms=6, label="Reactor hubs: power, hydrogen, process heat"),
          Line2D([], [], ls="", marker="*", mfc=C[1], mec="white", ms=10, label="Desert wind, solar and CSP bases"),
          Patch(fc=C[3], alpha=0.3, label="Autonomous regions"), Patch(fc=C[2], label="Offshore wind + kelp (Saccharina)"),
          Patch(fc=C[6], label="Offshore wind + kelp/red rotation"), Patch(fc=C[5], label="Offshore wind + Gracilaria/Ulva"),
          Patch(fc=C[4], label="Offshore wind + tropical reds"),
          Line2D([], [], ls="", marker="^", mfc=C[5], mec=INK, mew=0.6, ms=6.5, label="Nearshore seaweed in eutrophic bays")]
    ax.legend(handles=hl, loc="upper center", bbox_to_anchor=(0.5, 0.0), fontsize=6.2, ncol=3, frameon=False, columnspacing=1.2, handlelength=1.6)
    ax.set_xlim(72, 136); ax.set_ylim(15.5, 54.5); ax.set_aspect(1.15); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.text(72.5, 15.8, "Schematic; boundaries generalised and not authoritative.", ha="left", fontsize=5.5, color=INK2)
    if not labels: return fig, ax
    save(fig, "Fig2_system_map")


# ------------------------------------------------------------------ Fig 3: cost versus petroleum
GROUPS = [("Electricity, grids, charging, electric roads", ("electricity_generation", "transmission_distribution", "charging", "electric_highways", "rail_electrification", "farm_charging")),
          ("Reactor hubs and hydrogen", ("reactor_hubs", "pyrolysis_plants", "natural_gas", "electrolysis", "h2_delivery")),
          ("Land biofuels", ("land_biomass", "hemp_net_of_meal", "biorefineries", "hefa_oils", "sugar_starch_ethanol")),
          ("Offshore seaweed", ("seaweed_farms_harvest_haul", "seaweed_refining")),
          ("Other (heat equipment, residual gas, imports)", ("process_heat_equipment", "residual_pipeline_gas", "imported_renewable_fuel")),
          ("Nutrient and soil-carbon return, fertiliser, nearshore farms", ("nutrient_and_carbon_return", "mineral_fertiliser", "nearshore_seaweed_farms", "seaweed_to_soil_handling", "soil_carbon_deficit",
                                                                            "green_manure_and_compost"))]
GROUP_COL = [C[0], C[1], C[2], C[3], C[5], C[6]]


def fig3():
    """CN v1.6.3: panel A is the energy-system (project) cost; the net extra cost of owning electric vehicles and machines
    is paid by their owners and is shown separately in panel B."""
    cases = [("least_cost", "Least\ncost"), ("design_half_offshore", "230 GW\noffshore"), ("post_gas_least_cost", "After\ngas"),
             ("least_cost_no_nuclear", "No\nnuclear"), ("sustainable_fission_tmsr", "Closed\nthorium\ncycle")]
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, 3.9), gridspec_kw=dict(width_ratios=[1.55, 1]))
    pet = S["least_cost"]["petroleum"]
    a.bar(0, pet["late_2025_bn"], 0.62, color=GREY, edgecolor="white"); a.bar(1, pet["nov_2026_bn"], 0.62, color="#b5b4ae", edgecolor="white")
    a.text(0, pet["late_2025_bn"] + 10, f"{pet['late_2025_bn']:.0f}", ha="center", fontsize=7); a.text(1, pet["nov_2026_bn"] + 10, f"{pet['nov_2026_bn']:.0f}", ha="center", fontsize=7)
    for i, (k, lab) in enumerate(cases):
        r = S[k]; bot = 0; x = i + 2
        for j, (gn, keys) in enumerate(GROUPS):
            v = sum(r["costs_bn"].get(kk, 0.0) for kk in keys)
            if v > 0: a.bar(x, v, 0.62, bottom=bot, color=GROUP_COL[j], edgecolor="white", linewidth=1.0); bot += v
        cr = sum(r["credits_bn"].values()); a.bar(x, cr, 0.62, color=C[7], edgecolor="white")
        a.plot([x - 0.36, x + 0.36], [r["energy_system_cost_bn"]] * 2, color=INK, lw=1.4)
        a.text(x, bot + 10, f"{r['energy_system_cost_bn']:.0f}", ha="center", fontsize=7)
    a.axhline(0, color=INK2, lw=0.6)
    a.set_xticks(range(len(cases) + 2), ["Petrol.\nlate\n2025", "Petrol.\nNov\n2026"] + [l for _, l in cases], fontsize=5.6)
    a.set_ylabel("2050 energy-system cost (US\\$ bn/yr, 2026)"); a.grid(axis="x", visible=False)
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    hd = [Patch(fc=GROUP_COL[j], label=gn) for j, (gn, _) in enumerate(GROUPS)] + [Patch(fc=C[7], label="Credits (carbon, biomethane, nutrients, power)"),
          Line2D([], [], color=INK, lw=1.4, label="Net energy-system cost")]
    a.legend(handles=hd, fontsize=5.6, loc="upper left", ncol=2, bbox_to_anchor=(-0.18, -0.25))
    a.set_ylim(-45, 620); a.set_xlim(-0.6, len(cases) + 1.6); panel(a, "A")
    rows = [("China, least cost", "least_cost"), ("China, 230 GW offshore", "design_half_offshore"), ("China, after gas", "post_gas_least_cost"),
            ("China, no nuclear", "least_cost_no_nuclear"), ("China, closed thorium cycle", "sustainable_fission_tmsr"), ("Taiwan, least cost", "tw_least_cost")]
    y = np.arange(len(rows))[::-1] * 1.0; h = 0.36
    pv = [S[k]["saving_energy_system_pct"] for _, k in rows]; tv = [S[k]["saving_vs_late_2025_pct"] for _, k in rows]
    b.barh(y + h / 2, pv, h, color=C[0], edgecolor="white", label="Energy system (project cost)")
    b.barh(y - h / 2, tv, h, color="#b5b4ae", edgecolor="white", label="Including vehicle costs paid by owners")
    for yy, v in list(zip(y + h / 2, pv)) + list(zip(y - h / 2, tv)):
        b.text(v + (1.2 if v >= 0 else -1.2), yy, f"{v:.1f}%", va="center", ha="left" if v >= 0 else "right", fontsize=6)
    b.axvline(0, color=INK2, lw=0.6)
    b.set_yticks(y, [n for n, _ in rows], fontsize=6.3); b.set_xlabel("Saving vs late-2025 pre-tax petroleum (%)")
    lo = min(pv + tv); hi = max(pv + tv); b.set_xlim(min(-10, lo - 16), hi + 14)
    b.set_ylim(-0.75, len(rows) - 0.35)
    b.legend(fontsize=5.8, loc="upper left", bbox_to_anchor=(-0.05, -0.2), ncol=1)
    b.grid(axis="y", visible=False); panel(b, "B")
    fig.tight_layout(); save(fig, "Fig3_cost_vs_petroleum")


# ------------------------------------------------------------------ Fig 4: Monte Carlo and break-even
def fig4():
    """CN v1.6.3: energy-system (project) saving; the least-cost case including owners' vehicle costs is shown for comparison."""
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, 3.4))
    files = [("cn_monte_carlo_least_cost.csv", "Least cost", C[0]), ("cn_monte_carlo_half_offshore.csv", "230 GW offshore", C[1]),
             ("cn_monte_carlo_post_gas.csv", "After gas", C[2])]
    bins = np.arange(-40, 71, 2.5); top = 0
    for fn, lab, col in files:
        sv = [float(r["saving_energy_system_pct"]) for r in csv.DictReader(open(H / fn))]
        n_, _, _ = a.hist(sv, bins=bins, histtype="step", lw=1.5, color=col, label=f"{lab} (median {np.median(sv):.0f}%)"); top = max(top, n_.max())
    sv = [float(r["saving_pct"]) for r in csv.DictReader(open(H / files[0][0]))]
    n_, _, _ = a.hist(sv, bins=bins, histtype="step", lw=1.0, ls="--", color=GREY, label=f"Least cost incl. owners' vehicle costs (median {np.median(sv):.0f}%)"); top = max(top, n_.max())
    a.axvline(0, color=INK2, lw=0.6)
    a.set_xlabel("Saving vs late-2025 petroleum (%)"); a.set_ylabel("Draws"); a.set_ylim(0, top * 1.1); a.set_xlim(-42, 72)
    a.legend(fontsize=5.6, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=1, handlelength=1.6); panel(a, "A")
    be = list(csv.DictReader(open(H / "cn_breakeven.csv")))
    for (case, lab, col, basis, ls) in (("least_cost", "Least cost", C[0], "energy_system", "-"), ("half_offshore_230gw", "230 GW offshore", C[1], "energy_system", "-"),
                                        ("post_gas", "After gas", C[2], "energy_system", "-"),
                                        ("least_cost", "Least cost incl. owners' vehicle costs", GREY, "with_vehicles", "--")):
        rr = [r for r in be if r["case"] == case and r["basis"] == basis]
        b.plot([float(r["petroleum_price_multiple"]) for r in rr], [100 * float(r["share_cheaper"]) for r in rr], color=col, lw=1.8 if ls == "-" else 1.2, ls=ls, label=lab)
    nov = S["least_cost"]["petroleum"]["nov_2026_bn"] / S["least_cost"]["petroleum"]["late_2025_bn"]
    b.axvline(1.0, color=INK2, lw=0.6); b.axvline(nov, color=INK2, ls=":", lw=0.9)
    b.text(1.0, 101.5, "late 2025", fontsize=5.8, color=INK2, ha="center", va="bottom"); b.text(nov, 101.5, "Nov 2026", fontsize=5.8, color=INK2, ha="center", va="bottom")
    b.set_ylim(0, 100); b.set_xlim(0.5, 2.0)
    b.set_xlabel("Petroleum price (× late-2025 pre-tax)"); b.set_ylabel("Draws cheaper than petroleum (%)")
    b.legend(fontsize=5.6, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, handlelength=1.8)
    panel(b, "B")
    fig.tight_layout(); save(fig, "Fig4_uncertainty_breakeven")


# ------------------------------------------------------------------ Fig 5: reactor types and start-up fissile
def fig5():
    types = list(I.REACTOR_TYPES)
    lab = {"htr_pm": "HTR-PM\nHTGR", "vhtr": "950 °C\nVHTR", "tmsr": "Thorium\nMSR", "cfr": "Sodium fast\n(CFR)", "acp100": "LW SMR\n(ACP100)"}
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, 2.8), gridspec_kw=dict(width_ratios=[1.25, 1]))
    x = np.arange(len(types)); w = 0.38
    g = [S[f"type_{t}"]["energy_system_cost_bn"] for t in types]; pg = [S[f"post_gas_type_{t}"]["energy_system_cost_bn"] for t in types]
    a.bar(x - w / 2, g, w, color=C[0], edgecolor="white", label="Gas era (steam electrolysis + pyrolysis)"); a.bar(x + w / 2, pg, w, color=C[2], edgecolor="white", label="After gas (steam electrolysis only)")
    for i in range(len(types)):
        a.text(x[i] - w / 2, g[i] + 4, f"{g[i]:.0f}", ha="center", fontsize=6); a.text(x[i] + w / 2, pg[i] + 4, f"{pg[i]:.0f}", ha="center", fontsize=6)
    pet = S["least_cost"]["petroleum"]["late_2025_bn"]
    a.axhline(pet, color=GREY, ls="--", lw=0.9); a.text(-0.35, pet + 14, "petroleum, late 2025", fontsize=6, color=INK2, va="bottom")
    a.set_xticks(x, [lab[t] for t in types], fontsize=6.5); a.set_ylabel("2050 energy-system cost (US\\$ bn)"); a.set_ylim(0, 640); a.set_xlim(-0.55, len(types) - 0.45)
    a.legend(fontsize=5.8, loc="upper right", ncol=1)
    a.grid(axis="x", visible=False); panel(a, "A")
    fs_t = S["sustainable_fission_tmsr"]["fuel_supply"]; fs_c = S["sustainable_fission_cfr"]["fuel_supply"]
    bars = [("Sodium-fast fleet:\nPu to start", fs_c["startup_fast_pu_t"], C[7]), ("Thorium MSR fleet:\nfissile to start", fs_t["startup_msr_fissile_t"], C[3]),
            ("Pu in China's spent\nfuel by 2050", fs_t["china_snf_pu_2050_t"], GREY), ("Pu in spent\nfuel, 2024", fs_t["china_snf_pu_2024_t"], GREY),
            ("Military Pu\n(IPFM estimate)", fs_t["china_military_pu_t"], GREY)]
    y = np.arange(len(bars))[::-1]
    b.barh(y, [v for _, v, _ in bars], 0.6, color=[c for *_, c in bars], edgecolor="white"); b.set_xscale("log")
    for yy, (_, v, _) in zip(y, bars): b.text(v * 1.15, yy, f"{v:,.0f} t" if v >= 10 else f"{v:.1f} t", va="center", fontsize=6.5)
    b.set_yticks(y, [n for n, *_ in bars], fontsize=6.3); b.set_xlabel("Tonnes of fissile material (log scale)"); b.set_xlim(1, 3e4)
    b.grid(axis="y", visible=False); panel(b, "B")
    fig.tight_layout(); save(fig, "Fig5_reactor_types_fissile")


# ------------------------------------------------------------------ Fig 6: gas balance
def fig6():
    g = json.load(open(H / "cn_gas_depletion.json")); rows = [r for r in g["rows"]["programme"] if r["year"] <= 2160]
    yrs = [r["year"] for r in rows]
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, 3.1), gridspec_kw=dict(width_ratios=[1.4, 1]))
    a.stackplot(yrs, [r["domestic_bcm"] for r in rows], [r["pipeline_bcm"] for r in rows], [r["lng_bcm"] for r in rows],
                colors=[C[0], C[2], C[3]], labels=["Domestic production", "Pipeline imports", "LNG imports"], edgecolor="white", linewidth=0.5)
    a.plot(yrs, [r["demand_bcm"] for r in rows], color=INK, lw=1.4, label="Demand with pyrolysis programme")
    r0 = [r for r in g["rows"]["no_programme"] if r["year"] <= 2160]; a.plot([r["year"] for r in r0], [r["demand_bcm"] for r in r0], color=INK, ls="--", lw=1.0, label="Demand without programme")
    sy = g["summary"]["programme"]["first_shortfall_year"]; a.axvline(sy, color=C[7], lw=1.0)
    a.text(sy, 1.015, f"first shortfall {sy}", transform=a.get_xaxis_transform(), ha="center", va="bottom", fontsize=6, color=C[7])
    a.set_ylabel("Natural gas (bcm/yr)"); a.set_xlim(2026, 2160); a.set_ylim(0, 600)
    a.legend(fontsize=5.6, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2); panel(a, "A")
    keys = [("programme_rec40", "40% recovery"), ("programme_pipe_pool10", "Pipeline pool 10 tcm"), ("programme_no_lng_growth", "LNG held at 2025"),
            ("programme", "Central"), ("programme_lng_200", "LNG ceiling 200 bcm"), ("programme_heat_pumps", "+ building heat pumps"),
            ("programme_heat_pumps_biogas_high", "+ heat pumps, high biogas"), ("programme_rec80", "80% recovery")]
    y = np.arange(len(keys))[::-1]; v = [g["summary"][k]["first_shortfall_year"] for k, _ in keys]
    b.barh(y, [vv - 2050 for vv in v], 0.6, left=2050, color=[C[0] if k == "programme" else GREY for k, _ in keys], edgecolor="white")
    for yy, vv in zip(y, v): b.text(vv + 1, yy, str(vv), va="center", fontsize=6.5)
    b.set_yticks(y, [l for _, l in keys], fontsize=6.3); b.set_xlim(2050, 2180); b.set_xlabel("First gas shortfall year"); b.grid(axis="y", visible=False); panel(b, "B")
    fig.tight_layout(); save(fig, "Fig6_gas_supply")


# ------------------------------------------------------------------ Fig 7: regions
def fig7():
    R = json.load(open(H / "cn_regional_screen.json"))["rows"]
    keep = [r for r in R if r["region"] in ("guangxi", "inner_mongolia", "ningxia", "xizang", "xinjiang", "hong_kong", "macau", "tw_least_cost")]
    names = [r["name"].replace(" (island system, nuclear hubs allowed)", "").replace(" AR", "") for r in keep]
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, 3.3))
    y = np.arange(len(keep))[::-1]; h = 0.38
    a.barh(y + h / 2, [r["liquids_twh"] for r in keep], h, color=C[1], edgecolor="white", label="2050 liquid-fuel demand")
    a.barh(y - h / 2, [r.get("supply_liquid_twh", 0.0) if not r["region"].startswith("tw_") else r["liquids_twh"] - r["imported_liquids_twh"] for r in keep], h,
           color=C[5], edgecolor="white", label="Liquids from the region's own feedstocks")
    a.set_yticks(y, names, fontsize=6.5); a.set_xlabel("TWh/yr"); a.legend(fontsize=6, loc="upper center", bbox_to_anchor=(0.45, -0.2)); a.grid(axis="y", visible=False); panel(a, "A")
    b.barh(y + h / 2, [r["baseline_wtw_mt"] for r in keep], h, color=C[7], edgecolor="white", label="Petroleum baseline, 2050")
    b.barh(y - h / 2, [r["system_emissions_mt"] for r in keep], h, color=C[0], edgecolor="white", label="Least-cost system")
    b.set_yticks(y, ["" for _ in keep]); b.set_xlabel("Well-to-wheel Mt CO$_2$e/yr"); b.legend(fontsize=6, loc="upper center", bbox_to_anchor=(0.5, -0.2)); b.grid(axis="y", visible=False); panel(b, "B")
    fig.tight_layout(); save(fig, "Fig7_regions")


# ------------------------------------------------------------------ Fig 8: food and cross-feeding
def fig8():
    f = S["least_cost"]["food"]; cf = json.load(open(H / "cn_crossfeed.json"))["least_cost"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, 2.7), gridspec_kw=dict(width_ratios=[1, 1.3]))
    items = [("Greenhouse\nvegetables", f["vegetables_mt"]), ("RAS fish", f["fish_mt"]), ("RAS shrimp", f["shrimp_mt"]),
             ("Grain dried", f["grain_dried_mt"]), ("Seaweed food\ndried", f["seaweed_food_dried_mt"]), ("Hemp meal", f["hemp_meal_mt"])]
    a.bar(range(len(items)), [v for _, v in items], 0.6, color=[C[5], C[0], C[4], C[3], C[2], C[6]], edgecolor="white"); a.set_yscale("log")
    for i, (_, v) in enumerate(items): a.text(i, v * 1.15, f"{v:.1f}", ha="center", fontsize=6.5)
    a.set_xticks(range(len(items)), [n.replace("\n", " ") for n, _ in items], fontsize=6, rotation=35, ha="right", rotation_mode="anchor"); a.set_ylabel("Mt per year (log scale)"); a.grid(axis="x", visible=False); panel(a, "A")
    fl = cf["flows_t"]
    flows = [("Fishmeal → shrimp feed", fl["fishmeal_to_shrimp"]), ("Fishmeal → fish feed", fl["fishmeal_to_fish"]), ("Shrimp meal → fish feed", fl["shrimpmeal_to_fish"]),
             ("Insect meal → fish feed", fl["insect_to_fish"]), ("Hemp meal → fish feed", fl["hemp_meal_to_fish"]), ("Ulva → abalone", fl["ulva_to_abalone"]),
             ("Ulva → fish feed", fl["ulva_to_fish"]), ("Kelp → abalone, sea cucumber", fl["kelp_to_abalone_and_sea_cucumber"])]
    y = np.arange(len(flows))[::-1]
    b.barh(y, [v / 1e3 for _, v in flows], 0.6, color=C[0], edgecolor="white")
    for yy, (_, v) in zip(y, flows): b.text(v / 1e3 + 5, yy, f"{v/1e3:,.0f}", va="center", fontsize=6.3)
    b.set_yticks(y, [n for n, _ in flows], fontsize=6.3); b.set_xlabel("kt per year"); b.grid(axis="y", visible=False); panel(b, "B")
    b.set_title(f"Marine protein for fish and shrimp feed met internally: {100*cf['marine_protein_need_met_internally']:.0f}%", fontsize=6.8, loc="left", color=INK2)
    fig.tight_layout(); save(fig, "Fig8_food_crossfeed")


# ------------------------------------------------------------------ supplementary
def figS():
    sm = list(csv.DictReader(open(H / "cn_sweep_merit.csv")))
    fig, a = plt.subplots(figsize=(W * 0.62, 2.6))
    for (yl, pg, lab, col) in (("1", "False", "Design yields, gas era", C[0]), ("2", "False", "Learning yields, gas era", C[1]), ("1", "True", "Design yields, after gas", C[2])):
        rr = [r for r in sm if r["yield_level"] == yl and r["post_gas"] == pg]
        veh = S["least_cost"]["consumer_vehicle_cost_bn"]   # CN v1.6.3: owners' vehicle costs (the same in every sweep case) excluded
        a.plot([float(r["osw_gw"]) for r in rr], [float(r["cost_bn"]) - veh for r in rr], "-o", ms=3.5, color=col, lw=1.6, label=lab)
    a.axhline(S["least_cost"]["petroleum"]["late_2025_bn"], color=GREY, ls="--", lw=0.9); a.text(5, S["least_cost"]["petroleum"]["late_2025_bn"] + 4, "petroleum, late 2025", fontsize=6, color=INK2)
    a.set_xlabel("Offshore wind with seaweed (GW), zones added in merit order"); a.set_ylabel("2050 energy-system cost (US\\$ bn)"); a.legend(fontsize=6)
    fig.tight_layout(); save(fig, "FigS1_offshore_merit")
    t = json.load(open(H / "cn_transition.json"))["rows"]
    fig, a = plt.subplots(figsize=(W * 0.62, 2.4))
    a.plot([r["year"] for r in t], [r["baseline_mt"] / 1e3 for r in t], color=C[7], lw=1.6, label="Petroleum baseline")
    a.plot([r["year"] for r in t], [r["case_mt"] / 1e3 for r in t], color=C[0], lw=1.6, label="Phased transition")
    a.fill_between([r["year"] for r in t], [r["case_mt"] / 1e3 for r in t], [r["baseline_mt"] / 1e3 for r in t], color=C[0], alpha=0.12)
    a.set_ylabel("Gt CO$_2$e/yr (WTW)"); a.legend(fontsize=6); fig.tight_layout(); save(fig, "FigS2_transition")
    sens = json.load(open(H / "cn_monte_carlo_summary.json"))["sensitivity_least_cost_energy_system"]
    top = sorted(sens.items(), key=lambda kv: -abs(kv[1]))[:12]
    fig, a = plt.subplots(figsize=(W * 0.62, 2.8)); y = np.arange(len(top))[::-1]
    a.barh(y, [v for _, v in top], 0.6, color=[C[7] if v > 0 else C[0] for _, v in top], edgecolor="white")
    a.set_yticks(y, [k.replace("/", ": ") for k, _ in top], fontsize=6); a.axvline(0, color=INK2, lw=0.6); a.set_xlabel("Spearman ρ with least-cost energy-system cost")
    a.grid(axis="y", visible=False); fig.tight_layout(); save(fig, "FigS3_sensitivity")
    import cn_model as M
    n = np.arange(1, 4001); fig, a = plt.subplots(figsize=(W * 0.62, 2.4))
    for case, col in (("low", C[2]), ("central", C[0]), ("high", C[7])):
        c = I.REACTOR_COST[case]; foak = c["boak_kwe"] * c["foak_mult"]; bb = np.log2(1 - c["learning"])
        a.plot(n, foak * n ** bb * (1 + c["idc"]), color=col, lw=1.6, label=f"{case}: FOAK {foak:,.0f} $/kWe, learning {100*c['learning']:.0f}%")
    a.axvline(S["least_cost"]["reactors"], color=INK2, ls=":", lw=0.9); a.text(S["least_cost"]["reactors"] * 1.08, 5000, "least-cost\nfleet", fontsize=6, color=INK2, va="center")
    a.set_xscale("log"); a.set_xlabel("Cumulative 250-MWt modules"); a.set_ylabel("Unit cost incl. interest (US$/kWe)"); a.legend(fontsize=5.8)
    fig.tight_layout(); save(fig, "FigS4_reactor_learning")


def figS5():
    """Robustness and stress cases against petroleum (CN v1.6)."""
    RB = json.load(open(H / "cn_robustness.json"))["cases"]
    short = dict(least_cost_bev_tco_low="Electric-car cost, low derivation", least_cost_fleet_500="Car stock 500 million",
                 least_cost_fleet_350="Car stock 350 million", least_cost_hub_cap_60="At most 60 hubs", least_cost_hub_cap_30="At most 30 hubs",
                 least_cost_carbon_commodity="Commodity carbon only", least_cost_grid_tight="Tight grid and firming",
                 least_cost_no_carbon_revenue="No carbon revenue", least_cost_residues_75="Residues −25%", least_cost_residues_50="Residues −50%",
                 least_cost_bev_net_zero="No electric-car cost advantage", least_cost_bev_plus100="Electric cars +100 USD/yr",
                 least_cost_bev_plus100_no_carbon="Electric cars +100, no carbon revenue", least_cost_stress_moderate="Combined, moderate",
                 post_gas_stress_moderate="Combined, moderate, after gas", least_cost_bev_tco_high="Electric-car cost, high derivation",
                 least_cost_stress_severe="Combined, severe",
                 least_cost_no_nutrient_balance="Without nutrient or soil-carbon constraints", least_cost_humification_high="Humification ×1.5",
                 least_cost_fertiliser_price_high="Fertiliser prices ×1.5", least_cost_bioextraction_full="Eutrophic bays farmed in full",
                 least_cost_bioextraction_n_credit_30="Bays farmed, N paid 30 USD/kg",
                 least_cost_soc_no_pyro_carbon="Pyrolysis carbon not soil carbon", post_gas_no_biomethane_pyrolysis="After gas, no biomethane pyrolysis",
                 least_cost_biological_soc="Biological soil carbon only", least_cost_biological_soc_no_compost="Biological soil C, no compost")
    # CN v1.6.3: bars are energy-system (project) costs; diamonds add the net cost of vehicles and machines paid by owners
    rows = [("Central case", S["least_cost"]["energy_system_cost_bn"], S["least_cost"]["transport_cost_bn"])] + sorted(
        ((short[k], v["energy_system_cost_bn"], v["transport_cost_bn"]) for k, v in RB.items() if k in short), key=lambda t: (t[1], t[2]))
    pet, pet26 = S["least_cost"]["petroleum"]["late_2025_bn"], S["least_cost"]["petroleum"]["nov_2026_bn"]
    fig, a = plt.subplots(figsize=(W * 0.8, 4.9)); y = np.arange(len(rows))[::-1]
    a.barh(y, [v for _, v, _ in rows], 0.62, color=[C[0] if v < pet else C[7] for _, v, _ in rows], edgecolor="white", label="Energy-system (project) cost; red if above late-2025 petroleum")
    a.plot([t for _, _, t in rows], y, "D", ms=3.2, mfc="white", mec=INK, mew=0.8, ls="", label="Including vehicle costs paid by owners")
    a.axvline(pet, color=GREY, ls="--", lw=0.9); a.axvline(pet26, color=GREY, ls=":", lw=0.9)
    for yy, (_, v, t) in zip(y, rows):   # value of the bar, just right of it (moved past a diamond or reference line in the way)
        x = v + 7
        for _ in range(3):
            if x - 9 < t < x + 32: x = t + 11
            for line in (pet, pet26):
                if x - 4 < line < x + 32: x = line + 7
        a.text(x, yy, f"{v:.0f}", va="center", fontsize=6)
    a.text(pet, len(rows) - 0.3, "petroleum,\nlate 2025", fontsize=5.8, color=INK2, va="bottom", ha="center")
    a.text(pet26, len(rows) - 0.3, "petroleum,\nNov 2026", fontsize=5.8, color=INK2, va="bottom", ha="center")
    a.set_yticks(y, [r[0] for r in rows], fontsize=6.3); a.set_xlabel("2050 annual cost (US\\$ bn)"); a.grid(axis="y", visible=False)
    a.set_ylim(-0.7, len(rows) - 0.4); a.set_xlim(0, max(max(v, t) for _, v, t in rows) * 1.12)
    a.legend(fontsize=6, loc="upper center", bbox_to_anchor=(0.4, -0.12), ncol=2)
    fig.tight_layout(); save(fig, "FigS5_robustness")


# ------------------------------------------------------------------ Fig 9: nutrient and soil-carbon balance (CN v1.5)
SRC = [("hydrochar", "HTL hydrochar"), ("digestate", "Digested HTL wastewater"), ("gasifier_ash", "Gasifier ash"),
       ("ethanol_stillage", "Ethanol stillage"), ("offshore_seaweed", "Offshore seaweed"), ("nearshore_seaweed", "Nearshore seaweed"),
       ("green_manure", "Green manure"), ("compost", "Manure compost"), ("mineral_fertiliser", "Mineral fertiliser")]


SRC_COL = dict(hydrochar=C[0], digestate=C[1], green_manure=C[2], compost=C[3], ethanol_stillage=C[4], nearshore_seaweed=C[5],
               gasifier_ash=C[6], offshore_seaweed="#8fd19e", mineral_fertiliser=GREY, seaweed=C[5], pyrolysis_carbon=INK2)


def fig9():
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(W, 2.9), gridspec_kw=dict(width_ratios=[1.15, 1.15, 1]))
    lc = S["least_cost"]["nutrients"]; pg = S["post_gas_least_cost"]["nutrients"]
    bars = [("N", lc["n"]), ("P", lc["p"]), ("K", lc["k"]), ("N", pg["n"]), ("P", pg["p"]), ("K", pg["k"])]
    xs = [0, 1, 2, 3.6, 4.6, 5.6]
    for x, (el, e) in zip(xs, bars):
        bot = 0.0; rem = e["removed_mt"]
        for j, (k, lab) in enumerate(SRC):
            v = 100 * e["returned_mt"][k] / rem
            if v > 0.05:
                a.bar(x, v, 0.72, bottom=bot, color=SRC_COL[k], edgecolor="white", lw=1.0,
                      label=lab if x == 0 or (lab not in [h.get_label() for h in a.patches]) else None); bot += v
        a.text(x, bot + 2, f"{rem:.2f}", ha="center", fontsize=5.6, color=INK2)
    hs, ls_ = a.get_legend_handles_labels(); seen = {}
    for h, l in zip(hs, ls_): seen.setdefault(l, h)
    a.axhline(100, color=INK, lw=0.7, ls="--")
    top = max(100 * sum(e["returned_mt"].values()) / e["removed_mt"] for _, e in bars)
    a.set_xticks(xs, [el for el, _ in bars]); a.set_ylabel("Returned, % of nutrient removed"); a.set_ylim(0, max(125, top + 18)); a.grid(axis="x", visible=False)
    a.text(1, -0.2, "Least cost", ha="center", va="top", fontsize=6.5, transform=a.get_xaxis_transform()); a.text(4.6, -0.2, "After gas", ha="center", va="top", fontsize=6.5, transform=a.get_xaxis_transform())
    a.legend(seen.values(), seen.keys(), fontsize=5.4, loc="upper center", bbox_to_anchor=(0.55, -0.31), ncol=2, handlelength=1.0, columnspacing=0.8)
    panel(a, "A")
    cases = [("least_cost", "Least\ncost"), ("post_gas_least_cost", "After\ngas"), ("least_cost_biological_soc", "Biol.\nonly"),
             ("least_cost_biological_soc_no_compost", "Biol., no\ncompost")]
    socs = [(k_, n_, SRC_COL[k_]) for k_, n_ in (("hydrochar", "HTL hydrochar"), ("digestate", "Digestate"), ("seaweed", "Seaweed"),
                                                  ("green_manure", "Green manure"), ("compost", "Manure compost"), ("pyrolysis_carbon", "Pyrolysis carbon"))]
    for i, (k, lab) in enumerate(cases):
        sc = S[k]["nutrients"]["soil_carbon"]; bot = 0.0
        for kk, nm, col in socs:
            v = sc["stable_soc_supplied_mt"].get(kk, 0.0)
            if v > 1e-6: b.bar(i, v, 0.66, bottom=bot, color=col, edgecolor="white", lw=1.0, label=nm if nm not in [t.get_text() for t in []] else None); bot += v
        gap = sc.get("deficit_mt", 0.0)
        if gap > 1e-6: b.bar(i, gap, 0.66, bottom=bot, color="white", edgecolor=GREY, hatch="////", lw=0.6, label="Not replaced (priced gap)"); bot += gap
        b.plot([i - 0.38, i + 0.38], [sc["stable_soc_required_mt"]] * 2, color=C[7], lw=1.6)
        extra = f"\n{S[k]['liq_import_twh']:.0f} TWh\nliquids short" if S[k]["liq_import_twh"] > 1 else ""
        b.text(i, max(bot, sc["stable_soc_required_mt"]) + 0.8, f"{S[k]['biomass_mt']['residues']:.0f} Mt\nresidues{extra}", ha="center", va="bottom", fontsize=5.0, color=INK2)
    hs, ls_ = b.get_legend_handles_labels(); seen = {}
    for h, l in zip(hs, ls_): seen.setdefault(l, h)
    from matplotlib.lines import Line2D
    seen["Required (residue C that\nwould have become SOC)"] = Line2D([], [], color=C[7], lw=1.6)
    b.set_xticks(range(len(cases)), [l for _, l in cases], fontsize=5.8); b.set_ylabel("Stable soil carbon (Mt C/yr)"); b.grid(axis="x", visible=False)
    b.set_ylim(0, max(S[k]["nutrients"]["soil_carbon"]["stable_soc_required_mt"] for k, _ in cases) * 1.55)
    b.legend(seen.values(), seen.keys(), fontsize=5.2, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, handlelength=1.0, columnspacing=0.6)
    panel(b, "B")
    bx = S["design_half_offshore"]["bioextraction"]; nm = {"liaodong_bay": "Liaodong Bay", "haizhou_bay": "Haizhou Bay", "yangtze_plume": "Yangtze plume",
                                                           "fujian_bays": "Fujian bays", "pearl_river": "Pearl River", "beibu_qinzhou": "Qinzhou Bay"}
    y = np.arange(len(bx))[::-1]
    c.barh(y, [z["n_removed_kt"] for z in bx], 0.62, color=C[5], edgecolor="white")
    for yy, z in zip(y, bx): c.text(z["n_removed_kt"] + 1, yy, f"{z['n_removed_kt']:.0f} N, {z['p_removed_kt']:.1f} P", va="center", fontsize=5.6)
    c.set_yticks(y, [nm[z["zone"]] for z in bx], fontsize=6); c.set_xlabel("Removed from the water (kt/yr)")
    c.set_xlim(0, max(z["n_removed_kt"] for z in bx) * 1.75); c.grid(axis="y", visible=False)
    tot = sum(z["n_removed_kt"] for z in bx)
    c.set_title(f"Total {tot:.0f} kt N/yr; all Chinese\nseaweed farms now ~75 kt N/yr", fontsize=5.8, color=INK2, loc="right")
    panel(c, "C")
    fig.tight_layout(); fig.subplots_adjust(bottom=0.36); save(fig, "Fig9_nutrient_soil_carbon")


# ------------------------------------------------------------------ Graphical abstract (CN v1.6): 5:2, 300 dpi
def graphical_abstract():
    MC = json.load(open(H / "cn_monte_carlo_summary.json")); RB_ = json.load(open(H / "cn_robustness.json"))
    lc = S["least_cost"]; br = RB_["lull_bracket"]["least_cost"]
    fig = plt.figure(figsize=(10, 4), dpi=300)
    fig.text(0.03, 0.90, "A petroleum-free transport system for China in 2050: annual least-cost planning model", fontsize=13, fontweight="bold", color=INK)
    fig.text(0.03, 0.82, "Electric vehicles and roads  ·  reactor heat hubs  ·  residue, bamboo, hemp and seaweed fuels  ·  nutrients and soil carbon returned to fields",
             fontsize=8.5, color=INK2)
    tiles = [(f"{lc['saving_energy_system_pct']:.1f}%", "lower energy-system cost than\npetroleum (late-2025 prices)", C[0]),
             (f"{MC['least_cost']['saving_energy_system_pct']['p50']:.1f}%", f"median across {MC['least_cost']['n']:,}\nuncertainty draws", C[1]),
             (f"{lc['saving_vs_late_2025_pct']:.1f}%", "including the vehicle costs\npaid by their owners", C[2]),
             (f"{lc['emissions']['reduction_pct']:.0f}%", "lower well-to-wheel\nemissions", C[5])]
    for i, (big, small, col) in enumerate(tiles):
        x0 = 0.03 + i * 0.24
        ax = fig.add_axes([x0, 0.22, 0.215, 0.5]); ax.set_xticks([]); ax.set_yticks([])
        for s_ in ax.spines.values(): s_.set_visible(False)
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color=col, alpha=0.10, lw=0, gid="bg"))
        ax.add_patch(plt.Rectangle((0, 0), 0.025, 1, transform=ax.transAxes, color=col, lw=0))
        ax.text(0.09, 0.62, big, fontsize=30, fontweight="bold", color=INK, transform=ax.transAxes, va="center")
        ax.text(0.09, 0.22, small, fontsize=8.2, color=INK2, transform=ax.transAxes, va="center")
    fig.text(0.03, 0.08, "Central 2050 case; energy-system cost excludes vehicle purchases, which owners pay. Annual resource adequacy, not hourly operation.",
             fontsize=8, color=INK2, style="italic")
    save(fig, "graphical_abstract", tight=False)


if __name__ == "__main__":
    import sys
    for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, figS, figS5, graphical_abstract): f()
    import cn_htse_heat as HT
    LAYOUT["FigS7_htse_heat"] = HT.figure(json.load(open(H / "cn_htse_heat.json")))
    probs = [p for v in LAYOUT.values() for p in v]
    json.dump(dict(figures=sorted(LAYOUT), problems=probs), open(H / "cn_figure_layout_check.json", "w"), indent=1)
    for p in probs: print("LAYOUT FAIL:", p)
    print(f"figures written; layout check: {len(LAYOUT)} figures, {len(probs)} problems")
    sys.exit(1 if probs else 0)
