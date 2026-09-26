# integraCAD Open / ControlForgeCAD

**The open-source FreeCAD workbench that unites PLC controls with CAD.**

integraCAD Open is the integration-first controls-engineering project; ControlForgeCAD is its current FreeCAD workbench. Its primary job is not to replace CADbase, BOM workbenches, BIM tools, PLC IDEs, HMI platforms, or digital-twin simulators. Its job is to collect controls-engineering requirements once, validate missing or contradictory information, maintain traceability, and feed existing tools from one structured source of truth.

> Naming note: `ControlForgeCAD/` is the current workbench/module path. Older documents may use the former IntegraCAB working name; new project-facing material uses integraCAD Open.

## Project status

| Field | Value |
|---|---|
| Status | Pre-alpha / architecture seed |
| Version | 0.1.0-dev |
| FreeCAD target | FreeCAD 1.x |
| Language | Python |
| Workbench type | External Python workbench |
| FreeCAD menu label | Controls / Automation |
| License | MIT for original project code and docs |
| XML schema version | CEProject 0.1.0 |

## Current prototype commands

| Command ID | Menu text | Current behavior |
|---|---|---|
| `CE_NewProject` | New Controls Project | Opens a project intake dialog for core project/customer/site/deliverable fields, combined phase/voltage selection, starter controlled-load lines for current estimating, enclosure rating checkboxes, XML-backed PLC make/line/CPU selection, typed DI/DO/AI/AO counts, compatible Ethernet/power dropdowns, communication protocol checkboxes, optional I/O accessories, setup source metadata, a remembered CEProject XML import selector, YAML/UML-derived setup import, and a link to the project setup hardware catalog guide. It creates or updates an editable `CE_Project` object and shows an I/O expansion planning popup. If Qt/PySide is unavailable, it creates the starter object and prints a warning. |
| `CE_AddIOSignal` | Add I/O Signal | Opens an I/O signal dialog with selectable digital input, digital output, analog input, analog output, and relay types; user labels are stored as explicit signal rows with auto-generated tags and addresses. |
| `CE_AllocatePLCIO` | Allocate PLC I/O | Validates the selected catalog CPU and expansion capacity, deterministically assigns rack/slot/channel values, and persists a complete mapping for I/O export and save/reopen. |
| `CE_AddConnection` | Add Connection Record | Stores a traceable signal-to-terminal-to-wire record with field-device and PLC endpoint references. |
| `CE_AddElectricalPath` | Add Electrical Path | Creates and registers a typed PLC-channel-to-cabinet-terminal-to-field-device path with immutable identities, three ordered wire segments, conductor metadata, standardized color resolution, and specified millimetre lengths. |
| `CE_EditElectricalPath` | Edit Electrical Path | Edits the selected path's signal tag, terminal designations, wire metadata, specified lengths, and 3D routes while preserving every graph identity. |
| `CE_CaptureWireRoute` | Capture Wire Route from Geometry | Captures the ordered vertices from selected geometry onto one typed wire, preserves its identities, and recalculates the canonical route length. |
| `CE_CreatePanel` | Create Control Panel | Creates starter placeholder layout objects for a panel/backplate, DIN rail, wire duct, terminal strip, and PLC rack/module. |
| `CE_ExportBOM` | Export BOM | Exports controls metadata rows from the active FreeCAD document to CSV. |
| `CE_ValidateProject` | Validate Controls Project | Reports duplicate tags, missing controls metadata, starter intake missing-data findings, and verified/approved intake facts without source records. |
| `CE_PreviewMissingData` | Preview Missing Data | Prints the missing-data matrix for the active controls project intake object to the FreeCAD console. |
| `CE_ExportCEProjectXML` | Export CEProject XML | Exports the first controls project intake object in the active document to `~/integracab_ceproject.xml`. |
| `CE_ExportIOList` | Export I/O List | Exports a deterministic starter I/O list CSV to `~/integracab_io_list.csv` from explicit user-labeled signals plus the current project DI/DO/AI/AO counts. |
| `CE_ExportMissingDataCSV` | Export Missing Data CSV | Exports the active controls project missing-data matrix to `~/integracab_missing_data.csv`. |
| `CE_ExportConnectionSchedule` | Export Connection Schedule | Exports persisted connection records, including typed path/device/terminal/wire identities when available, to `~/integracad_connection_schedule.csv`. |
| `CE_ExportElectricalSchedules` | Export Electrical Schedules | Exports canonical typed-graph wiring and I/O path schedules with identities, endpoints, terminal chain, conductor metadata, and calculated length. |
| `CE_ExportTerminalPlan` | Export Terminal Plan | Exports validated cabinet-terminal connections to `~/integracad_terminal_plan.csv`. |

