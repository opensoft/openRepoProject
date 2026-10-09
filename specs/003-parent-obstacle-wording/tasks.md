Lane: openRepoProject-1

# Tasks: Parent obstacle wording

**Input**: Design documents from `specs/003-parent-obstacle-wording/`

**Prerequisites**: plan.md, spec.md, research.md, quickstart.md; the technical
design is `openspec/changes/fix-parent-obstacle-wording/design.md` (D1 to D6),
which governs wherever a task is shorter.

**Tests**: Required. FR-012 and `design.md` D3 require automated tests over
temporary fixtures for the cases D3 lists, with the new sentence pinned as
fixed text, and at least one test for each of the eight scenarios of the spec
delta (`openspec/changes/fix-parent-obstacle-wording/specs/project-command/spec.md`).
Tests come first and are seen to fail; then the implementation.

**Organization**: Phases follow the order the lane lead set: baseline, tests
first, implementation, verification. All three user stories are realized by
the same branch in `known_obstacles()` and cannot ship apart, so each task
names the stories it serves instead of having a phase per story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: The user story a task serves, where it serves exactly one (US1 to US3); otherwise the stories are named in the description
- Include exact file paths in descriptions

## Path Conventions

One executable, `project`, at the repository root; one test module,
`tests/test_project.py`; documentation in `README.md`; feature files under
`specs/003-parent-obstacle-wording/`. No other file changes. Line references
are at `26a5668`; re-read them if main has been merged in since.

## Rules for every new row and test (D3)

- Expected text comes from the fixtures only: `OBSTACLE_PARENT` (unchanged) and
  the new `OBSTACLE_PARENT_NOT_A_DIRECTORY`; no test reads history.
- No existing row, case or assertion is edited. The one existing line that may
  change is `tests/test_project.py:397`, the "all three" row that closes the
  dict `known_obstacle_cases()` returns, so that new rows can follow it; its
  tuple stays byte for byte. Everything else is added lines.
- Fixtures are created under `self.base`, which is already resolved (`:114`),
  with names distinct from every path an existing row expects to be absent, so
  expected paths hold on macOS too (N2).
- A pty test's name starts with `test_pty_` (feature 002's rule); environments
  come from the existing helpers (`shape_env`, `question_env`, `obstacle_env`),
  with `CI` removed.
- Every added line is ASCII (FR-011).
- Run the suite in py-bench from the worktree root:
  `docker exec py-bench bash -lc "cd '$PWD' && python3 -m unittest discover -s tests"`.

---

The implementer never ticks these boxes; the lane lead ticks each one after verifying it.

## Phase 1: Setup (verification baseline)

**Purpose**: The baseline and the traceability record

