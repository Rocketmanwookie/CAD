# Verification record — November 3, 2026

## Performed

- Imported the supplied ABB `ASM_CAD.step` using the installed FreeCAD 1.1.4 Python/CAD engine, inspected assembly objects, recorded unit declarations, hierarchy, source hashes, bounding boxes, volume outputs, and `isValid()` results in `cad_inventory.json`.
- Confirmed manufacturer workspace geometry is contained inside the assembly. Excluded it and avoided assembly-container double counting during browser-mesh export. Produced 12 component groups, 93,560 vertices, and 187,221 triangles. Checked finite vertices, triangle index ranges, and group triangle coverage.
- Found `LINK03_CAD` invalid, and the encompassing assembly compound invalid. Its displayed geometry is retained with a warning. The standalone LINK03 also fails independently: deep checking reports “Invalid imbrication of wires”. A standard fix on a transient copy returned false and remained invalid. `link03_diagnosis.json` records the result. No source CAD was changed, and no validated repair is claimed.
- Read supplied 210-page ABB product specification identity: 3HAC085704-001 Revision M. Extracted relevant pages and visually rendered/checked the range, dimension, and load-inertia diagrams, including the range footnotes. Recorded PDF hash and reviewed pages in `manual_provenance.json`.
- Browser-rendered the actual CAD geometry over a local HTTP server. Observed the 12-group/187,221-triangle model. Initial narrow viewport clipping led to an adaptive bounding-box fit correction; post-correction JavaScript syntax and mesh structure checked. The in-app browser subsequently refused local connections after temporary server lifecycle ended; it also blocks `file://` URLs. The final self-contained offline file was structurally checked but was not browser-rendered through that blocked route. A separate offline CAD plot was rendered and visually inspected.
- Local automated HTTP check: `python3 tools/verify_http.py` passed. Verifies fresh synthetic state, archive history, telemetry HTML, CAD HTML, and CAD mesh response, then stops its test server. Performed with loopback socket access enabled for that short test.
- Standalone unit tests: `python -m unittest discover -s tests -v` — **7 tests passed**, including malformed values, optional unavailable channels, timestamps, duplicate/out-of-order/gap behavior, archive retention, analytic synthetic velocity, and unmeasured-model rejection.
- Python compilation of teaching tools passed. Ruff fatal-error checks (`E9,F63,F7,F82`) passed for tools/tests.
- Generated a six-revolute-joint visual URDF example; unmeasured real-model generation remains refused unless explicitly marked demo.
- Generated 500 time-spaced synthetic JSONL records for the telemetry lesson.
- Both web JavaScript blocks passed `node --check` syntax checks.
- Built searchable HTML workbook with offline MathML equations and no Pandoc conversion warnings. More than 50 MathML expressions verified programmatically (231 before final appendices; exact total varies with edits).
- Repository regression run: `python3 -m pytest -q` — **306 passed, 1 skipped**. These are the repository's configured test collection, separate from the 7 standalone lab tests.
- Existing workbench Python compilation and repository-prescribed Ruff fatal-error checks passed. No existing workbench implementation files were changed.

## Not performed / not claimed

No physical controller connection, motion command, serial-number check, actual controller API measurement, verified joint-axis/zero calibration, physical link mass/inertia measurement, validated collision model, validated balancing-force law, or predictive-maintenance training was performed. ROS/Gazebo, MQTT/TLS, PostgreSQL, and Grafana deployments were not available as configured services and are documented integration steps rather than verified deployments. The JSONL-to-ROS and PostgreSQL loaders were compiled/linted but not executed against those external dependencies.

No claim of ABB controller equivalence, formal standards conformance, safety-system validation, or manufacturer CAD redistribution rights is made. The included FRS distinguishes delivered instructional artifacts from physical commissioning requirements.

The user-supplied source files and pre-existing repository changes were left untouched. Generated mesh and standalone CAD HTML are Git-ignored local artifacts; the source code, workbook, and evidence live independently under `docs/robotic-arm-twin`.

## Vibration / maintenance extension — November 3, 2026

- Retrieved ABB product manual 3HAC085697-001 as Revision N through the official document endpoint; SHA-256 stored in `product_manual_provenance.json`. Visually reviewed schedule pages 121–122 and interval definitions on p.120. No older cached-search revision was used for the final transcription.
- Added a two-inertia torsional time-response and harmonic-response model. Checked exact 2×2 modal reference values, static compliance, numerical/analytic forced-response agreement, undamped energy conservation, damped energy loss, zero excitation, singular resonance handling and input rejection using `node tests/test_vibration_model.js`.
- Checked calendar month/leap-day arithmetic, DTC deadlines, conditional forecasts, missing history, one-time completion and three-valued AND/OR gates using `node tests/test_maintenance_model.js`.
- Standalone Python suite now has 13 passing tests; existing static UI regression remains passing. New JavaScript parses, Python compiles and fatal-error lint checks pass. HTTP test includes the new page/script routes.
- Browser-rendered both new pages on a separate loopback test server. Changed damping and ran simulation: the table and plots updated. Loaded explicitly fictional maintenance history and observed calculated due/overdue results and conditional forecasts. Verified that assuming missed maintenance alone leaves a fault-tree outcome undetermined. Fixed leaf-dropdown updates to preserve focus, then rechecked the interaction in the browser. Browser screenshots saved as `vibration-browser.jpg` and `maintenance-browser.jpg`.
- Vibration values are assumed, not ABB-identified. Fault trees are qualitative scenarios, not measured conditions or probabilistic failure predictions. No real maintenance record or physical hardware command was written. The timeline is a reviewed schedule-table starter, not every event-triggered instruction in the full manual.
