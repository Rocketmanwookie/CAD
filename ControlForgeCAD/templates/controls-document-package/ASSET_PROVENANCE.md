# Asset provenance register — blocked intake

This register makes the current intake state auditable. It does **not** grant
permission to redistribute, edit, generate, or represent any package asset as
an approved engineering deliverable.

## Package snapshot

| Field | Recorded value |
|---|---|
| Repository location | `ControlForgeCAD/templates/controls-document-package/` |
| Intake description | Project-owner-supplied controls-document source package |
| Access/intake date | 2026-10-06 (commit history) |
| Snapshot Git tree object | `204eafdace420246ad3a36d68b2e41a10fad4383` |
| Inventory digest | SHA-256 `f310014ab430173a7fb017feb6e2cda37514f2a67e5e575a560730505d81e7a2` over sorted `git ls-tree -r HEAD` blob-ID/path records for this directory |
| Files in snapshot | 38 |
| Source locator and revision | Not recorded — blocked |
| Copyright/license and redistribution authority | Not recorded — blocked |
| Asset-review disposition | Not reviewed; do not treat package contents as approved templates |

## Required evidence before use

1. Record the original authorized source or project-owner locator, source
   revision, and access date.
2. Record copyright, license, or explicit redistribution permission for the
   PDF, DXF, Markdown, and CSV material.
3. Recompute and record file-level checksums if an approved source is
   established or any source asset changes.
4. Obtain the applicable Layer 0 SME and Layer 4 reviewer disposition for
   standards, safety, fail-safe, or engineering claims retained in the
   package.

Until then, the controlling disposition is the blocked asset-intake milestone
in [`docs/AGENT_OPERATIONS_LEDGER.md`](../../../docs/AGENT_OPERATIONS_LEDGER.md).
