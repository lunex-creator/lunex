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
  <marker id="tri-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{GREEN}"/>
  </marker>
  <marker id="tri-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{GRAY_DASH}"/>
  </marker>
  <marker id="tri-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{RED}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 15", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Predictive Maintenance & Improvement", size=26, weight=600, fill=INK)
text(60, 110, "a third guidance source, built on the Historian (Sub-model 14) \u2014 trend-based, not real-time or procedural", size=13, fill=SOFT)

# ============================================================
# Panel 1: Three sources now, not two
# ============================================================
p1_y = 145
p1_h = 300
rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "GuidanceRecommendation.source \u2014 a Third Value", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "same field as Sub-model 12, no new schema \u2014 procedural | simulated | now also predictive", size=12.5, fill=SOFT)

colw3 = (W-60-80-40)/3
xs3 = [60, 60+colw3+20, 60+2*(colw3+20)]
srcs = [
    ("procedural", SOFT, "ARP (Sub-model 11)", "static, engineer-written"),
    ("simulated", BLUE, "Digital Twin (Sub-model 7)", "live, current state"),
    ("predictive", GREEN, "Historian (Sub-model 14)", "trend-based, forward-looking"),
]
for (name, col, sub, desc), x in zip(srcs, xs3):
    rrect(x, p1_y+100, colw3, 150, rx=10, stroke=col, sw=2.4, fill="#FFFFFF")
    text(x+18, p1_y+134, name, size=15, weight=700, fill=col, family="Consolas, Menlo, monospace")
    text(x+18, p1_y+158, sub, size=11.5, fill=SOFT, style="italic")
    text(x+18, p1_y+186, desc, size=12, fill=MUTED)

