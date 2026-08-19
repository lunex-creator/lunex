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

def text(x, y, s, size=13, weight=400, fill=INK, anchor="start", style="normal", family=None, spacing=None, halo=False):
    fam = f' font-family="{family}"' if family else ""
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    it = f' font-style="{style}"' if style != "normal" else ""
    ha = f' stroke="{BG}" stroke-width="5" paint-order="stroke" stroke-linejoin="round"' if halo else ""
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{it}{fam}{sp}{ha}>{esc(s)}</text>')

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
  <marker id="tri-hollow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">
    <path d="M0 0 L12 6 L0 12 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="1.4"/>
  </marker>
  <marker id="tri-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{GRAY_DASH}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 10", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Alarm Management", size=26, weight=600, fill=INK)
text(60, 110, "ISA-18.2-based \u2014 priority is severity \u00d7 actionability, not severity alone", size=13, fill=SOFT)

# ============================================================
# Panel 1: Alarm — a first-class LunexObject
# ============================================================
p1_y = 145
p1_h = 410
rrect(30, p1_y, W-60, p1_h, stroke=RED, sw=2.2)
text(58, p1_y+38, "Alarm \u2014 a First-Class LunexObject", size=20, weight=700, fill=RED)
text(58, p1_y+60, "same pattern as Interlock, Zone and Conduit \u2014 a peer of Device and Component", size=12.5, fill=SOFT)

lo_x, lo_y, lo_w, lo_h = 90, p1_y+100, 220, 50
rrect(lo_x, lo_y, lo_w, lo_h, stroke=NAVY, sw=2, rx=8)
text(lo_x+lo_w/2, lo_y+22, "LunexObject", size=13.5, weight=700, fill=NAVY, anchor="middle")
text(lo_x+lo_w/2, lo_y+40, "\u00ababstract\u00bb", size=10.5, fill=SOFT, anchor="middle", style="italic")

al_x, al_y, al_w, al_h = 110, p1_y+195, 180, 60
rrect(al_x, al_y, al_w, al_h, stroke=RED, sw=2.4, rx=8)
text(al_x+al_w/2, al_y+26, "Alarm", size=15, weight=700, fill=RED, anchor="middle")
text(al_x+al_w/2, al_y+46, "extends LunexObject", size=10.5, fill=SOFT, anchor="middle", style="italic")
path(f"M {al_x+al_w/2} {al_y} L {lo_x+lo_w/2} {lo_y+lo_h}", stroke=NAVY, sw=2, marker_end="tri-hollow")

at_x, at_y, at_w, at_h = 380, p1_y+100, 560, 250
rrect(at_x, at_y, at_w, at_h, stroke=NAVY, sw=2, rx=8)
attrs = [
    ("+ id : string", MUTED),
    ("+ source : DeviceRef", MUTED),
    ("+ condition : string", MUTED),
    ("+ severity : Tier (0\u20133, Sub-model 9)", BLUE),
    ("+ actionable : bool  \u2190 derived, Panel 3", GREEN),
    ("+ priority : 1\u20134  \u2190 derived, Panel 2", RED),
    ("+ state : AlarmState (new, Panel 4)", NAVY),
    ("+ resetMode : auto | manual", RED),
    ("+ shelvedUntil : timestamp", MUTED),
]
ay = at_y+30
for a, col in attrs:
    text(at_x+18, ay, a, size=12, fill=col, family="Consolas, Menlo, monospace")
    ay += 24

