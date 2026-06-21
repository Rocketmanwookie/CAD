# IntegraCAB Open Roadmap

IntegraCAB Open is an integration-first FreeCAD workbench for controls-engineering intake, validation, traceability, and handoff.

## North star

Less havoc = more money.

The project should reduce costly controls-engineering rework by making missing data visible, capturing facts once, validating assumptions early, and feeding existing CAD/BOM/BIM/PLC resources instead of duplicating them.

## Release direction

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

## Companion workbench roadmap

- HMI / SCADA Design: future workbench for screen requirements, tag dictionaries, alarms, trends, modes, states, and operator interface traceability.
- Digital Twin / Simulation: future workbench for CAD-to-I/O simulation, process states, sensor behavior, actuator behavior, and runtime data model links.

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
| Digital twin seed | future simulation companion input | Medium |

## Development rule

If a mature tool already does the job, IntegraCAB should integrate with it. Native generation belongs only where controls-specific traceability or validation is missing.
