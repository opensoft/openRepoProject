Lane: openRepoProject-2

# Proposal: add-project-overview

Status: draft, revised after the alignment review and the lead's later
rulings (resolutions on PR #12 and in "Questions Resolved by the Alignment
Review"), awaiting Brett Heap's ratification; nothing here is ratified. Like
`add-project-clean-all-safe`, it adds "Decisions Taken by This Proposal",
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
`project:421` is the executable.

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
- **Every bound is reported.** The 32-root, 128-candidate and
  512-worktree-row caps apply after canonical sorting; the 4,096-entry cap
  cuts a root's listing in directory order and reports `omitted` with
  exactness `unknown` (DI:117-121, DI:153-228). Dropped work is reported as
  `omitted: {count, exactness}`, and at most four Git children run at once,
  across distinct repositories (DI:429-449). A cap, timeout or deadline makes
  the result `incomplete` and exits 1 (DI:222-225).
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
  a `merged-removable` worktree that passes change 1's four per-worktree
  gates (main-worktree, unsupported-path-bytes, registration-mismatch,
  locked-worktree) in a repository change 1 would not refuse as
  `inspection-incomplete` or `inspect-cap` and with no row the overview left
  unprobed; otherwise the read-only `project clean <root>` where the
  attention table names it, except on the merge-target checkout (OQ-20); and
  no suggestion for a code the table marks none, a null `repository.root` or
  a root that is not valid UTF-8. A finding names the gate that withheld or
  limited its suggestion in `suggestion_gate`. The batch may still exclude a
  suggested worktree through its index gates. Never `--apply` or `--yes`,
  never a bare name (DI:661-702, DI:847-886).
- **A versioned JSON envelope.** `--json` prints one `schema_version: 1`
  document with exactly the envelope, row, worktree, finding and summary
  fields and types of DI:724-819, plus the finding field `suggestion_gate`.
- **Exits by completeness and severity.** 0 when complete with no `error`
  finding; 1 when incomplete, on an `error` finding, or on a `warning` under
  `--strict`; 2 for an invalid invocation, an exception outside the
  collector, or `git-too-old` or `git-unavailable` before any root is listed;
  130, 143 or 129 on SIGINT, SIGTERM or SIGHUP, after every child is
  terminated and reaped, with no result document and `Cancelled.` printed on
  a best-effort basis; a signal's status wins over 1 (DI:313-326,
  DI:1066-1098).
- **Default-branch health, absorbed from the closed PR #2.** A checkout
  classified `protected-default` gains a `dirty` preserve warning when
  dirty, and otherwise `diverged` or `unpushed` (preserve, warning) or
  `remote-ahead` (informational, info) from its ahead and behind counts,
  each with no suggested command (OQ-19, OQ-20).
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
- **Unknown is never healthy.** `null` means not established, and an error
  row's empty `findings` means none were computed (DI:830-833).
- **Incomplete is visible.** Every cap, timeout and deadline surfaces as
  `completeness: "incomplete"`, an error and exit 1 (DI:222-225).
