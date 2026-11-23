"""Heat and mass balance of high-temperature steam electrolysis (solid oxide), per kg of hydrogen, CN v1.6.

Derives the two heat inputs used by the system model from a temperature-enthalpy calculation instead of assuming them:
  external_heat_kwh_kg   heat needed to raise steam (feed-water preheat not covered by recovery, plus evaporation),
                         at <= the saturation temperature at stack pressure; supplied by reactor process steam or
                         electric boilers;
  topping_kwh_kg         heat needed above what recuperation can supply (final lift to stack inlet temperature plus
                         stack heat loss), supplied by electric heaters unless the reactor outlet is >= 850 C.

Streams (no anode sweep gas; product O2 leaves the anode):
  cold:  feed water 20 C -> saturated liquid -> saturated vapour (at P) -> superheated to T_stack
  hot:   cathode outlet (H2 + unconverted steam) and anode outlet (O2), both leaving the stack at T_stack
High-temperature recuperator: hot streams cool from T_stack while superheating the steam to T_stack - dT_min.
Low-temperature recovery: remaining sensible heat of the hot streams above the dew point preheats feed water up to
T_sat - dT_min; condensation of unconverted steam below the dew point preheats feed water up to T_dew - dT_min.
Gas enthalpies from NIST-JANAF Shomate equations (ideal gas; at 0.5 MPa the real-gas correction for steam is <1%).
Saturation properties of water at 0.5 MPa from steam tables.  Values marked [A] are assumptions.
Writes cn_htse_heat.json and FigS7_htse_heat (PNG/TIFF) when run directly.
"""
import json
from pathlib import Path

H = Path(__file__).resolve().parent
M_H2, M_H2O, M_O2 = 2.016, 18.015, 31.998   # g/mol

# NIST Shomate coefficients (A, B, C, D, E) by temperature range [K]
SHOMATE = {"H2O": [(500, 1700, (30.09200, 6.832514, 6.793435, -2.534480, 0.082139))],
           "H2": [(298, 1000, (33.066178, -11.363417, 11.432816, -2.772874, -0.158558)),
                  (1000, 2500, (18.563083, 12.257357, -2.859786, 0.268238, 1.977990))],
           "O2": [(100, 700, (31.32234, -20.23531, 57.86644, -36.50624, -0.007374)),
                  (700, 2000, (30.03235, 8.772972, -3.988133, 0.788313, -0.741599))]}
MOLAR = {"H2O": M_H2O, "H2": M_H2, "O2": M_O2}

P = dict(stack_c=800.0,            # stack temperature, thermoneutral operation [A; INL reference design ~800 C]
         pressure_mpa=0.5,         # steam pressure [A]
         t_sat_c=151.8, h_f=640.1, h_fg=2107.4, h_water20=83.9,   # steam tables at 0.5 MPa, kJ/kg
         steam_utilisation=0.80,   # fraction of feed steam converted [A]
         dT_min=25.0,              # minimum approach in recuperators [A]
         feed_c=20.0,
         stack_kwh_e_kg=33.3,      # stack electricity near thermoneutral voltage (1.29 V) [U: INL]
         heat_loss_frac=0.015,     # stack and hot-box heat loss as a share of stack electricity [A]
         U_ht_w_m2k=60.0,          # overall coefficient, high-temperature gas-gas recuperator [A]
         recup_usd_m2=3000.0,      # installed cost of alloy 800H/617 compact recuperator [A]
         heater_usd_kw=150.0,      # electric topping heater, installed [A]
         life_yr=20, wacc=0.05, cf=0.90)


def cp_mass(sp, T):
    """kJ/(kg K) at T [K]."""
    for lo, hi, (A, B, C, D, E) in SHOMATE[sp]:
        if T <= hi or (lo, hi) == SHOMATE[sp][-1][:2]:
            t = T / 1000.0; return (A + B * t + C * t * t + D * t ** 3 + E / (t * t)) / MOLAR[sp]
    raise ValueError


