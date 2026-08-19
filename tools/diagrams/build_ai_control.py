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
  <marker id="tri-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{RED}"/>
  </marker>
  <marker id="tri-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{GREEN}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 16", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Closed-Loop AI Control", size=26, weight=600, fill=INK)
text(60, 110, "an AI model that adjusts the process daily, treated as an Assembly \u2014 almost nothing here is new", size=13, fill=SOFT)

# ============================================================
# Panel 1: AIControlUnit — a Control Unit subclass, in an Assembly
# ============================================================
p1_y = 145
p1_h = 330
rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "AIControlUnit \u2014 a Control Unit Subclass, Not a New Branch", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "sits in a Point-to-Point or Star Assembly (Sub-model 3) exactly like a PLC would", size=12.5, fill=SOFT)

cu_x, cu_y, cu_w, cu_h = 90, p1_y+100, 220, 56
rrect(cu_x, cu_y, cu_w, cu_h, stroke=NAVY, sw=2, rx=8)
text(cu_x+cu_w/2, cu_y+24, "Control Unit", size=13.5, weight=700, fill=NAVY, anchor="middle")
text(cu_x+cu_w/2, cu_y+42, "extends Device (Sub-model 1)", size=10, fill=SOFT, anchor="middle", style="italic")

ai_x, ai_y, ai_w, ai_h = 90, p1_y+195, 220, 60
rrect(ai_x, ai_y, ai_w, ai_h, stroke=BLUE, sw=2.4, rx=8)
text(ai_x+ai_w/2, ai_y+26, "AIControlUnit", size=14.5, weight=700, fill=BLUE, anchor="middle")
text(ai_x+ai_w/2, ai_y+46, "extends Control Unit", size=10.5, fill=SOFT, anchor="middle", style="italic")
path(f"M {ai_x+ai_w/2} {ai_y} L {cu_x+cu_w/2} {cu_y+cu_h}", stroke=NAVY, sw=2, marker_end="tri-hollow")

