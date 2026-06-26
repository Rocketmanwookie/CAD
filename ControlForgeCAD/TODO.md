# IntegraCAB Open Master TODO

This file tracks the project scope, roadmap, interoperability commitments, documentation obligations, and companion workbench ideas for IntegraCAB Open.

## 0. Working identity

- [ ] Rename working-title references from `ControlForgeCAD` to `IntegraCAB Open`.
- [ ] Use display name: `IntegraCAB™ Open`.
- [ ] Use repository/folder slug: `integracab-open` where practical.
- [ ] Use Python package name: `integracab`.
- [x] Use FreeCAD workbench/menu label: `Controls / Automation`.
- [ ] Keep XML project format name: `CEProject`.
- [ ] Keep tagline: `The open-source FreeCAD workbench that unites PLC controls with CAD.`
- [ ] Avoid the trademark symbol in filenames, Python imports, XML namespaces, or package identifiers.

## 1. Product philosophy

- [ ] Keep the core workbench light, integration-first, and useful before it is polished.
- [ ] Avoid brand-heavy engineering behavior; let open-source contributors improve packaging, themes, icons, installers, docs, and distribution when the structure is easy to work with.
- [ ] Prefer adapters into existing FreeCAD/openBIM resources instead of recreating mature tools.
- [ ] Treat IntegraCAB Open as a controls-engineering orchestration layer: intake, validation, traceability, and handoff.
- [ ] Do not replace CADbase, BOM workbenches, BIM tools, TechDraw, Spreadsheet, PLC IDEs, HMI platforms, ERP systems, or vendor catalogs.
- [ ] Reduce project havoc: missing data, duplicate entry, stale assumptions, rework, quoting churn, procurement mistakes, and field surprises.

## 2. Core workbench responsibilities

- [ ] Structured project intake.
- [x] Missing-data tracking.
- [ ] Role-based request templates.
- [x] CEProject XML source-of-truth model.
- [ ] Validation of missing, contradictory, assumed, estimated, and unapproved values.
- [ ] Traceability between requirements, devices, signals, terminals, circuits, CADbase parts, cost records, and exports.
- [ ] Adapter layer to CADbase, BOM tools, BIM/openBIM tools, spreadsheets, TechDraw, and future PLC/HMI/digital-twin tools.
- [ ] Controls-specific XML schema versioning and migration notes.
- [ ] Example projects that are non-proprietary and safe to publish.

## 3. Explicit non-goals

- [ ] Do not build a full BOM workbench.
- [ ] Do not build a full CAD component-library manager if CADbase can handle it.
- [ ] Do not build a full BIM/MEP electrical design platform.
- [ ] Do not build a proprietary PLC IDE.
- [ ] Do not build a full HMI editor inside the first IntegraCAB workbench.
- [ ] Do not build a digital twin simulator inside the first IntegraCAB workbench.
- [ ] Do not redistribute vendor CAD files, datasheets, or catalog data without clear rights.
- [ ] Do not claim automatic code, panel, or installation compliance.

## 4. Core roadmap by phase

### Phase 0 - Repository and governance

- [ ] Rename docs and metadata to IntegraCAB Open.
- [ ] Add contributor guide.
- [ ] Add issue templates.
- [ ] Add pull request template.
- [ ] Add coding style guide.
- [ ] Add schema style guide.
- [ ] Add external-asset policy.
- [ ] Add versioning and migration policy for CEProject XML.
- [ ] Add architecture decision record folder: `docs/adr/`.
- [ ] Add roadmap issue labels: `roadmap`, `intake`, `xml`, `adapter`, `documentation`, `learning`, `hmi`, `digital-twin`, `bim`, `cadbase`, `bom`, `costing`.

### Phase 1 - Intake-first workflow

