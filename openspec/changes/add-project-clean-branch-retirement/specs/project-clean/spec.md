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
repository identity, merge target and selection, since the mode is not in the
digest, and an `--expect-plan` carrying it SHALL match, which is intended,
except that a plan under `--retire-branches` has a digest of its own, as "Clean
retires a removed worktree's branch only on fresh head and ancestry evidence"
states, which no report's digest matches; the
digest also covers the merge target's name and SHA, so a target that advances
between the report and the preview gives `plan-digest-mismatch`, which is safe.
`apply_allowed` SHALL be false. It SHALL exit 0 when the report is complete, 1
when it is incomplete (`inspect-cap`, `inspection-incomplete` or
`deadline-exceeded`), and 2 when no report can be built, and its human output
SHALL say when and why it is incomplete.

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
core.fsmonitor=false -c protocol.allow=never -c protocol.file.allow=never -c
protocol.ssh.allow=never -c protocol.git.allow=never -c
protocol.http.allow=never -c protocol.https.allow=never -c
protocol.ext.allow=never -C <command directory> worktree remove <path>` in its
own process group; wait for it; and reconcile by rescan as
"Clean records a reconcilable result for every removal target" states. Under
`--retire-branches`, and only for a target that this rescan proves `removed`
with reason null and whose branch the confirmed plan retires, the sequence
SHALL then retire the target's branch as "Clean retires a removed worktree's
branch only on fresh head and ancestry evidence" states, before any later target
is revalidated. Removal SHALL stop after the first target whose result is not a
plain `removed`, or, under `--retire-branches`, whose `branch_retirement` is not
plain as that requirement defines it, a keep that the confirmed plan names being
plain, with no continuation, rollback or automatic retry.

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
`--retire-branches`, given with the removal, SHALL be such a separate, explicit
action: a stage of its own after the rescan proves the worktree gone, never the
default; without it every selected worktree's local branch SHALL remain.
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
an excluded row leaves it unchanged; under `--retire-branches` that text SHALL
also carry the branches the plan retires, as "Clean retires a removed
worktree's branch only on fresh head and ancestry evidence" states, and without
the flag it SHALL carry nothing more. `--expect-plan D` SHALL refuse with
`plan-digest-mismatch` and exit status 2, before any question and any mutation,
when the fresh digest differs from D, and SHALL still print the fresh plan. The
confirmation SHALL be one default-No question naming the count of worktrees to
remove and of branches kept, or, under `--retire-branches`, of branches to
retire and to keep, ending `[yes/N]`; only `yes`, surrounding
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
apply SHALL print `Removed N; branches kept: ` followed by the branches kept,
except that under `--retire-branches` every apply result SHALL print instead the
summary line and the branch lines that "Clean retires a removed worktree's
branch only on fresh head and ancestry evidence" states.

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
be `not-attempted` with `deadline-exceeded`. A branch stage of
`--retire-branches`, as "Clean retires a removed worktree's branch only on
fresh head and ancestry evidence" states, SHALL start its re-read, that
re-read's re-proof of the reflog, and its branch child only while more than
that floor remains, a strict test, where a removal child is spawned while at
least that floor remains, so that with exactly that floor left a removal child
is spawned and none of the stage's children starts. The re-read's manifest
read and ref listing, and its re-proof's reflog read and child, SHALL get
`min(5 s, work remaining less the removal floor)`, so that the floor is left
for the branch child. A
removal child still running at
the deadline SHALL be waited for, up to its 300 s hard ceiling, and the
reconciliation reserve SHALL count from its exit. A run with no removal in
flight SHALL therefore end within 64 s of its start, not counting the time
blocked at the confirmation question (50 s of work, the 10 s reserve, and up to
4 s to stop and reap a probe child), and a removal in flight SHALL add at most
300 s, except while a filesystem call stuck in the kernel is outstanding. Push
children and the children of the explicit `delete-branch` action SHALL stay
unbounded, as before this change; the branch child of `--retire-branches` SHALL
be bounded as "Clean retires a removed worktree's branch only on fresh head and
ancestry evidence" states.

The caps SHALL be: at most 128 worktree rows in
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
worktrees" states for a single-target removal, and except that a reflog child of
`--retire-branches` that fails or times out at its own 5 s budget SHALL keep
branches and leave the plan complete, as "Clean retires a removed worktree's
branch only on fresh head and ancestry evidence" states. A preview or report
SHALL exit 1 when its plan is incomplete and 0 when it is complete, deferred
rows included.

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

Plans and apply results SHALL report `probes: {estimated, performed}` and
`operations: {estimated, performed}`, every Git child counted once, a removal,
or a branch child of `--retire-branches`, under `operations` and every other
child under `probes`; `limits`
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
before the apply phase SHALL refuse with `internal-error` and exit status 2.
Under `--retire-branches` an exception raised in a target's branch stage SHALL
instead leave that target as its rescan decided it, as "Clean retires a
removed worktree's branch only on fresh head and ancestry evidence" states. No
`unknown` or `failed` target SHALL be retried automatically, and `project` SHALL
never force a removal or delete a directory itself.

The exit status of a run with `--apply` SHALL be the first row that matches:

1. 130, 143 or 129: a signal was received, the first one received deciding, or
   input ended at the question (130);
2. 1: the deadline stopped work after the apply phase began, a branch stage's
   `deadline-exceeded` under `--retire-branches` included, any target is
   `unknown`, any target's reason is `removal-ceiling`, or, under
   `--retire-branches`, any target's `branch_retirement` has a null `stage`;
3. Git's own status, passed through unchanged: a target is `failed` with
   `git-refused` or `git-failed`;
4. 2: any refusal; a `refused` target; a `removed` target with a
   branch-after-removal reason; a `failed` target with `spawn-error`; under
   `--retire-branches`, a target `removed` with reason null whose
   `branch_retirement` is not plain, as "Clean retires a removed worktree's
   branch only on fresh head and ancestry evidence" defines it;
5. 0: every selected target is `removed` with reason null and, under
   `--retire-branches`, its `branch_retirement` is plain, a keep that the
   confirmed plan names included; or nothing is eligible.

A preview or report SHALL exit 2 only for a refusal raised before a plan is
built, 1 for an incomplete plan, and 0 otherwise, the signal exits above
excepted.

A run that stops SHALL end its human result with `Stopped at P (reason). Removed
k of n. Not attempted: ... Next: ` followed by the command that shows a fresh
read-only plan, or, under `--retire-branches`, with the lines that "Clean
retires a removed worktree's branch only on fresh head and ancestry evidence"
orders after it, and SHALL name every retained branch.

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

### Requirement: Clean retires a removed worktree's branch only on fresh head and ancestry evidence

`project clean` SHALL accept `--retire-branches` only with `--all-safe`, as a
read-only preview or with `--apply`, and with `--apply --action remove
--worktree P`. With any other combination, the plain report, `--action push`
and `--action delete-branch` among them, it SHALL refuse with
`invalid-arguments` and exit status 2 before any plan is built, and SHALL run
nothing. The flag SHALL never be the default: without it every branch remains,
as "Clean can explicitly retire verified worktrees" states, and every key this
requirement adds to a plan or a result SHALL be absent, never null, because
null means unknown or not established. `--json` SHALL be accepted with the flag
exactly where "Clean plans and refusals are versioned JSON" accepts it without
the flag. The two per-target sub-records this requirement adds SHALL be
present under the flag only: `branch_retirement` on each target of an apply
result record, beyond the target keys that requirement lists, and `branch_plan`
on each entry of a plan's `selected`, whose keys that requirement does not
list; the plan envelope SHALL gain no key. The flag SHALL change no gate and no
selection.

Under the flag the plan SHALL decide, for each selected row, whether its branch
is retired or kept, and SHALL keep it for the first of these reasons that
holds:

1. `reflog-unmerged`: a commit that the branch's reflog names is not proven an
   ancestor of the merge target's SHA, a commit being named when it is the new
   object of an entry of `logs/refs/heads/<branch>`, as the `unstarted-branch`
   gate read it, or the non-zero old object of one, the oldest surviving entry's
   old object included. The plan SHALL NOT repeat that read: a read that fails
   or does not finish is the gate's own outcome, as the gate's rule above
   states it, a row excluded as `reflog-unavailable` or `inspection-error`, or
   left unprobed with the plan incomplete for the reason that rule gives such a
   read, so that no row reaches this keep without a read the gate finished,
   and the plan's own failed proof is its Git child's alone. The proof SHALL
   be one Git child per repository,
   `rev-list --max-count=1 --stdin`, given on its standard input the named
   commits of every selected row, one per line, and then the one line
   `^<merge target SHA>`, `^` immediately followed by the merge target's SHA
   on that one line, never `^` on a line of its own, a revision that excludes
   the merge target's history, never the pseudo-option `--not`, and, only when
   that child prints a commit, one such child per selected row over that row's
   named commits and the same line. A row whose child prints a commit, or
   whose proof fails or times out, a failure or timeout of the repository's
   child failing every row's proof, SHALL keep its branch. Such a failure, or
   a timeout at a reflog child's own 5 s budget, SHALL keep the branches it
   covers and SHALL leave the plan complete; only the deadline passing during
   the proof SHALL make the plan incomplete, with `deadline-exceeded`, as
   "Clean bounds its Git work and reports omitted work" states for planning.
   A row whose proof did not finish, the deadline passing while it ran or
   before it started, SHALL keep its branch with `reflog-unmerged` too, in its
   `branch_plan` and its plan line, although no apply runs on such a plan.
2. `branch-in-use`: a registered worktree that is not selected, the main
   worktree included, has the branch checked out in the plan's registry
   listing.
3. `head-not-merge-target`: the branch's configured upstream's remote-tracking
   ref is absent, so that Git's own non-force check judges the branch against
   the command directory's `HEAD`, and that `HEAD`, as the main worktree's row
   of the registry listing gives it, is not the merge target's SHA. This test
   MAY keep a branch that Git would accept, which is the safe direction.
4. `branch-shared`: another selected row later in canonical order holds the
   same branch, which is then decided at the last of its holders, the only one
   whose branch stage can run.

The printed plan SHALL read `  remove PATH and retire BRANCH` for a row whose
branch it retires, `  remove PATH; keep BRANCH (REASON)` for one whose branch
it keeps, `REASON` reading `checked out at PATH2` for `branch-in-use`, and
`  remove PATH; BRANCH is decided at PATH2` for an earlier holder of a shared
branch, `PATH2` being its last holder, where a plan without the flag prints
`  remove PATH [BRANCH]`. Each entry of the plan's `selected` SHALL carry
`branch_plan`, an object `{action, reason}`, `action` being `retire` or `keep`
and `reason` null or the keep's reason. The canonical JSON text of `plan_digest`
SHALL also carry a member named `retire`, placed wherever that text's
construction places a member, which this requirement does not fix: the
`[branch, planned_sha]` pairs of the branches the plan retires, ordered as
`selected` is, in canonical order, each pair at its branch's last holder, and
present when empty, so that `--expect-plan` binds a flagged apply only
to a flagged preview: a digest taken without the flag SHALL refuse a flagged
apply with `plan-digest-mismatch` and exit status 2, before any question or
mutation, as any mismatch does. Without the flag nothing SHALL be added to the
canonical text, so that the digest is the one a run without this requirement
computes.

Under the flag, and only for a target whose rescan proves it `removed` with
reason null and whose branch the confirmed plan retires, the run SHALL retire
the target's local branch in a branch stage that follows that rescan and
precedes any later target's revalidation, in this order:

1. Re-read the manifest by a filesystem read and the branch with one ref
   listing in the command directory, narrowed as the revalidation's ref listing
   is, each under `min(5 s, work remaining less the removal floor)`.
2. Check, stopping at the first check that fails: the branch exists; its head
   equals the reconciliation record's `branch_sha`; its `upstream`,
   `upstream_oid`, `ahead` and `behind` and the manifest's `tracking_branch`
   equal the plan's, a value null in the plan and null at the re-read not
   counting as a difference; the merge target, re-resolved from that manifest
   read and that listing, has the plan's `name`, `source` and `sha`, so that
   the plan's proof that the head is an ancestor of the merge target holds at
   the target's current tip, and no Git child but item 3's re-proof, given the
   head among the commits the reflog names, computes it again; and no
   registered worktree, the main worktree included, has the branch checked
   out in the registry listing of that rescan. A value that manifest read or
   that listing cannot establish, a read that fails or times out at its own
   5 s budget included, SHALL count as a difference; a read whose budget the
   work deadline ends SHALL count as no difference, and the stage SHALL then
   spawn nothing more and SHALL retain the branch with `deadline-exceeded`.
3. Re-prove the reflog, as the re-read's last step and under its budget,
   because a branch moved to a commit the merge target lacks and back to its
   planned SHA between the plan and the stage passes every check above while
   its reflog names that commit: read `logs/refs/heads/<branch>` again as the
   `unstarted-branch` gate reads it, and spawn one probe child in the command
   directory, `rev-list --max-count=1 --stdin`, given on its standard input
   every commit that the reflog now names, in item 1's sense of the plan's
   keeps, one per line, and then the one line `^<merge target SHA>`, as the
   plan's proof is given. A re-proof whose child prints a commit
   SHALL keep the branch, and so SHALL one whose read finds the reflog missing
   or empty or reaches its 64 KiB bound, or one whose read the gate's reading
   cannot decide, a line that does not parse or a last entry whose new object
   is not the head the re-read observed included: each is a value that the
   proof decided, and the stage SHALL then spawn nothing more and SHALL retain
   the branch with `reflog-unmerged`, so that no branch child runs on a reflog
   the stage has not proved. A re-proof whose read or child fails, or runs past
   its own 5 s budget while the work deadline is not the limit, decides no
   value: the stage SHALL spawn nothing more and SHALL retain the branch with
   `state-changed`, as it does for a value that the re-read cannot establish.
   A re-proof whose budget the work deadline ends SHALL retain the branch with
   `deadline-exceeded`.
4. Spawn the non-force command `git -c protocol.allow=never -c
   protocol.file.allow=never -c protocol.ssh.allow=never -c
   protocol.git.allow=never -c protocol.http.allow=never -c
   protocol.https.allow=never -c protocol.ext.allow=never -C <command
   directory> branch -d -- <branch>`, in its own process group, with the
   environment that "Repository inspection requires Git 2.36 and shares one
   evidence model" gives every Git child, the variables it removes and the
   variables it sets, any trace2 variables among them, and no
   `GIT_OPTIONAL_LOCKS`, which it gives to read-only probes alone, under
   `min(5 s, work remaining)`. The branch child
   SHALL NOT be signalled on SIGINT, SIGTERM or SIGHUP, and SHALL be waited for
   within that budget; past it, its process group SHALL receive SIGTERM and,
   2 s later, SIGKILL, and its reap SHALL wait at most a further 2 s.
5. Once a branch child was spawned, re-read the branch with one more such
   listing, under `min(5 s, reserve remaining)`, and decide the stage by that
   post-check. The branch child's exit status alone SHALL never prove a
   retirement.

The re-read, its re-proof and the branch child SHALL each start only while more
than the 5 s removal floor of the work deadline remains, so that a branch child
always has its whole budget and the deadline never stops it; the branch child,
a mutation, SHALL never be abandoned at its budget, and none of the three SHALL
start after a signal has been received. A stage that cannot start its re-read,
its re-proof or its branch child for either cause SHALL spawn nothing more and
SHALL retain the branch with `deadline-exceeded` or `interrupted`. A signal
SHALL stop no read or child of the stage, the post-check excepted, which a
second SIGINT SHALL abandon as "Clean records a reconcilable result for every
removal target" abandons the remaining rescans: a signal received while the
re-read, its re-proof or the branch child runs SHALL let it run to its own end
or budget, its outcome deciding as above, and SHALL only keep the stage from
starting its next re-read, re-proof or branch child, never the post-check.
The stage
SHALL never pass `-D`, `--force` or `-f`, never spawn a second branch child for
a target, never retry, and never delete, push or fetch a remote branch or
change a remote-tracking ref. Git's own refusal SHALL retain the branch. A
worktree in which a rebase or a bisect of the branch is in progress is listed
detached in the registry listing, so that neither the plan's `branch-in-use`
keep nor the stage's check of that listing sees it: that holder is a residual
left to Git's own check, which refuses the deletion, so that the branch is
retained with `git-refused` and the run stops.

Under the flag every target of the apply result record SHALL carry
`branch_retirement`, an object `{stage, reason, branch, planned_sha,
observed_sha, post_check_sha, command, exit_status, probes_performed}`:
`branch` and `planned_sha` are the target's; `observed_sha` is the head the
re-read found, null when it found none or did not run; `post_check_sha` is
the head the post-check listed, null when it listed none, the branch being
absent, or did not run; `command` is the branch child's
argument vector, null when none was spawned; `exit_status` is its exit status,
null when none was spawned or its exit could not be observed; and
`probes_performed` counts the stage's re-read children, its listing and its
re-proof, and its post-check child, 0 to 3, while the target's own
`probes_performed` keeps counting the Git children of its revalidation.
`stage` SHALL be one of these, with one reason, the sub-record's `git-refused`
and `git-failed` naming the branch child's outcomes below and not the target's
split of exit statuses at 128:

- `retired`: the post-check shows the branch absent after its branch child
  ran; reason null when the child exited 0, `git-failed` when it exited
  nonzero, `probe-timeout` when `project` stopped it past its budget, and
  `internal-error` when an exception ended the stage after that post-check;
- `retained`: the target is `removed` and its branch is present when the stage
  ends; `branch-changed` (the re-read found another head, or the target is
  `removed` with `branch-advanced-after-removal` and no stage ran),
  `state-changed` (the re-read found an upstream value, the manifest's
  `tracking_branch` or the merge target different from the plan, or could not
  establish one of them at its own budget, or its re-proof's reflog read or
  child failed or ran past its own budget, each while the work deadline is not
  the limit), `branch-in-use` (the rescan's
  registry listing shows
  a worktree holding the branch), `reflog-unmerged` (the re-proof printed a
  commit, or its read decided that the reflog cannot be proven, one missing,
  empty, read to its 64 KiB bound or undecidable by the gate's reading),
  `deadline-exceeded` (too little of
  the work deadline remained to start the re-read, its re-proof or the branch
  child, or the deadline stopped the re-read), `interrupted`, `spawn-error`,
  `git-refused` (the child exited nonzero), `unconfirmed-retirement` (the
  child exited 0), `probe-timeout`, `internal-error` (an exception ended the
  stage before its branch child was spawned, or after the post-check showed
  the branch present), or `removal-ceiling` (the target's own reason, no stage
  having run);
- `not-attempted`: the plan kept the branch, no branch remained to retire, or
  no stage ran for the target; `reflog-unmerged`, `branch-in-use`,
  `head-not-merge-target` or `branch-shared` (the plan's keep, which a row the
  plan keeps SHALL carry whatever its own stage), `branch-missing` (the rescan
  or the re-read found no branch, the target `removed` with
  `branch-missing-after-removal` included), `branch-retention-stop` (the
  target is `not-attempted` because the run stopped after an earlier target
  that was `removed` and whose `branch_retirement` was not plain), or
  `target-not-removed` (every other target that no stage reached: one that is
  `refused`, `failed` or `unknown`, or `not-attempted` for any other cause, a
  signal or the deadline after an earlier plain outcome included);
- null, with reason `reconciliation-incomplete`, only when the post-check
  failed, timed out or was abandoned, or an exception ended the stage after
  its branch child was spawned and before the post-check decided, so that
  whether the branch exists is not established.

A `branch_retirement` SHALL be plain when it is `retired` with reason null or
`not-attempted` with one of the plan's four keep reasons. The target's
`reconciliation` SHALL remain the rescan that decided its removal; the branch
stage's evidence SHALL be in `branch_retirement` alone. A null `stage` SHALL
make the apply result's `completeness` incomplete. The record SHALL add no
value to the target's `stage` or `reason` enums, to the ladder, to the gates,
or to the refusal and note codes.

An exception raised in a target's branch stage SHALL leave that target's
`stage`, `reason` and `reconciliation` as its rescan decided them, never
`unknown` with `internal-error`, and SHALL give its `branch_retirement` the
stage that the stage's evidence then establishes, as the list above states,
never `not-attempted` with `target-not-removed`: a branch the post-check showed
absent after its branch child ran is `retired`, and the result prints its line
with the SHA and the restore command. Such a `branch_retirement` is never
plain, so the run stops after that target.

Removal SHALL stop after the first target that is `removed` and whose
`branch_retirement` is not plain, as it stops after the first target that is
not a plain `removed`. A keep that the confirmed plan names SHALL neither stop
the run nor by itself raise the exit status: that row exits as it would in a
run without the flag. Every target after such a stop SHALL be `not-attempted`
with reason `batch-stopped`, or `interrupted` or `deadline-exceeded` where a
signal or the deadline stopped the run, and, unless the plan keeps its branch,
SHALL carry `branch_retirement` `not-attempted` with reason
`branch-retention-stop`. The exit status SHALL be the one that "Clean records a
reconcilable result for every removal target" orders: a branch that the stage
retains exits 2 unless a signal, the deadline or a null `stage` decides first.

The plan's reflog children, the re-read's listing and re-proof, and the
post-check SHALL be counted under `probes`, and the branch child under
`operations`, so that under the flag `operations.estimated` SHALL add one per
branch the plan retires and `probes.estimated` three per branch the plan
retires and the reflog children the plan spawned. The plan SHALL spawn at most
one reflog child per repository and one per selected row, and the stage at most
four Git children per target, one of them a branch child, so that
`limits.targets` caps the branch children of a
run and `budget.probe_timeout_seconds` bounds each; no `limits` or `budget`
member is added. A run with no removal in flight SHALL still end within 64 s of
its start, not counting the time blocked at the confirmation question.

A flagged `--apply`, single or batch, is a removal apply: on a standard input
that is not a terminal and without `--yes`, once its plan has passed the
checks that "Clean previews and applies a batch of eligible worktree removals
in one repository" runs before any question, it SHALL refuse with
`confirmation-required` and exit status 2 before any mutation, as "Clean hands
off work requiring review" states for a removal apply, so that no branch stage
starts; any refusal that requirement keeps for branch deletion is the explicit
`delete-branch` action's, with which the flag is refused as
`invalid-arguments`.

The confirmation SHALL be the one default-No question that "Clean previews and
applies a batch of eligible worktree removals in one repository" states,
reading `Remove N worktrees and retire their M local branches? [yes/N]` when
the plan keeps no branch and `Remove N worktrees, retire M local branches and
keep K? [yes/N]` when it keeps K, M and K counting distinct branches, a shared
branch at its last holder, and `worktree` and `branch` singular for a count of
1, or `Remove 1 worktree and retire its local branch? [yes/N]` for one worktree
whose branch the plan retires. Every apply result SHALL print `Removed N;
their branches retired: R; retained: K`, followed by `; already gone: G` when G
is above 0 and `; unconfirmed: U` when U is above 0, R, K, G and U counting the
distinct branches of the removed targets that were retired, that remain, that
were already gone and whose `branch_retirement` has a null `stage`, so that
they add up to those branches; then one line per such branch, in canonical
order:

- `Retired BRANCH (was SHA); restore: git -C ROOT branch BRANCH SHA`, or, for
  a name that `git branch` refuses to create, one that begins with `-` or that
  equals `HEAD`, `Retired BRANCH (was SHA); restore: git -C ROOT update-ref
  refs/heads/BRANCH SHA ''`, a form only defensive where BRANCH is `HEAD`,
  since under either setting of Git's `core.warnAmbiguousRefs` the row of a
  worktree on `refs/heads/HEAD` is `inspection-error` before any plan
  selects it, so that no run retires such a branch: under the default every
  status probe of a repository that holds `refs/heads/HEAD` exits 0 and
  warns `refname 'HEAD' is ambiguous.`, which makes every row of it
  `inspection-error`, and with that setting false, where the probe exits 0
  with nothing on standard error, that row's upstream evidence cannot be
  read, since the ref listing gives a branch named `HEAD` the upstream of
  the command directory's current branch, which is its own only where that
  directory is the worktree on `refs/heads/HEAD`; each followed,
  for every local branch BRANCH2 that the run did not retire and whose
  configured upstream the plan's ref
  listing gives as `refs/heads/BRANCH`, by `Note: BRANCH2 tracks BRANCH as its
  upstream, which now reads gone; no commit is lost`, BRANCH2 printed in prose
  as BRANCH is;
- `BRANCH was already gone` for `branch-missing`;
- `Unconfirmed BRANCH (was SHA); if git -C ROOT rev-parse --verify
  refs/heads/BRANCH fails, restore: ` followed by the restore command that the
  `Retired` line would print, and then `; otherwise retry: RETRY`, for a null
  `stage`, which never gets a `Kept` line;
- `Kept BRANCH (REASON)` and its next step: for `head-not-merge-target`, `;
  next: check out MERGE_TARGET in the main worktree; BRANCH's reflog was
  proven merged into MERGE_TARGET only at this run's plan; inspect git -C ROOT
  reflog show refs/heads/BRANCH before retrying: RETRY`, or, when the plan's
  registry listing shows MERGE_TARGET checked out in a linked worktree at
  PATH2, where Git refuses that checkout, `; next: MERGE_TARGET is checked out
  at PATH2, so check out its tip TARGET_SHA detached in the main worktree;
  BRANCH's reflog was proven merged into MERGE_TARGET only at this run's plan;
  inspect git -C ROOT reflog show refs/heads/BRANCH before retrying: RETRY`;
  for `git-refused` when the branch's upstream
  remote-tracking ref is absent, `; Git refused the deletion; if another
  worktree holds BRANCH, a rebase or bisect of it there included, wait for any
  rebase or bisect there to end, and then switch that worktree off BRANCH by
  running git switch --detach there, which changes none of its files` and
  then `; next: check out MERGE_TARGET in the main worktree, then: RETRY`,
  or, where the plan's registry listing shows MERGE_TARGET checked out in a
  linked worktree at PATH2, `; next: MERGE_TARGET is checked out at PATH2, so
  check out its tip TARGET_SHA detached in the main worktree, then: RETRY`;
  for `branch-in-use` and for `branch-shared`, PATH2 being the worktree that
  holds BRANCH, for `branch-shared` its last holder, a selected row and so
  never the main worktree, whose line is printed only when the run did not
  remove that holder: `; next: BRANCH is checked out at PATH2, which this run
  selected and did not reach; remove it and retire BRANCH with project clean
  ROOT --apply --action remove --worktree PATH2 --retire-branches`, which
  prints no retry, only where PATH2 is the last holder of a `branch-shared`
  branch and is `not-attempted`, a holder the plan selected, since this run's
  read of it is its plan's alone, the run having stopped before it
  revalidated that holder, and that command removes PATH2 only if a fresh
  plan of its own selects it, every gate read again, and retires BRANCH only
  on that plan's proof of its reflog, where `git worktree remove` would
  delete, with exit 0, state that the holder gained since and that the gates
  protect, a commit that only its HEAD reflog holds among it; `; next:
  BRANCH is checked out at PATH2; its path could not be read, so do not run
  git worktree prune, git worktree remove or git gc until it can; once it
  can, HOLD`, where PATH2 is a row of the plan whose path could not be read,
  its `present` null; `; next: BRANCH is checked out at PATH2; its path is or
  holds the main worktree, the common directory or another worktree, so do
  not delete it by hand or with git worktree remove; review its registration
  with git worktree list --porcelain; once it is repaired, switch that
  worktree off BRANCH by running git switch --detach there, which changes
  none of its files; BRANCH's reflog was proven merged into MERGE_TARGET only
  at this run's plan; inspect git -C ROOT reflog show refs/heads/BRANCH
  before retrying: RETRY`, where PATH2 is a linked row that the plan excludes
  as `registration-mismatch` because its path is, or holds, the main
  worktree, the common directory or another worktree, or is another row's
  path, even one whose path is the main worktree's, so that a step run at
  PATH2 acts on another worktree, and the worktree that the repaired
  registration names still holds BRANCH; `; next: BRANCH is checked out at
  PATH2, whose path is missing; if that worktree still exists, moved or on a
  drive that is not mounted, remount or repair it and switch it off BRANCH by
  running git switch --detach there, which changes none of its files;
  otherwise STALE; BRANCH's reflog was proven merged into MERGE_TARGET only
  at this run's plan; inspect git -C ROOT reflog show refs/heads/BRANCH
  before retrying: RETRY`, where PATH2 is a row of the plan whose path is
  missing, its `present` false, a `stale-worktree` row, at which `git -C
  PATH2 switch --detach` cannot run, STALE being `review and prune stale
  worktree metadata manually; git worktree prune also deletes the entry, and
  so the HEAD reflog, of every other worktree whose path is missing, one
  moved or on an unmounted drive included, so run git worktree prune
  --dry-run first and remount or repair any it lists that still exists` or,
  where a row of the plan has `present` null, `review and prune stale
  worktree metadata manually; a row's path could not be read, so do not run
  git worktree prune, git worktree remove or git gc until it can`, either
  beginning `review, unlock it, then prune` in the place of `review and
  prune` where PATH2's row is locked, since `git worktree remove` and `git
  worktree prune` each delete such an entry's administrative directory with
  exit 0, and with it the HEAD reflog of a worktree that was only moved or
  unmounted; where PATH2 is the main worktree, which Git refuses to
  remove, `; next: BRANCH is checked out at PATH2, the main worktree; switch
  it off BRANCH, by detaching it with git -C PATH2 switch --detach, which
  changes none of its files, or by checking out MERGE_TARGET there; BRANCH's
  reflog was proven merged into MERGE_TARGET only at this run's plan; inspect
  git -C ROOT reflog show refs/heads/BRANCH before retrying: RETRY`, whether
  the branch's upstream remote-tracking ref is present or absent, which names
  no other branch, since Git judges the retry against that worktree's `HEAD`
  when that ref is absent, and a checkout of a branch, with exit 0 and
  without a word, overwrites an ignored file at a path that the branch tracks,
  deletes an ignored file where the branch needs a directory and deletes every
  ignored file below a path that the branch tracks as a file; and
  otherwise `; next: BRANCH is checked out at PATH2; HOLD`, HOLD being `save
  its own work, uncommitted, ignored or flagged assume-unchanged or
  skip-worktree, by keeping that worktree and switching it off BRANCH with git
  -C PATH2 switch --detach, which changes none of its files; BRANCH's reflog
  was proven merged into MERGE_TARGET only at this run's plan; inspect git -C
  ROOT reflog show refs/heads/BRANCH before retrying: RETRY`,
  in which, and in the forms above for a path that is or holds another
  worktree and for a path that is missing, where the plan finds the branch's
  upstream remote-tracking ref absent and the main worktree's `HEAD` not the
  merge target's SHA, as `head-not-merge-target` tests, `; BRANCH's reflog
  was proven merged` is preceded by `; then check out MERGE_TARGET in the
  main worktree` or, where the plan's registry listing shows MERGE_TARGET
  checked out in a linked worktree at
  PATH3, by `; then, MERGE_TARGET being checked out at PATH3, check out its
  tip TARGET_SHA detached in the main worktree`; for `branch-changed`, `; now
  at SHA2; its reflog is not proven merged into MERGE_TARGET; inspect it and
  git -C ROOT reflog show refs/heads/BRANCH before retrying: RETRY`, SHA2
  being the head the re-read found, its `observed_sha`, or, where no re-read
  ran, as for `branch-advanced-after-removal`, the reconciliation record's
  `branch_sha`; for `reflog-unmerged`, whether its proof printed a
  commit, the plan's proof failed, or the re-proof found the reflog missing,
  empty, at its bound or undecidable, `; its reflog is not proven merged
  into MERGE_TARGET; inspect every commit it names, the old and the new of
  each entry, as cat REFLOG prints them, before any delete-branch`, REFLOG
  being `COMMON_DIR/logs/refs/heads/BRANCH`, the file that the
  `unstarted-branch` gate read and the re-proof reads again, and COMMON_DIR
  the plan's `repository.common_dir`, since git reflog show prints only each
  entry's new commit, and a commit that the reflog names only as an entry's
  old one, as an expired entry can leave it, a default `git gc` among the
  causes, would go unseen; for `git-refused` when the branch's upstream
  remote-tracking ref is present, `; Git refused the deletion; if another
  worktree holds BRANCH, a rebase or bisect of it there included, wait for any
  rebase or bisect there to end, and then switch that worktree off BRANCH by
  running git switch --detach there, which changes none of its files; then
  retry: RETRY`; for a `retained` stage whose post-check listed the branch at
  a head other than its `observed_sha`, whatever its reason, in the place of
  the line that reason would print, `; now at SHA2; its reflog is not proven
  merged into MERGE_TARGET; inspect it and git -C ROOT reflog show
  refs/heads/BRANCH before retrying: RETRY`, SHA2 being that head, its
  `post_check_sha`, the branch having moved after its re-proof; and for every
  other reason, `state-changed`, `deadline-exceeded`, `interrupted`,
  `spawn-error`, `unconfirmed-retirement`, `probe-timeout`, `internal-error` and
  `removal-ceiling`, `; retry: RETRY` only when the stage's re-proof proved
  the reflog merged, as it has for `spawn-error`, `unconfirmed-retirement` and
  `probe-timeout` and for a `deadline-exceeded`, `interrupted` or
  `internal-error` that came after that proof, and otherwise, when the stage
  did not re-prove the reflog, its re-proof never starting or never finishing
  with a proof, `; BRANCH's reflog was proven merged into MERGE_TARGET only at
  this run's plan; inspect git -C ROOT reflog show refs/heads/BRANCH before
  retrying: RETRY`: the plan's proof of the reflog holds only until the stage's
  re-proof renews it, since a branch moved to a commit the merge target lacks
  and back passes every check of the re-read, and RETRY proves only the branch's
  tip and would delete the branch with a reflog that may name a commit only that
  reflog holds. The `head-not-merge-target` and `branch-changed` lines, the
  `branch-in-use` and `branch-shared` lines other than the one that names
  PATH2's flagged removal, and the line of a branch that moved after its
  re-proof name that inspection for the same reason, their own steps ending
  in RETRY for a branch whose reflog the stage did not re-prove, or proved
  before the branch moved: a plan's keep spawns no stage, a stage that keeps
  a branch with `branch-in-use` or `branch-changed` stops before its
  re-proof, or never starts, and a move after the re-proof can write a commit
  that no proof saw.
  The lines that name that inspection for `state-changed`, `deadline-exceeded`,
  `interrupted`, `internal-error` and `removal-ceiling`, and the
  `head-not-merge-target`, `branch-in-use` and `branch-shared` lines, say that
  only this run's plan proved BRANCH's reflog: the plan tests `reflog-unmerged`
  before its other keeps and before it retires a branch, so that it proved the
  reflog of every branch that it kept for a later reason or retired, a proof
  that the retry does not make again; the `branch-changed` line and the line
  of a branch that moved after its re-proof keep `its reflog is not proven
  merged`, the branch having moved since a proof; and the `git-refused` lines
  and the `Unconfirmed` line keep the bare retry after their own steps, their
  branch child having run after the re-proof proved the reflog, and the
  post-check, where it decided, having found the branch where the re-read
  found it.

RETRY is `project clean ROOT --apply --action delete-branch --branch
BRANCH`, or `--branch=BRANCH` for a name that begins with `-`, the explicit
retry path, whose behaviour this requirement does not change. For a name that
begins with `-`, RETRY is the command that action is given, and that action
deletes the branch only if it passes the name to Git after `--`, which is its
own behaviour and not this requirement's.

A `branch-shared` holder SHALL get no line of its own: its branch has one line,
the last holder's when the run removed that holder, and otherwise the
`branch-shared` line above. No line SHALL name `-D` or any force. Each word of
a printed command that holds BRANCH or MERGE_TARGET, such as `BRANCH`,
`--branch=BRANCH`, `refs/heads/BRANCH` or REFLOG, SHALL be printed by the rule
that "Clean reports every path exactly or excludes it" sets for a path, as
ROOT and PATH2 are:
the name verbatim in prose and with POSIX shell quoting in commands, the word
quoted as one, and in the `$'...'` form in prose and commands alike when it
holds a code point to escape or an undecodable byte. Every `project clean ROOT
--all-safe` command that the plan or the result prints for the person to run
next, the deferral line and the stop block's `Next:`, SHALL carry
`--retire-branches`; RETRY SHALL NOT, since the flag with `--action
delete-branch` is refused: the deferral line SHALL read `run again: project
clean ROOT --all-safe --apply --retire-branches`. A run
that stops SHALL print the stop block that "Clean records a reconcilable
result for every removal target" states, whose reason, when a branch stage
stopped the run, SHALL read `branch BRANCH: REASON`, and whose `Next:` command
SHALL be the flagged preview `project clean ROOT --all-safe
--retire-branches`. Under the flag the human result SHALL end with these
lines, in this order: in a run that stops, that stop block, then the retained
branches it names, which SHALL be only the branches that remain, never one
that its branch line names retired, already gone or unconfirmed; then the
summary line and the branch lines, in the place of the success line `Removed
N; branches kept: `; and then the residual-window line.

#### Scenario: Retire the branches of a batch

- **WHEN** two eligible linked worktrees P1 and P2, on branches b1 and b2, each
  merged, clean and published with a commit of its own, P1's upstream's
  remote-tracking ref present and P2's deleted, sit beside the main worktree on
  the merge target, and `project clean <root> --all-safe --apply --yes
  --retire-branches` runs
- **THEN** the plan lists `  remove <P1> and retire b1` and `  remove <P2> and
  retire b2`, P1 is removed and b1 then deleted, then P2 the same, in
  canonical path order, each target `removed` with reason null and its
  `branch_retirement` `retired` with reason null, `observed_sha` equal to
  `planned_sha`, `post_check_sha` null, `exit_status` 0 and
  `probes_performed` 3
- **AND** P1's remote branch and its remote-tracking ref remain, nothing is
  fetched or pushed, the result prints `Removed 2; their branches retired: 2;
  retained: 0`, then `Retired b1 (was <b1's planned_sha>); restore: git -C
  <root> branch b1 <b1's planned_sha>` and the same line for b2, and the exit
  status is 0
- **AND** a counting `git` wrapper on PATH records one reflog child before the
  question, and each branch child with `-c protocol.allow=never`, the six
  per-protocol pins, `-C <command directory>` and `branch -d -- <branch>`, the
  environment that "Repository inspection requires Git 2.36 and shares one
  evidence model" gives every Git child, the variables it removes absent and
  any trace2 variables it sets as it sets them, and `GIT_OPTIONAL_LOCKS`
  absent, and a process group of its own, and none with `-D`, `--force` or
  `-f`, each re-read and post-check listing with `-C <command directory>` and
  the revalidation's narrowed ref patterns, and, between each re-read listing
  and its branch child, one re-proof child with `-C <command directory>`; the
  record's `operations.estimated` and `operations.performed` are 4,
  its `probes.performed` equals the wrapper's count of the other children, and
  its `probes.estimated` exceeds that of the same run without the flag by 7
- **AND** when a third local branch b3, checked out in no worktree, has b1 as
  its configured upstream (`branch.b3.remote` `.` and `branch.b3.merge`
  `refs/heads/b1`), the same run retires b1 and b2, prints after b1's
  `Retired` line `Note: b3 tracks b1 as its upstream, which now reads gone; no
  commit is lost`, leaves b3 at its SHA, and exits 0
- **AND** when b3, at b1's tip, is instead checked out in a third eligible
  linked worktree P3 that canonical order puts between P1 and P2, P3's
  revalidation compares the ref listing of P1's rescan, read before b1's
  branch stage, and passes, P3 is removed and its `branch_retirement` is
  `retained` with `state-changed`, its re-read finding b3's upstream gone, b3
  stays at its SHA, the result prints the same note after b1's `Retired`
  line, P2 is `not-attempted` with `batch-stopped` and its
  `branch_retirement` `not-attempted` with `branch-retention-stop`, and the
  exit status is 2

#### Scenario: Without the flag every branch remains

- **WHEN** the same repository runs `project clean <root> --all-safe --apply
  --yes`
- **THEN** both worktrees are removed, both branches remain at their planned
  SHAs, the result prints `Removed 2; branches kept: ` with both branches, the
  counting wrapper records no `branch` child and no reflog child, no target
  carries `branch_retirement`, no `selected` entry carries `branch_plan`, and
  the exit status is 0

#### Scenario: A single target with the flag equals a one-item batch

- **WHEN** two fresh copies of a repository in which P is the only eligible
  linked worktree are used in turn at one path, one with `project clean <root>
  --apply --action remove --worktree P --yes --retire-branches` and the other
  with `project clean <root> --all-safe --apply --yes --retire-branches`
- **THEN** both remove P, both run the same branch child argument vector, both
  end with `branch_retirement` `retired` with reason null, and both exit 0
- **AND** run without `--yes` at a terminal, the single-target form asks
  `Remove 1 worktree and retire its local branch? [yes/N]`
- **AND** run without `--yes` on a standard input that is not a terminal,
  each form refuses with `confirmation-required` and exit 2, nothing removed
  and no branch child spawned

#### Scenario: A branch moved after removal is retained and can be retried

- **WHEN** under the flag a test hook resets the first of two targets' branch
  to its parent commit, which is still merged into the merge target, after
  that target's rescan and before its re-read
- **THEN** the first target is `removed` with reason null and its
  `branch_retirement` is `retained` with `branch-changed` and `observed_sha`
  the parent commit, no branch child is spawned, the second target is
  `not-attempted` with `batch-stopped` and its `branch_retirement`
  `not-attempted` with `branch-retention-stop`, and the exit status is 2
- **AND** the result prints the stop block `Stopped at <first path> (branch
  <branch>: branch-changed). Removed 1 of 2. Not attempted: <second path>.
  Next: project clean <root> --all-safe --retire-branches`, then the retained
  branches, then `Removed 1; their branches retired: 0; retained: 1`, then
  `Kept <branch> (branch-changed); now at <parent>; its reflog is not proven
  merged into <merge target>; inspect it and git -C <root> reflog show
  refs/heads/<branch> before retrying: project clean <root> --apply --action
  delete-branch --branch <branch>`, then the residual-window line
- **AND** the printed `delete-branch` command, run with `--yes`, deletes the
  branch and exits 0
- **AND** when the hook instead moves the branch after the removal and before
  the rescan, the target is `removed` with `branch-advanced-after-removal`,
  its `branch_retirement` is `retained` with `branch-changed`, no re-read or
  branch child runs, and the exit status is 2; and when it deletes the branch
  there, the target is `removed` with `branch-missing-after-removal`, its
  `branch_retirement` is `not-attempted` with `branch-missing`, the result
  prints `<branch> was already gone`, and the exit status is 2

#### Scenario: The merge target moves before the branch stage

- **WHEN** under the flag, the main worktree on the merge target, a test hook
  commits to the merge target after the first of two targets' rescan and
  before its re-read
- **THEN** that target's `branch_retirement` is `retained` with
  `state-changed`, its `command` and `exit_status` null, no branch child is
  spawned, the second target is `not-attempted`, and the exit status is 2
- **AND** the same holds when the hook instead recreates by `git fetch` the
  deleted upstream of a target whose plan recorded `upstream_oid` null, edits
  the manifest's `tracking_branch` to name another existing branch, or makes
  the re-read's ref listing fail
- **AND** in each of these cases the result prints `Kept <branch>
  (state-changed); <branch>'s reflog was proven merged into <merge target> only
  at this run's plan; inspect git -C <root> reflog show refs/heads/<branch>
  before retrying: project clean <root> --apply --action delete-branch --branch
  <branch>`, since the re-read stopped before its re-proof, so that the stage
  did not re-prove the reflog

#### Scenario: A branch another worktree holds is retained

- **WHEN** two linked worktrees have one merged branch checked out, the second
  added with `git worktree add --force`, both are eligible, and `--all-safe
  --apply --yes --retire-branches` runs
- **THEN** the plan lists `  remove <first path>; <branch> is decided at
  <second path>` and `  remove <second path> and retire <branch>`, both
  worktrees are removed, the first target's `branch_retirement` is
  `not-attempted` with `branch-shared` and the second's `retired` with reason
  null, one branch child runs, and the exit status is 0
- **AND** run without `--yes` at a terminal, its question reads `Remove 2
  worktrees and retire their 1 local branch? [yes/N]`
- **AND** when a dirty linked worktree also has the branch checked out, the
  plan lists `  remove <second path>; keep <branch> (checked out at <holder
  path>)`, no branch child runs, the second target's `branch_retirement` is
  `not-attempted` with `branch-in-use`, the result prints `Kept <branch>
  (branch-in-use); next: <branch> is checked out at <holder path>; save its
  own work, uncommitted, ignored or flagged assume-unchanged or skip-worktree,
  by keeping that worktree and switching it off <branch> with git -C <holder
  path> switch --detach, which changes none of its files; <branch>'s reflog
  was proven merged into <merge target> only at this run's plan; inspect git
  -C <root> reflog show refs/heads/<branch> before retrying: project clean
  <root> --apply --action delete-branch --branch <branch>`, no line names a
  removal of the holder, the holder and the branch remain, and the exit
  status is 0
- **AND** when instead the main worktree also has the branch checked out, the
  plan lists `  remove <second path>; keep <branch> (checked out at <holder
  path>)`, no branch child runs, the second target's `branch_retirement` is
  `not-attempted` with `branch-in-use`, the result prints `Kept <branch>
  (branch-in-use); next: <branch> is checked out at <holder path>, the main
  worktree; switch it off <branch>, by detaching it with git -C <holder path>
  switch --detach, which changes none of its files, or by checking out <merge
  target> there; <branch>'s reflog was proven merged into <merge target> only
  at this run's plan; inspect git -C <root> reflog show refs/heads/<branch>
  before retrying: project clean <root> --apply --action delete-branch
  --branch <branch>`, the holder and the branch remain, and the exit status
  is 0
- **AND** when the main worktree holds the branch and the branch's upstream
  remote-tracking ref was deleted before the plan, the result prints the same
  `Kept <branch> (branch-in-use); next: <branch> is checked out at <holder
  path>, the main worktree; switch it off <branch>, by detaching it with git
  -C <holder path> switch --detach, which changes none of its files, or by
  checking out <merge target> there; <branch>'s reflog was proven merged into
  <merge target> only at this run's plan; inspect git -C <root> reflog show
  refs/heads/<branch> before retrying: project clean <root> --apply --action
  delete-branch --branch <branch>`, and either step, then the retry, deletes
  the branch with exit 0, where a checkout there of another branch that
  lacks it would leave the retry refused with exit 1
- **AND** when instead a test hook checks the branch out in a new worktree
  after the second removal and before its rescan, the second target's
  `branch_retirement` is `retained` with `branch-in-use`, no branch child
  runs, and the exit status is 2
- **AND** when instead a test hook makes the second worktree dirty after
  confirmation and before its revalidation, the first worktree is removed and
  its `branch_retirement` is `not-attempted` with `branch-shared`, the second
  is `refused` and its `branch_retirement` `not-attempted` with
  `target-not-removed`, no branch child runs, the result prints `Removed 1;
  their branches retired: 0; retained: 1` and then the one line `Kept
  <branch> (branch-shared); next: <branch> is checked out at <second path>;
  save its own work, uncommitted, ignored or flagged assume-unchanged or
  skip-worktree, by keeping that worktree and switching it off <branch> with
  git -C <second path> switch --detach, which changes none of its files;
  <branch>'s reflog was proven merged into <merge target> only at this run's
  plan; inspect git -C <root> reflog show refs/heads/<branch> before
  retrying: project clean <root> --apply --action delete-branch --branch
  <branch>`, the second worktree having been refused for the state it gained,
  and the exit status is 2

#### Scenario: A branch Git would judge against another HEAD is kept

- **WHEN** under the flag the main worktree is on a branch whose head is not
  the merge target's SHA, the merge target being checked out in no worktree,
  and the first of two eligible targets has an upstream whose remote-tracking
  ref was deleted, so that Git's own check would judge its branch against the
  command directory's `HEAD`, while the second's upstream ref is present
- **THEN** the plan lists `  remove <first path>; keep <branch>
  (head-not-merge-target)`, the question counts that branch as kept, both
  worktrees are removed, no branch child runs for the first, its
  `branch_retirement` is `not-attempted` with `head-not-merge-target`, the
  second's branch is retired, and the exit status is 0
- **AND** the result prints `Kept <branch> (head-not-merge-target); next: check
  out <merge target> in the main worktree; <branch>'s reflog was proven merged
  into <merge target> only at this run's plan; inspect git -C <root> reflog
  show refs/heads/<branch> before retrying: project clean <root> --apply
  --action delete-branch --branch <branch>`, and running the checkout and then
  the retry deletes the branch with exit 0
- **AND** when the merge target is instead checked out in a linked worktree at
  <holder path>, so that Git refuses to check it out in the main worktree, the
  result prints `Kept <branch> (head-not-merge-target); next: <merge target> is
  checked out at <holder path>, so check out its tip <merge target SHA>
  detached in the main worktree; <branch>'s reflog was proven merged into
  <merge target> only at this run's plan; inspect git -C <root> reflog show
  refs/heads/<branch> before retrying: project clean <root> --apply --action
  delete-branch --branch <branch>`, and running the checkout and then the
  retry deletes the branch with exit 0
- **AND** with the main worktree on the merge target, the same rows are both
  retired and the exit status is 0

#### Scenario: Git refuses the branch deletion

- **WHEN** under the flag a test `git` that runs the real Git for every other
  command, and whose `branch -d` prints Git's refusal and exits 1 without
  deleting, is first on PATH for the first of two targets whose branches the
  plan retires, the first branch's upstream remote-tracking ref present
- **THEN** the post-check shows the branch present, the target's
  `branch_retirement` is `retained` with `git-refused`, `exit_status: 1` and
  `post_check_sha` equal to its `observed_sha`, no other branch command runs
  for it, the second target is `not-attempted` with
  `batch-stopped` and its `branch_retirement` `not-attempted` with
  `branch-retention-stop`, and the exit status is 2
- **AND** the result prints `Kept <branch> (git-refused); Git refused the
  deletion; if another worktree holds <branch>, a rebase or bisect of it there
  included, wait for any rebase or bisect there to end, and then switch that
  worktree off <branch> by running git switch --detach there, which changes
  none of its files; then retry: project clean <root> --apply --action
  delete-branch --branch <branch>`
- **AND** when instead, with the real Git first on PATH, a test hook starts in
  another worktree, after the first target's rescan and before its re-read, a
  rebase of the first branch that stops at once, so that the registry listing
  shows that worktree detached and the branch at its planned SHA, the re-read's
  checks pass, Git refuses the deletion with exit 1, the target's
  `branch_retirement` is `retained` with `git-refused`, the branch remains,
  the result prints the same line, and the exit status is 2
- **AND** when, with the real Git and that rebase, the first branch's
  upstream remote-tracking ref was instead deleted before the plan and the
  main worktree is on the merge target, so that the plan retires the branch,
  Git refuses the deletion with exit 1, the target's `branch_retirement` is
  `retained` with `git-refused`, the branch remains, the result prints `Kept
  <branch> (git-refused); Git refused the deletion; if another worktree holds
  <branch>, a rebase or bisect of it there included, wait for any rebase or
  bisect there to end, and then switch that worktree off <branch> by running
  git switch --detach there, which changes none of its files; next: check out
  <merge target> in the main worktree, then: project clean <root> --apply
  --action delete-branch --branch <branch>`, and the exit status is 2

#### Scenario: The deadline before the branch stage

- **WHEN** under the flag the removal child of the first of two targets is
  still running when the work deadline passes, then exits 0, and the rescan
  proves it `removed`
- **THEN** no re-read or branch child is spawned, its `branch_retirement` is
  `retained` with `deadline-exceeded`, the second target is `not-attempted`
  with `deadline-exceeded`, and the exit status is 1
- **AND** when the first target's rescan ends with less than 5 s of the work
  deadline left, no re-read or branch child is spawned, its
  `branch_retirement` is `retained` with `deadline-exceeded`, the second
  target is `not-attempted` with `deadline-exceeded`, and the exit status is 1
- **AND** in both cases the result prints `Kept <branch> (deadline-exceeded);
  <branch>'s reflog was proven merged into <merge target> only at this run's
  plan; inspect git -C <root> reflog show refs/heads/<branch> before retrying:
  project clean <root> --apply --action delete-branch --branch <branch>`, since
  no re-proof ran

#### Scenario: A signal around the branch child

- **WHEN** under the flag SIGINT arrives after a target's rescan and before its
  branch child starts
- **THEN** no branch child is spawned, its `branch_retirement` is `retained`
  with `interrupted`, later targets are `not-attempted` with `interrupted`, and
  the exit status is 130
- **AND** when SIGTERM arrives while the branch child of a test `git` whose
  `branch -d` sleeps 2 s before running Git's own is running, that child is
  not signalled and is waited for, the post-check decides its stage, later
  targets are `not-attempted` with `interrupted`, their `branch_retirement`
  `not-attempted` with `target-not-removed` when the target's own is `retired`
  with reason null and with `branch-retention-stop` otherwise, and the exit
  status is 143
- **AND** when SIGINT instead arrives after a target's rescan and before that
  target's re-read starts, no read or child of its stage runs, the branch is
  `retained` with `interrupted`, the result prints `Kept <branch>
  (interrupted); <branch>'s reflog was proven merged into <merge target> only
  at this run's plan; inspect git -C <root> reflog show refs/heads/<branch>
  before retrying: project clean <root> --apply --action delete-branch
  --branch <branch>`, since no re-proof ran, and the exit status is 130

#### Scenario: Exit 0 without retirement

- **WHEN** under the flag a test `git` whose `branch -d` exits 0 without
  deleting the branch is first on PATH
- **THEN** the post-check shows the branch present, its `branch_retirement` is
  `retained` with `unconfirmed-retirement` and `exit_status: 0`, later targets
  are `not-attempted`, and the exit status is 2

#### Scenario: A retirement with a reason

- **WHEN** under the flag a test `git` whose `branch -d` runs Git's own
  deletion and then exits 1 is first on PATH, for the first of two targets
- **THEN** the post-check shows the branch absent, its `branch_retirement` is
  `retired` with `git-failed` and `exit_status: 1`, the second target is
  `not-attempted` and its `branch_retirement` `not-attempted` with
  `branch-retention-stop`, and the exit status is 2
- **AND** the result prints the stop block `Stopped at <first path> (branch
  <branch>: git-failed). Removed 1 of 2. Not attempted: <second path>. Next:
  project clean <root> --all-safe --retire-branches`, then the retained
  branches, the second target's branch among them and never <branch>, then
  `Removed 1; their branches retired: 1; retained: 0`, then `Retired <branch>
  (was <planned_sha>); restore: git -C <root> branch <branch> <planned_sha>`,
  then the residual-window line
- **AND** with a test `git` whose `branch -d` runs Git's own deletion, then
  ignores SIGTERM and never exits, its process group receives SIGTERM when its
  5 s budget ends and SIGKILL 2 s later, the post-check shows the branch
  absent, its `branch_retirement` is `retired` with `probe-timeout`, and the
  exit status is 2

#### Scenario: A branch child that cannot be spawned

- **WHEN** under the flag a test hook after a target's re-proof makes the
  spawn of its branch child fail
- **THEN** no post-check runs, its `branch_retirement` is `retained` with
  `spawn-error`, `command` and `exit_status` null and `probes_performed` 2, the
  branch remains, later targets are `not-attempted`, and the exit status is 2

#### Scenario: A removal past the hard ceiling under the flag

- **WHEN** under the flag a target's removal child is killed at its hard
  ceiling after Git removed the worktree, and the rescan finds its registry
  entry and path gone and its branch present
- **THEN** the target is `removed` with `removal-ceiling`, its
  `branch_retirement` is `retained` with `removal-ceiling`, no re-read or
  branch child runs, the branch remains, later targets are `not-attempted`,
  and the exit status is 1
- **AND** the result prints `Kept <branch> (removal-ceiling); <branch>'s reflog
  was proven merged into <merge target> only at this run's plan; inspect git -C
  <root> reflog show refs/heads/<branch> before retrying: project clean <root>
  --apply --action delete-branch --branch <branch>`, since no stage ran

#### Scenario: A removal that does not end removed under the flag

- **WHEN** under the flag a lock is added to the first of two targets after its
  revalidation, so that Git refuses its removal
- **THEN** the first target is `failed` with `git-refused` and its
  `branch_retirement` is `not-attempted` with `target-not-removed`, no branch
  command runs, the second target is `not-attempted` with `batch-stopped` and
  its `branch_retirement` `not-attempted` with `target-not-removed`, both
  branches remain, and the exit status is 128
- **AND** when a test hook instead deletes the first target's branch after its
  rescan and before its re-read, the first target is `removed` with reason
  null, its `branch_retirement` is `not-attempted` with `branch-missing` and
  `observed_sha` null, no branch child is spawned, the second target's
  `branch_retirement` is `not-attempted` with `branch-retention-stop`, and the
  exit status is 2

#### Scenario: A branch child past its budget

- **WHEN** under the flag a test `git` whose `branch -d` ignores SIGTERM and
  never exits is first on PATH
- **THEN** its process group receives SIGTERM when its 5 s budget ends and
  SIGKILL 2 s later, the post-check decides its stage, `retained` with
  `probe-timeout` while the branch is present, later targets are
  `not-attempted`, the exit status is 2, and the run ends within 64 s of its
  start

#### Scenario: A post-check that cannot decide

- **WHEN** under the flag a target's post-check listing fails after its branch
  child, the real Git's, exits 0, for the first of two targets
- **THEN** its `branch_retirement` has `stage: null`, reason
  `reconciliation-incomplete` and `post_check_sha` null, the result's
  `completeness` is incomplete,
  later targets are `not-attempted`, and the exit status is 1
- **AND** the result prints `Removed 1; their branches retired: 0; retained:
  0; unconfirmed: 1`, then `Unconfirmed <branch> (was <planned_sha>); if git
  -C <root> rev-parse --verify refs/heads/<branch> fails, restore: git -C
  <root> branch <branch> <planned_sha>; otherwise retry: project clean <root>
  --apply --action delete-branch --branch <branch>`, prints no `Kept` line for
  it, and does not name it among the retained branches
- **AND** when instead a test hook raises an exception after that branch child
  exits 0 and before its post-check decides, the target stays `removed` with
  reason null, its `branch_retirement` has `stage: null` with
  `reconciliation-incomplete`, never `not-attempted` with
  `target-not-removed`, and the result and the exit status are the same; when
  the hook raises it once the post-check has shown the branch absent, the
  `branch_retirement` is `retired` with `internal-error`, the result prints
  `Retired <branch> (was <planned_sha>); restore: git -C <root> branch <branch>
  <planned_sha>`, and the exit status is 2; and when it raises it during the
  re-read, before or while its re-proof runs, no branch child is spawned, the
  `branch_retirement` is `retained` with `internal-error`, the branch
  remains, the result prints `Kept <branch> (internal-error); <branch>'s reflog
  was proven merged into <merge target> only at this run's plan; inspect git -C
  <root> reflog show refs/heads/<branch> before retrying: project clean <root>
  --apply --action delete-branch --branch <branch>`, and the exit status is 2

#### Scenario: A branch whose reflog holds amended-away work keeps it

- **WHEN** under the flag an eligible branch b1's first commit was amended
  before it merged, so that the draft commit is named only by b1's reflog,
  beside a second eligible branch b2 with a plain history
- **THEN** the repository's reflog child prints a commit and one more child per
  row runs, the plan lists `  remove <P1>; keep b1 (reflog-unmerged)`, P1 is
  removed, b1 and its reflog remain, its `branch_retirement` is
  `not-attempted` with `reflog-unmerged`, P2 is removed and b2 retired, the
  draft is still reachable from b1's reflog, and the exit status is 0
- **AND** the result prints `Kept b1 (reflog-unmerged); its reflog is not
  proven merged into <merge target>; inspect every commit it names, the old
  and the new of each entry, as cat <common dir>/logs/refs/heads/b1 prints
  them, before any delete-branch`, `<common dir>` being the plan's
  `repository.common_dir`
- **AND** the counting `git` wrapper records each reflog child's standard input
  as the named commits, one per line, then one line `^<merge target SHA>`, and
  no `--not` on standard input
- **AND** when a test `git` makes the repository's reflog child exit nonzero,
  both branches are kept with `reflog-unmerged`, the plan stays complete and a
  flagged preview exits 0, both worktrees are removed, and the exit status is 0
- **AND** when a test `git` makes the repository's reflog child hang past its
  5 s budget, it is stopped, both branches are kept with `reflog-unmerged`, the
  plan stays complete, both worktrees are removed, and the exit status is 0
- **AND** when a test `git` makes the repository's reflog child block, and it
  starts with less than 5 s of the work deadline left, so that the deadline
  passes while it runs, the plan is incomplete with `deadline-exceeded`, a
  flagged preview exits 1, and `--apply` refuses with exit 2 before any
  question or mutation
- **AND** when `git reflog expire` has left of an eligible branch b3's reflog
  only a reset entry whose old object is a commit the merge target lacks, so
  that the commit is named only as that entry's old object, b3 is kept with
  `reflog-unmerged` too and the commit stays reachable from b3's reflog, and
  the `cat` command of b3's `Kept` line prints that commit as the entry's old
  commit, where `git reflog show refs/heads/b3` prints no entry that names it

#### Scenario: A commit the reflog names only as an old one is shown

- **WHEN** under the flag an eligible linked worktree P3's branch b3 once held
  a commit U that the merge target lacks, made more than 30 days ago and reset
  away since, and a default `git gc` has expired the entry that U's commit
  wrote, so that b3's reflog names U only as the old object of the reset
  entry, `git reflog show refs/heads/b3` printing no entry that names it, and
  `--all-safe --apply --yes --retire-branches` runs
- **THEN** b3 passes the `unstarted-branch` gate, its anchor being the
  creation entry and its commit entry a movement, the plan's proof prints U,
  the plan lists `  remove <P3>; keep b3 (reflog-unmerged)`, P3 is removed, b3
  and its reflog remain, U is still reachable from that reflog, and the exit
  status is 0
- **AND** the result prints `Kept b3 (reflog-unmerged); its reflog is not
  proven merged into <merge target>; inspect every commit it names, the old
  and the new of each entry, as cat <common dir>/logs/refs/heads/b3 prints
  them, before any delete-branch`, `<common dir>` being the plan's
  `repository.common_dir`, and that command, run from another directory,
  prints U as the reset entry's old commit

#### Scenario: A holder's own work is kept by its next step

- **WHEN** under the flag an eligible linked worktree P on a merged, published
  branch b, its upstream's remote-tracking ref present, sits beside a linked
  holder H of b, added with `git worktree add --force`, that the plan excludes
  for local state of its own, the main worktree on the merge target, and
  `--all-safe --apply --yes --retire-branches` runs, in turn with H holding an
  edit to a tracked file and an untracked file, so that it is `dirty`, an edit
  to a file flagged assume-unchanged, an edit to a file flagged skip-worktree,
  each `hidden-local-state`, and an ignored file, so that it is
  `ignored-local-files`
- **THEN** in each case the plan lists `  remove <P>; keep b (checked out at
  <H>)`, P is removed, no branch child runs, P's `branch_retirement` is
  `not-attempted` with `branch-in-use`, and the exit status is 0
- **AND** the result prints `Kept b (branch-in-use); next: b is checked out at
  <H>; save its own work, uncommitted, ignored or flagged assume-unchanged or
  skip-worktree, by keeping that worktree and switching it off b with git -C
  <H> switch --detach, which changes none of its files; b's reflog was proven
  merged into <merge target> only at this run's plan; inspect git -C <root>
  reflog show refs/heads/b before retrying: project clean <root> --apply
  --action delete-branch --branch b`, and no line names a removal of H
- **AND** the printed switch, run as printed, exits 0 and leaves H's edits,
  their index flags, its untracked file and its ignored file as they were, and
  the printed retry, run with `--yes`, then deletes b and exits 0, H remaining
- **AND** when instead b's upstream remote-tracking ref was deleted before the
  plan and the main worktree is on a branch that lacks b, the merge target
  checked out in no worktree, the plan still keeps b with `branch-in-use`, the
  result prints `Kept b (branch-in-use); next: b is checked out at <H>; save
  its own work, uncommitted, ignored or flagged assume-unchanged or
  skip-worktree, by keeping that worktree and switching it off b with git -C
  <H> switch --detach, which changes none of its files; then check out <merge
  target> in the main worktree; b's reflog was proven merged into <merge
  target> only at this run's plan; inspect git -C <root> reflog show
  refs/heads/b before retrying: project clean <root> --apply --action
  delete-branch --branch b`, and following its steps in order deletes b with
  exit 0, where the retry without the checkout is refused with exit 1
- **AND** when instead H's directory is moved away before the plan, as an
  unmounted drive leaves it, so that its row is `stale-worktree` with
  `present: false`, the plan still keeps b with `branch-in-use`, P is
  removed, no branch child runs, the result prints `Kept b (branch-in-use);
  next: b is checked out at <H>, whose path is missing; if that worktree
  still exists, moved or on a drive that is not mounted, remount or repair it
  and switch it off b by running git switch --detach there, which changes
  none of its files; otherwise review and prune stale worktree metadata
  manually; git worktree prune also deletes the entry, and so the HEAD
  reflog, of every other worktree whose path is missing, one moved or on an
  unmounted drive included, so run git worktree prune --dry-run first and
  remount or repair any it lists that still exists; b's reflog was proven
  merged into <merge target> only at this run's plan; inspect git -C <root>
  reflog show refs/heads/b before retrying: project clean <root> --apply
  --action delete-branch --branch b`, H's administrative directory remains,
  and the exit status is 0; once H's directory is moved back, the switch run
  there exits 0 and leaves H's files and their index flags as they were, and
  the printed retry, run with `--yes`, deletes b and exits 0
- **AND** when instead H's administrative `gitdir` file names the main
  worktree's `.git`, so that the registry listing gives H the main
  worktree's path, and `project clean <root> --apply --action remove
  --worktree P --yes --retire-branches` names P, the plan excludes H as
  `registration-mismatch` and keeps b with `branch-in-use`, P is removed, no
  branch child runs, the result prints `Kept b (branch-in-use); next: b is
  checked out at <root>; its path is or holds the main worktree, the common
  directory or another worktree, so do not delete it by hand or with git
  worktree remove; review its registration with git worktree list
  --porcelain; once it is repaired, switch that worktree off b by running git
  switch --detach there, which changes none of its files; b's reflog was
  proven merged into <merge target> only at this run's plan; inspect git -C
  <root> reflog show refs/heads/b before retrying: project clean <root>
  --apply --action delete-branch --branch b`, the main worktree stays on the
  merge target, and the exit status is 0; once `git worktree repair <H>` has
  repaired H's registration, the switch run in H exits 0 and leaves its files
  as they were, and the printed retry, run with `--yes`, deletes b and
  exits 0

#### Scenario: A holder whose path cannot be read is not to be removed

- **WHEN** under the flag `project clean <root> --apply --action remove
  --worktree P --yes --retire-branches` names an eligible P on a merged,
  published branch b while a linked holder H of b, added with `git worktree
  add --force`, sits in a directory that denies search permission
- **THEN** the plan records H as a non-blocking omission, `inspection-error`
  with `present: null`, and keeps b with `branch-in-use`, the registry listing
  still naming H's branch, P is removed, no branch child runs, and the exit
  status is 0
- **AND** the result prints `Kept b (branch-in-use); next: b is checked out at
  <H>; its path could not be read, so do not run git worktree prune, git
  worktree remove or git gc until it can; once it can, save its own work,
  uncommitted, ignored or flagged assume-unchanged or skip-worktree, by keeping
  that worktree and switching it off b with git -C <H> switch --detach, which
  changes none of its files; b's reflog was proven merged into <merge target>
  only at this run's plan; inspect git -C <root> reflog show refs/heads/b
  before retrying: project clean <root> --apply --action delete-branch
  --branch b`, and H's administrative directory remains
- **AND** once search permission is restored, the printed switch exits 0 and
  the printed retry, run with `--yes`, deletes b and exits 0

#### Scenario: A clean holder the plan would remove

- **WHEN** under the flag three eligible linked worktrees P1, P2 and P3, in
  canonical order, are selected, P1 and P3 holding one merged, published
  branch b, P3 added with `git worktree add --force`, and P2 holding a branch
  c, and a test hook makes P2 dirty after confirmation and before its
  revalidation while `--all-safe --apply --yes --retire-branches` runs
- **THEN** P1 is removed and its `branch_retirement` is `not-attempted` with
  `branch-shared`, P2 is `refused` with `state-changed`, P3 is `not-attempted`
  with `batch-stopped`, no branch child runs, and the exit status is 2
- **AND** the result prints `Kept b (branch-shared); next: b is checked out at
  <P3>, which this run selected and did not reach; remove it and retire b with
  project clean <root> --apply --action remove --worktree <P3>
  --retire-branches`, P3 being a holder that the plan read and selected and
  the run did not reach, and that command, run then with `--yes`, removes P3
  and retires b, and exits 0
- **AND** when the test hook also makes, in P3, a commit on a detached `HEAD`
  and then checks b out there again, so that only P3's HEAD reflog holds that
  commit, the result prints the same line, and the printed command, run with
  `--yes`, refuses with `target-excluded`, reason `worktree-only-commits`, and
  exit 2, P3, b and that commit remaining, where `git worktree remove <P3>`
  would exit 0 and leave that commit unreachable
- **AND** when instead `project clean <root> --apply --action remove --worktree
  P1 --yes --retire-branches` names P1 alone, P3 is `not-requested`, a gate
  before the index gates, so that the plan never read P3's index, the plan
  keeps b with `branch-in-use`, and the result prints `Kept b (branch-in-use);
  next: b is checked out at <P3>; save its own work, uncommitted, ignored or
  flagged assume-unchanged or skip-worktree, by keeping that worktree and
  switching it off b with git -C <P3> switch --detach, which changes none of
  its files; b's reflog was proven merged into <merge target> only at this
  run's plan; inspect git -C <root> reflog show refs/heads/b before retrying:
  project clean <root> --apply --action delete-branch --branch b`

#### Scenario: A branch moved to an unmerged commit and back is retained

- **WHEN** under the flag, after the plan is printed and before the first of
  two targets' revalidation, a test hook commits on that target's branch, in
  its worktree, a commit the merge target lacks and then resets the branch to
  its planned SHA with `git reset --hard`, so that its head, upstream
  evidence, merge target and worktree all match the plan while its reflog
  names the new commit
- **THEN** the first target is `removed` with reason null, its re-read's checks
  pass, its re-proof prints the new commit, no branch child is spawned, its
  `branch_retirement` is `retained` with `reflog-unmerged`, `observed_sha`
  equal to `planned_sha`, `command` and `exit_status` null and
  `probes_performed` 2, the branch and its reflog remain and the new commit is
  still reachable from that reflog, the second target is `not-attempted` with
  `batch-stopped` and its `branch_retirement` `not-attempted` with
  `branch-retention-stop`, and the exit status is 2
- **AND** the result prints the stop block `Stopped at <first path> (branch
  <branch>: reflog-unmerged). Removed 1 of 2. Not attempted: <second path>.
  Next: project clean <root> --all-safe --retire-branches`, then the retained
  branches, then `Removed 1; their branches retired: 0; retained: 1`, then
  `Kept <branch> (reflog-unmerged); its reflog is not proven merged into
  <merge target>; inspect every commit it names, the old and the new of each
  entry, as cat <common dir>/logs/refs/heads/<branch> prints them, before any
  delete-branch`, then the residual-window line
- **AND** the counting `git` wrapper records the re-proof's standard input as
  the commits the reflog then names, the new commit among them, one per line,
  then one line `^<merge target SHA>`
- **AND** the outcome is the same when a test hook instead moves the branch by
  `git update-ref` to such a commit and back after the first target's rescan
  and before its re-read
- **AND** when a test `git` instead makes only that re-proof exit nonzero, or
  hang past its 5 s budget, with nothing moved, the branch is `retained` with
  `state-changed`, no branch child is spawned, the result prints `Kept
  <branch> (state-changed); <branch>'s reflog was proven merged into <merge
  target> only at this run's plan; inspect git -C <root> reflog show
  refs/heads/<branch> before retrying: project clean <root> --apply --action
  delete-branch --branch <branch>`, and the exit status is 2
- **AND** when that re-proof hangs instead, with nothing moved, and starts with
  less than 5 s of the work deadline left above the removal floor, so that its
  budget ends when only the removal floor remains, it is stopped there, no
  branch child is spawned,
  the branch is `retained` with `deadline-exceeded`, the result prints `Kept
  <branch> (deadline-exceeded); <branch>'s reflog was proven merged into <merge
  target> only at this run's plan; inspect git -C <root> reflog show
  refs/heads/<branch> before retrying: project clean <root> --apply --action
  delete-branch --branch <branch>`, and the exit status is 1; and when a test
  `git` instead delays that re-proof by 2 s, with nothing moved, and SIGINT
  arrives while it runs, it is not signalled and runs to its end, printing
  nothing, no branch child is spawned, the branch is `retained` with
  `interrupted`, the result prints `Kept <branch> (interrupted); retry: project
  clean <root> --apply --action delete-branch --branch <branch>`, with no advice
  to inspect the reflog, since that re-proof proved the reflog merged, the
  second target is `not-attempted` with `interrupted` and its
  `branch_retirement` `not-attempted` with `branch-retention-stop`, and the
  exit status is 130

#### Scenario: A flagged run's next commands keep the flag

- **WHEN** under the flag twenty rows pass every gate before
  `deferred-target-cap`, none of them holding a submodule or hidden local
  state, and `--all-safe --apply --yes --retire-branches` runs
- **THEN** sixteen worktrees are removed and their branches retired, the
  deferral line reads `run again: project clean <root> --all-safe --apply
  --retire-branches`, and the exit status is 0
- **AND** running the printed command removes the other four and retires their
  branches

#### Scenario: The flag's argument rules

- **WHEN** `--retire-branches` is given to plain `project clean`, to `--action
  remove --worktree P` without `--apply`, or with `--apply --action push` or
  `--apply --action delete-branch`
- **THEN** the command refuses with `invalid-arguments` and exit 2, and runs
  nothing
- **AND** `project clean <root> --all-safe --apply --yes --json
  --retire-branches` prints exactly one JSON document on standard output, the
  apply result record, whose every target carries `branch_retirement`, with
  the human plan and progress on standard error, and `--apply --action remove
  --worktree P --yes --json --retire-branches` does the same for P
- **AND** `project clean <root> --all-safe --json --retire-branches` prints the
  plan envelope, whose every `selected` entry carries `branch_plan` and which
  has no key that the envelope without the flag lacks

#### Scenario: The question names the branches to retire

- **WHEN** `--all-safe --apply --retire-branches` asks its question at a
  terminal for two selected rows whose branches the plan retires
- **THEN** the plan lists `  remove <P1> and retire <b1>` and `  remove <P2>
  and retire <b2>`, the question reads `Remove 2 worktrees and retire their 2
  local branches? [yes/N]`, and the answer `y` refuses with `cancelled` and
  exit 2, nothing removed or deleted
- **AND** when the plan keeps one of the two branches, the question reads
  `Remove 2 worktrees, retire 1 local branch and keep 1? [yes/N]`

#### Scenario: A flagless digest does not bind a flagged apply

- **WHEN** a preview `project clean <root> --all-safe` prints digest D, and
  `project clean <root> --all-safe --apply --yes --expect-plan D
  --retire-branches` runs with nothing changed
- **THEN** the fresh plan is printed with a different digest, the run refuses
  with `plan-digest-mismatch` and exit 2 before any question or mutation, and
  every worktree and branch remains
- **AND** the same holds for the digest that plain `project clean <root>`
  prints

#### Scenario: A flagged preview's digest binds the flagged apply

- **WHEN** `project clean <root> --all-safe --retire-branches` previews two
  rows, printing `  remove <P1> and retire <b1>`, `  remove <P2> and retire
  <b2>` and digest D, and `project clean <root> --all-safe --apply --yes
  --expect-plan D --retire-branches` runs with nothing changed
- **THEN** the fresh digest equals D, the apply proceeds, both worktrees are
  removed and both branches retired, and the exit status is 0
- **AND** `project clean <root> --all-safe --apply --yes --expect-plan D`,
  without the flag, refuses with `plan-digest-mismatch` and exit 2
- **AND** when the plan's decision for a branch changes between the preview and
  the apply, as when the main worktree leaves the merge target before a row
  whose upstream ref is absent is planned, the fresh digest differs from D and
  the flagged apply refuses with `plan-digest-mismatch` and exit 2

#### Scenario: A branch name in a printed command is quoted for the shell

- **WHEN** under the flag an eligible branch is named `topic;id`, a name Git
  accepts, the repository's root path holds a space, and `project clean <root>
  --all-safe --apply --yes --retire-branches` runs
- **THEN** the branch is retired, and the result prints `Retired topic;id (was
  <sha>); restore: git -C '<root>' branch 'topic;id' <sha>`, the name verbatim
  in prose and single-quoted in the command
- **AND** that restore line, run by a POSIX shell from another directory,
  recreates `topic;id` at `<sha>` in the repository and runs nothing else
- **AND** when instead a test `git` whose `branch -d` refuses with exit 1 is
  first on PATH, the branch's upstream remote-tracking ref present, the result
  prints `Kept topic;id (git-refused); Git refused the deletion; if another
  worktree holds topic;id, a rebase or bisect of it there included, wait for
  any rebase or bisect there to end, and then switch that worktree off
  topic;id by running git switch --detach there, which changes none of its
  files; then retry: project clean '<root>' --apply --action delete-branch
  --branch 'topic;id'`
- **AND** when instead the branch's reflog names a commit the merge target
  lacks, the result prints `Kept topic;id (reflog-unmerged); its reflog is not
  proven merged into <merge target>; inspect every commit it names, the old
  and the new of each entry, as cat '<common dir>/logs/refs/heads/topic;id'
  prints them, before any delete-branch`, the plan's common directory holding
  the root's space, and when instead a test
  hook resets the branch to its parent commit, which is still merged, after
  its rescan and before its re-read, `Kept topic;id (branch-changed); now at
  <parent>; its reflog is not proven merged into <merge target>; inspect it
  and git -C '<root>' reflog show 'refs/heads/topic;id' before retrying:
  project clean '<root>' --apply --action delete-branch --branch 'topic;id'`
- **AND** for an eligible branch written by hand as `refs/heads/-f` and checked
  out in its worktree by `git symbolic-ref`, the result prints `Retired -f (was
  <sha>); restore: git -C '<root>' update-ref refs/heads/-f <sha> ''`, which
  run by a POSIX shell recreates the ref, and with the refusing test `git` the
  retry it prints passes `--branch=-f`; and where one is instead written by
  hand as `refs/heads/HEAD` the same way, a name that `git branch HEAD <sha>`
  refuses to create, no run retires it under either setting of
  `core.warnAmbiguousRefs`: under Git's default every status probe of the
  repository exits 0 and warns `refname 'HEAD' is ambiguous.` and every row
  is `inspection-error`, and with the setting false in the repository's
  configuration the row of the worktree on `refs/heads/HEAD` is
  `inspection-error`; in both the plan is incomplete, and the run removes no
  worktree and prints no `Retired HEAD` line
- **AND** for an eligible branch whose name is `topic`, U+202E and `x`, a name
  Git accepts that holds a code point to escape, the result prints `Retired
  $'topic\u202ex' (was <sha>); restore: git -C '<root>' branch $'topic\u202ex'
  <sha>`, the name in the `$'...'` form in prose and command alike, and that
  restore line, run by bash in a UTF-8 locale from another directory,
  recreates the branch at `<sha>`
