Lane: openRepoProject-2

# Tasks: Safe batch worktree cleanup

**Input**: Design documents from `specs/004-project-clean-all-safe/`

**Prerequisites**: plan.md, spec.md (as reviewed, `aadd709`), research.md (R1
to R15), data-model.md, contracts/project-clean.md and quickstart.md. The
technical design is the ratified change
`openspec/changes/add-project-clean-all-safe/`: design.md D1 to D20 and its
Migration Plan, clarifications.md N1 to N5, and the three spec deltas. It
governs wherever a task is shorter, and where the design and a delta scenario
differ, the scenario governs. The push child follows draft PR #19 (branch
`change/amend-clean-all-safe-push-pins`), as plan.md's LQ-3 assumption and
research.md R1 record. The plan review of `dd923ee` (`plan-review-004`: 2
blockers, 21 majors, 13 minors and 1 unverified finding) and the lead's rulings
R-29 to R-31, from the lead's harness spike (`harness-spike`), are folded in
wherever they change what is built or tested: each task names the finding or
ruling it follows, the plan artifacts take the same fixes in their own round,
and where a finding and a ruling differ, the ruling governs.

**Tests**: Required. FR-066 and SC-012 require at least one automated test
named after each of the 100 delta scenarios: 65 in `project-clean`, 18 in
`project-clean-review-safety` and 17 in `project-command`. PR #19 adds a 101st,
"The push child reaches its remote", tested here under LQ-3 (T074). Each phase
lists its tests first: write them, see them fail, then implement. Every
scenario test task names its scenario by its exact title. A test that pins what
an earlier task built says "pins" and that task's ID; it may pass on arrival,
as feature 002's T054, T055 and T058 did.

**Organization**: Setup, Foundational, then one phase per user story in
spec.md's priority order (US1 to US9), then Polish. Phases start in the order
"Dependencies & Execution Order" gives, which lets US7 and US9 run beside the
other stories.

**Departures from the change's proposal and design**, each stated in the
feature PR body for Brett Heap's word (lead ruling R-32); plan.md follows this
file on both:

- New tests go in new modules, one per foundational lane or story lane, with
  shared helpers in `tests/clean_support.py`; the design's Migration Plan step
  6 and the proposal's Impact name `tests/test_project.py`. That file changes
  in one method (T046, research.md R15) and in one line of its loader (T009,
  lead ruling R-29). If Brett Heap declines, the new modules fold into
  `tests/test_project.py` before the merge.
- `AGENTS.md` gains a clean section (T123); the proposal's Impact lists
  `project`, `README.md` and `tests/test_project.py`, and nothing in the change
  names `AGENTS.md`.

One difference is Brett Heap's own decision, so the PR body only notes it (lead
ruling R-35): the proposal's Impact says the suite runs "on Linux and macOS
with Python 3.10 and 3.12, as CI runs", and since his decision of 2026-10-15
(#32, `e9d6711`) the `test` job runs 3.10 and 3.12 on `ubuntu-latest` only. The
OpenSpec text stays as written; the macOS skips stay in the tests for a local
run, and no task adds a macOS job.

Three arrangements of this file are not departures, because the change leaves
them open: the `git-floor` job's place in Setup (T003; design D17 and Migration
Plan step 4 put the job in feature 004 and name no slice), the named regions
and contract constants of `project` (T004), and `clean()` rewritten once as a
fixed pipeline (T047), so that parallel writers add code in disjoint regions
and functions and their merges do not conflict.

The plan review and rulings R-29 to R-31 change behaviours of the plan as
written at `dd923ee`, among others: the timing table replaced per test by the
test's own factor or table, not by one scale factor (R-29); a child handle that
terminates without blocking, advanced by the driver loop (R-30); a
pseudo-terminal made the push child's controlling terminal for its terminal
tests (R-31); push and delete-branch refusing beside any `inspection-error` row
(B1) and printing their paths through the escaping printer (B2); one signal
scope over the whole `clean` run (M1); and a counting wrapper that records each
child's scrubbed names and process group before it `exec`s Git (M4).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: the task belongs to a lane that runs beside another lane of its
  phase, with a different test module and different functions and regions of
  `project`, which is one file. Tasks within one lane run in order. Each phase
  names its lanes.
- **[Story]**: US1 to US9, from spec.md.
- Every task names its exact repository-relative paths and the `project`
  functions it adds or changes.

## Path Conventions

- `project`, at the repository root, is one file. New code goes only inside the
  region its task names, between the markers T004 adds after `discover()` and
  before `repo_state()`. Existing functions are cited at `961c405`, which this
  branch leaves unchanged for `project`, `tests/` and `README.md` (plan.md,
  "Citations").
- New test modules are `tests/test_clean_<lane>.py` and
  `tests/test_status_doctor_update.py`; helpers are `tests/clean_support.py`,
  and the launcher is `tests/launch_project.py`. Discovery collects neither
  helper file (it takes `test*.py`), and both are importable, because `discover
  -s tests` puts `tests/` on `sys.path`.
- `tests/test_project.py`: one method rewritten (T046) and one line added to
  its loader (T009).
- `README.md`, `AGENTS.md` and `.github/workflows/tests.yml`;
  `specs/004-project-clean-all-safe/` (this file and `traceability.md`); and
  one line of `openspec/changes/add-project-clean-all-safe/tasks.md` (T133). No
  other file changes.

## Rules for every new test

1. Name: `test_clean_`, `test_status_`, `test_doctor_` or `test_update_`, by
   the subcommand the scenario drives, then the scenario's exact title in snake
   case: lower case, each run of characters other than a letter or digit
   replaced by one `_`, with no `_` at either end. "Git older than 2.36"
   becomes `test_clean_git_older_than_2_36`, and "A branch fetched at the merge
   target's tip stays unstarted" becomes
   `test_clean_a_branch_fetched_at_the_merge_target_s_tip_stays_unstarted`. A
   second test of one scenario appends `_` and words naming its clause. A
   `project-command` scenario of "Repository inspection requires Git 2.36 and
   shares one evidence model" names no subcommand, so it takes `test_status_`
   whatever subcommand drives it: "The sixteenth scrubbed name on Git 2.36" and
   the other seven, from "A git that floods standard error" to "A lazy fetch in
   a partial clone is refused locally", so that the floor job's `-k` selection
   runs them (plan review M14). Unit tests start `test_clean_` as well.
2. Modules: unittest matches `-k` against `module.Class.method`, so every
   module named `test_clean_*` or `test_status_*` falls wholly inside the floor
   job's `-k test_clean_ -k test_status_ -k test_doctor_` (checked here on
   Python 3.12: `-k test_clean_` ran a method of a module named
   `test_clean_parsers` whose own name lacks the prefix). A module with another
   prefix would need its own `-k` or a selection by module. Each module has one
   writer, its lane's.
3. Helpers come from `tests/clean_support.py` only. No module binds
   `ProjectTests` in its namespace or uses `import *`, since
   `loadTestsFromModule` would run the 96 tests again. A test patches the
   `project` module object it calls: `tests/clean_support.py` loads its own,
   separate from the one `tests/test_project.py` loads.
4. Fixtures are disposable repositories under the test's temporary directory,
   with `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL` set to a file or
   `os.devnull`, a fixed author and committer, and local bare remotes only; no
   test uses the network.
5. A test that needs the deadline, a budget, the grace, the reap wait or the
   ceiling runs `project` through `tests/launch_project.py` with its own factor
   or table, passed as `--timing=JSON` (lead ruling R-29). No one factor serves
   every test: Python-wrapped probes time out below a factor of 0.1 under load,
   while the 300 s ceiling must fit 20 s. Ceiling and deadline tests use a
   factor of about 0.03 to 0.05, or a table that shortens only what they
   assert, with no Python wrapper; counting tests use the `sh` counting wrapper
   or the real table. Each such test names its factor or table in its body and
   records the probe budget it yields (plan review U1). It asserts ratios and
   ordering (which child was cut, which stage was skipped, that SIGKILL
   followed SIGTERM by at least 0.9 of the grace in force, measured from the
   child), never wall-clock values (R10, R-29). Every test ends inside 20 s,
   `run_cli`'s timeout.
6. Caps are never scaled: 128 and 256 rows, 16 targets, and 64 and 4,096
   records run at their real sizes, with registrations written directly (R11).
7. SIGINT, SIGTERM, SIGHUP and SIGKILL go only to a `project` child process,
   through the launcher or the pseudo-terminal runner, never to the test
   process. An in-process `main()` call restores the previous signal handlers
   and wakeup descriptor even when it raises.
8. Expected human text comes from the D18 and D14 literals of
   `tests/clean_support.py` (T011), never from the design at test time.
9. Skips print their reason: non-UTF-8 paths on macOS (a person's local run, as
   no CI job runs macOS, lead ruling R-35); permission fixtures when
   `os.geteuid() == 0`; and "The sixteenth scrubbed name on Git 2.36" unless
   the `git` on PATH is 2.36 to 2.39.
10. Standard output under `--json` is parsed by one `json.loads`, so it must
    hold exactly one document; under `--apply --json` the human text is
    asserted on standard error.
11. Parity values are literals written into the test (R9), never computed from
    a baseline function or read from history.
12. Of the 96 existing tests only
    `test_clean_revalidates_a_worktree_after_confirmation` is edited (T046),
    and the module's loader gains one `sys.modules` line (T009, R-29). The
    tripwires at `tests/test_project.py:586`, `:615`, `:641`, `:673`, `:736`,
    `:783`, `:857`, `:899`, `:916`, `:978` and `:994` keep passing unchanged
    (research.md R15; impl-slicing-004 section 6).
13. Under the counting wrapper, fixture setup calls the real `git` by its
    absolute path (`REAL_GIT`) or resets the log before the command under test
    runs; the log is parsed by complete records only, never a record still
    being written; and a `doctor` test expects the wrapper's own path in the
    `git` row (lead ruling R-31).
14. A push-child terminal test runs `project` at a pseudo-terminal made its
    controlling terminal (`run_pty_steps(..., controlling_tty=True)`:
    `TIOCSCTTY` after `setsid`), since without one even a child in `project`'s
    own process group cannot open `/dev/tty` (ENXIO). `TIOCSCTTY` is untested
    on macOS, where no CI job runs: a note for a local run there, and a failure
    on macOS goes to the lead before any skip is added (R-31, R-35).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: The baseline, the traceability record, the floor job, and the
regions and contracts every lane writes against.

**Lanes**: T001 first; then T002, T003 and T004, one writer each.

- [x] T001 Confirm the baseline in this worktree: `python3 -m unittest discover
  -s tests -v` runs 96 tests, OK, and `git diff --stat 961c405 -- project tests
  README.md .github` prints nothing.
- [x] T002 [P] Create `specs/004-project-clean-all-safe/traceability.md`, lane
  line first: one row per delta scenario, 101 rows (the 100 of the three delta
  files on `main`, and PR #19's "The push child reaches its remote", marked as
  PR #19's draft), with columns for the delta, the requirement, the exact
  title, the story and the test names. Each test task fills its rows as its
  tests land.
- [x] T003 [P] Add the `git-floor` job to `.github/workflows/tests.yml`
  (FR-067, research.md R11), starting from the lead's ci-spike `workflow.patch`
  (48 added lines, applied with `git apply -p1`; its NOTES.md records the
  build, cache and timing checks): `ubuntu-latest`, Python 3.10,
  `actions/checkout@v4` and `actions/setup-python@v5` as the `test` job pins
  them, `pip install -r requirements.txt`; Git 2.36.6 from kernel.org's
  `git-2.36.6.tar.xz`, checked against sha256
  `3a54356dd0a6b23d7d0742952d5c86958ad8f797cbe41bd1952bc83ec429ea94`
  (quickstart.md), built only on a cache miss with `zlib1g-dev` installed and
  `make -j"$(nproc)" NO_GETTEXT=1 NO_TCLTK=1 NO_PERL=1 NO_PYTHON=1 NO_CURL=1
  NO_OPENSSL=1` into `$HOME/git-floor/2.36.6`, which `actions/cache@v6` keys as
  `git-2.36.6-Linux`; that prefix's `bin` first on `$GITHUB_PATH`; a step that
  fails unless `git --version` prints `git version 2.36.6`; then `python -m
  unittest discover -s tests -v -k test_clean_ -k test_status_ -k
  test_doctor_`, which takes every new module whole by its name (rule 2). Add
  `timeout-minutes: 30` to the new job only (impl-slicing-004 section 8). The
  patch's comment opens "The four jobs above"; it says "The `test` job above"
  instead, since #32 (`e9d6711`) left that job on Python 3.10 and 3.12 on
  `ubuntu-latest` only, with no CI job on macOS (lead ruling R-35). The `test`
  job is untouched; lane openRepoProject-4's issue #22 edits only that job's
  matrix, and whichever change lands second merges `main` in. Check that
  the file parses as YAML, that `actionlint` is clean where it is installed,
  and that the selection runs 15 tests at this commit.
- [x] T004 [P] Add the regions and contracts to `project`, one writer, nothing
  reading them yet. Imports: `errno`, `selectors`, `signal`, `stat`,
  `threading`, `time` and `unicodedata`, all at once. After `discover()` and
  before `repo_state()`, the empty regions `timing`, `contracts`, `git
  environment`, `runner`, `parsers`, `escaping`, `evidence`, `guard`,
  `dispatcher`, `resolution`, `plan`, `gates`, `reflog`, `index`, `preview`,
  `apply`, `result` and `push`, in that order, each opened by `# region NAME`
  and closed by `# endregion NAME`, one blank line between regions. In
  `contracts`: `LIMITS` (128 and 256 rows, 16 targets, 64 ignored entries,
  4,096 records, 8 samples, 64 KiB of reflog, 1 MiB of manifest, 5 revalidation
  and 3 rescan children); `GIT_FLOOR = (2, 36)`; the key tuples of the worktree
  row (the baseline `prunable` included, present only when the registry record
  says `prunable`; plan review M11), `repository`, `merge_target`, the plan
  envelope, a `selected` and an `excluded` entry, the extended error object, a
  target result, `reconciliation` and the apply result record (data-model.md;
  contracts/project-clean.md); `REFUSAL_CODES`, the eighteen; `STAGE_REASONS`
  (data-model.md, "Target stages"); `NOTE_CODES`; `TEXT`, every new D18 and D14
  line with its placeholders, the lines the contract fixes beyond D18 (plan
  review M8: one progress line per target, `  STAGE PATH` or `  STAGE PATH
  (REASON)`; the retained-branch line `Branches kept: B1, B2.`; a message for
  each refusal code that has no baseline message), and the kept baseline texts
  `Cannot remove the current worktree.`, `Worktree is CLASS; only clean merged
  worktrees may be removed.` and the `no-merge-target` message at
  `project:551`; and `NEXT_STEPS`, D18's next step by reason. Only this task
  edits the imports and `contracts`; later lanes read them, and a key change
  goes through the lead. Nothing in `contracts` reads a timing value (R-29).
  The 96 tests still pass.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: In the brief's order: the timing table and the launcher (R10, lead
rulings R-26 and R-29); the counting `git` wrapper and the fake Gits; the
scrubbed environment and the pins; the D2 child handle with its non-blocking
termination (lead ruling R-30), the one-wide driver and the parsers, with the
signal scopes, the filesystem budget, the version check, path escaping and the
reroute of `git()` and `git_text()`; the evidence model behind
`cleanup_report()` only, its parity asserted as literals (research.md R9); and
the `internal-error` guard (R6).

**CRITICAL**: No user story work begins until this phase's checkpoint.

**Lanes**: A, timing (T005 to T007); B, harness (T008 to T011); C, environment
(T012, T013); D, parsers (T014, T015); and E, escaping (T016, T017) start
together. F, runner (T018 to T026), starts when A and C are done; G, evidence
(T027 to T033), when D and F are; H, guard (T034, T035), when T023 is, beside
G. Landing order: A to E, then F, G and H.

### Lane A: the timing table and the launcher

- [ ] T005 [P] Add `tests/test_clean_timing.py`:
  `test_clean_timing_table_holds_every_time_constant` (`TIMING` equals
  `{"invocation_deadline": 60, "reconciliation_reserve": 10, "probe_budget": 5,
  "removal_floor": 5, "removal_ceiling": 300, "inspect_budget": 15,
  "term_grace": 2, "reap_wait": 2, "selector_tick": 0.1}`, and by `ast` its
  assignment in region `timing` is one dict of numeric literals, so no
  environment variable, flag or file feeds it; R10, FR-066);
  `test_clean_timing_is_read_at_call_time` (by `ast` over `project`: `TIMING`
  is read only inside function bodies, never in a default argument, a class
  attribute or a module-level assignment other than its own, and no default
  argument named `grace`, `budget`, `timeout`, `tick` or `wait` holds a number;
  after `TIMING` is replaced on a loaded module, `budget` reports the new
  values; plan review M16, lead ruling R-29); and
  `test_clean_launcher_replaces_the_table` (imported as a module,
  `tests/launch_project.py` given `--timing=JSON` replaces exactly the keys the
  object names and leaves `LIMITS` alone, an unknown key exits nonzero naming
  it, and without `--timing` the real table stands; run as a script with
  `--help` it exits 0 and prints the usage of `project`; the launched process
  is `project`'s own, with its pid, process group, signal handlers, streams and
  exit status).
- [ ] T006 [P] Add `TIMING` to region `timing` of `project`, the values of T005
  in seconds (data-model.md, "Constants"). Every later reader reads
  `TIMING[...]` when it is called, never through a default argument or a
  constant derived at import (plan review M16, R-29). The first two tests of
  T005 pass.
- [ ] T007 [P] Add `tests/launch_project.py`, after the lead's harness spike
  `harness-spike/launch.py` with `parents[1]` for the repository root: load
  `project` with `SourceFileLoader` and `spec_from_loader` under the module
  name `project_cli`, registered in `sys.modules` before `exec_module`, since a
  `@dataclass` under postponed annotations fails without it; when its first
  argument is `--timing=JSON`, replace `TIMING` with a new dict, the real table
  updated by the object's values as floats, refusing an unknown key by name;
  set `sys.argv` to the path of `project` and the remaining arguments, and
  `sys.path[0]` to the repository root, as `python3 project` has them; exit
  with `main(rest)`. Per-test factors and tables replace one scale factor for
  every test (R-29): each test passes the table it names. The spike's other
  pitfalls stand: a default argument or a derived constant keeps its old value,
  and a `DeprecationWarning` prints in a plain run but not under the launcher,
  so new code calls nothing deprecated (`observed_at` comes from
  `time.gmtime()`, not `datetime.utcnow()`). T005 passes.

