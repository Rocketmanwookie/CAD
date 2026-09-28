# Issue #2 roadmap acceptance map

This map makes the acceptance scope of GitHub Issue #2 —
"IntegraCAB Open roadmap: intake-first workflow, education docs, HMI and
digital twin companion workbenches" — auditable without presenting deferred
companion products as implemented functionality.

## Acceptance map

| Issue outcome | Authoritative implementation or roadmap evidence | Current boundary |
|---|---|---|
| Integration-first controls-engineering orchestration | [Integration-first policy](../ControlForgeCAD/docs/integration-first-policy.md), [roadmap](../ControlForgeCAD/docs/roadmap.md), and [master TODO](../ControlForgeCAD/TODO.md) | IntegraCAB Open captures, validates, and hands off structured controls data; it does not replace specialist CAD, BOM, BIM, PLC, HMI, ERP, or vendor tools. |
| Intake-first workflow | [Intake matrix](../ControlForgeCAD/docs/intake-matrix.md), role-based templates in [`ControlForgeCAD/templates`](../ControlForgeCAD/templates), CEProject schema/import-export work, and Phase 1 in the [master TODO](../ControlForgeCAD/TODO.md) | Starter intake and validation are implemented; incomplete stakeholder/template coverage and broader CEProject sections remain roadmap work. |
| Education for developing controls engineers | [Controls Engineering Learning Path](../ControlForgeCAD/docs/learning-path.md), [glossary](../ControlForgeCAD/docs/glossary.md), and [standards/resource map](../ControlForgeCAD/docs/standards-resource-map.md) | Documentation orients learners and points to authoritative sources. It does not reproduce restricted standards or vendor manuals, and it does not substitute for qualified engineering judgment. |
| Future HMI/SCADA companion | [Companion Workbenches](../ControlForgeCAD/docs/companion-workbenches.md) and the HMI roadmap in [`TODO.md`](../ControlForgeCAD/TODO.md) | A future, versioned CEProject extension may reference existing project, signal, and electrical-path identities while adding its own hierarchy, alarm, mode/state, and screen entities. Those companion entities and any vendor HMI editor are explicitly deferred from the initial workbench scope. |
| Future digital-twin/simulation companion | [Companion Workbenches](../ControlForgeCAD/docs/companion-workbenches.md), [roadmap](../ControlForgeCAD/docs/roadmap.md), and the parity audit’s [digital-twin boundary](../ControlForgeCAD/docs/autocad-electrical-plc-parity-audit.md) | The future companion links geometry, I/O, process state, sensors, actuators, faults, and test cases through stable identities. No runtime, physics, or PLC simulation is claimed as delivered. |

## Issue completion criteria

Issue #2 can be closed as a roadmap/documentation issue when the map above is
kept discoverable from project status, and the linked documents remain aligned
with the current implementation boundary. It must not be used to declare the
deferred HMI or digital-twin companions complete.

Any future implementation milestone must start a separate entry in
[`AGENT_OPERATIONS_LEDGER.md`](AGENT_OPERATIONS_LEDGER.md), identify its
specialist and SME evidence, and pass the applicable
[`RELEASE_GATE_CHECKLIST.md`](RELEASE_GATE_CHECKLIST.md). Tony CAD may
coordinate that evidence but cannot replace the review evidence required by
the active cycle position in
[`MILESTONE_REVIEW_CADENCE.md`](MILESTONE_REVIEW_CADENCE.md).
