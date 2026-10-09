Lane: openRepoProject-1

# Implementation Plan: Parent obstacle wording

**Branch**: `003-parent-obstacle-wording` | **Date**: 2026-10-09 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/003-parent-obstacle-wording/spec.md`

**Technical design**: `openspec/changes/fix-parent-obstacle-wording/design.md`,
decisions D1 to D6, ratified by Brett Heap ("ratify 15", 2026-10-09, PR #15)
and landed on main as `26a5668`; governing issue opensoft/openRepoProject#14.
This plan restates that design as the plan, by decision number, and decides
nothing the design does not decide. Where the two differ, the design governs.

## Summary

`project new` names a parent that exists but is not a directory as missing:
the obstacle is read as `parent.is_dir()` but worded "does not exist". The
obstacle keeps its condition. Only when it holds, `parent.exists()` on the same
resolved parent chooses between today's missing sentence, unchanged, and one
new sentence. The question line and the composed refusal still come from one
list, computed once. The change is confined to `known_obstacles()` in `project`
(one branch and its docstring), one sentence of `README.md`, and one fixture,
new rows and two new tests in `tests/test_project.py`.

Implementation slices, in dependency order (`tasks.md` holds the tasks):

1. **Baseline** (D3). The suite passes 94 tests unchanged at the base.
2. **Tests first** (D3). The fixture, the rows and the two new tests; against
   the unchanged `project` only the cases that expect the new sentence fail.
3. **The read and the sentence** (D1, D2) in `known_obstacles()`.
4. **The README sentence** (D2).
5. **Verification** (D2, D3, N4). The full suite, the failing-first check, the
   ASCII check of added lines, the fixture and README text checks, the diff
   check, and `openspec validate`.

Lane steps after verification (D5, OpenSpec `tasks.md` section 3) belong to
the lane lead and are listed, unticked, at the end of `tasks.md`.

## Technical Context

**Language/Version**: Python 3.10+ (the README's requirement); CI runs 3.10 and
3.12 on `ubuntu-latest` and `macos-latest` (`.github/workflows/tests.yml`),
unchanged (D6). Local runs use Python 3.12.3 in the `py-bench` container.

**Primary Dependencies**: Python standard library only; `pathlib` is already
used, and no import is added (design Non-Goals). Tests use `unittest`,
`unittest.mock` and the existing pty and in-process helpers; no new
dependency (D3).

**Storage**: N/A.

**Testing**: `python3 -m unittest discover -s tests` (CI adds `-v`). Locally,
from the worktree root: `docker exec py-bench bash -lc "cd '$PWD' && python3 -m
unittest discover -s tests"` (py-bench mounts the projects tree at the same
path).

**Target Platform**: Linux and macOS, at a terminal.

**Project Type**: CLI, one executable file (`project`).

**Performance Goals**: N/A (one more local read, only when the obstacle holds).

**Constraints**: three local facts in the order name, openRepoShape, parent,
with no network, no subprocess and no new import, flag, environment variable
or configuration (FR-001); the missing sentence byte for byte as today
(FR-003); ASCII in every changed string and added line (FR-011, N4); the 94
existing tests pass with no existing assertion or case edited, and the four CI
jobs stay green (SC-006).

**Scale/Scope**: one function of `project new`, one README sentence, one test
module.

No NEEDS CLARIFICATION remains: `design.md` decides every technical question
and records no open one (see [research.md](research.md)).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

`.specify/memory/constitution.md` is the unfilled template: no constitution
gates are defined. What governs instead: the ratified change
(`openspec/changes/fix-parent-obstacle-wording/`: the spec delta, `design.md`
D1 to D6, `clarifications.md` N1 to N6) and the lane's rules (ASCII-only text,
the lane line on every file, plain pushes only, no work outside this
worktree). Pre-research: pass, nothing to evaluate. Post-design: pass; the
Phase 1 artifacts cite the design and contradict none of it.

## Design

The ratified decisions, restated as the plan. Line references are to `project`
and `tests/test_project.py` at `26a5668`, unchanged on this branch.

### D1. The read: `is_dir()`, then `exists()` on the same path

- The third read stays `parent.is_dir()` (`project:244`) on the parent `new()`
  resolves once (`project:315`), however it was given: `--into`, the
  positional parent, `PROJECTS_DIR` or `~/projects`. A symbolic link is read
  as its target.
- Only when that read is false, `parent.exists()` on the same `parent` chooses
  the sentence: false gives the missing sentence, true gives the new one (D2).
  Archived D3 item 3 is restated that way (`design.md:59-63`).
- The facts stay three, in the order name, openRepoShape, parent. The
  docstring says "three local facts" in place of "three local reads" and names
  this design for the second parent sentence.
- `known_obstacles()` is still called once (`project:332`); that one list feeds
  the question (`project:333`) and the composed refusal (`project:338-339`), so
  the two cannot diverge and the refusal never reads the parent again. A parent
  repaired in another terminal while the question waits is refused with the
  sentence the question printed until a rerun, as today.
