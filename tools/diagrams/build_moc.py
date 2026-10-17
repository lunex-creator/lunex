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
  <marker id="tri-hollow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">
    <path d="M0 0 L12 6 L0 12 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="1.4"/>
  </marker>
  <marker id="tri-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{BLUE}"/>
  </marker>
  <marker id="tri-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{RED}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 13", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Management of Change (MOC)", size=26, weight=600, fill=INK)
text(60, 110, "One ChangeRequest lifecycle, generalizing five previously ad-hoc approval points across the model", size=13, fill=SOFT)

# ============================================================
# Panel 1: Five ad-hoc approval points -> one ChangeRequest
# ============================================================
p1_y = 145
p1_h = 495
rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "What MOC Generalizes — Five Approval Points, One Object", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "Each of these previously implied its own ad-hoc approval step; all now route through ChangeRequest", size=12.5, fill=SOFT)

sources = [
    ("ImprovementRecommendation.requiresApproval", "Sub-model 20 — Predictive Maintenance"),
    ("Interlock / SIF modification", "Sub-model 6 — Safety"),
    ("Zone / Conduit reconfiguration", "Sub-model 7 — Security Zones & Conduits"),
    ("AccessGrant escalation", "Sub-model 8 — Identity & Access Mgmt"),
    ("Recipe parameter change", "Sub-model 5 — Recipe & Execution"),
]
src_x = 58
src_w = 430
src_h = 56
src_y0 = p1_y + 100
gap_s = 18
cx_target = 1180
cy_target = p1_y + 100 + (len(sources)*(src_h+gap_s)-gap_s)/2

for i, (lab, sub) in enumerate(sources):
    y = src_y0 + i*(src_h+gap_s)
    rrect(src_x, y, src_w, src_h, rx=8, stroke=NAVY, sw=2, fill="#FFFFFF")
    text(src_x+16, y+24, lab, size=12.5, weight=700, fill=INK)
    text(src_x+16, y+42, sub, size=10.5, fill=SOFT, style="italic")
    # connector curving to the target box
    x0 = src_x+src_w
    y0 = y+src_h/2
    x1 = cx_target-160
    y1 = cy_target
    path(f"M{x0} {y0} C{x0+120} {y0} {x1-120} {y1} {x1} {y1}", stroke=GRAY_DASH, sw=1.6, dash="4,4", marker_end="tri-navy")

rrect(cx_target-160, cy_target-55, 320, 110, rx=10, stroke=RED, sw=2.6, fill="#FFFFFF")
text(cx_target, cy_target-20, "ChangeRequest", size=17, weight=700, fill=RED, anchor="middle")
text(cx_target, cy_target+2, "one object, one lifecycle,", size=11.5, fill=MUTED, anchor="middle", style="italic")
text(cx_target, cy_target+20, "one approval model", size=11.5, fill=MUTED, anchor="middle", style="italic")
text(cx_target, cy_target+42, "riskAssessment reuses Sub-model 14's Tier scale", size=10.5, fill=SOFT, anchor="middle", style="italic")

# ============================================================
# Panel 2: ChangeRequest lifecycle state machine
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 330
rrect(30, p2_y, W-60, p2_h, stroke=BLUE, sw=2.2)
text(58, p2_y+38, "ChangeRequest Lifecycle — Its Own State Value Space", size=20, weight=700, fill=BLUE)
text(58, p2_y+60, "A dedicated state machine, the same design move Sub-model 10's SecurityIncident makes for its lifecycle", size=12.5, fill=SOFT)

