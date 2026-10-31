# PLC control drawing and documentation rollout plan

## Purpose

This plan describes how integraCAD Open will introduce a controlled PLC
control-drawing and documentation capability. The intended outcome is a
package from which a qualified technician can trace a field signal—such as a
proximity sensor—through cable and terminal connections to the PLC input,
controller address, and associated functional/test records.

The rollout delivers usable, reviewable increments. It does not treat a
template, an export, or a successful automated test as electrical-design,
safety, or IEC 61082-1 compliance approval. Each release remains subject to
the applicable project requirements, the current standard edition, and
qualified engineering review.

## Target operating model

The source of truth is the typed project model: project identities, field
devices, I/O signals, PLC allocations, terminals, wires, cables, and their
connections. Drawings and schedules are coordinated projections of that same
model, not separately maintained sources of truth.

```text
Approved project facts and I/O requirements
                    |
                    v
PLC allocation + field/terminal/wire connection records
                    |
                    v
Controlled resolver snapshot
                    |
       +------------+-------------+-------------+
       |            |             |             |
       v            v             v             v
 I/O list     terminal plan   cable/connection  PLC/loop drawings
       \            |             |             /
        \-----------+-------------+------------/
                    v
      FAT/SAT evidence and controlled as-built issue
```

A release may only state that an output is *coordinated* when all of its
constituent artifacts can be related to the same project revision or immutable
resolver snapshot. A review artifact with unresolved links is allowed when
clearly marked; a released/as-built package is not.

## Rollout principles

- Preserve stable identities. Tags, terminals, cable/core identifiers, PLC
  coordinates, controller addresses, and document references must not rely on
  mutable labels or drawing order.
- Make missing information visible. Missing or conflicting data blocks a
  released package; it is never silently guessed.
- Start with traceability before graphics. A reliable data path and schedules
  are prerequisites for generated PLC drawings.
- Keep controls and safety distinct until the shared-cabinet phase, while
  preserving their common identifiers and connection rules.
- Use supplied document templates only as review-controlled source material.
  Their provenance/reviewer gate remains in force.
- Validate at each phase with automated checks, a representative project, and
  an independent engineering/manual FreeCAD review appropriate to the risk.

## Phases

| Phase | Objective | Primary delivery | Exit gate |
|---|---|---|---|
| 1 — IEC 61082-1 addressing traceability baseline | Define and verify the complete, bidirectional device-to-controller trace for a representative PLC input, and establish the controlled project starter records | Starting project documentation, preliminary BOM, I/O schedule, project conventions, document index, IEC 61082-1 addressing/traceability design basis, acceptance example and test method | **Complete for the template baseline**; live projects still require populated/issued records, PLC-configuration reconciliation, and FAT/SAT evidence |
| 2 — 2D system schematics and ladder package | Define the 2D system, power, low-voltage, PLC I/O, and ladder views required for every allocated I/O point and controlled load | Drawing-set definition, ladder-coverage rules, power/protection and low-voltage requirements, cross-reference rules, and review record | Controlled review confirms all-I/O coverage and bidirectional DI/DO/AI/AO traceability; ratings and safety decisions are approved or explicitly unresolved |
| 3 — Load calculations, wire schedule, and 3D deliverables | Capture/validate project and I/O data, allocate I/O, then develop source-backed load, fault-current, and conductor/protection calculation records and spatial routes | Intake/allocation/signal-path records, load/fault/conductor/protection records, wire schedule, 3D cabinet drawing, 3D system drawing where available, or 2D route and length-estimate package | Save/reopen preserves stable allocation/path identities; every circuit has an evidence-backed or explicitly blocked result; every wire has endpoints and route/length status; cabinet geometry and system route/fallback are reviewed |
| 4 — Resolver-backed engineering package | Produce coordinated review artifacts from one snapshot | Load/I/O requirements, hardware-class proposals, panel-capacity envelope, BOM, I/O, YAML, CEProject XML, CAx manifest, cost inputs | Every output shares a snapshot; rules/evidence and unresolved engineering decisions are visible; independent review is recorded |
| 5 — Package coordination and drawing generation | Generate or adapt the approved 2D/3D package from controlled data and coordinate it with functional documents | Drawing generator/adapters, package index, revision control, traceability matrix, FDS/SDS/cause-and-effect/alarm/FAT/SAT links | Issued references all resolve and every drawing/schedule agrees with the source snapshot and functional-document links |
| 6 — CAD realization and as-built package | Realize reviewed source data in the physical cabinet and final documentation | Checked vendor CAx, placement/routing, coordinated 2D/3D cabinet sheets, final wire schedule, FAT/SAT and as-built record set | Installed panel and deployed PLC configuration reconcile to the same issue; deviations are dispositioned; handover is approved |

