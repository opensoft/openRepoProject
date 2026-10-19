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
D6; A-5, as amended on 2026-10-18, to D7; A-6 to D8; A-7 to D9; L-4 to D5 and
D10; L-1, L-5 and L-7 to the Migration Plan. The addendum of 2026-10-18 maps:
L-10 and A-11 to D5; A-9 to D7; A-12 to this Context; L-12 to D9 and the
Migration Plan; L-11 and A-13 to the Migration Plan; A-10 to the proposal's
Open Questions; A-14 to D4; A-15 to D5 and D9. The council's verdicts of
2026-10-19 map: A-16, A-17 and A-18 to D4 (the plan's keeps), D5 and D8; A-4
as amended to D6; A-5 as amended to D3 and D7; A-1 as amended to D1 and D10;
A-19 and P-2 to D8 and Rollback; A-20 to D3 and the Migration Plan; P-4 to the
proposal's Why. The alignment review and the council are resolved
(`proposal.md`, "Questions Resolved by the Alignment Review" and "Council
Verdicts"); the council's one NOTED concern, S-4, is in `clarifications.md`,
and D2 answers it.

Citations follow `proposal.md`: packet files at `da33d92`, `CAS` for change 1,
`APO` for change 2, `project:N` and `tests:N` at `961c405`, all unchanged at
main `e9d6711`.

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
  (`project:658-663`); the stage's re-read covers that check and the upstream
  evidence change 1's revalidation compares (D4).
- `ancestor()` (`project:537-541`) spends one `merge-base --is-ancestor` child
  per call; the stage needs none (D4).
- `probe()` (`project:60-65`) sets `GIT_OPTIONAL_LOCKS=0` for read-only
  children; the branch child writes, so it is not one of those.
- The parser's `clean` flags (`project:1109-1117`) gain `--retire-branches`.
- Feature 004 (its `plan.md`, slices 2 and 6, and its `tasks.md`, on branch
  `004-project-clean-all-safe`, re-checked at `4e3af0a`, which descends from
  the `66d60b6` of the alignment round and changes only tests and task ticks
  since `5f58ac0`) builds what the stage stands on: the child handle
  `ChildHandle` (`start`, `terminate_group()`, `advance()` and the reap
  deadline; task T022), `run_bounded()` (T024), the scrub and the pins of
  `git_env(kind)` and `git_argv(kind, args)` (T013, whose kinds T012 lists and
  whose `GIT_KINDS` table has landed in `project` on that branch), the narrowed
  ref listing of revalidation and rescan (`narrowed_ref_patterns(plan)`, T084),
  the removal seam that change 1 names `retire_worktree(plan, target)` (CAS
  `proposal.md:189`; `BA:1319`), which slice 6 builds without that name, as
  `apply_removals(plan, run)` over `revalidate()`, `run_removal()`, `rescan()`
  and `decide_stage()` (T055 to T057), the rescan's reuse as the next target's
  repository part (T085), and the result record (`result_document()`,
  `print_result()` and `apply_exit_status()`, T057). The stage is a tail of
  that seam, after `decide_stage()`; its branch child is one more kind for
  `git_env` and `git_argv`, or reuses the `delegate` row's shape (not
  read-only, no status pins, the protocol pins).
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

The council's adversary engineer added, on Git 2.43.0 (council finding AE-1):
a commit reset or amended away on a branch stays reachable through that
branch's reflog after `worktree remove`, and is unreachable once `branch -d`
deletes the branch, a default `git gc` then pruning it once it is older than
`gc.pruneExpire`; `branch.<b>.description` goes with the section; and
`rev-list --max-count=1 --stdin` given a reflog's objects, `--not` and the
merge target's SHA prints an amended-away draft and prints nothing for a plain
history, exit 0 both times. Its product advocate reproduced the refusal of the
fifth row through the explicit `delete-branch` action, whose output passes
Git's advice to run `git branch -D` through to the person (council finding
P-1).

The Git 2.36 floor was not available for these checks here; D9 puts them on
change 1's CI floor job.

## Goals / Non-Goals

**Goals:**

- One opt-in branch stage per removed target, inside the seam feature 004
  builds, meeting `BA:1339-1345` whole (D2, D3, D4).
- A plan that decides which branches it retires and keeps, so that no keep it
  can foresee stops the batch (D4, D6).
- An evidence-decided outcome per branch, in a sub-record that leaves every
  change 1 enum as it is (D5, D10).
- A stop rule and exit status ordered inside change 1's table (D6), bounds
  that keep its 64 s run bound (D7), and fixed human text pinned by tests (D8,
  D9).

**Non-Goals:**

- Any change to a run without the flag: its plan, digest, question, result
  and exit status stay change 1's byte for byte. No change to the explicit
  `delete-branch` action, to `push`, to the gates or the ladder, or to the
  overview.
- Bounding the explicit `delete-branch` child, remote branch deletion,
  squash-merge or patch-equivalence retirement, a batch over branches whose
  worktree is already gone, and any lock.

## Decisions

### D1. The flag and its argument rules (A-1, as amended)

`--retire-branches` is a `store_true` flag of `clean`. `clean()` checks it with
change 1's other argument combinations, before resolution builds a plan:
accepted with `--all-safe`, as a read-only preview or with `--apply`, and with
`--apply --action remove --worktree P`; otherwise the `invalid-arguments`
refusal, exit 2, with the extended error object under `--json`. Change 1 has no
single-target preview, so the flagged preview is `--all-safe` only.

