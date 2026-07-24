# Contributing to integraCAD Open

Thank you for contributing to integraCAD Open. The project develops controls-engineering workflows and data models around the ControlForgeCAD FreeCAD workbench.

## Project identity

- **integraCAD Open** is the overall open-source controls-engineering CAD project.
- **ControlForgeCAD** is the FreeCAD workbench implementation located in `ControlForgeCAD/`.

Use these names consistently in code, documentation, issues, and pull requests.

## Development workflow

1. Create a focused branch from the current development branch.
2. Keep changes limited to one coherent capability, correction, or documentation topic.
3. Add or update tests for behavioral changes.
4. Run the repository validation commands:

```bash
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

5. Validate relevant GUI behavior in FreeCAD when changing commands, dialogs, document objects, or workbench initialization.
6. Update documentation affected by the change.
7. Add a concise entry under `Unreleased` in [`CHANGELOG.md`](CHANGELOG.md).
8. Open a pull request that explains the problem, implementation, validation performed, and known limitations.

## Architecture boundaries

Contributions should preserve the separation between:

- FreeCAD GUI commands and dialogs.
- FreeCAD document-object adapters and properties.
- Domain models for controls projects, intake data, I/O, hardware, and validation.
- Import/export services for XML, CSV, BOM, and future vendor integrations.
- Tests and fixtures that can run without requiring a FreeCAD GUI where practical.

Avoid embedding domain rules directly in toolbar commands or dialogs when the rule can live in a testable backend module.

## Documentation requirements

Update all documentation materially affected by a contribution. Typical files include:

- `README.md` for installation, commands, and primary workflows.
- `docs/ARCHITECTURE.md` for system structure and design decisions.
- Roadmap or standards documentation for scope and future work.
- [`CHANGELOG.md`](CHANGELOG.md) for contributor-visible changes.

Clearly distinguish implemented behavior from planned architecture.

## Changelog entries

Use the categories defined in [`CHANGELOG.md`](CHANGELOG.md): `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, or `Security`.

A useful entry states:

- what changed;
- which subsystem is affected;
- the observable impact;
- the related issue or pull request when available.

Do not list trivial formatting changes unless they materially affect contributors or generated documentation.

## Testing expectations

Pure-Python functionality should have automated tests. FreeCAD-dependent changes should include the strongest practical combination of:

- unit tests for backend logic;
- import and compile checks;
- command registration checks;
- documented manual GUI validation steps.

Do not reduce existing test coverage without documenting the reason.

## Commit and pull-request quality

Use imperative, scoped commit messages, for example:

```text
feat(io): add deterministic channel numbering
fix(project): preserve intake properties after reload
docs(architecture): document export service boundary
```

Pull requests should remain reviewable and should not combine unrelated refactoring with feature work unless the refactoring is required for the feature.
