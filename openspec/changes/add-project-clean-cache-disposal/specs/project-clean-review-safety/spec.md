## MODIFIED Requirements

### Requirement: Cleanup preserves all local work not proven disposable

Cleanup SHALL treat ignored local files, except the listed caches that "Clean
disposes of listed caches before a worktree removal" proves disposable, dirty
work, detached state, an unknown default branch, and remote divergence as
preservation or review states. It SHALL also treat as preservation states the
main worktree; a locked worktree; a
worktree whose index holds a gitlink or whose administrative directory holds a
`modules` entry (`contains-submodule`); a worktree whose index flags any entry
assume-unchanged or skip-worktree, sparse checkouts included
(`hidden-local-state`); a worktree whose registration disagrees in either
direction (`registration-mismatch`); a path that is not valid UTF-8
(`unsupported-path-bytes`); a branch whose reflog shows no movement since its
anchor, its last entry whose old object is all zeros, as any entry that creates
the branch has whatever its message, or whose message begins
`branch: Created from` or `branch: Reset to` (`unstarted-branch`), a head equal
to the merge target's SHA not being proof of that; a branch whose reflog is
missing, empty or read to its 64 KiB bound, or whose surviving entries cannot
decide that (`reflog-unavailable`); and a worktree whose path cannot be read or
whose state could not be established (`inspection-error`). It
MUST not offer destructive removal for those states. A value that is not
established SHALL be null, never false or 0, and SHALL keep its row out of every
removal. A listed cache SHALL be disposable only by the cache stage of a target
that a confirmed plan selected, under "Cache disposal never follows a symlink or
leaves its worktree"; in every other row it SHALL stay an ignored local file, as
an ignored path not proven a listed cache SHALL in every row.

#### Scenario: A merged worktree has ignored local files

- **WHEN** a non-current merged worktree contains an ignored file that is not a
  listed cache, such as `local.env`, with or without caches beside it
- **THEN** cleanup reports a preservation state and refuses its removal

#### Scenario: Default branch cannot be established locally

- **WHEN** neither the manifest, remote HEAD, nor a conventional local default
  branch identifies a merge target
- **THEN** cleanup refuses instead of guessing from the current branch

#### Scenario: An edit hidden by assume-unchanged survives

- **WHEN** a merged, clean, published linked worktree's only change is an edit
  to a file flagged assume-unchanged in its own index, and `--apply --action
  remove --worktree` names it with `--yes`
- **THEN** removal is refused with `target-excluded`, reason
  `hidden-local-state`, and exit 2, and the edit survives, where before this
  change the worktree was removed with exit 0, edit included

#### Scenario: A worktree holding a submodule is never offered

- **WHEN** a merged, clean, published linked worktree holds a populated
  submodule, and `--apply --action remove --worktree` names it with `--yes`
- **THEN** removal is refused with `target-excluded`, reason
  `contains-submodule`, and exit 2 before any Git removal runs, where before
  this change it was offered and Git refused it with exit 128

#### Scenario: The main worktree and a locked worktree

- **WHEN** `--apply --action remove --worktree` names the main worktree, or a
  merged, clean, published linked worktree that is locked
- **THEN** removal is refused with `target-excluded`, reason `main-worktree` or
  `locked-worktree`, and exit 2, and nothing is removed

#### Scenario: Caches alone are not a preservation state

- **WHEN** a non-current, merged, clean, published linked worktree's only
  ignored files are Python bytecode caches
- **THEN** cleanup reports no preservation state for them, and
  `--all-safe --apply --yes` disposes of the caches and removes the worktree,
  its branch kept
- **AND** when the same worktree is locked, or its branch is not merged, it is
  preserved and its caches are untouched

### Requirement: Cleanup revalidates destructive actions

Cleanup SHALL re-inspect the selected target after confirmation and before a
push, worktree removal, or local branch deletion. It MUST refuse when the
state no longer matches the reviewed plan.