text(58, p1_y+372, "priority and actionable are computed, not set by hand \u2014 same discipline as Sub-model 7/9's derived views", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 2: Priority Matrix — severity × actionability
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 380
rrect(30, p2_y, W-60, p2_h, stroke=RED, sw=2.2)
text(58, p2_y+38, "Priority \u2014 Severity \u00d7 Actionability, Not Severity Alone", size=20, weight=700, fill=RED)
text(58, p2_y+60, "an alarm the operator can still act on outranks one the system already handled", size=12.5, fill=SOFT)

gx, gy = 340, p2_y+120
cell_w, cell_h = 420, 100
cells = [
    ("Priority 1 \u2014 Critical", "operator can still prevent escalation", RED, 0, 0),
    ("Priority 2 \u2014 High", "operator can still act, lower severity", BLUE, 1, 0),
    ("Priority 3 \u2014 Informational", "already handled (e.g. by an Interlock) \u2014 Sub-model 5", SOFT, 0, 1),
    ("Priority 4 \u2014 Log Only", "already handled, low severity", GRAY_DASH, 1, 1),
]
for label, sub, col, cx_i, cy_i in cells:
    x = gx + cx_i*cell_w
    y = gy + cy_i*cell_h
    rrect(x, y, cell_w, cell_h, rx=10, stroke=col, sw=2.4, fill="#FFFFFF")
    text(x+20, y+34, label, size=15, weight=700, fill=col)
    text(x+20, y+58, sub, size=11.5, fill=MUTED)

text(gx-20, gy+cell_h/2+5, "high", size=12, fill=SOFT, anchor="end")
text(gx-20, gy+cell_h*1.5+5, "low", size=12, fill=SOFT, anchor="end")
text(gx-70, gy+cell_h, "severity", size=12.5, weight=700, fill=INK, anchor="middle")
text(gx+cell_w/2, gy-25, "actionable = true", size=12.5, weight=700, fill=GREEN, anchor="middle")
text(gx+cell_w*1.5, gy-25, "actionable = false", size=12.5, weight=700, fill=SOFT, anchor="middle")

text(58, p2_y+345, "\u201cactionable\u201d answers one question: can the operator still change the outcome? (Panel 3)", size=12, fill=MUTED, style="italic")

with open("./lunex-alarm-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part2 ok")

# ============================================================
# Panel 3: actionable — derived automatically from Interlock.state
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 260
rrect(30, p3_y, W-60, p3_h, stroke=RED, sw=2.2)
text(58, p3_y+38, "actionable \u2014 Derived Automatically from Interlock State", size=20, weight=700, fill=RED)
text(58, p3_y+60, "not a manual flag \u2014 it follows the linked Interlock's state (Sub-model 5), so it can't be left wrong", size=12.5, fill=SOFT)

ex_y = p3_y + 160
# example A
rrect(70, ex_y-45, 620, 90, rx=10, stroke=GREEN, sw=2.2, fill="#FFFFFF")
text(96, ex_y-15, "Interlock IL-014: state = Standby (not yet tripped)", size=13, weight=700, fill=GREEN)
text(96, ex_y+13, "\u2192 Alarm.actionable = true \u2192 Priority 1, if severity is high", size=12.5, fill=MUTED, family="Consolas, Menlo, monospace")

# example B
rrect(730, ex_y-45, 620, 90, rx=10, stroke=SOFT, sw=2.2, fill="#FFFFFF")
text(756, ex_y-15, "Interlock IL-014: state = Inhibited (already tripped)", size=13, weight=700, fill=SOFT)
text(756, ex_y+13, "\u2192 Alarm.actionable = false \u2192 Priority 3, same severity", size=12.5, fill=MUTED, family="Consolas, Menlo, monospace")

path(f"M 690 {ex_y} L 730 {ex_y}", stroke=GRAY_DASH, sw=1.8, dash="4,3", marker_end="tri-gray")

text(58, p3_y+230, "the operator sees the same underlying condition drop from Priority 1 to Priority 3 the instant the Interlock trips", size=12, fill=MUTED, style="italic")

with open("./lunex-alarm-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part3 ok")

# ============================================================
# Panel 4: Alarm State Machine — new, separate from Sub-model 4
# ============================================================
p4_y = p3_y + p3_h + 50
p4_h = 520
rrect(30, p4_y, W-60, p4_h, stroke=NAVY, sw=2.2)
text(58, p4_y+38, "Alarm State Machine \u2014 New, Not Reused From Sub-model 4", size=20, weight=700, fill=NAVY)
text(58, p4_y+60, "operator-response states, not object-behavior states \u2014 deliberately a separate value space", size=12.5, fill=SOFT)

def state_ellipse(cx, cy, label, w=140, h=52):
    parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{h/2}" fill="{NAVY}"/>')
    text(cx, cy+5, label, size=12.5, weight=600, fill="#FFFFFF", anchor="middle")

def state_rect(cx, cy, label, col=SOFT, w=160, h=44):
    rrect(cx-w/2, cy-h/2, w, h, rx=h/2, stroke=col, sw=2, fill="#FFFFFF")
    text(cx, cy+5, label, size=12, weight=600, fill=col, anchor="middle")

col_x = [150, 490, 830]
row1_y = p4_y + 240
row2_y = p4_y + 420

state_ellipse(col_x[0], row1_y, "Normal")
state_rect(col_x[1], row1_y, "Unacknowledged", RED)
state_rect(col_x[2], row1_y, "Acknowledged", BLUE)
state_rect(col_x[0], row2_y, "Out-of-Service", GRAY_DASH)
state_rect(col_x[1], row2_y, "Suppressed", SOFT)
state_rect(col_x[2], row2_y, "Shelved", SOFT)

# row 1: main flow, straight horizontal
line(col_x[0]+70, row1_y, col_x[1]-80, row1_y, stroke=RED, sw=2, marker_end="tri-navy")
text((col_x[0]+col_x[1])/2, row1_y-16, "condition trips", size=11.5, fill=RED, style="italic", anchor="middle", halo=True)

line(col_x[1]+80, row1_y, col_x[2]-80, row1_y, stroke=SOFT, sw=2, dash="3,3", marker_end="tri-gray")
text((col_x[1]+col_x[2])/2, row1_y-16, "acknowledge (operator)", size=11.5, fill=SOFT, style="italic", anchor="middle", halo=True)

# Acknowledged -> Cleared (RTN)
rtn_x, rtn_y = (col_x[0]+col_x[2])/2, row1_y-100
path(f"M {col_x[2]} {row1_y-26} C {col_x[2]-90} {row1_y-70}, {rtn_x+90} {rtn_y}, {rtn_x+70} {rtn_y}",
     stroke=GREEN, sw=2, marker_end="tri-navy")
text((col_x[2]+rtn_x)/2+35, row1_y-62, "condition clears", size=11, fill=GREEN, style="italic", anchor="middle", halo=True)

state_rect(rtn_x, rtn_y, "Cleared (RTN)", GREEN, w=150, h=40)

# Cleared (RTN) -> Normal: two distinct, non-overlapping paths
path(f"M {rtn_x-70} {rtn_y+6} C {rtn_x-190} {rtn_y+55}, {col_x[0]+70} {row1_y-70}, {col_x[0]+18} {row1_y-24}",
     stroke=GREEN, sw=2, marker_end="tri-navy")
text(rtn_x-195, rtn_y+28, "resetMode: auto", size=10.5, fill=GREEN, weight=700, style="italic", anchor="middle", halo=True)
text(rtn_x-195, rtn_y+44, "\u2192 immediate", size=10.5, fill=GREEN, style="italic", anchor="middle", halo=True)

path(f"M {rtn_x-90} {rtn_y-4} C {rtn_x-240} {rtn_y-50}, {col_x[0]-40} {row1_y-160}, {col_x[0]-18} {row1_y-24}",
     stroke=SOFT, sw=2, dash="3,3", marker_end="tri-gray")
text(rtn_x-235, rtn_y-58, "resetMode: manual", size=10.5, fill=SOFT, weight=700, style="italic", anchor="middle", halo=True)
text(rtn_x-235, rtn_y-42, "\u2192 operator resets", size=10.5, fill=SOFT, style="italic", anchor="middle", halo=True)

# columns: straight vertical down/up between row1 and row2
line(col_x[0], row1_y+26, col_x[0], row2_y-22, stroke=GRAY_DASH, sw=1.6, dash="3,3", marker_end="tri-gray")
text(col_x[0]-14, (row1_y+row2_y)/2, "taken out of service", size=10.5, fill=SOFT, style="italic", anchor="end")
line(col_x[0]+16, row2_y-22, col_x[0]+16, row1_y+26, stroke=GRAY_DASH, sw=1.6, dash="3,3", marker_end="tri-gray")
text(col_x[0]+30, (row1_y+row2_y)/2, "returned", size=10.5, fill=SOFT, style="italic")

line(col_x[1]-16, row1_y+22, col_x[1]-16, row2_y-22, stroke=SOFT, sw=1.6, dash="3,3", marker_end="tri-gray")
text(col_x[1]-30, (row1_y+row2_y)/2, "suppression rule fires", size=10.5, fill=SOFT, style="italic", anchor="end")
line(col_x[1]+16, row2_y-22, col_x[1]+16, row1_y+22, stroke=SOFT, sw=1.6, dash="3,3", marker_end="tri-gray")
text(col_x[1]+30, (row1_y+row2_y)/2, "rule ends", size=10.5, fill=SOFT, style="italic")

line(col_x[2]-16, row1_y+22, col_x[2]-16, row2_y-22, stroke=SOFT, sw=1.6, dash="3,3", marker_end="tri-gray")
text(col_x[2]-30, (row1_y+row2_y)/2, "shelve", size=11, fill=SOFT, style="italic", anchor="end")
line(col_x[2]+16, row2_y-22, col_x[2]+16, row1_y+22, stroke=SOFT, sw=1.6, dash="2,5", marker_end="tri-gray")
text(col_x[2]+30, (row1_y+row2_y)/2, "shelvedUntil expires", size=10.5, fill=SOFT, style="italic")

text(58, p4_y+485, "Shelved always expires back into Unacknowledged \u2014 an operator can delay an alarm, never silence it permanently", size=12, fill=MUTED, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p4_y + p4_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=RED, sw=2, marker_end="tri-navy")
text(118, ly2+5, "alarm raised", size=13, fill=INK)
line(280, ly2, 326, ly2, stroke=GREEN, sw=2, marker_end="tri-navy")
text(338, ly2+5, "condition clears", size=13, fill=INK)
line(520, ly2, 566, ly2, stroke=SOFT, sw=1.8, dash="3,3", marker_end="tri-gray")
text(578, ly2+5, "operator or timed action", size=13, fill=INK)

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

with open("./lunex-alarm-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
