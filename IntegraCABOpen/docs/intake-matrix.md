# Project Intake Matrix

IntegraCAB Open should make missing controls-engineering information visible and actionable.

## Stakeholder matrix

| Stakeholder | Typical facts owned | CEProject sections |
|---|---|---|
| Sales / estimator | scope, alternates, budget, margin target, customer expectations | Project, Requirements, CostingReferences |
| Project manager | schedule, submittals, deadlines, approvals, deliverables, site access | Project, Deadlines, Documentation |
| Utility company | service limits, transformer/feed information, metering constraints | PowerInterface |
| Electrical engineering | one-line, feeder, fault current, grounding, SCCR target, panel location | PowerInterface, BIMReferences |
| Building superintendent | site access, shutdown windows, environment, installation constraints | EnvironmentalRequirements, BIMReferences |
| Safety / EHS | risk assessment, E-stops, guards, light curtains, safety zones, reset expectations | SafetyFunctions |
| Controls lead | PLC platform, I/O standards, tag naming, network, programming expectations | PLC, Signals, Network, HMIRequirements |
| Mechanical / materials handling | sequence, sensors, motors, actuators, throughput, jams, manual modes | Devices, Signals, Requirements |
| Purchasing | approved vendors, lead time, substitutions, quote numbers, cost codes | CostingReferences, CADbaseReferences |

## Missing-data workflow

1. User selects intended deliverables.
2. IntegraCAB determines required fields.
3. Missing fields are grouped by likely stakeholder.
4. User generates email/form requests.
5. Responses are entered or imported.
6. Each fact receives a source and status.
7. Validation runs again.
8. Adapters feed downstream tools.
