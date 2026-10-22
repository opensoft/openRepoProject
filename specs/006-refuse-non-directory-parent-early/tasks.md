Lane: openRepoProject-1

# Tasks: Refuse a non-directory parent early

**Input**: Design documents from `specs/006-refuse-non-directory-parent-early/`

**Prerequisites**: plan.md (with its section "qs.sh (exact text)"), spec.md
(with its Clarifications section), research.md (R1 to R14; R5 is the run
inventory), quickstart.md (its twelve check blocks).
The technical design is the ratified change
`openspec/changes/refuse-non-directory-parent-early/`: design.md D1 to D6,
clarifications.md N1 to N6 and the `project-command` spec delta. It governs
wherever a task is shorter; plan.md places what the design leaves to the
realization.

**Clarify answers.** These tasks follow Brett Heap's answers of 2026-10-22 to
the five clarify questions (`clarify-questions.md`), "all recommended":
**Q1 B, Q2 A, Q3 A, Q4 B, Q5 A**, as plan.md does, recorded in the spec's
Clarifications section. Every task whose content, files or verify depends on an
answer carries its tag, `[Q1]` to `[Q5]`, after its tier tag; the tags trace to
those Clarifications. "Appendix A: Options not taken" lists the tasks that
change, appear or disappear for each other option, and it is the list that
governs: where plan.md, research.md or quickstart.md carries fewer answer tags
than this file for the same work, the tags here follow the task's files and
verify (a method count, a tagged subtest count, the scope of a check).
plan.md, research.md, quickstart.md and `qs.sh` are committed together, in the
planning commit, and this file follows in the next commit, before T001.

**Tests**: Required. FR-014 and design.md D3 require automated tests over
temporary fixtures for D3 items 1 to 10, with the new strings pinned as fixed
text, and FR-015 a traceability record that maps each of the delta's 40
scenarios to its tests. Tests come first and are seen to fail against the
unchanged `project` (red first); then the implementation.

**Organization**: The phases follow the order the lane lead set: the
governance record (Phase 0), the baseline and the traceability skeleton
(Phase 1), tests first (Phase 2, closed by the red-first checkpoint task), the
implementation (Phase 3), the checks (Phase 4) and the traceability record
(Phase 5), then the lane lead's numbered "Lane steps". The check runner
`qs.sh` is not a task: it is committed with the plan in the planning commit.
The hand walk at a real terminal and the adversarial review are not tasks
either: a build agent has no terminal, and the lead dispatches the review
itself, so they are lead steps, the first two of plan.md's "Lane steps" and of
this file's, and every task has a command verify. All six user stories are
realized by one read (`parent_case()`) and one head check in `new()`, so they
cannot ship apart: each task carries a story label where it serves exactly one
story, and otherwise names the stories it serves.

## Format: `[ID] [P?] [Story] [Tier] [Q?] Description -- files: -- verify:`

- **[P]**: can run in parallel with the other `[P]` tasks of its phase: its
  files are disjoint from theirs and it depends on none of them. A task with
  no files touches nothing in the worktree.
- **[Story]**: US1 to US6 of spec.md, where the task serves exactly one.
- **[Tier]**: exactly one of `[H]` (`haiku-high`), `[S]` (`sonnet-xhigh`) and
  `[O]` (`opus-xhigh`), dispatched by its agent definition with no `model`
  override. No task here is `[H]`: the repository declares no
  `## Governed invariants` section, and the workflow protocol (Build Tiers)
  gives such a repository no `[H]` tasks (lead's ruling). Appendix B lists the
  tasks that would be `[H]` if one were declared.
- **[Q1] to [Q5]**: the task depends on that clarify answer.
- **files:** every path the task may create, change or delete, relative to the
  worktree root; a task fails if its diff touches any other path.
- **verify:** one command line, run from the worktree root in the foreground
  after the task's own commit, that exits 0 only when the task is done. It is
  self-contained: the Bash tool keeps no shell state between calls, so a verify
  reads no variable that another call defined; a quickstart check runs through
  `qs.sh` (see "Verify note"), and any other value a verify needs is defined
  inside that line.
- The fields are separated by ` -- ` (two ASCII hyphens), the lane's ASCII
  form of the protocol's separator (lead's ruling).

## Path Conventions

One executable, `project`, at the repository root; one test module,
`tests/test_project.py`; documentation in `README.md`; the change's governance
record `openspec/changes/refuse-non-directory-parent-early/tasks.md` `[Q5]`;
feature files under `specs/006-refuse-non-directory-parent-early/` (among
them `qs.sh`, from the planning commit). No other file changes (FR-016 as the Clarifications
narrow it `[Q5]`). Line references are at `d47e8a4`, where `project`,
`tests/test_project.py` and `README.md` are the merge base's; once main is
merged in (lane step 4), cite by function name and re-read the line. Every
line citation is the merge base's: after T004 shifts `tests/test_project.py`,
locate a site by the function or test name the task gives.

## File sets and writers