def dh(sp, T1c, T2c, n=400):
    """Sensible enthalpy change kJ/kg from T1 to T2 (C), trapezoid rule."""
    a, b = T1c + 273.15, T2c + 273.15; s = 0.0; h = (b - a) / n
    for i in range(n):
        x0, x1 = a + i * h, a + (i + 1) * h; s += 0.5 * (cp_mass(sp, x0) + cp_mass(sp, x1)) * h
    return s


def balance(p=None):
    p = {**P, **(p or {})}
    w_cons = M_H2O / M_H2                       # kg water split per kg H2 (8.94)
    w_feed = w_cons / p["steam_utilisation"]    # kg steam fed
    w_resid = w_feed - w_cons; o2 = 0.5 * M_O2 / M_H2   # kg unconverted steam, kg O2
    Ts, Tst, dT = p["t_sat_c"], p["stack_c"], p["dT_min"]
    # cold-side duties (kJ per kg H2)
    q_preheat = w_feed * (p["h_f"] - p["h_water20"]); q_evap = w_feed * p["h_fg"]
    q_super = w_feed * dh("H2O", Ts, Tst)
    # high-temperature recuperator: steam from T_sat to T_stack - dT_min
    q_sh_recup = w_feed * dh("H2O", Ts, Tst - dT)
    hot = lambda T1, T2: dh("H2", T2, T1) + w_resid * dh("H2O", T2, T1) + o2 * dh("O2", T2, T1)   # heat released cooling T1->T2
    # find hot outlet temperature of the recuperator (bisection)
    lo, hi = Ts + dT, Tst
    assert hot(Tst, lo) >= q_sh_recup, "recuperator infeasible: hot streams cannot superheat the feed"
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if hot(Tst, mid) > q_sh_recup: lo = mid
        else: hi = mid
    t_hot_out = 0.5 * (lo + hi)
    # pinch check at the cold end: hot outlet must exceed cold inlet + dT_min (checked by construction) and the
    # capacity-rate profile must not cross; verify on a grid
    grid = []
    for k in range(1, 41):
        Tc = Ts + (Tst - dT - Ts) * k / 40; qc = w_feed * dh("H2O", Ts, Tc)
        # hot temperature where the hot side has released (q_sh_recup - qc) counted from its outlet end (counterflow)
        lo2, hi2 = t_hot_out, Tst
        for _ in range(60):
            m2 = 0.5 * (lo2 + hi2)
            if hot(m2, t_hot_out) < qc: lo2 = m2
            else: hi2 = m2
        grid.append(0.5 * (lo2 + hi2) - Tc)
    pinch = min(grid)
    # low-temperature recovery
    x_steam = (w_resid / M_H2O) / (w_resid / M_H2O + 1.0 / M_H2)            # mole fraction steam in cathode outlet
    p_steam = x_steam * p["pressure_mpa"]
    t_dew = 100.0 + 28.0 * (p_steam - 0.101325) / 0.1                      # linearised dew point near 0.1-0.2 MPa
    q_hot_sens = hot(t_hot_out, max(t_dew, p["feed_c"] + dT))               # sensible heat left above the dew point
    q_pre_hi_need = w_feed * 4.25 * (Ts - dT - (t_dew - dT))                # water from (T_dew - dT) to (T_sat - dT)
    q_pre_hi = min(q_hot_sens, max(q_pre_hi_need, 0.0))
    q_cond = w_resid * 2257.0 * 0.9                                          # 90% of unconverted steam condensed
    q_pre_lo_need = w_feed * 4.18 * ((t_dew - dT) - p["feed_c"])
    q_pre_lo = min(q_cond, q_pre_lo_need)
    q_ext = q_preheat - q_pre_hi - q_pre_lo + q_evap                         # external steam-raising heat
    q_trim = q_super - q_sh_recup                                            # final lift T_stack - dT -> T_stack
    q_loss = p["heat_loss_frac"] * p["stack_kwh_e_kg"] * 3600.0
    # recuperator size and cost (counterflow LMTD approximation)
    import math
    dT1, dT2 = Tst - (Tst - dT), t_hot_out - Ts
    lmtd = (dT2 - dT1) / math.log(dT2 / dT1) if abs(dT2 - dT1) > 1e-6 else dT1
    kg_h = 1.0                                                               # per kg/h of hydrogen capacity
    q_kw = q_sh_recup * kg_h / 3600.0; area = q_kw * 1e3 / (p["U_ht_w_m2k"] * lmtd)
    crf = p["wacc"] / (1 - (1 + p["wacc"]) ** -p["life_yr"]); kg_yr = 8760 * p["cf"] * kg_h
    recup_usd_kg = area * p["recup_usd_m2"] * crf / kg_yr
    heater_usd_kg = (q_trim + q_loss) / 3600.0 * p["heater_usd_kw"] * crf / kg_yr
    kwh = lambda kj: kj / 3600.0
    return dict(inputs=p, feed_steam_kg=w_feed, water_split_kg=w_cons, unconverted_steam_kg=w_resid, o2_kg=o2,
                duties_kwh_kg=dict(feed_water_preheat=kwh(q_preheat), evaporation=kwh(q_evap), superheat_total=kwh(q_super),
                                   superheat_by_recuperator=kwh(q_sh_recup), preheat_recovered_sensible=kwh(q_pre_hi),
                                   preheat_recovered_condensing=kwh(q_pre_lo), electric_trim=kwh(q_trim), stack_heat_loss=kwh(q_loss)),
                hot_outlet_after_recuperator_c=t_hot_out, recuperator_min_approach_c=pinch, cathode_dew_point_c=t_dew,
                external_heat_kwh_kg=kwh(q_ext), external_heat_max_temp_c=Ts,
                topping_kwh_kg=kwh(q_trim + q_loss),
                recuperator_m2_per_kg_h=area, recuperator_lmtd_c=lmtd, recuperator_usd_kg=recup_usd_kg, topping_heater_usd_kg=heater_usd_kg,
                no_lowT_recovery_external_heat_kwh_kg=kwh(q_preheat + q_evap))


