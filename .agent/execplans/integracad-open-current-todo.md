# integraCAD / IntegraCAB Open Current TODO ExecPlan

This ExecPlan is a living implementation plan for continuing the existing `Whrsdaparty/CAD` repository on branch `controlforgecad`. It follows the repository's current files and TODO backlog, not a replacement scaffold.

## Current State

- Active branch: `controlforgecad`.
- Initial working tree status: clean.
- Required guidance files: `AGENTS.md` and `.agent/PLANS.md` were requested but are not present in this checkout. The root contains `.agents/` and `.codex/` read-only placeholders.
- Root layout:
  - `README.md` is a minimal top-level placeholder.
  - `ControlForgeCAD/` contains the actual FreeCAD external workbench package.
- Workbench directory structure:
  - `ControlForgeCAD/Init.py`
  - `ControlForgeCAD/InitGui.py`
  - `ControlForgeCAD/controls_wb/`
  - `ControlForgeCAD/controls_wb/commands/`
  - `ControlForgeCAD/controls_wb/model/`
  - `ControlForgeCAD/docs/`
  - `ControlForgeCAD/examples/`
  - `ControlForgeCAD/schemas/`
  - `ControlForgeCAD/stubs/`
  - `ControlForgeCAD/templates/email/`
  - `ControlForgeCAD/templates/forms/`
- Existing workbench/package names:
  - Folder: `ControlForgeCAD`.
  - Python package: `controls_wb`.
  - `pyproject.toml` package name: `controlforgecad`.
  - FreeCAD workbench class: `ControlsEngineeringWorkbench`.
  - `package.xml` name: `ControlForgeCAD`.
- FreeCAD initialization status:
  - `Init.py` is present and thin; it prints a `ControlForgeCAD` loading message when FreeCAD imports are available.
  - `InitGui.py` is present and registers `ControlsEngineeringWorkbench` when `FreeCADGui` is importable.
  - GUI imports are guarded for non-FreeCAD environments.
- Existing command IDs:
  - `CE_NewProject`
  - `CE_CreatePanel`
  - `CE_ExportBOM`
  - `CE_ValidateProject`
- Existing commands:
  - `new_project.py` creates a starter `CE_Project` with CEProject metadata, intake statuses, contacts, source records, and question/response records.
  - `create_panel.py` creates a parametric backplate placeholder named `CE_Backplate`.
  - `export_bom.py` collects object attributes `Tag`, `Description`, `Manufacturer`, and `PartNumber` into CSV rows.
  - `validate_project.py` checks duplicate tags, missing description/part number for tagged objects, missing intake facts, and verified/approved intake facts without source records.
- Existing model code:
  - `controls_wb/model/panel.py` defines a FreeCAD FeaturePython control panel/backplate placeholder.
  - `controls_wb/missing_data.py` defines pure-Python missing-data matrix rows and CE project object intake parsing.
- Existing TODO items:
  - The master TODO is `ControlForgeCAD/TODO.md`.
  - It calls for identity cleanup toward IntegraCAB Open, but the repository still intentionally lives under `ControlForgeCAD/`.
  - Phase 1 prioritizes structured project intake, contacts/stakeholder model, question/response model, missing-data matrix, field status model, source record model, templates, and validation output telling who to ask for missing information.
  - Phase 2 prioritizes CEProject data model sections, schema versioning, ID-addressable facts, generated-artifact traceability, and assumptions/estimates.
  - Phase 6 later covers PLC/I/O and signal registry work.
- Existing tests:
  - `pyproject.toml` configures `pytest` with `testpaths = ["tests"]`.
  - Current tests cover intake validation, BOM row collection, project payload serialization, and document validation helpers.
- Existing examples:
  - `examples/conveyor_demo.ceproject.xml` contains a CEProject 0.1.0 conveyor demo with `Metadata`, `Devices`, `Signals`, and `Connections`.
- Existing README/install instructions:
  - `ControlForgeCAD/README.md` documents IntegraCAB Open, pre-alpha status, FreeCAD external workbench install by cloning into the FreeCAD `Mod` directory, and a note that the seed still lives under `ControlForgeCAD/`.
  - The root `README.md` only says `# CAD` and `CAD Scripts`.
