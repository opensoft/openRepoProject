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
path that cannot be read, a registration that disagrees, an effective work tree
that is not the registered path, or a combined status probe that failed or
timed out) SHALL be classified `inspection-error` directly, whatever
its branch. A branch with no configured upstream SHALL be `unpublished`. A
branch whose configured upstream's remote-tracking ref no longer exists SHALL be
tested for local ancestry before the `remote-gone` rung: when its
`merged_into_target` is true, the row SHALL be `merged-removable`, or
`merged-current` when it is the current worktree, and otherwise it SHALL be
`remote-gone`, so that only an unmerged row is `remote-gone`.
`review-required` SHALL remain a defensive rung that no value of the evidence
model reaches.

The `ignored-local-files` rung SHALL apply to a row that holds a blocking
ignored path, one that "Clean disposes of listed caches before a worktree
removal" does not prove, in the same invocation and within its caps, to be a
listed cache, or a listed cache in a directory that the access check of that
requirement finds the running user cannot change. A row whose every ignored
path that requirement proves a listed cache within its caps, and passes that
check, SHALL pass that rung and be classified by the rungs below it. A cache
enumeration that fails or times out SHALL leave the row's ignored
paths unproven, and SHALL NOT make the row `inspection-error`. A row's cache
proof SHALL count as its evidence, though the invocation's cache caps, applied
in canonical order, can withhold it.

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
instead of it. For a locked worktree, which `git worktree remove --force`
refuses, the recovery text SHALL instead be "inspect, unlock it, then `git
worktree remove --force <path>` by hand". A status stream stopped at its record
bound SHALL be judged on the records read. The note SHALL be advisory and SHALL
NOT change the row's classification, the ladder or any gate.

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
- **AND** when that worktree is also locked, the recovery text shown is
  "inspect, unlock it, then `git worktree remove --force <path>` by hand"
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
core.fsmonitor=false -c core.trustctime=true -c core.checkStat=default -c
protocol.allow=never -c protocol.file.allow=never -c
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
--force <path>` by hand" where the rescan finds both its `.git` file and its
registry entry present, and "inspect, then `git worktree prune` and delete
`<path>` by hand" otherwise, as where either is gone, Git refusing `git worktree
remove --force` while the path remains; the reason SHALL be `removal-ceiling` in
both cases. Where the rescan cannot read that `.git` file, the read failing
other than for the file's absence or cut at its budget, the recovery text SHALL
instead be "inspect `<path>` by hand; its `.git` could not be read, so do not
run `git worktree prune` until it can", since `git worktree prune` deletes the
administrative directory of a worktree whose `.git` Git cannot stat, even a
live one.

For a removal named by `--worktree P`, the plan's completeness SHALL be the
repository-wide evidence plus P's own row: another row's `inspection-error`, its
omission by the row cap, or its being left unprobed SHALL be recorded in the
plan as a non-blocking omission and SHALL NOT refuse P, while P's own inspection
and revalidation stay fully strict. P SHALL be probed first and SHALL be exempt
from the row cap.

It SHALL remove a local branch only as a separate, explicit action after the
worktree is gone and the branch is verified merged.
It MUST never use a force removal, reset, or deletion of unmerged work.
Branch deletion SHALL refuse, before its plan is shown, with exit status 2,
no code, a message after `REFUSED: ` on standard error and no `git branch
-d`: the default branch; a branch that a present linked worktree holds; a
branch that the main worktree holds; and a branch that the plan's evidence
does not show merged into the merge target, by its ref listing and its merged
set, so that a branch merged only into the current branch is refused, where
`git branch -d` alone would delete it. The message SHALL be the baseline's,
except for a branch that the main worktree holds, where the baseline's message
names a removal that Git refuses for the main worktree: that message SHALL
instead name detaching HEAD in the main worktree, or checking out the merge
target there, and then retrying.

#### Scenario: Remove a merged clean worktree

- **WHEN** the user requests removal of a clean linked worktree whose branch
  is an ancestor of the target branch
- **THEN** the command confirms and removes that worktree, while refusing to
  remove its branch unless the user separately requests branch deletion

#### Scenario: Branch deletion refuses a branch it may not delete

- **WHEN** `--apply --action delete-branch --branch B --yes` names, in turn:
  the merge target, while the main worktree is on another branch; a branch
  merged into the merge target that a linked worktree holds, and one that the
  main worktree holds; and a branch merged into the main worktree's current
  branch, which is not the merge target, but not into the merge target
- **THEN** each refuses with exit 2, printing nothing on standard output and
  on standard error only `REFUSED: ` followed, in turn, by `The default
  branch is protected and cannot be deleted.`, `Remove the linked worktree
  first; branch deletion is a separate action.`, `Branch B is checked out in
  the main worktree; detach HEAD there, or check out T there, then retry.`
  and `Branch B is not verified as merged into T.`, T the merge target
- **AND** no `git branch -d` runs, and every branch and worktree is kept

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
- **AND** the recovery text is "inspect, then `git worktree remove --force
  <path>` by hand" while the target's `.git` file and registry entry both
  remain, and "inspect, then `git worktree prune` and delete `<path>` by hand"
  once the `.git` file is gone, its path and registry entry remaining, or once
  the registry entry is gone, its path remaining
- **AND** where the rescan cannot read the target's `.git` file, as when a
  directory above it denies search, the recovery text is instead "inspect
  `<path>` by hand; its `.git` could not be read, so do not run `git worktree
  prune` until it can", whatever the rescan finds of the registry entry, since
  `git worktree prune` would delete that live worktree's administrative
  directory

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

### Requirement: Clean previews and applies a batch of eligible worktree removals in one repository

`project clean <root> --all-safe [--json] [--apply [--yes] [--expect-plan D]]`
SHALL plan every eligible linked worktree of one resolved repository, and never
of a sibling, a family member, a mounted leg, a pinned member copy or an
independent clone. `--all-safe` SHALL NOT be combined with `--action`,
`--branch` or `--worktree`; `--expect-plan` SHALL require `--all-safe --apply`
and a value of 64 lowercase hexadecimal characters; any violation SHALL refuse
with `invalid-arguments` and exit status 2.

A worktree row SHALL be selected only when it passes every gate. Each excluded
row SHALL carry one `reason`, its first failing gate in this order:
`main-worktree`; `unsupported-path-bytes`; `registration-mismatch`;
`locked-worktree`; the row's classification when it is not `merged-removable`;
`not-requested`, for an eligible row other than the named one in a single-target
removal; `unstarted-branch`, or `reflog-unavailable` where the reflog cannot
decide it; `deferred-target-cap`; `contains-submodule`; `hidden-local-state`;
`operation-in-progress`; and `worktree-only-commits`. A head equal to the merge
target's SHA SHALL NOT by itself prove a branch unstarted, because a branch
fast-forward merged into the target sits at the target's tip, so the gate
SHALL read the branch's reflog, `logs/refs/heads/<branch>` in the common
directory, for every row it checks,
from the filesystem, at most 64 KiB, counted in the filesystem budget and never
by a Git child. The reflog's anchor SHALL be its last surviving entry whose old
object is all zeros, as every entry that creates the branch has, whatever
command wrote it (`git fetch <remote> <ref>:<branch>`, `git update-ref` and
`git push .` among them), or whose message begins `branch: Created from` or
`branch: Reset to`; an entry whose old object is all zeros SHALL NOT be a
movement. A movement SHALL be an entry after the anchor, or any entry when no
anchor survives, whose old and new objects are non-zero and differ; an entry
whose old and new objects are equal, as a rename writes, SHALL NOT be a
movement. A branch whose last reflog entry's new object differs from its
current head SHALL be `reflog-unavailable`; otherwise a branch with a movement
SHALL pass the gate, its head equal to the merge target's SHA or not, and a
branch whose anchor survives with no movement after it, the anchor's new object
equal to its current head, SHALL be `unstarted-branch`. One
outcome rule SHALL govern the read: a reflog that is missing (`ENOENT` or
`ENOTDIR`), empty (0 bytes) or read to its 64 KiB bound, or whose surviving
entries cannot decide, no anchor and no movement surviving included, SHALL make
that row `reflog-unavailable`, at the gate's place in this order; any other
error on the read SHALL make that row `inspection-error`, as any failed row
probe does; a read not finished within the filesystem budget, the deadline not
being the limit, SHALL leave the row unprobed and the plan incomplete with
`inspection-incomplete`, except a read of the cache walk that times out, which
leaves its row `cache-unverified` and the plan complete, as "Clean disposes of
listed caches before a worktree removal" states; and a read that the deadline
cuts SHALL record
`deadline-exceeded` and leave the row unprobed and the plan incomplete with
`deadline-exceeded`, not `inspection-incomplete`, as for every other filesystem
read. A row SHALL be excluded as `contains-submodule`
when its index holds any gitlink or its worktree administrative directory holds
a `modules` entry, and as
`hidden-local-state` when its index flags any entry assume-unchanged or
skip-worktree, sparse checkouts included; the index SHALL be read inside the
row's own worktree, and both gates SHALL be checked only for rows that pass
every earlier gate.

A row SHALL be excluded as `operation-in-progress` when its own administrative
directory, `<common_dir>/worktrees/<admin_id>`, holds an entry of any kind
named `MERGE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `BISECT_LOG`,
`BISECT_START`, `rebase-apply`, `rebase-merge`, `sequencer`,
`MERGE_AUTOSTASH`, `NOTES_MERGE_PARTIAL` or `NOTES_MERGE_REF`: the markers by
which Git knows that a merge, a cherry-pick or revert or a sequence of them, an
`am` or a rebase, a bisect, or a notes merge is in progress there, or that a
merge holds an autostash, and which the removal would delete with that
directory, even where the operation left the index and the working tree
unchanged. The gate SHALL read that directory by one listing, counted in the
filesystem budget and never by a Git child. One outcome rule SHALL govern the
gate: a marker present SHALL make the row `operation-in-progress`; an error on
the listing SHALL make the row `inspection-error`, as any failed row probe does,
so that the plan is incomplete with `inspection-incomplete`; a listing not
finished within the filesystem budget, the deadline not being the limit, SHALL
record `probe-timeout` and make the row `inspection-error` likewise; and the
deadline passing SHALL leave it incomplete with `deadline-exceeded`, as for
every other read.

