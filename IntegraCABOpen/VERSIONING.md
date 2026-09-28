# Versioning Policy

Use Semantic Versioning: `MAJOR.MINOR.PATCH`.

During initial development, use `0.y.z`. Anything may change before `1.0.0`, but breaking changes must still be recorded in the changelog.

## Versioned artifacts

| Artifact | Version field | Compatibility concern |
|---|---|---|
| FreeCAD workbench code | `package.xml/version` | Command names, object properties, import paths |
| Python package | `pyproject.toml/version` | Public Python APIs |
| CEProject XML schema | `schemaVersion` and XSD filename | XML compatibility |
| Example projects | embedded `schemaVersion` | Demo reproducibility |
| Generated exports | generator version row/header | Downstream imports |
| Documentation | document revision | User-facing workflow traceability |

## Required release checklist

- Update `CHANGELOG.md`.
- Update `package.xml` version.
- Update `pyproject.toml` version.
- Validate XML examples against the XSD.
- Run tests.
- Create a release tag.
