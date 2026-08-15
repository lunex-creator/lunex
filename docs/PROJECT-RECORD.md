# LUNEX — Project Record & Decision Log

**Purpose of this document**: a complete, standalone record of how LUNEX came to be — every phase, every design decision, and the reasoning behind it — so that nothing discussed across this project's many sessions is lost to memory. This is not a replacement for `LUNEX-Specification.md` (the technical spec) or `INDEX.md` (the narrative overview); it is the *history* behind both: what was tried, what was rejected, what was corrected, and why.

**How to use this document**: Part 1 is chronological — read it top to bottom to understand how the project unfolded. Part 2 is a reference register — look up a specific decision by topic when you need to recall *why* something is the way it is, without re-reading the whole history.

---

## Part 1 — Chronological Record

### Phase 0 — Foundation: The Sixteen Sub-Models

LUNEX began as an attempt to build one object-oriented reference model spanning what PackML, ISA-88, ISA-95, IEC 61508/61511, IEC 62443, and ISA-18.2 each cover separately. Built collaboratively, sub-model by sub-model, each one pressure-tested against the ones before it:

1. **Object / Class Model** — `LunexObject` as the universal base class; five universal device classes (Sensor, Transducer, Control Unit, Signal Converter, Actuator) distinguished by composable function-interfaces rather than fixed categories.
2. **Asset Hierarchy / Namespace** — Realm → Domain → Location → Area → Cell → System → Assembly → Device → Component, mapped to Purdue levels.
3. **Topology Model** — Integrated / Point-to-Point / Star / Mesh wiring shapes, independent of High-Availability and Cloud & Analytics capability flags.
4. **Behavioral / State Model** — one universal state machine (5 stable + 10 transient states) shared by every object, generalized from PackML's pattern.
5. **Safety** — `Interlock` as a first-class object with proof-test history; SIF Assemblies always physically independent from BPCS.
6. **Security** — `Zone` and `Conduit` as first-class objects, reusing IEC 62443 directly.
7. **Data / AI Layer** — Telemetry Envelope, Context Layer, and Digital Twin as the bridge from physical object to AI-queryable representation.
8. **Naming & Terminology** — the living register of every deliberate deviation from source standards, and why; established the naming principle that governs the whole project: *rename a term only when it already carries a conflicting meaning elsewhere.*
9. **Collective Status (Rollup)** — Severity Tiers and a computed Rollup view, resolving the "what's the worst thing happening beneath this node" question Sub-model 4 deliberately deferred.
10. **Alarm Management** — ISA-18.2-based; the key correction here was that priority is severity × actionability, not severity alone.
11. **Alarm Response Guidance** — reusable `AlarmResponseProcedure` per alarm type, mandatory for Priority 1/2.
12. **Scenario Simulation & Operator Guidance** — AI-driven guidance tested on the Digital Twin before an operator commits to an action.
13. **Situational Awareness** — a navigation contract, not new data: the same three signals at every hierarchy level, plus `jumpToWorst()`.
14. **Historian & Analytics** — the retrospective half of Sub-model 7: what the state *was*, not just what it *is*.
15. **Predictive Maintenance & Improvement** — `PredictedEvent` and `ImprovementRecommendation`, with `requiresApproval` fixed to `true`, no exceptions.
16. **Closed-Loop AI Control** — `AIControlUnit` as an ordinary, governed Control Unit subclass.

Brand identity (colors, logo, the stacked-squares mark) was established in this same phase and carried through consistently into every diagram, the website, and social assets built later.

### Phase 1 — Extending the Model (Simulation Policy & Situational Awareness Refinement)

Two design questions sharpened Sub-models 12 and 13 before the model was considered structurally complete:

- **Golden scenario optionality**: confirmed that `GuidanceRecommendation.goldenScenarioId` may be `null` — equivalent options are a valid, honest outcome; the model should never force a single "best" answer when simulation genuinely produces a tie.
- **Simulation trigger policy**: settled on `automaticMode: always | risk-based | none`, with `riskThreshold` reusing the Sub-model 9 severity tiers (no new scale invented). Later generalized into `manualOverrideAvailable` as a universal, always-on fourth dimension — explicitly *not* a fourth "hybrid" mode, since manual triggering was never meant to be exclusive to one automatic mode.
- **Situational Awareness** was built around three requirements the user set directly: top-down clarity, unambiguous priority, and fast access without digging through layers. This produced the "same three signals at every level" pattern and `jumpToWorst()` — a navigation function, not new stored data, that always lands on the same object a manual layer-by-layer search would reach.

