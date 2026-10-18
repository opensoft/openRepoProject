Lane: openRepoProject-5

# Proposal: add-project-clean-branch-retirement

Status: draft; alignment review resolved on PR #26; council pending; nothing
here is ratified. Governing issue: opensoft/openRepoProject#23, claimed by lane
openRepoProject-5 (comment 6111211798); refs #6, the record of the project
maintenance design packet. Proposed on Brett Heap's word "usage reset, resume
all. read handoff and resume and fan out wide and do as much as possible in
parallel" (2026-10-11), read by lanes openRepoProject-4 and openRepoProject-5
as a go for the candidate list they put to him.

Citations are `file:line` at `da33d92`, which equals `961c405` for
`ideation/`. `BA`, `OV`, `SY` and `HO` are the packet's
`project-maintenance-batch-cleanup.md`, `project-maintenance-overview.md`,
`project-maintenance-synthesis-inspect-and-retire.md` and
`next-session-project-maintenance-fix-handoff.md` under `ideation/brainstorm/`,
which this change reads and never edits. `CAS` is the ratified, unarchived
change `openspec/changes/add-project-clean-all-safe/` ("change 1") at
`961c405`, `CAS/pc` and `CAS/rs` its `specs/project-clean/spec.md` and
`specs/project-clean-review-safety/spec.md`; `APO` is
`openspec/changes/add-project-overview/` ("change 2"), `APO/ov` its
`specs/project-overview/spec.md`. "PR #19's text" is `CAS/pc` on draft PR #19's
branch `change/amend-clean-all-safe-push-pins` at `c462d87`, whose spec files
equal those at `5ce23d7`, the head the lane's ruling L-1 names; PR #19 is
still a draft at `c462d87` (2026-10-18). `project:N` and `tests:N` are
`project` and `tests/test_project.py` at `961c405`. Main is now `e9d6711`,
whose `openspec/` and `ideation/` equal `961c405`'s and whose `project`,
`tests/test_project.py` and `README.md:178-200` are unchanged from it, so every
citation at `961c405` holds at main (L-15). Canonical requirements are cited as
`project-clean/spec.md:N` and `project-clean-review-safety/spec.md:N` under
`openspec/specs/`. The lane lead's rulings of 2026-10-11, L-1 to L-9 and A-1 to
A-7, and its addendum of 2026-10-18, L-10 to L-15, A-5 as amended and A-9 to
A-13, bind this draft and are applied under Decisions.

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

The packet keeps paired retirement out of the batch as a separately governed
extension (`HO:47-50`; `OV:142-146`; `BA:1314-1318`) and fixes the contract
such a change must meet (`BA:1339-1345`): branch deletion is a separate
post-removal stage with an immediate branch-head and local-ancestry check that
uses the reconciliation record's `branch_sha` as the expected head; a changed
head or a Git refusal retains the branch, stops later targets and reports the
removed worktree and the surviving branch; the explicit `delete-branch`
command remains the retry path; no composite operation may force-delete or
force-push. The PR #2 decision record (comment 6035824335, on Brett Heap's word
"go with your recommendation", 2026-10-07) requires the proposal to be a
MODIFIED requirement on `project-clean`, because it changes the governed
`remove` action (`BA:60-63`; `HO:36-39`), and change 1 names it as its own
change (CAS `proposal.md:690-696`; OQ-27 at `:756-757`).