Under the flag the plan decides each selected row's branch (D4), prints the
flagged plan lines (D8), carries `branch_plan` and adds `retire` to the digest
input (D10), and counts the stage in `operations.estimated` and
`probes.estimated` (D7). The digest input under the flag therefore differs
from every flagless one, even when it retires nothing, so `--expect-plan`
binds a flagged apply only to a flagged preview; a flagless digest given to a
flagged apply refuses with `plan-digest-mismatch`, exit 2, before any question
or mutation, as change 1 refuses any mismatch. Without the flag the digest
input and value are change 1's byte for byte, and so is the report's equality
with the `--all-safe` preview that "Clean reports local worktree state" states;
that requirement is MODIFIED only to say a flagged plan's digest is its own.

Alternatives rejected: deletion by default for `remove`, as `5fc2b51` did,
because the packet keeps "implicit local branch deletion" a non-goal
(`OV:150-152`); a new action such as `--action remove-and-delete-branch`,
because the batch takes no `--action` (`CAS/pc:571-574`) and one flag serves
both forms; a digest that ignores the flag, the draft's first choice, because
a reviewer approving a flagless preview's digest would then authorize, under
`--yes`, deletions no artifact showed (council finding AE-2); and refusing
`--expect-plan` with the flag, which would leave every scripted flagged apply
unbound.

### D2. Where the stage runs

`retire_worktree(plan, target)` keeps change 1's sequence: revalidate, spawn the
removal only while the 5 s floor remains, wait, rescan. Under the flag, when the
rescan decides `removed` with reason null and the confirmed plan retires the
target's branch, the seam calls the branch stage with the plan, the target and
that rescan's evidence, and returns both outcomes. The batch loop stops after
the first target whose removal is not a plain `removed` or whose
`branch_retirement` is not plain (D6).

The stage is: the re-read (a bounded manifest read and one ref listing of the
narrowed shape revalidation uses: the merge-target candidates,
`refs/remotes/origin/HEAD`, and the selected branches and their upstreams); the
checks of D4, in memory; the branch child of D3; and, once a branch child was
spawned, the post-check, one more listing of the same shape.

The next target's revalidation keeps change 1's sourcing: after a plain
`removed`, the rescan's three repository children serve as its repository
part, counted in its `probes_performed`, as feature 004's T085 says; the
stage's re-read and post-check are counted in the stage's own
`probes_performed` (D5) and are never reused. A merge target moved by a
concurrent writer during a branch stage is therefore not caught by the next
target's revalidation, which compares the rescan read before that stage, but
by the next target's own re-read before its branch child, which compares the
merge target (D4, ruling A-14), and retains that branch with `state-changed`.
Concurrent writers are outside the contract (`clarifications.md`, S-4).

A target that does not enter the stage gets its `branch_retirement` without a
child, by the table in D5.

### D3. The compare-and-delete (A-2, A-5 as amended, A-20)

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

It spawns only while at least change 1's 5 s removal floor of the work
deadline remains, as a removal does, and its budget is then `min(5 s, work
remaining)`, which is the whole 5 s; so the work deadline never stops a branch
child part-way, and the only stop past its budget is one of a child that ran
its full 5 s, a hung one. The re-read before it gets `min(5 s, work remaining
less the removal floor)`, as the cache change words its cache stage, so that
the floor is left for the spawn. A branch child is not signalled on a signal
or an exception and is waited for within its budget, as a removal child is
waited for, because a ref transaction killed part-way can leave a `.lock` file
to clear by hand. Change 1's project-command Termination paragraph names only
probe children, killed on every exit path, and removal children, waited for,
so that paragraph is MODIFIED to name the branch child beside the removal
child, and its Budgets sentence to give the re-read its narrower budget. That
block is written on PR #19's text and held uncommitted until lane
openRepoProject-2 checks its diff (ruling A-20; proposal, Dependencies and
Sequencing).

The compare is the re-read: the head it lists must equal the reconciliation
record's `branch_sha`, with the other values of D4. The delete is Git's
non-force `branch -d`, for three reasons: Git's own refusals stay the last
defense (a branch checked out in any worktree; a branch not merged into its
upstream, or into the command directory's `HEAD` when its upstream's
remote-tracking ref is absent); it removes the `branch.<b>` section and the
reflog with the branch; and it is the command `delete-branch` runs
(`project:734`), so the stage and its retry path agree. Git's merge test is
weaker than the stage's own check for a live upstream: an eligible row has
`ahead` and `behind` 0, the `unpushed`, `remote-ahead` and `diverged` rungs
preceding `merged-removable`, so Git compares the branch with an equal upstream
and passes. That is the PR #2 finding that `branch -d` "can accept a tracking
branch based on its configured upstream"; D4 runs first, so the stage, not
Git's test, decides eligibility. For an upstream whose remote-tracking ref is
absent, Git's test is the stricter one, against the command directory's
`HEAD`, and the plan keeps such a branch when that `HEAD` is not the merge
target's SHA (D4), so that Git's refusal there is foreseen, not met.

