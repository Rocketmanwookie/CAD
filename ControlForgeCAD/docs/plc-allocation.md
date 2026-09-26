# PLC I/O allocation and occurrence model

## Purpose

The PLC allocation model turns a selected catalog CPU and typed I/O demand into
a deterministic project-owned representation. It is deliberately narrower than
a vendor programming project: it records **where an I/O point belongs** in the
controls design without generating PLC logic or vendor project files.

## Allocation contract

`controls_wb.io_allocation.allocate_io_signals()` is FreeCAD-independent. Given
the project’s selected make, line, CPU, and logical DI/DO/AI/AO signals, it:

1. places CPU I/O in rack `0`, slot `1`;
2. adds the smallest compatible catalog expansion module in increasing slots;
3. assigns zero-based channel numbers within each module;
4. leaves unsupported signal types unassigned and reports a warning; and
5. reports insufficient capacity or duplicate manual assignments as findings.

The allocator returns three immutable result collections:

| Collection | Meaning |
|---|---|
| `signals` | Logical I/O signals with rack, slot, channel, and mapping status. |
| `modules` | CPU and expansion-module placements, including catalog part and source IDs. |
| `findings` | Capacity, collision, and compatibility results. |

Only a result without `ERROR` findings may be persisted. The **Allocate PLC
I/O** command writes that complete mapping to `CE_Project.IOSignals`, so it
survives save/reopen and is the source of the I/O-list CSV projection.

## Persistent FreeCAD occurrences

`controls_wb.model.layout.materialize_plc_allocation()` projects a valid,
persisted allocation into typed FreeCAD objects:

```text
CE_Project
  └─ PLC rack (plc.rack)
      └─ PLC module (plc.module) × N
          └─ PLC channel (plc.channel) × N
```

The rack owns a `Modules` link list. Each module links to its `RackObject` and
owns a `Channels` list. Each channel links to its `ModuleObject` and records the
allocated signal tag, address, type, rack, slot, and channel number. Rack and
module occurrences are also registered on the project’s `ElectricalDevices`
list so their identities can serve as electrical-graph owners.

Occurrence identities are deterministic UUID5 values derived from the project
identity (or `ProjectId`) and stable allocation coordinates. Re-materializing
the same project reuses the existing objects rather than creating duplicates.
Catalog part definitions remain separate from those placed occurrences.

## Current boundary and next work

**Allocate PLC I/O** persists and materializes a valid allocation inside one
FreeCAD transaction. Each allocated channel creates or reuses a deterministic
typed electrical signal, links to that signal in both directions, and records
the electrical paths that consume it. **Add Electrical Path** requires an
allocated PLC channel; it derives the path signal and the first PLC terminal's
owner and designation from that channel. The editor preserves this allocation
derived terminal address, and validation reports broken reciprocal links,
unregistered signals, omitted consuming paths, and corrupted owner/address
relationships.

The next boundary is **safe allocation reconciliation**. A changed allocation
must identify channel-owned signals and paths that would be moved or removed,
then either migrate them explicitly or stop with an actionable finding. Manual
FreeCAD allocate/save/reopen/recompute/edit/save/reopen evidence also remains
required; automated tests do not substitute for that acceptance run.

This model is not a PLCopen XML exporter, ladder editor, or a substitute for a
vendor PLC IDE.
