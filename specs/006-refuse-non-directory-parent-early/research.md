Lane: openRepoProject-1

# Research: Refuse a non-directory parent early

The design decides every technical question:
`openspec/changes/refuse-non-directory-parent-early/design.md` (D1 to D6)
records no open question that changes what is built (`design.md:364-369`). The
entries below record the decisions the packet made, with their rationale and
the alternatives it rejected, and the choices the realization makes (where code
and tests go, which runs the tests make, how they are split and checked). They
cite; the design holds the detail and governs.

**Clarify answers.** This research follows Brett Heap's clarify answers of
2026-10-22, "all recommended" (Q1 B, Q2 A, Q3 A, Q4 B, Q5 A; R12), recorded in
the spec's Clarifications; entries that turn on one carry its tag.

**Evidence.** Probes ran on scratch copies made with `git archive d47e8a4 |
tar -x` outside every repository, never in the worktree: a prototype of D1
exactly as the plan's reference shape, the README edits of R8, the mutants of
R10, and the governance text of R14. Line numbers are those of `d47e8a4`
(`project`, `tests/test_project.py`, `README.md`) unless a file is named. The
run inventory of R5 is adapted from agent T's test inventory (2026-10-21,
outside the repository, named for provenance only); everything R5 needs is
here.

## R1. The read is pathlib, in D1's order, on the resolved parent (D1)

- **Decision**: one helper, `parent_case(parent)`, returns `(kind, path)`:
  `parent.is_dir()`; then `parent.exists()`; then, for a missing parent,
  `exists()` on each path of `parent.parents` from the nearest, up to the first
  that exists, and that path's `is_dir()` (`design.md:69-87`). A second helper,
  `blocked_parent_sentence(parent, kind, path)`, returns sentence (a) or (b),
  for the two blocked kinds only. No exception handling, no import, nothing
  opened (`design.md:106-112`).
- **Rationale**: the reads the precedent already makes decide the four cases
  with certainty, open nothing (a FIFO is a `stat`, never an `open`), and end
  at the root, which exists (N2, `clarifications.md:33-45`). On 3.10 and 3.12
  they ignore the errors a missing or non-directory component gives, and an
  unsearchable ancestor raises earlier at `destination.exists()`
  (`project:328`).
