# Controls template and instance review

Review date: 2026-10-26, America/New_York. Two Controls Engineer role agents
were requested by the project owner: one reviewed and edited template Markdown,
and one independently inspected the current object model and proposed design.
These are advisory agent reviews, not qualified project engineering sign-off
or an independent QA/release approval.

## Delivered template changes

The six intake email templates now request source/revision-bound verification,
review ownership, electrical I/O characteristics, load/drive/coil demands,
power domains, supply topology and explicit drawing/functional requirements.
The I/O guide now separates stable CE identities from tags, spare channels
from actual signals, and contact states from safety-performance evidence.

The original draft
[engineering readiness supplement](../ControlForgeCAD/templates/controls-document-package/Engineering-Readiness.md)
maps those inputs to proposed feeder, PLC, PSU, switching/protection and drawing
outputs. The supplied reference package retains its blocked provenance state.
No numerical sizing, protection settings or code-compliance rules were added.
The existing JSON intake form has not yet been extended with these fields.

## Architecture findings and disposition

The actual PLC links are rack -> modules -> channels. `ElectricalDevices`
is an index, not a complete physical-parent tree. The recovered architecture
requires coil/contact and split PLC symbols to reference the same physical
device with distinct symbol occurrence identities.

The [proposed instance design](superpowers/specs/2026-10-26-verified-engineering-instances-design.md)
records physical ownership separately from circuit membership and drawing
placement. It preserves the one-project-per-document contract and adds
explicit ambiguous-root, cross-owner and cycle rejection acceptance cases.

The second Controls Engineer review requested immutable historical snapshots,
power-demand identity per consumer/interface/domain, ownership-safe
reconciliation, rollback and stale-dependency tests. Those corrections are
incorporated in the design. Template wording is being aligned to the same
physical-owner versus circuit-reference distinction.

## Implementation status and next increment

No circuit-instance generator, power-supply selector, protection-sizing
engine, symbol library or drawing renderer was implemented in this review.
The next proposed increment is verification and ownership records, followed
by verified supply -> feeder circuit records and a review manifest. It reuses
existing identities, typed requirements and JSON-first contracts. Full
single-line, three-line and electrical ladder generation depends on later
symbol, terminal and rendering adapters and actual FreeCAD acceptance.

## Planning environment

GitHub Codespaces was requested for planning. The repository is
`Rocketmanwookie/CAD`; the GitHub CLI account authenticates, but listing
Codespaces returned HTTP 403 because the token lacks the `codespace` scope.
No Codespace was created or charged by this review. Local planning documents
are ready to copy to an existing Codespace once access is authorized with
`gh auth refresh -h github.com -s codespace`.
