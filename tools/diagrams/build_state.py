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

W = 1500
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
  <marker id="tri-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{GRAY_DASH}"/>
  </marker>
  <marker id="diamond-navy" viewBox="0 0 14 10" refX="0.5" refY="5" markerWidth="15" markerHeight="11" orient="auto-start-reverse">
    <path d="M0 5 L7 0 L14 5 L7 10 Z" fill="{NAVY}"/>
  </marker>
</defs>
'''
parts.append(head)
# background + grid placeholder rects are appended at the very end once final H is known
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 4", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Behavioral / State Model", size=26, weight=600, fill=INK)
text(60, 110, "The universal state machine behind LunexObject.state (Sub-model 1) — shared by every class", size=13, fill=SOFT)

# ============================================================
# Full state machine (transplanted from the original diagram)
# ============================================================
with open("state_machine_fragment.svg", encoding="utf-8") as f:
    fragment = f.read()
SM_TX, SM_TY = 20, 100
parts.append(f'<g transform="translate({SM_TX},{SM_TY})">')
parts.append(fragment)
parts.append('</g>')

sm_bottom = SM_TY + 1000  # bottom-most element of the transplanted diagram (Emergency-stop label / On ellipse)

# ============================================================
# One panel: optional states. Rollup / collective-status behavior across the
# hierarchy is intentionally out of scope here — a child can carry more than
# one simultaneous condition (e.g. both Inhibited and Emergency Stopping),
# so "worst-case" is not a simple reduction and deserves its own sub-model.
# ============================================================
panel_y = sm_bottom + 60
panel_w = W - 60
panel_h = 390
panel_xA = 30

text(W/2, panel_y-22, "the full machine above is the maximum \u2014 an object only uses the states its class needs", size=12.5, fill=SOFT, anchor="middle", style="italic")

# ---------- Panel: states are optional ----------
rrect(panel_xA, panel_y, panel_w, panel_h, stroke=GREEN, sw=2.2)
text(panel_xA+28, panel_y+38, "States Are Optional", size=20, weight=700, fill=GREEN)
text(panel_xA+28, panel_y+60, "example: a simple Sensor (no lock, no inhibit function)", size=12.5, fill=SOFT)

sy = panel_y + 215
used = ["Off", "Enabling", "Standby", "Starting", "On"]
skipped_top = ["Locked", "Unlocking"]
skipped_bot = ["Inhibited", "Inhibiting"]
ustep = 120
ux0 = panel_xA + panel_w/2 - 2*ustep
u_pts = [(ux0+i*ustep, sy) for i in range(len(used))]
for (px, py), lab in zip(u_pts, used):
    is_stable = lab in ("Off", "Standby", "On")
    if is_stable:
        parts.append(f'<ellipse cx="{px}" cy="{py}" rx="46" ry="26" fill="{NAVY}"/>')
        text(px, py+5, lab, size=13, weight=600, fill="#FFFFFF", anchor="middle")
    else:
        rrect(px-50, py-20, 100, 40, rx=20, stroke=GREEN, sw=2, fill="#FFFFFF")
        text(px, py+5, lab, size=12.5, weight=600, fill=GREEN, anchor="middle")
for i in range(len(u_pts)-1):
    x1 = u_pts[i][0] + (46 if used[i] in ("Off","Standby","On") else 50)
    x2 = u_pts[i+1][0] - (46 if used[i+1] in ("Off","Standby","On") else 50)
    line(x1, sy, x2, sy, stroke=GREEN, sw=2, marker_end="tri-navy")

# skipped ghost states: Locked/Unlocking branch off "Off", Inhibited/Inhibiting branch off "Standby"
off_x = u_pts[0][0]
standby_x = u_pts[2][0]

gy_top = sy - 85
for gx, lab in zip([off_x-65, off_x+65], skipped_top):
    rrect(gx-48, gy_top-19, 96, 38, rx=19, stroke=GRAY_DASH, sw=1.6, dash="5,4", fill="#FFFFFF")
    text(gx, gy_top+5, lab, size=11.5, fill=SOFT, anchor="middle", style="italic")
path(f"M {off_x} {sy-26} L {off_x} {gy_top+19}", stroke=GRAY_DASH, sw=1.4, dash="4,3")

gy_bot = sy + 85
for gx, lab in zip([standby_x-65, standby_x+65], skipped_bot):
    rrect(gx-48, gy_bot-19, 96, 38, rx=19, stroke=GRAY_DASH, sw=1.6, dash="5,4", fill="#FFFFFF")
    text(gx, gy_bot+5, lab, size=11.5, fill=SOFT, anchor="middle", style="italic")
path(f"M {standby_x} {sy+26} L {standby_x} {gy_bot-19}", stroke=GRAY_DASH, sw=1.4, dash="4,3")

text(panel_xA+28, panel_y+344, "Locked/Inhibited branches exist in the model but are never reached \u2014", size=12.5, fill=MUTED)
text(panel_xA+28, panel_y+362, "this class simply has no transitions into them", size=12.5, fill=MUTED)

# ---------- Out-of-scope note: collective / rollup status ----------
oos_y = panel_y + panel_h + 40
rrect(30, oos_y, W-60, 84, rx=10, stroke=GRAY_DASH, sw=1.6, dash="6,4", fill="#FFFFFF")
text(54, oos_y+30, "Out of scope here: collective status across the hierarchy.", size=13, fill=SOFT, weight=600, style="italic")
text(54, oos_y+52, "A child can carry more than one condition at once (e.g. Inhibited and Emergency Stopping", size=12.5, fill=SOFT, style="italic")
text(54, oos_y+70, "together) \u2014 that is not a simple worst-case reduction and is described in Sub-model 9 (Collective Status / Rollup).", size=12.5, fill=SOFT, style="italic")

# ============================================================
# Formal link note

# ============================================================
note_y = oos_y + 84 + 45
rrect(30, note_y, W-60, 70, rx=10, stroke=SOFT, sw=1.5, fill="#FFFFFF")
text(54, note_y+28, "LunexObject.state (Sub-model 1) is one instance of this machine.", size=13, fill=INK, weight=600, family="Consolas, Menlo, monospace")
text(54, note_y+50, "LunexObject.health stays independent \u2014 diagnostics, not operating mode.", size=12.5, fill=SOFT, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = note_y + 70 + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
parts.append(f'<ellipse cx="76" cy="{ly2}" rx="14" ry="10" fill="{NAVY}"/>')
text(102, ly2+5, "stable state", size=13, fill=INK)
rrect(230, ly2-14, 34, 26, rx=13, stroke=SOFT, sw=1.8, fill="#FFFFFF")
text(276, ly2+5, "transition state (ends on Complete)", size=13, fill=INK)
rrect(560, ly2-14, 34, 26, rx=13, stroke=GRAY_DASH, sw=1.6, dash="5,4", fill="#FFFFFF")
text(606, ly2+5, "state not used by this object class", size=13, fill=INK)

ly3 = ly2 + 40
line(60, ly3, 106, ly3, stroke=GREEN, sw=2, marker_end="tri-navy")
text(118, ly3+5, "start-up path", size=13, fill=INK)
line(280, ly3, 326, ly3, stroke=BLUE, sw=2, marker_end="tri-navy")
text(338, ly3+5, "shutdown / stop", size=13, fill=INK)
line(500, ly3, 546, ly3, stroke=RED, sw=2, marker_end="tri-navy")
text(558, ly3+5, "emergency stop", size=13, fill=INK)

final_h = int(ly3 + 60)
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

with open("./lunex-state-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
