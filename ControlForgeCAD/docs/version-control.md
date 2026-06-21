# Version Control and Configuration Management

## Objectives

- Reproducible development.
- Traceable exports.
- Versioned XML schemas.
- Stable release artifacts.
- Clear migration path for project files.

## Required version fields

Every generated output should include:

```text
Generator: ControlForgeCAD
GeneratorVersion: 0.1.0-dev
SchemaVersion: 0.1.0
GeneratedAt: <timestamp>
SourceProjectId: <project id>
```

## Commit conventions

Use focused commit messages:

```text
feat(plc): add generic I/O module model
fix(bom): include panel-mounted safety relays
schema(ceproject): add Connection potential attribute
docs: add safety relay circuit workflow
test: validate conveyor XML example
```

## Schema migration policy

Schema changes require:

- New XSD filename.
- Changelog entry.
- Migration note.
- Example project update.
- Test validating old and new behavior when feasible.

## Initial milestone tags

```text
v0.1.0 - workbench loads, panel object, BOM export
v0.2.0 - PLC I/O and signal registry
v0.3.0 - terminals and wiring records
v0.4.0 - ladder/logic model
v0.5.0 - safety and power models
v1.0.0 - stable public API and schema
```
