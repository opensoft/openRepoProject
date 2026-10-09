## MODIFIED Requirements

### Requirement: Clean reports local worktree state

`project clean` SHALL inspect the target repository and every linked worktree
using local Git state only. It SHALL report each worktree's path, branch or
detached state, cleanliness, upstream, ahead/behind counts as of the last
fetch, and whether its commits are merged into the target's tracking branch.
Human and JSON reports SHALL describe that remote information may be stale.

The report SHALL be built from the evidence that "Repository inspection requires
Git 2.36 and shares one evidence model" defines, within the bounds that "Clean
bounds its Git work and reports omitted work" sets. `project clean` SHALL run
its Git version check before any other Git child, and SHALL refuse a Git older
than 2.36 with `git-too-old`, and a `git` that is missing or unusable with
`git-unavailable`, with exit status 2, before any repository is probed; under
`--json` it SHALL print the extended error object that "Clean plans and refusals
are versioned JSON" defines, carrying that code.

The plain report (neither `--all-safe` nor `--apply`) SHALL be the plan that a
batch preview builds, in `mode: "report"`, under a cap of 256 worktree rows. It
SHALL carry every plan field: `selected` SHALL be what `--all-safe` would
select, the per-run deferral applied, for a repository of at most 128 worktree
rows. Above 128, `selected` SHALL be null and the plan's `notes` SHALL carry an
`inspect-cap` entry with `rows`, the count of registered worktree rows, beside
the human line saying that `--all-safe` itself would be incomplete with
`inspect-cap`; that note alone SHALL NOT make the report incomplete. Above 128
the gates SHALL still run for every inspected row, so `excluded` SHALL list
every inspected row that a gate excludes with its `reason`, as in any report,
and only the selection step is withheld. Above 128 the `plan_digest` SHALL be
computed over the same canonical text as any plan, which covers only the
repository's identity fields, the merge target and `selected`, with `selected`
null, and `--expect-plan` SHALL never consume it, because an apply there is an
incomplete plan and is refused before the digest is compared. At most 128 rows,
a report's `plan_digest` SHALL equal the `--all-safe` preview's for the same
selection, since the mode is not in the digest, and an `--expect-plan` carrying
it SHALL match, which is intended. `apply_allowed` SHALL be false. It SHALL
exit 0 when the report is complete, 1 when it is incomplete (`inspect-cap`,
`inspection-incomplete` or `deadline-exceeded`), and 2 when no report can be
built, and its human output SHALL say when and why it is incomplete.

A worktree whose registered path cannot be read, for any reason other than its
absence, SHALL be one row with `present: null`, an `os-error` in its `errors`
and classification `inspection-error`, and SHALL NOT refuse the repository. A
status probe that fails or times out in any row, the main worktree's and the
merge-target checkout's included, SHALL leave that row's `dirty` null and
classify the row `inspection-error`. A row's `ignored_files` SHALL count the
ignored entries observed, a lower bound when `ignored_files_truncated` is true.
The report's `root` SHALL name the command directory, the main worktree of the
resolved repository.

#### Scenario: Audit a repository with a feature worktree

- **WHEN** `project clean` is run without an apply action
- **THEN** it prints a cleanup plan for the main checkout and each linked
  worktree without fetching, committing, pushing, resetting, stashing, or
  removing anything

#### Scenario: The plain report exits by completeness

- **WHEN** plain `project clean` runs on a repository with more than 256
  registered worktree rows
- **THEN** it prints an incomplete report carrying `inspect-cap` and `omitted`,
  and exits 1, where before this change it exited 0 whenever it printed
- **AND** on a repository with 200 rows the plain report is complete, says that
  `--all-safe` itself would be incomplete with `inspect-cap`, and exits 0, its
  JSON carrying `selected: null` and a `notes` entry `inspect-cap` with
  `rows: 200`, while `project clean <root> --all-safe` on the same repository
  is incomplete with `inspect-cap` and exits 1

#### Scenario: An unreadable worktree is one row

- **WHEN** a linked worktree's path cannot be read because its parent directory
  denies search permission, and plain `project clean` runs
- **THEN** that row has `present: null`, an `os-error` and classification
  `inspection-error`, every other row is reported, and the report is incomplete
  and exits 1, where before this change the whole command refused with exit 2

