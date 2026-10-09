Lane: openRepoProject-1

# Design

## Context

See `proposal.md` for why and what, and `specs/project-command/spec.md` for the
requirement this design builds. The council's noted constraints are N1 to N6
in `clarifications.md`, each answered below: N1 D1 and D6, N2 D3, N3 D1, N4
D2, N5 D1 and D6, N6 D1.

What in `project` shapes the approach (unchanged on this branch from main
`7a9134b`):

- `known_obstacles()` (`project:235-247`) returns the obstacle sentences in
  the order name, openRepoShape, parent. Its third read is `parent.is_dir()`
  (`project:244`), and its docstring says "three local reads".
- `new()` resolves the parent once (`project:315`), refuses an existing
  destination (`project:321`), and, when the question is offered, computes the
  obstacles once (`project:332`). That one list feeds the question's lines
  (`print_creation_question()`, `project:333`) and the composed refusal on a
  Triad answer (`project:338-339`). `main()` prints every `Refused` and
  `OSError` as `REFUSED: ...` and returns 2 (`project:1136-1141`).
- Downstream, the shape branch refuses a parent that is not a directory
  (`project:364-365`), and the bench path returns on `--dry-run`
  (`project:387-388`) before `parent.mkdir()` (`project:391`).
- Tests: the D13 fixtures (`tests/test_project.py:28-56`, ending at
  `# End D13 fixtures.`), `known_obstacle_cases()` (`:388-397`), the parent
  tests (`:1347-1437`), the in-process test (`:1381-1399`). `self.base` is
  already resolved (`:114`). CI runs `ubuntu-latest` and `macos-latest` on
  Python 3.10 and 3.12 (`.github/workflows/tests.yml:8-10`).

## Goals / Non-Goals

**Goals:**

- Each parent sentence is true of the path it names.
- A missing parent prints byte for byte what it prints today.
- The facts stay three, read once, with no network and no subprocess.
- The new string is fixed here (D2) and pinned in the tests as a fixture.

**Non-Goals:**

- Changing `ask()`, `confirm()`, `choose()`, `execute()`,
  `print_creation_question()`, the composed refusal's shape, the openRepoShape
  argv, `main()`'s handlers, or any subcommand other than `new`.
- Any new flag, environment variable or configuration file.
- Any YAML read, network access, subprocess or import on the obstacle read.
- Changing the shape branch's refusal or the bench path's refusals (D6).
- No stat-by-errno rewrite, no third sentence, no CI change (N5).

## Decisions

### D1. The discriminator: `is_dir()`, then `exists()` on the same path

The third read stays `parent.is_dir()` on the resolved parent. Only when it is
false, `parent.exists()` on the same `parent` chooses the sentence: false
gives the missing sentence, true gives the new one (D2). This restates
archived D3 item 3 as: "3. whether the parent is an existing directory, read
as `parent.is_dir()` for the resolved parent (`--into`, the positional parent,
or `projects_dirs()[0]`, which is `PROJECTS_DIR` or `~/projects`) and, only
when that is false, as `parent.exists()` on the same path, which chooses the
parent sentence." The facts stay three; the order stays name, openRepoShape,
parent. The docstring says "three local facts" in place of "three local
reads" and names this design for the second parent sentence.

`known_obstacles()` is still called once, and the refusal is still composed
from that list (N3, N6), so the question line and the refusal cannot diverge
and the refusal never reads the parent again. A parent repaired in another
terminal while the question waits is refused with the sentence the question
printed until a rerun, as today.

No exception handling is added. `exists()` has the same error handling as
`is_dir()` on every version (N3), and a parent that the two reads could not
stat on the CI versions is refused earlier, at `destination.exists()`
(`project:321`). All 94 existing tests pass with this read (Python 3.12.3).

| Parent given as | 3.10 and 3.12 (CI) | Later versions (residual) |
| --- | --- | --- |
| a missing path | missing sentence | same |
| a dangling symbolic link | missing sentence, naming the target | same |
| a regular file, `FILE/`, a symbolic link to a file, a FIFO | new sentence, naming the file (a link by its target) | same |
| a symbolic link to a directory | no parent obstacle | same |
| `FILE/sub` | missing sentence (D6, dead end) | same |
| a symbolic-link loop | `RuntimeError` traceback at `resolve()`, before the question | 3.13 and later: missing sentence (D6) |
| a directory beneath an unsearchable ancestor | `REFUSED: [Errno 13] ...` at `destination.exists()`, exit 2, before the question | 3.14: missing sentence for a directory that exists (D6) |

