# Project Maintenance Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Design a workstation project overview and repository-scoped batch cleanup while preserving existing ownership and retirement guarantees.
Topics: project-maintenance, project-command, overview-discovery, batch-cleanup
Repository context: opensoft/openRepoProject; coordination over openRepoShape, openRepoTools, and workBenches.
Captured: 2026-09-11

## Possible feats

- A coherent inspection-to-maintenance experience combining the two candidate features described in this packet.

## Status and motivation

The user requested design only for the two suggested features and deferred
OpenSpec proposals until later. This packet is non-normative brainstorm material.
It creates no proposal, specification change, implementation tasks, code,
installation, or cleanup operation.

The recovered session `01a08d8e-be7b-7900-baa1-5dc5b035e24f` developed project
inspection and cleanup, then clarified remote merge reporting. Its recurring
problem was understanding which work remained and why it could not yet be
retired. A multi-project overview addresses discovery; batch cleanup reduces
repetition after retirement is already proven safe.

## Goals and intended capabilities

| Candidate | Proposed experience | Boundary |
| --- | --- | --- |
| `project overview` / `project attention` | List local projects and highlight health findings, work to preserve, and cleanup opportunities | Read-only; bounded discovery; optional explicit remote inspection |
| `project clean --all-safe` | Preview and explicitly retire eligible worktrees and paired local branches in one repository | Fresh local proof, one fixed confirmed plan, stop on failure |

The intended outcomes are fewer one-repository-at-a-time inspection commands,
clearer next steps, and fewer repeated cleanup selections. Success includes
accurate partial-result reporting and preserving every excluded worktree.

## Non-goals

No estate-wide destructive batch, automatic merge or reconciliation, new
squash-merge deletion policy, shape adoption, new bench generator, or replacement
for park/resume. The previously noted exact bench/type doctor check is a
separate correctness follow-up; it is not a third feature in this packet.

## System fit and evidence

The first CLI was inspected at `562fdc7`; later cleanup behavior was inspected
at `12db36a`. The design deliberately includes that newer cleanup baseline,
which retires a worktree and its local branch together. The earlier suggestion
of separate opt-in branch deletion described the older behavior. These source
commits are evidence anchors, not a claim that the remote branch has stopped
changing; the future proposal should reconcile against its then-current head.

Useful baseline functions are `discover`, `repo_state`, `snapshot`,
`cleanup_report`, `clean`, and the repository-health renderer in the `project`
executable. Existing owners continue to own shape mechanics, workflow transport,
and bench generation/setup. No layout or family membership changes authority.

The main local checkout still contains the earlier repository setup, so these
notes describe the inspected feature history rather than claiming every
described baseline capability exists in this checkout's current working tree.

## Design map

- [Project overview and attention](project-maintenance-project-discovery.md): discovery, grouping, display, JSON, freshness, failure handling, and validation scenarios.
- [Batch cleanup](project-maintenance-batch-cleanup.md): selection, eligibility, confirmation, revalidation, partial failure, and recovery.
- [Inspect and retire synthesis](project-maintenance-synthesis-inspect-and-retire.md): shared evidence, narrowed scope, and the handoff from reporting to explicit action.

The synthesis relates the two feature documents; this overview is their entry
point. Every proposed command and output is illustrative until separately
governed and implemented.

## Key decisions to revisit before proposal

Recommended defaults are bounded local discovery, attention as a filter/alias,
one-repository batch scope, paired branch retirement matching newer cleanup,
and stopping at the first apply failure. These are design recommendations,
not recorded user approvals of every detail.

Confirm naming and default attention categories; choose a large-estate display
after prototyping. Keep squash-merged branches excluded under the current
local-ancestry contract: updating main alone does not necessarily make their
original tips ancestors. Any broader retirement proof deserves its own design.

Later OpenSpec proposals can use these documents as input. Implementation work
and executable task lists remain deferred to that later workflow.