A row SHALL be excluded as `worktree-only-commits` when a commit that its own
HEAD reflog or a ref under its own `refs/worktree/` holds is reachable from no
branch, tag or remote-tracking ref and from no non-zero object that its branch's
reflog names, because removing the worktree deletes that reflog and those refs
with its administrative directory. The gate SHALL read `logs/HEAD` in that
directory by one filesystem call, at most 64 KiB, counted in the filesystem
budget, every non-zero old and new object it names being a candidate, and SHALL
then run one Git child in the worktree, `git rev-list --max-count=1
--glob=refs/worktree <candidates> --not --branches --tags --remotes <the
non-zero objects the branch's reflog names>`, which prints a commit exactly when
one is held that way. A `logs/HEAD` that is missing (`ENOENT` or `ENOTDIR`) or
empty SHALL give no candidate. One outcome rule SHALL govern the gate, split as
the branch reflog's is, except that a read not finished within the filesystem
budget makes the row `inspection-error` here: a child that exits 0 and prints
anything, and a
`logs/HEAD` read to its 64 KiB bound or holding a line that cannot be parsed,
SHALL each make the row `worktree-only-commits`, at the gate's place in this
order; any other error on the read, and a child that cannot be started or exits
nonzero, as on a missing object, SHALL make the row `inspection-error`, as any
failed row probe does; a child stopped at its 5 s budget, the deadline not being
the limit, SHALL record `probe-timeout` and make the row `inspection-error`, and
so SHALL a read not finished within the filesystem budget; and a read or child
that the deadline cuts SHALL record `deadline-exceeded`. Each of those four
SHALL leave the plan incomplete, with `inspection-incomplete` or
`deadline-exceeded`, as for every other read and child.

`selected` and `excluded` SHALL be in canonical order, by raw path bytes, and
that order SHALL be the execution order. Once a plan is built, these checks
SHALL run in this order: an incomplete plan SHALL be refused first, a preview or
report exiting 1 and a run with `--apply` refusing with exit status 2 before any
question; an `--expect-plan` mismatch SHALL then refuse with
`plan-digest-mismatch` and exit status 2; and only then SHALL a complete
`--all-safe` plan whose selection is empty print "No eligible worktrees" and
exit 0 without asking. In `mode: "single"`, a P that a gate excludes SHALL
refuse with `target-excluded` and exit status 2, as below, and SHALL NOT be
treated as an empty selection.

`--apply` SHALL always build, print and confirm its own fresh plan; a preview
SHALL be advisory and SHALL never be stored or reused. The plan SHALL carry
`plan_digest`, the lowercase hexadecimal SHA-256 of a canonical JSON text of the
repository's four identity fields, the merge target's name and SHA, and the
selected `[path, branch, head]` triples in canonical order, so that a change to
an excluded row leaves it unchanged. After the triple of each selected target
whose plan lists caches, as "Clean disposes of listed caches before a worktree
removal" states, the canonical text SHALL carry that target's listed cache paths
as `[path, kind]` pairs and its planned cache directories as `[path, dev, ino]`
triples, each in canonical order, so that a listed cache that appears,
disappears or changes kind, or a cache directory with another identity, changes
the digest; the canonical text of a plan that selects no such target SHALL
carry no such pair or triple. `--expect-plan D` SHALL refuse with
`plan-digest-mismatch` and exit status 2, before any question and any mutation,
when the fresh digest differs from D, and SHALL still print the fresh plan. The
confirmation SHALL be one default-No question naming the count of worktrees to
remove and of branches kept, ending `[yes/N]`; only `yes`, surrounding
whitespace ignored, SHALL accept it, and any other answer SHALL refuse with
`cancelled` and exit status 2. This question SHALL replace `Type yes to run this
plan:` for `clean`'s removal apply only, and `--yes` SHALL accept the fresh plan
without asking.

A single-target removal, `--apply --action remove --worktree P`, SHALL keep its
flags and SHALL be a one-item batch: it SHALL build the same plan with `mode:
"single"`, select only P, list every other eligible row as `not-requested`, and
share the batch's sequence, refusal codes, stages and exit codes. A P that
matches no registry entry SHALL refuse with `worktree-not-found`, and a P that a
gate excludes SHALL refuse with `target-excluded`, whose `reason` carries the
exclusion reason and whose message keeps the existing wording for the current
worktree and for a class that is not removable. Every refusal that blocks a
plan, in either mode, SHALL name a manual remedy: `git worktree prune`, `git
worktree repair`, unsetting `core.worktree` and `core.bare` in the repository's
`config` or in a worktree's `config.worktree`, or removing the offending row by
hand, as the cause fits.

The human preview SHALL list the selected rows, then the excluded rows grouped
by reason, each group with its next step; an `ignored-local-files` exclusion
SHALL show its bounded count and the first ignored path observed. A successful
apply SHALL print `Removed N; branches kept: ` followed by the branches kept.

#### Scenario: Stable order and preserved work

- **WHEN** several eligible linked worktrees exist beside current, merge-target,
  dirty, locked, remote-ahead and unmerged ones, and `--all-safe --apply --yes`
  runs
- **THEN** the eligible worktrees are removed in canonical path order, the
  others remain, every retained local branch is reported, and no push, fetch,
  force option, branch deletion or remote deletion occurs
- **AND** the same holds when the merge-target branch is checked out in no
  worktree, the main worktree being on another branch: every removal runs from
  the command directory and succeeds

#### Scenario: Every protected classifier

- **WHEN** one repository's linked worktrees are stale, detached, dirty, holding
  ignored files that are not Python bytecode caches, unpublished, remote-gone,
  diverged, remote-ahead, unpushed, pushed-unmerged, merged but current, merged
  but locked, merged with a
  non-UTF-8 path, merged with an initialized submodule, and merged with an
  assume-unchanged entry, beside the main worktree on the merge target and
  exactly one plain merged, clean, published worktree with a commit of its own,
  and the batch previews and applies
- **THEN** only that last worktree is selected and removed, every other row is
  excluded with the reason the gate order gives, and the exit status is 0
- **AND** a copy that adds one unreadable worktree, or one with a broken
  administrative registration, yields `inspection-error`, an incomplete plan,
  and exit 2 under `--apply` with nothing removed

#### Scenario: Hidden local state

