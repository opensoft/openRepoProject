Lane: openRepoProject-4

# Research: Project overview

The Technical Context in [plan.md](plan.md) has no NEEDS CLARIFICATION. The
ratified change `add-project-overview` (landed as `961c405`), its amendment
A1 (PR #34 at `e4a30fc`, ratified by Brett Heap's "ratify 34" on
2026-10-22) and [spec.md](spec.md) with its 72 clarifications decide almost
every behaviour, and they govern. These entries settle what they leave to the
plan, record Brett Heap's word on the held items (C-72) and keep each held
item in its own place:

- R1 and R2: the authority for this plan, its pins, and the base and order of
  the implementation (brief decision 1);
- R3: what the overview reuses from feature 004 and what is new (decision 3);
- R4 to R9: the control loop, the collectors, the scheduler, the filesystem
  tasks, the ref listing's keep-filter and the places where the overview
  reads Git's output differently from feature 004's code;
- R10 to R17: discovery details, ordering, messages, times, counts, the JSON
  and human forms, and the re-verification of FR-007 against feature 004's
  fix, which answer the spec's plan notes PN-1 to PN-18 (PN-4 and PN-11
  withdrawn) and its open Assumption;
- R18: the test strategy (decision 4);
- R19: the threat model (PN-15);
- R20: the held items, O1 to O21 and D5's clause 2, all chosen by his word
  (C-72), and O22 and O23, open for it, each with its design and when it is
  built (decision 2);
- Revision 1: R1's "Re-pin of revision 1" entries;
- Revision 2: where each finding of lane openRepoProject-3's W96 read is
  taken;
- Revisions 3 onward: where each input of those revisions is taken.

Each entry gives a Decision, its Rationale and the Alternatives considered.
Citations, as [plan.md](plan.md) "Citations" defines them: `project:N` is
line N of feature 004's `project` at `d6bac50` (branch
`004-project-clean-all-safe`, draft PR #33), read with `git show
d6bac50:project`; `A1:N` and `A1 design.md:N` are lines of change 2's
`specs/project-overview/spec.md` and `design.md` at `e4a30fc`; `PCM:N`,
`PCL:N` and `#19 design.md:N` are lines of change 1's
`specs/project-command/spec.md`, `specs/project-clean/spec.md` and `design.md`
at PR #19's `54e869b`, its round (t); POD, PRSD, CMD, CLN and DI are as
[spec.md](spec.md) defines them. Revision 1 moved every cite from `4b4c36b` and
`ccc52b9` (R1); revision 2 moved none; revision 3 moved them from `0a82a62` and
`20084cd`, revision 4 from `211e43d` and `2250830`, revision 8 PR #19's from
`88d0d36`, revision 10 PR #19's from `e0b1671` and revision 11 PR #19's from
`4512441` (R1); a revision record cites PR #19 at the head it names. Nothing
here was
run against a repository: the plan step ran no `project` and no owner tool
(R18).

## R1. Authority, pins and re-pins

- **Finding**: C-56 (Q2 A) and A1's task 1.7 set the plan after feature 004
  merges into `main`, on Brett Heap's word given after that merge; spec 005 at
  `f47c2fd` (its commit 3av) records in C-56 and its Status that his word below
  moved that order for the plan step, and in C-72 his words on the plan's held
  items (R20). Feature 004 has not merged: PR #33 is a draft, its branch now at
  `904aefc`, the plan's cites at `d6bac50` (below). Brett
  Heap said, at 2026-10-22T19:46:57Z, "lane 4
  plans 005 now".
- **Decision**: that word moves C-56's order for this plan step only, as his
  "lane 4 specifies 005 now" moved change 2's order for the specify step
  (C-21). It authorizes this plan and nothing after it: no `tasks.md`, no
  code and no test is written, and the tasks and the implementation each
  wait for his word (R2). His words on the held items, "yes, recommended for
  O1-O10" (2026-10-22T21:24:03Z), "yes, recommended for O3, O5, O8-O11 and D5
  clause 2" (2026-10-23T12:19:11Z, RULED at 12:21:32Z, issue #10), "yes,
  recommended for O12-O16" (2026-10-23T13:30:30Z, in lane openRepoProject-3's
  pane, RULED there at 13:32:29Z) and "yes, recommended for O17-O21"
  (2026-10-23T21:10:35Z, in lane openRepoProject-4's session, RULED there at
  21:11:44Z, issue #10), all in C-72, choose options for change 2 and are no
  word for the tasks or the implementation either. This plan pins its reads
  at:
  - feature 004's `project`, tests and documents at `d6bac50`; its later head
    `f3724fc` (doc round 24) changes three documents only (`hand-runs.md`,
    `tasks.md`, `traceability.md`), `project` and the tests unchanged since
    `d6bac50` (`git diff --quiet`), so the plan names it as a later head only;
    its head `d8724e2` (lane openRepoProject-2's R-365, ruled by Brett Heap,
    merged on 2026-10-23) changes, of its 326 top-level definitions compared
    by syntax tree, `TEXT`, which gains one row and changes none,
    `partial_removal_text`, `print_result` and `repo_state` alone, none of
    which the overview reuses but `TEXT`'s rows, so the plan keeps its cites
    at `d6bac50` and names `d8724e2` as a later head; its suite holds 494 test
    methods there; and `project status --json`'s stale recommendation beside
    an unread row (T9) is 172 characters there, a text the overview never
    shows (C-59). Its head `41759a4` (2026-10-23T18:35:26Z; lane
    openRepoProject-2's report to lane 4 of 2026-10-23), a descendant of
    `d8724e2`, holds the A-items, Brett Heap's Q1 to Q5, Q8 and Q9 (b), built
    at `703b58c` and merged as `1579c22`, and doc rounds 25 and 26, its suite
    516 OK (skipped 1) and validate 7 of 7 by that report, and is named as a
    later head too. Compared by syntax tree with `d8724e2` (lane
    openRepoProject-4's map of feature 004 at `41759a4`, which this revision's
    own comparison agrees with), it adds six top-level definitions and changes
    24, four in a docstring alone; of the 75 definitions that R3 reuses, nine
    change in code. `STATUS_PINS` gains `-c core.ignoreCase=false`, the fifth
    pin, which `GIT_KINDS`, its text unchanged, gives kind `status` (Q1; O20
    (A), chosen). `TEXT`, of the rows the contract names, ends the locked
    stale text with Q3 (b)'s warning, 318 characters, and gains the plain
    stale text with it, 305 (O18 (A), chosen), its other named rows keeping
    their words.
    `row_evidence` gives a stale, unlocked row that 305-character text, a
    third override beside the two R12 names, and sets a `detached` flag, which
    `classify` and `WorktreeRow` read in place of the branch text `detached`
    (lane openRepoProject-2's wave 22 triage, its T10). `status_warned` counts
    a blank line on standard error as a line (Q8). `resolve_merge_target`
    finds no local branch for a name that holds a lone surrogate, and
    `os_error` and `_direct` record the error of a path that holds a NUL byte
    as `os-error` (T7). The other 66 keep their own text, `RECOMMENDATIONS`,
    `SECOND_RECOMMENDATIONS`, `STATUS_PROBE` and `StatusParser` among them,
    though some call a changed one (`verify_registration` runs with
    `_direct`); `identity_probe` and `repo_state`, which R3 names as not
    reused or never called, do not change either, `repo_state` having changed
    at `d8724e2` alone. The plan names no `NEXT_STEPS` row; that table gives
    `unstarted-branch` and `reflog-unavailable` Q5's words, 248 and 243
    characters (O17 (A), chosen). Of the definitions R3 names as not reused or
    mirrored, `status_probe` changes its docstring alone; at `41759a4`
    `_read_row` makes a registered path that is a symbolic link
    `registration-mismatch` (Q9 (b)) and `worktree_rows` adds `enclosing_rows()`
    (Q2 (1); with `_read_row`'s case, O19's), both in every command, and at
    feature 004's head `904aefc` (its `project` is d640539's, byte for byte)
    both are `project clean`'s alone (lane openRepoProject-2's R-409, from lane
    openRepoProject-3's W139 MEDIUM-1): `worktree_rows(repo, run, records=None,
    for_clean=False)` (`:3639`) and `_read_row(..., for_clean=False)` (`:3522`,
    Q9 (b)'s rule at `:3557`) take `for_clean`, which `match_target()`
    (`:4547`), `build_plan()` (`:5019`) and, for the symbolic-link rule alone,
    `registry_twin()` (`:6343`) set true and `repo_state()` (`:7547`) leaves
    false, so `project status`, `doctor` and `update` read an enclosing row and
    a symbolic-link path as the baseline did, and `enclosing_rows()` (`:3391`)
    runs only for `for_clean`; what stays shared by every command is R-67 (c)'s
    rule, `shared_paths()` and `shared_identities()`, which make a row
    `registration-mismatch` everywhere; `worktree_rows` also sets
    `WorktreeRow.holds` (`:3764`; Brett Heap's M3 (a), a path that is, holds or
    shares another's), which only `excluded_groups()` reads, and makes each
    present row on a branch `inspection-error` where the merged-set listing
    fails, its ref listing read (O21's), in every command, unchanged since
    `41759a4` (`:3717-3724` and `:3760-3761` at `904aefc`, `:3685-3692` and
    `:3727-3728` at `41759a4`);
    `hidden_state_probe` with the new `nested_git_check` excludes a nested
    `.git` as `contains-submodule`, a gate the batch alone applies (FR-032).
    T9 is unchanged at `:7464-7465` there, `UNREAD_NEXT_STEPS` at `:5770-5774`
    and T6 and T7 at `:934-939`. The `project:N` cites stay at `d6bac50` until
    tasks are written (plan.md's Citations): of the plan files' 209, the map
    finds 10 at the same lines at `41759a4`, 181 moved with their text and 18
    changed; and its head `904aefc` (2026-10-23T22:46:29Z; lane
    openRepoProject-2's report to lane 4 of 2026-10-23, its R-424), which has
    `41759a4` and `d640539` as ancestors and merges doc rounds 27 and 28 with
    the code of R-409 and M3 (a), its `project` that of `d640539` byte for byte,
    its suite 520 OK (skipped 1) and validate 7 of 7 by that report, is named as
    a later head too: compared by syntax tree with `41759a4` (lane
    openRepoProject-4's own comparison for this revision), its `project` has the
    same 332 top-level names, none added or removed, eight changed in code and
    three in a docstring alone, and of the definitions that R3 reuses two change
    in code, `TEXT`, which gains one row,
    `next_step_registration_mismatch_holds`, M3 (a)'s 197-character step, a text
    of `project clean`'s alone (C-59), and `WorktreeRow`, which gains the
    attribute `holds`, default false, never serialized and read by
    `excluded_groups()` alone; `STATUS_PINS` (`:1169`), `status_warned`
    (`:3139`), `row_evidence`, `classify` and every other reused definition keep
    their code, so no reused decider's signature or result changes, and
    `nested_git_check()` stands at `:5567`;
  - PR #19's change 1 at `54e869b`, its round (t) (2026-10-23; R-413, Brett
    Heap's M1 (a) and M3 (a)), after its round (s) at `dab8a64` (R-408, R-409)
    and its round (r) at `4512441` (R-391), which states the four stale forms in
    [L] and qualifies Q8's consequence, and its round (q) at `818311a` (Brett
    Heap's "yes, recommended for Q1-Q9", R-380), which withdraws F-1's (b) text
    beside an unread row by Q3 (a), ends the plain forms of T2 to T7, and T8,
    with Q3 (b)'s warning and puts T9 in [E], leaving T1 to T7's unread forms
    word for word, its round (p) at `e0b1671` (R-365 and R-377), which adds T9
    and F-1's (b) text beside an unread row, its round (o) at `88d0d36` (R-349)
    and its round (n), `2250830`, accepted by lane openRepoProject-2 (R-345),
    with T1 to T8 confirmed by Brett Heap ("R-320: yes" for T6 to T8) and their
    warnings in the words of his "R-324: yes" (the lead's R-343);
  - A1 at `e4a30fc`;
  - #24's change at `fe5b245` (PR #27 at `d95eea2`, its round B24, moved
    from `04be7f6` in revision 3, from `dafe476` in revision 5 and from
    `288fc34` in revision 8; its eight pinned ranges byte-identical by the
    lead's `cmp` at each move, at `d95eea2` its proposal's :803-806,
    :834-837, :937-949 and :967-968, its design's :1199-1202, :1278-1281
    and :1938-1944 and its tasks' :198-213, round B24 editing only its two
    ADDED requirements among its deltas, and its `project-overview` block
    blob `a40458cb` at `fe5b245`, `04be7f6`, `dafe476`, `288fc34` and
    `d95eea2` alike) and #25's at `05a424a` (PR
    #29 at `a529310`), both read only to confirm that neither gates this
    feature (C-71).
- **Re-pin of revision 1, feature 004** (its lines cited at `d6bac50`):
  `0a82a62` is three merges after the first draft's `4b4c36b`: `7e0a61e`
  (`impl/004-codex-closed-stdout`, R-322: a `--json` apply run whose standard
  output was closed at startup refuses before any removal, in `check_writes`,
  `:3809-3840`), `12c1821` (`impl/004-r320-stale-cap`: T6 and T7 as `TEXT` rows
  `:887-892` with `stale_recommendations`, `:4401-4421`, and the preview's
  `UNREAD_NEXT_STEPS`, `:5525-5529`; T8 in `remedy_inspect_cap`, `:806-809`)
  and doc round 21. Every `project:N` cite here was moved by a line map of the
  two files and spot-checked by text: no definition the overview reuses changed
  but in its line, the runner (`:1125-1986`), the parsers (`:1988-2255`) and
  `Invocation` among them byte for byte, and `row_evidence` (`:3263`) only in
  its docstring. None of the three merges reaches the overview's texts: its
  stale and cap texts stay A1's (R20, O6 and O8), and it calls neither
  `check_writes` nor `stale_recommendations`.
- **Re-pin of revision 1, PR #19** (its lines at `20084cd`): `20084cd`
  leaves `specs/project-command/spec.md` byte-identical to `ccc52b9` (by
  `cmp`), so PCM cites stand; `specs/project-clean/spec.md` gains a
  five-line AND at its lines 1099-1103, after line 1098 (T8 in "Row cap and
  planning failures"), so a later line moves down 5; its design carries T6
  and T7 at lines 1337-1350 and T8 at lines 1440-1446, and F-1's (b) stays
  OPEN in its Open Questions at lines 2187-2192.
- **Re-pin of revision 3, feature 004** (its lines cited at `d6bac50`):
  `211e43d` is `0a82a62` with lane openRepoProject-2's doc round 22 and the
  merges of R-332 for row 4c (`worktree_config`, `:3054-3075`) and R-336 for
  row 4b (`main_worktree`, its `:2931`), both through a new pure function,
  `config_key_unset` (`:2749-2761`), an exit 1 being the key unset only when
  Git printed nothing; and of lane openRepoProject-3's W90 fixes (R-329's third
  note in `rescan` and `partial_removal_text`; R-291's line-feed tests). The 44
  moved `project:N` cites were moved by a line map of the two files, and every
  top-level definition of both was compared by text: only `main_worktree`,
  `worktree_config`, `rescan` and `partial_removal_text` changed, none of which
  the overview reuses, and `config_key_unset` is new, which R3 and R9 now
  reuse; every reused definition (the runner, the parsers, `Invocation`,
  `resolve_merge_target`, `:2517-2557`, and its caller, `:3206-3208`,
  `relative_config_paths`, `:977`, `CONFIG_PATH_EXTENSION`, `:974`, and
  `row_evidence`, `:3263`, among them) and every other one this plan cites,
  `stale_recommendations` (`:4401`) among them, is unchanged but in its line.
  The suite holds 491 test methods (484 at `0a82a62`), `tests/` holding the
  same files. Feature 004's `TEXT` rows then still carried the warning before
  R-324's words; they take them at `d6bac50` (below).
- **Re-pin of revision 3, PR #19** (its lines at `2250830`): `2250830` is round
  (n), two commits on `20084cd` (`e6b6b16` and `2250830`).
  `specs/project-command/spec.md` is byte-identical (by `cmp`);
  `specs/project-clean/spec.md` changes in R-324's closing phrase alone,
  rewrapped, so its ladder sentence moves from line 164 to PCL:166 and T8's AND
  to PCL:1101-1105; in its design D2's driver is at `#19 design.md:215-220`, D9
  at `:635`, D14 at `:982`, D7's row 4c sentence at `:487-488` with its new row
  4b sentence at `:511-515` (R-336), T6 and T7 at `:1347-1367`, which now say
  "plan" where they said "plan or listing" and give T7 as the report row's
  recommendation alone, T8 at `:1457-1466`, R-343's sentence at `:1467-1475`
  (`:1696-1705` at `54e869b`, below), and F-1's (b), not ruled then (RULED in
  round (p), below), at `:2214-2219`. R-343 records Brett Heap's
  "R-324: yes" (2026-10-22T21:23:55Z): every no-prune warning closes "so do not
  run git worktree prune, git worktree remove or git gc until it can", and T8's
  clause reads "if a worktree's path cannot be read, do not run git worktree
  prune, git worktree remove or git gc until it can".
- **Re-pin of revision 4, feature 004**: `d6bac50` is `211e43d` with lane
  openRepoProject-2's doc round 23, which merges R-324 into feature 004
  (`impl/004-r324-remove-gc`, `e8dda2a` and `28db786`) and lane
  openRepoProject-3's W100 LOW-B tests (`2057c31`). Of the 324 top-level
  definitions, compared by text at both heads, only `TEXT` changes: its
  no-prune warnings take R-324's words. Lines up to `:732` stay, lines inside
  `TEXT` move by up to 12 and every line after it by 14, so 138 cite
  occurrences moved by a line map of the two files (127 in this file, 4 in the
  data model, 7 in the contract), and three that `TEXT`'s change rewrote were
  placed by content: T8's `remedy_inspect_cap`, `:795-797` to `:806-809`, and
  T6 and T7, `:873-878` to `:887-892`, whose texts now equal PR #19's T6 and T7
  word for word. Every reused definition but `TEXT` is unchanged but in its
  line, and the `TEXT` rows the contract names keep their texts (`:824-827`,
  `:854-855`, `:876`, `:877`, `:897`). The suite holds 491 test methods,
  `tests/` the same files; `tests/clean_support.py` changes its `TEXT_FIXTURES`
  alone, so the helpers R18 reuses are unchanged.
- **Re-pin of revision 4, PR #19** (its lines at `88d0d36`): `88d0d36` is
  round (o), one commit on `2250830` (R-349). Its specs equal round (n)'s
  (`git diff --quiet`; round (p), below, changes `specs/project-clean/spec.md`),
  so the PCM and PCL cites stood; its design gains two lines at `#19
  design.md:73-76` (`:73-92` at `54e869b`, lines 74-90 now also naming rounds
  (p) to (t)), so every design cite after them moves by 2, each checked by
  content: D2's driver at `:217-222`, D7's row 4c sentence at `:489-490` and
  row 4b's at `:513-517`, D9 at `:637`, D14 at `:984`, T6 and T7 at
  `:1349-1369`, T8 at `:1459-1468`, R-343's sentence at `:1469-1477`
  (`:1696-1705` at `54e869b`, below), and F-1's (b), not ruled then (RULED in
  round (p), below), at `:2216-2221`; its proposal changes in place at its line
  1314 and from its line 2338 on, none of which this plan cites.
- **Re-pin of revision 8, PR #19** (its lines at `e0b1671`, by lane
  openRepoProject-4's cite map of PR #19, every range checked by `cmp`):
  `e0b1671` is round (p), one commit on `88d0d36` (R-365, R-377). Its
  `specs/project-command/spec.md` and review-safety spec are unchanged (`git
  diff --quiet`), so the PCM cites stand; `specs/project-clean/spec.md` gains
  23 lines in four hunks, F-1's (b) beside an unread row at PCL:354-361 and
  :1217-1225, an AND at :540-547 and a rewording at :378-380, so `PCL:166`
  stands and T8's AND moves to PCL:1116-1120; its design gains 50 lines:
  round (o)'s header entry at `#19 design.md:73-79` (lines 74-77 now also
  name round (p)), D2's driver at `:220-225`, D7's row 4c sentence at `:492-493`
  and row 4b's at `:516-520`, D9 at `:640`, D14 at `:995`, T6 and T7 at
  `:1360-1380` and T8 at `:1482-1491`, each byte-identical, so T1 to T8 keep
  their words; R-343's sentence at `:1492-1500`, after which round (p) adds
  T9 (`:1500-1514`), `project status --json`'s stale recommendation beside an
  unread row, which the overview never shows (C-59), a round (p) addition
  only; and F-1's (b), RULED on 2026-10-23 in his answer "Yes, warn
  (Recommended)" (R-365), at `:2253-2265`: `project clean`'s partial-removal
  text beside an unread row, which the overview never shows either (C-59),
  so nothing in its design changes. The no-prune phrase stands at all 28 of
  its old sites, and round (p) adds 12.
- **Re-pin of revision 10, PR #19** (its lines at `4512441`, by lane
  openRepoProject-4's cite maps of PR #19's rounds (q) and (r), every range
  checked by `cmp`): `4512441` is round (r) (R-391), one commit on round (q)'s
  `818311a` (R-378, R-380, R-382), itself one commit on `e0b1671`. From
  `e0b1671` its `specs/project-command/spec.md` changes in 7 hunks, its
  review-safety spec in 7 and `specs/project-clean/spec.md` in 14, so the PCM
  cite moves too: `PCM:263-269` is PCM:273-279, byte-identical. In
  `specs/project-clean/spec.md` Q3 (a) replaces F-1's (b) text beside an unread
  row at PCL:395-399, :582-586 and :1264-1267, `PCL:166` stands (PCL:185 at
  `54e869b`, below), the rewording moves to :416-418 (:457-459 there),
  byte-identical, T8's AND, PCL:1161-1169, ends with Q3 (b)'s warning, and round
  (r) states the four stale forms in [L]
  (PCL:188-212). Its design holds, byte-identical at new lines, D2's driver at
  `#19 design.md:245-250`, D7's row 4c sentences at `:524-526` and `:526-527`
  and row 4b's at `:550-554`, D9 at `:706`, D14 at `:1085` and the recorded
  limits at `:1758-1766`; and, edited: round (o)'s header entry at `:73-87`,
  lines 74-85 naming rounds (p) to (r); T6 and T7 at `:1476-1514`, their unread
  forms (`:1476-1490`) and closing lines (`:1510-1514`) byte-identical, the
  line between them replaced by the plain forms with Q3 (b)'s warning, 305 and
  318 characters, and round (r)'s sentence on the four forms (`:1491-1508`); T8
  at `:1628-1641`, with Q3 (b)'s warning, its "the rows past the cap are never
  read" now at `:1637-1638`; R-343's sentence at `:1642-1651`, which gains
  "(and Q3 (b)'s warning, below, after it)", Q3 (b)'s paragraph following it
  (`:1651-1667`); T9 at `:1667-1685`, its text unchanged, now stated in [E] too
  (PCM:299-309), its plain case before Brett Heap as round (r)'s M1 (ruled (a)
  at `54e869b`, below; R-413); and F-1's (b) record at `:2508-2526`, its unread
  form superseded by Q3 (a). So T1 to
  T7's unread forms keep their words and the plain forms of T2 to T7, and T8,
  do not; T9 and F-1's (b) stay texts the overview never shows (C-59). The
  no-prune phrase stands at all 28 of its old sites; its 40 sites at `e0b1671`
  are 37 at `818311a` and 39 at `4512441`. Lane openRepoProject-3's W137 item 6
  table agrees on every class; where its lines differ from the maps', R-343's
  sentence and T9 take the sentences' own ranges, as the table does
  (`:1642-1651`, `:1667-1685`), which the maps' line images extend, and F-1's
  (b) second site takes the maps' `:1264-1267`, whose last line, kept from
  `e0b1671`'s :1225, the table's `:1264-1266` leaves out.
- **Re-pin of revision 11, PR #19** (its lines at `54e869b`, by lane
  openRepoProject-4's cite map of PR #19's rounds (s) and (t), every range
  checked by `cmp`): `54e869b` is round (t) (R-413), one commit on round (s)'s
  `dab8a64` (R-408, R-409), itself one commit on round (r)'s `4512441`. From
  `4512441` its `specs/project-command/spec.md` is byte-identical, so every PCM
  cite stands (PCM:273-279, PCM:299-309); its review-safety spec changes in 2
  hunks and `specs/project-clean/spec.md` in 4: the scenario for a worktree
  whose path holds the main worktree at PCL:112-129, round (s)'s paragraph on
  the main worktree's recommendation at PCL:207-214 with its scenario at
  :308-319, and the `contains-submodule` gate's sentence at :850-857; so every
  PCL cite after PCL:111 moves down, byte-identical where it moves: Q3 (a)
  replaces F-1's (b) text beside an unread row at PCL:436-440, :623-627 and
  :1307-1310, `PCL:166` is PCL:185, the rewording is at :457-459, T8's AND,
  PCL:1204-1212, ends with Q3 (b)'s warning, and round (r) states the four stale
  forms in [L] (PCL:216-240). Its design holds, byte-identical at new lines,
  D2's driver at `#19 design.md:250-255`, D7's row 4c sentences at `:529-531`
  and `:531-532` and row 4b's at `:555-559`, D9 at `:728`, D14 at `:1107` and
  the recorded limits at `:1813-1821`; and, edited: round (o)'s header entry at
  `:73-92`, lines 74-90 naming rounds (p) to (t); T6 and T7 at `:1513-1568`,
  their unread forms (`:1513-1527`) byte-identical, the line between them
  replaced by the plain forms with Q3 (b)'s warning, 305 and 318 characters, and
  round (r)'s sentence on the four forms (`:1528-1545`), their closing lines
  (`:1547-1550`) byte-identical, the last continued by round (s)'s sentences on
  the main worktree's recommendation (to `:1568`); T8 at `:1682-1695`, with Q3
  (b)'s warning, its "the rows past the cap are never read" at `:1691-1692`;
  R-343's sentence at `:1696-1705`, which gains "(and Q3 (b)'s warning, below,
  after it)", Q3 (b)'s paragraph following it (`:1705-1721`); T9 at
  `:1721-1740`, its text unchanged, stated in [E] too (PCM:299-309), its plain
  case ruled by Brett Heap, M1 (a), at `:1732-1734` (R-413); and F-1's (b)
  record at `:2512-2530`, its unread form superseded by Q3 (a). So T1 to T7's
  unread forms keep their words and the plain forms of T2 to T7, and T8, do not;
  T9 and F-1's (b) stay texts the overview never shows (C-59), and so does Brett
  Heap's M3 (a) next step for a `registration-mismatch` row whose path is or
  holds another's (PCL:120-122), a text that `project clean` alone prints. The
  no-prune phrase stands at all 39 of its sites at `4512441`, and at the same 39
  at `54e869b`.
