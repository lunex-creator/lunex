# LUNEX — Project Record & Decision Log

**Purpose of this document**: a complete, standalone record of how LUNEX came to be — every phase, every design decision, and the reasoning behind it — so that nothing discussed across this project's many sessions is lost to memory. This is not a replacement for `LUNEX-Specification.md` (the technical spec) or `INDEX.md` (the narrative overview); it is the *history* behind both: what was tried, what was rejected, what was corrected, and why.

**How to use this document**: Part 1 is chronological — read it top to bottom to understand how the project unfolded. Part 2 is a reference register — look up a specific decision by topic when you need to recall *why* something is the way it is, without re-reading the whole history.

---

## Part 1 — Chronological Record

### Phase 0 — Foundation: The Sixteen Sub-Models

LUNEX began as an attempt to build one object-oriented reference model spanning what PackML, ISA-88, ISA-95, IEC 61508/61511, IEC 62443, and ISA-18.2 each cover separately. Built collaboratively, sub-model by sub-model, each one pressure-tested against the ones before it:

1. **Object / Class Model** — `LunexObject` as the universal base class; five universal device classes (Sensor, Transducer, ControlUnit, SignalConverter, Actuator) distinguished by composable function-interfaces rather than fixed categories.
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
16. **Closed-Loop AI Control** — `AIControlUnit` as an ordinary, governed ControlUnit subclass.

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
- **Multi-interface devices** (a VFD or servo drive is simultaneously a ControlUnit and a SignalConverter, sometimes also a Transducer) — added as a canonical example to Sub-model 1, both in the diagram (with a footnote convention) and the specification text.
- **`physicalRef`** introduced on `Device` — optional, `DeviceRef | null` initially — to model the case where one physical asset (e.g. one PLC rack) backs several functionally distinct tags (three different control loops). This also gave Sub-model 3's "Integrated" topology a checkable definition instead of an assumed one.
- **`physicalRef` refined to `DeviceRef | ComponentRef`** after the user asked the sharper question: what if the rack has multiple CPUs? The resolution: "not independently addressable" (Sub-model 1's definition of `Component`) describes network reachability, not identity — a `Component` already has its own `id` via `LunexObject` inheritance, so it's just as valid a `physicalRef` target as a `Device`. Illustrated with a two-CPU rack example where two loops share one CPU and a third runs independently on the other.
- **`methods()` formalized** — previously an unused, vague attribute. Resolved as a *computed view*, not a stored list: the Sub-model 4 transition-triggers valid from an object's current state, excluding the automatic `Complete` transition, empty for any transient state. Five classes with their own state machines (`Alarm`, `Interlock`, `GuidanceRecommendation`, `PredictedEvent`, `ImprovementRecommendation`) override this with their own trigger sets, discovered incrementally as the user asked "don't Alarm handling and state transitions need their own methods too?" and then, sharper still, "shouldn't Interlock and others like it also get this treatment?"
- **Scope boundary made explicit**: `methods()` deliberately does not cover continuous operational functionality (a PID loop recalculating every scan cycle) — that lives in `properties`, gets exposed via the Telemetry Envelope, and is governed by `state` + Interlock + `operatingBounds`, with `objective` describing intent without prescribing implementation. This is the same boundary the rest of the model already drew (LUNEX specifies structure and governance, never control algorithms).
- **`AIControlUnit.target` renamed to `controlTarget`** to resolve a same-word, different-meaning collision with `Interlock.target` — the two fields meant genuinely different things on different classes, and the project's own naming principle called for resolving exactly this kind of case. *(Reversed shortly after — see Phase 9 below.)*
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

### Phase 9 — A Correction Reversed: `controlTarget` → back to `target`

Directly asked whether introducing two terms (`target` and `controlTarget`) had actually been necessary, the honest answer turned out to be no. The `AIControlUnit.controlTarget` rename (Phase 7) was reconsidered against a precedent the model already had: `Alarm.state` uses its own value space while `Interlock.state` reuses the Sub-model 4 enum — same field name, two different classes, two different meanings, never renamed, just documented per class. `Interlock.target` and `AIControlUnit.target` are in exactly the same situation: no object is ever both classes at once, so the two meanings never collide in practice. The original rename applied the Sub-model 8 naming principle too strictly — that principle exists for genuine *same-class* collisions (like `Alarm.origin` vs. `Alarm.source`), not for a field name that simply appears on two unrelated classes with two different, non-conflicting meanings. Reverted throughout the specification, Appendix A, the naming register, and `INDEX.md`; documented here rather than silently undone, consistent with how every other correction in this project has been handled.

---

### Phase 10 — Naming the Name: `LUNEX` as a Backronym

Asked directly what `LUNEX` could plausibly stand for, several options were considered before settling on one that describes what the model actually does rather than being chosen first and fitted to the model afterward: **Layered Unified Namespace for Entities & eXtensibility**. The first draft used "Equipment" in place of "Entities" and was corrected immediately: `LunexObject` (Sub-model 1) — the base class everything in the model inherits from — includes non-physical peers (`Alarm`, `Interlock`, `Zone`, `GuidanceRecommendation`, `PredictedEvent`, `ImprovementRecommendation`) that are not equipment in any normal sense. "Entities" matches the actual scope of Sub-model 1; "Equipment" would have silently narrowed it. Recorded in `README.md`, `LUNEX-Specification.md` §1, and `INDEX.md`.

---

### Phase 11 — A Concrete Gap Closed: `Operator`

Asked whether any future sub-models were needed, the honest answer led first to auditing what already existed rather than proposing something new: a grep across the specification for every `*Ref` type found that `OperatorRef` (used twice, in `AIControlUnit.disabledBy`) was the only one that never resolved to an actual defined class — every other `*Ref` type had a real class behind it. `Operator` was added as an eighth peer of `Device` in Sub-model 1, deliberately minimal (`role : string`) — it records identity and capacity, not permissions. A full role-based access model was explicitly considered and deliberately deferred as a separate, future concern rather than folded into this fix, consistent with how the model has drawn this same "structure now, mechanism later" boundary everywhere else (e.g. `objective` on `AIControlUnit` describing intent without prescribing an algorithm). Two candidate future sub-models were also discussed and intentionally *not* built yet — ISA-88 Recipe/Execution Execution and Management of Change (MOC) — both flagged as natural extensions given what LUNEX already cites or partially implies, but held back pending real external feedback rather than spun up speculatively. Revisited once, directly — asked whether to build them now regardless — and the original reasoning held: still waiting. Priority order for whenever that changes: **Recipe/Execution Execution first, then MOC.**

While implementing `Operator`, a second, unrelated latent bug was caught and fixed in passing: Sub-model 8's diagram script computed its "New Vocabulary" panel height from a hardcoded row count (`rows_n = 7`) rather than the actual number of entries, which happened to still be correct by coincidence right up until this addition. Changed to a computed ceiling-division so a future addition to that list can never silently overflow the panel.

---

### Phase 12 — Predictive Maintenance Is Not Predictive Analytics

Prompted by a direct comparison against an unrelated grid/utility architecture diagram (IEC 61850/CIM), the underlying distinction turned out to matter regardless of that comparison's own relevance: predictive maintenance (internal, Historian-derived) is one case of the broader category of predictive analytics, which also covers predictions driven by sources entirely external to the plant — a weather forecast informing an anticipatory setpoint change, an energy-price forecast informing a load shift. Sub-model 15's `PredictedEvent.basis` was, on inspection, explicitly typed as `string (Historian pattern)` only — it structurally could not represent an external-forecast-driven prediction. Resolved by adding `basisType: internal-pattern | external-forecast`, making both cases first-class under the same object rather than requiring a second mechanism for the external case. The sub-model's title was deliberately left unchanged (it names its two classes, `PredictedEvent` and `ImprovementRecommendation`, not the full scope of predictive analytics) — only the field's own type was too narrow, not the sub-model's boundary.

The same IEC 61850/CIM comparison surfaced two more terms worth checking against LUNEX directly: "Mapping" and "Semantic Annotation." "Semantic Annotation" turned out to already be fully covered — it's exactly what Sub-model 7's Context Layer `semanticTag` already does, just different vocabulary for the same idea, no gap. "Mapping" (a formal LunexObject-to-external-information-model mapping, e.g. to OPC UA's) is genuinely absent, but deliberately so: Sub-model 2 §2's standards table already states LUNEX "does not mandate OPC UA; it deliberately stays protocol-agnostic," and a concrete mapping would work against that choice by tying the object model to one specific protocol. Added to the same deferred list as Recipe/Execution and MOC, as a candidate optional appendix (not a core specification change) rather than something to build now: **Appendix C — Protocol Mapping Guidance (e.g. LunexObject → OPC UA Information Model)**.

---

### Phase 13 — `coordinates`: a Third, Unrelated Sense of "Mapping"

A follow-up question about "mapping" turned out to mean something else entirely — not protocol/schema mapping, but literal geographic location per object. Unlike the protocol-mapping question, this one was a genuine, immediately fixable gap with no competing design principle to weigh against it: no object anywhere in the model could carry a coordinate. Resolved by adding `coordinates : { lat, lon } | null` to `LunexObject` itself (Sub-model 1 §5.2) — deliberately on the base class rather than only on `Location` (Sub-model 2), after weighing both: a site-level coordinate on `Location` covers most cases, but individual objects within one Location can be genuinely kilometers apart (a pipeline's valves, a wind farm's turbines, a distributed solar array) — exactly the kind of asset the IEC 61850/CIM comparison that started this whole line of questioning was actually about. Optional, following the same reasoning as `physicalRef`: omission is a safe default (the object simply isn't geo-located), not a silent assertion, unlike `votingArchitecture`'s mandatory case.

---

### Phase 14 — Five New Sub-Models and Governance (Recipe & Execution, IAM, Vulnerability & Patch, Security Incident Response, Management of Change + Policy)

The two candidate future sub-models flagged and deliberately deferred back in Phase 11 (Recipe Execution, Management of Change) were finally built — alongside three more that emerged from auditing the same category of gap: Identity & Access Management, Vulnerability & Patch Management, and Security Incident Response. Each was checked against "reuse before invention" before being accepted as a genuinely new sub-model rather than an extension of an existing one:

- **Recipe & Execution Model** (Sub-model 5) — ISA-88's `Recipe` (originally General/Site/Master/Control; now `recipeLevel: product | location | equipment | execution`, see Phase 15) and `RecipeElement` (originally ProcedureElement: Procedure/Unit Procedure/Operation/Phase; now steps named by the asset level that runs them, `runsOn: area | cell | system | assembly`, see Phase 15) layered directly over Sub-model 2 (where) and Sub-model 4 (how), with no new level added to either. The deliberate finding, not a design choice imposed from outside: `RecipeExecution` needs no new state machine at all — PackML's states, already generalized once into Sub-model 4, already *are* batch-execution states, so unlike `Alarm` or the new `ChangeRequest`, `RecipeExecution.methods()` has no override.
- **Identity & Access Management** (Sub-model 8) — closes the "who's allowed to do what" question IEC 62443-3-3 SR 1.x/2.x asks, which `Operator` (added in Phase 11, deliberately minimal — identity and capacity, not permissions) never answered. `Identity`, `Role`, `Permission` reuse standard least-privilege RBAC vocabulary unchanged; `AccessGrant` is the scoped, time-bounded binding. This renumbered what had been Sub-model 8 (Naming & Terminology) to Sub-model 12 — the only renumbering this phase required beyond simple insertion, flagged explicitly because it touches a lot of cross-references (every `Sub-model 8` citation across the entire specification, index, and README had to be found and corrected to `Sub-model 12`).
- **Vulnerability & Patch Management** (Sub-model 9) — `Vulnerability` (`cveRef`/`cvss` unchanged from CVE/CVSS) and `PatchRecord`, with `status: accepted-risk` treated as a legitimate, permanent, *documented* end state rather than a silent default for incomplete triage. Every `PatchRecord` requires a `ChangeRequest` reaching `Implemented` — patching is governed exactly like any other change, not a parallel approval flow.
- **Security Incident Response** (Sub-model 10) — `SecurityIncident` built as a peer of `Alarm`, never a subtype: Alarm Management (Sub-model 15, after renumbering) is explicitly process-alarm-focused, and NIST CSF's Respond/Recover functions needed their own object with its own `Detected → Contained → Eradicated → Recovered → Closed` lifecycle. A remediation that changes plant configuration links out to a `ChangeRequest` via `relatedChange`, rather than being modeled as a configuration change itself.
- **Management of Change** (Sub-model 13) — the most structurally significant addition. Five previously ad hoc, ungoverned approval patterns scattered across the model (`ImprovementRecommendation.requiresApproval`, an Interlock/SIF modification, a Zone/Conduit reconfiguration, an `AccessGrant` escalation, a Master/Control Recipe parameter change) were generalized into one `ChangeRequest` object with its own lifecycle (`Draft → PendingApproval → Approved/Rejected → Implemented → Verified → Closed`), reusing Sub-model 14's existing Tier scale for `riskAssessment` rather than inventing a new risk vocabulary. `VersionRecord` reuses the Historian's append-only storage principle for before/after configuration snapshots — closing a real gap where *that* a change happened was recorded but not *what existed* immediately beforehand.

**Governance, added in the same pass**: asked directly whether governance ("who's accountable, what the rules are, whether they were followed") could be added without a new, sixth capability sub-model, the answer was yes, following the same reuse principle that has governed every other addition in this project:
- `LunexObject.owner : RoleRef | null` (Sub-model 1) — the *only* governance field added to the base class. Deliberately narrow: it answers "who is accountable for this object," nothing more. "Who may act" stays entirely in Sub-model 8's `AccessGrant`; "what the rules are" stays entirely in Sub-model 13's new `Policy` class below. Optional, `null` by default, following the same safe-omission logic as `physicalRef` and `coordinates`.
- `ChangePolicy extends LunexObject` (originally `Policy`; renamed in Phase 15) (Sub-model 13) — a standing, queryable approval rule (`appliesTo`, `changeTypes`, `requiredTier`, `requiredApprovals`, `minApprovals`, `rationale`) that a matching `ChangeRequest` resolves its requirements against, rather than repeating `requiredApprovals` by hand on every change. The resolution rule settled on: the most specific matching `Policy` (an instance match beats a class match) supplies the floor for `requiredApprovals`/`riskAssessment`, and a `ChangeRequest` may only raise that bar, never lower it — `Policy` is "governance authored once," `ChangeRequest` is "governance applied once."

A new, standalone 22nd sub-model for governance was explicitly considered and rejected: governance is cross-cutting (it touches every object and every change), not a new domain of its own, so it belongs distributed across the two sub-models that already own "identity of the object" (Sub-model 1) and "change happening to the object" (Sub-model 13), exactly the same reasoning that kept `Operator` out of a dedicated access-control sub-model back in Phase 11 until IAM was actually needed.

**Diagram work**: all five new sub-models got their own SVG diagram built from scratch (`lunex-recipe-execution-model.svg`, `lunex-iam-model.svg`, `lunex-vulnerability-model.svg`, `lunex-security-incident-model.svg`, `lunex-moc-model.svg`, the last extended mid-build to add the `Policy` schema box once governance was agreed). Sub-model 6's diagram (Safety) was extended with a new panel covering `silTarget`/`silAchieved`/`pfdAvg`/`pfh` (replacing a single unverified `SIL` field) and machine safety (ISO 13849-1/IEC 62061 `performanceLevel`/`category`, plus `SafeMotionFunction` per IEC 61800-5-2) — both diagrams required several rounds of trimming inter-panel spacing, box heights, and font sizes to stay within the project's established ~2300–2400px practical single-page height budget, the same constraint documented in Phase 6's PDF work. Sub-model 1's diagram was restructured from a single row of (then seven, now eight) peer classes to two rows, to fit the four new peers (`RecipeExecution`, `Identity`, `SecurityIncident`, `ChangeRequest`, `Policy`) without breaking that same height budget.

A stale cross-reference from the Sub-model 8→12 renumbering was caught in a proactive grep sweep before considering the work complete: §1.2's "Intentions" bullet still said "Sub-model 8 exists specifically to keep every naming and design decision traceable," which had meant Naming & Terminology before this phase's renumbering moved that sub-model to 12. Corrected; confirmed via a full-document grep that it was the only stale instance. A second pre-existing bug, unrelated to this phase's changes but found while editing nearby, was also fixed: Appendix A's "Sub-model 13" schema block had been misplaced after "Sub-model 17" since the Phase-8/9-era renumbering, instead of appearing in numerical order before Sub-model 14 — moved to its correct position, with the new `Policy` class added to it at the same time.

The version was bumped from 0.1 to 0.2 (still a draft) to reflect the scale of the change — five new sub-models, the governance layer, and a renumbering that touches every cross-reference. The `[Unreleased]` changelog section became `[0.2]`, and the version was updated in the README, specification header, `CITATION.cff`, `SECURITY.md`, the website, the PDF title page, and the social images.

`INDEX.md` and `README.md` were both rewritten for the resulting five-band, twenty-one-sub-model structure (Foundation 1–5, Safety & Security 6–10, Cross-cutting 11–13 (originally "Capability"), Operator capability 14–18, Autonomous layer 19–21) — including a new ASCII dependency diagram in `INDEX.md` reflecting the five bands instead of the original four-layer one.

### Phase 15 — Naming Review of the Five New Sub-Models (v0.2)

After the five sub-models were added, the naming principle from Sub-model 12 was applied to them. Four field/class collisions were found and fixed: `Operator.role` → `jobTitle`, `Vulnerability.status` → `state`, `category` → `architectureCategory`, `Policy` → `ChangePolicy`. Two titles were also ambiguous: band 11–13 "Capability" → "Cross-cutting", and Sub-model 7 "Security" → "Security Zones & Conduits". Sub-model 12's register had never been extended for the new sub-models; it now logs these renames, the newly kept standard terms, and the new vocabulary.

A second pass, prompted by the owner, targeted the Recipe & Execution model. ISA-88's `general | site | master | control` levels had no visible link to "recipe", and `site`, `control`, `unit` and `procedure` already meant something else in LUNEX. The result: `Recipe.recipeLevel : product | location | equipment | execution`, with `derivedFrom : RecipeRef` making the refinement chain explicit; and `RecipeElement` replacing `ProcedureElement` (step vocabulary revised again in the fourth pass below). Candidates `method`, `operation`, `scope` and `generic` were rejected because they are object-oriented terms or already used in the model (`scope` on `Permission`/`AccessGrant`). The owner's rule: every term clear and used once.

A third pass applied the same test to the execution side. "Batch" only fits batch production, so the class became `RecipeExecution` (neutral across batch, campaign, discrete and continuous production, with `quantityTarget : quantity | null`). The level value is `execution`, the diagram and sub-model title are "Recipe & Execution", and the step tree is called the recipe structure. In-run tuning is logged in `RecipeExecution.adjustments`; promoting a tuned result to a new `Recipe` (`basedOnExecution`, optional `goldenExecution`) goes through `ImprovementRecommendation` and `ChangeRequest`. "Production" alone was rejected because it already means non-production vs. production areas in Sub-model 2.

A fourth pass replaced the step vocabulary altogether. Plan/Stage/Task/Phase was judged unclear by the owner; instead each `RecipeElement` is named by the asset level that runs it (`runsOn: area | cell | system | assembly`), which needs no new words and ties the recipe structure directly to Sub-model 2. Children run on a lower level than their parent, `childOrder: sequence | parallel` makes ordering explicit, and there is deliberately no Device-level element because a Device has its own Sub-model 4 state. `area` was added so recipes spanning several cells can be expressed (a gap in ISA-88). `equipmentClass` became a typed `ClassRef`, checked against `target` when the recipe is bound. The `execution`-level recipe was also reworded from "frozen" to "baseline": its structure is fixed but parameters can be adjusted (logged in `adjustments`).

A related defect was found and fixed: every diagram still carried pre-0.2 sub-model numbers in its header and cross-references. All 21 diagrams were regenerated.

---

## Part 2 — Decisions Register

Organized by topic. Each entry: the question or trigger that prompted the decision → what was decided → why. Cross-referenced to the sub-model and section where it now lives in `LUNEX-Specification.md`.

### Phase 16 — Diagram Layout Pass (v0.2)

The diagrams for the new and extended sub-models had overlapping text, boxes too small for their content and arrows that did not end on a box. Fix: a rendering-based lint (`tools/diagrams/lint_diagram.py`) was added and every affected diagram was reworked until it was clean apart from known false positives (legends, dotted physicalRef arrows, scaled state-machine fragment). Safety: legend and notes moved beside the state machine. Object Model: peers split into rows of 8 and 5 with wider boxes; Operator moved to the second row. Follow-up: Security (Zone box, inheritance arrows, FW markers), Vulnerability and Recipe & Execution (state-machine excerpt) tidied; Sub-model 12 register and §16 of the specification brought up to date with every v0.2 rename, and a guidance item added that plain-language descriptions must use the register's terms.

Second pass over all 21 diagrams (visual review of each rendering): composition diamonds were drawn into the box instead of on its edge (marker `refX` corrected in every script, missing `diamond-navy` marker defined in the scenario diagram); the Object Model's interface lollipops moved to the right side so the Actuator inheritance line no longer crosses the "Converting" label; the state-machine fragment's opaque background no longer covers subtitles in the State, Safety and AI-control diagrams; text overflowing or touching box edges fixed in Rollup, Topology, Scenario, Historian, Data/AI and Predictive. Plurals of schema-bearing classes are written "ControlUnit objects", never "ControlUnits".

### Object Model & Identity

| Question | Decision | Reasoning |
|---|---|---|
| How does one physical asset (e.g. a PLC) backing multiple functional roles get represented? | `Device.physicalRef : DeviceRef \| ComponentRef \| null`, optional | Omission has a safe default (assumed unique asset); explicitly setting it also makes Sub-model 3's "Integrated" topology checkable rather than assumed. Sub-model 1 §5.2 |
| What if the shared asset is actually one CPU inside a multi-CPU rack, not the whole rack? | `physicalRef` may target a `Component`, not only a `Device` | "Not independently addressable" (the definition of `Component`) is about network reachability, not identity — a `Component` inherits `id`/`tag` from `LunexObject` just like a `Device` does. Sub-model 1 §5.2 |
| What does `LunexObject.methods()` actually return? | A computed view: Sub-model 4 transition-triggers valid from the current `state`, minus the automatic `Complete` transition; empty for any transient state | Makes an until-then-unused attribute meaningful without inventing new mechanism — it was already implicit in how the state diagram was drawn. Sub-model 1 §5.2.1 |
| Do classes with their own state machine (`Alarm`, `Interlock`, ...) get their own `methods()`? | Yes — `Alarm`, `Interlock`, `GuidanceRecommendation`, `PredictedEvent`, `ImprovementRecommendation` each override `methods()` with their own trigger set | Each of these has its own state enumeration separate from Sub-model 4; their valid transitions are equally class-specific. Sub-model 1 §5.2.1 |
| Where does continuous functionality (a PID loop, continuous sampling) belong, if not in `methods()`? | Explicitly out of scope for `methods()` — lives in `properties`, exposed via the Telemetry Envelope, governed by `state` + Interlock + `operatingBounds` | Matches the boundary already drawn everywhere else in LUNEX: the model specifies structure and governance, never control algorithms. Sub-model 1 §5.2.2 |
| Is a frequency/servo drive one class or several? | Canonical example of a multi-interface device: always both `ControlUnit` and `SignalConverter`, optionally `Transducer` too | Function-interfaces are composable, not exclusive — this was already the rule, the drive is just the clearest real-world illustration of it. Sub-model 1 §5.3 |
| Does `id` differ from `tag`? | Yes: `id` is permanent and what every `Ref` field points to; `tag` is the human-facing label and may be renamed without breaking references | Re-tagging projects and loop renumbering happen in real plants; references must survive them. Sub-model 1 §5.2 |
| What does `OperatorRef` (used by `AIControlUnit.disabledBy`) actually resolve to? | A new peer class, `Operator extends LunexObject { jobTitle : string }` (originally `role`; renamed in Phase 15) — the eighth peer of `Device`/`Component` | Found via an audit of every `*Ref` type in the specification: the only one with no defined class behind it. Deliberately minimal — identity and capacity, not a permissions system, which is left as a genuinely separate, future concern. Sub-model 1 §5.2 |
| Can any object carry a geographic position? | Yes — `LunexObject.coordinates : { lat, lon } \| null`, on the base class | Placed on `LunexObject` rather than only `Location` (Sub-model 2) because individual objects within one Location can be genuinely distributed (a pipeline's valves, a wind farm's turbines). Optional with a safe default, like `physicalRef` — not mandatory like `votingArchitecture`. Sub-model 1 §5.2 |

### Asset Hierarchy

| Question | Decision | Reasoning |
|---|---|---|
| What does `System` (Sub-model 2) actually mean? | A functional unit within a Cell, equivalent to ISA-88's "Unit" — *not* a control system (DCS/SCADA/PLC) | The original definition was simply wrong relative to the model's own stated ISA-88 alignment; a `ControlUnit` (Sub-model 1) is what lives *inside* a System, not the System itself. |

### Safety (Sub-model 6)

| Question | Decision | Reasoning |
|---|---|---|
| What happens when an inhibit-type Interlock fires while the target is already `Off`? | Drives directly to `Locked` via the same `Off→Locking→Locked` edge `lockType: lock` uses — not a silent block-and-wait | `Inhibited` is unreachable from `Off` in the Sub-model 4 graph; blocking and waiting was the wrong behavior for a genuinely tripped safety condition. Documented transparently as a corrected edge case, Sub-model 6 §10.4 |
| Can the Sub-model 3 `High-Availability` flag also express 1oo2 / 2oo3 voting architectures? | No — added a separate, mandatory `votingArchitecture` field (MooN notation, IEC 61508) on SIF Assemblies, one value per layer (sensor / logic solver / final element) | HA is about uptime and applies to any Assembly; voting architecture is about SIL/PFD integrity and applies only to a SIF — different questions, and voting can legitimately differ per layer within one SIF. Sub-model 6 §10.2 |
| Should `votingArchitecture` be optional, like `physicalRef`? | No — mandatory, no implicit default | The two fields look similar but follow opposite logic: omitting `physicalRef` has a safe default (assumed unique asset); omitting `votingArchitecture` would silently assert a SIL-relevant fact (no redundancy) that must always be an explicit, documented engineering decision. Sub-model 6 §10.2 |

### Alarm Management (Sub-model 15) & Extensions

| Question | Decision | Reasoning |
|---|---|---|
| Is alarm priority the same as severity? | No — `priority` is *derived* from `severity × actionable`, not severity alone | An alarm the system already handled (Interlock already tripped) is less urgent than the same condition while an operator could still prevent it, even at identical severity. Sub-model 15 §19.2 |
| How does a `PredictedEvent` (Sub-model 20) reach the operator without a second screen? | It raises an ordinary `Alarm`, tagged via `Alarm.origin: predictive` | Reuses Sub-model 18's single situational-awareness picture instead of building a parallel one. |
| Why `origin`, not `Alarm.source`? | `Alarm.source` already means "which Device" (`DeviceRef`) on the same class — reusing it would collide | Direct application of the Sub-model 12 naming principle: rename only on genuine same-class collision. |
| Does `Alarm` link to its response procedure? | Yes — `Alarm.procedure : AlarmResponseProcedureRef \| null` (`null` valid for Priority 3/4, where an ARP is optional) | This link was assumed/referenced by Sub-model 16 from early on but never actually written into the `Alarm` schema — closed in the full-document audit. |

### Scenario Simulation, Prediction & Improvement (Sub-models 17, 20)

| Question | Decision | Reasoning |
|---|---|---|
| Must `GuidanceRecommendation` always name one best scenario? | No — `goldenScenarioId` may be `null` | Equivalent options are an honest outcome; forcing a "best" answer when simulation produces a genuine tie would misrepresent the result. |
| When should normal (non-alarm) operation trigger simulation? | `SimulationPolicy.automaticMode: always \| risk-based \| none`, `riskThreshold` reusing Sub-model 14 tiers, plus a universal `manualOverrideAvailable` | Reuses the existing severity scale rather than inventing a new one; manual override was confirmed to be universal, not a fourth mode. |
| Does `RetentionPolicy` (Sub-model 19) need a different shape than `SimulationPolicy`? | No — deliberately identical shape | Both are "big-data cost vs. detail" trade-offs; one mental model serves both. |
| Does a `GuidanceRecommendation` need its own lifecycle, like a `PredictedEvent` does? | Yes — `state: Open \| Applied \| Dismissed \| Expired`, with `apply()`/`dismiss()` as `methods()` overrides | A recommendation is generated against a specific process-state snapshot and goes stale the same way a prediction does. |
| Can an `ImprovementRecommendation` ever be auto-applied at high confidence? | No — `requiresApproval: true`, fixed, no false case, even at `confidence: 1.0` | It changes how the plant runs going forward, a materially bigger decision than a single `ScenarioResult` shown in the moment. |
| Is "predictive maintenance" the same thing as "predictive analytics"? | No — predictive maintenance is one case of the broader predictive analytics category. `PredictedEvent` gained `basisType: internal-pattern \| external-forecast` to make both first-class | `basis` was previously typed as `string (Historian pattern)` only — it couldn't represent a prediction driven by an external source (weather forecast, energy price) with nothing to do with the Historian. An `external-forecast` `PredictedEvent` doesn't require a Historian to exist at all; `internal-pattern` does. Sub-model 20 §24.2 |

### AI Governance (Sub-model 21)

| Question | Decision | Reasoning |
|---|---|---|
| How is an `AIControlUnit` switched on/off? | Reuses the Sub-model 4 state machine completely unmodified — no new mechanism | An AI performing closed-loop control isn't exempt from the safety model; treating it like any other ControlUnit keeps Interlocks applicable without special-casing. |
| Can `operatingBounds` ever be empty? | Only when `target: DigitalTwin` — always required when `target: PhysicalDevice` | Unbounded action against the Digital Twin cannot cause real-world harm; unbounded action against the physical process always can. |
| Does `AIControlUnit.target` collide with `Interlock.target`? | No, and it was a mistake to treat it as if it did — briefly renamed to `controlTarget`, then reverted | The two are never the same object at once, so the shared name never actually collides in practice; the model already had a working precedent for exactly this (see `Alarm.state` vs. `Interlock.state`, Sub-model 12) — renaming was applying the naming principle where it didn't need to apply. |
| What happens when an action falls outside `operatingBounds`? | Clamped (never reaches the physical Device) *and* raises an `ImprovementRecommendation` suggesting the bound itself be reviewed | The bound might be wrong, but widening it is always a human decision — never a silent auto-adjustment. |

### Naming & Terminology (Sub-model 12) — Meta-Decisions

| Question | Decision | Reasoning |
|---|---|---|
| When should a term be renamed from its source-standard original? | Only when it already carries a conflicting meaning elsewhere in the model, or in an adjacent standard LUNEX must interoperate with | The one-sentence naming principle every other renaming decision in this log was tested against. |
| Where do naming corrections get recorded? | Sub-model 12's "Renamed Terms" register, permanently, including corrections discovered after the fact | The register's stated value is being complete, not just eventually correct — silently fixing a name without logging it would defeat its purpose. |
| What does the name `LUNEX` itself stand for? | *Layered Unified Namespace for Entities & eXtensibility* | "Entities," not "Equipment" — `LunexObject` (Sub-model 1) includes non-physical peers (`Alarm`, `Interlock`, `Zone`, etc.), so "Equipment" would have silently narrowed the backronym below the model's actual scope. |

### Recipe & Execution (Sub-model 5)

| Question | Decision | Reasoning |
|---|---|---|
| Does `RecipeExecution` need its own state machine, like `Alarm` or `ChangeRequest` do? | No — `RecipeExecution.methods()` has no override; it reuses Sub-model 4's state machine directly | PackML's states were already generalized once into Sub-model 4, and they already *are* batch-execution states — a second state machine would duplicate, not extend, the first. Sub-model 5 §9 |
| Does ISA-88's procedural hierarchy need a new level LUNEX doesn't already have? | Superseded — see Phase 15: levels renamed to `recipeLevel`, steps bound to asset levels via `runsOn` | A step's execution is just its target's own Sub-model 4 state — not a separate runtime object requiring new structure. Sub-model 5 §9 |
| Which Recipe/ProcedureElement terms are safe in LUNEX? | `recipeLevel: product \| location \| equipment \| execution`, `derivedFrom`, `RecipeElement.runsOn: area \| cell \| system \| assembly`, `childOrder`, `RecipeExecution` | ISA-88's words collide with Site/ControlUnit/System/AlarmResponseProcedure or with object-oriented terms; steps are named by the asset level that runs them |

### Identity & Access Management (Sub-model 8)

| Question | Decision | Reasoning |
|---|---|---|
| Should `Operator` (Sub-model 1, Phase 11) grow a permissions system, or should that be separate? | Separate — `Identity`/`Role`/`Permission`/`AccessGrant` built as their own sub-model; `Operator` stays deliberately minimal | Matches the "structure now, mechanism later" boundary Phase 11 explicitly drew when `Operator` was first added. Sub-model 8 §12 |
| What vocabulary does `Policy.appliesTo`, `ChangeRequest.requiredApprovals`, and `LunexObject.owner` all resolve through? | One shared `Role` vocabulary (Sub-model 8), not three separate ones | Avoids three parallel, drifting definitions of "who" across governance, change control, and ownership. Sub-model 8 §12, Sub-model 1 §5.2, Sub-model 13 §17.2 |

### Vulnerability & Patch Management (Sub-model 9)

| Question | Decision | Reasoning |
|---|---|---|
| Is `accepted-risk` a failure state or a valid end state for a `Vulnerability`? | A legitimate, permanent, *documented* end state | Distinguishes a deliberate risk-acceptance decision from incomplete triage left unresolved — both would otherwise look identical without this status. Sub-model 9 §13 |
| Does patching get its own approval flow, separate from `ChangeRequest`? | No — every `PatchRecord` requires a `ChangeRequest` reaching `Implemented` first | Patching is a change like any other; a parallel approval mechanism would duplicate Sub-model 13 rather than reuse it. Sub-model 9 §13 |

### Security Incident Response (Sub-model 10)

| Question | Decision | Reasoning |
|---|---|---|
| Is `SecurityIncident` a kind of `Alarm`? | No — a peer, both extending `LunexObject` directly | Sub-model 15 (Alarm Management, after renumbering) is explicitly process-alarm-focused; NIST CSF's Respond/Recover functions needed their own object and lifecycle, not a subtype squeezed into the alarm model's assumptions. Sub-model 10 §14 |
| How does a security-driven configuration change get tracked? | `SecurityIncident.relatedChange → ChangeRequest`, a link, not a merge of the two objects | Keeps "the incident happened" and "the configuration change it caused" governed separately, the same separation Sub-model 13 draws everywhere else it touches another object. Sub-model 10 §14 |

### Management of Change & Governance (Sub-model 13, Sub-model 1)

| Question | Decision | Reasoning |
|---|---|---|
| Should governance ("who's accountable," "what the rules are") get its own, new sub-model? | No — distributed across Sub-model 1 (`owner`) and Sub-model 13 (`Policy`) | Governance is cross-cutting, not a new domain — the same reasoning that kept `Operator` (Phase 11) out of a dedicated sub-model until IAM was genuinely needed. |
| What does `LunexObject.owner` answer, and what does it deliberately not answer? | Only "who is accountable" — not "who may act" (Sub-model 8's `AccessGrant`) and not "what the rules are" (Sub-model 13's `Policy`) | Keeping `owner` to one narrow question is what let it land on the base class without pulling the rest of governance onto every object. Sub-model 1 §5.2 |
| How does a standing `Policy` interact with a specific `ChangeRequest`'s own `requiredApprovals`? | The most specific matching `Policy` (instance match beats class match) sets a floor; a `ChangeRequest` may only raise it, never lower it | `Policy` is "governance authored once," `ChangeRequest` is "governance applied once" — the floor-only rule keeps a stricter standing policy from ever being silently bypassed by a looser one-off request. Sub-model 13 §17.2 |
| Does `VersionRecord` need its own storage mechanism, separate from the Historian? | No — reuses the Historian's (Sub-model 19) append-only storage principle directly | Avoids a second storage philosophy for what is structurally the same problem (immutable, timestamped records) the Historian already solves. Sub-model 13 §17.2 |

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
