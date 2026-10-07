Lane: openRepoProject-1

# Tasks: Triad-first project creation

**Input**: Design documents from `specs/002-triad-first-project-new/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md,
contracts/project-new.md, quickstart.md; the technical design is
`openspec/changes/prefer-triad-in-project-new/design.md` (D1 to D14), which
governs wherever a task is shorter.

**Tests**: Required. `design.md` D14 and SC-010 require at least one automated
test for each of the 47 scenarios of the spec delta
(`openspec/changes/prefer-triad-in-project-new/specs/project-command/spec.md`).
Each story phase lists its tests first; write them, see them fail, then
implement. Each test task names the delta scenario(s) it covers.

**Organization**: Tasks are grouped by user story to enable independent
implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1 to US5)
- Include exact file paths in descriptions

## Path Conventions

One executable, `project`, at the repository root; one test module,
`tests/test_project.py`; documentation in `README.md` and `AGENTS.md`; feature
files under `specs/002-triad-first-project-new/`. No other file changes.

## Rules for every new test (D14)

- A pty-driven test's name starts with `test_pty_` (so `-k test_pty_` runs them
  alone); an in-process test's name starts with `test_inproc_`.
- Every question and advisory test sets `CI` explicitly (a value, or removed)
  through the T004 helper, which also drops `GH_TOKEN`, `GITHUB_TOKEN` and every
  `OPENREPOSHAPE_*` variable and builds `PATH` from a temporary bin directory.
- Every test that runs a fake asserts that `PATH` resolves it; every test that
  needs a tool absent asserts that `PATH` resolves none.
- Expected text comes from the T003 fixtures only; no test reads history, and no
  test asserts which stream a prompt appears on.
- The 43 existing test methods are not edited; new helpers and tests are added
  to `ProjectTests` after the existing ones, helpers beside `run_cli`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Baseline and the traceability record

- [ ] T001 Confirm the baseline in this worktree: `python3 -m unittest discover -s tests -v` passes 43 tests in tests/test_project.py, and `project` is unchanged from `ca4c615`
- [ ] T002 [P] Create specs/002-triad-first-project-new/traceability.md (lane line first): a table of the 47 delta scenarios, by requirement and scenario title, with an empty test-name column that each test task fills as its test lands

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The test harness, and the one decision value every story reads

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 Add the D13 fixtures as string literals in tests/test_project.py: the question (header, entry 1, the three obstacle lines, entry 2), the three prompts, the three retry lines, the refusals (the composed known-obstacles refusal built from the obstacle sentences), the two restating forms and the two advisory lines, with NAME, ORG, VIS and PARENT as format fields, character for character as `design.md` D13
- [ ] T004 Add the environment helper beside `run_cli` in tests/test_project.py: from `self.env`, set or remove `CI` (a required argument), drop `GH_TOKEN`, `GITHUB_TOKEN` and every `OPENREPOSHAPE_*` key, and set `PATH` to a temporary bin directory plus the directories of `bash`, `git` and `sys.executable` (D14)
- [ ] T005 Add the fakes to tests/test_project.py: a writer for the fake `openRepoShape` in the temporary bin directory (appends its argv to a record file beside itself, prints `Type yes to continue: `, reads one line, on `yes` creates `<--into>/<name>` and exits 0 or a status the test sets, otherwise prints `not confirmed; nothing was created.` and exits 1) and for the fake `setup-openspeckit` (prints one marker line carrying its arguments on stdout and on stderr, then exits with a status the test sets), plus helpers asserting `shutil.which(tool, path=env["PATH"])` is the fake or `None` (D14)
- [ ] T006 Add the pty helper beside `run_cli` in tests/test_project.py: stdin and stdout on one `os.openpty()` slave, stderr on its own pipe; `subprocess.Popen` with `start_new_session=True`, and the test's own slave descriptor closed after `Popen`; a `select` loop draining the master and the stderr pipe until the child exits, treating `EIO` and an empty read as end of output; a script of steps, each written only after its expected prompt or line has appeared on either stream, where a step is a line of text, the EOF character `\x04`, or SIGINT sent with `send_signal` and repeated until the child exits; `\r\n` normalised to `\n`, echoed input ignored; a timeout on every run; no `pty.fork`; returns the exit status, the pty transcript and stderr (D14, research R2)
- [ ] T007 Add the in-process helper beside `run_cli` in tests/test_project.py: runs `module.main(argv)` with `builtins.input` patched to scripted answers (an answer may raise `EOFError` or `KeyboardInterrupt`), the `isatty` of `sys.stdin` and of `sys.stdout` patched independently after stdout and stderr are redirected to `io.StringIO`, and `CI` set with `patch.dict(os.environ, ...)` (D14)
- [ ] T008 Add `test_inproc_person_at_terminal_rule` in tests/test_project.py: true with both streams terminals and `CI` unset, empty, `0`, `false`, `no`, ` FALSE ` or ` No `; false for `true`, `1`, `yes` or `anything`; false when either stream is `None`, is not a terminal, or its `isatty` raises `OSError`, `ValueError` or `AttributeError` (D1). Scenarios: Not at a terminal; CI is set
- [ ] T009 Add `person_at_terminal()` to project (D1); T008 passes
- [ ] T010 [P] Add `ASSEMBLY_NAME` and `WORKSPACE_NAME` to project, compiled patterns used with `fullmatch`, each with its openRepoShape `contracts/repository-naming.yaml` line (`:345`, `:412`) and sha `1a9fc537bcce37301c85fc108fabd8a599b02000` in a comment beside it (D3, D10)
- [ ] T011 In `new()` in project, immediately after the existing-destination refusal, compute `workspace`, `chosen` (switches when set, valued options when not `None`) and `offer` once (D1, D2 step 2); nothing reads `offer` yet, and the 43 existing tests still pass

**Checkpoint**: Harness ready and `offer` computed; story work can begin

---

## Phase 3: User Story 1 - Offered the Triad first at the terminal (Priority: P1) MVP

**Goal**: A person at a terminal without a choosing flag is asked the question; the single-repository answer, retries, refusals and interrupts work end to end.

**Independent Test**: At the pty with `CI` removed, run `project new MyApp` against the fixtures, answer each way, and check the path that continues and that nothing exists before `Type yes` is answered.

### Tests for User Story 1

- [ ] T012 [US1] Add `test_pty_question_is_asked_once_the_name_is_known` in tests/test_project.py: with the name given and with it typed at `Project name:`, and with `--into`, a positional parent or `--workbenches` given, the question header appears after the name and before any generator list (two available generators configured; after `2` the list follows the header), plan or confirmation; ends with end of input at the generator number (130). Scenario: A person at the terminal without a choosing flag
- [ ] T013 [US1] Add `test_pty_question_entries` in tests/test_project.py: header, entry 1 and entry 2 equal the fixtures, entry 1 first and marked default, no obstacle line in this fixture; no `single-repository.yaml` exists under the fixture root afterwards. Scenario: The question's entries
- [ ] T014 [US1] Add `test_pty_single_answers_take_the_bench_path` in tests/test_project.py: each of `2`, `n`, `no`, `N`, ` No ` (subTest) continues to the plan and `Type yes`; `yes` creates the destination and `.project.json`; stderr carries no `warning:` line. Scenario: Answers that take a single repository
- [ ] T015 [US1] Add `test_pty_single_answer_is_not_a_confirmation` in tests/test_project.py: `2`, then `no` at `Type yes`: `REFUSED: Cancelled; no command was run.`, exit 2, destination absent. Scenario: An answer is not a confirmation (single repository)
- [ ] T016 [US1] Add `test_pty_one_unrecognised_answer_is_asked_again` in tests/test_project.py: `3` then `2`, and `maybe` then `n` (with `--dry-run`): the question retry line once, the prompt again, then the bench plan. Scenario: One unrecognised answer
- [ ] T017 [US1] Add `test_pty_two_unrecognised_answers_refuse` in tests/test_project.py: `3` then `maybe`: the question second-miss refusal, exit 2, destination absent, generator not run, fake `openRepoShape` record absent. Scenario: Two unrecognised answers
- [ ] T018 [US1] Add `test_pty_end_of_input_at_the_question_refuses` in tests/test_project.py: the question end-of-input refusal, exit 2, nothing created. Scenario: End of input at the question
- [ ] T019 [US1] Add `test_pty_interrupt_at_the_question_cancels` in tests/test_project.py: SIGINT at the question: `Cancelled.`, exit 130, nothing created. Scenario: An interrupt at the question
- [ ] T020 [US1] Add `test_pty_end_of_input_at_existing_prompts_is_unchanged` in tests/test_project.py: end of input at `Project name:`, and at `Type yes` after `2`: `Cancelled.`, exit 130. Scenario: End of input at an existing prompt is unchanged
- [ ] T021 [US1] Add `test_pty_dry_run_single_answer_prints_the_generator_plan` in tests/test_project.py: `--dry-run` with `--into` a new path, `2`: `Create:` and the generator command, exit 0, the parent not created, no `warning:` line. Scenarios: A dry run asks too (single repository); Preview (single repository)
- [ ] T022 [US1] Add `test_pty_refusals_before_a_path_come_first` in tests/test_project.py: an invalid name, a positional parent with `--into`, and an existing destination each refuse with today's text and exit 2, and no question line appears. Scenarios: Refusals before a path is chosen come first; Existing project

### Implementation for User Story 1

- [ ] T023 [US1] Add to project the question printer (header, entry 1, the obstacle sentences it is given as `Not possible here:` lines, entry 2, all with `print()` to stdout; D13) and the one ask-twice helper over `ask()` (prompt, accepted answers, retry line, second-miss refusal, end-of-input refusal; `EOFError` around each `ask()` call raised as `Refused`; `KeyboardInterrupt` not caught) (D4)
- [ ] T024 [US1] In `new()` in project, when `offer`: print the question (with no obstacles until T041), ask with the D13 question prompt, retry line and refusals, and route: a single-repository answer sets nothing and continues into the unchanged bench branch (D6); a Triad answer continues into the steps T034 and T041 add; T012 to T022 and the 43 existing tests pass

**Checkpoint**: The question and the single-repository answer work end to end; the Triad answer gains its steps in Phase 4 (US1 and US2 are both P1 and ship together as the MVP)

---

## Phase 4: User Story 2 - Creating the Triad from the answer (Priority: P1)

**Goal**: A Triad answer asks for the organization and the visibility, restates them, and delegates to openRepoShape without `--yes`.

**Independent Test**: At the pty with the fake `openRepoShape`, take the Triad, type an organization and a visibility, and check the restating line, the recorded argv, and that nothing exists until the fake's confirmation is typed.

### Tests for User Story 2

- [ ] T025 [US2] Add `test_pty_answers_that_take_the_triad` in tests/test_project.py: each of Enter, `1`, `y`, `yes`, `Y`, ` YES ` (subTest) leads to the organization prompt; end of input there refuses with exit 2; fake record absent. Scenario: Answers that take the Triad
- [ ] T026 [US2] Add `test_pty_organization_then_visibility` in tests/test_project.py: Enter, then `-bad`: the organization retry line and the organization prompt again, with no visibility prompt before it; then `example`: the visibility prompt follows. Scenario: Organization first, then visibility
- [ ] T027 [US2] Add `test_pty_visibility_is_a_full_word` in tests/test_project.py: `PUBLIC` and ` private ` are accepted as `public` and `private` (seen in the restating line and the recorded argv); `1`, `2`, `3` and an empty answer each draw the visibility retry line. Scenario: The visibility is a full word
- [ ] T028 [US2] Add `test_pty_two_misses_at_organization_or_visibility_refuse` in tests/test_project.py: empty then `-x` at the organization, and `1` then empty at the visibility: each second-miss refusal, exit 2, fake record absent. Scenario: Asked once more, then refused
- [ ] T029 [US2] Add `test_pty_end_of_input_at_organization_or_visibility_refuses` in tests/test_project.py: each end-of-input refusal, exit 2, nothing created. Scenario: End of input at the organization or visibility prompt
- [ ] T030 [US2] Add `test_pty_interrupt_at_organization_or_visibility_cancels` in tests/test_project.py: SIGINT at each prompt: `Cancelled.`, exit 130, nothing created. Scenario: An interrupt at the organization or visibility prompt
- [ ] T031 [US2] Add `test_pty_restating_line_precedes_the_plan` in tests/test_project.py: the `private` and `public` forms equal the fixtures and appear before `Create:`. Scenario: The restating line
- [ ] T032 [US2] Add `test_pty_triad_delegates_without_yes_and_keeps_its_confirmation` in tests/test_project.py: Enter, `example`, `private`; the fake's prompt appears; `yes` creates `<parent>/<name>`, exit 0, recorded argv `NAME --org example --visibility private --into PARENT` without `--yes`; `no` instead: `not confirmed; nothing was created.`, exit 1, destination absent; no `warning:` line in either run. Scenarios: Delegation keeps openRepoShape's confirmation; An answer is not a confirmation (Triad)
- [ ] T033 [US2] Add `test_pty_openreposhape_refusal_passes_through` (the fake set to exit 5 after `yes`: exit 5) and `test_pty_dry_run_triad_answer_prints_the_openreposhape_plan` (`--dry-run`, Enter, `example`, `private`: the restating line, `Create:`, the openRepoShape command, exit 0, fake record absent, nothing written, no `warning:`) in tests/test_project.py. Scenarios: openRepoShape refuses; A dry run asks too (Triad); Preview (Triad)

### Implementation for User Story 2

- [ ] T034 [US2] In `new()` in project, after a Triad answer with no obstacle: the organization prompt (accepted on a full match of today's `[A-Za-z0-9][A-Za-z0-9-]*`, kept as typed) and then the visibility prompt (the lower-cased word, one of `private`, `public`, `internal`), both through the T023 helper with their D13 prompts, retry lines and refusals; set `args.shape = True`, `args.org` and `args.visibility`; print the restating line (the `public` form for `public`) before the unchanged `args.shape` branch (D5, D2 step 4); T025 to T033 pass

**Checkpoint**: MVP complete: the question offers the Triad first and both answers reach their own confirmations

---

## Phase 5: User Story 3 - Known obstacles named beside the Triad (Priority: P2)

**Goal**: The three local facts are read before the question, named under the Triad, and refused at once on a Triad answer.

**Independent Test**: At the pty, run with `my-app`, with no `openRepoShape` on PATH, and with a missing parent; read the Triad entry, take the Triad (exit 2, fake never run), then take the single repository (the bench path proceeds).

### Tests for User Story 3

- [ ] T035 [US3] Add `test_pty_name_outside_the_assembly_form_is_named` in tests/test_project.py: `my-app`: entry 1 is still first and the default, followed by the name obstacle line for `my-app`. Scenario: A name outside the assembly-root form
- [ ] T036 [US3] Add `test_pty_missing_openreposhape_is_named` in tests/test_project.py: `PATH` asserted to resolve no `openRepoShape`; the openRepoShape obstacle line follows entry 1. Scenario: openRepoShape is not on PATH
- [ ] T037 [US3] Add `test_pty_missing_parent_is_named_without_into` in tests/test_project.py: `PROJECTS_DIR` set to a missing directory with no `--into`, and `--into` a missing directory: the parent obstacle line names the resolved directory, and no question line contains `--into`. Scenario: The parent directory is missing
- [ ] T038 [US3] Add `test_pty_triad_answer_with_an_obstacle_refuses` (each obstacle alone, and all three in the order name, openRepoShape, parent: Enter gives the composed known-obstacles refusal, exit 2, no organization prompt, fake record absent, destination absent) and `test_inproc_triad_obstacle_runs_nothing` (the same in process with `execute`, `subprocess.run`, `subprocess.Popen` and `socket.socket` patched to fail if called) in tests/test_project.py. Scenario: A Triad answer with a known obstacle
- [ ] T039 [US3] Add `test_pty_dry_run_with_an_obstacle_refuses` in tests/test_project.py: `--dry-run`, an obstacle, Enter: exit 2, nothing written. Scenario: A dry run with a known obstacle
- [ ] T040 [US3] Add `test_pty_single_answer_is_unaffected_by_obstacles` (all three obstacles, `2`, `yes`: the same plan and creation as without obstacles, exit 0) and `test_pty_no_known_obstacle_names_none` (an assembly-form name, the fake on PATH, an existing parent: no `Not possible here:` line) in tests/test_project.py. Scenarios: A single-repository answer is unaffected; No known obstacle

### Implementation for User Story 3

- [ ] T041 [US3] Add the obstacle reader to project (D3): `ASSEMBLY_NAME.fullmatch(name)`, `shutil.which("openRepoShape")` and `parent.is_dir()` in that order, no network and no subprocess, returning the D13 obstacle sentences; in `new()`, read it when `offer`, pass the sentences to the question printer, and on a Triad answer with any obstacle raise the D13 known-obstacles refusal before the T034 prompts; T035 to T040 pass

**Checkpoint**: Known obstacles are named and refused; the single-repository answer is unaffected

---

## Phase 6: User Story 4 - Scripted creation keeps its path and is advised on standard error (Priority: P2)

**Goal**: Flag-chosen and non-interactive runs are never asked; a single repository they create is followed by the guarded two-line advisory on stderr.

**Independent Test**: Create with `--type test --yes` through a pipe; compare stdout, files, `.project.json` and the exit status with pinned expectations; check stderr for exactly the two lines; repeat with stderr closed, on a broken pipe and on a full device.

### Tests for User Story 4

- [ ] T042 [US4] Add `test_pty_choosing_flags_skip_the_question` in tests/test_project.py: at the pty with `CI` removed, each of the nine choosing flags (subTest) gives no question line and today's outcome for that flag, pinned per flag; `--description ""` (an empty value) also skips it. Scenario: A choosing flag skips the question
- [ ] T043 [US4] Add `test_pty_shape_chosen_by_flag_keeps_openreposhape_confirmation` in tests/test_project.py: `--shape --org example --visibility private`, with and without `--yes`: no question line, the fake's prompt appears, recorded argv without `--yes`, `yes` creates, no `warning:` line; and `my-app` with the same flags reaches the fake (record present) with no pre-check, its exit status passed through (EC-009). Scenario: Shape chosen by flag
- [ ] T044 [US4] Add `test_new_without_a_terminal_is_not_asked` (`run_cli`, stdin a pipe, no flag: no question line, today's refusal at `Type yes`) and `test_inproc_stdout_not_a_terminal_is_not_asked` (stdin a terminal, stdout not: no question line; `yes` creates; captured stderr holds the two advisory lines) in tests/test_project.py. Scenarios: Not at a terminal; A single repository created where the question is not asked (stdout not a terminal)
- [ ] T045 [US4] Add `test_pty_ci_decides_the_question` in tests/test_project.py: `CI` of `true`, `1`, `yes` or ` TRUE ` gives no question line; empty, `0`, `false`, `no`, ` FALSE ` or ` No ` gives the question. Scenario: CI is set
- [ ] T046 [US4] Add `test_advisory_after_a_flag_chosen_single_repository` in tests/test_project.py: `run_cli` with `CI` set and `--type test --yes`: stdout equals the pinned stdout (built from the fixture paths with `shlex.join` and `shlex.quote`), the generator's files and `.project.json` as pinned, exit 0, stderr exactly the two advisory lines, and no `.git` in the destination. Scenarios: A single repository chosen by flag; A generator that initialises no Git repository
- [ ] T047 [US4] Add `test_pty_advisory_where_ci_is_true` in tests/test_project.py: `CI=true` at the pty, no flag, `yes` at `Type yes`: the two advisory lines on stderr after creation. Scenario: A single repository created where the question is not asked (CI)
- [ ] T048 [US4] Add `test_advisory_content` in tests/test_project.py: both fixture lines begin `warning:`, are ASCII, and carry "preferred, not required", "elective", "confers nothing", `adopt-project.py` with "a person deciding for this project", `single-repository.yaml` and "Nothing here changes"; T046's emitted lines equal them. Scenario: The advisory's content
- [ ] T049 [US4] Add `test_advisory_silent_cases` in tests/test_project.py: no `warning:` on stderr for `--type test --dry-run`, a `--shape` creation through the fake, a generator exiting 17, and a generator exiting 0 without creating the destination (exit 2); the question and workspace cases are T014, T032 and T054. Scenario: Silent cases
- [ ] T050 [US4] Add `test_advisory_with_stderr_closed` (`/bin/sh -c 'exec "$@" 2>&-' sh ...`), `test_advisory_with_stderr_on_dev_full` (skipped where `/dev/full` does not exist) and `test_advisory_with_stderr_on_a_closed_pipe` (stderr a pipe whose read end is closed) in tests/test_project.py: each run's stdout equals T046's pinned stdout and carries no `warning:`, exit 0, destination and `.project.json` present. Scenario: Standard error cannot be written
- [ ] T051 [US4] Add `test_advisory_is_never_a_report_input` in tests/test_project.py: `status` and `doctor`, human and `--json`, on a repository created with `--type test --yes` (advised) equal those on the same name created through the question (`2`, `yes`) under another parent, after replacing the root path; both destinations hold the same files. Scenario: Never a report input

### Implementation for User Story 4

- [ ] T052 [US4] Add the creation advisory writer to project (D7 steps 1 to 5, the two D13 lines with NAME): flush stdout if present; nothing when `sys.stderr` is `None`; ASCII bytes with `errors="replace"` through `os.write` on `sys.stderr.fileno()` in a short-write loop, else `sys.stderr.write()`; swallow `OSError`, `ValueError` and `AttributeError`
- [ ] T053 [US4] In `new()` in project, call the writer after the `.project.json` block and before the follow-up loop, only when `row` and `not offer and not workspace` (D2 step 6, D7); T042 to T051 and the 43 existing tests pass

**Checkpoint**: Scripted runs are unchanged on stdout and advised on stderr; the advisory cannot fail a run

---

## Phase 7: User Story 5 - Workspace names and the workflow follow-up (Priority: P3)

**Goal**: A `-wip` name gets no question and no advisory; under `--workflow` the offer comes first and the follow-up runs as before.

**Independent Test**: Create `alice-wip` (no question, no advisory); then, with the fake `setup-openspeckit`, create with `--yes --workflow` with both streams merged and check that both `warning:` lines precede the marker.

### Tests for User Story 5

- [ ] T054 [US5] Add `test_pty_workspace_name_is_not_asked_or_advised` (`alice-wip` at the pty, no flag: no question line, today's plan and `Type yes`, `yes` creates, no `warning:`) and `test_workspace_name_by_flag_gives_no_advisory` (`run_cli`, `alice-wip --type test --yes`: no `warning:`, stdout as pinned) in tests/test_project.py. Scenarios: A workspace name; Silent cases (workspace name)
- [ ] T055 [US5] Add `test_workflow_advisory_precedes_the_follow_up` in tests/test_project.py: the fake `setup-openspeckit` asserted on PATH; `run_cli` with `--type test --yes --workflow` and stderr merged into stdout: both advisory lines precede the marker, and the marker carries `--repo DEST`. Scenario: Two advisories back to back
- [ ] T056 [US5] Add `test_workflow_follow_up_failure_keeps_the_advisory` in tests/test_project.py: the fake exits 3, and 130: the exit status is the fake's; stderr holds both advisory lines, then `Project created at DEST; workflow setup failed.`. Scenario: The follow-up fails
- [ ] T057 [US5] Add `test_pty_single_answer_with_workflow_adds_no_advisory` in tests/test_project.py: `--workflow`, `2`, `yes`: the marker carries `--repo DEST`, and no `warning:` line comes from `project`. Scenario: A single-repository answer with --workflow
- [ ] T058 [US5] Add `test_workflow_workspace_name_gives_no_advisory` in tests/test_project.py: `bob-wip --type test --yes --workflow`: no `warning:` line; the marker appears. Scenario: A workspace name with --workflow
- [ ] T059 [US5] Add `test_pty_workflow_prerequisite_is_refused_before_the_question` in tests/test_project.py: `PATH` asserted to resolve no `setup-openspeckit`; `--workflow` with no choosing flag: `REFUSED: --workflow requires setup-openspeckit on PATH.`, exit 2, no question line. Scenario: The workflow prerequisite is refused before the question
- [ ] T060 [US5] Add `test_workflow_refusal_order_unchanged_when_not_asked` in tests/test_project.py: `run_cli` with `--type nope --workflow` and no `setup-openspeckit`: `REFUSED: No matching generator; run project benches.`, exit 2. Scenario: The refusal order of an invocation not asked the question is unchanged

### Implementation for User Story 5

- [ ] T061 [US5] In `new()` in project, right after computing `offer`: when `offer` and `args.workflow` and `shutil.which("setup-openspeckit")` is `None`, raise today's `--workflow requires setup-openspeckit on PATH.` refusal, leaving today's later check in place (D2 step 3, D8); T054 to T060 pass (T054, T055 and T058 may pass before this task, since `workspace` and the advisory guard come from T011 and T053; they pin that behaviour)

**Checkpoint**: Every user story is complete

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: FR-024 documentation, traceability and verification

- [ ] T062 [P] Update the "Create a project" section of README.md (FR-024): the question (Triad first and the default; Enter, `1`, `y`, `yes` or `2`, `n`, `no`; one retry; the known obstacles named beside the Triad; what skips it: the nine choosing flags, a stdin or stdout that is not a terminal, a `CI` value other than empty, `0`, `false` or `no`, a workspace name; a dry run asks too), the organization and visibility prompts and the restating line, the two-line advisory on stderr after a single repository created without the question, the second offer under `--workflow` (D8), what Ctrl-C does while openRepoShape runs (D9, in substance), and the agent sentence (D11); correct the sentence "Before running, the command shows the generator and destination and asks for `yes`" for the new first question
- [ ] T063 Add a `CI` row to the Configuration table of README.md (FR-024): a value other than empty, `0`, `false` or `no` means `project new` asks no creation question
- [ ] T064 [P] Add a short agent section to AGENTS.md (FR-024, D11): offer the Triad in conversation in the shared protocol's words, then run `project new` with a choosing flag (`--shape --org --visibility`, or `--bench` and `--type`), and never answer the creation question, the organization, the visibility or openRepoShape's confirmation on a person's behalf; leave the OPENSPEC-SPECKIT-GLOBAL block untouched and do not edit CLAUDE.md
- [ ] T065 Read README.md alone and confirm SC-011: the question's default, the answers that take each path, the flags that skip the question, and how to create a single repository without being asked are all stated
- [ ] T066 Complete specs/002-triad-first-project-new/traceability.md: all 47 delta scenarios each name at least one test, and every named test is defined in tests/test_project.py (checked by script: 47 rows, no empty test cell, each name found as `def NAME`)
- [ ] T067 Check the fixtures in tests/test_project.py against `design.md` D13 by script: every fixture equals a D13 line or quoted string character for character, placeholders included, and every D13 string has a fixture (SC-008)
- [ ] T068 Run the full suite in this worktree: `python3 -m unittest discover -s tests -v` passes, the 43 existing tests among them; `git diff "$BASE" -- tests/test_project.py`, where `BASE=$(git log --diff-filter=A --format=%H -1 -- specs/002-triad-first-project-new/tasks.md)`, deletes no line; where a Python 3.10 interpreter is available, run the suite under it as well (CI runs 3.10 and 3.12 on Linux and macOS)
- [ ] T069 Run the pty tests of tests/test_project.py five times in a row (`python3 -m unittest discover -s tests -k test_pty_`) and confirm no run fails or times out (D14 flakiness risk)
- [ ] T070 Run `openspec validate --all --strict` over openspec/ and confirm it passes
- [ ] T071 ASCII check of every new string: every added line of `git diff "$BASE"..HEAD -- project tests/test_project.py README.md AGENTS.md specs/002-triad-first-project-new` is ASCII (checked by script over the `+` lines), so no em dash or other non-ASCII character is added
- [ ] T072 Diff scope check: `git diff --name-only "$BASE"..HEAD` lists only project, tests/test_project.py, README.md, AGENTS.md and files under specs/002-triad-first-project-new/
- [ ] T073 Walk specs/002-triad-first-project-new/quickstart.md by hand at a real terminal and record any divergence as a defect against these tasks before the realization is handed to the lane lead

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies
- **Foundational (Phase 2)**: after Setup; blocks every story
- **US1 (Phase 3)**: after Phase 2
- **US2 (Phase 4)**: after US1 (the Triad answer is routed by T024)
- **US3 (Phase 5)**: after US2 (its refusal comes before the T034 prompts)
- **US4 (Phase 6)**: after US1 (T051 creates through the question); independent of US2 and US3 except that T049 uses the fake
- **US5 (Phase 7)**: after US4 (T055 and T056 assert the advisory)
- **Polish (Phase 8)**: T062 to T064 may start any time after Phase 2; T065 to T073 after every story

### Within Each User Story

- Tests first, failing, then the implementation tasks, which end by running the phase's tests and the 43 existing tests
- All test tasks edit tests/test_project.py and all implementation tasks edit project, so tasks within a story run in order

### Parallel Opportunities

- T002 (traceability.md) alongside T001
- T010 (project) alongside T003 to T008 (tests/test_project.py)
- T062 (README.md) and T064 (AGENTS.md) alongside any story phase

---

## Parallel Example: Phase 2 and documentation

```bash
# One writer on tests/test_project.py, one on project:
Task: "T003 to T008: fixtures, environment helper, fakes, pty helper, in-process helper, terminal-rule test"
Task: "T010 Add ASSEMBLY_NAME and WORKSPACE_NAME to project"

