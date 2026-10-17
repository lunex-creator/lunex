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
  <marker id="tri-hollow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">
    <path d="M0 0 L12 6 L0 12 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="1.4"/>
  </marker>
  <marker id="tri-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{BLUE}"/>
  </marker>
</defs>
'''
parts.append(head)
BG_INSERT_INDEX = len(parts)

text(60, 56, "LUNEX — SUB-MODEL 5", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Recipe & Execution Model", size=26, weight=600, fill=INK)
text(60, 110, "ISA-88's structure with self-describing names, laid over Sub-model 2 (where) and Sub-model 4 (state) — no new state machine", size=13, fill=SOFT)

# ============================================================
# Panel 1: Recipe scopes + RecipeElement tree
# ============================================================
p1_y = 145
p1_h = 475
rrect(30, p1_y, W-60, p1_h, stroke=BLUE, sw=2.2)
text(58, p1_y+38, "Recipe — a Template, Refined Step by Step via derivedFrom", size=20, weight=700, fill=BLUE)
text(58, p1_y+60, "Recipe.recipeLevel: each recipe refines the one in its derivedFrom link (ISA-88: General \u2192 Site \u2192 Master \u2192 Control)", size=12.5, fill=SOFT)

levels = [("product", SOFT, "the product, independent of any plant"), ("location", BLUE, "adapted to one Location"), ("equipment", NAVY, "fixed to specific equipment"), ("execution", RED, "baseline of one execution")]
lv_y = p1_y + 110
lv_w, gap = 260, 40
lv_x0 = (W - (len(levels)*lv_w + (len(levels)-1)*gap)) / 2
for i, (lab, col, sub) in enumerate(levels):
    x = lv_x0 + i*(lv_w+gap)
    rrect(x, lv_y, lv_w, 56, rx=8, stroke=col, sw=2.2, fill="#FFFFFF")
    text(x+lv_w/2, lv_y+24, lab, size=14, weight=700, fill=col, anchor="middle")
    text(x+lv_w/2, lv_y+44, sub, size=10.5, fill=SOFT, anchor="middle", style="italic")
    if i < len(levels)-1:
        line(x+lv_w, lv_y+28, x+lv_w+gap, lv_y+28, stroke=NAVY, sw=2, marker_end="tri-navy")
text(lv_x0+lv_w*3+gap*2, lv_y+90, "execution = equipment + resolved run-time parameters \u2014 recorded in RecipeExecution.parameterValues", size=12, fill=MUTED, style="italic", anchor="end")

pe_y = p1_y + 260
text(58, pe_y, "RecipeElement — Steps Named by the Asset Level They Run On (Recipe.structure)", size=15, weight=700, fill=INK)
tree = [("area", "multi-cell recipe", "not in ISA-88"), ("cell", "whole process", "ISA-88: procedure"), ("system", "one functional unit", "ISA-88: unit procedure"), ("assembly", "coordinated devices", "ISA-88: operation")]
tx0 = 58
for i, (lab, sub, iso) in enumerate(tree):
    x = tx0 + i*280
    col = RED if lab == "assembly" else NAVY
    rrect(x, pe_y+30, 230, 62, rx=8, stroke=col, sw=2, fill="#FFFFFF")
    text(x+115, pe_y+55, "runsOn: " + lab, size=13, weight=700, fill=col, anchor="middle", family="Consolas, Menlo, monospace")
    text(x+115, pe_y+73, sub + "  \u00b7  " + iso, size=10.5, fill=SOFT, anchor="middle", style="italic")
    if i < len(tree)-1:
        line(x+230, pe_y+61, x+280, pe_y+61, stroke=NAVY, sw=2, marker_end="tri-navy")
text(tx0+3*280+115, pe_y+112, "leaf \u2014 no children", size=11.5, fill=RED, anchor="middle", style="italic")
text(tx0, pe_y+112, "a child always runs on a lower level than its parent; any level may be skipped  \u00b7  childOrder: sequence | parallel", size=12, fill=MUTED, style="italic")
text(tx0, pe_y+134, "No element for Device \u2014 a Device has its own Sub-model 4 state; an assembly element commands it and waits for that state", size=12, fill=MUTED, style="italic")
text(tx0, pe_y+156, "target (AreaRef \u2026 AssemblyRef | null) is bound at equipment level; equipmentClass (ClassRef) filters before that", size=12, fill=MUTED, style="italic")
text(tx0, pe_y+192, "Recipe.goldenExecution \u2192 the known-good reference RecipeExecution  \u00b7  Recipe.basedOnExecution \u2192 provenance of a recipe promoted from a tuned RecipeExecution (after approval, Sub-model 13)", size=12, fill=MUTED, style="italic")

# ============================================================
# Panel 2: RecipeExecution — the instance, reusing Sub-model 4 directly
# ============================================================
p2_y = p1_y + p1_h + 50
p2_h = 455
rrect(30, p2_y, W-60, p2_h, stroke=BLUE, sw=2.2)
text(58, p2_y+38, "RecipeExecution — One Execution, Reusing Sub-model 4 Directly", size=20, weight=700, fill=BLUE)
text(58, p2_y+60, "PackML's states already ARE recipe-execution states — Sub-model 4 said so from the start; no override needed", size=12.5, fill=SOFT)

bx, by, bw, bh = 60, p2_y+100, 420, 280
rrect(bx, by, bw, bh, stroke=RED, sw=2.4, rx=8)
text(bx+16, by+28, "RecipeExecution", size=15, weight=700, fill=RED)
text(bx+16, by+46, "extends LunexObject", size=10.5, fill=SOFT, style="italic")
battrs = [
    "+ recipe : RecipeRef",
    "+ equipment : AreaRef | CellRef | SystemRef",
    "+ currentSteps : RecipeElementRef[]",
    "+ parameterValues : Map<string,value>",
    "+ adjustments : ParameterAdjustment[]",
    "+ startTime / endTime : timestamp",
    "+ quantityTarget : quantity | null",
    "+ genealogy : RecipeExecutionRef[]  (optional)",
    "+ state : State  (Sub-model 4 — reused)",
]
ay = by+70
for a in battrs:
    text(bx+16, ay, a, size=11.3, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 22

sx, sy, sw_, sh = 560, p2_y+100, 460, 250
rrect(sx, sy, sw_, sh, stroke=NAVY, sw=2, dash="5,4", rx=8)
text(sx+16, sy+28, "Sub-model 4 state machine", size=13.5, weight=700, fill=NAVY)
bw_, bh_ = 110, 36
cols = [sx+90, sx+230, sx+370]          # box centres, 140 apart
r1y, r2y = sy+62, sy+138
def sbox(cx, cy, label, col, w=bw_):
    rrect(cx-w/2, cy, w, bh_, rx=18, stroke=col, sw=2, fill="#FFFFFF")
    text(cx, cy+bh_/2+4, label, size=11.5, weight=700, fill=col, anchor="middle")
sbox(cols[0], r1y, "Standby", SOFT)
sbox(cols[1], r1y, "Starting", BLUE)
sbox(cols[2], r1y, "On", GREEN)
sbox(cols[0], r2y, "Standby", SOFT)
sbox(cols[2], r2y, "Controlled Stopping", BLUE, w=150)
line(cols[0]+bw_/2, r1y+bh_/2, cols[1]-bw_/2-2, r1y+bh_/2, stroke=NAVY, sw=1.8, marker_end="tri-navy")
line(cols[1]+bw_/2, r1y+bh_/2, cols[2]-bw_/2-2, r1y+bh_/2, stroke=NAVY, sw=1.8, marker_end="tri-navy")
line(cols[2], r1y+bh_, cols[2], r2y-2, stroke=NAVY, sw=1.8, marker_end="tri-navy")
line(cols[2]-75, r2y+bh_/2, cols[0]+bw_/2+2, r2y+bh_/2, stroke=NAVY, sw=1.8, marker_end="tri-navy")
text(cols[2]-8, (r1y+bh_+r2y)/2+4, "Controlled stop", size=10.5, fill=SOFT, anchor="end", style="italic")
text(cols[1], r2y+bh_/2-8, "Complete", size=10.5, fill=SOFT, anchor="middle", style="italic")
text(sx+16, sy+205, "no RecipeExecution-specific state value is ever introduced —", size=11.5, fill=MUTED, style="italic")
text(sx+16, sy+223, "unlike Alarm (Sub-model 15), which genuinely needed one.", size=11.5, fill=MUTED, style="italic")

note_y = p2_y + p2_h - 36
text(58, note_y, "methods() on RecipeExecution: no override — it returns exactly the standard Sub-model 4 trigger list for its current state (Appendix A)", size=12.5, fill=MUTED, style="italic")

# ============================================================
# Legend
# ============================================================
leg_y = p2_y + p2_h + 55
line(60, leg_y-15, W-60, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y + 40
line(60, ly2, 106, ly2, stroke=NAVY, sw=2, marker_end="tri-navy")
text(118, ly2+5, "narrows into / proceeds to", size=13, fill=INK)
rrect(380, ly2-14, 36, 28, rx=6, stroke=RED, sw=2, fill="#FFFFFF")
text(396, ly2+5, "", size=11, anchor="middle")
text(425, ly2+5, "assembly element — the only leaf in RecipeElement", size=13, fill=INK)

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

with open("./lunex-recipe-execution-model.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)

print("done", final_h)
