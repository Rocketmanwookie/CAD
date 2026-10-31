# Intake System Settings Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the intake settings command into a persisted FreeCAD preferences panel.

**Architecture:** A Qt-free settings module owns defaults, validation, and FreeCAD parameter persistence. The existing workflow command delegates panel display to that module, retaining its registered ID and resource metadata.

**Tech Stack:** Python 3.10+, FreeCAD ParamGet, Qt widgets, pytest.

**Spec:** `docs/superpowers/specs/2026-10-24-intake-system-settings-design.md`

## Global Constraints

- Do not add a database implementation, mail sender, or remote delivery integration.
- Keep existing command IDs and questionnaire/import behavior unchanged.
- Persist only per-user preferences through FreeCAD parameters.

## Review Focus

- Empty database locations must be rejected before any preference is changed.
- Unknown delivery methods must be rejected rather than persisted.
- A save/load round trip must preserve all user-entered settings.
- Loading an untouched preference group must return safe local defaults.
- The panel must state that delivery preferences do not send mail.

### Task 1: Settings persistence boundary

**Files:**
- Create: `ControlForgeCAD/controls_wb/intake_settings.py`
- Create: `ControlForgeCAD/tests/test_intake_settings.py`

**Interfaces:**
- Produces: `IntakeSystemSettings`, `load_intake_settings(app=None)`, and `save_intake_settings(settings, app=None)`.

- [ ] **Step 1: Write failing persistence tests** for defaults, validation, and a fake-ParamGet save/load round trip.
- [ ] **Step 2: Run** `pytest -q tests/test_intake_settings.py` **and confirm it fails because the module is absent.**
- [ ] **Step 3: Implement** the Qt-free value object, validation, and ParamGet persistence boundary.
- [ ] **Step 4: Run** `pytest -q tests/test_intake_settings.py` **and confirm it passes.**

### Task 2: Panel, command integration, and evidence

**Files:**
- Modify: `ControlForgeCAD/controls_wb/intake_settings.py`
- Modify: `ControlForgeCAD/controls_wb/commands/workflow.py`
- Modify: `docs/WORKFLOW_MILESTONES.md`

**Interfaces:**
- Consumes: `load_intake_settings`, `save_intake_settings`.
- Produces: `show_intake_system_settings(parent=None)`.

- [ ] **Step 1: Add a failing command-level test** that proves activating the settings command delegates to the panel.
- [ ] **Step 2: Run** its focused pytest target **and confirm it fails because activation remains a placeholder.**
- [ ] **Step 3: Implement** a form with database location and delivery controls, a save path, and the delivery boundary copy; replace the placeholder activation.
- [ ] **Step 4: Update** active milestone evidence to describe actual stored preferences and the unimplemented delivery/database boundaries.
- [ ] **Step 5: Run** focused tests and then `pytest -q` from `ControlForgeCAD`.