- **Re-pins still due**: after PR #33 merges, the implementation re-pins
  against that `main`, as C-56 asks, and against PR #19's ratified head; a
  later head of either before then is re-cited the same way before
  `tasks.md` is written.
- **Rationale**: the plan's design depends on feature 004's runner, parsers
  and deciders, which are complete at `0a82a62` (133 of 133 tasks were
  ticked at `2cf34d3`, the spec's re-check); writing it now costs at most a
  re-cite, while C-56's risk, a second plan, is bounded by R3's reuse list,
  which names every interface the plan leans on.
- **Alternatives considered**: waiting for PR #33 (C-56 as written),
  overtaken by his word; pinning at `2cf34d3`, the spec's re-check head,
  rejected because `d6bac50` is the head the lead named and carries the
  later fixes.

## R2. Implementation base and order (brief decision 1)

- **Decision** (recommended): the implementation starts from `main` after
  PR #33 lands, by merging `origin/main` into `005-project-overview`, never
  by a rebase (the organization refuses force pushes). The order of what
  gates it, each step on Brett Heap's word (lane openRepoProject-2's landing
  order):
  1. PR #19's ratification (change 1's amendment; its LQ items carry [E]'s
     pins, scrub, `commondir` check, work-tree probe and configuration-path
     test that this feature cites as pending);
  2. PR #33's merge (feature 004 into `main`), after which it takes `main`
     by merging `origin/main` in, and `impl/*` branches merge into it with
     `--no-ff`;
  3. the archive PR, which archives change 1 once PR #19 and PR #33 have
     landed; PR #33 does not wait on it;
  4. PR #34 (A1) lands by squash after PR #19's ratification of the commits
     A1's four LQ items follow (A1 `tasks.md` 1.7), or sooner without those
     items on his word, with the one re-alignment commit that also carries
     the items his word chose for change 2 (R20), he reviewing its final
     text first;
  5. his word on this feature's tasks, then on its implementation.
  PRs #27 and #29 do not gate this feature in either order (C-71): its
  parity fixtures keep an ignored `local.env` (R18), and #25's `--remote` is
  its own feature after this one.
- **Rationale**: C-56 pins the plan against the `main` that feature 004's
  merge produces; building on that `main` is the base C-56 already implies,
  needs no stacked PR, and lets the implementation cite `main` lines only.
- **Alternatives considered**: (a) stacking on feature 004's branch head
  when the implementation starts, which lane openRepoProject-2 calls sound
  too: it starts earlier, but every 005 PR then waits on PR #33 and
  re-targets when it merges, and it departs from C-56; it needs Brett
  Heap's word, and only the base changes (R3's reuse stands either way);
  (b) cherry-picking feature 004's runner onto `main`, rejected: it forks
  code PR #33 is still changing.

## R3. What the overview reuses, and what is new (brief decision 3)

- **Decision**: the overview is one new subcommand in the same `project`
  script, in new regions after feature 004's, reusing these definitions
  unchanged (`project:N` at `d6bac50`; R1, which records the nine of them
  that change at feature 004's later head `41759a4`, for the re-cite before
  tasks):

  - timing: `TIMING` (`:560-570`): deadline 60, probe budget 5, grace 2,
    reap wait 2, tick 0.1;
  - contracts: `LIMITS` (`:589-600`), for the shared constants and the
    record bounds; `GIT_FLOOR` (`:602`); the `TEXT` rows the contract
    names;
  - git environment: `GIT_SCRUB` (`:1048-1060`, 31 names), `TRACE2_OFF`
    (`:1068`), `PROTOCOL_PINS` (`:1072-1077`), `STATUS_PINS`
    (`:1084-1085`, four pins there, and five at `41759a4`, `-c
    core.ignoreCase=false` the fifth, taken by reference, as R20's O20 (A)
    chooses), `GIT_KINDS` (`:1090-1103`; kinds `probe` and `status`
    only), `git_env` (`:1106`), `git_argv` (`:1119`),
    `relative_config_paths` (`:977`), `config_path_message` (`:1017`),
    `home_directory` (`:995`), `expand_user` (`:1006`);
  - runner: `ChildHandle` (`:1145-1279`), `LIVE_PROBES` (`:1138`),
    `kill_live_probes` (`:1282-1301`), `Interrupted` and `Terminated`
    (`:1310-1328`), `Invocation` (`:1337-1452`, one branch added),
    `signal_scope` (`:1492`), `raising_signals` (`:1562`),
    `signal_wakeup` (`:1638`), `RawOutput` and `DriverOutcome`
    (`:1657-1707`), `git_version` (`:1959`);
  - parsers: `ParseError`, `RecordStream`, `StatusParser`,
    `WorktreeListParser`, `RefParser` and `MergedSetParser`
    (`:1989-2227`);
  - escaping: `escaping_decode`, `json_path` and `human_path`
    (`:2264-2330`);
  - evidence: `RECOMMENDATIONS` and `SECOND_RECOMMENDATIONS`
    (`:2342-2362`), `classify` (`:2365`), `IDENTITY_OPTIONS`,
    `REF_FORMAT`, `STATUS_PROBE`, `GITFILE_BYTES` and `HEAD_BRANCH_REF`
    (`:2577-2589`), `WorktreeRow` (`:2592`), `git_operation`,
    `unparseable_error`, `probe_error` (for `probe-failed` and
    `probe-timeout` only; a `deadline` outcome takes the overview's own
    `error.deadline-exceeded` row, R9, not its "work deadline", `:2666-2667`)
    and `os_error` (`:2630-2675`),
    `_direct` (`:2693`), `presence_from_lstat` (`:2713`), `gitdir_line`
    (`:2793`), `main_worktree_decision` (`:2853`),
    `registration_verdict` (`:2941`), `verify_registration` with
    `fs=_direct` (`:2978`), with `EvidenceError` (`:2615`) and the private
    readers it reaches, `_read_head` (`:2732`), `_realpath` (`:2737`),
    `_gitfile` (`:2803`), `_admin_gitdir` (`:2822`) and `_admin_commondir`
    (`:2836`), called only inside `verify_registration` with `fs=_direct`,
    `status_warned` (`:3012`),
    `WORK_TREE_PROBE` (`:3051`), `shared_paths` (`:3221`),
    `shared_identities` (`:3231`), `row_evidence` (`:3263`),
    `config_key_unset` (`:2749-2761`), the unset test of the extension
    read and of the `core.worktree` read (R9), and `resolve_merge_target`
    (`:2517-2557`), change 1's resolver, called as below;
  - guard: `observed_at` (`:3575`);
  - dispatcher: `divert_stream` (`:3758`), `write_failed` (`:3782`) and
    `advise` (`:3857`);
  - reflog: `reflog_path` (`:5073`) and `reflog_outcome` (`:5086`).

  Changed, without changing any behaviour of feature 004 (its tests pass
  unchanged, FR-049):
  - `Invocation.__init__` (`:1360-1374`) gains one branch: for `overview`,
    `work_end` and `reserve_end` are both the start plus
    `TIMING["invocation_deadline"]`, so `child_budget()` gives
    `min(5 s, deadline - now)` with no reserve (FR-011);
  - `run_bounded` (`:1765-1894`) is factored into `start_child()` (budget,
    spawn, count, budget end; `:1789-1809`) and `conclude()` (the outcome
    from the handle's state and the parser; `:1878-1893`), as R-54's X-2
    leaves to this feature, keeping its `feed_stderr` and `tick` hooks; the
    one-wide loop stays in `run_bounded` between them.
    `start_child(spec, parser, run)` returns either a `DriverOutcome` (no
    time left, `:1795-1796`, or a spawn failure, `:1800-1803`) or
    `(handle, argv, parser, tick, limit)`, raising `Interrupted` as
    `:1792-1793` does; `conclude(handle, argv, parser, name, run)` is called
    after the caller has unregistered and closed the handle's pipes, reads
    no selector, and raises `Interrupted` for `name == "interrupted"`;
  - `parser()` (`:7839`) gains the `overview` subparser and `main()`
    (`:7894`) one dispatch line, placed before its fall-through `return
    inspect_project(args)` (`:7912`). Every `Exception` of an overview run
    is mapped inside its own entry point (R15), so `main()`'s `(Refused,
    OSError)` handler keeps its behaviour for every other subcommand; the
    `BaseException`s reach `main()`'s existing handlers, as they do for
    `clean`: `Interrupted` and `Terminated` (`:7921-7924`), which print
    `Cancelled.` and return 128 plus the signal, and `KeyboardInterrupt`
    with `EOFError` (`:7925-7927`), which print it and return 130.

  **Lane openRepoProject-2's five conditions.** Lane 2 owns feature 004 and
  agrees in principle to these three changes as refactors that keep feature
  004's behaviour unchanged, on five conditions. Each is a gate on the
  changes and on their verification, and lane 2 or lane
  openRepoProject-3 reads the 004-touching diff before feature 005 merges:
  - **(a)** feature 004's existing tests pass with no edit; new tests may be
    added. Check: the whole suite at the change's commit, and no diff in
    feature 004's test files (`tests/test_clean_*.py`,
    `tests/test_status_doctor_update.py`, `tests/test_project.py`,
    `tests/clean_support.py`, `tests/launch_project.py`) against the base.
  - **(b)** the `run_bounded` split keeps `clean`'s output, JSON and
    human, byte-identical: every probe count, every per-probe budget and
    deadline figure, and the cut semantics (lane 2's R-80 P-2; the
    deadline-stopped marker, `deadline_stopped`, `:4355`). Check: a
    side-by-side run of the base `project` and the split one over `clean`'s
    fixtures, each fixture built twice from one script, comparing exit
    statuses, `probes` and `operations`, the documents with each
    `observed_at` masked, and the counting wrapper's child logs (argument
    vectors, directories, order); each command also runs without `--json`,
    its standard output and standard error compared byte for byte; the
    runs include deadline cuts under the launcher's shortened table, with
    a fake Git holding a chosen child so that the cut falls on the same
    child in both. It is a hand run, recorded in the change's pull
    request, not a CI test, since CI's checkout holds no base `project`
    ([quickstart.md](quickstart.md)). The comparison is one script,
    `tests/compare_clean_base.py`, named in quickstart.md, and slice 7 runs
    it again over the final `project`.
  - **(c)** the `Invocation` branch leaves `clean`'s 50 s work deadline and
    its 10 s reserve untouched: the `clean` branch (`:1367-1369`) is not
    edited and the overview's is a branch of its own. Check: feature 004's
    timing tests unchanged, and a new unit test that `Invocation("clean")`
    gives `work_end` 50 s and `reserve_end` 60 s after its start under the
    real table.
  - **(d)** `parser()` and `main()` add `overview` only; `clean`'s
    arguments, help text, refusals and exit codes are unchanged. Check:
    `project SUB --help` byte-identical side by side for every other
    subcommand (`new`, `benches`, `status`, `doctor`, `update`, `clean`),
    `project --help` differing in exactly three hunks, the usage line
    rewrapped to two lines, the `{...}` choices line and the overview's
    help row, both sides run with `COLUMNS=80` (the triage's TB and TD
    measured it over `d6bac50`'s `parser()` on Python 3.10 and 3.12), and
    feature 004's argument and refusal tests unchanged.
  - **(e)** the changes land on `main` after PR #33 (R2's base). If the split
    changes anything PR #19's text describes of the driver or of bounded work
    (its design D1 and D2, `run_bounded`'s contract at `#19 design.md:250-255`;
    D9, the removal child, `:728`; D14, the fit arithmetic, `:1107`), feature
    005's spec says so and PR #19 is not edited for it. Rounds (q) and (r) edit
    D1's body (Q8's rule and its `core.warnAmbiguousRefs` qualifier,
    `:186-196`), D7 (revalidation's `.git` `lstat`s) and the removal child's
    pins in D9 (Q1), and move D2, D9 and D14 with their text; round (s) edits D7
    again (the one call and budget of its `.git` `lstat`s) and rounds (s) and
    (t) move D1, D2, D9 and D14 again. This plan's split changes none of them:
    `run_bounded`
    keeps its signature, its outcomes and every caller. The spec is not this
    plan's to edit, so a finding of that kind goes to lane openRepoProject-4's
    lead before the change lands.

  New, in the overview's regions: the control loop and its slots (R4, R6),
  the per-candidate collectors (R5), the filesystem task (R7), the
  keep-filter parser (R8), the overview's own readers of the extension read,
  the work-tree probe and realpaths (R9), discovery (R10), findings, gates
  and the message composer (R12), the envelope, the human report and the
  writer (R15, R16), and the overview's tables of messages, attention codes
  and remedies (the contract).
- **Not reused**: `run_bounded`'s loop, `fs_call` (`:1896`), `_fs` and
  `_lstat` (`:2678-2711`; `_realpath` is never called directly, only inside
  `verify_registration`, above), `identity_probe` (`:2764`),
  `worktree_config` (`:3054`), `effective_work_tree` (`:3078`),
  `inspect_repository` (`:3109`), `status_probe()` (`:3034-3047`), whose
  composition of `STATUS_PROBE`, `StatusParser`, kind `status` and
  `status_warned` the overview's status step mirrors (plan.md's Risks),
  `_read_row`, `_identity_unchanged`,
  `_read_status` and `worktree_rows` (`:3345-3551`), `read_reflog`
  (`:5153`), `declared_tracking_branch` (`:2440`) and `projects_dirs`
  (`:114-122`): each blocks its caller until one child or call ends, or
  reads as R9 says the overview may not, while the overview's one loop
  drives four children and many tasks at once (FR-019); `projects_dirs`
  resolves `PROJECTS_DIR` on the calling thread (`found.resolve()`,
  `:120`), outside the root task (R10). The overview calls the same
  deciders from its own generators instead, in the same order, but that
  FR-007 puts a linked row's work-tree probe before its re-verification,
  where feature 004 runs it after (`:3539-3542`); no class differs (R9).
  `discover()`
  (`:491`), `repo_state()`, the lookup by name and the recursive project
  snapshot are never called (FR-003).
