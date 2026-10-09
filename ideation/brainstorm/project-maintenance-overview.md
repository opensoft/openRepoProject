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
OpenSpec proposals until later. This packet is non-normative brainstorm
material. It creates no proposal, specification change, implementation tasks,
code, installation, or cleanup operation.

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
| `project overview` and its `--attention` filter | List local projects and highlight work to repair, preserve, or tidy, with one next command per project | Configured roots and their immediate entries; caps of 32 roots, 4,096 entries per root, 128 candidates, and 512 worktree rows; one 60 s deadline with 5 s per Git child and at most four children at once across distinct repositories; human output and a `schema_version: 1` JSON envelope; an argv clean suggestion naming the canonical repository root, in its `--all-safe` form only for a worktree that passes the batch's gates in a repository with no `inspection-error` or unprobed row and no more than 128 worktree rows |
| `project clean <root> --all-safe` | Preview and explicitly remove every eligible linked worktree in one resolved repository | Worktree removal only; caps of 128 worktree rows (the main worktree included) and 16 targets per run, a larger backlog deferred as `deferred-target-cap`; one 60 s deadline with a 10 s reconciliation reserve, a 5 s removal floor, 5 s per probe, and serial probing; a fresh confirmed plan carrying `plan_digest`; one seam shared with the single-target `remove` action, whose completeness is the repository-wide evidence plus its own row; local branch deletion stays a separate explicit action |

The intended outcomes are fewer one-repository-at-a-time inspection commands,
clearer next steps, and fewer repeated cleanup selections. Success includes
accurate partial-result reporting and preserving every excluded worktree.

## First-version scope

The overview MVP lists configured local roots and their immediate entries only,
finds candidates by marker files without calling `discover`, and reports local
Git state, linked worktrees grouped by repository identity
`{root, common_dir, dev, ino}`, attention findings, and partial results in one
human and JSON result model. A `family.yaml` holder is one row with
`relationships: []`; no member is traversed. Its caps are 32 roots, 4,096
entries per root, 128 candidate project directories (sorted before truncation),
and 512 worktree rows estate-wide (`limits.worktree_rows`), main worktrees
included. One monotonic 60 s invocation deadline bounds the run, and each Git
child gets at most 5 s. At most four read-only Git children run at once, across
distinct repositories and never two once their `common_dir` is known to be the
same (`probe_concurrency: 4`). Listing runs as one worker task per root, each
bounded at 5 s; a root still unfinished then is `truncated`. The caps are the
largest whose worst case fits the deadline at 150 ms per Git child with that
concurrency, after a listing phase estimated at about 6 s, which leaves about
54 s for Git work. It never mutates, and it exits 0, 1, 2, 130, 143, or 129.