| Set | Files | Writer |
| --- | --- | --- |
| FS-Q | `specs/006-refuse-non-directory-parent-early/qs.sh` | the lane lead only, in the planning commit with plan.md, research.md and quickstart.md (plan.md "qs.sh (exact text)"); no build task creates or edits it |
| FS-G `[Q5]` | `openspec/changes/refuse-non-directory-parent-early/tasks.md` | one `[S]` writer, copying plan.md "G1 and G2 exact text" (lead's ruling) |
| FS-D | `specs/006-refuse-non-directory-parent-early/traceability.md` | one writer |
| FS-T | `tests/test_project.py` | one writer at a time; T004 to T012 in order, never two at once |
| FS-P | `project` | one writer |
| FS-R | `README.md` | one writer |
| FS-L | `specs/006-refuse-non-directory-parent-early/tasks.md` (ticks) | the lane lead only |

Each task commits alone, with explicit pathspecs (`git commit -m MSG -- PATH
...`), with the lane line `Lane: openRepoProject-1` first in the commit body.
Writers on different file sets share one worktree and one index, so the lead
lets only one of them commit at a time.

## Crosswalk: plan slices to tasks

plan.md's work breakdown names its slices S1, S2, T1 to T9, I1, I2, V1 to V7,
G1 and G2 (a slice id has no zero padding); this file's tasks are T001 to
T028. A task that follows a slice cites it; this table is the one place that
maps them. The runner `qs.sh` is neither a slice nor a task (FS-Q). The two
slices that became lead steps, V8 (the hand walk) and V9 (the adversarial
review), are kept in the table so that a reader of an earlier draft finds
them: plan.md now carries them as its Lane steps 1 and 2. Phases and tiers are
as the lead ruled them (no `[H]` task; V7 in Phase 5); where plan.md's table
differs, this table governs.

| Plan slice | Task | Phase | Tier |
| --- | --- | --- | --- |
| G1 `[Q5]` | T001 | 0 | `[S]` |
| S1 | T002 | 1 | `[S]` |
| S2 | T003 | 1 | `[S]` |
| T1 | T004 | 2 | `[S]` |
| T2 | T005 | 2 | `[S]` |
| T3 | T006 | 2 | `[S]` |
| T4 | T007 | 2 | `[S]` |
| T5 | T008 | 2 | `[S]` |
| T6 | T009 | 2 | `[S]` |
| T7 | T010 | 2 | `[S]` |
| T8 | T011 | 2 | `[S]` |
| T9 | T012 | 2 | `[S]` |
| (none: plan.md "Phase 2 checkpoint") | T013 | 2 | `[S]` |
| I1 | T014 | 3 | `[O]` |
| I2 | T015 | 3 | `[S]` |
| V1 | T016 | 4 | `[S]` |
| G2 `[Q5]` | T017 | 4 | `[S]` |
| V2 | T018 | 4 | `[S]` |
| V3 | T019 | 4 | `[S]` |
| V4 | T020 (ASCII), T021 (fixed text), T022 (README) | 4 | `[S]` |
| V5 | T023 (files changed), T024 (`ast-project`), T025 (`ast-tests`) | 4 | `[S]` |
| V6 | T026 | 4 | `[S]` |
| (none: plan.md "Other lanes", step 1) | T027 | 4 | `[S]` |
| V7 | T028 | 5 | `[S]` |
| V8 | lead step, not a task: Lane step 1, the hand walk | | |
| V9 | lead step, not a task: Lane step 2, the adversarial review | | |

## Verify note: qs.sh and preconditions

"Check `ID`" (plan.md, Work breakdown) names the block of quickstart.md whose
first line is `# check: ID`. A verify that runs one is a single line, run from
the worktree root:

```text
bash specs/006-refuse-non-directory-parent-early/qs.sh ID [NAME=VALUE ...]
```

`qs.sh` (plan.md "qs.sh (exact text)") changes to the top of the
worktree, computes `BASE` as `git merge-base origin/main HEAD` (never a fixed
sha; a `BASE` in the caller's environment is ignored, and a `BASE=<sha>`
argument overrides it, which no task here needs), extracts the `# check: ID` block of
the quickstart.md beside it, exports `BASE` and each `NAME=VALUE`, runs the
block with bash in the foreground, and exits with the block's status: 0 only
when everything the check examines holds. It exits 2 when it cannot run the
check (bad arguments, the marker missing or on more than one block), so a check
that must fail is read as exit 1, not "non-zero": a verify that expects a check
to fail tests for exit 1 (`{ ...; test $? -eq 1; }`, as T019 does for the M4
mutants), never for any non-zero status. Every argument after the id
is one `NAME=VALUE`: check `red-first` takes its test names in `TESTS`, one
argument with the names separated by spaces (`"TESTS=test_a test_b"`). There is
no setup block to run first, and no verify reads a variable from another call.

The variables the checks read: `ADDED` for `suite` (the tests this feature has
added so far, 0 before Phase 2 and 15 `[Q2]` after it; the check measures `N0`
itself, at the merge base, so no count is written here), `PY` (`suite`; a 3.10
interpreter gets PyYAML linked in), `PARTS` (`fixed-text`), `PROJECT`
(`ast-project`), `NEW_TESTS` (`ast-tests`, default 15 `[Q2]`), `TESTS`,
`MUTANT` and `RF_MUST_FAIL` (`red-first`), `OPENSPEC` (`openspec`,
`governance`), `MODE` (`traceability`), `STAGE` (`governance`), `HEAD33`
(`merge-check`, required). Check `red-first` (the plan's `RF`) judges each test
in `TESTS` (by default the whole list) by its subtests against its own planned
counts, and, for N6, N7, N8, N10 and the three existing tests that gain rows,
by the planned reason it reads from each failure ("red for the wrong reason"
fails it), so a task's verify needs no traceback test of its own.

Preconditions, which the lead checks before dispatching a task (a verify that
needs one is not a finding about the task's work):

- Every verify: `qs.sh` exists, committed with the plan in the planning commit
  (FS-Q; plan.md "qs.sh (exact text)"), so no task creates it; and `bash`,
  `git` and `python3` (3.12 here), with `origin/main` known locally (the
  default `BASE`), run in the foreground (in a background job SIGINT is ignored
  and three pty tests fail).
- Check `suite` (T002, T004, T014, T016): PyYAML importable by `python3`, or
  linkable from it, for the interpreter `PY` names. T016's second run needs
  `uv` (`uv python find 3.10`) and a 3.10 interpreter it can find.
- Checks `governance` (T001, T017) and `openspec` (T026): `/usr/bin/openspec`
  1.6.0, or the openspec in py-bench through `OPENSPEC=`; never the host
  PATH's npm-global 1.2.0. Without network 1.6.0 first prints a harmless
  telemetry error.
- T019: the five mutant files, made by hand in the mutants directory its
  verify names (see T019); the verify fails when one is missing.
- T027: network, and an ssh key where `origin` is an ssh remote (as it is on
  the lane's benches), for `git ls-remote origin`; and, only when the commit it
  prints is not yet in the repository, `git fetch --no-tags origin
  refs/pull/33/head`, which writes `FETCH_HEAD` and the fetched objects and no
  branch, tag or remote-tracking ref.

A Phase 2 verify also compares the number of test methods in
`tests/test_project.py` with the merge base's plus the methods added so far,
with `grep -c '^    def test_'` (the verify defines its own
`B=$(git merge-base origin/main HEAD)` in front). That is the only per-task
guard that a task added exactly its methods: check `ast-tests` cannot run
before T009 rewrites its test.

Run each verify in the foreground with the Bash tool's timeout raised to
600000 ms: the default 120000 ms kills a long verify, and that is a timeout,
not a failed verify. The long ones are T007, T013 and T018, which take 3 to 4
minutes (the red pty runs wait `pty_timeout = 5` each at the base), and the
full-suite verifies T002, T004, T014 and T016, which can pass 2 minutes under
load.

## Rules for every new row and test (D3)

- Expected text comes from the fixtures only: the block T004 adds and the
  existing literals (`:28-87`); no test reads history.
- No existing line of `tests/test_project.py` changes except inside the
  rewritten test (T009). `known_obstacle_cases()` and
  `test_pty_dry_run_with_an_obstacle_refuses` gain added lines only `[Q2]`; no
  other existing member or module-level statement changes (check
  `ast-tests`). Never edit `setUp`, `run_cli`, `question_env`, `shape_env`,
  `run_pty` or `run_inproc`: lane 4's `tests/test_parent_reads.py` composes
  them.
- The import block (`:2-19`) stays as it is; the builder imports `socket`
  locally `[Q3]` and checks special files with `Path.is_fifo()`,
  `is_socket()` and `is_char_device()`.
- Fixtures live under `self.base`, which is already resolved (`:120`), at
  names apart from feature 003's (`file parent`, `link to file parent`,
  `dangling link parent`, `absent link target`, `absent parent`), so that a
  test can call both builders.
- Subtests take keyword parameters only (plan.md D3; `subTest()` takes one
  positional parameter, `msg`): the matrix runs
  `with self.subTest(given=LABEL, form="F1"):`; N6 `given` and `dry_run`; N7
  and N8 the row's label as `msg`, as `:1435` does; N12 to N15 `run`, here the
  run's research R5 id (for example `run="R-9.1"`).
- The snapshot (plan.md D3, "The snapshot"): each run takes
  `before = sorted(self.base.rglob("*"))` after its own environment is built
  and just before it calls `project`, and compares after the run:
  `question_env()` creates `self.base/bin` and `shape_env()` writes the fake
  `openRepoShape` there. An in-process run calls `obstacle_env()` or
  `self.fake_bin()` first, as `:1457` does, then takes the snapshot. Each run's
  environment is rebuilt for that run.
- The 15 new method names are plan.md D3's, exactly (check `red-first` and
  check `traceability` read them). A pty test's name starts with `test_pty_`,
  an in-process one's with `test_inproc_` (feature 002's rule). They go after
  `:1553`, before `:1555`, in the order N1 to N15 in the file, though N6 is
  written after N7 and N8 (T010 puts it between N5 and N7).
- `pty_timeout` stays 20 (`:146`) in the committed file.
- Every added line is ASCII (FR-013); comments and docstrings name
  `refuse-non-directory-parent-early` design decisions by number.

---

The implementer never ticks these boxes; the lane lead ticks each one after
checking its scope and its verify.

## Phase 0: Governance record `[Q5]`

**Purpose**: The change's handoff record before the first implementation
commit (plan.md slice 0, G1; feature 003's `90a4cee` precedent). The first
implementation commit is the first to touch `project`, `tests/test_project.py`
or `README.md` (the paths of G2's `FIRSTSHA`); a commit under `specs/` (the
planning commit with `qs.sh`, the traceability skeleton) is a record commit,
not an implementation commit.

- [X] T001 [S] [Q5] In `openspec/changes/refuse-non-directory-parent-early/tasks.md`
  make exactly G1 (plan slice G1) of plan.md "G1 and G2 exact text": the six
  whole-line replacements of lines 16, 20, 31, 36, 37 and 38 (the 1.6 tick with
  the quote and its link; the 2.1 tick with its appended "Created:" clause; the
  "to be created" prose line; the three Speckit Handoff fields), each "after"
  copied character for character from plan.md, and nothing else. 2.2 and 3.1 to
  3.3 stay `- [ ]`. Commit it alone, with that one pathspec, before the first
  implementation commit (any commit that touches `project`,
  `tests/test_project.py` or `README.md`). Run the verify right after the
  commit: the check reads the last commit.
  -- files: `openspec/changes/refuse-non-directory-parent-early/tasks.md`
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh governance STAGE=g1`

---

## Phase 1: Setup (baseline and record)

**Purpose**: The baseline, and the traceability skeleton (feature 003's T002).

- [X] T002 [P] [S] Confirm the baseline (plan slice S1) after T001: the suite passes with the
  merge base's `N0` tests, and `project`, `tests/test_project.py` and
  `README.md` are the merge base's. No file changes and no commit. It runs
  before any edit of `README.md` (T015), `tests/test_project.py` (T004) or
  `project` (T014): its verify requires the three at the base.
  -- files: (none)
  -- verify: `B=$(git merge-base origin/main HEAD) && bash specs/006-refuse-non-directory-parent-early/qs.sh suite ADDED=0 && git diff --quiet "$B" -- project tests/test_project.py README.md`
- [X] T003 [P] [S] Create `specs/006-refuse-non-directory-parent-early/traceability.md`
  (plan slice S2), lane line first, in feature 003's form (quickstart.md "Traceability": a
  short intro, then a table with the columns `#`, Requirement, Scenario, FRs,
  Tests): one row per scenario of the delta
  (`openspec/changes/refuse-non-directory-parent-early/specs/project-command/spec.md`),
  by requirement and scenario title in file order, numbered 1 to 40. Tests
  cell (plan.md D4): for the 20 scenarios plan.md's "Coverage map" does not
  list, the Tests cell feature 002's `traceability.md` gives the same title,
  copied byte for byte, except "No known obstacle" (row 40), which takes
  feature 003's cell (`specs/003-parent-obstacle-wording/traceability.md:26`:
  `test_pty_symbolic_link_to_a_directory_names_no_obstacle`,
  `test_pty_no_known_obstacle_names_none`); for the 20 it lists, exactly
  `pending (T028)`. FRs cell, from spec.md's FR list: `FR-011` for the 20
  unlisted rows; for the listed rows, by delta row number: 1 and 2
  `FR-001, FR-003, FR-005`; 3 and 4 `FR-003, FR-005`; 5 `FR-004`; 6
  `FR-001, FR-008`; 7 `FR-010`; 8 and 9 `FR-003`; 10 `FR-009`; 11 (Preview)
  `FR-005, FR-008`; 20 (A dry run asks too) `FR-003, FR-005`; 23 `FR-003`;
  26 `FR-003, FR-008`; 34 and 35 `FR-006`; 36 `FR-006, FR-007`; 37 and 38
  `FR-007`; 39 `FR-008` (D4, FR-015).
  -- files: `specs/006-refuse-non-directory-parent-early/traceability.md`
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh traceability MODE=skeleton && python3 -I -c 'import re,sys;V=chr(124);row=lambda l:[c.strip() for c in l.strip().strip(V).split(V)];tab=lambda p:[row(l) for l in open(p).read().splitlines() if l.startswith(V)][2:];P="specs/006-refuse-non-directory-parent-early/";M={m.group(2) for m in (re.match(r"^\| (ADDED|MODIFIED) \"([^\"]+)\"",l) for l in open(P+"plan.md")) if m};T2={r[2]:r[3] for r in tab("specs/002-triad-first-project-new/traceability.md")};T3={r[2]:r[4] for r in tab("specs/003-parent-obstacle-wording/traceability.md")};X="No known obstacle";R=tab(P+"traceability.md");e=[x for x in (len(M)==20 or "map",len(R)==40 or "rows",all(len(r)==5 and r[3] for r in R) or "columns or FRs",all(r[4]=="pending (T028)" if r[2] in M else r[4]==(T3 if r[2]==X else T2).get(r[2]) for r in R) or "cells") if x is not True];print("cells",e or "OK");sys.exit(1 if e else 0)'`

---

## Phase 2: Tests first (D3)

**Purpose**: Pin every D3 run (research R5) against the unchanged `project`.
The nine tasks T004 to T012 edit `tests/test_project.py`: one writer at a
time, in order. T013, the red-first checkpoint, edits nothing and closes the
phase.

- [X] T004 [S] [Q4] Add the fixture block of D3 item 1 (plan slice T1) to `tests/test_project.py`,
  inserted after `:62` (`OBSTACLE_PARENT_NOT_A_DIRECTORY`) and before the
  blank lines `:63-64` and `obstacles_refusal()` (`:65`), under a comment
  header naming `openspec/changes/refuse-non-directory-parent-early/design.md`,
  D2, in the precedent's form (`:58-61`):
  `OBSTACLE_PARENT_BELOW_A_NON_DIRECTORY`, `design.md:138` character for
  character with `{PARENT}` and `{ANCESTOR}` its only format fields;
  `HEAD_REFUSAL_END = " Nothing was created."`, its own literal, never
  `OBSTACLES_REFUSAL_END` (`:47`; report A3); a module-level
  `head_refusal(question_line)` returning
  `question_line.split(OBSTACLE_LINE_START, 1)[1] + HEAD_REFUSAL_END`, with a
  one-line docstring like `obstacles_refusal()`'s and two blank lines on each
  side; and the kept texts `SHAPE_NEEDS_EXISTING_PARENT = "Shape creation
  requires an existing --into parent directory."` (`project:372`),
  `GENERATOR_LIST_FIRST = "1. testBench:test"` (`project:196-197`) and `[Q4]`
  `FAMILY_NOT_A_FOLDER_NAME = "Family must be a single folder name."`
  (`project:324`). Names as plan.md D3 gives them (checked against every name
  in the module and in #33's head, research R5). Added lines only. The short
  check of the three kept texts after check `fixed-text` is still needed:
  that check reads only the D2 texts.
  -- files: `tests/test_project.py`
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh fixed-text PARTS=fixtures && python3 -I -c "import sys;sys.path.insert(0,'tests');import test_project as t;assert (t.SHAPE_NEEDS_EXISTING_PARENT,t.GENERATOR_LIST_FIRST,t.FAMILY_NOT_A_FOLDER_NAME)==('Shape creation requires an existing --into parent directory.','1. testBench:test','Family must be a single folder name.');print('OK: kept texts')" && bash specs/006-refuse-non-directory-parent-early/qs.sh suite ADDED=0`
- [X] T005 [US3] [S] [Q2] Add the case (b) rows (plan slice T2; research R5 R-5.1 to R-5.5) to
  `tests/test_project.py`: in `known_obstacle_cases()` insert after `:405` the
  local `below_line = OBSTACLE_PARENT_BELOW_A_NON_DIRECTORY.format(PARENT=parent_file / "sub", ANCESTOR=parent_file)`,
  and after `:413`, before the last row `:414`, the rows
  `"parent below a file": ("MyApp", True, ("--into", parent_file / "sub"), [below_line])`
  and `"all three with the parent below a file": ("my-app", False, ("--into", parent_file / "sub"), [name_line, OBSTACLE_OPENREPOSHAPE, below_line])`,
  so that the dict's closing line `:415` stays; in
  `test_pty_dry_run_with_an_obstacle_refuses` insert after `:1490`, before
  `:1491`, the one statement
  `cases["parent below a file"] = (("MyApp", "--into", parent_file / "sub"), [OBSTACLE_PARENT_BELOW_A_NON_DIRECTORY.format(PARENT=parent_file / "sub", ANCESTOR=parent_file)])`.
  No existing line changes; the existing assertions then run the new rows
  (FR-006, FR-007; SC-003). At the base each of the three tests is red in
  exactly its new rows, for the planned reason (sentence (b) expected, the
  missing sentence printed, never inside `assert_parent_file_unchanged`): check
  `red-first` reads the reason from each failure itself.
  -- files: `tests/test_project.py`
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh red-first "TESTS=test_pty_triad_answer_with_an_obstacle_refuses test_inproc_triad_obstacle_runs_nothing test_pty_dry_run_with_an_obstacle_refuses"`
- [X] T006 [US1] [S] [Q1] [Q3] Add to `tests/test_project.py` (plan slice T3) the builder
  `blocked_parents()`, a `ProjectTests` method after
  `assert_parent_file_unchanged()` (`:439-444`) and before `run_cli_streams()`
  (`:446`), and the first two new methods, N1 and N2. The builder makes FILE
  with `parent_file_fixture()` (`:419`) under `self.base` at a name apart from
  feature 003's, and returns research R5's givens K1 to K12 in R5's order,
  each as label to (the arguments after the name, the environment change, the
  expected question line, the kept path). Labels, exactly: `the file`, `a link
  to the file`, `a FIFO`, `the file with a trailing slash`, `below the file`,
  `two below the file`, `a link below the file`, `a socket` `[Q3]`,
  `/dev/null` `[Q3]`, `the file, positional`, `the file as PROJECTS_DIR`,
  `the file as ~/projects`. The FIFO by `os.mkfifo`, never opened; K4 passes
  the string `str(FILE) + os.sep`; `[Q3]` the socket an `AF_UNIX` socket bound
  at a short name and closed, `socket` imported inside the method, and when
  `bind` raises `OSError` the K8 subtests call `self.skipTest`; K12 a regular
  file at `HOME/projects` (`HOME` is `self.base / "home"`, `:134`) with
  `PROJECTS_DIR` removed. N1 `test_blocked_parent_by_flag_is_refused_before_the_plan`:
  forms F1 and F2 for every given (24 runs `[Q1]` `[Q3]`); N2
  `test_blocked_parent_is_refused_without_a_terminal`: form F5 for every given
  (12). Each run through `run_cli`, `self.env` rebuilt from
  `self.question_env(None)` plus the given's change,
  `with self.subTest(given=label, form="F1"):` (or `"F2"`, `"F5"`), command
  `new MyApp`, the given's arguments, then the form's flags; it asserts exit 2,
  standard output `""`, standard error exactly
  `REFUSED + head_refusal(line) + "\n"`, the snapshot (taken as the rules
  say) unchanged, and the kept path: `assert_parent_file_unchanged()` for a
  regular file, otherwise its type check (research R5, "The givens", "The
  forms", the matrix runs in F1, F2 and F5; FR-001, FR-003, FR-005; SC-001,
  SC-002; EC-001, EC-002).
  -- files: `tests/test_project.py`
  -- verify: `B=$(git merge-base origin/main HEAD) && bash specs/006-refuse-non-directory-parent-early/qs.sh red-first "TESTS=test_blocked_parent_by_flag_is_refused_before_the_plan test_blocked_parent_is_refused_without_a_terminal" && test "$(grep -c '^    def test_' tests/test_project.py)" -eq "$(( $(git show "${B}:tests/test_project.py" | grep -c '^    def test_') + 2 ))"`
- [X] T007 [US1] [S] [Q1] [Q3] Add N3, N4 and N5 (plan slice T4) to `tests/test_project.py`,
  each a pty method over every given of `blocked_parents()`, `run_pty` with no
  steps: N3 `test_pty_blocked_parent_by_type_without_yes_is_refused`, form F3
  (`--type test`, no `--yes`, `env` = `question_env(None)` plus the change);
  N4 `test_pty_blocked_parent_is_refused_where_ci_is_true`, form F4 (no
  choosing flag, `env` = `question_env("true")` plus the change); N5
  `test_pty_blocked_parent_is_refused_for_a_workspace_name`, form F6 (name
  `alice-wip`, no choosing flag, `question_env(None)` plus the change), and
  research R5's R-3.1 (`new alice-wip --into FILE --dry-run`) as
  `self.subTest(given="the file", form="F6 --dry-run")`. Subtests
  `self.subTest(given=label, form="F3")` (`"F4"`, `"F6"`). Each run asserts
  exit 2, standard output (the transcript) `""`, standard error exactly
  `REFUSED + head_refusal(line) + "\n"`, `assert_not_asked()` (`:369`) for F4
  and F6, the snapshot and the kept path (FR-001, FR-003, FR-005; SC-001,
  SC-002).
  -- files: `tests/test_project.py`
  -- verify: `B=$(git merge-base origin/main HEAD) && bash specs/006-refuse-non-directory-parent-early/qs.sh red-first "TESTS=test_pty_blocked_parent_by_type_without_yes_is_refused test_pty_blocked_parent_is_refused_where_ci_is_true test_pty_blocked_parent_is_refused_for_a_workspace_name" && test "$(grep -c '^    def test_' tests/test_project.py)" -eq "$(( $(git show "${B}:tests/test_project.py" | grep -c '^    def test_') + 5 ))"`
- [X] T008 [US3] [S] [Q2] Add N7 `test_pty_triad_answer_below_a_file_leaves_the_file_intact`
  and N8 `test_inproc_triad_answer_below_a_file_leaves_the_file_intact` to
  `tests/test_project.py`, after N5 (plan slice T5; research R5 R-5.6 to R-5.9; report A1):
  each takes the two case (b) rows of `known_obstacle_cases()` by label
  (`parent below a file`, `all three with the parent below a file`), asserts
  `self.assertEqual(len(rows), 2)`, and runs each row in `self.subTest(label)`
  exactly as `test_pty_triad_answer_with_an_obstacle_refuses` (`:1433-1450`)
  and `test_inproc_triad_obstacle_runs_nothing` (`:1452-1475`) do, with their
  assertions, plus the snapshot (N8 calls `obstacle_env()` first) and
  `self.assert_parent_file_unchanged(Path(extra[1]).parent, before)`: FILE,
  the ancestor the refusal names, not the row's `FILE/sub`. At the base they
  fail on the text (sentence (b) absent, the missing sentence printed), never
  on the file check: check `red-first` reads that reason from each failure
  itself ("red for the wrong reason" fails it), so no second command is needed.
  -- files: `tests/test_project.py`
  -- verify: `B=$(git merge-base origin/main HEAD) && bash specs/006-refuse-non-directory-parent-early/qs.sh red-first "TESTS=test_pty_triad_answer_below_a_file_leaves_the_file_intact test_inproc_triad_answer_below_a_file_leaves_the_file_intact" && test "$(grep -c '^    def test_' tests/test_project.py)" -eq "$(( $(git show "${B}:tests/test_project.py" | grep -c '^    def test_') + 7 ))"`
- [X] T009 [US2] [S] [Q2] Rewrite `test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path`
  (`:1526-1553`) in `tests/test_project.py`, the one existing test that
  changes (plan slice T6; D3 item 6; N3, AC5; research R5 R-6.1, R-6.2): its name and its
  comparison form stay; its comment names this design. The asked run answers
  `2` only (`steps=[(QUESTION_PROMPT, "2")]`); the baseline is `--type test`
  with no step; env `shape_env(ci=None)` as today. Both exit 2; the asked run's
  question carries line (a) (`assert_question`); the baseline is not asked
  (`assert_not_asked`); neither standard output contains `Create:`; each run's
  standard error holds exactly one `REFUSED:` line, compared from `REFUSED:`
  on (the prompt shares the asked run's line), equal across the two and equal
  to `REFUSED + head_refusal(line_a)`; no `warning:` line in either; no
  openRepoShape record; snapshot and file unchanged. Lines outside this method
  stay.
  -- files: `tests/test_project.py`
  -- verify: `B=$(git merge-base origin/main HEAD) && bash specs/006-refuse-non-directory-parent-early/qs.sh red-first "TESTS=test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path" && test "$(grep -c '^    def test_' tests/test_project.py)" -eq "$(( $(git show "${B}:tests/test_project.py" | grep -c '^    def test_') + 7 ))"`
- [X] T010 [US2] [S] [Q2] Add N6 `test_pty_single_answer_with_a_blocked_parent_is_refused_at_once`
  to `tests/test_project.py`, immediately after N5 and before N7 and N8 (the
  Rules' order N1 to N15 holds in the file, though T008 wrote N7 and N8
  first; plan slice T7; research R5 R-4.1 to R-4.4): first a second
  available generator appended to
  `self.config["benches"]["testBench"]["project_scripts"]` and saved, as
  `:1066-1068` does; `env = self.shape_env(ci=None)`, so the parent's line is
  the only obstacle; then FILE and FILE/sub (`blocked_parents()`'s `the file`
  and `below the file`), each with and without `--dry-run`, in
  `self.subTest(given=label, dry_run=flag)`, `run_pty` with
  `steps=[(QUESTION_PROMPT, "2")]`. Each asserts exit 2;
  `assert_question()` with the case's line; `assert_line_ends(stderr, REFUSED
  + head_refusal(line))` and exactly one `REFUSED:` on the two streams;
  neither stream holds `GENERATOR_LIST_FIRST`, `GENERATOR_PROMPT`, `Create:`
  or `CONFIRM_PROMPT`; `shape_record()` is None; snapshot and FILE unchanged;
  the transcript's tail is not asserted (FR-003, FR-005; SC-001, SC-002). At
  the base each of its four subtests is red for the planned reason, waiting at
  `Select a generator number` (which shows the second generator is in place,
  as mutant M2 needs): check `red-first` reads that reason itself.
  -- files: `tests/test_project.py`
  -- verify: `B=$(git merge-base origin/main HEAD) && bash specs/006-refuse-non-directory-parent-early/qs.sh red-first "TESTS=test_pty_single_answer_with_a_blocked_parent_is_refused_at_once" && test "$(grep -c '^    def test_' tests/test_project.py)" -eq "$(( $(git show "${B}:tests/test_project.py" | grep -c '^    def test_') + 8 ))"`
- [X] T011 [US4] [S] [Q2] Add the in-process helper `run_inproc_acting(*args, ci, answers)`
  (plan slice T8) to `tests/test_project.py`, after `blocked_parents()`: it behaves as
  `run_inproc()` (`:324-346`: the `inproc_terminal()` streams, the prompts
  list, the "Scripted answers left unused" check) except that an answer may
  also be a callable, called with the prompt, whose return value is the
  answer; `run_inproc()` itself is not edited. Then N9
  `test_inproc_parent_repaired_while_the_question_waits_is_created` (R-7.1)
  and N10 `test_inproc_parent_broken_while_the_question_waits_is_refused`
  (R-7.2), as research R5 gives them, each calling `self.fake_bin()` before
  its snapshot (FR-004; SC-007; AC8). N9 passes at the base: it is a guard.
  N10 is red at the base because `Type yes to run this plan:` is asked, not
  because of an error in `run_inproc_acting()`: check `red-first` reads that
  reason itself.
  -- files: `tests/test_project.py`
  -- verify: `B=$(git merge-base origin/main HEAD) && bash specs/006-refuse-non-directory-parent-early/qs.sh red-first "TESTS=test_inproc_parent_repaired_while_the_question_waits_is_created test_inproc_parent_broken_while_the_question_waits_is_refused" && test "$(grep -c '^    def test_' tests/test_project.py)" -eq "$(( $(git show "${B}:tests/test_project.py" | grep -c '^    def test_') + 10 ))"`
- [X] T012 [S] [Q2] [Q4] Add N11 to N15 (plan slice T9) to `tests/test_project.py`, as research
  R5 gives their runs (US1 scenario 6 for N12; US5 for N11, N13, N14, N15),
  each run of N12 to N15 in `self.subTest(run=ID)` with its R5 id: N11
  `test_dangling_link_parent_is_created_as_before` (R-8.1, one run); N12
  `test_blocked_parent_is_refused_before_later_faults`, runs R-9.1, R-9.2
  (`setup-openspeckit` asserted absent) and `[Q4]` R-9.8 (an empty
  `--workbenches` directory); N13
  `test_earlier_refusals_keep_their_text_with_a_blocked_parent`, runs R-9.3,
  R-9.4 and `[Q4]` R-9.7; N14
  `test_shape_by_flag_keeps_its_parent_refusal_with_a_blocked_parent`, runs
  R-9.5, R-9.6, R-9.5b, R-9.6b; N15
  `test_unwritable_directory_child_passes_dry_run_and_fails_at_creation`, runs
  R-10.1, R-10.2, skipped when `os.geteuid` is missing or returns 0, the
  restore to mode 755 registered with `addCleanup` before the
  `chmod(0o555)`, the permission error built from `errno.EACCES` and
  `os.strerror()`. N11, N13, N14 and N15 pass at the base: they are guards
  (FR-003, FR-008, FR-009, FR-010; SC-004, SC-005, SC-008).
  -- files: `tests/test_project.py`
  -- verify: `B=$(git merge-base origin/main HEAD) && bash specs/006-refuse-non-directory-parent-early/qs.sh red-first "TESTS=test_dangling_link_parent_is_created_as_before test_blocked_parent_is_refused_before_later_faults test_earlier_refusals_keep_their_text_with_a_blocked_parent test_shape_by_flag_keeps_its_parent_refusal_with_a_blocked_parent test_unwritable_directory_child_passes_dry_run_and_fails_at_creation" && test "$(grep -c '^    def test_' tests/test_project.py)" -eq "$(( $(git show "${B}:tests/test_project.py" | grep -c '^    def test_') + 15 ))"`
- [X] T013 [S] [Q1] [Q2] [Q3] [Q4] The red-first checkpoint (plan.md "Phase 2
  checkpoint"), with `project` unchanged: run check `red-first` over its whole
  list and report its output. Owner: one `[S]` writer with no file set; it edits
  no file and makes no commit, and a failure is filed as a defect against the
  task that owns the test (FS-T keeps one writer at a time). The check prints
  `checkpoint as planned` and exits 0 when red are N1 to N8, N10, N12 and the
  rewritten test, each in exactly its planned number of subtests, and the three
  existing tests in their new rows only; N6, N7, N8, N10 and those three must
  also be red for the planned reason, which the check reads. Green, and unable
  to show red first, are five methods holding eleven runs: research R5's nine
  guards of D3 (R-7.1 in N9, R-8.1 in N11, R-9.3, R-9.4 and `[Q4]` R-9.7 in N13,
  R-9.5 and R-9.6 in N14, R-10.1 and R-10.2 in N15) and the plan's two added
  shape runs R-9.5b and R-9.6b in N14. They pin behaviour that must not change;
  T019's mutants show they bite. The check runs in the foreground and takes
  about four minutes (its scratch copy lowers `pty_timeout` to 5; the committed
  test keeps 20). T014 does not start before T013 is ticked.
  -- files: (none)
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh red-first`

---

## Phase 3: Implementation (D1, D2)

**Purpose**: The read, the head refusal, and the README texts.

- [ ] T014 [O] [Q2] After T013 (the red-first checkpoint, seen as planned), in
  `project` (plan slice I1; D1; FR-001 to FR-011): (1) insert
  `parent_case(parent)` and then `blocked_parent_sentence(parent, kind, path)`
  after `:234` (the second blank line after `VISIBILITIES`, `:232`), each
  followed by two blank lines, so both sit just before `known_obstacles()`
  (`:235`) and far above `discover()` (`:433`; never at or after it, PR #33's
  zone), with plan.md D1's reference bodies and ASCII docstrings naming
  `refuse-non-directory-parent-early` design D1 and D2, the second saying it
  is called for the two blocked kinds only; (2) in `known_obstacles()`
  (`:235-254`) the parent fact (`:247-253`) becomes one `parent_case(parent)`
  call: `"directory"` adds nothing, `"missing"` adds today's missing sentence
  (the two string pieces of `:252-253` byte for byte), the two blocked kinds
  add `blocked_parent_sentence(parent, kind, path)`, into which sentence (a)
  moves from `:249-250` byte for byte; its signature, its order (name,
  openRepoShape, parent) and its one call (`:339`) stay, and its docstring
  keeps "three local facts" and names this design for the walk; (3) in
  `new()`, after `:384` (the shape-only flag refusal) and before `:385`
  (`row = choose(...)`), exactly the comment and three lines of plan.md D1
  "Call site 2". Nothing else: no import, constant or exception handling; no
  line of `new()` above the bench branch (in particular `:322-329`, lane 4's
  span); nothing at or below `discover()`. The name `parent_case()` is fixed:
  lane 4's realization calls it. This task edits only `project`. If a new test
  still fails with the change in, and the cause is the test (a wrong expected
  string or fixture) and not `project`, do not touch `tests/test_project.py`
  and do not bend `project` to fit it: stop, and report the failing test, its
  subtest and the reason. The lead routes a fix task to the tests' writer
  (FS-T, one writer at a time) and this task resumes once that fix is
  committed.
  -- files: `project`
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh suite ADDED=15 && bash specs/006-refuse-non-directory-parent-early/qs.sh ast-project`
- [X] T015 [P] [US6] [S] After T002, make the four README edits of plan.md D2
  (plan slice I2) in `README.md` (FR-012; SC-009), each fixed text copied from
  `design.md` character for character: edit 1, `design.md:169`, from "or a parent that is missing or is
  not a directory." (`:60`) to the end of the paragraph `:57-64`; edit 2,
  `design.md:177`, the choosing-flag sentence (`:75-77`); edit 3,
  `design.md:184`, the dry-run sentence (`:81-82`); edit 4, `design.md:190`,
  inserted after "Existing destinations refuse." (ends `:96`). Rewrap by
  plan.md D2's recipe exactly: refill from the first line an edit touches to
  the end of its paragraph with
  `textwrap.wrap(width=79, break_on_hyphens=False, break_long_words=False)`;
  edits 2 and 3 refilled once from `:75`; for edit 4 keep `:96` byte for byte
  and refill from the inserted text through `:98`. Expected at `d47e8a4`'s
  numbering (research R8): edit 1 at lines 60-68, edits 2 and 3 at 79-86,
  edit 4 at 101-105 with the old `:97-98` unchanged below it; lines `:53-55`
  unchanged; lane 4's phrase "a parent that is a directory the person cannot
  write" once, on one line. T002's verify requires `README.md` at the merge
  base, so this task never runs before T002; no test reads `README.md`, so
  after T002 it may run beside Phase 2 or T014. The width test after check
  `readme-texts` is still needed: it is the one mechanical check of FR-012's
  "rewrapped to the README's line width", which no quickstart check reads.
  -- files: `README.md`
  -- verify: `B=$(git merge-base origin/main HEAD) && bash specs/006-refuse-non-directory-parent-early/qs.sh readme-texts && [ -z "$(git diff -U0 "$B" -- README.md | grep '^+[^+]' | awk 'length > 80')" ]`

**Checkpoint**: check `suite` passes with the 15 new tests on 3.12 (T014's
verify); the README holds its four texts (T015's verify).

---

## Phase 4: Verification

**Purpose**: Evidence for the lane lead, the review and the pull request; keep
each task's output. T016 first, then T017; T018 and T019 after T016, one at a
time; T020 to T027 after T017, in any order. T028 (Phase 5) follows. The hand
walk and the adversarial review are lane steps 1 and 2, not tasks.

- [ ] T016 [S] [Q2] Run the full suite (plan slice V1), in the foreground, with check `suite`:
  once with the default `PY=python3` (3.12.3) and once with `PY` a 3.10
  interpreter (the check links PyYAML in when it lacks it); both must give
  `Ran N0+15 tests`, `OK`, `N0` measured at the merge base. A 3.10 run without
  PyYAML is informational only: it must fail exactly the 11 YAML tests
  quickstart.md "Run the tests" names (SC-006).
  -- files: (none)
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh suite ADDED=15 && bash specs/006-refuse-non-directory-parent-early/qs.sh suite ADDED=15 PY="$(uv python find 3.10)"`
- [ ] T017 [S] [Q5] Make G2 (plan slice G2) of plan.md "G1 and G2 exact text" in
  `openspec/changes/refuse-non-directory-parent-early/tasks.md`: line 21's
  `- [ ] 2.2` becomes `- [x] 2.2`, the rest of the line byte for byte, then one
  space and the "Met:" sentence with `G1SHA` and `FIRSTSHA` replaced by the
  short shas the plan's two `git log` commands print (G1SHA is T001's commit;
  FIRSTSHA is the first commit after the merge base that touches `project`,
  `tests/test_project.py` or `README.md`: that of T004 or of T015, whichever
  was committed first, since T015 may precede T004). Nothing else; 3.1 to 3.3 stay open. Commit it alone, with that one
  pathspec. Run the verify right after the commit: the check reads the last
  commit.
  -- files: `openspec/changes/refuse-non-directory-parent-early/tasks.md`
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh governance STAGE=g2`
- [ ] T018 [S] [Q1] [Q2] [Q3] [Q4] Record red first for the pull request (plan
  slice V2; FR-014): with the realized tests and `project` taken from the
  merge base, check `red-first` over its whole list prints `checkpoint as
  planned`, as at the Phase 2 checkpoint. Keep its output.
  -- files: (none)
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh red-first`
- [ ] T019 [S] Run the mutation checks of quickstart.md "Mutation checks" (plan
  slice V3) in scratch copies only, never in the worktree and never
  committed. The mutants live in one fixed directory outside every repository,
  `006-mutants` in the temporary directory (the verify computes it as the
  directory `mktemp` uses): from the realized `project` make
  `M1/project`, `M2/project` and `M3/project` there (the plan's head check
  moved as that table says), `M4a/project` (one stray line inside the
  parent-resolution span, the old `:322-329`) and `M4b/project` (an
  `open(parent)` call in `parent_case()`); create the directories with
  `mkdir -p`. The verify first requires all five files to exist and to parse,
  so a missing mutant cannot pass as caught. Check `red-first` with `MUTANT`
  and `RF_MUST_FAIL` must print `mutant caught` for M1 to M3, and check
  `ast-project` with `PROJECT` must exit 1 on M4a and M4b (research R10); exit
  2 means the runner could not run the check and does not count as the mutant
  being caught.
  -- files: (none)
  -- verify: `T=$(dirname "$(mktemp -u)")/006-mutants && test -s "$T/M1/project" && test -s "$T/M2/project" && test -s "$T/M3/project" && test -s "$T/M4a/project" && test -s "$T/M4b/project" && python3 -I -c 'import ast,sys;[ast.parse(open(p).read()) for p in sys.argv[1:]]' "$T/M1/project" "$T/M2/project" "$T/M3/project" "$T/M4a/project" "$T/M4b/project" && bash specs/006-refuse-non-directory-parent-early/qs.sh red-first MUTANT="$T/M1/project" RF_MUST_FAIL="test_inproc_parent_repaired_while_the_question_waits_is_created test_inproc_parent_broken_while_the_question_waits_is_refused" && bash specs/006-refuse-non-directory-parent-early/qs.sh red-first MUTANT="$T/M2/project" RF_MUST_FAIL="test_blocked_parent_is_refused_before_later_faults test_pty_single_answer_with_a_blocked_parent_is_refused_at_once" && bash specs/006-refuse-non-directory-parent-early/qs.sh red-first MUTANT="$T/M3/project" RF_MUST_FAIL="test_inproc_parent_repaired_while_the_question_waits_is_created test_earlier_refusals_keep_their_text_with_a_blocked_parent test_shape_by_flag_keeps_its_parent_refusal_with_a_blocked_parent" && { bash specs/006-refuse-non-directory-parent-early/qs.sh ast-project PROJECT="$T/M4a/project"; test $? -eq 1; } && { bash specs/006-refuse-non-directory-parent-early/qs.sh ast-project PROJECT="$T/M4b/project"; test $? -eq 1; }`
