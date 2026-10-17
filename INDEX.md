# LUNEX — OT Reference Model

**A unified, object-oriented reference model for OT, safety, security and AI — built to do what PackML and ISA-88 don't: cover the full stack from a single Sensor to the AI layer that predicts, recommends, and — with approval — acts on it, in one consistent object model.**

*Layered Unified Namespace for Entities & eXtensibility* — Entity for `LunexObject` (Sub-model 1), Namespace for the addressable path every object resolves to (Sub-model 2), Layered for the five-band structure below, eXtensibility for why five more sub-models (Recipe & Execution, Identity & Access Management, Vulnerability & Patch Management, Security Incident Response, Management of Change) could be added to the original sixteen without disturbing any of them — and why a twenty-second could be added the same way.

This index brings together the twenty-one sub-models developed so far. Sub-model 12 (Naming & Terminology) is the living glossary — consult it whenever a term's origin or reasoning is unclear.

---

## How to read this

Each sub-model is a standalone SVG diagram. Together they form one coherent model, in five bands: **Foundation (1–5)** defines the object system, the addressable hierarchy, topology, behavior, and the procedural layer every later sub-model builds on; **Safety & Security (6–10)** covers interlocks/SIFs, network segmentation, identity, vulnerability/patch posture, and incident response — each depending on Foundation, independent of each other; **Cross-cutting (11–13)** adds the data/AI layer, the naming discipline that spans everything, and governed change — independent of each other, with Management of Change able to reference any object anywhere in the model as the subject of a change; **Operator capability (14–18)** builds real-time operator-facing capability (status, alarms, guidance, awareness) on top of Capability; **Autonomous layer (19–21)** adds the historical and autonomous layer (memory, prediction, closed-loop control) on top of that same foundation.

```
Foundation                      Safety & Security            Cross-cutting
1  Object Model  ───────────┬───┬─► 6  Safety        ─┐  ┌─► 11 Data/AI ──────┐
2  Asset Hierarchy            │   ├─► 7  Zones/Conduits ├──┤                   │
3  Topology                   │   ├─► 8  IAM            │  ├─► 12 Naming       │
4  Behavior / State           │   ├─► 9  Vuln. & Patch  │  │                   │
5  Recipe & Execution ────────────┘   └─► 10 Sec. Incident ─┘  └─► 13 MOC ◄────────┘
                                                                    │  (subject: any object)
                                        Operator capability         │
                                        14 Rollup ◄──────────────────┘
                                        15 Alarm Management
                                        16 Alarm Response
                                        17 Scenario Sim.
                                        18 Situational Awareness
                                              │
                                              ▼
                                        Autonomous layer
                                        19 Historian & Analytics
                                        ├─► 20 Predictive & Improvement
                                        └─► 21 Closed-Loop AI Control
```

---

## The twenty-one sub-models

### Foundation (1–5)

### 1 — Object / Class Model
`lunex-object-model.svg`