- **Observed for this plan** (Python 3.12.3, and 3.10.21 in `py-bench`, on the
  prototype):
  - The full suite: 3.12.3 `Ran 96 tests`, 1 failure, exactly
    `test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path`,
    which pins today's late refusal (its asked run waits for `Type yes to run
    this plan:` and the run now ends before it). 3.10.21 with PyYAML supplied
    as `quickstart.md` ("Environment") says: `Ran 96 tests`, the same 1
    failure. 3.10.21 without PyYAML: 12 failures, the 11 YAML tests of R11
    that fail at the base too and that one. This re-observes the packet's
    feasibility note (proposal, Impact) at `d47e8a4`.
  - A probe ran every kind (a regular file, a link to it, a FIFO, `FILE/`, a
    socket, `/dev/null`, `FILE/sub`, `FILE/a/b`, a link to `FILE/x`) by
    `--into` in AC1's six forms, the file by the positional parent,
    `PROJECTS_DIR` and `~/projects`, and the answer `2` with two generators,
    with and without `--dry-run`: every run exit 2, standard output empty (a
    pty transcript too), standard error the head refusal of D2 for the case,
    the tree and the file unchanged. Its outputs on 3.12.3 and 3.10.21 (65
    lines each) are identical by `diff`.
- **Alternatives considered** (packet): a raw `os.stat` classified by errno
  (archived N5; `design.md:121-125`); reading writability (N4, D6); reusing the
  question's read at the head (R4).

## R2. Where the code goes: the helpers above `known_obstacles()`, the head check after the shape-only flag check (D1, W1)

- **Decision**: the two helpers after `project:234`, just before
  `known_obstacles()` (`:235`). The head refusal in the bench branch, after
  `project:383-384` and before `:385` (`design.md:98-104`), on every bench
  path: by flag, not asked, or after the answer `2`. No other line of `new()`
  (in particular not `:322-329`), and no new module-level statement but the two
  functions.
- **Rationale**: the head check is the first step of the single-repository
  path, so the earlier refusals keep their place and text (the name, a
  positional parent with `--into`, the family form, an existing destination,
  the hoisted `--workflow` check and the question when asked, the shape-only
  flags), the ratified question line stays reachable, and the answer `2` meets
  no generator list, plan or `yes` prompt (proposal, "Alternatives", W1).
  "Generator selection" includes the workBenches lookup, since one expression
  does both (`choose(registry(workbenches(...)), args)`, `project:385`; spec
  FR-003, report A2). For the helpers, the spec's Assumptions carry report H's
  placement ("just before the reader of known obstacles"). Agent B measured
  the conflict-free zone against PR #33 as main's `:160-:432`, above
  `discover()` (`:433`), and found a conflict when helpers sit right after
  `discover()`. Lane 4's ratified change expects `parent_case()` by that name,
  the head refusal at `:383-385`, a changed `known_obstacles()`, and
  `:322-329` untouched (its `design.md:41-43`, `:376-378`).
- **Alternatives considered**: for the head check, W2, just before `Create:`
  (`project:392`): an answer `2` can still meet the generator list and its
  prompt first; W3, before the question for every path: the ratified (a) line
  and its Triad refusal become unreachable, the shape-by-flag text changes, and
  the spec's list of refusals before the question changes (proposal
  `:172-181`). R10's mutants M2 and M3 are W2 and W3. For the helpers, after
  `known_obstacles()` (the packet's prototype place, `:256`): as clean against
  #33, but the spec carries the first; anywhere in `:1-159` (imports,
  `Refused`, `git()`, `confirm()`, `execute()`): adjacent to #33's hunks.

## R3. Sentence (b) is new; (a), the missing sentence and the composition stay (D2)

- **Decision**: the fixed texts of `design.md:136-138` (question lines),
  `:147` (the Triad refusal with (b)) and `:155-156` (the head refusals);
  `Nothing was created.` only on the early refusal; the backstop keeps its raw
  errno.
- **Rationale**: each parent line is true of the path it names and states a
  repair that can work; (b) names the parent and the path that blocks it,
  because (a) naming the ancestor would be false of the parent given, and the
  missing sentence would imply a creation the answer `2` then refuses
  (proposal, "The (b) wording").
- **Alternatives considered**: a Triad-like prefix "A single repository cannot
  be created here." (a flag-chosen path never says "a single repository"
  outside the advisory), or the bare sentence (not saying the file was spared)
  (proposal, "The composition").

## R4. The question keeps one read; the head reads afresh (D1, V2)

- **Decision**: `known_obstacles()` computes its list once (`project:339`) and
  that list feeds the question (`:340`) and the Triad refusal (`:345-346`); the
  head calls `parent_case()` again when it is reached.
- **Rationale**: the question and its Triad refusal must not diverge (archived
  D1), while the head must read the parent as it is at the decision, so that a
  parent repaired while the question waits is created (council V2;
  `clarifications.md:19-31`). The two reads can differ when the parent changed
  during the wait; that is intended (EC-004).
- **Observed**: with `builtins.input` patched in process, a regular file
  replaced by a directory before the answer `2` gave exit 0, the prompts the
  question and `Type yes`, and the repository created; a directory replaced by
  a regular file gave exit 2, the head refusal (a), and only the question's
  prompt.
- **Alternatives considered**: reusing the question's list at the head, which
  turns today's success into a false refusal when the parent is repaired
  (council V2). Mutant M1 of R10 is that alternative.

## R5. The run inventory (D3 items 2 to 10) `[Q1]` `[Q2]` `[Q3]` `[Q4]`

- **Decision**: the tests make exactly the runs below; the plan's D3 places
  each in a method (N1 to N15) or an existing test. A **run** is one call of
  `project` through `run_cli` (`:141`, standard input a pipe), `run_pty`
  (`:210`, standard input and output on a pseudo-terminal, standard error on a
  pipe) or `module.main` in process; one `subTest` row of an existing loop that
  calls `project` once is one run. 101 new runs and the 2 of the rewritten
  test; by runner 49 `run_cli`, 46 `run_pty`, 6 in process (totals in R7).
- **Rationale**: D3 fixes the runs, not the method boundaries; each run here
  has an id, a place, a command and its exact expected result, so a writer
  needs nothing else, and each id is what the plan's method table and the
  traceability record name. Re-checked at `d47e8a4`: `ProjectTests` holds 130
  methods, 96 of them tests (`grep -c '^    def test_'`), 37 `test_pty_*` and
  3 `test_inproc_*`; the precedent fixture is `:58-62`; `pty_timeout = 20` is
  `:146`. The plan's new names (the 15 test methods, `blocked_parents`,
  `run_inproc_acting`, `head_refusal` and the five constants, 23 names)
  collide with no name of the test module at `d47e8a4` or at #33's head
  `ab10102` (`grep -cw`, no hit), and `parent_case` and
  `blocked_parent_sentence` with no name of `project` at either.

**Notation.** `FILE` is a regular file under `self.base` (resolved, `:120`)
holding `parent_file_content`, built by `parent_file_fixture()` (`:419`) under
a name apart from feature 003's `file parent`. `line_a(P)` is
`OBSTACLE_PARENT_NOT_A_DIRECTORY.format(PARENT=P)` (`:62`), `line_b(P, A)` is
`OBSTACLE_PARENT_BELOW_A_NON_DIRECTORY.format(PARENT=P, ANCESTOR=A)` (new).
`HR(line)` is `REFUSED + head_refusal(line)`, that is `REFUSED: ` followed by
the line's sentence and ` Nothing was created.` (`design.md:155-156`).
"Exactly" means whole-stream equality; "ends" means some line ends with the
text (`assert_line_ends()`, `:355`), used where a prompt shares the line.

**The givens** (D3 item 1; the builder `blocked_parents()` returns them in this
order):

| Id | Given | How built | Line | Kept path checked |
| --- | --- | --- | --- | --- |
| K1 | the file | `--into FILE` | `line_a(FILE)` | FILE |
| K2 | a link to the file | `LINK -> FILE`, `--into LINK` | `line_a(FILE)` | FILE |
| K3 | a FIFO | `os.mkfifo(FIFO)`, never opened, `--into FIFO` | `line_a(FIFO)` | `FIFO.is_fifo()` |
| K4 | the file with a trailing slash | `--into` the string `str(FILE) + os.sep` | `line_a(FILE)` | FILE |
| K5 | below the file | `--into FILE/sub` | `line_b(FILE/sub, FILE)` | FILE |
| K6 | two below the file | `--into FILE/a/b` | `line_b(FILE/a/b, FILE)` | FILE |
| K7 | a link below the file | `LINKB -> FILE/x` (dangling), `--into LINKB` | `line_b(FILE/x, FILE)` | FILE |
| K8 `[Q3]` | a socket | an `AF_UNIX` socket bound at `SOCK` and closed, `--into SOCK`; when `bind` raises `OSError` the K8 subtests call `skipTest` | `line_a(SOCK)` | `SOCK.is_socket()` |
| K9 `[Q3]` | `/dev/null` | `--into /dev/null` | `line_a(/dev/null)` | `Path("/dev/null").is_char_device()` |
| K10 | the file, positional | `new MyApp FILE` | `line_a(FILE)` | FILE |
| K11 | the file as `PROJECTS_DIR` | environment `PROJECTS_DIR=FILE`, no `--into` | `line_a(FILE)` | FILE |
| K12 | the file as `~/projects` | a regular file at `HOME/projects` (`HOME` is `self.base/home`, `:134`), `PROJECTS_DIR` removed | `line_a(HOME/projects)` | `HOME/projects` |

"FILE" in the kept-path column means `assert_parent_file_unchanged(FILE,
before)` (`:439`); K12 the same on `HOME/projects`; K3, K8, K9 the type check
named and the snapshot.

**The forms** (AC1's six):

| Id | Form | Runner and environment | Pins |
| --- | --- | --- | --- |
| F1 | `--type test --yes` | `run_cli`; `self.env = self.question_env(None)` for each row, then the row's change | US1.1 (case (a)) or US1.2 (case (b)) |
| F2 | `--type test --dry-run` | as F1 | US1.4; SC-002 |
| F3 | `--type test`, at a terminal, no `--yes` | `run_pty`, no steps; `env=question_env(None)` plus the row's change | US1.3 |
| F4 | no choosing flag, `CI=true`, at a terminal | `run_pty`, no steps; `env=question_env("true")` plus the row's change | US1.5 |
| F5 | no choosing flag, standard input not a terminal | `run_cli`; as F1, so that the runner's own `CI` is not what decides (as `:1654`) | US1.5 |
| F6 | name `alice-wip`, no choosing flag, at a terminal | `run_pty`, no steps; `env=question_env(None)` plus the row's change | US1.5 |

Every form also pins FR-001 (a) or (b), FR-003, FR-005 and SC-001; K3, K8 and
K9 pin EC-001; K2, K4 and K7 pin EC-002. The command is `new NAME` (`MyApp`,
or `alice-wip` for F6), then the given's arguments, then the form's flags.

**The matrix, M01 to M72** (D3 items 2 and 3; plan N1 to N5). Run `Mnn` is
given `K((nn - 1) div 6 + 1)` in form `F((nn - 1) mod 6 + 1)`: M01 to M06 are
K1 in F1 to F6, M07 to M12 are K2, and so on to M67 to M72, K12. Every matrix
run expects: exit 2; standard output empty (a pty run's transcript too, since
no step writes input); standard error exactly `HR(line) + "\n"`, `line` the
given's; for F4 to F6, `assert_not_asked()` (`:369`); the `rglob` snapshot of
`self.base` unchanged, taken after the run's environment is built and just
before the run (`question_env()` creates `self.base/bin`, `:148-152`, so an
earlier snapshot would fail the first run; plan D3, "The snapshot"); the
kept-path check. Each run is one subtest,
`self.subTest(given=LABEL, form="F1")`, keyword parameters only (`subTest()`
takes one positional parameter, `msg`). At the
base every matrix run is red: F1 exits 2 but only after `Create:` and the plan,
with `REFUSED: [Errno 17] File exists: ...` (case (a)) or `[Errno 20] Not a
directory: ...` (case (b)); F2 exits 0 with the plan; F3, F4 and F6 wait at
`Type yes to run this plan:` until `pty_timeout`; F5 exits 2 after `Create:`
and the plan with `Type yes to run this plan: Supply explicit options when
stdin is not a terminal.`. Under Q1 A only 29 of the 72 stay: M01 to M06, M27
(K5 in F3), and F1 and F2 of every other given. Under Q3 B, M43 to M48 (K8)
go; under Q3 C, M43 to M54 (K8, K9).

**The other runs** (D3 items 4 to 10, and this plan's three). `At the base`
is the state at `d47e8a4`; a GREEN run is a guard (R10).

| Run | In | Given and command | Expected | Pins | At the base |
| --- | --- | --- | --- | --- | --- |
| R-3.1 | N5 | FILE; `new alice-wip --into FILE --dry-run` at a pty, no step, `env=question_env(None)` (F6 with `--dry-run`) | exit 2; standard output empty; standard error exactly `HR(line_a(FILE)) + "\n"`; not asked; snapshot and FILE unchanged | US1.4, US1.5; FR-005; SC-002 | red at once: exit 0, the plan printed |
| R-4.1 | N6 | FILE; `new MyApp --into FILE` at a pty, `steps=[(QUESTION_PROMPT, "2")]`; a second available generator appended to `self.config["benches"]["testBench"]["project_scripts"]` and saved first (as `:1066-1068`); `env=shape_env(None)` | exit 2; `assert_question(stdout, "MyApp", line_a(FILE))`; a line of standard error ends with `HR(line_a(FILE))`, and the two streams hold exactly one `REFUSED:`; neither stream holds `GENERATOR_LIST_FIRST`, `GENERATOR_PROMPT`, `Create:` or `CONFIRM_PROMPT`; `shape_record()` is None; snapshot and FILE unchanged; the transcript's tail is not asserted | US2.1; FR-003, FR-005; SC-001 | red, waits at `Select a generator number` |
| R-4.2 | N6 | as R-4.1, with `--dry-run` | as R-4.1 | US2.2; SC-002 | red, waits |
| R-4.3 | N6 | as R-4.1 with `--into FILE/sub` | as R-4.1 with `line_b(FILE/sub, FILE)` | US2.1 | red, waits |
| R-4.4 | N6 | as R-4.3, with `--dry-run` | as R-4.3 | US2.2; SC-002 | red, waits |
| R-5.1 | `test_pty_triad_answer_with_an_obstacle_refuses` (`:1433`) | new row `parent below a file` = `("MyApp", True, ("--into", FILE/sub), [line_b(FILE/sub, FILE)])` of `known_obstacle_cases()`, FILE its `parent_file` (`:404`); the test's answer Enter | its assertions as they stand: exit 2; `assert_question()` with the row's lines; a standard error line ends with `REFUSED + obstacles_refusal(*lines)`; no `ORG_PROMPT`; no `Create:`; no destination; `shape_record()` None (its guard `:1439` is False here, so no file check) | US3.1, US3.2; FR-006, FR-007; SC-003; AC3 | red: entry 1 holds the missing line |
| R-5.2 | the same | new row `all three with the parent below a file` = `("my-app", False, ("--into", FILE/sub), [name_line, OBSTACLE_OPENREPOSHAPE, line_b(FILE/sub, FILE)])` | as R-5.1, the three sentences in that order | the same | red |
| R-5.3 | `test_inproc_triad_obstacle_runs_nothing` (`:1452`) | the row of R-5.1, in process, answer `""` | as it stands: exit 2; prompts `[QUESTION_PROMPT + " "]`; standard output exactly the question; standard error exactly `REFUSED + obstacles_refusal(*lines) + "\n"`; `execute`, `subprocess.run`, `subprocess.Popen`, `socket.socket` never called | US3.2; FR-007; SC-003 | red |
| R-5.4 | the same | the row of R-5.2 | as R-5.3 | the same | red |
| R-5.5 | `test_pty_dry_run_with_an_obstacle_refuses` (`:1477`) | new `cases["parent below a file"] = (("MyApp", "--into", FILE/sub), [line_b(FILE/sub, FILE)])` after `:1490`, FILE its `parent_file`; `--dry-run`, answer Enter | as it stands: exit 2; a standard error line ends with the composed refusal; no `ORG_PROMPT`; no `Create:`; the per-row snapshot (`:1500`); after the loop FILE unchanged (`:1502`) | US3.3; FR-007; SC-002, SC-003; AC3 | red |
| R-5.6 | N7 `[Q2]` | the row of R-5.1, selected by label (the two rows counted), at a pty, answer Enter, as `:1433-1450` | R-5.1's assertions, plus the snapshot taken before and `assert_parent_file_unchanged(Path(extra[1]).parent, before)`: FILE, the ancestor, not `FILE/sub` | FR-014 (A1); US3.1; SC-003 | red: sentence (b) absent |
| R-5.7 | N7 `[Q2]` | the row of R-5.2 | as R-5.6 | the same | red |
| R-5.8 | N8 `[Q2]` | the row of R-5.1, in process, as `:1452-1475` | R-5.3's assertions, plus the check of R-5.6 | the same | red |
| R-5.9 | N8 `[Q2]` | the row of R-5.2 | as R-5.8 | the same | red |
| R-6.1 | the rewritten test (`:1526`) | FILE; `new MyApp --into FILE` at a pty, `steps=[(QUESTION_PROMPT, "2")]`, `env=shape_env(None)` | exit 2; `assert_question(stdout, "MyApp", line_a(FILE))`; no `Create:` in standard output; exactly one `REFUSED:` line, which from `REFUSED:` on equals `HR(line_a(FILE))`; no `warning:`; `shape_record()` None; snapshot and FILE unchanged | US2.3; FR-005, FR-008, FR-014, FR-015; SC-001, SC-006 | red: `Create:`, then a wait at `Type yes` |
| R-6.2 | the same | FILE; `new MyApp --into FILE --type test` at a pty, no step | exit 2; not asked; no `Create:`; its one `REFUSED:` line equals R-6.1's | US2.3; FR-005, FR-014; SC-006 | red, waits at `Type yes` |
| R-7.1 | N9 | P starts as a regular file; `run_inproc_acting("new", "MyApp", "--into", P, ci=None, answers=[act, "yes"])`, `act` replacing P by a directory and returning `"2"` | exit 0; prompts `[QUESTION_PROMPT + " ", CONFIRM_PROMPT + " "]`; standard output has `line_a(P)` (the question was read before the repair), then `Create: P/MyApp`, the plan and `Created:`; `assert_created(P / "MyApp")`; no `REFUSED:` | US4.1; FR-004; SC-007; AC8 | GREEN |
| R-7.2 | N10 | P starts as a directory; `answers=[act]`, `act` replacing P by a regular file holding `parent_file_content` and returning `"2"` | exit 2; prompts `[QUESTION_PROMPT + " "]`; standard error exactly `HR(line_a(P)) + "\n"`; no `Create:`; P still that regular file | US4.2; FR-004, FR-005; SC-007; AC8 | red: `Type yes` is asked |
| R-8.1 | N11 | `LINK -> self.base/"absent target"` (dangling, below a directory); `new MyApp --into LINK --type test --yes`, `run_cli`, setUp's `self.env` | exit 0; standard output exactly `creation_stdout("MyApp", target)` (`:454`); standard error exactly the two `advisory("MyApp")` lines (`:462`); `assert_created(target / "MyApp")`; LINK still a link | US5.1; FR-001, FR-008; EC-003; SC-004; AC4 | GREEN |
| R-9.1 | N12 | FILE; `new MyApp --into FILE --type nomatch --yes`, `run_cli` | exit 2; standard output empty; standard error exactly `HR(line_a(FILE)) + "\n"` | US1.6; FR-003; EC-006; SC-001; AC6 | red: `NO_GENERATOR` |
| R-9.2 | N12 | FILE; `--type test --workflow --yes`; `self.env = question_env(None)` with `assert_absent_from_path(self.env, "setup-openspeckit")` | as R-9.1 | the same | red: `WORKFLOW_MISSING` |
| R-9.8 `[Q4]` | N12 | FILE; `--type test --yes --workbenches DIR`, DIR an empty directory (no `config/bench-config.json`) | as R-9.1 | US1.6; FR-003; EC-006; report A2; the lookup half (the registry half is R-9.10, Q4 C) | red: `Cannot find workBenches; ...` (`project:96`) |
| R-9.3 | N13 | FILE; `new MyApp --into FILE --org example --yes` | exit 2; standard output empty; standard error exactly `REFUSED + ORG_NEEDS_SHAPE + "\n"` | US5.2; FR-003; SC-005; AC5, AC6 | GREEN |
| R-9.4 | N13 | FILE; `new "bad name" --into FILE --type test --yes` | as R-9.3 with `INVALID_NAME` | US5.2; FR-003; SC-005; AC5 | GREEN |
| R-9.7 `[Q4]` | N13 | FILE; `new MyApp --into FILE --family 1bad --yes` | as R-9.3 with `FAMILY_NOT_A_FOLDER_NAME` | US5.2; EC-006; SC-005 | GREEN |
| R-9.5 | N14 | FILE; `new MyApp --into FILE --shape --org example --visibility private` | exit 2; standard output empty; standard error exactly `REFUSED + SHAPE_NEEDS_EXISTING_PARENT + "\n"` | US5.3; FR-009; SC-005; AC5 | GREEN |
| R-9.6 | N14 | as R-9.5, with `--dry-run` | as R-9.5 | the same | GREEN |
| R-9.5b | N14 | as R-9.5 with `--into FILE/sub` (spec US5 scenario 3) | as R-9.5 | the same | GREEN |
| R-9.6b | N14 | as R-9.5b, with `--dry-run` | as R-9.5 | the same | GREEN |
| R-10.1 | N15 | DIR a directory of mode 555 (restore to 755 registered with `addCleanup` first; skipped when `os.geteuid` is missing or returns 0); `new MyApp --into DIR/child --type test --dry-run`, `run_cli` | exit 0; standard output `Create: DIR/child/MyApp` and the plan line; standard error empty; DIR/child not created | US5.4; FR-010; EC-008; SC-008; AC9 | GREEN |
| R-10.2 | N15 | as R-10.1, with `--yes` | exit 2; standard output `Create:` and the plan line, no `Created:`; standard error exactly `f"REFUSED: [Errno {errno.EACCES}] {os.strerror(errno.EACCES)}: '{DIR / 'child'}'\n"`, without `Nothing was created.`; DIR/child not created | US5.5; FR-010; EC-008; SC-008; AC9 | GREEN |

`[Q4]` C adds five runs, each FILE by `--into`, `run_cli`: R-9.9 `new MyApp
FILE --into FILE --type test --yes`, exactly `REFUSED + PARENT_AND_INTO`
(`:79`), GREEN; R-9.10 a `bench-config.json` that is not valid JSON, with
`--type test --yes`, exactly the head refusal (a), red at the base (`Cannot
read ...`, raised by `read_json()`, `project:27-34`, through `registry()`,
`:130`); R-9.11 to R-9.13 `--visibility private`, `--family Products`,
`--elected-by alice`, each with `--yes` and without `--shape`, exactly
`REFUSED + ORG_NEEDS_SHAPE`, GREEN.

R-9.10 is the registry half of US1 scenario 6, FR-003 and EC-006: a malformed
generator registry ordered after the head refusal. `[Q4]` B pins only the
lookup half (R-9.8, which `workbenches()` refuses at `project:83-96`), so a
head check placed between `workbenches()` and `registry()` would pass every
Q4 B run: the registry half is untested under Q4 B and tested under Q4 C, as
the plan's "Not tested" list and its appendix Q4 C say. Under Q4 C, N12 holds
R-9.1, R-9.2, R-9.8 and R-9.10, red in 4 subtests (3 under Q4 B, 2 under
Q4 A).

- **Alternatives considered**: citing the inventory from outside the
  repository (it would not survive the scratch folder; agent R's review
  R01); one method per D3 item (agent T's 12-method split; R7).

## R6. The red-first check runs in a scratch copy with a short pty timeout

- **Decision**: the Phase 2 checkpoint and the V2 record run the new and
  changed tests by name through a small runner that sets
  `test_project.ProjectTests.pty_timeout = 5` for that process only, in a
  scratch copy made by `git archive HEAD | tar -x` with the working tests file
  copied in and `project` taken from `$BASE` (`quickstart.md`, "Red first").
  The committed test keeps `pty_timeout = 20` (`tests/test_project.py:146`).
  Each pty form is its own test method, at most 13 pty runs each.
- **Rationale**: at the base, every pty run with no step that the realization
  ends early (the F3, F4 and F6 forms, 36 runs `[Q1]` `[Q3]`) waits at
  `Type yes to run this plan:`, the four answer-`2` runs wait at
  `Select a generator number`, and the 2 runs of the rewritten test wait at
  `Type yes`, until `pty_timeout`: 42 runs, about 14 minutes at 20 s (R5's "At
  the base" column), beyond a 10-minute foreground command. With the runner, a
  red F3 run on the unpatched copy failed in 5.369 s (observed). A scratch
  runner changes no committed line and no shared state. Under heavy bench load
  (load average 73 to 87 on 32 CPUs), 5 s is still far above a red run's need
  (it only has to show the wait), and the existing tests are not run with it.
- **Observed**: check `red-first` of `quickstart.md`, run on a scratch copy at
  the base whose tests file held the fixture block, the three new rows of R5
  (R-5.1, R-5.2, R-5.5) and stand-in methods for the fifteen new names (each
  red in the planned number of subtests, two of N1's skipped as a failed
  socket `bind` would be), printed `checkpoint as planned` and exited 0: the
  three existing tests red in their new rows only. It exited 1 with `NOT as
  planned` for the unrewritten rewritten test (green) and for an existing
  test whose new rows pass, and with an unknown test name. In its mutant mode
  it exited 0 (`mutant caught`) when every named test was red and 1 when one
  was green. The three existing tests against the D1 prototype: green.
- **Alternatives considered**: lowering `pty_timeout` in the committed test
  (it would flake under load: the slowest pty test took 13.2 s on that bench);
  a sample of red runs (it proves less than every run); a `timeout=` argument
  on each new `run_pty` call (a committed value tuned to one bench).

## R7. The method split and the counts (D3) `[Q1]` `[Q2]` `[Q3]` `[Q4]`

- **Decision**: R5's runs go into 15 new methods (the plan's N1 to N15) and
  three existing tests; the suite goes from `N0`, the merge base's test count,
  to `N0 + 15` (96 to 111 at `d47e8a4`; quickstart check `suite` measures `N0`
  on an export of the merge base, since main gains PR #33's tests before this
  feature lands). The lead ruled to
  keep the split and this plan's three added runs: the shape-by-flag refusal
  for `FILE/sub` with and without `--dry-run` (R-9.5b, R-9.6b; spec US5
  scenario 3, which D3 item 9 names for the file only), and the not-asked dry
  run `alice-wip --into FILE --dry-run` at a pty (R-3.1, which "Considered and
  not asked" allows; at a pty it is not asked for the workspace name alone).
- **Counts**, under the answers given:

  | D3 item | New runs | By runner |
  | --- | --- | --- |
  | 2 (F1, F2, F3) | 36 | `run_cli` 24, `run_pty` 12 |
  | 3 (F4, F5, F6) | 36 | `run_cli` 12, `run_pty` 24 |
  | 3, this plan (R-3.1) | 1 | `run_pty` 1 |
  | 4 (answer `2`) | 4 | `run_pty` 4 |
  | 5 (case (b) rows) | 9 | `run_pty` 5, in process 4 |
  | 7 (repair, break) | 2 | in process 2 |
  | 8 (dangling link) | 1 | `run_cli` 1 |
  | 9 (order; `[Q4]` B) | 8 | `run_cli` 8 |
  | 9, this plan (R-9.5b, R-9.6b) | 2 | `run_cli` 2 |
  | 10 (permission) | 2 | `run_cli` 2 |
  | total | 101 | `run_cli` 49, `run_pty` 46, in process 6 |

  Plus the 2 runs of the rewritten test (item 6, `run_pty`). Of the 101, 5 are
  rows of 3 existing tests (R-5.1 to R-5.5), 96 are in new methods. At about
  0.09 s a run on a quiet machine they add about 9 s; at about 0.5 s a run on a
  heavily loaded bench, about 50 s.
- **Items 2 and 3 by Q1 and Q3** (matrix runs; the other 29 runs of the table
  above do not depend on Q1 or Q3):

  |  | Q3 A (socket and `/dev/null`) | Q3 B (`/dev/null` only) | Q3 C (neither) |
  | --- | --- | --- | --- |
  | Q1 A | 29 | 27 | 25 |
  | Q1 B | 72 | 66 | 60 |
  | Q1 C | 120 | 114 | 108 |

  Q1 C reads Q3 as the clarify file words it: the socket and `/dev/null` by
  `--into` only, six forms each.
- **New runs when one answer differs** (the others as answered): Q1 A 58;
  Q1 C 149; Q2 B 97 (N7 and N8 go: 4 runs, and the suite is `N0 + 13`); Q3 B 95;
  Q3 C 89; Q4 A 99 (R-9.7, R-9.8 go); Q4 C 106 (R-9.9 to R-9.13 come).
  Combined answers add: the matrix from the table above, item 5 from Q2 (9 or
  5), item 9 from Q4 (6, 8 or 13), plus the 4 + 2 + 1 + 2 runs of items 4, 7,
  8 and 10 and this plan's 3.
- **Rationale**: the split gives each delta scenario its own test name for the
  traceability record, and keeps pty methods small (R6): each pty form is a
  method of 12 runs, 13 for N5.
- **The in-process helper**: `run_inproc()` (`:324-346`) pops scripted answers
  that are strings or exceptions, so it cannot replace the parent inside the
  answer prompt. A new helper, `run_inproc_acting()`, whose answers may be
  callables called with the prompt, does it; the existing helper is not edited,
  since lane 4's test module composes `ProjectTests` and its helpers (lane 4
  `design.md:268-275`, `proposal.md:280`). R4's probe used
  `inproc_terminal()` (`:310`) with its own `builtins.input` patch, which is
  what the new helper wraps.
- **Alternatives considered**: agent T's 12-method split (suite 108);
  editing `run_inproc()` to accept callables (an edit to a helper lane 4
  composes).

## R8. The README edits and their rewrap (D2)

- **Decision**: the four texts of `design.md:169`, `:177`, `:184` and `:190`,
  each exact; each refilled from the first line it touches to the end of its
  paragraph, greedily at 79 columns, never breaking at a hyphen or inside a
  word; for the insertion after "Existing destinations refuse." (`README.md:96`),
  `:96` itself kept.
- **Rationale**: 79 is the width of the prose around the edits (no prose line
  of `README.md:48-120` exceeds it but the list item at `:72`, 117 characters,
  unchanged). A break at a hyphen ("single-" / "repository") would defeat the
  joined-line grep. Lines `:53-55` must stay (FR-012).
- **Observed** (the recipe applied by script to a scratch copy): edit 1 fills
  lines 60-68 (`:57-59` unchanged), edits 2 and 3 fill 79-86, edit 4 inserts
  lines 101-105 and leaves the old `:97-98` unchanged below; `:53-55`
  unchanged; no changed line over 79. With the lines joined
  (`tr '\n' ' ' | tr -s ' '`), each fixed text is found once, the joined
  insertion "Existing destinations refuse. A parent blocked by a non-directory
  ..." once, lane 4's phrase "a parent that is a directory the person cannot
  write" once (on one line, 103), and each replaced phrase ("or a parent that
  is missing or is not a directory.", "a parent that exists but is not a
  directory blocks both answers", "a single-repository answer is unaffected.",
  "without the question exactly", "had before the question existed", "its
  answer chose and writes nothing") 0 times. Agent R recomputed the recipe
  independently and got the same lines.
- **The count**: `grep -oF ... | wc -l`, not `grep -c`: on one joined line
  `grep -c` prints 1 for a text found twice, so it cannot prove FR-012's
  "exactly once" (feature 003's quickstart used `grep -c`).
- **Alternatives considered**: a minimal-diff rewrap by hand (not
  reproducible); leaving lines over 79 (the README keeps its width).

## R9. Taking PR #33 in: merge main, never rebase; the base is the merge base

- **Decision**: #33 lands first by agent B's recommended order; this feature
  depends on none of its content. When #33 is on main, the lead re-runs the
  merge check on the real commit, then merges main into this branch at a phase
  boundary (`git merge origin/main`), never a rebase and never a force push
  (the org ruleset refuses force pushes). Every check computes
  `BASE=$(git merge-base origin/main HEAD)`, never a fixed sha.
- **Observed** (2026-10-21; inputs read with `git show` into a scratch
  directory, merged with `git merge-file -p`, merge base `e45155a`, whose
  `project`, README and tests file equal `d47e8a4`'s):
  - #33's head moved during the day: `e256b59`, then `1eb5afa`, then
    `ab10102` (`git ls-remote origin refs/pull/33/head`, read again at
    14:52Z; each earlier head is an ancestor of the next). Only `project`
    differs among the three heads; README and `tests/test_project.py` are the
    same at all three.
  - The prototype `project` and README merge with each head at rc 0, and the
    merged `project` parses with `parent_case` at 272, `blocked_parent_sentence`
    284, `known_obstacles` 292, `new` 372 and `discover` 492 (about +37 above
    `known_obstacles()`).
  - `tests/test_project.py`: a stand-in with a block at every planned test
    site (after `:62`, after `:413`, after `:444`, after `:1490`, the rewritten
    test `:1526-1553`, after `:1553`) merges at rc 0; agent B's own stand-ins
    did too. #33's test hunks are at `:25`, `:1033-1040` and after `:1040`.
  - #33's four gates T009, T046, T128 and T131 read the fixed `961c405` and
    fail once this code is in their tree; re-pointing their baseline to the
    merge base is lane 2's work (agent B).
- **Alternatives considered**: a rebase onto main (refused by the lane's rules
  and by the org ruleset for a pushed branch); a fixed `b233333` base in the
  checks (wrong once main moves).

## R10. Order evidence and mutation checks (D3 item 9)

- **Observed on the base and the prototype** (3.12.3; the prototype's output
  identical on 3.10.21), with a regular file as the parent:
  `--type nomatch --yes`, `--type test --workflow --yes` without
  `setup-openspeckit`, and `--type test --yes --workbenches EMPTY` change from
  their own sentences to the head refusal; `--org example --yes`, an invalid
  name, `--family 1bad`, a positional parent with `--into`, and the
  shape-by-flag refusal for `FILE` and `FILE/sub`, with and without
  `--dry-run`, keep their text; a dangling link by flag is created (exit 0); a
  missing child of a mode-555 directory passes `--dry-run` (exit 0) and fails
  at creation with `[Errno 13] Permission denied` (exit 2).
- **Mutants** (scratch copies of the prototype only), each a plausible wrong
  realization that prints the right sentence:
  - M1, one read before the question reused at the head (V2's rejected
    option): the repaired parent is refused (exit 2) and the broken parent
    reaches `Type yes`: N9 and N10 red.
  - M2, the check after `choose()` (W2): `nomatch` and the empty
    `--workbenches` keep their own sentences: N12 red; with two generators the
    answer `2` would print the list and ask first (by reading
    `project:194-198`, not run): N6 red.
  - M3, the check before the question for every path (W3): `--org` without
    `--shape` and the shape-by-flag rows get the head refusal, and the repaired
    parent is refused before the question: N13, N14 and N9 red.
  - M4, a stray line inside the parent-resolution span lane 4 edits
    (`project:322-329`), or an `open()` call in `parent_case()`: no run need
    notice, so `quickstart.md`'s "The ast check of project" is the guard; it
    fails on both, and on M1 to M3, and passes the prototype.
- **So**: the eleven runs that pass at the base (R-7.1, R-8.1, R-9.3 to R-9.7,
  R-9.5b, R-9.6b, R-10.1, R-10.2) are guards. They cannot show red first, but
  M1 and M3 show they turn red for the wrong realizations they guard against.
  An over-wide check (any missing parent blocked) would turn N11 red, by
  reading.

## R11. Python 3.10 locally

- **Decision**: the local 3.10 gate is a 3.10 interpreter with PyYAML, as in
  CI (`.github/workflows/tests.yml:9`, `requirements.txt`), supplied as
  `quickstart.md` ("Environment") says; it must give `Ran N0+15 tests`, `OK`
  `[Q2]` (check `suite`, which links PyYAML in when the interpreter lacks it). A 3.10 run without PyYAML is informational only.
- **Observed**: agent T ran 3.10.18 (uv, host) with PyYAML linked onto
  `PYTHONPATH` (the system PyYAML 6.0.3, nothing installed): `Ran 96 tests`,
  `OK` at `d47e8a4`. The same recipe in `py-bench` with its uv 3.10.21:
  `Ran 96 tests`, `OK` at `d47e8a4` (45.0 s), and on the prototype exactly the
  one rewritten test fails. The recipe prints `3.10.18 6.0.3 False` on the
  host and `3.10.21 6.0.3 False` in `py-bench` (pure Python PyYAML). Without
  PyYAML, 3.10.21 fails these 11 tests at the base:
  `test_doctor_validate_reports_missing_owner_scripts`,
  `test_doctor_validate_with_a_project_leg_has_structured_output`,
  `test_family_name_prefers_holder_and_inspects_working_sibling`,
  `test_handoff_reads_matching_record_without_changing_it`,
  `test_handoff_rejects_non_github_host_before_record_lookup`,
  `test_handoff_rejects_path_like_remote_identity_before_record_lookup`,
  `test_human_reports_render_present_project_leg_state`,
  `test_shape_skips_assembly_dot_and_reports_missing_legs`,
  `test_shape_update_runs_check_then_apply_and_propagates_failure`,
  `test_update_refuses_a_dirty_family_member`,
  `test_update_refuses_missing_child_and_retains_shape_owner_prompt`
  (`project` imports `yaml` lazily in `read_yaml()`, `:37-41`); the
  prototype fails those 11 and the one test this feature rewrites.
- **Alternatives considered**: accepting the 11 known failures as the 3.10
  gate (it would not be the CI result, and a new YAML-path failure could hide
  among them).

## R12. The five clarify questions (the answers)

`clarify-questions.md` asks five; none changes what `project` does. Brett Heap
answered each on 2026-10-22 ("all recommended"), recorded in the spec's
Clarifications. This plan follows them and says in its appendix, "Options not
taken", what each other option changes:

- `[Q1]` B: AC1's six forms for every kind and route (R5's 72 matrix runs).
- `[Q2]` A: new tests N7 and N8 prove `FILE` intact for the case (b) rows; the
  two existing Triad-answer tests keep every existing line. So one existing
  test is rewritten, and two existing members, `known_obstacle_cases()` and
  `test_pty_dry_run_with_an_obstacle_refuses`, gain added lines only, no
  existing line of theirs removed or changed (N3, AC5, in the spec's sense of
  "unchanged").
- `[Q3]` A: the socket and `/dev/null` are built (R1 shows both are case (a)).
- `[Q4]` B: D3 item 9 plus an invalid `--family` and a `--workbenches` lookup
  fault (R5's R-9.7 and R-9.8). The registry half of US1 scenario 6 (a
  malformed generator registry) is untested under B and pinned by R-9.10 under
  C (R5).
- `[Q5]` A: the change's `tasks.md` ticks go on this branch: 1.6, 2.1 and the
  handoff fields before the first implementation commit, 2.2 once that commit
  exists (R14).

## R13. Lane 4's couplings

- **Decision**: keep the three pins lane 4's ratified change
  `support-later-python-versions` places on this realization: the name
  `parent_case()`; the README phrase "a parent that is a directory the person
  cannot write" exactly once (its realization replaces it character for
  character with "... can search but cannot write", its `design.md:248-256`);
  and no change to `:322-329` or to the harness its new
  `tests/test_parent_reads.py` composes (`setUp`, `run_cli`, `question_env`,
  `shape_env`, `run_pty`, `run_inproc`; its `design.md:268-275` and
  `proposal.md:280`).
- **Rationale**: lane 4's realization lands after this one and merges main in
  (its `tasks.md` 3.1, `design.md` D7). Its D8 will supersede, for a looped
  parent and an unreadable destination, any statement of this feature that the
  archived N1 residuals behave as today; this feature states nothing more than
  `design.md` D6 does.
- **Noted**: the README permission sentence (D2, edit 4) is false for a
  directory that also cannot be searched (mode 000): `destination.exists()`
  raises `[Errno 13]` before the question on 3.10 and 3.12 (spec EC-008). Lane
  4's Decision 12, ratified, scopes it in lane 4's realization; this feature
  keeps D2's text verbatim. After this feature's edit 1, "Existing destinations
  refuse." sits at line 100, not lane 4's cited `README.md:96`; lane 4 replaces
  by text, so nothing breaks.

## R14. The governance ticks go on this branch, by an `[S]` writer, in two commits `[Q5]`

- **Decision**: G1, one commit before the first implementation commit, makes
  the six line replacements of the plan's "G1 and G2 exact text" in
  `openspec/changes/refuse-non-directory-parent-early/tasks.md`: it ticks 1.6
  (the quote "ratify 21" and its link, the squash
  `b23333397f989462d13cf625c69e41bee8da8700` of `8f3ca2d`) and 2.1 (the
  feature, branch, worktree, base and spec), and fills the Speckit Handoff
  prose line and its three fields (lines 31, 36, 37, 38, every line that holds
  "to be created"). G2, one commit in Phase 4, ticks 2.2 with "Met: the handoff
  named feature 006-refuse-non-directory-parent-early at G1SHA before the first
  implementation commit FIRSTSHA.", the two short shas found by `git log`.
  3.1 to 3.3 wait for the landing and the archive. An `[S]` writer copies the
  text (lead's ruling). "The first implementation commit" is the first commit
  on the branch that touches `project`, `tests/test_project.py` or `README.md`;
  commits under `specs/` (spec, plan, tasks, `qs.sh`, the traceability
  skeleton) are record commits, not implementation commits, so FIRSTSHA's
  `git log` names those three paths only.
- **Rationale**: this is what feature 003 did. Its specify commit `90a4cee`
  ticked 1.6 and 2.1 and filled the handoff fields, and left 2.2 unticked; its
  branch's last commit ("Tick T001 to T018 on the verified evidence; fix the
  Phase 2 checkpoint; tick OpenSpec 2.2", in the message of squash `f401e06`)
  ticked 2.2 with "Met: the handoff named feature 003-parent-obstacle-wording
  at 90a4cee before the first implementation commit f492558"
  (`openspec/changes/archive/2026-10-09-fix-parent-obstacle-wording/tasks.md:21`).
  2.2 records a verification whose evidence, the first implementation commit,
  does not exist when G1 runs, so it is ticked once it does. The record lands
  in the PR that does the work, without a second PR (clarify Q5, option A).
  This is Q5 A as Brett Heap answered it (the clarify file, as corrected at
  `f700336`): 2.2 is ticked later in the same PR.
- **Observed**: `quickstart.md`'s `check_ticks.py` (inside check
  `governance`), which extracts the exact
  text from the plan, applied G1 and then G2 (with stand-in shas) to a scratch
  copy of the file at `d47e8a4`: every "before" line matched; after G1, one
  `- [x]` each for 1.6 and 2.1, 2.2 still `- [ ]`, three open `- [ ] 3.x`, 0
  "to be created", 6 lines removed and 6 added, 0 non-ASCII; after G2, 2.2
  ticked with its "Met:" line, 1 line changed against G1; `/usr/bin/openspec
  validate refuse-non-directory-parent-early --strict` valid and `--all
  --strict` 9 of 9 at both stages. A one-space change to a G1 line made the
  script fail with its diff. The whole check `governance`, run with a stand-in
  for the few `git` calls that need a commit, exited 0 at both stages and 1
  for a wrong line count, for the G2 file checked as G1, and for the
  one-space change. Today no commit after the merge base touches the
  file or an implementation path, so the G2 `git log` commands print nothing
  until G1 and the first implementation commit exist.
- **Alternatives considered**: a separate governance PR to main before
  `/opsx:apply` (Q5 B: FR-016 stands as written, at the cost of a second PR);
  ticking 2.2 in G1 (it would record a verification before its evidence
  exists); the lead's own edit (ruled out in favour of an `[S]` writer).

## R15. Every check runs through one committed runner, `qs.sh`

- **Decision**: `specs/006-refuse-non-directory-parent-early/qs.sh` (its text is
  the plan's "qs.sh (exact text)") takes the fenced block of `quickstart.md`
  whose first line is `# check: ID`, exports `BASE` and each `NAME=VALUE`, runs
  the block with bash from the top of the worktree, and exits with the block's
  status. Every verify is `bash specs/006-refuse-non-directory-parent-early/qs.sh
  ID [NAME=VALUE ...]`; the tests of one task go in `TESTS` for check
  `red-first`; a check that must fail (mutant M4) is read as exit 1, because
  the runner itself exits 2 when the marker is missing or repeated or an
  argument is bad. The twelve blocks stay the single source of check code. The
  lane lead commits `qs.sh` with the plan (no build task edits it), and check
  `files-changed` requires it among the committed changes.