#### Scenario: A failed status probe on the merge-target checkout

- **WHEN** the status probe of the worktree checked out on the merge-target
  branch fails or times out
- **THEN** that row is classified `inspection-error`, never `protected-default`,
  its `dirty` is null, and the report is incomplete with `inspection-incomplete`
  and exits 1

#### Scenario: A failed status in the repository root

- **WHEN** the main worktree's status probe fails
- **THEN** plain `project clean` reports the main worktree's row as
  `inspection-error` and exits 1 with an incomplete report, where before this
  change it refused the repository with exit 2

#### Scenario: Git older than 2.36

- **WHEN** `project clean` runs in any mode with Git 2.35 first on PATH
- **THEN** it refuses with `git-too-old` and exit 2 before any repository probe,
  and under `--json` it prints the extended error object with `code:
  "git-too-old"`
- **AND** with no `git` on PATH it refuses with `git-unavailable` and exit 2

### Requirement: Clean classifies preservation and cleanup actions

The command SHALL classify each worktree row with exactly one of fifteen
classes, by a ladder tested in this order: `stale-worktree`,
`protected-default`, `inspection-error`, `dirty`, `ignored-local-files`,
`detached`, `unpublished`, `remote-gone`, `review-required`, `diverged`,
`remote-ahead`, `unpushed`, `merged-removable`, `merged-current` and
`pushed-unmerged`. The ladder SHALL be a function of the row's evidence alone,
and its names and order SHALL NOT change. A row whose evidence could not be
established (a path that cannot be read, a registration that disagrees, or a
status probe that failed or timed out) SHALL be classified `inspection-error`
directly, whatever its branch. A branch with no configured upstream SHALL be
`unpublished`, and a branch whose configured upstream's remote-tracking ref no
longer exists SHALL be `remote-gone`. `review-required` SHALL remain a defensive
rung that no value of the evidence model reaches.

Every class other than `merged-removable` SHALL be preserved. Dirty, detached,
unpublished, remote-gone, and unmerged work SHALL be preserved and SHALL include
an actionable human handoff rather than being treated as removable. A
`remote-gone` row whose `merged_into_target` is true SHALL carry the
recommendation "Merged locally, upstream deleted: not removable by `project`
until the open question is ruled; review, then `git worktree remove` yourself".

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

- **WHEN** one linked worktree's branch has a configured upstream whose
  remote-tracking ref was deleted, and another's branch has no upstream
  configured
- **THEN** the first is classified `remote-gone` and the second `unpublished`,
  and both are preserved, where before this change both read `unpublished`

#### Scenario: A merged worktree whose upstream was deleted

- **WHEN** a clean linked worktree's branch is merged into the merge target and
  its upstream's remote-tracking ref was deleted
- **THEN** it is classified `remote-gone`, no `project` command removes it, and
  its recommendation reads "Merged locally, upstream deleted: not removable by
  `project` until the open question is ruled; review, then `git worktree remove`
  yourself"

#### Scenario: Only tracked-file deletions

- **WHEN** a registered linked worktree whose `.git` file is intact has only
  deleted tracked files as its working changes
- **THEN** it is classified `dirty` with the dirty advice, the human report
  shows the probable partial-removal note and the recovery text beside that
  advice, and the JSON row carries `notes: ["partially-removed"]`
- **AND** a worktree with one deleted tracked file and one untracked file
  carries no such note

### Requirement: Clean can explicitly push safe feature branches

An apply operation SHALL be able to push a named non-default branch to its
configured upstream, or establish its explicitly named upstream when none
exists. It MUST use a normal non-force push, require confirmation unless
explicit confirmation was supplied, and preserve the delegated exit status and
output. It SHALL refuse to push a default branch or a branch with unresolved
local work.

It SHALL refuse, with exit status 2 and no push, a branch classified
`remote-gone`, naming the reason `remote-gone`: its configured upstream was
deleted, so it must be reviewed before it is republished. It SHALL refuse with
`inspection-incomplete`, `inspect-cap` or `deadline-exceeded`, exit status 2 and
no push, when the full inspection it acts on, before or after confirmation, is
incomplete. Its argument SHALL be resolved as "Clean resolves its target
Git-first" states, and `--apply --json` SHALL stay refused with
`invalid-arguments` and exit status 2.

