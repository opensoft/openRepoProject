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

Where `root` is null, rows 6 and 7 run in the common directory for a bare
repository and otherwise where row 3 ran. Row 4, the registry listing, runs
where row 3 ran in every layout, since the main worktree is not yet known
when it runs. For a bare repository that is equivalent to running it in the
common directory: `git worktree list --porcelain -z` reads the same registry
from a linked worktree and from the common directory and prints the same
bytes (checked on Git 2.43.0), so the code keeps row 4 where row 3 ran
(lead ruling R-68, lane 4's note; evidence follow-up 2 may move it).

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
| `present` | true; false when `lstat` fails with `ENOENT` or `ENOTDIR` | any other `lstat` failure (with an `os-error`) |
| `branch` | short name, or `detached` | (baseline) |
| `head` | full object name | not established |
| `upstream` | configured short name, also when its remote-tracking ref is gone | none configured; not established for a branch named `HEAD` (below) |
| `remote_present` | false when the track is `gone` | none configured, or not established, a branch named `HEAD` among them |
| `ahead`, `behind` | from the track field | none configured, ref gone, or not established |
| `dirty` | from the combined probe | probe not run, failed or timed out |
| `ignored_files` | ignored records read; a lower bound when truncated | probe not run or failed, or stopped before any ignored record |
| `current` | the working directory is inside it (baseline) | |
| `merged_into_target` | head is in row 7's merged set | detached, or not established |
| `classification`, `recommendation` | the ladder below; the recommendation keeps its baseline text | |
| `prunable` | `true` when the record says `prunable`, else absent | |
| `locked` | from the registry's `locked` attribute | never null |
| `ignored_files_truncated` | the probe stopped at a bound | probe not run or failed |
| `ignored_samples` | at most 8 `{path, path_valid_utf8}`, paths relative to the worktree | probe not run or failed |
| `path_valid_utf8` | the path is valid UTF-8 | never null |
| `errors` | `{code, message, path?, path_valid_utf8?, reason?}`: `os-error`, `probe-failed`, `probe-timeout`, `deadline-exceeded` | |
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
resolved against the directory holding the file. A row with `present:
false` is decided first: it gets no registration check, no shared-path
check and no probe, and its reason is its class, `stale-worktree` (lead
rulings R-57 and R-59 D5). Otherwise a row whose registration disagrees
gets no status probe and is `inspection-error`, excluded as
`registration-mismatch`. Two registry entries naming one path, compared by
the registry records' raw path bytes as listed, fail closed: each is
`registration-mismatch`, since the porcelain listing does not name the admin
directory, so the two-way check alone cannot tell them apart (lead rulings
R-57, withdrawing R-51(c)'s known limit, and R-59 D5). The rule extends to
two present entries spelled differently with one realpath, or with one
admin id, which both pass the two-way check: each is `registration-mismatch`
too. Evidence follow-up 2 builds that extension in region `evidence`; until
then T049's single-mode match fails closed for P, its realpath matching both
(lead ruling R-67 (c), lane 3's L-4).

### Branch evidence (D6, D7)

`{branch, head, upstream, upstream_oid, ahead, behind}` from row 6, recorded
for each selected row. For a branch whose configured upstream's
remote-tracking ref was deleted, `upstream` is the short name and
`upstream_oid`, `ahead` and `behind` are null; at revalidation a value null
in the plan and null again is no difference, and one that reappears is
`state-changed` (D7, D20). For a branch named `HEAD` (`refs/heads/HEAD`),
`git for-each-ref` reports the current branch's upstream, so row 6 cannot
establish its upstream: its `upstream`, `remote_present`, `ahead` and
`behind` are null, meaning not established, never "none configured", and
the row is `inspection-error` with `probe-failed`, `git for-each-ref failed:
unparseable output` (lead rulings R-61 and R-64 (a); built by lane G's
follow-up).

### Classification (D6; FR-007)

First, a row whose evidence could not be established (`present` null, a
registration that disagrees, a status probe that failed or timed out, or
branch evidence row 6 could not establish, a branch named `HEAD` with its
`probe-failed` row error, R-61 and R-64) is
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

A row is selected only when it passes every gate; every excluded row
carries one `reason`, its first failing gate, never null. A row left
unprobed, whose reflog read did not finish within the filesystem budget
(T066's read, the unprobed marker's only setter), is excluded as
`reflog-unavailable` with its classification kept and its marker set, and
the plan is incomplete with `inspection-incomplete`; no reason value and no
group of its own are added for it (lead ruling R-67 (a), withdrawing R-56's
null reason for R-53's P-3):

| Order | Reason | Fails when |
| --- | --- | --- |
| 1 | `main-worktree` | the row is the main worktree |
| 2 | `unsupported-path-bytes` | the path is not valid UTF-8 |
| 3 | `registration-mismatch` | the two-way registration was read and disagrees (`registered is False`); a row whose registration was never read, a `present: false` one among them, passes and is excluded at gate 5 by its class (lead ruling R-53 P-16) |
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

A gate whose own read cannot finish decides nothing: a reflog read error
other than `ENOENT` or `ENOTDIR`, or a failed or timed-out `modules` read or
hidden-state probe, makes the row `inspection-error` (classification and
`reason`), its `errors` naming `os-error`, `probe-failed`, `probe-timeout`
or `deadline-exceeded`, and the plan incomplete (`inspection-incomplete`); a
null flag never passes gate 9 or 10, while gate 3 fails only on a
registration read and found to disagree (R-53 P-16). A reflog read not
finished within the filesystem budget follows the `project-clean` delta's
reflog outcome rule instead: the row is left unprobed, its marker set, and
excluded as `reflog-unavailable`, "where the reflog cannot decide it", never
selected, and the plan is incomplete with `inspection-incomplete` (R-67
(a)).

### Reflog anchor and movement (D10; FR-021, FR-022)

Read from `logs/refs/heads/<branch>` under `common_dir`, at most 64 KiB, by a
filesystem call (never a Git child). The read asks for no more than 65,536
bytes and needs no `fstat`: a read that returns 65,536 bytes has reached the
bound, and one that returns 65,535 is decided by its entries (lead ruling
R-33). Each line is `<old> <new> <identity> <time> <zone>`, then a tab and a
message when there is one.

- Anchor: the last surviving entry whose old object is all zeros, or whose
  message begins `branch: Created from` or `branch: Reset to`.
- Movement: an entry after the anchor, or any entry when no anchor survives,
  whose old and new objects are non-zero and differ (a rename's are equal).

| Outcome | When (first that holds) |
| --- | --- |
| `reflog-unavailable` | missing (`ENOENT`, `ENOTDIR`), 0 bytes, or the read reached its 64 KiB bound (65,536 bytes read) |
| `inspection-error` | any other error on the read |
| `reflog-unavailable`, the row left unprobed (its marker set; the plan `inspection-incomplete`; R-67 (a)) | the read did not finish within the filesystem budget |
| `reflog-unavailable` | a line that is not `<old> <new> ...`, a truncated last line included: the entries cannot decide, never `inspection-error` (lead ruling R-53 P-22) |
| `reflog-unavailable` | the last entry's new object is not the head |
| pass | a movement survives |
| `unstarted-branch` | an anchor survives with no movement after it, its new object the head |
| `reflog-unavailable` | anything else, no anchor and no movement included |

### Plan (FR-003, FR-019, FR-024, FR-025, FR-031, FR-032; D12 to D14)

What one invocation would do in one repository. Built fresh by every run.

| Mode | Spelled | Row cap | Selection |
| --- | --- | --- | --- |
| `report` | every other invocation without `--all-safe`: plain `project clean`, with or without `--json`, and flags without `--apply` | 256 | what `--all-safe` would select at 128 rows or fewer; null above 128, with the note `inspect-cap` and `rows` |
| `all-safe` | `--all-safe`, preview or `--apply` | 128 | every row passing every gate, at most 16 |
| `single` | `--apply --action remove --worktree P` | 128, P exempt and probed first | P alone |
| `single`, push and delete-branch | `--apply --action push` or `--action delete-branch`, which take single mode's cap and bounds only (below) | 128, no exemption | the named branch; completeness the batch's |

`clean_mode(args)` (T035) decides the mode as this table spells it: `single`
for `--apply` with any `--action` (lead rulings R-49 and R-57).

Fields, in the delta's envelope order: `schema_version`, `observed_at`,
`mode`, the baseline `root`, `target_branch` and `tracking_freshness`,
`worktrees`, the identity (`repository`), the merge target, `limits`,
`budget`, `probes`, `operations`, `selected`, `excluded`, `omitted`
(`{count, exactness: "exact"}`), `notes`, `completeness`, `apply_allowed`,
`refusals` and `plan_digest` (R12 in research.md).
`probes` counts every Git child other than a removal and `operations` the
removals, each child once (lead ruling R-27; research.md R8). Rows are ordered
main worktree first, then by raw path bytes; `selected`, `excluded` and the
execution order are by raw path bytes.

Completeness: a plan is `incomplete` when the row cap is exceeded
(`inspect-cap`), a repository-wide probe failed or a row is
`inspection-error` (`inspection-incomplete`), or the deadline passed while
planning (`deadline-exceeded`). In single mode those three are non-blocking
notes about other rows, and only P's own row and the repository-wide probes
decide (D13). In report mode above 128 rows, the `inspect-cap` note alone
does not make it incomplete. `apply_allowed` is false for every report and
for any plan that is incomplete or carries a refusal.

Push and delete-branch take single mode's 128-row cap and bounds only:
their completeness is the batch's, so any `inspection-error` row, the cap
or the deadline refuses them (`inspection-incomplete`, `inspect-cap`,
`deadline-exceeded`), exit 2, before and after confirmation (FR-010).

### Refusal (FR-043)

`{code, message, path?, path_valid_utf8?, reason?}`. `path_valid_utf8` is
present exactly when `path` is; `reason` only on `target-excluded`. The
eighteen codes and their phases are in the contract. `invalid-arguments`,
`internal-error` and every resolve refusal print the extended error object;
every other code prints the plan envelope with `apply_allowed: false`
(contract, "Streams").

### Target result and reconciliation record (FR-034, FR-035; D19)

One per selected target, in canonical order: `path`, `path_valid_utf8`,
`branch`, `planned_sha`, `stage`, `reason`, `notes`, `command` (the planned
argument vector, present even when nothing ran), `exit_status`,
`probes_performed` and `reconciliation`.

`exit_status` is null unless a child was spawned and reaped, and is 128
plus the number of the signal that ended it, whoever sent it, as
`BA:1035-1039` (at `da33d92`) and `execute()` report it: 143 when SIGTERM
ends it, at the ceiling too, and 137 only for a child that outlives SIGTERM
until SIGKILL (lead ruling R-68 (b)).

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
come from the revalidation that refused it, plus an `lstat` of the planned
path when that revalidation stopped before its own; a field from a listing
that did not run is null (`BA:1163-1174` at `da33d92` shows a ref-listing
refusal with `path_present: true`). A spawned target's values come from the
rescan after the child is reaped. Target notes: `orphaned-directory` (entry
gone, path present) and `partially-removed` (a child killed at the ceiling,
or whose exit was not observed, left its entry or path).

### Revalidation step and `probes_performed` (D7; FR-046, FR-047)

Each target's revalidation runs these steps in order and stops at the first
difference, which refuses the target, spawns nothing and attempts no later
target:

| Step | Read by | A difference gives |
| --- | --- | --- |
| 1. the identity probe (row 3 at `root`) | Git child | `identity-changed` |
| 2. the manifest re-read | filesystem | `state-changed` (manifest or merge target) |
| 3. the registry listing | Git child | `identity-changed` (registration, or a missing entry); `state-changed` (lock) |
| 4. the narrowed ref listing | Git child | `branch-changed` (branch name or head); `state-changed` (upstream, `upstream_oid`, `ahead`, `behind`, merge target) |
| 5. the target's identity and `modules` check | filesystem | `identity-changed`; `contains-submodule` (a `modules` entry) |
| 6. the combined status probe in the target, which must print nothing | Git child | `state-changed` |
| 7. the hidden-state probe | Git child | `contains-submodule` (a gitlink); `hidden-local-state` |

At most five Git children (steps 1, 3, 4, 6 and 7), from T084 on; until
then T055's interim full re-read runs 6 or 7 where row 4b or row 5 runs,
and T084 restores the bound (lead ruling R-68 (d)). A value null in the plan
and null again is no difference; a value that cannot be re-read, a
timed-out call included, is a difference, with its step's reason. The first
target's revalidation is the preflight of every selected target: its steps 3
and 4 and its filesystem reads compare every selected target's registration,
`locked` and filesystem identity, branch tip and upstream object, beside the
merge-target SHA, and a difference on any target refuses the first target
with that step's reason, nothing removed and later targets `not-attempted`
with `batch-stopped`; each target's steps 6 and 7 (its ignored-file state and
classification among them) run only in its own revalidation (research.md
R16, lead ruling R-41). After target k's
removal child is reaped, its rescan runs steps 1 to 4 again (three Git
children); when k ends as a plain `removed` they are target k+1's steps 1 to
4, and otherwise, or after the last spawned target, they are the final
rescan.

`probes_performed` counts the Git children of that target's revalidation,
the three it shares with the previous target's rescan included: at most 5,
fewer when it stopped at a difference, and 0 when it was never revalidated.
The record's `probes.performed` is the plan's count plus each target's
`probes_performed` plus the final rescan, which is 3 when the rescan after
the last spawned target counted toward no later target and 0 otherwise
(`BA:816-830` and `BA:1039-1042` at `da33d92`).

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
null, `worktrees` among them; an inspected dict has neither field (lead
ruling R-56). A `git-too-old` or
`git-unavailable` entry carries the contract's command-neutral message, never
`clean`'s refusal text (lead ruling R-48). Every `path` gains
`path_valid_utf8`, every `root` gains `root_valid_utf8`, and
`ignored_samples` entries are objects. A deleted upstream shows its short
name with `ahead` and `behind` null. `ignored_files` is the evidence model's
bounded count, capped at 64 (`ignored_entries`), so 64 means "64 or more";
no key is added for it (lead ruling R-66 (d)). The version check runs once
per invocation, memoized, when a repository is inspected; doctor's `git` row
runs it itself when none was, and `status` never runs it for nothing (lead
ruling R-56). `handoff()` runs its `git remote get-url origin` only for a
root whose repository was inspected, present and past the version check;
otherwise it returns the same no-identity state with no child (lead ruling
R-66 (c)).

### Child handle (D2; lead ruling R-30, research.md R14)

One spawned Git child other than the push child. It records its kind (`probe`,
read-only with `GIT_OPTIONAL_LOCKS=0`; `removal`; or `delegate`, the
`git branch -d` child), its process ID, which is also its process group ID, its
start time, its budget end (none for a removal or delegate handle), a removal's
300 s ceiling, its kill and reap deadlines once set, and the first 4 KiB of its
standard error. Termination never blocks: `terminate_group()` sends SIGTERM,
sets the kill deadline and returns at once, and the handle's `advance(now)`,
called by the driver loop on every tick, takes it on:

| State | Entered when | Leaves |
| --- | --- | --- |
| `running` | `start()` spawned and registered it | to `reaped` when its streams end and `Popen.poll()` returns a status; to `terminating` when its budget passes, its parser reaches a bound, the slot is read set while planning, a `finally` cleanup runs, or, for a removal, its ceiling passes |
| `terminating` | SIGTERM went to its group; kill deadline = now + grace | to `killing` at the kill deadline, or at once when its leader has exited |
| `killing` | SIGKILL went to its group, sweeping any member left; reap deadline = now + reap wait | to `reaped` when `Popen.poll()` returns a status; to `abandoned` at the reap deadline |
| `reaped` | its status was observed | final; it leaves the registry |
| `abandoned` | the reap deadline passed | final; `probe-timeout` recorded; never waited on again; it stays registered, so its group is killed again on exit |

The driver calls `advance()` on every `terminating` and `killing` handle on
each tick, and the selector's timeout counts their deadlines, so no handle's
grace delays another's. The grace and the reap wait (2 s each in the real
table) are read from `TIMING` when each step starts, never passed as an
argument. A `finally` cleanup moves every live probe handle to `terminating` at
once and ticks until each is `reaped` or `abandoned`, at most grace plus reap
wait (4 s) however many handles run. A removal handle reaches `terminating`
only at its ceiling, a delegate handle never, and the signal slot moves
neither.

### Driver outcome (D2)

`run_bounded()` returns one outcome per probe handle, with the parser's
result, the exit status and the standard-error head:

| Outcome | When | Row error |
| --- | --- | --- |
| `complete` | the child exited 0 and its streams ended | none |
| `complete-at-bound` | its parser reached its bound and the handle was terminated | none; never `probe-failed` |
| `failed` | it exited nonzero or by a signal, could not be spawned, or its parser's `finish()` raised `ParseError` (a truncated last record, or a record not in its format) | `probe-failed` |
| `timeout` | its budget passed | `probe-timeout` |
| `deadline` | the work deadline was the limit | `deadline-exceeded` |
| `interrupted` | the slot was read set while planning | none: D1's `Interrupted` is raised |

A handle abandoned at its reap deadline records `probe-timeout` (D2). The
version check maps any outcome but `complete`, and an unparseable
version, to `git-unavailable`.

### Invocation (D1; lead ruling R-44)

The per-run state of one `main()` call, a context manager in region `runner`
that `main()` enters fresh for every call: the per-child budget (5 s under
`clean`, 15 s otherwise), the clock (the work deadline and the reserve,
paused while a question waits), the probe and removal counters, the
per-invocation memos (the version check's result, the common-directory
evidence), and the phase: `planning` by default, then `apply` once the apply
phase begins, then `reconciling`. Outside any scope, `current_invocation()`
returns a fresh default: the 15 s budget and no signal handler. Its shell,
`Invocation(command=None)` with the phase and the signal slot, is T023's,
since the slot records with the phase; its budget, clock, counters and memos
are T024's (lead ruling R-47). A `signal_scope` entered with no `Invocation`
in force enters a default one for its own span, so that its handler and the
driver read one slot (R-47). So a direct `clean()` call, which only tests
make, runs on that scope's own default `Invocation`, whose command is None:
15 s per Git child and no 60 s deadline (lead ruling R-63 (e)).

### Signal slot (D1, D15)

The driver reads the slot by the `Invocation`'s phase: it raises
`Interrupted` only in `planning`, or on a second SIGINT in `reconciling`
(lead ruling R-44).

| Event | Effect |
| --- | --- |
| the first SIGINT, SIGTERM or SIGHUP | the handler stores its number and does nothing else; it decides the exit status (130, 143, 129) |
| a later signal | the slot keeps the first; a later SIGINT counts only in phase `reconciling` |
| the slot read set in phase `planning` (after each wake of the driver) | the child is terminated and `Interrupted` raised: cancelled |
| the slot read set at a seam of phase `apply` (before each revalidation and each spawn) | that target and every later one `not-attempted` with `interrupted`; reconciling follows |
| a second SIGINT while a rescan runs in phase `reconciling` | the remaining rescans are abandoned: the running group is terminated, fields not established stay null, and the target is `unknown` with `reconciliation-incomplete` |
| `raising_signals` entered with the slot already set | it raises at once, `KeyboardInterrupt` for SIGINT and `Terminated` for SIGTERM or SIGHUP, so no signal falls between reading the slot and installing its handlers (lead ruling R-47) |
| `default_signals` entered | the handlers in force before the outermost scope was entered are restored for its span (R-47) |
| a signal while a removal, push or `git branch -d` child runs | recorded only; the child is never signalled and is waited for |

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
| resolving to asking | unexpected exception | refused (`internal-error`) |
| planning | preview or report built | reported (exit 0 complete, 1 incomplete) |
| planning, `--apply` | incomplete; then `--expect-plan` mismatch | refused (exit 2), in that order |
| planning, `--apply` | complete `all-safe` plan selecting nothing | reported (`No eligible worktrees`, exit 0, no question) |
| planning, single | P matches no entry; P matches several, or one not decided (R-67 (b), R-69); a gate excludes P | refused (`worktree-not-found`; `inspection-incomplete`; `target-excluded`) |
| planning, `--apply` | standard input not a terminal, no `--yes` | refused (`confirmation-required`) |
| planning, `--apply` | `--yes` | applying |
| planning, `--apply` | otherwise | asking |
| asking | `yes` | applying |
| asking | any other answer | refused (`cancelled`) |
| asking | end of input, SIGINT, SIGTERM, SIGHUP | cancelled (130, 130, 143, 129) |
| resolving, planning | SIGINT, SIGTERM, SIGHUP | cancelled (130, 143, 129; probe groups killed and reaped) |
| reported | SIGINT, SIGTERM, SIGHUP recorded while the plan is written | cancelled (130, 143, 129; the slot read before the run exits, research.md R4) |
| applying | a target ends a plain `removed` and another follows | applying (next target) |
| applying | a target ends otherwise, the last target ends, a signal or the deadline | reconciling |
| applying, reconciling | an unexpected exception | reconciling (an in-flight removal waited for; that target `unknown` with `internal-error`, later ones `not-attempted`; research.md R6) |
| reconciling | record printed | exit by the table below |

### States of push and delete-branch

| From | Event | To |
| --- | --- | --- |
| (start), resolving | an argument check; a resolve refusal | refused (exit 2) |
| resolving | resolved | planning: the full inspection under single mode's row cap and bounds, with the batch's completeness |
| planning | incomplete; `remote-gone` (push); a baseline refusal | refused (exit 2, no delegate) |
| planning | accepted | confirming: `Cleanup action:` and the plan printed, then `confirm()` with the process's own handlers and the clock paused |
| confirming | `yes` or `--yes` | re-inspecting: the full re-inspection |
| confirming | another answer; no terminal and no `--yes`; Ctrl-C or end of input | refused (`confirm()`'s baseline messages, exit 2); cancelled (130) |
| re-inspecting | incomplete, or the state changed | refused (exit 2, no delegate) |
| re-inspecting | unchanged | delegating: the push child through `execute()`, or the `git branch -d` handle through the driver; unbounded, never signalled, waited for |
| delegating | the child exits | exit: 130, 143 or 129 when a signal was recorded, otherwise the child's status |
| resolving, planning, re-inspecting | SIGINT, SIGTERM, SIGHUP | cancelled (130, 143, 129; probe groups killed and reaped) |

### Target stages

`pending` leads to exactly one final stage. It is never printed: the plan
lists the selected rows, and each target's one progress line prints at its
final stage (lead ruling R-56 Q-10).

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

Later targets take `interrupted` after a signal, `deadline-exceeded` when
the floor or deadline stopped the run, and `batch-stopped` otherwise.

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
an incomplete plan, 0 otherwise, and 130, 143 or 129 when a signal ends it;
a write that fails after its plan is built is `internal-error`, exit 2, by
the delta's rule for an unexpected exception before the apply phase, which
conflicts with the preview rule above (research.md R4; lead rulings R-55 and
R-59; LQ-7).
A signal recorded while the push or `git branch -d` child runs is not
passed on: `project` never signals either child and waits for it. The run
then exits by D19's first row: 130, 143 or 129 when a signal was recorded,
otherwise the child's status (128 plus the signal number for a signal
death); a refusal exits 2. `status` keeps 0; `doctor` exits 1 on an `error`
check row, its rule unchanged; `update --apply --component shape` or
`bench` exits 2 when any `dirty` is not exactly false.

## Constants

| Name | Value |
| --- | --- |
| Git floor | 2.36 |
| deadline, reserve, work deadline | 60 s, 10 s, 50 s (time at the question not counted) |
| per Git child, per filesystem call | `min(5 s, work remaining)`; rescans `min(5 s, reserve remaining)` |
| per Git child in `status`, `doctor`, `update` | 15 s; no deadline, no row cap |
| per filesystem call in `status`, `doctor`, `update` | 15 s |
| grace, reap wait | 2 s, 2 s |
| removal floor, ceiling | 5 s of work deadline left; 300 s after spawn |
| row caps | 128 (`all-safe`, `single`), 256 (`report`) |
| targets per run | 16 |
| `ignored_entries`, `status_records`, `ignored_samples` | 64, 4,096, 8 |
| reflog read, manifest read | 64 KiB, 1 MiB |
| revalidation, final rescan | at most 5 and 3 Git children |

The timing values live in one module-level table, `TIMING`, read at call
time only, never captured in a default argument or a derived constant
(research.md R10, lead ruling R-29); `budget` and `limits` report the values
in force.
