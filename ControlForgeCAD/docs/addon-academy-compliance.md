# FreeCAD Addon Academy alignment

ControlForgeCAD follows the official FreeCAD Addon Academy guidance for an
existing Python workbench. This checklist is intended to remain executable and
reviewable as the add-on develops.

## Current decisions

- `package.xml` uses metadata format 1, the official metadata namespace, an
  SPDX license identifier, an icon, repository/readme/bug-tracker URLs, a
  minimum FreeCAD version, and focused lowercase tags.
- The manifest workbench `classname` exactly matches
  `ControlsEngineeringWorkbench` in `InitGui.py`.
- The workbench icon is an uncompiled SVG under `Resources/Icons/` and its class
  attribute is an absolute path.
- GUI command imports and registration are deferred to `Initialize()` so merely
  discovering the add-on does not load the implementation modules.
- All GUI command IDs use the project-specific `CE_` prefix.
- Commands that mutate a document run inside a named transaction and abort the
  transaction if an exception escapes, preserving FreeCAD Undo/Redo behavior.
- Source files carry SPDX license headers. The project retains its existing MIT
  license; Addon Academy's LGPL recommendation is guidance, not a requirement.
- The current `Init.py` / `InitGui.py` layout is the documented legacy layout.
  It remains supported for an existing add-on. A move to the modern
  `freecad/ControlForgeCAD/` namespace should be treated as a separate,
  compatibility-tested migration rather than a cosmetic file move.

## Release gate

Before Addon Manager submission:

1. Run the full Python test suite and XML schema validation.
2. Load the linked checkout in the minimum supported FreeCAD version and verify
   the workbench icon, commands, menus, and toolbars.
3. Exercise every document-changing command with Undo/Redo and verify saved
   documents reopen without migration warnings.
4. Add command-specific SVG icons and translation catalogs as the GUI stabilizes.
5. Add `Resources/Documents/Overview.md` and screenshots once the workbench has
   representative production UI.
6. Revisit the modern namespaced package layout before the first stable release.

## Authoritative guidance

- <https://freecad.github.io/Addon-Academy/Topics/Structuring/>
- <https://freecad.github.io/Addon-Academy/Topics/Structuring/Manifest/>
- <https://freecad.github.io/Addon-Academy/Guides/Code/Workbench/>
- <https://freecad.github.io/Addon-Academy/Guides/Code/Commands/>
- <https://freecad.github.io/Addon-Academy/Guides/Code/Icons/>
- <https://freecad.github.io/Addon-Academy/Guides/Maintaining/Compatibility/>