### Lane B: the counting wrapper, the fake Gits and the helpers

- [ ] T008 [P] Add `tests/test_clean_harness.py`:
  `test_clean_counting_wrapper_records_and_execs` (per child the wrapper
  records, before Git runs, the argument vector as raw bytes, the working
  directory, the pid, the parent pid, the process group, and which of the
  seventeen scrubbed names and `GIT_OPTIONAL_LOCKS` are set; with no hook the
  recorded pid and process group are Git's own, and the exit status and output
  are the real `git`'s; with hooks, `worktree remove` runs the pre-hook, the
  real `git` as a child and the post-hook in that order and exits with Git's
  status; a record still being written is never parsed; plan review M4, lead
  ruling R-31); `test_clean_fake_gits_behave_as_named` (each fake of T011,
  `version-2.35.0` answering `--version` behind the seven pins);
  `test_clean_register_worktrees_writes_valid_rows` (257 rows written directly
  list back through `git worktree list --porcelain -z`);
  `test_clean_pty_runner_gives_a_controlling_terminal` (`run_pty_steps` with
  `controlling_tty=True` runs a command whose own child, in its process group,
  opens `/dev/tty`; without it that child gets ENXIO; R-31); and
  `test_clean_text_fixtures_equal_the_contract_table` (the D18 and D14 literals
  of T011 equal the `TEXT` of `project`: two transcriptions checked against
  each other).
- [x] T009 [P] Create `tests/clean_support.py`: `load_project()`, which loads
  `project` as `tests/test_project.py` does but under its own name,
  `project_clean`, registered in `sys.modules` before `exec_module` (R-29), and
  returns that module object; `REAL_GIT`, the absolute path of the real `git`,
  resolved once before any wrapper goes on PATH;
  `CleanCase(unittest.TestCase)`, with no test methods, whose `setUp` builds
  what `ProjectTests.setUp` builds (`tests/test_project.py:117-136`: a resolved
  temporary base, a fake workBenches, and `self.env` with `WORKBENCHES_ROOT`,
  `HOME`, `PROJECTS_DIR`, `GIT_CONFIG_NOSYSTEM=1` and
  `GIT_CONFIG_GLOBAL=os.devnull`) plus a fixed author and committer;
  `run_cli()` (20 s, `input=""`); `timing_table(factor=None, **values)`, which
  scales every real value by the factor and then sets the named ones, and
  `run_launched(timing, *args)`, which passes that table as `--timing=JSON`
  (R-29); `run_json()`; `git()` and `commit()`, both calling `REAL_GIT` by
  absolute path (R-31); and the skip decorators `linux_paths`, `not_root` and
  `git_236_to_239`. In `tests/test_project.py`'s loader (`:23-26`) add one
  line, `sys.modules[loader.name] = module` before `exec_module`, so that a
  `@dataclass` in `project` loads there too (R-29): it is that file's only edit
  outside T046, and no test there changes.
- [ ] T010 [P] Add the fixture builders to `tests/clean_support.py`: `repo()`;
  `bare_remote()`; `merged_worktree(branch, path=None)`, the recipe of
  `tests/test_project.py:857` copied, not extracted (`worktree add -b`, a
  commit of its own, `push -u`, `merge --no-ff` into the merge target);
  `unstarted_worktree(branch)`; `register_worktrees(count, prefix)`, which
  writes each admin directory's `gitdir`, `commondir` and `HEAD` and each
  worktree's `.git` file directly and creates the branches with one `update-ref
  --stdin` child (R11); reflog surgery (delete, empty, pad past 64 KiB, write
  backdated entries); `gitlink()` and `submodule()`, the test's own `submodule
  add` passing `-c protocol.file.allow=always`; and `run_pty_steps(argv, steps,
  controlling_tty=False)`, the pseudo-terminal runner of
  `tests/test_project.py:210-307` copied and extended with SIGTERM, SIGHUP and
  callable steps, a callable changing the repository while the question waits,
  and with an opt-in controlling terminal: a `preexec_fn` calling
  `fcntl.ioctl(0, termios.TIOCSCTTY, 0)`, which runs after
  `start_new_session`'s `setsid()` (R-31; the spike's
  `harness-spike/prove4_pty.py`). That `preexec_fn` is the test's own;
  `project` never uses one (C4).
- [ ] T011 [P] Add the counting wrapper, the fake Gits and the text fixtures to
  `tests/clean_support.py`. `install_counting_git(bin_dir, log, real=REAL_GIT,
  hooks=None)` writes a POSIX `sh` script after `SH_WRAPPER` in the lead's
  `harness-spike/spike_lib.py` (plan review M4, R-29): before Git runs, it
  appends to `log`, with one `printf`, one record for the child, its fields
  NUL-separated and the record terminated: the pid, the parent pid, the process
  group (from `/proc/$$/stat`, else `ps -o pgid= -p $$`), the working directory
  (`pwd -P`), which of the seventeen scrubbed names and `GIT_OPTIONAL_LOCKS`
  are set (each tested as `${NAME+x}`), and the argument vector. With no hook
  it then `exec`s `real` by absolute path, so the record's pid and process
  group are Git's own; for `worktree remove` with hooks set it runs the
  pre-hook, `real` as a child and the post-hook, and exits with Git's status.
  `child_log(log)` returns the records in the order the children started and
  parses complete records only (R-31). `install_fake_git(bin_dir, kind,
  real=REAL_GIT, **options)` writes a fake, in `sh` wherever the kind allows,
  that can stand behind the counting wrapper as its `real`: `flood-stderr` (70
  KiB on standard error, then a real `status`), `ignore-sigterm` (ignores TERM,
  records its process group, sleeps past any budget, caps its own lifetime),
  `ignored-5000` (5,000 NUL-terminated `!! NAME` records), `version-2.35.0`
  (prints `git version 2.35.0` when `--version` stands anywhere in the argument
  vector, behind the seven pins included, as `case " $* " in *" --version "*)`
  matches it; plan review M21), `remove-noop` (exits 0 without removing),
  `remove-slow` (sleeps, then removes for real), `remove-exit` (exits a given
  status), `status-fails-in`, `status-hangs-in`, `ls-files-fails-in` and
  `ls-files-hangs-in` (for one worktree path), `signal-parent-in` (from the
  status probe of one worktree path, sends a given signal to its parent,
  `project`, then runs the real `status`), `slow-after-remove` (once a
  `worktree remove` has run, its registry and ref listings sleep past any
  budget) and `tty-credential` (for `push`: opens `/dev/tty`, runs the real
  `git credential fill` for `https://example.invalid` so that Git prompts
  there, records whether `/dev/tty` opened, the answers read and the terminal's
  foreground process group, then runs the real push), each passing every other
  command to `real`. A helper that must outlive a kill of the fake's group
  confirms its `setsid()` before the fake goes on, and no fake relies on
  `signal.sigtimedwait`, which macOS lacks (harness spike, item 3). Add
  `path_without_git()` and the D18 and D14 literals, character for character,
  with the contract's lines beyond D18 (M8). T008 passes.

### Lane C: the scrubbed environment and the pins

