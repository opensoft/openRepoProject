Lane: openRepoProject-4

# Proposal: support-later-python-versions

Status: ratified by Brett Heap on 2026-10-21 (10:40:31Z), in lane 4's session,
in his words "ratify 28, recommended for SA-2 and SA-7", quoted on PR #28 at
https://github.com/opensoft/openRepoProject/pull/28#issuecomment-6315794017.
Decision 3 (SA-7), which had no recommendation, he answered when asked, at
12:05:15Z the same day, by choosing "A1: PR per release (Recommended)";
Decision 12 (SA-2) takes its recommendation, and Decisions 1, 2 and 4 to 11
take theirs (Decisions for Brett Heap, below). The alignment review and the
council are applied (Review resolution, at the end); main is merged in at
`e9d6711`, so CI is Linux only (#32), and #21 is cited at its head
`8f3ca2d`; #21 has since landed on main as `b233333`, whose change directory
is identical to `8f3ca2d`, the commit cited; `clarifications.md`, the spec
delta, `design.md` and `tasks.md` complete the proposal stage. Governing
issue: opensoft/openRepoProject#22, claimed by lane openRepoProject-4. Taken
up under Brett Heap's word of 2026-10-11 (about 15:55Z), "usage reset, resume
all. read handoff and resume and fan out wide and do as much as possible in
parallel", which named no item; lanes openRepoProject-4 and -5 split the open
candidates and this one fell to lane 4 (issue #22, Authority). That word is
given, and PR #28 lands by squash (tasks.md 1.6).

Source: the archived change
`openspec/changes/archive/2026-10-09-fix-parent-obstacle-wording/` recorded
two later-Python residuals in its constraint N1 (`clarifications.md:16-35`)
and in its design's version table and D6 (`design.md:78-93`, `:222-224`), and
kept the CI matrix and the README's "Python 3.10+" out of that change (N5,
`clarifications.md:82-94`; D6, `design.md:225`), "the residual is on a version
CI does not run" (`design.md:100-101`). Issue #20 and its proposal PR #21
(lane openRepoProject-1, head `8f3ca2d`) put both residuals and the CI matrix
out of scope too (that proposal's Out of Scope, lines 412-416). This change is
where they go.

## Why

`README.md:17-18` says "Python 3.10+ is required", and `AGENTS.md:19` says the
same. CI (`.github/workflows/tests.yml:6-17`) runs the suite on
`ubuntu-latest` only (`:10`; #32, by Brett Heap's decision of 2026-10-15)
with Python 3.10 and 3.12 only (`:9`). So 3.11, 3.13, 3.14 and 3.15 are
claimed and never run; 3.15.0 is released (setup-python's version manifest
lists it as stable; Observed).

Some parents of `project new` change their answer with the interpreter (line
numbers at this branch's first base `961c405`, unchanged at main `e9d6711`,
where the archived record's `project:315` and `project:321`, at its base
`7a9134b`, are `project:322` and `project:328`):

- **A parent that is a symbolic-link loop.** On 3.10 to 3.12 the parent's
  `Path.resolve()` (`project:322`) raises `RuntimeError` before the question,
  and `main()` does not catch it: its handler takes `Refused` and `OSError`
  only (`project:1143`); a traceback, exit 1. On 3.13 and later it does not
  raise, and the parent reaches the question as a missing parent (Observed).
- **A destination that cannot be read.** On 3.10 to 3.13 the
  existing-destination check (`destination.exists()`, `project:328`) raises
  for a parent beneath a directory without search permission, for a parent
  that is such a directory, and for a parent with a component longer than the
  system allows; `main()` prints `REFUSED: [Errno 13] Permission denied:
  '<parent>/<name>'` or `REFUSED: [Errno 36] File name too long: ...`, exit
  2, before the question. On 3.14 and later that read returns False: the
  first and third reach the question as a missing parent, and the second
  shows no obstacle and fails later, in the generator (Observed).

That record's later column was "the council's record, not run here"
(`design.md:93`). This change measures it, states a closed supported range and
tests every version in it, and makes these parents get one answer on every
supported version.

### Observed

At `961c405`, exported by `git archive` into a scratch directory (the checkout
was never written), in `py-bench` as uid 1000 (not root), umask 022, on Linux
(a WSL2 kernel), the fixtures on overlayfs. Interpreters: CPython 3.10.21,
3.11.16, 3.12.14, 3.13.15, 3.14.7 and 3.15.0rc2 installed by
`uv python install` (python-build-standalone builds), and the bench's own
3.12.3; one virtual environment each with `requirements.txt` (PyYAML 6.0.3).

Method: under a scratch parent `P`, 18 parent kinds: a directory; a link to a
directory; a missing path; a dangling link; `FILE/sub`; a regular file
(`FILE`); `FILE/`; a link to a file; a FIFO; two links to each other (given as
the first); a link to itself; a missing path below a loop (`LOOP/sub`); an
existing directory below a directory of mode 600, and below one of mode 000; a
missing path below the mode 600 directory; the mode 600 and the mode 000
directory itself; and one 300-character component. For each, the reads that
`new()` makes (`Path(p).expanduser().resolve()`, then `is_dir()` and
`exists()` on the result, then `(parent / "MyApp").exists()`), and
`project new MyApp --into P/<kind>` run as a subprocess with a fake
`openRepoShape` and a fake workBenches registry of one generator, in four
forms:

- asked: standard input and output on a pseudo-terminal, `CI` unset, Enter
  (the Triad) at the question; where the organization prompt follows, end of
  input (that exit 2 is the harness's, not a finding);
- asked with `--dry-run`: Enter, `example`, `private`;
- not asked, `--type test --dry-run`, standard input not a terminal;
- not asked, `--type test --yes`, creating in a throwaway tree.

The asked form was also run with the parent given positionally and by
`PROJECTS_DIR`. Code sites come from the same arguments run through `new()` in
process, `main()`'s handlers bypassed, so that an exception keeps its frame.

| Parent | Versions | asked, Enter | asked, `--dry-run` | not asked, `--dry-run` | not asked, `--yes` |
| --- | --- | --- | --- | --- | --- |
| a directory; a link to one | all | Qn | Qn, P0 | P0 | C |
| missing; a dangling link | all | Qm | Qm | P0 | C |
| `FILE/sub` | all | Qm | Qm | P0 | M20 |
| `FILE`; `FILE/`; a link to a file; a FIFO | all | Qa | Qa | P0 | M17 |
| a link to itself; two links to each other | 3.10-3.12 | TB | TB | TB | TB |
| | 3.13-3.15 | Qm | Qm | P0 | M17 |
| `LOOP/sub` | 3.10-3.12 | TB | TB | TB | TB |
| | 3.13-3.15 | Qm | Qm | P0 | M40 |
| a directory below one of mode 600 or 000; a missing path below mode 600 | 3.10-3.13 | R13 | R13 | R13 | R13 |
| | 3.14-3.15 | Qm | Qm | P0 | M13 |
| the mode 600 or 000 directory itself | 3.10-3.13 | R13 | R13 | R13 | R13 |
| | 3.14-3.15 | Qn | Qn, P0 | P0 | G1 |
| one 300-character component | 3.10-3.13 | R36 | R36 | R36 | R36 |
| | 3.14-3.15 | Qm | Qm | P0 | M36 |

- Versions: 3.10-3.12 is 3.10.21, 3.11.16, 3.12.3 and 3.12.14, identical in
  every cell; 3.15 is 3.15.0rc2, identical to 3.14.7 in every cell; 3.13.15
  differs from 3.12 only in the loop rows.
- Qn: the question with no parent line. Qm: the question with `Not possible
  here: The parent directory PARENT does not exist; a Triad is created inside
  an existing directory.`; Enter is refused with `REFUSED: A Triad cannot be
  created here. ...`, exit 2, with `--dry-run` too. Qa: the same with the line
  `... exists but is not a directory; choose a parent that is a directory.`
  PARENT is the resolved parent in every Qm and Qa cell; a loop is named by
  its own path, "does not exist", although the link exists.
- TB: a traceback ending `RuntimeError: Symlink loop from 'PARENT'`, exit 1,
  before the question, at `project:322`. R13, R36: `REFUSED: [Errno 13]
  Permission denied: 'PARENT/MyApp'` or `REFUSED: [Errno 36] File name too
  long: 'PARENT/MyApp'`, exit 2, before the question, at `project:328`.
- P0: `Create:` and the plan, exit 0. C: created, exit 0. M13, M17, M20, M36,
  M40: `Create:`, the plan, then `REFUSED: [Errno N] ...` at `parent.mkdir`
  (`project:398`), exit 2. G1: the plan, then the generator runs and fails
  with its own `Permission denied`, exit 1, with no refusal.
- Routes: the positional parent and `PROJECTS_DIR` gave the `--into` outcome
  in every row on every version, except that on 3.10-3.12 a looped
  `PROJECTS_DIR` raises in `projects_dirs()` (`project:79`), not at `:322`.
  The default `~/projects` route was not run here (Feasibility runs it).
- Reads: on 3.13 and later `resolve()` returns a looped path unchanged, and
  `is_dir()` and `exists()` read False. On 3.14 and later `exists()`,
  `is_dir()` and `is_symlink()` return False for every `OSError`, where 3.13
  raises `PermissionError` and the `ENAMETOOLONG` `OSError` from the same
  calls.
- No `DeprecationWarning` or `SyntaxWarning` from `project`, at compile time
  or on `--version` under `-W error`, on any of the seven interpreters.
- Tests: `tests/test_project.py` has no loop fixture and no permission fixture
  (its one `chmod` makes a fake executable, `:175`), so no current test reads
  the rows above that differ.
- Suite: `python -m unittest discover -s tests -v`, with SIGINT at its
  default disposition (run in the foreground, or reset to the default by a
  wrapper): 96 tests, OK, on each of 3.10.21, 3.11.16, 3.12.3, 3.12.14,
  3.13.15, 3.14.7 and 3.15.0rc2. A first batch launched as a background job
  (`&`) inherited SIGINT ignored, and on each interpreter it reached (3.10,
  3.11, 3.13, 3.14) three pseudo-terminal interrupt cases timed out
  (`test_pty_interrupt_at_the_question_cancels`, and the organization and
  visibility subtests of
  `test_pty_interrupt_at_organization_or_visibility_cancels`); that is the
  launch, not the version, and the suite needs SIGINT at its default. The
  residuals are untested behaviour, not failing tests.
- Availability: `actions/python-versions`' `versions-manifest.json`, from
  which `actions/setup-python` resolves a version, read on 2026-10-11, lists
  stable 3.13.16, 3.14.8 and 3.15.0 for Linux (22.04, 24.04, 26.04; x64 and
  arm64). Read, not run in Actions.
- PyYAML on 3.15: PyYAML 6.0.3, the newest release (PyPI, read 2026-10-18),
  has no `cp315` wheel, so on 3.15 `pip install -r requirements.txt` builds
  it from the sdist, pure Python without libyaml (`yaml.__with_libyaml__`
  False). Shown with pip 26.2.1 on 3.15.0rc2 on Linux (exit 0, about 13 s),
  not in Actions.
- Not run: GitHub Actions, free-threaded builds, 3.15.0 final, and a
  single-repository answer followed by `yes` at a pseudo-terminal. Every run
  here is on Linux (the macOS residual is under Risks).

## What Changes

- **The supported range** (recommended; Alternatives below): CPython 3.10 to
  3.15, a closed range. `README.md` states it, says that CI tests each version
  in it on Linux, and says that later versions are untested. The `test` job's
  matrix (`tests.yml:9`) runs the full suite on 3.10, 3.11, 3.12, 3.13, 3.14
  and 3.15, on `ubuntu-latest` (`:10`), the one runner since #32: six jobs
  where there are two. A later minor version joins at its final release by
  one pull request that adds it to the matrix and to the README's range,
  under the first ADDED requirement below; until then the README calls it
  untested. Who opens that pull request was a decision for Brett Heap
  (Decisions, 3); he chose A1 on 2026-10-21: an issue and the pull request at
  each final release, opened by the lane that owns `project` at the time. No
  pre-release runs in CI. The floor stays 3.10, so
  `AGENTS.md:19` ("Python 3.10+") still states the floor.
- **The two cases**, read on the parent `new()` already computes from
  `--into`, the positional parent, `PROJECTS_DIR` or `~/projects`:
  - (L) **a looped parent**: the parent cannot be resolved because it, or a
    symbolic link on its path, loops. Read as: `resolve()` raises
    `RuntimeError` (3.10 to 3.12), or `os.stat()` of the resolved parent
    fails with `ELOOP` (any version). It covers a link to itself, two links
    to each other, a missing path below a loop (`LOOP/sub`), and a loop below
    a linked directory.
  - (U) **an unreadable destination**: reading the destination
    (`PARENT/NAME`, or `PARENT/FAMILY/NAME` with `--shape --family`) fails
    for a reason other than its absence. The measured reasons are `EACCES`,
    for a parent beneath a directory without search permission (existing or
    not) or a parent that is such a directory, and `ENAMETOOLONG`, for any
    component of that path longer than the system's name limit (a parent
    component, NAME, or the `--family` folder; neither name pattern,
    `project:318` and `:323`, caps the length), or for the whole path longer
    than the system's path limit. The command cannot tell whether such a
    destination exists, and does not guess.
- **The answers**, the same on every supported version, before the question
  and before any path's steps, for every route and form: by flag, not asked
  (`CI` set, no terminal, a workspace name), at a terminal with no choosing
  flag, with `--dry-run`, and with `--shape` by flag:
  - (L): `REFUSED: [Errno N] <the system's text for ELOOP>: 'PARENT'`,
    exit 2, printed by `main()`'s existing `OSError` handler. PARENT is the
    parent as given, before any resolution: `--into`, the positional parent,
    `PROJECTS_DIR` or `~/projects`, with `~` expanded and made absolute by
    `Path.absolute()` (which keeps `..` and links). It is the same string on
    every version, by every route, `PROJECTS_DIR` included (Feasibility). No
    new sentence. Its place: after the name check, the positional-parent
    check and the family-name check (`project:323-324`), before the
    existing-destination check, so a family that is not a single folder name
    is refused first on every version, as on 3.13 and later today. This
    changes 3.10 to 3.12 too: their traceback becomes a refusal.
  - (U): today's 3.10 to 3.13 answer, byte for byte, at the
    existing-destination check, where it is today:
    `REFUSED: [Errno 13] Permission denied: 'DESTINATION'` or
    `REFUSED: [Errno 36] File name too long: 'DESTINATION'` (each system's
    number and text), exit 2. DESTINATION is the destination built on the
    resolved parent (`PARENT/NAME`, or `PARENT/FAMILY/NAME`), where PARENT is
    the resolved parent, as `new()` computes it and as the missing and
    not-a-directory sentences name it.
  - The two name different prefixes under a linked prefix: (L) names the
    parent as given, (U) the resolved destination (council cases J and I).
    Both are true; (L) keeps the given form because it is the same string on
    every version and route, and (U) keeps today's 3.10 to 3.13 text.
- **The reads, by site** (recommended technique at each; Alternatives below):
  - S1, the parent's resolution (`project:322`, which reaches
    `projects_dirs()` at `project:79` when the parent is `PROJECTS_DIR`):
    the non-strict `resolve()` stays; its `RuntimeError`, or `ELOOP` from
    one `os.stat()` of the resolved parent, marks (L), which is raised after
    the family-name check. Every other outcome of that `os.stat()` (success,
    `ENOENT`, `ENOTDIR`, `EACCES`, `ENAMETOOLONG`) passes to S2 unchanged.
    `projects_dirs()` is not edited: PARENT is built from the same inputs
    before resolution, so no caller of it changes (`workbenches()`,
    `project:90`, and everything from `discover`, `project:433`, down are
    outside this change).
  - S2, the existing-destination check (`project:328`):
    `destination.exists() or destination.is_symlink()` becomes one
    `os.lstat(destination)`. Success refuses as an existing destination, with
    today's sentence. `ENOENT`, `ENOTDIR`, `EBADF` and `ELOOP` read as
    absent: the set that pathlib on 3.10 to 3.13 ignores in `exists()` and
    `is_symlink()` (read from each interpreter's pathlib). Any
    other `OSError` propagates to `main()`, as on 3.10 to 3.13. So a later
    pathlib cannot move the outcome. One deviation from 3.10 to 3.13 is
    intended: a destination that is itself a symbolic link into a directory
    without search permission is refused as existing (`Destination already
    exists`, 3.14's answer) instead of with `[Errno 13]`. Both answers are
    true, and both exit 2 before the question.
  - Unchanged: `known_obstacles()` (`project:235-254`) and its pathlib reads
    (archived D1), the shape branch's `parent.is_dir()` (`project:371`),
    `parent.mkdir` (`project:398`) and `main()`. They are reached only after
    S1 and S2 have refused both cases. Past S2, a read of the parent can fail
    only with `ENOENT` or `ENOTDIR`, which every version reads alike.
- **N5, revisited on its merits.** The archived lead rejected "a raw
  `os.stat` classified by errno" for that change because "it would add
  behaviour, strings and a third case beyond the wording follow-up"
  (`clarifications.md:88-92`). N3 chose `exists()` because it "has the same
  error handling as `is_dir()` on every version" (`:63-65`), and #21 keeps
  that for its own read (its Out of Scope, line 401). Here the behaviour is
  the change's purpose, the recommended answers add no string, and the third
  case, (L), is its subject. N3's premise holds only within a version:
  `exists()` and `is_dir()` share one error handling, and that handling is
  what moved between 3.13 and 3.14 (Observed). An errno from `os.stat()` or
  `os.lstat()` is the operating system's and does not move with the
  interpreter. The classification stays narrow: S1 classifies only `ELOOP`;
  S2 reads as absent exactly what 3.10 to 3.13 read as absent; everything
  else keeps the 3.10 to 3.13 path.
- **Tests** (recommended; Alternatives below): a module of its own,
  `tests/test_parent_reads.py` (name provisional), found by the existing
  `python -m unittest discover -s tests -v` (`tests.yml:17`). It borrows
  `tests/test_project.py`'s harness (`setUp`, `run_pty`, `run_inproc`, the
  parent fixtures) by composition: it imports the module and creates
  `test_project.ProjectTests(methodName)` instances, calling their `setUp()`
  and `doCleanups()`; `setUp` registers its own cleanup
  (`tests/test_project.py:117-119`). It never subclasses `ProjectTests` and
  never binds the class name in its own namespace, so discovery runs no
  existing test twice. No line of `tests/test_project.py` changes.
- **`README.md`** (texts fixed by the design, checked by a test): in Install
  (lines 17-18), the Python sentence states the closed range, for example
  "Python 3.10 to 3.15 is supported; CI tests each of those versions on
  Linux, and later versions are untested." It stays a sentence of its own,
  apart from the Git 2.36 sentence that feature 004 adds to the same
  paragraph. Lines 281-282 ("CI covers Linux only.", #32's wording) gain the
  range and keep "Linux only".
- **`.github/workflows/tests.yml`**: the `test` job's `python` list (`:9`)
  only. Its `runs-on: ubuntu-latest` (`:10`), its steps, its strategy keys
  and every other job are unchanged; no `os` axis returns.

### Alternatives

- **Versions.** (R1) Every released minor version from 3.10 to 3.15 on
  `ubuntu-latest`, six jobs: recommended. (R2) The floor, 3.12 and the newest
  (3.10, 3.12, 3.15; three jobs): cheaper, but 3.11, 3.13 and 3.14 stay
  claimed and unrun, the gap this change closes. (R3) Withdrawn: a macOS
  entry. Since #32, CI runs on Linux only, by Brett Heap's decision of
  2026-10-15, and this change proposes no macOS job (the residual is under
  Risks). (R4) Raise the floor to 3.11, as upstream
  security support for 3.10 ends in October 2026 (PEP 619): not recommended in
  this change. Ubuntu 22.04's `python3` is 3.10; lane openRepoProject-2's
  `add-project-overview` starts Git children with `start_new_session=True`
  rather than 3.11's `process_group=0` to keep 3.10 (its proposal, "Process
  groups on Python 3.10"); a floor change is its own decision. The
  repository is public and `main`'s ruleset requires no status check (its
  rules are `non_fast_forward`, `deletion` and `pull_request`), so the added
  jobs cost no paid minutes and gate nothing by rule; the landing practice
  reads every job (archived `tasks.md` 3.1, "green checks on all four CI
  jobs"; two jobs at `e9d6711`, six after this change).
- **The range's form.** (C1) A closed range, "3.10 to 3.15", with later
  versions called untested: recommended; the README claims only what CI runs.
  (C2) An open range, "3.10 or newer": it claims every later version as soon
  as it is released, before any job runs it, which is today's gap again;
  rejected.
- **The range's home.** (H1) The first ADDED requirement, which AC6's test
  enforces against `tests.yml` and the README: recommended. A drift between
  the README and the matrix fails a test, and since the requirement names
  versions, not systems, a decision about systems such as #32's needs no
  spec change. (H2) `README.md` and CI only, with no requirement: lighter,
  but AC6 then enforces no spec statement, and the range can change without
  a delta.
- **Who adds a new release.** (A1) At each CPython final release, an issue
  and one pull request that adds the version to the matrix and to the
  README's range, opened by the lane that owns `project` at the time: no new
  machinery, but it depends on someone noticing the release. (A2) A
  scheduled job that fails when setup-python's manifest lists a stable minor
  version above the matrix: it notices for us, at the cost of a new trigger
  and job in the shared `tests.yml`, beyond the matrix-only agreement, so it
  needs lane openRepoProject-2's assent. Neither was recommended over the
  other here (Decisions, 3); Brett Heap chose A1 on 2026-10-21, so A2 is not
  chosen.
- **A pre-release, such as 3.16.** (P1) None in CI; a minor version joins at
  its final release: recommended. It stays within the `test` job's matrix,
  the edit agreed with lane openRepoProject-2, and a pre-release failure
  cannot gate a merge. (P2) The pre-release as a non-gating entry of the
  `test` job: warning before the release, at the cost of a job that may be
  red by design. It needs keys outside the matrix (`allow-prereleases` on the
  setup step, a job-level `continue-on-error`), so lane 2's assent. A failing
  `continue-on-error` job still reports a failed check run while the workflow
  run passes, so the governance landing task must exempt that entry from
  "green on all jobs". Its check name carries the version (`test (3.16)`,
  the matrix having only the `python` axis since #32), so a future
  required-check rule would need editing at each release.
  `allow-prereleases` has no effect once a stable release matches. (P3) A
  scheduled or manually dispatched pre-release job: a new
  trigger and job in the shared file, beyond the agreement; rejected for this
  change.
- **(L)'s answer.** (L1) The system's `ELOOP` refusal through `main()`:
  recommended; no new string, the same handler and form as (U). (L2) A fixed
  sentence, such as `The parent PARENT is a symbolic link loop; choose a
  parent that is a directory.`: the same on every system and states a
  repair, but a new string for the design to fix. (L3) The 3.10 to 3.12
  traceback on every version: an uncaught exception exiting 1, a status the
  README gives to doctor findings (`README.md:284-286`); rejected. (L4) Name
  the loop as an obstacle in the question: it blocks both answers (one wasted
  answer, as #21's first risk), and it edits the requirement "Known Triad
  obstacles are named before the question and refused on a Triad answer",
  which #21 MODIFIES; rejected.
- **(L)'s place.** (Q1) After the family-name check (`project:323-324`):
  recommended; on 3.13 and later the family refusal comes first today, and
  #21's ADDED requirement lists "a family that is not a single folder name"
  among the earlier refusals (its delta, lines 16-20). (Q2) At the
  resolution (`project:322`), before the family check, where 3.10 to 3.12's
  traceback is: the family refusal would give way to (L) on every version.
- **(U)'s answer.** (U1) Today's 3.10 to 3.13 text: recommended. (U2) A
  fixed sentence: a new string, and the raw text already names the path and
  the reason. (U3) The 3.14 outcome on every version, the missing-parent
  sentence or none: false for a directory that exists, and the paths go on
  to fail later (Observed); rejected.
- **S1's technique.** (T1) `resolve(strict=True)` with errno handling: on
  3.10 to 3.12 strict mode still raises `RuntimeError` for a loop, and on
  every version it raises `FileNotFoundError` for the missing parent that a
  single-repository answer creates, so it needs the `RuntimeError` mapping
  and a fallback to the non-strict form as well: two resolutions and more
  errnos for one result. (T2) Non-strict `resolve()`, the `RuntimeError`
  mapping and one `os.stat()` classifying `ELOOP`: recommended. (T3) A
  wrapper gated on `sys.version_info`: it encodes one probe's findings as
  constants and is silently wrong after the next change; rejected in favour
  of reading the outcome. (T4) Pathlib only, walking `is_symlink()` and
  `readlink()`: it reimplements loop detection; rejected.
- **S2's technique.** (E1) One `os.lstat()`, reading 3.10 to 3.13 pathlib's
  ignored errnos as absent: recommended; one read, and its one deviation
  names the true obstacle (the name is taken by a link) with 3.14's answer.
  (E2) The same errnos over two reads, `os.stat()` then `os.lstat()`, as
  `exists() or is_symlink()` does: 3.10 to 3.13's outcome exactly, `[Errno
  13]` for a destination linked into a directory without search permission
  included, at the cost of a second read; acceptable, the design may choose
  it. (E3) One
  `os.lstat()` reading only `ENOENT` and `ENOTDIR` as absent: rejected by
  Feasibility, since it refuses `--shape --family FAMILY` with `[Errno 40]`
  where `PARENT/FAMILY` is a loop, which every version today plans (exit 0).
  (E4) An `os.access()` search check of the ancestors: it predicts refusals
  the system may not make (root, ACLs), #21's reason against a writability
  read; rejected.
- **Where the tests go.** (M1) A module of its own: recommended. #21's
  realization rewrites a test and adds `known_obstacle_cases()` rows in the
  `new`-path section of `tests/test_project.py` (`:394-415`, `:1394-1579`),
  and feature 004 edits its clean tests and helpers; a separate module
  touches neither lane's hunks. (M2) The `new`-path section, after
  `test_pty_no_known_obstacle_names_none` (`:1572-1579`): the helpers are at
  hand, at the cost of a merge with #21's realization in the same section.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

`project-command`: three ADDED and two MODIFIED requirements. ADDED titles are
provisional and distinct from every existing title, from #21's ADDED title and
from lane openRepoProject-2's ADDED "Repository inspection requires Git 2.36
and shares one evidence model". Each MODIFIED block is written against #21's
delta text (`openspec/changes/refuse-non-directory-parent-early/specs/
project-command/spec.md` at `8f3ca2d`, byte-identical to its text at
`1b84a94` and `a43e7d2`, or #21's head when the design is written) and
changes only the statements listed below; every other statement keeps its
wording.

- ADDED: "Supported Python versions are stated and tested". `README.md`
  names the supported range, from its lowest to its highest minor version,
  and calls later versions untested; CI runs the full suite on every minor
  version in that range and on no other. It names versions, not systems
  (H1). Scenarios: "Every version in the README's range is tested in CI";
  "The lowest supported version is 3.10"; "A version above the range is
  called untested".
- ADDED: "A parent that is a symbolic-link loop is refused before the
  question". It defines (L) by its read, states its answer, PARENT (the
  parent as given) and its place, and says that it holds on every supported
  version. Scenarios: "A looped parent by each route"; "A missing path below
  a loop"; "A loop below a linked directory is named as given"; "A relative
  looped parent is named from the working directory"; "A looped parent's dry
  run"; "A looped parent with the shape chosen by flag"; "A looped parent at
  the terminal is not asked"; "A looped parent with a family that is not a
  single folder name".
- ADDED: "A destination that cannot be read is refused before the question".
  It defines (U), names DESTINATION as built on the resolved parent, and
  states that the existing-destination check refuses it with the system's
  error, exit 2, on every supported version, and that a destination that
  exists, a symbolic link included, is refused as existing. Scenarios: "An
  existing directory beneath a directory without search permission"; "A
  missing path beneath one"; "A parent without search permission"; "A
  parent with a component longer than the system allows"; "An over-long
  name, family or path"; "An unreadable destination's dry run"; "An
  unreadable destination with the shape chosen by flag"; "An unreadable
  destination at the terminal is not asked"; "An existing destination is
  refused as before"; "A destination that is a symbolic link is refused as
  existing" (S2's intended deviation); "A destination below a looping folder
  is read as absent".
- MODIFIED: "Creation question is asked only of a person choosing at the
  terminal", as #21's delta states it (lines 129-198). Its list of refusals
  made before a path is chosen (lines 148-151) gains a looped parent and a
  destination that cannot be read. Its exception for invocations that are
  not asked (lines 153-155) gains both, ahead of every refusal after the
  existing-destination check. Its scenario "Refusals before a path is chosen
  come first" (lines 187-190) gains both in its WHEN, and its scenario "The
  refusal order of an invocation not asked the question is unchanged" (lines
  196-198) gains both in the carve-out its WHEN already makes for a parent
  blocked by a non-directory.
- MODIFIED: #21's ADDED "A parent blocked by a non-directory is refused
  before the single-repository path's steps", as #21's delta states it
  (lines 5-88). Its list of earlier refusals (lines 16-20) gains the two
  refusals. Its sentence "The shape path SHALL keep its own refusal of a
  parent that is not an existing directory" (lines 36-37), and its scenario
  "The shape branch's parent refusal is unchanged" (lines 86-88), are scoped
  to a parent that passes those earlier refusals. Its permission sentence
  (lines 37-43) and its scenario "A parent the person cannot write still
  fails only at creation" (lines 73-76) are scoped to "a directory the person
  can search but cannot write". This block would have dropped had lane
  openRepoProject-1 scoped them in #21 before it was ratified; Brett Heap took
  Decision 12's recommendation on 2026-10-21, so the block stays (Decisions,
  12).

### Statements this change makes false, and their treatment

Each is false on some supported version for a looped parent or an unreadable
destination:

- #21's MODIFIED "Creation question is asked only of a person choosing at
  the terminal": the list of refusals before a path is chosen (lines
  148-151), read as complete; "Every invocation that is not asked the
  question SHALL keep its existing order of refusals, except that a parent
  blocked by a non-directory is refused before generator selection" (lines
  153-155), since on 3.13 and later a looped parent has no early refusal
  today and (L) now precedes `--org` without `--shape` (`project:383-384`),
  `choose()` (`:385`) and the late `--workflow` check (`:388-390`), and on
  3.14 and later (U) does the same; the scenario "Refusals before a path is
  chosen come first" (lines 187-190); and the scenario "The refusal order of
  an invocation not asked the question is unchanged" (lines 196-198), whose
  WHEN admits a looped or unreadable parent that is not blocked by a
  non-directory and whose THEN, the generator refusal, (L) and (U) now
  precede. MODIFIED.
- #21's ADDED requirement: its list of earlier refusals (lines 16-20); its
  shape sentence (lines 36-37) and scenario (lines 86-88), since a looped or
  unreadable parent with `--shape` by flag now gets (L) or (U), not the shape
  refusal (on 3.13 and later for (L), on 3.14 and later for (U); on 3.10 to
  3.12 a loop is a traceback today). MODIFIED (Decision 12 took this route,
  not scoping by lane 1).
- #21's ADDED requirement, its permission sentence (lines 37-43, "a parent
  that is a directory the person cannot write, or a missing parent whose
  nearest existing path above it is such a directory, still passes the dry
  run and fails at creation") and its scenario "A parent the person cannot
  write still fails only at creation" (lines 73-76). For a directory the
  person cannot search (mode 000 or 600), (U) refuses the dry run with
  `[Errno 13]` naming the destination on every version. On 3.10 to 3.13 that
  is today's answer already, so the sentence is false there before this
  change (and disagrees with #21's own Out of Scope, its proposal lines
  410-411); on 3.14 and later this change makes it false. A directory the
  person can search but not write (mode 555, #21's acceptance criterion 9)
  is unchanged on every version (council evidence 1). MODIFIED, scoped to "a
  directory the person can search but cannot write" (Decision 12 took this
  route, not scoping by lane 1).
- #21's README sentence (its `design.md:187-191`, inserted after "Existing
  destinations refuse.", `README.md:96`): "`--dry-run` reads no permissions:
  a parent that is a directory the person cannot write still passes the dry
  run and fails at creation, as before, and so, for a single repository,
  does a missing parent whose nearest existing path above it is such a
  directory." The same claim, false in the same cases. This realization,
  landing after #21's, scopes it with the same clause (Decision 12).
- "Delegate project creation", scenario "Preview" (main spec `:25-28`): a
  looped dry run on 3.13 and later, and an unreadable one on 3.14 and later,
  no longer print the plan. #21's MODIFIED WHEN, "and no refusal precedes
  that path's plan" (its delta, line 111), covers both, so this change adds
  no block for it and relies on #21 archiving first.
- "Known Triad obstacles are named before the question and refused on a
  Triad answer" (main spec `:200-263`, as #21 MODIFIES it): unchanged; a
  looped or unreadable parent no longer reaches its read on any version.

Kept, true under their own wording: "the invocation follows the path its flags
choose, with its existing prompts and refusals" (main spec `:103-106`; #21's
delta, lines 163-166), since (L) and (U) come before any path and the path's
own prompts and refusals are unchanged for a parent that reaches it; and "the
creation runs exactly as it would without this requirement" (main spec
`:117-120`; #21's delta, lines 177-180), since that requirement is the
creation question's and (L) and (U) are this change's own. Also kept: #21's
scenarios "A person at the terminal without a choosing flag" (its delta,
lines 158-161) and "A single repository with a parent that is not blocked"
(lines 69-71). Each presupposes the refusals its requirement places first,
as each already does for an existing destination, and the MODIFIED lists
above now include (L) and (U) among them.

## Impact

- **`project`**: in `new()`, S1 (`project:322`, with (L) raised after the
  family-name check at `:323-324`) and S2 (`project:328`), and
  `import errno` (standard library). Unchanged: `projects_dirs()`,
  `known_obstacles()`, the question, the shape branch, `choose()`,
  `parent.mkdir`, `main()`, and everything from `discover` (`project:433`)
  down. No new sentence, flag, environment variable or configuration file.
- **Feasibility, observed** (below): the recommended S1 and S2 on a scratch
  copy gave the answers above on 3.10 to 3.15rc2, with every other row
  unchanged.
- **Tests**: the new module per the acceptance criteria below; no existing
  test is edited, and every one runs on all six jobs.
- **`README.md`** lines 17-18 and 281-282, and #21's README permission
  sentence once #21's realization has added it, scoped as Decision 12 says;
  **`.github/workflows/tests.yml`** line 9; the spec at archive.
  `AGENTS.md:19` ("Python 3.10+") states the floor and is not edited.
- **Feature records** stay unedited. The new feature's spec states that, for
  these cases, it supersedes feature 003's EC-004
  (`specs/003-parent-obstacle-wording/spec.md:139-142`: on CI's versions a
  loop "errors when the parent is resolved"; later versions print the
  missing sentence), its plan's rows and residual notes (`plan.md:124`,
  `:209-211`, `:272`) and its research note (`research.md:79-81`). The
  archived change is cited, never edited.
- **Speckit handoff**: one feature, numbered when `/speckit.specify` runs
  from a main synced to origin (the next free number; none hard-coded).
- **Handoffs after landing**: no new issue but the release practice of
  Decisions, 3 (A1, chosen). The realization reaches `onp` when workBenches
  next moves its pin, on its owner's act; a comment on a workBenches pin
  issue, as archived D5 did, is design D9's.

### Feasibility

A scratch copy of `project` at `961c405`, not committed, with S1 and S2 as
recommended (`import errno`, and 21 lines in `new()` in place of two), was
run beside the unpatched copy on 3.10.21, 3.11.16, 3.12.3, 3.13.15, 3.14.7
and 3.15.0rc2:

1. by the Observed method, all 18 kinds in seven modes (the four forms, and
   the asked form by the positional parent, by `PROJECTS_DIR` and by the
   default `~/projects`, `HOME/projects` being a link to the kind): 126 cells
   per version;
2. not asked (`CI=true`), the three loop kinds and six unreadable ones (an
   existing and a missing path below a mode 000 directory, a directory below
   a mode 600 one, parents of mode 600 and 000, an over-long component) by
   all four routes, and seven other kinds by `--into`, each in three forms
   (`--type test --yes`, `--type test --dry-run`, `--shape --org example
   --visibility private --dry-run`), with the fixture tree listed before and
   after each run: 130 runs per version;
3. the review's cases, not asked, with `--dry-run`.

| Case | 3.10 | 3.11 | 3.12 | 3.13 | 3.14 | 3.15rc2 |
| --- | --- | --- | --- | --- | --- | --- |
| a loop (3 kinds): the (L) line naming PARENT as given | yes | yes | yes | yes | yes | yes |
| below a directory without search permission (4 kinds): the 3.10 answer | yes | yes | yes | yes | yes | yes |
| a parent without search permission (modes 600 and 000): the 3.10 answer | yes | yes | yes | yes | yes | yes |
| an over-long component (300 and `PC_NAME_MAX` + 1 = 256): the 3.10 answer | yes | yes | yes | yes | yes | yes |
| every other kind: that version's unpatched output | yes | yes | yes | yes | yes | yes |
| a loop and `--family 1bad`: the family refusal | yes | yes | yes | yes | yes | yes |
| `LINK/loop` by `--into` and by `PROJECTS_DIR`: (L) naming `LINK/loop` | yes | yes | yes | yes | yes | yes |
| a destination that is a directory, a file, a dangling or self-loop link: unchanged | yes | yes | yes | yes | yes | yes |
| a destination linked into a mode 000 directory: `Destination already exists` | yes | yes | yes | yes | yes | yes |
| `--shape --family Fam`, `PARENT/Fam` a loop: unchanged, the plan, exit 0 | yes | yes | yes | yes | yes | yes |

- The patched copy's standard output, standard error and status were
  identical on all six versions in all 126 cells and all 130 runs, and
  nothing changed in the fixture tree in any (L) or (U) run of 2. The
  unpatched copy gave the Observed matrix in every cell, and by the default
  route the same outcomes as by `--into`.
- The one row whose unpatched answer the patch changes outside (L) and (U)
  is the destination linked into a mode 000 directory: `[Errno 13]` on 3.10
  to 3.13, `Destination already exists` on 3.14 and 3.15rc2 and, patched, on
  all six (the intended deviation in S2).
- An earlier copy that read only `ENOENT` and `ENOTDIR` as absent at S2 (E3)
  refused the `--family` loop with `[Errno 40]` on all six versions; hence
  E1's errno set.
- The council's runs of the same two copies, not asked, add these rows (its
  cases E, F and G, and its evidence 1):
  - an over-long NAME (256 characters, `PC_NAME_MAX` + 1), an over-long
    `--family` under `--shape`, and a parent of 4550 bytes, longer than
    `PC_PATH_MAX` (4096), made of short components: `[Errno 36]` naming the
    destination, exit 2, on 3.10 to 3.13 unpatched and on every version
    patched; unpatched 3.14 and 3.15rc2 print the plan and exit 0. That is
    (U) on every version (AD-1);
  - a missing parent below a directory of mode 555 (search, no write): the
    plan, exit 0, with `--dry-run`, and with `--yes` the plan then `[Errno
    13]` at `parent.mkdir`, exit 2, unpatched and patched, on 3.10.21,
    3.12.3, 3.13.15, 3.14.7 and 3.15.0rc2: unchanged, as #21's acceptance
    criterion 9 expects. Below a directory of mode 000 (no search): `[Errno
    13]` naming `D/missing/MyApp`, no `Create:`, exit 2, unpatched on 3.10
    to 3.13 and patched on all five; unpatched 3.14 and 3.15rc2 print the
    plan. That is (U) (AR-1).
- Not run: the existing suite against the patched copy (the realization runs
  it), and Actions. Linux only, as Observed.

## Ordering and shared files

- **#32 (CI on Linux only, on main at `e9d6711`).** Merged into this branch.
  This change builds on its `tests.yml` (one `python` axis, `runs-on:
  ubuntu-latest`) and its README sentence ("CI covers Linux only.",
  `README.md:281-282`), keeps both, and adds no `os` axis.
- **#21 (`refuse-non-directory-parent-early`, lane openRepoProject-1).**
  - Spec: this change's two MODIFIED blocks are written against #21's delta
    text at `8f3ca2d` (or #21's head when the design is written), and it
    relies on #21's MODIFIED "Preview" WHEN, so it archives after
    `refuse-non-directory-parent-early`.
  - Realization: it lands after #21's realization and merges main in first,
    as issue #22 says. Both edit `new()`: this one at `project:322-328`, #21's
    at the head of the bench branch (`project:382-385`) and in
    `known_obstacles()` (`project:235-254`).
  - S1 and S2 run before #21's head refusal and its question read, so on every
    version a looped or unreadable parent never reaches #21's read, and its
    Out of Scope note on N1 (its proposal, lines 412-414) stays true.
  - #21's surface, the early non-directory refusal and its sentences, is not
    touched. Its tests run on six versions once this matrix lands; a failure
    of one of them on an added version is reported to lane 1, not fixed here.
  - #21 at `8f3ca2d` has lane 1's alignment with Linux-only CI (#32): its
    design (`:39-40`, `:355-357`), its proposal (lines 353 and 415-416) and
    its landing task 3.1 no longer name the four-job matrix or macOS CI; they
    name `ubuntu-latest` on Python 3.10 and 3.12. Task 3.1 reads "green
    checks on every job of `.github/workflows/tests.yml`", which still holds
    once this change widens the matrix; its "since #32, two" count is lane
    1's to update. This change does not depend on it.
- **Feature 004 (`add-project-clean-all-safe`, lane openRepoProject-2).**
  - `.github/workflows/tests.yml`: this change edits only the `test` job's
    `python` list (`:9`); feature 004 adds a separate `git-floor` job on
    `ubuntu-latest` and leaves the `test` job unchanged
    (`specs/004-project-clean-all-safe/plan.md` on lane 2's branch
    `004-project-clean-all-safe` at `96a08d4`: "CI shape", `:248-250`, where
    "every job of the `test` matrix (`ubuntu-latest`, Linux only since #32;
    R-35, R-46)" runs the whole suite unchanged beside "one new job,
    `git-floor`, on `ubuntu-latest` with Python 3.10"; and its file table,
    `:312-313`, "the `test` job unchanged"). The job is merged into that
    branch (`4baec61`) and, at `96a08d4`, `.github/workflows/tests.yml`
    differs from main's by 50 added lines after `:17` only (comment
    `:19-24`, job `:25-67`), so the `test` job and its `python` list (`:9`)
    are as on main; the branch has merged `e9d6711`.
  - The job's comment first read "The two test jobs above (ubuntu-latest,
    Python 3.10 and 3.12)" (`tests.yml:19-20` as `4baec61` merged it), which
    goes stale when this matrix widens. Lane openRepoProject-2 agreed on
    2026-10-19 (its ruling R-46) to a comment that names no job count,
    merged by `0d3e0f7` and at `tests.yml:19-21` at `96a08d4`: "The test jobs
    above (ubuntu-latest, every Python of the matrix) run on whichever Git
    their runner ships". R-46 (`090dcc7`, merged by lane 2's doc round 3,
    `acc822e`) also replaced "two jobs" with "every job of the `test`
    matrix" in its plan, research and spec, and added it to its tasks; at
    `96a08d4`: plan.md:228-229, :248-249, :350; research.md:529-531, :547;
    spec.md:1626-1627, :1756-1757; tasks.md:53, :263-264. Its quickstart.md
    names no job count. This change needs no edit on 004's account,
    whichever of the two lands first.
  - `project`'s import block: feature 004 adds `import errno` there (with
    other standard modules, `project:11-12` at `96a08d4`), the import S1 and
    S2 need. A three-way merge of the feasibility copy with feature 004's
    `project` over `961c405` is clean and keeps one `import errno` (council
    evidence 4; re-run on 2026-10-20 at `96a08d4`).
    The realization adds the import only if main lacks it (design D7).
  - `tests/test_project.py`: this change adds no line to it (M1); feature
    004 edits its clean tests. Under M2 this change's tests would go in the
    `new`-path section only.
  - `README.md:17-19` (Install): overlapping lines, so the second to merge
    meets a textual conflict. This change edits only the Python-version
    wording; feature 004 edits only the Git 2.36 floor statement there (its
    plan, step 8, "README and AGENTS.md", `plan.md:106-112` at `96a08d4`;
    its T122 is open, so `README.md` is still main's text there), and its
    clean section further down. The merged paragraph keeps both as separate
    sentences, the Python sentence first, then Git's. Lane openRepoProject-2
    acknowledged these lines as a shared file under the same rule on
    2026-10-11 (relayed by the lead).
    This change's `:281-282` and feature 004's exit-code lines (`:284-286`)
    are adjacent paragraphs, not the same lines.
  - Whichever change lands second merges main in. Agreed with lane
    openRepoProject-2 on 2026-10-11 for `tests.yml` and
    `tests/test_project.py` (issue #22, "Ordering and shared files"), and
    for `README.md:17-19` as above.
  - The widened matrix runs feature 004's whole suite on 3.11, 3.13, 3.14
    and 3.15 in either order. If this change lands first, feature 004 must
    be green on six jobs; if feature 004 lands first, this realization
    must be. A failure of a feature 004 test on an added version is reported
    to lane 2, not fixed here.
- **`add-project-overview` (lane openRepoProject-2)** keeps 3.10
  compatibility by design; keeping the floor keeps that.
- Everything from `discover` down is not touched. No rebase and no force
  push: merges only.

## Acceptance criteria

On every version of the new matrix, on `ubuntu-latest`, each by a test:

1. The full suite passes on all six jobs, with no existing test edited;
   discovery's "Ran N" equals main's count at merge plus the new module's.
2. (L): a symbolic link to itself, two links to each other and `LOOP/sub`,
   each by `--into`, and the first also by the positional parent,
   `PROJECTS_DIR` and the default `~/projects`; a loop below a linked
   directory (`LINK/loop`) by `--into` and by `PROJECTS_DIR`. Each with
   `--type test --yes`, with `--dry-run`, with `--shape --org example
   --visibility private`, not asked (`CI=true`; a non-terminal stdin) and
   asked (a pty, no choosing flag): exit 2, the one line
   `REFUSED: [Errno {errno.ELOOP}] {os.strerror(errno.ELOOP)}: 'PARENT'`,
   PARENT as given (`LINK/loop` for the linked one), no question line, no
   `Create:`, and nothing changed (the `rglob` snapshot of archived N2). A
   loop with `--shape --family 1bad`: the family refusal. A relative
   `--into loop`, run from a working directory reached through a symbolic
   link: PARENT has the physical prefix that `os.getcwd()` reports (N7).
3. (U): an existing directory beneath a directory of mode 000 and beneath
   one of mode 600, a missing path beneath the mode 600 one, a parent of mode
   600 and one of mode 000, and a parent with one component of
   `os.pathconf(base, "PC_NAME_MAX") + 1` characters, each by `--into`, with
   the forms of 2; and three more sources of `ENAMETOOLONG` (AD-1): a NAME of
   that length into an existing directory, `--shape --org example
   --visibility private --family` with a family of that length, and a parent
   longer than `os.pathconf(base, "PC_PATH_MAX")` made of 200-character
   components. Each: exit 2,
   `REFUSED: [Errno {e}] {os.strerror(e)}: 'DESTINATION'` with `e` the
   `EACCES` or `ENAMETOOLONG` of the system, no question line, no
   `Create:`, nothing changed. DESTINATION is the destination built on the
   resolved parent, as `new()` computes it (`PARENT/MyApp`, or
   `PARENT/FAMILY/MyApp` for the family row), never the parent as given
   (AD-2). Both snapshots are taken with modes restored, and modes are
   restored before cleanup. For each permission row `setUp` creates a child
   of the locked directory before the chmod, and the row is skipped only when
   `os.lstat()` of that existing child succeeds (root, capabilities, ACLs;
   N10); no (U) test is skipped on any CI job (read from the `-v` output).
4. S2's success branch: a destination that is an existing directory, a
   regular file, a dangling symbolic link, a self-loop link and a link into a
   directory of mode 000 is refused with `REFUSED: Destination already
   exists: PARENT/MyApp`, exit 2; and `--shape --family Fam --dry-run` with
   `PARENT/Fam` a loop prints the plan and exits 0.
5. The parents that S1 and S2 do not classify (a directory, a link to one, a
   missing parent, a dangling link, a regular file, a link to a file, a FIFO,
   `FILE/sub`) pass both reads: asked, each reaches the question. Their
   answers after the question are main's at merge, #21's included, as main's
   own tests pin them.
6. A test in the new module reads `.github/workflows/tests.yml` with PyYAML
   (already in `requirements.txt`) and the README's two range sentences
   (Install and Development, design D1), and asserts that both name the same
   range, that the `test` job's `python` list is every minor version from the
   README's lowest to its highest and no other, and that the lowest is 3.10.
7. Every added line is ASCII (archived N4's scope: added lines, not the
   whole of `project`).

## Risks

- Two jobs become six. `on: [push, pull_request]` runs each twice for a pull
  request from a branch of this repository: 12 job runs per push, all on
  `ubuntu-latest`. Feature 004's suite runs in each job.
- `tests.yml` sets no `fail-fast`, so the default (true) cancels sibling jobs
  at the first failure, hiding which versions also fail; `fail-fast: false`
  is a strategy key outside `matrix:` and needs lane 2's assent (Decisions,
  11).
- By the manifest (read on 2026-10-11, not run), Linux 24.04 resolves 3.10
  to 3.15 to 3.10.22, 3.11.17, 3.12.15, 3.13.16, 3.14.8 and 3.15.0; 22.04
  and 26.04 list the same. The landing task cites each job's resolved
  version from setup-python's log.
- The 3.15 evidence here is from 3.15.0rc2; the realization's CI run is the
  first on 3.15.0.
- The 3.15 job builds PyYAML from source until a `cp315` wheel exists
  (Observed); a build failure there fails the job, not the code. The landing
  task cites the 3.15 job's pip log.
- A test outside this change's surface that fails on an added version blocks
  the widened matrix until its owner fixes it.
- NOTED residual, macOS: the README excludes only native Windows
  (`README.md:282`), so `project` may still be run on macOS, but since #32 no
  CI job runs there, and every run in this proposal is on Linux. The (L) and
  (U) lines carry the system's errno number and text; the tests build every
  line from `errno` and `os.strerror()`, size names from `os.pathconf()` and
  take paths under the resolved base, so they are written to hold there, but
  no job runs them and whether this change's answers hold on macOS is
  unproven (N12). This change adds no macOS job: Brett Heap decided on
  2026-10-15 that CI runs on Linux only.
- NOTED residual, argparse colour on 3.14 and later: argparse colours its
  usage and error lines when `FORCE_COLOR` or `PYTHON_COLORS=1` is set, even
  on a pipe (`project --help` at feature 004's `96a08d4`: coloured on 3.14.7
  and 3.15.0rc2, plain on 3.13.15). `tests.yml` sets neither variable and the
  hosted runners do not set them by default, so the widened matrix is
  unaffected (not run in Actions). A local run with either variable set on
  3.14 or later fails feature 004's two "usage: project" assertions at
  `96a08d4`, `tests/test_clean_timing.py:243` and
  `tests/test_clean_batch.py:449`, because its children inherit the
  variable (`tests/clean_support.py:686`); they are the only failures of its
  suite on 3.14.7 with `FORCE_COLOR=1`. As this change's rule says of a
  feature 004 failure on an added version, it is reported to its owner, lane
  openRepoProject-2, which has ruled (lane openRepoProject-2's ruling R-70,
  2026-10-20) that `CleanCase.setUp()` pops both variables and sets
  `NO_COLOR=1` (`tests/clean_support.py:686-691`), not yet on 004 at
  `96a08d4`; a scratch copy with that change passes both assertions. Main's
  `tests/test_project.py` builds its child environment the same way
  (`:133-136` at `e9d6711`) but asserts no argparse text, and its 96 tests
  pass on 3.14.7 and 3.15.0rc2 with either variable set; lane 2 notes that
  line for its T127.
- (L) changes 3.10 to 3.12: a traceback exiting 1 becomes a refusal exiting
  2. S2 changes a destination linked into a directory without search
  permission on 3.10 to 3.13 from `[Errno 13]` to `Destination already
  exists`. (U) changes 3.14 and later for an unsearchable parent and for an
  over-long NAME, family or path: a plan exiting 0 becomes the 3.10 to 3.13
  refusal. No caller relying on any of these is known.
- A later minor version may move pathlib again: S1 and S2 no longer depend on
  it; `known_obstacles()` still does, for parents whose answers agree today
  (Observed). The matrix catches a change only once the version is added,
  and the README calls it untested until then.
- The floor stays on a version whose upstream security support ends in
  October 2026; raising it is a separate decision (R4).

## Out of Scope

- #21's surface: the early non-directory refusal, its sentences, and the
  writability follow-up it names, except the scoping of Decision 12.
- Everything from `discover` down: lane openRepoProject-2's changes
  `add-project-clean-all-safe` (feature 004) and `add-project-overview`
  (feature 005), and feature 004's `git-floor` job.
- Other `resolve()` calls and pathlib reads: `project:54` (registry paths),
  `:87`, `:94`, and everything from `discover` down. One divergence is
  observed and left as a residual: on 3.10 to 3.12, a looped `PROJECTS_DIR`
  with the parent given by `--into` still ends in a `RuntimeError` traceback
  at `projects_dirs()` (`project:79`), reached through `workbenches()`
  (`:90`) on the bench path when `WORKBENCHES_ROOT` and `--workbenches` are
  unset; 3.13 and later refuse with "Cannot find workBenches". A follow-up,
  not this change. A second residual at the same line: a parent with an
  unknown `~user`, such as `--into ~nosuchuser/x`, ends in `RuntimeError:
  Could not determine home directory.`, exit 1, on every version, unpatched
  and patched (council case H), raised by `expanduser()`, which S1's mapping
  does not cover (N9).
- Any new sentence, flag, environment variable or configuration file.
- Raising the floor (R4); a pre-release job (P2, P3) unless Brett Heap
  chooses one; a scheduled release check (A2), which he did not choose
  (Decision 3 is A1, 2026-10-21); `fail-fast` or any other key outside the
  matrix unless he chooses it with lane 2's assent; a macOS or Windows job,
  since CI runs on Linux only by his decision of 2026-10-15 (#32), and the
  README directs Windows to WSL2 (`README.md:282`).
- workBenches, openRepoShape, setup-openspeckit, the archived changes and
  the feature records: other owners' code, or immutable records.

## Decisions for Brett Heap

Ratified by Brett Heap on 2026-10-21, in lane 4's session: "ratify 28,
recommended for SA-2 and SA-7" (quoted on PR #28 at
https://github.com/opensoft/openRepoProject/pull/28#issuecomment-6315794017).
Decisions 1, 2 and 4 to 11 take their recommendations. Decision 12 (SA-2), the
one that turned on lane 1's text, takes its recommendation. Decision 3 (SA-7),
which had no recommendation, he answered when asked, at 2026-10-21T12:05:15Z:
"A1: PR per release (Recommended)". The design and the delta follow every
recommendation, and say what would change under each alternative, none of
which is taken.

1. The versions: R1, every released minor version from 3.10 to 3.15 on
   `ubuntu-latest`, six jobs.
2. The range's form: C1, closed, with later versions called untested.
3. Who adds each new release (chosen by Brett Heap on 2026-10-21T12:05:15Z:
   "A1: PR per release (Recommended)"): A1, an issue and a pull request at
   each CPython final release by the lane that owns `project`, or A2, a
   scheduled check, with lane 2's assent (not chosen).
4. A pre-release: P1, none in CI.
5. The floor: keep 3.10 (R4 deferred).
6. (L)'s answer and place: L1, the system's `ELOOP` refusal, which also
   replaces the 3.10 to 3.12 traceback, after the family-name check (Q1).
7. (U)'s answer: U1, today's 3.10 to 3.13 text on every version, with S2's
   one intended deviation for a destination that is a link.
8. The techniques: T2 at S1 and E1 at S2, accepting the narrow errno reads
   that archived N5 rejected for its own change.
9. The tests: M1, a module of their own.
10. The range's home: H1, the first ADDED requirement, enforced by AC6's
    test (or H2, `README.md` and CI only).
11. `fail-fast`: unchanged (recommended, as the matrix-only agreement
    stands), or `false`, with lane 2's assent.
12. #21's shape sentence and scenario, and its permission sentence, its
    permission scenario and its README permission sentence (SA-2): this
    change MODIFIES and scopes them (recommended, as it needs nothing from
    lane 1), or lane 1 scopes them in #21 before ratification, and the second
    MODIFIED block and the README clause drop (design D6). The recommendation
    is taken (Brett Heap, 2026-10-21): this change MODIFIES and scopes them,
    and nothing drops.

## Review resolution

Alignment review of `0096c98` (stack architect SA-1 to SA-11, QA lead QA-1 to
QA-9; 2 BLOCKER, 9 MAJOR, 9 MINOR). Applied unless marked otherwise:

- SA-1 (3.15 is released): the range is 3.10 to 3.15, twelve jobs; R2, R3,
  the README example, the acceptance criteria, Risks and Decisions follow;
  the pre-release example is 3.16.
- SA-2 (MODIFIED blocks against #21): two MODIFIED blocks, the statements
  record, archive after #21, and reliance on #21's "Preview" WHEN. Its
  preferred route, asking lane 1 to scope #21's shape sentence, is not this
  proposal's to take; it is Decision 12's alternative (since decided: Brett
  Heap took Decision 12's recommendation on 2026-10-21, so this change
  MODIFIES and scopes #21's statements and the alternative is not taken).
- SA-3 (stale #21 pin): every #21 citation is re-pinned to `a43e7d2`, and
  the delta is quoted where it differs from #21's proposal.
- SA-4 (realization order): this realization lands after #21's, as issue #22
  says; "whichever lands second" stays for feature 004 only.
- SA-5 ((L)'s place): after the family-name check (Q1), with the two-fault
  scenario and a row in Feasibility and AC2.
- SA-6 (PARENT on the `PROJECTS_DIR` route): PARENT is built before
  resolution by `Path.absolute()`, and is the same string on every version by
  both routes (Feasibility, AC2).
- SA-7 (open range): closed range (C1). Who opens each release's pull
  request is left open for Brett Heap (Decision 3, A1 or A2) rather than
  named here: lanes are not standing owners, and A2 needs lane 2's assent
  (since decided: Brett Heap chose A1 on 2026-10-21, "A1: PR per release
  (Recommended)", so A2 is not chosen).
- SA-8 (E1 is not 3.10 to 3.12 made explicit): (ii) by taking 3.10 to 3.13
  pathlib's ignored errnos (E1, with the narrower read as rejected E3); (i)
  stated as S2's one intended deviation, with test rows (AC4), and E2 kept
  as the acceptable choice that has no deviation.
- SA-9 (README overlap): overlapping lines, lane 2's acknowledgement
  recorded, and the merged paragraph's order stated. The exact merged text is
  the design's, once both texts are fixed.
- SA-10 (P2's check and landing effects): added to P2.
- SA-11 (`:79` already diverges): named as an observed residual in Out of
  Scope, run in Feasibility.
- QA-1 (over-long component): in the Why, (U), the ADDED scenarios and AC3,
  sized by `PC_NAME_MAX`.
- QA-2 (AC4 cited missing tests): reworded as AC5. The new module checks
  that those parents reach the question, and main's own tests, #21's
  included, pin their answers.
- QA-3 (S2's success branch): AC4 and the ADDED scenario "An existing
  destination is refused as before".
- QA-4 (AC5 not enforced): AC6, a PyYAML test of `tests.yml` against the
  README.
- QA-5 (silent skips, blind snapshot): AC3's skip condition, the no-skip
  check, and snapshots with modes restored.
- QA-6 (CI shape facts): Risks; `fail-fast` is Decision 11.
- QA-7 (borrowing route): composition named, the class name kept out of the
  module, and AC1's count.
- QA-8 (statements record, one scenario title): the "Kept" paragraph, and
  that scenario split into three.
- QA-9 (template): the test-location options are renamed M1 and M2.
  Declined: moving "Ordering and shared files" under Impact as "Dependencies
  and Sequencing" and renaming "Decisions for Brett Heap" to "Open
  Questions". #21, the house template, has neither section; issue #22 and
  lane 2's acknowledgement name "Ordering and shared files"; and "Decisions
  for Brett Heap" says whose decisions they are.

Update, not a review round: main merged in at `e9d6711`, and #21 re-pinned
to `1b84a94`. SA-1's twelve jobs are now six, and SA-3's pin is now
`1b84a94`.

- #32, CI on Linux only (Brett Heap, 2026-10-15): the matrix is
  `ubuntu-latest` x 3.10-3.15, six jobs (What Changes, R1, R2, AC1, Risks,
  Decision 1). R3, the macOS entry, is
  withdrawn but keeps its number. The macOS errno, fixture and runner-patch
  notes are gone. One NOTED macOS residual sits under Risks, and Out of
  Scope names the macOS and Windows jobs. The README example and
  `README.md:281-282` keep #32's "Linux only". The `tests.yml` citations
  follow its lines (`:6-17`, `:9`, `:10`, `:17`), and P2's check name is
  `test (3.16)`. "Ordering and shared files" gains #32 and notes that #21
  and feature 004 still name four jobs.
- #21 at `1b84a94`: its delta is byte-identical to `a43e7d2`'s, so every
  delta line cited here (5-88, 16-20, 36-37, 86-88, 111, 129-198, 148-151,
  153-155, 163-166, 177-180, 187-190) and every quoted base text still match.
  Its proposal grew 20 lines above its Out of Scope with the same text there,
  so line 381 is now 401, lines 392-396 are 412-416, and lines 392-394 are
  412-414. Its first risk, and its reason against a writability read, are
  unchanged.
- Feature 004 at `96a08d4` (re-checked 2026-10-20; the pins were `d1e7c56`
  and `0d3e0f7`): three misquotes are fixed (quickstart.md never said "every
  job of the `test` matrix", plan step 8 is "README and AGENTS.md", and
  `add-project-overview` is feature 005); R-46's wording and the merged
  `git-floor` job are cited on 004's branch, not on `impl/004-t003-git-floor`;
  the pins whose lines held now read `96a08d4`; and the colour residual is
  noted under Risks. Main is at `e45155a`; #16 changed only files under
  `ideation/brainstorm/`, none cited here, so the `e9d6711` citations (this
  branch's merged base) stand.

Council of `461a010`, re-judged against main `e9d6711` and #21 at `1b84a94`
(product-advocate PO-1 to PO-5, systems-architect AR-1 to AR-7,
adversary-engineer AD-1 to AD-7; 19 concerns: VALID 7, NOTED 12, DISMISSED
0; results comment on PR #28, issuecomment-6254996548). Every VALID fix is
applied, and none is declined. The NOTED concerns are N1 to N12 in
`clarifications.md`, each answered by a decision in `design.md`.

- PO-5 (macOS re-added against #32): applied in the update above and checked
  against the council's #32 table row by row. Two of its wordings are taken
  as well: the first ADDED requirement and its scenario name versions, not
  systems ("tested in CI"), and the archived "four CI jobs" quote gains "two
  jobs at `e9d6711`, six after this change". QA-6's macOS facts no longer
  apply.
- AR-6 (`tests.yml` lines and shape after #32): applied in the update above,
  plus the `git-floor` job on feature 004's branch (merged as `4baec61`;
  `tests.yml` at `96a08d4`) in "Ordering and shared files".
- AR-1 (#21's permission statements): its permission sentence (delta lines
  37-43), its scenario (lines 73-76) and its README sentence (its
  `design.md:187-191`) join "Statements this change makes false". The second
  MODIFIED block scopes them to "a directory the person can search but cannot
  write", Decision 12 covers them, and Impact, Out of Scope and Feasibility
  follow.
- AD-1 (every `ENAMETOOLONG` source): (U) names an over-long parent
  component, NAME and `--family` folder, and a whole path past the path
  limit. The third ADDED requirement gains "An over-long name, family or
  path", AC3 gains three rows, and Feasibility and Risks follow.
- AD-2 (PARENT in (U)): (U) names DESTINATION, built on the resolved parent.
  What Changes says that (L) names the parent as given and (U) the resolved
  destination, and AC3 defines DESTINATION.
- PO-1 (Decision 10): Alternatives gains "The range's home" (H1 recommended,
  H2), and Decision 10 cites it.
- AR-4 (PyYAML on 3.15): Observed and Risks say that the 3.15 job builds
  PyYAML 6.0.3 from source (no `cp315` wheel; PyPI read 2026-10-18), and the
  landing task cites its pip log.

Found while writing the delta, not raised by the council: #21's scenario
"The refusal order of an invocation not asked the question is unchanged"
(its delta, lines 196-198) carves out a parent blocked by a non-directory in
its WHEN. A looped or unreadable parent satisfies that WHEN and now gets (L)
or (U), not the generator refusal its THEN names. It joins the statements
record, and the first MODIFIED block's WHEN gains both in the same
carve-out. Two scenarios that presuppose their requirement's earlier
refusals (its delta, lines 69-71 and 158-161) are recorded as kept.
