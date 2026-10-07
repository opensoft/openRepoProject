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

The packet was revised on 2026-10-07 against the findings of the 2026-09-11
[design-fix handoff](next-session-project-maintenance-fix-handoff.md), which
remains in the packet as the review trail.

## Goals and intended capabilities

| Candidate | Proposed experience | First-version boundary |
| --- | --- | --- |
| `project overview` and its `--attention` filter | List local projects and highlight work to repair, preserve, or tidy, with one next command per project | Configured roots and their immediate entries; caps of 32 roots, 4,096 entries per root, 128 candidates, and 512 worktree rows; one 60 s deadline with 5 s per Git child and at most four children at once across distinct repositories; human output and a `schema_version: 1` JSON envelope; an argv clean suggestion naming the canonical repository root, in its `--all-safe` form only for a worktree that passes the batch's gates in a repository with no `inspection-error` row |
| `project clean <root> --all-safe` | Preview and explicitly remove every eligible linked worktree in one resolved repository | Worktree removal only; caps of 128 worktree rows (the main worktree included) and 24 targets; one 60 s deadline with a 10 s reconciliation reserve, 5 s per probe, and serial probing; a fresh confirmed plan carrying `plan_digest`; one seam shared with the single-target `remove` action, which becomes a strict one-item batch; local branch deletion stays a separate explicit action |

The intended outcomes are fewer one-repository-at-a-time inspection commands,
clearer next steps, and fewer repeated cleanup selections. Success includes
accurate partial-result reporting and preserving every excluded worktree.

## First-version scope

The overview MVP lists configured local roots and their immediate entries
only, finds candidates by marker files without calling `discover`, and
reports local Git state, linked worktrees grouped by repository identity
`{root, common_dir, dev, ino}`, attention findings, and partial results in one
human and JSON result model. A `family.yaml` holder is one row with
`relationships: []`; no member is traversed. Its caps are 32 roots, 4,096
entries per root, 128 candidate project directories (sorted before
truncation), and 512 worktree rows estate-wide (`limits.worktree_rows`), main
worktrees included. One monotonic 60 s invocation deadline bounds the run,
and each Git child gets at most 5 s. At most four read-only Git children run
at once, across distinct repositories and never two once their `common_dir`
is known to be the same (`probe_concurrency: 4`). The caps are the largest
whose worst case fits 55 s at 150 ms per Git child with that concurrency,
leaving 5 s of the deadline for filesystem listing and rendering. It never
mutates, and it exits 0, 1, 2, or 130.

The cleanup MVP covers one resolved Git repository and removes only eligible
linked worktrees, with a non-force `git worktree remove` run from the
canonical repository root (`common_dir` for a bare repository) under
`-c status.showUntrackedFiles=normal`, so Git's own cleanliness check sees
untracked files whatever the user's configuration. Beyond the baseline
`merged-removable` classification, a target must pass the main-worktree,
path-byte, registration, lock, and hidden-local-state gates; the last is a
bounded `git ls-files -v -z` probe that excludes a worktree whose index flags
any entry assume-unchanged or skip-worktree. `--apply` always recomputes,
prints, and confirms its own plan. The plan carries `plan_digest`, and an
optional `--expect-plan <plan_digest>` binds a scripted apply to an earlier
preview. Single-target `remove` is strictly a one-item batch: it builds the
same full plan (`mode: "single"`) and calls the same revalidate, spawn, reap,
and reconcile seam, `retire_worktree`. Its caps are 128 worktree rows (every
registry entry, the main worktree included) and 24 targets, the largest whose
serial worst case fits the 50 s work deadline at 150 ms per Git child. One
monotonic 60 s invocation deadline holds back a 10 s reconciliation reserve,
so the work deadline is 50 s, and each probe gets at most 5 s; probing is
serial (`probe_concurrency: 1`). Concurrent writers are outside its safe
contract: it refuses any target whose identity or state changed at
revalidation and otherwise relies on Git's own non-force refusals. It exits
0, 1, 2, 130, or the Git child's own status for a failed removal.

