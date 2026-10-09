## MODIFIED Requirements

### Requirement: Cleanup preserves all local work not proven disposable

Cleanup SHALL treat ignored local files, dirty work, detached state, an unknown
default branch, and remote divergence as preservation or review states. It SHALL
also treat as preservation states the main worktree; a locked worktree; a
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
removal.

#### Scenario: A merged worktree has ignored local files

- **WHEN** a non-current merged worktree contains ignored files
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

### Requirement: Cleanup revalidates destructive actions

Cleanup SHALL re-inspect the selected target after confirmation and before a
push, worktree removal, or local branch deletion. It MUST refuse when the
state no longer matches the reviewed plan.

That MUST SHALL apply at the revalidation performed immediately before each
removal child is spawned; a change after it is the residual window that "Cleanup
states a narrow guarantee and its residual window" states. A worktree removal
SHALL be revalidated by a targeted check, never by recomputing the full report:
at most five Git children, a fresh manifest read and the `modules` check, run in
this order and stopping at the first difference: the identity probe in the
command directory; the manifest re-read; the registry listing; one ref listing
that names the merge-target candidates, `refs/remotes/origin/HEAD`, and the
selected branches and their upstreams; the target's identity and its `modules`
check, by filesystem reads; and, inside the target worktree, the combined status
probe, which SHALL print no record, then the hidden-state probe. It SHALL
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
manifest or merge-target difference, `contains-submodule` for a new gitlink or
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
`core.fsmonitor=false`; the protocol pins that every Git child carries
(`-c protocol.allow=never` and the six per-protocol pins) are no part of that
defense.

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

## ADDED Requirements

### Requirement: Cleanup states a narrow guarantee and its residual window

Concurrent writers (editors, other agents, other `project` invocations, and Git
commands run by anyone else) SHALL be outside the safe contract, and cleanup
SHALL claim no lock, lease or writer-quiescence handoff. Its one guarantee SHALL
be that a removal child is spawned only if, at the revalidation performed
immediately before spawning it, the repository identity, the target's worktree
identity and branch evidence, every baseline signature field of the target, its
`locked` flag, the absence of submodules and of hidden local state in its own
index (read inside the target worktree), the manifest's `tracking_branch`, and
the merge target's name, source and SHA all equal the values in the confirmed
plan.

Ignored files created, and index flags set, after that revalidation, and any
change made after Git's own check, SHALL be outside the contract; the
confirmation and the result SHALL each state this residual window in one line.
Cleanup SHALL never delete a branch, so that a branch race cannot lose commits:
a branch change seen at revalidation SHALL refuse the target with
`branch-changed`, and one seen only by the rescan after Git removed the worktree
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
