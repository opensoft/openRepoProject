Lane: openRepoProject-4

# Research: Project overview

The Technical Context in [plan.md](plan.md) has no NEEDS CLARIFICATION. The
ratified change `add-project-overview` (landed as `961c405`), its amendment
A1 (PR #34 at `e4a30fc`, ratified by Brett Heap's "ratify 34" on
2026-10-22) and [spec.md](spec.md) with its 71 clarifications decide almost
every behaviour, and they govern. These entries settle what they leave to the
plan, and isolate what only Brett Heap can still decide:

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
- R20: the held items, each OPEN for Brett Heap with the design of each
  answer (decision 2);
- Revision 2: where each finding of lane openRepoProject-3's W96 read is
  taken.

Each entry gives a Decision, its Rationale and the Alternatives considered.
Citations, as [plan.md](plan.md) "Citations" defines them: `project:N` is
line N of feature 004's `project` at `0a82a62` (branch
`004-project-clean-all-safe`, draft PR #33), read with `git show
0a82a62:project`; `A1:N` and `A1 design.md:N` are lines of change 2's
`specs/project-overview/spec.md` and `design.md` at `e4a30fc`; `PCM:N`,
`PCL:N` and `#19 design.md:N` are lines of change 1's
`specs/project-command/spec.md`, `specs/project-clean/spec.md` and
`design.md` at PR #19's `20084cd`; POD, PRSD, CMD, CLN and DI are as
[spec.md](spec.md) defines them. Revision 1 moved every cite from
`4b4c36b` and `ccc52b9` (R1); revision 2 moved none. Nothing here was run
against a repository: the plan step ran no `project` and no owner tool
(R18).

## R1. Authority, pins and re-pins

- **Finding**: C-56 (Q2 A) and A1's task 1.7 set the plan after feature 004
  merges into `main`, on Brett Heap's word given after that merge; spec 005 at
  `7af798a` (its commit 3ae) now records in C-56 and its Status that his word
  below moved that order for the plan step. Feature 004 has not merged: PR #33
  is a draft, its branch at `0a82a62`. Brett Heap said, at
  2026-10-22T19:46:57Z, "lane 4 plans 005 now".
- **Decision**: that word moves C-56's order for this plan step only, as his
  "lane 4 specifies 005 now" moved change 2's order for the specify step
  (C-21). It authorizes this plan and nothing after it: no `tasks.md`, no
  code and no test is written, and the tasks and the implementation each
  wait for his word (R2). This plan pins its reads at:
  - feature 004's `project`, tests and documents at `0a82a62`;
  - PR #19's change 1 at `20084cd`, its round (m), accepted by lane
    openRepoProject-2 (R-323), with T1 to T8 confirmed by Brett Heap
    ("R-320: yes" for T6 to T8);
  - A1 at `e4a30fc`;
  - #24's change at `fe5b245` (PR #27 at `04be7f6`, its round B21; its
    eight pinned ranges identical by the lead's `cmp`, and its
    `project-overview` block blob `a40458cb` at `fe5b245` and `04be7f6`
    alike) and #25's at `05a424a` (PR #29 at `a529310`), both read only to
    confirm that neither gates this feature (C-71).
- **Re-pin of revision 1, feature 004**: `0a82a62` is three merges after
  the first draft's `4b4c36b`: `7e0a61e` (`impl/004-codex-closed-stdout`,
  R-322: a `--json` apply run whose standard output was closed at startup
  refuses before any removal, in `check_writes`, `:3770-3801`), `12c1821`
  (`impl/004-r320-stale-cap`: T6 and T7 as `TEXT` rows `:873-878` with
  `stale_recommendations`, `:4362-4382`, and the preview's
  `UNREAD_NEXT_STEPS`, `:5486-5490`; T8 in `remedy_inspect_cap`,
  `:795-797`) and doc round 21. Every `project:N` cite here was moved by a
  line map of the two files and spot-checked by text: no definition the
  overview reuses changed but in its line, the runner (`:1111-1972`), the
  parsers (`:1974-2241`) and `Invocation` among them byte for byte, and
  `row_evidence` (`:3224`) only in its docstring. None of the three merges
  reaches the overview's texts: its stale and cap texts stay A1's (R20, O6
  and O8), and it calls neither `check_writes` nor `stale_recommendations`.
