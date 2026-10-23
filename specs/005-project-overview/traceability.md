Lane: openRepoProject-4

# Traceability: requirements and scenarios to the plan

Where each functional requirement and each delta scenario of change 2 (as
A1 amends it; 64 scenarios, [spec.md](spec.md) "Appendix: Traceability")
lands in this plan: the code region of `project`, the decision of
[research.md](research.md), the section of the
[contract](contracts/project-overview.md), and the test module. Test
method names come with the tasks and are added here during the
implementation, one or more per scenario, as feature 004's
`traceability.md` records its own; every test is named
`test_overview_<scenario>`.

## Code regions and test modules

New regions of `project`, after feature 004's (research.md R3):

- `overview contracts`: `OVERVIEW`, `OVERVIEW_LIMITS`, the key tuples, the
  attention, gate, message and remedy tables;
- `overview discovery`: roots, root tasks, markers, candidates;
- `overview loop`: `OverviewLoop`, the slots, `FsTask`, the barrier;
- `overview collect`: the collectors, the repository and row steps,
  `KeptRefParser` and the R9 deciders;
- `overview findings`: findings, gates, `compose_message`, suggestions;
- `overview render`: the envelope, the human report and the writer;
- changed: `Invocation` (one branch), `run_bounded` factored into
  `start_child` and `conclude`, `parser()` and `main()` (one dispatch).

## Slices (plan.md, Summary)

Each region lands in one slice, and a requirement reaches its slice
through its region: discovery in slice 2, the loop in 3, collect in 4,
findings in 5, render in 6. `overview contracts` grows in every slice,
each table with its first user, and `FsTask`, in the loop region, lands in
slice 2, which first uses it.

- Slice 1, base, factoring and scaffolding: the changed code above, the
  subparser and the dispatch, `tests/overview_support.py` and
  `test_overview_factoring.py`; scenarios 47, 55, 56 and 64.
- Slice 2, discovery: `overview discovery` and `FsTask`; scenarios 1 to
  4, 13, 14 and 23.
- Slice 3, the loop and the scheduler: `overview loop`; scenarios 16, 18,
  19, 20, 57 and 58.
- Slice 4, repositories and rows: `overview collect`; scenarios 5 to 12,
  15, 17, 21, 22, 24 to 34, 62 and 63.
- Slice 5, findings, gates and messages: `overview findings`; scenarios 35
  to 43 and 51 to 54.
- Slice 6, output: `overview render`; scenarios 44 to 46, 48 to 50 and 59
  to 61.
- Slice 7, documentation, CI and records: `README.md`,
  `.github/workflows/tests.yml` and, if T123 lands, `AGENTS.md`; no
  scenario.

Test modules under `tests/`, with `overview_support.py`:

| Module | Covers |
| --- | --- |
| `test_overview_discovery.py` | requirement 1 |
| `test_overview_identity.py` | requirement 2 |
| `test_overview_bounds.py` | requirement 3 |
| `test_overview_isolation.py` | requirement 4 |
| `test_overview_classifier.py` | requirement 5, the parity runs |
| `test_overview_attention.py` | requirement 6 |
| `test_overview_gates.py` | requirement 7 |
| `test_overview_json.py` | requirement 8 |
| `test_overview_readonly.py` | requirement 9 |
| `test_overview_health.py` | requirement 10 |
| `test_overview_exits.py` | requirement 11 |
| `test_overview_human.py` | requirement 12 |
| `test_overview_yaml.py` | the `project-review-safety` carve-out |
| `test_overview_floor.py` | FR-050's two floor tests |
| `test_overview_units.py` | deciders, keep-filter, composer, counts |
| `test_overview_factoring.py` | condition (c); `start_child`, `conclude` |

## The 004-touching changes (research.md R3)

Lane openRepoProject-2's five conditions, each a gate on slice 1 and on
its verification ([quickstart.md](quickstart.md), "The 004-touching
changes"); lane 2 or lane openRepoProject-3 reads the diff before feature
005 merges:

- (a) feature 004's tests unedited and passing: the whole suite; no diff
  in its test files and helpers against the base.
- (b) `clean`'s output, JSON and human, byte-identical (probes, budgets,
  deadline figures and cut semantics): the side-by-side run of the base
  and the split `project`, with and without `--json`, standard output and
  standard error compared byte for byte, recorded in slice 1's pull
  request.
