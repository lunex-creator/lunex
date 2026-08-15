# Contributing to LUNEX

LUNEX is a draft, authored so far by a single contributor, and it shows. The most useful thing you can do is find where it's wrong.

## Before anything else

Read `README.md` for what LUNEX is, and skim `docs/PROJECT-RECORD.md` if you want the reasoning behind a specific design decision before raising it — it might already be documented why something is the way it is (or, just as usefully, documented as a decision worth revisiting).

## How to raise something

Use [GitHub Discussions](../../discussions), not Issues, for anything design-related — a naming choice, a missing case, a schema you think is wrong. Issues are for concrete, actionable bugs (a broken diagram, a build script that doesn't run).

When raising a design question, include:
- **Which sub-model and section** you're referring to (e.g. "Sub-model 5 §9.2" or "the `Alarm` schema in Appendix A").
- **The specific case** that doesn't fit, ideally as a concrete example rather than an abstract concern — "a rack with two CPUs" got further, faster, than "physicalRef seems incomplete."
- **What you'd expect instead**, if you have a view — not required, but it speeds up the conversation.

## What happens next

Every substantive change in this project has followed the same shape, visible throughout `docs/PROJECT-RECORD.md`:

1. **A concrete question or case is raised** — often sharper than the first version of a rule ("what if the rack has multiple CPUs?" is what actually fixed `physicalRef`, not a general review).
2. **The reasoning is worked through in the open** — including checking whether the model already has a working precedent for the same kind of situation, rather than reaching for a new mechanism by default.
3. **The decision and its reasoning are recorded**, not just the resulting text. A schema change without documented reasoning is treated as incomplete.
4. **If it's a naming decision**, it's logged in Sub-model 8's naming register, whether the outcome was a rename or a decision *not* to rename.
5. **If a correction reverses an earlier decision**, the reversal is documented too — see `docs/PROJECT-RECORD.md` Phase 9 for an example. Nothing gets silently rewritten as if it had always been that way.

## Reviewing the model itself

If you want to stress-test a sub-model rather than wait for something to bother you organically: pick the one closest to your own domain expertise and try to break it. A safety engineer reading Sub-model 5, a cybersecurity practitioner reading Sub-model 6, an alarm-management specialist reading Sub-model 10 — that's worth more than a general read-through of all sixteen.

## Working on the diagrams or the PDF build

See `tools/README.md`. Every diagram is generated from a Python script, not hand-edited as SVG — if you're proposing a diagram change, propose it as a change to the corresponding `tools/diagrams/build_*.py` script.

## Naming

Before introducing a new term, check Sub-model 8's naming register first — the collision or the term you need may already be documented. The rule that governs every naming decision in this project:

> Rename a term only when it already carries a conflicting meaning elsewhere in the model, or in an adjacent standard LUNEX must interoperate with. Otherwise, reuse established vocabulary — inventing a new word is not innovation if the old one wasn't actually broken.

## License

By contributing, you agree your contribution is made under the same license as the rest of the repository (CC BY 4.0 for the specification and diagrams; see `LICENSE`).