- Existing roadmap/issue notes:
  - `docs/roadmap.md` defines release 0.1 seed architecture and 0.2 intake/validation prototype.
  - `docs/integration-first-policy.md`, `docs/intake-matrix.md`, and related docs reinforce the integration-first intake/validation direction.
- Naming mismatches:
  - README and TODO use `IntegraCAB Open` and display name `IntegraCAB™ Open`.
  - User context also mentions `integraCAD Open`.
  - Current code and metadata still use `ControlForgeCAD`, `controls_wb`, and `ControlsEngineeringWorkbench`.
  - README says FreeCAD menu label should be `Controls / Automation`, while `InitGui.py` currently uses `Controls Engineering`.
  - TODO asks for Python package `integracab`, but renaming package/folders would be broad and risky at this stage. Keep current package names unless a load blocker appears.

## Goal

Continue the existing FreeCAD controls-engineering workbench toward the next working MVP milestone without replacing the project scaffold. The immediate milestone is the intake and validation prototype: add an initial project/intake command and pure-Python intake validation that can run under tests without FreeCAD.

Current milestone: add pure-Python CEProject XML import and round-trip validation for the Phase 2 intake-related XML structure currently produced by the exporter.

## Milestones

1. Document current state and naming decisions in this ExecPlan.
2. Add a minimal CEProject/intake data model in importable pure-Python modules.
3. Add a FreeCAD command that creates an initial controls project/intake object.
4. Extend validation to report missing intake fields and who to ask next where practical.
5. Add focused pure-Python tests for intake validation, existing BOM collection, and existing tag validation.
6. Update README and TODO to reflect completed behavior only.
7. Run validation commands and record results.
8. Add starter stakeholder contact, source-record, and question/response models.

## Progress

- [x] Inspected repository branch and confirmed `controlforgecad`.
- [x] Confirmed initial working tree was clean.
- [x] Read required repository files where present: root README, workbench README, TODO, roadmap, package metadata, FreeCAD init files, schema, example, and command/model modules.
- [x] Created this ExecPlan at `.agent/execplans/integracad-open-current-todo.md`.
- [x] Implement intake/project milestone.
- [x] Add or update tests.
- [x] Update docs/TODO.
- [x] Run validation.
- [x] Implement starter contact/source/question-response milestone.
- [x] Add source-record traceability validation for verified or approved intake facts.
- [x] Add tests for open intake questions, source-backed verified facts, missing source warnings, serialized project payloads, and document validation source parsing.
- [x] Update README, TODO, and changelog for the source/question model behavior.
- [x] Implement Phase 1 missing-data matrix.
- [x] Add tests for complete, missing response, missing source, needs verification, needs approval, and CE project object matrix generation.
- [x] Update README, TODO, changelog, and this ExecPlan for the missing-data matrix milestone.
- [x] Implement Phase 2 CEProject XML intake export.
- [x] Expand the CEProject 0.1 XSD with optional contacts, intake, source-record, validation, and missing-data matrix sections.
- [x] Add deterministic XML tests for minimal projects, contacts, source records, intake questions/responses, validation findings, and missing-data rows.
- [x] Document XML export behavior and defer import/parsing as a follow-up.
- [x] Implement Phase 2 CEProject XML intake import/parsing.
- [x] Add import tests for minimal XML, contacts, source records, intake questions/responses, validation and missing-data findings, representative round-trip data, and invalid/incomplete XML handling.
- [x] Update README, TODO, changelog, and this ExecPlan for the XML import/round-trip milestone.

## Surprises & Discoveries

- `AGENTS.md` and `.agent/PLANS.md` are absent, so no local repo-specific agent guidance could be applied beyond the user's instructions.
- The repository has no current tests even though pytest is configured.
- The root README is not the product README; the useful README is under `ControlForgeCAD/`.
- The TODO asks for eventual identity/package renames, but the README explicitly notes the seed still lives under `ControlForgeCAD/`.

