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

Current milestone: add a repeatable FreeCAD workbench smoke-test and manual install/link workflow. The work should verify `Init.py` and `InitGui.py` remain import-safe outside FreeCAD, command registration metadata stays stable, and developers have exact steps for linking or copying the workbench into FreeCAD's user `Mod` directory.

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
- [x] Add FreeCAD-facing missing-data preview command wired to `controls_wb.missing_data`.
- [x] Add FreeCAD-facing CEProject XML export command wired to `controls_wb.ceproject_xml`.
- [x] Keep `InitGui.py` as command registration and workbench UI grouping only.
- [x] Add pure-Python command-adjacent tests for project-object discovery, missing-data formatting, and XML export selection.
- [x] Re-checked requested guidance files for this milestone; `AGENTS.md` and `.agent/PLANS.md` remain absent in this checkout.
- [x] Add import-safe command metadata shared by `InitGui.py` and tests.
- [x] Add pure-Python smoke tests for command IDs, menu text, command module imports without FreeCAD, and `Init.py`/`InitGui.py` import without FreeCAD.
- [x] Add `scripts/link_freecad_workbench.py` for creating a FreeCAD user `Mod/ControlForgeCAD` development symlink.
- [x] Add tests for the FreeCAD `Mod` symlink helper.
- [x] Document exact symlink, copy, launch, command-confirmation, and manual smoke validation steps in README files.
- [x] Fix manual FreeCAD GUI smoke-test workbench load failure caused by `InitGui.py` using `__file__` when FreeCAD did not define it.
- [x] Add pure-Python coverage for resolving the workbench root without `__file__` and initializing `InitGui.py` with fake FreeCAD modules.
- [x] Milestone 1: add a real editable `CE_Project` FreeCAD document object contract for starter intake data.
- [x] Add pure-Python tests for CE_Project property specs, payload mapping, fake object initialization, proxy persistence hooks, and create-or-update behavior.
- [x] Update manual FreeCAD validation steps for model-tree creation, editable properties, and `.FCStd` save/reopen confirmation.
- [x] Milestone 2: synchronize editable CE_Project document-object properties into backend intake payloads.
- [x] Add fake document-object tests proving edited Property View values feed validation and missing-data logic.
- [x] Update manual FreeCAD validation steps for editing a property and rerunning validation/missing-data.
- [x] Milestone 3: add a New Project / Intake dialog workflow with pure-Python form mapping helpers.
- [x] Wire `CE_NewProject` to open the dialog when Qt/PySide is available and create a starter object as a safe fallback when it is not.
- [x] Add tests for form value normalization, deliverable parsing, fake-object application, and create/update from form payloads.
- [x] Milestone 4: add starter I/O list model and deterministic CSV export.
- [x] Expose `CE_ExportIOList` in workbench export command registration.
- [x] Add tests for I/O CSV headers/rows, missing sensor-count handling, unmapped findings, and fake document-object extraction.
- [x] Add `CE_AddIOSignal` dialog workflow for selectable I/O type, user label, and deterministic auto tag/address generation.
- [x] Store explicit I/O signals on `CE_Project` as JSON-line records and include them in I/O CSV export before remaining sensor-count placeholders.
- [x] Extend the Project Intake dialog with Siemens/Allen-Bradley make selection, contingent PLC line dropdowns, DI/DO/AI/AO counts, and optional modular I/O accessories.
- [x] Replace separate voltage/phase text fields with a combined phase/voltage dropdown, enclosure rating checkboxes, communication protocol checkboxes, PLC CPU selection, compatible Ethernet/power dropdowns, and an I/O expansion planning popup.
- [x] Add Project Intake setup source metadata and attach one source record to filled starter setup facts.
- [ ] Add a project setup/import workflow from structured definition files such as CEProject XML, YAML, and UML-derived interchange where practical.
- [x] Milestone 5: add starter CAD-side controls layout placeholder objects.
- [x] Wire `CE_CreatePanel` to create panel/backplate, DIN rail, wire duct, terminal strip, and PLC rack/module placeholders.
- [x] Add tests for layout metadata, fake FreeCAD object creation, proxy persistence hooks, and BOM extraction from starter layout objects.

## Surprises & Discoveries

