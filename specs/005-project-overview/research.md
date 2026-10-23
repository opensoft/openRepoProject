Lane: openRepoProject-4

# Research: Project overview

The Technical Context in [plan.md](plan.md) has no NEEDS CLARIFICATION. The
ratified change `add-project-overview` (landed as `961c405`), its amendment
A1 (PR #34 at `e4a30fc`, ratified by Brett Heap's "ratify 34" on
2026-10-22) and [spec.md](spec.md) with its 72 clarifications decide almost
every behaviour, and they govern. These entries settle what they leave to the
plan, record Brett Heap's word on the held items (C-72) and isolate what
only he can still decide:

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
- R20: the held items, partly ruled: five chosen by his word (C-72), built
  once A1's re-alignment lands, and six open, each with the design of each
  answer (decision 2);
- Revision 2: where each finding of lane openRepoProject-3's W96 read is
  taken;
- Revisions 3 to 6: where each input of those revisions is taken.

Each entry gives a Decision, its Rationale and the Alternatives considered.
Citations, as [plan.md](plan.md) "Citations" defines them: `project:N` is
line N of feature 004's `project` at `d6bac50` (branch
`004-project-clean-all-safe`, draft PR #33), read with `git show
d6bac50:project`; `A1:N` and `A1 design.md:N` are lines of change 2's
`specs/project-overview/spec.md` and `design.md` at `e4a30fc`; `PCM:N`,
`PCL:N` and `#19 design.md:N` are lines of change 1's
`specs/project-command/spec.md`, `specs/project-clean/spec.md` and
`design.md` at PR #19's `88d0d36`, its round (o); POD, PRSD, CMD, CLN and
DI are as [spec.md](spec.md) defines them. Revision 1 moved every cite from
`4b4c36b` and `ccc52b9` (R1); revision 2 moved none; revision 3 moved them
from `0a82a62` and `20084cd`, and revision 4 from `211e43d` and `2250830`
(R1). Nothing here was run against a repository: the plan step ran no
`project` and no owner tool (R18).

## R1. Authority, pins and re-pins

- **Finding**: C-56 (Q2 A) and A1's task 1.7 set the plan after feature 004
  merges into `main`, on Brett Heap's word given after that merge; spec 005 at
  `98b95db` (its commit 3ai) records in C-56 and its Status that his word
  below moved that order for the plan step, and in C-72 his word on the
  plan's held items (R20). Feature 004 has not merged: PR #33 is a draft,
  its branch at `d6bac50`. Brett Heap said, at 2026-10-22T19:46:57Z, "lane 4
  plans 005 now".