- [x] T012 [P] Add `tests/test_clean_scrub.py`:
  `test_clean_scrub_removes_the_seventeen_names` (`GIT_SCRUB` is the contract's
  list in its order; from an environment holding all seventeen and
  `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`, `git_env("probe")` keeps those
  two, removes the seventeen and sets `GIT_OPTIONAL_LOCKS=0`; the kinds
  `removal` and `delegate` set no `GIT_OPTIONAL_LOCKS`; the kind `push` keeps
  the caller's `GIT_ALLOW_PROTOCOL` and removes the other sixteen, lead ruling
  R-28; `os.environ` is unchanged) and `test_clean_pins_are_on_every_argv`
  (`git_argv(kind, args)` puts the seven protocol pins on every kind but
  `push`, the two status pins on `status`, `hidden` and `removal`, and builds
  the removal vector exactly as D9 spells it; `push` carries no pin, PR #19).
- [x] T013 [P] Add `GIT_SCRUB`, `PROTOCOL_PINS`, `STATUS_PINS`, `git_env(kind)`
  and `git_argv(kind, args)` to region `git environment` of `project`. T012
  passes.

### Lane D: the parsers

- [x] T014 [P] Add `tests/test_clean_parsers.py` (FR-062, D2): for
  `StatusParser`, `WorktreeListParser`, `RefParser`, `MergedSetParser` and
  `HiddenStateParser`, recorded streams written as byte literals give equal
  records and the same `bound_reached` fed one byte at a time and whole. The
  streams: status records for a modified, an untracked and an ignored file,
  renamed and copied pairs, ` D` deletions, a path holding a line feed and one
  holding 0xFF; registry records for the main worktree, a locked one with a
  reason, a prunable, a bare and a detached one; ref records with a `gone`
  track, `ahead 2, behind 1` and an `origin/HEAD` symref; a merged set; and
  `ls-files -v --stage -z` records tagged `H`, `h` and `S` and one of mode
  `160000`. The status parser stops at the 65th ignored record and at the
  4,097th record; `dirty`, the ignored count, 8 raw samples and the deletion
  flag follow D2 and D4; a truncated last record fails at `finish()`; and no
  parser does I/O (`open`, `os.read` and `subprocess.Popen` patched to fail).
- [x] T015 [P] Add the five parsers to region `parsers` of `project`. T014
  passes.

### Lane E: path escaping

- [x] T016 [P] Add `tests/test_clean_escaping.py` (FR-039 to FR-041):
  `json_path(raw)` returns the text and `True` for valid UTF-8, and through
  `json.dumps` a line feed, a tab, U+0001, U+007F, U+0085, U+200E, U+2028,
  U+202E, U+FEFF and U+E0020 are written as escapes, never raw; an undecodable
  byte becomes `\xHH` in lower case, each literal backslash is doubled, and the
  flag is `False`. `human_path(raw, command=False)` prints a path verbatim in
  prose and `shlex.quote`d in a command, and in the `$'...'` form in both when
  it holds an undecodable byte or a code point whose `unicodedata.category` is
  Cc, Cf, Zl or Zp: `\xHH`, `\uXXXX` and `\UXXXXXXXX` in lower case, each
  backslash doubled, each single quote written `\'`.
- [x] T017 [P] Add `json_path()` and `human_path()` to region `escaping` of
  `project`. T016 passes.

### Lane F: the child handle, the driver and the runner

- [ ] T018 [P] Add `tests/test_clean_runner.py`, its signal cases run in a
  child interpreter that loads `project` as the launcher does, each with its
  own timing table (R-29): `test_clean_child_handle_runs_in_its_own_group` (a
  handle runs in its own session and process group with standard input from
  `/dev/null`, `close_fds` and `git_env(kind)`, as the counting wrapper
  records, and sits in `LIVE_PROBES` while live); `test_clean_driver_outcomes`
  (`complete`; `failed`, with a standard-error head; `complete-at-bound` on the
  `ignored-5000` fake, its child stopped; `timeout` on the `ignore-sigterm`
  fake: SIGTERM, then SIGKILL at least 0.9 of the grace in force later,
  measured from the child, the child reaped, `os.killpg(pgid, 0)` raising
  `ProcessLookupError`, and the handle abandoned and never waited on again;
  `deadline`; and `interrupted`; each outcome mapped to its row error, `failed`
  to `probe-failed`, `timeout` to `probe-timeout` and `deadline` to
  `deadline-exceeded`, while `interrupted` raises `Interrupted`; plan review
  M17); `test_clean_termination_never_blocks` (`terminate_group()` on the
  `ignore-sigterm` fake returns within a tenth of the grace in force, and the
  SIGKILL and the reap come from the driver loop's `advance()` calls; lead
  ruling R-30); `test_clean_a_flooding_child_never_times_out` (the
  `flood-stderr` fake completes, with a head of exactly 4,096 bytes and the
  rest counted); and `test_clean_reaping_uses_popen_only` (a patched
  `os.waitpid` is never called; R14).
- [ ] T019 [P] Add `test_clean_signal_scopes` to `tests/test_clean_runner.py`:
  `signal_scope()` installs record-only handlers for SIGINT, SIGTERM and SIGHUP
  and a non-blocking wakeup descriptor with `warn_on_full_buffer=False`,
  records only the first signal, and restores the previous handlers and
  descriptor on every exit, an exception included; `raising_signals()` raises
  `KeyboardInterrupt` for SIGINT and `Terminated` for SIGTERM and SIGHUP;
  `default_signals()` restores the handlers the process started with (R4); an
  exception inside a scope, `BaseException` included, kills and reaps every
  live probe group; `Interrupted` and `Terminated` are not `Exception`
  subclasses.
- [ ] T020 [P] Add to `tests/test_clean_runner.py`:
  `test_clean_filesystem_calls_are_bounded` (`fs_call(fn, *args, budget=...)`
  returns the value, or re-raises the `OSError`, from a daemon thread, and
  returns a timeout outcome at its budget while the thread stays blocked; never
  a `concurrent.futures` pool); `test_clean_git_version_check`
  (`git_version(run)` reads `git version 2.43.0` and a version with an `(Apple
  Git-N)` suffix, gives `git-too-old` for the `version-2.35.0` fake and
  `git-unavailable` for no `git`, a nonzero exit, a timeout or an unparseable
  line, and spawns one child per invocation); and
  `test_clean_invocation_holds_the_per_run_state` (an `Invocation`, made fresh
  by every `main()` call, holds the per-child budget, 5 s under `clean` and 15
  s otherwise, the clock with its work deadline and reserve, paused while a
  question waits, the probe and removal counters, and the per-invocation memos,
  so nothing carries from one in-process `main()` call to the next, the version
  check's result and the common-directory memos included; plan review M10).
- [ ] T021 [P] Add `test_clean_git_and_git_text_run_through_the_driver` to
  `tests/test_clean_runner.py`: `git()` and `git_text()` run through the
  driver, scrubbed (a `GIT_DIR` naming another repository is ignored), pinned
  and counted, and return what they return today: a `CompletedProcess` with
  text output, and the stripped standard output or `None`, as
  `tests/test_project.py:878` reads in process; outside a subcommand each runs
  one probe with the 15 s budget and installs no signal handler; and once an
  invocation's version check has failed, `git()` returns a failed
  `CompletedProcess` and `git_text()` `None` without spawning, as the counting
  log shows (FR-053, plan review M10).
- [ ] T022 [P] Add `ChildHandle`, `LIVE_PROBES` and `kill_live_probes()` to
  region `runner` of `project`, D2 as lead ruling R-30 amends it: `start`;
  `terminate_group()`, which sends SIGTERM to the group, sets the handle's kill
  deadline from `TIMING["term_grace"]`, read at that call, and returns at once;
  and `advance(now)`, which the driver loop calls on every tick: at the kill
  deadline, or as soon as the leader has exited, SIGKILL to the group with
  `ProcessLookupError` ignored, then a reap deadline from
  `TIMING["reap_wait"]`, past which the handle is abandoned, records
  `probe-timeout` and is never waited on again; `Popen.poll()` and
  `Popen.wait(timeout)` only (R14). Never a blocking `terminate_group()` per
  handle, which stacks graces once several handles run (the spike measured 1.79
  to 2.08 graces late; its `advance_terminations()` in
  `harness-spike/concurrent_driver.py` is the shape). `kill_live_probes()`
  sends SIGTERM to every live group at once and advances them together until
  each is reaped or abandoned. No default argument holds a timing value (plan
  review M16).
- [ ] T023 [P] Add `signal_scope()`, `raising_signals()`, `default_signals()`,
  the signal slot, `Interrupted(BaseException)` and `Terminated(BaseException)`
  to region `runner`.
- [ ] T024 [P] Add to region `runner`: `Invocation`, made fresh by each
  `main()` call (the budget, the clock, the counters and the memos, the version
  check's result among them); `current_invocation()`, for Git callers outside
  `clean`, which outside any subcommand gives the 15 s budget and installs no
  handler (plan review M10); `run_bounded(spec, parser, run)` with D1's loop
  (one selector over both pipes and the wakeup pipe, the tick, the 4 KiB head,
  and `advance()` of every terminating handle on every tick, R-30) and its six
  outcomes, each mapped to its row error (M17); `fs_call()`; and
  `git_version()`. Every timing value is read from `TIMING` when called (R-29).
  T018 to T020 pass.
- [ ] T025 [P] Reroute `git()` and `git_text()` (`project:68-74`) through
  `run_bounded()` with `git_argv("probe", ...)`, keeping their names, place,
  signatures and return values; after a failed version check in the invocation
  they spawn nothing and return a failed `CompletedProcess` and `None` (M10);
  `probe()` stays for the children that are not Git. T021 and the 96 tests
  pass.
- [ ] T026 [P] Add `test_clean_two_handles_share_scrub_termination_and_parsers`
  to `tests/test_clean_runner.py` (SC-004, SC-012, FR-062, N2, R-30), once T015
  has landed, with the spike's table (probe budget 1 s, grace 0.4 s): handles
  started at once and driven from the test's own selector loop, which calls
  `advance()` on every tick: a status probe of a real worktree, the
  `ignore-sigterm` fake, and a second `ignore-sigterm` fake whose budget falls
  due on a later tick, all fed through `StatusParser`; all scrubbed and pinned
  in the counting log; each slow one stopped by `terminate_group()`, getting
  SIGKILL at least 0.9 and under 1.5 graces after its own SIGTERM, measured
  from the child, with no process of its group left (a blocking termination per
  handle measured 1.79 to 2.08); the first one's records equal the one-wide
  driver's for the same worktree.

### Lane G: the evidence model, behind `cleanup_report()` only

- [ ] T027 [P] Add `tests/test_clean_evidence.py` with
  `test_clean_evidence_parity_with_the_baseline_reader` (R9, FR-061): one
  fixture holding the main worktree and an unpublished, a pushed-unmerged, an
  unpushed, a remote-ahead, a diverged, a dirty, an ignored-file, a detached, a
  stale, a merged-removable and a merged-current row; `project clean ROOT
  --json` gives, per row, the literal values written into the test for
  `classification`, `dirty`, `upstream`, `ahead`, `behind`,
  `merged_into_target`, `remote_present` and `current`, and the baseline keys
  with their types, `prunable: true` on the stale row and absent from every
  other (plan review M11). It passes on the baseline reader before T033 and
  must still pass after: it is the parity guard.
- [ ] T028 [P] Add to `tests/test_clean_evidence.py`:
  `test_clean_ladder_is_a_pure_function` (`classify(row, merge_target)` on
  literal rows reaches each of the fifteen classes; an unestablished row is
  `inspection-error` before `protected-default`; the one reorder makes a merged
  row with a deleted upstream `merged-removable`, or `merged-current` when
  current, and an unmerged one `remote-gone`; `review-required` comes only from
  a row the evidence model never builds; the recommendations are those of
  `project:566-616`, verbatim) and `test_clean_partial_removal_note_rules` (D4:
  a present, registration-verified, dirty linked worktree whose records other
  than ignored ones are all ` D` deletions gets `partially-removed`; one
  deletion and one untracked file get none; the main worktree never does; a
  stream stopped at its bound is judged on the records read).
- [ ] T029 [P] Add to `tests/test_clean_evidence.py`:
  `test_clean_evidence_probes_once_per_common_directory` (under the counting
  wrapper, `project clean ROOT --json` runs rows 3, 4, 6 and 7 once each, row
  4b only in a gitfile layout, and one combined status probe per present,
  verified row inside that worktree; every child carries the seven protocol
  pins and every status child the two status pins);
  `test_clean_evidence_checks_registration_both_ways` (a rewritten `.git` file,
  and a changed admin `gitdir` file, each give that row `inspection-error` and
  no status probe); `test_clean_evidence_reads_presence` (`ENOENT` gives
  `present: false`, and so does `ENOTDIR`, a registered path whose parent has
  become a regular file; a parent without search permission gives `present:
  null`, an `os-error` and `inspection-error`; `not_root`; lead ruling R-36);
  and `test_clean_evidence_row_fields` (every row carries `locked`,
  `ignored_files_truncated`, `ignored_samples` as `{path, path_valid_utf8}`
  objects, `path_valid_utf8`, `errors` as `{code, message, path?,
  path_valid_utf8?, reason?}` objects and `notes` as an array of code strings
  (plan review M6, m11); a deleted upstream keeps its configured short name
  with `ahead` and `behind` null).
- [ ] T030 [P] Add the evidence model's scenario tests to
  `tests/test_clean_evidence.py`, each through `project clean ROOT --json` and
  the counting wrapper and each named `test_status_` by rule 1 (FR-054 to
  FR-058; the US9 scenarios that need nothing beyond this lane; plan review
  M14): `test_status_a_git_that_floods_standard_error` (the `flood-stderr`
  fake's probe completes with its records, no `probe-timeout`, its standard
  error capped); `test_status_a_git_that_ignores_sigterm` (launcher, with its
  own table, R-29: the `ignore-sigterm` status probe's group gets SIGKILL at
  least 0.9 of the grace in force after SIGTERM, measured from the child, the
  row is `probe-timeout` and `inspection-error`, and no process of the group
  remains); `test_status_five_thousand_ignored_records` (the probe stops at the
  65th record, `ignored_files: 64`, `ignored_files_truncated: true`, a complete
  outcome, classified `ignored-local-files`);
  `test_status_user_status_configuration` (`status.showUntrackedFiles=no` in
  the `GIT_CONFIG_GLOBAL` file: the combined probe still runs, and a clean
  worktree is classified by the ladder, not `inspection-error`);
  `test_status_a_caller_s_git_environment_is_ignored` (`GIT_DIR`,
  `GIT_WORK_TREE` and `GIT_INDEX_FILE` naming another repository: every probe
  reads the resolved repository and each worktree probe its own index, the
  values equal to a run without them);
  `test_status_the_sixteenth_scrubbed_name_on_git_2_36` (`git_236_to_239`: a
  `GIT_INTERNAL_SUPER_PREFIX` the caller set is removed from every child, and
  the inspection succeeds; the floor job's `-k test_status_` selects it); and
  `test_status_a_lazy_fetch_in_a_partial_clone_is_refused_locally` (a clone
  made with `--no-checkout --filter=tree:0` over `file://` from a source with
  `uploadpack.allowFilter`, its `remote.origin.uploadpack` a script that logs
  each run: the status child carries the seven pins, Git refuses the fetch
  locally, the probe is `probe-failed` and the row `inspection-error`, and the
  script never runs; the same with `GIT_ALLOW_PROTOCOL=file` in the caller's
  environment and `protocol.file.allow=always` in the clone's configuration).
  Scenarios: "A git that floods standard error"; "A git that ignores SIGTERM";
  "Five thousand ignored records"; "User status configuration"; "A caller's Git
  environment is ignored"; "The sixteenth scrubbed name on Git 2.36"; "A lazy
  fetch in a partial clone is refused locally".
- [ ] T031 [P] Add to region `evidence` of `project`: `identity_probe()` (row
  3, repeated one option per child when a value holds a line feed);
  `main_worktree(identity, records, run)`, whose body here takes the first
  registry record (T107 gives it D8's order); `inspect_repository(directory,
  run)` (rows 3, 4, 4b, 5, 6 and 7 through `run_bounded()` and the parsers,
  memoized per common directory on the `Invocation`, returning the identity
  `{root, common_dir, dev, ino}` with the rows' evidence);
  `verify_registration()` and the presence `lstat`, both through `fs_call()`
  (`present` false on `ENOENT` or `ENOTDIR`, null with an `os-error` on any
  other failure, lead ruling R-36); `status_probe()`; and `worktree_rows()`
  (the baseline keys, `prunable` among them where the record says so (M11), and
  the six added fields), each failed driver outcome becoming the row's `errors`
  entry by T024's map (M17).
- [ ] T032 [P] Add to region `evidence`: `classify()` (pure, with its one
  reorder; `RECOMMENDATIONS` from `project:566-616`); `partial_removal_note()`;
  `declared_tracking_branch(root)` (today's `manifest()` read, bounded by
  T108); and `resolve_merge_target(refs, declared)` (`{name, source, sha,
  notes}` in D8's order over row 6; no candidate raises the baseline message of
  `project:551`).
- [ ] T033 [P] Switch `cleanup_report()` (`project:544-622`) onto T031 and
  T032, leaving `repo_state()` alone (R9) and `default_branch()` and
  `ancestor()` in place until T125. T027 to T030 and the 96 tests pass.

### Lane H: the `internal-error` guard

- [ ] T034 [P] Add `tests/test_clean_guard.py`, in process: with
  `cleanup_report` patched to raise `RuntimeError("boom")`, and in a second
  case with `discover` patched the same way under `clean`, `main(["clean",
  ROOT])` returns 2 and prints `REFUSED: RuntimeError: boom`, and with `--json`
  it prints one document, the extended error object (`error`, `code:
  "internal-error"`, `schema_version: 1`, `observed_at`, `mode: "report"`,
  `repository` and `merge_target` null, `completeness: "incomplete"`,
  `apply_allowed: false`, `refusals`), written as `json.dumps(doc, indent=2,
  ensure_ascii=True)` and one newline (plan review M6, m12); `Refused`,
  `Interrupted`, `Terminated`, `KeyboardInterrupt` and `EOFError` pass the
  guard unchanged (M2): `KeyboardInterrupt` and `EOFError` still print
  `Cancelled.` and return 130 with no document, and `Interrupted` raised inside
  `cleanup_report()` with SIGTERM or SIGHUP in the slot returns 143 or 129,
  never `internal-error`; a `RuntimeError` in `snapshot()` under `status` is
  not caught (R6); and `str()` of a `Refused` with a code is its message alone.
- [ ] T035 [P] Give `Refused` (`project:23-24`) the keyword fields `code`,
  `path`, `reason` and `context` (the repository and merge target once
  established) and `as_object()`; add to region `guard` `clean_mode(args)`;
  `run_clean(args)` (before the apply phase, any `Exception` but `Refused`
  becomes the refusal `internal-error`, R6, while `Refused`, `Interrupted`,
  `Terminated`, `KeyboardInterrupt` and `EOFError` pass through unchanged, plan
  review M2); `error_document(exc, args)`, the extended error object for
  `invalid-arguments`, `internal-error` and every resolve refusal (M6); and
  `write_document(doc)`, the one writer of every `clean --json` document:
  `json.dumps(doc, indent=2, ensure_ascii=True)` and one newline (M6). In
  `main()` (`project:1125-1151`), route `clean` through `run_clean()`, print
  `error_document()` for a `clean --json` refusal and `{"error": ...}` for
  every other subcommand as today, and map `Interrupted` and `Terminated` to
  `Cancelled.` on standard error with 130, 143 or 129 and no document. Only
  this task edits `Refused` and `main()`. T034 and the 96 tests pass.

**Checkpoint**: One runner, one evidence model behind `clean`, and the guard;
the 96 tests and every Phase 2 module pass. US1 and US9 can begin.

---

## Phase 3: User Story 1 - Retire every safe worktree in one run

**Priority**: P1. MVP.

**Goal**: `project clean ROOT --all-safe` previews; with `--apply` it builds,
prints and confirms its own fresh plan with one question, removes every
selected worktree in canonical order from the command directory, and keeps
every branch.

**Independent Test**: In a disposable repository with several merged, clean,
published worktrees, each with a commit of its own, beside dirty, locked and
unmerged ones, run the preview, then `--apply` at a pseudo-terminal and with
`--yes`, and compare the removed set with the plan and each branch with its
planned head.

**Lanes**: Tests first, two modules at once: plan (T036 to T040,
`tests/test_clean_batch.py`) and apply (T041 to T046,
`tests/test_clean_apply.py` and the one rewrite in `tests/test_project.py`).
Then T047 alone. Then the plan lane (T048 to T053: regions `dispatcher`,
`plan`, `gates` and `preview`) beside the apply lane (T054 to T057: regions
`apply` and `result`), both writing to T047's stage signatures and T004's key
tuples.

### Tests for User Story 1

- [ ] T036 [P] [US1] Add `test_clean_the_preview_says_what_keeps_each_row` to
  `tests/test_clean_batch.py`: with two rows selected, one excluded as
  `ignored-local-files` and two as `dirty`, the human preview equals the D18
  layout: `Selected (2):` with its `  remove PATH [BRANCH]` lines first, then
  `Excluded (3):` grouped by reason, the groups in gate order and the classes
  in ladder order (plan review M8), each group's `  REASON (K): NEXT STEP` line
  over its `    PATH [BRANCH]` rows, the ignored row adding `: 1 ignored;
  first: SAMPLE`; the rows of each list and group in raw path byte order; the
  residual-window line; and the registry, the branches and the files are
  unchanged. Scenario: "The preview says what keeps each row".
- [ ] T037 [P] [US1] Add to `tests/test_clean_batch.py`:
  `test_clean_plan_digest_mismatch` (a preview with digest D selects P1; when a
  second merged worktree becomes eligible, and again when P1's branch advances,
  `--all-safe --apply --yes --expect-plan D` prints the fresh plan with a
  different digest, refuses with `plan-digest-mismatch` and exit 2, asks
  nothing and runs no `worktree remove`; when only an excluded row changes, the
  digest is still D and the apply proceeds, exit 0) and
  `test_clean_plan_digest_canonical_text` (`plan_digest()` of the fixture
  values of
  `ideation/brainstorm/project-maintenance-batch-cleanup.md:1052-1130` at
  `da33d92`, which the test embeds as literals, is
  `7495756d199ba217f41ed4d648c241c95608b4f353c46952e9a7f4cddc17f3bc`; the mode,
  `observed_at`, `excluded` and the notes leave it unchanged; R12, lead ruling
  R-34). Scenario:
  "Plan digest mismatch".
- [ ] T038 [P] [US1] Add to `tests/test_clean_batch.py`:
  `test_clean_preview_is_advisory` (a preview selects only P1; P1 becomes
  dirty; `--all-safe --apply --yes` builds a fresh plan excluding P1 as
  `dirty`, prints `No eligible worktrees` and exits 0 without asking; with
  `--expect-plan` naming the preview's digest it refuses with
  `plan-digest-mismatch`, exit 2) and `test_clean_paths_and_empty_plans`
  (worktree paths with spaces are selected, shell-quoted in commands and
  removed; an external worktree whose path is missing is excluded as
  `stale-worktree`, and a locked one as `locked-worktree`; a complete plan
  selecting nothing prints `No eligible worktrees` and exits 0 without asking,
  as a preview and under `--apply`; an incomplete plan selecting nothing, from
  an unreadable row (`not_root`), previews with exit 1 and under `--apply`
  prints the plan, then `REFUSED: MESSAGE`, and exits 2 before any question;
  plan review M8). Scenarios: "Preview is advisory"; "Paths and empty plans".
- [ ] T039 [P] [US1] Add to `tests/test_clean_batch.py`:
  `test_clean_invalid_argument_combinations` (`--all-safe` with `--action`,
  `--branch` or `--worktree`; `--expect-plan` without `--all-safe` or without
  `--apply`; and the values `abc`, 63 and 65 hexadecimal digits, and upper-case
  hexadecimal: each refuses with `invalid-arguments` and exit 2, and the
  counting wrapper records no child, not even `git --version`; under `--json`
  the extended error object carries that code; an argument-parser usage error
  prints no JSON) and
  `test_clean_invalid_argument_combinations_unrefused_flags` (flags no row of
  the contract's table refuses keep the baseline's handling: without `--apply`
  or `--all-safe`, `--yes`, `--action`, `--branch` and `--worktree` are ignored
  and the run is a report; an unused `--branch` beside `--apply --action
  remove`, or `--worktree` beside `--apply --action push`, is ignored; plan
  review M9). Scenario: "Invalid argument combinations".
- [ ] T040 [P] [US1] Add to `tests/test_clean_batch.py`:
  `test_clean_first_gates_in_order` (`gate_rows()` on literal rows:
  `main-worktree` before every other gate, `unsupported-path-bytes` before
  `locked-worktree`, `locked-worktree` before the class, `not-requested` only
  in mode single; the first failing gate is the `reason`);
  `test_clean_plan_document_keys` (the keys of `plan_document()` equal the
  contract tuple; each `selected` entry carries the identity objects, the
  baseline signature fields, `locked` and `operation.argv`, which equals
  `git_argv("removal", ...)` for that path); `test_clean_plan_document_bytes`
  (standard output of `--all-safe --json` equals `json.dumps(json.loads(out),
  indent=2, ensure_ascii=True)` and one newline, its keys in the contract's
  order, its plan `notes` `{code, message}` objects and its row `notes` arrays
  of code strings; plan review M6); and
  `test_clean_estimates_are_the_apply_upper_bound` (in every mode, previews and
  reports included, `probes.estimated` is F + W + E + 5T + 3 and
  `operations.estimated` is T, so a preview's `probes.estimated` equals its
  `probes.performed` by the counting log plus 5T + 3; plan review M7).
- [ ] T041 [P] [US1] Add to `tests/test_clean_apply.py`:
  `test_clean_stable_order_and_preserved_work` (three eligible worktrees whose
  raw path order differs from their creation order and whose names differ by
  more than case, beside the current worktree, the merge-target checkout, two
  dirty, a locked, a remote-ahead and an unmerged one: `--all-safe --apply
  --yes` under the counting wrapper removes the three in raw path order and
  keeps the rest, the result names every retained branch, and the log holds no
  `push`, `fetch`, `--force`, `branch -d`, `branch -D`, remote deletion, or
  `worktree prune`, `repair`, `lock` or `unlock`) and
  `test_clean_stable_order_and_preserved_work_target_not_checked_out` (the main
  worktree on another branch, so that the merge-target branch is checked out
  nowhere: every removal names the command directory, and the exit status is
  0). Scenario: "Stable order and preserved work".
- [ ] T042 [P] [US1] Add `test_clean_every_branch_remains_after_a_batch` to
  `tests/test_clean_apply.py`: after `--all-safe --apply --yes`, each selected
  branch is at the SHA the preview's JSON planned, the result reads `Removed N;
  branches kept: B1, B2.`, and the exit status is 0. Scenario: "Every branch
  remains after a batch".
- [ ] T043 [P] [US1] Add `test_clean_only_yes_confirms` to
  `tests/test_clean_apply.py`, through `run_pty_steps`: the answers `y`, an
  empty line and `no` (subtests) each refuse with `cancelled` and exit 2 and
  remove nothing; the question equals `Remove 7 worktrees, keeping 7 branches?
  [yes/N]` for seven rows, and the singular form for one; ` yes ` begins the
  apply phase; under `--json` the question is on standard error and standard
  output holds one document, the plan envelope with `apply_allowed: false` and
  `cancelled` in `refusals` (plan review M6). Scenario: "Only yes confirms".
- [ ] T044 [P] [US1] Add `test_clean_a_noninteractive_batch_needs_yes` to
  `tests/test_clean_apply.py`: with standard input not a terminal and no
  `--yes`, `--all-safe --apply` refuses with `confirmation-required` and exit
  2, removes nothing and prints no question, and under `--json` prints the plan
  envelope with that refusal (M6); with `--yes`, the fresh plan's selection is
  removed with no question, exit 0. Scenario: "A noninteractive batch needs
  --yes".
- [ ] T045 [P] [US1] Add to `tests/test_clean_apply.py`:
  `test_clean_apply_exit_table` (`apply_exit_status()` on literal target lists
  gives each D19 row in its order, Git's status passing through even when it is
  1 or 2) and `test_clean_result_document_keys` (the keys equal the contract
  tuples; `reconciliation` is an object on `removed`, `refused`, `failed` and
  `unknown` targets and null on `not-attempted` ones; `exit_status` is null
  unless a child was spawned and reaped, and 128 plus the signal number when a
  signal ended it, whoever sent it, 137 for a child killed at the ceiling; plan
  review M12).
- [ ] T046 [P] [US1] Rewrite
  `test_clean_revalidates_a_worktree_after_confirmation` in
  `tests/test_project.py` (`:1020-1040`, the only edit to that file;
  research.md R15): the Namespace gains `all_safe=False` and
  `expect_plan=None`, with `json=True` and `yes=False`; standard input reads as
  a terminal; the patched removal question (`ask_removal`) dirties the worktree
  and answers `yes`; `clean(args)` returns 2, the one document's target is
  `refused` with `state-changed`, and the worktree remains.

### Implementation for User Story 1

- [ ] T047 [US1] Rewrite `clean()` (`project:669-743`) once as the fixed
  pipeline, frozen afterwards: later tasks fill stages and never reorder them.
  Build a `CleanRun`, an `Invocation` carrying the arguments, the mode, the
  action (`remove`, `push` or `delete-branch`) and the human stream (standard
  error under `--apply --json`). One `signal_scope()` covers the whole run,
  from the argument checks to its last write (plan review M1): run
  `check_clean_arguments()`, `require_git()`, `resolve_clean_target()`,
  `build_plan()`, `check_plan()` and `print_plan()`, the plan printed before
  any check refuses, as the contract's "Order of a run" requires; then either
  `push_or_delete()`, which swaps in `default_signals()` around `confirm()`
  alone, or `confirm_removal()`, which swaps in `raising_signals()` around the
  question alone, and then `apply_removals()`. The slot is read after planning,
  again before the question and again before the apply phase begins; a signal
  recorded before the apply phase ends the run by FR-036 (probe groups reaped,
  `Cancelled.`, 130, 143 or 129, no document). It is read once more before a
  preview or report exits, so that a signal recorded while it is written exits
  130, 143 or 129 with `Cancelled.` (research.md R4, plan review M1, lead
  ruling R-34). Each stage is a function in its region whose first body is the
  baseline code moved verbatim:
  `resolve_clean_target` (region `resolution`) wraps `discover()`; `build_plan`
  (region `plan`) wraps `cleanup_report()`; `print_plan` (region `preview`)
  calls `print_clean_report()`; `confirm_removal` (region `apply`) calls
  `show_plan()` and `confirm()`; `apply_removals` (region `apply`) calls
  `require_unchanged_cleanup_state()` and `execute()`; `push_or_delete` (region
  `push`) holds `project:680-706` and `:723-743`; and `check_clean_arguments`,
  `require_git` and `check_plan` (region `dispatcher`) keep the baseline
  checks. Arguments are read with `getattr(args, name, default)`. `parser()`
  (`project:1074-1122`) gains `--all-safe` and `--expect-plan D`, its only
  edit. The 96 tests pass, the one T046 rewrites aside.
- [ ] T048 [P] [US1] Fill `check_clean_arguments(args)` (the contract's
  "Argument checks": `invalid-arguments` with the baseline messages kept;
  `--apply --json` accepted only with `--all-safe` or `--action remove`; every
  flag the table does not refuse keeps the baseline's handling, ignored without
  `--apply` and when unused (plan review M9); all before any Git child) and
  `require_git(run)` (`git_version()`, refusing with `git-too-old` or
  `git-unavailable` before resolution, FR-002) in region `dispatcher`. T039
  passes.
- [ ] T049 [P] [US1] Fill `build_plan(repo, run)` in region `plan`: the rows of
  `worktree_rows()`, the main worktree first, then by raw path bytes; the merge
  target and its notes from `resolve_merge_target()`; `gate_rows()`;
  `select_entry()` (the identity objects, the branch evidence, the signature
  fields, `locked`, `operation.argv`); `plan_completeness()`
  (`inspection-incomplete` for an `inspection-error` row or a failed
  repository-wide probe); `apply_allowed`; `refusals`; `limits` and `budget` as
  the values in force; `probes` and `operations`, `estimated` as the upper
  bound for an `--apply` run of this plan in every mode, `probes` F + W + E +
  5T + 3 (F the repository-wide children this invocation ran, W the status
  probes, E the hidden-state probes, T the selected targets) and `operations` T
  (plan review M7), and `performed` from the counters of the `Invocation`; and
  `omitted` as `{count: 0, exactness: "exact"}` until T075. In mode single, P,
  expanded, joined to the working directory and realpath'd by one bounded call,
  names the one registry row whose path equals it, or else the one whose
  realpath does, and otherwise refuses with `worktree-not-found` (M9); it is
  selected alone, and every other eligible row is `not-requested`; in mode
  report the plan is the same, with `apply_allowed: false`.
- [ ] T050 [P] [US1] Fill `gate_rows(rows, plan)` in region `gates`: the ten
  gates of FR-020 as one ordered tuple of gate functions. This task writes
  `main-worktree`, `unsupported-path-bytes`, `locked-worktree`, the class gate
  and `not-requested`, and declares, each in its owner's region with a body
  that passes every row, `registration_gate` and `index_gates` (region `index`,
  filled by T067), `reflog_gate` (region `reflog`, T066) and `deferral_gate`
  (region `gates`, T100). The next steps come from `NEXT_STEPS`, and every
  other class's from its recommendation. The first test of T040 passes.
- [ ] T051 [P] [US1] Fill `plan_digest(plan)` (R12's canonical text) and
  `plan_document(plan)` (the envelope with the baseline keys kept, in the
  contract's key order, every path through `json_path()` beside its flag,
  `observed_at` from `time.gmtime()`, plan `notes` as `{code, message}` objects
  and row `notes` as code strings, written by T035's `write_document()`; plan
  review M6) in region `plan`. The canonical-text test of T037 and the second
  and third tests of T040 pass.
- [ ] T052 [P] [US1] Fill `print_plan(plan, run)` in region `preview`: the
  baseline report layout for modes report and single; the D18 preview layout
  for mode all-safe (the groups in gate order and the classes in ladder order,
  the next steps, the ignored count and first sample, the residual-window line,
  `No eligible worktrees`), and the single-mode layout the contract fixes (plan
  review M8); every path through `human_path()`; and `plan_document()` under
  `--json`, which under `--apply --json` prints only when the run stops before
  the apply phase.
- [ ] T053 [P] [US1] Fill `check_plan(plan, run)` in region `dispatcher`, in
  FR-024's order: an incomplete plan (an all-safe preview exits 1; `--apply`
  refuses with exit 2 and the plan's code before any question; a report still
  exits 0 until T101); an `--expect-plan` mismatch (`plan-digest-mismatch`); a
  complete all-safe plan selecting nothing (`No eligible worktrees`, exit 0);
  in mode single, P excluded by a gate (`target-excluded` with its `reason`,
  and the kept messages for the current worktree and for a class); then
  `confirmation-required` for `--apply` on a standard input that is not a
  terminal, without `--yes`. A plan, select or confirm refusal prints, under
  `--json`, the plan envelope with `apply_allowed: false` and the refusal in
  `refusals`, and otherwise the printed plan, then `REFUSED: MESSAGE` (plan
  review M6, M8). T036 to T040 pass.
- [ ] T054 [P] [US1] Add `ask_removal(plan, run)` and fill `confirm_removal()`
  in region `apply` (R3, FR-026): under `raising_signals()` and with the clock
  paused, write the D18 question, singular for one, to the human stream and
  flush it; read one line by `input()` with no prompt; accept only `yes` with
  its surrounding whitespace stripped, and otherwise refuse with `cancelled`;
  `--yes` accepts the fresh plan without asking.
- [ ] T055 [P] [US1] Add `revalidate(plan, target, run)` to region `apply`,
  with this phase's body: recompute the target's row through the evidence model
  and compare its signature fields, `locked`, the merge target and the
  repository identity with the plan's; any difference refuses the target with
  `state-changed`. T084 replaces the body with D7's targeted check.
- [ ] T056 [P] [US1] Add `run_removal(target, run)`, `rescan(target, run)` and
  `decide_stage()` to region `apply`: the removal child is a `ChildHandle` of
  kind `removal` running the target's planned argument vector from the command
  directory, waited for with no budget; the rescan (identity probe, registry
  listing, ref listing, `lstat` of the path) fills the reconciliation record;
  the stage is `removed` with reason null when the child exited 0 and the entry
  and path are gone, `unknown` with `unconfirmed-removal` when it exited 0
  otherwise, and `failed` with `git-refused` (128), `git-failed` (any other
  status) or `spawn-error`; `exit_status` as T045 states it (plan review M12).
- [ ] T057 [P] [US1] Fill `apply_removals(plan, run)` in region `apply` (per
  target in canonical order: revalidate, spawn, wait, rescan; stop after the
  first target that is not a plain `removed`, later targets `not-attempted`
  with `batch-stopped` and `reconciliation: null`), and add
  `apply_exit_status()` (D19's table), `result_document()` and `print_result()`
  (one progress line per target, `  STAGE PATH` or `  STAGE PATH (REASON)`;
  `Removed N; branches kept: B1, B2.`; the D18 stop block, then `Branches kept:
  B1, B2.` and the residual-window line; plan review M8) to region `result`;
  under `--apply --json` the result document goes to standard output and every
  human line to standard error. T041 to T046 pass.
- [ ] T058 [US1] Run T036 to T046, every Phase 2 module and the 96 tests (95
  unchanged and the one rewritten): all pass.

**Checkpoint**: MVP: preview, `--expect-plan`, one question, ordered removal
with every branch kept, and the named removal on the same path. US2, US3 and
US7 can begin.

---

## Phase 4: User Story 2 - Work not proven disposable is never removed

**Priority**: P1.

**Goal**: The registration, reflog, submodule and hidden-state gates join the
batch and the named removal, each exclusion carrying its first failing gate and
its next step.

**Independent Test**: Build the repository of "Every protected classifier" and
the reflog fixtures, preview and apply, and check that only the plain merged
worktree with a commit of its own is selected and removed, every other row
carrying the reason the gate order gives.

**Lanes**: reflog (T059, T060, T066: `tests/test_clean_reflog.py`, region
`reflog`) beside index (T061 to T065, T067: `tests/test_clean_gates.py`, region
`index`). Both start at US1's checkpoint, beside US3, US7 and US9.

### Tests for User Story 2

- [ ] T059 [P] [US2] Add `test_clean_reflog_gate_outcomes` to
  `tests/test_clean_reflog.py`: `reflog_gate()` on byte literals of the entries
  D10's Context records (a `worktree add -b` creation; that creation, then a
  `commit:` entry; a rename with equal objects; `branch: Reset to`; `fetch
  origin feat:f1: storing head`; an `update-ref` entry with no message; `push`)
  gives D10's outcome for each, pass, `unstarted-branch` or
  `reflog-unavailable`, and a last entry whose new object is not the head gives
  `reflog-unavailable`; `ENOENT`, `ENOTDIR`, 0 bytes and a file of 65,536 bytes
  or more give `reflog-unavailable`, while one of 65,535 bytes is decided by
  its entries (lead ruling R-33, in place of plan review m10); another
  `OSError` gives the row `inspection-error` with an `os-error` in its
  `errors`, and the plan incomplete with `inspection-incomplete` (M5); an
  `fs_call()` timeout leaves the row unprobed and the plan incomplete with
  `inspection-incomplete`, as the delta's outcome rule says (M5's replacement
  text would make that row `inspection-error`; the delta governs).
- [ ] T060 [P] [US2] Add the reflog scenarios to `tests/test_clean_reflog.py`:
  `test_clean_a_published_branch_with_no_commit_of_its_own` (`worktree add -b
  x`, `push -u`, no commit: `--all-safe` excludes it as `unstarted-branch`;
  `--apply --action remove --worktree` refuses with `target-excluded`, reason
  `unstarted-branch`, exit 2; after `git branch -m x y` it is still
  `unstarted-branch`);
  `test_clean_a_fast_forward_merged_branch_at_the_target_s_tip_stays_eligible`
  (a commit, then the merge target fast-forwarded to it: the commit follows the
  creation entry, `--all-safe` selects it, and `--all-safe --apply --yes`
  removes it);
  `test_clean_a_branch_reset_to_the_merge_target_s_tip_stays_unstarted`
  (`worktree add -B` over a branch with commits of its own);
  `test_clean_a_branch_fetched_at_the_merge_target_s_tip_stays_unstarted`
  (`fetch origin feat:f1`, then `branch -u origin/feat f1`, and the
  `update-ref` and `push .` variants); and
  `test_clean_a_branch_whose_reflog_is_missing_empty_or_expired` (a head that
  is a strict ancestor with no reflog, a head equal to the target's SHA, a
  0-byte file, and `reflog expire` leaving only a rename entry: each
  `reflog-unavailable`; `--worktree` refuses with `target-excluded`, reason
  `reflog-unavailable`, exit 2). Scenarios: "A published branch with no commit
  of its own"; "A fast-forward-merged branch at the target's tip stays
  eligible"; "A branch reset to the merge target's tip stays unstarted"; "A
  branch fetched at the merge target's tip stays unstarted"; "A branch whose
  reflog is missing, empty or expired".
- [ ] T061 [P] [US2] Add to `tests/test_clean_gates.py`:
  `test_clean_every_protected_classifier` (linked worktrees that are stale,
  detached, dirty, holding ignored files, unpublished, remote-gone, diverged,
  remote-ahead, unpushed, pushed-unmerged, merged but current, merged but
  locked, merged with a non-UTF-8 path (that row under `linux_paths`), merged
  with an initialized submodule and merged with an assume-unchanged entry,
  beside the main worktree on the merge target and one plain merged, clean,
  published worktree with a commit of its own: only that one is selected and
  removed, every other row excluded with the reason the gate order gives,
  written as a literal map from path to reason, exit 0) and
  `test_clean_every_protected_classifier_incomplete_copy` (a copy adding an
  unreadable worktree, and one adding a broken admin registration:
  `inspection-error`, an incomplete plan, exit 2 under `--apply`, nothing
  removed). Scenario: "Every protected classifier".
- [ ] T062 [P] [US2] Add to `tests/test_clean_gates.py`:
  `test_clean_hidden_local_state` (two otherwise eligible worktrees, one
  holding an edit to a file flagged assume-unchanged and one a file flagged
  skip-worktree through `git sparse-checkout set`, each flag in that worktree's
  own index while the main worktree's index flags nothing: the preview excludes
  both as `hidden-local-state`, and the edits survive an apply of the rest);
  `test_clean_an_edit_hidden_by_assume_unchanged_survives` (a merged, clean,
  published worktree whose only change is an assume-unchanged edit, named by
  `--worktree` with `--yes`: `target-excluded`, reason `hidden-local-state`,
  exit 2, and the edit survives); and `test_clean_index_gate_reads_that_fail`
  (on an otherwise eligible row, in turn: the `ls-files-fails-in` fake; the
  `ls-files-hangs-in` fake under the launcher, with a table that shortens the
  probe budget to no less than 1 s; and, in process, `modules_check()`'s
  filesystem call made to raise `PermissionError` and then to time out: that
  row `inspection-error` with `probe-failed`, `probe-timeout` or `os-error` in
  its `errors`, the plan incomplete with `inspection-incomplete`, the preview
  exit 1, `--apply` exit 2, nothing removed; plan review M5). Scenarios:
  "Hidden local state", whose after-confirmation clause is T083's; "An edit
  hidden by assume-unchanged survives".
- [ ] T063 [P] [US2] Add to `tests/test_clean_gates.py`:
  `test_clean_submodules` (otherwise eligible worktrees holding an initialized
  submodule, a submodule initialized then deinitialized, a gitlink never
  initialized, and an admin `modules` entry left after the gitlink was removed,
  beside one plain eligible worktree: the four are excluded as
  `contains-submodule`, and an apply removes only the plain one) and
  `test_clean_a_worktree_holding_a_submodule_is_never_offered` (a populated
  submodule named by `--worktree` with `--yes`: `target-excluded`, reason
  `contains-submodule`, exit 2, and the counting log holds no `worktree
  remove`). Scenarios: "Submodules", whose after-confirmation clause is T083's;
  "A worktree holding a submodule is never offered".
- [ ] T064 [P] [US2] Add to `tests/test_clean_gates.py`:
  `test_clean_a_merged_worktree_whose_upstream_was_deleted` (a clean, merged
  worktree with a commit of its own and a deleted remote-tracking upstream is
  `merged-removable` with that class's recommendation, `--all-safe` selects it,
  and `--worktree` with `--yes` removes it and keeps its branch; an unmerged
  one with a deleted upstream is `remote-gone` and preserved) and
  `test_clean_a_deleted_upstream_is_remote_gone` (an unmerged branch with a
  deleted upstream is `remote-gone` and one with no upstream `unpublished`,
  both preserved). They pin T032, T049 and T057. Scenarios: "A merged worktree
  whose upstream was deleted"; "A deleted upstream is remote-gone".
- [ ] T065 [P] [US2] Add to `tests/test_clean_gates.py`:
  `test_clean_dirty_or_unmerged_work_is_preserved` (the report marks dirty and
  unmerged rows for preservation or review and proposes no destructive action);
  `test_clean_a_merged_worktree_has_ignored_local_files` (a non-current merged
  worktree holding an ignored file is a preservation state, and its removal is
  refused); `test_clean_default_branch_cannot_be_established_locally` (no
  manifest `tracking_branch`, no `origin/HEAD`, neither `main` nor `master`:
  refused, never guessed from the current branch);
  `test_clean_pushed_feature_branch_has_an_open_review_path` (a clean branch
  with an upstream, not merged: the report names the normal pull-request or
  merge process, and the worktree and branch remain); and
  `test_clean_the_main_worktree_and_a_locked_worktree` (`--worktree` naming the
  main worktree, and a merged, clean, published, locked one: `target-excluded`,
  reasons `main-worktree` and `locked-worktree`, exit 2, nothing removed). The
  first four are canonical scenarios the change keeps (SC-011); all five pin
  T050 and T053. Scenarios: "Dirty or unmerged work is preserved"; "A merged
  worktree has ignored local files"; "Default branch cannot be established
  locally"; "Pushed feature branch has an open review path"; "The main worktree
  and a locked worktree".

### Implementation for User Story 2

- [ ] T066 [P] [US2] Fill `reflog_gate(common_dir, branch, head, run)` in
  region `reflog` (D10, FR-021, FR-022): one `fs_call()` read of
  `logs/refs/heads/<branch>` under the common directory, each `/` of the branch
  name a directory level, at most 64 KiB (the read asks for no more than 65,536
  bytes, so it needs no `fstat`), a read that returns 65,536 bytes having
  reached the bound (R-33), and never by a Git child; the anchor (the last
  entry whose old object is all zeros, or whose message begins `branch: Created
  from` or `branch: Reset to`), the movement (an entry after the anchor, or any
  entry when none survives, whose old and new objects are non-zero and differ),
  the head test and the outcome rule; it runs for every row that reaches gate
  7, in every mode. A read error other than `ENOENT` or `ENOTDIR` makes the row
  `inspection-error` with `os-error`, and a timeout leaves it unprobed, the
  plan incomplete with `inspection-incomplete` either way (plan review M5, as
  the delta words it). T059 and T060 pass.
- [ ] T067 [P] [US2] Fill in region `index`: `registration_gate`, gate 3, from
  the row's two-way registration result; and `index_gates`, gates 9 and 10, for
  rows that passed gates 1 to 8 only: `contains-submodule` from
  `modules_check()` (an `fs_call()` on
  `<common_dir>/worktrees/<admin_id>/modules`) and from a gitlink among
  `hidden_state_probe()`'s records, and `hidden-local-state` from an entry
  flagged assume-unchanged or skip-worktree, where `hidden_state_probe()` runs
  `ls-files -v --stage -z` with the status pins inside the row's worktree
  through `HiddenStateParser`. A `modules_check()` that fails or times out, or
  a `hidden_state_probe()` that fails, times out or meets the deadline, makes
  the row `inspection-error` with `os-error`, `probe-failed`, `probe-timeout`
  or `deadline-exceeded` in its `errors`, and the plan incomplete with
  `inspection-incomplete`; a null flag never passes a gate (plan review M5).
  T061 to T065 pass.
- [ ] T068 [US2] Run the US2 modules, every earlier module and the 96 tests:
  all pass.

**Checkpoint**: Only work proven disposable is offered; every other row says
which gate kept it and what to do.

---

## Phase 5: User Story 3 - A named action gains the batch's checks

**Priority**: P1.

**Goal**: `--apply --action remove --worktree P` is a one-item batch, complete
on P's own evidence beside an unreadable row, among seventeen eligible rows and
past the row cap; push and branch deletion keep their flags, refuse a deleted
upstream and an incomplete inspection, another row's `inspection-error`
included (plan review B1), print their paths escaped (B2), pass no signal on to
their children (M3), and run those children as research.md R1 and R5 set.

**Independent Test**: In two fresh copies of a repository whose only eligible
worktree is P, run `--worktree P --yes` in one and `--all-safe --apply --yes`
in the other and compare plans, argument vectors and results; then name P
beside an unreadable row, among seventeen eligible rows and above 128 rows, and
apply pushes against a deleted upstream and an incomplete inspection.

**Lanes**: single (T069 to T071, T075: `tests/test_clean_single.py`,
`build_plan()` in region `plan`) beside push (T072, T073, T074, T076, T077:
`tests/test_clean_push.py`, region `push`, `execute()` and
`require_unchanged_cleanup_state()`). Both start at US1's checkpoint, beside
US2, US7 and US9.

### Tests for User Story 3

- [ ] T069 [P] [US3] Add `test_clean_single_target_equals_a_one_item_batch` to
  `tests/test_clean_single.py`: two fresh copies of a repository whose only
  eligible worktree is P, used in turn at one path: `--apply --action remove
  --worktree P --yes` and `--all-safe --apply --yes` show the same `selected`
  entry for P apart from `dev` and `ino`, run the same argument vector by the
  counting log, and end with P `removed` and exit 0; P made dirty between
  confirmation and revalidation, through the question hook, refuses both with
  `state-changed`, the same message and exit 2; with another worktree
  unreadable (`not_root`), the batch refuses with `inspection-incomplete` while
  the named removal removes P; an unregistered path gives `worktree-not-found`,
  and a dirty worktree `target-excluded` with `reason: "dirty"`. Scenario:
  "Single target equals a one-item batch".
- [ ] T070 [P] [US3] Add to `tests/test_clean_single.py`:
  `test_clean_a_named_removal_beside_another_row_s_inspection_error` (P
  removed, the other row a non-blocking `inspection-incomplete` note, exit 0);
  `test_clean_a_named_removal_among_seventeen_eligible_rows` (P removed, the
  other sixteen `not-requested`, exit 0); and
  `test_clean_a_named_removal_beyond_the_row_cap` (130 rows registered
  directly, P sorting after the first 128: P's status probe is the first status
  child in the counting log, P is removed, and `omitted` counts the uninspected
  rows under a non-blocking `inspect-cap` note, exit 0). Scenarios: "A named
  removal beside another row's inspection error"; "A named removal among
  seventeen eligible rows"; "A named removal beyond the row cap".
- [ ] T071 [P] [US3] Add `test_clean_remove_a_merged_clean_worktree` to
  `tests/test_clean_single.py`: at a pseudo-terminal, the D18 question in the
  singular, then `yes`: the worktree is removed and its branch kept; only a
  separate `--action delete-branch` deletes the branch. It pins T054 and T057.
  Scenario: "Remove a merged clean worktree".
- [ ] T072 [P] [US3] Add to `tests/test_clean_push.py`, every pseudo-terminal
  run with `controlling_tty=True` (rule 14):
  `test_clean_push_an_unpushed_feature_branch` (the exact push plan shown,
  confirmed through `Type yes`, pushed without `--force` by the counting log; a
  push the remote rejects through a `pre-receive` hook leaves every local ref
  as it was); `test_clean_push_refuses_a_branch_whose_upstream_was_deleted`
  (merged and unmerged variants: reason `remote-gone`, exit 2, no push child in
  the log); `test_clean_push_refuses_an_incomplete_inspection` (another row
  `inspection-error` through `status-fails-in`: `inspection-incomplete`, exit
  2, no push child; the same for `--action delete-branch`, with no `branch -d`
  child; and at a pseudo-terminal, a callable step removing search permission
  from another worktree's parent while `Type yes` waits, then `yes`: refused
  after confirmation with `inspection-incomplete`, exit 2, no delegate,
  `not_root`; plan review B1; the deadline clause is T098's); and
  `test_clean_push_and_branch_deletion_stay_human_only` (`--apply --json` with
  `--action push` or `--action delete-branch`: `invalid-arguments`, exit 2, no
  child; it pins T048). Scenarios: "Push an unpushed feature branch"; "Push
  refuses a branch whose upstream was deleted"; "Push refuses an incomplete
  inspection"; "Push and branch deletion stay human-only".
- [ ] T073 [P] [US3] Add to `tests/test_clean_push.py`:
  `test_clean_a_signal_during_the_push_or_branch_deletion` (launcher, the real
  table: SIGTERM, and in turn SIGINT and SIGHUP, sent to `project` alone while
  a `pre-push` hook sleeps, and while a `reference-transaction` hook of `git
  branch -d` sleeps: the hook records that no signal reached it, the child is
  waited for and completes, `origin` holds the branch or the branch is gone,
  and `project` exits 143, 130 or 129; with no signal to `project`, the child's
  own status passes through, and a hook that ends its own `git` with SIGKILL
  gives 137; plan review M3) and
  `test_clean_push_and_delete_branch_escape_their_paths` (a repository root
  holding a tab and U+202E, written as the escape `\u202e` in the test's
  source: `--action push` and `--action delete-branch` print `Working
  directory:` and the command with the root in the `$'...'` form and never the
  raw code points; plan review B2, FR-041, SC-010).
- [ ] T074 [P] [US3] Add to `tests/test_clean_push.py` (PR #19; plan.md LQ-3;
  research.md R1): `test_clean_the_push_child_reaches_its_remote` (`project
  clean ROOT --apply --action push --branch B --yes`, with ROOT the main
  worktree's absolute path, run in its own session with `GIT_DIR` naming
  another repository and `GIT_CONFIG_PARAMETERS` set in its environment, for a
  clean feature branch B the push accepts (not the default branch, `origin/B`
  present, lacking a commit B holds and holding none B lacks, no other row
  `inspection-error`), `origin` a local path. The counting log shows the push
  child with none of the seven pins and with the seventeen names but
  `GIT_ALLOW_PROTOCOL` removed, and all seven pins on every other child; the
  push child's process group is `project`'s, and every other child's is its
  own; the push exits 0 and `origin` holds B at its local commit. With a
  `pre-push` hook that sleeps 7 s, unscaled, the push still exits 0, `origin`
  holds B, and the hook records that no signal reached it; the `sh` counting
  wrapper keeps the run inside 20 s (R-29). A `GIT_ALLOW_PROTOCOL` the caller
  set reaches the push child (R-28).) and
  `test_clean_the_push_child_reaches_its_remote_at_a_terminal` (at a
  pseudo-terminal made the controlling terminal (R-31), with `--yes`: the
  `tty-credential` fake behind the counting wrapper opens `/dev/tty`, Git's
  username and password prompts are answered through the pseudo-terminal, the
  terminal's foreground process group is the push child's, which is
  `project`'s, and the push lands; ^C typed at the username prompt interrupts
  the push, nothing is pushed, and `project` prints `Cancelled.` and exits 130,
  by D19's first row (plan review M3)). Scenario: "The push child reaches its
  remote" (PR #19, draft).

### Implementation for User Story 3

- [ ] T075 [P] [US3] Fill in `build_plan()` (region `plan`; FR-013, FR-031,
  D13): the registry read whole in one child before any cap; the row caps (128
  in modes all-safe and single, 256 in mode report, every registry entry
  counting, the main worktree and missing rows included); rows past the cap
  left uninspected and counted in `omitted` with `exactness: "exact"`; an
  all-safe plan past its cap incomplete with `inspect-cap`; and mode single: P
  matched against the whole registry and inspected first, exempt from the cap,
  the limit of 16 counting P alone, and another row's `inspection-error`,
  omission by the cap or being left unprobed recorded as the non-blocking notes
  `inspection-incomplete`, `inspect-cap` and `deadline-exceeded`, while P's own
  evidence stays strict. These non-blocking notes serve `--action remove`
  alone: a single plan built for push or delete-branch (the `Invocation`'s
  action) keeps the cap and the bounds with the batch's completeness, so
  another row's `inspection-error`, the cap or the deadline makes it incomplete
  (plan review B1). A report above 128 rows is T101's. T069 and T070 pass.
- [ ] T076 [P] [US3] Fill `push_or_delete()` in region `push` (FR-010, FR-041,
  FR-046, FR-047): both actions resolve through the pipeline and plan in mode
  single for the cap and the bounds, with the batch's completeness (T075; plan
  review B1); `require_unchanged_cleanup_state()` (`project:656-666`)
  re-inspects fully, before and after confirmation, through `build_plan()`, and
  refuses with `inspection-incomplete`, `inspect-cap` or `deadline-exceeded`,
  exit 2, when either inspection is incomplete, another row's
  `inspection-error` included; add `show_push_plan()`, which prints `Working
  directory:` and the command as `show_plan()` does but each path through
  `human_path()`, so that a root holding a Cc, Cf, Zl or Zp code point prints
  in the `$'...'` form (B2), while `show_plan()` stays as it is for `new` and
  `update`; `confirm()` stays as it is, under `default_signals()` alone (R4,
  M1); push refuses a branch whose configured upstream's remote-tracking ref is
  gone, whatever its class, naming the reason `remote-gone`; delete-branch
  reads the branch head from row 6 and merged-ness from row 7 instead of
  calling `ancestor()`; `remote get-url origin` runs through the driver; and
  the run exits by D19's first row: 130, 143 or 129 when a signal was recorded
  while the child ran, otherwise the child's status, 128 plus the signal number
  for a signal death, and 2 for a refusal (M3).
- [ ] T077 [P] [US3] `execute()` (`project:157-162`) gains only an optional
  `env` argument. The push child runs as `execute(["git", "-C", ROOT, "push",
  ...], env=git_env("push"))`: no pins, `project`'s own streams and process
  group, never signalled, unbounded, under `signal_scope()`, so that a signal
  reaching `project` is only recorded while the push, in the terminal's
  foreground, takes the terminal's own (R1, R4, PR #19). The delete-branch
  child `git branch -d BRANCH` runs as a `ChildHandle` of kind `delegate` on
  the driver (the scrub, the seven pins, its own group, no budget), its output
  relayed to `project`'s streams and a signal death mapped to 128 plus its
  number (R5); a set signal slot never stops a `delegate` handle, which is
  waited for, so a signal is recorded and passed on to neither child (plan
  review M3). T072, T073, T074 and `tests/test_project.py:899`, `:978` and
  `:994` pass.
- [ ] T078 [US3] Run the US3 modules, every earlier module and the 96 tests:
  all pass.

**Checkpoint**: The named removal is a one-item batch; push and branch deletion
keep their flags and gain their refusals.

---

## Phase 6: User Story 4 - A change after the plan stops the removal

**Priority**: P2.

**Goal**: Before each removal, a targeted revalidation of at most five Git
children compares the recorded identities and evidence and refuses at the first
difference; the rescan after a removal re-establishes the repository first and
reports a branch race without losing a commit.

**Independent Test**: With hooks at the question, between revalidation and
removal, and between Git's removal and the rescan, change the target, its
registration, its branch, the merge target, the manifest or the repository, and
check each target's stage, reason and reconciliation and the exit status.

**Lanes**: one, `tests/test_clean_revalidation.py` and region `apply`
(`revalidate()`, `rescan()`, `decide_stage()`). It starts after US2, whose
`modules_check()` and `hidden_state_probe()` revalidation calls, beside US5's
text lane, US3, US7 and US9.

### Tests for User Story 4

- [ ] T079 [US4] Add to `tests/test_clean_revalidation.py`:
  `test_clean_worktree_changes_while_confirmation_is_pending` (the question
  hook dirties the selected worktree: `refused`, `state-changed`, exit 2, the
  worktree preserved); `test_clean_new_worktree_and_pre_removal_changes` (a
  linked worktree registered at the question is not selected; and in turn a
  changed merge-target SHA, feature branch tip, upstream object, lock,
  ignored-file state or classification of a target before the first removal: no
  mutation, exit 2, the matching reason); and `test_clean_changed_later_target`
  (target 2 changed by the counting wrapper's post-remove hook on target 1: the
  run stops at target 2, and the record shows target 1 `removed` and every
  retained branch). Scenarios: "Worktree changes while confirmation is
  pending"; "New worktree and pre-removal changes"; "Changed later target".
- [ ] T080 [US4] Add to `tests/test_clean_revalidation.py`:
  `test_clean_target_directory_replaced` (at the question, the first target
  moved aside and a new directory put at its path, and in a second run a
  symlink: `refused` with `identity-changed`, no child spawned, later targets
  `not-attempted`, exit 2); `test_clean_admin_registration_changed` (the
  target's `.git` file rewritten to name another admin directory, and in a
  second run its admin `gitdir` file changed: `identity-changed`, exit 2; a
  fresh plan then shows the row as `registration-mismatch` with classification
  `inspection-error`, incomplete); and `test_clean_parent_directory_swapped`
  (the directory holding the target replaced by a symlink to a copy of it:
  `identity-changed`, exit 2). Scenarios: "Target directory replaced"; "Admin
  registration changed"; "Parent directory swapped".
- [ ] T081 [US4] Add to `tests/test_clean_revalidation.py`:
  `test_clean_state_changes_before_revalidation` (at the question, in turn: an
  ignored file created in the target, a commit on the merge target, the
  manifest's `tracking_branch` edited to another existing branch, the manifest
  made unparseable: `refused` with `state-changed`, exit 2, and nothing
  removed, since the preflight finds it; then, for a plan resolved through
  `origin/HEAD`, the manifest gaining `tracking_branch: release`, an existing
  branch the narrowed listing does not name, and `refs/remotes/origin/HEAD`
  repointed to another existing branch: the same);
  `test_clean_branch_advances_before_removal` (a commit on the target's branch
  at the question: `refused` with `branch-changed` at the ref listing, the
  reconciliation holding `registry_entry_present: true` from the registry
  listing, `branch_present: true` and the new `branch_sha` from the ref
  listing, `path_present: true` from the added `lstat`, and `reconciled: true`
  (plan review M13), later targets `not-attempted`, the branch kept at the new
  commit, exit 2); and
  `test_clean_deleted_upstream_reappears_before_revalidation` (P and Q
  selected, each with a deleted upstream recorded with `upstream_oid`, `ahead`
  and `behind` null: a fetch recreating P's upstream at the question refuses P
  with `state-changed`, Q is `not-attempted`, nothing is removed, exit 2; a
  fetch recreating only Q's in the post-remove hook of P, after P's child exits
  0 and before its rescan: P `removed`, Q `refused` with `state-changed`, exit
  2). Scenarios: "State changes before revalidation"; "Branch advances before
  removal"; "Deleted upstream reappears before revalidation".
- [ ] T082 [US4] Add to `tests/test_clean_revalidation.py`:
  `test_clean_untracked_file_under_status_showuntrackedfiles_no`
  (`status.showUntrackedFiles=no` in the `GIT_CONFIG_GLOBAL` file, and an
  untracked file created by the pre-remove hook: Git refuses with 128, the
  target is `failed` with `git-refused`, its reconciliation showing the entry
  and path present, the file kept, later targets `not-attempted`, exit 128);
  `test_clean_git_s_own_check_runs_on_the_pinned_configuration`
  (`core.untrackedCache=true` and `core.checkStat=minimal` in the repository,
  an index-writing `status` run, and a file created by the pre-remove hook:
  128, `failed` with `git-refused`, the file kept, exit 128); and
  `test_clean_ignored_file_in_the_residual_window` (an ignored file created by
  the pre-remove hook: Git removes the worktree with exit 0, the target is
  `removed`, the file is gone, and the result carries the residual-window line
  the confirmation carried). They pin T056 and T057. Scenarios: "Untracked file
  under status.showUntrackedFiles=no"; "Git's own check runs on the pinned
  configuration"; "Ignored file in the residual window".
- [ ] T083 [US4] Add to `tests/test_clean_revalidation.py`:
  `test_clean_branch_advances_after_removal` (the post-remove hook advances the
  target's branch: `removed` with `branch-advanced-after-removal`,
  reconciliation `registry_entry_present: false`, `path_present: false`,
  `branch_present: true` and a `branch_sha` other than `planned_sha`, later
  targets `not-attempted`, no commit lost, exit 2; a hook deleting the branch
  instead: `branch-missing-after-removal` with `branch_present: false`, exit
  2); `test_clean_repository_replaced_mid_batch` (in a three-target plan, the
  first target's post-remove hook renames the root and moves another clone into
  its path, and in a second run replaces the root's parent by a symlink to a
  copy: the first target `unknown` with `unconfirmed-removal`, every
  reconciliation field null and `reconciled: false`, the others `not-attempted`
  with `batch-stopped`, exit 1; the same replacement at the question refuses
  the first target with `identity-changed`, exit 2, nothing removed);
  `test_clean_hidden_local_state_after_confirmation` (an assume-unchanged flag
  set on a selected target at the question: `refused` with
  `hidden-local-state`, later targets `not-attempted`, exit 2); and
  `test_clean_submodules_after_confirmation` (a `modules` directory created in
  a selected target's admin directory at the question: `refused` with
  `contains-submodule`, exit 2). Scenarios: "Branch advances after removal";
  "Repository replaced mid-batch"; "Hidden local state" and "Submodules", their
  after-confirmation clauses (spec.md, US4 scenario 2).

### Implementation for User Story 4

- [ ] T084 [US4] Replace the body of `revalidate()` (region `apply`; D7,
  FR-046, FR-047, R-22) with the targeted check, in this order and stopping at
  the first difference: the identity probe in the command directory; the
  manifest re-read through `declared_tracking_branch()` and the merge target
  re-resolved; the registry listing; one narrowed ref listing whose patterns
  come from `narrowed_ref_patterns(plan)` (the merge target, the manifest's
  candidate, the branch the plan's `origin/HEAD` named, `main`, `master`,
  `refs/remotes/origin/HEAD`, and the selected branches and their upstreams);
  the target's identity `{path, dev, ino, admin_id}`, its two-way registration
  and `modules_check()`, by filesystem reads; then, inside the worktree,
  `status_probe()`, which must print no record, and `hidden_state_probe()`.
  Reasons: `identity-changed` (a repository or worktree identity, the
  registration, a missing registry entry), `branch-changed` (the branch name or
  head), `state-changed` (any other signature field, the lock, the manifest,
  the merge target, an `upstream_oid` that reappears), `contains-submodule` and
  `hidden-local-state`. A value null in the plan and null again is no
  difference, and one that cannot be re-read is one; the first target's three
  repository children are the preflight of every target; at most five Git
  children per target. A refused target's reconciliation comes from the
  revalidation that refused it, plus an `lstat` of the planned path when that
  revalidation stopped before its own; a field whose listing did not run is
  null (plan review M13).
- [ ] T085 [US4] In `rescan()` and `decide_stage()` (region `apply`; D7,
  FR-035, FR-049): the rescan re-establishes the repository identity first, and
  where it differs every reconciliation field is null, `reconciled` is false,
  the target is `unknown` with `unconfirmed-removal`, and later targets are
  `batch-stopped`; a removal whose branch the rescan finds at another SHA, or
  gone, is `removed` with `branch-advanced-after-removal` or
  `branch-missing-after-removal` and stops the run; after a plain `removed`,
  its rescan's three repository children serve as the next target's repository
  part, counted in that target's `probes_performed`. T079 to T083 pass.
- [ ] T086 [US4] Run the US4 module, every earlier module and the 96 tests: all
  pass.

**Checkpoint**: A change after the plan refuses its target and attempts nothing
later; a race after Git's own removal loses no commit.

---

## Phase 7: User Story 5 - Every removal ends in a reconcilable record

**Priority**: P2.

**Goal**: Whatever stops a batch, every selected target ends in one stage with
one reason and, unless it was not attempted, a reconciliation record; a started
removal is never interrupted, and the result names what was removed, what was
not attempted, every branch kept and the next command.

**Independent Test**: Drive the apply phase with fake Gits and hooks (exit 0
without removing, exit 128, exit 255 leaving a directory, a removal past the
ceiling, SIGINT, SIGTERM and SIGHUP, an injected exception, an unreadable
parent) and check each target's stage, reason, notes and reconciliation, the
stop block and the exit status.

**Lanes**: removal (T087 to T090, T092, T093: `tests/test_clean_result.py`,
region `apply`), after US4, since both edit `rescan()` and `decide_stage()`;
and text (T091, T094: `tests/test_clean_stop.py`, regions `preview` and
`result`), which may start after US2, beside US4.

### Tests for User Story 5

- [ ] T087 [P] [US5] Add to `tests/test_clean_result.py`, each launched run
  with its own table (R-29): `test_clean_a_signal_during_a_removal` (launcher;
  three targets, the second removed by the `remove-slow` fake: SIGINT to
  `project` while it runs leaves the child unsignalled, as the fake records,
  and waited for; the second target is `removed` when the child exits 0 and the
  rescan shows its entry and path gone, or `failed` with Git's status when a
  `remove-exit` fake exits nonzero; the third is `not-attempted` with
  `interrupted`; exit 130; SIGTERM there exits 143 and SIGHUP 129; at a
  pseudo-terminal, SIGINT at the question, and end of input there, exit 130
  with nothing removed); `test_clean_sigterm_before_the_apply_phase` (launcher;
  SIGTERM while the `ignore-sigterm` status probe runs during planning: its
  group gets SIGKILL at least 0.9 of the grace in force after the SIGTERM,
  measured from the child, and is reaped, `os.killpg(pgid, 0)` raises
  `ProcessLookupError`, nothing is mutated, exit 143; under `--json` standard
  error carries `Cancelled.` and standard output is empty; it pins T047 and
  T035); `test_clean_sigterm_before_the_apply_phase_after_the_last_probe` (the
  `signal-parent-in` fake sends SIGTERM, and in turn SIGHUP, to `project` from
  the last status probe, which then completes: with `--yes`, and at a
  pseudo-terminal before the question, `Cancelled.`, 143 or 129, no question
  asked, nothing removed and no document; plan review M1; it pins T047);
  `test_clean_sigterm_before_the_apply_phase_while_the_plan_is_written` (in
  process, `print_plan` patched to record SIGTERM in the slot as it returns, in
  turn SIGHUP and SIGINT: a report and an `--all-safe` preview each exit 143,
  129 and 130 with `Cancelled.` on standard error, and nothing is mutated;
  research.md R4, lead ruling R-34; it pins T047); and
  `test_clean_a_second_sigint_abandons_reconciliation` (the `slow-after-remove`
  fake: SIGINT while the first removal runs, then a second SIGINT while its
  rescan waits: the remaining rescans are abandoned, the target is `unknown`
  with `reconciliation-incomplete` and the fields not read are null, the record
  is printed, exit 130; plan review M17, FR-036). Scenarios: "A signal during a
  removal"; "SIGTERM before the apply phase".
- [ ] T088 [P] [US5] Add to `tests/test_clean_result.py`:
  `test_clean_exit_0_without_evidence` (the `remove-noop` fake: `unknown` with
  `unconfirmed-removal`, later targets `not-attempted`, exit 1; it pins T056);
  `test_clean_git_leaves_an_orphaned_directory` (`not_root`; a subdirectory
  without write permission: `failed` with `git-failed` and `exit_status: 255`,
  reconciliation `registry_entry_present: false` and `path_present: true`, the
  branch kept with its SHA, `notes: ["orphaned-directory"]`, later targets
  `not-attempted`, exit 255; no later plan lists the directory, and nothing
  deletes it); and `test_clean_git_refuses_the_removal` (the pre-remove hook
  locks the target: Git exits 128, the target is `failed` with `git-refused`,
  its record holding the command, `exit_status: 128` and a reconciliation with
  the entry and path present, later targets `not-attempted`, every retained
  branch reported, exit 128). Scenarios: "Exit 0 without evidence"; "Git leaves
  an orphaned directory"; "Git refuses the removal".
- [ ] T089 [P] [US5] Add to `tests/test_clean_result.py`:
  `test_clean_a_removal_past_the_hard_ceiling` (launcher, with a table that
  shortens the ceiling, the grace and the reap wait and leaves the probe budget
  whole (R-29); a `remove-slow` child past the ceiling: its group is killed,
  `exit_status` 137 once it is reaped (plan review M12), then the rescan
  decides: `unknown` with `removal-ceiling`, the note `partially-removed` and
  the recovery text while the entry or path remains, and `removed` with
  `removal-ceiling` when both are gone; later targets `not-attempted`; exit 1);
  `test_clean_unreadable_path_after_removal` (`not_root`; the post-remove hook
  removes search permission from the target's parent: `path_present: null`,
  `reconciled: false`, `unknown` with `reconciliation-incomplete`, the record
  printed, exit 1); and `test_clean_exception_after_the_apply_phase_begins` (in
  process, in turn: `rescan` patched to raise for the first target;
  `run_removal` patched to raise once its child has started, the child waited
  for before the target is decided; and the final rescan patched to raise: the
  target being handled `unknown` with `internal-error` and its fields not
  established null, later targets `not-attempted`, the record printed, exit 1,
  and 143 when the patch also records SIGTERM in the slot; plan review M2).
  Scenarios: "A removal past the hard ceiling"; "Unreadable path after
  removal"; "Exception after the apply phase begins".
- [ ] T090 [P] [US5] Add `test_clean_stage_and_reason_table` to
  `tests/test_clean_result.py`: `decide_stage()` on literal inputs reaches
  every stage and reason pair of data-model.md's "Target stages" and no other;
  a child that exits nonzero on its own is `failed` whatever the signal slot
  holds; only a child killed at the ceiling, or whose exit was not observed, is
  decided by the rescan.
- [ ] T091 [P] [US5] Add to `tests/test_clean_stop.py`:
  `test_clean_the_stop_block` (three targets, the second refused with
  `branch-changed`: the human result reads the progress lines in the contract's
  form (`  STAGE PATH` or `  STAGE PATH (REASON)`), then `Stopped at P2
  (branch-changed). Removed 1 of 3. Not attempted: P3. Next: project clean ROOT
  --all-safe`, then `Branches kept: B1, B2, B3.` and the residual-window line
  (plan review M8); it pins T057); `test_clean_only_tracked_file_deletions`
  (tracked files deleted by hand in a registered worktree whose `.git` file is
  intact: classified `dirty` with the dirty advice, the line `Probable partial
  removal: inspect, then git worktree remove --force PATH by hand.` beside it,
  and `notes: ["partially-removed"]` in the JSON row; one deleted tracked file
  and one untracked file: no note); and
  `test_clean_project_killed_during_a_deletion` (a worktree of about 8,000
  tracked files built once in `setUpClass`; launcher; `project` and its removal
  child killed with SIGKILL mid-deletion, then plain `project clean`: a target
  whose `.git` file survived reads `dirty` with the note and recovery text
  beside the dirty advice, and one whose `.git` file was already deleted reads
  `registration-mismatch` with classification `inspection-error`, a named
  manual remedy and no note; run once stopping before 4,096 deletions and once
  after; the deterministic gate is `test_clean_only_tracked_file_deletions`,
  D4). Scenarios: "The stop block"; "Only tracked-file deletions"; "project
  killed during a deletion".

### Implementation for User Story 5

- [ ] T092 [P] [US5] Fill `run_removal()` (region `apply`; D9, FR-012): the
  child is never signalled on SIGINT, SIGTERM, SIGHUP or the deadline; the
  first of those prints D18's wait line, at most once; the ceiling,
  `TIMING["removal_ceiling"]` read at the spawn, ends the wait by
  `terminate_group()`, which the wait's own loop advances to SIGKILL and a
  bounded reap (R-30), and a child reaped there has `exit_status` 137 (plan
  review M12); a child killed there, or whose exit was not observed, is decided
  by the rescan with reason `removal-ceiling` and, while its entry or path
  remains, the note `partially-removed`.
- [ ] T093 [P] [US5] In `apply_removals()`, `rescan()` and `decide_stage()`
  (region `apply`; D15, FR-034 to FR-036): read the signal slot before each
  revalidation and each spawn, a set slot making that target and every later
  one `not-attempted` with `interrupted`; reconcile within the reserve, each
  rescan child getting `min(5 s, reserve remaining)`; a second SIGINT during
  reconciliation abandons the remaining rescans, their fields null and the
  target `unknown` with `reconciliation-incomplete` (M17); an exception after
  the apply phase begins, in a target, its rescan, the final rescan or the
  record's rendering, first waits for an in-flight removal, then makes the
  target being handled `unknown` with `internal-error` (fields not established
  null) and later targets `not-attempted`, and the record is still printed, the
  exit by D19 (plan review M2); a rescan `lstat` that fails other than with
  `ENOENT` or `ENOTDIR`, or times out, gives `path_present: null` and
  `reconciliation-incomplete`; add the `orphaned-directory` note; guard every
  write of the record against `OSError`, the EIO a terminal may answer after
  SIGHUP. T087 to T090 pass.
- [ ] T094 [P] [US5] In `print_plan()` (region `preview`), print D18's
  partial-removal note on its own line under the `dirty` advice of a row noted
  `partially-removed`; in `print_result()` (region `result`), print the same
  note with the recovery text on a `partially-removed` target. T091 passes.
- [ ] T095 [US5] Run the US5 modules, every earlier module and the 96 tests:
  all pass.

**Checkpoint**: Every target of every apply ends in a stage, a reason and,
unless not attempted, a reconciliation record.

---

## Phase 8: User Story 6 - Every run is bounded and says what it omits

**Priority**: P2.

**Goal**: One deadline, per-child budgets, row and target caps, and a plain
report that exits 1 when incomplete; rows past sixteen deferred to the next run
with the plan complete; counts that equal what ran.

**Independent Test**: Under a counting `git` wrapper and slow fake Gits,
register more rows than the caps, more removable rows than sixteen and a
worktree with 70 ignored files, and check completeness, `omitted`, the exit
statuses, the child counts and the order of what was cut.

**Lanes**: one, `tests/test_clean_bounds.py`, in regions `plan`, `gates`,
`preview`, `dispatcher` and `apply`. It starts after US3, US4 and US5.

### Tests for User Story 6

- [ ] T096 [US6] Add to `tests/test_clean_bounds.py`:
  `test_clean_audit_a_repository_with_a_feature_worktree` (plain `project
  clean` reports the main worktree and each linked one and says remote
  information may be stale, and the counting log holds no fetch, commit, push,
  reset, stash or removal; it pins T052);
  `test_clean_the_plain_report_exits_by_completeness` (257 rows registered
  directly: an incomplete report with `inspect-cap` and `omitted`, exit 1; 200
  rows: a complete report, exit 0, the human line `--all-safe would be
  incomplete (inspect-cap)`, JSON `selected: null` and a `notes` entry
  `inspect-cap` with `rows: 200`, while `--all-safe` there exits 1, incomplete
  with `inspect-cap`); `test_clean_an_unreadable_worktree_is_one_row`
  (`not_root`; a parent without search permission: `present: null`, an
  `os-error`, `inspection-error`, every other row reported, an incomplete
  report, exit 1);
  `test_clean_a_failed_status_probe_on_the_merge_target_checkout`
  (`status-fails-in`, and `status-hangs-in` under the launcher with its own
  table, on the worktree holding the merge-target branch: `inspection-error`,
  never `protected-default`, `dirty` null, incomplete with
  `inspection-incomplete`, exit 1); and
  `test_clean_a_failed_status_in_the_repository_root` (the main worktree's
  status probe fails: its row `inspection-error`, an incomplete report, exit
  1). Scenarios: "Audit a repository with a feature worktree"; "The plain
  report exits by completeness"; "An unreadable worktree is one row"; "A failed
  status probe on the merge-target checkout"; "A failed status in the
  repository root".
- [ ] T097 [US6] Add to `tests/test_clean_bounds.py`:
  `test_clean_row_cap_and_planning_failures` (129 rows: incomplete with
  `inspect-cap`, `omitted` visible, the status children those of the main
  worktree and the 127 smallest paths, the preview exit 1, and `--apply` exit 2
  before any mutation; a status probe timing out under the launcher
  (`status-hangs-in`, with a table that shortens the probe budget to no less
  than 1 s; R-29): `inspection-incomplete` with the row visible; the work
  deadline passing during planning under the launcher (a table that shortens
  the deadline and the reserve), with slow fakes: `deadline-exceeded`);
  `test_clean_twenty_rows_pass_every_gate_before_deferred_target_cap` (twenty
  merged rows: the first sixteen by raw path selected and removed, four
  excluded as `deferred-target-cap` with D18's deferral line and the command to
  run next, the plan complete, exit 0, and a second run removes the four;
  seventeen rows holding gitlinks, made cheaply by `gitlink()`: the first
  sixteen excluded as `contains-submodule` and D18's non-drain line printed);
  and `test_clean_ignored_file_bound` (70 ignored files: `ignored_files: 64`,
  `ignored_files_truncated: true`, 8 samples, excluded as
  `ignored-local-files`; exactly 64: `false`, still excluded; 4,097 untracked
  entries and no ignored one: `ignored_files: null`, `ignored_files_truncated:
  true`, `dirty: true`, classification `dirty`, the plan complete; it pins the
  parsers and the evidence model of Phase 2). Scenarios: "Row cap and planning
  failures"; "Twenty rows pass every gate before deferred-target-cap";
  "Ignored-file bound".
- [ ] T098 [US6] Add to `tests/test_clean_bounds.py`:
  `test_clean_bounded_revalidation_work` (five rows, three selected,
  `--all-safe --apply --yes` under the counting wrapper and the real table
  (R-29): each revalidation spawns at most five children, the final rescan
  three, and three removals run; after confirmation, no `for-each-ref --merged`
  and no status probe of a non-selected worktree; every `status` and `ls-files`
  child names its own worktree, and every other child after resolution, the
  removals included, the command directory; `probes.performed` equals the count
  of children other than the three removals, and `operations.performed` is 3,
  as PR #19 words it and research.md R8 counts, and the plan's
  `probes.estimated` is F + W + E + 5T + 3 (plan review M7));
  `test_clean_deadline_expiry_mid_batch` (launcher, with a table that shortens
  the deadline, the reserve and the floor (R-29): the `remove-slow` removal of
  the second of three, still running at the work deadline, is not signalled and
  is waited for; the second is `removed` when it exits 0 and the rescan shows
  it gone; the third is `not-attempted` with `deadline-exceeded`; exit 1; with
  the first removal slow enough that less than the floor remains when the
  second passes revalidation: no second child, the second and third
  `not-attempted` with `deadline-exceeded` and `reconciliation: null`, exit 1);
  `test_clean_push_refuses_an_incomplete_inspection_deadline` (the deadline
  passing during a push's re-inspection after confirmation, through
  `status-hangs-in` under the launcher with its own table: `deadline-exceeded`,
  exit 2, no push child); and `test_clean_budget_reports_the_values_in_force`
  (unscaled, `budget` holds 5, 60, 10, 5, 300 and 1, and `limits` 128 or 256,
  16, 64, 4096 and 8; under the launcher, `budget` shows the values of the
  test's own table). Scenarios: "Bounded revalidation work"; "Deadline expiry
  mid-batch"; "Push refuses an incomplete inspection", its deadline clause.

### Implementation for User Story 6

- [ ] T099 [US6] Bound planning and gate removals by the clock of the
  `Invocation` (FR-029, FR-030; regions `plan` and `apply`): `build_plan()`
  stops at the work deadline, leaving the remaining rows unprobed and the plan
  incomplete with `deadline-exceeded`, a non-blocking note in mode single;
  every Git child and filesystem call gets `min(5 s, work remaining)`;
  `apply_removals()` spawns a removal only while the 5 s floor of work remains,
  else that target and every later one are `not-attempted` with
  `deadline-exceeded` and `reconciliation: null`; a removal running at the
  deadline is waited for, and the reserve counts from its exit.
- [ ] T100 [US6] Fill `deferral_gate` (region `gates`; D12, FR-032): the first
  16 rows that pass gates 1 to 7, in canonical order, go on to the index gates,
  and the rest are excluded as `deferred-target-cap`; in `print_plan()` (region
  `preview`), D18's deferral line with `project clean ROOT --all-safe --apply`,
  and its non-drain line when all 16 are `contains-submodule`.
- [ ] T101 [US6] Finish report mode (D14, FR-003 to FR-005; regions `plan`,
  `preview` and `dispatcher`): above 128 rows `selected` is null and the notes
  carry `inspect-cap` with `rows`, which alone leaves the report complete,
  while the gates still run and `excluded` still lists every inspected row a
  gate excludes; `print_plan()` adds, after `Freshness:`, `Report: complete` or
  `Report: incomplete (CODES)`, then `--all-safe would select N` or `--all-safe
  would be incomplete (inspect-cap)` (plan review M8); `check_plan()` exits a
  report 0 when complete and 1 when incomplete.
- [ ] T102 [US6] Account the counts (FR-033, research.md R8; regions `plan` and
  `apply`): `probes` and `operations`, `estimated` as T049 computes it (plan
  review M7) and `performed` from the counters, in plans and results; each
  target's `probes_performed` counts its revalidation children and the rescan
  children T085 attributes to it; each count equals the counting wrapper's.
  T096 to T098 pass.
- [ ] T103 [US6] Run the US6 module, every earlier module and the 96 tests: all
  pass.

**Checkpoint**: Every run is bounded, says what it omitted, and exits by
completeness.

---

## Phase 9: User Story 7 - Acting on exactly the repository given

**Priority**: P2.

**Goal**: Every `clean` mode resolves its argument Git-first to exactly one
repository and its main worktree, refuses what is not a repository root, and
finds the merge target by a fixed, recorded order with a bounded manifest read.

**Independent Test**: Pass subdirectories, linked worktrees, bare repositories,
submodule and separate-git-dir checkouts, family and manifest layouts, and
manifests of each kind to each `clean` mode, and check the resolved
`repository`, `root` and `merge_target`, or the refusal.

**Lanes**: one, `tests/test_clean_resolution.py`, region `resolution`, and
`main_worktree()`, `declared_tracking_branch()` and `resolve_merge_target()` in
region `evidence`. It starts at US1's checkpoint, beside US2, US3 and US9.

### Tests for User Story 7

- [ ] T104 [US7] Add to `tests/test_clean_resolution.py`:
  `test_clean_absolute_path_that_is_not_a_repository_root` (an absolute path to
  a subdirectory of the root, to a linked worktree, to a directory outside any
  repository and to a bare repository, each passed read-only, with `--all-safe
  --apply --yes`, and with `--apply --action remove --worktree X --yes`,
  `--action push --branch B --yes` and `--action delete-branch --branch B
  --yes`: `target-not-repository-root`, exit 2, before any plan, no other
  directory substituted, nothing changed);
  `test_clean_overview_handoff_keeps_identity` (in process, with
  `projects_dirs` patched to two directories, since macOS folds `~/projects`
  and `~/Projects` into one: the argument vector `["clean", ATLAS,
  "--all-safe", "--json"]`, with an independent clone also named Atlas in the
  second directory and in turn an ancestor of the Atlas root holding
  `project.yaml` and the root containing `Atlas/family.yaml`: the plan's
  `repository` names the Atlas repository by its four identity fields, `dev`
  and `ino` from `os.lstat` of its common directory, the report's `root` is the
  Atlas root, and no child names the other clone; without the family holder,
  `clean Atlas --all-safe` refuses with `ambiguous-name`, exit 2); and
  `test_clean_bare_name_predicate` (R13 as plan review M15 words it: `Atlas` is
  a bare name; `.`, `..`, `a/b`, `./a`, `a/` and an absolute path are not,
  every relative argument holding a `/` resolving as a path; `~` is expanded
  first). Scenarios: "Absolute path that is not a repository root"; "Overview
  handoff keeps identity".
- [ ] T105 [US7] Add to `tests/test_clean_resolution.py`:
  `test_clean_a_bare_repository_reached_from_a_linked_worktree` (a relative
  path, and no argument, inside a linked worktree of a bare repository:
  `target-not-repository-root`, exit 2); `test_clean_a_separate_git_directory`
  (a repository made by `git init --separate-git-dir`, passed by its checkout's
  absolute path: it resolves, `repository.root` is the checkout, and the git
  directory is no worktree row);
  `test_clean_a_separate_git_directory_with_a_relative_core_worktree` (the same
  layout with `core.worktree` set by `git config` to the relative value
  `../CHECKOUT`, the checkout a sibling of the git directory, `project` run
  from another directory: it resolves against the git directory, as Git
  documents and project-overview's spec states, so `repository.root` is the
  checkout's realpath; lead ruling R-36); and `test_clean_a_submodule_checkout`
  (a submodule's checkout: `target-not-repository-root`, exit 2). Scenarios: "A
  bare repository reached from a linked worktree"; "A separate git directory";
  "A submodule checkout".
- [ ] T106 [US7] Add to `tests/test_clean_resolution.py`:
  `test_clean_merge_target_missing_invalid_or_conflicting` (no candidate:
  `no-merge-target` with its baseline message, exit 2, `--json` printing the
  extended error object; a manifest of the wrong kind: `manifest-invalid` the
  same way; a manifest naming `release` and `origin/HEAD` naming `main`, both
  existing: `merge_target` is `release` with `source: "manifest"`, with a
  `merge-target-conflict` note and `apply_allowed: true` in the `--all-safe`
  preview; no manifest candidate, local `trunk` and `main`, and `origin/HEAD`
  naming `trunk`: `trunk` with `source: "origin-head"`);
  `test_clean_a_tracking_branch_spelled_with_its_remote` (`tracking_branch:
  origin/develop` with local `develop` and `main` and `origin/HEAD` naming
  `main`: `develop`, `source: "manifest"`, its SHA from `refs/heads/develop`);
  and `test_clean_a_manifest_over_1_mib` (a manifest of 1 MiB plus one byte:
  `manifest-invalid`, exit 2, no status child in the counting log, and, in
  process with `read_yaml` patched to fail, the file never read). Scenarios:
  "Merge target missing, invalid, or conflicting"; "A tracking branch spelled
  with its remote"; "A manifest over 1 MiB".

### Implementation for User Story 7

- [ ] T107 [US7] Fill `resolve_clean_target(args, run)` in region `resolution`
  (D8, FR-016, FR-017) with `is_bare_name()` (R13 as plan review M15 words it:
  after `expanduser()`, a relative argument that contains no `/` and is neither
  `.` nor `..`): an absolute path whose realpath equals row 3's toplevel and is
  the main worktree; a relative path, or none, joined to the working directory
  and resolved by row 3 there; a bare name through `discover()`, then resolved
  as a worktree toplevel; the family-holder and manifest-ancestor redirections
  never for a path. Fill `main_worktree()` (region `evidence`) with M6's order:
  row 3's third line, a submodule checkout, refused; a first registry record
  that is `bare` refused; a first record equal to the common directory resolved
  by the realpath of `core.worktree` (row 4b; a relative value resolved against
  the git directory, as Git documents and project-overview's spec states, lead
  ruling R-36) or the candidate toplevel whose `.git` file names it, else
  refused; otherwise the first record's realpath. Every refusal is
  `target-not-repository-root`, exit 2, before any plan.
- [ ] T108 [US7] Fill `declared_tracking_branch(root)` (region `evidence`; D8,
  FR-018, FR-060) with a bounded read: an `st_size` over 1 MiB is
  `manifest-invalid` without a read, the read never passes 1 MiB, and an
  unreadable file, a parse error or a wrong kind is `manifest-invalid`; in
  `resolve_merge_target()`, add the `merge-target-conflict` note when the
  manifest and `origin/HEAD` name different existing branches, the manifest
  winning; every refusal carries the established repository and merge target in
  `context`, so that the extended error object fills them. T104 to T106 pass.
- [ ] T109 [US7] Run the US7 module, every earlier module and the 96 tests: all
  pass.

**Checkpoint**: Every mode acts on exactly the repository given, with a
recorded merge target.

---

## Phase 10: User Story 8 - Exact paths and one JSON document per run

**Priority**: P3.

**Goal**: Paths holding line feeds, control or bidirectional characters, or
bytes that are not UTF-8 are reported exactly or excluded and never misread;
every `clean --json` run but the stated exceptions prints one versioned
document.

**Independent Test**: On Linux, create worktrees whose paths hold a line feed,
a tab, U+0001, U+202E and the byte 0xFF, run the preview and the apply with and
without `--json`, and parse standard output as JSON in every mode.

**Lanes**: one, `tests/test_clean_paths.py` and region `resolution`. It starts
after US6 and US7.

### Tests for User Story 8

- [ ] T110 [US8] Add to `tests/test_clean_paths.py`:
  `test_clean_control_character_and_non_utf_8_paths` (`linux_paths`; eligible
  worktrees whose paths hold a line feed, a tab, U+0001 and U+202E, and an
  otherwise eligible one whose path holds 0xFF: the preview and the apply
  select the first four with exact JSON strings and `path_valid_utf8: true`,
  the human plan prints them as `$'...'` with `\u000a`, `\u0009`, `\u0001` and
  `\u202e`, the counting log shows each raw path as one argument, and a rescan
  proves each removed; the fifth is excluded as `unsupported-path-bytes`, shown
  with `\xff` and `path_valid_utf8: false` in `worktrees` and `excluded`, in no
  removal's argument vector, and still present) and
  `test_clean_non_utf_8_repository_root` (`linux_paths`; a root path holding
  0xFF with `--all-safe`: `unsupported-path-bytes`, exit 2, and no plan, digest
  or status child). Scenarios: "Control-character and non-UTF-8 paths";
  "Non-UTF-8 repository root".
- [ ] T111 [US8] Add to `tests/test_clean_paths.py`:
  `test_clean_apply_with_json_prints_one_document` (`--all-safe --apply --yes
  --json` removing two worktrees: standard output is exactly one document, the
  apply result record with two `removed` targets and `exit_code: 0`, and the
  human plan and progress are on standard error; a run stopped by
  `plan-digest-mismatch` prints only the plan envelope; it pins T057);
  `test_clean_the_plain_report_in_json` (one eligible worktree: one envelope
  with `schema_version: 1`, `mode: "report"`, `apply_allowed: false` and
  `limits.worktree_rows: 256`, that worktree in `selected`, and a 64-character
  `plan_digest` equal to the `--all-safe` preview's, FR-004; exit 0; it pins
  T051 and T101); `test_clean_every_json_path_carries_its_flag` (every object
  with a `path` carries `path_valid_utf8`; `ignored_samples` entries are
  objects; `repository` carries `root_valid_utf8` and `common_dir_valid_utf8`,
  both true); and `test_clean_each_refusal_prints_its_document` (under
  `--json`, each refusal code, reached through the command line or, for
  `internal-error`, by an exception injected in process, prints one document:
  the extended error object for `invalid-arguments`, `internal-error` and every
  resolve code, and the plan envelope with `apply_allowed: false` and the code
  in `refusals` for `worktree-not-found`, `target-excluded`, the plan codes,
  `plan-digest-mismatch`, `confirmation-required` and `cancelled`; plan review
  M6). Scenarios: "Apply with JSON prints one document"; "The plain report in
  JSON".

### Implementation for User Story 8

- [ ] T112 [US8] In `resolve_clean_target()` (region `resolution`; FR-041),
  refuse a `root` or `common_dir` that is not valid UTF-8 with
  `unsupported-path-bytes`, exit 2, before any plan or digest. Check that every
  printer and document writer (regions `preview`, `result`, `plan` and `guard`)
  routes each path through `human_path()` or `json_path()`, ignored samples,
  refusal paths, row errors and the commands in the stop block and the deferral
  line included, and fix any that does not. T110 and T111 pass.
- [ ] T113 [US8] Run the US8 module, every earlier module and the 96 tests: all
  pass.

**Checkpoint**: Every path is exact or excluded, and every `clean --json` run
prints one document.

---

## Phase 11: User Story 9 - Status, doctor and update share the evidence

**Priority**: P3.

**Goal**: `status`, `doctor` and `update` read repositories through the
evidence model: they never refuse for Git's version or an uninspectable
repository, report `inspection-error` rows instead, and a shape or bench update
refuses any `dirty` that is not exactly false.

**Independent Test**: With Git 2.35 first on PATH, with no `git`, with fake
Gits that fail or hang a status probe, and with a deleted upstream, run
`status`, `doctor` and `update` and check the error rows, the exit statuses and
the counting wrapper's record. The seven evidence-model scenarios of this story
are T030's, in Phase 2.

**Lanes**: one, `tests/test_status_doctor_update.py`, editing `repo_state()`,
`discover()`, `snapshot()`, `check_rows()`, `print_report()`,
`inspect_project()` and `update()`. It starts at Phase 2's checkpoint, beside
every clean story; the `clean` tests of T114 and T116 also need US1.

### Tests for User Story 9

- [ ] T114 [US9] Add to `tests/test_status_doctor_update.py`:
  `test_clean_git_older_than_2_36` (the `version-2.35.0` fake first on PATH:
  every `clean` mode refuses with `git-too-old`, exit 2, its only child `git
  --version`; `--json` prints the extended error object with `code:
  "git-too-old"`; with no `git` on PATH, `git-unavailable`, exit 2; it pins
  T048); `test_status_git_older_than_2_36_in_status_and_doctor` (status marks
  the root `inspection-error` and exits 0; doctor reports `git-too-old` as an
  `error` check row and exits 1; neither refuses; the counting log of each
  holds `git --version` alone, `handoff()`'s `remote get-url` never spawned
  (plan review M10); a directory with no `.git` still reads `present: false`);
  `test_doctor_no_git_on_path` (`path_without_git()`: `git-unavailable` as an
  `error` row, exit 1; research.md R2); and
  `test_update_tools_and_workflow_need_no_git` (the 2.35 fake: `update --apply
  --component workflow --yes` runs the fake `setup-openspeckit` as before and
  is not refused for Git's version). Scenarios: "Git older than 2.36"; "Git
  older than 2.36 in status and doctor"; "No git on PATH"; "Tools and workflow
  need no Git".
- [ ] T115 [US9] Add to `tests/test_status_doctor_update.py`:
  `test_status_a_failed_root_status_is_reported` (`status-fails-in` the root:
  status and doctor report it with `classification: "inspection-error"`, its
  `errors` and a null `dirty`, and neither exits 2; doctor exits 1);
  `test_doctor_not_established_is_an_error_none_is_not` (run under the counting
  wrapper, so that its `git` row names the wrapper's path, rule 13; a fresh
  project with no remote: its null `upstream`, `ahead` and `behind` raise no
  error, and doctor passes; a leg whose status probe fails: an `error` row,
  exit 1); `test_status_a_deleted_upstream_in_status_and_doctor` (`upstream` is
  the configured short name, `origin/<branch>`, with `ahead` and `behind`
  null); and `test_update_a_leg_s_probe_times_out` (launcher, with a table that
  shortens the 15 s inspection budget (R-29); `status-hangs-in` a leg: `update
  --apply --component shape` refuses with exit 2, and the fake `openRepoShape`
  records no run). Scenarios: "A failed root status is reported"; "Not
  established is an error, none is not"; "A deleted upstream in status and
  doctor"; "A leg's probe times out".
- [ ] T116 [US9] Add to `tests/test_status_doctor_update.py`:
  `test_status_the_pinned_status_configuration` (rule 1, plan review M14;
  `core.untrackedCache` and `core.fsmonitor` true in the `GIT_CONFIG_GLOBAL`
  file: the counting log shows `-c core.untrackedCache=false -c
  core.fsmonitor=false` on every status child and on every removal child of an
  apply; it pins Phase 2 and T056); `test_doctor_missing_leg` (a declared leg
  with no checkout: an actionable failure, nonzero exit); and
  `test_update_default_report` (`update` without `--apply` reports a plan, the
  counting log holds no child that writes, and nothing is installed).
  Scenarios: "The pinned status configuration"; "Missing leg"; "Default
  report".

### Implementation for User Story 9

- [ ] T117 [US9] Move `repo_state()` (`project:470-521`) onto the evidence
  model (D16, FR-050, FR-051, FR-059): `lstat` of `<path>/.git` first, and when
  absent `present: false` with no Git child; then the version check; an old,
  missing or unusable Git, or a failed or timed-out status probe, gives
  `classification: "inspection-error"` and `errors`, with `present` null when
  the version check failed and every unestablished value null; 15 s per Git
  child and per filesystem call (plan review m8), no deadline, no row cap;
  `path_valid_utf8` beside every `path`, `root_valid_utf8` beside the top-level
  `root` and each nested member's, and `ignored_samples` as objects; a deleted
  upstream's short name with `ahead` and `behind` null; every other key and
  value as today, so that `tests/test_project.py:586`, `:615` and `:916` pass.
- [ ] T118 [US9] In `discover()` (`project:433-467`; research.md R2, FR-053):
  before its Git step, the version check memoized on that `main()` call's
  `Invocation` (plan review M10); with Git 2.36 or later, `rev-parse
  --show-toplevel` through the driver as now; otherwise no Git child: the
  nearest of the path and its ancestors holding a `.git` entry, by `lstat`,
  then today's `.project.json` and `.devcontainer` fallback.
  `tests/test_project.py:641` passes.
- [ ] T119 [US9] Update `check_rows()` (`project:876-906`: the `git` row
  reports the version check, `ok` with the version or `error` with
  `git-too-old` or `git-unavailable`; an `error` row for each null `present`,
  each `dirty` left null by a failed or timed-out probe and each
  `inspection-error` row, and none for a null that means "none"),
  `print_report()` (`project:909-933`: `Git: inspection-error (CODES)` in place
  of the branch line), `inspect_project()` (`project:936-977`: `signal_scope()`
  around the inspection, the exit rule unchanged) and `snapshot()`
  (`project:822-867`: the evidence memoized on the `Invocation`).
  `tests/test_project.py:736` passes with its exact error rows.
- [ ] T120 [US9] Update `update()` (`project:992-1071`; D-R, FR-052): `dirty is
  not False` refuses for the root and every child (`:1011`, `:1017`);
  `origin/HEAD` is read from row 6's symref instead of the child at `:1010`;
  the `tools` and `workflow` components need no Git, and after a failed version
  check `update()` spawns no Git child (M10); `signal_scope()` holds around its
  inspection and `default_signals()` around `confirm()` and the owner-tool
  delegates (R4, M1). `tests/test_project.py:652-670` and `:767-799` pass, and
  so do T114 to T116.
- [ ] T121 [US9] Run the US9 module, every earlier module and the 96 tests: all
  pass.

**Checkpoint**: Every subcommand that inspects a repository uses the one
evidence model.

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Documentation (FR-065), integration, traceability, and
verification.

- [ ] T122 [P] Update `README.md` (FR-065, SC-014; D3, D18, design Migration
  Plan step 5): the "Clean up Git worktrees" section opens with the five
  behaviour changes (plain `project clean` exits 1 on an incomplete report;
  `clean` refuses below Git 2.36; `--worktree P` refuses a freshly created
  merged worktree as `unstarted-branch`, and one whose reflog keeps no decisive
  entry as `reflog-unavailable`, each with its D18 remedy; and `--worktree P`
  removes a merged worktree whose upstream was deleted, keeping its branch);
  then the preview (`project clean ROOT --all-safe`) and the apply (`--apply`,
  the question, `--yes`), `--expect-plan` with the preview's digest, the gates
  in order with each reason's next step, the 16-per-run deferral, the narrow
  guarantee and its residual window, the result record and recovery (the stop
  block's `Next:` command and the partial-removal recovery), and the advice to
  close sessions in those worktrees before a batch apply. Correct "Apply
  actions are always explicit and target one branch or worktree."
  (`README.md:195`) for `--all-safe`; state Git 2.36 or later under Install
  (`README.md:17-19`); and give the exit-code line (`README.md:284-286`)
  `clean`'s 1 (an incomplete report or preview, and an apply that ends unknown,
  at the ceiling or past the deadline), 143 and 129, and Git's own status
  passing through. ASCII only.
- [ ] T123 [P] Update `AGENTS.md`: under "Runtime and verification", Git 2.36
  or later, and the clean tests in `tests/test_clean_*.py` and
  `tests/test_status_doctor_update.py`, with helpers in
  `tests/clean_support.py`, the launcher `tests/launch_project.py`, and `-k
  test_clean_ -k test_status_` to run them (rule 2); and a short section,
  "Cleaning up worktrees for a person": preview with `project clean ROOT
  --all-safe` and show it; apply with `--apply --expect-plan DIGEST` from that
  preview; never answer the removal question, or pass `--yes`, on a person's
  behalf unless they asked for that run; ask that sessions in the selected
  worktrees be closed first (D3). Leave the `OPENSPEC-SPECKIT-GLOBAL` block
  untouched, and do not edit `CLAUDE.md`.
- [ ] T124 Read the README's "Clean up Git worktrees" section alone and confirm
  SC-014: the five behaviour changes come first, and it says how to preview,
  confirm and pin a preview's digest, each exclusion reason with its next step,
  and the command to run after a stopped batch.
- [ ] T125 Retire `default_branch()` and `ancestor()` (`project:524-541`), and
  any baseline helper no caller still reaches (`print_clean_report()`,
  `matching_worktree()`, and `cleanup_report()` if no stage calls it), each
  checked by `grep` over `project` and `tests/`; plan.md's "Code touched, and
  what stays" names the same list (lead ruling R-34). No deletion happens
  before this task. The whole suite passes.
- [ ] T126 Complete `specs/004-project-clean-all-safe/traceability.md`: every
  one of the 101 rows names at least one test, and a script confirms each named
  test is defined as `def NAME` in a `tests/test_*.py` module and starts with
  its subcommand's prefix and the title in snake case (rule 1); if PR #19 has
  landed, the script reads the push-child scenario from `main`'s delta,
  otherwise from `origin/change/amend-clean-all-safe-push-pins`.
- [ ] T127 Check by script that every D18 and D14 literal of
  `tests/clean_support.py`, its placeholders substituted, equals a line or
  quoted string of design.md D18 or D14 character for character, and that every
  D18 and D14 string has a literal (SC-010); `TEXT` in `project` equals the
  literals (T008).
- [ ] T128 Run the whole suite in this worktree: `python3 -m unittest discover
  -s tests -v` passes; record the test count and the elapsed time, under 8
  minutes in `py-bench` (R11); run it under Python 3.10 too where an
  interpreter is available; and confirm by script that `git diff 961c405 --
  tests/test_project.py` changes only
  `test_clean_revalidates_a_worktree_after_confirmation` and adds the one
  `sys.modules` line to the loader, every other method's `ast` source being
  identical.
- [ ] T129 Run quickstart.md's "The Git 2.36 floor run", as plan review M18
  corrects it (the tests run from the repository): `git version 2.36.6`, then
  every selected test passing, with
  `test_status_the_sixteenth_scrubbed_name_on_git_2_36` listed by `-v` as run
  and passed rather than skipped, so that the floor job's `-k` selection
  catches it (plan review M14).
- [ ] T130 Run `/usr/bin/openspec validate --all --strict` (1.6.0 or later;
  plan.md, "Risks and Notes") and confirm every item passes.
- [ ] T131 Run quickstart.md's "Checks on the realization": every added line of
  `project`, `tests`, `README.md`, `AGENTS.md` and `.github` is ASCII; `git
  diff --stat main...HEAD` lists only the files of "Path Conventions"; every
  top-level function of `project` at `961c405` that plan.md's "Code touched,
  and what stays" does not list as changed or retired has identical source by
  `ast`; `parser()` gains options under `clean` only; and `requirements.txt` is
  unchanged (FR-064).
- [ ] T132 Walk quickstart.md's hand runs for User Stories 1 to 9, as plan
  review M19 to M21 correct them, at a real terminal and record any divergence
  as a defect against these tasks before the realization goes to the lead.
- [ ] T133 In `openspec/changes/add-project-clean-all-safe/tasks.md`, under
  "Speckit Handoff", change the Tasks line to `Tasks:
  specs/004-project-clean-all-safe/tasks.md (created by /speckit.tasks)`, as
  lane openRepoProject-1's archived changes record theirs. Tick no box there
  for this implementation: the landing, the archive and PR #19's ruling belong
  to the change's own governance record, not to this feature. `openspec
  validate --all --strict` still passes.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001, then T002, T003 and T004 at once.
- **Foundational (Phase 2)**: after T004. Lanes A to E at once; F after A and
  C; G after D and F; H after T023, beside G. Landing order as the brief sets
  it: timing, harness, environment, runner with the parsers and escaping,
  evidence, guard. Blocks every story.
- **US1 (Phase 3)**: after Phase 2.
- **US2 (Phase 4), US3 (Phase 5), US7 (Phase 9)**: after US1's checkpoint,
  beside each other.
- **US4 (Phase 6)**: after US2, since revalidation calls `modules_check()` and
  `hidden_state_probe()`.
- **US5 (Phase 7)**: the removal lane after US4, since both edit `rescan()` and
  `decide_stage()`; the text lane after US2, whose `registration-mismatch` row
  one of its tests reads, beside US4.
- **US6 (Phase 8)**: after US3, US4 and US5.
- **US8 (Phase 10)**: after US6 and US7.
- **US9 (Phase 11)**: after Phase 2, beside every clean story; T114's and
  T116's `clean` tests also need US1.
- **Polish (Phase 12)**: T122 and T123 after US1; the rest after every story.

### Critical Path

Setup, then lanes A and C, F, G, then US1 (T047, then its two lanes), US2, US4,
the US5 removal lane, US6, US8 and Polish.

### Within Each Phase

- Tests first, failing, except those marked as pins; then the implementation
  tasks, each ending with its tests passing; each phase ends by running the
  whole suite.
- A lane's writer owns its test module and its regions and functions; a
  conflict anywhere else is an ownership breach, stopped and reported to the
  lead (impl-slicing-004 section 7).
- Each lane merges into `004-project-clean-all-safe` with the whole suite run
  on the merged result; `main` is merged in as it moves; never a rebase or a
  forced push.

### Parallel Opportunities (fan-out)

| Window | Lanes at once | `project` functions per lane |
| --- | --- | --- |
| Phase 2 start | 5: A, B, C, D, E | A `TIMING`; B none (tests, and one loader line in `tests/test_project.py`); C `GIT_SCRUB`, `PROTOCOL_PINS`, `STATUS_PINS`, `git_env`, `git_argv`; D the five parsers; E `json_path`, `human_path` |
| Phase 2 end | 2: G, H | G `identity_probe`, `main_worktree`, `inspect_repository`, `verify_registration`, `status_probe`, `worktree_rows`, `classify`, `partial_removal_note`, `declared_tracking_branch`, `resolve_merge_target`, `cleanup_report`; H `Refused`, `clean_mode`, `run_clean`, `error_document`, `write_document`, `main` |
| US1 | 3: plan, apply, US9 | plan `check_clean_arguments`, `require_git`, `build_plan`, `select_entry`, `plan_completeness`, `gate_rows`, `plan_digest`, `plan_document`, `print_plan`, `check_plan`; apply `ask_removal`, `confirm_removal`, `revalidate`, `run_removal`, `rescan`, `decide_stage`, `apply_removals`, `apply_exit_status`, `result_document`, `print_result`; US9 below |
| After US1 | 6: US2 reflog, US2 index, US3 single, US3 push, US7, US9 | `reflog_gate`; `registration_gate`, `index_gates`, `modules_check`, `hidden_state_probe`; `build_plan`; `push_or_delete`, `show_push_plan`, `require_unchanged_cleanup_state`, `execute`; `resolve_clean_target`, `is_bare_name`, `main_worktree`, `declared_tracking_branch`, `resolve_merge_target`; `repo_state`, `discover`, `snapshot`, `check_rows`, `print_report`, `inspect_project`, `update` |
| After US2 | 2: US4, US5 text (plus US3, US7, US9 if running) | `revalidate`, `narrowed_ref_patterns`, `rescan`, `decide_stage`; `print_plan`, `print_result` |

The widest window is the one after US1: six lanes, each with its own test
module and a disjoint set of `project` functions.

---

## Parallel Example: Phase 2 start and the window after US1

```bash
# Phase 2 start, five writers:
Task: "Lane A: T005 to T007, TIMING and tests/launch_project.py"
Task: "Lane B: T008 to T011, tests/clean_support.py and its self-tests"
Task: "Lane C: T012 and T013, the scrub and the pins"
Task: "Lane D: T014 and T015, the five parsers"
Task: "Lane E: T016 and T017, json_path and human_path"

# After US1's checkpoint, six writers:
Task: "US2 reflog lane: T059, T060, T066"
Task: "US2 index lane: T061 to T065, T067"
Task: "US3 single lane: T069 to T071, T075"
Task: "US3 push lane: T072 to T074, T076, T077"
Task: "US7: T104 to T109"
Task: "US9: T114 to T121 (begun at Phase 2's checkpoint)"
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Phase 1 and Phase 2.
2. Complete US1: the preview, `--expect-plan`, the question, ordered removal
   with every branch kept.
3. **STOP and VALIDATE**: run the suite and quickstart.md's User Story 1 hand
   runs.

### Incremental Delivery

1. US2 and US3, the other P1 stories, beside US7 and US9.
2. US4, then US5, then US6; then US8.
3. Polish: documentation, integration, traceability, verification.

The realization ships as one pull request. Opening it, landing it, PR #19's
ruling (the change's task 1.7) and the archive belong to the lead and the
change's governance record, and are not tasks here.

---

## Requirement Coverage

Every delta scenario is named by at least one test task above, PR #19's
included (T074). By requirement:

| Requirement | Tasks |
| --- | --- |
| FR-001 | T033, T052, T096 |
| FR-002 | T048, T114 |
| FR-003 to FR-005 | T049, T051, T101, T096, T111 |
| FR-006 | T031, T029, T096 |
| FR-007, FR-008 | T032, T028, T064, T065 |
| FR-009 | T032, T094, T091 |
| FR-010 | T075, T076, T077, T072, T073, T074, T098 |
| FR-011, FR-012 | T056, T057, T092, T041, T087, T089 |
| FR-013 | T075, T070 |
| FR-014 | T076, T071 |
| FR-015 | T053, T044 |
| FR-016, FR-017 | T107, T104, T105 |
| FR-018 | T032, T108, T106 |
| FR-019 | T047, T048, T039 |
| FR-020 | T050, T066, T067, T100, T040, T061 |
| FR-021, FR-022 | T066, T059, T060 |
| FR-023 | T067, T062, T063 |
| FR-024 | T053, T038 |
| FR-025 | T051, T037 |
| FR-026 | T054, T043 |
| FR-027 | T049, T053, T069, T070 |
| FR-028 | T052, T057, T036, T042 |
| FR-029, FR-030 | T024, T099, T098 |
| FR-031 | T075, T101, T097 |
| FR-032 | T100, T097 |
| FR-033 | T049, T102, T040, T098 |
| FR-034, FR-035 | T056, T085, T093, T088, T090 |
| FR-036 | T047, T035, T093, T087, T089 |
| FR-037 | T057, T076, T045, T073 |
| FR-038 | T057, T091 |
| FR-039 to FR-041 | T017, T016, T076, T073, T110, T112 |
| FR-042, FR-043 | T051, T035, T053, T040, T111 |
| FR-044 | T052, T057, T111 |
| FR-045 | T050, T067, T061 |
| FR-046, FR-047 | T055, T084, T076, T079 to T083 |
| FR-048, FR-049 | T057, T085, T082, T083 |
| FR-050 to FR-052 | T117, T118, T119, T120, T114 to T116 |
| FR-053 | T024, T025, T048, T118, T021, T114 |
| FR-054 | T013, T012, T030, T077, T074 |
| FR-055 to FR-057 | T031, T015, T029, T030, T097 |
| FR-058 | T022, T023, T024, T018, T030 |
| FR-059 | T024, T117, T115 |
| FR-060 | T108, T106 |
| FR-061 | T033, T027 |
| FR-062 | T014, T015, T026 |
| FR-063 | T041, T088 |
| FR-064 | T047, T077, T131 |
| FR-065 | T122, T124 |
| FR-066 | T005 to T011, T126, T128 |
| FR-067 | T003, T129 |

Success criteria: SC-001 and SC-002 T041, T061, T097; SC-003 T030, T029, T074;
SC-004 and SC-005 T018, T026, T099, T089, T098; SC-006 T098, T102; SC-007 T090,
T045; SC-008 T045, T096; SC-009 T110, T111; SC-010 T016, T073, T127; SC-011
T065, T130; SC-012 T026, T126, T128, T129, T131; SC-013 T114, T115; SC-014
T124.

---

## Notes

- [P] marks a lane that runs beside another lane of its phase; [Story] maps a
  task to its user story; `traceability.md` maps each delta scenario to its
  tests.
- Verify that tests fail before implementing, except the ones marked as pins.
- Commit after each lane or phase at least, with `Lane: openRepoProject-2` in
  each commit body.
- LQ-3: if Brett Heap rules a follow-up change instead of PR #19 (option (b)),
  only the push child's treatment moves: T074, T077 and the push halves of T076
  and T073 (research.md R1). The delete-branch child keeps the pins either way
  (R5).
- R-31: `TIOCSCTTY` is untested on macOS, so the controlling-terminal tests of
  T008, T072 and T074 are a note for a local run there, no CI job running macOS
  (R-35); a failure on macOS goes to the lead before any skip is added.
- No task edits workBenches, openRepoShape, setup-openspeckit, `CLAUDE.md`,
  `requirements.txt`, or the change's files beyond T133's line.
