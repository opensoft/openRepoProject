## MODIFIED Requirements

### Requirement: Clean classifies preservation and cleanup actions

The command SHALL classify each worktree row with exactly one of fifteen
classes, by a ladder tested in this order: `stale-worktree`,
`protected-default`, `inspection-error`, `dirty`, `ignored-local-files`,
`detached`, `unpublished`, `remote-gone`, `review-required`, `diverged`,
`remote-ahead`, `unpushed`, `merged-removable`, `merged-current` and
`pushed-unmerged`. The ladder SHALL be a function of the row's evidence alone,
and its names SHALL NOT change; its order SHALL NOT change except by the one
ancestry test stated here. A row whose evidence could not be established (a
path that cannot be read, a registration that disagrees, or a status probe that
failed or timed out) SHALL be classified `inspection-error` directly, whatever
its branch. A branch with no configured upstream SHALL be `unpublished`. A
branch whose configured upstream's remote-tracking ref no longer exists SHALL be
tested for local ancestry before the `remote-gone` rung: when its
`merged_into_target` is true, the row SHALL be `merged-removable`, or
`merged-current` when it is the current worktree, and otherwise it SHALL be
`remote-gone`, so that only an unmerged row is `remote-gone`.
`review-required` SHALL remain a defensive rung that no value of the evidence
model reaches.

The `ignored-local-files` rung SHALL apply to a row that holds a blocking
ignored path: one that "Clean disposes of listed caches before a worktree
removal" does not prove, in the same invocation, to be a listed cache. A row
whose every ignored path that requirement proves a listed cache SHALL pass that
rung and be classified by the rungs below it. A cache enumeration that fails or
times out SHALL leave the row's ignored paths unproven, and SHALL NOT make the
row `inspection-error`.

Every class other than `merged-removable` SHALL be preserved. Dirty, detached,
unpublished, remote-gone, and unmerged work SHALL be preserved and SHALL include
an actionable human handoff rather than being treated as removable. A row whose
configured upstream's remote-tracking ref no longer exists and whose
`merged_into_target` is true SHALL carry the recommendation of its class, as
every `merged-removable` or `merged-current` row does.

