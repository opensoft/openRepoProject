Lane: openRepoProject-1

# Implementation Plan: Refuse a non-directory parent early

**Branch**: `006-refuse-non-directory-parent-early` | **Date**: 2026-10-21 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/006-refuse-non-directory-parent-early/spec.md`

**Technical design**: `openspec/changes/refuse-non-directory-parent-early/design.md`,
decisions D1 to D6, with `clarifications.md` N1 to N6 and the `project-command`
spec delta, ratified by Brett Heap ("ratify 21", 2026-10-21, PR #21) and landed
on main by squash as `b233333`; governing issue opensoft/openRepoProject#20.
This plan restates that design as the plan, by decision number, and decides
only what the design leaves to the realization (where code and tests go, how
the tests are split, how the checks run). Where the two differ, the design
governs.

**Clarify answers.** This plan follows Brett Heap's answers of 2026-10-22 to
the five clarify questions (`clarify-questions.md`), "all recommended":
**Q1 B, Q2 A, Q3 A, Q4 B, Q5 A**, recorded in the spec's Clarifications
section. Every sentence, row or section that depends on an answer carries its
tag, `[Q1]` to `[Q5]`, which trace to those Clarifications. The appendix
"Options not taken" says, for each option not chosen, exactly what changes
here. Nothing else in this plan turns on the answers. A tag on a slice, row or
step names the answers it depends on, directly or through the running count of
test methods (`N0` plus the methods added so far, which `[Q2]` changes by 2);
where a tag and the appendix differ, the appendix governs.

Line references are to `project`, `tests/test_project.py`, `README.md` and
`.github/workflows/tests.yml` at `d47e8a4`, where the first three are
byte-identical to the packet's base `961c405` except `README.md:282` (#32,
outside every cited range). Each was checked with `git show d47e8a4:<path>`.
After main is merged in (below), cite by function name and re-read the line.

Sources outside the repository are named for provenance only: the lane's
review reports A, H and K (as the spec names them), agent B's conflict map and
agent T's test inventory (both 2026-10-21). Nothing here needs them to be
built or checked: T's run table is carried in research R5, and every check's
command is in this plan or in `quickstart.md`.

## Summary

The single-repository path of `project new` refuses a parent blocked by a
non-directory as its first step, however that path was chosen: by flag, by an
invocation that is not asked the creation question, or by the answer `2`. Today
it prints the destination and the plan, asks for `yes`, and only then fails at
`parent.mkdir` (`project:398`) with a raw errno; its dry run exits 0. One new
helper, `parent_case(parent)`, reads the parent's case with the existing
pathlib reads (`is_dir()`, `exists()`, then `exists()` up `parent.parents` to
the first that exists, then its `is_dir()`); a second,
`blocked_parent_sentence()`, returns sentence (a) or the new sentence (b).
`known_obstacles()` calls the first helper once for the question and the Triad
refusal, as today; the bench branch calls it afresh after the shape-only flag
check (`project:383-384`) and before `choose()` (`project:385`). Four README
texts change, fixed by D2. The tests add one fixture block, two helpers, two
rows to `known_obstacle_cases()`, one row to the dry-run obstacle test, rewrite
one existing test, and add 15 test methods `[Q2]`.

Implementation slices, in dependency order (the later `tasks.md` holds the
tasks; "Work breakdown" below gives their file sets, writers, tiers and verify
commands):

0. **Governance record** `[Q5]`. Before the first implementation commit, the
   change's `tasks.md` gets its 1.6 and 2.1 ticks and the Speckit Handoff
   fields (G1); its 2.2 tick follows once the first implementation commit
   exists (G2), as feature 003's did.
1. **Baseline and traceability skeleton**. The suite passes at the base with
   its `N0` tests (`N0` is measured at the merge base, below; 96 at `d47e8a4`).
2. **Tests first** (D3). Fixtures, the blocked-parent builder, rows, the
   rewritten test and the new tests; against the unchanged `project` the red
   runs fail and the guard runs pass.
3. **The read and the head refusal** (D1, D2) in `project`; **the README
   texts** (D2), in parallel.
4. **Verification** (D2, D3, N3, N4). Full suite on 3.12 and 3.10, the
   red-first record, the mutation checks, ASCII, fixed text, README greps,
   the diff and `ast` checks, `openspec validate` and G2 (Phase 4); then the
   traceability record (Phase 5).

After Phase 5, the hand walk of the quickstart at a real terminal, the
adversarial review, and the pull request and landing steps (D5; the change's
`tasks.md` section 3; merging main in) are the lane lead's: a plain numbered
list at the end of the later `tasks.md`, not checkbox tasks and not
tier-tagged, as in feature 003 ("Lane steps", under the work breakdown below).
The walk and the review are not dispatchable tasks: the walk needs a real
terminal (User Story 4 needs two), and the lead dispatches the `[O]` review
and records its verdict before the pull request opens.

## Technical Context

**Language/Version**: Python 3.10+ (the README's requirement, `README.md:17-18`).
CI runs the `test` job on `ubuntu-latest` only, Python 3.10 and 3.12
(`.github/workflows/tests.yml:9-10`, since #32); unchanged (D6). Local runs:
Python 3.12.3 in `py-bench`; Python 3.10 from uv, with PyYAML supplied as
`quickstart.md` ("Environment") says.

**Primary Dependencies**: Python standard library only; `pathlib` is already
used and no import is added to `project` (design Non-Goals; FR-011). Tests use
`unittest`, `unittest.mock` and the existing pty and in-process helpers; the
blocked-parent builder imports `socket` locally `[Q3]` and checks special files
with `Path.is_fifo()`, `is_socket()` and `is_char_device()`, so the test
module's import block (`tests/test_project.py:2-19`) is not edited; no new
dependency (D3).

**Storage**: N/A.

**Testing**: `python3 -m unittest discover -s tests` (CI adds `-v`). Locally,
from the worktree root:

```text
bash specs/006-refuse-non-directory-parent-early/qs.sh suite ADDED=0                      # check suite on python3 (3.12.3), before Phase 2
bash specs/006-refuse-non-directory-parent-early/qs.sh suite                              # after I1: ADDED defaults to 15 [Q2]
bash specs/006-refuse-non-directory-parent-early/qs.sh suite PY="$(uv python find 3.10)"  # 3.10: the check links PyYAML in when it lacks it
docker exec py-bench bash -lc "cd '$PWD' && python3 -m unittest discover -s tests"       # the same suite by hand, 3.12.3 in the container
```

At `d47e8a4` the suite reports `Ran 96 tests`, `OK` on 3.12.3 and on 3.10 with
PyYAML, all 37 `test_pty_*` tests included (agent T: 3.12.3 and 3.10.18, on a
bench at load 73 to 87, 144.5 s and 83.4 s; this plan: 3.10.21 in `py-bench`,
45.0 s). Without PyYAML, 3.10 fails 11 YAML tests at the base;
with a D1 prototype it fails those 11 and the one test this feature rewrites,
nothing else (research R11). Run pty tests in the foreground: in a background
job SIGINT is ignored and three interrupt tests fail. No suite count is fixed
in this plan: main gains PR #33's tests before this feature lands, so every
expected count is `N0`, the number of tests at `BASE=$(git merge-base origin/main
HEAD)`, measured on an export of it, plus the tests added so far (15 after
Phase 2 `[Q2]`); `quickstart.md` ("Run the tests", check `suite`) holds the
commands.

**Target Platform**: Linux at a terminal (CI); the tests stay
system-neutral (resolved paths from `self.base`, errnos from `errno` and
`os.strerror()`), as on macOS.

**Project Type**: CLI, one executable file (`project`), one test module.

**Performance Goals**: N/A for the command (at most a few `stat` calls more,
on the bench path). Test time: 101 new runs `[Q1]` `[Q3]` `[Q4]` (research R5,
R7), about 9 s on a quiet machine and about 50 s on a heavily loaded bench.

**Constraints**: the reads are local, open nothing, read no permission, add no
network access, subprocess, import, flag, environment variable or
configuration (FR-002, FR-010, FR-011); sentence (a), the missing sentence and
the Triad refusal's shape byte for byte as today (FR-006, FR-007); the head
refusal one text by flag or answer, with or without `--dry-run` (FR-005);
ASCII in every changed string and added line (FR-013); one existing test is
rewritten, and two existing members (`known_obstacle_cases()` and
`test_pty_dry_run_with_an_obstacle_refuses`) gain added lines only, no existing
line of theirs removed or changed (N3, AC5, the spec's "unchanged") `[Q2]`;
both CI jobs green (SC-006).

**Scale/Scope**: two new functions and two edited ones in `project`
(`known_obstacles()`, `new()`); four README texts; one test module.

No NEEDS CLARIFICATION remains in the design: `design.md` decides every
technical question and records no open one (`design.md:364-369`). The five
clarify questions are about test breadth and the governance record, and Brett
Heap answered them on 2026-10-22 (see the banner above and research R12).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

`.specify/memory/constitution.md` is the unfilled template: no constitution
gates are defined. What governs instead: the ratified change
(`openspec/changes/refuse-non-directory-parent-early/`: the spec delta,
`design.md` D1 to D6, `clarifications.md` N1 to N6) and the lane's rules:
ASCII-only text, the lane line first in every Markdown file (`qs.sh`, a
script, has none), merges only (no rebase, no force push; the org ruleset
refuses force pushes), plain pushes, no work outside this feature's
worktree, no edit of features 002 and 003 or of the change's files beyond
`[Q5]`. Pre-research: pass, nothing to evaluate.
Post-design: pass, re-checked with `research.md` and `quickstart.md` in their
final form: they restate the design and contradict none of it; every research
number this plan cites (R1, R2, R5 to R12, R14, R15) resolves there with the
meaning cited; every quickstart section a verify cell names exists and holds
its commands in full; and no file needs a source outside the repository. The
three files and the runner `qs.sh` are committed together.

## Design

The ratified decisions, restated as the plan.

### D1. The read: `parent_case(parent)`, once for the question, afresh at the head

**Where the helpers go in the file.** Insert `parent_case()` and then
`blocked_parent_sentence()` after `project:234` (the second blank line after
`VISIBILITIES`, `:232`), each followed by two blank lines, so that they sit
just before `known_obstacles()` (`:235`): just before the reader of known
obstacles, the placement the spec's Assumptions carry (report H). This is
inside agent B's conflict-free zone, main's `:160-:432` above `discover()`
(`:433`). Never after `discover()`: helpers placed right after it conflict with
PR #33 (feature 004, lane 2), which rewrites `discover()` and the block below
it (research R2, R9). No new module-level statement other than the two
functions (no constant, no import).

**The helpers** (reference shape; a scratch prototype of exactly this passed
every existing test but the one this feature rewrites, on 3.12.3 and 3.10.21,
research R1):

```python
def parent_case(parent):
    """..."""   # ASCII; names refuse-non-directory-parent-early design D1
    if parent.is_dir():
        return "directory", parent
    if parent.exists():
        return "not a directory", parent
    for above in parent.parents:
        if above.exists():
            return ("missing", above) if above.is_dir() else ("below a non-directory", above)
    return "missing", parent