Git 2.43 deletes the ref without an expected old value (Context), so the
compare and the delete are not atomic: the window runs from the re-read to
Git's deletion. Between the re-read and Git's own read, Git's own check guards
it; after Git's read, nothing does. The narrow guarantee states that window,
and the proposal's Open Questions carry the atomic alternative, `git update-ref
-d refs/heads/<b> <sha>`, which skips Git's checked-out refusal and merge test
and leaves the `branch.<b>` section. `branch -D`, `--force`, `-f` and any second
branch child are never used.

### D4. The plan's keeps, the checks, and which targets qualify (A-2, A-3, A-14, A-16 to A-18)

**The plan's keeps.** Under the flag the plan decides, for each selected row,
whether the run retires its branch, and keeps it for the first of these
reasons that holds, in this order so that the printed advice never leads to
deleting work only the reflog holds:

1. `reflog-unmerged` (A-16): a commit the branch's reflog names, the new object
   of an entry of `logs/refs/heads/<branch>` as the `unstarted-branch` gate
   read it, is not proven an ancestor of the merge target's SHA. One `rev-list
   --max-count=1 --stdin` child per repository is given every selected row's
   named commits, then `--not` and the merge target's SHA; it prints nothing
   when every named commit is merged. Only when it prints a commit does one
   such child per selected row run, over that row's commits, to say which rows
   fail. A failed or timed-out child fails the proof of every row it covers.
   The gate's read is reused, so no file is read again.
2. `branch-in-use` (A-18): a registered worktree that is not selected, the
   main worktree included, holds the branch in the plan's registry listing.
3. `head-not-merge-target` (A-17): the branch's upstream remote-tracking ref is
   absent, so Git's non-force check judges it against the command directory's
   `HEAD`, and that `HEAD`, from the registry listing's main-worktree row, is
   not the merge target's SHA. The SHA test is conservative: it may keep a
   branch Git would accept, which is the safe direction, and it needs no child.
4. `branch-shared` (A-18): a later selected row holds the same branch; the
   branch is decided at its last holder, the only one whose stage can run.

A keep the plan names is printed, counted in the question, recorded
`not-attempted` with its reason, and never stops the run (D6).

**The checks.** A target enters the stage only as `removed` with reason null,
its branch one the plan retires, so its reconciliation record shows the branch
present at the planned head. The checks run in this order, stopping at the
first failure:

1. The branch is in the re-read listing; else `not-attempted`,
   `branch-missing`.
2. Its head equals the reconciliation record's `branch_sha`; else `retained`,
   `branch-changed`, with `observed_sha` the head found.
3. Its `upstream`, `upstream_oid`, `ahead` and `behind`, from the same
   listing, and the manifest's `tracking_branch` equal the plan's, a value
   null in both not counting; else `retained`, `state-changed` (A-14).
4. The merge target, re-resolved from the re-read's manifest and listing as
   change 1 resolves it, has the plan's `name`, `source` and `sha`; else
   `retained`, `state-changed`.
5. No registered worktree, the main worktree included, has the branch checked
   out in the rescan's registry listing; else `retained`, `branch-in-use`.

A value the re-read cannot establish, a listing that fails or times out or a
manifest read that does, is `retained` with `state-changed`, as change 1's
revalidation counts an unreadable value as a difference; a re-read the work
deadline stopped is `retained` with `deadline-exceeded`.

The re-read compares every value of the branch's evidence that change 1's
removal revalidation compares (`CAS/rs:77-82`): `branch`, `head`, `upstream`,
`upstream_oid`, `ahead` and `behind`, the manifest's `tracking_branch`, and the
merge target. Ruling A-14 names `tracking_branch`, `upstream` and
`upstream_oid`; `ahead` and `behind` are added because the ruling asks for
every value change 1 compares that applies to a branch, lane
openRepoProject-3's H1 names them, and they come from the same listing, so no
child is added. "Cleanup revalidates destructive actions" therefore holds as
written: the re-inspection before this local branch deletion refuses, by
retaining the branch, whenever the branch's state no longer matches the plan.

No Git child computes ancestry at the stage. The plan proved the planned head
an ancestor of the merge target's SHA through its merged set, and every commit
the branch's reflog names through the reflog proof; checks 2 to 4 find the
head, its upstream evidence and the merge target unchanged, so those proofs
hold at the target's current tip, as change 1's revalidation reasons (CAS
`design.md` D7). A-2 asks for ancestry "at its current tip"; a moved merge
target would need a `merge-base --is-ancestor` child, but the canonical "MUST
refuse when the state no longer matches the reviewed plan"
(`project-clean-review-safety/spec.md:51-53`) already retains the branch
there, so the child is never needed. This is narrower than A-2's text: a
branch whose merge target moved forward is retained, not retired.

What a deletion can lose is therefore bounded by what is proven: no commit
that the branch's head or its reflog names is lost, because the plan proves
them merged or keeps the branch. What a deletion does remove is the branch's
`branch.<b>` section, including its `description`, `pushRemote` and any
tool's keys, which nothing restores (Risks).

The re-read runs no identity probe. The repository identity is the one the
rescan re-established, which a target `removed` with reason null requires
(`CAS/pc:919-921`), and the narrow guarantee names it. A repository replaced
after the rescan that holds the same branch at the same head with the same
upstream evidence, merged into a merge target at the same SHA, loses no commit
the head or the plan's reflog proof names by the deletion, and one whose values
differ retains the branch. Concurrent writers are outside the contract in any
case.

Every target the run removes with reason null qualifies unless the plan keeps
its branch, whether its upstream lives (its remote branch and remote-tracking
ref stay) or its remote-tracking ref was deleted. The second case is the
lane's ruling A-3, which rests on Brett Heap's ruling of 2026-10-09 that local
ancestry proof outranks remote-gone, a ruling recorded for worktree rows. A row
gated `unstarted-branch` or `reflog-unavailable` is never removed, so it never
reaches the stage; the flag widens no gate.

### D5. The `branch_retirement` sub-record (A-4, L-4, A-15)

Each target object of the apply result record gains `branch_retirement` beside
`reconciliation`, under the flag only; without it the key is absent, never
null, so a run without the flag prints change 1's record byte for byte. That is
the lane's ruling L-10 for every extension's sub-record: present only where the
extension acts, absent otherwise, because null keeps change 1's meaning,
unknown or not established (`CAS/pc:1128-1129`).

| Field | Value |
| --- | --- |
| `stage` | `retired`, `retained`, `not-attempted`, or null when the post-check could not establish the outcome |
| `reason` | as below |
| `branch` | the target's branch |
| `planned_sha` | the target's planned head |
| `observed_sha` | the head the re-read listed; null when it listed none or did not run |
| `command` | the branch child's argument vector; null when none was spawned |
| `exit_status` | the branch child's status; null when none was spawned or its exit was not observed |
| `probes_performed` | the stage's re-read and post-check children, 0 to 2; the target's own `probes_performed` stays change 1's, its revalidation's children (lane openRepoProject-3's L5) |

| Stage | When | Reasons |
| --- | --- | --- |
| `retired` | the post-check shows the branch absent after the branch child ran | null (exit 0); `git-failed` (nonzero exit); `probe-timeout` (`project` stopped the child past its 5 s budget) |
| `retained` | the target is `removed` and its branch is present when the stage ends | `branch-changed`, `state-changed`, `branch-in-use`, `deadline-exceeded` (too little work time to start the re-read or the branch child, or the deadline stopped the re-read), `interrupted`, `spawn-error`, `git-refused` (nonzero exit), `unconfirmed-retirement` (exit 0), `probe-timeout`, `removal-ceiling` |
| `not-attempted` | the plan kept the branch, no branch remained to retire, or no stage ran | `reflog-unmerged`, `branch-in-use`, `head-not-merge-target`, `branch-shared` (the plan's keeps); `branch-missing`, `branch-retention-stop`, `target-not-removed` |
| null | the post-check failed or timed out | `reconciliation-incomplete` |

`retired` with `deadline-exceeded`, in the draft's list, is unreachable under
the spawn floor (D3) and is dropped (A-5 as amended): `retired` carries reason
null, `git-failed` (a test `git` that deletes and then exits nonzero) or
`probe-timeout` (one that deletes and then hangs past its budget), so A-15's
scenario of a retirement with a reason stays, with those two. The sub-record's
`git-refused` and `git-failed` name the branch child's outcome, the branch
present or absent after a nonzero exit; they are not the target enum's split
of exit statuses at 128 (lane openRepoProject-3's L8), and the ADDED
requirement says so.

A `branch_retirement` is plain when it is `retired` with reason null or
`not-attempted` with one of the plan's four keeps. A target that does not
enter the stage takes its record from the first matching row:

| Target | `branch_retirement` |
| --- | --- |
| any stage, its branch kept by the plan | `not-attempted`, the plan's reason |
| `removed`, `branch-advanced-after-removal` | `retained`, `branch-changed` |
| `removed`, `branch-missing-after-removal` | `not-attempted`, `branch-missing` |
| `removed`, `removal-ceiling`, branch present | `retained`, `removal-ceiling` |
| `removed`, `removal-ceiling`, branch absent | `not-attempted`, `branch-missing` |
| `refused`, `failed` or `unknown` | `not-attempted`, `target-not-removed` |
| `not-attempted`, the run stopped after an earlier target that was `removed` and whose `branch_retirement` was not plain | `not-attempted`, `branch-retention-stop` |
| `not-attempted`, any other cause | `not-attempted`, `target-not-removed` |

`reconciliation` stays the rescan that decided the removal, so a retired
target shows `branch_present: true` there and `retired` here; the record's two
objects are two moments, and the sub-record is the later. A null `stage` makes
the result's `completeness` incomplete. Change 1 lists `completeness` in the
apply result record (`CAS/pc:1138`) without saying when it is incomplete, so
this trigger is this change's own, stated in its ADDED requirement, and change
1's own triggers are lane openRepoProject-2's text to settle (A-11; proposal,
Dependencies and Sequencing). The sub-record's own `stage` reads
`BA:1319-1321`'s "stage values of its own"; change 1's target `stage`, its
reasons and its notes are untouched (L-4). Null rather than a fourth value
`unknown` keeps A-4's three values and follows change 1's rule that null means
not established.

Three examples of the sub-record, retired, retained after the merge target
moved, and kept by the plan (the target's other keys are change 1's):

```json
"branch_retirement": {"stage": "retired", "reason": null, "branch": "f1",
                      "planned_sha": "<40 hex>", "observed_sha": "<40 hex>",
                      "command": ["git", "-c", "protocol.allow=never", "...",
                                  "-C", "<command directory>", "branch", "-d",
                                  "--", "f1"],
                      "exit_status": 0, "probes_performed": 2}
