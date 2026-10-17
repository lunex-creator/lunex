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
    s = (len(s) - len(s.lstrip(' '))) * '\u00a0' + s.lstrip(' ')   # keep leading indentation visible in SVG
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
  <marker id="tri-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{RED}"/>
  </marker>
  <marker id="tri-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{GREEN}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 10", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Security Incident Response", size=26, weight=600, fill=INK)
text(60, 110, "NIST CSF Respond/Recover and IEC 62443-2-1 incident response — a cybersecurity event is not a process alarm, even when the same signal triggers both", size=12.8, fill=SOFT)

# ============================================================
# Panel 1: SecurityIncident vs Alarm — peer, not subtype
# ============================================================
p1_y = 145
p1_h = 460
rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "Peer of Alarm, Not a Subtype — Two Different Questions", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "The same underlying event can raise both, because each answers something the other doesn't", size=12.5, fill=SOFT)

lox, loy, low, loh = 700, p1_y+105, 200, 50
rrect(lox, loy, low, loh, rx=8, stroke=NAVY, sw=2, fill="#FFFFFF")
text(lox+low/2, loy+32, "LunexObject", size=13.5, weight=700, fill=NAVY, anchor="middle")
text(lox+low/2, loy-16, "peers — both extend LunexObject directly, neither is a subclass of the other", size=11.5, fill=SOFT, anchor="middle", style="italic")

ax, ay_, aw, ah = 420, loy+110, 350, 110
rrect(ax, ay_, aw, ah, rx=8, stroke=NAVY, sw=2.2)
text(ax+aw/2, ay_+30, "Alarm", size=16, weight=700, fill=NAVY, anchor="middle")
text(ax+aw/2, ay_+52, "Sub-model 15", size=10.5, fill=SOFT, anchor="middle", style="italic")
text(ax+aw/2, ay_+76, "“does an operator need to act", size=11, fill=MUTED, anchor="middle")
text(ax+aw/2, ay_+94, "on a process condition?”", size=11, fill=MUTED, anchor="middle")

sx, sy, sw_, sh = 830, loy+110, 350, 110
rrect(sx, sy, sw_, sh, rx=8, stroke=RED, sw=2.4)
text(sx+sw_/2, sy+30, "SecurityIncident", size=16, weight=700, fill=RED, anchor="middle")
text(sx+sw_/2, sy+52, "Sub-model 10", size=10.5, fill=SOFT, anchor="middle", style="italic")
text(sx+sw_/2, sy+76, "“is this a cybersecurity event,", size=11, fill=MUTED, anchor="middle")
text(sx+sw_/2, sy+94, "and where are we in containing it?”", size=11, fill=MUTED, anchor="middle")

path(f"M {ax+aw/2} {ay_} L {lox+low*0.3} {loy+loh}", stroke=NAVY, sw=2)
path(f"M {sx+sw_/2} {sy} L {lox+low*0.7} {loy+loh}", stroke=RED, sw=2)

