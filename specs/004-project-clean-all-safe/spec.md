Lane: openRepoProject-2

# Feature Specification: Safe batch worktree cleanup

**Feature Branch**: `004-project-clean-all-safe`

**Created**: 2026-10-09

**Status**: Draft

**Input**: User description: "Realize the ratified OpenSpec change
add-project-clean-all-safe: `project clean <root> --all-safe` previews and
applies a batch of eligible worktree removals in one repository, on a removal
path made safe to repeat (opensoft/openRepoProject#9)."

**Source of truth**: `openspec/changes/add-project-clean-all-safe/`
(proposal; spec deltas for `project-clean`, `project-clean-review-safety` and
`project-command`, 17 requirement headers and 100 scenarios; design D1 to D20
with the index of binding rulings in its Context; clarifications N1 to N5),
ratified by Brett Heap on 2026-10-09 in his words to lane openRepoProject-2,
"ratify, merge #11 and run the runbook" (recorded on PR #11,
https://github.com/opensoft/openRepoProject/pull/11#issuecomment-6087170840),
landed on main by squash as `0050f3e` (PR #11). Where this summary is shorter
than the spec deltas, the deltas govern. Exact human text is fixed in
`design.md` D18 and cited, never restated in another form. The change pins its
citations at `da33d92`; this spec cites it only by requirement header,
decision, scenario title and section name, and the plan re-pins code citations
against the `main` of its day (proposal, "Dependencies and Sequencing").

**Relations to earlier features**: `project clean` landed in the `a040790`
baseline (PR #1) beside feature 001's `project` command, under the archived
change `add-project-clean-command`, with no Speckit feature of its own; this
feature is the first to specify it. For `clean` it supersedes that baseline
where the deltas MODIFY the canonical `project-clean` and
`project-clean-review-safety` requirements. For `status`, `doctor` and
`update` it refines feature 001's "Understand a project" and "Maintain a
project" stories as the MODIFIED "Inspect and diagnose" and "Explicit
maintenance" state: a repository they cannot inspect is reported, not
refused, and a `dirty` that could not be established refuses a shape or bench
update as dirty work does. Features 002 (`002-triad-first-project-new`) and
003 (`003-parent-obstacle-wording`) changed `project new` only, and this
feature touches none of their requirements. No earlier feature's record is
edited.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Retire every safe worktree of a repository in one confirmed run (Priority: P1)

A person whose feature work has merged runs `project clean <root> --all-safe`
and sees, in one preview, which linked worktrees would be removed and what
keeps each other row. They run it again with `--apply`, read the same plan
recomputed fresh, and answer one question; every selected worktree is removed
in order and every local branch is kept. Today each worktree takes its own
run, its own selection and its own confirmation.

**Why this priority**: It is the change's purpose (issue #9), and the action
that `add-project-overview`'s `--all-safe` suggestion points to.

**Independent Test**: In a disposable repository with several merged, clean,
published worktrees, each with a commit of its own, beside dirty, locked and
unmerged ones, run the preview, then `--apply` at a terminal and with
`--yes`, and compare the removed set with the plan and each branch with its
planned head.

**Acceptance Scenarios**:

1. **Given** several eligible linked worktrees beside the current, the
   merge-target, a dirty, a locked, a remote-ahead and an unmerged one,
   **When** `--all-safe` previews, **Then** the plan lists the selected rows
   first, then the excluded rows grouped by reason with each group's next
   step, an `ignored-local-files` row showing its bounded count and first
   ignored path, both lists in canonical raw-byte path order, and nothing
   changes.
2. **Given** the same repository, **When** `--all-safe --apply` runs at a
   terminal, **Then** it builds, prints and confirms its own fresh plan with
   one default-No question naming the counts, such as `Remove 7 worktrees,
   keeping 7 branches? [yes/N]`; `yes` begins the apply phase, and `y`, an
   empty line or `no` refuses with `cancelled`, exit 2, removing nothing.
3. **Given** the answer `yes` or the flag `--yes`, **When** the apply phase
   runs, **Then** the eligible worktrees are removed in canonical order from
   the command directory, the others remain, every local branch remains at
   its planned SHA, the result prints `Removed N; branches kept: ` and the
   branches, no push, fetch, force option, branch deletion or remote deletion
   occurs, and the exit status is 0, also when the merge-target branch is
   checked out in no worktree.
4. **Given** a preview with digest D, **When** a selected row's branch
   advances or a new row becomes eligible before `--all-safe --apply --yes
   --expect-plan D` runs, **Then** the fresh plan is printed with its own
   digest and the run
   refuses with `plan-digest-mismatch`, exit 2, before any question or
   removal; when only an excluded row changed, the digest is still D and the
   apply proceeds.
5. **Given** a preview that selected only P1, after which P1 became dirty,
   **When** `--all-safe --apply --yes` runs without `--expect-plan`, **Then**
   the fresh plan excludes P1 as `dirty`, prints "No eligible worktrees" and
   exits 0 without asking; with `--expect-plan` naming the preview's digest it
   refuses with `plan-digest-mismatch`, exit 2, instead.
6. **Given** a complete plan that selects nothing, **When** it previews or
   applies, **Then** it prints "No eligible worktrees" and exits 0 without
   asking.
7. **Given** an incomplete plan that selects nothing, **When** it previews or
   applies, **Then** the preview exits 1 and `--apply` refuses with exit 2
   before asking, never reporting it as empty.
8. **Given** a standard input that is not a terminal, **When** `--all-safe
   --apply` runs without `--yes`, **Then** it refuses with
   `confirmation-required`, exit 2, and removes nothing; with `--yes` the
   selection of that invocation's fresh plan is applied without a question.
9. **Given** `--all-safe` with `--action`, `--branch` or `--worktree`, or
   `--expect-plan` without `--all-safe --apply` or with a value that is not
   64 lowercase hexadecimal characters, **When** the command runs, **Then** it
   refuses with `invalid-arguments`, exit 2, and runs nothing.

**Delta scenarios**: "Stable order and preserved work"; "Every branch remains
after a batch"; "The preview says what keeps each row"; "Only yes confirms";
"Plan digest mismatch"; "Preview is advisory"; "Paths and empty plans"; "A
noninteractive batch needs --yes"; "Invalid argument combinations".

---

### User Story 2 - Work that is not proven disposable is never removed (Priority: P1)

The batch must never delete what the person still needs. A worktree is
removable only when local ancestry proves its branch merged, its reflog shows
that work began on it here, and nothing in it is hidden from Git's own check.
Every other row is kept, with the first gate that kept it and the next step.
The gates close holes in today's single-target removal: an edit hidden by
assume-unchanged is deleted with exit 0, a worktree holding a submodule is
offered and then refused by Git, and a freshly created, published lane
worktree with no commit is removed.

**Why this priority**: A batch repeats the removal, so the removal must first
be safe to repeat (proposal, "Why").

**Independent Test**: Build the repository of "Every protected classifier"
and the reflog fixtures, preview and apply, and check that only the plain
merged worktree with a commit of its own is selected and removed, every other
row carrying the reason the gate order gives.

**Acceptance Scenarios**:

1. **Given** linked worktrees that are stale, detached, dirty, holding ignored
   files, unpublished, remote-gone, diverged, remote-ahead, unpushed,
   pushed-unmerged, merged but current, merged but locked, merged with a
   non-UTF-8 path, merged with an initialized submodule and merged with an
   assume-unchanged entry, beside the main worktree and one plain merged,
   clean, published worktree with a commit of its own, **When** the batch
   previews and applies, **Then** only that last worktree is selected and
   removed, every other row is excluded with its first failing gate, and the
   exit status is 0; a copy that adds an unreadable worktree or a broken
   registration is incomplete and refuses under `--apply` with exit 2.
2. **Given** an otherwise eligible worktree whose own index flags an entry
   assume-unchanged or skip-worktree, sparse checkouts included, **When** the
   batch previews or `--worktree` names it with `--yes`, **Then** it is
   excluded as `hidden-local-state` (a named removal refusing with
   `target-excluded` and that reason, exit 2) and the hidden edit survives.
3. **Given** an otherwise eligible worktree whose index holds a gitlink,
   initialized, deinitialized or never initialized, or whose administrative
   directory holds a `modules` entry, **When** the batch previews or
   `--worktree` names it, **Then** it is excluded as `contains-submodule`, a
   named removal refusing with `target-excluded`, exit 2, before any Git
   removal runs.
4. **Given** a worktree made by `git worktree add -b x`, pushed with
   `git push -u` and never committed to, so that its reflog holds only the
   creation entry, **When** `--all-safe` plans or `--worktree` names it,
   **Then** it is excluded as `unstarted-branch`, also after a rename, and a
   named removal refuses with `target-excluded`, reason `unstarted-branch`,
   exit 2, where before this change `--worktree` removed it.
5. **Given** a branch that gained a commit and that the merge target was then
   fast-forwarded to, so that its head equals the merge target's SHA, **When**
   `--all-safe` plans, **Then** its reflog shows that commit after the
   creation entry, and it is selected and removed.
6. **Given** a branch reset to the merge target's tip by `git worktree add -B`,
   or created there by `git fetch origin feat:f1`, `git update-ref` or
   `git push .` and never committed to here, **When** `--all-safe` plans,
   **Then** it is excluded as `unstarted-branch`.
7. **Given** a branch whose reflog is missing, empty (0 bytes) or expired to a
   lone rename entry, **When** `--all-safe` plans or `--worktree` names it,
   **Then** it is excluded as `reflog-unavailable` with the remedy fixed in
   `design.md` D18, a named removal refusing with `target-excluded`, exit 2,
   where before this change `--worktree` removed it.
8. **Given** a clean, merged worktree whose branch has a commit of its own and
   whose upstream's remote-tracking ref was deleted, **When** it is planned,
   **Then** it is `merged-removable` with that class's recommendation,
   `--all-safe` selects it, and `--worktree` with `--yes` removes it and keeps
   its branch, where before this change it read `unpublished` and was
   refused; an unmerged branch with a deleted upstream is `remote-gone` and
   preserved, and a branch with no upstream configured is `unpublished`.
9. **Given** a dirty or unmerged worktree, a merged one holding ignored files,
   a clean branch pushed but not merged, the main worktree or a locked
   worktree, **When** the report runs or `--worktree` names it, **Then** it is
   preserved with an actionable handoff (for the pushed, unmerged branch, the
   normal pull-request or merge process), no destructive action is proposed,
   and a named removal refuses with `target-excluded` and its reason, exit 2.
10. **Given** no manifest `tracking_branch`, no `origin/HEAD` and neither
    `main` nor `master`, **When** cleanup runs, **Then** it refuses with
    `no-merge-target` instead of guessing from the current branch.

**Delta scenarios**: "Every protected classifier"; "Hidden local state";
"Submodules"; "A published branch with no commit of its own"; "A
fast-forward-merged branch at the target's tip stays eligible"; "A branch
reset to the merge target's tip stays unstarted"; "A branch fetched at the
merge target's tip stays unstarted"; "A branch whose reflog is missing, empty
or expired"; "A merged worktree whose upstream was deleted"; "A deleted
upstream is remote-gone"; "Dirty or unmerged work is preserved"; "A merged
worktree has ignored local files"; "Default branch cannot be established
locally"; "An edit hidden by assume-unchanged survives"; "A worktree holding a
submodule is never offered"; "The main worktree and a locked worktree";
"Pushed feature branch has an open review path".

---

### User Story 3 - A named action keeps its flags and gains the batch's checks (Priority: P1)

`--apply --action remove --worktree P` keeps working as people use it today,
but becomes a one-item batch: the same plan, gates, sequence, refusal codes,
stages and exit codes. It removes P even when another row of the repository
cannot be read, among seventeen eligible rows, and past the row cap, because
refusing it would leave only a raw `git worktree remove`, which skips every
gate. A push keeps its flags too, and refuses a branch whose upstream was
deleted until it is reviewed.

**Why this priority**: Single-target removal is the command people run
today, and three of the five behaviour changes users will notice are its new
refusals and its new removal.

**Independent Test**: In two fresh copies of a repository whose only eligible
worktree is P, run `--worktree P --yes` in one and `--all-safe --apply --yes`
in the other and compare plans, argument vectors and results; then name P
beside an unreadable row, among seventeen eligible rows and above 128 rows,
and apply pushes against a deleted upstream and an incomplete inspection.

**Acceptance Scenarios**:

1. **Given** two fresh copies whose only eligible worktree is P, used in turn
   at one path, **When** one runs `--apply --action remove --worktree P --yes`
   and the other `--all-safe --apply --yes`, **Then** both plans show the same
   `selected` entry for P apart from `dev` and `ino`, both run the same
   argument vector, and both end with P `removed` and exit 0; P made dirty
   between confirmation and revalidation refuses both with `state-changed`,
   the same message, and exit 2.
2. **Given** another worktree that cannot be read, **When** `--worktree P
   --yes` names an eligible P, **Then** P is removed, the plan records the
   other row as a non-blocking omission, and the exit status is 0, while the
   batch refuses with `inspection-incomplete`.
3. **Given** seventeen eligible rows, or more than 128 registered rows with P
   sorting after the first 128, **When** `--worktree P --yes` names P,
   **Then** P is probed first and removed, the other eligible rows are
   `not-requested` or the uninspected rows are counted in `omitted` as a
   non-blocking omission, and the exit status is 0.
4. **Given** an unregistered path or a dirty worktree, **When** `--worktree`
   names it, **Then** it refuses with `worktree-not-found`, or with
   `target-excluded` and `reason: "dirty"`, exit 2; the current worktree and a
   class that is not removable keep their existing refusal messages.
5. **Given** a clean linked worktree whose branch is an ancestor of the merge
   target, **When** its removal is requested, **Then** the command confirms
   and removes the worktree and keeps its branch unless branch deletion is
   separately requested.
6. **Given** a clean feature branch with commits not present on its remote
   branch, **When** a push is applied, **Then** the exact push plan is shown,
   confirmed and pushed without force, and a failed push leaves the
   repository unchanged by the command.
7. **Given** a clean feature branch whose configured upstream's
   remote-tracking ref was deleted, whatever its row's class, **When** a push
   is applied, **Then** it refuses with the reason `remote-gone`, exit 2, and
   runs no push.
8. **Given** another row that is `inspection-error`, or a deadline that passes
   during the re-inspection after confirmation, **When** a push is applied,
   **Then** it refuses with `inspection-incomplete` or `deadline-exceeded`,
   exit 2, and runs no push.
9. **Given** `--apply --action push` or `--apply --action delete-branch` with
   `--json`, **When** the command runs, **Then** it refuses with
   `invalid-arguments`, exit 2, and runs nothing.

**Delta scenarios**: "Single target equals a one-item batch"; "A named
removal beside another row's inspection error"; "A named removal among
seventeen eligible rows"; "A named removal beyond the row cap"; "Remove a
merged clean worktree"; "Push an unpushed feature branch"; "Push refuses a
branch whose upstream was deleted"; "Push refuses an incomplete inspection";
"Push and branch deletion stay human-only".

---

### User Story 4 - A change after the plan stops the removal before it happens (Priority: P2)

Between the plan and each removal, the person, an editor or another agent may
change the repository. Before spawning each removal the command revalidates
that target with a bounded, targeted check against the identities and
evidence it recorded, and refuses at the first difference, removing nothing
more. It claims no lock: concurrent writers are outside the contract, and the
confirmation and the result each state, in one line, the residual window that
remains.

**Why this priority**: The batch's safety rests on it, but it guards against
concurrent change, which is the rarer case.

**Independent Test**: With test hooks between confirmation and each
revalidation, after it, and between Git's removal and the rescan, change the
target, its registration, its branch, the merge target, the manifest or the
repository, and check each target's stage, reason and reconciliation and the
exit status.

**Acceptance Scenarios**:

1. **Given** a confirmed plan, **When** before a target's revalidation the
   target becomes dirty or gains an ignored file, its directory or the
   directory holding it is replaced, its `.git` file or administrative
   `gitdir` file is rewritten, its branch gains a commit, the merge target
   gains a commit, the manifest's `tracking_branch` is edited or made
   unparseable, or `refs/remotes/origin/HEAD` is repointed, **Then** that
   target is `refused` with `identity-changed`, `branch-changed` or
   `state-changed` as the delta maps the difference, nothing is spawned,
   later targets are `not-attempted`, the exit status is 2, and a difference
   the first target's preflight finds removes nothing at all; a fresh plan
   then reports a rewritten registration as `registration-mismatch`, an
   `inspection-error` row, and is incomplete.
2. **Given** an assume-unchanged flag set, or a `modules` directory created in
   the administrative directory, of a selected target after confirmation,
   **When** it is revalidated, **Then** it is `refused` with
   `hidden-local-state` or `contains-submodule`, later targets are
   `not-attempted`, and the exit status is 2.
3. **Given** two selected rows whose upstreams were deleted, each recorded
   with `upstream_oid`, `ahead` and `behind` null, **When** a fetch recreates
   the first one's upstream before apply, **Then** the first is `refused` with
   `state-changed`, nothing is removed, and the exit status is 2; when the
   fetch instead recreates only the second's upstream after the first's
   removal, the first, null in the plan and null at revalidation, is
   `removed` and the second is `refused` with `state-changed`, exit 2.
4. **Given** `status.showUntrackedFiles=no` in the user's configuration, or
   the untracked cache on with `core.checkStat=minimal` after an
   index-writing status, **When** a file is created in a target after its
   revalidation, **Then** Git's own check, on the removal command's pinned
   configuration, refuses with 128, the target is `failed` with
   `git-refused`, the file survives, and the exit status is 128.
5. **Given** an ignored file created in a target after its revalidation,
   **When** the removal runs, **Then** Git removes the worktree and the file
   with exit 0, the target is `removed`, and the result carries the
   residual-window line that the confirmation also carried.
6. **Given** a target's branch advanced or deleted after Git removed the
   worktree and before the rescan, **When** the rescan runs, **Then** the
   target is `removed` with `branch-advanced-after-removal` or
   `branch-missing-after-removal`, no commit is lost, later targets are
   `not-attempted`, and the exit status is 2.
7. **Given** the repository root replaced by another clone, or its parent
   directory by a symlink to a copy, after the first target's removal and
   before its rescan, **When** the rescan runs, **Then** the first target is
   `unknown` with `unconfirmed-removal`, every reconciliation field null and
   `reconciled: false`, the others `not-attempted` with `batch-stopped`, and
   the exit status is 1; the same replacement before the first revalidation
   refuses it with `identity-changed`, exit 2, removing nothing.
8. **Given** a new linked worktree registered after confirmation, or a target
   that changes after earlier targets were removed, **When** the run
   continues, **Then** the new worktree is not selected, and the changed
   target stops the run with the earlier targets' stages and retained
   branches reported accurately.

**Delta scenarios**: "Worktree changes while confirmation is pending";
"Target directory replaced"; "Admin registration changed"; "Parent directory
swapped"; "New worktree and pre-removal changes"; "State changes before
revalidation"; "Changed later target"; "Untracked file under
status.showUntrackedFiles=no"; "Branch advances before removal"; "Deleted
upstream reappears before revalidation"; "Git's own check runs on the pinned
configuration"; "Ignored file in the residual window"; "Branch advances after
removal"; "Repository replaced mid-batch".

---

### User Story 5 - Every removal ends in a record the person can reconcile (Priority: P2)

Whatever stops a batch (Git refusing, a Git that reports success without
removing, a signal, the deadline, an exception, a hung mount), every selected
target ends in one stage with one reason and, where a child ran, a
reconciliation record from a rescan; a target is `removed` only on rescan
evidence. A started removal is never interrupted, because stopping it midway
leaves a half-deleted tree: the person sees a wait line instead, then a
result naming what was removed, what was not attempted, every branch kept and
the next command.

**Why this priority**: A batch that stops must leave the person knowing
exactly where they stand; it matters once the batch exists.

**Independent Test**: Drive the apply phase with test Gits and hooks (exit 0
without removing, exit 128, exit 255 leaving a directory, a removal past the
ceiling, SIGINT, SIGTERM and SIGHUP, an injected exception, an unreadable
parent) and check each target's stage, reason, notes and reconciliation, the
stop block and the exit status.

**Acceptance Scenarios**:

1. **Given** SIGINT, SIGTERM or SIGHUP while the second of three removals is in
   flight, **When** the signal arrives, **Then** the removal child is not
   signalled and is waited for, the second target is `removed` on rescan
   evidence or `failed` with Git's status, the third is `not-attempted` with
   `interrupted`, and the exit status is 130, 143 or 129; SIGINT or end of
   input at the question exits 130 with nothing removed.
2. **Given** a planning probe of a test Git that ignores SIGTERM, **When**
   SIGTERM reaches `project`, **Then** that probe's process group is killed
   2 s later and reaped, no process of it remains, nothing is mutated, the
   exit status is 143, and under `--json` standard error carries `Cancelled.`
   while standard output holds no JSON document.
3. **Given** a test Git that exits 0 without removing anything, **When** the
   rescan runs, **Then** the target is `unknown` with `unconfirmed-removal`,
   later targets are `not-attempted`, and the exit status is 1.
4. **Given** Git unregisters a target but cannot delete its directory and exits
   255, **When** the run reconciles, **Then** the target is `failed` with
   `git-failed` and `notes: ["orphaned-directory"]`, its reconciliation shows
   the registry entry gone, the path present and the branch kept, later
   targets are `not-attempted`, nothing deletes the directory, no later plan
   lists it, and the exit status is 255.
5. **Given** a lock added to a target after its revalidation, **When** Git
   refuses the removal with 128, **Then** the target is `failed` with
   `git-refused`, the record holds the command, the status and a
   reconciliation with the entry and path present, every retained branch is
   reported, and the exit status is 128.
6. **Given** a removal still running 300 s after its spawn, **When** the
   ceiling passes, **Then** its process group is killed and the rescan
   decides: `removed` when the registry entry and path are gone, otherwise
   `unknown` with the note `partially-removed` and the recovery text, the
   reason `removal-ceiling` either way, later targets `not-attempted`, and
   the exit status 1.
7. **Given** a rescan whose `lstat` fails, or a fault injected into a target's
   reconciliation, **When** the run ends, **Then** the target is `unknown`
   with `reconciliation-incomplete` or `internal-error`, the record is
   printed, later targets are `not-attempted`, and the exit status is 1.
8. **Given** `project` and its removal child both killed with SIGKILL during a
   large deletion, **When** plain `project clean` runs afterwards, **Then** a
   target whose `.git` file survived reads `dirty` with the dirty advice and,
   beside it, the probable partial-removal note and recovery text, and one
   whose `.git` file was deleted reads `registration-mismatch` with
   classification `inspection-error`, a named manual remedy and no note; a
   worktree with one deleted tracked file and one untracked file carries no
   note.
9. **Given** a batch of three stopped at its second target, refused with
   `branch-changed`, **When** the result prints, **Then** it reads
   `Stopped at <second path> (branch-changed). Removed 1 of 3. Not attempted:
   <third path>. Next: ` followed by the command for a fresh read-only plan,
   and names every retained branch.

**Delta scenarios**: "A signal during a removal"; "SIGTERM before the apply
phase"; "Exit 0 without evidence"; "Git leaves an orphaned directory"; "Git
refuses the removal"; "A removal past the hard ceiling"; "Unreadable path
after removal"; "Exception after the apply phase begins"; "project killed
during a deletion"; "Only tracked-file deletions"; "The stop block".

---

### User Story 6 - Every run is bounded and says what it left out (Priority: P2)

A repository with hundreds of worktrees, a huge index or a slow disk must
neither hang the command nor be half-read in silence. Every `clean` run has
one deadline, per-child budgets and row and target caps; a plan that hits any
of them is incomplete, says so and blocks apply, and plain `project clean`
now exits 1 when its report is incomplete. More than sixteen removable rows
are handled sixteen per run, each run planning afresh.

**Why this priority**: Bounds keep the batch predictable, yet most
repositories stay well inside them: task 2.1 surveyed 561 worktree rows in
296 resolving repositories, and its fit test rejected no cap.

**Independent Test**: Under a counting `git` wrapper and slow test Gits,
register more rows than the caps, more removable rows than sixteen and a
worktree with 70 ignored files, and check completeness, `omitted`, the exit
statuses, the child counts and each run's elapsed time.

**Acceptance Scenarios**:

1. **Given** more than 128 registered rows, a probe that times out, or a
   deadline that passes while planning, **When** `--all-safe` previews,
   **Then** the plan is incomplete with `inspect-cap`,
   `inspection-incomplete` or `deadline-exceeded`, the main worktree and the
   127 linked worktrees with the smallest paths are the rows inspected,
   `omitted` and the timed-out rows are visible, the preview exits 1, and
   `--apply` refuses with exit 2 before any mutation.
2. **Given** twenty rows that pass every gate before `deferred-target-cap`,
   none holding a submodule or hidden local state, **When** `--all-safe
   --apply --yes` runs twice, **Then** the first run removes the first
   sixteen in canonical order and defers four with the command to run next,
   its plan complete and its exit status 0, and the second run removes the
   four.
3. **Given** more than 256 registered rows, **When** plain `project clean`
   runs, **Then** it prints an incomplete report with `inspect-cap` and
   `omitted` and exits 1, where before this change it exited 0; with 200 rows
   the report is complete and exits 0, says that `--all-safe` itself would be
   incomplete, and its JSON carries `selected: null` and a `notes` entry
   `inspect-cap` with `rows: 200`, while `--all-safe` there exits 1.
4. **Given** a worktree whose path cannot be read for a reason other than its
   absence, or a status probe that fails in the main worktree or on the
   merge-target checkout, **When** plain `project clean` runs, **Then** that
   row is `inspection-error` (with `present: null` and an `os-error`, or a
   null `dirty`), never `protected-default`, every other row is reported, and
   the report is incomplete and exits 1; before this change an unreadable
   path or a failed root status refused the whole command with exit 2.
5. **Given** a merged, clean worktree with 70 ignored files, **When** the plan
   is built, **Then** the probe stops at the 65th ignored record, the row has
   `ignored_files: 64`, `ignored_files_truncated: true` and 8
   `ignored_samples`, and it is excluded as `ignored-local-files`; exactly 64
   ignored files give `ignored_files_truncated: false` and the same
   exclusion, and 4,097 untracked entries stop the probe with `dirty: true`
   and the plan complete.
6. **Given** five rows with three selected and a counting `git` wrapper on
   PATH, **When** `--all-safe --apply --yes` runs, **Then** each target's
   revalidation spawns at most five children, the final rescan three, no
   merged-set listing and no probe of a non-selected worktree runs after
   confirmation, worktree probes run in their own worktree and every other
   child in the command directory, and `probes.performed` equals the
   wrapper's count.
7. **Given** a test Git's removal of the second of three targets still running
   at the work deadline, **When** the deadline passes, **Then** the child is
   waited for and the second target ends by its own exit and the rescan, the
   third is `not-attempted` with `deadline-exceeded`, and the exit status is
   1; when less than 5 s of the work deadline remains as a target passes
   revalidation, no child is spawned for it or any later target.
8. **Given** `project clean` without an apply action, **When** it runs,
   **Then** it prints a cleanup plan for the main checkout and each linked
   worktree without fetching, committing, pushing, resetting, stashing or
   removing anything, and says that remote information may be stale.

**Delta scenarios**: "Audit a repository with a feature worktree"; "The plain
report exits by completeness"; "An unreadable worktree is one row"; "A failed
status probe on the merge-target checkout"; "A failed status in the
repository root"; "Row cap and planning failures"; "Twenty rows pass every
gate before deferred-target-cap"; "Ignored-file bound"; "Bounded
revalidation work"; "Deadline expiry mid-batch".

---

### User Story 7 - The command acts on exactly the repository it was given (Priority: P2)

Today an absolute path can be silently redirected to a family holder or a
manifest ancestor, and a bare repository's worktrees can be removed. Every
`clean` mode now resolves its argument Git-first to exactly one repository
and its main worktree, refuses what is not a repository root, and finds the
merge target by a fixed, recorded order.

**Why this priority**: A batch must never act on a neighbour, and the
overview's suggested command relies on identity surviving the handoff.

**Independent Test**: Pass subdirectories, linked worktrees, bare
repositories, submodule and separate-git-dir checkouts, family and manifest
layouts, and manifests of each kind to each `clean` mode, and check the
resolved `repository`, `root` and `merge_target`, or the refusal.

**Acceptance Scenarios**:

1. **Given** an absolute path to a repository's subdirectory, to one of its
   linked worktrees, to a directory outside any repository or to a bare
   repository, **When** any `clean` mode receives it, **Then** it refuses with
   `target-not-repository-root`, exit 2, before any plan, substituting no
   other directory and changing nothing.
2. **Given** an Atlas root with an ancestor holding `project.yaml`, or
   containing `Atlas/family.yaml`, and an independent clone named Atlas under
   a second projects directory, **When** the argument vector `["project",
   "clean", "<Atlas root>", "--all-safe"]` runs without a shell, **Then** the
   plan's `repository` names Atlas by its four identity fields, `root` is the
   Atlas root, and the other clone is never inspected; without the family
   holder, the bare name `Atlas` keeps the name lookup and refuses with
   `ambiguous-name`, exit 2.
3. **Given** a relative path or no argument inside a linked worktree of a bare
   repository, or a submodule's checkout, **When** `clean` runs, **Then** it
   refuses with `target-not-repository-root`, exit 2, where before this change
   it reported the repository (and, for a bare one, could remove its
   worktrees).
4. **Given** a checkout made with `git init --separate-git-dir`, **When** its
   absolute path is passed, **Then** it resolves, `repository.root` is that
   checkout, and the git directory is not a worktree row.
5. **Given** a manifest `tracking_branch` of `origin/develop` with local
   `develop` and `main`, or a manifest naming `release` while `origin/HEAD`
   names `main`, **When** the plan is built, **Then** `merge_target` is
   `develop` or `release` with `source: "manifest"`, never `main` by a silent
   fallback, the second carrying a `merge-target-conflict` note with apply
   allowed; with no manifest candidate and `origin/HEAD` naming `trunk`, it
   is `trunk` with `source: "origin-head"`.
6. **Given** no candidate, a manifest of the wrong kind, or a manifest over
   1 MiB, **When** any mode runs, **Then** it refuses with `no-merge-target`
   (its existing message) or `manifest-invalid`, exit 2, before any worktree
   row is probed, `--json` printing the extended error object.

**Delta scenarios**: "Absolute path that is not a repository root"; "Overview
handoff keeps identity"; "A bare repository reached from a linked worktree";
"A separate git directory"; "A submodule checkout"; "Merge target missing,
invalid, or conflicting"; "A tracking branch spelled with its remote"; "A
manifest over 1 MiB".

---

### User Story 8 - Every path is exact and every JSON run prints one document (Priority: P3)

Scripts and the overview read `clean --json`. Every run prints one versioned
document, and with `--apply` the human plan and question move to standard
error so that standard output holds only the result record. Paths holding
newlines, control or bidirectional characters, or bytes that are not UTF-8
are reported exactly or excluded, never misread and never passed to a
removal.

**Why this priority**: It serves automation and rare paths; the person at a
terminal is served by the earlier stories.

**Independent Test**: On Linux, create worktrees whose paths hold a newline,
a tab, U+0001, U+202E and the byte 0xFF, run the preview and the apply with
and without `--json`, and parse standard output as JSON in every mode.

**Acceptance Scenarios**:

1. **Given** eligible worktrees whose paths contain a newline, a tab, U+0001
   and U+202E, and an otherwise eligible one whose path contains the byte
   0xFF, **When** the batch previews and applies, **Then** the first four are
   selected with exact JSON strings and `path_valid_utf8: true`, printed in
   the `$'...'` form with `\u000a`, `\u0009`, `\u0001` and `\u202e`, passed to
   Git raw as one argument each and proven removed by rescan; the fifth is
   excluded as `unsupported-path-bytes`, shown with `\xff` and
   `path_valid_utf8: false`, never passed to a removal, and still present.
2. **Given** a repository root containing the byte 0xFF, **When** `project
   clean <that root> --all-safe` runs, **Then** it refuses with
   `unsupported-path-bytes`, exit 2, building no plan or digest.
3. **Given** `--all-safe --apply --yes --json` on a repository where it
   removes two worktrees, **When** it runs, **Then** standard output holds
   exactly one JSON document, the apply result record with two `removed`
   targets and `exit_code: 0`, and the human plan and progress are on
   standard error; a run stopped by `plan-digest-mismatch` prints only the
   plan envelope.
4. **Given** one eligible linked worktree, **When** `project clean <root>
   --json` runs, **Then** it prints one envelope with `schema_version: 1`,
   `mode: "report"`, `apply_allowed: false` and `limits.worktree_rows: 256`,
   that worktree in `selected` and a `plan_digest`, and exits 0.

**Delta scenarios**: "Control-character and non-UTF-8 paths"; "Non-UTF-8
repository root"; "Apply with JSON prints one document"; "The plain report in
JSON".

---

### User Story 9 - Status, doctor and update read the same evidence (Priority: P3)

`clean`, `status`, `doctor` and `update` inspect repositories through one
bounded evidence model on Git 2.36 or later: Git's version checked once, the
caller's Git variables scrubbed, the status configuration pinned, lazy
fetches refused locally, and every Git child stopped and reaped on every exit
path. `clean` refuses an old or missing Git; `status`, `doctor` and `update`
report instead of refusing, and a row they cannot inspect is an
`inspection-error` row, never a crash or a silent null.

**Why this priority**: The model is built first because every other story
reads it, but what it changes for a person using `status`, `doctor` and
`update` matters less than the cleanup itself.

**Independent Test**: With Git 2.35 first on PATH, with no `git`, with fake
Gits that flood standard error, ignore SIGTERM or print 5,000 ignored
records, with hostile caller variables and configuration, and in a partial
clone whose upload-pack logs each run, run `clean`, `status`, `doctor` and
`update` and check refusals, error rows, exit statuses and a counting
wrapper's record of every child.

**Acceptance Scenarios**:

1. **Given** Git 2.35 first on PATH, **When** `clean` runs in any mode,
   **Then** it refuses with `git-too-old`, exit 2, before any repository
   probe, its `--json` error object carrying `code: "git-too-old"`; with no
   `git` on PATH it refuses with `git-unavailable`, exit 2.
2. **Given** Git 2.35 first on PATH, or no `git`, **When** `status` and
   `doctor` run, **Then** doctor reports `git-too-old` or `git-unavailable` as
   an `error` check row and exits 1, status marks the root `inspection-error`
   and exits 0, neither refuses, and a directory with no `.git` still reads
   `present: false`; `update --apply --component workflow --yes` is not
   refused for Git's version.
3. **Given** a root whose status probe fails, **When** `status` and `doctor`
   run, **Then** the root is reported with `classification:
   "inspection-error"`, its `errors` and a null `dirty` instead of a refusal
   with exit 2, and doctor reports an `error` check row and exits 1.
4. **Given** a leg whose status probe times out at 15 s, **When** `update
   --apply --component shape` runs, **Then** it refuses with exit 2 and the
   owner tool is never invoked.
5. **Given** a fresh project with no remote, **When** doctor runs, **Then** its
   null `upstream`, `ahead` and `behind` raise no error and doctor passes,
   while a leg whose `dirty` is null after a failed probe gets an `error`
   check row and exit 1.
6. **Given** a branch whose upstream's remote-tracking ref was deleted,
   **When** status and doctor report it, **Then** its `upstream` is the
   configured short name, such as `origin/<branch>`, and its `ahead` and
   `behind` are null, where before this change `upstream` was null.
7. **Given** fake Gits that write over 64 KiB to standard error, ignore
   SIGTERM, or print 5,000 ignored records, **When** a status probe runs each,
   **Then** the first completes with no `probe-timeout`, the second's group is
   killed 2 s after SIGTERM and the row recorded `probe-timeout` and
   `inspection-error` with no process left, and the third stops at the 65th
   record with `ignored_files: 64`, a complete outcome, classified
   `ignored-local-files`.
8. **Given** `status.showUntrackedFiles=no`; `GIT_DIR`, `GIT_WORK_TREE` and
   `GIT_INDEX_FILE` naming another repository; `GIT_INTERNAL_SUPER_PREFIX` set
   under Git 2.36; or `core.untrackedCache` and `core.fsmonitor` on in the
   file `GIT_CONFIG_GLOBAL` names, **When** inspection runs, **Then** a clean
   worktree is classified by the ladder, every probe reads the resolved
   repository and each worktree's own index, inspection succeeds on Git 2.36,
   and every status and removal child carries the two status pins.
9. **Given** a partial clone made with `--no-checkout --filter=tree:0` whose
   `remote.origin.uploadpack` names a script that logs each run, **When** a
   status probe runs, also with `GIT_ALLOW_PROTOCOL=file` in the caller's
   environment and `protocol.file.allow=always` in the clone's configuration,
   **Then** the child carries `-c protocol.allow=never` and the six
   per-protocol pins, Git refuses the fetch locally, the probe is
   `probe-failed`, the row is `inspection-error`, and the script never runs.
10. **Given** a declared leg with no checkout, or `update` run without
    `--apply`, **When** doctor or update runs, **Then** doctor reports an
    actionable failure and returns nonzero, and update reports a plan without
    modifying repositories or installing software.

**Delta scenarios**: "Git older than 2.36"; "Git older than 2.36 in status
and doctor"; "No git on PATH"; "A failed root status is reported"; "A leg's
probe times out"; "Tools and workflow need no Git"; "Not established is an
error, none is not"; "A deleted upstream in status and doctor"; "A git that
floods standard error"; "A git that ignores SIGTERM"; "Five thousand ignored
records"; "User status configuration"; "A caller's Git environment is
ignored"; "The sixteenth scrubbed name on Git 2.36"; "The pinned status
configuration"; "A lazy fetch in a partial clone is refused locally";
"Missing leg"; "Default report".

---

### Edge Cases

- **EC-001**: A squash-merged branch never puts its tip into the merge
  target's ancestry, so it is never selected, and a squash-merging
  repository's batch selects little. Open question 2 (a local
  patch-equivalence proof) is deferred to a follow-on change and is not
  decided here (proposal, "Open Questions"; Out of Scope).
- **EC-002**: An ignored cache such as `__pycache__` keeps its worktree out as
  `ignored-local-files` until the cache-disposal change; the batch's yield is
  bounded on purpose (proposal, "Why"; Out of Scope).
- **EC-003**: A repository without file reflogs (the reftable backend, or
  `core.logAllRefUpdates=false`) excludes every merged row as
  `reflog-unavailable`, failing closed with its own reason (design, Risks).
- **EC-004**: A branch with no activity for `gc.reflogExpire` (90 days by
  default) keeps no decisive reflog entry and is `reflog-unavailable` in both
  modes, never removable by `project`; its remedy names `git worktree
  remove` (design D10 and D18).
- **EC-005**: A reflog over 64 KiB (about 300 entries) is
  `reflog-unavailable` even when it records movement, because the bound ends
  the read; a reflog whose last entry's new object is not the branch head is
  `reflog-unavailable` too (design D10, Risks).
- **EC-006**: A branch created from a remote branch that already had commits,
  then merged elsewhere and never moved here, reads `unstarted-branch` and
  fails closed with that remedy (design, Risks).
- **EC-007**: A live session (an editor or agent) in a started, merged
  worktree is not protected, since the change declines an `in-use` gate; the
  README asks for sessions to be closed before a batch apply, the
  confirmation lists every path, and the kept branch means no commit is lost
  (design D3).
- **EC-008**: Sixteen rows that an index gate always excludes, ahead of a
  backlog, stop the deferral from draining until a person handles them; when
  all sixteen are `contains-submodule` (Opensoft-Tenant's case in task 2.1's
  survey) the human report says why (design D12 and D18, Risks).
- **EC-009**: Rows of 100,000-entry indexes and CPU saturation exceed the
  measured budgets; the plan goes incomplete with `deadline-exceeded`, never
  unsafe, and a removal started within the floor is waited for (design D5,
  Risks).
- **EC-010**: A remote-helper protocol of another name, with its own
  `allow=always` in the repository's configuration, is not among the pins and
  could still fetch for a probe in a partial clone; the probe then succeeds
  rather than fails, and no unsafe removal follows (design D11, Risks).
- **EC-011**: SIGKILL of `project` runs no cleanup: its probe children run on,
  read-only, to their own end, and a removal child to its own end; the next
  report shows the partial-removal note or a `registration-mismatch` row
  (design D1 and D4).
- **EC-012**: A filesystem call stuck in the kernel is abandoned after its
  budget so the run never blocks on it, and is the one exception to the run
  bound (design D6 and D9, Risks).
- **EC-013**: After SIGHUP the terminal may answer writes with an error, so
  the result record is printed on a best-effort basis (design D15).
- **EC-014**: A plain report of 129 to 256 rows withholds the selection, and
  its `inspect-cap` note alone does not make it incomplete; its digest, over
  a null `selected`, is never consumable by `--expect-plan` (design D14).
- **EC-015**: A value null in the plan and null at revalidation, such as a
  deleted upstream's `upstream_oid`, is no difference; a value that cannot be
  re-read, a timed-out filesystem call included, is one (design D7 and D20).
- **EC-016**: Ignored files created, or index flags set, after the last
  revalidation, and any change after Git's own check, are outside the
  guarantee: such a target is removed, and the residual-window line says so
  (design D7).
- **EC-017**: A probe stopped at its record bound is complete, never
  `probe-failed`; a partial-removal note is judged on the records read, and
  4,097 records with no ignored one leave `ignored_files` null (design D2 and
  D4).
- **EC-018**: Git's own exit status passes through even when it equals one of
  `project`'s own codes; the result record tells them apart (design D19).
- **EC-019**: Non-UTF-8 path scenarios cannot run on macOS, whose filesystems
  reject such names, and are skipped there with that reason (design, Risks).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `project clean` MUST inspect the target repository and every
  linked worktree from local Git state only, and report each worktree's path,
  branch or detached state, cleanliness, upstream, ahead and behind counts as
  of the last fetch, and whether its commits are merged into the merge
  target, saying in human and JSON output that remote information may be
  stale. Without an apply action it MUST NOT fetch, commit, push, reset,
  stash or remove anything. Traces: "Clean reports local worktree state".
- **FR-002**: `project clean` MUST run its Git version check before any other
  Git child and, before any repository is probed, refuse a Git older than
  2.36 with `git-too-old` and a `git` that is missing or unusable with
  `git-unavailable`, exit status 2, printing under `--json` the extended
  error object carrying that code. Traces: "Clean reports local worktree
  state"; "Repository inspection requires Git 2.36 and shares one evidence
  model".
- **FR-003**: The plain report (neither `--all-safe` nor `--apply`) MUST be
  the plan a batch preview builds, in `mode: "report"`, under a cap of 256
  worktree rows, carrying every plan field with `apply_allowed` false. For at
  most 128 worktree rows, `selected` MUST be what `--all-safe` would select,
  the per-run deferral applied; above 128, `selected` MUST be null and
  `notes` MUST carry an `inspect-cap` entry with `rows`, the count of
  registered worktree rows, beside the human line saying that `--all-safe`
  itself would be incomplete, a note that alone MUST NOT make the report
  incomplete, while the gates still run for every inspected row and
  `excluded` lists every row a gate excludes. Traces: "Clean reports local
  worktree state"; design D14.
- **FR-004**: The report's `plan_digest` MUST be computed over the same
  canonical text as any plan. Above 128 rows it covers a null `selected` and
  MUST never be consumed by `--expect-plan`, because an apply there is
  refused as incomplete first; at most 128 rows it MUST equal the
  `--all-safe` preview's digest for the same repository identity, merge
  target and selection, so that an `--expect-plan` carrying it matches, and a
  merge target that advances in between gives `plan-digest-mismatch`.
  Traces: "Clean reports local worktree state"; design D14.
- **FR-005**: The plain report MUST exit 0 when complete, 1 when incomplete
  (`inspect-cap`, `inspection-incomplete` or `deadline-exceeded`) and 2 when
  no report can be built, and its human output MUST say whether it is
  complete and, if not, why, with the report lines fixed in `design.md` D14.
  Traces: "Clean reports local worktree state"; design D14 and D19.
- **FR-006**: A worktree whose registered path cannot be read for any reason
  other than its absence MUST be one row with `present: null`, an `os-error`
  and classification `inspection-error`, never a refusal of the repository.
  A status probe that fails or times out in any row, the main worktree's and
  the merge-target checkout's included, MUST leave that row's `dirty` null
  and classify it `inspection-error`. `ignored_files` MUST count the ignored
  entries observed, a lower bound when `ignored_files_truncated` is true, and
  the report's `root` MUST name the command directory, the main worktree of
  the resolved repository. Traces: "Clean reports local worktree state".
- **FR-007**: Each worktree row MUST get exactly one of fifteen classes, by a
  ladder tested in this order: `stale-worktree`, `protected-default`,
  `inspection-error`, `dirty`, `ignored-local-files`, `detached`,
  `unpublished`, `remote-gone`, `review-required`, `diverged`,
  `remote-ahead`, `unpushed`, `merged-removable`, `merged-current`,
  `pushed-unmerged`. The ladder MUST be a function of the row's evidence
  alone; its names MUST NOT change, and its order MUST NOT change except that
  a branch whose configured upstream's remote-tracking ref no longer exists
  is tested for local ancestry before the `remote-gone` rung: when its
  `merged_into_target` is true it is `merged-removable` (or `merged-current`
  for the current worktree), and otherwise `remote-gone`. A row whose
  evidence could not be established
  MUST be `inspection-error` whatever its branch; a branch with no configured
  upstream MUST be `unpublished`; `review-required` stays a defensive rung
  that no evidence reaches. Traces: "Clean classifies preservation and
  cleanup actions"; design D6.
- **FR-008**: Every class other than `merged-removable` MUST be preserved
  with an actionable human handoff, and a merged row whose upstream was
  deleted MUST carry its class's recommendation. A clean branch pushed but
  not merged MUST be sent to the repository's normal pull-request or merge
  process, and the command MUST NOT create, approve, merge, close or delete a
  pull request implicitly. Traces: "Clean classifies preservation and cleanup
  actions"; "Clean hands off work requiring review".
- **FR-009**: A linked worktree's `dirty` row whose status records are all
  deletions of tracked files, while its `.git` file and registry entry are
  present, MUST carry the advisory row note `partially-removed`, shown in
  human output with the recovery text beside the `dirty` advice and never
  instead of it, judged on the records read when the stream stopped at its
  bound, and changing no classification, ladder rung or gate. Traces: "Clean
  classifies preservation and cleanup actions"; design D4.
- **FR-010**: A push MUST stay a confirmed, non-force push of a named
  non-default branch that preserves the delegated exit status and output,
  refusing a default branch or unresolved local work. It MUST refuse, with
  exit status 2 and no push, a branch whose configured upstream's
  remote-tracking ref no longer exists, whatever its row's class, naming the
  reason `remote-gone`; and it MUST refuse with `inspection-incomplete`,
  `inspect-cap` or `deadline-exceeded`, exit 2, when the full inspection it
  acts on, before or after confirmation, is incomplete. Push and branch
  deletion MUST resolve their argument Git-first, run in `mode: "single"`
  for the row cap and bounds, keep their own children unbounded as before,
  and refuse `--apply --json` with `invalid-arguments`, exit 2. Traces:
  "Clean can explicitly push safe feature branches"; "Clean bounds its Git
  work and reports omitted work".
- **FR-011**: The command MUST remove one named linked worktree, or the set a
  fresh `--all-safe` plan selects, only when each is clean, not the current
  worktree, merged into the merge target and passing every gate of FR-020.
  Every removal, single or batch, MUST follow one sequence: revalidate the
  target (FR-046); spawn, only while at least the 5 s removal floor of the
  work deadline remains, the non-force `git worktree remove` of that path
  from the command directory in its own process group, pinned with
  `status.showUntrackedFiles=normal`, `core.untrackedCache=false`,
  `core.fsmonitor=false` and the protocol pins of FR-054, as the delta spells
  the command; wait for it; and reconcile by rescan. Removal MUST stop after
  the first target whose result is not a plain `removed`, with no
  continuation, rollback or automatic retry. Traces: "Clean can explicitly
  retire verified worktrees"; design D9.
- **FR-012**: Once spawned, a removal child MUST NOT be signalled on SIGINT,
  SIGTERM, SIGHUP or the work deadline, and MUST be waited for, the wait line
  fixed in `design.md` D18 printed at most once. Only a hard ceiling 300 s
  after its spawn MUST end the wait, by killing its process group, after
  which the rescan decides: `removed` when its registry entry and path are
  gone, and otherwise `unknown` with the note `partially-removed` and the
  recovery text, with the reason `removal-ceiling` either way. Traces: "Clean
  can explicitly retire verified worktrees"; design D9 and D15.
- **FR-013**: For a removal named by `--worktree P`, the plan's completeness
  MUST be the repository-wide evidence plus P's own row: P MUST be probed
  first and be exempt from the row cap, and another row's `inspection-error`,
  its omission by the cap, or its being left unprobed MUST be recorded as a
  non-blocking plan note (`inspection-incomplete`, `inspect-cap` or
  `deadline-exceeded`) and MUST NOT refuse P, while P's own inspection,
  revalidation and removal floor stay fully strict. Traces: "Clean can
  explicitly retire verified worktrees"; design D13.
- **FR-014**: A local branch MUST be removed only as a separate, explicit
  action after its worktree is gone and the branch is verified merged, and
  the command MUST never use a force removal, reset, or deletion of unmerged
  work. Traces: "Clean can explicitly retire verified worktrees".
- **FR-015**: Noninteractive execution MUST refuse apply actions unless the
  user supplied explicit confirmation and action targets. `--all-safe` MUST
  count as an explicit action target, the set its own fresh plan selects,
  and `--yes` as explicit confirmation of that plan; `--apply` on a standard
  input that is not a terminal and without `--yes` MUST refuse with
  `confirmation-required`, exit 2, before any mutation. Traces: "Clean hands
  off work requiring review".
- **FR-016**: Every `clean` mode MUST resolve its argument to exactly one
  repository. An absolute path MUST be exactly a main worktree root, its
  realpath equal to the toplevel Git reports there and that toplevel the
  main worktree, else `target-not-repository-root`; a relative path or no
  argument MUST resolve to the repository Git finds there, refused with
  `target-not-repository-root` where Git finds no worktree; a bare name (one
  path component) MUST keep the project-name lookup, its one Git child
  counted and bounded, refusing with `ambiguous-name` or
  `repository-not-found`. The manifest-ancestor and family-holder
  redirections MUST NOT apply to a path argument, and every repository-wide
  Git child after resolution, every removal and the manifest read MUST use
  the main worktree as the command directory. Traces: "Clean resolves its
  target Git-first"; design D8.
- **FR-017**: A bare repository MUST be refused in every mode with
  `target-not-repository-root`, also from a relative path, no argument or a
  bare name inside one of its linked worktrees. A submodule checkout MUST be
  tested first and refused the same way. Where the first registry record is
  the common directory itself, the main worktree MUST be the realpath of
  `core.worktree` or, where that is unset, the candidate toplevel whose
  `.git` file names the common directory; the common directory MUST never be
  a worktree row, and a linked worktree whose main checkout cannot be named
  MUST be refused. Traces: "Clean resolves its target Git-first"; design D8.
- **FR-018**: The merge target MUST be the first candidate that exists as a
  local branch: the manifest's `tracking_branch` less any leading `origin/`;
  the branch that `refs/remotes/origin/HEAD` points to, less
  `refs/remotes/origin/`; `main`; `master`. It MUST be recorded as `{name,
  source, sha}`, `source` being `manifest`, `origin-head`, `main` or
  `master`. A manifest naming a different existing branch from `origin/HEAD`
  MUST win, with an informational `merge-target-conflict` note; no candidate
  MUST refuse with `no-merge-target`, keeping its existing message; and a
  manifest that cannot be read, has the wrong kind or exceeds 1 MiB MUST
  refuse with `manifest-invalid`. Each such refusal MUST exit 2 before any
  mutation and, under `--json`, print the extended error object. Traces:
  "Clean resolves its target Git-first"; design D8.
- **FR-019**: `project clean <root> --all-safe [--json] [--apply [--yes]
  [--expect-plan D]]` MUST plan every eligible linked worktree of one
  resolved repository, and never of a sibling, family member, mounted leg,
  pinned member copy or independent clone. `--all-safe` combined with
  `--action`, `--branch` or `--worktree`, `--expect-plan` without
  `--all-safe --apply`, or an `--expect-plan` value that is not 64 lowercase
  hexadecimal characters MUST refuse with `invalid-arguments`, exit 2.
  Traces: "Clean previews and applies a batch of eligible worktree removals
  in one repository".
- **FR-020**: A row MUST be selected only when it passes every gate, and each
  excluded row MUST carry one `reason`, its first failing gate in this order:
  `main-worktree`; `unsupported-path-bytes`; `registration-mismatch`;
  `locked-worktree`; its classification when not `merged-removable`;
  `not-requested` (an eligible row other than the named one in a
  single-target removal); `unstarted-branch` or `reflog-unavailable`;
  `deferred-target-cap`; `contains-submodule`; `hidden-local-state`. Traces:
  "Clean previews and applies a batch of eligible worktree removals in one
  repository"; design D10 and D12.
- **FR-021**: The `unstarted-branch` gate MUST read the branch's reflog for
  every row it checks, in every mode, from the filesystem (at most 64 KiB,
  counted in the filesystem budget, never by a Git child), because a head
  equal to the merge target's SHA does not by itself prove a branch
  unstarted. Its anchor MUST be the last surviving entry whose old object is
  all zeros, whatever command wrote it, or whose message begins
  `branch: Created from` or `branch: Reset to`; a movement MUST be an entry
  after the anchor, or any entry when no anchor survives, whose old and new
  objects are non-zero and differ. Unless FR-022 makes it
  `reflog-unavailable`, a branch with a movement MUST pass, its head equal to
  the merge target's SHA or not, and a branch whose anchor survives with no
  movement after it, the anchor's new object equal to its head, MUST be
  `unstarted-branch`.
  Traces: "Clean previews and applies a batch of eligible worktree removals
  in one repository"; "Clean can explicitly retire verified worktrees";
  design D10.
- **FR-022**: One outcome rule MUST govern that read: a reflog that is
  missing, empty (0 bytes) or read to its 64 KiB bound, whose surviving
  entries cannot decide, or whose last entry's new object is not the head
  MUST make the row `reflog-unavailable` at the gate's place; any other error
  on the read MUST make the row `inspection-error`; and a read not finished
  within the filesystem budget MUST leave the row unprobed and the plan
  incomplete with `inspection-incomplete`. Traces: "Clean previews and
  applies a batch of eligible worktree removals in one repository"; design
  D10.
- **FR-023**: Only rows that pass every earlier gate MUST be checked, inside
  their own worktree, for `contains-submodule` (any gitlink in the index, or
  a `modules` entry in the worktree's administrative directory) and
  `hidden-local-state` (any index entry flagged assume-unchanged or
  skip-worktree, sparse checkouts included). Traces: "Clean previews and
  applies a batch of eligible worktree removals in one repository"; "Cleanup
  preserves all local work not proven disposable".
- **FR-024**: `selected` and `excluded` MUST be in canonical order by raw
  path bytes, which is also the execution order. Once a plan is built, an
  incomplete plan MUST be refused first (a preview or report exits 1, and
  `--apply` refuses with exit 2 before any question), then an
  `--expect-plan` mismatch (`plan-digest-mismatch`, exit 2), and only then
  MUST a complete `--all-safe` plan that selects nothing print "No eligible
  worktrees" and exit 0 without asking; in single mode a P that a gate
  excludes MUST refuse with `target-excluded`, exit 2, never as an empty
  selection. Traces: "Clean previews and applies a batch of eligible
  worktree removals in one repository"; design D15.
- **FR-025**: `--apply` MUST always build, print and confirm its own fresh
  plan, and a preview MUST never be stored or reused. The plan MUST carry
  `plan_digest`, the lowercase hexadecimal SHA-256 of a canonical JSON text
  of the repository's four identity fields, the merge target's name and SHA
  and the selected `[path, branch, head]` triples in canonical order, so
  that a change to an excluded row leaves it unchanged; `--expect-plan D`
  MUST print the fresh plan and, when its digest differs from D, refuse with
  `plan-digest-mismatch`, exit 2, before any question or mutation. Traces:
  "Clean previews and applies a batch of eligible worktree removals in one
  repository".
- **FR-026**: A removal apply (`--all-safe` or `--action remove`) MUST be
  confirmed by one default-No question naming the count of worktrees to
  remove and of branches kept, ending `[yes/N]`, as fixed in `design.md`
  D18; only `yes`, surrounding whitespace ignored, MUST accept it, and any
  other answer MUST refuse with `cancelled`, exit 2. It MUST replace `Type
  yes to run this plan:` for that apply only, every other confirmation
  staying as it is, and `--yes` MUST accept the fresh plan without asking.
  Traces: "Clean previews and applies a batch of eligible worktree removals
  in one repository"; design D18.
- **FR-027**: `--apply --action remove --worktree P` MUST keep its flags and
  be a one-item batch: the same plan with `mode: "single"`, only P selected,
  every other eligible row `not-requested`, and the batch's sequence,
  refusal codes, stages and exit codes, the 16-target limit counting P
  alone. A P that matches no registry entry MUST refuse with
  `worktree-not-found`, and a P that a gate excludes with `target-excluded`,
  its `reason` the exclusion reason and its message the existing wording for
  the current worktree and for a class that is not removable. Every
  plan-blocking refusal, in either mode, MUST name a manual remedy (`git
  worktree prune`, `git worktree repair`, or removing the row by hand) as the
  cause fits. Traces: "Clean previews and applies a batch of eligible
  worktree removals in one repository"; "Clean can explicitly retire
  verified worktrees"; design D13 and D18.
- **FR-028**: The human preview MUST list the selected rows, then the
  excluded rows grouped by reason with each group's next step, an
  `ignored-local-files` row showing its bounded count and first ignored
  path, and a successful apply MUST print `Removed N; branches kept: ` and
  the branches kept. The preview, deferral and non-drain lines, the
  residual-window line, the question, the wait line, the success and stop
  lines, the partial-removal note, the next step for each reason and the
  refusal messages MUST read as `design.md` D18 fixes them, in ASCII.
  Traces: "Clean previews and applies a batch of eligible worktree removals
  in one repository"; design D18.
- **FR-029**: Each `project clean` invocation MUST set one monotonic deadline
  60 s after it starts and hold back a 10 s reconciliation reserve, so that
  work stops 50 s after start, both moving later by the time spent blocked at
  the confirmation question. Each Git child, and each filesystem call
  (`lstat`, `realpath`, and the reads of `.git`, `gitdir`, reflog and
  manifest files), MUST get `min(5 s, work remaining)` and be abandoned after
  it, recording `probe-timeout`, or `deadline-exceeded` where the deadline
  was the limit, and leaving its values null; probing MUST be serial; and
  reconciliation probes MUST get `min(5 s, reserve remaining)`. Traces:
  "Clean bounds its Git work and reports omitted work"; design D9.
- **FR-030**: The deadline MUST gate only the start of a removal: a removal
  child MUST be spawned only while at least 5 s of the work deadline
  remains, and otherwise that target and every later one MUST be
  `not-attempted` with `deadline-exceeded`; a removal still running at the
  deadline MUST be waited for, up to its 300 s ceiling, the reserve counting
  from its exit. A run with no removal in flight MUST end within 64 s of its
  start, not counting time blocked at the question (50 s of work, the 10 s
  reserve and up to 4 s to stop and reap a probe child), and a removal in
  flight MUST add at most 300 s, except while a filesystem call stuck in the
  kernel is outstanding. Traces: "Clean bounds its Git work and reports
  omitted work"; design D9.
- **FR-031**: The caps MUST be 128 worktree rows in `mode: "all-safe"` and
  `mode: "single"` and 256 in `mode: "report"`, every registry entry
  counting, the main worktree and missing rows included; 16 targets per run;
  and the ignored-file bounds of FR-057. The registry MUST be read
  completely, in one child, before any cap applies; rows MUST be ordered main
  worktree first, then by raw path bytes; and rows beyond the cap MUST be
  left uninspected and counted in `omitted: {count, exactness}`, `exactness`
  being `exact`. A plan MUST be incomplete, and apply refused, when the row
  cap is exceeded (`inspect-cap`), a repository-wide probe fails or a row is
  `inspection-error` (`inspection-incomplete`), or the deadline passes while
  planning (`deadline-exceeded`), except as FR-013 states for a named
  removal; a preview or report MUST exit 1 when its plan is incomplete and 0
  when it is complete, deferred rows included. Traces: "Clean bounds its Git
  work and reports omitted work".
- **FR-032**: When more than 16 rows pass every gate before
  `deferred-target-cap`, the first 16 in canonical order MUST go on to the
  two index gates and the rest MUST be excluded as `deferred-target-cap`
  with the command to run next; the plan MUST stay complete and apply
  allowed, and each re-run MUST take the next 16 with its own fresh plan and
  revalidation. Rows that an index gate then excludes MUST keep their places
  among the 16, and when all 16 are `contains-submodule` the human report
  MUST say why the deferred rows will not drain. A plan MUST NOT be refused
  for having more than 16 such rows, and `project clean` MUST NOT raise
  `target-cap`. Traces: "Clean bounds its Git work and reports omitted
  work"; design D12.
- **FR-033**: Plans and apply results MUST report `probes` and `operations`
  as `{estimated, performed}`, every Git child counted; `limits`
  (`worktree_rows`, the row cap of the plan's mode, `targets`,
  `ignored_entries`, `status_records` and `ignored_samples`); and `budget`
  (`probe_timeout_seconds` 5, `invocation_timeout_seconds` 60,
  `reconciliation_reserve_seconds` 10, `removal_floor_seconds` 5,
  `removal_ceiling_seconds` 300 and `probe_concurrency` 1). Revalidating one
  target MUST spawn at most five Git children and never recompute the full
  report, and the final rescan at most three. Traces: "Clean bounds its Git
  work and reports omitted work"; design D7.
- **FR-034**: The apply phase MUST begin when the question is answered `yes`
  or `--yes` is accepted, and each selected target MUST end in one stage
  with one reason from that stage's list: `removed` (null,
  `branch-advanced-after-removal`, `branch-missing-after-removal` or
  `removal-ceiling`); `refused` (`identity-changed`, `branch-changed`,
  `state-changed`, `contains-submodule` or `hidden-local-state`); `failed`
  (`git-refused` for exit status 128, `git-failed` for any other, or
  `spawn-error`); `unknown` (`unconfirmed-removal`,
  `reconciliation-incomplete`, `internal-error` or `removal-ceiling`); or
  `not-attempted` (`batch-stopped`, `interrupted` or `deadline-exceeded`).
  `pending` MUST appear only in the printed plan and progress. A child that
  exits nonzero on its own MUST be `failed` with Git's status whether or not
  a signal reached `project`, and only for a child killed at the ceiling, or
  whose exit could not be observed, MUST the rescan decide between `removed`
  and `unknown`. Traces: "Clean records a reconcilable result for every
  removal target"; design D19.
- **FR-035**: Every `removed`, `refused`, `failed` or `unknown` target MUST
  carry a `reconciliation` object (`registry_entry_present`, `path_present`,
  `branch_present`, `branch_sha`, `reconciled`) and a `not-attempted` target
  null, and the child's exit status alone MUST never prove a removal. The
  rescan MUST first re-establish the repository identity, every field null
  and `reconciled` false where it differs. A target's `notes` MUST list
  `orphaned-directory` when its registry entry is gone and its path remains,
  and `partially-removed`, with the recovery text, when a child killed at the
  ceiling, or whose exit was not observed, left its registry entry or path.
  Traces: "Clean records a reconcilable result for every removal target".
- **FR-036**: Before the apply phase, SIGINT, SIGTERM or SIGHUP MUST terminate
  and reap every probe child, print "Cancelled." on standard error and no
  JSON document, and exit 130, 143 or 129 with nothing mutated; end of input
  at the question MUST exit 130 the same way. During it, the first such
  signal MUST set the exit status and stop scheduling: a removal in flight is
  waited for and ends by the stage rule of FR-034, targets not yet started
  are `not-attempted` with `interrupted`, and `project` reconciles within the
  reserve and prints the record, on a best-effort basis after SIGHUP; a
  second SIGINT during reconciliation MUST abandon the remaining rescans,
  leaving their fields null. An exception after the apply phase began MUST
  make that target `unknown` with `internal-error` and later targets
  `not-attempted`, and one before it MUST refuse with `internal-error`, exit
  2. An `unknown` or `failed` target MUST NOT be retried automatically, and
  `project` MUST never force a removal or delete a directory itself. Traces:
  "Clean records a reconcilable result for every removal target"; design
  D15.
- **FR-037**: A run with `--apply` MUST exit with the first matching row: 130,
  143 or 129 when a signal was received, the first deciding, or 130 when
  input ended at the question; 1 when the deadline stopped work after the
  apply phase began, any target is `unknown`, or any target's reason is
  `removal-ceiling`; Git's own status, passed through unchanged even when it
  equals one of `project`'s own, when a target is `failed` with
  `git-refused` or `git-failed`; 2 for any refusal, a `refused` target, a
  `removed` target with a branch-after-removal reason, or a `failed` target
  with `spawn-error`; 0 when every selected target is `removed` with reason
  null, or nothing is eligible. A preview or report MUST exit 2 only for a
  refusal raised before a plan is built, 1 for an incomplete plan and 0
  otherwise, the signal exits excepted. Traces: "Clean records a
  reconcilable result for every removal target"; design D19.
- **FR-038**: A run that stops MUST end its human result with the stop block,
  `Stopped at P (reason). Removed k of n. Not attempted: ... Next: `
  followed by the command that shows a fresh read-only plan, and MUST name
  every retained branch. Traces: "Clean records a reconcilable result for
  every removal target"; design D18.
- **FR-039**: Every Git output that carries a path MUST be read
  NUL-delimited, and a code point MUST be escaped when its Unicode general
  category is Cc, Cf, Zl or Zp. In JSON, a path that is valid UTF-8 MUST be
  an ordinary string, exact after unescaping, with every such code point
  written as a JSON escape and `path_valid_utf8: true`; a path that is not
  valid UTF-8 MUST be written with each undecodable byte as `\xHH` in
  lowercase hexadecimal and each literal backslash doubled, with
  `path_valid_utf8: false`, and its row MUST be excluded as
  `unsupported-path-bytes` and never be a removal operand. Traces: "Clean
  reports every path exactly or excludes it".
- **FR-040**: Every path value in JSON MUST carry its validity flag beside
  it: `path_valid_utf8` on every object with a `path` (worktree rows;
  `selected`, `excluded` and apply-result `targets` entries; refusals and
  row errors); each `ignored_samples` entry an object `{path,
  path_valid_utf8}`, its path relative to its worktree; and
  `root_valid_utf8` and `common_dir_valid_utf8` in `repository`, always true
  in `project clean`. Traces: "Clean reports every path exactly or excludes
  it"; design D7.
- **FR-041**: Human output MUST print a path verbatim in prose and with POSIX
  shell quoting in commands, unless it holds a code point to escape or an
  undecodable byte; such a path MUST print in the `$'...'` form in prose and
  commands alike (`\xHH`, `\uXXXX`, or `\UXXXXXXXX` above U+FFFF, in
  lowercase hexadecimal, each backslash doubled and each single quote as
  `\'`), sample paths included. A `repository.root` or `common_dir` that is
  not valid UTF-8 MUST refuse with `unsupported-path-bytes`, exit 2, before
  any plan or digest is built. Traces: "Clean reports every path exactly or
  excludes it".
- **FR-042**: Every `project clean --json` MUST print one JSON document with
  `schema_version: 1`: the plan envelope when a plan is built, with the
  fields the delta lists and `mode` being `report`, `single` or `all-safe`;
  otherwise the existing `{"error": ...}` object extended with `code`,
  `schema_version`, `observed_at`, `mode`, `repository` and `merge_target`
  (each null unless established), `completeness: "incomplete"`,
  `apply_allowed: false` and `refusals`. Baseline keys MUST keep their names
  and types; `root` naming the command directory, `ignored_files` counting
  the entries observed and `present` possibly null are the changes of
  meaning this version records; and worktree rows MUST add `locked`,
  `ignored_files_truncated`, `ignored_samples`, `path_valid_utf8`, `errors`
  and `notes`. Traces: "Clean plans and refusals are versioned JSON".
- **FR-043**: Refusals and row errors MUST be `{code, message, path?,
  path_valid_utf8?, reason?}` objects with a stable kebab-case `code` from
  the eighteen refusal codes the delta lists, and plan, target and row notes
  MUST use only the codes the delta lists for each. A resolve refusal MUST
  print the extended error object, and a plan or select refusal the plan with
  `apply_allowed: false`. Null MUST mean unknown or not established, never a
  default false or 0, in every field this change adds; enums MUST be closed
  within a schema version; and a rename, removal, type change or change of
  meaning MUST increment `schema_version`. Traces: "Clean plans and refusals
  are versioned JSON".
- **FR-044**: `--apply --json` MUST be accepted with `--all-safe` and with
  `--action remove` only, and MUST print exactly one document on standard
  output: the plan envelope or the extended error object when the run stops
  before the apply phase, and otherwise the apply result record with the
  fields the delta lists, while the human plan, the question and progress go
  to standard error. Only an argument-parser usage error, and SIGINT, SIGTERM
  or SIGHUP before the apply phase or end of input at the question, MUST
  print no JSON document. Traces: "Clean plans and refusals are versioned
  JSON".
- **FR-045**: Cleanup MUST treat as preservation or review states, and MUST
  NOT offer destructive removal for, ignored local files, dirty work,
  detached state, an unknown default branch, remote divergence, the main
  worktree, a locked worktree, `contains-submodule`, `hidden-local-state`,
  `registration-mismatch`, `unsupported-path-bytes`, `unstarted-branch`,
  `reflog-unavailable` and `inspection-error` (a path that cannot be read or
  state that could not be established). A value that is not established MUST
  be null, never false or 0, and MUST keep its row out of every removal.
  Traces: "Cleanup preserves all local work not proven disposable".
- **FR-046**: Cleanup MUST re-inspect the selected target after confirmation
  and before a push, worktree removal or local branch deletion, and refuse
  when its state no longer matches the reviewed plan; for a removal, that
  MUST hold at the revalidation immediately before each spawn. A removal
  MUST be revalidated by a targeted check, never the full report, of at most
  five Git children, a fresh manifest read and the `modules` check, in the
  delta's order and stopping at the first difference, comparing the recorded
  repository identity, the target's worktree identity and two-way
  registration, its branch evidence, every baseline signature field, its
  `locked` flag, the manifest's `tracking_branch` and the merge target
  re-resolved from the fresh read. Traces: "Cleanup revalidates destructive
  actions"; design D7.
- **FR-047**: A difference MUST refuse the target, spawn nothing, attempt no
  later target and exit 2, with `identity-changed` (an identity or
  registration difference, or a missing registry entry), `branch-changed` (a
  different branch name or head), `state-changed` (any other signature, lock,
  manifest or merge-target difference), `contains-submodule` or
  `hidden-local-state`. A value null in the plan and null at revalidation
  MUST NOT count as a difference, and a value that cannot be re-read, a
  timed-out filesystem call included, MUST. The first target's
  repository-wide checks MUST serve as the preflight of every target. Push
  and branch deletion MUST keep the full re-inspection and refuse with
  `inspection-incomplete`, `inspect-cap` or `deadline-exceeded`, exit 2,
  when it is incomplete. Git's own non-force check MUST be the last defense
  only on the removal command's pinned status configuration, the protocol
  pins being no part of it. Traces: "Cleanup revalidates
  destructive actions"; design D7.
- **FR-048**: Concurrent writers MUST be outside the safe contract, and
  cleanup MUST claim no lock, lease or writer-quiescence handoff. Its one
  guarantee MUST be that a removal child is spawned only if, at the
  revalidation immediately before it, every value FR-046 compares, the
  absence of submodules and of hidden local state in the target's own index
  included, equals the confirmed plan's. Ignored files created and index
  flags set after that revalidation, and any change after Git's own check,
  MUST be outside the contract, and the confirmation and the result MUST each
  state that residual window in one line. Traces: "Cleanup states a narrow
  guarantee and its residual window"; design D7.
- **FR-049**: Cleanup MUST never delete a branch, so that a branch race loses
  no commit: a branch change seen at revalidation refuses with
  `branch-changed`, and one seen only by the rescan after Git removed the
  worktree MUST leave the target `removed` with
  `branch-advanced-after-removal` or `branch-missing-after-removal`, stop the
  run and exit 2. A repository found replaced by the rescan after a removal
  MUST make that target `unknown` with `unconfirmed-removal`, every
  reconciliation field null and `reconciled` false, and stop the run with
  exit 1. Traces: "Cleanup states a narrow guarantee and its residual
  window".
- **FR-050**: Status and doctor MUST keep their human and JSON reports for
  single repositories, project manifests, families, worktrees and local
  tooling, show missing or malformed state, and never fetch, reset or
  bootstrap. They MUST inspect Git repositories through the evidence model
  and MUST NOT refuse for Git's version or for a repository they cannot
  inspect: doctor MUST report an old, missing or unusable Git as an `error`
  check row naming `git-too-old` or `git-unavailable`, keeping its exit rule
  for error rows; status MUST mark each root, leg or worktree row it cannot
  inspect `inspection-error`; a directory with no `.git` MUST keep `present:
  false` with no version check; and a root or leg whose state cannot be
  established, a failed or timed-out status probe included, MUST be a
  row-level `inspection-error`, never an exit 2. Traces: "Inspect and
  diagnose"; design D16.
- **FR-051**: In status and doctor JSON, which stays unversioned, a root or
  leg that could not be inspected MUST carry `classification:
  "inspection-error"` and an `errors` list of refusal-shaped objects, with
  every value not established null. Doctor MUST render as an `error` check
  row every null that means "not established" (a null `present`, a `dirty`
  left null by a failed or timed-out probe, any `inspection-error` row) and
  never one that means "none" (`upstream`, `ahead` and `behind` without an
  upstream, `merged_into_target` for a detached head). A branch whose
  upstream's remote-tracking ref was deleted MUST show its configured short
  name as `upstream`, with `ahead` and `behind` null, and every path value
  MUST carry its validity flag as FR-040 states, with `root_valid_utf8`
  beside the top-level `root` and each nested family member's `root`.
  Traces: "Inspect and diagnose"; design D16.
- **FR-052**: Update MUST report local tracking state and named owning
  commands by default, and applying it MUST require a component and
  confirmation, preserve failures and reject dirty project state for
  project-modifying delegates: `--component shape` or `--component bench`
  MUST refuse unless the root's and every child's `dirty` are exactly false,
  a null `dirty` refusing as dirty work does and the owner tool never
  invoked, while `--component tools` or `--component workflow` MUST NOT
  require Git. Traces: "Explicit maintenance"; design D16.
- **FR-053**: Every subcommand that inspects a Git repository MUST use one
  evidence model, running `git --version` once per invocation and inspecting
  no repository with a Git older than 2.36 (`git-too-old`) or a `git` that is
  missing, fails, times out or prints an unparseable version
  (`git-unavailable`); whether it then refuses or reports is its own
  requirement's rule (FR-002, FR-050). Traces: "Repository inspection
  requires Git 2.36 and shares one evidence model"; design D17.
- **FR-054**: Every Git child MUST run in its own process group with the
  seventeen variables the delta lists removed from its environment,
  unconditionally and from a fixed list never queried from Git (the fifteen
  that `git rev-parse --local-env-vars` prints on Git 2.40 and later,
  `GIT_INTERNAL_SUPER_PREFIX` and `GIT_ALLOW_PROTOCOL`); read-only probes
  MUST set `GIT_OPTIONAL_LOCKS=0`; every status probe MUST pin
  `core.untrackedCache=false` and `core.fsmonitor=false`; and every Git
  child, of every kind, MUST pin `protocol.allow=never` and the six
  per-protocol `allow=never` settings (`file`, `ssh`, `git`, `http`, `https`
  and `ext`), so that a lazy fetch in a partial clone fails locally and its
  row is `inspection-error`, never a network call. Traces: "Repository
  inspection requires Git 2.36 and shares one evidence model"; design D6 and
  D11.
- **FR-055**: A worktree probe MUST run in that worktree, against its own
  index, only after its identity was verified immediately before;
  repository-wide probes MUST run in the main worktree, except the identity
  probe, which runs where the argument resolves, and the registry listing
  while the main worktree is not yet known. A repository MUST be identified
  by `{root, common_dir, dev, ino}` and a worktree by `{path, dev, ino,
  admin_id}`, its registration checked in both directions between
  realpaths; a row whose registration disagrees MUST get no status probe and
  be `inspection-error`; an `lstat` that fails because the path does not
  exist MUST give `present: false`, and any other failure `present: null`,
  an `os-error`, `inspection-error` and no probe. Traces: "Repository
  inspection requires Git 2.36 and shares one evidence model"; design D6 and
  D7.
- **FR-056**: Once per common directory, the model MUST run the identity
  probe, the registry listing, one ref listing over local and
  remote-tracking refs carrying each ref's name, object, symref, upstream,
  upstream short name and track, and the merged set of local branches
  against the merge target's SHA; and for each present, registration-verified
  row, the main worktree's included, one combined status probe listing
  untracked and matching ignored entries. Every path-carrying output MUST be
  parsed NUL-delimited. A branch whose upstream's remote-tracking ref is
  missing MUST get `upstream` set to the configured short name,
  `remote_present` false and `ahead` and `behind` null. Traces: "Repository
  inspection requires Git 2.36 and shares one evidence model"; design D6.
- **FR-057**: The combined probe MUST set `dirty` true once a non-ignored
  record arrives, and false once an ignored record arrives first or an empty
  stream ends normally; it MUST stop reading, and stop the child, at the 65th
  ignored record or the 4,097th record of any kind, a stop at the bound being
  a complete outcome, never `probe-failed`. `ignored_files` MUST count the
  ignored records read, a lower bound when `ignored_files_truncated` is true,
  and `ignored_samples` MUST hold at most 8, both null when the probe did not
  run or failed; a stream stopped before any ignored record MUST leave
  `ignored_files` null with `dirty` true; and a probe that fails or times out
  before `dirty` is established MUST leave it null, record `probe-failed`,
  `probe-timeout` or `deadline-exceeded`, and make the row
  `inspection-error`. Traces: "Repository inspection requires Git 2.36 and
  shares one evidence model"; design D2.
- **FR-058**: Each Git child's standard output MUST be read as it streams,
  and its standard error drained at the same time and capped. A child stopped
  at its bound, past its budget or by a signal MUST receive SIGTERM to its
  process group, SIGKILL 2 s later, and a reap wait of at most a further 2 s,
  after which it is abandoned and its row recorded `probe-timeout`. On every
  exit path, exceptions and signals included, a subcommand MUST kill the
  process groups of the probe children it started, and MUST instead wait for
  a removal child, never signalling it before its 300 s ceiling. Traces:
  "Repository inspection requires Git 2.36 and shares one evidence model";
  design D1 and D2.
- **FR-059**: Under an invocation deadline, as `project clean` has, each Git
  child MUST get `min(5 s, work remaining)`; without one, as in status,
  doctor and update, each Git child MUST get 15 s, and those subcommands MUST
  have no invocation deadline and no row cap, a row whose probe is unreadable
  or times out showing as `inspection-error`. Children other than Git MUST
  keep 15 s. Traces: "Repository inspection requires Git 2.36 and shares one
  evidence model".
- **FR-060**: Every subcommand that resolves a merge target from a project
  manifest MUST read at most 1 MiB of it, detecting a larger manifest from
  its size before the read and treating it as `manifest-invalid`; the
  manifest reads that status, doctor and update make for a project's kind
  and legs stay as they are. Traces: "Repository inspection requires Git
  2.36 and shares one evidence model"; design D8.
- **FR-061**: Values MUST equal those of the inspection this model replaces,
  except where a requirement states a change. Traces: "Repository inspection
  requires Git 2.36 and shares one evidence model"; design D6.
- **FR-062**: Output parsing MUST yield the same records and the same bound
  whether a recorded stream is fed one byte at a time or whole, and the
  bounded handling of Git children MUST let a caller run several of them at
  once through the same environment scrub, termination path and parsers, so
  that `add-project-overview`'s feature reuses it rather than a second copy.
  Traces: design D2; clarifications N2.
- **FR-063**: The rules the change keeps MUST hold: one repository per
  invocation; nothing removed unconfirmed; local evidence only, remote
  evidence never proving a removal; the current worktree and the main
  worktree never removed; and `project` never running `git worktree prune`,
  `repair`, `lock` or `unlock`, leaving an orphaned directory for the person
  to inspect, while a refusal may name those commands as the person's own
  remedy. Traces: proposal, "Rules This Change Keeps"; "Cleanup protects the
  process worktree" (unchanged by the change).
- **FR-064**: The feature MUST add no flag outside `clean`, no network access
  and no new dependency; MUST leave `new`, `benches` and every confirmation
  other than FR-026's unchanged; and MUST keep running on every runtime
  version the README supports and CI runs. Traces: proposal, "Impact" and
  "Corrections to the Packet" (C4); design, "Goals / Non-Goals".
- **FR-065**: The README's "Clean up Git worktrees" section MUST open with
  the five behaviour changes users will notice: plain `project clean`
  exiting 1 on an incomplete report; `clean` refusing below Git 2.36;
  `--worktree P` refusing a freshly created merged worktree as
  `unstarted-branch`, and one whose reflog keeps no decisive entry as
  `reflog-unavailable`, each with its remedy; and `--worktree P` removing a
  merged worktree whose upstream was deleted, its branch kept. It MUST then
  describe the preview and apply, `--expect-plan`, the gates, the 16-per-run
  deferral, the narrow guarantee and residual window, the result record and
  recovery, and the advice to close sessions before a batch apply; correct
  "Apply actions are always explicit and target one branch or worktree";
  state the Git 2.36 requirement under Install; and add `clean`'s 1 for an
  incomplete preview, 143, 129 and Git's status passing through to its
  exit-code line. Traces: proposal, "Impact" (`README.md`); design D3 and
  "Migration Plan".
- **FR-066**: Automated tests over disposable repositories MUST cover every
  delta scenario with at least one test named after it, using a counting
  `git` wrapper that records each child's arguments and directory, the fake
  Gits of `design.md` D1, hooks for the residual window, the branch race,
  deadline expiry and signals, the parser feeds of FR-062, and value-parity
  checks against the baseline. Every existing test MUST keep passing
  unchanged except `test_clean_revalidates_a_worktree_after_confirmation`,
  which moves to the result record (a `refused` target with `state-changed`,
  exit 2). Non-UTF-8 path tests MUST run on Linux and be skipped on macOS
  with that reason, and ordering tests MUST use names that differ by more
  than case. Traces: proposal, "Impact" (tests); design D20 and "Migration
  Plan".
- **FR-067**: CI MUST gain a job that builds the floor Git version, 2.36,
  cached, and runs the `clean`, `status` and `doctor` tests with it first on
  PATH, beside the existing jobs. Traces: design D17.

### Key Entities *(include if feature involves data)*

- **Plan**: what one invocation would do in one repository, in `mode`
  `report`, `single` or `all-safe`: the repository identity, the merge
  target, the worktree rows, `selected`, `excluded` (one reason each),
  `omitted`, `notes`, completeness, `apply_allowed`, `plan_digest`,
  `limits`, `budget`, `probes` and `operations`. Built fresh by every run and
  never stored.
- **Worktree row**: one registry entry, the main worktree included: its path
  and validity flag, presence, branch evidence (`branch`, `head`,
  `upstream`, `upstream_oid`, `ahead`, `behind`), `dirty`, ignored-file
  count, truncation flag and samples, `locked`, one of fifteen
  classifications, `errors` and `notes`.
- **Gate**: an eligibility test in the fixed order of FR-020; the first one a
  row fails is its exclusion `reason`.
- **Repository identity** and **worktree identity**: `{root, common_dir, dev,
  ino}` and `{path, dev, ino, admin_id}` with two-way registration, recorded
  in the plan and compared at revalidation and at the rescan.
- **Merge target**: `{name, source, sha}`, the local branch whose ancestry
  proves a worktree's branch merged.
- **Reflog anchor and movement**: a branch's last creation or reset entry,
  and a later entry that moved the branch; together they decide
  `unstarted-branch`.
- **Target result**: one selected worktree's outcome: stage, reason, notes,
  command, exit status, probes performed and reconciliation record.
- **Reconciliation record**: what the rescan found: registry entry present,
  path present, branch present, branch SHA, and whether it reconciled.
- **Apply result record**: the run's JSON result: repository, merge target,
  plan digest, probes, operations, targets, exit code and completeness.
- **Refusal**: `{code, message, path?, path_valid_utf8?, reason?}` with a
  stable code; row errors have the same shape.
- **Residual window**: the changes the narrow guarantee does not cover,
  stated in one line at the confirmation and in the result.
- **Evidence model**: the bounded set of Git children and filesystem reads,
  shared by `clean`, `status`, `doctor` and `update`, from which every row's
  values come.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A person retires up to 16 merged, clean worktrees of one
  repository with one apply run and one confirmation (or one `--yes`), where
  today each worktree takes its own run and confirmation; twenty such
  worktrees take two runs, 16 and then 4.
- **SC-002**: No removal falls outside the plan: in every test run, every
  worktree removed is in the `selected` list of the fresh plan that run
  confirmed, and 0 excluded, not-requested, deferred or not-attempted
  worktrees and 0 local branches are removed or moved by the command.
- **SC-003**: No probe makes a network call: in every status probe run in a
  partial clone whose upload-pack logs each run, the log records 0 runs,
  with or without `GIT_ALLOW_PROTOCOL=file` in the caller's environment and
  `protocol.file.allow=always` in the repository's configuration, and a
  counting wrapper finds the protocol pins on 100% of Git children.
- **SC-004**: Every `project clean` run with no removal in flight ends within
  64 s of its start, not counting time blocked at the question; a removal in
  flight adds at most 300 s; no removal starts with less than 5 s of the
  50 s work deadline left; and no probe child is waited for more than 4 s
  past its budget (2 s grace, then at most 2 s of reaping).
- **SC-005**: Each Git child gets at most `min(5 s, work remaining)` under
  `clean`'s deadline, each reconciliation probe at most `min(5 s, reserve
  remaining)`, and each Git child of `status`, `doctor` and `update` 15 s.
- **SC-006**: No plan inspects more than 128 worktree rows in a batch or a
  named removal (P aside) or 256 in a plain report; no run removes more than
  16 worktrees; each target's revalidation spawns at most 5 Git children and
  the final rescan at most 3; and `probes.performed` equals a counting
  wrapper's count in every apply.
- **SC-007**: Every selected target of every apply ends in exactly one of
  the five stages with a reason from that stage's list; 100% of `removed`,
  `refused`, `failed` and `unknown` targets carry a reconciliation record;
  and 0 targets are reported `removed` on an exit status alone.
- **SC-008**: Every run's exit status is the first matching row of FR-037,
  and every preview or report exits 0, 1 or 2 by completeness.
- **SC-009**: In 100% of `project clean --json` runs other than the
  exceptions of FR-044, standard output parses as exactly one JSON document
  with `schema_version: 1`; every valid UTF-8 path round-trips exactly, and
  every other path carries `path_valid_utf8: false` and reaches no removal.
- **SC-010**: Human output from a path contains 0 raw characters of general
  category Cc, Cf, Zl or Zp and 0 undecodable bytes, and every new line
  matches `design.md` D18 character for character, in ASCII.
- **SC-011**: The 10 canonical scenarios that the modified requirements keep
  stay byte-identical in `openspec/specs/` after the change is archived, and
  pass, as do the scenarios of every requirement the change leaves
  untouched.
- **SC-012**: Each of the 100 delta scenarios has at least one automated test
  named after it; every test on main at `961c405` (96 tests) keeps passing,
  unchanged except the one moved to the result record; and the four CI jobs
  and the Git floor job stay green.
- **SC-013**: `status`, `doctor` and `update` exit 2 in 0 runs because of
  Git's version or a repository they cannot inspect; doctor exits 1 on its
  error row; and a fresh project with no remote still passes doctor.
- **SC-014**: A reader of the README's "Clean up Git worktrees" section alone
  can name the five behaviour changes, how to preview, confirm and pin a
  preview's digest, why a row was kept, and what to run after a stopped
  batch.

## Assumptions

- The spec names flags, refusal and reason codes, JSON fields, Git settings,
  standard streams and exit statuses because the ratified deltas fix them as
  behaviour, which outranks the template's advice to stay
  technology-agnostic, as in features 002 and 003. Its readers own, review
  and use `project` and the tools that read its JSON.
- `.specify/memory/constitution.md` is still the unfilled template, so the
  ratified change alone governs this feature.
- No clarification marker is used: the change is exhaustively specified.
  Open question 2, squash-merged branches, is deferred to a follow-on change
  and changes nothing built here; the V5 deferral (`design.md` D12) and the
  Git 2.36 floor kept with one more scrubbed name (R-21, `design.md` D17)
  were before Brett Heap at ratification and stand as ratified.
- The caps and budgets stand as measured by governance task 2.1, and the
  2.36 floor as verified by task 2.2 on Git 2.36.6, 2.40.4 and 2.43.0. Their
  results are posted on PR #11, task 2.1 at
  https://github.com/opensoft/openRepoProject/pull/11#issuecomment-6086983930
  and task 2.2 at
  https://github.com/opensoft/openRepoProject/pull/11#issuecomment-6082230232.
  drvfs was unmeasured, and the two degraded cases are edge cases, not cap
  changes.
- The change pins its code and test citations at `da33d92` and `7a9134b`.
  Feature 003 has since changed `project` and the tests (`f401e06`), so the
  plan re-pins every citation against the `main` of its day; this spec cites
  no line numbers.
- "Every existing test" means the suite on `main` when the feature is
  implemented: 94 tests at `7a9134b`, 96 at `961c405` after feature 003's
  two. The change's exception list (one test moved to the result record,
  three message tests passing unchanged because `target-excluded` and
  `no-merge-target` keep the baseline wording) applies to it unchanged.
- Exact wording is cited from `design.md` D18 and D14 and never changed
  here; the texts quoted in this spec are verbatim from the deltas or D18,
  except the README sentence FR-065 corrects, quoted from the proposal.
- Concurrent writers are outside the contract by design; the README's advice
  to close sessions before a batch apply is the only mitigation for a live
  session (`design.md` D3).
- workBenches' `onp` carries the batch only after workBenches moves its
  pinned `project` artifact, on its owner's act; this feature edits nothing
  in workBenches (proposal, "What This Repository Does Not Own").

## Dependencies

- **Feature 001** (`specs/001-project-command/`) and the `a040790` baseline
  (PR #1): the `project` command whose `clean`, `status`, `doctor` and
  `update` this feature changes. `clean` came from the archived change
  `add-project-clean-command`, which had no Speckit feature; its canonical
  specs `project-clean` and `project-clean-review-safety` are what the
  deltas modify.
- **Feature 002** (`specs/002-triad-first-project-new/`, PR #8, `d7f6b0e`):
  this feature builds on its `project` and tests and leaves its six
  creation requirements and the MODIFIED "Delegate project creation"
  untouched.
- **Feature 003** (`specs/003-parent-obstacle-wording/`, PR #17, `f401e06`)
  and lane openRepoProject-1's change `fix-parent-obstacle-wording`, archived
  on 2026-10-09 (`d81bf8d`): it modified "Known Triad obstacles are named
  before the question and refused on a Triad answer", which this change
  leaves untouched. It edited the same files and landed first, so this
  branch, cut from a `main` that holds it, carries it, and takes later
  `main` by merge, never by rebase; its tests join the suite this feature
  keeps passing.
- **The sibling change `add-project-overview`** (issue #10, PR #12), on
  `main` at `961c405`, depends on this one: its `--all-safe` suggestion
  exists through this change's gates and refusal codes, and it reuses the
  evidence model, the bounded child handling (FR-062), the ladder function
  and the Git 2.36 refusal; `target-cap` survives only as its limiting gate
  reason. It reconciles against this change's final requirement headers
  after this lands (task 2.3, governed by that change's own record), and its
  feature `005-project-overview` follows only after this feature merges.
- **Governance**: tasks 1.1 to 1.6, 2.1 and 2.2 of the change are done; the
  Speckit handoff in its `tasks.md` names this feature.
- **Runtime and CI**: Git 2.36 or later where `project` inspects a
  repository; a Git 2.36 build for the CI floor job; the existing four CI
  jobs (Linux and macOS, two runtime versions each).

## Out of Scope

As the change defers it (proposal, "Out of Scope"; design, "Goals /
Non-Goals"):

- Paired retirement, deleting a branch with its worktree: a future MODIFIED
  "Clean can explicitly retire verified worktrees".
- Cache disposal, the first follow-on change.
- Patch-equivalence retirement of squash-merged branches (open question 2),
  a follow-on change.
- Remote, GitHub and pull-request queries; family traversal and
  relationships; bench, container and park integrations.
- `project overview`, `--attention` and the doctor repository-health
  absorption, which belong to `add-project-overview`.
- Estate-wide destructive batches, merge or branch reconciliation, a lock or
  writer-quiescence protocol, a persistent cache or resumable plan,
  continuing after a failure, and the exact bench or type doctor check.
- Bare-repository support, user-configurable limits, and an `in-use` gate.
- Any change to `new` or `benches`, or to the confirmation that `new`,
  `update` and `clean`'s push and branch deletion use; bounding push and
  branch-deletion children; versioning the JSON of `status` and `doctor`; a
  doctor health section.
- The requirements and capabilities the change leaves untouched ("Cleanup
  protects the process worktree", "Cleanup respects configured upstream
  mappings", "Delegate project creation", "Distribution and compatibility",
  the six creation requirements, `project-review-safety` and
  `speckit-extension-integration`), the installed artifact's pin in
  workBenches, openRepoShape and setup-openspeckit.
