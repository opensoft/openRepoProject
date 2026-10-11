Lane: openRepoProject-5

# Design

## Context

See `proposal.md` for why and what, and the deltas under `specs/` for the
requirements. The packet's paired-retirement contract (`BA:1339-1345`) maps to
these decisions: the separate post-removal stage to D2; the immediate
branch-head and local-ancestry check with the reconciliation record's
`branch_sha` as the expected head to D3 and D4; "a changed head or a Git
refusal retains the branch, stops later targets, and reports the already
removed worktree plus the surviving branch" to D5 and D6; the `delete-branch`
retry path to D8; and "No future composite operation may force-delete or
force-push" to D3. The seam rule (`BA:1318-1322`: inside `retire_worktree`,
under the same deadline, stage values of its own, mutations counted in
`operations`) maps to D2, D5 and D7. The lane's rulings map as follows: A-1 to
D1; A-2 to D3, with D4 reading its ancestry clause; A-3 to D4; A-4 to D5 and
D6; A-5 to D7; A-6 to D8; A-7 to D9; L-4 to D5 and D10; L-1, L-5 and L-7 to
the Migration Plan. No alignment review or council has run yet, so no NOTED
constraint exists for a decision to answer.

Citations follow `proposal.md`: packet files at `da33d92`, `CAS` for change 1,
`APO` for change 2, `project:N` and `tests:N` at `961c405`.

What in `project` shapes the approach:

- `clean()` (`project:669-743`) handles `remove` at `project:707-722` and
  `delete-branch` at `project:723-735`. The latter refuses the default branch
  (`project:727-728`), refuses "Remove the linked worktree first; branch
  deletion is a separate action." while a present worktree holds the branch
  (`project:729-730`), requires ancestry (`project:731-732`), and runs `git -C
  root branch -d <branch>` (`project:734`) through `execute()`
  (`project:157-162`, unbounded, a signal death mapped to 128 plus its
  number), after `confirm()` (`project:152-154`).
- `require_unchanged_cleanup_state()` (`project:656-666`) re-reads, for
  `delete-branch`, the branch head and its ancestry after confirmation
  (`project:658-663`); the stage's re-read is that check, narrowed to one
  listing.
- `ancestor()` (`project:537-541`) spends one `merge-base --is-ancestor` child
  per call; the stage needs none (D4).
- `probe()` (`project:60-65`) sets `GIT_OPTIONAL_LOCKS=0` for read-only
  children; the branch child writes, so it is not one of those.
- The parser's `clean` flags (`project:1109-1117`) gain `--retire-branches`.
- Feature 004 (its `plan.md` on branch `004-project-clean-all-safe` at
  `dd923ee`, slices 2 and 6) builds what the stage stands on: the child handle
  (`start`, `terminate_group`, `reap`), `run_bounded`, the scrub and the pins,
  the narrowed ref listing of revalidation and rescan, the seam
  `retire_worktree(plan, target)` and the result record. The stage is a tail
  of that seam.
- `tests:857-878`, `test_clean_removes_only_merged_worktree_and_keeps_branch`,
  removes a worktree, sees its branch kept, then deletes it with
  `delete-branch`: the default path and the retry path in one test, kept
  unchanged.

Facts checked for this design on Git 2.43.0, in a scratch repository with a
bare remote, `GIT_CONFIG_NOSYSTEM=1` and an empty global configuration:

| Probe | Observed |
| --- | --- |
| `git branch -d -- <b>` on a merged branch | deletes it, exit 0, and removes its `branch.<b>` configuration section and its reflog `logs/refs/heads/<b>` |
| `git branch -- -x` | refused as not a valid branch name, exit 128: `git branch` creates no name beginning with `-` |
| `git branch -d b` while another worktree has `b` checked out | refused, "cannot delete branch 'b' used by worktree at ...", exit 1 |
| `branch -d` on a branch equal to its live upstream, the command directory's `HEAD` on another branch that lacks it | deletes, with the warning "deleting branch 'c' that has been merged to 'refs/remotes/origin/c', but not yet merged to HEAD", exit 0 |
| `branch -d` on a branch whose upstream's remote-tracking ref was deleted, the command directory's `HEAD` on another branch that lacks it | refused, "the branch 'd' is not fully merged", exit 1; run with `HEAD` on the merge target it deletes, exit 0 |
| a `reference-transaction` hook during `branch -d` | runs; for a loose and for a packed ref, every line it reads carries an all-zeros old value, so Git deletes without comparing the ref to the value its own check read |
| the same hook during `git update-ref -d refs/heads/<b> <sha>` | reads the SHA as the old value; with a wrong SHA the command refuses, "cannot lock ref ... is at X but expected Y", exit 1, and the ref stays |