That MUST SHALL apply at the revalidation performed immediately before each
removal child is spawned, or, for a target whose plan lists caches, immediately
before its cache stage; a change after it is the residual window that "Cleanup
states a narrow guarantee and its residual window" states. A worktree removal
SHALL be revalidated by a targeted check, never by recomputing the full report:
at most six Git children, and a seventh where the plan read the repository's
`extensions.worktreeConfig` as true, a fresh manifest read and the `modules`
and `operation-in-progress` checks, run in this order and stopping at the first
difference: the identity probe in the command directory; the manifest re-read;
the registry listing; one ref listing that names the merge-target candidates,
`refs/remotes/origin/HEAD`, and the selected branches and their upstreams; the
target's identity, its `modules` check and its `operation-in-progress` check,
by filesystem reads, and, where the plan read
`extensions.worktreeConfig` as true, its effective work tree, by the probe that
"Repository inspection requires Git 2.36 and shares one evidence model" states;
and, inside the target worktree, the combined status probe, which SHALL print
no record, or, for a target whose plan lists caches, the child of the cache
enumeration that "Clean disposes of listed caches before a worktree removal"
defines, which SHALL print exactly the ignored records that the plan listed and
no other record,
then the hidden-state probe, then the `worktree-only-commits` check
that "Clean previews and applies a batch of eligible worktree removals in one
repository" states, `logs/HEAD` read again and the non-zero objects that the
plan's branch reflog named taken as they were, whose probe SHALL print
nothing. It SHALL compare
the recorded repository identity (`root`, `common_dir`, `dev`, `ino`), the
target's worktree identity (`path`, `dev`, `ino`, `admin_id`), two-way
registration and, where it
was read, effective work tree, its branch evidence (`branch`, `head`,
`upstream`, `upstream_oid`, `ahead`, `behind`), every baseline signature field
of the target, its `locked` flag, the manifest's `tracking_branch`, and the
merge target's `name`, `source` and `sha`, re-resolved from the fresh manifest
read.

