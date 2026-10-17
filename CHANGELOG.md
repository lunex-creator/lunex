# Changelog

All notable changes to LUNEX are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). For the reasoning behind each change, see `docs/PROJECT-RECORD.md`.

## [0.2] — Draft (2026-10-17)

### Added — five new sub-models and cross-cutting governance

- **Sub-model 5 — Recipe & Execution Model**: `Recipe` (`recipeLevel: product | location | equipment | execution`, linked by `derivedFrom`) and `RecipeElement` (`runsOn: area | cell | system | assembly`, `childOrder: sequence | parallel`) layered over Sub-models 2 and 4. ISA-88's General/Site/Master/Control and Procedure/Unit Procedure/Operation/Phase were renamed because *site*, *control*, *unit*, *procedure*, *operation* and *method* already mean something else in LUNEX or in object orientation. `RecipeExecution` reuses Sub-model 4's state machine directly — no override.
- **Sub-model 8 — Identity & Access Management** (renumbered from the former Sub-model 8, Naming & Terminology, now Sub-model 12): `Identity`, `Role`, `Permission`, `AccessGrant`.
- **Sub-model 9 — Vulnerability & Patch Management**: `Vulnerability` (`cveRef`/`cvss`), `PatchRecord`, gated behind an `Implemented` `ChangeRequest`.
- **Sub-model 10 — Security Incident Response**: `SecurityIncident`, a peer of `Alarm`, `Detected → Contained → Eradicated → Recovered → Closed`, with `relatedChange → ChangeRequest`.
- **Sub-model 13 — Management of Change**: `ChangeRequest`, `Approval`, `VersionRecord`, generalizing five previously ad hoc approval patterns into one governed lifecycle.
- `LunexObject.owner : RoleRef | null` (Sub-model 1) — the only governance field on the base class; answers "who's accountable," nothing more.
- `ChangePolicy extends LunexObject` (Sub-model 13) — a standing approval rule (`appliesTo`, `changeTypes`, `requiredTier`, `requiredApprovals`, `minApprovals`, `rationale`) a matching `ChangeRequest` resolves against; can only raise the required-approvals/risk floor, never lower it.
- Sub-model 6 (Safety) extended: `silTarget`/`silAchieved` (plus `pfdAvg`/`pfh`) replace a single unverified `SIL` field; machine safety (`safetyStandard`, `performanceLevel`, `architectureCategory` per ISO 13849-1/IEC 62061) and `SafeMotionFunction` (IEC 61800-5-2) added.
- All five new sub-models given their own diagram; Sub-model 6's and Sub-model 1's diagrams extended/restructured to fit the new content and classes.
- Sub-model 12 register extended with `Recipe.derivedFrom`, `RecipeExecution.quantityTarget`, the kept terms `Recipe` and `golden`, and the new vocabulary `RecipeElement`, `ParameterAdjustment`, `ChangeRequest`; the specification text of §16 now lists all v0.2 renames. Security, Vulnerability and Recipe & Execution diagrams tidied (box sizes, arrows, state-machine excerpt).
- Code blocks in the specification (class schemas and Appendix A) no longer exceed 84 characters per line: field comments moved to their own indented lines, long type unions wrapped, so nothing needs horizontal scrolling. The example path in Sub-model 2 was shortened accordingly (`lunex://AcmeCorp/Benelux/Rotterdam/Utilities/Boilerhouse/Boiler-1/Loop-3/PT-101`).
- Writing convention added to Sub-model 12: terms with a schema in Appendix A are always CamelCase (`ControlUnit`, `SignalConverter`, `AlarmResponseProcedure`); concepts without a schema keep spaces (Digital Twin, Telemetry Envelope, Context Layer). Applied across the specification, diagrams, documentation and website.
- PDF: the Sub-model 12 diagram was made more compact (four-column vocabulary panel, tighter register rows) so it fits on one page with its heading, and the PDF build no longer leaves a blank page when a horizontal rule falls directly before a chapter.
- Diagram layout pass on the new and extended sub-model diagrams (Safety, Object Model, IAM, Vulnerability, Security Incident, MOC, Recipe & Execution): boxes enlarged to fit their text, arrows re-routed to end on box edges, overlapping text/arrow/box cases removed. New `tools/diagrams/lint_diagram.py` renders an SVG and reports text overflow, text overlap, arrows that miss a box and lines through text.