- `AGENTS.md` and `.agent/PLANS.md` are absent, so no local repo-specific agent guidance could be applied beyond the user's instructions.
- The repository has no current tests even though pytest is configured.
- The root README is not the product README; the useful README is under `ControlForgeCAD/`.
- The TODO asks for eventual identity/package renames, but the README explicitly notes the seed still lives under `ControlForgeCAD/`.
- Manual FreeCAD GUI smoke testing found a workbench load failure: `name '__file__' is not defined` at `ControlForgeCAD/InitGui.py:28`.

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
- Add `CE_PreviewMissingData` and `CE_ExportCEProjectXML` as new `CE_` command IDs instead of renaming existing commands.
- Share project-object discovery between the missing-data and XML export commands so command modules call backend helpers rather than duplicating intake parsing.
- Export CEProject XML from the first controls project intake object in the active FreeCAD document for this milestone; multi-project selection/export can be added later when there is a clearer document workflow.
- Keep command registration lists in `controls_wb.commands.metadata` so pure-Python tests can detect accidental command ID/menu text drift without importing real `FreeCADGui`.
- Add a Python symlink helper instead of shell-only documentation so the workflow is testable and can accept an alternate `--mod-dir` for non-default FreeCAD profiles.
- Treat FreeCAD CLI smoke as not feasible in this environment: `/snap/bin/freecad` is present, but no `freecadcmd`/`FreeCADCmd` command exists and `freecad --help` only emits GUI/module messages without usable headless help output.
- Keep `InitGui.py` thin by moving FreeCAD bootstrap path resolution into `controls_wb.freecad_paths`.
- Resolve the workbench root by trying `globals()["__file__"]`, then `globals()["__spec__"].origin`, then the imported `controls_wb` package path.
- Treat filled editable document-object values with `Unknown` or `Requested` starter statuses as `Received` when converting to backend intake data. This keeps Property View edits useful without forcing the user to update status fields manually.
- Store `Customer` and `SiteLocation` as editable `CE_Project` properties now, but do not mark them as required deliverable facts yet because the current backend required-field matrix does not use them.
- Keep Milestone 4 I/O generation intentionally simple: Project setup creates addressed starter DI/DO/AI/AO rows from counts; detailed rack/module/channel assignment and module capacity matching remain later Phase 6 work.
- Use the current I/O expansion popup as a starter planning aid: it subtracts onboard CPU I/O, targets requested I/O times 1.2 for 20 percent spare capacity, and suggests the nearest starter module count from a small internal catalog. Vendor part numbers and procurement suitability still need verification against official catalogs.
- Defer amperage calculation until load assumptions and power-drop modeling exist; track it under Phase 3.
- Add explicit I/O signal rows as the first labeling workflow: digital input/output, analog input/output, and relay rows receive deterministic generated tags and addresses, while rack/slot/channel assignment remains later work.
- Capture one setup source record during Project Intake submission so filled starter facts are source-backed instead of reported as `missing_source`; verification and approval remain separate lifecycle steps.
- Treat project setup as both GUI-driven and file-driven. CEProject XML is the canonical internal format, while YAML and UML-derived interchange can be supported as adapter inputs when they map cleanly to the same `CE_Project` object fields.
- Keep Milestone 5 geometry as simple boxes with editable metadata. Manufacturer-accurate models, assembly constraints, routing, wire schedules, and detailed panel layout remain future work.

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

Commands run for the FreeCAD command integration milestone:

```bash
python3 -m pytest ControlForgeCAD/tests/test_project_commands.py -q
python3 -m compileall ControlForgeCAD/controls_wb/commands ControlForgeCAD/InitGui.py
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

Commands run for the FreeCAD workbench smoke-test and install/link workflow milestone:

```bash
python3 -m pytest ControlForgeCAD/tests/test_command_metadata.py ControlForgeCAD/tests/test_freecad_link_script.py -q
python3 -m compileall ControlForgeCAD/Init.py ControlForgeCAD/InitGui.py ControlForgeCAD/controls_wb/commands scripts/link_freecad_workbench.py
freecad --version
command -v freecadcmd || command -v FreeCADCmd || command -v freecad
freecad --help
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

Commands run for the FreeCAD GUI `__file__` load-failure fix:

```bash
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

Commands run for Milestone 1 - real FreeCAD CE_Project document object:

```bash
python3 -m pytest ControlForgeCAD/tests/test_project_model.py -q
python3 -m compileall ControlForgeCAD/controls_wb/model/project.py ControlForgeCAD/controls_wb/commands/new_project.py
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

