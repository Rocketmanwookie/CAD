# Milestone review cadence

**Effective:** immediately, by project-owner direction.

This cadence replaces the standing two-person GitHub-approval requirement for
ordinary milestones. It preserves the required automated-verification workflow
and evidence rules; it changes who supplies review evidence and when a
project-owner review is mandatory.

## Rolling six-milestone cycle

| Cycle position | Required review evidence | Merge/release disposition |
|---|---|---|
| Milestones 1–5 | Two independent agent review reports. The agents must have different assigned roles, independently inspect the relevant surface, and record their conclusions and evidence links in the operations ledger. | Tony CAD may integrate only after automated evidence and both agent reports are recorded. No human approval is required by this cadence. |
| Milestone 6 | Project-owner review by the user, recorded as an issue/PR review, comment, or explicit ledger evidence. Agent review reports may assist but do not replace the user review. | **Blocked** until the user’s review evidence is recorded. |

The next eligible milestone starts at cycle position 1. After a milestone-6
user review, the next eligible milestone restarts at position 1. A blocked or
abandoned milestone does not consume a cycle position unless Tony CAD records
an integration disposition.

## Independence and evidence

An agent report is evidence only when it names the agent role, scope reviewed,
commit or pull request, commands/artifacts inspected, conclusion, and open
findings. Tony CAD cannot write both reports or infer either report from a test
run. Automated verification remains required for every protected-branch pull
request.

GitHub review identities represent human accounts and cannot natively attest
that an automated task is a distinct agent. Therefore the canonical record for
the two-agent requirement is the operations ledger and linked task reports,
not GitHub’s numeric approval count.
