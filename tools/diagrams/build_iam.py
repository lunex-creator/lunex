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
  <marker id="tri-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{BLUE}"/>
  </marker>
  <marker id="diamond-navy" viewBox="0 0 12 12" refX="1" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">
    <path d="M6 0 L12 6 L6 12 L0 6 Z" fill="{NAVY}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 8", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Identity & Access Management (IAM)", size=26, weight=600, fill=INK)
text(60, 110, "Who may do what, to which object — IEC 62443-3-3 SR 1.x / SR 2.x, with no model representation until now", size=13, fill=SOFT)

# ============================================================
# Panel 1: the chain — Identity -> AccessGrant -> Role -> Permission -> scope
# ============================================================
p1_y = 145
p1_h = 400
rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "The Chain — Identity Is Who, AccessGrant Is Where It Applies", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "A Role is a reusable template; an AccessGrant is the scoped, time-bounded binding that actually grants it", size=12.5, fill=SOFT)

row_y = p1_y + 130
bw, bh = 290, 96
gap = 55
labels = [
    ("Identity", "human | service-account", NAVY),
    ("AccessGrant", "scoped + time-bounded", RED),
    ("Role", "reusable template", NAVY),
    ("Permission", "action + scope", NAVY),
]
total_w = len(labels)*bw + (len(labels)-1)*gap
x0 = (W - total_w)/2
centers = []
for i, (lab, sub, col) in enumerate(labels):
    x = x0 + i*(bw+gap)
    rrect(x, row_y, bw, bh, rx=8, stroke=col, sw=2.4 if col == RED else 2, fill="#FFFFFF")
    text(x+bw/2, row_y+38, lab, size=16, weight=700, fill=col, anchor="middle")
    text(x+bw/2, row_y+60, sub, size=11, fill=SOFT, anchor="middle", style="italic")
    centers.append(x+bw/2)
    if i < len(labels)-1:
        line(x+bw, row_y+bh/2, x+bw+gap, row_y+bh/2, stroke=NAVY, sw=2, marker_end="tri-navy")

text(centers[0], row_y+bh+32, "a specific actor —", size=11.5, fill=MUTED, anchor="middle", style="italic")
text(centers[0], row_y+bh+50, "human or non-human", size=11.5, fill=MUTED, anchor="middle", style="italic")
text(centers[1], row_y+bh+32, "the binding: grantedAt,", size=11.5, fill=MUTED, anchor="middle", style="italic")
text(centers[1], row_y+bh+50, "expiresAt, and a scope", size=11.5, fill=MUTED, anchor="middle", style="italic")
text(centers[2], row_y+bh+32, "held by the AccessGrant,", size=11.5, fill=MUTED, anchor="middle", style="italic")
text(centers[2], row_y+bh+50, "resolved by MOC's RoleRef", size=11.5, fill=MUTED, anchor="middle", style="italic")
text(centers[3], row_y+bh+32, "view|operate|configure|approve,", size=11.5, fill=MUTED, anchor="middle", style="italic")
text(centers[3], row_y+bh+50, "scoped to an instance or a Class", size=11.5, fill=MUTED, anchor="middle", style="italic")

