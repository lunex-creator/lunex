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

W, H = 1500, 1750
parts = []

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def rrect(x, y, w, h, rx=12, fill="#FFFFFF", stroke=NAVY, sw=2, dash=None, opacity=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' fill-opacity="{opacity}"' if opacity is not None else ""
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')

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

head = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Inter, Segoe UI, Helvetica Neue, Arial, sans-serif">
<defs>
  <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
    <path d="M20 0H0V20" fill="none" stroke="#E6EBF0" stroke-width="1"/>
  </pattern>
  <pattern id="grid5" width="100" height="100" patternUnits="userSpaceOnUse">
    <rect width="100" height="100" fill="url(#grid)"/>
    <path d="M100 0H0V100" fill="none" stroke="{LINE}" stroke-width="1"/>
  </pattern>
  <marker id="tri-hollow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">
    <path d="M0 0 L12 6 L0 12 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="1.4"/>
  </marker>
  <marker id="diamond-navy" viewBox="0 0 14 10" refX="0.5" refY="5" markerWidth="15" markerHeight="11" orient="auto-start-reverse">
    <path d="M0 5 L7 0 L14 5 L7 10 Z" fill="{NAVY}"/>
  </marker>
  <marker id="tri-gray" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
    <path d="M0 0 L12 6 L0 12 Z" fill="#FFFFFF" stroke="{GRAY_DASH}" stroke-width="1.4"/>
  </marker>
</defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#grid5)"/>
'''
parts.append(head)

text(60, 56, "LUNEX — SUB-MODEL 2", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Asset Hierarchy / Namespace", size=26, weight=600, fill=INK)
text(60, 110, "A composed, addressable containment chain, mapped onto Purdue levels 0\u20134", size=13, fill=SOFT)

# ---------- chain ----------
bx, bw = 140, 480
levels = [
    ("Realm", "L4", "root namespace \u2014 the whole organization", False, None),
    ("Domain", "L4", "business unit / sub-namespace", True, "optional \u2014 skip when trivial"),
    ("Location", "L4", "physical location \u2014 plant, building, vessel, remote site", False, None),
    ("Area", "L3", "process area within a Location", False, None),
    ("Cell", "L2/L3", "process cell within an Area", False, None),
    ("System", "L2", "functional unit within a Cell \u2014 equivalent to ISA-88's Unit", False, None),
    ("Assembly", "L1/L2", "functional device group \u2192 see Sub-model 3 (topology patterns)", False, None),
    ("Device", "L1", "Sensor / Transducer / Control Unit / Signal Converter / Actuator \u2192 see Sub-model 1", False, None),
    ("Component", "L0/L1", "not independently addressable \u2192 see Sub-model 1", False, None),
]

box_h = 108
gap = 54
step = box_h + gap
top0 = 150

purdue_opacity = {"L4": 1.0, "L3": 0.8, "L2/L3": 0.65, "L2": 0.55, "L1/L2": 0.42, "L1": 0.32, "L0/L1": 0.22}

box_ys = []
for idx, (name, purdue, role, optional, note) in enumerate(levels):
    y = top0 + idx*step
    box_ys.append(y)
    dash = "6,4" if optional else None
    rrect(bx, y, bw, box_h, stroke=NAVY, sw=2, dash=dash)
    text(bx+24, y+34, name, size=19, weight=700, fill=NAVY)
    text(bx+24, y+58, role, size=12, fill=MUTED)
    if note:
        text(bx+24, y+82, note, size=11.5, fill=SOFT, style="italic")

    # purdue badge
    badge_w = 64
    op = purdue_opacity[purdue]
    rrect(bx+bw+30, y+box_h/2-16, badge_w, 32, rx=16, fill=NAVY, stroke="none", opacity=op)
    text(bx+bw+30+badge_w/2, y+box_h/2+5, purdue, size=13, weight=700, fill="#FFFFFF", anchor="middle")

# composition arrows between consecutive levels
for idx in range(len(levels)-1):
    y1 = box_ys[idx] + box_h
    y2 = box_ys[idx+1]
    cx_line = bx + 70
    line(cx_line, y1, cx_line, y2, stroke=NAVY, sw=2, marker_start="diamond-navy", marker_end="tri-hollow")
    text(cx_line+14, (y1+y2)/2+4, "0..*", size=12, fill=SOFT, style="italic")

# ---------- skip illustration: Realm -> Location bypassing Domain ----------
skip_x = bx - 55
realm_bottom = box_ys[0] + box_h/2
location_mid = box_ys[2] + box_h/2
path(f"M {bx} {box_ys[0]+box_h-18} C {skip_x} {box_ys[0]+box_h-18}, {skip_x} {box_ys[2]+18}, {bx} {box_ys[2]+18}",
     stroke=GRAY_DASH, sw=2, dash="5,4", marker_end="tri-gray")
mid_y = (box_ys[0]+box_h+box_ys[2])/2
parts.append(f'<text x="{skip_x-16}" y="{mid_y}" font-size="11.5" fill="{SOFT}" font-style="italic" text-anchor="middle" transform="rotate(-90 {skip_x-16} {mid_y})">skip when trivial</text>')

chain_bottom = box_ys[-1] + box_h

# ---------- namespace example ----------
ex_y = chain_bottom + 70
ex_x, ex_w = 60, W - 120
rrect(ex_x, ex_y, ex_w, 190, stroke=SOFT, sw=1.5, fill="#FFFFFF")
text(ex_x+24, ex_y+30, "ADDRESSABLE PATH \u2014 EXAMPLE", size=12, fill=SOFT, spacing="1.5")
text(ex_x+24, ex_y+62, "lunex://AcmeCorp/Benelux/RotterdamPlant/Utilities/Boilerhouse/BoilerUnit-1/PressureLoop-3/PT-101",
     size=14.5, fill=INK, family="Consolas, Menlo, monospace", weight=600)

seg_labels = ["Realm", "Domain", "Location", "Area", "Cell", "System", "Assembly", "Device"]
seg_values = ["AcmeCorp", "Benelux", "RotterdamPlant", "Utilities", "Boilerhouse", "BoilerUnit-1", "PressureLoop-3", "PT-101"]
sx = ex_x+24
sy = ex_y + 95
col_w = (ex_w - 48) / 8
for lab, val in zip(seg_labels, seg_values):
    text(sx, sy, lab, size=10.5, fill=SOFT, spacing="0.5")
    text(sx, sy+18, val, size=11, fill=MUTED, family="Consolas, Menlo, monospace")
    sx += col_w
text(ex_x+24, ex_y+150, "every LunexObject.id (Sub-model 1) is derivable from its position in this chain \u2014", size=12.5, fill=SOFT, style="italic")
text(ex_x+24, ex_y+168, "Component only appears in the path when addressing an internal signal, e.g. ...PT-101/AI-input", size=12.5, fill=SOFT, style="italic")

# ---------- legend ----------
leg_y = ex_y + 190 + 60
line(60, leg_y-15, ex_x+ex_w, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y+40
line(60, ly2, 110, ly2, stroke=NAVY, sw=2, marker_start="diamond-navy", marker_end="tri-hollow")
text(122, ly2+5, "composition (has 0..*)", size=13, fill=INK)

rrect(380, ly2-16, 64, 32, rx=16, fill=NAVY, stroke="none", opacity=1.0)
text(412, ly2+5, "L4", size=13, weight=700, fill="#FFFFFF", anchor="middle")
text(460, ly2+5, "Purdue level (darker = closer to Enterprise)", size=13, fill=INK)

ly3 = ly2 + 44
rrect(60, ly3-14, 44, 26, rx=13, stroke=NAVY, sw=1.6, fill="#FFFFFF", dash="6,4")
text(82, ly3+5, "", size=13, anchor="middle")
text(115, ly3+5, "dashed border = optional level", size=13, fill=INK)

path(f"M 500 {ly3} L 550 {ly3}", stroke=GRAY_DASH, sw=2, dash="5,4", marker_end="tri-gray")
text(562, ly3+5, "illustrates skipping a level when trivial", size=13, fill=INK)

final_h = int(ly3 + 60)
parts.append("</svg>")

svg = "\n".join(parts)
svg = svg.replace(f'viewBox="0 0 {W} {H}" width="{W}" height="{H}"', f'viewBox="0 0 {W} {final_h}" width="{W}" height="{final_h}"')
svg = svg.replace(f'<rect width="{W}" height="{H}" fill="{BG}"/>', f'<rect width="{W}" height="{final_h}" fill="{BG}"/>')
svg = svg.replace(f'<rect width="{W}" height="{H}" fill="url(#grid5)"/>', f'<rect width="{W}" height="{final_h}" fill="url(#grid5)"/>')
svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg

with open("./lunex-asset-hierarchy.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("done", final_h)
