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

### Known limitations

- Workbench commands are architecture stubs, not production FreeCAD tools yet.
- XML mappings are illustrative and not full certified exports.
- Safety validation is structural only; it does not certify PL, SIL, or category compliance.
