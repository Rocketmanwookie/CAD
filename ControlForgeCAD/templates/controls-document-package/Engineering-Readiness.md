# Engineering readiness and instance handoff

This is an original integraCAD Open requirements supplement authored for the
current template review. It is a draft design aid, not approved engineering
instructions, a standards interpretation, or a statement that generators exist.
The supplied package remains blocked under [ASSET_PROVENANCE.md](ASSET_PROVENANCE.md).
This addition grants no rights or approval to its supplied reference assets.

## Shared evidence record

For every fact used by a proposal or drawing, record the stable fact/subject
identity, value and units, source locator and revision, received date, verifier,
verification method and evidence, disposition, and unresolved conflicts. Record
an approval separately from verification, including approver, date, decision
scope, and applicable input revision. Missing evidence remains unknown.

Each generated or proposed occurrence needs a stable CE identity, role, exactly
one declared owning parent in the established project structure, and separate
references to upstream subjects and sources. Reuse an existing physical
occurrence when several views show the same equipment. A drawing or rung is a
representation with references to equipment; it is not a second physical device.
Record circuit upstream/source topology explicitly for multiple infeeds and
power domains; circuit membership references equipment and does not replace
its one physical owning parent.
Confirm exact parent roles against the project model before implementation;
this supplement does not invent a competing hierarchy.

## Prerequisites and outputs

| Target | Required reviewed input | Permitted intermediate result | Remaining decision before issue |
|---|---|---|---|
| Infeed and feeder circuit | Source endpoint, voltage basis, phases/conductors, neutral/PE, frequency, isolation boundaries, source evidence | Draft circuit topology and single-line overview | Ratings/settings, conductor sizing, fault duty, coordination, applicable requirements |
| PLC configuration | Actual typed I/O, electrical characteristics, special functions, platform/firmware compatibility, network and reserve policy | Compatible CPU/rack/module/channel proposal with actual versus spare allocation | Selected hardware and interface review; count feasibility alone is insufficient |
| Control power supply | All consumers assigned to power domains, continuous and pickup/inrush demand, source voltage, environment, simultaneity and reserve policy | Traceable PSU budget and catalog candidate | Derating, startup capacity, interfaces, distribution/protection and operating requirements |
| Switching and protection | Per-load nameplate/duty, control/drive arrangement, source topology/fault data, coil/control demand, manufacturer evidence | Contactor/drive/overload/protection classes and candidate references | Applicable ratings, utilization, settings, coordination and compatibility decisions |
| Full distribution drawing | Reviewed infeed, all load branches, control-power source, protective/switching paths and endpoints | Coordinated single-line and/or three-line representation | Phase/neutral/PE detail, cross-sheet continuity and engineering issue review |
| Low-voltage ladder schematic | Verified I/O electrical interfaces, power/return paths, contacts/coils, protection, terminals, functional narrative and interlocks | Draft wired control rungs referencing real occurrences | Loss-of-power/fault response, interlock/reset/restart behavior and circuit review |
| PLC logic representation | Approved functional behavior, signal mapping, permissives, sequences, feedback and program/function references | Rung/network documentation or explicit unresolved function reference | Program implementation/testing and independent safety decisions where applicable |

A three-phase system may need both a single-line overview and phase-resolved
three-line details. Phase count does not automatically choose the entire drawing
set. Capture the requested views and the detail required by the project reviewer.
I/O alone does not determine rungs, and PLC plus I/O counts alone do not size a PSU.

## Dependency and change review

Every candidate, instance, circuit, sheet, and rung records its input identities,
input revisions/snapshot, rule version, disposition, and open decisions. Changed
upstream facts mark dependent outputs stale/pending review. Rejected, superseded,
or conflicting facts cannot support a released designation. Recompute proposals
without silently replacing approved parts, manual edits, stable occurrence IDs,
or established parent links. Record the comparison and re-approval explicitly.

Record a separate technical readiness status and template/asset provenance
status. A fully verified circuit does not approve a blocked reference template;
an authorized template does not approve the circuit using it.

## Acceptance evidence to request

Confirm that infeed-to-load paths and supply/return paths are continuous; each
active I/O resolves to its PLC channel, electrical interface, field endpoint,
and functional reference; actual and spare channels remain distinct; and BOM,
I/O, circuit, drawing, and rung views refer to the same physical identities.
Check save/reopen persistence, duplicate-generation prevention, and invalidation
after a changed infeed, module, load, or I/O characteristic.

For testing, capture approved project-specific methods, limits, applicability,
isolation/energization authorization, responsible persons, equipment/calibration
references, result evidence, and deviations. Fixed voltages, resistances, ripple
limits, or simulation methods printed in supplied FAT/commissioning sources are
unverified source content until reviewed for the actual equipment and project;
do not automatically promote them into a test procedure.

Safety functions require their supplied requirements, reviewed architecture,
independent validation plan and responsible reviewer. Ordinary PLC logic,
contact type, template completion, or this agent review does not establish
achieved safety performance.

An original draft [Site Acceptance Test protocol](SAT-Protocol.md) now exists.
Its controlled baseline, responsibilities, installed-wiring versus functional
checks, authorized procedure references, interfaces, failure/recovery cases,
evidence, deviations, restoration and sign-off fields require project-specific
completion and review. A reviewed/released SAT remains pending; the supplied
package provenance block is unchanged. The existing factory simulation protocol
cannot substitute for installed site and process evidence.
