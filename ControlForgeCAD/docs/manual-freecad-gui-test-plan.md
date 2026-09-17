# Manual FreeCAD GUI Acceptance Checklist

Use this checklist when a FreeCAD desktop test is convenient. It is an
acceptance record, not a blocker for dependency-free development work.

## Setup

1. Close FreeCAD and link the committed checkout into the Flatpak user Mod
   directory:

   ```bash
   python3 scripts/link_freecad_workbench.py \
     --source /home/egrantjr/Documents/Repositories/controlforgecad/ControlForgeCAD \
     --mod-dir ~/.var/app/org.freecad.FreeCAD/data/FreeCAD/v1-1/Mod
   ```

   Expected: the command reports a `ControlForgeCAD` symlink. Rerunning it is
   safe. If a target points elsewhere, stop and record the setup failure rather
   than replacing it.

2. Start Flatpak FreeCAD, select **Controls / Automation**, and confirm the
   Controls Project, Layout, Validation, and Exports groups load without a
   traceback. Confirm **Capture Wire Route from Geometry** is present.

## Route-capture workflow

1. Create a new document, run **New Controls Project**, and enter a minimally
   valid intake.
2. Run **Create Control Panel**, then **Add Electrical Path**. Create a path
   through a registered PLC, terminal strip, and field device.
3. Create a visible Part or Draft polyline with vertices `(0,0,0)`,
   `(100,0,0)`, and `(100,50,0)` mm.
4. Select exactly one resulting `CE_Wire` and that polyline, then run
   **Capture Wire Route from Geometry**.

Expected results:

- Report View confirms three captured points and a `150.0 mm` calculated
  length.
- The wire’s `RoutePoints` contains three ordered points; `CalculatedLength`
  is `150.0 mm`.
- The fallback polyline updates visibly.
- The wire CE identity and its endpoint identities do not change.
- **Export Electrical Schedules** exports the routed length in
  `~/integracad_wiring_schedule.csv`; the I/O path export reflects the updated
  aggregate path length.
- After save, close, reopen, and re-export, the identity, route, length, and
  visible fallback remain unchanged.
- **Validate Controls Project** reports no typed-link, owner, or continuity
  errors for the path.

## Guard cases

- Geometry but no CE wire selected: warning; no mutation.
- Two CE wires selected: warning; neither mutates.
- One CE wire plus one vertex only: warning; route and length do not change.
- Two joined geometry segments sharing a vertex: stored route has three points,
  not four.
- Undo after capture restores the prior route and length; redo restores them.

Record the exact FreeCAD/Flatpak version, the Git commit, screenshots of the
command and resulting polyline, Report View output, exported CSVs, and any
traceback.
