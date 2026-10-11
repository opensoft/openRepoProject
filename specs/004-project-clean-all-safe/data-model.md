Lane: openRepoProject-2

# Data Model: Safe batch worktree cleanup

Nothing is stored. Every `project clean` run builds its plan fresh and never
stores or reuses it (FR-025); these are the values one invocation reads,
derives and reports. JSON shapes are in
[contracts/project-clean.md](contracts/project-clean.md); exact human text is
`design.md` D18 and D14. Line citations are at `961c405`.

## Entities

### Repository identity (D7, D8; FR-016, FR-017, FR-055)

| Field | Source |
| --- | --- |
| `root` | realpath of the main worktree, decided in D8's order; also the envelope's `root` and the command directory |
| `common_dir` | realpath of row 3's `--git-common-dir`; never a worktree row |
| `dev`, `ino` | `lstat` of `common_dir`, not following a symlink |
| `root_valid_utf8`, `common_dir_valid_utf8` | the escaping rule; always true in `clean` |

Validation: an absolute argument's realpath must equal `root`, and `root`
must be the main worktree; a bare repository, a submodule checkout and a
linked worktree whose main checkout cannot be named refuse with
`target-not-repository-root`; a `root` or `common_dir` that is not valid
UTF-8 refuses with `unsupported-path-bytes` before any plan or digest. The
four identity fields go into the plan and its digest, and are compared at
every revalidation and first in every rescan; `dev` and `ino` are host-local,
so a remount that renumbers them fails closed.

### Merge target (D8; FR-018, FR-060)

| Field | Value |
| --- | --- |
| `name` | the first candidate that exists as a local branch |
| `source` | `manifest`, `origin-head`, `main` or `master` |
| `sha` | the branch's head from row 6 when the plan is built |

Candidates, in order: the manifest's `tracking_branch` less a leading
`origin/`; the symref of `refs/remotes/origin/HEAD` less
`refs/remotes/origin/`; `main`; `master`. The manifest is read at `root` by
one bounded filesystem call: an `st_size` over 1 MiB is `manifest-invalid`
without a read, and an unreadable manifest or a wrong kind is
`manifest-invalid` too. No candidate refuses with `no-merge-target` and its
baseline message (`project:551`). A manifest and `origin/HEAD` naming
different existing branches: the manifest wins, with the plan note
`merge-target-conflict`.

### Worktree row (FR-006, FR-042, FR-056, FR-057)

One registry entry, the main worktree included. Baseline keys keep their
names and types; the last six are added.

| Field | Value | Null means |
| --- | --- | --- |
| `path` | the registered path, from the NUL-delimited registry | never null |
| `present` | true; false when `lstat` fails with `ENOENT` | any other `lstat` failure (with an `os-error`) |
| `branch` | short name, or `detached` | (baseline) |
| `head` | full object name | not established |
| `upstream` | configured short name, also when its remote-tracking ref is gone | none configured |
| `remote_present` | false when the track is `gone` | none configured, or not established |
| `ahead`, `behind` | from the track field | none configured, ref gone, or not established |
| `dirty` | from the combined probe | probe not run, failed or timed out |
| `ignored_files` | ignored records read; a lower bound when truncated | probe not run or failed, or stopped before any ignored record |
| `current` | the working directory is inside it (baseline) | |
| `merged_into_target` | head is in row 7's merged set | detached, or not established |
| `classification`, `recommendation` | the ladder below; the recommendation keeps its baseline text | |
| `locked` | from the registry's `locked` attribute | never null |
| `ignored_files_truncated` | the probe stopped at a bound | probe not run or failed |
| `ignored_samples` | at most 8 `{path, path_valid_utf8}`, paths relative to the worktree | probe not run or failed |
| `path_valid_utf8` | the path is valid UTF-8 | never null |
| `errors` | `{code, message, path?, path_valid_utf8?}`: `os-error`, `probe-failed`, `probe-timeout`, `deadline-exceeded` | |
| `notes` | `partially-removed` (D4) or empty | |

Null means unknown or not established, never a default false or 0, in every
field this change adds (FR-043, FR-045); `upstream`, `ahead`, `behind` and
`merged_into_target` keep their baseline "none" meaning where the table says
so, which doctor never reports as an error (FR-051).

### Worktree identity and registration (D7; FR-055)

`{path, dev, ino, admin_id}` together, recorded for each selected row. The
registration holds in both directions between realpaths: `<path>/.git` is a
regular file whose `gitdir:` line names `<common_dir>/worktrees/<admin_id>`,
and that directory's `gitdir` file names `<path>/.git`, relative values
resolved against the directory holding the file. A row whose registration
disagrees gets no status probe and is `inspection-error`, excluded as
`registration-mismatch`.

