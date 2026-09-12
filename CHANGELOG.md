# Changelog

All notable changes to **integraCAD Open** are documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions and intends to use [Semantic Versioning](https://semver.org/) once formal releases begin.

## [Unreleased]

### Added

- Added an XSD-validated technical-document registry linked from the master
  equipment catalog, deterministic datasheet-link and acceptance-test CSV
  exports, and a regeneration script. The registry currently covers all 285 CAD
  requests, links the supplied CPU 1212C datasheet with its SHA-256 checksum,
  records unresolved acquisition states honestly, and emits 2,656 tailored test
  instructions with required evidence.
- Added a 285-row CAD-library download manifest covering the requested Siemens
  PLC, panel, safety, operator, HMI, instrumentation, wiring, connector, and
  vendor-neutral accessory scope. Exact source-backed MLFBs are distinguished
  from configuration-required search keys, and every applicable row identifies
  required 3D, 2D, schematic, terminal-map, macro, and Cables-workbench assets.
- Added `CE_AddElectricalPath`, a transaction-safe FreeCAD workflow that creates
  the canonical PLC-channel → cabinet-terminal pair → field-device terminal
  chain, assigns immutable identities and roles at creation, registers an
  optional new field device before terminal ownership is persisted, and captures
  conductor size, approved color/function, wire tags, and segment lengths for
  the shared wiring and I/O schedule graph.
- Added optional ordered 3D route-coordinate entry for every created wire.
  Routes are validated as finite polylines, persisted on typed FreeCAD wire
  objects, rendered when Part geometry is available, and used to derive wiring
  and I/O schedule lengths without discarding a separately specified estimate.
- Added `CE_EditElectricalPath` for transaction-safe correction of a selected
  path's signal tag, terminal designations, wire metadata, specified lengths,
  and route geometry. The update boundary rejects identity changes and duplicate
  signal tags before mutating persisted objects.
- Added a schema-versioned neutral equipment catalog with source-traceable equipment classes and links to specialized PLC, panel, and vendor-record catalogs.
- Added a normalized Siemens SIMATIC S7-1200 XML record database containing 104 brochure-derived products across 13 categories, 20 TIA V20 data types, checksummed source aliases, CAD assets, and supplied reference files. Imported claims remain explicitly unverified pending source audit.
- Added deterministic JSON-to-equipment-XML import and read-only catalog exploration CLIs with category, search, and exact part-number views.
- Added pure-Python tests for equipment taxonomy loading, linked-catalog resolution, normalized record lookup/search, duplicate rejection, typed property preservation, and source hashing.
- Established [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) as the architectural source of truth for integraCAD Open, covering system context, layered architecture, component responsibilities, dependency boundaries, object contracts, data flows, extension strategy, testing, operational considerations, and current-versus-planned capabilities. Commit: `6dfeb12`.
- Added contributor-facing architecture checklists for project fields, FreeCAD document objects, exports, and vendor adapters in [`CONTRIBUTING.md`](CONTRIBUTING.md). Commit: `1a0c985`.
- Added a README architecture summary, current-capability statement, generated-artifact contract summary, and extension guidance. Commit: `b4c70c0`.
- Added contributor documentation and changelog traceability. Commits: `f1f9a6c`, `b5de200`, `c7a3fe1`.

### Changed

- Made intelligent schematic symbols a required companion contract for
  applicable equipment records, including IEC and NFPA/JIC variants, structured
  terminal pins, parent/child cross-references, and links to the same device
  occurrence used by 3D, wiring, BOM, and schedule projections.
- Defined the FreeCAD Cables workbench as the target physical routing engine;
  ControlForgeCAD owns electrical semantics and schedules and will link them to
  Cables route objects, retaining its current Part polyline only as a fallback.
- Standardized project terminology so **integraCAD Open** identifies the overall project and **ControlForgeCAD** identifies the FreeCAD workbench implementation.
- Defined the supported dependency direction from FreeCAD UI and adapters toward application services, domain contracts, and deterministic serializers.
- Documented `CE_Project` as the authoritative interactive project aggregate stored in the FreeCAD document.
- Clarified that starter layout objects, CEProject XML, BOM CSV, I/O-list CSV, and validation are implemented foundation contracts with partial engineering scope.
- Clarified that manufacturer catalog adapters, automatic hardware selection, full schematic generation, terminal/wire schedules, and PLC vendor project-file generation remain planned.
- Expanded contribution requirements so material contract, schema, boundary, data-flow, or implementation-status changes must update architecture documentation and this changelog.

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

Entries should describe user-visible or contributor-relevant effects, reference the affected subsystem, state whether a public contract or generated artifact changed, and include an issue or pull-request link when available.

A change to system boundaries, object contracts, validation paths, XML/CSV schemas, dependency direction, or implementation-status claims must also update [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