text(58, p1_y+275, "one Operator Guidance Panel (Sub-model 12) still shows all three \u2014 the source label tells the operator which kind of claim it is", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 2: PredictedEvent — flows into the Alarm system
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 430
rrect(30, p2_y, W-60, p2_h, stroke=GREEN, sw=2.2)
text(58, p2_y+38, "PredictedEvent \u2014 Joins the Alarm System, Doesn't Sit Beside It", size=20, weight=700, fill=GREEN)
text(58, p2_y+60, "one situational-awareness picture (Sub-model 13) \u2014 not a second screen the operator has to remember to check", size=12.5, fill=SOFT)

pe_x, pe_y, pe_w, pe_h = 60, p2_y+100, 480, 260
rrect(pe_x, pe_y, pe_w, pe_h, stroke=NAVY, sw=2, rx=8)
text(pe_x+18, pe_y+28, "PredictedEvent", size=13.5, weight=700, fill=GREEN)
text(pe_x+18, pe_y+46, "extends LunexObject (Sub-model 1)", size=10, fill=SOFT, style="italic")
peattrs = [
    "+ id : string",
    "+ subject : DeviceRef",
    "+ predictedCondition : string",
    "+ predictedWindow : {from, to}",
    "+ confidence : 0\u20131",
    "+ basis : string  (Historian pattern)",
    "+ state : Open | Confirmed |",
    "  Dismissed | Expired",
]
ay = pe_y+70
for a in peattrs:
    text(pe_x+18, ay, a, size=12, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 24

ar_x, ar_y, ar_w, ar_h = 620, p2_y+100, 460, 210
rrect(ar_x, ar_y, ar_w, ar_h, stroke=RED, sw=2.4, rx=8)
text(ar_x+18, ar_y+28, "Alarm", size=13.5, weight=700, fill=RED, family="Consolas, Menlo, monospace")
aattrs = [
    "+ origin : real-time | predictive",
    "+ condition : ref \u2192 PredictedEvent",
    "+ actionable : true  (maintenance can act)",
    "+ priority : from severity \u00d7 actionable",
    "  (Sub-model 10, unchanged)",
]
ay = ar_y+54
for a in aattrs:
    text(ar_x+18, ay, a, size=12, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 24

line(pe_x+pe_w, pe_y+pe_h/2, ar_x, ar_y+ar_h/2, stroke=GREEN, sw=2, marker_end="tri-green")
text((pe_x+pe_w+ar_x)/2, pe_y+pe_h/2-14, "raises", size=12, fill=GREEN, weight=700, style="italic", anchor="middle")

badge_x, badge_y = 1195, p2_y+150
rrect(badge_x-90, badge_y-20, 180, 40, rx=20, stroke=GREEN, sw=2, fill="#FFFFFF")
text(badge_x, badge_y+5, "PREDICTIVE", size=12.5, weight=700, fill=GREEN, anchor="middle")
text(badge_x, badge_y+38, "visible tag, so the operator", size=11, fill=SOFT, anchor="middle", style="italic")
text(badge_x, badge_y+56, "never confuses \u201cwill\u201d with \u201cis\u201d", size=11, fill=SOFT, anchor="middle", style="italic")

text(58, p2_y+405, "example: bearing wear predicted in 3\u20136 weeks \u2192 Priority 2 alarm, tagged predictive, same screen as real-time alarms", size=12, fill=MUTED, style="italic")

with open("./lunex-predictive-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part2 ok")

# ============================================================
# Panel 3: ImprovementRecommendation — always requires approval
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 430
rrect(30, p3_y, W-60, p3_h, stroke=RED, sw=2.2)
text(58, p3_y+38, "ImprovementRecommendation \u2014 Always Requires Approval", size=20, weight=700, fill=RED)
text(58, p3_y+60, "not a policy choice like Sub-model 12/14 \u2014 a fixed rule, with no false-case, by design", size=12.5, fill=SOFT)

ir_x, ir_y, ir_w, ir_h = 60, p3_y+100, 560, 270
rrect(ir_x, ir_y, ir_w, ir_h, stroke=NAVY, sw=2, rx=8)
text(ir_x+18, ir_y+28, "ImprovementRecommendation", size=13.5, weight=700, fill=RED)
text(ir_x+18, ir_y+46, "extends LunexObject (Sub-model 1)", size=10, fill=SOFT, style="italic")
irattrs = [
    "+ id : string",
    "+ subject : AssemblyRef | LunexObjectRef",
    "+ pattern : string  (what the Historian shows)",
    "+ suggestedChange : string",
    "+ evidenceBasis : string",
    "+ requiresApproval : true  \u2014 always",
    "+ state : Proposed | UnderReview |",
    "  Approved | Rejected | Applied",
]
ay = ir_y+70
for a in irattrs:
    col = RED if "always" in a else MUTED
    text(ir_x+18, ay, a, size=12, fill=col, family="Consolas, Menlo, monospace", weight=700 if col==RED else 400)
    ay += 24

fx0 = 700
fy0 = p3_y+130
steps = [
    ("Historian pattern", NAVY, "e.g. loop oscillating 3 months"),
    ("ImprovementRecommendation", RED, "suggested change + evidence"),
    ("Engineer review", BLUE, "always, no exception"),
    ("Applied \u2014 or not", GREEN, "engineer's call, not the AI's"),
]
fw = (W-60-fx0-40)
step_w = fw/4 - 20
for i, (lab, col, sub) in enumerate(steps):
    x = fx0 + i*(step_w+26)
    rrect(x, fy0, step_w, 70, rx=10, stroke=col, sw=2.2, fill="#FFFFFF")
    text(x+step_w/2, fy0+28, lab, size=11.5, weight=700, fill=col, anchor="middle")
    text(x+step_w/2, fy0+48, sub, size=9.5, fill=SOFT, anchor="middle", style="italic")
    if i < 3:
        line(x+step_w, fy0+35, x+step_w+26, fy0+35, stroke=NAVY, sw=1.8, marker_end="tri-navy")

text(fx0, fy0+110, "no shortcut from step 2 to step 4 \u2014 not even at confidence = 1.0", size=12, fill=RED, weight=600, style="italic")
text(fx0, fy0+130, "contrast with Sub-model 12: a Scenario can be shown to an operator directly; an", size=11.5, fill=MUTED)
text(fx0, fy0+148, "ImprovementRecommendation changes how the plant runs \u2014 a materially bigger decision", size=11.5, fill=MUTED)

text(58, p3_y+400, "the Historian finds the pattern and the AI drafts the suggestion \u2014 neither one ever touches the configuration", size=12, fill=MUTED, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p3_y + p3_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=GREEN, sw=2, marker_end="tri-green")
text(118, ly2+5, "raises (PredictedEvent \u2192 Alarm)", size=13, fill=INK)
line(430, ly2, 476, ly2, stroke=NAVY, sw=1.8, marker_end="tri-navy")
text(488, ly2+5, "mandatory workflow step", size=13, fill=INK)

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

with open("./lunex-predictive-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
