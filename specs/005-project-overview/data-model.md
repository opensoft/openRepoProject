Lane: openRepoProject-4

# Data Model: Project overview

Nothing is stored. Each `project overview` run builds its report fresh and
keeps no state beyond the invocation (FR-040); these are the values one run
reads, derives and reports. The JSON shapes and key orders are in
[contracts/project-overview.md](contracts/project-overview.md); exact human
text is A1's design D3, D4, D5 and D10 and the contract's message table.
`project:N` is feature 004's `project` at `d6bac50` ([plan.md](plan.md),
"Citations").

## Entities

### Invocation (FR-011, FR-043, FR-044)

Feature 004's `Invocation` (`project:1337-1452`), entered by `main()` for
command `overview`, with one added branch: its deadline is set when it is
made, after the arguments parse and before any root is listed, at the start
plus `TIMING["invocation_deadline"]` (60 s), with no reserve. It carries:

- `work_end`, `reserve_end`: both the deadline; `child_budget("probe")` gives
  `min(5 s, deadline - now)`, limit `deadline` when the time left is smaller
- `probes`: `probes.performed`: every Git child started, cut ones included
- `version`: the version check's memo, or the configuration-path refusal
- `signal`: the first SIGINT, SIGTERM or SIGHUP; decides 130, 143 or 129
- `phase`: `planning` throughout: the overview has no apply phase

### Root (FR-001, FR-005, FR-017; C-27, C-67)

- `path`, `path_valid_utf8`: the canonical path; the given path made absolute
  but not resolved when its canonicalisation was cut; the expanded, unresolved
  path of an absent default root
- `source`: `argument`, `environment` or `default`
- `state`: below
- `entries`: the count of entries read; null when not listed

Internal: the given string, its rank among roots (bytes of `path`), its
`(dev, ino)` for the dedupe, and its cancel flag (A1 design D2).

- `listed`: the root's task finished and read every entry
- `truncated`: the entry cap (4,096) stopped the listing, its task was cut
  (`probe-timeout`, `deadline-exceeded`), or an entry read failed partway
  (`os-error`, OPERATION `scandir`; research.md R10)
- `absent`: a default root that does not exist (`ENOENT` on the expanded path);
  no error
- `unreadable`: an argument or environment root that does not exist, is not a
  directory or cannot be opened, or a default root that exists and is not a
  directory or cannot be opened; one `root-unreadable` scan error
- `omitted`: past the 32-root cap after sorting; counted by one `scan-limit`
  error, `limit: "roots"`

### Candidate (FR-002, FR-003)

A canonical directory on which a marker holds: its raw path bytes, `kind`
(`family-holder`, `project-manifest`, `single`), `(dev, ino)`, and `rank`,
its position in canonical order after the dedupe (first spelling wins) and
before the 128-candidate cap. A candidate past the cap is counted by one
`scan-limit` error, `limit: "candidates"`, exactness `exact` when every
root listing completed, else `lower-bound`. A marker check that fails with
an error other than `ENOENT` or `ENOTDIR` (DI:142) yields an error row
instead (FR-005).

### Collector (FR-021; research.md R5)

One generator per candidate, resumed with each step's result.

- `waiting`
  - Entered when: the candidate is within the cap
  - Leaves: to `identity` when a slot is free
- `identity`
  - Entered when: its identity probe is started
  - Leaves: to `merged` on a known common directory; to `owner` on a new one;
    to `done` for no Git; to `failed` on a boundary exception
- `merged`
  - Entered when: its common directory's `(dev, ino)` is a repository already
  - Leaves: final; it adds its rank and kind to that row only
- `owner`
  - Entered when: it is the first candidate of a repository
  - Leaves: runs phase 1, then waits at the barrier, then phase 2
- `done`
  - Entered when: its row is complete
  - Leaves: final
- `failed`
  - Entered when: the boundary caught an exception
  - Leaves: final; row error `internal-error`, other evidence kept
- `not-started`
  - Entered when: the deadline came before its identity step
  - Leaves: final; a row of filesystem facts, status `error`,
    `deadline-exceeded` (OPERATION `collection`)

### Step request and step result (A1 design D1)

`GitStep(args, directory, parser, kind)`: one Git child, `git -C directory
ARGS`, of kind `probe` or `status`; `parser` one of feature 004's
incremental parsers, the keep-filter (`KeptRefParser`) or `RawOutput`.
`FsStep(fn, args)`: one filesystem task. A result carries the
`DriverOutcome` (`project:1673-1707`) or the task's value, its `OSError`,
or its cut, and the wall-clock time it completed (research.md R13).