def blocked_parent_sentence(parent, kind, path):
    """..."""   # ASCII; names design D2; called for the two blocked kinds only
    if kind == "not a directory":
        return f"The parent {parent} exists but is not a directory; choose a parent that is a directory."
    return (f"The parent {parent} cannot be created because {path} exists but is not a directory; choose a parent"
            " that is a directory.")
```

The fall-through return is unreachable (the resolved parent is absolute and
its `parents` end at the root, which exists; N2). Kinds are the four strings of
D1's table. A parent is blocked when the kind is `"not a directory"` or
`"below a non-directory"`. `blocked_parent_sentence()` is called for those two
kinds only (`design.md:85-87`); its docstring says so, since for `"directory"`
or `"missing"` its sentence (b) would be false.

**Call site 1, `known_obstacles()`** (`project:235-254`). Its signature, its
order (name, openRepoShape, parent) and its one call in `new()` (`:339`) stay.
The parent fact (`:247-253`) becomes one `parent_case(parent)` call:
`"directory"` adds nothing; `"missing"` adds today's missing sentence, the same
two string pieces byte for byte (`:252-253`); the blocked kinds add
`blocked_parent_sentence(parent, kind, path)`. Sentence (a) moves from
`:249-250` into `blocked_parent_sentence()`, byte for byte. The docstring
(`:236-240`) keeps "three local facts" and names this design for the walk.
The question (`:340`) and the Triad refusal (`:345-346`) still come from that
one list, so they cannot diverge (archived D1).

**Call site 2, the head of the bench branch.** Insert after `project:384` (the
shape-only flag refusal) and before `:385` (`choose(registry(workbenches(...)),
args)`):

```python
        # The head refusal (refuse-non-directory-parent-early design D1, D2): the parent read afresh.
        kind, path = parent_case(parent)
        if kind in ("not a directory", "below a non-directory"):
            raise Refused(blocked_parent_sentence(parent, kind, path) + " Nothing was created.")