- [x] Build project intake schema section.
- [x] Add contacts/stakeholder model.
- [x] Add question/response model.
- [x] Add missing-data matrix.
- [x] Add field status model: `Unknown`, `Requested`, `Received`, `Assumed`, `Estimated`, `Verified`, `Approved`, `Rejected`, `Superseded`.
- [x] Add source record model for email, meeting note, uploaded file, phone call, field note, vendor quote, CADbase asset, BIM object, or manual entry.
- [ ] Add form templates for project managers, sales, utility company, electrical engineering, building superintendent, safety/EHS, operations, purchasing, maintenance, controls lead, mechanical/materials handling, IT/OT, and customer stakeholders.
- [ ] Add email templates that map every requested fact to a CEProject field.
- [x] Add validation output that tells the user who to ask for missing information.
- [ ] Add CSV export for the missing-data matrix.
- [x] Expose starter intake validation and missing-data preview through FreeCAD workbench commands.
- [x] Create a real editable FreeCAD `CE_Project` document object for starter intake data.
- [x] Synchronize editable `CE_Project` properties into backend validation and missing-data intake payloads.

### Phase 2 - CEProject data model

- [ ] Define top-level schema sections: `Project`, `Contacts`, `Intake`, `Requirements`, `BIMReferences`, `CADbaseReferences`, `Devices`, `Signals`, `Circuits`, `PowerInterface`, `SafetyFunctions`, `HMIRequirements`, `CostingReferences`, `ExternalExports`, `ValidationFindings`.
- [x] Version the schema with XSD file name and internal `schemaVersion`.
- [x] Add pure-Python import for the supported CEProject intake XML structure.
- [x] Add export/import round-trip tests for intake metadata, contacts, source records, questions, validation findings, and missing-data rows.
- [x] Expose CEProject intake XML export through a FreeCAD workbench command.
- [ ] Make every project fact addressable by ID.
- [ ] Make every generated artifact traceable to source fields.
- [ ] Support assumptions and estimates without treating them as verified values.
- [ ] Add migration notes from schema `0.1` to future versions.

### Phase 3 - Power drop-in and BIM/MEP interface

- [ ] Add `PowerDropReference` object.
- [ ] Track upstream transformer/source equipment.
- [ ] Track source distribution equipment and circuit ID.
- [ ] Track voltage, phase, frequency, feeder ampacity, conductor/raceway reference, available fault current, grounding system, disconnecting means, metering requirements, source drawing, and BIM object reference.
- [ ] Integrate with IFC/ifcXML references where available.
- [ ] Export unresolved coordination items as BCF-style issues later.
- [ ] Do not duplicate the full building electrical model.
- [ ] Define the boundary: BIM/MEP owns distribution up to the cabinet; IntegraCAB owns cabinet-side controls package from main disconnect inward.

### Phase 4 - CADbase integration

- [ ] Treat CADbase as the preferred local component/CAD/datasheet library.
- [ ] Store CADbase references in CEProject rather than duplicating library content.
- [ ] Track CADbase part ID, model asset ID, datasheet asset ID, revision, source URL, local path, checksum, approval status, and last verified date.
- [ ] Add adapter for selected device to CADbase part reference.
- [ ] Add policy for official manufacturer sources and redistribution limits.
- [ ] Add manual upload path when download is unavailable or restricted.

### Phase 5 - BOM and costing integration

- [ ] Do not own BOM generation natively unless no adequate existing tool exists.
- [ ] Provide normalized BOM source records.
- [ ] Add adapter to existing FreeCAD BOM workbench or equivalent BOM tools.
- [ ] Add Spreadsheet export adapter.
- [ ] Add purchasing/quote CSV adapter.
- [ ] Add cost item reference model: device -> CADbase part -> BOM source item -> cost item -> quote item -> purchase item.
- [ ] Track quantity, unit, source device, library part reference, unit cost, quoted cost, lead time, vendor, quote number, cost code, and revision.
- [ ] Support estimated, quoted, approved, and superseded cost statuses.

### Phase 6 - PLC/I/O controls package

