# LUNEX GitHub Repository — Maintenance Guide

**Scope of this document**: the repository at `github.com/lunex-creator/lunex` — its layout, what every file is for, and the workflow for changing things without breaking cross-references. For the website, see `WEBSITE-GUIDE.md`. For LinkedIn, see `LINKEDIN-GUIDE.md`.

---

## 1. Full repository layout

```
lunex/
├── README.md
├── LICENSE                    (CC BY 4.0)
├── CHANGELOG.md
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── SECURITY.md
├── INDEX.md
├── LUNEX-Specification.md
├── LUNEX-Specification.pdf
├── docs/
│   └── PROJECT-RECORD.md
├── diagrams/                  (16 .svg files, one per sub-model)
├── brand/
│   ├── lunex-logo-light.svg / .png
│   ├── lunex-logo-dark.svg / .png
│   └── lunex-brand-concept.svg
├── tools/
│   ├── README.md
│   ├── diagrams/               (16 build_*.py scripts + shared fragment)
│   └── pdf/build_pdf.py
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   ├── documentation_correction.md
    │   └── config.yml
    └── PULL_REQUEST_TEMPLATE.md
```

---

## 2. What every top-level file is for

| File | Purpose | Update it when... |
|---|---|---|
| `README.md` | The landing page for the repository — what LUNEX is, links to everything else | Any of the linked documents' purpose changes, a sub-model title changes, a new top-level file is added |
| `LICENSE` | CC BY 4.0 full text | Never (unless the license itself changes, which would be a major decision) |
| `CHANGELOG.md` | Notable changes, Keep-a-Changelog style, terse | Every model-level change (new/changed field, corrected error). Not for website-only or purely cosmetic changes — see its own header note |
| `CITATION.cff` | Machine-readable citation metadata (powers GitHub's "Cite this repository" button) | Version number changes, author changes |
| `CODE_OF_CONDUCT.md` | Community behavior standard, Contributor-Covenant-based | Rarely — only if the reporting email changes or enforcement process changes |
| `CONTRIBUTING.md` | How to propose changes; Discussions vs. Issues distinction | If the contribution workflow itself changes |
| `SECURITY.md` | How to report a vulnerability in `tools/` scripts | If the reporting email or scope changes |
| `INDEX.md` | Narrative one-paragraph-per-sub-model overview, for readers who want the reasoning without reading the full 50-page spec | Every time a sub-model's schema, title, or key behavior changes — this is the file most likely to go stale, since it duplicates information that also lives in the full specification |
| `LUNEX-Specification.md` | The actual technical specification — the source of truth | Every model change. This is the file everything else (Appendix A, `INDEX.md`, diagrams, `README.md`'s table) must stay consistent with |
| `LUNEX-Specification.pdf` | Generated, formatted copy of the above | Regenerate via `tools/pdf/build_pdf.py` any time `LUNEX-Specification.md` or a diagram changes — never hand-edit the PDF |

**`lunex-index.md`** (lowercase, no path prefix) is a duplicate of `INDEX.md`, kept byte-identical, for a historical reason (an early file-naming inconsistency that was easier to keep mirrored than to fully deprecate one). **Whenever you edit `INDEX.md`, copy it over `lunex-index.md` immediately** — do not let them drift; several past sessions found and fixed drift between these two.

---

## 3. `docs/PROJECT-RECORD.md` — the project's memory

This is not a technical reference — it's the chronological and topical record of *why* the model is the way it is: every decision, every correction, every reconsidered-and-reverted choice, with the reasoning spelled out. It has two parts:

- **Part 1 — Chronological Record**: phases, in order, narrating what happened and why.
- **Part 2 — Decisions Register**: the same decisions, indexed by topic (Object Model, Safety, Alarm Management, etc.) as a quick-lookup table — question asked → what was decided → why.

**Update this file whenever a design decision is made or reconsidered** — not just successful additions, but reversals too (see Phase 9 in the file itself for the template: a decision was made, later found to be over-applying a principle, and reverted — documented as a distinct phase rather than silently undone). A decision that isn't recorded here will very likely need to be re-litigated from scratch the next time someone (human or AI) picks up the project, because the reasoning exists only in a chat transcript otherwise.

**A copy exists as `PROJECT-RECORD.md`** at the point of delivery from past sessions, identical in content to `docs/PROJECT-RECORD.md` — same mirroring situation as `INDEX.md`/`lunex-index.md`. Keep only the `docs/PROJECT-RECORD.md` copy in the actual repository; the root-level duplicate was a delivery artifact, not an intentional second file to maintain going forward.


---

## 4. `diagrams/` and `tools/diagrams/` — how the visuals are maintained

Every SVG in `diagrams/` is **generated output**, not a hand-edited file. Each has a corresponding Python script in `tools/diagrams/` (e.g. `diagrams/lunex-safety-model.svg` ← `tools/diagrams/build_safety.py`). **Never hand-edit an SVG in `diagrams/` directly** — any manual fix will be silently lost the next time someone regenerates it from the script, and worse, the script and the shipped SVG will now disagree about what the diagram should look like.

### Running a script

```bash
cd diagrams/
python3 ../tools/diagrams/build_safety.py
```

Each script writes its output to the current working directory, so run it from inside `diagrams/`. Pure Python, no dependencies beyond the standard library — that was a deliberate constraint so these scripts stay runnable years from now without a fragile dependency chain.

### The one shared dependency

`build_state.py`, `build_safety.py`, and `build_ai_control.py` all read `tools/diagrams/state_machine_fragment.svg` — the Sub-model 4 state machine is drawn once and transplanted into all three diagrams (a "shared fragment" pattern), so a correction to the state machine only has to happen in one place and then gets re-rendered into three outputs.

**This file will show a parse error if you try to open it directly as a standalone SVG.** That's expected, not a bug: it deliberately has no `<svg>` root element, because the three scripts above paste it as a raw text fragment inside their *own* `<svg>`/`<g>` context. Wrapping it in its own `<svg>` tag to "fix" the parse error would break the coordinate/transform system in all three consuming scripts. See `tools/README.md` for the full explanation — this exact confusion has come up before.

### `check_crossings.py`

A standalone QA script — point it at any generated SVG to detect line/box overlaps that are easy to miss by eye:

```bash
python3 tools/diagrams/check_crossings.py diagrams/lunex-object-model.svg
```

### Diagram height budget — a real, recurring constraint

Every diagram gets embedded into the PDF, and each one needs to fit on a single printed page alongside its heading and caption. Through repeated trial and error, the practical ceiling turned out to be **roughly 2300–2400px tall** at the widths used throughout this project (1500–1700px wide). Exceed that and the PDF build (§5) will separate the heading from the diagram across a page break — a bug that recurred multiple times before this constraint was written down. **If an edit to a `build_*.py` script pushes a diagram's computed height past this range, shrink the content (tighter spacing, a more compact sub-panel) rather than letting it grow — don't discover this the hard way by rebuilding the PDF and finding a page-break bug.**

---

## 5. `tools/pdf/build_pdf.py` — regenerating the PDF

One command, run from the repository root:

```bash
python3 tools/pdf/build_pdf.py
```

**Requirements**: system binaries `pandoc` and `wkhtmltopdf`; Python packages `beautifulsoup4`, `pikepdf`, `Pillow`, `playwright` (run `playwright install chromium` once, first time only).

This single script replaces what used to be eight separate manual steps (image rasterization, markdown-to-HTML conversion, table-of-contents link repair, heading/diagram pairing, subsection pairing, PDF rendering, image recompression) — see the script's own docstring for what each internal step does and why. **Do not attempt to reconstruct the PDF pipeline manually** — the script exists specifically because the manual version was error-prone and several of its steps encode fixes for real, previously-encountered bugs (see the docstring's references to specific `PROJECT-RECORD.md` phases).

**When to run it**: any time `LUNEX-Specification.md` changes, or any diagram in `diagrams/` changes. The output (`LUNEX-Specification.pdf`) should be committed alongside the source change — don't let the PDF drift out of sync with the markdown.

**After running it**, verify — don't just trust that it worked:
1. Check the page count is what you'd expect (currently 51 pages; a change of a few pages after a small edit is normal, a change of 10+ pages after a one-line edit suggests something broke).
2. Scan for orphaned headings — a heading alone at the very bottom of a page with its content pushed to the next page. This project automated this check with a script that OCRs the bottom 12% of every page looking for a heading-shaped line with nothing after it; worth doing the same rather than manually reading 51 pages.
3. Spot-check that arrows/diagrams actually render (a past, now-fixed bug caused arrowheads to point the wrong way specifically in the PDF, invisible unless you looked at the actual rendered pages).

---

## 6. The complete workflow for a model change

This is the sequence that's been used consistently, in the order that avoids leaving something stale:

1. **Change `LUNEX-Specification.md`** — the schema, the prose explanation, the "Application Guidance" if relevant.
2. **Update Appendix A** in the same file — it's written separately from each sub-model's own section, so a schema change must be applied in both places. This is the single most common thing to forget.
3. **Update the glossary** (also in `LUNEX-Specification.md`) if a new term or attribute was introduced.
4. **Update the corresponding `tools/diagrams/build_*.py` script** and regenerate the SVG (§4) if the change affects what's visually shown.
5. **Check Sub-model 8's naming register** (`tools/diagrams/build_naming.py`) — if a term was renamed, or a naming decision was reconsidered, log it there, whether the outcome was a rename or a deliberate decision *not* to rename.
6. **Update `INDEX.md`** (and mirror to `lunex-index.md`) if the change affects the one-paragraph summary of that sub-model.
7. **Update `README.md`'s sub-model table** if the title or one-line description changed.
8. **Log the decision in `docs/PROJECT-RECORD.md`** — both the chronological narrative (Part 1) and, if it fits an existing table, the Decisions Register (Part 2).
9. **Add a line to `CHANGELOG.md`** under the current unreleased/draft version.
10. **Regenerate the PDF** (§5) and verify.

Skipping steps 2, 6, or 7 has happened before and produced real, user-visible inconsistencies (a schema shown correctly in one place and stale in another) — this checklist exists because of those specific incidents, not as a hypothetical precaution.


---

## 7. GitHub features configured on this repository

### Discussions (not Issues) for design conversation

Enabled under `Settings → General → Features → Discussions`. Categories: Announcements, Q&A, Critique & Gaps, Proposals, Show & Tell — see the pinned welcome post for the full rationale. **Design disagreement goes here, not into Issues.** This distinction is enforced not just by convention but technically: `.github/ISSUE_TEMPLATE/config.yml` sets `blank_issues_enabled: false` and redirects anyone opening a blank issue toward Discussions instead.

**Pinning a discussion** is not in repository Settings — it's a control inside the Discussion itself (open the discussion, look for a pin icon in the right-hand sidebar). Up to 4 discussions can be pinned globally, plus more per-category.

### Issue templates

Two templates (`bug_report.md`, `documentation_correction.md`) plus the `config.yml` redirect. Both templates explicitly tell the reporter when *not* to use them (a design disagreement) and point to Discussions instead — this was a deliberate choice to keep Issues reserved for concrete, actionable problems.

### Pull request template

`.github/PULL_REQUEST_TEMPLATE.md` includes a checklist that mirrors §6's workflow above (Appendix A updated? Diagram regenerated via script, not hand-edited? Naming register checked? `PROJECT-RECORD.md` updated?). If the workflow in §6 changes, update this checklist to match — they're meant to stay in sync.

### Community Standards checklist

GitHub's own `/community` page for the repo checks for README, License, Code of Conduct, Contributing, Security Policy, Issue templates, and PR template. **Known issue**: this checklist has, in the past, failed to detect `SECURITY.md` as present for over 24 hours despite the file existing correctly at the repository root — this is a documented, unresolved GitHub platform bug (see community discussions referenced from `docs/PROJECT-RECORD.md`), not a sign that something is actually wrong. The checkmark is cosmetic; the file works for anyone who visits or links to it regardless of what that page shows.

### Mobile web limitations

Several GitHub management flows (repository "About" section's topics/description editor, in particular) don't render correctly — or at all — in GitHub's mobile web interface. **Fix**: force the desktop site in your mobile browser (Chrome: ⋮ menu → "Desktop site") before attempting these flows. This isn't a LUNEX-specific quirk, it's a general GitHub-on-mobile-web limitation, but it's come up repeatedly enough to document here explicitly rather than rediscover each time.

---

## 8. Naming conventions used across the repository

- **File names**: `SCREAMING_SNAKE_CASE.md` for community-health files that GitHub specifically looks for by exact name (`README.md`, `LICENSE`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`) — these names are not stylistic choices, GitHub's own tooling matches on them. Everything else uses `Title-Case-With-Hyphens.md` (`LUNEX-Specification.md`) or plain lowercase (`index.html`, `build_safety.py`).
- **Diagram files**: `lunex-<sub-model-topic>-model.svg`, matching the corresponding `build_<topic>.py` script name (with `build_object_model.py` as the one exception, since Sub-model 1's script predates this naming convention and was never renamed to avoid an unnecessary churn).
- **Sub-model numbering**: always referred to as "Sub-model N," never "Model N" or "Component N" — this specific phrase appears identically across the specification, diagrams, `INDEX.md`, and this guide, and should stay that way for searchability.


---

## 9. Governance status (as of this writing)

LUNEX has no formal legal entity — it's published under an individual's name, licensed CC BY 4.0, with no organization behind it yet. This is a deliberate, staged decision (see `docs/PROJECT-RECORD.md`, "Go-to-Market Strategy" phase): a foundation or similar entity is planned only once genuine external validation and multiple independent contributors exist. **Do not register a foundation, transfer copyright, or change the license preemptively** — this is a decision the project's owner makes deliberately when the conditions are actually met, not something to accelerate administratively.

---

*For the reasoning behind any specific structural decision in this repository (why Discussions over Issues, why the PDF pipeline was consolidated, why `docs/PROJECT-RECORD.md` exists at all), see `docs/PROJECT-RECORD.md` itself. This guide tells you *how* the repository is organized and maintained; that document tells you *why*.*
