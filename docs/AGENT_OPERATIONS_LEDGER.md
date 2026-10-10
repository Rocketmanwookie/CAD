# Agent operations ledger

This is the durable evidence record for execution of the project-management
charter. Add one entry when a milestone starts and complete it before calling
that milestone complete. Link to pull requests, commits, task handoffs, and
evidence rather than duplicating their contents.

**Completion rule:** a milestone is not done because implementation was
committed or automated tests passed. It is done only when this ledger contains
the applicable evidence links and, for a release candidate, the corresponding
`RELEASE_GATE_CHECKLIST.md` is completed with the evidence required by
`MILESTONE_REVIEW_CADENCE.md`. Tony CAD may coordinate and integrate, but may
not substitute the two independent agent reports for cycle positions 1–5 or
the project-owner review at cycle position 6.

## Active entries

| Milestone | Scope / owner | Worktree and handoffs | Required reviews | SME evidence | Automated evidence | Manual FreeCAD evidence | Status |
|---|---|---|---|---|---|---|---|
| Phase 0 contributor-governance baseline | Tony CAD; documentation implementation with independent Docu Nerd and QA agent reports | [PR #5](https://github.com/Rocketmanwookie/CAD/pull/5), bounded candidate `919adb9`; isolated documentation/configuration surface from `4ec8847` | Cycle position 2: independent Docu Nerd and QA agent reports required; no project-owner review required | No engineering-standard interpretation in this bounded baseline; later document-package scope is separately blocked below | [Automated verification](https://github.com/Rocketmanwookie/CAD/actions/runs/36405787263) passed; local `pip-audit --strict`, tracked-secret scan, 246 tests, compilation, critical Ruff, diff check, and workflow-YAML parse passed | Not applicable — no GUI behavior changes in this bounded baseline | Superseded as the active candidate by separately recorded M1/M2/document-package work; do not use this row as evidence for later commits |
| M1 intake workflow separation | Tony CAD; workflow implementation; independent Docu Nerd and QA review required | [PR #5](https://github.com/Rocketmanwookie/CAD/pull/5), implementation `7d5836d`, current candidate `7dfc685`; plant intake and I/O sizing separated | Cycle position 2: [independent Docu Nerd and QA block reports](https://github.com/Rocketmanwookie/CAD/pull/5#issuecomment-6101436696); no project-owner review required | No standards consultation recorded; feature behavior is not an engineering-compliance claim | [Current CI run](https://github.com/Rocketmanwookie/CAD/actions/runs/37466701977) passed 257 tests and critical Ruff; local CI-equivalent rerun at `7dfc685` passed 257 tests, compilation, critical Ruff, and applicable whitespace check | Unrun — GUI workflow changed; manual FreeCAD acceptance remains required | **Blocked:** reports require dedicated milestone evidence and manual FreeCAD acceptance before integration |
| M2 PLC configurator and spare-aware allocation | Tony CAD; workflow implementation; independent Docu Nerd and QA review required | [PR #5](https://github.com/Rocketmanwookie/CAD/pull/5), implementation `86eed6f`, current candidate `7dfc685`; PLC configuration, allocated-point labels, and spare-aware allocation | Cycle position 2: [independent Docu Nerd and QA block reports](https://github.com/Rocketmanwookie/CAD/pull/5#issuecomment-6101436696); no project-owner review required | No final hardware approval; 20% spare behavior is a product rule pending appropriate engineering review if promoted as a standards claim | [Current CI run](https://github.com/Rocketmanwookie/CAD/actions/runs/37466701977) passed 257 tests and critical Ruff; local CI-equivalent rerun at `7dfc685` passed 257 tests, compilation, critical Ruff, and applicable whitespace check | Unrun — configurator and allocation workflow need desktop evidence | **Blocked:** reports require dedicated milestone evidence and manual FreeCAD acceptance before integration |
| Supplied controls-document package intake | Tony CAD; imported source templates and reference assets; independent Docu Nerd and QA review required | [PR #5](https://github.com/Rocketmanwookie/CAD/pull/5), introduced after `919adb9` under `ControlForgeCAD/templates/controls-document-package/`, current candidate `7dfc685` | Cycle position 2: [independent Docu Nerd and QA block reports](https://github.com/Rocketmanwookie/CAD/pull/5#issuecomment-6101436696); no project-owner review required | Source, revision/access date, redistribution rights, practical checksums, and reviewer disposition are not yet recorded; standards/safety wording is unverified pending the applicable SME/Layer 4 disposition | [Current CI run](https://github.com/Rocketmanwookie/CAD/actions/runs/37466701977) passed repository verification; that does not verify asset provenance | Not applicable — assets are not current GUI behavior | **Blocked:** do not present, generate, or release these assets as approved templates until provenance and applicable SME evidence are recorded |
| Milestone review-cadence migration | Tony CAD; repository-governance owner | [PR #4](https://github.com/Rocketmanwookie/CAD/pull/4), corrective candidate `a950b31`; ledger-evidence follow-up pending | Cycle position 1: [QA Guy and Controls Engineer Guy independent reports](https://github.com/Rocketmanwookie/CAD/pull/4#issuecomment-5867021822); no person approval required | Not applicable; governance scope | [Automated verification](https://github.com/Rocketmanwookie/CAD/actions/runs/36402561358) passed at `a950b31`; 246 local tests, compilation, critical Ruff, PR-range whitespace, YAML compatibility parse, and `lxml` import passed | Not applicable | Ready for integration after CI on this ledger-evidence update |
| Issue #2 roadmap acceptance map | Tony CAD; documentation/architecture integration | [PR #4](https://github.com/Rocketmanwookie/CAD/pull/4), corrective candidate `a950b31`; ledger-evidence follow-up pending | Cycle position 1: [QA Guy and Controls Engineer Guy independent reports](https://github.com/Rocketmanwookie/CAD/pull/4#issuecomment-5867021822); no person approval required | No new engineering claim or standards interpretation; existing source locators remain authoritative | Target-existence check; `python -m pytest -q` — 246 passed; `python -m compileall -q ControlForgeCAD` — passed; critical Ruff and PR-range whitespace passed; [PR CI run](https://github.com/Rocketmanwookie/CAD/actions/runs/36402561358) — passed | Not applicable — no GUI behavior changes | Ready for integration after CI on this ledger-evidence update; Issue #2 handoff: [comment](https://github.com/Rocketmanwookie/CAD/issues/2#issuecomment-5866825369) |
| Release-branch governance enforcement | Tony CAD; repository-governance owner | `codex/controlForgeCAD` from `b7c7431`; protected-branch PR required for integration | Superseded by the two-agent / project-owner cadence | Not applicable; repository-process scope | PR **Automated verification** workflow required on `controlforgecad` | Not applicable | Superseded by milestone review-cadence migration |
| Manual FreeCAD allocation-to-path acceptance | Tony CAD; FreeCAD Guy executes; QA Guy observes; Controls Engineer Guy releases | Current checkout; create a dedicated acceptance handoff before execution | Two independent agent reports for cycle positions 1–5; project-owner review at position 6 | Not applicable unless scope changes into motor/protection, vendor assets, or standards adapters | 246 passing tests at `b7c7431` (local audit run); rerun at candidate commit | Unrun — see `MANUAL_FREECAD_ACCEPTANCE_HANDOFF.md` | Blocked pending desktop evidence and applicable cycle review |

## Entry template

| Field | Record |
|---|---|
| Milestone and bounded outcome | |
| Tony CAD owner | |
| Roles assigned and why | |
| Worktree path / base commit | |
| Handoff links and integration commit | |
| Affected charter layers and public contracts | |
| Agent review report 1 and evidence, or project-owner review at position 6 | |
| Agent review report 2 and evidence, if applicable | |
| FreeCAD Guy decision and evidence, if applicable | |
| Layer 0 consultation: role, source/version/date/page, conclusion | |
| Motor/protection dual consultation, if applicable | |
| Automated commands and exact results | |
| Manual acceptance: performed / unrun, evidence link | |
| Documentation synchronized | |
| Known limitations / follow-up owner | |
| Final disposition | |

## Operating rules

Workflow restructuring, 2026-10-06: primary owner implemented separate plant
and I/O-count steps, updated milestones and governing workflow, imported the
owner-supplied scope/document assets, and retired the combined intake entry
from visible navigation. Automated evidence: 254 regression tests passed;
desktop acceptance is pending per WORKFLOW_MILESTONES.md. This is a development
checkpoint, with release review and FreeCAD acceptance still open. The next
implementation item is the PLC configurator and I/O definition table.

Continuation on 2026-10-06: checkpoint `7d5836d` pushed to
`codex/phase0-contributor-governance`. Added the dedicated PLC configurator,
allocated-point label entry and spare-aware project allocation. Verification:
257 regression tests, compilation, critical Ruff and whitespace checks passed.
Desktop acceptance and broader I/O table/import work remain open; see the M2
checkpoint in WORKFLOW_MILESTONES.md. The unrelated charter edit is excluded.

1. One task may be assigned to one implementation owner; reviewers remain
   independent of that implementation work.
2. Use separate Git worktrees only for separable surfaces. Record their base
   commit and integration handoff so concurrent work is reconstructible.
3. A missing consultation or unrun manual acceptance is evidence of an open
   gate, not permission to infer it passed.
4. Do not place vendor credentials, proprietary standards text, or protected
   vendor assets in this ledger. Record authorized locators and access limits.