- **The merge target, by change 1's resolver** (FR-024, FR-025; A1 design
  D3 and its Non-Goal at design.md:73-74, "A second classifier, resolution
  order or path escaper: the overview calls change 1's"):
  `resolve_merge_target(refs, declared)` is pure over the records and a
  name passed in, and its caller reads that name (`:3206-3208`). The
  overview calls it on the keep-filter's records, which hold every record
  it reads (the local heads and `refs/remotes/origin/HEAD`, `:2531-2543`),
  with `declared` the manifest's raw `tracking_branch`, as change 1's
  caller passes it (`:3207`; the call ignores a value that is not a
  string, `:2537`), or None for a manifest shown absent or read without
  one. FR-025's other branches
  are decided before the call: a failed, refused, timed-out or cut
  manifest read, or a failed ref listing, makes no call, `merge_target`
  null and the row's error recorded. The call's `Refused` with code
  `no-merge-target` becomes the `no-merge-target` finding, `merge_target`
  null and no ladder; a non-empty `notes` becomes the
  `merge-target-conflict` finding, whose message is the contract's row,
  the two names escaped for the output's mode (FR-038). `{name, source,
  sha}` is the call's result less `notes`. For that finding's message the
  overview takes NAME from `name` and OTHER from the kept
  `refs/remotes/origin/HEAD` record's `symref` less `refs/remotes/origin/`,
  the field `resolve_merge_target` itself reads (`:2540-2542`), read only
  when `notes` is non-empty, each escaped by `json_path` or `human_path`
  for the output's mode; the note's own message, built with `human_path`
  (`:2554-2556`), is never printed. This reads a field; it is no
  resolution order (A1 design.md:73-74).
- **FR-040's ban kept**: the overview starts only `probe` and `status`
  handles, every one read-only with `GIT_OPTIONAL_LOCKS=0`, the 31-name
  scrub, `TRACE2_OFF` and the seven protocol pins (`GIT_KINDS`, `:1090`);
  it starts no `removal`, `delegate` or `push` child and calls no
  `execute()`; it writes no file; and it calls no function of the plan,
  preview, apply, result or push regions. A test asserts every child's
  argument vector against an allow-list of the overview's subcommands
  (R18).
- **Rationale**: one evidence model is the change's point ([E]); the
  deciders were split out of feature 004's readers for exactly this caller
  (its R-54 X-1; the evidence region's comment at `:2566-2572` names
  "another driver (feature 005's overview)", which "can feed it values it
  read itself"). Reusing the deciders keeps the ladder's
  classification equal to `project clean`'s (FR-026), while new readers are
  needed only where the reading itself must not block.
- **Alternatives considered**: calling `inspect_repository()` and
  `worktree_rows()` on worker threads, one per repository, rejected by A1's
  design D1 (signals land on the main thread; termination and canonical
  output would need cross-thread locking); a separate `project-overview`
  script, rejected by FR-047 and change 2's Impact.

## R4. The control loop and the driver's factoring

- **Decision**: one `OverviewLoop` on the main thread owns a
  `selectors.DefaultSelector` holding the standard output and standard
  error of every running child (non-blocking, as `ChildHandle.start` makes
  them), the read end of the innermost `signal_scope`'s wakeup pipe
  (`signal_wakeup()`) and the read end of the loop's own task pipe, which
  filesystem workers write one byte to when they finish. That pipe is made
  once per process, both ends non-blocking, and never closed; a worker posts
  its byte under a `try` that swallows every `OSError` (EAGAIN included), so
  a stuck worker that wakes after its run writes into a pipe the next run
  drains and discards; the loop drains the pipe to EAGAIN on each wake and
  then scans its task states, never counting bytes. Each wait's
  timeout is the least of `TIMING["selector_tick"]`, every running child's
  budget end, every pending task's wait end, every terminating or killing
  handle's due time (`ChildHandle.due()`) and the deadline. Children are
  started with `start_child()` and ended with `conclude()` (R3), and
  between those the loop feeds each child's parser as bytes arrive, stops a
  child whose parser reports `bound_reached` (a complete outcome, EC-019),
  drains and caps standard error (`keep_stderr`, never shown; FR-022),
  stops a child at its budget, and calls `advance()` on every terminating
  handle each tick, so no grace delays another child (`kill_live_probes`'s
  rule, `:1282-1301`). On deadline expiry it terminates every in-flight
  child at once and refuses every later start (FR-012). At the deadline
  every pending request is answered at once with a `deadline` result,
  whether ready, held for a slot, held by the per-common-directory rule or
  held at a barrier, and the not-started candidates become their rows (the
  data model's `not-started`). A collector stops at its first such result:
  its project row gets one `deadline-exceeded` error, OPERATION that step's
  (its `path` the worktree for a worktree's step), and the steps after it
  stay null (FR-012's "the same error"). The sweep terminates only
  `running` handles; a handle already terminating, for its budget or its
  record bound, keeps its outcome name, which `run_bounded` too decides
  once (`:1827-1837`). The loop ends when no child is running or
  terminating, no task wait is pending and every collector has ended. The
  run enters `signal_scope()` (record-only handlers, FR-044) before the
  configuration-path test and the version check, as `clean()` enters it
  before `check_clean_arguments` and `require_git` (`:7312-7319`), and holds
  it to the end of the write (the contract's "Order of a run"); the loop
  raises `Interrupted` (a `BaseException`, `:1310`) once the slot is set.
  Before a handle's `close()`, each of its two descriptors still registered
  is unregistered, at EOF, at reap or abandonment and in the loop's
  `finally`, as `close()` expects (`:1259-1260`), since a closed
  descriptor's reused number registered again raises `KeyError` on the
  loop, outside every boundary (triage TB's run on Python 3.10 and 3.12).
  The `finally` settles every handle it started, as `_settle()` does
  (`:1744`), before the scope's exit kills any group left
  (`kill_live_probes`); `conclude()` takes the outcome name the loop decided
  and touches no selector.
- **Rationale**: A1's design D1 fixes this shape; feature 004's handle
  already never blocks on termination (its R-30), so four handles share one
  loop with no new process code.
- **One departure from D1's wording: the self-pipe is two read ends.** A1
  names one self-pipe that the workers and the signal handlers write to:
  design D1 (`A1 design.md:86`, `:104`), D2 (`:155`), D8 (`:470`) and N1's
  design impact (A1 `clarifications.md:39`). In this plan that self-pipe
  is two read ends on the one selector: `signal_scope`'s wakeup pipe,
  which the handlers write to (`signal_wakeup()`, `:1638-1641`), and the
  loop's own task pipe, which the workers write to (R7). `signal_scope`
  keeps its pipe's write end private (`:1492-1555`), so the handlers cannot
  write to the task pipe without a change to feature 004's signal code.
  The behaviour D1 asks for, any signal or finished task waking the loop
  at once, holds; no requirement changes. The packet names no pipe; spec
  005 at `f47c2fd` records the choice in its Dependencies, where feature
  004's runner is described: "D1's one self-pipe being realized as two
  read ends on one selector, `signal_scope`'s wakeup pipe and the loop's
  task pipe, with behaviour unchanged (the plan's research.md R4 at
  `6fb619c`)".
- **Alternatives considered**: threads per repository and `asyncio`
  (rejected by D1); polling the workers on the tick alone, rejected because
  a 0.1 s tick would add latency to every one of up to R + 2,561 tasks, R
  the roots given (R7).

## R5. Collectors, the boundary and step order (FR-021)

- **Decision**: each candidate's collector is a generator. It yields
  requests, `GitStep(argv, directory, parser, kind)` or `FsStep(fn, args)`,
  and is resumed with a `StepResult` (the `DriverOutcome`, or a task's value,
  its `OSError` or `EvidenceError`, or its cut). A row task that calls
  `verify_registration(..., fs=_direct)` may end in an `EvidenceError`
  (`:2615`), an `Exception` that is not an `OSError`: the task's function
  catches it and returns its `.error` and `.errno` as the row's error, as
  `_read_row` does (`:3372-3373`), so that it never reaches the boundary.
  Its steps are FR-021's, in order: the marker
  checks (done by its root's task, R10), the identity probe and, when it
  exits 0 and its output is not two non-empty lines, the one-option
  re-reads (`IDENTITY_OPTIONS`, `:2577`; EC-032), in order, stopping at the
  first that fails or is cut, whose error is the row's, as feature 004's
  `identity_probe` does (`:2774-2789`); for the first candidate of a
  repository, that repository's steps: the registry listing, D3's gitfile
  steps where no candidate of the repository seen so far reported a
  superproject working tree, the first registry record is not marked
  `bare`, and its path is `common_dir` (A1 design D3, items 1 to 3, in that
  order, `A1 design.md:164-167`; feature 004 tests `bare` first, `:2876`),
  the manifest read at `repository.root` (at
  the row's `path` when that is null, or at the candidate without Git),
  the extension read, the ref listing, merge-target resolution, the merged
  set, then each row's task, the twin decision (`shared_paths`,
  `shared_identities`), and per row its work-tree probe (where the
  extension is taken as true), its re-verification and its status probe,
  then classification
  (`row_evidence`, then `classify` through it), the reflog gate's reads and
  the findings. The main row of a bare repository (C-68), of a submodule
  checkout and of an unnamed gitfile checkout (A1 design D3, items 1 to 3)
  takes only its `lstat` task: no registration read, no twin decision, no
  probe and no `row_evidence`, its status fields and `classification` null,
  no class finding and no row gate; a bare entry's `branch`, `head` and
  `merged_into_target` are null too (O16 (a), chosen, built now, ahead of A1's
  text; C-68, FR-008). Feature 004 builds no such row (`:3525-3530`), and
  through its deciders a bare row would be `detached` (`:3307-3308`) with a
  registration that disagrees (`:2998-2999`). When the working directory's
  realpath failed or was cut, a row that `classify` gives `merged-removable` or
  `merged-current` is `inspection-error` instead, with the class's finding
  and no row error, the one `realpath` scan error recording the cause
  (FR-026; A1:444-451): the ratified rule, which R20's O9 (A) keeps and its
  (C) would have widened to every present row. After a failed or cut step
  of the repository's own, the rest run as the packet has it, each failed
  child nulling only the fields it and its dependants would have
  established (DI:539-543): a failed registry listing leaves the extension
  read, the ref listing, the merge target and the merged set to run, with
  no row to probe; a failed ref listing makes no merge-target call and no
  merged-set child, and leaves every class null (FR-025, FR-026; O12 (A));
  no merge target means no merged-set child and no ladder (FR-025); and a
  manifest refusal ends that candidate's collection at the manifest step,
  its identity kept (C-24; A1:405-408). A candidate that merges later can
  still report a superproject working tree: the root then becomes null as
  D3's item 1 says, and a `core.worktree` read already made is one of R14's
  uncut divergences. A collector may hold several filesystem requests at once,
  at most 16 of them running per run (`OVERVIEW["fs_tasks"]`, the data model's
  Constants), an internal constant of the loop and no limit, so not in
  `limits`, a cut task freeing its place; a queued task's wait starts when it
  starts, so that a repository of 512 rows never opens 512 files at once
  against a low descriptor limit, and a hung mount holding more than 16 rows
  takes waves of 5 s, the later tasks past about 192 hung ones (60 s / 5 s x
  16) recording `deadline-exceeded`, not `probe-timeout` (scenario 24's few
  tasks fit in one wave). A `Thread.start()` failure becomes that task's error
  inside the boundary (`internal-error`, class `RuntimeError`). The boundary is
  one `try`/`except Exception` around each resume: an exception becomes that
  candidate's row error by the collector table (`internal-error`, message
  `internal error (CLASS)`), the generator is closed, evidence already held
  stays and every other field stays null. `Interrupted`, `Terminated` and
  `KeyboardInterrupt` are `BaseException`s and pass. A merge is the identity
  step's result: a candidate whose common directory's `(dev, ino)` is already a
  repository joins it and its generator ends.
- **The manifest's place**: FR-021 at `f47c2fd` places "the manifest read
  at `repository.root` once that is named (after the identity probe where
  the candidate is the main worktree, else after the registry listing and
  design D3's steps), always before the ref listing (design D9), or at the
  candidate for a row without Git", and A1 design D9 needs it before the
  ref listing, whose keep-filter takes its `tracking_branch`. The plan
  reads it there; row errors keep that step order. The candidate is taken
  as the main worktree, before the registry listing, when its `.git` is a
  directory whose realpath is the reported `common_dir`, read in its
  identity step's task (R7); for any other candidate the manifest is read
  after the registry listing and D3's steps. In D3
  item 3's layout, a first registry record equal to `common_dir` whose
  checkout no candidate has yet named, a later candidate may still name it
  (D3's third wait, `A1 design.md:196-201`), so that repository's manifest
  read, ref listing and merged set wait with its second phase until every
  candidate's identity probe has completed or failed. Once that wait
  lifts, the owner collector reads, in canonical order, the `.git` of each
  candidate that merged into the repository and is not yet read, one
  bounded task each (R7's "D3's reads"), and names the root from the first
  that names `common_dir` itself, passing the candidate toplevels to
  `main_worktree_decision` in that order, since it takes the first in
  insertion order (`:2886-2888`). The root is then final, and the manifest
  is read there, or at the row's `path` while the root stays null. So the
  manifest, the merge target and the JSON never
  depend on completion order in that layout either (FR-019).
- **Rationale**: generators give D1's continuations with no thread per
  candidate and keep each candidate's row errors in its own serial step
  order, which is FR-037's order for row errors.
- **Alternatives considered**: callbacks per step, rejected as harder to
  read in step order; one function per repository run to completion,
  rejected because it blocks (R3).

## R6. The scheduler: slots, phases and the barrier (FR-019)

- **Decision**: four slots (`OVERVIEW["probe_concurrency"]`, read when the
  loop is made, so that a test sets 1 or 4 in-process; no flag, variable or
  file sets it, FR-047). A Git request waits until a slot is free and no
  running child has the same known `common_dir`; filesystem tasks take no
  slot. Ready requests start lowest rank first (D6's throughput choice).
  Phase 1 (identity and repository-wide steps, the extension read among
  them) may start for any candidate within the cap once discovery has
  ended: every root task has finished or been cut, and the candidates are
  sorted, deduplicated (the first spelling winning), capped at 128 and
  ranked, since the caps apply after canonical sorting (FR-003, FR-017;
  A1:249-250) and D6 dispatches in canonical order (`A1 design.md:402`), so
  that `probes.performed` of an uncut run never depends on which root
  finished first; the cost is at most one 5 s wait. A repository's phase 2
  (its rows' tasks and probes) starts only when (1) every candidate earlier
  in canonical order has completed or failed its identity step, (2) every
  repository earlier in canonical order has finished phase 1, (3) for a
  repository whose first registry record equals its `common_dir` and whose
  checkout no candidate has named, every candidate's identity step has
  completed or failed (D3's third wait), and (4), CHOSEN (O4 (a)) and built
  once A1's re-alignment lands, for a repository in the ordinary layout
  whose main worktree is a Git candidate, that candidate's identity probe
  has completed or failed, since O4 (a)'s detector reads its toplevel (the
  draft at `558b0c29`, :1424-1427; R20). At that point the 512-row cap
  selects its rows by rank and row order (FR-018). Within phase 2, a
  repository's first worktree probe waits until each of its rows within
  the cap has finished its first-read task, so the twins are decided from
  every row (EC-031). A row's re-verification task starts only when a slot
  is free for its status probe, which is then held for it, so that the
  probe follows its re-verification at once, as FR-007's "immediately
  before" asks.
- **Rationale**: A1's design D6; with it the JSON of an uncut run at
  concurrency 1 and 4 differs only in timestamps and
  `budget.probe_concurrency` (FR-019, SC-007).
- **Alternatives considered**: one global barrier after every identity
  probe (deterministic, but holds every repository behind the slowest
  candidate; rejected by D6).

## R7. Filesystem tasks (FR-013; PN-10)

- **Decision**: `FsTask(fn, args, wait)` runs `fn` on a new daemon thread,
  stores its value or exception, and writes one byte to the loop's task
  pipe; the loop waits for it until `min(TIMING["probe_budget"], deadline -
  now)` from its start, then records the cut (`probe-timeout`, or
  `deadline-exceeded` where the deadline was the smaller) and never reads
  its result, but for a root's snapshot. No pool: an abandoned thread stays
  blocked and is never joined (EC-001). The tasks are FR-013's, each one
  thread:
  - one per root: canonicalisation, the dedupe `stat`, one `os.scandir`
    pass and, per entry directory, the marker checks and the holder `stat`
    (A1 design D2), the worker checking the root's cancel flag between
    entries and appending finished entries under a lock. At the root's cut
    the loop sets the cancel flag and, under the same lock, takes a snapshot
    of the finished entries: they stay candidates and `entries` counts them,
    and nothing appended later is read (`A1 design.md:146-153`). A cut
    before canonicalisation ends gives no entries, `entries` null and C-67's
    path;
  - one per Git candidate's identity step: the strict realpath and the
    no-follow `lstat` of the `common_dir` its probe reported, whose `(dev,
    ino)` keys the repository (A1:80-83), and the strict realpath of its
    toplevel;
  - one per manifest read (stat, then a read of at most 1 MiB of a regular
    file, `fstat` again on the open file, FR-014), parse included;
  - one per worktree row within the cap: its `lstat`, strict realpath and
    registration reads (`verify_registration(..., fs=_direct)`), the
    `commondir` read included; the missing-main `lstat`, and D3's `.git`
    reads with the realpath of `core.worktree`, take the same shape;
  - one per re-verification that FR-007 makes immediately before a status
    probe, enclosing the same reads again (lane openRepoProject-2's R-101
    (j); R17), the task FR-013 at `f47c2fd` names in those words;
  - one per linked row whose work-tree probe ran: the strict realpath of
    the toplevel it printed, compared with the row's;
  - one per reflog read (at most 64 KiB, `reflog_path`, `:5073`);
  - one at start for the working directory's realpath (FR-026);
  - CHOSEN (O4 (a)), built once A1's re-alignment lands: one per repository
    for its detector (R20), in the gitfile layout where `core.worktree` is
    set the read of the `.git` of the directory it names, and in the
    ordinary layout where the main worktree is no Git candidate the strict
    realpath of the toplevel its `main-toplevel` child printed.
- **The bound (PN-10)**: abandoned workers are bounded by the tasks a run
  can start, since no task starts after the deadline: one per root given,
  R, each canonicalised before the 32-root cap applies (C-67), 1 working
  directory, at most 4 per candidate (identity step, manifest, D3's reads,
  missing-main `lstat`; 128 candidates) and at most 4 per worktree row
  within the cap (first read, re-verification, toplevel realpath, reflog;
  512 rows): R + 1 + 512 + 2,048 = R + 2,561 threads at the very most, in
  practice the few whose call is stuck in the kernel. Nothing caps R: the
  32-root cap of FR-017 applies after every root given is canonicalised
  (FR-001; C-67), so the bound is a formula in R, 2,593 at 32 roots given. This
  count replaces, as the plan's bound, A1 design D8's "at most 32 roots, 128
  manifests, 512 rows, 512 toplevel realpaths, 512 reflog reads and a handful
  more" (A1 `design.md:506-508`), 1,696 at 32 roots, keeping its form, bounded
  by the tasks started and not by time, while A1's text stays as ratified: the
  roots are R, not 32, since they are canonicalised before the cap (C-67), and
  D8's list leaves out the identity step's task, D3's reads and the
  missing-main `lstat`, and the re-verification. Without the re-verification,
  which D8's list predates, the same sum is R + 2,049 (2,081 at 32 roots). Once
  A1's re-alignment lands, O4 (a)'s detector adds at most 1 per repository (at
  most 128), R + 2,689. The plan adds no further cap: a cap on abandoned
  threads would need a new limit and a new code, outside schema 1's closed sets
  (FR-022, FR-047).
- **Rationale**: A1's design D2 and D8; one thread per task keeps a stuck
  call from holding another task's thread.
- **Alternatives considered**: `concurrent.futures` (its shutdown joins a
  stuck thread; rejected by D1); one task per filesystem call (rejected by
  DI:469-470, too costly).

## R8. The ref listing's keep-filter (FR-015; PN-16)

- **Decision**: a new `KeptRefParser(RefParser)` in the overview's region
  overrides `_take` (`:2185-2203`): it parses each record as `RefParser`
  does, then keeps it only if it is a local head (`refs/heads/`), is
  `refs/remotes/origin/HEAD`, or is the upstream that a kept head names;
  for every other `refs/remotes/<remote>/<name>` record it sets the
  remote-copy flag of `<name>` when `<name>` is one of the candidate names
  known before the listing (the manifest's `tracking_branch` less
  `origin/`, `main`, `master`) and keeps nothing else. `for-each-ref
  refs/heads refs/remotes` (`:3199`) sorts by refname, so every head and
  the upstream it names are known before the first remote record arrives
  (A1 design D9); a `refs/heads/` record that arrives after a
  `refs/remotes/` record breaks that order, since an upstream it names may
  already be dropped, and is a `ParseError` (`failed`, `probe-failed` with
  DETAIL `unparseable output`), never a silent drop. When the merge
  target comes from `origin/HEAD`, its remote copy is the symref's own
  target, listed by construction (A1 design D9, `design.md:526-528`), so
  that flag needs no record of its own. `RefParser` itself, used by
  feature 004, is unchanged.
- **Rationale**: FR-015 bounds what the listing keeps by the heads; feature
  004's parser keeps every record and has no hook (its parsers are those of
  `96a08d4`); a subclass is the smallest change that leaves feature 004
  untouched.
- **Alternatives considered**: a `--sort` or extra patterns (more
  children or more output), and a hook in `RefParser` (a change to feature
  004 for a caller it does not have).

## R9. Where the overview reads Git differently from feature 004's code

Each is the overview's own decider, a pure function, so that its test needs
no Git and a later ruling edits one function:

- **The extension read** (FR-007): `true` is true and `false` false; an
  exit 1 with nothing on either stream is false with no error, decided by
  feature 004's `config_key_unset` (`:2749-2761`), which the overview
  calls; any other outcome is true with the row error change 2's table
  gives (`probe-failed`, its DETAIL `unparseable output` for other output;
  `probe-timeout`; `deadline-exceeded`). It reads the common `config` alone,
  without includes, as Git's own format check reads it, which also honours the
  key at format version 0, so that the read neither tests the format version
  nor follows an include (`#19 design.md:529-531` at `54e869b`; the review's R8
  saw an included value unread by `--file`, its c6f, and the key honoured at
  `core.repositoryformatversion = 0`, its c6e, on Git 2.43.0). A1's proposal
  says so of an exit 1 with a warning: it "stays a failure that counts as true"
  (A1 `proposal.md`:1370-1375). Feature 004 reads the key the same way since
  `211e43d`: lane openRepoProject-2's R-332 has `worktree_config`
  (`:3054-3075`) follow PR #19's D7, "an unset value is false and any
  other failure counts as true" (`#19 design.md:531-532`), through
  `config_key_unset` (`:3075`). The one difference left is the
  `probe-failed` row error that A1's table records on the project row
  (A1:369), ratified, which gates nothing and makes the run incomplete
  (exit 1), where feature 004 records none. The only exit 1 with a warning
  is a common `config` that cannot be read, where the identity probe and
  the registry listing already fail (exit 128, measured on Git 2.43.0 and
  2.36.6 by lane openRepoProject-3's W96), so no class differs. No held
  item arises.
- **The `core.worktree` read** (FR-008; A1 design D3, case 3, `A1
  design.md:187-208`; R20's O11). A1 makes the gitfile layout's root "the
  realpath of `core.worktree`, a relative value resolved against the git
  directory, else the toplevel of a candidate whose identity probe reported
  this `common_dir` and whose `.git` file names `common_dir` itself, else null
  with an `unsupported-layout` repair finding" (A1:130-135), and its scenario
  "A separate git directory" (A1:172-175) expects that checkout, with no error,
  where the git directory has no `core.worktree`, whose `git config --get
  core.worktree` exits 1 (A1 `clarifications.md`:79-83). But A1's failure table
  (A1:369) excepts only the extension read's exit 1 and the effective-work-tree
  read, so, read literally, the unset key's exit 1 is `probe-failed`, and the
  scenario's own test fails. Spec 005 at `f47c2fd` records the same conflict
  and his answer: the collector table's row with its two exceptions and, as a
  third that departs from DI:535 the same way, the unset key's exit 1, which
  O11's part 1 adds (spec.md:4531-4534 and :5636-5639), beside FR-008's
  gitfile root sentence (:2680-2687) and its sentence reading the unset key as
  no value (:2689-2699), User Story 8's scenario 1 (:1778-1788) and FR-007's
  note on A1's item 11, both of whose parts his word of 2026-10-23 chose
  (:2603-2615; C-72). The scenario's first case names no exit status, where its
  second case, only a linked worktree a candidate, gives exit 1; the plan reads
  the first case, by that contrast, as no error. The plan reads that conflict
  in ratified text as O11's part 1, built now, which departs from the
  packet's DI:535 as the extension read's exception does: an exit 1 with
  nothing on either
  stream is the key unset (`config_key_unset`, as PR #19's row 4b reads the same
  key, "an exit 1 with nothing printed is the key unset", `#19
  design.md:555-559`, the lead's R-336), so resolution falls through to the
  candidate's toplevel, as the requirement's "else" and the scenario require.
  Any other outcome, an exit 1 that printed anything or any other exit, keeps
  the table's row error (`probe-failed`; `probe-timeout`; `deadline-exceeded`).
  Ratified A1 states no root for it, so `repository.root` stays null, named
  from neither `core.worktree` nor a `.git` file, and no suggestion is given
  that `project clean` would refuse, since #19 makes the main worktree
  unreadable there and refuses the run `target-not-repository-root`; no
  `unsupported-layout` finding is added, since the read failed and nothing
  shows the checkout cannot be named. That the withheld suggestions carry
  `target-not-repository-root` is O11's part 2 (A), chosen, built once A1's
  re-alignment lands; until then they carry no gate code, as for the other
  layouts whose root is null. One decider,
  `core_worktree_value()`, holds both parts. A read that succeeds names the
  root only through the strict realpath of its value, a relative one joined
  to `common_dir`, taken in D3's task (R7). Where that realpath fails,
  `ENOENT` and `ENOTDIR` included, the row records `os-error` (OPERATION
  `realpath`), or `probe-timeout` or `deadline-exceeded` for a cut task,
  and `repository.root` stays null, with no suggestion and no
  `unsupported-layout` finding, exactly as a failed read is built (A1:366,
  :376-377; the lead's C5): no gate code until A1's re-alignment lands, then
  `target-not-repository-root`, O4 (a)'s gitfile test deciding first, since
  a missing directory holds no `.git`, so the case is a redirect with the
  redirect remedy (the draft at `558b0c29`, :1510-1515). Feature 004's
  non-strict `_realpath` (`:2930`) would name the missing path, which
  A1:148-149 keeps out of any suggestion. Where the read runs decides which
  route a relative value naming a missing directory takes. Until A1's
  re-alignment lands the read runs, as A1 design D3 has it, in the
  candidate that reached the repository (`A1 design.md:187-190`), where a
  linked candidate reads that value with exit 0, since Git ignores the
  common `core.worktree` in a linked worktree, so it reaches this realpath
  (triage TA's fixture, Git 2.43.0); under O13 (A), once the re-alignment
  lands, the read runs in the shared git directory, where the same value
  fails the read itself with exit 128, O11's part 2 case, with the same
  root, withheld suggestions and gate code.
- **The read's place, as ratified, and its defect** (R20's O13 and O14).
  Run in the candidate, under `extensions.worktreeConfig` the read in a
  linked candidate returns that worktree's own `config.worktree` value,
  which is not what `project clean` reads at the checkout (its row 4b,
  `:2925-2926`): the overview then suggests a target that clean refuses,
  or, under O4 (a), gives a redirect remedy naming config files that do not
  hold the value (triage TA's fixture, Git 2.43.0). That is the defect O13
  (A), chosen, mends once A1's re-alignment lands: `git -C <common_dir>
  config --get core.worktree`, one child as now, reading the files clean
  reads. A submodule whose only candidate is a linked worktree of its
  module directory, outside the superproject, prints no superproject line,
  so A1's submodule test does not fire, and the gitfile rule names the
  submodule checkout from `core.worktree`, which `project clean` refuses
  as a submodule checkout before any change, exit 2: a known limit, with
  no detection (O14 (A), chosen, built now), like the limits #19 records
  (`#19 design.md:1813-1821`).
- **Realpaths**: the overview's tasks use `os.path.realpath(...,
  strict=True)`, so `ENOENT` and `ENOTDIR` can be told from other errors
  as FR-007 and FR-026 need; feature 004's `_realpath` (`:2737`) is not
  strict, and never raises. The realpaths inside the registration verdict
  stay feature 004's non-strict ones, through `verify_registration` with
  `fs=_direct` (R3), so that the verdict equals `project clean`'s (FR-026).
- **An abandoned child**: feature 004's `conclude()` path maps an abandoned
  handle to `timeout` (`:1882-1883`), as [E] has it (PCM:273-279); FR-011
  makes an abandoned child that the deadline cut `deadline-exceeded`. The
  overview's loop maps that case itself after `conclude()`.
- **The deadline's text**: `OPERATION stopped at the invocation deadline`
  (A1's table), not feature 004's "work deadline" (`:908`).
- **`tracking_freshness`**: the overview's own constant, `local refs only;
  no fetch` (FR-036; C-32), not feature 004's `TRACKING_FRESHNESS`
  (`:4265`).
- **The work-tree probe's place**: FR-007 puts a linked row's work-tree
  probe before its re-verification and its status probe (A1:276-278),
  where feature 004 runs it after the re-verification (`:3539-3542`); no
  class differs.
- **The work-tree probe's output**: "not exactly one line" disagrees, as A1
  is ratified; PR #19's round (j) and feature 004 (`:3078-3106`) read one
  path less the final line feed. Round (j)'s reading is R20's O5, chosen,
  built once A1's re-alignment lands.
- **The wider `registration-mismatch`** (FR-032; R20's O19 (A), chosen, built
  now, ahead of A1's text): #19's round (q) widens the class to a worktree
  whose path is the common directory, the main worktree or another row's
  path, or an ancestor of one, and to one whose registered path is a symbolic
  link. The overview evaluates both cases from evidence it already holds,
  with no new Git child: for the first, the paths of the rows the registry
  listing gives, each row's `path` set against `common_dir`, the main
  worktree's `path` and every other row's `path`; for the second, the mode
  that the row task's no-follow `lstat` of the registered path returns
  (FR-007; R7). One pure decider takes those inputs and names the case that
  holds, if any, so that its test needs no Git. At feature 004's `904aefc`,
  whose `project` is that of `d640539` and which confines both cases to `project
  clean`'s plan, `project clean` gives a linked row in either case
  `inspection-error`, unprobed, its `dirty` null, excluded at the
  `registration-mismatch` gate, and the main worktree's row, where a linked row
  shares its path, `inspection-error` too, at the `main-worktree` gate, while a
  row that such a row holds is read and classified as before (C-72; lane
  openRepoProject-2's reports to lane 4 of 2026-10-23, its R-416 and R-424). The
  overview's class follows it (FR-026), `inspection-error`, so that the gate
  decides no `merged-removable` row, FR-034 withholds `--all-safe` for the
  repository as `inspection-incomplete` and SC-004 takes no new exclusion; a row
  that shares its realpath with another is FR-007's disagreement already
  (EC-031). Whether the overview also status-probes the other rows, and which
  finding it shows for them, is O23, open for his word: until he rules, FR-007
  as ratified, one status probe, `dirty` read, and the class's
  `inspection-error` finding (C-72).

## R10. Discovery details (FR-001 to FR-005; PN-9, PN-13)

- **Decision**:
  - Roots come from `--root` (repeatable), else `PROJECTS_DIR` when set and
    not empty, else `~/projects` and `~/Projects`: the strings
    `projects_dirs` (`:114-122`) selects, with its empty `PROJECTS_DIR`
    read as unset, made with `expand_user` (`:1006`) and `home_directory`
    (`:995`) and canonicalised in the root task, never by `projects_dirs`
    itself, whose `found.resolve()` (`:120`) would run a filesystem call on
    the main thread (A1 design D8, `design.md:504-505`) and skip C-67's cut
    path (FR-001). A relative root is joined to the working directory. The
    expansion, whose `~user` reads the user database (`:1006-1014`), and
    that join run in the root task; a failed `os.getcwd()` makes that root
    `unreadable` with `root-unreadable` (FR-005), never exit 2.
  - **An empty `--root` value (PN-13)** is an invalid invocation: the
    option's type check refuses it, so argparse prints its usage message
    on standard error, exit 2, no JSON and no Git child (FR-039, FR-042).
    An empty string names no directory; read literally, FR-001's join would
    scan the working directory, which no person typing `--root ""` meant.
  - **A root whose listing fails partway (PN-9)**: when `os.scandir` opens
    the root but an entry read raises `OSError`, the root is `truncated`,
    the entries read before the failure stay candidates, `entries` counts
    them, and one `os-error` scan error with OPERATION `scandir` and the
    root's `path` records it; the candidate cap's exactness is then
    `lower-bound` (FR-017). A failure to open the root is `unreadable` with
    `root-unreadable` (FR-005).
  - A marker check that fails other than with `ENOENT` or `ENOTDIR` makes
    that directory an error row (FR-005), its `os-error` OPERATION `stat`:
    the packet's rule, "`ENOENT` and `ENOTDIR` mean 'no marker'" (DI:142),
    so that a file named like its directory (the holder marker's `D/<name
    of D>`) is no error. Change 2's "an error other than 'no such entry'"
    (POD:46, A1:51) is narrower than DI:142, and FR-005 at `f47c2fd` takes
    DI:142's: "any error other than "no such entry" or "not a directory"
    (`ENOENT`, `ENOTDIR`; DI:142)" (lane openRepoProject-3's W96, LOW-7).
- **Rationale**: PN-9's two choices keep what was read (the run is already
  incomplete) and use the codes the closed set already has; FR-022 names
  `scandir` as an OPERATION for exactly such a task.
- **Alternatives considered**: for PN-13, the working directory, or an
  `unreadable` root; for PN-9, dropping the entries read, or
  `root-unreadable` for a root that was partly listed.

## R11. Ordering and ties (FR-037; PN-8; the open Assumption)

- **Decision**: rows by the bytes of `path`, then, for two rows with one
  `path` (PN-8: a `core.worktree` naming a candidate that has no `.git` of
  its own), by rank, the canonical position of the first candidate that
  reached the row; worktrees main first, then by path bytes; findings by
  checkout path bytes, a repository-level finding (null `checkout`) first,
  then by code; row errors in step order; scan errors as A1 design D6 has
  them. The repository-level position is the spec's open Assumption.
- **Rationale**: rank is fixed by canonical candidate order, so the tie
  never depends on completion order (FR-019); a repository-level finding
  (`no-merge-target`, `merge-target-conflict`) explains the worktree
  findings after it.
- **Alternatives considered**: repository-level findings last; ties by
  `common_dir` bytes (null for a row without Git, so not total).

## R12. Messages: one table and one composer (PN-1; D5; item 10)

- **Decision**: every fixed text the overview prints is one row of the
  contract's message table, keyed by code and condition, R20's items marked;
  [L]'s recommendations are read from `RECOMMENDATIONS` and
  `SECOND_RECOMMENDATIONS` (`:2342-2362`), never from `row_evidence`'s two
  overrides (`:3334-3337`), which are feature 004's report texts; at its later
  head `41759a4` there are three (`:3487-3492` there), the third giving a stale,
  unlocked row Q3 (b)'s 305-character text, which O18 (A) takes (R1); the first,
  `"The main worktree is never removed by project clean."` for a main row
  classed `merged-removable` or `merged-current` (`:3335` and `:3510` at
  `904aefc`, `TEXT`'s `recommendation_main_worktree`), is O22's, open for his
  word (R20): until he rules the overview takes it from none of them, and a
  `merged-removable` main row shows those words through the `main-worktree` gate
  (FR-032).
  The overview's stale text without an unread row is O18 (A)'s, chosen: once
  A1's re-alignment lands, [L]'s plain and locked forms with Q3 (b)'s warning,
  305 and 318 characters, as feature 004's `TEXT` at `41759a4` carries them,
  in place of A1's 50-character text and O8 (A)'s 63-character locked form,
  its `RECOMMENDATIONS["stale-worktree"]` (`:2426` there) staying the
  50-character text; until then A1's one 50-character text for every stale
  row. PN-1's sentences are fixed in the contract, each fixed text under 200
  characters (`merge-target-conflict` interpolates two escaped branch names
  and, like every finding no gate gates, is its own text alone, uncut, since A1
  design D5 states the 200 limit for gated messages only), from texts feature
  004 already prints where one exists (`no-merge-target`, `:897`;
  `merge-target-conflict`, `:854-855`; `main-worktree`, `:876`). The message of
  a gated finding is built by one pure function, `compose_message(own, remedy,
  warning=None, whole=False)`: own text, `; `, remedy, within 200 characters,
  the own text shortened with `...` when both do not fit (A1 design D5), a cut
  counted in characters. The own text is never shorter than `...`: it keeps
  max(n - 3, 0) characters, n = 200 - 2 - the remedy's length, so no slice by
  a negative length is taken; where the remedy alone leaves fewer than 3
  characters, the message is `...; ` and the remedy whole, longer than 200
  characters. Until A1's re-alignment lands only `re-run with --root
  <repository parent>` reaches that, at an escaped parent of 177 characters or
  more, in that case only (R20's O15 (A), chosen, built now, ahead of A1's
  text; C-72); once it lands, O17 (A)'s two reflog remedies, 248 and 243
  characters, reach it too, their messages 253 and 248 (R20's O17 (A)). Once
  it lands, O18 (A)'s warned stale texts, 305 and 318 characters, are composed
  with `whole=True`: the own text and any remedy after it are both kept whole,
  uncut, up to 459 and 472 characters beside the redirect remedy (R20's O18
  (A)); the stale forms beside an unread row take the clauses below. Two
  clauses, both chosen, the second by name (C-72), are branches of that one
  function, reached only when `warning` is given, which happens once A1's
  re-alignment lands:
  clause 1, keep the warning whole and shorten the recommendation before it
  (item 10 part 1, R20's O6 (A)), and clause 2, where the warning and the
  remedy cannot both be kept, leave the recommendation out and shorten the
  remedy, a reversal of ratified D5's "remedy kept whole" that only item 8's
  redirect remedy reaches (R20's O4 (a), with O6 (A)), taken first through O6's
  text at `7af798a` and chosen by name on 2026-10-23. The warning is in the
  words of PR #19's round (n) (R-324), 109 characters with its period. Until
  A1's re-alignment lands, neither `warning` nor `whole` is given and D5's rule
  alone applies, with O15 (A)'s floor. The function is tested by length tables
  alone, R20's table among them, under both the ratified rule and the chosen
  clauses.
- **Rationale**: a chosen text then lands as a one-row change, and the cut
  rule, which items 2, 8 and 10 all touch, sits in one testable place.

## R13. A finding's `observed_at` (PN-7)

- **Decision**: the wall-clock completion time of the last step whose
  result the finding's decision read: a Git child's end, or a filesystem
  task's end (a reflog gate, a registration or presence read). A finding
  decided by two sources (a manifest and the ref listing for
  `merge-target-conflict`; a status probe and the ref listing for a
  default-branch finding) takes the later. RFC 3339 UTC to the second, as
  `observed_at()` (`:3575`) writes it.
- **Alternatives considered**: the envelope's `observed_at` for every
  finding not decided by a Git child, rejected: it hides when the deciding
  read happened.

## R14. `probes.estimated` (FR-020; PN-12; item 7)

- **Decision**: `estimated` = 1 (version check) + 1 per Git candidate + 4
  per distinct repository whose identity was established + 1 per Git child
  needed to name the main checkout of a repository whose first registry
  record equals its `common_dir` (A1:283-285; D3 item 3), 1 per
  `core.worktree` read that R5's condition starts + 1 per worktree row
  within the cap that is present
  and registration-verified at its first read (the two-way check of
  FR-007, twins excluded, as A1:285-287 reads it: its second term counts
  the effective-work-tree probe that only that check triggers, A1:276-278)
  and that takes a status probe + 1 per such linked row in a repository
  whose extension read is taken as true. A bare main entry (C-68), a
  submodule checkout's main row and an unnamed git-directory record add
  none (PN-12; A1 design D3, items 1 and 3): none takes a status probe
  (FR-008). It is computed from first reads, and in an uncut run
  `estimated` differs from `performed` only where:
  - a row that its re-verification stops keeps its estimate: `performed`
    1 lower;
  - a linked row whose work-tree probe disagrees, by its output or by its
    toplevel's realpath, `ENOENT` included, takes no status probe: 1 lower;
  - a manifest refusal ends the candidate's collection (C-24): up to the
    four repository children lower, the registry listing having run for a
    candidate that is no main worktree;
  - no merge target, or a failed ref listing: no merged-set child, 1 lower,
    the rows' status probes still running, since their fields are reported
    whatever the class;
  - a candidate that merges later reports a superproject working tree
    after the `core.worktree` read ran (R5): 1 higher;
  - the identity re-reads: until A1's re-alignment lands no term counts
    them, up to 3 higher per such candidate; after it, a re-read that fails
    leaves the rest unstarted, so `performed` is then 1 + k for that
    candidate, k at most 3, against the 4 counted.
  A failed registry listing makes no difference here, the other three
  repository children still running (R5), and twins none, being excluded
  above. Item 7's term is R20's O3, chosen, and comes once A1's
  re-alignment lands: +3 per Git candidate whose identity probe exits 0 and
  prints other than two non-empty lines. That trigger is the triage's R4-3
  refining the option's words as he read them, "+3 per Git candidate whose
  identity probe prints other than two lines" (C-72, which R20 keeps), since
  the re-reads run only after such an exit (R5); item 8's term, 1 per
  repository in the ordinary layout whose
  present main worktree is no Git candidate, for the child that tests it
  for a redirect (the draft at `558b0c29`, :1522-1525), none for sub-item
  (c), whose data the registry already holds (:1434-1437), comes with O4
  (a), chosen, and is off until A1's re-alignment lands, as the detector is
  (R20).
- **Rationale**: FR-020 counts the children a run expects; a row that takes
  no status probe is expected to start none.

## R15. JSON form, error outputs and the writer (PN-6; PN-2; FR-039, FR-044)

- **Decision**:
  - The document is `json.dumps(doc, indent=2, ensure_ascii=True)` and one
    line feed, keys in the order the contract lists them (the delta's
    order), never sorted (PN-6), as feature 004's `write_document`
    (`:3640-3662`) writes its own. Every string field the document takes
    from Git, a manifest or the filesystem passes [P]'s escaper before
    `json.dumps`: `branch`, `upstream` and `merge_target.name` go through
    `json_path`, or `human_path` in the human report, from the record's
    bytes or `row_evidence`'s surrogateescape text alike (`json_path` takes
    a str by its `os.fsencode` bytes, `:2264-2272`), never as the str is,
    which feature 004 writes straight into `json.dumps` (`:3659`), so that a
    byte 0xff prints as FR-038's `\xff`, not as a lone surrogate's
    `\udcff`.
  - Exit-2 outputs: under `--json`, `{"error": MESSAGE, "code": CODE}`;
    without it, `REFUSED: MESSAGE` on standard error. For an exception of
    any other kind outside the boundary (PN-2) the message is `internal
    error (CLASS)`, the same text in both modes, no traceback, exit 2.
  - A failed write to standard output (PN-2): exit 2, no retry, and one
    line on standard error, best-effort: `Cannot write the report to
    standard output (STRERROR).`; a recorded signal decides the status
    instead (FR-039).
  - The writer: the whole report is rendered to bytes (UTF-8, every
    interpolated string escaped by [P]) after the loop has reaped or
    abandoned every child; then, inside `raising_signals()` (`:1562`),
    entered inside the run's `signal_scope`, it is written by `os.write`
    on the standard-output descriptor, in a loop until every byte is
    written, an EAGAIN on a non-blocking standard output waiting on the
    descriptor with `select` inside the raising span, so nothing is
    buffered for exit to flush (C-69). An interrupted or failed write
    diverts the descriptor (`divert_stream`, `:3758`). Where standard
    output has no descriptor (an in-process test), the stream's `write` is
    used; a `sys.stdout` of None is a failed write, `OSError(EBADF)`, as
    feature 004's `write_document` records it (`:3655-3656`), never an
    `os.write` to descriptor 1, which may by then be another file. After the
    raising
    span, and again after the scope has exited, the slot is read, as
    `clean()` reads it after its scope (`:7353-7354`): a recorded signal
    raises `Interrupted` (`read_slot`, `:3868-3874`), so `main()` prints
    `Cancelled.` and returns 128 plus its number (FR-044).
  - Residual of reuse: with standard error closed at start (`2>&-`),
    feature 004's `advise()` prints `Cancelled.` and `REFUSED:` to standard
    output, since `print` falls back to it (`:3857-3865`); the exit status
    129, 130 or 143 still marks no result (C-69). The overview's own
    standard-error lines skip a None `sys.stderr`; changing `advise` would
    be a fourth change to feature 004.
- **Rationale**: one rendering step makes C-66's "rendered whole before its
  first byte" and C-69's raising span hold together; `os.write` leaves
  nothing for the interpreter to flush after a signal.
- **Alternatives considered**: `sys.stdout.write` then `flush`, which can
  leave buffered bytes for exit; feature 004's `internal_error` text,
  `TYPE: TEXT` (`:3580`), rejected because A1's table names the class only.

## R16. Human report details (PN-3; PN-5)

- **Decision**: D10's layout and fixed lines exactly (the contract); count
  nouns stay as D10 fixes them for every count, `1 projects` and `Scanning
  1 roots...` included (PN-5), since FR-045 and SC-010 read D10's lines
  character for character; the `--help` texts are fixed in the contract
  (PN-3). The scanning notice is written under the record-only handlers,
  so a terminal that blocks it (XOFF) holds the run until it resumes: a
  residual, recorded beside EC-015.
- **Alternatives considered**: singular forms for one, a change to D10's
  fixed lines that only an amendment of change 2 could make.

## R17. FR-007's re-verification against feature 004's fix (PN-18)

- **Finding**: feature 004's R-101 fix is built at `d6bac50` as
  `_identity_unchanged` (`:3386-3416`): one bounded call re-reads the
  `lstat`, the realpath and the registration, and a changed value, a
  failed read or a cut stops the status probe. Compared with FR-007:
  - the class is `inspection-error` in both for every outcome, so no class
    differs and nothing goes to the lead under PN-18;
  - a re-read `lstat` failing with `ENOENT` or `ENOTDIR` appends an `os-error`
    in feature 004 (`_direct`, `:2693-2701`), while FR-007 counts it as a
    changed value with no row error; feature 004 has no findings, so its
    `registered: false` on a now-disagreeing registration has no counterpart,
    and the overview's finding is the class's `inspection-error` either way;
  - a cut re-read records OPERATION `lstat` in feature 004; the overview
    does the same.
- **Decision**: the overview implements FR-007 as written, keeps the row's
  first identity, and the parity tests compare classes only (FR-026).

## R18. Test strategy (brief decision 4; PN-14; PN-17)

- **Decision**:
  - **Modules**: new `tests/test_overview_*.py`, one per delta requirement
    group, with `tests/overview_support.py`; feature 004's
    `tests/clean_support.py` (`install_counting_git`, `child_log`,
    `death_watch`, `install_fake_git`, `register_worktrees`, the reflog
    helpers) and `tests/launch_project.py` reused unchanged. Each delta
    scenario has a test named `test_overview_<scenario>`, in human and
    `--json` form; the existing tests pass unchanged. Expected texts, key
    orders, the gate order and `OVERVIEW_LIMITS` come from the tests' own
    transcription of the contract in `overview_support.py`, never imported
    from `project`, one test checking them equal to `project`'s tables, as
    feature 004 keeps its own (`tests/clean_support.py:53-59`, :587-599;
    lead ruling R-42); that also gives scenario 48 its oracle. Feature
    004's `counted`, `snapshot`, `assert_error_document` and
    `plant_configuration` are methods of its test classes, not of
    `clean_support.py`, so `overview_support.py` carries its own.
  - **The 004-touching changes**: lane openRepoProject-2's conditions (a) to
    (e) of R3, checked in slice 1 before the change is read: the suite with
    feature 004's tests unedited (a), the side-by-side run, JSON and human (b),
    a unit test of `Invocation("clean")`'s figures and of `start_child()` and
    `conclude()` in `tests/test_overview_factoring.py` (c), the help diffs of
    every subcommand (d), and the base and the spec check of (e)
    ([quickstart.md](quickstart.md)).
  - **Isolation**: every test runs with a scratch `HOME`, `PROJECTS_DIR`
    set or unset explicitly, `WORKBENCHES_ROOT` at an empty scratch
    directory, so that `project` tries that root alone and never the
    discovery that tries `openBenches` and then `workBenches` (`main`'s #40),
    so no openBenches (formerly workBenches) checkout is read, the fixtures
    outside every Git work tree, and a bin
    directory first on `PATH` holding the counting `git` wrapper and fake
    owner tools (`gh`, `setup-openspeckit`, `openspec`, `onp`, `docker`)
    that log and exit 97; each test asserts that log empty. In-process
    runs add an audit hook, installed once when `overview_support` is
    imported (Python offers no way to remove one) and armed only inside
    `with overview_support.guarded(wrapper_dir):`, so fixture setup,
    feature 004's tests and every other module run unguarded. While armed
    it records each `socket.connect`, each `subprocess.Popen` whose
    executable, resolved with `shutil.which` against the run's `PATH` (the
    event carries `git` as `git_argv` wrote it, `:1119-1121`), is not the
    wrapper, and each `open`, `os.scandir` and `os.listdir` of FR-032's
    paths, to a list that the test asserts empty after the run. The hook
    raises no `Exception`, which the per-candidate boundary would turn into
    an `internal-error` row; a second line raises a `BaseException`
    subclass, so that a violation also ends the run. The partial-clone
    fixture's `remote.origin.uploadpack` names a logging script that must
    never run.
  - **Seams** (A1 design D13): each `FsTask` function reads its leaf calls
    (`stat`, `lstat`, `realpath`, `scandir`, `read`) from one module-level
    table, `OVERVIEW_FS`, when it is called, not when the module is imported,
    since a constant bound at import keeps its old value under
    `tests/launch_project.py`; tests replace entries with `mock.patch.dict` for
    one run, never `os.*` globally, and a slow entry waits on an `Event` that
    `tearDown` sets. It serves the device-and-inode dedupe (one device and
    inode for two realpaths; scenario 1), the two listing orders (`scandir`
    sorted, then reversed; scenario 13), a root's cut canonicalisation and cut
    listing (scenario 23), the hung `lstat` (17), the hung checkout (24), the
    cut manifest and reflog reads, a refused permission under root and the
    working directory's failing realpath (FR-026), and the running-task cap: a
    unit test gives a 512-row repository's row tasks `lstat` entries that wait
    on an `Event`, and asserts that no more than `OVERVIEW["fs_tasks"]` (16) of
    them run at once, a finished or cut task freeing its place (R5). The report
    is built by one function, `render_report()`, named in slice 6, which tests
    patch (scenario 49).
  - **The scanning notice** (scenario 61; FR-046):
    `overview_support.run_with_stderr_tty()` runs `project` with standard
    error on a pseudo-terminal slave (`os.openpty()`, `stderr=slave`),
    standard input from `/dev/null` and standard output on a pipe, and
    reads the master until `EIO`, `\r\n` read as `\n`; feature 004's
    `run_pty_steps` always puts standard error on a pipe
    (`tests/clean_support.py:1143-1146`), so it builds the pipe arm only.
    The test runs the human and the `--json` forms, since the notice and
    the contract's "Order of a run" step 4 apply in every mode and FR-046
    exempts no mode, once through it and once through `run_cli`, and
    asserts the first run's standard error is exactly `Scanning N
    roots...` and a line feed and the second's empty, and the two standard
    outputs equal byte for byte.
  - **Mechanisms the scenarios leave open**: scenario 27 runs `project` in
    a subprocess with a scratch directory first on `PYTHONPATH` holding a
    `yaml.py` that raises `ImportError`, since `import yaml` is made at
    call time (`:74`, `:2501`) and feature 004's suite has no test of the
    missing library to copy. Scenario 49 and FR-039's three kinds patch
    `render_report()` in-process to raise `RuntimeError`
    (`internal-error`), `Refused` (`refused`) and `OSError` (`os-error`).
    Scenario 55 prints `git version 2.34.1` from a one-line fake in
    `overview_support.py`; feature 004's `version-2.35.0` fake
    (`tests/clean_support.py:512-513`) cannot be edited (gate (a)).
  - **The wrapper** is feature 004's counting wrapper
    (`install_counting_git`: one record per child, written before Git
    runs: pid, parent pid, process group, directory, scrubbed names set,
    `GIT_OPTIONAL_LOCKS`, argument vector) first on `PATH`, with its `real`
    set to a probe shim that `overview_support.py` writes. The counting
    wrapper `exec`s Git, so it records no time and no end, sees no
    `GIT_TRACE2*` value and holds nothing (`tests/clean_support.py:219-240`),
    and `clean_support.py` is not edited (gate (a)). The shim has the shape
    of feature 004's Python-backed fakes (an sh prelude, then `python3 -I
    -S`; JSON lines with `time.monotonic()` in `fake-events.jsonl`, read by
    `fake_events()`). Under the wrapper's pid it appends a start line (pid,
    process group, the values of `GIT_TRACE2`, `GIT_TRACE2_EVENT` and
    `GIT_TRACE2_PERF`), applies a matching hold (argument-vector words, an
    optional `-C` directory prefix, a duration, and then either runs Git or
    exits with a given status and one line on standard error), runs Git as
    its own child in the same process group, and appends an end line (pid,
    status); a child cut by SIGTERM leaves no end line. A record and its
    events join on pid. Per child it asserts the seven protocol pins, the
    status pins of `GIT_KINDS["status"]` on a status probe, by reference,
    never a literal list (plan.md's Risks; five at `41759a4`, `-c
    core.ignoreCase=false` the fifth, R20's O20 (A)), `GIT_TRACE2*` at `0`,
    none of the 31 scrubbed names, `GIT_OPTIONAL_LOCKS=0`, an argument vector
    in the overview's allow-list (the contract's "Git children": `--version`,
    `rev-parse`, `worktree list`, `config --get core.worktree`, `config
    --file`, `for-each-ref`, `status`) and one process group.
    `assert_concurrency()` checks the intervals: at most four overlap, and
    no two in one repository (the repository of a directory known from the
    fixture), the identity probes and their one-option re-reads exempt,
    since A1 lets them overlap before `common_dir` is known (A1:265-266;
    `A1 design.md:402-405`; the review's R3-9). Scenario 19 holds every
    `status` for 1 s and then runs it; scenario 24 holds every child whose
    `-C` is the hung checkout; O11 part 2's test makes `config --get
    core.worktree` exit 1 with a line on standard error. Scenarios 16, 57
    and 58 use feature 004's fakes alone: `status-hangs-in` for a path
    (`tests/clean_support.py:527-530`), chained in front of `flood-stderr`
    or `ignored-5000` through `install_fake_git(..., real=...)` for 57 and
    58, as feature 004's own SIGTERM test does
    (`tests/test_status_doctor_update.py:715-751`). The triage's TD
    prototyped the shim with feature 004's helpers unedited.
  - **Zero mutation (PN-14)**: a snapshot of every path under the fixture
    root, `.git` directories included: type, mode, size, `st_mtime_ns`,
    `st_ctime_ns`, a file's SHA-256 and a link's target; access times are
    excluded, since reads update them on most mounts.
  - **EC-033 (PN-17)**: `test_overview_a_worktree_on_a_branch_named_head`
    asserts the row's five upstream fields null, `inspection-error`, the
    project row's `git for-each-ref failed: unparseable output`, and the
    status probes' `git status failed: unparseable output` that Git's
    ambiguity warning causes (`status_warned`, `:3012`) under Git's default
    `core.warnAmbiguousRefs`, which the fixture keeps: with it false the
    pinned probe exits 0 with empty standard error and no row fails on that
    account, as #19's round (r) records (PCM:269-271, `#19 design.md:186-196`;
    EC-033).
  - **The `core.worktree` read (R9; R20's O11)**: scenario 9's test, "A
    separate git directory", passes under part 1, its git directory having
    no `core.worktree`; part 2's case, a fake Git whose `config --get
    core.worktree` prints a line on standard error and exits 1, asserts the
    `probe-failed` row error, `repository.root` null, no suggestion, no
    `unsupported-layout` finding and, until A1's re-alignment lands, no gate
    code, then `target-not-repository-root` (O11's part 2 (A)); a unit
    test of `core_worktree_value()` covers every outcome. Two fixtures
    give `core.worktree` a directory that does not exist (R9): an absolute
    value, with the checkout as the candidate, and a relative one, with
    only a linked worktree a candidate, since the checkout's own identity
    probe exits 128 under a relative missing value; each asserts
    `os-error` with OPERATION `realpath`, `repository.root` null, no
    suggestion and no `unsupported-layout` finding.
  - **Identity outcomes**: three candidate fixtures, each asserting what
    A1 fixes: a main worktree whose `core.bare` is true, as a candidate (an
    error row, `probe-failed` from one child and no re-read; A1:369,
    :376-377); a main worktree that its own `core.worktree` redirects, as a
    candidate (its root its toplevel, A1:100-102, until O4 (a) lands); and
    `git init --bare X/.git`, X the candidate.
  - **The wider `registration-mismatch` (R9; R20's O19 (A))**: fixtures for
    #19's two cases, a linked worktree whose registered path is a symbolic link,
    and rows whose path is the common directory, the main worktree or another
    row's path, or an ancestor of one, with a unit test of the decider over its
    inputs. What they expect of such a row is `project clean`'s at feature 004's
    `904aefc` (lane openRepoProject-2's read of its code, R-416 and R-424;
    C-72), asserted beside the parity tests' comparison with `project clean
    <root> --json` run from the same directory: a linked row that holds another
    row or the main worktree, one registered through a symbolic link and one at
    the common directory or an ancestor of it are `inspection-error`; where a
    linked row shares the main worktree's path, both rows are; a linked row
    inside another is classified as before; every repository so built is
    `inspection-incomplete`, no row carrying an `--all-safe` suggestion (SC-004
    takes no new exclusion). Two assertions wait for O23 and are the ones that
    flip (traceability.md): for a row that holds another or the main worktree,
    or is registered through a symbolic link, its `dirty` (read, by FR-007's
    last case, until he rules; null under (A)) and its finding (the class's
    `inspection-error` finding; `registration-mismatch` under (A)); rows that
    share a realpath (EC-031) are FR-007's disagreement in both readings.
  - **Lengths**: the composer's tests take the product of every gated own
    text (the attention table's read-only and `--all-safe` findings) and
    every remedy of the contract, the expected strings computed from the
    contract's quoted texts and only R20's final lengths hard-coded as the
    oracle, under D5's rule alone and under the chosen clauses, asserting
    at most 200 characters, the remedy whole and the cut prefix, with rows
    of 199, 200 and 201 characters (own text, `; `, remedy), the
    201-character row cut to 200 ending `...`. They add rows at an escaped
    repository parent of 176, 177, 255 and 4,096 characters and one holding
    30 control characters escaped by [P], asserting O15 (A)'s rule, built
    now, ahead of A1's text, `...; ` and the remedy whole, for the `re-run
    with --root` remedy past 176 (R12). Under the chosen texts they add O17
    (A)'s two remedies, 253 and 248, and O18 (A)'s warned stale texts beside
    every remedy that can follow them, uncut, up to 459 and 472 (R20's
    "Lengths"). A unit test runs FR-022's 200-character bound over the error
    table with the longest STRERROR the platform gives.
  - **Parity**: every fixture compared with `project clean <root> --json` keeps
    its ignored file a `local.env` (C-71). Three cases stay out of the parity
    tests, each named there as a lasting difference (FR-026; SC-003): a failed
    ref listing, where feature 004 at `d6bac50` makes each present row on a
    branch `inspection-error` with the listing's error (`:3511-3514`) while the
    overview leaves every class null (A1:434-437), A1's null class kept by his
    word (R20's O12 (A)); a working directory whose realpath fails (R20's O9
    (A)); and a failed merged-set listing, its ref listing read, where feature
    004 at `904aefc` (`:3717-3724` and `:3760-3761`) makes each present row on a
    branch, the main worktree's included, `inspection-error`, keeps a detached
    row's ladder class and makes a row whose path is missing `stale-worktree`
    (`:2488-2489`), while the overview leaves each of them null (A1:434-437), a
    row that FR-007 sets to `inspection-error` directly apart, A1's null class
    staying by his word (R20's O21 (A); C-72). Those three kinds of row, not
    every row of such a repository, are the lasting difference. #19's rounds (q)
    and (r) also differ from A1 as ratified in four places, the fifth pin, the
    wider `registration-mismatch`, the stale text and Q5's two remedies, which
    O17 to O20 choose, (A): the overview takes the fifth pin and evaluates the
    wider class now (O20 (A), O19 (A)), and takes the two texts once A1's
    re-alignment lands (O18 (A), O17 (A)). Of the four, only O19's cases reach
    these tests, which compare classes, and they expect `inspection-error` of
    the rows the bullet on the wider `registration-mismatch` (above) names. The
    loop iterates `project clean`'s rows, which are the inspected ones.
  - **The row-cap fixture** (plan.md's budget table): one root, three
    repositories registered directly, of 505, 10 and 5 rows (520 in all),
    the cap falling inside the second, so 8 rows are past it, 3 in the
    second and 5 in the third. It serves scenario 15 (the scan error's
    count 8; the two project rows' counts 3 and 5), scenario 20
    (in-process, concurrency 1 and 4) and scenario 41: the second
    repository has 10 rows, within the batch row cap, so its real merged
    worktree, which sorts among its first 7 rows, is `scan-limit`, not
    `inspect-cap`, which a repository over 128 rows would give first
    (FR-035's order); the first has 505, past the report cap. One case
    holds the first repository's first status probe past the others'
    (the shim), so that completion order differs from rank order and the
    same rows are still probed.
  - **Git versions**: the suite runs on the CI runners' Git and on Git
    2.43.0 by hand; FR-050 adds `-k test_overview_floor_` to feature 004's
    `git-floor` job on Git 2.36.6, selecting
    `test_overview_floor_version_check_accepts_git_2_36` and
    `test_overview_floor_end_to_end_run`.
  - **Time**: only the deadline scenario shortens time, in-process,
    keeping the deadline-to-budget ratio of 12 (for example 6 s and
    0.5 s), the grace and the reap wait staying 2 s, its bound the
    shortened deadline plus 4 s; a cap or concurrency fixture that sees a
    `probe-timeout` or `deadline-exceeded` fails, never skips. Slow calls
    are injected through the run's own task-function table (Seams), never
    by patching `os.*`, and each waits on an `Event` that the test sets in
    `tearDown`. Fixture sizes and the time budget are in [plan.md](plan.md).
  - Root-only fixtures (a refused permission) skip under root with that
    reason; each has an injected twin that raises `PermissionError`
    through the Seams table (scenarios 2, 8 and 43's permission arm), named
    after the scenario, so that a test of each runs whoever runs the suite
    (SC-012); non-UTF-8 paths run on Linux and skip on macOS; a FUSE variant
    runs where a mount can be made, the injected slow call always.
- **Rationale**: FR-049, A1 design D13 and feature 004's harness, which
  already proved the wrapper, the launcher and the death watch.

## R19. Threat model (PN-15)

- **Assumed**: the person runs `project overview` on their own machine,
  as themselves, over directories they chose; `PATH`, `HOME` and their
  Git configuration are theirs. Some repositories under the roots may
  hold hostile names (control, format and bidirectional characters,
  bytes that are not UTF-8, a branch named `HEAD`), hostile repository
  configuration (`core.fsmonitor`, `core.worktree`, filter drivers,
  `protocol.*.allow`), hostile attributes, and hostile manifests (large,
  deeply nested, not UTF-8).
- **Defended**: no text from a repository reaches a terminal raw (FR-038);
  Git's standard error is never shown (FR-022); every Git child carries
  the pins and the scrub (FR-016), so no remote is reached and no
  monitor runs; the manifest is bounded to 1 MiB before parsing
  (FR-014) and parsed by `yaml.safe_load` in a bounded task; every path
  is read without following links where the spec says `lstat`; nothing
  is written.
- **Not defended, recorded**: filter drivers that a repository's own
  configuration defines and Git's status may run (EC-022); a hostile
  local process changing the estate during the run (EC-023); a parse
  that is slow within 1 MiB, abandoned at its task's wait but still
  using a thread; a hostile `git` first on `PATH`. Git's own ownership
  check refuses a repository another user owns, which the overview
  records as `probe-failed`.

## R20. Held items: O1-O21, D5's clause 2 chosen; O22, O23 open

Brett Heap typed "yes, recommended for O1-O10" at 2026-10-22T21:24:03Z,
against this entry as it stood at `7af798a`; "yes, recommended for O3, O5,
O8-O11 and D5 clause 2" at 2026-10-23T12:19:11Z, against it at `39f4ab6`;
"yes, recommended for O12-O16" at 2026-10-23T13:30:30Z, in lane
openRepoProject-3's pane, on the five items that the review of the plan at
`39f4ab6` raised; and "yes, recommended for O17-O21" at 2026-10-23T21:10:35Z,
in lane openRepoProject-4's session (RULED there at 21:11:44Z, issue #10), on
O17 to O20, which #19's round (q) raised, and O21, which feature 004's
`41759a4` raised. Spec 005 records all four as C-72, and this entry quotes
C-72 at `f47c2fd` (spec 3av; spec.md:961-1181, 221 lines, sha256
`08e05447e640...`) whole, as it stands, O22 and O23 included, which it
records open for his word:

> - **C-72** Q: Which options of the plan's held items does change 2 take: O1 to
> O10 (research.md R20 as it stood at `7af798a` when he answered, reworded at
> `6fb619c` and, at `664461f` as at `464c361`, "five chosen, six open"), O11,
> added in the plan's revision 3 at `664461f`, D5's clause 2, O12 to O16, which
> the review of the plan at `39f4ab6` raised, O17 to O21, which #19's round
> (q) at `818311a` and feature 004's `41759a4` raised, and O22 and O23, which
> #19's round (s) at `dab8a64` and feature 004's `904aefc` raised? -> A: On
> Brett Heap's
> word typed in lane openRepoProject-4's session at 2026-10-22T21:24:03Z, "yes,
> recommended for O1-O10", recorded by lane openRepoProject-4 as a RULED line
> at 21:30:52Z (issue #10), with three NOTED corrections, at 21:33:31Z (O3),
> 21:51:17Z (O8 to O10) and 21:54:01Z (O5), which read his "recommended" as
> choosing only where R20 or the lane's A1 re-alignment draft stated a
> recommendation, change 2 takes five: O1 (A), the draft's item 2, the F-7
> clause on the `unstarted-branch` and `reflog-unavailable` remedies, two next
> steps that #19's round (q) has since reworded (O17; FR-035);
> O2 (A), item 6, `deadline-exceeded` at the overview's reflog gate (FR-034);
> O4 (a), item 8, `target-not-repository-root` for a main worktree that its own
> `core.worktree` or `core.bare` redirects, with the sub-items (c) and (d) and
> D5's clause 2 case (FR-006); and O6 (A) and O7, item 10's parts 1 and 2, the
> warning beside a row whose path could not be read (FR-028, FR-009, FR-035).
> D5's clause 2, item 8's case, was taken then through O6's recommended text in
> R20 at `7af798a`, which carried it, and lane openRepoProject-3 asked, on
> W105's OBS-1, that he confirm it directly. On his word typed in the same
> session at 2026-10-23T12:19:11Z, "yes, recommended for O3, O5, O8-O11 and D5
> clause 2", recorded by lane openRepoProject-4 as a RULED line at 12:21:32Z
> (issue #10), which answers the seven items as the lane put them to him in its
> pane, each with a stated recommendation, and as R20 and this entry recorded
> them open at `39f4ab6`, change 2 takes the rest: O3, item 7's take,
> `probes.estimated` counting the identity re-reads, +3 per Git candidate whose
> identity probe prints other than two lines (FR-020, EC-032); O5, item 9, #19
> round (j)'s reading of the work-tree probe, its output less its final line
> feed being one path (FR-007); O8 (A), item 10, `project clean`'s locked text
> for a locked stale worktree, "Review, unlock it, then prune stale worktree
> metadata manually.", with the same warning (FR-028); O9 (A), the overview
> keeping its ratified rule where the working directory's realpath cannot be
> read, the parity tests leaving that case out (FR-026); O10 (A), LQ-15's
> extension kept, the relative-path test on `GIT_CONFIG_GLOBAL` and
> `GIT_CONFIG_SYSTEM` (FR-043); O11, A1's item 11, both parts: part 1 excepting
> the `core.worktree` read's unset exit 1, nothing printed, from A1's failure
> table, and part 2 (A), any other failure of that read leaving no root and
> withholding every clean suggestion as `target-not-repository-root`, with a
> remedy row of its own, "core.worktree could not be read; repair the
> repository's config, then run again" (FR-007, FR-008, EC-012, User Story 8
> and the discovery-identity checklist's CHK009); and D5's clause 2, by name:
> where the warning and the redirect remedy together pass 200 characters, the
> warning is kept whole, the recommendation left out and the remedy shortened,
> reversing D5's "remedy kept whole" for that one case only (FR-006, FR-035).
> Every item from O1 to O11, and D5's clause 2, is so chosen. They are choices
> for change 2. A1's ordering rule (its `proposal.md:1278-1284`) is the four LQ
> items' and reaches O10 (LQ-15's extension) and O5 (item 9, owed under it);
> the other chosen items that change A1's text, its items 2, 6, 7, 8, 10 and
> 11, rest on his word for change 2 and on #19's rounds; and items 2 and 6 to
> 11 reach A1 in the same re-alignment commit, which follows #19's
> ratification, he reviewing the final text before #34 merges, while O9 (A) and
> O10 (A) keep A1's text as ratified and O11's part 1 is a text re-alignment on
> a lane finding. His words of 2026-10-23 change no text of A1 itself, and A1's
> items 1, 3, 4 and 5 and this feature's tasks and implementation still wait
> for his word. On his word typed in lane openRepoProject-3's pane at
> 2026-10-23T13:30:30Z, "yes, recommended for O12-O16", recorded by lane
> openRepoProject-3 as a RULED line at 13:32:29Z (issue #10) and by lane
> openRepoProject-4 as a NOTED line at 13:35:04Z, change 2 takes the five items
> that the review of the plan at `39f4ab6` and its triage raised and that lane
> openRepoProject-4 put to him on 2026-10-23, each as that lane recommended it.
> O12 (A), a repository whose ref listing fails, where A1 leaves every worktree
> row's class null (its `specs/project-overview/spec.md:434-437`) while
> `project clean` at `d6bac50` makes each present row on a branch
> `inspection-error` (its `project:3511-3514`), A1 also asking the two classes
> to be equal: A1's null class stands, the parity tests naming the case as a
> lasting difference (FR-026; Dependencies). O13 (A), where the `core.worktree`
> read runs, in a repository made with `git init --separate-git-dir` whose
> `extensions.worktreeConfig` is true, reached through a linked worktree, where
> the read made there returns that worktree's own setting, not the one `project
> clean` reads, so that the overview suggests a target that clean refuses
> (measured on Git 2.43.0): the read is made in the shared git directory, which
> reads the files clean reads with no extra Git child, a rewording of A1's
> design D3, case 3 (FR-006, FR-009, User Story 8). O14 (A), a submodule
> reached only through a linked worktree of its module directory, outside the
> superproject, where Git prints no superproject line, so that the overview
> sees no submodule and suggests `project clean` on the submodule checkout,
> which clean refuses before changing anything: a known limit, like the limits
> #19 records, with no detection (User Story 8, EC-012). O15 (A), a remedy
> "re-run with --root <repository parent>" whose escaped parent is 177
> characters or more, where D5's "within 200 characters" and "remedy kept
> whole" cannot both hold: the remedy is kept whole and the finding's own text
> cut to "...", the message passing 200 characters in that case only (FR-035).
> O16 (a), a bare repository's main row, which C-68 makes a worktree row while
> C-40 copies the packet's rule that `branch` is never null: `branch`, `head`
> and `merged_into_target` are null for that row, recorded against C-40 and in
> C-68 and FR-008 (C-40, C-68, FR-008). With these, every item from O1 to O16,
> and D5's clause 2, is chosen. O13 (A), and A1's records for O12 (A), O14 (A)
> and O15 (A), with its design Risks entry for O14 (A) and D5's sentence for
> O15 (A), and an entry for the null `branch`, `head` and `merged_into_target`
> of O16 (a), since A1 adopts the packet's JSON types, reach A1 in the
> re-alignment commit, as O3 and O5 do, that entry being the lane
> openRepoProject-4 lead's choice on lane openRepoProject-3's W130 LOW-1 and
> not his word, which chose O16 (a) itself. This spec builds O12 (A) and O14
> (A) now, as A1 is ratified, as for O9 (A), and O15 (A) and O16 (a) now, ahead
> of A1's text, declared at FR-035, C-40, C-68 and FR-008; otherwise it records
> his words and follows A1 as ratified until A1's re-alignment lands, O13 (A)
> included. On his word typed in lane openRepoProject-4's session at
> 2026-10-23T21:10:35Z, "yes, recommended for O17-O21", recorded by lane
> openRepoProject-4 as a RULED line at 21:11:44Z (issue #10), change 2 takes
> the five items that #19's round (q) at `818311a` raised from Brett Heap's
> "yes, recommended for Q1-Q9" for change 1 (lane openRepoProject-2's R-380),
> O17 to O20, and that feature 004's `41759a4` raised, O21, and that lane
> openRepoProject-4 put to him on 2026-10-23, O18 as refined at 18:27Z and O21
> added at 19:34Z, each as that lane recommended it, (A). O17 (A), Q5's next
> steps for the `unstarted-branch` and `reflog-unavailable` gates, 248 and 243
> characters in #19, which O1 (A) has the overview show once A1's re-alignment
> lands, where a gated message is the finding's own text, `; ` and the remedy
> within D5's 200 characters, so that even with the own text cut to "..." they
> come to 253 and 248: #19's wording is kept whole, the own text cut to "..."
> and the message passing 200 characters for these two remedies too, as for O15
> (A)'s `--root` remedy (FR-035, User Story 4). O18 (A), Q3 (b)'s warning,
> which #19 appends to `project clean`'s plain stale recommendation and its
> locked form, making them 305 and 318 characters, where the overview's stale
> message is [L]'s 50-character text or, under O8 (A), the 63-character locked
> form: the overview takes the warning, its stale message equal to clean's text
> and kept whole past 200 characters, and where a gate's remedy also follows
> the stale message, that remedy is kept whole too, as D5 keeps every remedy,
> the longest case being beside the redirect remedy, at 459 and 472 characters,
> the warning not cut, since a shortened warning would drop the dry run it
> names, the forms for a row whose path could not be read (O6
> (A)) unchanged (FR-028, FR-026). O19 (A), `registration-mismatch`, which #19
> widens to a worktree whose path is the common directory, the main worktree or
> another row's path, or an ancestor of one, and to one whose registered path
> is a symbolic link: the overview evaluates the two new cases from its own
> evidence, the paths of the rows the listing gives and FR-007's no-follow
> `lstat`, with no new Git child, as clean's classification, and SC-004 takes
> no new exclusion (FR-032, SC-004). O20 (A), the fifth status pin, `-c
> core.ignoreCase=false`, which #19 adds to every status probe: the overview
> takes it with feature 004's `STATUS_PINS`, five at `41759a4`, by FR-016's own
> rule, A1's re-alignment adding it to its requirement 3 and design D13
> (FR-016). O21 (A), the sibling of O12, a repository whose merged-set listing
> fails, its ref listing read, where A1 leaves every worktree row's class null
> (its `specs/project-overview/spec.md:434-437`) while `project clean` at
> `41759a4` makes each present row on a branch `inspection-error` (its
> `project:3685-3692` and :3727-3728 there; not at `d8724e2`), A1 also asking
> the two classes to be equal: A1's null class stands, the parity tests naming
> the case as a lasting difference, beside O12's (FR-026, SC-003), for the
> reason the lane gave for those rows on a branch, that neither command
> suggests anything for them, so that only the label differs, and that (A)
> needs no amendment, as O12's answer for the same kind of case. This
> spec builds O19 (A) and O20 (A) now, ahead of A1's text, declared at FR-016,
> FR-032 and SC-004, and O21 (A) now, as A1 is ratified; O17 (A) and O18 (A)
> land with A1's re-alignment, which carries O17 to O20's texts and O21's
> record (the lane's A1 re-alignment draft, its items 17 to 21), and until then
> this spec follows A1 as ratified, the two next steps at 102 and 97 characters
> and one stale text for every stale row. At feature 004's head `904aefc`,
> whose `project` is that of `d640539` and which confines O19's two cases to
> `project clean`'s plan (lane openRepoProject-2's reports to lane 4 of
> 2026-10-23, its R-416 and R-424), `project clean` gives a linked row whose
> path is the common directory, the main worktree or another row's path, or an
> ancestor of one, and a linked row whose registered path is a symbolic link,
> `inspection-error`, unprobed, its `dirty` null, excluding it at the
> `registration-mismatch` gate, and the main worktree's row, where a linked
> row shares its path, `inspection-error` too, at the `main-worktree` gate,
> while a row that such a row holds is read and classified as before; the
> overview's class follows it, by FR-026's parity, a row that shares its
> realpath with another, the main worktree's included, being FR-007's
> disagreement already (EC-031), so that FR-034 withholds `--all-safe` for the
> repository as `inspection-incomplete`, as `project clean` refuses its plan,
> and SC-004 takes no new exclusion; whether the overview status-probes the
> other rows, and which finding it shows for them, is O23, below. Where the
> merged-set listing fails, its ref listing read, `project clean` there still
> gives each present row on a branch, the main worktree's included,
> `inspection-error` (its `project:3717-3724` and :3760-3761 there), while a
> detached row keeps the class the ladder gives it, `detached` in lane
> openRepoProject-2's fixture, and a row whose path is missing is
> `stale-worktree` (:2488-2489); A1's null class, which O21 (A) keeps, leaves
> each of them null, a row that FR-007 sets to `inspection-error` directly
> apart, so that these rows are the lasting difference that the parity tests
> name for O21's case. With these, O1 to O21 and D5's clause 2 are chosen,
> every held item of this feature but O22 and O23, which stay open (below).
> One more item, O22, which #19's round
> (s) at `dab8a64` raised (the lead's R-408, on lane openRepoProject-3's W141
> MEDIUM-1) and which lane openRepoProject-4 put to Brett Heap at
> 2026-10-23T22:39:41Z, with the lane's recommendation, is open for his word,
> and until he rules this spec builds A1 as ratified. O22, the main worktree's
> recommendation: #19 gives the main worktree's row, where the ladder classes
> it `merged-removable` or `merged-current`, one whose upstream was deleted
> included, "The main worktree is never removed by project clean." in place of
> its class's, the class unchanged (its `specs/project-clean/spec.md:207-215`
> at `54e869b`), where the overview's message for a classified row is the
> ladder's recommendation text (FR-028), so that a `merged-removable` main row
> already shows those words through the `main-worktree` gate's finding while a
> `merged-current` main row shows the baseline's "The branch is merged, but
> this is the current checkout; switch away before removal."; (A) follow round
> (s) now, the main worktree's row carrying #19's text for both classes, ahead
> of A1's text, A1's re-alignment narrowing its sentence on a merged row whose
> upstream was deleted, as #19 narrows its own, or (B) keep the class's
> baseline message for the main row until A1's re-alignment carries the
> change, the difference from `project clean` recorded until then;
> recommended, (A), and built until he rules, A1 as ratified (FR-028), whether
> #19's change stands waiting on his ratification of #19. One more item, O23,
> which feature 004's `904aefc` raised and which this spec records for Brett
> Heap's word at its commit 3au, with the lane's recommendation, is open for
> his word in the same way. O23, how the overview reads a linked row whose
> path is the common directory or an ancestor of it, of the main worktree or
> of another row's path, or whose registered path is a symbolic link, cases
> that FR-007's registration cases do not name, though they name a row that
> shares its realpath with another (EC-031): read as written, such a row whose
> registration agrees takes FR-007's last case, one status probe, its `dirty`
> read, its class `inspection-error` by FR-026's parity, with that class's
> finding, where `project clean` leaves the row unprobed, its `dirty` null,
> and excludes it as `registration-mismatch`; (A) read such a row as FR-007's
> disagreement case, no status probe, `inspection-error` set directly, a
> `registration-mismatch` finding in place of the class's `inspection-error`
> finding and no error, as for a row that shares its realpath, A1's
> re-alignment carrying it with O19 (A), or (B) keep FR-007's last case for
> it, one status probe, its `dirty` read, and the class's `inspection-error`
> finding, the difference from `project clean` recorded; recommended, (A),
> which keeps `dirty` as `project clean` reports it, needs no Git child for
> such a row and names the gate that excludes it, and until he rules this spec
> builds FR-007 as A1 ratifies it, as (B) reads it (FR-007, FR-032). Where
> applied: C-40; C-68; FR-006; FR-007; FR-008; FR-009; FR-016; FR-020; FR-026;
> FR-028; FR-032; FR-034; FR-035; FR-043; EC-012; EC-020; EC-032; SC-003;
> SC-004; User Story 4; User Story 8; Key Entities, Repository identity;
> Dependencies; the discovery-identity checklist's CHK009; the security
> checklist's CHK002 and CHK019; the idempotency checklist's CHK008.

In this entry's terms: O1 to O21 and D5's clause 2 are chosen, every held item
but O22 and O23 (C-72). O11's part 1 is built now, as the plan's reading of a
conflict in
ratified text (R9); O9 (A), O10 (A), O12 (A), O14 (A) and O21 (A) keep A1's
behaviour as ratified; O15 (A), O16 (a), O19 (A) and O20 (A) are built now,
ahead of A1's text, as the spec builds them; and every other choice, O1 to O8,
O11's part 2, O13 (A), O17 (A), O18 (A) and D5's clause 2, is built once A1's
re-alignment lands at PR #34, the ratified text standing until then. Feature
004's head `904aefc` states O19's outcome for a row in its two new cases and
O21's case (C-72; O19 and O21, below), and two items stay open for his word, O22
and O23, the plan building A1 as ratified for both until he rules (O22 and O23,
below). Each item stays isolated to
one table row, one decider, one count term or one branch of the composer, so
that a change in his review of the final text lands without touching the rest,
with one exception: a change to O11's part 1 would also re-word the scenario "A
separate git directory" (O11, below). traceability.md's "Held items, chosen:
their tests" names each item's behaviour test and the assertions that flip. The
design changes that the review of `39f4ab6` asks of these entries are made in
revision 9 (its record, below).

PR #19 is read at `54e869b`, its round (t) (R-413), after its round (s) at
`dab8a64` (R-408, R-409), its round (r) at `4512441` (R-391) and its round (q)
at `818311a` (R-380), which leave the unread forms of T1 to T7 unedited and end
T8 and the plain forms of T2 to T7 with Q3 (b)'s warning (for the stale texts,
O18 (A), below); the implementation re-pins at #19's ratified head (R1). Every
warning below is in round (n)'s words (`#19 design.md:1513-1568` at `54e869b`;
R-343, his "R-324: yes"), which feature 004's `TEXT` rows carry since `d6bac50`
(`:887-892`). The lane's A1 re-alignment draft is the source of each option,
not of behaviour: every item, 1 to 11, as read at sha256 `558b0c298f5c...`
(2,928 lines), where revision 4 read items 8 to 11 at `c5840a66bf1f...` (2,888
lines), revision 3 items 8 and 10 and the row 4b section at `811b9cef0889...`
(2,584 lines), revision 2 items 8 and 10 at `8ce4e9fb60e8...` (2,422 lines) and
revision 1 items 1 to 10 at `00205d73ba38...` (2,295 lines). Items 1, 3, 4 and
5 there change text only and have no design impact.

### Chosen (C-72), built once A1's re-alignment lands

- **O1. Item 2, the reflog remedies' submodule clause** (FR-035). CHOSEN
  (A): the overview's two reflog remedies end with " (--force if it holds
  a submodule)", as `project clean`'s next steps do since #19's round (g).
  Design: two rows of the remedy table. Beside `unstarted-branch` the
  merged worktree's own text is then cut to 59 of its 67 characters, and
  the `reflog-unavailable` message is exactly 200, uncut (the table
  below). Until then: A1's ratified texts. O17 (A), chosen since, keeps
  #19's later wording of the same two steps whole in place of the one
  quoted here, and both land in the one re-alignment commit (O17, below).
- **O2. Item 6, the deadline's cut at the reflog gate** (FR-034). CHOSEN
  (A), as he ruled it for `project clean` on 2026-10-22, "O-1:
  deadline-exceeded" (R-263): a reflog read the deadline cuts withholds
  with `deadline-exceeded`. Design: one branch in the repository gate,
  keyed on the cut's limit, which the filesystem task already records.
  Until then: `inspection-incomplete` for both cuts, as A1 is ratified.
- **O4. Item 8, the redirected main worktree** (FR-006; R-271, a lead ruling of
  lane openRepoProject-2's). CHOSEN (a): where a main worktree's own
  `core.worktree` or `core.bare` redirects it, which `project clean` refuses,
  the overview gives no clean suggestion, with a new remedy naming the redirect
  (one more Git child per such repository). Under (a), a bare entry whose path
  plus `/.git` is the common directory (the draft's sub-item (c)) and a
  main-worktree probe that exits nonzero (sub-item (d)) count as a redirect
  too: they apply under the option and are no further options (the draft at
  `558b0c29`, :1309-1311, as at `8ce4e9fb`; lane openRepoProject-3's W96,
  R2-LOW-2). Design: two tests, as the draft's item 8 (a) words them (at
  `558b0c29`, :1424-1433 and :1503-1515). In the ordinary layout, the main
  worktree's toplevel, from its own candidate's identity probe where it is a
  Git candidate, a failed probe included, else from the counted
  `main-toplevel` child, is compared, realpath-equal, with the first registry
  record's canonical path; a nonzero exit of that probe or child counts as a
  redirect (sub-item (d)), and that repository's phase 2 waits for the main
  worktree candidate's identity probe (R6's fourth wait; :1426-1427). The
  child's standard output, less the one line feed Git ends it with, is one
  path, as the identity probe's one-option re-reads read theirs; empty
  output, or output not ending in a line feed, names no toplevel and counts
  as sub-item (d)'s nonzero exit; its strict realpath is taken in one
  bounded task (R7). In the
  gitfile layout, one bounded filesystem task reads the `.git` of the
  directory `core.worktree` names, which must be a file naming `common_dir`
  itself, with no Git child (R7). The `core.bare` variant of a failed main
  probe is D3's case 2 with sub-item (c), not this detector. One remedy row,
  "core.worktree or core.bare redirects the main worktree; unset both in the
  repository's config, or in the main worktree's config.worktree, then run
  again" (152 characters); in `estimated`, 1 per repository in the ordinary
  layout whose present main worktree is no Git candidate, for the child that
  tests it, and none for sub-item (c), whose data the registry holds (R14);
  and the composer's clause 2: where a `stale-worktree` message carries
  O6's warning (109 characters with its period) beside this remedy, the two
  cannot both be kept within 200 characters (109 + 2 + 152 = 263), which
  happens through (a)'s new row and through sub-item (c)'s row, which carries
  the same remedy. Clause 2 leaves the recommendation out and shortens the
  remedy with `...`, reversing ratified D5's "remedy kept whole" for that one
  case: "a row's path could not be read, so do not run git worktree prune, git
  worktree remove or git gc until it can.; core.worktree or core.bare redirects
  the main worktree; unset both in the repository's..." (200 characters).
  Without it, D5 prints "Review and prune stale worktree metadata ma..." and
  the remedy whole, the prune advice with no warning. Clause 2, taken first
  through O6's text at `7af798a`, is chosen by name in his word of 2026-10-23
  (C-72), and a change in his review edits that one branch. Until then: A1's
  ratified behaviour in both layouts, a suggestion that `project clean` will
  refuse, or, where `core.worktree` names another repository's checkout, one
  that resolves that repository (A1:130-131, :148-149); the detector off.
- **O6. Item 10 part 1, the stale warning**. CHOSEN (A): the overview's
  stale message carries the warning while a row's path cannot be read,
  keeping the warning whole and shortening the advice to fit 200
  characters. His "R-320: yes" ruled T6 for PR #19 only and does not
  reach A1 by reference, since #19's ladder is a function of the row's
  evidence alone (PCL:185) while T6 depends on other rows (the draft's
  item 10, lane openRepoProject-3's W86 NM3-1); C-72 chose it for change 2.
  The text: "Review and prune stale worktree metadata manually; a row's path
  could not be read, so do not run git worktree prune, git worktree remove
  or git gc until it can." (160 characters). Design: one message-table
  condition, the overview's own trigger, any worktree row of the same
  repository with `present: null` (#19's T6 fires on any row of its plan,
  `#19 design.md:1513-1568`, and the overview has none). Rows past the
  512-row cap are `present: null` (C-35; the data model's worktree row), and
  so are rows the deadline cut (A1:104-109), so they count: every
  `stale-worktree` message of a repository with a row past the cap carries
  the warning, as #19's T8 warns always because "the rows past the cap are
  never read" (`#19 design.md:1691-1692` at `54e869b`). The design adds the
  composer's clause 1: the warning kept whole and the recommendation before
  it shortened, which keeps D5's "remedy kept whole". Beside the
  report-cap remedy (75 characters at 260 rows) the message would be 237
  characters, and D5's rule alone would cut inside the warning; under
  clause 1 it is 200, the recommendation keeping 9 of its 49 characters
  (8 from 1,000 rows, 7 from 10,000). Beside the bare repository's
  ratified remedy (45 characters) it would be 207; under clause 1 the
  recommendation keeps 39. The beside-the-redirect case is O4's clause 2.
  Until then: A1's one stale text, "Review and prune stale worktree metadata
  manually." Without an unread row, the stale text takes Q3 (b)'s warning
  whole by O18 (A), chosen, 305 characters, as feature 004's `TEXT` gives it
  at `41759a4`, which lands with A1's re-alignment; until then the plan
  builds that 50-character text (R12; O18, below).
- **O7. Item 10 part 2, the `main-worktree-missing` remedy**. CHOSEN, with
  O6: under the same test, "restore or prune the main worktree by hand; a
  row's path could not be read, so do not run git worktree prune, git
  worktree remove or git gc until it can" (152 characters; the finding's
  message 182). Design: one message-table row; it carries no gate, so no
  cut. Until then: "restore or prune the main worktree by hand".

### Chosen by his word of 2026-10-23T12:19:11Z (C-72)

O3, O5 and O8 are built once A1's re-alignment lands; O9 (A) and O10 (A) keep
A1's text as ratified; O11's part 1 is built now and its part 2 (A) once the
re-alignment lands.

- **O3. Item 7, the identity re-read in `estimated`** (FR-020; EC-032).
  Take: +3 per Git candidate whose identity probe prints other than two
  lines; leave (as ratified): no term. CHOSEN: take.
  Design: one term in R14's sum; `performed` counts the re-reads either
  way, and A1 design D3's "adds no child" is reworded either way (text
  only).
- **O5. Item 9, the work-tree probe's output** (FR-007; LQ-11). As
  ratified: output that is not exactly one line disagrees; PR #19's round
  (j): the output less its final line feed is one path. CHOSEN: round
  (j)'s reading. Design: one decider
  `work_tree_output()`; a linked worktree whose path holds a line feed, in
  a repository whose extension is true, is the test either way.
- **O8. T7's locked form**. "A locked stale worktree: should the
  overview's message be (A) `project clean`'s locked text, 'Review, unlock
  it, then prune stale worktree metadata manually.', with the same
  warning, or (B) the one stale text for every stale row, as A1 is
  ratified?" CHOSEN: (A). The text is feature 004's
  (lane openRepoProject-3's W52 F-10; `TEXT`, `:877`); round (n) states T7
  as the report row's recommendation alone, since #19's preview excludes a
  locked stale row as `locked-worktree` (`#19 design.md:1513-1568`), and
  the overview's finding is that row's text. Under (A), with O6's warning,
  it is 173 characters, and beside the report-cap remedy clause 1 keeps 9
  of its 62-character recommendation. Design: one message-table row keyed on
  `locked`. Without an unread row, the locked form takes Q3 (b)'s warning
  whole by O18 (A), chosen, 318 characters, as feature 004's `TEXT` carries
  it at `41759a4`, in place of the 63-character form that its `TEXT` carries
  at `d6bac50` and `d8724e2`; both land with A1's re-alignment, so that the
  63-character form is not built alone (R1; R12; O18, below).
- **O9. M1, parity when the working directory's realpath fails** (FR-026;
  C-61). "When the working directory's realpath cannot be read, the
  overview marks only merged rows `inspection-error`, but `project clean`
  marks every present row so. Should (A) the overview keep its ratified
  rule and the parity tests leave this case out, (B) feature 004 follow
  the overview, or (C) the overview follow feature 004 (an amendment of
  change 2)?" CHOSEN: (A). Design: (A) none beyond the ratified rule's own
  step, which R5 builds (a merged row `inspection-error`, with no row
  error), the parity tests naming the case (R18); (B) none in the overview,
  and the case returns to the parity tests; (C) that step widened to every
  present row.
- **O10. LQ-15's extension** (FR-043; EC-036). "You ratified
  `relative-config-path` with exit 2 in 'ratify 34'. One point stays open
  with #19: lane 2's extension of the test to `GIT_CONFIG_GLOBAL` and
  `GIT_CONFIG_SYSTEM`. Keep it (A), or strike it (B), in which case the
  overview drops those two names with `project clean`?" CHOSEN: (A),
  keep, so the code, its exit and the two names all stand. Design: none in
  the overview, which calls
  `relative_config_paths` (`:977`); under (B) feature 004's
  `CONFIG_PATH_EXTENSION` (`:974`) loses them.
- **O11. The `core.worktree` read's exit 1** (FR-007, FR-008, EC-012, User
  Story 8 and the discovery-identity checklist's CHK009, as C-72 lists them; A1
  design D3, case 3; R9), on a lane finding: lane openRepoProject-3's W100
  LOW-A, through the lead's R-336, which gives PR #19's row 4b, the same key's
  read, "an exit 1 with nothing printed is the key unset, and any other
  failure, an exit 1 that printed anything included, makes the main worktree
  unreadable, so the run is refused `target-not-repository-root`" (`#19
  design.md:555-559` at `54e869b`). In ratified A1 the requirement (A1:130-135)
  and the
  scenario "A separate git directory" (A1:172-175) read an unset
  `core.worktree` as no value, the root falling through to the candidate's
  toplevel, while the failure table (A1:369) excepts only the extension read's
  exit 1 and the effective-work-tree read, so that the unset key's exit 1 is
  `probe-failed` if read literally. Part 1: should the failure table except the
  unset key's exit 1, nothing printed on either stream, as #19's row 4b and
  A1's own D3 read it? (A) yes, a text re-alignment, A1's held item 11, part 1;
  (B) no. Part 2: for any other failure of that read, the table's
  `probe-failed` kept and `repository.root` null, should the withheld
  suggestions carry `target-not-repository-root`, as
  #19 refuses the run? (A) yes; (B) no gate code. CHOSEN: (A) for both.
  Design: one decider, `core_worktree_value()`, and one exception
  row. Part 1 is built now, as the plan's reading of a conflict in ratified
  text (R9), since only so does the scenario's own test pass. Under part 1 (B)
  the decider would make the unset key's exit 1 `probe-failed` and, by the rule
  that a failed read names no root, leave the root null with no suggestion, so
  A1's scenario "A separate git directory" and spec 005's User Story 8 scenario
  1 would fail on Git 2.43; (B) therefore costs more than that decider and its
  tests: an amendment of change 2 re-wording that scenario and FR-008's
  sentence on the unset key, or else a different rule for a failed read. Part 2
  (A), chosen, is built once A1's re-alignment lands, the ratified behaviour
  standing until then: `probe-failed`, the root null, no suggestion and no gate
  code. Under part 2 (A), every finding that would
  suggest a clean command gets `suggested_command: null` with `suggestion_gate:
  target-not-repository-root`, as A1 design D3 does for a bare repository, and
  a row of its own in requirement 7's table, for a gitfile checkout whose
  `core.worktree` read failed, with the remedy "core.worktree could not be
  read; repair the repository's config, then run again" (79 characters), in
  place of the bare row's "run project clean from the main worktree root",
  which names a run that `project clean` refuses there, as item 8's
  sub-item (d) found of it (lane openRepoProject-3's W86 N10-2; the draft
  at `558b0c29`, :2702-2715, the row at :2739); a cut read decides as a
  failed one under both.

### Chosen by his word of 2026-10-23T13:30:30Z (C-72)

The five items that the review of the plan at `39f4ab6` raised, each as the
lane recommended it; revision 9 gives their designs.

- **O12. A failed ref listing** (FR-026). CHOSEN (A): A1's null class
  stands, and the parity tests name the case as a lasting difference.
  Built now; it keeps A1's behaviour. Design: none in the classifier; the
  parity tests name the case beside feature 004's class (R18; R5).
- **O13. Where the `core.worktree` read runs** (FR-006, FR-009, User Story
  8). CHOSEN (A): in the shared git directory, a rewording of A1's design D3,
  case 3, built once A1's re-alignment lands; until then the read runs in the
  candidate, as A1 is ratified, the defect recorded. Design: the
  `core-worktree` child's `-C` directory, the common directory in place of
  the candidate; the defect, and the two routes of a relative value naming
  a missing directory, are in R9.
- **O14. A submodule reached only through a linked worktree of its module
  directory** (User Story 8, EC-012). CHOSEN (A): a known limit, with no
  detection. Built now; it keeps A1's behaviour. Design: none; the limit is
  recorded in R9.
- **O15. A remedy whose escaped repository parent is 177 characters or more**
  (FR-035). CHOSEN (A): the remedy is kept whole and the finding's own text
  cut to `...`, the message passing 200 characters in that case only. Built
  now, ahead of A1's text. Design: the composer's floor, max(n - 3, 0)
  characters of the own text (R12); its rows are in "Lengths" below and R18.
- **O16. A bare repository's main row** (C-40, C-68, FR-008). CHOSEN (a):
  `branch`, `head` and `merged_into_target` are null for that row. Built now,
  ahead of A1's text. Design: the row takes only its `lstat` (R5); the data
  model's worktree row and the contract's JSON say so.

### Chosen by his word of 2026-10-23T21:10:35Z (C-72)

The five items that #19's round (q) at `818311a` raised, O17 to O20, and that
feature 004's `41759a4` raised, O21, each as the lane recommended it, (A).
O19 (A) and O20 (A) are built now, ahead of A1's text; O21 (A) now, as A1 is
ratified; and O17 (A) and O18 (A) once A1's re-alignment lands, which carries
O17 to O20's texts and O21's record (C-72), A1 as ratified standing until
then. Feature 004's head `904aefc` confines O19's two cases to `project clean`'s
plan, `project clean` alone excluding them there, and leaves its merged-set
block unchanged (lane openRepoProject-2's reports to lane 4 of 2026-10-23, its
R-416 and R-424): O19's outcome for such a row and O21's case are stated below
(C-72).

- **O17. Q5's next steps for the two reflog gates** (FR-035, User Story 4).
  CHOSEN (A): #19's wording of the `unstarted-branch` and `reflog-unavailable`
  next steps, 248 and 243 characters (`#19 design.md:1419-1425` at `54e869b`;
  feature 004's `NEXT_STEPS` at `41759a4` and `904aefc`, R1), is kept whole, in
  place of the
  wording O1 (A) quoted (#19's at `3dcd2d8`, 136 and 131), the finding's own
  text cut to `...` and the message passing 200 characters, at 253 and 248, as
  for O15 (A)'s `--root` remedy. Built once A1's re-alignment lands; until
  then A1's ratified remedies, 102 and 97 characters, which US4 s5 and s6
  quote. Design: the two remedy rows, and O15 (A)'s floor in the composer
  (R12), which these two remedies also reach, since 200 - 2 - 248 and
  200 - 2 - 243 leave the own text no character.
- **O18. Q3 (b)'s warning on the stale text** (FR-028, FR-026). CHOSEN (A):
  without an unread row, the overview's stale message is `project clean`'s,
  [L]'s plain form, 305 characters, or for a locked row its locked form, 318
  (PCL:216-225 at `54e869b`; feature 004's `TEXT` at `41759a4`, R1), kept
  whole past 200 characters, in place of [L]'s 50-character text and O8 (A)'s
  63-character locked form; where a gate's remedy follows it, the remedy is
  kept whole too, as D5 keeps every remedy, up to 459 and 472 characters
  beside the redirect remedy (152), the warning not cut. The forms beside an
  unread row (O6 (A), O8 (A)) are unchanged, with the composer's clauses 1
  and 2. Built once A1's re-alignment lands; until then A1's one stale text
  for every stale row. Design: the two message-table rows, plain and keyed on
  `locked`, and one branch of the composer that cuts neither the text nor
  the remedy (R12).
- **O19. The wider `registration-mismatch`** (FR-032, SC-004). CHOSEN (A):
  #19's round (q) widens the class to a worktree whose path is the common
  directory, the main worktree or another row's path, or an ancestor of one,
  and to one whose registered path is a symbolic link
  (`specs/project-clean-review-safety/spec.md:13-17` at `54e869b`); the
  overview evaluates both cases from its own evidence, the paths of the rows
  the listing gives and FR-007's no-follow `lstat`, with no new Git child, as
  `project clean`'s classification, and SC-004 takes no new exclusion. Built
  now, ahead of A1's text. Design: one decider over those inputs (R9; the
  data model's "Gates"). At feature 004's `904aefc`, whose `project` is that of
  `d640539` and which confines both cases to `project clean`'s plan, `project
  clean` gives a linked row in either case `inspection-error`, unprobed, its
  `dirty` null, excluded at the `registration-mismatch` gate, and the main
  worktree's row, where a linked row shares its path, `inspection-error` too, at
  the `main-worktree` gate, while a row that such a row holds is read and
  classified as before (C-72; lane openRepoProject-2's reports to lane 4 of
  2026-10-23, its R-416 and R-424). The overview's class follows it (FR-026),
  `inspection-error`, so that the gate decides no `merged-removable` row, FR-034
  withholds `--all-safe` for the repository as `inspection-incomplete` and
  SC-004 takes no new exclusion; a row that shares its realpath with another is
  FR-007's disagreement already (EC-031). R18 names the two cases' fixtures with
  these results; the one point left open is O23 (below).
- **O20. The fifth status pin** (FR-016). CHOSEN (A): `-c
  core.ignoreCase=false`, which #19 adds to every status probe (PCM:158-162 at
  `4512441`), is taken with feature 004's `STATUS_PINS`, five at `41759a4`,
  by FR-016's own rule, A1's re-alignment adding it to its requirement 3 and
  design D13. Built now, ahead of A1's text. Design: none beyond the reuse
  by reference (R3): the status probe takes `GIT_KINDS["status"]`'s pins, and
  the wrapper asserts them by reference (R18).
- **O21. A failed merged-set listing** (FR-026, SC-003). CHOSEN (A): a
  repository whose merged-set listing fails, its ref listing read, where A1
  leaves every worktree row's class null (A1:434-437) while `project clean`
  at `41759a4` makes each present row on a branch `inspection-error` (C-72):
  A1's null class stands. Built now; it keeps A1's behaviour. Design: none in
  the classifier, a failed merged set leaving every class null (the data model's
  `classification`). At feature 004's `904aefc` (`project:3717-3724` and
  `:3760-3761`) the block stands: each present row on a branch, the main
  worktree's included, is `inspection-error`, a detached row keeps the class the
  ladder gives it and a row whose path is missing is `stale-worktree`
  (`:2488-2489`), where A1's null class leaves each of them null, a row that
  FR-007 sets to `inspection-error` directly apart; the parity tests name those
  rows as the lasting difference of O21's case, beside O12's and O9's (R18;
  C-72).

### Open, before Brett Heap (C-72)

Two items that #19's round (s) at `dab8a64` (O22) and feature 004's `904aefc`
(O23) raised, which C-72 records for his word with the lane's recommendation:
O22 was put to him at 2026-10-23T22:39:41Z, O23 is recorded at spec commit 3au.
Until he rules, the plan builds A1 as ratified for both, each in its own place,
and the contract marks each OPEN where its text would change.

- **O22. The main worktree's recommendation** (FR-028). OPEN. #19's round (s)
  (R-408; PCL:207-214 at `54e869b`) gives the main worktree's row, where the
  ladder classes it `merged-removable` or `merged-current`, one whose upstream
  was deleted included, "The main worktree is never removed by project clean."
  in place of its class's text, the class unchanged; the overview's message for
  a classified row is the ladder's recommendation (FR-028), so that a
  `merged-removable` main row already shows those words through the
  `main-worktree` gate's finding (FR-032) and a `merged-current` main row shows
  the baseline's "The branch is merged, but this is the current checkout; switch
  away before removal." (A) follow round (s) now, the main row carrying #19's
  text for both classes, ahead of A1's text, A1's re-alignment narrowing its
  sentence on a merged row whose upstream was deleted, as #19 narrows its own;
  (B) keep the class's baseline message for the main row until A1's re-alignment
  carries the change, the difference from `project clean` recorded. Recommended
  (A). Until he rules the plan builds (B)'s reading, A1 as ratified (FR-028);
  feature 004's `row_evidence` already gives the main row that text
  (`project:3335` at `d6bac50`, `:3510` at `904aefc`), so that the overview's
  `merged-current` main row differs from `project clean`'s output today as well
  as from round (s). Design if chosen: one message-table row for a row with the
  `main` flag, beside the class's two findings (R12).
- **O23. A row in O19's cases: status probe and finding** (FR-007, FR-032).
  OPEN. FR-007's registration cases do not name a linked row whose path is the
  common directory or an ancestor of it, of the main worktree or of another
  row's path, or whose registered path is a symbolic link, though they name a
  row that shares its realpath with another (EC-031). Read as written, such a
  row whose registration agrees takes FR-007's last case, one status probe, its
  `dirty` read, its class `inspection-error` by FR-026's parity, with that
  class's finding, where `project clean` leaves the row unprobed, its `dirty`
  null, and excludes it as `registration-mismatch`. (A) read such a row as
  FR-007's disagreement case, no status probe, `inspection-error` set directly,
  a `registration-mismatch` finding in place of the class's `inspection-error`
  finding and no error, A1's re-alignment carrying it with O19 (A); (B) keep
  FR-007's last case for it, the difference from `project clean` recorded.
  Recommended (A), which keeps `dirty` as `project clean` reports it, needs no
  Git child for such a row and names the gate that excludes it. Until he rules
  the plan builds (B)'s reading, FR-007 as ratified. Design if chosen: the O19
  decider's verdict joins the twin decision, made before the repository's first
  status probe, so that such a row takes neither the work-tree probe, the
  re-verification nor the status probe (R5), and `estimated` leaves out their
  probes (R14).

### Lengths

Measured by `lengths3.py`, a script outside this repository, over the
strings as the contract quotes them, each warning checked against PR #19's text
at `2250830` (unchanged at `88d0d36` and `e0b1671`, and in its unread forms at
`818311a`, `4512441` and `54e869b`, and equal to feature 004's `TEXT` at
`d6bac50`) after its whitespace was normalised. D5's cut to n
characters keeps n - 3 and adds `...`; clause 1 cuts the recommendation to
what 200 leaves beside the warning and the remedy; clause 2 cuts the
remedy to what 200 leaves beside the warning. "Old" is the warning before
round (n), "so do not run git worktree prune until it can". No figure rests
on that script: the composer's tests compute each from the contract's
strings and hard-code only these final lengths (R18), and the triage's
recount (TC) and lane openRepoProject-3's W132 reproduce them.

- The warning alone, with its period: 78 -> 109.
- T6, the stale text with the warning (O6): 129 -> 160.
- T7's locked form with the warning (O8 (A)): 173. Beside the bare
  repository's remedy, uncut 220; under clause 1 (200) the recommendation
  keeps 39 of its 62: "Review, unlock it, then prune stale wor...; a row's
  path could not be read, so do not run git worktree prune, git worktree
  remove or git gc until it can.; run project clean from the main worktree
  root". Beside the path-bytes remedy, uncut 205; under clause 1 (200) it
  keeps 54: "Review, unlock it, then prune stale worktree metadata ...; a
  row's path could not be read, so do not run git worktree prune, git
  worktree remove or git gc until it can.; rename the path to valid UTF-8".
  Beside the redirect remedy, uncut 327, clause 2 gives T6's message, the
  recommendation being left out; beside the report-cap remedy at 260 rows,
  250, keeping 9; beside O11's, 254, keeping 5.
- O7's remedy: 121 -> 152; its finding's message: 182.
- T6 beside the report-cap remedy at 260 rows, uncut: 206 -> 237. Under
  D5's rule alone (200): "Review and prune stale worktree metadata
  manually; a row's path could not be read, so do not run git worktree
  prune, git...; 260 rows exceed the report's row cap of 256; the report
  would be incomplete".
- The same under clause 1, 200 -> 200, the recommendation 40 -> 9: "Review
  an...; a row's path could not be read, so do not run git worktree
  prune, git worktree remove or git gc until it can.; 260 rows exceed the
  report's row cap of 256; the report would be incomplete".
- T6 beside the bare repository's remedy, uncut: 176 (whole) -> 207. Under
  D5's rule alone (200): "Review and prune stale worktree metadata
  manually; a row's path could not be read, so do not run git worktree
  prune, git worktree remove or git gc unt...; run project clean from the
  main worktree root". Under clause 1 (200): "Review and prune stale
  worktree metadat...; a row's path could not be read, so do not run git
  worktree prune, git worktree remove or git gc until it can.; run project
  clean from the main worktree root".
- T6 beside the path-bytes remedy: 161 -> 192, whole.
- The warning beside the redirect remedy (O4's clause 2), uncut: 232 ->
  263 (T6 beside it: 314). Under clause 2 (200): the message quoted in O4,
  the remedy keeping 86 of its 152 characters (117 before round (n)).
  Under D5's rule alone (200, either way): "Review and prune stale
  worktree metadata ma...; core.worktree or core.bare redirects the main
  worktree; unset both in the repository's config, or in the main
  worktree's config.worktree, then run again". Beside the redirect remedy
  every gated own text that can reach it, with no warning, keeps 43
  characters and `...`, the message exactly 200: the stale plain text (50,
  until O18 (A) lands, below), `dirty` (54), `ignored-local-files` (56),
  `detached` (75), `unpublished` (67), `remote-gone` (68), `review-required`
  (87 and 77), `diverged` (77),
  `unpushed` (76), `locked-worktree` (70) and `merged-removable` (67).
- O1 (A), unchanged by round (n): the merged worktree's text beside
  `unstarted-branch`, 200 with the own text cut to 59 of 67 ("This clean,
  merged, non-current worktree may be removed exp..."); beside
  `reflog-unavailable`, 200, uncut. These are the figures of the wording O1
  (A) quoted, which O17 (A)'s rows below replace, both landing together.
- O11 part 2 (A)'s remedy, "core.worktree could not be read; repair the
  repository's config, then run again": 79 characters. Beside the 17 ladder
  recommendations of feature 004's `RECOMMENDATIONS` and
  `SECOND_RECOMMENDATIONS` (`:2342-2362`, 50 to 87 characters; the
  `protected-default` one gives no overview finding), 131 to 168, each whole.
  Beside T6, uncut: 241. Under D5's rule alone (200): "Review and prune stale
  worktree metadata manually; a row's path could not be read, so do not run git
  worktree prune,...; core.worktree could not be read; repair the repository's
  config, then run again". Under clause 1 (200), the recommendation keeping 5
  characters: "Revie...; a row's path could not be read, so do not run git
  worktree prune, git worktree remove or git gc until it can.; core.worktree
  could not be read; repair the repository's config, then run again". T7 beside
  it under clause 1 gives the same message. Clause 1 keeps some of the
  recommendation beside any remedy of at most 83 characters; every remedy that
  can reach a `stale-worktree` finding is within that (the longest, this one,
  79; the report-cap one 77 from 10,000 rows) but item 8's redirect remedy
  (152), which clause 2 takes.
- `merged-removable` (67) over both inspect caps (C-14; the contract's
  "Human report" and "Remedies"), at 260 rows: beside the batch remedy,
  130, and beside the report remedy, 144, both whole.
- O15 (A), built now, ahead of A1's text: `merged-removable` beside `re-run
  with --root <repository parent>`, 19 characters plus the escaped parent:
  whole to a parent of 112 characters (200), cut from 113, the own text
  `...` alone at 176 (200), and from 177 `...; ` and the remedy whole, past
  200: 201 at 177, 279 at 255 and 4,120 at 4,096. Computed from the
  contract's strings by D5's rule with O15's floor; the triage's recount (TC)
  agrees at 10, 150, 176 and 177.
- O17 (A), once A1's re-alignment lands: #19's Q5 next steps, 248 and 243
  characters, kept whole; beside them the merged worktree's own text keeps
  nothing but `...`, the message `...; ` and the remedy, 253 and 248, past
  200 (O15 (A)'s floor). Until then A1's ratified remedies, 102 and 97, give
  171 and 166, uncut.
- O18 (A), once A1's re-alignment lands: the stale text with Q3 (b)'s
  warning, 305 alone, and its locked form, 318, each kept whole; a gate's
  remedy after either kept whole too, up to 459 and 472 beside the redirect
  remedy (152). Until then A1's one stale text, 50, with D5's rule.

- **Recorded, no design impact**: F-1's (b) beside an unread row, RULED in PR
  #19's round (p) on 2026-10-23, "Yes, warn (Recommended)" (R-365), and
  superseded by his Q3 (a) of the same day, which names the target's own
  administrative directory and no prune in every mode (R-380; the record at
  `#19 design.md:2512-2530` at `54e869b`), `project clean`'s partial-removal
  text, reaches no overview text in either form, since A1 mirrors none of F-1's
  texts and the overview never shows it (C-59); T8, clean's always-on cap
  warning, now "if a worktree's path cannot be read, do not run git worktree
  prune, git worktree remove or git gc until it can", with Q3 (b)'s warning
  after it since round (q) (`#19 design.md:1682-1695` at `54e869b`), reaches no
  A1 site, since the overview's two `inspect-cap` remedies are its own and name
  no prune; T9 (R-365), `project status --json`'s stale recommendation beside
  an unread row, "Review the stale worktree metadata before pruning it
  manually; a row's path could not be read, so do not run git worktree prune,
  git worktree remove or git gc until it can." (172 characters; feature 004's
  `project:7212-7213` at `d8724e2`, `:7464-7465` at `41759a4`, and `#19
  design.md:1721-1740` at `54e869b`, which PCM:299-309 states since round (q)),
  reaches no overview text either, the overview's stale message being [L]'s
  `stale-worktree` text (O6, O8), so no length here depends on it; and FR-051
  applies only if he accepts feature 004's T123 departure, else the sentence
  moves to a separate small change.

## Revision 2: lane openRepoProject-3's W96 read

W96 read this plan at `a80f10b` and, in a delta read, revision 1 at
`aeb0bb2`. Revision 2, made from `7af798a` (spec commit 3ae), takes each
finding, every one checked against the text it cites:

- **HIGH-1**, a second merge-target resolver against A1's Non-Goal (A1
  design.md:73-74): change 1's `resolve_merge_target` (`:2517-2557`) is
  pure, its caller reading the manifest (`:3206-3208`), so the overview
  calls it (R3, "The merge target, by change 1's resolver"; the data
  model's `merge_target`; the contract's two findings; traceability's
  FR-024 and FR-025; plan.md's slice 4 and Post-design). No departure is
  left to declare.
- **MEDIUM-1**, the plan word where the order is stated: the spec's text,
  which commit 3ae records in C-56 and its Status; R1's finding and
  plan.md's Authority say so.
- **LOW-1**: R4 names the five places A1 says one self-pipe and gives the
  record line for the spec or the A1 draft.
- **LOW-2**: R5 picks one for D3 item 3's unnamed-gitfile root: the
  manifest read, ref listing and merged set wait with phase 2.
- **LOW-3**: R8 and the data model's `remote_copy` carry D9's origin/HEAD
  sentence.
- **LOW-4**: R10 canonicalises the home rule's strings in the root task,
  and R3 lists `projects_dirs` as not reused.
- **LOW-5 and LOW-7**: the data model's marker line and R10 cite DI:142
  for `ENOTDIR`; FR-005's wording is the spec's to change.
- **LOW-6**: R9's extension read is rewritten, with no held item; the
  PENDING mark goes from R9 and from plan.md's Risks.
- **LOW-8 and LOW-9**: R7's re-verification task and R5's manifest place
  take W96's words for FR-013 and FR-021, which are the spec's to change.
- **LOW-10**: O2 quotes R-263, "O-1: deadline-exceeded".
- **LOW-11**: traceability.md gains "Slices", mapping regions and
  scenarios to plan.md's slices.
- **LOW-12**: R3 cites `:2566-2572` for "another driver".
- **LOW-13**: plan.md's Risks name the agent-context markers rightly.
- **GAP-3b with D-LOW-1, and D-LOW-2**: gate (b) compares `clean`'s
  output, JSON and human, standard output and standard error byte for
  byte, and gate (d) diffs every subcommand's help (R3, plan.md's Gates,
  quickstart.md, traceability.md). **GAP-3c and GAP-3e** were fixed in
  revision 1.
- **Section 4's rewordings**: O1, O2, O4 and O6 to O10 take them, O6 in
  section 7's corrected form (R20). One departure, in wording only: O4's
  ratified option carries no "(c)" label, since (c) names the draft's
  sub-item in the same question.
- **Section 7's currency** (the draft at `8ce4e9fb`): clause 2 moves to
  O4 with its (b) path, through sub-item (c)'s row, and O6 keeps clause 1
  (R12, R20, the contract's "Composer").
- **Also in revision 2, listed here in revision 3** (W96's R2-LOW-3): R3's
  `main()` sentence, which maps every `Exception` of an overview run inside
  its entry point and lets the `BaseException`s reach `main()`'s handlers
  (W96's part 3 note), and the contract's row
  `finding.unsupported-layout.redirect`, then held under O4 (b), whose
  text was the draft's option (b) message.

## Revision 3: Brett Heap's word, the re-pins and W96's delta read

Made from `4072608` (spec commit 3af), on the lead's message for revision
3 and its two additions. Each input, and where it is taken:

- **His word on O1 to O10** (C-72): R20 is retitled and split into five
  CHOSEN items and five OPEN, each open item with the lane's
  recommendation; each chosen item is built once A1's re-alignment lands
  at PR #34, the ratified text standing until then, and stays isolated.
  It is carried through plan.md's Summary and open questions, the
  contract's marked rows (O4 (b)'s row dropped, (a) being chosen), the
  data model's gate note, quickstart.md and traceability.md.
- **The re-pins** (R1): feature 004 at `211e43d`, from `0a82a62`, its 44
  moved cites moved by a line map and every reused definition unchanged
  but in its line, `config_key_unset` new and reused, 491 test methods;
  PR #19 at `2250830`, round (n), from `20084cd`, with round (o) at
  `88d0d36` named as a later head that changes no spec text (R1, R20);
  and PR #27 at `dafe476`, its round B22, from `04be7f6`.
- **R-324's words and every length**: the contract's stale, locked and
  `main-worktree-missing` texts are copied from `2250830`, and R20's length
  table is measured again, each message in full (R12, R20).
- **W96's delta read at `6fb619c`**: R2-LOW-1 in R3 (the raw
  `tracking_branch`, `:3207`; a value that is not a string ignored at
  `:2537`); R2-LOW-2 in O4 (sub-items (c) and (d) apply under (a), with no
  question of their own); R2-LOW-3 in the Revision 2 record above; and its
  plan-side PARTIAL notes: LOW-1 (R4 cites the spec's Dependencies), LOW-7
  (R10 cites FR-005), LOW-8 and LOW-9 (R7 and R5 cite FR-013 and FR-021),
  and part 3's `EOFError` (R3).
- **The spec's words at `4072608`**, cited where the plan said the spec
  would change: FR-005's `ENOTDIR` (R10), FR-013's re-verification task
  (R7), FR-021's manifest place (R5) and the Dependencies' two read ends
  (R4).
- **O11**, the `core.worktree` read's exit 1, which the A1 drafter found
  and the lead confirmed at `e4a30fc`: R9 and R20; part 1 is built now, as
  the plan's reading of a conflict in ratified text (the data model's
  exceptions, the contract's Git children), and part 2 is held; its tests
  are in R18.
- **Feature 004's row 4c** now reads an exit 1 as #19's D7 does (R-332 at
  `211e43d`), so the overview's extension read calls `config_key_unset`,
  and the one difference left is A1's row error (R9).
- **Also in revision 3, listed here in revision 4** (W96's R3-LOW-3): the
  A1 draft's move, items 8 and 10 and the row 4b section read at
  `811b9cef` (2,584 lines) where revision 2 read `8ce4e9fb` (2,422 lines),
  in R20 and in plan.md's Citations; and the contract's `error.probe-failed`
  entry, which gained its three cases that record no error, the third
  being O11's part 1, an O11 site beside the data model's exceptions and
  the contract's Git children.

## Revision 4: W96's read of revision 3, the ordering sentence, the re-pins

Made from `7b37557` (spec commit 3ag), on the lead's message for revision
4. Each input, and where it is taken:

- **R3-MED-1, D5's clause 2** (lane openRepoProject-3's W96 at `664461f`):
  R20's opening and O4 now say that clause 2 is chosen only through O6's
  recommended text at `7af798a` (research.md:789-792 there), that it reverses
  ratified D5's "remedy kept whole" for that one case, and that it is before
  Brett Heap for his direct word (W105's OBS-1), resting on that text until he
  answers, as C-72 at `7b37557` words it; R12 (its clause 2 sentence),
  plan.md's Summary and its list, the contract's composer and traceability.md's
  FR-031 to FR-035 line say the same (the last two sites added to this record
  in revision 5, W96's R4-LOW-2).
- **R3-LOW-1**: R9 cites spec 005's own conflict at `7b37557`, its "two
  exceptions" (spec.md:4060, :4961) against FR-008's gitfile sentences
  (:2424-2431, :2433-2439) and User Story 8's scenario 1 (:1569-1578), and
  records the plan's reading of that scenario's first case as no error, by
  contrast with its second (W96's OBS).
- **R3-LOW-2**: R20's O11 states what part 1 (B) builds and its cost, a
  scenario that fails and a re-wording of change 2; plan.md's sentence on
  isolation names that one exception.
- **R3-LOW-3**: the "Revision 3" record above.
- **W96's OBS on the pane**: R20 says O3 and O8 to O10 were put to him in
  lane 4's pane, and O5 is recorded by the lane's NOTED correction.
- **The ordering sentence** (lane openRepoProject-3's W105 MED-A): R20 and
  plan.md follow C-72 at `7b37557`: A1's ordering rule (A1
  `proposal.md`:1278-1284) is the four LQ items' and reaches O5 and O10;
  items 2, 6, 7, 8, 10 and 11 rest on his word for change 2 and reach PR
  #34 in the same re-alignment commit, after #19's ratification and his
  review of the final text.
- **The re-pins** (R1): feature 004 at `d6bac50`, from `211e43d`, only
  `TEXT` changing, 138 cite occurrences moved by a line map and three
  placed by content (T8 `:806-809`, T6 and T7 `:887-892`, now in R-324's
  words), and R1's sentence on the old warning reworded; PR #19 at
  `88d0d36`, round (o), from `2250830`, every design cite after its line 76
  moved by 2 and checked by content, and "the next revision re-pins at
  #19's ratified head" replaced by that pin; PR #27 stays at `dafe476`.
- **The A1 draft at `c5840a66`** (2,888 lines), cited wherever revision 3
  cited `811b9cef`: item 11 drafted, part 1 for the lane-findings list and
  part 2 for his word, with (A)'s design delta in O11 (requirement 7's
  bare row and its remedy, the drafter's choice); item 9 OPEN (O5); and
  item 8's clause 2 marked as taken through O6's text, his direct
  confirmation asked.

## Revision 5: W96's read of revision 4, O11 (A)'s own remedy row, #27

Made from `54dc025` (spec commit 3ah), on the lead's message for revision
5 and its addition. Each input, and where it is taken:

- **R4-LOW-1, the ordering sentence** (lane openRepoProject-3's W96 at
  `06b16e1`, W105's LOW-1): R20 and plan.md's Summary take C-72 at `54dc025` in
  substance, five places differing in form only (W96's OBS at `464c361`;
  revision 6 makes both copies identical to C-72 at `98b95db`): "the open O3
  and O8 (items 7 and 10), O11's part 2 (item 11) and, should he take (C), O9
  wait on his word for change 2 too, and O11's part 1 is a text re-alignment on
  a lane finding for his review"; R20 cites C-72's O11 split at `54dc025`
  (spec.md:971-974 and :979-982).
- **R4-LOW-2**: the draft is cited at `558b0c29` (2,928 lines) for every
  item, as the source of options only, in plan.md's Citations and R20,
  which also name its earlier reads; and the Revision 4 bullet for R3-MED-1
  now names R12 and traceability.md.
- **W96's OBS**: the contract's composer and R12 now open with "Two
  clauses, the second before him for his direct word".
- **O11 part 2 (A)'s own remedy row** (lane openRepoProject-3's W86 N10-2;
  the draft at `558b0c29`, :2702-2715, the row at :2739, placed at
  :2732-2733): `target-not-repository-root` for a gitfile checkout whose
  `core.worktree` read failed, with "core.worktree could not be read;
  repair the repository's config, then run again" (79 characters), in
  place of the bare row's remedy, which names a run that `project clean`
  refuses there. It replaces that remedy where the plan quoted or named it
  (the contract's `core-worktree` child, R20's O11, the data model's gate
  note and plan.md's list), and it is an OPEN entry of its own under
  `remedy.target-not-repository-root` in the contract; the plan builds (B)
  until his word. R20's "Lengths" adds its rows, measured by the same
  script with the 17 ladder recommendations: 131 to 168 beside them, whole;
  241 beside T6, cut, "Revie..." under clause 1; no remedy that reaches a
  `stale-worktree` finding passes 83 characters but the redirect, which
  clause 2 takes.
- **PR #27 at `288fc34`**, its round B23, from `dafe476` (R1): its eight
  ranges and specs byte-identical by the lead's `cmp`, its block blob
  `a40458cb` unchanged.

## Revision 6: W96's read of revision 5, and C-72 at 98b95db

Made from `98b95db` (spec commit 3ai), on the lead's message for revision
6, a wording revision. Each input, and where it is taken:

- **R5-LOW-1** (lane openRepoProject-3's W96 at `464c361`): R20's opening
  now quotes C-72 at `98b95db` (spec.md:966-985) as it stands, so its
  attribution reads "lane openRepoProject-3 asked, on W105's OBS-1, that he
  confirm it directly", and its wording pin is `98b95db`, not `7b37557`.
- **W96's OBS, "word for word"**: the Revision 5 record now says "in
  substance"; R20's quote is identical to C-72's text (checked by a script,
  whitespace normalised), and plan.md's Summary quotes C-72's ordering
  sentence from `98b95db` (spec.md:977-985) whole, in place of its short
  form.
- **W105's plan-side point** (its read of 3ah): R20's "W105 asked" and its
  "O3, O8 and O11 rest on his word" now read as C-72 does, through the
  quote: O3, O8, O11's part 2 and, should he take (C), O9 "wait on his word
  for change 2 too", and O11's part 1 is a text re-alignment on a lane
  finding for his review.
- **C-72 at `98b95db`**: its definition of (C), "(the overview follows
  feature 004, the plan's R20 O9 (C))", and its O11 site list with EC-012
  and the discovery-identity checklist's CHK009 come in through the quote,
  and R20's O11 entry takes that site list.
- **Pins, unchanged**: feature 004 stays at `d6bac50`, its later head
  `f3724fc` named as documents only (R1; plan.md's Citations); PR #19 stays
  at `88d0d36` and PR #27 at `288fc34`.
- **Bookkeeping** (added in revision 7, on W112's R6-OBS-3): the spec pins in
  plan.md's Input and R1's Finding move to `98b95db`, from `54dc025` and
  `7b37557`; plan.md's Citations add W96's delta read at `464c361`; plan.md's
  Citations and the index at the head of this file count the revisions to 6.

## Revision 7: W112's read of revision 6

Made from `84513fd` (spec commit 3aj), on the lead's message for revision 7, a
small revision. Each input, and where it is taken:

- **R6-LOW-1** (lane openRepoProject-3's W112 at `d500312`): R20's lead-in to
  its quote of C-72 now reads "For D5's clause 2 and the rest", since the five
  CHOSEN items before it name D5's clause 2 case and the quote opens with that
  clause's own qualifier.
- **R6-OBS-2**: traceability.md's FR-007 line names O11 (part 1 built now, part
  2 open) beside O5, as R20's O11 entry and C-72 list FR-007 among O11's sites.
- **R6-OBS-3**: the Revision 6 record gains a "Bookkeeping" bullet for its four
  hunks that only its header and title declared, and this record has one of its
  own, so every hunk of each is declared.
- **R6-OBS-1, the spec side**: from its commit 3aj the spec no longer lists
  plan revisions by sha and points to these "Revision" sections instead (the
  lead's decision), so a plan revision calls for no spec commit. The plan's
  cites of the spec stay pinned by sha, at `98b95db`, and no plan revision
  needs to re-pin its spec cites.
- **Pins, unchanged**: feature 004 at `d6bac50`, its later head `f3724fc`
  documents only; PR #19 at `88d0d36` and PR #27 at `288fc34`.
- **Bookkeeping**: plan.md's Citations bullet on lane openRepoProject-3's reads
  names W96 and W112 as its readers and adds W112's delta read at `d500312`;
  plan.md's Citations and the index at the head of this file count the
  revisions to 7.

## Revision 8: every held item chosen, C-72 at 7f4ab94, the re-pins

Made from `7f4ab94` (spec commit 3al), on the lead's decisions for revision 8,
narrowed by the lead to the choices' marks and the pins; the design changes
that the nine-reader review of revision 7 at `39f4ab6` and its triage ask
follow in revision 9. Each input, and where it is taken:

- **His words of 2026-10-23** (C-72): "yes, recommended for O3, O5, O8-O11 and
  D5 clause 2" (12:19:11Z) and "yes, recommended for O12-O16" (13:30:30Z, in
  lane openRepoProject-3's pane). R20 is retitled, every item chosen, and
  quotes C-72 at `7f4ab94` (spec.md:954-1047) whole; O3, O5 and O8 to O11
  move from Open to Chosen, each with the time it is built; and O12 to O16
  have short entries. Every OPEN or "before him" mark becomes CHOSEN: R1's
  Decision, R9's two bullets, R12, R14 and R18 here; plan.md's Input,
  Authority, Summary and held-items list, which now quotes C-72's ordering
  sentence from `7f4ab94` (spec.md:998-1006); the contract's reading note
  and its O8, O10 and O11 rows and composer; the data model's gate note; and
  traceability.md's lines.
- **The spec pins**: plan.md's Input and R1's Finding move to `7f4ab94`, from
  `98b95db`; R9's cites of the spec move to `7f4ab94`, from `7b37557`.
- **PR #19 at `e0b1671`**, round (p), from `88d0d36` (R1's "Re-pin of
  revision 8, PR #19"; the research.md citations paragraph and plan.md's
  Citations), by the lead's cite map of #19 and its five rulings on the
  changed cites: R-343's sentence at `:1492-1499`, T9 a round (p) addition
  only; F-1's (b) RULED (`:2253-2265`), in the two earlier re-pin bullets
  and in R20's record; round (o)'s entry at `:73-79`; the claim that #19's
  specs are unchanged corrected for `specs/project-clean/spec.md` (plan.md's
  Citations, R1); and round (p) as the pinned head. The live cites move: R3's
  (e), R9's two, R20's O6, O8 and O11 and the contract's T7.
- **PR #27 at `d95eea2`**, its round B24, from `288fc34` (R1), its eight
  ranges byte-identical at their new lines by `cmp` against lane
  openRepoProject-5's line map, its block blob `a40458cb` unchanged.
- **Feature 004 at `d8724e2`**, named as a later head (R1; plan.md's
  Citations): only `TEXT`, `partial_removal_text`, `print_result` and
  `repo_state` change, `TEXT` gaining one row; the `project:N` cites stay at
  `d6bac50`.
- **Bookkeeping**: the index at the head of this file names Revision 1 and
  reads "Revisions 3 onward"; plan.md's Citations bullet on the reads of
  this plan reads "revisions 2 onward" and adds W112's read at `39f4ab6` and
  the nine-reader review; the Revision 3 and Revision 4 PR #19 bullets of R1
  carry the `e0b1671` lines of their changed cites.

## Revision 9: the review of revision 7, its triage, and W112's OBS

Made from `d0a7c07` (plan revision 8, on spec commit 3al, `7f4ab94`), on
the lead's decisions for revision 8, whose section 8 answers the first
writer's conflicts C1 to C5, and on revision 8's list of what it left. It
takes the FIX-PLAN items of the triage of the nine-reader review of
revision 7 at `39f4ab6` (its files TA, TB, TC and TD, by the reviewers'
IDs) and lane openRepoProject-3's W112 OBS, in three parts. The spec stays
at `7f4ab94` and PR #19 at `e0b1671`. Every chosen item is designed as
chosen and built when C-72 says (C1): O11's part 1, O15 (A) and O16 (a)
now, the rest once A1's re-alignment lands. Each input, and where it is
taken:

Part 1, the five HIGH items and the MEDIUM items that share their text:

- **R1-1**, `EvidenceError`: R3 lists it and the private readers that
  `verify_registration` reaches with `fs=_direct`, and no longer lists
  `_realpath` as not reused; R5 maps a row task's `EvidenceError` to the
  row's error, as `_read_row` does; R9 keeps the registration's realpaths
  non-strict; the data model's step result and filesystem task name it.
- **R1-6**, FR-026's step: R5 builds the ratified rule, a merged row
  `inspection-error` with no row error when the working directory's
  realpath failed (TB refuting the row error); the data model's
  `classification`; O9's design line.
- **R1-7**, the rows that take only their `lstat`: R5 and the data model's
  worktree row, a submodule checkout's main row added; with **O16 (a)**,
  built now (TC's R7-5), a bare row's `branch`, `head` and
  `merged_into_target` null in R5, the data model and the contract's JSON.
- **R2-1 (a)**, O4 (a)'s two tests: O4's design, the contract's
  `main-toplevel` child, the data model's `target-not-repository-root` row,
  marked CHOSEN, and R7's task. With it: **R2-1 (b)**'s plan half, O4's
  "Until then" in both layouts; **R2-3**, the main worktree candidate's own
  probe as the input and R6's fourth wait, marked CHOSEN; **R4-5**, the
  draft's words for item 8's term in R14 and O4; and **R7-6**, the data
  model's O4 (a) paragraph and root-null list and the contract's
  `probe-failed` entry.
- **R3-1**, the discovery barrier: R6's phase 1 starts once discovery has
  ended, and the data model's `listing` state; with **R3-3**, a cut root's
  snapshot in R7 and in that state.
- **R3-11 with R4-6** (the lead's C2 and C3): R7 gains the identity step's
  task, and its bound is a formula, R + 2,561, R the roots given, which
  nothing caps: 2,593 at 32 roots, 2,081 there without the
  re-verification, as R4-6 measured, and R + 2,689 with O4 (a)'s task. R4's
  Alternatives and plan.md's Risks drop "2,465" with it.
- **The draft's lines**: R6, R14 and O4 cite the draft at `558b0c29`, the
  plan's pin. The triage read it at `ea6b79d7`, which differs from
  `558b0c29` only at its lines 2667-2674 (`diff`), so its cites hold at
  both.

Part 2, the remaining MEDIUM items (TD's test items are in part 3):

- **The loop** (R4): **R3-2**, the deadline's answer to every held
  request, a collector stopping at its first, a terminating handle keeping
  its name, and the loop's end, with the data model's `collecting` state;
  **R3-4**, the task pipe made once per process and never closed; **R3-5**,
  descriptors unregistered before `close()` and every handle settled in the
  `finally`; **R3-8 with R1-11**, `signal_scope()` entered before the
  configuration-path test and read again after the raising span and after
  the scope (R15; the contract's step 1a).
- **The collectors** (R5): **R4-3**, the re-reads only after an exit 0
  without two non-empty lines, stopping at the first that fails (and the
  contract's `identity` child); **R4-4**, D3's order before the
  `core.worktree` read (and the contract's `core-worktree` child); **R4-2**'s
  R5 half, what runs after a failed repository-wide step (DI:539-543);
  **R3-7**, at most 16 filesystem tasks running per run, a cut task freeing
  its place, and `Thread.start()` inside the boundary; **R3-10**, the owner
  reading merged candidates' `.git` in canonical order.
- **R14**: **R4-1**, "registration-verified" read as the two-way check,
  twins excluded; **R4-2**, every uncut divergence listed; **R4-4**, the
  `core.worktree` term; and O3's term stated exactly, the trigger's
  refinement named as R4-3's, the option's words kept in R20 (decisions,
  section 2).
- **R3 and R15**: **R1-3**, the conflict finding's OTHER read from the kept
  `origin/HEAD` symref, the note's text never printed; **R1-4**, the split's
  return and call contracts, and two gate (b) fixtures in quickstart.md;
  **R1-9**, every string field from Git through [P]'s escaper (and the
  data model's `branch`, `upstream` and `merge_target`).
- **R9**: **R2-2 with R8-1**, a read value whose strict realpath fails, as
  a failed read is built (the data model's root-null list, the contract's
  `core-worktree` child, R18's two fixtures), with the lead's C5, the two
  routes as ratified and under O13 (A); **R2-4**'s defect, recorded for O13
  (A) (and the contract's CHOSEN row); **ASK-2**, O14's known limit.
- **R12, the contract and R20**: **R5-1** as O15 (A), built now, the
  composer's floor (the contract's composer and remedies, R18's rows,
  R20's Lengths); **R5-4**, the both-caps remedy (the contract's human
  report and remedies; R20's Lengths, 130 and 144); O12 to O16's designs.
- **R1-8 with O12 (A)**: R18's parity bullet and plan.md's Risks drop
  "until its R-101 (c) fix" (lane openRepoProject-3's W132 MEDIUM-1 too),
  naming feature 004's class beside A1's null one as a lasting difference;
  traceability.md's SC-003 names the O9 and O12 cases (decisions, section
  4).
- **R7-4**: the data model's "Null when" rows keep every case of the
  packet's column (DI:770-790).
- **LANE2-PINS**, but its R18 site, which goes with R6-2 in part 3:
  plan.md's Risks bullet, R3's `status_probe()` as mirrored, and the
  contract's `STATUS_PINS` and `STATUS_PROBE` by reference.

Part 3, the LOW items, TD's test items, W112's OBS, W132's LOW items and
the stale cites:

- **TA's LOW items**: **R2-5**, the `main-toplevel` output read as one path
  (O4 and the contract's child); **R2-6**, the main worktree as a spelling
  of the first record's directory (the data model's Repository); **R4-7**,
  A1's words for R14's gitfile term and the submodule row adding none;
  **R8-3**, R18's three identity fixtures; **R8-5**, R9's extension read
  without includes (its format-version clause left out here on the reading that
  the review's R8 shows only the includes, which its c6e refutes; revision 10's
  part 3 takes the clause); **S5-16**'s plan sites, the departure from DI:535
  in R9, the data model's exceptions and the contract (twice).
- **TB's LOW items**: **R1-2**, `probe_error` for two outcomes only (R3);
  **R1-5**, `refs` as list and map (the data model); **R1-10 with R6-11**,
  gate (d)'s three hunks at `COLUMNS=80` (R3 (d), quickstart.md, the
  contract's help note); **R1-12** and **R3-13**, R15's residual and write
  loop; **R1-13**, the `unreadable` null root (the data model); **R3-6**,
  the slot held from re-verification to status probe (R6) and the order
  that differs from feature 004 (R3, R9); **R3-12**, the expansion in the
  root task (R10); **R3-14**, the notice beside EC-015 (R16); **R3-15**,
  slow calls by the task table (R18's Time); **R3-17**, the main-worktree
  test before the registry (R5).
- **TC's LOW items**: **R5-2** and **R5-3**, R20's rows beside the redirect
  remedy and T7's rows (each recomputed from the contract's strings);
  **R5-5** (R12); **R5-6** (traceability.md and R18); **R5-7** (the
  composer's clause 1); **R5-9**, past-cap and cut rows in O6's trigger;
  **R7-1**, **R7-2**, **R7-3** (a "Project row" in the data model, at
  DI:743-758), **R7-7**, **R7-8**, **R7-10**, **R7-11**, **R7-12**,
  **R7-13** (the `deadline-exceeded` row and `refusal.relative-config-path`
  marked CHOSEN), **R7-15**, **R7-16**, **R7-17** and **R7-18**, in the
  data model and the contract; and **LANE2-T9**'s record line in R20,
  T9 at 172 characters (`project:7212-7213` at `d8724e2`; the lead's C4).
- **TD's test items**: **R6-1** (gate (b)'s script,
  `tests/compare_clean_base.py`, in quickstart.md, R3 (b), slice 7 and the
  structure); **R6-2** with R3-9's plan part and LANE2-PINS's R18 site
  (the probe shim behind the counting wrapper; plan.md's Testing;
  traceability.md's module note); **R6-3** (the notice under `--json` too,
  the lead's reading of FR-046); **R6-4**; **R6-5** (the seam table
  `OVERVIEW_FS`, the render function `render_report()`); **R6-6**; **R6-7**
  (traceability.md's "Held items, chosen: their tests", O12 to O16 added;
  plan.md's Summary); **R6-8** (505, 10 and 5 rows); **R6-9**; **R6-10**;
  **R6-12** (the fake owner tools' loop, tried in a scratch directory
  first); **R6-13** (R18's "Lengths", and R20's note that no figure rests
  on the script); **R6-15**; and the optional **N1**, **N3** and **N4**.
- **Lane openRepoProject-3's W112 OBS**: **R7-OBS-1**, traceability.md's O11
  lines say "built now as the plan's reading", C-72 at `7f4ab94` naming no
  "for his review" any more; **R7-OBS-2**'s first half, Revision 7's
  R6-OBS-1 bullet (Bookkeeping, below).
- **Lane openRepoProject-3's W132 read of revision 8** (the lead's message):
  **LOW-1**, this file's opening; **LOW-2**, R1's Finding; **LOW-3**, R1's
  #19 ranges, R-343's sentence at `:1492-1500` and T9 at `:1500-1514` (with
  OBS-3, lines 74-77 naming round (p)); **LOW-4**, plan.md's Citations;
  **LOW-5**, O11 part 1's exception in plan.md's Summary and R20's opening;
  and OBS-2, O14 and O16 in traceability.md. Its round (q) table is not
  taken: PR #19 stays at `e0b1671` (revision 10's part 2 re-pins it to
  `4512441`).
- **The stale spec cites**: R4's Dependencies quote, R5's FR-021, R7's
  FR-013 and R10's FR-005 move from `4072608` to `7f4ab94`, each quoted
  string found once at both heads.
- **Bookkeeping**: Revision 7's R6-OBS-1 bullet now ends "no plan revision
  needs to re-pin its spec cites", W112's words, where it read "name a
  later spec commit"; the Revision 8 record keeps its `:1492-1499`, the
  range as revision 8 wrote it.

## Revision 10: C-72 at 8c408e6 and 617dcd9, O17 to O21 open, re-pins, W137

Made from `8c408e6` (spec commit 3an), on the lead's decisions for revision 10,
in three parts; this is part 1. The plan's other spec cites stay at `7f4ab94`
and PR #19's at `e0b1671` in this part. Each input of part 1, and where it is
taken:

- **C-72 at `8c408e6`** (spec.md:956-1097, sha256 `95a516fa4163...`): R20
  quotes it whole in place of its text at `7f4ab94` (spec.md:954-1047), and
  R20's opening names the new sha and lines. The quote less its `> ` marks
  equals those lines by `cmp`, each continuation line less its two-space
  indent, which the mark takes, as in the quote at `7f4ab94`.
- **The ordering sentence**: plan.md's quote of it, 99 words, is C-72's at
  `8c408e6` word for word, at spec.md:1003-1010 (:998-1006 at `7f4ab94`); its
  cite moves, and its words do not.
- **O15 (A) and O16 (a)**: built now, ahead of A1's text, as C-72's rule
  sentence says, in plan.md's Summary and held-items list, R20's opening and
  the contract's reading note.
- **O17 to O20**, raised by #19's round (q) and open for his word (C-72): R20
  is retitled; this file's index, R20's opening, plan.md's Technical design,
  Summary, closing Technical Context sentence and held-items section, and the
  contract's reading note say that O1 to O16 are chosen and O17 to O20 open;
  the contract marks each OPEN where it builds the text or check (the reflog
  remedies, the stale text, the registration finding and the status pins), and
  plan.md lists them as still before him: until his word the plan builds A1 as
  ratified, and the four pins by FR-016.
- **Still to come**: part 2 re-pins PR #19's cites from `e0b1671`, and part 3
  takes lane openRepoProject-3's W137 items.

Part 2, made from `617dcd9` (spec commit 3aq, on 3ao at `bb97468` and 3ap at
`922a7c0`), on the lead's brief for it and the lead's later messages (feature
004's map at `41759a4`, its section 2.4; O21; C-72 at `617dcd9`). Each input of
part 2, and where it is taken:

- **PR #19 from `e0b1671` to `4512441`**, its round (r) (R-391), on round (q)'s
  `818311a` (R-380): by lane openRepoProject-4's cite maps of rounds (q) and
  (r), sha and lines both, 23 ranges checked by `cmp` against the blobs at both
  heads, 11 moved, 1 the same and 11 changed, each class as the maps give it;
  R1's "Re-pin of revision 10, PR #19" gives the map and its cross-check with
  lane openRepoProject-3's W137 item 6 table, which agrees on every class. The
  cites move in plan.md's Citations; in this file's citations paragraph, R1's
  pin note and the pointers of its revision 3 and 4 bullets, R3 (e), R9, R18's
  PN-17 and R20's PR #19 paragraph, O6, O8, O11, Lengths and recorded items;
  and in the contract's reading note and its T7 row. The Revision 8 and 9
  records keep their `e0b1671` numbers, as records of their heads. The methods
  behind these counts, named in revision 11 on lane openRepoProject-3's W148
  OBS (2): the 23 are the range pairs of the lead's `cmp` check, each range
  the plan cited at `e0b1671` beside its image at `4512441`, both read by `git
  show`, which count T6 and T7's two kept runs (`:1360-1374` to `:1476-1490`
  and `:1376-1380` to `:1510-1514`) as moved ranges of their own beside the
  whole, changed `:1360-1380`, and T8's "never read" line (`:1488` to
  `:1637-1638`) as a changed range of its own; W148's 21, 1 the same, 9 moved
  and 11 changed, are the same pairs without the two kept runs. R1's no-prune
  sites, 40, 37 and 39, are the occurrences of R-324's whole closing phrase,
  "so do not run git worktree prune, git worktree remove or git gc until it
  can", with backticks and quote marks dropped and whitespace normalised, over
  #19's design, proposal, tasks, clarifications and three specs (28 at
  `88d0d36`); W148's 46, 43 and 45 count the shorter "do not run git worktree
  prune", which five sites of T8's clause and one design sentence also hold
  (34 at `88d0d36`), and both counts move by -3 at round (q) and +2 at round
  (r). Revision 11 reproduces all of these from `git show`.
- **The stale rows**, the round (q) map's rows 1 to 12 and 24 and the round (r)
  map's rows 27 to 31: row 1, plan.md's Citations; row 2, this file's citations
  paragraph; row 3, R1's pin note; rows 4 to 8, R1's revision 8 bullet, true at
  `e0b1671`, which the new revision 10 bullet follows; row 9, R20's PR #19
  paragraph; row 10, Lengths; row 11, the contract's reading note; row 12, the
  revision 3 and 4 bullets' pointers, the Revision 8 record keeping its own;
  row 24, R3 (e), D1, D7 and D9 edited and D2, D9 and D14 moved; row 27, R18's
  PN-17, with the `core.warnAmbiguousRefs` qualifier; row 28, which the brief
  calls row 27, plan.md's Risks bullet, now "Feature 004's build of #19's round
  (q)", the fifth pin and the nested `.git` check being his word since
  `818311a`; row 29, plan.md's parity gaps and R18's Parity, none of O17 to
  O20's differences recorded as lasting until his word; row 30, the Revision 9
  record's W132 bullet, which now points here; row 31, N-01 to N-04, in R20's
  O6, R20's recorded items and R9.
- **The spec cites** move from `7f4ab94` to `617dcd9`: plan.md's Input and R1's
  Finding; R4's Dependencies quote, R5's FR-021, R7's FR-013 and R10's FR-005,
  each quoted string found once at both heads; and R9's six ranges, mapped by
  content, four byte-identical at new lines (:4234-4237 to :4387-4390,
  :5160-5163 to :5402-5405, :1644-1654 to :1715-1725, :2444-2456 to :2527-2539)
  and FR-008's two sentences, rewrapped at 3am, word for word (:2521-2528 to
  :2604-2611, :2530-2541 to :2613-2623).
- **Feature 004 at `41759a4`**, its map's section 2.4, items 1 to 5 and 7 to 9:
  R1's pin note records the nine of the 75 R3 definitions that change in code,
  the other 66 keeping their text (`GIT_KINDS` and `RECOMMENDATIONS` among
  them), and `identity_probe` and `repo_state` unchanged, with plan.md's
  Citations and its "Feature 004 moves" bullet, and R3's opening points there
  (item 1); R12, the third override at `:3487-3492` there (item 2); plan.md's
  round (q) bullet and the contract's `STATUS_PINS`, five pins by reference
  against FR-016's four, O20 (item 3); the contract's O18 and O17 lines,
  feature 004's texts at `41759a4` (items 4 and 5); plan.md's parity gaps and
  R18, the merged-set case, O21 (item 7); the pin note and the contract's O19
  line, `enclosing_rows()`, `_read_row()`'s symbolic-link case and
  `nested_git_check()` (item 8); and the pin note, T9 at `:7464-7465`,
  `UNREAD_NEXT_STEPS` at `:5770-5774` and T6 and T7 at `:934-939` there, with
  R20's recorded items (item 9). The `project:N` cites stay at `d6bac50` until
  tasks are written (plan.md's rule): of the plan files' 209, the map finds 10
  at the same lines, 181 moved with their text and 18 changed. Item 6,
  EC-028's, is the spec's, taken at 3aq.
- **O21**, from feature 004's `41759a4`, open for his word (C-72 at 3aq): this
  file's index, R18's Parity, and R20's title, opening and terms; plan.md's
  Summary, Technical design, closing Technical Context sentence, parity gaps
  and held-items section; and the contract's reading note name it beside O17 to
  O20, and the plan builds A1 as ratified for it until his word. The contract
  has no OPEN line for it, a case of the parity tests.
- **C-72 at `617dcd9`** (spec.md:956-1118, 163 lines, sha256
  `126d943ed582...`): R20 quotes it whole in place of its text at `8c408e6`,
  and R20's opening names the new sha and lines. The quote less its `> ` marks
  equals those lines by `cmp`, each continuation line less its two-space
  indent. plan.md's quote of the ordering sentence, 99 words, is C-72's at
  `617dcd9` word for word, at spec.md:1003-1010 as at `8c408e6`; its cite moves
  to the new sha.
- **Bookkeeping**: this record's heading names part 2's sha and O21; R1's
  revision 4 bullet, R3 (e), R12's Decision and plan.md's Summary paragraph on
  the held items are rewrapped where an edit left a line short or long, their
  words unchanged.
- **Still to come**: part 3 takes lane openRepoProject-3's W137 items and the
  lead's two remaining revision 10 items, which wait for the lead's word.

Part 3, made from `3680f34` (spec commit 3ar, which cites feature 004's
`status_warned` at `41759a4` in EC-033), on the lead's message after part 2,
lane openRepoProject-3's W137 read of revision 9 at `e342275` and the two items
that part 1 left. Each input of part 3, and where it is taken:

- **W137's LOW-1**, the thread bound: R7's bound and plan.md's Threads bullet
  say that R + 2,561 replaces A1 design D8's "at most 32 roots ... and a
  handful more" (A1 `design.md:506-508`), 1,696 at 32 roots, A1's text staying
  as ratified, and why: the roots are canonicalised before the cap (C-67), and
  D8's list lacks the identity step, D3's reads and the re-verification.
- **LOW-2**, the 16 running filesystem tasks: the data model's Constants gain
  `OVERVIEW["fs_tasks"]`, 16 per run, an internal constant and not a limit; R5
  names it, and R18's Seams bullet tests that a 512-row repository never runs
  more than 16 at once.
- **LOW-3**, the extension read: R9 says that Git's own format check also
  honours the key at format version 0 (the review's R8, its c6e), so that the
  read neither tests the format version nor follows an include; the Revision 9
  record's R8-5 bullet says that its reason for leaving the clause out was a
  misreading, and that this part takes it.
- **OBS-1**: plan.md's Citations name W137's read at `e342275` and say that
  revisions 2 onward take each HIGH, MEDIUM and LOW finding of lane
  openRepoProject-3's reads, W96's one HIGH among them, where W137 proposed
  "each MEDIUM and LOW finding".
- **OBS-2**: R5 adds that a hung mount holding more than 16 rows takes waves of
  5 s, the later tasks past about 192 hung ones recording `deadline-exceeded`,
  and that scenario 24's few tasks fit in one wave.
- **OBS-3**, the plain stale text: R12, R20's O6 and O8 and the contract's "the
  class's recommendation, verbatim" say that it is O18's question, open: until
  his word the plan builds A1's 50-character text and, once A1's re-alignment
  lands, O8 (A)'s 63-character locked form, though feature 004's `TEXT` at
  `41759a4` carries the 305- and 318-character forms, its
  `RECOMMENDATIONS["stale-worktree"]` staying the 50-character text.
- **"Ahead of A1's text"**, the first item part 1 left: every other "built now"
  site of O15 (A) and O16 (a) says it, in R5, R12, R20's O15 and O16 entries,
  the contract's JSON keys and composer, the data model's `branch` and
  traceability.md's FR-008 line and held-items list.
- **The ordering note**, the second: plan.md's sentence after the ordering
  quote names, beside O13 (A), A1's records for O12 (A), O14 (A) and O15 (A),
  the design Risks entry for O14 (A), D5's sentence for O15 (A) and the entry
  for O16 (a)'s null fields, as C-72 does. C-72 names no A1 record for O21,
  open, whose (A) needs no amendment, so the note names none.
- **The spec cites** move from `617dcd9` to `3680f34`: plan.md's Input and
  ordering cite, R1's Finding, R20's opening, R4's Dependencies quote, R5's
  FR-021, R7's FR-013 and R10's FR-005, each quoted string found once at both
  heads, and R9's six ranges, mapped by content, byte-identical at their new
  lines (:4391-4394, :5408-5411, :2608-2615, :2617-2627, :1715-1725,
  :2531-2543). C-72 is unchanged at `3680f34` (spec.md:956-1118, sha256
  `126d943ed582...`): R20's quote equals it by `cmp`, and plan.md's ordering
  quote is its 99 words at spec.md:1003-1010, `d0fbdb9e738ecbab`.
- **Bookkeeping**: this record's heading names W137; the paragraphs that an
  edit left with a short or long line are rewrapped, their other words
  unchanged.

Revision 10 is complete with this part.

## Revision 11: O17-O21 chosen, O22, O23 open, C-72 at c71a53e, f47c2fd

Made from `c71a53e` (spec commit 3as), on the lead's decisions for spec 3as and
plan revision 11, in parts; this is part 1. Its inputs: Brett Heap's "yes,
recommended for O17-O21", typed in lane openRepoProject-4's session at
2026-10-23T21:10:35Z and RULED in its log at 21:11:44Z (issue #10); spec 3as,
which records it in C-72; and lane openRepoProject-3's W148 read of revision
10 at `dd69a2b` (0 HIGH, 0 MEDIUM, 1 LOW, 5 OBS). PR #19 stays at `4512441`,
PR #27 at `d95eea2`, and the `project:N` cites at `d6bac50`. Each input, and
where it is taken:

- **C-72 at `c71a53e`** (spec.md:960-1112, 153 lines, sha256
  `9e3e09f003d0...`): R20 quotes it whole in place of its text at `3680f34`,
  the quote's lines 99 on, from "included. On his word", replacing the old
  lines 99 to 163; the quote less its `> ` marks equals those lines by `cmp`,
  each continuation line less its two-space indent. R20's title and opening
  name the new sha and lines and his fourth word. plan.md's ordering quote,
  99 words, is C-72's at spec.md:1007-1014 word for word, `d0fbdb9e738ecbab`
  as at `3680f34` (spec.md:1003-1010); its cite moves, its words do not.
- **O17 to O21, chosen** (C-72): every plan mark of them as open becomes
  chosen. R20 gains "Chosen by his word of 2026-10-23T21:10:35Z" with an entry
  for each, its "In this entry's terms" paragraph and this file's index say
  every held item is chosen, and plan.md's Input note, Authority, Summary,
  closing Technical Context sentence and held-items section say the same, the
  Summary, the Technical design note, the parity gaps and the held-items section
  naming the two points that wait for feature 004's next head (the closing
  Technical Context sentence names none: part 2's record, W159 LOW-2). Built as
  follows:
  - O17 (A) and O18 (A) land with A1's re-alignment, A1 as ratified until
    then (102 and 97 characters; one 50-character stale text): R20's O1, O6,
    O8 and "Lengths" (O17's 253 and 248; O18's 305 and 318, up to 459 and 472
    beside the redirect remedy), R12's composer, which gains `whole=False`,
    R18's "Lengths", R1's pin note, and the contract's composer, stale rows
    and reflog remedies. W148's LOW-1 is settled by O18 (A): the contract's
    O8 (A) line names its 63-character text as the one O18 (A) ends with the
    warning, and a CHOSEN (O18 (A)) line follows it (PCL:188-197 at
    `4512441`).
  - O20 (A), built now, ahead of A1's text: the five pins by reference to
    feature 004's `STATUS_PINS`, `-c core.ignoreCase=false` the fifth at
    `41759a4`, in the contract's Git children, R3, R18's wrapper bullet and
    plan.md's round (q) Risks bullet.
  - O21 (A), built now, as A1 is ratified: A1's null class, in R18's Parity,
    plan.md's parity gaps, R20 and traceability.md's SC-003 line, with one
    pointer at each: the case is checked against feature 004's next head.
  - O19 (A), built now, ahead of A1's text, recorded as chosen: its inputs, the
    listing's paths and FR-007's no-follow `lstat`, with no new Git child, in
    a new R9 bullet and the data model's `registration-mismatch` gate; the
    contract's O19 line, R18's new fixture bullet, R20 and traceability.md,
    each with one pointer to feature 004's next head.
- **Held, and why**: O19's outcome for such a row (its class, its gate and its
  finding sentence) and O21's case. Lane openRepoProject-2's report to lane 4
  of 2026-10-23 says that lane openRepoProject-3's W139 found Q2 (1) and Q9
  (b) in feature 004's shared row reader at `41759a4`, and that lane 2's lead
  (R-409) confines both to `project clean`'s plan in a code round that has not
  landed yet, which may change the merged-set block too. So no plan text
  states that outcome, gives R18's tests an expected result for those rows,
  cites feature 004's functions for them, or names a parity test or a lasting
  difference for O21; the contract's O19 line drops its two function cites.
  R1's pin note keeps its record of what `41759a4` does, re-read at that head.
- **W148**: LOW-1, above; OBS (3), "ahead of A1's text" added at the seven
  bare O15 and O16 cites (data-model.md's worktree-row note, `head` and
  `merged_into_target`; the contract's `remedy.scan-limit`; R18's "Lengths";
  R20's O15 length row; traceability.md's FR-031 to FR-035 line); OBS (5),
  traceability.md's "Held items, chosen" gains rows for O17 to O21 and its FR
  lines name them; OBS (2), revision 10's part 2 record now names the methods
  behind its 23 ranges and R1's 40, 37 and 39 sites, which this part
  reproduces from `git show`, beside W148's 21 and 46, 43 and 45; plan.md's
  Citations name W148's read. OBS (1) and (4) need no edit here: (4) goes to
  part 2.
- **The spec cites** move from `3680f34` to `c71a53e`. Method: each range is
  mapped by the line shifts of the 18 hunks of `git diff -U0 3680f34 c71a53e`
  on spec.md and then compared byte for byte at its mapped lines, and each
  quoted string is counted once at both heads, whitespace normalised. Of the
  eight ranges, 0 are the same, 7 moved, byte-identical (the ordering quote,
  :1003-1010 to :1007-1014; R9's :4391-4394 to :4398-4401, :5408-5411 to
  :5424-5427, :2608-2615 to :2602-2609, :2617-2627 to :2611-2621, :1715-1725
  to :1709-1719 and :2531-2543 to :2525-2537), and 1 changed (C-72, re-quoted,
  above); the four quoted strings (R4's Dependencies, R5's FR-021, R7's FR-013
  and R10's FR-005) occur once at both heads, and plan.md's Input and R1's
  Finding move their sha alone.
- **Still to come**: part 2, for #19's rounds (s) and (t), #27's B26 and
  feature 004's next head, where O19's outcome is stated and O21's case
  checked, and R1's pin note and plan.md's Risks are re-read.

Part 2, made from `f47c2fd` (spec commit 3av, on 3au at `76c0073` and 3at at
`220ad83`), on the lead's decisions for 3at and part 2 and lane
openRepoProject-3's W158 and W159 reads, with its W160 read of `main` at
`b42355e`. Brett Heap has not ruled on O22 or O23. PR #19 moves to `54e869b`;
PR #27 stays at `d95eea2`, A1 at `e4a30fc` and the `project:N` cites at
`d6bac50`. Each input of part 2, and where it is taken:

- **PR #19 from `4512441` to `54e869b`**, rounds (s) (`dab8a64`; R-408, R-409)
  and (t) (R-413, Brett Heap's M1 (a) and M3 (a)), by lane openRepoProject-4's
  cite map of both rounds (251 distinct ranges, each class derived twice and
  read by `cmp`; the plan files hold 115 of its 350 rows) and its plan edit
  list: plan.md's Citations and Risks; this file's citations paragraph, R1's pin
  note, the pointers of its revision 3 and 4 bullets and a new "Re-pin of
  revision 11" bullet, R3 (e), R9, R18's PN-17, R20's PR #19 paragraph, O6, O8,
  O11, O17, O18, O19, Lengths and recorded items; and the contract's reading
  note, its T7 row and its O17 and O18 lines. The Revision 8 and 9 records and
  the older re-pin bullets keep their numbers, as records of their heads, by the
  rule of part 2 of revision 10: 52 history rows, each kept.
- **The stale statements**: the revision 10 bullet's "its plain case before
  Brett Heap as round (r)'s M1" (M1 is ruled (a), R-413) and "`PCL:166` stands"
  (it is PCL:185) are fixed in place with forward pointers, and plan.md's
  "`PCL:166` and the rewording at :416-418 stand" is rewritten; the contract's
  O17 line is rebuilt by script, quoting both messages whole, 253 and 248
  characters.
- **C-72 at `f47c2fd`** (spec.md:961-1181, 221 lines, sha256 `08e05447e640...`):
  R20 quotes it whole in place of its text at `c71a53e` (spec.md:960-1112), O22
  and O23 included, open; the quote less its `> ` marks equals those lines by
  `cmp`, each continuation line less its two-space indent. plan.md's ordering
  quote, 99 words, is C-72's at spec.md:1010-1017 word for word, as at
  :1007-1014 of `c71a53e`.
- **O19's outcome and O21's case, at feature 004's `904aefc`** (its `project`
  that of `d640539`; lane openRepoProject-2's R-416 and R-424; C-72): stated,
  with no wait, in R1's pin note, R9, R18's fixtures and Parity, R20's terms,
  opening and O19 and O21 entries, plan.md's Technical design note, Summary,
  parity gaps and held-items section, the data model's `registration-mismatch`
  gate, the contract's reading note and O19 line and traceability.md's O19, O21
  and SC-003 lines. O19's class follows `project clean`'s, `inspection-error`;
  O21's three kinds of row are a lasting difference of the parity tests.
- **O22 and O23, open for his word** (C-72): R20 gains a subsection for them,
  and this file's index, R20's heading and terms paragraph, R12, the data
  model's finding sources and `registration-mismatch` gate, the contract's
  reading note and `finding.*` lines, plan.md's Technical design note, Summary,
  closing Technical Context sentence and held-items section, and
  traceability.md's FR lines and a new "Held items, open" section say so; until
  he rules the plan builds A1 as ratified, O23 as FR-007 reads, (B)'s reading.
- **Feature 004 at `904aefc`** (lane openRepoProject-4's comparison by syntax
  tree with `41759a4`: 332 top-level names, none added or removed, 8 changed in
  code and 3 in a docstring alone): R1's Finding and pin note and plan.md's
  Citations and Risks name it; of R3's reused definitions only `TEXT` and
  `WorktreeRow` change, in neither a signature nor a result that the overview
  reads; round (s)'s one filesystem call under one budget for the nested `.git`
  check is `nested_git_check()`'s, a check the overview never runs.
- **W159** (lane openRepoProject-3's read of part 1 at `8c3b046`: 0 HIGH, 0
  MEDIUM, 2 LOW, 6 OBS): LOW-1, plan.md's Summary sentence on what reaches A1 no
  longer reads as if O17 to O20's texts were not his word, the lead's-choice
  clause being the O16 (a) entry's alone; LOW-2, part 1's record omitted three
  changes, which this part names: the data model's note on the items that change
  one row of each table gained "and O17" (data-model.md:415), R1's Decision
  names his fourth word beside the three before it (research.md:63-71), and
  plan.md's Summary (:91-102) says "Two points wait"; and part 1's record said
  the closing Technical Context sentence waits, which plan.md:289-292 does not
  (a forward pointer in place, above); OBS-2, R18's Parity and traceability.md's
  SC-003 line no longer imply O21's held half. Its OBS-1, OBS-3, OBS-4, OBS-5
  and OBS-6 are taken by the bullets above, and plan.md's Citations name W159's
  read.
- **`main` at `b42355e`** (lane openRepoProject-3's W160): since `f271a39`
  (PR #40) `workbenches()` tries `openBenches` and then `workBenches`, a set
  `WORKBENCHES_ROOT` being its only candidate, and `b42355e` (PR #41) links the
  repository as openBenches, GitHub redirecting the old name (lane
  openRepoProject-3's check of 2026-10-31): plan.md's slice 1, R18's Isolation
  and quickstart.md's isolation sentence name "openBenches (formerly
  workBenches)", as spec 3av does, and say that the fixture's `WORKBENCHES_ROOT`
  keeps that discovery from running. #40 changes no text the plan quotes, and no
  cite moves.
- **The spec cites** move from `c71a53e` to `f47c2fd`. Method: each range's
  lines at `c71a53e` are found once at `f47c2fd`, byte for byte, and each quoted
  string is counted once at both heads, whitespace normalised. Of the eight
  ranges, 7 moved, byte-identical (the ordering quote, :1007-1014 to :1010-1017;
  R9's :4398-4401 to :4531-4534, :5424-5427 to :5636-5639, :2602-2609 to
  :2680-2687, :2611-2621 to :2689-2699, :1709-1719 to :1778-1788 and :2525-2537
  to :2603-2615), and 1 changed (C-72, re-quoted, above); the four quoted
  strings (R4's Dependencies, R5's FR-021, R7's FR-013 and R10's FR-005) occur
  once at both heads, FR-005, FR-013, FR-021, C-56 and the Status paragraph are
  byte-identical, and plan.md's Input and R1's Finding move their sha alone.
- **Bookkeeping**: this record's heading names O22, O23 and the new sha.
- **Not taken here**: #27's B26. Spec 3au moved its own #27 cites from `d95eea2`
  to `7f3453c`; R1's #27 bullet keeps `d95eea2`, its re-pin not among this
  part's inputs.
