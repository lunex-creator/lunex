# LUNEX — OT Reference Model

**A unified, object-oriented reference model for OT, safety, security and AI — built to do what PackML and ISA-88 don't: cover the full stack from a single Sensor to the AI layer that predicts, recommends, and — with approval — acts on it, in one consistent object model.**

*Layered Unified Namespace for Entities & eXtensibility* — Entity for `LunexObject` (Sub-model 1), Namespace for the addressable path every object resolves to (Sub-model 2), Layered for the four-layer structure below, eXtensibility for why a seventeenth sub-model could be added without disturbing the sixteen already here.

This index brings together the sixteen sub-models developed so far. Sub-model 8 (Naming & Terminology) is the living glossary — consult it whenever a term's origin or reasoning is unclear.

---

## How to read this

Each sub-model is a standalone SVG diagram. Together they form one coherent model: **Sub-model 1** defines the object system every later sub-model builds on; **Sub-model 2** places those objects in an addressable hierarchy; **Sub-models 3–7** add topology, behavior, safety, security and data/AI; **Sub-models 9–13** build real-time operator-facing capability (status, alarms, guidance, awareness); **Sub-models 14–16** add the historical and autonomous layer (memory, prediction, closed-loop control) on top of that same foundation.

```
1  Object Model  ──────────────┬──────────────────────────────────────────┐
2  Asset Hierarchy              │                                          │
3  Topology                     ├─► 5 Safety      ─┐                       │
4  Behavior / State              ├─► 6 Security     ├─► 9 Rollup ──┐        │
                                 └─► 7 Data/AI ──┬───┘              │        │
                                                  │                  ▼        │
                                                  │   10 Alarm Management ───┼──┐
                                                  │   11 Alarm Response ─────┤  │
                                                  │   12 Scenario Sim. ──────┤  │
                                                  │   13 Situational Awareness ◄┘
                                                  │
                                                  └─► 14 Historian & Analytics
                                                         ├─► 15 Predictive & Improvement
                                                         └─► 16 Closed-Loop AI Control
                            8  Naming & Terminology (spans all of the above)
```

---

## The sixteen sub-models

### 1 — Object / Class Model
`lunex-object-model.svg`

The base of everything: `LunexObject`, the abstract class every object in LUNEX inherits from. Five universal classes (Sensor, Transducer, Control Unit, Signal Converter, Actuator) cover any physical device through composable function-interfaces (Sensing / Converting / Controlling / Actuating) rather than S88's fixed categories. `Device` and `Component` split what's independently addressable from what isn't — including the optional `physicalRef` for when one physical asset (a multi-CPU rack, for instance) backs several distinct functional tags. `methods()` is a computed view, not a stored list: it returns exactly the state-transition triggers valid from an object's current state. Seven peers added by later sub-models — Interlock, Zone, Conduit, Alarm, GuidanceRecommendation, PredictedEvent, ImprovementRecommendation — are shown here too, connected via a shared bus rather than individual arrows, so this diagram stays the complete, uncluttered picture of the class tree.

### 2 — Asset Hierarchy / Namespace
`lunex-asset-hierarchy.svg`

A composed, addressable containment chain — Realm → Domain → Location → Area → Cell → System → Assembly → Device → Component — mapped onto Purdue levels 0–4. Any level may be skipped when trivial. Every `LunexObject.id` is derivable as a path through this chain (`lunex://Realm/.../Device`), which Sub-model 7 uses directly for telemetry addressing.

### 3 — Topology Model (Assembly)
`lunex-topology-model.svg`

How Devices are wired within one Assembly: **Integrated**, **Point-to-Point**, **Star**, **Mesh** — an axis of wiring shape, independent of two capability flags (**High-Availability**, **Cloud & Analytics**) that can apply to any shape. This is the clearest structural departure from PackML/S88, which only really describe the Point-to-Point case. An `AIControlUnit` (Sub-model 16) occupies a Control Unit slot in this same topology — no new shape required.

### 4 — Behavioral / State Model
`lunex-state-model.svg`

