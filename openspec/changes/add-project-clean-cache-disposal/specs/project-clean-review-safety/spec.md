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
at most five Git children, a fresh manifest read and the `modules` check, run in
this order and stopping at the first difference: the identity probe in the
command directory; the manifest re-read; the registry listing; one ref listing
that names the merge-target candidates, `refs/remotes/origin/HEAD`, and the
selected branches and their upstreams; the target's identity and its `modules`
check, by filesystem reads; and, inside the target worktree, the combined status
probe, which SHALL print no record, or, for a target whose plan lists caches,
the child of the cache enumeration that "Clean disposes of listed caches before
a worktree removal" defines, which SHALL print exactly the ignored records that
the plan listed and no other record, then the hidden-state probe. It SHALL
compare the recorded repository identity (`root`, `common_dir`, `dev`, `ino`),
the target's worktree identity (`path`, `dev`, `ino`, `admin_id`) and two-way
registration, its branch evidence (`branch`, `head`, `upstream`, `upstream_oid`,
`ahead`, `behind`), every baseline signature field of the target, its `locked`
flag, the manifest's `tracking_branch`, and the merge target's `name`, `source`
and `sha`, re-resolved from the fresh manifest read.

A difference SHALL refuse the target, spawn nothing, attempt no later target and
exit 2, with the reason `identity-changed` for a repository or worktree identity
or registration difference or a missing registry entry, `branch-changed` for a
different branch name or head, `state-changed` for any other signature, lock,
manifest, merge-target or listed-cache difference and for a cache stage that
ends `refused` or `partial` as "Cache disposal never follows a symlink or leaves
its worktree" states, `contains-submodule` for a new gitlink or
`modules` entry, and `hidden-local-state` for a newly flagged index entry. A
value that was null in the plan and is null at revalidation, such as the
`upstream_oid`, `ahead` and `behind` of a selected row whose upstream was
deleted, SHALL NOT count as a difference; a value that cannot be re-read, a
filesystem call that times out included, SHALL count as a difference. The first
target's repository-wide checks SHALL serve as
the preflight of every selected target, so that a difference found there removes
nothing at all. Push and delete-branch SHALL keep the full re-inspection, and
SHALL refuse with `inspection-incomplete`, `inspect-cap` or `deadline-exceeded`
and exit 2 when it is incomplete. Git's own non-force check SHALL be the last
defense only on the pinned configuration that the removal command carries:
`status.showUntrackedFiles=normal`, `core.untrackedCache=false` and
`core.fsmonitor=false`; the protocol pins that every Git child, except the push
child, carries (`-c protocol.allow=never` and the six per-protocol pins) are no
part of that defense.

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

#### Scenario: A cache target changes before revalidation

- **WHEN** a confirmed plan's first target lists caches, and before its
  revalidation an ignored `local.env` is created in it, a new ignored
  `__pycache__` directory appears in it, or one of its listed caches is deleted
- **THEN** its revalidation's status child prints a record the plan did not
  list, or lacks one the plan listed, the target is `refused` with
  `state-changed`, no cache entry is deleted and no child is spawned, later
  targets are `not-attempted`, and the exit status is 2

## ADDED Requirements

### Requirement: Cache disposal never follows a symlink or leaves its worktree

A listed cache SHALL NOT be a symbolic link, nor SHALL any directory between it
and the worktree root, nor any entry inside a listed directory; every such
directory SHALL be on the device of the worktree root; and the cache's path
SHALL be valid UTF-8. An ignored path that fails any of these SHALL be blocking,
and its row SHALL be preserved as "Cleanup preserves all local work not proven
disposable" states. Neither the cache enumeration nor the cache stage SHALL ever
follow a symbolic link, so that its target, inside or outside the worktree, is
never read, listed or changed by them, and a file with other hard links SHALL
lose only its name inside the worktree.