The Git 2.36 floor was not available for these checks here; D9 puts them on
change 1's CI floor job.

## Goals / Non-Goals

**Goals:**

- One opt-in branch stage per removed target, inside the seam feature 004
  builds, meeting `BA:1339-1345` whole (D2, D3, D4).
- An evidence-decided outcome per branch, in a sub-record that leaves every
  change 1 enum as it is (D5, D10).
- A stop rule and exit status ordered inside change 1's table (D6), bounds
  that keep its 64 s run bound (D7), and fixed human text pinned by tests (D8,
  D9).

**Non-Goals:**

- Any change to a run without the flag, to the explicit `delete-branch`
  action, to `push`, to the preview, to the gates or the ladder, to
  `plan_digest`, or to the overview.
- Bounding the explicit `delete-branch` child, remote branch deletion,
  squash-merge retirement, and any lock.

## Decisions

### D1. The flag and its argument rules (A-1)

`--retire-branches` is a `store_true` flag of `clean`. `clean()` checks it with
change 1's other argument combinations, before resolution builds a plan:
accepted only with `--apply` and either `--all-safe` or `--action remove`;
otherwise the `invalid-arguments` refusal, exit 2, with the extended error
object under `--json`. A preview cannot carry it, so the preview, its digest and
`--expect-plan` stay change 1's; the flag changes no selection, so the digest
leaves it out. Under the flag the plan's `operations.estimated` and
`probes.estimated` count the stage (D7), and the plan text and question name the
branches (D8); no plan field records the flag.

Alternatives rejected: deletion by default for `remove`, as `5fc2b51` did,
because the packet keeps "implicit local branch deletion" a non-goal
(`OV:150-152`); a new action such as `--action remove-and-delete-branch`,
because the batch takes no `--action` (`CAS/pc:571-574`) and one flag serves
both forms; and a preview form, because it would make the advisory preview
differ by a flag that changes no selection.

### D2. Where the stage runs

`retire_worktree(plan, target)` keeps change 1's sequence: revalidate, spawn the
removal only while the 5 s floor remains, wait, rescan. Under the flag, when the
rescan decides `removed` with reason null, the seam calls the branch stage with
the plan, the target and that rescan's evidence, and returns both outcomes. The
batch loop stops after the first target whose removal is not a plain `removed`
or whose branch stage is not a plain `retired` (D6).

The stage is: the re-read (a bounded manifest read and one ref listing of the
narrowed shape revalidation uses: the merge-target candidates,
`refs/remotes/origin/HEAD`, and the selected branches and their upstreams); the
checks of D4, in memory; the branch child of D3; and the post-check, one more
listing of the same shape. Because the post-check is the newest listing, the
next target's revalidation compares against it in place of the rescan's
listing, so that a merge target moved during a branch stage is caught there,
where change 1's D7 would use the rescan that preceded the stage. The identity
probe and the registry listing of that next target's repository part stay
those of the rescan.

A target that does not enter the stage gets its `branch_retirement` without a
child, by the table in D5.

### D3. The compare-and-delete (A-2)

The branch child is a handle of a new kind, `branch`, through feature 004's
runner: the scrubbed environment (the seventeen names) without
`GIT_OPTIONAL_LOCKS`, because it writes; its own process group; standard input
from the null device; standard output and standard error read and capped like
a probe's. Its argument vector is

```sh
git -c protocol.allow=never -c protocol.file.allow=never \
  -c protocol.ssh.allow=never -c protocol.git.allow=never \
  -c protocol.http.allow=never -c protocol.https.allow=never \
  -c protocol.ext.allow=never -C <command directory> branch -d -- <branch>
```

with the branch name as the plan recorded it. `--` keeps a name that begins
with `-`, which `git branch` cannot create but a hand-written ref can hold, from
being read as an option. The status pins of the removal command are not added:
`branch -d` runs no status.

