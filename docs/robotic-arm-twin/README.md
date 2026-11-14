# ABB IRB 6720 digital-twin learning package

Start with [GUIDE.md](GUIDE.md), or open [GUIDE.html](GUIDE.html) for a searchable offline workbook with rendered equations. This is an independent educational package in the repository's documentation tree; it does not alter the ControlForgeCAD workbench.

## Run

```bash
cd /home/egrantjr/Documents/Repositories/controlforgecad/docs/robotic-arm-twin
python3 -m unittest discover -s tests -v
python3 tools/twin_lab.py serve --database /tmp/irb6720-lab.sqlite --port 8765
```

Keep the terminal open, then visit:

If the requested port is busy, the server tries the next port, up to five total attempts (for example, 8765–8769). Open the successful URL printed in the terminal; use that same port for `/cad.html`. If all five are busy, choose another `--port`.

- `http://127.0.0.1:8765/` — synthetic telemetry teaching lab.
- `http://127.0.0.1:8765/cad.html` — actual supplied ABB assembly preview, drag to orbit/scroll to zoom.

Both are local only. The CAD viewer's generated mesh is present locally and Git-ignored because manufacturer redistribution rights have not been established. The viewer is static CAD geometry with camera controls; it is not connected to the robot or to the synthetic joint stream.


You can also open `web/cad-standalone.html` directly in a WebGL-capable browser; it embeds the actual CAD mesh and needs no running server or internet connection. This generated manufacturer-geometry file is kept local.

## Contents

| File/directory | Purpose |
|---|---|
| `GUIDE.md`, `GUIDE.html` | 19-chapter step-by-step workbook and equation derivations |
| `evidence/cad_inventory.json` | Actual FreeCAD geometry inspection and source hashes |
| `evidence/manual_provenance.json` | Exact supplied ABB document revision and hash |
| `config/abb_specification.json` | Manual joint limits/speeds and variant qualifications |
| `config/measured_model.template.json` | Explicitly unmeasured frames and physics fields |
| `commissioning_measurements.csv` | Fillable evidence and measurement checklist |
| `requirements.csv` | Requirement-to-test traceability and honest current status |
| `tools/twin_lab.py` | Standard-library telemetry, validation, SQLite, replay, and HTTP |
| `tools/inspect_cad.py` | Reproducible FreeCAD-based STEP inventory |
| `tools/export_view_mesh.py` | CAD-to-WebGL preview export with workspace excluded |
| `tools/make_urdf.py` | Visual URDF helper; refuses unmeasured input unless `--demo` |
| `tools/jsonl_to_ros.py` | Observational normalized JSONL-to-JointState bridge starter |
| `tools/ingest_postgres.py` | Idempotent JSONL-to-PostgreSQL teaching loader |
| `sql/` | Historian/context schema and example dashboard queries |
| `config/mosquitto*` | Local exercise and site-configured TLS/ACL templates |
| `SOURCES.md` | Primary documentation, license references, and provenance |
| `evidence/verification.md` | Checks performed and boundaries not tested |

## Actual finding to resolve

The imported ABB `LINK03_CAD` fails FreeCAD solid validity checking. The standalone LINK03 deep check reports “Invalid imbrication of wires”; a standard repair attempt on a transient copy did not correct it. See `evidence/link03_diagnosis.json`. The workspace envelope is also included inside the source assembly. The preview excludes the envelope; the invalid link remains available for visual inspection, with a warning. Repair and revalidate it before using its solid volume/inertia or collision representation for engineering conclusions.

The original teaching code and text are MIT licensed; see `LICENSE` for scope exclusions covering manufacturer geometry and third-party software.

No ABB controller has been accessed. ROS/Gazebo, MQTT, PostgreSQL, and Grafana service deployment and hardware commissioning are described, not falsely reported as completed. All proposed twin-side software is open source; the existing ABB controller firmware is proprietary.

## Static pose exercise

The main page opens with two dropdowns in 15-degree increments and a Go button. The applied pose stays fixed until Go is clicked again. Its two-row table shows angles, gravity holding torques, and an illustrative elastic joint-deflection estimate, using the explicitly stated point-payload and stiffness assumptions. The image shows the requested rigid pose, not an exaggerated deflection. Temperature is not displayed. The page contains only the two-joint static exercise; the six-joint telemetry panel and its background polling have been removed. These controls are on `/`, not the static ABB CAD camera viewer at `/cad.html`.

## FreeCAD to WebGL exchange route

See [FREECAD_TO_WEBGL.md](FREECAD_TO_WEBGL.md) for the user-supplied video reference, grouped OBJ/MTL files for Blender, and standard GLB assets. Downloads appear on the CAD page after restarting the server. The existing preview renderer remains in place.

## Vibration and maintenance laboratories

After restarting the server, use `/vibration.html` for a two-inertia motor/load torsional simulation. Edit assumptions, compare damping, run periodic torque or free ring-down, and download the parameterized simulation record. The frequency-response plot is an analytic response, not a measured FFT. See [VIBRATION_AND_MAINTENANCE.md](VIBRATION_AND_MAINTENANCE.md) for equations and validation boundaries.

Continue to `/maintenance.html` for a schedule based on the independently retrieved ABB product manual **3HAC085697-001 Revision N, pp.120–122**. Enter per-item service history and DTC hours. Missing history remains unknown. A clearly marked fictional dataset is available for training. Qualitative fault trees preserve unknown conditions and do not assign failure probabilities from overdue status. Plans and hypothetical scenarios can be downloaded as JSON. These pages do not write to the real robot or CMMS.
