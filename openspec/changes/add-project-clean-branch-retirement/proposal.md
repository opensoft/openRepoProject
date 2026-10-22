Lane: openRepoProject-5

# Proposal: add-project-clean-branch-retirement

Status: draft; alignment review and council resolved on PR #26; ratification
by Brett Heap pending; round A3 applied lane openRepoProject-3's re-read of
`ca96701`, Codex's findings on `785a45e` and the lane's rulings A-21 to A-23;
round A4 applied Codex's finding on `abad010` under the lane's ruling A-24;
round A5 applied lane openRepoProject-3's delta read of `9ff8202`, Codex's two
findings on `9ff8202` and the cache change's worst shapes at `e1049b2` under
the lane's rulings A-25 to A-28; round A6 applied lane openRepoProject-3's
folded read of `9b67e8c`, four LOW wording items, under the lane's ruling A-29;
round A7 applied the lane's review wave of 2026-10-21 on `01b5dd8`, its
readers RA, RD and RE, under the lane's rulings A-30 to A-34;
round A8 applied lane openRepoProject-3's confirm read of round A7,
`01b5dd8..48e8119`, its F1 to F10, under the lane's ruling A-35, Codex
having found no major issue in `48e8119`;
round A9 applied the lane's reader RF's final composition read of
`55375ce`, its M2, L1, L2 and L3 and this change's share of its M1, under
the lane's ruling A-37, the fit stated at PR #19's `c462d87` and `6f2cb54`,
and lane openRepoProject-3's confirm read of round A8, its LOW-2, under
A-36, Codex having found no major issue in `55375ce`;
round A10 applied lane openRepoProject-3's confirm read of round A9, its
LOW-2 to LOW-5, stated the fit at PR #19's `a664799` and aligned the branch
stage's re-read with PR #19's revalidation rule there, under the lane's
ruling A-38 and the lead's refinement of it, Codex having found no major
issue in `d5896fc`;
round A11 applied lane openRepoProject-3's confirm read of round A10, its
MEDIUM-1 and LOW-1 to LOW-5, stated the case where
`extensions.worktreeConfig` is true on the three bases of PR #19's D14 at
its round (d), `9267303`, with a flagged run's result under each option of
its LQ-20 on each basis, and worded LQ-20's option (c) as round (d) words
it, under the lane's ruling A-39 as A-40 amends it, Codex having found no
major issue in `4635bda`;
round A12 applied lane openRepoProject-3's confirm read of round A11, its
MEDIUM-1, MEDIUM-2 and LOW-1, stated the case where
`extensions.worktreeConfig` is false on PR #19's D14 measured basis,
corrected task 2.1's average per child to about 0.063 s, moved every cite of
PR #19's current text to its round (e), `f0bf538`, with option (c)'s work
deadline, invocation deadline and run bound stated on each basis, and
checked the branch stage's filesystem reads against PR #19's R-208, under
the lane's rulings A-41 and A-42, Codex having found no major issue in
`7eb0615`;
round A13 applied lane openRepoProject-2's answer on R-208 for this change and
lane openRepoProject-3's confirm read of round A12, its LOW-1 and LOW-2 and its
observations: a re-proof whose reflog read or child fails or runs past its own
budget is retained with `state-changed`, not `reflog-unmerged`, the decided
values keeping `reflog-unmerged`, `design.md` D4's manifest sentence is
narrowed to a manifest read with a `tracking_branch`, the joint fit with the
cache change is also given at the cache change's own 3.7 s for its
enumerations, and the 16th branch child's due time carries the stage's re-read
refused first at 45.02 s, under the lane's rulings A-43 and A-44, Codex having
found no major issue in `a11bde8`;
round A14 applied Codex's P2 on `1bf217c` and lane openRepoProject-3's confirm
read of round A13, its LOW-1, LOW-2 and LOW-4, with its LOW-3 kept: a next
step that told the person to remove the worktree that holds the branch now
says, for a holder that is the main worktree, which Git refuses to remove, to
switch it off the branch, in the `branch-in-use` line and the `git-refused`
hint, `branch-shared`'s holder never being the main worktree, the review-safety
sentence on a failed re-proof gains "while the work deadline is not the
limit", and the spec says that the plan does not repeat the gate's reflog
read, under the lane's rulings A-45 and A-46, Codex's review of `1bf217c`
having raised that one P2;
nothing here is ratified. Governing issue:
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
PR #19 is still a draft at `c462d87` (2026-10-19); `design.md` D7 also
states its fit on PR #19's text at `6f2cb54`, the branch's head after lane
openRepoProject-2's round of 2026-10-21, whose inputs to that fit equal those
at `1ebdd90`, where reader RF read it (ruling A-37), and at `a664799`, its
head after that lane's round (b), whose inputs to that fit equal `6f2cb54`'s
and whose D14 counts a plan-time probe on each linked row where
`extensions.worktreeConfig` is true, and at `9267303`, its head after that
lane's rounds (c) and (d), whose inputs to that fit equal `a664799`'s and
whose D14 states the fit on three bases, choosing none, and each option of
its LQ-20 on each basis (rulings A-39 and A-40), and at `f0bf538`, its head
after that lane's round (e), whose inputs to that fit and whose D14 tables
equal `9267303`'s and whose LQ-20 states option (c)'s invocation deadline
and run bound (rulings A-41 and A-42); `design.md` D4 cites PR #19's
revalidation rule at `f0bf538` (rulings A-38 and A-42).
`project:N` and `tests:N` are
`project` and `tests/test_project.py` at `961c405`. Main is now `15504f1`,
whose `ideation/` has moved from `961c405`'s with packet revision 1
(`e45155a`) and whose `openspec/changes/` adds two changes,
`refuse-non-directory-parent-early` and `support-later-python-versions`,
which modify no requirement this change modifies; its `openspec/specs/`,
change 1's and change 2's directories, `project`, `tests/test_project.py` and
`README.md:178-201` are unchanged from `961c405`, so every citation of them at
`961c405` holds at main (L-15). Canonical requirements are cited as
`project-clean/spec.md:N` and `project-clean-review-safety/spec.md:N` under
`openspec/specs/`. The lane lead's rulings of 2026-10-11, L-1 to L-9 and A-1 to
A-7, its addendum of 2026-10-18, L-10 to L-15, A-5 as amended and A-9 to A-15,
its council verdicts and addendum of 2026-10-19, A-16 to A-21, A-1, A-4 and
A-5 as amended, and L-16, its rulings of 2026-10-20, A-22 to A-29, and its
rulings on the review wave of 2026-10-21, A-30 to A-34, and its ruling on
lane openRepoProject-3's confirm read of round A7, A-35, its ruling on that
lane's confirm read of round A8, A-36, whose LOW-2 this draft applies, and
its ruling on reader RF's final composition read, A-37, and its ruling on
lane openRepoProject-3's confirm read of round A9 and on PR #19's round (b),
A-38, with the lead's refinement of it in round A10, and its ruling on
that lane's confirm read of round A10 and on PR #19's round (c), A-39, as
its ruling on PR #19's round (d), A-40, amends it, and its plan for round
A12, A-41, with that plan's addendum on PR #19's round (e), and its ruling
on that lane's confirm read of round A11, A-42, with item 3 of its ruling
B-60, and its rulings on lane openRepoProject-2's answer on R-208 for this
change, A-43, and on lane openRepoProject-3's confirm read of round A12, A-44,
and its rulings on Codex's P2 on `1bf217c`, A-45, and on lane
openRepoProject-3's confirm read of round A13, A-46, bind this draft and are
applied under Decisions and
in the round tables. That wave's readers are lane openRepoProject-5's RA (an
adversarial read of `01b5dd8`), RD (how this change, PR #27 at `fe5b245` and
PR #29 at `e11d755` compose in archive order) and RE (feature 004 at
`2cf34d3` against the three drafts), and its later reader RF re-ran RD's
composition at the final heads, this change at `55375ce`, PR #27 at
`e07cc42` and PR #29 at `3965dfb`, all cited by finding id; their files are
the lane's working records, not on the register, and the rulings name what
each found. Feature 004's code is cited at `2cf34d3` as a check only, never
as a source of this change's text. Lane records are cited on the lane register's
`origin/main`, read at `4383a6f45`: the lane logs `lanes/log/<lane>.md:N`,
which are append-only, and the lanes' handoffs under `handoffs/openRepoProject/`
at the register commit named; lane openRepoProject-3's delta read of `9ff8202`
is `attachments/lane-openRepoProject-3/delta-26-a3-findings.md` there, read at
`653112ca8`, and its folded read of `9b67e8c` is
`attachments/lane-openRepoProject-3/delta-26-a5-findings.md`, read at
`196e1c1b3`, and its confirm read of round A7, by its reader W1, is
`attachments/lane-openRepoProject-3/wave01i-a7-findings.md`, read at
`050e4492e`, cited by finding id, F1 to F10, and its confirm read of round
A8, by its reader W13, is
`attachments/lane-openRepoProject-3/confirm-a8-findings.md`, read at
`51a67d7b5`, cited by finding id, LOW-1 and LOW-2, and its confirm read of
round A9, by its reader W27, is
`attachments/lane-openRepoProject-3/confirm-a9-findings.md`, read at
`15198dfdb`, cited by finding id, LOW-1 to LOW-5, and its confirm read of
round A10, by its reader W35, is
`attachments/lane-openRepoProject-3/confirm-a10-findings.md`, read at
`98a65851b`, cited by finding id, MEDIUM-1 and LOW-1 to LOW-5, and its
confirm read of round A11, by its reader W40, is
`attachments/lane-openRepoProject-3/confirm-a11-findings.md`, read at
`1cbdc517d`, cited by finding id, MEDIUM-1, MEDIUM-2 and LOW-1, and its confirm
read of round A12, by its reader W46, is
`attachments/lane-openRepoProject-3/confirm-a12-findings.md`, read at
`44c47d893`, cited by finding id, LOW-1 and LOW-2, and by its section 1 (iii),
and its confirm read of round A13, by its reader W47, is
`attachments/lane-openRepoProject-3/confirm-a13-findings.md`, read at
`d4008061c`, cited by finding id, LOW-1 to LOW-4, and by its checks (a) to (c);
lane openRepoProject-2's answer on option (c) of PR #19's LQ-20 is recorded in
this lane's `attachments/lane-openRepoProject-5/rulings-2026-10-20.md:1193`,
read at `61f71de88`, where that line gives its time, 02:29:29Z, and its answer
on R-208 for this change in the same file at `:1456`, with rulings A-43 and
A-44 at `:1462` and `:1496`, read at `a622a156e`, where the first gives its
time, 08:16:04Z, and Codex's P2 on `1bf217c` in the same file at `:1523`, with
rulings A-45 and A-46 at `:1531` and `:1548`, read at `573fbc11a`, where the
first gives its time, 08:45:31Z.

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
  plan names never stops the run, and a reflog proof that fails or times out
  at its own budget keeps the branches it covers and leaves the plan complete.
  The proof's child reads the merge target's exclusion as the one line
  `^<merge target SHA>` on its standard input, never `--not`.
- **A branch stage after each proven removal** (`BA:1318-1322`,
  `BA:1339-1345`; A-2, A-14, A-24). Inside the removal seam that feature 004
  builds (`retire_worktree`, CAS `proposal.md:189`), once a target's rescan
  proves it `removed` with reason null, its branch one the plan retires, the
  stage runs before the next target is revalidated:
  1. it re-reads the manifest and, in one ref listing narrowed as change 1's
     revalidation listing is, the branch and the merge-target candidates;
  2. it checks, stopping at the first failure, that the branch exists, that
     its head equals the reconciliation record's `branch_sha`, that its
     `upstream`, `upstream_oid`, `ahead` and `behind` and the manifest's
     `tracking_branch` equal the plan's, that the merge target re-resolves to
     the plan's name, source and SHA, so that the plan's proof that the head
     is merged holds at the target's current tip, and that no registered
     worktree, the main worktree included, had the branch checked out in the
     rescan's registry listing;
  3. as the re-read's last step, it proves the branch's reflog again: the
     plan's proof over the reflog as it then reads, one `rev-list --stdin`
     child, so that a branch moved to a commit the merge target lacks and back
     since the plan, which passes every check above, is retained with
     `reflog-unmerged` and stops the run, its worktree's removal standing, as
     is one whose reflog the re-proof finds missing, empty, at its bound or
     undecidable (ruling A-24); a re-proof whose read or child fails or times
     out at its own budget decides nothing and is retained with
     `state-changed` (rulings A-43 and A-44);
  4. it spawns Git's non-force `git -c protocol.allow=never` with the six
     per-protocol pins, `-C <command directory> branch -d -- <branch>`, with
     change 1's seventeen-name environment scrub, in its own process group;
  5. it re-reads the branch in one more narrowed listing, and that post-check,
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
  codes and the note codes gain no value. An exception in a branch stage
  leaves the target as its rescan decided it, never `unknown`, and records
  the branch by what the stage established, a deletion the post-check saw
  as `retired` (ruling A-31).
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
  re-read, its re-proof included, and the branch child start only while more
  than change 1's 5 s removal floor of the work deadline remains, the re-read
  and its re-proof under `min(5 s, work remaining less the removal floor)` and
  the branch child under `min(5 s, work remaining)`, the post-check under
  `min(5 s, reserve remaining)`; a branch child in flight is waited for within
  its budget when a signal arrives and stopped like a probe past it, never
  abandoned at its budget, since it is a mutation (A-20). As change 1's D15
  has it for the apply phase, a signal stops no child of the stage, the
  re-read and its re-proof included, the post-check excepted, which a second
  SIGINT abandons as change 1 abandons its remaining rescans: a signal only
  keeps the stage from starting its next re-read, re-proof or branch child,
  never the post-check (rulings A-34, A-35). The branch child
  counts under `operations`, the reflog children, the two listings and the
  re-proof under `probes`: up to 81 more children per run.
  A run with no removal in flight still ends within 64 s of its start. The
  explicit `delete-branch` action's child stays unbounded, as change 1 says of
  it.
- **What the person sees** (A-6, A-7, A-19, P-2). The plan reads `remove PATH
  and retire BRANCH` or `remove PATH; keep BRANCH (REASON)`; the question
  counts the branches to retire and to keep, `Remove N worktrees and retire
  their M local branches? [yes/N]` when none is kept; every apply result
  prints `Removed N; branches retired: R; retained: K`, with the branches
  already gone and those whose deletion is unconfirmed counted when there are
  any, then one line per
  branch: `Retired BRANCH (was SHA)` with its restore command, `git -C ROOT
  branch BRANCH SHA`, or `git -C ROOT update-ref refs/heads/BRANCH SHA ''` for
  a name `git branch` refuses to create, one that begins with `-` or equals
  `HEAD`, and a note for each local branch that tracks it as its upstream,
  `Kept BRANCH (REASON)` with a next step that never prints a retry
  the plan knows will fail, the retry of a name that begins with `-` excepted
  while change 1's action passes no `--`, and never suggests `-D` (and, for a
  holder that is the main worktree, which Git refuses to remove, says to switch
  it off the branch, as ruling A-45 has it), `BRANCH
  was already gone`, or `Unconfirmed BRANCH (was SHA)` with the check and the
  restore command, never `Kept`, when the post-check could not establish the
  deletion (rulings A-31, A-32); a stopped run prints change 1's stop block
  and its retained branches, a retired branch never among them, before those
  lines, and the residual-window line ends the result (ruling A-34); a
  branch or merge-target name inside a printed command is
  quoted for a POSIX shell by change 1's path rule (`CAS/pc:1061-1066`), whose
  `$'...'` form needs a shell that implements it, a documentation note
  (`design.md` D8); every
  `project clean --all-safe` command printed for the person to run next, the
  deferral line and the stop block's `Next:`, carries the flag, and the
  `delete-branch` retry does not; a stop ends with change 1's stop block, the
  branch's reason in it; and the residual-window line names a branch changed
  after its last check, before its last clause, so that a run that also
  selects a cache target prints the cache change's line with that clause
  added. The overview never suggests the flag:
  its suggestion is exactly one of two argument vectors and never carries
  `--apply` (`APO/ov:484-487`).
- **The narrow guarantee under the flag** (MODIFIED review-safety). Change 1's
  "Cleanup SHALL never delete a branch" stays true without the flag. With it,
  the guarantee extends to the branch child, the branch race keeps change 1's
  outcomes, a change seen by the re-read, or a reflog its re-proof does not
  prove, retains the branch, and a change after the re-proof is the residual,
  guarded only by Git's own non-force check. Git
  2.43's `branch -d` deletes without comparing the ref to the value its own
  check read (verified for this proposal: its `reference-transaction` hook
  receives an all-zeros old value), so that window ends inside Git (Decisions;
  Open Questions).
- **The evidence model names the branch child** (MODIFIED project-command).
  Change 1's Termination paragraph names only probe children, killed on
  every exit path, and removal children, waited for; one sentence names the
  branch child beside them, waited for within its budget, and one clause of
  Budgets gives the re-read its narrower budget. The block is written on PR
  #19's text, and lane openRepoProject-2 agreed it on 2026-10-19 (ruling A-20;
  Dependencies and Sequencing).

## Rules This Change Keeps

- **Never force.** No `branch -D`, `--force`, `-f` or force push
  (`BA:1344-1345`), no forced removal and no automatic retry
  (`BA:1295-1296`), no fetch, since
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
  commit the merge target lacks, at the plan or at the stage's re-proof, is
  kept, so that no commit the head or the reflog names is lost by the
  deletion.