- **Re-pin of revision 1, PR #19**: `20084cd` leaves
  `specs/project-command/spec.md` byte-identical to `ccc52b9` (by `cmp`),
  so PCM cites stand; `specs/project-clean/spec.md` gains a five-line AND
  at PCL:1099-1103, after PCL:1098 (T8 in "Row cap and planning
  failures"), so a PCL line after 1098 moves down 5 (this plan cites
  none); its design carries T6 and T7 at `#19 design.md:1337-1350` and T8
  at `:1440-1446`, and F-1's (b) stays OPEN in its Open Questions at
  `:2187-2192`.
- **Re-pins still due**: after PR #33 merges, the implementation re-pins
  against that `main`, as C-56 asks; a later head of feature 004 before
  then (lane openRepoProject-2's R-332, R9) is re-cited the same way
  before `tasks.md` is written.
- **Rationale**: the plan's design depends on feature 004's runner, parsers
  and deciders, which are complete at `0a82a62` (133 of 133 tasks were
  ticked at `2cf34d3`, the spec's re-check); writing it now costs at most a
  re-cite, while C-56's risk, a second plan, is bounded by R3's reuse list,
  which names every interface the plan leans on.
- **Alternatives considered**: waiting for PR #33 (C-56 as written),
  overtaken by his word; pinning at `2cf34d3`, the spec's re-check head,
  rejected because `0a82a62` is the branch head the lead named and carries
  the later fixes.

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
     items on his word;
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
  unchanged (`project:N` at `0a82a62`; R1):

  - timing: `TIMING` (`:560-570`): deadline 60, probe budget 5, grace 2,
    reap wait 2, tick 0.1;
  - contracts: `LIMITS` (`:589-600`), for the shared constants and the
    record bounds; `GIT_FLOOR` (`:602`); the `TEXT` rows the contract
    names;
  - git environment: `GIT_SCRUB` (`:1034-1046`, 31 names), `TRACE2_OFF`
    (`:1054`), `PROTOCOL_PINS` (`:1058-1063`), `STATUS_PINS`
    (`:1070-1071`), `GIT_KINDS` (`:1076-1089`; kinds `probe` and `status`
    only), `git_env` (`:1092`), `git_argv` (`:1105`),
    `relative_config_paths` (`:963`), `config_path_message` (`:1003`),
    `home_directory` (`:981`), `expand_user` (`:992`);
  - runner: `ChildHandle` (`:1131-1265`), `LIVE_PROBES` (`:1124`),
    `kill_live_probes` (`:1268-1287`), `Interrupted` and `Terminated`
    (`:1296-1314`), `Invocation` (`:1323-1438`, one branch added),
    `signal_scope` (`:1478`), `raising_signals` (`:1548`),
    `signal_wakeup` (`:1624`), `RawOutput` and `DriverOutcome`
    (`:1643-1693`), `git_version` (`:1945`);
  - parsers: `ParseError`, `RecordStream`, `StatusParser`,
    `WorktreeListParser`, `RefParser` and `MergedSetParser`
    (`:1975-2213`);
  - escaping: `escaping_decode`, `json_path` and `human_path`
    (`:2250-2316`);
  - evidence: `RECOMMENDATIONS` and `SECOND_RECOMMENDATIONS`
    (`:2328-2348`), `classify` (`:2351`), `IDENTITY_OPTIONS`,
    `REF_FORMAT`, `STATUS_PROBE`, `GITFILE_BYTES` and `HEAD_BRANCH_REF`
    (`:2563-2575`), `WorktreeRow` (`:2578`), `git_operation`,
    `unparseable_error`, `probe_error` and `os_error` (`:2616-2661`),
    `_direct` (`:2679`), `presence_from_lstat` (`:2699`), `gitdir_line`
    (`:2764`), `main_worktree_decision` (`:2824`),
    `registration_verdict` (`:2909`), `verify_registration` with
    `fs=_direct` (`:2946`), `status_warned` (`:2980`),
    `WORK_TREE_PROBE` (`:3019`), `shared_paths` (`:3182`),
    `shared_identities` (`:3192`), `row_evidence` (`:3224`) and
    `resolve_merge_target` (`:2503-2543`), change 1's resolver, called as
    below;
  - guard: `observed_at` (`:3536`);
  - dispatcher: `divert_stream` (`:3719`), `write_failed` (`:3743`) and
    `advise` (`:3818`);
  - reflog: `reflog_path` (`:5034`) and `reflog_outcome` (`:5047`).

  Changed, without changing any behaviour of feature 004 (its tests pass
  unchanged, FR-049):
  - `Invocation.__init__` (`:1346-1360`) gains one branch: for `overview`,
    `work_end` and `reserve_end` are both the start plus
    `TIMING["invocation_deadline"]`, so `child_budget()` gives
    `min(5 s, deadline - now)` with no reserve (FR-011);
  - `run_bounded` (`:1751-1880`) is factored into `start_child()` (budget,
    spawn, count, budget end; `:1775-1795`) and `conclude()` (the outcome
    from the handle's state and the parser; `:1864-1879`), as R-54's X-2
    leaves to this feature, keeping its `feed_stderr` and `tick` hooks; the
    one-wide loop stays in `run_bounded` between them;
  - `parser()` (`:7788`) gains the `overview` subparser and `main()`
    (`:7843`) one dispatch line, placed before its fall-through `return
    inspect_project(args)` (`:7861`). Every `Exception` of an overview run
    is mapped inside its own entry point (R15), so `main()`'s `(Refused,
    OSError)` handler keeps its behaviour for every other subcommand; the
    `BaseException`s, `Interrupted` and `Terminated` (`:7870-7873`) and
    `KeyboardInterrupt` (`:7874-7876`), reach `main()`'s existing
    handlers, which print `Cancelled.` and return 128 plus the signal, as
    they do for `clean`.

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
    deadline-stopped marker, `deadline_stopped`, `:4316`). Check: a
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
    its 10 s reserve untouched: the `clean` branch (`:1353-1355`) is not
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
    design.md:212-217`; D9, the removal child, `:628`; D14, the fit
    arithmetic, `:974`), feature 005's spec says so and PR #19 is not
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
- **Not reused**: `run_bounded`'s loop, `fs_call` (`:1882`), `_fs`,
  `_lstat` and `_realpath` (`:2664-2724`), `identity_probe` (`:2735`),
  `worktree_config` (`:3022`), `effective_work_tree` (`:3039`),
  `inspect_repository` (`:3070`), `_read_row`, `_identity_unchanged`,
  `_read_status` and `worktree_rows` (`:3306-3512`), `read_reflog`
  (`:5114`), `declared_tracking_branch` (`:2426`) and `projects_dirs`
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
  name passed in, and its caller reads that name (`:3167-3169`). The
  overview calls it on the keep-filter's records, which hold every record
  it reads (the local heads and `refs/remotes/origin/HEAD`, `:2517-2529`),
  with `declared` the manifest's `tracking_branch` as a string, or None
  for a manifest shown absent or read with none. FR-025's other branches
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
  scrub, `TRACE2_OFF` and the seven protocol pins (`GIT_KINDS`, `:1076`);
  it starts no `removal`, `delegate` or `push` child and calls no
  `execute()`; it writes no file; and it calls no function of the plan,
  preview, apply, result or push regions. A test asserts every child's
  argument vector against an allow-list of the overview's subcommands
  (R18).
- **Rationale**: one evidence model is the change's point ([E]); the
  deciders were split out of feature 004's readers for exactly this caller
  (its R-54 X-1; the evidence region's comment at `:2552-2558` names
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
  rule, `:1268-1287`). On deadline expiry it terminates every in-flight
  child at once and refuses every later start (FR-012). The run is entered
  under `signal_scope()` (record-only handlers, FR-044); the loop raises
  `Interrupted` (a `BaseException`, `:1296`) once the slot is set, and its
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
  which the handlers write to (`signal_wakeup()`, `:1624-1627`), and the
  loop's own task pipe, which the workers write to (R7). `signal_scope`
  keeps its pipe's write end private (`:1478-1541`), so the handlers cannot
  write to the task pipe without a change to feature 004's signal code.
  The behaviour D1 asks for, any signal or finished task waking the loop
  at once, holds; no spec line changes. Neither the packet nor spec 005
  names a pipe, so a reader of A1 finds this choice only here; the record
  line for spec 005's Dependencies or the A1 draft's lane-findings group
  (text only, the lead's call): "D1's one self-pipe is realized as two
  read ends on one selector, `signal_scope`'s wakeup pipe and the loop's
  task pipe; behaviour unchanged (plan R4)."
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
  `:2563`; EC-032); for the first candidate of a repository, that
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
- **The manifest's place**: FR-021 lists the manifest read before the
  repository's probes, and A1 design D9 needs it before the ref listing,
  whose keep-filter takes its `tracking_branch`. The plan reads it at
  `repository.root` once that is named (after the identity probe where the
  candidate is the main worktree, else after the registry listing and
  design D3's steps), always before the ref listing (design D9), or at the
  candidate for a row without Git; row errors keep that step order. In D3
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
    (j); R17);
  - one per linked row whose work-tree probe ran: the strict realpath of
    the toplevel it printed, compared with the row's;
  - one per reflog read (at most 64 KiB, `reflog_path`, `:5034`);
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
  overrides `_take` (`:2171-2189`): it parses each record as `RefParser`
  does, then keeps it only if it is a local head (`refs/heads/`), is
  `refs/remotes/origin/HEAD`, or is the upstream that a kept head names;
  for every other `refs/remotes/<remote>/<name>` record it sets the
  remote-copy flag of `<name>` when `<name>` is one of the candidate names
  known before the listing (the manifest's `tracking_branch` less
  `origin/`, `main`, `master`) and keeps nothing else. `for-each-ref
  refs/heads refs/remotes` (`:3160`) sorts by refname, so every head and
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

- **The extension read** (FR-007): `true` is true and `false` false; exit 1
  with nothing on either stream is false with no error; any other outcome
  is true with the row error change 2's table gives (`probe-failed`, its
  DETAIL `unparseable output` for other output; `probe-timeout`;
  `deadline-exceeded`). A1's proposal says so of that exit 1 with a
  warning: it "stays a failure that counts as true" (A1 `proposal.md`
  :1370-1375). Feature 004's `worktree_config` (`:3022-3036`) still reads
  every exit 1 as false at `0a82a62` (`return outcome.status != 1`,
  `:3036`); lane openRepoProject-2's R-332 has it follow PR #19's D7, "an
  unset value is false and any other failure counts as true" (`#19
  design.md:484-485`), a fix queued for feature 004's next window. The only
  exit 1 with a warning is a common `config` that cannot be read, where the
  identity probe and the registry listing already fail (exit 128, measured
  on Git 2.43.0 and 2.36.6 by lane openRepoProject-3's W96), so no class
  differs in either reading. The one difference from #19 is the
  `probe-failed` row error that A1's table records on the project row
  (A1:369), ratified, which gates nothing and makes the run incomplete
  (exit 1). The A1 drafter and W96 each found no held A1 item in it, so
  nothing joins R20.
- **Realpaths**: the overview's tasks use `os.path.realpath(...,
  strict=True)`, so `ENOENT` and `ENOTDIR` can be told from other errors
  as FR-007 and FR-026 need; feature 004's `_realpath` (`:2723`) is not
  strict, and never raises.
- **An abandoned child**: feature 004's `conclude()` path maps an abandoned
  handle to `timeout` (`:1868-1869`), as [E] has it (PCM:263-269); FR-011
  makes an abandoned child that the deadline cut `deadline-exceeded`. The
  overview's loop maps that case itself after `conclude()`.
- **The deadline's text**: `OPERATION stopped at the invocation deadline`
  (A1's table), not feature 004's "work deadline" (`:894`).
- **`tracking_freshness`**: the overview's own constant, `local refs only;
  no fetch` (FR-036; C-32), not feature 004's `TRACKING_FRESHNESS`
  (`:4226`).
- **The work-tree probe's output**: "not exactly one line" disagrees, as A1
  is ratified; PR #19's round (j) and feature 004 (`:3039-3067`) read one
  path less the final line feed. Held as R20's O5.

## R10. Discovery details (FR-001 to FR-005; PN-9, PN-13)

- **Decision**:
  - Roots come from `--root` (repeatable), else `PROJECTS_DIR` when set and
    not empty, else `~/projects` and `~/Projects`: the strings
    `projects_dirs` (`:114-122`) selects, with its empty `PROJECTS_DIR`
    read as unset, made with `expand_user` (`:992`) and `home_directory`
    (`:981`) and canonicalised in the root task, never by `projects_dirs`
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
    (POD:46, A1:51) is narrower than DI:142; FR-005's wording is the
    spec's to change (lane openRepoProject-3's W96, LOW-7).
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
  contract's message table, keyed by code and condition, held items marked;
  [L]'s recommendations are read from `RECOMMENDATIONS` and
  `SECOND_RECOMMENDATIONS` (`:2328-2348`), never from `row_evidence`'s two
  overrides (`:3295-3298`), which are feature 004's report texts. PN-1's
  sentences are fixed in the contract, each under 200 characters, from
  texts feature 004 already prints where one exists (`no-merge-target`,
  `:883`; `merge-target-conflict`, `:842-843`; `main-worktree`, `:864`). The
  message of a gated finding is built by one pure function,
  `compose_message(own, remedy, warning=None)`: own text, `; `, remedy,
  within 200 characters, the own text shortened with `...` when both do not
  fit (A1 design D5). The draft's two held clauses are branches of that
  one function, reached only when `warning` is given: clause 1, keep the
  warning whole and shorten the recommendation before it (item 10 part 1,
  R20's O6), and clause 2, where the warning and the remedy cannot both be
  kept, leave the recommendation out and shorten the remedy, a reversal of
  ratified D5's "remedy kept whole" that only item 8's redirect remedy
  reaches (R20's O4). The function is tested by length tables alone, with
  both answers of each held item.
- **Rationale**: a held text then lands as a one-row change, and the cut
  rule, which items 2, 8 and 10 all touch, sits in one testable place.

## R13. A finding's `observed_at` (PN-7)

- **Decision**: the wall-clock completion time of the last step whose
  result the finding's decision read: a Git child's end, or a filesystem
  task's end (a reflog gate, a registration or presence read). A finding
  decided by two sources (a manifest and the ref listing for
  `merge-target-conflict`; a status probe and the ref listing for a
  default-branch finding) takes the later. RFC 3339 UTC to the second, as
  `observed_at()` (`:3536`) writes it.
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
  than two lines) is held, R20's O3.
- **Rationale**: FR-020 counts the children a run expects; a row that takes
  no status probe is expected to start none.

## R15. JSON form, error outputs and the writer (PN-6; PN-2; FR-039, FR-044)

- **Decision**:
  - The document is `json.dumps(doc, indent=2, ensure_ascii=True)` and one
    line feed, keys in the order the contract lists them (the delta's
    order), never sorted (PN-6), as feature 004's `write_document`
    (`:3601-3623`) writes its own.
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
    abandoned every child; then, inside `raising_signals()` (`:1548`),
    entered inside the run's `signal_scope`, it is written by `os.write`
    on the standard-output descriptor, so nothing is buffered for exit to
    flush (C-69). An interrupted or failed write diverts the descriptor
    (`divert_stream`, `:3719`). Where standard output has no descriptor
    (an in-process test), the stream's `write` is used.
- **Rationale**: one rendering step makes C-66's "rendered whole before its
  first byte" and C-69's raising span hold together; `os.write` leaves
  nothing for the interpreter to flush after a signal.
- **Alternatives considered**: `sys.stdout.write` then `flush`, which can
  leave buffered bytes for exit; feature 004's `internal_error` text,
  `TYPE: TEXT` (`:3541`), rejected because A1's table names the class only.

## R16. Human report details (PN-3; PN-5)

- **Decision**: D10's layout and fixed lines exactly (the contract); count
  nouns stay as D10 fixes them for every count, `1 projects` and `Scanning
  1 roots...` included (PN-5), since FR-045 and SC-010 read D10's lines
  character for character; the `--help` texts are fixed in the contract
  (PN-3).
- **Alternatives considered**: singular forms for one, a change to D10's
  fixed lines that only an amendment of change 2 could make.

## R17. FR-007's re-verification against feature 004's fix (PN-18)

- **Finding**: feature 004's R-101 fix is built at `0a82a62` as
  `_identity_unchanged` (`:3347-3377`): one bounded call re-reads the
  `lstat`, the realpath and the registration, and a changed value, a
  failed read or a cut stops the status probe. Compared with FR-007:
  - the class is `inspection-error` in both for every outcome, so no class
    differs and nothing goes to the lead under PN-18;
  - a re-read `lstat` failing with `ENOENT` or `ENOTDIR` appends an `os-error`
    in feature 004 (`_direct`, `:2679-2687`), while FR-007 counts it as a
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
    ambiguity warning causes (`status_warned`, `:2980`).
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

## R20. The held items: OPEN for Brett Heap (brief decision 2)

Each is isolated to one table row, one decider, one count term or one
branch of the composer, so that either answer lands without touching the
rest. "As ratified" is what the implementation builds until his word. The
lane's A1 re-alignment draft is the source of each option: items 1 to 7
and 9 as read at sha256 `00205d73ba38...` (2,295 lines), items 8 and 10 as
read at `8ce4e9fb60e83cc2...` (2,422 lines), where item 8 gains "D5 beside
this item's remedy" and item 10 keeps D5's first clause only. Items 1, 3, 4
and 5 there change text only and have no design impact. Each question below
is lane openRepoProject-3's W96 wording, with its section 7 correction.

- **O1. Item 2, the reflog remedies' submodule clause** (FR-035). "Should
  the overview's two reflog remedies end with ' (--force if it holds a
  submodule)', as `project clean`'s next steps now do (#19 round (g))? (A)
  yes; the merged worktree's own text is then cut to 59 of its 67
  characters beside `unstarted-branch`. (B) no; keep A1's ratified texts."
  The draft leans (A); as ratified, (B). Design: two rows of the remedy
  table; under (A) the `reflog-unavailable` message is exactly 200
  characters. The length tests carry both answers.
- **O2. Item 6, the deadline's cut at the reflog gate** (FR-034). "You ruled
  this for `project clean` on 2026-10-22, 'O-1: deadline-exceeded' (R-263).
  Should the overview's suggestion gate do the same? (A) yes: a reflog read
  the deadline cuts withholds with `deadline-exceeded`; (B) no:
  `inspection-incomplete` for both cuts, as A1 is ratified." His ruling
  reaches PR #19 only; the draft and lane openRepoProject-2 lean (A).
  Design: one branch in the repository gate, keyed on the cut's limit,
  which the filesystem task already records.
- **O3. Item 7, the identity re-read in `estimated`** (FR-020; EC-032). Take:
  +3 per Git candidate whose identity probe prints other than two lines;
  leave (as ratified): no term. Design: one term in R14's sum; `performed`
  counts the re-reads either way, and A1 design D3's "adds no child" is
  reworded either way (text only).
- **O4. Item 8, the redirected main worktree** (FR-006; R-271, a lead
  ruling of lane openRepoProject-2's). "Where a main worktree's own
  `core.worktree` or `core.bare` redirects it, `project clean` refuses the
  checkout. Should the overview (a) give no clean suggestion, with a new
  remedy naming the redirect (one more Git child per such repository), (b)
  report it as an `unsupported-layout` error, or keep A1's ratified
  behaviour, a suggestion that `project clean` will refuse? With (a) or
  (b): should a bare entry whose path plus `/.git` is the common directory
  (the draft's sub-item (c)), and a main-worktree probe that exits nonzero
  (sub-item (d)), count as a redirect too? (yes / no each). With (a) or
  (b), where the warning and the redirect remedy cannot both fit, should
  the advice be left out and the remedy shortened?" The draft recommends
  (a). Design: one detector, off as ratified, comparing the main
  worktree's toplevel with the first registry record's canonical path; one
  remedy row, "core.worktree or core.bare redirects the main worktree;
  unset both in the repository's config, or in the main worktree's
  config.worktree, then run again" (152 characters); +1 in `estimated` per
  such repository whose main worktree is no Git candidate; and the
  composer's clause 2, held here: where a `stale-worktree` message carries
  O6's warning (78 characters with its period) beside this remedy, the two
  cannot both be kept within 200 characters (78 + 2 + 152), which happens
  under (a) through its new row and under (b) through sub-item (c)'s row,
  which carries the same remedy. Clause 2 leaves the recommendation out and
  shortens the remedy with `...`, reversing ratified D5's "remedy kept
  whole" for that one case; without it, D5 prints "Review and prune stale
  worktree metadata ma..." and the remedy whole, the prune advice with no
  warning. Clause 2 fires only when O4 takes (a) or (b) and O6 takes (A).
- **O5. Item 9, the work-tree probe's output** (FR-007; LQ-11). As
  ratified: output that is not exactly one line disagrees; PR #19's round
  (j): the output less its final line feed is one path. Design: one
  decider `work_tree_output()`; a linked worktree whose path holds a line
  feed, in a repository whose extension is true, is the test either way.
- **O6. Item 10 part 1, the stale warning**. "Should the overview's stale
  message carry the warning while a row's path cannot be read, keeping the
  warning whole and shortening the advice to fit 200 characters (A), or
  keep A1's one stale text (B)?" Held for his word for this change: his
  "R-320: yes" ruled T6 for PR #19 only, and it does not reach A1 by
  reference, since #19's ladder is a function of the row's evidence alone
  (pcl:164) while T6 depends on other rows, so A1's reference to the
  ladder still carries its one stale text (the draft's item 10, lane
  openRepoProject-3's W86 NM3-1). The draft recommends (A). Design: one
  message-table condition, the overview's own trigger, any worktree row of
  the same repository with `present: null` (#19's T6 fires on any row of
  its plan or listing, `#19 design.md:1337-1350`, and the overview has
  neither), and the composer's clause 1: the warning kept whole and the
  recommendation before it shortened, which keeps D5's "remedy kept
  whole". T6 is 129 characters; with D5's rule alone, beside the
  report-cap remedy (75 characters at 260 rows), the message would be 206
  characters and the cut would fall inside the warning, while under clause
  1 it is 200, "Review and prune stale worktree metadata...; a row's path
  could not be read, so do not run git worktree prune until it can.; 260
  rows exceed the report's row cap of 256; the report would be
  incomplete". The beside-the-redirect case is O4's clause 2.
