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

def pill(cx, cy, label, col, w=None, h=32):
    if w is None:
        w = 11*len(label) + 30
    rrect(cx-w/2, cy-h/2, w, h, rx=h/2, stroke=col, sw=1.8, fill="#FFFFFF")
    text(cx, cy+5, label, size=12, weight=700, fill=col, anchor="middle")
    return w

def mini_box(cx, cy, label, col, w=48, h=34):
    rrect(cx-w/2, cy-h/2, w, h, rx=6, stroke=col, sw=2, fill="#FFFFFF")
    text(cx, cy+5, label, size=12, weight=700, fill=col, anchor="middle", family="Consolas, Menlo, monospace")

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
  <marker id="diamond-navy" viewBox="0 0 14 10" refX="0.5" refY="5" markerWidth="15" markerHeight="11" orient="auto-start-reverse">
    <path d="M0 5 L7 0 L14 5 L7 10 Z" fill="{NAVY}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 9", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Collective Status (Rollup)", size=26, weight=600, fill=INK)
text(60, 110, "Deferred from Sub-model 4, resolved here \u2014 a computed view, not a new class (Sub-model 7 pattern)", size=13, fill=SOFT)

# ============================================================
# Panel 1: Severity tiers over the Sub-model 4 states
# ============================================================
p1_y = 145
text(58, p1_y+38, "Severity Tiers \u2014 Ranking the Sub-model 4 States", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "the state machine defines transitions, not severity \u2014 this adds the missing ranking", size=12.5, fill=SOFT)

tiers = [
    ("0", "Critical", RED, ["Emergency Stopping"]),
    ("1", "Restricted", BLUE, ["Locked", "Inhibited"]),
    ("2", "Transitioning", SOFT, ["Unlocking", "Locking", "Enabling", "Disabling", "Starting", "Inhibiting", "Clearing", "Quick Stopping", "Controlled Stopping"]),
    ("3", "Nominal", GREEN, ["On", "Standby", "Off"]),
]

# dry pass: compute the final layout height before drawing the panel box
max_x = W - 90
_ty = p1_y + 110
for _, _, _, states in tiers:
    _px, _rows = 240, 1
    for s in states:
        w = 11*len(s) + 30
        if _px + w > max_x:
            _px = 240
            _rows = 2
        _px += w + 12
    _ty += 40 + (35 if _rows == 2 else 0) + 35
p1_h = (_ty + 20) - p1_y + 30

rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "Severity Tiers \u2014 Ranking the Sub-model 4 States", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "the state machine defines transitions, not severity \u2014 this adds the missing ranking", size=12.5, fill=SOFT)

ty = p1_y + 110
for num, label, col, states in tiers:
    rrect(58, ty-22, 150, 44, rx=8, stroke=col, sw=2.2, fill="#FFFFFF")
    text(133, ty-2, f"Tier {num}", size=13, weight=700, fill=col, anchor="middle")
    text(133, ty+16, label, size=11, fill=col, anchor="middle")
    px = 240
    line_y = ty
    row_used = 1
    for s in states:
        w = 11*len(s) + 30
        if px + w > max_x:
            px = 240
            line_y += 40
            row_used = 2
        pill(px + w/2, line_y, s, col)
        px += w + 12
    ty += 40 + (35 if row_used == 2 else 0) + 35

