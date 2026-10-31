# IEC 61082-1 Addressing and signal-traceability design basis

## [Project name]

| | |
|---|---|
| **Document title** | IEC 61082-1 addressing and signal-traceability design basis |
| **Document number** | [Doc no.] |
| **Revision** | 0 |
| **Date** | [Date] |
| **Project** | [Project name] |
| **Client** | [Client] |
| **Prepared by** | [Author], [Your company] |

### Revision history

| Rev | Date | Description | Author | Approved |
|---|---|---|---|---|
| 0 | [Date] | First issue | [Author] | |

### Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Author | [Author] | | |
| Reviewer (electrical engineering) | | | |
| Approver ([Your company]) | | | |
| Approver ([Client]) | | | |

---

## 1. Purpose and delivery objective

The PLC control drawing and documentation package shall present electrical
engineering information so a qualified technician can identify, locate, and
trace each control signal from its field device to its PLC point and related
documentation without relying on unstated knowledge.

This template establishes project addressing and cross-reference rules that
support that objective. It is a design and verification aid aligned to the
documentation-presentation intent of IEC 61082-1; it is **not** a certificate
that a completed package complies with IEC 61082-1. The current, applicable
edition of the standard and the project requirements shall be reviewed by the
responsible engineer.

## 2. Required traceability chain

Each implemented PLC signal shall have one stable, unambiguous value for every
applicable item below. A drawing or schedule may repeat a value, but shall not
silently redefine it.

| Traceability item | Required identifier or information | Primary controlled location |
|---|---|---|
| Function | Process duty and signal description | Control narrative / FDS |
| Field device | Device tag and location | Loop or I/O drawing; I/O list |
| Field connection | Device terminal/pin and cable core | Loop drawing; cable schedule |
| Panel entry | Panel, terminal strip, terminal number and level/side where applicable | PLC drawing; terminal plan |
| Internal connection | Wire number and destination terminal/channel | PLC drawing; connection schedule |
| PLC hardware | Cabinet/panel, rack, module/slot, channel and terminal | PLC I/O drawing; I/O list |
| Controller address | Vendor-native PLC address and symbolic variable/tag | I/O list; software design specification |
| Functional use | Program block, interlock, alarm, HMI indication or command reference | FDS/SDS, cause and effect, alarm list |
| Verification | FAT and SAT evidence reference and status | I/O list; FAT/SAT records |

If an item does not apply, state `N/A` and give the reason. Do not leave it
blank in a released/as-built package.

## 3. Addressing and reference conventions

### 3.1 Reference designations

Use the project reference-designation convention consistently for equipment,
devices, terminals, cables, and PLC hardware. The exact syntax is project
defined; the following values are mandatory at minimum:

- a unique field-device tag;
- a unique PLC point identity: controller/rack, slot or module, channel, and
  vendor-native address;
- a unique panel terminal reference in the form `[terminal strip]:[terminal]`
  (and level/side where the terminal construction requires it);
- a unique cable identifier and core designation; and
- a unique drawing sheet identifier and grid/zone reference for cross-sheet
  continuation.

Do not use a PLC address alone as the device identity: hardware can be
reconfigured. Preserve the device tag and update its allocation under formal
change control.

### 3.2 Cross-references

Every signal shown leaving a drawing sheet shall identify its destination by
sheet number and grid/zone, and every continuation shall point back to its
source. Cross-references must use the issued drawing identifiers, not a
temporary filename or a page number that can change during publishing.

For a PLC signal, the PLC I/O drawing shall show the field-device tag, cable,
terminal reference, module/channel, and address or a clear reference to the
controlled I/O list that contains those values. The I/O list shall link back to
the loop or PLC drawing by drawing number and, where used, grid/zone.

### 3.3 Changes, spares, and as-built status

Allocate spares explicitly. A spare point must identify its hardware channel,
address, status, and intended signal type; unlabelled gaps are not spares.
When a change affects a tag, terminal, wire, cable, PLC channel, address, or
cross-reference, update every affected document in the same controlled
revision. The as-built issue shall be reconciled against the installed panel,
field termination, and deployed PLC configuration.

## 4. Minimum PLC drawing package

The completed package shall include the following, as applicable to the
project. Sheets may be combined only when readability and traceability remain
clear.