- No exception handling is added: `exists()` has the same error handling as
  `is_dir()` on every version (N3), and a parent the two reads could not stat
  on 3.10 and 3.12 is refused earlier, at `destination.exists()`
  (`project:321`).

On the CI versions (`design.md:78-86`; re-probed on 3.12.3 for this plan):

| Parent given as | Sentence |
| --- | --- |
| a missing path, or a dangling symbolic link | missing sentence, naming the path (a link by its target) |
| a regular file, `FILE/`, a symbolic link to a file, a FIFO | new sentence, naming the file (a link by its target) |
| a symbolic link to a directory | no parent obstacle |
| `FILE/sub` | missing sentence (D6, residual dead end) |
| a symbolic-link loop, or a parent under an unsearchable ancestor | fails before the question, as today (D6, N1) |

### D2. Fixed text

All text is ASCII; `PARENT` is the resolved parent, every other character is
literal. The parent's line under entry 1, with exactly one of the two present
(`design.md:110-111`):

```text
     Not possible here: The parent directory PARENT does not exist; a Triad is created inside an existing directory.
     Not possible here: The parent PARENT exists but is not a directory; choose a parent that is a directory.
```

The composed refusal keeps archived D13's shape: `A Triad cannot be created
here. `, the obstacle sentences in order joined by single spaces, then
` Nothing was created.` For `my-app`, no `openRepoShape` and a file parent,
`main()` prints on stderr (`design.md:127`):

```text
REFUSED: A Triad cannot be created here. my-app cannot be a Triad name; a Triad name is a letter first, then letters and digits only, such as MyApp. openRepoShape is not on PATH. Install openRepoShape through workBenches first. The parent PARENT exists but is not a directory; choose a parent that is a directory. Nothing was created.
```

`README.md` line 60: the clause "or a parent directory that does not exist."
is replaced, character for character, by the text below; the rest of that
paragraph (lines 57-62) is unchanged, rewrapped to the README's line width
(`design.md:135`):

```text
or a parent that is missing or is not a directory. A single-repository answer creates a missing parent; a parent that exists but is not a directory blocks both answers, so choose another parent.
```

The ASCII check covers the changed strings and the added lines of `project`,
`tests/test_project.py` and `README.md`, not the whole of `project`, which
already carries em dashes at lines 197, 908, 921 and 1129 (N4).

### D3. Tests

All in `tests/test_project.py`. `OBSTACLE_PARENT` (`:35`) stays, since the
missing sentence is unchanged.

| Where | What is added | Expected |
| --- | --- | --- |
| After `# End D13 fixtures.` (`:56`) | `OBSTACLE_PARENT_NOT_A_DIRECTORY`, the new line of D2 with `{PARENT}` as its format field, under its own header naming this design (D2); the D13 block stays a verbatim copy of the archived design | n/a |
| `known_obstacle_cases()` (`:388-397`) | creates under `self.base` a regular file with known content, a symbolic link to it and a dangling symbolic link; four rows after the existing four, each by `--into`: the file; the link to the file; the dangling link; `my-app` with no `openRepoShape` and the file | the file and the link: the new line, PARENT `self.base / "<file>"` (the resolved path); the dangling link: `OBSTACLE_PARENT`, PARENT its resolved target; `my-app`: the name, openRepoShape and new lines, the parent last |
| `test_pty_triad_answer_with_an_obstacle_refuses` (`:1367-1379`) and `test_inproc_triad_obstacle_runs_nothing` (`:1381-1399`) | run every new row through `known_obstacle_cases()`; for each row whose parent exists and is not a directory, also a "nothing created" check (N2) | the question line, the composed refusal, exit 2, no organization prompt, no openRepoShape record (in process: no `execute`, subprocess or socket); `sorted(self.base.rglob("*"))` the same after the run as before it, and the file still a regular file with its content |
| `test_pty_missing_parent_is_named_without_into` (`:1347-1365`) | a second table, after its first, for the regular file only (N6): by `--into`, by the positional parent, by `PROJECTS_DIR`, and as the default `~/projects` (a regular file at `HOME/projects`, `PROJECTS_DIR` removed) | the new line naming the resolved file, no question line containing `--into`, the file unchanged |
| `test_pty_dry_run_with_an_obstacle_refuses` (`:1401-1415`) | rows for the file, the link to the file and the dangling link, each by `--into` | its existing assertions, the `rglob` snapshot included, as they stand |
| a new pty test | the single-repository answer: `2` and `yes`, the file as `--into`, `CI` unset; and the baseline, the same name and parent with `--type test` (not asked), answering `yes` | the same exit status (today 2), the same stdout from `Create:` on, the same `REFUSED:` line (today `[Errno 17] File exists`), no `warning:` line in the asked run; the comparison leaves the advisory out |
| a new pty test | a symbolic link to a directory as `--into`, an assembly-form name, the fake on PATH; the Triad taken, input ended at the organization prompt, as `test_pty_no_known_obstacle_names_none` (`:1439-1446`) does | the question names no obstacle |

