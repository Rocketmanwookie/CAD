# Controls Engineering Learning Path

Controls engineering is interdisciplinary. This document is intended to help new and developing engineers understand what they need to learn and where IntegraCAB Open fits.

## Learning map

```text
Electrical power
    -> control panels
    -> PLC I/O
    -> sensors and actuators
    -> motor control and drives
    -> machine safety
    -> industrial networking
    -> HMI / SCADA
    -> data, historians, and OPC UA
    -> CAD / BIM / documentation
    -> costing, procurement, and project management
    -> commissioning and maintenance
```

## 1. Electrical fundamentals

Learn voltage, current, resistance, power, single-phase and three-phase systems, grounding, bonding, short-circuit current, overcurrent protection, wire sizing, and control power.

Practical outcomes:

- Read a one-line diagram.
- Understand transformer, feeder, panel, branch circuit, and control power relationships.
- Understand why available fault current and SCCR matter for panel work.

## 2. Industrial control panels

Learn enclosures, DIN rail, wire duct, terminal blocks, disconnects, breakers, fuses, power supplies, relays, contactors, VFDs, PLCs, safety relays, grounding bars, and layout rules.

Practical outcomes:

- Build a component list from a machine/control requirement.
- Understand panel-side power distribution.
- Understand layout constraints before drawing.

## 3. PLCs and I/O

Learn PLC architecture, CPU/rack/slot/channel concepts, digital inputs, digital outputs, analog inputs, analog outputs, addressing, scan cycle, tags, programs, tasks, and common IEC 61131-3 languages.

Practical outcomes:

- Build an I/O list.
- Map sensors and actuators to PLC channels.
- Trace a signal from field device to terminal to PLC tag.

## 4. Sensors and field devices

Learn proximity sensors, photoeyes, pressure switches, encoders, analog transmitters, thermocouples, RTDs, M12 cabling, junction boxes, shielding, calibration, and installation constraints.

Practical outcomes:

- Ask for the right sensor count and signal type.
- Capture installation and calibration notes.
- Feed sensor data into I/O, wiring, HMI, and maintenance records.

## 5. Motor control, VFDs, pneumatics, hydraulics, and motion

Learn motor starters, contactors, overloads, VFDs, STO, servo drives, cylinders, solenoids, valves, pressure/flow components, and simple motion systems.

Practical outcomes:

- Identify control outputs and feedback inputs.
- Understand how actuator choices affect power, safety, wiring, and HMI.

## 6. Machine safety

Learn E-stops, guards, light curtains, safety relays/controllers, dual-channel circuits, monitored reset, EDM/feedback, STO, risk assessment vocabulary, and safe commissioning practices.

Practical outcomes:

- Know what questions to ask EHS/safety stakeholders.
- Track safety functions separately from ordinary control logic.
- Avoid treating safety assumptions as verified requirements.

## 7. Industrial networking and cybersecurity

Learn Ethernet/IP, PROFINET, Modbus TCP, OPC UA, device addressing, VLANs, switch layout, remote access, backups, user accounts, and industrial cybersecurity concepts.

Practical outcomes:

- Ask IT/OT for network requirements early.
- Capture IP addressing and remote-access constraints.
- Track cybersecurity requirements as project data, not afterthoughts.

## 8. HMI / SCADA

Learn operator screens, navigation, alarms, trends, modes/states, recipes, user access, faceplates, equipment hierarchy, and high-performance HMI concepts.

Practical outcomes:

- Define HMI requirements before screens are drawn.
- Link screens and alarms to PLC tags and equipment states.
- Prepare for a future HMI companion workbench.

## 9. CAD, BIM, and documentation

Learn panel layouts, wiring diagrams, terminal schedules, TechDraw, BOM/schedules, FreeCAD workbenches, IFC/openBIM, COBie, BCF, and structured document handoff.

Practical outcomes:

- Use CAD for traceable engineering output, not disconnected drafting.
- Tie the control cabinet to BIM/MEP context without duplicating the building model.

## 10. Costing, procurement, and project management

Learn estimating, quote packages, approved vendors, lead times, substitutions, alternates, change control, deadlines, submittals, RFIs, FAT/SAT, commissioning, and documentation packages.

Practical outcomes:

- Capture purchasing and lead-time constraints early.
- Link cost items to devices and library parts.
- Reduce rework by making missing data visible.

## How IntegraCAB helps new engineers

IntegraCAB should help by showing what information is needed, who likely owns it, and where it goes in the project model. The goal is not to replace judgment. The goal is to prevent beginner mistakes caused by missing context.

## Beginner example projects

- Small conveyor panel.
- Pump skid.
- Robot-cell I/O cabinet.
- Building automation panel.
- Small VFD/motor starter cabinet.
- Sensor-only remote I/O panel.

## Documentation policy

Point to official standards, vendor manuals, FreeCAD documentation, PLCopen/AutomationML/OPC UA/openBIM resources, and trusted educational references. Do not copy restricted standards text or vendor manuals into the repo.
