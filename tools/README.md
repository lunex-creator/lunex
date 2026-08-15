# LUNEX Build Tools

Everything needed to regenerate the diagrams and the PDF from source, so LUNEX stays a living document rather than a set of files nobody but the original author can update.

## `diagrams/`

One Python script per diagram (`build_*.py`), each producing the corresponding `diagrams/lunex-*.svg`. Pure Python — no dependencies beyond the standard library.

```bash
cd diagrams/            # repo's diagrams/ folder, where you want the .svg output
python3 ../tools/diagrams/build_object_model.py
python3 ../tools/diagrams/build_hierarchy.py
# ...etc for each sub-model
```

Each script writes its output SVG to the current working directory — run them from inside the repo's `diagrams/` folder (or adjust the output filename at the bottom of the script).

**One shared dependency**: `build_state.py`, `build_safety.py`, and `build_ai_control.py` all read `state_machine_fragment.svg` (included in this folder) — the Sub-model 4 state machine is drawn once and transplanted into all three diagrams, so a correction to the state machine only ever needs to happen in one place. Copy `state_machine_fragment.svg` alongside whichever script you're running.

`check_crossings.py` is a standalone QA utility — point it at a generated SVG to detect line/box overlaps missed by eye:

```bash
python3 check_crossings.py path/to/diagram.svg
```

## `pdf/build_pdf.py`

Builds `LUNEX-Specification.pdf` from `LUNEX-Specification.md` in one command.

**Requirements**:
- System binaries: `pandoc`, `wkhtmltopdf`
- Python packages: `beautifulsoup4`, `pikepdf`, `Pillow`, `playwright` (run `playwright install chromium` once)

**Usage**, from the repo root:

```bash
python3 tools/pdf/build_pdf.py
```

Expects `LUNEX-Specification.md` and a populated `diagrams/` folder at the repo root; writes `LUNEX-Specification.pdf` back to the repo root. Intermediate build files go into `.pdfbuild/` (safe to delete, safe to `.gitignore`).

See the docstring at the top of `build_pdf.py` for what each step does and why — most of the steps exist because of a specific bug found the hard way (wrong arrow orientation, headings stranded across page breaks). The full story is in `docs/PROJECT-RECORD.md`, Phase 6.

**If a diagram+heading pairing breaks again after an edit**: it's very likely the diagram grew taller than the practical single-page budget (~2300–2400px at the widths used elsewhere in this repo). Shorten the diagram rather than fighting the PDF renderer further — see `PROJECT-RECORD.md` for why.
