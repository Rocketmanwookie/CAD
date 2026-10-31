# JSON-First Data Contract Migration — Design

## Intent

Move integraCAD Open from XML/XSD-based internal and project interchange
contracts to JSON/JSON Schema. The workbench must allocate I/O from its bundled
catalog without the user selecting or importing any catalog file. Existing
CEProject and connection-path XML files remain acceptable import inputs and are
converted into the matching JSON representation; XML is no longer emitted or
used as a runtime catalog format.

The migration also restores the visible I/O-count workflow step. The current
workflow cannot reliably reach PLC allocation because the count command is
registered but omitted from the active workflow toolbar/menu. Without typed
counts, the configurator cannot find a feasible CPU and allocation lacks the
required selected PLC tuple.

## Goals

- Make JSON the sole format for all newly created or exported project,
  connection-path, hardware-catalog, panel-catalog, equipment-catalog,
  equipment-record, and technical-document-registry data.
- Validate all shipped JSON documents with versioned JSON Schemas.
- Retain the existing data model, stable CE identities, controlled roles,
  allocation result, canonical ordering, review gate, and error behaviour.
- Provide read-only legacy XML import compatibility that converts every
  supported XML payload to the equivalent JSON model before staging or
  persistence.
- Make I/O Count visible in the workflow so a user can configure and allocate
  I/O without importing a project XML file.
- Remove XML from the normal user-facing workflow, documentation, examples,
  commands, and generated filenames.

## Non-goals

- No change to PLC capacity rules, 20-percent-spare calculation, channel
  allocation, electrical-path topology, or engineering authority boundaries.
- No conversion of arbitrary/unknown third-party XML; only supported CEProject
  and connection-path XML versions are accepted.
- No automatic migration of an existing saved FreeCAD document until the user
  imports or exports project data. FreeCAD document properties remain their
  current serialized Python/FreeCAD representation.
- No vendor-project-file generation or claim of vendor compatibility.

## Approaches considered

1. Convert only the PLC runtime catalog and leave CEProject XML unchanged.
   This unblocks allocation quickly but retains two data-contract families and
   does not meet the requested JSON-first project interchange direction.
2. Convert all runtime/reference catalogs while retaining CEProject XML.
   This normalizes application resources but still leaves the project source of
   truth and user workflow XML-centred.
3. Convert all contracts to JSON and retain XML only as a read/convert legacy
   bridge. **Selected.** It provides one active data family, preserves existing
   project access, and avoids an irreversible compatibility break.

## Canonical JSON contracts

Each JSON document has a top-level `schemaVersion` and deterministic
serialization using UTF-8, two-space indentation, sorted semantic collections,
and a trailing newline. JSON object-key ordering is deterministic but consumers
must not infer semantic meaning from object order.

### CEProject

New CEProject documents use `.ceproject.json` and retain the existing logical
sections as JSON properties:

```json
{
  "schemaVersion": "0.2.0",
  "projectId": "CE-001",
  "ceIdentity": "...",
  "ceRole": "project",
  "metadata": { "name": "..." },
  "contacts": [],
  "intake": { "deliverables": [], "fields": [], "questions": [] },
  "sourceRecords": [],
  "validationFindings": [],
  "missingDataMatrix": [],
  "connectionPaths": []
}
```

Arrays are sorted by their existing identity keys: contacts by `contactId`,
fields by `fieldId`, questions by `questionId`, sources by `sourceId`, findings
by `findingId`, missing-data rows by `itemId`, and paths by CE identity.

### Connection paths

Connection paths move from the dedicated XML namespace to an embedded JSON
object in `connectionPaths` and a standalone `.connection-path.json` contract.
The object retains path/terminal/wire identities, endpoint ownership, ordered
terminal and wire chains, route points, conductor metadata, and semantic
continuity validation.

### Catalogs and registries

The shipped resource files become JSON:

- `plc_catalog.json`
- `panel_catalog.json`
- `equipment_catalog.json`
- `siemens_s7_1200_2017.json`
- `technical_document_registry.json`

Their Python loaders consume JSON only. `plc_catalog.json` is packaged with the
workbench and loaded automatically; users never pick it in the I/O workflow.

## JSON Schema and validation

