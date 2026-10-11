Lane: openRepoProject-4

# Proposal: support-later-python-versions

Status: first draft, opened as a draft pull request; the alignment review,
council, design, spec delta and governance tasks follow; nothing is ratified.
Governing issue: opensoft/openRepoProject#22, claimed by lane
openRepoProject-4. Taken up under Brett Heap's word of 2026-10-11 (about
15:55Z), "usage reset, resume all. read handoff and resume and fan out wide
and do as much as possible in parallel", which named no item; lanes
openRepoProject-4 and -5 split the open candidates and this one fell to lane 4
(issue #22, Authority). It lands only on his word ratifying this pull request.

Source: the archived change
`openspec/changes/archive/2026-10-09-fix-parent-obstacle-wording/` recorded
two later-Python residuals in its constraint N1 (`clarifications.md:16-35`)
and in its design's version table and D6 (`design.md:78-93`, `:222-224`), and
kept the CI matrix and the README's "Python 3.10+" out of that change (N5,
`clarifications.md:82-94`; D6, `design.md:225`), "the residual is on a version
CI does not run" (`design.md:100-101`). Issue #20 and its proposal PR #21
(lane openRepoProject-1, head `70d90e6`) put both residuals and the CI matrix
out of scope too (that proposal's Out of Scope, lines 366-370). This change is
where they go.

## Why

`README.md:17-18` says "Python 3.10+ is required", and `AGENTS.md:19` says the
same. CI (`.github/workflows/tests.yml:6-18`) runs the suite on
`ubuntu-latest` and `macos-latest` with Python 3.10 and 3.12 only (`:9-10`).
So 3.11, 3.13 and 3.14 are claimed and never run.

Two parents of `project new` change their answer with the interpreter. Line
numbers here are at this branch's base `961c405`, where the archived record's
`project:315` and `project:321` (at its base `7a9134b`) are `project:322` and
`project:328`:

- **A parent that is a symbolic-link loop.** On 3.10 and 3.12 the parent's
  `Path.resolve()` (`project:322`) raises `RuntimeError` before the question,
  and `main()` does not catch it: its handler takes `Refused` and `OSError`
  only (`project:1143`). By the archived record, on 3.13 and later it no
  longer raises, and the parent reaches the question as a missing parent.
- **A parent beneath a directory without search permission.** On 3.10 and
  3.12 the existing-destination check (`destination.exists()`,
  `project:328`) raises `PermissionError`, which `main()` prints as
  `REFUSED: [Errno 13] Permission denied: '<parent>/<name>'`, exit 2, before
  the question. By the archived record, on 3.14 that read returns False, and
  an existing directory there reaches the question as a missing parent.

That record's later column is "the council's record, not run here"
(`design.md:93`). This change measures it, states the supported range and
tests every version in it, and makes the two parents get one answer on every
supported version.

### Observed

<<OBSERVED: filled from the probe report only>>

## What Changes

- **The supported range** (recommended; Alternatives below): CPython 3.10 and
  every later minor version. `README.md` names the floor and the versions CI
  tests. The `test` job's matrix (`tests.yml:9-10`) runs the full suite on
  3.10, 3.11, 3.12, 3.13 and 3.14, on `ubuntu-latest` and `macos-latest`:
  ten jobs where there are four. A later minor version joins the matrix once
  it is released, by an ordinary pull request under the ADDED requirement
  below. No pre-release runs in CI. The floor stays 3.10, so "3.10+" in
  `README.md` and `AGENTS.md:19` stays true.
- **The two cases**, read on the parent `new()` already computes from
  `--into`, the positional parent, `PROJECTS_DIR` or `~/projects`:
  - (L) **a looped parent**: the parent cannot be resolved because it, or a
    symbolic link on its path, loops. Read as: `resolve()` raises
    `RuntimeError` (3.10 to 3.12), or `os.stat()` of the resolved parent
    fails with `ELOOP` (any version). It covers a link to itself, two links
    to each other, and a missing path below a loop (`LOOP/sub`).
  - (U) **an unreadable destination**: reading the destination
    (`PARENT/NAME`) fails for a reason other than its absence (`ENOENT`,
    `ENOTDIR`). N1's case is `EACCES`, for a parent beneath a directory
    without search permission, or one that is such a directory, whether or
    not the parent exists; the command cannot tell, and does not guess.
- **The answers**, the same on every supported version, before the question
  and before any path's steps, for every route and form: by flag, not asked
  (`CI` set, no terminal, a workspace name), at a terminal with no choosing
  flag, with `--dry-run`, and with `--shape` by flag:
  - (L): `REFUSED: [Errno N] <the system's text for ELOOP>: 'PARENT'`,
    exit 2, printed by `main()`'s existing `OSError` handler, PARENT being
    the parent as given, made absolute and not resolved (a loop has no
    resolved form). No new sentence. This changes 3.10 and 3.12 too: their
    traceback becomes a refusal.
  - (U): today's 3.10 and 3.12 answer, byte for byte:
    `REFUSED: [Errno 13] Permission denied: 'PARENT/NAME'`, exit 2, at the
    existing-destination check, where it is today.
- **The reads, by site** (recommended technique at each; Alternatives below):
  - S1, the parent's resolution (`project:322`, which reaches
    `projects_dirs()` at `project:79` when the parent is `PROJECTS_DIR`):
    the non-strict `resolve()` stays; its `RuntimeError` becomes (L); then
    one `os.stat()` of the resolved parent, of which only `ELOOP` is
    classified, as (L). Every other outcome (success, `ENOENT`, `ENOTDIR`,
    `EACCES`) passes to S2 unchanged. `projects_dirs()` is not edited: its
    other callers (`workbenches()`, `project:90`, and everything from
    `discover`, `project:433`, down) are outside this change.
  - S2, the existing-destination check (`project:328`):
    `destination.exists() or destination.is_symlink()` becomes one
    `os.lstat(destination)`. Success refuses as an existing destination, with
    today's sentence; `FileNotFoundError` and `NotADirectoryError` read as
    absent; any other `OSError` propagates to `main()`, as on 3.10 and 3.12.
    This is the 3.10 to 3.12 outcome made explicit, so that a later pathlib
    cannot move it.
  - Unchanged: `known_obstacles()` (`project:235-254`) and its pathlib reads
    (archived D1), the shape branch's `parent.is_dir()` (`project:371`),
    `parent.mkdir` (`project:398`) and `main()`. They are reached only after
    S1 and S2 have refused both cases.