- **Decision**: that word moves C-56's order for this plan step only, as his
  "lane 4 specifies 005 now" moved change 2's order for the specify step
  (C-21). It authorizes this plan and nothing after it: no `tasks.md`, no
  code and no test is written, and the tasks and the implementation each
  wait for his word (R2). His word on the held items, "yes, recommended for
  O1-O10" (C-72), chooses options for change 2 and is no word for the tasks
  or the implementation either. This plan pins its reads at:
  - feature 004's `project`, tests and documents at `d6bac50`; its later
    head `f3724fc` (doc round 24) changes three documents only
    (`hand-runs.md`, `tasks.md`, `traceability.md`), `project` and the
    tests unchanged since `d6bac50` (`git diff --quiet`), so the plan names
    it as a later head only;
  - PR #19's change 1 at `88d0d36`, its round (o) (R-349), which changes no
    spec text of its round (n), `2250830`, accepted by lane
    openRepoProject-2 (R-345), with T1 to T8 confirmed by Brett Heap
    ("R-320: yes" for T6 to T8) and their warnings in the words of his
    "R-324: yes" (the lead's R-343);
  - A1 at `e4a30fc`;
  - #24's change at `fe5b245` (PR #27 at `288fc34`, its round B23, moved
    from `04be7f6` in revision 3 and from `dafe476` in revision 5; its
    eight pinned ranges and its specs byte-identical by the lead's `cmp`,
    and its `project-overview` block blob `a40458cb` at `fe5b245`,
    `04be7f6`, `dafe476` and `288fc34` alike) and #25's at `05a424a` (PR
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
  recommendation alone, T8 at `:1457-1466`, R-343's sentence at `:1467-1475`,
  and F-1's (b), still not ruled, at `:2214-2219`. R-343 records Brett Heap's
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
- **Re-pin of revision 4, PR #19**: `88d0d36` is round (o), one commit on
  `2250830` (R-349). Its specs are unchanged (`git diff --quiet`), so the PCM
  and PCL cites stand; its design gains two lines at `#19 design.md:73-76`, so
  every design cite after them moves by 2, each checked by content: D2's driver
  at `:217-222`, D7's row 4c sentence at `:489-490` and row 4b's at `:513-517`,
  D9 at `:637`, D14 at `:984`, T6 and T7 at `:1349-1369`, T8 at `:1459-1468`,
  R-343's sentence at `:1469-1477`, and F-1's (b), still not ruled, at
  `:2216-2221`; its proposal changes in place at its line 1314 and from its
  line 2338 on, none of which this plan cites.
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
  unchanged (`project:N` at `d6bac50`; R1):

  - timing: `TIMING` (`:560-570`): deadline 60, probe budget 5, grace 2,
    reap wait 2, tick 0.1;
  - contracts: `LIMITS` (`:589-600`), for the shared constants and the
    record bounds; `GIT_FLOOR` (`:602`); the `TEXT` rows the contract
    names;
  - git environment: `GIT_SCRUB` (`:1048-1060`, 31 names), `TRACE2_OFF`
    (`:1068`), `PROTOCOL_PINS` (`:1072-1077`), `STATUS_PINS`
    (`:1084-1085`), `GIT_KINDS` (`:1090-1103`; kinds `probe` and `status`
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
    `unparseable_error`, `probe_error` and `os_error` (`:2630-2675`),
    `_direct` (`:2693`), `presence_from_lstat` (`:2713`), `gitdir_line`
    (`:2793`), `main_worktree_decision` (`:2853`),
    `registration_verdict` (`:2941`), `verify_registration` with
    `fs=_direct` (`:2978`), `status_warned` (`:3012`),
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
    one-wide loop stays in `run_bounded` between them;
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
    ([quickstart.md](quickstart.md)).
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
    `project --help` differing only by the overview's name in the
    subcommand list and its help line, and feature 004's argument and
    refusal tests unchanged.
  - **(e)** the changes land on `main` after PR #33 (R2's base). If the
    split changes anything PR #19's text describes of the driver or of
    bounded work (its design D1 and D2, `run_bounded`'s contract at `#19
    design.md:217-222`; D9, the removal child, `:637`; D14, the fit
    arithmetic, `:984`), feature 005's spec says so and PR #19 is not
    edited for it. This plan's split changes none of them: `run_bounded`
    keeps its signature, its outcomes and every caller. The spec is not
    this plan's to edit, so a finding of that kind goes to lane
    openRepoProject-4's lead before the change lands.

  New, in the overview's regions: the control loop and its slots (R4, R6),
  the per-candidate collectors (R5), the filesystem task (R7), the
  keep-filter parser (R8), the overview's own readers of the extension read,
  the work-tree probe and realpaths (R9), discovery (R10), findings, gates
  and the message composer (R12), the envelope, the human report and the
  writer (R15, R16), and the overview's tables of messages, attention codes
  and remedies (the contract).
- **Not reused**: `run_bounded`'s loop, `fs_call` (`:1896`), `_fs`,
  `_lstat` and `_realpath` (`:2678-2738`), `identity_probe` (`:2764`),
  `worktree_config` (`:3054`), `effective_work_tree` (`:3078`),
  `inspect_repository` (`:3109`), `_read_row`, `_identity_unchanged`,
  `_read_status` and `worktree_rows` (`:3345-3551`), `read_reflog`
  (`:5153`), `declared_tracking_branch` (`:2440`) and `projects_dirs`
  (`:114-122`): each blocks its caller until one child or call ends, or
  reads as R9 says the overview may not, while the overview's one loop
  drives four children and many tasks at once (FR-019); `projects_dirs`
  resolves `PROJECTS_DIR` on the calling thread (`found.resolve()`,
  `:120`), outside the root task (R10). The overview calls the same
  deciders from its own generators instead, in the same order. `discover()`
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
  sha}` is the call's result less `notes`.
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
  filesystem workers write one byte to when they finish. Each wait's
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
  child at once and refuses every later start (FR-012). The run is entered
  under `signal_scope()` (record-only handlers, FR-044); the loop raises
  `Interrupted` (a `BaseException`, `:1310`) once the slot is set, and its
  `finally` terminates and reaps every live handle before the scope's exit
  kills any group left (`kill_live_probes`).
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
  005 at `4072608` records the choice in its Dependencies, where feature
  004's runner is described: "D1's one self-pipe being realized as two
  read ends on one selector, `signal_scope`'s wakeup pipe and the loop's
  task pipe, with behaviour unchanged (the plan's research.md R4 at
  `6fb619c`)".
- **Alternatives considered**: threads per repository and `asyncio`
  (rejected by D1); polling the workers on the tick alone, rejected because
  a 0.1 s tick would add latency to every one of up to 2,465 tasks (R7).

## R5. Collectors, the boundary and step order (FR-021)

- **Decision**: each candidate's collector is a generator. It yields
  requests, `GitStep(argv, directory, parser, kind)` or `FsStep(fn, args)`,
  and is resumed with a `StepResult` (the `DriverOutcome`, or a task's value,
  its `OSError`, or its cut). Its steps are FR-021's, in order: the marker
  checks (done by its root's task, R10), the identity probe and, on any
  line count but two, the one-option re-reads (`IDENTITY_OPTIONS`,
  `:2577`; EC-032); for the first candidate of a repository, that
  repository's steps: the registry listing, D3's gitfile steps where the
  first record is `common_dir`, the manifest read at `repository.root` (at
  the row's `path` when that is null, or at the candidate without Git),
  the extension read, the ref listing, merge-target resolution, the merged
  set, then each row's task, the twin decision (`shared_paths`,
  `shared_identities`), and per row its work-tree probe (where the
  extension is taken as true), its re-verification and its status probe,
  then classification
  (`row_evidence`, then `classify` through it), the reflog gate's reads and
  the findings. The boundary is one `try`/`except Exception` around each
  resume: an exception becomes that candidate's row error by the collector
  table (`internal-error`, message `internal error (CLASS)`), the generator
  is closed, evidence already held stays and every other field stays null.
  `Interrupted`, `Terminated` and `KeyboardInterrupt` are `BaseException`s
  and pass. A merge is the identity step's result: a candidate whose common
  directory's `(dev, ino)` is already a repository joins it and its
  generator ends.
- **The manifest's place**: FR-021 at `4072608` places "the manifest read
  at `repository.root` once that is named (after the identity probe where
  the candidate is the main worktree, else after the registry listing and
  design D3's steps), always before the ref listing (design D9), or at the
  candidate for a row without Git", and A1 design D9 needs it before the
  ref listing, whose keep-filter takes its `tracking_branch`. The plan
  reads it there; row errors keep that step order. In D3
  item 3's layout, a first registry record equal to `common_dir` whose
  checkout no candidate has yet named, a later candidate may still name it
  (D3's third wait, `A1 design.md:196-201`), so that repository's manifest
  read, ref listing and merged set wait with its second phase until every
  candidate's identity probe has completed or failed: the root is then
  final, and the manifest is read there, or at the row's `path` while the
  root stays null. So the manifest, the merge target and the JSON never
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
  them) may start for any candidate at once. A repository's phase 2 (its
  rows' tasks and probes) starts only when (1) every candidate earlier in
  canonical order has completed or failed its identity step, (2) every
  repository earlier in canonical order has finished phase 1, and (3) for a
  repository whose first registry record equals its `common_dir` and whose
  checkout no candidate has named, every candidate's identity step has
  completed or failed (D3's third wait). At that point the 512-row cap
  selects its rows by rank and row order (FR-018). Within phase 2, a
  repository's first worktree probe waits until each of its rows within
  the cap has finished its first-read task, so the twins are decided from
  every row (EC-031).
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
  its result. No pool: an abandoned thread stays blocked and is never
  joined (EC-001). The tasks are FR-013's, each one thread:
  - one per root: canonicalisation, the dedupe `stat`, one `os.scandir`
    pass and, per entry directory, the marker checks and the holder `stat`
    (A1 design D2), the worker checking the root's cancel flag between
    entries and appending finished entries under a lock;
  - one per manifest read (stat, then a read of at most 1 MiB of a regular
    file, `fstat` again on the open file, FR-014), parse included;
  - one per worktree row within the cap: its `lstat`, strict realpath and
    registration reads (`verify_registration(..., fs=_direct)`), the
    `commondir` read included; the missing-main `lstat`, and D3's `.git`
    reads with the realpath of `core.worktree`, take the same shape;
  - one per re-verification that FR-007 makes immediately before a status
    probe, enclosing the same reads again (lane openRepoProject-2's R-101
    (j); R17), the task FR-013 at `4072608` names in those words;
  - one per linked row whose work-tree probe ran: the strict realpath of
    the toplevel it printed, compared with the row's;
  - one per reflog read (at most 64 KiB, `reflog_path`, `:5073`);
  - one at start for the working directory's realpath (FR-026).
- **The bound (PN-10)**: abandoned workers are bounded by the tasks a run
  can start, since no task starts after the deadline: 32 roots, 1 working
  directory, at most 3 per candidate (manifest, D3's reads, missing-main
  `lstat`; 128 candidates) and at most 4 per worktree row
  within the cap (first read, re-verification, toplevel realpath, reflog;
  512 rows): 32 + 1 + 384 + 2,048 = 2,465 threads at the very most, in
  practice the few whose call is stuck in the kernel. Without the
  re-verification, which D8's list predates, the same sum is 1,953. The
  plan adds no further cap: a cap on abandoned threads would need a new
  limit and a new code, outside schema 1's closed sets (FR-022, FR-047).
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
  `probe-timeout`; `deadline-exceeded`). A1's proposal says so of an exit
  1 with a warning: it "stays a failure that counts as true" (A1
  `proposal.md`:1370-1375). Feature 004 reads the key the same way since
  `211e43d`: lane openRepoProject-2's R-332 has `worktree_config`
  (`:3054-3075`) follow PR #19's D7, "an unset value is false and any
  other failure counts as true" (`#19 design.md:489-490`), through
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
  scenario's own test fails. Spec 005 at `7b37557` carries the same conflict:
  it records the collector table's row with "two exceptions" (spec.md:4060 and
  :4961), against FR-008's gitfile root sentence (:2424-2431) and its sentence
  reading the unset key as no value (:2433-2439), and against User Story 8's
  scenario 1 (:1569-1578); its FR-007 names the gap and A1's held item 11
  (:2351-2362). The scenario's first case names no exit status, where its
  second case, only a linked worktree a candidate, gives exit 1; the plan reads
  the first case, by that contrast, as no error. The plan reads that conflict
  in ratified text as O11's part 1, built now: an exit 1 with nothing on either
  stream is the key unset (`config_key_unset`, as PR #19's row 4b reads the
  same key, "an exit 1 with nothing printed is the key unset", `#19
  design.md:513-517`, the lead's R-336), so resolution falls through to the
  candidate's toplevel, as the requirement's "else" and the scenario require.
  Any other outcome, an exit 1 that printed anything or any other exit, keeps
  the table's row error (`probe-failed`; `probe-timeout`; `deadline-exceeded`).
  Ratified A1 states no root for it, so `repository.root` stays null, named
  from neither `core.worktree` nor a `.git` file, and no suggestion is given
  that `project clean` would refuse, since #19 makes the main worktree
  unreadable there and refuses the run `target-not-repository-root`; no
  `unsupported-layout` finding is added, since the read failed and nothing
  shows the checkout cannot be named. Whether the withheld suggestions carry
  `target-not-repository-root` is O11's part 2, held; as planned, they carry no
  gate code, as for the other layouts whose root is null. One decider,
  `core_worktree_value()`, holds both parts.
- **Realpaths**: the overview's tasks use `os.path.realpath(...,
  strict=True)`, so `ENOENT` and `ENOTDIR` can be told from other errors
  as FR-007 and FR-026 need; feature 004's `_realpath` (`:2737`) is not
  strict, and never raises.
- **An abandoned child**: feature 004's `conclude()` path maps an abandoned
  handle to `timeout` (`:1882-1883`), as [E] has it (PCM:263-269); FR-011
  makes an abandoned child that the deadline cut `deadline-exceeded`. The
  overview's loop maps that case itself after `conclude()`.
- **The deadline's text**: `OPERATION stopped at the invocation deadline`
  (A1's table), not feature 004's "work deadline" (`:908`).
- **`tracking_freshness`**: the overview's own constant, `local refs only;
  no fetch` (FR-036; C-32), not feature 004's `TRACKING_FRESHNESS`
  (`:4265`).
- **The work-tree probe's output**: "not exactly one line" disagrees, as A1
  is ratified; PR #19's round (j) and feature 004 (`:3078-3106`) read one
  path less the final line feed. Open, as R20's O5.

## R10. Discovery details (FR-001 to FR-005; PN-9, PN-13)

- **Decision**:
  - Roots come from `--root` (repeatable), else `PROJECTS_DIR` when set and
    not empty, else `~/projects` and `~/Projects`: the strings
    `projects_dirs` (`:114-122`) selects, with its empty `PROJECTS_DIR`
    read as unset, made with `expand_user` (`:1006`) and `home_directory`
    (`:995`) and canonicalised in the root task, never by `projects_dirs`
    itself, whose `found.resolve()` (`:120`) would run a filesystem call on
    the main thread (A1 design D8, `design.md:504-505`) and skip C-67's cut
    path (FR-001). A relative root is joined to the working directory.
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
    (POD:46, A1:51) is narrower than DI:142, and FR-005 at `4072608` takes
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
  overrides (`:3334-3337`), which are feature 004's report texts. PN-1's
  sentences are fixed in the contract, each under 200 characters, from texts
  feature 004 already prints where one exists (`no-merge-target`, `:897`;
  `merge-target-conflict`, `:854-855`; `main-worktree`, `:876`). The message of
  a gated finding is built by one pure function, `compose_message(own, remedy,
  warning=None)`: own text, `; `, remedy, within 200 characters, the own text
  shortened with `...` when both do not fit (A1 design D5), a cut counted in
  characters. Two clauses, the second before him for his direct word, are
  branches of that one function (C-72), reached only when `warning` is given,
  which happens once A1's re-alignment lands: clause 1, keep the warning whole
  and shorten the recommendation before it (item 10 part 1, R20's O6 (A)), and
  clause 2, where the warning and the remedy cannot both be kept, leave the
  recommendation out and shorten the remedy, a reversal of ratified D5's
  "remedy kept whole" that only item 8's redirect remedy reaches (R20's O4 (a),
  with O6 (A)), chosen only through O6's text at `7af798a` and before him for
  his direct word. The warning is in the words of PR #19's round (n) (R-324),
  109 characters with its period. Until A1's re-alignment lands, `warning` is
  never given and D5's rule alone applies. The function is tested by length
  tables alone, R20's table among them, under both the ratified rule and the
  chosen clauses.
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
  needed to name a gitfile main checkout + 1 per worktree row within the
  cap that is present and registration-verified at its first read and that
  takes a status probe + 1 per such linked row in a repository whose
  extension read is taken as true. A bare main entry (C-68) and an unnamed
  git-directory record add none (PN-12): neither takes a status probe
  (FR-008). It is computed from first reads; a row that its
  re-verification stops keeps its estimate, so `performed` is then lower.
  Item 7's term (+3 per Git candidate whose identity probe prints other
  than two lines) is open, R20's O3; item 8's term (+1 per repository
  whose main worktree is no Git candidate, for its `main-toplevel` child)
  comes with O4 (a), chosen (R20).
- **Rationale**: FR-020 counts the children a run expects; a row that takes
  no status probe is expected to start none.

## R15. JSON form, error outputs and the writer (PN-6; PN-2; FR-039, FR-044)

- **Decision**:
  - The document is `json.dumps(doc, indent=2, ensure_ascii=True)` and one
    line feed, keys in the order the contract lists them (the delta's
    order), never sorted (PN-6), as feature 004's `write_document`
    (`:3640-3662`) writes its own.
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
    on the standard-output descriptor, so nothing is buffered for exit to
    flush (C-69). An interrupted or failed write diverts the descriptor
    (`divert_stream`, `:3758`). Where standard output has no descriptor
    (an in-process test), the stream's `write` is used.
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
  (PN-3).
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
    `--json` form; the existing tests pass unchanged.
  - **The 004-touching changes**: lane openRepoProject-2's conditions (a) to
    (e) of R3, checked in slice 1 before the change is read: the suite with
    feature 004's tests unedited (a), the side-by-side run, JSON and human (b),
    a unit test of `Invocation("clean")`'s figures and of `start_child()` and
    `conclude()` in `tests/test_overview_factoring.py` (c), the help diffs of
    every subcommand (d), and the base and the spec check of (e)
    ([quickstart.md](quickstart.md)).
  - **Isolation**: every test runs with a scratch `HOME`, `PROJECTS_DIR`
    set or unset explicitly, `WORKBENCHES_ROOT` at an empty scratch
    directory, the fixtures outside every Git work tree, and a bin
    directory first on `PATH` holding the counting `git` wrapper and fake
    owner tools (`gh`, `setup-openspeckit`, `openspec`, `onp`, `docker`)
    that log and exit 97; each test asserts that log empty. In-process
    runs add an audit hook failing on `socket.connect` and on any
    `subprocess.Popen` whose executable is not the wrapper. The
    partial-clone fixture's `remote.origin.uploadpack` names a logging
    script that must never run.
  - **The wrapper** asserts on every child: the seven protocol pins,
    `GIT_TRACE2`, `GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF` set to `0`, none
    of the 31 scrubbed names, `GIT_OPTIONAL_LOCKS=0`, the four status pins
    on a status probe, an argument vector in the overview's allow-list
    (the contract's "Git children": `--version`, `rev-parse`, `worktree
    list`, `config --get core.worktree`, `config --file`, `for-each-ref`,
    `status`), and its own process group; its log's intervals check the
    concurrency limits; it holds a chosen status probe (A1 design D13's
    fixture rewrite).
  - **Zero mutation (PN-14)**: a snapshot of every path under the fixture
    root, `.git` directories included: type, mode, size, `st_mtime_ns`,
    `st_ctime_ns`, a file's SHA-256 and a link's target; access times are
    excluded, since reads update them on most mounts.
  - **EC-033 (PN-17)**: `test_overview_a_worktree_on_a_branch_named_head`
    asserts the row's five upstream fields null, `inspection-error`, the
    project row's `git for-each-ref failed: unparseable output`, and the
    status probes' `git status failed: unparseable output` that Git's
    ambiguity warning causes (`status_warned`, `:3012`).
  - **The `core.worktree` read (R9; R20's O11)**: scenario 9's test, "A
    separate git directory", passes under part 1, its git directory having
    no `core.worktree`; part 2's case, a fake Git whose `config --get
    core.worktree` prints a line on standard error and exits 1, asserts the
    `probe-failed` row error, `repository.root` null, no suggestion, no
    `unsupported-layout` finding and, as planned, no gate code; a unit
    test of `core_worktree_value()` covers every outcome.
  - **Lengths**: the composer's tests take every row of R20's length
    table, under D5's rule alone and under the chosen clauses.
  - **Parity**: every fixture compared with `project clean <root> --json`
    keeps its ignored file a `local.env` (C-71). Two cases are recorded as
    not compared until their owners settle them: a failed ref listing
    (feature 004 prints rows `unpublished` until its R-101 (c) fix) and a
    working directory whose realpath fails (R20's O9).
  - **Git versions**: the suite runs on the CI runners' Git and on Git
    2.43.0 by hand; FR-050 adds `-k test_overview_floor_` to feature 004's
    `git-floor` job on Git 2.36.6, selecting
    `test_overview_floor_version_check_accepts_git_2_36` and
    `test_overview_floor_end_to_end_run`.
  - **Time**: only the deadline scenario shortens time, in-process,
    keeping the deadline-to-budget ratio of 12 (for example 6 s and
    0.5 s), the grace and the reap wait staying 2 s, its bound the
    shortened deadline plus 4 s; a cap or concurrency fixture that sees a
    `probe-timeout` or `deadline-exceeded` fails, never skips. Fixture
    sizes and the time budget are in [plan.md](plan.md).
  - Root-only fixtures (a refused permission) skip under root with that
    reason; non-UTF-8 paths run on Linux and skip on macOS; a FUSE variant
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

## R20. The held items: five chosen, six open (brief decision 2)

Brett Heap typed "yes, recommended for O1-O10" at 2026-10-22T21:24:03Z,
against this entry as it stood at `7af798a`; lane openRepoProject-4
recorded it as a RULED line at 21:30:52Z (issue #10), with three NOTED
corrections at 21:33:31Z (O3), 21:51:17Z (O8 to O10) and 21:54:01Z (O5).
Spec 005 records it as C-72 (at `4072608`, in the wording followed here at
`98b95db`). His "recommended" chose only where this entry or the lane's A1
re-alignment draft stated a recommendation, so five items are CHOSEN for
change 2: O1 (A), O2 (A), O4 (a) with its sub-items (c) and (d) and D5's
clause 2 case, O6 (A) and O7. For the rest, this entry quotes C-72 at
`98b95db` (spec.md:966-985) as it stands:

> D5's clause 2, item 8's case, was taken through O6's recommended text in R20
> at `7af798a`, which carried it; lane openRepoProject-3 asked, on W105's
> OBS-1, that he confirm it directly, and the lead has put it to him in lane
> openRepoProject-4's pane, so that until he answers it rests on that text.
> Five stay open for his direct word: O3, item 7's count (FR-020, EC-032); O5,
> item 9, #19 round (j)'s reading of the work-tree probe (FR-007); O8, the
> locked stale form; O9, the parity case where the working directory's realpath
> fails (FR-026); and O10, LQ-15's extension (FR-043). A sixth, O11, the
> `core.worktree` read's exit 1 (A1's held item 11; FR-007, FR-008, EC-012,
> User Story 8 and the discovery-identity checklist's CHK009), is a plan item
> added in its revision 3 at `664461f`, after his word, and he has not answered
> it. They are choices for change 2. A1's ordering rule (its
> `proposal.md:1278-1284`) is the four LQ items' and reaches O10 (LQ-15's
> extension) and O5 (item 9, owed under it); O1, O2, O4, O6 and O7 (items 2, 6,
> 8 and 10) rest on his word for change 2 and on #19's rounds, and reach A1 in
> the same re-alignment commit, which follows #19's ratification, he reviewing
> the final text before #34 merges; the open O3 and O8 (items 7 and 10), O11's
> part 2 (item 11) and, should he take (C) (the overview follows feature 004,
> the plan's R20 O9 (C)), O9 wait on his word for change 2 too, and O11's part
> 1 is a text re-alignment on a lane finding for his review.

In this entry's terms: D5's clause 2 was carried by O6's text at `7af798a`
("and, where the warning and the remedy cannot both fit (only beside O4
(a)'s remedy), leaves the recommendation out and shortens the remedy",
research.md:789-792 there, under "the draft recommends parts 1 and 2"),
and it reverses ratified D5's "remedy kept whole" for that one case. Each
open item carries the lane's recommendation (O3 and O8 to O10 as put to
him in lane 4's pane, O5 as the lane's NOTED correction records it), and
O11 is R9's lane finding. So the implementation builds a chosen option once
A1's re-alignment lands at PR #34, and until then the ratified text stands.
Each item stays isolated to one table row, one decider, one count term or
one branch of the composer, so that an answer, or a change in his review of
the final text, lands without touching the rest; the one exception is
O11's part 1 (B), which would also re-word a scenario (O11).

PR #19 is read at `88d0d36`, its round (o) (R-349), whose specs equal its round
(n)'s, `2250830`; the implementation re-pins at #19's ratified head (R1). Every
warning below is in round (n)'s words (`#19 design.md:1349-1369` at `88d0d36`;
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
  below). Until then: A1's ratified texts.
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
  R2-LOW-2). Design: one detector, comparing the main worktree's toplevel with
  the first registry record's canonical path; one remedy row, "core.worktree or
  core.bare redirects the main worktree; unset both in the repository's config,
  or in the main worktree's config.worktree, then run again" (152 characters);
  +1 in `estimated` per repository whose main worktree is no Git candidate
  (R14); and the composer's clause 2: where a `stale-worktree` message carries
  O6's warning (109 characters with its period) beside this remedy, the two
  cannot both be kept within 200 characters (109 + 2 + 152 = 263), which
  happens through (a)'s new row and through sub-item (c)'s row, which carries
  the same remedy. Clause 2 leaves the recommendation out and shortens the
  remedy with `...`, reversing ratified D5's "remedy kept whole" for that one
  case: "a row's path could not be read, so do not run git worktree prune, git
  worktree remove or git gc until it can.; core.worktree or core.bare redirects
  the main worktree; unset both in the repository's..." (200 characters).
  Without it, D5 prints "Review and prune stale worktree metadata ma..." and
  the remedy whole, the prune advice with no warning. Clause 2 is chosen only
  through O6's text at `7af798a` and is before him for his direct word (the
  paragraphs above); until he answers, it rests on that text, and either answer
  edits that one branch. Until then: A1's ratified behaviour, a suggestion that
  `project clean` will refuse, the detector off.