"branch_retirement": {"stage": "retained", "reason": "state-changed",
                      "branch": "f1", "planned_sha": "<40 hex>",
                      "observed_sha": "<40 hex>", "command": null,
                      "exit_status": null, "probes_performed": 1}
"branch_retirement": {"stage": "not-attempted", "reason": "reflog-unmerged",
                      "branch": "f2", "planned_sha": "<40 hex>",
                      "observed_sha": null, "command": null,
                      "exit_status": null, "probes_performed": 0}
```

### D6. The stop rule and the exit status (A-4, as amended)

The packet's "a retention stops later targets" (`BA:1341-1342`) governs a
retention the stage discovers: a changed head or upstream, a moved merge
target, a Git refusal, a spawn error, a holder appearing, the deadline at the
stage. A keep the confirmed plan names (D4) neither stops the run nor raises
the exit status by itself; that row exits as it would in a flagless run. So
the batch stops after the first target whose removal is not a plain `removed`
or whose `branch_retirement` is not plain. Later targets are `not-attempted`
with change 1's reason (`batch-stopped`, or `interrupted` or
`deadline-exceeded` when a signal or the deadline stopped the run), their
`branch_retirement` the plan's keep where the plan keeps their branch,
`branch-retention-stop` when the run stopped after a target that was `removed`
and whose `branch_retirement` was not plain (its branch retained, missing or
not established), and `target-not-removed` otherwise: after a target that was
not `removed`, or after a plain outcome when a signal or the deadline stopped
the run. The exit status is change 1's first matching row, this change's
additions marked "(flag)":

| Exit | First matching row |
| --- | --- |
| 130, 143 or 129 | a signal was received, the first deciding, or input ended at the question |
| 1 | the deadline stopped work after the apply phase began (a branch stage's `deadline-exceeded` included), any target is `unknown`, any target's reason is `removal-ceiling`, or (flag) any `branch_retirement` has a null `stage` |
| Git's status | a target is `failed` with `git-refused` or `git-failed` (removal children only) |
| 2 | any refusal; a `refused` target; `removed` with a branch-after-removal reason; `failed` with `spawn-error`; (flag) a target `removed` with reason null whose `branch_retirement` is not plain |
| 0 | every selected target `removed` with reason null and (flag) its `branch_retirement` plain, a keep the plan names included, or nothing eligible |

A Git refusal of `branch -d` exits 2, not Git's status: the worktree is gone and
the run is a partial success the record explains, and Git's 1 would read as
`project`'s "incomplete". Retirement with a reason (`git-failed`,
`probe-timeout`) is not plain, stops the run and exits 2, as change 1 stops
after `removed` with `removal-ceiling`.

### D7. Bounds, counts, signals and the fit (A-5, as amended)

| Child | Budget | Counted under |
| --- | --- | --- |
| reflog proof, at plan time (one per repository, and one per selected row only when the first prints a commit) | `min(5 s, work remaining)` | `probes` |
| re-read listing (and the manifest read, a filesystem call) | `min(5 s, work remaining less the removal floor)`, started only while more than the floor remains | `probes`, the sub-record's `probes_performed` |
| branch child | `min(5 s, work remaining)`, spawned only while at least the 5 s removal floor remains | `operations` |
| post-check listing, only after a branch child | `min(5 s, reserve remaining)` | `probes`, the sub-record's `probes_performed` |

The reflog proof is planning, like the merged set. The re-read gates a
mutation, as revalidation does, so it is work; the post-check reconciles, so
it runs in the reserve. When too little work time remains, neither the re-read
nor the branch child starts, the branch is `retained` with
`deadline-exceeded`, and change 1's deadline rule makes every later target
`not-attempted` with `deadline-exceeded`, exit 1.

Signals: the re-read listing and the reflog children are probes and are
stopped like one; a branch child in flight is not signalled and is waited for
within its budget; past the budget it gets change 1's probe termination
(SIGTERM to the group, SIGKILL 2 s later, a reap of at most 2 s). After the
signal the post-check runs in the reserve, as change 1 reconciles after a
signal.

The 64 s bound holds: a branch child spawns with at least 5 s of work left, so
it ends or is stopped by the 50 s work deadline and is reaped within 4 s more;
the post-check and the final rescan run in the reserve up to 60 s, and a
reserve child stopped there is reaped within 4 s, as change 1 counts.

Counts: under the flag `operations.estimated` gains one per branch the plan
retires, so that it is 2T when no cache is listed and every branch is retired
(`add-project-clean-cache-disposal` also counts each listed cache entry
there); `probes.estimated` is change 1's F + W + E + 5T + 3 (`BA:820`) plus two
per branch the plan retires plus the reflog children the plan spawned. No
`limits` or `budget` member is added: the stage spawns one branch child per
target, so `limits.targets` (16) caps them, and `budget.probe_timeout_seconds`
(5) bounds each. A run adds at most 65 children: 48 for the stage, 16 under
`operations` and 32 under `probes` (A-5 as amended), and 17 reflog children
under `probes`, one for the repository and one per selected row. A keep the
plan names spawns no stage child, so each kept branch lowers the count by
three.

The fit of `BA:729-760`, at the packet's assumed costs (150 ms per child, 0.3
s per removal, T = 16, the 50 s work deadline and the 5 s floor). Without the
cache change and with one reflog child, target k's removal spawns after 7 +
128 + 16 + 1 + 5k probes, k - 1 removals and 3(k - 1) stage children, at
22.05 + 1.5k s, and its branch child 0.9 s later (the removal, the three
rescan children and the re-read), at 22.95 + 1.5k s. The spawn floor needs
each at or before 45 s: removals 1 to 15 spawn (the 15th at 44.55 s), branch
children 1 to 14 spawn (the 14th at 43.95 s), and the 15th branch child, due at
45.45 s, cannot start. So at the packet's costs a flagged run of 16 removes 15
worktrees and retires 14 branches; the 15th branch is `retained` with
`deadline-exceeded`, the 16th target is `not-attempted` with
`deadline-exceeded`, and the run exits 1, never unsafe (`BA:772-774`). In the
worst case, when the repository's reflog child prints a commit and 16 per-row
children follow, every time moves 2.4 s later, at 24.45 + 1.5k s: 13 removed
and 13 retired (fewer where a row's proof failed, whose stage then does not
run and which saves 0.45 s for each later row).

At change 1's measured costs (CAS `tasks.md` 2.1: the 16th removal spawning at
23.6 s with 26.4 s left), the 45 stage children before the 16th removal, even
at 150 ms each, and one reflog child move it to about 30.5 s, and 17 reflog
children to about 32.9 s; its branch child follows within about a second, far
inside the floor. Change 1 kept its caps on its measured fit, and this design
does the same: no cap changes. Where the assumed costs do hold, the last
targets are `not-attempted` with `deadline-exceeded`, exit 1, and the next run
takes their worktrees; a branch `retained` with `deadline-exceeded` keeps
`delete-branch` as its retry (Risks).

With `add-project-clean-cache-disposal` archived first (L-5), its 16 cache
enumerations join the plan, and every time moves 2.4 s later again,
cache-stage filesystem time excluded: target k's removal spawns at 24.45 +
1.5k s and its branch child at 25.35 + 1.5k s with one reflog child, so
removals 1 to 13 spawn (the 13th at 43.95 s) and branch children 1 to 13 (the
13th at 44.85 s), and the 14th removal, due at 45.45 s, does not; in the worst
case of 17 reflog children, at 26.85 + 1.5k s, 12 removals spawn and 11
branch children, the 12th branch `retained` with `deadline-exceeded`. At change
1's measured costs the 16th removal then spawns near 32.9 s with one reflog
child and near 35.3 s with 17, and all 16 fit. Where the cache change's
archived fit sentence says that the 16th target reaches its spawn with more
than the removal floor left, that claim is therefore scoped to runs without the
flag when this change re-bases on it.

So at the packet's 150 ms model a flagged run with cache disposal brings 13 of
its 16 targets through their stage before the floor, 11 in the worst case;
change 1's own deadline rule makes the rest `not-attempted` with
`deadline-exceeded`, the run exits 1, and the next run takes them, never unsafe
(`BA:772-774`). At change 1's measured costs all 16 fit. `limits.targets` stays
16 (A-9). The alternative, a lower target cap under the flag, would be 8 by the
packet's rule (`BA:729-735`), since the last of T such targets then spawns at
about 19.7 + 1.8T s; it is rejected because the cap is applied by the
`deferred-target-cap` gate, so the flag would change the selection as well as
the digest, and because a smaller cap only splits across runs the work that
the deadline already splits safely. The proposal puts the choice to Brett Heap
(Open Questions).

### D8. What the person sees (A-6, A-7, A-19, P-2)

All new text is ASCII, with `ROOT`, `PATH`, `PATH2`, `BRANCH`, `SHA`, `SHA2`,
`MERGE_TARGET`, `N`, `M`, `R`, `K`, `G` and `REASON` substituted (paths by
change 1's escaping rule), and the tests pin it. Without the flag every line is
change 1's.

- Plan, preview and apply alike, under the flag: each selected row reads
  `  remove PATH and retire BRANCH` when the plan retires its branch, `  remove
  PATH; keep BRANCH (REASON)` when it keeps it, `REASON` reading `checked out
  at PATH2` for `branch-in-use`, and `  remove PATH; BRANCH is decided at
  PATH2` for an earlier holder of a shared branch, where change 1 prints
  `  remove PATH [BRANCH]`. The deferral line reads `run again: project clean
  ROOT --all-safe --apply --retire-branches`.
- Question: `Remove N worktrees and retire their M local branches? [yes/N]`
  when the plan keeps none, and `Remove N worktrees, retire M local branches
  and keep K? [yes/N]` when it keeps K, M and K counting distinct branches and
  `worktree` and `branch` singular for a count of 1: two worktrees on one
  branch read `Remove 2 worktrees and retire their 1 local branch? [yes/N]`,
  and one worktree `Remove 1 worktree and retire its local branch? [yes/N]`.
- Summary, on every apply result under the flag: `Removed N; branches
  retired: R; retained: K`, with `; already gone: G` when G is above 0, so
  that R, K and G add up to the distinct branches of the removed targets; then
  one line per such branch, a shared branch at its last holder:
  - `Retired BRANCH (was SHA); restore: git branch BRANCH SHA`;
  - `BRANCH was already gone`;
  - `Kept BRANCH (head-not-merge-target); next: check out MERGE_TARGET in the
    main worktree, then: project clean ROOT --apply --action delete-branch
    --branch BRANCH`, the same next step for `git-refused` when the upstream
    ref is absent;
  - `Kept BRANCH (branch-in-use); next: BRANCH is checked out at PATH2; remove
    that worktree first`, also for a branch whose later holder the run did not
    remove;
  - `Kept BRANCH (branch-changed); now at SHA2; inspect it before retrying:
    project clean ROOT --apply --action delete-branch --branch BRANCH`;
  - `Kept BRANCH (reflog-unmerged); its reflog names commits MERGE_TARGET
    lacks; inspect git reflog BRANCH before any delete-branch`;
  - otherwise `Kept BRANCH (REASON); retry: project clean ROOT --apply
    --action delete-branch --branch BRANCH`.
- Stop block: change 1's, with a branch stage's stop reading `Stopped at PATH
  (branch BRANCH: REASON). Removed K of N. Not attempted: P1, P2. Next: project
  clean ROOT --all-safe --retire-branches`.
- Residual-window line, under the flag: `Not protected: ignored files created
  or index flags set after the last check, a branch changed after its last
  check, and any change after Git's own check.` When the plan also selects a
  cache target (`add-project-clean-cache-disposal`), the line is: `Not
  protected: ignored files created or index flags set after the last check,
  caches recreated after the cache stage, a branch changed after its last
  check, and any change after Git's own check.`