### Changed

- Renumbered Sub-models 8–16 to 12–21 to make room for the five insertions; all cross-references across the specification, glossary, Appendix A, `INDEX.md`, and `README.md` updated accordingly.
- `README.md` and `INDEX.md` reorganized into five bands (Foundation 1–5, Safety & Security 6–10, Cross-cutting 11–13, Operator capability 14–18, Autonomous layer 19–21), replacing the original four-layer grouping.
- Backronym updated: *Layered Unified Namespace for Entities & eXtensibility* now also explains why five more sub-models could be added without disturbing the original sixteen.

- **Naming review.** `Operator.role` → `jobTitle` (`Role` is an IAM class); `Vulnerability.status` → `state` (own value space; "status" means Rollup); `category` → `architectureCategory`; `Policy` → `ChangePolicy` (Simulation-/Retention-/security-policy already exist); band 11–13 "Capability" → "Cross-cutting"; Sub-model 7 "Security" → "Security Zones & Conduits"; Recipe `level` → `recipeLevel` (values `product | location | equipment | execution`), `ProcedureElement` → `RecipeElement`, with ISA-88's four step names replaced by the asset level that runs each step (`runsOn`). All logged in Sub-model 12's register, whose diagram was extended with the new renames, kept terms and vocabulary.
- **Recipe structure bound to the asset hierarchy.** `RecipeElement.runsOn : area | cell | system | assembly` (a child runs on a lower level than its parent), `target`, typed `equipmentClass : ClassRef`, `childOrder : sequence | parallel`; `Recipe.plan` → `structure`; `RecipeExecution.currentStep` → `currentSteps`. No element for Device (it has its own Sub-model 4 state). `area` allows multi-cell recipes, which ISA-88 does not model.
- **Recipe & Execution.** `Batch` → `RecipeExecution` (neutral across batch, campaign, discrete and continuous production); new `quantityTarget`, `adjustments` (in-run tuning log), `Recipe.goldenExecution` and `Recipe.basedOnExecution`; sub-model retitled "Recipe & Execution Model", diagram renamed `lunex-recipe-execution-model.svg`.
- **Diagram numbering.** Every diagram header and cross-reference still used the pre-0.2 sub-model numbers; all 21 diagrams regenerated with the current numbering.

### Fixed — second diagram pass

- Composition diamonds now sit on the owning box's edge in all diagrams; Object Model lollipops and the Actuator inheritance line no longer cross labels; text overflow and overlaps fixed in the Rollup, Topology, Scenario, Historian, Data/AI and Predictive diagrams.
- Plural of schema-bearing classes written as "ControlUnit objects" (not "ControlUnits") in the specification and diagrams.

### Fixed

- Appendix A's Sub-model 13 schema block, misplaced after Sub-model 17 since an earlier renumbering, moved to its correct numerical position.
- §1.2's "Intentions" bullet still referenced "Sub-model 8" meaning Naming & Terminology; corrected to Sub-model 12.

## [0.1] — Draft

Initial public draft. Sixteen sub-models, full specification, glossary, and Appendix A schema reference.

### Fixed — full-document audit

- `Alarm.origin` was referenced in three other places in the specification but never actually added to the `Alarm` schema itself. Added.
- `Alarm.procedure` — same pattern: referenced by Sub-model 11 as an existing link, never defined on `Alarm`. Added.
- Glossary claimed `State` (Sub-model 4) was a 14-value enumeration; the documented states actually total 15 (5 stable, 10 transient). Corrected.
- The `methods()` glossary entry and Sub-model 16's prose both still listed only `Alarm` and `Interlock` as overrides, stale after three more classes gained their own trigger sets. Updated.
- The specification referenced a `Component` examples list ("Processor", etc.) as if it were written into Sub-model 1's prose; it only ever existed in the diagram. Added to the prose.
- `System` (Sub-model 2) was incorrectly defined as "a control system (DCS/SCADA/PLC)"; corrected to "a functional unit within a Cell, equivalent to ISA-88's Unit."