## Phase detail

### Phase 1 — IEC 61082-1 addressing traceability baseline

Establish the project reference-designation scheme for equipment, terminal
strips, cables, wires, PLC hardware, addresses, drawing sheets, and zones.
Adopt the [IEC 61082-1 addressing and signal-traceability design basis](../ControlForgeCAD/templates/controls-document-package/IEC-61082-1-Addressing-and-Traceability.md)
as the project template, then tailor it under engineering review. Confirm the
document package index and define who owns drawing issue, PLC configuration,
FAT, SAT, and as-built reconciliation.

Create the controlled starting project-documentation set, preliminary BOM,
and I/O schedule at the same time. The Phase-1 deliverable definition states
the required fields and review boundaries in
[IEC 61082-1 Phase 1 traceability acceptance](IEC_61082_1_PHASE_1_TRACEABILITY_ACCEPTANCE.md).

Do not proceed until the project team has agreed which documents are required
and how a cross-reference is rendered. This avoids building allocations that
cannot later be located in a drawing package. The detailed Phase-1 acceptance
method and bidirectional sensor example are in
[IEC 61082-1 Phase 1 traceability acceptance](IEC_61082_1_PHASE_1_TRACEABILITY_ACCEPTANCE.md).

### Phase 2 — 2D system schematics and ladder package

Phase 2 establishes the required 2D system drawings and schematics: incoming
power from supply breaker through distribution and controlled-load protection,
low-voltage control-power distribution, PLC digital/analogue I/O interfaces,
and ladder diagrams or explicit function-block references for every active
allocated I/O point. The detailed drawing-set definition, coverage rule, and
acceptance record are in
[Phase 2 — 2D system schematics, PLC I/O, and ladder package](PHASE_2_2D_SCHEMATICS_AND_LADDER_PACKAGE.md).

No drawing symbol, generic protective-device class, or ladder representation
constitutes a released protective-device selection, safety validation, or
approval for construction. Unresolved decisions must be visible to review.

### Phase 3 — Load calculations, wire schedule, and 3D deliverables

Phase 3 defines the complete calculation and spatial deliverable set: load
calculations, fault-current and conductor/protection calculation records, wire
schedule, 3D control-cabinet drawings, and 3D system drawings. Where system
3D geometry is unavailable, it requires an issued 2D route/render and an
auditable wire-length estimate instead. The required inputs, route-evidence
levels, deliverables, and review gate are in
[Phase 3 — load calculations, wire schedule, and 3D deliverables](PHASE_3_LOAD_CALCULATIONS_AND_3D_DELIVERABLES.md).

#### Phase 3 foundation records

Implement and validate the Project & Plant and I/O Count workflow. Capture
the known control context, project facts, actual I/O demand, and spare policy.
Create named I/O points early; preserve their canonical identity if labels or
hardware selection later change.

Select reviewable PLC hardware, allocate channels deterministically, and
record the connection path from the allocated point through PLC terminals,
internal wiring, terminal strips, cable/core, and field device. Export I/O,
terminal, and connection schedules from those typed records.

The output is a validated planning and signal-path dataset, not a finished
circuit or panel design. The phase is complete only after representative
project data survives FreeCAD save/reopen, missing facts are explicitly
reported, and a field tag can be followed through a unique terminal/wire path
to its PLC coordinate and address.

### Phase 4 — Resolver-backed engineering package

Build on the allocated signal model to capture loads and I/O requirements,
propose transparent generic hardware classes, calculate a panel-capacity
envelope, and issue the Release-1 export set from a single resolver snapshot.
This is the first major-release data and handoff capability defined in the
[first major release contract](FIRST_MAJOR_RELEASE_CONTRACT.md).

