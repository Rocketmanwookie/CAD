# Build an open-source digital twin of the ABB IRB 6720-240/2.65

A beginner's workbook, engineering reference, and commissioning plan. Prepared November 3, 2026.

**Start here:** read Chapters 1–4, run the local lab, then work through one chapter at a time. The numbered steps are work you can actually perform. The equations explain why those steps work. You do not need to understand every equation before seeing the first result.

**Evidence labels used throughout:** **MANUAL** means the supplied ABB product specification, **CAD** means inspected geometry, **EXAMPLE** means invented teaching numbers, **TARGET** means a proposed acceptance criterion, and **MEASURE** means data still needed from the installed robot. An example is never permission to move a real machine.

This is a complete instructional route and a tested local teaching package. It is not a claim that your physical robot has been connected or that an ABB-equivalent motion controller has been recreated. The actual 3D CAD preview, the synthetic telemetry lab, and the eventual calibrated operational twin are separate stages.

## Contents

1. What we are building
2. What your files establish
3. The open-source toolbox and architecture
4. First success: run the laboratory and CAD viewer
5. Hardware, sensors, and installation planning
6. CAD preparation in FreeCAD
7. Frames, units, and the mathematics of movement
8. Forward kinematics, Jacobians, and inverse kinematics
9. Mass, inertia, forces, and robot dynamics
10. ABB load diagrams and the balancing mechanism
11. Time, sampling, networking, and reliability
12. Telemetry contracts and controller integration
13. ROS 2, RViz, and Gazebo
14. Historical storage, dashboards, and enterprise context
15. Thermal, vibration, and condition monitoring
16. Calibration, uncertainty, and validation
17. Requirements and acceptance gates
18. Daily operation and troubleshooting
19. Exercises, glossary, and references

## 1. What we are building

Imagine that your robot has a notebook, a moving picture, and a calculator that stay together.

* The **picture** shows where the robot is.
* The **notebook** remembers temperatures, positions, maintenance, faults, and production jobs.
* The **calculator** estimates what should happen, compares that estimate with measurements, and flags differences.

A CAD model is the picture's shape. A simulation is an experiment with a model. A live digital shadow updates from a real machine. An operational twin adds identified model versions, synchronized measurements, validated calculations, history, and decisions linked to explicit engineering requirements. Definitions vary; this workbook uses that practical distinction rather than relying on a marketing label. NIST describes digital twins in the context of connected models and physical systems: [NIST digital twins](https://www.nist.gov/digital-twins).

Our first engineering goals are:

1. Display the measured six-axis posture with known joint ordering and units.
2. Show whether the displayed state is fresh, stale, uncertain, or unavailable.
3. Store enough context to reproduce what the twin showed yesterday.
4. Compare expected and measured behavior under documented operating conditions.
5. Detect changes worth investigating, without pretending an anomaly score proves a specific failure.

The default physical integration is observational. The factory controller continues controlling motion. Motion experiments run in a separate simulation. Connecting a planning package does not make a browser a safety controller.

### What “all open source” means here

Every proposed software component on the twin side has an open-source implementation. You do not need SolidWorks, RobotStudio, MATLAB, Simulink, Siemens digital-twin software, or a commercial cloud subscription to follow this route.

The actual ABB OmniCore controller and RobotWare are proprietary components of the physical asset. If “every piece of software, including firmware already inside the ABB robot” must be open source, the supplied ABB system does not meet that stronger requirement. Replacing that controller is a different controls and machine-safety project. We do not claim that an open-source simulator duplicates ABB TrueMove or QuickMove.

The supplied CAD and PDF are engineering inputs with their own rights. Open-source tools do not automatically make manufacturer CAD open licensed. Keep derived meshes local until redistribution rights are established.

## 2. What your files establish

### 2.1 Source identity

The main CAD file is:

`/home/egrantjr/Documents/CADBaseFiles/IRB6720LPS_240kg-265_OC_00_STEP_J/IRB6720LPS_240kg-265_OC_00_ASM_CAD.step`

The source document is:

`/home/egrantjr/Downloads/3HAC085704 PS IRB 6720-en.pdf`

