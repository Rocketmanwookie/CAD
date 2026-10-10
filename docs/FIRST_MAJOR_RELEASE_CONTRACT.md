# First Major Release Contract — Resolved Controls Project

## Outcome

Release 1 turns a structured controls intake into a reviewable, exportable
engineering project.  Given selected PLC hardware, labeled I/O, and described
loads, the workbench must determine the required *classes* of panel hardware,
preserve the evidence behind each proposed item, calculate a panel-capacity
envelope, and produce consistent handover artifacts.

It is deliberately an engineering-data release, not a final panel-design or
3D-CAD release.  Cabinet geometry, exact placement, routing, clearances,
manufacturing drawings, and imported vendor CAx are Release 2 work.

## Release-1 flow

```text
Plant/load intake + selected PLC + labeled I/O
                    |
                    v
          typed I/O and load resolver
                    |
                    v
   proposed hardware / protection / control classes
                    |
                    v
       panel-capacity and unresolved-data report
                    |
                    v
BOM + I/O schedules + YAML + CEProject XML + CAx acquisition manifest + cost inputs
```

Every arrow is traceable: output rows must retain the input identities, source
records, ruleset version, and unresolved assumptions that created them.

## Required release-1 domains

| Domain | Release-1 behavior | Explicit non-claim |
| --- | --- | --- |
| I/O resolver | Links each named I/O to a signal type, controlled load or field device, requested behavior, and PLC allocation. | A PLC allocation is not a complete electrical design. |
| Load intake | Supports motors, conveyors, hydraulic equipment, robots, and generic loads with operating description, quantity, voltage, power/current where known, duty, environment, and control/safety context. | Missing nameplate, load, or environmental data is not guessed. |
| Hardware resolver | Produces proposed classes such as circuit breaker/fuse, disconnect, contactor, overload/protection, VFD, relay, terminal block, power supply, and terminal-strip requirements. Each row names the rule and source used. | A proposal is not a released part selection, protective-device setting, safety determination, or purchase approval. |
| Panel-capacity resolver | Calculates a documented envelope from selected/proposed equipment: device counts, rail/terminal positions, heat/power inputs when provided, and reserve policy. | It does not claim a final enclosure size, physical fit, thermal compliance, or clearance. |
| Export contract | Emits BOM, I/O schedules, a human-readable YAML project document, CEProject XML, a CAx acquisition manifest, and cost-estimate inputs from the same resolved project model. | Exporting does not certify those artifacts. |
| CAx acquisition | Emits exact manufacturer, part number, requested format, official source locator, and checksum slots for needed CAD files. | Download/import and geometry placement are Release 2. |

## Resolver data contract

The following records are additive to the existing typed PLC allocation and
electrical-path records.  They must use stable CE identities and not depend on
display labels as keys.

| Record | Minimum fields | Produces |
| --- | --- | --- |
| `LoadRequirement` | identity, tag, load class, quantity, operating description, control mode, supply data, power/current data when known, duty/environment, source/evidence | one or more I/O and hardware requirements |
| `IORequirement` | identity, signal identity, direction/type, load identity, behavior, fail state, field-device/terminal need, evidence | PLC-allocation check and hardware requirements |
| `HardwareRequirement` | identity, requirement class, quantity, upstream load/I/O identities, rationale/rule version, unresolved fields | BOM candidate, panel-capacity input, CAx request, cost input |
| `EngineeringDecision` | identity, subject identity, decision type, status, evidence locator, qualified reviewer | approved or blocked disposition; never an implicit default |
| `PanelCapacityEnvelope` | identity, project identity, counts, assumed reserve policy, unresolved inputs, calculation version | enclosure/rail/terminal planning input |
| `CAxAcquisitionRequest` | manufacturer, part number, format, official source locator, local path/checksum when acquired, disposition | controlled library-import queue for Release 2 |

## Deterministic resolver rules

Rules may resolve a requirement only when their required data exists.  A rule
returns one of these dispositions:

- `resolved_candidate` — a traceable, reviewable hardware class or catalog
  candidate; it is not approval.
- `needs_engineering_decision` — a qualified reviewer must select/approve a
  value before the result can be treated as released.
- `blocked_missing_input` — the specific missing facts are exported and shown
  to the user; no default is invented.
- `not_applicable` — the rule's preconditions do not apply.

Circuit protection, motor overloads, short-circuit ratings, conductor sizing,
safety functions, and VFD selection must use source-backed rules and the
applicable qualified engineering review.  The application may organize their
inputs and evidence, but it must not represent an unsourced inference as a
design decision.

## Export set and consistency requirement

All Release-1 outputs originate from one immutable resolver snapshot ID:

1. BOM CSV and structured BOM JSON/YAML.
2. I/O schedule CSV plus terminal/path references where available.
3. Human-readable YAML project document.
4. CEProject XML for software/tool handover.
5. CAx acquisition manifest for the company library queue.
6. Cost-estimate input CSV/YAML: quantities, part numbers when resolved,
   requirement class, and unresolved status.
7. Missing-data and engineering-decision reports.

An export must fail clearly if its snapshot has unresolved identity links or an
ambiguous hardware candidate.  It may export a marked **review** artifact with
known missing engineering decisions; it must never label that artifact
released.

## Delivery sequence

1. Define and validate `LoadRequirement` and `IORequirement` records; add
   intake/editing surfaces and missing-data reporting.
2. Introduce source-versioned hardware requirement rules and their decision
   states; begin with transparent generic classes, not silent vendor choices.
3. Calculate the panel-capacity envelope and reserve policy from resolved
   requirements.
4. Build snapshot-based exporters and cross-format consistency tests.
5. Generate CAx acquisition manifests for all resolved manufacturer parts.
6. Perform independent QA and controls-engineering reviews, then a manual
   FreeCAD/export acceptance run under the active milestone cadence.

## Release-1 acceptance

Release 1 is ready for its release gate only when a representative project can
be taken from intake to the full export set; each proposed hardware row has a
traceable rule and evidence status; unresolved engineering decisions are
visible; all exported formats agree on identities and quantities; current
automated evidence passes; and the required independent reviews/manual
acceptance evidence are recorded in the operations ledger and release checklist.

## Release 2 — deferred CAD realization

Release 2 consumes the Release-1 CAx acquisition queue and resolver snapshot
to import checksum-recorded vendor files, place cabinet/backplate/rails and
equipment in 2D/3D, validate clearance/mounting/routing constraints, and
generate physical wiring geometry.  It must not treat Release-1 envelopes or
generic starter geometry as verified manufacturer CAD.
