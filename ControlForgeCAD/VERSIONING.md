# Versioning Policy

Use Semantic Versioning: `MAJOR.MINOR.PATCH`.

```text
MAJOR: incompatible public API, XML schema, or file format changes
MINOR: backward-compatible features
PATCH: backward-compatible fixes
```

During initial development, use `0.y.z`. Anything may change before `1.0.0`, but breaking changes must still be recorded in the changelog.

## Versioned artifacts

| Artifact | Version field | Compatibility concern |
|---|---|---|
| FreeCAD workbench code | `package.xml/version` | Command names, object properties, import paths |
| Python package | `pyproject.toml/version` | Public Python APIs |
| CEProject XML schema | `schemaVersion` and XSD filename | XML compatibility |
| Example projects | embedded `schemaVersion` | Demo reproducibility |
| Generated BOM format | export version row/header | Downstream spreadsheet imports |
| Generated I/O list format | export version row/header | PLC import scripts |
| Documentation | document revision | User-facing workflow traceability |

## Git branch model

```text
main          stable integration branch
dev           active development branch
feature/*     short-lived feature branches
release/*     release-hardening branches
hotfix/*      urgent fixes against latest release
```

## Required release checklist

- Update `CHANGELOG.md`.
- Update `package.xml` version.
- Update `pyproject.toml` version.
- Validate all XML examples against the XSD.
- Run tests.
- Render documentation if PDFs are included.
- Create a release tag.
- Attach generated release artifacts.

## Configuration-management rules

- Do not overwrite a released artifact.
- Do not modify a tagged release.
- Schema changes require migration notes.
- Generated files must list the generator version.
- Examples must state the schema version they target.
- Safety/power validation rules must be traceable to source documents or engineering assumptions.
