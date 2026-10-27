# ADR 0003: Manual FreeCAD acceptance is a release gate

- Status: accepted
- Date: 2026-09-28
- Owners: FreeCAD Guy, QA Guy, Tony CAD

## Context

Pure-Python tests and import-safe stubs cannot prove a real FreeCAD desktop
workflow: workbench registration, dialogs, FeaturePython persistence,
transactions, recompute, selection behavior, or saved `.FCStd` recovery.
The allocation-to-path workflow crosses all of those boundaries.

## Decision

For an affected candidate, manual FreeCAD acceptance remains **unrun** until a
real desktop run records the FreeCAD version, candidate commit, screenshots or
Report View output, saved FCStd, and generated exports. The run follows the
manual handoff and its result is linked from the operations ledger and release
checklist. No documentation may imply the desktop acceptance passed before
that evidence exists.

## Alternatives considered

- Treat headless tests as desktop acceptance.
- Omit the manual gate until a release is imminent.
- Record only a narrative confirmation without reproducible artifacts.

## Consequences

Desktop-sensitive milestones may remain blocked even with green CI. That is a
truthful product boundary, and it creates a clear, finite evidence packet for
the FreeCAD/QA review pair.

## Evidence

- [Manual acceptance handoff](../MANUAL_FREECAD_ACCEPTANCE_HANDOFF.md)
- [Project status](../PROJECT_STATUS.md)
- [Release-gate checklist](../RELEASE_GATE_CHECKLIST.md)