### Child outcome to row error (FR-011, FR-012, FR-022)

- `complete`
  - Row error: none
- `complete-at-bound`
  - Row error: none
  - Note: the status probe at its record bound (EC-019)
- `failed`
  - Row error: `probe-failed`, DETAIL `exit N`, `signal N`, `cannot spawn
    (STRERROR)` or `unparseable output`
  - Note: two exceptions below
- `timeout`
  - Row error: `probe-timeout`, `OPERATION timed out after S s`
  - Note: an abandoned child its own budget cut included
- `deadline`
  - Row error: `deadline-exceeded`, `OPERATION stopped at the invocation
    deadline`
  - Note: an abandoned child the deadline cut included (research.md R9)

Exceptions (A1's collector table): the extension read's exit 1 with nothing
on either stream is `false` with no error; the work-tree probe's failure or
unusable output makes the registration disagree, with no error. And, as the
plan's reading of a conflict in ratified A1 (research.md R9; R20's O11,
part 1): the `core.worktree` read's exit 1 with nothing on either stream
is the key unset, with no error, so the root falls through to the
candidate's toplevel (`config_key_unset`, `project:2749`); any other
failure of that read keeps the table's row error and leaves `root` null.

### Filesystem task (FR-013; research.md R7)

- `running`: to `done` when its thread posts; to `cut` at `min(5 s, deadline -
  now)`
- `done`: final: its value or its `OSError` is read
- `cut`: final: `probe-timeout`, or `deadline-exceeded` where the deadline was
  the limit; its thread is abandoned and never read

### Repository (FR-006 to FR-010, FR-024, FR-025)

Keyed by the `(dev, ino)` of the no-follow `lstat` of `common_dir`.

- `identity`: `{root, common_dir, dev, ino}` and the two flags; `root` by
  FR-008 and FR-009
- `rank`: the rank of the first candidate that reached it
- `records`: the registry listing (`WorktreeListParser`)
- `extension`: `true`, `false`, or `true` with an error (research.md R9)
- `refs`: the keep-filter's records: local heads, `origin/HEAD`, the upstreams
  the heads name
- `remote_copy`: one flag per candidate name known before the listing (A1
  design D9); when the merge target comes from `origin/HEAD`, its remote
  copy is the symref's own target, listed by construction, so the flag is
  set (D9, `A1 design.md:526-528`)
- `merge_target`: `{name, source, sha}` from change 1's
  `resolve_merge_target` (`project:2517`) over `refs` and the manifest's
  `tracking_branch`, less its `notes`; or null (FR-024, FR-025)
- `merged`: the merged set at `merge_target.sha` (`MergedSetParser`), or null
- `errors`: the project row's errors, in step order
- `rows`: its worktree rows, main first

