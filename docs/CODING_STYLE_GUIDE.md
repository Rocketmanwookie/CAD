# Coding style guide

## Scope

Use Python 3.11-compatible code. Keep domain/model logic independent of
FreeCAD and GUI imports; isolate FreeCAD transactions, FeaturePython proxies,
and Qt/PySide code at their adapters.

## Required practices

- Use clear, typed names and small functions with one observable purpose.
- Preserve stable CE identities, roles, persistence fields, and import/export
  contracts; do not silently normalize an invalid external identifier.
- Validate external data at boundaries and return actionable findings rather
  than inferred engineering approval.
- Wrap document mutations in the project transaction helpers and keep UI code
  from becoming the source of truth.
- Add or update focused regression tests for every behavior change.
- Run the repository verification commands before handoff: tests, compilation,
  the critical Ruff gate, and relevant schema/fixture checks.

## Review boundaries

Do not claim safety, electrical-code, manufacturer, or commissioning
compliance from a code change alone. Record required SME and review evidence in
the operations ledger.