main_states = ["Draft", "PendingApproval", "Approved", "Implemented", "Verified", "Closed"]
mrow_y = p2_y + 140
mx = 70
mw = 205
mgap = 24
for i, st in enumerate(main_states):
    x = mx + i*(mw+mgap)
    col = GREEN if st == "Closed" else NAVY
    rrect(x, mrow_y-20, mw, 40, rx=20, stroke=col, sw=2.2, fill="#FFFFFF")
    text(x+mw/2, mrow_y+6, st, size=12.5, weight=700, fill=col, anchor="middle")
    if i < len(main_states)-1:
        line(x+mw, mrow_y, x+mw+mgap, mrow_y, stroke=NAVY, sw=2, marker_end="tri-navy")

# Rejected branch from PendingApproval
rej_x = mx + 1*(mw+mgap)
rej_y = mrow_y + 95
rrect(rej_x, rej_y-20, mw, 40, rx=20, stroke=RED, sw=2.2, fill="#FFFFFF")
text(rej_x+mw/2, rej_y+6, "Rejected", size=12.5, weight=700, fill=RED, anchor="middle")
path(f"M{rej_x+mw/2} {mrow_y+20} L{rej_x+mw/2} {rej_y-20}", stroke=RED, sw=2, marker_end="tri-red")
text(rej_x+mw/2+14, mrow_y+56, "approval declined", size=11, fill=SOFT, style="italic")
# Rejected -> Closed
close_x = mx + 5*(mw+mgap)
path(f"M{rej_x+mw} {rej_y} C{rej_x+mw+220} {rej_y} {close_x-40} {rej_y} {close_x+mw/2} {mrow_y+20}",
     stroke=RED, sw=1.8, dash="4,4", marker_end="tri-red")