`root` is null for a bare repository, a submodule checkout, an unnamed
gitfile checkout, a gitfile checkout whose `core.worktree` read failed
other than as unset (R20's O11, parts 1 and 2, chosen), and a missing main
worktree (FR-008, FR-009).

### Worktree row (FR-006, FR-007, FR-018, FR-026)

One per registry entry, the main worktree included; a bare main entry and
an unnamed git-directory record are rows with no status probe (C-68).

- `path`, `path_valid_utf8`
  - Source: the registry record (the main worktree's realpath where the first
    record is `common_dir` and the root is named)
  - Null when: never
- `dev`, `ino`
  - Source: the row task's `lstat`
  - Null when: not present, cut, past the cap
- `admin_id`
  - Source: the two-way registration
  - Null when: the main worktree; not verified
- `present`
  - Source: the `lstat`: true, false (`ENOENT`, `ENOTDIR`), null (other error,
    cut)
  - Null when: past the cap
- `locked`, `prunable`
  - Source: the registry record
  - Null when: never
- `current`
  - Source: the working directory lies inside `path`
  - Null when: `present` null; the working directory's realpath failed
- `branch`
  - Source: the registry record; `"detached"` for a detached head
  - Null when: a bare entry
- `head`
  - Source: the registry record
  - Null when: a bare entry
- `upstream`, `upstream_oid`, `ahead`, `behind`, `remote_present`
  - Source: the kept ref records
  - Null when: none configured; `refs/heads/HEAD` (EC-033); listing failed
- `merged_into_target`
  - Source: the merged set
  - Null when: no target; listing failed
- `dirty`, `ignored_files`, `ignored_files_truncated`, `ignored_samples`
  - Source: the status probe (`StatusParser`)
  - Null when: no probe ran or it failed; past the cap
- `classification`
  - Source: [L]'s ladder through `row_evidence` and `classify`
  - Null when: past the cap; registry, ref listing or merged set failed; no
    target; but `inspection-error` set directly by FR-007

Internal: the first read (`dev`, `ino`, realpath, registration, admin id),
kept as the row's identity after re-verification (FR-007); `registered`;
the reflog gate's result; `unprobed`, set when the reflog read did not
finish (FR-033).

### The `git` object (FR-036; C-13, C-32)

For the checkout at the row's `path`, from evidence already held: `branch`,
`head`, `dirty`, `upstream`, `ahead`, `behind` and `tracking_freshness`,
the constant `local refs only; no fetch`. No probe of its own; null when
the row has no Git.

### Finding (FR-027 to FR-035, FR-041)

- `code`, `category`, `severity`, `evidence_source`: the attention table's row
  for the code (contract)
- `checkout`: `{path, path_valid_utf8, dev, ino, admin_id}` of the worktree;
  null for a repository-level finding
- `message`: the message table's text (contract), composed with a gate's remedy
  by `compose_message` (research.md R12)
- `observed_at`: the completion of the last step that decided it (research.md
  R13)
- `suggested_command`: the argument vector the attention table names, after the
  gates; else null
- `suggestion_gate`: null, or the first applicable gate code in the gate
  table's order
- `suggestion_gate_rows`: the repository's worktree-row count when the gate is
  `inspect-cap`; else null

Sources of findings, in the order a row computes them:

1. repository-level: `no-merge-target` (no candidate branch), and
   `merge-target-conflict` (manifest and `origin/HEAD` both local and
   different);
2. per worktree, the class's finding (the ladder's recommendation as its
   message), or, for `protected-default`, none of its own but FR-041's set:
   `dirty`, then at most one of `unpublished`, `remote-gone`, `diverged`,
   `unpushed`, `remote-ahead`, each with D4's message and no suggestion;
3. a disagreeing registration's `registration-mismatch` in place of the
   class's `inspection-error` finding (FR-007);
4. layouts: `unsupported-layout` (submodule, unnamed gitfile), and
   `main-worktree-missing` in place of `stale-worktree`; and paths:
   `unsupported-path-bytes`, once at repository level (null `checkout`)
   when the root or common directory is not valid UTF-8, and on every
   worktree whose path is not, which on a `merged-removable` row is the
   gate's finding in place of the housekeeping one (FR-038; A1 design D5);
5. gate findings that replace a `merged-removable` housekeeping finding
   (below).

### Gates (FR-031 to FR-035)

Row gates, for a `merged-removable` worktree, in [G]'s order; the first that
fails replaces the housekeeping finding with its own, the class unchanged:

- `main-worktree`
  - Fails when: the row is the main worktree
  - Finding: `main-worktree`, no suggestion
- `unsupported-path-bytes`
  - Fails when: its path is not valid UTF-8
  - Finding: `unsupported-path-bytes`, no suggestion
- `registration-mismatch`
  - Fails when: its registration disagrees (never reached: FR-007 makes it
    `inspection-error`)
  - Finding: `registration-mismatch`
- `locked-worktree`
  - Fails when: it is locked
  - Finding: `locked-worktree`, read-only
- reflog (FR-033)
  - Fails when: `unstarted-branch` or `reflog-unavailable`
  - Finding: `merged-removable` kept, read-only, gate code set

Repository and run gates, each withholding or limiting the suggestions of
every worktree of the repository (FR-031, FR-034):

- `target-not-repository-root`
  - Applies when: `repository.root` null for a bare repository
  - Effect: every clean suggestion withheld
- `unsupported-path-bytes`
  - Applies when: root or common directory not valid UTF-8
  - Effect: every clean suggestion withheld
- `inspection-incomplete`
  - Applies when: any row `inspection-error`, or a row left unprobed by its
    reflog read
  - Effect: `--all-safe` withheld; read-only kept
- `inspect-cap` (batch)
  - Applies when: worktree rows, every registry entry counted, over
    `batch_row_cap` (128)
  - Effect: `--all-safe` withheld
- `inspect-cap` (report)
  - Applies when: worktree rows over `report_row_cap` (256)
  - Effect: read-only suggestions limited
- `scan-limit`
  - Applies when: a row left unclassified by the 512-row cap
  - Effect: `--all-safe` withheld
- `deadline-exceeded`
  - Applies when: a row left unclassified by the deadline
  - Effect: `--all-safe` withheld