- **WHEN** otherwise eligible worktrees hold an edit to a file flagged
  assume-unchanged and a file flagged skip-worktree, each flag set only in that
  worktree's own index while the main worktree's index flags nothing, and the
  batch previews
- **THEN** both are excluded as `hidden-local-state`, because their own indexes
  were read, and the edits survive
- **AND** when such a flag is set on a selected target after confirmation and
  before its revalidation, that target is `refused` with `hidden-local-state`,
  later targets are `not-attempted`, and the exit status is 2

#### Scenario: Submodules

- **WHEN** otherwise eligible worktrees hold an initialized submodule, a
  submodule initialized and then deinitialized, a gitlink never initialized, and
  an administrative `modules` entry left after the gitlink was removed, beside
  one plain eligible worktree, and the batch previews and applies
- **THEN** the first four are excluded as `contains-submodule` and only the
  plain worktree is removed
- **AND** when a `modules` directory is created in a selected target's
  administrative directory before its revalidation, that target is `refused`
  with `contains-submodule`, later targets are `not-attempted`, and the exit
  status is 2

#### Scenario: An operation in progress

- **WHEN** otherwise eligible linked worktrees each hold, with an index and a
  working tree equal to their branch head: a `git am` that failed on a patch
  that does not apply; a `git cherry-pick` of two commits stopped at a conflict
  on the first and resolved to the branch's own content; a `git merge
  --no-commit -s ours` of another branch; a `git notes merge` stopped at a
  conflict; and a `git bisect start --no-checkout`
- **THEN** the combined status probe prints no record for any of them,
  `--all-safe` excludes each as `operation-in-progress`, and `--all-safe
  --apply --yes` removes none of them
- **AND** `--apply --action remove --worktree` naming one refuses with
  `target-excluded`, reason `operation-in-progress`, and exit 2
- **AND** once each operation is aborted (`git am --abort`, `git cherry-pick
  --abort`, `git merge --abort`, `git notes merge --abort` and `git bisect
  reset`), each worktree is selected as before, although the aborted notes
  merge leaves its `NOTES_MERGE_WORKTREE` directory behind
- **AND** a worktree whose administrative directory cannot be listed, its read
  permission removed while its `gitdir` file stays readable, is
  `inspection-error`, the plan is incomplete with `inspection-incomplete`, the
  preview exits 1, and `--all-safe --apply --yes` refuses with exit 2 before
  any removal

#### Scenario: A squash merge that holds an autostash

- **WHEN** an otherwise eligible linked worktree has an edit to a tracked file
  and runs `git merge --squash --autostash -s ours` of another branch, on a
  Git that keeps the autostash until the squash is committed, as 2.40.4 and
  2.43.0 do, so that only `MERGE_AUTOSTASH` in its administrative directory
  holds the edit, `git stash list` is empty and the combined status probe
  prints no record
- **THEN** `--all-safe` excludes it as `operation-in-progress`, and
  `--all-safe --apply --yes` leaves the worktree and its `MERGE_AUTOSTASH` in
  place, where before this change the non-force removal exited 0 and left the
  edit unreachable
- **AND** on Git 2.36.6, which applies the autostash at once, the edit is back
  in the working tree and the row is excluded as `dirty`

#### Scenario: A commit held only by the worktree

- **WHEN** one otherwise eligible linked worktree had its HEAD detached, a
  commit made there and its branch checked out again, so that only its HEAD
  reflog holds that commit, and another holds a commit made the same way that
  only its `refs/worktree/keep` holds
- **THEN** `--all-safe` excludes both as `worktree-only-commits`,
  `--all-safe --apply --yes` removes neither, and both commits stay reachable
  from their worktrees
- **AND** `--apply --action remove --worktree` naming either refuses with
  `target-excluded`, reason `worktree-only-commits`, and exit 2
- **AND** once the first commit is tagged, and a branch is made at the second
  and its `refs/worktree/keep` deleted, both worktrees are selected as before
- **AND** a worktree whose branch was amended and reset, so that its HEAD
  reflog names commits that only that branch's reflog still holds, is selected
  as before
- **AND** a worktree whose HEAD reflog names a commit whose object was deleted
  from the repository, so that the child exits 128 with `fatal: bad object`,
  is `inspection-error`, the plan is incomplete with `inspection-incomplete`,
  the preview exits 1, and `--all-safe --apply --yes` refuses with exit 2
  before any removal

#### Scenario: Paths and empty plans

- **WHEN** worktree paths contain spaces, an external worktree's path is
  missing, a worktree is locked, inspection is incomplete, or no row is eligible
- **THEN** the batch keeps the safety rules of the single-target command, and a
  complete plan whose selection is empty prints "No eligible worktrees" and
  exits 0 without asking
- **AND** an incomplete plan that selects nothing is refused, not reported as
  empty: its preview exits 1, and with `--apply` it refuses with exit 2 before
  asking

#### Scenario: Preview is advisory

- **WHEN** a preview selects only P1 and P1 becomes dirty before `--all-safe
  --apply --yes` runs without `--expect-plan`
- **THEN** the fresh plan excludes P1 as `dirty`, prints "No eligible
  worktrees", and exits 0 without asking
- **AND** with `--expect-plan` naming the preview's digest, the same run refuses
  with `plan-digest-mismatch` and exit 2 instead, because a digest mismatch is
  refused before an empty selection is reported

#### Scenario: Plan digest mismatch

- **WHEN** a preview with digest D selects P1, and a second merged worktree
  becomes eligible or P1's branch advances before `--all-safe --apply --yes
  --expect-plan D` runs
- **THEN** the fresh plan is printed with a different digest, the run refuses
  with `plan-digest-mismatch` and exit 2 before any question or removal, and
  nothing changes
- **AND** when only an excluded worktree changed, the digest is still D and the
  apply proceeds

#### Scenario: Invalid argument combinations

- **WHEN** `--all-safe` is given with `--action`, `--branch` or `--worktree`, or
  `--expect-plan` is given without `--all-safe --apply`, or its value is not 64
  lowercase hexadecimal characters
- **THEN** the command refuses with `invalid-arguments` and exit 2, and runs
  nothing

#### Scenario: Only yes confirms

- **WHEN** `--all-safe --apply` asks its question at a terminal and the answer
  is `y`, an empty line or `no`
- **THEN** the run refuses with `cancelled` and exit 2, and nothing is removed
- **AND** the question reads like `Remove 7 worktrees, keeping 7 branches?
  [yes/N]`, and the answer `yes` begins the apply phase

#### Scenario: The preview says what keeps each row

- **WHEN** a preview selects two rows and excludes one row as
  `ignored-local-files` and two as `dirty`
- **THEN** the selected rows are listed first, then the excluded rows grouped by
  reason, each group with its next step
- **AND** the `ignored-local-files` row shows its bounded ignored count and its
  first ignored path

#### Scenario: Cache paths are part of the plan digest

- **WHEN** a preview with digest D selects a target with listed caches, and
  before `--all-safe --apply --yes --expect-plan D` runs a new ignored
  `__pycache__` directory holding one `.pyc` file appears in it, or its listed
  cache directory is moved out of the worktree and a new directory of the same
  name and content is made in its place
- **THEN** the fresh plan has another digest, the run refuses with
  `plan-digest-mismatch` and exit 2 before any question, and no cache entry is
  deleted
- **AND** for a repository whose selected targets list no cache, the canonical
  text holds no cache pair or triple, and the digest is the one it was before
  this change

### Requirement: Clean bounds its Git work and reports omitted work

Each `project clean` invocation SHALL set one monotonic deadline 60 s after it
starts and SHALL hold back a 10 s reconciliation reserve, so that work stops 50
s after start; time spent blocked at the confirmation question SHALL NOT count,
both deadlines moving later by the time spent waiting. Each Git child SHALL get
`min(5 s, work remaining)`, and each filesystem call (`lstat`, `realpath`, the
reads of `.git`, `gitdir`, `commondir`, reflog and manifest files, the listing
of a worktree's administrative directory, and the directory opens, bounded
directory enumerations, `lstat` calls and access checks of the cache walk)
SHALL be abandoned after the
same budget, recording `probe-timeout`, or `deadline-exceeded` where the
deadline was the limit, and leaving its values null. Probing SHALL be serial.
Reconciliation probes SHALL get `min(5 s, reserve remaining)`.

The deadline SHALL bound inspection and SHALL gate only the start of a removal:
a removal child SHALL be spawned only while at least the 5 s removal floor of
the work deadline remains, and otherwise that target and every later one SHALL
be `not-attempted` with `deadline-exceeded`. A cache stage, as "Clean disposes
of listed caches before a worktree removal" states, SHALL start only while more
than that floor remains, a stricter test than the removal child's, which is
spawned while at least that floor remains, and each of its reads SHALL get
`min(5 s, work remaining less the removal floor)`, so that the floor is left for
the spawn. A cache stage SHALL hand an unlink or a directory removal to its
worker only while more than that floor remains. A removal handed over SHALL be
waited for until it returns, never abandoned at the per-call budget, and SHALL
count as a removal in flight; only the 300 s removal ceiling, counted from the
hand-off, SHALL end that wait, the listed cache that the removal belongs to
then being `removed: null`, and the reconciliation reserve SHALL count from its
return or from that ceiling. A removal child still running at
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
most 16 cache enumerations per invocation, at most 512 recorded cache objects,
its cache entries and the directories its plan records for them, and 256 MiB
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
16 in canonical order SHALL go on to the gates after it, the two index gates,
`operation-in-progress` and `worktree-only-commits`, and the rest SHALL be
excluded as `deferred-target-cap`, with the command to run next. The plan SHALL
stay complete and apply SHALL be allowed; re-running SHALL take the next 16 as
the rows ahead of them are removed or excluded by a gate before the cap, each
run building its own fresh plan and revalidating each of its targets, so that a
run that removes none of its 16, as when the deadline leaves every target
`not-attempted`, leaves its 16 to the next run. Rows that a gate after the cap
then excludes SHALL keep their places among the 16, so that when every one of
those 16 is excluded by a gate after the cap no re-run reaches a deferred row,
and the human report SHALL say why the deferred rows will not drain, naming
those gates' reasons. No plan SHALL be refused for having more than 16 such
rows. In a single-target removal the limit SHALL count P alone, because
`not-requested` precedes it.

The cache enumerations SHALL count in the fit that sets the row and target
caps: with 128 worktree rows, 16 cache enumerations and 16 targets, planning,
revalidation and the final rescan spawn at most 283 Git children besides the 16
removals where the plan read the repository's `extensions.worktreeConfig` as
false and neither the path of the repository's root nor that of its common
directory holds a line feed, about 47.3 s on the packet's basis of 150 ms per
child and 0.3 s per
removal, the cache walk's and the cache stages' filesystem calls not counted,
on which count the
first 14 targets start any cache stage and their removal child before only the
removal floor remains, and the last two are `not-attempted` with
`deadline-exceeded`; a
target whose cache stage or spawn cannot start under the removal floor SHALL be
`not-attempted` with `deadline-exceeded`, as for every removal, and a cache
stage's removal that does not return SHALL hold the run only as a removal in
flight does, up to the removal ceiling.

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
1). Revalidating one target SHALL spawn at most six Git children, seven where
the plan read the repository's `extensions.worktreeConfig` as true, and never
recompute the full report, and the final rescan at most three, except where the
path of the repository's root or of its common directory holds a line feed: `git
rev-parse` prints one value per line and has no NUL form, so the identity probe
is then read one option per child, four children in place of one, and
revalidating one target spawns at most nine Git children, ten where the plan
read `extensions.worktreeConfig` as true, and the final rescan at most six. The
plan's `probes.estimated` SHALL count those extra children.

#### Scenario: Row cap and planning failures

- **WHEN** more than 128 worktree rows are registered, or a probe times out or
  the deadline passes during planning, and `--all-safe` previews
- **THEN** the plan is incomplete with `inspect-cap`, `inspection-incomplete` or
  `deadline-exceeded`, `omitted` and the timed-out rows are visible, the main
  worktree and the 127 linked worktrees with the smallest paths are the ones
  inspected, and the preview exits 1
- **AND** `--apply` refuses with exit 2 before any mutation
- **AND** where the cause is the row cap, that refusal names the remedy "{N}
  rows exceed the row cap of {M}; remove worktrees explicitly, or prune stale
  entries by hand; if a worktree's path cannot be read, do not run git worktree
  prune until it can", whether or not any inspected row's path was read, since
  the rows past the cap are never read

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

- **WHEN** a repository without `extensions.worktreeConfig` has five worktree
  rows, three of them selected, and `--all-safe --apply --yes` runs under a
  counting `git` wrapper on PATH
- **THEN** every target's revalidation spawns at most six children, the final
  rescan spawns three, three removals run, no merged-set listing and no status
  probe of a non-selected worktree runs after confirmation, and the record's
  `probes.performed` equals the wrapper's count of children other than the three
  removals, and its `operations.performed` is 3
- **AND** every `status`, `ls-files` and `rev-list` child names its own
  worktree as its directory, and every other child after resolution, the
  removals included, names the command directory

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

### Requirement: Clean records a reconcilable result for every removal target

The apply phase SHALL begin when the question is answered `yes` or `--yes` is
accepted. Each selected target SHALL end in one stage with one reason:

- `removed`: the child exited 0, was killed at the hard ceiling, or ended with
  an exit that could not be observed, and the rescan shows its registry entry
  and its path both absent, with `reconciled` true; reason null,
  `branch-advanced-after-removal`, `branch-missing-after-removal` or
  `removal-ceiling`;
- `refused`: revalidation found a difference, or a cache stage ended `refused`
  or `partial`, and nothing was spawned; `identity-changed`, `branch-changed`,
  `state-changed`, `contains-submodule`, `hidden-local-state`,
  `operation-in-progress` or `worktree-only-commits`;
- `failed`: the child exited nonzero on its own, whether or not a signal reached
  `project`, or could not be spawned; `git-refused` for exit status 128,
  `git-failed` for any other status (128 plus the signal number when a signal
  that `project` did not send ended the child), or `spawn-error`;
- `unknown`: a child ran, or an exception interrupted the target, and removal is
  not proven; `unconfirmed-removal`, `reconciliation-incomplete`,
  `internal-error` or `removal-ceiling`;
- `not-attempted`: the run stopped before reaching the target, or before
  spawning its removal because less than the removal floor remained or the
  work deadline cut its revalidation, or, for a target whose cache stage ended
  `disposed`, before its removal was spawned because a signal had been
  received or less than the removal floor remained; `batch-stopped`,
  `interrupted` or `deadline-exceeded`.

A removal child that exits nonzero on its own SHALL be `failed` with Git's
status, `git-refused` for 128 and `git-failed` otherwise, whether or not a
signal reached `project`. Only for a child that `project` killed at the ceiling,
or whose exit could not be observed, SHALL the rescan decide between `removed`
and `unknown` with the note `partially-removed`; `removal-ceiling` SHALL name
the ceiling cause. `pending` SHALL appear only in the printed plan and progress.
Every `removed`, `refused`, `failed` or `unknown` target SHALL carry a
`reconciliation` object (`registry_entry_present`, `path_present`,
`branch_present`, `branch_sha`, `reconciled`), and a `not-attempted` target
SHALL carry null, except one whose cache stage removed at least one entry, which
SHALL carry its reconciliation. The child's exit status alone SHALL never prove
a removal. The
rescan SHALL first re-establish the repository identity, and where it differs
every reconciliation field SHALL be null and `reconciled` false. A target's
`notes` SHALL list `orphaned-directory` when its registry entry is absent and
its path present, and `partially-removed` when its removal child was killed at
the ceiling, or its exit could not be observed, and the rescan shows its
registry entry or its path remaining; a `partially-removed` target SHALL show
the recovery text "inspect, then `git worktree remove --force <path>` by hand"
where the rescan finds both its `.git` file and its registry entry present, and
"inspect, then `git worktree prune` and delete `<path>` by hand" otherwise, as
where either is gone, Git refusing `git worktree remove --force` while the path
remains. The rescan SHALL read the `.git` file by one `lstat`, a filesystem call
that starts no Git child. Where that `lstat` fails other than for the file's
absence, or is cut at its budget, the recovery text SHALL instead be "inspect
`<path>` by hand; its `.git` could not be read, so do not run `git worktree
prune` until it can", since `git worktree prune` deletes the administrative
directory of a worktree whose `.git` Git cannot stat, even a live one.

Before the apply phase, SIGINT, SIGTERM or SIGHUP SHALL terminate and reap every
probe child, print "Cancelled." on standard error and no JSON document, and exit
130, 143 or 129 with nothing mutated, and end of input at the question SHALL
exit 130 the same way. During the apply phase, the first of
those signals received SHALL set the exit status and stop scheduling, so that no
further probe or removal starts, a cache stage that has handed over its first
removal running to its end as "Clean disposes of listed caches before a
worktree removal" states. A removal
in flight SHALL be waited for, and
its target SHALL end by the stage rule above. Targets not yet started SHALL be
`not-attempted` with `interrupted`. `project` SHALL then reconcile within the
reserve and print the result record; a second SIGINT during reconciliation SHALL
abandon the remaining rescans, leaving their fields null; after SIGHUP the
record SHALL be printed on a best-effort basis. An exception while handling a
target after the apply phase began SHALL make that target `unknown` with
`internal-error` and later targets `not-attempted`; an unexpected exception
before the apply phase SHALL refuse with `internal-error` and exit status 2. No
`unknown` or `failed` target SHALL be retried automatically, and `project` SHALL
never force a removal or delete a directory itself, with one exception: a cache
stage's descriptor-relative deletion of its target's listed cache paths, the
cache directories it has emptied included, as "Clean disposes of listed caches
before a worktree removal" states.

The exit status of a run with `--apply` SHALL be the first row that matches:

1. 130, 143 or 129: a signal was received, the first one received deciding, or
   input ended at the question (130);
2. 1: the deadline stopped work after the apply phase began, any target is
   `unknown`, any target's reason is `removal-ceiling`, or a cache stage's
   removal reached the removal ceiling;
3. Git's own status, passed through unchanged: a target is `failed` with
   `git-refused` or `git-failed`;
4. 2: any refusal; a `refused` target; a `removed` target with a
   branch-after-removal reason; a `failed` target with `spawn-error`;
5. 0: every selected target is `removed` with reason null, or nothing is
   eligible.

A preview or report SHALL exit 2 only for a refusal raised before a plan is
built, 1 for an incomplete plan, and 0 otherwise, the signal exits above
excepted.

A run that stops SHALL end its human result with `Stopped at P (reason). Removed
k of n. Not attempted: ... Next: ` followed by the command that shows a fresh
read-only plan, and SHALL name every retained branch.

#### Scenario: Exit 0 without evidence

- **WHEN** a test Git exits 0 without removing anything
- **THEN** the target is `unknown` with `unconfirmed-removal`, later targets are
  `not-attempted`, and the exit status is 1

#### Scenario: A signal during a removal

- **WHEN** SIGINT arrives while the second of three removals is in flight
- **THEN** the removal child is not signalled and is waited for; the second
  target is `removed` when the child exits 0 and the rescan shows its registry
  entry and path gone, and `failed` with Git's status when the child exits
  nonzero on its own; the third is `not-attempted` with `interrupted`; and the
  exit status is 130
- **AND** SIGTERM in the same place exits 143, and SIGHUP 129
- **AND** SIGINT or end of input at the confirmation question exits 130 with
  nothing removed

#### Scenario: SIGTERM before the apply phase

- **WHEN** SIGTERM arrives while the plan is being built and a probe child of a
  fake `git` that ignores SIGTERM is running
- **THEN** the probe child's process group is killed 2 s after the SIGTERM and
  reaped, no process of that group remains, nothing is mutated, and the exit
  status is 143
- **AND** under `--json` standard error carries `Cancelled.` and standard output
  holds no JSON document

#### Scenario: Git leaves an orphaned directory

- **WHEN** a target contains a subdirectory without write permission, and Git
  unregisters the worktree but fails to delete its directory and exits 255
- **THEN** the target is `failed` with `git-failed` and `exit_status: 255`, its
  reconciliation shows `registry_entry_present: false`, `path_present: true` and
  the retained branch with its SHA, its `notes` is `["orphaned-directory"]`,
  later targets are `not-attempted`, and the exit status is 255
- **AND** no later plan lists the directory, and nothing deletes it

#### Scenario: Git refuses the removal

- **WHEN** a lock is added to a target after its revalidation
- **THEN** Git refuses with exit status 128, the target is `failed` with
  `git-refused`, the record holds the command, the exit status 128 and a
  reconciliation with the registry entry and path present, later targets are
  `not-attempted`, every retained branch is reported, and the exit status is 128

#### Scenario: Unreadable path after removal

- **WHEN** a test hook makes the target's parent directory unreadable after Git
  exits 0
- **THEN** the rescan's `lstat` fails, `path_present` is null, `reconciled` is
  false, the target is `unknown` with `reconciliation-incomplete`, the record is
  printed, and the exit status is 1

#### Scenario: Exception after the apply phase begins

- **WHEN** a fault is injected into the first target's reconciliation
- **THEN** that target is `unknown` with `internal-error`, later targets are
  `not-attempted`, the result record is printed, and the exit status is 1

#### Scenario: The stop block

- **WHEN** a batch of three stops at its second target, refused with
  `branch-changed`
- **THEN** the human result reads `Stopped at <second path> (branch-changed).
  Removed 1 of 3. Not attempted: <third path>. Next: ` followed by the command
  for a fresh read-only plan, and names every retained branch

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
`lstat` sizes of its regular files. A worktree's recorded cache objects SHALL
be its cache entries and every directory that its plan records for its cache
stage, each directory between the worktree root and a listed path included,
each counted once.

A candidate SHALL be a linked worktree row whose combined status probe
established `dirty` false after reading at least one ignored record, which
passes the sample test, and which, its ignored records disregarded, the ladder
would classify `merged-removable` and every gate that precedes
`deferred-target-cap` would pass; in `mode: "single"` only P can be a
candidate, and `--action push` and `--action delete-branch` have none. The
sample test SHALL read the row's `ignored_samples` and spawn no child: a row
fails it when any sample is a path that is not valid UTF-8, or whose last
component, a trailing `/` disregarded, is neither exactly `__pycache__` nor a
name ending exactly `.pyc` or `.pyo`, since such a path is blocking whatever it
holds. For the candidates in canonical order, at most 16 per invocation
(`limits.cache_rows`), `project clean` SHALL run one cache enumeration each,
after the row's identity is verified: one Git child in the row's own worktree,
`status --porcelain=v2 -z --untracked-files=normal --ignored=matching`,
carrying the four status pins that every status probe carries, `-c
core.untrackedCache=false -c core.fsmonitor=false -c core.trustctime=true -c
core.checkStat=default`, its own pin `-c status.showStash=false`, so that a
repository's stash never puts a `# stash` header before its records, the
protocol pins, the scrubbed environment and
`GIT_OPTIONAL_LOCKS=0` that every read-only Git child carries, under the
per-child budget and counted in `probes`; then a walk that takes the records in
canonical order, opens each directory it records once, from the worktree root
down, relative to its parent's descriptor and without following a symbolic
link, enumerates each listed or nested cache directory by a descriptor-relative
streaming enumeration that yields one entry at a time, and `lstat`s each entry
it takes, each directory open, bounded enumeration and `lstat` one filesystem
call under the per-call budget, and stops at the row's 513th recorded cache
object, closing the enumeration in hand as soon as that cap decides. No
enumeration SHALL hold a whole directory's listing, so that a row's walk holds
at most 513 entries whatever a directory holds. The walk SHALL also
check, for each
directory that a cache stage would change (each listed cache directory, each
nested `__pycache__` directory and the parent of each listed path), that the
running user may remove entries from it: one descriptor-relative access check
with effective ids, following no symbolic link, a filesystem call under the
per-call budget. The child SHALL stop at its 513th record, so that 512 records
(`limits.cache_entries`) is its bound.

