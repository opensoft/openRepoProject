# Next Session: Project Maintenance Design Fixes — Brainstorm

Status: brainstorm
Kind: process
Summary: Handoff for resolving the remaining pre-PR review findings in the project maintenance design packet.
Topics: next-session, project-maintenance, review-followup
Repository context: opensoft/openRepoProject; follow-up work for the project maintenance brainstorm packet.
Captured: 2026-09-11

## Possible feats

- A final design review that is traceable from each safety concern to a concrete contract, scenario, and later OpenSpec decision.

## Current state

At capture (2026-09-11) the design branch `docs/project-maintenance-design`
was at commit `e3a5288`, clean, pushed to origin, with no pull request. The
four-document packet passes the brainstorm packet validator:

- [Packet overview](project-maintenance-overview.md)
- [Project overview and attention](project-maintenance-project-discovery.md)
- [Batch cleanup](project-maintenance-batch-cleanup.md)
- [Inspect and retire synthesis](project-maintenance-synthesis-inspect-and-retire.md)

The packet remains design-only. Do not create an OpenSpec proposal, change
implementation code, or open the PR until the findings below are resolved and
the packet has passed a fresh review.

The packet was revised on 2026-10-07 and corrected the same day in a fix
round after its first adversarial review; the resolution record below maps
each finding to its contract and records which checks remain.

On 2026-10-07 PR #2 (`cleanup`) was closed unmerged on Brett Heap's decision
([decision record][pr2-decision]); the branch stays on origin at `bb91a49` as
harvest source and the packet's `a040790` baseline is unchanged. Follow-ups
for the next revision: absorb `acf0133` and `80fdef3` (doctor repository
health, local-only read-only reporting) into the overview design, and if
paired retirement is proposed, write it as a MODIFIED requirement on
`project-clean`. The first follow-up is discharged by the OpenSpec change
`add-project-overview` (issue #10, PR #12), which absorbs `acf0133` and
`80fdef3` as local-only read-only reporting; the overview design in this
packet does not absorb them.

[pr2-decision]: https://github.com/opensoft/openRepoProject/pull/2#issuecomment-6035824335

## Next-session objective

Make the design packet precise enough to open for review against
`origin/main`, whose current cleanup baseline is `a040790`. Keep the MVP
bounded to local overview reporting and explicit batch worktree removal. Keep
branch deletion, cache disposal, remote queries, family traversal, bench,
container, and park integrations as separately governed extensions unless a
later decision brings one into scope.

## Priority findings to resolve

### 1. Define the batch safety boundary

The [batch design](project-maintenance-batch-cleanup.md) still describes
path-based removal after revalidation while acknowledging that editors or
other processes may change the checkout between those steps. Decide and write
one deterministic guarantee:

- either establish a writer-quiescence/ownership handoff and stable identity
  checks before removal, or
- narrow the guarantee explicitly so concurrent writers are outside the safe
  contract and any identity change causes a refusal.

Define the observable identity as the Git common-directory and worktree-admin
registration plus no-follow device/inode checks for the repository and target
path. A path string by itself is insufficient. State what happens when the
target directory, repository parent, branch, or ignored files change after
confirmation.

Choose one deterministic branch-race result. The MVP keeps the local branch,
so a changed branch must produce a refused target, exit 2, and no later target
attempts. If removal succeeds before the change is observed, the postcondition
must rescan and report the removed worktree plus the retained branch SHA.

### 2. Make execution and interruption reconcilable

Clarify that `--apply` recomputes, displays, and confirms its own fresh plan;
the earlier read-only preview is advisory and is never silently reused. Define
one shared mutation seam so single-target removal and a one-item batch have the
same plan, revalidation, command, and refusal behavior.

Use one global deadline that covers Git probes and the removal subprocess, with
an explicit timeout unit. Cancellation or deadline expiry must stop new work,
terminate and reap the in-flight child when possible, rescan the Git worktree
registry, target path, repository identity, and retained branch, then report
`outcome-unknown` when state cannot be established. Return a nonzero result and
never claim a target completed from a subprocess exit alone.

Post-operation reconciliation must define stages for removed, refused, failed,
and unknown outcomes. It must record whether the Git registry entry exists,
whether the target path exists, and whether the local branch and SHA remain.

### 3. Bound and share the expensive work

The current design has limits, but the next revision must make their execution
model implementable:

- Separate repository-wide probes from worktree-specific probes. Memoize one
  common-directory probe and fan it out; use targeted per-worktree revalidation
  instead of recomputing the full report for every target.
- Define the five-second probe and sixty-second invocation deadlines against a
  monotonic global deadline. Include subprocess cancellation and omitted-result
  reporting. Reduce the 1,024-worktree and 100-target caps if the measured
  operation count cannot meet the deadline.
- Sort canonical candidate paths before applying discovery caps. An omitted
  count after early stop is a lower bound or unknown unless it was obtained
  within the same directory-entry/time budget.
- Bound ignored-file inspection and report size with count/truncation fields;
  do not materialize an unbounded `git status --ignored` result in memory or
  JSON.
- If remote inspection remains in the deferred text, add response page,
  item, and byte limits. A global deadline must cancel queued and in-flight
  requests and classify truncation as unknown.

### 4. Make the repository and JSON contracts explicit

The batch command must not require a merge-target worktree if the current
`origin/main` operation can execute from the resolved repository root. Define
the command directory as the canonical resolved repository root, subject to
the identity checks above, and preserve the existing explicit branch action.

Define the overview JSON and batch JSON separately or state an additive
compatibility plan. Preserve existing cleanup fields such as `root`,
`target_branch`, `tracking_freshness`, and `worktrees` when compatibility is
required. For every proposed envelope, record required field types, stable
identity rules, enum values, unknown/error representation, completeness, and
schema evolution. Add representative fixtures rather than only listing field
names.

Suggested commands and JSON rows must carry the canonical repository path or
common-directory identity, so duplicate project names and independent clones
cannot hand off to an ambiguous `project clean` invocation.

### 5. Close discovery scope and acceptance gaps

In the MVP, a `family.yaml` marker is reported as a holder-only local project.
Do not traverse siblings, pinned members, or mounted legs until a family
integration is separately proposed. Add a scenario proving the holder count,
relationship handling, and probe ownership.

Define the collector boundary before calling existing helpers: malformed,
unreadable, no-merge-target, and timed-out candidates become visible result
records with errors, while healthy projects continue. Existing helpers that
raise for one candidate must not erase the rest of the scan.

Add acceptance scenarios for:

- manifest-declared, `origin/HEAD`, `main`, `master`, conflicting, and missing
  merge targets, including source and SHA selection and zero mutation;
- every protected cleanup classifier, with only `merged-removable` selected;
- `--attention` filtering repair, preservation, housekeeping, and ordinary
  unmerged informational work while keeping exit semantics stable;
- a present eligible external linked worktree and a missing/unreadable one;
- newline, tab, and control-character paths, using NUL-delimited Git output or
  an explicit supported-byte refusal;
- canonical repository identity through the overview-to-clean handoff.

## Deferred remote boundary

Keep remote inspection deferred unless the next session intentionally scopes it
into a separate design. If the detailed constraints remain in the packet,
require canonical GitHub identity, rejection of credential-bearing remotes,
bounded deduplicated requests, response-size/page limits, redaction, and
explicit unknown results for 401, 403, rate-limit, timeout, and truncation.
Remote evidence remains explanatory and never authorizes cleanup.

## Suggested work order

1. Reconcile the batch contract with `origin/main` and remove any remaining
   prerequisite inherited from unmerged cleanup commits.
2. Specify identity, writer/race behavior, global deadlines, cancellation, and
   post-operation reconciliation.
3. Specify the shared single-target/batch mutation seam and exact JSON fields.
4. Narrow and formalize overview collection, family-holder behavior, caps,
   probe accounting, and error isolation.
5. Add the acceptance scenarios and deferred-extension boundaries above.
6. Run the packet validator, whitespace checks, and a fresh pre-PR review. Open
   the PR only when the review has no actionable findings.

## Completion gate

The next session is complete when the four packet documents plus this handoff
are clean and pushed, the packet validator passes, every high/P1 finding has a
written contract and scenario, and no implementation or OpenSpec proposal has
been created. The PR description should state that the branch contains design
only and link this handoff for the review trail.

## Resolution record — 2026-10-07

The packet was revised on 2026-10-07 against the five findings above, and a fix
round then resolved every high and medium finding of the first adversarial
review. Each row gives the decision taken, the document and exact section
headings that hold its contract, and the validation scenarios that prove it.
"Batch" is [batch cleanup](project-maintenance-batch-cleanup.md) and "Overview"
is [project overview and attention](project-maintenance-project-discovery.md);
headings read `section: subsections`. The design contract baseline is still
`a040790`. `origin/main` is now `7a9134b`, which merged PR #13 (lane
openRepoProject-1's archive of the `prefer-triad-in-project-new` OpenSpec
change, `openspec/` only) after `d7f6b0e` merged PR #8 (feature 002, "offer the
Triad first in `project new`") on 2026-10-08. Before them, `da33d92` merged
PR #7 (this packet) on 2026-10-07, PR #4 archived the completed OpenSpec changes
and promoted their specifications to `openspec/specs/`, and PR #5 added the
`prefer-triad-in-project-new` OpenSpec proposal. PR #8 added about 141 lines to
`project`, in the project-creation code between `choose()` and the end of
`new()`, and 1,163 lines to `tests/test_project.py`; the cleanup, status,
doctor, and update paths are unchanged in content but sit about 141 lines lower,
so every `project` line citation stays pinned at `a040790`, whose `project` is
byte-identical through `da33d92`.