- **N5, revisited on its merits.** The archived lead rejected "a raw
  `os.stat` classified by errno" for that change because "it would add
  behaviour, strings and a third case beyond the wording follow-up"
  (`clarifications.md:88-92`), and N3 chose `exists()` because it "has the
  same error handling as `is_dir()` on every version" (`:63-65`). Here the
  behaviour is the change's purpose, the recommended answers add no string,
  and the third case, (L), is its subject. N3's premise holds only within a
  version: `exists()` and `is_dir()` share one error handling, and that
  handling is what moved between 3.12 and 3.14 (N1; Observed). An errno from
  `os.stat()` or `os.lstat()` is the operating system's and does not move
  with the interpreter. The classification stays narrow: S1 classifies only
  `ELOOP`, S2 only absence, and everything else keeps today's path.
- **Tests** (recommended; Alternatives below): a module of its own,
  `tests/test_parent_reads.py` (name provisional), found by the existing
  `python -m unittest discover -s tests -v` (`tests.yml:18`). It borrows
  `tests/test_project.py`'s harness (`setUp`, `run_pty`, `run_inproc`, the
  parent fixtures) by importing the module, never by subclassing
  `ProjectTests`, so no existing test runs twice; how it borrows is the
  design's. No line of `tests/test_project.py` changes.
- **`README.md`** (texts fixed by the design, checked by a grep): lines 17-18
  name the floor and the tested versions, for example "Python 3.10 or newer
  is required; CI tests 3.10, 3.11, 3.12, 3.13 and 3.14 on Linux and macOS.";
  lines 281-282 ("CI covers Linux and macOS.") gain the versions.
- **`.github/workflows/tests.yml`**: the `test` job's `python` list
  (`:10`) only. Its `os` list, its steps and every other job are unchanged.

### Alternatives

