# Site acceptance test protocol

## Draft status and permitted use

This is an original integraCAD Open draft template. It is not an approved test
procedure, engineering instruction, safety-validation report, or authorization
to energize equipment. Complete the project-specific methods, limits,
responsibilities, and approvals before use. No numerical acceptance limits are
supplied. The source package's existing assets remain blocked as recorded in
[ASSET_PROVENANCE.md](ASSET_PROVENANCE.md); adding this draft does not change
their provenance, rights, or engineering disposition.

## 1. Controlled project and site baseline

| Field | Project entry |
|---|---|
| Project identity and name | [Stable project identity and name] |
| Protocol number, revision, and date | [Document identity and revision] |
| Resolver snapshot / project revision | [Input baseline and checksum/reference] |
| Site, area, machine, panels, circuits | [Identities and physical boundaries] |
| Equipment and interfaces included | [Occurrence identities and counterpart owners] |
| Exclusions and operating restrictions | [Boundaries and unresolved dependencies] |
| As-installed drawing / I/O / software versions | [Revision/checksum and controlled locator] |
| Approved narrative and requirements | [Revision and requirement/function identities] |
| FAT results and remaining punch items | [References and SAT disposition] |

Record all sources of power, external supplies, stored-energy interfaces, and
affected neighboring equipment in the approved site procedure. A recorded
baseline identifies the equipment under test; it does not itself authorize a
test or establish that equipment is ready.

## 2. Authorized responsibilities and entry approval

| Responsibility | Named authorized person | Authority/procedure reference | Date / disposition |
|---|---|---|---|
| Site operations and test window | [Name] | [Reference] | [Entry] |
| Electrical isolation / energization | [Name] | [Reference] | [Entry] |
| Controls test execution | [Name] | [Reference] | [Entry] |
| Mechanical / process readiness | [Name] | [Reference] | [Entry] |
| Interface counterpart coordination | [Name per system] | [Reference] | [Entry] |
| Independent safety validation | [Name] | [Separate plan reference] | [Entry] |
| Client witness / acceptance authority | [Name] | [Reference] | [Entry] |

Before each test category starts, record its authorized method and acceptance
criteria, equipment condition, approved isolation or energization procedure,
applicable permit/operating restrictions, test equipment and calibration
references, personnel/witnesses, and hold points. Record the disposition of
unresolved FAT/site issues and the authority accepting any restricted scope.
An incomplete entry prevents that category from being described as ready.

## 3. Installed wiring and point verification

Use approved isolated inspection/continuity methods where specified by the
project procedure. Identify tests requiring another equipment condition rather
than treating all installed checks as safe under one condition. Record the
method and authorization for that condition explicitly.

| Test ID / requirement | Occurrence and path identities | Condition / approved method | Expected / limit reference | Observed and evidence | Result / deviation |
|---|---|---|---|---|---|
| [ID] | [Source, terminal, cable/core, wire, destination] | [Reference] | [Reference] | [Entry] | [Entry] |

Reconcile actual installed tags, endpoints, terminal/cable/core identities,
PLC rack/module/channel/native address, power domains and return references
against the controlled I/O list and drawings. Record unused/spare channels
separately. Include analog loop/scaling and instrument configuration checks
using approved stimulus, range, tolerance, and procedure references. Record
point-by-point evidence and any inaccessible or untested point explicitly.

Physical continuity or an I/O indication is not evidence that a process
sequence, interlock, fault response, or safety function operates correctly.

## 4. Authorized functional and interface tests

Execute only the test cases and conditions approved for the site, plant, and
counterpart equipment. Record whether actual process material/motion is allowed,
the required readiness conditions and personnel, and the agreed abort/hold
procedure. Reference approved methods instead of supplying generic live-test
instructions here.

| Case ID / narrative requirement | Preconditions and allowed conditions | Approved procedure and expected result | Actual result / evidence | Witness / date | Disposition |
|---|---|---|---|---|---|
| [ID] | [References] | [References] | [Entry] | [Entry] | [Entry] |

Create applicable cases from the approved narrative for:

- Normal start, operating modes, controlled stop, feedback and sequence timing.
- Permissives/interlocks and the specified response to missing or contradictory
  feedback, device fault, communication failure, and control-power loss/return.
- Reset, recovery and restart behavior after each relevant interruption, with
  explicitly approved expected behavior; do not assume automatic restart.
- Network addressing, ownership, signal mapping, handshakes and failure/recovery
  behavior at PLC/HMI, remote I/O, drive and other equipment interfaces.
- Field instrument ranges/scaling, output interfaces and actual-load behavior
  where the approved site scope permits testing them.

For every case, retain the function/load/I/O/circuit identities, software and
hardware versions, counterpart-system versions, observation record and evidence
locator. A simulated counterpart result must be labeled simulated and cannot
stand in for an unperformed installed-interface test.

## 5. Safety validation reference

Record the independent approved safety-validation plan, requirement/function
identities, responsible reviewer, applicable configuration revision, evidence
locator, result and open restrictions. This SAT template supplies no safety test
method, achieved PL/SIL/category claim, or substitute validation. Record an
unperformed or unapproved safety validation as an open hold point rather than
inferring acceptance from ordinary PLC, contact, I/O or functional checks.

## 6. Deviations, retest, and restoration

| Finding ID | Affected identities / test IDs | Observed discrepancy and impact | Owner / corrective action | Retest baseline / evidence | Closure authority / date |
|---|---|---|---|---|---|
| [ID] | [References] | [Entry] | [Entry] | [References] | [Entry] |

For each interruption, correction, bypass, temporary wiring, simulation, force,
parameter change, or software change, record the authorized action and affected
baseline. Identify dependent tests and documents that need re-verification.
Retest against the revised approved baseline and preserve earlier results.

Record restoration evidence for temporary conditions, approved normal settings,
forces/simulations/bypasses, alarms, communications, backups and equipment
operating state. The responsible site owner records the handback condition and
remaining restrictions; this template does not authorize a return to service.

## 7. As-built reconciliation and acceptance disposition

Confirm controlled as-built drawings, I/O and terminal/cable/wire schedules,
hardware occurrence identities/parents, software backups/checksums, approved
settings, manuals and training/handover references match the accepted baseline.
Record remaining pending items with owner, due date, restriction, and explicit
acceptance authority. Distinguish passed, failed, not performed, and not
applicable results; explain the applicability decision.

| Sign-off role | Name | Scope / baseline accepted | Open-item restrictions | Signature or controlled evidence / date |
|---|---|---|---|---|
| Test lead | [Name] | [Reference] | [Entry] | [Entry] |
| Site operations owner | [Name] | [Reference] | [Entry] | [Entry] |
| Responsible controls reviewer | [Name] | [Reference] | [Entry] | [Entry] |
| Client acceptance authority | [Name] | [Reference] | [Entry] | [Entry] |

Keep safety-validation disposition separately referenced. Completion of fields
or signatures in a draft does not establish a regulatory approval, safety
certification, or construction/release authority beyond the stated scope.
