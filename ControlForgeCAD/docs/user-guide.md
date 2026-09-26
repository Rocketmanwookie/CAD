# ControlForgeCAD User Guide — PLC allocation to typed electrical path

This practical guide walks through the currently verified controls-design
workflow: select a catalog PLC, allocate I/O, author a path from an allocated
channel, validate it, and export review artifacts. It is pre-alpha software;
use it to organize and validate engineering data, not to certify a panel,
electrical design, safety function, or PLC program.

## Before you start

Install or link the workbench as described in the
[workbench README](../README.md). Start FreeCAD, choose **Controls /
Automation**, and create a new document.

The guide uses a Siemens S7-1200 starter catalog selection because that is the
source-backed catalog currently supplied. Other engineering choices remain
project-specific.

## 1. Create the project and select I/O

1. Run **New Controls Project**.
2. In the Project Intake dialog, select a PLC make, line, and CPU. For a quick
   path test, choose a Siemens S7-1200 CPU with at least one digital input.
3. Set `DI Count` to at least `1`, complete any required starter fields, and
   submit the form. A `CE_Project` appears in the model tree.
4. Run **Create Control Panel** to create the starter terminal-strip occurrence
   used by this workflow.

The created panel objects are metadata-rich placeholders, not final
manufacturer-accurate panel geometry.

## 2. Allocate PLC I/O

1. Select the `CE_Project` object and run **Allocate PLC I/O**.
2. Resolve any capacity or catalog warnings before continuing.
3. In the model tree, inspect the materialized PLC allocation occurrences:
   rack, module, and channel objects are created from the valid allocation.

Each allocated channel has a deterministic identity, an allocated signal tag
and address, and a typed electrical-signal link. Re-running a valid unchanged
allocation is intended to reuse those occurrences rather than duplicate them.
Same-type allocation moves preserve linked path identities and update the PLC
endpoint to the new channel/address; removing a path-dependent I/O point or
changing its signal type is rejected for explicit engineering resolution.

## 3. Create a typed electrical path

1. Run **Add Electrical Path**.
2. Select an **Allocated PLC channel**. The signal tag must match that channel;
   the PLC terminal owner and designation are derived from its allocated
   address.
3. Select the terminal strip created in step 1 and select an existing field
   device or enter a new field-device tag.
4. Complete conductor data, terminal designations, wire tags, and either a
   positive specified length or an ordered 3D route for each wire.
5. Submit the dialog.

The path contains a typed PLC-channel terminal, cabinet terminal pair, field
device terminal, and ordered wire segments. The consuming path reuses the
allocated channel's signal and is linked back to that channel.

The command rejects a generic PLC controller in place of an allocated channel,
a mismatched signal tag, or a mismatched PLC terminal designation.

## 4. Validate, edit, and export

1. Run **Validate Controls Project**. Resolve reported allocation, typed-link,
   owner, continuity, or input-data errors before treating schedules as review
   artifacts.
2. Select a typed path and run **Edit Electrical Path** to revise supported
   wire and route information. For an allocation-backed path, its first PLC
   terminal must remain the allocated channel address.
3. Run **Export Electrical Schedules**, **Export Terminal Plan**, and **Export
   I/O List** as needed. The defaults are shown in the workbench README.

Exports are deterministic projections of the current project graph. They are
not vendor PLC project files, schematics, or proof of code compliance.
Electrical schedule rows include the allocated PLC channel identity and
rack/slot/channel/address trace fields, and export stops if that allocation
trace cannot be reconciled with the path.

## 5. Manual desktop acceptance (not yet recorded)

The current automated suite exercises allocation, path linkage, endpoint
authoring, edit protection, and validation without a live FreeCAD desktop. A
manual FreeCAD acceptance record for this exact workflow has not yet been
recorded.

When performing that acceptance run, use the following evidence checklist:

1. Record FreeCAD version, operating system, Git commit, and installation path.
2. Allocate I/O, create a path from an allocated channel, save the `.FCStd`,
   close/reopen it, recompute, and verify the same rack/module/channel,
   signal, path, and terminal links remain visible.
3. Edit a wire route, confirm the allocated PLC terminal cannot be changed,
   save/reopen again, validate, and re-export schedules.
4. Record screenshots, Report View output, exported CSVs, and any traceback or
   unexpected finding. See the detailed
   [manual GUI acceptance checklist](manual-freecad-gui-test-plan.md).

Do not use a successful automated test run as evidence that the GUI behavior,
save/reopen behavior, or a particular FreeCAD build has been manually accepted.

## Where to go next

- [PLC allocation contract](plc-allocation.md)
- [Roadmap](roadmap.md)
- [Architecture](../../docs/ARCHITECTURE.md)
- [User Guide work-plan and owners](../../docs/USER_GUIDE_WORKPLAN.md)
