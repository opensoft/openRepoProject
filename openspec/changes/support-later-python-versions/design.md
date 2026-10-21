Lane: openRepoProject-4

# Design

## Context

See `proposal.md` for why and what, and `specs/project-command/spec.md` for the
requirements this design builds: three ADDED, "Supported Python versions are
stated and tested", "A parent that is a symbolic-link loop is refused before
the question" and "A destination that cannot be read is refused before the
question", and two MODIFIED, written against #21's delta at `8f3ca2d`, each
changing only the statements this change makes false. The council's noted
constraints are N1 to N12 in `clarifications.md`, each answered below: N1 D1,
N2 D4, N3 D1 and D10, N4 D6, N5 D6, N6 D2, N7 D2, N8 D2, N9 D2 and D10, N10
D5, N11 D7, N12 D5 and D10.

The design follows every recommendation in the proposal's "Decisions for
Brett Heap" (R1, C1, H1, P1, the 3.10 floor, L1 and Q1, U1, T2 and E1, M1,
`fail-fast` unchanged, and Decision 12's MODIFIED route). Brett Heap ratified
it on 2026-10-21 with every recommendation taken, Decision 12 as recommended
and Decision 3, which had none, as A1; "Open Questions" says what each
alternative would have changed.

What in `project` shapes the approach (unchanged on this branch from
`961c405` to main `e9d6711`):

