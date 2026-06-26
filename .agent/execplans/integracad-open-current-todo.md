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
  - `CE_CreatePanel`
  - `CE_ExportBOM`
  - `CE_ValidateProject`
- Existing commands:
  - `create_panel.py` creates a parametric backplate placeholder named `CE_Backplate`.
  - `export_bom.py` collects object attributes `Tag`, `Description`, `Manufacturer`, and `PartNumber` into CSV rows.
  - `validate_project.py` checks duplicate tags and missing description/part number for tagged objects.
- Existing model code:
  - `controls_wb/model/panel.py` defines a FreeCAD FeaturePython control panel/backplate placeholder.
- Existing TODO items:
  - The master TODO is `ControlForgeCAD/TODO.md`.
  - It calls for identity cleanup toward IntegraCAB Open, but the repository still intentionally lives under `ControlForgeCAD/`.
  - Phase 1 prioritizes structured project intake, contacts/stakeholder model, question/response model, missing-data matrix, field status model, source record model, templates, and validation output telling who to ask for missing information.
  - Phase 2 prioritizes CEProject data model sections, schema versioning, ID-addressable facts, generated-artifact traceability, and assumptions/estimates.
  - Phase 6 later covers PLC/I/O and signal registry work.
- Existing tests:
  - `pyproject.toml` configures `pytest` with `testpaths = ["tests"]`, but no `tests/` directory currently exists.
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

## Milestones

1. Document current state and naming decisions in this ExecPlan.
2. Add a minimal CEProject/intake data model in importable pure-Python modules.
3. Add a FreeCAD command that creates an initial controls project/intake object.
4. Extend validation to report missing intake fields and who to ask next where practical.
5. Add focused pure-Python tests for intake validation, existing BOM collection, and existing tag validation.
6. Update README and TODO to reflect completed behavior only.
7. Run validation commands and record results.

## Progress

- [x] Inspected repository branch and confirmed `controlforgecad`.
- [x] Confirmed initial working tree was clean.
- [x] Read required repository files where present: root README, workbench README, TODO, roadmap, package metadata, FreeCAD init files, schema, example, and command/model modules.
- [x] Created this ExecPlan at `.agent/execplans/integracad-open-current-todo.md`.
- [x] Implement intake/project milestone.
- [x] Add or update tests.
- [x] Update docs/TODO.
- [x] Run validation.

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

## Validation Commands

Commands run after implementation:

```bash
cd ControlForgeCAD
python -m pytest
python -m compileall controls_wb tests
python3 -m pytest
python3 -m compileall controls_wb tests
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

## Final Notes

- The project still has intentional naming drift: product docs say IntegraCAB Open, the current folder/package remains `ControlForgeCAD`/`controls_wb`, and command IDs remain `CE_*`.
- No broad rename was performed because that would be higher risk than the TODO-backed intake MVP increment.