#### Scenario: Push an unpushed feature branch

- **WHEN** the user requests an apply push for a clean feature branch with
  commits not present on its remote branch
- **THEN** the command shows the exact push plan, confirms it, and pushes
  without force; a failed push leaves the repository unchanged by the command

#### Scenario: Push refuses a branch whose upstream was deleted

- **WHEN** push is requested for a clean feature branch whose configured
  upstream's remote-tracking ref was deleted
- **THEN** the command refuses with the reason `remote-gone` and exit 2, and
  runs no push

#### Scenario: Push refuses an incomplete inspection

- **WHEN** push is requested while another worktree row of the repository is
  `inspection-error`, or the deadline passes during its re-inspection after
  confirmation
- **THEN** the command refuses with `inspection-incomplete` or
  `deadline-exceeded` and exit 2, and runs no push

#### Scenario: Push and branch deletion stay human-only

- **WHEN** `--apply --action push` or `--apply --action delete-branch` is given
  with `--json`
- **THEN** the command refuses with `invalid-arguments` and exit 2, and runs
  nothing

### Requirement: Clean can explicitly retire verified worktrees

An apply operation SHALL be able to remove one named linked worktree, or the set
that a fresh `--all-safe` plan selects, only when each is clean, not the current
worktree, and its branch is verified as merged into the target branch, and only
when each passes every gate that "Clean previews and applies a batch of eligible
worktree removals in one repository" lists, `unstarted-branch` included. Every
removal, single or batch, SHALL follow one sequence: revalidate the target as
"Cleanup revalidates destructive actions" states; spawn, only while at least the
5 s removal floor of the work deadline remains, the non-force command `git -c
status.showUntrackedFiles=normal -c core.untrackedCache=false -c
core.fsmonitor=false -C <command directory> worktree remove <path>` in its own
process group; wait for it; and reconcile by rescan as "Clean records a
reconcilable result for every removal target" states. Removal SHALL stop after
the first target whose result is not a plain `removed`, with no continuation,
rollback or automatic retry.

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

### Requirement: Clean hands off work requiring review

For a clean branch that is pushed but not merged, the command SHALL report that
the branch must go through the repository's normal pull-request or merge
process. It SHALL not create, approve, merge, close, or delete a pull request
implicitly. Noninteractive execution SHALL refuse apply actions unless the
user supplied explicit confirmation and action targets.

`--all-safe` SHALL count as an explicit action target: the set that the fresh
plan of that same invocation selects. `--yes` SHALL count as explicit
confirmation of that fresh plan. `--apply` on a standard input that is not a
terminal and without `--yes` SHALL refuse with `confirmation-required` and exit
status 2 before any mutation.

#### Scenario: Pushed feature branch has an open review path

- **WHEN** a clean feature branch has an upstream branch but is not merged
- **THEN** the report says to continue through the normal pull-request or
  merge process and leaves the worktree and branch intact

#### Scenario: A noninteractive batch needs --yes

- **WHEN** `project clean <root> --all-safe --apply` runs with a standard input
  that is not a terminal and without `--yes`
- **THEN** it refuses with `confirmation-required` and exit 2, and nothing is
  removed
- **AND** with `--yes` the selection of that invocation's fresh plan is applied
  without a question

## ADDED Requirements

### Requirement: Clean resolves its target Git-first

Every `project clean` mode (the plain report, `--json`, `--all-safe`, and
`--apply --action push|remove|delete-branch`) SHALL resolve its argument to
exactly one repository, ending in the identity probe that "Repository inspection
requires Git 2.36 and shares one evidence model" defines:

- an absolute path SHALL be exactly a main worktree root: its realpath SHALL
  equal the toplevel Git reports there, and that toplevel SHALL be the
  repository's main worktree; a subdirectory, a linked worktree, a bare
  repository or a path outside any repository SHALL be refused with
  `target-not-repository-root`;
- a relative path, or no argument, SHALL be made absolute against the working
  directory and SHALL resolve to the repository Git finds there, with `root` set
  to its main worktree, and SHALL be refused with `target-not-repository-root`
  where Git finds no worktree there;
- a bare name (one path component) SHALL keep the existing project-name lookup,
  its one Git child counted and bounded, refusing with `ambiguous-name` or
  `repository-not-found`, and the directory the lookup returns SHALL then be
  resolved as a worktree toplevel.