- **Rationale**: the Bash tool keeps no shell state between calls. An earlier
  form extracted blocks with a `qs_check` function and a random `mktemp -d`
  directory, defined once in a setup block outside every task line, and read
  `$BASE` the same way; a verify run in its own call then failed for want of
  those names, and under the build rules a failed verify fails the task and
  escalates its tier (the cross-artifact analysis of the drafts found it). One
  committed file is read once by the reviewer and needs no prelude in any
  verify. `BASE` is computed in one place, so a caller's stale `BASE` cannot
  leak in (an ambient `BASE` is ignored; `BASE=<sha>` overrides). Inside a git
  work tree the script must be that work tree's own copy, so a check cannot run
  against another tree by mistake; outside one it stays in the current
  directory, which a plain scratch copy needs.
- **Observed** (a scratch copy of the feature directory, `qs.sh` beside the
  quickstart, with no git repository and `BASE` passed; and a git stand-in for
  the calls the runner and the blocks make): check `openspec` ran and exited 0
  (`Change 'refuse-non-directory-parent-early' is valid`, `Totals: 9 passed, 0
  failed`) and exited 1 with `OPENSPEC=/bin/false`; an unknown id, a copy with
  one marker line removed, and a copy with the `ascii-added` block repeated
  each printed a message and exited 2; a block `exit 7` appended to the copy
  came out as 7; run from a subdirectory, the block ran at the top of the work
  tree; `BASE=<sha>` replaced the default and a `BASE` in the environment was
  ignored; standard input reached the block; a value with spaces and an equals
  sign arrived whole; a script outside the work tree it was run in exited 2.
  The runner extracted all twelve blocks, each beginning with its marker, and
  each passed `bash -n`; check `governance` through the runner passed at `g1`
  and at `g2` and failed `g1` on the `g2` file; check `files-changed` passed
  for the full expected set and failed for a missing `qs.sh`, a stray file and
  a feature 003 record.
- **Alternatives considered**: a prelude block copied to the top of every
  verify (a copy of one text in each); a fixed scratch directory for the
  extracted checks (state shared between lanes and runs); one script file per
  check (twelve copies of the check code next to the quickstart's); positional
  test names for `red-first` (the runner takes `NAME=VALUE` only, so they go in
  `TESTS`).