The cleanup MVP covers one resolved Git repository and removes only eligible
linked worktrees, with a non-force `git worktree remove` run from the canonical
repository root (a bare repository is refused) under
`-c status.showUntrackedFiles=normal`, `-c core.untrackedCache=false`, and
`-c core.fsmonitor=false`, so Git's own cleanliness check sees untracked files
whatever the user's configuration. Beyond the baseline `merged-removable`
classification, a target must pass the main-worktree, path-byte, registration,
lock, unstarted-branch, submodule, and hidden-local-state gates. The last two
read the worktree's own index through one bounded
`git -C <worktree path> ls-files -v --stage -z` probe, plus an `lstat` of its
admin `modules` directory: any gitlink or `modules` entry excludes it as
`contains-submodule`, and an entry flagged assume-unchanged or skip-worktree as
`hidden-local-state`. `--apply` always recomputes, prints, and confirms its own
plan. The plan carries `plan_digest`, and an optional
`--expect-plan <plan_digest>` binds a scripted apply to an earlier preview.
Single-target `remove` builds the same full plan (`mode: "single"`) and calls
the same revalidate, spawn, reap, and reconcile seam, `retire_worktree`, but its
completeness is the repository-wide evidence plus its own row, so other rows'
omissions never block it. Its caps are 128 worktree rows (every registry entry,
the main worktree included) and 16 targets, derived at 150 ms per Git child with
one fit test: a cap pair fits when its worst case completes within the 50 s work
deadline and spawns its last removal with at least `removal_floor_seconds` (5 s)
left. The row cap is the largest power of two for which at least 16 targets fit,
and the target cap the largest multiple of 8 that fits with it: 128 rows and 16
targets, with a worst case of about 39.9 s and the 16th removal spawned at 39.15
s. 256 rows admit fewer than 16 targets under the test and are rejected, and 24
targets would fit the deadline alone, but the 21st removal would start inside
the floor. One monotonic 60 s invocation deadline holds back a 10 s
reconciliation reserve, so the work deadline is 50 s, and each probe gets at
most 5 s; probing is serial (`probe_concurrency: 1`). No removal is spawned with
less than 5 s of the work deadline left: that target and every later one are
`not-attempted` with `deadline-exceeded`, and the run exits 1. Once spawned, a
removal child is never signaled; only a 300 s hard ceiling ends it. A child that
exits nonzero on its own stays `failed`, even after a signal; after a ceiling
kill, or an exit that could not be observed, the rescan decides the target's
stage: `removed` when the registry entry and the path are both gone, and
`unknown` with a `partially-removed` note when either remains, reason
`removal-ceiling` naming a ceiling kill, with which a `removed` target exits 1
(lane openRepoProject-2 ruling M1, confirmed 2026-10-09; change 1 phase 6
(`90854a3`)). With more than 16 eligible rows the plan selects the first 16 in
canonical order and defers the rest as `deferred-target-cap`, and re-running
drains the backlog 16 at a time. Plain read-only `clean` runs as
`mode: "report"` under the same deadline with its own 256-row cap, above which
the report is incomplete. Concurrent writers are outside its safe contract: it
refuses any target whose identity or state changed at revalidation and otherwise
relies on Git's own non-force refusals. It exits 0, 1, 2, 130, 143, 129, or the
Git child's own status for a failed removal.

The handoff between them is Git-first. An overview row's `suggested_command` is
`null` unless a finding supplies one. When present it is a JSON argument vector
naming the absolute canonical `repository.root`, such as
`["project", "clean", "/home/user/projects/Atlas", "--all-safe"]` or the same
vector without `--all-safe`; it never names a bare project and never includes
`--apply` or `--yes`. The `--all-safe` form comes only from a `merged-removable`
worktree that also passes the batch's gates in the batch's order; otherwise the
first failing gate's finding (`main-worktree`, `unsupported-path-bytes`,
`registration-mismatch`, or `locked-worktree`) replaces the housekeeping
finding. A fifth gate covers the whole repository: while any of its worktree
rows is `inspection-error` (an unreadable path, a registration-mismatched row,
or a failed status probe), or it has more than 128 worktree rows, the batch plan
would be refused as `inspection-incomplete` or `inspect-cap`, and while any of
its rows went unprobed because the 512-row cap or the deadline cut it, the plan
is not known to be complete; so the overview withholds every `--all-safe`
suggestion for it, and its housekeeping findings and the row suggest only the
read-only `project clean <root>`, and those housekeeping findings carry a
`suggestion_gate` code naming the gate. The gate changes suggestions only, not
the overview's completeness. `target-cap` only limits: with more than 16
gate-passing rows the `--all-safe` suggestion stays, its findings carrying
`suggestion_gate: "target-cap"`. An unstarted worktree keeps its housekeeping
finding with only the read-only suggestion and
`suggestion_gate: "unstarted-branch"` (rulings N-5 and P6-5), and a merged
worktree whose reflog is missing, empty, read to its 64 KiB bound, or
undecidable keeps it with only the read-only suggestion and
`suggestion_gate: "reflog-unavailable"`, the overview reading the branch's
reflog as the batch does, with no Git child (the D10 amendment and lane
openRepoProject-2 ruling R-12, 2026-10-09, change 1 at `0b3c33d` and `4f2162b`;
change 2, read at `996a181`, and at `4495ae7` (R-20; unchanged at `cc43860`)).
The batch may still exclude a suggested worktree as `hidden-local-state` or
`contains-submodule`, which only its own index probe and admin-directory check
see. Every `project clean` mode (the read-only report, `--json`, `--all-safe`,
and `--apply --action push|remove|delete-branch`) resolves an absolute path
Git-first: it must be exactly a main worktree root, or it is refused with
`target-not-repository-root` and exit 2, and no other directory is substituted.
A relative path or no argument resolves to the repository Git finds there. Only
a bare project name keeps the baseline `discover` lookup, whose one Git child
becomes counted and deadline-bounded.

