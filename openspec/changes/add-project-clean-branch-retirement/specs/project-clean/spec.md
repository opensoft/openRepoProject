## MODIFIED Requirements

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
with reason null, the sequence SHALL then retire the target's branch as "Clean
retires a removed worktree's branch only on fresh head and ancestry evidence"
states, before any later target is revalidated. Removal SHALL stop after the
first target whose result is not a plain `removed`, or, under
`--retire-branches`, whose `branch_retirement` is not `retired` with reason
null, with no continuation, rollback or automatic retry.

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
an excluded row leaves it unchanged. `--expect-plan D` SHALL refuse with
`plan-digest-mismatch` and exit status 2, before any question and any mutation,
when the fresh digest differs from D, and SHALL still print the fresh plan. The
confirmation SHALL be one default-No question naming the count of worktrees to
remove and of branches kept, or, under `--retire-branches`, of branches to
retire, ending `[yes/N]`; only `yes`, surrounding
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
summary line that "Clean retires a removed worktree's branch only on fresh head
and ancestry evidence" states.

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
before the apply phase SHALL refuse with `internal-error` and exit status 2. No
`unknown` or `failed` target SHALL be retried automatically, and `project` SHALL
never force a removal or delete a directory itself.

The exit status of a run with `--apply` SHALL be the first row that matches:

1. 130, 143 or 129: a signal was received, the first one received deciding, or
   input ended at the question (130);
2. 1: the deadline stopped work after the apply phase began, any target is
   `unknown`, any target's reason is `removal-ceiling`, or, under
   `--retire-branches`, any target's `branch_retirement` has a null `stage`;
3. Git's own status, passed through unchanged: a target is `failed` with
   `git-refused` or `git-failed`;
4. 2: any refusal; a `refused` target; a `removed` target with a
   branch-after-removal reason; a `failed` target with `spawn-error`; under
   `--retire-branches`, a target `removed` with reason null whose
   `branch_retirement` is not `retired` with reason null;
5. 0: every selected target is `removed` with reason null and, under
   `--retire-branches`, its `branch_retirement` is `retired` with reason null;
   or nothing is eligible.

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

### Requirement: Clean retires a removed worktree's branch only on fresh head and ancestry evidence

`project clean` SHALL accept `--retire-branches` only with `--apply` and either
`--all-safe` or `--action remove --worktree P`. With any other combination, a
preview, `--action push` and `--action delete-branch` among them, it SHALL
refuse with `invalid-arguments` and exit status 2 before any plan is built, and
SHALL run nothing. The flag SHALL never be the default: without it every
branch remains, as "Clean can explicitly retire verified worktrees" states, and
the record below SHALL be absent from every target, never null, because null
means unknown or not established. `--apply --json` SHALL be accepted with the
flag exactly where "Clean plans and refusals are versioned JSON" accepts it
without the flag. The flag SHALL change no gate, no selection, no `plan_digest`
and no `--expect-plan` comparison.

Under the flag, and only for a target whose rescan proves it `removed` with
reason null, the run SHALL retire the target's local branch in a branch stage
that follows that rescan and precedes any later target's revalidation, in this
order:

1. Re-read, while work remains, the manifest by a filesystem read and the
   branch with one ref listing in the command directory, narrowed as the
   revalidation's ref listing is, each under `min(5 s, work remaining)`.
2. Check, stopping at the first check that fails: the branch exists; its head
   equals the reconciliation record's `branch_sha`; the merge target,
   re-resolved from that manifest read and that listing, has the plan's
   `name`, `source` and `sha`, so that the plan's proof that the head is an
   ancestor of the merge target is the ancestry at the target's current tip,
   and no Git child computes it again; and no registered worktree, the main
   worktree included, has the branch checked out in the registry listing of
   that rescan. A value the re-read cannot establish, a read that fails or
   times out included, SHALL count as a difference.
