#!/usr/bin/env python3
INK = "#16202B"
MUTED = "#33404D"
SOFT = "#5A6B7B"
NAVY = "#1F3B57"
GREEN = "#2E7D4F"
BLUE = "#2F6F9E"
RED = "#B3402F"
GRAY_DASH = "#8FA0B3"
BG = "#FBFAF8"
LINE = "#D6DEE7"

W, H = 1700, 1450
parts = []

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def rrect(x, y, w, h, rx=10, fill="#FFFFFF", stroke=NAVY, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

def text(x, y, s, size=13, weight=400, fill=INK, anchor="start", style="normal", family=None, spacing=None):
    fam = f' font-family="{family}"' if family else ""
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    it = f' font-style="{style}"' if style != "normal" else ""
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{it}{fam}{sp}>{esc(s)}</text>')

def line(x1, y1, x2, y2, stroke=NAVY, sw=2, marker_end=None, marker_start=None, dash=None):
    me = f' marker-end="url(#{marker_end})"' if marker_end else ""
    ms = f' marker-start="url(#{marker_start})"' if marker_start else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{me}{ms}{d}/>')

def path(d_attr, stroke=NAVY, sw=2, marker_end=None, marker_start=None, fill="none", dash=None):
    me = f' marker-end="url(#{marker_end})"' if marker_end else ""
    ms = f' marker-start="url(#{marker_start})"' if marker_start else ""
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    parts.append(f'<path d="{d_attr}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{me}{ms}{dd}/>')

def mini_box(cx, cy, label, col, w=48, h=34):
    rrect(cx-w/2, cy-h/2, w, h, rx=6, stroke=col, sw=2, fill="#FFFFFF")
    text(cx, cy+5, label, size=12.5, weight=700, fill=col, anchor="middle", family="Consolas, Menlo, monospace")

head = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Inter, Segoe UI, Helvetica Neue, Arial, sans-serif">
<defs>
  <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
    <path d="M20 0H0V20" fill="none" stroke="#E6EBF0" stroke-width="1"/>
  </pattern>
  <pattern id="grid5" width="100" height="100" patternUnits="userSpaceOnUse">
    <rect width="100" height="100" fill="url(#grid)"/>
    <path d="M100 0H0V100" fill="none" stroke="{LINE}" stroke-width="1"/>
  </pattern>
  <marker id="tri-navy" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{NAVY}"/>
  </marker>
  <marker id="tri-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{GRAY_DASH}"/>
  </marker>
  <marker id="tri-open" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
    <path d="M0 0 L12 6 L0 12 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="1.3"/>
  </marker>
</defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#grid5)"/>
'''
parts.append(head)

text(60, 56, "LUNEX — SUB-MODEL 3", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Topology Model (Assembly)", size=26, weight=600, fill=INK)
text(60, 110, "Axis 1: wiring shape (choose exactly one per Assembly)  \u00b7  Axis 2: capability flags (independent of shape)", size=13, fill=SOFT)

# ============================================================
# Four shape cards
# ============================================================
card_y, card_w, card_h = 150, 380, 340
gap = 40
xs = [30 + i*(card_w+gap) for i in range(4)]

func_col = {"S": GREEN, "T": BLUE, "CU": NAVY, "SC": BLUE, "A": GREEN}

# ---------- Card 0: Integrated ----------
cx0 = xs[0]
rrect(cx0, card_y, card_w, card_h, stroke=NAVY, sw=2.2)
text(cx0+24, card_y+36, "Integrated", size=19, weight=700, fill=NAVY)
bx, by, bw, bh = cx0+60, card_y+120, 260, 100
rrect(bx, by, bw, bh, stroke=NAVY, sw=2.5)
third = bw/3
for i in range(1, 3):
    line(bx+third*i, by, bx+third*i, by+bh, stroke=NAVY, sw=1.4, dash="4,3")
for i, lab in enumerate(["S", "CU", "A"]):
    text(bx+third*i+third/2, by+bh/2+6, lab, size=18, weight=700, fill=func_col[lab if lab!="CU" else "CU"], anchor="middle", family="Consolas, Menlo, monospace")
text(cx0+24, card_y+265, "one physical unit \u2014 sensing, logic and", size=12.5, fill=MUTED)
text(cx0+24, card_y+283, "actuation fused together", size=12.5, fill=MUTED)
text(cx0+24, card_y+310, "plug-and-play \u00b7 minimal wiring", size=12, fill=SOFT, style="italic")

# ---------- Card 1: Point-to-Point ----------
cx1 = xs[1]
rrect(cx1, card_y, card_w, card_h, stroke=NAVY, sw=2.2)
text(cx1+24, card_y+36, "Point-to-Point", size=19, weight=700, fill=NAVY)
seq = ["S", "T", "CU", "SC", "A"]
seq_y = card_y + 150
seq_x0 = cx1 + 46
step = 68
seq_pts = [(seq_x0+i*step, seq_y) for i in range(5)]
for (px, py), lab in zip(seq_pts, seq):
    if lab != seq[0]:
        prev = seq_pts[seq.index(lab)-1]
        line(prev[0]+27, py, px-27, py, stroke=NAVY, sw=2, marker_end="tri-navy")
    mini_box(px, py, lab, func_col[lab])
# feedback arcs between the three "control" stages: T-CU and CU-SC
for i in (1, 2):
    p1 = seq_pts[i]
    p2 = seq_pts[i+1]
    midx = (p1[0]+p2[0])/2
    path(f"M {p1[0]+10} {p1[1]-20} Q {midx} {p1[1]-42}, {p2[0]-10} {p2[1]-20}", stroke=GRAY_DASH, sw=1.6, dash="4,3", marker_end="tri-gray")
text(cx1+24, card_y+205, "feedback \u2014 only between Control Units", size=11.5, fill=SOFT, style="italic")
text(cx1+24, card_y+265, "straight 1:1 chain, each stage wired to", size=12.5, fill=MUTED)
text(cx1+24, card_y+283, "its neighbor only \u2014 no shared stage", size=12.5, fill=MUTED)
text(cx1+24, card_y+310, "the simplest multi-device pattern", size=12, fill=SOFT, style="italic")

# ---------- Card 2: Star ----------
cx2 = xs[2]
rrect(cx2, card_y, card_w, card_h, stroke=NAVY, sw=2.2)
text(cx2+24, card_y+36, "Star", size=19, weight=700, fill=NAVY)
center = (cx2+card_w/2, card_y+165)
mini_box(center[0], center[1], "CU", NAVY, w=52, h=38)
top_y = card_y+120
bot_y = card_y+210
s_pts = [(cx2+42, top_y), (cx2+42, bot_y)]
t_pts = [(cx2+104, top_y), (cx2+104, bot_y)]
sc_pts = [(cx2+card_w-104, top_y), (cx2+card_w-104, bot_y)]
a_pts = [(cx2+card_w-42, top_y), (cx2+card_w-42, bot_y)]
for (sx, sy), (tx, ty) in zip(s_pts, t_pts):
    mini_box(sx, sy, "S", GREEN)
    mini_box(tx, ty, "T", BLUE)
    line(sx+25, sy, tx-25, ty, stroke=NAVY, sw=1.7, marker_end="tri-navy")
    yoff = -11 if ty < center[1] else 11
    line(tx+25, ty, center[0]-27, center[1]+yoff, stroke=NAVY, sw=1.7, marker_end="tri-navy")
for (cx_, cy_), (ax, ay) in zip(sc_pts, a_pts):
    mini_box(cx_, cy_, "SC", BLUE)
    mini_box(ax, ay, "A", GREEN)
    yoff = -11 if cy_ < center[1] else 11
    line(center[0]+27, center[1]+yoff, cx_-25, cy_, stroke=NAVY, sw=1.7, marker_end="tri-navy")
    line(cx_+25, cy_, ax-25, ay, stroke=NAVY, sw=1.7, marker_end="tri-navy")
text(cx2+24, card_y+265, "several sensors and actuators share", size=12.5, fill=MUTED)
text(cx2+24, card_y+283, "one Control Unit", size=12.5, fill=MUTED)
text(cx2+24, card_y+310, "fan-in / fan-out", size=12, fill=SOFT, style="italic")

# ---------- Card 3: Mesh ----------
cx3 = xs[3]
rrect(cx3, card_y, card_w, card_h, stroke=NAVY, sw=2.2)
text(cx3+24, card_y+36, "Mesh", size=19, weight=700, fill=NAVY)
top = (cx3+card_w/2, card_y+150)
bl = (cx3+95, card_y+245)
br = (cx3+card_w-95, card_y+245)
for p1, p2 in [(top, bl), (top, br), (bl, br)]:
    line(p1[0], p1[1], p2[0], p2[1], stroke=NAVY, sw=1.8, marker_end="tri-navy", marker_start="tri-navy")
for p in (top, bl, br):
    mini_box(p[0], p[1], "CU", NAVY, w=50, h=36)
s_top = (top[0]-155, top[1]-8)
t_top = (top[0]-90, top[1]-8)
sc_top = (top[0]+90, top[1]-8)
a_top = (top[0]+155, top[1]-8)
mini_box(s_top[0], s_top[1], "S", GREEN, w=40, h=28)
mini_box(t_top[0], t_top[1], "T", BLUE, w=40, h=28)
mini_box(sc_top[0], sc_top[1], "SC", BLUE, w=40, h=28)
mini_box(a_top[0], a_top[1], "A", GREEN, w=40, h=28)
line(s_top[0]+21, s_top[1], t_top[0]-21, t_top[1], stroke=NAVY, sw=1.6, marker_end="tri-navy")
line(t_top[0]+21, t_top[1], top[0]-27, top[1]-10, stroke=NAVY, sw=1.6, marker_end="tri-navy")
line(top[0]+27, top[1]-10, sc_top[0]-21, sc_top[1], stroke=NAVY, sw=1.6, marker_end="tri-navy")
line(sc_top[0]+21, sc_top[1], a_top[0]-21, a_top[1], stroke=NAVY, sw=1.6, marker_end="tri-navy")
text(cx3+24, card_y+287, "networked Control Units, each with", size=12.5, fill=MUTED)
text(cx3+24, card_y+305, "its own I/O (shown once, for clarity)", size=12.5, fill=MUTED)
text(cx3+24, card_y+325, "peer-to-peer network", size=12, fill=SOFT, style="italic")

# ============================================================
# Capability flags (independent axis) — now fully illustrated
# ============================================================
bracket_y = card_y + card_h + 35
path(f"M {xs[0]+20} {bracket_y} L {xs[3]+card_w-20} {bracket_y}", stroke=GRAY_DASH, sw=1.6, dash="5,4")
for x in xs:
    path(f"M {x+card_w/2} {bracket_y} L {x+card_w/2} {card_y+card_h}", stroke=GRAY_DASH, sw=1.6, dash="5,4")
text(W/2, bracket_y-10, "capability flags apply independently to any shape above", size=12.5, fill=SOFT, anchor="middle", style="italic")

panel_y = bracket_y + 30
panel_w = 800
panel_h = 410
panel_xA = 30
panel_xB = panel_xA + panel_w + 40
path(f"M {panel_xA+panel_w/2} {bracket_y} L {panel_xA+panel_w/2} {panel_y}", stroke=GRAY_DASH, sw=1.6, dash="5,4")
path(f"M {panel_xB+panel_w/2} {bracket_y} L {panel_xB+panel_w/2} {panel_y}", stroke=GRAY_DASH, sw=1.6, dash="5,4")

# ---------- Panel A: High-Availability ----------
rrect(panel_xA, panel_y, panel_w, panel_h, stroke=GREEN, sw=2.2)
text(panel_xA+28, panel_y+38, "High-Availability", size=20, weight=700, fill=GREEN)
text(panel_xA+28, panel_y+60, "any Control Unit, in any shape above, deployed as a redundant pair", size=12.5, fill=SOFT)

dcx = panel_xA + panel_w/2
dcy = panel_y + 165
cu_p = (dcx, dcy-48)
cu_s = (dcx, dcy+48)
fork_l = (panel_xA+150, dcy)
fork_r = (panel_xA+panel_w-150, dcy)
in_pt = (panel_xA+60, dcy)
out_pt = (panel_xA+panel_w-60, dcy)

line(in_pt[0], in_pt[1], fork_l[0]-8, fork_l[1], stroke=NAVY, sw=1.8, marker_end="tri-navy")
text(in_pt[0]-4, dcy-16, "shared input", size=11, fill=SOFT, style="italic")
line(fork_l[0], fork_l[1]-6, cu_p[0]-85, cu_p[1], stroke=NAVY, sw=1.8, marker_end="tri-navy")
line(fork_l[0], fork_l[1]+6, cu_s[0]-85, cu_s[1], stroke=NAVY, sw=1.6, marker_end="tri-navy", dash="5,4")

rrect(cu_p[0]-85, cu_p[1]-24, 170, 48, rx=8, stroke=NAVY, sw=2.4)
text(cu_p[0], cu_p[1]-2, "CU \u2014 Primary", size=14, weight=700, fill=NAVY, anchor="middle", family="Consolas, Menlo, monospace")
text(cu_p[0], cu_p[1]+16, "active", size=11, weight=700, fill=GREEN, anchor="middle")

rrect(cu_s[0]-85, cu_s[1]-24, 170, 48, rx=8, stroke=SOFT, sw=2.2, dash="6,4")
text(cu_s[0], cu_s[1]-2, "CU \u2014 Standby", size=14, weight=700, fill=SOFT, anchor="middle", family="Consolas, Menlo, monospace")
text(cu_s[0], cu_s[1]+16, "standby", size=11, weight=700, fill=SOFT, anchor="middle")

path(f"M {cu_p[0]+95} {cu_p[1]+18} L {cu_s[0]+95} {cu_s[1]-18}", stroke=GREEN, sw=1.8, dash="3,3", marker_end="tri-navy", marker_start="tri-navy")
text(cu_p[0]+108, dcy+5, "sync /", size=11, fill=GREEN, style="italic")
text(cu_p[0]+108, dcy+20, "heartbeat", size=11, fill=GREEN, style="italic")

line(cu_p[0]+85, cu_p[1], fork_r[0], fork_r[1]-6, stroke=NAVY, sw=1.8, marker_end="tri-navy")
line(cu_s[0]+85, cu_s[1], fork_r[0], fork_r[1]+6, stroke=NAVY, sw=1.6, marker_end="tri-navy", dash="5,4")
line(fork_r[0]+8, fork_r[1], out_pt[0], out_pt[1], stroke=NAVY, sw=1.8, marker_end="tri-navy")
text(out_pt[0]-70, dcy-16, "shared output", size=11, fill=SOFT, style="italic", anchor="end")

text(panel_xA+28, panel_y+368, "on failure, Standby takes over the shared inputs/outputs \u2014", size=12.5, fill=MUTED)
text(panel_xA+28, panel_y+388, "the shape above (Point-to-Point, Star or Mesh) is unchanged", size=12.5, fill=MUTED)

# ---------- Panel B: Cloud & Analytics ----------
rrect(panel_xB, panel_y, panel_w, panel_h, stroke=BLUE, sw=2.2)
text(panel_xB+28, panel_y+38, "Cloud & Analytics", size=20, weight=700, fill=BLUE)
text(panel_xB+28, panel_y+60, "any Control Unit, in any shape above, streams telemetry upward", size=12.5, fill=SOFT)

bcx = panel_xB + panel_w/2
cu_gnd = (bcx, panel_y+290)
cloud_box_y = panel_y+95
rrect(cu_gnd[0]-70, cu_gnd[1]-22, 140, 44, rx=8, stroke=NAVY, sw=2.2)
text(cu_gnd[0], cu_gnd[1]+5, "CU", size=15, weight=700, fill=NAVY, anchor="middle", family="Consolas, Menlo, monospace")
text(cu_gnd[0], cu_gnd[1]+34, "any shape above", size=11, fill=SOFT, style="italic", anchor="middle")

rrect(bcx-190, cloud_box_y, 380, 66, rx=20, stroke=BLUE, sw=2.4)
text(bcx, cloud_box_y+28, "AI / Analytics Layer", size=16, weight=700, fill=BLUE, anchor="middle")
text(bcx, cloud_box_y+48, "Sub-model 7", size=11, fill=SOFT, anchor="middle")

path(f"M {bcx} {cu_gnd[1]-22} L {bcx} {cloud_box_y+66+10}", stroke=BLUE, sw=2, dash="2,6", marker_end="tri-navy")
for t in (0.28, 0.52, 0.76):
    dy = cu_gnd[1]-22 - t*(cu_gnd[1]-22-(cloud_box_y+76))
    parts.append(f'<circle cx="{bcx}" cy="{dy}" r="4" fill="{BLUE}"/>')
text(bcx+50, (cu_gnd[1]+cloud_box_y+66)/2, "state \u00b7 health \u00b7", size=11.5, fill=SOFT, style="italic")
text(bcx+50, (cu_gnd[1]+cloud_box_y+66)/2+18, "properties", size=11.5, fill=SOFT, style="italic")
text(bcx+50, (cu_gnd[1]+cloud_box_y+66)/2+36, "(Sub-model 1)", size=11.5, fill=SOFT, style="italic")

text(panel_xB+28, panel_y+368, "telemetry feeds the AI layer regardless of shape \u2014 Integrated,", size=12.5, fill=MUTED)
text(panel_xB+28, panel_y+388, "Point-to-Point, Star and Mesh all expose the same interface", size=12.5, fill=MUTED)

# ============================================================
# Level 0 foundation
# ============================================================
f_y = panel_y + panel_h + 55
line(W/2, f_y-35, W/2, f_y-8, stroke=GRAY_DASH, sw=1.8, marker_end="tri-gray", dash="5,4")
rrect(60, f_y, W-120, 90, rx=12, stroke=NAVY, sw=2.2, fill="#FFFFFF")
text(90, f_y+38, "Level 0 \u2014 Physical Infrastructure Layer", size=17, weight=700, fill=NAVY)
text(90, f_y+62, "the physical process / equipment every shape above ultimately drives (Purdue L0, Sub-model 2)", size=12.5, fill=SOFT)

# ============================================================
# Legend
# ============================================================
leg_y = f_y + 90 + 60
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
lx = 60
for lab, name in [("S", "Sensor"), ("T", "Transducer"), ("CU", "Control Unit"), ("SC", "Signal Converter"), ("A", "Actuator")]:
    mini_box(lx+24, ly2, lab, func_col[lab], w=44, h=30)
    text(lx+56, ly2+5, name, size=12.5, fill=INK)
    lx += 56 + 12*len(name) + 40

ly3 = ly2 + 44
line(60, ly3, 106, ly3, stroke=NAVY, sw=2, marker_end="tri-navy")
text(118, ly3+5, "signal flow", size=13, fill=INK)
path(f"M 250 {ly3} L 296 {ly3}", stroke=GRAY_DASH, sw=1.6, dash="5,4", marker_end="tri-gray")
text(308, ly3+5, "feedback / dependency", size=13, fill=INK)
line(560, ly3, 606, ly3, stroke=NAVY, sw=1.8, marker_end="tri-navy", marker_start="tri-navy")
text(618, ly3+5, "peer-to-peer mesh link", size=13, fill=INK)

final_h = int(ly3 + 60)
parts.append("</svg>")

svg = "\n".join(parts)
svg = svg.replace(f'viewBox="0 0 {W} {H}" width="{W}" height="{H}"', f'viewBox="0 0 {W} {final_h}" width="{W}" height="{final_h}"')
svg = svg.replace(f'<rect width="{W}" height="{H}" fill="{BG}"/>', f'<rect width="{W}" height="{final_h}" fill="{BG}"/>')
svg = svg.replace(f'<rect width="{W}" height="{H}" fill="url(#grid5)"/>', f'<rect width="{W}" height="{final_h}" fill="url(#grid5)"/>')
svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg

with open("./lunex-topology-model.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("done", final_h)
