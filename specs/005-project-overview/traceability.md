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

`overview_support.py`: fixtures, isolation, snapshot, audit hook, the probe
shim, the seam helpers (`OVERVIEW_FS`), the pty runner
(`run_with_stderr_tty`) and the tests' own transcription of the contract
(research.md R18). `tests/compare_clean_base.py`, not collected, is gate
(b)'s script (quickstart.md).

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
- FR-006: collect; R5; data model "Repository"; research.md O4 (a) and
  O13 (chosen; D5's clause 2 chosen by name).
- FR-007: collect; R9, R17 (PN-18); research.md O5 (chosen), O11 (chosen:
  part 1 built now as the plan's reading of a conflict in ratified A1, a
  text re-alignment on a lane finding; part 2 with A1's re-alignment).
- FR-008, FR-009: collect, findings; R5, R9; contract "Other findings",
  "Git children"; data model "Worktree row" (O16 (a), chosen, built now,
  ahead of A1's text); research.md O4 (a), O7, O13 and O14 (chosen), O11
  (chosen: part 1 built now as the plan's reading, part 2 with A1's
  re-alignment).
- FR-010: collect; data model "Repository".
- FR-011, FR-012: loop; R4, R9; data model "Child outcome to row error".
- FR-013: loop; R7 (PN-10).
- FR-014: collect (manifest task); R7.
- FR-015: collect; R8 (PN-16).
- FR-016: runner reuse; R3; contract "Git children"; research.md O20
  (chosen, built now, ahead of A1's text).
- FR-017, FR-018: discovery, loop; R6; data model "Root", "Worktree row".
- FR-019: loop; R6; the concurrency-1 and concurrency-4 runs.
- FR-020: render; R14 (PN-12); research.md O3 and O4 (chosen).
- FR-021, FR-022: collect; R5; contract "Row and scan errors".
- FR-023: collect (manifest reader); `test_overview_yaml.py`.
- FR-024, FR-025: collect (change 1's `resolve_merge_target`, reused,
  over the kept records); R3; data model "Repository"; contract "Other
  findings".
- FR-026: collect (`row_evidence`, `classify`); R3, R18; research.md O9,
  O12 and O21 (chosen).
- FR-027: contract "The attention table".
- FR-028: findings; R12 (PN-1); contract "Findings from the ladder";
  research.md O6, O8 and O18 (chosen).
- FR-029, FR-030: render; data model "Exit statuses"; contract "Human
  report".
- FR-031 to FR-035: findings; R12; data model "Gates"; contract
  "Remedies", "Composer"; research.md O1, O2, O4, O6, O7, O11, O15, O17 and
  O19 (chosen, O15 and O19 built now, ahead of A1's text; D5's clause 2
  chosen by name).
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
`undecodable-output`; FR-022's 200-character bound (a unit test over the error
table with the longest STRERROR the platform gives, asserting at most 200) and
the composer's length tables (R12; R20's "Lengths"); O11 part 2's
`core.worktree` read that prints and exits 1 (R18); FR-033's reflogs of 65,535
and 65,536 bytes; FR-037's orders, ties by rank (PN-8) and the
repository-level finding first; FR-039's `refused` and `os-error`; EC-033's
branch named `HEAD` (PN-17); the empty `--root` (PN-13); a root listing that
fails partway (PN-9); the overview's own readings of R9; FR-049's
device-and-inode dedupe of roots and candidates and the canonically first
spelling, through an injected file-status call (`test_overview_discovery.py`);
FR-001's cut canonicalisation (C-67; US6 s6's second clause: the root's
`path` the given path made absolute and unresolved, sorted among canonical
paths, never deduplicated, counted toward the 32 roots; scenario 23's second
arm); scenario 13's two listing orders (US6 s1); scenario 24's hold of each
Git child in the hung checkout (R18's shim); and these, each named as
proposed (the plan's rule is `test_overview_<subject>`):

- FR-032's residual:
  `test_overview_the_two_residual_gates_keep_the_all_safe_suggestion`
  (gates): a `merged-removable`
  worktree with an operation-in-progress marker, one with a commit only on
  its worktree, one with a submodule and one with hidden local state each
  keep `--all-safe` with no gate; the wrapper log holds no `rev-list`, and
  the armed hook's list no `open` of a `logs/HEAD` and no `os.scandir` or
  `os.listdir` of an administrative directory (R18).
- FR-044, C-69 and EC-035, a signal while the report is written:
  `test_overview_a_signal_while_the_report_is_written` (exits): standard
  output a pipe nobody reads (shrunk with `fcntl.F_SETPIPE_SZ` on Linux,
  else a document over 64 KiB), SIGTERM once the run has outlived its last
  child by 1 s: status 143, `Cancelled.`, and standard output a strict
  prefix of the full document.
- FR-044, a signal recorded while rendering:
  `test_overview_a_signal_recorded_while_rendering_prints_nothing` (exits):
  `render_report()` delivers SIGTERM in-process: empty standard output,
  status 143.
- FR-039's failed write: `test_overview_a_failed_write_to_standard_output`
  (exits): descriptor 1 closed in the child, as feature 004's
  `test_clean_the_plain_report_in_json_with_standard_output_closed` closes
  it (`tests/test_clean_guard.py:373-397`): exit 2, no traceback, standard
  output empty, `line.write-failed` on standard error (R15).
- FR-026, the working directory's realpath failing:
  `test_overview_the_working_directory_s_realpath_fails` (classifier): the
  seam's `realpath` raising for the working directory, `PWD` absolute: the
  first scan error `os-error`, OPERATION `realpath`, `path` the `PWD`
  value; every `current` null; a clean, merged, published row
  `inspection-error` with no row error and gate `inspection-incomplete`;
  the other rows classified as usual (R5; O9 (A)).
- FR-043, a relative `GIT_CONFIG_GLOBAL` or `GIT_CONFIG_SYSTEM`:
  `test_overview_a_relative_configuration_path_each_variable` (exits),
  feature 004's cases copied (`tests/test_clean_resolution.py:1177-1248`):
  the wrapper log empty, `git --version` included (O10 (A)).
- FR-012's half-way rows: part of scenario 18's test: one repository with
  two rows, the first row's status probe held past the deadline; the second
  keeps the registry, extension, refs and merged evidence and gets
  `deadline-exceeded` (R4).
- FR-025's cut manifest read:
  `test_overview_a_cut_manifest_read_gives_no_merge_target` (isolation): a
  slow seam `read` for one manifest: `probe-timeout`, `merge_target` null,
  no `no-merge-target` finding, no fallback to `origin/HEAD`, `main` or
  `master`, and no ladder.
- US1 s8: `test_overview_a_root_that_is_itself_a_project` (discovery):
  `--root` naming one project's own directory gives that candidate its row.
- US2 s4: `test_overview_row_and_scan_errors_under_attention` (attention):
  a row error and a scan error under `--attention`, both shown under
  `repair`, neither counted as a finding.
- Scenario 44's "pasted into bash under a UTF-8 locale": part of its test,
  human form, on Linux: the printed `next` words run through `bash -c`
  under `LC_ALL=C.UTF-8` and the root compared; skipped with the reason
  where bash is older than 4.2 or the locale is missing.

## Held items, chosen: their tests

The first build asserts A1 as ratified; the commit that A1's re-alignment
lands with flips, in one commit, the assertions named here (C-72; plan.md,
Summary). Per item: its behaviour test (module), its fixture or seam, and
what flips.

- O1 (A): scenarios 42's and 43's tests (gates), the five reflog fixtures;
  flips: the message and the human `next` end "...yourself" to
  "...yourself (--force if it holds a submodule)", and the composer's rows,
  `unstarted-branch` cut to 59 of 67 and `reflog-unavailable` exactly 200.
- O2 (A):
  `test_overview_a_reflog_read_cut_by_the_deadline_is_deadline_exceeded`
  (units): the decider with the cut's limit as input; flips: the gate
  `inspection-incomplete` to `deadline-exceeded` with `re-run with --root
  <repository parent>`, a budget cut staying `inspection-incomplete`.
- O3: `test_overview_the_identity_re_read_is_counted_in_estimated` (units),
  a line-feed directory (scenario 44's) and a submodule checkout (scenario
  10's); flips: `estimated` gains +3 per such candidate, so that it equals
  `performed` in an uncut run but for R14's listed divergences.
- O4 (a) with (c) and (d):
  `test_overview_a_redirected_main_worktree_gets_no_clean_suggestion`
  (gates): a main worktree its own `core.worktree` redirects, in both
  layouts (R20's two tests), a bare entry whose path plus `/.git` is the
  common directory, and a main-worktree probe that exits nonzero (the
  shim's fail action); flips: the ratified suggestion to `suggested_command`
  null with `target-not-repository-root` and the redirect remedy (152
  characters), and `estimated` +1 per repository in the ordinary layout
  whose present main worktree is no candidate.
- D5's clause 2: the composer's stale-and-redirect row (units); flips: D5's
  rule alone to the recommendation left out and the remedy cut to 200.
- O5:
  `test_overview_a_linked_worktree_path_holding_a_line_feed_under_the_extension`
  (identity) and a unit of `work_tree_output()`; flips: output not exactly
  one line disagreeing to
  the output less its final line feed read as one path.
- O6 and O7: scenarios 7's and 11's tests and
  `test_overview_the_stale_warning_while_a_sibling_row_is_unreadable`
  (attention), a sibling row with `present: null` (`chmod 000` on its
  parent under `not_root`, and its injected `PermissionError` twin); flips:
  the plain stale text to T6 (160 characters), the `main-worktree-missing`
  remedy to 152 characters, and the composer's clause 1 rows.
- O8 (A): `test_overview_a_locked_stale_row` (attention), a locked worktree
  whose directory was deleted, once beside an unreadable sibling; flips:
  the one stale text to "Review, unlock it, then prune stale worktree
  metadata manually." (173 characters with the warning).
- O9 (A) and O10 (A): the FR-026 and FR-043 tests above; nothing flips.
- O11 part 1, built now: scenario 9's test and a unit of
  `core_worktree_value()` (`git init --separate-git-dir`, the key unset);
  nothing flips.
- O11 part 2 (A): `test_overview_a_core_worktree_read_that_fails_otherwise`
  (identity), the shim's fail action (a line on standard error, exit 1) and
  a second case cut by a hold; flips: no gate code to
  `target-not-repository-root` with the 79-character remedy, the row error
  `probe-failed`, `repository.root` null and no `unsupported-layout`
  finding staying.
- O12 (A), built now: the parity tests name a failed ref listing, and a
  unit asserts every class null after it; nothing flips.
- O13 (A):
  `test_overview_the_core_worktree_read_runs_in_the_common_directory`
  (identity): a `git init --separate-git-dir` repository with
  `extensions.worktreeConfig` true reached through a linked candidate whose
  own `config.worktree` sets `core.worktree`; flips: the wrapper log's
  `config --get core.worktree` from `-C` the candidate to `-C` the common
  directory, and the suggestion `project clean` refuses to the one it reads.
- O14 (A), built now: a test named after the limit (a linked worktree of a
  submodule's module directory as the only candidate) asserts the built
  behaviour, so that a later detection would flip it (R9).
- O15 (A), built now, ahead of A1's text: the composer's rows at an escaped
  parent of 176, 177, 255 and 4,096 characters and one of 30 escaped control
  characters (units; R18); nothing flips.
- O16 (a), built now, ahead of A1's text: scenario 12's test, "A bare
  repository with a linked worktree", asserts the bare row's `branch`, `head`
  and `merged_into_target` null; nothing flips.
- O17 (A): scenarios 42's and 43's tests (gates), the five reflog fixtures;
  flips: A1's remedies, 102 and 97 characters, to #19's Q5 next steps kept
  whole, 248 and 243, in place of O1 (A)'s texts above, the message `...; `
  and the remedy, 253 and 248, and the composer's rows.
- O18 (A): scenario 7's test and `test_overview_a_locked_stale_row`
  (attention), a stale row with no unread sibling, plain and locked; flips:
  A1's one 50-character text to [L]'s 305- and 318-character forms, kept
  whole, and the composer's rows beside each remedy that can follow them, up
  to 459 and 472; the forms under O6's test do not flip.
- O19 (A), built now, ahead of A1's text:
  `test_overview_the_wider_registration_mismatch` (gates) and a unit of its
  decider, fixtures for #19's two cases (R18); its expected result is stated
  at feature 004's next head (C-72); nothing flips.
- O20 (A), built now, ahead of A1's text: the wrapper's assertion of
  `GIT_KINDS["status"]`'s pins by reference on every status probe (R18);
  nothing flips.
- O21 (A), built now: a unit asserts every class null after a failed
  merged-set listing, its ref listing read; the case is checked against
  feature 004's next head (C-72); nothing flips.

## Success criteria

- SC-001, SC-008: `test_overview_isolation.py`, `test_overview_identity.py`.
- SC-002: the wrapper's assertions and the snapshot, in every module.
- SC-003: `test_overview_classifier.py` (parity runs, `local.env`); the
  parity tests name the cases left out as lasting differences, a working
  directory whose realpath fails (O9 (A)) and a failed ref listing (O12
  (A)), and, if #24's realization merges first, a cache-only worktree
  (C-71); a failed merged-set listing's rows stand apart too, A1's null class
  staying (O21 (A); research.md R20).
- SC-004: `test_overview_gates.py`: the argument vectors, and in every gate
  fixture a helper, `assert_preview_agrees(root, document)`, that runs the
  preview each ungated `--all-safe` suggestion names and asserts every such
  worktree selected or excluded only as SC-004 lists (scenarios 34 and 37).
- SC-005, SC-006: `test_overview_bounds.py`; the hand timing in
  [quickstart.md](quickstart.md).
- SC-007: `test_overview_bounds.py`, concurrency 1 and 4.
- SC-009, SC-011: `test_overview_json.py`, `test_overview_exits.py`.
- SC-010: `test_overview_human.py`, character for character.
- SC-012: every scenario above; this file.
- SC-013: the README review in the implementation's final task.
- SC-014: `test_overview_yaml.py` and the existing test.