3. Spawn, while work remains, the non-force command `git -c
   protocol.allow=never -c protocol.file.allow=never -c
   protocol.ssh.allow=never -c protocol.git.allow=never -c
   protocol.http.allow=never -c protocol.https.allow=never -c
   protocol.ext.allow=never -C <command directory> branch -d -- <branch>`, in
   its own process group, with the seventeen variables that "Repository
   inspection requires Git 2.36 and shares one evidence model" lists removed
   from its environment, under `min(5 s, work remaining)`. The branch child
   SHALL NOT be signalled on SIGINT, SIGTERM or SIGHUP, and SHALL be waited for
   within that budget; past it, its process group SHALL receive SIGTERM and,
   2 s later, SIGKILL, and its reap SHALL wait at most a further 2 s.
4. Re-read the branch with one more such listing, under `min(5 s, reserve
   remaining)`, and decide the stage by that post-check. The branch child's
   exit status alone SHALL never prove a retirement.

A signal received before the re-read or the branch child starts SHALL start
neither, and neither SHALL be spawned when no work remains. The stage SHALL
never pass `-D`, `--force` or `-f`, never spawn a second branch child for a
target, never retry, and never delete, push or fetch a remote branch or change
a remote-tracking ref. Git's own refusal SHALL retain the branch.

Under the flag every target of the apply result record SHALL carry
`branch_retirement`, an object `{stage, reason, branch, planned_sha,
observed_sha, command, exit_status}`: `branch` and `planned_sha` are the
target's; `observed_sha` is the head the re-read found, null when it found none
or did not run; `command` is the branch child's argument vector, null when none
was spawned; and `exit_status` is its exit status, null when none was spawned
or its exit could not be observed. `stage` SHALL be one of these, with one
reason:

- `retired`: the post-check shows the branch absent after its branch child
  ran; reason null when the child exited 0, `git-failed` when it exited
  nonzero, and `probe-timeout` or `deadline-exceeded` when `project` stopped it
  past its budget, the latter when the work deadline was the limit;