- `unstarted-branch`, `reflog-unavailable`
  - Applies when: the row's reflog decides so
  - Effect: that row's `--all-safe` withheld
- `target-cap`
  - Applies when: more `merged-removable` rows keep `--all-safe` than `targets`
    (16)
  - Effect: each keeps it, limited

A root left null by `unsupported-layout`, by `main-worktree-missing` or by a
failed `core.worktree` read carries no gate code; for the last, the gate code
`target-not-repository-root`, with a remedy row of its own, "core.worktree
could not be read; repair the repository's config, then run again", is O11's
part 2 (A), chosen, built once A1's re-alignment lands. A gate is recorded
only on a finding whose own suggestion it
changed: a `dirty` finding in an `inspection-incomplete` repository keeps its
read-only suggestion and a null `suggestion_gate` (A1 design D5). The items O1,
O2, O4 and O11's part 2 that Brett Heap's word chose (C-72; research.md R20)
each change one row of these tables once A1's re-alignment lands.

### Suggestion (FR-031)

`["project", "clean", "<root>", "--all-safe"]` or `["project", "clean",
"<root>"]`, `<root>` the absolute canonical `repository.root`. The row's
`suggested_command` is the `--all-safe` form when any finding suggests it,
else the read-only form when any does, else null.

### Error object (FR-012, FR-017, FR-022)

`{code, message, path?, path_valid_utf8?}`, plus `limit` and `omitted:
{count, exactness}` on `scan-limit` errors and on the one
`deadline-exceeded` scan error that counts the candidates not started.
Row errors sit in the project row's `errors` in step order, a worktree's
error naming the worktree in `path`; scan errors in `scan_errors` in A1
design D6's order.

### Envelope and summary (FR-036, FR-037; C-40)

The envelope's eleven fields and `summary`'s five are listed in the
contract. `completeness` is `incomplete` exactly when `scan_errors` is
non-empty or a row has status `error`; a row's status is `error` exactly
when its `errors` is non-empty. `summary` counts the whole collection,
whatever `--attention` shows.

## States of a run

- arguments: invalid: exit 2 (usage); else `config-paths`
- `config-paths`: a relative path: exit 2, `relative-config-path`; else
  `version`
- `version`: too old or unavailable: exit 2; else `notice`
- `notice`: `Scanning N roots...` when standard error is a terminal; `listing`
- `listing`: root tasks; then `collecting` (candidates start as roots finish)
- `collecting`: phase 1 and phase 2 per repository (research.md R6); deadline:
  terminate every child, stop starting; then `settling`
- `settling`: every child reaped or abandoned; then `rendering`
- `rendering`: the whole report in memory; then `writing`
- `writing`: inside the raising span; then exit 0 or 1

A signal recorded in any state stops scheduling; no report is started once
it is read, one being written stops, `Cancelled.` goes to standard error,
and the exit is 128 plus its number. An exception outside the boundary
ends the run with exit 2 (FR-039).

## Exit statuses (FR-042)

- 0: `complete` and no finding of severity `error` (and, under `--strict`, none
  of `warning`)
- 1: `incomplete`, a finding of severity `error`, or `--strict` and a finding
  of severity `warning`
- 2: an invalid invocation; a version or configuration-path refusal; an
  exception outside the boundary; a failed write to standard output
- 129, 130, 143: SIGHUP, SIGINT, SIGTERM, over any other status

## Constants

- deadline
  - Value: 60 s
  - Where: `TIMING["invocation_deadline"]`
- per-child and per-task budget
  - Value: 5 s
  - Where: `TIMING["probe_budget"]`
- grace, reap wait
  - Value: 2 s, 2 s
  - Where: `TIMING["term_grace"]`, `TIMING["reap_wait"]`
- concurrency
  - Value: 4
  - Where: `OVERVIEW["probe_concurrency"]` (new)
- roots, root entries, candidates, worktree rows
  - Value: 32, 4,096, 128, 512
  - Where: `OVERVIEW_LIMITS` (new)
- ignored entries, status records, samples
  - Value: 64, 4,096, 8
  - Where: `LIMITS` (`project:589-600`)
- batch row cap, report row cap, targets
  - Value: 128, 256, 16
  - Where: `LIMITS["worktree_rows"]`, `LIMITS["targets"]`
- reflog bound, manifest bound
  - Value: 65,536 B, 1 MiB
  - Where: `LIMITS`
- message bound
  - Value: 200 characters
  - Where: the composer (research.md R12)
