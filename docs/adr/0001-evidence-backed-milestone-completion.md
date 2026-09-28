# ADR 0001: Evidence-backed milestone completion

- Status: accepted
- Date: 2026-09-28
- Owners: Tony CAD, QA Guy, Controls Engineer Guy

## Context

Commits and passing automated tests demonstrate only part of a controls-CAD
milestone. The project also needs independent review evidence, truthful manual
FreeCAD status, source/SME records where relevant, and synchronized public
documentation. The charter names these controls but requires a durable,
repeatable completion rule.

## Decision

A material milestone starts with an entry in the operations ledger and is not
called complete until its applicable evidence is linked there. Cycle positions
1–5 require two independent role reports; position 6 requires project-owner
review. Tony CAD coordinates the work but cannot substitute for that evidence.
Release candidates also complete the release-gate checklist.

## Alternatives considered

- Treat merge to the development branch as completion.
- Treat a passing CI job as completion.
- Require a fixed number of GitHub account approvals for every milestone.

## Consequences

The project gains a reconstructible record of ownership, tests, consultations,
manual acceptance, and disposition. Milestones can remain correctly blocked
when a desktop environment or specialist review is unavailable. GitHub account
identity alone is insufficient evidence of distinct agent roles, so reports
must identify their scope, candidate, artifacts, findings, and conclusion.

## Evidence

- [Project-management charter](../PROJECT_MANAGEMENT_CHARTER.md)
- [Milestone review cadence](../MILESTONE_REVIEW_CADENCE.md)
- [Agent operations ledger](../AGENT_OPERATIONS_LEDGER.md)
- [Release-gate checklist](../RELEASE_GATE_CHECKLIST.md)