```

It runs on every bench path: by flag, not asked, or after the answer `2`. It
never reuses the question's list, so a parent repaired while the question
waits is created and one broken during the wait is refused here (council V2).
It comes after every earlier refusal of FR-003 (name `:317-319`, positional
with `--into` `:320-321`, family `:323-324`, existing destination `:328-329`,
the hoisted `--workflow` check `:336-337` and the question `:338-363` when
asked, the shape-only flags `:383-384`) and before the workBenches lookup and
`choose()` (`:385`), the late `--workflow` check (`:388-390`), `Create:` and
the plan (`:392-393`), the dry run's return (`:394-395`), `confirm()`
(`:396-397`) and `parent.mkdir` (`:398`). `main()` prints the `Refused` as
`REFUSED: ...` on standard error and returns 2 (`:1143-1148`), unchanged.

Lane 4's ratified `support-later-python-versions` (on main since `15504f1`)
expects exactly this: `parent_case()` by that name, its head refusal at the
bench branch (`:383-385`), `known_obstacles()` changed (`:235-254`), and
`:322-329` untouched (its `design.md` Context `:41-43` and D7 `:376-378`).
This plan touches none of `:322-329`, and V5's `ast` check proves it (the span
from `parent = Path(args.into ...` through the existing-destination refusal is
byte for byte the base's, and `new()`'s only added block sits between the
shape-only refusal and the `row = choose(...)` line).

No exception handling is added (D1, N2). On 3.10 and 3.12 the reads ignore the
errors a missing or non-directory component gives; an unsearchable ancestor
raises earlier, at `destination.exists()` (`:328`).

The parent cases, as observed in the prototype on 3.12.3 and 3.10.21 (outputs
identical; research R1):

| Parent given | kind | at the question | at the head |
| --- | --- | --- | --- |
| `FILE`, a link to it, a FIFO, a socket, `/dev/null`, `FILE/` | not a directory | sentence (a) | refused, (a) |
| `FILE/sub`, `FILE/a/b`, a link to `FILE/x` | below a non-directory, ANCESTOR `FILE` | sentence (b) | refused, (b) |
| a missing path below a directory, a dangling link to one | missing | missing sentence | continues |
| a directory, a link to one | directory | none | continues |

### D2. Fixed text

All text is ASCII; `PARENT` is the resolved parent and `ANCESTOR` the path
`parent_case()` returns for case (b). The question's parent line under entry
1, exactly one when the parent is not a directory (`design.md:136-138`):

```text
     Not possible here: The parent directory PARENT does not exist; a Triad is created inside an existing directory.
     Not possible here: The parent PARENT exists but is not a directory; choose a parent that is a directory.
     Not possible here: The parent PARENT cannot be created because ANCESTOR exists but is not a directory; choose a parent that is a directory.
```

The Triad refusal keeps its shape (`design.md:147`). The head refusal
(`design.md:155-156`):

```text
REFUSED: The parent PARENT exists but is not a directory; choose a parent that is a directory. Nothing was created.
REFUSED: The parent PARENT cannot be created because ANCESTOR exists but is not a directory; choose a parent that is a directory. Nothing was created.
```

Only this early refusal says `Nothing was created.`; the backstop keeps its raw
errno (N4, D6).

**README.md**, four edits, each exact (`design.md:162-193`), the rest of each
paragraph unchanged and rewrapped:

| Edit | Where at `d47e8a4` | Fixed text | Replaced phrase (must then be found 0 times) |
| --- | --- | --- | --- |
| 1 | `:60-64`, from "or a parent that is missing or is not a directory." to the end of the paragraph `:57-64` | `design.md:169` | "or a parent that is missing or is not a directory."; "a parent that exists but is not a directory blocks both answers"; "a single-repository answer is unaffected." (with its full stop) |
| 2 | `:75-77`, the choosing-flag sentence | `design.md:177` | "without the question exactly"; "had before the question existed" |
| 3 | `:81-82`, the dry-run sentence | `design.md:184` | "its answer chose and writes nothing" |
| 4 | after "Existing destinations refuse." (ends `:96`), paragraph `:92-98` | `design.md:190` | none (an insertion) |

Rewrap recipe, so that the result is deterministic and the greps hold: refill
from the first line an edit touches to the end of its paragraph, greedily at 79
columns (the width of the prose around it: no prose line in `:48-120` exceeds
79 but the list item at `:72`), never breaking at a hyphen or inside a word
(`textwrap.wrap(width=79, break_on_hyphens=False, break_long_words=False)`).
Edits 2 and 3 share the paragraph `:75-82` and are refilled once from `:75`.
For edit 4, keep `:96` byte for byte and refill from the inserted text through
`:98`. A scratch run of exactly this recipe gives: edit 1 at lines 60-68
(`:57-59` unchanged), edits 2 and 3 at 79-86, edit 4 inserted as lines 101-105
with the old `:97-98` unchanged below it; lines `:53-55` are unchanged
(research R8).

**The README check** (FR-012) joins the file's lines with single spaces and
counts each text's occurrences: `tr '\n' ' ' < README.md | tr -s ' ' | grep
-oF -e 'TEXT' | wc -l`, never `grep -c` (on one joined line `grep -c` prints 1
for a text found twice). Expected: each of the four fixed texts 1 (edit 4 also
as "Existing destinations refuse. " followed by it), each replaced phrase 0,
and lane 4's phrase exactly 1 (see below); lines `:53-55` byte for byte. `quickstart.md`
("User Story 6") lists every command in full. This check supersedes feature
003's README check.

**Lane 4's README coupling.** Lane 4's realization later replaces, character
for character, "a parent that is a directory the person cannot write" in edit
4's text with "a parent that is a directory the person can search but cannot
write" (its `design.md:248-256`). That phrase is verbatim in `design.md:190`
and must appear exactly once in the README; with the recipe it falls on one
line (line 103). After edit 1 the anchor "Existing destinations refuse." ends
line 100, not the `README.md:96` lane 4's design cites; lane 4 replaces by
text, so nothing breaks.

The ASCII check covers the changed strings and added lines of `project`,
`tests/test_project.py`, `README.md`, this feature's directory and `[Q5]` the
change's `tasks.md`, not the whole files: `project` already carries em dashes
at `:197`, `:915`, `:928` and `:1136`, and `tests/test_project.py` one at
`:622` (archived N4). The check runs over the `+` lines of `git diff "$BASE"`.

### D3. Tests

All in `tests/test_project.py`; no new dependency. Research R5 is the run
inventory: every run D3 items 2 to 10 call for, with its id, the test it lives
in, its command and its exact expected result, and whether it is red or green
at the base. It carries agent T's inventory (98 new runs and the 2 of the
rewritten test), re-checked at `d47e8a4` (130 methods in `ProjectTests`, 96 of
them tests, 37 `test_pty_*`, 3 `test_inproc_*`; the precedent fixture at
`:58-62`; `pty_timeout` at `:146`), plus this plan's three runs (R-3.1, R-9.5b,
R-9.6b). This section fixes where each run lives.

**Insertion sites** (no existing line changes except inside the rewritten
test). Each is clear of #33's test hunks (`:25`, `:1033-1040`, and an
insertion after `:1040`):

| Site at `d47e8a4` | What | Notes |
| --- | --- | --- |
| after `:62` | the fixture block of D3 item 1 | before today's blank lines `:63-64` and `obstacles_refusal` (`:65`) |
| after `:405`, and after `:413` before `:414` | in `known_obstacle_cases()`: the local `below_line` beside `file_line` (`:405`), then the two case (b) rows | the rows go before the last row, so the dict's closing line `:415` stays; 0 removed lines (003 had to change its closing line) |
| after `:444` | the blocked-parent builder and the in-process helper | after `assert_parent_file_unchanged()` (`:439-444`), before `run_cli_streams()` (`:446`) |
| after `:1490`, before `:1491` | the `FILE/sub` row of `test_pty_dry_run_with_an_obstacle_refuses` | one `cases[...] = ...` statement after its `cases.update(...)`, formatting the fixture inline; its loop and checks (`:1491-1502`) apply as they stand |
| `:1526-1553` | the one rewritten test | its name stays |
| after `:1553`, before `:1555` | the 15 new test methods `[Q2]` | beside the obstacle tests |

The import block (`:2-19`) is not an insertion site: the builder imports
`socket` locally.

**Fixtures (D3 item 1)**, one block after `:62`, under a header naming
`openspec/changes/refuse-non-directory-parent-early/design.md`, D2, in the
precedent's form (`:58-61`). Names checked against every existing name in the
module and in #33's head (research R5):

- `OBSTACLE_PARENT_BELOW_A_NON_DIRECTORY`: `design.md:138` character for
  character, with `{PARENT}` and `{ANCESTOR}` its only format fields.
- `HEAD_REFUSAL_END = " Nothing was created."`, its own literal, pinned apart
  from `OBSTACLES_REFUSAL_END` (`:47`), equal in value (FR-014, report A3).
- `head_refusal(question_line)`: a module-level function like
  `obstacles_refusal` (`:65-68`), returning
  `question_line.split(OBSTACLE_LINE_START, 1)[1] + HEAD_REFUSAL_END`; tests
  prepend `REFUSED` (`:72`).
- Existing text this change keeps, pinned as literals because no test pins it
  as a constant today: `SHAPE_NEEDS_EXISTING_PARENT` = "Shape creation requires
  an existing --into parent directory." (`project:372`); `GENERATOR_LIST_FIRST`
  = "1. testBench:test" (the first line `choose()` prints for this registry,
  `project:196-197`; inline at `:1087` today); `[Q4]`
  `FAMILY_NOT_A_FOLDER_NAME` = "Family must be a single folder name."
  (`project:324`). The workBenches refusal (`project:96`) is excluded by exact
  equality of standard error, so it needs no literal; the permission error is
  built from `errno.EACCES` and `os.strerror()` (`errno` is imported at `:3`).

**The blocked-parent builder** (D3 item 1), a `ProjectTests` method after
`:444`, suggested name `blocked_parents()`. Under `self.base` (already
resolved, `:120`) it builds a regular file `FILE` with `parent_file_content`
through `parent_file_fixture()` (`:419`), and returns the twelve givens of
research R5, in R5's order, each as label to (arguments before the form's
flags, environment change, expected question line, the path whose type and
content must stay) `[Q1]` `[Q3]`:

| Id | Given | How | Line |
| --- | --- | --- | --- |
| K1 | the file | `--into FILE` | (a), PARENT FILE |
| K2 | a link to the file | `--into LINK`, `LINK -> FILE` | (a), PARENT FILE |
| K3 | a FIFO | `--into FIFO`, `os.mkfifo`, never opened | (a), PARENT FIFO |
| K4 | the file with a trailing slash | `--into` the string `str(FILE) + os.sep` (a `Path` drops the slash) | (a), PARENT FILE |
| K5 | below the file | `--into FILE/sub` | (b), FILE/sub, ANCESTOR FILE |
| K6 | two below the file | `--into FILE/a/b` | (b), FILE/a/b, ANCESTOR FILE |
| K7 | a link below the file | `--into LINKB`, `LINKB -> FILE/x` | (b), FILE/x, ANCESTOR FILE |
| K8 | a socket `[Q3]` | `--into SOCK`, an AF_UNIX socket bound and closed; when `bind` raises `OSError`, its subtests call `skipTest` | (a), PARENT SOCK |
| K9 | `/dev/null` `[Q3]` | `--into /dev/null` | (a), PARENT `/dev/null` |
| K10 | the file as the positional parent | `MyApp FILE` | (a), PARENT FILE |
| K11 | the file as `PROJECTS_DIR` | env `PROJECTS_DIR=FILE` | (a), PARENT FILE |
| K12 | the file as `~/projects` | a regular file at `HOME/projects`, `PROJECTS_DIR` removed | (a), PARENT `HOME/projects` |

The given names must differ from the 003 fixtures' (`file parent`, `link to
file parent`, ...) so a test can call both builders. Each run is its own
subtest, `with self.subTest(given=LABEL, form="F1"):`, keyword parameters only
(`subTest()` takes one positional parameter, `msg`, so a second positional
argument raises `TypeError`), so a failure names its given and form. Every
method with more than one run makes each run a subtest the same way (N6 with
`given` and `dry_run`, N7 and N8 with the row's label as `msg`, as
`:1435` does, N12 to N15 with `run`).

**The snapshot.** Each run takes `before = sorted(self.base.rglob("*"))` after
its own environment is built and just before it calls `project`, and compares
after the run. `question_env()` creates `self.base/bin` (through `fake_bin()`,
`:148-152`) and `shape_env()` writes the fake openRepoShape into it, so a
snapshot taken earlier, after the builder and before the first environment,
would differ after the first run and fail it: red for the wrong reason at the
base, and again after I1. An in-process run builds its environment inside
`run_inproc()` (`inproc_terminal()` calls `question_env()`, `:316`), so it
calls `obstacle_env()` or `self.fake_bin()` first, as `:1457` does, and then
takes the snapshot. Each run also checks the kept path:
`assert_parent_file_unchanged()` (`:439`) for a regular file (FILE itself for
K1, K2, K4 to K7, K10, K11; `HOME/projects` for K12), and a type check for K3,
K8 and K9 (`Path.is_fifo()`, `is_socket()`, `is_char_device()`).

**The in-process helper** (D3 item 7). `run_inproc()` (`:324-346`) pops
answers that are strings or exceptions, so it cannot replace the parent inside
the answer prompt. Decision: add a new helper after `:444`, suggested
`run_inproc_acting(*args, ci, answers)`, whose answers may also be callables,
called with the prompt, that return the answer; otherwise it behaves as
`run_inproc()` (the `inproc_terminal()` streams, the prompts list, the
"Scripted answers left unused" check). Do not edit `run_inproc()`: lane 4's
`tests/test_parent_reads.py` composes `ProjectTests` as a harness and relies on
its helpers (its `design.md:268-275` and `proposal.md:280`, which name
`run_inproc` among them), and an unchanged helper keeps FR-014's "unchanged"
true without reading it narrowly.

**The forms** (AC1's six), each matrix run ending with exit 2, standard output
empty (a pty transcript too, since no step writes input), standard error
exactly `REFUSED + head_refusal(line) + "\n"`, the snapshot (taken as above)
and the kept path unchanged, and, for F4 to F6, `assert_not_asked()` (`:369`):

| Form | Runner | Environment |
| --- | --- | --- |
| F1 `--type test --yes` | `run_cli` (`:141`) | `self.env` rebuilt from `self.question_env(None)` for each row, then the row's change |
| F2 `--type test --dry-run` | `run_cli` | the same |
| F3 `--type test`, at a terminal, no `--yes` | `run_pty` (`:210`), no steps | `question_env(None)` plus the row's change |
| F4 no choosing flag, `CI=true`, at a terminal | `run_pty`, no steps | `question_env("true")` plus the row's change |
| F5 no choosing flag, standard input not a terminal | `run_cli` | as F1, so that the runner's own `CI=true` is not what decides (as `:1654` does) |
| F6 name `alice-wip`, no choosing flag, at a terminal | `run_pty`, no steps | `question_env(None)` plus the row's change |

Rebuilding `self.env` per row keeps a later row from inheriting K12's dropped
`PROJECTS_DIR`.

**Where each run lives** (the method split is this plan's; D3 fixes the runs,
not the method boundaries; the lead ruled to keep this split). Test names start
with `test_pty_` for a pty test and `test_inproc_` for an in-process one
(feature 002's rule). Each pty form is its own method, so that no method holds
more than 13 pty runs (research R6). Run ids are research R5's:

| # | Method | Runs (research R5) | Expected, in short | At the base |
| --- | --- | --- | --- | --- |
| N1 | `test_blocked_parent_by_flag_is_refused_before_the_plan` | F1 and F2 for K1 to K12: 24 `[Q1]` `[Q3]` | the matrix rule above | red |
| N2 | `test_blocked_parent_is_refused_without_a_terminal` | F5 for K1 to K12: 12 `[Q1]` `[Q3]` | the matrix rule | red |
| N3 | `test_pty_blocked_parent_by_type_without_yes_is_refused` | F3 for K1 to K12: 12 `[Q1]` `[Q3]` | the matrix rule | red, waits at `Type yes` |
| N4 | `test_pty_blocked_parent_is_refused_where_ci_is_true` | F4 for K1 to K12: 12 `[Q1]` `[Q3]` | the matrix rule | red, waits at `Type yes` |
| N5 | `test_pty_blocked_parent_is_refused_for_a_workspace_name` | F6 for K1 to K12: 12 `[Q1]` `[Q3]`; plus R-3.1, `alice-wip --into FILE --dry-run` at a pty (the not-asked dry run "Considered and not asked" allows) | the matrix rule, R-3.1 too | red, waits at `Type yes` (R-3.1 red at once, exit 0) |
| N6 | `test_pty_single_answer_with_a_blocked_parent_is_refused_at_once` | R-4.1 to R-4.4: `FILE` and `FILE/sub`, answer `2`, with and without `--dry-run`; first a second available generator appended to `self.config` and saved, as `:1066-1068` does (per test); env `shape_env(None)`, so the parent's line is the only obstacle | exit 2; `assert_question()` with the case's line; `assert_line_ends(stderr, REFUSED + head_refusal(line))` and exactly one `REFUSED:` line; neither stream holds `GENERATOR_LIST_FIRST`, `GENERATOR_PROMPT`, `Create:` or `CONFIRM_PROMPT`; no openRepoShape record; snapshot and FILE unchanged; the transcript's tail is not asserted (the prompt may print on standard error) | red, waits at `Select a generator number` |
| N7 | `test_pty_triad_answer_below_a_file_leaves_the_file_intact` `[Q2]` | R-5.6, R-5.7: the two case (b) rows of `known_obstacle_cases()`, selected by label and counted (`assertEqual(len(rows), 2)`), a Triad answer at a pty as `:1433-1450` does | its existing assertions, plus `assert_parent_file_unchanged(Path(extra[1]).parent, before)`: FILE, the ancestor the refusal names, not the row's `--into` `FILE/sub` | red (sentence (b) absent) |
| N8 | `test_inproc_triad_answer_below_a_file_leaves_the_file_intact` `[Q2]` | R-5.8, R-5.9: the same rows in process, as `:1452-1475` does | the same, with the same check on `Path(extra[1]).parent` | red |
| N9 | `test_inproc_parent_repaired_while_the_question_waits_is_created` | R-7.1, through `run_inproc_acting()` | exit 0; prompts the question and `Type yes`; line (a) printed; `assert_created()` inside the new directory | GREEN (guard) |
| N10 | `test_inproc_parent_broken_while_the_question_waits_is_refused` | R-7.2 | exit 2; standard error exactly the head refusal (a) for it; prompts only the question; nothing created | red |
| N11 | `test_dangling_link_parent_is_created_as_before` | R-8.1 | exit 0; standard output `creation_stdout("MyApp", target)`; standard error the two advisory lines; the repository created in the link's target | GREEN (guard) |
| N12 | `test_blocked_parent_is_refused_before_later_faults` | R-9.1 `--type nomatch --yes`, R-9.2 `--type test --workflow --yes` (`setup-openspeckit` asserted absent), `[Q4]` R-9.8 `--type test --yes --workbenches DIR` (no `config/bench-config.json` in DIR) | each exit 2, standard output empty, standard error exactly the head refusal (a) for FILE | red |
| N13 | `test_earlier_refusals_keep_their_text_with_a_blocked_parent` | R-9.3 `--org example --yes`, R-9.4 the name `bad name`, `[Q4]` R-9.7 `--family 1bad --yes` | each exit 2, standard output empty, standard error exactly `REFUSED` + its own text (`ORG_NEEDS_SHAPE`, `INVALID_NAME`, `FAMILY_NOT_A_FOLDER_NAME`) | GREEN (guard) |
| N14 | `test_shape_by_flag_keeps_its_parent_refusal_with_a_blocked_parent` | R-9.5, R-9.6 (`FILE`, with and without `--dry-run`), R-9.5b, R-9.6b (`FILE/sub`, the same; spec US5 scenario 3) | each exit 2, standard output empty, standard error exactly `REFUSED + SHAPE_NEEDS_EXISTING_PARENT` | GREEN (guard) |
| N15 | `test_unwritable_directory_child_passes_dry_run_and_fails_at_creation` | R-10.1, R-10.2; skipped when `os.geteuid()` is missing or returns 0; the mode-755 restore registered with `addCleanup` before the `chmod(0o555)` | `--dry-run`: exit 0, the plan, standard error empty; `--yes`: exit 2, the plan, standard error exactly `REFUSED: [Errno EACCES] TEXT: 'CHILD'` from `errno` and `os.strerror()`, no `Nothing was created.`; the child never created | GREEN (guard) |

Existing tests that gain runs (rows are added; no existing tuple changes):

- `known_obstacle_cases()` gains `parent below a file` = `("MyApp", True,
  ("--into", FILE / "sub"), [line_b])` and `all three with the parent below a
  file` = `("my-app", False, ("--into", FILE / "sub"), [name_line,
  OBSTACLE_OPENREPOSHAPE, line_b])`, with `FILE` the method's `parent_file`
  (`:404`) and `line_b` the local `below_line =
  OBSTACLE_PARENT_BELOW_A_NON_DIRECTORY.format(PARENT=parent_file / "sub",
  ANCESTOR=parent_file)`, inserted after `:405`. `test_pty_triad_answer_with_an_obstacle_refuses` and
  `test_inproc_triad_obstacle_runs_nothing` then run them (R-5.1 to R-5.4) with
  their existing assertions; their guard (`:1439`, `:1460`) is False for
  `FILE/sub`, so they do not check the file for these rows, which is why N7
  and N8 exist `[Q2]`.
- `test_pty_dry_run_with_an_obstacle_refuses` gains `parent below a file`
  (R-5.5); its per-row snapshot (`:1500`) and its final file check (`:1502`)
  apply.

**The rewritten test (D3 item 6; N3, AC5)**:
`test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path`
(`:1526-1553`) keeps its name and its comparison form (R-6.1, R-6.2). Its
comment names this design. The asked run answers `2` only
(`steps=[(QUESTION_PROMPT, "2")]`); the baseline is `--type test` with no step.
Both exit 2; the asked run's question carries line (a); the baseline is not
asked; neither standard output contains `Create:`; the `REFUSED:` line of each
(compared from `REFUSED:` on, since the question's prompt shares the asked
run's standard error line: the prototype showed `Create it as a Triad? [Y/n or
1/2]: REFUSED: ...`) is one line, equal across the two, and equal to `REFUSED
+ head_refusal(line_a)`; no `warning:` line in either; no openRepoShape record;
the snapshot and the file unchanged. It is the one existing test rewritten; the
two members of the Constraints gain added lines only `[Q2]`.

**Answer-2 runs read standard error by line end.** In every run that answers
at a prompt (N6, the rewritten test), the refusal follows the prompt on the
same standard error line, as above; assert with `assert_line_ends()`
(`:355`) and a count of `REFUSED:` lines, not whole-stream equality.

**Counts** `[Q1]` `[Q2]` `[Q3]` `[Q4]`. 101 new runs (T's 98 plus R-3.1,
R-9.5b and R-9.6b) and the 2 rewritten: by runner, 49 `run_cli`, 46 `run_pty`,
6 in process (research R5, R7). The suite goes from `N0` tests, the merge
base's count, to **`N0 + 15`** (N1 to N15; 96 and 111 at `d47e8a4`); of the
answers only `[Q2]` changes the 15. On a quiet machine
at about 0.09 s a run this adds about 9 s; on a heavily loaded bench about
50 s.

### D4. The feature records

`specs/002-triad-first-project-new/` and `specs/003-parent-obstacle-wording/`
are not edited; the spec carries the supersession statement (D4, spec
"Supersession"). `traceability.md` is built during implementation, as feature
003's was: its precedent file was first added by 003's implementation commit
`f492558` (task T002 of its Phase 1), not by the plan commit `393bfe4`. It maps
each of the delta's 40 scenarios, by requirement and title, to its tests. Two
mappings are fixed (FR-015): the rewritten test to "A single repository taken
at the question with a parent blocked by a non-directory", and
`test_pty_single_answer_is_unaffected_by_obstacles` to "A single-repository
answer is unaffected" (feature 003's `traceability.md:25`). The planned map for
the 20 scenarios this feature adds, alters or re-pins is under "Coverage map"
below. Each of the other 20 takes the Tests cell feature 002's
`traceability.md` gives its title (each of the 20 titles is there), except
"No known obstacle", which takes feature 003's cell
(`specs/003-parent-obstacle-wording/traceability.md:26`):
`test_pty_symbolic_link_to_a_directory_names_no_obstacle`, which feature 003
added, and `test_pty_no_known_obstacle_names_none`. This feature adds no test
for that scenario; check `traceability` asserts the two names in its row.

### D5. Handoffs after landing (a lane step, not an implementation task)

No new issue. When the realization merges, the lane posts one comment on
workBenches#145 if it is still open, naming the merge sha and the sha256 of
`project` at that sha (`git show <sha>:project | sha256sum`) as an alternative
pin target; if #145 is closed, nothing is posted. Then the change is archived
(its `tasks.md` 3.2, 3.3).

### D6. What is not changed

- The shape branch's refusal (`project:371-372`), `parent.mkdir` (`:398`),
  `main()`'s handlers (`:1143-1151`), `ask()`, `confirm()`, `choose()`,
  `execute()`, `print_creation_question()`, `ask_twice()`, the question's
  prompts, and everything from `discover()` (`:433`) down.
- `new()` above the bench branch, in particular `:322-329` (lane 4's sites).
- No permission is read; no line under entry 2; no CI change; the README's
  "Python 3.10+".
- The archived N1 residuals and the symbolic-link loop: lane 4's change, which
  will supersede any statement here that they behave as today (its
  `design.md` D8).

## Work breakdown for /speckit-tasks

The phases, file sets and writers below are what the tier tags need. A task
fails if its diff touches a file outside its file set. Within a file set
exactly one writer works at a time; tasks on the same file set run in the
order given and each commits alone with explicit pathspecs. Parallel work is
only across file sets. Tiers: no task is `[H]` (the lead's ruling); every
task is `[S]`, well scoped, except I1, `[O]`, hard or cross-cutting (lead's
ruling), and the lead has ruled on G1.

**The first implementation commit** is the first commit on the branch that
touches `project`, `tests/test_project.py` or `README.md`. Commits under
`specs/` (the spec, this plan, `tasks.md`, `qs.sh`, the traceability skeleton)
are record commits, not implementation commits: G1 comes before the first
implementation commit and may come before or after the record commits.

**File sets and writers**

| Set | Files | Writer |
| --- | --- | --- |
| FS-G `[Q5]` | `openspec/changes/refuse-non-directory-parent-early/tasks.md` | one `[S]` writer, copying "G1 and G2 exact text" below (lead's ruling) |
| FS-D | `specs/006-refuse-non-directory-parent-early/traceability.md` | one writer |
| FS-T | `tests/test_project.py` | one writer at a time, tasks in order |
| FS-P | `project` | one writer |
| FS-R | `README.md` | one writer |
| FS-L | `specs/006-refuse-non-directory-parent-early/tasks.md` (ticks) | the lane lead only |
| FS-Q | `specs/006-refuse-non-directory-parent-early/qs.sh` | the lane lead only, in the planning commit with `plan.md`, `research.md` and `quickstart.md`; its text is "qs.sh (exact text)" below; no build task edits it |

Throughout, a check's `BASE` is `git merge-base origin/main HEAD`, never a
fixed sha, so that the checks hold whether #33 lands before or after this
feature (research R9); the runner computes it. "Check `ID`" in a verify cell
means: run `bash specs/006-refuse-non-directory-parent-early/qs.sh ID
[NAME=VALUE ...]`, from anywhere in the worktree, in the foreground, with the
variables the cell names (`STAGE=g1` check `governance` is `qs.sh governance
STAGE=g1`); the verify passes when it exits 0. The runner is one committed
file, "qs.sh (exact text)" below. It takes the block whose first line is
`# check: ID` from `quickstart.md`, so the twelve blocks stay the single source
of check code, and it exits 2, not 1, when that marker is missing or repeated,
so a "must fail" check reads exit 1, not "non-zero". No verify relies on a
variable, function or file that an earlier call left: the Bash tool keeps no
shell state between calls (research R15). Every check exits non-zero on any
mismatch. The ids:
`suite`, `readme-texts`, `ascii-added`, `files-changed`, `fixed-text`,
`ast-project`, `ast-tests`, `red-first`, `openspec`, `traceability`,
`governance`, `merge-check`. `RF` is check `red-first`: a scratch copy (`git
archive HEAD`, the working tests file copied in, `project` from `$BASE`) with
`ProjectTests.pty_timeout = 5` for that process only, which judges each named
test by its red, passed and skipped subtests and, for N6, N7, N8, N10 and the
three tests that gain rows, by the planned reason it reads from each
failure's traceback and message ("red for the wrong reason" fails it). The
tests a verify cell names go in `TESTS`, one argument, separated by spaces.

| Phase | Slice | Set | Tier | Content | Verify |
| --- | --- | --- | --- | --- | --- |
| 0 `[Q5]` | G1 | FS-G | `[S]` | The six line replacements of "G1 and G2 exact text" (1.6, 2.1, the handoff fields), nothing else, committed alone before the first implementation commit | `STAGE=g1` check `governance` |
| 1 | S1 | none | `[S]` | Baseline | `ADDED=0` check `suite` (`Ran N0 tests`, `OK`); `git diff --quiet "$(git merge-base origin/main HEAD)" -- project tests/test_project.py README.md` exits 0 |
| 1 | S2 | FS-D | `[S]` | `traceability.md` skeleton (lane line first): 40 rows, by requirement and title in file order; the 20 unaltered scenarios filled with the cell feature 002's `traceability.md` gives each, "No known obstacle" with feature 003's (D4); the rest filled as tests land (V7) | `MODE=skeleton` check `traceability` |
| 2 | T1 | FS-T | `[S]` | The fixture block after `:62` `[Q4]` | `PARTS=fixtures` check `fixed-text`; `ADDED=0` check `suite` |
| 2 | T2 | FS-T | `[S]` | The local after `:405`, the two rows after `:413`, and the dry-run row after `:1490` `[Q2]` | check `red-first` with the three tests' names: each red in exactly its new rows, for the planned reason (the check reads it: sentence (b) expected, the missing sentence printed, not in `assert_parent_file_unchanged`) |
| 2 | T3 | FS-T | `[S]` | `blocked_parents()` after `:444`; N1, N2 `[Q1]` `[Q3]` | check `red-first` with N1 and N2: red in 24 and 12 subtests (skipped socket subtests counted) |
| 2 | T4 | FS-T | `[S]` | N3, N4, N5 (with R-3.1) `[Q1]` `[Q3]` | check `red-first` with N3 to N5: red in 12, 12 and 13 subtests |
| 2 | T5 | FS-T | `[S]` | N7, N8 `[Q2]` | check `red-first` with N7 and N8: red in 2 subtests each, for the planned reason, which the check reads from each failure: on the text (sentence (b) expected, the missing sentence printed), never inside `assert_parent_file_unchanged` |
| 2 | T6 | FS-T | `[S]` | The rewritten test `[Q2]` | check `red-first` with its name: red as a whole |
| 2 | T7 | FS-T | `[S]` | N6 (`GENERATOR_LIST_FIRST` is T1's) `[Q2]` | check `red-first` with N6: red in 4 subtests, each waiting at `Select a generator number` (the check reads it; it proves the second generator is in place, which M2 needs) |
| 2 | T8 | FS-T | `[S]` | `run_inproc_acting()` after `:444`; N9, N10 `[Q2]` | check `red-first` with N9 and N10: N9 green, N10 red as a whole because `Type yes to run this plan:` is asked (the check reads it), not on an error in `run_inproc_acting()` |
| 2 | T9 | FS-T | `[S]` | N11 to N15 `[Q2]` `[Q4]` | check `red-first` with N11 to N15: N12 red in 3 subtests; N11, N13, N14, N15 green |
| 3 | I1 | FS-P | `[O]` | D1's helpers, `known_obstacles()`, the head check | check `suite` (`Ran N0+15 tests`, `OK` `[Q2]`); check `ast-project` |
| 3 | I2 | FS-R | `[S]` | The four README edits with the rewrap recipe | check `readme-texts` |
| 4 | V1 | none | `[S]` | Full suite on 3.12.3 and on 3.10 with PyYAML | check `suite` with `PY=python3`, and with `PY` a 3.10 interpreter (the check links PyYAML in when it lacks it): both `Ran N0+15 tests`, `OK` `[Q2]`. A 3.10 run without PyYAML is informational only: it fails exactly the 11 YAML tests research R11 names, as at the base |
| 4 | V2 | none | `[S]` | Red-first record `[Q1]` `[Q2]` `[Q3]` `[Q4]` | check `red-first` (the whole list): `checkpoint as planned` |
| 4 | V3 | none | `[S]` | Mutation checks in scratch copies | quickstart "Mutation checks": for M1 to M3, check `red-first` with `MUTANT` and `RF_MUST_FAIL` (M1: N9, N10; M2: N12, N6; M3: N9, N13, N14) prints `mutant caught`; for M4, `PROJECT=M4` check `ast-project` exits 1 (a runner exit of 2 is not a pass) |
| 4 | V4 | none | `[S]` | ASCII `[Q5]`, fixed text, README | checks `ascii-added`, `fixed-text` and `readme-texts` |
| 4 | V5 | none | `[S]` | Diff and `ast` checks | checks `files-changed` (FR-016 `[Q5]`; `qs.sh` among the changes), `ast-project` and `ast-tests` (15 new test methods `[Q2]`) |
| 4 | V6 | none | `[S]` | OpenSpec | check `openspec` (the change valid; `Totals: N passed, 0 failed`, 9 of 9 at `d47e8a4`) |
| 4 `[Q5]` | G2 | FS-G | `[S]` | The 2.2 tick of "G1 and G2 exact text", after V1, committed alone | `STAGE=g2` check `governance` |
| 5 | V7 | FS-D | `[S]` | Complete `traceability.md` `[Q2]` | check `traceability` (40 rows, no empty Tests cell, every named test defined, FR-015's two mappings, "No known obstacle" with 003's two tests) |

The hand walk and the adversarial review are not slices: see "Lane steps".

I1 is `[O]` and no slice is `[H]` (lead's rulings). I1 is the one behavioral
slice, its order and placement semantics are subtle (the mutants M1 to M3 of
research R10 are each a plausible wrong placement that still prints the right
sentence), and lane 4's realization is coupled to it. The builder (T3) and the pty forms (T4) are
separate attempts so that one miss does not escalate the whole matrix, and the
in-process helper lands with its first users (T8). Merging main into the
branch (below) is the lead's, not a build task.

**Lane steps** (the lane lead's, after Phase 5). In the later `tasks.md` these
are a plain numbered list, not checkbox tasks and not tier-tagged, as feature
003's "Lane steps" were; no build agent runs them. The first two come before the
pull request opens:

1. The hand walk `[Q3]` `[Q4]`: the lead or Brett Heap walks `quickstart.md`,
   User Stories 1 to 6, at a real terminal (User Story 4 needs two terminals)
   before the pull request opens, and records each divergence as a defect for
   the lead to rule on. A dispatched writer has no terminal.
2. The adversarial review: the lead dispatches the `[O]` adversarial review at
   the branch head, after Phase 5 and the walk, and records its verdict before
   the pull request opens. An independent reviewer re-runs every check through
   `qs.sh` and reads the diff against the spec, `design.md` D1 to D6 and this
   plan; its report names the head sha, gives each check's exit status (all 0),
   and lists every finding as fixed or ruled on by the lead.
3. Push the branch (a plain push) and open the realization as a draft pull
   request to main; its body carries `Closes #20` and the line
   `Lane: openRepoProject-1`.
4. When #33 is on main: `HEAD33=origin/main` check `merge-check`, then merge
   main in ("Other lanes", below) and re-run the checks of Phases 4 and 5 on
   the merge.
5. Mark the pull request ready once the review's findings are resolved and both
   CI jobs (`ubuntu-latest`, Python 3.10 and 3.12) are green.
6. Land only on Brett Heap's word for that pull request, quoted with its
   link; no rebase, no force push.
7. After landing: cite the merge sha in the change's `tasks.md` 3.1 (`gh pr
   view <n> --json mergeCommit,statusCheckRollup`); post D5's one comment on
   workBenches#145 if it is still open (3.2), nothing if it is closed; open no
   new issue.
8. The archive pull request: `/opsx:archive` for
   refuse-non-directory-parent-early (3.3), its `openspec validate --all
   --strict` run with `/usr/bin/openspec` or the openspec in py-bench.
9. Retire the worktree and its branch once the realization and the archive
   have landed.

**qs.sh (exact text)**. The committed check runner,
`specs/006-refuse-non-directory-parent-early/qs.sh`. The lane lead adds it in
the planning commit with `plan.md`, `research.md` and `quickstart.md`, as this
text, character for character; check `files-changed` requires it among the
committed changes, and no build task edits it (FS-Q). It is ASCII, uses `set
-u` and makes no network call. Its interface:

- `bash specs/006-refuse-non-directory-parent-early/qs.sh <check-id>
  [NAME=VALUE ...]`, from anywhere in the worktree: it changes to `git
  rev-parse --show-toplevel` first (outside a git work tree it stays in the
  current directory, which a plain scratch copy needs, with `BASE=<sha>`
  passed), so a path in a `NAME=VALUE` is read from the top of the worktree.
- `BASE` defaults to `git merge-base origin/main HEAD`, unless the call passes
  `BASE=<sha>`; a `BASE` in the caller's environment is ignored.
- It takes from the `quickstart.md` in the script's own directory the fenced
  block whose first line is exactly `# check: <check-id>`. If that marker is
  missing, or starts more than one block, it prints a message and exits 2.
- It exports `BASE` and each `NAME=VALUE`, runs the block with bash, and exits
  with the block's status. Exit 2 therefore means "the runner could not run
  the check", and a check that must fail is read as exit 1.

```bash
#!/usr/bin/env bash
# qs.sh: run one check of this feature's quickstart.md as one command, with no shell state from the caller.
#
# Usage: bash specs/006-refuse-non-directory-parent-early/qs.sh <check-id> [NAME=VALUE ...]
#
# It works from anywhere in the work tree: it changes to the top of the work tree first, so a path given in
# a NAME=VALUE is read from there (give an absolute path, or one relative to the top of the work tree).
# It takes the fenced block of the quickstart.md in this script's own directory whose first line is exactly
# "# check: <check-id>", exports BASE and every NAME=VALUE, runs the block with bash and exits with the
# block's own status. BASE is "git merge-base origin/main HEAD" unless the call passes BASE=<sha>; a BASE
# left in the caller's environment is ignored. Exit 2 means the runner could not run the check (bad
# arguments, no such block, or the marker found on more than one block); any other status is the block's.
# Outside a git work tree it stays in the current directory (a plain scratch copy: run it from the copy's
# top and pass BASE=<sha>). Inside one, the script must be the work tree's own copy.
# No network is used.
set -u

die() { printf 'qs.sh: %s\n' "$*" >&2; exit 2; }

[ "$#" -ge 1 ] || die "usage: bash specs/006-refuse-non-directory-parent-early/qs.sh <check-id> [NAME=VALUE ...]"
ID=$1; shift
case $ID in
  "" | *[!A-Za-z0-9._-]*) die "bad check id '$ID'" ;;
esac
unset BASE
for ARG in "$@"; do
  case $ARG in
    [A-Za-z_]*=*) ;;
    *) die "bad argument '$ARG'; expected NAME=VALUE" ;;
  esac
  case ${ARG%%=*} in
    *[!A-Za-z0-9_]*) die "bad variable name in '$ARG'; expected NAME=VALUE" ;;
  esac
done

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P) || die "cannot find this script's directory"
QS=$HERE/quickstart.md
[ -f "$QS" ] || die "no quickstart.md next to this script ($QS)"
ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || ROOT=
if [ -n "$ROOT" ]; then
  [ "$HERE" = "$ROOT/specs/006-refuse-non-directory-parent-early" ] \
    || die "this script is in $HERE, not in the work tree at $ROOT; run it from the work tree that holds it"
else
  ROOT=$(pwd -P)
fi
cd "$ROOT" || die "cannot change to $ROOT"

for ARG in "$@"; do export "$ARG"; done
if [ -z "${BASE:-}" ]; then
  BASE=$(git merge-base origin/main HEAD 2>/dev/null) && [ -n "$BASE" ] \
    || die "cannot compute BASE (git merge-base origin/main HEAD failed); pass BASE=<sha>"
fi
export BASE

# One pass: the number of blocks that start with the marker, then the text of the block(s).
OUT=$(awk -v id="$ID" '
  /^ *```/ { if (inb) { inb = 0; grab = 0 } else { inb = 1; first = 1 }; next }
  inb && first { first = 0; if ($0 == "# check: " id) { grab = 1; n++ } }
  grab { buf = buf $0 "\n" }
  END { print n + 0; printf "%s", buf }' "$QS") || die "cannot read $QS"
N=${OUT%%$'\n'*}
BLOCK=${OUT#*$'\n'}
case $N in
  1) ;;
  0) die "no block of $QS starts with '# check: $ID'" ;;
  *) die "'# check: $ID' starts $N blocks of $QS; it must start exactly one" ;;
esac

printf 'qs.sh: check %s at BASE %s in %s\n' "$ID" "$BASE" "$ROOT" >&2
exec bash -c "$BLOCK" "qs.sh:$ID"
```

**G1 and G2 exact text** `[Q5]`. In
`openspec/changes/refuse-non-directory-parent-early/tasks.md` at `d47e8a4`,
the lines holding "to be created" are 31, 36, 37 and 38, and the unticked
boxes 1.6, 2.1, 2.2 (lines 16, 20, 21) and 3.1 to 3.3. Each "before" below is
the line as it stands (checked with `git show d47e8a4:<path>`); each "after"
is copied character for character. Lines 16, 20 and 21 are each one line in
the file.

G1 replaces six whole lines and changes nothing else:

- Line 16, before: `- [ ] 1.6 Ratified by Brett Heap's word "ratify 21", quoted with its link on PR #21; PR #21 lands by squash; verified by that quote. No implementation starts before it.`
  After: `- [x] 1.6 Ratified by Brett Heap's word "ratify 21" (2026-10-21), quoted with its link on PR #21 (https://github.com/opensoft/openRepoProject/pull/21#issuecomment-6313890629); PR #21 landed by squash as b23333397f989462d13cf625c69e41bee8da8700 (of 8f3ca2d); verified by that quote. No implementation started before it.`
- Line 20: change its leading `- [ ] 2.1` to `- [x] 2.1`, keep the rest of the line byte for byte, and append, after its final `filled in once.`, one space and: `Created: feature 006-refuse-non-directory-parent-early on branch 006-refuse-non-directory-parent-early (worktree ../openRepoProject-worktrees/006-refuse-non-directory-parent-early, cut from main at b233333; 006 was the next free number on 2026-10-21), spec at specs/006-refuse-non-directory-parent-early/spec.md.`
- Line 31, before: `Implementation is tracked exclusively in one Speckit feature, to be created`
  After: `Implementation is tracked exclusively in one Speckit feature, created`
  (line 32, which begins `by` and the backticked `/speckit.specify`, stays as it is).
- Line 36, before: ``- Feature identifier: to be created by `/speckit.specify` after ratification (the next free number that day)``
  After: `- Feature identifier: 006-refuse-non-directory-parent-early`
- Line 37, before: `- Branch: to be created with the feature`
  After: `- Branch: 006-refuse-non-directory-parent-early (worktree ../openRepoProject-worktrees/006-refuse-non-directory-parent-early, cut from main at b233333)`
- Line 38, before: ``- Tasks: `specs/<feature>/tasks.md` (to be created by `/speckit.tasks`)``
  After: `- Tasks: specs/006-refuse-non-directory-parent-early/tasks.md (created by /speckit.tasks)`

G2 replaces one line, in Phase 4 after V1, and changes nothing else:

- Line 21: change its leading `- [ ] 2.2` to `- [x] 2.2`, keep the rest of the line byte for byte, and append, after its final `` `/opsx:apply`. ``, one space and: `Met: the handoff named feature 006-refuse-non-directory-parent-early at G1SHA before the first implementation commit FIRSTSHA.`
  with `G1SHA` and `FIRSTSHA` replaced by the short shas the G2 commands below print.

This follows feature 003. Its specify commit `90a4cee` ticked 1.6 and 2.1
and filled the handoff fields, and left 2.2 unticked. The last commit of its
branch ("Tick T001 to T018 on the verified evidence; fix the Phase 2
checkpoint; tick OpenSpec 2.2", listed in the message of the squash
`f401e06`) ticked 2.2 with "Met: the handoff named feature
003-parent-obstacle-wording at 90a4cee before the first implementation commit
f492558" (`openspec/changes/archive/2026-10-09-fix-parent-obstacle-wording/tasks.md:21`).
2.2's own wording, "verified by reading that section before the first
`/opsx:apply`", records a verification whose evidence, the first
implementation commit, does not exist when G1 runs; so 2.2 is ticked once it
does. This is Q5 A as Brett Heap answered it (the clarify file, as corrected at
`f700336`): the 2.2 tick lands later in the same realization PR.

The facts in G1 and G2 were checked: `b233333` is
`b23333397f989462d13cf625c69e41bee8da8700`, the squash of `8f3ca2d`
(`git ls-remote origin refs/pull/21/head` prints `8f3ca2d0759e...`, and the
change's files are the same at both); the branch's first commit `447f2a8` has
parent `b233333`; the quote's link is the one the spec's header cites
(`spec.md:24`). Today no commit after the merge base touches the change's
`tasks.md` or an implementation path, so the two commands below print nothing
until G1 and the first implementation commit exist. A scratch
application of G1's six replacements and then G2's, both extracted from this
plan by the script of `quickstart.md` ("Governance record"), matched every
"before" line and passed every part of check `governance` that does not need
a commit (research R14).

Verify: right after the G1 commit, `STAGE=g1` check `governance`; right after
the G2 commit, `STAGE=g2` check `governance` (quickstart "Governance record",
which holds `check_ticks.py` and every count in full). Before writing G2, the
writer prints the two shas, in one Bash call (the block defines what it uses).
FIRSTSHA is the first implementation commit as defined above, so the pathspec
names `project`, `tests/test_project.py` and `README.md` only, not
`specs/`:

```bash
BASE=$(git merge-base origin/main HEAD); F=openspec/changes/refuse-non-directory-parent-early/tasks.md
git log --reverse --format=%h "$BASE"..HEAD -- "$F" | head -n 1                                      # G1SHA
git log --reverse --format=%h "$BASE"..HEAD -- project tests/test_project.py README.md | head -n 1   # FIRSTSHA
```

**Phase 2 checkpoint** `[Q1]` `[Q2]` `[Q3]` `[Q4]` (against the unchanged
`project`, by check `red-first`): red are N1 to N8, N10, N12, the rewritten test, and the new rows of the
three existing tests; green are N9, N11, N13, N14, N15 and every other existing
test and row. The eleven green runs (R-7.1, R-8.1, R-9.3 to R-9.7, R-9.5b,
R-9.6b, R-10.1, R-10.2) cannot show red first: they are guards of behaviour
that must not change, and V3's mutants show that the guards bite (N9 fails if
the head reuses the question's read; N13 and N14 fail if the check moves before
the question, W3).

## Coverage map (the 20 scenarios the feature adds, alters or re-pins)

Of the delta's 40 scenarios, 11 are new titles (the 10 ADDED and "The parent
would be created below a path that is not a directory"), 5 change their text,
and 24 are identical to main; four identical ones are mapped here too, since
sentence (b) now applies to them. The other 20 are in feature 002's
`traceability.md` by title.

| Delta scenario | Planned tests |
| --- | --- |
| ADDED "A flag-chosen single repository with a parent that is not a directory" | N1, N2, N3, N4, N5 (case (a) givens) |
| ADDED "A flag-chosen single repository below a path that is not a directory" | N1, N3 (case (b) givens) |
| ADDED "A single-repository dry run with a parent blocked by a non-directory" | N1 (F2), N5 (R-3.1), N6 (with `--dry-run`) |
| ADDED "A single repository taken at the question with a parent blocked by a non-directory" | the rewritten test (FR-015), N6 |
| ADDED "A parent repaired or broken while the question waits" | N9, N10 |
| ADDED "A single repository with a parent that is not blocked" | N11, `test_new_preserves_paths_with_spaces_and_writes_profile`, `test_dry_run_creates_no_parent` |
| ADDED "A parent the person cannot write still fails only at creation" | N15 |
| ADDED "The parent refusal comes after the earlier refusals" | N13 |
| ADDED "The parent refusal comes before generator selection" | N12 |
| ADDED "The shape branch's parent refusal is unchanged" | N14 |
| MODIFIED "Preview" | `test_pty_dry_run_single_answer_prints_the_generator_plan`, `test_advisory_silent_cases`, `test_dry_run_creates_no_parent` |
| MODIFIED "A dry run asks too" | `test_pty_dry_run_single_answer_prints_the_generator_plan`, N6 (with `--dry-run`) |
| MODIFIED "The refusal order of an invocation not asked the question is unchanged" | `test_workflow_refusal_order_unchanged_when_not_asked` |
| MODIFIED "Answers that take a single repository" | `test_pty_single_answers_take_the_bench_path`, N6 |
| MODIFIED "The parent directory is missing" | the existing rows (003 traceability row 3) |
| MODIFIED "The parent exists but is not a directory" | the existing rows (003 traceability row 4) |
| MODIFIED "The parent would be created below a path that is not a directory" | the new rows in `test_pty_triad_answer_with_an_obstacle_refuses`, `test_inproc_triad_obstacle_runs_nothing`, `test_pty_dry_run_with_an_obstacle_refuses`; N7, N8 `[Q2]` |
| MODIFIED "A Triad answer with a known obstacle" | `test_pty_triad_answer_with_an_obstacle_refuses`, `test_inproc_triad_obstacle_runs_nothing`, N7, N8 |
| MODIFIED "A dry run with a known obstacle" | `test_pty_dry_run_with_an_obstacle_refuses` |
| MODIFIED "A single-repository answer is unaffected" | `test_pty_single_answer_is_unaffected_by_obstacles` (FR-015) |

The rewritten test maps to the ADDED scenario only, not also to "A
single-repository answer is unaffected" (lead's ruling): with a file parent
the single-repository path's steps are never reached, so listing it there
would mislead, although feature 003's `traceability.md:25` listed its earlier
form under that title.

**Coverage note, FR-003's "a standard input or output that is not a
terminal".** The new runs pin the standard-input half only: F5 (N2) runs
`project` with standard input a pipe. Both halves reach the same rule,
`offer = not workspace and not chosen and person_at_terminal()` (`project:334`),
and `person_at_terminal()` is true only when `CI` reads false and standard
input and standard output are both terminals (`project:217-225`); the head
check comes after that decision and reads no terminal, so a standard output
that is not a terminal reaches it the same way. Existing tests pin the output
half:
`test_inproc_person_at_terminal_rule` (`tests/test_project.py:1042-1063`, the
pair `(True, False)`, standard input a terminal and standard output not, at
`:1049-1052`) and, end to end for a directory parent,
`test_inproc_stdout_not_a_terminal_is_not_asked` (`:1664-1671`: not asked, the
confirmation is the only prompt, the repository is created). No new run pins a
blocked parent with standard output not a terminal.

## Project Structure

### Documentation (this feature)

```text
specs/006-refuse-non-directory-parent-early/
  spec.md                  feature specification (/speckit-specify), with its Clarifications as answered
  clarify-questions.md     the five questions (/speckit-clarify)
  checklists/requirements.md
  plan.md                  this file (/speckit-plan)
  research.md              Phase 0 (/speckit-plan); R5 is the run inventory
  quickstart.md            Phase 1 (/speckit-plan); the checks' commands in full
  qs.sh                    the check runner: bash qs.sh <check-id> [NAME=VALUE ...]; every verify calls it
  tasks.md                 Phase 2 (/speckit-tasks)
  traceability.md          delta scenario to test name (built during implementation, D4)
```

No `data-model.md` or `contracts/`: the parent case is the return pair of one
helper, fixed in `design.md` D1, and the one interface change is fixed text of
an existing command, fixed in D2. This mirrors feature 003's set.

### Source Code (repository root)

```text
project                    parent_case() and blocked_parent_sentence() above known_obstacles(); its parent fact
                           and docstring; the head check in new()'s bench branch
tests/test_project.py      one fixture block, two helpers, three rows, one rewritten test, 15 new tests [Q2]
README.md                  four texts of design.md D2
openspec/changes/refuse-non-directory-parent-early/tasks.md
                           [Q5] the 1.6, 2.1 and 2.2 ticks and the Speckit Handoff fields only (G1, G2)
.github/workflows/tests.yml
                           CI; unchanged (D6)
```

**Structure Decision**: one executable with one test module. The feature edits
only `project`, `tests/test_project.py`, `README.md` and `[Q5]` the change's
`tasks.md`, and adds files only under `specs/006-refuse-non-directory-parent-early/`.

## Other lanes and the landing order

- **PR #33 (feature 004, lane 2) lands first** by agent B's recommended order.
  This plan does not depend on its content: no 006 edit falls in
  `project:1-159` or at or below `discover()`, and no 006 test site is near
  #33's test hunks. When #33 is on main, the lead merges main into this branch
  at a phase boundary, never in the middle of a task:
  1. Re-run the merge check on the real commit, check `merge-check` with
     `HEAD33` the then-current #33 head (or `origin/main` once #33 is on it):
     for `project`, `README.md` and `tests/test_project.py`, `git merge-file -p`
     of this branch's file, the merge base's and that head's, each read with
     `git show` into a scratch directory; each must exit 0. So far only stand-ins were checked, on 2026-10-21: a D1
     prototype `project` and README against #33's heads `e256b59`, `1eb5afa`
     and `ab10102` (its head when last read, 14:52Z), all rc 0, and a
     stand-in tests file with a block at every planned test site, rc 0
     (research R9).
  2. `git fetch origin`, then `git merge origin/main` in this feature's
     worktree; never a rebase and never a force push (the org ruleset refuses
     force pushes).
  3. Re-read every line citation by function name (`project` moves about +37
     above `known_obstacles()`; tests +1 between `:25` and `:1033` and +16
     below `:1040`), and re-run Phases 4 and 5; the suite's count becomes the merge
     base's count `N0` plus 15 `[Q2]`, as check `suite` computes it.
  If 006 is ready first, it may land first: the cost is lane 2's four gates
  (below).
- **Lane 2's four gates** T009, T046, T128 and T131 of feature 004 read the
  fixed baseline `961c405` and fail once this realization's code is in their
  tree. Re-pointing their baseline to the merge base is lane 2's work; the lead
  tells lane 2 once, nothing more.
- **Lane 4 (#28's realization) lands after this one** and merges main in. This
  plan keeps its three pins: the name `parent_case()`, the README phrase "a
  parent that is a directory the person cannot write" exactly once, and no
  change to the harness signatures its new module composes (`setUp`, `run_cli`,
  `question_env`, `shape_env`, `run_pty`, `run_inproc`; its `design.md:268-275`
  and `proposal.md:280`) or to `:322-329`.

## Risks and Notes

- **Red runs wait** `[Q1]` `[Q3]`. At the base, the F3, F4, F6 runs and N6's
  wait at a prompt until `pty_timeout` (20 s, `:146`): 40 runs, plus the 2 of
  the rewritten test, about 14 minutes, beyond a 10-minute foreground command.
  The red-first record therefore runs in a scratch copy through a runner that
  sets `ProjectTests.pty_timeout = 5` for that process only (checked: a red F3
  run then fails in 5.4 s; the whole record takes about 4 minutes); the
  committed test keeps 20 s (research R6).
- **The host's openspec is outdated.** Use `/usr/bin/openspec` 1.6.0 or the
  openspec in py-bench, never the npm-global 1.2.0 first on the host PATH
  (feature 003's plan, Risks). Without network 1.6.0 prints a harmless
  telemetry error (an `AbortError` or a PostHog network error); the result
  line follows it.
- **The README sentence over-promises for an unsearchable directory.** Edit
  4's "a parent that is a directory the person cannot write still passes the
  dry run" is false when that directory also cannot be searched (mode 000):
  `destination.exists()` raises `[Errno 13]` before the question on 3.10 and
  3.12. Lane 4's ratified Decision 12 scopes it later ("can search but cannot
  write"); this feature keeps D2's text verbatim.
- **A FIFO opened by mistake would hang a run**; `run_cli` has `timeout=20`
  (`:144`) and `run_pty` its `pty_timeout`, so a wrong read fails, it does not
  hang the suite.
- **The socket rows** skip when `bind` raises `OSError` (a long `TMPDIR`); on
  the bench the bound path was 31 characters `[Q3]`.
- **The superuser** skips N15; CI runs as a normal user, and `py-bench` as uid
  1000.
- **Not tested, each with its reason** (none is asked by D3):
  - EC-004, a parent that becomes blocked after the head read: the backstop
    at `parent.mkdir` is unchanged code, and a test would need a race inside
    one process step.
  - FR-010's existing directory the person cannot write: D3 item 10 tests the
    missing child only; the generator's own error passes through unchanged
    code.
  - EC-008's other bullets: an unsearchable ancestor is refused at
    `destination.exists()` (`project:328`), before any of this feature's code;
    a read-only mount and a full disk fail late at unchanged code, and cannot
    be built in a temporary tree.
  - EC-009, a symbolic-link loop: lane 4's change; unchanged here.
  - FR-003's "a positional parent together with `--into`" with a blocked
    parent: refused at `:320-321`, before the parent is read (pinned with a
    directory by `test_pty_refusals_before_a_path_come_first`; with a blocked
    parent only under `[Q4]` C); and "an existing destination", which cannot
    co-occur with a blocked parent (`FILE/MyApp` cannot exist).
  - An asked `--workflow` with a blocked parent: refused before the question
    by unchanged code (`:336-337`), pinned for a directory parent by
    `test_pty_workflow_prerequisite_is_refused_before_the_question`.
  - The registry half of US1 scenario 6, FR-003 and EC-006 `[Q4]`: a malformed
    generator registry (a `config/bench-config.json` that is not valid JSON,
    which `registry()` (`project:130`) rejects through `bench_registry()`
    (`:100-101`) and `read_json()` (`:27-34`)) ordered after the head refusal.
    Q4 B pins the lookup half only (R-9.8: a `--workbenches` directory without
    `config/bench-config.json`, which `workbenches()` refuses, `:83-96`); a
    head check placed between `workbenches()` and `registry()` would pass every
    Q4 B run. Untested under Q4 B; tested under Q4 C (research R5's R-9.10, a
    fourth red run in N12; appendix Q4 C).
  - FR-002's read order and its "local, nothing opened, no permission, no
    network" properties: no run can observe them directly; V5's `ast` check
    asserts that `parent_case()` calls only `is_dir()` and `exists()`, and
    `blocked_parents()`'s FIFO row would hang a read that opened it.
  - SC-011, workBenches users after their pin moves: outside this
    repository; the lane's D5 comment reports the pin target.

## Complexity Tracking

None. There is no constitution gate, so there is nothing to justify.

## Appendix: Options not taken

Each entry lists only what changes in this plan; everything else stands.
Counts are research R7's, which include this plan's three runs.
Combined answers add up: Q1 and Q3 change the matrix runs of N1 to N5 (research
R7's table), Q2 the runs of N7 and N8 and the method count, Q4 the runs of N12
and N13. A short answer ("Another breadth", "Another way", "Another place"):
re-derive the affected rows of research R5 and the counts by the same rules;
nothing else changes.

### Q1 (test breadth of the head refusal)

- **A (D3's matrix exactly).** The givens per form shrink: N1 keeps K1 to K12
  (24 runs); N2 keeps K1 only (1); N3 keeps K1 and K5 (2); N4 keeps K1 only
  (1); N5 keeps K1 and R-3.1 (2). Items 2 and 3 fall from 72 to 29 runs; new
  runs 58; the method list and the suite's `N0 + 15` stay. The builder still builds
  every given (N1 uses them). Red-first: the runs that wait at the base fall to
  10 (N3 2, N4 1, N5 1, N6 4, the rewritten test 2), about 3.5 minutes at 20 s
  and about 1 minute with the 5 s runner. The coverage map is unchanged.
- **C (full cross product).** The builder adds every case (a) kind by every
  route it can take (`FILE/` has no `~/projects` form), the case (b) kinds by
  `--into`; `[Q3]` kinds stay `--into` only. 20 givens; items 2 and 3 grow to
  120 runs; new runs 149. Each pty method holds 20 or 21 runs (about 2 minutes
  each in the red-first record). Methods and count stay.

### Q2 (proving `FILE` intact for the case (b) rows)

- **B (widen the guard).** N7 and N8 are dropped (13 new methods; the suite
  goes to **`N0 + 13`**; 109 at `d47e8a4`). In `test_pty_triad_answer_with_an_obstacle_refuses`
  (`:1439`) and `test_inproc_triad_obstacle_runs_nothing` (`:1460`), the guard
  becomes true also for a missing parent whose nearest existing path is not a
  directory, and the check reads that path (`assert_parent_file_unchanged` on
  it). Three existing tests then change, not one: the Constraints' "one
  existing test is rewritten" (N3, AC5) no longer holds to the letter, and the
  spec's FR-014 sentence on A1 and its "Every existing test ... except one"
  must be re-worded at clarify time. The tests `ast` check adds the two to its
  allowed set, each allowed to change its guard line only. New runs 97. T5
  disappears; T2 also edits the two guards (it stays `[S]`, as every slice
  but I1 does: finding the nearest existing path is logic, not pattern
  copying).

### Q3 (the optional kinds)

- **B (`/dev/null` only).** K8 goes from the builder; 6 runs fewer (items 2 and
  3: 66; new runs 95). Drop the socket risk note and the builder's local
  `socket` import.
- **C (neither).** K8 and K9 go; 12 runs fewer (60; new runs 89). EC-001's
  statement for those kinds stays proven by the prototype only (research R1),
  not by a test.

### Q4 (faults the order tests pin)

- **A (D3 item 9 as it stands).** N12 loses R-9.8 and N13 loses R-9.7;
  `FAMILY_NOT_A_FOLDER_NAME` is not added; `red-first`'s count for N12 becomes 2
  (the quickstart's `RED` table, tagged `[Q4]`). New runs 99. The workBenches
  lookup (FR-003, US1 scenario 6, report A2) then has no test of its own: a
  head check between `workbenches()` and `choose()` would pass every run
  (clarify Q4). The registry half of US1 scenario 6 stays untested, as under
  B.
- **C (B plus five faults).** N13 adds a positional parent with `--into`
  (`PARENT_AND_INTO`, `:79`) and `--visibility private`, `--family Products`,
  `--elected-by alice` without `--shape` (`ORG_NEEDS_SHAPE`); N12 adds R-9.10,
  a malformed `bench-config.json` (not valid JSON) with `--type test --yes`,
  which gets the head refusal: the registry half of US1 scenario 6, FR-003 and
  EC-006, red at the base, so N12 is red in 4 subtests and `red-first`'s count
  for N12 becomes 4. New runs 106 (research R5's R-9.9 to R-9.13). The "Not
  tested" entries for the registry half and for a positional parent with
  `--into` go.

### Q5 (where the governance ticks go)

- **B (a separate governance PR).** Phase 0, G2 and FS-G leave this plan: the
  lead opens a governance PR to main with G1's six replacements before
  `/opsx:apply` (its `git diff HEAD~1` checks read against that PR's own
  commit), and this branch merges main in afterwards; 2.2 is ticked there or at
  the archive, with its "Met:" line. Nothing under `openspec/` changes on this
  branch, so the quickstart's "Files changed" list and its ASCII check drop
  the change's `tasks.md`, and FR-016 stands as written.
- **Short answer.** Whatever place is named replaces Phase 0 and G2; the
  "Files changed" list follows it.
