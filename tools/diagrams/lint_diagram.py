#!/usr/bin/env python3
"""Lint a LUNEX SVG diagram: text overflowing its box, text-on-text overlap,
arrows whose end does not touch a box edge. Usage: lint_diagram.py file.svg [...]"""
import sys
from playwright.sync_api import sync_playwright

JS = r"""
() => {
  const svg = document.querySelector('svg');
  const rects = [...svg.querySelectorAll('rect')].filter(r => r.getAttribute('fill') !== 'url(#grid5)' && r.getAttribute('width') < 1500 && r.getAttribute('height') > 20)
    .map(r => ({x:+r.getAttribute('x'), y:+r.getAttribute('y'), w:+r.getAttribute('width'), h:+r.getAttribute('height')}))
    .filter(r => r.w>30 && r.h>20);
  const texts = [...svg.querySelectorAll('text')].map(t => {const b=t.getBBox(); return {s:t.textContent.trim().slice(0,50), x:b.x, y:b.y, w:b.width, h:b.height};}).filter(t=>t.s);
  const arrows = [], polys = [];
  svg.querySelectorAll('line,path').forEach(e => {
    let pts=[];
    if (e.tagName==='line') pts=[[+e.getAttribute('x1'),+e.getAttribute('y1')],[+e.getAttribute('x2'),+e.getAttribute('y2')]];
    else if (e.getTotalLength) { const L=e.getTotalLength(); if (L<5) return; for(let i=0;i<=40;i++){const q=e.getPointAtLength(L*i/40); pts.push([q.x,q.y]);} }
    if (pts.length<2) return;
    const hasM = (e.getAttribute('marker-end')||'').length>0;
    if (hasM) arrows.push({end:pts[pts.length-1], start:pts[0]});
    if (e.tagName==='line' && pts.length===2) { const [a,b]=pts; const n=30; pts=[]; for(let i=0;i<=n;i++) pts.push([a[0]+(b[0]-a[0])*i/n, a[1]+(b[1]-a[1])*i/n]); }
    polys.push({pts, arrow:hasM});
  });
  return {rects, texts, arrows, polys};
}
"""

def lint(path):
    svg = open(path, encoding='utf-8').read().split('?>', 1)[-1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = b.new_page(viewport={'width': 1700, 'height': 900})
        pg.route('http*://**', lambda r: r.abort())
        pg.set_content('<html><body style="margin:0">' + svg + '</body></html>')
        d = pg.evaluate(JS)
        b.close()
    rects, texts, arrows, polys = d['rects'], d['texts'], d['arrows'], d['polys']
    rects = [r for r in rects if not (r['x']==0 and r['y']==0)]
    maxy = max(r['y']+r['h'] for r in rects)
    issues = []
    for t in texts:
        cx, cy = t['x'] + 4, t['y'] + t['h'] / 2
        host = [r for r in rects if r['x'] <= cx <= r['x'] + r['w'] and r['y'] <= cy <= r['y'] + r['h']]
        if not host: continue
        r = min(host, key=lambda r: r['w'] * r['h'])
        if t['x'] + t['w'] > r['x'] + r['w'] - 3 or t['y'] + t['h'] > r['y'] + r['h'] + 1:
            issues.append(f"OVERFLOW text '{t['s']}' ({t['x']:.0f},{t['y']:.0f},w{t['w']:.0f}) leaves box ({r['x']:.0f},{r['y']:.0f},{r['w']:.0f}x{r['h']:.0f})")
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, c = texts[i], texts[j]
            ox = min(a['x'] + a['w'], c['x'] + c['w']) - max(a['x'], c['x'])
            oy = min(a['y'] + a['h'], c['y'] + c['h']) - max(a['y'], c['y'])
            if ox > 3 and oy > 4:
                issues.append(f"TEXT-OVERLAP '{a['s']}' / '{c['s']}'")
    def edgedist(x, y):
        best = 1e9
        for r in rects:
            ex, ey = max(r['x'], min(x, r['x'] + r['w'])), max(r['y'], min(y, r['y'] + r['h']))
            dd = ((ex - x) ** 2 + (ey - y) ** 2) ** .5
            if r['x'] < x < r['x'] + r['w'] and r['y'] < y < r['y'] + r['h']:
                dd = min(abs(x - r['x']), abs(x - r['x'] - r['w']), abs(y - r['y']), abs(y - r['y'] - r['h']))
            best = min(best, dd)
        return best
    for a_ in arrows:
        x, y = a_['end']
        if y > maxy: continue
        dd = edgedist(x, y)
        if dd > 4:
            issues.append(f"ARROW-END ({x:.0f},{y:.0f}) is {dd:.0f}px from any box edge")
    seen = set()
    for pl in polys:
        if pl['pts'][0][1] > maxy: continue
        for (x, y) in pl['pts']:
            for t in texts:
                if t['x'] + 1 < x < t['x'] + t['w'] - 1 and t['y'] + 2 < y < t['y'] + t['h'] - 2:
                    key = (t['s'], round(x/20), round(y/20))
                    if t['s'] not in seen:
                        seen.add(t['s'])
                        issues.append(f"LINE-THROUGH-TEXT '{t['s']}' at ({x:.0f},{y:.0f})")
    return issues

if __name__ == '__main__':
    for f in sys.argv[1:]:
        iss = lint(f)
        print(f"== {f}: {len(iss)} issues")
        for i in iss: print("  ", i)