A row SHALL stay at the `ignored-local-files` rung, with `cache_disposal.reason`
naming why, when its ignored paths are not all proven listed caches within the
caps, or when its cache stage could not remove them:

- `not-candidate`: it holds ignored records but is not a candidate, the sample
  test included;
- `cache-cap`: it is a candidate past the 16th; its child reached its record
  bound; its recorded cache objects exceed 512 (`limits.cache_entries`) or its
  bytes 256 MiB (268,435,456, `limits.cache_bytes`); or, every ignored path
  being a listed cache that
  passes the access check, its entries or bytes would take the invocation's
  totals, summed in canonical order over such rows, past 4,096 entries
  (`limits.cache_entries_total`) or 1 GiB (1,073,741,824,
  `limits.cache_bytes_total`), its own then not counted, nor those of a row
  ahead of it that a gate after `deferred-target-cap` excludes, the plan
  applying those gates to each row that reaches them before it applies the
  totals to any later row;
- `cache-unverified`: its child failed or timed out, read a record that is not
  an ignored one or an ignored record whose path, its trailing `/`
  disregarded, begins with `/` or holds an empty, `.` or `..` component, or
  read no ignored record, or a filesystem call of its walk failed or timed
  out, an open that the walk's no-follow rule refused at plan time included;
- `cache-unwritable`: every ignored path being a listed cache within the
  per-worktree caps, a directory that its cache stage would change failed the
  access check;