## Decision Log

- Keep `ControlForgeCAD/`, `controls_wb`, package metadata, and existing command prefix `CE_` for now. This avoids a broad rename and preserves current load conventions.
- Apply the smallest safe display-label correction: align the FreeCAD workbench/menu text with the TODO/README label `Controls / Automation` while preserving the class name and command IDs.
- Implement business logic as pure Python under `controls_wb/` and keep `InitGui.py` thin.
- Treat Phase 1 intake/validation as the next TODO-backed milestone before PLC/I/O expansion.
- Update `TODO.md` checkboxes only for behavior that is present in code now. Broader roadmap items remain open even when a seed exists.
- Treat the starter contact/source/question-response model as sufficient to close those Phase 1 model checkboxes, while keeping templates and full CEProject XML schema work open.
- Keep the missing-data matrix as a pure-Python helper instead of a FreeCAD command for this milestone.
- Defer CSV export for the missing-data matrix until the project has a clearer export convention.
- Add XML export in `controls_wb.ceproject_xml` instead of the FreeCAD model layer so it remains importable and testable without FreeCAD installed.
- Export XML deterministically by sorting contact IDs, deliverables, field IDs, question IDs, source IDs, field references, and missing-data row IDs.
- Do not add XML import/parsing in this milestone because the current architecture only has a one-way object-to-intake parser and no project-file loading API yet.
- Add XML import/parsing in `controls_wb.ceproject_xml` beside the exporter so the XML surface remains a pure-Python boundary.
- Return a `CEProjectXmlDocument` wrapper from `parse_ceproject_xml()` instead of changing `ProjectIntake`, because parsed validation findings and missing-data rows are XML document sections rather than editable intake source fields.
- Raise `CEProjectXmlError` for malformed XML, missing required metadata, invalid enum values, invalid booleans, or invalid integers instead of silently dropping unsupported required content.
- Keep the importer scoped to the intake-related XML currently emitted by `ceproject_to_xml()`; future device, signal, circuit, PLC, HMI, or BIM sections remain outside this milestone.

## Validation Commands

Commands run after implementation:

```bash
cd ControlForgeCAD
python -m pytest
python -m compileall controls_wb tests
python3 -m pytest
python3 -m compileall controls_wb tests
```

Commands run for the contact/source/question-response milestone:

```bash
cd ControlForgeCAD
python3 -m pytest
python3 -m compileall controls_wb tests
```

Commands run for the missing-data matrix milestone:

```bash
cd ControlForgeCAD
python3 -m pytest
python3 -m compileall controls_wb tests
```

Commands run for the Phase 2 CEProject XML intake export milestone:

```bash
python3 -m pytest ControlForgeCAD/tests/test_ceproject_xml.py -q
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

Commands run for the Phase 2 CEProject XML intake import/round-trip milestone:

```bash
python3 -m pytest ControlForgeCAD/tests/test_ceproject_xml.py -q
python3 -m compileall ControlForgeCAD/controls_wb
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

## Outcomes & Retrospective

