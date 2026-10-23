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
`DriverOutcome` (`project:1673-1707`) or the task's value, its `OSError` or
`EvidenceError` (`project:2615`, from a row task's registration reads, taken
as the row's error; research.md R5), or its cut, and the wall-clock time it
completed (research.md R13).

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
part 1; a departure from DI:535): the `core.worktree` read's exit 1 with
nothing on either stream is the key unset, with no error, so the root falls
through to the
candidate's toplevel (`config_key_unset`, `project:2749`); any other
failure of that read keeps the table's row error and leaves `root` null.

### Filesystem task (FR-013; research.md R7)

- `running`: to `done` when its thread posts; to `cut` at `min(5 s, deadline -
  now)`
- `done`: final: its value, or its `OSError` or `EvidenceError`, is read
- `cut`: final: `probe-timeout`, or `deadline-exceeded` where the deadline was
  the limit; its thread is abandoned and never read

### Repository (FR-006 to FR-010, FR-024, FR-025)

Keyed by the `(dev, ino)` of the no-follow `lstat` of `common_dir`.

- `identity`: `{root, common_dir, dev, ino}` and the two flags; `root` by
  FR-008 and FR-009. The main worktree itself is a candidate when a
  candidate is a spelling of the first registry record's directory (the
  same `(dev, ino)`; A1 design.md:455-458), and the root is then that
  candidate's identity toplevel (A1:139-141)
- `rank`: the rank of the first candidate that reached it
- `records`: the registry listing (`WorktreeListParser`)
- `extension`: `true`, `false`, or `true` with an error (research.md R9)
- `refs`: the keep-filter's records: local heads, `origin/HEAD`, the upstreams
  the heads name; kept as the list for `resolve_merge_target` and passed to
  `row_evidence` as `{refname: record}`, as `project:3510` builds it
- `remote_copy`: one flag per candidate name known before the listing (A1
  design D9); when the merge target comes from `origin/HEAD`, its remote
  copy is the symref's own target, listed by construction, so the flag is
  set (D9, `A1 design.md:526-528`)
- `merge_target`: `{name, source, sha}` from change 1's
  `resolve_merge_target` (`project:2517`) over `refs` and the manifest's
  `tracking_branch`, less its `notes`; or null (FR-024, FR-025); `name`
  written through `json_path` (JSON) or `human_path` (human), never as the
  resolver's str is (research.md R15)
- `merged`: the merged set at `merge_target.sha` (`MergedSetParser`), or null
- `errors`: the project row's errors, in step order
- `rows`: its worktree rows, main first

