# Verified engineering inputs and project instances

Status: proposed implementation design for project-owner review. Template
review is being performed separately; no circuit generator, sizing engine,
or new instance materializer is implemented by this document.

## Outcome and recovered requirements

The project owner requests a workflow in which verified incoming power,
I/O, and controlled-load data progressively produce proposed hardware,
canonical project instances, and coordinated electrical drawing views.
The Controls Engineer agent reviews the collection templates and the
engineering prerequisites. This extends the existing
[workflow](../../governance/WORKBENCH_WORKFLOW.md),
[Phase 2 drawing requirements](../../PHASE_2_2D_SCHEMATICS_AND_LADDER_PACKAGE.md),
and [Phase 3 input requirements](../../PHASE_3_LOAD_CALCULATIONS_AND_3D_DELIVERABLES.md).

The recovered parent/child agreement is in
[Architecture section 6.3](../../ARCHITECTURE.md): coil/contact and split
PLC symbols share their physical device identity but have separate symbol
occurrence identities. Existing PLC instances already link rack to modules
and module to channels. The broader grouping below is a proposal, not a
claim that all earlier hierarchy decisions were recovered.

## Approach

Extend the existing CE identity, typed requirements, electrical graph,
and immutable snapshot model with verification, circuit, equipment, and
drawing records. The materializer and all views consume the same snapshot.
An independent drawing-first model would duplicate equipment and lose
cross-references. Immediate geometry-first generation would require cabinet
placement before the electrical design supplies its equipment requirements.
The shared graph approach supports the requested progression and the current
Release 1 engineering-data boundary.

Use JSON for new contracts, consistent with the
[JSON migration design](2026-10-25-json-first-data-contract-migration-design.md).
Keep legacy XML conversion at its import boundary. The existing XML format
cannot be represented as already supporting the new records.

## Input verification and engineering decisions

Every input fact carries identity, subject/field identity, value, unit,
source ID and locator, source revision, received date, verifier identity,
verification date, scope, and disposition. An empty value is unknown, not
zero. A general project status cannot verify individual values. Verification
means the identified fact was checked against its evidence; it does not
approve a hardware choice or a drawing for issue.

Keep separate records for input verification, proposal/selection decision,
and derivation freshness. Engineering decisions identify the reviewer, rule
or manufacturer evidence, subject, accepted input revision, and disposition.
Imported `Verified` text without its supporting evidence/reviewer remains
unverified for automatic derivation. Decisions are not supplied by an agent
pretending to be a qualified project signatory.

## Proposed ownership and reference structure

The following is a logical navigation structure. `CE_Project` remains the
existing root object; do not change its FreeCAD type simply to display groups.
Group objects or a tree presentation may expose the structure while explicit
links remain authoritative. One controls project per document remains the
supported contract; ambiguous roots are rejected.

```text
CE_Project
  Design basis
    Incoming supplies and verified facts
    Load and I/O requirements
    Engineering decisions and source records
  Physical equipment occurrences
    Assigned panel/location, or explicitly unassigned location
      PLC rack
        CPU and expansion modules
          Allocated channels and device terminals
      Power supplies
      Disconnects, contactors, protection and interface devices
      Terminal strips
        Cabinet terminals
    Field equipment locations
      Controlled loads and field devices
        Device terminals
  Electrical model
    Feeder and branch circuits
    Control-power domains and low-voltage circuits
    Signals, connection paths and wires
  Drawing package
    Sheets
      Symbol occurrences and net/continuation occurrences
  Resolver snapshots and generated artifact records
```

Each physical device has one canonical identity and one immediate physical
owner. Before a panel is selected, project-level unassigned location is a
valid explicit state; it blocks claims of completed placement, not logical
circuit definition. Location assignment changes an ownership link without
changing device identity. Rack/module/channel links are retained. The
existing CPU is a PLC module with `IsCPU`; do not create a second physical
CPU merely to add a controller-system navigation entry.