`test_pty_single_answer_is_unaffected_by_obstacles` keeps its row. No existing
row, case or assertion is edited (spec Assumptions, SC-006). One existing line
may change: the line that closes the dict `known_obstacle_cases()` returns
(`:397`), so that the new rows can follow the "all three" row, whose tuple
stays byte for byte. How a non-directory row is recognised for the snapshot is
the realization's choice, provided no existing row's tuple changes. Expected
paths come from `self.base`, which is already resolved (`:114`), so they hold
on macOS, where a temporary directory resolves under `/private/var` (N2).

### D4. Feature 002's record

Carried by `spec.md` (its Supersession paragraph): feature 002's FR-012 parent
fact is superseded by the two cases, and `specs/002-triad-first-project-new/`
is not edited. This feature's `traceability.md`, built during implementation,
maps every scenario of the delta by title to its tests, among them "The parent
directory is missing", whose title is unchanged so feature 002's
`traceability.md:37` still points at it, and "The parent exists but is not a
directory" (FR-012).

### D5. Handoffs after landing (a lane step, not an implementation task)

No new issue on any repository. When the realization merges, the lane posts
one comment on workBenches#145 if that issue is still open, naming the merge
sha and the sha256 of `project` at that sha (`git show <sha>:project |
sha256sum`) as an alternative pin target; if #145 is closed by then, nothing is
posted.

### D6. What is not changed

- The shape branch's refusal, "Shape creation requires an existing --into
  parent directory." (`project:364-365`), reached only with `--shape` by flag.
- The bench path for a parent that exists and is not a directory: it shows the
  plan, asks for `yes`, and only then refuses (`[Errno 17] File exists`, exit
  2), and its dry run exits 0. Re-observed on 3.12.3 for this plan: the asked
  and the flag-chosen run, and the flag-chosen dry run.
- The residual dead ends: `FILE/sub`, the symbolic-link loop on 3.13 and later,
  and the unsearchable ancestor on 3.14.
- The CI matrix and the README's "Python 3.10+". `ask()`, `confirm()`,
  `choose()`, `execute()`, `print_creation_question()`, `new()`, `main()` and
  every other subcommand.

## Project Structure

### Documentation (this feature)

```text
specs/003-parent-obstacle-wording/
  spec.md                  feature specification (/speckit-specify)
  checklists/requirements.md
  plan.md                  this file (/speckit-plan)
  research.md              Phase 0 (/speckit-plan)
  quickstart.md            Phase 1 (/speckit-plan)
  tasks.md                 Phase 2 (/speckit-tasks)
  traceability.md          delta scenario to test name (built during implementation, D4)
```

No `data-model.md` or `contracts/`: the feature adds no entity, and its one
interface change is a fixed string of an existing question, fixed in
`design.md` D2.

### Source Code (repository root)

```text
project                    known_obstacles() only: the second parent read, the new sentence, the docstring
tests/test_project.py      one fixture, new rows, the snapshot checks, two new pty tests
README.md                  the known-obstacles sentence (line 60)
openspec/changes/fix-parent-obstacle-wording/
                           the ratified change; read, not changed by implementation
.github/workflows/tests.yml
                           CI matrix; unchanged (D6)
```

**Structure Decision**: The repository is one executable with one test module.
The feature edits only `project`, `tests/test_project.py` and `README.md`, and
adds files only under `specs/003-parent-obstacle-wording/`.

## Risks and Notes

- **The host's openspec is outdated.** The `openspec` first on the host's PATH,
  an npm-global install at 1.2.0, checks only the first line of a requirement
  for SHALL or MUST, so `openspec validate --all --strict` misreports
  `spec/project-command` (`openspec/specs/project-command/spec.md:311`) and
  `spec/speckit-extension-integration`
  (`openspec/specs/speckit-extension-integration/spec.md:11`) as failing, on
  main `26a5668` and on this branch alike. `/usr/bin/openspec` 1.6.0 and the
  openspec 1.13.1 inside py-bench report 6 of 6 passing, this change included,
  and `openspec validate fix-parent-obstacle-wording --strict` passes under all
  three. Verification, and the archive check of OpenSpec `tasks.md` 3.3, run
  `/usr/bin/openspec` or the openspec in py-bench, never the bare host
  `openspec`. The main specs need no fix.
- **PR #11's feature (lane openRepoProject-2) edits `project` and
  `tests/test_project.py` too.** Whichever merges second merges main in; no
  rebase, no force push. Line numbers and the test count here are at
  `26a5668` and are re-read if main is merged in first.
- **A single-repository answer with a file parent fails after `yes`.** Known
  limitation (D6); the README's new sentence says such a parent blocks both
  answers.
- **Later Python versions** print the missing sentence for a symbolic-link
  loop (3.13 and later) or an unsearchable ancestor (3.14): residuals on
  versions CI does not run (D1, D6, N1).
- **`FILE/sub`** keeps the missing sentence, which is true, while the repair it
  suggests fails with `Not a directory`: an accepted gap (D6).

## Complexity Tracking

None. There is no constitution gate, so there is nothing to justify.
