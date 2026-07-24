# Changelog

All notable changes to integraCAD Open are documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions and intends to use [Semantic Versioning](https://semver.org/) once formal releases begin.

## [Unreleased]

### Added

- Architecture documentation initiative covering system boundaries, components, data flows, extension points, and operational considerations.
- Contributor documentation and changelog traceability.

### Changed

- Documentation terminology is being aligned so **integraCAD Open** identifies the overall project and **ControlForgeCAD** identifies the FreeCAD workbench implementation.

## Milestone History

### Editable CE_Project object contract

- Added an editable FreeCAD `CE_Project` document object.
- Defined project and intake property specifications.
- Added deterministic object creation and update behavior.
- Commit: `abb2201`.

### Intake validation synchronization

- Connected `CE_Project` properties to backend intake validation.
- Added missing-data payload generation based on current document state.
- Commit: `05e69d1`.

### Project Intake dialog

- Added a Qt/PySide Project Intake dialog to `CE_NewProject`.
- Added a safe fallback path when the GUI toolkit is unavailable.
- Commit: `a240c5b`.

### Starter I/O list

- Added a starter I/O-list model.
- Added deterministic CSV export through `CE_ExportIOList`.
- Commit: `9ef069e`.

### Starter physical-layout objects

- Added starter panel/backplate, DIN rail, wire duct, terminal strip, PLC rack, and PLC module objects.
- Extended BOM export to include supported layout objects.
- Commit: `57bbe4f`.

### Earlier project foundations

- Added intake source records and questions: `594a9a5`.
- Added the missing-data matrix: `19de1c4`.
- Added starter controls-project intake support: `ac75fb2`.
- Documented the integraCAD Open direction: `682d412`.
- Updated XML standards documentation: `11e449a`.
- Added the project roadmap: `237464a`.
- Added the smoke-install workflow: `faeedfc`.
- Added split-execution-safe FreeCAD workbench initialization: `9295f05`, `02532d0`.

## Contribution Entry Format

Each contribution should add an entry under **Unreleased** using one of these categories:

- `Added` for new capabilities.
- `Changed` for behavior, architecture, or documentation changes.
- `Deprecated` for features scheduled for removal.
- `Removed` for deleted capabilities.
- `Fixed` for defect corrections.
- `Security` for vulnerability-related changes.

Entries should describe user-visible or contributor-relevant effects, reference the affected subsystem, and include an issue or pull-request link when available.