### Branch evidence (D6, D7)

`{branch, head, upstream, upstream_oid, ahead, behind}` from row 6, recorded
for each selected row. For a branch whose configured upstream's
remote-tracking ref was deleted, `upstream` is the short name and
`upstream_oid`, `ahead` and `behind` are null; at revalidation a value null
in the plan and null again is no difference, and one that reappears is
`state-changed` (D7, D20).

### Classification (D6; FR-007)

First, a row whose evidence could not be established (`present` null, a
registration that disagrees, a status probe that failed or timed out) is
`inspection-error` directly, whatever its branch, so a failed probe on the
merge-target checkout is never `protected-default`. Every other row takes the
first rung that holds, in this order (names unchanged; the one reorder is
marked):

| Rung | Holds when |
| --- | --- |
| `stale-worktree` | `present` is false |
| `protected-default` | `branch` is the merge target |
| `inspection-error` | `dirty` is null |
| `dirty` | `dirty` is true |
| `ignored-local-files` | `ignored_files` is non-zero |
| `detached` | `branch` is `detached` |
| `unpublished` | no upstream configured |
| `remote-gone` | `remote_present` is false; but first (the reorder) a merged row is `merged-removable`, or `merged-current` when it is current |
| `review-required` | defensive; no value of the evidence model reaches it |
| `diverged` | `ahead` and `behind` both positive |
| `remote-ahead` | `behind` positive |
| `unpushed` | `ahead` positive |
| `merged-removable` | merged and not current |
| `merged-current` | merged and current |
| `pushed-unmerged` | otherwise |

The ladder is a pure function of the row (OQ-28). The partial-removal note is
added after it by a separate function (D4): a present, registration-verified,
`dirty` linked worktree whose status records read are all tracked-file
deletions (`" D"`), judged on the records read when the stream stopped at its
bound. It changes no class, rung or gate.

### Gate (FR-020 to FR-023; D10, D12, D13)

A row is selected only when it passes every gate; an excluded row's `reason`
is its first failing gate:

| Order | Reason | Fails when |
| --- | --- | --- |
| 1 | `main-worktree` | the row is the main worktree |
| 2 | `unsupported-path-bytes` | the path is not valid UTF-8 |
| 3 | `registration-mismatch` | the two-way registration disagrees |
| 4 | `locked-worktree` | `locked` is true |
| 5 | the classification | the class is not `merged-removable` |
| 6 | `not-requested` | single mode, an eligible row other than P |
| 7 | `unstarted-branch` or `reflog-unavailable` | the reflog rule below |
| 8 | `deferred-target-cap` | beyond the first 16 rows that passed gates 1 to 7 |
| 9 | `contains-submodule` | a gitlink in the row's index, or `modules` in its admin directory |
| 10 | `hidden-local-state` | an index entry flagged assume-unchanged or skip-worktree |

Gates 9 and 10 read the row's own index, inside its worktree, only for rows
that passed gates 1 to 8; at most 16 rows reach them. A row an index gate
excludes keeps its place among the 16.

### Reflog anchor and movement (D10; FR-021, FR-022)

Read from `logs/refs/heads/<branch>` under `common_dir`, at most 64 KiB, by a
filesystem call (never a Git child). Each line is `<old> <new> <identity>
<time> <zone>`, then a tab and a message when there is one.

- Anchor: the last surviving entry whose old object is all zeros, or whose
  message begins `branch: Created from` or `branch: Reset to`.
