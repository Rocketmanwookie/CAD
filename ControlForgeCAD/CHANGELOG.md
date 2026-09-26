# Changelog

## Unreleased

- Added persistent, idempotent PLC rack, module, and channel occurrences for a
  valid allocation. Their deterministic CE identities and direct containment
  links preserve the selected catalog placement and allocated signal metadata
  across FreeCAD document persistence.

- Added catalog-backed PLC I/O allocation with deterministic CPU/module slot and
  channel assignments, capacity/collision findings, persisted `CE_Project`
  mappings, allocation-aware I/O export, and the `CE_AllocatePLCIO` FreeCAD
  command.

- Newly materialized typed electrical paths now create backward-compatible
  connection records carrying stable path, signal, device, ordered-terminal,
  and ordered-wire identities. Connection schedule export includes those
  references, and project validation reports missing, dangling, wrong-role, and
  path-inconsistent links.

- Added `CE_RouteWireWithCables`, which creates or synchronizes an optional
  Cables-workbench `WireFlex` physical route for a typed `CE_Wire`.  The link is
  guarded by the wire's immutable CE identity in both directions, and the
  dependency-free Part-polyline remains the fallback when Cables is unavailable.

- Added `CE_ExportTerminalPlan`, a validated deterministic CSV projection of
  cabinet terminals and their connected wire-side endpoints.

- Added `CE_CaptureWireRoute`, which captures ordered vertices from selected
  FreeCAD geometry onto one typed `CE_Wire`, preserves CE identity, validates
  the route, recalculates length, and regenerates the Part-polyline fallback.

All notable changes to this project will be documented in this file.

This project follows Semantic Versioning once public APIs stabilize. During `0.y.z`, APIs, XML schemas, and generated output formats may change.

## [0.1.0-dev] - 2026-06-21

### Added

- Addon Manager metadata, SVG branding, document transaction boundaries, and an
  Addon Academy release checklist.
- Evidence-based AutoCAD Electrical PLC parity audit, target electrical-graph
  architecture, delivery gates, and strict parity definition.
- Working-MVP fast lane and deferred ROS/ROS 2 digital-twin integration boundary.
- Immutable CEProject UUID identities and controlled semantic roles assigned at
  project/layout object creation and restored for legacy document objects.
- Repository-level master completion prompt with XML conformance, identity,
  working-MVP, FreeCAD, adapter, validation, and completion gates.
- CEProject root identity and role now round-trip through namespace-aware XML;
  legacy XML without identity attributes receives a deterministic imported ID.
- Fixed, deterministic continuous electrical-path contract spanning PLC channel
  terminal, wire segments, cabinet terminal levels, and device terminal, with
  physical route lengths and common wiring/I/O schedule projections.
- Version 1.0 clarified as ROS/ROS 2 digital-twin ready, not runtime initialized.
- Wiring schedules now carry routed length, conductor size, color, circuit
  function, and conduit identity from the canonical wire segment.
- Profile-driven preliminary raceway sizing with NEC Chapter 9 fill percentages
  and explicit code edition, raceway type, supplied internal areas, and
  unverified status; reserved colors are separated from project conventions.
- Namespace-correct `ceproject.connection-path/1.0` XML serialization and XSD for
  continuous terminal/wire paths, including identities, roles, routing points,
  length fields, conductor data, ordered sequences, and deterministic round trips.
- Typed FreeCAD path, terminal, and wire objects that preserve CE identities and
  roles, own ordered object links, bind each wire to its terminal endpoints, keep
  route and conductor metadata, and reject identity collisions before placement.
- CEProject XML now imports the connection-path XSD namespace and embeds typed
  paths with deterministic ordering, round trips, semantic validation, and
  duplicate path-identity rejection.
- Whole-project electrical graph validation for duplicate identities, dangling
  signals/terminal owners, cross-signal terminal conflicts, inconsistent signal
  tags, and missing wire size/color/length schedule data.
- Typed signal objects and `CE_Project` signal/path/device link collections with
  canonical fact IDs, automatic path registration, signal reuse/tag conflict
  protection, typed path reconstruction, and FreeCAD validation-command output.
- Typed field-device occurrence creation and project registration, plus automatic
  electrical-device registration for placed PLC controller and terminal-strip
  layout objects so terminal owner identities resolve to project objects.
- `CE_ExportElectricalSchedules` command and deterministic typed-graph wiring/I/O
  path CSVs containing identities, ordered endpoints, terminal paths, conductor
  size/color/function, conduit identity, segment length, and total path length.
