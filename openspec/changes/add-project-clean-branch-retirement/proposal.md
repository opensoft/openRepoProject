Lane: openRepoProject-5

# Proposal: add-project-clean-branch-retirement

Status: draft; alignment review and council resolved on PR #26; ratification
by Brett Heap pending; nothing here is ratified. Governing issue:
opensoft/openRepoProject#23, claimed by lane openRepoProject-5 (comment
6111211798); refs #6, the record of the project maintenance design packet.
Proposed on Brett Heap's word "usage reset, resume all. read handoff and
resume and fan out wide and do as much as possible in parallel" (2026-10-11),
read by lanes openRepoProject-4 and openRepoProject-5 as a go for the candidate
list they put to him.

Citations are `file:line` at `da33d92`, which equals `961c405` for `ideation/`.
`BA`, `OV`, `SY` and `HO` are the packet's
`project-maintenance-batch-cleanup.md`, `project-maintenance-overview.md`,
`project-maintenance-synthesis-inspect-and-retire.md` and
`next-session-project-maintenance-fix-handoff.md` under `ideation/brainstorm/`,
which this change reads and never edits. `CAS` is the ratified, unarchived
change `openspec/changes/add-project-clean-all-safe/` ("change 1") at `961c405`,
`CAS/pc`, `CAS/rs` and `CAS/cmd` its `specs/project-clean/spec.md`,
`specs/project-clean-review-safety/spec.md` and `specs/project-command/spec.md`;
`APO` is `openspec/changes/add-project-overview/` ("change 2"), `APO/ov` its
`specs/project-overview/spec.md`. "PR #19's text" is change 1's spec text on
draft PR #19's branch `change/amend-clean-all-safe-push-pins` at `c462d87`,
whose spec files equal those at `5ce23d7`, the head the lane's ruling L-1 names;
PR #19 is still a draft at `c462d87` (2026-10-19). `project:N` and `tests:N` are
`project` and `tests/test_project.py` at `961c405`. Main is now `e9d6711`, whose
`openspec/` and `ideation/` equal `961c405`'s and whose `project`,
`tests/test_project.py` and `README.md:178-201` are unchanged from it, so every
citation at `961c405` holds at main (L-15). Canonical requirements are cited as
`project-clean/spec.md:N` and `project-clean-review-safety/spec.md:N` under
`openspec/specs/`. The lane lead's rulings of 2026-10-11, L-1 to L-9 and A-1 to
A-7, its addendum of 2026-10-18, L-10 to L-15, A-5 as amended and A-9 to A-15,
and its council verdicts of 2026-10-19, A-16 to A-20, A-1, A-4 and A-5 as
amended, and L-16, bind this draft and are applied under Decisions.

## Why

A removal under `project clean --apply` removes a merged, clean worktree and
keeps its local branch; the branch is retired only by a second command, one
branch at a time, `--apply --action delete-branch --branch <b>`
(`project-clean/spec.md:59-60`; `project:723-735`). Change 1 keeps that rule on
purpose, "so that a branch race cannot lose commits" (`CAS/rs:210-211`; CAS
`proposal.md:338-340`), and its batch widens the gap: `--all-safe` removes up
to sixteen worktrees in one confirmed run and leaves sixteen merged branches,
each to be deleted by its own command with its own report, question and
re-inspection (`BA:1281-1293`).

The flag serves repositories whose merged branches are ancestors of the merge
target: merges by merge commit, and fast-forwards of branches not rebased
first. Measured 2026-10-19, two of the estate's merge-commit repositories held
31 and 29 merged branches that still had their worktree, the set this flag
retires, beside 16 and 2 merged branches whose worktree was already gone,
which it does not reach (Out of Scope); those counts are local refs against
each local default branch, so they bound the benefit from above. Squash-merged
branches never prove ancestry, so neither change 1's batch nor this flag acts
on them (Out of Scope); this repository's own pull requests land that way
(`origin/main` holds no merge commit). Branches rebased or amended before their
merge keep their branch, because their reflog names commits the merge target
lacks (ruling A-16).

The packet keeps paired retirement out of the batch as a separately governed
extension (`HO:47-50`; `OV:173-180` and `OV:357-358`; `BA:1314-1318`) and fixes
the contract such a change must meet (`BA:1339-1345`): branch deletion is a
separate post-removal stage with an immediate branch-head and local-ancestry
check that uses the reconciliation record's `branch_sha` as the expected head;
a changed head or a Git refusal retains the branch, stops later targets and
reports the removed worktree and the surviving branch; the explicit
`delete-branch` command remains the retry path; no composite operation may
force-delete or force-push. The PR #2 decision record (comment 6035824335, on
Brett Heap's word "go with your recommendation", 2026-10-07) requires the
proposal to be a MODIFIED requirement on `project-clean`, because it changes
the governed `remove` action (`BA:60-63`; `HO:36-39`), and change 1 names it as
its own change (CAS `proposal.md:690-696`; OQ-27 at `:756-757`).

