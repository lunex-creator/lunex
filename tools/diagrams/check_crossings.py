#!/usr/bin/env python3
import re, sys, math

def parse_rects(svg):
    rects = []
    for m in re.finditer(r'<rect x="([\-\d.]+)" y="([\-\d.]+)" width="([\-\d.]+)" height="([\-\d.]+)"[^>]*fill="([^"]*)"', svg):
        x, y, w, h, fill = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(5)
        rects.append((x, y, w, h, fill))
    return rects

def parse_lines(svg):
    segs = []
    for m in re.finditer(r'<line x1="([\-\d.]+)" y1="([\-\d.]+)" x2="([\-\d.]+)" y2="([\-\d.]+)"', svg):
        x1,y1,x2,y2 = map(float, m.groups())
        segs.append([(x1,y1),(x2,y2)])
    return segs

def sample_bezier_q(p0,p1,p2,n=20):
    pts=[]
    for i in range(n+1):
        t=i/n
        x=(1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t**2*p2[0]
        y=(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t**2*p2[1]
        pts.append((x,y))
    return pts

def sample_bezier_c(p0,p1,p2,p3,n=25):
    pts=[]
    for i in range(n+1):
        t=i/n
        x=(1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t**2*p2[0]+t**3*p3[0]
        y=(1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t**2*p2[1]+t**3*p3[1]
        pts.append((x,y))
    return pts

def parse_paths(svg):
    all_polylines = []
    for m in re.finditer(r'<path d="([^"]+)"[^>]*stroke="(#[0-9A-Fa-f]{6})"', svg):
        d = m.group(1)
        tokens = re.findall(r'[MLQC]|-?\d+\.?\d*', d)
        pts = []
        i = 0
        cur = None
        cmd = None
        while i < len(tokens):
            t = tokens[i]
            if t in ('M','L','Q','C'):
                cmd = t
                i += 1
                continue
            if cmd == 'M':
                x,y = float(tokens[i]), float(tokens[i+1])
                cur = (x,y)
                pts.append(cur)
                i += 2
            elif cmd == 'L':
                x,y = float(tokens[i]), float(tokens[i+1])
                cur = (x,y)
                pts.append(cur)
                i += 2
            elif cmd == 'Q':
                cx,cy,x,y = float(tokens[i]),float(tokens[i+1]),float(tokens[i+2]),float(tokens[i+3])
                pts.extend(sample_bezier_q(cur,(cx,cy),(x,y))[1:])
                cur = (x,y)
                i += 4
            elif cmd == 'C':
                c1x,c1y,c2x,c2y,x,y = [float(tokens[i+k]) for k in range(6)]
                pts.extend(sample_bezier_c(cur,(c1x,c1y),(c2x,c2y),(x,y))[1:])
                cur = (x,y)
                i += 6
            else:
                i += 1
        if len(pts) >= 2:
            all_polylines.append(pts)
    return all_polylines

def polyline_from_line(seg, n=30):
    (x1,y1),(x2,y2) = seg
    return [(x1+(x2-x1)*i/n, y1+(y2-y1)*i/n) for i in range(n+1)]

def check_file(path):
    with open(path, encoding='utf-8') as f:
        svg = f.read()
    rects = parse_rects(svg)
    # only medium-sized "card/box" rects, white-ish fill, to avoid flagging huge panels or the bg
    card_rects = [(x,y,w,h) for (x,y,w,h,fill) in rects if 25 <= w <= 750 and 15 <= h <= 450 and fill.upper() in ('#FFFFFF',)]

    polylines = []
    for seg in parse_lines(svg):
        polylines.append(polyline_from_line(seg))
    polylines.extend(parse_paths(svg))

    issues = []
    for poly in polylines:
        n = len(poly)
        if n < 2:
            continue
        # skip first/last 12% of points (near the line's own endpoints/boxes)
        skip = max(1, int(n*0.12))
        mid_pts = poly[skip: n-skip] if n - 2*skip > 0 else poly
        for (px,py) in mid_pts:
            for (rx,ry,rw,rh) in card_rects:
                if rx+3 < px < rx+rw-3 and ry+3 < py < ry+rh-3:
                    issues.append((px,py,rx,ry,rw,rh))
                    break
    return issues, len(card_rects), len(polylines)

if __name__ == "__main__":
    import glob
    files = sorted(glob.glob("./lunex-*.svg"))
    for f in files:
        try:
            issues, nrects, npoly = check_file(f)
        except Exception as e:
            print(f"{f}: ERROR {e}")
            continue
        tag = "ISSUES" if issues else "clean"
        print(f"{f.split('/')[-1]:40s} rects={nrects:3d} lines={npoly:3d}  ->  {tag} ({len(issues)} sample hits)")
        if issues:
            # cluster/report a few unique rect hits
            seen = set()
            for (px,py,rx,ry,rw,rh) in issues:
                key = (round(rx),round(ry))
                if key not in seen:
                    seen.add(key)
                    print(f"    crosses rect at ({rx:.0f},{ry:.0f},{rw:.0f}x{rh:.0f}) near point ({px:.0f},{py:.0f})")