A difference SHALL refuse the target, spawn nothing, attempt no later target and
exit 2, with the reason `identity-changed` for a repository or worktree identity
or registration difference, an effective work tree that the probe decides is
not the target's path, or a missing registry entry, `branch-changed` for a
different branch name or head, `state-changed` for any other signature, lock,
manifest, merge-target or listed-cache difference and for a cache stage that
ends `refused` or `partial` as "Cache disposal never follows a symlink or leaves
its worktree" states, whose exit status is the one "Clean disposes of listed
caches before a worktree removal" gives, `contains-submodule` for a new gitlink
or `modules` entry, `hidden-local-state` for a newly flagged index entry,
`operation-in-progress` for a marker that the re-read listing finds, and
`worktree-only-commits` for a commit that only the target's HEAD reflog or
`refs/worktree/` holds, or for a `logs/HEAD` read to its 64 KiB bound or holding
a line that cannot be parsed. A value that was null in the plan and is null at
revalidation, such as the `upstream_oid`, `ahead` and `behind` of a selected row
whose upstream was deleted, SHALL NOT count as a difference; a value that cannot
be re-read SHALL count as a difference, other than one that the work deadline
cuts, as the rule that follows decides. One rule SHALL decide every Git child
and every filesystem call of these steps that does not finish with a value: one
that the work deadline cuts SHALL count as no difference, and the target and
every later one SHALL be `not-attempted` with `deadline-exceeded`; one that
fails, or that runs past its own budget while the deadline is not the limit,
SHALL count as a difference with the reason `state-changed`, whatever its step,
as for a status probe that fails there and for the listing, read or child of the
`operation-in-progress` or `worktree-only-commits` check. A filesystem call that
finds no file or directory at its path (`ENOENT` or `ENOTDIR`) SHALL not count
as one that fails: it SHALL decide that the path is absent. A Git child or a
filesystem call SHALL give its step's own reason only for a value it decided, so
that, of the work-tree probe's outcomes, only an effective work tree that it
decides is not the target's path gives `identity-changed`, and a work-tree probe
that fails, runs past its own budget or prints anything but one line gives
`state-changed` (the lead's R-171), and so that a filesystem call reading the
repository's or the target's identity or registration that fails, or runs past
its own budget while the deadline is not the limit, gives `state-changed`, while
a different value that it decides, an absent path included, gives
`identity-changed` (the lead's R-208). The first target's repository-wide checks
SHALL serve as the preflight of every selected target, so that a difference
found there removes nothing at all. Push and delete-branch SHALL keep the full
re-inspection, and SHALL refuse with `inspection-incomplete`, `inspect-cap` or
`deadline-exceeded` and exit 2 when it is incomplete. Git's own non-force check
SHALL be the last defense only on the pinned configuration that the removal
command carries: `status.showUntrackedFiles=normal`,
`core.untrackedCache=false`, `core.fsmonitor=false`, `core.trustctime=true` and
`core.checkStat=default`; the protocol pins that every Git child, except the
push child, carries (`-c protocol.allow=never` and the six per-protocol pins)
are no part of that defense.

#### Scenario: Worktree changes while confirmation is pending

- **WHEN** a selected worktree becomes dirty after the plan is shown
- **THEN** cleanup refuses removal and preserves the worktree

#### Scenario: Target directory replaced

- **WHEN** a confirmed plan's first target P has recorded `dev`, `ino` and
  `admin_id`, and P is moved aside and a new directory or a symlink is put at P
  before its revalidation
- **THEN** P is `refused` with `identity-changed`, no child is spawned, later
  targets are `not-attempted`, and the exit status is 2

#### Scenario: Admin registration changed

- **WHEN** P's `.git` file is rewritten to name another administrative
  directory, or P's administrative `gitdir` file is changed to name another
  path, after confirmation
- **THEN** P is `refused` with `identity-changed` and exit 2
- **AND** a fresh plan reports the row as `registration-mismatch` with
  classification `inspection-error`, and is incomplete

#### Scenario: Parent directory swapped

- **WHEN** the directory holding a target is replaced by a symlink to a copy of
  it after confirmation
- **THEN** the target's realpath differs, and it is `refused` with
  `identity-changed` and exit 2

#### Scenario: New worktree and pre-removal changes

- **WHEN** a new linked worktree is registered after confirmation
- **THEN** it is not selected
- **AND** a changed merge-target SHA, feature branch tip, upstream object, lock,
  ignored-file state, or classification of any target before the first removal
  causes no mutation and exit 2 with the matching reason

#### Scenario: State changes before revalidation

- **WHEN** before a target's revalidation an ignored file is created in it, the
  merge target gains a commit, the manifest's `tracking_branch` is edited to
  name another existing branch, or the manifest is made unparseable
- **THEN** the target is `refused` with `state-changed` and exit 2, and a change
  that the preflight finds removes nothing at all
- **AND** the same holds for a plan resolved through `origin/HEAD` when the
  manifest gains a `tracking_branch` naming an existing branch, such as
  `release`, that the narrowed ref listing does not name, and when
  `refs/remotes/origin/HEAD` is repointed to another existing branch

#### Scenario: Changed later target

- **WHEN** a target changes after earlier targets were removed
- **THEN** it stops the run, and the record reports the earlier targets'
  completed stages and retained branches accurately

#### Scenario: Untracked file under status.showUntrackedFiles=no

- **WHEN** the user's configuration sets `status.showUntrackedFiles=no` and a
  test hook creates an untracked file in a target after its revalidation
- **THEN** Git refuses the removal with exit status 128, the target is `failed`
  with `git-refused` and its reconciliation shows the registry entry and path
  present, the file survives, later targets are `not-attempted`, and the exit
  status is 128

#### Scenario: Branch advances before removal

- **WHEN** a selected target's branch gains a commit after confirmation and
  before its revalidation
- **THEN** it is `refused` with `branch-changed`, its reconciliation shows the
  new `branch_sha`, later targets are `not-attempted`, the branch is retained at
  the new commit, and the exit status is 2

#### Scenario: Deleted upstream reappears before revalidation

- **WHEN** a confirmed plan selects two merged-removable worktrees P and Q, in
  that order, each on a branch whose configured upstream's remote-tracking ref
  was deleted, so that each row records its `upstream` with `upstream_oid`,
  `ahead` and `behind` null, and a `git fetch` recreates `origin/<branch>` for
  P's branch before apply while Q's stays deleted
- **THEN** P's `upstream_oid` is non-null at revalidation where the plan
  recorded null, so P is `refused` with `state-changed`, no child is spawned,
  Q is `not-attempted`, nothing is removed, and the exit status is 2
- **AND** when the fetch instead recreates Q's upstream after P's removal child
  exits 0 and before the rescan that follows it, P, null in the plan and null at
  revalidation, is `removed`, Q is `refused` with `state-changed`, and the exit
  status is 2

#### Scenario: A worktree-only commit made after the plan

- **WHEN** a confirmed plan selects P and Q, in that order, and after the plan
  and before P's revalidation P's HEAD is detached, a commit is made there and
  P's branch is checked out again, so that only P's HEAD reflog holds the
  commit and P's tree, index and branch are as the plan recorded them
- **THEN** P is `refused` with `worktree-only-commits`, no child is spawned, Q
  is `not-attempted`, nothing is removed, and the exit status is 2, where
  before this change P was removed with exit 0
- **AND** the same holds when that commit is held only by a ref under P's
  `refs/worktree/`, created after the plan

#### Scenario: An operation started after the plan

- **WHEN** a confirmed plan selects P and Q, in that order, and after the plan
  and before P's revalidation `git bisect start --no-checkout` runs in P,
  leaving P's tree, index and branch as the plan recorded them
- **THEN** P is `refused` with `operation-in-progress`, no child is spawned, Q
  is `not-attempted`, nothing is removed, and the exit status is 2, where
  before this change P was removed with exit 0

#### Scenario: A check that fails at revalidation

- **WHEN** a confirmed plan selects P and Q, in that order, and after the plan
  and before P's revalidation P's administrative directory loses its read
  permission while its `gitdir` and `commondir` files stay readable, so that
  its listing fails
- **THEN** P is `refused` with `state-changed`, no removal child is spawned, Q
  is `not-attempted`, nothing is removed, and the exit status is 2
- **AND** the same holds when, instead, a line naming an object that the
  repository does not hold is appended to P's `logs/HEAD`, so that the
  reachability child exits 128 with `fatal: bad object`
- **AND** the same holds, with `state-changed` rather than `identity-changed`,
  when, instead, P's `.git` file loses its read permission, so that the read of
  P's registration fails

#### Scenario: A work-tree probe at revalidation

- **WHEN** a repository sets `extensions.worktreeConfig` to true, a confirmed
  plan selects P and Q, in that order, having read P's effective work tree as
  P's own path, and after the plan and before P's revalidation the
  `config.worktree` in P's administrative directory sets `core.worktree` to a
  clean directory D elsewhere
- **THEN** P's work-tree probe prints D's path, so P is `refused` with
  `identity-changed`, no removal child is spawned, Q is `not-attempted`,
  nothing is removed, and the exit status is 2
- **AND** when that `config.worktree` instead sets `core.bare` to true, so that
  the probe exits 128, or sets `core.worktree` to an existing directory whose
  name holds a line feed, so that the probe prints two lines, or when a `git`
  wrapper holds the probe past its own 5 s budget, the probe having started
  with more than 5 s of the work deadline left, P is `refused` with
  `state-changed`, nothing is removed, and the exit status is 2
- **AND** when a `git` wrapper holds the probe until the work deadline passes,
  the probe having started with less than 5 s of it left, P and Q are
  `not-attempted` with `deadline-exceeded`, nothing is removed, and the exit
  status is 1

#### Scenario: A cache target changes before revalidation

- **WHEN** a confirmed plan's first target lists caches, and before its
  revalidation an ignored `local.env` is created in it, a new ignored
  `__pycache__` directory appears in it, or one of its listed caches is deleted
- **THEN** its revalidation's status child prints a record the plan did not
  list, or lacks one the plan listed, the target is `refused` with
  `state-changed`, no cache entry is deleted and no child is spawned, later
  targets are `not-attempted`, and the exit status is 2

### Requirement: Cleanup states a narrow guarantee and its residual window

Concurrent writers (editors, other agents, other `project` invocations, and Git
commands run by anyone else) SHALL be outside the safe contract, and cleanup
SHALL claim no lock, lease or writer-quiescence handoff. Its one guarantee for a
worktree removal SHALL be that a removal child is spawned only if, at the
revalidation performed immediately before spawning it, or, for a target whose
plan lists caches, immediately before its cache stage, the repository identity,
the target's worktree identity and branch evidence, every baseline signature
field of the target, its `locked` flag, the absence of submodules and of hidden
local state in its own index (read inside the target worktree), the manifest's
`tracking_branch`, and the merge target's name, source and SHA all equal the
values in the confirmed plan. A cache stage SHALL carry the one guarantee for
the cache entries it removes that "Cache disposal never follows a symlink or
leaves its worktree" states, and nothing SHALL run between that stage and the
spawn but the removal floor and signal checks.

Ignored files created, and index flags set, after that revalidation, and any
change made after Git's own check, SHALL be outside the contract; the
confirmation and the result SHALL each state this residual window in one line.
For a target whose plan lists caches, that window SHALL include a cache
recreated after its cache stage and ignored files created during its cache
stage outside the listed caches, both of which Git's non-force removal deletes
with the worktree; when the plan selects such a target, the residual-window
line SHALL also name ignored files created during a cache stage and caches
recreated after it. Cleanup SHALL never
delete a
branch, so that a branch race cannot lose commits: a branch change seen at
revalidation SHALL refuse the target with `branch-changed`, and one seen only by
the rescan after Git removed the worktree
SHALL leave the target `removed` with `branch-advanced-after-removal`, the
branch present at a different SHA, or `branch-missing-after-removal`, stop the
run, and exit 2. A repository found replaced by the rescan after a removal SHALL
make that target `unknown` with `unconfirmed-removal`, every reconciliation
field null and `reconciled` false, and SHALL stop the run with exit status 1.

#### Scenario: Ignored file in the residual window

- **WHEN** a test hook creates an ignored file in a target after its
  revalidation and before its removal child starts
- **THEN** Git removes the worktree with exit 0, the target is `removed`, the
  file is gone, and the result text carries the residual-window line, which the
  confirmation also carried; this documents the boundary rather than a guarantee

#### Scenario: Branch advances after removal

- **WHEN** a test hook advances a target's branch after Git removed the worktree
  and before the rescan
- **THEN** the target is `removed` with `branch-advanced-after-removal`, its
  reconciliation has `registry_entry_present: false`, `path_present: false`,
  `branch_present: true` and a `branch_sha` that differs from `planned_sha`,
  later targets are `not-attempted`, no commit is lost, and the exit status is 2
- **AND** a hook that deletes the branch instead yields
  `branch-missing-after-removal` with `branch_present: false` and exit 2

#### Scenario: Repository replaced mid-batch

- **WHEN** in a three-target plan, after the first target's removal child exits
  0 and before the rescan that follows it, the repository root is renamed and
  another clone is moved into its path, or the root's parent directory is
  replaced by a symlink to a copy
- **THEN** the rescan's identity probe finds a different repository, the first
  target is `unknown` with `unconfirmed-removal`, every reconciliation field
  null and `reconciled: false`, the second and third are `not-attempted` with
  `batch-stopped`, and the exit status is 1
- **AND** when the same replacement happens before the first target's
  revalidation, the first target is `refused` with `identity-changed`, the later
  targets are `not-attempted`, nothing is removed, and the exit status is 2

#### Scenario: A cache recreated after the cache stage

- **WHEN** a test hook recreates `src/pkg/__pycache__/a.cpython-312.pyc` after a
  target's cache stage and before its removal child starts
- **THEN** Git removes the worktree with exit 0, the target is `removed`, the
  file is gone, and the confirmation and the result carry the residual-window
  line that names it; this documents the boundary rather than a guarantee
- **AND** when the hook instead creates an ignored `local.env` at the worktree
  root during the cache stage, the same holds for that file, and the line also
  names ignored files created during a cache stage

## ADDED Requirements

### Requirement: Cache disposal never follows a symlink or leaves its worktree

A listed cache SHALL NOT be a symbolic link, nor SHALL any directory between it
and the worktree root (at plan time a symbolic-link directory on the way down
is `cache-unverified`, below, since the walk meets it only as a refused
no-follow open), nor any entry inside a listed directory; every such
directory, and a listed cache that is a directory and every directory inside
it, SHALL be on the device of the worktree root; and the cache's path, and the
name of every entry inside a listed directory, SHALL be valid UTF-8. An
ignored path that fails any of these SHALL be blocking,
and its row SHALL be preserved as "Cleanup preserves all local work not proven
disposable" states. Where the walk's no-follow open of a directory is refused
at plan time, as for a directory replaced by a symbolic link after Git printed
its records, the row SHALL instead be `cache-unverified`, as for any failed
call of the walk, and SHALL NOT be counted blocking. Neither the cache
enumeration nor the cache stage SHALL ever
follow a symbolic link, so that its target, inside or outside the worktree, is
never read, listed or changed by them, and a file with other hard links SHALL
lose only its name inside the worktree.

The cache stage SHALL use descriptor-relative operations only. It SHALL open the
worktree root by the target's recorded path with `O_DIRECTORY` and `O_NOFOLLOW`
and require the opened directory's device and inode to equal the target's
recorded worktree identity; it SHALL open every directory below the root
relative to its parent's descriptor with `O_DIRECTORY` and `O_NOFOLLOW`, and
require each opened directory's device and inode to equal those that the plan
recorded for it. In its preflight, and again in its removals, it SHALL open
that chain once for each directory that holds a listed path, not once per
entry, checking every identity on it, SHALL check or remove that directory's
listed entries relative to its descriptor, and SHALL reach a listed cache
directory and the directories inside it from that descriptor. It SHALL remove a
file by an unlink relative to its directory's
descriptor, and a directory by a removal relative to its parent's descriptor
only after removing every entry it listed there. It SHALL NOT use a recursive
deletion, a check by path name followed by a deletion by path name, `git clean`,
or any child process. A directory that still holds an entry when its removal is
attempted SHALL be left in place, with that entry untouched. A worker with a
call still outstanding (a read abandoned at its budget, or a removal whose wait
the removal ceiling ended) SHALL be given no further call, and no descriptor
given to a call still outstanding SHALL be closed before `project` exits, so
that no later open receives its number.

Before its first removal the stage SHALL run a whole-list preflight: it SHALL
open and check every directory that the target's `cache_disposal.directories`
lists; re-list every listed cache directory by a descriptor-relative streaming
enumeration that yields one entry at a time and is closed at the first entry
beyond the `entries` that the plan recorded for its listed cache, which is a
difference, so that no enumeration holds a whole directory's listing, requiring
each entry to have the allowlisted shape, each nested directory to carry its
planned identity, each listed cache's entries to number exactly the `entries`
that the plan recorded for it, and the target's bytes to stay within the
per-worktree cap; require every listed file to be a regular file; keep the
run's byte total, the sum of
the bytes that this preflight measures and that the preflight of every earlier
target whose cache stage passed its preflight in this run measured, and
require it to stay within the invocation's 1 GiB (1,073,741,824 bytes,
`limits.cache_bytes_total`); and fix the names it will remove. A difference, an
error, a byte total past either cap, or a filesystem call that outlives its 5 s
per-call budget (`probe-timeout`) SHALL end the stage `refused` with
`cache-changed`, nothing deleted, except where a signal received first decides
it, as stated below. Where the removal floor or the work deadline stops a read
of the preflight, or of the reopening of the first listed cache's chain that
follows it, nothing SHALL be deleted and the stop SHALL NOT be reported as a
change of state: a read that cannot start because no more than the floor
remains, or that outlives the shorter budget that the deadline set,
`work remaining less the removal floor` (`deadline-exceeded`, as "Clean bounds
its Git work and reports omitted work" states), SHALL end the stage
`not-attempted` with `target-stopped`, and the target and every later one SHALL
be `not-attempted` with `deadline-exceeded`, never `refused` with
`cache-changed`. Before it classifies any outcome of the preflight, or of the
reopening of the first listed cache's chain that follows it, whether a
difference, an error, a byte total past either cap, a `probe-timeout`, or a stop
by the removal floor or the work deadline, the stage SHALL check whether a
signal has been received, and where one has, that outcome SHALL be the signal's:
the stage SHALL end `not-attempted` with `target-stopped`, nothing deleted, the
target and every later one SHALL be `not-attempted` with `interrupted`, as at
the check before the hand-off of its first removal, never `refused` with
`cache-changed` and never `deadline-exceeded`, and the exit status SHALL be the
signal's.

After its first removal, a removal that fails, a read that runs out of its
budget, a removal whose wait the removal ceiling ends, or the removal floor
reached at a hand-off SHALL end the stage. A stage that has handed over its
first removal SHALL end `disposed` or `partial`, never `refused`, except that a
stage every one of whose handed-over removals returned without removing its
entry SHALL end `refused` with `cache-changed`, nothing deleted, as a removal
refused for a sticky directory or a filesystem made read-only after the plan,
which the plan's access check cannot see, ends it. Otherwise the entries
already removed SHALL
stay removed, recorded as permanent partial cache completion. The stage SHALL
then rescan every listed cache: it SHALL open the chain to the cache's parent
as its removals do, checking every identity, and `lstat` the cache's name
relative to that parent without following a symbolic link; a chain that does
not open, or whose identity differs, SHALL leave that cache `removed: null`;
the rescan SHALL run as a reconciliation probe, each call on a thread of its
own, never on the stage's worker, and getting `min(5 s, reserve remaining)`,
and its first call past its budget SHALL leave that cache and every later one
`removed: null`. The stage SHALL record each listed cache as removed, remaining
or not established, and end `partial` with `cache-partial`; the person SHALL be
told to re-run for a fresh plan, which lists the caches that remain. A stage
that ends `refused` or `partial` SHALL be followed by no worktree removal and no
branch change for that target.

Once per invocation, before any cache enumeration, `project clean` SHALL check
that the running platform provides `O_NOFOLLOW`, `O_DIRECTORY`, and the
descriptor-relative open, `lstat`, streaming directory enumeration, unlink,
directory removal and access check with effective ids that follows no symbolic
link. Where it
does not, no row SHALL get a cache plan: no cache enumeration
SHALL run, every row that reaches the `ignored-local-files` rung holding
ignored records SHALL stay `ignored-local-files` with `cache_disposal.reason`
`cache-unsupported-platform`, and no cache stage SHALL run. A row that an
earlier rung classifies (`stale-worktree`, `protected-default`,
`inspection-error` or `dirty`) SHALL keep that classification, with
`cache_disposal.reason` `not-candidate` where it holds ignored records, as
where the calls exist: the platform withholds the cache proof and SHALL NOT
change what an earlier rung of the ladder established.

The stage's guarantee SHALL be that it removes an entry only if, at its
whole-list preflight, the entry had the allowlisted shape, its listed cache held
exactly the number of entries that the confirmed plan recorded, and its
directory and every directory above it, up to the worktree root, carried the
identity that the confirmed plan recorded. The revalidation that the narrow
guarantee names for a target whose plan lists caches, and the residual window
it leaves, SHALL be as "Cleanup states a narrow guarantee and its residual
window" states.

#### Scenario: A symlink named like a cache is never disposable

- **WHEN** an otherwise eligible worktree's only ignored path is `__pycache__`,
  ignored by the rule `__pycache__` and a symbolic link to a directory outside
  the worktree that holds `.pyc` files
- **THEN** the path is blocking, the row is `ignored-local-files` with
  `blocking: 1`, nothing is deleted, and the outside directory and its files are
  intact
- **AND** a symbolic link `link.pyc` ignored by the rule `*.pyc`, and a
  `__pycache__` directory holding a symbolic link `x.pyc`, a file `notes.txt`
  or, on Linux, a file whose name holds the byte 0xFF before its `.pyc`, are
  blocking the same way
- **AND** a `__pycache__` directory whose parent's `lstat`, or whose own,
  stubbed, reports a device other than the worktree root's is blocking the same
  way, and on Linux a
  `__pycache__` directory under a directory whose name holds the byte 0xFF
  fails the sample test, its row `not-candidate` with that path in
  `blocking_samples`; both are untouched

#### Scenario: An ancestor swapped for a symlink before the stage

- **WHEN** a test hook, after a selected target's revalidation and before its
  cache stage, moves the target's `src` directory, an ancestor of its listed
  cache `src/pkg/__pycache__`, aside and puts at `src` a symbolic link to a copy
  of it, or to a directory outside the worktree
- **THEN** the whole-list preflight refuses with `cache-changed` before any
  removal,
  nothing is deleted in the moved directory, the copy or the outside directory,
  the target is `refused` with `state-changed`, no removal child is spawned, and
  the exit status is 2

#### Scenario: The whole list is checked before the first removal

- **WHEN** a selected target lists two caches and a test hook, after its
  revalidation and before its cache stage, moves the second listed
  `__pycache__` directory out of the worktree and makes a new directory of the
  same name and content in its place
- **THEN** the stage refuses with `cache-changed` before removing anything, the
  first listed cache is intact as well as the second, the target is `refused`
  with `state-changed`, and the exit status is 2
- **AND** when the hook instead writes `c.cpython-312.pyc` into the first listed
  `__pycache__` directory before the target's revalidation, the revalidation's
  status child prints the planned records, the preflight finds one entry more
  than the plan recorded and refuses with `cache-changed`, nothing is deleted,
  `c.cpython-312.pyc` survives, the target is `refused` with `state-changed`,
  and the exit status is 2
- **AND** in both cases, before the stop block, the human result reads `Cache
  disposal at PATH refused (cache-changed); nothing was deleted.`

#### Scenario: A file placed in a cache directory during the stage

- **WHEN** a test hook adds `notes.txt` to a listed `__pycache__` directory
  after the stage's whole-list preflight
- **THEN** the removal of that directory fails because it is not empty,
  `notes.txt` survives, the stage ends `partial` with `cache-partial`, the
  worktree is not removed, and the exit status is 2

#### Scenario: No descriptor-relative calls on this platform

- **WHEN** the platform check reports the descriptor-relative calls unavailable,
  and the batch previews and applies a repository with one merged worktree whose
  only ignored files are caches and one plain merged worktree
- **THEN** no cache enumeration runs, the first is `ignored-local-files` with
  `cache_disposal.reason: "cache-unsupported-platform"` and its caches are
  untouched, the second is selected and removed, and the exit status is 0
- **AND** when the repository also holds a dirty linked worktree with an
  ignored `local.env`, a preview classifies it `dirty`, with the dirty advice,
  and not `ignored-local-files`; its `cache_disposal.reason` is
  `not-candidate`, as where the calls exist, and not
  `cache-unsupported-platform`; and it is excluded as `dirty` and untouched

#### Scenario: A removal call that outlives its wait

- **WHEN** a selected target lists two caches and a test hook holds the first
  unlink of the second listed cache in the stage's worker until the 300 s
  removal ceiling, counted from its hand-off, has passed, and releases it after
  the result record is written
- **THEN** the stage waits for that call rather than abandoning it at the
  per-call budget, and ends `partial` with `cache-partial`; the second cache is
  `removed: null` whatever its rescan finds, the held entry is counted in
  neither `entries_removed` nor `operations.performed`, no further call is
  given to that worker, no descriptor number the held call received is returned
  by a later `os.open`, and no entry outside the listed caches is removed
- **AND** before the stop block the human result names the second cache as one
  that may still be removed, and does not say that nothing was deleted
- **AND** when the held call is instead the stage's first removal, the stage
  still ends `partial` and never `refused`
- **AND** when the hook holds the second cache's first unlink for 6 s and then
  lets it return, the stage waits for it, counts its entry and goes on

#### Scenario: Caches that grew after the plan cannot pass the run's byte cap

- **WHEN** a plan selects five targets, each listing one `__pycache__`
  directory holding two small `.pyc` files, and a test hook, after the plan is
  built and before the first target's revalidation, grows each listed `.pyc`
  file in place, its name, its type and its cache's number of entries
  unchanged, until each target's listed regular files total 250 MiB, and
  `--all-safe --apply --yes` runs
- **THEN** the first four targets pass their revalidations and preflights, the
  run's byte total reaching 1,000 MiB, and their caches are disposed of and
  their worktrees removed as without the hook, their branches kept
- **AND** the fifth target passes its revalidation, but its preflight finds
  that its 250 MiB would take the run's byte total past 1 GiB, so its stage
  ends `refused` with `cache-changed` and nothing in it is deleted, the target
  is `refused` with `state-changed` and carries its reconciliation, no removal
  child is spawned for it, and the exit status is 2
- **AND** before the stop block the human result reads `Cache disposal at PATH
  refused (cache-changed); nothing was deleted.`
