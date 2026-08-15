#!/usr/bin/env python3
"""
build_pdf.py — builds LUNEX-Specification.pdf from LUNEX-Specification.md
in a single command.

Requires: pandoc, wkhtmltopdf (system binaries), and the Python packages
beautifulsoup4, pikepdf, Pillow, playwright (with `playwright install chromium`
run once beforehand).

Expected layout when running this script:

  repo-root/
    LUNEX-Specification.md
    diagrams/                  <- the 16 .svg files referenced by the spec
    tools/pdf/build_pdf.py     <- this script

Usage (from repo root):
    python3 tools/pdf/build_pdf.py

Output: LUNEX-Specification.pdf, written to the repo root.

What this does, in order:
  1. Rasterizes each referenced diagrams/*.svg to a quantized PNG.
     (wkhtmltopdf's SVG marker support is unreliable for arrowheads —
     rasterizing sidesteps that entirely; see PROJECT-RECORD.md, Phase 6.)
  2. Inserts each PNG into the markdown right after its `*Diagram: ...*` line.
  3. Converts markdown -> HTML via pandoc.
  4. Fixes the hand-written table-of-contents links to pandoc's actual
     generated heading ids.
  5. Wraps every top-level heading together with its diagram (if any) in one
     DOM node, and every subsection heading together with its first block of
     content, so page breaks can never separate a heading from what follows
     it. (Done with BeautifulSoup, not regex — see PROJECT-RECORD.md, Phase 6,
     for why a regex-based version of this step previously failed silently.)
  6. Wraps the result in a styled HTML shell (title page + CSS) and renders
     to PDF with wkhtmltopdf.
  7. Recompresses embedded images as JPEG via pikepdf to bring the file size
     down (typically 20MB+ -> ~7MB with no visible quality loss).

If a diagram's heading+content still doesn't fit on one page after an edit,
the diagram itself is very likely too tall (>~2300-2400px at the widths used
elsewhere in this repo) — shorten the diagram rather than fighting the PDF
renderer further. See PROJECT-RECORD.md for the reasoning.
"""

import io
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image
import pikepdf
from pikepdf import Name
from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_MD = REPO_ROOT / "LUNEX-Specification.md"
DIAGRAMS_DIR = REPO_ROOT / "diagrams"
BUILD_DIR = REPO_ROOT / ".pdfbuild"
OUTPUT_PDF = REPO_ROOT / "LUNEX-Specification.pdf"

DIAGRAM_RE = re.compile(r"\*Diagram: `([a-z0-9-]+\.svg)`\*")


def log(msg):
    print(f"[build_pdf] {msg}")


def rasterize_diagrams(svg_names):
    BUILD_DIR.mkdir(exist_ok=True)
    png_dir = BUILD_DIR / "diagrams_png"
    png_dir.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name in svg_names:
            svg_path = DIAGRAMS_DIR / name
            if not svg_path.exists():
                log(f"WARNING: {svg_path} not found, skipping")
                continue
            svg = svg_path.read_text(encoding="utf-8")
            m = re.search(r'width="(\d+)"\s+height="(\d+)"', svg)
            w, h = int(m.group(1)), int(m.group(2))
            html = f'<!DOCTYPE html><html><head><style>*{{margin:0;padding:0;}}</style></head><body>{svg}</body></html>'
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1.4)
            page.set_content(html)
            png_path = png_dir / name.replace(".svg", ".png")
            page.locator("svg").screenshot(path=str(png_path))
            page.close()

            # Palette-quantize: these diagrams use few flat colors and
            # compress far better as indexed PNGs than as raw RGB.
            img = Image.open(png_path).convert("RGB")
            img_p = img.quantize(colors=64, method=Image.MEDIANCUT)
            img_p.save(png_path, optimize=True)
        browser.close()
    log(f"rasterized {len(svg_names)} diagrams")
    return png_dir


def insert_diagram_images(spec_text, png_dir_rel):
    def repl(m):
        filename = m.group(1)
        pngname = filename.replace(".svg", ".png")
        return f'{m.group(0)}\n\n<div class="diagram-embed">\n\n![{filename}]({png_dir_rel}/{pngname})\n\n</div>'

    new_text, n = DIAGRAM_RE.subn(repl, spec_text)
    log(f"inserted {n} diagram references")
    return new_text


def run_pandoc(md_path, html_path):
    subprocess.run(
        ["pandoc", str(md_path), "-f", "markdown", "-t", "html", "-o", str(html_path)],
        check=True,
    )