- `new()` checks the name (`project:317-319`) and a positional parent given
  with `--into` (`:320-321`), then resolves the parent in one expression
  (`:322`), through `projects_dirs()` (`:77-80`) when neither `--into` nor the
  positional parent is given. It checks the family (`:323-324`), builds the
  destination (`:325-327`; `PARENT/FAMILY/NAME` with `--shape --family`
  unless the parent's own folder name is the family), and refuses an
  existing destination with `destination.exists() or
  destination.is_symlink()` (`:328-329`). Only then does it decide whether
  to ask (`:331-334`), make the hoisted `--workflow` check (`:336-337`) and
  read `known_obstacles()` (`:339`).
- `main()` prints every `Refused` and `OSError` as `REFUSED: ...` and returns
  2 (`project:1143-1148`); an `OSError` with a filename prints as `[Errno N]
  TEXT: 'FILENAME'`. A `RuntimeError` is not caught: a traceback, exit 1.
- The import block (`project:9-20`) has no `errno`.
- #21's realization, which lands first, adds `parent_case()` and its head
  refusal at the bench branch (`project:383-385`) and changes
  `known_obstacles()` (`project:235-254`); it does not touch `:322-329`.
- Tests: `ProjectTests.setUp` (`tests/test_project.py:116-136`) makes a
  resolved `self.base` (`:120`), a fake workBenches with the generator
  `test`, and `self.env` with `HOME` at `base/home` and `PROJECTS_DIR` at
  `base`. `run_cli(*args, cwd=None)` (`:141-144`) runs `project` with
  `self.env`, standard input not a terminal; `question_env()` and
  `shape_env()` (`:154-208`) build a question or shape environment;
  `run_pty()` (`:210`) runs at a pseudo-terminal; `run_inproc()` (`:324`)
  calls `main()` in process.
- CI: `.github/workflows/tests.yml:6-17`, the `test` job, with `python:
  ['3.10', '3.12']` (`:9`), `runs-on: ubuntu-latest` (`:10`) since #32, and
  `python -m unittest discover -s tests -v` (`:17`).

## Goals / Non-Goals

**Goals:**

- The README claims only the Python versions CI runs, and a test keeps the
  two equal.
- A looped parent gets one answer on every supported version: the system's
  `ELOOP` refusal, exit 2, naming the parent as given.
- A destination that cannot be read gets today's 3.10 to 3.13 refusal on
  every supported version, naming the destination.
- No new string in `project`; S1 and S2 read errnos from the operating
  system, which do not move with the interpreter.

**Non-Goals:**

- Raising the floor (R4), a pre-release job (P2, P3), a scheduled release
  check (A2), `fail-fast` or any other key outside the `test` job's matrix.
- A macOS or Windows job (#32).
- Changing `projects_dirs()`, `known_obstacles()`, `parent_case()`, the
  question, the shape branch, `choose()`, `parent.mkdir`, `main()`, or
  anything from `discover` (`project:433`) down.
- Any new flag, environment variable, configuration file or sentence.

## Decisions

### D1. The supported range, the README and CI

The range is CPython 3.10 to 3.15 (R1), closed (C1), and stated as the first
ADDED requirement (H1). The floor stays 3.10 (Decision 5), so `AGENTS.md:19`
("Python 3.10+") keeps stating the floor. It is agent-facing, AC6 does not
read it, and it is edited only if Brett Heap asks, then to "Python 3.10 to
3.15" (N3).

`.github/workflows/tests.yml`, line 9 only:

```
        python: ['3.10', '3.11', '3.12', '3.13', '3.14', '3.15']
```

Each entry stays a quoted string: unquoted, YAML reads `3.10` as the number
3.1. `runs-on: ubuntu-latest`, the steps, the strategy keys and every other
job are unchanged; no `os` axis returns.

`README.md`, each replacement exact, the rest of its paragraph unchanged and
rewrapped to the README's line width:

- Install, lines 17-18: "Python 3.10+ is required." becomes

  ```
  Python 3.10 to 3.15 is supported; CI tests each of those versions on Linux, and later versions are untested.
  ```

  "Supported" is defined by the same sentence: each listed version is run by
  CI. No end-of-life wording is added (N1). Feature 004 adds a Git 2.36
  sentence to the same paragraph; the merged paragraph keeps the Python
  sentence first, then Git's (D7).
- Development, lines 281-282: "CI covers Linux only." becomes

  ```
  CI covers Linux only, on Python 3.10 to 3.15.
  ```

A later minor version joins at its final release by one pull request that
changes line 9 and both README sentences together. AC6's test fails if any
of the three disagrees. Who opens that pull request was Decision 3; Brett Heap
chose A1 on 2026-10-21: an issue and the pull request at each final release,
opened by the lane that owns `project` at the time.

### D2. S1: the looped parent

At `project:322`, in place of the one expression:

```python
    source = Path(args.into or args.parent or os.environ.get("PROJECTS_DIR")
                  or Path.home() / "projects").expanduser()
    looped = False
    try:
        parent = source.resolve()
    except RuntimeError:  # 3.10 to 3.12: a symbolic-link loop (design D2)
        looped = True
    else:
        try:
            os.stat(parent)
        except OSError as exc:
            looped = exc.errno == errno.ELOOP
```

and, right after the family check (`project:323-324`):

```python
    if looped:
        raise OSError(errno.ELOOP, os.strerror(errno.ELOOP), str(source.absolute()))
```

- **One source (N6).** `source` is the only expression that chooses the
  parent; the unresolved PARENT and the resolved parent both come from it.
  It equals today's choice: `projects_dirs()` returns
  `Path(PROJECTS_DIR).expanduser().resolve()` when `PROJECTS_DIR` is
  non-empty and `Path.home() / "projects"` otherwise, and the old expression
  resolved either again. `projects_dirs()` is not edited, and its other
  callers (`workbenches()`, `project:90`, and everything from `discover`
  down) keep it. AC2's `PROJECTS_DIR` and default `~/projects` rows guard the
  equivalence.
- **The mapping's reach (N9).** `expanduser()` and `Path.home()` run outside
  the `try`, so an unknown `~user` still ends in its own `RuntimeError`
  traceback, as today on every version (D10). Only `resolve()` is mapped.
- **The read (N8).** (L) is exactly "non-strict `resolve()` raised
  `RuntimeError`, or `os.stat()` of the resolved parent failed with
  `ELOOP`". Every other outcome of that `os.stat()` (success, `ENOENT`,
  `ENOTDIR`, `EACCES`, `ENAMETOOLONG`) passes to S2 unchanged. `LOOP/..`
  resolves to an existing directory and keeps its answer; `LOOP/sub/..` is
  (L). The 45-link chain with no cycle is not (L) on any version (council).
- **PARENT (N7).** `source.absolute()` joins the working directory as
  `os.getcwd()` reports it, the physical path, not `$PWD`, and keeps `..`
  and links. It is computed only when (L) is raised, so no other path pays
  for it, and it is the same string on every version and route.
- **The place.** After the family check (Q1), so `--shape --family 1bad`
  with a looped parent is refused for the family on every version, as on
  3.13 and later today. Before S2, the question and every path.
- **The errno.** `errno.ELOOP` and `os.strerror()` give the system's number
  and text (40 on Linux). `main()`'s existing handler prints it.

Rejected: `resolve(strict=True)` (T1: two resolutions and more errnos for one
result), a `sys.version_info` gate (T3), a pathlib walk (T4), and catching
`RuntimeError` around the whole expression (N9).

### D3. S2: the destination read

At `project:328-329`, in place of `destination.exists() or
destination.is_symlink()`:

```python
    # S2 (design D3): absent is what 3.10-3.13 pathlib ignored; any other error propagates.
    try:
        os.lstat(destination)
    except OSError as exc:
        if exc.errno not in (errno.ENOENT, errno.ENOTDIR, errno.EBADF, errno.ELOOP):
            raise
    else:
        raise Refused(f"Destination already exists: {destination}")
```

- **Absent.** `ENOENT`, `ENOTDIR`, `EBADF` and `ELOOP`: the errnos pathlib
  on 3.10 to 3.13 ignores in `exists()` and `is_symlink()`. `ELOOP` matters:
  with `--shape --family Fam` and `PARENT/Fam` a loop, every version plans
  today (exit 0); reading only `ENOENT` and `ENOTDIR` (E3) refused it with
  `[Errno 40]` in the feasibility runs.
- **Unreadable.** Any other `OSError` propagates to `main()`, which prints
  `REFUSED: [Errno N] TEXT: 'DESTINATION'`, byte for byte the 3.10 to 3.13
  line: `os.lstat()` given a `Path` raises with a `str` filename (council).
  The measured sources are `EACCES`, beneath a directory the person cannot
  search (a parent beneath one, existing or not, or a parent that is one),
  and `ENAMETOOLONG`, for any component longer than the name limit (a parent
  component, NAME, or the `--family` folder; neither name pattern caps the
  length, `project:318`, `:323`) or a whole path longer than the path limit.
- **DESTINATION.** The destination built on the resolved parent, as the
  existing-destination refusal names it. Under a linked prefix (L) and (U)
  therefore name different prefixes: (L) the parent as given, (U) the
  resolved destination (council cases J and I). Both are true.
- **One deviation.** A destination that is itself a symbolic link into a
  directory the person cannot search: `lstat` succeeds, so it is refused as
  existing (3.14's answer), where 3.10 to 3.13 gave `[Errno 13]`. E2, two
  reads (`os.stat()` then `os.lstat()`), would keep the 3.10 to 3.13 answer
  exactly; it stays the acceptable alternative.
- **The place.** Where the check is today, after S1's raise, so the order of
  every refusal around it is unchanged.

### D4. Fixed text

All text is ASCII. `project` gains no string: both lines come from the
system through `OSError`. On Linux:

```
REFUSED: [Errno 40] Too many levels of symbolic links: 'PARENT'
REFUSED: [Errno 13] Permission denied: 'DESTINATION'
REFUSED: [Errno 36] File name too long: 'DESTINATION'
```

The tests build each from `errno` and `os.strerror()` (D5), never from these
numbers.

L2, carried for Decision 6 (N2): if Brett Heap chooses it, S1 raises
`Refused("The parent PARENT is a symbolic link loop; choose a parent that is
a directory.")`, PARENT as given, and `main()` prints:

```
REFUSED: The parent PARENT is a symbolic link loop; choose a parent that is a directory.
```

AC2 then expects that line in place of the `ELOOP` line, and nothing else
changes.

`README.md`: the two sentences of D1. Under Decision 12, once #21's
realization has inserted its permission sentence after "Existing destinations
refuse." (`README.md:96`; #21's `design.md:187-191`), this realization
replaces, character for character, "a parent that is a directory the person
cannot write" in it with:

```
a parent that is a directory the person can search but cannot write
```

The ASCII check covers the changed strings and the added lines of `project`,
`README.md`, `.github/workflows/tests.yml` and the new test module, not the
whole of `project`, which already carries em dashes (archived N4).

### D5. Tests

One new module, `tests/test_parent_reads.py`, found by `python -m unittest
discover -s tests -v`; no new dependency (PyYAML is already in
`requirements.txt`). No line of `tests/test_project.py` changes (M1).

1. **The harness, by composition.** The module does `import test_project`
   and, in its own `setUp`, builds `harness = test_project.ProjectTests()`
   (the default method name), calls `harness.setUp()` and registers
   `self.addCleanup(harness.doCleanups)`. It uses `harness.base`,
   `harness.env`, `run_cli`, `question_env`, `shape_env` and `run_pty`. It
   never subclasses `ProjectTests` and never binds the class name in its own
   namespace, so discovery runs no existing test twice. AC1's "Ran N" is
   main's count plus this module's.
2. **Fixtures** under `harness.base`: `self_loop` (a link to itself),
   `loop_a` and `loop_b` (links to each other), `self_loop/sub`, `f/` with
   `f/loop` (a link to itself), `LINK` (a link to `f`), `CWDLINK` (a link to
   `f`), and `home/projects` as a looping link for the default route.
   Expected PARENT is the path as given, made absolute: for `LINK/loop`,
   `base/LINK/loop`. For the relative row, `run_cli("new", "MyApp", "--into",
   "loop", ..., cwd=base/CWDLINK)`, it is `base/f/loop`, the physical
   prefix (N7).
3. **(L) rows (AC2).** Each loop kind by `--into`; `self_loop` also by the
   positional parent, by `PROJECTS_DIR` and as the default (`PROJECTS_DIR`
   removed); `LINK/loop` by `--into` and by `PROJECTS_DIR`. Forms: `--type
   test --yes`; `--type test --dry-run`; `--shape --org example --visibility
   private`; not asked (`CI=true` at a pty, and `run_cli`'s non-terminal
   standard input); asked (`run_pty` with `question_env(None)`, no choosing
   flag). Each: exit 2; standard error ends with exactly
   `f"REFUSED: [Errno {errno.ELOOP}] {os.strerror(errno.ELOOP)}: '{parent}'"`;
   no `Create it as a Triad` line; no `Create:`; the `rglob` snapshot of
   `harness.base` unchanged (archived N2). `--shape --org example
   --visibility private --family 1bad` with `self_loop`: `Family must be a
   single folder name.`.
4. **(U) rows (AC3).** Permission fixtures: `d000/` and `d600/`, each with a
   `child/` directory made before the chmod. The rows: `d000/child`,
   `d600/child`, `d600/missing`, and `d600` and `d000` themselves, each by
   `--into`. A cleanup that restores mode 0o700 is registered before each
   chmod. Both snapshots are taken with modes restored. The skip probe (N10):
   a permission row is skipped only when `os.lstat()` of the existing
   `child` succeeds through the locked directory (root, capabilities, ACLs);
   on every CI job no (U) test is skipped, read from the `-v` output by the
   landing task. Length rows: a parent component of
   `os.pathconf(base, "PC_NAME_MAX") + 1` characters; a NAME of that length
   into `harness.base`; `--shape --org example --visibility private
   --family` of that length; and a parent of 200-character components longer
   than `os.pathconf(base, "PC_PATH_MAX")`, never created. Forms as in 3.
   Each: exit 2; standard error ends with exactly
   `f"REFUSED: [Errno {e}] {os.strerror(e)}: '{destination}'"`, where `e` is
   `errno.EACCES` or `errno.ENAMETOOLONG` and `destination` is the resolved
   parent joined with `MyApp`, or with the family and `MyApp`; no question
   line; no `Create:`; nothing changed.
5. **S2's success branch (AC4).** A destination `base/MyApp` that is a
   directory, a regular file, a dangling link, a link to itself, or a link
   into `d000/`: `REFUSED: Destination already exists: {base}/MyApp`, exit 2.
   With `shape_env("true")` as the run's environment (the fake openRepoShape
   on PATH), `--shape --org example --visibility private --family Fam
   --dry-run`, where `base/Fam` is a link to itself: the plan, exit 0.
6. **Unclassified parents (AC5).** A directory, a link to one, a missing
   path, a dangling link, a regular file, a link to a file, a FIFO and
   `FILE/sub`, each by `--into`, asked at a pty with `question_env(None)`:
   the creation question appears; input ends there. What follows the
   question is main's, #21's included, and main's own tests pin it.
7. **The range (AC6).** The test loads `.github/workflows/tests.yml` with
   `yaml.safe_load` and reads `jobs.test.strategy.matrix.python`. It asserts
   that every entry is a string, reads `README.md` with runs of whitespace
   collapsed, and matches the two sentences of D1 with the versions as
   groups. Then it asserts that both sentences name the same range, that the
   list equals every minor version from the lowest to the highest, in order
   and with no other, and that the lowest is `3.10`.
8. **Neutral construction (N12).** Every expected line is built from `errno`
   and `os.strerror()`, every length from `os.pathconf()`, and every path
   under the resolved `harness.base`, so the module stays correct if run on
   macOS, though no CI job runs it there.

### D6. The spec delta, #21 and the archive order

- **Against #21 (N4).** Both MODIFIED blocks are #21's delta text at
  `8f3ca2d` (byte-identical to its text at `1b84a94` and `a43e7d2`), lines
  129-198 and 5-88, with only the statements the proposal records as false
  changed. They were built by exact, asserted replacements, and a diff
  against #21's text shows those changes only. Every #21 citation in this
  change is to `8f3ca2d`; if #21's head moves before this change is
  ratified, the citations and the blocks are re-checked against the new
  head. On 2026-10-19 #21's head was `8f3ca2d` (`b8e9be5` merged main
  `e9d6711`, and `8f3ca2d` aligned its CI statements with Linux-only CI,
  #32): its delta is byte-identical to `1b84a94`'s, so both MODIFIED blocks
  stand, and the citations were re-pinned with no cited line moved.
- **Archive order (N5).** This change archives after
  `refuse-non-directory-parent-early`. openspec 1.13.1 validates the second
  block with only `[INFO] ... Archive would refuse this delta ... not found`,
  and the first block's requirement already exists in main, so the tool
  would let the first block archive alone and carry #21's text into main. A
  governance task (tasks.md 3.3) checks, before `/opsx:archive`, that
  `refuse-non-directory-parent-early` is under `openspec/changes/archive/`
  on main, that `openspec validate support-later-python-versions --strict`
  prints no "Archive would refuse" line, and that each MODIFIED block's base
  text equals main's requirement text then. A difference means #21 changed
  before archiving, and the block is rewritten against main.
- **Decision 12's alternative.** If lane 1 scopes #21's shape sentence and
  scenario, and its permission sentence, scenario and README sentence, in
  #21 before it is ratified, the second MODIFIED block and D4's README
  replacement drop. The first block, the ADDED requirements, `project` and
  the tests are unchanged. Not taken: Brett Heap took Decision 12's
  recommendation on 2026-10-21, so this change MODIFIES and scopes #21's
  statements, and nothing drops.

### D7. Shared files

- **`project`'s import block (N11).** Feature 004 adds `import errno` there,
  after `argparse` (`project:11-12` on `004-project-clean-all-safe` at
  `96a08d4`). The realization adds `import errno`, in the block's
  alphabetical place after `argparse`, only if main lacks it then. A
  three-way merge of the two is clean (council evidence 4).
- **`project` `new()`.** #21's realization lands first and edits other lines
  (`:235-254`, `:383-385`); this realization merges main in first and edits
  `:322-329` only.
- **`README.md:17-19`.** Shared with feature 004's Git 2.36 sentence; the
  second to merge keeps both sentences, Python's first.
- **`.github/workflows/tests.yml`.** This change edits line 9; feature 004
  appends its `git-floor` job. Whichever lands second merges main in. Lane 2
  agreed on 2026-10-19 (its ruling R-46) that the job's comment names no job
  count, so this change needs no edit on 004's account in either order.
- **`tests/test_project.py`.** Untouched here (M1).

No rebase and no force push: merges only.

### D8. The feature records

`specs/003-parent-obstacle-wording/` and the archived changes are not edited.
The new feature's `spec.md` carries this statement, in substance: "For a
looped parent and a destination that cannot be read, this feature supersedes
feature 003's EC-004 (spec.md:139-142), its plan's row and residual notes
(plan.md:124, :209-211 and :272) and its research note (research.md:79-81).
It also supersedes, for those cases, any statement of the feature that
realizes refuse-non-directory-parent-early that records the archived N1
residuals as behaving as today (that change's design D6), named by path once
that feature exists. Their other statements stay true." Its
`traceability.md` maps each ADDED scenario, and each changed MODIFIED
scenario, to its tests.

### D9. Handoffs after landing

No new issue on any repository. When the realization merges, this lane posts
one comment on workBenches#145 if that issue is still open, naming the merge
sha and the sha256 of `project` at that sha (from `git show <sha>:project |
sha256sum`) as an alternative pin target, as archived D5 and #21's D5 did. If
#145 is closed by then, nothing is posted, and the change reaches `onp` and
`new-project.sh` at the owner's next pin move. The release practice for each
later CPython version is Decision 3's, which Brett Heap chose as A1 on
2026-10-21: it needs no machinery here. A2, not chosen, would have been a
scheduled check in a later change with lane 2's assent.

### D10. What is explicitly not changed

- `projects_dirs()`, and so the residual of a looped `PROJECTS_DIR` with the
  parent given by `--into` on 3.10 to 3.12, which still ends in a
  `RuntimeError` traceback through `workbenches()` (`project:79`, `:90`) on
  the bench path when `WORKBENCHES_ROOT` and `--workbenches` are unset
  (proposal, Out of Scope).
- An unknown `~user` parent: `RuntimeError: Could not determine home
  directory.`, exit 1, on every version, raised by `expanduser()` outside
  S1's mapping (N9).
- `known_obstacles()`, `parent_case()` and #21's head refusal: a looped or
  unreadable parent never reaches them. The question, the shape branch,
  `choose()`, the `--workflow` checks, `parent.mkdir` and `main()`.
- `AGENTS.md:19` (N3); `fail-fast` (Decision 11); no pre-release job (P1).
- macOS: no job, by #32; the tests are written system-neutral (D5 item 8),
  and macOS stays untested by CI (N12).
- Everything from `discover` down, lane openRepoProject-2's surface.

## Risks / Trade-offs

- [Two `test` jobs become six; 12 job runs per pull-request push] ->
  Accepted: public repository, no paid minutes, no required check.
- [The 3.15 job builds PyYAML 6.0.3 from source until a `cp315` wheel exists]
  -> A build failure fails the job, not the code; the landing task cites the
  3.15 job's pip log.
- [(L) changes 3.10 to 3.12 from a traceback, exit 1, to a refusal, exit 2;
  (U) changes 3.14 and later from a plan, exit 0, to the 3.10 to 3.13
  refusal; S2's one deviation for a destination linked into an unsearchable
  directory] -> No caller relying on any of them is known; each is pinned by
  a test (D5).
- [A test outside this change's surface fails on an added version] -> It
  blocks the matrix until its owner (lane 1 or lane 2) fixes it; reported,
  not fixed here.
- [The archive tool would let the first MODIFIED block archive before #21]
  -> tasks.md 3.3 (D6).
- [A later pathlib moves again] -> S1 and S2 no longer depend on it;
  `known_obstacles()` still does, for parents whose answers agree today.
- [The floor's upstream support ends in October 2026] -> A separate decision
  (R4).

## Migration Plan

Nothing migrates for a parent that is neither looped nor unreadable: its
output, files and exit status are unchanged on every version. A looped parent
exits 2 instead of 1 on 3.10 to 3.12; an unreadable destination exits 2
instead of 0 on 3.14 and later.

1. Ratification by Brett Heap's word ratifying #28, given on 2026-10-21
   (Decision 12's recommendation is taken, so the second MODIFIED block
   stays).
2. #21 ratified and its realization landed; this realization merges main in
   after it.
3. `/speckit.specify`, from a local main synced to origin, creates the one
   feature under the next free number; it is recorded once in `tasks.md`
   under "Speckit Handoff", and `/opsx:apply` runs only then.
4. The realization PR merges with green checks on the six `test` jobs and
   every other job on main then, and closes issue #22.
5. The workBenches#145 comment of D9, if that issue is still open.
6. The change is archived after `refuse-non-directory-parent-early` is
   archived and after 4 and 5 (tasks.md 3.3).

Rollback: revert the realization commit on main. Installed `project` artifacts
follow workBenches' pin, so a revert reaches nobody until the pin moves.

## Open Questions

None remains. None changed what `project` or the tests do, and the two
decisions that stayed with Brett Heap are answered (ratified on 2026-10-21,
"ratify 28, recommended for SA-2 and SA-7"):

- Decision 3 (SA-7), who adds each new release: A1 is chosen, "A1: PR per
  release (Recommended)" (2026-10-21T12:05:15Z); A2 is not chosen. Either is a
  practice after landing (D9); neither changes this change's artifacts.
- Decision 12 (SA-2), whether this change scopes #21's statements or lane 1
  does: the recommendation is taken, and this change scopes them. The
  alternative, not taken, would have dropped the second MODIFIED block and
  D4's README replacement only (D6); nothing drops.

He took the recommendation on each of the decisions the alternatives below
belong to, so none of them applies; the change under each would have been: L2,
D4's sentence in AC2; H2, the first ADDED requirement drops and AC6's test
stays as a README-to-CI check; E2, two reads at S2 and no deviation; R2, three
versions in line 9 and the README.
