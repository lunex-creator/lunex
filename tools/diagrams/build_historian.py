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
  <marker id="tri-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{BLUE}"/>
  </marker>
  <marker id="tri-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{GRAY_DASH}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 14", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Historian & Analytics", size=26, weight=600, fill=INK)
text(60, 110, "what the state WAS, not just what it IS \u2014 the retrospective half of Sub-model 7", size=13, fill=SOFT)

# ============================================================
# Panel 1: Historian — append-only, the Twin's other destination
# ============================================================
p1_y = 145
p1_h = 330
rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "Historian \u2014 Append-Only, Not Overwritten", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "same Telemetry Envelope (Sub-model 7), two destinations \u2014 one overwrites, one never does", size=12.5, fill=SOFT)

src_x, src_y = 260, p1_y+190
rrect(src_x-110, src_y-30, 220, 60, rx=10, stroke=NAVY, sw=2.2, fill="#FFFFFF")
text(src_x, src_y+5, "Telemetry Envelope", size=13.5, weight=700, fill=NAVY, anchor="middle")

twin_x, twin_y = 760, p1_y+120
rrect(twin_x-140, twin_y-30, 280, 60, rx=10, stroke=BLUE, sw=2.2, fill="#FFFFFF")
text(twin_x, twin_y-6, "Digital Twin", size=13.5, weight=700, fill=BLUE, anchor="middle")
text(twin_x, twin_y+14, "overwrites \u2014 current state only", size=11, fill=SOFT, anchor="middle")

hist_x, hist_y = 760, p1_y+260
rrect(hist_x-140, hist_y-30, 280, 60, rx=10, stroke=GREEN, sw=2.4, fill="#FFFFFF")
text(hist_x, hist_y-6, "Historian", size=13.5, weight=700, fill=GREEN, anchor="middle")
text(hist_x, hist_y+14, "appends \u2014 every state, ever", size=11, fill=SOFT, anchor="middle")

line(src_x+110, src_y-14, twin_x-140, twin_y, stroke=BLUE, sw=1.8, marker_end="tri-blue")
line(src_x+110, src_y+14, hist_x-140, hist_y, stroke=GREEN, sw=1.8, marker_end="tri-navy")

sx2, sy2 = 1120, p1_y+190
rrect(sx2-140, sy2-70, 340, 200, rx=10, stroke=NAVY, sw=2, fill="#FFFFFF")
text(sx2, sy2-40, "HistorianRecord", size=13.5, weight=700, fill=NAVY, anchor="middle")
hattrs = ["path, timestamp  (Sub-model 2/7)", "state, health, properties", "retention : RetentionPolicyRef"]
hy = sy2-14
for a in hattrs:
    text(sx2-120, hy, "+ "+a, size=11.5, fill=MUTED, family="Consolas, Menlo, monospace")
    hy += 24
text(sx2-120, hy+14, "one row per envelope, kept at", size=11, fill=SOFT, style="italic")
text(sx2-120, hy+32, "whatever resolution the policy sets", size=11, fill=SOFT, style="italic")