Circuits reference equipment and endpoints; they are not additional physical
owners. A coil supply circuit and a motor power circuit may reference the
same contactor. A symbol is owned by a sheet and references its canonical
device and terminal identities. Auxiliary contacts carry a parent-symbol or
device reference without becoming extra contactors in the BOM. Separate
phase conductors and repeated drawings never multiply equipment quantity.
The project device registry is an index, not a second containment parent.
PLC channels and signals express logical ownership, not separately purchased
equipment. Mounting/location and circuit-membership links are distinct from
logical ownership and do not create additional BOM occurrences.

## Progressive derivation

| Verified inputs and decisions | Proposed records and instances | Drawing readiness and limits |
|---|---|---|
| Supply source/circuit, voltage, phase/wire arrangement, frequency, earthing and neutral, fault-current evidence where applicable, boundary and upstream device references | Supply and feeder circuit records with explicit endpoints and unresolved items | Incoming single-line draft can be designated; final branch ratings remain open until their own evidence exists |
| I/O electrical requirements, actual typed counts, protocol/module compatibility and selected hardware decision | PLC configuration proposal; accepted rack/module/channel occurrences through existing allocation | I/O interface drawings use channel and terminal links; numeric count alone does not establish electrical compatibility |
| Selected PLC/module consumption, field-device and coil/relay demands, separate output-load supplies, duty/inrush, manufacturer limits, environment and reserve policy | Control-power domains, load budget, proposed supplies and accepted supply occurrences | Control-power and distribution drawings reference explicit supply/return/protection; PLC backplane capacity and external supply demand are distinct checks |
| Controlled-load nameplate and drive data, supply, operation/duty, coil/control interface, applicable rule profile and reviewed coordination decisions | Branch circuits, contactor/drive/interface and protection proposals, accepted device occurrences | Load-power views show selected or pending devices; no invented ratings/settings or blanket motor starter assumption |
| Current supply and all load-branch circuits with endpoint and decision references | Coordinated distribution network and drawing manifest | Single-line and/or expanded three-line views follow an explicit deliverable selection, even for three-phase systems |
| I/O electrical characteristics, selected devices, terminals, supply/common, approved connection intent | Low-voltage electrical circuits and schematic rung occurrences | Electrical ladder schematics can be drafted from connection intent; PLC executable logic additionally requires reviewed narrative/cause-and-effect, modes and interlocks |

I/O count cannot establish coil inrush, sensor consumption, loop power,
output-bank limits, duty, redundancy, or supply segregation. Missing inputs
remain a named blocker for the dependent result, while independent branches
can proceed. An analogue loop needs a loop diagram/interface view; do not
invent a discrete rung to satisfy coverage. Safety interfaces retain their
separate requirements, decisions and validation evidence.

## New record boundaries

All new records have a schema version, CE identity and project identity.
The following names are proposed interfaces, not existing implemented APIs.

| Record | Required relationship and behavior |
|---|---|
| `VerifiedFact` | Subject, field, value/unit, source/revision and verifier/disposition; immutable revision history |
| `EngineeringDecision` | Subject, decision scope, reviewer and accepted input revisions; no inferred approval |
| `SupplyRecord` | Supply boundary, evidence references, phase/conductor arrangement and defined endpoints |
| `CircuitRecord` | Circuit kind, upstream circuit/supply, member devices, endpoints, source facts and decision references; validate topology separately from physical ownership |
| `PowerDemandRecord` | Consuming physical occurrence plus distinct power interface and supply domain, sourced steady/transient/duty data and inclusion rule; reject duplicate counting of one demand while retaining separate backplane, external and output-load interfaces |
| `EquipmentOccurrence` | Canonical identity, requirement/selection reference, physical owner/location and decision status; separate catalog definition from installed quantity |
| `SymbolOccurrence` | Sheet owner, device reference, terminal mapping, symbol definition/profile and optional parent-symbol reference |
| `DerivedArtifact` | Source snapshot/revision, represented circuits/devices, view type, output status, open findings and regeneration state |

