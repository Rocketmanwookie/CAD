# Release-gate checklist

Use this checklist for every release candidate and any milestone described as
complete. It implements the release gate in
[`PROJECT_MANAGEMENT_CHARTER.md`](PROJECT_MANAGEMENT_CHARTER.md). A completed
checkbox is evidence, not a substitute for qualified project-specific
engineering review.

## Candidate

- Version or milestone:
- Commit / pull request:
- Date:
- Tony CAD (integration owner):

## Automated gate

- [ ] Full test suite passed; record the exact command and result.
- [ ] `python -m compileall -q ControlForgeCAD` passed.
- [ ] Critical Ruff gate passed.
- [ ] Schema/fixture validation relevant to the change passed.
- [ ] Failure-state and regression tests cover the changed workflow.
- [ ] Dependency changes have source, license, provenance, and vulnerability-review evidence.

## Specialist and SME evidence

- [ ] For cycle milestones 1–5: two independent agent review reports are
  recorded in the operations ledger, each with role, scope, evidence, and
  conclusion. See `MILESTONE_REVIEW_CADENCE.md`.
- [ ] For cycle milestone 6: the project-owner review is recorded in the
  operations ledger, pull request, or issue. Do not substitute agent reports.
- [ ] FreeCAD Guy reviewed lifecycle, transactions, persistence, and GUI
  effects when applicable.
- [ ] Required Layer 0 consultations are recorded in the operations ledger with
  source, version/date, locator, conclusion, and Layer 4 disposition.
- [ ] For motor-circuit protection or sizing, both Circuit Protection SME and
  Motor Sizing SME consultations are recorded; neither alone is sufficient.

## Manual acceptance and public claims

- [ ] Required FreeCAD desktop checks were run and attached with FreeCAD
  version, commit, screenshots/Report View output, FCStd, and generated files.
- [ ] Or: desktop checks remain explicitly **unrun** and the candidate is not
  represented as having passed that acceptance gate.
- [ ] README, architecture, user guide, TODO/roadmap, changelog, and handoff
  were checked for behavior or boundary changes.
- [ ] Known limitations and any unrun manual tests are stated truthfully.

## Decision

- Cycle position (1–6):
- Agent review report 1 / evidence link, or project-owner review at position 6:
- Agent review report 2 / evidence link, if applicable:
- Tony CAD integration decision:
- Release status: approved / approved with follow-ups / blocked

For cycle positions 1–5, the two agent reports must be independent. At cycle
position 6, the project-owner review is mandatory. Tony CAD coordinates the
gate and cannot replace either form of required evidence.

**Evidence rule:** do not mark this candidate done based only on a commit or a
passing test run. Each applicable completed item must point to durable evidence
in the operations ledger, pull request, CI run, review, or acceptance artifact.
