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

def mini_box(cx, cy, label, col, w=48, h=34):
    rrect(cx-w/2, cy-h/2, w, h, rx=6, stroke=col, sw=2, fill="#FFFFFF")
    text(cx, cy+5, label, size=12, weight=700, fill=col, anchor="middle", family="Consolas, Menlo, monospace")

def text_bg(x, y, s, size=13, weight=400, fill=INK, anchor="middle", style="normal", pad_x=6, pad_y=3):
    est_w = size*0.6*len(s) + pad_x*2
    rect_x = x - est_w/2 if anchor == "middle" else (x - pad_x if anchor == "start" else x - est_w + pad_x)
    rect_h = size*1.15 + pad_y*2
    rect_y = y - size*0.85 - pad_y
    rrect(rect_x, rect_y, est_w, rect_h, rx=3, fill=BG, stroke="none")
    text(x, y, s, size=size, weight=weight, fill=fill, anchor=anchor, style=style)

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
  <marker id="tri-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{BLUE}"/>
  </marker>
  <marker id="tri-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{GRAY_DASH}"/>
  </marker>
  <marker id="diamond-navy" viewBox="0 0 14 10" refX="0.5" refY="5" markerWidth="15" markerHeight="11" orient="auto-start-reverse">
    <path d="M0 5 L7 0 L14 5 L7 10 Z" fill="{NAVY}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 11", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Alarm Response Guidance", size=26, weight=600, fill=INK)
text(60, 110, "ISA-18.2 response procedures \u2014 actionable (Sub-model 10) says the operator CAN act; this says HOW", size=13, fill=SOFT)

# ============================================================
# Panel 1: Alarm Response Procedure — a reusable template
# ============================================================
p1_y = 145
p1_h = 400
rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "Alarm Response Procedure (ARP) \u2014 a Reusable Template", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "tied to the alarm TYPE, not to each Alarm instance \u2014 same template pattern as the Inventory (Sub-model 1)", size=12.5, fill=SOFT)

