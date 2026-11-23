"""Figure layout check (CN v1.6.3): no text may sit on top of bars, lines, markers, outlines or other text.

For each figure, every drawn text (labels, tick labels, titles, annotations, legend entries) and every legend box is
tested against
  (1) the figure's graphics drawn with all text and legends hidden (any pixel darker than the light-grey gridlines counts,
      so bars, lines, markers, outlines and data fills are all 'ink'), and
  (2) every other text and legend.
Each text is tested as its exact (rotated) rectangle, so slanted tick labels are judged by their real outline.
Patches given gid="bg" (region shading on the map, the tiles of the graphical abstract) keep their edges but lose their
fill in the test, so text may sit on a background fill but not across its outline.  Only tick labels that are actually
drawn are tested.

    from cn_layout_check import check
    problems = check(fig, "Fig3_cost_vs_petroleum")     # list of strings; empty = clean
"""
from __future__ import annotations
import numpy as np
from matplotlib.text import Text
from matplotlib.legend import Legend
from matplotlib.path import Path as MPath

DPI = 200          # test resolution
INK = 205          # a pixel is ink if its darkest channel is below this (gridlines #e4e3df and the map's land fill are not)
SHRINK = 1.5       # px trimmed from each side of a text box (anti-aliasing tolerance)
MAX_INK_PX = 2     # ink pixels allowed inside a text box
MAX_SHARED_PX = 1  # pixels two texts may share


def _drawn_texts(fig):
    tick_labels, drawn = set(), set()
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            for tk in axis.get_major_ticks() + axis.get_minor_ticks():
                tick_labels.update({id(tk.label1), id(tk.label2)})
            for tk in axis._update_ticks():
                for lb in (tk.label1, tk.label2):
                    if lb.get_visible(): drawn.add(id(lb))
    out = []
    for t in fig.findobj(Text):
        if not t.get_visible() or not t.get_text().strip() or t.get_gid() == "allow_overlap": continue
        if t.axes is not None and not t.axes.get_visible(): continue
        if id(t) in tick_labels and id(t) not in drawn: continue
        out.append(t)
    return out


def _poly(t, r):
    """Display-space outline of a text: its unrotated box rotated by the text angle, placed on the drawn extent."""
    bb = Text.get_window_extent(t, r); ang = t.get_rotation() % 360   # text only (an annotation's leader is graphics)
    if min(abs(ang - q) for q in (0, 90, 180, 270, 360)) < 1e-6:
        p = np.array([[bb.x0, bb.y0], [bb.x1, bb.y0], [bb.x1, bb.y1], [bb.x0, bb.y1]], dtype=float)
    else:
        rot = t.get_rotation(); t.set_rotation(0); b0 = Text.get_window_extent(t, r); t.set_rotation(rot)
        w, h = b0.width, b0.height; a = np.deg2rad(ang)
        R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
        p = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=float) @ R.T
        p = p - p.min(axis=0) + [bb.x0, bb.y0]
    c = p.mean(axis=0); v = p - c; n = np.linalg.norm(v, axis=1, keepdims=True); n[n == 0] = 1
    return p - v / n * SHRINK * np.sqrt(2)


def _pixels(poly, Hpx, Wpx):
    x0, y0 = np.floor(poly.min(axis=0)).astype(int); x1, y1 = np.ceil(poly.max(axis=0)).astype(int)
    x0, x1 = max(x0, 0), min(x1, Wpx); y0, y1 = max(y0, 0), min(y1, Hpx)
    if x1 <= x0 or y1 <= y0: return set()
    xs, ys = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
    pts = np.column_stack([xs.ravel(), ys.ravel()]); inside = MPath(poly).contains_points(pts)
    sel = pts[inside].astype(int)
    return set(zip(sel[:, 0].tolist(), sel[:, 1].tolist()))   # (x, y counted from the bottom)


def check(fig, name=""):
    old = fig.get_dpi(); fig.set_dpi(DPI); fig.canvas.draw(); r = fig.canvas.get_renderer()
    texts = _drawn_texts(fig); legends = [l for l in fig.findobj(Legend) if l.get_visible()]
    in_legend = {id(t) for l in legends for t in l.get_texts() + [l.get_title()]}
    Wpx, Hpx = fig.canvas.get_width_height()
    tpix = [(t, _pixels(_poly(t, r), Hpx, Wpx)) for t in texts]
    lpix = []
    for l in legends:
        b = l.get_window_extent(r); s = 0.5
        lpix.append((l, _pixels(np.array([[b.x0 + s, b.y0 + s], [b.x1 - s, b.y0 + s], [b.x1 - s, b.y1 - s], [b.x0 + s, b.y1 - s]]), Hpx, Wpx)))
    # graphics only: hide text and legends, strip background fills
    hidden = texts + legends
    bg = list(fig.findobj(lambda a: hasattr(a, "set_facecolor") and a.get_gid() == "bg"))
    saved_fc = [(p, p.get_facecolor()) for p in bg]
    for a in hidden: a.set_visible(False)
    for p in bg: p.set_facecolor("none")
    fig.canvas.draw(); img = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()
    for a in hidden: a.set_visible(True)
    for p, fc in saved_fc: p.set_facecolor(fc)
    fig.set_dpi(old); fig.canvas.draw()
    ink = img.min(axis=2) < INK
    def n_ink(px): return sum(1 for x, y in px if 0 <= Hpx - 1 - y < ink.shape[0] and x < ink.shape[1] and ink[Hpx - 1 - y, x])
    problems = []
    lab = lambda t: repr(t.get_text().replace("\n", " ")[:40])
    for t, px in tpix:
        n = n_ink(px)
        if n > MAX_INK_PX: problems.append(f"{name}: text {lab(t)} lies on graphics ({n} px)")
    for l, px in lpix:
        n = n_ink(px)
        if n > MAX_INK_PX: problems.append(f"{name}: legend lies on graphics ({n} px)")
    for i in range(len(tpix)):
        for j in range(i + 1, len(tpix)):
            k = len(tpix[i][1] & tpix[j][1])
            if k > MAX_SHARED_PX: problems.append(f"{name}: text {lab(tpix[i][0])} overlaps text {lab(tpix[j][0])} ({k} px)")
    for t, px in tpix:
        if id(t) in in_legend: continue
        for l, lp in lpix:
            k = len(px & lp)
            if k > MAX_SHARED_PX: problems.append(f"{name}: text {lab(t)} overlaps a legend ({k} px)")
    for i in range(len(lpix)):
        for j in range(i + 1, len(lpix)):
            if len(lpix[i][1] & lpix[j][1]) > MAX_SHARED_PX: problems.append(f"{name}: two legends overlap")
    return problems
