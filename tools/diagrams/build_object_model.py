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

W, H = 1700, 1260
parts = []

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def rrect(x, y, w, h, rx=12, fill="#FFFFFF", stroke=NAVY, sw=2, dash=None):
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

head = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Inter, Segoe UI, Helvetica Neue, Arial, sans-serif">
<defs>
  <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
    <path d="M20 0H0V20" fill="none" stroke="#E6EBF0" stroke-width="1"/>
  </pattern>
  <pattern id="grid5" width="100" height="100" patternUnits="userSpaceOnUse">
    <rect width="100" height="100" fill="url(#grid)"/>
    <path d="M100 0H0V100" fill="none" stroke="{LINE}" stroke-width="1"/>
  </pattern>
  <marker id="tri-hollow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">
    <path d="M0 0 L12 6 L0 12 Z" fill="#FFFFFF" stroke="{NAVY}" stroke-width="1.4"/>
  </marker>
  <marker id="diamond-navy" viewBox="0 0 14 10" refX="0.5" refY="5" markerWidth="15" markerHeight="11" orient="auto-start-reverse">
    <path d="M0 5 L7 0 L14 5 L7 10 Z" fill="{NAVY}"/>
  </marker>
  <marker id="tri-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 Z" fill="{RED}"/>
  </marker>
</defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#grid5)"/>
'''
parts.append(head)

text(60, 56, "LUNEX — SUB-MODEL 1", size=14, fill=SOFT, spacing="2.5")
text(60, 86, "Object / Class Model", size=26, weight=600, fill=INK)
text(60, 110, "Base class, function interfaces, five universal classes and derived types", size=13, fill=SOFT)

# ---------- LunexObject ----------
lx, ly, lw, lh = 650, 140, 400, 250
rrect(lx, ly, lw, lh, stroke=NAVY, sw=2.5)
cx_lunex = lx + lw/2
text(cx_lunex, 172, "LunexObject", size=21, weight=700, fill=NAVY, anchor="middle")
text(cx_lunex, 192, "«abstract base class»", size=12, fill=SOFT, anchor="middle", style="italic")
line(lx+15, 202, lx+lw-15, 202, stroke=LINE, sw=1)
attrs = [
    "+ id : string", "+ tag : string", "+ class : Class", "+ parent : LunexObject",
    "+ state : State", "+ health : Health", "+ properties : Map<Key,Value>", "+ methods() : Procedure[]",
]
ay = 222
for a in attrs:
    text(lx+22, ay, a, size=13, fill=MUTED, family="Consolas, Menlo, monospace")
    ay += 19
lunex_bottom = ly + lh

# ---------- Device / Component ----------
dy, dh = 430, 100
dx, dw = 740, 220
rrect(dx, dy, dw, dh, stroke=NAVY, sw=2)
cx_device = dx + dw/2
text(cx_device, 462, "Device", size=18, weight=700, fill=NAVY, anchor="middle")
text(cx_device, 480, "«abstract»", size=11, fill=SOFT, anchor="middle", style="italic")
text(cx_device, 500, "assembly-level unit", size=11, fill=SOFT, anchor="middle")
text(cx_device, 516, "composes 0..* Component", size=11, fill=SOFT, anchor="middle")
line(cx_device, dy, cx_device, lunex_bottom, stroke=NAVY, sw=2, marker_end="tri-hollow")

px, pw = 1300, 220
rrect(px, dy, pw, dh, stroke=NAVY, sw=2)
cx_comp = px + pw/2
text(cx_comp, 462, "Component", size=18, weight=700, fill=NAVY, anchor="middle")
text(cx_comp, 480, "«abstract»", size=11, fill=SOFT, anchor="middle", style="italic")
text(cx_comp, 500, "not independently", size=11, fill=SOFT, anchor="middle")
text(cx_comp, 516, "addressable", size=11, fill=SOFT, anchor="middle")
path(f"M {cx_comp} {dy} L {lx+lw} {ly+130}", stroke=NAVY, sw=2, marker_end="tri-hollow")

comp_link_y = 480
line(dx+dw, comp_link_y, px, comp_link_y, stroke=NAVY, sw=2, marker_start="diamond-navy")
text((dx+dw+px)/2, comp_link_y-8, "0..*", size=12, fill=SOFT, anchor="middle", style="italic")

# component derived card
ccy = 555
ccw = 240
ccx2 = cx_comp - ccw/2
comp_items = ["Digital Input", "Analog Output", "PID-controller", "Processor", "Comms Module / Gateway"]
cch = 46 + len(comp_items)*22 + 16
rrect(ccx2, ccy, ccw, cch, stroke=SOFT, sw=1.5, fill="#FFFFFF")
line(cx_comp, dy+dh, cx_comp, ccy, stroke=NAVY, sw=1.6, marker_end="tri-hollow")
text(ccx2+16, ccy+26, "examples (derived)", size=10.5, fill=SOFT, spacing="1")
iy = ccy + 50
for it in comp_items:
    text(ccx2+16, iy, "• " + it, size=12.5, fill=MUTED, family="Consolas, Menlo, monospace")
    iy += 22
comp_card_bottom = ccy + cch

# ---------- Five universal classes ----------
row_y, row_h = 740, 100
centers = [230, 540, 850, 1160, 1470]
box_w = 220
names = ["Sensor", "Transducer", "Control Unit", "Signal Converter", "Actuator"]
func_of = {
    "Sensor": ("Sensing", GREEN),
    "Transducer": ("Converting", BLUE),
    "Control Unit": ("Controlling", NAVY),
    "Signal Converter": ("Converting", BLUE),
    "Actuator": ("Actuating", GREEN),
}

box_coords = {}
# spread arrival points across Device's bottom edge, in the same left-to-right
# order as the source boxes, so the five inheritance lines fan out without crossing
arrival_xs = [dx + dw*0.09, dx + dw*0.30, dx + dw*0.5, dx + dw*0.70, dx + dw*0.91]
lollipop_side = {"Sensor": -1, "Transducer": -1, "Control Unit": 1, "Signal Converter": 1, "Actuator": 1}

for cx, name, arrival_x in zip(centers, names, arrival_xs):
    bx = cx - box_w/2
    rrect(bx, row_y, box_w, row_h, stroke=NAVY, sw=2)
    text(cx, row_y+34, name, size=17, weight=700, fill=NAVY, anchor="middle")
    text(cx, row_y+52, "extends Device", size=11, fill=SOFT, anchor="middle", style="italic")
    box_coords[name] = (bx, row_y, box_w, row_h, cx)
    if name == "Actuator":
        # bend left below the Component derived-card before heading up to Device,
        # so the diagonal never clips through that card
        path(f"M {cx} {row_y} L 1280 732 L {arrival_x} {dy+dh}", stroke=NAVY, sw=1.8, marker_end="tri-hollow")
    else:
        path(f"M {cx} {row_y} L {arrival_x} {dy+dh}", stroke=NAVY, sw=1.8, marker_end="tri-hollow")
    lp_x = cx + 70*lollipop_side[name]
    lp_y = row_y - 46
    func, col = func_of[name]
    line(lp_x, row_y, lp_x, lp_y+9, stroke=col, sw=2)
    parts.append(f'<circle cx="{lp_x}" cy="{lp_y}" r="7" fill="#FFFFFF" stroke="{col}" stroke-width="2.5"/>')
    text(lp_x, lp_y-14, func, size=11, weight=600, fill=col, anchor="middle")

# ---------- derived example cards ----------
card_y = row_y + row_h + 40
derived = {
    "Sensor": ["Load Cell", "Encoder", "Pressure Sensor", "Temperature Sensor", "Energy Meter", ("E-stop Button", "safety")],
    "Transducer": ["4-20mA Transmitter", "Signal Amplifier"],
    "Control Unit": ["PLC", "DCS", "Microcontroller", "AIControlUnit", "VFD / Servo Drive *", ("Safety PLC / SIS", "safety"), ("Firewall / IDS", "security")],
    "Signal Converter": ["Relay", "Soft Starter", "Solenoid Driver", "3/2-way Pilot", "VFD / Servo Drive *"],
    "Actuator": ["Valve", "Motor", "Heater", "Pump", ("Shutdown Valve", "safety")],
}
card_bottom_max = card_y
for name in names:
    bx, by, bw, bh, cx = box_coords[name]
    items = derived[name]
    n = len(items)
    ch = 46 + n*22 + 16
    ccx3 = cx - box_w/2
    rrect(ccx3, card_y, box_w, ch, stroke=SOFT, sw=1.5, fill="#FFFFFF")
    line(cx, by+bh, cx, card_y, stroke=NAVY, sw=1.6, marker_end="tri-hollow")
    text(ccx3+16, card_y+26, "examples (derived)", size=10.5, fill=SOFT, spacing="1")
    iy = card_y + 50
    for it in items:
        if isinstance(it, tuple):
            label, kind = it
            col = RED if kind == "safety" else BLUE
            weight = 600
        else:
            label, col, weight = it, MUTED, 400
        text(ccx3+16, iy, "• " + label, size=12.5, fill=col, family="Consolas, Menlo, monospace", weight=weight)
        iy += 22
    card_bottom_max = max(card_bottom_max, card_y + ch)

# ---------- legend ----------
leg_y = card_bottom_max + 60
line(60, leg_y-15, 1640, leg_y-15, stroke=LINE, sw=1)
text(60, leg_y+8, "LEGEND", size=12, fill=SOFT, spacing="1.6")

ly2 = leg_y+40
line(60, ly2, 110, ly2, stroke=NAVY, sw=2, marker_end="tri-hollow")
text(122, ly2+5, "inheritance (extends)", size=13, fill=INK)

line(320, ly2, 370, ly2, stroke=NAVY, sw=2, marker_start="diamond-navy")
text(382, ly2+5, "composition (has 0..*)", size=13, fill=INK)

parts.append(f'<circle cx="610" cy="{ly2}" r="7" fill="#FFFFFF" stroke="{BLUE}" stroke-width="2.5"/>')
line(610, ly2+7, 610, ly2+22, stroke=BLUE, sw=2)
text(632, ly2+5, "function-interface (Sensing / Converting / Controlling / Actuating)", size=13, fill=INK)

text(60, ly2+40, "red + bold = safety-related subclass (SIL/interlock)", size=13, fill=RED, weight=600)
text(700, ly2+40, "blue + bold = security-related subclass (IEC 62443)", size=13, fill=BLUE, weight=600)
path(f"M 1050 {ly2} L 1100 {ly2}", stroke=RED, sw=1.8, dash="4,3", marker_end="tri-red")
text(1112, ly2+5, "physicalRef (points to a Device or Component \u2014 whichever is actually shared)", size=13, fill=INK)
text(60, ly2+68, "* VFD / Servo Drive appears under both classes \u2014 one physical device, always Controlling + Converting at once, optionally Transducer too", size=12.5, fill=SOFT, style="italic")

# ============================================================
# Cross-cutting peers of Device & Component, added by later sub-models
# ============================================================
sec_y = ly2 + 110
line(60, sec_y-20, 1640, sec_y-20, stroke=LINE, sw=1)
text(60, sec_y+10, "Peers of Device & Component \u2014 Added by Later Sub-models", size=19, weight=700, fill=INK)
text(60, sec_y+32, "same base class, same rules \u2014 none of these needed a new class tree of their own", size=12.5, fill=SOFT)

lo2_w, lo2_h = 280, 56
lo2_x = 850 - lo2_w/2
lo2_y = sec_y + 60
rrect(lo2_x, lo2_y, lo2_w, lo2_h, stroke=NAVY, sw=2, rx=8)
text(850, lo2_y+24, "LunexObject", size=14, weight=700, fill=NAVY, anchor="middle")
text(850, lo2_y+42, "\u00ababstract\u00bb", size=10.5, fill=SOFT, anchor="middle", style="italic")

peer_names = ["Interlock", "Zone", "Conduit", "Alarm", "GuidanceRecommendation", "PredictedEvent", "ImprovementRecommendation", "Operator"]
peer_sm = ["5", "6", "6", "10", "12", "15", "15", "1"]
peer_desc = ["forces/blocks a", "security grouping,", "governed crossing", "priority = severity", "simulated scenarios,", "a forward-looking", "always requires", "resolves"]
peer_desc2 = ["transition", "target/achieved SL", "between two Zones", "\u00d7 actionable", "golden optional", "claim, raised into Alarm", "human approval", "OperatorRef elsewhere"]

n_peer = len(peer_names)
peer_box_w = 190
peer_gap = 10
total_peer_w = n_peer*peer_box_w + (n_peer-1)*peer_gap
start_x = 850 - total_peer_w/2
peer_centers = [start_x + i*(peer_box_w+peer_gap) + peer_box_w/2 for i in range(n_peer)]

bus_y = lo2_y + lo2_h + 40
peer_row_y = bus_y + 55
peer_box_h = 100

line(850, lo2_y+lo2_h, 850, bus_y, stroke=NAVY, sw=2, marker_end="tri-hollow")
line(peer_centers[0], bus_y, peer_centers[-1], bus_y, stroke=NAVY, sw=1.6)

for cx, name, sm, d1, d2 in zip(peer_centers, peer_names, peer_sm, peer_desc, peer_desc2):
    bx = cx - peer_box_w/2
    line(cx, bus_y, cx, peer_row_y, stroke=NAVY, sw=1.6)
    rrect(bx, peer_row_y, peer_box_w, peer_box_h, stroke=RED, sw=2, rx=8)
    text(cx, peer_row_y+26, name, size=11, weight=700, fill=RED, anchor="middle", family="Consolas, Menlo, monospace")
    text(cx, peer_row_y+50, d1, size=10, fill=MUTED, anchor="middle")
    text(cx, peer_row_y+66, d2, size=10, fill=MUTED, anchor="middle")
    text(cx+peer_box_w/2-10, peer_row_y+90, "Sub-model " + sm, size=9.5, fill=SOFT, anchor="end")

text(60, peer_row_y+peer_box_h+32, "most peers follow the pattern set by Interlock (Sub-model 5): their own id, own state, and a reference back to the Device they concern \u2014 Operator is the exception, minimal by design (Sub-model 1 \u00a75.2)", size=12, fill=MUTED, style="italic")
text(60, peer_row_y+peer_box_h+54, "PredictedEvent.state: Open | Confirmed | Dismissed | Expired \u00b7 ImprovementRecommendation.state: Proposed | UnderReview | Approved | Rejected | Applied", size=11.5, fill=SOFT, style="italic", family="Consolas, Menlo, monospace")

# ============================================================
# New panel: physicalRef — functional identity vs shared physical hardware
# ============================================================
p3_y = peer_row_y + peer_box_h + 100
line(60, p3_y-20, 1640, p3_y-20, stroke=LINE, sw=1)
text(60, p3_y+10, "physicalRef \u2014 One Physical Asset, Many Functional Roles", size=19, weight=700, fill=INK)
text(60, p3_y+32, "optional on Device \u2014 targets whichever unit is actually shared: the Device itself, or one Component inside it", size=12.5, fill=SOFT)

attr_x, attr_y, attr_w = 60, p3_y+62, 640
rrect(attr_x, attr_y, attr_w, 74, stroke=NAVY, sw=2, rx=8)
text(attr_x+18, attr_y+28, "Device {", size=13, fill=MUTED, family="Consolas, Menlo, monospace")
text(attr_x+18, attr_y+50, "  physicalRef : DeviceRef | ComponentRef | null", size=12, fill=RED, weight=700, family="Consolas, Menlo, monospace")
text(attr_x+18, attr_y+68, "}", size=13, fill=MUTED, family="Consolas, Menlo, monospace")

oop_x = attr_x + attr_w + 40
rrect(oop_x, attr_y, 940, 74, stroke=BLUE, sw=1.6, rx=8, fill="#FFFFFF")
text(oop_x+18, attr_y+22, "cf. OOP: the Proxy / Flyweight pattern \u2014 several instances, each with their own identity, sharing one implementation", size=11.5, fill=MUTED, style="italic")
text(oop_x+18, attr_y+40, "single-CPU rack \u2192 physicalRef targets the Device itself, one shared asset for every role", size=11.5, fill=MUTED, style="italic")
text(oop_x+18, attr_y+58, "omitted \u2192 the instance is assumed to be its own unique physical device", size=11.5, fill=SOFT, style="italic")

# one combined illustration: a rack with two independent CPU components
rack_x, rack_y, rack_w, rack_h = 610, attr_y+74+40, 480, 110
rrect(rack_x, rack_y, rack_w, rack_h, stroke=SOFT, sw=1.6, rx=8, dash="5,4")
text(rack_x+rack_w/2, rack_y+20, "Device: PLC-Rack-04", size=12, weight=700, fill=SOFT, anchor="middle", family="Consolas, Menlo, monospace")

cpu_w = 190
cpuA_x = rack_x + 25
cpuB_x = rack_x + rack_w - 25 - cpu_w
cpu_y = rack_y + 38
for cx, label in [(cpuA_x, "CPU-A : Processor"), (cpuB_x, "CPU-B : Processor")]:
    rrect(cx, cpu_y, cpu_w, 56, stroke=NAVY, sw=1.8, rx=7, fill="#FFFFFF")
    text(cx+cpu_w/2, cpu_y+22, label, size=11, weight=700, fill=NAVY, anchor="middle", family="Consolas, Menlo, monospace")
    text(cx+cpu_w/2, cpu_y+40, "\u00ababstract\u00bb Component", size=9, fill=SOFT, anchor="middle", style="italic")

tag2_y = rack_y + rack_h + 55
tag2_positions = [
    ("PressureLoop-3.CU", 200, cpuA_x+cpu_w/2, "physicalRef \u2192 CPU-A"),
    ("TempLoop-7.CU", 780, cpuA_x+cpu_w/2, "physicalRef \u2192 CPU-A"),
    ("MeshNode-B.CU", 1360, cpuB_x+cpu_w/2, "physicalRef \u2192 CPU-B"),
]
for label, x, target_x, sublabel in tag2_positions:
    rrect(x, tag2_y, 260, 52, stroke=NAVY, sw=1.8, rx=7, fill="#FFFFFF")
    text(x+130, tag2_y+22, label, size=12, weight=700, fill=NAVY, anchor="middle", family="Consolas, Menlo, monospace")
    text(x+130, tag2_y+39, sublabel, size=9.5, fill=SOFT, anchor="middle")
    path(f"M {x+130} {tag2_y} C {x+130} {(cpu_y+56+tag2_y)/2}, {target_x} {(cpu_y+56+tag2_y)/2}, {target_x} {cpu_y+56}",
         stroke=RED, sw=1.6, dash="4,3", marker_end="tri-red")

text(60, tag2_y+72, "multi-CPU rack \u2192 physicalRef targets the specific Processor Component: two loops share CPU-A (patching it affects both together), one runs on independent CPU-B", size=12, fill=MUTED, style="italic")
text(60, tag2_y+92, "each Processor Component still has its own id (Sub-model 1) \u2014 \u201cnot independently addressable\u201d means not reachable directly on the network, not \u201cwithout identity\u201d", size=11.5, fill=SOFT, style="italic")

integ_y = tag2_y + 128
rrect(60, integ_y, 1580, 60, stroke=GREEN, sw=2, rx=8, fill="#FFFFFF")
text(84, integ_y+24, "confirms Sub-model 3's Integrated shape:", size=13, weight=700, fill=GREEN)
text(84, integ_y+44, "when every role in one Assembly's chain (S\u2192T\u2192CU\u2192SC\u2192A) shares the same physicalRef, that IS what \u201cIntegrated\u201d means \u2014 now checkable, not just assumed", size=11.5, fill=MUTED)

final_h = int(integ_y + 60 + 55)
parts.append("</svg>")

svg = "\n".join(parts)
svg = svg.replace(f'viewBox="0 0 {W} {H}" width="{W}" height="{H}"', f'viewBox="0 0 {W} {final_h}" width="{W}" height="{final_h}"')
svg = svg.replace(f'<rect width="{W}" height="{H}" fill="{BG}"/>', f'<rect width="{W}" height="{final_h}" fill="{BG}"/>')
svg = svg.replace(f'<rect width="{W}" height="{H}" fill="url(#grid5)"/>', f'<rect width="{W}" height="{final_h}" fill="url(#grid5)"/>')

svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg

with open("./lunex-object-model.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("done", final_h)
