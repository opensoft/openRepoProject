Lane: openRepoProject-2

# Implementation Plan: Safe batch worktree cleanup

**Branch**: `004-project-clean-all-safe` | **Date**: 2026-10-11 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from
`specs/004-project-clean-all-safe/spec.md`, as reviewed (`aadd709`).

**Technical design**: `openspec/changes/add-project-clean-all-safe/`: the
proposal, `design.md` (decisions D1 to D20, Risks, Migration Plan, Open
Questions), `clarifications.md` (N1 to N5) and the three spec deltas
(`project-clean`, 65 scenarios; `project-clean-review-safety`, 18;
`project-command`, 17), ratified by Brett Heap on 2026-10-09 ("ratify, merge
#11 and run the runbook") and landed on main as `0050f3e` (PR #11). This plan
sequences that design by decision number and decides only what the change
leaves to the implementation ([research.md](research.md), R1 to R16). Where
the plan and the change differ, the change governs; where the design and a
delta scenario differ, the scenario governs.

## Summary

`project clean <root> --all-safe` previews, and with `--apply` removes, every
worktree of one repository that passes the gates, at most 16 per run, on a
removal path made safe to repeat: Git-first resolution, one bounded evidence
model shared with `status`, `doctor` and `update` on Git 2.36 or later, a
targeted revalidation before each removal, a removal child that is never
interrupted, and a reconcilable record for every target. Single-target
`--apply --action remove --worktree P` becomes a one-item batch. Every
`clean --json` prints one versioned document. The work is confined to
`project`, `tests/` (new test modules, one per lane, with their helpers and one
launcher), `README.md`, `AGENTS.md` and the CI workflow.

Implementation slices, in dependency order; each leaves the suite green:

1. **Baseline and test scaffolding** (research.md R10, R11, R15). The 96 tests
   pass at `aadd709`. The new tests go in modules of their own, one per lane
   (`tests/test_clean_<lane>.py`, `tests/test_status_doctor_update.py`),
   editing no existing test (lead ruling R-32). Their helpers, in
   `tests/clean_support.py`: a merged, published worktree with a commit of its
   own; bulk registrations written directly; a counting `git` wrapper (a POSIX
   `sh` script that logs, per child, its arguments, directory, pid, parent pid,
   process group (`/proc/$$/stat` on Linux, `ps -o pgid= -p $$` elsewhere) and
   which of the seventeen scrubbed names are set, runs an optional pre-hook,
   runs the real `git` by absolute path, runs an optional post-hook after
   `worktree remove`, and exits with Git's status; with no hook set it `exec`s
   Git, so the record is the child's own; a wrapper of the harness spike
   recorded each child's scrub names, pid, process group and parent before it
   `exec`ed Git, R10); the fake Gits of D1 and of the result scenarios
   (standard-error flood, SIGTERM ignored, 5,000 `!!` records, version 2.35.0,
   exit 0 without removing, a slow removal), each matching its subcommand
   anywhere in its arguments, since the seven pins come first; and a pty helper
   that makes the pty the controlling terminal (`TIOCSCTTY` after `setsid`) for
   the push-child tests (R-31). The launcher of R10 is
   `tests/launch_project.py`. The test module's loader
   (`tests/test_project.py:23-26`) gains `sys.modules` registration, a setup
   line and not a test (R-29). The `git-floor` CI job (FR-067, D17, R11) lands
   here too, so that every push runs the floor.
2. **Runner, parsers and the timing table** (D1, D2, D11, C4; R4, R10, R14).
   The module-level timing table, read at call time only (R-29); the child
   handle (`start`, termination without blocking: SIGTERM, then the handle's
   own kill and reap deadlines, advanced by the driver each tick (R-30);
   `reap`; the registry of live probe handles); the one-wide driver
   `run_bounded` (one selector over both pipes and a wakeup pipe, the 100 ms
   tick, a 4 KiB standard-error head); the scoped signal handlers; the five
   incremental parsers; filesystem calls on daemon threads under
   `min(5 s, work remaining)`; the seventeen-name scrub and the pins (R1); the
   memoized version check; path escaping. Tests: each parser fed byte by byte
   and whole (FR-062); two handles driven at once through the shared scrub,
   termination path and parsers (SC-012); the three fake Gits of D1; the
   escaping rules.
3. **Evidence pipeline and ladder** (D4, D6, D10, D11; R9). Row 1 once per
   invocation; rows 3 to 7 memoized per common directory; identity and two-way
   registration; the combined status probe and its bounds; the ladder as a pure
   function with its one reorder; the partial-removal note; the reflog read.
   Switch `cleanup_report()` only; `repo_state()` keeps today's reader. Parity
   is asserted as literal values.
4. **Resolution and the report** (D8, D14; R2, R6, R12, R13). Git-first
   resolution, the gitfile, bare and submodule rules and the bare-name test;
   the merge target and the 1 MiB manifest cap; report mode (256 rows, the
   D14 lines, exit 0, 1 or 2); the version 1 envelope, the extended error
   object and `plan_digest`; the `internal-error` guard.
5. **Gates and plans** (D10, D12, D13; FR-019 to FR-028). The gate order,
   the deferral, single mode (P first and exempt from the cap, other rows'
   omissions as notes), the `--all-safe` preview with D18's layout,
   `--expect-plan`, `invalid-arguments`, and the plan checks in their order.
6. **Apply** (D7, D9, D15, D18, D19; R3, R5, R8). The removal question,
   `confirmation-required`, the targeted revalidation, the removal child (5 s
   floor, 300 s ceiling, never signalled, the wait line), the rescan and
   reconciliation, stages, the exit table, the stop block, `--apply --json`,
   `probes` and `operations`. Push and delete-branch: Git-first resolution,
   single mode's row cap and bounds with the batch's completeness (any
   `inspection-error` row refuses them), the full re-inspection with its
   incompleteness refusals, the `remote-gone` push refusal, their children
   through the runner (R5), never signalled, a signal recorded meanwhile
   deciding the exit status (data-model.md), and the push child under the
   push-child exception (R1).
   `test_clean_revalidates_a_worktree_after_confirmation` moves to the result
   record (R15).
7. **Status, doctor and update** (D16, D-R; R2, R4, R5, R9). `repo_state()`
   onto the pipeline; `discover()` without a usable Git; doctor's `git` row
   and error rows; `Git: inspection-error (CODES)`; the JSON additions;
   `update`'s `dirty is not False` and `origin/HEAD` from row 6;
   `handoff()`'s `remote get-url` through the runner.
8. **README and AGENTS.md** (FR-065; D17). The "Clean up Git
   worktrees" section opens with the five behaviour changes, then the preview
   and apply, `--expect-plan`, the gates, the deferral, the narrow guarantee
   and residual window, the result record and recovery, and the advice to
   close sessions before a batch apply; the sentence at `README.md:195` is
   corrected; Install (`README.md:17-19`) states Git 2.36; the exit-code line
   (`README.md:284-286`) gains `clean`'s 1, 143, 129 and Git's status passing
   through. `AGENTS.md` gains the Git 2.36 requirement and the clean tests with
   their commands under "Runtime and verification", and a short section on
   cleaning up worktrees for a person (lead ruling R-32).
9. **Verification**. The whole suite; `traceability.md` naming a test for each
   of the 100 delta scenarios and for PR #19's "The push child reaches its
   remote", which R1 implements; `openspec validate --all --strict`; the ASCII
   check of added lines; the diff scope; the floor run (quickstart.md).

Code touched, and what stays. In `project`: `Refused` gains a code, path and
reason; `git()` and `git_text()` (`:68-74`) keep their names and place and call
the runner; outside a subcommand (as `tests/test_project.py:878` calls
`git_text()`) they run one probe with the 15 s budget and no handlers. The
version and common-directory memos live in a per-`main()` context, reset on
every call, and once the version check fails no Git child is spawned: `git()`
returns a failed result, so `handoff()` and `update()` run none (FR-053).
`execute()` (`:157-162`) gains only an optional environment argument (R5);
`discover()`, `repo_state()`, `cleanup_report()`, `print_clean_report()`,
`require_unchanged_cleanup_state()`, `clean()`, `handoff()`, `snapshot()`,
`check_rows()`, `print_report()`, `inspect_project()`, `update()`, `parser()`
and `main()` change; `default_branch()` and `ancestor()` retire, and so do
`print_clean_report()`, `matching_worktree()` and `cleanup_report()` once
`grep` over `project` and `tests/` finds no caller after `clean()` is rewritten
(lead ruling R-34). The new block sits after `discover()` and before
`repo_state()`, so the code above it, which features 002 and 003 cite, moves
only by what `Refused`, `git()` and `execute()` gain, and its names avoid those
taken (`registry`, `profile`, `manifest`, `snapshot`, `probe`, `git`).
Unchanged: `probe()` for non-Git children (`:863`, `:965`), `ask()`,
`confirm()`, `choose()`, `manifest()` (the merge target reads through a bounded
variant; `snapshot()` keeps `manifest()`), `new()` and its helpers, and
`benches`. `show_plan()` stays as it is for `new` and `update`; `clean`'s push
and delete-branch print `Working directory:` and their command through the
path-escaping printer, so a root holding a Cc, Cf, Zl or Zp code point prints
in the `$'...'` form (FR-041, SC-010).

## Citations

The change pins its `project`, test and README citations at `da33d92`
(proposal, "Dependencies and Sequencing"; `design.md:25-27` at `0050f3e`),
leaving the
re-pin to this feature. The rule at `961c405`, stated once here; every other
artifact of this feature cites `961c405`, read with `git show
961c405:<file>`, since from T004 (`a0368ac`) this branch's `project` differs
from it, and so do `tests/` from T009 and one line of `README.md` from #32
(`e9d6711`), a line no citation names:

- `project`: lines 1 to 203 are identical; a citation at line 274 or later
  (`manifest()` onward) is N + 148 (141 lines from PR #8, 7 more from PR #17
  inside `known_obstacles()`); lines 204 to 273 (`da33d92`'s `new()`) have
  no uniform offset and are re-read. Checked by `diff`: `da33d92` lines 274
  to the end equal `961c405` lines 422 to the end.
- `tests/test_project.py`: the cited `clean` tests are N + 430 (393, 409,
  450, 542 and 590 become 823, 839, 880, 972 and 1020).
- `README.md`: the clean-section citations are N + 89 (106 and 110 become
  195 and 199), the exit-code line N + 90 (194-196 becomes 284-286), and
  Install (17-19) is unmoved.
- `openspec/specs/project-command/spec.md`: N + 22 (22, 31 and 40 become
  44, 53 and 62); `project-clean` and `project-clean-review-safety` are
  unchanged since `da33d92`.
- Counts: the design's "The other 90 pass unchanged" (Migration Plan, step
  6) is 92 at `961c405`, which PR #17 brought to 96 tests.
- One citation is off at its source: D8's `project:401` names the line two
  above the `no-merge-target` message, which is `da33d92:403`, now
  `project:551`; PR #19 corrects D8 to `project:403`.
- Packet citations (`BA:N`) are at `da33d92`, the proposal's key; research.md
  R12 names that commit beside the packet's full path.

Table rows may exceed 79 columns, as in features 002 and 003.

## Technical Context

**Language/Version**: Python 3.10+ (the README's requirement); CI runs every
job of the `test` matrix on `ubuntu-latest` only (Brett Heap's decision of
2026-10-15, #32; lead rulings R-35 and R-46). Git 2.36 or later wherever a
repository is inspected: 2.43.0 in the benches, 2.36.6 in the floor job.
Local runs use Python 3.12.3 in the `py-bench` container.

**Primary Dependencies**: Python standard library only; `project` adds the
imports `errno`, `selectors`, `signal`, `stat`, `threading`, `time` and
`unicodedata`. PyYAML (`requirements.txt`, YAML inspection only) is
untouched; no dependency is added (FR-064). Tests use `unittest`,
`unittest.mock`, `subprocess`, `os` and the existing pty and in-process
helpers.

**Storage**: N/A. Nothing is persisted; a plan is never stored or reused
(FR-025).

**Testing**: `python3 -m unittest discover -s tests -v`, on disposable
repositories, with the counting wrapper, the fake Gits and the launcher
(R10). At `aadd709`, 96 tests ran OK in 17.5 s in `py-bench` (the plan
research measured 48 to 52 s on another host; the harness spike measured
120.3 s at load 126 to 136, and 91.4 s for its copy of `project` with every
CLI run through the launcher).

**Target Platform**: Linux and macOS, at a terminal and in scripts; CI runs
Linux only (R-35). Non-UTF-8 path scenarios run on Linux only, and are skipped
with their reason on macOS, as a person's local run may do.

**Project Type**: CLI, one executable file (`project`).

**Performance Goals**: the bounds the change fixes, not throughput: a run
with no removal, push or branch deletion in flight ends within 64 s of its
start, not counting time at the question (SC-004); a removal in flight adds
at most 300 s; each probe child gets `min(5 s, work remaining)` (SC-005);
each revalidation spawns at most 5 Git children and the final rescan 3
(SC-006). Task 2.1's fit holds them: at 128 rows and 16 targets the 16th
removal spawns at 23.6 s with 26.4 s left, and 256 report rows take 19.9 s
(task 2.1's measured medians; D14's model at BA's 150 ms per child gives
39.15 s and 41.85 s).

**Constraints**: local evidence only and no network (the pins, R1); ASCII in
all added text; no flag outside `clean`, no configurable limit, and no time
scale read from the environment, a flag or a file (R10); Python 3.10
compatibility in `project` (`start_new_session=True`, never `process_group=0`
or `preexec_fn`; daemon threads, never a `concurrent.futures` pool; C4; the
tests' pty helper may use `preexec_fn` for `TIOCSCTTY`); one executable file;
every existing test passing unchanged but one (R15); every job of the `test`
matrix and the floor job green (SC-012; lead ruling R-46).

**Scale/Scope**: `clean` rebuilt in three modes; `status`, `doctor` and
`update` moved onto the evidence model; 67 FRs and 100 delta scenarios (65,
18 and 17), each with at least one test named after it, beside the unit
tests of the parsers, ladder, gates, digest, escaping and exit table.

**Fixture and timing budget** (R10, R11):

| Item | Budget |
| --- | --- |
| largest registry | 257 rows, written directly: 0.93 s here, against 24.0 s for 257 `worktree add` children |
| status-bound fixture | 4,097 untracked files: 4.3 s to create |
| partial-deletion fixture | about 8,000 tracked files, one commit per test class (20,000 took 20.2 s to create and commit) |
| caps | never scaled: 128 and 256 rows, 16 targets, 64 and 4,096 records run at their real sizes |
| time | every timing constant in one table, read at call time and replaced by the launcher; each time-bound test names its own factor or table (R-29): about 0.03 to 0.05 for the ceiling and deadline tests, with no Python wrapper, and the `sh` wrapper or the real table for counting tests; timing tests assert ratios and ordering, the SIGTERM-to-SIGKILL gap at 0.9 grace or more, never wall-clock values |
| one test | under `run_cli`'s 20 s timeout |
| whole suite | under 8 minutes in the bench, under 6 minutes per CI job |

**CI shape** (R11): every job of the `test` matrix (`ubuntu-latest`, Linux
only since #32; R-35, R-46) runs the whole suite unchanged;
one new job, `git-floor`, on `ubuntu-latest` with Python 3.10, checks out, sets
up Python and installs `requirements.txt` as the `test` job does, then builds
Git 2.36.6 from kernel.org's tarball (sha256 checked), caches it by version and
runner OS, puts it first on PATH, checks `git --version`, and runs `-k
test_clean_ -k test_status_ -k test_doctor_`. At `961c405` that selection ran
15 tests, OK, in 7.7 s on task 2.2's build.

No NEEDS CLARIFICATION remains: the change decides every technical question
but those [research.md](research.md) settles, and its one open item, the
push-child exception (LQ-3, R1), is planned under a stated assumption.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

`.specify/memory/constitution.md` is the unfilled template, so there are no
constitution gates. What governs instead: the ratified change
(`openspec/changes/add-project-clean-all-safe/`: the three spec deltas,
`design.md` D1 to D20, `clarifications.md` N1 to N5) and the lane's rules
(ASCII-only text, the lane line on every file, plain pushes only, merges
never rebases, no work outside this worktree). Pre-research: pass, nothing to
evaluate. Post-design: pass; the Phase 1 artifacts cite the design and depart
from its text only where research.md records why: the push-child exception
(R1, awaiting Brett Heap's word on PR #19), the lead's rulings R-26 to R-32
(R10, R8, R1, R10, R14, R10, R15) and R-35 (R11), D1's handler span (R4) and
D2's `waitpid` wording (R14).

## Project Structure

### Documentation (this feature)

```text
specs/004-project-clean-all-safe/
  spec.md                    feature specification (/speckit-specify)
  checklists/requirements.md
  plan.md                    this file (/speckit-plan)
  research.md                Phase 0 (/speckit-plan)
  data-model.md              Phase 1 (/speckit-plan)
  contracts/project-clean.md Phase 1 (/speckit-plan)
  quickstart.md              Phase 1 (/speckit-plan)
  tasks.md                   Phase 2 (/speckit-tasks)
  traceability.md            delta scenario to test name (implementation)
  hand-runs.md               T132's hand-run record (lead ruling R-50)
```

### Source Code (repository root)

```text
project                      the single executable: clean rebuilt; status,
                             doctor and update on the evidence model
tests/test_clean_<lane>.py   new: one test module per lane (R-32)
tests/test_status_doctor_update.py
                             new: the status, doctor and update tests
tests/clean_support.py       new: the helpers every new module imports; not
                             collected by discovery
tests/launch_project.py      new: loads project, replaces its timing table,
                             calls main() in a child process (R10)
tests/test_project.py        one method rewritten (R15) and one loader line
                             added (R-29); nothing else
README.md                    "Clean up Git worktrees", Install, exit codes
AGENTS.md                    Git 2.36, the clean tests and a section on
                             cleaning up worktrees for a person
.github/workflows/tests.yml  the git-floor job added in the first slice; the
                             `test` job unchanged
openspec/changes/add-project-clean-all-safe/
                             the ratified change; read, not changed by the
                             implementation, except its tasks.md: four
                             hunks from the specify and plan commits (PR
                             #11's governance links, the Speckit Handoff's
                             feature lines) and T133's Tasks line; a merge
                             resolves their conflict with PR #19 when main
                             gains it (analyze M8)
```

**Structure Decision**: one executable; its new tests in modules of their own,
one per lane, with the helpers in `tests/clean_support.py` and the launcher in
`tests/launch_project.py` (lead ruling R-32). The feature adds those files and
the files under `specs/004-project-clean-all-safe/`, and edits `project`,
`tests/test_project.py` (one method and one loader line only), `README.md`,
`AGENTS.md` and `.github/workflows/tests.yml`. `CLAUDE.md` and the other agent
files at the root are not edited: they hold no Speckit plan markers, and
feature 002's plan edited none; `AGENTS.md` gains its sections by hand, outside
the `OPENSPEC-SPECKIT-GLOBAL` block.

## Risks and Notes

- **The push-child exception (LQ-3)**: planned to PR #19 (draft, after its
  review fixes) for Brett Heap's word; if he rules a follow-up change
  instead, only the push child's treatment moves (R1). The delete-branch
  child carries the pins either way (R5).
- **Test layout (lead ruling R-32)**: the new tests live in new modules, not
  in `tests/test_project.py`, which departs from design Migration Plan step 6
  and the proposal's Impact; the feature PR body states it for Brett Heap's
  word, and if he declines, the new modules fold into `tests/test_project.py`
  before the merge (R15). `AGENTS.md` (T123) is outside the proposal's
  Impact list too, which names `project`, `README.md` and
  `tests/test_project.py`, so the PR body states it as well. The `git-floor`
  job's place in Setup is no departure: design D17 and Migration Plan step 4
  put the job in feature 004 and name no slice.
- **CI runs Linux only (lead ruling R-35)**: since Brett Heap's decision of
  2026-10-15 (#32, `e9d6711`), every job of the `test` matrix runs on
  `ubuntu-latest` (R-46) and no CI job runs macOS, where the proposal's
  Impact says the suite runs "on Linux and macOS ... as CI runs". The
  OpenSpec text stays as written, and the feature PR body notes the
  difference.
- **Scenario count**: PR #19 adds one scenario, "The push child reaches its
  remote"; its test is written whether or not PR #19 has landed, and
  `traceability.md` names it (slice 9).
- **macOS timing headroom, a local-run note (plan review U1, unverified)**:
  R-29's factors were measured on Linux only. The harness spike, at load 124 to
  134 on 32 cores, counted spurious timeouts in 5 runs per child budget: bare
  `git` 1/5 at 0.025 s and 0.05 s and 0/5 at 0.1 s, 0.25 s and 0.5 s; the `sh`
  wrapper 5/5 at 0.1 s and below and 0/5 at 0.25 s and 0.5 s; the Python
  wrapper 5/5 up to 0.25 s and 3/5 at 0.5 s. At the factors R-29 names for the
  ceiling and deadline tests (about 0.03 to 0.05) the probe budget is 0.15 to
  0.25 s. The plan review measured real Git children at 10 to 20 ms median and
  50 to 119 ms at worst on a loaded host. macOS was not measured, so a
  time-bound test run there may time out a real probe; no CI job runs macOS
  (R-35), so this is a note for a person's local run, not a CI risk. Not
  resolved here.
- **`TIOCSCTTY` on macOS, a local-run note (R-31)**: the push-child terminal
  tests need the pty as the controlling terminal; `fcntl.ioctl(0,
  termios.TIOCSCTTY, 0)` after `setsid` was proven on Linux only, and is
  untested on macOS, where no CI job runs (R-35): a note for a local run, for
  tasks to state.
- **Existing tests that guard the switch**: `tests/test_project.py:736`
  asserts the exact set of doctor error rows, `:586` reads `status` of a
  linked worktree and expects that worktree's branch, and `:916` keys rows by
  branch (R15).
- **Text in `project`**: four existing lines hold an em dash (`:197`,
  `:915`, `:928`, `:1136`); the ASCII rule binds added text only.
- **OpenSpec CLI**: validate with `/usr/bin/openspec` (1.6.0 or later;
  1.13.1 in `py-bench`); the 1.2.0 first on some PATHs misreports two main
  specs.
- **Ordering**: never rebase; merge `main` into this branch as it moves.

### Open questions for Brett Heap

The feature PR body lists these for his word:

- **LQ-7, the delta's two exit rules** (lead ruling R-59): a write that
  fails in a preview or report after its plan is built exits 2 as
  `internal-error` (R-55), by the `project-clean` delta's rule for an
  unexpected exception before the apply phase, while the delta's preview
  rule gives exit 2 only to a refusal raised before a plan is built; and a
  reader that stalls can hold a run past the delta's 64 s bound, which does
  not cover a write blocked by its reader. R-55 stands until he rules
  (research.md R4; contract, "Exit statuses").

The others are recorded where they apply: LQ-3, the push-child exception
(R1); LQ-4, the preflight's scope (R16); and LQ-5, the remedy reading
(contract, "Human output").

## Complexity Tracking

None. There is no constitution gate, so there is nothing to justify.