- `retained`: the target is `removed` and its branch is present when the stage
  ends; `branch-changed` (the re-read found another head, or the target is
  `removed` with `branch-advanced-after-removal` and no stage ran),
  `state-changed` (the merge target differs from the plan, or the re-read
  could not establish a value), `branch-in-use`, `deadline-exceeded` (the work
  deadline left no time to start, or stopped, the re-read or the branch child),
  `interrupted`, `spawn-error`, `git-refused` (the child exited nonzero),
  `unconfirmed-retirement` (the child exited 0), `probe-timeout`, or
  `removal-ceiling` (the target's own reason, no stage having run);
- `not-attempted`: no branch remained to retire, or no stage ran for the
  target; `branch-missing` (the rescan or the re-read found no branch, the
  target `removed` with `branch-missing-after-removal` included),
  `branch-retention-stop` (the target is `not-attempted` because the run
  stopped after an earlier target that was `removed` and whose
  `branch_retirement` was not `retired` with reason null), or
  `target-not-removed` (every other target that no stage reached: one that is
  `refused`, `failed` or `unknown`, or `not-attempted` for any other cause, a
  signal or the deadline after an earlier plain retirement included);
- null, with reason `reconciliation-incomplete`, only when the post-check
  failed or timed out, so that whether the branch exists is not established.

The target's `reconciliation` SHALL remain the rescan that decided its removal;
the branch stage's evidence SHALL be in `branch_retirement` alone. A null
`stage` SHALL make the apply result's `completeness` incomplete. The record
SHALL add no value to the target's `stage` or `reason` enums, to the ladder, to
the gates, or to the refusal and note codes.

Removal SHALL stop after the first target that is `removed` and whose
`branch_retirement` is not `retired` with reason null, as it stops after the
first target that is not a plain `removed`. Every target after it SHALL be
`not-attempted` with reason `batch-stopped`, or `interrupted` or
`deadline-exceeded` where a signal or the deadline stopped the run, and SHALL
carry `branch_retirement` `not-attempted` with reason `branch-retention-stop`.
The exit status SHALL be the one that "Clean records a reconcilable result for
every removal target" orders: a retained branch exits 2 unless a signal, the
deadline or a null `stage` decides first.

The re-read and the post-check SHALL be counted under `probes` and in the
target's `probes_performed`, and the branch child under `operations`, so that
under the flag `operations.estimated` SHALL add one per selected target and
`probes.estimated` two per selected target. The stage SHALL spawn at most three
Git children per target, one of them a branch child, so that `limits.targets`
caps the branch children of a run and `budget.probe_timeout_seconds` bounds
each; no `limits` or `budget` member is added. A run with no removal in flight
SHALL still end within 64 s of its start, not counting the time blocked at the
confirmation question.

Under the flag the printed plan SHALL mark each selected row's branch as one to
retire. The confirmation SHALL be the one default-No question that "Clean
previews and applies a batch of eligible worktree removals in one repository"
states, reading `Remove N worktrees and retire their M local branches?
[yes/N]`, M being the number of distinct branches of the selected rows and
`branch` singular when M is 1, or `Remove 1 worktree and retire its local
branch? [yes/N]` for one.
Every apply result SHALL print `Removed N; branches retired: R; retained: K`,
then each retained branch with the command `project clean <root> --apply
--action delete-branch --branch <branch>`, the explicit retry path, whose
behaviour this requirement does not change. A run that stops SHALL then end
with the stop block that "Clean records a reconcilable result for every removal
target" states, whose reason, when a branch stage stopped the run, SHALL be
that stage's reason with the branch named.

#### Scenario: Retire the branches of a batch

- **WHEN** two eligible linked worktrees P1 and P2, each merged, clean and
  published with a commit of its own, P1's upstream's remote-tracking ref
  present and P2's deleted, sit beside the main worktree on the merge target,
  and `project clean <root> --all-safe --apply --yes --retire-branches` runs
- **THEN** P1 is removed and its branch then deleted, then P2 the same, in
  canonical path order, each target `removed` with reason null and its
  `branch_retirement` `retired` with reason null, `observed_sha` equal to
  `planned_sha` and `exit_status` 0
- **AND** P1's remote branch and its remote-tracking ref remain, nothing is
  fetched or pushed, the result prints `Removed 2; branches retired: 2;
  retained: 0`, and the exit status is 0
- **AND** a counting `git` wrapper on PATH records each branch child with `-c
  protocol.allow=never`, the six per-protocol pins, `-C <command directory>`
  and `branch -d -- <branch>`, and none with `-D`, `--force` or `-f`; the
  record's `operations.performed` is 4 and its `probes.performed` equals the
  wrapper's count of the other children

#### Scenario: Without the flag every branch remains

- **WHEN** the same repository runs `project clean <root> --all-safe --apply
  --yes`
- **THEN** both worktrees are removed, both branches remain at their planned
  SHAs, the result prints `Removed 2; branches kept: ` with both branches, the
  counting wrapper records no `branch` child, no target carries
  `branch_retirement`, and the exit status is 0

#### Scenario: A single target with the flag equals a one-item batch

- **WHEN** two fresh copies of a repository in which P is the only eligible
  linked worktree are used in turn at one path, one with `project clean <root>
  --apply --action remove --worktree P --yes --retire-branches` and the other
  with `project clean <root> --all-safe --apply --yes --retire-branches`
- **THEN** both remove P, both run the same branch child argument vector, both
  end with `branch_retirement` `retired` with reason null, and both exit 0

#### Scenario: A branch moved after removal is retained and can be retried

- **WHEN** under the flag a test hook resets the first of two targets' branch
  to its parent commit, which is still merged into the merge target, after
  that target's rescan and before its re-read
- **THEN** the first target is `removed` with reason null and its
  `branch_retirement` is `retained` with `branch-changed` and `observed_sha`
  the parent commit, no branch child is spawned, the second target is
  `not-attempted` with `batch-stopped` and its `branch_retirement`
  `not-attempted` with `branch-retention-stop`, and the exit status is 2
- **AND** the result names the surviving branch with `project clean <root>
  --apply --action delete-branch --branch <branch>`, and that command run with
  `--yes` deletes the branch and exits 0
- **AND** the result prints `Removed 1; branches retired: 0; retained: 1`
  before the stop block
- **AND** when the hook instead moves the branch after the removal and before
  the rescan, the target is `removed` with `branch-advanced-after-removal`,
  its `branch_retirement` is `retained` with `branch-changed`, no re-read or
  branch child runs, and the exit status is 2

#### Scenario: The merge target moves before the branch stage

- **WHEN** under the flag a test hook commits to the merge target after the
  first of two targets' rescan and before its re-read
- **THEN** that target's `branch_retirement` is `retained` with
  `state-changed`, no branch child is spawned, the second target is
  `not-attempted`, and the exit status is 2

#### Scenario: A branch another worktree holds is retained

- **WHEN** two linked worktrees have one merged branch checked out, the second
  added with `git worktree add --force`, both are eligible, and `--all-safe
  --apply --yes --retire-branches` runs
- **THEN** the first in canonical order is removed and its
  `branch_retirement` is `retained` with `branch-in-use`, no branch child is
  spawned, the second is `not-attempted`, the branch and the second worktree
  remain, and the exit status is 2
- **AND** run without `--yes` at a terminal, its question reads `Remove 2
  worktrees and retire their 1 local branch? [yes/N]`

#### Scenario: Git refuses the branch deletion

- **WHEN** under the flag the main worktree is on a branch that does not
  contain the target's commits, the merge target being checked out in no
  worktree, and the target's upstream's remote-tracking ref was deleted, so
  that Git's own check judges the branch against the command directory's
  `HEAD`
- **THEN** Git refuses with exit status 1, the post-check shows the branch
  present, the target's `branch_retirement` is `retained` with `git-refused`
  and `exit_status: 1`, no other branch command runs for it, later targets are
  `not-attempted`, and the exit status is 2

#### Scenario: The deadline before the branch stage

- **WHEN** under the flag the removal child of the first of two targets is
  still running when the work deadline passes, then exits 0, and the rescan
  proves it `removed`
- **THEN** no re-read or branch child is spawned, its `branch_retirement` is
  `retained` with `deadline-exceeded`, the second target is `not-attempted`
  with `deadline-exceeded`, and the exit status is 1

#### Scenario: A signal around the branch child

- **WHEN** under the flag SIGINT arrives after a target's rescan and before its
  branch child starts
- **THEN** no branch child is spawned, its `branch_retirement` is `retained`
  with `interrupted`, later targets are `not-attempted` with `interrupted`, and
  the exit status is 130
- **AND** when SIGTERM arrives while a branch child is running, that child is
  not signalled and is waited for, the post-check decides its stage, later
  targets are `not-attempted` with `interrupted`, their `branch_retirement`
  `not-attempted` with `target-not-removed` when the target's own is `retired`
  with reason null and with `branch-retention-stop` otherwise, and the exit
  status is 143

#### Scenario: Exit 0 without retirement

- **WHEN** under the flag a test `git` whose `branch -d` exits 0 without
  deleting the branch is first on PATH
- **THEN** the post-check shows the branch present, its `branch_retirement` is
  `retained` with `unconfirmed-retirement` and `exit_status: 0`, later targets
  are `not-attempted`, and the exit status is 2

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

- **WHEN** under the flag a fault is injected into a target's post-check
  listing after its branch child exits 0
- **THEN** its `branch_retirement` has `stage: null` and reason
  `reconciliation-incomplete`, the result's `completeness` is incomplete,
  later targets are `not-attempted`, and the exit status is 1

#### Scenario: The flag's argument rules

- **WHEN** `--retire-branches` is given to plain `project clean`, to
  `--all-safe` without `--apply`, or with `--apply --action push` or `--apply
  --action delete-branch`
- **THEN** the command refuses with `invalid-arguments` and exit 2, and runs
  nothing
- **AND** `project clean <root> --all-safe --apply --yes --json
  --retire-branches` prints exactly one JSON document on standard output, the
  apply result record, whose every target carries `branch_retirement`, with
  the human plan and progress on standard error

#### Scenario: The question names the branches to retire

- **WHEN** `--all-safe --apply --retire-branches` asks its question at a
  terminal for two selected rows
- **THEN** the plan marks both branches for retirement, the question reads
  `Remove 2 worktrees and retire their 2 local branches? [yes/N]`, and the
  answer `y` refuses with `cancelled` and exit 2, nothing removed or deleted

#### Scenario: The plan digest ignores the flag

- **WHEN** a preview `project clean <root> --all-safe` prints digest D, and
  `project clean <root> --all-safe --apply --yes --expect-plan D
  --retire-branches` runs with nothing changed
- **THEN** the fresh digest equals D, the apply proceeds, and every selected
  worktree is removed and its branch retired
