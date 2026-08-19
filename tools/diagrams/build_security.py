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
  <marker id="tri-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{BLUE}"/>
  </marker>
  <marker id="diamond-navy" viewBox="0 0 14 10" refX="0.5" refY="5" markerWidth="15" markerHeight="11" orient="auto-start-reverse">
    <path d="M0 5 L7 0 L14 5 L7 10 Z" fill="{NAVY}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 6", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Security", size=26, weight=600, fill=INK)
text(60, 110, "IEC 62443 zones and conduits, mapped onto Sub-models 1\u20132 \u2014 Zone is now exclusively the security term", size=13, fill=SOFT)

# ============================================================
# Panel 1: Zone & Conduit — first-class LunexObjects
# ============================================================
p1_y = 145
p1_h = 330
rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "Zone & Conduit \u2014 First-Class LunexObjects", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "same pattern as Interlock (Sub-model 5): peers of Device and Component, not subtypes", size=12.5, fill=SOFT)

lo_x, lo_y, lo_w, lo_h = 90, p1_y+100, 220, 50
rrect(lo_x, lo_y, lo_w, lo_h, stroke=NAVY, sw=2, rx=8)
text(lo_x+lo_w/2, lo_y+22, "LunexObject", size=13.5, weight=700, fill=NAVY, anchor="middle")
text(lo_x+lo_w/2, lo_y+40, "\u00ababstract\u00bb", size=10.5, fill=SOFT, anchor="middle", style="italic")

zn_x, zn_y, zn_w, zn_h = 90, p1_y+195, 100, 60
rrect(zn_x, zn_y, zn_w, zn_h, stroke=BLUE, sw=2.4, rx=8)
text(zn_x+zn_w/2, zn_y+26, "Zone", size=14, weight=700, fill=BLUE, anchor="middle")
text(zn_x+zn_w/2, zn_y+46, "extends", size=9.5, fill=SOFT, anchor="middle", style="italic")

cn_x, cn_y, cn_w, cn_h = 210, p1_y+195, 100, 60
rrect(cn_x, cn_y, cn_w, cn_h, stroke=BLUE, sw=2.4, rx=8)
text(cn_x+cn_w/2, cn_y+26, "Conduit", size=13, weight=700, fill=BLUE, anchor="middle")
text(cn_x+cn_w/2, cn_y+46, "extends", size=9.5, fill=SOFT, anchor="middle", style="italic")

path(f"M {zn_x+zn_w/2} {zn_y} L {lo_x+lo_w/2-18} {lo_y+lo_h}", stroke=NAVY, sw=2, marker_end="tri-hollow")
path(f"M {cn_x+cn_w/2} {cn_y} L {lo_x+lo_w/2+18} {lo_y+lo_h}", stroke=NAVY, sw=2, marker_end="tri-hollow")

text(zn_x, zn_y+zn_h+26, "peer of Device, Component and", size=11.5, fill=SOFT, style="italic")
text(zn_x, zn_y+zn_h+44, "Interlock (Sub-models 1, 5)", size=11.5, fill=SOFT, style="italic")