### Phase 2 — Diagram Quality Pass

A long series of visual bugs were found and fixed across the sixteen diagrams, mostly through the user spotting rendering issues on a mobile SVG viewer that a desktop-only check would have missed:

- Text overlapping panel borders (systematically fixed by measuring actual rendered text width rather than estimating).
- Arrowhead markers rendering with the wrong orientation *specifically in exported PDFs* — traced to `wkhtmltopdf`'s outdated WebKit engine mishandling the modern `orient="auto-start-reverse"` SVG marker syntax. Fixed by rasterizing each diagram to a fixed PNG (using the same reliable Chromium renderer used for every visual check) before embedding, rather than embedding raw SVG.
- A genuine, long-buried bug in the Sub-model 1 diagram: the inheritance line from `Actuator` up to `Device` diagonally clipped through the `Component` derived-examples card. Missed by earlier point-sample checks; only caught once boundary math was done properly. Fixed with a routed bend in the line.
- A factual modeling error, caught by the user directly: an inhibit-type Interlock forcing an object to `Standby` — incorrect, since Standby is Tier 3 (Nominal) and can never be an Interlock's target. Corrected to target `Inhibited` (or `Locked`, when starting from `Off`, since `Inhibited` is unreachable from `Off` — see the Off→Locked correction below).

### Phase 3 — Off→Locked Correction (Sub-model 5)

The most consequential correction in the whole project. The user pointed out that when an inhibit-type Interlock condition is active while the target object is already `Off`, the model's original behavior (silently blocking the `Off→Enabling` transition and waiting) was wrong. The corrected rule: drive the object directly to `Locked` via the same `Off→Locking→Locked` edge that lock-type Interlocks already use — because `Inhibited` is structurally unreachable from `Off` in the Sub-model 4 state graph. This is documented transparently as a corrected edge case in Sub-model 5 §9.4, rather than silently rewritten, consistent with the project's stated intention to be a "living document."

The Sub-model 4 state machine's transition labels were subsequently relabeled to make this dual-use explicit: `Emergency stop / Inhibit / Lock` and `Disable / Lock`, since the shared fragment technique meant this single edit propagated correctly into every diagram that transplants the state machine (Sub-models 4, 5, and 16).

### Phase 4 — Go-to-Market Strategy

A substantive, non-technical discussion: how to bring LUNEX to market. Landscape considered: non-profit standards body, pure open-source, vendor-led reference architecture, and pure commercial/IP. Recommendation: the OPC UA pattern — open core specification (free, drives adoption and credibility) with a commercial layer built later (tooling, certification, consulting), kept in a legally separate entity once it exists, to avoid the standard-owner/only-vendor conflict-of-interest problem that has damaged trust in other open projects.

Given the user's actual starting position (independent, small team, no organization), the concrete recommendation was staged:
1. **Now**: publish openly (CC BY 4.0), no formal entity yet — a one-person foundation has no credibility.
2. **Once external validation exists**: seek independent reviewers, consider a Stichting (Dutch foundation) once multiple parties want to contribute.
3. **Later**: build the commercial layer in a structurally separate entity from whatever holds the specification's IP.

### Phase 5 — Publishing Infrastructure

- **GitHub repository** created at `github.com/lunex-creator/lunex`, structured with `README.md`, `LICENSE` (CC BY 4.0), `INDEX.md`, the sixteen diagrams under `diagrams/`, and brand assets under `brand/`.
- **GitHub Discussions** set up with a welcome post explicitly inviting critique over agreement, citing the Off→Locked and `Alarm.origin` corrections as proof that flagged problems get fixed, not defended.
- **Website** (lunex.cloud) built as a single-page site, deliberately reusing the established visual system (grid-paper background, exact brand colors, the real stacked-squares logo mark) rather than inventing new visual language. Signature moment: a self-drawing SVG animation of the `LunexObject` inheritance tree in the hero section. A genuine early mistake — the favicon and OG-image initially used an invented placeholder mark instead of the real logo — was caught by the user and corrected everywhere (favicon, nav, OG image) by extracting the mark directly from the actual brand file.
- **LinkedIn assets** prepared (profile logo, cover banner, post image), with the LinkedIn-specific constraint researched and respected that the profile photo overlaps the bottom-left of a company cover photo.

### Phase 6 — The Full Written Specification