- Added `controls_wb/intake.py` with `FieldStatus`, starter intake fields, selected-deliverable requirements, and validation findings that include an `ask` owner.
- Added `controls_wb/model/project.py` and `controls_wb/commands/new_project.py` so FreeCAD can create a starter `CE_Project` object with CEProject metadata and intake statuses.
- Updated `InitGui.py` to register `CE_NewProject`, keep command IDs under the existing `CE_` prefix, and use the documented workbench label `Controls / Automation`.
- Extended `CE_ValidateProject` pure helper logic to include starter project intake missing-data findings.
- Added focused pytest coverage under `ControlForgeCAD/tests/`.
- Updated `README.md`, `TODO.md`, and `CHANGELOG.md` for the behavior implemented in this milestone.
- `python -m pytest` and `python -m compileall controls_wb tests` failed because `python` is not on PATH in this environment.
- `python3 -m pytest` passed: 6 tests.
- `python3 -m compileall controls_wb tests` passed.
- Added starter `Contact`, `SourceRecord`, `SourceRecordType`, and `IntakeQuestionResponse` pure-Python models.
- `default_project_intake()` now seeds stakeholder contacts, a manual-entry source for the project name, and requested questions for missing starter fields.
- `open_questions_for()` returns unresolved question/response records for intake follow-up workflows.
- `CE_Project` now stores contacts, source records, and intake questions as JSON string-list properties, plus simple response value fields for nominal voltage, phase count, PLC platform, and sensor count.
- `CE_ValidateProject` now parses those JSON string-list properties and warns when verified or approved required fields have no source record.
- `python3 -m pytest` passed: 10 tests. The environment still prints `Failed to create stream fd: Operation not permitted` before pytest output, but tests complete successfully.
- `python3 -m compileall controls_wb tests` passed. The same stream-fd warning appears before compile output.
- Added `controls_wb/missing_data.py` with `MissingDataRow`, `missing_data_matrix()`, and shared CE project object-to-intake parsing.
- Matrix rows report `item_id`, `category`, `question_id`, `fact_id`, label, required flag, value, response/source coverage, verification/approval booleans, status, severity, finding, and next action.
- Matrix statuses currently include `complete`, `missing_response`, `missing_source`, `needs_verification`, and `needs_approval`.
- `CE_Project` now exposes `EnclosureRating` and `EnclosureRatingStatus` properties so object-based intake parsing covers the starter panel-layout requirement.
- `CE_ValidateProject` now reuses the missing-data module's CE project object parser, preserving current validation behavior while avoiding duplicate parsing code.
- CSV export was not added; it is recorded as the next missing-data matrix follow-up in `TODO.md`.
- `python3 -m pytest` passed: 16 tests. The environment still prints `Failed to create stream fd: Operation not permitted` before pytest output, but tests complete successfully.
- `python3 -m compileall controls_wb tests` passed. The same stream-fd warning appears before compile output.
- Added `controls_wb/ceproject_xml.py` with `ceproject_element()` and `ceproject_to_xml()` pure-Python export helpers.
- CEProject XML export now emits `Metadata`, optional `Contacts`, `Intake`, `SourceRecords`, `ValidationFindings`, and `MissingDataMatrix` sections for records supported by the current model.
- The existing `Devices`, `Signals`, and `Connections` schema sections remain optional and unchanged, preserving the existing conveyor demo XML structure.
- XML tests parse the generated output with `xml.etree.ElementTree` and verify stable ordering for deterministic comparisons.
- `python3 -m pytest ControlForgeCAD/tests/test_ceproject_xml.py -q` passed: 5 tests.
- `required_fields_for()` now iterates selected deliverables in sorted order so validation and missing-data output are stable when callers pass a set.
- `python3 -m pytest` passed from the repository root: 21 tests.
- `python3 -m compileall ControlForgeCAD` passed from the repository root.
- Added `CEProjectXmlError`, `CEProjectXmlDocument`, and `parse_ceproject_xml()` in `controls_wb/ceproject_xml.py`.
- CEProject XML import now parses project ID, schema version, metadata name, contacts, deliverables, intake fields, intake question/response records, source records, validation findings, and missing-data matrix rows into pure-Python dataclasses.
- Import failures for malformed XML, missing required elements/attributes, invalid field status values, invalid source record types, invalid booleans, and invalid integers now raise `CEProjectXmlError` with context.
- XML round-trip tests now prove a representative exported intake can be parsed back with equivalent supported project identity, contacts, deliverables, fields, source records, questions, and missing-data source references.
- `python3 -m pytest ControlForgeCAD/tests/test_ceproject_xml.py -q` passed: 13 tests.
- `python3 -m compileall ControlForgeCAD/controls_wb` passed.
- `python3 -m pytest` passed from the repository root: 29 tests.
- `python3 -m compileall ControlForgeCAD` passed from the repository root.

## Final Notes

- The project still has intentional naming drift: product docs say IntegraCAB Open, the current folder/package remains `ControlForgeCAD`/`controls_wb`, and command IDs remain `CE_*`.
- No broad rename was performed because that would be higher risk than the TODO-backed intake MVP increment.
