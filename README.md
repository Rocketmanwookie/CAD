# integraCAD Open

This repository contains **integraCAD Open**, an open-source controls-engineering CAD project. Its current FreeCAD implementation is the **ControlForgeCAD** workbench under `ControlForgeCAD/`.

## Project documentation

- [Architecture overview](docs/ARCHITECTURE.md) — architectural source of truth for system boundaries, layers, component contracts, data flows, dependencies, extension strategy, and implementation status.
- [Contributing](CONTRIBUTING.md) — development workflow, testing expectations, architecture rules, and documentation requirements.
- [Changelog](CHANGELOG.md) — implemented milestones, unreleased changes, and contributor-facing change history.

## Architecture summary

ControlForgeCAD uses a layered design:

1. **FreeCAD UI** — workbench registration, commands, menus, toolbars, and dialogs.
2. **FreeCAD adapters** — `CE_Project` properties, document-object creation, persistence, and translation into backend inputs.
3. **Application services** — project intake, validation, missing-data, layout, and export orchestration.
4. **Domain contracts** — controls-project, intake, I/O, hardware/layout, and validation models.
5. **Boundary services** — deterministic CEProject XML, BOM CSV, and I/O-list CSV serialization.

FreeCAD-specific code should remain thin. Controls-domain rules and serializers should be testable without launching the FreeCAD GUI wherever practical. See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) before changing system boundaries or adding integrations.

## Current capability status

Implemented starter capabilities include:

- editable `CE_Project` project and intake properties;
- a Project Intake dialog with safe GUI fallback;
- missing-data preview and starter project validation;
- starter panel/backplate, DIN rail, wire duct, terminal strip, PLC rack, and PLC module objects;
- CEProject XML export;
- BOM CSV export; and
- deterministic starter I/O-list CSV export.

These are foundation contracts, not yet a complete electrical schematic, automatic hardware-selection, terminal/wire-schedule, or vendor project-generation system. Manufacturer catalog adapters and richer engineering automation remain planned.

## FreeCAD development install

Link or copy `ControlForgeCAD/` into your FreeCAD user `Mod` directory, then restart FreeCAD. The helper script creates an idempotent symlink from this checkout:

```bash
python3 scripts/link_freecad_workbench.py
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

In FreeCAD, select **Controls / Automation** from the workbench selector. Confirm these commands appear in the toolbar or menu:

- `CE_NewProject` — New Controls Project
- `CE_CreatePanel` — Create Control Panel
- `CE_ValidateProject` — Validate Controls Project
- `CE_PreviewMissingData` — Preview Missing Data
- `CE_ExportBOM` — Export BOM
- `CE_ExportCEProjectXML` — Export CEProject XML
- `CE_ExportIOList` — Export I/O List

## Generated artifacts

The current command defaults are:

- CEProject XML: `~/integracab_ceproject.xml`
- BOM CSV: `~/controlforgecad_bom.csv`
- I/O-list CSV: `~/integracab_io_list.csv`

These output contracts are starter implementations. Changes to their schemas, ordering, naming, or overwrite behavior must be documented in the architecture and changelog.

## Automated validation

Run from the repository root:

```bash
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

Pure controls-domain behavior should have automated tests that do not require FreeCAD when practical. FreeCAD-dependent changes should retain import safety and GUI fallback behavior.

## Manual FreeCAD validation

1. Start or restart FreeCAD after linking or copying the workbench.
2. Select **Controls / Automation** from the workbench selector.
3. Confirm the commands listed above appear in the workbench toolbar or menu.
4. Run **New Controls Project** and confirm the Project Intake dialog opens.
5. Enter core intake values, submit the dialog, and confirm a `CE_Project` object appears in the model tree.
6. Select `CE_Project` and confirm the Property View exposes editable CEProject and Intake properties including project name, customer, site/location, deliverables, PLC platform, voltage, phase count, enclosure rating, and sensor count.
7. Save the document as `.FCStd`, close it, reopen it, and confirm the basic editable `CE_Project` properties are retained.
8. Clear `SensorCount`, run **Preview Missing Data**, and confirm `io.sensorCount` is reported as missing.
9. Fill `SensorCount`, rerun **Preview Missing Data**, and confirm the value is shown as a response rather than missing.
10. Run **Create Control Panel** and confirm starter placeholder layout objects appear for panel/backplate, DIN rail, wire duct, terminal strip, and PLC rack/module.
11. Run **Validate Controls Project** and confirm validation reads the edited project and starter layout metadata.
12. Run **Export BOM** and confirm `~/controlforgecad_bom.csv` includes starter layout objects where manufacturer/part-number/description data is assigned.
13. Run **Export CEProject XML** and confirm `~/integracab_ceproject.xml` is written.
14. Run **Export I/O List** and confirm `~/integracab_io_list.csv` is written from the current starter intake data.

## Extending the system

Before adding a command, project property, export format, or vendor integration, follow the extension checklists in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). New features must preserve dependency direction: GUI code may call domain/application services, but domain logic must not depend on FreeCAD GUI widgets.

## Contribution traceability

Every material contribution must update the relevant documentation and add an entry under **Unreleased** in [`CHANGELOG.md`](CHANGELOG.md). See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the required validation, architecture-review, and changelog workflow.