No line prints a retry the plan knows will fail, and none suggests `-D`: the
branch child's output is captured like a probe's, so Git's own advice to run
`git branch -D` never reaches the person from the batch, and the
`head-not-merge-target` line names the checkout under which the retry succeeds
(council finding P-1 reproduced both). The retry command names
`delete-branch`, the explicit action, unchanged (`BA:1281-1293`). Every
command printed for the person to run next under the flag carries
`--retire-branches`, so that following the tool's own advice never strands a
branch whose worktree a flagless run removed. The overview never suggests the
flag: its suggestion is one of two fixed argument vectors without `--apply`
(`APO/ov:484-487`), so A-6's rule stands under A-1 as amended.

### D9. Tests (A-7, A-15)

`test_clean_removes_only_merged_worktree_and_keeps_branch` (`tests:857`) stays
as the default path's test. Each scenario of the ADDED requirement, and the
review-safety scenario this change adds, gets a test named after it, built on
feature 004's helpers (its T010 fixture builders and T011 counting wrapper and
fake Gits, landed on its branch at `4e3af0a`): the merged, published worktree
with a commit of its own; a worktree whose first commit was amended before it
merged, for the reflog proof; the counting `git` wrapper, which records the
branch child's arguments, `-C` directory, environment (no `GIT_ALLOW_PROTOCOL`,
no `GIT_OPTIONAL_LOCKS`) and process group, and each reflog child; test hooks
after the rescan and after the re-read, and fault injection into the re-read,
the branch child's spawn and the post-check; and fake `git`s that pass every
other command to the real Git: one whose `branch -d` exits 0 without deleting;
one that refuses with exit 1; one that runs Git's deletion and then exits 1;
one that runs it and then hangs, ignoring SIGTERM; one that ignores SIGTERM
without deleting; one that sleeps 2 s before deleting, for the signal
scenario; and one whose reflog child exits nonzero. The Context table's facts
become fixtures run on change 1's CI floor job at Git 2.36 (its D17; feature
004's `git-floor` job, task T003, ticked on its branch at `4e3af0a` and not yet
on `main`) as well as on the CI workflow's test jobs, which since PR #32 are
Linux only: one `test` job on `ubuntu-latest` for Python 3.10 and 3.12
(`.github/workflows/tests.yml` at `origin/main` `e9d6711`), run as `python3 -m
unittest discover -s tests -v`. No CI job runs these tests on macOS, so
nothing here is verified by CI there.