The continuous electrical-path domain contract follows a signal from its PLC
channel terminal through ordered wire segments and cabinet terminal levels to
the field-device terminal. Wiring and I/O schedule rows are projections of that
same identity-safe path. The standalone connection-path XML vocabulary is
namespace-correct and XSD validated; typed FreeCAD persistence and embedding in
the CEProject XML aggregate are implemented.

Continuous paths can now be created through **Add Electrical Path** and
materialized as typed FreeCAD document objects. The dialog selects registered
PLC and terminal-strip occurrences, selects or creates an immediately identified
field device through an explicit selector choice, and captures the complete
three-wire terminal chain. A
path object owns ordered terminal and wire link lists; terminal objects retain
their owner identity, role, and designation; wire objects link directly to their
endpoint terminals and persist route points, calculated length, conductor size,
color, circuit function, and conduit identity. Form normalization is tested
outside FreeCAD, and the FreeCAD command wraps all mutations in one abortable
document transaction. Each segment also accepts ordered `x,y,z` millimetre route
coordinates; when present, their polyline length is authoritative in the wiring
and I/O schedules, while a separate specified length remains preserved for
traceability. Select a typed path and run **Edit Electrical Path** to revise
those engineering fields without changing topology or identities. **Capture
Wire Route from Geometry** provides the corresponding graphical route selection
workflow described below.

`CE_Project` now owns typed `ElectricalSignals`, `ElectricalPaths`, and
`ElectricalDevices` link collections with canonical fact IDs. Materializing a
path creates or safely reuses its signal object, registers the signal and path on
the project, and permits reconstruction of the validated domain path from direct
FreeCAD links. **Validate Controls Project** reports broken typed links and
whole-project electrical graph findings.

**Capture Wire Route from Geometry** closes that first interactive route-capture
gap. Select exactly one typed `CE_Wire`, then select visible geometry with two
or more vertices and run the command. The workbench stores the ordered points,
validates the resulting route, updates the calculated length, and regenerates
its dependency-free Part polyline. **Route CE Wire with Cables** optionally
creates a Cables-workbench `WireFlex` physical route from that polyline, or
synchronizes a previously linked route back into the canonical CE wire. The CE
wire and route retain each other's immutable wire identity; if Cables is not
installed, the Part polyline remains the controlled fallback.

Typed field devices can now be created with an immutable identity and
`electrical.field_device` role before any terminal refers to them. Starter panel
creation automatically registers the PLC controller and terminal strip as
project electrical-device occurrences. This establishes resolvable owner IDs for
PLC-channel, cabinet-terminal, and device-terminal objects.

**Export Electrical Schedules** writes
`~/integracad_wiring_schedule.csv` and
`~/integracad_io_path_schedule.csv`. The wiring file has one row per physical
wire segment; the I/O path file has one row per signal path. Both are generated
from the same reconstructed and validated typed graph.

The pure-Python `controls_wb.missing_data.missing_data_matrix()` helper can build a structured missing-data matrix from a `ProjectIntake` payload or a `CE_Project`-style object without FreeCAD installed. Matrix rows include the required fact, current value, question ID, source records, verification/approval booleans, status, severity, finding, and recommended next action.
The companion `controls_wb.missing_data.missing_data_csv()` helper serializes those rows to a deterministic CSV export for spreadsheet review.

Editable `CE_Project` properties are converted back into the backend intake model before validation, missing-data preview, and CEProject XML export. Filling a starter property such as `PlcPlatform` or `SensorCount` in the FreeCAD Property View is treated as a received response even if the adjacent status field is still `Requested`; blank required properties remain reported as missing.

The pure-Python `controls_wb.ceproject_xml.ceproject_to_xml()` helper exports a `ProjectIntake` payload or `CE_Project`-style object to deterministic CEProject XML. The companion `controls_wb.ceproject_xml.parse_ceproject_xml()` helper reads the supported CEProject XML intake structure back into a stable pure-Python document wrapper. The current XML round trip includes metadata, contacts, intake deliverables and fields, intake question/response records, source records, validation findings, and missing-data matrix rows.