- Movement: an entry after the anchor, or any entry when no anchor survives,
  whose old and new objects are non-zero and differ (a rename's are equal).

| Outcome | When (first that holds) |
| --- | --- |
| `reflog-unavailable` | missing (`ENOENT`, `ENOTDIR`), 0 bytes, or read to the 64 KiB bound |
| `inspection-error` | any other error on the read |
| unprobed (`inspection-incomplete`) | the read did not finish within the filesystem budget |
| `reflog-unavailable` | the last entry's new object is not the head |
| pass | a movement survives |
| `unstarted-branch` | an anchor survives with no movement after it, its new object the head |
| `reflog-unavailable` | anything else, no anchor and no movement included |

### Plan (FR-003, FR-019, FR-024, FR-025, FR-031, FR-032; D12 to D14)

What one invocation would do in one repository. Built fresh by every run.

| Mode | Spelled | Row cap | Selection |
| --- | --- | --- | --- |
| `report` | plain `project clean`, with or without `--json` | 256 | what `--all-safe` would select at 128 rows or fewer; null above 128, with the note `inspect-cap` and `rows` |
| `all-safe` | `--all-safe`, preview or `--apply` | 128 | every row passing every gate, at most 16 |
| `single` | `--apply --action remove --worktree P`; also push and delete-branch for the cap and bounds | 128, P exempt and probed first | P alone |

Fields: identity, merge target, `worktrees`, `selected`, `excluded`,
`omitted` (`{count, exactness: "exact"}`), `notes`, `completeness`,
`apply_allowed`, `refusals`, `plan_digest` (R12 in research.md), `limits`,
`budget`, `probes` and `operations`. `probes` counts every Git child other
than a removal and `operations` the removals, each child once (lead ruling
R-27; research.md R8). Rows are ordered main worktree first, then by raw path
bytes; `selected`, `excluded` and the execution order are by raw path
bytes.

Completeness: a plan is `incomplete` when the row cap is exceeded
(`inspect-cap`), a repository-wide probe failed or a row is
`inspection-error` (`inspection-incomplete`), or the deadline passed while
planning (`deadline-exceeded`). In single mode those three are non-blocking
notes about other rows, and only P's own row and the repository-wide probes
decide (D13). In report mode above 128 rows, the `inspect-cap` note alone
does not make it incomplete. `apply_allowed` is false for every report and
for any plan that is incomplete or carries a refusal.

### Refusal (FR-043)

`{code, message, path?, path_valid_utf8?, reason?}`. `path_valid_utf8` is
present exactly when `path` is; `reason` only on `target-excluded`. The
eighteen codes and their phases are in the contract. A resolve refusal prints
the extended error object; a plan or select refusal prints the plan with
`apply_allowed: false`.

### Target result and reconciliation record (FR-034, FR-035; D19)

One per selected target, in canonical order: `path`, `path_valid_utf8`,
`branch`, `planned_sha`, `stage`, `reason`, `notes`, `command` (the planned
argument vector, present even when nothing ran), `exit_status`,
`probes_performed` and `reconciliation`.

`exit_status` is null unless a child was spawned and reaped; a child ended by
a signal that `project` did not send has 128 plus the signal number.

`reconciliation` is an object on every `removed`, `refused`, `failed` or
`unknown` target and null on a `not-attempted` one:

| Field | Value |
| --- | --- |
| `registry_entry_present` | the registry still lists the planned path; true, false or null |
| `path_present` | `lstat` of the planned path succeeds; false only on `ENOENT` or `ENOTDIR`; null on any other error or a timeout |
| `branch_present`, `branch_sha` | from the ref listing |
| `reconciled` | true only when the three presence fields are non-null and `branch_sha` is non-null whenever `branch_present` is true |

The rescan first re-establishes the repository identity; where it differs,
every field is null and `reconciled` is false. A `refused` target's values
come from the revalidation scan that refused it; a spawned target's from the
rescan after the child is reaped. Target notes: `orphaned-directory` (entry
gone, path present) and `partially-removed` (a child killed at the ceiling,
or whose exit was not observed, left its entry or path).

### Apply result record (FR-044)

`schema_version`, `observed_at`, `repository`, `merge_target`,
`plan_digest`, `probes`, `operations`, `targets`, `exit_code`,
`completeness` (complete when every target whose `reconciliation` is an
object has `reconciled: true`).

### Residual window (D7; FR-048)

Ignored files created and index flags set after the last revalidation, and
any change after Git's own check. Stated in one line (D18) in the
confirmation and in the result.

### Root and leg state outside `clean` (D16; FR-050 to FR-052)

Each root, leg and nested member keeps its baseline dict. A directory with no
`.git` is `present: false` with no Git child. A present one that cannot be
inspected (an old, missing or unusable Git, a failed or timed-out status
probe) adds `classification: "inspection-error"` and `errors` (`git-too-old`,
`git-unavailable`, `probe-failed`, `probe-timeout` or `os-error`), with
`present` null when the version check failed and every value not established
null; an inspected dict has neither field. Every `path` gains
`path_valid_utf8`, every `root` gains `root_valid_utf8`, and
`ignored_samples` entries are objects. A deleted upstream shows its short
name with `ahead` and `behind` null.

## States of a `project clean` run

| State | Meaning |
| --- | --- |
| resolving | arguments checked, `git --version` run, the argument resolved, the merge target found |
| planning | rows inspected under the deadline, caps and budgets; gates applied |
| reported | a preview or report printed; the run ends |
| asking | the removal question is on the human stream (`--apply` without `--yes`) |
| applying | the apply phase: per target, revalidate, spawn, wait, rescan |
| reconciling | the final rescan within the reserve; the record printed |
| refused | a refusal; nothing mutated, exit 2 |
| cancelled | a signal before the apply phase, or end of input at the question |

### Transitions

| From | Event | To |
| --- | --- | --- |
| (start) | invalid argument combination; parser usage error | refused (exit 2; a usage error prints no JSON) |
| resolving | Git missing, unusable or older than 2.36; a resolve refusal | refused |
| resolving | resolved | planning |
| planning | an unexpected exception | refused (`internal-error`) |
| planning | preview or report built | reported (exit 0 complete, 1 incomplete) |
| planning, `--apply` | incomplete; then `--expect-plan` mismatch | refused (exit 2), in that order |
| planning, `--apply` | complete `all-safe` plan selecting nothing | reported (`No eligible worktrees`, exit 0, no question) |
| planning, single | P matches no entry; a gate excludes P | refused (`worktree-not-found`; `target-excluded`) |
| planning, `--apply` | standard input not a terminal, no `--yes` | refused (`confirmation-required`) |
| planning, `--apply` | `--yes` | applying |
| planning, `--apply` | otherwise | asking |
| asking | `yes` | applying |
| asking | any other answer | refused (`cancelled`) |
| asking | end of input, SIGINT, SIGTERM, SIGHUP | cancelled (130, 130, 143, 129) |
| resolving, planning | SIGINT, SIGTERM, SIGHUP | cancelled (130, 143, 129; probe groups killed and reaped) |
| applying | a target ends a plain `removed` and another follows | applying (next target) |
| applying | a target ends otherwise, the last target ends, a signal or the deadline | reconciling |
| reconciling | record printed | exit by the table below |

### Target stages

`pending` (printed plan and progress only) leads to exactly one final stage:

| Stage | Reasons |
| --- | --- |
| `removed` | null, `branch-advanced-after-removal`, `branch-missing-after-removal`, `removal-ceiling` |
| `refused` | `identity-changed`, `branch-changed`, `state-changed`, `contains-submodule`, `hidden-local-state` |
| `failed` | `git-refused` (128), `git-failed` (any other status), `spawn-error` |
| `unknown` | `unconfirmed-removal`, `reconciliation-incomplete`, `internal-error`, `removal-ceiling` |
| `not-attempted` | `batch-stopped`, `interrupted`, `deadline-exceeded` |

A child that exits nonzero on its own is `failed`, signal or not; only a
child killed at the 300 s ceiling, or whose exit was not observed, is decided
by the rescan between `removed` and `unknown`. No target is retried.

## Exit statuses

A run with `--apply`, first matching row (FR-037, D19):

| Exit | When |
| --- | --- |
| 130, 143, 129 | a signal was received, the first deciding; 130 when input ended at the question |
| 1 | the deadline stopped work after the apply phase began, any target is `unknown`, or any reason is `removal-ceiling` |
| Git's own status | a target is `failed` with `git-refused` or `git-failed`, passed through even when it equals one of `project`'s own |
| 2 | any refusal; a `refused` target; `removed` with a branch-after-removal reason; `failed` with `spawn-error` |
| 0 | every selected target `removed` with reason null, or nothing eligible |

A preview or report: 2 only for a refusal raised before a plan is built, 1 for
an incomplete plan, 0 otherwise, and 130, 143 or 129 when a signal ends it.
Push and delete-branch pass their child's status through (128 plus the signal
number for a signal death) and exit 2 for a refusal. `status` keeps 0; `doctor`
exits 1 on an `error` check row, its rule unchanged; `update --apply
--component shape` or `bench` exits 2 when any `dirty` is not exactly false.

## Constants

| Name | Value |
| --- | --- |
| Git floor | 2.36 |
| deadline, reserve, work deadline | 60 s, 10 s, 50 s (time at the question not counted) |
| per Git child, per filesystem call | `min(5 s, work remaining)`; rescans `min(5 s, reserve remaining)` |
| per Git child in `status`, `doctor`, `update` | 15 s; no deadline, no row cap |
| grace, reap wait | 2 s, 2 s |
| removal floor, ceiling | 5 s of work deadline left; 300 s after spawn |
| row caps | 128 (`all-safe`, `single`), 256 (`report`) |
| targets per run | 16 |
| ignored entries, status records, samples | 64, 4,096, 8 |
| reflog read, manifest read | 64 KiB, 1 MiB |
| revalidation, final rescan | at most 5 and 3 Git children |

The timing values live in one module-level table (research.md R10); `budget`
and `limits` report the values in force.