The base of everything: `LunexObject`, the abstract class every object in LUNEX inherits from — including the optional `owner : RoleRef | null`, the only governance field on the base class (who's accountable; Sub-model 8 resolves it). Five universal classes (Sensor, Transducer, ControlUnit, SignalConverter, Actuator) cover any physical device through composable function-interfaces (Sensing / Converting / Controlling / Actuating) rather than S88's fixed categories. `Device` and `Component` split what's independently addressable from what isn't — including the optional `physicalRef` for when one physical asset (a multi-CPU rack, for instance) backs several distinct functional tags. `methods()` is a computed view, not a stored list: it returns exactly the state-transition triggers valid from an object's current state. Thirteen peers added by later sub-models — Batch, Interlock, Zone, Conduit, Identity, SecurityIncident, ChangeRequest, ChangePolicy, Alarm, GuidanceRecommendation, PredictedEvent, ImprovementRecommendation, Operator — are shown here too, connected via a shared bus rather than individual arrows, so this diagram stays the complete, uncluttered picture of the class tree.

### 2 — Asset Hierarchy / Namespace
`lunex-asset-hierarchy.svg`

A composed, addressable containment chain — Realm → Domain → Location → Area → Cell → System → Assembly → Device → Component — mapped onto Purdue levels 0–4. Any level may be skipped when trivial. Every `LunexObject.id` is derivable as a path through this chain (`lunex://Realm/.../Device`), which Sub-model 11 uses directly for telemetry addressing.

### 3 — Topology Model (Assembly)
`lunex-topology-model.svg`

How Devices are wired within one Assembly: **Integrated**, **Point-to-Point**, **Star**, **Mesh** — an axis of wiring shape, independent of two capability flags (**High-Availability**, **Cloud & Analytics**) that can apply to any shape. This is the clearest structural departure from PackML/S88, which only really describe the Point-to-Point case. An `AIControlUnit` (Sub-model 21) occupies a ControlUnit slot in this same topology — no new shape required.

### 4 — Behavioral / State Model
`lunex-state-model.svg`

The universal state machine behind `LunexObject.state` — one machine shared by every class. States are optional per object capability (a simple Sensor never touches the Locked branch). Transition labels name every purpose that reuses them (`Emergency stop / Inhibit / Lock`, `Disable / Lock`), so an Interlock's exact target is never ambiguous. Deliberately does **not** define collective/rollup status here — that question is resolved in Sub-model 14.

### 5 — Recipe & Execution Model
`lunex-recipe-execution-model.svg`

ISA-88's recipe model, laid over Sub-model 2 (where something runs) and Sub-model 4 (how it behaves) rather than invented fresh. `Recipe` keeps ISA-88's four levels under self-describing names (`recipeLevel: product | location | equipment | execution`, each linked to its parent by `derivedFrom`; in-run tuning is logged in `RecipeExecution.adjustments` and only promoted to a new Recipe through approval); `RecipeElement` replaces ISA-88's four step names with the asset level that runs the step (`runsOn: area | cell | system | assembly`, with `childOrder: sequence | parallel`) — no element for Device, because a Device has its own Sub-model 4 state, and no separate runtime object per step. `RecipeExecution` is the one execution — and the sub-model's only structural claim is that it needs **no new state machine at all**: PackML's states, already generalized once in Sub-model 4, already *are* batch-execution states, so `RecipeExecution.methods()` has no override, unlike `Alarm` or `ChangeRequest`.

---

### Safety & Security (6–10)

### 6 — Safety
`lunex-safety-model.svg`

`Interlock` becomes a first-class `LunexObject` (not a property list) so it can carry its own proof-test history. A Safety Instrumented Function is always its own Assembly, physically independent from process control, now carrying `silTarget`/`silAchieved` (plus the `pfdAvg`/`pfh` calculation behind `silAchieved`) rather than a single unverified `SIL` field — the same target/achieved split Sub-model 7 already uses for Security Level. `safetyStandard` picks which rating system an Interlock was engineered against: `IEC61508-SIL` keeps the SIF path above, while `ISO13849-PL`/`IEC62061-SIL` bring in machine safety's own `performanceLevel`/`category` fields, previously absent entirely. `SafeMotionFunction` reuses IEC 61800-5-2 unchanged for STO/SS1/SS2/SOS/SLS/SDI/SLP on a Drive. `lockType: inhibit | lock` triggers exactly the Sub-model 4 transition it corresponds to — never an arbitrary jump, including the corrected edge case: from **Off**, Inhibited is unreachable, so an inhibit-type Interlock targets Locked directly instead of blocking and waiting. Stop categories (Controlled/Quick/Emergency Stopping) are confirmed against IEC 60204-1.

### 7 — Security Zones & Conduits
`lunex-security-model.svg`

`Zone` and `Conduit` — also first-class `LunexObject`s — bring IEC 62443 into the model. This is where "Zone" (deliberately kept out of Sub-model 2's hierarchy) gets its real, single meaning. Zones commonly wrap a Purdue band; Conduits are where a Firewall/IDS ControlUnit (Sub-model 1) actually lives.

### 8 — Identity & Access Management
`lunex-iam-model.svg`

The "who's allowed to do what" question IEC 62443-3-3 SR 1.x/2.x asks and nothing in LUNEX answered until now — `Operator` (Sub-model 1) records identity and capacity, deliberately not permissions. `Identity` is the broader, permissions-capable actor (human or service-account); `Role`/`Permission` are reused unchanged from standard least-privilege RBAC practice; `AccessGrant` is the scoped, time-bounded binding that actually applies a Role to an Identity. This is also the vocabulary Sub-model 13's `requiredApprovals`, `ChangePolicy.appliesTo`, and Sub-model 1's `owner` all resolve through — one Role vocabulary, not several.

### 9 — Vulnerability & Patch Management
`lunex-vulnerability-model.svg`

IEC 62443-2-3/-4-1 and the EU Cyber Resilience Act both require tracking known vulnerabilities and patch status per asset — nothing in LUNEX tracked firmware version, CVEs, or patch state before this. `Vulnerability` carries `cveRef`/`cvss` unchanged and a `status` where `accepted-risk` is a legitimate, permanent, *documented* end state — never a silent default for incomplete triage. Every `PatchRecord` requires a `ChangeRequest` (Sub-model 13) reaching `Implemented` first: patching is a change like any other, governed the same way, not a parallel approval flow.

### 10 — Security Incident Response
`lunex-security-incident-model.svg`

NIST CSF's Respond/Recover functions and IEC 62443-2-1 incident response had no object representation — Alarm Management (Sub-model 15) is explicitly process-alarm-focused and answers a different question. `SecurityIncident` is a peer of `Alarm`, never a subtype of it, with its own `Detected → Contained → Eradicated → Recovered → Closed` lifecycle. A remediation that changes plant configuration raises a `ChangeRequest` (Sub-model 13) via `relatedChange` — the incident-response workflow and the configuration change it causes are tracked, and governed, separately, the same separation Sub-model 13 already draws everywhere else.

---

### Cross-cutting (11–13)

### 11 — Data / AI Layer
`lunex-data-ai-model.svg`

The layer PackML and S88 don't have. A **Telemetry Envelope** wraps what `LunexObject` already exposes with an address and timestamp. A **Context Layer** adds semantic relationships (`measures`, `partOf`, `semanticTag`) beyond the containment chain — what makes the data AI-ready, not just available. A **Digital Twin** is the AI-side mirror an AI model actually queries — and only ever holds the *current* state; for everything the state *was*, see Sub-model 19.

### 12 — Naming & Terminology
`lunex-naming-model.svg`

The living register: every deliberate deviation from S88/S95/PackML, with the reason (Realm/Domain, Point-to-Point/Star/Mesh, Envelope, Inventory, `Alarm.origin`, `automaticMode`, and more) — and, for balance, every term deliberately **kept** unchanged (SIL/SIF, IEC 62443, ISA-18.2). Now also the home of the UCUM convention: every `hasUnit`/`properties` value across the model must be a valid UCUM code. Closes with the one-sentence naming principle every decision above was tested against.

### 13 — Management of Change
`lunex-moc-model.svg`

Five previously ad hoc approval patterns — `ImprovementRecommendation.requiresApproval`, an Interlock/SIF modification, a Zone/Conduit reconfiguration, an `AccessGrant` escalation, an equipment/execution-level Recipe parameter change — generalized into one governed object instead of five parallel flows. `ChangeRequest` carries its own `Draft → PendingApproval → Approved/Rejected → Implemented → Verified → Closed` lifecycle and reuses Sub-model 14's Tier scale for `riskAssessment`, never a new risk vocabulary. `ChangePolicy` is the standing rule a `ChangeRequest` resolves its `requiredApprovals`/risk floor against — authored once, applied every time — and can only raise the approval bar a `ChangeRequest` must clear, never lower it. `VersionRecord` reuses the Historian's (Sub-model 19) append-only storage principle for before/after configuration snapshots, closing the gap where *that* a change happened was recorded but not *what existed* immediately before it.

---

### Operator capability (14–18)

### 14 — Collective Status (Rollup)
`lunex-rollup-model.svg`

Resolves what Sub-model 4 deferred. **Severity Tiers** (0 Critical – 3 Nominal) rank the Sub-model 4 states. **Rollup** is a computed view, not a new class: `worstTier` gives the at-a-glance badge, `tierCounts`/`contributors` keep every simultaneous condition visible. **Bubbling** means a parent only ever reads its direct children's rollups — never scans the whole tree.

### 15 — Alarm Management
`lunex-alarm-model.svg`

ISA-18.2-based. `Alarm` is a first-class `LunexObject`. **Priority is severity × actionability**, not severity alone — an alarm the operator can still prevent from escalating outranks one the system already handled. `actionable` is derived automatically from the linked Interlock's state. A new Alarm State Machine (deliberately not reused from Sub-model 4) adds shelving (always expires), operator-acknowledge as an explicit action, and a `resetMode: auto | manual` Return-to-Normal step.

### 16 — Alarm Response Guidance
`lunex-arp-model.svg`

An `AlarmResponseProcedure` is a reusable template tied to the alarm type — the same pattern as the Inventory (Sub-model 1). Mandatory for Priority 1/2 alarms, optional otherwise. Surfaces Context Layer relationships (Sub-model 11) automatically at the moment they matter — no new data source.

### 17 — Scenario Simulation & Operator Guidance
`lunex-scenario-model.svg`

Extends guidance beyond alarms to normal operation. `GuidanceRecommendation` holds a set of simulated `ScenarioResult`s tested on the Digital Twin (Sub-model 11) — a golden scenario is optional, not guaranteed. A `SimulationPolicy` (`automaticMode: always | risk-based | none`, plus a universal `manualOverrideAvailable`) decides in advance, per Assembly, when a normal setpoint change gets checked — risk-based reuses the Sub-model 14 severity tiers.

### 18 — Situational Awareness
`lunex-sa-model.svg`

No new data — a navigation contract over Sub-models 10, 11, 14 and 15. The same three signals (own state, rollup badge, top alarm) appear at every hierarchy level, top to bottom — `SecurityIncident` (Sub-model 10) surfaces through the same pattern. `jumpToWorst()` replaces manual layer-by-layer digging with one action that always lands where the manual path would. On arrival, the right context is already there.

---

### Autonomous layer (19–21)

### 19 — Historian & Analytics
`lunex-historian-model.svg`

The retrospective half of Sub-model 11: what the state *was*, not just what it *is*. The **Historian** appends every Telemetry Envelope permanently, alongside the Digital Twin, without gating it — and now also stores `VersionRecord` configuration baselines (Sub-model 13), reusing the same append-only principle rather than a second storage philosophy. `RetentionPolicy` mirrors `SimulationPolicy`'s shape exactly (`always | risk-based | none` + `manualOverrideAvailable`) — the classic big-data cost/detail trade-off, resolved with the same mental model rather than a new one. **Analytics** is descriptive, not predictive (contrast Sub-model 20), and computes the alarm-performance metrics ISA-18.2 requires — alarms/hour, bad actors, time-to-acknowledge by Priority.

### 20 — Predictive Maintenance & Improvement
`lunex-predictive-model.svg`

A third `GuidanceRecommendation.source`: `predictive`, built on the Historian rather than the live Twin or a static procedure. `PredictedEvent` (a full `LunexObject`, state: `Open | Confirmed | Dismissed | Expired`) *raises* into the ordinary Alarm system — tagged `PREDICTIVE` — rather than sitting in a second screen the operator has to remember to check. `basisType` (`internal-pattern | external-forecast`) makes explicit that predictive maintenance (Historian-derived) is one case of the broader predictive analytics category, not a synonym for it — a weather- or energy-price-driven prediction is equally first-class, and doesn't require a Historian to exist at all. `ImprovementRecommendation` (also a full `LunexObject`, state: `Proposed | UnderReview | Approved | Rejected | Applied`) always requires human approval — `requiresApproval` has no false case, even at confidence 1.0, because it changes how the plant runs rather than just informing one decision, and that approval is routed through Sub-model 13's `ChangeRequest`.

### 21 — Closed-Loop AI Control
`lunex-ai-control-model.svg`

An AI model that adjusts the process daily, modeled with almost nothing new: `AIControlUnit` is a `ControlUnit` subclass occupying an ordinary Assembly slot (Sub-models 1, 3). On/Off reuses the Sub-model 4 state machine unchanged, and an Interlock forces it exactly like any Device — including the corrected Off→Locked edge case from Sub-model 6. `operatingBounds` is required whenever `target` is the physical process, and may only be empty when `target` is the Digital Twin (Sub-model 11) — unbounded is structurally safe there, never a promise. `target` means something different here than on `Interlock` (Sub-model 6), the same way `state` already means something different on `Alarm` than elsewhere — documented, not renamed, since no object is ever both classes at once. An action outside `operatingBounds` is clamped and raises an `ImprovementRecommendation` (Sub-model 20) to review the bound itself.

---

## Brand assets

| File | Contents |
|---|---|
| `lunex-brand-concept.svg` | Color palette, logo rationale, typography |
| `lunex-logo-light.svg` / `.png` | Logo for light backgrounds |
| `lunex-logo-dark.svg` / `.png` | Logo for dark backgrounds |

---

## Open items

None outstanding in this document. This pass added five sub-models (5 Recipe & Execution, 8 Identity & Access Management, 9 Vulnerability & Patch Management, 10 Security Incident Response, 13 Management of Change) and governance — `LunexObject.owner` (Sub-model 1) and `ChangePolicy` (Sub-model 13) — reusing existing structure rather than adding a 22nd sub-model, per the project's own naming/reuse principle (Sub-model 12). Sub-model 6 (Safety) was extended with `silTarget`/`silAchieved`/`pfdAvg`/`pfh` and machine safety (ISO 13849-1/IEC 62061, `SafeMotionFunction`); Sub-model 1's diagram and prose were updated for the resulting thirteen peer classes. All twenty-one diagrams are rendered and verified (text fits its boxes, arrows end on box edges, no overlaps, within the single-page height budget), and this index, `README.md`, and `LUNEX-Specification.md` (spec text, glossary, Appendix A schema reference) are consistent with the new numbering and content as of this pass.

`PROJECT-RECORD.md` (Phases 14–16) and `CHANGELOG.md` (`[0.2]`) record this work, including the naming review (Phase 15) and the diagram layout pass with `tools/diagrams/lint_diagram.py` (Phase 16). The PDF has been rebuilt from the current specification text and all twenty-one diagrams (73 pages), and `lunex-site/index.html` carries the five-band, twenty-one-node structure. Nothing outstanding from this pass remains.