The pure-Python `controls_wb.io_list` module provides the first starter I/O list model. It generates deterministic CSV rows with tag, address, description, signal type, device, PLC rack/slot/channel placeholders, terminal placeholder, source record IDs, and mapping status. Project setup captures XML-backed PLC make/line/CPU, DI/DO/AI/AO counts, compatible Ethernet and power-supply selections, communication protocols, enclosure ratings, and optional modular I/O accessories. Explicit user-labeled I/O signals can be added through the dialog and reduce the remaining starter placeholders. **Allocate PLC I/O** turns a complete selected catalog CPU/module configuration into deterministic rack, slot, and channel assignments, rejects capacity/collision errors, and persists the valid allocation on `CE_Project` for save/reopen and I/O CSV export. Valid allocations can also be materialized as persistent, identity-safe `plc.rack`, `plc.module`, and `plc.channel` occurrences with rack-to-module-to-channel links. See [`docs/plc-allocation.md`](docs/plc-allocation.md) for the contract, persistence model, and current boundary.

For intake validation, `io.sensorCount` means input points only. The Project Intake dialog derives it from `DICount + AICount`; output counts still drive I/O list and expansion planning, but they are not treated as sensors. The `IOSignals` property remains blank until **Add I/O Signal** records explicit user-labeled signal rows.

The PLC hardware catalog lives at `controls_wb/resources/hardware/plc_catalog.xml` and is shaped by `schemas/plc_hardware_catalog_v0_1.xsd`. Starter panel hardware placeholder metadata lives at `controls_wb/resources/hardware/panel_catalog.xml` and is shaped by `schemas/panel_hardware_catalog_v0_1.xsd`. The first source-backed PLC seed is Siemens S7-1200; see [`docs/project-setup-hardware-catalog.md`](docs/project-setup-hardware-catalog.md) for the verified starter parts, panel placeholder seed, update rules, and amperage-calculation roadmap.

Project setup records a setup source record for filled starter facts. The source can be a manual entry, customer email, meeting note, phone call, field note, vendor quote, or uploaded file/reference. That source is attached to project name, voltage, phase, enclosure rating, PLC platform, and sensor/input-count facts where values are present.

The current project facts are addressable through the pure-Python `controls_wb.fact_ids` registry. It assigns stable IDs to supported project, intake, power, PLC/I/O, contact, source, question, signal, and status facts. Intake requirements, starter question IDs, setup source records, editable `CE_Project` property mappings, and missing-data row IDs use that registry so downstream exports can point back to the same fact surface.

Project setup can also store starter controlled-load lines such as `motor, Conveyor motor, 2, 1hp` and estimate total load amps from the selected phase/voltage with 20 percent spare capacity. This is an early planning aid, not a final electrical design calculation.

Project setup can import supported CEProject XML through the Project Intake dialog. Imported XML is remembered on the editable `CE_Project` object, can be selected again later, and preserves parsed project metadata, contacts, source records, and intake questions. The dialog can also import lightweight YAML-ish setup notes and PlantUML/UML-derived fact lines that map into the same Project Intake fields. Those setup text imports are adapter inputs, not remembered CEProject source records yet.

The first CAD-side layout objects are placeholders, not manufacturer-accurate models. **Create Control Panel** creates a panel/backplate, DIN rail, wire duct, terminal strip, and PLC rack/module with editable metadata such as tag, manufacturer, part number, description, panel name, voltage, current, terminal count, slot number, channel count, and signal type where applicable. Panel placeholder metadata comes from the XML panel hardware catalog. When a selected PLC CPU exists in the XML hardware catalog, the PLC placeholder receives the catalog manufacturer, part number, onboard channel count, and CADbase reference metadata. BOM export includes these objects when they expose controls metadata.

## Business thesis

Less havoc = more money.

IntegraCAB Open should reduce controls-engineering rework by making missing project data visible early, capturing facts once, tracking assumptions, and feeding downstream tools consistently.

## What IntegraCAB owns

- Structured project intake.
- Missing-data tracking.
- Role-based email and form templates.
- CEProject XML source-of-truth model.
- Validation findings and traceability.
- Power drop-in references from BIM/MEP/electrical teams.
- PLC/I/O and signal registry source data.
- HMI and digital-twin requirement source data for future companion workbenches.
- Adapter mappings to external tools.

## What IntegraCAB does not replace

