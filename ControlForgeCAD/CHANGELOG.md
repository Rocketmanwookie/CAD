# Changelog

All notable changes to this project will be documented in this file.

This project follows Semantic Versioning once public APIs stabilize. During `0.y.z`, APIs, XML schemas, and generated output formats may change.

## [0.1.0-dev] - 2026-06-21

### Added

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

### Known limitations

- Workbench commands are architecture stubs, not production FreeCAD tools yet.
- FreeCAD command validation for this milestone is documented as a manual step because no usable headless `freecadcmd` CLI is available in the test environment.
- XML mappings are illustrative and not full certified exports.
- CEProject XML import currently covers the intake-related XML emitted by the exporter, not future device, signal, circuit, PLC, HMI, or BIM sections.
- Safety validation is structural only; it does not certify PL, SIL, or category compliance.
