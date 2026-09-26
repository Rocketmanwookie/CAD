# Import and Review project data

`CE_ImportAndReview` is the explicit project-import entry point in **Controls /
Automation**. It stages a file first, shows only changed supported project
fields and logical-I/O rows, and applies only the checkboxes the user approves.
Cancelling the dialog—or pressing Apply with no checked items—does not import
project data.

## Supported phase-1 inputs

- CEProject XML intake documents (`.xml` and XML content).
- Lightweight setup YAML/YML notes.
- PlantUML/UML setup notes (`.uml`, `.puml`, `.plantuml`) using the existing
  supported key/value adapter.

The preview covers project/intake, PLC/I/O, power, and enclosure form fields
that the existing adapters understand. For an existing CEProject XML `Signals`
section, it additionally stages one logical I/O candidate per supported `DI`,
`DO`, `AI`, or `AO` signal. A candidate can add a new unallocated logical row
or update only the readable label of an existing same-tag/same-type row.

CEProject XML source text is remembered on the project after either an approved
field or I/O-row apply. Parser warnings and conflicts are shown in the review
dialog; unsupported input is not silently converted.

## Safe workflow

1. Select **Import and Review Project Data**.
2. Select a supported file and inspect each proposed current → imported value
   and, for CEProject XML signals, each logical-I/O candidate.
3. Check only the items to approve, then apply. Conflicted I/O rows are shown
   but cannot be approved.
4. Run **Validate Controls Project**, then run **Allocate PLC I/O** before
   creating electrical paths.

Application occurs inside one FreeCAD document transaction. The I/O review has
a source-and-current-state fingerprint, so it rejects a stale decision before
writing, and it fails closed if an existing persisted I/O row is malformed or
tagless rather than discarding it. Imported `plcAddress` and `terminal`
attributes are reference-only and are never applied: catalog allocation creates
canonical rack/slot/channel, terminal, and part data. The command does not yet
create imported PLC occurrences, field devices, terminals, wires, connection
paths, vendor PLC projects, or electrical-compliance conclusions. Those need
separate staged schemas and conflict rules before they can be offered for approval.
