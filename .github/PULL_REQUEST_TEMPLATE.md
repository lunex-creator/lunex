## What this changes

<!-- One or two sentences. If this resolves an open Discussion or Issue, link it. -->

## Why

<!-- The reasoning, not just the change. If this reverses or corrects an earlier decision, say so explicitly — see docs/PROJECT-RECORD.md, Phase 9, for how that's normally handled here. -->

## Checklist

- [ ] If this changes a schema or adds/renames a field: `LUNEX-Specification.md` **and** `Appendix A` are both updated (they're written separately, not generated from one source — it's easy to update one and miss the other).
- [ ] If this changes a diagram: the corresponding `tools/diagrams/build_*.py` script was updated and re-run, not the `.svg` hand-edited.
- [ ] If this renames or introduces a term: logged in Sub-model 8's naming register (`tools/diagrams/build_naming.py`), whether the outcome was a rename or a decision not to rename.
- [ ] If this is a design decision worth remembering: added to `docs/PROJECT-RECORD.md` (Part 1 chronologically, Part 2 if it fits an existing table).
- [ ] `CHANGELOG.md` updated.
- [ ] If the PDF is affected: rebuilt via `tools/pdf/build_pdf.py` and spot-checked (page breaks, arrow orientation — see `tools/README.md` for the specific failure modes this project has hit before).

## Anything you're unsure about

<!-- Genuinely welcome here — a flagged uncertainty is more useful than a confident guess. -->