`LUNEX-Specification.md` was built as the complete, standalone technical document: introduction and intentions, a standards cross-reference table, a full glossary, all sixteen sub-model chapters (each with Purpose / Technical Description / Application Guidance), a references list, and — added later after a direct question about whether attributes and methods needed fuller treatment — **Appendix A: Schema Reference**, collecting every class's schema in one place.

A PDF build pipeline was set up (pandoc → HTML → wkhtmltopdf), which went through several rounds of real bugs, each one root-caused rather than patched around:

- **Arrowhead orientation wrong in the PDF only** — root cause: `wkhtmltopdf`'s outdated rendering engine mishandling modern SVG marker syntax. Fixed by pre-rendering every diagram to PNG.
- **File size ballooned to 20MB** after high-resolution rasterization — fixed via PNG palette quantization (diagrams have few flat colors, compress extremely well) and a second JPEG recompression pass on the assembled PDF, bringing it to ~7MB without visible quality loss.
- **Heading separated from its diagram across a page break** — occurred *twice*, for two different underlying reasons. First: `page-break-before` applied only to the diagram, not the heading above it, so the heading could be stranded alone at the bottom of a page. Fixed by moving the break rule to the heading itself. Second: after a diagram grew taller through later edits, the heading+diagram pairing broke again because a synthetic wrapper `<div>`'s `page-break-before` doesn't reliably force reflow of an oversized image inside it — `wkhtmltopdf` would still push the image alone to the next page. Fixed properly with a robust BeautifulSoup-based DOM wrap (not regex, which had already caused a *separate* bug by matching across unrelated element boundaries) pairing every heading with its diagram as one atomic unit, and by making the diagram itself more compact where it was pushing past the practical one-page height budget (~2300–2400px).
- **A subtler heading-orphan pattern**: subsection headings (e.g. "9.1 Purpose") stranded alone at the bottom of a page with their body text pushed to the next page. `page-break-after: avoid` (a hint) proved unreliable on this renderer; fixed properly with `page-break-inside: avoid` on a heading+first-paragraph wrapper, again built with BeautifulSoup after a regex-based first attempt silently failed for one specific case.

### Phase 7 — Model Corrections Following Direct Technical Questions

A cluster of real modeling gaps were found and closed, each starting from a specific, concrete question rather than an abstract review:

- **`System` was wrongly defined** as "a control system (DCS/SCADA/PLC)" when it should be the equivalent of ISA-88's "Unit" — a functional grouping within a Cell, not a piece of hardware. Corrected across the diagram, the specification, and the standards cross-reference table, including the example address path (`DCS-01` → `BoilerUnit-1`).
- **Multi-interface devices** (a VFD or servo drive is simultaneously a Control Unit and a Signal Converter, sometimes also a Transducer) — added as a canonical example to Sub-model 1, both in the diagram (with a footnote convention) and the specification text.
- **`physicalRef`** introduced on `Device` — optional, `DeviceRef | null` initially — to model the case where one physical asset (e.g. one PLC rack) backs several functionally distinct tags (three different control loops). This also gave Sub-model 3's "Integrated" topology a checkable definition instead of an assumed one.
- **`physicalRef` refined to `DeviceRef | ComponentRef`** after the user asked the sharper question: what if the rack has multiple CPUs? The resolution: "not independently addressable" (Sub-model 1's definition of `Component`) describes network reachability, not identity — a `Component` already has its own `id` via `LunexObject` inheritance, so it's just as valid a `physicalRef` target as a `Device`. Illustrated with a two-CPU rack example where two loops share one CPU and a third runs independently on the other.
- **`methods()` formalized** — previously an unused, vague attribute. Resolved as a *computed view*, not a stored list: the Sub-model 4 transition-triggers valid from an object's current state, excluding the automatic `Complete` transition, empty for any transient state. Five classes with their own state machines (`Alarm`, `Interlock`, `GuidanceRecommendation`, `PredictedEvent`, `ImprovementRecommendation`) override this with their own trigger sets, discovered incrementally as the user asked "don't Alarm handling and state transitions need their own methods too?" and then, sharper still, "shouldn't Interlock and others like it also get this treatment?"
- **Scope boundary made explicit**: `methods()` deliberately does not cover continuous operational functionality (a PID loop recalculating every scan cycle) — that lives in `properties`, gets exposed via the Telemetry Envelope, and is governed by `state` + Interlock + `operatingBounds`, with `objective` describing intent without prescribing implementation. This is the same boundary the rest of the model already drew (LUNEX specifies structure and governance, never control algorithms).
- **`AIControlUnit.target` renamed to `controlTarget`** to resolve a same-word, different-meaning collision with `Interlock.target` — the two fields meant genuinely different things on different classes, and the project's own naming principle called for resolving exactly this kind of case.
- **`GuidanceRecommendation` gained its own `state`** (`Open | Applied | Dismissed | Expired`), matching the pattern already established for `PredictedEvent`, after the user asked whether a recommendation's lifecycle needed its own tracking the same way a prediction's did.
- **`votingArchitecture` (MooN notation) added to SIF Assemblies**, mandatory per layer (sensor / logic solver / final element), following a direct question about whether the High-Availability flag could double for 1oo2/2oo3 voting architectures. It cannot — HA is about uptime and applies to any Assembly; voting architecture is about SIL integrity and applies only to a SIF. This also produced a reusable general principle: a field is *mandatory* when its omission would silently assert a safety-relevant fact (no safe default exists); a field stays *optional* when omission has a safe, harmless default. `operatingBounds` (Sub-model 16) already followed this same rule.

### Phase 8 — Full-Document Audit

At the user's request, the entire specification was read end-to-end against its own actual current text (not against memory of earlier sessions) to find gaps and contradictions. Six confirmed issues were found and fixed in one pass:

1. `Alarm.origin` was used in three other places in the document as if it existed, but was never actually added to the `Alarm` schema itself.
2. `Alarm.procedure` — same pattern: referenced by Sub-model 11 as an existing link, never defined on `Alarm`.
3. The glossary claimed `State` was a "14-value enumeration"; actually counting the documented states (5 stable + 10 transient) gives 15.
4. The glossary's `methods()` entry still only listed `Alarm` and `Interlock` as overrides, stale since three more classes had gained overrides.
5. Sub-model 16's own prose had the same stale list.
6. The specification referenced "`Processor`, already a standard Component example, Sub-model 1 §5.2" — but that examples list existed only in the diagram, never actually written into the specification's prose.

A follow-up pass then checked the *surrounding* documents (website, `INDEX.md`, `README.md`, the GitHub Discussions welcome post, LinkedIn content) for the same category of staleness, finding and fixing three more instances confined to `INDEX.md`/`lunex-index.md` (a still-current-sounding "Open items: none outstanding" note that pointed at an earlier, much smaller audit; two sub-model summaries using attribute names that had since been renamed or extended).

---

## Part 2 — Decisions Register

Organized by topic. Each entry: the question or trigger that prompted the decision → what was decided → why. Cross-referenced to the sub-model and section where it now lives in `LUNEX-Specification.md`.

### Object Model & Identity

| Question | Decision | Reasoning |
|---|---|---|
| How does one physical asset (e.g. a PLC) backing multiple functional roles get represented? | `Device.physicalRef : DeviceRef \| ComponentRef \| null`, optional | Omission has a safe default (assumed unique asset); explicitly setting it also makes Sub-model 3's "Integrated" topology checkable rather than assumed. Sub-model 1 §5.2 |
| What if the shared asset is actually one CPU inside a multi-CPU rack, not the whole rack? | `physicalRef` may target a `Component`, not only a `Device` | "Not independently addressable" (the definition of `Component`) is about network reachability, not identity — a `Component` inherits `id`/`tag` from `LunexObject` just like a `Device` does. Sub-model 1 §5.2 |
| What does `LunexObject.methods()` actually return? | A computed view: Sub-model 4 transition-triggers valid from the current `state`, minus the automatic `Complete` transition; empty for any transient state | Makes an until-then-unused attribute meaningful without inventing new mechanism — it was already implicit in how the state diagram was drawn. Sub-model 1 §5.2.1 |
| Do classes with their own state machine (`Alarm`, `Interlock`, ...) get their own `methods()`? | Yes — `Alarm`, `Interlock`, `GuidanceRecommendation`, `PredictedEvent`, `ImprovementRecommendation` each override `methods()` with their own trigger set | Each of these has its own state enumeration separate from Sub-model 4; their valid transitions are equally class-specific. Sub-model 1 §5.2.1 |
| Where does continuous functionality (a PID loop, continuous sampling) belong, if not in `methods()`? | Explicitly out of scope for `methods()` — lives in `properties`, exposed via the Telemetry Envelope, governed by `state` + Interlock + `operatingBounds` | Matches the boundary already drawn everywhere else in LUNEX: the model specifies structure and governance, never control algorithms. Sub-model 1 §5.2.2 |
| Is a frequency/servo drive one class or several? | Canonical example of a multi-interface device: always both `Control Unit` and `Signal Converter`, optionally `Transducer` too | Function-interfaces are composable, not exclusive — this was already the rule, the drive is just the clearest real-world illustration of it. Sub-model 1 §5.3 |
| Does `id` differ from `tag`? | Yes: `id` is permanent and what every `Ref` field points to; `tag` is the human-facing label and may be renamed without breaking references | Re-tagging projects and loop renumbering happen in real plants; references must survive them. Sub-model 1 §5.2 |

### Asset Hierarchy

| Question | Decision | Reasoning |
|---|---|---|
| What does `System` (Sub-model 2) actually mean? | A functional unit within a Cell, equivalent to ISA-88's "Unit" — *not* a control system (DCS/SCADA/PLC) | The original definition was simply wrong relative to the model's own stated ISA-88 alignment; a `Control Unit` (Sub-model 1) is what lives *inside* a System, not the System itself. |

### Safety (Sub-model 5)

| Question | Decision | Reasoning |
|---|---|---|
| What happens when an inhibit-type Interlock fires while the target is already `Off`? | Drives directly to `Locked` via the same `Off→Locking→Locked` edge `lockType: lock` uses — not a silent block-and-wait | `Inhibited` is unreachable from `Off` in the Sub-model 4 graph; blocking and waiting was the wrong behavior for a genuinely tripped safety condition. Documented transparently as a corrected edge case, Sub-model 5 §9.4 |
| Can the Sub-model 3 `High-Availability` flag also express 1oo2 / 2oo3 voting architectures? | No — added a separate, mandatory `votingArchitecture` field (MooN notation, IEC 61508) on SIF Assemblies, one value per layer (sensor / logic solver / final element) | HA is about uptime and applies to any Assembly; voting architecture is about SIL/PFD integrity and applies only to a SIF — different questions, and voting can legitimately differ per layer within one SIF. Sub-model 5 §9.2 |
| Should `votingArchitecture` be optional, like `physicalRef`? | No — mandatory, no implicit default | The two fields look similar but follow opposite logic: omitting `physicalRef` has a safe default (assumed unique asset); omitting `votingArchitecture` would silently assert a SIL-relevant fact (no redundancy) that must always be an explicit, documented engineering decision. Sub-model 5 §9.2 |

### Alarm Management (Sub-model 10) & Extensions

| Question | Decision | Reasoning |
|---|---|---|
| Is alarm priority the same as severity? | No — `priority` is *derived* from `severity × actionable`, not severity alone | An alarm the system already handled (Interlock already tripped) is less urgent than the same condition while an operator could still prevent it, even at identical severity. Sub-model 10 §14.2 |
| How does a `PredictedEvent` (Sub-model 15) reach the operator without a second screen? | It raises an ordinary `Alarm`, tagged via `Alarm.origin: predictive` | Reuses Sub-model 13's single situational-awareness picture instead of building a parallel one. |
| Why `origin`, not `Alarm.source`? | `Alarm.source` already means "which Device" (`DeviceRef`) on the same class — reusing it would collide | Direct application of the Sub-model 8 naming principle: rename only on genuine same-class collision. |
| Does `Alarm` link to its response procedure? | Yes — `Alarm.procedure : AlarmResponseProcedureRef \| null` (`null` valid for Priority 3/4, where an ARP is optional) | This link was assumed/referenced by Sub-model 11 from early on but never actually written into the `Alarm` schema — closed in the full-document audit. |

### Scenario Simulation, Prediction & Improvement (Sub-models 12, 15)

| Question | Decision | Reasoning |
|---|---|---|
| Must `GuidanceRecommendation` always name one best scenario? | No — `goldenScenarioId` may be `null` | Equivalent options are an honest outcome; forcing a "best" answer when simulation produces a genuine tie would misrepresent the result. |
| When should normal (non-alarm) operation trigger simulation? | `SimulationPolicy.automaticMode: always \| risk-based \| none`, `riskThreshold` reusing Sub-model 9 tiers, plus a universal `manualOverrideAvailable` | Reuses the existing severity scale rather than inventing a new one; manual override was confirmed to be universal, not a fourth mode. |
| Does `RetentionPolicy` (Sub-model 14) need a different shape than `SimulationPolicy`? | No — deliberately identical shape | Both are "big-data cost vs. detail" trade-offs; one mental model serves both. |
| Does a `GuidanceRecommendation` need its own lifecycle, like a `PredictedEvent` does? | Yes — `state: Open \| Applied \| Dismissed \| Expired`, with `apply()`/`dismiss()` as `methods()` overrides | A recommendation is generated against a specific process-state snapshot and goes stale the same way a prediction does. |
| Can an `ImprovementRecommendation` ever be auto-applied at high confidence? | No — `requiresApproval: true`, fixed, no false case, even at `confidence: 1.0` | It changes how the plant runs going forward, a materially bigger decision than a single `ScenarioResult` shown in the moment. |

### AI Governance (Sub-model 16)

| Question | Decision | Reasoning |
|---|---|---|
| How is an `AIControlUnit` switched on/off? | Reuses the Sub-model 4 state machine completely unmodified — no new mechanism | An AI performing closed-loop control isn't exempt from the safety model; treating it like any other Control Unit keeps Interlocks applicable without special-casing. |
| Can `operatingBounds` ever be empty? | Only when `controlTarget: DigitalTwin` — always required when `controlTarget: PhysicalDevice` | Unbounded action against the Digital Twin cannot cause real-world harm; unbounded action against the physical process always can. |
| Why `controlTarget`, not `target`? | `Interlock.target` (Sub-model 5) already means something different on a different class — same word, different meaning, would collide | Direct application of the Sub-model 8 naming principle. |
| What happens when an action falls outside `operatingBounds`? | Clamped (never reaches the physical Device) *and* raises an `ImprovementRecommendation` suggesting the bound itself be reviewed | The bound might be wrong, but widening it is always a human decision — never a silent auto-adjustment. |

### Naming & Terminology (Sub-model 8) — Meta-Decisions

| Question | Decision | Reasoning |
|---|---|---|
| When should a term be renamed from its source-standard original? | Only when it already carries a conflicting meaning elsewhere in the model, or in an adjacent standard LUNEX must interoperate with | The one-sentence naming principle every other renaming decision in this log was tested against. |
| Where do naming corrections get recorded? | Sub-model 8's "Renamed Terms" register, permanently, including corrections discovered after the fact | The register's stated value is being complete, not just eventually correct — silently fixing a name without logging it would defeat its purpose. |

### Publishing & Governance

| Question | Decision | Reasoning |
|---|---|---|
| Open standard, foundation, or commercial? | Open specification first (CC BY 4.0), commercial layer later, kept in a legally separate entity | Mirrors the OPC UA pattern; avoids the standard-owner/only-vendor trust problem seen in other projects. |
| Foundation now or later? | Later — only once genuine external validation and multiple contributors exist | A one-person foundation carries no more credibility than no foundation at all. |
| License for the specification vs. future tooling? | CC BY 4.0 for the spec and diagrams; Apache 2.0 planned for any future reference implementation | Standard, permissive pairing that keeps the spec maximally reusable while leaving room for a conventional open-source software license later. |

### Tooling & Process Lessons (non-model, but worth keeping)

| Problem | Root cause | Fix |
|---|---|---|
| PDF arrows pointed the wrong way | `wkhtmltopdf`'s old WebKit engine mishandles modern SVG marker syntax | Rasterize diagrams to PNG before embedding, instead of embedding raw SVG. |
| Heading stranded on a different page than its diagram | Page-break rule applied to the wrong element, twice over (once by design, once after a diagram grew past the one-page height budget) | Pair heading+diagram as one atomic DOM unit via BeautifulSoup (not regex — regex silently matched across unrelated element boundaries once); keep an eye on the practical ~2300–2400px single-page diagram height ceiling. |
| Subsection heading stranded without its first paragraph | `page-break-after: avoid` is a hint this renderer ignores | `page-break-inside: avoid` on a heading+paragraph wrapper is a hard constraint the same renderer does respect. |
| Favicon/OG image didn't match the real logo | A new placeholder mark was drawn from scratch instead of extracting the established one | Always pull brand marks from the source file (`lunex-logo-light.svg`) rather than recreating them by eye. |

---

*This document should be updated whenever a future session produces a decision worth preserving — append to Part 1 chronologically, add to the relevant table in Part 2. It is intentionally separate from `LUNEX-Specification.md` (what LUNEX currently *is*) and `INDEX.md` (a narrative summary for newcomers) — this document is specifically the *why*, preserved for whoever picks this project up next, including a future instance of this same collaboration.*