def figure(b):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]; INK = "#1a1a1a"
    p = b["inputs"]; d = b["duties_kwh_kg"]; Ts, Tst, dT = p["t_sat_c"], p["stack_c"], p["dT_min"]
    q0 = 0.0; q1 = q0 + d["feed_water_preheat"]; q2 = q1 + d["evaporation"]; q3 = q2 + d["superheat_total"]
    fig, a = plt.subplots(figsize=(3.35, 3.4))
    a.plot([q0, q1, q2, q3], [p["feed_c"], Ts, Ts, Tst], color=C[0], lw=2, label="Feed water to stack inlet (cold)")
    qa = q2; qb = q2 + d["superheat_by_recuperator"]
    a.plot([qa, qb], [b["hot_outlet_after_recuperator_c"], Tst], color=C[1], lw=2, label="H$_2$/steam and O$_2$ from stack (hot)")
    a.axvspan(q0, q0 + d["preheat_recovered_condensing"] + d["preheat_recovered_sensible"], color=C[2], alpha=0.15, lw=0, label="Preheat from recovered heat")
    a.axvspan(q0 + d["preheat_recovered_condensing"] + d["preheat_recovered_sensible"], q2, color=C[3], alpha=0.18, lw=0, label="External heat (reactor steam or boiler)")
    a.axvspan(qb, q3, color="#e34948", alpha=0.25, lw=0, label="Electric topping")
    a.set_xlabel("Heat per kg of hydrogen (kWh)", fontsize=7); a.set_ylabel("Temperature (°C)", fontsize=7)
    a.tick_params(labelsize=6.5); a.set_ylim(0, 880)
    a.legend(fontsize=5.3, loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=1, frameon=False)   # below the plot, clear of the curves
    for s in ("top", "right"): a.spines[s].set_visible(False)
    fig.tight_layout()
    from cn_layout_check import check   # CN v1.6.3: no text on graphics or on other text
    problems = check(fig, "FigS7_htse_heat")
    for ext in ("png", "tif"): fig.savefig(H / f"FigS7_htse_heat.{ext}", dpi=300)
    plt.close(fig)
    return problems


if __name__ == "__main__":
    b = balance(); json.dump(b, open(H / "cn_htse_heat.json", "w"), indent=1)
    figure(b)
    print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in b.items() if k not in ("inputs",)}, indent=1))
