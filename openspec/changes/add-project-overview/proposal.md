Lane: openRepoProject-2

# Proposal: add-project-overview

Status: draft, awaiting Brett Heap's ratification. Nothing here is ratified.

Governing issue: opensoft/openRepoProject#10, claimed by lane
openRepoProject-2 (comment 6069504479); refs #6, the design packet's record.
Its sibling, opensoft/openRepoProject#9, governs `add-project-clean-all-safe`,
the change this one depends on (see "Dependencies and sequencing").

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
  and a family holder is one row with `relationships: []` (DI:276-290).
- **Every bound is reported.** Caps of 32 roots, 4,096 entries per root, 128
  candidates and 512 worktree rows apply after canonical sorting, dropped work
  is reported as `omitted: {count, exactness}`, and at most four Git children
  run at once, across distinct repositories (DI:153-228, DI:429-449). A cap,
  timeout or deadline makes the result `incomplete` and exits 1 (DI:222-225).
- **One candidate's failure stays in its row.** A per-candidate collector
  turns exceptions and failed probes into that row's errors (DI:528-537), and
  the scan continues (DI:513-566).
- **No second classifier.** Worktree classification is the cleanup ladder as
  change 1 leaves it, fed from the overview's memoized evidence; the merge
  target is `{name, source, sha}` in the baseline `default_branch` order, and
  its absence is a `no-merge-target` finding, not an error row (DI:551-630).
- **Findings by attention category.** Each finding has one code, category
  (repair, preserve, housekeeping, informational) and severity from the
  packet's table (DI:638-659). An `error` finding exits 1, a `warning` only
  under `--strict`, `info` never; `--attention` filters the display only
  (DI:704-714).
- **Suggestions never carry permission.** A suggestion is an argv array naming
  the canonical `repository.root`: `project clean <root> --all-safe` only for
  a worktree that passes change 1's batch gates in a repository the batch
  would plan, otherwise the read-only `project clean <root>`; never `--apply`
  or `--yes`, never a bare name (DI:661-702, DI:847-886).
- **A versioned JSON envelope.** `--json` prints one `schema_version: 1`
  document (DI:716-925) that reuses the clean report's field names wherever
  it carries the same fact.
- **Default-branch health, absorbed from the closed PR #2.** The checkout on
  the merge target gains drift and inspection findings the packet left out
  (see "Absorbing doctor repository health from the closed PR #2").
- **One carve-out in `project-review-safety`.** A manifest with an invalid
  text encoding is a `manifest-invalid` row error in the overview, which then
  exits 1, not 2 (Capabilities).
- **README and tests** describe and cover all of the above (Impact).

## Dependencies and sequencing