text(58, p1_y+300, "the Historian never blocks or slows the Twin \u2014 it observes the same stream, it doesn't gate it", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 2: RetentionPolicy — mirrors SimulationPolicy (Sub-model 12)
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 560
rrect(30, p2_y, W-60, p2_h, stroke=BLUE, sw=2.2)
text(58, p2_y+38, "Retention Policy \u2014 the Same Shape as Simulation Policy", size=20, weight=700, fill=BLUE)
text(58, p2_y+60, "decided in advance, per Assembly \u2014 the classic big-data cost/detail trade-off, not a new decision pattern", size=12.5, fill=SOFT)

pol_y = p2_y+110
col_w3 = (W-60-80-40)/3
cols3 = [60, 60+col_w3+20, 60+2*(col_w3+20)]
policies = [
    ("always", GREEN, "every point kept at full", "resolution \u2014 highest cost"),
    ("risk-based", BLUE, "full resolution only where it", "matters \u2014 the default"),
    ("none", SOFT, "no automatic trigger \u2014 relies entirely on", "manualOverrideAvailable below"),
]
for (name, col, l1, l2), x in zip(policies, cols3):
    rrect(x, pol_y, col_w3, 150, rx=10, stroke=col, sw=2.4, fill="#FFFFFF")
    text(x+20, pol_y+34, name, size=15, weight=700, fill=col, family="Consolas, Menlo, monospace")
    text(x+20, pol_y+62, l1, size=11.5, fill=MUTED)
    text(x+20, pol_y+80, l2, size=11.5, fill=MUTED)

mid_x = cols3[1] + col_w3/2
text(mid_x, pol_y+128, "RetentionPolicy.automaticMode", size=11, weight=700, fill=BLUE, anchor="middle", family="Consolas, Menlo, monospace")
text(mid_x, pol_y+144, "reuses the severity tiers \u2014 same field as Sub-model 12", size=11, fill=SOFT, style="italic", anchor="middle")

override_y = pol_y + 168
rrect(60, override_y, W-120, 46, rx=10, stroke=GREEN, sw=2, fill="#FFFFFF")
text(84, override_y+29, "manualOverrideAvailable : true \u2014 always, regardless of automaticMode (not a fourth \u201chybrid\u201d mode)", size=12.5, weight=700, fill=GREEN, family="Consolas, Menlo, monospace")

ex_y = override_y + 76
rrect(60, ex_y, W-120, 130, rx=10, stroke=NAVY, sw=2, fill="#FFFFFF")
text(84, ex_y+30, "example: Assembly \u201cReactor Feed\u201d, RetentionPolicy.automaticMode = risk-based, riskThreshold = Tier 1", size=13, weight=700, fill=INK)
text(84, ex_y+58, "\u2022 normal telemetry, worstTier stays 3 \u2192 downsampled after 24h (1-minute averages, kept 1 year)", size=12, fill=MUTED)
text(84, ex_y+80, "\u2022 a contributor to a Tier \u2264 1 rollup, or the source of a Priority 1/2 alarm (Sub-model 9/10) \u2192", size=12, fill=MUTED)
text(84, ex_y+100, "  kept at full raw resolution, indefinitely \u2014 exactly the data an investigation will need", size=12, fill=MUTED)

text(58, ex_y+160, "same policy shape as Sub-model 12 by design \u2014 one mental model for \u201cwhen does this get the expensive treatment\u201d", size=12, fill=MUTED, style="italic")

with open("./lunex-historian-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part2 ok")

# ============================================================
# Panel 3: Analytics — descriptive, not predictive
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 480
rrect(30, p3_y, W-60, p3_h, stroke=BLUE, sw=2.2)
text(58, p3_y+38, "Analytics \u2014 Descriptive, Not Predictive", size=20, weight=700, fill=BLUE)
text(58, p3_y+60, "deliberately distinct from Sub-model 12 \u2014 this looks back at the Historian, that looks forward on the Twin", size=12.5, fill=SOFT)

colw = (W-60-80-60)/2
ax = 60
sx3 = ax + colw + 60
by3 = p3_y+110

rrect(ax, by3, colw, 110, stroke=BLUE, sw=2.2, fill="#FFFFFF")
text(ax+24, by3+30, "Analytics (here)", size=14.5, weight=700, fill=BLUE)
text(ax+24, by3+52, "source: Historian, retrospective", size=11.5, fill=BLUE, style="italic", family="Consolas, Menlo, monospace")
text(ax+24, by3+78, "what happened, how often,", size=12, fill=MUTED)
text(ax+24, by3+96, "how this alarm/loop performs", size=12, fill=MUTED)

rrect(sx3, by3, colw, 110, stroke=SOFT, sw=2, fill="#FFFFFF")
text(sx3+24, by3+30, "Scenario Simulation (Sub-model 12)", size=14, weight=700, fill=SOFT)
text(sx3+24, by3+52, "source: Digital Twin, predictive", size=11.5, fill=SOFT, style="italic", family="Consolas, Menlo, monospace")
text(sx3+24, by3+78, "what would happen if \u2014", size=12, fill=MUTED)
text(sx3+24, by3+96, "before the operator acts", size=12, fill=MUTED)

metrics_y = by3 + 160
rrect(60, metrics_y, W-120, 170, rx=10, stroke=NAVY, sw=2, fill="#FFFFFF")
text(84, metrics_y+30, "ISA-18.2 requires alarm performance metrics \u2014 impossible without the Historian", size=13.5, weight=700, fill=INK)
metrics = [
    "alarms per hour, per operator position \u2014 industry benchmark: < 6/hour average, < 2/10min in upset",
    "\u201cbad actors\u201d \u2014 the small set of alarm types generating a disproportionate share of all activations",
    "average time-to-acknowledge, by Priority (Sub-model 10) \u2014 is Priority 1 actually acknowledged fastest?",
    "stale alarms \u2014 Shelved (Sub-model 10) instances approaching shelvedUntil expiry, not yet resolved",
]
my = metrics_y+56
for m in metrics:
    text(84, my, "\u2022 " + m, size=12, fill=MUTED)
    my += 27

text(58, p3_y+458, "computed periodically over Historian data, not streamed \u2014 a report, not a telemetry envelope", size=12, fill=MUTED, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p3_y + p3_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=BLUE, sw=1.8, marker_end="tri-blue")
text(118, ly2+5, "to Digital Twin (current state)", size=13, fill=INK)
line(400, ly2, 446, ly2, stroke=GREEN, sw=1.8, marker_end="tri-navy")
text(458, ly2+5, "to Historian (permanent record)", size=13, fill=INK)

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

with open("./lunex-historian-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