def fix_toc_links(html):
    heading_re = re.compile(r'<h2 id="([^"]+)">(.*?)</h2>', re.DOTALL)
    id_map = {}
    for m in heading_re.finditer(html):
        hid, text = m.group(1), m.group(2)
        clean = re.sub(r"<[^>]+>", "", text).strip()
        id_map[clean] = hid

    toc_link_re = re.compile(r'<a href="#[^"]+">(.*?)</a>', re.DOTALL)

    def repl(m):
        link_text = re.sub(r"<[^>]+>", " ", m.group(1))
        link_text = re.sub(r"\s+", " ", link_text).strip()
        for text, hid in id_map.items():
            norm = re.sub(r"^\d+\.\s*", "", text).strip()
            if link_text == norm or link_text in norm or norm in link_text:
                return f'<a href="#{hid}">{m.group(1)}</a>'
        return m.group(0)

    return toc_link_re.sub(repl, html)


def wrap_chapters_with_diagrams(html):
    """Pair each h2 heading with its `*Diagram:*` caption and image (if any)
    as one atomic DOM node, so a page break can never separate them. Plain
    h2 sections (no diagram) get a marker class instead, so they still start
    a fresh page on their own."""
    soup = BeautifulSoup(html, "html.parser")
    n_with_diagram = n_plain = 0

    for h2 in soup.find_all("h2"):
        next_el = h2.find_next_sibling()
        if (
            next_el is not None
            and next_el.name == "p"
            and next_el.find("em")
            and next_el.em
            and "Diagram:" in next_el.em.get_text()
        ):
            diagram_div = next_el.find_next_sibling()
            if (
                diagram_div is not None
                and diagram_div.name == "div"
                and "diagram-embed" in (diagram_div.get("class") or [])
            ):
                wrapper = soup.new_tag("div")
                wrapper["class"] = "chapter-with-diagram"
                h2.insert_before(wrapper)
                wrapper.append(h2.extract())
                wrapper.append(next_el.extract())
                wrapper.append(diagram_div.extract())
                n_with_diagram += 1
                continue
        h2["class"] = (h2.get("class") or []) + ["chapter-no-diagram"]
        n_plain += 1

    log(f"wrapped {n_with_diagram} chapter+diagram headings, {n_plain} plain headings")
    return str(soup)


def wrap_subsections(html):
    """Pair each h3 with its immediately following block so a subsection
    heading can never be stranded at the bottom of a page without its
    content."""
    soup = BeautifulSoup(html, "html.parser")
    n = 0
    for h3 in soup.find_all("h3"):
        next_el = h3.find_next_sibling()
        if next_el is None:
            continue
        wrapper = soup.new_tag("div")
        wrapper["class"] = "keep-together"
        h3.insert_before(wrapper)
        wrapper.append(h3.extract())
        wrapper.append(next_el.extract())
        n += 1
    log(f"wrapped {n} subsection headings")
    return str(soup)


CSS = """
@page { margin: 22mm 20mm 22mm 20mm; }
body { font-family: 'Helvetica Neue', Arial, sans-serif; color: #16202B; font-size: 10.3pt; line-height: 1.55; }
h1 { color: #1F3B57; font-size: 24pt; border-bottom: 3px solid #2F6F9E; padding-bottom: 10px; margin-top: 0; }
h2 { color: #1F3B57; font-size: 15pt; margin-top: 30px; padding-top: 6px; border-top: 1px solid #D6DEE7; }
.chapter-with-diagram { page-break-before: always; }
.chapter-no-diagram { page-break-before: always; }
h3 { color: #2F6F9E; font-size: 12pt; margin-top: 18px; }
h4 { color: #2E7D4F; font-size: 10.5pt; }
.keep-together { page-break-inside: avoid; }
p { margin: 8px 0; text-align: justify; }
strong { color: #1F3B57; }
code { font-family: 'Consolas','Menlo',monospace; background: #F1F4F7; padding: 1px 4px; border-radius: 3px; font-size: 9pt; color: #B3402F; }
pre { background: #F8F9FB; border: 1px solid #D6DEE7; border-left: 3px solid #2F6F9E; border-radius: 4px; padding: 10px 14px; font-size: 8.7pt; overflow-x: auto; page-break-inside: avoid; }
pre code { background: none; color: #16202B; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 9pt; page-break-inside: avoid; }
th { background: #1F3B57; color: #FFFFFF; text-align: left; padding: 6px 8px; font-size: 8.7pt; }
td { border-bottom: 1px solid #E6EBF0; padding: 5px 8px; vertical-align: top; }
tr:nth-child(even) td { background: #FBFAF8; }
blockquote { border-left: 3px solid #2E7D4F; margin: 10px 0; padding: 4px 16px; color: #33404D; font-style: italic; background: #F8FBF9; }
hr { border: none; border-top: 1px solid #D6DEE7; margin: 22px 0; }
a { color: #2F6F9E; text-decoration: none; }
ul, ol { margin: 6px 0; padding-left: 24px; }
li { margin: 3px 0; }
em { color: #5A6B7B; }
.diagram-embed { margin: 14px 0 22px 0; }
.diagram-embed img { width: 100%; height: auto; border: 1px solid #D6DEE7; border-radius: 6px; display: block; }
.titlepage { text-align: center; padding-top: 26mm; page-break-after: always; }
.titlepage .kicker { color: #5A6B7B; letter-spacing: 3px; font-size: 11pt; text-transform: uppercase; }
.titlepage h1 { font-size: 42pt; border: none; margin: 14px 0 6px 0; }
.titlepage .sub { font-size: 13pt; color: #33404D; max-width: 420px; margin: 0 auto 30px auto; }
.titlepage .meta { margin-top: 60px; color: #5A6B7B; font-size: 10pt; }
.titlepage .swatch { display: inline-block; width: 60px; height: 6px; background: #2E7D4F; margin: 20px 0; }
"""