The compare is the re-read: the head it lists must equal the reconciliation
record's `branch_sha`. The delete is Git's non-force `branch -d`, for three
reasons: Git's own refusals stay the last defense (a branch checked out in any
worktree; a branch not merged into its upstream, or into the command
directory's `HEAD` when its upstream's remote-tracking ref is absent); it
removes the `branch.<b>` section and the reflog with the branch; and it is the
command `delete-branch` runs (`project:734`), so the stage and its retry path
agree. Git's merge test is weaker than the stage's own check for a live
upstream: an eligible row has `ahead` and `behind` 0, the `unpushed`,
`remote-ahead` and `diverged` rungs preceding `merged-removable`, so Git
compares the branch with an equal upstream and passes. That is the PR #2
finding that `branch -d` "can accept a tracking branch based on its configured
upstream"; D4 runs first, so the stage, not Git's test, decides eligibility.

Git 2.43 deletes the ref without an expected old value (Context), so the
compare and the delete are not atomic: the window runs from the re-read to
Git's deletion. Between the re-read and Git's own read, Git's own check guards
it; after Git's read, nothing does. The narrow guarantee states that window,
and the proposal's Open Questions carry the atomic alternative, `git update-ref
-d refs/heads/<b> <sha>`, which skips Git's checked-out refusal and merge test
and leaves the `branch.<b>` section. `branch -D`, `--force`, `-f` and any second
branch child are never used.

### D4. The checks, and which targets qualify (A-2, A-3)

A target enters the stage only as `removed` with reason null, so its
reconciliation record shows the branch present at the planned head. The checks
run in this order, stopping at the first failure:

1. The branch is in the re-read listing; else `not-attempted`,
   `branch-missing`.
2. Its head equals the reconciliation record's `branch_sha`; else `retained`,
   `branch-changed`, with `observed_sha` the head found.
3. The merge target, re-resolved from the re-read's manifest and listing as
   change 1 resolves it, has the plan's `name`, `source` and `sha`; else
   `retained`, `state-changed`.
4. No registered worktree, the main worktree included, has the branch checked
   out in the rescan's registry listing; else `retained`, `branch-in-use`.

A value the re-read cannot establish, a listing that fails or times out or a
manifest read that does, is `retained` with `state-changed`, as change 1's
revalidation counts an unreadable value as a difference.

No Git child computes ancestry. The plan proved the planned head an ancestor of
the merge target's SHA through its merged set, and checks 2 and 3 find both
unchanged, so that proof is the ancestry at the target's current tip, as change
1's revalidation reasons (CAS `design.md` D7). A-2 asks for ancestry "at its
current tip"; a moved merge target would need a `merge-base --is-ancestor`
child, but the canonical "MUST refuse when the state no longer matches the
reviewed plan" (`project-clean-review-safety/spec.md:51-53`) already retains
the branch there, so the child is never needed. This is narrower than A-2's
text: a branch whose merge target moved forward is retained, not retired.

The re-read runs no identity probe. The values it compares make a deletion
lossless wherever it lands: a repository replaced after the rescan that holds
the same branch at the same head, merged into a merge target at the same SHA,
loses no commit by the deletion, and one whose values differ retains the
branch. Concurrent writers are outside the contract in any case.

Every target the run removes with reason null qualifies, whether its upstream
lives (its remote branch and remote-tracking ref stay) or its remote-tracking
ref was deleted (merged on local ancestry, Brett Heap's ruling of 2026-10-09).
A row gated `unstarted-branch` or `reflog-unavailable` is never removed, so it
never reaches the stage; the flag widens no gate.

### D5. The `branch_retirement` sub-record (A-4, L-4)

Each target object of the apply result record gains `branch_retirement` beside
`reconciliation`, under the flag only; without it the key is absent, so a run
without the flag prints change 1's record byte for byte.

| Field | Value |
| --- | --- |
| `stage` | `retired`, `retained`, `not-attempted`, or null when the post-check could not establish the outcome |
| `reason` | as below |
| `branch` | the target's branch |
| `planned_sha` | the target's planned head |
| `observed_sha` | the head the re-read listed; null when it listed none or did not run |
| `command` | the branch child's argument vector; null when none was spawned |
| `exit_status` | the branch child's status; null when none was spawned or its exit was not observed |

| Stage | When | Reasons |
| --- | --- | --- |
| `retired` | the post-check shows the branch absent after the branch child ran | null (exit 0); `git-failed` (nonzero exit); `probe-timeout`, `deadline-exceeded` (`project` stopped the child past its budget, the latter when the work deadline was the limit) |
| `retained` | the target is `removed` and its branch is present when the stage ends | `branch-changed`, `state-changed`, `branch-in-use`, `deadline-exceeded`, `interrupted`, `spawn-error`, `git-refused` (nonzero exit), `unconfirmed-retirement` (exit 0), `probe-timeout`, `removal-ceiling` |
| `not-attempted` | no stage ran | `branch-missing`, `target-not-removed`, `branch-retention-stop` |
| null | the post-check failed or timed out | `reconciliation-incomplete` |

A target that does not enter the stage takes its record from its own stage:

| Target | `branch_retirement` |
| --- | --- |
| `removed`, `branch-advanced-after-removal` | `retained`, `branch-changed` |
| `removed`, `branch-missing-after-removal` | `not-attempted`, `branch-missing` |
| `removed`, `removal-ceiling`, branch present | `retained`, `removal-ceiling` |
| `removed`, `removal-ceiling`, branch absent | `not-attempted`, `branch-missing` |
| `refused`, `failed` or `unknown` | `not-attempted`, `target-not-removed` |
| `not-attempted`, the run stopped at an earlier branch stage | `not-attempted`, `branch-retention-stop` |
| `not-attempted`, any other cause | `not-attempted`, `target-not-removed` |

`reconciliation` stays the rescan that decided the removal, so a retired
target shows `branch_present: true` there and `retired` here; the record's two
objects are two moments, and the sub-record is the later. A null `stage` makes
the result's `completeness` incomplete. The sub-record's own `stage` reads
`BA:1319-1321`'s "stage values of its own"; change 1's target `stage`, its
reasons and its notes are untouched (L-4). Null rather than a fourth value
`unknown` keeps A-4's three values and follows change 1's rule that null means
not established.

Two examples of the sub-record, the first retired, the second retained after
the merge target moved (the target's other keys are change 1's):

```json
"branch_retirement": {"stage": "retired", "reason": null, "branch": "f1",
                      "planned_sha": "<40 hex>", "observed_sha": "<40 hex>",
                      "command": ["git", "-c", "protocol.allow=never", "...",
                                  "-C", "<command directory>", "branch", "-d",
                                  "--", "f1"],
                      "exit_status": 0}
