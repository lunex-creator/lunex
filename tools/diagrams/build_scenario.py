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
  <marker id="tri-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{GREEN}"/>
  </marker>
  <marker id="tri-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{GRAY_DASH}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 12", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Scenario Simulation & Operator Guidance", size=26, weight=600, fill=INK)
text(60, 110, "AI-driven, not just alarm-triggered \u2014 tested on the Digital Twin (Sub-model 7) before the operator ever sees it", size=13, fill=SOFT)

# ============================================================
# Panel 1: GuidanceRecommendation & ScenarioResult
# ============================================================
p1_y = 145
p1_h = 380
rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "GuidanceRecommendation \u2014 a Set of Simulated Scenarios", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "peer of Interlock, Zone, Conduit, Alarm \u2014 goldenScenarioId is optional, not guaranteed", size=12.5, fill=SOFT)

gx, gy, gw, gh = 60, p1_y+100, 560, 230
rrect(gx, gy, gw, gh, stroke=NAVY, sw=2, rx=8)
text(gx+18, gy+28, "GuidanceRecommendation", size=13.5, weight=700, fill=BLUE)
gattrs = [
    "+ id : string",
    "+ context : DeviceRef | AlarmRef",
    "+ source : procedural | simulated",
    "+ scenarios : ScenarioResult[]",
    "+ goldenScenarioId : string | null",
    "+ generatedAt : timestamp",
]
ay = gy+56
for a in gattrs:
    text(gx+18, ay, a, size=12, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 24
text(gx+18, ay+6, "null \u2192 equivalent options shown,", size=11.5, fill=RED, style="italic")
text(gx+18, ay+24, "no single \u201cbest\u201d recommended", size=11.5, fill=RED, style="italic")

sx, sy, sw_, sh_ = 680, p1_y+100, 560, 230
rrect(sx, sy, sw_, sh_, stroke=NAVY, sw=2, rx=8)
text(sx+18, sy+28, "ScenarioResult", size=13.5, weight=700, fill=BLUE)
sattrs = [
    "+ id : string",
    "+ description : string",
    "+ predictedOutcome : string",
    "+ successProbability : 0\u20131",
    "+ isGolden : bool",
]
ay = sy+56
for a in sattrs:
    text(sx+18, ay, a, size=12, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 24
line(gx+gw, gy+gh/2, sx, sy+sh_/2, stroke=NAVY, sw=1.8, marker_start="diamond-navy")
text((gx+gw+sx)/2, gy+gh/2-10, "0..*", size=11.5, fill=SOFT, style="italic", anchor="middle")

text(58, p1_y+350, "tested on the Digital Twin, not the physical Device \u2014 a wrong scenario costs nothing (Sub-model 7)", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 2: Two sources, one operator screen
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 400
rrect(30, p2_y, W-60, p2_h, stroke=BLUE, sw=2.2)
text(58, p2_y+38, "Two Sources, One Operator Screen", size=20, weight=700, fill=BLUE)
text(58, p2_y+60, "static procedure and live simulation feed the same guidance panel \u2014 for alarms AND normal operation", size=12.5, fill=SOFT)

colw = (W-60-80-60)/2
arp_x = 60
sim_x = arp_x + colw + 60
by = p2_y+100

rrect(arp_x, by, colw, 130, stroke=SOFT, sw=2, fill="#FFFFFF")
text(arp_x+24, by+30, "ARP (Sub-model 11)", size=14.5, weight=700, fill=SOFT)
text(arp_x+24, by+52, "source: procedural", size=11.5, fill=SOFT, style="italic", family="Consolas, Menlo, monospace")
text(arp_x+24, by+80, "static, engineer-written \u2014", size=12, fill=MUTED)
text(arp_x+24, by+100, "same text every time", size=12, fill=MUTED)

rrect(sim_x, by, colw, 130, stroke=BLUE, sw=2.4, fill="#FFFFFF")
text(sim_x+24, by+30, "Scenario Simulation", size=14.5, weight=700, fill=BLUE)
text(sim_x+24, by+52, "source: simulated", size=11.5, fill=BLUE, style="italic", family="Consolas, Menlo, monospace")
text(sim_x+24, by+80, "dynamic, on the Digital Twin \u2014", size=12, fill=MUTED)
text(sim_x+24, by+100, "current state, current outcome", size=12, fill=MUTED)

scr_x = (arp_x+colw/2 + sim_x+colw/2)/2
scr_y = by + 200
rrect(scr_x-160, scr_y-30, 320, 60, rx=10, stroke=NAVY, sw=2.4, fill="#FFFFFF")
text(scr_x, scr_y-6, "Operator Guidance Panel", size=13.5, weight=700, fill=NAVY, anchor="middle")
text(scr_x, scr_y+14, "same screen, whichever fired", size=11, fill=SOFT, anchor="middle")

line(arp_x+colw/2, by+130, scr_x-40, scr_y-30, stroke=SOFT, sw=1.8, marker_end="tri-gray")
line(sim_x+colw/2, by+130, scr_x+40, scr_y-30, stroke=BLUE, sw=1.8, marker_end="tri-blue")

text(58, p2_y+365, "an alarm can trigger either or both; a normal setpoint change can too \u2014 governed by the policy in Panel 3", size=12, fill=MUTED, style="italic")

with open("./lunex-scenario-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part2 ok")

# ============================================================
# Panel 3: SimulationPolicy — when does normal operation get simulated
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 560
rrect(30, p3_y, W-60, p3_h, stroke=BLUE, sw=2.2)
text(58, p3_y+38, "Simulation Policy \u2014 When Normal Operation Gets Checked", size=20, weight=700, fill=BLUE)
text(58, p3_y+60, "decided in advance, per Assembly \u2014 not every setpoint change needs an AI simulation", size=12.5, fill=SOFT)

pol_y = p3_y+110
col_w3 = (W-60-80-40)/3
cols3 = [60, 60+col_w3+20, 60+2*(col_w3+20)]
policies = [
    ("always", GREEN, "every operator action is simulated first", "highest assurance, highest compute cost"),
    ("risk-based", BLUE, "simulated only if predicted worst-case", "\u2265 Tier 1 (Sub-model 9) \u2014 the middle ground"),
    ("none", SOFT, "no automatic trigger \u2014 relies entirely on", "manualOverrideAvailable below"),
]
for (name, col, l1, l2), x in zip(policies, cols3):
    rrect(x, pol_y, col_w3, 150, rx=10, stroke=col, sw=2.4, fill="#FFFFFF")
    text(x+20, pol_y+34, name, size=15, weight=700, fill=col, family="Consolas, Menlo, monospace")
    text(x+20, pol_y+62, l1, size=11.5, fill=MUTED)
    text(x+20, pol_y+80, l2, size=11.5, fill=MUTED)

mid_x = cols3[1] + col_w3/2
text(mid_x, pol_y+128, "SimulationPolicy.automaticMode", size=11, weight=700, fill=BLUE, anchor="middle", family="Consolas, Menlo, monospace")
text(mid_x, pol_y+144, "reuses the severity tiers \u2014 no new scale", size=11, fill=SOFT, style="italic", anchor="middle")

override_y = pol_y + 168
rrect(60, override_y, W-120, 46, rx=10, stroke=GREEN, sw=2, fill="#FFFFFF")
text(84, override_y+29, "manualOverrideAvailable : true \u2014 always, regardless of automaticMode (not a fourth \u201chybrid\u201d mode)", size=12.5, weight=700, fill=GREEN, family="Consolas, Menlo, monospace")

ex_y = override_y + 76
rrect(60, ex_y, W-120, 130, rx=10, stroke=NAVY, sw=2, fill="#FFFFFF")
text(84, ex_y+30, "example: Assembly \u201cReactor Feed\u201d, SimulationPolicy.automaticMode = risk-based, riskThreshold = Tier 1", size=13, weight=700, fill=INK)
text(84, ex_y+58, "\u2022 setpoint nudge within normal band \u2192 predicted worst-case stays Tier 3 \u2192 not simulated, applied directly", size=12, fill=MUTED)
text(84, ex_y+80, "\u2022 setpoint change approaching an Interlock's trip point \u2192 predicted worst-case reaches Tier 1 \u2192", size=12, fill=MUTED)
text(84, ex_y+100, "  simulation runs automatically, operator sees scenarios before confirming", size=12, fill=MUTED)

text(58, ex_y+160, "Priority 1/2 alarms (Sub-model 10) are always simulated \u2014 actionable + high severity already implies the threshold is met", size=12, fill=MUTED, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p3_y + p3_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=SOFT, sw=1.8, marker_end="tri-gray")
text(118, ly2+5, "procedural (ARP) contribution", size=13, fill=INK)
line(400, ly2, 446, ly2, stroke=BLUE, sw=1.8, marker_end="tri-blue")
text(458, ly2+5, "simulated (Digital Twin) contribution", size=13, fill=INK)
line(800, ly2, 846, ly2, stroke=NAVY, sw=1.8, marker_start="diamond-navy")
text(858, ly2+5, "composition (has 0..*)", size=13, fill=INK)

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

with open("./lunex-scenario-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