- **O6. Item 10 part 1, the stale warning**. CHOSEN (A): the overview's
  stale message carries the warning while a row's path cannot be read,
  keeping the warning whole and shortening the advice to fit 200
  characters. His "R-320: yes" ruled T6 for PR #19 only and does not
  reach A1 by reference, since #19's ladder is a function of the row's
  evidence alone (PCL:166) while T6 depends on other rows (the draft's
  item 10, lane openRepoProject-3's W86 NM3-1); C-72 chose it for change 2.
  The text: "Review and prune stale worktree metadata manually; a row's path
  could not be read, so do not run git worktree prune, git worktree remove
  or git gc until it can." (160 characters). Design: one message-table
  condition, the overview's own trigger, any worktree row of the same
  repository with `present: null` (#19's T6 fires on any row of its plan,
  `#19 design.md:1349-1369`, and the overview has none), and the
  composer's clause 1: the warning kept whole and the recommendation before
  it shortened, which keeps D5's "remedy kept whole". Beside the
  report-cap remedy (75 characters at 260 rows) the message would be 237
  characters, and D5's rule alone would cut inside the warning; under
  clause 1 it is 200, the recommendation keeping 9 of its 49 characters
  (8 from 1,000 rows, 7 from 10,000). Beside the bare repository's
  ratified remedy (45 characters) it would be 207; under clause 1 the
  recommendation keeps 39. The beside-the-redirect case is O4's clause 2.
  Until then: A1's one stale text, "Review and prune stale worktree
  metadata manually."
- **O7. Item 10 part 2, the `main-worktree-missing` remedy**. CHOSEN, with
  O6: under the same test, "restore or prune the main worktree by hand; a
  row's path could not be read, so do not run git worktree prune, git
  worktree remove or git gc until it can" (152 characters; the finding's
  message 182). Design: one message-table row; it carries no gate, so no
  cut. Until then: "restore or prune the main worktree by hand".

