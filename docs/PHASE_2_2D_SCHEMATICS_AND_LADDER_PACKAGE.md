# Phase 2 — 2D system schematics, PLC I/O, and ladder package

## Objective

Phase 2 produces the reviewable 2D electrical views needed to understand how
power and control signals move through the system. It incorporates system
drawings, electrical schematics, PLC I/O interface drawings, ladder diagrams,
power distribution from the incoming supply breaker, protective devices for
controlled loads, and low-voltage control schematics.

The phase uses the Phase-1 traceability convention. Every I/O point and
controlled load shown on a Phase-2 drawing must be traceable by its issued
identifier to the I/O list, terminal/cable/wire records, PLC allocation, and
the appropriate functional and test references.

This is a package-definition and acceptance requirement. It does not select
protective-device ratings, prove short-circuit/coordination performance,
establish a safety function, or approve a panel for construction. Those
decisions require applicable source data and qualified engineering review.

## Required 2D drawing set

| Sheet family | Minimum scope | Required information |
|---|---|---|
| `000` — cover, index, and drawing rules | Package navigation | Project and revision identity, sheet index, symbol legend, reference designations, sheet-zone and cross-reference syntax |
| `010` — incoming power and distribution | From incoming supply to distribution branches | Supply characteristics, main isolator/disconnect where applicable, incoming breaker, protective-device references, distribution points, PE/earth and neutral treatment, outgoing circuit references |
| `020` — controlled-load power circuits | One view per load group or feeder | Source breaker/fuse/protective device, switching/protection device, controlled load, motor/VFD/contactor/overload interfaces where applicable, cable and terminal references, ratings/source references and open decisions |
| `030` — low-voltage control power | Control-power creation and distribution | Control transformer or DC power supply, input/output protective devices, +24 V DC, 0 V/common, PE/functional earth, distribution terminals, fuse/MCB references, voltage-drop/segregation assumptions where required |
| `040` — ladder and control logic interface | Logic representation for every allocated I/O point | Rung or explicit interface reference, enabling conditions, coils/commands, PLC symbolic tags, cross-references to I/O and field drawings, functional-document references |
| `050` — PLC digital inputs | All allocated DI and discrete safety-interface inputs | Module/slot/channel, native address, signal tag, field device/pin, cable/core, terminals, commons, input power/return, cross-sheet references |
| `055` — PLC digital outputs | All allocated DO and discrete safety-interface outputs | Module/slot/channel, native address, command tag, relay/contactor/solenoid/load interface, protection/suppression where applicable, terminals/cable/core, output supply/return |
| `060` — analogue I/O | All allocated AI and AO points | Module/slot/channel, address, tag, signal type/range, terminals, cable/core, screen/earth treatment, loop power/isolator/barrier when applicable |
| `070` — safety interface | Safety-related interfaces only; not a safety-validation claim | Safety device/interface tags, dual-channel or monitored paths where required, safety-controller or relay points, reset/feedback references, independent safety-analysis references |
| terminal, cable, wire, and I/O schedules | Controlled schedule views | The same identifiers and endpoints that appear on the schematics and ladder views |

The repository’s existing `010`, `030`, `050`, `055`, `060`, and `070` files
are source assets for these families. They remain provenance-gated reference
assets until their source, redistribution rights, and reviewer disposition are
recorded. Phase 2 may create or adapt controlled project drawings only after
that gate is satisfied.

## Ladder-diagram coverage rule

“All I/O” means each active, allocated DI, DO, AI, AO, and applicable
safety-interface channel has exactly one of the following in the controlled
package:

1. a dedicated ladder rung or network; or
2. an unambiguous rung/network cross-reference to a reusable function block,
   with the I/O tag, PLC address, and function-block instance shown.

The ladder view must not invent program behavior. It is a reviewed
representation of the approved PLC logic or control narrative. Where a point
is intentionally unused, spare, bypassed, or not applicable, the I/O list and
the relevant drawing must state that status rather than omit the channel.

### Required content per I/O representation