The closed PR #2's `5fc2b51` met none of that contract. It made branch deletion
unconditional for `remove`, deleted by name without checking the planned head
(PR #2 review comment 3988326415), returned Git's status as its own, and
declared no modified capability while the cleanup spec still said that removal
leaves the branch. This change is the extension the contract describes: an
opt-in flag that retires each removed worktree's local branch in the same
confirmed run, on fresh evidence, with nothing changed for a run without it.

## What Changes

- **An opt-in flag, `--retire-branches`** (A-1, as amended). It is accepted
  with `--all-safe`, as a read-only preview or with `--apply`, and with
  `--apply --action remove --worktree P`; with anything else (the plain
  report, `--action push`, `--action delete-branch`) the command refuses with
  `invalid-arguments`, exit 2, and runs nothing. It is never the default: a run
  without it keeps every branch and prints exactly what change 1 prints, and
  its plan and targets carry nothing new. `--json` is accepted with the flag
  where change 1 accepts it (`CAS/pc:1133-1134`). The flag changes no gate and
  no selection. Under it the `plan_digest` input also carries the branches the
  plan retires, so `--expect-plan` binds a flagged apply only to a flagged
  preview, and a flagless digest refuses a flagged apply with
  `plan-digest-mismatch`, exit 2, before any question or mutation.
- **The plan decides which branches it retires** (A-16 to A-18). Under the
  flag the plan keeps a selected row's branch, and says why, when its reflog
  names a commit the merge target lacks (`reflog-unmerged`: one `rev-list
  --stdin` child per repository, and one per row only when that child prints a
  commit), when a worktree outside the selection holds it (`branch-in-use`),
  when its upstream's remote-tracking ref is absent and the main worktree's
  `HEAD` is not the merge target's SHA, so that Git would judge it against
  that `HEAD` and refuse (`head-not-merge-target`), or when a later selected
  row holds it too (`branch-shared`, decided at the last holder). A keep the
  plan names never stops the run.
- **A branch stage after each proven removal** (`BA:1318-1322`,
  `BA:1339-1345`; A-2, A-14). Inside the removal seam that feature 004 builds
  (`retire_worktree`, CAS `proposal.md:189`), once a target's rescan proves it
  `removed` with reason null, its branch one the plan retires, the stage runs
  before the next target is revalidated:
  1. it re-reads the manifest and, in one ref listing narrowed as change 1's
     revalidation listing is, the branch and the merge-target candidates;
  2. it checks, stopping at the first failure, that the branch exists, that
     its head equals the reconciliation record's `branch_sha`, that its
     `upstream`, `upstream_oid`, `ahead` and `behind` and the manifest's
     `tracking_branch` equal the plan's, that the merge target re-resolves to
     the plan's name, source and SHA, so that the plan's ancestry proofs hold
     at the target's current tip, and that no registered worktree, the main
     worktree included, had the branch checked out in the rescan's registry
     listing;
  3. it spawns Git's non-force `git -c protocol.allow=never` with the six
     per-protocol pins, `-C <command directory> branch -d -- <branch>`, with
     change 1's seventeen-name environment scrub, in its own process group;
  4. it re-reads the branch in one more narrowed listing, and that post-check,
     never the child's exit status alone, decides the outcome.

  Never `-D`, `--force`, `-f`, a retry, a remote branch or a remote-tracking
  ref.
- **Which targets qualify** (A-3). Every target the run removes with reason
  null whose branch the plan does not keep, whether its upstream lives (the
  remote branch stays untouched) or its remote-tracking ref was deleted. The
  second case is the lane's ruling A-3; it rests on Brett Heap's ruling of
  2026-10-09, "yes, local ancestry proof outranks remote-gone, apply it",
  recorded for worktree rows (CAS `proposal.md:811-820`), as its proof rule.
  Rows gated `unstarted-branch` or `reflog-unavailable` never reach `removed`,
  so they never reach the stage.
- **A per-target sub-record** (A-4, L-4, L-10). Under the flag every target of
  the apply result record carries `branch_retirement` `{stage, reason, branch,
  planned_sha, observed_sha, command, exit_status, probes_performed}`; `stage`
  is `retired`, `retained` or `not-attempted`, or null when the post-check
  could not establish it, and the ADDED requirement lists each reason. Each
  entry of the plan's `selected` carries `branch_plan`, its planned action,
  and the plan envelope gains no key.
  Without the flag both keys are absent, never null, since null keeps change
  1's meaning, unknown or not established (`CAS/pc:1128-1129`). The target's
  `stage`, its reasons, the fifteen ladder classes, the gates, the refusal
  codes and the note codes gain no value.
- **The stop rule and the exit status** (A-4, as amended; `BA:1341-1343`). The
  run stops after the first target whose branch stage discovers a retention,
  as it stops after the first target that is not a plain `removed`; each later
  target is `not-attempted` with change 1's `batch-stopped` and carries
  `branch_retirement` `not-attempted` with `branch-retention-stop`. A keep the
  confirmed plan names neither stops the run nor raises the exit status. A
  retained branch exits 2, unless an earlier row of change 1's exit table
  decides first: a signal (130, 143, 129), the deadline, or a stage the
  post-check could not establish (1).
- **Bounded like a probe, with the removal floor** (A-5, as amended). The
  re-read and the branch child start only while more than change 1's 5 s removal
  floor of the work deadline remains, the re-read under `min(5 s, work remaining
  less the removal floor)` and the branch child under `min(5 s, work
  remaining)`, the post-check under `min(5 s, reserve remaining)`; a branch
  child in flight is waited for within its budget when a signal arrives and
  stopped like a probe past it, never abandoned at its budget, since it is a
  mutation (A-20). The branch child counts under `operations`, the reflog
  children and the two listings under `probes`: up to 65 more children per run.
  A run with no removal in flight still ends within 64 s of its start. The
  explicit `delete-branch` action's child stays unbounded, as change 1 says of
  it.
- **What the person sees** (A-6, A-7, A-19, P-2). The plan reads `remove PATH
  and retire BRANCH` or `remove PATH; keep BRANCH (REASON)`; the question
  counts the branches to retire and to keep, `Remove N worktrees and retire
  their M local branches? [yes/N]` when none is kept; every apply result
  prints `Removed N; branches retired: R; retained: K`, then one line per
  branch: `Retired BRANCH (was SHA)` with its restore command, `Kept BRANCH
  (REASON)` with a next step that never prints a retry the plan knows will
  fail and never suggests `-D`, or `BRANCH was already gone`; every command
  printed for the person to run next carries the flag; a stop ends with change
  1's stop block, the branch's reason in it; and the residual-window line names
  a branch changed after its last check. The overview never suggests the flag:
  its suggestion is exactly one of two argument vectors and never carries
  `--apply` (`APO/ov:484-487`).
- **The narrow guarantee under the flag** (MODIFIED review-safety). Change 1's
  "Cleanup SHALL never delete a branch" stays true without the flag. With it,
  the guarantee extends to the branch child, the branch race keeps change 1's
  outcomes, a change seen by the re-read retains the branch, and a change after
  the re-read is the residual, guarded only by Git's own non-force check. Git
  2.43's `branch -d` deletes without comparing the ref to the value its own
  check read (verified for this proposal: its `reference-transaction` hook
  receives an all-zeros old value), so that window ends inside Git (Decisions;
  Open Questions).
- **The evidence model names the branch child** (MODIFIED project-command,
  held). Change 1's Termination paragraph names only probe children, killed on
  every exit path, and removal children, waited for; one sentence names the
  branch child beside them, waited for within its budget, and one clause of
  Budgets gives the re-read its narrower budget. The block is written on PR
  #19's text and held uncommitted until lane openRepoProject-2 checks its diff
  (ruling A-20; Dependencies and Sequencing).

## Rules This Change Keeps

- **Never force.** No `branch -D`, `--force`, `-f`, forced removal or force
  push (`BA:1344-1345`), no automatic retry (`BA:1295`), no fetch, since
  removal proof is local ancestry only (`BA:195-196`; `SY:221-226`), and no
  reset; the canonical "MUST never use a force removal, reset, or deletion of
  unmerged work" (`project-clean/spec.md:61`) stays verbatim.
- **Never by default.** Without `--retire-branches` removing a worktree leaves
  its branch (`BA:36-38`), and branch deletion stays "a separate opt-in
  action" (archived `2026-10-07-add-project-clean-command/design.md:17-18`);
  "implicit local branch deletion" stays a non-goal (`OV:150-152`;
  `SY:232-235`).
- **Never a remote branch.** Remote branches and remote-tracking refs remain
  untouched (`BA:1293`; archived design `:83-84`).
- **`delete-branch` stays the retry path, unchanged** (`BA:1281-1293`,
  `BA:1343-1344`).
- **Local evidence only.** The plan and the stage read refs, the registry, the
  reflog and the manifest; they never fetch, and no remote status approves a
  deletion (`SY:129-130`; `project-clean/spec.md:12-16`).
- **Preserve what is not proven disposable**
  (`project-clean-review-safety/spec.md:21`): a branch whose reflog names a
  commit the merge target lacks is kept, so that no commit the head or the
  reflog names is lost by the deletion.
- **Revalidate before every destructive action, and fail closed**
  (`project-clean-review-safety/spec.md:51-53`): the re-read is that
  re-inspection, comparing every value of the branch's evidence that change
  1's removal revalidation compares, and a mismatch, or a value it cannot
  read, retains the branch.
- **Nothing unconfirmed.** The question names the branches to retire and to
  keep, `--yes` accepts the fresh plan as change 1 defines it, and
  `--expect-plan` binds a flagged apply only to a flagged preview.
- **Evidence decides.** The post-check decides the outcome, and a value not
  established is null, never a default (`CAS/pc:919`, `CAS/pc:1128-1129`).
- **Stop at the first failure.** No continuation, rollback or retry
  (`CAS/pc:246-248`).
- **Change 1's contract unchanged without the flag.** Its enums, ladder,
  gates, caps and refusal codes keep their values (L-4), and its digest input
  and value are byte-identical in a run without the flag.

## What This Repository Does Not Own

- **Git's own non-force check**: `git branch -d` refuses a branch checked out
  in any worktree and a branch it does not find merged; it is the last line of
  defense, never bypassed.
- **Remote branches and pull requests**: the remote host and its owners.
- **Repository hooks**: a `reference-transaction` hook runs during any ref
  deletion, under `delete-branch` today as under this flag; it is the
  repository owner's code.
- **The installed `project` artifact**: workBenches pins it on its owner's
  act; this change does not move the pin.

## Capabilities

### New Capabilities

None. PR #2's `project-clean-branch-retirement` capability is not reused
(L-3); the change stays in `project-clean`, `project-clean-review-safety` and
`project-command`.

### Modified Capabilities

Headers are quoted verbatim, one per line; the ADDED header is proposed text.
Canonical lines are at `961c405`; change 1's ADDED requirements are cited at
their `CAS` line.

- `project-clean` (all five canonical requirements and change 1's six ADDED
  ones accounted for):
  - MODIFIED (`:10`; change 1's text at `CAS/pc:3`):
    `### Requirement: Clean reports local worktree state`.
    One clause only: its sentence that a report's `plan_digest` equals the
    `--all-safe` preview's and that an `--expect-plan` carrying it "SHALL
    match" gains that a plan under `--retire-branches` has a digest of its own,
    which no report's digest matches (A-1 as amended, L-11). The flag adds no
    report field and is refused with the plain report. Its six scenarios stay
    verbatim.
  - Untouched (`:25`; change 1's text at `CAS/pc:105`):
    `### Requirement: Clean classifies preservation and cleanup actions`.
    No class is added and the fifteen names (`CAS/pc:105-111`) stay (L-4).
  - Untouched (`:39`; change 1's text at `CAS/pc:180`):
    `### Requirement: Clean can explicitly push safe feature branches`.
    Its scenario "Push and branch deletion stay human-only"
    (`CAS/pc:223-228`) concerns the explicit `delete-branch` action's `--json`
    refusal, which stays (Decisions).
  - MODIFIED (`:55`; change 1's text at `CAS/pc:230`):
    `### Requirement: Clean can explicitly retire verified worktrees`.
    The one sequence gains the branch stage, for a target the rescan proves
    `removed` with reason null whose branch the plan retires, and only under
    the flag; the stop rule gains a branch stage that does not end plain, a
    keep the plan names being plain; after the sentence "It SHALL remove a
    local branch only as a separate, explicit action after the worktree is
    gone and the branch is verified merged." (`:59-60`, kept verbatim) one
    sentence names `--retire-branches` as such a separate, explicit action,
    never the default (a reading put to ratification, Decisions). "It MUST
    never use a force removal, reset, or deletion of unmerged work." (`:61`)
    and all fourteen of change 1's scenarios, `Remove a merged clean worktree`
    (`:63-68`) and `Every branch remains after a batch` among them, stay
    verbatim; both describe runs without the flag.
  - Untouched (`:70`): `### Requirement: Clean hands off work requiring review`.
    `--all-safe` and `--yes` keep their meaning as action target and
    confirmation.
  - Untouched (`CAS/pc:443`): `### Requirement: Clean resolves its target Git-first`.
    The flag adds no mode; it resolves as `--all-safe` and `--action remove`
    do.
  - MODIFIED (`CAS/pc:566`):
    `### Requirement: Clean previews and applies a batch of eligible worktree removals in one repository`.
    Three sentences only: the digest's canonical text also carries, under the
    flag only, the branches the plan retires (A-1 as amended); the question
    names the branches to retire and to keep under the flag (`:635-637`); and
    the success line gives way to the flag's summary and branch lines
    (`:655-656`). Its ten scenarios stay verbatim.
  - MODIFIED (`CAS/pc:767`, on PR #19's text):
    `### Requirement: Clean bounds its Git work and reports omitted work`.
    Three sentences only: PR #19's counting sentence puts the branch child under
    `operations` beside a removal; the unbounded-children sentence (`:788-789`)
    is scoped to push children and the explicit `delete-branch` action's
    children, the flag's branch child being bounded (A-5); and one sentence
    after the removal floor starts a branch stage's re-read and branch child
    only while more than the floor remains, the re-read under `min(5 s, work
    remaining less the removal floor)` (A-5 as amended), as the cache change
    words its cache stage. Its five scenarios stay as PR #19 words them.
  - MODIFIED (`CAS/pc:886`):
    `### Requirement: Clean records a reconcilable result for every removal target`.
    Three rows of the exit table (`:949-956`): row 2 gains a branch stage the
    post-check could not establish, row 4 a removed target whose
    `branch_retirement` is not plain, and row 5 a plain one, a keep the plan
    names included, for every target under the flag. Its eight scenarios stay
    verbatim.
  - Untouched (`CAS/pc:1034`):
    `### Requirement: Clean reports every path exactly or excludes it`.
  - Untouched (`CAS/pc:1091`):
    `### Requirement: Clean plans and refusals are versioned JSON`.
    Its plan envelope is a listed set of fields ("When a plan is built it SHALL
    be the plan envelope: ...", `CAS/pc:1094-1100`), so the envelope gains no
    key; the two per-target sub-records, `branch_plan` on each `selected` entry
    and `branch_retirement` on each target, follow L-10's pattern and are stated
    in the ADDED requirement (L-4), which says that they extend this
    requirement's keys for those objects under the flag only (lane
    openRepoProject-3's L10); a new key is not "a rename, removal, type change
    or change of meaning" (`CAS/pc:1129-1131`), no enum value, refusal code or
    note code is added, and `--apply --json` stays accepted with `--all-safe`
    and `--action remove` only.
  - ADDED:
    `### Requirement: Clean retires a removed worktree's branch only on fresh head and ancestry evidence`.
    The flag and its argument rules; the plan's keeps and the reflog proof;
    the flagged plan lines, the `branch_plan` sub-record of each `selected`
    entry and the digest's `retire` member;
    the branch stage, its re-read, checks, branch child and post-check; never
    force, never remote, never a retry; the `branch_retirement` sub-record and
    its reasons; the stop rule; the bound and the counts; the question,
    summary line, branch lines, next commands and stop block. Twenty-three
    scenarios.
- `project-clean-review-safety` (all four canonical requirements and change
  1's one ADDED one accounted for):
  - Untouched (`:9`): `### Requirement: Cleanup protects the process worktree`.
  - Untouched (`:21`; MODIFIED by change 1 at `CAS/rs:3`):
    `### Requirement: Cleanup preserves all local work not proven disposable`.
    The plan's reflog proof keeps a branch whose reflog names unmerged work,
    so that the flag never removes local work not proven disposable.
  - Untouched (`:38`):
    `### Requirement: Cleanup respects configured upstream mappings`.
  - Untouched (`:49`; MODIFIED by change 1 at `CAS/rs:60`):
    `### Requirement: Cleanup revalidates destructive actions`.
    Its first sentence requires a re-inspection before "local branch
    deletion" and its MUST a refusal on any difference from the reviewed plan.
    Under ruling A-14 the stage's re-read compares every value of the branch's
    evidence that the requirement's removal revalidation compares
    (`CAS/rs:77-82`: `branch`, `head`, `upstream`, `upstream_oid`, `ahead`,
    `behind`, the manifest's `tracking_branch` and the merge target) and
    retains the branch on any difference or unreadable value, so the MUST is
    met, not narrowed, and nothing here is contradicted. Its sentence "Push and
    delete-branch SHALL keep the full re-inspection" (`CAS/rs:96-98`) names the
    explicit actions; the flag's stage is neither, and its targeted re-read is
    the ADDED requirement's.
  - MODIFIED (`CAS/rs:194`):
    `### Requirement: Cleanup states a narrow guarantee and its residual window`.
    "Cleanup SHALL never delete a branch, so that a branch race cannot lose
    commits" (`:210-211`) holds without the flag; under it, a second guarantee
    covers the branch child, naming the plan's reflog proof and the values the
    re-read compares, the race outcomes are stated, and the residual window
    names a branch changed after its last check. Its three scenarios stay
    verbatim and one is added.
- `project-command` (change 1's three requirements, two MODIFIED and one
  ADDED, accounted for; every other canonical requirement untouched):
  - Untouched (`CAS/cmd:3` and `CAS/cmd:64`): `### Requirement: Inspect and
    diagnose` and `### Requirement: Explicit maintenance`.
  - MODIFIED (`CAS/cmd:90`, on PR #19's text; HELD, written in the worktree
    and not committed until lane openRepoProject-2 checks its diff, ruling
    A-20):
    `### Requirement: Repository inspection requires Git 2.36 and shares one evidence model`.
    One sentence in Termination, in the form of PR #19's own push-child
    carve-out: the branch child of `clean --retire-branches` is waited for on
    every exit path, as a removal child is, and signalled only past the budget
    the ADDED requirement gives it, and it is none of the delete-branch
    children that Budgets leaves unbounded; and one clause in Budgets: the
    re-read of a branch stage gets `min(5 s, work remaining less the removal
    floor)`. Its nine scenarios stay as PR #19 words them.
- `project-review-safety` and `speckit-extension-integration`: untouched.
  `project-overview`, change 2's new capability: untouched, because its
  suggestion is exactly `["project", "clean", "<root>", "--all-safe"]` or
  `["project", "clean", "<root>"]` and never carries `--apply`
  (`APO/ov:484-487`); it never carries the flag either (A-6), although the
  flagged preview now exists.

## Impact

- **`project`**: inside the seam feature 004 builds (slice 6 of
  `specs/004-project-clean-all-safe/plan.md` on branch
  `004-project-clean-all-safe`, re-checked at `4e3af0a`, where its tasks build
  it as `apply_removals(plan, run)`; `design.md` Context), the flag, its
  argument rules, the plan's keeps and the reflog proof, the `branch_plan`
  sub-record and the digest's `retire` member, the branch stage after the
  rescan, the `branch_retirement` sub-record, the three exit rows, the question,
  the summary and branch lines, the next commands, the stop block's branch
  reason and the residual-window line; the parser's `clean` flags
  (`project:1109-1117` today) gain `--retire-branches`. The explicit
  `delete-branch` path (`project:723-735`) is unchanged. No new dependency, no
  network.
- **`README.md`**: "Clean up Git worktrees" (`README.md:178-201`) gains the
  flag, its flagged preview, its opt-in contract, the keeps, the stop and the
  retry path, and says that a merged branch whose worktree is already gone
  stays with `delete-branch`, one branch per command; "deleting its local
  branch is a separate action" (`README.md:197-198`) names the flag as that
  separate, explicit request.
- **`tests/test_project.py`**: the default path's test,
  `test_clean_removes_only_merged_worktree_and_keeps_branch` (`tests:857`),
  stays unchanged; each scenario this change adds gets a test named after it
  (A-7), with feature 004's fixtures and counting wrapper, fake `git`s for each
  branch-child outcome (`design.md` D9), test hooks after the rescan and after
  the re-read, and change 1's counting wrapper recording the branch child's
  pins, directory, environment and arguments. Tests run as change 1 runs
  them, `python3 -m unittest discover -s tests -v`, on the CI workflow's jobs:
  since PR #32, one `test` job on `ubuntu-latest` for Python 3.10 and 3.12
  (`.github/workflows/tests.yml` at `origin/main` `e9d6711`), and feature
  004's `git-floor` job once it lands (L-12).
- **Speckit handoff**: one feature, numbered when `/speckit.specify` runs
  after ratification, 006 or later (L-7).

### Dependencies and Sequencing

- **On change 1** (L-1, L-15). Written on change 1's ratified text at
  `961c405`, which main `e9d6711` keeps unchanged; change 1 is still
  unarchived (2026-10-19). Every block this change MODIFIES is written on
  change 1's text or PR #19's, and five of the seven are change 1's ADDED
  requirements (batch, bounds, reconcilable result, narrow guarantee, the
  project-command evidence model), so this change cannot archive before change
  1 does (`openspec
  archive` fails a MODIFIED block whose header is not in the main spec);
  `validate --strict` passes meanwhile. Change 1 archives after feature 004
  merges. Change 1 lists the apply result's `completeness` (`CAS/pc:1138`)
  without saying when it is incomplete: this change states its own trigger, a
  null `branch_retirement` `stage`, inside its ADDED requirement, and when
  change 1's own result is incomplete is lane openRepoProject-2's text to
  settle in change 1 (A-11). It does not block this change.
- **On PR #19** (L-1, L-15, L-16). Two blocks are written on PR #19's text,
  still a draft at `c462d87`: "Clean bounds its Git work and reports omitted
  work", and the held project-command block "Repository inspection requires
  Git 2.36 and shares one evidence model" (ruling A-20); this change's other
  blocks are byte-identical on `main` and PR #19. Ratifying this change ratifies
  those two blocks only as written on PR #19's text at `c462d87`, not PR #19's
  own sentences, which stay PR #19's to ratify (lane openRepoProject-3's M1);
  before the Speckit handoff, `tasks.md` 2.2 re-reads both against PR #19's
  merged text, or against change 1's archived text if PR #19 closes unmerged.
  This change therefore archives after PR #19's amendment of change 1 lands.
- **The project-command block, held** (ruling A-20). Change 1's Termination
  paragraph names probe children, killed on every exit path, and removal
  children, waited for; the branch child, waited for on a signal and stopped
  only past its budget, is neither, so lane openRepoProject-3's M2 asked for a
  sentence naming it. Lane openRepoProject-2 will not widen PR #19 before Brett
  Heap rules on it, so this change carries the block itself:
  - it is written on PR #19's text (ruling L-16), so this change archives after
    PR #19's amendment of change 1 lands;
  - `add-project-overview-remote-merge-status` (issue #25, PR #29) is to MODIFY
    the same requirement, its block pending in that change's own fix round, and
    by L-11 whichever of the two archives second re-bases on the first's
    archived block;
  - lane openRepoProject-2 checks the block's diff against PR #19's block
    before it is committed; until then it is written in the worktree and not
    committed;
  - if Brett Heap has PR #19 absorb the clause (lane openRepoProject-2's LQ-6),
    this block is dropped and this change cites PR #19 instead.
- **Archive order** (L-5, L-11, A-13). Change 1, then
  `add-project-clean-cache-disposal` (issue #24, draft PR #27, lane
  openRepoProject-5), then this change. PR #27 is an unratified draft (its
  Status at `9ebe9f0`: "alignment review resolved on PR #27; council pending;
  nothing here is ratified"; lane openRepoProject-3's M4). Under the lane's
  ruling B-10 the cache change MODIFIES five of the requirements this change
  MODIFIES, so this change carries the cache change's archived block of each
  of the five and re-bases each on it before it archives:
  - "Clean can explicitly retire verified worktrees": the cache change adds one
    clause to the removal sequence, before the spawn, that no edit here
    touches.
  - "Clean previews and applies a batch of eligible worktree removals in one
    repository": both changes extend the digest's canonical text, the cache
    change for a plan that selects a cache target (B-10) and this change under
    the flag, so the re-based sentence carries both members; this change's
    other two sentences, the question and the summary line, are elsewhere in
    the block. The flagless invariant and the place of `retire` are stated
    against the base text: today change 1's digest input, `retire` its last
    member after the selected triples. Once re-based on the cache change's
    archived block, the invariant becomes byte-identical to the cache
    change's digest input, and `retire` goes after its per-target cache data,
    which follows each triple; the ADDED AND for a flagged plan with a cache
    target pins that order, and is checked again at the re-base (`tasks.md`
    2.3 and 3.2).
  - "Clean bounds its Git work and reports omitted work": both rewrite the
    counting sentence, merged as "a removal, or a branch child of
    `--retire-branches`, under `operations`, every other child, a cache
    enumeration included, under `probes`, and each cache entry that a cache
    stage removes counted once under `operations`"; both add a stage sentence
    after the removal floor, the cache stage's and the branch stage's, which
    sit side by side; and where the cache change's fit sentence says that the
    16th target reaches its spawn with more than the removal floor left, which
    the flag makes false at the packet's costs, the re-based block scopes it to
    runs without `--retire-branches` (`design.md` D7).
  - "Clean records a reconcilable result for every removal target": the cache
    change makes its descriptor-relative deletion of listed cache paths the one
    exception to "`project` SHALL never force a removal or delete a directory
    itself" (B-10); this change's edits are exit rows 2, 4 and 5.
  - "Cleanup states a narrow guarantee and its residual window": the cache
    change names the revalidation its guarantee means for a cache target
    (B-10); this change extends the guarantee to the branch child, and the
    residual-window line of a flagged run whose plan also selects a cache
    target names both (`design.md` D8).

  If PR #27 is not ratified, this change's five shared blocks re-base on change
  1's archived text instead, and A-9's joint fit with cache disposal is moot.
  "Clean reports local worktree state" is shared with no other open change.
  `add-project-overview-remote-merge-status` archives after change 2 and, apart
  from the project-command block above, touches no capability here.
- **Change 1's open question 2** (lane openRepoProject-3's M3). Branch
  retirement follows change 1's eligibility, whose only removal proof today is
  local ancestry (`BA:195-199`). If Brett Heap rules that question 2 admits
  removal evidence other than local ancestry (CAS `proposal.md:1001-1005`), a
  row removed on that evidence lacks the ancestry the stage relies on. Before
  this change archives, such a branch must then become a keep the plan names,
  with a reason of the sub-record's own enum, so that it never stops the run
  and is never retired. No behaviour changes now.
- **Implementation.** The stage lives in feature 004's seam, so this change's
  feature is specified after feature 004 merges and change 1 archives; it
  never alters the order of feature 004 or feature 005. Whichever of this
  feature and the cache-disposal feature merges second merges `main` in.
  Never rebase: the organisation ruleset refuses force pushes. Lane
  openRepoProject-1's issue #20 and PR #21 touch `new()` only.

## Out of Scope

- **Cache disposal** (issue #24) and **remote merge status** (issue #25), each
  its own change.
- **The explicit `delete-branch` action's own behaviour**, its unbounded
  child and its `--json` refusal.
- **Remote branch deletion, force deletion, and `update-ref -d`** (Open
  Questions).
- **Branches whose worktree is already gone.** The flag retires only the
  branch of a worktree that it removes in the same run. A merged branch left by
  an earlier run, with or without the flag, stays with `delete-branch`, one
  branch per command; a batch over such branches would be its own change.
- **Squash-merged branches**, which never prove ancestry (change 1's open
  question), and **patch-equivalent reflog commits** (`git cherry`), so that a
  rebased or amended branch is kept (Open Questions).
- **The ladder, the gates, the fifteen classes, the closed `stage` enum, the
  overview's finding codes and the CI matrix.**
- **PR #2's command-root workaround** (`1789ad9`'s `cleanup_command_root`,
  `bb91a49`'s verification of it): every child after resolution runs in the
  command directory, the main worktree (`CAS/pc:244`; `BA:845-846`), so no
  surviving target worktree is needed; a branch Git would judge against that
  directory's `HEAD` is kept by the plan instead (A-17).
- **Cherry-picking PR #2**: `5fc2b51`, and `branch_still_merged` (`1789ad9`)
  and `git_common_dir` (`bb91a49`), are reference only; nothing applies
  cleanly to the pipeline feature 004 builds.

## Decisions Taken by This Proposal

Each is a proposal decision, open to ratification. The lane's rulings are
applied as stated; packet open decisions taken cite the text that leaves them
open:

- **Opt-in, by a flag on the removal apply and the batch preview** (A-1, as
  amended; `BA:1339` "If paired retirement is proposed later", and `OV:356`
  "The final command and flag spelling"). `--retire-branches`, never the
  default, because "implicit local branch deletion" is a non-goal
  (`OV:150-152`) and the confirmation names "their retained local branches"
  (`BA:76-77`); `5fc2b51`'s unconditional deletion is rejected. Spelling: Open
  Questions.
- **The flag is a separate, explicit action** (a reading put to ratification;
  lane openRepoProject-3's L6). The canonical "It SHALL remove a local branch
  only as a separate, explicit action after the worktree is gone and the branch
  is verified merged" (`project-clean/spec.md:59-60`) and "unless the user
  separately requests branch deletion" (`:63-68`) are read as met by a flag the
  person gives explicitly, whose stage runs separately after the rescan proves
  the worktree gone; the archived design's "a separate opt-in action"
  (`2026-10-07-add-project-clean-command/design.md:17-18`) and `BA:36-38`'s "a
  later explicit action" are read the same way. Ratifying this change ratifies
  that reading; the alternative, an amendment of those sentences, is not taken
  because both stay true of every run without the flag.
- **The primitive: a re-read, then non-force `branch -d`** (A-2;
  `BA:1340-1341` names the check, not the command). The rejected alternative,
  `git update-ref -d refs/heads/<b> <sha>`, compares atomically but skips
  Git's checked-out refusal and merge test and leaves the `branch.<b>`
  section; Open Questions carries the fact that reopens it.
- **Every plain `removed` target qualifies unless the plan keeps its branch**
  (A-3; not in the packet). Upstream live or deleted; the deleted case is the
  lane's ruling A-3, which applies Brett Heap's ruling of 2026-10-09, recorded
  for worktree rows, as its proof rule (lane openRepoProject-3's L7).
- **The plan keeps what it can foresee** (A-16, A-17, A-18; the packet leaves
  the case open). A branch whose reflog names a commit the merge target lacks
  (`reflog-unmerged`), one a worktree outside the selection holds
  (`branch-in-use`), one Git would judge against a command-directory `HEAD`
  that is not the merge target's SHA (`head-not-merge-target`), and the earlier
  holders of a shared branch (`branch-shared`) are kept by the plan, printed
  and counted as kept, and recorded `not-attempted`. The reflog proof is the
  canonical "Cleanup preserves all local work not proven disposable"
  (`project-clean-review-safety/spec.md:21`) applied to the reflog the deletion
  removes; change 1 already reads that reflog for its `unstarted-branch` gate.
  The rejected alternative, letting the stage discover these and stop, would
  remove one worktree per run, retire no branch, and print a retry Git refuses
  the same way (council findings S-1, P-1, AE-3).
- **A sub-record, not new stage values** (A-4, L-4; `BA:1319-1321` "stage
  values of its own"). Read as satisfied by the sub-record's own `stage`;
  change 1's enum is untouched. The sub-record is present only under the flag
  and absent without it, never null for "not applicable" (L-10), because null
  keeps change 1's meaning, unknown or not established (`CAS/pc:1128-1129`);
  the alternative, the key on every target and null without the flag, is
  rejected for that reason.
- **What stops the run** (A-4, as amended; the packet says only "stops later
  targets"). A retention the stage discovers stops the run and exits 2, ordered
  inside change 1's exit table; a keep the confirmed plan names does not, and
  that row exits as it would in a flagless run.
- **No new `limits` or `budget` member** (A-5; `BA:1321-1322` "its bounds in
  `limits`"). The stage spawns one branch child per target, so
  `limits.targets` (16) caps branch children, and
  `budget.probe_timeout_seconds` bounds each; a `limits.branch_retirements`
  member is rejected as always equal to `limits.targets`.
- **The target cap of a flagged run stays 16** (A-9; the packet's fit rule,
  `BA:729-735`, leaves the caps to measurement, `BA:766-771`). With the cache
  change archived first and the reflog proof's one child, a flagged run at the
  packet's 150 ms per child brings 13 of its 16 targets through their stage
  before the removal floor, 11 in the worst case of 17 reflog children; change
  1's own deadline rule makes the rest `not-attempted` with
  `deadline-exceeded`, exit 1, taken by the next run and never unsafe
  (`BA:772-774`); at change 1's measured costs all 16 fit (`design.md` D7).
  The alternative, a lower target cap under the flag (8 by the packet's rule),
  is rejected: the cap is applied by the `deferred-target-cap` gate, so the
  flag would change the selection. Put to Brett Heap (Open Questions).
- **The digest binds the flag** (A-1, as amended; council finding AE-2). Under
  the flag the digest's canonical text also carries `retire`, the branches the
  plan retires with their planned SHAs, so a flagless preview's digest, which
  a reviewer approved with every branch kept, never authorizes a flagged
  apply; without the flag the text and value are change 1's. Each `selected`
  entry carries a `branch_plan` sub-record, so that a JSON preview shows what
  the digest binds; the plan envelope, a listed set of fields in change 1
  (`CAS/pc:1094-1100`), gains no key.
  The rejected alternatives: a digest that ignores the flag, the draft's first
  choice, which let a flagless approval delete up to 16 branches under `--yes`;
  and refusing `--expect-plan` with the flag, which would leave every scripted
  flagged apply unbound.
- **The result names every branch** (A-19, P-2). The human result prints one
  line per branch of a removed target, with the retired branch's SHA and
  restore command, or the kept branch's reason and a next step that never
  prints a retry the plan knows will fail and never suggests `-D`; every
  command printed for the person to run next carries the flag, so that
  following the tool's own advice never strands a branch whose worktree a
  flagless run removed.

Readings of the rulings against the sources, each named where it narrows or
departs:

- **A-2's ancestry "at its current tip", read with the canonical MUST.**
  `project-clean-review-safety/spec.md:51-53` requires a refusal "when the
  state no longer matches the reviewed plan", and the merge target is part of
  that plan. The stage therefore requires the merge target to re-resolve to
  the plan's name, source and SHA; ancestry at the current tip is then the
  plan's own proof and needs no Git child, as change 1's revalidation reasons
  (CAS `design.md` D7). A merge target that moved, even forward, retains the
  branch with `state-changed`. This is narrower than A-2's text, which would
  retire a branch whose target moved forward.
- **The re-read's values** (A-14). It compares every value of the branch's
  evidence that change 1's removal revalidation compares (`CAS/rs:77-82`): the
  branch's head, `upstream`, `upstream_oid`, `ahead` and `behind`, the
  manifest's `tracking_branch`, the merge target's name, source and SHA, and
  the checked-out state. A-14 names `tracking_branch`, `upstream` and
  `upstream_oid`; `ahead` and `behind` are added because A-14 asks for every
  value that applies to a branch, lane openRepoProject-3's H1 names them, and
  the same listing carries them, so no child is added. What is proven, and so
  what a deletion cannot lose, is every commit the branch's head or its reflog
  names: the plan proves them merged, or keeps the branch. The branch's
  `branch.<b>` section goes with it (`design.md` Risks). The repository
  identity is the one the rescan re-established, which a target `removed` with
  reason null requires (`CAS/pc:919-921`).
- **A-16's reflog proof, as amended on 2026-10-19.** A commit is named when it
  is the new object or the non-zero old object of a reflog entry, the oldest
  surviving entry's old object included, so that a commit that `git reflog
  expire` has left named only as an old object is proven merged too; the first
  text named new objects only, and the writer's report raised the gap. The proof
  is the ruling's form, with no extra child, one child per repository and one
  per row only when it prints a commit. A failure or timeout of the repository's
  child fails every row's proof, so every selected branch is kept.
- **The plan's keep order.** `reflog-unmerged`, then `branch-in-use`, then
  `head-not-merge-target`, then `branch-shared`, so that the next step printed
  for a kept branch never leads to deleting work only its reflog holds: the
  `head-not-merge-target` advice ends in a `delete-branch` retry, which Git's
  merge test would let through for a branch whose head is merged.
- **Children per target, and the fit** (A-5, as amended twice). The stage spawns
  the re-read that A-2 requires, the branch child, and a post-check that change
  1's evidence rule requires ("The child's exit status alone SHALL never prove a
  removal", `CAS/pc:919`; null for what is not established, `CAS/pc:1128-1129`),
  and the plan spawns the reflog proof (A-16): up to 65 more children per run,
  16 under `operations` and 49 under `probes`. A-5's first text said "up to 16
  more children"; the lane amended it to 48 on 2026-10-18 and its verdict of
  2026-10-19 adds the reflog children, and the departure from the first text
  stands as recorded. The branch child spawns only while more than the 5 s
  removal floor remains. At the packet's assumed 150 ms per child its fit rule
  (`BA:729-735`) fails for a flagged run of 16 targets: the 15th removal spawns
  at 44.55 s, but its branch child, due at 45.45 s, cannot start, so 15
  worktrees are removed and 14 branches retired, the 16th target deferred. The
  caps stay on change 1's measured fit (CAS `tasks.md` 2.1: the 16th removal at
  23.6 s; about 30.5 s with the 45 stage children before it and one reflog child
  at 150 ms each, about 32.9 s with 17), as change 1 kept them on its
  measurement; a slower repository leaves its last targets `not-attempted` with
  `deadline-exceeded`, exit 1, never unsafe (`BA:772-774`). This departs from
  the packet's rule for flagged runs; the joint fit with the cache change is
  A-9's decision above.
- **Where the stage's probes are counted** (lane openRepoProject-3's L5). The
  packet defines a target's `probes_performed` as "the Git children of that
  target's revalidation ... at most 5" (`BA:1039-1042`, `BA:1422`), so the
  target's count stays that, and the stage's re-read and post-check are counted
  in the sub-record's own `probes_performed`. The next target's revalidation
  keeps change 1's sourcing, the rescan's repository children (feature 004's
  T085), and a merge target moved during a branch stage is caught by the next
  target's own re-read (`clarifications.md`, S-4).
- **A-4's three stage values, and null.** When the post-check cannot decide,
  `stage` is null with reason `reconciliation-incomplete`, by change 1's null
  rule; a fourth value `unknown` is rejected to keep A-4's list.
- **A-4's `branch-retention-stop`** is carried by the later targets'
  `branch_retirement`; their own reason stays change 1's `batch-stopped`
  (`CAS/pc:906-908`), because a new reason in the target's closed enum is what
  L-4 avoids. A-4's "their removal and branch stages become `not-attempted`,
  reason `branch-retention-stop`" is read that way.
- **The sub-record's `git-refused` and `git-failed`** (lane openRepoProject-3's
  L8) name the branch child's outcome, the branch present or absent after a
  nonzero exit; the target enum splits the same two names at exit status 128.
  The ADDED requirement says so rather than renaming them, since the verdicts
  name `git-refused` as the stage's outcome.
- **A-15 against the spawn floor.** Under A-5 as amended the branch child
  spawns with its whole 5 s budget, so the work deadline never stops it and
  `retired` with `deadline-exceeded` is unreachable; it is dropped. `retired`
  with a reason stays reachable, as `git-failed` (a child that deletes and then
  exits nonzero) and `probe-timeout` (one that deletes and then hangs), and
  A-15's scenario keeps those two.
- **A-6's summary line on every apply result under the flag**, extended so its
  counts add up: `Removed N; branches retired: R; retained: K`, with `;
  already gone: G` when G is above 0, R, K and G counting the distinct branches
  of the removed targets; it replaces `Removed N; branches kept: ` and precedes
  the branch lines and the stop block, which ends the result
  (`CAS/pc:962-964`).
- **A-6's question counts distinct branches.** A-6 words it "Remove N
  worktrees and retire their N local branches?", but two selected worktrees
  can hold one branch (the second added with `git worktree add --force`), and
  under A-4 as amended it counts only the branches the plan retires and names
  the kept ones: `Remove N worktrees and retire their M local branches?
  [yes/N]` when none is kept, and `Remove N worktrees, retire M local branches
  and keep K? [yes/N]` when K are, M and K being distinct branches and
  `branch` singular for 1. Change 1's `keeping N branches` has the same shape
  and is lane openRepoProject-2's to settle in change 1.
- **A-1's `--json`** is read as `--json` accepted with the flag in every form
  change 1 accepts it, as change 1's OQ-10 allows `--apply --json` "for
  removal only" and keeps it refused "with `--action push` or `delete-branch`"
  (CAS `proposal.md:735-737`). Change 1's push requirement keeps its scenario
  "Push and branch deletion stay human-only", which tests the explicit
  `delete-branch` action with `--json`; that refusal stays and the requirement
  is untouched.
- **A-1's "single-target preview if change 1 has one".** Change 1 has none: its
  single-target removal is `--apply --action remove --worktree P` only, so the
  flagged preview is `--all-safe --retire-branches`.
- **A branch child is waited for on a signal.** Within its budget, as a
  started removal is never interrupted (change 1's V1), because a ref
  transaction killed part-way can leave a lock to clear by hand; past its
  budget it is stopped like a probe.

Packet decisions adopted, not open: the paired-retirement contract
(`BA:1339-1345`) whole, the seam rule (`BA:1318-1322`), the retry path
(`BA:1281-1293`) and the deferred scenario (`BA:1635-1636`), carried as the
ADDED scenario "A branch moved after removal is retained and can be retried".

The lane's rulings, where each lands: L-1 (drafted on change 1 and PR #19;
Dependencies), L-2 (citations), L-3 (Capabilities), L-4 (sub-record; Open
Questions), L-5 (archive order), L-6 (Status; issue #23), L-7 (Speckit
numbering), L-8 (draft only; the review tables below), L-9 (no host path);
A-1 to A-7 as above. The addendum of 2026-10-18: L-10 (keys absent without
the flag; What Changes, Decisions, the ADDED requirement, `design.md` D5),
L-11 (placement; Capabilities, Dependencies), L-12 (CI; Impact, `design.md` D9
and the Migration Plan, `tasks.md` 3.1), L-13 (commit trailers), L-14
(`tasks.md` 1.2), L-15 (base text; the citation key and Dependencies); A-5 as
amended and A-9 (Decisions; Open Questions; `design.md` D7), A-10 (Open
Questions), A-11 (Dependencies; `design.md` D5), A-12 (Impact; `design.md`
Context), A-13 (Dependencies; `tasks.md` 2.3 and 3.2), A-14 (What Changes,
Capabilities, Decisions; the deltas; `design.md` D4) and A-15 (the ADDED
scenarios; `design.md` D5, D9). The council verdicts of 2026-10-19 are listed
in "Council Verdicts" below.

## Corrections to the Packet

For lane openRepoProject-3, the packet's owner, to edit; this change reads the
packet and does not edit it (lane openRepoProject-3's L11):

- **`BA:1339-1341`** ("uses the reconciliation record's `branch_sha` as the
  expected head"). Non-force `git branch -d` on Git 2.43 deletes with no
  expected old value (`design.md` Context), and the only atomic primitive,
  `update-ref -d <old>`, skips Git's merged and checked-out refusals, against
  `BA:1344-1345`. The packet should state a paired-retirement residual window,
  as `BA:305-325` does for removal (lane openRepoProject-3's P1).
- **`BA:1343-1344`** ("The existing explicit `delete-branch` command remains
  the retry path"). Since question 1 (2026-10-09), a merged branch whose
  remote-tracking ref was deleted is judged by `branch -d` against the command
  directory's `HEAD`, so the retry fails the same way whenever the main
  worktree is off the merge target; this change keeps such a branch at plan
  time and prints the checkout under which the retry succeeds (lane
  openRepoProject-3's P2).
- **`BA:437-440`.** The removal floor is stated for removals only; this change
  applies it to the branch child, an extension's mutation, as the cache change
  applies it to its cache stage (lane openRepoProject-3's P8).

## Open Questions

Each is before Brett Heap with a recommendation; the deltas implement the
recommendation, and a different ruling edits them before ratification.

- **Enum closure** (L-4). Change 1 says "Enums SHALL be closed within a schema
  version" (`CAS/pc:1129-1131`); change 2 says adding "an enum value is
  additive" (`APO/ov:656-658`). This change adds keys with enums of their own
  and no value to any existing enum, so the disagreement does not bind it.
  Recommendation: rule that an extension's states live in its own sub-record,
  which makes the question moot for the three extensions.
- **The flag's spelling** (A-1). Recommendation: `--retire-branches`, after
  the requirement it extends, "Clean can explicitly retire verified
  worktrees"; `--delete-branches` names Git's verb, but `delete-branch` is
  already the explicit action, and two near spellings invite a slip.
- **The deletion primitive, with a fact found for this proposal** (A-2). On Git
  2.43.0, `git branch -d` deletes the ref without an expected old value: its
  `reference-transaction` hook receives an all-zeros old value, for a loose
  and for a packed ref, while `git update-ref -d refs/heads/<b> <sha>` passes
  the SHA and refuses "is at X but expected Y". A branch moved between Git's
  own read and its deletion is therefore deleted unchecked. Options: (a) keep
  `branch -d` (A-2), whose checked-out refusal and merge test stay the last
  defense, the window inside one Git process being the residual, as change 1
  accepts "any change made after Git's own check" for a removal; (b) `git
  update-ref -d refs/heads/<b> <observed_sha>`, an atomic compare that skips
  Git's checked-out refusal and merge test and leaves the `branch.<b>`
  section, which reads as the force deletion `BA:1344-1345` forbids.
  Recommendation: (a).
- **The target cap of a flagged run** (A-9). With
  `add-project-clean-cache-disposal` archived first, a run with
  `--retire-branches` whose plan also selects cache targets reaches the removal
  floor at its 14th target under the packet's 150 ms per child: with the reflog
  proof's one child, 13 of its 16 targets are removed and their branches
  retired, and in the worst case of 17 reflog children 12 are removed and 11
  retired; change 1's deadline rule leaves the rest `not-attempted` with
  `deadline-exceeded`, exit 1, for the next run, never unsafe. At change 1's
  measured costs all 16 fit, the 16th removal spawning near 32.9 s, or 35.3 s in
  that worst case (`design.md` D7). Options: (a) keep `limits.targets` 16 for
  every run; (b) a lower cap under the flag, 8 by the packet's rule
  (`BA:729-735`), which would make the flag change the selection.
  Recommendation: (a), keep 16.
- **Merge-target candidates** (A-10). Under the flag the stage can retire a
  merged local branch named `main` or `master`, or one that a
  `refs/remotes/<r>/HEAD` names, when it is not the plan's merge target:
  `protected-default` covers only the merge-target branch (`project:569-570`),
  and the explicit `delete-branch` action protects only that branch too
  (`project:727-728`). No commit can be lost, because the branch is merged
  into the merge target and its remote copy is untouched. Options: (a) no rule
  now; (b) retain such a branch, with a reason of the sub-record's own enum, so
  that no target enum changes (L-4). Recommendation: (a), no rule.
- **Patch-equivalent reflog commits** (A-16). Should a commit that a branch's
  reflog names, and whose patch the merge target carries (`git cherry`), count
  as merged, so that branches rebased or amended before their merge also
  retire? Options: (a) no: such a branch is kept with `reflog-unmerged` and
  named in the result, and `delete-branch` stays its explicit path after the
  person inspects `git reflog BRANCH`; (b) yes: one more bounded child per
  failing row compares patches, and a branch whose every unmerged reflog commit
  has an equivalent patch in the merge target retires. Recommendation: (a), no,
  for this MVP.

## Questions Resolved by the Alignment Review

Stack-architect and qa-lead findings on `e7f3e65` (2026-10-11); the lane's
rulings of 2026-10-18 bind where they differ. The last seven rows are the
rulings that answered the review's GAPs and its joint-fit and carry findings.

| Findings | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| SA-1: the re-read's compared values, the identity it rests on, and the reach of "Push and delete-branch SHALL keep the full re-inspection" were unstated | DRIFT | applied; its optional widening of step 2 (`tracking_branch`, `upstream`, `upstream_oid`) not taken, since no ruling asks for it and the re-read follows the explicit action's re-check (`project:658-663`) | Capabilities (review-safety `:49`); Decisions, readings ("The re-read's values"); review-safety delta (narrow guarantee); `design.md` D4 |
| SA-2: the carry of the cache change was understated, and the joint fit and the residual-window line of a flagged cache run were unstated | DRIFT | applied with change: under B-10 and A-13 the two changes share five MODIFIED requirements, not two, each named with its re-base; the cache change's fit sentence is scoped only where it says the 16th target clears the floor, since that change's own fix round may reword it | Dependencies and Sequencing; `design.md` D7, D8, Migration Plan; `tasks.md` 2.3, 3.2 |
| SA-3: the departure from the packet's fit rule (`BA:729-735`) was not named in Decisions | DRIFT | applied, beside A-5 as amended | Decisions, readings ("Three children per target") |
| SA-4: `retire_worktree` was attributed to feature 004's plan, which never names it | DRIFT | applied; the attach points re-checked at feature 004's head `66d60b6` (A-12) | What Changes (branch stage); Impact (`project`); `design.md` Context |
| SA-5: one review-safety spec line ran to 127 characters | DRIFT | applied | review-safety delta |
| QA-1: `branch-retention-stop` and `target-not-removed` overlapped, and neither covered a signal or deadline stop after a plain retirement | MISMATCH | applied with change: `branch-retention-stop` needs the earlier target to be `removed`, because the review's text would give it to every target after a `refused`, `failed` or `unknown` one, whose own sub-record is not a plain retirement, against QA-3's new scenario; the `not-attempted` lead-in reads "no branch remained to retire, or no stage ran", since `branch-missing` can follow the re-read; the SIGTERM AND also pins `branch-retention-stop` otherwise | project-clean delta (ADDED: the `not-attempted` reasons; "A signal around the branch child"); `design.md` D5, D6 |
| QA-2: "`operations.estimated` twice the selected targets" stops being true once the cache change archives first | MISMATCH | applied, in the lane's words ("the flag adds one per target") | project-clean delta (ADDED); What Changes ("Bounded like a probe"); `design.md` D7 |
| QA-3: no scenario for `target-not-removed`, for `branch-missing` at the re-read, or for the summary line with K above 0 | GAP | applied as given: one scenario added ("A removal that does not end removed under the flag") and one AND, 53 scenarios; the finding's other cases (`retained` with `spawn-error` or `removal-ceiling`, `retired` with a reason) carry no replacement text and stay without a scenario of their own | project-clean delta (ADDED); Capabilities (ADDED, sixteen scenarios); `tasks.md` 1.4 |
| QA-4: the question counted N branches for N worktrees, wrong when two worktrees hold one branch | MISMATCH | applied with change: the pinned question is an AND run without `--yes`, because the scenario runs with `--yes`, which asks nothing | project-clean delta (ADDED; "A branch another worktree holds is retained"); What Changes; Decisions, readings; `design.md` D8 |
| A-5 amended (GAP: A-5's "up to 16 more children" against the draft's 48) | GAP | ruling: the flag adds up to 48 children per run, 16 under `operations` and 32 under `probes`, and the departure stands | Decisions, readings; `design.md` D7 |
| L-10 (GAP: the sibling convention for result sub-records) | GAP | ruling: a sub-record is present only where its extension acts and absent otherwise, never null for "not applicable" | What Changes; Decisions; project-clean delta (ADDED); `design.md` D5 |
| A-10 (GAP: merge-target candidates under the flag) | GAP | ruling: no rule now; put to Brett Heap, recommendation "no rule", with the alternative | Open Questions |
| A-11 (GAP: change 1 does not say when its apply result is incomplete) | GAP | ruling: this change keeps its own trigger, a null `stage`, in its ADDED requirement; change 1's triggers are lane openRepoProject-2's to settle | Dependencies and Sequencing; `design.md` D5 |
| A-12 (GAP: feature 004 moved past `dd923ee`) | GAP | ruling: re-check the attach points at the branch's current head; done at `66d60b6` | Impact; `design.md` Context |
| A-9 (SA-2, SA-3; the cache change's review, G3) | DRIFT | ruling: state the joint fit (13 of 16 at the packet's costs, all 16 at change 1's measured costs), keep `limits.targets` 16, and put it to Brett Heap, recommendation "keep 16" | Decisions; Open Questions; `design.md` D7 |
| A-13 (SA-2) | DRIFT | ruling: name every requirement shared with the cache change and re-base each on its archived block before archiving (L-11) | Dependencies and Sequencing; `design.md` Migration Plan; `tasks.md` 2.3, 3.2 |

The review agreed with the writer's eight flagged items, the changes it asked
for being the findings above; its optional citation for item (5), CAS
`proposal.md:735-737`, is added to the A-1 reading, and item (8), the commit
trailer, stands. The common rulings L-11 to L-15 are applied where the
Decisions list says. Two rows are superseded by the council round below:
SA-1's optional widening, not taken then, is taken by ruling A-14, and QA-3's
three remaining cases have their scenarios under ruling A-15, `retired` with
`deadline-exceeded` excepted, which the spawn floor makes unreachable; the
re-read's values and the fit are stated as they now stand under Decisions.

### Council Verdicts

The council (product-advocate P-1 to P-4, systems-architect S-1 to S-4,
adversary-engineer AE-1 to AE-4, read-only) reviewed `874d1ad` on 2026-10-19;
the lane lead's verdicts bind: 11 VALID, 1 NOTED (S-4, in
`clarifications.md`), 0 DISMISSED. Three of the council and lane
openRepoProject-3's M5 found the top problem independently: a retention the
plan can foresee stopped the batch, and its printed retry failed the same way.
Lane openRepoProject-3's packet-fidelity read of `874d1ad` (H1, M1 to M6, L1
to L12) was applied in the same round; its rows follow the council's.

| Concern | Severity | Verdict | Section changed |
| --- | --- | --- | --- |
| P-1: the printed retry fails the same way for two retentions the plan can foresee, and Git then advises `-D` | HIGH | VALID (A-17, A-19): such branches are kept by the plan, and each kept branch's line gives a next step that works, never `-D` | What Changes; Decisions; project-clean delta (ADDED); `design.md` D4, D8 |
| P-2: the next commands printed drop the flag | MEDIUM | VALID (P-2): the deferral line and the stop block's `Next:` carry the flag; scenario "A flagged run's next commands keep the flag" | What Changes; Decisions; project-clean delta (ADDED); `design.md` D8 |
| P-3: the human result names no retired branch or SHA | MEDIUM | VALID (A-19): one line per branch, `Retired BRANCH (was SHA); restore: git branch BRANCH SHA`; Rollback cites the SHAs both results print | project-clean delta (ADDED); `design.md` D8, Rollback |
| P-4: Why never says who benefits | LOW | VALID: Why names merge-commit and fast-forward repositories, with counts measured 2026-10-19 and no names, and the squash and rebase cases; Out of Scope and the README line name branches whose worktree is already gone | Why; Out of Scope; Impact (README) |
| S-1: an upstream-gone branch is judged against the command directory's `HEAD` and the batch stops | HIGH | VALID (A-17): plan-time keep `head-not-merge-target`, no child, no stop; the restated scenario is "A branch Git would judge against another HEAD is kept", and "Git refuses the branch deletion" now uses a fake `git` | project-clean delta (ADDED); `design.md` D3, D4, Risks |
| S-2: the branch child has no spawn floor | MEDIUM | VALID (A-5 as amended): the re-read and branch child start only while more than the 5 s removal floor remains, the strict test council B on PR #27 asked for, the re-read under `min(5 s, work remaining less the removal floor)`; the deadline scenario gains the AND; `retired` with `deadline-exceeded` dropped as unreachable | What Changes; Capabilities (bounds); project-clean delta; held project-command block; `design.md` D3, D5, D7 |
| S-3: a branch two worktrees hold stops the batch | LOW | VALID (A-18): `branch-shared` for earlier holders, the stage at the last; `branch-in-use` at plan time for a holder outside the selection; a holder found only at the stage still stops | project-clean delta (ADDED); `design.md` D4, Risks |
| S-4: D2's reuse of the post-check listing is in no requirement and collides with T085 | LOW | NOTED: D2's substitution deleted; the next target's own re-read catches a moved merge target; T085 untouched | `clarifications.md`; `design.md` D2 |
| AE-1: retiring a branch deletes its reflog, the last reference to amended-away work | HIGH | VALID (A-16, amended 2026-10-19 to name each entry's non-zero old object as well as its new one, the oldest surviving entry's old object included, with no extra child): the plan's reflog proof keeps such a branch (`reflog-unmerged`); the "loses no commit" and "lossless" claims now say what is proven; Risks names the `branch.<b>` keys; new Open Question on patch equivalence | What Changes; Rules; Decisions; Open Questions; both deltas; `design.md` D4, Risks |
| AE-2: the digest ignores the flag, so a flagless approval authorizes deletions | MEDIUM | VALID (A-1 as amended): the flagged preview exists, the digest carries `retire` under the flag, and a flagless digest refuses a flagged apply; the Out of Scope bullet on previews is deleted; "Clean reports local worktree state" MODIFIED for its digest sentence (L-11); a JSON preview shows each row's planned action in a `branch_plan` sub-record on its `selected` entry, the plan envelope, a listed set of fields in change 1, gaining no key | What Changes; Capabilities; Decisions; Out of Scope; project-clean delta; `design.md` D1, D10 |
| AE-3: two foreseeable retentions stop the batch every run | MEDIUM | VALID (A-17, A-18, A-4 as amended): plan-time keeps never stop the run; applied with change: no `merge-base --is-ancestor` child at plan time, the ruling taking the SHA test instead | Decisions; project-clean delta; `design.md` D4, D6 |
| AE-4: the human result keeps no record of what it deleted | LOW | VALID (A-19): as P-3 | project-clean delta (ADDED); `design.md` D8, Rollback |
| A-20 (the lead's ruling on lane 3's M2, after lane openRepoProject-2's answer) | ruling | applied: the project-command block is MODIFIED on PR #19's text and HELD uncommitted for lane openRepoProject-2's check, with the five Dependencies points | Capabilities (project-command); Dependencies and Sequencing; `design.md` D3, Migration Plan |
| Council B's refinements for this change (the lead, 2026-10-19, from council B on PR #27) | ruling | applied: the re-read and the branch child start only while more than the floor remains, the branch child never abandoned at its budget; the flagless invariant and `retire`'s place stated against the base text, with the re-base note; one AND for a flagged plan with a cache target | What Changes; Capabilities (bounds); Decisions; Dependencies and Sequencing; project-clean delta; `design.md` D3, D7, D10 |
| H1: the re-read applies the revalidation MUST selectively | HIGH | applied (A-14): the re-read compares `upstream`, `upstream_oid`, `ahead`, `behind` and `tracking_branch` as well, retaining with `state-changed`; `ahead` and `behind` beyond A-14's list, from the same listing | Capabilities (review-safety `:49`); Decisions; both deltas; `design.md` D4 |
| M1: ratifying #26 would ratify PR #19's pending text | MEDIUM | applied: the two blocks on PR #19's text are ratified only as written there, and 2.2 re-reads them before the handoff | Dependencies and Sequencing; `tasks.md` 1.6, 2.2; `design.md` Migration Plan |
| M2: project-command's child rules do not account for the branch child | MEDIUM | applied with change, per A-20: change 1's Termination paragraph is exhaustive about the two kinds it names, so the requirement is MODIFIED, on PR #19's text, held | Capabilities (project-command); Dependencies and Sequencing |
| M3: question 2 would be decided by default | MEDIUM | applied with change, per the verdicts: a Dependency, no new behaviour now; lane 3's fix of qualifying only `merged_into_target` rows is not taken | Dependencies and Sequencing |
| M4: PR #27 relied on without being called a draft | MEDIUM | applied: PR #27 named as an unratified draft, with what changes if it is not ratified | Dependencies and Sequencing |
| M5: the printed retry is known to fail | MEDIUM | settled by A-17 and A-19 | as P-1 |
| M6: the branch child has no start floor | MEDIUM | settled by A-5 as amended | as S-2 |
| L1: `OV:142-146` is the wrong citation | LOW | applied: `OV:173-180` and `OV:357-358` | Why |
| L2: `README.md:178-200` is off by one | LOW | applied: `README.md:178-201`, twice | citation key; Impact |
| L3: `BA:1344-1345` is broader than its source | LOW | applied: `BA:1295` for no automatic retry, `BA:195-196` and `SY:221-226` for local evidence | Rules This Change Keeps |
| L4: canonical lines cited for change-1-only text | LOW | applied: `CAS/pc:105-111`, `CAS/pc:180` and `CAS/pc:223-228` beside the canonical lines | Capabilities |
| L5: the stage's listings counted in `probes_performed` | LOW | applied: the target's `probes_performed` stays the packet's; the stage's are in the sub-record's own `probes_performed` | Decisions; project-clean delta (ADDED); `design.md` D5, D7 |
| L6: "separate, explicit action" reinterpreted | LOW | applied: listed under Decisions as a reading put to ratification | Decisions |
| L7: question 1's ruling applied beyond its recorded scope | LOW | applied: the extension attributed to A-3, Brett Heap's ruling cited as its proof rule | What Changes; Decisions; `design.md` D4 |
| L8: `git-refused` and `git-failed` reused with other meanings | LOW | applied: the ADDED text says so; not renamed, since the verdicts name `git-refused` as the stage's outcome | project-clean delta (ADDED); Decisions; `design.md` D5 |
| L9: D2's sourcing change in no spec delta | LOW | applied, as S-4: revalidation keeps its own listing | `design.md` D2; `clarifications.md` |
| L10: the JSON requirement enumerates keys | LOW | applied: the ADDED requirement says its keys extend those lists under the flag | Capabilities; project-clean delta (ADDED); `design.md` D10 |
| L11: "Corrections to the Packet: None" | LOW | applied: lane 3's P1, with P2 and P8, which this change also bears on | Corrections to the Packet |
| L12: testability gaps | LOW | applied: scenarios or ANDs for a re-read fault, `retired` with `git-failed` and `probe-timeout`, `retained` with `spawn-error` and `removal-ceiling`, `branch-missing-after-removal`, a holder in the main worktree, the estimated and performed counts, the scrub and process group, the stage listings' directory, the stop block, the one-target question, null `command` and `exit_status`, the single-target `--json`, the exact plan lines and a slow fake `git`; `retired` with `deadline-exceeded` left out as unreachable | project-clean delta (ADDED) |
