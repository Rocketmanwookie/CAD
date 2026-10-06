# Project status

[`PROJECT_MANAGEMENT_CHARTER.md`](PROJECT_MANAGEMENT_CHARTER.md) is the
authoritative YAML swarm roster, reporting structure, and release-gate policy.
This page records the verified product position and its next acceptance gate;
it does not duplicate or override the charter's agent structure.

## Verified project position

The project provides a pre-alpha but connected workflow: project intake,
catalog-backed PLC I/O allocation, persistent rack/module/channel occurrences,
allocated-channel-owned electrical paths, validation, and deterministic CSV/XML
exports. It is not yet a complete electrical CAD package, vendor PLC IDE, or
engineering-compliance tool.

| Capability | Verified implementation | Remaining boundary |
|---|---|---|
| Project intake | Editable `CE_Project`, intake dialog, source/missing-data tracking, CEProject XML round trip, and staged Import & Review of intake fields plus existing CEProject logical I/O rows | Broader requirements and external-fact traceability; imported physical PLC coordinates remain non-canonical |
| PLC I/O | Explicit catalog-feasibility recommendation against 120%-spare typed demand; approved CPU/module/channel review; editable engineering labels with immutable allocation keys; deterministic allocation, persistent occurrences, and safe same-type reconciliation | Manual FreeCAD acceptance evidence; catalog feasibility is not final hardware approval |
| PLC-to-field graph | Allocated channel owns the typed signal and PLC endpoint; connected paths migrate on safe same-type allocation moves | Manual save/reopen/recompute evidence in a real FreeCAD desktop |
| Wiring and routing | Typed paths, terminals, wires, geometry capture/editing, optional Cables routing, schedules | Cabinet-side power/circuit modeling and richer engineering attributes |
| FreeCAD lifecycle | Identity-aware FeaturePython objects, transaction boundaries, headless regression coverage | Recorded manual allocate/save/reopen/recompute/edit/save/reopen acceptance in FreeCAD |
| Interchange and compliance | Deterministic CEProject/XML/CSV starter boundaries | PLCopen/schematic contracts, vendor adapters, code/safety/protection and commissioning workflows |

## Next milestone

The workflow restructuring is now tracked in
[Workflow milestones](WORKFLOW_MILESTONES.md): focused plant intake/counts,
controls circuit, safety circuit, combined parts/CAD, shared cabinet/routing,
and package generation. M1 has starter implementation; M2 is the next
implementation milestone. The existing desktop acceptance below remains an
open foundation gate.

**Manual FreeCAD allocation-to-path acceptance evidence**: run and record the
documented project-intake recommendation/review → allocate → path →
save/reopen → recompute → edit → export workflow. Desktop evidence must include
the FreeCAD version, commit, screenshots, Report View output, saved FCStd, and
exported CSVs; it is not yet recorded.

## Recorded narrow desktop evidence

At `701f8ab`, the user restarted the linked FreeCAD workbench and confirmed
**New Controls Project** opens and its CPU recommendation updates after changes
to the relevant PLC/I/O inputs. This confirms the repaired intake callback
initialization in a fresh desktop process. It does not cover allocation,
electrical-path authoring, persistence, recompute, edit protection, validation,
or schedule export; those remain part of the open acceptance gate above.

## Evidence and governance

- [Project-management charter](PROJECT_MANAGEMENT_CHARTER.md) — startup,
  source-of-truth, specialist review, and release-gate procedure.
- [Agent operations ledger](AGENT_OPERATIONS_LEDGER.md) — milestone ownership,
  worktree/handoff, consultation, and evidence record.
- [Release-gate checklist](RELEASE_GATE_CHECKLIST.md) — required automated,
  specialist, manual-acceptance, and independent release decisions.
- [Change of SOP for Tony CAD](TONY_CAD_CHANGE_OF_SOP.md) — required milestone,
  handoff, evidence, and escalation procedure.
- [QA fault-tree analysis](QA_FAULT_TREE.md) — living failure-mode map and
  future QA evidence backlog.
- [PLC allocation model](../ControlForgeCAD/docs/plc-allocation.md) — allocation
  and occurrence contract.
- [Architecture](ARCHITECTURE.md) — system layers and extension boundaries.
- [Roadmap](../ControlForgeCAD/docs/roadmap.md) and
  [TODO](../ControlForgeCAD/TODO.md) — release direction and remaining scope.
- [Issue #2 roadmap acceptance map](ISSUE_2_ROADMAP_ACCEPTANCE.md) — traced
  intake-first, education, HMI-companion, and digital-twin-companion scope.

Before a milestone is called complete, Tony CAD records the exact test results,
manual checks still needed, known limitations, and the review evidence required
by the active position in the [milestone review cadence](MILESTONE_REVIEW_CADENCE.md):
two independent agent reports for positions 1–5, or the project-owner review
at position 6.
