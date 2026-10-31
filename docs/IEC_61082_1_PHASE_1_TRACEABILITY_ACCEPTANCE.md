# Phase 1 — IEC 61082-1 addressing traceability acceptance

## Completion statement

**Phase 1 is complete for the documentation-template baseline.** The project
now defines one complete example chain and a repeatable acceptance method for
following a PLC input from field device to controller address, functional use,
and test evidence.

This completion statement is deliberately limited to the template and
verification-method deliverable. It is not a declaration that an installed
control system, a generated drawing set, or a project delivery complies with
IEC 61082-1. That requires the applicable standard edition, a complete
project-specific package, and responsible-engineer review.

## Objective

Establish a controlled addressing chain that lets a qualified technician start
with any one identifier and recover the same signal path, without guessing:

```text
field device → cable/core → panel terminal → internal wire
→ PLC module/channel → controller address → functional use → test evidence
```

## Phase-1 reference example

The example is a 24 V DC PNP, normally-open proximity sensor used to detect a
product at a conveyor infeed. The identifiers are illustrative source-template
values. A live project must replace them with issued identifiers and keep all
related documents under the same controlled revision.

| Chain position | Controlled example value | Required document reference | Verification rule |
|---|---|---|---|
| Field device | `-B101` — infeed proximity sensor | PLC I/O / signal sheet `050`, grid `C3`; I/O list | Device tag is unique and describes the field function |
| Field connection | Pin 4 — switching output | Sheet `050`, grid `C3` | Pin assignment matches the selected sensor’s manufacturer data |
| Cable/core | `-W101` / BK — signal core | Sheet `050`; cable schedule | Cable ID and core appear once for this signal and agree at both ends |
| Panel terminal | `-X1:12` — signal terminal | Sheet `050`, grid `D3`; terminal plan | Terminal strip and terminal designation resolve to an issued terminal-plan row |
| Internal wire | `W-050-012` from `-X1:12` to DI channel 00 | Sheet `050`, grid `E3`; connection/wire schedule | Wire identity has the same two endpoints in the drawing and schedule |
| PLC module/channel | `=A1/-A1`, DI module, slot 3, channel 00 | Sheet `050`; I/O list | Slot/channel is allocated to only one active signal |
| Controller address | `%I0.0`; `DI_CONV01_INFEED_PE` | I/O list; Software Design Specification | Native address and symbolic tag agree with the deployed/project PLC configuration |
| Functional use | `CONV01_PRODUCT_PRESENT` permissive; HMI text `Infeed product detected` | FDS/SDS; HMI/alarm record if applicable | Functional references use the same signal/tag identity |
| FAT evidence | `FAT-IO-014` | FAT protocol and I/O list | Test invokes the field signal and verifies the expected PLC address/function response |
| SAT evidence | `SAT-IO-014` | SAT protocol and I/O list | Site test verifies the installed device, cable/terminal path, PLC input, and function |

The trace, in condensed form, is:

```text
-B101 pin 4
  → -W101/BK
  → -X1:12
  → W-050-012
  → =A1/-A1, DI slot 3/channel 00
  → %I0.0 / DI_CONV01_INFEED_PE
  → CONV01_PRODUCT_PRESENT
  → FAT-IO-014 and SAT-IO-014
```

Support conductors are recorded alongside the signal on the same sheet:
`-B101` pin 1 / `-W101` BN / `-X1:13` for +24 V DC, and `-B101` pin 3 /
`-W101` BU / `-X1:14` for 0 V DC. They must be included in the complete loop
or signal drawing even though the switching-output trace above is the
acceptance path.

## Acceptance method

Conduct the navigation check in both directions. Record the actual revision,
reviewer, date, and any discrepancies in the final table.

### Field-to-controller trace

1. Start at `-B101` on the I/O or field-loop drawing.
2. Confirm Pin 4, `-W101/BK`, and the destination `-X1:12`.
3. Open the terminal plan and confirm that `-X1:12` identifies the internal
   wire `W-050-012` and its PLC-side destination.