Any unresolved protection, conductor, safety, rating, environmental, or
vendor-selection decision must be exported as a review item—not converted into
an implied design choice.

### Phase 5 — Package coordination and drawing generation

Generate or adapt the Phase-2 drawing set from controlled data in this order:

1. cover sheet, document index, symbols, reference convention, and revisions;
2. PLC hardware and I/O sheets;
3. field-loop/signal sheets and sheet-zone continuations;
4. terminal plans, cable schedules, and connection/wire schedules;
5. power/control-supply and safety-interface views required by the Phase-2
   definition; and
6. cross-links to the control narrative, FDS/SDS, cause-and-effect, alarm,
   FAT, and SAT records.

For every published signal, the generated or reviewed views must agree with
the source snapshot on device tag, cable/core, terminal, wire, PLC module/
channel, controller address, and functional reference. Changes require
reconciliation of all affected views in the same controlled revision.

### Phase 6 — CAD realization and as-built package

Consume the released resolver snapshot and controlled CAx assets to make the
physical cabinet representation. Validate placement, mounting, routing,
clearances, and provenance as part of the subsequent CAD-realization release;
do not represent a capacity envelope or starter geometry as a final cabinet.

During FAT and SAT, record trace tests against the issued drawings and the
deployed PLC configuration. The as-built issue is produced only after installed
terminal/cable/wire conditions, PLC address/configuration, changes, and test
evidence have been reconciled and approved.

## Readiness checklist between phases

Before promoting a phase, record the following in the release evidence:

| Area | Required confirmation |
|---|---|
| Scope | The target workflow, included signal types, and explicit non-claims are agreed |
| Data | Required identifiers are complete, stable, unique, and round-trip through save/reopen |
| Validation | Automated validation detects duplicate/conflicting identifiers and broken links |
| Trace test | A representative signal can be followed from field device to functional/test record and back |
| Exports | Artifacts identify their source revision/snapshot and fail or are visibly marked when incomplete |
| Reviews | Required engineering, QA, provenance, and manual FreeCAD evidence is recorded |
| Change control | A change’s affected schedules, drawings, PLC configuration, and test evidence are identifiable |

## Release communication

Use the following language when communicating status:

| State | Approved description |
|---|---|
| Foundation | “The project captures and validates structured controls data.” |
| Path-ready | “The project can produce reviewable I/O, terminal, and connection traces from typed records.” |
| Package-review | “The project can produce snapshot-linked review artifacts with explicit unresolved decisions.” |
| Drawing-coordinated | “A reviewed package has resolved cross-references for the stated scope and revision.” |
| As-built handover | “The approved package is reconciled to the installed panel and deployed PLC configuration.” |

Avoid “IEC compliant,” “approved for construction,” “released panel design,”
or “as built” unless the responsible authority has completed the required
project-specific review and approval.

## Dependencies and risks

| Dependency or risk | Control |
|---|---|
| Incomplete or changing field data | Use missing-data gates and controlled change records; do not allocate or publish silently inferred values |
| Vendor address/terminal behavior | Retain vendor-native syntax and source/version evidence; test against selected hardware/configuration |
| Template provenance and rights | Keep the supplied package blocked until its provenance register and reviewer disposition are complete |
| Divergent drawing and PLC data | Require snapshot/revision identifiers and automated reconciliation before package issue |
| CAD geometry treated as engineering approval | Keep generic capacity/envelope outputs distinct from checked vendor CAx and placement/routing approval |
| Safety scope leakage | Keep safety requirements, decisions, and acceptance evidence in their own reviewed workflow |

## Related plans and controls

- [Workflow restructuring milestones](WORKFLOW_MILESTONES.md) — the current
  implementation sequence and acceptance checkpoints.
- [First major release contract](FIRST_MAJOR_RELEASE_CONTRACT.md) — Release-1
  resolver/export scope and Release-2 CAD-realization boundary.
- [Controls workbench roadmap](../ControlForgeCAD/docs/roadmap.md) — product
  roadmap and present capability boundary.
- [Controls document package](../ControlForgeCAD/templates/controls-document-package/README.md)
  — source template inventory and provenance warning.
- [Release gate checklist](RELEASE_GATE_CHECKLIST.md) — evidence to record for
  an actual project or product release.