`root` is null for a bare repository, a submodule checkout, an unnamed
gitfile checkout, a gitfile checkout whose `core.worktree` read failed
other than as unset (R20's O11, parts 1 and 2, chosen), a gitfile checkout
whose read `core.worktree` value has no strict realpath (`os-error`,
OPERATION `realpath`, or the task's cut; research.md R9), a first registry
record whose `lstat` or realpath fails other than with `ENOENT` or
`ENOTDIR`, or is cut, where the first candidate is a linked worktree
(`main_worktree_decision`'s `unreadable`, `project:2880-2881`: the row's own
error records it, with no suggestion and no gate code), and a missing main
worktree (FR-008, FR-009); and, once A1's re-alignment lands, for a main
worktree that O4 (a)'s detector finds redirected (R20's O4 (a), chosen;
"Gates", below).

### Worktree row (FR-006, FR-007, FR-018, FR-026)

One per registry entry, the main worktree included; a bare main entry, an
unnamed git-directory record and a submodule checkout's main row are rows
with no status probe (C-68; A1 design D3, items 1 to 3), each taking only
its `lstat` task: no registration read, no twin decision and no
`row_evidence`, its status fields and `classification` null (research.md
R5). Each field's "Null when" keeps every case of the packet's column
(DI:770-790), as C-40 asks, and adds the overview's own: the cap, a cut,
the working directory's realpath, and O16 (a)'s bare row.

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
  - Source: the registry record; `"detached"` for a detached head; written
    through `json_path` or `human_path`, from the record's bytes or
    `row_evidence`'s surrogateescape str alike (research.md R15)
  - Null when: a bare entry (O16 (a), chosen, built now: C-68 and FR-008,
    departing from C-40's packet rule that `branch` is never null)
- `head`
  - Source: the registry record
  - Null when: a bare entry (O16 (a))
- `upstream`
  - Source: the kept ref records; escaped as `branch` is
  - Null when: none configured; `refs/heads/HEAD` (EC-033); listing failed
- `upstream_oid`, `ahead`, `behind`
  - Source: the kept ref records
  - Null when: none configured; the upstream ref is gone; `refs/heads/HEAD`;
    listing failed
- `remote_present`
  - Source: the kept ref records
  - Null when: none configured; `refs/heads/HEAD`; listing failed
- `merged_into_target`
  - Source: the merged set
  - Null when: a detached head; a missing path; no target; the ref listing
    or the merged set failed; a bare entry (O16 (a))
- `dirty`, `ignored_files_truncated`
  - Source: the status probe (`StatusParser`)
  - Null when: no probe ran or it failed; past the cap
- `ignored_files`
  - Source: the status probe
  - Null when: as for `dirty`, or the stream stopped before any ignored
    record (US6 s11: `dirty: true` with `ignored_files` null at 4,097
    untracked files)
- `ignored_samples`
  - Source: the status probe
  - Null when: as for `dirty`; `[]`, never null, when the probe ran and
    found none
- `classification`
  - Source: [L]'s ladder through `row_evidence` and `classify`
  - Null when: past the cap; registry, ref listing or merged set failed; no
    target; but `inspection-error` set directly by FR-007, and by FR-026 for
    a row the ladder would make `merged-removable` or `merged-current` when
    the working directory's realpath failed, with no row error (research.md
    R5)

Internal: the first read (`dev`, `ino`, realpath, registration, admin id),
kept as the row's identity after re-verification (FR-007); `registered`;
the reflog gate's result; `unprobed`, set when the reflog read did not
finish (FR-033).

### The `git` object (FR-036; C-13, C-32)

For the checkout at the row's `path`, from evidence already held: `branch`,
`head`, `dirty`, `upstream`, `ahead`, `behind` and `tracking_freshness`,
the constant `local refs only; no fetch`. No probe of its own. `git` is
null exactly when `worktrees` is null (a candidate without `.git`, FR-004;
a family holder with no Git toplevel, FR-003; an error row whose
collection ended before the registry, FR-005, A1:407); otherwise it is an
object whose fields are null where the checkout at `path` established
nothing (no registry row for `path`, a failed or cut probe), with the null
rules of that worktree row's fields, and whose `tracking_freshness` is
never null (C-13, C-32).

### Project row (FR-036; C-40; DI:743-758)

- `name`: string, the manifest's `name`, else the directory name
- `path`, `path_valid_utf8`: string and boolean, never null; `path` is
  `repository.root` for a Git row (the candidate when `root` is null), the
  holder for a family holder, else the candidate; the flag speaks for that
  path alone (A1 design.md:606-618), not by the packet's any-of rule
- `kind`: `single`, `project-manifest` or `family-holder`; null when the
  marker checks failed
- `repository`: object or null; `root` null for a bare main entry, a
  submodule checkout, an unnamed gitfile checkout, a missing main worktree
  and the other cases under "Repository" above
- `merge_target`: object or null ("Repository")
- `git`: object or null (above)
- `worktrees`: array or null, main first, then by path bytes
- `findings`: array, never null
- `suggested_command`: argument vector or null ("Suggestion")
- `status`: `error` exactly when `errors` is non-empty, else `ok`
- `errors`: array, never null, in step order

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

Repository, run and row gates, in FR-035's order after the row gates above,
each withholding or limiting the suggestions it names (FR-031, FR-034):

- `target-not-repository-root`
  - Applies when: `repository.root` null for a bare repository; CHOSEN, once
    A1's re-alignment lands: a redirected main worktree (O4 (a), with its
    sub-items (c) and (d); below), and a gitfile checkout whose
    `core.worktree` read failed other than as unset (O11, part 2 (A))
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
  - Applies when: a row left unclassified by the deadline; CHOSEN (O2 (A)),
    once A1's re-alignment lands, also a row whose reflog read the deadline
    cut, in place of `inspection-incomplete`
  - Effect: `--all-safe` withheld
- `unstarted-branch`, `reflog-unavailable`
  - Applies when: the row's reflog decides so
  - Effect: that row's `--all-safe` withheld
