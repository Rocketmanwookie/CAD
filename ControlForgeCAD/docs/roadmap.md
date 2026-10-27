# integraCAD Open Roadmap

integraCAD Open is an integration-first FreeCAD workbench for controls-engineering intake, validation, traceability, and handoff. **ControlForgeCAD** remains the name of its current FreeCAD workbench implementation.

## Current position

The seed, intake/validation, and early controls-package milestones are underway rather than merely aspirational. The current workbench includes editable project intake, missing-data validation and CSV export, staged CEProject XML/setup YAML/UML intake review, explicit starter I/O signals and CSV export, XML-backed PLC/panel planning metadata, starter load estimates, placeholder panel objects, typed device/terminal/wire paths, route capture and editing, Cables-workbench routing, and persisted signal-to-terminal-to-wire connection records. Project Intake can explicitly choose a catalog-feasible CPU against 120-percent spare typed demand, then show CPU/module/channel allocation rows for approval and accept readable engineering labels without permitting edits to canonical allocation keys. Selected catalog-backed PLC CPUs and expansion modules allocate I/O signals deterministically to rack, slot, and channel assignments, validate capacity/collisions, persist complete mappings, and feed I/O exports. The allocation command materializes stable PLC rack, module, and channel occurrences in the same transaction. Each channel links to one deterministic typed signal; a later path for that tag reuses the signal and is linked back to the channel, with validation for broken or incomplete links. Path authoring selects an allocated channel and derives its PLC-terminal owner and designation from the allocated address. Manual FreeCAD save/reopen acceptance evidence remains open; catalog feasibility is not final hardware approval, and this is not yet a schematic-generation or vendor-project-generation tool.

## North star

The detailed AutoCAD Electrical comparison and acceptance gates for true
feature parity are maintained in
[`autocad-electrical-plc-parity-audit.md`](autocad-electrical-plc-parity-audit.md).
Until those gates pass, project material must describe the workbench as a
controls data/workflow foundation rather than an AutoCAD Electrical replacement
or a complete digital twin.

Less havoc = more money.

The project should reduce costly controls-engineering rework by making missing data visible, capturing facts once, validating assumptions early, and feeding existing CAD/BOM/BIM/PLC resources instead of duplicating them.

## Release direction

The active [workflow milestones](../../docs/WORKFLOW_MILESTONES.md) organize
delivery into six stages: Project & Plant, Controls Circuit, Safety Circuit,
Parts & CAD, Cabinet & Routing, and Generate Package. Bulk CAD collection
follows definition of both circuits. Final enclosure construction and routing
use their combined equipment list; package generation produces the coordinated
BOM and drawings, followed by the final wire schedule.

The governing [workbench workflow](../../docs/governance/WORKBENCH_WORKFLOW.md)
now sets the product sequence: plant questionnaire, I/O counts with 20% spare
capacity, PLC/model/module selection, detailed I/O definition or import,
controls circuit definition, safety circuit definition, combined CAD collection, shared
cabinet construction, BOM and 2D/3D/cabinet drawings, then the combined wire
schedule. Implementation proceeds in that order using the existing allocation
and electrical-path services as foundations.

After defining the controls circuit, a similar safety-circuit modeling workflow
captures supplied requirements, sizes/selects safety hardware, defines points,
gathers CAD, and completes the safety connections within the same project.
Both circuits must be defined before constructing their shared cabinet. The
combined assembly then supplies BOM/drawings and wire schedules. See the
governing workflow for its ownership boundary.

### Working MVP fast lane

The existing allocation-to-path slice is a foundation milestone within the
revised workflow. That foundation is complete when a user can:

1. select a catalog-backed PLC and modules;
2. create/edit labeled I/O with rack, slot, channel, and address assignments;
3. map each I/O point through a typed terminal and wire to a field device;
4. see those devices and connection points as persistent FreeCAD objects; and
5. export a validated I/O list, terminal plan, connection schedule, and BOM from
   the same project state.

The next workflow implementation milestone separates plant intake from I/O
sizing and configuration, then supports detailed I/O definition after hardware
selection. Controls and safety circuit definition, combined CAD gathering, shared cabinet
construction, BOM/drawing adapters,
and final wire schedules follow. Their completion requires more than the
foundation exports above.

Ladder drawing generation follows the electrical foundation. HMI authoring, automatic
3D routing, broad vendor coverage, and runtime simulation do not block the MVP.

### 0.1 - Seed architecture

- Workbench loads in FreeCAD.
- Repository has license, versioning, changelog, TODO, and architecture docs.
- CEProject XML seed exists.
- First intake templates exist.
- Core philosophy is integration-first.

### 0.2 - Intake and validation prototype

- Project intake form model.
- Missing-data engine.
- Stakeholder request templates.
- Field status model.
- Basic validation report.
- Example project showing power feed, PLC platform, sensor count, environmental requirements, and cost/BOM source mapping.

### 0.3 - Adapter foundations

- CADbase reference adapter concept.
- BOM source export adapter concept.
- Spreadsheet export adapter.
- IFC/COBie/BCF reference mapping plan.
- PLCopen XML mapping plan.
- HMI requirements export seed.

### 0.4 - Controls package model

- PLC/I/O registry.
- Signal registry.
- Device registry.
- Power interface reference.
- Terminal/wire source model.
- Cabinet-side power model.
- XSD-validated continuous connection-path XML boundary.

### 0.5 - Documentation and education release

- Learning path.
- Glossary.
- Example projects.
- Standards/resource map.
- Contributor guide.
- Template catalog.

### 1.0 - Stable integration workflow

- Stable CEProject schema.
- Stable adapter interfaces.
- Validation engine usable on real projects.
- Packaging path ready for FreeCAD Addon Manager consideration.
- Companion workbench interfaces documented for HMI and digital twin projects.
- Digital-twin ready for later ROS/ROS 2 integration through stable identities,
  roles, units, continuous electrical paths, geometry bindings, and adapter
  contracts; ROS runtime initialization is not required.

## Companion workbench roadmap

- HMI / SCADA Design: future workbench for screen requirements, tag dictionaries, alarms, trends, modes, states, and operator interface traceability.
- Digital Twin / Simulation: later ROS/ROS 2 integration for CAD-to-I/O
  simulation, process states, sensor/actuator behavior, faults, and runtime data
  links. It consumes the stable electrical graph and does not block the working
  electrical-design MVP.

## Adapter roadmap

| Adapter | Purpose | Priority |
|---|---|---|
| CADbase | link reusable CAD/datasheet/library assets | High |
| BOM workbench / Spreadsheet | feed BOM source rows and cost references | High |
| IFC/COBie/BCF | BIM/facility handoff and issue coordination | High |
| PLCopen XML | PLC logic/project exchange | High |
| AutomationML / CAEX | automation topology exchange | Medium |
| OPC UA NodeSet2 | runtime information model | Medium |
| HMI requirements | future HMI companion input | Medium |
| ROS/ROS 2 digital-twin adapter | future simulation companion input/runtime boundary | Deferred |

## Development rule

If a mature tool already does the job, integraCAD Open should integrate with it. Native generation belongs only where controls-specific traceability or validation is missing.