Both features read one shared evidence model and require Git 2.36 or newer for
`git worktree list --porcelain -z`, refusing older Git with `git-too-old` and a
missing or unusable `git` with `git-unavailable`. One `git --version` child runs
per invocation. Each repository then costs the same four repository-wide
children, memoized per `common_dir` and fanned out to every row: identity
(`rev-parse --path-format=absolute --show-toplevel --git-common-dir`), the
registry listing (`worktree list --porcelain -z`), the ref listing (one
`for-each-ref` over `refs/heads` and `refs/remotes` in one shared NUL-separated
format), and the merged set (`for-each-ref --merged=<merge-target sha>`);
merge-target resolution spawns no child. Each present, registration-verified
worktree row, the main one included, gets exactly one combined bounded probe,
`git status --porcelain=v1 -z --untracked-files=normal --ignored=matching`,
run with `-c core.untrackedCache=false -c core.fsmonitor=false`, which stops
reading at a 65th ignored record or a 4,097th record of any kind.
Worktree-specific probes run as `git -C <worktree path>` against that worktree's
own index, only after its identity is verified; repository-wide probes run as
`git -C <repository.root>` (`common_dir` for a bare repository), except the
identity probe, which runs in the candidate. When a linked worktree is reached
first in canonical candidate order, the registry listing also runs in the
candidate, because the main worktree's path comes from that listing; that
changes which directory the command runs in, never which index a probe reads.
Where `root` is null (a bare repository, a missing main worktree, or a gitfile
checkout whose main worktree cannot be named), the repository-wide probes run in
`common_dir` for a bare repository and otherwise where the identity probe ran;
`clean` refuses those layouts, and the overview reports them (lane
openRepoProject-2 ruling R-13, R-13a in its messages, 2026-10-09; change 1 at
`4f2162b`).

Family/member relationships, working siblings, mounted spec/code legs,
parked-work records, bench and container status, GitHub merge queries, and
cache disposal remain documented extension points. They are not hidden v1
requirements. Each extension must preserve the ownership boundary of the
tool that already owns that data or operation. The batch removes only
worktrees with no ignored files, so caches such as `__pycache__` keep a
worktree out until the cache-disposal change; in one surveyed repository 20
of 29 merged worktrees were excluded for caches alone, the evidence for that
follow-on.

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
measure against. `origin/main` has since advanced to `7a9134b`, which merged
PR #13 (lane openRepoProject-1's archive of the `prefer-triad-in-project-new`
OpenSpec change, `openspec/` only) after `d7f6b0e` merged PR #8 (feature 002,
"offer the Triad first in `project new`") on 2026-10-08. Before them, `da33d92`
merged PR #7 (this packet) on 2026-10-07, PR #4 archived the three completed
OpenSpec changes and promoted their specifications into `openspec/specs/`,
including the governing cleanup specifications
`openspec/specs/project-clean/spec.md` and
`openspec/specs/project-clean-review-safety/spec.md`, and PR #5 (merged
2026-10-07) added the `prefer-triad-in-project-new` OpenSpec proposal. PR #8
added about 141 lines to `project`, in the project-creation code between
`choose()` and the end of `new()`, and 1,163 lines to `tests/test_project.py`;
the cleanup, status, doctor, and update paths are unchanged in content but sit
about 141 lines lower, so every `project` line citation stays pinned at
`a040790`, whose `project` is byte-identical through `da33d92`. The cleanup
contract is therefore still the one at `a040790`. That contract has separate
explicit `remove` and `delete-branch` actions; a worktree removal does not
delete its local branch.

