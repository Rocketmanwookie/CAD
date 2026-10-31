# Phase 3 — Load calculations, wire schedule, and 3D deliverables

## Objective

Phase 3 develops the calculation and spatial data needed to turn the Phase-2
schematics into a reviewable cabinet and system design. It delivers a
traceable load-calculation package, fault-current and conductor-sizing inputs
and results, a wire schedule, a 3D control-cabinet representation, and a 3D
system representation where geometry is available.

When 3D system geometry is unavailable, the alternative deliverable is an
issued 2D route/render together with auditable wire-length estimates. The
fallback must identify the route basis, allowance, and confidence level for
each affected circuit; a drawing view by itself is not a wire-length estimate.

Before calculation, the project must capture and validate plant/load facts and
actual I/O demand, allocate PLC points, and record typed device, terminal,
wire, and cable paths. These Phase-3 foundation records retain stable
identities through save/reopen and supply the endpoints and loads used by the
calculation and schedule records below.

“Full calculation” means every included load and circuit has an identified
calculation record, inputs, method/version, result, assumptions, source
evidence, and reviewer disposition. It does not mean that missing field or
utility data has been assumed, or that an unreviewed calculation is approved
for construction.

## Required inputs and data-quality states

Capture each value with its source, units, revision/date, and status:
`verified`, `provided-unverified`, `estimated`, `assumed-for-review`,
`missing`, or `not-applicable`. A released result cannot depend on `missing`
data. An `estimated` or `assumed-for-review` value requires an explicit
engineering decision and must remain visible in every affected deliverable.

| Domain | Minimum inputs |
|---|---|
| Incoming supply | Nominal voltage, phase/wire arrangement, frequency, grounding/earthing arrangement, source/transformer/generator identity, available fault-current data at the defined point, and supply-protection details |
| Loads | Tag, equipment class, quantity, voltage, phase, nameplate current/power, power factor/efficiency if applicable, duty/demand, starting/inrush or drive information when applicable, control method, operating mode, and source evidence |
| Distribution/protection | One-line path, upstream device data, intended protective device and settings where known, panel/assembly ratings, and all unresolved selection decisions |
| Conductors/cables | Circuit endpoints, conductor material/insulation, installation method, conductor count/current-carrying conductors, ambient/grouping/derating inputs, route length, termination limits, voltage-drop criterion, and PE/grounding/bonding requirements |
| Physical routes | 3D route points and geometry when available; otherwise a scaled 2D path, segment list, elevation changes, end/termination allowances, service loop allowance, and estimate confidence |
| Cabinet | Enclosure, backplate/rail/duct/terminal layout, component dimensions and mounting data, heat/power data when used, reserve policy, and source/provenance for imported CAx assets |

## Calculation package

The calculation package shall identify the governing project/code basis and
the responsible reviewer. It shall include the following records for every
applicable circuit and load:

| Calculation record | Required result and traceability |
|---|---|
| Connected-load schedule | Load tag, source/equipment reference, nameplate basis, quantity, connected load/current, and calculated contribution |
| Demand/load calculation | Demand/diversity and operating-case assumptions, total demand current/power, control-power demand, spare/reserve treatment, and upstream feed implications |
| Fault-current study | Defined calculation point, source available-fault-current data, upstream/downstream impedance/path data, method/version, resulting available fault current, device/assembly duty comparison, and reviewer decision |
| Conductor/wire-sizing calculation | Circuit ID, load/protective basis, ampacity inputs and adjustments, selected conductor/cable, voltage-drop input/result, fault/PE/grounding considerations as applicable, terminal compatibility, and reviewer decision |
| Protection coordination/selection record | Proposed/selected device, rating/setting/curve or manufacturer reference where applicable, protected conductor/load, short-circuit duty/SCCR evidence, open items, and qualified approval |
| Panel capacity/thermal input | Component/load heat and power inputs, reserve policy, source/evidence, and whether the result is a planning envelope or reviewed design calculation |

The workbench may collect values, calculate transparent intermediate results,
and preserve their provenance. It must not represent a missing source value,
generic equipment class, or planning envelope as a final fault-duty,
protective-device, SCCR, conductor, or thermal approval.

## Geometry and route hierarchy

Use the highest available evidence level for each wire/cable record:

| Evidence level | Acceptable source | Wire-schedule length status |
|---|---|---|
| A — Routed 3D | Ordered route geometry between verified endpoint/port locations | `routed-3d`; calculated route length plus documented end allowance |
| B — 3D layout + 2D system route | Verified cabinet endpoint geometry plus an issued scaled 2D system path | `hybrid-estimate`; 3D internal length plus 2D field-route segments and allowances |
| C — 2D route estimate | Issued scaled 2D route/segment schedule with elevations and allowances | `estimated-2d`; no claim of physical routing verification |
| D — Planning allowance | Controlled stated assumption only | `planning-only`; blocks construction/as-built issue |

