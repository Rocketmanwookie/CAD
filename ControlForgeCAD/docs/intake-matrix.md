# Project Intake Matrix

integraCAD Open should make missing controls-engineering information visible and actionable. This matrix maps project facts to likely stakeholders, request templates, XML sections, and downstream consumers.

## Status values

Use status metadata on captured facts:

```text
Unknown
Requested
Received
Assumed
Estimated
Verified
Approved
Rejected
Superseded
```

## Stakeholder matrix

| Stakeholder | Typical facts owned | Templates to build | CEProject sections |
|---|---|---|---|
| Sales / estimator | scope, alternates, budget, margin target, customer expectations | sales-intake | Project, Requirements, CostingReferences |
| Project manager | schedule, submittals, deadlines, approvals, deliverables, site access | project-manager-intake | Project, Deadlines, Documentation |
| Utility company | service limits, transformer/feed information, metering constraints | utility-feed-request | PowerInterface |
| Electrical engineering | one-line, feeder, fault current, grounding, SCCR target, panel location | electrical-feed-request | PowerInterface, BIMReferences |
| Building superintendent | site access, shutdown windows, environment, installation constraints | site-conditions-request | EnvironmentalRequirements, BIMReferences |
| Safety / EHS | risk assessment, E-stops, guards, light curtains, safety zones, reset expectations | safety-requirements-request | SafetyFunctions |
| Controls lead | PLC platform, I/O standards, tag naming, network, programming expectations | controls-platform-request | PLC, Signals, Network, HMIRequirements |
| IT / OT | network addressing, remote access, backups, cybersecurity, segmentation | it-ot-request | Network, SecurityRequirements |
| Mechanical / materials handling | sequence, sensors, motors, actuators, throughput, jams, manual modes | machine-sequence-request | Devices, Signals, Requirements |
| Operations / maintenance | preferred brands, spares, accessibility, diagnostics, training | maintenance-preference-request | CADbaseReferences, Documentation |
| Purchasing | approved vendors, lead time, substitutions, quote numbers, cost codes | purchasing-request | CostingReferences, CADbaseReferences |
| Customer stakeholder | acceptance criteria, operator expectations, project constraints | customer-intake | Project, Requirements, HMIRequirements |

## Required data domains

### Electrical feed

- Source transformer.
- Source distribution equipment.
- Source circuit/breaker/fuse.
- Nominal voltage.
- Phase count.
- Frequency.
- Feeder ampacity.
- Conductor size/material.
- Raceway/conduit/cable tray reference.
- Grounding system.
- Available fault current.
- Required SCCR.
- Utility/company requirements.
- Existing one-line drawing reference.
- BIM/IFC object reference.

### Environmental and installation

- Indoor/outdoor.
- Ambient temperature.
- Humidity.
- Dust/washdown/corrosion.
- Vibration.
- NEMA/IP target.
- Enclosure material.
- Cooling/heating needs.
- Access restrictions.
- Shutdown window.
- Mounting location.

### PLC / controls

- PLC platform.
- Network protocol.
- Preferred tag naming.
- Programming standard.
- I/O estimate.
- Spare I/O requirement.
- Remote access requirements.
- Backup expectations.
- Customer standard drawings or templates.

### Sensors / I/O

- Sensor count.
- Sensor types.
- Signal type.
- Cable/connector preference.
- Field junction boxes.
- Analog scaling.
- Calibration needs.
- Installation notes.
- Spare channels.

### HMI / SCADA

- HMI platform.
- Screen list.
- Equipment hierarchy.
- Alarm philosophy.
- Trends.
- Recipes.
- Modes/states.
- Users/access levels.
- Historian points.

### Costing and procurement

- Approved vendors.
- Preferred brands.
- Required alternates.
- Lead-time constraints.
- Quote deadline.
- Project deadline.
- Cost codes.
- Labor assumptions.
- Commissioning window.

## Output mapping

| Captured data | Downstream use |
|---|---|
| Electrical feed | Power interface, panel validation, one-line references, SCCR review prompts |
| PLC platform | I/O list, tag dictionary, PLCopen mapping, HMI requirements |
| Sensor list | I/O list, wiring, HMI, CADbase part lookup, installation notes |
| Environmental data | enclosure selection, cooling/heating, materials, field warnings |
| Safety requirements | safety-function records, safety device list, validation checklist |
| CADbase references | panel layout, drawing references, BOM source rows, datasheet packages |
| Costing data | estimate exports, purchasing requests, quote tracking |
| BIM references | IFC/COBie/BCF export and coordination |

## Missing-data workflow

1. User selects intended deliverables.
2. IntegraCAB determines required fields.
3. Missing fields are grouped by likely stakeholder.
4. User generates email/form requests.
5. Responses are entered or imported.
6. Each fact receives a source and status.
7. Validation runs again.
8. Adapters feed downstream tools.