za_x, za_y, za_w, za_h = 380, p1_y+100, 260, 195
rrect(za_x, za_y, za_w, za_h, stroke=NAVY, sw=2, rx=8)
text(za_x+16, za_y+26, "Zone", size=14, weight=700, fill=BLUE)
zattrs = [
    "+ id : string",
    "+ members : LunexObjectRef[]",
    "+ securityLevelTarget : SL-T (0-4)",
    "+ securityLevelAchieved : SL-A (0-4)",
    "+ purdueLevel : ref (Sub-model 2)",
]
ay = za_y+50
for a in zattrs:
    text(za_x+16, ay, a, size=11.5, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 24

ca_x, ca_y, ca_w, ca_h = 660, p1_y+100, 280, 195
rrect(ca_x, ca_y, ca_w, ca_h, stroke=NAVY, sw=2, rx=8)
text(ca_x+16, ca_y+26, "Conduit", size=14, weight=700, fill=BLUE)
cattrs = [
    "+ id : string",
    "+ zoneA : ZoneRef",
    "+ zoneB : ZoneRef",
    "+ controlUnit : DeviceRef",
    "  (Firewall / IDS, Sub-model 1)",
    "+ securityLevelTarget : SL-T (0-4)",
]
ay = ca_y+50
for a in cattrs:
    text(ca_x+16, ay, a, size=11.5, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 24

note_x = ca_x + ca_w + 40
text(note_x, p1_y+126, "why Zone was renamed away", size=12.5, fill=INK, weight=700)
text(note_x, p1_y+148, "from Sub-model 2:", size=12.5, fill=INK, weight=700)
text(note_x, p1_y+172, "a physical Area and a security", size=12, fill=MUTED)
text(note_x, p1_y+190, "Zone don't always coincide \u2014", size=12, fill=MUTED)
text(note_x, p1_y+208, "one word for both would hide", size=12, fill=MUTED)
text(note_x, p1_y+226, "that mismatch when it matters.", size=12, fill=MUTED)

# ============================================================
# Panel 2: Zones over the Asset Hierarchy (Sub-model 2)
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 340
rrect(30, p2_y, W-60, p2_h, stroke=BLUE, sw=2.2)
text(58, p2_y+38, "Zones Over the Asset Hierarchy", size=20, weight=700, fill=BLUE)
text(58, p2_y+60, "a Zone commonly wraps a Purdue band \u2014 but its membership is independent of the Sub-model 2 chain", size=12.5, fill=SOFT)

levels = ["Realm", "Domain", "Location", "Area", "Cell", "System", "Assembly", "Device", "Component"]
purdue = ["L4", "L4", "L4", "L3", "L2/L3", "L2", "L1/L2", "L1", "L0/L1"]
n = len(levels)
lv_y = p2_y + 190
lv_w = 130
gap2 = 18
total_w = n*lv_w + (n-1)*gap2
lv_x0 = (W - total_w)/2
lv_xs = [lv_x0 + i*(lv_w+gap2) for i in range(n)]
for x, lab, pu in zip(lv_xs, levels, purdue):
    rrect(x, lv_y, lv_w, 50, rx=8, stroke=NAVY, sw=1.8)
    text(x+lv_w/2, lv_y+24, lab, size=12.5, weight=700, fill=NAVY, anchor="middle")
    text(x+lv_w/2, lv_y+42, pu, size=10, fill=SOFT, anchor="middle")
    if x != lv_xs[-1]:
        line(x+lv_w, lv_y+25, x+lv_w+gap2, lv_y+25, stroke=GRAY_DASH, sw=1.4)

zone_defs = [
    ("Enterprise / IT Zone", "SL-T 1", 0, 2, GREEN),
    ("Operations Zone", "SL-T 2", 3, 4, BLUE),
    ("Control Zone", "SL-T 3", 5, 6, NAVY),
    ("Field Zone", "SL-T 3", 7, 8, RED),
]
for name, slt, i0, i1, col in zone_defs:
    bx0 = lv_xs[i0]
    bx1 = lv_xs[i1] + lv_w
    by = lv_y - 55
    rrect(bx0, by, bx1-bx0, 34, rx=8, stroke=col, sw=2.2, fill="#FFFFFF")
    text((bx0+bx1)/2, by+16, name, size=12, weight=700, fill=col, anchor="middle")
    text((bx0+bx1)/2, by+30, slt, size=10, fill=col, anchor="middle")
    for x in lv_xs[i0:i1+1]:
        line(x+lv_w/2, by+34, x+lv_w/2, lv_y, stroke=col, sw=1.6, dash="3,3")

# conduit markers between adjacent zone groups
for k in range(len(zone_defs)-1):
    _, _, _, i1a, cola = zone_defs[k]
    _, _, i0b, _, colb = zone_defs[k+1]
    bx = (lv_xs[i1a]+lv_w + lv_xs[i0b])/2
    by = lv_y - 55 + 17
    parts.append(f'<circle cx="{bx}" cy="{by}" r="13" fill="#FFFFFF" stroke="{BLUE}" stroke-width="2.2"/>')
    text(bx, by+4, "FW", size=9.5, weight=700, fill=BLUE, anchor="middle")

text(58, p2_y+300, "FW = Firewall / IDS Control Unit sitting on the Conduit between two Zones (Sub-model 1)", size=12, fill=MUTED, style="italic")
text(58, p2_y+320, "zone boundaries are illustrative \u2014 real deployments vary; membership is what the Zone object defines, not position alone", size=12, fill=MUTED, style="italic")

with open("./lunex-security-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part2 ok")

# ============================================================
# Panel 3: Conduit detail — contrasted with Sub-model 5's independence rule
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 320
rrect(30, p3_y, W-60, p3_h, stroke=BLUE, sw=2.2)
text(58, p3_y+38, "Conduit Detail \u2014 Where Firewall / IDS Lives", size=20, weight=700, fill=BLUE)
text(58, p3_y+60, "a controlled crossing point between two Zones, not a shared Control Unit", size=12.5, fill=SOFT)

zA_x, zA_w = 90, 380
zB_x, zB_w = W-90-380, 380
zy, zh = p3_y+110, 140
rrect(zA_x, zy, zA_w, zh, stroke=NAVY, sw=2, dash="5,4")
text(zA_x+20, zy+30, "Zone: Operations", size=14.5, weight=700, fill=NAVY)
text(zA_x+20, zy+50, "SL-T 2", size=11.5, fill=SOFT)
mini_box(zA_x+zA_w-60, zy+80, "CU", NAVY, w=56, h=38)
text(zA_x+zA_w-60, zy+118, "SCADA server", size=10.5, fill=SOFT, anchor="middle", style="italic")

rrect(zB_x, zy, zB_w, zh, stroke=NAVY, sw=2, dash="5,4")
text(zB_x+20, zy+30, "Zone: Control", size=14.5, weight=700, fill=NAVY)
text(zB_x+20, zy+50, "SL-T 3", size=11.5, fill=SOFT)
mini_box(zB_x+60, zy+80, "CU", NAVY, w=56, h=38)
text(zB_x+60, zy+118, "PLC", size=10.5, fill=SOFT, anchor="middle", style="italic")

mid_cx = W/2
fw_y = zy+80
line(zA_x+zA_w-32, fw_y, mid_cx-60, fw_y, stroke=BLUE, sw=2, marker_end="tri-blue")
line(mid_cx+60, fw_y, zB_x+32, fw_y, stroke=BLUE, sw=2, marker_end="tri-blue")
rrect(mid_cx-60, fw_y-30, 120, 60, rx=10, stroke=BLUE, sw=2.6, fill="#FFFFFF")
text(mid_cx, fw_y-6, "Firewall / IDS", size=12.5, weight=700, fill=BLUE, anchor="middle")
text(mid_cx, fw_y+13, "Control Unit", size=11, fill=SOFT, anchor="middle")
text(mid_cx, fw_y+48, "Conduit \u00b7 SL-T 2", size=11.5, fill=BLUE, weight=700, anchor="middle")

text(58, p3_y+280, "contrast with Sub-model 5: there, a shared Control Unit between BPCS and SIF was forbidden.", size=12.5, fill=MUTED, style="italic")
text(58, p3_y+298, "here, a Control Unit governing the crossing is the entire point \u2014 different rule, different context.", size=12.5, fill=MUTED, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p3_y + p3_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=NAVY, sw=2, marker_end="tri-hollow")
text(118, ly2+5, "inheritance (extends)", size=13, fill=INK)
line(320, ly2, 366, ly2, stroke=BLUE, sw=2, marker_end="tri-blue")
text(378, ly2+5, "conduit traffic, via Firewall/IDS", size=13, fill=INK)
parts.append(f'<circle cx="700" cy="{ly2}" r="12" fill="#FFFFFF" stroke="{BLUE}" stroke-width="2"/>')
text(700, ly2+4, "FW", size=9, weight=700, fill=BLUE, anchor="middle")
text(722, ly2+5, "Firewall/IDS at a zone boundary", size=13, fill=INK)

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

with open("./lunex-security-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
