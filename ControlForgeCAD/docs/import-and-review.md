# Import and Review project data

`CE_ImportAndReview` is the explicit project-import entry point in **Controls /
Automation**. It stages a file first, shows only changed supported project
fields, and applies only the checkboxes the user approves. Cancelling the
dialog—or pressing Apply with no checked fields—does not import project data.

## Supported phase-1 inputs

- CEProject XML intake documents (`.xml` and XML content).
- Lightweight setup YAML/YML notes.
- PlantUML/UML setup notes (`.uml`, `.puml`, `.plantuml`) using the existing
  supported key/value adapter.

The preview currently covers project/intake, PLC/I/O, power, and enclosure form
fields that the existing adapters understand. CEProject XML source text is
remembered on the project only after an approved apply. Parser warnings are
shown in the review dialog; unsupported input is not silently converted.

## Safe workflow

1. Select **Import and Review Project Data**.
2. Select a supported file and inspect each proposed current → imported value.
3. Check only the items to approve, then apply.
4. Run **Validate Controls Project** and resolve warnings before allocating I/O
   or creating electrical paths.

Application occurs inside one FreeCAD document transaction. The command does
not yet create imported PLC occurrences, field devices, terminals, wires,
connection paths, vendor PLC projects, or electrical-compliance conclusions.
Those need separate staged schemas and conflict rules before they can be
offered for approval.
