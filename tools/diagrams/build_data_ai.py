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
  <marker id="tri-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{BLUE}"/>
  </marker>
  <marker id="tri-hollow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">
    <path d="M0 0 L12 6 L0 12 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="1.4"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 7", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Data / AI Layer", size=26, weight=600, fill=INK)
text(60, 110, "The layer PackML and S88 don't have \u2014 telemetry with meaning attached, ready for AI consumption", size=13, fill=SOFT)

# ============================================================
# Panel 1: Telemetry Envelope
# ============================================================
p1_y = 145
p1_h = 420
rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "Telemetry Envelope \u2014 What Every LunexObject Emits", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "no new fields invented \u2014 this just wraps and addresses what Sub-models 1, 2 and 4 already define", size=12.5, fill=SOFT)

jx, jy, jw, jh = 60, p1_y+100, 620, 250
rrect(jx, jy, jw, jh, stroke=NAVY, sw=2, rx=8, fill="#FFFFFF")
lines_json = [
    ('"path"', '"lunex://AcmeCorp/.../PT-101"', BLUE),
    ('"timestamp"', '"2026-08-09T14:32:01Z"', MUTED),
    ('"class"', '"Sensor.PressureSensor"', GREEN),
    ('"state"', '"On"', NAVY),
    ('"health"', '{ "score": 0.97, "flags": [] }', MUTED),
    ('"properties"', '{ "value": 4.2, "unit": "bar" }', MUTED),
]
ay = jy+34
text(jx+20, ay, "{", size=13, fill=INK, family="Consolas, Menlo, monospace", weight=700)
ay += 26
for k, v, col in lines_json:
    text(jx+40, ay, f'{k}: {v}', size=12.5, fill=col, family="Consolas, Menlo, monospace")
    ay += 27
text(jx+20, ay, "}", size=13, fill=INK, family="Consolas, Menlo, monospace", weight=700)

anno_x = jx + jw + 50
annos = [
    ("path", "Sub-model 2 \u2014 the addressable namespace"),
    ("class", "Sub-model 1 \u2014 which universal class / derived type"),
    ("state", "Sub-model 4 \u2014 the state machine instance"),
    ("health", "Sub-model 1 \u2014 diagnostics, independent of state"),
    ("properties", "Sub-model 1 \u2014 the object's own parameters"),
]
ay2 = jy+30
for k, note in annos:
    text(anno_x, ay2, k, size=12.5, weight=700, fill=BLUE, family="Consolas, Menlo, monospace")
    text(anno_x+80, ay2, note, size=12, fill=MUTED)
    ay2 += 34