The cache stage SHALL use descriptor-relative operations only. It SHALL open the
worktree root by the target's recorded path with `O_DIRECTORY` and `O_NOFOLLOW`
and require the opened directory's device and inode to equal the target's
recorded worktree identity; it SHALL open every directory below the root
relative to its parent's descriptor with `O_DIRECTORY` and `O_NOFOLLOW`, and
require each opened directory's device and inode to equal those that the plan
recorded for it. It SHALL remove a file by an unlink relative to its directory's
descriptor, and a directory by a removal relative to its parent's descriptor
only after removing every entry it listed there. It SHALL NOT use a recursive
deletion, a check by path name followed by a deletion by path name, `git clean`,
or any child process. A directory that still holds an entry when its removal is
attempted SHALL be left in place, with that entry untouched.

Before its first removal the stage SHALL run a whole-list preflight: it SHALL
open and check every directory that the target's `cache_disposal.directories`
lists; re-list every listed cache directory, requiring each entry to have the
allowlisted shape, each nested directory to carry its planned identity, and the
target's cache entries and bytes to stay within the per-worktree caps; require
every listed file to be a regular file; and fix the names it will remove. A
difference, an error, or a filesystem call that runs out of its budget SHALL end
the stage `refused` with `cache-changed`, nothing deleted.

After its first removal, a removal that fails, a filesystem call that runs out
of its budget, or the removal floor reached SHALL end the stage. The entries
already removed SHALL stay removed, recorded as permanent partial cache
completion. The stage SHALL then rescan every listed cache with an `lstat`
relative to the worktree root's descriptor that follows no symbolic link, record
each as removed, remaining or not established, and end `partial` with
`cache-partial`; the person SHALL be told to re-run for a fresh plan, which
lists the caches that remain. A stage that ends `refused` or `partial` SHALL be
followed by no worktree removal and no branch change for that target.

Once per invocation, before any cache enumeration, `project clean` SHALL check
that the running platform provides `O_NOFOLLOW`, `O_DIRECTORY`, and the
descriptor-relative open, `lstat`, directory listing, unlink and directory
removal. Where it does not, no row SHALL get a cache plan: no cache enumeration
SHALL run, every row that holds ignored records SHALL stay `ignored-local-files`
with `cache_disposal.reason` `cache-unsupported-platform`, and no cache stage
SHALL run.

The stage's guarantee SHALL be that it removes an entry only if, at its
whole-list preflight, the entry had the allowlisted shape and its directory and
every directory above it, up to the worktree root, carried the identity that the
confirmed plan recorded. For a target whose plan lists caches, the revalidation
that "Cleanup states a narrow guarantee and its residual window" names SHALL be
the one performed immediately before its cache stage, and nothing SHALL run
between the stage and the spawn but the removal floor and signal checks. A cache
recreated after the stage, like any ignored file created after that
revalidation, SHALL be outside the contract: Git's non-force removal deletes it
with the worktree, and the residual-window line SHALL say so.

#### Scenario: A symlink named like a cache is never disposable

- **WHEN** an otherwise eligible worktree's only ignored path is `__pycache__`,
  ignored by the rule `__pycache__` and a symbolic link to a directory outside
  the worktree that holds `.pyc` files
- **THEN** the path is blocking, the row is `ignored-local-files` with
  `blocking: 1`, nothing is deleted, and the outside directory and its files are
  intact
- **AND** a symbolic link `link.pyc` ignored by the rule `*.pyc`, and a
  `__pycache__` directory holding a symbolic link `x.pyc` or a file `notes.txt`,
  are blocking the same way

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
  revalidation and before its cache stage, replaces the second listed
  `__pycache__` directory by a new directory of the same name and content
- **THEN** the stage refuses with `cache-changed` before removing anything, the
  first listed cache is intact as well as the second, the target is `refused`
  with `state-changed`, and the exit status is 2

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

#### Scenario: A cache recreated after the cache stage

- **WHEN** a test hook recreates `src/pkg/__pycache__/a.cpython-312.pyc` after a
  target's cache stage and before its removal child starts
- **THEN** Git removes the worktree with exit 0, the target is `removed`, the
  file is gone, and the confirmation and the result carry the residual-window
  line that names it; this documents the boundary rather than a guarantee