- **Versions.** (R1) Every released minor version from 3.10 to 3.14 on both
  systems, ten jobs: recommended. (R2) The floor, 3.12 and the newest (3.10,
  3.12, 3.14; six jobs): cheaper, but 3.11 and 3.13 stay claimed and unrun,
  the gap this change closes. (R3) macOS on the floor and the newest only
  (seven jobs): not recommended, since both cases are POSIX symbolic-link and
  permission semantics where macOS differs (`ELOOP` is 62 there and 40 on
  Linux; a temporary directory under `/var` resolves to `/private/var`,
  archived N2). (R4) Raise the floor to 3.11, as upstream security support
  for 3.10 ends in October 2026 (PEP 619): not recommended in this change.
  Ubuntu 22.04's `python3` is 3.10; lane openRepoProject-2's
  `add-project-overview` starts Git children with `start_new_session=True`
  rather than 3.11's `process_group=0` to keep 3.10 (its proposal, "Process
  groups on Python 3.10"); a floor change is its own decision. The
  repository is public and `main`'s ruleset requires no status check (its
  rules are `non_fast_forward`, `deletion` and `pull_request`), so the added
  jobs cost no paid minutes and gate nothing by rule; the landing practice
  reads every job (archived `tasks.md` 3.1, "green checks on all four CI
  jobs").
- **A pre-release, such as 3.15.** (P1) None in CI; a minor version joins at
  its release: recommended. It stays within the `test` job's matrix, the
  edit agreed with lane openRepoProject-2, and a pre-release failure cannot
  gate a merge. (P2) The pre-release as a non-gating entry of the `test`
  job: warning before the release, at the cost of a job that may be red by
  design; it needs keys outside the matrix (`allow-prereleases` on the setup
  step, a job-level `continue-on-error`), so lane 2's assent. (P3) A
  scheduled or manually dispatched pre-release job: a new trigger and job in
  the shared file, beyond the agreement; rejected for this change.
- **(L)'s answer.** (L1) The system's `ELOOP` refusal through `main()`:
  recommended; no new string, the same handler and form as (U). (L2) A fixed
  sentence, such as `The parent PARENT is a symbolic link loop; choose a
  parent that is a directory.`: the same on both systems and states a
  repair, but a new string for the design to fix. (L3) The 3.10 and 3.12
  traceback on every version: an uncaught exception exiting 1, a status the
  README gives to doctor findings (`README.md:284-286`); rejected. (L4) Name
  the loop as an obstacle in the question: it blocks both answers (one
  wasted answer, as #21's first risk), and it edits the requirement "Known
  Triad obstacles are named before the question and refused on a Triad
  answer", which #21 MODIFIES; rejected.
- **(U)'s answer.** (U1) Today's 3.10 and 3.12 text: recommended. (U2) A
  fixed sentence: a new string, and the raw text already names the path and
  the reason. (U3) The 3.14 outcome on every version, the missing-parent
  sentence: false for a directory that exists, and the paths go on to fail
  later (Observed); rejected.
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
- **S2's technique.** (E1) `os.lstat()` classifying absence: recommended.
  (E2) A wrapper reproducing 3.12 pathlib's ignored errnos (`ENOENT`,
  `ENOTDIR`, `EBADF`, `ELOOP`) for `exists()` and `is_symlink()`: the same
  outcome in two reads; acceptable, the design may choose it. (E3) An
  `os.access()` search check of the ancestors: it predicts refusals the
  system may not make (root, ACLs), #21's reason against a writability read;
  rejected.
- **Where the tests go.** (W1) A module of its own: recommended. #21's
  realization rewrites a test and adds `known_obstacle_cases()` rows in the
  `new`-path section of `tests/test_project.py` (`:394-415`, `:1394-1579`),
  and feature 004 edits its clean tests and helpers; a separate module
  touches neither lane's hunks. (W2) The `new`-path section, after
  `test_pty_no_known_obstacle_names_none` (`:1572-1579`): the helpers are at
  hand, at the cost of a merge with #21's realization in the same section.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

`project-command`: three ADDED requirements and no MODIFIED one. Titles are
provisional and distinct from every existing title and from #21's ADDED
requirement.

- ADDED: "Supported Python versions are stated and tested". `README.md`
  names the lowest supported version and the versions CI tests; CI runs the
  full suite on Linux and macOS on every released minor version from the
  lowest to the newest the README names. Scenarios: "A version the README
  names is tested on both systems"; "The lowest supported version is
  3.10".
- ADDED: "A parent that is a symbolic-link loop is refused before the
  question". Its text defines (L), states its answer and its place (after
  the name and the positional-parent check, before the existing-destination
  check), and says it holds on every supported version. Scenarios: "A looped
  parent by each route"; "A missing path below a loop"; "A looped parent's
  dry run"; "A looped parent with the shape chosen by flag"; "A looped
  parent at the terminal is not asked".
- ADDED: "A destination that cannot be read is refused before the
  question". Its text defines (U) and states that the existing-destination
  check refuses it with the system's error, exit 2, on every supported
  version. Scenarios: "An existing directory beneath a directory without
  search permission"; "A missing path beneath one"; "A parent without search
  permission"; "Its dry run, the shape by flag and the terminal".

### Statements this change makes false, and their treatment

None, by this reading of `openspec/specs/project-command/spec.md`. The
closest, for the council:

