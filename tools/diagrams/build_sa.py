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

W = 1600
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

def text_bg(x, y, s, size=13, weight=400, fill=INK, anchor="middle", style="normal", pad_x=6, pad_y=3):
    est_w = size*0.6*len(s) + pad_x*2
    rect_x = x - est_w/2 if anchor == "middle" else (x - pad_x if anchor == "start" else x - est_w + pad_x)
    rect_h = size*1.15 + pad_y*2
    rect_y = y - size*0.85 - pad_y
    rrect(rect_x, rect_y, est_w, rect_h, rx=3, fill=BG, stroke="none")
    text(x, y, s, size=size, weight=weight, fill=fill, anchor=anchor, style=style)

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

def diamond_at(cx, cy, col=NAVY, dw=15, dh=11):
    pts = f"{cx-dw/2},{cy} {cx},{cy-dh/2} {cx+dw/2},{cy} {cx},{cy+dh/2}"
    parts.append(f'<polygon points="{pts}" fill="{col}"/>')

def tier_badge(cx, cy, tier_label, col, r=14, fs=11):
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" stroke="#FFFFFF" stroke-width="2"/>')
    text(cx, cy+fs*0.35, tier_label, size=fs, weight=700, fill="#FFFFFF", anchor="middle")

head = f'''<svg xmlns="http://www.w3.org/2000/svg" font-family="Inter, Segoe UI, Helvetica Neue, Arial, sans-serif">
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
  <marker id="tri-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{RED}"/>
  </marker>
  <marker id="tri-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{GRAY_DASH}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 13", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Situational Awareness", size=26, weight=600, fill=INK)
text(60, 110, "no new data \u2014 a navigation contract over Sub-models 7, 9 and 10, so the operator is never lost or digging", size=13, fill=SOFT)

with open("./lunex-sa-model.svg.partial", "w") as f:
    f.write("placeholder")
print("head ok")

# ============================================================
# Panel 1: Same three signals, at every level, top to bottom
# ============================================================
p1_y = 145
p1_h = 440
rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "The Same Three Signals, at Every Level", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "own state \u00b7 rollup badge \u00b7 top alarm \u2014 identical shape from Realm down to Device (Sub-model 2)", size=12.5, fill=SOFT)

levels_sa = [
    ("Cell \u2014 Utilities", "On", GREEN, "0", RED, "Pump-07: High Vibration"),
    ("System \u2014 Boiler DCS", "On", GREEN, "0", RED, "Pump-07: High Vibration"),
    ("Assembly \u2014 Feed Pumps", "Standby", NAVY, "0", RED, "Pump-07: High Vibration"),
    ("Device \u2014 Pump-07", "Inhibited", BLUE, "0", RED, "High Vibration (Priority 1)"),
]
row_h_sa = 78
ry0 = p1_y + 105
colA, colB, colC, colD = 60, 480, 640, 900
text(colA, ry0-16, "LEVEL", size=10.5, fill=SOFT, spacing="1", weight=700)
text(colB, ry0-16, "OWN STATE", size=10.5, fill=SOFT, spacing="1", weight=700)
text(colC, ry0-16, "ROLLUP", size=10.5, fill=SOFT, spacing="1", weight=700)
text(colD, ry0-16, "TOP ALARM", size=10.5, fill=SOFT, spacing="1", weight=700)
line(58, ry0-4, W-58, ry0-4, stroke=LINE, sw=1)

for i, (lvl, st, stcol, tier, tiercol, alarm) in enumerate(levels_sa):
    ry = ry0 + 30 + i*row_h_sa
    text(colA, ry, lvl, size=13.5, weight=700, fill=INK)
    rrect(colB, ry-20, 100, 30, rx=15, stroke=stcol, sw=1.8, fill="#FFFFFF")
    text(colB+50, ry, st, size=11.5, weight=700, fill=stcol, anchor="middle")
    tier_badge(colC+14, ry-6, tier, tiercol, r=14, fs=11)
    text(colC+38, ry, "Critical", size=11.5, fill=tiercol, weight=700)
    text(colD, ry, alarm, size=12, fill=MUTED, family="Consolas, Menlo, monospace")
    if i < len(levels_sa)-1:
        line(58, ry+26, W-58, ry+26, stroke=LINE, sw=1)

text(58, p1_y+405, "same worst-case Pump-07 alarm is visible from the top of the hierarchy \u2014 the operator never wonders \u201cis anything wrong?\u201d", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 2: Jump to Worst — bypass manual layer-by-layer navigation
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 380
rrect(30, p2_y, W-60, p2_h, stroke=BLUE, sw=2.2)
text(58, p2_y+38, "Jump to Worst \u2014 No Manual Digging Through Layers", size=20, weight=700, fill=BLUE)
text(58, p2_y+60, "one action follows the Rollup's own contributors path (Sub-model 9) straight to the cause", size=12.5, fill=SOFT)

chain = ["Cell", "System", "Assembly", "Device", "Alarm"]
n = len(chain)
cx0 = 120
step = (W-60-240)/(n-1)
cy = p2_y + 160
for i, lab in enumerate(chain):
    x = cx0 + i*step
    col = RED if i == n-1 else NAVY
    rrect(x-65, cy-24, 130, 48, rx=10, stroke=col, sw=2.2, fill="#FFFFFF")
    text(x, cy+5, lab, size=13, weight=700, fill=col, anchor="middle")
    if i < n-1:
        line(x+65, cy, x+step-65, cy, stroke=GRAY_DASH, sw=1.6, dash="3,3")
        text_bg(x+step/2, cy-32, "manual click", size=10, fill=SOFT, style="italic")

jump_y = cy + 90
path(f"M {cx0} {cy+24} C {cx0} {jump_y}, {cx0+(n-1)*step} {jump_y}, {cx0+(n-1)*step} {cy+24}",
     stroke=RED, sw=2.4, marker_end="tri-red")
text_bg((cx0+cx0+(n-1)*step)/2, jump_y+28, "jumpToWorst(node)  \u2014  one action, same result", size=13, weight=700, fill=RED)

text(58, p2_y+345, "the shortcut and the manual path always land on the same Device/Alarm \u2014 it's a shortcut, not a different answer", size=12, fill=MUTED, style="italic")

with open("./lunex-sa-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part2 ok")

# ============================================================
# Panel 3: Landed — the right information is already there
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 300
rrect(30, p3_y, W-60, p3_h, stroke=BLUE, sw=2.2)
text(58, p3_y+38, "Landed \u2014 the Right Information Is Already There", size=20, weight=700, fill=BLUE)
text(58, p3_y+60, "reuses the Context Layer surfacing from Sub-model 11 \u2014 no separate hunt after arriving", size=12.5, fill=SOFT)

acx, acy = 260, p3_y+190
rrect(acx-120, acy-40, 240, 80, rx=10, stroke=RED, sw=2.4, fill="#FFFFFF")
text(acx, acy-12, "Pump-07", size=14.5, weight=700, fill=RED, anchor="middle")
text(acx, acy+12, "High Vibration \u00b7 Priority 1", size=11.5, fill=MUTED, anchor="middle")

targets_sa = [
    ("trend, last 4h", GREEN, -1),
    ("ARP: corrective action", BLUE, 0),
    ("nearest Interlock: IL-014", NAVY, 1),
]
for label, col, slot in targets_sa:
    tx = 760
    ty = acy + slot*70
    rrect(tx, ty-24, 340, 48, rx=10, stroke=col, sw=2, fill="#FFFFFF")
    text(tx+20, ty+6, label, size=13, weight=700, fill=col)
    line(acx+120, acy, tx-4, ty, stroke=col, sw=1.8, marker_end="tri-navy")

text(58, p3_y+270, "one screen: alarm, trend, procedure and nearest safeguard together \u2014 nothing else to click through", size=12, fill=MUTED, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p3_y + p3_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=GRAY_DASH, sw=1.6, dash="3,3")
text(118, ly2+5, "manual, layer-by-layer navigation", size=13, fill=INK)
line(430, ly2, 476, ly2, stroke=RED, sw=2.4, marker_end="tri-red")
text(488, ly2+5, "jumpToWorst() shortcut", size=13, fill=INK)
line(750, ly2, 796, ly2, stroke=NAVY, sw=1.8, marker_end="tri-navy")
text(808, ly2+5, "context surfaced automatically", size=13, fill=INK)

final_h = int(ly2 + 60)
parts.append("</svg>")

svg_body = "\n".join(parts)
bg = f'<rect width="{W}" height="{final_h}" fill="{BG}"/>\n<rect width="{W}" height="{final_h}" fill="url(#grid5)"/>\n'
parts_final = parts[:BG_INSERT_INDEX] + [bg] + parts[BG_INSERT_INDEX:]
svg_body = "\n".join(parts_final)
svg_body = svg_body.replace(
    '<svg xmlns="http://www.w3.org/2000/svg" font-family="Inter, Segoe UI, Helvetica Neue, Arial, sans-serif">',
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {final_h}" width="{W}" height="{final_h}" font-family="Inter, Segoe UI, Helvetica Neue, Arial, sans-serif">'
)
svg_body = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg_body

with open("./lunex-sa-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
