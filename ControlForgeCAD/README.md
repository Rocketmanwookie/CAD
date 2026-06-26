# IntegraCAB™ Open

**The open-source FreeCAD workbench that unites PLC controls with CAD.**

IntegraCAB Open is an integration-first FreeCAD workbench concept for controls engineering. Its primary job is not to replace CADbase, BOM workbenches, BIM tools, PLC IDEs, HMI platforms, or digital-twin simulators. Its job is to collect controls-engineering requirements once, validate missing or contradictory information, maintain traceability, and feed existing tools from one structured source of truth.

> Working branch note: this repository seed still lives under `ControlForgeCAD/` until the rename task is completed.

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
| `CE_NewProject` | New Controls Project | Opens a project intake dialog for core project/customer/site/deliverable/intake fields, then creates or refreshes an editable `CE_Project` FeaturePython document object. If Qt/PySide is unavailable, it creates the starter object and prints a warning. |
| `CE_CreatePanel` | Create Control Panel | Creates a parametric backplate placeholder with controls metadata. |
| `CE_ExportBOM` | Export BOM | Exports controls metadata rows from the active FreeCAD document to CSV. |
| `CE_ValidateProject` | Validate Controls Project | Reports duplicate tags, missing controls metadata, starter intake missing-data findings, and verified/approved intake facts without source records. |
| `CE_PreviewMissingData` | Preview Missing Data | Prints the missing-data matrix for the active controls project intake object to the FreeCAD console. |
| `CE_ExportCEProjectXML` | Export CEProject XML | Exports the first controls project intake object in the active document to `~/integracab_ceproject.xml`. |

The pure-Python `controls_wb.missing_data.missing_data_matrix()` helper can build a structured missing-data matrix from a `ProjectIntake` payload or a `CE_Project`-style object without FreeCAD installed. Matrix rows include the required fact, current value, question ID, source records, verification/approval booleans, status, severity, finding, and recommended next action.

Editable `CE_Project` properties are converted back into the backend intake model before validation, missing-data preview, and CEProject XML export. Filling a starter property such as `PlcPlatform` or `SensorCount` in the FreeCAD Property View is treated as a received response even if the adjacent status field is still `Requested`; blank required properties remain reported as missing.

The pure-Python `controls_wb.ceproject_xml.ceproject_to_xml()` helper exports a `ProjectIntake` payload or `CE_Project`-style object to deterministic CEProject XML. The companion `controls_wb.ceproject_xml.parse_ceproject_xml()` helper reads the supported CEProject XML intake structure back into a stable pure-Python document wrapper. The current XML round trip includes metadata, contacts, intake deliverables and fields, intake question/response records, source records, validation findings, and missing-data matrix rows.

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
| `CE_CreatePanel` | Create Control Panel |
| `CE_ValidateProject` | Validate Controls Project |
| `CE_PreviewMissingData` | Preview Missing Data |
| `CE_ExportBOM` | Export BOM |
| `CE_ExportCEProjectXML` | Export CEProject XML |

Manual smoke validation:

1. Start or restart FreeCAD after linking or copying the workbench.
2. Select **Controls / Automation** from the workbench selector.
3. Run **New Controls Project** and confirm the Project Intake dialog opens.
4. Enter or edit project name, customer, site/location, deliverables, PLC platform, nominal voltage, phase count, enclosure rating, and sensor count, then submit the dialog.
5. Confirm `CE_Project` appears in the model tree and the Report View says the project intake was updated. If Qt/PySide cannot be loaded, confirm the fallback warning is printed and a starter `CE_Project` is still created.
6. Select `CE_Project` and confirm the Property View exposes editable CEProject and Intake properties matching the dialog values.
7. Edit one basic property, save the document as `.FCStd`, close it, reopen it, and confirm the property value is retained.
8. Clear `SensorCount`, run **Preview Missing Data**, and confirm `io.sensorCount` is reported as missing.
9. Fill `SensorCount`, rerun **Preview Missing Data**, and confirm the value is shown as a response rather than missing.
10. Run **Validate Controls Project** and confirm validation messages print to the FreeCAD console from the edited object values.
11. Run **Export CEProject XML** and confirm `~/integracab_ceproject.xml` is written.

Automated tests do not import real FreeCAD in this environment. They compile `Init.py` and `InitGui.py`, import both files without FreeCAD installed, and verify import-safe command metadata for the workbench command IDs above.

For pure-Python validation outside FreeCAD, run tests from the repository root:

```bash
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

or from this directory:

```bash
python3 -m pytest
```

## License

This repository uses the MIT License for original code, documentation, schemas, and examples unless a file states otherwise. See `LICENSE` and `docs/license-strategy.md`.

## Version control

This repository follows Semantic Versioning for public APIs and project deliverables. See `VERSIONING.md` and `docs/version-control.md`.