- "Creation question is asked only of a person choosing at the terminal",
  prose (`:89-92`) and scenario "Refusals before a path is chosen come
  first" (`:127-130`), list the refusals made before a path is chosen: an
  invalid name, a positional parent with `--into`, an existing destination.
  (U) is the existing-destination check's own read. (L) is a new refusal
  before the question; it does not make "the question comes after these"
  false, but the list reads as complete. If the council reads it so, the
  design adds a MODIFIED block for that requirement, written against #21's
  delta text at head `70d90e6`, and this change then archives after
  `refuse-non-directory-parent-early`.
- Same requirement, "Every invocation that is not asked the question SHALL
  keep its existing order of refusals" (`:94-95`): the existing refusals
  keep their order; a looped parent, which had a traceback, now has a
  refusal, first.
- "Delegate project creation", scenario "Preview" (`:25-28`): its WHEN names
  no refusal, as it already does not for an existing destination; #21's
  MODIFIED WHEN ("no refusal precedes its plan") covers both.
- "Known Triad obstacles are named before the question and refused on a
  Triad answer" (`:200-263`): unchanged; a looped or unreadable parent no
  longer reaches its missing-parent sentence on any version.

## Impact

- **`project`**: in `new()`, S1 (`project:322`) and S2 (`project:328`), and
  `import errno` (standard library) for `ELOOP`. Unchanged:
  `projects_dirs()`, `known_obstacles()`, the question, the shape branch,
  `choose()`, `parent.mkdir`, `main()`, and everything from `discover`
  (`project:433`) down. No new sentence, flag, environment variable or
  configuration file.
- **Feasibility**: <<FEASIBILITY: after the report>>
- **Tests**: the new module per the acceptance criteria below; no existing
  test is edited, and every one runs on all ten jobs.
- **`README.md`** lines 17-18 and 281-282; **`.github/workflows/tests.yml`**
  line 10; the spec at archive. `AGENTS.md:19` ("Python 3.10+") stays true
  and is not edited.
- **Feature records** stay unedited. The new feature's spec states that, for
  the two cases, it supersedes feature 003's EC-004
  (`specs/003-parent-obstacle-wording/spec.md:139-142`: on CI's versions a
  loop "errors when the parent is resolved"; later versions print the
  missing sentence), its plan's rows and residual notes (`plan.md:124`,
  `:209-211`, `:272`) and its research note (`research.md:79-81`). The
  archived change is cited, never edited.
- **Speckit handoff**: one feature, numbered when `/speckit.specify` runs
  from a main synced to origin (the next free number; none hard-coded).
- **Handoffs after landing**: no new issue. The realization reaches `onp`
  when workBenches next moves its pin, on its owner's act; whether a comment
  on a workBenches pin issue names it, as archived D5 did, is the design's.

## Ordering and shared files

- **#21 (`refuse-non-directory-parent-early`, lane openRepoProject-1).** This
  change ADDs three requirements and MODIFIES none, so its delta does not
  depend on #21's text and either may archive first. If the design adds the
  one MODIFIED block named above, that block is written against #21's delta
  text at head `70d90e6` and this change archives after
  `refuse-non-directory-parent-early`. #21's surface, the early
  non-directory refusal and its sentences, is not touched. Both realizations
  edit `new()`: this one at `project:322` and `:328`, #21's at the head of
  the bench branch (`project:382-385`) and in `known_obstacles()`
  (`project:235-254`); whichever merges second merges main in. S1 and S2 run
  before #21's head refusal and its question read, so on every version a
  looped or unreadable parent never reaches #21's read, and its Out of Scope
  note on N1 (lines 366-368) stays true. #21's acceptance criteria name 3.10
  and 3.12; if this matrix lands first, its realization runs on five
  versions.
