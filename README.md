# CAD

This repository currently contains the IntegraCAB Open / ControlForgeCAD FreeCAD workbench under `ControlForgeCAD/`.

## FreeCAD development install

Link or copy `ControlForgeCAD/` into your FreeCAD user `Mod` directory, then restart FreeCAD. The helper script creates an idempotent symlink from this checkout:

```bash
python3 scripts/link_freecad_workbench.py
```

Equivalent manual symlink command:

```bash
mkdir -p ~/.local/share/FreeCAD/Mod
ln -s /home/egrantjr/Dev/CAD/ControlForgeCAD ~/.local/share/FreeCAD/Mod/ControlForgeCAD
```

Equivalent copy command:

```bash
mkdir -p ~/.local/share/FreeCAD/Mod
cp -R /home/egrantjr/Dev/CAD/ControlForgeCAD ~/.local/share/FreeCAD/Mod/ControlForgeCAD
```

In FreeCAD, select **Controls / Automation** from the workbench selector. Confirm these commands appear in the toolbar or menu:

- `CE_NewProject` - New Controls Project
- `CE_AddIOSignal` - Add I/O Signal
- `CE_CreatePanel` - Create Control Panel
- `CE_ValidateProject` - Validate Controls Project
- `CE_PreviewMissingData` - Preview Missing Data
- `CE_ExportBOM` - Export BOM
- `CE_ExportCEProjectXML` - Export CEProject XML
- `CE_ExportIOList` - Export I/O List
- `CE_ExportMissingDataCSV` - Export Missing Data CSV

Pure-Python validation from the repository root:

```bash
/usr/bin/python3 -m pytest
python3 -m compileall ControlForgeCAD
```

On this workstation, `/usr/bin/python3` has `pytest` available. The default
`python3` currently resolves to Homebrew Python and may report `No module named
pytest`.

Manual FreeCAD validation:

1. Start or restart FreeCAD after linking or copying the workbench.
2. Select **Controls / Automation** from the workbench selector.
3. Confirm the commands listed above appear in the workbench toolbar or menu.
4. Run **New Controls Project** and confirm the Project Intake dialog opens.
5. Enter core intake values, submit the dialog, and confirm a `CE_Project` object appears in the model tree.
6. Select `CE_Project` and confirm the Property View exposes editable CEProject and Intake properties including project name, customer, site/location, deliverables, PLC platform, voltage, phase count, enclosure rating, and sensor count.
7. Save the document as `.FCStd`, close it, reopen it, and confirm the basic editable `CE_Project` properties are retained.
8. Clear `SensorCount`, `DICount`, and `AICount`, run **Preview Missing Data**, and confirm `io.sensorCount` is reported as missing.
9. Fill `SensorCount`, or fill DI and AI counts, rerun **Preview Missing Data**, and confirm `io.sensorCount` is shown as an input-count response rather than missing.
10. Run **Create Control Panel** and confirm starter placeholder layout objects appear for panel/backplate, DIN rail, wire duct, terminal strip, and PLC rack/module.
11. Run **Validate Controls Project** and confirm validation reads the edited project and starter layout metadata.
12. Run **Export BOM** and confirm `~/controlforgecad_bom.csv` includes starter layout objects where manufacturer/part-number/description data is assigned.
13. Run **Export CEProject XML** and confirm `~/integracab_ceproject.xml` is written.
14. Run **Export I/O List** and confirm `~/integracab_io_list.csv` is written from explicit `IOSignals` plus the current starter intake data. `IOSignals` remains blank until **Add I/O Signal** is used.