cap_y = ty + 20
text(58, cap_y, "worstTier = the lowest tier index present anywhere below a node (0 is worst) \u2014 Off stays Tier 3, always", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 2: Rollup — computed view, not a new class
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 460
rrect(30, p2_y, W-60, p2_h, stroke=BLUE, sw=2.2)
text(58, p2_y+38, "Rollup \u2014 a Computed View, Not a New Class", size=20, weight=700, fill=BLUE)
text(58, p2_y+60, "same pattern as the Sub-model 7 telemetry envelope \u2014 no new LunexObject subtype needed", size=12.5, fill=SOFT)

jx, jy, jw, jh = 60, p2_y+100, 660, 300
rrect(jx, jy, jw, jh, stroke=NAVY, sw=2, rx=8, fill="#FFFFFF")
lines_json = [
    ('"subject"', '"lunex://.../Utilities"', BLUE),
    ('"worstTier"', '0', RED),
    ('"worstState"', '"Emergency Stopping"', RED),
    ('"tierCounts"', '{ "3": 3, "1": 1, "0": 1 }', MUTED),
    ('"contributors"', '[', MUTED),
    ('  ', '{ "path": ".../Vessel-02", "state": "Inhibited" },', BLUE),
    ('  ', '{ "path": ".../Pump-07", "state": "Emergency Stopping" }', RED),
    (' ', ']', MUTED),
    ('"computedAt"', '"2026-08-09T14:32:05Z"', MUTED),
]
ay = jy+34
text(jx+20, ay, "{", size=13, fill=INK, family="Consolas, Menlo, monospace", weight=700)
ay += 25
for k, v, col in lines_json:
    text(jx+40, ay, f'{k}: {v}' if k.strip() else v, size=11.5, fill=col, family="Consolas, Menlo, monospace")
    ay += 24
text(jx+20, ay, "}", size=13, fill=INK, family="Consolas, Menlo, monospace", weight=700)

note_x = jx + jw + 40
text(note_x, p2_y+126, "this is exactly the multi-condition case", size=12.5, fill=INK, weight=700)
text(note_x, p2_y+148, "from Sub-model 4 \u2014 an Inhibited Vessel", size=12, fill=MUTED)
text(note_x, p2_y+166, "and an Emergency Stopping Pump at the", size=12, fill=MUTED)
text(note_x, p2_y+184, "same time. Nothing is lost: the badge", size=12, fill=MUTED)
text(note_x, p2_y+202, "shows worstTier for a glance, but every", size=12, fill=MUTED)
text(note_x, p2_y+220, "contributor stays visible on demand.", size=12, fill=MUTED)

text(58, p2_y+430, "the subject's own state (LunexObject.state, Sub-model 1) is never touched by this \u2014 shown side by side, as agreed", size=12, fill=MUTED, style="italic")

with open("./lunex-rollup-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part2 ok")

# ============================================================
# Panel 3: Bubbling — each layer aggregates only its own children
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 470
rrect(30, p3_y, W-60, p3_h, stroke=BLUE, sw=2.2)
text(58, p3_y+38, "Bubbling \u2014 Each Layer Aggregates Only Its Own Children", size=20, weight=700, fill=BLUE)
text(58, p3_y+60, "a Cell never scans every Device below it \u2014 it reads its Assemblies' Rollups, already computed (Sub-model 2)", size=12.5, fill=SOFT)

def tier_badge(cx, cy, tier_label, col, r=18, fs=13):
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" stroke="#FFFFFF" stroke-width="2"/>')
    text(cx, cy+fs*0.35, tier_label, size=fs, weight=700, fill="#FFFFFF", anchor="middle")

# device layer — label sits ABOVE the box, tier badge as a small corner accent;
# nothing sits below the box, so the connector line down to the Assembly is never crossed
dev_y = p3_y + 150
dev_xs = [140+i*130 for i in range(5)]
dev_tiers = [("3", GREEN), ("3", GREEN), ("1", BLUE), ("3", GREEN), ("0", RED)]
dev_labels = ["Sensor", "Sensor", "Vessel", "Actuator", "Pump"]
for x, (t, c), lab in zip(dev_xs, dev_tiers, dev_labels):
    text(x, dev_y-30, lab, size=10.5, fill=SOFT, anchor="middle", style="italic")
    mini_box(x, dev_y, "D", c)
    tier_badge(x+22, dev_y-15, t, c, r=13, fs=11)
text(dev_xs[0]-70, dev_y-58, "Devices", size=12.5, weight=700, fill=INK)

asm_y = p3_y + 270
def diamond_at(cx, cy, col=NAVY, dw=15, dh=11):
    pts = f"{cx-dw/2},{cy} {cx},{cy-dh/2} {cx+dw/2},{cy} {cx},{cy+dh/2}"
    parts.append(f'<polygon points="{pts}" fill="{col}"/>')

asm1_x, asm2_x = 270, 660
line(asm1_x, asm_y-22, dev_xs[0], dev_y+22, stroke=NAVY, sw=1.6)
line(asm1_x, asm_y-22, dev_xs[1], dev_y+22, stroke=NAVY, sw=1.6)
line(asm2_x, asm_y-22, dev_xs[2], dev_y+22, stroke=NAVY, sw=1.6)
line(asm2_x, asm_y-22, dev_xs[3], dev_y+22, stroke=NAVY, sw=1.6)
line(asm2_x, asm_y-22, dev_xs[4], dev_y+22, stroke=NAVY, sw=1.6)

rrect(asm1_x-70, asm_y-22, 140, 44, rx=8, stroke=GREEN, sw=2.2, fill="#FFFFFF")
text(asm1_x, asm_y-2, "Assembly-01", size=11.5, weight=700, fill=INK, anchor="middle")
text(asm1_x, asm_y+14, "Rollup: Tier 3", size=10.5, fill=GREEN, weight=700, anchor="middle")

rrect(asm2_x-70, asm_y-22, 140, 44, rx=8, stroke=RED, sw=2.2, fill="#FFFFFF")
text(asm2_x, asm_y-2, "Assembly-02", size=11.5, weight=700, fill=INK, anchor="middle")
text(asm2_x, asm_y+14, "Rollup: Tier 0", size=10.5, fill=RED, weight=700, anchor="middle")
text(asm1_x-160, asm_y+5, "Assemblies", size=12.5, weight=700, fill=INK)
diamond_at(asm1_x, asm_y-22)
diamond_at(asm2_x, asm_y-22)

cell_y = p3_y + 380
cell_x = (asm1_x+asm2_x)/2
line(cell_x, cell_y-26, asm1_x, asm_y+22, stroke=NAVY, sw=1.8)
line(cell_x, cell_y-26, asm2_x, asm_y+22, stroke=NAVY, sw=1.8)
rrect(cell_x-100, cell_y-26, 200, 52, rx=10, stroke=RED, sw=2.6, fill="#FFFFFF")
text(cell_x, cell_y-4, "Cell \u2014 Utilities", size=13.5, weight=700, fill=INK, anchor="middle")
text(cell_x, cell_y+14, "Rollup: Tier 0 (from Assembly-02 only)", size=10.5, fill=RED, weight=700, anchor="middle")
diamond_at(cell_x, cell_y-26)
text(cell_x+150, cell_y+5, "Cell", size=12.5, weight=700, fill=INK)

text(58, p3_y+425, "the Cell never looked at the five Devices directly \u2014 it only compared two Assembly Rollups. That's the bubble.", size=12, fill=MUTED, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p3_y + p3_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
tier_badge(76, ly2, "0", RED)
text(102, ly2+5, "Critical", size=13, fill=INK)
tier_badge(220, ly2, "1", BLUE)
text(246, ly2+5, "Restricted", size=13, fill=INK)
tier_badge(390, ly2, "2", SOFT)
text(416, ly2+5, "Transitioning", size=13, fill=INK)
tier_badge(590, ly2, "3", GREEN)
text(616, ly2+5, "Nominal", size=13, fill=INK)
line(770, ly2, 816, ly2, stroke=NAVY, sw=2, marker_start="diamond-navy")
text(828, ly2+5, "rolls up into (worst tier only)", size=13, fill=INK)

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

with open("./lunex-rollup-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
