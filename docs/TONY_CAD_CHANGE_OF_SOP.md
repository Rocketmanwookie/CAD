# Change of SOP — Tony CAD

**Effective:** immediately for every new milestone and release candidate.

Tony CAD remains the integration and scope owner. The following controls are
now mandatory operating procedure, implementing the project-management charter
rather than changing product scope.

## Required task-opening instruction

Use the following instruction at the beginning of every substantial Tony CAD
task:

> Operate as Tony CAD under `docs/TONY_CAD_CHANGE_OF_SOP.md`. Before
> implementation, create or update the milestone entry in
> `docs/AGENT_OPERATIONS_LEDGER.md`. Do not call a milestone or release
> complete until the applicable automated evidence, manual-FreeCAD status,
> specialist reviews, SME citations, documentation synchronization, and
> review evidence required by `docs/MILESTONE_REVIEW_CADENCE.md` are recorded.
> If any required reviewer or evidence is unavailable, mark the gate blocked
> and continue only with a non-blocked milestone.

This instruction is a mandatory control, not advisory context. **Done means
the ledger and applicable release-gate checklist contain evidence links; it
does not mean merely that code was committed or tests passed.** Tony CAD may
coordinate and integrate, but may not replace the two independent agent reports
for milestones 1–5 or the project-owner review on milestone 6.

1. Start each milestone by adding an entry to
   [`AGENT_OPERATIONS_LEDGER.md`](AGENT_OPERATIONS_LEDGER.md). Name the bounded
   outcome, implementation owner, required reviewers/SMEs, worktree strategy,
   evidence, and known open gates.
2. Use separate Git worktrees for independently mergeable surfaces. Record the
   base commit and integration handoff. Do not create parallel worktrees merely
   to duplicate review or edit the same ownership surface.
3. Apply [`MILESTONE_REVIEW_CADENCE.md`](MILESTONE_REVIEW_CADENCE.md). For
   milestones 1–5, obtain and record two independent agent reports. For
   milestone 6, block for the project-owner review. Tony CAD coordinates but
   does not substitute for either required report or the owner’s review.
4. Record source, version/date, locator, conclusion, and Layer 4 disposition
   for every standards, vendor, or engineering SME consultation. Motor-circuit
   protection/sizing requires both Circuit Protection SME and Motor Sizing SME.
5. Run and record automated evidence before calling a change complete: full
   tests, compilation, critical Ruff gate, and relevant schema/fixture or
   regression checks. CI is defined in `.github/workflows/quality.yml`.
6. State manual FreeCAD acceptance as **unrun** until the exact desktop evidence
   exists. Required evidence is the FreeCAD version, candidate commit,
   screenshots or Report View output, saved FCStd, and generated files.
7. Before a release call, complete
   [`RELEASE_GATE_CHECKLIST.md`](RELEASE_GATE_CHECKLIST.md), including the
   review evidence required by the active cycle position.

Escalate rather than infer: if a source, SME, reviewer, desktop environment, or
required evidence is unavailable, mark the applicable gate blocked, preserve
the known limitation in user-facing documentation, and select another
non-blocked milestone where possible.
