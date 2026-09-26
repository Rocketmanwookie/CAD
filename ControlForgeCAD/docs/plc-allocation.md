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

## Catalog recommendation and reviewed labels

Project Intake can rank catalog CPUs against 120-percent spare DI/DO/AI/AO
demand and their documented signal-module limit. Selecting **Use
catalog-feasible CPU** is explicit: it opens an allocation review that displays
each CPU/module part, rack, slot, channel, and PLC terminal. Those allocation
keys are read-only; the user may approve readable engineering labels for the
I/O points. The accepted rows persist their catalog module name/part number and
canonical coordinates. This is catalog feasibility only, not electrical,
safety, compliance, lifecycle, or vendor-PLC-project approval.

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

Safe allocation reconciliation is implemented: supported same-type moves
migrate their linked signal, terminal, and paths atomically; incompatible
changes or removals with dependent design data stop with actionable findings.
The remaining acceptance boundary is a **manual FreeCAD
allocate/save/reopen/recompute/edit/save/reopen** run. Automated tests do not
substitute for that desktop evidence.

This model is not a PLCopen XML exporter, ladder editor, or a substitute for a
vendor PLC IDE.
