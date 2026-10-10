# CEProject versioning and migration policy

This policy governs the public CEProject XML contract. It supplements the
workbench-wide [versioning policy](../ControlForgeCAD/VERSIONING.md) and the
configuration-management guide in
[`ControlForgeCAD/docs/version-control.md`](../ControlForgeCAD/docs/version-control.md).

## Current support boundary

The supported CEProject contract is **schema version `0.1.0`**:

- root namespace: `https://whrsdaparty.github.io/ceproject/0.1`;
- root `schemaVersion`: `0.1.0`;
- primary XSD: `ControlForgeCAD/schemas/ce_project_v0_1.xsd`; and
- ordered electrical-path vocabulary:
  `ControlForgeCAD/schemas/connection_path_v1.xsd`.

The importer reads the current exported structure and validates it through the
available schema and domain checks. It is **not** a general automatic migration
engine. A document whose `schemaVersion` is merely syntactically present must
not be presented as semantically compatible with a later or older contract
unless that compatibility is explicitly tested and documented.

## Compatibility classification

| Change | Required versioning action | Existing-document behavior |
|---|---|---|
| Documentation-only clarification; no emitted or accepted XML change | No schema version change | Existing documents remain unchanged. |
| Optional additive element/attribute that is ignored safely by older consumers and does not alter existing meaning | Maintain the current minor schema family only after compatibility tests prove it | Preserve current fixtures and test both old and new documents. |
| Required field, changed meaning, namespace change, removed/renamed element, altered identity/reference rule, or changed ordering semantics | Create a new versioned XSD/namespace family and migration note | Do not silently rewrite a project file. Provide an explicit conversion path or a clear incompatibility finding. |
| Bug fix that changes emitted XML values or parsing interpretation | Record the affected schema behavior and migration impact even if the version remains `0.1.0` during pre-1.0 development | Add regression fixtures for both the former failure and corrected behavior. |

## Required change packet

Before changing a public CEProject schema or importer/exporter behavior:

1. Schema Guy records the proposed contract, compatibility class, and affected
   public artifacts in the operations ledger.
2. Create a new, versioned XSD filename and namespace when the change is not
   demonstrably backward-compatible. Do not overwrite a released XSD.
3. Add a migration note describing source version, target version, preserved
   fields/identities, transformed fields, dropped data, failure behavior, and
   rollback or backup expectations.
4. Add valid and invalid fixtures, round-trip tests, and a test of the
   migration or incompatibility behavior.
5. Update example projects, generated-output metadata, architecture, user
   documentation, changelog, and any affected external adapter mapping.
6. Have QA Guy review the changed surface; obtain Standards Adapter SME input
   when an outward PLCopen, AutomationML, OPC UA, or related standard adapter is
   affected.

## Migration safety rules

- Preserve stable project, source-record, signal, path, terminal, and wire
  identities whenever a migration can do so without changing their meaning.
- Never overwrite an input document in place. Write a distinct target artifact
  or require an explicit user-approved transaction.
- Fail closed on unknown required semantics, conflicting IDs, unsafe reference
  changes, or data that cannot be represented in the target contract.
- Keep source facts, validation findings, and uncertainty states distinguishable
  from verified/approved facts during conversion.
- Keep vendor-specific data behind adapters; a CEProject migration does not
  establish vendor-project, safety, code, or commissioning compatibility.

## Release evidence

The release-gate packet for a schema-affecting milestone must link the changed
XSDs, fixtures, migration note, exact tests, reviewer reports, and any required
SME receipt. A manual FreeCAD gate remains separately applicable when the
schema change crosses into persisted FreeCAD object behavior.