- `target-cap`
  - Applies when: more `merged-removable` rows keep `--all-safe` than `targets`
    (16)
  - Effect: each keeps it, limited

A root left null by `unsupported-layout` or by `main-worktree-missing`
carries no gate code. A root left null by a failed `core.worktree` read
(O11, chosen) carries none until A1's re-alignment lands; then every clean
suggestion is withheld with `target-not-repository-root` and the remedy of
its own row, `remedy.target-not-repository-root`'s "core.worktree could not
be read; repair the repository's config, then run again" (79 characters),
in place of the bare row's. A gate is recorded only on a finding whose own
suggestion it
changed: a `dirty` finding in an `inspection-incomplete` repository keeps its
read-only suggestion and a null `suggestion_gate` (A1 design D5). A
worktree path that is not valid UTF-8 changes no suggestion but its own
`merged-removable` row's, the row gate replacing that finding; every other
finding of that worktree keeps its table suggestion and a null
`suggestion_gate`, since the command names only the root (A1:776-779; A1
design.md:289-293, :617-618). The items O1, O2, O4 and O11's part 2 that
Brett Heap's word chose (C-72; research.md R20) each change one row of
these tables once A1's re-alignment lands.

O4 (a), CHOSEN, once A1's re-alignment lands (research.md R20): where the
main worktree's toplevel, from its own candidate's identity probe or else
from one `main-toplevel` child, is not the first registry record's canonical
path (the ordinary layout), where the directory `core.worktree` names holds
no `.git` file naming `common_dir` itself (the gitfile layout), where a bare
entry's path joined with `/.git` is `common_dir` (sub-item (c)), or where
that probe or child exits nonzero (sub-item (d)), `repository.root` is null,
every clean suggestion is withheld with `target-not-repository-root` and
the redirect remedy, and the main worktree row keeps the record's path,
`present` from `lstat`, null status fields and classification, and takes no
status probe. A nonzero `main-toplevel` exit records `probe-failed`
(A1:369; no exception lists it) and counts as a redirect; a cut one decides
nothing. `probes.estimated` takes 1 per repository in the ordinary layout
whose present main worktree is no Git candidate (research.md R14).

### Suggestion (FR-031)

`["project", "clean", "<root>", "--all-safe"]` or `["project", "clean",
"<root>"]`, `<root>` the absolute canonical `repository.root`. The row's
`suggested_command` is the `--all-safe` form when any finding suggests it,
else the read-only form when any does, else null.

### Error object (FR-012, FR-017, FR-022)

`{code, message, path?, path_valid_utf8?}`, plus `limit` and `omitted:
{count, exactness}` on `scan-limit` errors and on the one
`deadline-exceeded` scan error that counts the candidates not started;
`exactness` is `exact`, `lower-bound` or `unknown`, `count` null under
`unknown`, as for the entry cap (A1:253-257).
Row errors sit in the project row's `errors` in step order, a worktree's
error naming the worktree in `path`; scan errors in `scan_errors` in A1
design D6's order.

### Envelope and summary (FR-036, FR-037; C-40)

The envelope's eleven fields and `summary`'s five are listed in the
contract; `relationships` is `[]` (FR-003). `completeness` is `incomplete`
exactly when `scan_errors` is non-empty or a row has status `error`; a
row's status is `error` exactly
when its `errors` is non-empty. `summary` counts the whole collection,
whatever `--attention` shows.

## States of a run

- arguments: invalid: exit 2 (usage); else `config-paths`
- `config-paths`: a relative path: exit 2, `relative-config-path`; else
  `version`
- `version`: too old or unavailable: exit 2; else `notice`
- `notice`: `Scanning N roots...` when standard error is a terminal; `listing`
- `listing`: every root task, run at once; once each has finished or been
  cut, a cut root keeping the snapshot of the entries it had read
  (research.md R7), the candidates are sorted, deduplicated (the first
  spelling wins), capped at 128 and ranked; then `collecting`
- `collecting`: phase 1 and phase 2 per repository (research.md R6); deadline:
  terminate every running child, a terminating one keeping its outcome, stop
  starting, answer every pending request with a `deadline` result (each
  collector stopping at its first, one `deadline-exceeded` error on its row)
  and make the not-started candidates their rows; then `settling` once no
  child runs or terminates, no task wait is pending and every collector has
  ended (research.md R4)
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