[Official ABB manual source](https://search.abb.com/library/Download.aspx?DocumentID=3HAC085704-001&LanguageCode=en&DocumentPartId=&Action=Launch). The revision and page citations below refer to the supplied local PDF; the online download may change.

The PDF identifies itself as **Product specification — IRB 6720**, **3HAC085704-001, Revision M**, 210 PDF pages. Its scope covers OmniCore. It references separate manipulator product manuals, controller manuals, and RobotWare documentation. It is a product specification, not a full servicing manual or a controller API manual. Page references below refer to the printed page numbers, which match the inspected PDF pages here.

The STEP header identifies AP214, a SolidWorks 2024 export, and an export date of June 11, 2026. That is provenance, not a requirement to use SolidWorks. See the generated `evidence/cad_inventory.json` for SHA-256 hashes, products, assembly relationships, geometry validity checks, volumes, and bounding boxes. A checksum is a file's fingerprint: if the file changes, its fingerprint almost certainly changes.

The former small demonstration arm is superseded. Its inferred dimensions and components must not be mixed into this ABB model.

### 2.2 Verified manual facts

| Item | MANUAL value | Where and how to use it |
|---|---|---|
| Variant | IRB 6720-240/2.65, standard variant | Verify installed nameplate; do not substitute a 215 kg LID model |
| Nominal handling capacity | 240 kg | p.10; load diagrams and configuration still apply |
| Nominal reach | 2.65 m | p.10; not a solid sphere of reachable tool poses |
| Nominal manipulator mass | 1,160 kg | p.21; excludes added options, tool, and other attached equipment |
| Mounting | Floor mounted, nominal 0° | p.21; actual installation angle must be configured |
| A2–A3 center distance D | 1,185 mm | p.41 drawing, cross-check CAD axes |
| A3 to A5 horizontal drawing dimension B | 1,132.5 mm | p.41; use drawing's precise witness lines |
| A5-to-flange drawing dimension C | 200 mm | p.41, standard variant; LID uses another dimension |
| Base-axis to shoulder drawing offset E | 320 mm | p.41; do not assume every dimension is a DH parameter |
| Axis speed maxima | 110, 90, 90, 170, 120, 190 degrees/s | p.96; maxima, not required operating speeds |

The p.41 drawing also gives A = 2,351.5 mm, F = 345 mm, G = 30 mm, R1a = 634 mm, R1b = 525 mm, R3 = 446 mm, and R4 = 216 mm. The R values describe circumscribed radii; they are not link lengths. Use the drawing's dimension arrows, not a guessed interpretation of the letters.

### 2.3 Joint limits for the standard variant

| Joint | Default manual range, degrees | Range, radians (approximately) | Maximum speed, rad/s |
|---|---:|---:|---:|
| A1 | −170 to +170 | −2.96706 to +2.96706 | 1.91986 |
| A2 | −65 to +85 | −1.13446 to +1.48353 | 1.57080 |
| A3 | −180 to +70 | −3.14159 to +1.22173 | 1.57080 |
| A4 | −300 to +300 | −5.23599 to +5.23599 | 2.96706 |
| A5 | −130 to +130 | −2.26893 to +2.26893 | 2.09440 |
| A6 | −360 to +360 | −6.28319 to +6.28319 | 3.31613 |

Sources: manual pp.38–39 and p.96. The A1 extension to ±220° is optional, not the default. The A3 lower limit becomes −160° with lower-arm DressPack. Installed restrictions, mechanical stops, and configuration can reduce these envelopes. The LID wrist limits are different. Preserve multi-turn A4/A6 values; blindly wrapping all angles into ±π loses real configuration information.

**Do not invent actuator torque limits from these speeds.** They are separate physical quantities. The manual does not provide the six verified link masses and inertia tensors needed for a trustworthy inverse-dynamics model. Nor does it provide every encoder, transmission, friction, thermal, or controller parameter.

### 2.4 What each CAD file is for

| Filename suffix | Intended starting role | Important check |
|---|---|---|
| `ASM_CAD` | Complete assembly and its reference posture | Establish assembly coordinates and placement hierarchy |
| `BASE_CAD` | Fixed base | Align base frame to mounting plane and A1 axis |
| `LINK01` through `LINK06` | Candidate moving-link geometry | Determine physical attachment and axis frame; filename is not proof of a revolute joint |
| `LINK02_CAD00`, `LINK04_CAD00` | Additional or alternate component geometry | Compare against assembly references before inclusion; avoid duplicate mass |
| `LINK01m_CABLE` etc. | DressPack/cable geometry | Separate cosmetic rigid approximation from flexible behavior |
| `CYL_CAD`, `ROD_CAD` | Balancing-cylinder mechanism | Determine passive motion; do not turn into extra independent robot axes |
| `Working-space` | Manufacturer workspace visualization | Reference envelope; do not export as a solid robot link or collision obstacle |

Existing `RobotArm.FCStd`, `RobotArm_Exploded.FCStd`, and `RobotAssemb.FCStd` files were observed in the source folder. They are left untouched. A reproducible workflow starts from the specified STEP and records transformations into a separate working copy.

## 3. The open-source toolbox and architecture

### 3.1 Chosen baseline

Use **Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic** as a deliberately matched teaching baseline. It is a supported combination, not a claim that Jazzy is the newest release. The official Gazebo integration documentation identifies compatible ROS/Gazebo combinations: [Gazebo with ROS](https://gazebosim.org/docs/harmonic/ros_installation/). ROS's installation source specifies Ubuntu Noble: [ROS Jazzy Ubuntu installation source](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Installation/Ubuntu-Install-Debs.rst).

| Job | Open-source choice | Why it is present |
|---|---|---|
| CAD preparation | FreeCAD / Open CASCADE | Read STEP, measure axes, group solids, export meshes |
| Robot description | URDF / Xacro | Name links and joints and encode their transforms |
| Live robot communication | ROS 2, DDS | Share synchronized robot state between processes |
| Live 3D display | RViz 2 | Render geometry using measured joint states |
| What-if physics | Gazebo Harmonic, ros2_control | Simulated motion and dynamics, separate from hardware |
| Optional trajectory planning | MoveIt 2 | Plan collision-aware paths after model validation |
| Telemetry transport | Eclipse Mosquitto MQTT | Broker signals across edge and historian boundary |
| Data adapter | Python; optional open62541 | Normalize controller APIs or OPC UA into one contract |
| Teaching archive | SQLite | No server setup needed for the first lab |
| Production historian | PostgreSQL | Structured observations plus maintenance and production context |
| Dashboard | Grafana OSS | Query history and show trends and health |
| Time sync | chrony; LinuxPTP when justified | Keep timestamps comparable across hosts |
| High-rate recordings | rosbag2 / MCAP | Reproduce robot state and debugging sessions |
| Optional engineering analysis | CalculiX, NumPy, SciPy | Structural, parameter-fit, and signal-analysis work |
| Local CAD preview | Python + browser WebGL | View the supplied geometry without a proprietary viewer |

Licenses vary by component and dependency. FreeCAD's main license is LGPL; the ROS `rclcpp` client and Gazebo Sim use Apache-2.0; Mosquitto offers EPL/EDL licensing; PostgreSQL uses its own permissive open-source license; Grafana OSS is AGPLv3; open62541 uses MPL-2.0. Exact deployed versions and dependencies need their own license inventory. Do not replace Grafana OSS with an enterprise binary while calling the stack wholly open source. Primary license links are in `SOURCES.md`.

### 3.2 Data flow, explained as a delivery route

```text
PHYSICAL CELL                   EDGE HOST                    TWIN / HISTORIAN HOST

Encoders -> ABB controller -> read-only adapter -> MQTT/TLS -> validator -> PostgreSQL
Temp / vibration sensors ------ timestamped DAQ -----^          |             |
                                                               |             v
                                                               |          Grafana
                                                               v
                                                    ROS JointState -> RViz
                                                               |
                                                       recorded rosbag2

Versioned CAD -> measured frames -> URDF + meshes -> RViz / separate Gazebo instance
Manual + maintenance + job records -----------------> contextual database tables

Separate Gazebo experiment -> expected behavior -> residual analytics <- real measurements
```

The **adapter** is a translator. The **broker** is a post office. The **validator** checks names, units, timestamps, and quality. The **historian** is the notebook. The **model registry** says which geometry and calibration were in use. The **analytics** are the calculator.

Use separate namespaces such as `/physical/irb6720/joint_states` and `/simulation/irb6720/joint_states`. A measured joint stream animates RViz. A simulation command drives Gazebo's simulated joints. They are different operations; publishing `JointState` alone does not apply torque to a Gazebo model.

### 3.3 Two alternatives and why they are not the baseline

A MuJoCo-based twin can be compact and useful for dynamics and optimization, but still needs CAD frames, a historian, telemetry, and controller integration. A browser-only mesh animation is quick to view, but does not solve timing, physical dynamics, or engineering validation. We use a small browser lab for learning and the ROS/Gazebo ecosystem for the larger integration.

## 4. First success: run the laboratory and CAD viewer

### 4.1 Open a terminal and start the lab

A terminal is a window where you type instructions. Copy one line at a time. Python is the program that runs our teaching scripts.

```bash
cd /home/egrantjr/Documents/Repositories/controlforgecad/docs/robotic-arm-twin
python3 -m unittest discover -s tests -v
python3 tools/twin_lab.py serve --database /tmp/irb6720-lab.sqlite --port 8765
```

Keep that terminal running. In a browser open:

`http://127.0.0.1:8765/`

`127.0.0.1` means your own computer. The server listens only locally. It does not connect to the ABB controller. The synthetic producer creates 100 samples per second; the browser asks for updates 10 times per second. Those are intentionally different rates.

The main page has shoulder and elbow dropdowns in 15-degree increments. Click **Go** to apply a static pose. The two-row table shows selected angles, gravity holding torques, and example gravity deflections for the stated point-payload and joint-stiffness assumptions. The picture stays fixed until Go is clicked again. Temperature is omitted. The page contains only this two-joint static exercise; it does not display or poll the six-joint synthetic stream. The two-link picture is not the supplied ABB CAD model or a six-axis kinematic solution.

Open `http://127.0.0.1:8765/cad.html` for the actual assembled CAD preview when the local mesh has been generated. Drag to orbit, scroll to zoom. That viewer displays the supplied assembly in its exported posture. It is not calibrated or telemetry-bound; displaying correct geometry is the first static-layer result.


You can also open `web/cad-standalone.html` directly in a WebGL-capable browser; it embeds the actual CAD mesh and needs no running server or internet connection. This generated manufacturer-geometry file is kept local.

Stop the server with Ctrl+C. Your SQLite archive remains at the path you selected.

### 4.2 Record and replay a file

```bash
python3 tools/twin_lab.py generate --count 500 --hz 100 --output /tmp/irb6720-example.jsonl
python3 tools/twin_lab.py serve --replay /tmp/irb6720-example.jsonl --database /tmp/irb6720-replay.sqlite --port 8765
```

A JSONL file contains one JSON object per line. Replay preserves recorded source timestamps and labels the stream `replay`; old recordings are intentionally stale. The generator creates a time-spaced synthetic recording ending at generation time. Use an actual live recording when testing real controller timing. This lab does not claim hard real-time scheduling, durable MQTT delivery, production authentication, or certified monitoring.

### 4.3 Generate a visual URDF example

```bash
python3 tools/make_urdf.py --demo --output /tmp/example_arm.urdf
```

The explicit `--demo` flag permits invented teaching dimensions. Calling the generator without that flag refuses an unmeasured model. The generated URDF has placeholder boxes and six revolute joints; it deliberately contains no fictional masses, collisions, or dynamics. It is a frame-learning aid, not an ABB model ready for Gazebo.

For the real model, copy `config/measured_model.template.json`, fill measured transforms and documented limits, then use `--model YOUR_FILE`. Even the measured generator output is visualization-only until its box visuals are replaced with local meshes and engineering checks pass.

## 5. Hardware, sensors, and installation planning

### 5.1 Start with the question, then choose a sensor

| Question | Signal needed | Plausible initial acquisition rate, TARGET |
|---|---|---:|
| Where is the arm? | Six joint positions, controller state | 100–250 Hz when supported |
| Is it following the expected path? | Measured and reference positions with timestamps | Match the relevant trajectory bandwidth |
| Is a gearbox warming unusually? | Calibrated temperature plus load and ambient | 1–10 Hz |
| Is vibration changing? | Accelerometer waveforms with analog anti-alias filtering | e.g. 12.8 kHz for a chosen band below 6.4 kHz |
| Is an air-operated tool losing pressure? | Pressure at the tool and valve state | e.g. 10–100 Hz |
| What job was running? | Job ID, payload, cycle start/end | Event driven |
| Why was it idle? | Controller mode, fault code, production schedule | Changes plus periodic heartbeat |

These are starting design targets, not rates promised by ABB RWS. Pressure and flow are relevant only if your tool or process uses them. Do not invent such channels because a generic digital-twin checklist mentions them.

Controller joint position is often the easiest first useful signal. An external temperature sensor may be needed if the controller does not expose a suitable channel. Motor current is not automatically output torque; Chapter 9 explains the additional parameters.

### 5.2 Computing and storage

For an initial single-arm project, a reasonable **planning starting point**, not a purchase specification, is a modern multicore CPU, 16–32 GB RAM, and SSD storage. A GPU helps large meshes and rendered cameras; a compact arm-state twin does not inherently require a large-VRAM GPU or a storage array. Benchmark the actual scene first. If all installed drivers must be open source, choose a GPU supported by the Linux Mesa stack and verify the specific device and distribution before purchase.

Use a separate edge computer near the robot if the visualization workstation is frequently disconnected. Prefer wired Ethernet for operational telemetry. Keep the robot's existing control network intact; the monitoring host must not become an unplanned component in its servo loop.

Before choosing an SSD, derive data volume in Chapter 11, add indexes and backups, and define retention. High-frequency vibration waveforms can dominate disk space. Store high-rate waveforms in chunks with metadata rather than a database row for every scalar sample.

### 5.3 Physical preparation

1. Record robot serial number, variant, controller type, RobotWare version, installed options, tool, DressPack, and mounting angle.
2. Photograph the cell and record coordinate markers; keep photos separate from calibration claims.
3. Find an approved observational interface on the installed controller.
4. Connect sensors through an appropriate isolated DAQ; record units, range, calibration date, sensor location, and clock source.
5. Start with existing stationary observations, then use established site commissioning procedures for permitted low-speed measurement motions.

A normal laptop, MQTT connection, and dashboard are not protective equipment. Keep the robot's existing emergency stops, guards, and safety logic independent of the twin.

## 6. CAD preparation in FreeCAD

### 6.1 Make a clean working copy

1. Open FreeCAD and create a new document.
2. Import `...ASM_CAD.step` using File → Import. Preserve assembly structure if the importer offers it.
3. Use View → Standard views → Axonometric, then Fit all.
4. Save to a new local working directory, for example `/tmp/irb6720-working.FCStd` while learning. Never overwrite the original source assembly.
5. Expand the model tree. Select parts one at a time and hide/show them using Space. Identify the fixed base, each moving body, balancing cylinder, rod, and cables.
6. Run Part workbench → Check geometry on the relevant solids. A valid B-rep does not prove a correct assembly or a physically accurate inertia.

A **solid** is a closed volume. A **compound** is a collection that may contain many solids. A rigid **link** in robotics can contain several solids bolted together. Ten solids do not necessarily mean ten independently moving links.

### 6.2 Establish units and scale

STEP carries unit information; STL does not. FreeCAD geometry normally uses millimeters. ROS uses meters.

One meter contains 1,000 millimeters, so:

\[
L_{m}=L_{mm}/1000.
\]

Example: 1,185 mm ÷ 1,000 = 1.185 m. A 1,185-meter lower arm is a unit error, not a very large robot.

Check the 1,185 mm shoulder-to-elbow dimension against the selected CAD geometry. Check the mounting plane and p.41 dimensions. The current folded-posture bounding box is not the nominal 2.65 m reach; reach involves possible motion.

### 6.3 Find joint axes

A revolute joint is a hinge. Its axis is an imaginary straight line through the bearing centers.

1. Select a cylindrical bearing or circular bore near A1.
2. In the Python console, inspect the selected face's surface; a true cylinder has a center/axis representation. A circle edge also exposes its center and axis.
3. Record a point on the axis and its normalized direction, in assembly coordinates.
4. Repeat for A2 through A6.
5. Check those axes against the manual p.41 diagram.
6. Establish the sign using the controller convention and observed positive motion. CAD alone does not prove the controller's positive sign.

Example console exploration after selecting one face:

```python
selection = Gui.Selection.getSelectionEx()[0]
face = selection.SubObjects[0]
print(face.Surface)
# If this is a cylinder, inspect face.Surface.Axis and face.Surface.Center.
# These properties depend on surface type; do not assume every selected face is cylindrical.
```

Do not identify a joint by the largest bolt hole. Prefer bearing axes and multiple concentric features. Geometric inference creates candidate frames, which must still be validated against the installed robot.

### 6.4 Separate rigid links and flexible accessories

Group all geometry that moves rigidly together. The base is fixed. Each rotor-side body belongs to the downstream link, while a motor housing may belong upstream. Name by physical attachment, not simply by filename.

Cylinder and rod geometry belong to the balancing mechanism. Cable models can be useful visually but do not contain their true bending, contact, or fatigue behavior. Begin with cable collision envelopes or simplified swept volumes. Do not assign their mass to two adjacent links.

Compare `CAD00` files to assembly references before including them. The workspace STEP is an envelope, not material. Counting it in the mass or collision model would be a major modeling error.

### 6.5 The most important mesh conversion: global to local

Suppose the assembly stores a point \(p_A\) in the global assembly frame. The link's frame is rotated by \(R\) and its origin is at \(t\). The local point is \(p_L\).

The assembly placement says:

\[
p_A=Rp_L+t.
\]

Subtract the translation:

\[
p_A-t=Rp_L.
\]

A rotation's inverse is its transpose, so multiply by \(R^T\):

\[
\boxed{p_L=R^T(p_A-t)}.
\]

Child explanation: first move the ruler back to the hinge, then turn the ruler to face the same way as the link. If you skip this, a link can spin around the room instead of around its hinge.

In FreeCAD, transform a copy of the assembly-space shape by the inverse link-frame placement before mesh export. A conceptual console pattern is:

```python
# assembly_shape must already include the full placement chain, exactly once.
# frame_A_L is the chosen link-frame placement in the assembly frame.
local_shape = assembly_shape.copy()
local_shape.Placement = frame_A_L.inverse().multiply(local_shape.Placement)
# Tessellate/export local_shape; preserve the original document geometry.
```

Importers can represent placements in object, container, and linked-instance layers. Inspect `Placement`, parent containers, and `getGlobalPlacement()` where supported. Applying a placement twice is as wrong as omitting it. Verify three known points against the assembly after reconstructing the local mesh in its link frame.

Export visual meshes with enough detail to recognize the robot. Export much simpler collision meshes or convex components. Small bolt threads can create huge meshes and unstable contacts without improving your engineering question.

If an STL is in millimeters, use `<mesh ... scale="0.001 0.001 0.001"/>` in URDF. If vertices were converted to meters during export, use scale 1. Never do both.

### 6.6 Reproducible CAD inspection

The provided `tools/inspect_cad.py` uses FreeCAD's Python bindings. The already generated evidence records what was inspected. To reproduce using an extracted FreeCAD AppImage, set `PYTHONPATH` to that distribution's `usr/lib` and run its own `usr/bin/python` with the script, source directory, and evidence directory. An arbitrary system Python may not match FreeCAD's compiled ABI.

The inspection outputs object relationships because summing every visible object can double-count a compound and its children. Shape centers are centers of volume under uniform density, not verified physical centers of mass.

## 7. Frames, units, and the mathematics of movement

### 7.1 A coordinate frame is three rulers

Attach three imaginary rulers at the robot base. X points along one direction, Y along a perpendicular direction, and Z along the third. A point is a list \([x,y,z]\). A vector describes a displacement or direction. A frame also has an origin and orientation.

Use a right-handed frame: point your right index finger along X and middle finger along Y; your thumb indicates Z. Positive rotation follows the curl of the right-hand fingers around the axis pointed to by the thumb.

Record frames such as `world`, `base_link`, `link_1` … `link_6`, `flange`, and `tool0`. The TCP, or tool center point, can differ from the flange and changes when the tool changes.

### 7.2 Degrees and radians

A full circle is 360 degrees or \(2\pi\) radians. Divide both by 360:

\[
1^\circ=\pi/180\ \text{rad};\quad q_{rad}=q_{deg}\pi/180.
\]

So 90° becomes \(90\pi/180=\pi/2\approx1.5708\) rad. Degrees per second convert with the same factor. Do the conversion once at the adapter boundary.

### 7.3 Where sine and cosine come from

On a circle of radius one, a point at angle \(q\) has horizontal coordinate \(\cos q\) and vertical coordinate \(\sin q\). For a link of length \(L\), multiply both coordinates by \(L\):

\[
x=L\cos q,\qquad y=L\sin q.
\]

At 0°, the point is \((L,0)\). At 90°, it is \((0,L)\). This is why those two functions appear in robot motion.

### 7.4 Derive a rotation matrix

Rotate the X unit arrow around Z by \(q\): it becomes \([\cos q,\sin q,0]^T\). Rotate the Y arrow: it becomes \([-\sin q,\cos q,0]^T\). The Z arrow stays \([0,0,1]^T\). Put those arrows in columns:

\[
R_z(q)=\begin{bmatrix}\cos q&-\sin q&0\\\sin q&\cos q&0\\0&0&1\end{bmatrix}.
\]

A point transforms by multiplying the matrix by its coordinates. The other basic rotations follow the same reasoning:

\[
R_x(q)=\begin{bmatrix}1&0&0\\0&\cos q&-\sin q\\0&\sin q&\cos q\end{bmatrix},\quad
R_y(q)=\begin{bmatrix}\cos q&0&\sin q\\0&1&0\\-\sin q&0&\cos q\end{bmatrix}.
\]

Order matters: turning a book left and then tipping it forward is generally different from tipping it first and then turning left. URDF fixed roll/pitch/yaw corresponds to \(R=R_z(yaw)R_y(pitch)R_x(roll)\).

### 7.5 Combine rotation and translation

We already have \(p_A=Rp_B+t\). Append a fourth coordinate, 1, to represent an ordinary point:

\[
\begin{bmatrix}p_A\\1\end{bmatrix}
=\underbrace{\begin{bmatrix}R&t\\0\ 0\ 0&1\end{bmatrix}}_{T_{AB}}
\begin{bmatrix}p_B\\1\end{bmatrix}.
\]

The bottom row makes the translation appear in matrix multiplication. A direction vector instead has last coordinate 0, so translation does not change it.

If \(T_{AB}\) maps B coordinates to A, and \(T_{BC}\) maps C to B, substitute the second relation into the first:

\[
p_A=T_{AB}(T_{BC}p_C)=(T_{AB}T_{BC})p_C.
\]

Therefore \(T_{AC}=T_{AB}T_{BC}\). Read the subscripts like a chain: B cancels in the middle.

The inverse is:

\[
T^{-1}=\begin{bmatrix}R^T&-R^Tt\\0&1\end{bmatrix}.
\]

That expression comes directly from the local-point derivation in Chapter 6.

### 7.6 Encoder counts to joint angle

Let an encoder produce \(N\) counts per motor revolution and let the motor turn \(G\) times per joint revolution. One joint revolution gives \(NG\) counts and equals \(2\pi\) radians. Therefore one count represents \(2\pi/(NG)\) radians.

Subtract zero count \(c_0\), and include direction sign \(s\in\{-1,+1\}\) and a frame offset \(q_0\):

\[
\boxed{q=s\frac{2\pi(c-c_0)}{NG}+q_0}.
\]

EXAMPLE: \(N=4096\), \(G=100\), and 102,400 counts above zero produce \(2\pi(102400/409600)=\pi/2\) rad. These are not ABB gear parameters. Clarify whether the encoder specification counts quadrature edges, decoded counts, or pulses. If the controller already reports joint angles, use those rather than applying this conversion a second time.

### 7.7 Velocity and acceleration

Velocity means “how much angle changed per second.” Over a small interval:

\[
\dot q_k\approx(q_k-q_{k-1})/(t_k-t_{k-1}).
\]

Acceleration means “how much velocity changed per second”:

\[
\ddot q_k\approx(\dot q_k-\dot q_{k-1})/(t_k-t_{k-1}).
\]

EXAMPLE: angle changes by 0.02 rad in 0.01 s, so speed is 2 rad/s. If it changes from 2 to 2.5 rad/s in the next 0.01 s, acceleration is 50 rad/s². That large number explains why differentiating noisy signals is dangerous: dividing a tiny noise difference by a tiny time magnifies it.

Prefer validated controller velocities if available. Otherwise filter and differentiate with actual source timestamps. Handle duplicated timestamps, gaps, encoder wrap, and multi-turn axes before computing derivatives.

## 8. Forward kinematics, Jacobians, and inverse kinematics

### 8.1 A two-link lesson before six axes

Take two flat links of lengths \(L_1,L_2\). The first link angle is \(q_1\). The elbow angle \(q_2\) is relative to the first link, so the second link's absolute angle is \(q_1+q_2\).

Add the two horizontal displacements and the two vertical displacements:

\[
x=L_1\cos q_1+L_2\cos(q_1+q_2),
\quad y=L_1\sin q_1+L_2\sin(q_1+q_2).
\]

EXAMPLE: both links are 0.5 m, shoulder 0°, elbow 90°. The first contributes \((0.5,0)\), the second \((0,0.5)\), so the tip is \((0.5,0.5)\). The ABB arm is three-dimensional, but the same “rotate, move, add” idea applies.

### 8.2 Six-axis chain

For each measured URDF joint, form the fixed zero-pose transform \(T_{fixed,i}\) and the axis rotation \(T_{axis,i}(q_i)\). Their order is:

\[
T_{i-1,i}(q_i)=T_{fixed,i}T_{axis,i}(q_i).
\]

Then:

\[
\boxed{T_{base,TCP}=T_{01}(q_1)T_{12}(q_2)\cdots T_{56}(q_6)T_{6,TCP}}.
\]

The final transform contains the tip orientation and position. Include the physical tool transform; a correct flange pose with the wrong tool length gives a wrong TCP.

Another convention, standard Denavit–Hartenberg, uses
\(T=R_z(\theta)T_z(d)T_x(a)R_x(\alpha)\), giving:

\[
\begin{bmatrix}
c_\theta&-s_\theta c_\alpha&s_\theta s_\alpha&a c_\theta\\
s_\theta&c_\theta c_\alpha&-c_\theta s_\alpha&a s_\theta\\
0&s_\alpha&c_\alpha&d\\0&0&0&1
\end{bmatrix}.
\]

Here \(c\) and \(s\) abbreviate cosine and sine. Derive it by multiplying the four elementary transforms. A DH table is not supplied for this particular installed robot, and standard and modified DH conventions differ. Do not copy a table from another ABB model. For this project, directly measured URDF frames avoid needing a guessed DH table.

### 8.3 The Jacobian is a motion sensitivity table

Ask: if joint 2 turns a tiny amount, how far does the tip move? The Jacobian stores those sensitivities.

For the two-link example, differentiate x and y:

\[
J=\begin{bmatrix}
-L_1\sin q_1-L_2\sin(q_1+q_2)&-L_2\sin(q_1+q_2)\\
L_1\cos q_1+L_2\cos(q_1+q_2)&L_2\cos(q_1+q_2)
\end{bmatrix}.
\]

The chain rule then gives \(\dot p=J\dot q\). For a 3D revolute joint with unit axis \(z_i\), joint origin \(o_i\), and tip \(p\), all expressed in one frame:

\[
J_{v,i}=z_i\times(p-o_i),\qquad J_{\omega,i}=z_i.
\]

Why? A rotating point's instantaneous velocity is angular velocity crossed with its radius from the axis. Stack the linear and angular parts into a 6×6 matrix for a six-axis arm.

A singularity is a posture where some columns become dependent: two different joint motions cannot produce independent tip motions. A fully stretched two-link arm cannot move the tip directly farther outward using an infinitesimal joint rotation. Near singularities, a tiny requested tip change can require a very large joint change.

### 8.4 Inverse kinematics

Forward kinematics asks “where does this joint posture put the tool?” Inverse kinematics asks “which posture puts the tool here?” There can be several answers, including elbow-up and elbow-down. Some requested poses have no solution.

For the flat two-link arm, let \(r^2=x^2+y^2\). The cosine rule gives:

\[
r^2=L_1^2+L_2^2+2L_1L_2\cos q_2,
\quad
\cos q_2=(r^2-L_1^2-L_2^2)/(2L_1L_2).
\]

If that value is outside [−1,1] beyond numerical tolerance, the target is unreachable. Otherwise choose \(q_2=\pm\arccos(\cdot)\), then:

\[
q_1=\operatorname{atan2}(y,x)-\operatorname{atan2}(L_2\sin q_2,L_1+L_2\cos q_2).
\]

For six-axis numerical IK, linearize the pose error \(e\): \(J\Delta q\approx e\). To limit extreme changes, minimize
\(\|J\Delta q-e\|^2+\lambda^2\|\Delta q\|^2\). Differentiate with respect to \(\Delta q\), set to zero, and solve:

\[
(J^TJ+\lambda^2I)\Delta q=J^Te.
\]

An equivalent damped form is
\(\Delta q=J^T(JJ^T+\lambda^2I)^{-1}e\). Solve linear systems numerically rather than explicitly inverting matrices. Weight translation and rotation errors using meaningful length scales; meters and radians are not interchangeable. Enforce joint limits, collision checks, and branch continuity. Run IK in simulation first.

For deeper derivations of these standard robotics concepts, use the authors' [Modern Robotics teaching materials](https://modernrobotics.northwestern.edu/nu-gm-book-resource/).

## 9. Mass, inertia, forces, and robot dynamics

### 9.1 Mass from density and volume

Density means how much mass fits in one unit of volume. If a uniform material has density \(\rho\) kg/m³ and volume \(V\) m³, divide the body into tiny pieces. Each piece has mass \(\rho\,dV\). Add them:

\[
m=\int_V\rho\,dV=\rho V\quad\text{for constant density}.
\]

One cubic millimeter is \((0.001)^3=10^{-9}\) m³, so \(V_{m^3}=10^{-9}V_{mm^3}\). EXAMPLE: 1,000,000 mm³ is 0.001 m³. At 7,850 kg/m³, that would be 7.85 kg.

Do not assign one guessed steel density to every ABB exterior solid. Motors, castings, cavities, gears, covers, and cables differ. Manufacturer CAD can simplify or fill internal space. Match a measured or documented link mass and center of mass where possible. The 1,160 kg total does not identify seven link masses; infinitely many distributions add to that total.

**CAD finding:** the supplied assembly's `LINK03_CAD` fails FreeCAD `isValid()`, and the top-level compound consequently fails too. Preserve the original. Inspect that link with Part → Check geometry and its diagnostic options, identify failing subshapes, compare the standalone LINK03 STEP, and repair a copy or obtain a corrected export. A successful tessellation is not proof that the solid is valid for volume or inertia. Record repair method, tolerances, before/after geometry differences, and new hash.

The standalone LINK03 file was also checked independently. FreeCAD reports **“Invalid imbrication of wires”**: a topological nesting problem in face-boundary wires. A standard shape-fix attempt on a transient copy, using working/minimum precision 1e-7 mm and maximum tolerance 1e-3 mm, returned false and did not restore validity. The source was untouched. See `evidence/link03_diagnosis.json` and the reproducible `tools/diagnose_link03.py`. Do not keep increasing repair tolerance until a check turns green; that can change engineering geometry. Inspect the reported faces or request a corrected manufacturer export.

### 9.2 Center of mass

A heavy piece pulls the balance point toward itself. For point masses:

\[
c=\frac{\sum_i m_i r_i}{\sum_i m_i}.
\]

This follows from balancing first moments: total mass times its representative position must equal the sum of each mass times its position. For continuous density:

\[
c=\frac1m\int_V r\rho(r)\,dV.
\]

EXAMPLE: a 2 kg part at x = 0 and a 1 kg part at x = 0.3 m have center \((2\cdot0+1\cdot0.3)/3=0.1\) m. All positions must use the same frame.

### 9.3 Rotational inertia

It is harder to spin a mass when it is far from the axis. The inertia around Z is:

\[
I_z=\int(x^2+y^2)\,dm.
\]

The full tensor is

\[
I=\int\left((r^Tr)I_3-rr^T\right)dm.
\]

Thus \(I_{xx}=\int(y^2+z^2)dm\) and \(I_{xy}=-\int xy\,dm\), with analogous entries. The off-diagonal sign matters: URDF stores tensor entries, not unsigned products of inertia.

For a uniform slender rod centered at zero, \(dm=(m/L)dx\). About an axis perpendicular to the rod:

\[
I=\frac mL\int_{-L/2}^{L/2}x^2dx
=\frac mL\left[\frac{x^3}{3}\right]_{-L/2}^{L/2}=\frac{mL^2}{12}.
\]

Translate the reference axis by vector \(d\). Expanding the squared distances makes cross terms vanish at the center of mass, giving the parallel-axis theorem:

\[
I_O=I_C+m[(d^Td)I_3-dd^T].
\]

Rotate the tensor into a different frame using \(I'=RI R^T\). A tool's inertia cannot be copied unchanged from a differently oriented CAD frame.

FreeCAD shape inertia is geometric unless mass/density has been applied. Unit-density geometric second moments have length-to-the-fifth units. For mm geometry and density in kg/mm³, multiply by density and then convert mm² to m² by \(10^{-6}\); equivalently multiply a geometric mm⁵ tensor by density in kg/m³ and \(10^{-15}\). Confirm the exact API's units and test against an analytic box before using it. A mass inertia already in kg·mm² only needs the \(10^{-6}\) conversion. Mixing these cases causes enormous errors.

URDF expects inertia about the center of mass in the inertial frame. Check positive mass, symmetric tensor, positive eigenvalues, and physical principal-moment triangle inequalities. Sum component tensors with proper rotations and parallel-axis shifts.

### 9.4 Force and torque

Newton's law is \(F=ma\): more mass or more acceleration needs more force. Torque is the turning effect of force:

\[
\tau=r\times F;\qquad |\tau|=rF\sin\theta.
\]

For gravity acting perpendicular to a horizontal lever, \(\tau=mgr\). EXAMPLE: 10 kg at 0.2 m gives \(10\cdot9.81\cdot0.2=19.62\) N·m. Moving the same load twice as far away doubles its torque. Payload mass alone is therefore insufficient.

For one rotating inertia, \(\tau=I\alpha\). This is the rotational counterpart of \(F=ma\).

### 9.5 Derive the six-axis dynamics equation

For each link's center-of-mass velocity \(v_i\) and angular velocity \(\omega_i\), the kinetic energy is:

\[
K_i=\tfrac12m_i v_i^Tv_i+\tfrac12\omega_i^TI_i\omega_i.
\]

Use the link Jacobians: \(v_i=J_{v,i}\dot q\), \(\omega_i=J_{\omega,i}\dot q\). Substitute and collect terms:

\[
K=\tfrac12\dot q^TM(q)\dot q,
\quad M=\sum_i(m_iJ_{v,i}^TJ_{v,i}+J_{\omega,i}^TI_iJ_{\omega,i}).
\]

Each tensor must be expressed consistently with its angular Jacobian. Potential energy for Z upward and gravitational magnitude g is \(U=\sum_i m_i g z_i(q)\). Define \(L=K-U\). The Euler–Lagrange equation is:

\[
\frac d{dt}\frac{\partial L}{\partial\dot q_i}-\frac{\partial L}{\partial q_i}=\tau_i+\tau_{external,i}.
\]

Substituting K and U gives, with a defined friction model:

\[
\boxed{M(q)\ddot q+C(q,\dot q)\dot q+g(q)+\tau_f
=\tau_{act}+J(q)^TF_{external}+\tau_{balance}}.
\]

Here M represents inertia, C represents velocity-dependent coupling, g represents gravity, and \(\tau_f\) represents friction. The balancing mechanism is explicit because this ABB assembly includes cylinder/rod geometry. A common consistent expression for the coupling vector is

\[
[C\dot q]_i=\sum_{j,k}\tfrac12
(\partial M_{ij}/\partial q_k+\partial M_{ik}/\partial q_j-\partial M_{jk}/\partial q_i)
\dot q_j\dot q_k.
\]

You do not need to hand-code this for production; use a verified dynamics library. The derivation tells you what parameters and assumptions the library requires. An attractive CAD rendering cannot fill those inputs.

The external-force relation \(\tau_{external}=J^TF\) follows from work: \(F^T\delta x=\tau^T\delta q\), and \(\delta x=J\delta q\). Substitute and compare coefficients.

### 9.6 Friction and motor current

A simple friction model is \(\tau_f=b\dot q+\tau_c\operatorname{sign}(\dot q)\). The first term grows with speed; the second approximately opposes motion. Near zero speed, stiction and more detailed friction models may be necessary.

An ideal motor has \(\tau_m=K_t i\). With a transmission, an initial approximation is \(\tau_{joint}\approx\eta G K_t i\), where G is reduction ratio and \(\eta\) efficiency. Back-driving efficiency, acceleration, sensor offsets, and friction complicate this. Do not label a measured current as a verified joint torque without identifying these terms.

### 9.7 Elasticity: why a loaded arm can bend

Rigid-body kinematics assumes links do not bend. Real materials stretch and bend slightly. Stress is force divided by loaded area, \(\sigma=F/A\), in pascals. Strain is fractional extension, \(\epsilon=\Delta L/L\), with no unit. In the small-elastic-strain regime, Young's modulus E relates them: \(\sigma=E\epsilon\). Substitute both definitions and solve:

\[
\Delta L=FL/(AE).
\]

EXAMPLE: a straight bar under 1,000 N tension, length 1 m, cross-section 0.001 m², and E = 200 billion Pa stretches \(1000/(0.001\cdot200\times10^9)=0.000005\) m, or 0.005 mm. These are teaching values, not ABB material assignments.

For a simplified horizontal cantilever beam with end load F, bending moment at coordinate x from the fixed end is \(M(x)=F(L-x)\). Small-deflection beam theory gives \(EI_A y''(x)=M(x)\), where \(I_A\) is the **area** second moment, in m⁴, different from mass inertia in kg·m². Integrate twice with fixed-end conditions \(y(0)=y'(0)=0\):

\[
y'(x)=\frac F{EI_A}(Lx-x^2/2),\qquad
 y(x)=\frac F{EI_A}(Lx^2/2-x^3/6).
\]

At the tip, \(\delta=FL^3/(3EI_A)\). Doubling length multiplies this simplified deflection by eight. A real robot also has gearbox, bearing, and joint compliance; an exterior solid plus guessed modulus cannot reproduce that stiffness.

For a small joint deflection model with joint stiffness matrix \(K_q\), \(\delta q=K_q^{-1}\tau\). Substitute \(\tau=J^TF\) and \(\delta p=J\delta q\):

\[
\delta p=J K_q^{-1}J^T F.
\]

This gives a local Cartesian compliance approximation under explicit assumptions. Identify stiffness from controlled loading and measurement. For detailed structural analysis, use FreeCAD FEM with an open-source solver such as CalculiX, validated material properties, boundary conditions, mesh convergence, and load cases. An FEM image with colors is not validation by itself.

### 9.8 Thermal conductivity is different from thermal capacity

Thermal capacity says how much heat raises temperature. Conductivity says how easily heat travels through material. Fourier's one-dimensional law is \(P=-kA\,dT/dx\). For a uniform slab of thickness L between temperatures \(T_h,T_c\), integrate a constant gradient to obtain \(P=kA(T_h-T_c)/L\). Rearranging gives a conductive thermal resistance \(R_{th}=L/(kA)\). Contact interfaces, convection, and radiation add other effects; a single fitted resistance can summarize them only over its validated conditions.

## 10. ABB load diagrams and the balancing mechanism

### 10.1 Use the exact variant's diagrams

Manual pp.73 onward explain the loading context; p.75 provides the standard 240/2.65 diagram and p.76 a special near-vertical-wrist case. Full A5 movement inertia limits are on p.91; limited movement has different figures on p.92. Do not treat a special wrist-down overload case as the general robot rating.

For the standard variants with full A5 movement, p.91 specifies:

\[
L=\sqrt{X^2+Y^2},
\quad J_{a5}=m(Z+0.2)^2+\max(J_{0x},J_{0y})\le250\ \mathrm{kg\,m^2},
\]

\[
J_{a6}=mL^2+J_{0z}\le185\ \mathrm{kg\,m^2}.
\]

These are manufacturer loading criteria for the stated geometry and conditions. The offsets and limits are supplied by ABB; they are not universal mechanics constants. Their form follows the parallel-axis theorem: center-of-mass inertia plus mass times squared offset.

EXAMPLE only: a tool plus workpiece totals 100 kg, X = 0.1 m, Y = 0, Z = 0.3 m, and its CoM inertias are 2, 3, 1 kg·m². Then L = 0.1 m,
\(J_{a5}=100(0.5)^2+3=28\), and
\(J_{a6}=100(0.1)^2+1=2\) kg·m². These pass those two numerical inequalities, but that is not a complete load approval: mass/CoM load diagrams, arm loads, orientation restrictions, equipment, duty cycle, installed options, and current manufacturer instructions also apply.

Tool and workpiece must be combined using weighted centers and shifted tensors. The p.103 stopping-test `tooldata` values describe the test conditions; they are not measurements of your tool.

### 10.2 Model the cylinder and rod as a mechanism

A cylinder in the CAD does not imply that its internal pressure, spring law, or control interface is known. Identify the actual balancing mechanism from the appropriate manipulator manual or inspection.

If a fixed attachment is \(a\) and a moving attachment is \(b(q)\), the separation is:

\[
\ell(q)=\|b(q)-a\|.
\]

Take the dot product to see why: distance squared is
\((b_x-a_x)^2+(b_y-a_y)^2+(b_z-a_z)^2\), and square root gives length.

Let n be the unit vector from a to b. Then \(\partial\ell/\partial q=n^T\partial b/\partial q\). A force F acting to increase length does work \(\delta W=F\delta\ell\). Therefore:

\[
\tau_{balance}=F(\ell)\frac{\partial\ell}{\partial q}.
\]

For a conservative spring, this is also \(-\partial U_{spring}/\partial q\). If a model uses \(F=k(\ell_0-\ell)\), k and preload length \(\ell_0\) must be identified. A gas spring needs a different law. Omit unknown force laws from a visualization model, and mark dynamics incomplete.

URDF is a tree and cannot directly close a mechanical loop. Use a visual attachment approximation for the first twin; for dynamics, model the closure in SDF/Gazebo constraints or reduce the passive mechanism analytically to its joint torque. A `mimic` joint encodes a linear relation, not an arbitrary cylinder-length function.

## 11. Time, sampling, networking, and reliability

### 11.1 There are several different clocks

* **Source time:** when the sensor/controller measured the value.
* **Receipt time:** when your software received it.
* **Monotonic time:** a local elapsed-time clock that does not jump with wall-clock correction.
* **Simulation time:** the simulator's clock; it may pause or run slower than real time.

Use UTC epoch timestamps for cross-system records, monotonic time for local timeouts, and ROS simulation time only for explicitly simulated streams. Do not put simulation timestamps in a physical robot stream.

A printed timestamp with nine digits after the second does not guarantee nanosecond accuracy. Precision is the number of digits; accuracy is how close the time is to the truth. Record clock uncertainty and synchronization state.

### 11.2 Derive the sampling rate

If a signal repeats at frequency f, one cycle lasts \(T=1/f\). To distinguish a band-limited sinusoid from lower-frequency aliases, sampling must exceed twice its highest frequency. Real systems also need an analog anti-alias filter and transition-band margin.

EXAMPLE: a 4 kHz vibration band suggests a sampling rate above 8 kHz, with practical margin such as 12.8 kHz after filter design. Temperature changing over seconds does not need 12.8 kHz sampling.

Robot poses at 100 Hz have 10 ms spacing because \(1/100=0.01\) s. That is a monitoring rate, not a claim that the physical servo controller runs at 100 Hz.

### 11.3 Latency and freshness

A useful latency budget is:

\[
D=D_{acquire}+D_{transport}+D_{queue}+D_{process}+D_{render}.
\]

EXAMPLE target allocation: 10 + 5 + 5 + 10 + 20 = 50 ms. This is an initial budget, not a measured result. At 100 Hz, acquisition phase alone can add almost 10 ms. Measure distributions, especially p95 and p99, under realistic load; average delay hides occasional old frames.

Freshness is source age \(a=t_{now}-t_{source}\). If clock uncertainty is \(\epsilon\), the true age is uncertain by roughly that amount. For conservative gating use \(a+\epsilon\). A packet can arrive now and still contain a ten-second-old measurement. Test both source age and receipt timeout.

The lab uses a 250 ms stale threshold and flags excessive clock uncertainty. Those are teaching defaults. For production, configure thresholds from process requirements and reject model/asset mismatches as well.

Clock skew also becomes position error: at constant speed v, \(\Delta x=v\Delta t\). At 1 m/s and 5 ms mismatch, the apparent error is 5 mm. Do not blame the robot for a timestamp error.

### 11.4 Clock synchronization

Start with chrony on the edge and historian, using the same approved time sources. Inspect `chronyc tracking` and `chronyc sources -v`, log offset/uncertainty, and test recovery from time-source loss. See [chrony configuration](https://chrony-project.org/doc/4.6/chrony.conf.html).

For tighter requirements, evaluate PTP using LinuxPTP plus NIC hardware timestamping and a compatible switch/time source. PTP software alone does not guarantee microsecond alignment. The robot controller may have a separate time domain that your PC's chrony does not discipline. Map controller time into the common timeline and document the uncertainty.

### 11.5 Bandwidth and storage, with arithmetic

For f messages per second, B bytes per message, and protocol overhead factor h:

\[
R_{bytes/s}=fBh,\qquad R_{bits/s}=8fBh.
\]

EXAMPLE: 250 Hz × 800 bytes × 1.5 = 300,000 bytes/s, or 2.4 Mbit/s. Measure serialized packet size; JSON contains names and punctuation as well as numbers.

Daily raw payload storage is:

\[
S_{day}=fB\cdot86400.
\]

Without the network overhead factor, 250 × 800 × 86,400 = 17,280,000,000 bytes/day, about 17.28 decimal GB. Thirty days is 518.4 GB before database row overhead, indexes, replicas, or backups. Compression can reduce it; do not assume a ratio before testing.

A 3-axis accelerometer at 12,800 samples/s with 4 bytes/channel generates
\(3\cdot12800\cdot4=153600\) bytes/s, or about 13.27 GB/day before metadata. Multiple sensors multiply the requirement.

Plan hot retention for raw data, longer retention for summaries, and event-triggered waveform preservation. Keep backups on a separate device and test restoration.

### 11.6 MQTT and delivery behavior

MQTT QoS 0 can drop messages. QoS 1 retries and can deliver duplicates. QoS 2 has more overhead and does not make an entire sensor-to-database application magically exactly once. Use an application identity `(robot_id, stream_id, seq)` for idempotent storage.

A new boot/session gets a new stream ID. The sequence counts upward inside that session. Detect missing sequence intervals, duplicates, and late records. Archive late packets if useful, but do not let them move the live displayed state backward. Separate asset/session channels prevent a late prior-session packet from replacing the current state.

Use non-retained high-rate measurements, explicit freshness checks, and a last-will/heartbeat for availability. A retained state value is not evidence that the robot is still online. Broker persistence is not an edge outage buffer: the edge adapter needs its own bounded durable queue and replay policy.

Use TLS and separate topic permissions. An adapter should publish observations, a historian should subscribe, and the visualization should not have robot-command permissions. The Mosquitto configuration reference documents authentication, access control, and TLS: [Mosquitto configuration](https://mosquitto.org/man/mosquitto-conf-5.html).

## 12. Telemetry contracts and controller integration

### 12.1 Agree on a message before connecting hardware

A contract tells every program what a message means. A bare list like `[10,20,30]` is ambiguous: degrees or radians? Which axes? When measured? Real or simulated? Which calibration?

The local contract is illustrated by `config/telemetry.example.json` and validated in `tools/twin_lab.py`:

```json
{
  "schema_version": 1,
  "robot_id": "irb6720_cell01",
  "stream_id": "new-uuid-on-adapter-session",
  "model_revision": "irb6720-measured-v1",
  "source": "physical",
  "seq": 0,
  "source_time_ns": 0,
  "clock_uncertainty_ms": 2.0,
  "joint_names": ["joint_1","joint_2","joint_3","joint_4","joint_5","joint_6"],
  "q": [0,0,0,0,0,0],
  "dq": null,
  "tau": null,
  "temperature": null,
  "mode": "idle",
  "quality": "uncertain",
  "units": {"q":"rad","dq":"rad/s","tau":"N*m","temperature":"degC"}
}
```

This is a format example, not a captured physical sample; the zero timestamp and uncertain quality deliberately make it unsuitable as live state. Unknown optional channels are `null`, not invented zeros. Position q is required. A missing temperature is different from a temperature of 0°C. Add per-sensor timestamps and per-channel quality in a versioned schema when channels are acquired independently. Do not pretend asynchronously read temperatures and positions were captured simultaneously.

Asset identity, model revision, and source type must match the intended physical display. The teaching Store's duplicate/out-of-order logic is deliberately simpler than a production multi-asset session manager; do not mix multiple assets or live and replay sources into a single unconfigured displayed-state stream. Enforce active session changes in a production adapter.

Nanosecond epoch integers can exceed JavaScript's exact integer range. Python and PostgreSQL bigint preserve them here. A production browser-facing contract should transmit those timestamps as decimal strings, or split seconds and nanoseconds. The lab's Python server computes ages before sending them to the browser, so it does not rely on exact browser nanosecond arithmetic.

### 12.2 ABB-specific connection boundary

The product specification confirms OmniCore context but not your installed API version, credentials, options, or exact sensor availability. ABB's official [Robot Web Services documentation](https://robotwebservices.robotics.abb.com/?resourceVersion=rw7) separates RobotWare versions. Match the actual controller release. Do not use an IRC5/RobotWare 6 client and assume OmniCore compatibility.

An existing open-source Python client, [abb_robot_client](https://github.com/rpiRobotics/abb_robot_client), describes itself as an IRC5 RWS/EGM client. It is useful prior art; that description is not evidence that it supports your OmniCore release. The baseline therefore uses an adapter contract rather than shipping a falsely universal ABB driver.

Recommended connection sequence:

1. Read the installed controller's version and interface/options list using the site's established tools or controller information screens.
2. Open the corresponding official RWS API documentation.
3. Identify the supported read-only mechanical-unit joint-position resource and subscription mechanism. Confirm whether values are measured, target, or planned positions.
4. Use a dedicated read-only account and verified HTTPS certificates. Do not disable TLS verification to make an example work.
5. Capture a stationary response and record its format and units.
6. Map A1…A6 to `joint_1`…`joint_6`, convert degrees to radians once, and timestamp appropriately.
7. Measure achieved interval, jitter, age, and loss over at least one representative operating period.
8. If source measurement time is absent, record acquisition interval bounds and label the estimated time/uncertainty. An HTTP response arrival time is not the exact sensor acquisition time.
9. Keep unsupported torque, temperature, and fault channels unavailable until documented sources exist.

RWS request/response timing should not be advertised as deterministic millisecond streaming. If the application requires higher-rate data, investigate the installed controller's supported streaming facilities and licensing. EGM is a motion-related interface requiring controller-side setup; do not enable or drive it merely to animate a dashboard. No physical command code is included here.

If the factory already exposes OPC UA, an adapter based on [open62541](https://open62541.org/) is an open-source alternative. Its availability on the edge does not mean the ABB controller automatically contains an OPC UA server.

### 12.3 Local MQTT exercise

After installing Mosquitto and its clients on a learning machine:

```bash
mosquitto -c config/mosquitto-local.conf
```

In a second terminal:

```bash
mosquitto_sub -h 127.0.0.1 -p 18883 -t factory/cell01/irb6720/observed/state -q 1
```

In a third terminal:

```bash
python3 tools/twin_lab.py generate --count 10 --output /tmp/mqtt-lesson.jsonl
mosquitto_pub -h 127.0.0.1 -p 18883 -t factory/cell01/irb6720/observed/state -q 1 -l < /tmp/mqtt-lesson.jsonl
```

`-l` publishes each input line as a separate message. The provided listener is intentionally restricted to loopback and is anonymous for this local exercise. For a cell-network broker, provision certificates, password users, storage ownership, and topic permissions using the production templates. Test that unauthorized subscription/publication fails. The templates will not start correctly until their site-specific paths and files exist.

### 12.4 Convert normalized physical data to ROS

On the ROS workstation, after sourcing ROS and implementing the verified controller adapter:

```bash
python3 tools/jsonl_to_ros.py --robot-id irb6720_cell01 --model-revision irb6720-measured-v1 < /tmp/normalized-physical.jsonl
```

For a live stream, pipe the observational adapter's JSONL output instead of using a finite file. This bridge validates identity, units, names, quality, sequence, and source age before publishing. It publishes only `sensor_msgs/JointState`; it sends no robot motion commands. Velocity and effort remain empty when unavailable.

The bridge is a starter, not a complete station service: production needs process supervision, explicit active-session handling, metrics, a source-time mapping, bounded queues, and a stale-state overlay. RViz can keep the last posture after a publisher stops; the status panel must independently mark that posture stale.

## 13. ROS 2, RViz, and Gazebo

### 13.1 Install a matching software environment

Use a separate Ubuntu 24.04 machine, partition, or appropriate VM if the current host is another distribution. Do not mix Ubuntu package sources into another distribution. FreeCAD's AppImage and the Python-only lab can run independently of ROS.

Follow the official [ROS Jazzy installation instructions](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html) to configure locale and the ROS apt repository. If the website blocks automated access, the matching [official source](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Installation/Ubuntu-Install-Debs.rst) and its repository-setup include are readable. Use the official `ros2-apt-source` package for keys and repository configuration, and record the package version installed.

Once that repository is installed on Ubuntu 24.04:

```bash
sudo apt update
sudo apt install ros-jazzy-desktop ros-jazzy-xacro ros-jazzy-joint-state-publisher-gui ros-jazzy-robot-state-publisher ros-jazzy-ros-gz ros-jazzy-gz-ros2-control ros-jazzy-ros2-controllers liburdfdom-tools
source /opt/ros/jazzy/setup.bash
```

Install optional MoveIt only when planning is needed. Record package versions in an environment manifest; avoid silently upgrading a validated twin.

These are setup instructions, not a claim that this workstation's ROS/Gazebo dependencies were installed or tested during guide preparation.

### 13.2 Understand the URDF before typing it

A `link` is one rigid body. A `joint` connects a parent link to a child link. Its origin is the child/joint zero frame expressed in the parent frame. Its axis is expressed in that joint frame.

Example, invented dimensions:

```xml
<joint name="joint_2" type="revolute">
  <parent link="link_1"/>
  <child link="link_2"/>
  <origin xyz="0.32 0 0.7" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.134464" upper="1.483530" effort="1" velocity="1.570796"/>
</joint>
```

The origin here is **EXAMPLE**, not a verified ABB shoulder transform. `effort="1"` is a parser placeholder for a visual lesson, not an ABB torque rating. The real dynamics model must have identified torque limits. Published joint ranges assume your chosen q coordinates align with ABB joint coordinates; if zero offsets or signs differ, transform the limits too.

Add a mesh to a link only after converting it to that link's local frame:

```xml
<visual>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry><mesh filename="file:///absolute/path/link_2.stl" scale="0.001 0.001 0.001"/></geometry>
</visual>
```

That scale applies only to a millimeter STL. A portable ROS package uses a `package://.../meshes/...` URI after packaging the assets. Add a separate simple collision element, and add real inertial properties only after their validation.

### 13.3 Make the first frame display work

1. Generate `/tmp/example_arm.urdf` using `--demo`.
2. Check it with `check_urdf /tmp/example_arm.urdf`.
3. Start `robot_state_publisher` with that description.
4. Start `joint_state_publisher_gui` to move the teaching joints.
5. Open RViz, set Fixed Frame to `world`, and add RobotModel and TF displays.
6. Move one joint at a time and inspect the frame arrows. A parent move must carry all downstream links.

Typical ROS command pattern for the small generated example:

```bash
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(cat /tmp/example_arm.urdf)"
```

In another sourced terminal:

```bash
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

Then `rviz2` in a third. Large descriptions are better passed through a launch file rather than a shell argument.

For the measured physical model, do not run the GUI publisher on the same joint topic as the observational adapter. Remap `robot_state_publisher`'s joint input to `/physical/irb6720/joint_states`, load the measured URDF, and retain a separate freshness indicator.

### 13.4 From visual model to physics model

Before Gazebo, finish these inputs: mass, CoM, inertia, collision shapes, joint damping/friction, limits, tool payload, gravity direction, and balancing-mechanism strategy. A visually convincing model with guessed inertia is unsuitable for force or failure predictions.

Use the `gz_ros2_control` integration that matches Jazzy/Harmonic. The official package documentation shows the `<ros2_control>` block, Gazebo plugin, and controller-manager setup: [gz_ros2_control Jazzy](https://control.ros.org/jazzy/doc/gz_ros2_control/doc/index.html).

A complete experiment requires:

1. A world with gravity and a fixed robot base.
2. A physics-valid robot description or SDF.
3. A matching Gazebo ros2_control system plugin and joint command/state interfaces.
4. A joint-state broadcaster and a simulated trajectory controller.
5. Controller spawning after the model and controller manager are ready.
6. A small simulated trajectory that respects limits.
7. Recording of states, command references, forces, timestamps, and model version.

Do not claim this package supplies a commissioned ABB Gazebo model: it supplies the route and a visual-description helper; measured dynamics and controller integration remain commissioning work.

### 13.5 Simulation speed is not clock accuracy

Let simulated elapsed time be \(\Delta t_s\) and wall time be \(\Delta t_w\). The real-time factor is
\(RTF=\Delta t_s/\Delta t_w\). If a one-second simulation takes two real seconds, RTF = 0.5. Use smaller collision models, benchmark step size, and reduce rendering load before assuming a larger GPU solves it. Tight physics steps can be CPU-limited.

To compare simulation with hardware, align timestamps and interpolate onto a common time grid. Do not continuously overwrite simulator positions with measurements and then claim the simulator predicted those same positions. Maintain an independent expected trajectory/model when evaluating prediction error.

## 14. Historical storage, dashboards, and enterprise context

### 14.1 Why not just one long CSV?

CSV is useful for exports, but relational tables make relationships explicit: this sample came from this robot, with this model revision, during this job, after this maintenance event.

The provided `sql/schema.sql` creates assets, model revisions, telemetry, maintenance, faults, production runs, and analytics results. Telemetry's primary key deduplicates `(robot_id, stream_id, seq)`. Foreign keys prevent accidental references to nonexistent assets and model revisions.

The baseline is intentionally ordinary PostgreSQL, with no proprietary extension required. High data volumes may justify partitioning, batching, compression, or chunked waveform files. Preserve deduplication semantics when designing partition keys.

### 14.2 Local PostgreSQL exercise

On a learning Ubuntu host with PostgreSQL installed:

```bash
sudo -u postgres createuser --pwprompt twin_lab
sudo -u postgres createdb --owner=twin_lab twin_lab
psql -h 127.0.0.1 -U twin_lab -d twin_lab -f sql/schema.sql
```

Enter credentials interactively. Use a protected password file or local authentication policy rather than putting passwords into shell history. For production, the database owner, ingestion role, dashboard reader, and maintenance editor should be different roles.

Insert the teaching asset and example model, making the unmeasured state explicit:

```sql
INSERT INTO asset(robot_id,manufacturer,variant)
VALUES ('teaching_arm','example','synthetic six-joint signals');
INSERT INTO model_revision(revision,robot_id,cad_sha256,validation_state)
VALUES ('EXAMPLE-NOT-MEASURED-v1','teaching_arm','not-applicable-synthetic','example');
```

Create a Python virtual environment, install the open-source `psycopg` driver, and record its installed version:

```bash
python3 -m venv /tmp/irb-twin-db-venv
source /tmp/irb-twin-db-venv/bin/activate
pip install 'psycopg[binary]>=3,<4'
export TWIN_DATABASE_DSN='host=127.0.0.1 dbname=twin_lab user=twin_lab'
python3 tools/twin_lab.py generate --count 100 --output /tmp/db-lesson.jsonl
python3 tools/ingest_postgres.py < /tmp/db-lesson.jsonl
```

The DSN contains no password; provide authentication through the site's chosen protected mechanism. Reimport the file and check that the row count does not double. This verifies the database deduplication boundary, not end-to-end MQTT crash recovery.

`mosquitto_sub ... | python3 tools/ingest_postgres.py` is a useful learning connection. It is not a durable production transaction pipeline: MQTT acknowledgment can happen before the database commits. A production consumer needs explicit acknowledgment after durable storage, appropriate persistent session behavior, backpressure, an edge spool, and restart testing.

### 14.3 Build Grafana panels

Install the OSS distribution, add a PostgreSQL data source with a read-only role, and use `sql/dashboard_queries.sql` as starting queries.

Create panels for:

* Six joint positions with units and fixed joint ordering.
* Temperature trends and ambient temperature.
* Source age, sequence gaps, invalid-message count, and clock uncertainty.
* Active/idle/fault timeline.
* Maintenance and job annotations.
* Model revision, tool revision, payload, and validation status.
* Residual trends conditioned on the same job and operating regime.

Do not label “no data” as healthy. An alert must have an explicit behavior for no data, stale data, bad quality, and application failure. A flat line can mean a stationary robot or a disconnected sensor; freshness distinguishes them.

### 14.4 Interoperability without semantic confusion

Use stable asset IDs across SCADA, maintenance, ERP, and PLM. Exchange documented JSON or CSV records, or use a suitable open API. Preserve source document IDs and revisions rather than copying a part description into an unrelated field.

Examples: a production system supplies `run_id` and expected payload; maintenance supplies component replacement dates; the model registry supplies CAD and calibration hashes. A temperature increase following a payload change has a different meaning from the same increase under unchanged loading.

Record time zone on imported business schedules and convert event times to UTC. Keep original source values for audit. Use New York local time for the operator's display if desired, while calculations use a common timeline.

## 15. Thermal, vibration, and condition monitoring

The added browser lesson `/vibration.html` provides a two-inertia torsional model with editable assumptions and checked time/frequency responses. Continue to `/maintenance.html` for sourced service intervals and qualitative fault-tree scenarios. See `VIBRATION_AND_MAINTENANCE.md` for derivations, validation boundaries, and the independently retrieved ABB product manual Revision N provenance. These additions do not constitute a calibrated ABB vibration model.

### 15.1 Start with a baseline, not artificial intelligence

A model needs a meaningful comparison. Record known operating conditions: same program, payload, tool, speed, ambient temperature, and warm-up state. Mark periods of maintenance or known faults. A model trained on mixed conditions can interpret normal job changes as faults.

A **residual** is a measured value minus its predicted value:

\[
r(t)=y_{measured}(t)-y_{predicted}(t).
\]

For example, if the thermal model predicts 43°C and the sensor measures 48°C, the residual is +5°C. It is a reason to investigate the model or machine, not proof of bearing failure.

### 15.2 A beginner thermal model, derived

Heating a body stores energy \(E=C\Delta T\), where thermal capacity \(C=mc_p\) has units J/K. Differentiating gives stored-power rate \(C\dot T\).

Suppose electrical/mechanical losses provide heat power \(P_{loss}\). Approximate heat leaving to ambient as \((T-T_a)/R_{th}\), with thermal resistance \(R_{th}\) in K/W. Energy in minus energy out equals energy stored:

\[
\boxed{C\dot T=P_{loss}-(T-T_a)/R_{th}}.
\]

At steady temperature, \(\dot T=0\), so \(T_\infty=T_a+R_{th}P_{loss}\). With constant loss and ambient, separate variables to obtain:

\[
T(t)=T_\infty+[T(0)-T_\infty]e^{-t/(R_{th}C)}.
\]

The time constant is \(\tau_{th}=R_{th}C\). After one time constant, the gap to final temperature falls to \(e^{-1}\approx0.368\), meaning about 63.2% of the change has occurred.

EXAMPLE: \(R_{th}=0.5\) K/W, \(C=1000\) J/K, loss 20 W, ambient 25°C. Final temperature is 35°C and the time constant is 500 s. Starting at 25°C, after 500 s the model predicts \(35-10e^{-1}\approx31.32\)°C. These are invented values; identify the actual thermal parameters from time-aligned heating/cooling data.

A forward-Euler update is
\(T_{k+1}=T_k+\Delta t[P_{loss}-(T_k-T_a)/R_{th}]/C\).
For this simple linear model, numerical stability requires \(0<\Delta t<2R_{th}C\); accurate integration usually uses a much smaller step. Exact exponential discretization is preferable when inputs are constant over a sample interval.

Motor copper loss is approximately \(i^2R_e\), derived from electrical power \(P=Vi\) and Ohm's law \(V=iR_e\). It is only one heat source. Resistance changes with temperature; external sensor surface temperature can lag internal winding temperature.

### 15.3 Vibration: RMS and frequency content

First decide whether you want total acceleration RMS or vibration after removing gravity/DC. A stationary accelerometer can read about 9.81 m/s² along a vertical axis; that is not a vibration defect.

For samples \(a_k\), mean is \(\bar a=\sum a_k/N\). Remove the mean when appropriate: \(x_k=a_k-\bar a\). The RMS is:

\[
x_{RMS}=\sqrt{\frac1N\sum_{k=0}^{N-1}x_k^2}.
\]

Why square? Positive and negative movement should not cancel. Why square root? Squaring changes units to acceleration squared; the root restores acceleration units. A sinusoid of amplitude A has RMS \(A/\sqrt2\), because the average of \(\sin^2\) over a full cycle is 1/2.

To inspect frequency content, compare the signal to sinusoids at discrete frequencies:

\[
X_j=\sum_{k=0}^{N-1}x_k e^{-i2\pi jk/N},\qquad f_j=jf_s/N.
\]

That is the discrete Fourier transform; an FFT computes it efficiently. The frequency-bin spacing is \(\Delta f=f_s/N\). At 12,800 Hz with 12,800 samples, the record spans one second and spacing is 1 Hz. Longer windows improve spacing but delay the result.

Use a suitable window such as Hann, correct amplitude/PSD normalization, and respect anti-aliasing. Bearing-specific defect frequencies require bearing geometry and rotational speed. Gear mesh frequencies require gear tooth counts and shaft speed. The exterior STEP model does not supply these hidden parameters.

### 15.4 Thresholds and persistence

A simple standardized residual is
\(z=(r-\mu_r)/\sigma_r\), where \(\mu_r\) and \(\sigma_r\) come from a matched healthy baseline. This measures how many baseline standard deviations a residual is from its usual value. When \(\sigma_r\) is nearly zero, use a justified noise floor; do not divide by zero.

For smoothing, use
\(s_k=\alpha r_k+(1-\alpha)s_{k-1}\), with \(0<\alpha\le1\). This is a weighted average of new evidence and previous evidence. A common time-constant choice is \(\alpha=1-e^{-\Delta t/\tau}\); when sample intervals vary, recompute using actual \(\Delta t\).

EXAMPLE policy: flag an advisory when a residual exceeds a documented threshold for ten seconds under comparable operating conditions. Record the reason, model version, input quality, and operating context. Choose thresholds from false-alarm and missed-detection costs, not an arbitrary “3 sigma means broken” rule.

### 15.5 What AI can and cannot add

An anomaly detector can learn patterns of temperature, load, speed, and vibration. A useful progression is simple thresholds, then contextual residuals, then an explainable multivariable model. A remaining-useful-life estimate requires degradation/failure histories and a defined failure criterion; a few minutes of healthy data do not establish it.

Split training and evaluation by time and preferably machine/run groups. Randomly shuffling adjacent samples leaks nearly identical operating data into both sets and exaggerates performance. Compare against a simple baseline and evaluate false alarms per operating hour, fault detection delay, and performance under job changes. A surrogate is a fast approximation to an identified model; validate its domain and flag extrapolation.

## 16. Calibration, uncertainty, and validation

### 16.1 Calibrate one layer at a time

1. **Identity:** verify exact robot variant, options, mounting, tool, and payload.
2. **Scale:** verify CAD length conversion against drawing dimensions.
3. **Base frame:** align mounting plane and A1 centerline to the physical cell's reference frame.
4. **Joint axes and signs:** compare isolated permitted joint observations with the candidate frames.
5. **Zero offsets:** match controller angles to the CAD reference posture.
6. **Tool transform:** measure the TCP relative to the flange using an appropriate tool-calibration procedure.
7. **Timing:** quantify source-time mapping, source age, jitter, and missing data.
8. **Kinematics:** compare measured TCP positions/orientations over varied postures.
9. **Dynamics:** validate static gravity/loading behavior before accelerating simulated mechanisms.
10. **Analytics:** establish healthy baselines and independent evaluation data.

Never compensate for a wrong joint frame by arbitrarily moving the visual mesh until one posture looks right. It may fit that posture and fail all others.

### 16.2 Fit model parameters

Let \(\theta\) contain parameters such as joint zero offsets, base alignment, or link dimensions. For calibration pose k, model position is \(f(q_k,\theta)\), and independently measured tip position is \(p_k\). Minimize:

\[
\theta^*=\arg\min_\theta\sum_k\|p_k-f(q_k,\theta)\|_{W_k}^2.
\]

The weighted square means \(e^TW_ke\). Set weights using measurement uncertainty. A parameter cannot be identified if the calibration motions do not reveal its effect. Use diverse safe postures and reserve held-out poses for verification.

A small-error linearization is \(e\approx A\Delta\theta\), where each column of A is sensitivity to a parameter. Least squares minimizes \(\|A\Delta\theta-e\|^2\). Its normal equation is \(A^TA\Delta\theta=A^Te\); in software use QR or SVD for better conditioning. Check rank and parameter correlation rather than blindly accepting a fitted result.

### 16.3 Error measures

For N position differences \(e_k\),

\[
RMSE=\sqrt{\frac1N\sum_k\|e_k\|^2}.
\]

Also report maximum and p95 error; average alone can hide a bad region. For orientation, compute relative rotation \(R_e=R_{pred}^TR_{meas}\). A rotation by angle \(\phi\) has trace \(1+2\cos\phi\), so:

\[
\phi=\arccos\left(\operatorname{clamp}((\operatorname{tr}R_e-1)/2,-1,1)\right).
\]

Clamping handles floating-point roundoff. Do not subtract Euler-angle components and assume that gives a meaningful orientation distance near angle wrap or gimbal lock.

### 16.4 Propagate uncertainty

Small joint errors \(\delta q\) create tip error \(\delta p\approx J_v\delta q\). If joint-error covariance is \(\Sigma_q\), then:

\[
\Sigma_p\approx J_v\Sigma_qJ_v^T.
\]

This follows by substituting the linear relation into
\(E[\delta p\delta p^T]\). Add appropriate calibration, tool, timing, and measurement uncertainties, including correlations when present.

A simple scalar budget with independent components is
\(u_{total}=\sqrt{u_1^2+u_2^2+\cdots}\). That independence assumption must be justified. Bias does not disappear merely because many samples were averaged.

### 16.5 Do not confuse ABB repeatability with twin accuracy

Manual p.95 gives, for the standard 240/2.65 variant under its stated test conditions, pose repeatability 0.04 mm and path repeatability 0.09 mm. It also defines the pose-accuracy entry relative to taught positions and notes the test regime. Those values do not promise that an uncalibrated open-source CAD model knows the absolute tool position to 0.04 mm.

Twin performance includes geometry, frame, tool, sensor, and timing errors. Select an initial visual-monitoring target such as 10 mm held-out TCP RMSE only as a **project target**, then revise it with the application. Precision metrology requires different evidence from a shop-floor status display.

### 16.6 Evidence package

For each validation run, save source CAD/PDF hashes, repaired-model hashes, joint-frame definitions, tool/payload data, controller version, synchronization report, raw observations, test poses, scripts, residual plots, thresholds, and result disposition. A model revision remains unvalidated until its required gates pass.

## 17. Requirements and acceptance gates

The machine-readable `requirements.csv` connects the user's requirements to components, tests, and current status. Targets below are initial engineering proposals; change them to match the actual business use.

| Gate | Functional requirement | Acceptance evidence | Status in this package |
|---|---|---|---|
| G0 | Provenance and exact variant | Source files hashed; manual revision and options recorded | CAD/PDF provenance inspected; physical nameplate pending |
| G1 | Static 3D geometry | Assembly renders with workspace excluded; frame/scale checks recorded | Local CAD preview delivered; LINK03 repair unresolved |
| G2 | Robot structure | Six verified axes, signs, zeros; correct rigid grouping and tool frame | Manual limits recorded; measured joint frames pending |
| G3 | Physics data | Valid mass, CoM, inertia, collision and balance model | Derivations and workflow delivered; identification pending |
| G4 | Operational data | Real source, correct units/order, no invented channels | Contract and bridge starter delivered; controller connection pending |
| G5 | Timing and reliability | e.g. p95 end-to-end age ≤100 ms, clock uncertainty ≤5 ms, stale indication within 250 ms | Lab failure handling tested; hardware measurements pending |
| G6 | Archive/context | Deduplication, jobs/maintenance/fault links; restoration tested | SQLite lab and PostgreSQL schema delivered; service deployment pending |
| G7 | Interoperability | Documented APIs, stable asset/model IDs, SCADA/ERP mappings | Contract/schema delivered; site mappings pending |
| G8 | Analytical validity | Matched baseline and independent residual evaluation | Equations/procedure delivered; labeled observations pending |
| G9 | Open-source twin stack | Version/license manifest; no commercial twin dependency | Architecture documented; deployed dependency audit pending |
| G10 | Operational use | Restart/reconnect/outage tests and operator runbook pass | Local runbook delivered; cell commissioning pending |

A target is not a result. Do not mark G5 passed because the configuration says 100 Hz. Measure source age and losses under load. Do not mark G8 passed because a graph has a green color.

### 17.1 Suggested project sequence

* **Stage A — local learning:** run lab, inspect CAD, learn units/frames, review manual variant.
* **Stage B — calibrated geometry:** repair LINK03, establish joint frames, export local meshes, validate several poses.
* **Stage C — live shadow:** implement verified read-only controller adapter, normalize data, measure time quality, animate RViz with a stale indicator.
* **Stage D — history:** deploy broker/historian/dashboard, link maintenance and jobs, test replay and restoration.
* **Stage E — physics and health:** identify dynamics/thermal parameters, validate independent simulations, then add condition monitoring.

Do not buy hardware for Stage E before proving Stage C has the required signals. The controller API is an early feasibility checkpoint, even though the local lab can be completed first.

### 17.2 Deliberate failure tests

Disconnect the data producer. Duplicate a sequence. Send a packet from a previous model revision. Reverse two joint names. Send degrees while declaring radians. Send a packet with an old source time and current receipt time. Jump the wall clock in a learning environment while confirming monotonic timeout behavior. Restart the adapter with a new stream ID. Restore the historian backup to an empty database. Measure each result; do not just describe what the design intends.

A schema cannot detect every semantic error. Six degree values labeled radians are finite and correctly shaped; plausibility checks, mapped joint limits, isolated-motion checks, and known-pose validation are needed to catch that mistake.

## 18. Daily operation and troubleshooting

### Daily startup

1. Verify correct asset, model, tool, payload, and controller version.
2. Check clock synchronization and source age before interpreting motion.
3. Confirm the adapter, broker, historian, and visualizer are running.
4. Verify recording capacity and retention status.
5. Compare one known stationary posture and expected operating mode.
6. Review advisories with their run/job context and quality flags.

### Troubleshooting table

| Symptom | Likely cause | First useful check |
|---|---|---|
| Robot is 1,000 times too big | mm/m error | Inspect mesh vertices and URDF mesh scale |
| Link swings around the building | Mesh still in assembly coordinates | Recompute inverse link-frame transform |
| Some parts appear twice | Compound/child or CAD00 duplication | Inspect hierarchy and component identity |
| Huge sphere/envelope hides robot | Workspace included as material | Exclude `Working-space` from geometry |
| Mass or CoM is implausible | Invalid solid or simplistic material assumption | Check LINK03, density units, and mass evidence |
| A6 jumps at ±180° | Multi-turn state wrapped | Preserve unwrapped controller joint angle |
| Robot looks right at one pose only | Frame or zero-offset error | Compare isolated joint changes and held-out poses |
| Live view freezes without warning | Missing freshness watchdog | Check source age and monotonic receipt timeout |
| Faults appear only during fast motion | Time skew or derivative noise | Align timestamps before blaming mechanics |
| Temperature is always zero | Missing channel coerced into zero | Use unavailable/null and check sensor mapping |
| History has duplicated packets | QoS retries without application dedup | Check primary key and adapter session IDs |
| Gazebo model explodes or collapses | Bad inertia, collision, or timestep | Validate units/tensors and fixed base |
| RViz updates but Gazebo does not move | State publication confused with simulated control | Inspect ros2_control command interfaces/controllers |
| “No module named FreeCAD” | Wrong Python runtime/search path | Use installed FreeCAD's matching Python and libraries |
| “Connection refused” in local viewer | Server is stopped | Start `tools/twin_lab.py serve` in a running terminal |

### Recovery and rollback

Keep previous validated model revisions. A geometry or calibration update creates a new revision; do not rewrite the identity of an old run. If a new model fails, select the prior validated revision and retain evidence of the failed change. Mark the display unusable while its geometry and data revisions differ.

Test backups by restoration, not merely by checking a backup file exists. Document who can update assets, calibration, credentials, and alert thresholds. Keep credentials out of CAD files and Git. No hardware command path is needed for this observational twin.

## 19. Exercises, glossary, and references

### Exercises with answers

1. **Convert 200 mm to meters.** Divide by 1,000: 0.2 m.
2. **Convert A2's 90°/s maximum speed.** Multiply by π/180: 1.5708 rad/s.
3. **At 100 Hz, how long between samples?** 1/100 = 0.01 s = 10 ms.
4. **A 20 kg load is 0.3 m horizontally from an axis. What gravity torque does this simplified lever create?** 20 × 9.81 × 0.3 = 58.86 N·m. This is not a complete robot joint load calculation.
5. **Why does an old message arriving now remain stale?** Receipt time describes delivery; source time describes the measurement.
6. **Does a 240 kg capacity mean a 240 kg object is acceptable at every offset?** No. Mass, CoM, inertia, motion range, accessories, and load diagrams all matter.
7. **Can the 1,160 kg total identify each link's inertia?** No. Many mass distributions share that total.
8. **Why is the source workspace not a collision body?** It describes possible operating reach, not physical robot material.
9. **Can an accurate rendering prove a valid solid?** No. LINK03 demonstrates why rendering and solid validity are different tests.
10. **If measured angle is 0.02 rad and predicted is 0.01 rad, what is the residual?** +0.01 rad, provided times and frames match.

### Glossary

| Word | Plain meaning |
|---|---|
| CAD | A computer description of shapes and assemblies |
| STEP | A standard engineering geometry exchange format |
| B-rep | Surfaces, edges, and their relationships defining a shape |
| Mesh | Small triangles approximating a surface |
| Link | One rigid robot body, possibly made from many solids |
| Joint | Connection allowing a defined relative motion |
| Frame | An origin and three directed coordinate rulers |
| Pose | Position and orientation together |
| TCP | The selected working point attached to the tool |
| URDF | A robot tree description for links, joints, visuals, and other properties |
| SDF | A simulation description including worlds and mechanisms |
| Telemetry | Measurements sent from equipment |
| Timestamp | A statement of when something happened |
| Latency | Delay between an event and its useful arrival/display |
| Jitter | Variation in delay or sample interval |
| Historian | Storage for time-indexed industrial observations |
| CoM/CoG | Center of mass / center of gravity under a uniform gravity field |
| Inertia | How mass distribution resists angular acceleration |
| Residual | Measurement minus model prediction |
| Calibration | Measuring and correcting the relation between model and reality |
| Validation | Evidence that a model is adequate for its stated purpose |

### Reading order after the workbook

Use `SOURCES.md` for source links and access notes. First revisit your manual pp.21, 38–41, 73–76, 91–96, and the stopping-data context pp.97–103. Then learn URDF/TF using a small example, before attaching detailed geometry. Finally work through the Modern Robotics motion and dynamics lessons as needed.

The supplied product specification and CAD were treated as evidence, not as instructions to change system behavior. External documents and websites cannot authorize hardware writes or override your request.