- **Ordinary work is not trouble.** Housekeeping and informational findings
  stay distinct from warnings and errors (SY:308-309).
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
  `specs/project-overview/spec.md` with eleven ADDED requirements (proposed
  header, then proposed text). Where one relies on change 1, its spec text
  cites the canonical header by name, never "change 1's" prose:
  - [E] `Repository inspection requires Git 2.36 and shares one evidence model`
    (project-command), which names `overview` among its readers;
  - [L] `Clean classifies preservation and cleanup actions` (project-clean);
  - [G] `Clean previews and applies a batch of eligible worktree removals in one repository`
    and `Clean bounds its Git work and reports omitted work` (project-clean).
  1. `Overview discovers projects within configured roots only`: SHALL
     examine each root and its immediate entries only, by the marker table.
  2. `Overview groups worktrees by repository identity`: rows SHALL be keyed
     by `{root, common_dir, dev, ino}` from [E]'s identity probe; a family
     holder SHALL be one row.
  3. `Overview bounds its work and reports what it omitted`: SHALL bound the
     run by its own 60 s invocation deadline and each Git child by [E]'s
     per-child budget, apply the root, candidate and worktree-row caps after
     sorting and the entry cap in listing order, and report each dropped
     unit; SHALL schedule in two canonical phases so that the JSON, apart
     from timestamps and `budget.probe_concurrency`, does not depend on
     concurrency or completion order, and SHALL report
     `probes: {estimated, performed}` as DI:503-511 defines.
  4. `Overview isolates one candidate's failure`: a failure SHALL become that
     candidate's error row and SHALL NOT change any other row.
  5. `Overview reuses the cleanup classifier and merge target`: SHALL classify
     by [L]'s ladder over [E]'s evidence and report the merge target
     `{name, source, sha}`.
  6. `Overview reports findings by attention category`: severity SHALL decide
     the exit, and `--attention` SHALL change only the display.
  7. `Overview suggests only gated clean commands`: SHALL suggest argv naming
     `repository.root`, `--all-safe` only behind [G]'s four per-worktree
     gates and its `inspection-incomplete` and `inspect-cap` refusals and
     with no row left unprobed, and SHALL name the gate that withheld or
     limited a finding's suggestion in `suggestion_gate`.
  8. `Overview prints a versioned JSON envelope`: SHALL print one
     `schema_version: 1` envelope; a `--json` exit 2 other than an argument
     error prints `{"error", "code"}` with code `git-too-old`,
     `git-unavailable`, `refused`, `os-error` or `internal-error`, and an
     argument error prints argparse's usage on standard error and no JSON.
     SHALL emit every path, parsed as [E] parses it, exactly when valid
     UTF-8, else escaped with `path_valid_utf8: false`, SHALL print a path
     with control, bidirectional or format characters or undecodable bytes
     in `$'...'` form, and SHALL give a non-UTF-8 path an
     `unsupported-path-bytes` finding and no clean suggestion (scenarios
     DI:1338-1347, DI:1392-1408).
  9. `Overview is local and read-only`: SHALL make no network connection and
     no filesystem or Git mutation.
  10. `Overview reports default-branch health`: a merge-target checkout
      classified `protected-default` SHALL keep that classification and gain
      the OQ-19 and OQ-20 findings.
  11. `Overview exits by completeness and severity`: SHALL exit 0, 1, 2 or
      130 as DI:1070-1075 defines, and 143 or 129 on SIGTERM or SIGHUP;
      SHALL refuse Git older than 2.36 with `git-too-old`, and a missing or
      unusable `git` with `git-unavailable`, by [E]'s version check and with
      exit 2 before listing any root; on any of those signals SHALL
      terminate and reap every child, print no result document, print
      `Cancelled.` to standard error on a best-effort basis and exit with
      that signal's status, which wins over 1.

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

In sum: one new capability, `project-overview`, with 11 ADDED requirements,
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
  envelope, and that a suggestion is advice to review, not permission.
