Lane: openRepoProject-2

# Proposal: add-project-overview

Status: draft, revised after the alignment review, the lead's later rulings,
the council and the packet author's final delta read (resolutions on PR #12
and in "Questions Resolved by the Alignment Review"; noted constraints in
`clarifications.md`), awaiting Brett Heap's ratification; nothing here is
ratified. Like `add-project-clean-all-safe`, it adds "Decisions Taken by This
Proposal", "Corrections to the Packet" and "Open Questions" to the house
sections.

Governing issue: opensoft/openRepoProject#10, claimed by lane
openRepoProject-2 (comment 6069504479); refs #6, the design packet's record.
Its sibling, opensoft/openRepoProject#9, governs `add-project-clean-all-safe`,
the change this one depends on (see "Dependencies and Sequencing", Impact).

Input: the project maintenance design packet under `ideation/brainstorm/`,
merged by PR #7 as `da33d92`. The packet is non-normative (OV:16-19); this
proposal adopts or rejects its contracts one by one. Its baseline holds:
`git diff a040790 da33d92 -- project tests/` is empty. Citations: `DI:98` is
line 98 of `project-maintenance-project-discovery.md` at `da33d92`; OV, BA,
SY and HO are the packet overview, batch cleanup, synthesis and fix-handoff
documents beside it; PRS is `openspec/specs/project-review-safety/spec.md`;
`project:421` is the executable at `da33d92` (Dependencies).

## Why

`project status`, `doctor` and `clean` each inspect one selected project.
Nothing answers the packet's question, "Which of my local projects needs
attention?", across the configured roots (DI:16-18). The packet's session kept
losing track of which work remained and why it could not yet be retired
(OV:21-25): one command per project, and doctor correlated with clean by hand,
the gap PR #2's doctor repository health (`acf0133`) tried to close in doctor.