The existing manifest-ancestor and family-holder redirections SHALL NOT be
applied to a path argument. The command directory SHALL be the main worktree,
every repository-wide Git child after resolution and every removal SHALL run
there, and the manifest SHALL be read there.

A repository without a main worktree (a bare repository) SHALL be refused in
every mode with `target-not-repository-root`, including from a relative path, no
argument or a bare name inside one of its linked worktrees. A submodule checkout
SHALL be tested first: where Git reports a superproject working tree for the
resolved directory, the command SHALL refuse with `target-not-repository-root`.
Otherwise, where the first registry record is the common directory itself (a
main checkout whose `.git` is a file), the main worktree SHALL be the realpath
of `core.worktree` or, where that is unset, the candidate toplevel whose `.git`
file names the common directory; a root equal to it SHALL resolve, the common
directory SHALL never be probed as a worktree row, and a linked worktree whose
main checkout cannot be named SHALL be refused with
`target-not-repository-root`.

The merge target SHALL be the first of these candidates that exists as a local
branch: the manifest's `tracking_branch` with any leading `origin/` removed; the
branch that the symref of `refs/remotes/origin/HEAD` names, with its
`refs/remotes/origin/` prefix removed; `main`; `master`. It SHALL be recorded as
`merge_target: {name, source, sha}`, `source` being `manifest`, `origin-head`,
`main` or `master` and `sha` its tip when the plan is built. When the manifest
and `origin/HEAD` name different existing branches, the manifest SHALL win and
the plan SHALL carry an informational `merge-target-conflict` note. When no
candidate exists the command SHALL refuse with `no-merge-target`, keeping its
existing message, and a manifest that cannot be read, has the wrong kind or is
larger than 1 MiB SHALL refuse with `manifest-invalid`. Every refusal this
requirement names SHALL exit 2 before any mutation and, under `--json`, SHALL
print the extended error object.

#### Scenario: Absolute path that is not a repository root

- **WHEN** an absolute path to a subdirectory of a repository root, to one of
  its linked worktrees, to a directory outside any repository, or to a bare
  repository is passed to `project clean` in the read-only form, with
  `--all-safe --apply --yes`, and with `--apply --action remove`, `push` or
  `delete-branch`
- **THEN** each is refused with `target-not-repository-root` and exit 2 before
  any plan is built, no other directory is substituted, and nothing changes

#### Scenario: Overview handoff keeps identity

- **WHEN** the argument vector `["project", "clean", "<Atlas root>",
  "--all-safe"]` runs without a shell, an independent clone also named Atlas
  exists under a second configured projects directory, and in turn an ancestor
  of the Atlas root holds `project.yaml` or the root contains
  `Atlas/family.yaml`
- **THEN** the path resolves Git first, the plan's `repository` names the Atlas
  repository itself by its four identity fields, the read-only report's `root`
  is the Atlas root, and the other clone is never inspected
- **AND** without the family holder, `project clean Atlas --all-safe` keeps the
  existing name lookup and refuses with `ambiguous-name` and exit 2

#### Scenario: A bare repository reached from a linked worktree

- **WHEN** `project clean` runs with a relative path, or with no argument,
  inside a linked worktree of a bare repository
- **THEN** it refuses with `target-not-repository-root` and exit 2, where before
  this change it reported the repository and could remove its worktrees

#### Scenario: A separate git directory

- **WHEN** a repository made with `git init --separate-git-dir` is passed by the
  absolute path of its checkout
- **THEN** it resolves, `repository.root` is that checkout, and the git
  directory is not a worktree row

#### Scenario: A submodule checkout

- **WHEN** the argument is a submodule's checkout inside a superproject
- **THEN** the command refuses with `target-not-repository-root` and exit 2,
  where before this change it exited 0

#### Scenario: Merge target missing, invalid, or conflicting

- **WHEN** a repository has no manifest `tracking_branch`, no `origin/HEAD`, and
  neither `main` nor `master`
- **THEN** the command refuses with `no-merge-target` and exit 2 before any
  mutation, and `--json` prints the extended error object; a manifest of the
  wrong kind refuses with `manifest-invalid` the same way