The council verified the 3.10 and 3.12 column (N1). For this design the 3.12
column was probed again on Python 3.12.3 in `py-bench` with `project` at
`7a9134b`, and every row held: `is_dir()` and `exists()` read False and False
for the missing, dangling and `FILE/sub` rows, and False and True for the
file, `FILE/`, link-to-file and FIFO rows. The later column is the council's
record, not run here.

Rejected alternatives:

- A raw `os.stat` classified by errno: rejected by the lead for this change
  (N5). It would add behaviour, strings and a third case beyond a wording
  follow-up.
- Adding `is_symlink()` to the discriminator (N1): a loop is not one of the
  two cases, and the residual is on a version CI does not run.

### D2. Fixed text

All text is ASCII. `PARENT` is substituted with the resolved parent, as today;
every other character is literal. The parent's line under entry 1, with
exactly one of the two present:

```
     Not possible here: The parent directory PARENT does not exist; a Triad is created inside an existing directory.
     Not possible here: The parent PARENT exists but is not a directory; choose a parent that is a directory.
```

- The missing sentence is archived D13's, unchanged: `The parent directory
  PARENT does not exist; a Triad is created inside an existing directory.`
- The new sentence: `The parent PARENT exists but is not a directory; choose a
  parent that is a directory.` Its clause after the semicolon is deliberately
  not Triad-specific: nothing can be created inside such a parent on either
  path.

The composed refusal keeps archived D13's shape: `A Triad cannot be created
here. `, the obstacle sentences in order joined by single spaces, then
` Nothing was created.` For `my-app`, no `openRepoShape` and a file parent,
`main()` prints on stderr:

```
REFUSED: A Triad cannot be created here. my-app cannot be a Triad name; a Triad name is a letter first, then letters and digits only, such as MyApp. openRepoShape is not on PATH. Install openRepoShape through workBenches first. The parent PARENT exists but is not a directory; choose a parent that is a directory. Nothing was created.
```

`README.md` line 60: the clause "or a parent directory that does not exist."
is replaced, character for character, by the text below; the rest of that
paragraph is unchanged, rewrapped to the README's line width:

```
or a parent that is missing or is not a directory. A single-repository answer creates a missing parent; a parent that exists but is not a directory blocks both answers, so choose another parent.
```

The ASCII check (N4) covers the changed strings and the added lines of
`project`, `tests/test_project.py` and `README.md`, not the whole of
`project`, which already carries em dashes at lines 197, 908, 921 and 1129.

### D3. Tests

All in `tests/test_project.py`; no new dependency. Every existing row and
assertion stays as it is, and `OBSTACLE_PARENT` stays, since the missing
sentence is unchanged.

- **The fixture**: one new literal, `OBSTACLE_PARENT_NOT_A_DIRECTORY`, the
  new line of D2 with `{PARENT}` as its format field, placed after the
  `# End D13 fixtures.` marker under its own header naming this design (D2),
  so the D13 block stays a verbatim copy of the archived design.
- **`known_obstacle_cases()`** creates its own fixtures under `self.base`: a
  regular file with known content, a symbolic link to it, and a dangling
  symbolic link. It gains four rows, the existing four unchanged, each by
  `--into`: the file; the link to the file; the dangling link; and `my-app`
  with no `openRepoShape` and the file, the parent sentence last. The
  expected PARENT is `self.base / "<file>"`, the resolved path, for the file
  row and the link row alike, and the dangling link's resolved target, with
  `OBSTACLE_PARENT`, for its row. So the pty refusal test and
  `test_inproc_triad_obstacle_runs_nothing` (no `execute`, subprocess or
  socket) run each new row: the question line, the composed refusal, exit 2,
  no organization prompt, no openRepoShape record.
- **Nothing created** (N2): for each row whose parent exists and is not a
  directory, the test also asserts that `sorted(self.base.rglob("*"))` is the
  same after the run as before it, and that the file is still a regular file
  with its content. How a row is recognised is the realization's choice,
  provided no existing row's tuple changes.
- **The routes**: `test_pty_missing_parent_is_named_without_into` gains a
  second table, after its first, for the file as parent given by `--into`, by
  the positional parent, by `PROJECTS_DIR`, and as the default `~/projects`
  (a regular file at `HOME/projects`, with `PROJECTS_DIR` removed). Each
  expects the new line naming the resolved file, no question line containing
  `--into`, and the file unchanged.