"branch_retirement": {"stage": "retained", "reason": "state-changed",
                      "branch": "f1", "planned_sha": "<40 hex>",
                      "observed_sha": "<40 hex>", "command": null,
                      "exit_status": null}
```

### D6. The stop rule and the exit status (A-4)

The batch stops after the first target whose removal is not a plain `removed`
or whose `branch_retirement` is not `retired` with reason null. Later targets
are `not-attempted` with change 1's reason (`batch-stopped`, or `interrupted`
or `deadline-exceeded` when a signal or the deadline stopped the run), their
`branch_retirement` `not-attempted` with `branch-retention-stop` when the stop
came at a branch stage. The exit status is change 1's first matching row, this
change's additions marked "(flag)":

| Exit | First matching row |
| --- | --- |
| 130, 143 or 129 | a signal was received, the first deciding, or input ended at the question |
| 1 | the deadline stopped work after the apply phase began (a branch stage's `deadline-exceeded` included), any target is `unknown`, any target's reason is `removal-ceiling`, or (flag) any `branch_retirement` has a null `stage` |
| Git's status | a target is `failed` with `git-refused` or `git-failed` (removal children only) |
| 2 | any refusal; a `refused` target; `removed` with a branch-after-removal reason; `failed` with `spawn-error`; (flag) a target `removed` with reason null whose `branch_retirement` is not `retired` with reason null |
| 0 | every selected target `removed` with reason null and (flag) its branch `retired` with reason null, or nothing eligible |

A Git refusal of `branch -d` exits 2, not Git's status: the worktree is gone and
the run is a partial success the record explains, and Git's 1 would read as
`project`'s "incomplete". Retirement with a reason (`git-failed`,
`probe-timeout`) is not plain, stops the run and exits 2, as change 1 stops
after `removed` with `removal-ceiling`.

### D7. Bounds, counts, signals and the fit (A-5)

| Child | Budget | Counted under |
| --- | --- | --- |
| re-read listing (and the manifest read, a filesystem call) | `min(5 s, work remaining)` | `probes`, the target's `probes_performed` |
| branch child | `min(5 s, work remaining)` | `operations` |
| post-check listing | `min(5 s, reserve remaining)` | `probes`, the target's `probes_performed` |

The re-read gates a mutation, as revalidation does, so it is work; the
post-check reconciles, so it runs in the reserve. When no work remains, neither
the re-read nor the branch child starts and the branch is `retained` with
`deadline-exceeded`.

Signals: the re-read listing is a probe and is stopped like one; a branch child
in flight is not signalled and is waited for within its budget, because a ref
transaction killed part-way can leave a `.lock` file to clear by hand; past the
budget it gets change 1's probe termination (SIGTERM to the group, SIGKILL 2 s
later, a reap of at most 2 s). After the signal the post-check runs in the
reserve, as change 1 reconciles after a signal.

The 64 s bound holds: a branch child ends or is stopped by the 50 s work
deadline and reaped within 4 s more; the post-check and the final rescan run
in the reserve up to 60 s, and a reserve child stopped there is reaped within 4
s, as change 1 counts.

Counts: `operations.estimated` is 2T; `probes.estimated` is change 1's F + W +
E + 5T + 3 (`BA:820`) plus 2T. No `limits` or `budget` member is added: the
stage spawns one branch child per target, so `limits.targets` (16) caps them,
and `budget.probe_timeout_seconds` (5) bounds each.

The fit of `BA:729-760` gains three children per target before the next
removal. At the packet's assumed costs (150 ms per child, 0.3 s per removal,
T = 16), target k's removal spawns after 7 + 128 + 16 + 5k probes, k - 1
removals and 3(k - 1) stage children, at 21.9 + 1.5k s: the 15th at 44.4 s
with 5.6 s left, the 16th at 45.9 s with 4.1 s left, inside the 5 s floor by
0.9 s. At change 1's measured costs (CAS `tasks.md` 2.1: the 16th removal
spawning at 23.6 s with 26.4 s left), the 45 added children, even at 150 ms
each, move the 16th to about 30.4 s with about 19.6 s left. Change 1 kept its
caps on its measured fit, and this design does the same: no cap changes.
Where the assumed costs do hold, the 16th target is `not-attempted` with
`deadline-exceeded` and the run exits 1; the next run takes it (Risks).

### D8. What the person sees (A-6, A-7)

All new text is ASCII, with `ROOT`, `PATH`, `BRANCH`, `N`, `R`, `K` and
`REASON` substituted (paths by change 1's escaping rule), and the tests pin it.

- Plan, under the flag: each selected row reads `  remove PATH and retire
  BRANCH` where change 1 prints `  remove PATH [BRANCH]`.
- Question: `Remove N worktrees and retire their N local branches? [yes/N]`;
  for one, `Remove 1 worktree and retire its local branch? [yes/N]`.
- Summary, on every apply result under the flag: `Removed N; branches
  retired: R; retained: K.`, then one line per retained branch, `Retained
  BRANCH (REASON); retry: project clean ROOT --apply --action delete-branch
  --branch BRANCH`.
- Stop block: change 1's, with a branch stage's stop reading `Stopped at PATH
  (branch BRANCH: REASON). Removed K of N. Not attempted: P1, P2. Next: project
  clean ROOT --all-safe`.
- Residual-window line, under the flag: `Not protected: ignored files created
  or index flags set after the last check, a branch changed after its last
  check, and any change after Git's own check.`

