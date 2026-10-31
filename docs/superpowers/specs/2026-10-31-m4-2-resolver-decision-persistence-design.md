# M4.2 resolver decision and persistence design

Status: proposed for project-owner review; no product-code implementation is
authorized by this document alone.

## Intent and boundary

Make the existing deterministic `ResolverSnapshot` usable as a durable,
reviewable source for later Release 1 data exports. A project reviewer must be
able to distinguish current input, a proposal, a recorded decision, and stale
evidence after input changes. This increment does not select rated devices,
calculate enclosure fit or heat, approve electrical engineering, or generate
physical CAD.

## Approaches

1. **Extend each existing export directly.** This is quick for one output, but
   each exporter would independently resolve inputs and could disagree.
2. **Persist a versioned snapshot and separate decision records, then adapt
   exports to those records.** This follows the charter's shared-source
   direction and allows stale decisions to be detected. Recommended for M4.2.
3. **Create a parallel resolver service or database.** This adds deployment and
   synchronization work before the FreeCAD project object has a stable
   contract; defer it.

The accepted roundtable recommendation favors approach 2. The exact record
shape and migration behavior below require owner review before code changes.

## Contract

- Keep `CE_Project` as the single project root. Use its existing
  `ResolverSnapshots` string-list property as an append-only history of
  canonical JSON snapshot records. A repeated generation with identical
  inputs reuses the existing snapshot identity and does not append a duplicate.
- Add a distinct versioned decision record collection to the project. Each
  record names project identity, snapshot identity, subject requirement
  identity, decision scope, disposition, reviewer identity, evidence references,
  recorded time, and accepted input digest. No agent-generated field defaults
  to qualified engineering approval. An unresolved or rejected proposal stays
  visibly unresolved.
- Validate each persisted JSON record against its published JSON Schema and
  typed parser. Reject malformed records, duplicate identities with conflicting
  payloads, wrong-project references, and unsupported major versions before a
  project mutation or export.
- Derive currentness from the newly computed snapshot identity and accepted
  input digest. Keep historical snapshots and decisions intact. If inputs
  change, mark prior decisions stale in the read model; never rewrite their
  original evidence or silently carry approval forward.
- Use one read-only resolver package builder for BOM, I/O, YAML, CEProject XML,
  CAx manifest, and cost adapters. An adapter may emit a review draft with
  explicit unresolved fields, but cannot label the package approved while any
  applicable decisions, source facts, or capacity inputs remain open. Existing
  starter exports keep their current scope until an adapter is connected and
  tested; the first adapter should demonstrate the shared identity and status
  contract without implying all six are complete.
- Do not infer reserve percent, conductor or device rating, manufacturer part,
  cost, rail/terminal positions, heat, power, or physical fit. Unknown remains
  `null` plus a named blocker. Snapshot and decision records use stable CE
  identities and an explicit schema version.

## Acceptance

Pure-Python fixtures must prove deterministic identity, append-only storage,
duplicate suppression, save/load round trip, schema rejection, wrong-project
rejection, stale-decision detection after a source change, and draft export
status with every unresolved input visible. A FreeCAD desktop run must then
prove save/reopen/recompute of the new records and the existing
allocation-to-path/edit/export workflow. Independent QA and Controls Engineer
reports must inspect the same candidate before a milestone completion call.

## Implementation choices left to the builder

Choose internal module names and whether JSON Schema validation is performed
through the project's existing validator or a lightweight explicit parser.
Keep dependencies and project-property migration minimal. Document the exact
decision schema and any version migration before introducing consumers.
