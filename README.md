# LUNEX

**A unified, object-oriented reference model for OT, safety, security and AI.**

*Layered Unified Namespace for Entities & eXtensibility* — every object in the model, from a pressure sensor to an AI-generated recommendation, is an **Entity** (`LunexObject`); the **Namespace** is the addressable `lunex://Realm/.../Device` path every one of them lives at (Sub-model 2); **Layered** is the four-layer structure the sixteen sub-models are organized into; **eXtensibility** is why a new sub-model can be added without breaking the ones already there.

LUNEX covers what PackML and ISA-88 don't try to: one consistent object model spanning process control, safety instrumentation, cybersecurity (IEC 62443), alarm management (ISA-18.2), and the AI/data layer — from a single Sensor up to the closed-loop AI model that adjusts the process daily.

🌐 **[lunex.cloud](https://lunex.cloud)**

> **Status: early draft (v0.1).** This is a proposal, not an established standard. It has not been reviewed by an independent working group. Feedback, criticism, and pull requests are actively welcome — see [Contributing](#contributing).

---

## What's here

Sixteen sub-models, each a standalone SVG diagram, building from the base object system up through operator-facing and autonomous capability:

| # | Sub-model | Covers |
|---|---|---|
| 1 | [Object / Class Model](diagrams/lunex-object-model.svg) | `LunexObject`, five universal device classes, function-interfaces |
| 2 | [Asset Hierarchy / Namespace](diagrams/lunex-asset-hierarchy.svg) | Realm → Domain → Location → Area → Cell → System → Assembly → Device → Component, mapped to Purdue |
| 3 | [Topology Model](diagrams/lunex-topology-model.svg) | Integrated / Point-to-Point / Star / Mesh wiring, HA and Cloud & Analytics flags |
| 4 | [Behavioral / State Model](diagrams/lunex-state-model.svg) | The universal state machine behind `LunexObject.state` |
| 5 | [Safety](diagrams/lunex-safety-model.svg) | `Interlock` as a first-class object, SIF Assemblies, IEC 60204-1 stop categories |
| 6 | [Security](diagrams/lunex-security-model.svg) | `Zone` / `Conduit`, IEC 62443 |
| 7 | [Data / AI Layer](diagrams/lunex-data-ai-model.svg) | Telemetry Envelope, Context Layer, Digital Twin |
| 8 | [Naming & Terminology](diagrams/lunex-naming-model.svg) | Living register of every deliberate naming decision, and why |
| 9 | [Collective Status (Rollup)](diagrams/lunex-rollup-model.svg) | Severity Tiers, Rollup, Bubbling |
| 10 | [Alarm Management](diagrams/lunex-alarm-model.svg) | ISA-18.2-based `Alarm`, priority = severity × actionability |
| 11 | [Alarm Response Guidance](diagrams/lunex-arp-model.svg) | Reusable `AlarmResponseProcedure` per alarm type |
| 12 | [Scenario Simulation & Operator Guidance](diagrams/lunex-scenario-model.svg) | `GuidanceRecommendation`, `SimulationPolicy` |
| 13 | [Situational Awareness](diagrams/lunex-sa-model.svg) | Navigation contract: same signals at every level, `jumpToWorst()` |
| 14 | [Historian & Analytics](diagrams/lunex-historian-model.svg) | Append-only history, `RetentionPolicy`, ISA-18.2 alarm performance metrics |
| 15 | [Predictive Maintenance & Improvement](diagrams/lunex-predictive-model.svg) | `PredictedEvent`, `ImprovementRecommendation` (always requires human approval) |
| 16 | [Closed-Loop AI Control](diagrams/lunex-ai-control-model.svg) | `AIControlUnit`, `operatingBounds`, Interlock override |

A full narrative index with the reasoning behind each sub-model is in [`INDEX.md`](INDEX.md). The complete written specification — glossary, standards cross-reference, and a full schema appendix — is [`LUNEX-Specification.md`](LUNEX-Specification.md) (also available as a formatted [PDF](LUNEX-Specification.pdf)). The complete project history — every phase, every design decision, and why — is in [`docs/PROJECT-RECORD.md`](docs/PROJECT-RECORD.md).

Brand assets (logo, color palette) are in [`brand/`](brand/). The scripts that generate every diagram and the PDF from source are in [`tools/`](tools/) — LUNEX is meant to stay editable, not just readable.

---

## Design principle

> Rename a term only when it already carries a conflicting meaning elsewhere in the model, or in an adjacent standard LUNEX must interoperate with. Otherwise, reuse established vocabulary.

Every naming decision in this model — `Realm`/`Domain` instead of `Enterprise`/`Division`, `Point-to-Point`/`Star`/`Mesh` instead of PackML's terms, `Envelope` instead of `Container`, and more — is tested against this one sentence and documented in Sub-model 8.

---

## License

- **Specification and diagrams** (this repository): [CC BY 4.0](LICENSE) — free to use, adapt, and build on, with attribution.
- **Reference implementations**, if and when they exist, will be released separately under Apache 2.0.

## Contributing

This is a one-person effort so far, and it shows — it needs outside scrutiny before anyone should call it a standard. If you work in OT, process safety, or industrial cybersecurity and see something wrong, missing, or overcomplicated: say so in [Discussions](../../discussions), not Issues (Issues are for concrete bugs — a broken diagram, a build script that doesn't run). Disagreement is more useful right now than agreement. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for how design questions get resolved here, and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) for how we expect to disagree with each other.

Changes are tracked in [`CHANGELOG.md`](CHANGELOG.md).

## Citing LUNEX

See [`CITATION.cff`](CITATION.cff), or use GitHub's "Cite this repository" button in the sidebar.

## Contact

General: [info@lunex.cloud](mailto:info@lunex.cloud). Code of Conduct concerns: [conduct@lunex.cloud](mailto:conduct@lunex.cloud) (see [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)). Security issues in `tools/`: see [`SECURITY.md`](SECURITY.md) — please report privately, not as a public Issue.