| Document or sheet | Minimum information |
|---|---|
| Cover sheet, index and legend | Project identity, document index, revisions, symbol and reference conventions |
| Power/control supply | Supply source, protective devices, 0 V/common, PE, distribution terminals, sheet continuations |
| PLC hardware and I/O | PLC/rack/module identification, channel allocation, terminal/pin data, addresses, commons, field terminations, spare points |
| Field loop or signal sheets | Field device/pin, signal type, cable/core, shield/earth treatment, terminal strip, PLC channel, cross-sheet references |
| Terminal plan | Terminal strip, terminal number, levels/sides, wire/cable destinations, jumpers and accessories where used |
| Cable and connection schedules | Cable ends, cores, routes/location if required, screen/earth treatment, connection/wire identifiers |
| I/O list | Controlled signal allocation and functional, hardware, address, terminal, cable, and test references |
| Functional documents | Control narrative/FDS, cause and effect, alarm list, SDS and test records linked to the relevant tag or variable |

## 5. Worked example — proximity sensor to PLC digital input

This example illustrates the minimum information needed to trace a single
24 V DC, PNP, normally-open proximity sensor. Names and addresses are
illustrative only and must be replaced with the project-approved convention.

| Trace point | Example value | Where the technician finds it |
|---|---|---|
| Function | Conveyor infeed product detected | FDS `CONV-01`, input description |
| Field device | `-B101` — Infeed proximity sensor | Sheet `050`, grid `C3`; I/O list |
| Device pin | Pin 1 = +24 V, Pin 3 = 0 V, Pin 4 = switching output | Sheet `050`, grid `C3` |
| Cable/core | `-W101`, core BK (signal); BN (+24 V); BU (0 V) | Sheet `050`; cable schedule |
| Panel terminal | `-X1:12` (signal), `-X1:13` (+24 V), `-X1:14` (0 V) | Sheet `050`, grid `D3`; terminal plan |
| Internal wiring | `W-050-012` from `-X1:12` to input module channel 00 | Sheet `050`, grid `E3` |
| PLC point | `=A1/-A1`, DI module slot 3, channel 00 | Sheet `050`; I/O list |
| Controller address | `%I0.0`; symbolic tag `DI_CONV01_INFEED_PE` | I/O list; SDS |
| Functional use | Permissive `CONV01_PRODUCT_PRESENT`; HMI indication `Infeed product detected` | FDS/SDS; HMI/alarm records as applicable |
| Acceptance evidence | FAT test `FAT-IO-014`; SAT test `[SAT-IO-014]` | I/O list; FAT/SAT records |

The signal sheet must visually connect or unambiguously cross-reference this
path: `-B101 pin 4 → -W101/BK → -X1:12 → W-050-012 → DI slot 3/channel 00 →
%I0.0`. A technician should be able to start at any one of those identifiers
and recover the whole chain from the controlled package.

## 6. Release verification checklist

Before issue for construction, FAT, SAT, or as-built handover, the responsible
reviewer shall confirm:

- every used PLC channel is represented once in the I/O list and on the
  applicable drawing;
- every field I/O tag traces to a cable/core, terminal, PLC point, address,
  and functional reference, or is documented as intentionally not applicable;
- equipment, terminal, cable, wire, channel, and software identifiers agree
  across drawings, schedules, and PLC configuration exports;
- sheet cross-references resolve to an issued sheet and grid/zone;
- all spares, unused channels, and disconnected/obsolete signals are
  explicitly marked;
- no duplicate tag, terminal, cable/core, PLC address, or channel allocation
  exists unless an approved architecture expressly permits it;
- the I/O list, drawings, terminal plan, cable schedule, logic documentation,
  and test records share the same project revision or record the controlled
  deviation; and
- an independent reviewer has recorded discrepancies and their disposition.

## 7. Evidence record

Use the bidirectional navigation method in
[`docs/IEC_61082_1_PHASE_1_TRACEABILITY_ACCEPTANCE.md`](../../../docs/IEC_61082_1_PHASE_1_TRACEABILITY_ACCEPTANCE.md)
to record the Phase-1 template baseline and to execute the project-specific
field-to-controller and controller-to-field trace checks.

| Check | Evidence location | Reviewer | Date | Result / deviation reference |
|---|---|---|---|---|
| Drawing-to-I/O-list reconciliation | [Reference] | | | |
| I/O-list-to-PLC-configuration reconciliation | [Reference] | | | |
| Terminal/cable/wire reconciliation | [Reference] | | | |
| Cross-reference navigation check | [Reference] | | | |
| FAT traceability check | [Reference] | | | |
| SAT/as-built traceability check | [Reference] | | | |
