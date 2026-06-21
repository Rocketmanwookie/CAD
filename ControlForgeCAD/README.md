# ControlForgeCAD - FreeCAD Controls Engineering Workbench

> Working title. Final project name is still open.

ControlForgeCAD is a proposed FreeCAD external Python workbench for controls engineering. The workbench is intended to connect PLC I/O, ladder/logic models, 3D control-panel layouts, wiring diagrams, safety relay circuits, power distribution, sensor installation data, BOMs, and standardized XML interchange into one model-based engineering workflow.

## Project status

| Field | Value |
|---|---|
| Status | Pre-alpha / architecture seed |
| Version | 0.1.0-dev |
| FreeCAD target | FreeCAD 1.x |
| Language | Python |
| Workbench type | External Python workbench |
| License | MIT for original project code and docs |
| XML schema version | CEProject 0.1.0 |

## Design principle

Do not draw first. Define the controls model first, then generate drawings, schedules, reports, and exports from the shared project data.

```text
Controls Project Model
    |-- PLC I/O map
    |-- Ladder / logic model
    |-- 3D panel layout
    |-- Wiring diagrams
    |-- Terminal schedules
    |-- Safety relay circuits
    |-- Power distribution
    |-- Sensor installation data
    |-- BOM
    |-- XML interchange
```

## Initial feature roadmap

### MVP-1: PLC I/O -> 3D panel layout -> BOM

- Create a FreeCAD workbench that loads in the GUI.
- Add parametric control-panel objects: enclosure, backplate, DIN rail, wire duct, PLC module, terminal block, power supply, safety relay, sensor/device placeholder.
- Store controls metadata on FreeCAD document objects.
- Export device list, BOM, and I/O list to CSV.
- Validate missing tags, duplicate addresses, missing BOM fields, and unplaced devices.

### MVP-2: Wiring and terminal model

- Add connection tables.
- Generate terminal schedules.
- Generate point-to-point wiring CSV.
- Build first SVG/PDF wiring diagram generator.

### MVP-3: Ladder / logic model

- Add internal rung graph model.
- Generate readable ladder documentation.
- Add PLCopen XML mapping stub.

### MVP-4: Safety and power model

- Add safety-function templates.
- Add power-distribution net model.
- Add validation rules for safety relay circuits, STO circuits, branch protection, protective earth, and 24 VDC load budgets.

### MVP-5: Standards-oriented XML interchange

- Stabilize `CEProject` XSD.
- Map to PLCopen XML, AutomationML/CAEX, OPC UA NodeSet2, and STEP/AP242-related references where appropriate.

## Quick install for development

Clone or copy this folder into your FreeCAD user `Mod` directory.

```bash
mkdir -p ~/.local/share/FreeCAD/Mod
cd ~/.local/share/FreeCAD/Mod
git clone <repo-url> ControlForgeCAD
```

Restart FreeCAD and select **Controls Engineering** from the workbench selector.

## License

This repository uses the MIT License for original code, documentation, schemas, and examples unless a file states otherwise. See `LICENSE` and `docs/license-strategy.md`.

## Version control

This repository follows Semantic Versioning for public APIs and project deliverables. See `VERSIONING.md` and `docs/version-control.md`.