This is change 2 of two. Change 1 is `add-project-clean-all-safe` (issue #9),
drafted in parallel. This change depends on it, cites it by name, and does not
restate its contract. Change 1 owns:

- the shared evidence model: the version check, the four repository-wide
  probes memoized per `common_dir`, the combined status probe per worktree row
  and its record bounds, NUL-delimited parsing and path escaping, the child
  environment, the 5 s per-child and 60 s per-invocation budgets, and
  process-group termination (DI "Probe model and deadline", DI:292-511; SY
  "One evidence model; permission is not shared", SY:78-130);
- the Git 2.36 floor and its codes `git-too-old` and `git-unavailable`
  (SY:51);
- every modification to `project-clean`, `project-clean-review-safety` and
  `project-command`, among them the ladder's names and order, the
  deleted-upstream `remote-gone` change and Git-first resolution of
  `project clean <path>` (DI "Baseline behavior changes", DI:1100-1173; BA
  "Command directory and repository resolution", BA:834-878);
- the cleanup gates and refusal codes the overview's suggestions mirror: the
  per-worktree gate order `main-worktree`, `unsupported-path-bytes`,
  `registration-mismatch`, `locked-worktree` (BA "Eligibility and
  merge-target terminology", BA:113-199), the plan refusals
  `inspection-incomplete` and `inspect-cap` (BA "Refusal codes", BA:987-1015)
  and the batch's worktree-row cap (BA "Cap arithmetic", BA:721-774).

Consequences:

- This change modifies none of those three specs. The overview's repository
  gate is defined by change 1's refusals: it withholds `--all-safe` exactly
  when change 1's batch would refuse that repository as
  `inspection-incomplete` or `inspect-cap`, and copies no number, so a cap
  that measurement moves in change 1 carries over.
- Change 1 is ratified first. This change's spec deltas are written against
  change 1's ratified text, and a gate, code or probe that moves in change 1's
  review re-aligns this proposal before its own ratification.
- Speckit feature 004 is created after feature 003 merges, because the
  overview runs on the probes 003 builds; this change archives after change 1.
- How the ladder becomes reusable is change 1's decision (OQ-28, DI:599-600);
  this change needs it fed from memoized evidence, spawning no probe.
- If Brett prefers one change, this proposal folds into a single
  `add-project-maintenance` change with one Speckit feature (OQ-1).

## Absorbing doctor repository health from the closed PR #2

PR #2 was closed unmerged on Brett Heap's word. Its decision record (OV:186)
assigns `acf0133` and `80fdef3` to this design: "Absorbed into the packet's
project-overview design as local-only, read-only reporting." The packet left
that to its next revision (HO:35-39, HO:379-380; OV:180-183); this proposal
does it directly (OQ-3).

What the two commits add (`git show <sha> -- project` on `origin/cleanup`,
`bb91a49`): doctor attaches `repository_health` to each complete snapshot,
recursing into family members but not project legs, with `target_branch`,
`tracking_freshness` and the cleanup rows plus `health_level`,
`health_status` and `health_recommendation`. A `protected-default` row is `ok`
unless `dirty-`, `ignored-local-files-`, `diverged-`, `unpushed-` or
`remote-ahead-default`, and `80fdef3` adds `inspection-error-default`; every
other row is a `warning`. Any `cleanup_report` refusal, a missing default
branch included, makes health `unavailable`, a warning, and doctor continues.
One check row per snapshot feeds `--strict`. Nothing is fetched.

| acf0133 / 80fdef3 element | Where the overview carries it | Status |
| --- | --- | --- |
| `target_branch` | `merge_target {name, source, sha}` (DI:570-594) | Subsumed (superset) |
| `tracking_freshness` | `git.tracking_freshness` (DI:760-763) | Subsumed |
| Per-row classification and recommendation | worktree `classification`, finding `message` (DI:790, DI:817) | Subsumed |
| Every non-default row is a warning | category and severity table (DI:638-659) | Changed on purpose: `merged-removable` and `pushed-unmerged` are `info` (SY:308-309) |
| `dirty-default` | the extra `dirty` preserve finding (DI:626-630) | Subsumed (OQ-19) |
| `diverged-`, `unpushed-`, `remote-ahead-default` | none: `protected-default` yields no finding (DI:704) | Gap, closed by OQ-20 |
| `ignored-local-files-default` | none | Changed on purpose (OQ-20) |
| `inspection-error-default` | only the row's `probe-failed` or `probe-timeout` error | Gap, closed by OQ-20 |
| Unavailable health is a warning | `no-merge-target`, repair, severity error, exit 1 (DI:551-558) | Escalated (OQ-21) |
| Aggregate check row and `--strict` | `summary.findings` and the `--strict` exit (DI:704-707, DI:1068-1075) | Subsumed |
| Recursion into family members | holder row only, `relationships: []` (DI:276-290) | Deliberately not carried |

Two of PR #2's open review threads concern this work, and the overview's own
rules answer them: "doctor `--strict` health-warning coverage" by the
severity-to-exit rule, and "doctor rendering unknown inspection state as zero
counts" by "`null` means unknown or not established" (DI:830-833). Not
carried: `09af8c8`'s remote merge target and GitHub pull-request lookup, which
is outside the absorbed pair and waits for a remote-queries proposal (PR #2
harvest table); remote evidence never proves cleanup (SY:219-226).

Decisions, each a proposal decision, open to ratification:

- **OQ-19, the extra `dirty` finding** (DI:626-630): kept. A dirty checkout on
  the merge target stays `protected-default` and gains one `dirty` preserve
  finding, `dirty-default` under the overview's code.
- **OQ-20, default-branch drift and inspection.** For a checkout the ladder
  classifies `protected-default`, the overview adds, from evidence it already
  holds, `diverged` (ahead and behind both above 0) or else `unpushed` (ahead
  above 0), each preserve and `warning`, or else `remote-ahead` (behind above
  0), informational; and an `inspection-error` repair finding of severity
  error when its status probe failed, timed out or was cut by the deadline.
  The classification stays `protected-default`, so overview and clean still
  classify alike (DI:618-624). These findings reuse existing codes, add no
  `-default` code, and suggest no command, because `project clean` refuses to
  push or delete the merge-target branch (`project:539-540`, `:579-580`).
  Ignored files in that checkout yield no finding: it is never a removal
  target, and a `.venv` there would otherwise warn on most projects.
- **OQ-21, `no-merge-target` severity** (DI:551-558): error, exit 1. Without a
  merge target no worktree of the repository can be classified, so the row
  must not read as healthy, and other rows are unaffected. The departure from
  `acf0133`'s warning is recorded here.
- **OQ-22, doctor** (OV:269-273): `project doctor` gains no health section and
  no pointer; it changes only through change 1's shared evidence. No
  `project-doctor-repository-health` capability is created; `acf0133`'s
  unmerged one is superseded by `project-overview`.

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
  `specs/project-overview/spec.md` with ten ADDED requirements (proposed
  header, then proposed text):
  1. `Overview discovers projects within configured roots only`: SHALL
     examine each root and its immediate entries only, by the marker table.
  2. `Overview groups worktrees by repository identity`: rows SHALL be keyed
     by `{root, common_dir, dev, ino}`; a family holder SHALL be one row.
  3. `Overview bounds its work and reports what it omitted`: SHALL cap after
     sorting, within change 1's budgets, and report each dropped unit.
  4. `Overview isolates one candidate's failure`: a failure SHALL become that
     candidate's error row and SHALL NOT change any other row.
  5. `Overview reuses the cleanup classifier and merge target`: SHALL classify
     by change 1's ladder and report the merge target `{name, source, sha}`.
  6. `Overview reports findings by attention category`: severity SHALL decide
     the exit, and `--attention` SHALL change only the display.
  7. `Overview suggests only gated clean commands`: SHALL suggest argv naming
     `repository.root`, `--all-safe` only behind change 1's gates.
  8. `Overview prints a versioned JSON envelope`: SHALL print one
     `schema_version: 1` envelope; a `--json` exit 2 prints `{"error", "code"}`.
  9. `Overview is local and read-only`: SHALL make no network connection and
     no filesystem or Git mutation.
  10. `Overview reports default-branch health`: the merge-target checkout
      SHALL keep `protected-default` and gain the OQ-19 and OQ-20 findings.

  It is a new capability rather than ADDED requirements in `project-command`
  (OQ-2): `overview` is a whole subcommand with its own contract, as `clean`
  is in `project-clean`. The prefer-triad proposal dropped its standalone
  capability because it changed an existing requirement (its `proposal.md`,
  lines 322-329), which is not the case here.

### Modified Capabilities

- `project-review-safety`: one MODIFIED requirement, whose canonical header
  is `### Requirement: YAML decoding errors are structured refusals` (PRS:78)
  and whose canonical text is:

  > Every YAML input read by the command SHALL turn an invalid text encoding
  > into a normal refusal. JSON mode MUST preserve its structured error output
  > and exit code 2 rather than printing a traceback.

  The overview conflicts with "exit code 2": its collector turns the `Refused`
  that `manifest()` raises for such a manifest into a `manifest-invalid` row
  error and exits 1 with the other rows intact (DI:528-531, DI:1279-1286). The
  MODIFIED block keeps both sentences and the canonical scenario for every
  other command, and adds that in `project overview` such a manifest SHALL be
  a `manifest-invalid` error on its candidate's row, never a traceback, while
  the run continues and exits 1, with one scenario for it.

Untouched: the other five `project-review-safety` requirements (PRS:9, :21,
:32, :51, :67), since the overview renders no profile field, reads no bench
registry or parked work, applies no update and renders no nested estate or
leg; `project-command`, `project-clean` and `project-clean-review-safety`,
which only change 1 modifies; and `speckit-extension-integration`.

## Impact

- **`project`**: a new `overview` subcommand; a per-candidate collector and
  two-phase scheduler over change 1's shared probes; human and JSON
  renderers. Every other subcommand changes only as change 1 changes it.
  Standard library only; no new dependency.
- **`README.md`**: a section for `project overview` covering roots and
  `PROJECTS_DIR`, the caps, `--attention`, `--strict`, the exits, the JSON
  envelope, and that a suggestion is advice to review, not permission.
- **`tests/test_project.py`**: temporary fixtures only, network disabled,
  zero-mutation snapshots, covering the packet's 31 MVP scenarios
  (DI:1175-1446), the default-branch findings and the carve-out. Where CI
  cannot host a fixture ("Hung filesystem call" needs FUSE), design chooses an
  injected slow call or a skip with its reason. Tests run as CI does,
  `python3 -m unittest discover -s tests -v` (`.github/workflows/tests.yml:18`).
- **Speckit handoff**: exactly one feature, `specs/004-<slug>/`, created by
  `/speckit.specify` after ratification and after feature 003 merges. `002`
  is lane openRepoProject-1's (draft PR #8), `003` is change 1's. OpenSpec
  `tasks.md` holds governance boxes and that one handoff only.
- **Expected conflicts**: PR #8 and feature 003 also touch `project` and
  `tests/test_project.py`; feature 004 merges `main` in and never rebases.
- **Review inputs**: this repository has no `docs/requirements/` or
  `docs/architecture/`, which the repo-local propose flow names
  (`.claude/commands/opsx/propose.md:65-69`, :105, :132, :208, :219, :241,
  :263). The alignment review and the council read this proposal, the packet,
  `openspec/specs/`, `openspec/config.yaml` and `project` instead.

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
change to `project clean` (change 1's) or `project doctor` (OQ-22).

## Decisions taken by this proposal

The numbers label the packet's consolidated open decisions (OV:311-359;
HO:317-353) as this lane numbers them for both changes. Each is a proposal
decision, open to ratification; OQ-19 to OQ-22 are in the absorption section.
OQ-10 to OQ-16, OQ-23, OQ-24, OQ-28, OQ-29 and the batch half of OQ-25
concern `project clean` alone and are change 1's.

- **OQ-1, one change or two**: two, batch first; this is the second.
- **OQ-2, where the overview lives**: a new `project-overview` capability.
- **OQ-3, revise the packet first or absorb**: absorb here (Corrections).
- **OQ-4, measured costs** (OV:314-319; DI:179-194): not measured here.
  Design measures warm and cold child costs and the listing phase on a
  realistic estate (Git 2.43, WSL2) and reruns the fit test; OQ-5 rests on it.
- **OQ-5, caps** (OV:35): 32 roots, 4,096 entries per root, 128 candidates and
  512 worktree rows. The record bounds (64 ignored, 4,096 records, 8 samples)
  are change 1's shared values.
- **OQ-6, concurrency** (OV:320-327): four children across distinct
  repositories. If design rejects concurrency, the packet's serial fallback
  of 32 candidates and 128 worktree rows applies (DI:1465-1471).
- **OQ-7, a per-repository row cap** (OV:328-331): none. A repository with
  more than about 355 worktree rows ends at the deadline, visibly incomplete.
- **OQ-8, configurable limits** (OV:332): none; the fixed values are reported
  in `limits` and `budget`.
- **OQ-9, deadlines** (DI:451-485): 60 s per invocation, 5 s per child and
  per root listing, 2 s from TERM to KILL; only the per-root listing bound is
  the overview's own, the rest are change 1's.
- **OQ-17, an `attention` alias** (DI:72-75): no.
- **OQ-18, `--attention --json`** (DI:709-714): the full envelope; consumers
  filter on `findings[].category`.
- **Suggestion display string** (OV:353; DI:1479-1480; unnumbered): argv
  arrays only in JSON. Human output prints the command with shell quoting, or
  in the `$'...'` form for a path that needs it (DI:910-925).
- **OQ-25, overview exits** (DI:1068-1098): 0, 1, 2 and 130; 130 wins over 1.
- **OQ-26, spelling** (OV:356):
  `project overview [--root D]... [--attention] [--json] [--strict]`.
- **OQ-27, separate changes** (OV:357-359): yes, one per extension.

## Corrections to the packet

The packet stays as merged (OQ-3). Where it is wrong or stale, the spec phase
follows this list instead:

- **Stale `origin/main`.** OV:163, DI:28 and HO:200 (and BA:30) say
  `origin/main` is now `ca4c615`; it is `da33d92`, PR #7's squash.
- **Incomplete commit list.** DI:33-35 (and BA:39-42) name `5fc2b51`,
  `1789ad9` and `bb91a49` as the `cleanup` branch's behaviour commits and omit
  `acf0133` and `09af8c8`, which OV:176-178 lists; `acf0133` is the one this
  change absorbs.
- **A failed status probe on the merge-target branch.** DI:255-262 has such a
  probe yield `inspection-error` "from the ladder", and DI:675-678 counts it
  toward the repository gate. The ladder tests the merge-target branch first
  (`project:421-426`), so on that branch it yields `protected-default`. The
  overview keeps that classification and adds an `inspection-error` finding
  (OQ-20), and its repository gate follows whatever change 1's batch decides
  for the same row; BA:643-644 and BA:908-910 carry the same assumption.
- **Process groups on Python 3.10.** DI:457-458 (and BA:398) start children
  with `subprocess.Popen(..., process_group=0)`, a parameter added in Python
  3.11, while `README.md:17` requires Python 3.10 or newer and CI tests 3.10
  (`.github/workflows/tests.yml:10`). `start_new_session=True` also gives
  each child its own process group. The mechanism is change 1's to settle.
- **Isolation versus exit 2.** DI:1279-1286 has the overview exit 1 on a
  `Refused` manifest, which PRS:78-82 forbids for an invalid encoding; the
  MODIFIED requirement resolves it.

## Questions Resolved by the Alignment Review

None yet: the alignment review and the council have not run. Their rulings
go on this change's pull request, noted constraints into `clarifications.md`.