- `cache-unsupported-platform`, as "Cache disposal never follows a symlink or
  leaves its worktree" states.

A cache cap reached, or an access check failed, SHALL NOT make the plan
incomplete, and a row left with `cache-unwritable` SHALL NOT be selected and
SHALL NOT stop the run. A candidate whose enumeration leaves it at the
`ignored-local-files` rung, and one that passes the rung and that a gate after
`deferred-target-cap` then excludes, SHALL keep its place among the 16
enumerations. The
sample test keeps out of them a row whose samples show a blocking name, but not
a row whose samples all have cache names while it holds a blocking path beyond
its 8 samples, a path with a cache name that is blocking by its type, its
contents or its device, more recorded cache objects or bytes than a
per-worktree cap allows, an enumeration that fails, or a cache directory that
the running user cannot change; nor does any test keep out a row that a gate
after `deferred-target-cap` excludes, since those gates are checked only for
rows that pass every gate before it. A candidate SHALL count as held for a
persistent reason when any one of these holds:

- it is left at the rung and its enumeration finished with `blocking` above 0;
- it is left at the rung with `reason` `cache-cap` from a per-worktree cap,
  which leaves its counts null, and not from the invocation's totals, which
  leave them established, nor from the 16-enumeration cap, which leaves only
  candidates past the 16th;
