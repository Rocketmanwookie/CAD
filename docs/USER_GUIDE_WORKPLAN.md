# User Guide task group

This record assigns durable ownership for the integraCAD Open / ControlForgeCAD
user guide. It governs the practical guide in
[`ControlForgeCAD/docs/user-guide.md`](../ControlForgeCAD/docs/user-guide.md)
and the acceptance checks that support its claims.

## Ownership and handoff

| Role | Owns | Required handoff |
|---|---|---|
| Tony CAD | Scope, sequence, integration, and truthful status | Selects guide workflows from verified MVP behavior and resolves cross-role findings. |
| FreeCAD Guy | UI commands, selection behavior, persistence, and manual FreeCAD procedure | Verifies command names/guards and records the exact FreeCAD version, visible result, save/reopen result, and exceptions when a manual run occurs. |
| QA Guy | Reproducible user-guide acceptance checks | Separates automated evidence from desktop-only checks and rejects unsupported guide claims. |
| Docu Nerd | User-facing prose, navigation, limitations, and change history | Keeps guides, README, roadmap, and changelog aligned with delivered behavior. |

Tony CAD owns the final guide integration. No guide may claim a manual FreeCAD
result until FreeCAD Guy records it and QA Guy accepts the evidence.

## Initial guide scope

The first guide covers the verified controls-design vertical slice:

1. create a project and choose a catalog PLC;
2. allocate I/O and inspect materialized rack/module/channel occurrences;
3. create a typed path from an allocated channel through a terminal strip to a
   field device;
4. validate and export the resulting project; and
5. save/reopen as a **manual acceptance procedure**, not a completed claim.

It deliberately excludes electrical-code compliance, final panel approval,
schematic generation, vendor PLC projects, automatic routing, and guaranteed
vendor CAD fidelity.

## Acceptance evidence

| Check | Evidence owner | Current state |
|---|---|---|
| Allocation, channel/signal/path linkage, endpoint-authoring, and edit guard tests | QA Guy | Automated test coverage required and currently available. |
| Workbench load, dialogs, object visibility, selection behavior, save/reopen, and Undo/Redo | FreeCAD Guy | Manual desktop verification required; not yet recorded for the current workflow. |
| Command/output paths and documented limitations | Docu Nerd | Documentation review required for each guide change. |

## Maintenance trigger

Update the guide and this work plan when a command's user-visible behavior,
selection contract, persisted property, export schema, validation finding, or
manual acceptance status changes. Link rather than duplicate detailed design
contracts from the architecture, roadmap, and PLC-allocation documentation.

Allocation changes are a guide-maintenance trigger: document same-type move
migration, and state that dependent removals and type changes require explicit
engineering resolution.
