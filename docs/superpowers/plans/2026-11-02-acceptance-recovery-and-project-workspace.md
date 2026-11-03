# Acceptance Recovery and Project Workspace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the PLC allocation dependency cycle and create a single,
persisted project folder that owns all ControlForgeCAD artifacts.

**Architecture:** A Qt-free workspace service owns names, fixed directories,
and output destinations.  New-project and export commands delegate to it.  The
PLC allocation graph retains its directed channel-to-signal link while its
reverse relationship becomes an identity value resolved by validation.

**Tech Stack:** Python 3.10+, FreeCAD document properties/Qt, pathlib, pytest.

**Spec:** `docs/superpowers/specs/2026-11-02-acceptance-recovery-and-project-workspace-design.md`

## Global Constraints

- Never overwrite, delete, or move an existing project artifact.
- Ask for the workspace parent once; default to Documents/ControlForgeCAD Projects.
- All generated outputs stay under the persisted project root.
- F-04 and F-07 are deferred when no physical endpoint exists.
- A hardware/protection recommendation remains review-only unless separately approved.

## Review Focus

- Test malformed project names and project roots outside the selected parent.
- Test an existing project’s root and artifacts remain unchanged on rerun.
- Test every exporter’s route is under its specified category directory.
- Test duplicate or role-invalid reverse allocation identities are findings.
- Execute a live FreeCAD recompute test before claiming the DAG failure fixed.

---

### Task 1: Add a project-workspace domain service

**Files:**
- Create: `ControlForgeCAD/controls_wb/project_workspace.py`
- Create: `ControlForgeCAD/tests/test_project_workspace.py`

**Interfaces:**
- Produces: `ProjectWorkspace`, `create_project_workspace(parent, project_name)`,
  `workspace_artifact_path(workspace, artifact)`, and `export_path(workspace, category, filename)`.
- Consumes: `pathlib.Path`, a project name, and a fixed artifact/category map.

- [ ] **Step 1: Write failing tests** for name validation, exact directory tree,
  idempotent creation, rejection of a path separator, and category-bound
  export paths.
- [ ] **Step 2: Run** `pytest -q ControlForgeCAD/tests/test_project_workspace.py`
  **and confirm it fails because the workspace service is absent.**
- [ ] **Step 3: Implement** the immutable `ProjectWorkspace` value object and
  filesystem service without FreeCAD/Qt imports.
- [ ] **Step 4: Run** the focused test target and confirm it passes.
- [ ] **Step 5: Commit** the workspace service and focused tests.

### Task 2: Persist and initialize the project root

**Files:**
- Modify: `ControlForgeCAD/controls_wb/model/project.py`
- Modify: `ControlForgeCAD/controls_wb/commands/new_project.py`
- Modify: `ControlForgeCAD/controls_wb/gui/project_intake.py`
- Modify: `ControlForgeCAD/tests/test_project_model.py`
- Modify: `ControlForgeCAD/tests/test_project_commands.py`

**Interfaces:**
- Consumes: `ProjectWorkspace`, `create_project_workspace`, and persisted
  `WorkspaceParent` / `ProjectRoot` CE project properties.
- Produces: a new project whose root is created only after dialog confirmation.

- [ ] **Step 1: Write failing tests** for the two persisted properties and a
  command boundary that calls workspace creation only after a confirmed intake.
- [ ] **Step 2: Run** those focused tests and confirm they fail because the
  properties/call are absent.
- [ ] **Step 3: Implement** persisted project-root properties, parent-directory
  preference access, and the confirmed GUI flow.  Save the FCStd only when the
  document has a root and FreeCAD supplies a save API.
- [ ] **Step 4: Run** focused tests, then `pytest -q` from `ControlForgeCAD`.
- [ ] **Step 5: Commit** the project-root integration.

### Task 3: Route exports and imports through the root