TITLEPAGE = """
<div class="titlepage">
  <div class="kicker">LUNEX &mdash; VERSION 0.1 &mdash; DRAFT</div>
  <h1>LUNEX</h1>
  <div class="swatch"></div>
  <div class="sub">A unified, object-oriented reference model for operational technology, safety, security, and AI.</div>
  <div class="meta">lunex.cloud<br/>Sixteen sub-models &middot; Full specification, with diagrams</div>
</div>
"""


def wrap_full_html(body):
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{TITLEPAGE}{body}</body></html>'


def run_wkhtmltopdf(html_path, pdf_path):
    subprocess.run(
        [
            "wkhtmltopdf",
            "--enable-local-file-access",
            "--margin-top", "22", "--margin-bottom", "22",
            "--margin-left", "20", "--margin-right", "20",
            str(html_path), str(pdf_path),
        ],
        check=True,
    )


def recompress_images(pdf_path, out_path, quality=82):
    pdf = pikepdf.Pdf.open(pdf_path)
    count = 0
    for page in pdf.pages:
        if "/Resources" not in page or "/XObject" not in page["/Resources"]:
            continue
        for key in list(page["/Resources"]["/XObject"].keys()):
            obj = page["/Resources"]["/XObject"][key]
            if obj.get("/Subtype") != Name("/Image"):
                continue
            try:
                pil_img = Image.open(io.BytesIO(obj.read_bytes()))
            except Exception:
                try:
                    pil_img = pikepdf.PdfImage(obj).as_pil_image()
                except Exception:
                    continue
            buf = io.BytesIO()
            pil_img.convert("RGB").save(buf, format="JPEG", quality=quality, optimize=True)
            obj.write(buf.getvalue(), filter=Name("/DCTDecode"))
            obj["/ColorSpace"] = Name("/DeviceRGB")
            obj["/BitsPerComponent"] = 8
            count += 1
    pdf.save(out_path, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)
    log(f"recompressed {count} embedded images")


def main():
    if not SPEC_MD.exists():
        sys.exit(f"ERROR: {SPEC_MD} not found. Run this script from inside the repo.")

    BUILD_DIR.mkdir(exist_ok=True)
    spec_text = SPEC_MD.read_text(encoding="utf-8")
    svg_names = DIAGRAM_RE.findall(spec_text)

    rasterize_diagrams(svg_names)

    spec_with_images = insert_diagram_images(spec_text, png_dir_rel="diagrams_png")
    spec_md_tmp = BUILD_DIR / "spec_with_images.md"
    spec_md_tmp.write_text(spec_with_images, encoding="utf-8")

    html_path = BUILD_DIR / "spec.html"
    run_pandoc(spec_md_tmp, html_path)

    html = html_path.read_text(encoding="utf-8")
    html = fix_toc_links(html)
    html = wrap_chapters_with_diagrams(html)
    html = wrap_subsections(html)
    full_html_path = BUILD_DIR / "spec_final.html"
    full_html_path.write_text(wrap_full_html(html), encoding="utf-8")

    raw_pdf = BUILD_DIR / "spec_raw.pdf"
    run_wkhtmltopdf(full_html_path, raw_pdf)

    recompress_images(raw_pdf, OUTPUT_PDF)

    log(f"done -> {OUTPUT_PDF} ({OUTPUT_PDF.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