### Open, for his direct word

- **O3. Item 7, the identity re-read in `estimated`** (FR-020; EC-032).
  Take: +3 per Git candidate whose identity probe prints other than two
  lines; leave (as ratified): no term. The lane's recommendation: take.
  Design: one term in R14's sum; `performed` counts the re-reads either
  way, and A1 design D3's "adds no child" is reworded either way (text
  only).
- **O5. Item 9, the work-tree probe's output** (FR-007; LQ-11). As
  ratified: output that is not exactly one line disagrees; PR #19's round
  (j): the output less its final line feed is one path. The lane's
  recommendation: round (j)'s reading. Design: one decider
  `work_tree_output()`; a linked worktree whose path holds a line feed, in
  a repository whose extension is true, is the test either way.
- **O8. T7's locked form**. "A locked stale worktree: should the
  overview's message be (A) `project clean`'s locked text, 'Review, unlock
  it, then prune stale worktree metadata manually.', with the same
  warning, or (B) the one stale text for every stale row, as A1 is
  ratified?" The lane's recommendation: (A). The text is feature 004's
  (lane openRepoProject-3's W52 F-10; `TEXT`, `:877`); round (n) states T7
  as the report row's recommendation alone, since #19's preview excludes a
  locked stale row as `locked-worktree` (`#19 design.md:1349-1369`), and
  the overview's finding is that row's text. Under (A), with O6's warning,
  it is 173 characters, and beside the report-cap remedy clause 1 keeps 9
  of its 62-character recommendation. Design: one message-table row keyed
  on `locked`.
- **O9. M1, parity when the working directory's realpath fails** (FR-026;
  C-61). "When the working directory's realpath cannot be read, the
  overview marks only merged rows `inspection-error`, but `project clean`
  marks every present row so. Should (A) the overview keep its ratified
  rule and the parity tests leave this case out, (B) feature 004 follow
  the overview, or (C) the overview follow feature 004 (an amendment of
  change 2)?" The lane's recommendation: (A). Design: (A) none, the parity
  tests naming the case (R18); (B) none in the overview, and the case
  returns to the parity tests; (C) one branch of the classification step,
  every present row `inspection-error`.
