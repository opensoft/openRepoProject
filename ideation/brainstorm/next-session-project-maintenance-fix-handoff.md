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
`add-project-overview` (issue #10, draft PR #12), which absorbs `acf0133` and
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

The packet was revised on 2026-10-07 against the five findings above, and a
fix round then resolved every high and medium finding of the first
adversarial review. Each row gives the decision taken, the document and exact
section headings that hold its contract, and the validation scenarios that
prove it. "Batch" is [batch cleanup](project-maintenance-batch-cleanup.md)
and "Overview" is
[project overview and attention](project-maintenance-project-discovery.md);
headings read `section: subsections`. The design contract baseline is still
`a040790`: `origin/main` has since advanced to `da33d92`, which merged PR #7
(this packet) on 2026-10-07; before it, PR #4 archived the completed OpenSpec
changes and promoted their specifications to `openspec/specs/` and PR #5
added the `prefer-triad-in-project-new` OpenSpec proposal; and the `project`
executable and its tests are unchanged.

| Finding | Decision | Contract | Proving scenarios |
| --- | --- | --- | --- |
| 1. Define the batch safety boundary | The guarantee is narrowed: concurrent writers are outside the safe contract, and a removal child is spawned only when the repository identity `{root, common_dir, dev, ino}`, the worktree identity `{path, dev, ino, admin_id}` with two-way admin registration, the branch evidence, every baseline signature field, the `locked` flag, the absence of submodules (a gitlink or an admin `modules` entry) and of hidden local state (an index entry flagged assume-unchanged or skip-worktree), read by a bounded `git -C <worktree path> ls-files -v --stage -z` inside the target worktree under the probe directory rule, the manifest's `tracking_branch`, and the merge target `{name, source, sha}`, re-resolved from a fresh manifest read, still equal the confirmed plan at revalidation; otherwise the target is `refused` (`identity-changed`, `branch-changed`, `state-changed`, `contains-submodule`, or `hidden-local-state`), no later target is attempted, and the exit is 2. A repository replaced after a removal makes that target `unknown` with `unconfirmed-removal`, and the exit is 1. The removal runs as `git -c status.showUntrackedFiles=normal -C <command directory> worktree remove <path>`, so Git's own non-force check sees untracked files whatever the user's configuration; ignored files created and index flags set after revalidation are the documented residual window. A branch change seen only after removal is `removed` with `branch-advanced-after-removal` (or `branch-missing-after-removal`), exit 2, and the branch retained. | Batch, "Eligibility and merge-target terminology"; "Safety boundary": "Identity", "The narrow guarantee", "Changes after confirmation", "Residual window", "Branch race"; "Probe accounting and limits": "Probe directory rule", "Worktree-specific probes", "Preflight and targeted revalidation" | Batch: **Hidden local state.**, **Submodules.**, **Target directory replaced.**, **Admin registration changed.**, **Parent directory swapped.**, **Repository replaced mid-batch.**, **New worktree and pre-removal changes.**, **State changes before revalidation.**, **Changed later target.**, **Untracked file under `status.showUntrackedFiles=no`.**, **Ignored file in the residual window.**, **Branch advances before removal.**, **Branch advances after removal.** |
| 2. Make execution and interruption reconcilable | `--apply` always recomputes, prints, and confirms a fresh plan carrying `plan_digest`, and an optional `--expect-plan` refuses a differing one with `plan-digest-mismatch`. Single-target `remove` is strictly a one-item batch on the shared `retire_worktree` seam (revalidate, spawn, reap, reconcile): the same full plan (`mode: "single"`) under the same caps, the refusals `worktree-not-found` and `target-excluded`, and `inspection-incomplete` when any row is `inspection-error`. One monotonic 60 s deadline holds back a 10 s reconciliation reserve, so work stops at 50 s, with 5 s per probe and every filesystem call in a worker thread; SIGINT or expiry terminates and reaps the child's process group before a rescan, and no removal is spawned with less than `removal_floor_seconds` (5 s) of the work deadline left: that target and every later one are `not-attempted` with `deadline-exceeded`, and the exit is 1. Every target ends in the stage enum `pending`, `removed`, `refused`, `failed`, `unknown`, or `not-attempted`, and every `removed`, `refused`, `failed`, or `unknown` target carries a reconciliation record (`registry_entry_present`, `path_present`, `branch_present`, `branch_sha`, `reconciled`); `removed` needs rescan evidence and `reconciled: true`; an unproven outcome, or an exception after the apply phase begins, is `unknown` with exit 1; and a `failed` target (`git-refused` for exit 128, `git-failed` for any other status such as 255 with an `orphaned-directory` note, or `spawn-error`) exits with Git's own status, or 2 for `spawn-error`. | Batch, "Execution model": "Fresh plan and plan digest", "One mutation seam", "Deadline and budgets", "Interruption and expiry", "Stages and reconciliation", "Exit codes"; "Repository and JSON contract": "Apply result record"; "Baseline behavior changes"; "Partial completion and recovery" | Batch: **Deadline expiry mid-batch.**, **Exit 0 without evidence.**, **SIGINT.**, **Git leaves an orphaned directory.**, **Git refuses the removal.**, **Unreadable path after removal.**, **Exception after the apply phase begins.**, **Single target equals a one-item batch.**, **Preview is advisory.**, **Plan digest mismatch.** |
| 3. Bound and share the expensive work | Both documents use one probe set: one `git --version` per invocation; per repository, memoized by `common_dir` and fanned out, the same four repository-wide children (identity, registry listing, ref listing in one shared NUL-separated `for-each-ref` format, and merged set); and per present, registration-verified worktree row, the main worktree included, one combined status probe that stops at a 65th ignored record or a 4,097th record. Every worktree-specific probe runs as `git -C <worktree path>` against that worktree's own index after its identity is verified, and repository-wide probes run as `git -C <repository.root>` (`common_dir` for a bare repository), except the identity probe, which runs in the candidate; when a linked worktree is reached first, the registry listing also runs in the candidate, because the main worktree's path comes from that listing, which changes which directory the command runs in, never which index a probe reads. Batch revalidation is a targeted check of at most five children plus a manifest re-read and a `modules` check, and `probes` and `operations` (`{estimated, performed}`) appear in both the plan and the apply result record. Candidates and registry entries are sorted before any cap, and dropped work is reported as `omitted: {count, exactness}`. Both derive their caps at 150 ms per Git child, a 1.5× margin over the assumed 100 ms. The batch probes serially and uses one fit test, a worst case that completes within the 50 s work deadline and spawns its last removal with at least `removal_floor_seconds` (5 s) left: its row cap is the largest power of two for which at least 16 targets fit, and its target cap the largest multiple of 8 that fits with it, so it inspects at most 128 worktree rows (`limits.worktree_rows`, the main worktree included) and selects at most 16 targets, with a worst case of about 39.9 s. The overview takes at most 32 roots, 128 candidates, and 512 worktree rows with four concurrent children across repositories, after a listing phase estimated at about 6 s, one worker task per root bounded at 5 s, which leaves about 54 s for Git work. A cap hit or deadline gives an incomplete result (`inspect-cap`, `inspection-incomplete`, or `deadline-exceeded` in the batch; `scan-limit`, `probe-timeout`, or `deadline-exceeded` in the overview). | Batch, "Execution model": "Deadline and budgets"; "Probe accounting and limits": "Probe directory rule", "Repository-wide probes", "Worktree-specific probes", "Preflight and targeted revalidation", "Cap arithmetic", "Inspection order and omitted work", "Bounded ignored-file inspection", "Probe and operation estimates". Overview, "Discovery scope and ordering": "Ordering, truncation, and omitted counts", "Caps and their arithmetic"; "Probe model and deadline": "Git version check", "Repository-wide probes", "Worktree-specific probes", "Scheduling and concurrency", "Deadline and timeouts", "Probe accounting"; "Deferred remote inspection boundary" | Overview: **One probe set per repository.**, **Candidate cap after sorting, exact count.**, **Candidate cap with an incomplete listing.**, **Root and worktree-row caps.**, **Probe timeout.**, **Hung filesystem call.**, **Invocation deadline.**, **Bounded concurrency.**, **Bounded ignored files.**, **User status configuration.**, **Git version refusal.**, and the remote item under "Deferred validation scenarios". Batch: **Row cap and planning failures.**, **Target cap.**, **Ignored-file bound.**, **Bounded revalidation work.** |
| 4. Make the repository and JSON contracts explicit | The command directory is the canonical, identity-checked `repository.root` (or `common_dir` for a bare repository) with no merge-target worktree requirement. Every `project clean` mode resolves an absolute path Git-first and refuses `target-not-repository-root` with exit 2 unless it is exactly a main worktree root; a relative path or no argument resolves to the repository Git finds there; only a bare name keeps the `discover` lookup, its Git child counted and bounded; and the report's `root` always names the command directory. The overview prints a new `schema_version: 1` envelope with typed project-row, worktree-row, finding, and `summary` fields; the batch plan is an additive superset of the baseline clean report with `limits`, `budget`, `probes`, and `operations`; the apply result record is defined and rendered as human text; both documents state representation rules with fixtures; a non-UTF-8 `repository.root` or `common_dir` refuses with `unsupported-path-bytes`; an unreadable or wrong-kind manifest is `manifest-invalid`; under `--json` an overview exit 2 prints the baseline error object with a `code` added, `{"error", "code"}`, which batch cleanup extends with its plan fields when no plan can be built, and an argument error prints no JSON; `suggested_command` is `null` unless a finding supplies one, and otherwise a JSON argv array naming the canonical root; and both documents list their baseline behavior changes. | Batch, "Repository and JSON contract": "Command directory and repository resolution", "Representation rules", "Plan envelope", "Refusal codes", "Apply result record", "Fixtures", "Machine-readable apply results"; "Baseline behavior changes". Overview, "JSON contract": "Envelope", "Project row", "Finding object", "Representation rules", "Repository identity and the clean handoff", "Path encoding", "Fixture"; "Result semantics"; "Baseline behavior changes" | Batch: **Overview handoff keeps identity.**, **Absolute path that is not a repository root.**, **Non-UTF-8 repository root.**, **Merge target missing, invalid, or conflicting.** Overview: **Canonical identity through the handoff.**, **Independent clones and aliases.** |
| 5. Close discovery scope and acceptance gaps | A `family.yaml` holder is one `family-holder` row counted once, with `relationships: []` and Git probes only when its own directory is the toplevel. A marker check that fails with anything but `ENOENT` or `ENOTDIR` makes an error row with `kind: null`; `collect(candidate) -> result` turns helper exceptions (such as `manifest-invalid`, `os-error`, or `internal-error`) and failed or timed-out probes into error rows while the scan continues, and path candidates never pass through `discover`. An unreadable or registration-mismatched worktree row is set to `inspection-error` directly, bypassing the ladder. A missing merge target becomes `merge_target: null` with a `no-merge-target` finding and no `cleanup_report` call. A `merged-removable` worktree yields the housekeeping finding and the `--all-safe` suggestion only after the batch's main-worktree, path-byte, registration, and lock gates, and otherwise the first failing gate's finding (`main-worktree`, `unsupported-path-bytes`, `registration-mismatch`, or `locked-worktree`, the batch's own exclusion reasons); a fifth gate withholds every `--all-safe` suggestion for a repository while any of its worktree rows is `inspection-error` or it has more than 128 worktree rows, because the batch plan would be refused as `inspection-incomplete` or `inspect-cap`, so its housekeeping findings and the row suggest only the read-only `project clean <root>`; the batch may still exclude a suggested worktree as `hidden-local-state` or `contains-submodule`, which only its own index probe and admin-directory check see. `review-required` is covered by a classifier test on an injected row; paths are read NUL-delimited; a path holding a control, bidirectional, or format code point or an undecodable byte prints in `$'…'` form with `\uXXXX` and `\xHH` escapes in lowercase hexadecimal (pasting the `\uXXXX` form needs a UTF-8 locale), JSON escapes every such code point, and a non-UTF-8 path is escaped and excluded as `unsupported-path-bytes`; and every acceptance scenario the finding listed is written. | Overview, "Discovery scope and ordering": "Candidates", "Repositories and linked worktrees", "Family holders"; "Collector boundary and error isolation"; "Merge target and classification reuse"; "Attention categories"; "JSON contract": "Path encoding"; "MVP validation scenarios". Batch, "Eligibility and merge-target terminology" | Overview: **Family holder count, relationships, and probe ownership.**, **Unreadable candidate directory.**, **One helper failure is isolated.**, **Manifest target.**, **`origin/HEAD` target.**, **`main` target.**, **`master` target.**, **Conflicting targets.**, **Missing target.**, **Every protected classifier.**, **Gated merged worktrees.**, **Attention filter per category.**, **Present eligible external worktree.**, **Missing external worktree.**, **Unreadable external worktree.**, **Control and format characters in paths.**, **Non-UTF-8 path.**, **Canonical identity through the handoff.**, **Local and read-only.** Batch: **Stable order and preserved work.**, **Every protected classifier.**, **Paths and empty plans.**, **Control-character and non-UTF-8 paths.**, **Merge target missing, invalid, or conflicting.** |

### Cross-document decisions

- Narrow guarantee: concurrent writers are outside the safe contract. The MVP
  claims no lock, lease, or writer-quiescence handoff, refuses on any change
  it observes at revalidation, and documents the residual window for ignored
  files created, and index flags set, after it.
- Removal command: single-target and batch removal both pass
  `-c status.showUntrackedFiles=normal` to the non-force
  `git -C <command directory> worktree remove <path>`, so Git's own check
  sees untracked files under any user configuration.
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
  the candidate. When a linked worktree is reached first, the registry listing
  also runs in the candidate, because the main worktree's path comes from that
  listing; that changes which directory the command runs in, never which index a
  probe reads.
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
  refuses it as it refuses a batch.
- Overview gates: a `merged-removable` worktree gets the housekeeping finding
  and the `--all-safe` suggestion only when it passes the batch's
  main-worktree, path-byte, registration, and lock gates in the batch's
  order, under the same codes the batch uses as exclusion reasons
  (`locked-worktree` for the lock), and only while no worktree row of its
  repository is `inspection-error` and the repository has no more than 128
  worktree rows, which would make the batch plan `inspection-incomplete` or
  `inspect-cap`, and, as amended on 2026-10-08, no worktree row of it went
  unprobed because the 512-row cap or the deadline cut it; otherwise the
  read-only `project clean <root>` is suggested, and the gate changes
  suggestions only. The batch may still exclude a suggested worktree as
  `hidden-local-state` or `contains-submodule`.
- Shared probes: one version check per invocation, the same four
  repository-wide children per repository (identity, registry listing, ref
  listing, and merged set) with one identical ref-listing format, and one
  combined bounded probe per worktree row,
  `git status --porcelain=v1 -z --untracked-files=normal --ignored=matching`,
  in both documents. All Git output is parsed NUL-delimited.
- Caps at 150 ms per Git child, a 1.5× margin over an assumed 100 ms that
  the proposal must measure: the batch inspects 128 worktree rows, the main
  worktree included, and selects 16 targets (Batch "Cap arithmetic"); the
  overview takes 32 roots, 128 candidates, and 512 worktree rows
  (Overview "Caps and their arithmetic") with four concurrent children across
  repositories, after a listing phase estimated at about 6 s that leaves
  about 54 s for Git work. Both name the row cap `limits.worktree_rows`. They
  replace the earlier 1,024/100 and 256/1,024 figures, which could not meet
  the deadline.
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
  remaining targets are `not-attempted` with `deadline-exceeded`, exit 1.
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
  reports `unpublished`; both are preserve states. Doctor classifies no
  worktree: it reads the same evidence but reports no classification.
- `ignored_files` keeps its baseline name and type but counts the ignored
  records read, a lower bound when `ignored_files_truncated` is true.
- Path escaping: a path holding a control, bidirectional, or format code
  point or an undecodable byte prints in the same `$'…'` form in both
  documents, with `\xHH` for each undecodable byte and `\uXXXX` for each
  decoded control, bidirectional, or format code point, both in lowercase
  hexadecimal, and each backslash doubled; pasting the `\uXXXX` form needs a
  UTF-8 locale. JSON escapes every such code point.
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

These remain open, except the entries marked decided, which the proposals
took on 2026-10-08 (see "Decisions taken by the proposals — 2026-10-08");
the [packet overview](project-maintenance-overview.md) carries the same
consolidated list without them.

- The measured per-child and per-removal costs and the overview's listing
  time, and therefore the final caps; the batch reapplies the same rule and
  fit test, which lowers the target cap in steps of 8 and keeps the row cap
  as large as it can.
- Caps versus concurrency: if the overview's four-way concurrency is
  rejected, its fallback is 32 candidates and 128 worktree rows (257
  children, about 38.6 s at 150 ms, or about 44.6 s with the listing
  estimate); above about 210 ms per child even concurrency needs lower caps.
- Whether to cap worktree rows per repository, since one repository with
  more than about 355 worktree rows cannot complete at 150 ms per child.
- Whether any limit is user-configurable.
- Whether `--apply --json` prints the apply result record (recommended) or
  the MVP stays human-only.
- Whether `--expect-plan` is required whenever `--yes` is used; the MVP makes
  it optional.
- Whether a relative path or the no-argument default must be an exact
  repository root, as an absolute path must, instead of resolving to the
  repository Git finds there.
- Whether a skip-worktree entry whose file is absent from disk, as in a
  sparse checkout, may be treated as safe instead of `hidden-local-state`.
- Whether a gitlink that was never populated, in a worktree whose admin
  directory holds no `modules`, may be treated as removable instead of
  `contains-submodule`.
- Whether bare repositories are supported or refused. Decided 2026-10-08:
  refused.
- Whether SIGTERM and SIGHUP receive the SIGINT treatment. Decided
  2026-10-08: yes, exiting 143 and 129, for `clean` and the overview.
- Whether the `attention` alias merits a separate command, and how
  `--attention --json` filters.
- Whether suggested commands also carry a display string (decided
  2026-10-08: no, argv arrays only), and whether the extra `dirty` finding
  for a dirty default-branch checkout is wanted.
- The final command and flag spelling.
- Whether cache disposal, paired branch retirement, and the remote, family,
  bench, container, and park integrations deserve separate changes.
- Added 2026-10-08, for Brett Heap and carried by both proposal lanes:
  whether a local ancestry proof should outrank `remote-gone` for worktree
  rows. The ladder tests remote presence before merge state, as the
  baseline does; GitHub's head-branch auto-delete leaves a merged branch's
  upstream gone; and the MVP never deletes a branch, so under the baseline
  order such a worktree is never eligible for `--all-safe`. Until it is
  ruled, the packet keeps the baseline ladder.

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
to be written until that PR was reviewed and merged, and the follow-ups above
are for the next revision.

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
  and `overview` only.
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
- `add-project-clean-all-safe`, `push` and `remote-gone` (ruling D-D): a
  deleted upstream now fills `upstream`, and `push` refuses a `remote-gone`
  branch with refusal reason `remote-gone`, exit 2, instead of republishing
  it; `push` and `delete-branch` refuse with `inspection-incomplete`,
  `inspect-cap`, or `deadline-exceeded`, exit 2, when their re-inspection is
  incomplete. Decided by the proposal: Batch "One mutation seam", which said
  both keep their behavior apart from argument resolution, and the
  batch-only baseline changes of Batch, Overview, and the packet overview.
- `add-project-clean-all-safe`, the Git child runner (ruling D-G): Git
  children run through a new bounded runner, `Popen(start_new_session=True)`
  per child with a scrubbed environment and output streamed as bytes, and
  `probe()` stays for non-Git children; abandonable filesystem calls run on
  daemon threads, never on a `concurrent.futures` pool, and `preexec_fn` is
  never used. Decided by the proposal: the bare-name item of "Baseline
  behavior changes" in Batch and Overview, which said the proposal gives
  `probe()` a timeout argument; C4 below corrects the rest.
- `add-project-overview`, the repository gate (ruling D-J, amended after
  lane openRepoProject-3's finding L2): the gate also withholds `--all-safe`
  while the repository has an unprobed worktree row, its classification
  null because the 512-row cap or the deadline cut it, because the batch
  plan is then not known to be complete; `target-cap` does not withhold it,
  because the batch preview is complete and lists every row that passes
  every gate before the two index gates. The gate still changes suggestions
  only. Decided by the proposal: Overview "Attention categories" and
  "Repository identity and the clean handoff", the synthesis's handoff and
  gate text, the packet overview's goals table and handoff text, and the
  "Overview gates" bullet above.
- `add-project-overview`, the withheld-suggestion reason (ruling D-P), a
  departure from the project row and finding object of Overview "JSON
  contract": a new field, `suggestion_gate`, beside `suggested_command` in
  the overview row and the finding, carries an existing code
  (`inspection-incomplete`, `inspect-cap`, `scan-limit`,
  `deadline-exceeded`, `target-not-repository-root`, or
  `unsupported-path-bytes`) naming the gate that withheld or limited a
  suggestion. A repository of 129 to 256 worktree rows keeps the plain
  read-only `project clean <root>` suggestion, with
  `suggestion_gate: "inspect-cap"` only on a `merged-removable` finding
  whose `--all-safe` was withheld; over 256 rows every read-only suggestion
  carries `inspect-cap`, because the report itself would be incomplete.
  Decided by the proposal: Overview "Attention categories" names the field,
  and the packet overview and the synthesis mention it; the field tables and
  fixture of Overview "JSON contract" do not list it.
- `add-project-overview`, findings on the merge-target checkout (ruling
  D-I): on a `protected-default` checkout the `dirty`, `diverged`,
  `unpushed`, and `remote-ahead` findings carry `suggested_command: null`
  and never set the row's suggestion, because `project clean` offers no
  action for that checkout; the last three are the proposal's drift
  findings for that checkout. Decided by the proposal, as a deliberate
  narrowing of the attention table's per-code suggestions: Overview
  "Attention categories".
- `add-project-overview`, manifest refusals: a `Refused` from `manifest()`,
  for an unreadable or a wrong-kind manifest, is a `manifest-invalid` row
  error with exit 1 in the overview; the `project-review-safety` exit 2 for
  an undecodable manifest applies to `clean`, not to an overview row.
  Decided by the proposal: Overview "Collector boundary and error
  isolation" and **One helper failure is isolated.**
- `add-project-overview`, the shared model (ruling D-M): the overview reads
  the shared evidence model through change 1's canonical `project-command`
  requirement and states its own 60 s deadline. No packet sentence changes.
- Both changes, measurement (ruling D-Q): the caps stay provisional in the
  spec deltas, and `tasks.md` carries a warm- and cold-cache measurement on
  a Linux file-system path, never `/mnt/c`, before the Speckit handoff.
- `add-project-clean-all-safe`, `update --apply` (ruling D-R): it refuses
  unless the root's and every child's `dirty` is exactly `false`.
- `add-project-clean-all-safe`, `doctor` and `status` on unknown state
  (ruling D-S, narrowed by lane openRepoProject-2 on 2026-10-09): they
  report a failed status probe instead of exiting 2, and `doctor` renders as
  an error check row only a null that means "not established" (a `present`
  null, a `dirty` null left by a failed probe, any row classified
  `inspection-error`), never a null that means "none" (`upstream`, `ahead`,
  and `behind` for a branch with no upstream; `merged_into_target` for a
  detached head). The overview's inherited rule is the same. The proposal
  lists this as a baseline behavior change.

### Corrections and review constraints — 2026-10-08

The proposals' alignment reviews and lane openRepoProject-3's fidelity reads
also found errors and omissions in the packet's account of `a040790`, and
limits on how the design can be built and tested. Each correction was
checked against `project` at `a040790`, and the packet text now carries it.

- Baseline (C1): `origin/main` is `da33d92`, which merged PR #7 on
  2026-10-07, so the `origin/main` commit the packet named is stale and
  PR #7 is merged, not open. The cleanup-branch commit lists of the packet
  overview and both feature documents now name all six harvest commits:
  `5fc2b51`, `acf0133`, `80fdef3`, `1789ad9`, `09af8c8`, and `bb91a49`.
- Doctor health follow-up (M2): the follow-up to absorb `acf0133` and
  `80fdef3` is discharged by `add-project-overview` (issue #10, draft PR
  #12), which absorbs them as local-only read-only reporting; "Current
  state" above and the packet overview say so, and the overview design does
  not absorb them itself.
- `remote-gone` (C3): doctor classifies no worktree at `a040790`; its
  `check_rows` reports no classification, and `repo_state` sets only
  `stale-worktree`. Overview and clean classify a deleted upstream
  `remote-gone`; doctor reads the same evidence but reports no
  classification.
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
  merge-target branch first and would read such a row as
  `protected-default`. Overview "Repositories and linked worktrees" and
  "Merge target and classification reuse" and Batch "Worktree-specific
  probes" now state the case, so the passages that assume
  `inspection-error` stand.
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
