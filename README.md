# CAD

This repository currently contains the IntegraCAB Open / ControlForgeCAD FreeCAD workbench under `ControlForgeCAD/`.

## FreeCAD development install

Link or copy `ControlForgeCAD/` into your FreeCAD user `Mod` directory, then restart FreeCAD.

```bash
mkdir -p ~/.local/share/FreeCAD/Mod
ln -s /home/egrantjr/Dev/CAD/ControlForgeCAD ~/.local/share/FreeCAD/Mod/ControlForgeCAD
```

In FreeCAD, select **Controls / Automation** from the workbench selector. Confirm these commands appear in the toolbar or menu:

- `CE_NewProject` - New Controls Project
- `CE_CreatePanel` - Create Control Panel
- `CE_ValidateProject` - Validate Controls Project
- `CE_PreviewMissingData` - Preview Missing Data
- `CE_ExportBOM` - Export BOM
- `CE_ExportCEProjectXML` - Export CEProject XML

Pure-Python validation from the repository root:

```bash
python3 -m pytest
python3 -m compileall ControlForgeCAD
```