- (c) `clean`'s 50 s work deadline and 10 s reserve untouched:
  `test_overview_factoring.py`, and feature 004's timing tests unedited.
- (d) `overview` added only: the `--help` diffs of the top level and of
  every other subcommand, and feature 004's argument and refusal tests
  unedited.
- (e) on `main` after PR #33; a change to what PR #19's D1, D2, D9 or D14
  describe goes into feature 005's spec, never into PR #19.

## Functional requirements

- FR-001: discovery; R10; contract "Invocation".
- FR-002, FR-003: discovery; R10; data model "Candidate".
- FR-004: collect (no Git child for a candidate without `.git`).
- FR-005: discovery; R10 (PN-9); contract "Row and scan errors".
- FR-006: collect; R5; data model "Repository".
- FR-007: collect; R9, R17 (PN-18); research.md O5 (chosen), O11 (chosen:
  part 1 built now, part 2 with A1's re-alignment).
- FR-008, FR-009: collect, findings; R5, R9; contract "Other findings",
  "Git children"; research.md O4 (a), O7 and O13 (chosen), O11 (chosen:
  part 1 built now, part 2 with A1's re-alignment).
- FR-010: collect; data model "Repository".
- FR-011, FR-012: loop; R4, R9; data model "Child outcome to row error".
- FR-013: loop; R7 (PN-10).
- FR-014: collect (manifest task); R7.
- FR-015: collect; R8 (PN-16).
- FR-016: runner reuse; R3; contract "Git children".
- FR-017, FR-018: discovery, loop; R6; data model "Root", "Worktree row".
- FR-019: loop; R6; the concurrency-1 and concurrency-4 runs.
- FR-020: render; R14 (PN-12); research.md O3 and O4 (chosen).
- FR-021, FR-022: collect; R5; contract "Row and scan errors".
- FR-023: collect (manifest reader); `test_overview_yaml.py`.
- FR-024, FR-025: collect (change 1's `resolve_merge_target`, reused,
  over the kept records); R3; data model "Repository"; contract "Other
  findings".
- FR-026: collect (`row_evidence`, `classify`); R3, R18; research.md O9
  and O12 (chosen).
- FR-027: contract "The attention table".
- FR-028: findings; R12 (PN-1); contract "Findings from the ladder";
  research.md O6 and O8 (chosen).
- FR-029, FR-030: render; data model "Exit statuses"; contract "Human
  report".
- FR-031 to FR-035: findings; R12; data model "Gates"; contract
  "Remedies", "Composer"; research.md O1, O2, O4, O6 and O15 (chosen; D5's
  clause 2 chosen by name).
- FR-036 to FR-038: render; R11, R15 (PN-6, PN-8); contract "JSON".
- FR-039: render, dispatcher; R15 (PN-2); contract "Exit-2 outputs".
- FR-040: R3 (the ban), R18 (the wrapper's allow-list), R19.
- FR-041: findings; contract "Default-branch findings".
- FR-042 to FR-044: dispatcher, loop, render; R4, R15; data model "States
  of a run"; research.md O10 (chosen).
- FR-045, FR-046: render; R16 (PN-3, PN-5); contract "Human report",
  "Fixed lines".
- FR-047: R3 (one subcommand; no new limit, variable, file or dependency).
- FR-048: the README section (plan.md, Project Structure).
- FR-049: R18; this file.
- FR-050: `.github/workflows/tests.yml`, one `-k test_overview_floor_`;
  R18.
- FR-051: `AGENTS.md`, one sentence, only if feature 004's T123 lands;
  research.md R20.

## Delta scenarios

Requirement 1, discovery (R10, R11): 1 Independent clones and aliases; 2
Unreadable candidate directory; 3 Family holder count, relationships and
probe ownership; 4 Every root is absent.

Requirement 2, identity (R5, R9, R17; O11 for 9): 5 One probe set per
repository; 6 Present eligible external worktree; 7 Missing external worktree;
8 Unreadable external worktree; 9 A separate git directory; 10 A submodule
checkout under a root; 11 A deleted main worktree; 12 A bare repository with a
linked worktree.

Requirement 3, bounds (R4, R6, R7, R8, R14): 13 Candidate cap after
sorting, with an exact count; 14 Candidate cap with an incomplete listing;
15 Root and worktree-row caps; 16 Probe timeout; 17 Hung filesystem call on
an external worktree; 18 Invocation deadline; 19 Bounded concurrency; 20
The JSON does not depend on concurrency; 21 Bounded ignored files; 22 User
status configuration; 23 A root on a hung mount; 24 A repository root on a
hung mount; 25 A manifest over the size bound.

Requirement 4, isolation (R5): 26 One helper failure is isolated; 27 The
YAML library is not installed.

Requirement 5, classifier (R3, R18): 28 Manifest target; 29 origin/HEAD
target; 30 main target; 31 master target; 32 Conflicting targets; 33
Missing target; 34 Every protected classifier.

Requirement 6, attention (R12): 35 Attention filter per category; 36 A
merged worktree whose upstream was deleted.

Requirement 7, suggestions (R12; chosen O1, O2, O4, O6): 37 Gated merged
worktrees; 38 Canonical identity through the handoff; 39 More eligible
worktrees than the batch's target limit; 40 The two inspect-cap bands; 41
A row left unprobed closes the repository gate; 42 An unstarted branch; 43
A branch whose reflog cannot decide.

Requirement 8, JSON (R11, R15): 44 Control and format characters in paths;
45 Non-UTF-8 path; 46 Non-UTF-8 common directory; 47 An argument error
under --json; 48 Every envelope field is present; 49 An internal error
outside the collector under --json.

Requirement 9, read-only (R3, R18, R19): 50 Local and read-only.

Requirement 10, default branch: 51 A default branch pushed without an
upstream; 52 A repository with no remote; 53 A dirty default branch ahead
of its upstream; 54 A failed status probe on the default branch.

Requirement 11, exits (R4, R15; chosen O10): 55 Git too old; 56 Git
unavailable; 57 SIGTERM or SIGHUP during collection; 58 SIGINT during
collection; 64 A relative configuration path (A1's).

Requirement 12, human report (R16): 59 Nothing needs attention; 60 A gated
suggestion; 61 The scanning notice.

`project-review-safety`: 62 Manifest is not valid UTF-8 text (the kept
canonical scenario, with the existing
`test_invalid_yaml_encoding_is_a_structured_error`); 63 Overview keeps a
manifest with invalid text in its row.

## Requirements no scenario exercises (FR-049)

Each gets a test of its own, named here when written: FR-004's candidates that
are not family holders; FR-007's twins (EC-031), its identity re-read before a
status probe, its extension read, effective-work-tree probe and `commondir`
check, and a wrapper log with no `rev-parse` child in a linked worktree where
the extension reads false; FR-010; FR-020's `estimated`; FR-021's `refused` and
`undecodable-output`; FR-022's 200-character bound, with the composer's length
tables (R12; R20's "Lengths"); O11 part 2's `core.worktree` read that prints
and exits 1 (R18); FR-033's reflogs of 65,535 and 65,536 bytes; FR-037's
orders, ties by rank (PN-8) and the repository-level finding first; FR-039's
`refused` and `os-error`; EC-033's branch named `HEAD` (PN-17); the empty
`--root` (PN-13); a root listing that fails partway (PN-9); and the overview's
own readings of R9.

## Success criteria

- SC-001, SC-008: `test_overview_isolation.py`, `test_overview_identity.py`.
- SC-002: the wrapper's assertions and the snapshot, in every module.
- SC-003: `test_overview_classifier.py` (parity runs, `local.env`); the
  parity tests name the cases left out as lasting differences, a working
  directory whose realpath fails (O9 (A)) and a failed ref listing (O12
  (A)), and, if #24's realization merges first, a cache-only worktree
  (C-71).
- SC-004: `test_overview_gates.py` (argument vectors only).
- SC-005, SC-006: `test_overview_bounds.py`; the hand timing in
  [quickstart.md](quickstart.md).
- SC-007: `test_overview_bounds.py`, concurrency 1 and 4.
- SC-009, SC-011: `test_overview_json.py`, `test_overview_exits.py`.
- SC-010: `test_overview_human.py`, character for character.
- SC-012: every scenario above; this file.
- SC-013: the README review in the implementation's final task.
- SC-014: `test_overview_yaml.py` and the existing test.