- **`tests/test_project.py`**: temporary fixtures only, network disabled,
  zero-mutation snapshots, covering the packet's 31 MVP scenarios
  (DI:1175-1446), the default-branch findings, the carve-out and a manifest
  row read without PyYAML. Where CI cannot host a fixture ("Hung filesystem
  call" needs FUSE), design chooses an injected slow call or a skip with its
  reason. Tests run with `python3 -m unittest discover -s tests -v`
  (README.md:187), the command CI runs as `python -m ...`
  (`.github/workflows/tests.yml:18`).
- **Speckit handoff**: exactly one feature, `specs/004-<slug>/`, created by
  `/speckit.specify` after ratification and after feature 003 merges. `002`
  is lane openRepoProject-1's (draft PR #8), `003` is change 1's. OpenSpec
  `tasks.md` holds governance boxes, the cap measurement (OQ-4) and that one
  handoff only.
- **Expected conflicts**: PR #8 and feature 003 also touch `project` and
  `tests/test_project.py`; feature 004 merges `main` in and never rebases.
- **Review inputs**: this repository has no `docs/requirements/` or
  `docs/architecture/`, which the repo-local propose flow names
  (`.claude/commands/opsx/propose.md:65-69`, :105, :132, :208, :219, :241,
  :263). The alignment review and the council read this proposal, the packet,
  `openspec/specs/`, `openspec/config.yaml` and `project` instead.

### Dependencies and Sequencing

This is change 2 of two. Change 1 is `add-project-clean-all-safe` (issue #9),
drafted in parallel. This change depends on it, cites it by name, and does not
restate its contract. Change 1 owns:

- the shared evidence model: the version check, the four repository-wide
  probes memoized per `common_dir`, the combined status probe per worktree row
  and its record bounds, NUL-delimited parsing and path escaping, the child
  environment, the 5 s per-child budget (the 60 s invocation deadline is the
  overview's own, requirement 3), and the bounded runner, not `probe()`, for
  one Git child in its own process group (DI "Probe model and deadline",
  DI:292-511; SY "One evidence model; permission is not shared", SY:78-130).
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
  merge-target terminology", BA:113-199), the plan refusals
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
  a plan cut by the batch's own deadline, and a `target-cap` plan keeps the
  suggestion: its preview is complete and lists every target, and the user
  removes some explicitly first (BA:100).
- Change 1 is ratified first. This change's spec deltas are written against
  change 1's ratified text, and a gate, code or probe that moves in change 1's
  review re-aligns this proposal before its own ratification.
- Speckit feature 004 is created after feature 003 merges, because the
  overview runs on the probes 003 builds; this change archives after change 1.
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
list for both changes: OQ-1 to OQ-3, OQ-20 to OQ-24, OQ-28 and OQ-29 are lane
additions, and the others number the packet's consolidated open decisions
(OV:311-359; HO:317-353). OQ-10 to OQ-16, OQ-22 to OQ-24, OQ-28, OQ-29 and
the batch half of OQ-25 are change 1's. OQ-19 to OQ-21, and the one record
OQ-22 leaves here, are in the absorption subsection below.

Packet open decisions taken, each citing the packet text that leaves it open:

- **OQ-4, measured costs** (OV:314-319; DI:179-180, DI:189-190,
  DI:227-228): the spec deltas mark the caps provisional, and the governance
  `tasks.md` carries the warm and cold-cache measurement, run on a Linux
  filesystem and never on a Windows drive mounted into WSL2, before the
  Speckit handoff.
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
  arrays only in JSON. Human output prints the command with shell quoting, or
  in the `$'...'` form for a path that needs it (DI:910-925). The pasteable
  `$'...'` form assumes bash 4.2 or newer, or zsh; tests assert the rendered
  string, not a shell round trip on macOS's bash 3.2.
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
  no reconciliation reserve and no removal floor; the 5 s per child is [E]'s
  and the 2 s grace is change 1's runner's. `budget` holds only
  `probe_timeout_seconds`, `invocation_timeout_seconds` and
  `probe_concurrency`.
- **OQ-25, overview exits** (DI:1066-1098): 0, 1, 2 and 130; 130 wins over 1
  (requirement 11, which departs below for SIGTERM and SIGHUP).

Lane additions here: **OQ-1, one change or two**: two, batch first; this is
the second. **OQ-2, where the overview lives**: a new `project-overview`
capability. **OQ-3, revise the packet first or absorb**: absorb here
(Corrections). OQ-20 and OQ-21 follow in the absorption subsection.

Departures from packet decisions, each citing the decision departed from:

- **Default-branch findings** (DI:704; DI:645, DI:650-651): OQ-20, below.
- **Unprobed rows close the repository gate** (DI:675-686, DI:855-859, which
  name only `inspection-error` rows and the batch's row cap): a row the
  overview's own cap or deadline left unclassified could hide an
  `inspection-error`, so the gate withholds `--all-safe` for it as well.
- **`suggestion_gate`** (the finding object, DI:810-819): a field beside
  `suggested_command` on every finding, null unless a gate withheld or
  limited that suggestion, else the gate's code. A withheld `--all-safe`
  form names `inspection-incomplete`, `inspect-cap`, or `scan-limit` or
  `deadline-exceeded` for an unprobed row; a withheld clean suggestion names
  `target-not-repository-root` (a bare repository, which change 1 refuses)
  or `unsupported-path-bytes`; a read-only suggestion for a repository over
  change 1's plain-report row cap (256) names `inspect-cap`, since that
  report would be incomplete. A repository of 129 to 256 rows gets the plain
  read-only suggestion, with no gate on findings whose table suggestion is
  that command.
- **SIGTERM and SIGHUP** (DI:1070-1075, DI:1094-1096, which treat SIGINT
  only): the SIGINT treatment, exits 143 and 129, so no Git child outlives
  the overview in its own session; after SIGHUP printing can fail with EIO,
  so `Cancelled.` is printed on a best-effort basis.

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
| `dirty-default` | the extra `dirty` preserve finding (DI:626-630) | Subsumed (OQ-19) |
| `diverged-`, `unpushed-default` | `diverged`, `unpushed`, preserve, warning (OQ-20) | Subsumed |
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
  stays `protected-default` and gains one `dirty` preserve finding; that
  finding replaces `acf0133`'s `dirty-default`.
- **OQ-20, default-branch drift and inspection** (lane addition). On a
  checkout the ladder classifies `protected-default` that is not dirty, the
  overview adds, from evidence it already holds and in `acf0133`'s order,
  `diverged` (ahead and behind both above 0) or else `unpushed` (ahead above
  0), each preserve and `warning`, or else `remote-ahead` (behind above 0),
  informational. They reuse their codes on a row whose classification stays
  `protected-default`, departing from DI:704 ("`protected-default` produces
  no finding by itself"), and add no `-default` code. A checkout whose
  status probe failed, timed out or was cut by the deadline is
  `inspection-error` by change 1's ladder (its R1), on the merge-target
  branch too, with that code's repair finding of severity error, exactly as
  `project clean` classifies it; the drift findings apply only to a checkout
  classified `protected-default`. On such a checkout the `dirty`,
  `diverged`, `unpushed` and `remote-ahead` findings carry
  `suggested_command: null`, overriding the attention table for that
  checkout only, and never set the row's `suggested_command`, departing from
  DI:645 and DI:650-651: `project clean` reports that checkout only as
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

The packet stays as merged (OQ-3). Where it is wrong or stale, the spec phase
follows this list instead:

- **Stale baseline sentences.** OV:163, DI:28 and HO:200 (and BA:30) say
  `origin/main` is now `ca4c615`; it is `da33d92`, PR #7's squash, and
  HO:365-366 and HO:377-380 describe PR #7 as opened from `506a66b` and
  "open for review". DI:33-35 (and BA:39-42) name `5fc2b51`, `1789ad9` and
  `bb91a49` as the `cleanup` branch's behaviour commits and omit `acf0133`,
  `80fdef3` and `09af8c8`; OV:176-178 lists `acf0133` and `09af8c8` but also
  omits `80fdef3`. `acf0133` and `80fdef3` are the pair this change absorbs.
- **A failed status probe on the merge-target branch.** DI:255-262 has such
  a probe yield `inspection-error` "from the ladder", and DI:675-678 counts
  it toward the repository gate, but the ladder tests the merge-target branch
  after presence and before cleanliness (`project:418-426`), so there it
  would yield `protected-default`. Change 1's R1 sets such a row to
  `inspection-error` directly, on that branch too, so DI:255-262 stands with
  "set directly" for "from the ladder", and DI:675-678, BA:643-644 and
  BA:908-910 hold once change 1 lands; the overview follows (OQ-20).
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

- **`remote-gone` before a merge proof.** A merged worktree whose remote
  branch was deleted classifies `remote-gone`, because the ladder tests
  `remote_present` before merge state (`project:442` before `:457`). Under
  GitHub's head-branch auto-delete with `fetch.prune` that is the usual state
  of a merged branch, so the overview's `--all-safe` suggestion never fires
  for the commonest merged case. The question is before Brett, with lane
  openRepoProject-3's recommendation that a local ancestry proof outrank
  `remote-gone` for worktree rows (the MVP never deletes the branch). Until
  he rules, the overview follows the packet's ladder.

## Questions Resolved by the Alignment Review

The alignment review ran on `babd1d5` (SA-1 to SA-18: 4 MISMATCH, 14 DRIFT;
QA-1 to QA-21: 9 MISMATCH, 12 GAP). 38 findings are applied and SA-3 is
superseded, some under the lane lead's rulings D-A to D-L; PR #12 carries the
reports and rulings. "Absorbing" and "Dependencies" name the subsections of
Decisions and Impact. The council has not run; its verdicts go on PR #12,
noted constraints into `clarifications.md`.

The lead's later rulings, from lane openRepoProject-3's fidelity reads of
PRs #11 and #12, are applied as well: D-M (headers [E], [L] and [G]; the 60 s
deadline in requirement 3), D-J amended (unprobed rows; What Changes,
requirement 7, Dependencies, Decisions; no Corrections entry), D-I
relabelled (OQ-20), D-O and D-X (SIGTERM, SIGHUP, best-effort `Cancelled.`;
What Changes, requirement 11, Decisions), D-P and D-V (`suggestion_gate`;
What Changes, requirement 7, Decisions), D-Q (OQ-4, Impact), C1
(Corrections), C13 (requirement 8), L5 and D-Z (Decisions), D-N and D-S
(Dependencies), and the `remote-gone` question for Brett (Open Questions).

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| SA-1 | MISMATCH | applied per D-A | Absorbing (OQ-20, table); Corrections |
| SA-2 | MISMATCH | applied per D-B (requirement 11, not 8) | What Changes; Capabilities; Dependencies |
| SA-3 | MISMATCH | superseded by D-J (QA-17 applied) | Dependencies |
| SA-4 | MISMATCH | applied | Impact |
| SA-5 | DRIFT | applied | Impact |
| SA-6 | DRIFT | applied per D-I (relabelled) | Absorbing (OQ-20); Decisions (departures) |
| SA-7 | DRIFT | applied | Corrections |
| SA-8 | DRIFT | applied per D-G | Dependencies; Impact; Corrections |
| SA-9 | DRIFT | applied | Decisions (suggestion display string) |
| SA-10 | DRIFT | applied | Impact |
| SA-11 | DRIFT | applied | Capabilities (Modified); Corrections |
| SA-12 | DRIFT | applied per D-H | Decisions (preamble); Absorbing (OQ-22) |
| SA-13 | DRIFT | applied | Decisions (OQ-7) |
| SA-14 | DRIFT | applied | Absorbing |
| SA-15 | DRIFT | applied | Capabilities (New) |
| SA-16 | DRIFT | applied | Absorbing (OQ-19) |
| SA-17 | DRIFT | applied | Absorbing |
| SA-18 | DRIFT | applied per D-K | Status; Impact; Decisions; Corrections; Open Questions; layout |
| QA-1 | MISMATCH | applied per D-A | Absorbing (OQ-20, table); Capabilities (requirement 10); Corrections |
| QA-2 | MISMATCH | applied | Absorbing (table) |
| QA-3 | MISMATCH | applied; `inspection-error-default` row per D-A | Absorbing (table) |
| QA-4 | MISMATCH | applied | What Changes; Capabilities (requirement 3) |
| QA-5 | MISMATCH | applied, consistent with D-J (amended), D-I and D-P | What Changes |
| QA-6 | MISMATCH | applied per D-I (relabelled) | Absorbing (OQ-20); Decisions (departures) |
| QA-7 | MISMATCH | applied per D-H | Decisions (preamble); Absorbing (OQ-22 record); Out of Scope |
| QA-8 | MISMATCH | applied | Capabilities (New) |
| QA-9 | MISMATCH | applied | Capabilities (requirement 8) |
| QA-10 | GAP | applied; status cells follow `project:679-681` | Absorbing (prose, table) |
| QA-11 | GAP | applied | Absorbing (table) |
| QA-12 | GAP | applied | Absorbing (table) |
| QA-13 | GAP | applied per D-B, with D-O | What Changes; Capabilities (requirement 11) |
| QA-14 | GAP | applied, with C13 | Capabilities (requirement 8) |
| QA-15 | GAP | applied | Capabilities (requirement 3) |
| QA-16 | GAP | applied, with D-M | Decisions (OQ-9) |
| QA-17 | GAP | applied per D-J (amended: no Corrections entry) | Dependencies |
| QA-18 | GAP | applied per D-E | What Changes |
| QA-19 | GAP | applied; OQ-20 states the order | What Changes; Absorbing (OQ-20) |
| QA-20 | GAP | applied, completed by C1 | Corrections |
| QA-21 | GAP | applied | Absorbing |