- [ ] Add PLC platform requirement fields.
- [ ] Add rack/slot/module/channel model.
- [ ] Add signal registry.
- [ ] Add I/O count estimates and actual assignments.
- [ ] Add signal-to-device, signal-to-terminal, signal-to-wire, and signal-to-HMI relationships.
- [ ] Add PLCopen XML export plan.
- [ ] Add vendor-neutral export first; vendor-specific adapters later.
- [ ] Include ladder/logic references without becoming a full PLC IDE.

### Phase 7 - Wiring, terminals, and cabinet-side power

- [ ] Add terminal strip reference model.
- [ ] Add wire/from-to reference model.
- [ ] Add internal cabinet power circuits.
- [ ] Add control power distribution.
- [ ] Add protective-device references.
- [ ] Add VFD/motor branch references.
- [ ] Add sensor cable and field junction references.
- [ ] Feed wiring/terminal data to drawing or schedule tools.

### Phase 8 - HMI as future companion workbench

- [ ] Create companion concept: `IntegraHMI Open` or `HMI / SCADA Design`.
- [ ] Keep HMI GUI design out of the initial core workbench.
- [ ] Define tag dictionary export from CEProject.
- [ ] Define screen requirements, alarm requirements, equipment hierarchy, modes/states, navigation, faceplate needs, trends, historian points, and operator actions.
- [ ] Include ISA-101/high-performance HMI concepts in documentation.
- [ ] Start vendor-neutral HMI requirements format before platform-specific adapters.
- [ ] Later adapters may target Ignition, FactoryTalk View, AVEVA/Wonderware, WinCC, and other systems only if legal/technical access is practical.

### Phase 9 - Digital twin as future companion workbench

- [ ] Create companion concept: `IntegraTwin Open` or `Digital Twin / Simulation`.
- [ ] Keep digital twin simulation out of the initial core workbench.
- [ ] Define links from CEProject to geometry, I/O state, simulated sensors, actuators, states, sequences, faults, and HMI behavior.
- [ ] Research AutomationML, OPC UA NodeSet2, FMI/FMU, ROS 2, Gazebo/Ignition, and discrete-event simulation interfaces.
- [ ] Add a future simulator boundary document.

### Phase 10 - Education docs for new controls engineers

- [ ] Add `docs/learning-path.md`.
- [ ] Add `docs/glossary.md`.
- [ ] Add `docs/resources.md`.
- [ ] Explain the interdisciplinary map: electrical power, controls, PLCs, CAD, sensors, pneumatics/hydraulics, motion, motor control, industrial networks, machine safety, HMI/SCADA, data/historians, cybersecurity, BIM/openBIM, costing, documentation, project management, commissioning, and maintenance.
- [ ] Link official resources where possible.
- [ ] Do not duplicate copyrighted manuals or standards text.
- [ ] Provide beginner examples: small conveyor panel, pump skid, robot cell I/O cabinet, simple building automation panel.
- [ ] Add practical checklists and vocabulary, not just theory.

## 5. Stakeholder intake templates to build

- [ ] Sales / estimator intake.
- [ ] Project manager intake.
- [ ] Customer engineering intake.
- [ ] Utility company electrical feed request.
- [ ] Electrical engineering feed and SCCR/fault-current request.
- [ ] Building superintendent/site conditions request.
- [ ] Safety/EHS requirements request.
- [ ] Controls platform standards request.
- [ ] IT/OT network and cybersecurity request.
- [ ] Mechanical/materials-handling sensor and sequence request.
- [ ] Operations/maintenance preference request.
- [ ] Purchasing/vendor/lead-time request.
- [ ] Commissioning and startup constraints request.

## 6. Required question domains

