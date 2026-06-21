# IntegraCAB Open TODO

This file tracks near-term scope decisions, future companion workbenches, and documentation obligations.

## Product philosophy

- [ ] Keep the core workbench light and integration-first.
- [ ] Avoid brand-heavy packaging inside the engineering tool; make the open-source structure easy for contributors to brand, fork, package, and document cleanly.
- [ ] Prefer adapters into existing FreeCAD/openBIM resources instead of recreating them.
- [ ] Treat IntegraCAB Open as a controls-engineering orchestration layer: intake, validation, traceability, and handoff.

## Core IntegraCAB Open workbench

- [ ] Rename working-title references from ControlForgeCAD to IntegraCAB Open.
- [ ] Use `Controls / Automation` as the FreeCAD workbench/menu label.
- [ ] Keep `CEProject` as the internal controls-project XML format.
- [ ] Define integration-first policy: reference external systems instead of duplicating their databases.
- [ ] Add CADbase integration plan for reusable CAD models, datasheets, and component library references.
- [ ] Add BOM workbench integration plan instead of native BOM generation.
- [ ] Add BIM/openBIM integration plan for IFC, COBie, and BCF.
- [ ] Add power drop-in interface for transformer/feeder/circuit information from BIM/MEP/electrical teams.
- [ ] Add structured project intake workflow for missing controls-engineering data.
- [ ] Add email/form templates for stakeholders: sales, PM, superintendent, utility, electrical engineering, safety/EHS, controls lead, purchasing, and maintenance.

## Documentation for up-and-coming controls engineers

- [ ] Add `docs/learning-path.md` for new controls engineers.
- [ ] Explain the interdisciplinary map: electrical power, PLCs, CAD, sensors, pneumatics/hydraulics, networking, safety, HMI/SCADA, BIM, costing, documentation, and project management.
- [ ] Link official resources where possible instead of duplicating copyrighted manuals.
- [ ] Add glossary for field terms: SCCR, STO, EDM, MCR, AHJ, UL 508A, NEC, P&ID, I/O, HMI, SCADA, OPC UA, PLCopen XML, IFC, COBie, BCF.
- [ ] Add beginner project examples: small conveyor panel, pump skid, robot cell I/O cabinet, building automation panel.

## HMI / GUI Design companion workbench

- [ ] Create future workbench concept: `IntegraHMI Open` or `HMI / SCADA Design`.
- [ ] Treat HMI as a companion workbench, not a subpanel of the main controls-intake workbench.
- [ ] Include ISA-101/high-performance HMI concepts in documentation.
- [ ] Link HMI screens to CEProject tags, alarms, modes, states, equipment hierarchy, and PLC I/O.
- [ ] Generate HMI tag dictionaries and screen requirements from the same structured project model.
- [ ] Avoid vendor lock-in; export neutral screen/tag requirements first, then add adapters for specific platforms later.

## Digital Twin companion workbench

- [ ] Create future workbench concept: `IntegraTwin Open` or `Digital Twin / Simulation`.
- [ ] Treat digital twin as a later companion workbench.
- [ ] Link CAD geometry, I/O simulation, PLC tag state, sensor behavior, equipment states, and process sequence.
- [ ] Research AutomationML, OPC UA, FMI/FMU, and ROS/robotics links for simulation handoff.
- [ ] Define what remains in IntegraCAB versus what belongs in the digital twin workbench.

## Standards and interoperability

- [ ] PLC logic: PLCopen XML / IEC 61131-3.
- [ ] Automation topology: AutomationML / CAEX.
- [ ] Runtime information model: OPC UA NodeSet2.
- [ ] BIM/facility handoff: IFC / ifcXML.
- [ ] Asset handoff: COBie.
- [ ] Coordination issues: BCF.
- [ ] Product classification: ETIM / ECLASS / IEC CDD where practical.

## Open-source maintainability

- [ ] Add contributor guide.
- [ ] Add issue templates.
- [ ] Add pull request template.
- [ ] Add coding style guide.
- [ ] Add schema versioning and migration guide.
- [ ] Add example data sets that do not include proprietary vendor files.
- [ ] Add policy for external assets: link or reference vendor files unless redistribution rights are clear.