The handoff between them is Git-first. An overview row's `suggested_command`
is `null` unless a finding supplies one. When present it is a JSON argument
vector naming the absolute canonical `repository.root`, such as
`["project", "clean", "/home/user/projects/Atlas", "--all-safe"]` or the same
vector without `--all-safe`; it never names a bare project and never includes
`--apply` or `--yes`. The `--all-safe` form comes only from a
`merged-removable` worktree that also passes the batch's gates in the batch's
order; otherwise the first failing gate's finding (`main-worktree`,
`unsupported-path-bytes`, `registration-mismatch`, or `locked-worktree`)
replaces the housekeeping finding. A fifth gate covers the whole repository:
while any of its worktree rows is `inspection-error` (an unreadable path, a
registration-mismatched row, or a failed status probe), the batch plan would
be refused as `inspection-incomplete`, so the overview withholds every
`--all-safe` suggestion for it, and its housekeeping findings and the row
suggest only the read-only `project clean <root>`. Every `project clean` mode
(the read-only report, `--json`, `--all-safe`, and
`--apply --action push|remove|delete-branch`) resolves an absolute path
Git-first: it must be exactly a main worktree root, or it is refused with
`target-not-repository-root` and exit 2, and no other directory is
substituted. A relative path or no argument resolves to the repository Git
finds there. Only a bare project name keeps the baseline `discover` lookup,
whose one Git child becomes counted and deadline-bounded.

Both features read one shared evidence model and require Git 2.36 or newer
for `git worktree list --porcelain -z`, refusing older Git with `git-too-old`
and a missing or unusable `git` with `git-unavailable`. One `git --version`
child runs per invocation. Each repository then costs the same four
repository-wide children, memoized per `common_dir` and fanned out to every
row: identity
(`rev-parse --path-format=absolute --show-toplevel --git-common-dir`), the
registry listing (`worktree list --porcelain -z`), the ref listing (one
`for-each-ref` over `refs/heads` and `refs/remotes` in one shared
NUL-separated format), and the merged set
(`for-each-ref --merged=<merge-target sha>`); merge-target resolution spawns
no child. Each present, registration-verified worktree row, the main one
included, gets exactly one combined bounded probe,
`git status --porcelain=v1 -z --untracked-files=normal --ignored=matching`,
which stops reading at a 65th ignored record or a 4,097th record of any kind.

Family/member relationships, working siblings, mounted spec/code legs,
parked-work records, bench and container status, GitHub merge queries, and
cache disposal remain documented extension points. They are not hidden v1
requirements. Each extension must preserve the ownership boundary of the
tool that already owns that data or operation.

## Non-goals

No estate-wide destructive batch, automatic merge or branch reconciliation,
new squash-merge deletion policy, implicit local branch deletion, cache
deletion in the first batch version, shape adoption, new bench generator, or
replacement for park/resume. There is also no lock, lease, or
writer-quiescence protocol, and no persistent cache; the batch's
reconciliation record is a read-only rescan, not a repair. The previously
noted exact bench/type doctor check is a separate correctness follow-up; it
is not a third feature in this packet.

## System fit and evidence