- **AND** with a manifest naming `release` and `origin/HEAD` naming `main`, both
  existing, `merge_target` is `release` with `source: "manifest"`, the plan
  carries a `merge-target-conflict` note, and apply is allowed
- **AND** with no manifest candidate, local `trunk` and `main`, and
  `refs/remotes/origin/HEAD` pointing at `refs/remotes/origin/trunk`,
  `merge_target` is `trunk` with `source: "origin-head"`, not `main`

#### Scenario: A tracking branch spelled with its remote

- **WHEN** the manifest's `tracking_branch` is `origin/develop`, local `develop`
  and `main` exist, and `origin/HEAD` names `main`
- **THEN** `merge_target` is `develop`, read from `refs/heads/develop`, with
  `source: "manifest"`, never `main` by a silent fallback

#### Scenario: A manifest over 1 MiB

- **WHEN** the manifest at the repository root is larger than 1 MiB
- **THEN** `project clean` refuses with `manifest-invalid` and exit 2 before any
  worktree row is probed, where before this change it read the manifest

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
decide it; `deferred-target-cap`; `contains-submodule`; and
`hidden-local-state`. A head equal to the merge target's SHA SHALL NOT by itself
prove a branch unstarted, because a branch fast-forward merged into the target
sits at the target's tip, so the gate SHALL read the branch's reflog,
`logs/refs/heads/<branch>` in the common directory, for every row it checks,
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
probe does; and a read not finished within the filesystem budget SHALL leave
the row unprobed and the plan incomplete with `inspection-incomplete`, as for
every other filesystem read. A row SHALL be excluded as `contains-submodule`
when its index holds any gitlink or its worktree administrative directory holds
a `modules` entry, and as
`hidden-local-state` when its index flags any entry assume-unchanged or
skip-worktree, sparse checkouts included; the index SHALL be read inside the
row's own worktree, and both gates SHALL be checked only for rows that pass
every earlier gate.

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
an excluded row leaves it unchanged. `--expect-plan D` SHALL refuse with
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
worktree repair`, or removing the offending row by hand, as the cause fits.

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
  ignored files, unpublished, remote-gone, diverged, remote-ahead, unpushed,
  pushed-unmerged, merged but current, merged but locked, merged with a
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

### Requirement: Clean bounds its Git work and reports omitted work

Each `project clean` invocation SHALL set one monotonic deadline 60 s after it
starts and SHALL hold back a 10 s reconciliation reserve, so that work stops 50
s after start; time spent blocked at the confirmation question SHALL NOT count,
both deadlines moving later by the time spent waiting. Each Git child SHALL get
`min(5 s, work remaining)`, and each filesystem call (`lstat`, `realpath`, and
the reads of `.git`, `gitdir`, reflog and manifest files) SHALL be abandoned
after the same budget, recording `probe-timeout`, or `deadline-exceeded` where
the deadline was the limit, and leaving its values null. Probing SHALL be
serial. Reconciliation probes SHALL get `min(5 s, reserve remaining)`.

The deadline SHALL bound inspection and SHALL gate only the start of a removal:
a removal child SHALL be spawned only while at least the 5 s removal floor of
the work deadline remains, and otherwise that target and every later one SHALL
be `not-attempted` with `deadline-exceeded`. A removal child still running at
the deadline SHALL be waited for, up to its 300 s hard ceiling, and the
reconciliation reserve SHALL count from its exit. A run with no removal in
flight SHALL therefore end within 64 s of its start, not counting the time
blocked at the confirmation question (50 s of work, the 10 s reserve, and up to
4 s to stop and reap a probe child), and a removal in flight SHALL add at most
300 s, except while a filesystem call stuck in the kernel is outstanding. Push
and delete-branch children SHALL stay unbounded, as before this change.

The caps, provisional until measured, SHALL be: at most 128 worktree rows in
`mode: "all-safe"` and `mode: "single"`, and 256 in `mode: "report"`, every
registry entry counting, the main worktree and missing rows included; at most 16
targets per run; and the ignored-file bounds that "Repository inspection
requires Git 2.36 and shares one evidence model" sets. Push and delete-branch
SHALL run in `mode: "single"` for the row cap and these bounds. The registry
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
that an index gate then excludes SHALL keep their places among the 16. No plan
SHALL be refused for having more than 16 such rows. In a single-target removal
the limit SHALL count P alone, because `not-requested` precedes it.

Plans and apply results SHALL report `probes: {estimated, performed}` and
`operations: {estimated, performed}`, every Git child counted; `limits`
(`worktree_rows`, the row cap of the plan's mode, `targets`, `ignored_entries`,
`status_records` and `ignored_samples`); and `budget` (`probe_timeout_seconds`
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

- **WHEN** a merged, clean worktree holds 70 ignored files and the plan is built
- **THEN** the probe stops when the 65th ignored record arrives, the row has
  `ignored_files: 64`, `ignored_files_truncated: true` and 8 `ignored_samples`,
  and it is excluded as `ignored-local-files`
- **AND** with exactly 64 ignored files the row has `ignored_files: 64` and
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
  `probes.performed` equals the wrapper's count
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

### Requirement: Clean records a reconcilable result for every removal target

The apply phase SHALL begin when the question is answered `yes` or `--yes` is
accepted. Each selected target SHALL end in one stage with one reason:

- `removed`: the child exited 0, was killed at the hard ceiling, or ended with
  an exit that could not be observed, and the rescan shows its registry entry
  and its path both absent, with `reconciled` true; reason null,
  `branch-advanced-after-removal`, `branch-missing-after-removal` or
  `removal-ceiling`;
- `refused`: revalidation found a difference and nothing was spawned;
  `identity-changed`, `branch-changed`, `state-changed`, `contains-submodule` or
  `hidden-local-state`;
- `failed`: the child exited nonzero on its own, whether or not a signal reached
  `project`, or could not be spawned; `git-refused` for exit status 128,
  `git-failed` for any other status (128 plus the signal number when a signal
  that `project` did not send ended the child), or `spawn-error`;
- `unknown`: a child ran, or an exception interrupted the target, and removal is
  not proven; `unconfirmed-removal`, `reconciliation-incomplete`,
  `internal-error` or `removal-ceiling`;
- `not-attempted`: the run stopped before reaching the target, or before
  spawning its removal because less than the removal floor remained;
  `batch-stopped`, `interrupted` or `deadline-exceeded`.

A removal child that exits nonzero on its own SHALL be `failed` with Git's
status, `git-refused` for 128 and `git-failed` otherwise, whether or not a
signal reached `project`. Only for a child that `project` killed at the ceiling,
or whose exit could not be observed, SHALL the rescan decide between `removed`
and `unknown` with the note `partially-removed`; `removal-ceiling` SHALL name
the ceiling cause. `pending` SHALL appear only in the printed plan and progress.
Every `removed`, `refused`, `failed` or `unknown` target SHALL carry a
`reconciliation` object (`registry_entry_present`, `path_present`,
`branch_present`, `branch_sha`, `reconciled`), and a `not-attempted` target
SHALL carry null. The child's exit status alone SHALL never prove a removal. The
rescan SHALL first re-establish the repository identity, and where it differs
every reconciliation field SHALL be null and `reconciled` false. A target's
`notes` SHALL list `orphaned-directory` when its registry entry is absent and
its path present, and `partially-removed` when its removal child was killed at
the ceiling, or its exit could not be observed, and the rescan shows its
registry entry or its path remaining; a `partially-removed` target SHALL show
the recovery text "inspect, then `git worktree remove --force <path>` by hand".

Before the apply phase, SIGINT, SIGTERM or SIGHUP SHALL terminate and reap every
probe child, print "Cancelled." on standard error and no JSON document, and exit
130, 143 or 129 with nothing mutated, and end of input at the question SHALL
exit 130 the same way. During the apply phase, the first of
those signals received SHALL set the exit status and stop scheduling, so that no
further probe or removal starts. A removal in flight SHALL be waited for, and
its target SHALL end by the stage rule above. Targets not yet started SHALL be
`not-attempted` with `interrupted`. `project` SHALL then reconcile within the
reserve and print the result record; a second SIGINT during reconciliation SHALL
abandon the remaining rescans, leaving their fields null; after SIGHUP the
record SHALL be printed on a best-effort basis. An exception while handling a
target after the apply phase began SHALL make that target `unknown` with
`internal-error` and later targets `not-attempted`; an unexpected exception
before the apply phase SHALL refuse with `internal-error` and exit status 2. No
`unknown` or `failed` target SHALL be retried automatically, and `project` SHALL
never force a removal or delete a directory itself.

The exit status of a run with `--apply` SHALL be the first row that matches:

1. 130, 143 or 129: a signal was received, the first one received deciding, or
   input ended at the question (130);
2. 1: the deadline stopped work after the apply phase began, any target is
   `unknown`, or any target's reason is `removal-ceiling`;
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

### Requirement: Clean reports every path exactly or excludes it

`project clean` SHALL read every Git output that carries a path NUL-delimited,
so that newline, tab and other control characters in paths are supported. A
code point SHALL count as one to escape when its Unicode general category, as
the running interpreter's `unicodedata.category` reports it, is Cc, Cf, Zl or
Zp: for example the control characters U+0000 to U+001F and U+007F to U+009F,
and the bidirectional, format and separator characters U+200E, U+200F, U+2028,
U+2029, U+202A to U+202E and U+2066 to U+2069, as well as U+200B, U+FEFF and the
tag characters U+E0020 to U+E007F. In JSON, a path that is valid UTF-8 SHALL be
an ordinary string, exact after JSON unescaping, with `path_valid_utf8: true`,
and every code point to escape SHALL be written as a JSON escape, never raw. A
path that is not valid UTF-8 SHALL be written with each undecodable byte as the
four characters `\xHH`, in lowercase hexadecimal, and each literal backslash
doubled, with `path_valid_utf8: false`; its row SHALL be excluded as
`unsupported-path-bytes` and SHALL never be a removal operand.

Every path value in JSON SHALL carry its validity flag beside it, so that an
escaped `\xHH` is never read as a valid path holding those four characters.
Every object that carries a `path` (worktree rows; `selected`, `excluded` and
apply-result `targets` entries; refusals and row errors) SHALL carry
`path_valid_utf8` beside it. Each `ignored_samples` entry SHALL be an object
`{path, path_valid_utf8}`, its `path` relative to its worktree. `repository`
SHALL carry `root_valid_utf8` and `common_dir_valid_utf8`, the first also
covering the envelope's `root`, which names the same directory; both are always
true in `project clean`, because an invalid root or common directory refuses.

In human output a path SHALL print verbatim in prose, and with POSIX shell
quoting in commands, unless it contains a code point to escape or an
undecodable byte. Such a path SHALL print in the `$'...'` form in prose and
commands alike: each undecodable byte as `\xHH`, each code point to escape as
`\uXXXX`, or `\UXXXXXXXX` above U+FFFF, all in lowercase hexadecimal, each
backslash doubled and each single quote as `\'`. `ignored_samples` paths SHALL
be escaped like any other path. A `repository.root` or `common_dir` that is not
valid UTF-8 SHALL refuse with `unsupported-path-bytes` and exit status 2 before
any plan or digest is built.