- [ ] T001 Confirm the baseline in this worktree: the suite in py-bench reports `Ran 94 tests` and `OK`, and `git diff --quiet 26a5668 -- project tests/test_project.py README.md` exits 0 (project, tests/test_project.py and README.md are main's)
- [ ] T002 [P] Create specs/003-parent-obstacle-wording/traceability.md (lane line first): one row per scenario of the spec delta, by requirement and scenario title in file order (eight rows, among them "The parent directory is missing" and "The parent exists but is not a directory"), with a Tests column each test task fills as its test lands (D4, FR-012)

---

## Phase 2: Tests first (D3)

**Purpose**: Pin the new sentence and every D3 case before `project` changes

- [ ] T003 Add the fixture `OBSTACLE_PARENT_NOT_A_DIRECTORY` to tests/test_project.py, after the `# End D13 fixtures.` marker (`:56`) under its own comment header naming `openspec/changes/fix-parent-obstacle-wording/design.md` D2: the new line of D2 (`design.md:111`) character for character, with `{PARENT}` as its only format field; the D13 block (`:28-56`) and `OBSTACLE_PARENT` (`:35`) are not touched (D3 the fixture; US1, US2; FR-004, FR-012)
- [ ] T004 Extend `known_obstacle_cases()` and the two tests that read it, in tests/test_project.py (D3 rows and "Nothing created"; US1, US2, US3; FR-002 to FR-007): (a) in `known_obstacle_cases()` (`:388-397`), create under `self.base` a regular file with known content, a symbolic link to it and a dangling symbolic link, and add four rows after "all three", each by `--into`: the file and the link to the file, each like the existing "parent" row (`MyApp`, the fake on PATH) with `[OBSTACLE_PARENT_NOT_A_DIRECTORY]` and PARENT `self.base / "<file>"`, the resolved path, for both; the dangling link, likewise with `[OBSTACLE_PARENT]` and PARENT its resolved target; and `my-app` with no `openRepoShape` and the file, with the name, openRepoShape and new lines in that order, the parent last; (b) in `test_pty_triad_answer_with_an_obstacle_refuses` (`:1367-1379`) and `test_inproc_triad_obstacle_runs_nothing` (`:1381-1399`), for each row whose parent exists and is not a directory, add a snapshot `sorted(self.base.rglob("*"))` taken after the environment is prepared and just before the run, assert it is the same after the run, and assert the file is still a regular file (not a link) with its content; how such a row is recognised is the realization's choice, provided no existing tuple changes. Every new row then runs the existing assertions: the question line, the composed refusal, exit 2, no organization prompt, no openRepoShape record, and in process no `execute`, subprocess or socket. Scenarios: The parent exists but is not a directory; The parent directory is missing (dangling link); A Triad answer with a known obstacle
- [ ] T005 [US1] Add a second table to `test_pty_missing_parent_is_named_without_into` in tests/test_project.py (`:1347-1365`), after the first table's loop, for the regular file as the parent given by `--into`, by the positional parent, by `PROJECTS_DIR`, and as the default `~/projects` (a regular file at `HOME/projects`, the `HOME` directory created for it, `PROJECTS_DIR` removed); create its fixtures only after the first table's loop, whose default case needs `HOME/projects` absent. Each run ends input at the question as the first table does, and asserts the question with the new line naming the resolved file (`assert_question`), no question line containing `--into`, and the file still a regular file with its content. The regular file only (N6). Scenario: The parent exists but is not a directory (D3 routes; FR-002, FR-004, FR-005; SC-001)
- [ ] T006 [US2] Add rows to `test_pty_dry_run_with_an_obstacle_refuses` in tests/test_project.py (`:1401-1415`) for the file and the link to the file (each `[OBSTACLE_PARENT_NOT_A_DIRECTORY]` naming the file) and the dangling link (`[OBSTACLE_PARENT]` naming its resolved target), each by `--into`, with the same three fixtures created under `self.base` before its loop; add the rows in new lines after the `cases` literal so `:1404-1405` stay as they are. Its existing assertions, the `rglob` snapshot included, apply as they stand. Scenario: A dry run with a known obstacle (D3 dry run; FR-007; SC-004)
- [ ] T007 [US3] Add a new pty test to tests/test_project.py (for example `test_pty_single_answer_with_a_file_parent_ends_as_by_flag`): with a regular file under `self.base` as `--into`, the fake on PATH and `CI` removed (`shape_env(ci=None)`) and an assembly-form name such as `MyApp`, answer `2` then `yes`; then run the baseline, the same name and `--into` with `--type test` (not asked), answering `yes`. Assert both exit statuses are equal (today 2), the pty transcripts from `Create:` on are equal, the `REFUSED:` texts on stderr are equal (today `[Errno 17] File exists`), and no `warning:` line appears in the asked run; the comparison leaves the advisory out. `test_pty_single_answer_is_unaffected_by_obstacles` keeps its row. Scenario: A single-repository answer is unaffected (D3; FR-008; SC-005)
- [ ] T008 [US3] Add a new pty test to tests/test_project.py (for example `test_pty_symlink_to_a_directory_names_no_obstacle`): a symbolic link under `self.base` to a directory under `self.base` as `--into`, the name `MyApp`, the fake on PATH (`shape_env(ci=None)`); Enter at the question and end of input at the organization prompt, as `test_pty_no_known_obstacle_names_none` (`:1439-1446`) does. Assert exit 2, `assert_question(result.stdout, "MyApp")` with no obstacle line, no `Not possible here: ` on either stream, the organization end-of-input refusal, and no openRepoShape record. Scenario: No known obstacle (D3; FR-009; SC-003)

**Checkpoint**: With `project` unchanged, run the suite: the only failures are in the cases that expect the new line (the file, link-to-file and `my-app`-with-file rows of the two T004 tests, the four routes of T005, and the file and link rows of T006). Every existing case, the dangling-link rows, T007 and T008 pass, since they pin behaviour that does not change. Fill the Tests column of traceability.md for T003 to T008.

---

## Phase 3: Implementation (D1, D2)

**Purpose**: The second parent read, the new sentence, and the README sentence

- [ ] T009 In `known_obstacles()` in project (`:235-247`): keep the third read `parent.is_dir()`; inside its false branch, read `parent.exists()` on the same `parent`: false appends today's missing sentence, unchanged byte for byte; true appends the new sentence of D2 with the parent substituted as today. Add no other read, no exception handling and no import; keep the order name, openRepoShape, parent; leave `new()` untouched (one call at `:332` still feeds the question at `:333` and the refusal at `:338-339`). In the docstring, say "three local facts" in place of "three local reads" and name this change's design (`fix-parent-obstacle-wording`) for the second parent sentence. T003 to T008 and every existing test pass (D1, D2; US1, US2, US3; FR-001 to FR-007, FR-009, FR-011)
- [ ] T010 [P] [US1] In README.md line 60, replace the clause "or a parent directory that does not exist." with the README text of D2 (`design.md:135`) character for character; leave the rest of the paragraph (`:57-62`) unchanged apart from rewrapping it to the README's line width (D2; FR-010; SC-007)

**Checkpoint**: The suite passes; every story works end to end

---

## Phase 4: Verification

**Purpose**: Evidence for the lane lead; keep each task's command output for the PR. Throughout, `BASE=$(git merge-base origin/main HEAD)`.

- [ ] T011 Run the full suite in py-bench: `Ran 96 tests`, `OK` (the 94 existing tests plus T007 and T008); where a Python 3.10 interpreter is available, run it under 3.10 as well (CI runs 3.10 and 3.12 on Linux and macOS) (SC-006)
- [ ] T012 Show that the new tests fail against unchanged code: with only the project and README.md hunks stashed (`git stash push -- project README.md` while they are uncommitted; once committed, `git checkout "$BASE" -- project README.md`, restored afterwards with `git checkout HEAD -- project README.md`), run the suite and confirm the failures are exactly those named at the Phase 2 checkpoint; then restore (`git stash pop`) and confirm the suite passes again (FR-012)
- [ ] T013 ASCII check of added lines: every `+` line of `git diff "$BASE" -- project tests/test_project.py README.md specs/003-parent-obstacle-wording` is ASCII (`LC_ALL=C grep -nP '[^\x00-\x7F]'` over them prints nothing); the whole of project is not checked, as it already carries em dashes at 197, 908, 921 and 1129 (N4; FR-011)
- [ ] T014 Check the fixed text by script: `OBSTACLE_PARENT_NOT_A_DIRECTORY.format(PARENT="PARENT")` equals `design.md:111` and `OBSTACLE_PARENT.format(PARENT="PARENT")` equals `design.md:110`, character for character; and README.md, with lines joined by single spaces, contains the text of `design.md:135` exactly once and no longer contains "or a parent directory that does not exist", while the rest of the paragraph's words are unchanged (D2; FR-004, FR-010, FR-012)
- [ ] T015 Diff check (D3, design Non-Goals; FR-012, SC-006): (a) `git diff "$BASE" -- tests/test_project.py` has exactly one `-` line, the old "all three" row at `:397`, and an added line with the same tuple followed by a comma, so no existing assertion or row tuple is edited; (b) `git diff --name-only "$BASE"..HEAD` lists only project, tests/test_project.py, README.md, files under specs/003-parent-obstacle-wording/, and openspec/changes/fix-parent-obstacle-wording/tasks.md (changed by the specify commit `90a4cee`); (c) a script confirms by `ast` that project's imports and every top-level function other than `known_obstacles` have identical source at `$BASE` and HEAD
- [ ] T016 Validate OpenSpec with a current CLI, `/usr/bin/openspec` (1.6.0) or the openspec in py-bench (1.13.1), never the host's npm-global 1.2.0 (plan.md, Risks and Notes): `openspec validate fix-parent-obstacle-wording --strict` passes, and `openspec validate --all --strict` reports 6 of 6 passing
- [ ] T017 Complete specs/003-parent-obstacle-wording/traceability.md: eight rows, no empty Tests cell, and every named test defined in tests/test_project.py (checked by script, each name found as `def NAME`) (D4; FR-012)
- [ ] T018 Walk specs/003-parent-obstacle-wording/quickstart.md by hand at a real terminal, the FIFO, `FILE/` and `FILE/sub` runs included, and record any divergence as a defect against these tasks before the realization is handed to the lane lead (SC-001, EC-001, EC-002)

---

## Lane steps (the lane lead's, not implementer tasks)

These are not checkbox tasks and are never done by the implementer. They follow
OpenSpec `tasks.md` section 3 and `design.md` D5.

1. Open the realization as a draft pull request from `003-parent-obstacle-wording`
   to main; its body carries `Closes #14` and the line `Lane: openRepoProject-1`.
2. Independent re-verification: a separate verifier re-runs Phase 4 on the PR
   head, and the lane lead ticks the boxes above from that evidence.
3. Mark the pull request ready once it is re-verified and the four CI jobs
   (`ubuntu-latest` and `macos-latest`, Python 3.10 and 3.12) are green.
4. Land only on Brett Heap's word "ratify <n>" for that pull request, quoted
   with its link. If PR #11 (lane openRepoProject-2) lands first, merge main
   in; no rebase, no force push.
5. After landing: cite the merge sha in OpenSpec `tasks.md` 3.1 (`gh pr view
   <n> --json mergeCommit,statusCheckRollup`). If workBenches#145 is still
   open, post one comment there naming the merge sha and the sha256 of
   `project` at it (`git show <sha>:project | sha256sum`) as an alternative pin
   target (D5, 3.2); if it is closed, post nothing. Open no new issue anywhere.
6. The archive pull request: `/opsx:archive` for fix-parent-obstacle-wording
   (3.3), its `openspec validate --all --strict` run with `/usr/bin/openspec`
   or the openspec in py-bench.
7. The worktree sweep: retire `../openRepoProject-worktrees/003-parent-obstacle-wording`
   and its branch once the realization and the archive have landed.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies; T002 alongside T001
- **Tests first (Phase 2)**: after T001; T003 first, since T004 to T006 use the fixture; T004 to T008 in order (one file)
- **Implementation (Phase 3)**: T009 after Phase 2 and its checkpoint; T010 may run any time after T001 (no test reads README.md)
- **Verification (Phase 4)**: after Phase 3; T012 before the project and README.md hunks are committed, or with the checkout form; T017 after T011; T018 last

### Within Each Phase

- Every test task edits tests/test_project.py, so test tasks run one at a time
- Tests are seen to fail at the Phase 2 checkpoint before T009 is written

### Parallel Opportunities

- T002 (traceability.md) alongside T001
- T010 (README.md) alongside Phase 2 or T009 (project)

---

## Parallel Example

```bash
# One writer on tests/test_project.py and project, one on README.md:
Task: "T003 to T009: the fixture, the rows, the two pty tests, then known_obstacles()"
Task: "T010 Replace the README.md clause with the D2 text"
```

---

## Implementation Strategy

The realization ships as one pull request with no MVP split: the three stories
come from one branch in `known_obstacles()`. Stop and validate twice: at the
Phase 2 checkpoint (only the new-line cases fail) and at T011 (all 96 pass).
Commit after each phase at least, with the lane line first in each commit body.

---

## Requirement Coverage

| Requirement | Tasks |
| --- | --- |
| FR-001 | T004 (in process: no subprocess or socket), T009, T015 |
| FR-002 | T004, T005, T009 |
| FR-003 | T004 and T006 (dangling-link rows), T009, T011 (the existing missing-parent cases) |
| FR-004 | T003, T004, T005, T009, T014 |
| FR-005 | T004, T005 |
| FR-006 | T004 (the `my-app` row, the parent last), T009 |
| FR-007 | T004, T006, T009 |
| FR-008 | T007 |
| FR-009 | T008 |
| FR-010 | T010, T014 |
| FR-011 | T013 |
| FR-012 | T002, T003 to T008, T012, T015, T017 |

Success criteria: SC-001 T005, T018; SC-002 T011, with the dangling-link rows
of T004 and T006; SC-003 T008; SC-004 T004, T006; SC-005 T007; SC-006 T011,
T015, and the four CI jobs (lane step 3); SC-007 T010, T014; SC-008 lane step
5 (D5), nothing in workBenches.

Edge cases: EC-001 (a FIFO, `FILE/`) follows from D1's read and is shown by
hand in T018; D3 adds no automated case for it. EC-002 to EC-004 are
unchanged behaviour (D6): `FILE/sub` is walked in T018, and the later-version
residuals are not tested here (N1).

---

## Notes

- [P] tasks = different files, no dependencies
- `traceability.md` maps each delta scenario to its tests (D4, FR-012)
- No task edits workBenches, openRepoShape, setup-openspeckit, `.github/workflows/`, CLAUDE.md, feature 002's record (`specs/002-triad-first-project-new/`), or the OpenSpec change's files