text(58, p1_y+382, "same envelope for a Sensor, a Firewall/IDS or an Interlock \u2014 one shape, every class (Sub-models 1, 5, 6)", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 2: Context Layer — semantic relationships beyond containment
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 400
rrect(30, p2_y, W-60, p2_h, stroke=BLUE, sw=2.2)
text(58, p2_y+38, "Context Layer \u2014 What Makes It AI-Ready, Not Just Data", size=20, weight=700, fill=BLUE)
text(58, p2_y+60, "semantic relationships an AI can traverse \u2014 separate from the containment chain in Sub-model 2", size=12.5, fill=SOFT)

cx0 = W/2
cy0 = p2_y + 185
mini_box(cx0, cy0, "S", GREEN, w=64, h=44)
text(cx0, cy0+40, "PT-101", size=11.5, fill=SOFT, anchor="middle", style="italic")

targets = [
    (cx0-460, cy0-90, "Vessel-01", "measures", GREEN),
    (cx0-460, cy0+90, "Assembly-04", "partOf", NAVY),
    (cx0+460, cy0-90, "unit: bar", "hasUnit", BLUE),
    (cx0+460, cy0+90, "ISA-5.1 / PI&ID tag", "semanticTag", BLUE),
]
for tx, ty, label, rel, col in targets:
    rrect(tx-100, ty-24, 200, 48, rx=10, stroke=col, sw=2, fill="#FFFFFF")
    text(tx, ty+6, label, size=12.5, weight=700, fill=col, anchor="middle")
    lx = tx + (100 if tx < cx0 else -100)
    ex = cx0 + (-32 if tx < cx0 else 32)
    ey = cy0 + (-14 if ty < cy0 else 14)
    line(lx, ty, ex, ey, stroke=col, sw=1.8, marker_end="tri-navy" if col==NAVY else ("tri-blue" if col==BLUE else "tri-navy"))
    mx, my = (lx+ex)/2, (ty+ey)/2
    text(mx, my - 10, rel, size=11, fill=col, style="italic", anchor="middle", halo=True)

text(58, p2_y+372, "Sub-model 2 answers \u201cwhat contains what\u201d \u2014 the Context Layer answers \u201cwhat relates to what, and what does it mean\u201d", size=12, fill=MUTED, style="italic")

with open("./lunex-data-ai-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part2 ok")

# ============================================================
# Panel 3: Digital Twin — the AI-side mirror
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 285
rrect(30, p3_y, W-60, p3_h, stroke=BLUE, sw=2.2)
text(58, p3_y+38, "Digital Twin \u2014 the AI-Side Mirror", size=20, weight=700, fill=BLUE)
text(58, p3_y+60, "kept in sync by the telemetry envelope, at whatever rate the Cloud & Analytics flag (Sub-model 3) allows", size=12.5, fill=SOFT)

phys_x, phys_w = 100, 340
twin_x, twin_w = W-100-340, 340
ty3 = p3_y + 150

rrect(phys_x, ty3-55, phys_w, 110, rx=10, stroke=NAVY, sw=2.2)
text(phys_x+phys_w/2, ty3-20, "Physical Object", size=14.5, weight=700, fill=NAVY, anchor="middle")
mini_box(phys_x+phys_w/2, ty3+18, "S", GREEN, w=56, h=38)
text(phys_x+phys_w/2, ty3+50, "PT-101 (Sub-model 1)", size=11, fill=SOFT, anchor="middle", style="italic")

rrect(twin_x, ty3-55, twin_w, 110, rx=10, stroke=BLUE, sw=2.4)
text(twin_x+twin_w/2, ty3-20, "Digital Twin", size=14.5, weight=700, fill=BLUE, anchor="middle")
mini_box(twin_x+twin_w/2, ty3+18, "S'", BLUE, w=56, h=38)
text(twin_x+twin_w/2, ty3+50, "AI / Analytics Layer", size=11, fill=SOFT, anchor="middle", style="italic")

midx3 = W/2
line(phys_x+phys_w, ty3-10, midx3-70, ty3-10, stroke=BLUE, sw=2, marker_end="tri-blue")
line(midx3+70, ty3+10, twin_x, ty3+10, stroke=GRAY_DASH, sw=1.6, dash="4,3")
rrect(midx3-70, ty3-35, 140, 50, rx=10, stroke=BLUE, sw=2, fill="#FFFFFF")
text(midx3, ty3-10, "telemetry envelope", size=11, weight=700, fill=BLUE, anchor="middle")
text(midx3, ty3+8, "(Panel 1)", size=10, fill=SOFT, anchor="middle")
text(midx3, ty3+42, "queries flow back", size=10.5, fill=SOFT, style="italic", anchor="middle")

text(58, p3_y+230, "the twin is what an AI model actually queries \u2014 it never touches the physical Device directly", size=12, fill=MUTED, style="italic")
text(58, p3_y+252, "the Twin only ever holds the current state \u2014 for everything the state WAS, see the Historian (Sub-model 14)", size=12, fill=MUTED, style="italic")

# ============================================================
# Closing note: resolving the Sub-model 4 rollup deferral
# ============================================================
p4_y = p3_y + p3_h + 45
p4_h = 110
rrect(30, p4_y, W-60, p4_h, stroke=GREEN, sw=2.2)
text(58, p4_y+30, "Closing the loop from Sub-model 4", size=15, weight=700, fill=GREEN)
text(58, p4_y+52, "collective status (\u201crollup\u201d) was deliberately left out of the state model \u2014 formalized in Sub-model 9,", size=12.5, fill=MUTED)
text(58, p4_y+72, "computed on the Digital Twin graph this layer maintains: worst-case tier, tier counts, and the full list of", size=12.5, fill=MUTED)
text(58, p4_y+92, "contributors \u2014 not baked into LunexObject itself, and never overwriting an object's own state.", size=12.5, fill=MUTED)

# ============================================================
# Legend
# ============================================================
leg_y = p4_y + p4_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=BLUE, sw=2, marker_end="tri-blue")
text(118, ly2+5, "telemetry (physical \u2192 twin)", size=13, fill=INK)
line(320, ly2, 366, ly2, stroke=GRAY_DASH, sw=1.6, dash="4,3")
text(378, ly2+5, "queries / commands (twin \u2192 physical)", size=13, fill=INK)
line(660, ly2, 706, ly2, stroke=GREEN, sw=1.8, marker_end="tri-navy")
text(718, ly2+5, "semantic relationship (Context Layer)", size=13, fill=INK)

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

with open("./lunex-data-ai-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