#### Scenario: Control-character and non-UTF-8 paths

- **WHEN** eligible linked worktrees' paths contain a newline, a tab, U+0001 and
  U+202E, an otherwise eligible worktree's path contains the byte 0xFF, and the
  batch previews and applies
- **THEN** the first four are selected with exact JSON strings and
  `path_valid_utf8: true`, the human plan prints them in the `$'...'` form with
  `\u000a`, `\u0009`, `\u0001` and `\u202e`, Git receives each raw path as one
  argument, and a rescan proves each removed
- **AND** the fifth is excluded as `unsupported-path-bytes`, shown with `\xff`
  and `path_valid_utf8: false` in both `worktrees` and `excluded`, never passed
  to a removal command, and still present afterwards

#### Scenario: Non-UTF-8 repository root

- **WHEN** a repository's root path contains the byte 0xFF and `project clean
  <that root> --all-safe` runs
- **THEN** it refuses with `unsupported-path-bytes` and exit 2, no plan or
  digest is built, and nothing changes

### Requirement: Clean plans and refusals are versioned JSON

Every `project clean --json` SHALL print one JSON document with `schema_version:
1`. When a plan is built it SHALL be the plan envelope: `schema_version`,
`observed_at`, `mode` (`report`, `single` or `all-safe`), `root`,
`target_branch`, `tracking_freshness`, `worktrees`, `repository` (`root`,
`common_dir`, `dev`, `ino`, `root_valid_utf8`, `common_dir_valid_utf8`),
`merge_target`, `limits`, `budget`, `probes`, `operations`, `selected`,
`excluded`, `omitted`, `notes`, `completeness`, `apply_allowed`, `refusals` and
`plan_digest`. When no plan can be built it
SHALL be the existing error object `{"error": ...}` extended with `code`, then
`schema_version`, `observed_at`, `mode`, `repository` and `merge_target` (each
null unless established), `completeness: "incomplete"`, `apply_allowed: false`
and `refusals`. Baseline keys SHALL keep their names and types; `root` naming
the command directory, `ignored_files` counting the entries observed and
`present` possibly being null are the changes of meaning that this version
records. Worktree rows SHALL add `locked`, `ignored_files_truncated`,
`ignored_samples` (objects `{path, path_valid_utf8}`), `path_valid_utf8`,
`errors` and `notes`.

Refusals and row errors SHALL be `{code, message, path?, path_valid_utf8?,
reason?}` objects, `path_valid_utf8` present exactly when `path` is, with a
stable kebab-case `code`. The refusal codes SHALL be `invalid-arguments`,
`internal-error`, `git-unavailable`, `git-too-old`, `repository-not-found`,
`ambiguous-name`, `target-not-repository-root`, `unsupported-path-bytes`,
`manifest-invalid`, `no-merge-target`, `inspection-incomplete`, `inspect-cap`,
`deadline-exceeded`, `worktree-not-found`, `target-excluded`,
`plan-digest-mismatch`, `confirmation-required` and `cancelled`; `project clean`
SHALL NOT raise `target-cap`. The plan's `notes` codes SHALL be
`merge-target-conflict`; in `mode: "single"`, the non-blocking omissions
`inspection-incomplete`, `inspect-cap` and `deadline-exceeded`; and in
`mode: "report"` with more than 128 worktree rows, `inspect-cap` with `rows`,
the count of registered worktree rows, beside `selected: null` and the human
line saying that `--all-safe` itself would be incomplete with `inspect-cap`. A
target's `notes` codes SHALL be `orphaned-directory` and `partially-removed`,
and a worktree row's `notes` code `partially-removed`. A resolve refusal SHALL
print the extended error object, and a plan or select refusal SHALL print the
plan with `apply_allowed: false`. Null SHALL mean unknown or not established,
never a default false or 0, in every field this change adds. Enums SHALL be
closed within a schema version, and a rename, removal, type change or change of
meaning SHALL increment `schema_version`.

`--apply --json` SHALL be accepted with `--all-safe` and with `--action remove`
only, and SHALL print exactly one document on standard output: the plan envelope
or the extended error object when the run stops before the apply phase, and
otherwise the apply result record (`schema_version`, `observed_at`,
`repository`, `merge_target`, `plan_digest`, `probes`, `operations`, `targets`,
`exit_code` and `completeness`, each target carrying `path`,
`path_valid_utf8`, `branch`, `planned_sha`, `stage`, `reason`, `notes`,
`command`, `exit_status`, `probes_performed` and `reconciliation`). The human
plan, the question and progress SHALL then go to standard error. Two exceptions
SHALL print no JSON document: an argument-parser usage error SHALL print the
parser's message, as before this change; and SIGINT, SIGTERM or SIGHUP before
the apply phase, or end of input at the question, SHALL print "Cancelled." on
standard error and exit 130, 143 or 129, as "Clean records a reconcilable result
for every removal target" states.

#### Scenario: Apply with JSON prints one document

- **WHEN** `project clean <root> --all-safe --apply --yes --json` runs and
  removes two worktrees
- **THEN** standard output holds exactly one JSON document, the apply result
  record with two `removed` targets and `exit_code: 0`, and the human plan and
  progress are on standard error
- **AND** when the run stops before the apply phase with `plan-digest-mismatch`,
  standard output holds only the plan envelope

#### Scenario: The plain report in JSON

- **WHEN** `project clean <root> --json` runs on a repository with one eligible
  linked worktree
- **THEN** it prints one envelope with `schema_version: 1`, `mode: "report"`,
  `apply_allowed: false` and `limits.worktree_rows: 256`, with that worktree in
  `selected` and a `plan_digest`, and exits 0
