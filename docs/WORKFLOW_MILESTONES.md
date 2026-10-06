# Workflow restructuring milestones

Owner-approved direction: 2026-10-06. The primary stages are Project & Plant,
Controls Circuit, Safety Circuit, Parts & CAD, Cabinet & Routing, and Generate
Package. Both circuits precede shared cabinet construction.

| Milestone | Delivery | Acceptance | Status |
|---|---|---|---|
| M1 — Focused intake and counts | Separate Plant Questionnaire and I/O Count entry points, persisted plant facts and actual counts, live 20% capacity targets | Plant edits preserve PLC/I/O data; count edits preserve labels/hardware; correct per-type rounding; desktop save/reopen | Starter implemented; 254 tests passed on 2026-10-06; desktop acceptance pending |
| M2 — Controls circuit | PLC configurator using count targets, CPU/module review, one editable I/O definition table and import route, logical circuit connections | Installed capacity covers typed targets; spare channels remain separate; edits/imports preserve identities and expose affected assignments | Configurator and allocated-point label table implemented; import/table expansion and circuit workflow remain open; desktop acceptance pending |
| M3 — Safety circuit | Supplied requirements, safety point/channel definitions, hardware selection and logical connections | Both circuit equipment/endpoint sets are ready for shared cabinet construction | Planned |
| M4 — Combined parts and CAD | Combined equipment list, personal/CADbase library resolution, missing-asset collection and endpoint matching | Every needed occurrence has a resolved part, dimensions and connection data, or an explicit unresolved item | Planned |
| M5 — Shared cabinet and routing | Final enclosure sizing/selection, placement of both circuits, terminals and Cables routes | Combined assembly realizes both circuits; routed connections retain endpoint identities | Planned |
| M6 — Generate package | Coordinated BOM, circuit drawings, 2D/3D cabinet representations, cabinet sheets and final wire schedule | Outputs use the same project revision and show changes requiring regeneration | Planned |

M1 initially uses the plant fields already supported by CE_Project. Richer
environmental conditions and supplied requirements references need model and
interchange extensions before Project & Plant can be considered complete.

The existing allocation/path save/reopen/recompute acceptance remains open as
a foundation check for M2. The supplied controls-document templates are inputs
to later adapters and do not establish generated-package completion.

## M1 desktop acceptance

Restart the linked FreeCAD workbench and select Controls / Automation.
The new Controls Workflow toolbar and Workflow submenu expose Plant
Questionnaire and I/O Count. Lower-level commands remain in Supporting Tools
and Exports submenus during migration. The combined New Controls Project entry
is retired from visible navigation; its command registration is retained for
compatibility.

1. In a new document, open Plant Questionnaire, fill project/plant facts and
   save. Confirm one CE_Project exists. Cancel a subsequent edit and confirm
   its saved values remain unchanged.
2. Open I/O Count. Enter DI=1, DO=5, AI=6, AO=0. Confirm capacity targets are
   DI=2, DO=6, AI=8, AO=0; save and verify actual counts remain 1, 5, 6, 0.
3. Enter an invalid count and confirm it is rejected without saving; cancel.
4. On a project with existing PLC selection and defined I/O, edit the plant
   facts and counts separately. Confirm neither action replaces those records.
5. Save, close, reopen and inspect the stored plant facts and actual counts.
   Reopen both dialogs and confirm they show the saved values.

Record FreeCAD version, tested checkout/revision, Report View findings and
saved FCStd evidence. Passing this check covers the starter dialogs, not the
remaining configuration/table/import and richer questionnaire work.

## M2 configurator checkpoint

The Controls Workflow toolbar continues with PLC Configurator and Define I/O.
The configurator shows feasible CPUs and the installed module/slot list for
20% capacity targets; saving also materializes the allocation. Define I/O
opens the existing channel review table to edit engineering labels while
preserving canonical tags and coordinates. Custom tag/type/device editing and
CSV import are subsequent table work.

Project allocations now retain spare-only expansion modules, while IOSignals
contains actual demand only. This also applies to the supporting Allocate PLC
I/O command. Checks at this checkpoint: 257 regression tests passed, compilation
and critical Ruff passed. Desktop check: DI=8 with CPU 1212C DC/DC/DC must
create a spare-only DI module beyond its eight onboard points; Define I/O must
show eight actual points. Save/reopen and verify that labels, assignments and
the extra module remain consistent.