### Added

- `Device.physicalRef : DeviceRef | ComponentRef | null` — models one physical asset (e.g. a multi-CPU PLC rack) backing several functionally distinct tags; also gives Sub-model 3's "Integrated" topology a checkable definition.
- `LunexObject.methods()` formalized as a computed view of valid Sub-model 4 transition-triggers for the object's current state, rather than an unused attribute. Five classes (`Alarm`, `Interlock`, `GuidanceRecommendation`, `PredictedEvent`, `ImprovementRecommendation`) override it with their own trigger sets.
- Explicit scope boundary: continuous operational functionality (a PID loop, continuous sampling) is out of scope for `methods()`; documented where it does live (`properties`, Telemetry Envelope, `operatingBounds`).
- `GuidanceRecommendation.state : Open | Applied | Dismissed | Expired`, matching the lifecycle pattern already established for `PredictedEvent`.
- `votingArchitecture` (IEC 61508 MooN notation) added to SIF Assemblies, mandatory per layer (sensor / logic solver / final element) — distinct from Sub-model 3's `High-Availability` flag, which is about uptime, not SIL integrity.
- `Appendix A — Schema Reference`, collecting every class's schema from all sixteen sub-models in one place.
- Multi-interface device example (VFD/servo drive: simultaneously `ControlUnit` and `SignalConverter`) added to Sub-model 1.
- `Operator` added as an eighth peer of `Device`/`Component` (`Operator extends LunexObject { jobTitle : string }` (originally `role`; renamed in 0.2)) — resolves `OperatorRef`, used by `AIControlUnit.disabledBy` but previously never defined anywhere. Deliberately minimal: identity and capacity, not a permissions system.
- `PredictedEvent.basisType : internal-pattern | external-forecast` — makes explicit that predictive maintenance (Historian-derived) is one case of the broader predictive analytics category, not a synonym for it. An `external-forecast` prediction (e.g. weather, energy price) doesn't require a Historian to exist at all.
- `LunexObject.coordinates : { lat, lon } | null` — optional geographic position, on the base class rather than only `Location` (Sub-model 2), since individual objects within one Location can be genuinely distributed (a pipeline's valves, a wind farm's turbines).
- The backronym **Layered Unified Namespace for Entities & eXtensibility** adopted and documented in `README.md`, `LUNEX-Specification.md` §1, and `INDEX.md`.
- `SECURITY.md`, GitHub issue templates (bug report, documentation correction), and a pull request template added to the repository.

### Changed

- Sub-model 4's Off→Locked edge case corrected: an inhibit-type Interlock firing while the target is already `Off` now drives directly to `Locked` (via `Off→Locking→Locked`), rather than blocking and waiting — `Inhibited` is structurally unreachable from `Off`. Documented transparently in Sub-model 5 §9.4 rather than silently rewritten.
- Sub-model 4 transition labels relabeled (`Emergency stop / Inhibit / Lock`, `Disable / Lock`) to make dual-use transitions explicit.

### Considered and reverted

- `AIControlUnit.target` was briefly renamed to `controlTarget` to avoid a perceived collision with `Interlock.target`. Reverted: the two fields are never on the same object at once, so they never actually collide — the model already had a working precedent for this exact situation (`Alarm.state` vs. `Interlock.state`, documented per-class rather than renamed). See `docs/PROJECT-RECORD.md`, Phase 9.

## [0.0] — Foundation

- Initial sixteen sub-models built: Object/Class Model, Asset Hierarchy, Topology, Behavioral/State, Safety, Security, Data/AI Layer, Naming & Terminology, Collective Status (Rollup), Alarm Management, Alarm Response Guidance, Scenario Simulation, Situational Awareness, Historian & Analytics, Predictive Maintenance & Improvement, Closed-Loop AI Control.
- Brand identity established (color palette, logo).
- `SimulationPolicy`/`RetentionPolicy` unified around `automaticMode: always | risk-based | none` + universal `manualOverrideAvailable`.
- `Alarm.priority` corrected to `severity × actionable`, not severity alone.
