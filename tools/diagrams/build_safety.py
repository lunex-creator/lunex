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
  <marker id="tri-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{RED}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 5", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Safety", size=26, weight=600, fill=INK)
text(60, 110, "Cross-cutting safety properties and mechanisms on top of Sub-models 1\u20134 \u2014 no new class tree", size=13, fill=SOFT)

# ============================================================
# Panel 1: Interlock — a first-class LunexObject
# ============================================================
p1_y = 145
p1_h = 330
rrect(30, p1_y, W-60, p1_h, stroke=RED, sw=2.2)
text(58, p1_y+38, "Interlock \u2014 a First-Class LunexObject", size=20, weight=700, fill=RED)
text(58, p1_y+60, "not a property list \u2014 its own class, sibling to Device and Component", size=12.5, fill=SOFT)

lo_x, lo_y, lo_w, lo_h = 90, p1_y+100, 220, 50
rrect(lo_x, lo_y, lo_w, lo_h, stroke=NAVY, sw=2, rx=8)
text(lo_x+lo_w/2, lo_y+22, "LunexObject", size=13.5, weight=700, fill=NAVY, anchor="middle")
text(lo_x+lo_w/2, lo_y+40, "\u00ababstract\u00bb", size=10.5, fill=SOFT, anchor="middle", style="italic")

il_x, il_y, il_w, il_h = 90, p1_y+195, 220, 60
rrect(il_x, il_y, il_w, il_h, stroke=RED, sw=2.4, rx=8)
text(il_x+il_w/2, il_y+26, "Interlock", size=15, weight=700, fill=RED, anchor="middle")
text(il_x+il_w/2, il_y+46, "extends LunexObject", size=11, fill=SOFT, anchor="middle", style="italic")
line(lo_x+lo_w/2, lo_y+lo_h, il_x+il_w/2, il_y, stroke=NAVY, sw=2, marker_end="tri-hollow")

text(il_x, il_y+il_h+26, "peer of Device and Component \u2014", size=11.5, fill=SOFT, style="italic")
text(il_x, il_y+il_h+44, "not a subtype of either (Sub-model 1)", size=11.5, fill=SOFT, style="italic")