- **Revalidate before every destructive action, and fail closed**
  (`project-clean-review-safety/spec.md:51-53`): the re-read is that
  re-inspection, comparing every value of the branch's evidence that change
  1's removal revalidation compares and proving the reflog again, and a
  mismatch, a value it cannot read, or a reflog it cannot prove retains the
  branch.
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
    No class is added and the fifteen names (`CAS/pc:107-112`) stay (L-4).
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
    Three sentences and one clause only: PR #19's counting sentence puts the
    branch child under `operations` beside a removal; the unbounded-children
    sentence (`:788-789`) is scoped to push children and the explicit
    `delete-branch` action's children, the flag's branch child being bounded
    (A-5); one sentence after the removal floor starts a branch stage's re-read,
    its re-proof included, and branch child only while more than the floor
    remains, the re-read and its re-proof under `min(5 s, work remaining less
    the removal floor)` (A-5 as amended; ruling A-24), as the cache change
    words its cache stage; and one clause of the incompleteness
    sentence: a reflog child that fails or times out at its own 5 s budget keeps
    branches and leaves the plan complete, only the deadline making it
    incomplete (lane openRepoProject-3's re-read of `ca96701`, MEDIUM-1). Its
    five scenarios stay as PR #19 words them.
  - MODIFIED (`CAS/pc:886`):
    `### Requirement: Clean records a reconcilable result for every removal target`.
    Three rows of the exit table (`:949-956`): row 2 gains a branch stage the
    post-check could not establish and names a branch stage's
    `deadline-exceeded` among the deadline's stops (ruling A-32), row 4 a
    removed target whose
    `branch_retirement` is not plain, and row 5 a plain one, a keep the plan
    names included, for every target under the flag; one sentence after
    the exception sentence (`:938-941`): under the flag, an exception raised in
    a branch stage leaves the target as its rescan decided it (ruling A-31);
    and one clause of the stop sentence (`:962-964`), added after its command
    with none of change 1's words changed: under the flag the human result
    ends instead with the lines that the ADDED requirement orders after the
    stop block (ruling A-35, lane openRepoProject-3's confirm read, F1).
    Its eight scenarios stay verbatim.
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
    the branch stage, its re-read, checks, re-proof, branch child and
    post-check; never force, never remote, never a retry; the
    `branch_retirement` sub-record and its reasons; the stop rule; the bound
    and the counts; the question, summary line, branch lines, the quoting of
    names in printed commands, next commands and stop block. Twenty-five
    scenarios.
- `project-clean-review-safety` (all four canonical requirements and change
  1's one ADDED one accounted for):
  - Untouched (`:9`): `### Requirement: Cleanup protects the process worktree`.
  - Untouched (`:21`; MODIFIED by change 1 at `CAS/rs:3`):
    `### Requirement: Cleanup preserves all local work not proven disposable`.
    The plan's reflog proof, and the stage's re-proof of it, keep a branch
    whose reflog names unmerged work, so that the flag never removes local
    work not proven disposable.
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
    the ADDED requirement's. Under the flag, the repository-wide values a
    revalidation takes from the previous target's rescan were read before that
    target's branch stage; the MODIFIED narrow guarantee states it (lane
    openRepoProject-3's re-read, LOW-12).
  - MODIFIED (`CAS/rs:194`):
    `### Requirement: Cleanup states a narrow guarantee and its residual window`.
    "Cleanup SHALL never delete a branch, so that a branch race cannot lose
    commits" (`:210-211`) holds without the flag; under it, a second guarantee
    covers the branch child, naming the plan's reflog proof, the values the
    re-read compares and the re-read's re-proof of the reflog (ruling A-24),
    the race outcomes are stated, a reflog the re-proof does not prove among
    them, the repository-wide values a revalidation reuses from the previous
    rescan are said to precede that target's branch stage, and the residual
    window names a branch changed after its last check, the re-proof, before
    the line's last clause. Its three scenarios stay verbatim and one is added.
- `project-command` (change 1's three requirements, two MODIFIED and one
  ADDED, accounted for; every other canonical requirement untouched):
  - Untouched (`CAS/cmd:3` and `CAS/cmd:64`): `### Requirement: Inspect and
    diagnose` and `### Requirement: Explicit maintenance`.
  - MODIFIED (`CAS/cmd:90`, on PR #19's text; agreed by lane
    openRepoProject-2 on 2026-10-19, ruling A-20):
    `### Requirement: Repository inspection requires Git 2.36 and shares one evidence model`.
    One sentence in Termination, in the form of PR #19's own push-child
    carve-out: the branch child of `clean --retire-branches` is waited for on
    every exit path, as a removal child is, and signalled only past the budget
    the ADDED requirement gives it, and it is none of the delete-branch
    children that Budgets leaves unbounded; and one clause in Budgets: the
    re-read of a branch stage gets `min(5 s, work remaining less the removal
    floor)`. Ruling A-20 named the Termination clause only, and lane
    openRepoProject-2's LQ-6 lists only that clause for this change; the Budgets
    clause is part of the same block, which lane 2 agreed with it, and is
    recorded here as part of A-20 (lane openRepoProject-3's re-read, LOW-2).
    The re-read's re-proof of ruling A-24 is the re-read's last step, so that
    clause already gives it its budget, and the block is unchanged by it.
    Its nine scenarios stay as PR #19 words them.
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
  separate, explicit request; and it records `design.md` D8's note that a
  command printed in the `$'...'` form needs a shell that implements the form
  (bash, zsh, ksh93 or a POSIX.1-2024 shell), in a UTF-8 locale for its
  code-point escapes, which dash, Ubuntu's `/bin/sh`, lacks, a limitation
  change 1's path rule shares (ruling A-28 as amended); the note, the README
  text and the quoting scenario's literal follow change 1's command form as
  ratified, whether that form changes being lane openRepoProject-2's LQ-8,
  with Brett Heap, on which this change takes no side (ruling A-29).
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
  work", and the project-command block "Repository inspection requires
  Git 2.36 and shares one evidence model" (ruling A-20); this change's other
  blocks are byte-identical on `main` and PR #19 at `c462d87`. PR #19 has
  since moved: at `1ebdd90`, at `6f2cb54`, at `a664799`, at `9267303` and at
  `f0bf538` it changes all seven requirements this change modifies, and the
  inputs of `design.md` D7's fit, which D7 states at `c462d87`, at
  `6f2cb54`, at `a664799`, at `9267303` and at `f0bf538`; this does not block
  this change, whose blocks meet PR #19's final text at the re-base
  (`tasks.md` 2.1 to 2.3 and 3.2; reader RF's M2; rulings A-37 to A-42).
  Ratifying this change ratifies
  those two blocks only as written on PR #19's text at `c462d87`, not PR #19's
  own sentences, which stay PR #19's to ratify (lane openRepoProject-3's M1);
  before the Speckit handoff, `tasks.md` 2.2 re-reads both against PR #19's
  merged text, or against change 1's archived text if PR #19 closes unmerged,
  and a re-base that changes either block's text returns that block to Brett
  Heap. This change therefore archives after PR #19's amendment of change 1
  lands (L-16), or, if PR #19 closes unmerged, once both blocks are re-based on
  change 1's archived text (lane openRepoProject-3's re-read, LOW-8).
- **The project-command block** (ruling A-20). Change 1's Termination
  paragraph names probe children, killed on every exit path, and removal
  children, waited for; the branch child, waited for on a signal and stopped
  only past its budget, is neither, so lane openRepoProject-3's M2 asked for a
  sentence naming it. Lane openRepoProject-2 will not widen PR #19 before Brett
  Heap rules on it, so this change carries the block itself:
  - it is written on PR #19's text (ruling L-16), so this change archives after
    PR #19's amendment of change 1 lands, or after the re-base above if PR #19
    closes unmerged;
  - `add-project-overview-remote-merge-status` (issue #25, PR #29) MODIFIES the
    same requirement: its block is committed at `f66ed58`, on PR #19's text,
    and unchanged at that change's head `c928cb2`, lane openRepoProject-2
    having agreed it with one fix ("as a probe child past its budget is
    above"); by L-17 whichever of the two archives second re-bases its block on
    the first's archived block, changing none of the first's ratified words,
    quotation marks included, so that if this change is second the composed
    block keeps that change's backquoted requirement name beside this
    change's double-quoted ones, quoting one way binding this change's own
    text only (`design.md` Migration Plan; ruling A-35, lane
    openRepoProject-3's confirm read, F9, refining lane openRepoProject-5's
    reader RD, its L4, under A-33);
  - lane openRepoProject-2 checked the block's diff against PR #19's block and
    agreed it on 2026-10-19 (recorded at `lanes/log/openRepoProject-5.md:34`,
    and as committed and owed nothing more in lane openRepoProject-2's handoff,
    `session-handoff-2026-10-06-lane-openRepoProject-2.md:49`), in its words
    "Yes, with one fix": a verbatim
    slice of `c462d87` with all nine scenarios carried, ASCII, one hunk; the
    fix makes the Budgets clause name "Clean retires a removed worktree's
    branch only on fresh head and ancestry evidence" where it read "that
    requirement", which would have read as the nearer "Clean bounds its Git
    work and reports omitted work". The block is committed with that fix;
  - if PR #19's text moves before it merges, this block re-bases on the text
    that lands (`tasks.md` 2.2);
  - if Brett Heap has PR #19 absorb the clauses (lane openRepoProject-2's
    LQ-6), this block is dropped and this change cites PR #19 instead only if
    PR #19 also absorbs a Budgets exception that covers the re-read's shorter
    budget in the sentence that gives each Git child `min(5 s, work
    remaining)`, since the re-read and its re-proof are Git children (lane
    openRepoProject-3's delta read, D1); otherwise the block stays, on PR
    #19's absorbed text, carrying the Budgets clause alone (lane
    openRepoProject-3's re-read, LOW-2).
- **Archive order** (L-5, L-11, A-13). Change 1, then
  `add-project-clean-cache-disposal` (issue #24, draft PR #27, lane
  openRepoProject-5), then this change. PR #27 is an unratified draft (its
  Status at `e1049b2`: "alignment review and council resolved on PR #27;
  ratification by Brett Heap pending; ... nothing here is ratified"; lane
  openRepoProject-3's M4). Under the lane's
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
    the block. The flagless invariant is stated against the base text, today
    change 1's digest input, and `retire` is a member named in the ADDED
    requirement, its position left to the construction of the canonical text,
    which change 1 and PR #19 do not fix ("a canonical JSON text of the
    repository's four identity fields, the merge target's name and SHA, and
    the selected `[path, branch, head]` triples in canonical order",
    `CAS/pc:629-632`), and its pairs ordered as `selected` is (ruling A-30).
    Once re-based on the cache change's archived block, the invariant becomes
    byte-identical to the cache change's digest input, and this change's
    digest sentence, placed after the cache change's, reads as `design.md`
    D10 writes it, binding to "the canonical text" and carrying "nothing more
    than the members this paragraph names" (lane openRepoProject-5's reader
    RD, its M3(a); ruling A-33). The AND that tests the joint digest for a
    flagged plan with a cache target, pinning no order of its members, tests
    the cache change's own requirement, so it is added to "A flagged
    preview's digest binds the flagged apply" at the re-base (`tasks.md` 2.3
    and 3.2), not before (lane openRepoProject-3's re-read, MEDIUM-2).
  - "Clean bounds its Git work and reports omitted work": both rewrite the
    counting sentence, merged as "a removal, or a branch child of
    `--retire-branches`, under `operations`, every other child, a cache
    enumeration included, under `probes`, and each cache entry that a cache
    stage removes counted once under `operations`"; both add a stage sentence
    after the removal floor, the cache stage's and the branch stage's, which
    sit side by side; this change's clause in the incompleteness sentence,
    which the cache change does not edit, stays; and where the cache change's
    fit sentence counts, as it reads at `e1049b2`, "at most 250 Git children
    besides the 16 removals, about 42.3 s", which the flag's up to 81 more
    children make false, the re-based block scopes that sentence, and any
    restatement of it under the lane's ruling B-25, to runs without
    `--retire-branches` (`design.md` D7).
  - "Clean records a reconcilable result for every removal target": the cache
    change makes its descriptor-relative deletion of listed cache paths the one
    exception to "`project` SHALL never force a removal or delete a directory
    itself" (B-10), and edits five other passages; this change's edits are
    exit rows 2, 4 and 5, the sentence after the exception sentence, and one
    clause of the stop sentence (reader RF's L3; ruling A-37). Row 2
    is edited by both, its one shared passage, and merges as `design.md`'s
    Migration Plan writes it, the cache change's "a cache stage's removal
    reached the removal ceiling" beside this change's two clauses (lane
    openRepoProject-5's reader RD, its L1).
  - "Cleanup states a narrow guarantee and its residual window": the cache
    change names the revalidation its guarantee means for a cache target
    (B-10); this change extends the guarantee to the branch child, its two
    sentences placed directly after the guarantee sentence and before the
    cache change's "A cache stage SHALL carry the one guarantee ...", the
    first reading "that guarantee" for "the guarantee", so that it binds to
    the removal's guarantee (RD's M3(b); ruling A-33), and the
    residual-window line of a flagged run whose plan also selects a cache
    target is the cache change's line with this change's branch clause before
    its last clause (ruling A-23): `Not protected: ignored files created or
    index flags set after the last check or during a cache stage, caches
    recreated after it, a branch changed after its last check, and any change
    after Git's own check.` (`design.md` D8). The scenario "A branch changed
    after the re-read meets Git's own check" then names a run whose plan
    selects no cache target (RD's L3).
  - The human result: the cache change's `Caches disposed` line, which it
    prints after change 1's success line, follows this change's summary line
    and precedes its branch lines (RD's L2; `design.md` D8). The re-base
    rewords this change's ADDED sentence that orders the flagged result
    (`specs/project-clean/spec.md:1121-1126`) to place it, in the words that
    `design.md`'s Migration Plan gives (reader RF's L1; ruling A-37).

  Each re-base is checked by `diff -u` of the archived block against the
  re-based block showing additions only, apart from the rewordings that
  `design.md`'s Migration Plan writes out, and by a second `diff -u`, of this
  change's block as committed at its ratified head against the re-based
  block, which may show only the archived block's text carried in and those
  rewordings (reader RF's M1; ruling A-37); a re-base that changes this
  change's words beyond them returns that block to Brett Heap; `validate`
  alone is no proof, since a re-base that keeps every scenario but drops
  sentences validates and archives (RD's M1 and M3; ruling A-33).

  If PR #27 is not ratified, this change's five shared blocks re-base on change
  1's archived text instead, the AND of `tasks.md` 2.3 is not added, and A-9's
  joint fit with cache disposal is moot (lane openRepoProject-3's re-read,
  MEDIUM-2).
  "Clean reports local worktree state" is shared with no other open change;
  it is written on change 1's unarchived text, so before the handoff it is
  re-read against change 1's archived text and re-copied with this change's
  one clause, checked by `diff -u` showing additions only (`tasks.md` 2.1;
  RD's M4; ruling A-33).
  `add-project-overview-remote-merge-status` archives after change 2 and, apart
  from the project-command block above, touches no capability here.
- **Change 1's open question 2** (lane openRepoProject-3's M3; its fix,
  qualifying only `merged_into_target` rows, is declined, and lane 3 agrees
  the reason holds). Branch retirement follows change 1's eligibility, whose
  only removal proof today is local ancestry (`BA:195-199`). If Brett Heap
  rules that question 2 admits removal evidence other than local ancestry (CAS
  `proposal.md:1001-1005`), a row removed on that evidence lacks the ancestry
  the stage relies on. The plan already keeps such a branch: A-16's proof
  names every reflog entry's new object, and the `unstarted-branch` gate makes
  the last entry's new object the branch's head (a branch whose last entry
  differs from its head is `reflog-unavailable`, in the batch block), so a head
  that is not an ancestor of the merge target fails the proof, and the branch
  is kept with `reflog-unmerged`, a keep that never stops the run and is never
  retired. Before this change archives, the follow-on change need only confirm
  `reflog-unmerged` as that branch's reason, or give it a reason of its own in
  the sub-record's enum. No behaviour changes now.
- **Change 1's `delete-branch` and a name that begins with `-`** (lane
  openRepoProject-3's delta read, D5). Change 1's explicit action runs `git -C
  ROOT branch -d <branch>` with no `--` (`project:734`), so the retry this
  change prints for such a name, `--branch=BRANCH`, reaches Git as an option:
  for `-f`, `branch -d -f` fails, "branch name required", exit 128, and the
  ref stays (`design.md` Context). The retry deletes the branch once change
  1's action passes the name after `--`, which change 1, lane
  openRepoProject-2's, settles; this change prints the retry that action is
  given and changes nothing in it. A branch named `HEAD` needs no such change:
  `branch -d HEAD` deletes it.
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
- **The primitive: a re-read and its re-proof, then non-force `branch -d`**
  (A-2, A-24; `BA:1340-1341` names the check, not the command). The re-proof
  runs the plan's reflog proof again before the branch child, since a branch
  moved to an unmerged commit and back after the plan passes every other
  check while its reflog names that commit. The rejected alternative,
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
  `BA:729-735`, leaves the caps to measurement, `BA:766-771`). At the
  packet's 150 ms per child, a flagged run of 16 without the cache change
  removes 14 worktrees and retires 13 branches on change 1's terms at PR
  #19's `c462d87`. At PR #19's `6f2cb54`, `a664799`, `9267303` and
  `f0bf538`, at the packet's 150 ms per child (D14's 150 ms basis), it
  removes 11 and retires 10 where the plan read `extensions.worktreeConfig`
  as false, six children per revalidation, all 16 removals spawning without
  the flag; in that case, on D14's measured basis at `f0bf538`, where change
  1's 16th removal spawns at 35.1 s, or 42.8 s with 20,000-file removals, a
  flagged run of 16 removes 16 and retires 15 with this change's children at
  150 ms, the 16th branch child due at 45.32 s, its re-read refused first at
  45.02 s, and `retained` with `deadline-exceeded`, exit 1, never unsafe, and
  16 and 16 with them at task
  2.1's average of about 0.063 s per child (`design.md` D7). Where the plan
  read `extensions.worktreeConfig` as true, seven, PR #19's D14 counts a
  plan-time probe on each linked row, and at `f0bf538` it states that case on
  three bases, choosing none. At 128 rows, on its 150 ms basis, change 1
  alone removes nothing and a flagged run removes and retires nothing, its
  first removal due at
  45.45 s, past the 45 s spawn limit, or 45.3 s without the flag; on its
  measured basis, with the stand-ins it names for the two probes task 2.1 did
  not measure, change 1 alone removes all 16, or 15 with 20,000-file
  removals, and a flagged run removes and retires 14 and 14 with this
  change's children at 150 ms each, or 11 and 11 with 20,000-file removals,
  and 16 and 16 with them at task 2.1's average of about 0.063 s per child,
  or 13 and 13; on its mixed basis change 1 alone removes 11 and a flagged
  run removes and retires 7 and 7. Which basis the cap test uses is the first
  step of PR #19's LQ-20, to measure LQ-11's and LQ-13's two probes or to
  decide the basis; its options, (a) to (c) and (d), the rule's own step of
  lowering the caps, apply only if the case still fails, and none is chosen.
  A-9 for that case waits on Brett Heap's LQ-20 for PR #19, whose framing
  lane openRepoProject-2 may revise; `design.md` D7's table gives a flagged
  run's result under each option on each basis, beside D14's table for
  change 1 (`design.md` D7; reader RF's M2; rulings A-37 to A-42). The
  figures below are at `c462d87`, which this
  change's PR #19 blocks are ratified on (`tasks.md` 1.6); PR #19's later
  heads do not block this change, and every figure meets PR #19's final text
  at the re-base. With the cache
  change archived first, its filesystem time added as the lane's ruling B-25
  restates it (ruling A-23), the reflog proof's one child and the stage's
  re-proof, one more child per retired branch (ruling A-24), a flagged run at
  the packet's 150 ms per child brings 9 of its 16 targets through their stage
  before the spawn limit through one worker per stage, 8 in the worst case of
  17 reflog children, and at least 5, or 3, at a thread per call, 6, or 5, in
  the worst order a run can take; change 1's own deadline rule makes the rest
  `not-attempted` with `deadline-exceeded`, exit 1, taken by the next run and
  never unsafe (`BA:772-774`); on change 1's measured costs at `c462d87`, task
  2.1's 23.6 s, which predates LQ-11's and LQ-13's children, all 16 fit
  through a worker, while at a thread per call at least the 16th target is
  deferred, with one reflog child as in the worst case, and on D14's measured
  basis at `f0bf538`, with the cache change's 16 enumerations at 2.4 s, 12 of
  the 16 come through their stage through a worker and at least 8 at a thread
  per call, and at the cache change's own 3.7 s for them 11 and at least 7
  (ruling A-44). These are the cache change's
  ordinary trees; its worst shapes lie outside this fit, under its own cap
  questions to Brett Heap (`design.md` D7; ruling A-25).
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
  prints a retry the plan knows will fail, the retry of a name that begins
  with `-` excepted while change 1's action passes no `--`, and never
  suggests `-D`; every
  `project clean --all-safe` command printed for the person to run next, the
  deferral line and the stop block's `Next:`, carries the flag, so that
  following the tool's own advice never strands a branch whose worktree a
  flagless run removed, and the `delete-branch` retry does not, since that
  action refuses the flag (ruling A-22(a)). The restore line names the
  repository with `git -C ROOT`, a name that `git branch` refuses to create,
  one that begins with `-` or equals `HEAD`, is restored by `update-ref`
  (ruling A-27, Codex's P2 on `9ff8202`), and every name in a printed command
  is quoted for a POSIX shell (ruling A-22(b) and (c)), its `$'...'` form
  needing a shell that implements it, which `design.md` D8 and the README
  record and no printed line says (ruling A-28 as amended, Codex's P2 on
  `9ff8202`); the rejected alternative, names printed verbatim in commands,
  lets a valid branch named `topic;id` run `id` when the line is pasted
  (`design.md` Context). A retired branch that another local branch tracks
  as its upstream gets a note naming that branch, no commit being lost and a
  later row's refusal standing, and a branch that Git refuses because a
  rebase or bisect in another worktree holds it, which the registry listing
  shows detached, is a residual whose line says to wait for that to end and
  remove that worktree, or, for the main worktree, which Git refuses to remove,
  to switch it off the branch, before the retry (rulings A-32 and A-45, RA's
  LOW-4 and LOW-5; the rejected alternatives, a plan keep for each, are in
  `design.md` D4 and D8). A `branch-in-use` line whose holder PATH2 is the main
  worktree reads `next: BRANCH is checked out at PATH2, the main worktree;
  switch it off BRANCH, by checking out another branch there, such as
  MERGE_TARGET, or by detaching it, then: RETRY`, where `git worktree remove`
  of a main worktree exits 128, "is a main working tree", on Git 2.43.0 and on
  2.36.6; `branch-shared`'s holder is a selected row, which change 1's
  `main-worktree` gate never selects, so its line keeps the linked form
  (ruling A-45, Codex's P2 on `1bf217c`).

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
  names: the plan proves them merged, the stage's re-proof proves the reflog's
  again over the reflog as it then reads (ruling A-24), and otherwise the
  branch is kept. The branch's
  `branch.<b>` section goes with it (`design.md` Risks). The repository
  identity is the one the rescan re-established, which a target `removed` with
  reason null requires (`CAS/pc:919-921`).
- **A-16's reflog proof, as amended on 2026-10-19** (recorded at
  `lanes/log/openRepoProject-5.md:33`). A commit is named when it
  is the new object or the non-zero old object of a reflog entry, the oldest
  surviving entry's old object included, so that a commit that `git reflog
  expire` has left named only as an old object is proven merged too; the first
  text named new objects only, and the writer's report raised the gap. The proof
  is the ruling's form, with no extra child, one child per repository and one
  per row only when it prints a commit. A failure or timeout of the repository's
  child fails every row's proof, so every selected branch is kept, and the plan
  stays complete: change 1 makes a plan incomplete when a repository-wide probe
  fails, and the bounds block names this exception, since the proof decides
  which branches retire, never whether the plan is whole; the deadline passing
  during the proof still makes the plan incomplete (lane openRepoProject-3's
  re-read, MEDIUM-1). Its child reads the merge target's exclusion as the one
  line `^<merge target SHA>`, a revision, because lane 3 reads `--not` on
  standard input as Git 2.42 or later, above the 2.36 floor (its MEDIUM-3;
  `design.md` Context, D9). The stage proves the reflog again (ruling A-24,
  Codex's P1 on `abad010`): its re-proof, the re-read's last step, gives the
  same child the commits the
  reflog names when the stage runs, because a branch moved to a commit the
  merge target lacks and back between the plan and the stage passes every
  other check while its reflog names that commit, which `branch -d` would
  leave unreachable. Such a branch is retained with `reflog-unmerged`, a
  retention the stage discovers, so the run stops with exit 2 while the
  worktree's removal stands, as is one whose reflog the re-proof finds missing,
  empty, at its 64 KiB bound or undecidable, each a value the re-proof
  decided; a re-proof whose read or child fails or runs past its own budget
  decides nothing and retains it with `state-changed`, as PR #19's rule for
  revalidation gives a call that decides nothing, again exit 2 (rulings A-43
  and A-44; lane openRepoProject-2's answer on R-208), and one that the
  deadline stops with `deadline-exceeded`. The plan's own failed proof, its
  `rev-list` child's alone since the plan does not repeat the gate's reflog
  read, stays a `reflog-unmerged` keep (ruling A-46, W47's LOW-2).
- **The plan's keep order.** `reflog-unmerged`, then `branch-in-use`, then
  `head-not-merge-target`, then `branch-shared`, so that the next step printed
  for a kept branch never leads to deleting work only its reflog holds: the
  `head-not-merge-target` advice ends in a `delete-branch` retry, which Git's
  merge test would let through for a branch whose head is merged.
- **Children per target, and the fit** (A-5, as amended twice; A-24). The stage
  spawns the re-read that A-2 requires, with its re-proof of the reflog (ruling
  A-24), the branch child, and a post-check that change 1's evidence rule
  requires ("The child's exit status alone SHALL never prove a removal",
  `CAS/pc:919`; null for what is not established, `CAS/pc:1128-1129`), and the
  plan spawns the reflog proof (A-16): up to 81 more children per run, 16 under
  `operations` and 65 under `probes`. A-5's first text said "up to 16 more
  children"; the lane amended it to 48 on 2026-10-18, its verdict of 2026-10-19
  adds the reflog children, and its ruling A-24 of 2026-10-20 adds the
  re-proof, one more child per retired branch; the departure from the first
  text stands as recorded. The branch child spawns only while more than the 5 s
  removal floor remains. At the packet's assumed 150 ms per child its fit rule
  (`BA:729-735`) fails for a flagged run of 16 targets: the 14th removal spawns
  at 45.0 s, on the spawn limit's boundary, but its branch child, due at 46.05
  s, cannot start, so 14 worktrees are removed and 13 branches retired, the
  15th and 16th targets deferred, on change 1's terms at PR #19's `c462d87`; at
  its `6f2cb54`, `a664799`, `9267303` and `f0bf538`, at the same 150 ms per
  child (D14's 150 ms basis), 11 and 10 where the plan read
  `extensions.worktreeConfig` as false; where it read it as true, PR #19's
  D14 counting a plan-time probe on each linked row, at `f0bf538` a flagged
  run of 16 at 128 rows removes and retires 0 and 0 on that basis, 14 and 14
  on D14's measured basis with this change's children at 150 ms, or 16 and 16
  with them at task 2.1's average of about 0.063 s per child (23.6 s less its
  15 removals at 0.604 s, over its 231 children), and 7 and 7 on its mixed
  basis, where change 1 alone removes 0, 16 and 11, and `design.md` D7's table
  gives its result under each option of LQ-20 on each basis (`design.md` D7;
  reader RF's M2; rulings A-37 to A-42). Where the plan read
  `extensions.worktreeConfig` as false, change 1's measured fit is PR #19's
  D14 at `f0bf538` (its `design.md:968`: the 16th removal at 35.1 s, 42.8 s
  with 20,000-file removals; task 2.1's 23.6 s predates LQ-11's and LQ-13's
  children, its `:1002-1003`), on which a flagged run of 16 removes 16 and
  retires 15 with this change's children at 150 ms (the 16th branch child due
  at 45.32 s, its re-read refused first at 45.02 s, `retained` with
  `deadline-exceeded`, exit 1, never unsafe), 15
  and 14 with 17 reflog children, 13 and 12 with 20,000-file removals, and 16
  and 16 at task 2.1's average, or 15 and 14 with 20,000-file removals; the
  caps stay, as change 1 kept them on its measurement. Task 2.1's own
  account, `c462d87`'s, is kept as that sha's: CAS `tasks.md` 2.1's 16th
  removal at 23.6 s, about 32.75 s with the 60 stage children before it and
  one reflog child at 150 ms each, about 35.15 s with 17 (`design.md` D7;
  lane openRepoProject-3's W40, MEDIUM-1; ruling A-42). Where the plan read it
  as true, which basis PR #19's cap test uses is the first step of its LQ-20, to
  measure the two probes or to decide the basis, its options applying only if
  the case still fails, so that A-9 there waits on Brett Heap's LQ-20 for PR
  #19, whose framing lane openRepoProject-2 may revise. A slower repository
  leaves its last targets `not-attempted` with `deadline-exceeded`, or a
  branch `retained` with it, exit 1, never unsafe (`BA:772-774`). This
  departs from the packet's rule for flagged runs; the joint fit with the
  cache change is A-9's decision above.
- **Where the stage's probes are counted** (lane openRepoProject-3's L5). The
  packet defines a target's `probes_performed` as "the Git children of that
  target's revalidation ... at most 5" (`BA:1039-1042`, `BA:1422`), so the
  target's count stays that, and the stage's re-read, its re-proof included,
  and post-check are counted in the sub-record's own `probes_performed`. The
  next target's revalidation
  keeps change 1's sourcing, the rescan's repository children (feature 004's
  T085), and a merge target moved during a branch stage is caught by the next
  target's own re-read (`clarifications.md`, S-4).
- **A-4's three stage values, and null.** When the post-check cannot decide,
  `stage` is null with reason `reconciliation-incomplete`, by change 1's null
  rule; a fourth value `unknown` is rejected to keep A-4's list. Such a
  branch gets its own line, `Unconfirmed BRANCH (was SHA)` with the check and
  the restore command, and its own count in the summary, never `Kept`, since
  it may be gone; this applies A-19's accounting of every removed target's
  branch to the one stage it missed and does not reopen A-19 (ruling A-31,
  RA's MEDIUM-3).
- **An exception in a branch stage departs from change 1's exception rule**
  (ruling A-31, RA's MEDIUM-2). Change 1 makes a target that an exception
  interrupts after the apply phase began `unknown` with `internal-error`
  (`CAS/pc:938-941`), and `unknown` means "removal is not proven"; a target
  in its branch stage was proven `removed` by its rescan. Under the flag an
  exception in the stage leaves the target as that rescan decided it, and
  its `branch_retirement` records what the stage established, with reason
  `internal-error`, or null with `reconciliation-incomplete` once a branch
  child ran and no post-check decided, never `target-not-removed`; a
  deletion the post-check saw is `retired`, its SHA and restore line
  printed. The reconcilable block's exception sentence names this exception,
  and the run stops as for any branch stage that does not end plain. This
  departs from the packet's rule as well, `BA:479-482` ("Once the apply phase
  begins, every exception raised while handling a target is caught for that
  target and recorded as `unknown` with reason `internal-error`; later
  targets are `not-attempted`, the result record is always printed, and the
  exit status is 1 (130 after SIGINT)"): the target is not `unknown`, and the
  exit status 1 becomes 2, by exit row 4, or stays 1 for a null `stage`, by
  row 2, while later targets are still `not-attempted`, the record is still
  printed and a signal still decides first (ruling A-35, lane
  openRepoProject-3's confirm read, F2).
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
  counts add up: `Removed N; branches retired: R; retained: K`, with
  `; already gone: G` when G is above 0 and `; unconfirmed: U` when U is
  above 0, R, K, G and U counting the distinct branches of the removed
  targets; it replaces `Removed N; branches kept: ` and precedes the branch
  lines. Its place among change 1's lines extends change 1's order, which
  holds no summary or branch line after the stop block (CAS `design.md` D18:
  a stop prints `Stopped at ...`, "then the retained branches and the
  residual-window line"): in a run that stops, the stop block and the
  retained branches come first, a branch the stage retired, or whose
  deletion is unconfirmed or was already gone, never named among them; then
  the summary and branch lines; then the residual-window line (ruling A-34,
  lane openRepoProject-5's reader RE, its RE-3). `CAS/pc:962-964` states the
  stop block as ending the result and naming every retained branch, so the
  reconcilable block's sentence gains one clause, added to change 1's words:
  under the flag the result ends with the lines that the ADDED requirement
  orders after the stop block (ruling A-35, lane openRepoProject-3's confirm
  read, F1). The first text put the stop block last.
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
  budget it is stopped like a probe. This departs from `BA:466-468` ("If a
  child is in flight, `project` sends SIGTERM to the child's process group"),
  as change 1's V1 departs from it for a removal (CAS `proposal.md:866-867`).
  The stage's re-read and re-proof follow change 1's D15 as well: in the
  apply phase the handler only records and the seam reads the slot between
  steps, so a signal stops none of them and only keeps the stage from
  starting its next re-read, re-proof or branch child, never the post-check,
  and a second SIGINT abandons the post-check as it abandons change 1's
  remaining rescans (ruling A-34, RE's RE-2; ruling A-35, lane
  openRepoProject-3's confirm read, F3). The first
  text had a signal stop the re-read and the re-proof like planning probes.

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
- **The target cap of a flagged run** (A-9). Without the cache change, at the
  packet's 150 ms per child, a flagged run of 16 removes 14 worktrees and
  retires 13 branches on change 1's terms at PR #19's `c462d87`, and at its
  `6f2cb54`, `a664799`, `9267303` and `f0bf538`, at the packet's 150 ms per
  child (D14's 150 ms basis), 11 and 10 where the plan read
  `extensions.worktreeConfig` as false, six children per revalidation, and on
  D14's measured basis at `f0bf538`, where change 1's 16th removal spawns at
  35.1 s, 16 and 15 with this change's children at 150 ms, the 16th branch
  child due at 45.32 s, its re-read refused first at 45.02 s, and `retained`
  with `deadline-exceeded`, exit 1, never unsafe, and 16 and 16 with them at
  task 2.1's average of about 0.063 s per
  child (`design.md` D7); where it read it as true, seven, PR #19's D14 counts
  a plan-time probe on each linked row and at `f0bf538` states that case on
  three bases, choosing none: at 128 rows a flagged run of 16 removes and
  retires 0 and 0 on its 150 ms basis; 14 and 14 on its measured basis, with
  the stand-ins it names and this change's children at 150 ms, or 16 and 16
  with them at task 2.1's average; and 7 and 7 on its mixed basis; change 1
  alone removes 0, 16 (15 with 20,000-file removals) and 11. That case waits
  on Brett Heap's LQ-20 for PR #19, whose framing lane openRepoProject-2 may
  revise: its first step is to measure
  LQ-11's and LQ-13's two probes or to decide the basis, and its options, (a)
  to (c) and (d), the rule's own step of lowering the caps, apply only if the
  case still fails, none chosen; `design.md` D7's table gives a flagged run's
  result under each on each basis (`design.md` D7; reader RF's M2; rulings A-37
  to A-42). The figures that follow are at `c462d87`; this change ratifies its
  PR #19 blocks only as written there (`tasks.md` 1.6), PR #19's later heads do
  not block it, and every figure meets PR #19's final text at the re-base. With
  `add-project-clean-cache-disposal` archived first, its plan-time walk (about
  2 s through one worker per stage, about 5.6 s at a thread per call) and its
  cache stages (about 2 s, or about 5.3 s) added as the lane's ruling B-25
  restates them, and the stage's re-proof of the reflog, one more child per
  retired branch (ruling A-24), a run with `--retire-branches` whose plan also
  selects cache targets reaches the spawn limit early under the packet's 150 ms
  per child: through a worker, with the reflog proof's one child, 10 of its 16
  targets are removed and 9 branches retired, and in the worst case of 17
  reflog children 8 removed and 8 retired; at a thread per call at least 5 and
  5, or 4 and 3, bounds that take the cache stages whole before the first
  removal, and 6 and 6, or 5 and 5, in the worst order a run can take. Change
  1's deadline rule leaves the rest `not-attempted` with `deadline-exceeded`,
  exit 1, for the next run, never unsafe. On change 1's measured costs at
  `c462d87`, task 2.1's 23.6 s, which predates LQ-11's and LQ-13's children,
  the cache change's 16 enumerations taken at 150 ms each, the 16th removal
  spawns near 39.15 s through a worker, or 41.55 s in that worst case, and all
  16 fit; at a thread per call it is due near 46.05 s, or 48.45 s in the worst
  case, past the spawn limit either way, so at least the 16th target is
  deferred; at the cache change's measured 3.7 s for its enumerations each
  figure is 1.3 s later and no conclusion changes. On D14's measured basis at
  `f0bf538`, where the plan read `extensions.worktreeConfig` as false, the same
  additions, with the 16 enumerations at 2.4 s, bring 12 of the 16 targets
  through their stage through a worker, and at least 8 at a thread per call,
  and at the cache change's own 3.7 s for them 11 and at least 7 (`design.md`
  D7; ruling A-44). These figures are for
  the cache change's ordinary trees; its worst shapes, a walk of directories
  only and deep chains,
  lie outside them, under its own cap questions to Brett Heap (`design.md` D7;
  ruling A-25). Options: (a) keep `limits.targets` 16 for every run; (b) a
  lower cap under the flag, 8 by the packet's rule (`BA:729-735`) before the
  cache change's filesystem time, which would make the flag change the
  selection. Recommendation: (a), keep 16.
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
  person inspects `git -C ROOT reflog show refs/heads/BRANCH`; (b) yes: one
  more bounded child per
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
| SA-3: the departure from the packet's fit rule (`BA:729-735`) was not named in Decisions | DRIFT | applied, beside A-5 as amended | Decisions, readings ("Children per target, and the fit", then titled "Three children per target") |
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
The counts in QA-3's row, "53 scenarios" and "sixteen scenarios", and in A-9's
row, "13 of 16", are those of their round; the ADDED requirement now holds 25
scenarios, and the joint fit stands as rounds A4 and A5 state it.

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
| S-2: the branch child has no spawn floor | MEDIUM | VALID (A-5 as amended): the re-read and branch child start only while more than the 5 s removal floor remains, the strict test council B on PR #27 asked for, the re-read under `min(5 s, work remaining less the removal floor)`; the deadline scenario gains the AND; `retired` with `deadline-exceeded` dropped as unreachable | What Changes; Capabilities (bounds); project-clean delta; project-command block; `design.md` D3, D5, D7 |
| S-3: a branch two worktrees hold stops the batch | LOW | VALID (A-18): `branch-shared` for earlier holders, the stage at the last; `branch-in-use` at plan time for a holder outside the selection; a holder found only at the stage still stops | project-clean delta (ADDED); `design.md` D4, Risks |
| S-4: D2's reuse of the post-check listing is in no requirement and collides with T085 | LOW | NOTED: D2's substitution deleted; the next target's own re-read catches a moved merge target; T085 untouched | `clarifications.md`; `design.md` D2 |
| AE-1: retiring a branch deletes its reflog, the last reference to amended-away work | HIGH | VALID (A-16, amended 2026-10-19 to name each entry's non-zero old object as well as its new one, the oldest surviving entry's old object included, with no extra child; recorded at `lanes/log/openRepoProject-5.md:33`): the plan's reflog proof keeps such a branch (`reflog-unmerged`); the "loses no commit" and "lossless" claims now say what is proven; Risks names the `branch.<b>` keys; new Open Question on patch equivalence | What Changes; Rules; Decisions; Open Questions; both deltas; `design.md` D4, Risks |
| AE-2: the digest ignores the flag, so a flagless approval authorizes deletions | MEDIUM | VALID (A-1 as amended): the flagged preview exists, the digest carries `retire` under the flag, and a flagless digest refuses a flagged apply; the Out of Scope bullet on previews is deleted; "Clean reports local worktree state" MODIFIED for its digest sentence (L-11); a JSON preview shows each row's planned action in a `branch_plan` sub-record on its `selected` entry, the plan envelope, a listed set of fields in change 1, gaining no key | What Changes; Capabilities; Decisions; Out of Scope; project-clean delta; `design.md` D1, D10 |
| AE-3: two foreseeable retentions stop the batch every run | MEDIUM | VALID (A-17, A-18, A-4 as amended): plan-time keeps never stop the run; applied with change: no `merge-base --is-ancestor` child at plan time, the ruling taking the SHA test instead | Decisions; project-clean delta; `design.md` D4, D6 |
| AE-4: the human result keeps no record of what it deleted | LOW | VALID (A-19): as P-3 | project-clean delta (ADDED); `design.md` D8, Rollback |
| A-20 (the lead's ruling on lane 3's M2, after lane openRepoProject-2's answer) | ruling | applied: the project-command block is MODIFIED on PR #19's text, agreed by lane openRepoProject-2 on 2026-10-19 with one fix and committed, with the Dependencies points | Capabilities (project-command); Dependencies and Sequencing; `design.md` D3, Migration Plan |
| Council B's refinements for this change (the lead, 2026-10-19, from council B on PR #27; recorded in the lane's handoff, `session-handoff-2026-10-11-lane-openRepoProject-5.md:50` at the register's `c3a9b3767`: "the strict floor, the digest re-base note, and a flagged scenario with a cache target") | ruling | applied: the re-read and the branch child start only while more than the floor remains, the branch child never abandoned at its budget; the flagless invariant and `retire`'s place stated against the base text, with the re-base note; one AND for a flagged plan with a cache target, moved to the re-base in round A3 | What Changes; Capabilities (bounds); Decisions; Dependencies and Sequencing; project-clean delta; `design.md` D3, D7, D10 |
| H1: the re-read applies the revalidation MUST selectively | HIGH | applied (A-14): the re-read compares `upstream`, `upstream_oid`, `ahead`, `behind` and `tracking_branch` as well, retaining with `state-changed`; `ahead` and `behind` beyond A-14's list, from the same listing | Capabilities (review-safety `:49`); Decisions; both deltas; `design.md` D4 |
| M1: ratifying #26 would ratify PR #19's pending text | MEDIUM | applied: the two blocks on PR #19's text are ratified only as written there, and 2.2 re-reads them before the handoff | Dependencies and Sequencing; `tasks.md` 1.6, 2.2; `design.md` Migration Plan |
| M2: project-command's child rules do not account for the branch child | MEDIUM | applied with change, per A-20: change 1's Termination paragraph is exhaustive about the two kinds it names, so the requirement is MODIFIED, on PR #19's text, agreed by lane openRepoProject-2 | Capabilities (project-command); Dependencies and Sequencing |
| M3: question 2 would be decided by default | MEDIUM | applied with change, per the verdicts: a Dependency, no new behaviour now; lane 3's fix of qualifying only `merged_into_target` rows is not taken | Dependencies and Sequencing |
| M4: PR #27 relied on without being called a draft | MEDIUM | applied: PR #27 named as an unratified draft, with what changes if it is not ratified | Dependencies and Sequencing |
| M5: the printed retry is known to fail | MEDIUM | settled by A-17 and A-19 | as P-1 |
| M6: the branch child has no start floor | MEDIUM | settled by A-5 as amended | as S-2 |
| L1: `OV:142-146` is the wrong citation | LOW | applied: `OV:173-180` and `OV:357-358` | Why |
| L2: `README.md:178-200` is off by one | LOW | applied: `README.md:178-201`, twice | citation key; Impact |
| L3: `BA:1344-1345` is broader than its source | LOW | applied: `BA:1295` for no automatic retry, `BA:195-196` and `SY:221-226` for local evidence | Rules This Change Keeps |
| L4: canonical lines cited for change-1-only text | LOW | applied: `CAS/pc:107-112` (first given as `:105-111`, corrected in round A3), `CAS/pc:180` and `CAS/pc:223-228` beside the canonical lines | Capabilities |
| L5: the stage's listings counted in `probes_performed` | LOW | applied: the target's `probes_performed` stays the packet's; the stage's are in the sub-record's own `probes_performed` | Decisions; project-clean delta (ADDED); `design.md` D5, D7 |
| L6: "separate, explicit action" reinterpreted | LOW | applied: listed under Decisions as a reading put to ratification | Decisions |
| L7: question 1's ruling applied beyond its recorded scope | LOW | applied: the extension attributed to A-3, Brett Heap's ruling cited as its proof rule | What Changes; Decisions; `design.md` D4 |
| L8: `git-refused` and `git-failed` reused with other meanings | LOW | applied: the ADDED text says so; not renamed, since the verdicts name `git-refused` as the stage's outcome | project-clean delta (ADDED); Decisions; `design.md` D5 |
| L9: D2's sourcing change in no spec delta | LOW | applied, as S-4: revalidation keeps its own listing | `design.md` D2; `clarifications.md` |
| L10: the JSON requirement enumerates keys | LOW | applied: the ADDED requirement says its keys extend those lists under the flag | Capabilities; project-clean delta (ADDED); `design.md` D10 |
| L11: "Corrections to the Packet: None" | LOW | applied: lane 3's P1, with P2 and P8, which this change also bears on | Corrections to the Packet |
| L12: testability gaps | LOW | applied: scenarios or ANDs for a re-read fault, `retired` with `git-failed` and `probe-timeout`, `retained` with `spawn-error` and `removal-ceiling`, `branch-missing-after-removal`, a holder in the main worktree, the estimated and performed counts, the scrub and process group, the stage listings' directory, the stop block, the one-target question, null `command` and `exit_status`, the single-target `--json`, the exact plan lines and a slow fake `git`; `retired` with `deadline-exceeded` left out as unreachable | project-clean delta (ADDED) |

### Re-read and Codex Findings (round A3)

Lane openRepoProject-3 re-read this change at `ca96701` (its 19 earlier ids: 15
FIXED, M1, M4 and L4 PARTLY, M3 declined with its reason holding; new: no HIGH,
3 MEDIUM and 15 LOW), and Codex reviewed `785a45e`, whose cited lines are
unchanged at `ca96701` (one P1, two P2); the lead's rulings A-21 to A-23 bind,
with B2's third escalation and the lead's note from council C's product-advocate
on PR #29 at `c928cb2`. Of the 28 rows below, 27 are applied and 1 is applied
with change (lane 3's re-read LOW-2, whose cosmetic part is declined), and none
is declined.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| lane 3 re-read (ca96701) M3: the declined fix's reason, which holds, is not the one the text gives | MEDIUM | A-21: applied: the Dependency now says the declined fix's reason: A-16's proof names the head, which the `unstarted-branch` gate makes the last reflog entry's new object, so a row removed on any evidence but ancestry is kept as `reflog-unmerged` and never stops the run | Dependencies and Sequencing (question 2) |
| lane 3 re-read (ca96701) MEDIUM-1: a reflog-proof failure keeps every branch, but whether the plan stays complete is unstated against change 1's planning rule | MEDIUM | A-21: applied: a failure, or a timeout at a reflog child's own 5 s budget, keeps branches and leaves the plan complete, only the deadline making it incomplete, in the bounds block's incompleteness sentence and the ADDED requirement; ANDs for a nonzero and a hung reflog child | Capabilities (bounds); What Changes; Decisions, readings (A-16); project-clean delta (bounds; ADDED; "A branch whose reflog holds amended-away work keeps it"); `design.md` D4, D7 |
| lane 3 re-read (ca96701) MEDIUM-2: an AND tests the cache change's unratified requirement, and tasks 3.2, 3.3 and Migration step 6 are unconditional | MEDIUM | A-21: applied: the AND moved to the re-base step, its text kept in `tasks.md` 2.3, and not added if PR #27 is not ratified; 3.2, 3.3 and Migration step 6 conditional on its ratification | project-clean delta (ADDED); Dependencies and Sequencing (archive order); `tasks.md` 2.3, 3.2, 3.3; `design.md` D10, Migration Plan |
| lane 3 re-read (ca96701) MEDIUM-3: `--not` on `rev-list`'s standard input may need Git 2.42, above the 2.36 floor | MEDIUM | A-21: applied: the merge target's exclusion is a line `^<merge target SHA>`, checked on Git 2.43.0 (2.36 not available here), its fixture on D9's floor job; an AND has the wrapper record no `--not` on standard input | project-clean delta (ADDED item 1 and AND); What Changes; Decisions, readings (A-16); `design.md` Context, D4, D9 |
| lane 3 re-read (ca96701) LOW-1: "every command printed next carries the flag" contradicts the `delete-branch` retry lines | LOW | A-21 with A-22(a): applied: scoped to the `project clean --all-safe` commands, the deferral line and the stop block's `Next:`; the retry never carries the flag | project-clean delta (ADDED); What Changes; Decisions; `design.md` D8 |
| lane 3 re-read (ca96701) LOW-2: the Budgets clause goes beyond A-20 and LQ-6, the drop rule ignores it, and a base sentence is rewrapped | LOW | A-21: applied with change: the clause is recorded as part of A-20, and the block is dropped only if PR #19 also absorbs a Budgets exception that covers it; the cosmetic rewrap at `specs/project-command/spec.md:125-126` is declined, because that block is lane openRepoProject-2's agreed `16051d1` and its words equal the base's, so a rewrap would reopen lane 2's check for no change of content | Capabilities (project-command); Dependencies and Sequencing; `tasks.md` 1.6 |
| lane 3 re-read (ca96701) LOW-3: lane 2's agreement, council B's refinements and A-16 as amended were cited without a readable record | LOW | A-21: applied: `lanes/log/openRepoProject-5.md:34` and lane 2's handoff `:49` for the agreement, the lane's handoff `:50` at `c3a9b3767` for the refinements, and `lanes/log/openRepoProject-5.md:33` for A-16 as amended, all on the lane register | citation key; Dependencies and Sequencing; Decisions, readings; Council Verdicts (AE-1 and council B rows); `tasks.md` 1.3 |
| lane 3 re-read (ca96701) LOW-4: `CAS/pc:105-111` stops one line short of the fifteenth class | LOW | A-21: applied: `CAS/pc:107-112`, checked at `e9d6711` | Capabilities; Council Verdicts (L4 row) |
| lane 3 re-read (ca96701) LOW-5: "forced removal" cited to `BA:1344-1345` | LOW | A-21: applied: `BA:1295-1296` | Rules This Change Keeps |
| lane 3 re-read (ca96701) LOW-6: PR #27 described as it no longer reads | LOW | A-21: applied, as it reads at `e906c2f`: (a) its fit sentence's "at most 250 Git children besides the 16 removals, about 42.3 s"; (b) "the cache stage's reads" are abandoned at their budget; (c) the joint residual-window line, by A-23(a); (d) its Status quoted at `e906c2f`; round A5 cites each at `e1049b2`, where (a) to (c) still hold (lane 3's delta read, D11) | Dependencies and Sequencing; `design.md` D3, D7, D8; `tasks.md` 2.3 |
| lane 3 re-read (ca96701) LOW-7: the M3 Dependency is out of step with A-16 | LOW | A-21: applied, as M3 above | Dependencies and Sequencing |
| lane 3 re-read (ca96701) LOW-8: no re-ratification after a re-base that changes a PR #19 block, and the archive waits for PR #19 even if it closes | LOW | A-21: applied: a re-base that changes either block returns it to Brett Heap; the archive follows PR #19's amendment landing, as L-16 says, or, if PR #19 closes unmerged, the re-base on change 1's archived text | Dependencies and Sequencing; `tasks.md` 2.2, 3.3; `design.md` Migration Plan |
| lane 3 re-read (ca96701) LOW-9: "Git refuses the branch deletion" does not state the first target's upstream | LOW | A-21: applied: its upstream remote-tracking ref present | project-clean delta (ADDED scenario) |
| lane 3 re-read (ca96701) LOW-10: the `head-not-merge-target` step fails when a linked worktree holds the merge target | LOW | A-21: applied: the line then names a detached checkout of the merge target's tip, checked on Git 2.43.0; one AND | project-clean delta (ADDED and "A branch Git would judge against another HEAD is kept"); `design.md` Context, D8 |
| lane 3 re-read (ca96701) LOW-11: the line for a shared branch whose last holder was not removed | LOW | A-21: applied: one line, `Kept BRANCH (branch-shared)` with the holder and its next step; one AND | project-clean delta (ADDED and "A branch another worktree holds is retained"); `design.md` D8 |
| lane 3 re-read (ca96701) LOW-12: the revalidation's sourcing under the flag is stated only in the design | LOW | A-21: applied: one clause in the narrow guarantee; rerunning the repository part after each stage not taken, as three more children per target | review-safety delta; Capabilities (review-safety); `design.md` D2 |
| lane 3 re-read (ca96701) LOW-13: the branch child's wait on a signal departs from `BA:466-468` unnamed | LOW | A-21: applied: named beside change 1's V1 (CAS `proposal.md:866-867`) | Decisions, readings |
| lane 3 re-read (ca96701) LOW-14: task 1.3 omits `ca96701`, a pointer names an old heading, and old counts are unmarked | LOW | A-21: applied | `tasks.md` 1.3; alignment table (SA-3 row) and its note |
| lane 3 re-read (ca96701) LOW-15: "the keys that requirement lists" lists none for `selected` entries | LOW | A-21: applied: reworded | project-clean delta (ADDED) |
| lane 3 review-26 M1: PR #19's pending text ratified through this change (PARTLY at `ca96701`) | MEDIUM | A-21: applied, as LOW-8 | as LOW-8 |
| lane 3 review-26 M4: PR #27 relied on as if ratified (PARTLY at `ca96701`) | MEDIUM | A-21: applied, as MEDIUM-2 | as MEDIUM-2 |
| lane 3 review-26 L4: change-1-only text cited by canonical lines (PARTLY at `ca96701`) | LOW | A-21: applied, as LOW-4 | as LOW-4 |
| Codex (785a45e) P1 at spec.md:1006: the flag on every next command contradicts the retry lines | P1 | A-22(a): applied, as LOW-1 | as LOW-1 |
| Codex (785a45e) P2 at spec.md:997: branch names unquoted in printed commands | P2 | A-22(b): applied: branch and merge-target names follow change 1's path rule (`CAS/pc:1061-1066`); one scenario, a branch named `topic;id`, its lines checked through `dash` on Git 2.43.0 | project-clean delta (ADDED, new scenario); What Changes; Decisions; `design.md` Context, D8, D9 |
| Codex (785a45e) P2 at spec.md:988: the restore command runs in the caller's directory | P2 | A-22(c): applied, with the lead's additions from F-1 and F-2: `git -C ROOT branch`, `update-ref refs/heads/BRANCH SHA ''` for a name that begins with `-`, `reflog show refs/heads/BRANCH`, and `--branch=BRANCH` for such a name; each checked on Git 2.43.0 | project-clean delta (ADDED); What Changes; Decisions; Open Questions; `design.md` Context, D8, Risks, Rollback |
| B2 escalation 3 (a): the residual-window line of a flagged run with a cache target | escalation | A-23(a): applied: the cache change's line with this change's branch clause before its last clause, said alike in the narrow guarantee, D8 and the proposal; the flagged line pinned in an AND | review-safety delta; What Changes; Dependencies and Sequencing; `design.md` D8 |
| B2 escalation 3 (b): D7's joint fit excluded the cache stages' filesystem time | escalation | A-23(b): applied: B-25's walk and stage costs added whole; "13 of 16, 11 in the worst case" becomes 10 and 8 through one worker per stage, 5 and 4 at a thread per call; at measured costs all 16 fit through a worker, and at a thread per call the worst case defers at least the 16th; no cap changed, `limits.targets` 16 and A-9 still Brett Heap's | `design.md` D7, Risks; Decisions; Open Questions |
| council C product-advocate (c928cb2): PR #29's evidence-model block described as pending | LOW | the lead's note under A-21's LOW-6, extended to #29: applied: committed at `f66ed58`, on PR #19's text, agreed by lane openRepoProject-2 with one fix and unchanged at `c928cb2`; L-17's re-base kept; no other passage called it pending | Dependencies and Sequencing; `tasks.md` 2.4 |

### Re-read and Codex Findings (round A4)

Codex re-reviewed this change at `abad010` and found one P1 (comment
4323748513, on the ADDED requirement at `specs/project-clean/spec.md:881`),
which the lead's ruling A-24 of 2026-10-20 accepts; lane openRepoProject-3's
delta read of `ca96701..abad010` had not reported when this round was
committed, so it has no row here. The one row below is applied, none is
applied with change and none is declined; round A3's figures for B2's
escalation (b) are those of their round, and the fit now stands as this row
gives it.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Codex (abad010) P1 at spec.md:881: the stage relies on the plan's reflog proof, so a branch moved to an unmerged commit and reset to its planned SHA between the plan and the stage passes the re-read, and `branch -d` deletes the only reference to that commit | P1 | A-24: applied: the re-read's last step re-proves the reflog with A-16's proof as amended (the commits the reflog then names, then the `^<merge target SHA>` line, on standard input), one probe child under the re-read's budget, `min(5 s, work remaining less the removal floor)`, counted under `probes` and the sub-record's `probes_performed`; a commit printed, or a read or child that fails or times out at its own budget, retains the branch with `reflog-unmerged`, a retention the stage discovers, so the target's removal stands and the run stops with exit 2, and a re-proof the deadline stops retains it with `deadline-exceeded`; the narrow guarantee and the residual window name the re-proof; the fit restated at four stage children per retired branch: at the packet's costs 14 removed and 13 retired, was 15 and 14, and 12 and 11 in the worst case, was 13 and 13; with the cache change 9 targets through their stage through one worker per stage, was 10, 8 in the worst case, unchanged, and 5, or 3, at a thread per call, was 5, or 4; at change 1's measured costs all 16 still fit through a worker (the 16th removal near 39.15 s, was 36.9 s), while at a thread per call the 16th target is now deferred even with one reflog child (near 46.05 s, was 43.8 s); no cap changed and A-9 stays Brett Heap's; the project-command block's Budgets clause covers the re-proof as the re-read's last step, so nothing is held; one scenario added, the move and back checked on Git 2.43.0 | project-clean delta (bounds; ADDED: the stage, the sub-record, the counts, two scenarios' counts and the new scenario "A branch moved to an unmerged commit and back is retained"); review-safety delta; What Changes; Rules; Capabilities; Decisions; Open Questions; `design.md` Context, D2 to D7, D9, Risks; `tasks.md` 1.3 to 1.5 |

### Re-read and Codex Findings (round A5)

Lane openRepoProject-3 read this change's rounds A3 and A4, `ca96701..9ff8202`
(`delta-26-a3-findings.md` at the register's `653112ca8`): no HIGH and no
MEDIUM, the 28 rows of round A3 holding, A-24's re-proof faithful to change
1's revalidation rule, `BA:1339-1345` and the exit table, and the fit at 81
children reproduced, with twelve LOWs, D1 to D12, D3's second part resolved
in round A4. The lead's ruling A-26 accepts all twelve, as lane 3 words their
fixes, the nine of its message with D1, D5, D6 and D10 as their ninth. Codex
re-reviewed `9ff8202` and found two P2s, which the rulings A-27 and A-28 as
amended answer, and the ruling A-25 has this change name the cache change's
worst shapes at `e1049b2`. Lane openRepoProject-2's reading of A-24's
placement answers lane 3's first open item, so `specs/project-command/spec.md`
is unchanged. Of the 16 rows below, 13 are applied, 2 are applied with change
(lane 3's D11 and Codex's P2 at line 1050), 1 is a ruling with no edit (lane
openRepoProject-2's reading, the last row), and none is declined; the
scenarios stay 68, 4 and 9, round A5 adding ANDs only. Git facts were checked
on Git 2.43.0 in a scratch repository (`design.md` Context).

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| lead (A-25): D7 used only the cache change's inputs for ordinary trees, leaving its worst shapes at `e1049b2` unnamed | ruling | A-25: applied: one sentence in D7 names the walk where every recorded object is a directory (about 32,800 calls, 7.3 s through one worker and 20.4 s at a thread per call) and the deep chains (up to 43,947 opens a pass for one target) as outside the joint fit, under that change's B-3/CD-6 question and its `cache_opens` Open Question; no arithmetic changes, since the ordinary-tree inputs (about 9,000 walk calls and 8,500 stage calls, 2 s and 5.6 s, and 2 s and 5.3 s) are unchanged at `e1049b2` | `design.md` D7; Decisions (A-9); Open Questions (A-9) |
| lane 3 delta read (9ff8202) D4 (A-26, item 1): a failed or timed-out proof, at the plan or at the re-proof, prints "its reflog names commits MERGE_TARGET lacks" | LOW | A-26: applied, lane 3's first fix: every `reflog-unmerged` line reads `its reflog is not proven merged into MERGE_TARGET; inspect git -C ROOT reflog show refs/heads/BRANCH before any delete-branch`, and the failing re-proof's AND pins that line | project-clean delta (ADDED: the line; "A branch whose reflog holds amended-away work keeps it"; "A branch moved to an unmerged commit and back is retained"); `design.md` D8 |
| lane 3 delta read (9ff8202) D7 (A-26, item 2): no scenario for the deadline at the plan's proof, nor for the deadline or a signal stopping the re-proof | LOW | A-26: applied as lane 3 words it, two ANDs: a reflog child that starts with less than 5 s of work left and meets the deadline makes the plan incomplete with `deadline-exceeded`, a flagged preview exiting 1 and `--apply` refusing with exit 2 before any question or mutation; a re-proof whose budget ends at the removal floor is `retained` with `deadline-exceeded`, exit 1, and one SIGINT stops is `retained` with `interrupted`, exit 130, the next target `not-attempted` with `interrupted` and `branch-retention-stop` | project-clean delta (ADDED: "A branch whose reflog holds amended-away work keeps it"; "A branch moved to an unmerged commit and back is retained"); `design.md` D9 |
| lane 3 delta read (9ff8202) D8 (A-26, item 3): "one line `^` followed by the merge target's SHA" reads as two lines, which Git refuses | LOW | A-26: applied: the one line `^<merge target SHA>`, `^` immediately followed by the SHA, in the ADDED item 1 and step 3, `design.md` D4 twice, its Context and D9, and What Changes and the A-16 reading; checked: after a branch's named commits the one line prints an amended-away draft and nothing for a plain history, exit 0, and a line `^` before the SHA's own line fails, "bad revision '^'", exit 128 | project-clean delta (ADDED item 1, step 3); `design.md` Context, D4, D9; What Changes; Decisions, readings (A-16) |
| lane 3 delta read (9ff8202) D12 (A-26, item 4): step 2 says no Git child computes the head's ancestry again, while step 3's re-proof is given the head | LOW | A-26: applied: "no Git child but item 3's re-proof, given the head among the commits the reflog names, computes it again", `design.md` D4 alike, and What Changes reads "the plan's proof that the head is merged holds" | project-clean delta (ADDED step 2); `design.md` D4; What Changes |
| lane 3 delta read (9ff8202) D3(i) (A-26, item 5): the cache stages "taken whole before the first removal, the worst order" are a bound, not an order a run can take | LOW | A-26: applied: called a bound, and the worst order a run can take named, the 8 cache targets that the totals select first, with its arithmetic: at a thread per call 6 removed and 6 retired with one reflog child, or 5 and 5 with 17, where the bound gives 5 and 5, or 4 and 3; through a worker the counts are the bound's; the thread-per-call counts the proposal and Risks give now read "at least" | `design.md` D7, Risks; Decisions (A-9); Open Questions (A-9) |
| lane 3 delta read (9ff8202) D2 (A-26, item 6): the measured-cost figures take the 16 enumerations at 2.4 s, the cache change at most about 3.7 s | LOW | A-26: applied: each named, 2.4 s at the packet's 150 ms a child, as the stage and reflog children are taken, and 3.7 s at change 1's measured costs (the cache change's D4 at `e1049b2`), which moves each figure 1.3 s later, to 40.45 s and 42.85 s through a worker and 47.35 s and 49.75 s at a thread per call, changing no conclusion | `design.md` D7; Open Questions (A-9) |
| lane 3 delta read (9ff8202) D11 (A-26, item 7): PR #27 cited at `e906c2f`, its head now `e1049b2` | LOW | A-26: applied with change: the Status quote, the fit sentence (exact at `e1049b2`), D13's line, D7's inputs and task 2.3 now cite `e1049b2`; the round A3 row for LOW-6 keeps `e906c2f`, the head that round read, and names `e1049b2` beside it, so that the record of round A3 stays true | Dependencies and Sequencing (archive order); `design.md` D7, D8; `tasks.md` 2.3; the round A3 table (LOW-6 row) |
| lane 3 delta read (9ff8202) D9 (A-26, item 8): the quoting scenario lacks the `reflog-unmerged`, `branch-changed` and `$'...'` cases | LOW | A-26: applied: one AND with `Kept topic;id (reflog-unmerged)` and its quoted `'refs/heads/topic;id'`, and `Kept topic;id (branch-changed)` with its quoted retry, and one AND for a branch named `topic`, U+202E and `x`, printed in the `$'...'` form in prose and command, its restore line recreating it when run by bash in a UTF-8 locale | project-clean delta (ADDED, "A branch name in a printed command is quoted for the shell"); `design.md` Context, D9 |
| lane 3 delta read (9ff8202) D1 (A-26, item 9): the drop condition's example, the clause LQ-6 lists for #29, would not meet the condition | LOW | A-26: applied: the example is deleted, and the Budgets exception must sit in the sentence that gives each Git child `min(5 s, work remaining)`, since the re-read and its re-proof are Git children; `tasks.md` 1.6, consistent with it, is unchanged | Dependencies and Sequencing (the project-command block) |
| lane 3 delta read (9ff8202) D5 (A-26, item 9): the retry printed for a name that begins with `-` cannot run on change 1's action, which passes no `--` | LOW | A-26: applied: the ADDED requirement says that for such a name RETRY is the command that action is given, which deletes the branch only if the action passes the name after `--`; a Dependency on change 1, and D8's exception to "no line prints a retry the plan knows will fail"; checked: `branch -d -f` fails, "branch name required", exit 128, the ref staying, and `branch -d -- -f` deletes it | project-clean delta (ADDED, RETRY); Dependencies and Sequencing (new bullet); `design.md` Context, D8; What Changes |
| lane 3 delta read (9ff8202) D6 (A-26, item 9): the narrow guarantee names "those for a cache stage", which only the unratified PR #27 defines | LOW | A-26: applied: the residual-window sentence places the branch clause "after every other clause the run's line names and before its last clause"; the cache wording stays in `design.md` D8 and joins the narrow guarantee's re-base in `tasks.md` 2.3 | review-safety delta; `tasks.md` 2.3 |
| lane 3 delta read (9ff8202) D10 (A-26, item 9): the Context rows quote Git 2.43's messages, which differ on 2.36.6 and 2.40.4 | LOW | A-26: applied: the Context marks the quoted messages as 2.43.0's and gives the three that lane 3 found different on 2.36.6 and 2.40.4, as it reports them, not re-run here; D9's fixtures assert exit statuses and outcomes, never Git's wording | `design.md` Context, D9 |
| Codex (9ff8202) P2 at spec.md:1022 (comment 4324517974): `git branch` refuses to recreate a branch named `HEAD`, so its restore line fails | P2 | A-27: applied: the `update-ref` restore line for every name that `git branch` refuses to create, one that begins with `-` or equals `HEAD`, every other name keeping `git -C ROOT branch BRANCH SHA`, and the quoting scenario's AND extended with `refs/heads/HEAD`; checked: `git branch HEAD <sha>` refuses, "'HEAD' is not a valid branch name", exit 128, a worktree holds `refs/heads/HEAD`, `branch -d -- HEAD` deletes it, and `git -C '<root>' update-ref refs/heads/HEAD <sha> ''`, run by dash from another directory, recreates it and refuses when it exists | project-clean delta (ADDED: the restore line; "A branch name in a printed command is quoted for the shell"); `design.md` Context, D8, D9, Risks; What Changes; Decisions |
| Codex (9ff8202) P2 at spec.md:1050 (comment 4324517988): the `$'...'` form in a command specified as POSIX-shell-compatible, which dash does not implement | P2 | A-28 as amended: applied with change: no runtime text, the printed lines staying in change 1's form; `design.md` D8 and the README text that `tasks.md` names record that a command in that form needs bash, zsh, ksh93 or a POSIX.1-2024 shell, that dash, Ubuntu's `/bin/sh`, lacks it, and that change 1's path rule shares the limitation (lane openRepoProject-2's R-60); the change: the note also names the UTF-8 locale that its `\u` and `\U` escapes need, because with `LC_ALL=C` bash 5.2.21 passes `\u202e` as text and zsh 5.9 refuses it, and both drop a `\U` escape, which names another branch, while with `LC_ALL=C.UTF-8` both recreate the branch; ksh93 was not available to check | `design.md` Context, D8, D9, Migration Plan; Impact (README); What Changes; Decisions; `tasks.md` Speckit Handoff |
| lane 3 delta read (9ff8202), its first open item, and A-26's question to lane openRepoProject-2: whether the Budgets clause's "re-read of a branch stage" covers the re-proof | ruling | lane openRepoProject-2's reading, in the lead's rulings of 2026-10-20: every evidence read the stage makes before `branch -d` counts, on the condition that this change's own requirement makes the re-proof the re-read's last step under the same budget, which the ADDED step 3 and the bounds block do; nothing is held, and `specs/project-command/spec.md` is unchanged (blob `e7665dda`) | none |

### Re-read and Codex Findings (round A6)

Lane openRepoProject-3 read round A5, `9ff8202..9b67e8c`
(`delta-26-a5-findings.md` at the register's `196e1c1b3`): no HIGH and no
MEDIUM, four LOW wording items (L1 to L4) and one cross-PR note (N1), and it
found no round needed. The lead's ruling A-29 takes the four LOWs in a short
round, on lines at `9b67e8c`; lane 3 confirms that A-25 to A-28 and lane
openRepoProject-2's condition hold, that the `project-command` blob is
unchanged and that no line presumes Brett Heap's answer to lane
openRepoProject-2's LQ-8. Of the 5 rows below, 4 are applied and 1 is a
ruling with no edit; none is applied with change and none is declined. Round
A6 edits no spec file, so the scenarios stay 68, 4 and 9, and the quoting
scenario's literal stays as it is. Lane 3 could not check whether
POSIX.1-2024's `$'...'` form accepts the code-point escapes, nor ksh93, which
was not installed; the shells list is the lead's own (ruling A-28 as amended),
and this round adds no claim about either.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| lane 3 delta read (9b67e8c) L1 (A-29): Decisions says the kept branch's next step "never prints a retry the plan knows will fail", with no exception for a name that begins with `-`, which What Changes and `design.md` D8 have | LOW | A-29: applied: the sentence reads "the retry of a name that begins with `-` excepted while change 1's action passes no `--`", as What Changes and D8 word it, so Decisions alone no longer reads as contradicting the Dependency on change 1's `delete-branch` | Decisions (the result names every branch) |
| lane 3 delta read (9b67e8c) L2 (A-29): the `$'...'` note's UTF-8 locale clause, the README text and the quoting scenario's literal would go stale, with nothing saying so, if Brett Heap rules lane openRepoProject-2's LQ-8 on change 1's command form | LOW | A-29: applied: one clause each in `design.md` D8, Impact (README) and `tasks.md`'s Speckit Handoff: the note, the README text and the quoting scenario's literal follow change 1's command form as ratified, whether that form changes being lane openRepoProject-2's LQ-8, with Brett Heap; this change takes no side on it and reads no answer into it; the spec scenario at `specs/project-clean/spec.md:1499-1504` is not edited, because it is correct as it stands against change 1's form as ratified (`CAS/pc:1061-1066`), so nothing is held | `design.md` D8 and its Context map; Impact (README); `tasks.md` Speckit Handoff |
| lane 3 delta read (9b67e8c) L3 (A-29): the README text that `tasks.md` and Impact prescribe omits the shells list, which only D8 names | LOW | A-29: applied: both name it as D8 does, bash, zsh, ksh93 or a POSIX.1-2024 shell, beside the UTF-8 locale and dash's lack of the form | Impact (README); `tasks.md` Speckit Handoff |
| lane 3 delta read (9b67e8c) L4 (A-29): round A5's prose says "14 are applied", which counts its last row, lane openRepoProject-2's reading, a ruling with no edit | LOW | A-29: applied: the 16 rows of the round A5 table recounted by their Ruling cells, 13 applied, 2 applied with change (lane 3's D11 and Codex's P2 at line 1050) and 1 ruling with no edit, the count lane 3 found; the prose reads so and names that row; round A5's last commit message keeps the earlier count, which a later commit does not change | Re-read and Codex Findings (round A5), its opening prose |
| lane 3 delta read (9b67e8c) N1, a note on PR #27: its `design.md` D4 gives this change's thread-per-call counts as they stood before round A5, "5 and 5, or 4 and 3", where this change now says "at least" 5, or 3, with 6, or 5, as the worst order a run can take | note | the lead's B-42: no edit here: the restatement is PR #27's, taken in its round B6 against this change at `9b67e8c`, and round A6 changes none of these figures | none |

### Re-read and Codex Findings (round A7)

The lane's review wave of 2026-10-21 read this change at `01b5dd8`. Reader RA
read it adversarially (no HIGH, 3 MEDIUM, 5 LOW) and found that, beyond the
window ruling A-2 accepts, `--retire-branches` cannot delete a branch whose
work is missing from the merge target, or one that is checked out: every
finding is a gap in records or specification. Reader RD read how this
change, PR #27 and PR #29 compose in archive order; its M1, M3, M4 and four
LOWs are this change's, and its M2 is PR #27's (the lead's B-52). Reader RE
read feature 004 at `2cf34d3` against the drafts; the lead's ruling A-34
applies its RE-2 and RE-3, its RE-1 being RA's MEDIUM-1, and records RE-4,
RE-6, RE-7 and RE-8 for alignment when feature 004 merges. The lead's rulings
A-30 to A-34 bind. Of the 22 rows below, 15 are applied, 3 are applied with
change (RA's LOW-5, RD's M3 and RE's RE-2), 4 are rulings with no edit (RE-4,
RE-6, RE-7 and RE-8), and none is declined. RE's other findings, RE-5, whose
subject A-31 meets, and RE-9 to RE-17, were recorded by A-34 for alignment
with no edit. No ruling needs `specs/project-command/spec.md`, lane
openRepoProject-2's agreed block, which is unchanged (blob `e7665dda`). Round
A7 adds no scenario; it edits WHENs and ANDs, so the scenarios stay 68, 4
and 9. Git facts were checked on Git 2.43.0 in a scratch
repository (`design.md` Context), and feature 004's code at `2cf34d3` was
read only as a check.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| RA (01b5dd8) MEDIUM-1: "`retire` ... as its last member, after the selected triples" cannot hold under feature 004's canonical text, a JSON object with sorted keys, and the order of the retire pairs is undefined | MEDIUM | A-30: applied: change 1 and PR #19 name what the canonical JSON text covers and not its layout (`CAS/pc:629-632`, the same at `c462d87`), so the ADDED requirement names the member `retire` and leaves its position to that construction, its pairs ordered as `selected` is, each at its branch's last holder; D10, the archive-order note and task 2.3's AND pin no position; checked against feature 004's `project:3729-3749` at `2cf34d3`, where `retire` sorts before `selected` (reproduced) | project-clean delta (ADDED); Dependencies and Sequencing (archive order); `design.md` D10; `tasks.md` 2.3 |
| RA (01b5dd8) MEDIUM-2: an exception during a branch stage is recorded by change 1's rule as `unknown` and `target-not-removed`, even after the branch child deleted the branch | MEDIUM | A-31: applied: under the flag an exception in the stage leaves the target as its rescan decided it, and `branch_retirement` takes what the stage established, `retained` or `retired` with `internal-error`, a reason of the sub-record's own enum, or null with `reconciliation-incomplete` once a branch child ran and no post-check decided, never `target-not-removed`; a deletion the post-check saw is `retired`, with its SHA and restore line printed; the reconcilable block's exception sentence names the exception; one AND pins the three cases; and, from RA's fix, "a fault" in three ADDED scenarios is reworded to the failed listing or spawn it meant, the WHEN of "A post-check that cannot decide" also gaining two preconditions, its branch child "the real Git's", so that the deletion its `Unconfirmed` line reports is real, and "for the first of two targets", so that a later target is there to be `not-attempted` | project-clean delta (reconcilable block; ADDED; "The merge target moves before the branch stage", "A branch child that cannot be spawned", "A post-check that cannot decide"); What Changes; Capabilities; Decisions, readings; `design.md` D5, D6, D9, Risks |
| RA (01b5dd8) MEDIUM-3: a null `stage` has no human line, and R, K and G cannot add up for it | MEDIUM | A-31: applied, applying A-19 without reopening it: `; unconfirmed: U` in the summary when U is above 0, R, K, G and U adding up, and the line `Unconfirmed BRANCH (was SHA); if git -C ROOT rev-parse --verify refs/heads/BRANCH fails, restore: ` with the restore command, never `Kept`, nor named among a stopped run's retained branches; checked: `rev-parse --verify` exits 128 for a deleted ref, 0 for `refs/heads/-f` and `refs/heads/HEAD`; one AND | project-clean delta (ADDED; "A post-check that cannot decide"); What Changes; Decisions, readings; `design.md` Context, D5, D8 |
| RA (01b5dd8) LOW-4: a branch that another local branch tracks as its upstream is retired without notice | LOW | A-32: applied: after its `Retired` line, `Note: BRANCH2 tracks BRANCH as its upstream, which now reads gone; no commit is lost`, from the plan's ref listing, with no child; a later row on BRANCH2, refused with `state-changed` at its revalidation, stands; reproduced: `branch -d` deletes `b1` without a word, `b3`'s upstream reads `[gone]`, and the restore line restores it; one AND | project-clean delta (ADDED; "Retire the branches of a batch"); What Changes; Decisions; `design.md` Context, D8, D9, Risks |
| RA (01b5dd8) LOW-5: a branch being rebased or bisected in another worktree is invisible to the registry listing, so Git refuses it and the printed retry fails the same way | LOW | A-32: applied with change: stated as a residual in the ADDED requirement, and the `git-refused` line, with the upstream ref present, reads `; if a rebase or bisect in another worktree holds BRANCH, wait for it to end and remove that worktree; then retry: RETRY`; the change: the hint also says to remove that worktree, because, reproduced for a rebase and a bisect, once either ends that worktree holds the branch again and Git still refuses until it is removed; two scenario literals updated and one AND with the real Git | project-clean delta (ADDED; "Git refuses the branch deletion"; "A branch name in a printed command is quoted for the shell"); Decisions; `design.md` Context, D4, D8, D9, Risks |
| RA (01b5dd8) LOW-6: the re-proof's outcome rule omits the gate's other undecidable readings | LOW | A-32: applied: a line that does not parse, and a last entry whose new object is not the head the re-read observed, keep the branch with `reflog-unmerged` | project-clean delta (ADDED step 3); `design.md` D4 |
| RA (01b5dd8) LOW-7: `branch_plan` and the plan line are unspecified for a row whose proof did not finish | LOW | A-32: applied: such a row keeps its branch with `reflog-unmerged`, in its `branch_plan` and plan line, as a failed proof keeps it; no apply runs on such a plan | project-clean delta (ADDED item 1); `design.md` D4 |
| RA (01b5dd8) LOW-8: two scenarios leave out a precondition, and exit row 2 lacks D6's clause | LOW | A-32: applied: "The merge target moves before the branch stage" has the main worktree on the merge target in its WHEN, which its AND inherits; the second AND of "The deadline before the branch stage" asserts the second target `not-attempted` with `deadline-exceeded`; exit row 2 reads "a branch stage's `deadline-exceeded` under `--retire-branches` included", worded so that every word of change 1's row stays | project-clean delta (reconcilable block; two ADDED scenarios); Capabilities |
| RD (01b5dd8) M1: the re-bases are checked by `validate` alone, which cannot see a dropped sentence | MEDIUM | A-33: applied: tasks 2.3, 2.4 and 3.2, and Migration steps 2 and 6, check each re-base and re-read by `diff -u` of the archived block against this change's block showing additions only, apart from the rewordings written out, `validate` being a second check | `tasks.md` 2.3, 2.4, 3.2; `design.md` Migration Plan; Dependencies and Sequencing (archive order) |
| RD (01b5dd8) M3: the re-base onto PR #27 rewrites this change's own words in two blocks, written nowhere and with no route back to Brett Heap | MEDIUM | A-33: applied with change: the batch digest sentence and "that guarantee", with the guarantee sentences' place, are written into the Migration Plan and D10 from RD's wording, and tasks 2.3 and 2.4 return a re-base that changes a block's added text beyond them to Brett Heap; the change: RD's batch wording placed the branches "after every selected triple and its cache data", a position left out under A-30 | `design.md` D10, Migration Plan; Dependencies and Sequencing (archive order); `tasks.md` 2.3, 2.4 |
| RD (01b5dd8) M4: "Clean reports local worktree state" is never re-read against change 1's archived text | MEDIUM | A-33: applied: task 2.1 and Migration step 2 re-read it and re-copy it with this change's one clause, checked by `diff -u` showing additions only | `tasks.md` 2.1; `design.md` Migration Plan; Dependencies and Sequencing |
| RD (01b5dd8) L1: the reconcilable block's note misses exit row 2, which both changes edit | LOW | A-33: applied: row 2 named as the one shared passage, its merged form written out with A-32's clause | Dependencies and Sequencing (archive order); `design.md` Migration Plan; `tasks.md` 2.3 |
| RD (01b5dd8) L2: the place of PR #27's `Caches disposed` line among this change's result lines is unstated | LOW | A-33: applied: after the summary line and before the branch lines | `design.md` D8, Migration Plan; Dependencies and Sequencing; `tasks.md` 2.3 |
| RD (01b5dd8) L3: the residual-window scenario does not exclude a cache target | LOW | A-33: applied for the re-base: its WHEN gains "in a run whose plan selects no cache target" at the re-base, written into the Migration Plan and task 2.3, since a cache target is a term of the unratified PR #27 | `design.md` Migration Plan; Dependencies and Sequencing; `tasks.md` 2.3 |
| RD (01b5dd8) L4: requirement names are quoted two ways in the composed evidence-model block | LOW | A-33: applied: this change's deltas quote requirement names in double quotes only (checked); its project-command block, agreed by lane openRepoProject-2, is not edited, so if this change archives second the composed block quotes PR #29's backquoted name in change 1's double quotes, a change of quoting only | `design.md` Migration Plan; Dependencies and Sequencing (the project-command block); `tasks.md` 2.4 |
| RE (2cf34d3) RE-1: the same finding as RA's MEDIUM-1 | HIGH | A-30, as RA's MEDIUM-1 above | as RA's MEDIUM-1 |
| RE (2cf34d3) RE-2: a signal is said to stop the stage's re-read and re-proof, where change 1's D15, and feature 004 with it, stops no child in the apply phase | HIGH | A-34: applied with change: a signal stops no read or child of the stage; one in flight runs to its own end or budget, its outcome decides, and the stage reads the slot before each start, retaining the branch with `interrupted` where the step that ran left it to retire; the SIGINT AND of "A branch moved to an unmerged commit and back is retained" now delays the re-proof by 2 s, which the signal does not stop, where the re-proof hung and was stopped; D4, D7, D9 and the readings follow; the change: RE-2 also asked what a second SIGINT does to the post-check, which A-34's summary does not name, and the text keeps change 1's rule, a second SIGINT abandoning it as change 1's D15 abandons the remaining rescans, the stage then null; checked: feature 004's phase probe, re-run, stops no child in its apply phase and stops one on a second SIGINT in its reconciling phase | project-clean delta (ADDED; "A branch moved to an unmerged commit and back is retained"); What Changes; Decisions, readings; `design.md` D4, D5, D7, D9 |
| RE (2cf34d3) RE-3: under the flag a retired branch would still be named as kept, and the flagged result's order against change 1's lines is undefined | MEDIUM | A-34: applied: under the flag the result ends with, in a run that stops, change 1's stop block and the retained branches it names, never a branch its line names retired, already gone or unconfirmed, then the summary and branch lines, then the residual-window line, change 1's D18 order with the flag's lines before the residual-window line; the retained list is computed from the branch lines, since the reconciliation read before the stage shows a retired branch present; two scenarios' result order re-pinned and one AND added; checked against feature 004's `print_result` at `2cf34d3` | project-clean delta (ADDED; "A branch moved after removal is retained and can be retried", "A retirement with a reason", "A branch moved to an unmerged commit and back is retained"); What Changes; Decisions, readings; `design.md` D8 |
| RE (2cf34d3) RE-4: the stage's budgets, phase, kind and counts have no counterpart in feature 004's runner | MEDIUM | A-34: no edit; recorded for alignment when feature 004 merges; checked against change 1's text: no contradiction of change 1 itself, the strict floor being this change's stated choice (`design.md` D7) and the shorter budget and the counts its own amendments in its MODIFIED blocks | none |
| RE (2cf34d3) RE-6: "the gate's read is reused" needs an API change in feature 004 | MEDIUM | A-34: no edit; recorded for alignment when feature 004 merges; a matter of feature 004's code, not of change 1's text, whose gate reads the reflog this change reuses | none |
| RE (2cf34d3) RE-7: the README's edit points at feature 004's head | MEDIUM | A-34: no edit; recorded for alignment when feature 004 merges; feature 004's README, not change 1's text | none |
| RE (2cf34d3) RE-8: the CI job list, chiefly PR #29's | MEDIUM | A-34: no edit; recorded for alignment when feature 004 merges; `tasks.md` 3.1 already names every job, `git-floor` included | none |

### Re-read and Codex Findings (round A8)

Lane openRepoProject-3's reader W1 read round A7, `01b5dd8..48e8119`
(`wave01i-a7-findings.md` at the register's `050e4492e`): no HIGH, 2 MEDIUM
and 8 LOW, F1 to F10. It found validate valid and 8 of 8, the scenarios 68, 4
and 9, all seven MODIFIED blocks carrying their source scenarios, the
project-command blob `e7665dda`, and A-30 faithful, change 1 and PR #19
fixing no layout of the digest's text. The lead's ruling A-35 accepts all
ten; where its wording differs from W1's suggested fix it governs, F9
refining A-33's reading of RD's L4 and F10 settling the D8 clause. Codex
reviewed `48e8119` and found no major issue. Of the 11 rows below, 9 are
applied, 1 is applied with change (F2), 1 is a review with no finding, and
none is declined. No ruling needs `specs/project-command/spec.md`, which is
unchanged (blob `e7665dda`). Round A8 adds no scenario and edits none, so the
scenarios stay 68, 4 and 9, and every MODIFIED block still carries its source
scenarios byte for byte; F1's clause is added to change 1's sentence with
none of its words changed. F5 to F8 correct round A7's own record in place,
and the round A7 row for RD's L4 keeps what that round did, which F9
replaces. Git facts were checked on Git 2.43.0 in a scratch repository
(`design.md` Context).

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| lane 3 confirm read (48e8119) F1: the flagged result order puts the summary and branch lines after the stop block, while the reconcilable block's carried sentence says that a run that stops ends its human result with `Stopped at ...` | MEDIUM | A-35: applied: that sentence gains, after its command, "or, under `--retire-branches`, with the lines that "Clean retires a removed worktree's branch only on fresh head and ancestry evidence" orders after it", added to change 1's sentence with none of its words changed, the block's eight scenarios carried byte for byte; Capabilities lists the clause; the reading of A-6's summary line no longer calls the flagged order change 1's own order, since change 1's D18 holds no summary or branch line after the stop block | project-clean delta (reconcilable block); Capabilities; Decisions, readings (A-6's summary line) |
| lane 3 confirm read (48e8119) F2: the exception rule departs from the packet's own rule, its exit status included, while the reading named only change 1's copy of the rule | MEDIUM | A-35: applied with change: the reading of an exception in a branch stage quotes the packet's rule and names its exit change, 1 becoming 2 by exit row 4, or staying 1 for a null `stage` by row 2, a departure recorded the way the reading of the branch child's wait records `BA:466-468`; the change: it is cited as `BA:479-482`, where W1 and A-35 give `BA:478-482`, because line 478 at `da33d92` is blank and the rule begins at 479 | Decisions, readings (an exception in a branch stage) |
| lane 3 confirm read (48e8119) F3: "SHALL only keep the stage from starting its next read or child" literally takes in the post-check, the stage's next read after its branch child | LOW | A-35: applied: "its next re-read, re-proof or branch child, never the post-check"; What Changes names the second SIGINT's exception, which abandons the post-check as change 1 abandons its remaining rescans; D7 and the reading of the branch child's wait read the same | project-clean delta (ADDED); What Changes; Decisions, readings (a branch child is waited for on a signal); `design.md` D7 |
| lane 3 confirm read (48e8119) F4: the rebase-or-bisect hint is on the `git-refused` line with the upstream ref present only, while Git refuses the same way with it absent | LOW | A-35: applied: the `git-refused` line with the upstream ref absent carries `; if a rebase or bisect in another worktree holds BRANCH, wait for it to end and remove that worktree` before its `; next: ` step, which stays the `head-not-merge-target` step, unchanged for that keep; reproduced on Git 2.43.0: W1's `exp2` re-run (a rebase stopped on a conflict, no upstream configured: "used by worktree", exit 1), and, for an eligible row's shape, a published branch whose upstream's remote-tracking ref was deleted, the main worktree on the merge target: Git refuses the same way, the step printed before this round, a checkout of the merge target the main worktree already holds, exits 0 while the retry still fails, and once the rebase ends and that worktree is removed the same steps delete the branch, exit 0 | project-clean delta (ADDED); `design.md` Context, D8 |
| lane 3 confirm read (48e8119) F5: "Round A7 adds ANDs only" is inexact, since round A7 also rewrote three WHENs and seven existing ANDs | LOW | A-35: applied: round A7 "adds no scenario; it edits WHENs and ANDs", in its prose and in `tasks.md` 1.4 | Re-read and Codex Findings (round A7), its opening prose; `tasks.md` 1.4 |
| lane 3 confirm read (48e8119) F6: the WHEN of "A post-check that cannot decide" gained two preconditions that no row names | LOW | A-35: applied: RA's MEDIUM-2 row names them, its branch child "the real Git's" and "for the first of two targets", with what each supports | Re-read and Codex Findings (round A7), RA's MEDIUM-2 row |
| lane 3 confirm read (48e8119) F7: RA's LOW-4 row omits What Changes, which gained the note | LOW | A-35: applied | Re-read and Codex Findings (round A7), RA's LOW-4 row |
| lane 3 confirm read (48e8119) F8: round A7's prose says that RE-5 and RE-9 to RE-17 "were not ruled for this round" | LOW | A-35: applied: they "were recorded by A-34 for alignment with no edit", and take no rows, as A-34 gives them none | Re-read and Codex Findings (round A7), its opening prose |
| lane 3 confirm read (48e8119) F9: RD's L4 was met by re-quoting PR #29's ratified words at this change's archive | LOW | A-35, refining A-33's reading of RD's L4: applied: a re-base never changes another change's ratified words, quotation marks included, and one-way quoting binds this change's own text only, so PR #29's backquoted requirement name stays as ratified and the composed block may hold both styles; the re-quote is withdrawn from the Migration Plan, the project-command Dependency and task 2.4, whose `diff -u` check needs no exception for quoting; the round A7 row for RD's L4 keeps what that round did | Dependencies and Sequencing (the project-command block); `design.md` Migration Plan; `tasks.md` 2.4 |
| lane 3 confirm read (48e8119) F10: D8 calls feature 004's stop form "the form this order extends", while its `Branches not confirmed:` line has no place in the flagged order | LOW | A-35: applied: D8 says that under the flag the per-branch `Unconfirmed` lines name each branch whose deletion is unconfirmed, and that whether feature 004's `Branches not confirmed:` line, which change 1's text does not hold (checked at `961c405` and at PR #19's `c462d87`), stays beside them is settled at the alignment with feature 004, with RE-4 to RE-8 | `design.md` D8 |
| Codex (48e8119): its review receipt on PR #26 of 2026-10-21T13:24:29Z, "Didn't find any major issues", for reviewed commit `48e81197b0` | none | no finding and no edit | none |

### Re-read and Codex Findings (round A9)

The lane's reader RF re-ran reader RD's composition at the final heads, this
change at `55375ce`, PR #27 at `e07cc42` and PR #29 at `3965dfb`: the same
eight conflict regions, each resolved by keeping both sides, this change's
two re-base rewordings still anchored in PR #27's text, and the real
`openspec archive` clean in three orders. Its M2, L1, L2 and L3 are this
change's, and its M1 is all three drafts'; the lead's ruling A-37 accepts
them, with M2's figures stated at PR #19's `c462d87` and at its settled head,
which the lead named as `6f2cb54` after lane openRepoProject-2's round of
2026-10-21, beside the case of seven children per revalidation. Lane
openRepoProject-3's reader W13 read round A8, `48e8119..55375ce`
(`confirm-a8-findings.md` at the register's `51a67d7b5`): no HIGH and no
MEDIUM, and two LOWs; the lead's ruling A-36 takes no action on LOW-1, the
short lines left by re-wrapping, and has LOW-2 ride in this round. Codex
reviewed `55375ce` and found no major issue. Of the 7 rows below, 6 are
applied, 1 is a review with no finding, and none is applied with change or
declined. No ruling needs `specs/project-command/spec.md`, which is unchanged
(blob `e7665dda`). Round A9 adds no scenario; it adds one AND to an ADDED
scenario, so the scenarios stay 68, 4 and 9, and every MODIFIED block still
carries its source scenarios byte for byte. The fit was re-derived from PR
#19's lines at each sha, and the AND's case checked on Git 2.43.0 in a
scratch repository.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| RF (55375ce) M2: the claim that this change's other blocks are byte-identical on `main` and PR #19 is false against PR #19's current text, and D7's fit, which feeds A-9 and the target-cap question, rests on change 1's superseded terms | MEDIUM | A-37, with the lead's two refinements of 2026-10-21 (the settled head `6f2cb54`, not `1ebdd90`; the seven-child case): applied: the Dependency reads "byte-identical on `main` and PR #19 at `c462d87`" (checked: the five blocks equal `main`'s there, and at `1ebdd90` and `6f2cb54` all seven differ); D7 states its fit at `c462d87` (F = 7, five children per revalidation: 14 removed, 13 retired) and at `6f2cb54`, whose inputs equal `1ebdd90`'s byte for byte: F = 8, at most 16 D21 probes and six children per revalidation, 11 and 10, RF's figures re-derived from PR #19's lines, and seven where the plan read `extensions.worktreeConfig` as true, 10 and 9, on D14's planning term as written, the 10th branch child at 45.0 s refused by its strict test, with D14's plan-time probe per linked row named and lane openRepoProject-2's check of that case; D7's other figures marked as at `c462d87`; ratification on `c462d87` (`tasks.md` 1.6) not blocked, the figures meeting PR #19's final text at the re-base; A-9 restated with them | Dependencies and Sequencing (on PR #19); Decisions (A-9; readings, the fit); Open Questions (A-9); citation key; `design.md` D7, Risks |
| RF (55375ce) M1, this change's share: every re-base check diffs the archived block against the re-based block, which cannot see a change to this change's own ratified words | MEDIUM | A-37: applied: tasks 2.1, 2.2, 2.3, 2.4 and 3.2 and the Migration Plan add a second `diff -u`, of this change's block as committed at its ratified head against the re-based block, which may show only the archived block's text carried in and the rewordings written out, the ADDED requirement included at 2.3 and 3.2, any other change returning the block to Brett Heap; the archived-against-re-based check is kept; 3.2 gains its return route, "before the archive"; wording matched to PR #29's round C15 (`tasks.md` 2.3 and 2.4 and its Migration Plan at `2eeaec4`); the archive-order note says the same | `tasks.md` 2.1 to 2.4, 3.2; `design.md` Migration Plan; Dependencies and Sequencing (archive order) |
| RF (55375ce) L1: the `Caches disposed` line's place needs an edit of the ADDED sentence that orders the flagged result, which no re-base step names and no words give | LOW | A-37: applied: the Migration Plan's human-result bullet writes that sentence's re-based words, "then the summary line, the line that "Clean disposes of listed caches before a worktree removal" adds to a successful apply, and the branch lines", checked against PR #27's ADDED requirement at `e07cc42`; task 2.3's list of rewordings and the archive-order note for the human result name that sentence (`specs/project-clean/spec.md:1121-1126`) | `design.md` Migration Plan; `tasks.md` 2.3; Dependencies and Sequencing (archive order) |
| RF (55375ce) L2: "a re-base never changes another change's ratified words" is broader than this change's own re-base onto PR #27 | LOW | A-37: applied: a re-base changes no other change's ratified words except the two rewordings of the cache change's words that this change's re-base makes, a scope added to its fit sentence and its "or" moved in exit-table row 2 (checked at `e07cc42`), each of which returns to Brett Heap, as task 2.3 now says | `design.md` Migration Plan; `tasks.md` 2.3 |
| RF (55375ce) L3: the archive-order note for the reconcilable block omits round A8's stop-sentence clause | LOW | A-37: applied: "and one clause of the stop sentence" | Dependencies and Sequencing (archive order) |
| lane 3 confirm read (55375ce) LOW-2: no scenario pins the `git-refused` hint with the upstream ref absent | LOW | A-36: applied: one AND on "Git refuses the branch deletion", whose WHEN has the upstream ref present; like that scenario's third AND, which puts the real Git in its test `git`'s place, it varies the WHEN with "instead" (the real Git and that AND's rebase, the upstream's ref deleted before the plan, the main worktree on the merge target, so that the plan retires the branch), so it contradicts no precondition, and pins the line with the rebase-or-bisect clause before its `next:` step; no scenario added; checked on Git 2.43.0: the rebase's worktree lists detached and `branch -d -- b` refuses, exit 1 | project-clean delta (ADDED, "Git refuses the branch deletion") |
| Codex (55375ce): its review on PR #26 of 2026-10-21T14:04:48Z, which found no major issues, as the lead's ruling A-36 records it | none | no finding and no edit | none |

### Re-read and Codex Findings (round A10)

Lane openRepoProject-3's reader W27 read round A9, `55375ce..d5896fc`
(`confirm-a9-findings.md` at the register's `15198dfdb`): no HIGH, no MEDIUM,
five LOWs and nothing departing. It re-derived D7's figures two ways, found
every MODIFIED block carrying its source scenarios, the project-command blob
`e7665dda`, validate 8 of 8 and the scenarios 68, 4 and 9, and framed
observations for a follow-on at PR #19's round (b). That round landed as
`4485678`, with lane openRepoProject-2's R-171, and `a664799`, with D14
restated on the child counts that lane measured (its R-178) and its open
question LQ-20 named. The lead's ruling A-38 takes W27's LOW-2 to LOW-5,
states D7's figures at `a664799`, aligns the branch stage's re-read with PR
#19's revalidation rule there, and corrects the citation key's main; W27's
LOW-1, on the lead's rulings file, needs no edit here. During the round the
lead refined A-38 from lane openRepoProject-3's read W31 of PR #19's round
(b). Codex reviewed `d5896fc` and found no major issue. Of the 9 rows below,
8 are applied, 1 is a review with no finding, and none is applied with
change or declined. No ruling needs `specs/project-command/spec.md`, which is
unchanged (blob `e7665dda`). Round A10 adds no scenario and edits none; it
edits one sentence of the ADDED requirement's step 2, so the scenarios stay
68, 4 and 9, and every MODIFIED block still carries its source scenarios byte
for byte. Every figure at `a664799` was re-derived from PR #19's lines there,
each input checked against `6f2cb54`, and equals W27's. The round also
updates `design.md`'s Context map, the Status clause, the citation key and
tasks 1.1, 1.3, 1.4 and 1.5, as earlier rounds did.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| lane 3 confirm read (d5896fc) LOW-2: the seven-child figure, "10 and 9 where the plan read `extensions.worktreeConfig` as true", in Decisions, the readings and Open Questions and in `design.md` Risks, drops D7's "on D14's planning term", which left out D14's plan-time probe on each linked row | LOW | A-38: applied with the follow-on below: the four places state PR #19's restated D14 at `a664799` instead, a flagged run at 128 rows removing and retiring nothing where the plan read `extensions.worktreeConfig` as true, at the packet's 150 ms per child (D14's model), a worst case that waits on Brett Heap's LQ-20 for PR #19; the 10 and 9 on D14's earlier planning term is no longer stated, since D14's planning term at `a664799` counts that probe | Decisions (A-9; readings, the fit); Open Questions (A-9); `design.md` Risks |
| lane 3 confirm read (d5896fc) LOW-3: D7's six-child bullet writes "0.9(k - 1)" without its parts | LOW | A-38: applied: each formula D7 states at `a664799`, for six children, for seven at 128 rows and for LQ-20's option (b), reads "after k - 1 removals and their 4(k - 1) stage children, at ... x 0.15 + 0.3(k - 1) + 0.6(k - 1)", as D7's paragraph at `c462d87` writes it; the seven-child bullet that gave only the sum, 24.45 + 1.95k s, is replaced by the follow-on below | `design.md` D7 |
| lane 3 confirm read (d5896fc) LOW-4: task 3.2's new return route says "a block's added text", where the Migration Plan, the archive-order note and reader RF's M1 say "this change's words" | LOW | A-38: applied in place: "a re-base that changes this change's words beyond the rewordings of 2.3 returns that block to Brett Heap for ratification before the archive" | `tasks.md` 3.2 |
| lane 3 confirm read (d5896fc) LOW-5: two of round A9's edits are named in no row of its table | LOW | A-38: applied here, round A9's table left as it is: round A9 also renamed "a second check" to "a check" in tasks 2.3, 2.4 and 3.2, and to "a further check" in `design.md`'s Migration Plan, once a second `diff -u` existed, and added its own sentence to `design.md`'s Context map; W27 found both faithful | none (round A9's edits of `tasks.md` 2.3, 2.4 and 3.2 and `design.md` Context and Migration Plan, recorded here) |
| A-38, the follow-on at PR #19's `a664799` (its round (b): `4485678`, lane openRepoProject-2's R-171, and `a664799`, D14 restated with its R-178 and LQ-20 named) | ruling | A-38: applied: D7 cites PR #19 at `a664799` for every input it took from `6f2cb54`, each checked by mapping the cited range by content: F at `design.md:327-328` and D14 `:875`, E and D21 at `:844-845`, six and seven children per revalidation at `specs/project-clean/spec.md:1020-1022`, `specs/project-clean-review-safety/spec.md:76-77` and `design.md:480-482`, and the per-row probe at `:433-435` are byte-identical, while D14's row at `:881` gains "row 4c false" and D21's sentence at `:918-919` opens its own paragraph, their figures unchanged; so the six-child bullet stays 11 removed and 10 retired, stated at `a664799`, with 16 removals without the flag; the seven-child bullet states D14 at `a664799`, a plan-time probe on each linked row where the plan read `extensions.worktreeConfig` as true (its `:891-893`), so that a flagged run at 128 rows is 0 and 0, its first removal due at 45.45 s, or 45.3 s without the flag, D14 stating that shortfall at its `:882` and `:905-911`; LQ-20's options there: (a) 0 and 0, no removal without the flag; (b) 9 and 8, 13 removals without the flag; (c) no figure in PR #19's record, all 16 needing a work deadline above 80.75 s, the 16th branch child being due at 75.75 s, and without the flag one of at least 70.55 s; "lane openRepoProject-2 is checking D14's fit for the seven-child case" removed, with its echoes in Decisions, the readings and Open Questions, each now saying that the worst case waits on Brett Heap's LQ-20 for PR #19; A-9 restated with these figures; the Dependency on PR #19 names `a664799` (checked: all seven requirements this change modifies differ from `c462d87` there, and the five blocks whose `c462d87` text is main's still equal main's at `15504f1`) | `design.md` D7, Risks, Context; Decisions (A-9; readings, the fit); Open Questions (A-9); Dependencies and Sequencing (on PR #19); citation key; Status |
| the lead's refinement of A-38, from lane openRepoProject-3's read W31 of PR #19's round (b): LQ-20 rests on D14's flat 150 ms per child, while PR #19's ratified D5 and its task 2.1 fit the caps on measured costs | ruling | applied: every figure stated at `a664799`, 11 and 10, 0 and 0, and LQ-20's 0 and 0 and 9 and 8, is named as at the packet's 150 ms per child (D14's model), kept apart from change 1's measured costs as this change already keeps the two; no measured-cost figure is added for the case where `extensions.worktreeConfig` is true, because PR #19's text at `a664799` states none: its task 2.1 gives measured costs for the status probe, `for-each-ref`, the merged set and the removal (its `tasks.md:108-112`) and none for the per-row work-tree probe, and it calls D21's walk unmeasured (its `design.md:918-921`); D7 said so as "the only figures for this case that PR #19's record supports", which overstated the record, since D5 and task 2.1 give a measured basis by arithmetic, and round A11 replaces that claim with the case on the three bases of D14 at `9267303` (its `design.md:960-965`): change 1 alone 0, 16 (15 with 20,000-file removals) and 11, and a flagged run 0 and 0, 14 and 14 (16 and 16 at task 2.1's average per child) and 7 and 7 (lane openRepoProject-3's W35, MEDIUM-1; rulings A-39 and A-40); A-9's wait reads "waits on Brett Heap's LQ-20 for PR #19, whose framing lane openRepoProject-2 may revise", and LQ-20's options are given as PR #19 frames them at `a664799` | `design.md` D7, Risks; Decisions (A-9; readings, the fit); Open Questions (A-9) |
| A-38, the R-171 alignment: the branch stage's re-read gave `state-changed` for a listing or manifest read that "fails or times out" (`specs/project-clean/spec.md:897-900` and `design.md:416-419` at `d5896fc`), a read the work deadline cuts included, where PR #19's general rule at `a664799` gives such a read `deadline-exceeded` | ruling | A-38: applied: step 2 of the ADDED requirement counts a read that fails or times out at its own 5 s budget as a difference, `state-changed`, and a read whose budget the work deadline ends as none, retaining the branch with `deadline-exceeded`, the outcome that the sub-record's reason list and `design.md` D4 and D5 already gave it; D4 cites PR #19's rule (its `specs/project-clean-review-safety/spec.md:117-127`, R-171) and states what changes for such a read: exit 1 by row 2, not 2 by row 4; its `Kept` line and the stop block naming `deadline-exceeded`; and the later targets `not-attempted` with `deadline-exceeded`, not `batch-stopped`; the next step unchanged; the re-proof's split (`specs/project-clean/spec.md:916-920`, was `:914-918`) kept; no scenario added or edited, since none states the outcome of a re-read the work deadline cuts: "The deadline before the branch stage" starts no re-read, the failing listing of "The merge target moves before the branch stage" stays `state-changed`, and the re-proof's AND is the re-proof's own split | project-clean delta (ADDED, step 2); `design.md` D4 |
| lane 3 confirm read (d5896fc), its observation that main has moved | note | A-38: applied: the citation key's "Main is now `e9d6711`, whose `openspec/` and `ideation/` equal `961c405`'s" now says what git shows at `origin/main` `15504f1`: `ideation/` moved with packet revision 1 (`e45155a`); `openspec/changes/` gained `refuse-non-directory-parent-early` and `support-later-python-versions`, whose deltas modify only project-command requirements that this change does not modify; `openspec/specs/`, change 1's and change 2's directories, `project`, `tests/test_project.py` and `README.md:178-201` are unchanged (the README's one change since, at `:282`, came with `e9d6711`); the other mentions of `e9d6711`, each a fact at that sha that still holds, are left | citation key |
| Codex (d5896fc): its review receipt on PR #26 of 2026-10-21T16:44:10Z, "Didn't find any major issues", for reviewed commit `d5896fcbf1` | none | no finding and no edit | none |

### Re-read and Codex Findings (round A11)

Lane openRepoProject-3's reader W35 read round A10, `d5896fc..4635bda`
(`confirm-a10-findings.md` at the register's `98a65851b`): no HIGH, one
MEDIUM, five LOWs and nothing departing. It re-derived the figures at
`a664799` two ways, equal to W27's, found the R-171 alignment faithful, every
MODIFIED block carrying its source scenarios, the project-command blob
`e7665dda`, validate 8 of 8 and the scenarios 68, 4 and 9. Its MEDIUM-1
found that "the only figures for this case that PR #19's record supports"
and "no figure at measured costs" overstated the record, which PR #19's
round (c), `2e819ad`, contradicted by stating D14's fit on three bases. The
lead's ruling A-39 takes all six items. PR #19's round (d) then landed as
`9267303`, D14's three bases unchanged and a second table giving each option
of LQ-20 on each basis for change 1, and the lead's ruling A-40 amends A-39:
every cite moves to `9267303`, D7 gives a flagged run's result under each
option on each basis, option (c)'s figure is reconciled, (c) is quoted in
round (d)'s words, and 45 s is the spawn limit. Lane openRepoProject-2
answered the lead at 02:29:29Z that "a larger removal floor" was its slip
and that (c) means a longer work deadline (this lane's
`rulings-2026-10-20.md:1193`, at the register's `1e5bdf22f`). Codex reviewed
`4635bda` and found no major issue. Of the 10 rows below, 7 are applied, 2
are applied with change, 1 is a review with no finding, and none is
declined. No ruling needs `specs/project-command/spec.md`, which is
unchanged (blob `e7665dda`). Round A11 adds no scenario; it edits one
phrase of the ADDED requirement's `state-changed` reason and the words of
one AND of an ADDED scenario, so the scenarios stay 68, 4 and 9, and every
MODIFIED block still carries its source scenarios byte for byte. Every
figure at `9267303` was derived two ways, by D7's closed form and by a step
simulation, after both had reproduced D14's own figures and its table for
change 1. The round also updates `design.md`'s Context map, the Status
clause, the citation key and tasks 1.1, 1.3, 1.4 and 1.5, as earlier rounds
did.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| lane 3 confirm read (4635bda) MEDIUM-1: "the only figures for this case that PR #19's record supports" and "no figure at measured costs" overstate the record: D5 and task 2.1 give a measured basis by arithmetic, and PR #19's `2e819ad` states the case on three bases | MEDIUM | A-39, as A-40 amends it: applied: D7 states the case where the plan read `extensions.worktreeConfig` as true on D14's three bases at `9267303` (its `design.md:960-965`, the row at `:963`, unchanged from `2e819ad`), for change 1 alone and for this change's flagged run of 16 at 128 rows, each figure naming its basis and the cost of this change's children, which task 2.1 did not measure: on the 150 ms basis change 1 removes 0, the first due at 45.3 s, and the flagged run 0 and 0, the first due at 45.45 s; on the measured basis, D5's, with D14's stand-ins (row 4c's read and the per-row `rev-parse --show-toplevel` at the identity probe's 19.7 ms, LQ-13's `rev-list` at the full ref listing's 359.7 ms), change 1 removes 16, the 16th at 37.9 s, or 15 with 20,000-file removals, and the flagged run 14 and 14 with this change's children at 150 ms, as D7's measured-cost paragraph takes them, its 16th removal moving to about 47.1 s, or 11 and 11 with 20,000-file removals, and 16 and 16 with them at task 2.1's average of about 0.0827 s per child, the 16th at about 43.0 s, or 13 and 12; on the mixed basis change 1 removes 11, 176 children added before the 16th, due at 50.0 s, and the flagged run 7 and 7, its 61 children counted as added since at 150 ms, 237 before the 16th, due at about 59.15 s, the count W35 confirmed; LQ-20's first step stated, (i) measure LQ-11's and LQ-13's two probes or (ii) decide the basis, with (a) to (c) and (d) only if the case still fails, none chosen; "Change 1's measured fit governs" in Risks and the caps sentences in D7 and the readings scoped to a plan that read `extensions.worktreeConfig` as false, A-9 waiting on Brett Heap's LQ-20 for PR #19 where it read it as true; the A-9 restatements in Decisions, the readings and Open Questions state the three bases and cite D7's table; round A10's refinement row corrected in place; every D14 figure reproduced before this change's were derived | `design.md` D7, Risks; Decisions (A-9; readings, the fit); Open Questions (A-9); round A10's table (the refinement row) |
| lane 3 confirm read (4635bda) LOW-1: task 2.3 keeps "a block's added text", the wording round A10 fixed in 3.2 | LOW | A-39: applied in place: "A re-base that changes this change's words beyond those rewordings returns that block to Brett Heap for ratification before the handoff" | `tasks.md` 2.3 |
| lane 3 confirm read (4635bda) LOW-2: D9 has no fixture for a re-read listing that hangs past its own budget or into the work deadline | LOW | A-39: applied: D9's fake `git`s gain "one whose re-read listing hangs past its own budget and, separately, into the work deadline", W35's words in the list's form; no scenario added | `design.md` D9 |
| lane 3 confirm read (4635bda) LOW-3: the sub-record's `state-changed`, "or could not establish one of them", overlaps `deadline-exceeded` for a read the work deadline cuts | LOW | A-39: applied: "or could not establish one of them at its own budget" in the ADDED requirement's `state-changed` reason (`specs/project-clean/spec.md:983`), that phrase alone; no scenario added | project-clean delta (ADDED, the sub-record) |
| lane 3 confirm read (4635bda) LOW-4: LQ-20's option (c) is PR #19's "larger removal floor", which round A10 answered with a work deadline | LOW | A-39 and A-40, on lane openRepoProject-2's answer of 02:29:29Z ("a larger removal floor" was its slip; (c) means a longer work deadline where `extensions.worktreeConfig` is true; this lane's `rulings-2026-10-20.md:1193` at the register's `1e5bdf22f`): applied: D7 quotes round (d)'s own words, "a longer work deadline where `extensions.worktreeConfig` is true, so that later removals can still start, the 5 s removal floor kept" (PR #19's `design.md:1792-1793` at `9267303`), and "a larger removal floor" is gone from D7, Decisions and Open Questions; W35's interim wording is not needed | `design.md` D7; Decisions (A-9); Open Questions (A-9) |
| lane 3 confirm read (4635bda) LOW-5: round A10's follow-on row says "the five other blocks still equal main's at `15504f1`", which reads as the opposite of the clause before it | LOW | A-39: applied in place: "the five blocks whose `c462d87` text is main's still equal main's at `15504f1`" (checked: at `15504f1` the five equal `961c405`'s and `c462d87`'s, and at `9267303` all seven differ from `c462d87`) | round A10's table (the follow-on row) |
| A-39 and A-40, the cites: D7's cites into PR #19 move by W35's map, and then to its round (d), `9267303` | ruling | applied with change: each range mapped by content from `a664799` through `2e819ad` to `9267303`: F at `design.md:331-332` and D14 `:889`; E and D21 `:854-855`; D21 per revalidation `:992-993`; six and seven children at `specs/project-clean/spec.md:1024-1026` and `specs/project-clean-review-safety/spec.md:76-77`; the per-row probe `:437-439`; D14's rows `:897` and `:898`; the planning term `:907-909`; P = 168 at `:918-919`; P = 39 + 2R at `:919-925`; the three bases `:885-888`, `:935-958` and their table `:960-965`; the option table `:967-976` and its notes `:978-990`; the spawn limit `:916-918`; LQ-20 at `:1762-1805` and Risks `:1603-1620`; the Dependency on PR #19 (checked: all seven requirements differ from `c462d87` at `9267303`) and the citation key name `9267303`; the change: round A10's table rows, records of that round, keep their `a664799` cites, the refinement row's correction citing `9267303`, and D4's cite of PR #19's revalidation rule stays at `a664799`, which it names | `design.md` D7, Risks, Context; Dependencies and Sequencing (on PR #19); citation key; Status |
| A-40, the options: a flagged run's result under each option of LQ-20 on each basis, and option (c)'s figure reconciled from round (d)'s inputs | ruling | applied: D7's table, beside D14's for change 1, this change's children at 150 ms on the 150 ms and mixed bases and at 150 ms, or task 2.1's average, on the measured basis: (a) 0 and 0 on every run at 150 ms, 14 and 14, then 15 and 15 and 16 and 15, then 16 and 16 a run measured (16 and 16 a run at the average), and 7 and 7 rising to 16 and 16 a run from 53 rows mixed; (b) 9 and 8, 16 and 15 (16 and 16), and 16 and 16; (c) at least 79.70 s for all 16 removals and more than 80.75 s for all 16 retired at 150 ms, at least 52.08 s and more than 53.13 s measured (none needed at the average), and at least 64.13 s and more than 65.19 s mixed; (d) at change 1's pairs 8 and 8, or 15 and 14, at 150 ms and 8 and 8, or 16 and 15, mixed, and on the measured basis, where change 1 needs no step, still needed with this change's children at 150 ms, 8 and 8 at 128 rows and 8 targets or 16 and 16 at 64 rows and 16 targets, and none at the average; the reconciliation: change 1's 70.55 s plus 61 children at 150 ms, 79.70 s, is the work deadline all 16 removals need, the 16th spawning at 74.70 s, while round A10's 80.75 s is the one all 16 retirements need, the 16th branch child spawning 1.05 s after its removal and needing more than the removal floor left, so the figure stands and both are stated; the A-9 restatements cite the table; no option chosen | `design.md` D7, Risks; Decisions (A-9; readings, the fit); Open Questions (A-9) |
| A-40, the spawn limit: 45 s is "the spawn limit", the 50 s work deadline less the 5 s removal floor, in the text restated and wherever #26 says "floor" meaning 45 s | ruling | applied with change: the term defined in D7 (PR #19's `design.md:916-918` at `9267303`), and "floor" meaning 45 s replaced in `design.md` D7 in five places ("past the floor" for the first removal at 45.45 s, "far inside the floor", "0.05 s inside the floor", "past the floor either way" and "before the floor") and in the proposal in four ("before the removal floor" in Decisions, "on the floor's boundary" in the readings, and "reaches the removal floor early" and "past the floor either way" in Open Questions); the change: one AND of the ADDED scenario "A branch moved to an unmerged commit and back is retained" read "its budget ends at the floor", and now reads "its budget ends when only the removal floor remains", since no spec text defines "the spawn limit"; "the spawn floor" (`design.md` D5 and D7, and the proposal's A-15 reading and the alignment section), which names the rule that a child starts only while more than the removal floor remains, and the Git 2.36 floor and the `git-floor` job, another sense, are kept, and the round tables, records of their rounds, are left | `design.md` D7; project-clean delta (ADDED, one AND); Decisions (A-9); Decisions (readings, the fit); Open Questions (A-9) |
| Codex (4635bda): its review receipt on PR #26 of 2026-10-21T21:55:32Z, "Didn't find any major issues", for reviewed commit `4635bda8b4` | none | no finding and no edit | none |

### Re-read and Codex Findings (round A12)

Lane openRepoProject-3's reader W40 read round A11, `4635bda..7eb0615`
(`confirm-a11-findings.md` at the register's `1cbdc517d`): no HIGH, two
MEDIUM, one LOW and nothing departing. It re-derived every figure of round
A11 by its own child-by-child simulation, after reproducing D14's two tables,
and found A-39's six items and A-40's five applied, every MODIFIED block
carrying its source scenarios, the project-command blob `e7665dda`, validate
8 of 8 and the scenarios 68, 4 and 9. It confirmed both observations of round
A11's writer: its MEDIUM-1, that task 2.1's 23.6 s was still said to govern
where the plan read `extensions.worktreeConfig` as false, which PR #19's D14
supersedes; and its MEDIUM-2, that task 2.1's average per child is about
0.063 s, not 0.0827 s, lane 3's own error from W35. PR #19's round (e) then
landed as `f0bf538`: D14's tables unchanged but shifted, LQ-20's option (c)
stating its invocation deadline and run bound, and its revalidation rule
gaining L-4 and L-5. The lead's ruling A-41, with its addendum and item 3 of
ruling B-60, and its ruling A-42 take W40's three findings and four of its
observations, and do not adopt its fifth. Codex reviewed `7eb0615` and found
no major issue. Of the 10 rows below, 7 are applied, 1 is applied with change
(MEDIUM-1), 1 is not adopted and 1 is a review with no finding. No ruling
needs `specs/project-command/spec.md`, which is unchanged (blob `e7665dda`),
and round A12 edits no spec file, the R-208 check finding the spec delta's
words in agreement, so the scenarios stay 68, 4 and 9 and every MODIFIED block
still carries its source scenarios byte for byte. Every figure at `f0bf538`
was derived two ways, by D7's closed form and by a step simulation, after both
had reproduced D14's figures for change 1, and W40's figures at the withdrawn
0.0827 s were reproduced as a control. Round A11's rows keep their figures and
cites as that round's record. The round also updates `design.md`'s Context
map, the Status clause, the citation key and tasks 1.1, 1.3, 1.4 and 1.5, as
earlier rounds did.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| lane 3 confirm read (7eb0615) MEDIUM-1: `design.md` Risks and the readings' caps account keep task 2.1's 23.6 s as governing where the plan read `extensions.worktreeConfig` as false, under which all 16 fit, which PR #19's D14 supersedes (round A11's writer's observation 1) | MEDIUM | A-42: applied with change: Risks, the readings' caps account, Decisions (A-9) and Open Questions (A-9) state that case on D14's measured basis at `f0bf538` (its `design.md:968`, change 1's 16th removal at 35.1 s, or 42.8 s with 20,000-file removals; its `:1002-1003`, task 2.1's 26.4 s the margin before LQ-11 and LQ-13 added children): a flagged run of 16 removes 16 and retires 15 with this change's children at 150 ms, the 16th removal at 44.26 s and the 16th branch child due at 45.32 s, `retained` with `deadline-exceeded`, exit 1, never unsafe; 15 and 14 with 17 reflog children; 13 and 12 with 20,000-file removals; and, at task 2.1's corrected average, 16 and 16, the 16th branch child at 39.83 s, or 15 and 14 with 20,000-file removals, where W40 gave 16 and 16 at 41.08 s, or 14 and 13, at the withdrawn 0.0827 s; the caps stay; the 23.6 s account is kept, labelled as `c462d87`'s; D7's measured-cost paragraph states its scope to a plan that read the setting as false explicitly, for `c462d87`'s account and for D14's; every other "all 16 fit" at measured costs, the joint fit with the cache change (D7 twice, Risks, Decisions and Open Questions), is labelled `c462d87`'s, and D7 gives that fit on D14's measured basis, by the same bound: 12 removed and 12 retired through a worker, 11 and 10 with 17 reflog children, and at least 9 and 8, or 7 and 7, at a thread per call; the change: W40's "a flagged run of 16 through a worker" is written without "through a worker", since its figures are a run without the cache change, whose one-worker figures are the joint fit's | `design.md` D7, Risks; Decisions (A-9; readings, the fit); Open Questions (A-9) |
| lane 3 confirm read (7eb0615) MEDIUM-2: task 2.1's average per child takes its 15 removals at 0.3 s, where its 23.6 s holds them at 0.604 s (round A11's writer's observation 2; lane 3's own error from W35, which A-39 carried) | MEDIUM | A-42: applied: "task 2.1's average of about 0.063 s per child (23.6 s less its 15 removals at 0.604 s, over its 231 children)", (23.6 - 9.06) / 231 = 0.0629 s, or 14.52 / 231 = 0.0628 s from task 2.1's own children (its `report.md`: "spawn16 = 10.43 + 16 x 0.2552 + 15 x 0.604 = 23.58 s"; PR #19's `design.md:946-947` at `f0bf538`); every bracket restated: where the plan read `extensions.worktreeConfig` as true, on the measured basis, 16 and 16, the 16th removal at 41.77 s and its branch child at 42.65 s, were about 43.0 s and 43.89 s, and 13 and 13 with 20,000-file removals, the 13th branch child at 44.86 s, were 13 and 12; (b) the 16th branch child at 40.46 s, was 41.71 s; (c) none needed, the 16th branch child at 42.65 s, was 43.89 s; (a) and (d) unchanged; no conclusion changes | `design.md` D7, Risks; Decisions (A-9; readings, the fit); Open Questions (A-9) |
| lane 3 confirm read (7eb0615) LOW-1: D7's (d) cells give change 1's two pairs on the 150 ms and mixed bases and the rule's own step for the flagged run on the measured basis | LOW | A-42: applied: each (d) cell gives change 1's pairs and then the rule's step for the flagged run, in PR #19's two ways (its `design.md:984-987`: the target cap in steps of 8 with the row cap as large as it can be, or the row cap first, E = T): on the 150 ms basis 64 rows and 8 targets, change 1's first pair, or, with the row cap first, 16 rows and 16 targets, 16 and 16, the 16th branch child at 42.15 s, since 64 rows give 10 and 10 and 32 rows 15 and 14; on the mixed basis 128 rows and 8 targets, change 1's first pair, or 32 rows and 16 targets, 16 and 16, the 16th branch child at 38.67 s, since 64 rows give 16 and 15; on the measured basis, as before, 128 rows and 8 targets, 8 and 8, or 64 rows and 16 targets, 16 and 16, now with their branch children's times, 30.34 s and 42.13 s | `design.md` D7 |
| A-41 and B-60 item 3: PR #19 cited at its round (e), `f0bf538` | ruling | applied: every cite of PR #19's current text moves from `9267303` to `f0bf538`, each range mapped by content: F at `design.md:332-333` and D14 `:895`; E and D21 `:860-861`; D21 per revalidation `:998-999`; six and seven children at `specs/project-clean/spec.md:1026-1028` and `specs/project-clean-review-safety/spec.md:76-77`; the per-row probe `:438-440`; D14's rows `:903` and `:904`; the planning term `:913-915`; P = 168 at `:924-925`; P = 39 + 2R at `:925-931`; the spawn limit `:922-924`; the three bases `:891-894` and `:941-964`, with `:941-956` and `:957-961`, and their table's rows `:968` and `:969`; the option table `:973-982` and its notes `:984-996`; LQ-20 at `:1768-1817`, its (b) at `:1794-1795` and its (c) at `:1800-1808`, and Risks `:1609-1626`; every input and D14's two tables equal `9267303`'s; the Dependency on PR #19 (checked: all seven requirements differ from `c462d87` at `f0bf538`, only the batch block having moved since `9267303`, and the five whose `c462d87` text is main's still equal main's at `15504f1`), D7's paragraph of heads, Risks, Decisions, the readings, Open Questions, the Status clause and the citation key name `f0bf538`; round tables keep their shas, as records of their rounds | `design.md` D7, Risks, Context; Dependencies and Sequencing (on PR #19); Decisions (A-9; readings, the fit); Open Questions (A-9); citation key; Status |
| A-41's addendum and B-60 item 3: option (c) with its work deadline, invocation deadline and run bound on each basis | ruling | applied: D7 cites change 1's figures at PR #19's `design.md:1800-1808` (at least 70.55 s, 80.55 s and 84.55 s on the 150 ms basis, none needed on the measured basis, and at least 55.0 s, 65.0 s and 69.0 s on the mixed basis) and writes no offset rule; for the flagged run it states each figure, derived in the relation of PR #19's own and cited to that range: on the 150 ms basis a work deadline of at least 79.70 s for all 16 removals, with an invocation deadline of at least 89.70 s and a run bound of at least 93.70 s, and more than 80.75 s, 90.75 s and 94.75 s for all 16 retired; on the measured basis, with this change's children at 150 ms, at least 52.08 s, 62.08 s and 66.08 s, and more than 53.13 s, 63.13 s and 67.13 s, none needed at task 2.1's average; on the mixed basis at least 64.13 s, 74.13 s and 78.13 s, and more than 65.19 s, 75.19 s and 79.19 s; change 1's own three on each basis were reproduced from D14's inputs first (70.55 s, 80.55 s and 84.55 s; 54.98 s, which PR #19 gives as 55.0 s) | `design.md` D7 |
| lane 3 confirm read (7eb0615), its observation that D7's (b) drops PR #19's "and report the other rows' identity as unverified" | note | A-42: applied: D7 quotes (b) in full, "bound the plan-time work-tree probe to the selected targets, at most 16, and report the other rows' identity as unverified" (PR #19's `design.md:1794-1795` at `f0bf538`, as its Risks at `:1621-1623` word it too); no figure changes | `design.md` D7 |
| lane 3 confirm read (7eb0615), its observation that D4's alignment with PR #19's revalidation rule, cited at `a664799`, is not checked against R-208 | note | A-42: applied: D4 cites the rule at `f0bf538` (its `specs/project-clean-review-safety/spec.md:113-135`, R-171 and R-208, with round (e)'s L-4 and L-5; its `design.md:486-497`) and checks the stage's two filesystem reads: the re-read's manifest read follows the rule whole, a failed or timed-out read giving `state-changed`, one the work deadline cuts `deadline-exceeded`, and one that finds no manifest (`ENOENT` or `ENOTDIR`) a decided absence, no difference where the plan had none and `state-changed` where it had one; the re-proof's reflog read takes the decided absence, a missing reflog keeping `reflog-unmerged`, and keeps the re-proof's own split, `reflog-unmerged`, for a read that fails or runs past its own budget, where the rule, for a removal's revalidation, gives `state-changed`, either retaining the branch with exit 2; the stage reads no administrative directory, so L-4 does not reach it, and L-5 changes only a SHALL NOT's case; R-208 went to Brett Heap as PR #19's O-2; no spec word changes, since the spec delta agrees: step 2's value that the manifest read "cannot establish" does not take in a decided absence, and step 3 already names a missing reflog | `design.md` D4; citation key |
| lane 3 confirm read (7eb0615), its observation that the citation key gives lane openRepoProject-2's answer as 02:29:29Z at `rulings-2026-10-20.md:1193` read at `1e5bdf22f`, where that line reads "about 02:3xZ" | note | A-42: applied: the key cites the line at the register's `61f71de88`, where it reads "(02:29:29Z)" (checked: at `1e5bdf22f` it reads "(about 02:3xZ)", and `61f71de88` is on the register's `origin/main`); round A11's prose and its LOW-4 row, which give the same time with `1e5bdf22f`, are left as that round's record, the time being at `61f71de88` | citation key |
| lane 3 confirm read (7eb0615), its observation of an optional third cost, by kind, for this change's children | note | A-42: not adopted: with D14's stand-ins this change's four stage children average about 0.158 s (the re-read listing at the narrowed listing's 101.6 ms, the post-check at the identity probe's 19.7 ms, the re-proof's `rev-list` at the full ref listing's 359.7 ms, and `branch -d`, with no measured match, at 150 ms), close to the 150 ms variant, so no third variant is added | none |
| Codex (7eb0615): its review receipt on PR #26 of 2026-10-22T03:07:56Z, "Didn't find any major issues", for reviewed commit `7eb0615f78` | none | no finding and no edit | none |

### Re-read and Codex Findings (round A13)

Lane openRepoProject-2 answered on 2026-10-22 (08:16:04Z) the question that
the lead put to it on round A12's third judgment call: a failed re-proof
reflog read should be worded `state-changed`, not `reflog-unmerged`. Under
R-208 only a decided value gives its step's own reason, so that a failed read,
which decides nothing, would have `reflog-unmerged` claim unmerged commits
that were never seen, as feature 004's gate 7 leaves such a row unprobed and
never reports it unmerged; this change's D4 cites PR #19's rule at `f0bf538`
(its `specs/project-clean-review-safety/spec.md:113-135`) for a re-proof that
revalidates a destructive action, so that splitting the rule inside one stage
would need a declared departure, and aligning is cheaper; the outcome is
unchanged, retained with exit 2, a report-truth point at LOW; and the
manifest re-read is right as stated. The lead's ruling A-43 takes the answer
and overrules round A12's call on the failed read. Lane openRepoProject-3's
reader W46 read round A12, `7eb0615..a11bde8` (`confirm-a12-findings.md` at
the register's `44c47d893`): no HIGH, no MEDIUM, two LOW and nothing
departing. It upheld the writer's three calls: the joint fit with the cache
change belongs in this change, and re-derives at 12 and 12, 11 and 10, 9 and 8
and 7 and 7; the manifest case needs no spec clause; and a reflog missing at
the re-proof, where the plan proved one merged, is a decided absence that
keeps `reflog-unmerged`, PR #19's `:122-127` and `:133-135` giving a decided
value its step's own reason and the plan never selecting a branch with no
reflog. It re-derived every figure of round A12 and found every MEDIUM-1,
MEDIUM-2, LOW-1 and A-41 (c) figure equal, with the carry check, validate,
the scenarios and the project-command blob unchanged. It left the failed read
ungraded under A-43 and asked that this round say whether the re-proof's
child, which step 3 groups with the read and to which PR #19's `:115-120`
gives `state-changed`, moves too. The lead's ruling A-44 takes its two LOW,
its two observations (the due time, and the rounding, which it keeps) and that
point. Codex reviewed `a11bde8` (2026-10-22T08:17:23Z) and found no major
issue. Of the 7 rows below, 5 are applied, 1 is kept as it stands and 1 is a review with
no finding. No ruling needs `specs/project-command/spec.md`, which is
unchanged (blob `e7665dda`). Round A13 edits the project-clean delta, step 3
of the ADDED requirement, its `state-changed` and `reflog-unmerged` reasons,
its result line and one AND of one ADDED scenario, and one sentence of the
review-safety delta, and adds no scenario, so the scenarios stay 68, 4 and 9
and every MODIFIED block still carries its source scenarios byte for byte.
Every figure was derived two ways, by round A12's closed form and its step
simulation, each extended for this round and agreeing. Rounds A4, A5, A10 and
A12's rows, which give the re-proof's failed read or child `reflog-unmerged`,
keep their words as those rounds' record; row 1 below supersedes them. The
round also updates `design.md`'s Context map, the Status clause, the citation
key and tasks 1.1, 1.3, 1.4 and 1.5, as earlier rounds did.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| lane openRepoProject-2's answer on R-208 for this change (08:16:04Z): the re-proof's reflog read that fails or runs past its own budget keeps the step's own reason, `reflog-unmerged`, where PR #19's rule for revalidation (its `specs/project-clean-review-safety/spec.md:113-135`, R-171 and R-208) gives `state-changed` to a call that decides nothing; round A12's judgment call 3 kept it | LOW (a report-truth point; the outcome is unchanged, retained with exit 2) | A-43: applied: step 3 of the ADDED requirement gives a re-proof whose read fails or runs past its own 5 s budget while the work deadline is not the limit `state-changed`, and one whose budget the work deadline ends `deadline-exceeded`, as before; the stage's `state-changed` reason takes in the re-proof's failed read; D4 states the reading, that a read that fails decides nothing and `reflog-unmerged` would say that a commit was seen, with the plan's own failed proof staying a `reflog-unmerged` keep (the plan's reasons are its keep list's four and a keep never stops the run); the missing-reflog case is settled by W46's section 1 (iii): a reflog missing at the re-proof (`ENOENT` or `ENOTDIR`) is a decided absence and keeps `reflog-unmerged`, as do one found empty, one read to its 64 KiB bound and one that the gate's reading cannot decide, each a value the read decided, as PR #19 gives its own `worktree-only-commits` to a `logs/HEAD` read to that bound or holding a line that cannot be parsed (its `:110-111`) | project-clean delta (ADDED: step 3, the reasons); `design.md` D4, D5; What Changes; Decisions |
| lane 3 confirm read (a11bde8), section 1 (iii) and its note for A13: the re-proof's child, which step 3 groups with the read, fails or times out at its own 5 s budget, and PR #19's `:115-120` gives such a call `state-changed`; the places that A-43 moves together | LOW | A-44 item 1: applied: the child gives `state-changed` as the read does, and one that the work deadline cuts `deadline-exceeded`; the places moved together: step 3, whose failed read and child and ground "the reason a failed proof gives in the plan" are replaced; the stage's `state-changed` reason; `reflog-unmerged`'s "or could not prove the reflog", narrowed to the values the proof decided; the result line, worded for a proof that printed a commit, the plan's proof that failed and a re-proof that found the reflog missing, empty, at its bound or undecidable, so that it stays true for the plan's own failed proof; `design.md` D4 (check 6, the paragraph that splits the outcomes, the re-proof's split and the two filesystem reads); and, by the same ground, the review-safety delta's one sentence on a reflog its re-proof "does not prove", D5's stage table, D7's table row for the re-proof, D8's `Kept` line and Risks' restatement; the one scenario that pins it, "A branch moved to an unmerged commit and back is retained", its AND with only the re-proof made to exit nonzero or hang past its 5 s budget, gave `reflog-unmerged` and `Kept <branch> (reflog-unmerged)` and now gives `state-changed` and `Kept <branch> (state-changed); retry: project clean <root> --apply --action delete-branch --branch <branch>`, exit 2 as before; the ANDs of the plan's failed reflog child and of a reflog that names a commit the merge target lacks stay; no scenario added, the counts 68, 4 and 9 | project-clean delta (ADDED: step 3, the reasons, the result line, the scenario's AND); review-safety delta (narrow guarantee); `design.md` D4, D5, D7, D8, Risks; What Changes; Decisions |
| lane 3 confirm read (a11bde8) LOW-1: `design.md` D4's sentence that a manifest the plan read and the re-read finds absent is a manifest difference is wider than step 2, which compares only the manifest's `tracking_branch` and the merge target re-resolved from it | LOW | A-44 item 2: applied in W46's wording: "one that the plan read with a `tracking_branch` and the re-read finds absent is a `tracking_branch` difference, `state-changed`", and one that the plan read with no `tracking_branch` and the re-read finds absent gives no difference; no spec word changes | `design.md` D4 |
| lane 3 confirm read (a11bde8) LOW-2: D7's joint fit with the cache change gives only the 16 enumerations at 2.4 s, so that "at least 9 and 8", and Risks' "at least 8", hold only there; at the cache change's own 3.7 s for them (its D4 at `e1049b2`) the pairs fall | LOW | A-44 item 3: applied: each place gives both costs, named: the enumerations at 2.4 s, 6.4 s through a worker and 13.3 s at a thread per call before the first removal, 12 removed and 12 retired through a worker (the 13th removal due at 45.20 s), 11 and 10 with 17 reflog children, and at least 9 and 8, or 7 and 7, at a thread per call; and at 3.7 s, 7.7 s and 14.6 s, 12 and 11 through a worker (the 12th removal at 44.68 s, the 12th branch child due at 45.74 s), 10 and 10 with 17 reflog children, and at least 8 and 7, or 7 and 6, at a thread per call; re-derived by round A12's closed form and step simulation extended for this round, with a check that the worst order a run can take gives the same four pairs at each cost; Risks' "at least 8" and the proposal's "at least 8" are scoped to 2.4 s, with 11 and at least 7 at 3.7 s | `design.md` D7, Risks; Decisions (A-9; readings, the fit); Open Questions (A-9) |
| lane 3 confirm read (a11bde8), its observation that "the 16th branch child, due at 45.32 s, cannot start": the stage's re-read is refused first, at 45.02 s | note | A-44 item 4: applied: where 45.32 s is cited for the 16th branch child, in D7, Risks, Decisions (A-9; readings, the fit) and Open Questions (A-9), "its re-read refused first at 45.02 s" is added: the 16th removal at 44.26 s, its removal's 0.604 s and its rescan's three children's 0.155 s put the re-read's due time at 45.02 s, past the 45 s before which it may start, so that the outcome, `retained` with `deadline-exceeded`, exit 1, is unchanged; both figures reproduced by the closed form and the step simulation; the other due times keep W40's convention of ungated due times, as W46 notes | `design.md` D7, Risks; Decisions (A-9; readings, the fit); Open Questions (A-9) |
| lane 3 confirm read (a11bde8), its observation that 41.77 s and 42.65 s follow from 23.6 s, and that task 2.1's exact 23.578 s gives 41.76 s and 42.64 s | note | A-44: kept: 41.77 s and 42.65 s stand, from the stated 23.6 s, "about 0.063 s" either way; no edit | none |
| Codex (a11bde8): its review receipt on PR #26 of 2026-10-22T08:17:23Z, which found no major issues, for reviewed commit `a11bde8` | none | no finding and no edit | none |

### Re-read and Codex Findings (round A14)

Codex reviewed `1bf217c` (2026-10-22T08:45:31Z) and raised one P2, an inline
thread on the project-clean delta at the `branch-in-use` next step (its spec
:1094), "Tell main-worktree holders to switch branches": when PATH2, the holder
of a `branch-in-use` branch, is the main worktree, the next step "remove that
worktree first" cannot work, since `git worktree remove` of a main worktree
exits 128, "is a main working tree". The lead verified it on Git 2.43.0 in a
scratch repository, from the main worktree and from a linked one, found that
the ADDED requirement's `branch-in-use` includes the main worktree and that its
scenario covers that case with the same advice, and found that the
`git-refused` hint, "wait for it to end and remove that worktree", has the same
flaw when the worktree that holds the branch in a rebase or a bisect is the
main one (ruling A-45, `rulings-2026-10-20.md:1523` and `:1531` at the
register's `573fbc11a`). Lane openRepoProject-3's reader W47 read round A13,
`a11bde8..1bf217c` (`confirm-a13-findings.md` at the register's `d4008061c`):
no HIGH, no MEDIUM, four LOW and nothing departing. It found (a) that the
scenario's retry hint is this change's existing `otherwise ; retry: RETRY`,
(b) that the review-safety sentence lacks "while the work deadline is not the
limit" (LOW-1), and (c) no departure from gate 7, the plan's reflog read being
gate 7's own and "the plan's own failed proof" meaning the `rev-list` child
alone, with LOW-2 (the spec should say so), LOW-3 (a failed re-proof's line
says `retry: RETRY`, with no advice to inspect the reflog) and LOW-4 (the
record sentence omits A5's row); it re-derived the 3.7 s pairs, 45.02 s and
45.74 s, validate, the carry check, the counts and the project-command blob.
W47 had finished before A-45 reached it and was not asked about the
main-worktree case. The lead's ruling A-46 applies A-45 and W47's LOW-1, LOW-2
and LOW-4, and keeps LOW-3. Of the 6 rows below, 4 are applied, 1 is kept as it
stands and 1 is upheld with no change. No ruling needs
`specs/project-command/spec.md`, which is unchanged (blob `e7665dda`). Round
A14 edits the project-clean delta, step 1 of the ADDED requirement, its `Kept`
next steps, one AND of one ADDED scenario, split in two, and the literals of
three more ADDED scenarios' ANDs, and one sentence of the review-safety delta,
and adds no scenario, so the scenarios stay 68, 4 and 9 and every MODIFIED
block still carries its source scenarios byte for byte. The Git facts were
re-run on Git 2.43.0 and on the 2.36.6 floor, in scratch repositories
(`design.md` Context). Rounds A7's and A8's rows, which give the `git-refused`
hint as "wait for it to end and remove that worktree", keep their words as
those rounds' record; row 1 below supersedes them. The round also updates
`design.md`'s Context map, the Status clause, the citation key and tasks 1.1,
1.3, 1.4 and 1.5, as earlier rounds did.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Codex (1bf217c), P2, an inline thread at the project-clean delta's `branch-in-use` next step (its spec :1094), "Tell main-worktree holders to switch branches" (2026-10-22T08:45:31Z): when PATH2, the holder of a `branch-in-use` branch, is the main worktree, "remove that worktree first" cannot work, since Git refuses to remove a main working tree | P2 | A-45: applied (the lead verified it VALID): wherever a next step told the person to remove the worktree that holds BRANCH and the holder can be the main worktree, the main worktree's next step now says to switch it off BRANCH, by checking out another branch there, such as MERGE_TARGET, or by detaching it, and then retry; the places moved together: the `branch-in-use` line, `; next: BRANCH is checked out at PATH2; remove that worktree first`, now followed by "or, when PATH2 is the main worktree, which Git refuses to remove, `; next: BRANCH is checked out at PATH2, the main worktree; switch it off BRANCH, by checking out another branch there, such as MERGE_TARGET, or by detaching it, then: RETRY`"; the `git-refused` hint, in both its forms (the upstream ref present and absent), now `wait for it to end and remove that worktree, or, for the main worktree, which Git refuses to remove, switch it off BRANCH, by checking out another branch there, such as MERGE_TARGET, or by detaching it`, carrying both forms because the registry listing shows a worktree mid-rebase or mid-bisect detached, with no `branch` line, so that the line cannot say whether the holder is linked or the main worktree; `branch-shared` checked, and unchanged in its step: its holder PATH2 is a selected row, change 1's first gate, `main-worktree` (`CAS/pc:576-578`), never selects the main worktree, and a branch also held by the main worktree is kept `branch-in-use` before `branch-shared` is reached, so its next step stays the linked form, and its sentence says so ("a selected row and so never the main worktree, the first of those next steps"); the scenario "A branch another worktree holds is retained", whose AND "when a dirty linked worktree, or the main worktree, also has the branch checked out" is split into two ANDs, "when a dirty linked worktree also has the branch checked out", with the linked next step unchanged, and "when instead the main worktree also has the branch checked out", with the new one, every other clause of the AND kept byte for byte (checked clause by clause against the AND at `1bf217c`), no scenario added; the `git-refused` literals of three scenarios' ANDs ("Git refuses the branch deletion", twice, and "A branch name in a printed command is quoted for the shell") carry the new hint; the wording follows the spec's `head-not-merge-target` lines, which already speak of the main worktree, and names a detach because a checkout of MERGE_TARGET is refused while a linked worktree holds it; re-run on Git 2.43.0 and on 2.36.6: `git worktree remove <main>`, with and without `--force`, run from the main worktree or from a linked one, exits 128, "is a main working tree"; `branch -d b` run in the main worktree is refused while it holds `b`, mid-rebase, mid-bisect, or once either ends, and deletes `b`, exit 0, after the main worktree checks out another branch or detaches | project-clean delta (ADDED: the `Kept` next steps; "A branch another worktree holds is retained"; "Git refuses the branch deletion"; "A branch name in a printed command is quoted for the shell"); `design.md` Context, D8, Risks; What Changes; Decisions |
| lane 3 confirm read (1bf217c), LOW-1 (its check (b)): the review-safety sentence "a re-proof whose read or child fails or runs past its own budget SHALL retain it with `state-changed`, each stopping the run with exit 2" lacks "while the work deadline is not the limit", which step 3 (`specs/project-clean/spec.md:918-923` at `1bf217c`), the bounds block (`:526-529`) and PR #19's `specs/project-clean-review-safety/spec.md:119` carry, so that read alone it takes in a deadline-shortened budget, which gives `deadline-exceeded` and exit 1 | LOW | A-46: applied: "a re-proof whose read or child fails or runs past its own budget while the work deadline is not the limit SHALL retain it with `state-changed`", as PR #19's rule words it; wording only, and the MODIFIED block's three source scenarios still carry byte for byte | review-safety delta (narrow guarantee) |
| lane 3 confirm read (1bf217c), LOW-2: the spec never says that the plan's proof reuses the gate's read; only `design.md` D4 does, so that a reader of step 1 and of "whose proof fails or times out" alone could ask whether a failed plan-time read is a failed proof | LOW | A-46: applied: step 1 of the ADDED requirement says that the plan SHALL NOT repeat the `unstarted-branch` gate's reflog read, that a read that fails or does not finish is that gate's own outcome (a row excluded as `reflog-unavailable` or `inspection-error`, or left unprobed with the plan incomplete, as the gate's rule at `:334-340` says, and as feature 004's `reflog_gate` does, on W47's reading), that no row reaches the keep without a read the gate finished, and that the plan's own failed proof is its `rev-list` child alone; `design.md` D4 already says it and is unchanged | project-clean delta (ADDED: step 1); Decisions |
| lane 3 confirm read (1bf217c), LOW-3: a failed re-proof's line, `Kept BRANCH (state-changed); retry: RETRY`, no longer says to inspect the reflog, and `delete-branch`'s own check is by tip and merged set, not by reflog, so that the retry can delete a branch whose reflog still names a commit the merge target lacks; declared at `design.md` D4 | LOW | A-46: kept as it stands: a failed re-proof's line keeps `retry: RETRY`, like this change's other `state-changed` lines, since a read that decides nothing has nothing to inspect, so the next step is to retry; if lane openRepoProject-2 objects later, a later round changes it | none |
| lane 3 confirm read (1bf217c), LOW-4: the record sentence of round A13's section, "Rounds A4, A10 and A12's rows ... keep their words as those rounds' record", omits round A5's row, whose A-26 item 1 says "the failing re-proof's AND pins that line", the `reflog-unmerged` line of the AND that round A13 changed | LOW | A-46: applied: the sentence reads "Rounds A4, A5, A10 and A12's rows"; A5's row keeps its words as that round's record | round A13's section (its record sentence) |
| lane 3 confirm read (1bf217c), checks (a) and (c): (a) the changed AND's retry hint matches this change's existing next step for `state-changed`, the `otherwise ; retry: RETRY` arm (`specs/project-clean/spec.md:1105-1108` at `1bf217c`; `design.md` D8's last `Kept` bullet); (c) lane openRepoProject-2's wording check, whether "the plan's own failed proof stays a `reflog-unmerged` keep" takes in a plan-time reflog read that fails: it does not, the plan's read is gate 7's own (`:334-340`) and the proof that fails is the `rev-list` child alone | check | A-46: upheld, no change: (a) and (c) both hold; (c)'s one wording gap is LOW-2, row 3 | none |