at_x, at_y, at_w, at_h = 400, p1_y+100, 560, 190
rrect(at_x, at_y, at_w, at_h, stroke=NAVY, sw=2, rx=8)
aiattrs = [
    "+ objective : string",
    "+ operatingBounds : {parameter, min, max}[]",
    "+ target : PhysicalDevice | DigitalTwin",
    "+ state : State  (Sub-model 4)",
    "+ disabledBy : OperatorRef | InterlockRef | null",
    "+ lastAction : {setpoint, timestamp, withinBounds}",
]
ay = at_y+30
for a in aiattrs:
    text(at_x+18, ay, a, size=12, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 26

seq_x0 = 1050
seq_y = p1_y+220
seq = ["S", "AI", "SC", "A"]
seq_col = {"S": GREEN, "AI": BLUE, "SC": BLUE, "A": GREEN}
step = 130
for i, s in enumerate(seq):
    x = seq_x0 + i*step
    mini_box(x, seq_y, s, seq_col[s], w=64 if s=="AI" else 48, h=36)
    if i > 0:
        line(seq_x0+(i-1)*step+34, seq_y, x-(34 if s!="AI" else 40), seq_y, stroke=NAVY, sw=1.8, marker_end="tri-navy")
text(seq_x0+1.5*step, seq_y-40, "an ordinary Point-to-Point Assembly", size=11.5, fill=SOFT, style="italic", anchor="middle")
text(seq_x0+1.5*step, seq_y+45, "\u2014 the AI just occupies the CU slot", size=11.5, fill=SOFT, style="italic", anchor="middle")

text(58, p1_y+300, "no new topology, no new hierarchy level \u2014 an AIControlUnit is deployed exactly like any other Control Unit", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 2: On/Off — the real Sub-model 4 machine, transplanted (not reinvented)
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 1050
rrect(30, p2_y, W-60, p2_h, stroke=BLUE, sw=2.2)
text(58, p2_y+38, "On / Off \u2014 the Real State Machine, Not a Redrawn One", size=20, weight=700, fill=BLUE)
text(58, p2_y+60, "an Interlock forces exactly the Sub-model 4 transition it corresponds to \u2014 the target depends on where the AI currently is", size=12.5, fill=SOFT)

with open("state_machine_fragment.svg", encoding="utf-8") as f:
    fragment16 = f.read()
S16, TX16, TY16 = 0.62, 90, p2_y+95
parts.append(f'<g transform="translate({TX16},{TY16}) scale({S16})">')
parts.append(fragment16)

INHIBIT_COL16 = GREEN
LOCK_COL16 = RED

def hl16(d_attr, col):
    parts.append(f'<path d="{d_attr}" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round" opacity="0.55"/>')

# inhibit target: reachable from Standby and On
hl16("M955.5 956.4 Q561.0 1038.8 216.5 868.0", INHIBIT_COL16)
hl16("M150.0 800.0 Q150.0 720.0 150.0 642.0", INHIBIT_COL16)
hl16("M721.3 565.1 Q612.5 610.0 510.7 652.0", INHIBIT_COL16)
hl16("M368.6 655.2 Q302.5 640.0 203.7 617.3", INHIBIT_COL16)

# lock target: reachable from Standby and Inhibited (via Disabling) — and directly from Off
hl16("M732.4 515.8 Q626.7 433.6 522.4 398.0", LOCK_COL16)
hl16("M178.3 570.9 Q275.4 454.1 402.8 398.0", LOCK_COL16)
hl16("M491.2 350.9 Q612.5 270.0 730.9 191.0", LOCK_COL16)
hl16("M715.8 177.0 Q612.5 200.0 540.1 216.1", LOCK_COL16)
hl16("M370.3 214.2 Q312.5 200.0 221.7 177.7", LOCK_COL16)

parts.append('</g>')

diagram_bottom16 = TY16 + 1000*S16

note_y16 = diagram_bottom16 + 40
rrect(60, note_y16, W-120, 150, rx=10, stroke=NAVY, sw=2, fill="#FFFFFF")
text(84, note_y16+30, "the Off case \u2014 corrected here", size=14, weight=700, fill=INK)
text(84, note_y16+54, "Inhibited is unreachable from Off (Sub-model 4 has no such edge). So while the AI is Off, an", size=12.5, fill=MUTED)
text(84, note_y16+74, "inhibit-type Interlock cannot target Inhibited \u2014 it targets Locked instead, via the same Off \u2192", size=12.5, fill=MUTED)
text(84, note_y16+94, "Locking \u2192 Locked edge lockType: lock already uses. Off never silently blocks Enabling and waits;", size=12.5, fill=MUTED)
text(84, note_y16+114, "it actively locks out \u2014 this rule applies to every object with an Interlock, not only AIControlUnit.", size=12.5, fill=MUTED)

leg16_y = note_y16 + 190
line(60, leg16_y, 106, leg16_y, stroke=GREEN, sw=8)
text(118, leg16_y+5, "leads to Inhibited (from Standby or On)", size=13, fill=INK)
line(500, leg16_y, 546, leg16_y, stroke=RED, sw=8)
text(558, leg16_y+5, "leads to Locked (from Standby, Inhibited \u2014 or directly from Off)", size=13, fill=INK)

text(58, leg16_y+45, "same highlighted paths as Sub-model 5 \u2014 this diagram is transplanted, not redrawn, so it cannot drift out of sync", size=12, fill=MUTED, style="italic")

with open("./lunex-ai-control-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part2 ok")

# ============================================================
# Panel 3: operatingBounds — required on the real process, optional on the twin
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 430
rrect(30, p3_y, W-60, p3_h, stroke=RED, sw=2.2)
text(58, p3_y+38, "operatingBounds \u2014 Required on the Process, Optional on the Twin", size=20, weight=700, fill=RED)
text(58, p3_y+60, "unbounded is only safe where it can't cause real-world harm \u2014 a structural rule, not a promise", size=12.5, fill=SOFT)

colw4 = (W-60-80)/2
bx1 = 60
bx2 = bx1+colw4+60
by4 = p3_y+105

rrect(bx1, by4, colw4, 130, stroke=RED, sw=2.4, fill="#FFFFFF")
text(bx1+24, by4+32, "target: PhysicalDevice", size=14.5, weight=700, fill=RED)
text(bx1+24, by4+56, "operatingBounds REQUIRED", size=12, weight=700, fill=RED, family="Consolas, Menlo, monospace")
text(bx1+24, by4+82, "a real setpoint, a real consequence \u2014", size=12, fill=MUTED)
text(bx1+24, by4+100, "governance never allows unbounded here", size=12, fill=MUTED)

rrect(bx2, by4, colw4, 130, stroke=GREEN, sw=2.2, fill="#FFFFFF")
text(bx2+24, by4+32, "target: DigitalTwin (Sub-model 7)", size=14.5, weight=700, fill=GREEN)
text(bx2+24, by4+56, "operatingBounds may be empty", size=12, weight=700, fill=GREEN, family="Consolas, Menlo, monospace")
text(bx2+24, by4+82, "the twin absorbs the consequence \u2014", size=12, fill=MUTED)
text(bx2+24, by4+100, "safe to test without limits", size=12, fill=MUTED)

# out-of-bounds flow
fy = by4 + 210
steps4 = [
    ("AI wants setpoint", NAVY, "outside operatingBounds"),
    ("action clamped", RED, "never reaches the Device"),
    ("ImprovementRecommendation", RED, "raised (Sub-model 15)"),
    ("engineer reviews bounds", BLUE, "always \u2014 no exception"),
]
fx0 = 60
fw4 = (W-60-fx0-3*26)/4
for i, (lab, col, sub) in enumerate(steps4):
    x = fx0 + i*(fw4+26)
    rrect(x, fy, fw4, 74, rx=10, stroke=col, sw=2.2, fill="#FFFFFF")
    text(x+fw4/2, fy+30, lab, size=11.5, weight=700, fill=col, anchor="middle")
    text(x+fw4/2, fy+52, sub, size=10, fill=SOFT, anchor="middle", style="italic")
    if i < 3:
        line(x+fw4, fy+37, x+fw4+26, fy+37, stroke=NAVY, sw=1.8, marker_end="tri-navy")

text(58, p3_y+400, "the bound itself may turn out to be wrong \u2014 but that's a human decision (Sub-model 15), never a silent auto-widen", size=12, fill=MUTED, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p3_y + p3_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=NAVY, sw=2, marker_end="tri-hollow")
text(118, ly2+5, "inheritance (extends)", size=13, fill=INK)
line(400, ly2, 446, ly2, stroke=NAVY, sw=1.8, marker_end="tri-navy")
text(458, ly2+5, "mandatory workflow step", size=13, fill=INK)

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

with open("./lunex-ai-control-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