trig_y = sy + sh + 50
rrect(58, trig_y, W-116, 60, rx=8, stroke=GRAY_DASH, sw=1.6, dash="4,4", fill="#FFFFFF")
text(80, trig_y+24, "detectedVia : ZoneRef | ConduitRef | DeviceRef — a Sub-model 7 anomaly or an Identity/AccessGrant violation (Sub-model 8),", size=12, fill=MUTED, style="italic")
text(80, trig_y+44, "which may or may not be the same underlying signal an Alarm (Sub-model 15) was also raised from.", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 2: SecurityIncident lifecycle
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 290
rrect(30, p2_y, W-60, p2_h, stroke=BLUE, sw=2.2)
text(58, p2_y+38, "SecurityIncident.state — Its Own Value Space [NIST CSF Respond/Recover]", size=20, weight=700, fill=BLUE)
text(58, p2_y+60, "A third, distinct kind of question — not a restatement of Alarm.state or the Sub-model 4 object-behavior states", size=12.5, fill=SOFT)

states2 = ["Detected", "Contained", "Eradicated", "Recovered", "Closed"]
triggers = ["detect()\n(automatic)", "contain()", "eradicate()", "recover()", "close()"]
mrow_y = p2_y + 150
mw = 250
mgap = 40
mx = (W - (5*mw + 4*mgap)) / 2
for i, st in enumerate(states2):
    x = mx + i*(mw+mgap)
    col = GREEN if st == "Closed" else NAVY
    rrect(x, mrow_y-22, mw, 44, rx=22, stroke=col, sw=2.2, fill="#FFFFFF")
    text(x+mw/2, mrow_y+6, st, size=13.5, weight=700, fill=col, anchor="middle")
    if i < len(states2)-1:
        line(x+mw, mrow_y, x+mw+mgap, mrow_y, stroke=NAVY, sw=2, marker_end="tri-navy")
        text(x+mw+mgap/2, mrow_y-32, triggers[i+1].split("\n")[0], size=10.5, fill=SOFT, anchor="middle", style="italic", family="Consolas, Menlo, monospace")

text(mx+mw/2, mrow_y-60, "raised automatically — never a manual method call", size=10.5, fill=SOFT, anchor="middle", style="italic")
text(mx+mw/2, mrow_y+50, "isolated: typically a Conduit restriction (Sub-model 7)", size=10.5, fill=MUTED, anchor="middle", style="italic")
text(mx+mw+mgap+mw/2, mrow_y+50, "root cause removed", size=10.5, fill=MUTED, anchor="middle", style="italic")
text(mx+2*(mw+mgap)+mw/2, mrow_y+50, "normal operation restored", size=10.5, fill=MUTED, anchor="middle", style="italic")
text(mx+3*(mw+mgap)+mw/2, mrow_y+50, "always requires a lessons-learned note", size=10.5, fill=MUTED, anchor="middle", style="italic")

text(58, p2_y+p2_h-30, "severity : Tier (0-3) reuses Sub-model 14's scale directly — every risk judgment in LUNEX speaks the same vocabulary", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 3: Schema + relatedChange -> ChangeRequest
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 330
rrect(30, p3_y, W-60, p3_h, stroke=BLUE, sw=2.2)
text(58, p3_y+38, "Schema — SecurityIncident and Its Link to Remediation", size=20, weight=700, fill=BLUE)
text(58, p3_y+60, "SecurityIncident tracks the response workflow; ChangeRequest tracks what was actually changed as a result — never merged into one object", size=12.3, fill=SOFT)

bx, by, bw, bh = 58, p3_y+100, 600, 190
rrect(bx, by, bw, bh, stroke=RED, sw=2.4, rx=8)
text(bx+16, by+28, "SecurityIncident", size=15, weight=700, fill=RED)
text(bx+16, by+46, "extends LunexObject", size=10.5, fill=SOFT, style="italic")
si_attrs = [
    "+ detectedVia : ZoneRef | ConduitRef | DeviceRef",
    "+ severity : Tier (0-3)  (Sub-model 14)",
    "+ relatedChange : ChangeRequestRef | null",
    "+ state : Detected | Contained | Eradicated |",
    "          Recovered | Closed  (own value space)",
]
ay = by+70
for a in si_attrs:
    text(bx+16, ay, a, size=10.8, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 20

crx, cry, crw, crh = 1010, by+bh/2-80, 490, 160
rrect(crx, cry, crw, crh, rx=30, stroke=GREEN, sw=2.2, dash="5,4", fill="#FFFFFF")
text(crx+crw/2, cry+36, "ChangeRequest (Sub-model 13)", size=13, weight=700, fill=GREEN, anchor="middle")
text(crx+crw/2, cry+62, "raised only when remediation changes", size=11, fill=MUTED, anchor="middle")
text(crx+crw/2, cry+80, "plant configuration — not for", size=11, fill=MUTED, anchor="middle")
text(crx+crw/2, cry+98, "containment alone", size=11, fill=MUTED, anchor="middle")
text(crx+crw/2, cry+124, "the same separation MOC draws for a Recipe parameter", size=10.5, fill=SOFT, anchor="middle", style="italic")
text(crx+crw/2, cry+140, "change and the approval that authorized it", size=10.5, fill=SOFT, anchor="middle", style="italic")

line(bx+bw, by+bh/2, crx, cry+crh/2, stroke=GREEN, sw=1.8, dash="4,4", marker_end="tri-green")
text((bx+bw+crx)/2, by+bh/2-12, "relatedChange", size=10.5, fill=SOFT, anchor="middle", style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p3_y + p3_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=NAVY, sw=2, marker_end="tri-navy")
text(118, ly2+5, "lifecycle transition", size=13, fill=INK)
line(360, ly2, 406, ly2, stroke=GREEN, sw=1.8, dash="4,4", marker_end="tri-green")
text(418, ly2+5, "relatedChange reference (optional)", size=13, fill=INK)
rrect(760, ly2-14, 28, 28, rx=6, stroke=RED, sw=2.2, fill="#FFFFFF")
text(802, ly2+5, "security-related (IEC 62443 / NIST CSF)", size=13, fill=INK)

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

with open("./lunex-security-incident-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