text(58, p2_y+p2_h-30, "requiredApprovals : RoleRef[] names who must approve before Draft can leave PendingApproval; approvals : Approval[] records each decision", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 3: ChangeRequest / Approval schema + VersionRecord -> Historian
# ============================================================
p3_y = p2_y + p2_h + 50
p3_h = 545
rrect(30, p3_y, W-60, p3_h, stroke=BLUE, sw=2.2)
text(58, p3_y+38, "Schema — ChangeRequest, Approval, ChangePolicy, and the VersionRecord It Produces", size=20, weight=700, fill=BLUE)
text(58, p3_y+60, "ChangePolicy is governance authored once; ChangeRequest is governance applied once — it can only raise the approval bar, never lower it", size=12.5, fill=SOFT)

bx, by, bw, bh = 58, p3_y+95, 440, 270
rrect(bx, by, bw, bh, stroke=RED, sw=2.4, rx=8)
text(bx+16, by+26, "ChangeRequest", size=14.5, weight=700, fill=RED)
text(bx+16, by+44, "extends LunexObject", size=10.5, fill=SOFT, style="italic")
cr_attrs = [
    "+ subject : ObjectRef",
    "+ changeType : parameter|configuration|",
    "    procedural|physical",
    "+ proposedBy : IdentityRef",
    "+ description : string",
    "+ riskAssessment : Tier  (Sub-model 14)",
    "+ requiredApprovals : RoleRef[]",
    "+ approvals : Approval[]",
    "+ state : Draft|PendingApproval|Approved|",
    "    Rejected|Implemented|Verified|Closed",
]
ay = by+66
for a in cr_attrs:
    text(bx+16, ay, a, size=10.8, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 20.5

mx2, my2, mw2, mh2 = 598, p3_y+95, 400, 130
rrect(mx2, my2, mw2, mh2, stroke=NAVY, sw=2, rx=8)
text(mx2+16, my2+26, "Approval", size=14.5, weight=700, fill=NAVY)
ap_attrs = [
    "+ role : RoleRef",
    "+ approver : IdentityRef",
    "+ decision : approve|reject",
    "+ comment : string  (optional)",
    "+ timestamp : datetime",
]
ay = my2+50
for a in ap_attrs:
    text(mx2+16, ay, a, size=10.8, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 17.5

vx, vy, vw, vh = 598, p3_y+260, 400, 105
rrect(vx, vy, vw, vh, stroke=GREEN, sw=2, rx=8)
text(vx+16, vy+26, "VersionRecord", size=14.5, weight=700, fill=GREEN)
v_attrs = [
    "+ subject, changeRequest : ref",
    "+ baselineBefore / baselineAfter : snapshot",
    "+ createdAt : datetime",
]
ay = vy+50
for a in v_attrs:
    text(vx+16, ay, a, size=10.8, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 17.5

line(bx+bw, my2+45, mx2, my2+45, stroke=NAVY, sw=1.8, marker_end="tri-navy")
text((bx+bw+mx2)/2, my2+33, "approvals[]", size=10.5, fill=SOFT, anchor="middle", style="italic")

line(mx2+30, my2+mh2, vx+30, vy, stroke=GREEN, sw=1.8, marker_end="tri-navy")

hx, hy, hw, hh = 1060, p3_y+95, 440, 60
rrect(hx, hy, hw, hh, rx=30, stroke=GREEN, sw=2.2, dash="5,4", fill="#FFFFFF")
text(hx+hw/2, hy+36, "Historian  (Sub-model 19) — append-only store", size=13, weight=700, fill=GREEN, anchor="middle")
path(f"M{vx+vw} {vy+vh/2} L{(vx+vw+hx)/2} {vy+vh/2} L{(vx+vw+hx)/2} {hy+hh/2} L{hx} {hy+hh/2}", stroke=GREEN, sw=2, dash="4,4", marker_end="tri-navy")
text(hx+16, hy+hh+24, "closing a ChangeRequest appends one VersionRecord", size=11.5, fill=MUTED, style="italic")
text(hx+16, hy+hh+42, "alongside ordinary HistorianRecords", size=11.5, fill=MUTED, style="italic")

px, py, pw, ph = 1060, p3_y+215, 440, 165
rrect(px, py, pw, ph, stroke=NAVY, sw=2.2, rx=8)
text(px+16, py+26, "ChangePolicy", size=14.5, weight=700, fill=NAVY)
text(px+16, py+44, "extends LunexObject", size=10.5, fill=SOFT, style="italic")
pol_attrs = [
    "+ appliesTo : ClassRef | LunexObjectRef",
    "+ changeTypes : [...]  (empty = all)",
    "+ requiredTier : Tier | null  (Sub-model 14)",
    "+ requiredApprovals : RoleRef[]",
    "+ minApprovals : integer  (default 1)",
]
ay = py+66
for a in pol_attrs:
    text(px+16, ay, a, size=10.8, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 19.5

# route the Policy -> ChangeRequest link through the clear corridor below
# the schema boxes, well under VersionRecord/Approval, so it never crosses them
corridor_y = p3_y + 440
path(f"M{px+pw-40} {py+ph} C{px+pw-40} {corridor_y+20} {bx+bw-60} {corridor_y+20} {bx+bw-60} {by+bh}",
     stroke=NAVY, sw=1.8, dash="4,4", marker_end="tri-navy")
text((bx+bw+px)/2, corridor_y+36, "ChangePolicy resolves requiredApprovals / riskAssessment floor onto a matching ChangeRequest", size=11, fill=SOFT, anchor="middle", style="italic")

text(58, corridor_y+62, "LunexObject.owner (Sub-model 1) and ChangePolicy.appliesTo both resolve through the same Sub-model 8 Role vocabulary.", size=11.3, fill=MUTED, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p3_y + p3_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=NAVY, sw=2, marker_end="tri-navy")
text(118, ly2+5, "state transition / schema reference", size=13, fill=INK)
line(400, ly2, 446, ly2, stroke=GRAY_DASH, sw=1.6, dash="4,4", marker_end="tri-navy")
text(458, ly2+5, "routes into ChangeRequest", size=13, fill=INK)
line(760, ly2, 806, ly2, stroke=RED, sw=2, marker_end="tri-red")
text(818, ly2+5, "rejection path", size=13, fill=INK)

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

with open("./lunex-moc-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
