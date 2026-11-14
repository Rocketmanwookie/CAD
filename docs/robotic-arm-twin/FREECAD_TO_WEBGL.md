# FreeCAD → Blender → WebGL

The reference supplied by the user is [Exporting models from FreeCAD to WebGL](https://www.youtube.com/watch?v=nQB6FfC7C7Y), published by Verge3D by Soft8Soft on August 13, 2019. Its published description outlines FreeCAD-to-OBJ transfer, Blender preparation, and a Verge3D browser application, including appearance optimization. Video playback/transcript was not retrieved; this attribution refers to the published description. Its interface steps may differ from current software.

We use the same CAD-to-mesh-to-browser principle with an open-source path: **FreeCAD geometry → named mesh components → optional Blender preparation → glTF/GLB → WebGL viewer**. Verge3D is not a dependency of this package. The current custom WebGL viewer remains functional and does not yet load the new GLB; the GLB is an additional standard asset for compatible viewers and the next iteration.

## Files ready to use

Under `web/assets/`:

- `abb_irb6720.obj`: actual supplied ABB geometry, with 12 named component objects. Meters; CAD Z-up orientation.
- `abb_irb6720.mtl`: simple body/base/cable colors. Keep beside the OBJ.
- `abb_irb6720.glb`: glTF 2 binary, 12 named component nodes, meters, and a Z-up-to-Y-up scene rotation for glTF. Contains the same preview geometry and simple materials.

The source is the supplied `IRB6720LPS_240kg-265_OC_00_ASM_CAD.step`, processed using FreeCAD. Workspace geometry was excluded. Source filename and SHA-256 are included in GLB metadata. No joint axes, motor constants, material densities, or deflection values were invented. The LINK03 validity finding still applies.

The assets are generated locally and Git-ignored because manufacturer geometry redistribution rights have not been established. Original exporter code uses the package's MIT license; that does not relicense the ABB geometry.

## Reproduce exports

First generate `web/cad_mesh.json` from the actual STEP using FreeCAD's matching Python and `tools/export_view_mesh.py`, as described in the workbook. Then ordinary Python is sufficient:

```bash
cd /home/egrantjr/Documents/Repositories/controlforgecad/docs/robotic-arm-twin
python3 tools/export_web_assets.py web/cad_mesh.json web/assets
python3 tools/build_offline_viewer.py
```

This adds a portable exchange route without replacing the existing viewer. On the CAD page, download links appear below the static table. Refresh the browser; restart an already running Python lab server to register the newly added asset routes.

## Optional Blender preparation

1. Open Blender in a new working file.
2. Import the Wavefront OBJ, with its MTL in the same folder. Preserve separation by named objects; verify all 12 components in the Outliner.
3. Check units against the known dimensions. These exported coordinates are already meters: do not apply another 0.001 conversion.
4. Inspect the assembled posture. Do not move components independently while merely preparing appearances.
5. Improve materials, lighting, and mesh density as needed. Keep an untouched reference copy and compare before/after geometry. Do not collapse all components into a single object if joint animation is planned.
6. Save the Blender working file separately from original engineering CAD.
7. Export glTF 2 Binary (`.glb`) with the intended component objects selected. Keep the hierarchy and check the imported result in the target viewer.

The OBJ has CAD coordinates with Z upward; import-axis settings must preserve that physical orientation. glTF uses Y upward. The directly generated GLB already contains the coordinate conversion. Do not apply the same correction twice.

For motion, each component also needs a physical joint pivot, an axis, parent/child relationships, and an angle convention. A named object does not automatically have its origin at its bearing. Material/UV preparation does not establish kinematics or validated gravity sag.

## Why keep the STEP?

The STEP is the engineering reference. OBJ and GLB approximate its surfaces with triangles for display. Measurements and model repairs should refer back to the engineering geometry and the cited manual. The current export uses a preview tessellation tolerance, not a manufacturing or metrology mesh.
