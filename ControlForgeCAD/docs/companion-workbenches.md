# Companion Workbenches

IntegraCAB Open should remain focused on controls-engineering intake, validation, traceability, and integration with existing FreeCAD resources. HMI design and digital twin simulation are important enough to become companion workbenches later.

## Product family concept

```text
IntegraCAB Open      Controls / Automation intake and CAD integration
IntegraHMI Open      HMI / SCADA GUI design and requirements
IntegraTwin Open     Digital twin / simulation and I/O behavior
CADbase              Reusable CAD assets, datasheets, component library
BOM Workbench        BOM generation and schedule output
BIM/openBIM tools    IFC, COBie, BCF, spatial/facility handoff
```

## Companion 1: IntegraHMI Open

Possible workbench labels:

- `HMI / SCADA Design`
- `IntegraHMI Open`
- `Operator Interface`

### Purpose

Design and document HMI/SCADA requirements using the same structured project model that feeds PLC I/O, cabinet layout, sensors, alarms, and equipment states.

### Inputs from CEProject

- Tag dictionary.
- Equipment hierarchy.
- PLC/I/O map.
- Alarm list.
- Modes and states.
- Sensor and actuator list.
- Safety status points.
- Process sequence.
- User/access requirements.
- Historian/trend points.

### Outputs

- HMI screen requirements.
- Navigation map.
- Alarm matrix.
- Trend list.
- Faceplate requirements.
- Operator action list.
- Tag dictionary export.
- Vendor-neutral HMI specification.
- Future vendor-specific adapters where practical.

### First version boundary

Do not build full vendor HMI projects first. Build neutral requirements, tag dictionaries, screen maps, alarm lists, and traceability.

## Companion 2: IntegraTwin Open

Possible workbench labels:

- `Digital Twin / Simulation`
- `IntegraTwin Open`
- `I/O Simulation`

### Purpose

Connect CAD geometry, PLC I/O state, process behavior, sensor simulation, actuator behavior, and HMI expectations into a testable digital model.

### Inputs from CEProject

- 3D panel and equipment references.
- PLC I/O map.
- Signals and devices.
- Sensor behavior assumptions.
- Actuator behavior assumptions.
- Sequence/state model.
- HMI modes/states.
- Fault conditions.
- Network/runtime tag references.

### Outputs

- Simulation object map.
- I/O simulation table.
- State machine references.
- Test cases.
- Fault-injection scenarios.
- OPC UA / simulation interface mapping.
- Future ROS 2 / Gazebo / FMI exploration.

### First version boundary

Do not build a full physics simulator first. Build traceability between CAD, I/O, and process state. Add simulation engine adapters later.

## Why separate workbenches?

HMI and digital twin design are large domains. Keeping them separate prevents IntegraCAB Open from becoming a monolith. The first workbench should focus on capturing and validating the data that those later workbenches need.

## Shared source-of-truth rule

The companion workbenches should consume CEProject data instead of recreating it. If an HMI screen needs a tag or a digital twin needs an actuator, it should reference the same signal/device IDs used by the main IntegraCAB project.
