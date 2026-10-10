# SME consultation receipt

Use this receipt for a milestone that changes or publicly claims anything
affected by a Layer 0 subject-matter expert. Store the completed receipt in
[`AGENT_OPERATIONS_LEDGER.md`](AGENT_OPERATIONS_LEDGER.md), a pull request, or
an issue; this file is the reusable format, not a log of consultations that
did not occur.

## When a receipt is required

| Change or claim | Required consultation |
|---|---|
| IEC or NFPA/JIC symbols, terminology, or code-profile behavior | Applicable IEC and/or NFPA/JIC Standards SME |
| Siemens S7-1200 catalog or engineering assertion | Siemens S7-1200 SME |
| FreeCAD lifecycle, Addon Manager, FeaturePython, or Cables integration boundary | FreeCAD API SME when established project knowledge is insufficient |
| PLCopen, AutomationML/CAEX, OPC UA, or external standards adapter | Standards Adapter SME |
| Proprietary ECAD/CAD compatibility or round-trip claim | Competitor Format Adapter SME and a recorded real-tool validation procedure |
| Vendor asset acquisition or manufacturer-accurate geometry claim | Vendor Catalog SME before CAD Asset Scout/Importer work |
| Conductor, protective-device, overload, SCCR, or motor-circuit sizing behavior | Applicable sizing/protection SME; motor protection or sizing requires both Circuit Protection and Motor Sizing SMEs |

## Receipt

```text
Milestone / candidate commit:
Question and scope:
Consulted charter role:
Source title, publisher, version or revision, and publication/access date:
Exact locator (page, section, table, URL fragment, or artifact checksum):
Source freshness / next recheck date:
SME conclusion and uncertainty or boundary:
Required implementation or documentation action:
Layer 4 reviewer and disposition:
Evidence link:
```

## Rules

- Cite an authorized source. Do not copy restricted standards text into the
  repository.
- A source locator alone is not a consultation receipt: record the conclusion
  and the Layer 4 disposition.
- A receipt advises the milestone; it does not itself approve a merge.
- For motor-circuit protection or sizing, attach two receipts—one from
  `circuit_protection_sme` and one from `motor_sizing_sme`. Neither can sign
  off alone.
- If the source, expert, or qualified project-specific review is unavailable,
  record that limitation and do not claim code, safety, vendor, or
  commissioning compliance.
