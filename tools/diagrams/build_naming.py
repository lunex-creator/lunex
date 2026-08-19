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

def text(x, y, s, size=13, weight=400, fill=INK, anchor="start", style="normal", family=None, spacing=None, strike=False):
    fam = f' font-family="{family}"' if family else ""
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    it = f' font-style="{style}"' if style != "normal" else ""
    td = ' text-decoration="line-through"' if strike else ""
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{it}{fam}{sp}{td}>{esc(s)}</text>')

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
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 8", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Naming & Terminology", size=26, weight=600, fill=INK)
text(60, 110, "A living register of every deliberate deviation from S88 / S95 / PackML \u2014 and why", size=13, fill=SOFT)

# ============================================================
# Panel 1: Renamed terms — the register
# ============================================================
p1_y = 145
rows = [
    ("Realm / Domain / Location", "Enterprise / Division / Site", "broader than an industrial plant; enables the addressable path in Sub-model 7", "2"),
    ("Area", "Zone", "\u201cZone\u201d already means something specific in IEC 62443 (Sub-model 6)", "2"),
    ("Cell", "Segment", "S88 and S95 already use \u201csegment\u201d differently from each other", "2"),
    ("Point-to-Point", "Distributed", "\u201cDistributed\u201d already means a DCS (multiple controllers) in OT usage", "3"),
    ("Star", "Mixed-Distributed", "precise, standard network-topology term \u2014 needs no explanation", "3"),
    ("Mesh", "Hybrid", "\u201cHybrid\u201d already means continuous+batch manufacturing in S88", "3"),
    ("lockType: inhibit / lock", "Process Lock / Machine Lock", "reuses existing Sub-model 4 state names instead of new, severity-implying labels", "5"),
    ("Envelope", "Container", "\u201cContainer\u201d already means a Docker/Kubernetes deployment unit", "7"),
    ("Inventory", "Library", "plainer, more approachable \u2014 avoids a stuffy academic connotation", "1"),
    ("Alarm.state (own value space)", "reusing Sub-model 4's State enum", "operator-response states are not object-behavior states \u2014 different question, different values", "10"),
    ("Alarm.origin", "reusing Alarm.source's name", "Alarm.source already means \u201cwhich Device\u201d (DeviceRef) \u2014 origin avoids a same-class field collision", "15"),
    ("automaticMode: none", "on-demand", "manual override is universal, not exclusive to one mode (manualOverrideAvailable)", "12/14"),
    ("physicalRef: DeviceRef | ComponentRef", "physicalRef: DeviceRef only", "multi-CPU racks need Component granularity \u2014 Components already have id (Sub-model 1)", "1"),
]
row_h = 42
header_h = 40
p1_h = header_h + len(rows)*row_h + 30
rrect(30, p1_y, W-60, p1_h, stroke=NAVY, sw=2.2)
text(58, p1_y+34, "Renamed Terms", size=18, weight=700, fill=INK)

col1, col2, col3, col4 = 60, 460, 860, 1500
hy = p1_y + 70
text(col1, hy, "LUNEX TERM", size=11, fill=SOFT, spacing="1.2", weight=700)
text(col2, hy, "AVOIDED TERM", size=11, fill=SOFT, spacing="1.2", weight=700)
text(col3, hy, "REASON", size=11, fill=SOFT, spacing="1.2", weight=700)
text(col4, hy, "SUB-MODEL", size=11, fill=SOFT, spacing="1.2", weight=700, anchor="end")
line(58, hy+12, W-58, hy+12, stroke=LINE, sw=1)

ry = hy + 38
for lunex_term, avoided, reason, sm in rows:
    text(col1, ry, lunex_term, size=13, weight=700, fill=NAVY, family="Consolas, Menlo, monospace")
    text(col2, ry, avoided, size=12.5, fill=SOFT, strike=True)
    text(col3, ry, reason, size=12, fill=MUTED)
    text(col4, ry, sm, size=12.5, fill=SOFT, anchor="end")
    ry += row_h

with open("./lunex-naming-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part1 ok", p1_y+p1_h)

# ============================================================
# Panel 2: Terms deliberately kept — for balance
# ============================================================
p2_y = p1_y + p1_h + 45
kept = [
    ("SIL / SIF", "IEC 61508 / 61511", "Sub-model 5"),
    ("SL / Zone / Conduit", "IEC 62443", "Sub-model 6"),
    ("Stop Categories 0 / 1 / 2", "IEC 60204-1", "Sub-model 4 / 5"),
    ("the state machine itself", "PackML-style pattern", "Sub-model 4"),
    ("Priority \u00b7 Shelving \u00b7 RTN", "ISA-18.2", "Sub-model 10 / 11"),
    ("System (= Unit)", "ISA-88", "Sub-model 2"),
]
p2_h = 40 + len(kept)*38 + 60
rrect(30, p2_y, W-60, p2_h, stroke=GREEN, sw=2.2)
text(58, p2_y+34, "Terms Deliberately Kept", size=18, weight=700, fill=GREEN)
text(58, p2_y+56, "renaming is not the default \u2014 these already fit LUNEX exactly as written in the source standard", size=12.5, fill=SOFT)

