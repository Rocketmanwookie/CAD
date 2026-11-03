# Acceptance Recovery and Project Workspace Design

## Intent

ControlForgeCAD needs a dependable project workspace before it can be used for
reviewable controls projects.  The user chooses a workspace parent once, then
each new project owns one folder containing its FCStd file, CEProject XML,
imports, exports, and acceptance evidence.  Export commands must use that
project root instead of silently writing to the user's home folder.

The same pass must correct the PLC allocation graph that currently leaves
objects "touched after recompute" in FreeCAD.  The reported desktop evidence
shows the affected objects are PLC channels, signals, modules, and the
allocation rack.

## Goals

- Persist a project-root path on the CE project.
- Create the agreed folder tree once for a new project:

  ```text
  <Project Name>/
    <Project Name>.FCStd
    <Project Name>.ceproject.xml
    imports/cad/vendor/
    imports/cad/customer/
    imports/cad/reference/
    imports/documents/
    imports/data/
    exports/bom/
    exports/io/
    exports/schedules/
    exports/reports/
    exports/package/
    evidence/screenshots/
    evidence/report-view/
    evidence/acceptance/
  ```

- Default the workspace parent to `Documents/ControlForgeCAD Projects`, but
  ask permission/location before first creation and retain that preference.
- Route generated CSV/XML outputs to named subfolders below the project root;
  do not ask where to export each time.
- Use a single directed FreeCAD dependency relation for a PLC channel and its
  typed signal, while retaining reciprocal navigation/validation through the
  stored CE identity.
- Add automated tests that prove directory routing and prevent restoration of
  the dependency cycle.

## Non-goals

- No deletion, relocation, or modification of existing user projects.
- No CAD-file checksum requirement or automatic CAD-download claim.
- No electrical-path endpoint invention: F-04 and F-07 remain deferred until
  a valid endpoint exists.
- No automatic engineering approval, protection sizing, or final part
  selection.
- The larger Siemens power/communications, motor, I/O-wiring, and datasheet
  workflow is intentionally deferred to its own pass.

## Current Evidence and Root-Cause Assessment

The user’s FreeCAD report shows a DAG violation followed by allocation
objects still touched after recompute.  The materialization code creates both
`channel.AllocatedSignalObject -> signal` and
`signal.AllocatedChannelObject -> channel` as `App::PropertyLink` relations.
Those two dependency-forming links are reciprocal and therefore form a cycle.
The fake-document tests preserve object references but have no dependency
graph, which explains why the suite did not detect the desktop failure.

This is the working root-cause hypothesis.  A headless or desktop FreeCAD
regression run remains required to mark it verified; no `FreeCADCmd` executable
was discoverable in the current shell during investigation.

## Approaches Considered

1. **Keep two FreeCAD links and suppress/recompute around the cycle.** Rejected:
   it preserves the invalid dependency graph and risks masking errors.
2. **Keep the channel-to-signal `PropertyLink`; replace the signal-to-channel
   object link with the channel CE identity string.** Chosen: it creates one
   dependency direction, preserves deterministic reciprocal lookup, and keeps
   existing path ownership identities stable.
3. **Change both links to cross-document/specialized link types.** Rejected for
   this pass: it adds FreeCAD-specific persistence behavior without proving
   that it removes the dependency edge.

## Architecture

`controls_wb.project_workspace` will be a Qt-free application service: it
validates a project name, creates the fixed tree idempotently, assigns stable
artifact paths, and resolves export destinations.  FreeCAD commands and GUI
dialogs call it; they do not encode filesystem policy.  A CE project stores
the selected root and may be reopened without prompting.

The electrical graph keeps `AllocatedSignalObject` as the only object link
between an allocation channel and signal.  The signal stores
`AllocatedChannelIdentity` as a string.  Validation resolves that identity
against document objects and reports a missing/wrong/stale identity clearly.

## Acceptance and Review Focus

- A path outside the configured project root must be rejected rather than
  creating output in an arbitrary location.
- An existing project tree must be idempotent and never overwrite a saved
  FCStd/XML artifact.
- Project names that are empty or contain a path separator must be rejected.
- A missing, duplicated, or role-mismatched allocated-channel identity must
  fail graph validation.
- A representative allocation must recompute with no DAG/touched-object error
  in actual FreeCAD before F-03/F-05/F-06 are advanced from failed/blocked.

## Verified / Unverified Boundary

The current Python regression suite verifies data-model behavior only.  The
FreeCAD DAG diagnosis is strongly supported by the report and source graph but
remains **unverified in a repeatable live-FreeCAD command** until an executable
or desktop capture can run the regression.  Generated schedules without a
real electrical path remain valid empty artifacts, not evidence of a completed
wiring path.