Now, because the packet has merged (PR #7), issue #6's "Done when" still waits
on "a later OpenSpec proposal picks the packet up as input", and the PR #2
decision record assigns that doctor work to this design as "local-only,
read-only reporting" (OV:180-183). The overview comes behind change 1, which
builds the shared evidence model the overview reads across many repositories.

## What Changes

- **A new read-only subcommand, `project overview [--root D]... [--attention]
  [--json] [--strict]`** (DI:58-75; OV:356). It lists every local project it
  discovers with its local Git health, its linked worktrees, findings grouped
  by attention category and at most one next command per row.
- **Discovery is bounded and local.** Roots come from repeatable `--root`,
  else `PROJECTS_DIR`, else the `projects_dirs()` defaults; only each root and
  its immediate entries are examined, by the packet's marker table
  (DI:98-151). The overview never calls `discover` or `snapshot` (DI:39-47).
- **Rows are repositories, not names.** Each Git row carries the identity
  `{root, common_dir, dev, ino}`; every registered worktree, external ones
  included, is listed under its repository; clones stay apart (DI:230-274),
  and a family holder is one row with `relationships: []` (DI:276-290). A
  bare repository's row has `repository.root: null` and no clean suggestion
  (DI:238-239, DI:853-854), as change 1 refuses bare repositories (its OQ-15).
  Every repository first takes change 1's submodule test, and a submodule
  checkout gets `unsupported-layout` with no suggestion; a gitfile main
  checkout takes its root from `core.worktree` or the matching candidate,
  else gets `unsupported-layout` too; and a missing main worktree gets
  `main-worktree-missing` (requirement 2).
- **Every bound is reported.** The 32-root, 128-candidate and 512-worktree-row
  caps apply after canonical sorting; the 4,096-entry cap cuts a root's listing
  in directory order and reports `omitted` with exactness `unknown`
  (DI:117-121, DI:153-228). Dropped work is reported as
  `omitted: {count, exactness}`, and at most four Git children run at once,
  across distinct repositories (DI:429-449). Every filesystem call runs in a
  bounded task, and a manifest over the shared evidence model's 1 MiB bound,
  judged from its size before the read, is `manifest-invalid`. A cap, timeout
  or deadline makes the result `incomplete` and exits 1 (DI:222-225).
- **One candidate's failure stays in its row.** A per-candidate collector
  turns exceptions and failed probes into that row's errors (DI:528-537), and
  the scan continues (DI:513-566).
- **No second classifier.** Worktree classification is the cleanup ladder as
  change 1 leaves it, fed from the overview's memoized evidence; the merge
  target is `{name, source, sha}` in the baseline `default_branch` order, and
  its absence is a `no-merge-target` finding, not an error row (DI:551-630).
- **Findings by attention category.** Each finding has one code, category
  (repair, preserve, housekeeping, informational) and severity from the
  packet's table (DI:638-659). `--attention` shows every scan error, every
  error row and every row with a repair, preserve or housekeeping finding,
  hides informational findings within those rows, and changes neither the
  JSON, the summary nor the exit (DI:704-714).
- **Suggestions never carry permission.** A suggestion is an argv array naming
  the canonical `repository.root`: `project clean <root> --all-safe` only for
  a `merged-removable` worktree that passes the batch gates the overview can
  evaluate from its own evidence (`main-worktree`, `unsupported-path-bytes`,
  `registration-mismatch`, `locked-worktree`, and `unstarted-branch` or
  `reflog-unavailable` from one bounded read of the branch's reflog) in a
  repository change 1 would not refuse as `inspection-incomplete` or
  `inspect-cap` and with no row the overview left unprobed; otherwise the
  read-only `project clean <root>` where the attention table names it,
  except on the merge-target checkout (OQ-20); and no suggestion for a code
  the table marks none, a null `repository.root`, or a root or common
  directory that is not valid UTF-8. A finding names the gate that withheld
  or limited its suggestion in `suggestion_gate`, with a fixed remedy in its
  message. The batch may still exclude a suggested worktree through its
  index gates. Never `--apply` or `--yes`, never a bare name (DI:661-702,
  DI:847-886).
- **A versioned JSON envelope.** `--json` prints one `schema_version: 1`
  document with exactly the envelope, row, worktree, finding and summary
  fields and types of DI:724-819, plus the finding fields `suggestion_gate`
  and `suggestion_gate_rows`, three `limits` keys read from change 1's
  shared constants, `batch_row_cap`, `report_row_cap` and `targets`, and a
  validity flag beside every serialized path: `path_valid_utf8`
  beside each `path`, a finding's `checkout` and `ignored_samples` entries,
  now `{path, path_valid_utf8}` objects, included, and `root_valid_utf8` and
  `common_dir_valid_utf8` in `repository`.
- **A readable human report** in DI:83-96's shape: a `next` line says why a
  suggestion was withheld or limited, and the summary line always prints
  and says findings reflect local refs as of the last fetch.
- **Exits by completeness and severity.** 0 when complete with no `error`
  finding; 1 when incomplete, on an `error` finding, or on a `warning` under
  `--strict`; 2 for an invalid invocation, an exception outside the
  collector, or `git-too-old` or `git-unavailable` before any root is listed;
  130, 143 or 129 on SIGINT, SIGTERM or SIGHUP, after every child is
  terminated and reaped (or abandoned, if still unreaped 2 s after SIGKILL),
  with no result document and `Cancelled.` printed on a best-effort basis; a
  signal's status wins over 1 (DI:313-326, DI:1066-1098).
- **Default-branch health, absorbed from the closed PR #2.** A checkout
  classified `protected-default` gains every finding that applies, not the
  first: a `dirty` preserve warning when dirty; `diverged` or `unpushed`
  (preserve, warning) or `remote-ahead` (informational, info) from its
  ahead and behind counts; `unpublished` with no upstream while the ref
  listing holds a remote copy of the merge target, or `remote-gone` with its
  upstream gone (preserve, warning); each with no suggested command (OQ-19,
  OQ-20).
- **One carve-out in `project-review-safety`.** A manifest with an invalid
  text encoding is a `manifest-invalid` row error in the overview, which then
  exits 1, not 2 (Capabilities).
- **README and tests** describe and cover all of the above (Impact).

## Rules This Change Keeps

- **Local and read-only.** No fetch, pull, reset, bootstrap, validator run,
  file write or network connection; no worktree created, pruned, repaired,
  locked or unlocked; no credential file read; a memo that lives for one
  invocation (DI:273-274, DI:303-311).
- **Evidence is not permission.** No suggestion carries `--apply` or `--yes`;
  `project clean` recomputes, shows and confirms its own plan and may still
  exclude a suggested worktree (SY:122-130; DI:688-702, DI:879-886).
- **One classifier, one evidence model** (DI:596-630).
- **Unknown is never healthy.** A `null` that means not established
  (`present`, a `dirty` left by a failed probe, any `inspection-error` row)
  never reads as healthy, and an error row's empty `findings` means none
  were computed (DI:830-833). A `null` that means none (`upstream`, `ahead`
  and `behind` with no upstream configured; `merged_into_target` on a
  detached head; DI:781-785, BA:897-900) is an observation, not an error.
- **Incomplete is visible.** Every cap, timeout and deadline surfaces as
  `completeness: "incomplete"`, an error and exit 1 (DI:222-225).
- **Ordinary work is not trouble.** Housekeeping and informational findings
  stay distinct from warnings and errors (SY:308-309), and a merge-target
  branch with no remote copy at all raises no `unpublished` (OQ-20).
- **Grouping grants nothing.** Independent clones stay separate, and a later
  family grouping never permits cleaning a sibling (SY:34-37).

## What This Repository Does Not Own

- **Manifest schemas and shape mechanics**: openRepoShape. The overview reads
  a manifest only through `manifest()`, for name, kind and `tracking_branch`.
- **Bench, container and parked-work state**: workBenches and the Speckit git
  extension's park records; the overview reads none of them.
- **Pull-request and remote state**: GitHub, which no default overview reads.
- **Worktree, ref and status semantics**: Git, observed as of the last fetch.

## Capabilities

### New Capabilities

- `project-overview`: the `project overview` subcommand. The spec phase writes
  `specs/project-overview/spec.md` with twelve ADDED requirements (proposed
  header, then proposed text). Where one relies on change 1, its spec text
  cites the canonical header by name, never "change 1's" prose:
  - [E] `Repository inspection requires Git 2.36 and shares one evidence model`
    (project-command), whose readers are every subcommand that inspects a
    Git repository; the overview binds itself by citing it;
  - [L] `Clean classifies preservation and cleanup actions` (project-clean);
  - [G] `Clean previews and applies a batch of eligible worktree removals in one repository`
    and `Clean bounds its Git work and reports omitted work` (project-clean);
  - [R] `Clean resolves its target Git-first` (project-clean): the
    merge-target order with both `origin/` strips, and Git-first resolution;
  - [P] `Clean reports every path exactly or excludes it` (project-clean).
  1. `Overview discovers projects within configured roots only`: SHALL
     examine each root and its immediate entries only, by the marker table;
     when every root is `absent`, the human output SHALL say so, naming
     `--root` and `PROJECTS_DIR`.
  2. `Overview groups worktrees by repository identity`: rows SHALL be keyed
     by `{root, common_dir, dev, ino}`, `common_dir` from [E]'s identity
     probe, with [E]'s registration rule (relative values resolved,
     realpaths compared; BA:230-232); a family holder SHALL be one row.
     "Reached first" SHALL mean first in canonical candidate order, and
     where a bind mount gives two root spellings for one `(dev, ino)` the
     canonical-first SHALL win.
     Every repository SHALL first take [R]'s submodule test
     (`rev-parse --show-superproject-working-tree`), and a submodule
     checkout SHALL give `repository.root: null` with an
     `unsupported-layout` repair finding of severity error and no
     suggestion. Otherwise a bare main entry SHALL give a null root, as [R]
     refuses it, and when the first registry record's path equals
     `common_dir`, the main checkout is a gitfile checkout:
     `repository.root` SHALL be the realpath of `core.worktree`, else the
     `--show-toplevel` of a candidate that is that checkout, else null with
     an `unsupported-layout` repair finding of severity error and no
     suggestion, and that record SHALL NOT be a status-probe row. In the
     ordinary layout `repository.root` SHALL be the main worktree: the
     identity probe's toplevel only when the candidate that reached the
     repository first is the main worktree itself, else the canonical path
     of the first registry record, never a linked worktree's toplevel (the
     lead's R-14). A main worktree path that does not exist SHALL give
     `repository.root: null` with a `main-worktree-missing` repair finding
     of severity warning, the
     repository-wide probes running in the candidate. A suggestion for a
     gitfile checkout SHALL follow [R] (scenarios: `--separate-git-dir`, a
     submodule entry, a missing main worktree).
  3. `Overview bounds its work and reports what it omitted`: SHALL bound the
     run by its own 60 s invocation deadline and each Git child by [E]'s
     per-child rule under that deadline, `min(5 s, deadline - now)`, run each
     child in its own process group and stop it with SIGTERM to the group, then
     SIGKILL after 2 s, then reap it within a further 2 s grace or abandon it,
     its row recorded `probe-timeout`; SHALL run every filesystem call, root
     canonicalisation and dedupe, marker and holder checks, manifest reads and
     branch reflog reads (at most 64 KiB each, an unfinished one leaving its
     row unprobed for requirement 7's gate) included, in a bounded daemon
     task waited for with `min(5, deadline - now)`, a manifest whose
     `st_size` exceeds [E]'s 1 MiB
     being `manifest-invalid` unread and no read exceeding 1 MiB; SHALL parse
     the ref listing as it streams, keeping heads, `origin/HEAD`, the remote
     refs named as upstreams and one flag for a remote copy of the merge
     target; SHALL apply the root, candidate and worktree-row caps after
     sorting and the entry cap in listing order, and report each dropped unit.
     It SHALL schedule in two canonical phases and start a repository's phase 2
     only when every candidate earlier in canonical order has completed or
     failed its identity probe and every repository earlier in canonical order
     has finished its phase 1 (DI:446-448); speculative phase-1 dispatch stays
     legal. Without both conditions a run where the worktree-row cap binds
     would select rows by completion order. In a run in which no child, task or
     root listing reaches its budget and the deadline does not expire, the
     JSON, apart from timestamps and `budget.probe_concurrency`, SHALL NOT
     depend on concurrency or completion order; a cut run SHALL report each cut
     unit with `omitted` and DI:165-169's exactness. It SHALL report
     `probes: {estimated, performed}` as DI:503-511 defines (scenarios:
     concurrency 1 and 4 on one fixture give byte-identical JSON less
     timestamps and `probe_concurrency`; a root, and a `repository.root`, on a
     hung mount, by an injected slow call where FUSE is unavailable; a manifest
     over the bound).
  4. `Overview isolates one candidate's failure`: a failure SHALL become that
     candidate's error row and SHALL NOT change any other row.
  5. `Overview reuses the cleanup classifier and merge target`: SHALL classify
     by [L]'s ladder over [E]'s evidence and report the merge target
     `{name, source, sha}` resolved in [R]'s order, both `origin/` strips
     included.
  6. `Overview reports findings by attention category`: severity SHALL decide
     the exit, and `--attention` SHALL change only the display; a worktree
     whose upstream was deleted SHALL be classified as [L] classifies it,
     `merged-removable` (or `merged-current`) with that class's finding and
     suggestion when the merged set shows its ancestry, and `remote-gone`,
     with the read-only suggestion, only when it does not (Brett Heap's
     ruling of 2026-10-09; Decisions, departures).
  7. `Overview suggests only gated clean commands`: SHALL suggest argv naming
     `repository.root`, `--all-safe` only behind the gates of [G] it can
     evaluate from its own evidence (`main-worktree`,
     `unsupported-path-bytes`, `registration-mismatch`, `locked-worktree`,
     and `unstarted-branch` or `reflog-unavailable` from one bounded
     filesystem read of the branch's reflog, as [G] reads it: the anchor is
     the last surviving entry whose old object is all zeros (a creation by
     any command, `git fetch origin feat:f1` included) or whose message
     begins `branch: Created from` or `branch: Reset to`, and a movement a
     later entry, or any entry when no anchor survives, whose old and new
     objects are non-zero and differ, a rename's entry being none
     (the lead's R-15); a last
     entry whose new object is not the head is `reflog-unavailable`, tested
     first; a movement passes, so a fast-forward-merged branch at the
     target's tip passes; an anchor with no movement after it, at the head,
     is `unstarted-branch`, as is a branch reset to the target's tip by
     `worktree add -B`; and one outcome rule makes a missing, empty,
     bound-reaching or undecidable reflog `reflog-unavailable`, any other OS
     error the row's `inspection-error`, and an unfinished read an unprobed
     row (`inspection-incomplete`); only the index gates stay residual
     exclusions the batch applies) and [G]'s `inspection-incomplete` and
     `inspect-cap`
     refusals, and with no row left unprobed; a `merged-removable` worktree
     withheld by either reflog code SHALL keep its finding with the
     read-only suggestion. It SHALL name the gate that withheld or limited a
     finding's suggestion in `suggestion_gate`, each code with a fixed remedy
     in the finding `message` and the human text, naming the batch's row cap
     and target limit and taking their numbers at run time from the shared
     constants, never from a clean plan and never copied:
     `inspection-incomplete` "repair the inspection-error rows, or re-run
     for the rows left unprobed, first"; `inspect-cap` "N rows exceed the
     batch's row cap of M; remove explicitly" or "N rows exceed the report's
     row cap of M; the report would be incomplete", the JSON finding carrying
     N in `suggestion_gate_rows` and M in `limits`; `scan-limit` and
     `deadline-exceeded` "re-run with --root <repository parent>";
     `unstarted-branch` "no commit was made on this branch here since it
     was created; review, then git worktree remove yourself";
     `reflog-unavailable` "the branch's reflog is missing, expired or
     undecidable; review, then git worktree remove yourself";
     `target-not-repository-root` "run project clean from the main worktree
     root"; `unsupported-path-bytes` "rename the path to valid UTF-8"; and
     `target-cap`, a limiting gate set when more gate-passing
     `merged-removable` rows keep the `--all-safe` suggestion than the
     batch's target limit, "limited to the batch's target limit of M per
     run; re-run to drain the backlog" (scenarios: 17 eligible rows; a
     fast-forward-merged branch; a branch reset by `worktree add -B`; a
     branch created by `git fetch origin feat:f1` at the target's tip and
     given an upstream by `git branch -u origin/feat f1`, which writes no
     reflog entry; a missing, an empty, an expired and a rewritten reflog; an
     unreadable
     one). The
     null-root findings carry no gate code and their remedy in their
     message: `unsupported-layout` "set core.worktree or move the checkout",
     `main-worktree-missing` "restore or prune the main worktree by
     hand".
  8. `Overview prints a versioned JSON envelope`: SHALL print one
     `schema_version: 1` envelope with DI:724-819's fields plus
     `suggestion_gate`, `suggestion_gate_rows`, the `limits` keys
     `batch_row_cap`, `report_row_cap` and `targets`, read from the shared
     constants and never from a clean plan, and a validity flag beside every
     serialized path (`path_valid_utf8`, `root_valid_utf8`,
     `common_dir_valid_utf8`; `ignored_samples` entries as
     `{path, path_valid_utf8}` objects); a `--json` exit 2 other than an
     argument error prints `{"error", "code"}` with code `git-too-old`,
     `git-unavailable`, `refused`, `os-error` or `internal-error`, and an
     argument error prints argparse's usage on standard error and no JSON.
     SHALL emit every path by [E]'s parsing and [P]'s rules: exactly when valid
     UTF-8, else escaped with its flag false; SHALL print a path holding a code
     point of Unicode general category Cc, Cf, Zl or Zp (control, format, line
     and paragraph separators, [P]'s listed characters being examples) or an
     undecodable byte in `$'...'` form, with `\UXXXXXXXX` above U+FFFF, and
     SHALL give a non-UTF-8 worktree path, root or common directory an
     `unsupported-path-bytes` finding and no clean suggestion (scenarios
     DI:1338-1347, DI:1392-1408, and a common directory that is not valid
     UTF-8, the lead's R-3).
  9. `Overview is local and read-only`: SHALL make no network connection and
     no filesystem or Git mutation.
  10. `Overview reports default-branch health`: a merge-target checkout
      classified `protected-default` SHALL keep that classification and gain
      every applicable OQ-19 and OQ-20 finding, never only the first,
      `unpublished` only where the ref listing holds a remote copy of the
      merge target (scenarios: a default branch pushed without `-u`, then
      given two local commits, shows an `unpublished` preserve warning under
      `--attention`; a repository with no remote shows none; a dirty default
      branch ahead by 3 gives both `dirty` and `unpushed`).
  11. `Overview exits by completeness and severity`: SHALL exit 0, 1, 2 or
      130 as DI:1070-1075 defines, and 143 or 129 on SIGTERM or SIGHUP;
      SHALL refuse Git older than 2.36 with `git-too-old`, and a missing or
      unusable `git` with `git-unavailable`, by [E]'s version check and with
      exit 2 before listing any root; on any of those signals SHALL
      terminate and reap every child as requirement 3 states (abandoning one
      still unreaped 2 s after SIGKILL), print no result document, print
      `Cancelled.` to standard error on a best-effort basis and exit with
      that signal's status, which wins over 1; its main thread SHALL never
      block in an unbounded filesystem call.
  12. `Overview renders a readable human report`: SHALL adopt DI:83-96's
      shape: one header line per row (name, absolute path); one line per
      shown finding (category, code, message, plus the worktree path for a
      worktree's finding); one `next` line carrying the row's suggested
      command, followed by `(withheld: <reason>)` when a gate removed the
      `--all-safe` form or every clean suggestion (`inspection-incomplete`,
      `inspect-cap` over the batch's row cap, an unprobed row,
      `unstarted-branch`, `reflog-unavailable`, `target-not-repository-root`,
      `unsupported-path-bytes`), or `(limited: <reason>)` when a suggestion
      is given but capped (`target-cap`, or `inspect-cap` over the report's
      row cap on the read-only command); an `Incomplete:` line per scan
      error; and always the summary line, even under `--attention` with no
      row shown ("nothing needs attention" plus the counts), stating that
      findings reflect local refs as of the last fetch. SHALL write a
      one-line `Scanning N roots...` notice to stderr only when stderr is a
      TTY (scenarios: an empty `--attention` run; a gated suggestion).

  It is a new capability rather than ADDED requirements in `project-command`
  (OQ-2): `overview` is a whole subcommand with its own contract, as `clean`
  has `project-clean`. The prefer-triad proposal dropped its standalone
  capability because the archived reason for one, specs not yet archived, no
  longer applies (its `proposal.md`, lines 321-326).

### Modified Capabilities

- `project-review-safety`: one MODIFIED requirement, whose canonical header
  is `### Requirement: YAML decoding errors are structured refusals` (PRS:78)
  and whose canonical text is:

  > Every YAML input read by the command SHALL turn an invalid text encoding
  > into a normal refusal. JSON mode MUST preserve its structured error output
  > and exit code 2 rather than printing a traceback.

  The overview conflicts with "exit code 2": its collector turns the `Refused`
  that `manifest()` raises for such a manifest into a `manifest-invalid` row
  error and exits 1 with the other rows intact (DI:530, within DI:528-531;
  DI:1279-1286). The MODIFIED block keeps both sentences and the canonical
  scenario for every other command, and adds that in `project overview` such
  a manifest SHALL be a `manifest-invalid` error on its candidate's row,
  never a traceback, while the run continues and exits 1, with one scenario.

In sum: one new capability, `project-overview`, with 12 ADDED requirements,
and one MODIFIED requirement in `project-review-safety`. Untouched: its other
five requirements (PRS:9, :21, :32, :51, :67), since the overview renders no
profile field, reads no bench registry or parked work, applies no update and
renders no nested estate or leg; `project-command`, `project-clean` and
`project-clean-review-safety`, which only change 1 modifies; and
`speckit-extension-integration`.

## Impact

- **`project`**: a new `overview` subcommand; a per-candidate collector, the
  two-phase four-way scheduler with its in-flight child registry and daemon
  filesystem workers, over change 1's shared probes and runner; human and
  JSON renderers. Every other subcommand changes only as change 1 changes it.
  The `code` field for `refused`, `os-error` and `internal-error`, and exit 2
  for an exception outside the collector, apply to `project overview` only;
  other subcommands keep `main()`'s handling (`project:995-1003`) apart from
  change 1's two Git codes. No new dependency: manifest reads use `manifest()`
  and so the existing PyYAML requirement (`requirements.txt:2`,
  `project:37-41`); without PyYAML each manifest row carries a
  `manifest-invalid` error and the run exits 1, and every other path uses
  the standard library.
- **`README.md`**: a section for `project overview` covering roots and
  `PROJECTS_DIR`, the caps, `--attention`, `--strict`, the exits, the JSON
  envelope, and that a suggestion is advice to review, not permission; how
  to check one project (`project overview --root <dir>`, replacing PR #2's
  doctor health); that `git fetch` refreshes merge evidence; that roots on a
  Windows drive mounted into WSL2 can truncate on every run; and that a
  merged worktree whose upstream was deleted gets the gated `--all-safe`
  suggestion like any merged worktree, while an unmerged `remote-gone` one
  gets only the read-only `project clean <root>`, which reviews it.
- **A merged worktree whose upstream was deleted is housekeeping** (Brett
  Heap's ruling of 2026-10-09; Decisions, departures); only an unmerged
  `remote-gone` worktree's suggestion is review-only, by design.
- **`tests/test_project.py`**: temporary fixtures only, network disabled,
  zero-mutation snapshots, covering the packet's 31 MVP scenarios
  (DI:1175-1446), the default-branch findings, the carve-out and a manifest
  row read without PyYAML. Where CI cannot host a fixture ("Hung filesystem
  call" needs FUSE), design chooses an injected slow call or a skip with its
  reason; as in change 1, the non-UTF-8 path scenarios run on Linux only,
  skipped on macOS with that reason. Tests run with
  `python3 -m unittest discover -s tests -v` (README.md:187), the command
  CI runs as `python -m ...` (`.github/workflows/tests.yml:18`).
- **Speckit handoff**: exactly one feature, `specs/005-<slug>/`, created by
  `/speckit.specify` after ratification and after feature 004 merges. `002`
  is lane openRepoProject-1's, merged by PR #8; `003` is lane
  openRepoProject-1's too (PR #17); `004` is change 1's. OpenSpec
  `tasks.md` holds governance boxes, the cap measurement (OQ-4) and that one
  handoff only.
- **Expected conflicts**: feature 004, like the merged PR #8 (`d7f6b0e`, 94
  tests), touches `project` and `tests/test_project.py`; feature 005 merges
  `main` in and never rebases. PR #13 (`7a9134b`) archived
  `prefer-triad-in-project-new` and touched only `openspec/`, so `project`
  and the tests are as at `d7f6b0e`.
- **Review inputs**: the repo-local propose flow names `docs/requirements/`
  and `docs/architecture/` (`.claude/commands/opsx/propose.md:65-69`), which
  this repository lacks; the reviews read the packet, `openspec/specs/`,
  `openspec/config.yaml` and `project` instead.

### Dependencies and Sequencing

This is change 2 of two. Change 1 is `add-project-clean-all-safe` (issue #9),
drafted in parallel. This change depends on it, cites it by name, and does not
restate its contract. Change 1 owns:

- the shared evidence model: the version check, the four repository-wide
  probes memoized per `common_dir`, the combined status probe per worktree row
  and its record bounds, NUL-delimited parsing and path escaping, the child
  environment, the 1 MiB manifest read, over-cap judged from the file's size
  before the read (so `clean` and the overview resolve the same merge
  target), and the bounded runner, not `probe()`, for
  one Git child in its own process group (DI "Probe model and deadline",
  DI:292-511; SY "One evidence model; permission is not shared", SY:78-130).
  [E] names the per-child budget, `min(5 s, work remaining)` under an
  invocation deadline, and the overview applies that rule under its own
  deadline arithmetic: 60 s with no reserve, then up to 2 s from SIGTERM to
  SIGKILL and up to 2 s of reap wait, 60 + 2 + 2 = 64 s, where `clean`'s is
  50 + 10 + 4 (requirement 3). The version check's timing stays the
  overview's own: before any root is listed (requirement 11).
  This change owns running up to four such children at once, terminating
  every in-flight child together on SIGINT or deadline, and its filesystem
  workers, on daemon threads and never in a `concurrent.futures` pool, so an
  abandoned call cannot hold process exit beyond what DI:480-485 allows;
- the Git 2.36 floor and its codes `git-too-old` and `git-unavailable`
  (SY:51); this change applies that check to `project overview`, which
  refuses before any root is listed (requirement 11);
- every modification to `project-clean`, `project-clean-review-safety` and
  `project-command`, among them the ladder's names and order, the
  deleted-upstream `remote-gone` change and Git-first resolution of
  `project clean <path>` (DI "Baseline behavior changes", DI:1100-1173; BA
  "Command directory and repository resolution", BA:834-878), and change 1's
  R1: at `a040790` a failed `git status` in a repository root raises
  `Refused` (`project:326-328`) and ends clean, status, doctor and update
  with exit 2 (`project:995-1000`), while under the shared model it is a
  row-level `inspection-error`, which the overview inherits;
- the cleanup gates and refusal codes the overview's suggestions mirror: the
  per-worktree gate order `main-worktree`, `unsupported-path-bytes`,
  `registration-mismatch`, `locked-worktree` (BA "Eligibility and
  merge-target terminology", BA:113-199), with `unstarted-branch` and
  `reflog-unavailable`, which change 1's council added and whose bounded
  reflog read the overview mirrors within its own filesystem budget, the
  plan refusals
  `inspection-incomplete` and `inspect-cap` (BA "Refusal codes", BA:987-1015)
  and the batch's worktree-row cap (BA "Cap arithmetic", BA:721-774).

Consequences:

- This change modifies none of those three specs. The overview's repository
  gate is defined by change 1's refusals: it withholds `--all-safe` when
  change 1's batch would refuse that repository's plan as
  `inspection-incomplete` or `inspect-cap`, each computed from the overview's
  own evidence, and also when the overview's own 512-row cap or deadline left
  any of its rows unprobed (`classification: null`). It copies no number, so
  a cap that measurement moves in change 1 carries over. It does not predict
  a plan cut by the batch's own deadline. More gate-passing rows than the
  batch's target limit keep the suggestion under the limiting gate
  `target-cap` (Decisions, departures).
- The overview needs change 1's runner as a child handle (start, readable
  fds, `terminate_group` with the 2 s grace, reap), one-wide and four-wide,
  and pure incremental byte parsers for the status, registry and ref
  listings; change 1 records that constraint in its `clarifications.md`.
- Change 1 resolves a gitfile main checkout through `core.worktree` or the
  candidate toplevel and refuses a submodule checkout, tested first, as
  listed baseline changes ([R]; its R11). The overview applies the same
  submodule-first order to every repository and gives a submodule checkout
  `unsupported-layout`, so it never suggests what `project clean` refuses
  (requirement 2).
- PR #8 has merged (`d7f6b0e`, with 94 tests), and PR #13 (`7a9134b`)
  archived `prefer-triad-in-project-new`, merging its requirements into the
  canonical `project-command`; that spec at `7a9134b` is the base change 1
  modifies, and `origin/main` is `f401e06` at this commit (`26a5668` merged
  at `12febc0`; `f401e06`, lane 1's PR #17, merged below). Every `project:N`
  and README citation stays pinned at `da33d92`; at `d7f6b0e` the cited
  `clean` and `repo_state` code (`manifest()` onward) sits 141 lines lower and
  README.md:187 is :275, and feature 005's specify and plan re-pin citations
  against the `main` of that day.
- Change 1 is ratified first. This change's spec deltas are written against
  change 1's ratified text, and a gate, code or probe that moves in change 1's
  review re-aligns this proposal before its own ratification.
- Speckit feature 005 is created after feature 004 merges, because the
  overview runs on the probes 004 builds; this change archives after change 1.
- How the ladder becomes reusable is change 1's decision (OQ-28, DI:599-600);
  this change needs it fed from memoized evidence, spawning no probe.
- If Brett prefers one change, this proposal folds into a single
  `add-project-maintenance` change with one Speckit feature (OQ-1).

## Out of Scope

Each extension below needs its own proposal (OQ-27):

- **Branch deletion.** Worktree removal leaves the local branch, and
  `delete-branch` stays a separate explicit action (OV:36, OV:170-171;
  BA:329, BA:1281-1293).
- **Cache disposal** (OV:144, OV:151-152; BA:1314-1337).
- **Remote, GitHub or pull-request queries**, including a
  `project overview --remote` and `09af8c8`'s lookups; the packet's sketch of
  an opt-in boundary (DI:1036-1064; HO:160-167) is not adopted here.
- **Family traversal and relationships** (DI:276-290, DI:1062-1064;
  SY:34-37).
- **Bench, container and park integrations** (OV:142-146; DI:1062-1064).
- **Paired retirement.** A future proposal must MODIFY `project-clean`'s
  "Clean can explicitly retire verified worktrees", because it changes
  `remove` (BA:60-63; HO:36-39; PR #2 decision record), and keep the
  post-removal stage contract of BA:1339-1345.

Also out of scope, as the packet already holds: an estate-wide destructive
batch, merge or branch reconciliation, squash-merge retirement, a lock or
quiescence protocol, a persistent cache or plan, an arbitrary-depth scan, and
the exact bench/type doctor check (OV:148-157, OV:361-366; SY:233-235). So are
a `project attention` alias (OQ-17), user-configurable limits (OQ-8), and any
change to `project clean` or `project doctor` (change 1's, OQ-22).

## Decisions Taken by This Proposal

Each is a proposal decision, open to ratification. OQ numbers are this lane's
list for both changes: OQ-1 to OQ-3, OQ-20 to OQ-22 and OQ-29 are lane
additions; OQ-23 and OQ-24 are departures from packet decisions
(BA:1241-1245; BA:949-953 with HO:210) and OQ-28 a packet open decision
(DI:599-600); the others number the packet's consolidated open decisions
(OV:311-359; HO:317-353). OQ-10 to OQ-16, OQ-22 to OQ-24, OQ-28, OQ-29 and
the batch half of OQ-25 are change 1's. OQ-19 to OQ-21, and the one record
OQ-22 leaves here, are in the absorption subsection below.

Packet open decisions taken, each citing the packet text that leaves it open:

- **OQ-4, measured costs** (OV:314-319; DI:179-180, DI:189-190,
  DI:227-228): the spec deltas mark the caps provisional, and the governance
  `tasks.md` carries the warm and cold-cache measurement, run on a Linux
  filesystem and never on a Windows drive mounted into WSL2, before the
  Speckit handoff; it includes the cold time of one 4,096-directory root
  against the 5 s root bound and `for-each-ref` on one large-ref repository.
- **OQ-6, concurrency** (OV:320-327): four children across distinct
  repositories. If design rejects concurrency, the packet's serial fallback
  of 32 candidates and 128 worktree rows applies (DI:1465-1471).
- **OQ-7, a per-repository row cap** (OV:328-331): none. A repository with
  more than about 355 worktree rows ends at the deadline, visibly
  incomplete, if children cost the 150 ms margin rate; OQ-4's measurement
  settles it (DI:219-223, DI:1473-1476).
- **OQ-8, configurable limits** (OV:332): none; the fixed values are reported
  in `limits` and `budget`.
- **OQ-17, an `attention` alias** (OV:350; DI:1482-1483): no (DI:72-75).
- **OQ-18, `--attention --json`** (OV:350-352; DI:1478-1479): the full
  envelope; consumers filter on `findings[].category` (DI:709-714).
- **Suggestion display string** (OV:353; DI:1479-1480; unnumbered): argv
  arrays only in JSON. Human output prints the command with shell quoting,
  or in the `$'...'` form for a path that needs it (DI:910-925; [P]). The
  pasteable `$'...'` form assumes bash 4.2 or newer, or zsh; tests assert the
  rendered string, not a shell round trip on macOS's bash 3.2.
- **OQ-26, spelling** (OV:356):
  `project overview [--root D]... [--attention] [--json] [--strict]`.
- **OQ-27, separate changes** (OV:357-359): yes, one per extension.

Packet decisions adopted, not open:

- **OQ-5, caps** (OV:35; DI:171-177): 32 roots, 4,096 entries per root, 128
  candidates and 512 worktree rows, provisional until OQ-4. The record
  bounds (64 ignored, 4,096 records, 8 samples) are [E]'s shared values.
- **OQ-9, deadlines** (DI:451-485): 60 s per invocation, 5 s per child and
  per root listing, 2 s from TERM to KILL. The 60 s deadline and the per-root
  listing bound are the overview's own (requirement 3): the full 60 s, with
  no reconciliation reserve and no removal floor; the 5 s per child is
  [E]'s rule under that deadline, `min(5 s, deadline - now)`, and the 2 s
  grace is stated there too.
  `budget` holds only `probe_timeout_seconds`, `invocation_timeout_seconds`
  and `probe_concurrency`.
- **OQ-25, overview exits** (DI:1066-1098): 0, 1, 2 and 130; 130 wins over 1
  (requirement 11, which departs below for SIGTERM and SIGHUP).

Lane additions here: **OQ-1, one change or two**: two, batch first; this is
the second. **OQ-2, where the overview lives**: a new `project-overview`
capability. **OQ-3, revise the packet first or absorb**: absorb here
(Corrections). OQ-20 and OQ-21 follow in the absorption subsection.

Departures from packet decisions, each citing the decision departed from:

- **Default-branch findings** (DI:704; DI:645, DI:648-651): OQ-20, below.
- **Unprobed rows close the repository gate** (DI:675-686, DI:855-859, which
  name only `inspection-error` rows and the batch's row cap): a row the
  overview's own cap or deadline left unclassified could hide an
  `inspection-error`, so the gate withholds `--all-safe` for it as well.
- **`suggestion_gate`** (the finding object, DI:810-819): a field beside
  `suggested_command` on every finding, null unless a gate withheld or limited
  that suggestion, else the gate's code. A withheld `--all-safe` form names
  `inspection-incomplete`, `inspect-cap`, `scan-limit` or `deadline-exceeded`
  for an unprobed row, or `unstarted-branch` or `reflog-unavailable`; a
  withheld clean suggestion names `target-not-repository-root` (a bare
  repository, which change 1 refuses) or `unsupported-path-bytes` (a root or
  common directory that is not valid UTF-8, which change 1 refuses too); a
  read-only suggestion for a repository over change 1's report row cap names
  `inspect-cap`, since that report would be incomplete. A repository over the
  batch's row cap but within the report's gets the plain read-only suggestion,
  with no gate on findings whose table suggestion is that command. Both
  `inspect-cap` bands keep one code (D-P's values are change 1's codes, with
  `target-cap` carrying its deferral meaning), told apart by
  `suggestion_gate_rows` (requirement 7).
- **`target-cap` limits, it does not withhold** (BA:96-101 refuses apply
  over 16 gate-passing rows; D-J kept the suggestion ungated): `--all-safe`
  stays, with `suggestion_gate: target-cap` and requirement 7's message, as
  change 1's council has the batch select rows up to its target limit in
  canonical order, defer the rest as `deferred-target-cap`, allow apply and
  drain the backlog on re-runs.
- **`unstarted-branch` and `reflog-unavailable` mirrored from the reflog**
  (DI:661-673 names four gates): the overview reads each remaining
  `merged-removable` worktree's branch reflog, `logs/refs/heads/<branch>`
  under `common_dir`, by one bounded filesystem task of at most 64 KiB,
  never a Git child, as change 1's gate reads it under the lead's amended
  V2, R-1, R-12 and R-15. It decides from the anchor, the last surviving
  entry whose old object is all zeros, a creation by any command, or whose
  message begins `branch: Created from` or `branch: Reset to`, so a branch
  created by `git fetch origin feat:f1` at the target's tip and given an
  upstream by `git branch -u origin/feat f1` (which writes no reflog entry),
  or reset to it by `worktree add -B`, stays unstarted, while a movement (an
  entry after the anchor, or any entry when no anchor survives, whose old
  and new objects are non-zero and differ; a rename's entry is none)
  passes, so a branch fast-forward merged into the
  target, sitting at its tip, passes. A last entry whose new object is not
  the head, tested first, and a missing, empty, bound-reaching or
  undecidable reflog are
  `reflog-unavailable`; any other OS error makes the row
  `inspection-error`, and an unfinished read leaves it unprobed
  (`inspection-incomplete`). Either code keeps the finding with the
  read-only suggestion, that `suggestion_gate` and requirement 7's message.
  Only the index gates stay residual exclusions the batch applies.
- **Determinism scoped** (DI:440-449, "never depends on timing"):
  requirement 3 promises timing-independent JSON only for an uncut run, and
  starts a repository's phase 2 only once every candidate earlier in
  canonical order has completed or failed its identity probe and every
  repository earlier in canonical order has finished its phase 1
  (DI:446-448).
- **Two layout findings** (DI:634-659's closed list; DI:236-239): repair,
  no suggestion: `unsupported-layout` of severity error, since a repository
  whose checkout cannot be named is unknown and unknown is never healthy,
  given also to a submodule checkout, which change 1 refuses, so the
  overview never suggests what `project clean` refuses (the lead's R-2);
  and `main-worktree-missing` of severity warning (requirement 2).
- **A validity flag beside every serialized path** (DI:724-819, where the
  project row's one `path_valid_utf8` covers `path`, `repository.root` and
  `repository.common_dir` (DI:748), and a finding's `checkout` and the
  `ignored_samples` strings carry none): `path_valid_utf8` sits beside every
  `path`, a finding's `checkout` and an error object's included, and speaks
  for that path alone; `repository` carries `root_valid_utf8` and
  `common_dir_valid_utf8`, false beside the `unsupported-path-bytes`
  finding; and each `ignored_samples` entry is a `{path, path_valid_utf8}`
  object, the shape change 1 adopts, so a `\xHH` escape never reads like a
  valid path holding those four characters (the lead's R-9, on Codex's
  finding on PR #12).
- **Escaping by general category** (the packet's single escape form,
  `\uXXXX` for every escaped code point, HO:301-306 and SY:247-250; and
  DI:910-916's enumerated set of control, bidirectional and format
  characters): every code point of
  Unicode general category Cc, Cf, Zl or Zp, as the running interpreter's
  `unicodedata.category` reports it, is escaped in JSON and puts its path in
  the `$'...'` form in human output, the packet's enumerated characters
  being examples, so U+200B, U+FEFF, U+00AD and the tag characters are
  caught too; and human output writes a code point above U+FFFF as
  `\UXXXXXXXX`, where the packet has only `\uXXXX` (the lead's R-8,
  on Codex's finding on PR #11, listed here by R-14).
- **SIGTERM and SIGHUP** (DI:1070-1075, DI:1094-1096, which treat SIGINT
  only): the SIGINT treatment, exits 143 and 129, so no Git child outlives
  the overview in its own session; after SIGHUP printing can fail with EIO,
  so `Cancelled.` is printed on a best-effort basis.
- **Local ancestry outranks a deleted upstream** (open question 1, ruled
  "yes, local ancestry proof outranks remote-gone, apply it" (Brett Heap,
  2026-10-09, to lane openRepoProject-2); DI:596-598, the ladder's "same
  test order" and "same recommendation text", and DI:1124-1129, where a
  deleted upstream is `remote-gone` and "nothing becomes removable"): the
  overview mirrors [L], which tests local ancestry before the `remote-gone`
  rung for worktree rows, so a worktree whose upstream was deleted and whose
  tip the merged set shows to be an ancestor of the merge target is
  `merged-removable` (or `merged-current`), with the housekeeping finding and
  the gated `--all-safe` suggestion, and only an unmerged one is
  `remote-gone`, with the read-only suggestion (requirement 6). The ruling
  supersedes R-6: the interim message that called such a worktree not
  removable, which R-6 had requirement 6 quote, is withdrawn. Default-branch
  health is untouched: its `remote-gone` finding on a `protected-default`
  checkout (requirement 10; design D4; OQ-20) reads the checkout's own
  upstream, not the ladder.

### Absorbing Doctor Repository Health from the Closed PR #2

PR #2 was closed unmerged on Brett Heap's word. Its decision record (PR #2
comment 6035824335, linked at OV:186; paraphrased at OV:180-183) assigns
`acf0133` and `80fdef3` to this design: "Absorbed into the packet's
project-overview design as local-only, read-only reporting." The packet left
that to its next revision (HO:35-39, HO:379-380; OV:180-183); this proposal
does it directly (OQ-3).

What the two commits add (`git show <sha> -- project` on `origin/cleanup`,
`bb91a49`): doctor attaches `repository_health` to each complete snapshot,
recursing into family members but not project legs, with `target_branch`,
`tracking_freshness` and the cleanup rows plus `health_level`,
`health_status` and `health_recommendation`. A `protected-default` row is
`ok` unless the first of `dirty-`, `ignored-local-files-`, `diverged-`,
`unpushed-` or `remote-ahead-default` matches, in that order, and `80fdef3`
checks `inspection-error-default` (a null `dirty` or `ignored_files`) first;
every other row is a `warning`. Any `Refused` from `cleanup_report`, a
missing default branch included, makes health `unavailable`, a warning, and
doctor continues; an `OSError` still ends doctor with exit 2. In practice
only a missing Git checkout or default branch reaches `unavailable`:
`snapshot` reads the manifest and the top-level status first
(`project:679-681`, as in `acf0133`) and exits 2 if either fails. One check
row per snapshot feeds `--strict`. Nothing is fetched.

| acf0133 / 80fdef3 element | Where the overview carries it | Status |
| --- | --- | --- |
| `target_branch` | `merge_target {name, source, sha}` (DI:570-594) | Subsumed (superset) |
| `tracking_freshness` | `git.tracking_freshness` (DI:760-763) | Subsumed |
| Per-row classification and recommendation | worktree `classification`, finding `message` (DI:790, DI:817) | Subsumed |
| Every non-default row is a warning | category and severity table (DI:638-659) | Changed on purpose: `merged-removable`, `pushed-unmerged`, `merged-current` and `remote-ahead` are `info`; `inspection-error` is `error`; the other classifications stay `warning` (DI:638-659; SY:308-309) |
| `dirty-default` | the extra `dirty` preserve finding (DI:626-630), beside any drift finding | Changed on purpose: no longer masks drift (OQ-19, OQ-20) |
| `diverged-`, `unpushed-default` | `diverged`, `unpushed`, preserve, warning (OQ-20) | Subsumed |
| `ok` with no upstream, or with the upstream gone | `unpublished` (only where a remote copy of the merge target exists) or `remote-gone`, preserve, warning (OQ-20) | Changed on purpose: unverified local commits warn |
| `remote-ahead-default` | `remote-ahead`, informational, info (OQ-20) | Changed on purpose: warning to info |
| `ignored-local-files-default` | none | Changed on purpose (OQ-20) |
| `inspection-error-default` | `inspection-error`, repair, error (change 1's R1) | Subsumed by change 1's R1; escalated: warning to error |
| `inspection-error-default` on a null `ignored_files` alone | `dirty` finding when the stream stopped before any ignored record (DI:414-417) | Changed on purpose |
| Unavailable: no merge target | `no-merge-target`, repair, severity error, exit 1 (DI:551-558) | Escalated (OQ-21) |
| Unavailable: no Git checkout | row with null `repository` and `git`, no finding | Changed on purpose: no warning |
| Unavailable: manifest refused, or status failed | `manifest-invalid`, or `probe-failed` with `inspection-error` (change 1's R1), as a row error, exit 1 | Changed on purpose: doctor ends with exit 2 in `snapshot` before health runs; the overview keeps the error in the row |
| Aggregate check row and `--strict` | `summary.findings` and the `--strict` exit (DI:704-707, DI:1068-1075) | Subsumed |
| Recursion into family members | holder row only, `relationships: []` (DI:276-290) | Changed on purpose: no traversal of members or legs; a member that is an immediate entry of a configured root is its own row (DI:287-290) |

Two of PR #2's open review threads concern this work: "doctor `--strict`
health-warning coverage" is answered by the severity-to-exit rule, and the
`acf0133` part of "doctor rendering unknown inspection state as zero counts"
(`dirty` and `ignored` printed as `None`) by "`null` means unknown or not
established" (DI:830-833); its zero `disposable` and `blocking` counts come
from the cache commit `1789ad9` and belong to the cache-disposal extension.
Not carried: `09af8c8`'s remote merge target and pull-request lookup, which
waits for a remote-queries proposal (PR #2 harvest table); remote evidence
never proves cleanup (SY:219-226).

Decisions, each open to ratification:

- **OQ-19, the extra `dirty` finding** (packet open decision, OV:354-355;
  DI:1480-1481; DI:626-630): kept. A dirty checkout on the merge target
  stays `protected-default` and gains one `dirty` preserve finding, beside
  any OQ-20 finding; it replaces `acf0133`'s `dirty-default`.
- **OQ-20, default-branch drift and inspection** (lane addition). On a
  checkout the ladder classifies `protected-default`, the overview adds from
  evidence it already holds every finding that applies, not a first match:
  `dirty` (OQ-19) when dirty, and besides it one of `diverged` (ahead and
  behind both above 0) or `unpushed` (ahead above 0), each preserve and
  `warning`, or `remote-ahead` (behind above 0), informational; with no
  upstream configured and a remote copy of the merge target in the ref
  listing (`refs/remotes/<remote>/<name>`, one flag in the streaming parser,
  no new probe), `unpublished` (preserve, warning) with the message
  "merge-target branch has no upstream; local commits are unverified", a
  repository with no such copy being ordinary work, not trouble; with its
  upstream `gone`, `remote-gone` (preserve, warning). This supersedes
  the first-match reading applied for QA-19, `acf0133`'s single slot (council
  AE-1). They reuse their codes on a row whose classification stays
  `protected-default`, departing from DI:704 ("`protected-default` produces
  no finding by itself"), and add no `-default` code. A checkout whose
  status probe failed, timed out or was cut by the deadline is
  `inspection-error` by change 1's ladder (its R1), on the merge-target
  branch too, with that code's repair finding of severity error, exactly as
  `project clean` classifies it; the drift findings apply only to a checkout
  classified `protected-default`. There the six findings above carry
  `suggested_command: null`, overriding the attention table for that
  checkout only, and never set the row's `suggested_command`, departing from
  DI:645 and DI:648-651: `project clean` reports that checkout only as
  `protected-default` and offers no action for it (`project:421-423`,
  `:539-540`, `:579-580`). Ignored files there yield no finding: it is never
  a removal target, and a `.venv` would otherwise warn on most projects.
- **OQ-21, `no-merge-target` severity** (lane addition; DI:551-558): error,
  exit 1. Without a merge target no worktree of the repository can be
  classified, so the row must not read as healthy, and other rows are
  unaffected. The departure from `acf0133`'s warning is recorded here.

OQ-22, a doctor health section (OV:269-273), is change 1's decision: none;
doctor changes only through the shared evidence. This change records only
that `acf0133`'s unmerged `project-doctor-repository-health` capability
(change `add-doctor-repository-health`) is superseded by `project-overview`.

## Corrections to the Packet

Citations stay at `da33d92`. The packet author, lane openRepoProject-3, is
revising the packet for these entries, the `suggestion_gate` and report-cap
departures (D-P, D-V) and change 1's R1 baseline change; until that revision
merges, these corrections bind this change and the spec phase (OQ-3):

- **Stale baseline sentences.** DI:28 (and BA:30) say `origin/main` "is now
  `ca4c615`", and OV:163 and HO:200 that it "has since advanced to
  `ca4c615`"; PR #7's squash `da33d92` superseded it, and HO:365-366 and
  HO:377-380 describe PR #7 as opened from `506a66b` and "open for review".
  DI:33-35 (and BA:39-42) name `5fc2b51`, `1789ad9` and `bb91a49` as the
  `cleanup` branch's behaviour commits and omit `acf0133`, `80fdef3` and
  `09af8c8`; OV:176-178 lists `acf0133` and `09af8c8` but also omits
  `80fdef3`. `acf0133` and `80fdef3` are the pair this change absorbs.
- **A failed status probe on the merge-target branch.** DI:255-262 has such
  a probe yield `inspection-error` "from the ladder", and DI:675-678 counts
  it toward the repository gate, but the ladder tests the merge-target branch
  after presence and before cleanliness (`project:418-426`), so there it
  would yield `protected-default`. DI:263 ("Both rows set directly"),
  DI:607-609 (a null `dirty` "is passed through, so the ladder yields its
  own `inspection-error`") and DI:1387-1388 state the same wrong mechanism.
  Change 1's R1 sets such a row to `inspection-error` directly, on that
  branch too, so DI:255-262 stands with "set directly" for "from the
  ladder", and DI:675-678, BA:643-644 and BA:908-910 hold once change 1
  lands; the overview follows (OQ-20).
- **Process groups on Python 3.10.** DI:457-458 (and BA:397-398) start
  children with `Popen(..., process_group=0)`, added in Python 3.11, while
  `README.md:17` requires Python 3.10 or newer and CI tests 3.10
  (`.github/workflows/tests.yml:10`). Both changes start each Git child with
  `start_new_session=True` instead, never `preexec_fn`; change 1 supplies
  that runner.
- **Isolation versus exit 2.** DI:530 maps every `Refused` from `manifest()`
  to a `manifest-invalid` row error with exit 1 (DI:1279-1286 shows the
  wrong-kind case); for an invalid encoding PRS:78-82 requires exit 2, and
  the MODIFIED requirement resolves it.

## Open Questions

None is open here. The one this proposal carried, `remote-gone` before a
merge proof, was ruled by Brett Heap on 2026-10-09: a local ancestry proof
outranks `remote-gone` for worktree rows, so the overview's `--all-safe`
suggestion now reaches a merged worktree whose upstream was deleted (Decisions,
departures), and council PA-1's advice not to ratify before he ruled is met.
Change 1's open question on squash-merged branches stays open there, and the
overview would inherit its ruling through [L].

## Questions Resolved by the Alignment Review

The alignment review ran on `babd1d5` (SA-1 to SA-18: 4 MISMATCH, 14 DRIFT;
QA-1 to QA-21: 9 MISMATCH, 12 GAP). 38 findings are applied and SA-3 is
superseded, some under the lane lead's rulings D-A to D-L; PR #12 carries the
reports and rulings. "Absorbing" and "Dependencies" name the subsections of
Decisions and Impact.

The lead's later rulings, from lane openRepoProject-3's reads of PRs #11
and #12, are applied too: D-M ([E], [L], [G]; the 60 s deadline in
requirement 3), D-J amended (unprobed rows; no Corrections entry), D-P and
D-V (`suggestion_gate`), each in What Changes, requirement 7, Dependencies
and Decisions; D-I relabelled (OQ-20); D-O and D-X (What Changes,
requirement 11, Decisions); D-Q (OQ-4, Impact); C1, C13, L5 and D-Z
(Corrections, requirement 8, Decisions); D-N and D-S (Dependencies); the
`remote-gone` question (Open Questions); and with the council D-S narrowed
(Rules), D-AB (Corrections), D-AE ([R], [P], requirement 3, OQ-9), D-AF
([E]) and lane 3's LOW items (Impact, Decisions, Corrections).

Lane 3's final delta read of PR #12 at `a8cef41` and the lead's rulings on
the phase 6 writer's six contradictions are applied as well: N-1 (What
Changes; Rules; requirement 10; Absorbing, OQ-20 and table), N-2 (requirement
3; Decisions, determinism), N-3 (requirement 7; Dependencies), N-4
(requirement 3; Dependencies; OQ-9), N-5 with P6-5 (What Changes;
requirement 7; Decisions, `suggestion_gate` and `unstarted-branch`), N-6 with
P6-6 (requirement 2; Decisions, layout findings; P6-6 overrides the earlier
confirmation that both layout findings warn), P6-1 (What Changes;
requirements 3 and 11), P6-2 (requirement 7), P6-3 (requirement 12), P6-4
(What Changes; requirement 8), and the two LOW items (Decisions,
`suggestion_gate`; What Changes, requirement 3 and Dependencies for the
manifest bound, which change 1 carries in [E]).

The reconciliation with change 1 at `0b3c33d` (design.md D12) applies the
lead's amended V2 and R-1 to R-9: V2 amended with R-1 (What Changes;
requirements 3, 7 and 12; Dependencies; Decisions, `suggestion_gate` and the
reflog gates), R-2 (What Changes; requirement 2; Dependencies; Decisions,
layout findings), R-3 (What Changes; requirements 7 and 8; Decisions,
`suggestion_gate`), R-4 (What Changes; requirement 3; Dependencies), R-5
(requirement 3; Dependencies; OQ-9), R-6 (requirement 6; Open Questions), R-7
(requirements 7 and 8), and R-8 and R-9, from two Codex findings on PRs #11 and
#12 (requirement 8; What Changes; Decisions, path validity flags).

The re-verification of `996a181` and lane 3's read of it are applied against
change 1's head at `4f2162b`: R-12's reflog anchor and one outcome rule
(requirements 3 and 7; Capabilities; Decisions, the reflog gates) and its
remedy texts, as R-14 amends the `unstarted-branch` one (requirement 7;
Capabilities); R-13 (b) (the three scenarios whose branches have a commit
of their own; requirement 5's claim limited to the rows `project clean`'s
report inspects; design Context; task 2.2); and R-14's M-A (Decisions,
escaping by general category), M-B (requirement 7; design Risks), M-C
(requirement 2; Capabilities; design D3 and D7) and LOW items (a scenario
for a common directory that is not valid UTF-8; the `limits` key `targets`,
requirement 8). R-15, lane 3's read of change 1 at `6792e06`, amends R-12,
and change 1 carries it at `4f2162b`: an entry whose old object is all zeros
is an anchor, written by any command, and never a movement, and the
`reflog-unavailable` remedy reads "the branch's reflog is missing, expired
or undecidable; review, then git worktree remove yourself" (requirement 7;
Capabilities; Decisions, the reflog gates; design D5 and D13). R-16, on
this change's addition at `fa9f0be` (a reflog read that times out leaves
its row unprobed), fits the `inspection-incomplete` remedy to both causes,
an `inspection-error` row and a row left unprobed (requirement 7's gate
table and requirement 12's scenario; Capabilities), and has the escaping
departure cite the packet's texts, not a numbered decision (Decisions).
R-18 gives the fetch-created branch an upstream by `git branch -u origin/feat
f1`, which writes no reflog entry, so its row reaches the reflog gate
(requirement 7's scenario and the proposal's scenario list; design D13),
records in design Risks that a reflog over 64 KiB fails closed even when it
records movement, takes change 1's movement wording, an entry whose old and
new objects are non-zero and differ (requirement 7; design D5; Decisions, the
reflog gates), and has design D5's reflog line format say the tab and the
message are present only when the command wrote one.
R-10's remedy wording is superseded by R-12, R-14 and R-15. Brett Heap's
ruling of 2026-10-09 on open question 1, relayed by lane openRepoProject-3
and given to lane openRepoProject-2 in his own words (Decisions, departures),
that a local ancestry proof outranks `remote-gone` for worktree rows, is
carried by change 1's [L] and mirrored here (Capabilities, requirement 6;
Impact, README; Decisions, departures; Open Questions; requirement 6 and its
scenario "A merged worktree whose upstream was deleted"; design D12 and Open
Questions; task 2.2), and it supersedes R-6.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| SA-1, QA-1 | MISMATCH | applied per D-A | Absorbing (OQ-20, table); Capabilities (requirement 10); Corrections |
| SA-2, QA-13 | MISMATCH, GAP | applied per D-B (requirement 11, not 8); QA-13 with D-O | What Changes; Capabilities; Dependencies |
| SA-3, QA-17 | MISMATCH, GAP | SA-3 superseded by D-J; QA-17 applied per D-J (amended: no Corrections entry) | Dependencies |
| SA-4, SA-5, SA-10 | MISMATCH, DRIFT | applied | Impact |
| SA-6, QA-6 | DRIFT, MISMATCH | applied per D-I (relabelled) | Absorbing (OQ-20); Decisions (departures) |
| SA-7, QA-20 | DRIFT, GAP | applied; QA-20 completed by C1 | Corrections |
| SA-8 | DRIFT | applied per D-G | Dependencies; Impact; Corrections |
| SA-9, SA-13 | DRIFT | applied | Decisions (suggestion display string; OQ-7) |
| SA-11 | DRIFT | applied | Capabilities (Modified); Corrections |
| SA-12, QA-7 | DRIFT, MISMATCH | applied per D-H | Decisions (preamble); Absorbing (OQ-22 record); Out of Scope |
| SA-14, SA-16, SA-17, QA-21 | DRIFT, GAP | applied | Absorbing (SA-16: OQ-19) |
| SA-15, QA-8 | DRIFT, MISMATCH | applied | Capabilities (New) |
| SA-18 | DRIFT | applied per D-K | Status; Impact; Decisions; Corrections; Open Questions; layout |
| QA-2, QA-3, QA-11, QA-12 | MISMATCH, GAP | applied; QA-3's `inspection-error-default` row per D-A | Absorbing (table) |
| QA-4, QA-15 | MISMATCH, GAP | applied | What Changes (QA-4); Capabilities (requirement 3) |
| QA-5 | MISMATCH | applied, consistent with D-J (amended), D-I and D-P | What Changes |
| QA-9, QA-14 | MISMATCH, GAP | applied; QA-14 with C13 | Capabilities (requirement 8) |
| QA-10 | GAP | applied; status cells follow `project:679-681` | Absorbing (prose, table) |
| QA-16 | GAP | applied, with D-M | Decisions (OQ-9) |
| QA-18 | GAP | applied per D-E | What Changes |
| QA-19 | GAP | applied; its first-match order superseded by council AE-1 (V1) | What Changes; Absorbing (OQ-20) |

### Council Verdicts

The council (PA product advocate, SA systems architect, AE adversary
engineer) read `6204234`: V1 to V12 are applied here, N1 to N4 are in
`clarifications.md`, none was dismissed, and X1 and X2 go to change 1.

| Concern | Severity | Verdict | Section changed |
| --- | --- | --- | --- |
| PA-1 `remote-gone` advice leads nowhere | HIGH | VALID, V11 (interim wording; ratification timing is Brett's); superseded by Brett Heap's ruling of 2026-10-09 | Open Questions; Impact |
| PA-2 no human-output requirement | HIGH | VALID, V3 | What Changes; Capabilities (requirement 12) |
| PA-3 gate codes without remedies | MEDIUM | VALID, V4 | What Changes; Capabilities (requirement 7); Decisions (departures) |
| PA-4 no roots, stale evidence, one project | MEDIUM | VALID, V10 (freshness through V3) | Capabilities (requirements 1, 12); Impact (README) |
| SA-1 scheduler control loop | HIGH | NOTED, N1 | `clarifications.md` |
| SA-2 runner must multiplex | MEDIUM-HIGH | VALID, V12; constraint routed to change 1 (X1) | Dependencies |
| SA-3 determinism too broad | MEDIUM-HIGH | VALID, V6, one item with AE-5 | Capabilities (requirement 3); Decisions (departures) |
| SA-4 unbounded costs | MEDIUM | VALID, V8 (bounds); NOTED, N2 (workers) | Capabilities (requirement 3); Decisions (OQ-4); Impact (README) |
| SA identity residual | LOW | VALID, V9 | Capabilities (requirement 2) |
| AE-1 default branch reads healthy | HIGH | VALID, V1, superseding QA-19's first match; NOTED, N4 | What Changes; Capabilities (requirement 10); Absorbing (OQ-19, OQ-20, table); Decisions (departures) |
| AE-2 gitfile repositories, missing main worktree | MEDIUM-HIGH | VALID, V2; NOTED, N3; change 1 part routed (X2) | What Changes; Capabilities (requirement 2); Dependencies; Decisions (departures) |
| AE-3 unbounded filesystem calls | MEDIUM | VALID, V7 | What Changes; Capabilities (requirements 3, 11) |
| AE-4 predictable `target-cap` refusal | MEDIUM-LOW | VALID, V5, amended per change 1 council V5 | Capabilities (requirement 7); Dependencies; Decisions (departures) |
| AE-5 determinism versus cuts | LOW | VALID, V6, with SA-3 | Capabilities (requirement 3) |