Current `LoadRequirement`, `IORequirement`, `HardwareRequirement` and
`ResolverSnapshot` need additive adapters/versioning rather than replacement
with parallel unconnected records. Register new roles in `identity.py` and
persisted property fact IDs in `fact_ids.py`. Publish JSON Schemas and
fixture/round-trip validation with their actual consumers.

## Reconciliation and regeneration

1. Build and validate the proposed graph in memory before changing a document.
2. Validate ownership, references, duplicate identities, circuit cycles,
   terminal mapping, required evidence and compatible decision revisions.
3. Reconcile by stable occurrence/requirement identities; unchanged instances
   retain identity, labels, terminal links and user-approved overrides.
4. Expand quantities into individually identifiable occurrences where the
   devices need independent wiring/placement; a requirement quantity is not
   itself a device occurrence. Retired occurrences retain audit references.
5. Perform document changes inside the existing transaction boundary. Reject
   ambiguous ownership, incompatible updates and orphaning of connected data.
6. Changed source revision invalidates dependent approvals and marks dependent
   proposals/drawings stale. Immutable historical snapshots remain unchanged;
   currentness/supersession is recorded in the artifact/index and a new snapshot
   captures the revised basis. Accepted devices are not silently
   swapped; their affected decisions are presented for review.
7. Re-render all selected views from one current snapshot. Preserve old issued
   artifacts and record supersession; do not overwrite their approval history.

The current allocation pruning scans document-wide roles. Before extending
ownership, constrain reconciliation to proven project-owned objects and
reject unsupported multi-root documents. This is a foundation correction,
not a new promise of multi-project support.

## Delivery increments and acceptance

1. **Verification and ownership foundation:** pure JSON records and
   validation; project-specific ownership/index checks; fact registration;
   persistence and current-model adapters. Prove missing evidence cannot
   authorize a dependent derivation and hierarchy round-trips without new
   device identities. No sizing or drawing renderer in this increment.
2. **Supply and circuits:** supply/feeder/branch graph, explicit blockers,
   topology and endpoint validation; reviewed un-rated draft single-line
   manifest from verified inputs.
3. **PLC and power domains:** reuse allocation; electrical compatibility,
   sourced power-demand budget and distinct backplane/external checks;
   supply candidates and reviewed occurrence materialization.
4. **Load interfaces:** load-specific switching/protection proposals using
   evidence-backed profiles. Motor sizing/protection work requires the
   charter's joint motor and protection consultations before approval.
5. **Drawing occurrences and adapters:** symbol/pin library, parent-child
   references, single-line/three-line/low-voltage electrical ladder outputs,
   and cross-view schedules from a shared snapshot. PLC program-generation
   is a separately reviewed scope, not inferred from I/O.
6. **Integrated acceptance:** repeated generation creates no duplicates;
   changing a source marks only its dependency closure stale; shared
   contactors appear once in the BOM; spare channels remain channels;
   save/reopen/recompute retains links; representative DI/DO/AI/AO,
   feeder and controlled-load circuits reconcile across all views.

Required regression cases also include rejection of multiple project roots,
missing roots, wrong-project references, illegal parent roles, physical-parent
cycles and orphaned owners; conflicting source facts and revision-mismatched
evidence/decisions; symbol
pins referencing a different project's device; label renames retaining IDs;
coil/main/auxiliary contact views yielding one physical BOM occurrence;
stable quantity expansion on repeated generation; distinct power interfaces
on one consumer without double counting; upstream revisions invalidating old
verification and decisions; and rollback after partial materialization fails.

Headless tests establish data and reconciliation behavior. A recorded real
FreeCAD desktop run remains required for hierarchy display, undo/rollback,
save/reopen and drawing rendering. The Controls Engineer's agent review is
advisory and distinct from qualified project design approval and independent
QA acceptance.

## Release and template status

This is an additive proposal to the current data-first release plan. Logical
instances and review manifests fit Release 1. Actual sheet rendering and
physical CAD require the separately scoped adapters and acceptance above;
do not silently call those implemented or change the release contract.
Existing supplied PDF/DXF/CSV assets retain the package's blocked provenance
disposition. Original template supplements collect inputs; they do not
resolve the source package's rights or engineering approval.