- [ ] Electrical feed: voltage, phase, frequency, transformer, source panel, circuit, breaker/fuse, feeder ampacity, conductor, raceway, grounding, available fault current, required SCCR, utility/company requirements.
- [ ] Environmental: indoor/outdoor, temperature, humidity, dust, washdown, corrosive exposure, vibration, area classification, NEMA/IP rating, enclosure material, cooling/heating.
- [ ] Equipment and process: machine type, sequence, throughput, motors, drives, actuators, materials handled, jam/fault conditions, manual modes, maintenance modes.
- [ ] I/O and sensors: sensor count, type, signal level, analog scaling, field wiring, connector type, junction boxes, spare I/O, calibration, installation constraints.
- [ ] Safety: E-stops, guards, light curtains, STO, safety relays/controllers, reset, EDM/feedback, zones, risk assessment references, required safety standard references.
- [ ] PLC/controls: preferred platform, programming standard, tag naming, network type, HMI/SCADA, alarms, historian, remote access, cybersecurity, backup policy.
- [ ] HMI: screens, operator tasks, alarm philosophy, trends, recipes, users, access levels, equipment hierarchy, state/mode model.
- [ ] BIM/site: room/space, panel location, upstream source references, raceway routes, IFC object references, COBie handoff expectations, BCF issue workflow.
- [ ] Cost/schedule: budget, quote deadline, delivery deadline, lead-time constraints, approved vendors, substitutions, alternates, labor assumptions, commissioning window.
- [ ] Documentation: drawing package, submittals, O&M manuals, datasheet package, training docs, FAT/SAT/IQ/OQ style requirements where applicable.

## 7. Standards and interoperability watchlist

- [ ] FreeCAD workbench/addon architecture.
- [ ] FreeCAD BIM and IFC workflows.
- [ ] FreeCAD Spreadsheet/BOM/TechDraw resources.
- [ ] CADbase or equivalent local library workflows.
- [ ] PLCopen XML / IEC 61131-3.
- [ ] AutomationML / CAEX.
- [ ] OPC UA / NodeSet2 XML.
- [ ] IFC / ifcXML / openBIM.
- [ ] COBie / asset handoff.
- [ ] BCF / model coordination issues.
- [ ] ETIM / ECLASS / IEC CDD product classification.
- [ ] ISA-101 HMI guidance.
- [ ] ISA/IEC 62443 industrial cybersecurity guidance.
- [ ] NEC / NFPA 70, NFPA 79, UL 508A, IEC 60204-1, ISO 13849, IEC 62061, IEC 61508 as reference domains; do not reproduce restricted text.
- [ ] FMI/FMU and ROS 2 for future digital twin links.

## 8. Validation engine backlog

- [x] Missing required data by selected deliverables.
- [ ] Contradictory voltage/phase values.
- [ ] Missing available fault current.
- [ ] Missing SCCR target.
- [ ] Missing enclosure/environmental rating.
- [x] Missing PLC platform.
- [ ] Missing preferred vendors.
- [x] Missing sensor count or I/O estimate.
- [ ] Missing HMI requirement set.
- [ ] Missing upstream BIM/feed reference.
- [ ] Missing CADbase part reference.
- [ ] Missing BOM export mapping.
- [ ] Missing cost item reference.
- [ ] Unverified assumption used in a deliverable.
- [ ] Superseded answer still referenced.
- [ ] Conflicting answers from different stakeholders.

## 9. Open-source maintainability

- [x] Use small, readable modules.
- [ ] Keep schema examples human-readable.
- [ ] Keep dependencies minimal.
- [x] Add tests for deterministic CEProject XML intake export.
- [x] Add tests for CEProject XML intake import and round-trip behavior.
- [x] Add FreeCAD workbench smoke tests for import-safe init files and command metadata.
- [x] Add documented FreeCAD user `Mod` install/link workflow.
- [ ] Add tests for XML examples and validators.
- [ ] Add CI later if GitHub Actions access is available.
- [ ] Add documentation build later.
- [ ] Keep all sample data non-proprietary.
- [ ] Provide clear extension points for adapters.
- [ ] Make packaging easy for the FreeCAD Addon Manager when the project matures.

## 10. Business thesis

- [ ] Less havoc = more money.
- [ ] Less missing information = fewer redesigns.
- [ ] Less duplicate entry = fewer clerical errors.
- [ ] Less vendor chasing = faster quoting and purchasing.
- [ ] Less drawing churn = better schedule control.
- [ ] Less field surprise = better margin.
- [ ] Capture once; validate early; reuse everywhere.