- **Feature 004 (`add-project-clean-all-safe`, lane openRepoProject-2).**
  - `.github/workflows/tests.yml`: this change edits only the `test` job's
    matrix (`:10`); feature 004 adds a separate `git-floor` job and leaves
    the four jobs unchanged (`specs/004-project-clean-all-safe/plan.md`, "CI
    shape").
  - `tests/test_project.py`: this change adds no line to it (W1); feature
    004 edits its clean tests. Under W2 this change's tests would go in the
    `new`-path section only.
  - Whichever change lands second merges main in. Agreed with lane
    openRepoProject-2 on 2026-10-11 (issue #22, "Ordering and shared
    files").
  - `README.md`, not covered by that agreement: feature 004 edits Install
    (`README.md:17-19`, Git 2.36) and the exit-code lines (`:284-286`); this
    change edits `:17-18` and `:281-282`. Adjacent lines of one paragraph:
    the design keeps the Python sentence separate from Git's so the merge is
    mechanical, and this is recorded for lane 2 to acknowledge.
  - The widened matrix runs feature 004's whole suite on 3.11, 3.13 and 3.14
    in either order. If this change lands first, feature 004 must be green on
    ten jobs; if feature 004 lands first, this realization must be. A
    failure of a feature 004 test on an added version is reported to lane 2,
    not fixed here.
- **`add-project-overview` (lane openRepoProject-2)** keeps 3.10
  compatibility by design; keeping the floor keeps that.
- Everything from `discover` down is not touched. No rebase and no force
  push: merges only.

## Acceptance criteria

On every version of the new matrix, on both systems, each by a test:

1. The full suite passes on all ten jobs, with no existing test edited.
2. (L): a symbolic link to itself, two links to each other and `LOOP/sub`,
   each by `--into`, and the first also by the positional parent,
   `PROJECTS_DIR` and the default `~/projects`; each with `--type test
   --yes`, with `--dry-run`, with `--shape --org example --visibility
   private`, not asked (`CI=true`; a non-terminal stdin) and asked (a pty,
   no choosing flag): exit 2, the one (L) line naming the given parent, no
   question line, no `Create:`, and nothing changed (the `rglob` snapshot of
   archived N2).
3. (U): an existing directory beneath a directory of mode 000, a missing
   path beneath it, and a parent of mode 600 (readable, not searchable),
   each by `--into`, with the forms of 2: exit 2,
   `REFUSED: [Errno 13] Permission denied: 'PARENT/MyApp'`, no question line,
   nothing changed; modes restored before cleanup; skipped when
   `os.geteuid() == 0`.
4. The parents that do not change keep today's answer on every version: a
   missing parent, a dangling link, a regular file, a FIFO, `FILE/sub` and a
   link to a directory (the existing tests, now run on every version).
5. The versions `README.md` names as tested and the `test` job's `python`
   list are the same, checked by a grep in the realization's quickstart, as
   feature 003's quickstart checked its README text.
6. Every added line is ASCII (archived N4's scope: added lines, not the
   whole of `project`).

## Risks

- Four jobs become ten; macOS runners queue under a lower concurrency, and
  feature 004's suite runs in each job.
- A test outside this change's surface that fails on an added version
  blocks the widened matrix until its owner fixes it (Observed).
- The (L) line differs by system (`ELOOP` is 40 on Linux, 62 on macOS, with
  each system's text); the tests build it from `errno.ELOOP` and
  `os.strerror()`.
- (L) changes 3.10 and 3.12: a traceback exiting 1 becomes a refusal exiting
  2. No caller relying on the traceback is known.
- A later minor version may move pathlib again: S1 and S2 no longer depend
  on it; `known_obstacles()` still does, for parents whose answers agree
  today (Observed), and the matrix catches a change at release.
- The floor stays on a version whose upstream security support ends in
  October 2026; raising it is a separate decision (R4).

## Out of Scope

- #21's surface: the early non-directory refusal, its sentences, and the
  writability follow-up it names.
- Everything from `discover` down: lane openRepoProject-2's changes
  `add-project-clean-all-safe` and `add-project-overview` (feature 004), and
  feature 004's `git-floor` job.
- Other `resolve()` calls and pathlib reads: `project:54` (registry paths),
  `:87`, `:94`, `projects_dirs()` (`:79`) when `PROJECTS_DIR` is not the
  parent (reached through `workbenches()`, `:90`), and everything from
  `discover` down. Not measured here; a follow-up if evidence shows them
  diverging.
- Any new sentence, flag, environment variable or configuration file.
- Raising the floor (R4); a pre-release job (P2, P3) unless Brett Heap
  chooses one; Windows, where the README directs Bash generators to WSL2
  (`README.md:282`).
- workBenches, openRepoShape, setup-openspeckit, the archived changes and
  the feature records: other owners' code, or immutable records.

## Decisions for Brett Heap

Each has a recommendation above; none is taken.

1. The versions: R1, every released minor version from 3.10 to 3.14 on both
   systems.
2. A pre-release: P1, none in CI.
3. The floor: keep 3.10 (R4 deferred).
4. (L)'s answer: L1, the system's `ELOOP` refusal, which also replaces the
   3.10 and 3.12 traceback.
5. (U)'s answer: U1, today's 3.10 and 3.12 text on every version.
6. The techniques: T2 at S1 and E1 at S2, accepting the narrow errno reads
   that archived N5 rejected for its own change.
7. The tests: W1, a module of their own.
8. Whether the supported range is a spec requirement (the first ADDED
   requirement) or stated only in `README.md` and CI.