The design contract baseline is `a040790`, the commit both feature documents
measure against; the `project` executable and its tests are unchanged since.
`origin/main` has since advanced to `67efa80` (PR #4), which archives the
three completed OpenSpec changes and promotes their specifications into
`openspec/specs/`, including the governing cleanup specifications
`openspec/specs/project-clean/spec.md` and
`openspec/specs/project-clean-review-safety/spec.md`. The cleanup contract is
therefore still the one at `a040790`. That contract has separate explicit
`remove` and `delete-branch` actions; a worktree removal does not delete its
local branch.

The `cleanup` branch is PR #2, open and unmerged. Its behavior changes
include `5fc2b51` (branch retirement), `acf0133` (doctor repository health),
`1789ad9` (disposable-cache handling), `09af8c8` (remote merge status), and
`bb91a49` (cache deletion hardening). Those commits are evidence for possible
future extensions only. `12db36a` records review closure and is not an
implementation baseline.

The designs in this packet target the `a040790` contract. A future proposal
may choose to make paired retirement or cache disposal prerequisites, but it
must name that dependency and reconcile the governing cleanup spec and CLI
before proposing behavior. No document here silently assumes an unmerged
change.

Both feature documents carry a "Baseline behavior changes" section listing
the changes to `a040790` that a proposal must carry into the governing
cleanup specifications. Both list the shared items; batch cleanup adds the
batch-only items, which concern `clean` resolution, removal, and the batch
plan. Deduplicated, the shared items are:

- Git-first resolution: in every `project clean` mode, `push` and
  `delete-branch` included, an absolute path must be exactly a main worktree
  root or is refused with `target-not-repository-root`; today `discover`
  redirects `/outer/leg` to `/outer` when `/outer/project.yaml` exists, and
  `/Atlas` to `/Atlas/Atlas` when `/Atlas/Atlas/family.yaml` exists. No path
  goes through `discover`: the overview never passes its candidates to it,
  and `project clean` keeps its lookup only for a bare name, whose one Git
  child becomes counted and deadline-bounded.
- Shared probes: `repo_state` and `cleanup_report` move onto the four
  repository-wide children and the one combined status probe, so overview,
  doctor, and clean read one evidence model. A deleted upstream reports
  `remote-gone` instead of `unpublished` in all three, and both are preserve
  states. The explicit `--untracked-files=normal` keeps a user's
  `status.showUntrackedFiles=no` from turning every clean, present,
  non-default worktree into `inspection-error`. A registration-mismatched
  worktree is no longer status-probed and is `inspection-error`. An
  unreadable worktree path becomes one `inspection-error` row with
  `present: null` and an `os-error`, where at `a040790` `main()` catches the
  `OSError` and refuses the whole repository with exit 2. Each worktree row
  costs one status probe instead of two.
- NUL-delimited parsing: a worktree path with a newline is no longer misread
  as a truncated path and classified `stale-worktree`, and a non-UTF-8 path
  no longer stops the run with an uncaught `UnicodeDecodeError`.
- `ignored_files` keeps its name and type but means ignored records observed,
  at least: a lower bound when the new `ignored_files_truncated` is true, and
  `null` when the probe stopped before any ignored record.
- The manifest's `tracking_branch` is read at `repository.root`, not at
  whichever directory `discover` returned.
- Timeouts: each Git child gets `min(5 s, remaining)` under one 60 s
  monotonic invocation deadline and runs in its own process group, where the
  baseline `probe()` helper gives a fixed 15 s with no invocation deadline.
- Git 2.36 or newer: `project clean` refuses older Git with `git-too-old`
  and a missing or unusable `git` with `git-unavailable`, and
  `project doctor`, which reads `repo_state`, requires it as well.

The batch-only items are:

- A relative path or no argument resolves to the repository Git finds there,
  with `root` set to its main worktree, instead of going through `discover`;
  the report's `root` always names the command directory; and a bare
  repository's first registry record is no longer an `inspection-error`
  checkout.
- The removal command, single-target and batch alike, gains
  `-c status.showUntrackedFiles=normal`, so Git's own check sees untracked
  files whatever the user's configuration.
- A worktree whose index flags an entry assume-unchanged or skip-worktree is
  never removed (`hidden-local-state`, found by the bounded
  `git ls-files -v -z` probe), so sparse checkouts are excluded.
- Single-target `remove` runs through `retire_worktree` as a strict one-item
  batch, gaining the identity checks, the gates, full-repository inspection
  (an inspection error anywhere refuses it with `inspection-incomplete`), the
  refusal codes `worktree-not-found` and `target-excluded`, the `unknown`
  outcome with exit 1, and its own process group for the removal child.

The designs build on baseline helpers by name: `projects_dirs`, `manifest`,
`repo_state`, `default_branch`, the classification ladder in
`cleanup_report`, and `clean`. The overview mirrors `discover`'s marker and
family-holder rules without calling it. Batch revalidation re-checks one
target with at most five Git children (the identity probe, the registry
listing, a narrowed ref listing, the combined status probe, and the
hidden-state probe) and a manifest re-read, instead of recomputing the whole
report as `require_unchanged_cleanup_state` does. Doctor's existing checks in
`check_rows` keep their meanings, and the overview never calls `snapshot`,
which follows family members and project legs. Existing owners continue to
own shape mechanics, workflow transport, and bench generation/setup. No
layout or family membership changes authority.

The main local checkout still contains the earlier repository setup, so these
notes describe the inspected feature history and current remote contract rather
than claiming that extension behavior exists in this checkout.

## Design map

- [Project overview and attention](project-maintenance-project-discovery.md): bounded discovery and its cap arithmetic, the probe model with four-way cross-repository concurrency, the collector boundary, attention categories and the gates before an `--all-safe` suggestion, the `schema_version: 1` JSON contract and fixture, the Git-first clean handoff, result semantics, baseline behavior changes, and validation scenarios.
- [Batch cleanup](project-maintenance-batch-cleanup.md): eligibility gates including the hidden-local-state probe, the safety boundary and branch race, the execution model (plan digest, one mutation seam, deadlines, stages, exit codes), probe accounting and cap arithmetic, the plan and apply-result JSON, baseline behavior changes, and validation scenarios.
- [Inspect and retire synthesis](project-maintenance-synthesis-inspect-and-retire.md): the shared vocabulary and evidence model, the distinct failure policies, the one mutation seam, the overview gates, and the Git-first handoff from reporting to explicit action.

The synthesis relates the two feature documents; this overview is their entry
point. Every proposed command and output is illustrative until separately
governed and implemented.

## Key decisions to revisit before proposal

Recommended defaults are bounded local discovery, attention as a display
filter, one repository batch scope, worktree-only cleanup against the current
contract, a narrow safety guarantee instead of a writer-quiescence protocol,
and stopping the batch at the first target that is not plainly removed. These
are design recommendations, not recorded user approvals of every detail.

The open proposal decisions, consolidated from both feature documents'
"Alternatives and open decisions" sections:

- Measured costs. Both documents derive their caps at 150 ms per Git child,
  a 1.5× margin over an assumed 100 ms per warm child (and about 0.3 s per
  removal) that the proposal must measure. If measurement disagrees, batch
  cleanup reapplies its rule and lowers the target cap first.
- Caps versus concurrency. The overview's caps fit only with four children
  at once across repositories: the break-even is about 214 ms per child with
  four and about 54 ms serially. If the proposal rejects concurrency, the
  fallback is 32 candidates and 128 worktree rows, which fit serially
  (1 + 32 × 4 + 128 = 257 children, about 38.6 s at 150 ms). If warm
  children average more than about 214 ms even with concurrency, the caps
  must fall or very large estates end incomplete.
- A per-repository row cap. One repository's children always run serially,
  so a single repository with more than about 360 worktree rows cannot
  complete within the overview's deadline at 150 ms per child; accept that or
  cap rows per repository.
- Whether any limit is user-configurable.
- Whether `--apply --json` prints the apply result record for single-target
  and batch removal (recommended), or the MVP stays human-only and keeps the
  baseline refusal of `--json` with `--apply`.
- Whether `--expect-plan` is required whenever `--yes` is used, or stays
  optional as in the MVP.
- Whether a relative path or the no-argument default must be an exact
  repository root, as an absolute path must, instead of resolving to the
  repository Git finds there.
- Whether a skip-worktree entry whose file is absent from disk, as in a
  sparse checkout, may be treated as safe instead of `hidden-local-state`.
- Whether bare repositories are supported (`root: null`, with `common_dir` as
  the command directory) or refused.
- Whether SIGTERM and SIGHUP receive the SIGINT treatment, exiting 143 and
  129.
- Whether the `attention` alias merits a separate command, and whether
  `--attention --json` keeps printing the full envelope or filters `projects`
  behind an explicit envelope field.
- Whether suggested commands stay argv arrays or also carry a display string.
- Whether the extra `dirty` finding for a dirty default-branch checkout is
  wanted.
- The final command and flag spelling.
- Whether cache disposal and paired branch retirement, and later the remote,
  family, bench, container, and park integrations, deserve separate changes.
  Exact bench/type validation remains existing-doctor follow-up work.

Rejected or deferred alternatives stay closed unless a proposal reopens them:
an arbitrary-depth recursive scan, continuing a batch after a failure, a
persistent resumable plan, and a writer-quiescence or ownership handoff, which
a later design may add on top of the same seam. Keep squash-merged branches
excluded under the local-ancestry contract unless a separately reviewed
preservation/equivalence rule is adopted.

Later OpenSpec proposals can use these documents as input. Implementation work
and executable task lists remain deferred to that later workflow.