The universal state machine behind `LunexObject.state` — one machine shared by every class. States are optional per object capability (a simple Sensor never touches the Locked branch). Transition labels name every purpose that reuses them (`Emergency stop / Inhibit / Lock`, `Disable / Lock`), so an Interlock's exact target is never ambiguous. Deliberately does **not** define collective/rollup status here — that question is resolved in Sub-model 9.

### 5 — Safety
`lunex-safety-model.svg`

`Interlock` becomes a first-class `LunexObject` (not a property list) so it can carry its own proof-test history. A Safety Instrumented Function is always its own Assembly, physically independent from process control. `lockType: inhibit | lock` triggers exactly the Sub-model 4 transition it corresponds to — never an arbitrary jump, including the corrected edge case: from **Off**, Inhibited is unreachable, so an inhibit-type Interlock targets Locked directly instead of blocking and waiting. Stop categories (Controlled/Quick/Emergency Stopping) are confirmed against IEC 60204-1.

### 6 — Security
`lunex-security-model.svg`

`Zone` and `Conduit` — also first-class `LunexObject`s — bring IEC 62443 into the model. This is where "Zone" (deliberately kept out of Sub-model 2's hierarchy) gets its real, single meaning. Zones commonly wrap a Purdue band; Conduits are where a Firewall/IDS Control Unit (Sub-model 1) actually lives.

### 7 — Data / AI Layer
`lunex-data-ai-model.svg`

The layer PackML and S88 don't have. A **Telemetry Envelope** wraps what `LunexObject` already exposes with an address and timestamp. A **Context Layer** adds semantic relationships (`measures`, `partOf`, `semanticTag`) beyond the containment chain — what makes the data AI-ready, not just available. A **Digital Twin** is the AI-side mirror an AI model actually queries — and only ever holds the *current* state; for everything the state *was*, see Sub-model 14.

### 8 — Naming & Terminology
`lunex-naming-model.svg`

The living register: every deliberate deviation from S88/S95/PackML, with the reason (Realm/Domain, Point-to-Point/Star/Mesh, Envelope, Inventory, `Alarm.origin`, `automaticMode`, and more) — and, for balance, every term deliberately **kept** unchanged (SIL/SIF, IEC 62443, ISA-18.2). Closes with the one-sentence naming principle every decision above was tested against.

### 9 — Collective Status (Rollup)
`lunex-rollup-model.svg`

Resolves what Sub-model 4 deferred. **Severity Tiers** (0 Critical – 3 Nominal) rank the Sub-model 4 states. **Rollup** is a computed view, not a new class: `worstTier` gives the at-a-glance badge, `tierCounts`/`contributors` keep every simultaneous condition visible. **Bubbling** means a parent only ever reads its direct children's rollups — never scans the whole tree.

### 10 — Alarm Management
`lunex-alarm-model.svg`

ISA-18.2-based. `Alarm` is a first-class `LunexObject`. **Priority is severity × actionability**, not severity alone — an alarm the operator can still prevent from escalating outranks one the system already handled. `actionable` is derived automatically from the linked Interlock's state. A new Alarm State Machine (deliberately not reused from Sub-model 4) adds shelving (always expires), operator-acknowledge as an explicit action, and a `resetMode: auto | manual` Return-to-Normal step.

### 11 — Alarm Response Guidance
`lunex-arp-model.svg`

An `AlarmResponseProcedure` is a reusable template tied to the alarm type — the same pattern as the Inventory (Sub-model 1). Mandatory for Priority 1/2 alarms, optional otherwise. Surfaces Context Layer relationships (Sub-model 7) automatically at the moment they matter — no new data source.

### 12 — Scenario Simulation & Operator Guidance
`lunex-scenario-model.svg`

Extends guidance beyond alarms to normal operation. `GuidanceRecommendation` holds a set of simulated `ScenarioResult`s tested on the Digital Twin (Sub-model 7) — a golden scenario is optional, not guaranteed. A `SimulationPolicy` (`automaticMode: always | risk-based | none`, plus a universal `manualOverrideAvailable`) decides in advance, per Assembly, when a normal setpoint change gets checked — risk-based reuses the Sub-model 9 severity tiers.

### 13 — Situational Awareness
`lunex-sa-model.svg`

No new data — a navigation contract over Sub-models 7, 9 and 10. The same three signals (own state, rollup badge, top alarm) appear at every hierarchy level, top to bottom. `jumpToWorst()` replaces manual layer-by-layer digging with one action that always lands where the manual path would. On arrival, the right context is already there.

### 14 — Historian & Analytics
`lunex-historian-model.svg`

The retrospective half of Sub-model 7: what the state *was*, not just what it *is*. The **Historian** appends every Telemetry Envelope permanently, alongside the Digital Twin, without gating it. `RetentionPolicy` mirrors `SimulationPolicy`'s shape exactly (`always | risk-based | none` + `manualOverrideAvailable`) — the classic big-data cost/detail trade-off, resolved with the same mental model rather than a new one. **Analytics** is descriptive, not predictive (contrast Sub-model 12), and computes the alarm-performance metrics ISA-18.2 requires — alarms/hour, bad actors, time-to-acknowledge by Priority.

### 15 — Predictive Maintenance & Improvement
`lunex-predictive-model.svg`

A third `GuidanceRecommendation.source`: `predictive`, built on the Historian rather than the live Twin or a static procedure. `PredictedEvent` (a full `LunexObject`, state: `Open | Confirmed | Dismissed | Expired`) *raises* into the ordinary Alarm system — tagged `PREDICTIVE` — rather than sitting in a second screen the operator has to remember to check. `basisType` (`internal-pattern | external-forecast`) makes explicit that predictive maintenance (Historian-derived) is one case of the broader predictive analytics category, not a synonym for it — a weather- or energy-price-driven prediction is equally first-class, and doesn't require a Historian to exist at all. `ImprovementRecommendation` (also a full `LunexObject`, state: `Proposed | UnderReview | Approved | Rejected | Applied`) always requires human approval — `requiresApproval` has no false case, even at confidence 1.0, because it changes how the plant runs rather than just informing one decision.

### 16 — Closed-Loop AI Control
`lunex-ai-control-model.svg`

An AI model that adjusts the process daily, modeled with almost nothing new: `AIControlUnit` is a `ControlUnit` subclass occupying an ordinary Assembly slot (Sub-models 1, 3). On/Off reuses the Sub-model 4 state machine unchanged, and an Interlock forces it exactly like any Device — including the corrected Off→Locked edge case from Sub-model 5. `operatingBounds` is required whenever `target` is the physical process, and may only be empty when `target` is the Digital Twin (Sub-model 7) — unbounded is structurally safe there, never a promise. `target` means something different here than on `Interlock` (Sub-model 5), the same way `state` already means something different on `Alarm` than elsewhere — documented, not renamed, since no object is ever both classes at once. An action outside `operatingBounds` is clamped and raises an `ImprovementRecommendation` (Sub-model 15) to review the bound itself.

---

## Brand assets

| File | Contents |
|---|---|
| `lunex-brand-concept.svg` | Color palette, logo rationale, typography |
| `lunex-logo-light.svg` / `.png` | Logo for light backgrounds |
| `lunex-logo-dark.svg` / `.png` | Logo for dark backgrounds |

---

## Open items

None outstanding. The most recent audit checked the full specification text end-to-end for gaps and contradictions — not just individual sub-model updates — and found six: `Alarm.origin`/`Alarm.procedure` referenced elsewhere but missing from the `Alarm` schema itself, the Sub-model 4 state count mismatched (documented as 14, actually 15), the `methods()` override list gone stale after three more classes gained their own trigger sets, and the `Component` examples referenced in prose but never actually listed there. All six are fixed in the current specification. Earlier in the same pass: `physicalRef` gained `ComponentRef` as a valid target (multi-CPU racks), and `GuidanceRecommendation` gained its own `state` and `methods()` override, matching the pattern already set by `PredictedEvent`. `AIControlUnit.target` was briefly renamed to `controlTarget` to avoid a perceived collision with `Interlock.target`, then reverted — the two never actually collide (no object is ever both classes), and the model already had a working precedent for this exact situation in how `Alarm.state` and `Interlock.state` coexist under one shared field name.