The `cleanup` branch was PR #2, closed unmerged on 2026-10-07 on Brett Heap's
decision ([decision record][pr2-decision]); the branch stays on origin at
`bb91a49` as the harvest source for separately governed extensions. Its behavior
changes include `5fc2b51` (branch retirement), `acf0133` (doctor repository
health), `80fdef3` (health-warning fixes and regressions), `1789ad9`
(disposable-cache handling), `09af8c8` (remote merge status), and `bb91a49`
(cache deletion hardening). Those commits are evidence for
possible future extensions only. Each extension needs its own proposal that
updates the governing cleanup specification first; the decision record names
`acf0133` and `80fdef3` (doctor repository health, local-only read-only
reporting) as the piece for a later revision of this overview design to absorb
rather than defer. That follow-up is discharged by the OpenSpec change
`add-project-overview` (issue #10, PR #12), which absorbs both commits
as local-only read-only reporting, so this design does not absorb them.
`12db36a` records review closure and is not an implementation baseline.

[pr2-decision]: https://github.com/opensoft/openRepoProject/pull/2#issuecomment-6035824335

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
  doctor, and clean read one evidence model. Overview and clean classify a
  deleted upstream `remote-gone` instead of `unpublished`, and both are preserve
  states, except that a merged row is, by Brett Heap's ruling of 2026-10-09
  (applied at `b772195` and `cc43860`), tested for local ancestry first and
  reads `merged-removable`; doctor never classifies a deleted upstream, its only
  worktree classification being `repo_state`'s `stale-worktree`, shown under
  `--json`. The explicit
  `--untracked-files=normal` keeps a user's
  `status.showUntrackedFiles=no` from turning every clean, present, non-default
  worktree into `inspection-error`. A registration-mismatched worktree is no
  longer status-probed and is set to `inspection-error` directly. An unreadable
  worktree path becomes one `inspection-error` row with `present: null` and an
  `os-error`, where at `a040790` `main()` catches the `OSError` and refuses the
  whole repository with exit 2. A failed `git status` in the repository root,
  which at `a040790` makes `repo_state` raise `Refused` and ends `clean`,
  `status`, `doctor`, and `update` with exit 2, becomes an `inspection-error`
  row for the main worktree, and the other rows are still reported. Each
  worktree row costs one status probe instead of two.
- NUL-delimited parsing: a worktree path with a newline is no longer misread
  as a truncated path and classified `stale-worktree`, and a non-UTF-8 path
  no longer stops the run with an uncaught `UnicodeDecodeError`.
- `ignored_files` keeps its name and type but means ignored records observed,
  at least: a lower bound when the new `ignored_files_truncated` is true, and
  `null` when the probe stopped before any ignored record.
- The manifest's `tracking_branch` is read at `repository.root`, not at
  whichever directory `discover` returned.
- A manifest larger than 1 MiB by `st_size` is `manifest-invalid` before it is
  read (lane openRepoProject-2 ruling R-4, 2026-10-09), at the merge-target
  manifest read, where `a040790` reads a manifest of any size: `clean`
  refuses with exit 2, and the overview records a row error (change 2
  council V7; the shared evidence model of change 1 at `0669a20`).
- Timeouts: under the overview's and `clean`'s 60 s monotonic invocation
  deadlines each inspection Git child gets `min(5 s, remaining)` and runs in
  its own process group, where the baseline `probe()` helper gives a fixed
  15 s with no invocation deadline; `status`, `doctor`, and `update` have no
  deadline and keep 15 s per Git child, and `push` and `delete-branch` stay
  unbounded (ruling D-W).
- Git 2.36 or newer. The version check runs only when a Git repository is
  about to be inspected; a directory with no `.git` keeps `present: false`.
  `clean` and `overview` refuse with `git-too-old` or `git-unavailable`,
  exit 2, before any probe; under `--json` they print `{"error", "code"}`.
  `status`, `doctor` and `update` never refuse: `doctor` reports an old or
  unusable Git as an error check row and keeps its exit semantics for error
  rows; `status` marks rows it cannot inspect `inspection-error`;
  `update --apply --component tools|workflow` does not require Git. The
  overview checks once before any root is listed (ruling D-AF). The
  baseline `main()` prints a `Refused` under `--json` as `{"error"}`, with
  no `code`, which these refusals add. The `inspection-error` mark that `status`
  and `doctor` set is `classification: "inspection-error"` with `errors` beside
  it, on the root and leg dicts (change 1 phase 6 (`90854a3`), lane
  openRepoProject-2, 2026-10-09).

The batch-only items are:

- A relative path or no argument resolves to the repository Git finds there,
  with `root` set to its main worktree, instead of going through `discover`;
  the report's `root` always names the command directory; and a bare
  repository is refused in every `clean` mode with
  `target-not-repository-root` and exit 2.
- `push` refuses a `remote-gone` branch with refusal reason `remote-gone` and
  exit 2 (on the deleted upstream itself, whatever the row's class, since Brett
  Heap's ruling of 2026-10-09 applied at `b772195`), and `push` and
  `delete-branch` refuse with `inspection-incomplete`, `inspect-cap`, or
  `deadline-exceeded` when their re-inspection is incomplete, `push` doing so
  before or after confirmation (change 1 phase 6 (`90854a3`)).
- When the first registry record's path equals `common_dir`, a submodule
  checkout, for which `git rev-parse --show-superproject-working-tree`
  prints a path (its first record lies under `.git/modules`), is refused
  with `target-not-repository-root`; otherwise a gitfile main checkout
  resolves through `core.worktree` or, where that is unset, as Git 2.43
  leaves it after `git init --separate-git-dir`, through the candidate
  toplevel whose `.git` file names `common_dir`, and a linked worktree of
  such a repository with `core.worktree` unset is refused the same way; at
  `a040790` `clean` handles all three with exit 0.
- Plain read-only `clean` runs as `mode: "report"` under the deadline with a
  256-row cap; above it the report is incomplete and exits 1, where at
  `a040790` plain `clean` exits 0 whenever it prints.
- `--apply --json` is accepted for `--all-safe` and `--action remove`,
  printing the apply result record, where `a040790` refuses `--json` with
  `--apply`; with `push` or `delete-branch` it stays refused.
- The removal command, single-target and batch alike, gains
  `-c status.showUntrackedFiles=normal`, `-c core.untrackedCache=false`, and
  `-c core.fsmonitor=false`, so Git's own check sees untracked files
  whatever the user's configuration.
- A worktree whose branch has no commit of its own is excluded as
  `unstarted-branch`, and one whose reflog cannot decide as
  `reflog-unavailable`; at `a040790` it classifies `merged-removable`. The gate
  applies to single-target `remove` too, so a fresh merged worktree named with
  `--worktree` is refused with `target-excluded`, where `a040790` removes it.
- A merged worktree whose reflog keeps no decisive entry, as after 90 days
  without activity under the default `gc.reflogExpire`, is refused in
  single-target mode with `target-excluded`, reason `reflog-unavailable`, where
  `a040790` removes it (change 1 at `0b3c33d`, worded so at `4f2162b`, lane
  openRepoProject-2, 2026-10-09).
- Not a change to `a040790`, which has no target cap, but change 1 council
  V5's departure from this packet's `target-cap` refusal, listed here for
  the proposal: more than 16 eligible rows no longer block apply; the first
  16 are selected and the rest deferred as `deferred-target-cap`.
- A worktree whose index flags an entry assume-unchanged or skip-worktree is
  never removed (`hidden-local-state`, found by the bounded
  `git -C <worktree path> ls-files -v --stage -z` probe), so sparse checkouts
  are excluded.
- A worktree whose index holds a gitlink, or whose admin directory holds
  `modules`, is excluded as `contains-submodule`; at `a040790` it can be
  classified `merged-removable` and offered for removal, which Git then
  refuses with exit 128 whenever the submodule is populated or `modules`
  exists.
- Single-target `remove` runs through `retire_worktree` on the batch's seam,
  gaining the identity checks, the gates (the unstarted-branch, submodule,
  and hidden-state gates included), a completeness of the repository-wide
  evidence plus its own row (other rows' inspection errors and omissions
  recorded as non-blocking), the refusal codes `worktree-not-found` and
  `target-excluded`, each naming a manual remedy, the `unknown` outcome
  (exit 1), the removal floor, and its own process group for the removal
  child.

The designs build on baseline helpers by name: `projects_dirs`, `manifest`,
`repo_state`, `default_branch`, the classification ladder in `cleanup_report`,
and `clean`. The overview mirrors `discover`'s marker and family-holder rules
without calling it. Batch revalidation re-checks one target with at most five
Git children (the identity probe, the registry listing, a narrowed ref listing,
and, inside the target worktree, the combined status probe and the hidden-state
probe) plus a manifest re-read and the target's `modules` check, instead of
recomputing the whole report as `require_unchanged_cleanup_state` does. Doctor's
existing checks in `check_rows` keep their meanings, and the overview never
calls `snapshot`, which follows family members and project legs. Existing owners
continue to own shape mechanics, workflow transport, and bench generation/setup.
No layout or family membership changes authority.

The main local checkout still contains the earlier repository setup, so these
notes describe the inspected feature history and current remote contract rather
than claiming that extension behavior exists in this checkout.

## Design map

- [Project overview and attention](project-maintenance-project-discovery.md):
  bounded discovery and its cap arithmetic, the probe model with four-way
  cross-repository concurrency, the collector boundary, attention categories and
  the gates before an `--all-safe` suggestion, the `schema_version: 1` JSON
  contract and fixture, the Git-first clean handoff, result semantics, baseline
  behavior changes, and validation scenarios.
- [Batch cleanup](project-maintenance-batch-cleanup.md): eligibility gates
  including the submodule and hidden-local-state index gates, the safety
  boundary and branch race, the execution model (plan digest, one mutation seam,
  deadlines and the removal floor, stages, exit codes), the probe directory
  rule, probe accounting and cap arithmetic, the plan and apply-result JSON,
  baseline behavior changes, and validation scenarios.
- [Inspect and retire
  synthesis](project-maintenance-synthesis-inspect-and-retire.md): the shared
  vocabulary and evidence model, the distinct failure policies, the one mutation
  seam, the overview gates, and the Git-first handoff from reporting to explicit
  action.

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
"Alternatives and open decisions" sections, with the first question for Brett
Heap now ruled and applied:

- Measured costs. Both documents derive their caps at 150 ms per Git child,
  a 1.5× margin over an assumed 100 ms per warm child (and about 0.3 s per
  removal) that the proposal must measure, and the overview's listing phase,
  estimated at about 6 s, must be measured too. If measurement disagrees,
  batch cleanup reapplies the same rule with the same fit test, which lowers
  the target cap in steps of 8 and keeps the row cap as large as it can.
  The caps stay provisional until measured, and if warm children average
  more than about 210 ms even with the overview's four-way concurrency, its
  caps must fall or very large estates end incomplete.
- For Brett Heap, ruled and applied: whether a local ancestry proof should
  outrank `remote-gone` for worktree rows. Brett Heap ruled yes on 2026-10-09
  ("yes, local ancestry proof outranks remote-gone"; to lane openRepoProject-2,
  "yes, local ancestry proof outranks remote-gone, apply it"), and both
  proposals applied it: change 1 at `b772195`, change 2 at `cc43860`. Lane
  openRepoProject-3 raised it, recommending yes, and lane openRepoProject-2
  carried it in both proposals. The packet's own ladder tests remote presence
  before merge state, as the baseline does, and the packet designs no mechanism
  for the ruling; GitHub's head-branch auto-delete with `fetch.prune` leaves a
  merged branch's upstream gone, and the MVP never deletes a branch, so under
  that order such a worktree was never eligible for `--all-safe`. Measured here:
  4 of about 90 merged worktrees, `fetch.prune` unset everywhere, and
  auto-delete on 2 of 21 repositories. The proposals now test a branch whose
  configured upstream's remote-tracking ref no longer exists for local ancestry
  before the `remote-gone` rung: when it is merged into the target the row is
  `merged-removable` (`merged-current` when it is the current worktree), and
  otherwise it is `remote-gone`, so only an unmerged row is `remote-gone`. The
  interim `remote-gone` text, the recommendation that called a merged row not
  removable by `project`, is gone from the seven places that carried it. In
  change 1, `push` refuses on the deleted upstream itself, whatever the row's
  class; revalidation does not count a value null in the plan and null again as
  a difference; and `--worktree` removes a merged worktree whose upstream was
  deleted, where `a040790` refuses it as `unpublished`, which is the fifth
  user-visible change; the scenario "A merged worktree whose upstream was
  deleted" keeps its title and gains an AND clause for `--worktree`. In change
  2, requirement 6 and its scenario mirror the ladder, the departures bullet
  quotes Brett Heap's words and records that the ruling supersedes R-6, and
  requirement 10's default-branch finding is untouched.
- For Brett Heap: squash merges never satisfy the ancestry proof, so the MVP
  selects little in a squash-merge repository. The recommendation is a local
  patch-equivalence proof (`git cherry` or patch-id against the merge
  target), designed as a follow-on change, not in the MVP.
- Change 1 council V4, single-target `remove` completeness (other rows'
  inspection errors no longer block it): departure, open to Brett Heap's
  ratification.
- Change 1 council V5, the deferred target cap (more than 16 eligible rows
  are drained 16 per run instead of refused): departure, open to Brett
  Heap's ratification.
- Change 1 council V1, the removal child (never signaled once spawned,
  only a 300 s hard ceiling ending it): departure, open to Brett Heap's
  ratification.
- Change 1 council V10, the per-child budget (`status`, `doctor`, and
  `update` keep 15 s per Git child): departure, open to Brett Heap's
  ratification.
- Change 1 R-21: the Git floor stays 2.36 with a sixteen-name scrub instead of
  task 2.2's rule to raise it to 2.40 (Debian 12 ships 2.39); open to Brett
  Heap at ratification.

Every other decision this list carried is now a proposal decision, open to
ratification, recorded in the
[design-fix handoff](next-session-project-maintenance-fix-handoff.md) under
"Decisions taken by the proposals — 2026-10-08": four-way concurrency, with
the serial fallback of 32 candidates and 128 worktree rows if design rejects
it; no per-repository row cap; no configurable limit; `--apply --json` for
removal only; `--expect-plan` optional; a relative path resolving to the
repository Git finds; sparse skip-worktree entries and never-populated
gitlinks staying excluded; no `attention` alias; the full envelope under
`--attention --json`; the extra `dirty` finding kept; the current spellings
kept; one separate change per extension; bare repositories refused; SIGTERM
and SIGHUP treated as SIGINT; and argv-only suggested commands. Exact
bench/type validation remains existing-doctor follow-up work.

Rejected or deferred alternatives stay closed unless a proposal reopens them:
an arbitrary-depth recursive scan, continuing a batch after a failure, a
persistent resumable plan, and a writer-quiescence or ownership handoff, which
a later design may add on top of the same seam. Keep squash-merged branches
excluded under the local-ancestry contract unless a separately reviewed
preservation/equivalence rule is adopted.

Later OpenSpec proposals can use these documents as input. Implementation work
and executable task lists remain deferred to that later workflow.