ky = p2_y + 96
for term, source, sm in kept:
    parts.append(f'<circle cx="70" cy="{ky-5}" r="4" fill="{GREEN}"/>')
    text(84, ky, term, size=13, weight=700, fill=NAVY, family="Consolas, Menlo, monospace")
    text(440, ky, source, size=12.5, fill=MUTED)
    text(W-58, ky, sm, size=12.5, fill=SOFT, anchor="end")
    ky += 38

with open("./lunex-naming-model.svg.partial", "w") as f:
    f.write("placeholder")
print("part2 ok", p2_y+p2_h)

# ============================================================
# Panel 3: New vocabulary — concepts PackML/S88 don't have at all
# ============================================================
p3_y = p2_y + p2_h + 45
newterms = [
    ("LunexObject", "the abstract base class every object in LUNEX inherits from", "1"),
    ("Interlock", "a first-class safety object with its own id, state and proof-test history", "5"),
    ("Zone", "a security grouping with a target and achieved Security Level", "6"),
    ("Conduit", "the governed crossing point between two Zones, where Firewall/IDS sits", "6"),
    ("Digital Twin", "the AI-side, queryable mirror of a physical object", "7"),
    ("Telemetry Envelope", "the addressed, timestamped wrapper every object streams out", "7"),
    ("Context Layer", "semantic relationships an AI can traverse, beyond the containment chain", "7"),
    ("Tier / worstTier", "the severity ranking the state machine itself doesn't carry", "9"),
    ("Rollup", "cross-object status aggregation, computed in the AI layer, not the object model", "9"),
    ("Alarm", "priority = severity \u00d7 actionability, not severity alone", "10"),
    ("Alarm Response Procedure", "reusable, per alarm type \u2014 probable cause through corrective action", "11"),
    ("GuidanceRecommendation", "simulated scenarios from the Digital Twin, golden scenario optional", "12"),
    ("SimulationPolicy", "always / risk-based / none + manualOverrideAvailable \u2014 decided per Assembly", "12"),
    ("jumpToWorst()", "one action from any node straight to the Device/Alarm causing it", "13"),
    ("Historian", "append-only record of every state, ever \u2014 the Twin's other destination", "14"),
    ("RetentionPolicy", "same shape as SimulationPolicy \u2014 always / risk-based / none, by design", "14"),
    ("PredictedEvent", "a forward-looking claim, raised into the Alarm system tagged predictive", "15"),
    ("ImprovementRecommendation", "always requires human approval \u2014 no confidence threshold skips it", "15"),
    ("AIControlUnit", "a Control Unit subclass; Interlock forces it exactly like any Device", "16"),
]
cols = 3
card_w = (W - 60 - 56 - 2*24) / 3
card_h = 84
row_gap = 16
rows_n = 7
p3_h = 90 + rows_n*(card_h+row_gap) + 20
rrect(30, p3_y, W-60, p3_h, stroke=BLUE, sw=2.2)
text(58, p3_y+34, "New Vocabulary", size=18, weight=700, fill=BLUE)
text(58, p3_y+56, "not renamed from anything \u2014 these concepts simply don't exist in PackML or S88", size=12.5, fill=SOFT)

gy0 = p3_y + 90
for idx, (term, desc, sm) in enumerate(newterms):
    col = idx % cols
    row = idx // cols
    cx_ = 58 + col*(card_w+24)
    cy_ = gy0 + row*(card_h+row_gap)
    rrect(cx_, cy_, card_w, card_h, rx=8, stroke=BLUE, sw=1.8, fill="#FFFFFF")
    text(cx_+16, cy_+26, term, size=13, weight=700, fill=BLUE, family="Consolas, Menlo, monospace")
    text(cx_+card_w-14, cy_+26, sm, size=10.5, fill=SOFT, anchor="end")
    words = desc.split(" ")
    line1, line2, cur = "", "", ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if len(trial) > 40 and not line1:
            line1 = cur
            cur = w_
        else:
            cur = trial
    line2 = cur
    if not line1:
        line1, line2 = line2, ""
    text(cx_+16, cy_+48, line1, size=11, fill=MUTED)
    if line2:
        text(cx_+16, cy_+65, line2, size=11, fill=MUTED)

# ============================================================
# Panel 4: The naming principle
# ============================================================
p4_y = p3_y + p3_h + 45
p4_h = 130
rrect(30, p4_y, W-60, p4_h, stroke=NAVY, sw=2.4)
text(58, p4_y+36, "The Naming Principle", size=18, weight=700, fill=NAVY)
text(58, p4_y+66, "Rename a term only when it already carries a conflicting meaning elsewhere in the model, or in", size=14, fill=INK, weight=600)
text(58, p4_y+88, "an adjacent standard LUNEX must interoperate with. Otherwise, reuse established vocabulary \u2014", size=14, fill=INK, weight=600)
text(58, p4_y+110, "inventing a new word is not innovation if the old one wasn't actually broken.", size=14, fill=INK, weight=600)

final_h = int(p4_y + p4_h + 50)
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

with open("./lunex-naming-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