4. Confirm the DI module, slot 3, channel 00, `%I0.0`, and symbolic tag in
   the I/O list and PLC configuration/SDS.
5. Confirm the functional use and the linked FAT/SAT test identifiers.

### Controller-to-field trace

1. Start from `%I0.0` or `DI_CONV01_INFEED_PE` in the PLC configuration or
   I/O list.
2. Confirm the allocation `=A1/-A1`, DI slot 3, channel 00.
3. Locate `W-050-012`, then `-X1:12`, in the connection schedule and terminal
   plan.
4. Confirm `-W101/BK`, Pin 4, and the field device `-B101` in the cable
   schedule and signal drawing.
5. Confirm the device function and its recorded FAT/SAT evidence.

The check passes only if both routes resolve to the same identities with no
ambiguous cross-reference, duplicate allocation, blank required field, or
uncontrolled document revision.

## Required project evidence before release

| Evidence | Minimum content | Phase-1 baseline status |
|---|---|---|
| Addressing convention | Tags, terminals, cable/core, wire, PLC coordinate, address, and sheet-zone syntax | Defined in the IEC 61082-1 traceability design basis |
| Traceability example | Complete bidirectional sensor-to-PLC chain | Defined in this document and the traceability design basis |
| I/O-list rule | Required allocation, address, terminal, cable, functional, and test fields | Defined in the I/O-list guide |
| Controlled drawings/schedules | Issued project sheets, terminal plan, cable/wire schedules, and I/O list | Required for a project; not supplied by this template baseline |
| PLC configuration reconciliation | Native address and symbolic tag checked against the project PLC configuration | Required for a project; not yet evidenced by a template |
| FAT/SAT execution | Actual results, signatures, and deviation disposition | Required for a project; test IDs are example placeholders |

## Phase-1 deliverables

| Deliverable | Minimum Phase-1 content | Release status |
|---|---|---|
| Starting project documentation | Cover/index, project identity and revision, URS/FDS or equivalent project requirements, control narrative, reference-designation convention, traceability design basis, and change-control record | Controlled starter set; not an issued construction/as-built package |
| Preliminary BOM | Tagged/project-location-referenced equipment and material rows, quantity, description, manufacturer/part number status, source/evidence status, and explicit `TBD`/engineering-decision items | Review/planning only until selected items and engineering decisions are approved |
| I/O schedule | One row per known active, spare, or intentionally unused point; tag, description, type, PLC rack/slot/channel/address when allocated, panel/terminal, cable/core, field device, function, drawing/test references, and unresolved fields | Controlled starter schedule; PLC allocation and installed configuration require later reconciliation |
| IEC 61082-1 traceability basis | [Addressing and signal-traceability design basis](../ControlForgeCAD/templates/controls-document-package/IEC-61082-1-Addressing-and-Traceability.md) | Template baseline complete |
| Bidirectional traceability example | This acceptance record, including the field-device-to-test-evidence chain and navigation method | Template baseline complete |

The supplied [BOM template](../ControlForgeCAD/templates/controls-document-package/BOM.csv),
[I/O list](../ControlForgeCAD/templates/controls-document-package/IO-List.csv),
[I/O-list guide](../ControlForgeCAD/templates/controls-document-package/IO-List-README.md),
and project-document templates in the
[controls document package](../ControlForgeCAD/templates/controls-document-package/README.md)
form the Phase-1 starter sources. Their existing provenance and engineering
review restrictions remain applicable.

Phase 2 consumes these controlled starter records to create the 2D drawing
package; see [Phase 2 — 2D system schematics, PLC I/O, and ladder package](PHASE_2_2D_SCHEMATICS_AND_LADDER_PACKAGE.md).

## Execution record for a live project

| Project/revision | Signal tag | Field-to-controller result | Controller-to-field result | FAT evidence | SAT evidence | Reviewer | Date | Deviation reference |
|---|---|---|---|---|---|---|---|---|
| [Project / revision] | [Tag] | [Pass / Fail] | [Pass / Fail] | [Reference] | [Reference] | | | |
