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
`a040790`: `origin/main` has since advanced to `67efa80` (PR #4), which
archives the completed OpenSpec changes, promotes their specifications to
`openspec/specs/`, and leaves the `project` executable unchanged.

| Finding | Decision | Contract | Proving scenarios |
| --- | --- | --- | --- |
| 1. Define the batch safety boundary | The guarantee is narrowed: concurrent writers are outside the safe contract, and a removal child is spawned only when the repository identity `{root, common_dir, dev, ino}`, the worktree identity `{path, dev, ino, admin_id}` with two-way admin registration, the branch evidence, every baseline signature field, the `locked` flag, the absence of hidden local state (an index entry flagged assume-unchanged or skip-worktree, found by a bounded `git ls-files -v -z`), and the merge target `{name, source, sha}`, re-resolved from a fresh manifest read, still equal the confirmed plan at revalidation; otherwise the target is `refused` (`identity-changed`, `branch-changed`, `state-changed`, or `hidden-local-state`), no later target is attempted, and the exit is 2. The removal runs as `git -c status.showUntrackedFiles=normal -C <command directory> worktree remove <path>`, so Git's own non-force check sees untracked files whatever the user's configuration; ignored files created and index flags set after revalidation are the documented residual window. A branch change seen only after removal is `removed` with `branch-advanced-after-removal` (or `branch-missing-after-removal`), exit 2, and the branch retained. | Batch, "Eligibility and merge-target terminology"; "Safety boundary": "Identity", "The narrow guarantee", "Changes after confirmation", "Residual window", "Branch race"; "Probe accounting and limits": "Worktree-specific probes", "Preflight and targeted revalidation" | Batch: **Hidden local state.**, **Target directory replaced.**, **Admin registration changed.**, **Parent directory swapped.**, **Repository replaced mid-batch.**, **New worktree and pre-removal changes.**, **State changes before revalidation.**, **Changed later target.**, **Untracked file under `status.showUntrackedFiles=no`.**, **Ignored file in the residual window.**, **Branch advances before removal.**, **Branch advances after removal.** |
| 2. Make execution and interruption reconcilable | `--apply` always recomputes, prints, and confirms a fresh plan carrying `plan_digest`, and an optional `--expect-plan` refuses a differing one with `plan-digest-mismatch`. Single-target `remove` is strictly a one-item batch on the shared `retire_worktree` seam (revalidate, spawn, reap, reconcile): the same full plan (`mode: "single"`) under the same caps, the refusals `worktree-not-found` and `target-excluded`, and `inspection-incomplete` when any row is `inspection-error`. One monotonic 60 s deadline holds back a 10 s reconciliation reserve, so work stops at 50 s, with 5 s per probe and every filesystem call in a worker thread; SIGINT or expiry terminates and reaps the child's process group before a rescan. Every target ends in the stage enum `pending`, `removed`, `refused`, `failed`, `unknown`, or `not-attempted` with a reconciliation record (`registry_entry_present`, `path_present`, `branch_present`, `branch_sha`, `reconciled`); `removed` needs rescan evidence and `reconciled: true`; an unproven outcome, or an exception after the apply phase begins, is `unknown` with exit 1; and a `failed` target (`git-refused` for exit 128, `git-failed` for any other status such as 255 with an `orphaned-directory` note, or `spawn-error`) exits with Git's own status, or 2 for `spawn-error`. | Batch, "Execution model": "Fresh plan and plan digest", "One mutation seam", "Deadline and budgets", "Interruption and expiry", "Stages and reconciliation", "Exit codes"; "Repository and JSON contract": "Apply result record"; "Baseline behavior changes"; "Partial completion and recovery" | Batch: **Deadline expiry mid-batch.**, **Exit 0 without evidence.**, **SIGINT.**, **Git leaves an orphaned directory.**, **Git refuses the removal.**, **Unreadable path after removal.**, **Exception after the apply phase begins.**, **Single target equals a one-item batch.**, **Preview is advisory.**, **Plan digest mismatch.** |
| 3. Bound and share the expensive work | Both documents use one probe set: one `git --version` per invocation; per repository, memoized by `common_dir` and fanned out, the same four repository-wide children (identity, registry listing, ref listing in one shared NUL-separated `for-each-ref` format, and merged set); and per present, registration-verified worktree row, the main worktree included, one combined status probe that stops at a 65th ignored record or a 4,097th record. Batch revalidation is a targeted check of at most five children plus a manifest re-read, and `probes` and `operations` (`{estimated, performed}`) appear in both the plan and the apply result record. Candidates and registry entries are sorted before any cap, and dropped work is reported as `omitted: {count, exactness}`. The caps follow one rule, the largest values whose worst case fits at 150 ms per Git child, a 1.5× margin over the assumed 100 ms: the batch inspects at most 128 worktree rows (`limits.worktree_rows`, the main worktree included) and selects at most 24 targets, serially within its 50 s work deadline; the overview takes at most 32 roots, 128 candidates, and 512 worktree rows with four concurrent children across repositories within 55 s. A cap hit or deadline gives an incomplete result (`inspect-cap`, `inspection-incomplete`, or `deadline-exceeded` in the batch; `scan-limit`, `probe-timeout`, or `deadline-exceeded` in the overview). | Batch, "Execution model": "Deadline and budgets"; "Probe accounting and limits": "Repository-wide probes", "Worktree-specific probes", "Preflight and targeted revalidation", "Cap arithmetic", "Inspection order and omitted work", "Bounded ignored-file inspection", "Probe and operation estimates". Overview, "Discovery scope and ordering": "Ordering, truncation, and omitted counts", "Caps and their arithmetic"; "Probe model and deadline": "Git version check", "Repository-wide probes", "Worktree-specific probes", "Scheduling and concurrency", "Deadline and timeouts", "Probe accounting"; "Deferred remote inspection boundary" | Overview: **One probe set per repository.**, **Candidate cap after sorting, exact count.**, **Candidate cap with an incomplete listing.**, **Root and worktree-row caps.**, **Probe timeout.**, **Hung filesystem call.**, **Invocation deadline.**, **Bounded concurrency.**, **Bounded ignored files.**, **User status configuration.**, **Git version refusal.**, and the remote item under "Deferred validation scenarios". Batch: **Row cap and planning failures.**, **Target cap.**, **Ignored-file bound.**, **Bounded revalidation work.** |
| 4. Make the repository and JSON contracts explicit | The command directory is the canonical, identity-checked `repository.root` (or `common_dir` for a bare repository) with no merge-target worktree requirement. Every `project clean` mode resolves an absolute path Git-first and refuses `target-not-repository-root` with exit 2 unless it is exactly a main worktree root; a relative path or no argument resolves to the repository Git finds there; only a bare name keeps the `discover` lookup, its Git child counted and bounded; and the report's `root` always names the command directory. The overview prints a new `schema_version: 1` envelope with typed project-row, worktree-row, finding, and `summary` fields; the batch plan is an additive superset of the baseline clean report with `limits`, `budget`, `probes`, and `operations`; the apply result record is defined and rendered as human text; both documents state representation rules with fixtures; a non-UTF-8 `repository.root` or `common_dir` refuses with `unsupported-path-bytes`; an unreadable or wrong-kind manifest is `manifest-invalid`; `suggested_command` is `null` unless a finding supplies one, and otherwise a JSON argv array naming the canonical root; and both documents list their baseline behavior changes. | Batch, "Repository and JSON contract": "Command directory and repository resolution", "Representation rules", "Plan envelope", "Refusal codes", "Apply result record", "Fixtures", "Machine-readable apply results"; "Baseline behavior changes". Overview, "JSON contract": "Envelope", "Project row", "Finding object", "Representation rules", "Repository identity and the clean handoff", "Path encoding", "Fixture"; "Result semantics"; "Baseline behavior changes" | Batch: **Overview handoff keeps identity.**, **Absolute path that is not a repository root.**, **Non-UTF-8 repository root.**, **Merge target missing, invalid, or conflicting.** Overview: **Canonical identity through the handoff.**, **Independent clones and aliases.** |
| 5. Close discovery scope and acceptance gaps | A `family.yaml` holder is one `family-holder` row counted once, with `relationships: []` and Git probes only when its own directory is the toplevel. A marker check that fails with anything but `ENOENT` or `ENOTDIR` makes an error row with `kind: null`; `collect(candidate) -> result` turns helper exceptions (such as `manifest-invalid`, `os-error`, or `internal-error`) and failed or timed-out probes into error rows while the scan continues, and path candidates never pass through `discover`. A missing merge target becomes `merge_target: null` with a `no-merge-target` finding and no `cleanup_report` call. A `merged-removable` worktree yields the housekeeping finding and the `--all-safe` suggestion only after the batch's main-worktree, path-byte, registration, and lock gates, and otherwise the first failing gate's finding (`main-worktree`, `unsupported-path-bytes`, `registration-mismatch`, or `locked-worktree`, the batch's own exclusion reasons); a fifth gate withholds every `--all-safe` suggestion for a repository while any of its worktree rows is `inspection-error`, because the batch plan would be refused as `inspection-incomplete`, so its housekeeping findings and the row suggest only the read-only `project clean <root>`. `review-required` is covered by a classifier test on an injected row; paths are read NUL-delimited, with a non-UTF-8 path escaped and excluded as `unsupported-path-bytes`; and every acceptance scenario the finding listed is written. | Overview, "Discovery scope and ordering": "Candidates", "Repositories and linked worktrees", "Family holders"; "Collector boundary and error isolation"; "Merge target and classification reuse"; "Attention categories"; "JSON contract": "Path encoding"; "MVP validation scenarios". Batch, "Eligibility and merge-target terminology" | Overview: **Family holder count, relationships, and probe ownership.**, **Unreadable candidate directory.**, **One helper failure is isolated.**, **Manifest target.**, **`origin/HEAD` target.**, **`main` target.**, **`master` target.**, **Conflicting targets.**, **Missing target.**, **Every protected classifier.**, **Gated merged worktrees.**, **Attention filter per category.**, **Present eligible external worktree.**, **Missing external worktree.**, **Unreadable external worktree.**, **Control and format characters in paths.**, **Non-UTF-8 path.**, **Canonical identity through the handoff.**, **Local and read-only.** Batch: **Stable order and preserved work.**, **Every protected classifier.**, **Paths and empty plans.**, **Control-character and non-UTF-8 paths.**, **Merge target missing, invalid, or conflicting.** |

### Cross-document decisions

- Narrow guarantee: concurrent writers are outside the safe contract. The MVP
  claims no lock, lease, or writer-quiescence handoff, refuses on any change
  it observes at revalidation, and documents the residual window for ignored
  files created, and index flags set, after it.
- Removal command: single-target and batch removal both pass
  `-c status.showUntrackedFiles=normal` to the non-force
  `git -C <command directory> worktree remove <path>`, so Git's own check
  sees untracked files under any user configuration.
- Hidden local state: batch cleanup never removes a worktree whose index
  flags an entry assume-unchanged or skip-worktree. A bounded
  `git ls-files -v -z` probe finds it for rows that pass every other gate, at
  plan time and at revalidation, so sparse checkouts are excluded; the
  overview does not run it.
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
  repository is `inspection-error`, which would make the batch plan
  `inspection-incomplete`; otherwise the read-only `project clean <root>` is
  suggested. The batch may still exclude a suggested worktree as
  `hidden-local-state`.
- Shared probes: one version check per invocation, the same four
  repository-wide children per repository (identity, registry listing, ref
  listing, and merged set) with one identical ref-listing format, and one
  combined bounded probe per worktree row,
  `git status --porcelain=v1 -z --untracked-files=normal --ignored=matching`,
  in both documents. All Git output is parsed NUL-delimited.
- Caps by one rule at 150 ms per Git child, a 1.5× margin over an assumed
  100 ms that the proposal must measure: the batch inspects 128 worktree
  rows, the main worktree included, and selects 24 targets within its 50 s
  work deadline (Batch "Cap arithmetic"); the overview takes 32 roots, 128
  candidates, and 512 worktree rows within 55 s with four concurrent children
  across repositories (Overview "Caps and their arithmetic"). Both name the
  row cap `limits.worktree_rows`. They replace the earlier 1,024/100 and
  256/1,024 figures, which could not meet the deadline.
- Concurrency: the overview runs at most four read-only Git children across
  distinct repositories and never two once their `common_dir` is known to be
  the same (`probe_concurrency: 4`); batch probing is serial
  (`probe_concurrency: 1`).
- Codes: `deadline-exceeded` and `probe-timeout` for the two time limits,
  and `manifest-invalid`, `git-unavailable`, and `git-too-old` (Git older
  than 2.36, exit 2 before any repository probe), with the same spelling in
  both documents.
- `remote-gone`: the shared ref listing reports a deleted upstream as `gone`,
  so overview, doctor, and clean all report `remote-gone` where `a040790`
  reports `unpublished`; both are preserve states.
- `ignored_files` keeps its baseline name and type but counts the ignored
  records read, a lower bound when `ignored_files_truncated` is true.
- `plan_digest`: the SHA-256 of the repository identity, the merge-target
  name and SHA, and the canonically ordered selected path, branch, and head.
  The optional `--expect-plan` refuses a differing fresh plan with
  `plan-digest-mismatch` and exit 2.
- Baseline behavior changes: both documents carry the section, and the
  [packet overview](project-maintenance-overview.md) lists their union.

### Open proposal decisions

These remain open; the [packet overview](project-maintenance-overview.md)
carries the same consolidated list.

- The measured per-child and per-removal costs, and therefore the final caps
  under the shared rule; batch cleanup lowers its target cap first.
- Caps versus concurrency: if the overview's four-way concurrency is
  rejected, its fallback is 32 candidates and 128 worktree rows (257
  children, about 38.6 s at 150 ms); above about 214 ms per child even
  concurrency needs lower caps.
- Whether to cap worktree rows per repository, since one repository with
  more than about 360 worktree rows cannot complete at 150 ms per child.
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
- Whether bare repositories are supported or refused.
- Whether SIGTERM and SIGHUP receive the SIGINT treatment.
- Whether the `attention` alias merits a separate command, and how
  `--attention --json` filters.
- Whether suggested commands also carry a display string, and whether the
  extra `dirty` finding for a dirty default-branch checkout is wanted.
- The final command and flag spelling.
- Whether cache disposal, paired branch retirement, and the remote, family,
  bench, container, and park integrations deserve separate changes.

### Checks

- Packet validator: PASS, printing
  `PASS: 4 docs (2 atomic, 1 synthesis, 1 overview)` for the command below.
- `git diff --check`: clean.
- Adversarial review round 1: 6 high / 14 medium / 15 low findings, all high
  and medium resolved in the fix round; verification review: pending; result
  recorded in the PR.

```sh
python3 -I ~/.claude/skills/document-software-brainstorm/scripts/validate_packet.py \
  --root ideation/brainstorm --packet-prefix project-maintenance
git diff --check
```

The completion gate above is not yet met: the verification review is
pending, and the revision is not yet committed or pushed.