at_x, at_y, at_w, at_h = 60, p1_y+100, 620, 220
rrect(at_x, at_y, at_w, at_h, stroke=NAVY, sw=2, rx=8)
text(at_x+18, at_y+28, "AlarmResponseProcedure", size=13.5, weight=700, fill=BLUE)
attrs = [
    "+ id : string",
    "+ appliesTo : AlarmType (condition key)",
    "+ probableCause : string",
    "+ consequenceIfIgnored : string",
    "+ correctiveAction : string",
    "+ escalation : string",
    "+ reference : string  (SOP / document link)",
]
ay = at_y+56
for a in attrs:
    text(at_x+18, ay, a, size=12, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 24

# many alarms -> one shared ARP
al_x0 = 780
al_y = p1_y + 140
arp_x, arp_y = al_x0+320, al_y+60

for i in range(3):
    ay_ = al_y + i*60
    mini_box(al_x0, ay_, "A", RED, w=90, h=38)

rrect(arp_x-90, arp_y-30, 240, 60, rx=10, stroke=BLUE, sw=2.4, fill="#FFFFFF")
text(arp_x+30, arp_y-6, "ARP: \u201cHigh Vessel", size=13, weight=700, fill=BLUE, anchor="middle")
text(arp_x+30, arp_y+14, "Pressure\u201d", size=13, weight=700, fill=BLUE, anchor="middle")

for i in range(3):
    ay_ = al_y + i*60
    line(al_x0+45, ay_, arp_x-90, arp_y, stroke=NAVY, sw=1.6)
diamond_at(arp_x-90, arp_y)
text(al_x0, al_y-45, "3 alarms of the same type", size=12, weight=700, fill=SOFT, anchor="middle")

text(58, p1_y+370, "one ARP serves every alarm of that type \u2014 not duplicated per instance, and updated in exactly one place", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 2: Mandatory for Priority 1/2 (Sub-model 10)
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 340
rrect(30, p2_y, W-60, p2_h, stroke=BLUE, sw=2.2)
text(58, p2_y+38, "Mandatory Where It Matters", size=20, weight=700, fill=BLUE)
text(58, p2_y+60, "reuses the Priority Matrix from Sub-model 10 \u2014 no new severity scale invented", size=12.5, fill=SOFT)

gx, gy = 340, p2_y+110
cell_w, cell_h = 420, 90
cells = [
    ("Priority 1 \u2014 Critical", "ARP required", RED, True, 0, 0),
    ("Priority 2 \u2014 High", "ARP required", BLUE, True, 1, 0),
    ("Priority 3 \u2014 Informational", "ARP optional", SOFT, False, 0, 1),
    ("Priority 4 \u2014 Log Only", "ARP optional", GRAY_DASH, False, 1, 1),
]
for label, req_label, col, required, cx_i, cy_i in cells:
    x = gx + cx_i*cell_w
    y = gy + cy_i*cell_h
    rrect(x, y, cell_w, cell_h, rx=10, stroke=col, sw=2.4, fill="#FFFFFF")
    text(x+20, y+32, label, size=14, weight=700, fill=col)
    badge_col = RED if required else SOFT
    rrect(x+cell_w-140, y+18, 120, 26, rx=13, stroke=badge_col, sw=1.6, fill="#FFFFFF")
    text(x+cell_w-80, y+35, req_label, size=10.5, weight=700, fill=badge_col, anchor="middle")

text(58, p2_y+308, "an actionable, high-severity alarm with no corrective action text is exactly the gap ISA-18.2 exists to close", size=12, fill=MUTED, style="italic")

with open("./lunex-arp-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part2 ok")

# ============================================================
# Panel 3: Context at the moment it matters — reusing Sub-model 7
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 380
rrect(30, p3_y, W-60, p3_h, stroke=BLUE, sw=2.2)
text(58, p3_y+38, "Context at the Moment It Matters", size=20, weight=700, fill=BLUE)
text(58, p3_y+60, "no new data source \u2014 the alarm screen surfaces relationships the Context Layer (Sub-model 7) already has", size=12.5, fill=SOFT)

acx, acy = 260, p3_y+200
rrect(acx-110, acy-40, 220, 80, rx=10, stroke=RED, sw=2.4, fill="#FFFFFF")
text(acx, acy-12, "Alarm", size=14.5, weight=700, fill=RED, anchor="middle")
text(acx, acy+12, "High Vessel Pressure", size=11.5, fill=MUTED, anchor="middle")

targets = [
    ("PT-101 trend", "source", GREEN, -1),
    ("Vessel-01", "measures", GREEN, 0),
    ("ARP: corrective action", "procedure", BLUE, 1),
]
for i, (label, rel, col, slot) in enumerate(targets):
    tx = 780
    ty = acy + slot*95
    rrect(tx, ty-28, 320, 56, rx=10, stroke=col, sw=2, fill="#FFFFFF")
    text(tx+20, ty+6, label, size=13, weight=700, fill=col)
    x1, y1 = acx+110, acy
    x2, y2 = tx-4, ty
    mk = "tri-blue" if col == BLUE else "tri-navy"
    line(x1, y1, x2, y2, stroke=col, sw=1.8, marker_end=mk)
    mx, my = (x1+x2)/2, (y1+y2)/2
    text_bg(mx, my-10, rel, size=11, fill=col, style="italic", anchor="middle")

text(58, p3_y+350, "same operator screen, zero extra configuration \u2014 the relationships already existed, this just surfaces them on alarm", size=12, fill=MUTED, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p3_y + p3_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 100, ly2, stroke=NAVY, sw=2, marker_end="diamond-navy")
text(150, ly2+5, "shares / uses (template reuse)", size=13, fill=INK)
rrect(400, ly2-13, 100, 26, rx=13, stroke=RED, sw=1.6, fill="#FFFFFF")
text(450, ly2+5, "ARP required", size=10.5, weight=700, fill=RED, anchor="middle")
text(510, ly2+5, "for Priority 1/2 alarms", size=13, fill=INK)

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

with open("./lunex-arp-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