- it is left at the rung with `reason` `cache-unverified`;
- it is left at the rung with `reason` `cache-unwritable`;
- it passes the rung and a gate after `deferred-target-cap` excludes it.

The test SHALL read these reasons and never `blocking` alone, which is null for
`cache-cap` and `cache-unverified` and 0 for `cache-unwritable`. When each of
the first 16 candidates in canonical order is held for a persistent reason, no
later candidate is enumerated, and a re-run enumerates the same 16 first. When
that holds and, besides those 16, at least one later candidate is left with
`cache-cap` by the 16-enumeration cap, the human report SHALL then, and only
then, say why the rows left with `cache-cap` will not drain (the stall line),
naming from those 16 rows' reasons how many hold ignored files that are not
caches, how many exceed a per-worktree cache cap, how many could not be
enumerated, how many hold a cache directory that the running user cannot
change, and how many a gate after `deferred-target-cap` excludes, by those
gates' reasons, each with its next step, and SHALL never tell the person to
remove by hand a worktree whose state was not established. When that holds but
no later candidate is so left, as when there are exactly 16 candidates, each
row's own reason and next step SHALL print as usual, and no stall line SHALL
print. When any of the first 16 is not held for a persistent reason, a later
run SHALL take the candidates that the 16-enumeration cap left as the
candidates ahead of them are removed or cease to be candidates, since a
candidate that its enumeration leaves at the `ignored-local-files` rung keeps
its place among the 16 enumerations though a gate before `deferred-target-cap`
excludes it. A later run SHALL take the candidates that the invocation's totals
left as the candidates ahead of them are removed, cease to be candidates or
cease to count toward those totals. A later run SHALL take the rows that
`deferred-target-cap` left as the rows ahead of them are removed or excluded by
a gate before the cap. Each holds unless the rows that `deferred-target-cap`
defers will not drain, as "Clean bounds its Git work and reports omitted work"
states, whose human report then says so. A deadline that passes
during an enumeration SHALL make the plan incomplete with `deadline-exceeded`,
as it does during any probe. A row whose enumeration finished with no cap
reached SHALL have its ignored records counted as `disposable`, those that are
listed caches, and `blocking`, the rest, and SHALL have `reason` null, except
that such a row with `blocking` 0 of which a directory failed the access check
SHALL have `cache-unwritable`; a row with `reason` null and `blocking` 0 SHALL
pass the `ignored-local-files` rung. A row left at the rung with
`not-candidate`, `cache-cap`, `cache-unverified` or
`cache-unsupported-platform` SHALL have `disposable`, `blocking`, `entries`,
`bytes`, `paths`, `directories` and `blocking_samples` null, except a row left
only by the invocation's totals, whose enumeration finished and which keeps
them, and a row that only the sample test keeps from being a candidate, whose
`blocking_samples` SHALL hold the samples that test rejects; a row left with
`cache-unwritable` SHALL keep them, its enumeration having finished.

A row whose `cache_disposal.reason` is `not-candidate` and whose samples pass
the sample test SHALL carry `candidate_block`: the class the ladder gives it
with the `ignored-local-files` rung skipped, when that class is not
`merged-removable`, or else the first gate before `deferred-target-cap` that it
fails, so that its value is one of the existing class names or gate reasons.
Every other row, and every row of a plan of `--action push` or `--action
delete-branch`, SHALL carry `candidate_block` null. Computing it SHALL spawn no
Git child.

`cache_disposal` SHALL be present on a worktree row exactly when its
`ignored_files` is above 0, and on a `selected` entry exactly when the plan
lists at least one cache for it; it SHALL be absent otherwise, never null. It
SHALL be an object of:

- `disposable` and `blocking`: integers, or null, never 0, when not
  established;
- `reason`: null or one of the codes above;
- `candidate_block`: null, or the class or gate reason above;
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

The listed cache paths and planned cache directories that `plan_digest` covers,
as "Clean previews and applies a batch of eligible worktree removals in one
repository" states, SHALL be a selected target's `paths` as `[path, kind]`
pairs and its `directories` as `[path, dev, ino]` triples.
`operations.estimated` SHALL count each selected target's cache entries besides
its removal.

For a selected target whose `cache_disposal.paths` is not empty, the removal
sequence SHALL run its cache stage after the target's revalidation passes and
before its removal child is spawned, under the same deadline. The stage SHALL
start only while more than the 5 s removal floor of the work deadline remains
and no signal has been received; otherwise the target and every later one SHALL
be `not-attempted` with `deadline-exceeded`, or with `interrupted`, and nothing
SHALL be deleted. The same two checks SHALL run again immediately before the
stage hands its first removal to its worker, after the whole-list preflight and
once the first listed cache's chain is reopened, with the same outcome, which
the removal floor or the deadline stopping a read of that preflight has too, a
signal received before any outcome of that preflight is classified taking
precedence over each, as "Cache disposal never follows a symlink or leaves its
worktree" states; a
signal recorded after that check SHALL be handled as one received during the
removals. That hand-off SHALL be the stage's first removal for every rule of
this requirement and of "Cache disposal never follows a symlink or leaves its
worktree". Each of its filesystem calls SHALL run on a daemon thread; each read
SHALL get `min(5 s, work remaining less the removal floor)`, and each unlink and
directory removal SHALL be handed over and waited for as "Clean bounds its Git
work and reports omitted work" states. It SHALL dispose of exactly the target's
listed caches, as "Cache disposal never follows a symlink or leaves its
worktree" states. Once it has handed over its first removal it SHALL run to its
end, a signal received meanwhile being only recorded, and the removal child
SHALL then be spawned, or not, by the sequence's own checks. A stage that
removes every listed cache SHALL let the sequence go on to the spawn, and a
target whose removal child those checks then do not spawn, because a signal had
been received or less than the removal floor remained, SHALL be `not-attempted`
with `interrupted` or `deadline-exceeded` and SHALL carry its reconciliation. A
stage that ends `refused` or `partial` SHALL refuse the target with
`state-changed`, as "Cleanup revalidates destructive actions" states: no
removal child is spawned, the target carries its reconciliation, no later
target is attempted, and the exit status is the first matching row of the table
that "Clean records a reconcilable result for every removal target" defines, 2
unless a signal, the deadline or the removal ceiling decides it. When the
removal floor ends a stage after its first removal, or the removal ceiling ends
the wait for one of its removals, every later target SHALL be `not-attempted`
with `deadline-exceeded`, and the exit status SHALL be 1 unless a signal
decides it.

