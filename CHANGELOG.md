# Changelog

All notable changes to LUNEX are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). For the reasoning behind each change, see `docs/PROJECT-RECORD.md`.

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
- Multi-interface device example (VFD/servo drive: simultaneously `Control Unit` and `Signal Converter`) added to Sub-model 1.
- `Operator` added as an eighth peer of `Device`/`Component` (`Operator extends LunexObject { role : string }`) — resolves `OperatorRef`, used by `AIControlUnit.disabledBy` but previously never defined anywhere. Deliberately minimal: identity and capacity, not a permissions system.
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
