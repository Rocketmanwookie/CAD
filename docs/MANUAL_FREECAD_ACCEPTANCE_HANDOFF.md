# Manual FreeCAD acceptance handoff

Use this handoff with the current `controlforgecad` head after the workbench is
linked into a real FreeCAD desktop. Follow
[`ControlForgeCAD/docs/manual-freecad-gui-test-plan.md`](../ControlForgeCAD/docs/manual-freecad-gui-test-plan.md)
and attach its acceptance-record template to the resulting issue or handoff.

Required workflow: create one project, allocate catalog I/O, create a path from
an allocated channel, save/reopen/recompute, verify identities and links, edit
the allocation-backed path and confirm its first PLC terminal cannot change
away from the allocated address, validate, and export schedules. Route capture
may be exercised separately, but does not prove that address invariant. Include
the saved FCStd and generated CSVs as evidence.

For the current acceptance-recovery candidate, first confirm the project-root
prompt appears only for a new project without `ProjectRoot`, then confirm that
the saved FCStd, CEProject XML, and CSV artifacts are created under that root.
Re-run the allocation before and after save/reopen and record the Report View:
there must be no "graph must be a DAG" or "still touched after recompute"
message. A headless regression is intentionally skipped when FreeCAD is not
installed in the executing environment; that skip is not acceptance evidence.

This handoff is intentionally not a pass record. The current desktop inventory
contains no FreeCAD window, so no manual result has been captured here.