**Files:**
- Modify: `ControlForgeCAD/controls_wb/commands/export_bom.py`
- Modify: `ControlForgeCAD/controls_wb/commands/export_ceproject_xml.py`
- Modify: `ControlForgeCAD/controls_wb/commands/export_io_list.py`
- Modify: `ControlForgeCAD/controls_wb/commands/export_missing_data_csv.py`
- Modify: `ControlForgeCAD/controls_wb/commands/export_connection_schedule.py`
- Modify: `ControlForgeCAD/controls_wb/commands/export_electrical_schedules.py`
- Modify: `ControlForgeCAD/controls_wb/commands/export_terminal_plan.py`
- Modify: `ControlForgeCAD/controls_wb/gui/project_intake.py`
- Test: existing export command tests plus `ControlForgeCAD/tests/test_project_workspace.py`

**Interfaces:**
- Consumes: `export_path(workspace, category, filename)` and a project root.
- Produces: categorized output under `exports/` and import dialogs initially
  located at the matching `imports/` folder.

- [ ] **Step 1: Write failing command-helper tests** that each destination is
  inside the project root and retains its expected filename/category.
- [ ] **Step 2: Run** those targets and confirm they fail because commands use
  `Path.home()`.
- [ ] **Step 3: Implement** shared destination lookup and change each command
  to use it; warn and stop clearly when no project root is configured.
- [ ] **Step 4: Run** focused export tests, then the complete suite.
- [ ] **Step 5: Commit** output routing.

### Task 4: Break the PLC allocation dependency cycle

**Files:**
- Modify: `ControlForgeCAD/controls_wb/model/layout.py`
- Modify: `ControlForgeCAD/controls_wb/model/electrical.py`
- Modify: `ControlForgeCAD/tests/test_layout_objects.py`
- Modify: `ControlForgeCAD/tests/test_electrical_objects.py`
- Create: `ControlForgeCAD/tests/test_freecad_allocation_recompute.py`

**Interfaces:**
- Replaces: `signal.AllocatedChannelObject: App::PropertyLink`.
- Produces: `signal.AllocatedChannelIdentity: App::PropertyString` and a
  `resolve_allocated_channel(document, signal)` helper that returns exactly
  one `PLC_CHANNEL` or `None`/a validation finding.

- [ ] **Step 1: Write failing tests** asserting that materialized signals use
  an identity rather than a reverse object link and that reciprocal validation
  finds a channel by identity.
- [ ] **Step 2: Run** the focused targets and confirm they fail against the
  existing bidirectional links.
- [ ] **Step 3: Implement** the one-direction relationship and migrate all
  consumers/pruning/move logic to the resolver.
- [ ] **Step 4: Add and run** an actual-FreeCAD regression test that creates a
  project with allocated I/O, recomputes, and asserts no recompute failure.
  Mark the test skipped with a precise reason only when FreeCAD is unavailable.
- [ ] **Step 5: Run** focused tests and the whole suite; perform a desktop
  FreeCAD rerun for F-03/F-05/F-06 evidence.
- [ ] **Step 6: Commit** the cycle fix only after the live recompute test
  passes, or report the exact remaining environmental block.

### Task 5: Update the acceptance record and project documentation

**Files:**
- Modify: `ControlForgeCAD/CHANGELOG.md`
- Modify: `docs/MANUAL_FREECAD_ACCEPTANCE_HANDOFF.md`
- Modify: `docs/AGENT_OPERATIONS_LEDGER.md`
- Modify: `20261102_ControlForgeCAD_Acceptance_and_Reconciliation_Worksheet.ipynb` only with user confirmation if its current untracked version is to be replaced.

**Interfaces:**
- Consumes: test results and desktop evidence.
- Produces: explicit PASS/FAIL/BLOCKED/DEFERRED status with evidence paths.

- [ ] **Step 1: Record** the FreeCAD recompute result and workspace-root
  behavior without marking F-04/F-07 as failed when endpoints do not exist.
- [ ] **Step 2: Update** the changelog and ledger with verified versus
  unverified boundaries.
- [ ] **Step 3: Run** the relevant tests/document checks and commit only the
  tracked documentation.

## Self-Review

Coverage: this plan implements the two selected pass goals and deliberately
leaves Siemens power/communication configuration, I/O wiring metadata, motor
intake, datasheet extraction, and workflow-menu consolidation to later plans.
Each requirement in the selected design maps to Tasks 1–5.  Task 4 owns the
DAG and live-FreeCAD risk; Tasks 1–3 own paths, safety, and export routing;
Task 5 owns evidence status.  No artifact is overwritten by design.