An apply-result target SHALL carry `cache_disposal` exactly when its plan
listed at least one cache for it, and SHALL carry no such key otherwise, never
null. It SHALL be `{stage, reason, paths, entries, entries_removed}`: `stage`
and `reason` SHALL be `disposed` with null, `refused` with `cache-changed`,
`partial` with `cache-partial`, or `not-attempted` with `target-stopped` when
the target's revalidation refused it,
or the run stopped, was interrupted or reached the deadline, before its stage
started or before the hand-off of its first removal; `paths` SHALL list each
listed cache as `{path, path_valid_utf8, kind, removed}`, `removed` being true
when the stage removed it or its rescan found it absent, false when it remains,
and null when that is not established or when a removal of it is still
outstanding, whatever its rescan finds; `entries` SHALL be the planned count and
`entries_removed` the number of removals that returned having removed their
entry. `operations.performed` SHALL count each such removal once, and a removal
still outstanding SHALL count in neither.

The human preview SHALL list under each selected target with listed caches the
number of its cache paths, entries and bytes and its first cache path. An
`ignored-local-files` exclusion SHALL add its `disposable` and `blocking`
counts, each printed `unknown` with the reason when null, its first blocking
path when established, its `candidate_block` with that class's or gate's next
step when it has one, and, for `cache-unwritable`, the next step to fix the
ownership or mode of the first directory, by raw path bytes, that the row's
access check found the running user cannot change, named by its path relative
to the worktree, `.` for the worktree itself, or, on a read-only filesystem, to
remount it writable, and re-run. The confirmation question SHALL
stay as "Clean previews and applies a batch of eligible worktree removals in
one repository" states it. A successful apply SHALL add one line naming how
many cache paths were disposed of in how many worktrees. A run that stops at a
target whose cache stage ended `refused` or `partial` SHALL print, before its
stop block, one line naming that target and saying that nothing was deleted,
only when no entry was removed and no removal is outstanding and, for a stage
that ended before its first removal, no signal had been received by then, or
else how many of its cache paths were removed, which remain and which a removal
still outstanding may still remove, naming the work deadline as the cause, and
not a change of state, when the deadline ended the stage, with the command that
shows a fresh plan for the rest. A run that stops after a target's cache stage
ended `disposed`, before its removal child was spawned or at that target when
its removal then ended `failed`, SHALL print
`Cache disposal at PATH: removed N cache paths; the worktree was not removed.`
before its stop block, and one that stops at such a target that ended
`unknown` SHALL print there `Cache disposal at PATH: removed N cache paths;
the worktree's removal is not proven.`, so that the person reads how many
cache paths were deleted before the stop block names the target's reason and
the next step. A run that stops at a target whose cache stage the
removal floor or the work deadline stopped in a read before its first removal,
no signal having been received by then, SHALL print
`Cache disposal at PATH not attempted (deadline-exceeded); nothing was deleted.`
before its stop block, naming the deadline and not a change of state. The
residual-window line SHALL be the one that "Cleanup states a narrow guarantee
and its residual window" states.

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
  5, the exit status is 0, and the human result adds `Caches disposed: 2 paths
  in 1 worktree.`
- **AND** on a copy, `--apply --action remove --worktree` naming it with `--yes`
  does the same, where before this change it refused with `target-excluded`,
  reason `ignored-local-files`
- **AND** on a copy whose branch's upstream remote-tracking ref was deleted, the
  branch still merged, the row is still a candidate and `merged-removable`, its
  caches are disposed of, and the worktree is removed, its branch kept
- **AND** on a copy where a test hook locks the worktree after its cache stage
  and before its removal child is spawned, Git refuses the removal with exit
  status 128, the target is `failed` with `git-refused`, its four cache
  entries are gone and its worktree remains, the exit status is 128, and
  before the stop block the human result reads `Cache disposal at PATH:
  removed 2 cache paths; the worktree was not removed.`

#### Scenario: Caches beside a blocking ignored file

- **WHEN** the same worktree also holds the ignored file `local.env`, which its
  combined status probe samples
- **THEN** it is classified `ignored-local-files`, it fails the sample test and
  no cache enumeration runs in it, its `cache_disposal` has `reason:
  "not-candidate"`, `disposable` and `blocking` null and `blocking_samples`
  naming `local.env`, the preview shows both counts as `unknown` and
  `local.env` as the first blocking path, and nothing is deleted
- **AND** `--apply --action remove --worktree` naming it refuses with
  `target-excluded`, reason `ignored-local-files`, and exit 2, and every cache
  and `local.env` survive
- **AND** when it holds, instead of `local.env`, eight ignored loose files
  `a0.pyc` to `a7.pyc`, which fill its 8 samples, and an ignored `zz.env`,
  which Git prints after them, it is a candidate and is enumerated, and its
  `cache_disposal` has `reason: null`, `disposable: 10`, `blocking: 1` and
  `blocking_samples` naming `zz.env`

#### Scenario: Unknown counts are null, never zero

- **WHEN** one linked worktree holds ignored caches and its branch, pushed and
  level with its upstream, is not merged, a second, merged one holds no ignored
  file, and a third's status probe fails
- **THEN** the first has `cache_disposal.reason: "not-candidate"` with
  `disposable`, `blocking`, `entries`, `bytes`, `paths`, `directories` and
  `blocking_samples` null, and the human report prints its counts as `unknown`
- **AND** neither the second, whose `ignored_files` is 0, nor the third, whose
  `ignored_files` is null, carries a `cache_disposal` key
- **AND** the first's `cache_disposal.candidate_block` is `pushed-unmerged`,
  and its preview line names that class and its next step, not the advice to
  delete ignored files; a detached worktree holding only caches names
  `detached`

#### Scenario: Cache caps

- **WHEN** one candidate holds 513 ignored loose `.pyc` files under an ignore
  rule `*.pyc`, and another holds caches whose regular files total more than
  256 MiB
- **THEN** both are `ignored-local-files` with `cache_disposal.reason:
  "cache-cap"`, the first's enumeration child having stopped at its 513th
  record, nothing is deleted, the plan is complete, and apply is allowed, with
  `disposable` and `blocking` null
- **AND** when a candidate's only ignored file is one loose `.pyc` 600
  directories below the worktree root, it stays `ignored-local-files` with
  `cache-cap`, since the directories above that file count toward its 512
  recorded cache objects, its counts are null, and nothing is deleted
- **AND** when a candidate's only ignored path is one `__pycache__` directory
  holding 100,000 entries, under the ignore rule `__pycache__/`, which Git
  prints as one record, a test hook counting the entries taken from that
  directory's enumeration sees at most 513 taken, the row stays
  `ignored-local-files` with `cache-cap`, its counts are null, and nothing is
  deleted
- **AND** when seventeen candidates each hold one small cache directory, the
  first sixteen in canonical order are enumerated and selected, the seventeenth
  stays `ignored-local-files` with `cache-cap`, `--all-safe --apply --yes`
  removes sixteen, and a second run removes the seventeenth
- **AND** when nine candidates each hold caches of 500 entries, the first eight
  are selected and the ninth stays `ignored-local-files` with `cache-cap`, its
  entries not counted toward the 4,096, its `disposable` and `entries` are
  established and `blocking` is 0, and no stall line is printed, since it drains
- **AND** when five candidates each hold caches whose regular files total
  250 MiB, the first four are selected and the fifth stays
  `ignored-local-files` with `cache-cap`, its bytes not counted toward the
  1 GiB
- **AND** when sixteen candidates each hold, beside a cache directory, eight
  ignored loose `.pyc` files that fill their samples and an ignored `zz.env`
  beyond them, and a seventeenth, later in canonical order, holds only caches,
  every run enumerates the sixteen, each stays `ignored-local-files` with
  `blocking: 1`, the seventeenth stays `ignored-local-files` with `cache-cap`,
  and the human report's line says that the 16 ahead of it hold ignored files
  that are not caches, with that next step
