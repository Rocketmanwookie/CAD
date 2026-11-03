# ControlForgeCAD working-progress handoff — 2026-11-02

## Current branch and committed implementation

Active branch: `codex/phase0-contributor-governance`.

- `cc4f3ad` reconciled `codex/controlForgeCAD` into the active branch.
- `8b4551c` added the project-workspace foundation and its tests.
- `d1398c0` added project-root persistence, export routing, the one-way PLC
  allocation graph, desktop acceptance instructions, and a live-FreeCAD test
  that skips precisely when FreeCAD is unavailable to the test interpreter.
- `3dae8f0` keeps an existing project workspace usable after a display-name
  change.

## Verified state

- Full Python suite: `306 passed, 1 skipped`.
- Python compilation: passed.
- The skipped test is `test_freecad_allocation_recompute.py`, because the
  FreeCAD Python module/executable is not available to the shell test runner.
- The allocation graph stores the reverse channel relationship as a CE identity
  rather than a reciprocal FreeCAD `PropertyLink`; this is the source-level
  correction for the reported DAG/recompute failure.

## Manual next action

Restart FreeCAD, create a new blank document, select **Controls / Automation**,
then run **New Controls Project**. After the intake form, the current workbench
must prompt for the project workspace parent. Confirm that it creates the
project folder and its `imports/`, `exports/`, and `evidence/` folders.

Then run F-01 through F-10 in the acceptance workbook. F-03, F-05, and F-06
remain unverified until a live FreeCAD run captures a clean Report View after
allocation and save/reopen/recompute. F-04/F-07 are legitimately `DEFERRED`
until a physical endpoint exists.

## Acceptance workbook

`20261102_ControlForgeCAD_Acceptance_and_Reconciliation_Worksheet.ipynb`
contains operator directions plus F-01 through F-10 controls. Each check has a
status dropdown (`NOT RUN`, `PASS`, `FAIL`, `BLOCKED`, `DEFERRED`), a notes
area, and an evidence-path field. The final ledger cell collects the selections.

Run the notebook with:

```bash
cd /home/egrantjr/Documents/Repositories/controlforgecad
/home/egrantjr/.local/bin/jupyter-notebook
```

The system Jupyter Notebook 6.4.13 was incompatible with the installed Tornado
version. A working Notebook 7.6.4 plus `ipywidgets` is installed in the
user-level pipx environment. Use the server URL/port printed by that command.

## Deliberately not committed

- `tmp/` remains untracked and untouched.
