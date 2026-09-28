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

- [ ] QA Guy independently reviewed the affected project surface and recorded
  approve / approve-with-follow-ups / changes-required.
- [ ] Controls Engineer Guy independently reviewed PLC, panel, I/O, electrical
  graph, catalog, export, and engineering-boundary effects when applicable.
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

- QA Guy decision / evidence link:
- Controls Engineer Guy decision / evidence link:
- Tony CAD integration decision:
- Release status: approved / approved with follow-ups / blocked

The QA and Controls Engineer decisions must be independent for a release. Tony
CAD coordinates the gate and cannot replace either required approver.
