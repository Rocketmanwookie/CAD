# integraCAD Open agent roster

This is the readable index for the 27 roles in the
[project management charter](../PROJECT_MANAGEMENT_CHARTER.md). The charter is
the source of truth for role IDs, reporting lines, planned effort, and rules;
update it first when a role changes. This roster describes roles, not
separately running or credentialed agents. Twenty-six roles are listed as
active and Web Interface Guy is in reserve. Planned effort is a planning
allocation, not measured time or authority to approve engineering work.

The [agent spreadsheet](https://docs.google.com/spreadsheets/d/14pXsO1jcoW6wBlAahzmO6WW5qeN9k0NPBekH4SmMfEs/edit)
is a 2026-10-31 snapshot of the same 27 charter roles. Refresh it when the
charter's role records change.

Tony CAD is the primary coordinator. Every other role reports to Tony CAD in
the charter. Specialist advice, implementation, independent review, and
documentation are distinct responsibilities. Role-specific materials live at
`docs/agents/layer_<n>/<role_id>/` when they exist; the Controls Engineer Guy
materials are currently under
[`layer_4/controls_engineer_guy/`](layer_4/controls_engineer_guy/CONTROLS_ENGINEER_LOAD_PROTECTION_PLAYBOOK.md).
The four owner-authorized reference PDFs are stored only in the matching
directory of the private agent-backup repository.

## Layer 0 — domain experts (advisory)

These specialists answer bounded questions with a source title, version/date,
exact locator, conclusion, and uncertainty. Their advice is recorded through
the [SME consultation receipt](../SME_CONSULTATION_RECEIPT.md) and routed
through a Layer 4 reviewer. A specialist does not independently approve a
merge, construction issue, or code-compliance claim.

| Role and ID | Planned effort | Detailed remit |
| --- | ---: | --- |
| IEC Electrical Standards SME (`iec_electrical_standards_sme`) | 2% | Consult on IEC 60204-1 and IEC 61439 topics and IEC schematic-symbol conventions. Identify the edition and exact source basis before an IEC-specific claim. |
| NFPA/JIC Standards SME (`nfpa_jic_standards_sme`) | 1.5% | Consult on NFPA 79 and JIC symbol conventions. Keep this profile distinct from IEC rather than relabeling symbols or rules across systems. |
| Siemens S7-1200 SME (`siemens_s7_1200_sme`) | 2% | Advise on SIMATIC S7-1200 and TIA data types and the project's 104-product catalog; support source-backed Siemens-specific assertions. |
| FreeCAD API SME (`freecad_api_sme`) | 2% | Consult on FeaturePython behavior, Addon Manager metadata, and Cables workbench integration where established project knowledge is insufficient. |
| Standards Adapter SME (`standards_adapter_sme`) | 1.5% | Advise on adapters for officially published formats: PLCopen XML, AutomationML/CAEX, and OPC UA NodeSet2. Keep the claim bounded to the cited published specification. |
| Competitor Format Adapter SME (`competitor_format_adapter_sme`) | 1.5% | Examine proprietary or reverse-engineered ECAD, AutoCAD Electrical, and SolidWorks Electrical formats. Require a recorded real-tool round trip before any compatibility claim. |
| Conductor Sizing Code SME (`conductor_sizing_code_sme`) | 2% | Consult on NEC/CEC conductor sizing inputs and methods, including load/protection, ambient correction, voltage drop, and fault duty. Surface the adopted code and project conditions. |
| Circuit Protection SME (`circuit_protection_sme`) | 2% | Consult on breaker, fuse, and overload-relay selection, selective coordination, and SCCR. Must work jointly with Motor Sizing SME for motor-circuit protection or sizing. |
| Motor Sizing SME (`motor_sizing_sme`) | 2% | Consult on NEC 430 motor branch-circuit and overload sizing, FLA tables, starter/VFD selection, and service factor. Must work jointly with Circuit Protection SME for motor-circuit protection or sizing. |
| Vendor Catalog SME (`vendor_catalog_sme`) | 2.5% | Identify official vendor catalog structures, correct CAD/2D asset variants, access methods, and terms. CAD Asset Scout consults this role before onboarding a vendor. |

## Layer 1 — coordination and context

| Role and ID | Planned effort | Detailed remit |
| --- | ---: | --- |
| Tony CAD (`tony_cad`) | 8% | Establish the verified project state and smallest useful milestone; coordinate scope, specialists, implementation, independent reviews, integration, documentation, and handoff. Create or train roles and acquire needed skills while preserving evidence and known limitations. Tony CAD makes completion calls only from recorded evidence and does not replace required independent reports or project-owner review. |

## Layer 2 — tools and assets

| Role and ID | Planned effort | Detailed remit |
| --- | ---: | --- |
| Integration Scout (`integration_scout`) | 3% | Find and vet SDKs, FreeCAD Addon Manager dependencies, and standards-adapter libraries. Check licenses and provenance before a dependency enters the project. |
| CAD Asset Scout (`cad_asset_scout`) | 3% | Find the correct vendor asset variant, with terminal-labelled geometry where required; consult Vendor Catalog SME, check redistribution terms, and use authorized access with securely stored credentials. Do not scrape a vendor where its terms prohibit that access. |

## Layer 3 — construction

Construction roles own separable surfaces. Tony CAD records worktree bases and
integration handoffs when parallel work is appropriate; a role's assignment
does not grant it independent product-scope or engineering-approval authority.

| Role and ID | Planned effort | Detailed remit |
| --- | ---: | --- |
| Python Guy (`python_guy`) | 7% | Own pure domain logic such as `model/`, `identity.py`, and validation, keeping FreeCAD and GUI imports out of that layer. |
| GUI Expert (`gui_expert`) | 6% | Own Qt/PySide dialogs and FreeCAD FeaturePython ViewProvider and TaskPanel interactions. |
| Backend Guy (`backend_guy`) | 7% | Own command and transaction plumbing, including `freecad_transactions.py` and `commands/`, plus XML/XSD serialization and adapters. |
| Schema Guy (`schema_guy`) | 6% | Own XSD schema design, versioning, and instance-fixture validation across the project. |
| Web Interface Guy (`web_interface_guy`) — **reserve** | 0% | Remains unstaffed until a web dashboard or REST surface is explicitly scoped. |
| CAD Asset Importer (`cad_asset_importer`) | 5% | Parse and normalize acquired geometry into the equipment-catalog contract. Reject a terminal-bearing asset that lacks labelled terminal geometry and never fabricate missing vendor geometry. |
| Panel Builder (`panel_builder`) | 6% | Build typed panel/backplate, DIN rail, wire duct, terminal strip, PLC placement, relay, breaker, and pilot/annunciation objects. Use Circuit Protection SME guidance for protection-device sizing and label placeholder geometry honestly. |

## Layer 4 — independent quality and engineering review

The charter names QA Guy and Controls Engineer Guy as release-gate roles.
The [milestone review cadence](../MILESTONE_REVIEW_CADENCE.md) defines the
evidence required for each milestone; review reports must be independent and
record their inspected scope, findings, and disposition.

| Role and ID | Planned effort | Detailed remit |
| --- | ---: | --- |
| QA Guy (`qa_guy`) | 8% | Independently inspect implementation, tests, identity and persistence invariants, and documentation claims across the relevant project surface. Classify severity and approve, approve with follow-ups, or require changes. |
| FreeCAD Guy (`freecad_guy`) | 6% | Inspect workbench lifecycle, command registration, FeaturePython proxies, transactions, FCStd persistence, and manual GUI acceptance. Identify regressions a headless test cannot establish. |
| Controls Engineer Guy (`controls_engineer_guy`) | 6% | Review PLC/panel/I/O semantics, electrical graph continuity, catalog/export truthfulness, and the load-to-protection path. Use the [load and protection playbook](layer_4/controls_engineer_guy/CONTROLS_ENGINEER_LOAD_PROTECTION_PLAYBOOK.md), [source library](layer_4/controls_engineer_guy/CONTROLS_ENGINEER_LOAD_PROTECTION_SOURCES.md), and [evaluation cases](layer_4/controls_engineer_guy/CONTROLS_ENGINEER_LOAD_PROTECTION_EVALUATION.md). Keep ratings, settings, conductor choices, SCCR, safety, and code claims open until the applicable source, SME consultation, and qualified project review exist. |

## Layer 5 — documentation and traceability

| Role and ID | Planned effort | Detailed remit |
| --- | ---: | --- |
| Docu Nerd (`docu_nerd`) | 3% | Keep architecture and TODO documentation aligned with verified behavior; review public comments and docstrings for clarity and sufficiency. |
| Historian (`historian`) | 2% | Maintain `CHANGELOG.md` and the decision/milestone history, recording why choices were made as well as what changed. |
| README Guy (`readme_guy`) | 2% | Own `README.md` as the entry point for a new contributor or user discovering the repository. |
| Manual Guy (`manual_guy`) | 3% | Own in-FreeCAD walkthroughs, tutorials, and ordered manual GUI acceptance procedures with Report View evidence capture. |

## Cross-role rules

- A motor-circuit protection or sizing change requires separate Circuit
  Protection SME and Motor Sizing SME consultations; Layer 4 checks both.
- Vendor assets enter through Catalog SME guidance, Scout provenance and
  rights checks, then Importer normalization. Placeholder geometry stays
  labelled as such.
- Competitor-format compatibility needs a real-tool validation procedure.
- Automated tests and agent reviews are evidence, not a substitute for
  project-specific qualified engineering review or manual FreeCAD acceptance.
- The [operations ledger](../AGENT_OPERATIONS_LEDGER.md) records milestone
  ownership, consultations, review evidence, and unresolved gates.