Replace each active XSD with a Draft 2020-12 JSON Schema under
`ControlForgeCAD/schemas/`, named after the new contract. The implementation
uses only the standard library for runtime parsing. A lightweight internal
validator enforces required keys, primitive types, IDs, role values, reference
integrity, ranges, and semantic invariants already enforced by existing
parsers. JSON Schema files are published as contract documentation and tested
for valid JSON and expected identifiers; adding a third-party validator is
deferred unless a product need requires full JSON Schema evaluation.

## Legacy XML conversion

`legacy_xml.py` is an isolated import-only adapter. It reuses the current XML
parsers while they remain available, then translates their parsed domain
objects into canonical JSON document models. Import dispatch is based on file
extension plus safe content sniffing:

- `.ceproject.json` and JSON content: parse as native JSON;
- `.connection-path.json`: parse as native JSON;
- supported `.xml` CEProject or connection-path content: parse through the
  legacy adapter, generate a warning that identifies the conversion, then
  stage the canonical JSON model;
- unsupported XML: fail closed with an actionable error.

Legacy XML remains import-only during one documented compatibility release. It
is never re-exported and is not written back over the source file. The import
review record stores the original source pathname, detected legacy format,
canonical JSON text, and a conversion warning so provenance remains visible.

## Application boundary changes

- Replace `ceproject_xml.py` public write/read functions with a JSON model and
  serializer/parser module. Retain narrowly named XML adapter functions only in
  the legacy adapter during compatibility support.
- Rename/export command behaviour to **Export CEProject JSON** and write
  `~/integracad_ceproject.json`.
- Update Import and Review, intake import selectors, remembered-source records,
  user-facing messages, example projects, and docs to refer to JSON.
- Change runtime loaders in `hardware_catalog.py`, `panel_hardware_catalog.py`,
  `equipment_catalog.py`, and technical-document registry code to default to
  their JSON resources.
- Update vendor-asset and layout call sites only insofar as their loader input
  changes; their allocation and selection outputs remain unchanged.
- Add `CE_IOCount` to `WORKFLOW_COMMANDS` between job intake and PLC
  configuration. The actual allocation command remains a supporting tool for
  compatibility; saving PLC Configuration may continue to materialize the
  allocation as it does today.

## Migration sequence

1. Add JSON domain models, deterministic serializers/parsers, JSON Schemas,
   and round-trip tests alongside existing XML behavior.
2. Add legacy XML-to-model adapters and fixture tests proving XML input produces
   the same canonical JSON model as native JSON input.
3. Switch CEProject import/export and GUI language to JSON; retain legacy XML
   detection as import-only.
4. Convert shipped runtime/reference catalogs and update their loaders/tests.
5. Add visible I/O Count workflow command and an end-to-end headless workflow
   regression: intake → counts → PLC selection → allocation without any import.
6. Convert examples/docs/templates and remove active XML/XSD references.
7. Keep legacy XML fixtures only under a clearly named compatibility-test
   location; delete active XML resources and XSDs once the compatibility tests
   no longer need them.

## Validation and acceptance

- Native JSON CEProject round trip preserves every currently supported field,
  source, question, validation finding, missing-data row, and connection path.
- Legacy CEProject and connection-path XML fixtures convert to equal canonical
  JSON models, with a conversion warning and no silent data loss.
- Every shipped JSON catalog loads successfully and has source-reference,
  capacity, and deterministic-order checks equivalent to current tests.
- The I/O Count command is present in the toolbar/menu and the headless
  workflow can allocate a selected CPU after counts are entered, without any
  project or catalog import.
- The complete automated suite, compilation check, and manual native-FreeCAD
  allocation/save/reopen/export acceptance run pass.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Legacy data loss | Convert through existing proven parsers; compare parsed domain models; fail closed on unsupported elements. |
| Schema drift | Version every contract, deterministic fixtures, and explicit migration tests. |
| Silent allocation behavior change | Preserve existing allocation functions and assert identical allocation results for equivalent catalog data. |
| Partial document mutation | Keep import review and transaction boundaries; conversion completes before any project property is changed. |
| User confusion during transition | File filters, clear conversion warnings, `JSON` command/menu labels, and documentation migration notes. |

## Open implementation calls

- The first JSON format version is `0.2.0` to distinguish it from CEProject XML
  `0.1.0` without implying XML and JSON are byte-level interchangeable.
- JSON Schema files are contract artifacts, while Python semantic validation
  remains authoritative for graph continuity and allocation rules.
- XML adapters are isolated and will be removed only in a later explicitly
  announced breaking release after legacy-import support is retired.
