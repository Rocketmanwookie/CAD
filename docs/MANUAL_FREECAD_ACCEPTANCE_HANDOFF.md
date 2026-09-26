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

This handoff is intentionally not a pass record. The current desktop inventory
contains no FreeCAD window, so no manual result has been captured here.
