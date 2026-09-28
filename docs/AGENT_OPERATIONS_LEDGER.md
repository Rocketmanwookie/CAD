# Agent operations ledger

This is the durable evidence record for execution of the project-management
charter. Add one entry when a milestone starts and complete it before calling
that milestone complete. Link to pull requests, commits, task handoffs, and
evidence rather than duplicating their contents.

## Active entries

| Milestone | Scope / owner | Worktree and handoffs | Required reviews | SME evidence | Automated evidence | Manual FreeCAD evidence | Status |
|---|---|---|---|---|---|---|---|
| Manual FreeCAD allocation-to-path acceptance | Tony CAD; FreeCAD Guy executes; QA Guy observes; Controls Engineer Guy releases | Current checkout; create a dedicated acceptance handoff before execution | QA + Controls Engineer required; FreeCAD review required | Not applicable unless scope changes into motor/protection, vendor assets, or standards adapters | 246 passing tests at `b7c7431` (local audit run); rerun at candidate commit | Unrun — see `MANUAL_FREECAD_ACCEPTANCE_HANDOFF.md` | Blocked pending desktop evidence and independent dual decision |

## Entry template

| Field | Record |
|---|---|
| Milestone and bounded outcome | |
| Tony CAD owner | |
| Roles assigned and why | |
| Worktree path / base commit | |
| Handoff links and integration commit | |
| Affected charter layers and public contracts | |
| QA Guy decision and evidence | |
| Controls Engineer Guy decision and evidence | |
| FreeCAD Guy decision and evidence, if applicable | |
| Layer 0 consultation: role, source/version/date/page, conclusion | |
| Motor/protection dual consultation, if applicable | |
| Automated commands and exact results | |
| Manual acceptance: performed / unrun, evidence link | |
| Documentation synchronized | |
| Known limitations / follow-up owner | |
| Final disposition | |

## Operating rules

1. One task may be assigned to one implementation owner; reviewers remain
   independent of that implementation work.
2. Use separate Git worktrees only for separable surfaces. Record their base
   commit and integration handoff so concurrent work is reconstructible.
3. A missing consultation or unrun manual acceptance is evidence of an open
   gate, not permission to infer it passed.
4. Do not place vendor credentials, proprietary standards text, or protected
   vendor assets in this ledger. Record authorized locators and access limits.