| I/O class | Minimum schematic/ladder content |
|---|---|
| DI | Field contact/sensor state, PLC address and symbolic tag, input common/power context, signal conditioning if used, and the rung/function that consumes it |
| DO | PLC command/tag, rung/function that drives it, interposing relay/driver where used, output protective device, field load/terminal/cable path, and feedback reference if applicable |
| AI | Field source, loop/supply/isolator as applicable, range and units, PLC address/tag, terminal/cable/screen details, and the scaling/validation function reference |
| AO | PLC address/tag, scaling/command function reference, isolator/loop-power arrangement as applicable, range/units, terminal/cable/screen details, and field final element |
| Safety interface | Relevant device/channel path and independent safety-reference identifier; do not portray the drawing as a completed safety analysis or validation report |

## Power-distribution and protection requirements

The 2D power views shall let a reviewer follow each controlled load from the
declared supply through its protective and switching path to the load. At a
minimum show:

```text
incoming supply → main breaker / isolation → distribution bus or terminals
→ branch breaker or fuse → protective/switching device → controlled load
→ PE and return/neutral path as applicable
```

For each branch, show the equipment tags, conductor/cable references,
terminal references, voltage, and drawing cross-references. Show a device as
`engineering selection pending` when its rating, setting, SCCR/short-circuit
duty, coordination, conductor size, or manufacturer data has not been
reviewed. A schematic symbol or generic hardware class is not evidence of a
validated protective-device selection.

The low-voltage control sheet must separately show the source and distribution
of control power—including supply/transformer, primary and secondary/input and
output protection as applicable, +24 V DC, 0 V/common, PE/functional earth,
and terminals. Do not use the power drawing alone to imply that a low-voltage
control circuit is protected or isolated correctly.

## Cross-reference rules

- Use issued sheet identifiers and grid/zone locations at every off-sheet
  continuation; do not use a page number or temporary filename.
- Show the source and destination at both ends of a cross-sheet connection.
- Use the same device tag, cable/core, terminal, wire, PLC coordinate, and
  address in the system, power, I/O, ladder, and schedule views.
- Reference controlled-load circuits from the PLC output and its ladder rung;
  reference the controlling I/O and output tag from the load-power circuit.
- Every ladder I/O instruction, function-block connection, or output coil
  must resolve to an I/O-list record and PLC allocation (or an explicit
  spare/unused/not-applicable record).

## Phase-2 acceptance criteria

Phase 2 is ready for review only when all of the following are true:

- The sheet index contains every required drawing family or documents its
  project-specific `N/A` disposition.
- The incoming supply, main protection/isolating reference, distribution,
  each controlled-load branch, and low-voltage control power are shown on 2D
  schematic views with resolvable cross-references.
- Every active allocated I/O point appears once in the I/O list and is
  represented by a PLC interface view and a ladder rung/network or explicit
  function-block cross-reference.
- Each PLC output has a resolvable controlled-load or explicit unassigned/
  spare status, including the protection and switching interface reference.
- Cable/core, terminals, internal wires, PLC module/channel, native address,
  and symbolic tag reconcile across all views and schedules.
- Representative DI, DO, AI, and AO points can be traced in both directions
  using the Phase-1 method; a safety-interface example is checked when safety
  scope exists.
- All required ratings, settings, and safety decisions are either supported by
  evidence and approval or conspicuously marked as unresolved engineering
  decisions.
- The reviewer records drawing, PLC-configuration, and schedule reconciliation
  results against one issued project revision or resolver snapshot.

## Review record

The calculation, wire-schedule, and 3D delivery requirements that consume this
2D package are defined in
[Phase 3 — load calculations, wire schedule, and 3D deliverables](PHASE_3_LOAD_CALCULATIONS_AND_3D_DELIVERABLES.md).

| Review item | Evidence/reference | Reviewer | Date | Result / deviation |
|---|---|---|---|---|
| Sheet index and cross-reference navigation | [Reference] | | | |
| Incoming power and distribution trace | [Reference] | | | |
| Controlled-load protection/interface trace | [Reference] | | | |
| Low-voltage control supply trace | [Reference] | | | |
| All-I/O ladder coverage reconciliation | [Reference] | | | |
| PLC I/O/address-to-drawing reconciliation | [Reference] | | | |
| DI/DO/AI/AO bidirectional trace tests | [Reference] | | | |
| Safety-interface review, if applicable | [Reference or N/A] | | | |
