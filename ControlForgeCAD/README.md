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
| `CE_NewProject` | New Controls Project | Creates a starter `CE_Project` object with CEProject metadata, stakeholder contacts, source records, question/response records, required response fields, and initial intake statuses. |
| `CE_CreatePanel` | Create Control Panel | Creates a parametric backplate placeholder with controls metadata. |
| `CE_ExportBOM` | Export BOM | Exports controls metadata rows from the active FreeCAD document to CSV. |
| `CE_ValidateProject` | Validate Controls Project | Reports duplicate tags, missing controls metadata, starter intake missing-data findings, and verified/approved intake facts without source records. |

The pure-Python `controls_wb.missing_data.missing_data_matrix()` helper can build a structured missing-data matrix from a `ProjectIntake` payload or a `CE_Project`-style object without FreeCAD installed. Matrix rows include the required fact, current value, question ID, source records, verification/approval booleans, status, severity, finding, and recommended next action.

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

Clone or copy this folder into your FreeCAD user `Mod` directory.

```bash
mkdir -p ~/.local/share/FreeCAD/Mod
cd ~/.local/share/FreeCAD/Mod
git clone <repo-url> IntegraCABOpen
```

Restart FreeCAD and select **Controls / Automation** from the workbench selector once the workbench metadata is fully renamed.

For pure-Python validation outside FreeCAD, run tests from this directory:

```bash
python3 -m pytest
```

## License

This repository uses the MIT License for original code, documentation, schemas, and examples unless a file states otherwise. See `LICENSE` and `docs/license-strategy.md`.

## Version control

This repository follows Semantic Versioning for public APIs and project deliverables. See `VERSIONING.md` and `docs/version-control.md`.
