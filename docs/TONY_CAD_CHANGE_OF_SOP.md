# Change of SOP — Tony CAD

**Effective:** immediately for every new milestone and release candidate.

Tony CAD remains the integration and scope owner. The following controls are
now mandatory operating procedure, implementing the project-management charter
rather than changing product scope.

1. Start each milestone by adding an entry to
   [`AGENT_OPERATIONS_LEDGER.md`](AGENT_OPERATIONS_LEDGER.md). Name the bounded
   outcome, implementation owner, required reviewers/SMEs, worktree strategy,
   evidence, and known open gates.
2. Use separate Git worktrees for independently mergeable surfaces. Record the
   base commit and integration handoff. Do not create parallel worktrees merely
   to duplicate review or edit the same ownership surface.
3. Treat QA Guy, FreeCAD Guy, Controls Engineer Guy, and Layer 0 SMEs as
   evidence-bearing reviewers. Tony CAD coordinates their work but does not
   substitute for an unavailable independent reviewer.
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
   [`RELEASE_GATE_CHECKLIST.md`](RELEASE_GATE_CHECKLIST.md). QA Guy and
   Controls Engineer Guy must independently record their decisions; only then
   may Tony CAD make the integration disposition.

Escalate rather than infer: if a source, SME, reviewer, desktop environment, or
required evidence is unavailable, mark the applicable gate blocked, preserve
the known limitation in user-facing documentation, and select another
non-blocked milestone where possible.