- **The dry run**: `test_pty_dry_run_with_an_obstacle_refuses` gains rows for
  the file, the link to the file and the dangling link, each by `--into`; its
  existing assertions, the `rglob` snapshot included, apply to them as they
  stand.
- **The single-repository answer**: a new pty test answers `2` and `yes` with
  the file as `--into` and `CI` unset, and runs the baseline, the same name
  and parent with `--type test` (not asked), answering `yes`. Both exit with
  the same status, which today is 2; stdout from `Create:` on is the same; the
  `REFUSED:` line is the same (today `[Errno 17] File exists`); no `warning:`
  line appears in the asked run, and the comparison leaves the advisory out.
  `test_pty_single_answer_is_unaffected_by_obstacles` keeps its row.
- **A symbolic link to a directory**: a new pty test gives one as `--into`
  with an assembly-form name and the fake on PATH, takes the Triad and ends
  input at the organization prompt, as `test_pty_no_known_obstacle_names_none`
  does: the question names no obstacle.

### D4. Feature 002's record

`specs/002-triad-first-project-new/` is not edited. The new feature's
`spec.md` carries this statement, in substance: "For the parent fact, this
feature supersedes feature 002's FR-012 'whether the parent directory exists'
and 'the missing parent directory' (spec.md:367 and :370-371) with two cases:
a parent that does not exist, named with the unchanged sentence, and a parent
that exists but is not a directory, named with the new one. Feature 002's
other statements of the parent fact (spec.md:130-132, :140, :151-154, :156
and :459-460, quickstart.md:118, traceability.md:37, tasks.md:137 and :143)
describe the missing case and stay true of it." Its `traceability.md` maps
"The parent directory is missing", whose title is unchanged so feature 002's
`traceability.md:37` still points at it, and "The parent exists but is not a
directory" to their tests.

### D5. Handoffs after landing

No new issue on any repository. When the realization merges, this lane posts
one comment on workBenches#145 if that issue is still open, naming the
realization's merge sha and the sha256 of `project` at that sha (from
`git show <sha>:project | sha256sum`) as an alternative pin target that
carries the corrected sentence. If #145 is closed by then, nothing is posted;
the sentence reaches `onp` and `new-project.sh` at the owner's next pin move.

### D6. What is explicitly not changed

- The shape branch's refusal, "Shape creation requires an existing --into
  parent directory." (`project:364-365`), reached only with `--shape` by flag.
- The bench path for a parent that exists and is not a directory, a known
  limitation: it shows the plan, asks for `yes`, and only then refuses
  (`[Errno 17] File exists`, exit 2), and its dry run exits 0 (both observed
  on 3.12.3). An earlier refusal is its own change, on Brett Heap's word.
- Residual dead ends: `FILE/sub`, whose sentence is true while the repair it
  suggests fails with `Not a directory`, and the symbolic-link loop on 3.13
  and later. The 3.14 unsearchable ancestor is a residual too.
- The CI matrix and the README's "Python 3.10+".

## Risks / Trade-offs

- [A single-repository answer with a file parent fails after `yes`] -> Known
  limitation (D6); the README's new sentence says such a parent blocks both
  answers.
- [Later Python versions print the missing sentence for a loop or an
  unsearchable ancestor] -> Residuals on versions CI does not run (D1, D6).
- [`FILE/sub` suggests a repair that fails] -> Accepted gap; the sentence is
  true of the path.
- [PR #11's feature edits `project` and `tests/test_project.py` too] ->
  Whichever merges second merges main in; no rebase, no force push.

## Migration Plan

Nothing migrates: a missing parent prints exactly today's text, and no flag,
stream or exit status changes.

1. Ratification by Brett Heap's word on PR #15.
2. `/speckit.specify`, from a main synced to origin, creates the one feature
   under the next free number; it is recorded once in `tasks.md` under
   "Speckit Handoff", and `/opsx:apply` runs only then.
3. The realization PR merges with green checks on all four CI jobs and closes
   issue #14.
4. The workBenches#145 comment of D5, if that issue is still open.
5. The change is archived after the merge.

Rollback: revert the realization commit on main. Installed `project` artifacts
follow workBenches' pin, so a revert reaches nobody until the pin moves.

## Open Questions

None changes what is built. The lead's decisions are taken: the new sentence
(D2), the dropped scenario for the late single-repository refusal (D6), the
pathlib read (D1), and the feature number taken at creation (Migration Plan).