at_x, at_y, at_w, at_h = 420, p1_y+100, 520, 200
rrect(at_x, at_y, at_w, at_h, stroke=NAVY, sw=2, rx=8)
attrs = [
    "+ id : string",
    "+ condition : DeviceRef",
    "+ action : force | block",
    "+ target : DeviceRef",
    "+ lockType : inhibit | lock",
    "+ state : State  (Sub-model 4)",
    "+ proofTestHistory : ProofTest[]",
]
ay = at_y+28
for a in attrs:
    text(at_x+18, ay, a, size=12.5, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 24

note_x = at_x + at_w + 40
text(note_x, p1_y+118, "why a full object, not a property:", size=12.5, fill=INK, weight=700)
text(note_x, p1_y+140, "SIL requires periodic proof-testing \u2014", size=12, fill=MUTED)
text(note_x, p1_y+158, "a property can't carry its own test", size=12, fill=MUTED)
text(note_x, p1_y+176, "history, id or lifecycle. One Interlock", size=12, fill=MUTED)
text(note_x, p1_y+194, "can also govern more than one target.", size=12, fill=MUTED)

# ============================================================
# Panel 2: Safety Instrumented Function — always its own Assembly
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 350
rrect(30, p2_y, W-60, p2_h, stroke=NAVY, sw=2.2)
text(58, p2_y+38, "Safety Instrumented Function (SIF) \u2014 Always Its Own Assembly", size=20, weight=700, fill=NAVY)
text(58, p2_y+60, "physically independent from the process Assembly \u2014 never mixed (Sub-model 3)", size=12.5, fill=SOFT)

col_w = (W-60-100-60)/2
bpcs_x = 60
sif_x = bpcs_x + col_w + 100

by = p2_y+110
rrect(bpcs_x, by, col_w, 172, stroke=SOFT, sw=1.8, dash="5,4")
text(bpcs_x+20, by+28, "BPCS Assembly", size=15, weight=700, fill=SOFT)
text(bpcs_x+20, by+46, "normal process control", size=11.5, fill=SOFT, style="italic")
bseq = ["S", "T", "CU", "SC", "A"]
bx0 = bpcs_x + 55
bstep = (col_w-110)/4
bpts = [(bx0+i*bstep, by+100) for i in range(5)]
bcol = {"S": GREEN, "T": BLUE, "CU": SOFT, "SC": BLUE, "A": GREEN}
for (px, py) in bpts:
    pass
for (px, py), lab in zip(bpts, bseq):
    mini_box(px, py, lab, bcol[lab], w=42, h=30)
for i in range(4):
    line(bpts[i][0]+22, by+100, bpts[i+1][0]-22, by+100, stroke=SOFT, sw=1.6, marker_end="tri-navy")

rrect(sif_x, by, col_w, 172, stroke=RED, sw=2.4)
text(sif_x+20, by+28, "SIF Assembly", size=15, weight=700, fill=RED)
text(sif_x+20, by+46, "independent: true \u00b7 SIL 2", size=11.5, fill=RED, weight=700, style="italic")
sseq = [("S", GREEN, "initiator", "2oo3"), ("SIS", RED, "logic solver", "1oo1"), ("A", GREEN, "final element", "1oo2")]
sx0 = sif_x + 70
sstep = (col_w-140)/2
spts = [(sx0+i*sstep, by+100) for i in range(3)]
for (px, py), (lab, col, role, voting) in zip(spts, sseq):
    mini_box(px, py, lab, col, w=56, h=36)
    text(px, py+34, role, size=10, fill=SOFT, anchor="middle", style="italic")
    text(px, py+50, "votingArchitecture: " + voting, size=9, fill=RED, anchor="middle", weight=700, family="Consolas, Menlo, monospace")
for i in range(2):
    line(spts[i][0]+28, by+100, spts[i+1][0]-28, by+100, stroke=RED, sw=1.8, marker_end="tri-red")

# forbidden-share indicator between the two assemblies
mid_x = (bpcs_x+col_w + sif_x)/2
mid_y = by+75
parts.append(f'<circle cx="{mid_x}" cy="{mid_y}" r="20" fill="#FFFFFF" stroke="{RED}" stroke-width="2.6"/>')
line(mid_x-12, mid_y-12, mid_x+12, mid_y+12, stroke=RED, sw=2.6)
text(mid_x, mid_y+42, "no shared", size=11, fill=RED, weight=700, anchor="middle")
text(mid_x, mid_y+58, "Control Unit", size=11, fill=RED, weight=700, anchor="middle")

text(58, p2_y+308, "SIL is a property of the SIF Assembly as a whole, not of a single Device inside it \u2014 votingArchitecture (MooN, IEC 61508) is mandatory per layer, unlike physicalRef (Sub-model 1)", size=12.5, fill=MUTED, style="italic")

# ============================================================
# Panel 3: Interlock Paths — overlaid on the real Sub-model 4 machine
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 1040
rrect(30, p3_y, W-60, p3_h, stroke=RED, sw=2.2)
text(58, p3_y+38, "Interlock Paths on the Sub-model 4 State Machine", size=20, weight=700, fill=RED)
text(58, p3_y+60, "only two lockTypes exist \u2014 each one is an existing transition path, never an arbitrary jump", size=12.5, fill=SOFT)

with open("state_machine_fragment.svg", encoding="utf-8") as f:
    fragment3 = f.read()
S3, TX3, TY3 = 0.72, 70, p3_y+95
parts.append(f'<g transform="translate({TX3},{TY3}) scale({S3})">')
parts.append(fragment3)

# highlight overlays, drawn in the SAME coordinate space as the fragment for exact alignment
INHIBIT_COL = "#2E7D4F"
LOCK_COL = "#B3402F"
HW = 9  # highlight stroke width, pre-scale

def hl(d_attr, col):
    parts.append(f'<path d="{d_attr}" fill="none" stroke="{col}" stroke-width="{HW}" stroke-linecap="round" opacity="0.55"/>')

# inhibit: On -> Emergency Stopping -> Inhibited, and Standby -> Inhibiting -> Inhibited
hl("M955.5 956.4 Q561.0 1038.8 216.5 868.0", INHIBIT_COL)
hl("M150.0 800.0 Q150.0 720.0 150.0 642.0", INHIBIT_COL)
hl("M721.3 565.1 Q612.5 610.0 510.7 652.0", INHIBIT_COL)
hl("M368.6 655.2 Q302.5 640.0 203.7 617.3", INHIBIT_COL)

# lock: Standby/Inhibited -> Disabling -> Off -> Locking -> Locked
hl("M732.4 515.8 Q626.7 433.6 522.4 398.0", LOCK_COL)
hl("M178.3 570.9 Q275.4 454.1 402.8 398.0", LOCK_COL)
hl("M491.2 350.9 Q612.5 270.0 730.9 191.0", LOCK_COL)
hl("M715.8 177.0 Q612.5 200.0 540.1 216.1", LOCK_COL)
hl("M370.3 214.2 Q312.5 200.0 221.7 177.7", LOCK_COL)

parts.append('</g>')

diagram_bottom = TY3 + 1000*S3

# in-panel legend for the two path colors
lg_y = diagram_bottom + 30
line(70, lg_y, 130, lg_y, stroke=INHIBIT_COL, sw=8, dash=None)
text(144, lg_y+5, "lockType: inhibit \u2014 path to Inhibited", size=13, fill=INK, weight=600)
line(70, lg_y+30, 130, lg_y+30, stroke=LOCK_COL, sw=8)
text(144, lg_y+35, "lockType: lock \u2014 path to Locked (continues past Inhibited)", size=13, fill=INK, weight=600)

note_y2 = lg_y + 70
text(58, note_y2, "from On, both lockTypes always route through Emergency Stopping (Category 0) \u2014", size=12.5, fill=MUTED, style="italic")
text(58, note_y2+20, "Quick/Controlled Stopping return to Standby and are not safety-relevant paths, so an", size=12.5, fill=MUTED, style="italic")
text(58, note_y2+40, "interlock never uses them. lock reuses the inhibit path from On, then continues to Locked.", size=12.5, fill=MUTED, style="italic")
text(58, note_y2+64, "from Off, Inhibited is unreachable \u2014 an inhibit-type interlock uses the lock path's final leg", size=12.5, fill=MUTED, style="italic")
text(58, note_y2+84, "(Off \u2192 Locking \u2192 Locked) directly, rather than blocking Enabling and waiting (Sub-model 16)", size=12.5, fill=MUTED, style="italic")

# ============================================================
# Panel 4: Stop categories — confirming Sub-model 4 against IEC 60204-1
# ============================================================
p4_y = p3_y + p3_h + 50
p4_h = 190
rrect(30, p4_y, W-60, p4_h, stroke=NAVY, sw=2.2)
text(58, p4_y+38, "Stop Categories \u2014 Confirmed Against IEC 60204-1", size=20, weight=700, fill=NAVY)
text(58, p4_y+60, "the three stop states from Sub-model 4 map directly \u2014 no change needed", size=12.5, fill=SOFT)

rows = [
    ("Controlled Stopping", "Category 2", "power remains available"),
    ("Quick Stopping", "Category 1", "controlled, then power removed"),
    ("Emergency Stopping", "Category 0", "power removed immediately"),
]
rx0 = 58
ry0 = p4_y + 92
col1, col2, col3 = 0, 330, 560
for i, (a, b, c) in enumerate(rows):
    yy = ry0 + i*30
    col = RED if "Emergency" in a else (BLUE if "Quick" in a else NAVY)
    text(rx0+col1, yy, a, size=13, weight=700, fill=col)
    text(rx0+col2, yy, b, size=13, weight=700, fill=col, family="Consolas, Menlo, monospace")
    text(rx0+col3, yy, c, size=12.5, fill=MUTED)

# ============================================================
# Legend
# ============================================================
leg_y = p4_y + p4_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=NAVY, sw=2, marker_end="tri-hollow")
text(118, ly2+5, "inheritance (extends)", size=13, fill=INK)
line(320, ly2, 366, ly2, stroke=NAVY, sw=2, marker_end="tri-navy")
text(378, ly2+5, "signal / reference", size=13, fill=INK)
path(f"M 560 {ly2} L 606 {ly2}", stroke=RED, sw=2, dash="3,3", marker_end="tri-red")
text(618, ly2+5, "forces / blocks a transition", size=13, fill=INK)
parts.append(f'<circle cx="900" cy="{ly2}" r="13" fill="#FFFFFF" stroke="{RED}" stroke-width="2"/>')
line(900-8, ly2-8, 900+8, ly2+8, stroke=RED, sw=2)
text(922, ly2+5, "physical independence required", size=13, fill=INK)

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

with open("./lunex-safety-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