# Documentation alongside any story phase:
Task: "T062 Update Create a project in README.md"
Task: "T064 Add the agent section to AGENTS.md"
```

---

## Implementation Strategy

### MVP First (User Stories 1 and 2)

1. Complete Phase 1 and Phase 2
2. Complete US1 and US2 (both P1): the question, both answers, both confirmations
3. **STOP and VALIDATE**: run the suite and the quickstart sections for US1 and US2

### Incremental Delivery

1. US3: obstacles named and refused
2. US4: scripted runs and the guarded advisory
3. US5: workspace names and the `--workflow` order
4. Polish: documentation, traceability, verification

The realization ships as one pull request. Opening it, landing it, the
workBenches handoff issue and the comments on issue #3 belong to the lane lead
(OpenSpec `tasks.md` section 3) and are not tasks here.

---

## Requirement Coverage

Every delta scenario is named by at least one test task above. By requirement:

| Requirement | Tasks |
| --- | --- |
| FR-001 | T001, T022, T049, T068 |
| FR-002, FR-003 | T015, T032, T034 |
| FR-004 | T021, T033, T049 |
| FR-005 | T043 |
| FR-006 | T008, T009, T011, T042, T044, T045, T054 |
| FR-007 | T012, T020, T021, T057, T072 |
| FR-008 | T012, T022, T059, T060, T061 |
| FR-009 | T013, T023 |
| FR-010, FR-011 | T014, T016 to T019, T024, T025 |
| FR-012, FR-013 | T035 to T041 |
| FR-014, FR-015 | T026 to T030, T034 |
| FR-016 | T031 to T033 |
| FR-017, FR-018 | T046 to T048, T052, T053 |
| FR-019, FR-020 | T013, T049 to T051 |
| FR-021 | T054, T058 |
| FR-022 | T055 to T058 |
| FR-023 | T003, T067, T071 |
| FR-024 | T062 to T065 |

EC-012 (Ctrl-C while openRepoShape runs) and EC-013 (an agent at a
pseudo-terminal) are documented, not changed: T062 and T064.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps a task to its user story for traceability; `traceability.md` maps each delta scenario to its tests
- Verify tests fail before implementing
- Commit after each phase at least, with the lane line first in each commit body
- No task edits workBenches, openRepoShape, setup-openspeckit, `.github/workflows/`, CLAUDE.md, or the OpenSpec change's files
