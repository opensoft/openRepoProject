Lane: openRepoProject-1

# Implementation Plan: Triad-first project creation

**Branch**: `002-triad-first-project-new` | **Date**: 2026-10-07 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-triad-first-project-new/spec.md`

**Technical design**: `openspec/changes/prefer-triad-in-project-new/design.md`,
decisions D1 to D14, ratified ("ratify 5", PR #5) and landed on main as
`ca4c615`. This plan sequences that design and cites it by decision number; it
decides nothing the design decides. Where the two differ, the design governs.

## Summary

`project new` asks a person at a terminal who has not chosen by flag one
question, Triad (default) or single repository. A Triad answer asks for the
organization and the visibility and re-enters today's `--shape` branch; a
single-repository answer re-enters today's bench branch; each keeps its own
confirmation. A single repository created without the question is followed by
two `warning:` lines on stderr through a guarded descriptor write. The change
is confined to `new()` and new module-level helpers in `project`, new tests in
`tests/test_project.py`, and text in `README.md` and `AGENTS.md`.

Implementation slices, in dependency order:

1. **Terminal rule and the one decision** (D1, D2, D8). Add
   `person_at_terminal()`. In `new()`, immediately after the
   existing-destination refusal, compute `workspace`, `chosen` and `offer` once.
   If `offer` and `--workflow` and `setup-openspeckit` is not on PATH, raise
   today's refusal there; today's later `--workflow` check stays where it is. (tasks.md lands this refusal in T061, after the question exists; its place in `new()` is the same.)
2. **Known obstacles and the pinned name forms** (D3, D10). Add the module
   constants `ASSEMBLY_NAME` and `WORKSPACE_NAME`, each with its openRepoShape
   path and sha comment, applied with `fullmatch`; add a helper that returns
   the obstacle sentences in the order name, openRepoShape, parent. It runs
   only when `offer` is true, with no network and no subprocess.
3. **The question** (D4, D12, D13). Add one ask-twice helper over `ask()`
   (prompt, accepted answers, retry line, second-miss refusal, end-of-input
   refusal) that turns `EOFError` into `Refused` and never catches
   `KeyboardInterrupt`; print the question's lines with `print()`. In `new()`,
   when `offer`: print, ask, route. A Triad answer with any obstacle raises
   the D13 obstacle refusal.
4. **Organization, visibility and the restating line** (D5, D13). In `new()`,
   after a Triad answer with no obstacle: both prompts through the slice-3
   helper, then set `args.shape`, `args.org` and `args.visibility` and print
   the restating line. The unchanged `args.shape` branch re-runs today's shape
   checks and builds today's argv.
5. **The single-repository answer** (D6). It sets nothing; the unchanged bench
   branch follows. No code beyond the routing of slice 3.
6. **The creation advisory and its guarded write** (D7, D13). Add the writer
   (flush stdout; nothing when `sys.stderr` is `None`; ASCII bytes through
   `os.write` on stderr's descriptor with a short-write loop, and
   `sys.stderr.write()` only where there is no descriptor; swallow `OSError`,
   `ValueError` and `AttributeError`). Call it in `new()` after the
   `.project.json` block and before the follow-up loop, only when the bench
   branch ran (`row`) and `not offer and not workspace`.
7. **README and AGENTS.md** (FR-024, D9, D11). README "Create a project" and
   its Configuration table (`CI` row); an AGENTS.md section for agents.
8. **Tests** (D14). The D13 strings as fixtures, the pty helper beside
   `run_cli`, the environment rules, the fake `openRepoShape` and
   `setup-openspeckit`, in-process tests, the guarded-stderr tests, and at
   least one test for each of the 47 delta scenarios, listed in
   `traceability.md`.
9. **Verification**. The full suite (43 existing tests unchanged), `openspec
   validate --all --strict`, an ASCII check of every new string, a fixture
   check against D13, and a diff-scope check.

Code touched, and what stays (design, Non-Goals): only `new()` changes, plus
the new module-level helpers and constants. `ask()`, `confirm()`, `choose()`,
`execute()`, `show_plan()`, the openRepoShape argv, `parser()`, `main()` and
its handlers, and every subcommand other than `new` are unchanged.

## Technical Context

**Language/Version**: Python 3.10 and 3.12 (the CI matrix); local runs use 3.12.3.

**Primary Dependencies**: Python standard library only for the new code; no
new dependency. The existing PyYAML requirement (YAML inspection only) is not
on the creation path and is untouched. Tests use `unittest`, `unittest.mock`,
`subprocess`, `os` (`openpty`, `pipe`), `select` and `signal`; no `pty.fork`
(D14).

**Storage**: N/A. The creation path writes only what the generator and
`.project.json` write today; the advisory is recorded nowhere (D7).

**Testing**: `python3 -m unittest discover -s tests` (CI adds `-v`), over
temporary fixtures with fake generators and fake owner tools.

**Target Platform**: Linux and macOS, at a terminal; CI runs `ubuntu-latest`
and `macos-latest`.

**Project Type**: CLI, one executable file (`project`).

**Performance Goals**: N/A.

**Constraints**: no network on the creation path (D3); ASCII-only new text
(FR-023); no new flag, configuration file or environment variable other than
reading `CI` (D1); the 43 existing tests pass unchanged and the four CI jobs
stay green (SC-010).

**Scale/Scope**: one command, `project new`.

No NEEDS CLARIFICATION remains: `design.md` decides every technical question
(see [research.md](research.md)).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

`.specify/memory/constitution.md` is the unfilled template, so there are no
constitution gates. What governs instead: the ratified change
(`openspec/changes/prefer-triad-in-project-new/`: the spec delta, `design.md`
D1 to D14, `clarifications.md` N1 to N6) and the lane's rules (ASCII-only text,
the lane line on every file, plain pushes only, no work outside this
worktree). Pre-research: pass, nothing to evaluate. Post-design: pass; the
Phase 1 artifacts cite the design and contradict none of it.

## Project Structure

### Documentation (this feature)

```text
specs/002-triad-first-project-new/
  spec.md                  feature specification (/speckit-specify)
  checklists/requirements.md
  plan.md                  this file (/speckit-plan)
  research.md              Phase 0 (/speckit-plan)
  data-model.md            Phase 1 (/speckit-plan)
  contracts/project-new.md Phase 1 (/speckit-plan)
  quickstart.md            Phase 1 (/speckit-plan)
  tasks.md                 Phase 2 (/speckit-tasks)
  traceability.md          delta scenario to test name (built during implementation)
```

### Source Code (repository root)

```text
project                    the single executable: new() and new helpers change
tests/test_project.py      fixtures, fakes, pty helper and new tests
README.md                  "Create a project" and Configuration (FR-024)
AGENTS.md                  agent instruction section (FR-024, D11)
openspec/changes/prefer-triad-in-project-new/
                           the ratified change; read, not changed by implementation
.github/workflows/tests.yml
                           CI matrix; unchanged
```

**Structure Decision**: The repository is one executable with one test module;
the feature adds no file outside `specs/002-triad-first-project-new/` and edits
only `project`, `tests/test_project.py`, `README.md` and `AGENTS.md`.
`CLAUDE.md` and the other agent files at the root are not edited.

## Complexity Tracking

None. There is no constitution gate, so there is nothing to justify.
