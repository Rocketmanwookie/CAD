# Intake System Settings Design

## Intent

Replace the intake-settings toolbar placeholder with a local, per-user panel
that records where the proposed local intake database lives and how an intake
form should be delivered. The existing intake form is a local FreeCAD dialog;
the existing database-console command is the staged import/review dialog.

## Goals

- Preserve `CE_IntakeSystemSettings` and all existing/legacy command IDs.
- Persist database and delivery preferences through FreeCAD user parameters,
  not inside a project document.
- Keep the persistence API independent of Qt so it can be regression tested
  without FreeCAD.
- Make the panel explicit about its boundary: it stores delivery preferences;
  it does not send email or synchronize a database.

## Non-goals

- No SQLite schema, database migration, email client automation, or remote
  form delivery is introduced.
- The existing questionnaire and staged import/review behavior is unchanged.

## Approach

Use a focused `controls_wb.intake_settings` module with a value object and
load/save functions backed by `App.ParamGet` under the ControlForgeCAD
preferences path. The command opens a Qt dialog supplied by the same module.
This follows FreeCAD's user-preference convention while avoiding Qt or FreeCAD
imports in the persistence logic.

## Constraints

- Database location and delivery values are user preferences, not CE_Project
  facts, because they configure a workstation's local intake workflow.
- Existing command registrations and IDs remain intact.
- Automated evidence covers default values, normalization, validation, and
  persistence using a ParamGet-compatible fake.