| Finding | Decision | Contract | Proving scenarios |
| --- | --- | --- | --- |
| 1. Define the batch safety boundary | The guarantee is narrowed: concurrent writers are outside the safe contract, and a removal child is spawned only when the repository identity `{root, common_dir, dev, ino}`, the worktree identity `{path, dev, ino, admin_id}` with two-way admin registration, the branch evidence, every baseline signature field, the `locked` flag, the absence of submodules (a gitlink or an admin `modules` entry) and of hidden local state (an index entry flagged assume-unchanged or skip-worktree), read by a bounded `git -C <worktree path> ls-files -v --stage -z` inside the target worktree under the probe directory rule, the manifest's `tracking_branch`, and the merge target `{name, source, sha}`, re-resolved from a fresh manifest read, still equal the confirmed plan at revalidation; otherwise the target is `refused` (`identity-changed`, `branch-changed`, `state-changed`, `contains-submodule`, or `hidden-local-state`), no later target is attempted, and the exit is 2. A repository replaced after a removal makes that target `unknown` with `unconfirmed-removal`, and the exit is 1. The removal runs as `git -c status.showUntrackedFiles=normal -c core.untrackedCache=false -c core.fsmonitor=false -C <command directory> worktree remove <path>`, the last two pins added on 2026-10-08 by change 1 council V3, so Git's own non-force check sees untracked files whatever the user's configuration; ignored files created and index flags set after revalidation are the documented residual window. A branch change seen only after removal is `removed` with `branch-advanced-after-removal` (or `branch-missing-after-removal`), exit 2, and the branch retained. | Batch, "Eligibility and merge-target terminology"; "Safety boundary": "Identity", "The narrow guarantee", "Changes after confirmation", "Residual window", "Branch race"; "Probe accounting and limits": "Probe directory rule", "Worktree-specific probes", "Preflight and targeted revalidation" | Batch: **Hidden local state.**, **Submodules.**, **Target directory replaced.**, **Admin registration changed.**, **Parent directory swapped.**, **Repository replaced mid-batch.**, **New worktree and pre-removal changes.**, **State changes before revalidation.**, **Changed later target.**, **Untracked file under `status.showUntrackedFiles=no`.**, **Untracked cache.**, **Ignored file in the residual window.**, **Branch advances before removal.**, **Branch advances after removal.** |
| 2. Make execution and interruption reconcilable | `--apply` always recomputes, prints, and confirms a fresh plan carrying `plan_digest`, and an optional `--expect-plan` refuses a differing one with `plan-digest-mismatch`. Single-target `remove` is strictly a one-item batch on the shared `retire_worktree` seam (revalidate, spawn, reap, reconcile): the same full plan (`mode: "single"`) under the same caps, the refusals `worktree-not-found` and `target-excluded`, and `inspection-incomplete` when any row is `inspection-error`; amended on 2026-10-08 by change 1 council V4, a departure open to Brett Heap's ratification, its completeness is the repository-wide evidence plus its own row, other rows' `inspection-error`, `inspect-cap`, and unprobed states being non-blocking omissions, while its own revalidation stays fully strict. One monotonic 60 s deadline holds back a 10 s reconciliation reserve, so work stops at 50 s, with 5 s per probe and every filesystem call in a worker thread; SIGINT or expiry terminates and reaps the child's process group before a rescan (amended on 2026-10-08 by change 1 council V1: a probe child's only, since a spawned removal child is never signaled; SIGINT, SIGTERM, SIGHUP, and the deadline wait for it to exit, a 300 s hard ceiling kills its group, and a child that exits nonzero on its own stays `failed`, even after a signal, while after a ceiling kill or an exit that could not be observed the rescan decides the stage, `removed` when the registry entry and the path are both gone and `unknown` with the `partially-removed` note when either remains, reason `removal-ceiling` naming a ceiling kill, with which a `removed` target exits 1 (lane openRepoProject-2 ruling M1, 2026-10-09, confirmed 2026-10-09; change 1's text at `0669a20` said always `unknown`, corrected in its phase 6 at `90854a3`), so a run, not counting time blocked at the confirmation question (ruling R-11), is bounded at 64 s, the 50 s of work, the 10 s reserve, and up to 4 s of termination, plus up to 300 s for a removal in flight), and no removal is spawned with less than `removal_floor_seconds` (5 s) of the work deadline left: that target and every later one are `not-attempted` with `deadline-exceeded`, and the exit is 1. Every target ends in the stage enum `pending`, `removed`, `refused`, `failed`, `unknown`, or `not-attempted`, and every `removed`, `refused`, `failed`, or `unknown` target carries a reconciliation record (`registry_entry_present`, `path_present`, `branch_present`, `branch_sha`, `reconciled`); `removed` needs rescan evidence and `reconciled: true`; an unproven outcome, or an exception after the apply phase begins, is `unknown` with exit 1; and a `failed` target (`git-refused` for exit 128, `git-failed` for any other status such as 255 with an `orphaned-directory` note, or `spawn-error`) exits with Git's own status, or 2 for `spawn-error`. | Batch, "Execution model": "Fresh plan and plan digest", "One mutation seam", "Deadline and budgets", "Interruption and expiry", "Stages and reconciliation", "Exit codes"; "Repository and JSON contract": "Apply result record"; "Baseline behavior changes"; "Partial completion and recovery" | Batch: **Deadline expiry mid-batch.**, **Hard ceiling.**, **Exit 0 without evidence.**, **SIGINT.**, **Git leaves an orphaned directory.**, **Git refuses the removal.**, **Unreadable path after removal.**, **Exception after the apply phase begins.**, **Single target equals a one-item batch.**, **Preview is advisory.**, **Plan digest mismatch.** |
| 3. Bound and share the expensive work | Both documents use one probe set: one `git --version` per invocation; per repository, memoized by `common_dir` and fanned out, the same four repository-wide children (identity, registry listing, ref listing in one shared NUL-separated `for-each-ref` format, and merged set); and per present, registration-verified worktree row, the main worktree included, one combined status probe that stops at a 65th ignored record or a 4,097th record. Every worktree-specific probe runs as `git -C <worktree path>` against that worktree's own index after its identity is verified, and repository-wide probes run as `git -C <repository.root>` (`common_dir` for a bare repository), except the identity probe, which runs in the candidate; when a linked worktree is reached first, the registry listing also runs in the candidate, because the main worktree's path comes from that listing, which changes which directory the command runs in, never which index a probe reads. Batch revalidation is a targeted check of at most five children plus a manifest re-read and a `modules` check, and `probes` and `operations` (`{estimated, performed}`) appear in both the plan and the apply result record. Candidates and registry entries are sorted before any cap, and dropped work is reported as `omitted: {count, exactness}`. Both derive their caps at 150 ms per Git child, a 1.5× margin over the assumed 100 ms. The batch probes serially and uses one fit test, a worst case that completes within the 50 s work deadline and spawns its last removal with at least `removal_floor_seconds` (5 s) left: its row cap is the largest power of two for which at least 16 targets fit, and its target cap the largest multiple of 8 that fits with it, so it inspects at most 128 worktree rows (`limits.worktree_rows`, the main worktree included) and selects at most 16 targets, with a worst case of about 39.9 s. The overview takes at most 32 roots, 128 candidates, and 512 worktree rows with four concurrent children across repositories, after a listing phase estimated at about 6 s, one worker task per root bounded at 5 s, which leaves about 54 s for Git work. A cap hit or deadline gives an incomplete result (`inspect-cap`, `inspection-incomplete`, or `deadline-exceeded` in the batch; `scan-limit`, `probe-timeout`, or `deadline-exceeded` in the overview). | Batch, "Execution model": "Deadline and budgets"; "Probe accounting and limits": "Probe directory rule", "Repository-wide probes", "Worktree-specific probes", "Preflight and targeted revalidation", "Cap arithmetic", "Inspection order and omitted work", "Bounded ignored-file inspection", "Probe and operation estimates". Overview, "Discovery scope and ordering": "Ordering, truncation, and omitted counts", "Caps and their arithmetic"; "Probe model and deadline": "Git version check", "Repository-wide probes", "Worktree-specific probes", "Scheduling and concurrency", "Deadline and timeouts", "Probe accounting"; "Deferred remote inspection boundary" | Overview: **One probe set per repository.**, **Candidate cap after sorting, exact count.**, **Candidate cap with an incomplete listing.**, **Root and worktree-row caps.**, **Probe timeout.**, **Hung filesystem call.**, **Invocation deadline.**, **Bounded concurrency.**, **Bounded ignored files.**, **User status configuration.**, **Git version refusal.**, and the remote item under "Deferred validation scenarios". Batch: **Row cap and planning failures.**, **Target cap.**, **Ignored-file bound.**, **Bounded revalidation work.** |
| 4. Make the repository and JSON contracts explicit | The command directory is the canonical, identity-checked `repository.root` (or `common_dir` for a bare repository) with no merge-target worktree requirement. Every `project clean` mode resolves an absolute path Git-first and refuses `target-not-repository-root` with exit 2 unless it is exactly a main worktree root; a relative path or no argument resolves to the repository Git finds there; only a bare name keeps the `discover` lookup, its Git child counted and bounded; and the report's `root` always names the command directory. The overview prints a new `schema_version: 1` envelope with typed project-row, worktree-row, finding, and `summary` fields; the batch plan is an additive superset of the baseline clean report with `limits`, `budget`, `probes`, and `operations`; the apply result record is defined and rendered as human text; both documents state representation rules with fixtures; a non-UTF-8 `repository.root` or `common_dir` refuses with `unsupported-path-bytes`; an unreadable or wrong-kind manifest is `manifest-invalid`; under `--json` an overview exit 2 prints the baseline error object with a `code` added, `{"error", "code"}`, which batch cleanup extends with its plan fields when no plan can be built, and an argument error prints no JSON; `suggested_command` is `null` unless a finding supplies one, and otherwise a JSON argv array naming the canonical root; and both documents list their baseline behavior changes. | Batch, "Repository and JSON contract": "Command directory and repository resolution", "Representation rules", "Plan envelope", "Refusal codes", "Apply result record", "Fixtures", "Machine-readable apply results"; "Baseline behavior changes". Overview, "JSON contract": "Envelope", "Project row", "Finding object", "Representation rules", "Repository identity and the clean handoff", "Path encoding", "Fixture"; "Result semantics"; "Baseline behavior changes" | Batch: **Overview handoff keeps identity.**, **Absolute path that is not a repository root.**, **Non-UTF-8 repository root.**, **Merge target missing, invalid, or conflicting.** Overview: **Canonical identity through the handoff.**, **Independent clones and aliases.** |
| 5. Close discovery scope and acceptance gaps | A `family.yaml` holder is one `family-holder` row counted once, with `relationships: []` and Git probes only when its own directory is the toplevel. A marker check that fails with anything but `ENOENT` or `ENOTDIR` makes an error row with `kind: null`; `collect(candidate) -> result` turns helper exceptions (such as `manifest-invalid`, `os-error`, or `internal-error`) and failed or timed-out probes into error rows while the scan continues, and path candidates never pass through `discover`. An unreadable or registration-mismatched worktree row is set to `inspection-error` directly, bypassing the ladder. A missing merge target becomes `merge_target: null` with a `no-merge-target` finding and no `cleanup_report` call. A `merged-removable` worktree yields the housekeeping finding and the `--all-safe` suggestion only after the batch's main-worktree, path-byte, registration, and lock gates, and otherwise the first failing gate's finding (`main-worktree`, `unsupported-path-bytes`, `registration-mismatch`, or `locked-worktree`, the batch's own exclusion reasons); a fifth gate withholds every `--all-safe` suggestion for a repository while any of its worktree rows is `inspection-error` or it has more than 128 worktree rows, because the batch plan would be refused as `inspection-incomplete` or `inspect-cap`, so its housekeeping findings and the row suggest only the read-only `project clean <root>`; the batch may still exclude a suggested worktree as `hidden-local-state` or `contains-submodule`, which only its own index probe and admin-directory check see. `review-required` is covered by a classifier test on an injected row; paths are read NUL-delimited; a path holding a control, bidirectional, or format code point or an undecodable byte prints in `$'…'` form with `\uXXXX` and `\xHH` escapes in lowercase hexadecimal (pasting the `\uXXXX` form needs a UTF-8 locale), JSON escapes every such code point, and a non-UTF-8 path is escaped and excluded as `unsupported-path-bytes`; and every acceptance scenario the finding listed is written. | Overview, "Discovery scope and ordering": "Candidates", "Repositories and linked worktrees", "Family holders"; "Collector boundary and error isolation"; "Merge target and classification reuse"; "Attention categories"; "JSON contract": "Path encoding"; "MVP validation scenarios". Batch, "Eligibility and merge-target terminology" | Overview: **Family holder count, relationships, and probe ownership.**, **Unreadable candidate directory.**, **One helper failure is isolated.**, **Manifest target.**, **`origin/HEAD` target.**, **`main` target.**, **`master` target.**, **Conflicting targets.**, **Missing target.**, **Every protected classifier.**, **Gated merged worktrees.**, **Attention filter per category.**, **Present eligible external worktree.**, **Missing external worktree.**, **Unreadable external worktree.**, **Control and format characters in paths.**, **Non-UTF-8 path.**, **Canonical identity through the handoff.**, **Local and read-only.** Batch: **Stable order and preserved work.**, **Every protected classifier.**, **Paths and empty plans.**, **Control-character and non-UTF-8 paths.**, **Merge target missing, invalid, or conflicting.** |

### Cross-document decisions

- Narrow guarantee: concurrent writers are outside the safe contract. The MVP
  claims no lock, lease, or writer-quiescence handoff, refuses on any change
  it observes at revalidation, and documents the residual window for ignored
  files created, and index flags set, after it.
- Removal command: single-target and batch removal both pass
  `-c status.showUntrackedFiles=normal`, `-c core.untrackedCache=false`, and
  `-c core.fsmonitor=false` to the non-force
  `git -C <command directory> worktree remove <path>`, so Git's own check
  sees untracked files under any user configuration. The last two pins were
  added on 2026-10-08 by change 1 council V3, and `-c` also overrides
  `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`, which the environment scrub
  leaves.
- Index gates: batch cleanup never removes a worktree whose index holds a
  gitlink or whose admin directory holds `modules` (`contains-submodule`),
  or whose index flags an entry assume-unchanged or skip-worktree
  (`hidden-local-state`). One bounded
  `git -C <worktree path> ls-files -v --stage -z` probe and an `lstat` of the
  admin `modules` directory check both for rows that pass every other gate,
  at plan time and at revalidation, so sparse checkouts are excluded; the
  overview does not run them.
- Probe directory rule: every worktree-specific probe runs as
  `git -C <worktree path>` against that worktree's own index, only after its
  identity is verified; repository-wide probes run as `git -C <repository.root>`
  (`common_dir` for a bare repository), except the identity probe, which runs in
  the candidate. When a linked worktree is reached first, in canonical
  candidate order, the registry listing also runs in the candidate, because
  the main worktree's path comes from that listing; that changes which
  directory the command runs in, never which index a probe reads. As amended
  on 2026-10-08 by change 1 council X2 with change 1's R11 and by change 2
  council V2, when the first registry record's path equals `common_dir`,
  `clean` first refuses a submodule checkout, for which
  `git rev-parse --show-superproject-working-tree` prints a path, with
  `target-not-repository-root` (R11's precedence, settled by lane
  openRepoProject-2's ruling of 2026-10-09); otherwise the main checkout is
  a gitfile checkout, whose main worktree is the realpath of `core.worktree`
  or, where that is unset, as Git 2.43 leaves it after
  `git init --separate-git-dir`, the candidate toplevel whose `.git` file
  names `common_dir`, and that record is never a status-probe row. `clean`
  also refuses, the same way, a linked worktree of such a repository whose
  `core.worktree` is unset; the overview gives a main worktree it cannot name
  `repository.root: null` with an `unsupported-layout` finding, a submodule
  checkout included (lane openRepoProject-2 ruling R-2, change 2 at `996a181`),
  and a missing one `main-worktree-missing`, the repository-wide probes then
  running in the candidate. Where `root` is null (a bare repository, a missing
  main worktree, or a gitfile checkout whose main worktree cannot be named), the
  repository-wide probes run in `common_dir` for a bare repository and otherwise
  where the identity probe ran, as the shared evidence model states (lane
  openRepoProject-2 ruling R-13, R-13a in its messages, 2026-10-09; change 1 at
  `4f2162b`).
- Git-first resolution: every `project clean` mode (the read-only report,
  `--json`, `--all-safe`, and `--apply --action push|remove|delete-branch`)
  resolves an absolute path Git-first. It must be exactly the main worktree
  root, or the run refuses with `target-not-repository-root` and exit 2, with
  no redirection. A relative path or no argument resolves to the repository
  Git finds there; only bare names keep `discover`, and the overview never
  calls it. The overview's `suggested_command` is a JSON argv array naming
  that root.
- One mutation seam: single-target removal is strictly a one-item batch on
  `retire_worktree`, so an inspection error anywhere in the repository
  refuses it as it refuses a batch. Amended on 2026-10-08 by change 1
  council V4, a departure open to Brett Heap's ratification: the
  single-target plan's completeness is the repository-wide evidence plus the
  named target's own row, so other rows' inspection errors, cap omissions,
  and unprobed states are non-blocking omissions, while the target's own
  revalidation stays fully strict.
- Overview gates: a `merged-removable` worktree gets the housekeeping finding
  and the `--all-safe` suggestion only when it passes the batch's main-worktree,
  path-byte, registration, and lock gates in the batch's order, under the same
  codes the batch uses as exclusion reasons (`locked-worktree` for the lock),
  and only while no worktree row of its repository is `inspection-error` and the
  repository has no more than 128 worktree rows, which would make the batch plan
  `inspection-incomplete` or `inspect-cap`, and, as amended on 2026-10-08, no
  worktree row of it went unprobed because the 512-row cap or the deadline cut
  it; otherwise the read-only `project clean <root>` is suggested, and the gate
  changes suggestions only. As amended by change 2 council V5, `target-cap` only
  limits: the `--all-safe` suggestion stays, its findings carrying
  `suggestion_gate: "target-cap"`. An unstarted worktree keeps its finding with
  only the read-only suggestion and `suggestion_gate: "unstarted-branch"`
  (rulings N-5 and P6-5 on change 1 council V2's gate), and a merged worktree
  whose reflog cannot decide keeps it with only the read-only suggestion and
  `suggestion_gate: "reflog-unavailable"` (change 2, read at `996a181`, final
  `4495ae7`), the overview reading the branch's reflog as the batch does (the
  D10 amendment and ruling R-12, change 1 at `0b3c33d` and `4f2162b`). The batch
  may still exclude a suggested worktree as `hidden-local-state` or
  `contains-submodule`, which only its own index probe and admin-directory check
  see.
- Shared probes: one version check per invocation, the same four
  repository-wide children per repository (identity, registry listing, ref
  listing, and merged set) with one identical ref-listing format, and one
  combined bounded probe per worktree row,
  `git status --porcelain=v1 -z --untracked-files=normal --ignored=matching`,
  run with `-c core.untrackedCache=false -c core.fsmonitor=false` (added on
  2026-10-08 by change 1 council V3), in both documents. All Git output is
  parsed NUL-delimited.
- Caps at 150 ms per Git child, a 1.5× margin over an assumed 100 ms that
  the proposal must measure: the batch inspects 128 worktree rows, the main
  worktree included, and selects 16 targets (Batch "Cap arithmetic"); the
  overview takes 32 roots, 128 candidates, and 512 worktree rows
  (Overview "Caps and their arithmetic") with four concurrent children across
  repositories, after a listing phase estimated at about 6 s that leaves
  about 54 s for Git work. Both name the row cap `limits.worktree_rows`, which
  in a `clean` plan holds only that mode's cap; the overview reads the batch's
  128 and the report's 256 from the shared constants and reports them in its
  `limits` as `batch_row_cap` and `report_row_cap`, beside the batch's target
  limit (lane openRepoProject-2 ruling R-7, landed in change 2 at `996a181`,
  2026-10-09). They replace the earlier 1,024/100 and 256/1,024 figures, which
  could not meet the deadline.
- Batch cap decision: 16 targets, not 24. A cap pair fits when its worst
  case completes within the 50 s work deadline and spawns its last removal
  with at least `removal_floor_seconds` (5 s) left. The row cap is the
  largest power of two for which at least 16 targets fit, and the target cap
  the largest multiple of 8 that fits with that row cap: 128 rows and 16
  targets, with a worst case of about 39.9 s and the 16th removal spawned at
  39.15 s. 256 rows admit fewer than 16 targets under the test and are
  rejected, and 24 targets would fit the deadline alone, but the 21st
  removal would start inside the floor. At the 100 ms assumption the caps
  leave about 21.8 s of headroom.
- Removal floor: `removal_floor_seconds` (5 s) joins the batch `budget`; no
  removal is spawned with less than 5 s of the work deadline left, and the
  remaining targets are `not-attempted` with `deadline-exceeded`, exit 1. The
  300 s hard ceiling joins it as `removal_ceiling_seconds: 300` (change 1 phase
  6 (`90854a3`), lane openRepoProject-2, 2026-10-09).
- Concurrency: the overview runs at most four read-only Git children across
  distinct repositories and never two once their `common_dir` is known to be
  the same (`probe_concurrency: 4`); batch probing is serial
  (`probe_concurrency: 1`).
- Codes: `deadline-exceeded` and `probe-timeout` for the two time limits,
  and `manifest-invalid`, `git-unavailable`, and `git-too-old` (Git older
  than 2.36, exit 2 before any repository probe), with the same spelling in
  both documents.
- `remote-gone`: the shared ref listing reports a deleted upstream as `gone`,
  so overview and clean both classify it `remote-gone` where `a040790`
  reports `unpublished`; both are preserve states. Doctor never classifies a
  deleted upstream; its only worktree classification is `repo_state`'s
  `stale-worktree`, shown under `--json`.
- `ignored_files` keeps its baseline name and type but counts the ignored
  records read, a lower bound when `ignored_files_truncated` is true.
- Path escaping: a path holding a control, bidirectional, or format code
  point or an undecodable byte prints in the same `$'…'` form in both
  documents, with `\xHH` for each undecodable byte and `\uXXXX` for each
  decoded control, bidirectional, or format code point, both in lowercase
  hexadecimal, and each backslash doubled; pasting the `\uXXXX` form needs a
  UTF-8 locale. JSON escapes every such code point. Lane openRepoProject-2
  ruling R-8 names the escaped code points by Unicode general category, keeping
  the enumerated ones this rule shares as examples; see "Rulings R-4, R-8, and
  R-9 — 2026-10-09" below.
- JSON error object: under `--json`, an overview exit 2 prints
  `{"error", "code"}`; batch cleanup prints the same object extended with its
  plan fields when no plan can be built; argument errors print no JSON.
- `plan_digest`: the SHA-256 of the repository identity, the merge-target
  name and SHA, and the canonically ordered selected path, branch, and head.
  The optional `--expect-plan` refuses a differing fresh plan with
  `plan-digest-mismatch` and exit 2.
- Baseline behavior changes: both documents carry the section, and the
  [packet overview](project-maintenance-overview.md) lists their union.

### Open proposal decisions

These were the open decisions when PR #7 merged, followed by the entries
added on 2026-10-08. The entries marked decided were taken on 2026-10-08 by the
proposals as proposal decisions, open to ratification, under lane
openRepoProject-2's OQ numbers (see "Decisions taken by the proposals —
2026-10-08"), and the first question for Brett Heap is marked ruled, as he ruled
it on 2026-10-09; the others remain open: the measured costs, the second
question for Brett Heap, and the four change 1 council rulings this record
labels departures, V1, V4, V5, and V10, which await his ratification. The
[packet overview](project-maintenance-overview.md) carries the open entries and
names the decided ones in one paragraph.

- The measured per-child and per-removal costs and the overview's listing
  time, and therefore the final caps; the batch reapplies the same rule and
  fit test, which lowers the target cap in steps of 8 and keeps the row cap
  as large as it can. Open (OQ-4): the caps stay provisional until measured
  (ruling D-Q).
- Caps versus concurrency: if the overview's four-way concurrency is
  rejected, its fallback is 32 candidates and 128 worktree rows (257
  children, about 38.6 s at 150 ms, or about 44.6 s with the listing
  estimate); above about 210 ms per child even concurrency needs lower caps.
  Decided 2026-10-08 (OQ-6): four-way concurrency, with that fallback if
  design rejects it.
- Whether to cap worktree rows per repository, since one repository with
  more than about 355 worktree rows cannot complete at 150 ms per child.
  Decided 2026-10-08 (OQ-7): no cap; such a repository ends at the deadline,
  visibly incomplete.
- Whether any limit is user-configurable. Decided 2026-10-08 (OQ-8): no; the
  fixed values are reported in `limits` and `budget`.
- Whether `--apply --json` prints the apply result record (recommended) or
  the MVP stays human-only. Decided 2026-10-08 (OQ-10, ruling D-C): it does,
  for `--all-safe` and `--action remove` only.
- Whether `--expect-plan` is required whenever `--yes` is used; the MVP makes
  it optional. Decided 2026-10-08 (OQ-11): optional.
- Whether a relative path or the no-argument default must be an exact
  repository root, as an absolute path must, instead of resolving to the
  repository Git finds there. Decided 2026-10-08 (OQ-12): it resolves to the
  repository Git finds there.
- Whether a skip-worktree entry whose file is absent from disk, as in a
  sparse checkout, may be treated as safe instead of `hidden-local-state`.
  Decided 2026-10-08 (OQ-13): no, it stays `hidden-local-state`.
- Whether a gitlink that was never populated, in a worktree whose admin
  directory holds no `modules`, may be treated as removable instead of
  `contains-submodule`. Decided 2026-10-08 (OQ-14): no, it stays
  `contains-submodule`.
- Whether bare repositories are supported or refused. Decided 2026-10-08
  (OQ-15): refused.
- Whether SIGTERM and SIGHUP receive the SIGINT treatment. Decided
  2026-10-08 (OQ-16): yes, exiting 143 and 129, for `clean` and the overview.
- Whether the `attention` alias merits a separate command, and how
  `--attention --json` filters. Decided 2026-10-08 (OQ-17, OQ-18): no alias,
  and `--attention --json` prints the full envelope.
- Whether suggested commands also carry a display string (decided
  2026-10-08: no, argv arrays only), and whether the extra `dirty` finding
  for a dirty default-branch checkout is wanted (decided 2026-10-08, OQ-19:
  kept).
- The final command and flag spelling. Decided 2026-10-08 (OQ-26): the
  current spellings are kept.
- Whether cache disposal, paired branch retirement, and the remote, family,
  bench, container, and park integrations deserve separate changes. Decided
  2026-10-08 (OQ-27): yes, one change each.
- For Brett Heap, ruled: whether a local ancestry proof should outrank
  `remote-gone` for worktree rows. Brett Heap ruled yes on 2026-10-09 ("yes,
  local ancestry proof outranks remote-gone"); see "Rulings R-11 to R-20 and
  Brett Heap's ruling — 2026-10-09"; the proposals' interim `remote-gone` text
  quoted below is lane openRepoProject-2's to amend, sha to follow, and the
  packet designs no mechanism for the ruling. Lane openRepoProject-3 raised it
  on 2026-10-08, recommending yes, and lane openRepoProject-2 carries it in both
  proposals. The ladder tests remote presence before merge state, as the
  baseline does; GitHub's head-branch auto-delete with `fetch.prune` leaves a
  merged branch's upstream gone; and the MVP never deletes a branch, so under
  the baseline order such a worktree is never eligible for `--all-safe`, and
  `push` now refuses its branch. Measured here: 4 of about 90 merged worktrees,
  `fetch.prune` unset everywhere, and auto-delete on 2 of 21 repositories. Until
  the proposals are amended, the packet keeps the baseline ladder; a
  `remote-gone` row whose `merged_into_target` is true carries the
  recommendation "Merged locally, upstream deleted: not removable by `project`
  until the open question is ruled; review, then `git worktree remove` yourself"
  (change 1 council V7), and the overview's `remote-gone` message says whether
  the branch tip is already an ancestor of the merge target when its evidence
  establishes that, its suggestion only reviewing (change 2 council V11).
- For Brett Heap: squash merges never satisfy the ancestry proof, so the MVP
  selects little in a squash-merge repository (change 1 council V2). The
  recommendation is a local patch-equivalence proof (`git cherry` or
  patch-id against the merge target), designed as a follow-on change, not in
  the MVP.
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

### Checks

- Packet validator: PASS, printing
  `PASS: 4 docs (2 atomic, 1 synthesis, 1 overview)` for the command below.
- `git diff --check`: clean.
- Adversarial review round 1: 6 high / 14 medium / 15 low findings, all high
  and medium resolved in the fix round; verification review round 2: 3 high /
  9 medium / 13 low; all high and medium resolved in fix round 2; targeted
  re-verification of the round-2 fixes: 0 high / 1 medium / 4 low, all five
  resolved before the PR; result also recorded in the PR.
- Design-only PR: [opensoft/openRepoProject#7][pr7] (governing issue
  [#6][issue6]), opened 2026-10-07 from commit `506a66b`.

[pr7]: https://github.com/opensoft/openRepoProject/pull/7
[issue6]: https://github.com/opensoft/openRepoProject/issues/6

```sh
python3 -I ~/.claude/skills/document-software-brainstorm/scripts/validate_packet.py \
  --root ideation/brainstorm --packet-prefix project-maintenance
git diff --check
```

The completion gate is met: the packet passes the packet validator, every
high finding has a written contract and scenario, and the design-only PR #7
was reviewed and merged on 2026-10-07 as `da33d92`. No OpenSpec proposal was
to be written until that PR was reviewed and merged, and the remaining
follow-up above, writing paired retirement as a MODIFIED requirement on
`project-clean` if it is proposed, is for the next revision.

### Decisions taken by the proposals — 2026-10-08

The packet is a non-normative design record (packet overview, "Status and
motivation"). Lane openRepoProject-2 is proposing the two OpenSpec changes
it feeds, `add-project-clean-all-safe` (issue #9, draft PR #11) and
`add-project-overview` (issue #10, draft PR #12), and those proposals are
the governing text. They took the open items below as proposal decisions,
open to ratification, and departed from some packet decisions, each bullet
saying so; this revision keeps the record accurate and re-decides nothing.
A ruling is lane openRepoProject-2's of 2026-10-08 unless marked as lane
openRepoProject-3's. Where a decision changes a packet sentence, the
sentence now states the decision, and its bullet names the passages under
"decided by the proposal".

- `add-project-clean-all-safe` and `add-project-overview`, bare
  repositories (OQ-15, ruling D-E): refused in every `clean` mode with
  `target-not-repository-root`, exit 2; an overview row for one has
  `repository.root: null` and no clean suggestion, as the packet already
  said. Decided by the proposal: Batch "Identity" says the MVP refuses them
  and keeps its bare-repository clauses as a sketch for a later extension;
  the refusal replaces the void baseline change for a bare repository's
  first registry record in Batch and the packet overview; and the packet
  overview's first-version scope no longer names a bare command directory.
- `add-project-clean-all-safe` and `add-project-overview`, SIGTERM and
  SIGHUP (OQ-16, ruling D-O, with ruling D-F for `clean`): the SIGINT
  treatment, exiting 143 and 129, now decided for both commands. In the
  `clean` apply phase the first signal received sets the status; before it
  they exit 143 and 129 with zero mutation. Decided by the proposal: Batch
  "Interruption and expiry" and "Exit codes", Overview "Result semantics",
  and the exit lists of the packet overview and the synthesis.
- `add-project-overview`, suggested commands: `suggested_command` stays an
  argv array only, with no display string. No packet sentence changes; the
  entry leaves the open lists.
- `add-project-clean-all-safe`, Git 2.36 scope (OQ-23), a departure from
  the packet's rule that `doctor` refuses old Git, ruling D-B (lane
  openRepoProject-2, 2026-10-08): "The version check runs only when a Git
  repository is about to be inspected; a directory with no `.git` keeps
  `present: false`. `clean` and `overview` refuse with `git-too-old` or
  `git-unavailable`, exit 2, before any probe; under `--json` they print
  `{"error", "code"}`. `status`, `doctor` and `update` never refuse:
  `doctor` reports an old or unusable Git as an error check row and keeps
  its exit semantics for error rows; `status` marks rows it cannot inspect
  `inspection-error`; `update --apply --component tools|workflow` does not
  require Git." Decided by the proposal (ruling D-B): the Git 2.36 item of
  "Baseline behavior changes" in Batch, Overview, and the packet overview
  now carries that text and notes that the baseline `main()` prints a
  `Refused` under `--json` as `{"error"}`, with no `code`. The "Codes"
  bullet above, "exit 2 before any repository probe", now holds for `clean`
  and `overview` only. The quoted timing is `clean`'s: the overview checks
  once before any root is listed (ruling D-AF), as those three items now
  also say.
- `add-project-clean-all-safe`, JSON compatibility (OQ-24), a departure from
  "additive superset" in Batch "Plan envelope" and in finding 4's row above:
  one `schema_version: 1` envelope for every `clean --json`, not only
  `--all-safe`. Decided by the proposal: Batch "Plan envelope" now keeps the
  baseline key names and types, says that `root`, `present`, and
  `ignored_files` change as "Baseline behavior changes" lists, and has plain
  `clean --json` print the same envelope with `mode: "report"`.
- `add-project-clean-all-safe`, the plain report (OQ-29) and its row cap
  (ruling D-V, a lane openRepoProject-3 packet-owner decision accepted by
  lane openRepoProject-2): plain read-only `clean` runs as
  `mode: "report"` under the same deadline, with `completeness` and
  `omitted`, and caps worktree rows at 256 by the same fit test applied to
  its own children, 7 + W + 16 with no removals (about 41.85 s at 256 rows,
  about 80.25 s at 512); the `--all-safe` and single-target plans keep 128
  rows and 16 targets. Decided by the proposal: Batch "User interface and
  selection", "One mutation seam", "Cap arithmetic", "Plan envelope", and
  "Refusal codes".
- `add-project-clean-all-safe`, deadline scope (ruling D-W, a lane
  openRepoProject-3 decision accepted by lane openRepoProject-2): the 60 s
  deadline bounds the inspection children and the batch's removal children
  only; the `push` and `delete-branch` children, run through `execute()`,
  stay without a timeout, as at `a040790`. Decided by the proposal: Batch
  "Deadline and budgets". Batch "Focus and baseline" now also says that at
  `a040790` only `probe()` children have a timeout; ruling D-W withdrew that
  item (C5) as a correction, since "each Git probe" meant those children.
- `add-project-clean-all-safe`, `push` and `remote-gone` (ruling D-D), a
  departure from Batch "One mutation seam", which said `push` and
  `delete-branch` keep their behavior apart from argument resolution: a
  deleted upstream now fills `upstream`, and `push` refuses a `remote-gone`
  branch with refusal reason `remote-gone`, exit 2, instead of republishing
  it; `push` and `delete-branch` refuse with `inspection-incomplete`,
  `inspect-cap`, or `deadline-exceeded`, exit 2, when their re-inspection is
  incomplete, `push` doing so before or after confirmation (change 1 phase 6
  (`90854a3`)). Decided by the proposal: Batch "One mutation seam" and the
  batch-only baseline changes of Batch, Overview, and the packet overview.
- `add-project-clean-all-safe`, the Git child runner (ruling D-G), a
  departure from the bare-name item of "Baseline behavior changes" in Batch
  and Overview (Batch lines 1212-1213 at `da33d92`, ruling D-AC), which said
  the proposal gives `probe()` a timeout argument: Git children run through a
  new bounded runner, `Popen(start_new_session=True)` per child with a
  scrubbed environment and output streamed as bytes, and `probe()` stays for
  non-Git children; abandonable filesystem calls run on daemon threads, never
  on a `concurrent.futures` pool, and `preexec_fn` is never used. Decided by
  the proposal: those two bare-name items; C4 below corrects the rest.
- `add-project-overview`, the repository gate (ruling D-J, amended after
  lane openRepoProject-3's finding L2): the gate also withholds `--all-safe`
  while the repository has an unprobed worktree row, its classification
  null because the 512-row cap or the deadline cut it, because the batch
  plan is then not known to be complete; `target-cap` does not withhold it,
  because the batch preview is complete and lists every row that passes
  every gate before the two index gates. Change 2 council V5 makes
  `target-cap` a limiting gate: with more than 16 gate-passing
  `merged-removable` rows the suggestion stays and its findings carry
  `suggestion_gate: "target-cap"`, the message naming the 16-target limit
  and change 1's drain of 16 per run. The gate still changes suggestions
  only. Decided by the proposal: Overview "Attention categories" and
  "Repository identity and the clean handoff", the synthesis's handoff and
  gate text, the packet overview's goals table and handoff text, and the
  "Overview gates" bullet above.
- `add-project-overview`, the withheld-suggestion reason (ruling D-P), a
  departure from the finding object of Overview "JSON contract": a new field on
  the finding object only, `suggestion_gate`, beside the finding's
  `suggested_command`, carries an existing code (`inspection-incomplete`,
  `inspect-cap`, `scan-limit`, `deadline-exceeded`,
  `target-not-repository-root`, `unsupported-path-bytes`, after change 2 council
  V5 `target-cap`, after lane openRepoProject-2 ruling P6-5 `unstarted-branch`,
  or, after change 2 at `996a181`, `reflog-unavailable`) naming the gate that
  withheld or limited a suggestion;
  after change 2 council V4, `suggestion_gate_rows` carries the worktree-row
  count behind an `inspect-cap` gate, which tells the batch's 128-row band from
  the report's 256-row band, and each code's fixed remedy appears in the
  finding's message and in the human "(withheld: ...)" or "(limited: ...)" text.
  A repository of 129 to 256 worktree rows keeps the plain read-only
  `project clean <root>` suggestion, with `suggestion_gate: "inspect-cap"` only
  on a `merged-removable` finding whose `--all-safe` was withheld; over 256 rows
  every read-only suggestion carries `inspect-cap`, because the report itself
  would be incomplete. Decided by the proposal: Overview "Attention categories"
  names both fields and the remedies, its "Finding object" table and fixture
  list both fields, and the packet overview and the synthesis mention
  `suggestion_gate`.
- `add-project-overview`, findings on the merge-target checkout (ruling
  D-I): on a `protected-default` checkout the `dirty`, `diverged`,
  `unpushed`, and `remote-ahead` findings carry `suggested_command: null`
  and never set the row's suggestion, because `project clean` offers no
  action for that checkout; the last three are the proposal's drift
  findings for that checkout. Change 2 council V1 amends it: on that
  checkout the overview emits every applicable finding, not a first match,
  `dirty` plus one of `diverged`, `unpushed`, or `remote-ahead`, and two
  more preserve warnings with `suggested_command: null`, `unpublished` when
  no upstream is configured ("merge-target branch has no upstream; local
  commits are unverified") and `remote-gone` when the upstream is gone.
  Decided by the proposal, as a deliberate narrowing of the attention
  table's per-code suggestions: Overview "Attention categories".
- `add-project-overview`, manifest refusals: a `Refused` from `manifest()`,
  for an unreadable or a wrong-kind manifest, is a `manifest-invalid` row
  error with exit 1 in the overview; the `project-review-safety` exit 2 for
  an undecodable manifest applies to `clean`, not to an overview row.
  Decided by the proposal: Overview "Collector boundary and error
  isolation" and **One helper failure is isolated.**
- `add-project-overview`, the shared model (ruling D-M): the overview reads
  the shared evidence model through change 1's canonical `project-command`
  requirement and states its own 60 s deadline. No packet sentence changes.
  Change 1 council V10, which amends rulings D-B and D-M, withdrew the 5 s
  per Git child they gave `status`, `doctor`, and `update`, which keep 15 s;
  the timeout items of "Baseline behavior changes" say so.
- Both changes, measurement (ruling D-Q): the caps stay provisional in the
  spec deltas, and `tasks.md` carries a warm- and cold-cache measurement on
  a Linux file-system path, never `/mnt/c`, before the Speckit handoff.
- `add-project-clean-all-safe`, `update --apply` (ruling D-R): it refuses
  unless the root's and every child's `dirty` is exactly `false`.
- `add-project-clean-all-safe`, `doctor` and `status` on unknown state
  (ruling D-S, narrowed by lane openRepoProject-2 on 2026-10-08): they
  report a failed status probe instead of exiting 2, and `doctor` renders as
  an error check row only a null that means "not established" (a `present`
  null, a `dirty` null left by a failed probe, any row classified
  `inspection-error`), never a null that means "none" (`upstream`, `ahead`,
  and `behind` for a branch with no upstream; `merged_into_target` for a
  detached head). The overview's inherited rule is the same. The proposal
  lists this as a baseline behavior change. Change 1's phase 6 (`90854a3`) gives
  the mark that `status` and `doctor` set the shape
  `classification: "inspection-error"` with `errors` beside it, on the root and
  leg dicts.
- `add-project-clean-all-safe`, the packet's remaining open items
  (verification finding H1), each a proposal decision open to ratification,
  numbered in lane openRepoProject-2's list: OQ-8, no configurable limit,
  the fixed values reported in `limits` and `budget`; OQ-10 (ruling D-C),
  `--apply --json` accepted for `--all-safe` and `--action remove` only;
  OQ-11, `--expect-plan` optional with `--yes`; OQ-12, a relative path or no
  argument resolving to the repository Git finds there; OQ-13, a sparse
  skip-worktree entry staying `hidden-local-state`; OQ-14, a never-populated
  gitlink staying `contains-submodule`; OQ-26, `--all-safe` and
  `--expect-plan` kept; OQ-27, one separate change per extension; and
  OQ-28, the ladder made a pure function over evidence. Decided by the
  proposal: Batch "User interface and selection" (OQ-10), Overview "Merge
  target and classification reuse" (OQ-28), "Open proposal decisions"
  above, and the open lists of Batch, the packet overview, and the
  synthesis, which keep only the open entries.
- `add-project-overview`, the packet's remaining open items (verification
  finding H1), each a proposal decision open to ratification: OQ-6, four
  concurrent children across distinct repositories, with the serial
  fallback of 32 candidates and 128 worktree rows if design rejects
  concurrency; OQ-7, no per-repository row cap, so a repository with more
  than about 355 worktree rows ends at the deadline, visibly incomplete;
  OQ-8, no configurable limit; OQ-17, no `attention` alias; OQ-18, the full
  envelope under `--attention --json`, consumers filtering on
  `findings[].category`; OQ-19, the extra `dirty` finding on a dirty
  merge-target checkout kept; OQ-26, the spelling
  `project overview [--root D]... [--attention] [--json] [--strict]`; and
  OQ-27, one separate change per extension. Decided by the proposal: "Open
  proposal decisions" above and the open lists of Overview, the packet
  overview, and the synthesis, which keep only the open entries.

### Corrections and review constraints — 2026-10-08

The proposals' alignment reviews and lane openRepoProject-3's fidelity reads
also found errors and omissions in the packet's account of `a040790`, and
limits on how the design can be built and tested. Each correction was
checked against `project` at `a040790`, and the packet text now carries it.

- Baseline (C1): `origin/main` was `da33d92`, which merged PR #7 on
  2026-10-07, so the `origin/main` commit the packet named was stale and
  PR #7 is merged, not open. It has since moved to `d7f6b0e` (PR #8,
  feature 002, 2026-10-08) and then to `7a9134b` (PR #13, `openspec/`
  only); every `project` line citation stays pinned at `a040790`, whose
  `project` is byte-identical through `da33d92` (change 1 council V12), as
  the baseline sentence above says. The cleanup-branch commit lists of the
  packet overview and both feature documents now name all six harvest
  commits: `5fc2b51`, `acf0133`, `80fdef3`, `1789ad9`, `09af8c8`, and
  `bb91a49`.
- Doctor health follow-up (M2 of the PR #12 fidelity read): the follow-up
  to absorb `acf0133` and `80fdef3` is discharged by `add-project-overview`
  (issue #10, PR #12), which absorbs them as local-only read-only
  reporting; "Current state" above and the packet overview say so, and the
  overview design does not absorb them itself.
- `remote-gone` (C3): at `a040790` doctor never classifies a deleted
  upstream. Its `check_rows` reports no classification, and its only
  worktree classification is `repo_state`'s `stale-worktree` (`project`
  line 352), which `snapshot` embeds (line 681) and `print_report` prints
  under `--json` (lines 762-763). Overview and clean classify a deleted
  upstream `remote-gone`; doctor reads the same evidence but never
  classifies it.
- Child processes (C4): `Popen(process_group=0)` needs Python 3.11, and the
  project's floor is 3.10, so children start with `start_new_session=True`,
  which also gives each child its own process group, and never with
  `preexec_fn`; filesystem calls run on daemon threads abandoned on timeout,
  never on a `concurrent.futures` pool, whose abandoned thread would block
  interpreter exit.
- Failed status probe on the merge-target checkout (C6), ruling D-A: "A
  failed, timed-out or deadline-cut status probe sets the row to
  `inspection-error` directly, on the merge-target branch too, with that
  code's repair finding of severity error." The baseline ladder tests the
  merge-target branch after presence but before cleanliness (`project`
  lines 418-427) and would read such a row as `protected-default`. Overview
  "Repositories and linked worktrees" and "Merge target and classification
  reuse" and Batch "Worktree-specific probes" now state the case, so the
  passages that assume `inspection-error` stand.
- Failed root status (M4, ruling D-N): at `a040790` a failed `git status` in
  the repository root makes `repo_state` raise `Refused`, ending `clean`,
  `status`, `doctor`, and `update` with exit 2; under the shared probes it
  is a row-level `inspection-error` for the main worktree. The shared
  baseline lists of the packet overview and both feature documents now
  carry it.
- Merge-target strips (ruling D-T): Batch "Eligibility and merge-target
  terminology" now names both `origin/` strips, on the manifest's
  `tracking_branch` and on the `origin/HEAD` symref, as the baseline
  `default_branch` and Overview "Merge target and classification reuse" do.
- Git 2.36 floor (C12): every Git behavior the batch design cites, the
  `ls-files -v --stage -z` combination, the scrubbed variable list, and the
  removal refusals among them, was verified on Git 2.43 only. The proposal
  must verify on a pinned Git 2.36 or raise the floor, as Batch
  "Repository-wide probes" now says.
- Platform-bound scenarios (C13): the non-UTF-8 path scenarios, the
  overview's **Gated merged worktrees.** and **Non-UTF-8 path.** among
  them, cannot be built on macOS APFS; raw-byte order differs from
  `core.ignoreCase` order on case-insensitive APFS; and WSL2 `/mnt/c` does
  not guarantee stable inode numbers. Those scenarios are Linux-only and
  skipped elsewhere with a reason.
- Pasting the escaped path form (C17): the human `$'…'` form needs bash
  4.2 or newer for `\u`; the stock bash 3.2 of macOS lacks it. Both feature
  documents say so beside their path rules.

### Council rulings recorded — 2026-10-08

The councils of both proposals (lane openRepoProject-2, 2026-10-08) ruled on
the proposals' reviews. Each bullet names the change and ruling, quotes the
mechanism closely, and names the packet passages that now carry it. The
council's own departure labels are kept, and a departure is open to Brett
Heap's ratification. Change 1's post-council commit is `0669a20`: the
council verdicts were applied at `ea9c73b`, followed by clarifications, the
merge of `7a9134b`, and a restatement. The writer adjustments made with the
verdicts, which lane openRepoProject-2 accepted, are recorded with the
ruling each refines, and so are lane openRepoProject-2's rulings of
2026-10-09 for change 1's phase 6, which settled the items lane
openRepoProject-3 raised in its delta read of change 1 at those commits.

Change 1, `add-project-clean-all-safe`:

- Change 1 council V1, the removal child, a departure, open to Brett Heap's
  ratification, from Batch "Interruption and expiry", where SIGINT or expiry
  terminated and reaped the removal child's process group, and from this
  record's own finding 2 row (line 208 at `da33d92`), "SIGINT or expiry
  terminates and reaps the child's process group": "Once the removal child is
  spawned, `project` does not signal it: SIGINT, SIGTERM, SIGHUP and the work
  deadline are deferred until it exits; the deadline gates only the start of a
  removal ... and never its completion; a separate hard ceiling (300 s, for a
  hung mount) ends the wait by killing the group and recording the target
  `unknown` with a `partially-removed` note and recovery text". The writer
  adjustment gives that outcome the reason code `removal-ceiling`, which both
  the `removed` and `unknown` rows of Batch's stage table now list, the
  `unknown` row beside the note. Lane openRepoProject-2 ruling M1 (2026-10-09,
  confirmed 2026-10-09; change 1's text at `0669a20` said always `unknown`,
  corrected in its phase 6 at `90854a3`) states one rule for a signal and for
  the ceiling: the rescan decides the stage, `removed` when the registry entry
  and the path are both gone, and `unknown` with the `partially-removed` note
  when either remains, a target in flight at a signal included, with
  `removal-ceiling` naming the cause in both cases after a ceiling kill; after a
  signal the run exits per the 130 row (130, 143, or 129). Lane
  openRepoProject-2 confirmed on 2026-10-09 lane openRepoProject-3's reading of
  M1 with the `failed` rule: a removal child that exits nonzero on its own, with
  or without a signal having reached `project`, is `failed` with Git's own
  status as before (`git-refused` for 128, `git-failed` otherwise), and the
  rescan decides between `removed` and `unknown` with `partially-removed` only
  for a child that `project` killed at the 300 s ceiling or whose exit could not
  be observed, `removal-ceiling` naming the ceiling cause; so a target in flight
  at a signal is decided by the rescan only when its exit could not be observed,
  and change 1's phase 6 (`90854a3`) makes a `removed` target with
  `removal-ceiling` exit 1, which stops the batch. A run, not counting time
  blocked at the confirmation question (ruling R-11), is therefore bounded at
  64 s, the 50 s of work, the 10 s reserve, and up to 4 s of termination
  (SIGTERM, a 2 s grace, SIGKILL, and a reap wait of up to 2 s), plus up to
  300 s for a removal in flight, after whose exit the reserve counts; both
  changes use the same runner (lane openRepoProject-2, 2026-10-09). The
  report's ladder text for a registered row whose only working changes are
  deletions of tracked files carries the partial-removal note beside, never
  instead of, the dirty classification, and probe children are still terminated.
  The adversary's fixture was an 18,333-file half-deletion from a TERM at
  0.25 s. Batch "One mutation seam", "Deadline and budgets", which now bounds a
  run at 64 s plus up to 300 s for a removal in flight, "Interruption
  and expiry", "Stages and reconciliation", "Exit codes", and "Partial
  completion and recovery", the **Deadline expiry mid-batch.**,
  **Hard ceiling.**, and **SIGINT.** scenarios, the synthesis's seam, stop rule,
  and exit list, the packet overview's scope, and finding 2's row above carry
  it.
- Change 1 council V2, a new gate, `unstarted-branch`: "a row is excluded when
  its branch has no commit of its own: its head equals the merge-target SHA, or
  its head is an ancestor of the target and the branch's creation reflog entry
  shows no commit since creation; a missing reflog fails closed (excluded,
  reason stated)". The verdict does not place it in the gate order; the writer
  adjustment places it after `not-requested` and before `deferred-target-cap`,
  and the packet's gate order follows. Change 1's phase 6 (`90854a3`) puts
  `reflog-unavailable` at the same position in the gate order and the reason
  list. The gate's evidence, the branch's creation reflog entry, was missing
  from change 1's fit test, and lane openRepoProject-3 asked for a bounded read
  or one child counted in F; lane openRepoProject-2 ruling M3 (2026-10-09) makes
  it one bounded filesystem read, never a Git child, so the fit test is
  unchanged, and rules that "an expired or missing reflog fails closed with its
  own reason" (`reflog-unavailable` at change 1's `ba9f7c3`), OQ-4 counting the
  rows so excluded. The gate applies to single-target `remove` too: a fresh
  merged worktree named with `--worktree` is refused where `a040790` removes it,
  a listed baseline change. Batch "Eligibility and merge-target terminology"
  (the list, the gate order, the reason enum, and the reflog read), "Cap
  arithmetic", its batch-only baseline change (at `a040790` such a row
  classifies `merged-removable`, and `--worktree` removes it), the **Unstarted
  branch.** scenario, the packet overview's baseline list, and the exclusion
  mentions in Overview "Attention categories", the synthesis, the packet
  overview, and the "Overview gates" bullet above carry it. The ruling adds the
  second question for Brett Heap, on squash merges, to the open lists. The D10
  amendment (landed in change 1 at `0b3c33d`, lane openRepoProject-2 D10,
  2026-10-09) replaces the verdict's "head equals the merge-target SHA, or ..."
  test: the gate reads the reflog in every case, and lane openRepoProject-2
  ruling R-12 (2026-10-09; change 1 at `4f2162b`) states the test as a movement
  after an anchor, the last surviving `branch: Created from` or
  `branch: Reset to` entry, or, under ruling R-15, an entry whose old object is
  all zeros, so a head at the merge-target SHA with a movement recorded is
  merged, the fast-forward case, and a reflog that cannot decide is
  `reflog-unavailable`. The overview mirrors the read (change 2, read at
  `996a181`, final `4495ae7`): a merged row whose reflog cannot decide keeps its
  `merged-removable` finding with only the read-only suggestion and
  `suggestion_gate: "reflog-unavailable"`. Batch "Eligibility and merge-target
  terminology" and its batch-only baseline change, Overview "Attention
  categories" and "Repository identity and the clean handoff", the synthesis's
  handoff and gate text, the packet overview's handoff text and batch-only list,
  and the "Overview gates" bullet above carry it.
- Change 1 council V3, configuration pins: "Every status probe and the
  removal child carry `-c core.untrackedCache=false -c core.fsmonitor=false`
  beside the `status.showUntrackedFiles` pin"; the last-defense sentence
  names the pinned configuration, and `-c` covers `GIT_CONFIG_GLOBAL` and
  `GIT_CONFIG_SYSTEM` where the environment scrub does not. In the
  adversary's fixture, with the untracked cache on, `core.checkStat=minimal`,
  and an index-writing status already run, Git's own pre-removal check
  deleted an untracked file with exit 0. Every spelling of the removal
  command and of the combined status probe in the five documents now carries
  the pins, finding 1's row and the "Removal command" and "Shared probes"
  bullets above included; the one exception, which says so, is the snapshot
  command of Overview's zero-mutation check, a test-harness command and not
  a probe. Batch gains the **Untracked cache.** scenario, and the overview's
  two fsmonitor-held fixtures are marked for feature 005 to rewrite with an
  injected slow `git`.
- Change 1 council V4, single-target `remove`, a departure, open to Brett Heap's
  ratification, from the packet's strict one-item batch, under which "an
  inspection error anywhere in the repository makes its plan incomplete and
  refuses it too": Batch lines 188-192 (its preserve paragraph), 419-420 ("One
  mutation seam"), 1268-1272 (its single-target baseline change), and 1562-1563
  (the scenario **Single target equals a one-item batch.**) at `da33d92`, and
  this record's own finding 2 row (line 208 at `da33d92`) and "One mutation
  seam" bullet (lines 247-249 at `da33d92`). The ruling: "completeness is the
  repository-wide evidence plus P's own row; other rows' `inspection-error`,
  `inspect-cap` and unprobed states are recorded as non-blocking omissions in
  the plan; P's own revalidation stays fully strict; the named target is probed
  first so the 128-row cap never omits it", the 16-target cap counts P alone,
  and every remaining refusal names a manual remedy. Batch "Eligibility and
  merge-target terminology", "One mutation seam", "Inspection order and omitted
  work", its baseline change, and that scenario, the synthesis, the packet
  overview, Overview's batch-only item, finding 2's row, and the "One mutation
  seam" bullet above carry it.
- Change 1 council V5, the deferred target cap, a departure from Batch "User
  interface and selection" and the packet's `target-cap` refusal, open to Brett
  Heap's ratification: "When more than 16 rows pass the pre-index gates, the
  plan selects the first 16 in canonical order, lists the rest as excluded
  `deferred-target-cap` with the next command, and apply is allowed; re-running
  drains the backlog 16 at a time"; the `target-cap` refusal is retired, and the
  code survives only as the overview's limiting gate reason, "limited to 16 per
  run; re-run to drain". An estate survey, about 20 eligible rows in one
  repository, grounds it. The writer adjustment adds the caveat: a selected row
  that an index gate (`hidden-local-state` or `contains-submodule`) then
  excludes still took one of the 16 places, so a run may remove fewer than 16
  and the deferred rows wait for the next run; if 16 such rows lead the
  canonical order, they stop the batch until they are handled by hand (change 1
  at `0669a20`). Batch "User interface and selection", "Eligibility and
  merge-target terminology", "Worktree-specific probes", "Cap arithmetic" (the
  fit test is per run), "Exit codes", "Refusal codes", and the **Target cap.**
  scenario, the synthesis, the packet overview, and Overview "Attention
  categories" carry it.
- Change 1 council V6, honest scope, recorded as evidence for the
  cache-disposal follow-on, not as a change: the batch removes only
  worktrees with no ignored files, so caches such as `__pycache__` keep a
  worktree out until the cache-disposal change; in one surveyed repository
  20 of 29 merged worktrees were excluded for caches alone. Batch "Deferred
  cache and paired-retirement extension" and the packet overview carry it.
- Change 1 council V7, the interim `remote-gone` text: until Brett Heap rules on
  the ancestry question, a `remote-gone` row whose `merged_into_target` is true
  reads "Merged locally, upstream deleted: not removable by `project` until the
  open question is ruled; review, then `git worktree remove` yourself", and the
  question carries the measured numbers: 4 of about 90 merged worktrees,
  `fetch.prune` unset everywhere, and auto-delete on 2 of 21 repositories. The
  question in the open lists of Batch, Overview, the packet overview, and this
  record carries both. Brett Heap ruled the question on 2026-10-09, and the text
  stays in the proposals until lane openRepoProject-2 amends it, sha to follow
  (see "Rulings R-11 to R-20 and Brett Heap's ruling — 2026-10-09").
- Change 1 council V8, what the person sees: the preview lists the selected
  rows, then the excluded rows grouped by reason with each next step; the
  apply prompt names the count; and the success line and the stop block
  name what was removed, what was kept, and the next command. The
  proposal's writer had also accepted `y` beside `yes` ("[y/N]"), which
  lane openRepoProject-3 flagged as unlabeled against Batch lines 354 and
  1009 at `da33d92` (the apply phase begins when the prompt is answered
  `yes`, and anything else is `cancelled`) and against the `project-command`
  specification's `yes` confirmation for `new`. Lane openRepoProject-2's
  ruling of 2026-10-09 accepts `yes` only, for `clean`'s removal apply, and
  withdraws "[y/N]", so the packet's `yes` rule stands unchanged and no
  packet sentence changes.
- Change 1 council V9, evidence-model details: a probe stopped by `project`
  at its record bound is a complete outcome, never `probe-failed`; after
  SIGKILL the reap waits at most the 2 s grace, then the child is abandoned
  and the row recorded `probe-timeout`; every exit path terminates the
  process groups it started; and standard error is drained and capped.
  Batch "Interruption and expiry" and "Bounded ignored-file inspection" and
  Overview "Deadline and timeouts", which said a child "is always reaped",
  now say so. Lane openRepoProject-2 ruling M7 (2026-10-09) states that
  termination rule in change 1's own requirement instead of citing an
  overview requirement that did not yet exist.
- Change 1 council V10, the per-child budget, a departure, open to Brett Heap's
  ratification, from the packet's shared baseline item that the per-probe
  timeout drops from 15 s to 5 s (the timeout item of "Baseline behavior
  changes" in Batch, Overview, and the packet overview, the last at lines
  228-230 at `da33d92`): `status`, `doctor`, and `update` keep 15 s per Git
  child, having no deadline, and `min(5 s, work_remaining)` applies only under
  `clean`'s and the overview's deadlines; the 5 s that rulings D-B and D-M gave
  those three commands is withdrawn. Lane openRepoProject-2's ruling of
  2026-10-09 cites the packet overview's lines too. Those three items carry it.
- Change 1 council V12, the moved baseline: `origin/main` was then `d7f6b0e`,
  where PR #8 (feature 002, merged 2026-10-08) added about 141 lines to
  `project`, in the project-creation code between `choose()` and the end of
  `new()`, and 1,163 lines to `tests/test_project.py`. The cleanup, status,
  doctor, and update paths are unchanged in content but sit about 141 lines
  lower, so every `project` line citation stays pinned at `a040790`, whose
  `project` is byte-identical through `da33d92`. `origin/main` has since moved
  to `7a9134b`, PR #13, which touched `openspec/` only. "Focus and baseline" of
  Batch and Overview, the packet overview's baseline paragraph, and this
  record's baseline sentence say so.
- Change 1 council X2, raised by change 2's council: Git-first resolution
  supports a gitfile main checkout. When the first registry record's path
  equals `common_dir`, the main worktree is the realpath of `core.worktree`,
  and a command root equal to it resolves; a submodule checkout, whose first
  record lies under `.git/modules`, is refused with
  `target-not-repository-root`, a listed baseline change (at `a040790`
  `clean` handles both with exit 0). The writer adjustment R11 completes it:
  Git 2.43 leaves `core.worktree` unset after `git init --separate-git-dir`,
  so the main worktree is then the candidate toplevel whose `.git` file
  names `common_dir`, and a linked worktree of such a repository is refused
  with `target-not-repository-root`. The precedence, which lane
  openRepoProject-3 raised and lane openRepoProject-2's ruling of 2026-10-09
  settles, is the submodule test first, a non-empty
  `git rev-parse --show-superproject-working-tree`, then `core.worktree`,
  then the candidate toplevel. Batch "Command directory and repository
  resolution", its baseline list, and the scenario
  **Gitfile main checkout and submodule checkout.**, the synthesis, the
  packet overview's batch-only list, and the "Probe directory rule" bullet
  above carry it.

Change 2, `add-project-overview`:

- Change 2 council V1, amending ruling D-I: "On a `protected-default`
  checkout the overview emits every applicable finding, not a first match:
  `dirty` plus one of `diverged`, `unpushed`, `remote-ahead`; and two new
  cases, both preserve, warning, `suggested_command: null`": no upstream
  configured reuses `unpublished`, with the message "merge-target branch has
  no upstream; local commits are unverified", and an upstream that is gone
  reuses `remote-gone`. Overview "Attention categories" and the ruling D-I
  bullet above carry it.
- Change 2 council V2, a gitfile main checkout and a missing main worktree:
  when the first registry record's path equals `common_dir`,
  `repository.root` is the realpath of `core.worktree`, else the
  `--show-toplevel` of a candidate that is that checkout, else null with an
  `unsupported-layout` repair finding and no suggestion, and that record is
  never a status-probe row; a nonexistent main-worktree path gives
  `repository.root: null` with a `main-worktree-missing` repair finding, and
  the repository-wide probes run in the candidate; "reached first" means
  canonical candidate order. With `core.worktree` unset, as change 1's R11
  finds after `git init --separate-git-dir`, the second case names the root
  when the main checkout is a candidate, and the third applies otherwise.
  `main-worktree-missing` is a warning; `unsupported-layout` was a warning at
  change 2's `a8cef41`, and lane openRepoProject-2 ruling N-6, confirmed as
  P6-6 (2026-10-09), makes it an error, as lane openRepoProject-3
  recommended.
  Overview "Repositories and linked worktrees", "Worktree-specific probes",
  and "Attention categories", the synthesis, the packet overview's "reached
  first" clause, and the "Probe directory rule" bullet above carry it.
- Change 2 council V4, the `suggestion_gate` code set: each code has a fixed
  remedy in the finding's message and in the human "(withheld: ...)" or
  "(limited: ...)" text; `inspect-cap` tells the batch's 128-row band from
  the report's 256-row band, and the JSON finding carries the row count, in
  `suggestion_gate_rows`. Overview "Attention categories" and its finding
  object carry it, folded into the ruling D-P bullet above.
- Change 2 council V5, amending ruling D-J: `target-cap` is a limiting
  gate; with more than 16 gate-passing `merged-removable` rows the
  `--all-safe` suggestion stays and `suggestion_gate: target-cap` is set,
  the message naming the 16-target limit and that the preview is complete,
  after change 1's V5 "limited to 16 per run; re-run to drain the backlog".
  Overview "Attention categories", the synthesis, the packet overview, and
  the ruling D-J bullet above carry it.
- Change 2 council V6, scoping the determinism clause to "a run in which no
  child, task or root listing reaches its budget and the deadline does not
  expire"; a cut run reports each cut unit with `omitted` and the exactness
  of Overview "Ordering, truncation, and omitted counts". The packet keeps
  its rank condition and adds the barrier as a further condition: a
  repository's second phase starts only after every candidate earlier in
  canonical order has finished its identity probe and every repository
  ranked earlier has finished its first phase. Lane openRepoProject-3 asked
  change 2 to state both. Overview "Scheduling and concurrency" and the
  synthesis carry it.
- Change 2 council V7, bounded filesystem calls: every filesystem call the
  overview makes, root canonicalization and deduplication, marker and
  holder checks, and manifest reads included, runs in a bounded daemon task
  with `min(5, deadline - now)`; the main thread never blocks in an
  unbounded filesystem call; and a manifest larger than 1 MiB is
  `manifest-invalid`, by `st_size` before it is read (lane openRepoProject-2
  ruling R-4, 2026-10-09). Change 1 at `0669a20` places that cap in the shared
  evidence model, limited to the merge-target manifest read, so it applies
  to that read in both commands and `clean` and the overview resolve the
  same merge target: `clean` refuses with exit 2, and the overview records a
  row error. Overview "Deadline and timeouts" and "Collector boundary and
  error isolation" and the shared "Baseline behavior changes" lists of
  Batch, Overview, and the packet overview carry it.
- Change 2 council V9, identity: the registration rule is change 1's
  (relative values resolved, realpaths compared), and where a bind mount
  gives two root spellings for one `(dev, ino)`, the canonical-first one
  wins. Overview "Repositories and linked worktrees" carries it.
- Change 2 council V11, the interim `remote-gone` message: until Brett Heap
  rules, a `remote-gone` finding's message states whether the worktree's branch
  tip is already an ancestor of the merge target when the overview's evidence
  establishes it, spawning no extra probe, and its suggestion only reviews. The
  ancestry question in the open lists carries it. Brett Heap ruled on
  2026-10-09, and the message is lane openRepoProject-2's to amend, sha to
  follow.

### Change 2 phase 6 records — 2026-10-09

Change 2's phase 6 (PR #12 head `5094e4e`) and lane openRepoProject-2's rulings
for that round, both of 2026-10-09, settled the items below. Each is recorded at
its passage as "change 2 phase 6 (5094e4e), lane openRepoProject-2, 2026-10-09"
or under its ruling label.

- The overview's `unstarted-branch` gate (rulings N-5 and P6-5): a worktree
  whose head equals the merge-target SHA keeps its `merged-removable` finding
  with only the read-only suggestion and `suggestion_gate: "unstarted-branch"`
  and a fixed remedy, which lane openRepoProject-2 rulings R-12 M6 and R-14 M-B
  (2026-10-09) make "no commit was made on this branch here since it was
  created; review, then git worktree remove yourself" in both changes,
  superseding the phase 6 wording and ruling R-10; the reflog-based part stays a
  residual exclusion the batch applies. Overview "Attention categories" carries
  it, where the packet had said such a worktree counts as `merged-removable`,
  and the ruling D-P bullet above adds the code. The D10 amendment, landed in
  change 1 at `0b3c33d`, replaces the head test and retires the residual part:
  the overview mirrors the batch's reflog read (change 2, read at `996a181`,
  final `4495ae7`), as the change 1 council V2 bullet above records.
- `main-worktree-missing` replaces the `stale-worktree` finding on the main
  worktree's row. Overview "Repositories and linked worktrees" carries it.
- `unsupported-layout` is severity error (ruling N-6, confirmed as P6-6),
  where change 2 at `a8cef41` had warning; `main-worktree-missing` stays a
  warning. Overview's finding table and the change 2 council V2 bullet
  above carry it.
- The bound of the **Invocation deadline.** scenario is 64 s, not 62 s:
  after SIGTERM a child gets 2 s before SIGKILL, and the reap then waits the
  2 s grace. That scenario and Overview "Deadline and timeouts" carry it.
- `scan_errors` are in canonical collection order, not occurrence order, so
  the result does not depend on timing and the promise of Overview
  "Scheduling and concurrency" holds. Overview's envelope table carries it.
  Row-level `errors` stay in probe order, which is fixed; only `scan_errors` and
  the collection order are canonical (lane openRepoProject-2, 2026-10-09), as
  Overview's project-row table now says where the packet had said occurrence
  order.
- `probes.estimated` adds a gitfile main checkout's layout children, at most 2.
  Change 2 at `996a181` corrects it to at most one, the `core.worktree` read,
  beyond the identity probe, because lane openRepoProject-2 ruling R-2 moved the
  submodule test into the identity probe; the identity probe and the
  per-worktree status probes remain Git children. Overview "Probe accounting"
  carries it.
- The overview's submodule outcome (lane openRepoProject-2 ruling R-2, change 2
  at `996a181`): a submodule checkout gets `repository.root: null` with an
  `unsupported-layout` error, the message "submodule checkout, which project
  clean refuses; review it yourself", and no gate code, and
  `target-not-repository-root` now covers only a bare repository, where
  `5094e4e` also gave it to a submodule checkout. Overview "Repositories and
  linked worktrees" and the "Probe directory rule" bullet above carry it.
- Change 2's fix round (lane openRepoProject-2 rulings R-13 (b), R-14, the R-12
  mirror, and R-15, 2026-10-09) landed at `fa9f0be`: it mirrors R-12's
  anchor-based reflog test with R-15's all-zeros anchor and adopts the R-12,
  R-14, and R-15 remedy texts; `ef288fe` adds ruling R-16, `fd4b05a` ruling
  R-18, `568c477` copies change 1's movement wording, and `4495ae7`, change 2's
  final text, adds ruling R-20. "Rulings R-11 to R-20 and Brett Heap's ruling
  — 2026-10-09" below records their items.
- Change 2's final text is `4495ae7`: read at `996a181`, fix round at `fa9f0be`,
  R-16 at `ef288fe`, R-18 at `fd4b05a` and `568c477`, and R-20 at `4495ae7`;
  lane openRepoProject-3 read `568c477` clean on 2026-10-09, lane
  openRepoProject-2 landed that read's two LOW findings as ruling R-20, and
  PR #12 was marked ready for review at `4495ae7` the same day, ratification
  remaining Brett Heap's, as "Rulings R-11 to R-20 and Brett Heap's ruling —
  2026-10-09" below records.

### Change 1 phase 6 records — 2026-10-09

Change 1's phase 6 (PR #11 head `90854a3`) and lane openRepoProject-2's
confirmations and rulings for that round, all of 2026-10-09, settled the items
below. Each is recorded at its passage as "change 1 phase 6 (`90854a3`), lane
openRepoProject-2, 2026-10-09", under its ruling label, or, for change 2's
reconciliation, as landed in change 2 at `996a181`. Change 1's phase 6 text
ended at `0b3c33d`, after `9ea2f02`, where the D10 amendment landed and where
lane openRepoProject-3 made its re-verification read; "Rulings R-11 to R-20 and
Brett Heap's ruling — 2026-10-09" below records the fix round at `d6aaa9a`,
the wordings at `6792e06`, ruling R-15 at `9eeac52`, ruling R-17 at `4f2162b`,
ruling R-19 at `7e2589f`, and change 1's final text at `8973762`, which adds
ruling R-20.

- Ruling M1 confirmed: lane openRepoProject-3's reading stands. A removal child
  that exits nonzero on its own, with or without a signal, is `failed` with
  Git's own status, and the rescan decides between `removed` and `unknown` with
  `partially-removed` only for a child that `project` killed at the ceiling or
  whose exit could not be observed, `removal-ceiling` naming the cause. The
  `removed` row of Batch's stage table now says "or its exit could not be
  observed" where it said "or was still running at a signal". Batch
  "Interruption and expiry" and "Stages and reconciliation", the packet
  overview's scope, the synthesis's seam, finding 2's row, and the change 1
  council V1 bullet above carry it, without the "pending confirmation" wording.
- The run bound (lane openRepoProject-2, 2026-10-09): a run is bounded at 64 s,
  not counting time blocked at the confirmation question (ruling R-11, recorded
  below), the 50 s of work, the 10 s reserve, and up to 4 s of termination
  (SIGTERM, a 2 s grace, SIGKILL, and a reap wait of up to 2 s), plus up to
  300 s for a removal in flight; both changes use the same runner, and the
  overview's 64 s stands. Batch "Deadline and budgets", where the packet had
  said "no longer bounded at about 60 s" and "plus the 2 s reaping grace",
  finding 2's row, and the change 1 council V1 bullet above carry it.
- Row-level `errors` stay in probe order, which is fixed; only `scan_errors` and
  the collection order are canonical (lane openRepoProject-2, 2026-10-09).
  Overview's project-row table, which had said occurrence order, and the
  `scan_errors` bullet of "Change 2 phase 6 records — 2026-10-09" above carry
  it.
- A `removed` target with reason `removal-ceiling` exits 1 and, not being a
  plain `removed`, stops the batch; the work deadline has passed by then in any
  case. Batch "One mutation seam", "Interruption and expiry", "Stages and
  reconciliation", "Exit codes", "Partial completion and recovery", and the
  **Hard ceiling.** scenario, the synthesis's stop rule and exit list, the
  packet overview's scope, and finding 2's row carry it.
- `push` refuses an incomplete re-inspection, with `inspection-incomplete`,
  `inspect-cap`, or `deadline-exceeded` and exit 2, before or after
  confirmation. Batch "One mutation seam" and its batch-only baseline item, the
  packet overview's batch-only list, and the ruling D-D bullet above carry it.
- The mark that `status` and `doctor` set on a row they cannot inspect is
  `classification: "inspection-error"` with `errors` beside it, on the root and
  leg dicts. The Git 2.36 items of "Baseline behavior changes" in Batch,
  Overview, and the packet overview carry it after ruling D-B's quoted text,
  which stays verbatim, and so does the ruling D-S bullet above.
- `removal_ceiling_seconds: 300` joins the batch `budget`. Batch "Deadline and
  budgets", its plan envelope's `budget` row and the plan fixture's `budget`
  object, the synthesis's bounds row, and the "Removal floor" bullet above carry
  it; the fixture's `plan_digest` is unchanged, because the digest does not
  cover `budget`.
- `reflog-unavailable` sits at the `unstarted-branch` position in the gate order
  and the reason list. Batch "Eligibility and merge-target terminology" (the
  list and the gate order), the batch-only baseline items of Batch and the
  packet overview, and the change 1 council V2 bullet above carry it.
- A merged worktree whose reflog keeps no decisive entry, as after 90 days
  without activity under the default `gc.reflogExpire`, is refused in
  single-target mode as `target-excluded` with reason `reflog-unavailable`,
  where `a040790` removes it; change 1 at `0b3c33d` lists it as a fourth
  user-visible change, worded so at `4f2162b`. The batch-only baseline items of
  Batch, Overview, and the packet overview carry it beside the
  `unstarted-branch` single-target item, and Batch "Eligibility and merge-target
  terminology" names it.
- The D10 amendment (landed in change 1 at `0b3c33d`, lane openRepoProject-2
  D10): the `unstarted-branch` gate reads the branch's reflog in every case, so
  a head at the merge-target SHA with a commit recorded is merged, the
  fast-forward case, a missing reflog is `reflog-unavailable`, and the overview
  mirrors the same read. It replaces council V2's "head equals the merge-target
  SHA, or ..." test and the residual reflog part of rulings N-5 and P6-5. Ruling
  R-12, recorded below, states its test as a movement after an anchor, where the
  amendment had tested for a commit since the branch's creation. The overview's
  outcome is recorded at change 2's `996a181` and stated at `fa9f0be`: a merged
  row whose reflog is missing, empty (0 bytes), or read to its 64 KiB bound, or
  whose surviving entries cannot decide, keeps its `merged-removable` finding,
  which suggests only the read-only form with
  `suggestion_gate: "reflog-unavailable"` and no `--all-safe` form; the finding
  code stays `merged-removable`, `reflog-unavailable` being only the gate value;
  the overview reads the reflog itself, at most 64 KiB, within its filesystem
  budget (its requirement 3), with no Git child; and `project clean --all-safe`
  excludes the same rows as `reflog-unavailable`. Its remedy is "the branch's
  reflog is missing, expired or undecidable; review, then git worktree remove
  yourself" (rulings R-12 M6, R-14 M-B, and R-15). This closes the gap that the
  earlier rounds of this revision left open for that outcome. Batch "Eligibility
  and merge-target terminology", Overview "Attention categories" (its gate text
  and `suggestion_gate` code set) and "Repository identity and the clean
  handoff", the synthesis's handoff and gate text, the packet overview's handoff
  text, the "Overview gates" and ruling D-P bullets, and the change 1 council V2
  and change 2 phase 6 bullets above carry it.
- Change 2's reconciliation, landed in change 2 at `996a181` (lane
  openRepoProject-2 ruling R-7): a `clean` plan's `limits.worktree_rows` holds
  only its own mode's cap, and the overview reads three keys from the shared
  constants and reports them in its `limits`: `batch_row_cap` (128),
  `report_row_cap` (256), and `target_limit` (16), which ruling R-14 renames
  `targets` at `fa9f0be` to match `clean`'s plan. Overview "Attention
  categories", the synthesis's bounds row, and the "Caps at 150 ms" bullet above
  carry it.
- Change 1's final text is `8973762`: read at `0b3c33d`, fix round at `d6aaa9a`,
  wordings at `6792e06`, R-15 at `9eeac52`, R-17 at `4f2162b`, R-19 at
  `7e2589f`, and R-20 at `8973762`; lane openRepoProject-3 read `7e2589f` clean
  on 2026-10-09, lane openRepoProject-2 landed that read's LOW finding and the
  change 1 proposal phrase noted in the `568c477` read, as ruling R-20, and
  PR #11 was marked ready for review at `8973762` the same day, ratification
  remaining Brett Heap's, as "Rulings R-11 to R-20 and Brett Heap's ruling —
  2026-10-09" below records.

### Rulings R-4, R-8, and R-9 — 2026-10-09

Lane openRepoProject-2 ruled on Codex's inline review of both changes on
2026-10-09, and rulings R-8 and R-9 go into the changes' current commits; each
is a departure from the packet, recorded at its passages as "lane
openRepoProject-2 ruling R-8" or "R-9" (2026-10-09), a departure from the
packet. Its ruling R-4 of the same day is recorded at its passages as "lane
openRepoProject-2 ruling R-4, 2026-10-09".

- R-8, the escaped code points: the path-escaping rule names the Unicode general
  categories Cc, Cf, Zl, and Zp as the code points escaped in the `$'…'` form
  and in JSON, the packet's enumeration (U+0000 to U+001F, U+007F to U+009F,
  U+200E, U+200F, U+2028, U+2029, U+202A to U+202E, and U+2066 to U+2069) kept
  as examples within that rule (change 1 at `0b3c33d`). Overview "Path encoding"
  and Batch "Representation rules" keep the enumeration, each with a note saying
  so, and the "Path escaping" bullet above points here. In the `$'…'` form a
  code point above U+FFFF is escaped as `\UXXXXXXXX`, with eight hexadecimal
  digits, and both notes say so. The escaped set follows the running Python's
  `unicodedata` (Unicode 15.0 on Python 3.12, 13.0 on 3.10), so it also escapes
  U+00AD, U+061C, U+200B, U+FEFF, U+E0001, and U+E0020 to U+E007F, which the
  packet's list omits, and `plan_digest`, which hashes raw values, is
  unaffected.
- R-9, path validity flags: every nested JSON path value carries a validity flag
  beside it, and `ignored_samples` entries become objects
  `{path, path_valid_utf8}` in both changes, where the packet has an array of
  strings. Overview "Worktree-specific probes", its worktree-row table, and its
  "Representation rules", and Batch "Bounded ignored-file inspection", its plan
  envelope's `worktrees` row, and its "Representation rules" carry it; the
  fixtures of both documents keep the packet's shape, with a one-line note
  beside each. Change 1 at `0b3c33d` names the keys:
  `repository.root_valid_utf8`, which also covers the envelope's `root`, and
  `common_dir_valid_utf8`, both always true in `clean`; `path_valid_utf8` on
  refusals, row errors, and apply targets; and the same flag added, additively,
  to the `status` and `doctor` dicts and their `errors` entries. At `d6aaa9a`
  `root_valid_utf8` also sits beside each nested family member's `root`, and the
  departure cites Batch lines 804-806 and 963-964 at `da33d92`, line 966 being
  the limits row.
- R-4, the manifest cap: the over-cap test reads `st_size`, so a manifest larger
  than 1 MiB by `st_size` is `manifest-invalid` before it is read. Batch
  "Eligibility and merge-target terminology" and its `manifest-invalid` refusal
  row, Overview "Collector boundary and error isolation", the shared baseline
  items of Batch, Overview, and the packet overview, and the change 2 council V7
  bullet above carry it.

### Rulings R-11 to R-20 and Brett Heap's ruling — 2026-10-09

Lane openRepoProject-3 re-verified change 1 at `0b3c33d` and change 2 at
`996a181` on 2026-10-09, and lane openRepoProject-2 ruled on the findings the
same day; each ruling is recorded at its passages under its label (lane
openRepoProject-2, 2026-10-09). Change 1 was read at `0b3c33d`; its fix round
landed at `d6aaa9a`; `6792e06` made two wording fixes (the proposal's JSON
bullet adds "or end of input at the question"; design D12 says "pass every gate
before `deferred-target-cap`" instead of "through `unstarted-branch`"), after a
merge of `main` at `26a5668` (`a83a661`) that changed nothing in the change;
ruling R-15 landed at `9eeac52` ("Anchor the reflog test on the creation entry
whatever its message (R-15)"); ruling R-17 at `4f2162b` ("State what the
report's excluded list and digest hold above 128 rows (R-17)"); ruling R-19 at
`7e2589f` ("Scope the report digest rule to the band above 128 rows and record
R-17 (R-19)"); and `8973762`, change 1's final text, adds ruling R-20 ("Name the
digest's full scope in the report band and align one movement phrase (R-20)").
Change 2 was read at `996a181`; its fix round, carrying R-13 (b), R-14, the R-12
mirror, and R-15, landed at `fa9f0be` (followed by a merge of `main` at
`26a5668`, `12febc0`, that changed nothing in the change); `ef288fe` adds ruling
R-16, takes requirement 7's anchor wording into design D5, adds the
fetch-created case to the proposal's scenario list and D13's map, drops the
"decision 11" phrase from its R-8 bullet, and cites change 1 at `4f2162b` in
task 2.2, D12, D5, and the later-rulings paragraph, which also records R-16;
`fd4b05a` adds ruling R-18; `568c477` copies change 1's movement wording into
all four places and lists R-18 in the later-rulings list and task 2.2; and
`4495ae7`, change 2's final text, adds ruling R-20 ("Credit selected: null to
R-15 and complete D12's ruling record (R-20)"). Change 1's delta scenarios
number 95 at `0b3c33d`, 96 at `d6aaa9a` and `6792e06`, and 97 at `9eeac52` and
after, 65 in `project-clean`, 17 in `project-clean-review-safety`, and 15 in
`project-command`: "A branch reset to the merge target's tip stays unstarted" is
new at `d6aaa9a`, where the material of finding M4 landed as AND clauses inside
existing scenarios and two scenarios were renamed, "A branch whose reflog is
missing, empty or expired" and "Twenty rows pass every gate before
deferred-target-cap", and R-15 adds "A branch fetched at the merge target's tip
stays unstarted", with AND clauses for `update-ref` and `push .`. Change 2's
`project-overview` delta has 61 scenarios at `fa9f0be` and after. At `996a181`
change 2 agreed with change 1 at `0b3c33d` on every shared value, and lane
openRepoProject-2's re-check of `fa9f0be` found its remedies byte-identical with
change 1's. Lane openRepoProject-3's delta reads found every R-11 to R-14 item
applied in change 1 at `d6aaa9a` and `6792e06` and every R-15 and R-17 element
applied at `4f2162b`, recorded change 2 at `fa9f0be` as below, and found both
changes clean at `7e2589f` and `568c477`; lane openRepoProject-2 landed the
three LOW findings of those reads and a phrase they noted as ruling R-20, at
`8973762` and `4495ae7`, and marked PRs #11 and #12 ready for review at those
commits on 2026-10-09, ratification remaining Brett Heap's. At `4f2162b` and
`7e2589f` and in change 2 at `ef288fe` and after
`openspec validate --all --strict` passes 7 of 7 items. Change 2's task 2.1, the
OQ-4 cap measurement, is still open and gates the Speckit handoff.

- R-11 (change 1, landed at `d6aaa9a`), the eight internal contradictions that
  change 1's re-verification found: (a) once a plan is built, an incomplete plan
  is refused first, then an `--expect-plan` mismatch, and only then does an
  empty complete selection exit 0, while in single mode an excluded target stays
  `target-excluded`, the order Batch "Fresh plan and plan digest" already gives;
  (b) the exit table is scoped to runs with `--apply`, and a preview or report
  exits 2 only for a refusal raised before a plan is built, 1 for an incomplete
  plan, and 0 otherwise, the signal exits excepted; (c) the report's `selected`
  and its human line `--all-safe would select N` hold only for a repository of
  at most 128 worktree rows, and above 128 the line reads
  `--all-safe would be incomplete (inspect-cap)`, the plan JSON carrying
  `selected: null` and a report-only `notes` entry with code `inspect-cap` and
  `rows`, the count of registered worktree rows, which alone does not make the
  report incomplete, under ruling R-15, with R-17 below; (d) SIGINT, SIGTERM, or
  SIGHUP before the apply phase, and end of input at the confirmation question,
  print `Cancelled.` on standard error, on a best-effort basis, and no JSON
  document; (e) `push` and `delete-branch` re-inspect in single mode for the row
  cap and the ignored-file bounds; (f) the `errors` entries of `status` and
  `doctor` take design D16's shape,
  `{code, message, path?, path_valid_utf8?, reason?}`, with `root_valid_utf8`
  beside the top-level `root`; (g) the 64 s run bound excludes time blocked at
  the confirmation question; and (h) the `reflog-unavailable` remedy is unified,
  as R-12 and R-15 word it. Batch "Deadline and budgets", "Interruption and
  expiry", "Exit codes", and "Machine-readable apply results", the synthesis's
  exit list, finding 2's row, and the change 1 council V1 and run-bound bullets
  above carry b, d, and g.
- R-12 (change 1, landed at `d6aaa9a`) accepts lane openRepoProject-3's six
  MEDIUM findings on change 1 at `0b3c33d`, and its LOW items: M1, the read's
  outcomes split; M2, a branch whose anchor has expired while a later movement
  survives, which now passes, where the text at `0b3c33d` failed closed whatever
  the later history; M3, force-reset branches; M4, the missing delta scenarios;
  M5, R-labels that could not be traced; and M6, the remedy texts. The test is a
  movement after an anchor, where the D10 amendment had tested for a commit
  since the branch's creation: the anchor is the last surviving entry whose
  message begins `branch: Created from`, as `worktree add -b`, `branch`, and
  `checkout -b` write, or `branch: Reset to`, as `worktree add -B`, `branch -f`,
  and `checkout -B` write on an existing branch; a movement is an entry after
  the anchor, or any entry when no anchor survives, whose old and new objects
  differ, so a rename is no movement. The head test runs first: a last entry
  whose new object differs from the current head gives `reflog-unavailable`;
  otherwise a movement passes the gate; an anchor with no movement after it, its
  new object equal to the head, gives `unstarted-branch`; and no anchor and no
  movement, or any other combination, gives `reflog-unavailable`. The reflog,
  `logs/refs/heads/<branch>` in the common directory, is read once, at most
  64 KiB, within the filesystem budget, and revalidation does not read it again.
  A missing file (`ENOENT` or `ENOTDIR`), a 0-byte file, the 64 KiB bound
  reached, whatever was read before it, or surviving entries that cannot decide
  give `reflog-unavailable`; no test reads an expired first line, since expiry
  shows as no surviving decisive entry; any other OS error is the row's
  `inspection-error` with `os-error`; and a read not finished within the
  filesystem budget leaves the row unprobed. `gc.reflogExpire` defaults to
  90 days, Git 2.43 leaves a 0-byte file once every entry has expired, and a
  branch created 100 days earlier, committed to 95 days earlier, and renamed
  10 days earlier keeps only the rename entry, so neither an anchor nor a
  movement survives. Change 1's Risks record that a branch with no surviving
  decisive entry is never removable by `project` in either mode, that the
  reftable backend or `core.logAllRefUpdates=false` excludes every merged row,
  and that a branch created from a remote branch that already had commits reads
  as unstarted and fails closed. Under M6 and R-14 M-B, change 1's D18 form
  governs both changes, superseding R-10, with no "explicitly":
  `unstarted-branch` reads "no commit was made on this branch here since it was
  created; review, then git worktree remove yourself", and `reflog-unavailable`
  takes R-15's wording below. Change 1's README section now opens with four
  user-visible changes; at `4f2162b` its task 1.2 cites `9ea2f02`, `0b3c33d`,
  `d6aaa9a`, and "the commit that anchors the reflog test on the creation entry,
  R-15", and design D10's header reads "(V2 as amended, M3, M4, R-12, R-15)".
  Batch "Eligibility and merge-target terminology", Overview "Attention
  categories", the synthesis, the packet overview, and the D10 bullets above
  carry it.
- R-13 (R-13a in lane openRepoProject-2's messages, "R-13 (a)" in change 2's
  text; change 1, landed at `d6aaa9a`): the shared evidence model gains the
  null-root case of its probe directory rule. Where `root` is null (a bare
  repository, a missing main worktree, or a gitfile checkout whose main worktree
  cannot be named), the repository-wide probes run in `common_dir` for a bare
  repository and otherwise where the identity probe ran; `clean` refuses those
  layouts and the overview reports them, so the shared model carries the rule
  and the overview records no departure. Overview "Worktree-specific probes",
  the probe directory rules of the packet overview and the synthesis, and the
  "Probe directory rule" bullet above carry it.
- R-13 (b) (R-13b in lane openRepoProject-2's messages; change 2, landed at
  `fa9f0be`): three delta scenarios, "Present eligible external worktree",
  "Canonical identity through the handoff", and the repaired worktree of "Gated
  merged worktrees", state that the branch has a commit of its own; task 2.2 was
  ticked at `fa9f0be` citing `0b3c33d`, `996a181`, and `d6aaa9a`, and at
  `ef288fe` also cites the re-read against change 1's `4f2162b`; the long
  sentence of the design's Context says "manifest() onward"; requirement 5's
  classification claim is limited to the rows that `clean`'s report inspects,
  the overview classifying rows up to its own worktree-row cap per run; and
  PR #12's body names the OQ-4 measurement, task 2.1, as owed before the Speckit
  handoff.
- R-14 (both changes) accepts lane openRepoProject-3's findings on change 2 at
  `996a181`: M-A, the R-8 departure unlabeled in both proposals, which change 1
  at `d6aaa9a` labels beside R-9 and a new R-4 `st_size` departure, and change 2
  at `fa9f0be` labels, citing as the packet text it departs from the single
  `\uXXXX` form of this record's lines 301-306 and the synthesis's lines 247-250
  and the enumerated set of Overview's lines 910-916, all at `da33d92`; M-B, the
  `unstarted-branch` remedy, false for a branch created from a remote branch
  that already had commits, replaced in both changes by R-12's text with a Risks
  line for that case; and M-C, `repository.root` for a repository reached first
  through a linked worktree, which is the canonical path of the first registry
  record when the candidate is a linked worktree. Its LOW items add a scenario
  for a `common_dir` that is not valid UTF-8 and rename the overview's `limits`
  key `target_limit` to `targets`, matching `clean`'s plan. Change 1's halves
  landed at `d6aaa9a` and change 2's at `fa9f0be`.
- R-15 (both changes; landed in change 2 at `fa9f0be` and in change 1 at
  `9eeac52`) accepts lane openRepoProject-3's findings on change 1 at `6792e06`:
  MEDIUM, a branch created without a `branch:` message, as by
  `git fetch origin feat:f1`, `git update-ref`, or `git push .`, had no anchor,
  so any entry was a movement and an unstarted branch failed open, against the
  review-safety requirement; LOW, the `reflog-unavailable` remedy was false for
  the bound-reached and head-mismatch cases, a reflog over 64 KiB failing closed
  even with a movement, which Risks did not record; and LOW, task 1.2 claimed
  R-1 to R-14 where the change names only R-4, R-8, R-9, and R-11 to R-14. The
  anchor is now also the last surviving entry whose old object is all zeros, a
  creation by any command, and such an entry is never a movement; a movement is
  an entry after the anchor, or any entry when no anchor survives, "whose old
  and new objects are non-zero and differ"; and D10 adds that a line is
  `<old> <new> <identity> <time> <zone>`, "then a tab and the message when there
  is one; an update-ref without -m writes neither" (change 1 at `4f2162b`). The
  new scenario "A branch fetched at the merge target's tip stays unstarted"
  gives its branch an upstream by `git branch -u`, with AND clauses for
  `update-ref` and `push .`; on Git 2.43.0 the fetch writes "fetch origin
  feat:f1: storing head" ("fetch -q origin feat:f1: storing head" in the quiet
  form), `git update-ref` writes no message, the line ending after the time zone
  with no tab, `git push .` writes "push", and a later `git branch -u` or
  `git worktree add <path> f1` adds no entry. The `reflog-unavailable` remedy in
  both changes becomes "the branch's reflog is missing, expired or undecidable;
  review, then git worktree remove yourself", with a Risks line for the
  fail-closed residual over 64 KiB. Task 1.2 matches the later-rulings list,
  R-4, R-8, R-9, and R-11 to R-15, whose entries name sections, and which now
  also carries V2 amended with its sections; design D10 names R-15 in its
  header, and the design's opening says R-15 edited Context, D10, D14, D18,
  Risks, and the Migration Plan. Above 128 rows a report's JSON carries
  `selected: null` and a report-only `notes` entry with code `inspect-cap` and
  `rows`, the count of registered worktree rows (200 in its scenario), which
  alone does not make the report incomplete, beside the unchanged human line
  `--all-safe would be incomplete (inspect-cap)`.
- R-17 (change 1, landed at `4f2162b`): above 128 rows a report's gates still
  run for every inspected row, so `excluded` lists every inspected row a gate
  excludes, with its `reason`, as in any report, and "only the selection step is
  withheld"; `apply_allowed` is false; and, at `4f2162b`, `plan_digest` was
  computed over the document as written, a null `selected` included, and a
  report's digest was never consumed by `--expect-plan` (rescoped by R-19
  below). At `4f2162b` change 1 passes `openspec validate --all --strict` for 7
  of 7 items, with 94 tests.
- R-19 (change 1, landed at `7e2589f`; R-20 widens its band sentence at
  `8973762`) accepts lane openRepoProject-3's three LOW findings on change 1 at
  `4f2162b`: R-17's digest sentence stood apart and so covered every report,
  against the digest's definition and for reports of at most 128 rows (L1);
  design D19's `notes` list lacked the report's `inspect-cap` note (L2); and
  R-17 was missing from the later-rulings list, task 1.2, and the design's
  opening (L3). Above 128 rows the `plan_digest` is now "computed over the same
  canonical text as any plan, which covers only the repository's identity
  fields, the merge target and selected, with selected null", and
  `--expect-plan` never consumes it, "because an apply there is an incomplete
  plan and is refused before the digest is compared"; at most 128 rows, a
  report's `plan_digest` equals the `--all-safe` preview's for the same
  selection, since the mode is not in the digest, and an `--expect-plan`
  carrying it matches, which is intended; `apply_allowed` stays false, and D14
  and OQ-29 say the same. D19's `notes` list carries the report-mode
  `inspect-cap` note with `rows`, crediting D14 and R-15, and the design's
  Context, the later-rulings list, and task 1.2 name "R-11 to R-15, R-17 and
  R-19", R-16 and R-18 binding change 2 only. At `7e2589f` change 1 has 97
  delta scenarios and passes `openspec validate --all --strict` for 7 of 7
  items.
- R-16 (change 2, landed at `ef288fe`): a reflog read that does not finish
  leaves the row unprobed, and the repository's `inspection-incomplete` gate
  withholds the suggestion, so that gate's remedy becomes "repair the
  inspection-error rows, or re-run for the rows left unprobed, first"; `ef288fe`
  also re-ticks task 2.2 citing change 1's `4f2162b`.
- R-18 (change 2, landed at `fd4b05a`, with `568c477`) accepts lane
  openRepoProject-3's findings on change 2 at `fa9f0be`: the fetch-created
  clause gives its branch an upstream, "given an upstream by
  `git branch -u origin/feat f1`, which writes no reflog entry", as change 1's
  scenario does, in the spec, the proposal's scenario list, the Decisions
  bullet, and D13's fixtures; the residual over 64 KiB joins the overview's
  Risks; the canonical movement wording is change 1's at `9eeac52`, an entry
  after the anchor, or any entry when no anchor survives, whose old object is
  not all zeros and whose old and new objects differ, which `568c477` copies
  literally, "whose old and new objects are non-zero and differ", into all four
  places, replacing `fa9f0be`'s "both not all zeros and differ"; and the
  line-format note says the tab and message exist only when the command wrote a
  message, `git update-ref` without `-m` writing neither, the line still an
  anchor.
- R-20 (landed in change 1 at `8973762` and in change 2 at `4495ae7`, their
  final texts) accepts lane openRepoProject-3's three LOW findings from its
  final reads of `7e2589f` and `568c477`, and the proposal phrase it noted. In
  change 1, the spec, D14, and OQ-29 now make a report's `plan_digest` at most
  128 rows equal the `--all-safe` preview's "for the same repository identity,
  merge target and selection", and add that the digest also covers the merge
  target's name and SHA, so a target that advances between the report and the
  preview gives `plan-digest-mismatch`, which is safe; the proposal's movement
  phrase now reads "whose old and new objects are non-zero and differ", as its
  spec and design do. In change 2, design D12 credits `selected: null` above 128
  rows to R-15, R-17 having added only what `excluded` and `plan_digest` hold in
  that band, names R-16 and R-18, and states the sequence: R-12, R-13 (b), and
  R-14 landed at `fa9f0be` against change 1 at `d6aaa9a` and were re-read
  against `4f2162b` at `ef288fe`, R-18 landed at `fd4b05a` and `568c477`, and
  the current reconciliation is against change 1 at `7e2589f`. R-20 changes
  wording only and is named in the two commit subjects, not in either change's
  later-rulings list or tasks; change 1 keeps 97 delta scenarios and change 2's
  `project-overview` delta 61. Lane openRepoProject-2 marked PR #11 ready for
  review at `8973762` and PR #12 at `4495ae7` on 2026-10-09; ratification
  remains Brett Heap's.
- Change 2 at `996a181` also landed R-2, the submodule test first in every
  repository at no extra child, with the outcomes recorded in "Change 2 phase 6
  records — 2026-10-09" above; R-3, the UTF-8 check of `common_dir`; R-5, the
  per-child budget `min(5 s, work remaining)`; R-6, the interim `remote-gone`
  text, identical in all seven places across both changes; R-7, the three
  `limits` keys recorded in "Change 1 phase 6 records — 2026-10-09" above; and
  the D10 mirror, which read from the creation entry until `fa9f0be` adopted the
  anchors of R-12 and R-15.
- Change 2 at `fa9f0be` (lane openRepoProject-2, 2026-10-09) also carries: the
  R-12 mirror with R-15's anchor, its movement wording "both not all zeros and
  differ" until ruling R-18 made change 1's canonical, and the creation-anchor
  writers named as `git fetch <remote> <ref>:<branch>`, `git update-ref`, and
  `git push .`, a rename's entry having equal old and new objects; a reflog read
  cut by its wait or by the deadline records `probe-timeout` or
  `deadline-exceeded` and leaves the row unprobed for the gate, while reaching
  the 64 KiB bound is `reflog-unavailable`, and the repository gates count a
  reflog `OSError` and an unfinished read alike; the gate table's descriptions
  "(an anchor with no movement after it)" and "(a reflog that cannot decide)";
  the new scenario "Non-UTF-8 common directory" and AND clauses for a
  `git branch -m` rename, a `worktree add -B` reset, `git fetch origin feat:f1`,
  a ref rewritten without a reflog entry, and a second repository whose
  permission error gives `os-error`, `inspection-error`, and
  `inspection-incomplete`; one Risks line for the reftable backend and for a
  branch with no surviving decisive entry, where change 1 keeps two; and the
  sentence "R-10's remedy wording is superseded by R-12, R-14 and R-15".
- Writer additions in change 1's fix round, which lane openRepoProject-2
  accepted: the R-9 departure cites Batch lines 804-806 and 963-964 at
  `da33d92`, line 966 being the limits row; design D16 gains `reason?`; end of
  input at the confirmation question joins the exceptions that print no JSON
  document; `root_valid_utf8` also sits beside each nested family member's
  `root`; and the head test runs first in the reflog order.
- New human text in change 1 at `0b3c33d`: the plain report adds
  `Report: complete` or `Report: incomplete (CODES)` and the line
  `--all-safe would select N`, limited by R-11 to 128 rows; the preview and the
  apply add the wait line, the residual-window line, and the deferral line.
- Lane openRepoProject-3's findings on change 2 at `fa9f0be`, sent to lane
  openRepoProject-2 on 2026-10-09, all landed: the `inspection-incomplete`
  remedy and task 2.2 at `ef288fe` (R-16), the rest under ruling R-18 at
  `fd4b05a` and `568c477`. They were: MEDIUM, the `git fetch origin feat:f1`
  clause cannot be reached as written, since the branch has no upstream and the
  ladder gives `unpublished` first, the fix being an upstream set by
  `git branch -u`, as change 1's scenario at `9eeac52` does; LOW, R-15's Risks
  line for the fail-closed residual over 64 KiB is missing; LOW, the movement
  wording goes beyond R-15; LOW, `git update-ref` writes a reflog line with no
  tab, against design D5's line format and "any command"; LOW, the
  `inspection-incomplete` remedy (R-16); and LOW, task 2.2 was ticked early.
- Lane openRepoProject-3's final read of change 1 at `7e2589f` (2026-10-09)
  reads it clean: R-19 resolves L1 to L3, in the band sentences of its
  `project-clean` delta, D14, and OQ-29, in D19's `inspect-cap` note crediting
  D14 and R-15, and in the design's opening, the later-rulings list, and task
  1.2, which name R-11 to R-15, R-17, and R-19; its scenarios are 65, 17, and
  15, 97 in all; its interim `remote-gone` text is byte-identical in its three
  places; its later-rulings list credits the ruling whose content a section
  carries, as R-19's entry says; and R-16 and R-18 bind change 2 only. Its one
  LOW finding, sent to lane openRepoProject-2, landed as ruling R-20 at
  `8973762`: the statement that a report's `plan_digest` equals the
  `--all-safe` preview's for the same selection overstates, since the digest
  also covers the merge target's name and SHA, so a target that advances
  between report and preview gives `plan-digest-mismatch`, a safe refusal.
- Lane openRepoProject-3's final read of change 2 at `568c477` (2026-10-09)
  reads it clean: every R-16 and R-18 element is applied, and all six of its
  findings at `fa9f0be` are resolved, the `git branch -u` clause, the Risks line
  over 64 KiB, change 1's movement phrase in all four places, the line format,
  the `inspection-incomplete` remedy, and task 2.2 listing R-18. It has 61
  scenarios in its `project-overview` delta and 2 in its review-safety delta;
  its interim `remote-gone` text is identical in its four places, seven with
  change 1's three; and question 1 is still open in both changes, pending Brett
  Heap's word to lane openRepoProject-2. Its reflog test and change 1's differ
  in nine points of framing, none of which changes an outcome. Its two LOW
  findings, sent to lane openRepoProject-2, landed as ruling R-20 at `4495ae7`:
  its design credits `selected: null` above 128 rows to R-17, where change 1's
  D14 credits R-15; and its D12 names neither R-16 nor R-18 and dates R-12, R-13
  (b), and R-14 to a re-read at `4f2162b`, though they landed in `fa9f0be`
  against `d6aaa9a`. Lane openRepoProject-3 also noted that change 1's proposal
  reads "whose non-zero old and new objects differ" where its spec and design
  read "whose old and new objects are non-zero and differ", with the same
  meaning; R-20 aligns the proposal with them at `8973762`.
- Lane openRepoProject-2 marked PR #11 ready for review at `8973762` and PR #12
  at `4495ae7` on 2026-10-09, after lane openRepoProject-3's word that both
  changes read clean and the two R-20 commits, and reported both ready to Brett
  Heap; ratification remains Brett Heap's. The PR heads later moved, PR #11 to
  `cab78d8` and PR #12 to `704eaa9`, by numbering-only commits that renumbered
  the Speckit handoffs to features 004-project-clean-all-safe and
  005-project-overview after lane openRepoProject-1's PR #17 took 003; content
  is unchanged, and `8973762` and `4495ae7` remain the content shas (lane 2,
  2026-10-09).
- Brett Heap's ruling on the packet's first open question (Brett Heap,
  2026-10-09): "yes, local ancestry proof outranks remote-gone", delivered
  verbatim through lane openRepoProject-3's resume prompt as a preserved draft
  of his and logged as lane openRepoProject-3's RULED line of
  2026-10-09T03:05:47Z on issue #6. A local ancestry proof outranks
  `remote-gone` for worktree rows. The packet records it only as the answer to
  that question: the open lists of Batch, Overview, the packet overview, the
  synthesis, and this record mark it ruled, and the packet designs no mechanism
  and changes no gate text. The proposals' interim `remote-gone` text is
  unchanged in seven identical places, three in change 1 at `6792e06` and after,
  to its final `8973762`, and four in change 2 at `fa9f0be` and after, to its
  final `4495ae7`, and both changes still list the question as open; amending
  them on Brett Heap's word is lane openRepoProject-2's, sha to follow. The
  second question, patch equivalence for squash merges, stays open.