| Area | Preferred owner |
|---|---|
| Reusable CAD parts, datasheets, CAD files | CADbase or equivalent library |
| BOM generation | Existing FreeCAD BOM workbench, Spreadsheet, BIM schedules, or ERP/export tools |
| BIM/facility model | FreeCAD BIM/openBIM tools and IFC workflows |
| Drawing sheet production | TechDraw or other drawing tools |
| Full PLC programming IDE | Vendor PLC IDEs or PLCopen-compatible tools |
| HMI screen editor | Future HMI companion workbench or vendor HMI tools |
| Simulation/digital twin engine | Future digital twin companion workbench or external simulators |

## Design principle

Do not draw first. Define and validate the controls project facts first, then feed CAD, BOM, PLC, HMI, BIM, costing, and documentation tools from the same structured data.

```text
Project Intake
    -> CEProject XML
        -> Validation
        -> CADbase references
        -> BOM source rows
        -> Spreadsheet/cost exports
        -> IFC/COBie/BCF handoff
        -> PLCopen XML mapping
        -> HMI requirements
        -> Digital twin seed data
```

## Key documents

- `TODO.md` - master roadmap and checklist.
- `docs/roadmap.md` - release direction.
- `docs/integration-first-policy.md` - what IntegraCAB should and should not own.
- `docs/intake-matrix.md` - stakeholder intake map.
- `docs/learning-path.md` - controls engineering learning path.
- `docs/companion-workbenches.md` - HMI and digital twin future workbench scope.
- `docs/standards-resource-map.md` - standards/resource families to point toward.
- `docs/project-setup-hardware-catalog.md` - XML-backed PLC catalog guide and schema link.
- `docs/plc-allocation.md` - deterministic PLC allocation and persistent occurrence model.
- `templates/email/` - role-based request templates.
- `templates/forms/` - structured form/schema seeds.

## Quick install for development

Clone, copy, or symlink this folder into your FreeCAD user `Mod` directory.

From the repository root, the repeatable symlink helper is:

```bash
python3 scripts/link_freecad_workbench.py
```

The script creates `~/.local/share/FreeCAD/Mod/ControlForgeCAD` as a symlink to `/home/egrantjr/Dev/CAD/ControlForgeCAD`. To use a different FreeCAD profile or source path:

```bash
python3 scripts/link_freecad_workbench.py --mod-dir /path/to/FreeCAD/Mod --source /path/to/ControlForgeCAD
```

For the Flatpak build, use
`~/.var/app/org.freecad.FreeCAD/data/FreeCAD/v1-1/Mod` as `--mod-dir`. See
[`docs/manual-freecad-gui-test-plan.md`](docs/manual-freecad-gui-test-plan.md)
for the complete future GUI acceptance checklist.

Equivalent manual symlink command:

```bash
mkdir -p ~/.local/share/FreeCAD/Mod
ln -s /home/egrantjr/Dev/CAD/ControlForgeCAD ~/.local/share/FreeCAD/Mod/ControlForgeCAD
```

Equivalent copy command:

```bash
mkdir -p ~/.local/share/FreeCAD/Mod
cp -R /home/egrantjr/Dev/CAD/ControlForgeCAD ~/.local/share/FreeCAD/Mod/ControlForgeCAD
```

Restart FreeCAD and select **Controls / Automation** from the workbench selector. Confirm these commands appear in the toolbar or menu:

| Command ID | Menu text |
|---|---|
| `CE_NewProject` | New Controls Project |
| `CE_AddIOSignal` | Add I/O Signal |
| `CE_AddConnection` | Add Connection Record |
| `CE_AddElectricalPath` | Add Electrical Path |
| `CE_EditElectricalPath` | Edit Electrical Path |
| `CE_CreatePanel` | Create Control Panel |
| `CE_ValidateProject` | Validate Controls Project |
| `CE_PreviewMissingData` | Preview Missing Data |
| `CE_ExportBOM` | Export BOM |
| `CE_ExportCEProjectXML` | Export CEProject XML |
| `CE_ExportIOList` | Export I/O List |
| `CE_ExportMissingDataCSV` | Export Missing Data CSV |
| `CE_ExportConnectionSchedule` | Export Connection Schedule |
| `CE_ExportElectricalSchedules` | Export Electrical Schedules |

Manual smoke validation:

