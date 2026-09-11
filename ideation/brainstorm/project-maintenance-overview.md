# Project Maintenance Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Design a bounded workstation project overview and repository-scoped batch worktree cleanup while preserving existing ownership and retirement guarantees.
Topics: project-maintenance, project-command, overview-discovery, batch-cleanup
Repository context: opensoft/openRepoProject; coordination over openRepoShape, openRepoTools, and workBenches.
Captured: 2026-09-11

## Possible feats

- A coherent inspection-to-maintenance experience combining a local project overview with a repository-scoped batch of the existing safe worktree-removal action.

## Status and motivation

The user requested design only for the two suggested features and deferred
OpenSpec proposals until later. This packet is non-normative brainstorm material.
It creates no proposal, specification change, implementation tasks, code,
installation, or cleanup operation.

The recovered session `01a08d8e-be7b-7900-baa1-5dc5b035e24f` developed project
inspection and cleanup, then clarified remote merge reporting. Its recurring
problem was understanding which work remained and why it could not yet be
retired. A multi-project overview addresses discovery; batch worktree cleanup
reduces repeated selections after retirement is already proven safe.

## Goals and intended capabilities

| Candidate | Proposed experience | First-version boundary |
| --- | --- | --- |
| `project overview` / `project attention` | List local projects and highlight health findings, work to preserve, and cleanup opportunities | Bounded local discovery, Git state, linked-worktree grouping, human and JSON reports |
| `project clean --all-safe` | Preview and explicitly remove every eligible linked worktree in one resolved repository | Uses the current explicit worktree-removal contract; local branch deletion stays a separate explicit action |

The intended outcomes are fewer one-repository-at-a-time inspection commands,
clearer next steps, and fewer repeated cleanup selections. Success includes
accurate partial-result reporting and preserving every excluded worktree.

## First-version scope

The overview MVP covers configured local roots, project identity markers,
local Git state, linked-worktree grouping, bounded partial results, and a
shared human/JSON result model. The cleanup MVP covers one resolved Git
repository, a read-only eligibility plan, explicit confirmation, fresh
revalidation, and non-force removal of eligible linked worktrees.

Family/member relationships, working siblings, mounted spec/code legs,
parked-work records, bench and container status, GitHub merge queries, and
cache disposal remain documented extension points. They are not hidden v1
requirements. Each extension must preserve the ownership boundary of the
tool that already owns that data or operation.

## Non-goals

No estate-wide destructive batch, automatic merge or reconciliation, new
squash-merge deletion policy, implicit local branch deletion, cache deletion in
the first batch version, shape adoption, new bench generator, or replacement
for park/resume. The previously noted exact bench/type doctor check is a
separate correctness follow-up; it is not a third feature in this packet.

## System fit and evidence

The current remote baseline is `origin/main` at `a040790`. Its cleanup contract
has separate explicit `remove` and `delete-branch` actions; a worktree removal
does not delete its local branch. The later cleanup branch contains these
unmerged behavior changes: `5fc2b51` adds branch retirement, `1789ad9` adds
disposable-cache handling, and `bb91a49` hardens cache deletion. Those commits
are evidence for possible future extensions only. `12db36a` records review
closure and is not an implementation baseline.

The designs in this packet target the current `origin/main` contract. A future
proposal may choose to make paired retirement or cache disposal prerequisites,
but it must name that dependency and reconcile the governing cleanup spec and
CLI before proposing behavior. No document here silently assumes an unmerged
change.

Useful baseline functions are `discover`, `repo_state`, `snapshot`,
`cleanup_report`, `clean`, and the repository-health renderer in the `project`
executable. Existing owners continue to own shape mechanics, workflow
transport, and bench generation/setup. No layout or family membership changes
authority.

The main local checkout still contains the earlier repository setup, so these
notes describe the inspected feature history and current remote contract rather
than claiming that extension behavior exists in this checkout.

## Design map

- [Project overview and attention](project-maintenance-project-discovery.md): MVP scope, bounded discovery, grouping, JSON, deferred integrations, and validation scenarios.
- [Batch cleanup](project-maintenance-batch-cleanup.md): current-contract selection, confirmation, revalidation, partial failure, and explicit branch/cache extension boundaries.
- [Inspect and retire synthesis](project-maintenance-synthesis-inspect-and-retire.md): shared evidence, narrowed scope, and the handoff from reporting to explicit action.

The synthesis relates the two feature documents; this overview is their entry
point. Every proposed command and output is illustrative until separately
governed and implemented.

## Key decisions to revisit before proposal

Recommended defaults are bounded local discovery, attention as a filter, one
repository batch scope, worktree-only cleanup against the current contract,
and stopping at the first apply failure. These are design recommendations,
not recorded user approvals of every detail.

Before proposal, confirm command naming, hard limits, the default attention
categories, the merge-target resolution wording, and whether branch retirement
or cache disposal should be proposed as separate changes. Keep squash-merged
branches excluded under the local-ancestry contract unless a separately
reviewed preservation/equivalence rule is adopted.

Later OpenSpec proposals can use these documents as input. Implementation work
and executable task lists remain deferred to that later workflow.