- **O7. Item 10 part 2, the `main-worktree-missing` remedy**. Held for his
  word for this change, as part 1 is. Under the same test: "restore or
  prune the main worktree by hand; a row's path could not be read, so do
  not run git worktree prune until it can" (121 characters). As ratified:
  "restore or prune the main worktree by hand". Design: one message-table
  row; it carries no gate, so no cut.
- **O8. T7's locked form**. "A locked stale worktree: should the
  overview's message be (A) `project clean`'s locked text, 'Review, unlock
  it, then prune stale worktree metadata manually.', with the same
  warning, or (B) the one stale text for every stale row, as A1 is
  ratified?" The text is feature 004's (lane openRepoProject-3's W52 F-10;
  `TEXT`, `:865`), with T7's warning at `:876-878`. Design: one
  message-table row keyed on `locked`.
- **O9. M1, parity when the working directory's realpath fails** (FR-026;
  C-61). "When the working directory's realpath cannot be read, the
  overview marks only merged rows `inspection-error`, but `project clean`
  marks every present row so. Should (A) the overview keep its ratified
  rule and the parity tests leave this case out, (B) feature 004 follow
  the overview, or (C) the overview follow feature 004 (an amendment of
  change 2)?" Design: (A) none, the parity tests naming the case (R18);
  (B) none in the overview, and the case returns to the parity tests; (C)
  one branch of the classification step, every present row
  `inspection-error`.