- [ ] T020 [P] [S] [Q5] Check that every added line is ASCII (plan slice V4; FR-013; SC-010),
  check `ascii-added`: the `+` lines of the diff from the merge base over
  `project`, `tests/test_project.py`, `README.md`, this feature's directory
  and `[Q5]` the change's `tasks.md`. The whole files are not checked:
  `project` already carries em dashes at `:197`, `:915`, `:928` and `:1136`,
  and the test module one at `:622` (archived N4).
  -- files: (none)
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh ascii-added`
- [ ] T021 [P] [S] Check the fixed text (plan slice V4), check `fixed-text`, both parts: the
  fixtures equal `design.md:136-138`, `:147` and `:155-156` character for
  character, `HEAD_REFUSAL_END` is its own literal, and the README holds
  `design.md:169`, `:177`, `:184` and `:190` once each (D2; FR-005, FR-006,
  FR-012, FR-014).
  -- files: (none)
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh fixed-text`
- [ ] T022 [P] [US6] [S] Check the README (plan slice V4), check `readme-texts`
  (`grep -oF ... | wc -l` on the lines joined by single spaces, never
  `grep -c`): each of the four fixed texts once, edit 4 as "Existing
  destinations refuse. " followed by it, lane 4's phrase once, each replaced
  phrase 0 times, lines `:53-55` the merge base's (FR-012; SC-009). This
  check supersedes feature 003's README check.
  -- files: (none)
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh readme-texts`
- [ ] T023 [P] [S] [Q5] Check the files changed (plan slice V5; FR-016 as the
  Clarifications narrow it), check `files-changed`: since the merge base the
  branch changes only `project`, `tests/test_project.py`, `README.md`, `[Q5]`
  the change's `tasks.md`, and files under
  `specs/006-refuse-non-directory-parent-early/` (`spec.md`,
  `clarify-questions.md`, `checklists/requirements.md`, `plan.md`,
  `research.md`, `quickstart.md`, `tasks.md`, `traceability.md` and the runner
  `qs.sh`); `qs.sh` must be among the committed changes. `qs.sh` is a
  planning-commit file, not a build change: no task creates or edits it, and the
  check sees it because the branch diff since the merge base includes the
  planning commit.
  -- files: (none)
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh files-changed`
- [ ] T024 [P] [S] Check `project`'s structure (plan slice V5), check `ast-project` (D1, D6;
  FR-002, FR-011): only `parent_case()` and `blocked_parent_sentence()` are
  new, just above `known_obstacles()` and above `discover()`; only
  `known_obstacles()` and `new()` change; `new()` gains one block, between the
  shape-only refusal and the `row = choose(...)` line; `parent_case()` calls
  only `is_dir()` and `exists()`; imports and module-level statements
  unchanged. Its span assertion is the byte-identity check of lane 4's
  `project:322-329` (the parent resolution through the existing-destination
  refusal; lane 4's design D7, plan D6).
  -- files: (none)
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh ast-project`
- [ ] T025 [P] [S] [Q2] Check the tests' structure (plan slice V5), check `ast-tests` (FR-014;
  SC-006): no existing module-level statement or member removed or changed
  but the rewritten test; `known_obstacle_cases()` and
  `test_pty_dry_run_with_an_obstacle_refuses` gained lines only; exactly 15 new
  test methods (`NEW_TESTS`, default 15).
  -- files: (none)
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh ast-tests`
- [ ] T026 [P] [S] Validate OpenSpec (plan slice V6), check `openspec`, with
  `/usr/bin/openspec` (1.6.0) or the openspec in py-bench, never the host's
  npm-global 1.2.0: the change is valid strictly, and `--all --strict` prints
  `Totals: N passed, 0 failed` (9 of 9 at `d47e8a4`). Without network, 1.6.0
  first prints a harmless telemetry error.
  -- files: (none)
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh openspec`
- [ ] T027 [P] [S] Run the merge check against PR #33's head as it is when the
  task runs, check `merge-check` (plan.md "Other lanes", step 1; research R9):
  `project`, `README.md` and `tests/test_project.py` merge cleanly with that
  head and the merged `project` parses. Read-only for the worktree, the branch
  and every ref. The head is read at run time with
  `git ls-remote origin refs/pull/33/head`, never written into a task; when
  that commit is not yet in the repository, `git fetch --no-tags origin
  refs/pull/33/head` brings it, writing `FETCH_HEAD` and the fetched objects
  only (no branch, tag or remote-tracking ref). It needs network, and an ssh
  key where `origin` is an ssh remote. No merge, rebase or checkout is made.
  Once #33 is on main the check runs as
  `bash specs/006-refuse-non-directory-parent-early/qs.sh merge-check HEAD33=origin/main`
  instead; lane step 4 does that on the real commit before main is merged in.
  -- files: (none)
  -- verify: `H=$(git ls-remote origin refs/pull/33/head | cut -f1) && test -n "$H" && { git cat-file -e "${H}^{commit}" 2>/dev/null || git fetch --no-tags origin refs/pull/33/head; } && bash specs/006-refuse-non-directory-parent-early/qs.sh merge-check HEAD33="$H"`

---

## Phase 5: Traceability (D4; FR-015)

- [ ] T028 [S] [Q2] Complete `specs/006-refuse-non-directory-parent-early/traceability.md`
  (plan slice V7): replace each `pending (T028)` cell with the tests plan.md's
  "Coverage map" plans for that scenario, by method name (N1 to N15 as plan.md
  D3 names them; "the rewritten test" is
  `test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path`;
  "the existing rows (003 traceability row 3)" and "(row 4)" are the tests of
  feature 003's `traceability.md` rows 3 and 4, with the rows in parentheses
  as there), each name in backticks; the 20 rows T003 filled stay, "No known
  obstacle" with 003's two tests. FR-015's two mappings: the rewritten test
  under "A single repository taken at the question with a parent blocked by a
  non-directory" only, never under "A single-repository answer is
  unaffected", which keeps `test_pty_single_answer_is_unaffected_by_obstacles`
  (lead's ruling). The coverage-map command after check `traceability` is
  still needed: the check proves that every row names defined tests and
  FR-015's mappings, but not that each mapped row names the tests the plan's
  coverage map plans for it.
  -- files: `specs/006-refuse-non-directory-parent-early/traceability.md`
  -- verify: `bash specs/006-refuse-non-directory-parent-early/qs.sh traceability && python3 -I -c 'import re,sys;V=chr(124);B=chr(96);row=lambda l:[c.strip() for c in l.strip().strip(V).split(V)];tab=lambda p:[row(l) for l in open(p).read().splitlines() if l.startswith(V)][2:];P="specs/006-refuse-non-directory-parent-early/";pl=open(P+"plan.md").read().splitlines();N={m.group(1):m.group(2) for m in (re.match(r"^\| (N\d+) \| "+B+r"(test_\w+)"+B,l) for l in pl) if m};C={m.group(2):m.group(3) for m in (re.match(r"^\| (ADDED|MODIFIED) \"([^\"]+)\" \| (.*) \|$",l) for l in pl) if m};T3=[r[4] for r in tab("specs/003-parent-obstacle-wording/traceability.md")];RW="test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path";q=lambda c:re.findall(B+r"(test_\w+)"+B,c);need=lambda c:[N[k] for k in re.findall(r"\bN\d+\b",c)]+q(c)+([RW] if "the rewritten test" in c else [])+[n for k in re.findall(r"003 traceability row (\d+)",c) for n in q(T3[int(k)-1])];R=tab(P+"traceability.md");miss=[(r[2],sorted(set(need(C[r[2]]))-set(q(r[4])))) for r in R if r[2] in C and not set(need(C[r[2]]))<=set(q(r[4]))];e=[x for x in (len(N)==15 or "methods",len(C)==20 or "map",sum(r[2] in C for r in R)==20 or "map rows",not miss or miss) if x is not True];print("map",e or "OK");sys.exit(1 if e else 0)' && bash specs/006-refuse-non-directory-parent-early/qs.sh ascii-added && bash specs/006-refuse-non-directory-parent-early/qs.sh files-changed`

---

## Lane steps (the lane lead's, after T028)

Not checkbox tasks, not tier-tagged, and no build agent runs them, as in
feature 003's `tasks.md` (plan.md, "Lane steps"). Steps 1 and 2 are lead
steps, not tasks, because a build agent has no terminal and the lead
dispatches the review itself; both come before the pull request opens.

1. **Hand walk** `[Q3]` `[Q4]`. The lead, or Brett Heap, walks quickstart.md
   at a real terminal before the pull request opens: its fixture, then every
   run of User Stories 1 to 6 (the FIFO, `FILE/`, `FILE/sub`, `[Q3]` the
   socket and `/dev/null`, `[Q4]` the `--family` and `--workbenches` runs
   included; User Story 4 needs two terminals, the second repairing or
   breaking the parent while the first waits at the question). Every run
   prints and exits as its row says; each divergence is recorded with the run,
   its output and the task that owns the file, as a defect against that task,
   before the review (SC-001, EC-001, EC-002).
2. **Adversarial review**. The lead dispatches the `[O]` adversarial review
   once T001 to T028 are ticked and step 1 is done, and records its verdict
   before the pull request opens. The reviewer is an independent `opus-xhigh`
   agent that wrote none of T001 to T028, read-only, in its own scratch copy.
   It re-runs every check through `qs.sh` (`suite` with 3.12 and with 3.10,
   `readme-texts`, `ascii-added`, `files-changed`, `fixed-text`,
   `ast-project`, `ast-tests`, `red-first`, `openspec`, `traceability`,
   `governance` with `STAGE=g2`, `merge-check` against #33's head at that
   time) and reads the diff against spec.md, design.md D1 to D6 and plan.md,
   lane 4's three pins included (`parent_case()` by name, the README phrase
   once, `:322-329` and the harness helpers untouched). Findings by severity
   (blocker, major, minor, nit), each with file, line and a fix. The verdict
   is a review report that names the head sha it read, gives each check's exit
   status (all 0), and lists every finding as fixed or ruled on by the lead; a
   fix is a new task on its own file set, after which the review re-runs on
   the new head.
3. Push the branch (a plain push) and open the realization as a draft pull
   request to main; its body carries `Closes #20` and the line `Lane:
   openRepoProject-1`.
4. When #33 is on main, run
   `bash specs/006-refuse-non-directory-parent-early/qs.sh merge-check HEAD33=origin/main`,
   then merge main in (`git fetch origin`, `git merge origin/main`; never a
   rebase, never a force push), re-read every line citation by function name,
   and re-run the checks of Phases 4 and 5 on the merge (check `suite` measures
   the new `N0` itself).
5. Mark the pull request ready once step 2's findings are resolved and both CI
   jobs (`ubuntu-latest`, Python 3.10 and 3.12) are green.
6. Land only on Brett Heap's word for that pull request, quoted with its link;
   no rebase, no force push.
7. After landing: cite the merge sha in the change's `tasks.md` 3.1 (`gh pr
   view <n> --json mergeCommit,statusCheckRollup`); post D5's one comment on
   workBenches#145 if it is still open (3.2), nothing if it is closed; open no
   new issue.
8. The archive pull request: `/opsx:archive` for
   refuse-non-directory-parent-early (3.3), its `openspec validate --all
   --strict` run with `/usr/bin/openspec` or the openspec in py-bench.
9. Retire the worktree and its branch once the realization and the archive
   have landed.

Also from plan.md "Other lanes": if this realization lands before #33, the
lead tells lane 2 once that feature 004's gates T009, T046, T128 and T131 read
the fixed baseline `961c405`; re-pointing them is lane 2's work.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Before T001**: the spec's Clarifications carry Brett Heap's answers, and
  plan.md (with its section "qs.sh (exact text)"), research.md, quickstart.md,
  `qs.sh` and this file are committed (the planning commit, a record commit and
  not an implementation commit; FIRSTSHA's paths exclude them).
- **Phase 0**: T001 first and alone; no commit touches `project`,
  `tests/test_project.py` or `README.md` before it `[Q5]`.
- **Phase 1**: after T001; T002 and T003 in parallel.
- **Phase 2**: after T002; T004 first (every later test uses its fixtures),
  then T005 to T012 in order, one writer; T006 before T007 and T010 (the
  builder), T011's helper with its users. T013, the red-first checkpoint,
  closes the phase and needs T004 to T012 committed.
- **Phase 3**: T014 after T013. T015 after T002 (never before it: T002's
  verify requires `README.md`, `project` and the tests at the merge base),
  beside Phase 2 or T014 (no test reads `README.md`).
- **Phase 4**: after Phase 3; T016 first; T017 after T016 (the first
  implementation commit, T004's or T015's, already exists); T018 and T019 after
  T016, one at a time (pty load); T020 to T027 after T017, in parallel.
- **Phase 5**: T028 after T016 (every named test defined).
- **Lane steps**: after T028 for steps 1 and 2, which come before the pull
  request opens; step 4 at any phase boundary once #33 is on main.

### Within Each Phase

- Every Phase 2 task but T013 edits `tests/test_project.py`: they run one at a
  time, each committed before the next starts.
- Tests are seen red at the Phase 2 checkpoint (T013) before T014 is written.
- `project` has one writer (T014), who edits only `project`; a new test that
  fails there because of the test goes back to the tests' writer (see the
  Notes).
- Each FS-G task (T001, T017) is its own commit with its one pathspec.

### Parallel Opportunities

- T003 (`traceability.md`) beside T002.
- T015 (`README.md`), after T002, beside Phase 2 or T014
  (`tests/test_project.py`, `project`).
- T020 to T027, which touch no file, beside one another.

---

## Parallel Example

```bash
# One writer per file set; the lead serializes their commits.
Task: "T004 to T012: the fixtures, rows, builder and the 15 new tests, in tests/test_project.py, in order"
Task: "T015: the four README edits by plan.md D2's recipe, in README.md"
Task: "T003: the traceability skeleton, in specs/006-refuse-non-directory-parent-early/traceability.md"
```

---

## Implementation Strategy

The realization ships as one pull request with no MVP split: the six stories
come from one read and one head check. Stop and validate at the Phase 2
checkpoint, T013 (exactly the planned subtests red, the guards green), and at
T016 (the suite passes with the 15 new tests on 3.12 and 3.10 `[Q2]`).
Escalation follows the build tiers: `[S]` then `[O]`, one attempt each; an
`[O]` failure goes back to `/speckit-plan` or `/speckit-clarify` with a short
failure record.

---

## Requirement Coverage

| Requirement | Tasks |
| --- | --- |
| FR-001 | T006, T007 (case (a) and (b) givens), T012 (N11), T014 |
| FR-002 | T014, T024 (`parent_case()` calls only `is_dir()` and `exists()`), T006 (the FIFO never opened) |
| FR-003 | T006, T007, T010, T012 (N12, N13, N14), T014, T019 (M2, M3) |
| FR-004 | T011, T019 (M1) |
| FR-005 | T004, T006, T007, T009, T010, T014, T021 |
| FR-006 | T005, T014, T021 |
| FR-007 | T005, T008 |
| FR-008 | T012 (N11), T016 (`test_pty_single_answer_is_unaffected_by_obstacles`) |
| FR-009 | T012 (N14) |
| FR-010 | T012 (N15), T014 |
| FR-011 | T014, T016, T024, T025 |
| FR-012 | T015, T021, T022 |
| FR-013 | T020 |
| FR-014 | T004 to T012, T018, T025 |
| FR-015 | T003, T028 |
| FR-016 `[Q5]` | T001, T017, T023 |

Success criteria: SC-001 T006, T007, T010; SC-002 T006 (F2), T007 (R-3.1),
T010; SC-003 T005, T008; SC-004 T012 (N11), T016; SC-005 T012 (N13, N14);
SC-006 T016, T025, T028, lane step 5 (both CI jobs); SC-007 T011; SC-008 T012
(N15); SC-009 T015, T022; SC-010 T020; SC-011 lane step 7 (D5), nothing in
workBenches.

Edge cases: EC-001 T006 (the FIFO; `[Q3]` the socket and `/dev/null`), lane
step 1; EC-002 T006 (`FILE/`, the two links), lane step 1; EC-003 T012 (N11);
EC-004 not tested (plan.md, Risks: a race inside one process step); EC-005
T015 (the README sentence); EC-006 T012 (N12, N13); EC-007 T016
(`test_pty_workflow_prerequisite_is_refused_before_the_question`, unchanged);
EC-008 T012 (N15) for the missing child, the other bullets not tested
(plan.md, Risks); EC-009 out of scope (lane 4).

Every row below is also made true by T014 (`project`) and shown by the Phase 4
checks; the tasks named are the ones that pin the row by a test or a check.
"Existing tests" are tests that T016 runs unchanged and T028 maps.

User-story scenarios (spec.md; 25: US1 6, US2 4, US3 4, US4 2, US5 8, US6 1):

| Scenario | Tasks |
| --- | --- |
| US1.1 flag-chosen, case (a) kinds and routes | T004 (fixtures), T006 (N1, N2), T007 (N3 to N5) |
| US1.2 case (b) by flag | T006, T007 |
| US1.3 at a terminal without `--yes` | T007 (N3) |
| US1.4 `--dry-run` | T006 (N1, form F2), T007 (N5, R-3.1) |
| US1.5 not asked, three ways | T006 (N2, standard input not a terminal), T007 (N4 `CI=true`, N5 workspace name) |
| US1.6 later faults | T012 (N12: `nomatch`, `--workflow`, `[Q4]` the `--workbenches` lookup); partial: the generator-registry fault (a malformed `bench-config.json`) is untested under Q4 B (plan.md "Not tested"); Q4 C's R-9.10 pins it |
| US2.1 answer `2`, two generators | T010 (N6) |
| US2.2 answer `2` with `--dry-run` | T010 (N6) |
| US2.3 the comparison with `--type test` | T009 (the rewritten test) |
| US2.4 known obstacle, parent not blocked, answer `2` | existing tests (`test_pty_single_answer_is_unaffected_by_obstacles`), T016, T028 |
| US3.1 case (b) named at the question | T005 (rows), T008 (N7, N8) |
| US3.2 the Triad refusal, composed | T005 (the `all three with the parent below a file` row), T008 |
| US3.3 the Triad refusal with `--dry-run` | T005 (the dry-run row) |
| US3.4 case (a) and a missing parent unchanged | existing rows (003 traceability rows 3 and 4), T016, T028 |
| US4.1 parent repaired while waiting | T011 (N9, a guard) |
| US4.2 parent broken while waiting | T011 (N10) |
| US5.1 dangling link, missing parent, directory | T012 (N11), existing tests (T016) |
| US5.2 earlier refusals keep their text | T012 (N13: `--org` without `--shape`, invalid name, `[Q4]` `--family`) |
| US5.3 shape by flag | T012 (N14) |
| US5.4 unwritable directory, dry run | T012 (N15) |
| US5.5 unwritable directory, `--yes` | T012 (N15) |
| US5.6 dry run, parent not blocked | existing tests (T016, T028) |
| US5.7 `--workflow` order when not asked, parent not blocked | existing test (`test_workflow_refusal_order_unchanged_when_not_asked`), T016 |
| US5.8 unaltered scenarios of the four MODIFIED requirements | existing tests, T016, T028 |
| US6.1 README, four texts once | T015, T021, T022 |

Acceptance criteria (the ratified proposal's AC1 to AC9; 9):

| Criterion | Tasks |
| --- | --- |
| AC1 kinds, routes and forms, each refused | T004, T006, T007 |
| AC2 answer `2` refused at once, `--dry-run` too | T010 |
| AC3 asked, Enter: (a) as today; (b) the new line and refusal | T005, T008; existing rows (T016) for (a) |
| AC4 missing parent and dangling link as today | T012 (N11), T016 |
| AC5 earlier refusals; ASCII; existing tests unchanged but the rewritten one | T009 (the rewrite), T012 (N13, N14), T016, T020, T025 |
| AC6 `nomatch` and `--workflow` give the parent refusal; `--org` keeps its own | T012 (N12, N13) |
| AC7 README fixed text by grep | T015, T022 |
| AC8 parent repaired or broken while waiting, in process | T011 (N9, N10) |
| AC9 permission boundary pinned | T012 (N15) |

---

## Appendix A: Options not taken

Each entry lists only the tasks that change, appear or disappear; every other
task stands. Combined answers add up as research R7 says. The planned subtest
counts live in check `red-first`'s tagged numbers, so a different answer
changes quickstart.md there and leaves these verify commands as they are,
unless an entry says otherwise. A short answer ("Another breadth", "Another
way", "Another place"): re-derive the affected runs of research R5 by the
same rules, then the tasks named under that question.

### Q1 (test breadth of the head refusal)

- **A (D3's matrix exactly).** T006: N1 keeps all twelve givens (24 runs); N2
  keeps `the file` only (1). T007: N3 keeps `the file` and `below the file`
  (2), N4 `the file` (1), N5 `the file` and R-3.1 (2). The builder is
  unchanged (N1 uses every given). Check `red-first`'s counts follow. No task
  appears or disappears; the suite is still `N0 + 15`.
- **C (full cross product).** T006: the builder adds every case (a) kind by
  every route it can take (`FILE/` has no `~/projects` form), 20 givens; N1 40
  runs, N2 20. T007: N3 20, N4 20, N5 21. Methods and the suite's count stay.

### Q2 (proving FILE intact for the case (b) rows)

- **B (widen the guard).** T008 disappears (N7 and N8 go; 13 new methods).
  T005 also edits the guard at `:1439` and `:1460` of the two Triad-answer
  tests so that it holds for a missing parent whose nearest existing path is
  not a directory, the check reading that path; it stays `[S]`. The
  method-count offsets in T009 to T012 fall by 2 (7, 8, 10, 15 become 5, 6, 8,
  13); T014 and T016 run check `suite` with `ADDED=13`; T025 runs check
  `ast-tests` with `NEW_TESTS=13`, and quickstart.md's check allows the two
  Triad tests a changed guard line; check `red-first` drops N7 and N8 (T013, T018);
  T028's coverage row for "The parent would be created below a path that is
  not a directory" loses N7 and N8 (its command reads plan.md, so it stands).

### Q3 (the optional kinds)

- **B (`/dev/null` only).** T006: no socket, no local `socket` import; N1 22
  runs, N2 11. T007: N3 11, N4 11, N5 12. Lane step 1's hand walk drops the
  socket run.
- **C (neither).** T006: no socket and no `/dev/null`; N1 20, N2 10. T007: N3
  10, N4 10, N5 11. Lane step 1 drops both runs.

### Q4 (faults the order tests pin)

- **A (D3 item 9 as it stands).** T004 drops `FAMILY_NOT_A_FOLDER_NAME` (and
  its verify's kept-text check drops it too). T012: N12 loses R-9.8, N13 loses
  R-9.7 (check `red-first`'s N12 count becomes 2). The checkpoint's green runs
  are ten (T013's). Lane step 1 drops the `--family` and `--workbenches` runs.
- **C (B plus five faults).** T012: N13 adds R-9.9 (a positional parent with
  `--into`, `PARENT_AND_INTO`, `:79`) and R-9.11 to R-9.13 (`--visibility
  private`, `--family Products`, `--elected-by alice` without `--shape`,
  `ORG_NEEDS_SHAPE`); N12 adds R-9.10 (a malformed `bench-config.json`, the
  head refusal), so its count becomes 4. The checkpoint's green runs are
  fifteen. No new literal is needed.

### Q5 (where the governance ticks go)

- **B (a separate governance PR).** T001 and T017 leave this branch: the lead
  opens a governance PR to main with G1 before `/opsx:apply`, and a lane step
  "merge main in after the governance PR lands" takes T001's place before T002;
  2.2 is ticked there or at the archive. FS-G
  leaves; check `ascii-added` (T020) and check `files-changed` (T023) drop the
  change's `tasks.md` in quickstart.md.
- **Short answer.** The place named replaces T001 and T017; T020 and T023
  follow it.

---

## Appendix B: If a Governed invariants section is declared

If plan.md (or `AGENTS.md`) gains a `## Governed invariants` section that
covers neither `project`, `tests/test_project.py` nor `README.md`, the
protocol's `[H]` rubric admits the fully specified, pattern-copying tasks:
T002 (S1), T004 (T1), T005 (T2; `[S]` under Q2 B), T015 (I2), T016 (V1),
T020, T021, T022 (V4), T023, T024, T025 (V5) and T026 (V6). The `openspec/`
text is governed in every repository, so T001 and T017 stay `[S]`. T013 (the
checkpoint) stays `[S]` by the lead's ruling.

---

## Notes

- [P] tasks = disjoint files, no dependencies between them.
- `traceability.md` maps each delta scenario to its tests (D4, FR-015).
- No task edits workBenches, openRepoShape, setup-openspeckit,
  `.github/workflows/`, `CLAUDE.md`, `AGENTS.md`, the records of features 002
  and 003, or the change's files other than its `tasks.md` `[Q5]`.
- No task names PR #33's head: T027 and lane step 4 read it when they run.
- Every verify is self-contained (see "Verify note"): it reads no variable
  another call defined, runs a quickstart check through `qs.sh`, and defines
  any other value (`B`, `T`, `H`) inside its own line.
- Test defects at T014. The `project` builder edits only `project`. If a new
  test fails at T014 because of the test, not because of `project`, the
  builder leaves `tests/test_project.py` alone and reports it; the lead routes a
  fix task to the tests' writer. `tests/test_project.py` keeps one writer at a
  time (FS-T), so no `project` builder edits it.
- A block caused by a defect in an earlier task's output counts as that earlier
  task's failure, not the later task's: the lead re-opens the earlier task at
  its tier, then re-dispatches the later one.
- Plan slice ids (T1 to T9, V1 to V9, S1, S2, G1, G2, I1, I2) are not task
  ids (T001 to T028): the crosswalk above maps one to the other, and a task
  names its slice where the plan's text is cited.
- Scratch directories (the mutants directory of T019, the checks' own
  `mktemp -d` copies) stay outside every repository; remove them by hand
  afterwards (no recursive delete in a verify line).