A linked worktree's `dirty` row whose status records are all deletions of
tracked files in the working tree, while its `.git` file and its registry entry
are present, SHALL carry the row note `partially-removed`: the human report
SHALL show a probable partial removal with the recovery text "inspect, then `git
worktree remove --force <path>` by hand" beside the `dirty` advice, never
instead of it. A status stream stopped at its record bound SHALL be judged on
the records read. The note SHALL be advisory and SHALL NOT change the row's
classification, the ladder or any gate.

#### Scenario: Dirty or unmerged work is preserved

- **WHEN** a worktree contains uncommitted changes or a branch is not merged
  into the target branch
- **THEN** the report identifies it as requiring preservation or review and
  proposes no destructive action for it

#### Scenario: A deleted upstream is remote-gone

- **WHEN** one linked worktree's branch, not merged into the merge target, has
  a configured upstream whose remote-tracking ref was deleted, and another's
  branch has no upstream configured
- **THEN** the first is classified `remote-gone` and the second `unpublished`,
  and both are preserved, where before this change both read `unpublished`

#### Scenario: A merged worktree whose upstream was deleted

- **WHEN** a clean linked worktree's branch, with a commit of its own, is merged
  into the merge target and its upstream's remote-tracking ref was deleted
- **THEN** it is classified `merged-removable`, where before this change it read
  `unpublished`, with the recommendation that every `merged-removable` row
  carries, and `--all-safe` selects it
- **AND** `--apply --action remove --worktree` naming it with `--yes` removes it
  and keeps its branch, where before this change it was refused as `unpublished`
- **AND** a linked worktree whose upstream's remote-tracking ref was deleted and
  whose branch is not merged into the merge target is classified `remote-gone`
  and preserved

#### Scenario: Only tracked-file deletions

- **WHEN** a registered linked worktree whose `.git` file is intact has only
  deleted tracked files as its working changes
- **THEN** it is classified `dirty` with the dirty advice, the human report
  shows the probable partial-removal note and the recovery text beside that
  advice, and the JSON row carries `notes: ["partially-removed"]`
- **AND** a worktree with one deleted tracked file and one untracked file
  carries no such note

#### Scenario: Cache-only ignored files pass the ignored-local-files rung

- **WHEN** a clean linked worktree whose branch, with a commit of its own, is
  merged into the merge target and published holds only ignored Python
  bytecode caches, and a second such worktree also holds an ignored `local.env`
- **THEN** the first is classified `merged-removable`, with the recommendation
  that every `merged-removable` row carries, where before this change it read
  `ignored-local-files`
- **AND** the second is classified `ignored-local-files` and preserved, and its
  caches are untouched

### Requirement: Clean can explicitly retire verified worktrees

An apply operation SHALL be able to remove one named linked worktree, or the set
that a fresh `--all-safe` plan selects, only when each is clean, not the current
worktree, and its branch is verified as merged into the target branch, and only
when each passes every gate that "Clean previews and applies a batch of eligible
worktree removals in one repository" lists, `unstarted-branch` included. Every
removal, single or batch, SHALL follow one sequence: revalidate the target as
"Cleanup revalidates destructive actions" states; for a target whose plan lists
caches, dispose of them as "Clean disposes of listed caches before a worktree
removal" states; spawn, only while at least the
5 s removal floor of the work deadline remains, the non-force command `git -c
status.showUntrackedFiles=normal -c core.untrackedCache=false -c
core.fsmonitor=false -c protocol.allow=never -c protocol.file.allow=never -c
protocol.ssh.allow=never -c protocol.git.allow=never -c
protocol.http.allow=never -c protocol.https.allow=never -c
protocol.ext.allow=never -C <command directory> worktree remove <path>` in its
own process group; wait for it; and reconcile by rescan as
"Clean records a reconcilable result for every removal target" states. Removal
SHALL stop after the first target whose result is not a plain `removed`, with no
continuation, rollback or automatic retry.

Once a removal child is spawned, `project` SHALL NOT signal it on SIGINT,
SIGTERM, SIGHUP or the work deadline, and SHALL wait for it to exit. Only a hard
ceiling 300 s after its spawn SHALL end the wait, by killing the child's process
group. The rescan SHALL then decide the target: `removed` when its registry
entry and path are gone, and otherwise `unknown` with the note
`partially-removed` and the recovery text "inspect, then `git worktree remove
--force <path>` by hand"; the reason SHALL be `removal-ceiling` in both cases.

For a removal named by `--worktree P`, the plan's completeness SHALL be the
repository-wide evidence plus P's own row: another row's `inspection-error`, its
omission by the row cap, or its being left unprobed SHALL be recorded in the
plan as a non-blocking omission and SHALL NOT refuse P, while P's own inspection
and revalidation stay fully strict. P SHALL be probed first and SHALL be exempt
from the row cap.

It SHALL remove a local branch only as a separate, explicit action after the
worktree is gone and the branch is verified merged.
It MUST never use a force removal, reset, or deletion of unmerged work.

#### Scenario: Remove a merged clean worktree

- **WHEN** the user requests removal of a clean linked worktree whose branch
  is an ancestor of the target branch
- **THEN** the command confirms and removes that worktree, while refusing to
  remove its branch unless the user separately requests branch deletion

#### Scenario: Every branch remains after a batch

- **WHEN** `project clean <root> --all-safe --apply --yes` removes every
  selected worktree
- **THEN** every selected worktree's local branch remains at its planned SHA,
  the result says that each branch was kept, and the exit status is 0

#### Scenario: A published branch with no commit of its own

- **WHEN** a linked worktree is made with `git worktree add -b x`, its branch is
  pushed with `git push -u`, and no commit is made on it, so that its reflog
  holds only the creation entry, whose new object is the branch's head
- **THEN** `--all-safe` reads that reflog and excludes the worktree as
  `unstarted-branch`
- **AND** `--apply --action remove --worktree` naming it refuses with
  `target-excluded`, reason `unstarted-branch`, and exit 2, where before this
  change it was removed
- **AND** after `git branch -m x y`, whose reflog entry has equal old and new
  objects, it is still excluded as `unstarted-branch`

#### Scenario: A fast-forward-merged branch at the target's tip stays eligible

- **WHEN** an otherwise eligible linked worktree's branch gains a commit and the
  merge target is then fast-forwarded to it, so that the branch's head equals
  the merge target's SHA
- **THEN** its reflog records that commit after its creation entry, `--all-safe`
  selects it rather than excluding it as `unstarted-branch`, and
  `--all-safe --apply --yes` removes it

#### Scenario: A branch reset to the merge target's tip stays unstarted

- **WHEN** a branch with commits of its own, merged into the merge target, is
  reset to the merge target's tip by `git worktree add -B <branch> <path>
  <merge target>`, and no commit is made on it afterwards
- **THEN** its last `branch: Reset to` entry is the anchor, no entry after it
  moves the branch, and `--all-safe` excludes the worktree as
  `unstarted-branch`, where its earlier commits would otherwise read as
  movement

#### Scenario: A branch fetched at the merge target's tip stays unstarted

- **WHEN** an otherwise eligible linked worktree's branch `f1` was created by
  `git fetch origin feat:f1` while `origin`'s `feat` was at the merge target's
  tip, then given `origin/feat` as its upstream by `git branch -u`, so that its
  reflog's only entry has an all-zeros old object and a message that does not
  begin `branch:`, and no commit is made on it here
- **THEN** that entry is the anchor and is no movement, and `--all-safe`
  excludes the worktree as `unstarted-branch`, where reading the entry as a
  movement would select it at the target's tip
- **AND** the same holds for a branch created at the merge target's tip by
  `git update-ref`, whose entry has no message, or by `git push .`, whose
  entry's message is `push`, each given its upstream the same way

#### Scenario: A branch whose reflog is missing, empty or expired

- **WHEN** an otherwise eligible worktree's branch head is a strict ancestor of
  the merge target and the branch has no reflog
- **THEN** the worktree is excluded as `reflog-unavailable` and is not removed
- **AND** the same holds when its head equals the merge target's SHA, and when
  its reflog file exists but is empty (0 bytes), as `git reflog expire` leaves
  it once every entry has expired
- **AND** when `git reflog expire` has removed the branch's creation and commit
  entries, older than `gc.reflogExpire`, and kept only a later rename entry,
  `--all-safe` excludes the worktree as `reflog-unavailable`
- **AND** `--apply --action remove --worktree` naming such a worktree refuses
  with `target-excluded`, reason `reflog-unavailable`, and exit 2, where before
  this change it was removed

#### Scenario: Git's own check runs on the pinned configuration

- **WHEN** the repository sets `core.untrackedCache=true` and
  `core.checkStat=minimal`, a status that writes the index has run, and a file
  is created in a selected target after its revalidation and before its removal
- **THEN** Git refuses the removal with exit status 128, the target is `failed`
  with `git-refused`, the file survives, and the exit status is 128

#### Scenario: A named removal beside another row's inspection error

- **WHEN** `--apply --action remove --worktree P --yes` names an eligible P
  while another linked worktree of the repository is `inspection-error`
- **THEN** P is removed, the plan records the other row as a non-blocking
  omission, and the exit status is 0

#### Scenario: A named removal among seventeen eligible rows

- **WHEN** seventeen rows are eligible and `--apply --action remove --worktree P
  --yes` names one of them
- **THEN** P is removed, the other sixteen are listed as `not-requested`, and
  the exit status is 0

#### Scenario: A named removal beyond the row cap

- **WHEN** more than 128 worktree rows are registered and `--apply --action
  remove --worktree P --yes` names an eligible row whose path sorts after the
  first 128
- **THEN** P is probed first and removed, the plan records the uninspected rows
  in `omitted` as a non-blocking omission, and the exit status is 0

#### Scenario: Single target equals a one-item batch

- **WHEN** two fresh copies of a repository in which P is the only eligible
  linked worktree are used in turn at one path, one with `project clean <root>
  --apply --action remove --worktree P --yes` and the other with `project clean
  <root> --all-safe --apply --yes`
- **THEN** both plans show the same `selected` entry for P apart from `dev` and
  `ino`, both run the same argument vector, and both end with P `removed` and
  exit 0
- **AND** when P is made dirty between confirmation and revalidation in both
  copies, both refuse with `state-changed`, the same message, and exit 2
- **AND** when another worktree in the repository is unreadable, the batch
  refuses with `inspection-incomplete` while the single-target removal removes P
- **AND** `--worktree` naming an unregistered path refuses with
  `worktree-not-found`, and naming a dirty worktree refuses with
  `target-excluded` and `reason: "dirty"`

#### Scenario: A removal past the hard ceiling

- **WHEN** a removal child is still running 300 s after it was spawned
- **THEN** its process group is killed and the rescan decides: the target is
  `unknown` with reason `removal-ceiling`, the note `partially-removed` and the
  recovery text when its registry entry or path remains, and `removed` with
  reason `removal-ceiling` when both are gone; later targets are
  `not-attempted`, and the exit status is 1

#### Scenario: project killed during a deletion

- **WHEN** `project` and its removal child are both killed with SIGKILL while
  Git is deleting a large target's files, and plain `project clean` runs
  afterwards
- **THEN** a target whose `.git` file survived is reported `dirty`, with the
  dirty advice and, beside it, the probable partial-removal note and the
  recovery text
- **AND** a target whose `.git` file was already deleted is reported as
  `registration-mismatch` with classification `inspection-error`, a named manual
  remedy and no partial-removal note

### Requirement: Clean bounds its Git work and reports omitted work

Each `project clean` invocation SHALL set one monotonic deadline 60 s after it
starts and SHALL hold back a 10 s reconciliation reserve, so that work stops 50
s after start; time spent blocked at the confirmation question SHALL NOT count,
both deadlines moving later by the time spent waiting. Each Git child SHALL get
`min(5 s, work remaining)`, and each filesystem call (`lstat`, `realpath`, the
reads of `.git`, `gitdir`, reflog and manifest files, and the directory listings
of the cache walk) SHALL be abandoned
after the same budget, recording `probe-timeout`, or `deadline-exceeded` where
the deadline was the limit, and leaving its values null. Probing SHALL be
serial. Reconciliation probes SHALL get `min(5 s, reserve remaining)`.

The deadline SHALL bound inspection and SHALL gate only the start of a removal:
a removal child SHALL be spawned only while at least the 5 s removal floor of
the work deadline remains, and otherwise that target and every later one SHALL
be `not-attempted` with `deadline-exceeded`. A cache stage, as "Clean disposes
of listed caches before a worktree removal" states, SHALL start only while more
than that floor remains, under the same rule, and each of its filesystem calls
SHALL get `min(5 s, work remaining less the removal floor)`, so that the floor
is left for the spawn. A removal child still running at
the deadline SHALL be waited for, up to its 300 s hard ceiling, and the
reconciliation reserve SHALL count from its exit. A run with no removal in
flight SHALL therefore end within 64 s of its start, not counting the time
blocked at the confirmation question (50 s of work, the 10 s reserve, and up to
4 s to stop and reap a probe child), and a removal in flight SHALL add at most
300 s, except while a filesystem call stuck in the kernel is outstanding. Push
and delete-branch children SHALL stay unbounded, as before this change.

The caps SHALL be: at most 128 worktree rows in
`mode: "all-safe"` and `mode: "single"`, and 256 in `mode: "report"`, every
registry entry counting, the main worktree and missing rows included; at most 16
targets per run; and the ignored-file bounds that "Repository inspection
requires Git 2.36 and shares one evidence model" sets; and the cache caps: at
most 16 cache enumerations per invocation, at most 512 cache entries and 256 MiB
(268,435,456 bytes) per worktree, and at most 4,096 cache entries and 1 GiB
(1,073,741,824 bytes) per invocation, applied as "Clean disposes of listed
caches before a worktree removal" states. A cache cap reached SHALL keep its row
`ignored-local-files` and SHALL NOT make the plan incomplete. Push and
delete-branch SHALL run in `mode: "single"` for the row cap and these bounds,
and SHALL run no cache enumeration. The registry
SHALL be read completely, in one child, before any cap applies; rows SHALL be
ordered main worktree first, then by raw path bytes; and the rows beyond the cap
SHALL be left uninspected and counted in `omitted: {count, exactness}`, with
`exactness` `exact`. A plan SHALL be incomplete, and apply refused, when the row
cap is exceeded (`inspect-cap`), a repository-wide probe fails or a row is
`inspection-error` (`inspection-incomplete`), or the deadline passes while
planning (`deadline-exceeded`), except as "Clean can explicitly retire verified
worktrees" states for a single-target removal. A preview or report SHALL exit 1
when its plan is incomplete and 0 when it is complete, deferred rows included.

When more than 16 rows pass every gate before `deferred-target-cap`, the first
16 in canonical order SHALL go on to the two index gates and the rest SHALL be
excluded as `deferred-target-cap`, with the command to run next. The plan SHALL
stay complete and apply SHALL be allowed; re-running SHALL take the next 16,
each run building its own fresh plan and revalidating each of its targets. Rows
that an index gate then excludes SHALL keep their places among the 16, so that
when every one of those 16 is excluded as `contains-submodule` no re-run reaches
a deferred row, and the human report SHALL say why the deferred rows will not
drain. No plan SHALL be refused for having more than 16 such rows. In a
single-target removal the limit SHALL count P alone, because `not-requested`
precedes it.

The cache enumerations SHALL count in the fit that sets the row and target
caps: with 128 worktree rows, 16 cache enumerations and 16 targets, planning,
revalidation and the final rescan spawn at most 250 Git children besides the 16
removals, so that at 150 ms per child and 0.3 s per removal the run's worst
case is about 42.3 s and the 16th target reaches its cache stage and its spawn
with more than the removal floor of the work deadline left.

Plans and apply results SHALL report `probes: {estimated, performed}` and
`operations: {estimated, performed}`, every Git child counted once, a removal
under `operations` and every other child, a cache enumeration included, under
`probes`, and each cache entry that a cache stage removes counted once under
`operations`; `limits` (`worktree_rows`, the row cap of the plan's mode,
`targets`, `ignored_entries`, `status_records`, `ignored_samples`, `cache_rows`
16, `cache_entries` 512, `cache_bytes` 268435456, `cache_entries_total` 4096
and `cache_bytes_total` 1073741824); and `budget` (`probe_timeout_seconds`
5, `invocation_timeout_seconds` 60, `reconciliation_reserve_seconds` 10,
`removal_floor_seconds` 5, `removal_ceiling_seconds` 300 and `probe_concurrency`
1). Revalidating one target SHALL spawn at most five Git children and never
recompute the full report, and the final rescan at most three.

#### Scenario: Row cap and planning failures

- **WHEN** more than 128 worktree rows are registered, or a probe times out or
  the deadline passes during planning, and `--all-safe` previews
- **THEN** the plan is incomplete with `inspect-cap`, `inspection-incomplete` or
  `deadline-exceeded`, `omitted` and the timed-out rows are visible, the main
  worktree and the 127 linked worktrees with the smallest paths are the ones
  inspected, and the preview exits 1
- **AND** `--apply` refuses with exit 2 before any mutation

#### Scenario: Twenty rows pass every gate before deferred-target-cap

- **WHEN** twenty rows pass every gate before `deferred-target-cap`, none of
  them holding a submodule or hidden local state, and `--all-safe --apply
  --yes` runs
- **THEN** the first sixteen in canonical order are selected and removed, the
  other four are deferred as `deferred-target-cap` with the command to run
  next, the plan is complete, and the exit status is 0
- **AND** a second run removes the remaining four

#### Scenario: Ignored-file bound

- **WHEN** a merged, clean worktree holds 70 ignored files, none of them a
  Python bytecode cache, and the plan is built
- **THEN** the probe stops when the 65th ignored record arrives, the row has
  `ignored_files: 64`, `ignored_files_truncated: true` and 8 `ignored_samples`,
  and it is excluded as `ignored-local-files`
- **AND** with exactly 64 such ignored files the row has `ignored_files: 64` and
  `ignored_files_truncated: false` and is still excluded as
  `ignored-local-files`
- **AND** a worktree with 4,097 untracked entries and no ignored ones stops at
  the 4,097th record with `ignored_files: null`, `ignored_files_truncated:
  true`, `dirty: true` and classification `dirty`, and the plan stays complete

#### Scenario: Bounded revalidation work

- **WHEN** a repository has five worktree rows, three of them selected, and
  `--all-safe --apply --yes` runs under a counting `git` wrapper on PATH
- **THEN** every target's revalidation spawns at most five children, the final
  rescan spawns three, three removals run, no merged-set listing and no status
  probe of a non-selected worktree runs after confirmation, and the record's
  `probes.performed` equals the wrapper's count of children other than the three
  removals, and its `operations.performed` is 3
- **AND** every `status` and `ls-files` child names its own worktree as its
  directory, and every other child after resolution, the removals included,
  names the command directory

#### Scenario: Deadline expiry mid-batch

- **WHEN** a test Git's removal of the second of three targets is still running
  when the work deadline passes
- **THEN** `project` does not signal it and waits for it; the second target is
  `removed` when the child exits 0 and the rescan shows its registry entry and
  path gone; the third is `not-attempted` with `deadline-exceeded`; and the exit
  status is 1
- **AND** when the first removal is slow enough that less than 5 s of the work
  deadline remains when the second target passes revalidation, no second child
  is spawned, the second and third targets are `not-attempted` with
  `deadline-exceeded` and `reconciliation: null`, and the exit status is 1

#### Scenario: The cache limits and counts

- **WHEN** `project clean <root> --all-safe --json` previews a repository whose
  one candidate for a cache enumeration holds caches of three entries, and then
  `--all-safe --apply --yes --json` runs
- **THEN** the plan's `limits` carries `cache_rows: 16`, `cache_entries: 512`,
  `cache_bytes: 268435456`, `cache_entries_total: 4096` and
  `cache_bytes_total: 1073741824`, its `probes.performed` counts the cache
  enumeration's child, and its `operations.estimated` is 4
- **AND** the apply record's `operations.performed` is 4, three cache entries
  and one removal

## ADDED Requirements

### Requirement: Clean disposes of listed caches before a worktree removal

`project clean` SHALL treat as a listed cache, and as nothing else, an ignored
path of a worktree that is either a directory named `__pycache__` whose entries
are only regular files whose names end `.pyc` or `.pyo` and directories named
`__pycache__` of the same shape, or a regular file whose name ends `.pyc` or
`.pyo`, none of them a symbolic link, and that meets the conditions "Cache
disposal never follows a symlink or leaves its worktree" adds. Names SHALL match
byte for byte. Every other ignored path SHALL be blocking. A cache entry SHALL
be each file and each directory that disposing of a listed cache removes, the
listed path included, and a listed cache's bytes SHALL be the sum of the
`lstat` sizes of its regular files.

A candidate SHALL be a linked worktree row whose combined status probe
established `dirty` false after reading at least one ignored record, and which,
its ignored records disregarded, the ladder would classify `merged-removable`
and every gate that precedes `deferred-target-cap` would pass; in
`mode: "single"` only P can be a candidate, and `--action push` and
`--action delete-branch` have none. For the candidates in canonical order, at
most 16 per invocation (`limits.cache_rows`), `project clean` SHALL run one
cache enumeration each, after the row's identity is verified: one Git child in
the row's own worktree, `status --porcelain=v2 -z --untracked-files=normal
--ignored=matching`, carrying the status pins `-c core.untrackedCache=false -c
core.fsmonitor=false`, the protocol pins, the scrubbed environment and
`GIT_OPTIONAL_LOCKS=0` that every read-only Git child carries, under the
per-child budget and counted in `probes`; then a walk of each listed directory
that opens every directory relative to its parent's descriptor without
following a symbolic link, each directory listing one filesystem call under the
per-call budget. The child SHALL stop at its 513th record, so that 512 records
(`limits.cache_entries`) is its bound.

A row SHALL stay at the `ignored-local-files` rung, with `cache_disposal.reason`
naming why, when its ignored paths are not all proven listed caches:

- `not-candidate`: it holds ignored records but is not a candidate;
- `cache-cap`: it is a candidate past the 16th; its child reached its record
  bound; its cache entries exceed 512 or its bytes 256 MiB (268,435,456,
  `limits.cache_bytes`); or, every ignored path being a listed cache, its
  entries or bytes would take the invocation's totals, summed in canonical
  order over such rows, past 4,096 entries (`limits.cache_entries_total`) or
  1 GiB (1,073,741,824, `limits.cache_bytes_total`), its own then not counted;
- `cache-unverified`: its child failed or timed out, read a record that is not
  an ignored one, or read no ignored record, or a filesystem call of its walk
  failed or timed out;
- `cache-unsupported-platform`, as "Cache disposal never follows a symlink or
  leaves its worktree" states.

A cache cap reached SHALL NOT make the plan incomplete, and a later run SHALL
take the rows the caps left. A deadline that passes during an enumeration SHALL
make the plan incomplete with `deadline-exceeded`, as it does during any probe.
A row whose enumeration finished with no cap reached SHALL have `reason` null,
and its ignored records SHALL be counted as `disposable`, those that are listed
caches, and `blocking`, the rest; such a row with `blocking` 0 SHALL pass the
`ignored-local-files` rung.

Every worktree row and every `selected` entry SHALL carry `cache_disposal`,
null when the row's `ignored_files` is null and otherwise an object of:

- `disposable` and `blocking`: integers, both 0 for a row with no ignored
  record, and null, never 0, when not established;
- `reason`: null or one of the codes above;
- `entries` and `bytes`: the totals of the row's listed caches, or null when
  not established;
- `paths`: the listed caches in canonical order, each `{path, path_valid_utf8,
  kind, entries, bytes}`, `path` relative to the worktree and `kind`
  `directory` or `file`, or null when not established;
- `directories`: every directory below the worktree root that the cache stage
  opens, each directory on the way down to a listed cache and each listed or
  nested cache directory, as `{path, path_valid_utf8, dev, ino}`, the device and
  inode read without following a symbolic link, or null when not established;
- `blocking_samples`: at most 8 (`limits.ignored_samples`) blocking paths as
  `{path, path_valid_utf8}`, or null when not established.

The canonical text of `plan_digest` SHALL carry, after the `[path, branch,
head]` triple of each selected target whose `cache_disposal.paths` is not empty,
that target's `paths` as `[path, kind]` pairs and its `directories` as `[path,
dev, ino]` triples, each in canonical order, so that a listed cache that
appears, disappears or changes kind, or a directory with another identity,
changes the digest. For a plan that selects no such target the canonical text
and the digest SHALL be those that "Clean previews and applies a batch of
eligible worktree removals in one repository" defines. `operations.estimated`
SHALL count each selected target's cache entries besides its removal.

For a selected target whose `cache_disposal.paths` is not empty, the removal
sequence SHALL run its cache stage after the target's revalidation passes and
before its removal child is spawned, under the same deadline. The stage SHALL
start only while more than the 5 s removal floor of the work deadline remains
and no signal has been received; otherwise the target and every later one SHALL
be `not-attempted` with `deadline-exceeded`, or with `interrupted`, and nothing
SHALL be deleted. Each of its filesystem calls SHALL run on a daemon thread and
get `min(5 s, work remaining less the removal floor)`. It SHALL dispose of
exactly the target's listed caches, as "Cache disposal never follows a symlink
or leaves its worktree" states. Once it has removed its first entry it SHALL run
to its end, a signal received meanwhile being only recorded, and the removal
child SHALL then be spawned, or not, by the sequence's own checks. A stage that
removes every listed cache SHALL let the sequence go on to the spawn. A stage
that ends `refused` or `partial` SHALL refuse the target with `state-changed`,
as "Cleanup revalidates destructive actions" states: no removal child is
spawned, the target carries its reconciliation, no later target is attempted,
and the exit status is the first matching row of the table that "Clean records
a reconcilable result for every removal target" defines, 2 unless a signal or
the deadline decides it.

Every apply-result target SHALL carry `cache_disposal`, null when its plan
listed no cache and otherwise `{stage, reason, paths, entries,
entries_removed}`: `stage` and `reason` SHALL be `disposed` with null,
`refused` with `cache-changed`, `partial` with `cache-partial`, or
`not-attempted` with `target-stopped` when the target's revalidation refused it,
or the run stopped, was interrupted or reached the deadline, before its stage
started; `paths` SHALL list each listed cache as `{path, path_valid_utf8, kind,
removed}`, `removed` being true when the stage removed it or its rescan found it
absent, false when it remains, and null when that is not established; `entries`
SHALL be the planned count and `entries_removed` the entries removed.
`operations.performed` SHALL count each entry removed.

The human preview SHALL list under each selected target with listed caches the
number of its cache paths, entries and bytes and its first cache path. An
`ignored-local-files` exclusion SHALL add its `disposable` and `blocking`
counts, each printed `unknown` with the reason when null, and its first blocking
path when established. The confirmation question SHALL stay as "Clean previews
and applies a batch of eligible worktree removals in one repository" states it.
A successful apply SHALL add one line naming how many cache paths were disposed
of in how many worktrees. A run that stops at a target whose cache stage ended
`refused` or `partial` SHALL print, before its stop block, one line naming that
target and saying that nothing was deleted, or how many of its cache paths were
removed and which remain, with the command that shows a fresh plan for the
rest. The residual-window line of the confirmation and of the result SHALL also
name caches recreated after a cache stage.

#### Scenario: A merged worktree whose only ignored files are caches

- **WHEN** a merged, clean, published linked worktree with a commit of its own,
  under the ignore rules `__pycache__/` and `*.pyc`, holds the directory
  `src/pkg/__pycache__/` with `a.cpython-312.pyc` and
  `b.cpython-312.opt-1.pyc`, and the loose file `tools/old.pyc`, and
  `project clean <root> --all-safe --json` previews
- **THEN** the row is `merged-removable` and selected, and its `cache_disposal`
  has `disposable: 2`, `blocking: 0`, `reason: null`, `entries: 4`, the two
  paths, and the device and inode of `src`, `src/pkg`, `src/pkg/__pycache__`
  and `tools` in `directories`
- **AND** `--all-safe --apply --yes --json` removes the four entries and then
  the worktree, the target is `removed` with `cache_disposal.stage:
  "disposed"`, its branch remains at its planned SHA, `operations.performed` is
  5, and the exit status is 0
- **AND** on a copy, `--apply --action remove --worktree` naming it with `--yes`
  does the same, where before this change it refused with `target-excluded`,
  reason `ignored-local-files`

#### Scenario: Caches beside a blocking ignored file

- **WHEN** the same worktree also holds the ignored file `local.env`
- **THEN** it is classified `ignored-local-files`, its `cache_disposal` has
  `disposable: 2`, `blocking: 1` and `blocking_samples` naming `local.env`, the
  preview shows both counts and `local.env` as the first blocking path, and
  nothing is deleted
- **AND** `--apply --action remove --worktree` naming it refuses with
  `target-excluded`, reason `ignored-local-files`, and exit 2, and every cache
  and `local.env` survive

#### Scenario: Unknown counts are null, never zero

- **WHEN** one linked worktree holds ignored caches and its branch is not
  merged, a second, merged one holds no ignored file, and a third's status probe
  fails
- **THEN** the first has `cache_disposal.reason: "not-candidate"` with
  `disposable`, `blocking`, `entries`, `bytes`, `paths`, `directories` and
  `blocking_samples` null, and the human report prints its counts as `unknown`
- **AND** the second has `disposable: 0`, `blocking: 0`, `reason: null`,
  `entries: 0`, `bytes: 0` and empty lists
- **AND** the third has `cache_disposal: null`

#### Scenario: Cache caps

- **WHEN** one candidate holds 513 ignored loose `.pyc` files under an ignore
  rule `*.pyc`, and another holds caches whose regular files total more than
  256 MiB
- **THEN** both are `ignored-local-files` with `cache_disposal.reason:
  "cache-cap"`, the first's enumeration child having stopped at its 513th
  record, nothing is deleted, the plan is complete, and apply is allowed
- **AND** when seventeen candidates each hold one small cache directory, the
  first sixteen in canonical order are enumerated and selected, the seventeenth
  stays `ignored-local-files` with `cache-cap`, `--all-safe --apply --yes`
  removes sixteen, and a second run removes the seventeenth
- **AND** when nine candidates each hold caches of 500 entries, the first eight
  are selected and the ninth stays `ignored-local-files` with `cache-cap`, its
  entries not counted toward the 4,096

#### Scenario: The cache enumeration runs under the pins

- **WHEN** the user's configuration sets `status.showUntrackedFiles=no` and
  `core.untrackedCache=true`, and `--all-safe` previews a repository with one
  cache-only candidate under a counting `git` wrapper on PATH
- **THEN** the wrapper records one `status --porcelain=v2 -z
  --untracked-files=normal --ignored=matching` child naming that worktree as its
  directory and carrying `-c core.untrackedCache=false -c
  core.fsmonitor=false` and the seven protocol pins, the enumeration succeeds,
  and `probes.performed` counts that child
- **AND** no such child runs for a row that is not a candidate, nor for
  `--apply --action push`

#### Scenario: Cache paths are part of the plan digest

- **WHEN** a preview with digest D selects a target with listed caches, and
  before `--all-safe --apply --yes --expect-plan D` runs a new ignored
  `__pycache__` directory holding one `.pyc` file appears in it, or its listed
  cache directory is replaced by a new directory of the same name and content
- **THEN** the fresh plan has another digest, the run refuses with
  `plan-digest-mismatch` and exit 2 before any question, and no cache entry is
  deleted
- **AND** for a repository whose selected targets list no cache, the digest
  equals the one that the batch requirement's canonical text alone gives

#### Scenario: A partial cache phase

- **WHEN** a selected target lists three caches and a test hook makes the
  removal of an entry of the second fail after the first cache was removed
- **THEN** the stage stops, the first cache stays removed, the target's
  `cache_disposal` is `partial` with `cache-partial` and `paths` showing the
  first `removed: true` and the other two `removed: false`, the target is
  `refused` with `state-changed` and carries its reconciliation, no removal
  child is spawned, later targets are `not-attempted` with `batch-stopped`, and
  the exit status is 2
- **AND** before the stop block the human result says that one of three cache
  paths was removed, names the two that remain, and gives the command for a
  fresh plan
- **AND** a second run lists only the two remaining caches, disposes of them
  and removes the worktree, its branch kept

#### Scenario: No time for a cache stage

- **WHEN** no more than the 5 s removal floor of the work deadline remains when
  a target with listed caches passes revalidation
- **THEN** its cache stage does not start, no cache entry is deleted, it and
  every later target are `not-attempted` with `deadline-exceeded`, its
  `cache_disposal` is `not-attempted` with `target-stopped`, and the exit status
  is 1

#### Scenario: A signal during a cache stage

- **WHEN** SIGINT arrives after a cache stage has removed its first entry
- **THEN** the stage removes the rest of its listed caches and records
  `disposed`, no removal child is spawned for that target, the target and every
  later one are `not-attempted` with `interrupted`, and the exit status is 130
- **AND** SIGINT before the stage's first removal leaves every cache in place,
  and the target is `not-attempted` with `interrupted` and its `cache_disposal`
  `not-attempted` with `target-stopped`