The retry command names `delete-branch`, the explicit action, unchanged
(`BA:1281-1293`). The overview never suggests the flag: its suggestion is one
of two fixed argument vectors without `--apply` (`APO/ov:484-487`).

### D9. Tests (A-7)

`test_clean_removes_only_merged_worktree_and_keeps_branch` (`tests:857`) stays
as the default path's test. Each scenario of the ADDED requirement, and the
review-safety scenario this change adds, gets a test named after it, built on
feature 004's helpers: the merged, published worktree with a commit of its own;
the counting `git` wrapper, which records the branch child's arguments, `-C`
directory and environment (no `GIT_ALLOW_PROTOCOL`, no `GIT_OPTIONAL_LOCKS`);
test hooks after the rescan and after the re-read; and two fake `git`s, one
whose `branch -d` exits 0 without deleting and one whose `branch -d` ignores
SIGTERM. The Context table's facts become fixtures run on change 1's CI floor
job (its D17) at Git 2.36 as well as on the four test jobs (`ubuntu-latest`
and `macos-latest`, Python 3.10 and 3.12), run as `python3 -m unittest
discover -s tests -v`.

### D10. JSON and the enum question (L-4)

`branch_retirement` is one new key on a target object, with enums of its own.
Change 1 versions "a rename, removal, type change or change of meaning"
(`CAS/pc:1129-1131`), and a new key is none of those; change 2 calls "adding a
field" additive (`APO/ov:656-657`). No existing enum gains a value: the target's
`stage` and `reason`, the refusal codes, the notes and the ladder are as change
1 leaves them. The disagreement between the two changes about adding an enum
value therefore does not bind this change; the proposal puts it before Brett
Heap with L-4's recommendation.

