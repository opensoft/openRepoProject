Lane: openRepoProject-2

# Proposal: add-project-overview

Status: ratified by Brett Heap on 2026-10-09, in his words to lane
openRepoProject-2, "ratify, merge #11 and run the runbook". It lands by
squash-merge of PR #12 after PR #11 (`add-project-clean-all-safe`), and the
Speckit handoff `005-project-overview` follows after feature 004 merges;
amendment A1 (PR #34) is drafted and not ratified, and lands only on Brett
Heap's word. The change was
revised after the alignment review, the lead's later rulings, the council and
the packet author's final delta read (resolutions on PR #12 and in "Questions
Resolved by the Alignment Review"; noted constraints in `clarifications.md`).
Like `add-project-clean-all-safe`, it adds "Decisions Taken by This Proposal",
"Corrections to the Packet" and "Open Questions" to the house sections.

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
  index gates and its `operation-in-progress` and `worktree-only-commits`
  gates. Never `--apply` or `--yes`, never a bare name (DI:661-702,
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
     its row recorded `probe-timeout`; SHALL pin
     `-c protocol.allow=never -c protocol.file.allow=never -c protocol.ssh.allow=never -c protocol.git.allow=never -c protocol.http.allow=never -c protocol.https.allow=never -c protocol.ext.allow=never`
     on every Git child beside [E]'s pins, Git 2.43 having no
     `GIT_NO_LAZY_FETCH`, so that a lazy fetch in a partial clone fails
     locally and never reaches the network (R-23), the per-protocol pins
     sitting beside `protocol.allow` because it is only the default policy,
     which a per-protocol `allow=always` in a config file or
     `GIT_ALLOW_PROTOCOL` in the caller's environment would override, so that
     `GIT_ALLOW_PROTOCOL` is among the names of [E]'s list that its scrub
     removes (R-25); SHALL run every filesystem call, root
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
     row (`inspection-incomplete`); only the index gates, then
     `operation-in-progress` and `worktree-only-commits`, stay residual
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
     `git-unavailable`, `relative-config-path`, `refused`, `os-error` or
     `internal-error`, and an argument error prints argparse's usage on
     standard error and no JSON.
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
- **`.github/workflows/tests.yml`** (Amendment A1, Brett Heap's answer Q3 B):
  feature 004's Git 2.36 floor job, `git-floor`, which builds Git 2.36 and
  runs the `clean`, `status` and `doctor` tests with it first on `PATH`, also
  runs a small set of the overview's tests, selected by one more `-k` prefix:
  the version check accepting Git 2.36, and one end-to-end run over a fixture
  with linked worktrees, merge targets and a gated suggestion.
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
  probes memoized per `common_dir` and the `extensions.worktreeConfig` read
  beside them, the combined status probe per worktree row
  and its record bounds, NUL-delimited parsing and path escaping, the child
  environment and pins (R-23 adds `-c protocol.allow=never`, and R-25 adds
  the six per-protocol `allow=never` pins and `GIT_ALLOW_PROTOCOL` in the
  scrub's list, there and in
  requirement 3), the 1 MiB manifest read, over-cap judged from the file's size
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
  `project-command`, among them [L]'s keeping of the ladder's names and
  order with one ancestry exception (a row whose upstream's remote-tracking
  ref is gone is tested for local ancestry before the `remote-gone` rung),
  the deleted-upstream `remote-gone` change and Git-first resolution of
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
  review re-aligns this proposal before the merge that ratifies it.
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

Each is a proposal decision, ratified with the merge of PR #12; the departures
from packet decisions are ratified as recorded. OQ numbers are this lane's
list for both changes: OQ-1 to OQ-3, OQ-20 to OQ-22 and OQ-29 are lane
additions; OQ-23 and OQ-24 are departures from packet decisions
(BA:1241-1245; BA:949-953 with HO:210) and OQ-28 a packet open decision
(DI:599-600); the others number the packet's consolidated open decisions
(OV:311-359; HO:317-353). OQ-10 to OQ-16, OQ-22 to OQ-24, OQ-28, OQ-29 and
the batch half of OQ-25 are change 1's. OQ-19 to OQ-21, and the one record
OQ-22 leaves here, are in the absorption subsection below.

Packet open decisions taken, each citing the packet text that leaves it open:

- **OQ-4, measured costs** (OV:314-319; DI:179-180, DI:189-190,
  DI:227-228): the governance `tasks.md` records the warm and cold-cache
  measurement of 2026-10-09, run on a Linux filesystem and never on a Windows
  drive mounted into WSL2, and the caps stand as measured: the 32-root,
  4,096-entry, 128-candidate and 512-row caps take 48.3 s of the 60 s
  deadline at their worst case. This workstation's default root holds 219
  candidates, so a default-root run here is incomplete by design, with a
  `scan-limit` error on `candidates` and 91 omitted, and no cap moves for it.
  Git 2.43 has no `GIT_NO_LAZY_FETCH`, so a read-only probe in a partial clone
  could fetch from the network, and R-23 pins `-c protocol.allow=never` on
  every Git child, with R-25's six per-protocol `allow=never` pins beside it
  and `GIT_ALLOW_PROTOCOL` in [E]'s scrub (requirement 3; design D13).
- **OQ-6, concurrency** (OV:320-327): four children across distinct
  repositories. If design rejects concurrency, the packet's serial fallback
  of 32 candidates and 128 worktree rows applies (DI:1465-1471).
- **OQ-7, a per-repository row cap** (OV:328-331): none. A repository with
  more than about 355 worktree rows ends at the deadline, visibly
  incomplete, if children cost the 150 ms margin rate; OQ-4's measurement
  kept it: one repository's children fit about 426 rows at 10,000 index
  entries (284 with the margin) and about 75 at 100,000, and a repository
  past that ends incomplete (DI:219-223, DI:1473-1476).
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
  candidates and 512 worktree rows, confirmed by OQ-4's measurement. The
  record bounds (64 ignored, 4,096 records, 8 samples) are [E]'s shared
  values.
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
  Amendment A1 (proposed, not ratified): after the index gates,
  `operation-in-progress` and `worktree-only-commits` are further exclusions
  that only the batch applies (section "Amendment A1" below); the words above
  are this entry's as ratified.
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

Decisions, each ratified with the merge of PR #12:

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

None is open here but one point that amendment A1 leaves open, M1 (section
"Amendment A1" below). The one this proposal carried, `remote-gone` before a
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

R-23, from the OQ-4 measurement (task 2.1, 2026-10-09), pins
`-c protocol.allow=never` on every Git child beside [E]'s pins: Git 2.43 has
no `GIT_NO_LAZY_FETCH`, so a read-only probe in a partial clone could
otherwise fetch from the network, and with the pin the lazy fetch fails
locally and the failed probe is recorded `probe-failed`. Change 1's [E]
carries the same pin (requirement 3; Dependencies; Decisions, OQ-4; design
D13 and Risks; task 2.1). The same measurement confirmed the caps and found
this workstation's default root, at 219 candidates, incomplete by design
(Decisions, OQ-4).

R-25, a gap found in change 1's application of R-23 at `8aad1e8`, completes
the pin: `protocol.allow` is only the default policy, so a per-protocol
`protocol.<name>.allow=always` in a config file or `GIT_ALLOW_PROTOCOL` in
the caller's environment would still allow the fetch. Every Git child also
pins `-c protocol.file.allow=never -c protocol.ssh.allow=never -c protocol.git.allow=never -c protocol.http.allow=never -c protocol.https.allow=never -c protocol.ext.allow=never` beside `-c protocol.allow=never`
(command-line `-c` outranks every config file), and `GIT_ALLOW_PROTOCOL` joins
the fixed scrub that [E] applies to the child environment, which then removed
seventeen names; the overview carries the pins and the scrub by citation of
[E] plus the literal list. The residual that a remote-helper protocol of
another name, with its own `allow=always` in the repository's config, could
still fetch is accepted: the case is rare, and the probe would then succeed
rather than fail, so no unsafe removal follows (requirement 3; Dependencies;
Decisions, OQ-4; design D13 and Risks; task 2.1).

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

## Amendment A1: Brett Heap's answers to feature 005's clarify questions (2026-10-21)

Status: A1 drafted; not ratified; it lands only on Brett Heap's word. It is
draft PR #34, https://github.com/opensoft/openRepoProject/pull/34.

A1, `amend-project-overview-clarify-answers`, is lane openRepoProject-4's
amendment of this change in place, under its governing issue
opensoft/openRepoProject#10, in the form in which draft PR #19 amends
`add-project-clean-all-safe`. Until Brett Heap's word ratifies it, the
ratified text is this change as PR #12 landed it (`961c405`), and the text A1
amends is its draft.

Task 1.7 records A1's ratification and holds feature 005's plan until it, a
gate beyond the words of Q2 A, which waits for feature 004's merge and Brett
Heap's word after it. The gate is declared here as the cautious direction: it
matches spec 005's interim rule that nothing is planned or built from the
answers A1 carries until A1 is ratified.

Brett Heap's words, in lane openRepoProject-4's session at about
2026-10-21T10:31Z, answering the seventeen clarify questions of feature 005
(`specs/005-project-overview/clarify-questions.md` at `acd8cef`, its question
block unchanged at `c54d393`): "yes, recommended for Q1-Q17". The answers are
Q1 A, Q2 A, Q3 B, Q4 D, Q5 A, Q6 A,
Q7 A, Q8 D, Q9 B, Q10 A, Q11 A, Q12 A, Q13 A, Q14 A, Q15 A, Q16 B and Q17 A,
each the recommended option, and spec 005 encodes them as its Clarifications
C-55 to C-71. Lane openRepoProject-4 recorded them as a RULED line at
10:33:09Z:
https://github.com/opensoft/brett-wip/blob/bd597b390d918c3f832e787c97844e3a2ce3ccea/lanes/log/openRepoProject-4.md#L115

Citations in this section add to those of Input above: `POD:N` is line N of
`specs/project-overview/spec.md`, and `design.md:N`, `clarifications.md:N`
and `proposal.md:N` are lines of this change's files, all at `961c405`,
before A1, as spec 005 cites them; `CMD:N` is line N of change 1's
`specs/project-command/spec.md` at the same commit.

Each carried answer, with what it amends and where:

- **Q3 B, an amendment, carried in Impact as the option allows.** A small set
  of the overview's tests runs in feature 004's Git 2.36 floor job,
  `git-floor`, selected by one more `-k` prefix: the version check accepting
  Git 2.36, and one end-to-end run over a fixture with linked worktrees,
  merge targets and a gated suggestion. Amended: Impact, a new
  `.github/workflows/tests.yml` bullet after the tests bullet
  (proposal.md:441-449).
- **Q4 D, a recorded departure from Impact, on Brett Heap's word.** After
  feature 004 lands, feature 005 adds one sentence on the overview, that a
  suggestion is advice to review and that applying it needs the person's
  word, to the `AGENTS.md` section that feature 004's task T123 adds,
  "Cleaning up worktrees for a person", following that section's title and
  wording; it is recorded as feature 004 records its own departures (its lead
  ruling R-32). If Brett Heap declines feature 004's T123 departure, the
  question's option C applies instead: a separate small OpenSpec change,
  after feature 005, carries agent guidance on the overview and the batch
  apply. Amended: no text; Impact (proposal.md:415-465) names no `AGENTS.md`
  change and stays so.
- **Q6 A, an amendment.** Only the `deadline-exceeded` scan error that counts
  the candidates not started carries `limit` and `omitted`, `limit` being
  `"invocation_timeout_seconds"`, the `budget` key, and `omitted` the
  candidates not started; every other `deadline-exceeded` error, row or scan,
  carries neither; and a row-level `scan-limit` error carries `limit:
  "worktree_rows"` and `omitted` counting that repository's rows past the
  cap, exactness `exact`. Amended: requirement 3 (POD:180-181, :233-234) and
  requirement 8's error object (POD:646-648). For the one deadline error it
  departs from the packet's `limit`, "a key of `limits`" (DI:824-825).
- **Q7 A, an amendment.** When the working directory's realpath cannot be
  established, one scan error records it (`os-error` or `probe-timeout`, with
  feature 004's fixed text and OPERATION `realpath`, its `path` the `PWD`
  value when that is set and absolute, else omitted, first among the scan
  errors), every `current` is null, and each row the ladder would classify
  `merged-removable` or `merged-current` is `inspection-error` instead, so
  that `inspection-incomplete` withholds `--all-safe`. Amended: requirement
  5, a new paragraph after its equality clause (after POD:386); design D6's
  scan-error order (design.md:410-412) and D8's realpath task
  (design.md:470-471). Its raw `PWD` path departs from DI:842-843's rule that
  paths are canonical, and from DI:778's null rule for `current`, which is
  null there only when `present` is.
- **Q8 D, an amendment.** Every row and scan error's message is the fixed
  text of its code, naming no path, the path going in `path`; a child's
  standard error is drained and capped, and never shown; and names, branch
  names, admin ids and every other string taken from the filesystem, a
  manifest or Git follow [P]'s path rule, with no new field. Git's own reason
  is then not shown: the person re-runs the Git command to see it. Amended:
  requirement 4 (POD:337-338, and a table of fixed texts after POD:347);
  requirement 8 (POD:675); design D1 (design.md:99-101); clarifications N1
  (clarifications.md:35-36 and :46-47). The texts for `os-error`,
  `probe-failed` and `probe-timeout` are feature 004's (its
  `contracts/project-clean.md:300-302` at `b0243e5`, lead ruling R-45);
  `deadline-exceeded` reads `OPERATION stopped at the invocation deadline`,
  the overview's own term, where that contract's :303 reads `work deadline`;
  the texts for `manifest-invalid`, `refused`, `undecodable-output`,
  `internal-error`, `scan-limit` and `root-unreadable`, and the OPERATION
  values `stat`, `scandir` and `collection`, are A1's own, drafted for Brett
  Heap's review. Re-checked at feature 004's `e256b59`, where the same rows
  sit at `contracts/project-clean.md:430-433` with the texts unchanged; the
  `b0243e5` pin stays (R-45). It departs from the packet's DI:544-545 ("for a
  failed probe, the first line of Git's standard error"). A fill, declared for
  Brett Heap's review (lane openRepoProject-3's W7-M1): since the path leaves
  the message, the human report prints an error's `path`, when it carries
  one, by [P]'s rules, a scan error as `Incomplete: <path>: <message>
  (<code>).`, as the packet's DI:94 names the root, and a row error with its
  `path` on the next line, indented to the message column, as a worktree's
  finding shows its worktree path; an error with no `path` prints as before.
  Amended for the fill: design D10 (design.md:519-520 and :526-527, and a
  paragraph after :533) and requirement 12 (POD:812-813).
- **Q9 B, an amendment of this change; its change-1 half rides in PR #19.**
  The read-only wording claims for the overview's Git children only what the
  pins and the scrub prove, the clean and process filters and the
  configuration files being recorded residuals beside the remote-helper one;
  and "seventeen names" becomes a citation of [E]'s list, which PR #19 amends
  at `423a532` to thirty-one names, with `GIT_TRACE2`, `GIT_TRACE2_EVENT` and
  `GIT_TRACE2_PERF` at `0` on every Git child, both reaching the overview by
  that citation. Amended: requirement 3 (POD:212-215); requirement 9 (after
  POD:717); design D13 (design.md:661) and Risks (after design.md:726);
  proposal.md:231-232 and :477, and :1000, whose record of R-25 now reads in
  the past tense. If feature 004 merges before PR #19 is ratified, it builds
  the narrower scrub and the wider one follows as a change-1 amendment; the
  citation holds either way. For the overview's Git children, the new
  sentence after POD:717 narrows the packet's DI:307-308, "it never fetches,
  pulls, resets, bootstraps, runs validators, writes files, or contacts the
  network", as this change already accepted the remote-helper residual
  without correcting the packet (design Risks, design.md:721-726; R-25).
- **Q11 A, an amendment.** A candidate other than a family holder whose
  identity probe reports a toplevel that is a proper ancestor of the
  candidate is a `refused` error row, its `path` the candidate's `.git`, and
  creates or joins no repository row; a family holder whose probe reports
  another toplevel keeps null `repository`, `merge_target`, `git` and
  `worktrees` and no error, as DI:284-287 has it; and a toplevel that Git
  reports for a layout it accepts, such as a `core.worktree` naming another
  directory, is unaffected. Amended: requirement 2, a new paragraph after
  POD:87; the `refused` row of requirement 4's new table.
- **Q12 A, an amendment.** The whole document or report is rendered before
  its first byte is written, as UTF-8 whatever the locale, the JSON document
  with ASCII escapes as feature 004 writes its own (its lead ruling R-38); a
  failed write to standard output ends the run with exit 2, no traceback and
  no retry, nothing more on standard output and one best-effort line on
  standard error, the one exit 2 under `--json` besides an argument error
  that prints no error object, and so no code (lane openRepoProject-2's
  ruling R-55 gives `internal-error` there, which is not kept); a recorded
  signal decides the status over it. Amended: requirement 8 (POD:675-676, and
  a new paragraph after POD:679). It departs from the packet's DI:1086-1089.
- **Q13 A, an amendment.** A root whose canonicalisation is cut takes as its
  `path` the given path made absolute but not resolved, sorts by those bytes
  among the canonical paths, is never deduplicated, and counts toward the
  32-root cap. Amended: requirement 1, a new sentence after POD:16, through
  which POD:217-222, :303-306, :610-611 and :622-624 read. The unresolved
  `path` departs from DI:842-843, whose exceptions to canonical paths,
  `ignored_samples` and an absent default root, are three with this one and
  four with Q7 A's.
- **Q15 A, an amendment.** "Print no result document" becomes "start no
  result document once the signal is read, and stop one that is being
  written"; the part of a result that a stopped write leaves is a recorded
  residual, marked as no result by the exit status 130, 143 or 129; a signal
  recorded before the run exits decides its status, also over the exit 2 of
  a write that fails after it; and the raising span around the write is
  entered before its first byte, so that a signal recorded while rendering
  prints nothing, and output not yet written is discarded, never flushed at
  exit. Amended: requirement 11 (POD:778-779, and new sentences after
  POD:781); design D1 (design.md:110-111, in the same words, as lead decision
  L6 has it; a new paragraph for the raising span; and the "Recorded"
  paragraph, design.md:121-122). It departs from the packet's DI:1094-1096.
- **Q16 B, an amendment.** Each Git child starts with SIGINT, SIGTERM and
  SIGHUP unblocked, under handlers that only record the signal, which keeps a
  termination pass from missing a child; a child started with them blocked
  inherits the mask, survives SIGTERM to its group and needs SIGKILL at every
  stop (runtime cross-check X-7). Amended: design D1's spawning paragraph
  (design.md:115-119); clarifications N1 (clarifications.md:42-44, where "or
  raise a `BaseException` subclass" is struck, and :45-47).
- **Q17 A, a recorded departure, in one order only.** Feature 005 leaves the
  overview parts of #24 and #25 to their own features in every order. If
  #24's realization merges first, a worktree whose only ignored files are
  Python bytecode caches is `ignored-local-files` in the overview and
  `merged-removable` in `project clean`, a departure on Brett Heap's word from
  requirement 5's equality clause (POD:381-386, on DI:620-624) until #24's
  overview block is archived, after which that block records it as a lasting
  exception. Amended: no text.

Not carried, since each changes only spec 005 and builds this change as
ratified: Q1 A, Q2 A, Q5 A, Q10 A and Q14 A.

Four items of A1's own follow from change 1's amendments in draft PR #19,
not from Q1-Q17. Their basis is Brett Heap's ruling, in lane
openRepoProject-3's session on 2026-10-21, "yes to all six recommendations,
LQ-10 to LQ-15", which that lane recorded as a NOTED line at 12:33:41Z:
https://github.com/opensoft/brett-wip/blob/5276f65d18fcb46ba3fcc5758a09941d15a36e21/lanes/log/openRepoProject-3.md#L89
and, for LQ-15, his words to lane openRepoProject-2, "LQ-15: yes, refuse
relative HOME like #29" (its ruling R-102 (a)), as PR #19 records them. That
ruling is about change 1: the lead's form of LQ-15 (lane openRepoProject-2's
ruling R-102 (c) 3) names `clean`, `status`, `doctor` and `update`, and what
reaches the overview reaches it through [E] and [G], which this change cites;
beyond that, each item is A1's own proposal, put to Brett Heap here. Each
follows PR #19's text at the commits its heading names, a draft pending its
own ratification; PR #19's tip is `f0bf538`, whose round (e) keeps the two
gates' outcome and names the `worktree-only-commits` gate's unfinished read as
its exception to the branch reflog's split (its
`specs/project-clean/spec.md:736-737` there); its rulings R-124 (`2b86a5f`,
amended at `9267303` by PR #19's round (d)), R-125 (`93f3194`) and R-126
(`1ebdd90`) are taken in below. Each lands only with or after PR #19's
ratification of the commits it follows, and is re-aligned before A1 is
ratified if one of those commits changes first, and, if A1 is ratified first,
is re-aligned for Brett Heap's review before PR #34 merges. So PR #34 does not
merge before that ratification; if Brett Heap wants it to land sooner, the
four items move to a later amendment of this change, and A1 lands without
them. Each item is declared here for Brett Heap's review:

- **`relative-config-path` (LQ-15; PR #19 at `cc000ea` and `9fb22fa`), a
  declared item.** Once its arguments are parsed, and before any Git child
  starts, the version check included, the overview refuses with
  `relative-config-path` and exit 2 when `HOME` or `XDG_CONFIG_HOME` is set
  to a non-empty value whose first byte is not `/`, tested on the raw bytes
  and for each variable whether or not Git would read a file through it, not
  following Git's order of precedence (C-44's other half, which PR #19 adds
  at `9fb22fa`), its message naming each variable that fails the test, never
  its value, as `project clean`'s refusal does; under `--json` it prints only
  the error object with that code. The order is PR #19's at `9fb22fa`:
  argument errors, then this refusal, then the version check. A separate
  sentence applies the same test to `GIT_CONFIG_GLOBAL` and
  `GIT_CONFIG_SYSTEM`, the lead's extension in PR #19; if Brett Heap strikes
  that extension, A1's sentence is struck with PR #19's sites (its design
  D11's list at `9fb22fa`), and no other text here tests the two variables:
  the scenario's precedence AND, which names an absolute `GIT_CONFIG_GLOBAL`,
  stays, as PR #19's own does by the sentence after that list. Amended:
  requirement 8's exit-2 code list (POD:677-678); requirement 11's exit rule
  (POD:765-768), a new paragraph after POD:768, and the scenario "A relative
  configuration path" after "Git unavailable" (POD:790), with its
  precedence AND, 62 scenarios in all; design D13's scenario map
  (design.md:697); the summary of requirement 8 in Capabilities
  (proposal.md:334-335); and task 1.4, which records the 62. PR #19 at
  `9fb22fa` leaves the overview's code and exit status under this test to
  this change. The code departs from the packet's closed list of exit-2 codes
  (DI:1086-1089). If Brett Heap strikes the code, the fallback is `refused`
  with exit 2, which departs from nothing.
- **`operation-in-progress` and `worktree-only-commits` (LQ-14, PR #19 at
  `43f7107` and `1ebdd90`; LQ-13, at `93de4bb`; both at `2b86a5f` and
  `9267303`), a declared proposal.** PR #19 adds them as [G]'s last two gates,
  in that order after `hidden-local-state`: an operation marker of [G]'s list
  at `1ebdd90` (its `specs/project-clean/spec.md:650-659`, after R-126) in the
  worktree's administrative directory, read by one listing and no Git child;
  and a commit that only the worktree's HEAD reflog or a ref under its
  `refs/worktree/` holds, read from `logs/HEAD` and one `rev-list` child. A1
  makes both further exclusions that only the batch applies, beside the index
  gates: the overview evaluates neither, makes no listing, `logs/HEAD` read or
  `rev-list` child for them, and keeps its `--all-safe` suggestion, which
  `project clean`'s batch then excludes itself. That clause follows the one
  outcome rule of each gate that R-124 settles at `2b86a5f`, as PR #19's round
  (d) amends it at `9267303` (its `specs/project-clean/spec.md:719-722` and
  :741-746 there; lane openRepoProject-3's W32 L1 and lane openRepoProject-2's
  R-208, with lane openRepoProject-3's W39 LOW-3 and LOW-4 on these words),
  pending PR #19's ratification: the overview still evaluates neither gate,
  and the batch decides each itself. It excludes the worktree on a decided
  result: a marker present; a `rev-list` child that exits 0 and prints
  anything; a `logs/HEAD` read to its 64 KiB bound or holding a line that
  cannot be parsed. An error on the listing, any other error on the read (a
  missing or empty `logs/HEAD` giving no candidate), and a child that cannot
  be started or exits nonzero make the worktree `inspection-error`; a child
  stopped at its 5 s budget, or a listing or read not finished within the
  filesystem budget, the deadline not being the limit, records `probe-timeout`
  and makes the worktree `inspection-error`; the deadline's cut records
  `deadline-exceeded`; and each of these leaves the batch's plan incomplete.
  Amended: requirement 7 (POD:525-526) and design D5 (design.md:324-325), with
  the proposal's summaries of the batch's exclusions in What Changes
  (proposal.md:100-101) and in Capabilities, requirement 7
  (proposal.md:290-291), and design's in D5's `target-cap` item
  (design.md:346) and in Risks (design.md:732-733). The reflog-gates departure
  (proposal.md:704) keeps its ratified words, with an A1 note after it. The
  route departs from the packet's OV:110-113 and DI:690-692, which name
  `hidden-local-state` and `contains-submodule` as the only exclusions the
  batch applies beyond the overview's gates. The alternative, for Brett Heap:
  overview gate codes `operation-in-progress` and `worktree-only-commits`,
  evaluated from the same reads, each a new row in requirement 7's closed gate
  table, which withholds `--all-safe` for that worktree; the second costs one
  Git child per row that reaches it.
- **The redirected work tree (LQ-11, PR #19 at `addd346` and `93f3194`), a
  minimal amendment.** PR #19 adds to the shared evidence model one
  `extensions.worktreeConfig` read per common directory and, where that is
  taken as true, one `rev-parse --path-format=absolute --show-toplevel` in
  each linked row whose registration agrees, before its status probe, a
  different work tree making the registration disagree. The overview reaches
  both by citation, but this change's own probe counts are closed: the
  scenario "One probe set per repository" counts `probes.performed` exactly,
  and the `estimated` rule and design D6 list the repository-wide probes.
  Amended: requirement 3's `estimated` rule (POD:250-254) and that scenario
  (POD:129), whose fixture now states that the repository does not set
  `extensions.worktreeConfig` (POD:127); design D6 (design.md:390-392); and
  the shared evidence model as "Dependencies and Sequencing" lists it
  (proposal.md:472-473). The counts depart from the packet's DI:506-509 ("3
  more per distinct repository") and DI:1193-1201 ("plus three"). Amended
  also, where this change's text contradicts PR #19's two reads, at the sites
  spec 005 recorded at `b511bdb`: the collector table's `probe-failed` row
  (POD:333), so that the extension read's exit 1 with nothing printed on
  standard output or standard error, by which Git reports the value not set,
  reads as false with no error, as PR #19 has an unset value, while an exit 1
  with a warning, as for an unreadable `config`, stays a failure that counts
  as true, and so that the effective-work-tree read records no error where a
  probe that fails, as it does under `core.bare=true` (exit 128) and as a
  probe that cannot be spawned does, on the lane openRepoProject-4 lead's
  ruling, and output that is not exactly one line each make the row's
  registration disagree, as PR #19 has it at `addd346` and as POD:89-95
  classifies a disagreeing registration (lane openRepoProject-3's W17 L2, W20
  M2 and W25 L8); the second phase, which runs a linked row's
  effective-work-tree read before its status probe (POD:238-239 and a sentence
  after POD:246); and design D8, a task for the realpath of the toplevel that
  read reports (after design.md:463), with its outcomes, `ENOENT` or `ENOTDIR`
  making the registration disagree with no error and any other `OSError` or a
  missed wait leaving the check not completed, and its count (design.md:478).
  POD:248-254 and design D6, amended above, agree with both reads. The table's
  two exceptions depart from the packet's DI:535 ("A Git child exits nonzero |
  `probe-failed`"). R-125 at `93f3194` adds the administrative directory's
  `commondir` file to [E]'s two-way registration: it must name `<common_dir>`,
  read by the filesystem with no Git child as Git reads it; a missing one, or
  one naming another directory, makes the registration disagree, and a read of
  it that fails gives the row `inspection-error` (its scenario "A commondir
  that names another repository"). It reaches the overview through the shared
  evidence model, by the registration check that requirement 2 cites (POD:84),
  with no Git child and no task or count of its own. Two texts are amended for
  it. D8's per-row task names its reads and now names the `commondir` file
  (design.md:461-462). Requirement 2's closed case list (POD:89-95) gains,
  after its second case, a case for a registration check that cannot be
  completed: a registration read, the `commondir` read included, failing with
  an error that shows no disagreement, or the realpath of the toplevel that
  the effective-work-tree read reports failing other than with `ENOENT` or
  `ENOTDIR`, or that realpath or that read itself being cut, gives no status
  probe, the code that fits it and `inspection-error` set directly, as [E] at
  `93f3194` has a failed `commondir` read ("a read of it that fails SHALL give
  the row `inspection-error` and no probe", its
  `specs/project-command/spec.md:211-213`) and as D8's realpath task leaves
  the check not completed (lane openRepoProject-3's W25 M1, W29 L1 for the
  words, which are spec 005 FR-007's, and W34 LOW-1 for the cut, which is the
  realpath's and the work-tree read's only). Its disagreement case gains
  FR-007's tie-break: a `<path>/.git` that is missing (`ENOENT` or `ENOTDIR`)
  or not a regular file, or an administrative `gitdir` or `commondir` file
  that is missing (`ENOENT` or `ENOTDIR`), is a disagreement and not such an
  error, as [E] requires that `<path>/.git` "SHALL be a regular file", that
  the `gitdir` file "SHALL name `<path>/.git`" and that "A `commondir` file
  that is missing" makes the registration disagree (its :203-213, unchanged
  through `6f2cb54` and `a664799`). What a failed read of the `.git` or
  `gitdir` file gives, and that a missing or non-regular file decides as a
  disagreement before any read can fail, [E] does not state; they are A1's
  fill, in FR-007's words. Without the new case the list sent such a row to
  its last case, a status probe. The case departs from the packet's
  DI:251-261, whose table of the cases a registered path falls into has none
  for a check that cannot be completed. Spec 005 carries the parity.
- **The stat pins (LQ-10, PR #19 at `ea697ba`; its pointer at `93f3194`), a
  restatement.** PR #19 adds `-c core.trustctime=true -c
  core.checkStat=default` after `-c core.fsmonitor=false` on every status
  probe, and on its hidden-state probe and removal, because Git compares a
  file's ctime only while both settings keep these values, so that under a
  repository's `core.trustctime=false` or `core.checkStat=minimal` an edit
  that keeps a file's size and restores its mtime would read unchanged. The
  overview's status probe takes the four pins through [E], by citation; the
  overview runs no hidden-state probe and no removal. This change quoted [E]'s
  status pins as the two older ones, quotes that PR #19 at `93f3194` calls
  stale after LQ-10 and this change's to restate (its Dependencies and
  Sequencing). Amended: requirement 3's quote (POD:202-204) and design D13's
  (design.md:650-652), each now `-c core.untrackedCache=false -c
  core.fsmonitor=false -c core.trustctime=true -c core.checkStat=default` on a
  status probe. D13's fixture-rewrite item (design.md:664-665) keeps its
  words: it names the two pins that disarm a `core.fsmonitor` hook, which [E]
  still passes on every status probe. PR #19 at `93f3194` changes no pin; it
  adds a precondition to the scenario "An edit that keeps its size and
  restores its mtime" (lane openRepoProject-3's W9 L1). No packet line quotes
  the two older pins: the packet gives the status probe's argv with no `-c`
  pin (DI:396, DI:1181), so no departure is declared. PR #19 accepts in its
  design Risks, on Brett Heap's ruling LQ-10, that where ctimes or inodes
  change without an edit the probe is slower, never wrong, and a slow probe
  makes a plan incomplete, never unsafe; and that where the repository defines
  a clean filter, a ctime-only change under `core.trustctime=false` now runs
  that filter once per probe, where it ran none before, which widens the
  clean-filter residual that LQ-16 leaves open (requirement 9's sentence after
  POD:717, Q9 B above), a filter whose command is missing giving a false
  `dirty` or a failed probe, both of which fail closed (lane
  openRepoProject-3's W25 L10).

Q15 A and Q16 B together: the handlers only record the signal wherever a
child can run, and Q15 A's raising span, feature 004's `raising_signals` (its
lead ruling R-47), is entered only after every child is reaped or abandoned,
so that no child runs under its raising handlers (design D1).

Requirement 2 and design D8 together (lane openRepoProject-3's W29 O2):
requirement 2's second case now also takes an `lstat` whose filesystem task
reaches its 5 s limit or that the deadline ends or prevents, with the code
that fits it, `os-error`, `probe-timeout` or `deadline-exceeded` (POD:330,
:334-335), as spec 005's FR-007 does. By its words the closed list sent a cut
`lstat` to its last case, a status probe, and only its closing sentence, that
no probe runs in a path the overview could not `lstat`, kept the probe from
running. Design D8 already gives the outcome: one task for the row's `lstat`
and registration reads (design.md:461-462), whose missed wait records
`probe-timeout` or `deadline-exceeded` and leaves every field it would have
established null (design.md:473-475). That task's cut, its `lstat` and its
registration reads together, is therefore the second case's, and the third
case's cut is that of the toplevel realpath and of the effective-work-tree
read only (lane openRepoProject-3's W34 LOW-1), as the packet has the row's
`lstat` and registration reads form one task with the same wait (DI:477-479).
Amended: requirement 2's second case (POD:90-92). It departs from no packet
line: DI:258's row, "`lstat` fails with any other `OSError`", does not exclude
a cut, and DI:477-480 and DI:1238-1242 give a row cut this way `probe-timeout`
or `deadline-exceeded`.

Open point, left to Brett Heap with no behaviour written (lead decision M1,
from lane openRepoProject-3's fidelity read of spec 005 at `c54d393`): Q7 A is
silent on parity with `project clean` run from the same working directory
when that directory's realpath cannot be established. Requirement 5's
equality clause (POD:381-386) stays as ratified, while at `2cf34d3` feature
004 gives every present row `inspection-error` there (its
`project:2960-2962`, :2887-2888 and :2081), wider than the two classes Q7 A
converts, so that rows such as a `dirty` one would differ.

Points for Brett Heap's review, beside the answers themselves: Q8 D's six
drafted texts and its OPERATION values, with the fill that prints an error's
`path` in the human report (lane openRepoProject-3's W7-M1); PR #19's new
refusal code, `relative-config-path`, and its two new gates,
`operation-in-progress` and `worktree-only-commits`, reaching the overview,
with the route and the alternative each takes above; LQ-11's counted reads and
its conflict sites: the collector table's two exceptions to `probe-failed`,
the second phase's effective-work-tree read, design D8's toplevel realpath
task with its outcomes and the `commondir` read in its per-row task, and
requirement 2's case for a check that cannot be completed; LQ-10's four stat
pins, restated where this change quoted two; the merge order, under which PR
#34 does not merge before PR #19's ratification of the commits its four LQ
items follow, unless Brett Heap moves those items to a later amendment; and
the open point M1. All of A1 stays drafted, not ratified.

The changes that carry this change's requirements in MODIFIED blocks are to
re-align them to A1's text: lane openRepoProject-5's
`add-project-clean-cache-disposal` (#24, PR #27) for requirement 5, and
`add-project-overview-remote-merge-status`
(#25, PR #29) for requirements 3, 8 and 9 and, through its task 2.3, for the
spawning sentence of its design D7. Spec 005 folded its FR-011, FR-022,
FR-039, FR-044, SC-009 and SC-011 ahead of A1, and re-reads them against A1's
text once A1 is ratified.