- **AND** when the sixteen instead each hold one `__pycache__` directory of 600
  entries, each stays `ignored-local-files` with `cache-cap`, and the line
  names the per-worktree cache cap with its next step, to delete their caches
  and re-run
- **AND** when the sixteen instead are held with no `blocking` above 0, five
  because a fake `git` makes their cache enumeration child exit 128, five
  because their `__pycache__` directory is mode 0555 and the run is not root's,
  and six because their `__pycache__` directory holds 600 entries, they stay
  `ignored-local-files` with `cache-unverified`, `cache-unwritable` and
  `cache-cap`, the seventeenth stays `ignored-local-files` with `cache-cap`,
  and the line is printed, naming the six that exceed a per-worktree cache cap,
  the five that could not be enumerated and the five that this user cannot
  change, each with its next step, and no count of rows holding ignored files
  that are not caches
- **AND** when the sixteen instead each hold only caches and an initialized
  submodule, or an entry flagged assume-unchanged, each is enumerated, passes
  the `ignored-local-files` rung and is excluded as `contains-submodule` or
  `hidden-local-state`, its caches untouched, the seventeenth stays
  `ignored-local-files` with `cache-cap` on every run, and the line names the
  sixteen as excluded after the target cap by those reasons, with their next
  step
- **AND** when eight candidates each hold caches of 500 entries and an
  initialized submodule, ahead of a ninth holding caches of 500 entries, the
  eight are excluded as `contains-submodule`, their entries are not counted
  toward the 4,096, and the ninth is selected, its caches disposed of and its
  worktree removed
- **AND** when there is no seventeenth candidate, so that exactly sixteen
  candidates exist and each is held for a persistent reason as in any of the
  cases above, no stall line is printed, and each row's preview line gives its
  own reason and next step
- **AND** when the sixteen instead hold `local.env` among their samples, none
  of them is enumerated, and the seventeenth is enumerated and selected

#### Scenario: The cache enumeration runs under the pins

- **WHEN** the user's configuration sets `status.showUntrackedFiles=no`,
  `core.untrackedCache=true` and `status.showStash=true`, and `--all-safe`
  previews a repository that holds one stash and one cache-only candidate
  under a counting `git` wrapper on PATH
- **THEN** the wrapper records one `status --porcelain=v2 -z
  --untracked-files=normal --ignored=matching` child naming that worktree as its
  directory and carrying `-c core.untrackedCache=false -c
  core.fsmonitor=false -c core.trustctime=true -c core.checkStat=default`,
  `-c status.showStash=false` and the seven protocol pins, the enumeration
  succeeds, its output holding no `# stash` header, and
  `probes.performed` counts that child
- **AND** `--all-safe --apply --yes` then revalidates the candidate with the
  same child and pins, which prints exactly the planned records, disposes of
  its caches and removes it, its branch kept, and the exit status is 0
- **AND** no such child runs for a row that is not a candidate, nor for
  `--apply --action push`

#### Scenario: A failed cache enumeration preserves the row, not the plan

- **WHEN** a merged, clean, published worktree holds only caches and a second
  plain merged worktree is eligible, and a fake `git` makes the first
  worktree's cache enumeration child exit 128, or print an untracked record
  before its ignored ones
- **THEN** the first is `ignored-local-files` with `cache_disposal.reason:
  "cache-unverified"` and null counts, not `inspection-error`, the plan is
  complete, `--all-safe --apply --yes` removes only the second, the first's
  caches are untouched, and the exit status is 0
- **AND** the same holds when the child prints no ignored record, or, a fake
  `git` printing it, an ignored record whose path begins `../`, for which the
  walk opens nothing, or when a test hook makes a filesystem call of the walk
  fail or outlive its budget, or makes a directory's no-follow open fail as
  for a symbolic link
- **AND** when the work deadline passes while that cache enumeration child
  runs, the plan is incomplete with `deadline-exceeded`, the preview exits 1,
  and `--apply` refuses with exit 2 before any mutation

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
- **AND** when more than the floor remains as the stage starts but no more than
  the floor remains at the check before the hand-off of its first removal,
  after its whole-list preflight, nothing is deleted, its `cache_disposal` is
  `not-attempted` with `target-stopped`, it and every later target are
  `not-attempted` with `deadline-exceeded` and `reconciliation: null`, and the
  exit status is 1
- **AND** when more than the floor remains as the stage starts and a test hook
  holds a read of its whole-list preflight until the budget that the deadline
  sets, `work remaining less the removal floor` being under 5 s, is spent, or
  until no more than the floor remains for the next read to start, the listed
  caches being unchanged, nothing is deleted, its `cache_disposal` is
  `not-attempted` with `target-stopped`, it and every later target are
  `not-attempted` with `deadline-exceeded` and `reconciliation: null`, the exit
  status is 1, and before the stop block the human result reads `Cache disposal
  at PATH not attempted (deadline-exceeded); nothing was deleted.`, never
  `cache-changed`; where the hook instead holds the read past its 5 s per-call
  budget with at least 10 s of work remaining, or the preflight finds a changed
  entry, the stage ends `refused` with `cache-changed`, nothing deleted, the
  target is `refused` with `state-changed`, and the exit status is 2

#### Scenario: The removal floor reached during a cache stage

- **WHEN** a selected target lists two caches, a later target is selected, and
  a test hook delays the stage after the first cache's removal and before it
  hands over the second cache's first removal, until no more than the 5 s
  removal floor of the work deadline remains
- **THEN** the stage ends `partial` with `cache-partial`, the first cache stays
  removed and the second remains, its rescan establishing `removed: false`
  within the reconciliation reserve, the target is `refused` with
  `state-changed` and carries its reconciliation, no removal child is spawned,
  the later target is `not-attempted` with `deadline-exceeded`, and the exit
  status is 1
- **AND** before the stop block the human result says that the work deadline
  ended the stage after removing 1 of 2 cache paths, names the one that
  remains and gives the command for a fresh plan, and does not say that the
  worktree's state changed

#### Scenario: A signal during a cache stage

- **WHEN** SIGINT arrives after a cache stage has handed over its first removal
- **THEN** the stage removes the rest of its listed caches and records
  `disposed`, no removal child is spawned for that target, the target and every
  later one are `not-attempted` with `interrupted`, the target carrying its
  reconciliation and every later one `reconciliation: null`, and the exit
  status is 130
- **AND** before the stop block the human result says that the target's caches
  were removed and its worktree was not
- **AND** SIGINT before that check, the one immediately before the hand-off of
  the stage's first removal, during its whole-list preflight and while the
  first listed cache's chain is reopened included, leaves every cache in place,
  and the target is `not-attempted` with `interrupted` and its
  `cache_disposal` `not-attempted` with `target-stopped`
- **AND** where SIGINT arrives while a test hook holds a read of that
  whole-list preflight, and the read then outlives its 5 s per-call budget, or
  the shorter budget that the deadline sets, or is held until no more than the
  removal floor remains for the next read to start, or the preflight then finds
  a changed entry, before that check is reached, the signal is checked before
  that outcome is classified: nothing is deleted, the stage is `not-attempted`
  with `target-stopped`, the target and every later one are `not-attempted`
  with `interrupted`, never `refused` with `cache-changed` and never
  `deadline-exceeded`, and the exit status is 130

#### Scenario: An unwritable cache directory is kept, not a stop

- **WHEN** a merged, clean, published linked worktree's only ignored files are
  caches and its `__pycache__` directory is mode 0555, beside a later plain
  eligible worktree, and `--all-safe --apply --yes` runs as a user other than
  root
- **THEN** the first is `ignored-local-files` with `cache_disposal.reason:
  "cache-unwritable"`, its `disposable` and `entries` established and
  `blocking` 0, it is not selected, nothing in it is deleted, the second is
  removed, and the exit status is 0
- **AND** its preview line names `cache-unwritable` with the next step to fix
  the ownership or mode of that `__pycache__` directory, named by its path
  relative to the worktree, or, on a read-only filesystem, to remount it
  writable, and re-run, and a re-run plans the same, also after a mode change
  of the worktree itself
- **AND** when the access check passes but a test hook makes the stage's first
  unlink fail with `EACCES` or `EROFS`, the stage ends `refused` with
  `cache-changed` and nothing deleted, the target is `refused` with
  `state-changed`, and the exit status is 2