Commands run for Milestone 2 - editable intake property synchronization:

```bash
python3 -m pytest ControlForgeCAD/tests/test_missing_data.py ControlForgeCAD/tests/test_validate_project.py -q
python3 -m compileall ControlForgeCAD/controls_wb/missing_data.py ControlForgeCAD/tests/test_missing_data.py ControlForgeCAD/tests/test_validate_project.py
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

Commands run for Milestone 3 - New Project / Intake GUI task panel:

```bash
python3 -m pytest ControlForgeCAD/tests/test_project_intake_gui.py ControlForgeCAD/tests/test_command_metadata.py -q
python3 -m compileall ControlForgeCAD/controls_wb/gui ControlForgeCAD/controls_wb/commands/new_project.py ControlForgeCAD/tests/test_project_intake_gui.py
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

Commands run for Milestone 4 - I/O list model and CSV export:

```bash
python3 -m pytest ControlForgeCAD/tests/test_io_list.py ControlForgeCAD/tests/test_command_metadata.py -q
python3 -m compileall ControlForgeCAD/controls_wb/io_list.py ControlForgeCAD/controls_wb/commands/export_io_list.py ControlForgeCAD/InitGui.py ControlForgeCAD/tests/test_io_list.py
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

Commands run for Milestone 5 - starter controls layout objects:

```bash
python3 -m pytest ControlForgeCAD/tests/test_layout_objects.py ControlForgeCAD/tests/test_bom.py -q
python3 -m compileall ControlForgeCAD/controls_wb/model/layout.py ControlForgeCAD/controls_wb/commands/create_panel.py ControlForgeCAD/tests/test_layout_objects.py
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

FreeCAD CLI smoke feasibility result:

```text
`freecad --version` and `freecad --help` both return exit code 0, but the snap emits mount/Gtk messages and does not provide useful headless CLI/version/help output in this sandbox. `freecadcmd` and `FreeCADCmd` are not present; only `/snap/bin/freecad` is found. Automated FreeCAD GUI/workbench loading remains a documented manual validation step for this milestone.
```

Manual FreeCAD validation steps for this milestone:

```text
1. Symlink or copy /home/egrantjr/Dev/CAD/ControlForgeCAD into the FreeCAD user Mod directory.
2. Restart FreeCAD.
3. Select the Controls / Automation workbench.
4. Confirm New Controls Project, Validate Controls Project, Preview Missing Data, Export BOM, and Export CEProject XML appear in the workbench UI.
5. Run New Controls Project and confirm the Project Intake dialog opens.
6. Enter or edit project name, customer, site/location, deliverables, nominal voltage, phase count, enclosure rating, PLC make, PLC line, DI/DO/AI/AO counts, optional I/O accessories, and source metadata, then submit the dialog.
7. Confirm a CE_Project object appears in the model tree and Report View says the project intake was updated. If Qt/PySide cannot load, confirm the fallback warning appears and a starter CE_Project is still created.
8. Select CE_Project and confirm editable CEProject and Intake properties appear in the Property View matching the submitted dialog values.
9. Edit a basic property, save the document as .FCStd, close it, reopen it, and confirm the property value is retained.
10. Clear all input counts, run Preview Missing Data, and confirm io.sensorCount is reported as missing.
11. Fill DI or AI count, rerun Preview Missing Data, and confirm the value is shown as a response rather than missing.
12. Run Validate Controls Project and confirm validation reads the edited object values.
13. Run Create Control Panel and confirm CE_Backplate, CE_DIN_Rail, CE_Wire_Duct, CE_Terminal_Strip, and CE_PLC_Rack appear in the model tree with editable controls metadata.
14. Run Validate Controls Project and confirm validation reads the project and starter layout metadata.
15. Run Export BOM and confirm ~/controlforgecad_bom.csv includes starter layout objects with tag/description/manufacturer/part-number data where assigned.
16. Run Export CEProject XML and confirm ~/integracab_ceproject.xml is written.
17. Run Add I/O Signal, choose a type, enter a label, and confirm Report View prints the generated tag and address.
18. Run Export I/O List and confirm ~/integracab_io_list.csv is written from explicit I/O rows plus remaining starter intake data. If rack/slot/channel data is not assigned yet, confirm Report View prints a concise unmapped I/O summary.
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
- Added `controls_wb/commands/missing_data.py` with `CE_PreviewMissingData`, pure-Python project-object discovery, row generation, and console line formatting.
- Added `controls_wb/commands/export_ceproject_xml.py` with `CE_ExportCEProjectXML` and a pure-Python helper that exports the first controls project intake object through `ceproject_to_xml()`.
- Updated `InitGui.py` to import/register the new command modules and group validation commands separately from export commands.
- Added `tests/test_project_commands.py` for command-adjacent pure-Python behavior.
- `python3 -m pytest ControlForgeCAD/tests/test_project_commands.py -q` passed: 5 tests.
- `python3 -m compileall ControlForgeCAD/controls_wb/commands ControlForgeCAD/InitGui.py` passed.
- `python3 -m pytest` passed from the repository root: 34 tests.
- `python3 -m compileall ControlForgeCAD` passed from the repository root.
- Added `controls_wb/commands/metadata.py` with stable command IDs, menu text, module names, and workbench command group tuples.
- Updated `InitGui.py` to consume the metadata tuples while keeping GUI-dependent command registration in `Initialize()`.
- Added `scripts/link_freecad_workbench.py`; it creates `~/.local/share/FreeCAD/Mod/ControlForgeCAD` as a symlink to the checkout, supports `--source` and `--mod-dir`, is idempotent for an existing matching symlink, and refuses conflicting existing paths.
- Added smoke tests for command metadata, import-safe command modules, `Init.py`, `InitGui.py`, and the symlink helper.
- Updated root and workbench READMEs with exact symlink/copy commands, helper-script usage, workbench launch steps, expected command IDs/menu text, and manual FreeCAD smoke steps.
- Updated `TODO.md` and `CHANGELOG.md` for the completed smoke-test/install workflow.
- `python3 -m pytest ControlForgeCAD/tests/test_command_metadata.py ControlForgeCAD/tests/test_freecad_link_script.py -q` passed: 8 tests.
- `python3 -m compileall ControlForgeCAD/Init.py ControlForgeCAD/InitGui.py ControlForgeCAD/controls_wb/commands scripts/link_freecad_workbench.py` passed.
- `python3 -m pytest` passed from the repository root: 43 tests.
- `python3 -m compileall ControlForgeCAD` passed from the repository root.
- Removed generated `__pycache__` directories after validation.
- The FreeCAD snap binary was probed for CLI feasibility, but the workbench was not loaded in a GUI session in this environment; manual validation steps are documented above and in `README.md`.
- Milestone 1 completed: `controls_wb.model.project` now defines an explicit editable property set for the `CE_Project` object, initializes fake and real FreeCAD-like objects through shared helpers, and gives the proxy simple persistent state hooks for FreeCAD save/reopen.
- `CE_NewProject` now creates or refreshes the active document's `CE_Project` object via `create_or_update_project()`.
- Milestone 1 validation passed: `python3 -m pytest` passed 50 tests; `python3 -m compileall ControlForgeCAD` passed.
- Milestone 2 completed: `project_object_to_intake()` now converts edited `CE_Project` values into backend `ProjectIntake` fields, including project customer/site properties and received-status inference for filled starter fields.
- Validation and missing-data helpers now operate on edited document-backed data; blank required properties still report as missing, while filled values are recognized as responses.
- Milestone 3 completed: `controls_wb.gui.project_intake` provides pure-Python form mapping helpers plus a lazy Qt dialog for editing starter intake fields.
- `CE_NewProject` now opens the Project Intake dialog when possible and prints a fallback warning while creating the starter object if Qt/PySide is unavailable.
- Milestone 4 completed: `controls_wb.io_list` defines `IOSignal`, deterministic CSV export, starter signal generation from project DI/DO/AI/AO counts, explicit user-labeled I/O rows, and clear missing/unmapped I/O summaries.
- `CE_ExportIOList` is registered with the workbench export commands and writes `~/integracab_io_list.csv`.
- Milestone 5 completed: `controls_wb.model.layout` defines starter layout object specs and FreeCAD-like object creation helpers for the required placeholder types.
- `CE_CreatePanel` now creates the starter layout set, and existing BOM export includes those objects through their controls metadata.

## Final Notes

- The project still has intentional naming drift: product docs say IntegraCAB Open, the current folder/package remains `ControlForgeCAD`/`controls_wb`, and command IDs remain `CE_*`.
- No broad rename was performed because that would be higher risk than the TODO-backed intake MVP increment.
