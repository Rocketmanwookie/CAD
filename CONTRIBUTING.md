# Contributing to integraCAD Open

Thank you for contributing to **integraCAD Open**. The project develops controls-engineering data, validation, layout, and documentation workflows around the **ControlForgeCAD** FreeCAD workbench.

## Project identity

- **integraCAD Open** is the overall open-source controls-engineering CAD project.
- **ControlForgeCAD** is the FreeCAD workbench implementation located in `ControlForgeCAD/`.
- `CE_Project` is the principal FreeCAD project object.
- `CE_` identifies controls-engineering workbench commands.

Use these names consistently in code, documentation, issues, and pull requests. Treat IntegraCAB references as legacy naming unless compatibility with an existing artifact requires them.

## Architectural source of truth

Read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) before changing:

- system or module boundaries;
- dependency direction;
- FreeCAD object contracts;
- project/intake fields;
- validation or missing-data rules;
- XML or CSV output contracts;
- layout-object roles;
- extension points; or
- implemented-versus-planned capability claims.

A contribution that changes any of these must update the architecture document in the same change.

## Development workflow

1. Create a focused branch from the current development branch.
2. Keep changes limited to one coherent capability, correction, or documentation topic.
3. Identify the affected architecture layer and public contracts.
4. Add or update tests for behavioral changes.
5. Run the repository validation commands:

```bash
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

6. Validate relevant GUI behavior in FreeCAD when changing commands, dialogs, document objects, object properties, workbench initialization, or command-driven exports.
7. Update all documentation affected by the change.
8. Add a concise entry under `Unreleased` in [`CHANGELOG.md`](CHANGELOG.md).
9. Open a pull request that explains the problem, implementation, architecture impact, validation performed, generated-artifact impact, and known limitations.

## Architecture boundaries

Contributions must preserve the separation between:

1. **FreeCAD UI layer** — workbench registration, commands, menus, toolbars, and dialogs.
2. **FreeCAD adapter layer** — document objects, properties, persistence, and conversion of FreeCAD state into backend inputs.
3. **Application service layer** — project-intake, validation, missing-data, layout, and export orchestration.
4. **Domain layer** — controls-project, intake, I/O, hardware/layout, and validation contracts.
5. **Boundary services** — deterministic XML and CSV serialization.
6. **Tests and fixtures** — pure-Python verification plus documented GUI checks where required.

Avoid embedding domain rules directly in toolbar commands or dialogs when the rule can live in a testable backend module.

### Dependency rules

Allowed:

- GUI commands may depend on adapters and application services.
- adapters may depend on domain contracts and FreeCAD APIs.
- application services may depend on domain logic and serializers.
- serializers may depend on normalized domain snapshots.

Prohibited or strongly discouraged:

- domain modules depending on FreeCAD GUI or PySide widgets;
- serializers reading active-document global state directly;
- validation rules displaying message boxes;
- command classes defining XML/CSV schemas;
- vendor-specific identifiers becoming mandatory core-domain fields;
- pure-domain tests requiring FreeCAD GUI startup.

## Contract-change checklists

### Adding or changing a project field

Review and update, where applicable:

- the domain/intake contract;
- the `CE_Project` property specification;
- FreeCAD-to-domain normalization;
- missing-value semantics;
- validation rules and finding paths;
- XML, BOM, or I/O-list serializers;
- automated tests;
- manual FreeCAD verification steps;
- architecture documentation; and
- changelog entry.

### Adding or changing a FreeCAD document object

Define:

- stable role or type identification;
- human-readable label behavior;
- parent/containment expectations;
- persistence requirements;
- geometry status: production, simplified, or placeholder;
- BOM/export eligibility;
- validation behavior; and
- behavior when optional metadata is missing.

### Adding or changing an export

An exporter must:

- accept a normalized domain snapshot;
- produce deterministic output;
- avoid mutating the FreeCAD document;
- define ordering and missing-value behavior;
- handle overwrite behavior explicitly;
- have pure-Python tests where practical;
- document schema or column changes; and
- update the changelog when contributor- or user-visible behavior changes.

### Adding a vendor integration

Vendor catalog and project-file integrations must use an adapter boundary. Core workflows must remain functional without a vendor package, website, account, or network connection. Map vendor records into neutral project/hardware contracts rather than spreading manufacturer-specific identifiers through the core domain.

## Documentation requirements

Update all documentation materially affected by a contribution. Typical files include:

- [`README.md`](README.md) for installation, commands, generated artifacts, and primary workflows;
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for system structure, contracts, data flows, dependencies, extension points, and implementation status;
- roadmap or standards documentation for planned scope;
- [`CONTRIBUTING.md`](CONTRIBUTING.md) when contributor workflow changes; and
- [`CHANGELOG.md`](CHANGELOG.md) for contributor-visible changes.

Clearly distinguish:

- **Implemented** — present and usable;
- **Partial** — starter or placeholder contract; and
- **Planned** — architectural direction not yet complete.

Do not present proposed hardware automation, vendor adapters, electrical schematic generation, or project-file generation as implemented unless the repository contains and validates that behavior.

## Changelog entries

Use the categories defined in [`CHANGELOG.md`](CHANGELOG.md): `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, or `Security`.

A useful entry states:

- what changed;
- which subsystem is affected;
- the observable impact;
- whether an output or public contract changed; and
- the related issue or pull request when available.

Do not list trivial formatting changes unless they materially affect contributors or generated documentation.

## Testing expectations

Pure-Python functionality should have automated tests. FreeCAD-dependent changes should include the strongest practical combination of:

- unit tests for backend logic;
- deterministic serializer tests;
- property-specification and object-contract tests;
- import and compile checks;
- command-registration checks;
- fallback-path checks; and
- documented manual GUI validation steps.

Do not reduce existing test coverage without documenting the reason.

## Manual validation expectations

Perform relevant steps from [`README.md`](README.md) when a change affects workbench loading, command registration, dialogs, Property View behavior, `.FCStd` persistence, model-tree objects, validation messages, or generated files.

Record exactly which manual steps were performed in the pull request. Do not state that GUI behavior was validated when only pure-Python tests were run.

## Commit and pull-request quality

Use imperative, scoped commit messages, for example:

```text
feat(io): add deterministic channel numbering
fix(project): preserve intake properties after reload
docs(architecture): document export service boundary
```

Pull requests should remain reviewable and should not combine unrelated refactoring with feature work unless the refactoring is required for the feature.

A strong pull request description includes:

- problem and intended engineering outcome;
- affected architecture layer and contracts;
- implementation summary;
- automated validation results;
- manual FreeCAD validation results;
- generated-artifact or schema changes;
- documentation and changelog updates; and
- known limitations or planned follow-up.