The closed PR #2's `5fc2b51` met none of that contract. It made branch deletion
unconditional for `remove`, deleted by name without checking the planned head
(PR #2 review comment 3988326415), returned Git's status as its own, and
declared no modified capability while the cleanup spec still said that removal
leaves the branch. This change is the extension the contract describes: an
opt-in flag that retires each removed worktree's local branch in the same
confirmed run, on fresh evidence, with nothing changed for a run without it.

## What Changes

- **An opt-in flag, `--retire-branches`** (A-1). It is accepted only with
  `--apply` and either `--all-safe` or `--action remove --worktree P`; with
  anything else (a preview, `--action push`, `--action delete-branch`) the
  command refuses with `invalid-arguments`, exit 2, and runs nothing. It is
  never the default: a run without it keeps every branch and prints exactly
  what change 1 prints, and its targets carry nothing new. `--apply --json` is
  accepted with the flag in the two forms change 1 accepts it for removal
  (`CAS/pc:1133-1134`). The flag changes no gate, no selection, no
  `plan_digest` and no `--expect-plan` comparison.
- **A branch stage after each proven removal** (`BA:1318-1322`,
  `BA:1339-1345`; A-2). Inside the removal seam that feature 004 builds
  (`retire_worktree`, CAS `proposal.md:189`), once a target's rescan proves it
  `removed` with reason null, so that its reconciliation record shows the
  branch present at the planned head, the stage runs before the next target is
  revalidated:
  1. it re-reads the manifest and, in one ref listing narrowed as change 1's
     revalidation listing is, the branch and the merge-target candidates;
  2. it checks, stopping at the first failure, that the branch exists, that
     its head equals the reconciliation record's `branch_sha`, that the merge
     target re-resolves to the plan's name, source and SHA, so that the plan's
     ancestry proof is the ancestry at the target's current tip, and that no
     registered worktree, the main worktree included, had the branch checked
     out in the rescan's registry listing;
  3. it spawns Git's non-force `git -c protocol.allow=never` with the six
     per-protocol pins, `-C <command directory> branch -d -- <branch>`, with
     change 1's seventeen-name environment scrub, in its own process group;
  4. it re-reads the branch in one more narrowed listing, and that post-check,
     never the child's exit status alone, decides the outcome.

  Never `-D`, `--force`, `-f`, a retry, a remote branch or a remote-tracking
  ref.
- **Which targets qualify** (A-3). Every target the run removes with reason
  null, whether its upstream lives (the remote branch stays untouched) or its
  remote-tracking ref was deleted (merged by local ancestry, Brett Heap's
  ruling of 2026-10-09, "yes, local ancestry proof outranks remote-gone, apply
  it"). Rows gated `unstarted-branch` or `reflog-unavailable` never reach
  `removed`, so they never reach the stage.
- **A per-target sub-record** (A-4, L-4, L-10). Under the flag every target of
  the apply result record carries `branch_retirement` `{stage, reason, branch,
  planned_sha, observed_sha, command, exit_status}`; `stage` is `retired`,
  `retained` or `not-attempted`, or null when the post-check could not
  establish it, and the ADDED requirement lists each reason. Without the flag
  the key is absent from every target, never null, since null keeps change 1's
  meaning, unknown or not established (`CAS/pc:1128-1129`). The target's
  `stage`, its reasons, the fifteen ladder classes, the gates, the refusal
  codes and the note codes gain no value.
- **The stop rule and the exit status** (A-4; `BA:1341-1343`). The run stops
  after the first target whose branch stage is not `retired` with reason null,
  as it stops after the first target that is not a plain `removed`; each later
  target is `not-attempted` with change 1's `batch-stopped` and carries
  `branch_retirement` `not-attempted` with `branch-retention-stop`. A retained
  branch exits 2, unless an earlier row of change 1's exit table decides first:
  a signal (130, 143, 129), the deadline, or a stage the post-check could not
  establish (1).
- **Bounded like a probe** (A-5). The re-read and the branch child each get
  `min(5 s, work remaining)` and the post-check `min(5 s, reserve remaining)`;
  a branch child in flight is waited for within its budget when a signal
  arrives and stopped like a probe past it. The branch child counts under
  `operations` and the two listings under `probes`, so `operations.estimated`
  gains one per target and `probes.estimated` two. A run with no removal in
  flight still ends within 64 s of its start. The explicit
  `delete-branch` action's child stays unbounded, as change 1 says of it.
- **What the person sees** (A-6, A-7). The plan marks each selected branch for
  retirement; the question reads `Remove N worktrees and retire their M local
  branches? [yes/N]`, M counting distinct branches; every apply result prints
  `Removed N; branches retired: R; retained: K`, then each retained branch
  with its retry command, `project clean <root> --apply --action delete-branch
  --branch <b>` (`BA:1281-1293`); a stop ends with change 1's stop block, the
  branch's reason in it; and the residual-window line names a branch changed
  after its last check. The overview never suggests the flag: its suggestion
  is exactly one of two argument vectors and never carries `--apply`
  (`APO/ov:484-487`).
- **The narrow guarantee under the flag** (MODIFIED review-safety). Change 1's
  "Cleanup SHALL never delete a branch" stays true without the flag. With it,
  the guarantee extends to the branch child, the branch race keeps change 1's
  outcomes, a change seen by the re-read retains the branch, and a change after
  the re-read is the residual, guarded only by Git's own non-force check. Git
  2.43's `branch -d` deletes without comparing the ref to the value its own
  check read (verified for this proposal: its `reference-transaction` hook
  receives an all-zeros old value), so that window ends inside Git (Decisions;
  Open Questions).

## Rules This Change Keeps

- **Never force.** No `branch -D`, `--force`, `-f`, forced removal, force
  push, reset, fetch or automatic retry (`BA:1344-1345`); the canonical "MUST
  never use a force removal, reset, or deletion of unmerged work"
  (`project-clean/spec.md:61`) stays verbatim.
- **Never by default.** Without `--retire-branches` removing a worktree leaves
  its branch (`BA:36-38`), and branch deletion stays "a separate opt-in
  action" (archived `2026-10-07-add-project-clean-command/design.md:17-18`);
  "implicit local branch deletion" stays a non-goal (`OV:150-152`;
  `SY:232-235`).
- **Never a remote branch.** Remote branches and remote-tracking refs remain
  untouched (`BA:1293`; archived design `:83-84`).
- **`delete-branch` stays the retry path, unchanged** (`BA:1281-1293`,
  `BA:1343-1344`).
- **Local evidence only.** The stage reads refs, the registry and the
  manifest; it never fetches, and no remote status approves a deletion
  (`SY:129-130`; `project-clean/spec.md:12-16`).
- **Revalidate before every destructive action, and fail closed**
  (`project-clean-review-safety/spec.md:51-53`): the re-read is that
  re-inspection, and a mismatch, or a value it cannot read, retains the
  branch.
- **Nothing unconfirmed.** The question names the branches to retire, and
  `--yes` accepts the fresh plan as change 1 defines it.
- **Evidence decides.** The post-check decides the outcome, and a value not
  established is null, never a default (`CAS/pc:919`, `CAS/pc:1128-1129`).
- **Stop at the first failure.** No continuation, rollback or retry
  (`CAS/pc:246-248`).
- **Change 1's contract unchanged.** Its enums, ladder, gates, caps, digest
  and refusal codes keep their values (L-4).

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
(L-3); the change stays in `project-clean` and `project-clean-review-safety`.

### Modified Capabilities

Headers are quoted verbatim, one per line; the ADDED header is proposed text.
Canonical lines are at `961c405`; change 1's ADDED requirements are cited at
their `CAS` line.

- `project-clean` (all five canonical requirements and change 1's six ADDED
  ones accounted for):
  - Untouched (`:10`): `### Requirement: Clean reports local worktree state`.
    The flag adds no report field; the report stays read-only.
  - Untouched (`:25`):
    `### Requirement: Clean classifies preservation and cleanup actions`.
    No class is added and the fifteen names stay (L-4).
  - Untouched (`:39`):
    `### Requirement: Clean can explicitly push safe feature branches`.
    Its scenario "Push and branch deletion stay human-only" concerns the
    explicit `delete-branch` action's `--json` refusal, which stays
    (Decisions).
  - MODIFIED (`:55`; change 1's text at `CAS/pc:230`):
    `### Requirement: Clean can explicitly retire verified worktrees`.
    The one sequence gains the branch stage, for a target the rescan proves
    `removed` with reason null and only under the flag; the stop rule gains a
    branch stage that does not end `retired` with reason null; after the
    sentence "It SHALL remove a local branch only as a separate, explicit
    action after the worktree is gone and the branch is verified merged."
    (`:59-60`, kept verbatim) one sentence names `--retire-branches` as such a
    separate, explicit action, never the default. "It MUST never use a force
    removal, reset, or deletion of unmerged work." (`:61`) and all fourteen of
    change 1's scenarios, `Remove a merged clean worktree` (`:63-68`) and
    `Every branch remains after a batch` among them, stay verbatim; both
    describe runs without the flag.
  - Untouched (`:70`): `### Requirement: Clean hands off work requiring review`.
    `--all-safe` and `--yes` keep their meaning as action target and
    confirmation.
  - Untouched (`CAS/pc:443`): `### Requirement: Clean resolves its target Git-first`.
    The flag adds no mode; it resolves as `--all-safe` and `--action remove`
    do.
  - MODIFIED (`CAS/pc:566`):
    `### Requirement: Clean previews and applies a batch of eligible worktree removals in one repository`.
    Two sentences only: the question names the branches to retire under the
    flag (`:635-637`), and the success line gives way to the flag's summary
    line (`:655-656`). Its ten scenarios stay verbatim.
  - MODIFIED (`CAS/pc:767`, on PR #19's text):
    `### Requirement: Clean bounds its Git work and reports omitted work`.
    Two sentences only: PR #19's counting sentence puts the branch child
    under `operations` beside a removal, and the unbounded-children sentence
    (`:788-789`) is scoped to push children and the explicit `delete-branch`
    action's children, the flag's branch child being bounded (A-5). Its five
    scenarios stay as PR #19 words them.
  - MODIFIED (`CAS/pc:886`):
    `### Requirement: Clean records a reconcilable result for every removal target`.
    Three rows of the exit table (`:949-956`): row 2 gains a branch stage the
    post-check could not establish, row 4 a removed target whose branch stage
    did not end `retired` with reason null, and row 5 that stage for every
    target under the flag. Its eight scenarios stay verbatim.
  - Untouched (`CAS/pc:1034`):
    `### Requirement: Clean reports every path exactly or excludes it`.
  - Untouched (`CAS/pc:1091`):
    `### Requirement: Clean plans and refusals are versioned JSON`.
    The sub-record is stated in the ADDED requirement (L-4); no enum value,
    refusal code or note code is added, and `--apply --json` stays accepted
    with `--all-safe` and `--action remove` only.
  - ADDED:
    `### Requirement: Clean retires a removed worktree's branch only on fresh head and ancestry evidence`.
    The flag and its argument rules; the branch stage, its re-read, checks,
    branch child and post-check; never force, never remote, never a retry;
    the `branch_retirement` sub-record and its reasons; the stop rule; the
    bound and the counts; the question, summary line, stop block and retry
    command. Sixteen scenarios.
- `project-clean-review-safety` (all four canonical requirements and change
  1's one ADDED one accounted for):
  - Untouched (`:9`): `### Requirement: Cleanup protects the process worktree`.
  - Untouched (`:21`; MODIFIED by change 1 at `CAS/rs:3`):
    `### Requirement: Cleanup preserves all local work not proven disposable`.
  - Untouched (`:38`):
    `### Requirement: Cleanup respects configured upstream mappings`.
  - Untouched (`:49`; MODIFIED by change 1 at `CAS/rs:60`):
    `### Requirement: Cleanup revalidates destructive actions`.
    Its first sentence already requires a re-inspection before "local branch
    deletion" and its MUST a refusal on any difference from the reviewed plan;
    the stage's re-read is that re-inspection, retaining the branch on a
    difference, and the ADDED requirement states it, so nothing here is
    contradicted (Decisions). Its sentence "Push and delete-branch SHALL keep
    the full re-inspection" (`CAS/rs:96-98`) names the explicit actions; the
    flag's stage is neither, and its targeted re-read is the ADDED
    requirement's.
  - MODIFIED (`CAS/rs:194`):
    `### Requirement: Cleanup states a narrow guarantee and its residual window`.
    "Cleanup SHALL never delete a branch, so that a branch race cannot lose
    commits" (`:210-211`) holds without the flag; under it, a second guarantee
    covers the branch child, the race outcomes are stated, and the residual
    window names a branch changed after its last check. Its three scenarios
    stay verbatim and one is added.
- `project-command`, `project-review-safety` and
  `speckit-extension-integration`: untouched. `project-overview`, change 2's
  new capability: untouched, because its suggestion is exactly
  `["project", "clean", "<root>", "--all-safe"]` or
  `["project", "clean", "<root>"]` and never carries `--apply`
  (`APO/ov:484-487`), so it can never carry the flag (A-6).

## Impact

- **`project`**: inside the seam feature 004 builds (slice 6 of
  `specs/004-project-clean-all-safe/plan.md` on branch
  `004-project-clean-all-safe`, re-checked at `66d60b6`, where its tasks build
  it as `apply_removals(plan, run)`; `design.md` Context), the flag, its
  argument rules, the branch stage after the rescan, the
  `branch_retirement` sub-record, the three exit rows, the question, the
  summary line, the stop block's branch reason and the residual-window line;
  the parser's `clean` flags (`project:1109-1117` today) gain
  `--retire-branches`. The explicit `delete-branch` path (`project:723-735`)
  is unchanged. No new dependency, no network.
- **`README.md`**: "Clean up Git worktrees" (`README.md:178-200`) gains the
  flag, its opt-in contract, the stop and the retry path; "deleting its local
  branch is a separate action" (`README.md:197-198`) names the flag as that
  separate, explicit request.
- **`tests/test_project.py`**: the default path's test,
  `test_clean_removes_only_merged_worktree_and_keeps_branch` (`tests:857`),
  stays unchanged; each scenario this change adds gets a test named after it
  (A-7), with a fake `git` whose `branch -d` exits 0 without deleting, one
  whose `branch -d` ignores SIGTERM, test hooks after the rescan and after the
  re-read, and change 1's counting wrapper recording the branch child's pins,
  directory and arguments. Tests run as change 1 runs them, `python3 -m
  unittest discover -s tests -v`, on the CI workflow's jobs: since PR #32,
  one `test` job on `ubuntu-latest` for Python 3.10 and 3.12
  (`.github/workflows/tests.yml` at `origin/main` `e9d6711`), and feature
  004's `git-floor` job once it lands (L-12).
- **Speckit handoff**: one feature, numbered when `/speckit.specify` runs
  after ratification, 006 or later (L-7).

### Dependencies and Sequencing

- **On change 1** (L-1, L-15). Written on change 1's ratified text at
  `961c405`, which main `e9d6711` keeps unchanged; change 1 is still
  unarchived (2026-10-18). Four of the five blocks this change MODIFIES
  (batch, bounds, reconcilable result, narrow guarantee) are change 1's ADDED
  requirements, so this change cannot archive before change 1 does (`openspec
  archive` fails a MODIFIED block whose header is not in the main spec);
  `validate --strict` passes meanwhile. Change 1 archives after feature 004
  merges. Change 1 lists the apply result's `completeness` (`CAS/pc:1138`)
  without saying when it is incomplete: this change states its own trigger, a
  null `branch_retirement` `stage`, inside its ADDED requirement, and when
  change 1's own result is incomplete is lane openRepoProject-2's text to
  settle in change 1 (A-11). It does not block this change.
- **On PR #19** (L-1, L-15). "Clean bounds its Git work and reports omitted
  work" is written on PR #19's text, still a draft at `c462d87`; its other
  blocks are byte-identical on `main` and PR #19. If PR #19 lands, this block
  is its text plus this change; if PR #19 changes or closes first, the block
  is re-based before ratification.
- **Archive order** (L-5, L-11, A-13). Change 1, then
  `add-project-clean-cache-disposal` (issue #24, lane openRepoProject-5), then
  this change. Under the lane's ruling B-10 the cache change MODIFIES every
  requirement this change MODIFIES, so this change carries the cache change's
  archived block of each of the five and re-bases each on it before it
  archives:
  - "Clean can explicitly retire verified worktrees": the cache change adds one
    clause to the removal sequence, before the spawn, that no edit here
    touches.
  - "Clean previews and applies a batch of eligible worktree removals in one
    repository": the cache change extends `plan_digest` for a plan that
    selects a cache target (B-10); this change's two sentences, the question
    and the summary line, are elsewhere in the block.
  - "Clean bounds its Git work and reports omitted work": both rewrite the
    counting sentence, merged as "a removal, or a branch child of
    `--retire-branches`, under `operations`, every other child, a cache
    enumeration included, under `probes`, and each cache entry that a cache
    stage removes counted once under `operations`"; and where the cache
    change's fit sentence says that the 16th target reaches its spawn with
    more than the removal floor left, which the flag makes false at the
    packet's costs, the re-based block scopes it to runs without
    `--retire-branches` (`design.md` D7).
  - "Clean records a reconcilable result for every removal target": the cache
    change makes its descriptor-relative deletion of listed cache paths the one
    exception to "`project` SHALL never force a removal or delete a directory
    itself" (B-10); this change's edits are exit rows 2, 4 and 5.
  - "Cleanup states a narrow guarantee and its residual window": the cache
    change names the revalidation its guarantee means for a cache target
    (B-10); this change extends the guarantee to the branch child, and the
    residual-window line of a flagged run whose plan also selects a cache
    target names both (`design.md` D8).

  `add-project-overview-remote-merge-status` (issue #25) archives after change
  2 and touches neither capability here.
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
- **A preview form of the flag**: `--all-safe --retire-branches` without
  `--apply` refuses; the preview stays change 1's.
- **Squash-merged branches**, which never prove ancestry (change 1's open
  question).
- **The ladder, the gates, the fifteen classes, the closed `stage` enum, the
  overview's finding codes and the CI matrix.**
- **PR #2's command-root workaround** (`1789ad9`'s `cleanup_command_root`,
  `bb91a49`'s verification of it): every child after resolution runs in the
  command directory, the main worktree (`CAS/pc:244`; `BA:845-846`), so no
  surviving target worktree is needed.
- **Cherry-picking PR #2**: `5fc2b51`, and `branch_still_merged` (`1789ad9`)
  and `git_common_dir` (`bb91a49`), are reference only; nothing applies
  cleanly to the pipeline feature 004 builds.

## Decisions Taken by This Proposal

Each is a proposal decision, open to ratification. The lane's rulings are
applied as stated; packet open decisions taken cite the text that leaves them
open:

- **Opt-in, by a flag on the removal apply** (A-1; `BA:1339` "If paired
  retirement is proposed later", and `OV:356` "The final command and flag
  spelling"). `--retire-branches`, never the default,
  because "implicit local branch deletion" is a non-goal (`OV:150-152`) and
  the confirmation names "their retained local branches" (`BA:76-77`);
  `5fc2b51`'s unconditional deletion is rejected. Spelling: Open Questions.
- **The primitive: a re-read, then non-force `branch -d`** (A-2;
  `BA:1340-1341` names the check, not the command). The rejected alternative,
  `git update-ref -d refs/heads/<b> <sha>`, compares atomically but skips
  Git's checked-out refusal and merge test and leaves the `branch.<b>`
  section; Open Questions carries the fact that reopens it.
- **Every plain `removed` target qualifies** (A-3; not in the packet).
  Upstream live or deleted, by Brett Heap's ruling of 2026-10-09.
- **A sub-record, not new stage values** (A-4, L-4; `BA:1319-1321` "stage
  values of its own"). Read as satisfied by the sub-record's own `stage`;
  change 1's enum is untouched. The sub-record is present only under the flag
  and absent without it, never null for "not applicable" (L-10), because null
  keeps change 1's meaning, unknown or not established (`CAS/pc:1128-1129`);
  the alternative, the key on every target and null without the flag, is
  rejected for that reason.
- **Exit 2 for a retained branch** (A-4; the packet says only "stops later
  targets"), ordered inside change 1's exit table.
- **No new `limits` or `budget` member** (A-5; `BA:1321-1322` "its bounds in
  `limits`"). The stage spawns one branch child per target, so
  `limits.targets` (16) caps branch children, and
  `budget.probe_timeout_seconds` bounds each; a `limits.branch_retirements`
  member is rejected as always equal to `limits.targets`.
- **The target cap of a flagged run stays 16** (A-9; the packet's fit rule,
  `BA:729-735`, leaves the caps to measurement, `BA:766-771`). With the cache
  change archived first, a flagged run at the packet's 150 ms per child brings
  only 13 of its 16 targets to their stage before the removal floor; change
  1's own deadline rule makes the rest `not-attempted` with
  `deadline-exceeded`, exit 1, taken by the next run and never unsafe
  (`BA:772-774`); at change 1's measured costs all 16 fit (`design.md` D7).
  The alternative, a lower target cap under the flag (8 by the packet's rule),
  is rejected: the cap is applied by the `deferred-target-cap` gate, so the
  flag would change the selection, the digest and `--expect-plan`'s
  comparison. Put to Brett Heap (Open Questions).
- **The plan digest ignores the flag.** The flag changes no selection, so an
  `--expect-plan` digest taken from a preview, which cannot carry the flag,
  matches an apply with it; the question names the branches to retire. No
  plan-envelope field records the flag; under it every result target carries
  `branch_retirement` and `operations.estimated` counts the branch children.

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
- **The re-read's values.** It compares the branch's head, the merge target's
  name, source and SHA, and the checked-out state, as the explicit action's
  re-check compares head, target and ancestry (`project:658-663`), not the
  upstream evidence or the manifest's `tracking_branch` that change 1's
  removal revalidation compares (`CAS/rs:77-82`): a head unchanged and an
  ancestor of an unchanged merge target loses no commit when deleted
  (`BA:1339-1341`). The repository identity is the one the rescan
  re-established, which a target `removed` with reason null requires
  (`CAS/pc:919-921`).
- **Three children per target, as A-5 amended records.** The stage spawns the
  re-read that A-2 requires, the branch child, and a post-check that change
  1's evidence rule requires ("The child's exit status alone SHALL never prove
  a removal", `CAS/pc:919`; null for what is not established,
  `CAS/pc:1128-1129`): up to 48 more children, 16 under `operations` and 32
  under `probes`. A-5's first text said "up to 16 more children"; the lane
  amended it to this count on 2026-10-18, and the departure from its first
  text stands as recorded. `design.md` restates the fit. At the packet's
  assumed 150 ms per child its fit rule (`BA:729-735`) fails for a flagged run
  of 16 targets: the 16th removal would spawn at 45.9 s, 0.9 s inside the 5 s
  floor. The caps stay on change 1's measured fit (CAS `tasks.md` 2.1: the
  16th removal at 23.6 s; about 30.4 s with the 45 stage children before it at
  150 ms each), as change 1 kept them on its measurement; a slower repository
  leaves its last targets `not-attempted` with `deadline-exceeded`, exit 1,
  never unsafe (`BA:772-774`). This departs from the packet's rule for flagged
  runs; the joint fit with the cache change is A-9's decision above.
- **A-4's three stage values, and null.** When the post-check cannot decide,
  `stage` is null with reason `reconciliation-incomplete`, by change 1's null
  rule; a fourth value `unknown` is rejected to keep A-4's list.
- **A-4's `branch-retention-stop`** is carried by the later targets'
  `branch_retirement`; their own reason stays change 1's `batch-stopped`
  (`CAS/pc:906-908`), because a new reason in the target's closed enum is what
  L-4 avoids. A-4's "their removal and branch stages become `not-attempted`,
  reason `branch-retention-stop`" is read that way.
- **A-6's summary line on every apply result under the flag.** Exit 0 needs
  every branch retired, so `retained` is 0 there and counts only on a stop;
  the line replaces `Removed N; branches kept: ` and precedes the stop block,
  which ends the result (`CAS/pc:962-964`).
- **A-6's question counts distinct branches.** A-6 words it "Remove N
  worktrees and retire their N local branches?", but two selected worktrees
  can hold one branch (the second added with `git worktree add --force`), so
  the question reads `Remove N worktrees and retire their M local branches?
  [yes/N]`, M being the number of distinct branches of the selected rows and
  `branch` singular when M is 1. Change 1's `keeping N branches` has the same
  shape and is lane openRepoProject-2's to settle in change 1.
- **A-1's `--json`** is read as `--apply --json` accepted with the flag in
  both forms change 1 accepts, as change 1's OQ-10 allows it "for removal
  only" and keeps it refused "with `--action push` or `delete-branch`" (CAS
  `proposal.md:735-737`). Change 1's push requirement keeps its scenario "Push
  and branch deletion stay human-only", which tests the explicit
  `delete-branch` action with `--json`; that refusal stays and the requirement
  is untouched.
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
A-1 to A-7 as above. The addendum of 2026-10-18: L-10 (sub-record absent
without the flag; What Changes, Decisions, the ADDED requirement, `design.md`
D5), L-11 (placement; Dependencies), L-12 (CI; Impact, `design.md` D9 and the
Migration Plan, `tasks.md` 3.1), L-13 (commit trailers), L-14 (Status;
`tasks.md` 1.2), L-15 (base text; the citation key and Dependencies); A-5 as
amended and A-9 (Decisions; Open Questions; `design.md` D7), A-10 (Open
Questions), A-11 (Dependencies; `design.md` D5), A-12 (Impact; `design.md`
Context) and A-13 (Dependencies; `tasks.md` 2.3 and 3.2).

## Corrections to the Packet

None.

## Open Questions

Each is before Brett Heap with a recommendation; the deltas implement the
recommendation, and a different ruling edits them before ratification.

- **Enum closure** (L-4). Change 1 says "Enums SHALL be closed within a schema
  version" (`CAS/pc:1129-1131`); change 2 says adding "an enum value is
  additive" (`APO/ov:656-658`). This change adds a field with enums of its own
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
  floor at its 14th target under the packet's 150 ms per child: 13 of its 16
  targets reach their stage, and change 1's deadline rule leaves the rest
  `not-attempted` with `deadline-exceeded`, exit 1, for the next run, never
  unsafe; at change 1's measured costs all 16 fit, the 16th spawning near
  32.8 s (`design.md` D7). Options: (a) keep `limits.targets` 16 for every run;
  (b) a lower cap under the flag, 8 by the packet's rule (`BA:729-735`), which
  would make the flag change the selection, the digest and `--expect-plan`'s
  comparison. Recommendation: (a), keep 16.
- **Merge-target candidates** (A-10). Under the flag the stage can retire a
  merged local branch named `main` or `master`, or one that a
  `refs/remotes/<r>/HEAD` names, when it is not the plan's merge target:
  `protected-default` covers only the merge-target branch (`project:569-570`),
  and the explicit `delete-branch` action protects only that branch too
  (`project:727-728`). No commit can be lost, because the branch is merged
  into the merge target and its remote copy is untouched. Options: (a) no rule
  now; (b) retain such a branch, with a reason of the sub-record's own enum, so
  that no target enum changes (L-4). Recommendation: (a), no rule.

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
Decisions list says.

### Council Verdicts

| Concern | Severity | Verdict | Section changed |
| --- | --- | --- | --- |
