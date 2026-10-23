Lane: openRepoProject-5

# Design

## Context

See `proposal.md` for why and what, and the deltas under `specs/` for the
requirements. Citations follow the proposal's key: the packet at `da33d92`
(`BA`, `SY`, `OV`, `HO`), change 1 (`CAS`, `CAS/pc`, `CAS/rs`, `CAS/cmd`) and
change 2 (`APO`, `APO/ov`) at `961c405`, draft PR #19 (`PR19/pc`, `PR19/rs`,
`PR19/cmd`) at `2250830`, its round (n), for the three requirements of
`PR19/pc` whose text round (n) changed, the retire, bounds and
reconcilable-result requirements; at `173d83c`, its round (k), for the
revalidation requirement of `PR19/rs`, whose text round (k) changed; at
`b3228bb`, its round (h), for the batch requirement of `PR19/pc`; at
`6bf9f77`, its round (g3), for the classification requirement; at
`4f1c0e0`, its round (g), for its design, proposal and tasks; and at `f0bf538`,
its round (e), for the rest of the spec text this change cites; `88d0d36`, its
round (o) and its head, whose spec text is `2250830`'s, keeps byte for byte
each of those texts and every string of its design, proposal and
tasks that this change quotes (in round B21 the bounds requirement at
`20084cd`, its round (m), in rounds B19 to B21 the retire requirement at
`173d83c` and the reconcilable-result requirement at `e14ada0`, in rounds B16
to B20 the bounds requirement at `b3228bb`, in round B18 the retire,
reconcilable-result and revalidation requirements at `e14ada0`, its round (j),
in round B17 the retire and reconcilable-result requirements at `e0c91bb`, its
round (i), and the revalidation requirement at `b3228bb`, in round B16 the
retire and reconcilable-result requirements at `b3228bb`, and in
its earlier stages the retire and batch requirements at `4f1c0e0` and the other
three at `f0bf538`, at `f0bf538` throughout in rounds B13 to B15, at `9267303`
in round B12, at `2e819ad` in round B11, at `a664799` in round B10 and at
`c462d87` before it), and `project:N` at `961c405`; at `origin/main` `15504f1`,
`project`, `openspec/specs/` and the directories of change 1 and change 2 equal
`961c405`'s, `ideation/` differs by PR #16's packet revision (`e45155a`), and
`openspec/changes/` gains two other changes (L-15). The lane's rulings are L-1
to L-17 and B-1 to B-109, and A-9, A-23 and A-24 for #23; this change's own
decisions are CD-1 to CD-18 in `proposal.md`, and the alignment review's
findings (SA-n, QA-n, G1 to G5) are resolved in its table. The council (P-n,
S-n and AE-n) read `9ebe9f0`; its VALID verdicts, ruled as B-16 to B-24, are
applied below and in the deltas, and its one NOTED item, S-4, is in
`clarifications.md`, which D4, D14, the Migration Plan and `tasks.md` 2.3 and
3.1 answer. Codex's two findings on `90d18ee` and lane openRepoProject-3's
re-read of `e906c2f`, ruled as B-25 to B-27, and the lead's B-28 are applied in
round B3 (proposal, "Re-read and Codex Findings (round B3)"). Lane
openRepoProject-4's re-align step and wording of 2026-10-20, lane 3's delta
read of `cf57956` and Codex's two findings on `cf57956`, ruled as B-29 to B-33,
are applied in round B4 (proposal, "Re-read and Codex Findings (round B4)").
Codex's two findings on `e1049b2`, ruled as B-34 and B-37, and the lead's B-35
and B-36 (D4's account of #26 at `9ff8202`; `tasks.md` 2.2 ticked again on lane
4's byte check) are applied in round B5 (proposal, "Re-read and Codex Findings
(round B5)"). Lane 3's folded read of `cf57956..fffc194` and Codex's finding on
`fffc194`, ruled as B-38 and B-39, the last two LOWs of lane 3's read, ruled as
B-40, the lead's B-41 on this round's own signal sentence and B-42 on D4's
account of #26 are applied in round B6 (proposal, "Re-read and Codex Findings
(round B6)"). Lane 3's three optional LOWs from its confirm read of round B6 at
`e399309`, ruled as B-43, and Codex's two findings on `e399309`, ruled as B-44
and B-45, are applied in round B7 (proposal, "Re-read and Codex Findings
(round B7)"). Round B8 edited only the proposal and `tasks.md` (B-46). Lane
openRepoProject-5's adversarial read of `fe5b245` (RB) and the M2 of its
composition read of #26, #27 and #29 (RD), ruled as B-47 to B-52, are applied
in round B9 (proposal, "Re-read and Codex Findings (round B9)"). Lane 3's
confirm read of round B9 (W2's LOW 1 to 8) and reader RF's composition read at
the final heads (its H1, and this change's share of its M1), ruled as B-53 and
B-54, with the lead's B-55 on that round's choices, are applied in round B10
(proposal, "Re-read and Codex Findings (round B10)"): the two blocks written on
PR #19's text are rewritten on its text at `a664799`, its round (b), and D4
restates the fit on it. Codex's P2 on `d4e960b` at
`specs/project-clean/spec.md:866`, which reader RG verified and found wider,
ruled as B-56, and PR #19's round (c) at `2e819ad`, on which the two blocks
are re-based and whose three bases D4's fit follows, are applied in round B11
(proposal, "Re-read and Codex Findings (round B11)"). PR #19's round (d) at
`9267303`, with the lead's R-208 on filesystem reads at revalidation, on which
"Cleanup revalidates destructive actions" is re-based, and the lead's B-57 and
B-58 are applied in round B12 (proposal, "Re-read and Codex Findings (round
B12)"), with the lead's B-59 on its first drafts: the bounds block's fit clause
says that the first 14 targets start before only the removal floor remains, and
the drain sentence words the drain past the 16-enumeration cap on its own.
PR #19's round (e) at `f0bf538`, its answer to lane 3's W38 read of round (d),
on which "Cleanup revalidates destructive actions" is re-based, and lane 3's
W33 read of rounds B10 to B12 are applied in round B13 under the lead's B-60 to
B-62 (proposal, "Re-read and Codex Findings (round B13)"): W38's L-4 makes an
administrative directory that the `operation-in-progress` listing finds absent
at revalidation a registration difference, `identity-changed`, which no word
of this change contradicts (D10), and the drain sentence gives the candidates
that the invocation's totals leave a condition of their own (W33's M-1, D4).
Lane 3's W44 read of round B13, whose three wording LOWs the lead ruled as
B-63 and B-64, is applied in round B14 (proposal, "Re-read and Codex
Findings (round B14)"): D10 states outright the rule that a decided absence
keeps its step's own reason (PR19/rs:122-127 at `f0bf538`), and no word of
the deltas changes. Reader RH's and RI's composition reads of the three drafts,
Codex's three findings on `69cb7a1`, lane 3's W56 note on round B14, its W52
read of next steps and its W53 departure ledger, ruled as B-67 to B-69, B-72,
B-74 and B-75 (B-65, B-66, B-70 and B-71 queue or prepare later rounds, and B-73
puts the bounds block and M1's hunk before lane openRepoProject-2 beside the
six), are applied in round B15 (proposal, "Re-read and Codex Findings (round
B15)"): the six blocks that this change carried from
change 1's text at `961c405` are re-based on PR #19's text at `f0bf538`, as the
other two are, with lane openRepoProject-2's byte check of each held block
before the commit, so that all eight are (B-69); the enumeration's child
carries all four status pins (D3, RH's M1); the bounds block words the cache
stage's start test beside the removal child's (RI-9, B-67); D13's cache-run
line carries the two window items that PR #19 added (RI-1, B-67); D10 cites
PR19/rs:122-135, the sentence running past :127 (B-68); D4 gives #26's joint
fit at `9b67e8c` as history (RH's L2); and the `cache-unwritable` line names
the directory whose access check failed and both remedies (D3, D11; lane 3's
F-12 and F-11, B-72, B-74). PR #19's round (g) at `4f1c0e0`, its answer to
lane 3's W52 read of next steps that Git refuses, which changed three of the
eight blocks (W52's F-2, F-3 and F-5), its round (g3) at `6bf9f77`, which adds
to the classification block's scenario "Only tracked-file deletions" the
locked worktree's recovery text (F-2), its round (h) at `b3228bb`, which on
Brett Heap's ruling of 2026-10-22 gives the removal ceiling's recovery text
two forms (F-1), makes a read of gate 7 that the deadline cuts
`deadline-exceeded` (O-1) and adds the exception for a root or common-directory
path that holds a line feed (reader RI's RI-3), and its round (f) at
`662be89`, which resolved LQ-20 by measurement, are applied in round B16 under
the lead's B-76, B-78, B-80, B-84, B-85, B-65, B-79 and B-77 (proposal,
"Re-read and Codex Findings (round B16)"): the classification block is re-based
on `6bf9f77`, and the retire, batch, bounds, reconcilable-result and
revalidation blocks on `b3228bb`, which keeps the classification block's text,
PR #19's text carried in and this change's additions re-applied, two of them
adapted (the batch block's cache-walk exception, attached to gate 7's budget
clause, and the bounds block's fit sentence, given the line-feed condition,
B-85), with lane openRepoProject-2's byte check of each held block before the
commit; D4 states this change's own fit on PR #19's measured costs where the
plan read `extensions.worktreeConfig` as true, which B-55 had left to LQ-20, on
both costs of the enumeration's child at revalidation, and restates on those
costs the fit where it read it as false, for paths without a line feed; and
every cite of PR #19's design, proposal and tasks moves to `4f1c0e0`, whose
quoted strings `b3228bb` keeps, D11's quotation of change 1's next steps
following round (g)'s `contains-submodule` step (W52's F-8). PR #19's round (i)
at `e0c91bb`, which gives the removal ceiling's recovery text a third form, for
a `.git` file that the rescan cannot read (lane 3's W73 M-1, lane
openRepoProject-2's R-284, confirmed by Brett Heap (R-290)), and lane 3's W79
read of round B16, ruled as B-86 and B-87, are applied in round B17 (proposal,
"Re-read and Codex Findings (round B17)"): the retire and reconcilable-result
blocks are re-based on `e0c91bb`, PR #19's text carried byte for byte and this
change's additions re-applied word for word with no adaptation, with lane
openRepoProject-2's byte check of each held block before the commit, and the
other six blocks keep their bases, whose text `e0c91bb` keeps byte for byte;
D11's "the recovery text of a `partially-removed` target" reads true of all
three forms and stays; and D4 counts 11 or 13 targets where the variant's
figures for a plan that read `extensions.worktreeConfig` as false come to about
52.3 s, by its rule that a target counts when it reaches its cache stage or its
spawn by the spawn limit (W79's LOW-1). PR #19's round (j) at `e14ada0`, its
answer to lane 3's W70 read of round (h) with its one-path work-tree probe
(lane openRepoProject-2's R-285, R-287, R-290 and R-291), which narrows the
reason that the ceiling's second recovery text gives to "Git refusing `git
worktree remove --force` while the path remains" (W70's LOW-1) in the retire
and reconcilable-result blocks, and in the revalidation block and its scenario
"A work-tree probe at revalidation" reads that probe's output as one path even
over several lines, another path being `identity-changed` and output that is
empty, names no path or does not end in a line feed `state-changed` (R-287,
R-291), Brett Heap's confirmation of R-284 (R-290), and lane 3's W85 read of
round B17, ruled as B-88 to B-92, are applied in round B18 (proposal, "Re-read
and Codex Findings (round B18)"): the three blocks are re-based on `e14ada0`,
PR #19's text carried byte for byte and this change's additions re-applied word
for word with no adaptation, with lane openRepoProject-2's byte check of each
held block before the commit; the other five keep their bases, whose text
`e14ada0` keeps byte for byte; no text of this change's own restates the
narrowed reason or the probe's rule; and R-284 is named as confirmed by Brett
Heap (R-290) where this change's live text named it pending (B-89). PR #19's
round (k) at `173d83c`, its answer to lane 3's W80 read of its round (i) (lane
openRepoProject-2's R-294, R-299 and R-301), which says in the retire block's
scenario "A removal past the hard ceiling" that the recovery text for a `.git`
file that the rescan cannot read applies instead, "whatever the rescan finds of
the registry entry", and re-wraps the THEN line of the revalidation block's
scenario "A work-tree probe at revalidation", which now ends "since the probe's
two lines are read as one path, which is D's", ruled as B-93, is applied in
round B19 (proposal, "Re-read and Codex Findings (round B19)"): the two blocks
are re-based on `173d83c`, PR #19's text carried byte for byte and this
change's additions re-applied word for word with no adaptation, with lane
openRepoProject-2's byte check of each held block before the commit; the other
six keep their bases, whose text `173d83c` keeps byte for byte; the proposal's
Capabilities bullet for the retire block names the third form in round (k)'s
words; and round (k)'s changes to PR #19's design, proposal and tasks touch no
range that this change cites, every string that this change quotes from them
being present at `173d83c`. PR #19's round (l) at `ccc52b9` (d1c5343 and
ccc52b9), its answer to lane 3's W87 read of its rounds (j) and (k) (lane
openRepoProject-2's R-307, R-310 and R-311), which drops `git worktree prune`
from the next steps and the `inspection-incomplete` remedies while a row's path
could not be read, warning against it, and since round (n) against `git
worktree remove` and `git gc` too (R-324), in five texts, round (l)'s T1 to T5,
which Brett Heap has confirmed ("T1-T5: yes", lane openRepoProject-3's RULED
line d6dd6d9a8, and "R-307: yes; R-310: yes", as lane openRepoProject-2 relays
it, its R-319), and names D18's locked note as a report row's own form, never a
ceiling target's, and lane 3's W92 read of rounds B18 and B19, ruled as B-95 to
B-98, are applied in round B20 (proposal, "Re-read and Codex Findings (round
B20)"): its one spec change, an AND in the scenario "An unreadable worktree is
one row" of "Clean reports local worktree state", is in no block that this
change carries, so the eight blocks keep their bases, whose text `ccc52b9`
keeps byte for byte, and nothing is re-based; no live text of this change's own
restates D18's remedies, and its two mentions of the locked note, round (g3)'s
recovery text in the classification block's scenario "Only tracked-file
deletions", name a report row's form and stay; and round (l)'s changes to PR
#19's design, proposal and tasks leave D14 and task 2.1 byte for byte as they
were and every string that this change quotes from them present at `ccc52b9`;
and D4 scopes its claim that no change of rounds (g) to (l) states a count of
children or a time to PR #19's spec text and its D14 (W92's LOW-1). PR #19's
round (m) at `20084cd`, which records Brett Heap's confirmation of round (l)'s
T1 to T5 and his ruling of three more texts, T6 to T8, "R-320: yes" (lane
openRepoProject-2's R-321), the recommendations of a stale worktree beside a
row whose path could not be read and the row cap's remedy, each leaving out or
warning against `git worktree prune` (lane 2's R-323; round (n) adds `git
worktree remove` and `git gc` to each warning, R-324), ruled as B-99, is
applied in round B21 (proposal, "Re-read and Codex Findings (round B21)"): its
one spec change, an AND in the bounds block's scenario "Row cap and planning
failures" that names the row cap's remedy, "{N} rows exceed the row cap of {M};
remove worktrees explicitly, or prune stale entries by hand; if a worktree's
path cannot be read, do not run git worktree prune until it can" (its words at
`20084cd`, which round (n) extends, below), is carried by re-basing that block
on `20084cd`, PR #19's text carried byte for byte and this
change's additions re-applied word for word with no adaptation, with lane
openRepoProject-2's byte check of the held block before the commit; the other
seven blocks keep their bases, whose text `20084cd` keeps byte for byte; the
cites into the bounds block take `20084cd`'s lines; no live text of this
change's own restates the row cap's remedy or a stale worktree's
recommendation; and round (m)'s changes to PR #19's design, proposal and tasks
leave D14 and task 2.1 byte for byte as they were and every string that this
change quotes from them present at `20084cd`. PR #19's round (n) at `2250830`
(e6b6b16 and 2250830; lane openRepoProject-2's R-345), which applies Brett
Heap's ruling "R-324: yes" of 2026-10-22 (lane openRepoProject-5's RULED line
26e556b43; lane 2's R-343), extending the warnings of round (l)'s and round
(m)'s T1 to T8, and the removal ceiling's third recovery text, to `git worktree
remove` and `git gc` beside `git worktree prune`, so that T8, the row cap's
remedy, reads "{N} rows exceed the row cap of {M}; remove worktrees explicitly,
or prune stale entries by hand; if a worktree's path cannot be read, do not run
git worktree prune, git worktree remove or git gc until it can", and lane 3's
W97 read of rounds B20 and B21, ruled as B-100 to B-106, are applied in round
B22 (proposal, "Re-read and Codex Findings (round B22)"): round (n)'s changes
to three blocks that this change carries, the third recovery text in the retire
block's requirement text and in its scenario "A removal past the hard ceiling",
the third recovery text in the reconcilable-result block's requirement text,
and T8's AND in the bounds block's scenario "Row cap and planning failures",
are carried by re-basing those three blocks on `2250830`, PR #19's text carried
byte for byte and this change's additions re-applied word for word with no
adaptation, with lane openRepoProject-2's byte check of each held block before
the commit; its fifth change, to the scenario "An unreadable worktree is one
row" of "Clean reports local worktree state", is in no block that this change
carries; the other five blocks keep their bases, whose text `2250830` keeps
byte for byte; the cites into the three blocks take `2250830`'s lines; this
change's own live mentions of those warnings name round (n)'s extension; and
round (n)'s changes to PR #19's design, proposal and tasks leave D14 and task
2.1 byte for byte as they were and every string that this change quotes from
them present at `2250830`. PR #19's round (o) at `88d0d36` (lane
openRepoProject-2's R-349, which launched it, and R-350, which accepted it),
its answer to lane 3's W103 read of its round (n), which edits four record
items of its design, proposal and tasks and no spec text, and lane 3's W107
read of round B22, ruled as B-107 to B-109, are applied in round B23 (proposal,
"Re-read and Codex Findings (round B23)"): the eight blocks keep their bases,
whose text `88d0d36` keeps byte for byte, so nothing is re-based; D14 and task
2.1 are byte for byte as they were, two lines later, every cited range of PR
#19's design, proposal and tasks keeps its bytes there, and every string that
this change quotes from them is present at `88d0d36`; and W107's one LOW, a
cell of round B22's record that does not name D3, is corrected by a row of
round B23's record, round B22's record staying as history.

How the packet's contract and the rulings map to the decisions below:

| Source | What it asks | Decision |
| --- | --- | --- |
| `BA:1318-1322`, B-8 | a stage of its own before the worktree removal, inside the seam and its deadline, mutations in `operations.estimated`, bounds in `limits` | D1, D4, D12 |
| `BA:1324-1325`, B-1 | a symlink candidate or ancestor is ineligible and preserved | D2, D7 |
| `BA:1326-1330` | descriptor-relative, no-follow operations; the opened directory checked against the planned device and inode; fail closed where the platform cannot; no check-then-recursive-delete | D5, D7, D9 |
| `BA:1332-1336`, B-6 | each path reported; a partial phase recorded, rescanned and retried; no worktree mutation after a failed preflight | D7, D8 |
| `BA:1336-1337`, B-3 | hard limits on entries and bytes, in the plan estimate | D4 |
| `BA:1632-1634` | symlink candidates and ancestor swaps rejected, external targets intact, each path reported after a partial failure, no broad recursive deletion | D7, D8, D14 |
| `BA:1640-1643` | stop on the first failure | D8 (CD-1) |
| B-2 | an enumeration of its own, bounded, in `probes` and the fit | D3, D4 |
| B-4 | identities of every cache directory and ancestor; cache paths in `plan_digest` | D5 |
| B-5, B-9 | the rung reads blocking paths; disposable and blocking counts, `null` when unknown | D6, D11 |
| B-7 | the residual window stated | D13 |
| L-4, L-10, B-13 | values only in sub-records, present only where this change acts | D11 |
| CD-4 | revalidating a cache target | D10 |
| B-10, L-11 | the digest, the narrow guarantee and the deletion exception in MODIFIED blocks | D5, D8, D13 |
| B-12 | the sample test before any enumeration, and the stall stated | D2, D4 |
| B-14, B-22 | the overview's equality clause excepts the cache-proven case, and the carried "Every protected classifier" scenarios name a non-cache ignored file | D6, D14 |
| L-12, B-15 | CI on Linux only; macOS not verified by CI | D9, D14 |
| B-16 | the stage's removals waited for as change 1 waits for its removal child; the hand-off of the first removal as the commit point | D1, D4, D8, D12 |
| B-17 | the second check immediately before that hand-off; a target whose stage ended `disposed` and whose removal was not spawned | D1, D8, D11, D12 |
| B-18 | the partial-stage rescan by the descriptor chain, under the reserve | D8, D12 |
| B-19 | the residual window widened by the cache stage, stated and bounded | D13 |
| B-20 | a cache directory the user cannot change kept at plan time | D2, D3, D9, D11 |
| B-21 | the stall and deadline lines name their cause | D4, D11 |
| B-23 | `.pytest_cache` before Brett Heap; the measured benefit | Non-Goals, Open Questions |
| B-24 | `candidate_block` names what really keeps a cache-only row | D2, D11 |
| S-4 (NOTED) | measured dispatch cost; the gates of task 2.3 and 3.1 | `clarifications.md`, D4, D14, Migration Plan |
| B-25 | the plan-time walk bounded at 16 x 512 = 8,192 entries, the rows the invocation's totals reject included; the fit and every figure that depends on the walk restated | D4, D13 |
| B-26 | the preflight keeps the run's byte total of the bytes it measures and refuses a target that would take it past 1 GiB | D1, D4, D5, D7, D8 |
| B-27 | lane 3's re-read of `e906c2f`: the ceiling in the exit table, the `not-attempted` stage of a `disposed` stage, the signal paragraph, one relative clause, the citations of `tasks.md` 2.2 | D8 |
| B-28 | "because clean's cache enumeration proved", as the committed `project-overview` delta reads | D6 |
| B-29 | lane openRepoProject-4's re-align step: before `/opsx:archive`, the `project-overview` block re-read against main's text of its requirement and re-copied, keeping any amendment | Migration Plan |
| B-30 | the overview's SHALL NOT holds for the same working directory and refs, in lane 4's words | D6 |
| B-31 | lane 3's delta read of `cf57956`: the removal ceiling beside a signal and the deadline in the stage's exit sentence; the 16th target of D4's case listing no cache | D4, D8 |
| B-32 | the stall test on persistent reasons, never on `blocking` alone; a per-worktree cap told from the totals by the row's counts | D4, D11 |
| B-33 | every recorded directory counts toward the per-worktree cap of 512; the walk opens each recorded directory once, and the stage one chain per directory with removals in each pass; the worst case, depth times those directories, and its limit put to Brett Heap | D3, D4, D5, D7, D14, Risks, Open Questions |
| B-34 | a read of the preflight that the removal floor or the deadline stops before the first removal deletes nothing and changes no state: the stage is `not-attempted` with `target-stopped`, the target `not-attempted` with `deadline-exceeded`, exit 1, the human line naming the deadline, never `refused` with `cache-changed`; a real difference, or a read past its own 5 s budget with no signal received (B-39, B-41), stays `refused`; Codex's P2 at `specs/project-clean-review-safety/spec.md:353` on `e1049b2` is the same item | D1, D7, D8, D11, D12, D14, Risks |
| B-35 | D4 describes #23's joint fit as #26 states it, first at `9ff8202` and, since B-42, at `9b67e8c`, under A-23 and A-24: 81 children, and at the packet's model with cache disposal 10 of 16 targets removed and 9 branches retired through one worker | D4, D13 |
| B-36 | `tasks.md` 2.2 ticked again on lane openRepoProject-4's byte check of B-30's commit, quoted from its log | D6, Migration Plan |
| B-37 | an unsupported platform withholds the cache proof only from a row that reaches the `ignored-local-files` rung; a row that an earlier rung classified, a `dirty` one among them, keeps its classification (Codex's P2 at `specs/project-clean-review-safety/spec.md:383` on `e1049b2`) | D9 |
| B-38 | lane 3's folded read of `cf57956..fffc194`: the last AND of "No time for a cache stage" reads "at least 10 s of work remaining", the complement of the first half's budget under 5 s; "no difference was found"; the packet's reapplication rule cited beside its fit rule; the walk's call count behind D4's 28.3 s | D4, D7, D14 |
| B-39 | a signal received before a preflight read's stop is classified outranks it, and B-41 widens that to every preflight outcome: a read that reaches its own 5 s budget, or the floor or the deadline, after a signal ends the stage `not-attempted` with `target-stopped` and the target `not-attempted` with `interrupted`, never `refused` with `cache-changed`; Codex's P2 at `specs/project-clean-review-safety/spec.md:354` on `fffc194` | D1, D7, D8, D11, D12, D14, Risks |
| B-40 | lane 3's last two LOWs on `fffc194`: B-30's row cites the SHALL NOT sentence's end at `spec.md:35-36`; the quotations of #26's `ca96701` ("13 of its 16 targets ... 11 in the worst case") and of B-19 ("13 at `ca96701`") are verbatim | D4 |
| B-41 | a signal received before the stage classifies any outcome of its preflight, a difference, an error, a byte total past either cap, a `probe-timeout` or a floor or deadline stop, takes the signal's outcome: the stage `not-attempted` with `target-stopped`, nothing deleted, the target and every later one `not-attempted` with `interrupted`, the exit status the signal's; the lead's ruling on this round's own sentence that left a found difference `refused`, which B-39 widened | D1, D7, D8, D11, D12, D14, Risks |
| B-42 | D4 restates #26 at `9b67e8c` exactly, in #26's own words for its counts: 9 of 16 through their stage, 8 in the worst case of the reflog proof, through one worker; at least 5, or 3, at a thread per call, 6, or 5, in the worst order a run can take; all 16 fit through a worker at change 1's measured costs, and at a thread per call at least the 16th target is deferred, where D4 had quoted #26's counts from before its round A5 ("5 and 5, or 4 and 3") | D4 |
| B-43 | lane 3's confirm read of round B6 at `e399309`: "work remaining" in the proposal's 10 s threshold, the floor stop named in the signal AND of "A signal during a cache stage", and the signal exception at D4's run byte total | D4 |
| B-44 | the walk and the whole-list preflight enumerate a directory by `os.scandir` on its descriptor, lazily, one entry at a time, closed as soon as the cap decides, never holding a whole directory's listing; one bounded enumeration is one call under the per-call budget, as a listing was, so no call count or fit moves; D9 checks `os.scandir` in `os.supports_fd` (Codex's P2 at `specs/project-clean/spec.md:873` on `e399309`) | Context, D3, D4, D7, D9, D12, D14, Risks |
| B-45 | the stall line also needs at least one later candidate left with `cache-cap` by the 16-enumeration cap; with exactly 16 candidates, each held for a persistent reason, each row prints its own reason and next step and no stall line prints (Codex's P2 at `specs/project-clean/spec.md:928` on `e399309`) | D4, D11, D14, Risks |
| B-47 | the enumeration's child, which the revalidation of a cache target runs again, carries `-c status.showStash=false`, since under a user's `status.showStash=true` porcelain v2 prints `# stash N` before the records whenever the repository holds a stash, which made every candidate `cache-unverified` (RB's HIGH-1); Git's own documentation gives the setting and the header at the Git 2.36 floor | Context, D3 |
| B-48 | a listed cache directory and every directory inside it fall under the device rule too; a bind mount from the worktree's own filesystem passes the device check, so the claim that disposal never reaches a mounted tree is withdrawn and the residual stated; parsing `/proc/self/mountinfo` rejected (RB's MEDIUM-1) | D2, Risks |
| B-49 | a human line for a target whose cache stage ended `disposed` and whose removal then ended `failed` or `unknown`: the cache paths deleted, and the worktree not removed or its removal not proven (RB's MEDIUM-2) | D11 |
| B-50 | the recommendation on `.pytest_cache` turns to no for this change, with its reasons and what a later change would need (RB's MEDIUM-3) | Non-Goals, Risks, Migration Plan, Open Questions |
| B-51 | RB's five LOWs: an ignored record whose path is absolute or holds an empty, `.` or `..` component is `cache-unverified`; the access check's premise corrected, a read-only mount being seen; the batch block's reflog sentence excepts the cache walk's timed-out reads; the digest covers the disposal decision and not the entry counts, by decision; an entry name that is not valid UTF-8 is blocking, and a no-follow open refused at plan time is `cache-unverified` | Context, D2, D3, D5, D8, Risks |
| B-52 | `tasks.md` 2.1 verifies the re-check of every block written on change 1's or PR #19's text by `diff -u`, `validate` being a second check only, and returns a re-base that changes this change's added text to Brett Heap (RD's M2) | Migration Plan |
| B-53 | lane 3's confirm read of round B9 (W2), LOW 1 to 8: the round B9 record's citation form and LOW-2 count; LOW-1's empty and `.` components named in the proposal; the `faccessat2` condition kept wherever the access check is said to see a read-only mount; a sticky directory's `partial` case; task 2.1's word-level check, a conjunction that a list extension moves allowed; the Migration Plan's step 2 naming the re-base on main and the return to Brett Heap; the review-safety ADDED requirement's ancestor-symlink clause | D3, Risks, Migration Plan |
| B-54 | reader RF's H1 and this change's share of its M1: the two blocks written on PR #19's text rewritten on its text at `a664799`, its round (b), the revalidation's step lists kept in one order; the fit restated on PR #19's D14 at `a664799`, and the caps' Open Question with it; every re-base or re-copy checked by a second diff, from this change's block as committed at its ratified head, and `tasks.md` 3.2 given its return route | Context, Goals, D4, D10, D14, Migration Plan |
| B-55 | the lead's rulings on round B10's first drafts: its choices kept; the enumeration's child at revalidation follows PR #19's round (b) rule (R-171), a cut by the work deadline giving `deadline-exceeded` and its own failure or timeout `state-changed`, B-34's preflight rule unchanged; D13's and the B-19 decision's figures labelled "at `c462d87`"; the Context's account of main corrected to `origin/main` at `15504f1` | Context, D10, D13 |
| B-56 | Codex's P2 on `d4e960b`, verified by reader RG: a candidate that a gate after `deferred-target-cap` excludes keeps its enumeration and its target place and counts as held for a persistent reason, the stall line naming such rows by those gates' reasons with change 1's next steps, and the drain sentence excepting change 1's own deferral stall (RG's (b)); such a row is not counted toward the invocation's totals, the plan applying those gates to each row that reaches them before it applies the totals to any later row, in one canonical pass (T2); running those gates before the enumeration declined; the admin-directory pre-filter put to Brett Heap | Goals, D2, D4, D11, D14, Risks, Migration Plan, Open Questions |
| B-57 | the lead's rulings on round B11's choices, and lane openRepoProject-2's two corrections on its YES: the drain sentence carries PR #19's own condition in full, "removed or excluded by a gate before the cap", and 45 s, the 50 s work deadline less the 5 s removal floor, is the spawn limit wherever this change's text means that instant | D4 |
| B-58 | the plan for round B12: "Cleanup revalidates destructive actions" re-based on PR #19's round (d) at `9267303` for the lead's R-208, every filesystem call of the revalidation following the rule of a Git child, a path found absent (`ENOENT` or `ENOTDIR`) a decided value; the bounds block's fit clause "before the spawn limit"; the fit re-cited at `9267303` | D4, D7, D10 |
| B-59 | the lead's rulings on round B12's first drafts: the bounds block's fit clause reads "before only the removal floor remains, and the last two are", since no spec defines the spawn limit, which the design and proposal keep where D4 defines it; `ENOTDIR` at the preflight is either a non-directory where the plan recorded a directory or an ancestor that is no longer a directory, a decided absence as R-208 reads it, a difference either way | D4, D7 |
| B-60 | the plan for round B13: "Cleanup revalidates destructive actions" re-based on PR #19's round (e) at `f0bf538`, which writes "SHALL NOT" (W38's L-5) and makes an administrative directory that the `operation-in-progress` listing finds absent at revalidation a registration difference, `identity-changed` (W38's L-4); this change's own words read against W38's L-4; the bounds block byte-identical to round B12's; every cite of PR #19's current text moved to `f0bf538` | D4, D10 |
| B-61 | the lead's ruling on round B13's own observation: an error or timeout of the admin-directory pre-filter's listing filters nothing, the row staying a would-be candidate that meets change 1's own gates in their turn, so the pre-filter never makes a plan incomplete | proposal, Open Questions |
| B-62 | lane 3's W33 read of rounds B10 to B12, all its findings: the drain sentence gives each cap its own condition, the candidates that the invocation's totals leave draining as the candidates ahead of them are removed, cease to be candidates or cease to count toward those totals, since a candidate that a gate after `deferred-target-cap` excludes stops counting toward them but keeps its place among the 16 (M-1); D10 cites PR #19's carve-out at `f0bf538` (L-1); D4 numbers feature 004's gates since `93a3ae9` (L-2); `tasks.md` 1.4's attribution (L-3); the round B12 record's fit-clause row (L-4); short lines re-wrapped only in passages this round edits (O-1) | D4, D10 |
| B-63 | lane 3's W44 read of round B13, `25f7333..bced895`, no HIGH or MEDIUM and three wording LOWs, queued for #27's next round and not a round of their own; LOW-3 is applied by making D10 state the decided-absence rule explicitly, which makes the B13 pull-request comment's sentence exact, the comment itself standing | D10 |
| B-64 | the lead's ruling that round B14 runs on Brett Heap's word of 2026-10-22 to do as much as possible in parallel, the trigger that B-63 waited for: W44's LOW-1 (lane 2's check covered three held blocks), LOW-2 (round B13's tally counts as the earlier rounds' do) and LOW-3 (D10 states the rule outright, PR19/rs:122-127 at `f0bf538`) are applied with no spec edit and no PR #19 block change, so lane openRepoProject-2 needs no check | D10; proposal, round B13 and round B14 records |
| B-65 | the lead's ruling, queued in round B15 and triggered by PR #19's round (f) at `662be89`, which resolved LQ-20 by measurement: this change states its own fit on PR #19's measured costs where the plan read `extensions.worktreeConfig` as true, since its stance of stating none (B-55) rested on LQ-20 being open, and its statements that LQ-20 is open, or that it asks Brett Heap to measure first, go (reader RH's item 6: D4's account of D14's bases and the proposal's sentences on LQ-20's first step); applied in round B16 | D4 |
| B-66 | the lead's ruling: A1's alignment prepared now, in scratch only, as held blocks that become a round on this change only after #34 merges, and go to lane openRepoProject-4 first as one held file; nothing is applied in round B15 | Migration Plan (queued) |
| B-67 | the lead's ruling on reader RI's RI-9 and RI-1: the bounds block says that a cache stage starts only while more than the removal floor remains, a stricter test than the removal child's, which is spawned while at least that floor remains (RI-9); D13's cache-run residual-window line carries the operations started and worktree-only commits that PR #19's requirement names, with the base question settled by B-69 (RI-1, RH's M3) | D13; the bounds block |
| B-68 | lane 3's W56 note on round B14, which the lead put into round B15: D10 cites PR19/rs:122-135 at `f0bf538` for the decided-absence rule, the sentence running on past :127 | D10 |
| B-69 | the lead's ruling, option (a) on reader RH's item 7 and Codex's three findings on `69cb7a1`: the six blocks that this change carried from change 1's text at `961c405` (classification, retire, batch, reconcilable result, preservation, narrow guarantee) are re-based on PR #19's text at `f0bf538`, which also makes the batch block define `operation-in-progress` and `worktree-only-commits` (7.2-a to 7.2-e), with lane openRepoProject-2's byte check before the commit, as in round B13; RH's M1, the enumeration's child carrying all four status pins; and RH's L2, D4's account of #26's joint fit given as history; the rule that this change re-bases its PR #19 blocks whenever PR #19 changes them now covers eight blocks | D3, D4, D10, D14, Migration Plan; the six blocks |
| B-70 | the lead's ruling: AL1's held blocks on A1's ratified text go to lane openRepoProject-4 now, as one held file; they become a round on this change only after #34 merges, and the 21 other places join that round; nothing is applied in round B15 | Migration Plan (queued) |
| B-71 | the lead's ruling: task 2's re-align step gains lane openRepoProject-4's survival check, that every A1 line of requirements 3, 5, 8 and 9 is present in the re-aligned block, by a diff against A1's block at its landing sha; it is written in the alignment rounds, and nothing is applied in round B15 | Migration Plan (queued) |
| B-72 | the lead's ruling on lane 3's W52 (`compose-nextsteps-findings.md`) F-12 and F-11, which concern this change's own `cache-unwritable` next step and no PR #19 block: the line names the first directory, by raw path bytes, whose access check failed, relative to the worktree, since a mode change of the worktree itself leaves the check false (F-12); the check returns a boolean and cannot tell a read-only filesystem apart, so the line stays one general line and D3 says so (F-11), which B-74 completes | D3, D11, Risks |
| B-73 | the lead's ruling: lane openRepoProject-2 also checks the bounds block, since its RI-9 hunk changes a PR #19 block, together with M1's hunk in the ADDED requirement, beside the six re-based blocks | the bounds block; D3 |
| B-74 | the lead's ruling for stage 2: `os.access` cannot tell `EROFS` apart, so the general `cache-unwritable` line names both remedies, to fix the ownership or mode of the directory or, on a read-only filesystem, to remount it writable; the failing directory stays in the human line only, with no JSON key, so the schema does not change | D3, D11, Risks |
| B-75 | the lead's ruling: this change's departures list cites the packet line that each of lane 3's W53 rows changes, 27-03, 27-04, 27-06 and 27-07, as W53 gives it, so that the packet revision can take them as written | proposal, Corrections to the Packet |
| B-76 | the lead's ruling: once PR #19's round (g) lands, at `4f1c0e0`, this change re-bases the blocks that round (g) changes, the classification (W52's F-2, a locked worktree's partial-removal recovery), retire (F-5, the refusal for a branch that the main worktree holds, and the scenario "Branch deletion refuses a branch it may not delete") and batch (F-3, the plan-blocking remedy naming `core.worktree` and `core.bare` in `config` or `config.worktree`) blocks, with lane openRepoProject-2's byte check before the commit, and carries B-65; the other five blocks are byte-identical at `f0bf538` and `4f1c0e0` and need no change | Context, D4, D11, Migration Plan; the three blocks |
| B-77 | the lead's ruling on lane openRepoProject-4's YES (2026-10-22): the proposal's Archive order bullet, in lane 4's pinned range, names the blocks written on PR #19's text without a count, the one change inside lane 4's pins in round B16 | proposal, Dependencies and Sequencing |
| B-78 | the lead's ruling on lane openRepoProject-2's notice of PR #19's round (g3): round B16 finishes its first stage on `4f1c0e0`, re-bases the blocks that round (g3) changes on it in a stage of its own, and commits only after round (g3) lands and lane 2's byte check | Context; the classification block |
| B-79 | the lead's ruling on round B16's own doubt: D4 and the caps Open Question give both costs of the enumeration's child at a cache target's revalidation, as the status probe whose place it takes, this change's method, and as an enumeration, about 0.23 s, under which 8 cache targets add about 1.3 s and the thread-per-call 10,000-file case is about 45.9 s, past the spawn limit, its 16th target waiting for the next run with exit 1; task 2.3's measurement settles which cost holds, and neither is chosen before it | D4; proposal, What Changes and Open Questions |
| B-80 | the lead's ruling: PR #19's round (g3) at `6bf9f77` changes, of the blocks this change carries, only the classification block, whose scenario "Only tracked-file deletions" gains the locked worktree's recovery text (W52's F-2), so round B16 re-bases that block alone on `6bf9f77`, carrying the clause as PR #19's current text, which a later re-base follows if Brett Heap reverts F-2, and keeps the retire and batch blocks on `4f1c0e0`, which `6bf9f77` keeps byte for byte; it applies B-79 | Context, D4, Migration Plan; the classification block |
| B-81 | the lead's ruling: round B16 reports whether a block this change carries, or its own text, quotes or restates PR #19's bounds sentence on the Git children of one revalidation and of the final rescan, so that a re-base follows PR #19's round (h) where one does; it does, so round B16's last stage re-bases it (B-84) | D4, D10; the bounds and revalidation blocks |
| B-82 | the lead's ruling on Brett Heap's ruling of 2026-10-22 on PR #19's F-2, F-1 and O-1 (lane openRepoProject-2's R-263): F-2 stands as written, and round B16 maps every place that PR #19's round (h) touches, the removal ceiling's recovery text, gate 7's budget-cut sentence and the bounds sentence, each marked as carried or this change's own, changing none of them before round (h) lands | Context |
| B-83 | the lead's ruling on round B16's two judgment calls: the What Changes clause of B-79 stays, so that the proposal never says that all 16 fit without the variant, and the 16th target waits as every target the deadline leaves does, since this change's drain rule covers the candidates that the caps leave | proposal, What Changes; D4 |
| B-84 | the lead's ruling: PR #19's round (h) at `b3228bb` changes five of the eight blocks, the retire, batch, bounds, reconcilable-result and revalidation blocks, so round B16 re-bases those five on it, carrying PR #19's text byte for byte and re-applying this change's additions, the batch block's cache-walk exception attached to gate 7's budget clause, the deadline not being the limit, a deadline cut of a cache-walk read following PR #19's `deadline-exceeded` as this change's enumeration rule already gives; this change's live restatements of the three strings take round (h)'s form, its six-child fit arithmetic staying for paths without a line feed and saying so, and its records stay as history; PR #19's head is `b3228bb` | Context, D4, D10, Migration Plan; the five blocks |
| B-85 | the lead's ruling: round B16's two adaptations of this change's own words, made where round (h) changed the text they rest on, stand as within B-84 and go to lane openRepoProject-2 with the held set: the batch block's cache-walk exception attaches to gate 7's budget clause, the deadline not being the limit, and the bounds block's fit sentence of 283 Git children gains the condition that neither the path of the repository's root nor that of its common directory holds a line feed | Context, D4; the batch and bounds blocks |
| B-86 | the lead's ruling: round B17 takes lane 3's W79 read of round B16, 0 HIGH, 0 MEDIUM, 2 LOW and nothing departing: D4's count for the variant where the plan read `extensions.worktreeConfig` as false, at 20,000-file removals and a thread per call, reads 11 or 13 with D4's rule stated, the 13th target with the 8 cache targets last reaching its stage at about 44.6 s (LOW-1), and the cite-only hunks that round B16's table leaves out of its B-76 and B-84 rows are recorded in round B17's table, round B16's table staying as history (LOW-2) | D4 |
| B-87 | the lead's ruling: PR #19's round (i) at `e0c91bb` gives the removal ceiling's recovery text a third form, "inspect `<path>` by hand; its `.git` could not be read, so do not run `git worktree prune` until it can", for a `.git` file that the rescan cannot read (lane 3's W73 M-1, lane openRepoProject-2's R-284, pending Brett Heap's confirmation), in the retire and reconcilable-result blocks, so round B17 re-bases those two on it, carrying R-284's text as PR #19's current text, as B-80 did with F-2 while F-2 was pending, a later re-base following if Brett Heap reverts it, with lane openRepoProject-2's byte check before the commit; the other six blocks are byte-identical at `e0c91bb`; PR #19's head is `e0c91bb` | Context, D4, D10, Migration Plan; the two blocks |
| B-88 | the lead's ruling: once lane openRepoProject-2 accepts PR #19's round (j), round B18 re-bases the blocks it changes, with lane 2's byte check before the commit: at `e14ada0` the retire and reconcilable-result blocks give the ceiling's second recovery text the reason "Git refusing `git worktree remove --force` while the path remains" (W70's LOW-1), and the revalidation block and its scenario "A work-tree probe at revalidation" read the probe's output as one path even over several lines, another path being `identity-changed` and output that is empty, names no path or does not end in a line feed `state-changed` (R-287, R-291); the other blocks are byte-identical at `e14ada0`; PR #19's head is `e14ada0` | Context, D4, D10, D14, Goals, Migration Plan; the three blocks |
| B-89 | the lead's ruling: Brett Heap has confirmed R-284 ("R-284: yes", lane openRepoProject-2's R-290), so every live mention of it as pending, or as put to Brett Heap, reads "confirmed by Brett Heap (R-290)", round records staying as history | Context; proposal, Decisions (L-1 and L-15) |
| B-90 | the lead's ruling: round B18 runs now, in two stages with lane openRepoProject-2's one-pass byte check between, re-basing the blocks round (j) changed (B-88) and bringing R-284 to confirmed (B-89), lane 3's W85 findings joining it if they arrive while it works | none |
| B-91 | the lead's ruling on lane 3's W85 read of round B17, 0 HIGH, 0 MEDIUM, 1 LOW and nothing departing: the proposal's key names W73 as lane 3's read of feature 004's writer G, not of round B16 (LOW-1); its list of R-284's stale wording is B-89's sites; its sites of the narrowed reason are the carried lines that B-88 takes from `e14ada0`; and its verdict and checks are a row of round B18's table | proposal, key |
| B-92 | the lead's ruling: round B18's stage 2, its commits, its record and its line map, runs on lane openRepoProject-2's YES to the held set (R-298) in the lane's next window, an account swap having been requested at the moment that YES arrived; round B19 follows PR #19's round (k) once lane 2 accepts it | none |
| B-93 | the lead's ruling: after round B18's stage 2, round B19 re-bases, in the same tree, the blocks that PR #19's round (k) at `173d83c` changes, which lane openRepoProject-2 accepted (R-301), with lane 2's byte check before the commit: the retire block's scenario "A removal past the hard ceiling" says that the recovery text for a `.git` file that the rescan cannot read applies instead, "whatever the rescan finds of the registry entry", and the THEN line of the revalidation block's scenario "A work-tree probe at revalidation" is re-wrapped and ends "since the probe's two lines are read as one path, which is D's"; the other six blocks are byte-identical at `173d83c`; round (k) also changes PR #19's design, proposal and tasks, so each cite of them is checked; PR #19's head is `173d83c` | Context, Goals, D4, D10, D14, Migration Plan; the two blocks |
| B-94 | the lead's ruling: round B19's stage 2 runs on lane openRepoProject-2's YES (R-306); lane 3's W87 sites in this change at `97bf4ee` are round B18's and round B19's re-bases, whose words the stage confirms at each, and it sweeps the R-284 sites, the live ones saying "confirmed by Brett Heap (R-290)" and the records staying as history | none |
| B-95 | the lead's ruling: PR #19's round (l) at `ccc52b9`, which lane openRepoProject-2 accepted (R-311), changes no block that this change carries, its one spec change being an AND in the scenario "An unreadable worktree is one row" of "Clean reports local worktree state", so nothing is re-based; PR #19's head and any live restatement of D18's locked note go to round B20, with lane 3's one-pass read of rounds B18 and B19 if it has come | Context, D4, Migration Plan |
| B-96 | the lead's ruling: round B20 runs now, in two stages, stage 1 building and holding round (l)'s currency and stage 2 committing on the lead's message, with lane 3's one-pass read of `97bf4ee..dc39ec3` if it has come or without it; no spec re-base is expected (B-95) | none |
| B-97 | the lead's ruling: Brett Heap has confirmed round (l)'s T1 to T5, the unread forms of the next steps and remedies (lane openRepoProject-2's R-307 and R-310), in his words "T1-T5: yes" (lane openRepoProject-3's RULED line, d6dd6d9a8), so the Context's "put to Brett Heap to confirm" for them names his confirmation, and so does any other live mention of them as put to him, round records staying as history | Context |
| B-98 | the lead's ruling on lane 3's W92 read of rounds B18 and B19, 0 HIGH, 0 MEDIUM, 1 LOW and nothing departing: D4's claim that no change of rounds (g) to (l) states a count of children or a time is scoped to PR #19's spec text and its D14, since round (k)'s proposal states three more children for a submodule checkout's repeated identity probe, which D14 does not count, so that no figure moves (LOW-1); W92's verdict and notes are rows of round B20's table | Context, D4 |
| B-99 | the lead's ruling: round B21 re-bases the bounds block on PR #19's round (m) at `20084cd`, which lane openRepoProject-2 accepted (R-323), in two stages with lane 2's byte check before the commit: the block's scenario "Row cap and planning failures" gains an AND that names the row cap's remedy, "{N} rows exceed the row cap of {M}; remove worktrees explicitly, or prune stale entries by hand; if a worktree's path cannot be read, do not run git worktree prune until it can"; the other seven blocks are byte-identical at `20084cd`; the round also takes round (m)'s currency, Brett Heap's confirmation of T1 to T8 ("R-307: yes; R-310: yes" and "R-320: yes", as lane 2 relays them), and a report on any live restatement of F-1, whose (b) PR #19 now records as open; PR #19's head is `20084cd` | Context, Goals, D4, Migration Plan; the bounds block |
| B-100 | the lead's ruling: round B21's stage 2, its commits, its record and its line map, runs on lane openRepoProject-2's YES to the held set (R-325), with a checkpoint if the lane's usage meter reaches 85% | none |
| B-101 | the lead's ruling on lane 3's W97 read of rounds B20 and B21, 0 HIGH, 0 MEDIUM, 1 LOW and nothing departing: its LOW-1, that round B21's row on round (m)'s changes to PR #19's design, proposal and tasks names as the 22nd cited range the residual-window line (its design.md:1183-1185 at `4f1c0e0`), which is byte-identical at every sha, where the range that changed is its design.md:1189-1216 at `4f1c0e0`, goes to round B22: the line inside round B21's record stays as history, and its correction is a row of round B22's record; round B22 waits for Brett Heap's answer to R-324 | proposal, "Re-read and Codex Findings (round B22)" |
| B-102 | the lead's ruling, refining B-101: W97's LOW-1 corrects only a row of round B21's record, which stays as history, and changes no live text that Brett Heap ratifies, so it opens no round by itself; round B22 opens when R-324 is answered yes, or when lane 3's next read of this change brings a finding, and the LOW-1 row rides with it | none |
| B-103 | the lead's ruling: Brett Heap having ruled "R-324: yes" (lane openRepoProject-5's RULED line 26e556b43; lane openRepoProject-2's R-343), so that every no-prune warning, the removal ceiling's third recovery text and T1 to T8, names `git worktree remove` and `git gc` beside `git worktree prune`, round B22 re-bases on PR #19's round (n), once its sha comes, the retire and bounds blocks, the two that lane 2 first reported it changing, in two stages with lane 2's byte check before the commit, records R-324, and carries W97's LOW-1 row (B-101, B-102) | Context; proposal, Capabilities, Dependencies and Sequencing |
| B-104 | the lead's ruling: PR #19's round (n) is at `2250830` (e6b6b16 and 2250830), which lane openRepoProject-2 accepted (R-345), and round B22 re-bases three blocks on it, retire (its requirement text's third recovery text and the AND of the scenario "A removal past the hard ceiling"), reconcilable result (its requirement text's third recovery text) and bounds (T8's AND in the scenario "Row cap and planning failures"); round (n)'s fifth change, in the scenario "An unreadable worktree is one row", is in a block that this change does not carry; the other five blocks are byte-identical at `2250830`, and D14 and task 2.1 are byte-identical to `20084cd`'s; PR #19's head is `2250830` | Context, Goals, D4, Migration Plan; the retire, reconcilable-result and bounds blocks |
| B-105 | the lead's ruling: after the lane's swap to team-01e, round B22 runs now, its stage 1 on PR #19's round (n) at `2250830`, in parallel with round A22 on #26, one writer to each tree | none |
| B-106 | the lead's ruling on round B22's five questions: the ruling range runs to B-106, the B-100 row staying and rows B-105 and B-106 added, in the design's ruling table, the key and the Status; the round B22 table may start in stage 1; round B21's Context sentence keeps its quotation of T8 in round (m)'s words, marked as such; the re-wrap of the proposal's key and of Dependencies and Sequencing stands, the round B22 table naming each re-wrapped paragraph and saying that its words are unchanged except where the word diff shows; and W97's O-1 gets no edit and is recorded as a note | Context; proposal, Status, key, "Re-read and Codex Findings (round B22)" |
| B-107 | the lead's ruling: PR #19's round (o) at `88d0d36` (lane openRepoProject-2's R-349 and R-350), which edits four record items of its design, proposal and tasks and no spec text, so that its spec text is `2250830`'s, moves this change's naming of PR #19's current head to `88d0d36` in this change's next round, with lane 3's findings on round B22; each cite of PR #19's design, proposal and tasks is checked by content at `88d0d36`; nothing is re-based, the bases staying where round B22 put them, and no round opens for this alone | key, Context, D4, Migration Plan; proposal, Status, key, Capabilities, Dependencies and Sequencing, Decisions (L-1 and L-15); `tasks.md` 1.4, 2.1 |
| B-108 | the lead's ruling on lane 3's W107 read of round B22, 0 HIGH, 0 MEDIUM, 1 LOW and nothing departing: its LOW-1, that the "Section edited" cell of round B22's row for B-103 and B-104 does not name D3, whose cite PR19/pc:310-311 at `173d83c` becomes :333-334 at `2250830`, is corrected by a row of round B23's record, round B22's row staying as history; W107's verdict, its checks not done at lane 3's wrap-up and the lead's facts (CI and SonarCloud at `dafe476`, round B22's comment 6352482312, and lane openRepoProject-2's YES as R-348, sent at 22:07:28Z) are rows of that record | proposal, "Re-read and Codex Findings (round B23)" |
| B-109 | the lead's ruling: lane 3 closed two of W107's checks not done on 2026-10-23 at 03:16:22Z, CI and SonarCloud at `dafe476` with round B22's comment, and the saved stage 1 diff's sha256, the other two folding into its read of round B23, so that round B23's row for those checks records the closures rather than "not yet read" | proposal, "Re-read and Codex Findings (round B23)" |

What in `project` shapes the approach:

- `repo_state()` runs one ignored-file probe per worktree, `git status
  --porcelain=v1 --ignored=matching`, with no `--untracked-files` and no bound,
  and keeps only the count of `!! ` lines (`project:505-507`); under
  `status.showUntrackedFiles=no` that probe fails, which change 1 records (CAS
  proposal.md:51-53). No list of ignored paths survives it.
- `cleanup_report()` tests `ignored_files is None` (`inspection-error`) and then
  any non-zero count (`ignored-local-files`) before every merge test
  (`project:578-583`), so a merged worktree holding a single `.pyc` file is
  never `merged-removable` today.
- `cleanup_signature()` compares `ignored_files` and `classification`
  (`project:642-645`), and `require_unchanged_cleanup_state()` recomputes the
  whole report to revalidate (`project:656-666`).
- The remove path builds `git -C <root> worktree remove <path>`, shows it,
  confirms it, revalidates and runs it through `execute()` (`project:707-722`,
  `project:736-743`; `execute()` is `project:157-162`); nothing in `project`
  deletes a file today.
- Feature 004 replaces all of this (its `plan.md` slices 2, 3, 5 and 6 on
  `origin/004-project-clean-all-safe`): the bounded runner and its parsers,
  filesystem calls on daemon threads under `min(5 s, work remaining)`, the
  evidence pipeline and pure ladder, the gates and plans, and the seam
  `retire_worktree(plan, target)` with the targeted revalidation. This change
  attaches to that code, so its feature starts after feature 004 merges.

Facts checked here, on Git 2.43.0 and Linux 6.18, with Python 3.10.21 and
3.12.3, in scratch fixtures outside the repository:

| Probe | Observed |
| --- | --- |
| `status --porcelain=v2 -z --untracked-files=normal --ignored=matching` under the ignore rules `__pycache__/` and `*.py[co]` | one record per ignored `__pycache__` directory (`! src/pkg/__pycache__/`), its contents, nested `__pycache__` included, unlisted; one per loose file (`! loose/old.pyc`); porcelain v1 gives the same records with `!!` |
| the same under `*.pyc` and `*.pyo` alone | one record per file (`! src/pkg/__pycache__/a.cpython-312.pyc` and so on); the directories themselves are never listed |
| `--ignored=matching` with `--untracked-files=no`, or with `status.showUntrackedFiles=no` and no `--untracked-files` | `fatal: Unsupported combination of ignored and untracked-files arguments`, exit 128 |
| a symbolic link named `__pycache__` | ignored (`! __pycache__`) under the rule `__pycache__`; untracked (`? __pycache__`) under `__pycache__/`, which makes the row `dirty` |
| a symbolic link named `link.pyc` | ignored under `*.pyc` |
| `os.open(name, O_RDONLY \| O_DIRECTORY \| O_NOFOLLOW, dir_fd=fd)` on a symbolic link to a directory | fails with `ENOTDIR` |
| `os.rmdir(name, dir_fd=fd)` on a directory still holding a file | fails with `ENOTEMPTY`; the file is intact |
| `O_NOFOLLOW`, `O_DIRECTORY`; `open`, `stat`, `unlink`, `rmdir` in `os.supports_dir_fd`; `stat` in `os.supports_follow_symlinks`; `listdir`, `scandir` in `os.supports_fd` | all present on both Pythons on Linux; macOS was not checked here and is not verified by CI, whose jobs `test (3.10)` and `test (3.12)` run on `ubuntu-latest` only (D9) |
| `status --porcelain=v1 -z --untracked-files=normal --ignored=matching` with eight ignored `a0.pyc` to `a7.pyc`, an ignored `__pycache__/` and an ignored `zz.env` | ignored records in path order, so the first eight, the combined probe's samples, are the `.pyc` files and `zz.env` comes after them |
| `os.access` in `os.supports_dir_fd`, `os.supports_effective_ids` and `os.supports_follow_symlinks`; `os.access("__pycache__", os.W_OK \| os.X_OK, dir_fd=fd, effective_ids=True, follow_symlinks=False)` on a `__pycache__` of mode 0555, as a user other than root | all three present; the check returns false, and an `os.unlink` of an entry relative to that directory fails with `EACCES` (errno 13); checked on Python 3.12.3 only, on 2026-10-19 (B-20) |
| `os.scandir(fd)` on the descriptor of a `__pycache__` holding 100,000 empty files on ext4, taken one entry at a time to the 513th and closed (B-44) | one descriptor more while it is open, a duplicate, and none after its close; while it is open the duplicate shares the descriptor's offset, and its close rewinds it, so the descriptor then reads offset 0, `fstat`s to the same device and inode and gives a second enumeration all 100,000 entries; the Python-traced memory of the stopped enumeration peaked at about 1 KB, against 7.2 to 8.0 MB for `os.listdir(fd)` on the same directory; checked on Python 3.10.21, 3.12.3 and 3.13.15 on 2026-10-20 |
| `status --porcelain=v2 -z --untracked-files=normal --ignored=matching` with the protocol and status pins, in a linked worktree holding `src/pkg/__pycache__/`, under a user's `status.showStash=true`, the repository holding one stash (B-47) | `# stash 1` before `! src/pkg/__pycache__/`; with `-c status.showStash=false` added, `! src/pkg/__pycache__/` alone; change 1's porcelain v1 combined probe prints `!! src/pkg/__pycache__/` and no header; checked on Git 2.43.0 on 2026-10-21 |
| Git's own documentation at `v2.36.0`: `Documentation/config/status.txt`, `Documentation/git-status.txt`, `Documentation/RelNotes/2.14.0.txt` and `Documentation/RelNotes/2.35.0.txt` (B-47) | `status.showStash`, which "Defaults to false", makes `git status` show the number of stash entries, added in 2.14.0; porcelain v2 prints `# stash <N>` "If `--show-stash` is given", added in 2.35.0; so the setting and the header both exist at the Git 2.36 floor, and so does the pin that turns them off |
| `os.access(name, os.W_OK \| os.X_OK, dir_fd=fd, effective_ids=True, follow_symlinks=False)` on a directory of a read-only bind mount that the running user owns (B-51) | false, `faccessat` failing with `EROFS` (errno 30); on Linux 6.18 with glibc 2.39 and Python 3.12.3, on 2026-10-21 |

## Goals / Non-Goals

**Goals:**

- Admit a merged worktree whose only ignored content is Python bytecode, with
  no change for any repository whose worktrees hold no ignored file: same plan,
  digest, question, stages and exit status as change 1 (D5, D11); where
  cache-only rows that a gate after `deferred-target-cap` excludes take target
  places, a worktree with no ignored file behind them is deferred where change 1
  selected it (Risks, B-56).
- Delete nothing that the confirmed plan did not list, never through a symbolic
  link, never outside the worktree, never recursively, and say exactly what was
  and was not deleted when a stage stops (D7, D8).
- Keep change 1's bounds: the 50 s work deadline, the 64 s run bound, the
  removal floor, at most six children per revalidation, seven where the plan
  read `extensions.worktreeConfig` as true, and nine and ten where the path of
  the repository's root or of its common directory holds a line feed, as PR #19
  states them at `173d83c` and `2250830`, as at `b3228bb` (B-54, B-58, B-60,
  B-84, B-88, B-93, B-99, B-104), and the fit (D4, D12).

**Non-Goals:**

- Any cache kind but `__pycache__`, `.pyc` and `.pyo` (`.pytest_cache` is
  before Brett Heap, recommended against for this change, B-50); any disposal
  without the worktree's removal; any change to `status`, `doctor` or what `project
  overview` collects (only its equality clause gains the cache exception, D6);
  configurable caps or allowlists; continuing past a failed target.

## Decisions

### D1. The cache stage in the removal sequence

For a selected target whose `cache_disposal.paths` is not empty,
`retire_worktree` runs, in this order:

1. the targeted revalidation of change 1, with D10's status child in place of
   the combined probe;
2. the slot check that change 1 already makes before a spawn, and the start
   condition: more than `removal_floor_seconds` of the work deadline left;
   otherwise the target and every later one are `not-attempted` with
   `interrupted` or `deadline-exceeded`, and nothing is deleted;
3. the whole-list preflight (D7), which also keeps the run's byte total
   (B-26), then the reopening of the first listed cache's chain; a read of
   either that the floor or the deadline stops ends the stage with step 2's
   outcome, nothing deleted, never `refused` (B-34), and a signal recorded by
   the time the stage classifies any outcome of either, a difference, an error,
   a byte total past a cap, a read past its own 5 s budget or a stop by the
   floor or the deadline, is checked first and gives step 2's `interrupted`
   outcome in its place (B-39, B-41);
3a. immediately before the hand-off of the first removal, the floor and slot
   checks of step 2 again, with the same outcome; a signal recorded after this
   check is handled as one received during the removals (B-17), and the
   hand-off that follows is the stage's first removal for every rule of the
   two ADDED requirements (B-16);
4. the removals (D7), each handed over only while more than the floor remains
   and waited for until it returns (D12), then, on any failure, the rescan
   (D8);
5. change 1's floor and slot checks, then the spawn, the wait and the
   reconciliation, unchanged; a target whose stage ended `disposed` and whose
   spawn these checks refuse is `not-attempted`, with its reconciliation (D8).

A target with no listed cache skips steps 2 to 4, so its sequence is change 1's
exactly. The one clause inserted into "Clean can explicitly retire verified
worktrees" names steps 2 to 4 as one step; the ADDED requirement holds the
rest.
Nothing runs between step 4 and the spawn but the checks of step 5, so the
revalidation that the narrow guarantee names is, for a cache target, the one of
step 1, as the MODIFIED "Cleanup states a narrow guarantee and its residual
window" states (B-10; D13).

### D2. The allowlist, candidates and blocking paths

A listed cache is decided from Git's record and from `lstat` results read
without following a symbolic link (D3, D7), by byte comparison only: a directory
record whose last component is exactly `__pycache__`, whose walk finds only
regular files whose names end exactly `.pyc` or `.pyo` and directories named
exactly `__pycache__` that pass the same walk; or a file record whose name ends
exactly `.pyc` or `.pyo` and whose `lstat` is a regular file. Python's own
temporary names (`*.pyc.<number>`, left by an interrupted write) and any
`__PYCACHE__` on a case-insensitive filesystem are blocking, and so is an
entry of a listed directory whose name is not valid UTF-8, whatever its suffix
(B-51, RB's LOW-5). A record's parent
directories may have any name (the `bb91a49` review finding at `project:759`
of that commit, where a parent not named `__pycache__` was refused after
confirmation); each must be a non-symlink directory on the worktree root's
device (CD-8), recorded in `directories` (D5), and so must a listed cache
directory and every directory inside it, since a mount there passes every
check of its parents (B-48, RB's MEDIUM-1).

A candidate is decided from evidence the plan already holds before any
enumeration: the combined probe established `dirty` false with at least one
ignored record; the sample test passes; with the ignored-files rung skipped,
the pure ladder gives `merged-removable`; and the gates before
`deferred-target-cap` pass (`main-worktree`, `unsupported-path-bytes`,
`registration-mismatch`, `locked-worktree`, `not-requested`, and the reflog
gate, read for the candidate as change 1 reads it for each row it checks: one
more bounded filesystem read of at most 64 KiB and no Git child). In single
mode only P can pass `not-requested`. The plan takes candidates in canonical
order and enumerates the first 16 (D4).

The gates after `deferred-target-cap`, `contains-submodule`,
`hidden-local-state`, `operation-in-progress` and `worktree-only-commits`, which
the batch block defines on PR #19's text (B-69), are not part of the candidate
test: the hidden-state
probe and D21's reachability probe that they read each cost a Git child a row,
which change 1 runs only for the 16 rows past the cap (PR #19's D12, its
design.md:863-881 at `4f1c0e0`). So a candidate that one of them excludes, a
cache-only row holding an initialized submodule among them, is enumerated,
passes the `ignored-local-files` rung, and holds one of the 16 enumerations and
one of the 16 target places, as change 1's index-gate rows hold theirs; it
counts as held for a persistent reason (D4, D11), and its entries and bytes
are not counted toward the invocation's totals (D4). Codex's P2 at
`specs/project-clean/spec.md:866` on `d4e960b` found the candidate test
admitting such rows, and reader RG's trace found them holding the totals as
well (B-56).

The sample test (B-12) is a pure function of the row's `ignored_samples`, the
up to 8 ignored paths that change 1's incremental status parser keeps (CAS
design.md:164-171), which it takes as Git prints them, in path order (Context):
a sample that is not valid UTF-8, or whose last component, a
trailing `/` disregarded, is neither exactly `__pycache__` nor a name ending
exactly `.pyc` or `.pyo`, is blocking whatever it holds, so the row is not a
candidate. It stays `ignored-local-files` with `not-candidate`, its counts
`null`, and its rejected samples in `blocking_samples`, so the preview can name
the path that keeps it. The test spends no child and no filesystem call, and it
keeps every row with a sampled `local.env` out of the 16 enumerations (D4).

A row that holds ignored records and passes the sample test but is still not a
candidate carries `candidate_block` (B-24): the class the pure ladder gives it
with the ignored-files rung skipped, when that class is not `merged-removable`,
or else the first gate before `deferred-target-cap` that it fails. The candidate
test already computes both: the ladder's inputs are the repository-wide ref
listing and merged set and the row's own combined probe, and the gates before
`deferred-target-cap` read the registry, the lock, the path's bytes and the
reflog file, which the candidate test reads for exactly the rows whose answer
depends on it. So `candidate_block` spawns no Git child, and there is no gap to
record. Its values are existing class names and gate reasons (L-4, CD-16). The
preview prints it after the unknown counts (D11), so that a detached,
unpublished or unmerged row whose sampled ignored files are all caches is told
what really keeps it rather than to delete its caches; squash-merged worktrees
are among those rows while question 2 is open. Every other row carries
`candidate_block` null.

A record is blocking when it is not a listed cache. A directory record stops its
walk at the first entry that is not allowed, and counts once as blocking. Up to
8 blocking records are kept, in the order Git prints them, as
`blocking_samples`.

### D3. The cache enumeration's child and parser

The child is a D2 handle of change 1's kind `probe`: the scrubbed environment
with `GIT_OPTIONAL_LOCKS=0`, the seven protocol pins, the four status pins
that every status probe carries (PR19/cmd:158-164 at `f0bf538`; LQ-10), `-c
core.untrackedCache=false -c core.fsmonitor=false -c core.trustctime=true -c
core.checkStat=default`, its own `-c status.showStash=false`, and `-C
<worktree>` after the row's identity check, with the argument vector `status
--porcelain=v2 -z --untracked-files=normal --ignored=matching`.
`--untracked-files=normal` is there because Git refuses `--ignored=matching`
otherwise (Context; CD-5), as a user's `status.showUntrackedFiles=no` would
make it. `-c status.showStash=false` is this child's own pin (B-47, RB's
HIGH-1): under a user's
`status.showStash=true`, porcelain v2 prints `# stash N` before the records
whenever the repository holds a stash, and a stash is repository-wide, so
without the pin every candidate of such a repository would read another record
type and be `cache-unverified`, and every revalidation of a cache target would
refuse, nothing ever being disposed of (Context). Git documents the setting
from 2.14 and porcelain v2's header from 2.35, so both, and the pin, exist at
the 2.36 floor (Context). Change 1's combined probe is porcelain v1, which
prints no such header, so the evidence model's pins stay as change 1 has them;
the revalidation of a cache target runs this same child (D10), pin included.
The four status pins are not this child's own: at that revalidation it stands in
for the combined status probe (D10), so it carries what that probe carries. With
only the first two of those pins, an edit that keeps a tracked file's size and
restores its mtime would read unchanged under a user's `core.trustctime=false`
or `core.checkStat=minimal`, the cache stage would run, and only Git's own check
on the removal, which carries all four pins (PR19/pc:333-334 at `2250830`,
:310-311 at `173d83c`), would refuse, the worktree kept and its caches gone
(reader RH's M1; B-69).

A sixth incremental parser, beside change 1's five, reads porcelain v2 with
`-z`: an ignored record is `! `, then a NUL-terminated path, a directory's path
ending `/`; any other record type (`1`, `2`, `u`, `?`) sets an `other` flag and
stops the child, since the combined probe had established `dirty` false and the
row has changed under the plan. The parser stops at the 513th record, holds at
most one partial record, and is fed byte by byte and whole in its tests, as
change 1's parsers are. Git prints changed and untracked entries before ignored
ones, so a non-ignored record arrives first when there is one. A `#` header
that arrives all the same is another record type and fails closed. So is an
ignored record whose path, its trailing `/` disregarded, begins with `/` or
holds an empty, `.` or `..` component (B-51, RB's LOW-1): real Git prints
none, but a `git` wrapper on PATH or a test fake could, and a walk written to
the bare rule would open `..` relative to the root, which is no symbolic link
and is on the root's device, and so leave the worktree; the row is
`cache-unverified`, and the walk opens nothing.

The walk then takes the records in canonical order, depth-first: it opens each
directory it records once, from the worktree root down, relative to its
parent's descriptor and checking that it is a non-symlink directory on the
root's device, keeping open only the directories above the current record; it
`lstat`s each listed file relative to its parent, enumerates each listed cache
directory (below), `lstat`s each entry relative to it and descends into each
entry named `__pycache__` that is a directory, counting every object it
records, entries and directories alike, toward the per-worktree cap of 512
(B-33), summing the regular files' `st_size`, and stopping at the first entry
outside the shape or at a per-worktree cap. Opening each recorded directory
once keeps the walk's opens within its recorded objects, where a chain per
record would cost depth times records (D4). An open that the no-follow rule
refuses at plan time, a directory on the way down replaced by a symbolic link
after the child printed its records, since Git never prints a path below a
symbolic link, is a failed call of the walk: the row is `cache-unverified`,
its counts null, and nothing is counted blocking for it (B-51, RB's LOW-5). A
symbolic link that the walk's `lstat` shows, the listed path itself or an
entry inside a listed directory, stays blocking, as do an entry whose name is
not valid UTF-8 and a listed or nested directory on another device (D2).

A directory is enumerated by `os.scandir` on its descriptor, iterated lazily,
one entry at a time, and closed as soon as the cap decides, at the row's 513th
recorded object, and never by `os.listdir`, which builds the whole directory's
listing before the cap can act, so that a `__pycache__` of millions of entries
could take unbounded memory, which a timeout, abandoning the worker, cannot
reclaim (B-44, Codex's P2 at `specs/project-clean/spec.md:873` on `e399309`).
Each bounded enumeration is one call on the worker under the per-call budget,
as a listing was: it takes entries until the directory ends or the cap decides
and closes the iterator before it returns. No enumeration holds a whole
directory's listing, so a row's walk holds at most 513 entries whatever a
directory holds, and a call abandoned at its budget holds no more, since the
cap still closes it. CPython's `os.scandir` of a descriptor works on a
duplicate of it and rewinds it on close, so the walk's own descriptor stays
usable for the `lstat` calls and the descent that follow (Context). The
whole-list preflight enumerates the same way (D7).

For a row whose walk finished with `blocking` 0 and within the per-worktree
caps, the walk then checks each directory that its stage would change, each
listed cache directory, each nested `__pycache__` and the parent of each listed
path, with `os.access(name, os.W_OK | os.X_OK, dir_fd=parent,
effective_ids=True, follow_symlinks=False)`, one filesystem call under the
per-call budget (B-20). A false result leaves the row `ignored-local-files`
with `cache-unwritable`, its counts, paths and directories established; it is
not selected, its entries are not counted toward the invocation's totals, and
it stops nothing, by the principle of A-17 for a refusal the plan can see. Its
line names the first, by raw path bytes, of the directories whose check was
false, relative to the worktree and `.` for the worktree itself, so that the
person fixes the directory that the check tests: a mode change of the worktree
alone leaves the check false for a `__pycache__` of mode 0555 (lane 3's F-12,
B-72). The walk keeps that path in the row's evidence for the line, and no JSON
key carries it. A
`__pycache__` that a root-run container or `sudo python` wrote is the usual
cause; none was found on this workstation (the council's measurement of
2026-10-19). A check that times out leaves the row `cache-unverified`, as any
walk call does. The check sees a read-only filesystem: on Linux 5.8 or later,
where the C library makes the effective-ids check with the `faccessat2` call,
it returns false with `EROFS` for a directory of a read-only mount, so such a
row is `cache-unwritable` at plan time and never reaches a stage. That was
observed on Linux 6.18 with glibc 2.39 on 2026-10-21, for a directory of a
read-only bind mount that the running user owns (Context; B-51, RB's LOW-2);
an older kernel or C library was not checked, and where the check misses it
the stage refuses as below. The check returns a boolean and no error number, so
it cannot tell a read-only filesystem from a mode or an owner, and the row's one
next step, to fix the ownership or mode, cannot work on a read-only mount, where
`chmod` and `chown` fail with `EROFS` (lane 3's F-11, reasoned and not
reproduced; B-72). The line therefore stays one general line and names both
remedies, to fix the ownership or mode of the directory or, on a read-only
filesystem, to remount it writable (B-74). Telling the two apart would take one
more call a directory, `os.statvfs` on the directory's descriptor and its
`ST_RDONLY` flag, which moves B-25's call counts and the fit, and this change
does not add it. What the check cannot see fails the stage's first
removal instead, which then ends the stage `refused` with `cache-changed` and
nothing deleted (D8): an entry that is not the running user's in a sticky
directory that is not the user's, an append-only or immutable attribute, a
security module's refusal, and a filesystem made read-only, or a mode or an
owner changed, after the plan. B-20 first named a read-only filesystem among
these; its decision stands on the cases above, each a refusal that the plan
cannot see. A sticky directory is computable from what the walk already reads,
the directory's `S_ISVTX` and owner and each entry's `st_uid` against the
effective uid, but the check does not add it: such a target fails closed,
`refused` or `partial`, never deleting anything but cache entries: `refused`,
nothing deleted, when the stage's first removal meets an entry the user does
not own, and `partial` when the user's own entries in that directory come
first (D8; B-53, lane 3's LOW 5). So the case is no safety gap, and
B-51 changes behaviour only to close one; each run then stops at that target,
and its line names it.

### D4. The caps and the fit

| Limit | Value | Scope | Reached |
| --- | --- | --- | --- |
| `cache_rows` | 16 | enumerations per invocation | later candidates `cache-cap` |
| `cache_entries` | 512 | Git records, and recorded objects, the cache entries and every directory the plan records (B-33), per worktree | `cache-cap` |
| `cache_bytes` | 268,435,456 (256 MiB) | `lstat` sizes of regular files per worktree | `cache-cap` |
| `cache_entries_total` | 4,096 | cache entries over the invocation's cache-only rows, but those that a gate after `deferred-target-cap` excludes (B-56) | that row `cache-cap`, its entries uncounted |
| `cache_bytes_total` | 1,073,741,824 (1 GiB) | bytes, likewise, and at each cache stage's preflight the bytes it measures (B-26) | likewise; at a preflight, that target `refused` with `cache-changed`, where no signal was received first (B-41) |

A cap reached keeps the row `ignored-local-files` and the plan complete, so the
batch removes everything else. A later run takes the rows that
`deferred-target-cap` defers as the rows ahead of them are removed or excluded
by a gate before the cap, as PR #19's deferral drains (PR19/pc:1059-1073 at
`2250830`, :1025-1039 at `b3228bb`, as at its round (c)); the candidates that
the invocation's totals leave as the candidates ahead of them are removed,
cease to be candidates or cease to count toward those totals (round B13, W33's
M-1); and, unless each of the 16 enumerated candidates is held for a persistent
reason, the candidates past the 16th as the candidates ahead of them are
removed or cease to be candidates; each unless the rows that
`deferred-target-cap` defers will not drain, which change 1's line then names
(B-56). A candidate that a gate after `deferred-target-cap` excludes stops
counting toward the totals (T2) but keeps its place among the 16, so it frees
room in the totals and no place, which is why only the totals' drain names it
(B-62). The rung does not free an enumeration (round B12): a candidate left at
the rung keeps its place among the 16, though the classification, a gate before
`deferred-target-cap`, excludes it, as change 1's index gates keep theirs, and
one that passes the rung and that a gate after `deferred-target-cap` then
excludes keeps it in just that way (D2). The sample
test (D2) keeps out every row whose samples show a blocking name; what can
still hold a place is a candidate whose samples all have cache names while it
holds a blocking path beyond its 8 samples, a cache-named path that is blocking
by its type, contents or device (a symbolic link named `__pycache__`, a
`__pycache__` holding `notes.txt`, a mount), more than a per-worktree cap
allows, an enumeration that failed, or a directory the user cannot change
(B-20), and, past the rung, a candidate that a gate after the cap excludes,
which no test before the enumeration sees (D2). The stall line (B-21, D11) is
printed only when each of the first 16
candidates in canonical order is held for a persistent reason, any one of
these: at the rung, `blocking` above 0, `cache-cap` from a per-worktree cap,
`cache-unverified` or `cache-unwritable` (B-32); or, past the rung, an
exclusion by a gate after `deferred-target-cap` (B-56), and when, besides those
16, at least one later candidate is left with `cache-cap` by the 16-enumeration
cap, a row the line can name as held back (B-45, Codex's P2 at
`specs/project-clean/spec.md:928` on `e399309`). With exactly 16 candidates,
each held so, no row waits behind them: each row's own reason and next step
print as usual, and no stall line prints. The test reads those reasons
and never `blocking` alone, which is null for `cache-cap` and
`cache-unverified` and 0 for `cache-unwritable`, so that sixteen rows held by
those three print the line too (Codex's P2 at `specs/project-clean/spec.md:910`
on `cf57956`). The report tells a per-worktree cap from the invocation's totals
by the counts the row already carries: a per-worktree cap stops the enumeration
and leaves them null, while a row left only by the totals keeps them
established, `blocking` 0, and drains as the rows ahead of it are removed or
excluded by a gate before the cap, printing none, since the totals leave out a
row that a gate after the cap excludes, which could otherwise hold them on every
run (below; reader RG's W1, B-56); the 16-enumeration cap leaves only candidates
past the 16th. One run
cannot tell that an enumeration "fails each time", so a `cache-unverified` row
is named as one to re-run and, if it repeats, to inspect, never as one to remove
by hand. Bytes are the apparent sizes
that `lstat` reports at plan time; a sparse file counts at its apparent size,
which only errs toward a cap.

The invocation's byte total is applied twice. At plan time the totals count,
in canonical order, the planned entries and bytes of the rows that pass every
per-worktree check (the `cache-cap` rule). They leave out a row that a gate
after `deferred-target-cap` excludes, which holds no target and whose caches no
stage removes, so that rows of that kind ahead of a cache-only row never keep
it at `cache-cap` on every run (T2; reader RG's W1, B-56); rows that
`deferred-target-cap` defers still count, which errs on the safe side, and the
selected rows' totals stay within 4,096 entries and 1 GiB. The plan applies
those gates to each row that reaches them before it applies the totals to any
later row: one pass in canonical order. Feature 004's planner
(`origin/004-project-clean-all-safe` at `881119b`, `project`:4270-4279 and
:4420-4441) runs its gates 1 to 7 over every row, then gate 8,
`deferral_gate()`, over the rows that pass them, then gates 9 to 11 for the 16
it takes. This change's feature runs as one pass, row by row in canonical
order, every gate from the row's classification when it is not
`merged-removable` through `worktree-only-commits`, the last of PR #19's list
at `b3228bb` (PR19/pc:682-689): the classification, `not-requested`,
`unstarted-branch` or `reflog-unavailable`, `deferred-target-cap`, its count
kept inline, `contains-submodule`, `hidden-local-state`,
`operation-in-progress` and `worktree-only-commits`. Those are feature 004's
gates 5 to 11 at `881119b`, which has no `worktree-only-commits` gate yet, and
5 to 12 since `93a3ae9`, where LQ-13's gate merged into feature 004, whose
numbering this follows. No child is added: the gates
after the cap still run for at most 16 rows, only in another order. At each
cache stage the preflight
applies the byte total again, to the sizes it measures (B-26, Codex's P2 at
`specs/project-clean-review-safety/spec.md:341` on `90d18ee`): a `.pyc`
recompiled in place keeps its name, its type and its cache's number of
entries, so it passes the revalidation and the preflight's count, but it can
grow, and five targets planned with tiny caches could each reach the 256 MiB
per-worktree cap, 1.25 GiB in all. So the preflight keeps the run's byte
total, the bytes it measures for this target added to those it measured for
every earlier target whose stage passed its preflight in this run, and a
target whose bytes would take that total past 1 GiB ends `refused` with
`cache-changed`, nothing deleted, as one past the per-worktree cap at its
preflight does; the run then stops at that target (CD-1), exit 2, and the
earlier targets keep their results. Where a signal was received before the
stage classified that outcome, the signal decides instead, as for every
outcome of the preflight (B-41, D7): the stage is `not-attempted` with
`target-stopped`, nothing deleted, the target and every later one
`not-attempted` with `interrupted`, and the exit status the signal's (B-43,
lane 3's LOW 3). Entries need no running total, since the
preflight requires each listed cache's entries to equal the plan's, whose sum
the plan already capped at 4,096. The check adds no filesystem call: the
preflight already `lstat`s every entry it re-lists.

The fit is change 1's as PR #19 states it at `4f1c0e0` (its design.md D14,
lines 898-1062; `BA:729-735`), on the first of its three bases, the packet's
flat 150 ms per Git child (its :905-907) and 0.3 s per removal, with the
enumerations added, for a plan that read `extensions.worktreeConfig` as false
(B-54, B-58, B-60, B-76; the same rows and figures on `f0bf538` in rounds B13
to B15, on `9267303` in round B12, on `2e819ad` in round B11 and on `a664799`
in round B10, and other rows on `c462d87` before it):

| Mode | Children | Time | Fits the 50 s work deadline |
| --- | --- | --- | --- |
| all-safe, 128 rows, 16 enumerations, 16 targets | 8 + 128 + 16 + 16 + 16 + 96 + 3 = 283, and 16 removals | 42.45 s + about 4.8 s = 47.25 s | no for the Git children and removals: the 15th target reaches its cache stage or spawn after 274 children and 14 removals, at about 45.3 s, and the 16th after 280 children and 15 removals, at about 46.5 s, with 3.5 s left, so 14 of 16 reach it before the spawn limit, before the walk's and the stages' filesystem time; with that time at B-25's bound, 11 of 16 at the top of the measured cost (below); in B-33's worst shapes fewer, or none at a thread per call (below) |
| report, 256 rows | 8 + 256 + 16 + 16 + 16 = 312 | 46.8 s, plus the walk's about 2.0 s (B-25): about 48.8 s, and 46.8 + 5.6 = about 52.4 s at a thread per call | yes for ordinary trees through one worker; no at a thread per call, and in B-33's directory shape at no measured cost (below) |
| single, 128 rows plus P | 8 + 129 + 1 + 1 + 1 + 6 + 3 = 149, and 1 removal | 22.35 s + about 0.3 s | yes |
| all-safe, one enumeration per candidate (no `cache_rows`) | 8 + 128 + 16 + 16 + 127 + 96 + 3 = 394 | 59.1 s + 4.8 s | no |
| report, likewise | 8 + 256 + 16 + 16 + 255 = 551 | 82.65 s | no |

The last two rows are why CD-6 adds `cache_rows`. A cache stage spawns no
child. In each of its two passes, the preflight and the removals, it opens one
chain per directory that holds a listed path (B-33): the worktree root by its
path and each directory below it down to that one, each open checking its
identity, and then the listed caches in that directory from its descriptor.
Beyond the chains it makes two calls per cache entry that is a file (its
`lstat` at the preflight, its unlink after it) and five per one that is a
directory (its `lstat`, open and bounded enumeration at the preflight, its open
and removal after it). For an ordinary tree, `__pycache__` directories of
`.pyc` files under package directories a few levels deep, that is about 1,100
calls for 512 entries and about 8,500 for the 4,096 of a run. The plan-time
walk makes one call per directory open, per bounded enumeration and per entry
`lstat`, and one access check per directory a stage would change (B-20); it
opens each directory it records once and counts every directory it records
toward the per-worktree cap with the entries (D3, B-33). It walks more than
the stages remove: each of the 16 enumerated rows can be walked to its
per-worktree cap of 512 recorded objects before the invocation's totals reject
it, and a row that the totals reject is uncounted from the 4,096 but was walked
(B-25, Codex's P2 at `design.md:294` on `90d18ee`). The walk's bound is
therefore 16 x 512 = 8,192 recorded objects: about 9,000 calls for ordinary
trees, whose objects are
mostly files, and at most four calls an object, a nested `__pycache__`
directory's `lstat`, open, bounded enumeration and access check, about 32,800
where every object is a directory. A directory's streaming enumeration, closed
when the cap decides (B-44, D3), counts as one call under the per-call budget,
as its listing did, so no call count, time or fit of this section moves: the
stages' 1,100 and 8,500 calls, the walk's 9,000 and 32,800, the 683 calls a
row and the 43,947 opens a pass of B-33's chains are as before, and so are
A-9's and B-3's fits.
Through one daemon worker per stage (D12), the hand-off measured 169-224 us a
call at load 30 to 37 on this workstation, and 393-622 us for a thread per
call, the shape of feature 004's `fs_call` (`clarifications.md`, S-4): at
224 us, 8,500 stage calls take 1.9 s and the walk's 9,000 take 2.0 s, about
2 s each; at 622 us, a thread per call, 5.3 s and 5.6 s. A 512-entry stage
took about 0.25 s here (AE-4's 1,248 calls in 236 to 273 ms).

B-54 restates the fit on PR #19's text, on which this change's bounds block and
revalidation block are written since round B10 (reader RF's H1), first at
`a664799`, its round (b), in round B11, at `2e819ad`, its round (c), in round
B12, at `9267303`, its round (d), and, in round B13, at `f0bf538`, its round
(e), and its other six blocks since round B15 (B-69), and round B16 re-bases
classification on `6bf9f77`, its round (g3), and the retire, batch, bounds,
reconcilable-result and revalidation blocks on `b3228bb`, its round (h) (B-76,
B-80, B-84), round B17 the retire and reconcilable-result blocks on `e0c91bb`,
its round (i) (B-87), round B18 those two and the revalidation block on
`e14ada0`, its round (j) (B-88), round B19 the retire and revalidation blocks
on `173d83c`, its round (k) (B-93), round B21 the bounds block on `20084cd`,
its round (m) (B-99), and round B22 the retire, reconcilable-result and bounds
blocks on `2250830`, its round (n) (B-104), whose D14 and task 2.1 cite here at
`4f1c0e0` are its round (f)'s at `662be89`, byte for byte, the strings quoted
here unchanged at `88d0d36`, its round (o) (B-107); on its 150 ms basis every
figure of this paragraph for a plan that read `extensions.worktreeConfig` as
false is unchanged, none of the six and no change of rounds (g) to (o) to its
spec text or its D14 stating a count of children or a time, save round (h)'s
count for a path that holds a line feed, below. PR #19's D14 (its
design.md:898-1062) has F = 8, D21's reachability probe for at most 16 rows,
and six revalidation children a target, seven where the plan read
`extensions.worktreeConfig` as true (PR19/pc:1082-1090 at `2250830`,
PR19/rs:76-79), and since round (h) nine and ten, with a final rescan of six,
where the path of the repository's root or of its common directory holds a line
feed (its design.md:976-987 at `b3228bb`), a case that this section's
arithmetic, which is for paths without a line feed,
does not count (B-84): where it read it as false, 8 + 128 + 16 + 16 + 96 + 3 =
267 children, the 16th removal spawning at 44.1 s with 5.9 s left, by the
formula this section uses, on that basis (its design.md:913 and :931-935). With
this change's 16 enumerations, target k reaches its cache stage, or its spawn,
after the 184 planning children (8 + 128 + 16 + 16 + 16), the 6k revalidation
children of it and the targets before it, and k - 1 removals, at 0.15 x (184 +
6k) + 0.3 x (k - 1) = 27.3 + 1.2k s: the 14th at 44.1 s, the 15th at 45.3 s and
the 16th at 46.5 s, so at the packet's model 14 of 16 targets reach their stage
before the spawn limit before any filesystem time is counted, as the table's
first row says. With the walk and the stages at B-25's bound, through one
worker, 11 of 16 do at 224 us a call, or 12 with the 8
cache targets last, and 12 at 169 us; at a thread per call 6 do with the 8 cache
targets first, and 9 with them last. On PR #19's measured basis, D5's, task
2.1's warm medians with the 1.5 margin at 10,000 files, with the two children
it did not measure, LQ-11's work-tree probe and LQ-13's `rev-list`, at the
8.7 ms and 160.3 ms with the margin that LQ-20's step (i) measured (its
design.md:951-968; `tasks.md`:148-158), its 16th removal spawns at 28.7 s
where the plan read `extensions.worktreeConfig` as false, D21's 32 children
counted there at 5.1 s (its design.md:994 and :1031-1036); the enumerations'
at most 3.7 s and the walk and the stages bring the 16th to about 36.3 s
through one worker and about 43.3 s at a thread per call, so all 16 fit on
both, and with PR #19's 20,000-file removals, its 16th at 36.4 s, to about
44.0 s through one worker, where all 16 fit, and about 51.0 s at a thread per
call, past the work deadline, where 12 of 16 fit with the 8 cache targets
first and 13 with them last. At `f0bf538`, with D21's children at the full ref
listing's stand-in, 11.5 s, this sentence read 35.1 s, 42.7 s and 49.7 s, and
42.8 s with 20,000-file removals, the 16th past the spawn limit through one
worker; at `a664799` it added D21's 7.7 s without the margin to task 2.1's
23.6 s, which carries it (its `tasks.md`:129-130), and read 38.9 s and 45.9 s.
Where the plan read `extensions.worktreeConfig` as true, PR #19's D14 gives
the 128-row case on three bases (its design.md:992-997): on the 150 ms basis
no removal, the first due at 45.3 s, and on the mixed basis as first stated
11, the rest `not-attempted` with `deadline-exceeded` and the run exiting 1,
never unsafe; on its measured basis, D5's as ratified, all 16, the first
spawning at 14.55 s and the 16th at 30.0 s with 20.0 s left, and with
20,000-file removals all 16 as well, the 16th at 37.7 s (its
design.md:968-976). Its open question LQ-20 is resolved: Brett Heap chose its
step (i), to measure those two probes, on 2026-10-22 (the lead's R-236), the
case passes on the measured basis, and options (a) to (d) are not taken, their
results kept as the record of what was costed (its design.md:999-1029 and
:1831-1893). On those measured costs this change states its own figure (B-65),
by the method above, which costs the enumeration's child at a cache target's
revalidation as the status probe whose place it takes (D10), 74.1 ms with the
margin (its design.md:955). PR #19's targets there come (30.0 - 14.55) / 15 =
1.03 s apart, or (37.7 - 14.55) / 15 = about 1.54 s with 20,000-file removals,
and 8.7 ms less a target, one work-tree probe fewer, where the plan read the
setting as false. Through one worker at 224 us, the 16 enumerations' at most
3.7 s and the walk's 2.0 s and the stages' 1.9 s at B-25's bound bring the
16th to its stage or spawn at 30.0 + 3.7 + 2.0 + 1.9 = about 37.6 s, with
12.4 s left, and at a thread per call, 5.6 s and 5.3 s, at 30.0 + 3.7 + 5.6 +
5.3 = about 44.6 s, with 5.4 s left, so all 16 fit on both. With 20,000-file
removals the 16th comes at 37.7 + 3.7 + 2.0 + 1.9 = about 45.3 s through one
worker, past the spawn limit, so 15 of 16 fit, the 15th by about 43.8 s, and
the 16th is `not-attempted` with `deadline-exceeded`, the run exits 1 and the
next run takes it, never unsafe; at 169 us all 16 fit, the 16th at about
44.3 s; and at a thread per call the 16th would come at about 52.3 s, past the
work deadline itself, so 11 of 16 fit with the 8 cache targets first and 12
with them last. Beside these figures stands a conservative variant (B-79),
which costs that child as an enumeration, at most 3.7 / 16 = about 0.23 s, so
that each of the 8 cache targets' revalidations takes about 0.16 s more and
the 16th comes about 8 x 0.157 = 1.3 s later. With 10,000-file removals the
16th then comes at about 38.9 s through one worker, all 16 fitting, and at
about 45.9 s at a thread per call, past the spawn limit, so 15 of 16 fit, the
15th by about 44.8 s, and the 16th target is `not-attempted` with
`deadline-exceeded` and waits for the next run, exit 1, as every target the
deadline leaves does. With 20,000-file removals it comes at about 46.6 s
through one worker, so 14 of 16 fit with the 8 cache targets first, the 15th
due at about 45.0 s, and 15 with them last, at about 45.6 s at 169 us, 15 of
16, and at about 53.6 s at a thread per call, 10 or 12 of 16. Where the plan
read the setting as false, the variant gives about 37.6 s and 44.6 s, all 16,
and with 20,000-file removals about 45.3 s through one worker, 15 of 16, and
about 52.3 s at a thread per call, 11 or 13 of 16, 11 with the 8 cache targets
first and 13 with them last, by this section's rule that a target counts when
it reaches its cache stage, or its spawn, by the spawn limit: with them last
the 13th, a cache target, reaches its stage at about 44.6 s, and its stage,
which ends at about 45.2 s, leaves its removal to the next run with exit 1
(W79's LOW-1, B-86). Task 2.3's measurement of the
enumeration settles which cost holds, and neither set of figures is chosen
before it. The paragraphs of this section that
follow keep their arithmetic on change 1's terms at `c462d87`, F = 7 with no
reachability probe and five revalidation children a target, where target k
arrives at 24.75 + 1.05k s, 2.55 + 0.15k s earlier than at `4f1c0e0` on its
150 ms basis, as at `f0bf538`, and the report mode's Git children take 2.55 s
less; each count of targets there is therefore an upper bound on that count at
`4f1c0e0`, and the counts of this paragraph are the ones that the Open
Question on the caps cites.

The fit for ordinary trees, restated with those costs, with the walk's bound of
B-25 and with the stage's removals waited for (B-16); B-33's worst case follows
it. At the packet's 150 ms model, target k
reaches its cache stage, or its spawn when it lists no cache, after the 167
planning children (7 + 128 + 16 + 16), the 5k revalidation children of it and
the targets before it, and k - 1 removals: at 0.15 x (167 + 5k) + 0.3 x (k - 1)
= 24.75 + 1.05k s, plus the walk and the earlier stages. A stage starts only
while more than the 5 s floor remains, and a removal child is spawned only
while at least that floor remains, so each must come by about 45 s, the spawn
limit, the 50 s work deadline less the 5 s removal floor; "the floor" names
only the 5 s that must remain (lane 3's W36 M-A on PR #19).
The walk's bound and the stages' come together: of the 16 enumerated rows, 8
of 512 entries fill the run's 4,096 and are selected, and 8 more are walked to
the 512 recorded objects of their cap and kept by it, so 8 cache targets share
the 16 targets with 8 that list no cache. Through one worker at 224 us a call,
the 16th target, which lists no cache once the 8 stages come before it, then
arrives at its spawn at 41.55 + 2.0 + 1.9 = about 45.5 s, with about 4.5 s
left, under the floor, while the 15th arrives at 40.5 + 2.0 + 1.9 = 44.4 s,
with 5.6 s left:
15 of 16 targets reach their stage, and the 16th is `not-attempted` with
`deadline-exceeded`, exit 1, and the next run takes it, never unsafe. At
169 us a call (1.5 s of walk, 1.4 s of stages) the 16th arrives at about
44.5 s, with about 5.5 s left, and all 16 fit. At a thread per call the 16th
would arrive at 41.55 + 5.6 + 5.3 = about 52.4 s, past the work deadline
itself: with the 8 cache targets first in canonical order the 9th arrives at
34.2 + 5.6 + 5.3 = about 45.1 s, so 8 of 16 targets reach their stage, and
with them last, 12 of 16. Before B-25 these figures read about 44.6 s with
about 5.4 s left (41.55 + 1 + 2, the walk counted only over the 4,096 entries
the totals admit) and about 49.65 s at a thread per call (41.55 + 2.8 + 5.3).
So at B-25's bound the all-safe mode no longer fits at the top of the measured
cost: through one worker the floor refuses the spawn of the 16th target, which
lists no cache, at the packet's model (B-31, lane 3's delta read), and at a
thread per call as few as 8 targets reach their stage, the rest deferred to the
next run with exit 1. No cap changes (B-25): B-3 and CD-6 stay
Brett Heap's question (proposal, Open Questions), and task 2.3's measurement
decides under the rule below. At change 1's measured costs (CAS `tasks.md`
2.1: the 16th removal spawning at 23.6 s with 26.4 s left), the 16
enumerations add at most about 3.7 s and the walk and stages at most about
10.9 s (5.6 + 5.3, at a thread per call), the 16th then spawning by about
38.2 s, and all 16 fit. A removal is handed over only while
more than the floor remains and is waited for until it returns, as change 1
waits for its removal child; an unlink returns in microseconds, so in the
normal case this costs nothing, and the floor stays for the spawn. A hung
mount costs what a hung removal child costs: up to the 300 s removal ceiling,
counted from the hand-off, after which that cache is `removed: null`, the
stage ends `partial`, the later targets are `not-attempted` with
`deadline-exceeded`, and the run reconciles in its reserve, counted from the
return or the ceiling; the 64 s run bound keeps its two exceptions, a removal
in flight and a filesystem call stuck in the kernel. B-19 adds no Git child,
B-20 only filesystem calls, and B-24 none.

The worst case of B-33. Counting every recorded directory toward the 512
bounds a row's depth and its number of directories with removals, but the
stage opens one chain per such directory in each pass, so a pass costs the sum,
over those directories, of one plus each one's depth below the worktree root:
depth times directories at worst (Codex's P2 at `design.md:323` on `cf57956`).
Under the 512-object cap that sum is largest for a chain of 341 directories
whose deepest 171 each hold one loose `.pyc` (341 + 171 = 512 objects): 172 +
173 + ... + 342 = 43,947 opens per pass, and 88,236 calls for the target with
the files' `lstat` calls and unlinks, about 14.9 s at 169 us, 19.8 s at 224 us
and 54.9 s at 622 us. Sixteen such targets list 2,736 entries, within the
run's 4,096, and would need about 1.41 million calls, 239 to 878 s. Nothing is
unsafe, but no fit holds that: at 224 us the first such target reaches its stage
at about 28.3 s (the 172 Git children before it, 25.8 s at the packet's 150 ms,
and the walk of those 16 rows at 683 calls a row, 10,928 calls and 2.45 s: 341
directory opens, 171 file `lstat` calls and 171 access checks, besides the
worktree root's own open), its preflight takes about 9.9 s, and the floor ends
its removals about 7 s later, `partial`, exit 1, so each run removes part of its
caches and no worktree while it comes first; at 169 us one such target is
removed in a run, and at a thread per call its preflight alone runs into the
spawn limit, which ends the stage before its first removal with nothing deleted,
`not-attempted` with `deadline-exceeded` and no change of state (B-34). So
the fit cannot hold without a new limit. A limit on depth alone would not do:
a row 8 levels deep still holds 252 directories with removals, 2,268 opens per
pass, and 16 such targets need 72,576 opens in their two passes. The proposal
therefore puts a limit on the chains to Brett Heap beside B-3 and CD-6
(proposal, Open Questions). It recommends `limits.cache_opens`, 512 opens per
pass per worktree, the sum above as the walk computes it, past which a row
stays `ignored-local-files` with `cache-cap` from a per-worktree cap, so that a
run's chains are at most 16 x 2 x 512 = 16,384 opens, about 3.7 s at 224 us and
10.2 s at 622 us. The deltas do not add it, and no cap changes (B-33).

The other worst shape is every recorded object a directory, as in 16 rows each
holding 512 nested `__pycache__` directories, whose chains stay short. The walk
then makes four calls an object, about 32,800 calls, 5.5 s at 169 us, 7.3 s at
224 us and 20.4 s at 622 us, and the 8 targets that the totals select make
five calls an entry, about 20,500 calls, 3.5 s to 12.7 s. With those 8 targets
first, through one worker, 10 of 16 targets reach their stage or spawn at
169 us and 8 at 224 us, the 9th arriving at about 46.1 s; at a thread per call
the walk ends planning at about 45.5 s, so none does, and the report mode,
44.25 s of Git children and the walk, exceeds the work deadline, about 51.6 s
at 224 us and 64.7 s at 622 us, its plan incomplete with `deadline-exceeded`,
fitting only at 169 us, about 49.8 s. With the recommended limit as well, a
run makes at most about 69,700 filesystem calls (the walk's 32,800, the
chains' 16,384 and the stages' other 20,480), about 11.8 s at 169 us and 15.6 s
at 224 us, and through one worker at least 9 of 16 targets reach their stage
or spawn at 169 us and at least 7 at 224 us. At change 1's measured costs that
worst case adds at most about 15.6 s through one worker at 224 us, the 16th
removal then spawning by about 42.9 s, so all 16 fit, while at a thread per
call the walk alone, about 20.4 s, takes the 16th past the spawn limit. This
shape
is within the existing caps, so its remedy is B-3 and CD-6's rule below, which
task 2.3's deep-tree measurement applies; no cap changes now, and the modes of
the table above fit as it says for ordinary trees only.

Governance task 2.3 measures the enumeration, the walk at 16 rows of 512
recorded objects with the invocation's totals reached (8,192 walked, 4,096
counted; B-25), the deep-tree worst case of B-33 (the chain of 341 directories
and the rows of nested `__pycache__` directories) and the stage before the
handoff, through `fs_call`, idle and at the workstation's usual load, as
change 1's task 2.1 measured its probes; a measured cost that breaks the fit
lowers `cache_rows` in steps of 4 and the entry caps in powers of two before
the feature starts. The fit sentence of the bounds block counts the Git
children and the removals, on the packet's 150 ms basis, which it names since
round B11, with the first 14 of 16 targets starting before the spawn limit on
that count, which the block words as before only the removal floor remains,
since no spec defines the spawn limit (B-59, round B12), and the last two
`not-attempted` (lane
openRepoProject-2's check of round B10), states the walk's and the stages'
filesystem calls as
outside it, and a target whose stage or spawn cannot start under the floor is
`not-attempted` with `deadline-exceeded` as for every removal (QA-5), so the
margins above that count those calls are design arithmetic, not a promise of
the spec.

With `--retire-branches` (#23, PR #26) a run spawns branch children too. #26
stated the joint fit at `9b67e8c` (its design.md D7), under A-23, A-24 and A-25
(B-35, B-42), and has since restated it, its D7 at `7b224c7` adding PR #19's
text at `f0bf538` and its three bases, so that what follows is history, as B-35
and B-42 ruled it at `9b67e8c`, and #26's D7 holds #26's present account (reader
RH's L2). At `9b67e8c` a flagged run added at most 81 children: 64 for the
retirement stage, four for each retired branch (the re-read's listing, its
re-proof of the reflog, the branch child and the post-check), and 17 reflog
children, one for the repository and one per selected row. With this change's
walk and earlier
stages added whole as B-25 gives them, for ordinary trees, B-33's worst shapes
staying under this change's own questions (A-25), #26 said: "So at the packet's
150 ms model a flagged run with cache disposal brings 9 of its 16 targets
through their stage before the floor, 8 in the worst case of the reflog proof,
through one worker per stage, and at least 5, or 3, at a thread per call, 6, or
5, in the worst order a run can take; change 1's own deadline rule makes the
rest `not-attempted` with `deadline-exceeded`, the run exits 1, and the next run
takes them, never unsafe (`BA:772-774`). At change 1's measured costs all 16 fit
through a worker; at a thread per call at least the 16th target is deferred,
with one reflog child as in the worst case." Its bullets gave those counts as
removals and branch children. Through one worker per stage they were 10 and 9,
and 8 and 8 in the worst case of 17 reflog children; at a thread per call 5 and
5, and 4 and 3; in the worst order, which puts first the 8 cache targets that
this change's totals select, each stage spending an eighth of the stage time
just before its own removal, 6 and 6, and 5 and 5, at a thread per call, and
through a worker the counts of the first bullet. Its draft at `ca96701` read "13
of its 16 targets ... 11 in the worst case" and left the cache-stage filesystem
time out. #26, which archives after this change, states its joint fit in its
own D7 (A-9, the alignment review's G3), which stays Brett Heap's question,
`limits.targets` staying 16. The inputs it needs from this change, as rounds B3
and B4 restate them:

- Git children: 16 cache enumerations per invocation under `probes`, 2.4 s at
  the model; none added at revalidation, where the enumeration's child takes
  the combined probe's place (CD-4); and no status probe after a `disposed`
  stage, which B-19 rejected.
- Plan-time filesystem calls: the walk's at most 8,192 recorded objects, 16
  rows of 512 with the rows the invocation's totals reject included and every
  directory it records counted, each opened once (B-33), and the access
  checks, at most one per planned directory: for ordinary trees about 9,000
  calls, about 2 s through one worker per stage and up to about 5.6 s at a
  thread per call (B-25); at most four calls an object, about 32,800 calls,
  7.3 s and 20.4 s, where every object is a directory.
- Stage filesystem calls: for ordinary trees about 1,100 per target and 8,500
  per run, about 0.25 s for a 512-entry stage, about 2 s per run through one
  worker, up to about 5.3 s at a thread per call; at worst one chain per
  directory with removals in each pass, up to 43,947 opens a pass for one
  target under the 512-object cap, which the Open Question's limit would hold
  to 512 (16,384 for a run's two passes), and five calls an entry, 20,480 for a
  run (B-33).
- Start and hand-off: a stage starts, and hands over each removal, only while
  more than the 5 s floor remains; a removal handed over is waited for up to
  the 300 s ceiling and counts as a removal in flight.
- Counts: `operations.estimated` and `performed` gain one per cache entry, the
  latter only for removals that returned.
- The residual-window line of a run that selects a cache target is D13's, so a
  flagged run with a cache target re-bases its line on it.

### D5. Planned identities and the digest

The plan records, for each candidate whose enumeration finished, every
directory the stage will open below the worktree root: each directory on the way
down to a listed cache, each listed cache directory and each nested
`__pycache__` directory, as `{path, path_valid_utf8, dev, ino}`, the device and
inode from an `lstat` that follows no symbolic link. The worktree root's own
identity is change 1's `{path, dev, ino, admin_id}` of the selected entry. Each
of those directories counts toward the per-worktree cap of 512 recorded objects
with the cache entries, once however many listed paths lie below it (B-33), so
the depth of a listed path and the number of directories above the caches are
bounded with the entries.

Files carry no identity. Unlinking a name inside a directory whose identity was
just checked can only remove that name: a file replaced by a symbolic link loses
only the link, and a hard link only its name in the worktree. Python writes a
`.pyc` by renaming a temporary file over it, so a file's inode changes whenever
Python recompiles, and an identity in the plan would refuse `--expect-plan` and
the preflight for no safety gain. Each listed file is instead checked for its
type at the preflight, and each listed cache for its planned number of entries
(D7, QA-1): a `.pyc` written into a listed directory adds an entry and
refuses, while a `.pyc` recompiled in place keeps the count and passes, its
new size counted at the preflight toward the per-worktree cap and the run's
byte total (D4, B-26). A file
renamed within a listed directory keeps the count too; it is an allowlisted
cache either way, so the stage still removes nothing but caches.

The canonical text of `plan_digest` is change 1's (CAS/pc:629-632): the four
repository identity fields, the merge target's name and SHA, and the selected
`[path, branch, head]` triples. For a selected target with listed caches, its
triple is followed by its `paths` as `[path, kind]` and its `directories` as
`[path, dev, ino]`, each in canonical order by raw bytes; a plan with no such
target serializes exactly as change 1's, so its digest is unchanged (CD-14).
The MODIFIED "Clean previews and applies a batch of eligible worktree removals
in one repository" states this beside change 1's digest sentence (B-10). A new
`__pycache__` beside a listed one, or a listed directory moved out and made
again, changes the digest; a `.pyc` recompiled in place does not. Tests move a
directory out of the worktree before making its replacement, since a deleted
directory's inode number can be reused at once on ext4 (QA-6).

By decision, the digest covers each selected target's disposal decision, its
listed cache paths with their kinds and the identities of the directories its
stage opens, and not its entry counts or bytes (B-51, RB's LOW-4). Caches
change between a preview and its apply as Python runs, so a count in the
digest would refuse `--expect-plan` for no safety gain, and the apply's caps
bound the difference: the fresh plan that `--apply` builds runs the
enumeration and the walk again under the per-worktree caps of 512 recorded
objects and 256 MiB and the invocation's 4,096 entries and 1 GiB, and prints
the counts it found, and each preflight applies the byte caps again to what it
measures (B-26). A `.pyc` added after the preview to a listed `__pycache__`
therefore keeps D, and the apply disposes of it within those caps, an
allowlisted cache like the rest.

### D6. The ladder, the counts and the overview

The pure ladder gains one input per row, the cache proof, which is true only
when the row's enumeration finished with `reason` null and `blocking` 0. The
ignored-files rung tests `ignored_files` as before, except that a row with the
proof passes it. A row whose enumeration did not run or did not finish has no
proof and stays at the rung, `cache_disposal.reason` saying why; a failed
enumeration never makes the row `inspection-error` (CD-9), because its combined
probe already established its state.

`disposable` and `blocking` count Git records, which for a directory record is
one `__pycache__` tree; they can exceed `ignored_files`, which change 1 caps at
64. Both are `null` whenever the enumeration did not run or did not finish,
which is the `1789ad9` thread that APO proposal.md:804-809 hands to this
change: unknown is never printed as 0. A row with no ignored record carries no
`cache_disposal` at all (L-10, B-13): its `ignored_files` of 0 already says
there is nothing to count, and a `null` object would read as unknown.

`status` and `doctor` keep their evidence; doctor classifies no worktree.
`project overview` feeds the same ladder from evidence that has no cache proof,
so it reads a cache-only candidate `ignored-local-files` where `project clean`
reads it `merged-removable`, against change 2's equality clause
(APO/ov:381-386). The overview's suggestion for that row is then the read-only
form, whose report shows the row selectable, so no suggestion becomes unsafe.
B-14 settles the clause in this change: its `project-overview` delta appends
two sentences to the equality clause, agreed by lane openRepoProject-4 on
2026-10-19 and committed as `b4d3e12`. B-22 rewords them, since lane 3 found
cache-proven rows that `project clean` classifies `merged-removable` and then
excludes (as `contains-submodule`, `deferred-target-cap` or
`hidden-local-state`), which the first wording missed (M4), and a second
sentence that read at the gate level contradicted change 2's carried rule that
a gate finding replaces the housekeeping finding "while the classification
stays" (M5): the exception now covers a worktree that `project clean`
classifies `merged-removable` because clean's cache enumeration proved every
ignored path a listed cache, and the overview SHALL NOT classify a worktree
`merged-removable` where `project clean` classifies it otherwise for the same
working directory and refs. Lane 4 agreed the edit on 2026-10-19, with one
optional point that the committed text takes, "clean's" for "its" before
"cache enumeration", and it is committed as `9f30fb9` (`tasks.md` 2.2). B-30
adds "for the same working directory and refs", lane 4's own words of
2026-10-20, since read alone the sentence bound runs from different
directories, where the current worktree decides `merged-current` against
`merged-removable`; it is committed as `4d5855a`, the added scenario's AND
following it, and lane 4 byte-checked it on 2026-10-20 (B-36; `tasks.md` 2.2).
The council measured 3 such submodule rows on this workstation on 2026-10-19.
Feature 005's spec (`specs/005-project-overview/spec.md` on
`origin/005-project-overview` at `33a1214`, User Story 3 scenario 6) names the
`ignored-local-files` row of its "Every protected classifier" fixture by its
class only, and feature 005 has no plan or test yet. Once feature 005 has
landed, any of its tests asserting that the overview and `project clean`
classify identically gets the cache case excluded in this change's
realization, never in feature 005 (D14).

### D7. The whole-list preflight and descriptor-relative removal

Descriptor chains. Every directory is reached from the worktree root by a chain
of `os.open(component, O_RDONLY | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC,
dir_fd=parent)`, each opened descriptor checked by `os.fstat` against its
planned `dev` and `ino`. The root itself is opened by its recorded path with
`O_DIRECTORY | O_NOFOLLOW` and checked against the target's worktree identity;
the root's own ancestors are change 1's concern, checked at revalidation through
the realpath and identity comparison, so `BA:1324-1325`'s "any ancestor" is read
as any directory between the worktree root and the cache (lane 3's LOW 3). The
stage handles one directory holding a listed path at a time (B-33): in each
pass it opens the chain to that directory once, checking every identity on it,
deals with every listed path in it, reaching a listed cache directory and its
nested ones from that directory's descriptor, and closes the chain before the
next, except a descriptor given to a call still outstanding, which stays open
until `project` exits (D12). So at most that chain's descriptors and those of
the nesting below it, and those of an outstanding call, are open at once, a
number the 512-object cap bounds and an ordinary tree keeps far below any
platform's default descriptor limit; an open that fails, `EMFILE` included, is
an error like any other (D8). One chain per directory, rather than one per
listed path, is what bounds the stage's opens by depth times directories with
removals (D4).

The preflight, before any removal: for each directory holding a listed path, in
canonical order, open its chain once, checking every identity; then for each
listed cache in it: for a directory, enumerate it by `os.scandir` on its
descriptor, iterated lazily, one entry at a time, as the walk does (D3), and
close the enumeration as soon as it yields the first entry beyond the number
the plan recorded for that listed cache, which is a difference, so that no
enumeration holds a whole directory's listing (B-44); the duplicate descriptor
that CPython's `os.scandir` works on is rewound and closed with it, so the
directory's own descriptor stays usable; `lstat` each entry relative to it,
require the allowlisted shape, require each nested `__pycache__` to carry
its planned identity, require the cache to hold exactly its planned number of
entries, and record the names to remove; for a file, `lstat` it relative to
that directory and require a regular file with an allowed suffix; keep the
target's running byte total within the per-worktree cap; and
keep the run's byte total, this target's measured bytes added to those
measured at the preflight of every earlier target whose stage passed it in
this run, within the invocation's 1 GiB (B-26, D4). Any `OSError` (`ENOTDIR`
or `ELOOP` from a swapped symlink, `ENOENT`, `EACCES`), any identity, shape or
entry-count difference, either byte cap exceeded, or a call past its own 5 s
budget (`probe-timeout`) ends the stage `refused` with `cache-changed`, unless a
signal was received first (B-41, below). `ENOENT` here is a planned path found
absent, which the lead's R-208 counts at revalidation as a decided value and
not as a failed read; `ENOTDIR` from a no-follow open is either a symbolic link
or other non-directory where the plan recorded a directory, or an ancestor that
is no longer a directory, which R-208 reads as a decided absence; each is a
difference from the plan, and the target is `state-changed` either way, the
reason R-208 gives a failed read (B-58, B-59).
A read of the preflight, or of the
reopening of the first listed cache's chain after it, that the removal floor or
the deadline stops is not one of these (B-34, Codex's P2 at
`specs/project-clean-review-safety/spec.md:353` on `e1049b2`): the read's budget
is `min(5 s, work remaining less the removal floor)`, so a read that outlives
the second term, where it is the smaller, ran into the deadline, recorded
`deadline-exceeded` as change 1's bounds rule records it, and a read that cannot
start because no more than the floor remains has no budget at all. Neither has
found a difference: nothing was deleted, and no difference was found before the
read stopped, so the stage ends `not-attempted` with `target-stopped`, as at the
check before the first hand-off (D1, step 3a), and the target `not-attempted`
with `deadline-exceeded`. Which budget ran out tells a slow run from a changed
worktree, and a read past the 5 s budget is still a preflight error, where no
signal was received. The signal comes first (B-39, B-41; Codex's P2 at
`specs/project-clean-review-safety/spec.md:354` on `fffc194`): the stage reads
the slot before it classifies any outcome of the preflight, or of the reopening,
whether a difference, an error, a byte total past a cap, a `probe-timeout`, or a
stop by the floor or the deadline, and a signal recorded by then gives the check
before the first hand-off's outcome instead: the stage `not-attempted` with
`target-stopped`, the target and every later one `not-attempted` with
`interrupted`, the exit status the signal's, never `refused` with
`cache-changed` and never `deadline-exceeded`. The signal has stopped the run,
so nothing is acted on that the preflight found: nothing is deleted in either
reading, and a re-run's preflight sees any real difference again. This is the
whole-list check that PR #2's open thread 3989548481 asked for: no path is
removed until every path has passed.

The removals: for each directory holding a listed path, in canonical order,
open its chain again, once, checking every identity again; then for each listed
cache in it, remove the names fixed at the preflight, depth-first, files by
`os.unlink(name, dir_fd=directory)` and each emptied nested directory by
`os.rmdir(name, dir_fd=parent)`, then the listed directory by `os.rmdir`
relative to that directory; a listed file by `os.unlink` relative to it.
Nothing listed after the preflight is removed, and `rmdir` refuses a
directory that holds anything else, so a file placed in a cache directory at any
time before that directory's removal survives (Context, `ENOTEMPTY`) and ends
the stage `partial`, or `refused` when no entry had yet been removed (D8). Each
unlink and directory removal is handed to the worker
only while more than the removal floor remains and is waited for until it
returns (D12). No recursive deletion, no `shutil.rmtree`, no path-name
deletion and no child process is used.

### D8. The partial phase and the target's result

The stage's first removal is the hand-off of its first unlink or directory
removal to the worker, not the first one completed (B-16). After it, any
failure (an `OSError` from an unlink, a removal or a chain open, `ENOENT`
included, since something else is changing the worktree), a read past its
budget, a removal still outstanding when the 300 s removal ceiling, counted
from its hand-off, ends its wait, or the removal floor reached at the next
hand-off ends the removals. A stage that has handed over a removal ends
`disposed` or `partial`, never `refused`, with one exception: when every
removal handed over has returned and none removed its entry, as when the first
unlink meets a sticky directory, an append-only or immutable attribute or a
filesystem made read-only after the plan, which the plan's access check cannot
see (B-20, B-51; D3), it ends `refused` with `cache-changed`, nothing
deleted. Otherwise the stage then rescans each listed cache (B-18): on threads
of its own, never the stage's worker, each call a reconciliation probe under
`min(5 s, reserve remaining)`, it opens the chain to the cache's parent as in D7,
checking every identity, and `lstat`s the cache's name relative to it with
`follow_symlinks=False`; absent is `removed: true`, present `removed: false`,
and a chain that no longer opens or carries another identity is `removed:
null`, while the first call past its budget leaves that cache and every later
one `removed: null`. A cache with a removal still outstanding is `removed:
null` whatever the rescan finds, since that call can still complete. Its
`cache_disposal` is `partial` with `cache-partial`, the planned `entries`, and
`entries_removed` counting the removals that returned having removed their
entry, as `operations.performed` does; an outstanding removal counts in
neither. The rescan of the listed paths, beside the target's reconciliation,
is this change's reading of `BA:1334`'s "the report rescans the worktree"
(lane 3's LOW 2): a status of the worktree would add a Git child and would not
say which listed path remains.

| Stage outcome | `cache_disposal` | Target | Later targets | Exit (first matching row of change 1's table) |
| --- | --- | --- | --- | --- |
| every listed cache removed | `disposed`, null | the sequence goes on to the spawn | as change 1 | as change 1 |
| preflight difference, error or call past its 5 s budget with no signal received (B-41), either byte cap included (B-26) | `refused`, `cache-changed`; each `removed` false where the preflight found the path, null where it did not | `refused`, `state-changed`, reconciliation, nothing spawned | `not-attempted`, `batch-stopped` | 2 |
| every removal handed over returned and none removed its entry (B-20) | `refused`, `cache-changed`; each `removed` false | likewise | likewise | 2 |
| failure after an entry was removed | `partial`, `cache-partial` | likewise | likewise | 2 |
| the floor reached at a hand-off after the first removal | `partial`, `cache-partial` | likewise | `not-attempted`, `deadline-exceeded` | 1 (the deadline stopped work) |
| a removal still outstanding at the 300 s removal ceiling (B-16) | `partial`, `cache-partial`; that cache `removed: null` | likewise | `not-attempted`, `deadline-exceeded` | 1 |
| a signal after the first hand-off, then a finished stage | `disposed`, null | `not-attempted`, `interrupted`, with its reconciliation (B-17) | `not-attempted`, `interrupted`, `reconciliation: null` | 130, 143 or 129 |
| a finished stage, then less than the floor at the spawn check | `disposed`, null | `not-attempted`, `deadline-exceeded`, with its reconciliation (B-17) | `not-attempted`, `deadline-exceeded` | 1 |
| no start, a preflight read that the floor or the deadline stops (B-34), any preflight outcome after a signal was received (B-41), or the check before the first hand-off fails (floor or signal) | `not-attempted`, `target-stopped` | `not-attempted`, `deadline-exceeded` or `interrupted`, `reconciliation: null` | likewise | 1, or the signal's |
| target refused at revalidation, or never reached | `not-attempted`, `target-stopped` | as change 1 | as change 1 | as change 1 |

Mapping a cache failure onto the target's `refused` with `state-changed`, rather
than new reasons, is CD-2, and the MODIFIED "Clean records a reconcilable result
for every removal target" widens its `refused` stage to name a cache stage that
ended `refused` or `partial` and gives the stage's deletions as the one
exception to "never ... delete a directory itself" (B-10); stopping the run is
CD-1. The same block's `not-attempted` stage now names a target whose cache
stage ended `disposed` and whose removal was not spawned, for a signal or the
floor, so that it does not also match a stage that ended `refused` or
`partial`, which the `refused` stage names (lane 3's re-read MEDIUM 2), and
such a target carries its reconciliation once its stage removed an entry
(B-17, lane 3's M2), so the carried rule "a `not-attempted` target SHALL carry
null" no longer contradicts the ADDED requirement. Its signal paragraph lets a
cache stage that has handed over its first removal run to its end, since one
that has not yet handed it over stops at the check before it (lane 3's
re-read LOW 1). The ceiling row is this design's reading of B-16: past 300 s
the work deadline has passed, so the later targets meet the floor, and the run
exits 1 as change 1's `removal-ceiling` does. The target itself is `refused`
with `state-changed`, not `removal-ceiling`, so the same block's exit table
names the case in its row 2, "a cache stage's removal reached the removal
ceiling", and an only or last target also exits 1 (lane 3's re-read MEDIUM 1,
B-27). The ADDED requirement's exit sentence says the same: 2 unless a signal,
the deadline or the removal ceiling decides it, and 1 when the floor or the
ceiling ended the stage unless a signal decides it, as the table's first two
rows order them (B-31, lane 3's delta read). The retry is a re-run: the
fresh plan enumerates the caches that remain, the revalidation and preflight run
again, and a persistent failure stops at the same target each time, which the
human line says (D11). A stage that the floor or the deadline stops in a read
before its first removal is no cache failure and is not mapped onto `refused`
(B-34): the target is `not-attempted` with `deadline-exceeded` and
`reconciliation: null`, as at the check before the first hand-off, the later
targets are `not-attempted` likewise, and the exit status is 1 by the deadline
row; the retry is the same re-run. Where a signal was received before the stage
classified any outcome of its preflight, a difference, an error, a byte total
past a cap, a read past its own 5 s budget or a stop by the floor or the
deadline, the stage is not mapped onto `refused` either (B-39, B-41): the target
is `not-attempted` with `interrupted` and `reconciliation: null`, the later
targets likewise, and the exit status is the signal's, 130, 143 or 129.

### D9. The platform check

Once per invocation, before any enumeration, a pure function checks
`hasattr(os, "O_NOFOLLOW")` and `hasattr(os, "O_DIRECTORY")`; `os.open`,
`os.stat`, `os.unlink`, `os.rmdir` and `os.access` in `os.supports_dir_fd`;
`os.stat` and `os.access` in `os.supports_follow_symlinks`; `os.access` in
`os.supports_effective_ids` (B-20); and `os.scandir` in `os.supports_fd`, the
streaming enumeration of D3 and D7, in place of `os.listdir` (B-44; the
Context table lists both). False
makes every row that reaches the `ignored-local-files` rung holding ignored
records `cache-unsupported-platform` with null counts, runs no enumeration, and
leaves the batch as change 1's (CD-3). A row that an earlier rung classified
(`stale-worktree`, `protected-default`, `inspection-error` or `dirty`) keeps
that classification, and its sub-record, `not-candidate` where it holds ignored
records, as where the calls exist (B-37, Codex's P2 at
`specs/project-clean-review-safety/spec.md:383` on `e1049b2`): the check
withholds the cache proof and does not rewrite the ladder, whose order is a
function of the row's evidence alone, so a dirty worktree that also holds an
ignored file keeps the dirty advice, which is the actionable one, where "every
row holding ignored records" had forced it to `ignored-local-files`. The check
never falls back to a flag of 0, as `bb91a49` did. Tests stub it to false; CI
runs the real check and the descriptor scenarios on `ubuntu-latest` only (`test
(3.10)` and `test (3.12)`), so macOS's support is not verified by CI (L-12,
B-15), and where it is missing the check fails closed.

### D10. Revalidating a cache target

The targeted revalidation keeps the order and the limit of PR #19's text at
`173d83c`, on which the MODIFIED "Cleanup revalidates destructive actions" is
written since round B19 (B-54, B-58, B-60, B-84, B-88, B-93; at `e14ada0` in
round B18, at `b3228bb` in rounds B16 and B17, at `f0bf538` in rounds B13 to
B15, re-based from `2e819ad` in round B12 and from `9267303` in round B13): six
Git children, seven where the plan read `extensions.worktreeConfig` as true,
and three more where the path of the repository's root or of its common
directory holds a line feed (PR19/rs:76-79). In the target worktree, a target
with listed caches runs the D3 child instead of the combined probe: it must
read no record other than ignored ones, and its ignored records must be exactly
the plan's `paths` as `[path, kind]`, the trailing `/` of a directory record
giving `directory`; the baseline signature's `ignored_files` is recomputed from
those records with the combined probe's bound of 64. A difference, a failure of
the child, or a run past its own budget while the deadline is not the limit,
refuses the target with `state-changed` (a value that cannot be re-read is a
difference, PR19/rs:115-117 at `173d83c`), before any cache is touched. A child
that the work deadline cuts counts as no difference, and the target and every
later one are `not-attempted` with `deadline-exceeded`, nothing touched, by the
one rule that PR #19 states for every Git child and every filesystem call of
the revalidation (PR19/rs:115-139 at `173d83c`; lane 2's R-171, the lead's
R-208 and W38's L-4; B-55, B-58, B-60); the child is one of those steps, so the
block needs no sentence of its own for it. This change adds no filesystem call
to the revalidation and leaves PR #19's reads of the administrative directory,
its `modules` and `operation-in-progress` checks, as they are. It follows
PR #19's rule for a path found missing: a filesystem call that finds no file
or directory at its path (`ENOENT` or `ENOTDIR`) decides that the path is
absent, and a decided value keeps its step's own reason (PR19/rs:124-139 at
`173d83c`; the lead's R-208 and W38's L-4; B-64, B-68). So a decided absence
keeps its step's own reason: a listed cache missing at revalidation is a record
that the child does not print, a value it decided, and is a listed-cache
difference, `state-changed`, and an administrative directory that the
`operation-in-progress` listing finds absent is a registration difference,
`identity-changed`; a cache directory that cannot be read either
changes the child's records, a difference, or meets the stage's preflight,
whose failed read refuses the target with `state-changed` (D7), the reason
R-208 gives a failed read; and a read that the deadline cuts is
`deadline-exceeded` in both. B-34's rule for a read of the stage's preflight is
unchanged. The hidden-state probe and PR #19's
`worktree-only-commits` check follow it, in that order, as for every target.
Where the two step lists meet (reader RF's H1), the block's order is therefore:
the combined status probe, or for a target whose plan lists caches the D3
child in its place, then the hidden-state probe, then the
`worktree-only-commits` check. That keeps the meaning of both: this change's,
the D3 child in the combined probe's place and before the hidden-state probe,
and PR #19's, the hidden-state probe and then the `worktree-only-commits` check
after the in-worktree status check. The D3 child takes a place and adds none,
so the count stays PR #19's six, or seven, and nine or ten for a path that
holds a line feed.

### D11. JSON and what the person sees

`cache_disposal` in the plan (worktree rows and `selected` entries) and in the
apply record (targets) is exactly as the ADDED requirement lists it, present
only where this change acts and absent otherwise, never `null` (L-10, B-13): on
a worktree row whose `ignored_files` is above 0, and on a `selected` entry and
an apply-result target whose plan lists at least one cache; the codes
are the sub-records' own: `reason` in the plan `not-candidate`, `cache-cap`,
`cache-unverified`, `cache-unwritable` (B-20) or `cache-unsupported-platform`;
`candidate_block` in the plan null or an existing class name or gate reason
(B-24); `stage` in the record `disposed`, `refused`, `partial` or
`not-attempted`, with `reason` null, `cache-changed`, `cache-partial` or
`target-stopped`. Every path is written by change 1's escaping rule with
`path_valid_utf8` beside it, which is always true in `paths` and `directories`,
since a cache path that is not valid UTF-8 is blocking, and can be false in
`blocking_samples`, as for the 0xFF path of "A symlink named like a cache is
never disposable" (lane 3's LOW 13). `limits` gains the five keys of D4. No
existing enum gains a value and `schema_version` stays 1 (CD-16).

The text is ASCII, pinned by the tests, with `PATH`, `CPATH`, `BPATH`, `DPATH`,
`ROOT`, `N`, `E`, `B`, `D`, `K`, `C`, `U`, `W`, `G`, `CLASS`, `NEXT STEP`,
`REASON` and `REASONS` substituted:

- Preview, under `  remove PATH [BRANCH]`: `    caches: N paths, E entries, B
  bytes; first: CPATH`.
- Preview, an `ignored-local-files` row, after change 1's `: N ignored; first:
  SAMPLE`: `; disposable D, blocking K; first blocking: BPATH` when the counts
  are established and `blocking` is above 0; `; disposable D, blocking 0; not
  disposed: REASON` for a row the invocation's totals left, and, for
  `cache-unwritable`, `; disposable D, blocking 0; not disposed:
  cache-unwritable; fix the ownership or mode of DPATH, or, on a read-only
  filesystem, remount it writable, then re-run`, `DPATH` being the first, by raw
  path bytes, of the directories whose access check was false, relative to the
  worktree and `.` for the worktree itself, which the row's evidence holds for
  the line and no JSON key carries (B-20; lane 3's F-12, F-11, B-72, B-74; D3);
  `; disposable unknown, blocking unknown
  (REASON)` when they are null, followed by `; first blocking: BPATH` when the
  sample test rejected a sample (D2), or by `; kept as CLASS: NEXT STEP` when
  the row has a `candidate_block`, `NEXT STEP` being change 1's next step for
  that class or gate (CAS design.md:751-760), so that the line names what
  really keeps the row and not the advice to delete its ignored files (B-24).
- The plain report, a row holding ignored records: one more line, `  caches:
  disposable D, blocking K` or `  caches: disposable unknown, blocking unknown
  (REASON)`, with the same `; kept as CLASS: NEXT STEP` ending.
- Success, after `Removed N; branches kept: B1, B2.`: `Caches disposed: N paths
  in K worktrees.` (`1 path` when N is 1, `1 worktree` when K is 1).
- The stall line (B-21), printed under the `ignored-local-files` group only
  when each of the first 16 candidates in canonical order is held for a
  persistent reason, at the rung any one of `blocking` above 0, `cache-cap`
  from a per-worktree cap, `cache-unverified` or `cache-unwritable`, the test
  never on `blocking` alone (B-32, D4), or past the rung an exclusion by a gate
  after `deferred-target-cap` (B-56, D2), and only when at least one later
  candidate is left with `cache-cap` by the 16-enumeration cap, the rows the
  line names (B-45), and built from those rows' reasons with
  every zero count left out, a `cache-cap` row counting as one past a
  per-worktree cap when its counts are null: `  these cache-cap rows will not
  drain while the 16 candidates
  ahead of them stay kept: K hold ignored files that are not caches (review
  them), C exceed a per-worktree cache cap (delete their caches, then re-run),
  U could not be enumerated (re-run; if it repeats, inspect them), W cannot be
  changed by this user (fix their ownership or mode, then re-run), G are
  excluded after the target cap as REASONS (follow their groups' next
  steps)`, in the form of change 1's index-gate line (CAS design.md:743-746),
  `REASONS` listing each of those rows' reasons once, in gate order, joined by
  `, `, as change 1's deferral line forms its own (PR19 design.md:1176-1182 at
  `4f1c0e0`). Each such row also prints in its own group with change 1's next
  step (PR19 design.md:1189-1216): "review, then git worktree remove --force
  yourself" for `contains-submodule` (lane 3's W52 F-8, which PR #19's round
  (g) applied), "review, then remove the worktree yourself" for
  `hidden-local-state`, "finish or abort it ...
  then run again" for `operation-in-progress`, and "keep it on a branch or tag,
  or review, then git worktree remove yourself" for `worktree-only-commits`
  (B-56). It never tells the
  person to remove by hand a worktree whose state was not established; a row
  that a gate after the cap excludes has its state established, so its group's
  next step stands. The `W`
  part is this design's completion of B-21 for B-20's reason, since 16
  `cache-unwritable` rows stall the same way. With exactly 16 candidates, each
  held for a persistent reason, no row waits behind them, so each row's own
  reason and next step print as usual and no stall line prints (B-45).
- A stop at a cache stage, before the stop block: `Cache disposal at PATH
  refused (cache-changed); nothing was deleted.`, printed only when no entry was
  removed and no removal is outstanding and, for a stage that ended before its
  first removal, no signal had been received by then (B-41); or `Cache disposal
  at PATH partial (cache-partial): removed K of N cache paths; remaining: C1,
  C2. A fresh plan lists the rest: project clean ROOT --all-safe`, with `; may
  still be removed: C3` after the remaining paths for a cache whose removal is
  still outstanding (B-16); or, when the work deadline ended the stage, `Cache
  disposal at PATH partial (cache-partial): the work deadline ended it after
  removing K of N cache paths; remaining: C1, C2. A fresh plan lists the rest:
  project clean ROOT --all-safe` (B-21), so that a deadline does not read as a
  change of state. The stop block that follows is change 1's, its reason the
  target's.
- A stop after a stage that ended `disposed`, before the spawn (B-17) or at
  that target when Git's removal then ended it `failed` (B-49), before the stop
  block: `Cache disposal at PATH: removed N cache paths; the worktree was not
  removed.`; and when that target ended `unknown`, its removal not proven, as
  after a removal child that exited 0 without evidence or that the removal
  ceiling killed: `Cache disposal at PATH: removed N cache paths; the
  worktree's removal is not proven.` (B-49, RB's MEDIUM-2). The end state is
  B-17's, the caches deleted and the worktree kept or its removal unproven, so
  the line gives the count deleted, and the stop block that follows gives the
  target's reason and the next step, with the recovery text of a
  `partially-removed` target.
- A stop at a target whose cache stage the floor or the deadline stopped in a
  read before its first removal, no signal having been received by then (B-39,
  B-41), before the stop block: `Cache disposal at PATH not attempted
  (deadline-exceeded); nothing was deleted.` (B-34), so that the deadline is
  named and a change of state is not claimed. The `refused` line above is
  printed only for a difference or a preflight error, with no signal received.
- The question is change 1's, unchanged (CD-15).

### D12. Time, threads and signals in the stage

The stage starts only while more than `removal_floor_seconds` of the work
deadline remains (D1). It runs its calls through one daemon worker thread per
stage, fed one call at a time, and treats the two kinds of call as change 1
does (B-16): its reads, as change 1 treats its identity reads (CAS
design.md:304-306), and its unlinks and directory removals, as change 1 treats
its removal child.

- A read (an open, a bounded enumeration, an `lstat`) is waited for by the
  main thread with `min(5 s, work remaining - removal_floor_seconds)`. A read
  past that wait abandons the worker and ends the stage: `partial` after the
  first removal;
  before it, the slot is read first (B-39, B-41), and a signal recorded by then
  ends the stage `not-attempted` with the target `interrupted`, whichever wait
  it was; otherwise `refused` when 5 s was the wait, which holds when at least
  10 s of work remained, and `not-attempted` when the wait was the smaller `work
  remaining - removal_floor_seconds`, which is the deadline's limit, as it is
  when a read cannot start because no more than the floor remains (B-34).
- A removal is handed to the worker only while more than the floor remains,
  and the hand-off of the first one is the stage's first removal for every rule
  of the two ADDED requirements. A removal handed over is waited for until it
  returns, never abandoned at the per-call budget, and counts as a removal in
  flight for the run bound and for signals. Only the 300 s removal ceiling,
  counted from the hand-off, ends that wait; its cache is then `removed: null`
  and the stage ends `partial`, never `refused`. The reconciliation reserve
  counts from the return or from that ceiling.
- A worker with a call still outstanding gets no further call, and no
  descriptor given to an outstanding call is closed before `project` exits, so
  that `os.open`, which returns the lowest free number, never hands that number
  to a later chain or to the rescan. Without that rule a late `unlinkat`
  against a reused number could remove a same-named entry in a directory the
  plan never checked, as AE-1 reproduced.
- The rescan of a partial stage (D8) never runs on the stage's worker: each of
  its calls runs on a thread of its own, as a reconciliation probe under
  `min(5 s, reserve remaining)` (B-18).

The floor is therefore left for the spawn whenever every removal returns in
time, and the 64 s run bound keeps change 1's two exceptions, a removal in
flight, up to its ceiling, and a filesystem call stuck in the kernel. The
earlier design abandoned removals as well as reads; Codex's P1 on `3c08613`,
S-1 and AE-1 showed that an abandoned unlink could finish after the record had
said "nothing was deleted".

Signals keep change 1's handlers, which only record. The stage reads the slot
before its preflight and again immediately before the hand-off of its first
removal, after the preflight and once the first listed cache's chain is reopened
(D1, steps 2 and 3a, B-17), and not again until the spawn check, except that it
reads the slot when the preflight, or the reopening of that chain, reaches an
outcome, before it classifies it, whether a difference, an error, a byte total
past a cap, the end of a read's wait or a stop by the floor or the deadline
(B-39, B-41). The handler only records, so a signal received while a read is
held changes nothing until then, and without that read the target would be
reported `refused` with a change of state, or `not-attempted` with
`deadline-exceeded`, for a run that a signal had already stopped. A signal
recorded before that second check stops the target with nothing deleted; one
recorded after it is handled as one received during the removals, which finish,
and then stops the target before its spawn (CD-11): its caches are either
untouched or all removed, and a target whose caches were removed is
`not-attempted` with its reconciliation. Every check-then-act has a window like
this; masking signals around the check would only move it, since Python runs
handlers in the main thread between bytecodes.

### D13. The guarantee and the residual window

The stage removes an entry only if, at its preflight, the entry had the allowed
shape, its listed cache held its planned number of entries, and every directory
from the worktree root down to it carried its planned identity, and, at its
removal, the chain to it carried those identities again. For a cache target the
narrow guarantee's revalidation is D1's step 1, and the window it leaves, as
PR #19's text states it (PR19/rs:309-313 at `f0bf538`), ignored files created,
index flags set, operations started and commits made that only the target's HEAD
reflog or `refs/worktree/` holds, after it, covers a cache that Python writes
again after the stage: Git's non-force removal deletes it with the worktree
(`BA:319-323`). The MODIFIED "Cleanup states a narrow guarantee and its
residual window" states both, and gives the stage's guarantee as the one for
the cache entries it removes, beside the one for a worktree removal (B-10,
SA-2).

For a cache target the window is wider than change 1's (B-19, lane 3's M1,
S-3, AE-4). The last check that covers ignored files outside the listed caches
is that revalidation, before the stage, so an ignored file created during the
stage outside the listed caches, a `local.env` at the worktree root or an
editor's swap file, is deleted with the worktree by Git's non-force removal,
which deletes ignored files and refuses only untracked or modified ones
(`BA:319-321`). The packet's window is "one child start-up plus Git's own
status check, typically well under a second" (`BA:323-324`); a cache target's
adds the stage, which took about 0.25 s for 512 entries on this workstation
(AE-4's measurement, 2026-10-19), and which task 2.3 re-measures. A file placed
in a listed cache directory is still protected, since `rmdir` refuses a
directory that holds it (D7), which is the sense in which CD-18 calls the stage
safer. The window is stated, not closed: one combined status probe after each
`disposed` stage would close it at one Git child per cache target, at most 266
children and 16 removals, 39.9 s + 4.8 s = about 44.7 s at the packet's model
before any filesystem time, these figures and the counts below being at
`c462d87`, on change 1's terms before PR #19 changed them (B-55; D4). With
the walk and the stages at B-25's bound through one worker (D4), it costs
about one target: each earlier cache target
delays target k by 0.15 s more, and 16 cache targets and an 8,192-entry walk
cannot come together, since 16 selected targets hold the walk to the 4,096
entries they list. With 16 cache targets the 15th arrives at 40.5 + 2.1 + 1.0
+ 1.9 = about 45.5 s, and with 8 cache targets ahead of it and 8,192 entries
walked at 40.5 + 1.2 + 2.0 + 1.9 = about 45.6 s, past the spawn limit either
way,
while the 14th arrives by about 44.6 s: 14 of 16 targets reach their stage,
against 15 of 16 without the probe. Under #23's flag B-19 put the probe's
cost at about one target fewer than #23's 13 of 16 at `ca96701`, 12, with the
cache-stage filesystem time excluded; #26 restated its own count under A-23
and A-24, which D4 gives as it stood at `9b67e8c` (B-35). That would buy a
window that concurrent writers, outside the contract, alone can use (B-19;
proposal, Decisions).

When the plan selects a cache target, change 1's residual-window line gains
the cache items, and on PR #19's text at `4f1c0e0` reads `Not protected:
ignored files created, index flags set, operations started or worktree-only
commits made after the last check or during a cache stage, caches recreated
after it, and any change after Git's own check.` (PR19/design.md:1183-1185; the
window of PR19/rs:309-313; reader RI's RI-1, RH's M3, B-67); otherwise it is
change 1's line, unchanged. The MODIFIED "Cleanup states a narrow guarantee and
its residual window" says only that the line SHALL also name the two cache
items, so that a later change to change 1's line moves this one with it.

### D14. Tests

The deltas hold 59 scenarios in `project-clean` (5 classification, 15 retire,
14 batch, 6 bounds, 8 reconcilable result and 11 ADDED), 32 in
`project-clean-review-safety` (6 preservation, 15 revalidation, the 14 of PR
#19's text at `173d83c`, as at `b3228bb` and `f0bf538`, and this change's one
(B-54, B-58, B-60, B-84, B-88, B-93; 14 at `9267303` in round B12 and at
`2e819ad` in round B11, 13 at `a664799` before it), 4 narrow
guarantee and 7 ADDED, B-26's among them) and 8 in `project-overview` (the one
MODIFIED block of B-14). The new ones, 1 + 1 + 1 + 11 + 1 + 1 + 1 + 7 + 1 = 25,
each get a test
named after it. Of the 74 carried ones, which keep the tests of features 004
and 005, 70 are byte-exact and four are edited, the four more than before being
PR #19's scenarios in the retire and batch blocks, carried byte for byte (B-69),
each of the four edited to name its ignored file
as not a Python bytecode cache: "Ignored-file bound" and "A merged worktree has
ignored local files", as before, and, under B-22 and lane openRepoProject-4's
precision, change 1's "Every protected classifier" in the batch block and
change 2's "Every protected classifier" in the overview block, whose THEN
would otherwise fail on a fixture whose ignored files are caches (lane 3's
LOW 11). The overview edit departs from B-14's "plus one scenario", and lane 4
agreed it on 2026-10-19 with the rest of B-22. The new tests' names begin
`test_clean_`, so that feature 004's `git-floor` job, which runs `-k
test_clean_ -k test_status_ -k test_doctor_` with Git 2.36.6 first on PATH,
runs them (S-4, `clarifications.md`). The deferred
scenario of `BA:1632-1634` is covered by "A symlink named like a cache is never
disposable", "An ancestor swapped for a symlink before the stage", "A partial
cache phase" and "A file placed in a cache directory during the stage".

- Fixtures write `.pyc` and `.pyo` bytes directly, so no compiler runs, under
  explicit ignore rules (`__pycache__/` with `*.py[co]`, or `*.pyc` alone, or
  `__pycache__` for the symlink case) in the worktree's `.gitignore` or
  `info/exclude`; the 256 MiB cap uses sparse files made by `os.truncate`.
- Hooks: between the revalidation and the stage, after the preflight, while
  the first listed cache's chain is reopened, before the n-th hand-off, and on
  the n-th unlink, holding it or making it fail, through `patch.object` on the
  stage's call table, the removal ceiling patched short; `os.close` stubbed to
  record the numbers the stage closes, so that a test can assert that no
  number given to an outstanding call is reused; the stage's and the walk's
  call tables counting their opens, so that a test asserts one chain per
  directory holding a listed path in each pass and one open per recorded
  directory in the walk (B-33); a preflight read held until the budget that
  the patched clock leaves to the deadline is spent, or until no more than the
  floor remains, against the same read held past 5 s with at least 10 s
  remaining (B-34, B-38), and each of them again with SIGINT delivered while
  it is held, and a preflight that finds a changed entry again with SIGINT
  delivered before it does, in each of these the stage then `not-attempted`,
  the target `interrupted` and the exit status 130, never `refused` (B-39,
  B-41); the access check stubbed to false where the runner is root; the
  platform check stubbed to false; the counting `git` wrapper of change 1 for
  the enumeration's argument vector, directory and count.
- The streaming enumeration (B-44): a test hook on the walk's call table counts
  the entries taken from the enumeration of a `__pycache__` holding 100,000
  entries, under the ignore rule `__pycache__/`, and sees at most 513, the row
  `cache-cap` and nothing deleted, as the AND of "Cache caps" says; the same
  hook on the preflight sees, for a listed cache that gained entries after the
  plan, at most one entry beyond the number the plan recorded before the stage
  ends `refused` with `cache-changed`; and after each enumeration is closed the
  directory's descriptor still `fstat`s to its identity and a second
  enumeration from it starts at its first entry, as the Context's check found.
- The stall line's held-back row (B-45): with exactly 16 candidates, each held
  for a persistent reason, the human report prints each row's own reason and
  next step and no stall line, as the AND of "Cache caps" says, and with a
  seventeenth candidate added it prints the line.
- The stall line's late-gated rows and the totals (B-56): sixteen candidates
  each holding only caches and an initialized submodule, or an entry flagged
  assume-unchanged, are each enumerated, pass the rung and are excluded as
  `contains-submodule` or `hidden-local-state`, their caches untouched, and
  with a seventeenth candidate the line names them by those reasons, `G` and
  `REASONS`; and eight candidates of 500 entries holding an initialized
  submodule, ahead of a ninth of 500 entries, are left out of the totals, so
  the ninth is selected and removed, as the two ANDs of "Cache caps" say.
- Every existing test keeps passing, among them
  `test_clean_preserves_ignored_files_in_an_otherwise_merged_worktree`
  (tests:949, `local.env`) and feature 004's tests, whose fixtures hold no
  cache; a feature 004 test whose fixture holds a cache, should one exist when
  this feature starts, is listed in its plan and its fixture changes to a
  non-cache ignored file, as change 1's "Every protected classifier"
  (CAS/pc:670-683), edited in this change's MODIFIED batch block, now says.
- Once feature 005 has landed, any of its tests asserting that the overview
  and `project clean` classify identically, "Every protected classifier"
  among them, gets the cache case excluded in this change's realization (its
  `ignored-local-files` fixture row given a non-cache ignored file, as the
  edited overview scenario now says, or a cache-only row left out of the
  equality check), never in feature 005 (B-14); the new overview scenario pins
  the exception itself.
- `python3 -m unittest discover -s tests -v`, which CI runs as `test (3.10)`
  and `test (3.12)` on `ubuntu-latest`; macOS is not verified by CI (L-12).

## Risks / Trade-offs

- [A `.gitignore` that names `*.pyc` but not `__pycache__/` lists every cache
  file as its own record, so a large tree reaches 512 records sooner] -> The row
  stays `ignored-local-files` with `cache-cap` and the plan stays complete; the
  stage leaves empty `__pycache__` directories for Git's removal to delete with
  the worktree.
- [A worktree with more than 512 recorded cache objects, or 256 MiB, is never
  disposed of by `project`] -> It is preserved as change 1 preserves it, and
  its preview says `cache-cap`; the person deletes the caches and re-runs.
- [A cache directory holding far more entries than the cap, such as millions in
  one `__pycache__`] -> The walk and the preflight enumerate it one entry at a
  time and close the enumeration when the cap decides, so a row's walk holds at
  most 513 entries and a call abandoned at its budget holds no more; the row
  stays `cache-cap` (B-44, D3).
- [A cache tree that is deep and spread over many directories] -> Every
  directory the plan records counts toward the 512 objects, the walk opens each
  once, and the stage opens one chain per directory with removals in each pass
  (B-33), so the work is bounded; but depth times those directories can reach
  43,947 opens a pass for one target, which no fit holds, so until Brett Heap
  answers the Open Question on a limit for them, such a target takes its run
  to the spawn limit and ends `partial`, exit 1, never unsafe, each run removing
  part of its caches (D4).
- [Python running in the worktree between the plan and the stage rewrites
  caches] -> A new cache refuses at revalidation, a replaced directory at the
  preflight, a new file in a listed directory refuses at the preflight, or
  ends the stage `partial` when it arrives after it; a re-run plans afresh. A
  `.pyc` recompiled in place changes nothing (D5), unless its growth takes the
  target past 256 MiB or the run's byte total past 1 GiB, which its preflight
  refuses with nothing deleted (B-26).
- [Sixteen candidates that each keep a blocking path the samples did not show,
  or that a gate after `deferred-target-cap` excludes, sort first, so no run
  enumerates a later cache-only candidate] -> The sample
  test keeps out every row whose samples show a blocking name (D2); the rest is
  a stall the human report names, as change 1 names its index-gate stall, with
  how many of the 16 stay for each cause and each cause's next step (B-21),
  those a gate after the cap excludes by its reasons (B-56),
  whenever a later candidate waits behind them (B-45),
  never advising the person to remove by hand a worktree whose state was not
  established (D4, D11).
- [Cache-only rows that a gate after `deferred-target-cap` excludes, such as
  rows holding caches and an initialized submodule, now pass the
  `ignored-local-files` rung and take the target places that change 1 left to
  later rows (reader RG's W3)] -> Sixteen of them ahead of a backlog stall it,
  plain rows with no ignored file included, as change 1's index-gate rows do,
  and change 1's line names them ("these deferred rows will not drain while
  the 16 rows ahead of them are REASONS", PR19 design.md:1176-1182 at
  `4f1c0e0`), as the stall line does for the cache rows behind them;
  `--apply --action remove --worktree P` still removes an eligible P, since in
  single mode the target limit counts P alone (B-56). The admin-directory
  pre-filter before Brett Heap would keep rows holding an initialized
  submodule or an operation in progress out of the candidates, and so out of
  those places (proposal, Open Questions).
- [A partial phase leaves some caches removed and the worktree in place] ->
  `__pycache__` entries are regenerable; a loose `.pyc` may be sourceless,
  since Python 3 writes bytecode only into `__pycache__/` and a loose one is
  what Python 2 or `compileall -b` left, imported when its source is absent.
  Each path is reported removed, remaining or not established, and a re-run
  finishes the job or stops at the same place with the same report.
- [A `__pycache__` the user cannot change, such as one a root-run container
  wrote] -> The plan's access check keeps the row `cache-unwritable`, not
  selected and stopping nothing, its line naming the directory whose check
  failed and saying to fix its ownership or mode and re-run (B-20, B-72), and so
  it does for a read-only mount, which the check sees on Linux 5.8 or later
  where the C library makes the effective-ids check with the `faccessat2` call
  (B-51, B-53, D3); the check cannot tell a read-only mount from a mode or an
  owner, so the line also names the remount that a read-only mount needs (lane
  3's F-11, B-74, D3). Only a failure the check cannot see, a sticky directory,
  an append-only or immutable attribute or a change made after the plan, stops
  the run at that target, `refused` with `cache-changed` and nothing deleted, or
  `partial`, only cache entries deleted, where a sticky directory also holds the
  user's own entries (B-53), and the human line names it each time.
- [The overview reads a cache-proven row as `ignored-local-files` where
  `project clean` reads it `merged-removable`, whether or not `project clean`
  then excludes it] -> The safe direction: its suggestion is the read-only
  report, which shows the row's state, and change 2's equality clause states
  the exception as B-22 words it, the edit agreed by lane openRepoProject-4
  (B-14, B-22; `tasks.md` 2.2).
- [A filesystem call stuck in the kernel during the stage] -> A read is
  abandoned after its budget and ends the stage `refused` or `partial`, or
  `not-attempted` where the deadline set the budget, or a signal was received,
  before any removal (B-34, B-39); a removal is waited for up to the 300 s
  removal ceiling, as a removal child is, its cache then `removed: null`; the
  worker gets no further call and its descriptors stay open until `project`
  exits, and the rescan, on threads of its own, records `removed: null` where it
  cannot tell (D12).
- [An ignored file created outside the listed caches during a cache stage is
  deleted with the worktree] -> The residual-window line names it; the stage
  took about 0.25 s for 512 entries here, and concurrent writers are outside
  the contract (D13, B-19).
- [The change frees fewer rows than its first evidence suggested: of the 37
  merged, clean, published rows kept for ignored files measured on 2026-10-19,
  13] -> `.pytest_cache`, which alone keeps 16 more, is before Brett Heap with
  a recommendation not to admit it in this change, since its form would
  delete by place, leave a stopped stage's remnant untracked and miss the
  repositories that ignore it themselves; a later change, first in line, takes
  it (B-23, B-50; proposal, Open Questions).
- [Bind mounts and other devices inside a worktree] -> A cache path, a
  directory above it, or a listed cache directory or a directory inside it,
  on another device is blocking (CD-8, B-48). A bind mount from the worktree's
  own filesystem has that filesystem's device, so the device check cannot see
  it: disposal acts on paths inside the worktree's tree and, through such a
  mount, disposes of the mount's cache files as the worktree's own,
  cache-shaped entries only. Where the mount point is a directory the stage
  removes, a listed or nested `__pycache__`, its removal fails with `EBUSY`
  (rmdir(2)), the stage ends `partial`, and each later run lists the emptied
  directory again and stops at that target, `refused`, until the mount is
  gone; this was not reproduced here, for want of the privileges to mount.
  Detecting mount points by parsing `/proc/self/mountinfo` is rejected:
  Linux-only parsing for a rare case whose reach is limited to caches inside
  the worktree's path (B-48, RB's MEDIUM-1).
- [Case-insensitive filesystems and temporary names] -> Only exact names count;
  anything else is blocking, so the row is kept.
- [#23, which archives after this change, must carry five blocks re-based on
  this change's archived text] -> Dependencies and Sequencing names each of
  them, and #23's own tasks re-base them before it archives (L-11, A-13).
- [The descriptor calls are verified here on Linux only, and CI runs on Linux
  only] -> D9's check fails closed on any platform without them; macOS is not
  verified by CI (L-12).

## Migration Plan

1. Ratification by Brett Heap's word on this change's pull request (`tasks.md`
   1.6), with the six Open Questions of `proposal.md` before him; an answer
   admitting `.pytest_cache`, against the recommendation, adds it to the deltas
   with what B-50 names before ratification (B-23, B-50), and so does one
   adopting the limit on the stage's directory opens (B-33), or the
   admin-directory pre-filter (B-56).
2. Before the Speckit handoff (`tasks.md` section 2): change 1 archived after
   feature 004 merges, with PR #19's amendment of change 1 landed (L-16), or
   PR #19 closed, and the eight blocks written on its text, one at `6bf9f77`,
   two at `f0bf538`, one at `b3228bb`, one at `173d83c` and three at `2250830`,
   whose text `88d0d36` keeps byte for byte (B-54, B-58, B-60, B-69, B-76,
   B-80, B-84, B-87, B-88, B-93, B-95, B-99, B-104, B-107), re-checked, or
   re-based on change 1's text at main if PR #19 closes unmerged (B-52), each
   block written on change 1's or PR #19's text checked by the two diffs below,
   a change to this change's added text returning the block to Brett Heap
   before the Speckit handoff (B-52, B-53, B-54); lane openRepoProject-4's
   agreement on the `project-overview` delta's diff, given on 2026-10-19 for
   `b4d3e12`, and again on B-22's diff before its commit as `9f30fb9` (B-14,
   B-22), and its byte check of B-30's `4d5855a`, given on 2026-10-20 (B-30,
   B-36); the enumeration, the walk and the stage measured (task 2.3).
3. Local `main` is synced to `origin/main`, then `/speckit.specify` creates the
   one feature under the next free number, 006 or later, recorded once in
   `tasks.md` under "Speckit Handoff"; `/opsx:apply` runs only then.
4. The feature implements D1 to D14 on feature 004's code, merging `main` into
   its branch as `main` moves and never rebasing.
5. README: the "Clean up Git worktrees" section gains the cache paragraph: what
   is disposed of and what blocks, the caps, the residual window, the partial
   phase and its re-run.
6. Tests per D14, the feature 005 exclusion included once feature 005 has
   landed.
7. The realization PR merges with green checks on every job of the workflow on
   its base, feature 004's `git-floor` job included beside `test (3.10)` and
   `test (3.12)` on `ubuntu-latest`, and closes issue #24 (S-4).
8. The change is archived after that merge and after the archives of change 1
   and change 2. Before `/opsx:archive`, its `project-overview` block is
   re-read against main's text of "Overview reuses the cleanup classifier and
   merge target" and re-copied from it, keeping any amendment of change 2 that
   landed there meanwhile, such as lane openRepoProject-4's planned one for
   feature 005's open Q7 A, which the archive would otherwise drop silently,
   since a MODIFIED block replaces its requirement whole; a `diff -u` of main's
   block against this change's shows additions only, the second diff below
   shows no change to this change's added text, and the validation passes
   again (B-29, B-54, `tasks.md` 3.2). `add-project-clean-branch-retirement`
   archives after this change, writing its blocks of the five requirements both
   changes modify on this change's archived text.

Each re-check, re-base or re-copy of a block in steps 2 and 8 (`tasks.md` 2.1
and 3.2) is checked by two diffs (reader RF's M1; B-54). The first, `diff -u`
of the archived block, or of main's block, against this change's re-based
block, shows additions only, as tasks 2.1 and 3.2 say, and is kept. It cannot
see a change to this change's own words, which after the earlier change
archives are all additions to the archived block, so a re-base that reworded
them would still show additions only, validate and archive. The second,
`diff -u` of this change's block as committed at its ratified head against the
re-based block, shows only the archived block's own text carried in: for the
eight blocks written on PR #19's text, change 1's archived text in place of PR
#19's at each block's base, `6bf9f77`, `b3228bb`, `173d83c`, `2250830` or
`f0bf538`; and for the `project-overview` block, main's text in
place of change 2's at `961c405`, every amendment that landed there included.
Any change that the second diff shows to this change's own ratified words, its
added sentences, clauses and scenarios and its edits of carried scenarios,
returns the block to Brett Heap before the Speckit handoff (step 2) or before
the archive (step 8); a sentence that lane openRepoProject-4 asks for in step 8
is such a change.

Rollback: revert the realization commit on `main`. `__pycache__` entries
already disposed of are written again by Python on the next import; a loose
`.pyc` already disposed of may have been sourceless and is not written again
(B-17). A worktree already removed stays removed as under change 1, its branch
kept; installed `project` artifacts follow workBenches' pin.

## Open Questions

The six questions of `proposal.md` are before Brett Heap: enum closure and
`schema_version`, `.pytest_cache`, the other cache kinds, the caps, a limit
on the cache stage's directory opens (B-33), and the admin-directory
pre-filter (B-56). Change 2's equality clause, the
fourth in the draft, is settled by B-14 and B-22. The deltas implement each
recommendation but two: the opens limit, which recommends a new per-worktree
cap and is added only on his answer (B-33), no cap changing before it, and the
pre-filter, which the lead recommends adding in this change and which changes
what makes a row a candidate, so it too is added only on his answer (B-56). The
recommendation on `.pytest_cache` is now no for this change (B-50), which the
deltas implement by not admitting it. A
different ruling edits the deltas before ratification. No other question
changes what is built.