1. Start or restart FreeCAD after linking or copying the workbench.
2. Select **Controls / Automation** from the workbench selector.
3. Run **New Controls Project** and confirm the Project Intake dialog opens with a link to the project setup hardware catalog guide.
4. Enter or edit project name, customer, site/location, deliverables, phase/voltage, enclosure ratings, XML-backed PLC make, PLC line, PLC CPU, DI/DO/AI/AO counts, compatible Ethernet/power selections, communication protocols, optional I/O accessories, and source metadata, then submit the dialog.
5. Confirm the I/O expansion planning popup appears and suggests whether CPU I/O covers the requested count plus 20 percent spare, or which starter expansion modules are needed.
6. Confirm `CE_Project` appears in the model tree and the Report View says the project intake was updated. If Qt/PySide cannot be loaded, confirm the fallback warning is printed and a starter `CE_Project` is still created.
7. Select `CE_Project` and confirm the Property View exposes editable CEProject and Intake properties matching the dialog values.
8. Reopen **New Controls Project**, import a CEProject XML file, submit, reopen the dialog, and confirm the imported XML appears in **Saved CEProject XML** and can be applied again.
9. Import a supported YAML, YML, PUML, PlantUML, UML, or TXT setup file and confirm matching form fields are populated before submit.
10. Edit one basic property, save the document as `.FCStd`, close it, reopen it, and confirm the property value is retained.
11. Clear `SensorCount`, `DICount`, and `AICount`, run **Preview Missing Data**, and confirm `io.sensorCount` is reported as missing.
12. Fill `SensorCount`, or fill DI and AI counts, rerun **Preview Missing Data**, and confirm the value is shown as an input-count response rather than missing.
13. Run **Validate Controls Project** and confirm validation messages print to the FreeCAD console from the edited object values. Filled setup fields with source metadata should not report `missing_source`; they may still need verification or approval.
14. Run **Add I/O Signal**, choose an I/O type, enter a label, and confirm Report View prints the generated tag and address.
15. Run **Create Control Panel** and confirm `CE_Backplate`, `CE_DIN_Rail`, `CE_Wire_Duct`, `CE_Terminal_Strip`, and `CE_PLC_Rack` appear in the model tree with editable controls metadata.
16. Run **Add Electrical Path**, select the registered PLC and terminal strip, select an existing field device or enter a new device tag, and submit the terminal/wire chain. Optionally enter each route as semicolon-separated `x,y,z` millimetre coordinates. Confirm one typed path, four typed terminals, three typed wires, and a signal appear with immutable identities and assigned roles; routed wires should display as polylines.
17. Select the typed path, run **Edit Electrical Path**, change a terminal designation and route, and confirm its path, signal, terminal, and wire identities do not change.
18. Run **Validate Controls Project** and confirm validation reads the project, starter layout metadata, and typed graph without dangling-owner or path-continuity findings.
19. Run **Export Electrical Schedules** and confirm `~/integracad_wiring_schedule.csv` has three wire rows while `~/integracad_io_path_schedule.csv` has one signal-path row containing the edited values.
20. Run **Export BOM** and confirm `~/controlforgecad_bom.csv` includes starter layout objects with tag/description/manufacturer/part-number data where assigned.
21. Run **Export CEProject XML** and confirm `~/integracab_ceproject.xml` is written.
22. Run **Export I/O List** and confirm `~/integracab_io_list.csv` is written. If starter I/O remains unmapped, confirm Report View prints a concise summary and the CSV contains the detailed rows.
23. Run **Export Missing Data CSV** and confirm `~/integracab_missing_data.csv` is written with one row per required intake fact.

Automated tests do not import real FreeCAD in this environment. They compile `Init.py` and `InitGui.py`, import both files without FreeCAD installed, and verify import-safe command metadata for the workbench command IDs above.

For pure-Python validation outside FreeCAD, run tests from the repository root:

```bash
/usr/bin/python3 -m pytest
python3 -m compileall ControlForgeCAD
```

or from this directory:

```bash
/usr/bin/python3 -m pytest
```

On this workstation, `/usr/bin/python3` has `pytest` available. The default
`python3` currently resolves to Homebrew Python and may report `No module named
pytest`.

## License

This repository uses the MIT License for original code, documentation, schemas, and examples unless a file states otherwise. See `LICENSE` and `docs/license-strategy.md`.

## Version control

This repository follows Semantic Versioning for public APIs and project deliverables. See `VERSIONING.md` and `docs/version-control.md`.
