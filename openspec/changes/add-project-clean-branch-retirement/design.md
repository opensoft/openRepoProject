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
and D2 answers it. Round A3 maps: A-21 (lane openRepoProject-3's re-read of
`ca96701`) to D2, D4, D7, D8, D9, D10 and the Migration Plan; A-22 (Codex's
findings on `785a45e`) to D8 and Rollback; A-23 (the residual-window line and
the joint fit with the cache change) to D7 and D8 (proposal, "Re-read and
Codex Findings (round A3)"). Round A4 maps A-24 (Codex's finding on
`abad010`: the reflog proved again before the branch child) to D2, D3, D4,
D5, D6, D7, D9 and Risks (proposal, "Re-read and Codex Findings (round A4)").
Round A5 maps A-25 (the cache change's worst shapes at `e1049b2`) to D7; A-26
(lane openRepoProject-3's delta read of `9ff8202`) to Context, D4, D7, D8, D9
and Risks; A-27 (the `update-ref` restore for a branch named `HEAD`) to
Context, D8, D9 and Risks; and A-28 as amended (the `$'...'` note) to Context,
D8, D9 and the Migration Plan (proposal, "Re-read and Codex Findings (round
A5)"). Round A6 maps A-29 (lane openRepoProject-3's folded read of `9b67e8c`,
four LOW wording items) to D8, which gains the one clause that has the note
follow change 1's command form as ratified (proposal, "Re-read and Codex
Findings (round A6)"). Round A7 maps the lane's review wave of 2026-10-21:
A-30 (the digest's `retire` member) to D10 and the Migration Plan; A-31 (an
exception in the stage, and a deletion the post-check could not confirm) to
D5, D6 and D8; A-32 (five LOW items) to D4, D8, D9 and Risks; A-33 (how the
re-bases are checked, and the rewordings they need) to D8, D10 and the
Migration Plan; and A-34 (signals in the apply phase, and the flagged result's
order) to D4, D5, D7, D8 and D9 (proposal, "Re-read and Codex Findings (round
A7)"). Round A8 maps A-35 (lane openRepoProject-3's confirm read of round A7,
its F1 to F10) to Context and D8 (F4), D7 (F3), D8 (F10) and the Migration
Plan (F9) (proposal, "Re-read and Codex Findings (round A8)"). Round A9 maps
A-37 (the lane's reader RF's final composition read: its M2, L1, L2 and L3,
and this change's share of its M1) to D7 and Risks (M2) and the Migration
Plan (M1, L1 and L2); A-36's LOW-2 edits the spec delta alone (proposal,
"Re-read and Codex Findings (round A9)"). Round A10 maps A-38 (lane
openRepoProject-3's confirm read of round A9, its LOW-2 to LOW-5, and PR
#19's round (b) at `a664799`) to D4 (the re-read aligned with PR #19's
revalidation rule) and to D7 and Risks (the fit at `a664799` and PR #19's
LQ-20; LOW-2 and LOW-3) (proposal, "Re-read and Codex Findings (round
A10)"). Round A11 maps A-39 (lane openRepoProject-3's confirm read of round
A10, its MEDIUM-1 and LOW-1 to LOW-5), as ruling A-40 amends it for PR #19's
round (d) at `9267303`, to D7 and Risks (the case where the plan read
`extensions.worktreeConfig` as true on the three bases of PR #19's D14, a
flagged run under each option of its LQ-20 on each basis, LQ-20's first step
and its option (c), and 45 s named the spawn limit; MEDIUM-1, LOW-4 and
A-40) and to D9 (LOW-2); its LOW-3 edits the spec delta alone, and its LOW-1
and LOW-5 `tasks.md` and the proposal (proposal, "Re-read and Codex Findings
(round A11)"). Round A12 maps A-42 (lane openRepoProject-3's confirm read of
round A11, its MEDIUM-1, MEDIUM-2 and LOW-1 and its observations), with
A-41 and B-60 for PR #19's round (e) at `f0bf538`, to D4 (the stage's
filesystem reads under PR #19's revalidation rule, R-208) and to D7 and
Risks (the case where the plan read `extensions.worktreeConfig` as false on
D14's measured basis, task 2.1's average per child corrected, the (d) cells,
and option (c)'s work deadline, invocation deadline and run bound) (proposal,
"Re-read and Codex Findings (round A12)"). Round A13 maps A-43 (lane
openRepoProject-2's answer on R-208 for this change) and A-44 (lane
openRepoProject-3's confirm read of round A12, `a11bde8`, its LOW-1 and LOW-2
and its observations) to D4 (the re-proof's failed read and failed child, and
the manifest sentence), D5 (the sub-record's reasons), D7 (the re-proof's row,
the joint fit at the cache change's own 3.7 s, and the stage's re-read gate at
45.02 s), D8 (the `Kept` line) and Risks (proposal, "Re-read and Codex
Findings (round A13)"). Round A14 maps A-45 (Codex's P2 on `1bf217c`: a holder
that is the main worktree, which Git refuses to remove) and A-46 (lane
openRepoProject-3's confirm read of round A13, `a11bde8..1bf217c`, its LOW-1,
LOW-2 and LOW-4, with LOW-3 kept) to the Context table (a row for
`git worktree remove` of a main worktree), D8 (the `branch-in-use`,
`branch-shared` and `git-refused` next steps) and Risks; LOW-1 edits the
review-safety delta, LOW-2 the spec's step 1, which D4 already states, and
LOW-4 the proposal (proposal, "Re-read and Codex Findings (round A14)").
Round A15 maps A-48 (reader RI's RI-5, RI-7 and RI-9, and the RE-6 record),
A-49 (Codex's P2 on `7b224c7`: the line of a failed re-proof names an
inspection of the reflog before the retry, superseding A-46's keeping of W47's
LOW-3), A-50 (the restatements of PR #19's moving facts worded relatively: RI-2
and M2, RI-1 and M3, RI-8, L1 and L3), A-51 (lane openRepoProject-3's W54
confirm read of round A14, its LOW-1 to LOW-3) and A-52 (lane
openRepoProject-3's W52, F-4: the retry of a name that begins with `-`, which
feature 004's `delete-branch` still runs with no `--`) to D3 (the branch
child's environment), D4 (the re-proof's next step, the RE-6 closure), D5 and
D7 (the realization notes, the counts, the fit sentence's quote), D6 (the stop
rule's two sites), D8 (the `Kept` lines, the residual-window line, the retry of
a name that begins with `-`), the Context table (a row for a rebase stopped in
the main worktree) and Risks; the spec deltas edit the bounds block's start
test, step 4 of the ADDED requirement, its `state-changed` definition and
`Kept` next steps, the literals in four ADDED scenarios' ANDs, one AND added to
"The merge target moves before the branch stage", and the review-safety
scenario's last AND (proposal, "Re-read and Codex Findings (round A15)").
Round A16 maps A-53 (any line that keeps a branch with its reflog unproven
names the reflog inspection, `deadline-exceeded` from the re-proof included)
and A-55 (lane openRepoProject-3's W60 confirm read of round A15, its
MEDIUM-1: every line whose next step is RETRY for a branch the stage did not
re-prove names it) to D4, D7, D8, D9 and Risks; A-47 (PR #19's LQ-20
resolved by measurement at its round (f), `662be89`, and this change's
restatements of option (c) withdrawn, reader RH's item 6) to D4, D7 and
Risks, every cite of PR #19's design moving to `662be89` and its spec cites
staying at `f0bf538`, and names PR #19's head at that round, `6bf9f77`, after
its rounds (g) to (g3), where a place states it, every cite at `662be89` and
at `f0bf538` holding there by content (D7); and A-54 (lane openRepoProject-3's
W53 departure ledger) and A-56 (W60's four LOW) to the proposal and the spec
deltas; the spec deltas edit the ADDED requirement's `Kept` next steps, four
ANDs of four ADDED scenarios, one of them added, the bounds block's
strict-test sentence and the review-safety scenario's last AND (proposal,
"Re-read and Codex Findings (round A16)"; round A17 corrects the count, which
read five, under ruling A-61). Round A17 maps A-60 (lane openRepoProject-3's
W69, LOW-3: the own steps that end in RETRY for a branch the stage did not
re-prove, `head-not-merge-target`, `branch-in-use` with the main worktree as
holder and `branch-changed`, name the reflog inspection too) to D4, D8 and
Risks; A-59 (PR #19's round (h) at `b3228bb`: step 1 of the ADDED requirement
worded relatively to the gate's rule, which (h) changes for a read the
deadline cuts, A-50's note and the currency) and A-62 (D14's new line-feed
case) to D4 and D7; and A-61 (W69's other LOW) to this map, the proposal and
the tasks; the spec delta edits the ADDED requirement's `Kept` next steps and
its step 1 and the literals of four ADDED scenarios, and adds no scenario
(proposal, "Re-read and Codex Findings (round A17)"). Round A18 maps A-63
(lane openRepoProject-3's W78 read of round A17, four LOW: the plan-keep lines
name BRANCH's reflog and say that only this run's plan proved it, the keep
order's account names the inspection, and the line-feed case's 13 retired
rests on D14's rounding) to D4, D7 and D8, and A-64 (PR #19's round (i),
`e0c91bb`, its head then, with A-50's note) to D4 and D7; the spec delta
edits the ADDED requirement's `Kept` next steps and the literals of two ADDED
scenarios, three in all (proposal, "Re-read and Codex Findings (round A18)";
round A19 corrects the count, which read three scenarios, under ruling A-69).
Round A19 maps A-66 (Brett Heap's confirmation of lane openRepoProject-2's
R-284, R-290) to D7; A-67 (PR #19's round (j), `e14ada0`, with A-50's note)
and A-71 (its round (k), `173d83c`, its head then, with A-50's note) to D4,
D7 and Risks; A-68 (lane openRepoProject-3's W84 on the lines for a branch the
stage did not re-prove, which say that only this run's plan proved its reflog)
to D4 and D8; and A-69 (W84's three LOW) to this map and D7; the spec delta
edits the ADDED requirement's `Kept` next steps and the literals of four ADDED
scenarios, five in all (six and seven since round A21 adds two, under ruling
A-80), and adds no scenario (proposal, "Re-read and Codex Findings (round
A19)"). Round A20 maps A-74 (lane openRepoProject-3's W89 read of round A19, two
LOW) to D4 and D7, and A-75 and A-76 (PR #19's round (l), `ccc52b9`, its head
then, with A-50's note) to D4, D7 and Risks; no spec delta changes (proposal,
"Re-read and Codex Findings (round A20)"). Round A21 maps A-79 (lane
openRepoProject-3's W94 read of round A20, two LOW, and its notes) to D4, A-80
(W94's LOW-2) to this map, A-77 (Brett Heap's confirmation of lane
openRepoProject-2's R-307 and R-310) to D7, and A-78 (PR #19's round (m),
`20084cd`, its head then, with A-50's note, and Brett Heap's confirmation of T1
to T8) to D4, D7 and Risks; the spec delta adds an AND to each of two ADDED
scenarios, "A signal around the branch child" and "A removal past the hard
ceiling under the flag", which print the `Kept` literals for `interrupted`
before the re-proof and for `removal-ceiling`, so that rounds A19 and A21 have
edited seven literals in six ADDED scenarios, those of `state-changed`,
`deadline-exceeded`, `interrupted`, `internal-error` and `removal-ceiling`
(round A22 words this count as edits, not a total, under ruling A-82), and adds
no scenario (proposal, "Re-read and Codex Findings (round A21)"). Round A22 maps
A-82 (lane openRepoProject-3's W98 read of round A21, two LOW) to this map, and
A-83 and A-84 (Brett Heap's "R-324: yes" and PR #19's round (n), `2250830`, its
head then, with A-50's note) to D4, D7 and Risks; no spec delta changes
(proposal, "Re-read and Codex Findings (round A22)"). Round A23 maps A-86
(PR #19's round (o), `88d0d36`, its current head, whose spec text is
`2250830`'s, with A-50's note) to D4, D7 and Risks, and A-87 and A-88 (lane
openRepoProject-3's W104 read of round A22, two LOW in the proposal, and its
verdict) to no section here; no spec delta changes (proposal, "Re-read and Codex
Findings (round A23)"). Round A24 maps A-98 as A-100 splits it (the lane's
reader RA2 of the review wave of 2026-10-23: its HIGH L3, the holder advice,
which re-opens A-45 and A-60, its MEDIUM L1 and L2 and its LOW L4 to L7, N1 and
N2), with the reader RD's L1, lane openRepoProject-3's W120 L-2 and the reader
RE's RE23-2, RE23-4, RE2-2 and RE-4, to the Context table
(round A24's rows) and its account of feature 004, D3 (the branch kind), D4
(the lines' account), D5 (`post_check_sha`), D7 (RE-4 at `f3724fc`, N2), D8
(the holder, `reflog-unmerged`, `git-refused`, moved, `Unconfirmed` and summary
lines, F-4 closed), D9, Risks and the Migration Plan (RD's L1, RE2-2); the spec
deltas edit the ADDED requirement's `branch_retirement` fields, its summary,
`Unconfirmed` and `Kept` lines and the literals of nine ADDED scenarios, add
four ADDED scenarios, and edit the review-safety scenario's THEN and add an AND
to it (proposal, "Re-read and Codex Findings (round A24)"); PR #19's round
(p), its F-1 (b) and the other items that wait on it or on Brett Heap's Q8 are
round A25's (ruling A-100), the (b) text not fitting the holder whose path
could not be read, which keeps R-324's clause (ruling A-101; D8); A-91's record
lines, lane openRepoProject-3's W109 LOW-1 and LOW-2 on round A23's table, map
to the proposal's table alone. Its ruling A-103, on the writer's five
decisions, maps to D8 (the main-worktree holder line, which names the detach or
a checkout of MERGE_TARGET there, one text whatever the upstream's state,
narrowing A-45)
and Risks (the checkout's residual); the spec deltas edit that line's template
and the two literals of the scenario that carries it, adding no scenario.
Round A25 maps A-106 (PR #19's rounds (p), `e0b1671`, and (q), `818311a`, its
current head, accepted under lane openRepoProject-2's R-389, which builds Brett
Heap's "yes, recommended for Q1-Q9", R-380) to the Context table (round A25's
row), D4 and D7 (the currency, every cite of PR #19 checked by content at
`818311a`), D8 (the `Retired` line's form for `HEAD`, defensive under Q8's
warned-probe rule, RE2-1; the unreadable holder's clause under Q3 (a) and
A-103 (3)'s live-holder test; N1's residual under Q8; F-4's D18 cite), D9 and
the Migration Plan (what the archive-time re-base takes, A-50's note being in
the proposal); the spec delta edits the `Retired` line's sentence and one AND
of the quoting scenario, adding no scenario (proposal, "Re-read and Codex
Findings (round A25)").
Round A26 maps A-110 (PR #19's round (r), `4512441`, its current head,
accepted under lane openRepoProject-2's R-396, and lane openRepoProject-3's
W131 read of rounds A24 and A25, with W133's Q9 (c) note, under A-108 and
A-109) to the Context table (round A24's row of a stopped merge, widened to
the four stopped operations, and round A26's rows: the checkout of
MERGE_TARGET and ignored files, and `core.warnAmbiguousRefs`), D1 (a flagged
apply without `--yes` on a standard input that is not a terminal, Q9 (c)),
D4 and D7 (the currency, every cite of PR #19 checked by content at
`4512441`, and "169 or 180 lines later" scoped to D14, W131's LOW-4), D8
(the `Retired` line's form for `HEAD` under each setting, W131's LOW-3), D9
(a test with the setting false), Risks (the checkout's residual widened,
W131's MEDIUM-1) and the Migration Plan (what the archive-time re-base takes
at `4512441`); the spec delta edits the `Retired` line's sentence and one AND
of the quoting scenario for LOW-3, and adds a sentence to the ADDED
requirement and an AND to "A single target with the flag equals a one-item
batch" for Q9 (c), adding no scenario (proposal, "Re-read and Codex Findings
(round A26)").
Round A27 maps A-119, with A-111 to A-118 (PR #19's rounds (s), `dab8a64`,
and (t), `54e869b`, its current head, accepted under lane
openRepoProject-2's R-412 and R-415, round (t) building Brett Heap's "yes,
recommended for M1 and M3", R-413; and lane openRepoProject-3's W138 read of
round A26 and W146 read of round (s), under A-112, A-115 and A-117) to the
Context table (round A27's row: a checkout of another branch and a holder's
ignored files), D1 (Q9 (c)'s sentence, which rounds (s) and (t) do not
restate, W138's OBS-4), D4 and D7 (the currency, every cite of PR #19
checked by content at `54e869b`, what rounds (s) and (t) changed, and M1 and
M3 named as ruled), D4 and D8 (the holder lines' three reasons for naming no
other branch, which now give the whole residual that Risks holds, W138's
OBS-1), D8, Risks and the Migration Plan (the currency, and T9's lines,
which M1 (a) keeps); the spec delta edits the main-worktree holder line's
reason clause for OBS-1, adding no scenario (proposal, "Re-read and Codex
Findings (round A27)").
Round A28 maps A-126 (the lane's reader RJ's seven findings on `a6f6616`, F1 to
F7, and lane openRepoProject-3's W153 observations 1 and 2, under A-122), A-127
(Brett Heap's answers on his ledger word) and A-128 (the reader RN's RN-1 and
RN-2 on feature 004 at `904aefc`, RN-1 superseding F2 at the spec's sites) to
the Context table (round A28's rows: the clean last holder's later commit, a
branch named `HEAD` and the borrowed upstream, feature 004's row for a worktree
on `refs/heads/HEAD`, the listing a next target compares, a holder whose path
is missing and a holder whose registration names another worktree's path), D1
(the order of a flagged apply's refusals, RN-2), D3 (a branch named `HEAD`
never reaching Git's merge test, F2 under RN-1, and the primitive ruled), D4
and D8 (the holder lines: the flagged single-target command for the clean last
holder, F1, narrowing A-98; a missing holder's form, F5; M3 (a)'s step, F7), D7
(R-406 named as lane openRepoProject-2's, W153's observation 2, and A-9 ruled),
D8 (the `Retired` line for `HEAD`, only defensive under either setting, RN-1,
narrowing A-106 and A-110; the note's two outcomes, F3), D9, D10 (the enum
question ruled), Risks (the holders, the checkout residual of any branch,
W153's observation 1, the note's outcomes, F3, the facts checked on 2.43 only,
F6, and the primitive and the cap ruled), the Migration Plan and the Open
Questions (the four questions that A-127 rules); the spec delta edits a flagged
apply's refusal sentence, the `Retired` line's sentence, the holder lines and
four ADDED scenarios, adding ANDs and no scenario (proposal, "Re-read and Codex
Findings (round A28)").
Round A29 maps A-131 and A-132 (lane openRepoProject-3's W160, OBS-9, on
main's move to `b42355e`; the reader RN's RN-3, which re-pins the cites of
feature 004 at `f3724fc` to `904aefc`; A-129's calls (2) and (4); and lane
openRepoProject-3's W166 confirm read of round A28, its LOW-1 and OBS-1 to
OBS-4), with A-133, and A-134 (lane openRepoProject-3's W169 read of PR #19's
round (u) at `1476110`) to the Context table (round A29's row: the ref listing
run in the worktree on `refs/heads/HEAD`), the citation key (main at
`b42355e`), the Context's account of feature 004 (`GIT_KINDS` at `904aefc`),
D3 and D8 (the upstream the listing gives a branch named `HEAD`, OBS-1; F-4
and `RelayParser` at `904aefc`), D4 and D7 (the sentences that named
`54e869b` as PR #19's head dated, its D14 and task 2.1 unchanged at
`1476110`), D7 (RE-4 at `904aefc`, and the cache change's B-3/CD-6 ruled,
A-129's call (4) and OBS-4) and the Migration Plan (the README's edit points
at `904aefc`); the spec delta edits the `Retired` line's sentence, adding no
scenario (proposal, "Re-read and Codex Findings (round A29)").

Citations follow `proposal.md`: packet files at `da33d92`, `CAS` for change 1,
`APO` for change 2, `project:N` and `tests:N` at `961c405`, all but the packet
files unchanged at main `15504f1`, whose `ideation/` holds packet revision 1
(`e45155a`). Main has since moved to `b42355e` (#40 and #41), whose `project`
changes only inside `workbenches()`, three net lines longer there, so that
each fact cited at `project:N` past `:89` holds at `b42355e` three lines
lower, as checked for each such cite, and whose `tests/test_project.py` keeps
every line cited here (`proposal.md`, the citation key; lane
openRepoProject-3's W160, OBS-9).

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
  `git_env` and `git_argv`, a row `branch` of its own in `GIT_KINDS`, not
  read-only, with no status pins and the protocol pins, and not the
  `delegate` row reused: at `904aefc` that table holds `probe`, `status`,
  `hidden`, `removal`, `delegate` and `push` (`project:1175-1188`),
  `child_budget` gives a `removal` or `delegate` child no budget and any
  other kind, under a deadline, the 5 s probe budget or the time left
  (`:1487-1502`), and only a read-only handle is put in `LIVE_PROBES`
  (`:1246`, `:1274-1275`), so that a `branch` row, not read-only, gets that
  budget and stays out of that registry (the reader RE's RE23-4; ruling
  A-100; re-pinned from `f3724fc` by the reader RN's RN-3, ruling A-131).
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
| `rev-list --max-count=1 --stdin` given named commits, then the one line `^<merge target SHA>` (round A3) | prints an amended-away draft, as the `--not` form does, and nothing for a plain history, exit 0 both times; any option on standard input, `--bogus` for one, is fatal: "invalid option '--bogus' in --stdin mode", exit 128 |
| `git check-ref-format --branch 'topic;id'` (round A3; the lead's F-1) | accepted; `git branch -d -- 'topic;id'` deletes it, and the restore line `git -C '<root>' branch 'topic;id' <sha>`, run by `dash` from another directory with a space in the root, recreates it and runs nothing else; the same line unquoted runs `id` |
| a hand-written `refs/heads/-f` (round A3; F-1) | `git update-ref` writes it, `git symbolic-ref HEAD refs/heads/-f` checks it out in a worktree, and it commits, publishes with `git push -u origin refs/heads/-f` and merges; `git branch -- -f <sha>` refuses, "'-f' is not a valid branch name", exit 128; `git branch -f <sha>` exits 0 after creating a branch named after the SHA; `git -C '<root>' update-ref refs/heads/-f <sha> ''` recreates the ref, and refuses, "reference already exists", exit 128, when it exists |
| a branch named `expire` (round A3; F-1) | `git reflog expire` runs the subcommand and prints nothing; `git reflog show refs/heads/expire` shows the branch's reflog |
| a branch whose upstream's remote-tracking ref was deleted, the merge target checked out in a linked worktree, the main worktree on another branch (round A3) | `git checkout <merge target>` in the main worktree refuses, "already used by worktree", exit 128; `git switch --detach <merge target SHA>` there succeeds, and `branch -d` then deletes the branch, exit 0 |
| a merged, published branch given, after the plan, a commit its merge target lacks in its worktree and reset to its planned SHA by `git reset --hard` (round A4; ruling A-24, Codex's P1 on `abad010`) | its head, `origin/<b>`, ahead and behind (0 and 0), the merge target and the worktree's status all equal the plan's, and its reflog names the commit as the new object of a `commit:` entry and the old object of the `reset:` entry after it; the plan's proof printed nothing before the move, and the same proof over the reflog as it then reads, after `worktree remove`, prints the commit, exit 0; without it `branch -d -- <b>` deletes the branch and its reflog, exit 0, and `git fsck --unreachable` then names the commit; a move to such a commit and back by `git update-ref` after the removal is caught the same way |
| a hand-written `refs/heads/HEAD` (round A5; ruling A-27, Codex's P2 on `9ff8202`) | `git check-ref-format --branch HEAD`, `git branch HEAD <sha>` and `git branch -- HEAD <sha>` refuse, "'HEAD' is not a valid branch name", exit 128; `git update-ref` writes the ref, `git symbolic-ref HEAD refs/heads/HEAD` checks it out in a worktree, which `worktree list --porcelain` lists as `branch refs/heads/HEAD`, and, in a repository whose `refs/remotes/origin/HEAD` is not a symbolic ref, it commits, publishes with `git push -u origin refs/heads/HEAD:refs/heads/HEAD` and merges; after `worktree remove`, `branch -d -- HEAD` with the seven pins deletes it and its reflog, exit 0, and so does `branch -d HEAD`, change 1's `delete-branch` form; `git -C '<root>' update-ref refs/heads/HEAD <sha> ''`, run by `dash` from `/` with a space in the root, recreates it, exit 0, and refuses, "reference already exists", exit 128, when it exists; `git reflog show refs/heads/HEAD` shows the branch's reflog and `git reflog show HEAD` the main worktree's; `for-each-ref` reports its upstream as `refs/remotes/origin/main`, the current branch's, where its configuration names `refs/heads/HEAD` on `origin` |
| the merge target's exclusion on `rev-list --max-count=1 --stdin` (round A5; lane openRepoProject-3's delta read, D8) | after a branch's named commits, the one line `^<merge target SHA>` prints an amended-away draft, and nothing for a plain history, exit 0; a line `^` with the SHA on the next line fails, "bad revision '^'", exit 128, and so does a line `^ <sha>`, "bad revision '^ <sha>'" |
| change 1's `delete-branch` for a hand-written `refs/heads/-f` (round A5; lane openRepoProject-3's delta read, D5) | `project` builds `git -C <root> branch -d <branch>` with no `--` (`project:734`), so `--branch=-f` gives `git branch -d -f`, which fails, "branch name required", exit 128, and leaves the ref; `branch -d -- -f`, the branch child's form, deletes it, exit 0 |
| a branch named `topic`, U+202E and `x`, restored by a line in the `$'...'` form (round A5; ruling A-28, Codex's P2 on `9ff8202`) | `git check-ref-format --branch` accepts the name; `git -C '<root>' branch $'topic\u202ex' <sha>`, run from `/` with `LC_ALL=C.UTF-8`, recreates it under bash 5.2.21 and zsh 5.9, exit 0; with `LC_ALL=C` bash passes the text `topic\u202Ex`, which Git refuses as not a valid branch name, exit 128, and zsh refuses the line, "character not in range", exit 1, while both drop the escape from `$'a\U000e0041b'`, passing `ab`, another name; `\xHH` gives its byte in either locale; dash 0.5.12, Ubuntu's `/bin/sh`, passes every such word as text, `$topic\u202ex` for the first, which Git refuses, exit 128; ksh93 was not available here |
| a local branch `b3` whose configured upstream is the local `b1` (`branch.b3.remote` `.`, `branch.b3.merge` `refs/heads/b1`; round A7, ruling A-32, RA's LOW-4) | `for-each-ref` over `refs/heads` gives `b3`'s upstream as `refs/heads/b1`; after `worktree remove`, `branch -d -- b1` deletes `b1`, exit 0, without a word about `b3`; `b3` stays at its SHA and its upstream track reads `[gone]`; the restore line recreates `b1`, exit 0, and `b3`'s upstream reads again |
| a rebase, then a bisect, of `b` in another worktree (round A7, ruling A-32, RA's LOW-5) | an interactive rebase whose instruction list begins with `break` stops at once, `worktree list --porcelain` lists that worktree as `detached` with no `branch` line, and `b` stays at its SHA; `branch -d -- b` refuses, "cannot delete branch 'b' used by worktree at", exit 1; after `rebase --abort` the worktree lists `branch refs/heads/b` and Git still refuses; a bisect of `b` started there behaves alike, detached while it runs and holding `b` after `bisect reset`; once that worktree is removed, `branch -d -- b` deletes it, exit 0 |
| `git -C '<root>' rev-parse --verify refs/heads/<b>`, run from `/` (round A7, ruling A-31) | exit 0 while the branch exists, `refs/heads/-f` and `refs/heads/HEAD` included; after `branch -d`, "fatal: Needed a single revision", exit 128; the restore line then recreates the branch, exit 0 |
| a rebase of `b` in another worktree, `b` published and its upstream's remote-tracking ref deleted, the main worktree on the merge target (round A8; ruling A-35, lane openRepoProject-3's F4 and its `exp2`, re-run) | `branch -d -- b` refuses, "cannot delete branch 'b' used by worktree at", exit 1, as it does with the ref present and with no upstream configured; `git checkout <merge target>` in the main worktree, which already holds it, exits 0, and `branch -d b` still refuses, exit 1; after `rebase --abort` and `worktree remove` of that worktree, the same checkout and `branch -d b` delete the branch, exit 0; with no rebase and the main worktree moved to a branch that lacks `b`, Git refuses "the branch 'b' is not fully merged", exit 1, and the checkout of the merge target and `branch -d b` delete it, exit 0 |
| `git worktree remove` given the main worktree, and the main worktree as the holder of a branch (round A14; ruling A-45, Codex's P2 on `1bf217c`), re-run on Git 2.43.0 and on the 2.36.6 floor | `git worktree remove <main>` and `git worktree remove --force <main>`, run from the main worktree or from a linked one, print "'<main>' is a main working tree", exit 128, and the main worktree stays; with the main worktree on a merged branch `b`, `branch -d b` run in it refuses, "cannot delete branch 'b' used by worktree at" (2.36.6: "Cannot delete branch 'b' checked out at"), exit 1, and so it does with a rebase of `b` stopped in it, which lists the main worktree `detached`, with a bisect of `b` in it, and again once `rebase --abort` or `bisect reset` leaves it on `b`; after `git checkout <other branch>`, or after `git checkout --detach`, `branch -d b` deletes it, exit 0; `git checkout <branch>` in the main worktree for a branch that a linked worktree holds is refused, "'topic' is already used by worktree at" (2.36.6: "already checked out at"), exit 128, so that a step that names a branch such as the merge target names a detach too, as `head-not-merge-target`'s linked case does |
| a rebase of `b` stopped in the main worktree, and the switch that frees `b` (round A15; ruling A-51, lane openRepoProject-3's W54, LOW-1), re-run here on Git 2.43.0 and by W54 on 2.43.0 and on the 2.36.6 floor | while the rebase is stopped, `git switch --detach` and `git switch <other branch>` in the main worktree both refuse, "fatal: cannot switch branch while rebasing", exit 128, and `branch -d b` refuses, "cannot delete branch 'b' used by worktree at" (2.36.6: "Cannot delete branch 'b' checked out at"), exit 1; after `rebase --abort` or `rebase --continue` the main worktree lists `branch refs/heads/b` again and `branch -d b` still refuses, exit 1; only then does `git switch --detach` or a switch to another branch free `b`, and `branch -d b` deletes it, exit 0; a bisect of `b` in the main worktree is alike once `bisect reset` ends it (W54: `git switch --detach` mid-bisect runs, exit 0, and leaves `b` held on both builds), so that the wait for a rebase or bisect to end comes before the removal of a linked worktree and before the switch of the main one |
| a linked holder of a merged, published branch `b` whose target worktree was already removed, on Git 2.43.0 and on the 2.36.6 floor (round A24; ruling A-98, reader RA2's L3) | clean: `git worktree remove` exits 0, and `branch -d -- b` then deletes `b`, exit 0; dirty, a tracked edit and an untracked file: the removal refuses, "contains modified or untracked files, use --force to delete it", exit 128; locked: it refuses, "cannot remove a locked working tree", exit 128; holding a submodule: "working trees containing submodules cannot be moved or removed", exit 128; an edit to a file flagged assume-unchanged or skip-worktree, or an ignored file, which `status --porcelain` does not print: the removal exits 0 and deletes it (as RA2's `p3b` found); in every case `git -C <holder> switch --detach` exits 0, changes no file, keeps the flags and the ignored file, and `branch -d -- b` then deletes `b`, exit 0, the holder remaining; `git checkout <other>` of a branch that differs at the flagged file refuses, "Your local changes to the following files would be overwritten by checkout", exit 1, the edit kept, but one of a branch that tracks the ignored file's path overwrites that file without a word, exit 0 |
| such a holder whose parent directory denies search (round A24; RA2's L3) | `worktree list --porcelain` still lists it, `branch refs/heads/b` and `prunable gitdir file points to non-existent location`; `git -C <holder> switch --detach` fails, "cannot change to ...: Permission denied", exit 128; `branch -d -- b` refuses, "cannot delete branch 'b' used by worktree at" (2.36.6: "Cannot delete branch 'b' checked out at"), exit 1; `worktree prune -n -v` would remove its administrative directory; `git worktree remove <holder>` exits 0 and deletes that directory, the worktree's `.git` file then naming nothing, after which `branch -d -- b` deletes `b`; once search is restored, the detach exits 0 and `branch -d -- b` deletes `b` |
| an operation stopped in such a holder: a merge on a conflict (round A24), and a merge stopped by `--no-commit` with no conflict, a cherry-pick, a revert and an am session on a conflict, each in a linked holder and in the main worktree as holder, on Git 2.43.0 and on the 2.36.6 floor (round A26; lane openRepoProject-3's W131, LOW-1) | for each of the four operations, merge, cherry-pick, revert and am, `git switch --detach` refuses, exit 128, "cannot switch branch while merging", "while cherry-picking", "while reverting" or "in the middle of an am session", with Git's advice to run that operation's `--quit` or `git worktree add`, changing no file and leaving `b` checked out there, `MERGE_HEAD` staying for a merge; `branch -d -- b` then refuses, exit 1; a bisect, by contrast, lets the detach run, exit 0, with a warning, `branch -d -- b` still refusing, exit 1, and a rebase refuses the detach as round A15's row says (`S/round-A26/bin/l1.sh`) |
| the upstream's remote-tracking ref deleted (round A24; RA2's L4) | with a linked holder detached and the main worktree on a branch that lacks `b`, `branch -d -- b` refuses, "the branch 'b' is not fully merged", with Git's `-D` advice, exit 1, and deletes `b`, exit 0, once the main worktree checks out the merge target, or, where a linked worktree holds the merge target, so that the checkout is refused, exit 128, once the main worktree is detached at the merge target's tip; with the main worktree as the holder, a checkout there of a branch that lacks `b` leaves `branch -d` refused, exit 1, where a checkout of the merge target or `git switch --detach` lets it delete `b`, exit 0, as a checkout of any branch does with the ref present |
| a commit U made on `b3` 40 days ago, which its merge target lacks, reset away now, then a default `git gc` (round A24; RA2's L1, its `p1c`) | `gc.reflogExpireUnreachable` drops U's `commit` entry and keeps the creation entry, the `commit: M` entry and the reset entry, whose old object is U: the gate's reading passes, `commit: M` being a movement after the creation anchor, the plan's proof prints U, and U is reachable; `git reflog show refs/heads/b3` and `git log -g` name U nowhere; `git -C <root> rev-parse --path-format=absolute --git-common-dir` prints the common directory, and `cat <it>/logs/refs/heads/b3`, run from `/`, prints U as the reset entry's old object; `branch -d -- b3` then deletes `b3`, exit 0, and `git fsck --unreachable` names U; the shape that the b3 AND writes by `git reflog expire` reads the same |
| a branch moved, after its re-proof, to a commit merged into neither the merge target nor its upstream (round A24; RA2's L2, its `p2`) | `branch -d -- b` refuses, "the branch 'b' is not fully merged", exit 1, with the upstream ref present or absent; the post-check's listing shows the new head; `git reflog show refs/heads/b` names it, and still does once the branch is moved back to its planned SHA |
| Git refusing for a cause that is no holder (round A24; RA2's N1) | a stale `packed-refs.lock` makes `branch -d -- b` exit 1, "Unable to create '.../packed-refs.lock': File exists", and a retry the same; a `reference-transaction` hook that rejects makes it exit 128, "ref updates aborted by hook"; `b` remains in both |
| a repository holding a hand-written `refs/heads/HEAD`, with a linked worktree on another branch and one on `HEAD` by `git symbolic-ref`, on Git 2.43.0 and on the 2.36.6 floor (round A25; the reader RE's RE2-1, under Q8) | `git status --porcelain=v1 -z --untracked-files=normal --ignored=matching` exits 0 in each of the three worktrees and writes `warning: refname 'HEAD' is ambiguous.` twice to standard error, so that under PR #19's warned-probe rule at `818311a` every row is `inspection-error` (`S/round-A25/bin/head.sh`) |
| `git checkout <merge target>`, `git switch <merge target>` and each with `--detach` at the merge target's tip, run in the main worktree on `b`, where the merge target tracks a file `d` that `b` tracks as a directory `d/`, tracks `ig-file/inner` where the worktree holds an ignored file `ig-file`, and tracks a force-added `app.log` where the worktree holds an ignored `app.log`, on Git 2.43.0 and on the 2.36.6 floor (round A26; lane openRepoProject-3's W131, MEDIUM-1) | each exits 0 and prints only "Switched to branch" or "HEAD is now at", and: overwrites the ignored `app.log` with the merge target's content; deletes the ignored file `ig-file` to make the directory that the merge target needs there; and deletes every ignored file below `d/`, `d/cache.log`, `d/build/a.o` and `d/build/sub/b.o`, to write the file `d`; an ignored file at a path that the merge target does not touch stays (`S/round-A26/bin/m1.sh`) |
| a repository like round A25's, its `refs/heads/HEAD` merged into `main` and published, with a linked worktree on another branch and one on `HEAD`, and `core.warnAmbiguousRefs` unset, set true or set false in its configuration, or set false in a `GIT_CONFIG_GLOBAL` file, on Git 2.43.0 and on the 2.36.6 floor (round A26; lane openRepoProject-3's W131, LOW-3) | unset or true: the pinned status probe, with `GIT_OPTIONAL_LOCKS=0` and the five status pins, exits 0 and writes `warning: refname 'HEAD' is ambiguous.` twice in each of the three worktrees; false, in either file: it exits 0 with nothing on standard error in each, so that under PR #19's warned-probe rule no row is `inspection-error` on that account; the hidden-state listing `ls-files -v --stage -z` writes nothing in any setting; in every setting, after `worktree remove` of the holder of `HEAD`, `branch -d -- HEAD` deletes it, exit 0, `git branch HEAD <sha>` refuses, exit 128, and `git -C <root> update-ref refs/heads/HEAD <sha> ''`, run from `/`, recreates it, exit 0; with the setting false that line, run by dash from `/` with a space in the root, recreates it, exit 0, and refuses, "reference already exists", exit 128, once it exists (`S/round-A26/bin/l3.sh`, `l3b.sh`) |
| `git checkout other` and `git switch other`, `other` being a branch that is not the merge target, run in a linked holder on `b` and in the main worktree as holder on `b`, where `other` tracks a file `d` that `b` tracks as a directory `d/`, tracks `ig-file/inner` where the holder has an ignored file `ig-file`, and tracks a force-added `app.log` where the holder has an ignored `app.log`, on Git 2.43.0 and on the 2.36.6 floor (round A27; lane openRepoProject-3's W138, OBS-1) | each exits 0 and prints only "Switched to branch 'other'", and, as round A26's row finds for the merge target: overwrites the ignored `app.log` with `other`'s content; deletes the ignored file `ig-file` to make the directory that `other` needs there; and deletes every ignored file below `d/`, `d/cache.log`, `d/build/a.o` and `d/build/sub/b.o`, to write the file `d`; an ignored file at a path that `other` does not touch stays (`S/round-A27/bin/o1.sh`) |
| the last holder P3 of a merged branch `b`, added with `--force` beside P1 on `b`, clean when read, after P1's `worktree remove`: P3 then given a commit made on a detached `HEAD`, `b` checked out again, so that only P3's HEAD reflog holds it, or that commit held by P3's `refs/worktree/keep` too, or nothing, on Git 2.43.0 and on the 2.36.6 floor (round A28; ruling A-126, the reader RJ's F1) | `status --porcelain` prints nothing in each case; PR #19's `worktree-only-commits` gate child, `rev-list --max-count=1 --glob=refs/worktree` over the objects of P3's `logs/HEAD`, `--not --branches --tags --remotes` and the objects of `b`'s reflog (its `specs/project-clean/spec.md:882-906` at `54e869b`), run in P3, prints nothing before the commit and prints the commit after it in both commit cases, exit 0, and nothing in the third; `git worktree remove <P3>` exits 0 in every case, and `git fsck --unreachable` then names the commit; `branch -d -- b` then deletes `b`, exit 0 (`S/round-A28/bin/f1.sh`) |
| a hand-written `refs/heads/HEAD` published as `refs/heads/HEAD`, with `branch.HEAD.remote` `origin` and `branch.HEAD.merge` `refs/heads/HEAD`, merged into `main`, `core.warnAmbiguousRefs` false, on Git 2.43.0 and on the 2.36.6 floor (round A28; ruling A-126, the reader RJ's F2, which the reader RN's RN-1 supersedes at the spec's sites under ruling A-128; the reason for lane openRepoProject-2's R-61 (b)) | `git status --porcelain=v1` writes nothing to standard error; with the main worktree on `main`, pushed one commit past `HEAD`'s tip, `for-each-ref` gives `refs/heads/HEAD` the upstream `refs/remotes/origin/main` and an empty track, `main`'s, and `branch -d -- HEAD` deletes it, exit 0; with the main worktree on `other`, pushed and level with `refs/remotes/origin/other`, which lacks that tip, the upstream reads `refs/remotes/origin/other` and `branch -d -- HEAD` refuses, "the branch 'HEAD' is not fully merged", exit 1; on a branch with no upstream, or detached, the listing gives `refs/heads/HEAD` no upstream; with `main` one commit ahead of its upstream, the track reads `[ahead 1]`; `refs/remotes/origin/HEAD`, its own upstream, holds its tip throughout (`S/round-A28/bin/f2.sh`) |
| a hand-written `refs/heads/HEAD` with a commit of its own, published as `refs/heads/HEAD` with `branch.HEAD.*` set, merged into `main` and `main` pushed, in a linked worktree beside one on a merged, published `topic`, the main worktree on `main`, `core.warnAmbiguousRefs` unset or false in the repository's configuration, and feature 004's `project clean --all-safe --json` at `904aefc`, `git show 904aefc:project`, run on the fixture only, on Git 2.43.0 and on the 2.36.6 floor (round A28; ruling A-128, the reader RN's RN-1) | unset: the pinned status probe in that worktree warns `refname 'HEAD' is ambiguous.` twice, exit 0, and every row is `inspection-error`, the `topic` row with `probe-failed` "git status failed: unparseable output"; false: the probe writes nothing to standard error, the `topic` row is `merged-removable`, and the `HEAD` row is still `inspection-error`, its one error `probe-failed`, "git for-each-ref failed: unparseable output", its upstream null, though `for-each-ref` names `refs/remotes/origin/main`; in both the plan is incomplete with `inspection-incomplete` and the preview exits 1 (`S/round-A28/bin/rn1.sh`) |
| `b3`, whose configured upstream is the local `b1`, at `b1`'s tip, in a linked worktree P3, beside P1 on `b1`, on Git 2.43.0 and on the 2.36.6 floor (round A28; ruling A-126, the reader RJ's F3) | after P1's `worktree remove`, the ref listing still gives `b3` the upstream `refs/heads/b1` with an empty track and `b1` at its SHA, as the plan's listing did; after `branch -d -- b1`, exit 0, the listing gives `b3`'s upstream track `[gone]` and no `b1`; `worktree remove` of P3 exits 0 and `b3` stays at its SHA (`S/round-A28/bin/f3.sh`) |
| a linked holder S of a merged `b` whose directory is moved away, as an unmounted drive leaves it, beside P on `b`, which `worktree remove` removes, S holding an untracked and an ignored file, on Git 2.43.0 and on the 2.36.6 floor (round A28; ruling A-126, the reader RJ's F5) | `worktree list --porcelain` lists S with `branch refs/heads/b` and `prunable gitdir file points to non-existent location`; `branch -d -- b` refuses, "cannot delete branch 'b' used by worktree at" (2.36.6: "Cannot delete branch 'b' checked out at"), exit 1; `git -C <S> switch --detach` fails, "cannot change to", exit 128; with S moved back, the detach run there exits 0 and keeps both files, and `branch -d -- b` deletes `b`, exit 0; with S moved to a new path, `git worktree repair <new path>` exits 0, the registry lists the new path on `b`, and the detach there and `branch -d -- b` do the same; with S gone and another worktree T also moved away, `git worktree prune --dry-run -v` lists both, `git worktree prune` removes both entries, T then fails "not a git repository" once moved back, and `branch -d -- b` deletes `b`, exit 0 (`S/round-A28/bin/f5.sh`) |
| a linked worktree X on a merged `b` whose administrative `gitdir` file names the main worktree's `.git`, beside P on `b`, which `worktree remove` removes, the main worktree on `main`, on Git 2.43.0 and on the 2.36.6 floor (round A28; ruling A-126, the reader RJ's F7) | `worktree list --porcelain` lists the main worktree's path twice, on `refs/heads/main` and on `refs/heads/b`; `branch -d -- b` refuses, naming the main worktree's path, exit 1; `git -C <main> switch --detach` exits 0 and detaches the main worktree, and `branch -d -- b` still refuses, exit 1; `git worktree repair <X>` exits 0 and the registry lists X on `b`, `branch -d -- b` still refusing, now naming X, exit 1; `git -C <X> switch --detach` exits 0 and keeps X's untracked file, and `branch -d -- b` deletes `b`, exit 0, the main worktree on `main` (`S/round-A28/bin/f7.sh`) |
| a hand-written `refs/heads/HEAD` with a commit of its own, published as `refs/heads/HEAD` with `branch.HEAD.remote` `origin` and `branch.HEAD.merge` `refs/heads/HEAD`, merged into `main` and `main` pushed, the main worktree on `main`, a linked worktree T on a published `topic` and a linked worktree H on `refs/heads/HEAD`, `core.warnAmbiguousRefs` false, the ref listing `for-each-ref refs/heads/HEAD` run in each, on Git 2.43.0 and on the 2.36.6 floor (round A29; ruling A-132, lane openRepoProject-3's W166, OBS-1) | run in the main worktree the listing gives `refs/heads/HEAD` the upstream `refs/remotes/origin/main`, in T `refs/remotes/origin/topic`, and in H `refs/remotes/origin/HEAD`, its own; `branch -d -- HEAD` run in H refuses, "cannot delete branch 'HEAD' used by worktree at" (2.36.6: "Cannot delete branch 'HEAD' checked out at"), exit 1, and the branch stays; with `branch.HEAD.*` removed the listing run in H gives no upstream, and run in the main worktree still `refs/remotes/origin/main` (`S/round-A29/bin/o1.sh`) |

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
P-1). Lane openRepoProject-3 reads Git's history as accepting a pseudo-option
such as `--not` on `rev-list`'s standard input only from Git 2.42 (its
re-read's MEDIUM-3, unverified on 2.36), so the proof gives the merge target's
exclusion as the one line `^<merge target SHA>`, a revision rather than an
option, which the round A3 row above checks on 2.43.

The Git 2.36 floor was not available for these checks here, nor for rounds
A3's, A4's, A5's, A7's and A8's; D9 puts them on change 1's CI floor job. Lane
openRepoProject-3, running rows of this table on Git 2.36.6, 2.40.4 and 2.43.0
(its delta read of `9ff8202`, D10), found the same exit statuses and outcomes
on all three and three messages that differ, so the messages the table quotes
are 2.43.0's: on 2.36.6 and 2.40.4 an option on `rev-list`'s standard input
reads "options not supported in --stdin mode", the refused checkout "is
already checked out at", and the refused `branch -d` "The branch '<b>' is not
fully merged.", capitalised and with a full stop. D9's fixtures assert exit
statuses and outcomes, never Git's wording.

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

A flagged `--apply`, single or batch, is a removal apply, so that on a
standard input that is not a terminal and without `--yes` it refuses with
`confirmation-required`, exit 2, before any mutation, as "Clean hands off
work requiring review" refuses a removal apply, and no branch stage starts
(the ADDED requirement, with an AND in "A single target with the flag equals
a one-item batch"; ruling A-109). That refusal comes once the plan has passed
the checks that the batch requirement runs before any question: an
incomplete plan refuses first, an `--expect-plan` mismatch next, and a
complete batch plan that selects nothing prints "No eligible worktrees" and
exits 0 without asking, a single target that a gate excludes refusing with
`target-excluded` (PR #19's `specs/project-clean/spec.md:909-916` at
`54e869b`; feature 004 at `904aefc`, read as a check, its checks 1 to 6
before check 7, `project:4202` and `:4243-4251`; the reader RN's RN-2;
ruling A-128). Brett Heap's Q9 (c), which PR #19 builds,
scopes that refusal to "`--apply` of a removal, single or batch" and says
"push and branch deletion keep the baseline's refusal, `Type yes to run this
plan: Supply explicit options when stdin is not a terminal.`, with exit status
2 and no code" (its `specs/project-clean/spec.md:616-621` at `4512441` and
`:657-662` at `54e869b`, the same words, which neither its round (s) nor its
round (t) restates; lane openRepoProject-3's W133, OBS-3, and W138, OBS-4).
Read beside this change's sentence that
makes `--retire-branches` a separate, explicit action, that "branch deletion"
could be taken to bind the flag's stage, as the reader RD2's M1 found of PR
#19's "Branch deletion SHALL refuse ..." until its round (p) named the
action, "The `delete-branch` action SHALL refuse" (its
`specs/project-clean/spec.md:416` at `4512441` and `:457` at `54e869b`).
Settled the same way: the
branch deletion that keeps the baseline's refusal is the explicit
`delete-branch` action's, with which the flag is refused as
`invalid-arguments`, and the flag's stage runs only inside a removal apply
that has passed its own confirmation, so that the removal's
`confirmation-required` governs. This change's sentence names that
requirement rather than restating its text, so that it holds on change 1's
text, where every `--apply` refuses so, and on PR #19's alike (ruling A-50).

Under the flag the plan decides each selected row's branch (D4), prints the
flagged plan lines (D8), gives each `selected` entry a `branch_plan` sub-record
and adds `retire` to the digest input (D10), and counts the stage in
`operations.estimated` and `probes.estimated` (D7). The digest input under the
flag therefore differs from every flagless one, even when it retires nothing, so
`--expect-plan` binds a flagged apply only to a flagged preview; a flagless
digest given to a flagged apply refuses with `plan-digest-mismatch`, exit 2,
before any question or mutation, as change 1 refuses any mismatch. Without the
flag the digest input and value are change 1's byte for byte, and so is the
report's equality with the `--all-safe` preview that "Clean reports local
worktree state" states; that requirement is MODIFIED only to say a flagged
plan's digest is its own.

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
checks of D4, in memory; the re-read's last step, the re-proof of D4 (a
bounded read of the branch's reflog and one `rev-list --stdin` child; ruling
A-24); the branch child of D3; and, once a branch child was spawned, the
post-check, one more listing of the same shape.

The next target's revalidation keeps change 1's sourcing: after a plain
`removed`, the rescan's three repository children serve as its repository
part, counted in its `probes_performed`, as feature 004's T085 says; the
stage's re-read and post-check are counted in the stage's own
`probes_performed` (D5) and are never reused. A merge target moved by a
concurrent writer during a branch stage is therefore not caught by the next
target's revalidation, which compares the rescan read before that stage, but
by the next target's own re-read before its branch child, which compares the
merge target (D4, ruling A-14), and retains that branch with `state-changed`.
Concurrent writers are outside the contract (`clarifications.md`, S-4). The
narrow guarantee states this sourcing: under the flag, the repository-wide
values a revalidation takes from the previous rescan were read before that
target's branch stage, earlier by at most the stage's own bounded run (its
reads, its listings, its re-proof and its branch child, each under a 5 s
budget) and a branch child's reap, and a change to them during
the stage is outside the contract for the next removal, whose own branch
evidence and merge target its re-read compares again (lane openRepoProject-3's
re-read, LOW-12). Rerunning the repository part after each stage was not
taken: it adds three children per target to a fit that already defers targets
(D7).

A target that does not enter the stage gets its `branch_retirement` without a
child, by the table in D5.

### D3. The compare-and-delete (A-2, A-5 as amended, A-20)

The branch child is a handle of a new kind, `branch`, through feature 004's
runner: the environment that the evidence model gives every Git child, the
variables it removes and the variables it sets, any trace2 variables among
them, without `GIT_OPTIONAL_LOCKS`, because it writes, the evidence model
giving that variable to read-only probes alone; its own process group; standard
input from the null device; standard output and standard error read and capped
like a probe's. The environment is worded relatively, with no count of names
and no trace2 pin of its own, so that the evidence model's later text, which
removes more names and pins trace2 where PR #19's rounds do, changes none of
this change's words (ruling A-50; readers RI's RI-2 and RH's M2). Its argument
vector is

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

It spawns only while more than change 1's 5 s removal floor of the work deadline
remains, as the cache change starts its cache stage, and its budget is then
`min(5 s, work remaining)`, which is the whole 5 s; so the work deadline never
stops a branch child part-way, and the only stop past its budget is one of a
child that ran its full 5 s, a hung one. The re-read before it, its re-proof
included (D4), gets `min(5 s, work remaining less the removal floor)`, as the
cache change words its cache stage, so that the floor is left for the spawn.
A branch child is not signalled
on a signal or an exception and is waited for within its budget, as a removal
child is waited for, because a ref transaction killed part-way can leave a
`.lock` file to clear by hand. Unlike the cache stage's reads, which are
abandoned at their budget, a branch child is a mutation and is never
abandoned at its budget: past it, it gets change 1's probe termination and is
reaped, and the post-check decides (ruling A-20). Change 1's project-command
Termination paragraph names only probe children, killed on every exit path, and
removal children, waited for, so that paragraph is MODIFIED to name the branch
child beside the removal child, and its Budgets sentence to give the re-read its
narrower budget. That block is written on PR #19's text, and lane
openRepoProject-2 agreed it on 2026-10-19 (ruling A-20; proposal, Dependencies
and Sequencing). The re-proof of ruling A-24 is a probe child, killed like one
on every exit path, and the re-read's last step, so that the block's Budgets
clause for "the re-read of a `clean --retire-branches` branch stage" already
gives it the re-read's budget, and the agreed block needs no edit for it.

Realization note for feature 006, from lane openRepoProject-2 (2026-10-19):
feature 004's runner registers every probe handle in `LIVE_PROBES` and kills
every live group in it on an exception path (`kill_live_probes()`; `project`
on branch `004-project-clean-all-safe` at `5a02c1a`). The branch child must
stay out of that registry, as the removal child does: its `GIT_KINDS` row is a
non-probe one, as the `removal` and `delegate` rows are, so `ChildHandle.start`
never adds it, and its past-budget termination is driven by the driver's
`advance()`, never by `kill_live_probes()`. The row is `branch`, its own, and
not the `delegate` row, which `child_budget` gives no budget (Context; reader
RE's RE23-4).

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
and passes. A branch named `HEAD` never reaches that test, since its row is
`inspection-error` before any plan selects it (D8; ruling A-128); for it, Git's
test and the ref listing would take the upstream of the command directory's
current branch, the branch's own only where that directory is the worktree on
`refs/heads/HEAD`, which holds the branch, so that Git refuses to delete it
there; that is why its row's upstream evidence is not read (Context, rounds
A28 and A29; the reader RJ's F2, under the reader RN's RN-1; lane
openRepoProject-3's W166, OBS-1; rulings A-126, A-128 and A-132). That is the
PR #2
finding that `branch -d` "can accept a tracking branch based on its
configured upstream"; D4 runs first, so the stage, not
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
and leaves the `branch.<b>` section; Brett Heap ruled that question as
recommended, option (a), this compare and `branch -d` (ruling A-127).
`branch -D`, `--force`, `-f` and any second branch child are never used.

### D4. The plan's keeps, the checks, the re-proof, and which targets qualify (A-2, A-3, A-14, A-16 to A-18, A-24)

**The plan's keeps.** Under the flag the plan decides, for each selected row,
whether the run retires its branch, and keeps it for the first of these
reasons that holds, in this order so that the printed advice never leads to
deleting work only the reflog holds as this run's plan read it; a branch can
still move between the plan and the retry, so that a kept branch's line whose
step ends in the retry, for a branch the stage did not re-prove, also names the
reflog inspection before it, saying, but for `branch-changed`'s line, that only
this run's plan proved the reflog (D8; ruling A-60; lane openRepoProject-3's
W78, LOW-3, its W89, LOW-1, under ruling A-74, and its W94, LOW-1, under ruling
A-79):

1. `reflog-unmerged` (A-16, as amended): a commit the branch's reflog names,
   the new object or the non-zero old object of an entry of
   `logs/refs/heads/<branch>` as the `unstarted-branch` gate read it, the
   oldest surviving entry's old object included, is not proven an ancestor of
   the merge target's SHA. One `rev-list
   --max-count=1 --stdin` child per repository is given on its standard input
   every selected row's named commits, one per line, then the one line
   `^<merge target SHA>`, `^` immediately followed by the SHA, a revision and
   not the pseudo-option `--not`, which Git takes on standard input only from
   2.42 by lane openRepoProject-3's reading (its re-read's MEDIUM-3); a line
   `^` with the SHA on the next line is fatal (Context; lane
   openRepoProject-3's delta read, D8). It prints nothing when every named
   commit is merged. Only when it prints a commit does one such child per
   selected row run, over that row's commits and the same line, to say which
   rows fail. A failed child, or one timed out at its own 5 s budget, fails the
   proof of every row it covers, so those branches are kept and the plan stays
   complete: the proof decides only which branches retire, never whether the
   plan is whole. Only the deadline passing during the proof makes the plan
   incomplete, with `deadline-exceeded`, as for any planning child; the bounds
   block's incompleteness sentence names this exception (its re-read's
   MEDIUM-1). A row whose proof did not finish, the deadline passing while it
   ran or before it started, is kept with `reflog-unmerged` too, so that its
   `branch_plan` and its plan line still say what the preview would do, a
   decision no apply acts on, since such a plan is incomplete (ruling A-32,
   RA's LOW-7). The gate's read is reused, so no file is read again: feature
   004 at `e69f6ef`, checked only as a check, keeps what the gate read in
   `row.reflog_objects` (`project:4776` and `:4808`), every non-zero old and new
   object once, so that the reuse needs no change to its API and reader RE's
   RE-6 is closed (ruling A-48, reader RI's RI-5).
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
   out in the rescan's registry listing; else `retained`, `branch-in-use`. A
   worktree in which a rebase or a bisect of the branch is in progress is
   listed detached, with no `branch` line, so neither this check nor the
   plan's `branch-in-use` keep sees it; Git's own checked-out refusal does,
   and the branch is `retained` with `git-refused`, a residual the ADDED
   requirement states (Context; ruling A-32, RA's LOW-5). Reading the
   worktrees' `rebase-merge/head-name`, `rebase-apply/head-name` and
   `BISECT_START` would foresee it; it is not taken, as the ruling states
   the case as a residual.
6. The re-proof, the re-read's last step (ruling A-24): the branch's reflog,
   read again as the `unstarted-branch` gate reads it, names no commit that
   one `rev-list --max-count=1 --stdin` child prints, given every named commit
   and then the one line `^<merge target SHA>`, as the plan's proof is given;
   else `retained`, `reflog-unmerged`, or `state-changed` where its read or
   child fails or runs past its own budget (below).

A value the re-read's manifest read or listing cannot establish, a listing that
fails or times out at its own 5 s budget or a manifest read that does, is
`retained` with `state-changed`, as change 1's revalidation counts an
unreadable value as a difference; so is a re-proof that decides nothing,
whether its child failed or timed out at its own 5 s budget or its read failed
or ran past its own budget (rulings A-43 and A-44). A re-proof that decides the
reflog cannot be proven, its read finding the reflog missing, empty or at its
64 KiB bound, or finding what the gate's reading cannot decide, a line that
does not parse or a last entry whose new object is not the head the re-read
observed (ruling A-32, RA's LOW-6), is `retained` with `reflog-unmerged`, so
that no branch child runs on a reflog the stage has not proved. A re-read
whose budget the work deadline ended, its re-proof included, is `retained` with
`deadline-exceeded`. A signal stops neither: as change 1's D15 has it for the
apply phase, the handler only records, so a re-read or re-proof in flight runs
to its own end or budget and its outcome decides as above; where that outcome
leaves the branch to retire, the stage starts nothing more and the branch is
`retained` with `interrupted` (D7; ruling A-34, RE-2).

The re-read's outcomes follow PR #19's rule for revalidation, which since its
round (d) governs every Git child and every filesystem call of its steps, cited
here at `f0bf538`, whose text there its rounds (f) to (i) keep, and its rounds
(j) to (t), up to `54e869b`, keep but for the work-tree
probe's outcomes, whose output round (j) reads as one path even over several
lines (lane openRepoProject-2's R-287 and R-291), which this section does not
restate (its `specs/project-clean-review-safety/spec.md:113-135`, and
`:115-139` at `e14ada0`, `173d83c`, `ccc52b9`, `20084cd`, `2250830`, `88d0d36`
and `e0b1671`, `:137-161` at `818311a`, `:138-162` at `4512441` and
`:140-164` at `dab8a64` and `54e869b`, the same text, round (q) adding
`core.ignoreCase=false` to the removal command's pinned configuration after
it, round (r), before it, Q2 (2)'s `lstat` of `<dir>/.git` to the targeted
check's hidden-state step and a `.git` entry to `contains-submodule`'s reason,
and round (s), before it too, that `lstat` for every directory that the
listing shows holding an index entry directly or below it, other than the
worktree's own top level (its `:112-116` at `dab8a64` and `54e869b`), none
of which the stage runs; lane openRepoProject-2's R-171 and R-208; rulings
A-38, A-42, A-47, A-67, A-71, A-75, A-78, A-84, A-86, A-106, A-110 and
A-119): a child or a
read that the work deadline cuts counts as no difference and gives
`deadline-exceeded`, and one that fails, or runs past its own budget while the
deadline is not the limit, gives `state-changed`; a filesystem call that finds
no file or directory at its path (`ENOENT` or `ENOTDIR`) does not fail but
decides that the path is absent, a value that keeps its step's reason (its
`design.md:489-503` at `662be89`, the same words from "Every filesystem read"
at `:645-660` at `54e869b`, `:642-657` at `dab8a64` and `:623-638` at
`4512441`, round (r) adding before them its D7 phrase on Q2 (2)'s `lstat`,
which round (s) rewords, naming every directory that the listing shows
holding an index entry directly or below it, other than the worktree's own
top level, and one filesystem call for the target as at planning, `:602-617`
at `818311a`, `:554-569` at `88d0d36`, `:552-567` at `2250830` and `:545-560`
at `20084cd`, where round A20's `:541-555` at `ccc52b9` stopped one line
short; rulings A-79, A-84, A-86, A-106, A-110 and A-119).
Step 2 of the ADDED requirement had
counted a re-read listing or manifest read that "fails or times out" as a
difference, which took in one whose budget the work deadline ended, while
D5's table and the sentence
above on a re-read whose budget the work deadline ended gave that read
`deadline-exceeded`; step 2 now gives it `deadline-exceeded` as well. For such
a read this changes the exit status from 2, by D6's exit row 4 for a
`state-changed` retention, to 1, by its row 2; its line from `Kept BRANCH
(state-changed)` to `Kept BRANCH (deadline-exceeded)`, and the stop block's
reason to `branch BRANCH: deadline-exceeded`; and the later targets from
`not-attempted` with `batch-stopped` to `not-attempted` with
`deadline-exceeded`, their `branch_retirement` staying `branch-retention-stop`.
Its next step, then `retry: RETRY`, now names the reflog inspection before
the retry, since the re-read stopped before its re-proof (below; ruling
A-55), and the stop block's `Next:` is unchanged. The
re-proof follows the rule as well (rulings A-43 and A-44): its own failure or
timeout, of its read or its child, gives `state-changed`, as a re-read
listing's does, and a budget the work deadline ends gives `deadline-exceeded`.
For a re-proof that fails or runs past its own budget this changes the reason
from `reflog-unmerged` to `state-changed`, its line from `Kept BRANCH
(reflog-unmerged)` to `Kept BRANCH (state-changed)`, and the stop block's
reason to `branch BRANCH: state-changed`; the branch remains and the exit
status stays 2, by D6's row 4. Its next step keeps the reflog inspection, ahead
of the retry: `; BRANCH's reflog was proven merged into MERGE_TARGET only at
this run's plan; inspect git -C ROOT reflog show refs/heads/BRANCH before
retrying: RETRY`, where
`reflog-unmerged`'s ends `before any delete-branch` (ruling A-49, Codex's P2 on
`7b224c7`; it supersedes ruling A-46's keeping of W47's LOW-3, which had the
line say `retry: RETRY` alone). RETRY is change 1's `delete-branch`, whose own
check is the branch's tip against the merge target and never reads the reflog:
a branch that briefly held a commit the merge target lacks, or an amended-away
one, and then returned to its merged tip passes it, and `git branch -d` deletes
the branch with its reflog, the only reachability of that commit. A re-proof
that decided nothing has not proved the reflog, so the line says to inspect it
before the retry, in the form that `branch-changed`'s step, `inspect it
before retrying`, had when ruling A-49 chose it. The same holds wherever the
stage did not re-prove the reflog, its re-proof never starting or never
finishing with a proof, and the line's next step is RETRY (rulings A-53 and
A-55; lane openRepoProject-3's W60,
MEDIUM-1): the plan's proof of the reflog does not stand by itself, since
step 3's reason for the re-proof is that a branch moved to a commit the merge
target lacks and back since the plan passes every check of the re-read while
its reflog names that commit, so that only the re-proof renews the plan's
proof. W60 reproduced the loss on Git 2.43.0 and on the 2.36.6 floor: with
the merge target moved, the re-read stops at check 4, and the printed retry's
`git branch -d -- b` deletes `b`, its reflog-only commit becoming
unreachable. So the line names the reflog inspection before the retry for a
`state-changed` that the re-read's values caused, an upstream value, the
manifest's `tracking_branch` or the merge target different from the plan, or
one that could not be established, a failed listing or manifest read
included, which stops the stage at its reads or at checks 3 and 4, before the
re-proof (ruling A-55 reverses round A15's keeping of `retry: RETRY` there,
which rested on the plan's proof standing); for a `deadline-exceeded` whose
re-read or re-proof could not start, or whose re-read or re-proof budget the
work deadline ended (ruling A-53 for the re-proof's); for an `interrupted`
before the re-proof started, a signal stopping no re-proof, which runs to its
own end or budget and decides; for an `internal-error` of an exception
before the re-proof proved the reflog; and for a `removal-ceiling`, whose
stage never ran. `retry: RETRY` stays where the stage's re-proof proved the
reflog merged before the stage ended: the `spawn-error`,
`unconfirmed-retirement` and `probe-timeout` lines, whose re-proof proved it
before the branch child, and a `deadline-exceeded`, `interrupted` or
`internal-error` after that proof, too little work time being left to start
the branch child, a signal received before it, or an exception after the
proof or once the post-check showed the branch present. The lines with their
own next steps keep them, and those whose own step ends in RETRY for a branch
the stage did not re-prove name the inspection too, after their step and
before the retry (ruling A-60; lane openRepoProject-3's W69, LOW-3, which
showed on Git 2.43.0 and 2.36.6 that following such a step deletes the branch
and orphans a commit only its reflog held, as this round's run of each own
step did again): `head-not-merge-target`, a plan keep, which spawns no stage,
in both its forms; `branch-in-use` with the main worktree as holder, a plan
keep or the rescan's; and `branch-changed`, whose re-read stopped before its
re-proof or whose stage never ran, which reads `; now at SHA2; its reflog is
not proven merged into MERGE_TARGET; inspect it and git -C ROOT reflog show
refs/heads/BRANCH before retrying: RETRY`. The holder lines follow ruling
A-98, the reader RA2's HIGH L3, which re-opens rulings A-45 and A-60, since
A-60 weighed only the branch's reflog and never the holder's own work, and as
ruling A-126 narrows A-98's allowance of a removal to one routed through the
tool's gates (the reader RJ's F1): for a `branch-shared` last holder that the
run did not reach, `not-attempted`, the only holder the plan itself would
remove, the flagged single-target command for it, `project clean ROOT --apply
--action remove --worktree PATH2 --retire-branches`, with no retry, since a
`branch-in-use` holder is a row the plan did not select, its later gates
unread from the one that excluded it, its index unread where `not-requested`
or `deferred-target-cap` excluded it, or a worktree the plan never read, and a
last holder that the run reached and did not remove was refused, failed or
left `unknown`; the command and not `git worktree remove`, because this run's
read of that holder is its plan's alone, the run having stopped before it
revalidated it, and a raw `git worktree remove` deletes, with exit 0, any state
of the kinds change 1's gates protect that the holder gained since, an ignored
or index-flagged file, or a commit that only its HEAD reflog or its
`refs/worktree/` holds, which PR #19's `worktree-only-commits` gate keeps (its
`specs/project-clean/spec.md:882-906` at `54e869b`; Context, rounds A24 and
A28), where the command builds a fresh plan that reads every gate again,
removes PATH2 only if that plan selects it, proves BRANCH's reflog again and
retires BRANCH only if that plan does; for a holder whose path could not be
read, R-324's no-prune clause and never a removal; for a holder that the plan
excludes as `registration-mismatch` under PR #19's M3 (a), its path being, or
holding, the main worktree, the common directory or another worktree, or
another row's path, M3's own step in PR #19's words (its
`specs/project-clean/spec.md:112-129` at `54e869b`), and then, once that
registration is repaired, a detach run in the worktree it names, which still
holds BRANCH, and the reflog inspection and the retry, since a detach at PATH2
acts on the other worktree there, the main worktree's included, and frees
nothing (Context, round A28; the reader RJ's F7); for a holder whose path is
missing, its row `stale-worktree` with `present` false, at which no detach can
run, its remount or repair and a detach run there, or else change 1's
stale-worktree caution in PR #19's words (its `:216-240`), then the reflog
inspection and the retry, since `git worktree remove` and `git worktree prune`
each delete such an entry's administrative directory, and with it the HEAD
reflog of a worktree that was only moved or unmounted (Context, round A28; the
reader RJ's F5); and for every other holder, its own work named as the work to
save and a detach, `git -C PATH2 switch --detach`, which changes none of its
files, then the reflog inspection and the retry, the plan alone having proved
the reflog. Round A24's Context
rows show why: `git worktree remove` of a holder deletes its ignored and
index-flagged files with exit 0, refuses a dirty one with Git's `--force`
advice, and deletes the administrative directory of one whose path cannot be
read, where the detach keeps every file and flag and frees the branch. The
step names no checkout of another branch, which the ruling's text allows,
because a checkout of a branch, with exit 0 and without a word, overwrites an
ignored file at a path that the branch tracks, deletes an ignored file where
it needs a directory and deletes every ignored file below a path that it
tracks as a file, the whole residual that Risks records for a checkout of
MERGE_TARGET (Context, rounds A24, A26 and A27; lane openRepoProject-3's
W138, OBS-1). `reflog-unmerged` prints no retry and
names, as its inspection, the reflog file that the gate read, since `git
reflog show` prints no commit that the reflog names only as an old object, the
shape a default `git gc` leaves (reader RA2's L1; D8). Both `git-refused` lines
keep their bare retry after their steps, their branch child having run after
the re-proof proved the reflog, as for `spawn-error`, so that `git-refused`
with the upstream ref absent no longer shares `head-not-merge-target`'s text;
and the line of any `retained` reason whose post-check listed the branch at a
head other than the re-read's gives way to D8's moved line, which names that
head and the reflog inspection before the retry, the move having written an
entry that no proof saw (reader RA2's L2; D5). A target that the
run did not reach gets no `Kept` line: its retry is the deferral line or the
stop block's `Next:`, a flagged run that plans again and proves the reflog
again.

The stage makes two filesystem reads, each checked against that rule (ruling
A-42; lane openRepoProject-3's W40, its observation on R-208). The re-read's
manifest read follows it whole: one that fails or runs past its own budget is
a difference, `state-changed`, and one that the work deadline cuts gives
`deadline-exceeded`, as step 2 says; one that finds no manifest at its path
decides that the repository has none, as the plan's merge-target resolution
takes a repository without one, with no manifest candidate, so that a
manifest absent at the plan and at the re-read is no difference, its
`tracking_branch` null in both, and one that the plan read with a
`tracking_branch` and the re-read finds absent is a `tracking_branch`
difference, `state-changed`, the step's own reason, where one that the plan
read with no `tracking_branch` and the re-read finds absent gives no
difference (lane openRepoProject-3's W46, LOW-1). The re-proof's reflog read,
read as the `unstarted-branch` gate reads it, takes the rule whole. A reflog
missing at its path (`ENOENT` or `ENOTDIR`) is the rule's decided absence and
keeps the re-proof's own reason, `reflog-unmerged`, as step 3 says, as do a
reflog found empty or read to its 64 KiB bound and one that the gate's reading
cannot decide: each is a value that the read decided, as PR #19 gives its own
`worktree-only-commits` to a `logs/HEAD` read to that bound or holding a line
that cannot be parsed (its `specs/project-clean-review-safety/spec.md:110-111`,
`:122-127` and `:133-135`). The plan never selects a branch with no reflog
(the gate excludes it as `reflog-unavailable`) and records no reflog value, so
that a reflog missing at the re-proof is a change since the plan which the
stage's `state-changed` (the manifest's `tracking_branch` and the merge
target) does not take in (lane openRepoProject-3's W46, section 1 (iii)). A
reflog read that fails or runs past its own budget while the work deadline is
not the limit decides nothing, and gives `state-changed`, as the rule gives a
call that decides nothing (its `:115-120`): `reflog-unmerged` would say that a
commit the merge target lacks was seen, and none was (ruling A-43, lane
openRepoProject-2's answer on R-208). The re-proof's child follows the same
rule, a child that fails or runs past its own 5 s budget giving
`state-changed` (ruling A-44), and a read or child that the work deadline cuts
gives `deadline-exceeded`. The plan's own failed proof stays a
`reflog-unmerged` keep: the plan's reasons are its keep list's four, it has no
`state-changed`, and a keep never stops the run, where the re-proof gates a
deletion. Each retention of the stage keeps the branch, is not plain and
exits 2 by D6's row 4. No other filesystem read is in the stage: the
post-check and the branch child are Git children, the checks run in memory,
and the plan's proof reuses the gate's read. The stage reads no
administrative directory, so round (e)'s L-4, by which one that the
`operation-in-progress` listing finds absent is a registration difference,
`identity-changed`, does not reach it, and its L-5 changes only the case of a
SHALL NOT. R-208 is PR #19's reading of
`BA:271-276`, which went to Brett Heap to confirm as its O-2 (its
`design.md:499-503` at `662be89`, `:655-660` at `54e869b`, `:652-657` at
`dab8a64`, `:633-638` at `4512441`, `:612-617` at `818311a`, `:564-569` at
`88d0d36`, `:562-567` at `2250830` and `:555-560` at `20084cd`, where round
A20's `:551-555` at `ccc52b9` stopped one line short; rulings A-79, A-84,
A-86, A-106, A-110 and A-119). No word of step 2
changes for the
manifest: its value that the manifest read "cannot establish" does not take
in a decided absence, which establishes the manifest's values as absent; and
step 3 already names a
missing reflog, while its failed read and failed child now give
`state-changed` (rulings A-43 and A-44).

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

One Git child computes ancestry at the stage, the re-proof. The plan proved
the planned head an ancestor of the merge target's SHA through its merged set;
checks 2 to 4 find the head, its upstream evidence and the merge target
unchanged, so that proof holds at the target's current tip, as change 1's
revalidation reasons (CAS `design.md` D7), and no child repeats it but the
re-proof, whose input names the head among the reflog's commits (lane
openRepoProject-3's delta read, D12). The plan's
reflog proof does not carry over so: a branch given a commit the merge target
lacks and reset to its planned SHA between the plan and the stage passes
checks 1 to 5, its head, upstream evidence and merge target all as planned,
while its reflog now names that commit, which `branch -d` would leave
unreachable by deleting the reflog (Codex's P1 on `abad010`; Context). So the
stage runs the plan's proof again over the reflog as it then reads, one child
under the re-read's budget (ruling A-24). A-2 asks for ancestry "at its
current tip"; a moved merge target would need a `merge-base --is-ancestor`
child, but the canonical "MUST refuse when the state no longer matches the
reviewed plan" (`project-clean-review-safety/spec.md:51-53`) already retains
the branch there, so that child is never needed. This is narrower than A-2's
text: a branch whose merge target moved forward is retained, not retired.

What a deletion can lose is therefore bounded by what is proven: no commit
that the branch's head or its reflog names at the re-proof is lost, because
the plan proves the head merged, the re-proof proves the reflog's commits
merged, and otherwise the branch is kept; a reflog entry written after the
re-proof's read is in the residual window (D3). What a deletion does remove is
the branch's `branch.<b>` section, including its `description`, `pushRemote`
and any tool's keys, which nothing restores (Risks).

The re-read runs no identity probe. The repository identity is the one the
rescan re-established, which a target `removed` with reason null requires
(`CAS/pc:919-921`), and the narrow guarantee names it. A repository replaced
after the rescan that holds the same branch at the same head with the same
upstream evidence, merged into a merge target at the same SHA, loses no commit
that the head or its reflog, proved again by the re-proof, names by the
deletion, and one whose values differ retains the branch. Concurrent writers
are outside the contract in any case.

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
| `post_check_sha` | the head the post-check listed; null when it listed none, the branch absent, or did not run (reader RA2's L2) |
| `command` | the branch child's argument vector; null when none was spawned |
| `exit_status` | the branch child's status; null when none was spawned or its exit was not observed |
| `probes_performed` | the stage's re-read children, its listing and its re-proof, and its post-check child, 0 to 3; the target's own `probes_performed` stays change 1's, its revalidation's children (lane openRepoProject-3's L5) |

| Stage | When | Reasons |
| --- | --- | --- |
| `retired` | the post-check shows the branch absent after the branch child ran | null (exit 0); `git-failed` (nonzero exit); `probe-timeout` (`project` stopped the child past its 5 s budget); `internal-error` (an exception ended the stage after that post-check) |
| `retained` | the target is `removed` and its branch is present when the stage ends | `branch-changed`, `state-changed` (a value the re-read found different or could not establish, or the re-proof's read or child failed or ran past its own budget), `branch-in-use`, `reflog-unmerged` (the re-proof printed a commit, or its read decided that the reflog cannot be proven: missing, empty, at its 64 KiB bound or undecidable), `deadline-exceeded` (too little work time to start the re-read, its re-proof or the branch child, or the deadline stopped the re-read), `interrupted`, `spawn-error`, `git-refused` (nonzero exit), `unconfirmed-retirement` (exit 0), `probe-timeout`, `internal-error` (an exception ended the stage before its branch child was spawned, or after the post-check showed the branch present), `removal-ceiling` |
| `not-attempted` | the plan kept the branch, no branch remained to retire, or no stage ran | `reflog-unmerged`, `branch-in-use`, `head-not-merge-target`, `branch-shared` (the plan's keeps); `branch-missing`, `branch-retention-stop`, `target-not-removed` |
| null | the post-check failed, timed out or was abandoned by a second SIGINT, or an exception ended the stage after its branch child was spawned and before the post-check decided | `reconciliation-incomplete` |

`retired` with `deadline-exceeded`, in the draft's list, is unreachable under
the spawn floor (D3) and is dropped (A-5 as amended): `retired` carries reason
null, `git-failed` (a test `git` that deletes and then exits nonzero) or
`probe-timeout` (one that deletes and then hangs past its budget), so A-15's
scenario of a retirement with a reason stays, with those two. The sub-record's
`git-refused` and `git-failed` name the branch child's outcome, the branch
present or absent after a nonzero exit; they are not the target enum's split
of exit statuses at 128 (lane openRepoProject-3's L8), and the ADDED
requirement says so.

`reflog-unmerged`, like `branch-in-use`, is a reason of two stages. Under
`not-attempted` it is the plan's keep: printed, counted in the question,
plain, and never a stop. Under `retained` it is the re-proof's finding (ruling
A-24): the stage ran, the branch is present when it ends, and the plan did not
foresee it, so it is a retention the stage discovers, not plain, and it stops
the run and exits 2 (D6), while the target's removal stands, `removed` with
reason null. That follows the ruling's outcome, the branch kept with
`reflog-unmerged` and the worktree removed, through this table's own
definitions of the two stages.

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

An exception raised in a target's branch stage (ruling A-31, RA's MEDIUM-2)
does not take change 1's rule that an exception makes a target `unknown` with
`internal-error`: that rule's `unknown` means "removal is not proven", and the
rescan that admitted the target to the stage proved it. The target keeps the
stage, reason and reconciliation its rescan decided, and its
`branch_retirement` takes the stage the evidence then establishes, never
`not-attempted` with `target-not-removed`, which would claim that no stage ran:
`retained` with `internal-error` before a branch child was spawned or once the
post-check has shown the branch present; null with
`reconciliation-incomplete` once a branch child was spawned and no post-check
decided; and `retired` with `internal-error` once the post-check has shown the
branch absent, so that the result prints the `Retired` line with its SHA and
restore command, the one human record a person needs to undo the deletion
(Rollback). None of the three is plain, so the run stops after that target,
with exit 2, or 1 for the null stage (D6). The reconcilable block's exception
sentence gains that exception for the flag. Feature 004's per-target handler,
checked at `2cf34d3` and only as a check, makes any exception of a target
`unknown` with `internal-error` (lane openRepoProject-5's reader RE, its
RE-5), so feature 006 handles the stage's own exceptions inside the stage. At
`e69f6ef` RE-5 still holds: `apply_removals` rewrites any exception to
`unknown` with `internal-error` (`project:6208-6211`), and `_settle` waits for
a non-probe handle with no budget (`project:1610-1628`) (reader RI's RI-7;
ruling A-48).

`post_check_sha` records what the post-check saw, so that a branch moved after
the re-proof, which Git's own check then refuses, reads as a move in the record
as well as in its line (D8), the reason staying the one the branch child's
outcome gives, `git-refused` among them; it is null for a retired branch,
absent at the post-check (reader RA2's L2; ruling A-100).

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

Four examples of the sub-record, retired, retained after the merge target
moved, retained by the re-proof, and kept by the plan (the target's other keys
are change 1's):

```json
"branch_retirement": {"stage": "retired", "reason": null, "branch": "f1",
                      "planned_sha": "<40 hex>", "observed_sha": "<40 hex>",
                      "post_check_sha": null,
                      "command": ["git", "-c", "protocol.allow=never", "...",
                                  "-C", "<command directory>", "branch", "-d",
                                  "--", "f1"],
                      "exit_status": 0, "probes_performed": 3}
"branch_retirement": {"stage": "retained", "reason": "state-changed",
                      "branch": "f1", "planned_sha": "<40 hex>",
                      "observed_sha": "<40 hex>", "post_check_sha": null,
                      "command": null, "exit_status": null,
                      "probes_performed": 1}
"branch_retirement": {"stage": "retained", "reason": "reflog-unmerged",
                      "branch": "f1", "planned_sha": "<40 hex>",
                      "observed_sha": "<40 hex>", "post_check_sha": null,
                      "command": null, "exit_status": null,
                      "probes_performed": 2}
"branch_retirement": {"stage": "not-attempted", "reason": "reflog-unmerged",
                      "branch": "f2", "planned_sha": "<40 hex>",
                      "observed_sha": null, "post_check_sha": null,
                      "command": null, "exit_status": null,
                      "probes_performed": 0}
```

### D6. The stop rule and the exit status (A-4, as amended)

The packet's "a retention stops later targets" (`BA:1341-1342`) governs a
retention the stage discovers: a changed head or upstream, a moved merge
target, a reflog the re-proof does not prove (ruling A-24), a Git refusal, a
spawn error, a holder appearing, the deadline at the stage, an exception in
the stage (D5; ruling A-31). A keep the
confirmed plan names (D4) neither stops the run nor raises
the exit status by itself; that row exits as it would in a flagless run. So
the batch stops after the first target whose removal is not a plain `removed`
or whose `branch_retirement` is not plain. Feature 004 at `e69f6ef`, checked
only as a check (reader RI's RI-7; ruling A-48), keys both its batch stop and
its result's stop target on the target alone: `stopped = not (target["stage"]
== "removed" and target["reason"] is None)` (`project:6212`) and `stop =
next(...)` over the same test (`project:6368-6369`). A run stopped by the
branch stage of its last target would therefore have no stop target in its
`print_result` and would print the success line, where this change requires
the stop block with `branch BRANCH: REASON`; the realization changes both
sites, the loop's and the result's, where the text above states the rule for
the loop only. Later
targets are `not-attempted`
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
`probe-timeout`, `internal-error`) is not plain, stops the run and exits 2, as
change 1 stops after `removed` with `removal-ceiling`.

### D7. Bounds, counts, signals and the fit (A-5, as amended; A-24)

| Child | Budget | Counted under |
| --- | --- | --- |
| reflog proof, at plan time (one per repository, and one per selected row only when the first prints a commit); a failure or a timeout at its own budget keeps branches and leaves the plan complete | `min(5 s, work remaining)` | `probes` |
| re-read listing (and the manifest read, a filesystem call) | `min(5 s, work remaining less the removal floor)`, started only while more than the floor remains | `probes`, the sub-record's `probes_performed` |
| re-proof, the re-read's last step, after its checks pass (ruling A-24): one `rev-list --max-count=1 --stdin` child over the commits the branch's reflog then names (and the reflog read, a filesystem call); a commit printed retains the branch with `reflog-unmerged`, and a failure or a timeout at its own budget with `state-changed` | the re-read's, `min(5 s, work remaining less the removal floor)`, started only while more than the floor remains | `probes`, the sub-record's `probes_performed` |
| branch child | `min(5 s, work remaining)`, spawned only while more than the 5 s removal floor remains | `operations` |
| post-check listing, only after a branch child | `min(5 s, reserve remaining)` | `probes`, the sub-record's `probes_performed` |

The reflog proof is planning, like the merged set. The re-read, its re-proof
included, gates a mutation, as revalidation does, so it is work; the post-check
reconciles, so it runs in the reserve. When too little work time remains, none
of the re-read, its re-proof and the branch child starts, the branch is
`retained` with `deadline-exceeded`, and change 1's deadline rule makes every
later target `not-attempted` with `deadline-exceeded`, exit 1.

Signals (ruling A-34, RE-2). The plan's reflog children are planning probes: a
signal before the apply phase stops them like any probe, as change 1's D1 and
D15 stop the planning child. In the apply phase change 1's D15 holds for the
stage as for a removal: the handler only records, and the seam reads the slot
between steps, so a signal stops no child of the stage. A re-read listing, a
re-proof or a branch child in flight when it arrives runs to its own end or
budget and its outcome decides; the stage reads the slot before each re-read,
re-proof or branch child it would start, never before the post-check, and once
the slot is set it starts none of them, the branch `retained` with
`interrupted` unless the step that ran decided another reason (ruling A-35,
lane openRepoProject-3's F3). A branch child past its budget gets change 1's
probe termination
(SIGTERM to the group, SIGKILL 2 s later, a reap of at most 2 s) from that
budget, never from the signal. After the signal the post-check runs in the
reserve, as change 1 reconciles after a signal, and a second SIGINT while it
runs abandons it, as change 1's D15 abandons the remaining rescans, so that
the stage is null with `reconciliation-incomplete`. Feature 004, checked at
`2cf34d3` and only as a check, stops no child in its apply phase and, on a
second SIGINT, stops a probe in its reconciling phase (lane
openRepoProject-5's reader RE, its RE-2). At `e69f6ef` RE-4 still holds, and
the stage's needs stay unbuilt (reader RI's RI-7; ruling A-48): `child_budget`
has no term for the work remaining less the removal floor (`project:1268-1283`);
the phase stays `reconciling` from the rescan until the next target sets
`apply` (`project:6132`, `:6205`), so the stage's re-read would draw on the
reserve, and a second SIGINT would raise `Interrupted` out of its probes
(`project:1309-1318`), where this change lets a second SIGINT abandon only the
post-check; and `count_child` counts only a removal under `operations`
(`project:1285-1291`). At `904aefc` RE-4 still holds, as the reader RE found
at `f3724fc` in the review wave of 2026-10-23, round A24 re-reading it there
(ruling A-100), and the reader RN found at `904aefc` (its RN-3; ruling A-131):
`child_budget` has no such term and gives the reserve while reconciling
(`project:1487-1502`), the phase is set to `reconciling` in `remove_target`
(`:6936`) and to `apply` before each target (`:7009`), a second SIGINT while
reconciling still stops a probe (`interrupting()`, `:1528-1537`), and
`count_child` still counts only a removal under `operations`
(`:1504-1510`).

The 64 s bound holds: a branch child spawns with more than 5 s of work left, so
it ends or is stopped by the 50 s work deadline and is reaped within 4 s more;
the post-check and the final rescan run in the reserve up to 60 s, and a
reserve child stopped there is reaped within 4 s, as change 1 counts.

Counts: under the flag `operations.estimated` gains one per branch the plan
retires, so that it is 2T when no cache is listed and every branch is retired
(`add-project-clean-cache-disposal` also counts each listed cache entry
there); `probes.estimated` is change 1's F + W + E + 5T + 3 (`BA:820`) plus
three per branch the plan retires, the re-read's listing, its re-proof and the
post-check, plus the reflog children the plan spawned. Change 1's 5T is its
text at PR #19's `c462d87`: ten gates (its
`specs/project-clean/spec.md:577-583`), the two index gates after the target
cap (`:807-809`) and at most five Git children per revalidation (`:826-827`).
At `f0bf538` the term is 6T, or 7T where the plan read
`extensions.worktreeConfig` as true: twelve gates, with `operation-in-progress`
and `worktree-only-commits` added (its `specs/project-clean/spec.md:665-671`),
four after the cap (`:1003-1006`), and at most six Git children per
revalidation, seven where the repository sets the extension (`:1026-1028`),
which feature 004 at `e69f6ef` computes as its planning children plus 6T, or
7T, plus 3 (`project:4261-4262` and `:6218-6219`; reader RI's RI-8). The
figures below give each at its own base, those on 5T at `c462d87`'s terms and
those on 6T or 7T at `f0bf538`'s, which `662be89` and `6bf9f77` keep, and
`b3228bb`, `e0c91bb`, `e14ada0`, `173d83c`, `ccc52b9`, `20084cd`, `2250830`,
`88d0d36`, `e0b1671`, `818311a`, `4512441`, `dab8a64` and `54e869b` keep where
no path of the
repository's root
or common directory holds a line feed (below),
as round A9 stated D7's figures
at both heads, and no figure changes its meaning (ruling A-50). No `limits` or
`budget` member is added: the stage spawns one branch child per target, so
`limits.targets` (16) caps them, and `budget.probe_timeout_seconds` (5) bounds
each. A run adds at most 81 children: 64 for the stage, 16 under `operations`
and 48 under `probes` (A-5 as amended, with ruling A-24's re-proof, one more
child per retired branch), and 17 reflog children under `probes`, one for the
repository and one per selected row. A keep the plan names spawns no stage
child, so each kept branch lowers the count by four.

The fit of `BA:729-760`, at the packet's assumed costs (150 ms per child, 0.3
s per removal, T = 16, the 50 s work deadline and the 5 s floor), on change
1's terms as PR #19 words them at `c462d87`: F = 7 (its `design.md:305` and
D14 at `:625`), E = 16 (`:596`) and five children per revalidation (its
`specs/project-clean/spec.md:826-827`). Without the
cache change and with one reflog child, target k's removal spawns after 7 +
128 + 16 + 1 + 5k probes, k - 1 removals and 4(k - 1) stage children, at
(152 + 5k) x 0.15 + 0.3(k - 1) + 0.6(k - 1) = 21.9 + 1.65k s, and its branch
child 1.05 s later (the removal, the three rescan children, the re-read's
listing and its re-proof), at 22.95 + 1.65k s. The spawn floor needs each at
or before 45 s, the spawn limit, which is the 50 s work deadline less the 5 s
removal floor, as PR #19's D14 names it at `662be89` (its
`design.md:929-931`; rulings A-40, A-42 and A-47): removals 1 to 14 spawn (the
14th at 45.0 s, on the boundary,
which change 1's inclusive test for a removal admits), branch children 1 to 13
spawn (the 13th at 44.4 s), and the 14th branch child, due at 46.05 s, cannot
start; no branch child falls on the boundary, so the branch child's strict
test changes no count here. So at the packet's costs a flagged run of 16
removes 14 worktrees and retires 13 branches; the 14th branch is `retained`
with `deadline-exceeded`, the 15th removal, due at 46.65 s, does not spawn,
the 15th and 16th targets are `not-attempted` with `deadline-exceeded`, and
the run exits 1, never unsafe (`BA:772-774`). In the worst case, when the
repository's reflog child prints a commit and 16 per-row children follow,
every time moves 2.4 s later, removals at 24.3 + 1.65k s and branch children
at 25.35 + 1.65k s: 12 removed (the 12th at 44.1 s) and 11 retired (the 11th
branch child at 43.5 s, the 12th due at 45.15 s), fewer where a row's proof
failed, whose stage then does not run and which saves 0.6 s for each later
row.

At PR #19's `6f2cb54`, its head after lane openRepoProject-2's round of
2026-10-21, change 1's terms move (reader RF's M2, derived at `1ebdd90`,
whose inputs `6f2cb54` keeps byte for byte; ruling A-37). Its head `a664799`,
after that lane's round (b), keeps every input this paragraph takes, each
checked against `6f2cb54`, while its D14, restated with the child counts
that lane openRepoProject-2 measured (its R-178), counts one more child at
plan time where the plan read `extensions.worktreeConfig` as true (ruling
A-38). Its head `9267303`, after that lane's rounds (c) and (d), keeps every
input this paragraph takes, each checked by content from `a664799` through
`2e819ad`, while its D14 states the fit on three bases, chooses none, and
gives each option of its LQ-20 on each basis (rulings A-39 and A-40). Its
head `f0bf538`, after that lane's round (e), keeps every such input and
D14's two tables, each checked by content from `9267303`, and states option
(c)'s invocation deadline and run bound (its `design.md:891-894`,
`:973-996` and `:1800-1808`; rulings A-41 and A-42). Its head `662be89`,
after that lane's round (f), changes its design, proposal and tasks only, its
spec text equal to `f0bf538`'s, and keeps every such input and D14's 150 ms
column, each checked by content from `f0bf538`, while LQ-20's step (i), which
Brett Heap chose, gives the measured costs of the two probes that task 2.1
did not measure, which move D14's measured basis (below; ruling A-47). At
`662be89`: F = 8, its row 4c added (its `design.md:335-336` and D14 at
`:903`); E and the reachability probes of its D21 at most 16 each
(`:866-867`), D21 adding one child to each revalidation (`:1028-1029`); and
six children per revalidation, seven where the plan read the repository's
`extensions.worktreeConfig` as true (its `specs/project-clean/spec.md:1026-1028`
and `specs/project-clean-review-safety/spec.md:76-77` at `f0bf538`, which
`662be89` keeps). Its head `6bf9f77`, after that lane's rounds (g), (g2) and
(g3) (`4f1c0e0` and `3dcd2d8` before it), keeps every
input this section takes and every figure of D14 and of task 2.1, each
checked by content from `662be89`: its D14 differs only in the runs per case
of step (i)'s protocol, 40 to 48 where `662be89` has 30 to 48, and its task
2.1 in that and one comma (D14 at its `:903-1067`, task 2.1's step (i) at its
`tasks.md:152-162`), and its spec text moves in the retire, batch and
classification requirements and in the project-command block, none of whose
moved lines this section takes. Every cite below of PR #19's design at
`662be89` holds at `6bf9f77` by content, D14's 8 lines later (`:335-336`
and `:441-443` 9 lines later, and the LQ-20 entry of its Open Questions,
`:1805-1866`, at `:1843-1905`, with the same options, none taken, re-wrapped),
the measured basis at `:956-969` with every figure unchanged at `:964-977`,
and every cite of its spec at `f0bf538` holds there 9 or 10 lines later, the
review-safety lines unmoved (ruling A-47). Its head `b3228bb`, after that
lane's round (h) (`e322f52`, `324192f` and
`fc95766` before it), which carries Brett Heap's R-263, keeps task 2.1 and
every figure of D14 that this section takes, each checked by content from
`6bf9f77`; its D14 (`:925-1100`) adds one paragraph, a new case: where the
path of the repository's root or of its common directory holds a line feed,
the identity probe is read one option per child, so that a revalidation
spawns nine children, ten where row 4c reads true, and the final rescan six,
and the 51 extra children before a 16th spawn cost about 1.0 s at the
identity probe's 19.7 ms, so that change 1's case still fits (ruling A-62).
Its spec states that exception beside the six and seven children
(`specs/project-clean/spec.md:1048-1056` and
`specs/project-clean-review-safety/spec.md:76-79` at `b3228bb`), so that the
counts above hold for a repository whose paths hold no line feed, which is
the case this section's figures take, and its spec also moves in the ceiling's
recovery text, gate 7's sentence on a read the deadline cuts and the
project-command block, none of whose moved lines this section takes. Every
cite below of PR #19's design at `662be89` holds at `b3228bb` by content, 30
or 41 lines later (`:335-336` and `:441-443` 16 lines later, the measured
basis at `:956-969` at `:997-1010`, every figure unchanged, and the LQ-20
entry at `:1921-1983`), task 2.1's step (i) at its `tasks.md:159-169`, and
every cite of its spec at `f0bf538` holds there 18 to 22 lines later, the
review-safety lines 2 lines later, except the two counts above. For a flagged
run whose root or common-directory path holds a line feed, D14's own pricing
of those extra children, about 1.0 s before a 16th spawn and 3 more per
target before each earlier one, puts this change's 16th removal near 40.1 s
where the plan read `extensions.worktreeConfig` as true, or 38.9 s, its
branch child near 41.2 s, or 39.9 s, still inside the spawn limit at
10,000-file removals; with 20,000-file removals it removes 14 and retires 13
where the plan read the setting as true, the 15th removal then due near
45.6 s and the 14th branch child due about 0.01 s past the limit, so that it
does not start, and 15 and 14 where it read it as false, the 15th removal near
44.4 s and the 15th target's re-read due near 45.7 s. The 13 rests on D14's
figures as rounded to 0.1 s: the 14th branch child falls within that rounding
of the spawn limit, 0.006 to 0.023 s past it for D14's 37.7 s read as 37.68
to 37.70 s, and before it below about 37.67 s, so that the case retires 13 or
14 (ruling A-63; lane openRepoProject-3's W78, LOW-4). This change's own
children are not modelled separately for that case: its stage runs no
identity probe, only its ref listings, its re-proof and its branch child, and
the figures take D14's pricing of change 1's extra children alone (ruling
A-62). Its head `e0c91bb`, after that lane's round (i) (`4204eb9`, `b60f6ac` and
`1a4785e` before it), kept D14, its line-feed paragraph included, and task 2.1
byte for byte, each checked against `b3228bb` (D14 at its `:944-1119`), so that
every figure above stands; its spec moved only in the ceiling's recovery text, a
third text for a `.git` file that the rescan cannot read (lane
openRepoProject-2's R-284, confirmed by Brett Heap (R-290)), which this section
does not take. Every cite below of PR #19's design at `662be89` held at
`e0c91bb` by content, 49 or 60 lines later (`:441-443` 27 lines later, the F = 8
sentence at `:361-363`, re-wrapped beside round (i)'s account of row 3, the
measured basis at `:1016-1029`, every figure unchanged, and the LQ-20 entry at
`:1984-2046`), task 2.1's step (i) at its `tasks.md:165-175`, and every cite of
its spec at `f0bf538` held there 28 to 32 lines later, the review-safety lines 2
lines later, except the two counts above (ruling A-64). Its head `e14ada0`,
after that lane's round (j), kept D14 and task 2.1 byte for byte, each checked
against `e0c91bb` (D14 at its `:959-1134`), so that every figure above stands;
its spec moved only in the reason clause of the ceiling's second recovery text,
now "Git refusing `git worktree remove --force` while the path remains" (lane
openRepoProject-3's W70, LOW-1), in the revalidation rule's account of the
work-tree probe, whose output it reads as one path even over several lines (lane
openRepoProject-2's R-287 and R-291), with its scenario "A work-tree probe at
revalidation", and in the project-command block's work-tree probe, with an AND
of its scenario "A linked worktree whose work tree is redirected", none of which
this section takes. Every cite below of PR #19's design at `662be89` held at
`e14ada0` by content, 64 or 75 lines later (`:441-443` 30 lines later, the F = 8
sentence at `:364-366`, the measured basis at `:1031-1044` and the LQ-20 entry
at `:2002-2064`), task 2.1's step (i) at its `tasks.md:168-178`, and every cite
of its spec at `f0bf538` held there 28 to 32 lines later, the review-safety
lines 2 or 4 lines later, except the two counts above and the revalidation
rule's sentence on the work-tree probe (ruling A-67). Its head `173d83c`, after
that lane's round (k), kept D14 and task 2.1 byte for byte, each checked against
`e14ada0` (D14 at its `:965-1140`), so that every figure above stands; its spec
moved only in the retire requirement's scenario "A removal past the hard
ceiling", in the AND for a `.git` file that the rescan cannot read, whose
recovery text is now "instead" the unread note, "whatever the rescan finds of
the registry entry", and in the THEN line of the review-safety scenario "A
work-tree probe at revalidation", which now ends "since the probe's two lines
are read as one path, which is D's", neither of which this section takes. Every
cite below of PR #19's design at `662be89` held at `173d83c` by content, 70 or
81 lines later (`:441-443` 36 lines later, the F = 8 sentence at `:371-372`,
re-wrapped beside round (k)'s account of row 3's line counts, the measured basis
at `:1037-1050` and the LQ-20 entry at `:2051-2113`), task 2.1's step (i) at its
`tasks.md:172-182`, and every cite of its spec at `f0bf538` held there 29 to 33
lines later, the review-safety lines 2 or 4 lines later, except the two counts
above and the revalidation rule's sentence on the work-tree probe (ruling A-71;
the wording of the AND under ruling A-74, lane openRepoProject-3's W89, LOW-2).
Its head `ccc52b9`, after that lane's round (l) (`d1c5343` before it), kept D14
and task 2.1 byte for byte, each checked against `173d83c` (D14 at its
`:970-1145`), so that every figure above stands; its spec moved only in an AND
of the scenario "An unreadable worktree is one row", in the requirement "Clean
reports local worktree state", which gives the preview's next steps and the
`inspection-incomplete` remedies, while a row's path could not be read, without
`git worktree prune`, each saying "so do not run git worktree prune until it
can" (lane openRepoProject-2's R-307 and R-310, which Brett Heap confirmed,
"T1-T5: yes" in lane openRepoProject-3's RULED line `d6dd6d9a8` and "R-307: yes;
R-310: yes" in lane openRepoProject-2's R-319; ruling A-77), a clause that round
(n) widens to "so do not run git worktree prune, git worktree remove or git gc
until it can", and none of which this section takes. Every cite below of
PR #19's design at `662be89` held at
`ccc52b9` by content, 75 or 86 lines later (`:441-443` 40 lines later, the F = 8
sentence at `:375-376`, the measured basis at `:1042-1055` and the LQ-20 entry
at `:2100-2162`), task 2.1's step (i) at its `tasks.md:176-186`, and every cite
of its spec at `f0bf538` held there 50 to 54 lines later, the review-safety
lines 2 or 4 lines later, except the two counts above and the revalidation
rule's sentence on the work-tree probe (rulings A-75 and A-76). Its head
`20084cd`, after that lane's round (m), kept D14 and task 2.1 byte for byte,
each checked against `ccc52b9` (D14 at its `:974-1149`, task 2.1 at its
`tasks.md:140-191`), so that every figure above stands; its spec moved only in
an AND of the scenario "Row cap and planning failures", in the requirement
"Clean bounds its Git work and reports omitted work", which gave the inspect-cap
refusal's remedy the clause "if a worktree's path cannot be read, do not run git
worktree prune until it can" (lane openRepoProject-2's R-320, whose texts T6 to
T8 Brett Heap confirmed, "R-320: yes" in its R-321), which round (n) widens to
"if a worktree's path cannot be read, do not run git worktree prune, git
worktree remove or git gc until it can", and which this section does not take.
Every cite below of PR #19's design at `662be89` held at `20084cd` by content,
79 or 90 lines later (`:441-443` 44 lines later, the F = 8 sentence at
`:379-380`, the measured basis at `:1046-1059` and the LQ-20 entry at
`:2123-2185`), task 2.1's step (i) at its `tasks.md:181-191`, and every cite of
its spec at `f0bf538` held there 50 to 54 lines later, the review-safety lines 2
or 4 lines later, except the two counts above and the revalidation rule's
sentence on the work-tree probe (rulings A-77 and A-78). Its head `2250830`,
after that lane's round (n) (`e6b6b16` before it), kept D14 and task 2.1 byte
for byte, each checked against `20084cd` (D14 at its `:982-1157`, task 2.1 at
its `tasks.md:146-197`), so that every figure above stands; its spec moved only
in the closing words of every no-prune warning, which now reads "so do not run
git worktree prune, git worktree remove or git gc until it can": R-284's text
(c) in the retire requirement, in its scenario "A removal past the hard ceiling"
and in the reconcilable-result requirement, T1 to T5 in "An unreadable worktree
is one row" and T8 in "Row cap and planning failures" (lane openRepoProject-2's
R-324, which Brett Heap ruled, "R-324: yes", in this lane's RULED line
`26e556b43` and lane openRepoProject-2's R-343), none of which this section
takes. Every cite below of PR #19's design at `662be89` held at `2250830` by
content, 87 or 98 lines later (`:441-443` 47 lines later, the F = 8 sentence at
`:382-383`, the measured basis at `:1054-1067` and the LQ-20 entry at
`:2150-2212`), task 2.1's step (i) at its `tasks.md:187-197`, and every cite of
its spec at `f0bf538` held there 52 to 56 lines later, the review-safety lines 2
or 4 lines later, except the two counts above and the revalidation rule's
sentence on the work-tree probe (rulings A-83 and A-84). Its head `88d0d36`,
after that lane's round (o) (lane openRepoProject-2's R-349 and R-350, on lane
openRepoProject-3's W103), kept D14 and task 2.1 byte for byte, each checked
against `2250830` (D14 at its `:984-1159`, task 2.1 at its
`tasks.md:148-199`), so that every figure above stood; its spec text was
`2250830`'s, round (o) editing four record items of its design, proposal and
tasks only. Every cite below of PR #19's design at `662be89` held at `88d0d36`
by content, 89 or 100 lines later (`:441-443` 49 lines later, the F = 8 sentence
at `:384-385`, the measured basis at `:1056-1069` and the LQ-20 entry at
`:2152-2214`), task 2.1's step (i) at its `tasks.md:189-199`, and every cite of
its spec at `f0bf538` held there 52 to 56 lines later, the review-safety lines
2 or 4 lines later, except the two counts above and the revalidation rule's
sentence on the work-tree probe (ruling A-86). Its head `e0b1671`, after that
lane's round (p) (Brett Heap's R-365 and R-377), kept D14 byte for byte, and
its task 2.1 gained only the link to the PR #11 comment that holds task 2.1's
results, no figure moving; its spec moved in the retire and reconcilable-result
requirements, for R-365's form of the ceiling's second recovery text beside a
row whose path could not be read, and in the retire requirement's sentence on
the `delete-branch` action's refusals. Its head `818311a`, after that lane's
round (q), accepted under lane openRepoProject-2's R-389, which builds Brett
Heap's "yes, recommended for Q1-Q9" (R-380) and T9's project-command clause,
kept D14 byte for byte, checked against `88d0d36` (D14 at its `:1064-1239`),
and task 2.1 as `e0b1671` has it (its `tasks.md:161-214`), so that every
figure above stood; its spec moved in the classification, retire, batch,
bounds, reconcilable-result and review hand-off requirements, in the
review-safety preservation and revalidation requirements and in the
project-command block, among them Q1's `core.ignoreCase=false` pin on every
status, hidden-state and removal child, Q2's widened `contains-submodule` and
`registration-mismatch` gates, Q3 (a)'s by-hand recovery text in place of
R-365's, Q3 (b)'s dry-run warning in the row-cap refusal's remedy, Q8's
warned-probe rule and T9's "Stale entries:" paragraph, none of which moved a
figure this section takes, D14 being unchanged, and none of which this
section restates (the proposal's A-50 note, block by block); every cite
below of PR #19's design at `662be89` held at `818311a` by content, D14's 169
or 180 lines later (`:441-443` 75 lines later, the F = 8 sentence at
`:410-411`, the measured basis at `:1136-1149` and the LQ-20 entry at
`:2362-2424`), task 2.1's step (i) at its `tasks.md:204-214`, its first line
then also giving the PR #11 link, and every cite of its spec at `f0bf538`
held there 71 to 78 lines later, the review-safety lines 24 or 26 lines
later, except the two counts above and the revalidation rule's sentence on
the work-tree probe (ruling A-106; round A26 scopes "169 or 180 lines later"
to D14, the only place it held, under lane openRepoProject-3's W131, LOW-4).
Its head `4512441`, after that lane's round (r), accepted under lane
openRepoProject-2's R-396, kept D14 byte for byte, checked against `818311a`
(D14 at its `:1085-1260`), and task 2.1 as `818311a` has it (its
`tasks.md:167-220`), so that every figure above stood; its spec moved in the
review-safety revalidation requirement, Q2 (2)'s `lstat` of `<dir>/.git` re-run
there and a `.git` entry named in `contains-submodule`'s reason, in the
classification requirement, which then stated clean's four `stale-worktree`
recommendations, in the retire requirement's scenario "A removal past the hard
ceiling", one AND's last clause reworded, and in the project-command block,
whose Q8 sentence then held "under Git's default `core.warnAmbiguousRefs`",
none of which moved a figure this section takes and none of which this section
restates; every cite below of PR #19's design at `662be89` held at `4512441` by
content, D14's 190 or 201 lines later (`:441-443` 86 lines later, the F = 8
sentence at `:421-422`, the measured basis at `:1157-1170` and the LQ-20 entry
at `:2444-2506`), task 2.1's step (i) at its `tasks.md:210-220`, and every cite
of its spec at `f0bf538` held there 109 to 116 lines later, the review-safety
lines 25 or 27 lines later, except the two counts above and the revalidation
rule's sentence on the work-tree probe (ruling A-110). Its round (s), which
round A26 named as owed and as able to touch its D7 revalidation phrase, its
D18 and its Open Questions M1 and M3, came at `dab8a64`, accepted under lane
openRepoProject-2's R-412, and touched all four: it kept D14 byte for byte,
checked against `4512441` (D14 at its `:1104-1279`), and task 2.1 as `4512441`
has it (its `tasks.md:171-224`); its spec moved in the classification
requirement, which also states the main worktree's own recommendation, "The
main worktree is never removed by project clean.", which is no `stale-worktree`
text, with the scenario "The main worktree's recommendation", and in the batch
requirement's `contains-submodule` gate and the review-safety preservation and
revalidation requirements, where a directory whose `.git` entry counts is now
one that holds an index entry directly or below it, other than the worktree's
own top level, the gate's `lstat`s being all of a row's in one filesystem call
under one budget; and its design moved in D7, which says that the widenings of
Q2 (1) and Q9 (b) are `clean`'s classifications, the other commands reporting
such a row as the baseline does, puts all of a row's `lstat`s in one call and
says that on a warm cache they add about 0.25 s to a run at 50,000 tracked
directories (lane openRepoProject-2's R-406, which PR #19 writes "the lead's
R-406", its `design.md:612` at `54e869b`; lane openRepoProject-3's W153,
observation 2), a cost that neither D14 nor this section counts, and
rewords its revalidation phrase, "an entry found there is a new
`.git` entry, which refuses the target as `contains-submodule`", one call for
the target as at planning; in D18, which states the main worktree's
recommendation; and in M1's labels and closing sentence and M3's lead-in, none
of which moves a figure this section takes, D14 being unchanged, and none of
which this section restates. At `54e869b`, after that lane's round (t),
accepted under lane openRepoProject-2's R-415, PR #19 keeps D14 byte for
byte, checked against `dab8a64` (D14 at its `:1107-1282`), and task 2.1 as
`4512441` has it (its `tasks.md:176-229`), and at `1476110`, after its round
(u), it keeps both as `54e869b` has them (D14 at its `:1131-1306`, task 2.1
at its `tasks.md:182-235`; ruling A-134), so that every figure above
stands; round (t) builds Brett Heap's "yes, recommended for M1 and M3" (R-413),
each question's (a), so that M1 and M3 are ruled and leave its Open Questions:
by M1 (a), where no row's path is unread, `project status`, `project doctor`
and `project update` keep the baseline's stale recommendation without Q3 (b)'s
warning, T9's lines and the project-command delta staying unchanged, and by M3
(a) a `registration-mismatch` row whose path is, or holds, the main worktree,
the common directory or another worktree, or which shares its path with another
row, has its own next step, which its D18 states, with the scenario "A worktree
whose path holds the main worktree" in "Clean reports local worktree state",
the preservation requirement's `registration-mismatch` sentence staying as it
was; none of this moves a figure this section takes, and this section restates
none of it. Every cite below of PR #19's design at `662be89` holds at `54e869b`
by content, D14's 212 or 223 lines later (`:441-443` 91 lines later, the F = 8
sentence at `:426-427`, the measured basis at `:1179-1192` and the LQ-20 entry
at `:2448-2510`), task 2.1's step (i) at its `tasks.md:219-229`, and every cite
of its spec at `f0bf538` holds there 150 to 159 lines later, the review-safety
lines 27 or 29 lines later, except the two counts above and the revalidation
rule's sentence on the work-tree probe (ruling A-119).

- Where the plan read `extensions.worktreeConfig` as false, six children per
  target, on D14's 150 ms basis at `662be89` (its `design.md:910`, the row
  for row 4c false), target k's removal spawns after k - 1 removals and their
  4(k - 1) stage children, at (169 + 6k) x 0.15 + 0.3(k - 1) + 0.6(k - 1) =
  24.45 + 1.8k s, and its branch child at 25.5 + 1.8k s: removals 1 to 11
  spawn (the 11th at 44.25 s) and branch children 1 to 10 (the 10th at 43.5
  s); the 11th branch child, due at 45.3 s, cannot start, and the 12th
  removal, due at 46.05 s, does not spawn. At the packet's 150 ms per child
  (D14's 150 ms basis) a flagged run of 16 then removes 11 worktrees and
  retires 10 branches, at `54e869b`, `dab8a64`, `4512441`, `818311a`,
  `e0b1671`, `88d0d36`, `2250830`,
  `20084cd`, `ccc52b9`, `173d83c`, `e14ada0`, `e0c91bb`, `b3228bb`, `6bf9f77`
  and `662be89` as at `f0bf538`,
  `9267303`, `2e819ad`, `a664799` and `6f2cb54`, where `c462d87` gives 14 and
  13; without the flag all 16 removals spawn, the 16th at 44.1 s, as D14 says
  (its `:910` and `:931-932`).
- Where the plan read `extensions.worktreeConfig` as true, seven children per
  target, D14 at `662be89`, as at `f0bf538`, also counts the
  effective-work-tree probe at plan time on each linked row (its
  `design.md:920-922`; the probe at `:441-443`), so that on its 150 ms basis
  its planning term is 39 + 2R children for R rows and at 128 rows the first
  removal would spawn at 45.3 s: nothing is removed, every target is
  `not-attempted` with `deadline-exceeded`, and the run exits 1, never unsafe
  (its `:911` and `:932-938`). A flagged run there
  adds the reflog child, so that, with the 127 linked rows' probes, target
  k's removal spawns after k - 1 removals and their 4(k - 1) stage children,
  at (296 + 7k) x 0.15 + 0.3(k - 1) + 0.6(k - 1) = 43.5 + 1.95k s: the first
  is due at 45.45 s, past the spawn limit, so that at the packet's 150 ms per
  child (D14's 150 ms basis) a flagged run of 16 at 128 rows removes 0
  worktrees and retires 0 branches.

D14 at `f0bf538` stated that case on three bases and chose none, because task
2.1 had measured neither LQ-11's per-row `rev-parse --show-toplevel` nor
LQ-13's `rev-list` (rulings A-39 to A-42, lane openRepoProject-3's W35,
MEDIUM-1). Brett Heap ruled PR #19's LQ-20 on 2026-10-22, choosing its step
(i), to measure those two probes first, and D14 at `662be89` gives that
measurement, unchanged at `88d0d36`, `e0b1671`, `818311a`, `4512441`,
`dab8a64` and `54e869b`, on task 2.1's protocol in the same
container: the work-tree probe's warm median 5.8 ms, 8.7 ms with the 1.5
margin, and the `rev-list`'s 106.9 ms, 160.3 ms with the margin, row 4c's
read keeping the identity probe's 19.7 ms (its `design.md:956-965` and
`tasks.md:145-155` at `662be89`, `:1056-1065` and `:189-199` at `88d0d36`,
`:1136-1145` and `:204-214` at `818311a`, `:1157-1166` and `:210-220` at
`4512441`, `:1179-1188` and `:219-229` at `54e869b`;
lane openRepoProject-2's R-236; ruling A-47). On each basis this
change's figure for a flagged run of 16 at 128 rows is change 1's with this
change's own children added by this section's method: before target k's removal
its 4(k - 1) stage children and the reflog child, 61 before the 16th (60 for
the 15 earlier targets, and the reflog child), and each branch child after its
removal, the rescan's three children, the re-read's listing and the re-proof.
Task 2.1 measured none of this change's children, so each figure names the cost
it gives them: 150 ms, or task 2.1's average of about 0.063 s per child (23.6 s
less its 15 removals at 0.604 s, over its 231 children; lane
openRepoProject-3's W40, MEDIUM-2, which corrects round A11's 0.0827 s, taken
with those removals at 0.3 s).

- On D14's 150 ms basis, every child at 150 ms: change 1 alone removes none,
  its first removal due at 45.3 s, and a flagged run removes 0 and retires
  0, as above.
- On the measured basis, D5's, each child at task 2.1's warm median times
  1.5, a removal at its 0.604 s, or 1.118 s at 20,000 files, and the two
  probes that step (i) measured at its costs, the per-row `rev-parse
  --show-toplevel` at 8.7 ms and LQ-13's `rev-list` at 160.3 ms, row 4c's
  read at the identity probe's 19.7 ms (its `:948-969` at `662be89`, its
  figures unchanged at `88d0d36`, `818311a`, `4512441` and `54e869b`):
  change 1 alone removes all 16, the first at 14.55 s and the 16th at
  30.0 s with 20.0 s left, or at 37.7 s with 20,000-file removals, so that
  the case passes (its `:992`). With this change's children at 150 ms each,
  as the paragraph below on change 1's measured costs takes them, a flagged
  run's 16th removal moves to about 39.15 s, 61 x 0.15 s after D14's 30.0 s
  (39.12 s from its unrounded 29.97 s), and its branch child to 40.18 s,
  after the removal's 0.604 s, the rescan's three children and two of this
  change's: all 16 are removed and retired, and so they are with 17 reflog
  children, the 16th branch child at 42.58 s. With 20,000-file removals,
  change 1's 16th at 37.7 s, 15 are removed (the 15th at 44.69 s, the 16th
  due at 46.83 s) and 14 retired (the 14th branch child at 44.12 s), the 15th
  target's re-read, due at 45.96 s, being refused, so that its branch is
  `retained` with `deadline-exceeded`, exit 1, never unsafe, its line naming
  the reflog inspection before the retry (D8; ruling A-55); 14 and 13 with
  17 reflog children. With this change's children at task 2.1's average all
  16 are removed and retired, the 16th branch child at 34.70 s, or at
  42.92 s with 20,000-file removals. At `f0bf538`, with the stand-ins that
  step (i) replaced, the per-row probe at the identity probe's 19.7 ms and
  the `rev-list` at the full ref listing's 359.7 ms, change 1 alone removed
  all 16, the 16th at 37.9 s, or 15 with 20,000-file removals, and a flagged
  run removed and retired 14 and 14 with this change's children at 150 ms,
  or 11 and 11 with 20,000-file removals, and 16 and 16 at task 2.1's
  average, or 13 and 13 (rounds A11 and A12; reader RH's item 6).
- On the mixed basis as D14 first stated it and keeps it in its table, task
  2.1's measured costs for the children it measured and 150 ms for each child
  added since (its `:973-978` at `662be89`): change 1
  alone removes 11, the 12th due at 45.3 s and the 16th at 50.0 s, 176
  children having been added before the 16th to task 2.1's 231. This
  change's 61 are added children too, at 150 ms by that basis, 237 before
  the 16th, which would be due at about 59.15 s: a flagged run removes 7
  (the 7th at 43.29 s, the 8th due at 45.05 s) and retires 7 (the 7th branch
  child at 44.35 s). Restated after step (i), with the two kinds of child
  that it measured at their costs and only row 4c's read at 150 ms, change 1
  alone removes all 16, the 16th at 30.1 s, or 37.8 s with 20,000-file
  removals (its `:978-981`), and a flagged run, this change's children at
  150 ms by that basis, removes and retires all 16, the 16th branch child at
  40.31 s, or 15 and 14 with 20,000-file removals.

LQ-20 is therefore resolved, and none of its options is taken: the case
passes on the measured basis, D5's as ratified, and PR #19 keeps its options
(a) to (d), each marked not taken, and D14's option table as the record of
what was costed before step (i) (its `design.md:996-1002` and Open Questions
`:1805-1866` at `662be89`). This section's table of a flagged run under each
option on each basis, and its statement of option (c)'s work deadline,
invocation deadline and run bound for a flagged run, are withdrawn with them
(ruling A-47; reader RH's item 6): no option is a choice before Brett Heap,
and the table's measured column stood on the stand-ins that step (i)
replaced. They stay in this change's history, at `36adbc0` and earlier, and
in the rows of rounds A11 to A13. What the measured basis leaves to A-9 is
this change's own children, which task 2.1 did not measure: where change 1
alone takes all 16, a flagged run of 16 at 128 rows takes all 16 at the
10,000-file removal that the cap test uses, with this change's children at
150 ms or at task 2.1's average, whether the plan read
`extensions.worktreeConfig` as true (above) or as false (below), and falls
short only at the 20,000-file removal of D14's sensitivity case with them at
150 ms, 15 removed and 14 retired, or 14 and 13 with 17 reflog children, a
target that the spawn limit stops being `not-attempted` with
`deadline-exceeded` and a branch whose stage it stops `retained` with
`deadline-exceeded`, exit 1, never unsafe, the next run taking them. A-9
therefore no longer waited on LQ-20, and its question for Brett Heap was about
two cases only: the packet's flat 150 ms per child, at which a flagged run
falls short in every case of this section, and the 20,000-file removal with
this change's children at 150 ms (proposal, Open Questions); he ruled it as
recommended, `limits.targets` 16 for every run (ruling A-127). Lane
openRepoProject-3's W62 reached the same sums by this section's method,
adding the 61 children to D14's rounded 30.0 s and 28.7 s: the 16th removal
at about 39.15 s and 37.85 s, where the figures above take D14's unrounded
29.97 s and 28.73 s.

The other figures of this section, the worst case of the reflog proof, the
joint fit with the cache change, change 1's measured fit as its task 2.1 gives
it and a lower target cap's arithmetic, stand on change 1's terms at `c462d87`.
This change ratifies its two blocks on PR #19's text only as written at
`c462d87` (`tasks.md` 1.6), PR #19's later heads do not block it, and the
figures meet PR #19's final text at the re-base (`tasks.md` 2.2).

Where the plan read `extensions.worktreeConfig` as false, change 1's measured
costs on its terms at `c462d87` (CAS `tasks.md` 2.1: the 16th removal spawning
at 23.6 s with 26.4 s left), with the 60 stage children before the 16th
removal, four for each earlier target, even at 150 ms each, and one reflog
child, move it to 23.6 + 9.0 + 0.15 = about 32.75 s, and 17 reflog children to
about 35.15 s, its branch child following within about a second, inside the
spawn limit. That account is `c462d87`'s: task 2.1's 23.6 s predates LQ-11's
and LQ-13's children (lane openRepoProject-3's W40, MEDIUM-1; ruling A-42).
Where the plan read it as false, change 1's measured fit at `662be89` is
D14's measured basis with step (i)'s costs: the 16th removal at 28.7 s with
21.3 s left, or 36.4 s with 20,000-file removals (its `design.md:991`; "task
2.1's 26.4 s was the margin before LQ-11 and LQ-13 added children", its
`:1032-1033`). On it a flagged run of 16 at 128 rows removes and retires all
16 with this change's children at 150 ms, the 16th removal at 37.88 s and
its branch child at 38.94 s, and all 16 with 17 reflog children, the 16th
branch child at 41.34 s. With 20,000-file removals it removes 15 and retires
14 (the 15th removal at 43.46 s, the 16th due at 45.59 s): the 15th target's
re-read starts at 44.73 s and its re-proof at 44.88 s, whose budget the work
deadline ends at 45.0 s, so that its branch is `retained` with
`deadline-exceeded`, exit 1, never unsafe, its line naming the reflog
inspection before the retry (D8; ruling A-53); 14 and 13 with 17 reflog
children. With this change's children at task 2.1's average of about 0.063 s
it removes and retires all 16, the 16th branch child at 33.45 s, or 41.68 s
with 20,000-file removals. At `f0bf538`, with the stand-ins that step (i)
replaced, change 1's 16th removal was at 35.1 s, or 42.8 s with 20,000-file
removals, and a flagged run removed 16 and retired 15 with this change's
children at 150 ms, the 16th removal at 44.26 s and the 16th branch child due
at 45.32 s, the stage's re-read refused first at 45.02 s, since it starts
only while less than 45 s have run, 15 and 14 with 17 reflog children, 13
and 12 with 20,000-file removals, and 16 and 16 at task 2.1's average, or 15
and 14 with 20,000-file removals (rounds A12 and A13). Change 1 kept its caps
on its measured fit, and this design does the same on every account: no cap
changes. Where the plan read `extensions.worktreeConfig` as true, the case
passes on PR #19's measured basis at `662be89` (above), so that A-9 there no
longer waits on LQ-20. Wherever a run falls short, at the assumed
costs or on D14's bases, a target the spawn limit stops is `not-attempted`
with `deadline-exceeded` and a branch whose stage it stops, or whose branch
child it keeps from starting, `retained` with `deadline-exceeded` (the reader
RA2's N2: the deadline never stops a branch child once spawned), exit 1; the
next run takes their worktrees, and such a branch keeps `delete-branch` as its
retry, after the reflog inspection that
its line names wherever its stage did not re-prove the reflog (Risks; D8;
rulings A-53 and A-55).

With `add-project-clean-cache-disposal` archived first (L-5), its 16 cache
enumerations join the plan, and every time moves 2.4 s later again: target k's
removal would spawn at 24.3 + 1.65k s with one reflog child. The cache change's
filesystem time is added on top, with the inputs of the lane's ruling B-25 as
ruling A-23 gives them, unchanged for ordinary trees at that change's
`e1049b2`: the plan-time walk, at most 8,192 recorded objects and about 9,000
calls, about 2 s through one worker per stage and about 5.6 s at a thread per
call; and the cache stages, at most about 8,500 calls in a run, about 2 s
through a worker and about 5.3 s at a thread per call. Both are taken whole
before the first removal, 4 s through a worker and 10.9 s at a thread per
call. That is a bound, not an order a run can take, since each cache stage
runs just before its own target's removal (lane openRepoProject-3's delta
read, D3(i)); the last bullet below gives the worst order a run can take.

- Through one worker per stage, target k's removal spawns at 24.3 + 4 + 1.65k
  = 28.3 + 1.65k s and its branch child at 29.35 + 1.65k s with one reflog
  child: removals 1 to 10 spawn (the 10th at 44.8 s) and branch children 1 to
  9 (the 9th at 44.2 s); the 10th branch child, due at 45.85 s, cannot start,
  so the 10th branch is `retained` with `deadline-exceeded`, and the 11th
  removal, due at 46.45 s, does not spawn. In the worst case of 17 reflog
  children, at 30.7 + 1.65k s, 8 removals spawn (the 8th at 43.9 s) and 8
  branch children (the 8th at 44.95 s, 0.05 s inside the spawn limit).
- At a thread per call, at 24.3 + 10.9 + 1.65k = 35.2 + 1.65k s, 5 removals
  spawn (the 5th at 43.45 s) and 5 branch children (the 5th at 44.5 s); in the
  worst case, at 37.6 + 1.65k s, 4 removals (the 4th at 44.2 s) and 3 branch
  children (the 3rd at 43.6 s, the 4th due at 45.25 s).
- The worst order a run can take puts first the 8 cache targets that the
  cache change's totals select (its D4), each stage spending an eighth of the
  stage time just before its own removal. At a thread per call target k's
  removal, for k up to 8, then spawns at 24.3 + 5.6 + 1.65k + 5.3k/8 = 29.9 +
  2.3125k s with one reflog child: 6 removals spawn (the 6th at 43.8 s) and 6
  branch children (the 6th at 44.8 s), the 7th removal due at 46.1 s; with 17
  reflog children, at 32.3 + 2.3125k s, 5 and 5 (the 5th removal at 43.9 s,
  its branch child at 44.9 s). Through a worker the same order gives the counts
  of the first bullet, since by the 8th target the stages have spent their
  whole 2 s.

On change 1's measured costs at `c462d87`, the 32.75 s account above, the 16th
removal then spawns near 32.75 + 2.4 + 4 = 39.15 s through a worker with one
reflog child and near 41.55 s with 17, and all 16 fit, each branch child
within about a second. At a thread per call it
is due near 32.75 + 2.4 + 10.9 = 46.05 s with one reflog child and near 48.45
s with 17, past the spawn limit either way, so at least the 16th target is
`not-attempted` with `deadline-exceeded`, exit 1. These figures take the 16
enumerations at the packet's 150 ms a child, 2.4 s, as they take the stage and
reflog children, while the cache change gives at most about 3.7 s for them at
change 1's measured costs (its D4 at `e1049b2`); at 3.7 s each figure moves
1.3 s later, to 40.45 s and 42.85 s through a worker, where all 16 still fit,
and 47.35 s and 49.75 s at a thread per call, and no conclusion changes (lane
openRepoProject-3's delta read, D2). On D14's measured basis at `662be89`,
with step (i)'s costs, where the plan read `extensions.worktreeConfig` as
false, a flagged run retires all 16 without the cache change (above), and
the same additions, the 16 enumerations at 2.4 s and the filesystem time
taken whole before the first removal, leave 16 removed and 15 retired
through a worker (the 16th removal at 44.28 s, its stage's re-read refused
first at 45.04 s), 14 and 14 with 17 reflog children (the 15th removal due
at 45.06 s), and at least 12 and 11, or 10 and 10, at a thread per call. At
the cache change's own 3.7 s for the enumerations, with 7.7 s through a
worker and 14.6 s at a thread per call before the first removal, the same
bound leaves 15 removed and 14 retired through a worker (the 15th target's
re-read starting at 44.72 s and its re-proof at 44.87 s, whose budget the
work deadline ends, so that its line names the reflog inspection; ruling
A-53), 14 and 13 with 17 reflog children, and at least 11 and 10, or 9 and
9, at a thread per call; the worst order a run can take gives the same
pairs, every stop falling after the 8th target (ruling A-47). At `f0bf538`,
with the stand-ins that step (i) replaced, the same additions left 12
removed and 12 retired through a worker (the 13th removal due at 45.20 s),
11 and 10 with 17 reflog children, and at least 9 and 8, or 7 and 7, at a
thread per call (ruling A-42), and at the cache change's own 3.7 s 12 and 11
through a worker (the 12th branch child due at 45.74 s, its re-read refused
first at 45.44 s), 10 and 10 with 17 reflog children, and at least 8 and 7,
or 7 and 6, at a thread per call (ruling A-44, lane openRepoProject-3's W46,
LOW-2). Where the cache change's fit sentence counts
children, as it read at `e1049b2` ("at most 250 Git children besides the 16
removals, about 42.3 s") and as it reads at `69cb7a1` ("at most 283 Git
children besides the 16 removals where the plan read the repository's
`extensions.worktreeConfig` as false, about 47.3 s on the packet's basis of 150
ms per child and 0.3 s per removal"), a count which the flag's up to 81 more
children make false, the re-based block scopes that sentence, as it then reads,
to runs without the flag, and so does any restatement the cache change makes of
it, under its rulings B-25, B-54, B-55, B-57 and B-59 or a later one, when this
change re-bases on it (ruling A-50; reader RH's L1).

The cache change's worst shapes at `e1049b2`, the walk where every recorded
object is a directory (about 32,800 calls, 7.3 s through one worker and 20.4 s
at a thread per call) and the deep chains (up to 43,947 opens a pass for one
target), lie outside this joint fit, which takes that change's inputs for
ordinary trees, and stay under its `cache_opens` Open Question before Brett
Heap (ruling A-25) and under its caps question, B-3/CD-6, which he ruled as
recommended at 2026-10-31T17:58:12Z, `limits.targets` staying 16, to be
measured by that change's task 2.3 (lane openRepoProject-3's ledger row
27-05; this lane's RULED line, `lanes/log/openRepoProject-5.md:179`; rulings
B-149, A-129 and A-132).

So at the packet's 150 ms model a flagged run with cache disposal brings 9 of
its 16 targets through their stage before the spawn limit, 8 in the worst case
of the reflog proof, through one worker per stage, and at least 5, or 3, at a
thread per call, 6, or 5, in the worst order a run can take; change 1's own
deadline rule makes the rest `not-attempted` with `deadline-exceeded`, the run
exits 1, and the next run takes them, never unsafe (`BA:772-774`). On change
1's measured costs at `c462d87` all 16 fit through a worker, and at a thread
per call at least the 16th target is deferred, with one reflog child as in the
worst case; on D14's measured basis at `662be89`, with the enumerations at
2.4 s, 16 are removed and 15 retired through a worker, and at least 12 and 11
at a thread per call, and at the cache change's own 3.7 s for them 15 and 14
through a worker, and at least 11 and 10 at a thread per call, where
`f0bf538`'s stand-ins gave 12 and 12, 9 and 8, 12 and 11, and 8 and 7.
`limits.targets` stays 16 (A-9). The alternative, a lower
target cap under the flag, would be 8 by the packet's rule (`BA:729-735`),
since the last of T such targets then spawns at about (136 + 7T) x 0.15 +
0.3(T - 1) + 0.6(T - 1) = 19.5 + 1.95T s before the cache change's filesystem
time, 35.1 s for 8 and 50.7 s for 16; with that time, 8 still fits through one
worker per stage (39.1 s) but not at a thread per call (46.0 s). It is
rejected because the cap is applied by the `deferred-target-cap` gate, so the
flag would change the selection as well as the digest, and because a smaller
cap only splits across runs the work that the deadline already splits safely.
The proposal put the choice to Brett Heap, who ruled it as recommended, keep
16 (Open Questions; ruling A-127).

### D8. What the person sees (A-6, A-7, A-19, P-2)

All new text is ASCII, with `ROOT`, `PATH`, `PATH2`, `PATH3` (a linked
worktree that holds the merge target, in a holder line), `BRANCH`, `BRANCH2`,
`SHA`, `SHA2` (the head the re-read found, the head the post-check found in
the moved line, or, where no re-read ran, the reconciliation record's
`branch_sha`; the reader RA2's L5), `TARGET_SHA` (the merge target's SHA),
`MERGE_TARGET`, `COMMON_DIR` (the plan's `repository.common_dir`, an absolute
path), `N`, `M`, `R`, `K`, `G`, `U` and `REASON` substituted, and the tests
pin it. Paths, and
branch and
merge-target names, follow change 1's path rule (`CAS/pc:1061-1066`; ruling
A-22(b), Codex's P2 on `785a45e`): verbatim in prose and with POSIX shell
quoting in commands, a word such as `refs/heads/BRANCH` or `--branch=BRANCH`
quoted as one word, and the `$'...'` form in prose and commands alike for a
name that holds a code point to escape or an undecodable byte. Git accepts a
branch named `topic;id`, so an unquoted retry would run `id` (Context). In
every `project` command printed, a name that begins with `-` is passed as
`--branch=BRANCH`, which argparse reads as the value where `--branch -f` reads
as a missing one (the lead's F-2). Change 1's `delete-branch` action, as
`project` builds it at main, passes the name to Git with no `--`, so Git reads
such a name as an option and the retry fails (Context; lane
openRepoProject-3's delta read, D5): whether that action passes it after `--`
is change 1's question, carried as a Dependency (proposal, Dependencies and
Sequencing), and this change prints the retry that action is given. RETRY
below is `project clean ROOT --apply --action delete-branch --branch BRANCH`,
or `--branch=BRANCH` for such a name. The retry for such a name therefore
depends on change 1's `delete-branch` putting `--` before the name, and feature
004 at `e69f6ef` lacks it: its `delete-branch` still runs `git branch -d
<branch>` with no `--` (`project:6487`), so that `--branch=-f` reaches Git as
`git branch -d -f`, which answers "branch name required", exit 128, and leaves
the branch, where `branch -d -- -f` deletes it, exit 0 (lane
openRepoProject-3's W52, F-4, reproduced there on Git 2.43.0 and on the 2.36.6
floor; ruling A-52). That item is closed (ruling A-100; lane
openRepoProject-3's W120, L-2, and the reader RE's RE23-2): feature 004 at
`904aefc` runs `git -C ROOT branch -d -- BRANCH` (`project:7367`; the reader
RN's RN-3; ruling A-131), and PR #19's
D18 records it at `88d0d36`, "feature 004 runs it as `git -C ROOT branch -d --
BRANCH`, the `--` ending the options, so that a branch whose name begins with
`-` is deleted rather than read as an option (W52 F-4, R-259)" (its
`design.md:1436-1438`, the same sentence at `:1568-1570` at `818311a` and at
`:1598-1600` at `4512441` and `:1652-1654` at `54e869b`); W120
ran the printed retry `--branch=-f` against feature 004 at `f3724fc` on
Git 2.43.0 and 2.36.6, and it deleted the branch, exit 0. The departure rests on
lane openRepoProject-2's R-259, for Brett Heap's yes or no; if he declines, the
`--` leaves that action and such a retry fails again as above. The printed
retry text is unchanged, the spec's sentence on it being conditional. RE-4 and
RE-5 stay for the alignment with feature 004, RE-7 being superseded by RE2-2,
which the Migration Plan's step 4 now applies, and RE-8 holding for PR #29
alone. Without the flag every line is change 1's.

A command printed in the `$'...'` form needs a shell that implements that
form, bash, zsh, ksh93 or a POSIX.1-2024 shell, and, for its `\u` and `\U`
escapes, a UTF-8 locale: dash, Ubuntu's `/bin/sh`, lacks the form, and in the
C locale bash and zsh can pass such an escape as text, refuse the line, or
drop the code point, which names another branch (Context). Change 1's path
rule, whose form this is, shares the limitation, as feature 004 records it
(lane openRepoProject-2's R-60). The note, and the literal of the quoting
scenario in the spec delta, follow change 1's command form as ratified:
whether that form changes is lane openRepoProject-2's LQ-8, with Brett Heap,
and this change takes no side on it (ruling A-29, lane openRepoProject-3's
delta read of `9b67e8c`, L2). This is a documentation note, made here and
in the README's "Clean up Git worktrees" (`tasks.md`, Speckit Handoff), and
no printed line carries it: the lines stay in change 1's form (ruling A-28
as amended, Codex's P2 on `9ff8202`).

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
- Summary, on every apply result under the flag: `Removed N; their branches
  retired: R; retained: K`, "their" saying that R and K count the removed
  worktrees' branches, not those that a stop block's retained list also
  names (the reader RA2's L6), with `; already gone: G` when G is above 0 and
  `; unconfirmed: U` when U is above 0, so that R, K, G and U add up to the
  distinct branches of the removed targets, U counting a null `stage` (ruling
  A-31, RA's MEDIUM-3); then one line per such branch, a shared branch at its
  last holder:
  - `Retired BRANCH (was SHA); restore: git -C ROOT branch BRANCH SHA`, so
    that the restore works from any directory (Codex's P2 on `785a45e`), or,
    for a name that `git branch` refuses to create, one that begins with `-`
    or that equals `HEAD` (ruling A-27, Codex's P2 on `9ff8202`), `restore:
    git -C ROOT update-ref refs/heads/BRANCH SHA ''`: the naive line for `-f`,
    `git branch -f SHA`, creates a branch named after the SHA, and `git branch
    HEAD SHA` refuses (Context); for `HEAD` the form is only defensive under
    either setting of Git's `core.warnAmbiguousRefs`: under its default every
    status probe of a repository that holds `refs/heads/HEAD` exits 0 and warns
    `refname 'HEAD' is ambiguous.` (Context, round A25), which PR #19's
    warned-probe rule, Brett Heap's yes to Q8, makes a failed probe, so that
    every row is `inspection-error` and no run retires such a branch (its
    `specs/project-command/spec.md:265-271` at `4512441` and `54e869b`,
    which round (r) qualifies: "so, under Git's default
    `core.warnAmbiguousRefs`, a
    repository holding `refs/heads/HEAD`, for which Git warns
    `refname 'HEAD' is ambiguous.` in every status probe, has every row
    `inspection-error`"; the reader RE's RE2-1; ruling A-106); with that
    setting false, in the repository's configuration or the user's, which no
    pin of PR #19 overrides, the probe exits 0 with nothing on standard
    error, so that no row is `inspection-error` on that account (Context,
    round A26; lane openRepoProject-3's W131, LOW-3; PR #19's
    `design.md:181-191` at `4512441` and `:186-196` at `54e869b`, which adds
    no pin for it; ruling A-110), but the row of the worktree on
    `refs/heads/HEAD` is still `inspection-error`: feature 004 at `904aefc`,
    read as a check, gives it the row error `probe-failed`, "git
    for-each-ref failed: unparseable output", whatever Git prints, by lane
    openRepoProject-2's R-61 (b), because the ref listing gives a branch
    named `HEAD` the upstream and track of the command directory's current
    branch, its own only where that directory is the worktree on
    `refs/heads/HEAD` (its `project:2693-2697` and `:3487-3488`, and its
    contract `:1070-1081`; Context, round A29; lane openRepoProject-3's
    W166, OBS-1), a rule that change 1 as ratified does not state;
    so that under either setting such a row is `inspection-error` before any
    plan selects it, its plan is incomplete, and no run retires such a
    branch, the form being only defensive under both (Context, round A28;
    the reader RN's RN-1, which also finds round A26's claim in PR #19's
    `design.md:186-196` at `54e869b` and in feature 004's contract; ruling
    A-128, which narrows A-106 and A-110 and supersedes the reader RJ's F2
    here); round A26's sentence that with the setting false a run can retire
    `HEAD` and the form is the restore that works is withdrawn, and the
    quoting scenario states that no run retires `refs/heads/HEAD` under
    either setting, its row `inspection-error` and no `Retired HEAD` line
    printed;
    followed, for each local branch BRANCH2 that
    the run did not retire and whose configured upstream the plan's ref
    listing gives as `refs/heads/BRANCH`, by `Note: BRANCH2 tracks BRANCH as
    its upstream, which now reads gone; no commit is lost` (ruling A-32, RA's
    LOW-4): Git deletes such a branch without a word, the other branch's
    upstream then reads `[gone]` (Context), and under change 1's ladder an
    unmerged BRANCH2 then reads `remote-gone`; the plan's ref listing already
    carries every upstream, so the note needs no child, and restoring BRANCH
    restores the upstream. A later selected row on BRANCH2 meets one of two
    outcomes, by canonical order (the reader RJ's F3; ruling A-126): the next
    selected target, its revalidation taking its repository-wide values, the
    ref listing among them, from the rescan of BRANCH's target, read before
    BRANCH's branch stage (D2; the narrow guarantee), passes it and is
    removed, and its own stage's re-read then finds its `upstream_oid` no
    longer the plan's and retains BRANCH2 with `state-changed`, a retention
    that stops the run with exit 2; a target farther on, after another
    target whose rescan follows that stage, is refused at its revalidation
    with `state-changed`, and that refusal stands (Context, rounds A7 and
    A28). Either keeps BRANCH2 and loses no commit; a plan keep that
    foresees the first, of BRANCH or of BRANCH2, is not taken, ruling A-126
    having the two outcomes stated;
  - `BRANCH was already gone`;
  - `Unconfirmed BRANCH (was SHA); if git -C ROOT rev-parse --verify
    refs/heads/BRANCH fails, restore: ` and the restore command of the
    `Retired` line, for a null `stage`, whose branch child ran and whose
    deletion the post-check could not confirm (ruling A-31, RA's MEDIUM-3):
    the branch may be gone, so it is never a `Kept` line, never counted as
    retained and never named among a stopped run's retained branches, and the
    line carries the SHA and the restore that a deletion needs;
    `rev-parse --verify` exits 128 for a ref that is gone (Context); the line
    ends `; otherwise retry: RETRY`, for a branch that still exists, the ground
    of `unconfirmed-retirement`'s retry, its branch child having run after the
    re-proof proved the reflog (the reader RA2's L7);
  - `Kept BRANCH (head-not-merge-target); next: check out MERGE_TARGET in the
    main worktree; BRANCH's reflog was proven merged into MERGE_TARGET only at
    this run's plan; inspect git -C ROOT reflog show refs/heads/BRANCH before
    retrying: RETRY`; when the plan's registry listing shows MERGE_TARGET
    checked out in a linked worktree at PATH2, where Git refuses that
    checkout, `next: MERGE_TARGET is checked out at PATH2, so check out its tip
    TARGET_SHA detached in the main worktree; BRANCH's reflog was proven
    merged into MERGE_TARGET only at this run's plan; inspect git -C ROOT
    reflog show refs/heads/BRANCH before retrying: RETRY` (lane
    openRepoProject-3's re-read, LOW-10; Context): the plan's keep spawns no
    stage, so nothing re-proves the reflog before the retry, and the
    inspection comes after the checkout and before the retry (ruling A-60;
    lane openRepoProject-3's W69, LOW-3); the line names BRANCH, where "its"
    could be read as the main worktree's, and says what the plan found, its
    keep order testing `reflog-unmerged` first, not that the reflog was never
    proven (ruling A-63; lane openRepoProject-3's W78, LOW-2 and LOW-3);
    `git-refused` with the upstream ref absent keeps `then: RETRY` after the
    same checkout steps (below);
  - `Kept BRANCH (branch-in-use)` and `Kept BRANCH (branch-shared)`, the
    latter once, for a shared branch whose last holder PATH2 the run did not
    remove (its re-read, LOW-11), PATH2 being a selected row and so never the
    main worktree, which change 1's first gate, `main-worktree`
    (`CAS/pc:576-578`), never selects (ruling A-45), and when the run removed
    the last holder, the branch's line being that holder's. Their next step
    follows ruling A-98 (the reader RA2's HIGH L3; D4; Context, round A24),
    as ruling A-126 narrows and extends it (the reader RJ's F1, F5 and F7):
    - `next: BRANCH is checked out at PATH2, which this run selected and did
      not reach; remove it and retire BRANCH with project clean ROOT --apply
      --action remove --worktree PATH2 --retire-branches`, and no retry, only
      for a `branch-shared` last holder that the run did not reach,
      `not-attempted`, a holder the plan itself would remove, which it
      selected after every gate, its index gates included; the line once
      read `remove that worktree first`, on A-98's ground that this run read
      the holder and found none of the local state the plan protects, a read
      that is the plan's alone, the run having stopped before it revalidated
      that holder, so that the raw `git worktree remove` the line led to
      deletes with exit 0 what the holder gained since, a commit that only
      its HEAD reflog holds among it (Context, round A28); the printed
      command reads the holder again through every gate, PR #19's
      `worktree-only-commits` among them, refusing such a holder with
      `target-excluded`, and retires BRANCH only on its own plan's proof of
      the reflog, so that the line needs neither the reflog inspection nor a
      retry; that gate is PR #19's, built for Brett Heap's LQ-13 ruling, and
      change 1's text without it removes such a holder, as the raw removal
      does, its other gates still applied;
    - `next: BRANCH is checked out at PATH2; its path could not be read, so do
      not run git worktree prune, git worktree remove or git gc until it can;
      once it can, HOLD`, for a holder that is a plan row whose path could not
      be read, its `present` null, which only a single-target removal can
      meet, another row's `inspection-error` being a non-blocking omission
      there: the clause is PR #19's ruled wording of R-324 at `88d0d36`, byte
      for byte, the next step it gives an unread row of its own (its
      `specs/project-clean/spec.md:89-91`, in "An unreadable worktree is one
      row", the same lines at `818311a`, `4512441` and `54e869b`, that
      scenario unchanged, its block gaining only round (t)'s scenario after
      it), since
      `git worktree remove` of such a holder exits 0 and deletes its
      administrative directory, and `git worktree prune` would too (Context);
      round (p)'s F-1 (b) text at `e0b1671`, "inspect, then delete `<path>` by
      hand; a row's path could not be read, ...", is not taken, because its
      first clause tells the person to delete the path by hand, the removal
      this line must never advise for a live holder (ruling A-101), and nor is
      Q3 (a)'s text that supersedes it at `818311a`, "inspect, then delete
      `<path>` and its administrative directory
      `<common_dir>/worktrees/<admin_id>` by hand" (its
      `specs/project-clean/spec.md:357-359`, `:544-548` and `:1226-1228`, and
      `:395-397`, `:582-586` and `:1264-1266` at `4512441`, where round (r)
      rewords only the second site's last clause, the same text at
      `:436-438`, `:623-627` and `:1307-1309` at `54e869b`),
      which is the recovery text of a removal target whose `.git` file or
      registry entry the rescan finds gone, a worktree known not to be live,
      and here would have the person delete a live holder's path and its
      administrative directory, so that it fails A-103 (3)'s live-holder test
      and this line keeps R-324's clause (ruling A-106);
    - `next: BRANCH is checked out at PATH2; its path is or holds the main
      worktree, the common directory or another worktree, so do not delete
      it by hand or with git worktree remove; review its registration with
      git worktree list --porcelain; once it is repaired, switch that worktree
      off BRANCH by running git switch --detach there, which changes none of
      its files; BRANCH's reflog was proven merged into MERGE_TARGET only at
      this run's plan; inspect git -C ROOT reflog show refs/heads/BRANCH
      before retrying: RETRY`, for a linked holder that the plan excludes as
      `registration-mismatch` because its path is, or holds, the main
      worktree, the common directory or another worktree, or is another
      row's path, the rows that PR #19's M3 (a), Brett Heap's (R-413), gives
      their own next step, whose words this line carries from "its path is or
      holds" to "--porcelain" (its `specs/project-clean/spec.md:112-129` at
      `54e869b`, the scenario "A worktree whose path holds the main
      worktree"; the reader RJ's F7; ruling A-126); such a holder's listed
      path names another worktree, the main worktree where it shares that
      path, so that HOLD's `git -C PATH2 switch --detach`, or the
      main-worktree form, which a test by path would print, detaches the
      main worktree and frees nothing, and the retry is still refused; once
      `git worktree repair` has repaired the registration, the worktree it
      names still holds BRANCH, and the detach run there frees it, so the
      line names that detach, as the `git-refused` hint does for a holder it
      cannot name, before the reflog inspection and the retry (Context, round
      A28); the line comes before the main-worktree form for such a row;
    - `next: BRANCH is checked out at PATH2, whose path is missing; if that
      worktree still exists, moved or on a drive that is not mounted, remount
      or repair it and switch it off BRANCH by running git switch --detach
      there, which changes none of its files; otherwise STALE; BRANCH's reflog
      was proven merged into MERGE_TARGET only at this run's plan; inspect git
      -C ROOT reflog show refs/heads/BRANCH before retrying: RETRY`, for a
      holder whose path is missing, its row `stale-worktree` with `present`
      false, STALE being the recommendation that PR #19 gives a
      `stale-worktree` row, in its words, its first letter lower case and with
      no full stop (its `specs/project-clean/spec.md:216-240` at `54e869b`):
      `review and prune stale worktree metadata manually; git worktree prune
      also deletes the entry, and so the HEAD reflog, of every other worktree
      whose path is missing, one moved or on an unmounted drive included, so
      run git worktree prune --dry-run first and remount or repair any it
      lists that still exists`, or, where a row of the plan has `present`
      null, its no-prune form, `review and prune stale worktree metadata
      manually; a row's path could not be read, so do not run git worktree
      prune, git worktree remove or git gc until it can`, each with `review,
      unlock it, then prune` for a locked row, as PR #19 words its locked
      form (the reader RJ's F5; ruling A-126); HOLD's detach cannot run at a
      missing path, exit 128, Git refuses the retry while the stale entry
      holds BRANCH, and `git worktree remove` of such a holder, without
      `--force`, and `git worktree prune` both delete its administrative
      directory with exit 0, and with it the HEAD reflog, index and
      per-worktree refs of a worktree that was only moved or unmounted; a
      remount, or `git worktree repair` of a moved one, lets the detach run
      there, which keeps its files, and frees BRANCH, and for a worktree that
      is gone the prune after its dry run does (Context, round A28); the
      plan, which reads `present` false, prints this line before HOLD, never a
      detach that cannot run;
    - for the main worktree, which Git refuses to remove (`worktree remove` of
      it exits 128, "is a main working tree"), `next: BRANCH is checked out
      at PATH2, the main worktree; switch it off BRANCH, by detaching it with
      git -C PATH2 switch --detach, which changes none of its files, or by
      checking out MERGE_TARGET there; BRANCH's reflog was proven merged into
      MERGE_TARGET only at this run's plan; inspect git -C ROOT reflog show
      refs/heads/BRANCH before retrying: RETRY` (ruling A-45, Codex's P2 on
      `1bf217c`, as ruling A-103 narrows it; Context; the inspection under
      ruling A-60, since neither the plan's keep nor the rescan's re-proves
      the reflog, in ruling A-63's words), one text whether the branch's
      upstream remote-tracking ref is present or absent: the detach comes
      first, since it changes no file and Git refuses a checkout of
      MERGE_TARGET while a linked worktree holds it; the checkout it names is
      of MERGE_TARGET alone, since with that ref absent Git judges the retry
      against that worktree's `HEAD`, which another branch that lacks BRANCH
      would make the retry fail (the reader RA2's L4; Context), and a
      checkout of another branch, which A-45's text named, adds, at that
      branch's paths, the whole residual that Risks records for a checkout of
      MERGE_TARGET: the silent overwrite of an ignored file at a path that
      branch tracks, and the silent deletion of an ignored file where it needs
      a directory and of every ignored file below a path that it tracks as a
      file (Context, rounds A24, A26 and A27; ruling A-103, which drops
      "another branch there, such as"; lane openRepoProject-3's W138, OBS-1);
    - otherwise, `next: BRANCH is checked out at PATH2; HOLD`, HOLD being
      `save its own work, uncommitted, ignored or flagged assume-unchanged or
      skip-worktree, by keeping that worktree and switching it off BRANCH with
      git -C PATH2 switch --detach, which changes none of its files; BRANCH's
      reflog was proven merged into MERGE_TARGET only at this run's plan;
      inspect git -C ROOT reflog show refs/heads/BRANCH before retrying:
      RETRY`: a holder that a gate excluded for its local state, `dirty`,
      `ignored-local-files`, `hidden-local-state` or `contains-submodule`, or
      for another reason, its later gates unread, other than the two kinds of
      row above; one that `not-requested` or `deferred-target-cap` excluded
      before the index gates read its index; a last holder that the run
      refused, failed or left `unknown`; and one that appeared after the plan,
      which the stage's check 5 finds. Where the plan also finds
      `head-not-merge-target`'s condition, the upstream ref absent and the
      main worktree's `HEAD` not the merge target's SHA, the detach is
      followed by that keep's checkout, in HOLD and in the two forms above
      that name a detach run there, before `; BRANCH's reflog was proven
      merged`: `; then check out MERGE_TARGET in the main worktree`, or, where
      a linked worktree at PATH3 holds MERGE_TARGET,
      `; then, MERGE_TARGET being checked out at PATH3, check out its tip
      TARGET_SHA detached in the main worktree`, since a detached holder
      leaves the retry judged against that `HEAD` (Context, round A24). The
      detach is the only switch the line names: a checkout of another branch
      in the holder, without a word, overwrites an ignored file at a path that
      branch tracks, deletes an ignored file where it needs a directory and
      deletes every ignored file below a path that it tracks as a file, the
      whole residual that Risks records for a checkout of MERGE_TARGET, and
      refuses one whose flagged edit it would overwrite (Context, rounds A24,
      A26 and A27; lane openRepoProject-3's W138, OBS-1), and a linked holder
      cannot check out a branch that another worktree holds, the merge target
      included;
  - `Kept BRANCH (branch-changed); now at SHA2; its reflog is not proven
    merged into MERGE_TARGET; inspect it and git -C ROOT reflog show
    refs/heads/BRANCH before retrying: RETRY`, the new head and the reflog
    both to be inspected, since the re-read stopped before its re-proof, or
    no stage ran (ruling A-60), SHA2 being the re-read's `observed_sha` or,
    for a target `removed` with `branch-advanced-after-removal`, whose
    `observed_sha` is null, its reconciliation record's `branch_sha` (the
    reader RA2's L5); the same step, the moved line, takes the place of the
    line of any `retained` reason whose post-check listed the branch at a
    head other than `observed_sha`, SHA2 being that `post_check_sha`, the
    branch having moved after its re-proof (the reader RA2's L2): Git's own
    check then refused it, and the bare retry's ground, a reflog the re-proof
    proved, no longer holds, since the move wrote an entry no proof saw
    (Context, round A24), so that a later move back to the planned SHA would
    let the bare retry orphan that commit;
  - `Kept BRANCH (reflog-unmerged); its reflog is not proven merged into
    MERGE_TARGET; inspect every commit it names, the old and the new of each
    entry, as cat REFLOG prints them, before any delete-branch`, REFLOG being
    `COMMON_DIR/logs/refs/heads/BRANCH`, the file that the gate read and the
    re-proof reads again, printed by the path rule as one word (the reader
    RA2's L1): `git reflog show` prints only each entry's new commit, so that
    a commit the reflog names only as an entry's old one, the shape a default
    `git gc` leaves once `gc.reflogExpireUnreachable` drops the entry that its
    commit wrote, would go unseen and the next `delete-branch` would orphan it
    (Context, round A24). The line names the file and not the commit because
    the plan records no reflog value and the result no commit (D4, D5): naming
    the proof's commit would need a new key in `branch_plan` and in
    `branch_retirement`, which the JSON reader would need as well, and a proof
    that failed, or a re-proof that found the reflog missing, empty, at its
    bound or undecidable, has no commit to name, where the file, from the
    plan's own `repository.common_dir`, serves every case. The line is
    alike for a proof that printed a commit, one that failed
    or timed out at the plan, and a re-proof that found the reflog missing,
    empty, at its bound or undecidable (lane openRepoProject-3's delta read,
    D4; a re-proof whose read or child failed or ran past its own budget
    prints the next line, a `state-changed` one; rulings A-43 and A-44). The
    lines that name `git reflog show` for a branch whose reflog the plan proved
    keep it: a commit written after the plan is the new object of the entry
    that wrote it, which `reflog show` prints (Context, round A24), and they
    name `show` and the full ref name because `show`, `expire`, `delete` and
    `exists` are valid branch names and also `git reflog` subcommands, and
    `git reflog show HEAD` reads the main worktree's own reflog (Context);
  - `Kept BRANCH (state-changed); BRANCH's reflog was proven merged into
    MERGE_TARGET only at this run's plan; inspect git -C ROOT reflog show
    refs/heads/BRANCH before retrying: RETRY`, for a re-proof whose reflog read
    or child failed or ran past its own budget while the work deadline is not
    the limit (rulings A-43, A-44 and A-49, Codex's P2 on `7b224c7`): such a
    re-proof saw no commit, so that `reflog-unmerged` would claim one, and
    proved nothing, and RETRY is change 1's `delete-branch`, which proves only
    the branch's tip and deletes the branch with its reflog, so the line names
    the inspection before the retry, in the form that `branch-changed`'s step,
    `inspect it before retrying`, had when ruling A-49 chose it, and keeps
    `reflog-unmerged`'s `show` and full ref name; it supersedes ruling A-46's
    keeping of W47's LOW-3. The same next step
    follows every `Kept` line whose next step is RETRY for a branch the stage
    did not re-prove, its re-proof never starting or never finishing with a
    proof, since the plan's proof holds only until the re-proof renews it
    (rulings A-53 and A-55; D4): a `state-changed` that the re-read's values
    caused, a `deadline-exceeded`, `interrupted` or `internal-error` before
    the re-proof proved the reflog, or a `removal-ceiling`, as in `Kept BRANCH
    (deadline-exceeded); BRANCH's reflog was proven merged into MERGE_TARGET
    only at this run's plan; inspect git -C ROOT reflog show refs/heads/BRANCH
    before retrying: RETRY`, and the own steps above that end in that retry
    carry it before the retry (ruling A-60); each of these lines says that only
    this run's plan proved BRANCH's reflog, which is what the plan found, since
    the plan retires a branch only after its `reflog-unmerged` keep does not
    hold, where these lines had said that the reflog was not proven merged, the
    opposite of what the plan found (ruling A-68; lane openRepoProject-3's W84,
    which showed on Git 2.43.0 and 2.36.6, for `removal-ceiling` and both kinds
    of `state-changed`, that the inspection names the commit only the reflog
    holds and the retry then orphans it);
  - `Kept BRANCH (git-refused); Git refused the deletion; if another worktree
    holds BRANCH, a rebase or bisect of it there included, wait for any rebase
    or bisect there to end, and then switch that worktree off BRANCH by
    running git switch --detach there, which changes none of its files; then
    retry: RETRY`, for `git-refused` with the upstream ref present, the
    post-check finding the branch where the re-read found it (ruling A-32,
    RA's LOW-5; reworded in round A24 under the reader RA2's N1 and ruling
    A-98): the line says that Git refused and names a holder as one cause
    among others, since a stale `packed-refs.lock` or a rejecting
    `reference-transaction` hook gives the same refusal (Context, round A24),
    and the retry, which feature 004's `delete-branch` runs with Git's
    standard error relayed to the person (`RelayParser`, `project:7411` and
    `:7384` at `904aefc`; the reader RN's RN-3), shows Git's own reason if the
    cause persists; printing Git's
    first line in the `Kept` line is not taken, since it would need a field of
    its own, capped and printed by the path rule, where D5's record keeps no
    standard error, and Brett Heap's yes to Q8 does not reach it: PR #19's
    warned-probe rule makes a status probe that exits 0 with a warning fail,
    since Git then leaves what it could not read out of its records (its
    `specs/project-command/spec.md:265-271` at `818311a`, `4512441` and
    `54e869b`),
    where the branch
    child is a mutation that reads no records, whose outcome the post-check
    decides, and whose warning on a deletion it makes, exit 0, against an
    upstream that `HEAD` lacks (Context) would misreport that deletion as a
    failure, so the residual stays (rulings A-103 and A-106); and the holder,
    which the listing does not name as
    BRANCH's, is switched off the branch by a detach run there, never removed,
    by A-98's rule for a holder this run did not read, the detach working in
    the main worktree as in a linked one once a rebase or bisect there has
    ended. The branch child's output is captured, so the
    person never sees Git's "used by worktree"; a worktree mid-rebase or
    mid-bisect is listed detached and Git refuses, and once the rebase or
    bisect ends that worktree holds the branch again and Git still refuses
    until it is switched off the branch or removed (Context), which is why the
    hint names both steps, the wait and the detach, and puts the wait ahead of
    the detach, since a rebase stopped in the main worktree refuses every `git
    switch`, a detach included, with
    exit 128, "cannot switch branch while rebasing" (Context; lane
    openRepoProject-3's W54, LOW-1; ruling A-51); the registry listing shows
    such a worktree detached,
    with no `branch` line, so that the line cannot say whether its holder is
    linked or the main worktree, and the detach serves both (ruling A-45,
    Codex's P2 on `1bf217c`, whose two forms the detach replaces); with the
    upstream ref absent, the same clause comes before that line's own checkout
    step, `Kept BRANCH (git-refused); Git refused the deletion; if another
    worktree holds BRANCH, a rebase or bisect of it there included, wait for
    any rebase or bisect there to end, and then switch that worktree off
    BRANCH by running git switch --detach there, which changes none of its
    files; next: check out MERGE_TARGET in the main worktree, then: RETRY`, or
    its detached-tip form where a linked worktree
    holds MERGE_TARGET, because Git refuses a branch so held whether its
    upstream's ref is present or absent, or no upstream is configured, and the
    checkout alone, of a merge target the main worktree already holds, changes
    nothing (ruling A-35, lane openRepoProject-3's F4; Context); both
    `git-refused` lines keep the bare retry, their branch child having run
    after the re-proof proved the reflog, so that the absent form no longer
    shares `head-not-merge-target`'s text, which names the inspection (ruling
    A-60);
  - otherwise, where the stage's re-proof proved the reflog merged, `Kept
    BRANCH (REASON); retry: RETRY`: `spawn-error`, `unconfirmed-retirement`
    and `probe-timeout`, and a `deadline-exceeded`, `interrupted` or
    `internal-error` that came after that proof, the re-proof's standing
    (rulings A-49, A-53 and A-55; D4).
- Stop block: change 1's, with a branch stage's stop reading `Stopped at PATH
  (branch BRANCH: REASON). Removed K of N. Not attempted: P1, P2. Next: project
  clean ROOT --all-safe --retire-branches`.
- Order (ruling A-34, RE-3). Change 1's D18 prints a stop as `Stopped at ...`,
  then the retained branches and the residual-window line, and success as
  `Removed N; branches kept: B1, B2.`, which the summary and branch lines
  replace. Under the flag the result ends: in a run that stops, the stop block,
  then the retained branches it names, only those that remain, never a branch
  its line names retired, already gone or unconfirmed; then the summary line
  and the branch lines; then the residual-window line. A retired branch is
  absent although the target's `reconciliation`, read before the stage, shows
  `branch_present: true` (D5), so the retained list is computed from the
  branch lines and not from that reconciliation. Feature 004, checked at
  `2cf34d3` only as a check, prints the stop block, `Branches kept:`,
  `Branches not confirmed:` and then the residual-window line, the form this
  order extends (reader RE's RE-3). Under the flag the per-branch
  `Unconfirmed` lines name each branch whose deletion is unconfirmed; whether
  feature 004's `Branches not confirmed:` line, which change 1's text does not
  hold, stays beside them is settled at the alignment with feature 004,
  together with RE-4 to RE-8 (ruling A-35, lane openRepoProject-3's F10). With
  the cache change archived first, its
  `Caches disposed` line, which it prints after change 1's success line,
  follows the summary line and precedes the branch lines (reader RD's L2;
  `tasks.md` 2.3).
- Residual-window line, under the flag: change 1's residual-window line, the
  one that "Cleanup states a narrow guarantee and its residual window" has the
  confirmation and the result each state, with this change's branch clause, `a
  branch changed after its last check`, placed after every other clause that
  line names and before its last clause, `any change after Git's own check`.
  When the plan also selects a cache target
  (`add-project-clean-cache-disposal`), the line is the cache change's line
  (its ruling B-19; its `design.md` D13), which adds that change's clauses to
  change 1's, with this change's branch clause before its last clause (ruling
  A-23). The line is worded relatively and given no literal here, because
  change 1's line has grown since this change's blocks were written, from two
  items to four at PR #19's `f0bf538`, which adds the operations started and
  the worktree-only commits made after the last check, so that a literal would
  have to follow each of its moves (ruling A-50; readers RI's RI-1 and RH's
  M3). The narrow guarantee states that order, so its block, this section and
  the proposal say it alike.

No line prints a retry the plan knows will fail, RETRY for a name that begins
with `-` excepted wherever the action passes no `--` (above), the holder lines
carrying `head-not-merge-target`'s checkout where the plan finds that keep's
condition too, and none
suggests `-D`: the branch child's output is captured like a probe's, so Git's
own advice to run `git branch -D` never reaches the person from the batch, and
the `head-not-merge-target` line names the checkout under which the retry
succeeds (council finding P-1 reproduced both). The retry command names
`delete-branch`, the explicit action, unchanged (`BA:1281-1293`), and never
carries `--retire-branches`, which that action refuses (`invalid-arguments`).
Every `project clean ROOT --all-safe` command printed for the person to run
next under the flag, the deferral line and the stop block's `Next:`, carries
`--retire-branches`, so that following the tool's own advice never strands a
branch whose worktree a flagless run removed (ruling A-22(a), Codex's P1 on
`785a45e`, lane openRepoProject-3's re-read LOW-1). The overview never
suggests the
flag: its suggestion is one of two fixed argument vectors without `--apply`
(`APO/ov:484-487`), so A-6's rule stands under A-1 as amended.

### D9. Tests (A-7, A-15)

`test_clean_removes_only_merged_worktree_and_keeps_branch` (`tests:857`) stays
as the default path's test. Each scenario of the ADDED requirement, and the
review-safety scenario this change adds, gets a test named after it, built on
feature 004's helpers (its T010 fixture builders and T011 counting wrapper and
fake Gits, landed on its branch at `4e3af0a`): the merged, published worktree
with a commit of its own; a worktree whose first commit was amended before it
merged, for the reflog proof; a branch given a commit its merge target lacks
and reset to its planned SHA after the plan, and one moved to such a commit and
back by `git update-ref` after its removal, for the re-proof (ruling A-24);
a local branch with no worktree whose configured upstream is a retired branch,
for the note, and a rebase of the branch that stops at once in another
worktree, with the real Git, for the residual (ruling A-32, RA's LOW-4 and
LOW-5; Context);
the counting `git` wrapper, which records the branch child's arguments, `-C`
directory, environment (no `GIT_ALLOW_PROTOCOL`, no `GIT_OPTIONAL_LOCKS`) and
process group, and each reflog child and re-proof child with its standard
input; test hooks after the plan is printed, after the rescan and after the
re-read, its re-proof included, failures injected into the re-read's listing,
the branch child's spawn and the post-check's listing, and an exception raised
in the stage before its branch child, one of them while its re-proof runs
(ruling A-53), after it and before the post-check decides, and after the
post-check has shown the branch absent (ruling A-31);
and fake `git`s that pass every
other command to the real Git: one whose `branch -d` exits 0 without deleting;
one that refuses with exit 1; one that runs Git's deletion and then exits 1;
one that runs it and then hangs, ignoring SIGTERM; one that ignores SIGTERM
without deleting; one that sleeps 2 s before deleting, for the signal
scenario; one whose reflog child exits nonzero, and one whose reflog child
hangs, past its own budget or into the work deadline, at the plan and,
separately, at the stage's re-proof (lane openRepoProject-3's delta read, D7),
one whose re-read listing hangs past its own budget and, separately, into the
work deadline (lane openRepoProject-3's confirm read of round A10, LOW-2),
and one that delays the re-proof by 2 s, which SIGINT reaches and does not
stop (ruling A-34, RE-2); holders of a target's branch that are dirty, that
hold an edit to a file flagged assume-unchanged or skip-worktree or an ignored
file, whose path cannot be read, that `not-requested` excludes, and a shared
branch's last holder that the run does not reach, each line's printed step
run as printed and the holder's files and flags compared before and after
(round A24, ruling A-98), and, from round A28 (ruling A-126), that last
holder given a commit that only its HEAD reflog holds, which the printed
command refuses, a holder whose directory is moved away, and one whose
administrative `gitdir` file names the main worktree's `.git`, beside a
single-target removal, its main worktree left on the merge target, and a
third target on a branch that tracks a retired one, adjacent to the first; a
reflog that names a commit only as an old object,
made by a commit dated 40 days back and a default `git gc`, whose line's `cat`
command is run from another directory (the reader RA2's L1); a branch moved
after its re-proof, for `post_check_sha` and the moved line (RA2's L2); and
branches named `topic;id` and
`topic`, U+202E and `x`, and, by hand, `-f` and `HEAD`, whose repository's
every row is `inspection-error` under Q8's warned-probe rule and Git's default
`core.warnAmbiguousRefs` (round A25), and whose worktree's row is
`inspection-error` with that setting false in the repository's configuration
too, so that no run retires it (round A28; the reader RN's RN-1; ruling A-128,
which withdraws round A26's test that retired it and restored it by its
printed `update-ref` line), with a root path that
holds a space, run through `dash` for the printed lines and through bash in a
UTF-8 locale for the `$'...'` form. The Context table's facts, the reflog
proof's `^<merge target SHA>` line (lane openRepoProject-3's re-read,
MEDIUM-3) and the re-proof's move and back among them, become fixtures that
assert exit statuses and outcomes, never Git's wording, which differs across
versions (Context; lane openRepoProject-3's delta read, D10), run on change
1's CI floor job at Git 2.36 (its D17; feature
004's `git-floor` job, task T003, ticked on its branch at `4e3af0a` and not yet
on `main`) as well as on the CI workflow's test jobs, which since PR #32 are
Linux only: one `test` job on `ubuntu-latest` for Python 3.10 and 3.12
(`.github/workflows/tests.yml` at `origin/main` `15504f1`), run as `python3 -m
unittest discover -s tests -v`. No CI job runs these tests on macOS, so
nothing here is verified by CI there.

### D10. JSON and the enum question (L-4, A-1 as amended)

`branch_retirement` is one new key on a target object, with enums of its own,
and `branch_plan` one new key on each entry of a plan's `selected`, `{action,
reason}`, `action` `retire` or `keep`, both under the flag only. The plan
envelope gains no key: "Clean plans and refusals are versioned JSON" defines it
as a listed set of fields ("When a plan is built it SHALL be the plan envelope:
...", `CAS/pc:1094-1100`), so a new envelope key would need a MODIFIED block of
that requirement (L-11), and the per-target sub-record of L-10's pattern needs
none. The canonical JSON text of `plan_digest` gains a member named `retire`
under the flag only: the `[branch, planned_sha]` pairs of the branches the
plan retires, ordered as `selected` is, the plan's canonical row order, each
pair at its branch's last holder, and present when empty; without the flag the
text is change 1's byte for byte. Change 1 and PR #19 name what that text
covers, "a canonical JSON text of the repository's four identity fields, the
merge target's name and SHA, and the selected `[path, branch, head]` triples
in canonical order" (`CAS/pc:629-632`, the same at `c462d87`), and not how it
is laid out, so this change names its member and leaves its position to that
construction (ruling A-30, RA's MEDIUM-1); the first text, "its last member,
after the selected triples", is withdrawn. Feature 004, checked at `2cf34d3`
and only as a check, serializes that text as one JSON object with sorted keys
(`project:3729-3749` there), where a `retire` key sorts between `repository`
and `selected` (lane openRepoProject-5's readers RA and RE, RE-1 being RA's
MEDIUM-1, both reproduced in round A7); the flagless
text is unchanged, since the key is added only under the flag. The pairs'
order was undefined before: canonical order is defined for paths, and a shared
branch is retired at its last holder, so the pairs follow `selected`. Both
statements are made against the base text this change is written on. When
this change re-bases on the cache change's archived block (L-11), the flagless
invariant becomes byte-identical to the cache change's text, and the batch
block's digest sentence is re-worded so that it binds to the whole canonical
text, which the cache change's sentence before it ends on "the canonical text
of a plan that selects no such target" (lane openRepoProject-5's reader RD,
its M3(a); ruling A-33); placed after that change's "...carry no such pair or
triple.", it reads: "Under `--retire-branches` the canonical text SHALL also
carry the branches the plan retires, as "Clean retires a removed worktree's
branch only on fresh head and ancestry evidence" states, and without the flag
it SHALL carry nothing more than the members this paragraph names." RD's
wording also placed the branches "after every selected triple and its cache
data"; that position is left out under A-30. The AND that tests the joint
digest is added to "A flagged preview's digest binds the flagged apply" at
that re-base (`tasks.md` 2.3), pinning no order of the members, since it tests
the cache change's own requirement, and is not added if that change is not
ratified (lane openRepoProject-3's re-read, MEDIUM-2). Change 1 versions "a
rename, removal, type change or change of meaning" (`CAS/pc:1129-1131`), and a
new key is none of those; change 2 calls "adding a field" additive
(`APO/ov:656-657`). The ADDED
requirement says that its keys extend, under the flag only, the lists that
"Clean plans and refusals are versioned JSON" enumerates (lane
openRepoProject-3's L10), so that requirement is not modified. No existing enum
gains a value: the target's `stage` and `reason`, the refusal codes, the notes
and the ladder are as change 1 leaves them. The disagreement between the two
changes about adding an enum value therefore does not bind this change; the
proposal put it before Brett Heap with L-4's recommendation, which he ruled as
recommended: an extension's states live in its own sub-record (ruling A-127).

## Risks / Trade-offs

- [Git 2.43's `branch -d` deletes without an expected old value, so a branch
  moved after Git's own read is deleted unchecked] -> The re-read is the last
  read before Git's; Git's checked-out refusal and merge test run on the value
  Git reads; the residual-window line names the window; the proposal's Open
  Questions carry `update-ref -d` with its costs, and Brett Heap ruled that
  question as recommended, option (a), `branch -d` (ruling A-127).
- [A branch whose upstream's remote-tracking ref was deleted is judged by Git
  against the command directory's `HEAD`] -> The plan keeps it with
  `head-not-merge-target` when that `HEAD` is not the merge target's SHA, the
  run continues, and the result names the checkout under which the
  `delete-branch` retry succeeds; with the main worktree on the merge target
  the branch is retired. The SHA test may keep a branch Git would accept.
  PR #2's command-root workaround is not carried (proposal, Out of Scope).
- [Retiring a branch deletes its reflog and its `branch.<b>` section] -> The
  plan proves every commit the reflog names merged, and the stage proves it
  again over the reflog as it then reads, or the branch is kept
  (`reflog-unmerged`, or another retention or plan keep, whose line names
  the reflog inspection before the retry wherever the stage did not re-prove
  the reflog, its own step first where it has one; D8, rulings A-53, A-55 and
  A-60), so no commit named when the branch
  child spawns is lost. The section's keys
  (`description`, `pushRemote`, any tool's keys) are deleted and not
  restored; the printed restore line, `git -C ROOT branch BRANCH SHA` or, for
  a name `git branch` refuses to create, one that begins with `-` or equals
  `HEAD`, `git -C ROOT update-ref refs/heads/BRANCH SHA ''`, recreates the
  branch from the SHA both results print, and `git branch -u` its upstream,
  nothing else.
- [After `git reflog expire` has dropped earlier entries, a commit can be
  named only as the old object of the oldest surviving entry] -> Closed by
  A-16 as amended on 2026-10-19: the proof's input is every non-zero object a
  reflog entry names, new and old, so that commit is proven merged or the
  branch is kept, with no extra child; and the kept branch's line names, as
  its inspection, the reflog file, whose lines print each entry's old object,
  where `git reflog show` does not, a default `git gc` leaving that shape on
  its own (the reader RA2's L1; D8).
- [A branch moved to a commit the merge target lacks and back to its planned
  SHA between the plan and the stage, so that its head, upstream evidence and
  merge target all match the plan while its reflog names the commit] -> Closed
  by ruling A-24 (Codex's P1 on `abad010`): the re-read's re-proof runs the
  plan's proof again over the reflog as it then reads, and retains the branch
  with `reflog-unmerged`, its worktree's removal standing and the run
  stopping; the cost is one more child per retired branch (D7). A commit made
  and moved away after the re-proof's read is in the residual window (D3).
- [A rebased or amended branch whose old commits the merge target lacks is
  kept, never retired] -> By design (A-16); `delete-branch` stays its explicit
  path after the person inspects every commit its reflog names, as `cat
  COMMON_DIR/logs/refs/heads/BRANCH` prints them (D8; the reader RA2's L1),
  and the patch-equivalence
  alternative is an Open Question.
- [A retention the stage discovers stops the run and leaves later eligible
  worktrees for the next run] -> The packet's rule (`BA:1341-1343`); the stop
  block names the flagged preview as the next command. A keep the plan
  foresees never stops it (D6).
- [A holder appearing only after the plan, or a branch whose later holder the
  run did not reach] -> `retained` with `branch-in-use` and a stop, or a line
  naming the holder: its removal only through the flagged single-target
  command, which reads it again through every gate, for a shared branch's
  last holder that the run did not reach (ruling A-126, narrowing A-98);
  R-324's no-prune clause for one whose path could not be read; M3's own step
  for one whose registration names another worktree's path, and a detach in
  the worktree it names once that registration is repaired; its remount or
  repair and a detach there, or change 1's stale-worktree caution, for one
  whose path is missing; and otherwise its own work named and a detach, which
  changes none of its files, then `delete-branch` after the reflog
  inspection, the main worktree switched off the branch by a detach or a
  checkout of MERGE_TARGET (rulings A-45, A-98, A-103 and A-126; D8). No line
  tells the person to remove a holder by hand or by `git worktree remove`, or
  runs a detach at a path that names another worktree or none.
- [A checkout of MERGE_TARGET in the main worktree overwriting an ignored file]
  -> A residual (ruling A-103): every step that advises checking out
  MERGE_TARGET in the main worktree, or its tip TARGET_SHA detached there,
  inherits Git's silent overwrite of an ignored file at a path that
  MERGE_TARGET tracks, as a checkout of any branch that tracks that path does,
  with exit 0 (Context, round A24): the `head-not-merge-target` lines, the
  `git-refused` lines with the upstream ref absent, the holder lines' step
  for `head-not-merge-target`'s condition, and the main-worktree holder line,
  which names the detach first, which changes no file. The same checkout, of
  MERGE_TARGET or of its tip detached, does more than overwrite an ignored
  file at a path that MERGE_TARGET tracks: it also deletes, with exit 0 and
  without a word, an ignored file where MERGE_TARGET needs a directory and
  every ignored file below a path that MERGE_TARGET tracks as a file (Context,
  round A26; lane openRepoProject-3's W131, MEDIUM-1), and a checkout of any
  other branch does the same at the paths that branch tracks (Context, round
  A27; lane openRepoProject-3's W153, observation 1), which is why no step
  names one. The steps keep the
  checkout because with the upstream's remote-tracking ref absent Git judges
  the retry against the main worktree's `HEAD`, which the merge target, or a
  detach at a commit that holds BRANCH, satisfies (Context); the person runs
  the checkout, never the run, and Git refuses one that would overwrite a
  tracked file's or a flagged file's change.
- [A branch moved after its re-proof and moved back before the post-check]
  -> The moved line covers a branch that the post-check finds at another head
  (D8). Two moves by a concurrent writer, both after the re-proof and before
  the post-check, are outside the contract, as the narrow guarantee states a
  change after the re-proof, and the `git-refused` line's bare retry then
  rests on that re-proof, as does the `Unconfirmed` line's, whose post-check
  did not decide (the reader RA2's L2 and L7).
- [A rebase or bisect of the branch in progress in another worktree, which the
  registry listing shows detached] -> A residual (ruling A-32, RA's LOW-5): no
  plan keep or check sees it, Git's own checked-out refusal does, so the
  branch is `retained` with `git-refused` and the run stops with exit 2; the
  `git-refused` line says to wait for the rebase or bisect to end, and then to
  switch that worktree off the branch by a detach run there, which changes
  none of its files, before the retry, a worktree this run did not read being
  never one to remove (D8; Context; rulings A-45, A-51 and A-98). No commit is
  at risk.
- [A local branch whose configured upstream is the retired branch] -> Its
  upstream then reads gone, an unmerged one reads `remote-gone` under change
  1's ladder; a selected row on it next after the retired branch's target is
  removed, and its branch retained with `state-changed` by its re-read, a
  retention that stops the run, its revalidation having compared the ref
  listing read before that branch's stage, while a selected row on it farther
  on is refused at its revalidation with `state-changed`, a refusal that
  stands; no commit is lost either way, and the result names it in a note
  after the `Retired` line, whose restore line restores the upstream too
  (ruling A-32, RA's LOW-4; the reader RJ's F3, ruling A-126; D8).
- [An exception in the stage] -> The target keeps its rescan's outcome, the
  sub-record its evidence, and a deletion the stage made keeps its `Retired`
  line with SHA and restore, or, unconfirmed, its own line (D5, D8; ruling
  A-31).
- [A `reference-transaction` hook runs inside the branch child, as under
  `delete-branch` today] -> Its time counts in the child's 5 s budget, and the
  post-check decides; the hook is the repository owner's code.
- [At the packet's assumed costs a flagged run of 16 retires 13 branches on
  change 1's terms at PR #19's `c462d87`, and, at the packet's 150 ms per child
  (D14's 150 ms basis), 10 at its `6f2cb54`, `a664799`, `2e819ad`, `9267303`,
  `f0bf538`, `662be89`, `6bf9f77`, `b3228bb`, `e0c91bb`, `e14ada0`, `173d83c`,
  `ccc52b9`, `20084cd`, `2250830`, `88d0d36`, `e0b1671`, `818311a`,
  `4512441`, `dab8a64` and `54e869b` where the plan read
  `extensions.worktreeConfig` as false; where it
  read it as true, PR
  #19's D14
  counts a plan-time probe on each linked row, so that at 128 rows a flagged run
  removes and retires nothing on its 150 ms basis, its first removal due at
  45.45 s, and 7 and 7 on its mixed basis as first stated (D7); with the cache
  change and its filesystem time, at `c462d87`, 9 through one worker per stage,
  8 in the worst case of the reflog proof, and at least 5, or 3, at a thread per
  call, 6, or 5, in the worst order a run can take]
  -> On PR #19's measured basis at `662be89`, where LQ-20's step (i) measured
  the two probes that task 2.1 did not (its `design.md:956-969`, its figures
  unchanged at `88d0d36`, `818311a`, `4512441` and `54e869b`; rulings A-47,
  A-62, A-64, A-67, A-71, A-75, A-78, A-84, A-86, A-106, A-110 and A-119),
  change 1 alone removes all 16 at 128 rows, the 16th at 28.7 s where the plan
  read `extensions.worktreeConfig` as false and at 30.0 s where it read it as
  true, or 36.4 s and 37.7 s with 20,000-file removals; on it a flagged run of
  16 removes and retires all 16 in both cases, with this change's children at
  150 ms, the 16th branch child at 38.94 s and 40.18 s, or at task 2.1's
  average of about 0.063 s per child, and falls short only with 20,000-file
  removals and this change's children at 150 ms, 15 removed and 14 retired in
  both cases (D7). With the cache change and one reflog child, where the plan
  read the setting as false, its 16 enumerations at 2.4 s, it brings 15 of 16
  through their stage through one worker per stage, and at least 11 at a
  thread per call, and at the cache change's own 3.7 s for them 14 of 16 and
  at least 10 (D7). At `f0bf538`, with the stand-ins that step (i) replaced,
  a flagged run retired 15 where the setting was false and 14 at 128 rows
  where it was true, with this change's children at 150 ms, and with the
  cache change 12 and at least 8, or 11 and at least 7 (rounds A11 to A13;
  rulings A-42 and A-44). Task 2.1's own account, `c462d87`'s, under which
  all 16 fit through a worker and at least the 16th is deferred at a thread
  per call, with one reflog child or 17, is kept as that sha's (D7). The caps
  stay (A-9): the degraded case is a `not-attempted` target with
  `deadline-exceeded`, or a branch `retained` with it, exit 1, never unsafe,
  and the next run takes it; a branch `retained` with `deadline-exceeded` is
  retried with `delete-branch`, after the reflog inspection that its line
  names wherever its stage did not re-prove the reflog (D8; rulings A-53 and
  A-55). LQ-20 is
  resolved with none of its options taken, so that A-9 no longer waited on it,
  and Brett Heap ruled A-9 on these figures as recommended, `limits.targets`
  16 (D7; ruling A-127).
- [The re-read runs no identity probe] -> The compared head, upstream evidence
  and merge-target SHA, with the plan's reflog proof and the stage's re-proof,
  bound what any deletion can lose (D4); concurrent writers are outside the
  contract.
- [A script running `--yes --json --retire-branches` deletes branches
  unattended] -> Opt-in only, never suggested by the overview, bound by
  `--expect-plan` only to a flagged preview, and every deletion listed in the
  record and the human result with its SHA.
- [Some facts of D3 and D4, those of the Context rows of rounds A3 to A8, were
  checked on Git 2.43 only] -> D9 runs them on change 1's CI floor job at Git
  2.36, once feature 004's `git-floor` job reaches `main`; the rows that name
  the 2.36.6 floor, from round A14 on, were run on it too, and lane
  openRepoProject-3 ran rows of the table on 2.36.6, 2.40.4 and 2.43.0 with
  the same exit statuses and outcomes (Context; the reader RJ's F6; ruling
  A-126).

## Migration Plan

Without the flag nothing changes: every run behaves as change 1 specifies.

1. Ratification by Brett Heap's word on the pull request the lane opens for
   this change, with the two of the proposal's six Open Questions that his
   ledger word did not rule before him, merge-target candidates and
   patch-equivalent reflog commits (ruling A-127; `tasks.md` 1.6). The two
   blocks written on PR #19's text are ratified only as written
   there (`tasks.md` 1.6 and 2.2); a re-base that changes either block's text
   returns that block to Brett Heap (lane openRepoProject-3's re-read, LOW-8).
2. Before the handoff (`tasks.md` section 2): feature 004 merges and change 1
   archives; "Clean reports local worktree state", which no open change
   other than PR #19, the amendment of change 1, modifies, and which PR #19
   modifies beyond round (l)'s AND, with its `relative-config-path`
   paragraph, its scenario "A relative configuration path" and a changed
   "The plain report exits by completeness" (lane openRepoProject-5's reader
   RD, its L1 of 2026-10-23; ruling A-100), and, since its round (t), the
   scenario "A worktree whose path holds the main worktree", Brett Heap's
   M3 (a) (lane openRepoProject-2's R-413; ruling A-119), is re-read against
   change 1's
   archived text, that amendment included, and re-copied from it with this
   change's one clause (`tasks.md` 2.1; lane
   openRepoProject-5's reader RD, its M4; ruling A-33); PR #19 is resolved and
   the two blocks on its text, "Clean bounds
   its Git work and reports omitted work" and the project-command block
   "Repository inspection requires Git 2.36 and shares one evidence model",
   re-read against the text that landed, or change 1's archived text, which
   at PR #19's `54e869b`, as at `4512441` and `818311a`, differ from this
   change's in their texts and in two of five and ten of sixteen scenarios,
   the project-command block's differences being Q1's pin, Q8's warned-probe
   rule, which round (r) qualifies to Git's default `core.warnAmbiguousRefs`,
   T9's "Stale entries:" paragraph and the AND that pins its plain text,
   which Brett Heap's M1 (a) keeps (lane openRepoProject-2's R-413), PR #19's
   rounds (s) and (t) changing no line of that delta, its two added scenarios
   and its two edited ones, all of which the re-base takes as change 1's
   text, keeping this change's sentence on the branch child and its Budgets
   clause (proposal, Dependencies and Sequencing; rulings A-106, A-110 and
   A-119); and
   this change validates again. Each of these re-reads is checked by
   `diff -u` of the archived block against this change's block, as step 6
   says.
3. `/speckit.specify`, from a local `main` synced to `origin/main`, creates the
   one feature under the next free number, 006 or later, recorded once in
   `tasks.md` under "Speckit Handoff"; `/opsx:apply` runs only then.
4. The feature implements D1 to D10 inside feature 004's seam, the README's
   "Clean up Git worktrees" (the flag, its flagged preview, the keeps, the
   stop, the branch lines, the retry path and D8's note on the `$'...'` form;
   the section is `README.md:189-646` in feature 004 at `904aefc`, where the
   edit also takes the sentences that say no run deletes a branch, `:270-271`
   and `:545-547`, and the places the flag changes, the question at `:308`, the
   deferral row at `:423`, the stop block at `:558-559` and the kept-branches
   lines at `:554` and `:562-564`, re-pinned to the text that merged; the
   reader RE's RE2-2, re-pinned from `f3724fc` by the reader RN's RN-3) and
   the tests of D9, merging
   `main` into its branch as `main` moves, the cache-disposal feature included
   when it lands first, and never rebasing.
5. The realization PR merges with green checks on every job that
   `.github/workflows/tests.yml` then runs (at `origin/main` `15504f1`, the
   `test` job on `ubuntu-latest` for Python 3.10 and 3.12; feature 004 adds
   `git-floor`) and closes issue #23.
6. The change is archived after that merge and after the archive of change 1;
   after PR #19's amendment of change 1 lands, or, if PR #19 closes unmerged,
   once the two blocks on its text are re-based on change 1's archived text;
   and, if `add-project-clean-cache-disposal` is ratified, after its archive.
   In that case the five blocks this change shares with the cache change (the
   lane's ruling B-10) are re-based on its archived blocks first (L-5, L-11,
   A-13), and the AND of `tasks.md` 2.3 is added; if it is not ratified, they
   re-base on change 1's archived text and the AND is not added (lane
   openRepoProject-3's re-read, MEDIUM-2; its review-26, M4). The
   project-command block is re-based on the archived block of
   `add-project-overview-remote-merge-status` if that change archives first,
   or is the block it re-bases on (L-11); "Clean reports local worktree state"
   is modified by no open change but PR #19, the amendment of change 1, and is
   re-read against change 1's archived text, that amendment included (step
   2).

   Every re-base and re-read is checked by two diffs (reader RF's M1; ruling
   A-37). The first, kept, is `diff -u` of the archived block against this
   change's block showing additions only, read with
   `git diff --no-index --word-diff` where a line takes an insertion, apart
   from this change's own edits of its base text, which the proposal's
   Capabilities names, and the rewordings below (lane openRepoProject-5's
   reader RD, its M1; ruling A-33). It cannot see a change to this change's
   own words, which after the earlier change archives are all additions to
   the archived block, so a re-base that reworded them would still show
   additions only. The second is `diff -u` of this change's block as
   committed at its ratified head against the re-based block, which may show
   only the archived block's text carried in and the rewordings written out
   below; the ADDED requirement, which has no archived block, is checked the
   same way, as committed there against its re-based text, which may show
   only the rewording of its order sentence below and the AND of `tasks.md`
   2.3. Any other change to this change's words returns that block to Brett
   Heap, before the handoff or before the archive, as the task that makes the
   re-base says (`tasks.md` 2.1 to 2.4 and 3.2; RD's M3).
   `/usr/bin/openspec validate` is a further check and no proof, since
   OpenSpec's archive guard compares scenario names only, so that a re-base
   that keeps every scenario but drops sentences validates and archives (RD's
   M1, shown with `/usr/bin/openspec` 1.13.1). The re-base onto the cache
   change's archived blocks needs these, written here so that they are
   ratified with this change (RD's M3 and its LOWs, ruling A-33; its table
   "What a re-base at archive has to change"):
   - "Clean can explicitly retire verified worktrees": the cache change's one
     clause is carried; nothing is reworded.
   - "Clean previews and applies a batch of eligible worktree removals in one
     repository": this change's digest sentence reads as D10 gives it, after
     the cache change's "...carry no such pair or triple.", "the canonical
     text" for "that text" and "nothing more than the members this paragraph
     names" for "nothing more" (RD's M3(a)), with no position for the branches
     (ruling A-30); the success line's sentence keeps this change's except
     clause; and the cache change's sentences and its scenario "Cache paths
     are part of the plan digest" are carried.
   - "Clean bounds its Git work and reports omitted work": the counting
     sentence merged as the proposal's archive-order note gives it, the two
     stage sentences after the removal floor side by side, the branch stage's
     after the cache stage's, this change's incompleteness clause kept, the
     unbounded-children sentence in this change's wording, and the cache
     change's fit sentence scoped to runs without `--retire-branches` (D7).
   - "Clean records a reconcilable result for every removal target": exit-table
     row 2, which both changes edit (RD's L1), merges as "1: the deadline
     stopped work after the apply phase began, a branch stage's
     `deadline-exceeded` under `--retire-branches` included, any target is
     `unknown`, any target's reason is `removal-ceiling`, a cache stage's
     removal reached the removal ceiling, or, under `--retire-branches`, any
     target's `branch_retirement` has a null `stage`;", and the block carries
     the cache change's five other edits.
   - "Cleanup states a narrow guarantee and its residual window": this
     change's two sentences beginning "Under `--retire-branches`" go directly
     after the guarantee sentence, "...all equal the values in the confirmed
     plan.", and before the cache change's "A cache stage SHALL carry the one
     guarantee ...", the first of them reading "Under `--retire-branches` that
     guarantee SHALL extend to the branch child", so that it binds to the
     removal's guarantee and not to the cache entries' (RD's M3(b)); and the
     scenario "A branch changed after the re-read meets Git's own check" gains
     in its WHEN "in a run whose plan selects no cache target", since the cache
     change's longer line applies when one is selected (RD's L3).
   - The human result: the cache change's `Caches disposed` line follows the
     summary line and precedes the branch lines (RD's L2; D8). The ADDED
     requirement's sentence that orders the flagged result ("Under the flag
     the human result SHALL end with these lines, in this order: ...") is
     reworded to place it: its "then the summary line and the branch lines"
     reads "then the summary line, the line that "Clean disposes of listed
     caches before a worktree removal" adds to a successful apply, and the
     branch lines" (reader RF's L1; ruling A-37).

   If this change archives after `add-project-overview-remote-merge-status`,
   the composed project-command block keeps that change's words as ratified,
   quotation marks included, so that its backquoted `Overview reports remote
   merge evidence on request` stays backquoted beside the double-quoted names
   of change 1, PR #19 and this change: a re-base changes no other change's
   ratified words, except the two rewordings of the cache change's words that
   this change's re-base onto it makes, written out above, a scope added to
   that change's fit sentence and its "or" moved in exit-table row 2, each of
   which returns to Brett Heap, as `tasks.md` 2.3 says (reader RF's L2;
   ruling A-37); and quoting requirement names one way binds this change's
   own text only, so the composed block may hold both styles and the check
   above needs no exception for quoting (ruling A-35, lane
   openRepoProject-3's F9, refining A-33's reading of RD's L4).

Rollback: revert the realization commit on `main`. The flag is opt-in, so the
revert removes only it; branches it retired can be recreated from the SHAs that
the human and the JSON result both print, by the human result's restore line,
which names the repository with `git -C` and so runs from any directory.
Installed `project` artifacts follow
workBenches' pin, so a revert before the pin moves reaches nobody downstream.

## Open Questions

The proposal's six Open Questions each carry a recommendation that the deltas
implement. Four, enum closure, the flag's spelling, the deletion primitive and
the target cap of a flagged run, are ruled as recommended by Brett Heap's
ledger word, in his answers of 2026-10-31 (lane openRepoProject-5's RULED
line; ruling A-127), so that the deltas, D1, D3, D7 and D10 stand as written
for them. Two, merge-target candidates and patch-equivalent reflog commits,
are still before him; a ruling against either recommendation edits the
deltas and D4 or D5 before ratification. No other question changes what is
built.