note_y = row_y + bh + 95
rrect(58, note_y, W-116, 58, rx=8, stroke=GRAY_DASH, sw=1.6, dash="4,4", fill="#FFFFFF")
text(80, note_y+24, "Operator (Sub-model 1) ≠ Identity: Operator records job title and capacity for display/audit; Identity is the broader,", size=12, fill=MUTED, style="italic")
text(80, note_y+42, "permissions-capable actor. Identity.operator links the two when an Identity represents a specific named Operator.", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 2: schema
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 385
rrect(30, p2_y, W-60, p2_h, stroke=BLUE, sw=2.2)
text(58, p2_y+38, "Schema — Identity, Role, Permission, AccessGrant", size=20, weight=700, fill=BLUE)
text(58, p2_y+60, "Least-privilege, reused from standard RBAC practice rather than invented", size=12.5, fill=SOFT)

def schema_box(x, y, w, h, title, subtitle, attrs, col=NAVY):
    rrect(x, y, w, h, stroke=col, sw=2.2, rx=8)
    text(x+16, y+26, title, size=14.5, weight=700, fill=col)
    if subtitle:
        text(x+16, y+44, subtitle, size=10.5, fill=SOFT, style="italic")
    ay = y + (66 if subtitle else 50)
    for a in attrs:
        text(x+16, ay, a, size=10.8, fill=MUTED, family="Consolas, Menlo, monospace")
        ay += 19.5
    return x, y, w, h

bx1, by1, bw1, bh1 = 58, p2_y+95, 340, 150
schema_box(bx1, by1, bw1, bh1, "Identity", "extends LunexObject", [
    "+ identityType : human | service-account",
    "+ credentialRef : string",
    "+ operator : OperatorRef | null",
], col=RED)

bx2, by2, bw2, bh2 = 448, p2_y+95, 320, 150
schema_box(bx2, by2, bw2, bh2, "AccessGrant", None, [
    "+ identity : IdentityRef",
    "+ role : RoleRef",
    "+ scope : LunexObjectRef",
    "+ grantedAt : timestamp",
    "+ expiresAt : timestamp | null",
])

bx3, by3, bw3, bh3 = 818, p2_y+95, 390, 75
schema_box(bx3, by3, bw3, bh3, "Role", None, [
    "+ permissions : PermissionRef[]",
])

bx4, by4, bw4, bh4 = 818, p2_y+215, 390, 95
schema_box(bx4, by4, bw4, bh4, "Permission", None, [
    "+ action : view | operate | configure | approve",
    "+ scope : LunexObjectRef | ClassRef",
])

ay_ = by1 + 50
line(bx1+bw1, ay_, bx2, ay_, stroke=NAVY, sw=1.8, marker_end="tri-navy")
line(bx2+bw2, ay_, bx3, ay_, stroke=NAVY, sw=1.8, marker_end="tri-navy")
line(bx3+bw3/2, by3+bh3, bx4+bw4/2, by4, stroke=NAVY, sw=1.8, marker_end="tri-navy")

mocx, mocy, mocw, moch = 1258, p2_y+95, 282, 215
rrect(mocx, mocy, mocw, moch, stroke=GREEN, sw=2.2, dash="5,4", rx=8)
text(mocx+mocw/2, mocy+30, "MOC (Sub-model 13)", size=13.5, weight=700, fill=GREEN, anchor="middle")
text(mocx+14, mocy+58, "ChangeRequest.requiredApprovals", size=10.5, fill=MUTED, family="Consolas, Menlo, monospace")
text(mocx+14, mocy+74, "\u00a0\u00a0: RoleRef[]", size=10.5, fill=MUTED, family="Consolas, Menlo, monospace")
text(mocx+14, mocy+104, "ChangePolicy.appliesTo and", size=10.5, fill=MUTED, family="Consolas, Menlo, monospace")
text(mocx+14, mocy+120, "LunexObject.owner also resolve", size=10.5, fill=MUTED, family="Consolas, Menlo, monospace")
text(mocx+14, mocy+136, "through RoleRef", size=10.5, fill=MUTED, family="Consolas, Menlo, monospace")
text(mocx+14, mocy+168, "an approval role is meaningless", size=10.5, fill=SOFT, style="italic")
text(mocx+14, mocy+185, "without something that says", size=10.5, fill=SOFT, style="italic")
text(mocx+14, mocy+202, "who holds it.", size=10.5, fill=SOFT, style="italic")
line(bx3+bw3, by3+bh3/2, mocx, by3+bh3/2, stroke=GREEN, sw=1.8, dash="4,4", marker_end="tri-navy")

text(58, by4+bh4+45, "AccessGrant.scope narrows a Role's permissions to a specific part of the model — the Role is reusable, the AccessGrant is where it actually applies.", size=12, fill=MUTED, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p2_y + p2_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=NAVY, sw=2, marker_end="tri-navy")
text(118, ly2+5, "resolves to / schema reference", size=13, fill=INK)
line(400, ly2, 446, ly2, stroke=GREEN, sw=2, dash="4,4", marker_end="tri-navy")
text(458, ly2+5, "referenced by Sub-model 13 (MOC)", size=13, fill=INK)
rrect(820, ly2-14, 28, 28, rx=6, stroke=RED, sw=2.2, fill="#FFFFFF")
text(862, ly2+5, "security-related (IEC 62443)", size=13, fill=INK)

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

with open("./lunex-iam-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