## Risks / Trade-offs

- [Git 2.43's `branch -d` deletes without an expected old value, so a branch
  moved after Git's own read is deleted unchecked] -> The re-read is the last
  read before Git's; Git's checked-out refusal and merge test run on the value
  Git reads; the residual-window line names the window; the proposal's Open
  Questions carry `update-ref -d` with its costs.
- [A branch whose upstream's remote-tracking ref was deleted is judged by Git
  against the command directory's `HEAD`, so with the main worktree on another
  branch that lacks its commits Git refuses and the run stops] -> `retained`,
  `git-refused`, exit 2, the branch and the next command named; `delete-branch`
  runs the same command from the same directory and is refused the same way,
  so the README tells the person to run `git branch -d BRANCH` from a checkout
  of the merge target, never `-D`; PR #2's command-root workaround is not
  carried (proposal, Out of Scope).
- [A retention stops the run and leaves later eligible worktrees for the next
  run] -> The packet's rule (`BA:1341-1343`); the stop block names the next
  command.
- [A branch checked out by two worktrees, one added with `--force`, stops the
  batch at the first] -> `retained`, `branch-in-use`; once the second worktree
  is removed, a later run or `delete-branch` retires the branch.
- [A `reference-transaction` hook runs inside the branch child, as under
  `delete-branch` today] -> Its time counts in the child's 5 s budget, and the
  post-check decides; the hook is the repository owner's code.
- [At the packet's assumed costs the 16th removal would start 0.9 s inside the
  5 s floor] -> Change 1's measured fit governs (D7); the degraded case is a
  `not-attempted` target with `deadline-exceeded`, exit 1, never unsafe.
- [The re-read runs no identity probe] -> The compared head and merge-target
  SHA make any deletion lossless (D4); concurrent writers are outside the
  contract.
- [A retired branch's reflog and `branch.<b>` section go with it] -> The record
  keeps `planned_sha` and `observed_sha`; `git branch BRANCH SHA` recreates the
  branch, whose commits are in the merge target, and `git branch -u` restores
  its upstream.
- [A script running `--yes --json --retire-branches` deletes branches
  unattended] -> Opt-in only, never suggested by the overview, and every
  deletion listed in the record.
- [The facts of D3 were checked on Git 2.43 only] -> D9 runs them on change 1's
  CI floor job at Git 2.36.

## Migration Plan

Without the flag nothing changes: every run behaves as change 1 specifies.

1. Ratification by Brett Heap's word on the pull request the lane opens for
   this change, with the proposal's three Open Questions before him
   (`tasks.md` 1.6).
2. Before the handoff (`tasks.md` section 2): feature 004 merges and change 1
   archives, PR #19 is resolved and "Clean bounds its Git work and reports
   omitted work" re-based on the text that landed, and this change validates
   again.
3. `/speckit.specify`, from a local `main` synced to `origin/main`, creates the
   one feature under the next free number, 006 or later, recorded once in
   `tasks.md` under "Speckit Handoff"; `/opsx:apply` runs only then.
4. The feature implements D1 to D10 inside feature 004's seam, the README's
   "Clean up Git worktrees" (the flag, the stop, the retry path and the
   deleted-upstream case of Risks) and the tests of D9, merging `main` into its
   branch as `main` moves, the cache-disposal feature included when it lands
   first, and never rebasing.
5. The realization PR merges with green checks on all four CI jobs and closes
   issue #23.
6. The change is archived after that merge and after the archives of change 1
   and `add-project-clean-cache-disposal`, its shared MODIFIED blocks re-based
   on the cache change's archived text first (L-5).

Rollback: revert the realization commit on `main`. The flag is opt-in, so the
revert removes only it; branches it retired can be recreated from the SHAs
their records hold. Installed `project` artifacts follow workBenches' pin, so a
revert before the pin moves reaches nobody downstream.

## Open Questions

The proposal's three Open Questions (enum closure, the flag's spelling, and
the deletion primitive) are before Brett Heap, each with a recommendation the
deltas implement; a ruling against a recommendation edits the deltas and D1,
D3 or D10 before ratification. No other question changes what is built.