- **O10. LQ-15's extension** (FR-043; EC-036). "You ratified
  `relative-config-path` with exit 2 in 'ratify 34'. One point stays open
  with #19: lane 2's extension of the test to `GIT_CONFIG_GLOBAL` and
  `GIT_CONFIG_SYSTEM`. Keep it (A), or strike it (B), in which case the
  overview drops those two names with `project clean`?" The code and its
  exit are ratified; only the two names are open. Design: none in the
  overview, which calls `relative_config_paths` (`:963`); under (B)
  feature 004's `CONFIG_PATH_EXTENSION` (`:960`) loses them.
- **Recorded, no design impact**: F-1's (b) beside an unread row, open in
  PR #19 (`#19 design.md:2187-2192` at `20084cd`), reaches no overview text,
  since A1 mirrors none of F-1's texts; T8, clean's always-on cap warning,
  reaches no A1 site, since the overview's two `inspect-cap` remedies are
  its own and name no prune; and FR-051 applies only if he accepts feature
  004's T123 departure, else the sentence moves to a separate small change.

## Revision 2: lane openRepoProject-3's W96 read

W96 read this plan at `a80f10b` and, in a delta read, revision 1 at
`aeb0bb2`. Revision 2, made from `7af798a` (spec commit 3ae), takes each
finding, every one checked against the text it cites:

- **HIGH-1**, a second merge-target resolver against A1's Non-Goal (A1
  design.md:73-74): change 1's `resolve_merge_target` (`:2503-2543`) is
  pure, its caller reading the manifest (`:3167-3169`), so the overview
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
- **LOW-12**: R3 cites `:2552-2558` for "another driver".
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