- **O10. LQ-15's extension** (FR-043; EC-036). "You ratified
  `relative-config-path` with exit 2 in 'ratify 34'. One point stays open
  with #19: lane 2's extension of the test to `GIT_CONFIG_GLOBAL` and
  `GIT_CONFIG_SYSTEM`. Keep it (A), or strike it (B), in which case the
  overview drops those two names with `project clean`?" The lane's
  recommendation: (A), keep. The code and its exit are ratified; only the
  two names are open. Design: none in the overview, which calls
  `relative_config_paths` (`:977`); under (B) feature 004's
  `CONFIG_PATH_EXTENSION` (`:974`) loses them.
- **O11. The `core.worktree` read's exit 1** (FR-007, FR-008, EC-012, User
  Story 8 and the discovery-identity checklist's CHK009, as C-72 lists them; A1
  design D3, case 3; R9), on a lane finding: lane openRepoProject-3's W100
  LOW-A, through the lead's R-336, which gives PR #19's row 4b, the same key's
  read, "an exit 1 with nothing printed is the key unset, and any other
  failure, an exit 1 that printed anything included, makes the main worktree
  unreadable, so the run is refused `target-not-repository-root`" (`#19
  design.md:513-517`). In ratified A1 the requirement (A1:130-135) and the
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
  #19 refuses the run? (A) yes; (B) no gate code. The lane's recommendation:
  (A) for both. Design: one decider, `core_worktree_value()`, and one exception
  row. Part 1 is built now, as the plan's reading of a conflict in ratified
  text (R9), since only so does the scenario's own test pass. Under part 1 (B)
  the decider would make the unset key's exit 1 `probe-failed` and, by the rule
  that a failed read names no root, leave the root null with no suggestion, so
  A1's scenario "A separate git directory" and spec 005's User Story 8 scenario
  1 would fail on Git 2.43; (B) therefore costs more than that decider and its
  tests: an amendment of change 2 re-wording that scenario and FR-008's
  sentence on the unset key, or else a different rule for a failed read. Part 2
  is built as (B) until his word: `probe-failed`, the root null, no suggestion
  and no gate code. Under part 2 (A), the lean, every finding that would
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

### Lengths

Measured by `lengths3.py`, a script outside this repository, over the
strings as the contract quotes them, each warning checked against PR #19's
text at `2250830` (unchanged at `88d0d36`, and equal to feature 004's
`TEXT` at `d6bac50`) after its whitespace was normalised. D5's cut to n
characters keeps n - 3 and adds `...`; clause 1 cuts the recommendation to
what 200 leaves beside the warning and the remedy; clause 2 cuts the
remedy to what 200 leaves beside the warning. "Old" is the warning before
round (n), "so do not run git worktree prune until it can".

- The warning alone, with its period: 78 -> 109.
- T6, the stale text with the warning (O6): 129 -> 160.
- T7's locked form with the warning (O8 (A)): 173.
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
  worktree's config.worktree, then run again".
- O1 (A), unchanged by round (n): the merged worktree's text beside
  `unstarted-branch`, 200 with the own text cut to 59 of 67 ("This clean,
  merged, non-current worktree may be removed exp..."); beside
  `reflog-unavailable`, 200, uncut.
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

- **Recorded, no design impact**: F-1's (b) beside an unread row, still
  not ruled in PR #19 (`#19 design.md:2216-2221` at `88d0d36`), reaches no
  overview text, since A1 mirrors none of F-1's texts; T8, clean's
  always-on cap warning, now "if a worktree's path cannot be read, do not
  run git worktree prune, git worktree remove or git gc until it can",
  reaches no A1 site, since the overview's two `inspect-cap` remedies are
  its own and name no prune; and FR-051 applies only if he accepts feature
  004's T123 departure, else the sentence moves to a separate small change.

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