At no level may a straight-line distance replace the documented route without
being labeled an estimate. Do not mark a route `routed-3d` when a model lacks
verified terminals/ports, physical routing path, or relevant clearance/bend/
segregation review.

## Phase-3 deliverables

| Deliverable | Minimum content | Status allowed at Phase 3 |
|---|---|---|
| Load-calculation report | Connected/demand loads, cases, assumptions, sources, calculations, reviewer decisions, unresolved items | Review; released only after qualified approval |
| Fault-current report | Point-by-point fault data, method/source, equipment duty comparison, assumptions, and decision record | Review; released only after qualified approval |
| Conductor and protection schedule | Circuit/load/protection/conductor/route/voltage-drop/fault-duty/SCCR fields with decisions | Review; released only after qualified approval |
| Wire schedule | Wire/cable tag, endpoints/terminals, conductor attributes, route evidence level, length, allowances, circuit function, PLC association, and revision/snapshot | `routed-3d`, `hybrid-estimate`, `estimated-2d`, or `planning-only` per record |
| 3D control-cabinet drawing/model | Enclosure, backplate, rails, ducts, terminals, PLC, power/control equipment, equipment identities, and internal-route representation | Reviewable geometry; not physical-fit or routing approval without checks |
| 3D system drawing/model | Field devices, equipment, panel locations, routed paths, elevations, and endpoint identities where geometry is available | Optional by availability; must be provenance/units reviewed |
| 2D system render and length-estimate package | Scaled routes, segment/elevation/allowance table, endpoint identities, and estimate status | Required fallback when 3D system geometry is unavailable |
| Reconciliation record | Cross-check of drawings, calculations, I/O, PLC allocation, terminals, cables, and wire schedule against one project revision/snapshot | Required |

## Wire schedule minimum columns

Every wire or cable row must contain the following, or an explicit `N/A`
reason where it does not apply:

| Identity and endpoints | Electrical and installation data | Route and calculation link | Control traceability |
|---|---|---|---|
| Wire/cable ID; from/to device and terminal; panel/field location | Conductor count, material, insulation/type, size, colour/core, voltage class, PE/screen treatment, terminal range | Evidence level; route source/revision; raw length; allowance; scheduled cut length; voltage-drop calculation reference; fault/protection/conductor decision reference | Circuit/load tag; PLC signal/module/channel/address where applicable; drawing and grid/zone; snapshot/revision |

## 3D control-cabinet requirements

The cabinet model/drawing shall use the same logical identities as the 2D
package. It must show, at minimum, the enclosure/backplate boundaries,
mounting rails, wire duct/guides, terminal strips, PLC/controller, power and
control-supply equipment, protective/switching hardware, and controlled-load
interfaces that reside in the cabinet. Each placed item must identify whether
its geometry is manufacturer-verified, family-reference/unverified, generic,
or placeholder.

Before a model is used to support final routing, verify component dimensions,
mounting constraints, terminal/port mapping, clearance, service access, duct
capacity, bend radius, segregation, and asset provenance. Until those checks
are recorded, the model supports route estimation and review only.

## Phase-3 acceptance criteria

Phase 3 is ready for its review gate when:

- every included load and circuit has a unique record, source/evidence status,
  and link to the relevant Phase-2 schematic and Phase-1 identifiers;
- incoming supply and available-fault-current data are present at every
  calculation boundary, or the affected fault/selection result is blocked and
  clearly marked;
- every conductor/protective-device result records its method, inputs,
  assumptions, reviewer disposition, and links to the wire schedule;
- every wire/cable row has endpoint identities, conductor data, a route
  evidence level, a length or explicitly blocked length, and revision/snapshot
  provenance;
- a 3D cabinet model/drawing exists with all placed components identified; and
- either an available 3D system model or the required 2D route/length-estimate
  fallback is supplied for each external route.

Final construction, procurement, and as-built approval additionally require
the applicable electrical, protection, safety, manufacturer, installation, and
site reviews. They are not conferred by this phase.

## Review record

| Review item | Evidence/reference | Reviewer | Date | Result / deviation |
|---|---|---|---|---|
| Load schedule and demand calculation | [Reference] | | | |
| Supply and fault-current input validation | [Reference] | | | |
| Fault-duty/SCCR decision review | [Reference] | | | |
| Conductor/protection sizing review | [Reference] | | | |
| Wire-schedule endpoint and length reconciliation | [Reference] | | | |
| 3D cabinet geometry/provenance review | [Reference] | | | |
| 3D system route review or 2D fallback review | [Reference] | | | |
| Drawing/PLC/calculation snapshot reconciliation | [Reference] | | | |
