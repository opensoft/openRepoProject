Lane: openRepoProject-4

# Implementation Plan: Project overview

**Branch**: `005-project-overview` | **Date**: 2026-10-22 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/005-project-overview/spec.md`
at `7f4ab94` (its commit 3al; its 72 clarifications, Brett Heap's answers
of 2026-10-21 folded in and his words on the held items in C-72), with its
17 checklists and `clarify-questions.md`.

**Technical design**: `openspec/changes/add-project-overview/` as amendment
A1 at `e4a30fc` leaves it (PR #34; Brett Heap, "ratify 34", 2026-10-22):
the proposal, `design.md` D1 to D13, the two spec deltas (12 ADDED
requirements and 62 scenarios in `project-overview`, one MODIFIED
requirement with 2 scenarios in `project-review-safety`) and
`clarifications.md` N1 to N4. Where this plan and the change differ, the
change governs; where the spec settles a reading of the change, the spec
does. This plan decides only what they leave to the implementation
([research.md](research.md), R1 to R19), records Brett Heap's word on the
held items and keeps each in its own place (R20: every one chosen, O1 to
O16 and D5's clause 2).

**Authority**: Brett Heap, 2026-10-22T19:46:57Z: "lane 4 plans 005 now".
That word moves C-56's order (the plan after feature 004's merge) for this
plan step only, as C-21's moved the specify step, and spec commit 3ae
records it in C-56; it gives no word for tasks or implementation
(research.md R1, R2). Brett Heap, 2026-10-22T21:24:03Z: "yes, recommended
for O1-O10", and 2026-10-23, "yes, recommended for O3, O5, O8-O11 and D5
clause 2" (12:19:11Z) and "yes, recommended for O12-O16" (13:30:30Z), recorded
in C-72, choose options for change 2 and are no word for the tasks or the
implementation either (R20).

## Summary

`project overview [--root D]... [--attention] [--json] [--strict]` reports,
in one bounded, local and read-only run, every project under the configured
roots: one row per repository identity with its worktrees, findings by
attention category, and at most one gated `project clean` command per row,
advice to review and never permission. It is one new subcommand of the
`project` script, driving feature 004's child handle, parsers and evidence
deciders from a loop of its own that runs up to four Git children and many
bounded filesystem tasks at once, under a 60 s deadline, and changes no
other subcommand. The work is confined to `project`, new test modules
under `tests/`, `README.md`, one CI line and, if feature 004's T123 lands,
one `AGENTS.md` sentence.

Implementation slices, in dependency order; each leaves the suite green:

1. **Base, factoring and scaffolding** (research.md R2, R3, R18). Merge
   `origin/main` after PR #33 lands; re-cite R3's list there. Factor
   `start_child()` and `conclude()` out of `run_bounded` with no change in
   behaviour, add the `overview` branch to `Invocation`, the subparser
   (help texts, the empty `--root` check) and the dispatch line, the
   configuration-path test and the version check. Add
   `tests/overview_support.py`: scratch `HOME`, explicit `PROJECTS_DIR`,
   `WORKBENCHES_ROOT` at an empty directory, fake owner tools first on
   `PATH`, the audit hook, the snapshot, the allow-list on feature 004's
   counting wrapper. Scenarios 47, 55, 56 and 64. The three 004-touching
   changes ship in this slice alone, under the gates below.
2. **Discovery** (R7, R10). `FsTask`, the root tasks with their cancel
   flag, markers, candidates, the dedupe and the root, entry and candidate
   caps. Scenarios 1 to 4, 13, 14 and 23; PN-9, PN-13.
3. **The loop and the scheduler** (R4, R6). `OverviewLoop`, the four
   slots, the per-common-directory rule, the identity step and the merge by
   `(dev, ino)`, the barrier, the deadline and the signals. Scenarios 16,
   18, 19, 20, 57 and 58; PN-10.
4. **Repositories and rows** (R5, R8, R9, R14, R17). The registry, A1
   design D3's layouts, the manifest reader, the extension read, the
   keep-filter, change 1's resolver (`resolve_merge_target`, called on the
   kept records), the merged set, the row tasks, the twins, the work-tree
   probe, the re-verification, the status probe and classification through
   `row_evidence`. Scenarios 5 to 12, 15, 17, 21, 22, 24 to 34, 62 and 63;
   EC-031 to EC-033.
5. **Findings, gates and messages** (R12, R13). The attention table, the
   default-branch set, the row and repository gates, the reflog gate, the
   composer and the suggestions. Scenarios 35 to 43 and 51 to 54.
6. **Output** (R11, R15, R16). The envelope, the human report, the writer
   in its raising span and the exit-2 outputs. Scenarios 44 to 46, 48 to
   50 and 59 to 61.
7. **Documentation, CI and records** (FR-048, FR-050, FR-051). The README
   section, one `-k test_overview_floor_` in the `git-floor` job, the
   `AGENTS.md` sentence if T123 has landed, the test names in
   [traceability.md](traceability.md), the hand runs of
   [quickstart.md](quickstart.md), gate (b)'s script run again over the
   final `project`, and the full-length timing.

Each held item sits in its own row, decider, term or composer branch
(research.md R20), and Brett Heap's words chose every one for change 2 (C-72).
O11's part 1 is built now, as the plan's reading of a conflict in ratified A1
(R9); O9 (A), O10 (A), O12 (A) and O14 (A) keep A1's behaviour as ratified;
O15 (A) and O16 (a) are built now, as the spec builds them; and the rest, D5's
clause 2 among them, now chosen by name, are built in their chosen form once
A1's re-alignment lands at PR #34, in one commit after PR #19's ratification,
he reviewing the final text before #34 merges; until then the ratified text
stands. C-72 at `7f4ab94` (spec.md:998-1006) gives the order: "A1's ordering
rule (its `proposal.md:1278-1284`) is the four LQ items' and reaches O10
(LQ-15's extension) and O5 (item 9, owed under it); the other chosen items
that change A1's text, its items 2, 6, 7, 8, 10 and 11, rest on his word for
change 2 and on #19's rounds; and items 2 and 6 to 11 reach A1 in the same
re-alignment commit, which follows #19's ratification, he reviewing the final
text before #34 merges, while O9 (A) and O10 (A) keep A1's text as ratified and
O11's part 1 is a text re-alignment on a lane finding." O13 (A) reaches A1 in
that commit too (C-72). A change in his review of the final text lands as a
change to that place and its tests alone, with one exception: a change to
O11's part 1 would also re-word the scenario "A separate git directory" of
change 2 and of this spec (research.md R20, O11). traceability.md lists
each item's behaviour test and the assertions that flip.

### Gates on the three 004-touching changes

Slice 1 changes feature 004's code in three places: `Invocation` (one
branch), `run_bounded` (split into `start_child()` and `conclude()`) and
`parser()` with `main()` (the `overview` subcommand). Lane
openRepoProject-2, which owns feature 004, agrees to them in principle as
refactors that keep its behaviour unchanged, on five conditions, each a
gate on the change and on its verification (research.md R3):

- **(a)** feature 004's existing tests pass with no edit (new tests may be
  added): the whole suite green, and no diff in feature 004's test files
  or helpers against the base.
- **(b)** the split keeps `clean`'s output, JSON and human,
  byte-identical: every probe count, every per-probe budget and deadline
  figure and the cut semantics (R-80 P-2, the deadline-stopped marker),
  shown by a side-by-side run of the base and the split `project` over
  `clean`'s fixtures comparing probes, operations, exit statuses,
  documents (each `observed_at` masked) and the wrapper's child logs, and
  the same commands without `--json`, standard output and standard error
  byte for byte ([quickstart.md](quickstart.md)).
- **(c)** the `Invocation` branch leaves `clean`'s 50 s work deadline and
  10 s reserve untouched: its `clean` branch is not edited, and a unit test
  pins both figures.
- **(d)** `parser()` and `main()` add `overview` only: `clean`'s arguments,
  help text, refusals and exit codes unchanged, and `project SUB --help`
  byte-identical for every other subcommand (`new`, `benches`, `status`,
  `doctor`, `update`, `clean`).
- **(e)** the changes land on `main` after PR #33; if the split changes
  anything PR #19's text describes of the driver or bounded work (its D1,
  D2, D9 and D14), feature 005's spec says so and PR #19 is not edited for
  it.

Lane 2 or lane openRepoProject-3 reads the 004-touching diff before
feature 005 merges, and slice 1's pull request quotes the checks of (a) to
(d).

## Citations

- `project:N`: line N of feature 004's `project` at `d6bac50` (branch
  `004-project-clean-all-safe`, draft PR #33), read with `git show`; the
  other files of that branch at the same commit, as `tests/NAME:N` and
  `specs/004-project-clean-all-safe/NAME:N`. Revision 1 moved every cite
  from `4b4c36b`, revision 3 from `0a82a62` and revision 4 from `211e43d`;
  a later head is re-cited before tasks are written, and `main` after PR
  #33 lands (research.md R1). Its later head `f3724fc` changes documents
  only, `project` and the tests unchanged since `d6bac50`, and its head
  `d8724e2` (R-365) changes no definition the overview reuses but `TEXT`,
  which gains one row (research.md R1).
- `A1:N`, `A1 design.md:N`: change 2's `specs/project-overview/spec.md`
  and `design.md` at `e4a30fc` (branch
  `change/amend-project-overview-clarify-answers`).
- `PCM:N`, `PCL:N`, `#19 design.md:N`: change 1's
  `specs/project-command/spec.md`, `specs/project-clean/spec.md` and
  `design.md` at `e0b1671` (branch `change/amend-clean-all-safe-push-pins`,
  PR #19, round (p), R-365 and R-377), whose `project-command` and
  review-safety specs equal its round (n)'s, `2250830`, accepted as lane
  openRepoProject-2's R-345, and whose `project-clean` spec gains F-1's (b)
  text beside an unread row (PCL:354-361, :540-547, :1217-1225) and a
  rewording at :378-380; moved from `ccc52b9` in revision 1, from `20084cd`
  in revision 3, from `2250830` in revision 4 and from `88d0d36` in revision
  8. The implementation re-pins at #19's ratified head.
- POD, PRSD, CMD, CLN, DI, BA and the labels [E], [L], [G], [R] and [P]:
  as [spec.md](spec.md) defines them.
- The lane's A1 re-alignment draft, held for Brett Heap's review and the
  source of options only, not of behaviour: every item, 1 to 11, with its
  note on row 4c's exit 1 under item 9, as read at sha256
  `558b0c298f5c5ce6bc7a9d91cc0279e6b32b7af877140f34423ebac2cc262579`
  (2,928 lines; research.md R9, R12, R20), its warnings in PR #19's round
  (n) words. Earlier revisions read it at `00205d73`, `10890e2c`,
  `8ce4e9fb`, `811b9cef` and `c5840a66` (research.md R20).
- Lane openRepoProject-3's reads of this plan: W96's at `a80f10b`, with its
  delta reads at `aeb0bb2`, `6fb619c`, `664461f`, `06b16e1` and `464c361`,
  W112's delta reads at `d500312` and `39f4ab6`, and W132's at `d0a7c07`;
  revisions 2 onward take each of their findings (research.md, "Revision 2"
  onward). Lane openRepoProject-4's own nine-reader review of revision 7 at
  `39f4ab6`, with its triage: revision 8 takes its choices' marks and pins,
  and revision 9 its FIX-PLAN items.

## Technical Context

**Language/Version**: Python 3.10+ (the README's requirement; CI's `test`
matrix runs 3.10 and 3.12 on `ubuntu-latest`). Git 2.36 or later: 2.43.0
in the benches, 2.36.6 in the `git-floor` job. `os.path.realpath(...,
strict=True)` needs 3.10, the floor already in force.

**Primary Dependencies**: the Python standard library only, every module
the overview needs already imported by `project` at `d6bac50`
(`selectors`, `signal`, `threading`, `os`, `stat`, `json`, `argparse`);
PyYAML through the existing requirement, for manifests. No dependency is
added (FR-047).

**Storage**: N/A. Nothing persists beyond the invocation (FR-040).

**Testing**: `python3 -m unittest discover -s tests -v`, over temporary
fixtures, with feature 004's counting wrapper, fake Gits, death watch and
launcher (`tests/clean_support.py`, `tests/launch_project.py`) and, in
`overview_support.py`, a probe shim behind the counting wrapper, and new
modules `tests/test_overview_*.py` with `tests/overview_support.py`
(research.md R18). At `d6bac50` the suite holds 491 test methods; all
pass unchanged after this feature (FR-049).

**Target Platform**: Linux and macOS, at a terminal and in scripts; CI runs
Linux only. Non-UTF-8 path tests run on Linux and are skipped on macOS
with their reason.

**Project Type**: CLI, one executable file (`project`).

**Performance Goals**: the bounds the change fixes: a run ends within 64 s
of the moment its deadline is set, plus rendering, but while a filesystem
call is stuck in the kernel (SC-005, EC-001); each Git child and each
filesystem task gets `min(5 s, deadline - now)`; at most four Git children
at once, one per repository. Governance task 2.1 measured the caps' worst
case at 48.3 s of 60 s before LQ-11's extension read and work-tree probe
added children; at PR #19's measured costs the lane's re-alignment draft
(item 3, text only) puts the worst case with them at 55.3 s run one at a
time, and at 62.8 s (57.2 s four at once) were all 128 candidates' identity
probes read again one option per child (EC-032), which the deadline then
cuts as FR-012 states.

**Constraints**: local evidence only, no network and no mutation (FR-040;
research.md R3); ASCII in every added fixed text; no flag outside
`overview`, no configurable limit and no time read from the environment,
a flag or a file (FR-047); daemon threads, never a `concurrent.futures`
pool; `start_new_session=True`, never `process_group=0` or `preexec_fn`
(feature 004's C4); one executable file; every existing test unchanged.

**Scale/Scope**: one subcommand; 51 FRs and 64 delta scenarios (62 and 2,
one of them A1's), each scenario with at least one test named after it,
beside unit tests of the deciders, the keep-filter, the composer, the
counts and the orders (FR-049).

**Fixture and timing budget** (research.md R18):

| Item | Budget |
| --- | --- |
| 512-row cap | 505, 10 and 5 rows in three repositories, registered |
| 128-candidate cap | 129 directories holding `.project.json`, no Git |
| 32-root and 4,096-entry caps | 33 roots; 4,097 entries in one root |
| status bounds | 65 and 64 ignored files; 4,097 untracked files |
| reflog bound | files of 65,535 and 65,536 bytes, written directly |
| deadline | in-process, 6 s and 0.5 s (ratio 12); bound 10 s |
| one test | under `run_cli`'s 20 s timeout |
| overview modules | under 4 minutes in the bench |
| whole suite | under 10 minutes per CI job |

Feature 004 measured 257 rows registered directly in 0.93 s against 24.0 s
by `worktree add`, and 4,097 untracked files in 4.3 s
(`specs/004-project-clean-all-safe/plan.md:259-260`). The row-cap fixture
is one root with three repositories registered directly
(`register_worktrees`, prefixes `a-`, `b-`, `c-`), 520 rows in all, the
second holding one real merged worktree among its first 7 rows; the cap
falls inside the second, so 8 rows are past it, 3 in the second and 5 in
the third (research.md R18). The other sizes are stand-ins, by choice, that
reach the same bound with a smaller fixture: 129 candidates for scenario
13's 130, 4,097 entries for scenario 14's 4,100, and 65 and 64 ignored
files for scenario 21's 10,000 and exactly 64.

**CI shape**: the `test` matrix runs the whole suite unchanged; feature
004's `git-floor` job gains `-k test_overview_floor_` beside its own
prefixes, its one change (FR-050; A1's Impact).

No NEEDS CLARIFICATION remains: the change, A1 and the spec decide every
behaviour but what research.md R1 to R19 settles, and the held items, every
one chosen, are planned each in its place, most landing with A1's
re-alignment (R20).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

`.specify/memory/constitution.md` is the unfilled template, so there are no
constitution gates. What governs instead: change 2 as A1 leaves it, this
feature's spec, and the lane's rules (ASCII text, the lane line on every
file, plain pushes, merges never rebases, no work outside this worktree).

- Pre-research: pass, nothing to evaluate.
- Post-design: pass. The artifacts cite the change and depart from its text
  only where research.md records why: the plan written before feature 004
  merges, on Brett Heap's word (R1); two read ends on one selector in place
  of D1's one self-pipe (R4); and the plan's own readings where the change
  leaves a choice (R5's manifest place, R10, R11, R13 to R16), with one
  reading of a conflict in ratified A1, the `core.worktree` read's unset
  exit 1 (R9; O11's part 1). They keep
  A1's Non-Goals: the merge target is change 1's `resolve_merge_target`,
  called on the kept records, and no second classifier, resolution order
  or path escaper is written (A1 design.md:73-74; R3).

## Project Structure

### Documentation (this feature)

```text
specs/005-project-overview/
  spec.md                  # the feature specification (unchanged here)
  clarify-questions.md     # the clarification record (unchanged here)
  checklists/              # 17 requirement-quality checklists (unchanged)
  plan.md                  # this file
  research.md              # R1 to R20
  data-model.md            # entities, states, exits, constants
  contracts/
    project-overview.md    # CLI, JSON, human report, every message
  quickstart.md            # hand validation of the built feature
  traceability.md          # FRs and scenarios to regions and modules
  tasks.md                 # not written by this plan (/speckit-tasks)
```

### Source Code (repository root)

```text
project                      # new regions after feature 004's:
                             #   overview contracts, discovery, loop,
                             #   collect, findings, render; changed:
                             #   Invocation (one branch), run_bounded
                             #   (factored), parser(), main()
tests/
  overview_support.py        # fixtures, isolation, snapshot, audit hook,
                             #   probe shim, seams, pty runner
  compare_clean_base.py      # gate (b)'s side-by-side run, by hand
  test_overview_*.py         # one module per requirement group
  clean_support.py           # feature 004's, reused unchanged
  launch_project.py          # feature 004's, reused unchanged
README.md                    # a `project overview` section (FR-048)
AGENTS.md                    # one sentence, only if T123 lands (FR-051)
.github/workflows/tests.yml  # one -k prefix in git-floor (FR-050)
```

**Structure Decision**: the overview lives in `project` beside the
evidence model it shares, as change 2's Impact and FR-047 require; its
regions follow feature 004's last region so that a re-cite of feature
004's lines moves none of the overview's. The README section sits after
"Understand a project" and before "Clean up Git worktrees", since its
suggestions lead to `project clean`.

## Risks and Notes

- **Feature 004 moves under the plan.** Revision 1 re-cited every line at
  `0a82a62` (R-322, T6 to T8, doc round 21), revision 3 at `211e43d`
  (R-332, R-336, doc round 22), where no reused definition changed but in
  its line and `config_key_unset` is new, and revision 4 at `d6bac50` (doc
  round 23, R-324's words in `TEXT`, its one changed definition; research.md
  R1). A later head is re-cited the same way before tasks, and `main` after
  PR #33. A change to a reused decider's signature or result is the one
  re-plan trigger.
- **The 004-touching changes** stay inside lane 2's five conditions
  (Summary, "Gates"); a failed gate stops slice 1 and returns the change
  to lane 2 and the lead, never an edit of feature 004's tests.
- **PR #19 not ratified as written.** The overview cites [E]'s `commondir`
  check, status pins, extension read, work-tree probe and
  configuration-path test as pending #19; a different ruling there changes
  the reused constants and deciders, which the overview takes as they land.
- **Lane openRepoProject-2's open safety fixes to feature 004**
  (2026-10-23: a `core.ignoreCase` pin missing from the status and removal
  probes; a nested `.git` inside a tracked directory unseen) may change
  `STATUS_PINS`, `STATUS_PROBE`, `StatusParser`, `status_warned` or
  `status_probe()`. The overview takes the first four by reference and so
  inherits a fix there; it mirrors `status_probe()`'s composition
  (research.md R3), so each re-cite diffs that function and carries any
  change over. The wrapper and the contract assert `GIT_KINDS["status"]`'s
  pins and `STATUS_PROBE`, never a literal list. A fix that adds a child, a
  read or a classification input is a re-plan trigger (FR-019, FR-020's
  `estimated`, the allow-list, FR-026's parity), and a change to the pins
  goes to lane openRepoProject-4's lead, since FR-016 and A1:230-232 list
  four by name.
- **Recorded parity gaps** (research.md R18): a failed ref listing, where
  feature 004 at `d6bac50` makes each present row on a branch
  `inspection-error` with the listing's error while the overview leaves
  every class null, as A1 does (O12 (A), a lasting difference); a working
  directory whose realpath fails (O9 (A), a lasting difference); and, if
  #24's realization merges first, a cache-only worktree (C-71). Parity
  tests leave these cases out by name.
- **Readings that differ from feature 004's code** (research.md R9): the
  extension read's row error on an exit 1 with a warning, which A1 records
  and feature 004 does not, both counting it true as PR #19's D7 does (A1
  proposal.md:1370-1375; R-332 at `211e43d`; no class differs, and no held
  item arises); the `core.worktree` read's other failures, which leave the
  root null where feature 004 refuses the run (O11); strict realpaths, an
  abandoned child the deadline cut, the deadline text and
  `tracking_freshness`. Each is the overview's own decider, tested alone.
- **Threads**: at most R + 2,561 tasks a run, R the roots given, which
  nothing caps (2,593 at 32 roots), and R + 2,689 once O4 (a) lands, each
  its own daemon thread, the stuck ones never joined (R7); a filesystem
  call stuck in the kernel can hold process exit (EC-001), which the README
  states.
- **Hostile repositories**: R19's threat model; filter drivers a
  repository's own configuration defines stay a residual (EC-022).
- The agent-context step of the plan workflow is not run: this repository's
  `CLAUDE.md` and `AGENTS.md` carry no agent-context markers (only the
  OPENSPEC-SPECKIT-GLOBAL protocol block), and `.specify/scripts` has no
  agent-context script; none is added.

### Brett Heap's words on the held items

His "yes, recommended for O1-O10" (2026-10-22T21:24:03Z), "yes, recommended
for O3, O5, O8-O11 and D5 clause 2" (2026-10-23T12:19:11Z) and "yes,
recommended for O12-O16" (2026-10-23T13:30:30Z), all in C-72, chose every
held item for change 2, each as the lane recommended it (research.md R20):

- built once A1's re-alignment lands at PR #34: O1 (A), the reflog
  remedies' submodule clause; O2 (A), `deadline-exceeded` at the reflog
  gate ("O-1: deadline-exceeded", R-263); O3, the identity re-reads in
  `probes.estimated`; O4 (a), the redirected main worktree, with its
  sub-items (c) and (d); D5's clause 2, by name; O5, PR #19 round (j)'s
  reading of the work-tree probe; O6 (A), the stale warning and the
  composer's clause 1; O7, the `main-worktree-missing` remedy's warning;
  O8 (A), feature 004's locked text with the warning; O11's part 2 (A),
  `target-not-repository-root` with the remedy "core.worktree could not be
  read; repair the repository's config, then run again"; and O13 (A), the
  `core.worktree` read in the shared git directory;
- built now: O11's part 1, A1's failure table excepting the unset key, as
  the plan's reading; O15 (A), the remedy kept whole past 200 characters;
  and O16 (a), a bare main row's null `branch`, `head` and
  `merged_into_target`;
- A1's behaviour kept as ratified: O9 (A), parity leaving out a working
  directory whose realpath fails; O10 (A), LQ-15's extension kept; O12 (A),
  a failed ref listing's null class; and O14 (A), a known limit.

Still before him:

- The base: `main` after PR #33 (recommended, C-56), or stacked on feature
  004's branch (his word needed; R2).
- His word on the tasks, then on the implementation.

## Complexity Tracking

None. The plan adds no project, dependency, flag, setting or file outside
the structure above.