- Initial repository seed.
- FreeCAD external workbench bootstrap files: `Init.py` and `InitGui.py`.
- Draft controls-project data model.
- Draft `CEProject` XML schema.
- Conveyor demo XML instance.
- Mapping stubs for PLCopen XML, AutomationML/CAEX, and OPC UA NodeSet2.
- License strategy section.
- Version-control and configuration-management policy.
- Project-name brainstorm document.
- Starter `CE_NewProject` command for creating a CEProject intake object.
- Pure-Python intake field status and missing-data validation helpers.
- Tests for intake validation, BOM row collection, and document validation helpers.
- Starter stakeholder contact, source-record, and intake question/response models.
- Validation warning for verified or approved intake facts that lack source records.
- Pure-Python missing-data matrix rows for required intake facts, including response/source coverage, verification, approval, severity, findings, and next actions.
- CE project object parsing shared by validation and missing-data matrix generation, including enclosure rating response/status fields.
- Pure-Python deterministic CEProject XML export for intake metadata, contacts, fields, question/response records, source records, validation findings, and missing-data matrix rows.
- CEProject 0.1 XSD expansion for optional contacts, intake, source-record, validation, and missing-data matrix sections.
- Pure-Python CEProject XML import for the supported intake XML structure, including contacts, source records, questions/responses, validation findings, and missing-data rows.
- Export/import round-trip tests for representative intake-related CEProject XML data.
- `CE_PreviewMissingData` workbench command for console preview of the active project intake missing-data matrix.
- `CE_ExportCEProjectXML` workbench command for exporting the active project intake object to CEProject XML.
- FreeCAD workbench registration now groups starter project, validation, missing-data, BOM, and CEProject XML commands while keeping `InitGui.py` thin.
- Import-safe command metadata for smoke tests and workbench registration.
- `scripts/link_freecad_workbench.py` helper for creating a FreeCAD user `Mod/ControlForgeCAD` development symlink.
- README manual validation steps for confirming the workbench loads and expected commands appear in FreeCAD.
- Editable `CE_Project` FeaturePython document object with explicit CEProject and Intake properties for project name, customer, site/location, deliverables, PLC platform, voltage, phase count, enclosure rating, and sensor count.
- `CE_NewProject` now creates or refreshes the active document's starter `CE_Project` object instead of relying on unstructured starter-only data.
- Editable `CE_Project` Property View values now synchronize into backend intake validation, missing-data preview, and CEProject XML payload mapping.
- `CE_NewProject` now opens a Project Intake dialog for core starter fields when Qt/PySide is available, with a safe starter-object fallback when the GUI cannot be shown.
- Starter pure-Python I/O list model and deterministic CSV export helpers driven by project intake sensor count.
- `CE_ExportIOList` workbench command for exporting `~/integracab_io_list.csv` and reporting unmapped starter I/O points.
- Starter CAD-side controls layout objects for panel/backplate, DIN rail, wire duct, terminal strip, and PLC rack/module placeholders.
- `CE_CreatePanel` now creates the starter layout object set, and BOM export can include those objects through their controls metadata.
- Deterministic missing-data matrix CSV export helper and `CE_ExportMissingDataCSV` workbench command.
- Pure-Python project setup import adapters for lightweight YAML-ish setup files and PlantUML/UML-derived fact lines.
- Project Intake dialog button for importing YAML, YML, PUML, PlantUML, UML, or TXT setup files into starter intake fields.
- Stable pure-Python CEProject fact ID registry for current project, intake, power, PLC/I/O, source, contact, and status facts.
- Intake requirements, starter question IDs, setup source records, editable project properties, and missing-data row IDs now use the central fact ID registry.
- Claude review handoff note with current repository path, validation commands, review focus, known limitations, and next-milestone recommendation.
- CEProject object-to-intake mapping now carries the richer editable `CE_Project` setup fields into validation and XML export, including customer/site, typed I/O counts, PLC selections, controlled loads, enclosure rating lists, accessories, and communication protocols.
- CEProject XML import now accepts schema-valid documents without an `Intake` section and restores richer intake facts back into the Project Intake form when those field IDs are present.

### Known limitations

- Workbench commands are architecture stubs, not production FreeCAD tools yet.
- FreeCAD command validation for this milestone is documented as a manual step because no usable headless `freecadcmd` CLI is available in the test environment.
- XML mappings are illustrative and not full certified exports.
- CEProject XML import currently covers the intake-related XML emitted by the exporter and schema-valid metadata-only/demo documents, not future device, signal, circuit, PLC, HMI, or BIM sections.
- YAML/UML setup import intentionally supports a small key/value and list subset; full YAML and formal UML parsing remain future adapter work.
- Generated artifact rows are not yet fully trace-linked back to fact IDs beyond existing source record and missing-data references.
- Safety validation is structural only; it does not certify PL, SIL, or category compliance.