### D10. JSON and the enum question (L-4, A-1 as amended)

`branch_retirement` is one new key on a target object, with enums of its own,
and `branch_plan` one new key on the plan envelope, under the flag only:
`{path, branch, planned_sha, action, reason}` per selected row in canonical
order, `action` `retire` or `keep`. The canonical text of `plan_digest` gains a
`retire` member under the flag only, the `[branch, planned_sha]` pairs of the
branches the plan retires in canonical order, present when empty; without the
flag the text is change 1's byte for byte. Change 1 versions "a rename,
removal, type change or change of meaning" (`CAS/pc:1129-1131`), and a new key
is none of those; change 2 calls "adding a field" additive
(`APO/ov:656-657`). The ADDED requirement says that its keys extend, under the
flag only, the lists that "Clean plans and refusals are versioned JSON"
enumerates (lane openRepoProject-3's L10), so that requirement is not
modified. No existing enum gains a value: the target's `stage` and `reason`,
the refusal codes, the notes and the ladder are as change 1 leaves them. The
disagreement between the two changes about adding an enum value therefore does
not bind this change; the proposal puts it before Brett Heap with L-4's
recommendation.

## Risks / Trade-offs

- [Git 2.43's `branch -d` deletes without an expected old value, so a branch
  moved after Git's own read is deleted unchecked] -> The re-read is the last
  read before Git's; Git's checked-out refusal and merge test run on the value
  Git reads; the residual-window line names the window; the proposal's Open
  Questions carry `update-ref -d` with its costs.
- [A branch whose upstream's remote-tracking ref was deleted is judged by Git
  against the command directory's `HEAD`] -> The plan keeps it with
  `head-not-merge-target` when that `HEAD` is not the merge target's SHA, the
  run continues, and the result names the checkout under which the
  `delete-branch` retry succeeds; with the main worktree on the merge target
  the branch is retired. The SHA test may keep a branch Git would accept.
  PR #2's command-root workaround is not carried (proposal, Out of Scope).
- [Retiring a branch deletes its reflog and its `branch.<b>` section] -> The
  plan proves every commit the reflog names merged or keeps the branch
  (`reflog-unmerged`), so no named commit is lost. The section's keys
  (`description`, `pushRemote`, any tool's keys) are deleted and not
  restored; `git branch BRANCH SHA` recreates the branch from the SHA both
  results print and `git branch -u` its upstream, nothing else.
- [The reflog proof names only each entry's new object, as ruling A-16
  defines it] -> After `git reflog expire` has dropped earlier entries, the
  old object of the oldest surviving entry is held by the reflog but is not
  checked, and is lost with it when it is not merged. The ruling binds; the
  proposal reports the point to the lead for a ruling.
- [A rebased or amended branch whose old commits the merge target lacks is
  kept, never retired] -> By design (A-16); `delete-branch` stays its explicit
  path after the person inspects `git reflog BRANCH`, and the patch-equivalence
  alternative is an Open Question.
- [A retention the stage discovers stops the run and leaves later eligible
  worktrees for the next run] -> The packet's rule (`BA:1341-1343`); the stop
  block names the flagged preview as the next command. A keep the plan
  foresees never stops it (D6).
- [A holder appearing only after the plan, or a branch whose later holder the
  run did not reach] -> `retained` with `branch-in-use` and a stop, or a line
  naming the holder; once that worktree is removed, `delete-branch` retires
  the branch.
- [A `reference-transaction` hook runs inside the branch child, as under
  `delete-branch` today] -> Its time counts in the child's 5 s budget, and the
  post-check decides; the hook is the repository owner's code.
- [At the packet's assumed costs a flagged run of 16 retires 14 branches, 13
  with the cache change, 11 in the worst case of the reflog proof] -> Change
  1's measured fit governs (D7, A-9); the degraded case is a `not-attempted`
  target with `deadline-exceeded`, exit 1, never unsafe, and the next run
  takes it; a branch `retained` with `deadline-exceeded` is retried with
  `delete-branch`.
- [The re-read runs no identity probe] -> The compared head, upstream evidence
  and merge-target SHA, with the plan's reflog proof, bound what any deletion
  can lose (D4); concurrent writers are outside the contract.
- [A script running `--yes --json --retire-branches` deletes branches
  unattended] -> Opt-in only, never suggested by the overview, bound by
  `--expect-plan` only to a flagged preview, and every deletion listed in the
  record and the human result with its SHA.
- [The facts of D3 and D4 were checked on Git 2.43 only] -> D9 runs them on
  change 1's CI floor job at Git 2.36, once feature 004's `git-floor` job
  reaches `main`.

## Migration Plan

Without the flag nothing changes: every run behaves as change 1 specifies.

1. Ratification by Brett Heap's word on the pull request the lane opens for
   this change, with the proposal's six Open Questions before him (`tasks.md`
   1.6). The two blocks written on PR #19's text are ratified only as written
   there (`tasks.md` 1.6 and 2.2).
2. Before the handoff (`tasks.md` section 2): feature 004 merges and change 1
   archives; PR #19 is resolved and the two blocks on its text, "Clean bounds
   its Git work and reports omitted work" and the held project-command block
   "Repository inspection requires Git 2.36 and shares one evidence model",
   re-read against the text that landed, or change 1's archived text; and
   this change validates again.
3. `/speckit.specify`, from a local `main` synced to `origin/main`, creates the
   one feature under the next free number, 006 or later, recorded once in
   `tasks.md` under "Speckit Handoff"; `/opsx:apply` runs only then.
4. The feature implements D1 to D10 inside feature 004's seam, the README's
   "Clean up Git worktrees" (the flag, its flagged preview, the keeps, the
   stop, the branch lines and the retry path) and the tests of D9, merging
   `main` into its branch as `main` moves, the cache-disposal feature included
   when it lands first, and never rebasing.
5. The realization PR merges with green checks on every job that
   `.github/workflows/tests.yml` then runs (at `origin/main` `e9d6711`, the
   `test` job on `ubuntu-latest` for Python 3.10 and 3.12; feature 004 adds
   `git-floor`) and closes issue #23.
6. The change is archived after that merge and after the archives of change 1,
   of PR #19's amendment of it, and of `add-project-clean-cache-disposal`. The
   five blocks this change shares with the cache change (the lane's ruling
   B-10) are re-based on its archived blocks first (L-5, L-11, A-13); the
   project-command block is re-based on the archived block of
   `add-project-overview-remote-merge-status` if that change archives first,
   or is the block it re-bases on (L-11); "Clean reports local worktree state"
   is shared with no other open change.

Rollback: revert the realization commit on `main`. The flag is opt-in, so the
revert removes only it; branches it retired can be recreated from the SHAs that
the human and the JSON result both print. Installed `project` artifacts follow
workBenches' pin, so a revert before the pin moves reaches nobody downstream.

## Open Questions

The proposal's six Open Questions (enum closure, the flag's spelling, the
deletion primitive, the target cap of a flagged run, merge-target candidates,
and patch-equivalent reflog commits) are before Brett Heap, each with a
recommendation the deltas implement; a ruling against a recommendation edits
the deltas and D1, D3, D4, D7 or D10 before ratification. No other question
changes what is built.
