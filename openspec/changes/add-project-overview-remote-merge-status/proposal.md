Lane: openRepoProject-5

# Proposal: add-project-overview-remote-merge-status

Status: draft; alignment review and council pending (lane openRepoProject-5
runs them on this draft); nothing here is ratified. Governing issue:
opensoft/openRepoProject#25, claimed by lane openRepoProject-5 (comment
6111242617); refs #6, the record of the project maintenance design packet.
Proposed on Brett Heap's word "usage reset, resume all. read handoff and resume
and fan out wide and do as much as possible in parallel" (2026-10-11), read by
lanes openRepoProject-4 and openRepoProject-5 as a go for the candidate list
they put to him.

Citations are `file:line`. The packet is cited at `da33d92`, equal to main
`961c405` for `ideation/`: `DI`, `SY`, `BA` and `OV` are its
`project-maintenance-` files `project-discovery.md`,
`synthesis-inspect-and-retire.md`, `batch-cleanup.md` and `overview.md`, and
`HO` is `next-session-project-maintenance-fix-handoff.md`. Everything else is
cited at main `961c405`, whose `openspec/`, `ideation/`, `project` and
`tests/` main still holds unchanged at `e9d6711` (L-15): `APO` is
`openspec/changes/add-project-overview/` (change 2, ratified and unarchived)
and `APO/ov` its `specs/project-overview/spec.md`, the text this change's
deltas are written on; `CAS` is `openspec/changes/add-project-clean-all-safe/`
(change 1), with `CAS/pc` and `CAS/cmd` its `specs/project-clean/spec.md` and
`specs/project-command/spec.md`; `PRS` is
`openspec/specs/project-review-safety/spec.md`; and `project:N` is the
executable. Change 1's evidence model,
`Repository inspection requires Git 2.36 and shares one evidence model`
(CAS/cmd:90), is [E]. The lane's rulings are cited as L-1 to L-9 and C-1 to
C-8 (2026-10-11), and L-10 to L-15, B-14, C-9 and C-10 (2026-10-18).

## Why

The overview change 2 defines, like `project clean`, judges merges by local
ancestry as of the last fetch (APO/ov:709-717; CAS/pc:5-9). A branch merged on
GitHub by squash never enters the merge target's local ancestry (BA:195-199),
so its worktree reads `pushed-unmerged`, or `remote-gone` once GitHub deleted
its branch, and nothing in either output says why it is kept. The person has
to open GitHub to learn that the work is merged.

The packet names the interface, `project overview --remote` (DI:72-75), and
fixes its boundary (DI:1036-1060): opt-in and read-only, a validated canonical
GitHub identity, requests deduplicated by exact head and bounded in count,
concurrency, time, pages, items and bytes, every failure an explicit unknown,
and local ancestry the only cleanup gate. Change 2 leaves exactly this to "a
remote-queries proposal" (APO proposal.md:566-568, :810-812), and the packet
keeps remote queries a separately governed extension (HO:47-50; OV:142-146;
CAS proposal.md:756-757, OQ-27). This is that proposal. The closed PR #2's
`09af8c8` is the harvest source, for reference only: it queried GitHub from
plain `clean` and `doctor` with no opt-in and no bounds, put the answer inside
the revalidation signature and added ladder classes.

## What Changes

- **`project overview --remote`, opt-in.** Without it nothing changes: no
  `gh` child starts, and the document and the human report are exactly change
  2's. `--remote` exists on `project overview` alone; `clean`, `status` and
  `doctor` stay local (C-1).
- **Which rows are explained.** A worktree row is queried when it is on a
  branch other than the merge target, its head is known, and local ancestry
  does not prove it merged (`merged_into_target` false). A row whose upstream
  was deleted is queried by its head like any other (C-6). Every other row
  has no `remote` key, never a null one (L-10).
- **Where the identity comes from.** After collection, for each repository
  with a queried row, at most two pinned, read-only Git children, counted in
  the envelope's `probes` like every other Git child (C-9), read the
  merge-target branch's `branch.<target>.remote` and `branch.<target>.merge`
  and that remote's URL as Git expands it, never a worktree row's upstream
  (C-3). Only a valid GitHub `owner/repository` on host `github.com`, as PRS:32
  accepts one, is used; a credential-bearing, non-GitHub or malformed URL, or
  no remote configured for the merge target, makes the repository's queried
  rows `unavailable` with a reason and sends nothing. No URL is printed or
  forwarded (DI:1039-1042).
- **One bounded request per exact head.** Rows share one request per
  `(host, owner/repository, head)`, in canonical order (DI:1044). Each request
  is one `gh api` child with a fixed read-only GraphQL query for at most 100
  pull requests associated with that commit, one page, never paginated or
  cached. At most 64 requests, four at once, each `min(5 s, remote time
  remaining)`, inside a 30 s remote budget, counted from the first request
  after collection, that is part of the 60 s deadline, not added to it; at
  most 1 MiB of each body (DI:1045-1051; C-4). On expiry, requests not sent
  are `unknown` with `cancelled` and requests in flight are stopped and
  `unknown` with `aborted` (DI:1051-1053).
- **Explicit results.** A row's `remote` is `{state, number, url, head_sha,
  reason}` with `state` `merged`, `open`, `closed`, `not-found`, `unavailable`
  or `unknown`, from pull requests whose head is exactly the row's head and
  whose base is the merge target's remote branch in that repository (C-5). A
  further page, a body cut at 1 MiB, a timeout, a 401, a 403, a rate limit or
  any other failure is `unknown` with its reason, never a partial answer, and
  no response text, `gh` error output or credential appears in either output
  (DI:1055-1058). No `gh` on `PATH`, or a `gh` that needs authentication, is
  `unavailable`.
- **Evidence, never permission.** Remote evidence changes no classification,
  finding, suggestion, gate, row status, summary count, `completeness` or exit
  status, and is kept nowhere beyond the invocation, so it can never feed a
  `project clean` eligibility gate, `plan_digest` or revalidation (DI:1059-1060;
  SY:129-130; HO:167). No finding code, ladder class or stage value is added
  (L-4).
- **What the person sees.** Under a kept worktree's finding a `remote` line
  says, for a merged one, "merged on GitHub as pull request #N; local ancestry
  does not prove it (a squash or rebase merge, or a merge target not fetched
  since); never retired on this evidence"; one summary line gives the requests
  sent, the counts by state and the sentence "Remote evidence was queried live
  from github.com and may already be stale; it never authorizes cleanup."
  Under `--json` the envelope gains a `remote` object with its limits, its
  budget, its count of `gh` requests (`requests`), the counts by state, the
  freshness sentence and its own completeness, and each queried row a
  `remote` sub-record, all only in a `--remote` run: without `--remote` both
  keys are absent, not null, and in a `--remote` run a row outside the query
  set has no `remote` key either (L-10).
- **One carve-out in "Overview is local and read-only"**, in lane
  openRepoProject-4's wording. Without `--remote` the requirement holds as
  written. With it, the network clause still binds the `project` process and
  every Git child and does not bind the `gh` children of the ADDED
  requirement; every other sentence holds; and the credential clause splits:
  the `project` process reads no credential file, a `gh` child authenticates
  by the GitHub client's own means, and the overview reads, tests, prints and
  forwards no credential value (C-7).
- **One addition to "Overview bounds its work and reports what it
  omitted"**, lane openRepoProject-4's fourth option (C-9). The remote-target
  reads are Git children, so `probes.performed` counts them as it counts every
  Git child started, and in a `--remote` run `probes.estimated` gains 1 per
  repository with a queried row and 1 more per such repository whose merge
  target names a usable remote, so that the two stay equal in a complete run.
  A remote-phase child that reaches its limit or is stopped at the deadline
  is recorded in its rows' `remote`, never as a row or scan error. Without
  `--remote` both counts are change 2's, byte for byte; the `gh` requests are
  counted in `remote.requests` alone, and the `remote` object keeps no
  `probes` of its own, so a run has one count of Git children.

## Rules This Change Keeps

- **Local ancestry is the only removal proof** (BA:195-199; SY:224-226;
  DI:1059-1060). A merged pull request explains a kept row; it never makes it
  removable, and `project clean` never sees it.
- **Opt-in and read-only** (DI:1038-1039). A default overview opens no
  connection (APO/ov:710); a `--remote` run sends only the fixed query, writes
  nothing, mutates nothing and keeps nothing (DI:1060, "Persistent remote
  caching is deferred").
- **Credentials are never touched** (DI:1056-1058). The `project` process
  reads, tests, prints and forwards no credential value; `gh` authenticates by
  its own path, and a URL with embedded credentials is refused unprinted.
- **Unknown is explicit** (DI:1049-1056). Every failure is `unknown` or
  `unavailable` with a reason, never a guess and never `not-found`.
- **Bounded, inside the overview's run bound.** The remote phase sits inside
  the 60 s deadline, so change 2's 60 + 2 + 2 = 64 s bound holds
  (APO proposal.md:483-487).
- **No new vocabulary for the local result.** The fifteen ladder names
  (CAS/pc:107-114), the closed attention table (APO/ov:421-422) and the stage
  enum stay as they are (L-4).
- **`clean`, `status` and `doctor` stay local** (CAS/pc:5-9; CAS/cmd:6;
  CAS proposal.md:344-346).

## What This Repository Does Not Own

- **Pull-request state**: GitHub, read only through its client, `gh`, as of
  the moment of the query.
- **Authentication**: the GitHub CLI's own credential store and environment
  (`gh auth login`, `GH_TOKEN`); `project` reads none of it.
- **Which pull requests a commit is associated with**: GitHub's API, whose
  scope this change reports and does not redefine.
- **Remote and URL configuration**: Git, including `url.<base>.insteadOf`,
  which the identity read takes as Git expands it.

## Capabilities

### New Capabilities

None. `project-overview` is change 2's capability, unarchived; this change
writes its deltas on change 2's text (L-1, L-3).

### Modified Capabilities

Headers are quoted verbatim, one per line; the ADDED header is proposed text.
Line numbers are APO/ov's at `961c405`.

- `project-overview` (all twelve of change 2's requirements accounted for; it
  has no canonical spec until change 2 archives):
  - MODIFIED (`:166`):
    `### Requirement: Overview bounds its work and reports what it omitted`.
    Change 2's whole block and its thirteen scenarios stay untouched; one
    paragraph is added (C-9): in a `--remote` run the remote-target reads are
    Git children that `probes.performed` counts, `probes.estimated` gains 1
    per repository with a queried row and 1 more per such repository whose
    merge target names a usable remote, the `gh` children are counted in
    neither, and a remote-phase child stopped at its limit or at the deadline
    is recorded in its rows' `remote`, never as a row or scan error; without
    `--remote` both counts stay as change 2 states them. Added scenario: in a
    complete run `estimated` equals `performed` with and without `--remote`,
    the `--remote` run's counts exceeding the other's by exactly the
    remote-target reads, and the `gh` request counted only in
    `remote.requests`.
  - MODIFIED (`:709`):
    `### Requirement: Overview is local and read-only`.
    Change 2's whole block and its one scenario stay untouched; a second
    paragraph, in lane openRepoProject-4's wording, says that without
    `--remote` the requirement holds as written, and that with it the network
    clause still binds the `project` process and every Git child and does not
    bind the `gh` children of the ADDED requirement, every other sentence
    holding (no fetch, mutation or file write; nothing kept), the credential
    clause split three ways, and remote evidence labelled as live. Added
    scenario: a `--remote` run with a fake `gh` leaves the zero-mutation
    snapshots identical, opens no connection from `project`, sends only the
    fixed query, again on a second run, and every recorded `gh` environment
    sets `GH_NO_UPDATE_NOTIFIER=1`, `GH_NO_EXTENSION_UPDATE_NOTIFIER=1` and
    `GH_PROMPT_DISABLED=1`.
  - ADDED:
    `### Requirement: Overview reports remote merge evidence on request`.
    The opt-in; the query set; the remote target from the merge target's
    branch configuration and the identity rule; the dedupe key; the request,
    its argv and environment; the 64-request, four-at-once, 5 s, 30 s,
    one-page, 100-item and 1 MiB bounds; the explicit `unknown` and
    `unavailable` results with their reasons; cancellation on expiry; the row
    `remote` sub-record, on queried rows only, and the envelope `remote`
    object, each absent, never null, where it does not apply (L-10); the
    freshness sentence; isolation from every local result and from `project
    clean`; and the human lines. Eleven scenarios.
  - Untouched (`:10`):
    `### Requirement: Overview discovers projects within configured roots only`
  - Untouched (`:74`):
    `### Requirement: Overview groups worktrees by repository identity`
  - Untouched (`:317`):
    `### Requirement: Overview isolates one candidate's failure`
  - Untouched (`:358`):
    `### Requirement: Overview reuses the cleanup classifier and merge target`
    (`add-project-clean-cache-disposal` carries a MODIFIED block of it under
    ruling B-14; this change does not)
  - Untouched (`:420`):
    `### Requirement: Overview reports findings by attention category`
    (no finding code is added)
  - Untouched (`:483`):
    `### Requirement: Overview suggests only gated clean commands`
  - Untouched (`:606`):
    `### Requirement: Overview prints a versioned JSON envelope`
    (fields added in a `--remote` run only, absent, not null, without it,
    under its "additive" sentence; Decisions, Open Questions)
  - Untouched (`:724`):
    `### Requirement: Overview reports default-branch health`
  - Untouched (`:761`):
    `### Requirement: Overview exits by completeness and severity`
  - Untouched (`:801`):
    `### Requirement: Overview renders a readable human report`
    (a `remote` line and a summary line added in a `--remote` run only)
- `project-clean`, `project-clean-review-safety`, `project-command`,
  `project-review-safety` (change 2's MODIFIED "YAML decoding errors are
  structured refusals" included) and `speckit-extension-integration`:
  untouched.

In sum: two MODIFIED and one ADDED requirement in `project-overview`, 27
scenarios (14, 2 and 11), nothing else.

## Impact

- **`project`**: the overview's parser gains `--remote`. After collection, a
  remote phase runs the remote-target reads (at most two Git children per
  repository with a queried row, through change 1's runner under [E]'s pins
  and scrub, counted in the envelope's `probes`), then up to four `gh`
  children at once through the overview's control loop, reads their bounded
  output, and adds the `remote` fields and lines. No other
  subcommand changes. No new dependency: `gh` is optional at run time, its
  absence giving `unavailable`, and nothing is imported. `probe()`
  (`project:60-65`, one child, 15 s, no process group) is not used for `gh`.
- **`README.md`**: the overview section gains `--remote`: what it asks, that
  it needs an authenticated `gh`, its bounds, what `unknown` and `unavailable`
  mean, that the answer is live, and that it never authorizes cleanup.
- **`tests/test_project.py`**: one test named after each scenario, offline,
  with a fake `gh` written into the fake bin directory (`fake_bin`,
  tests:148; `write_fake`, tests:172) that answers from a fixture table and
  records each argv, environment and working directory, and with networking
  disabled for the `project` process as change 2's design does (APO
  design.md, D13); no test runs a real `gh` or reaches the network (C-8). The
  tests run with `python3 -m unittest discover -s tests -v`, as CI runs them
  on Linux only since PR #32: the `tests` workflow's two jobs, `test (3.10)`
  and `test (3.12)`, on `ubuntu-latest` (`.github/workflows/tests.yml` at
  main `e9d6711`; L-12).
- **Speckit handoff**: exactly one feature, created by `/speckit.specify`
  after ratification, after feature 005 lands and after change 2 is
  archived, under the next free number, 006 or later, from a local `main`
  synced to `origin/main` (L-7).
- **Expected conflicts**: features 004 and 005, the realizations of
  `add-project-clean-branch-retirement` and `add-project-clean-cache-disposal`,
  and lane openRepoProject-1's PR #21 (`new()` only) edit `project`,
  `tests/test_project.py` and `README.md`; whichever merges second merges
  `main` in, never rebasing (CAS proposal.md:684-686).

### Dependencies and Sequencing

- **Written on change 2's text (L-1, L-15).** The two MODIFIED blocks are
  change 2's "Overview bounds its work and reports what it omitted"
  (APO/ov:166-315) and "Overview is local and read-only" (APO/ov:709-722) as
  merged at `961c405`, which main still holds at `e9d6711` with change 2
  unarchived (2026-10-18), not `openspec/specs/`, which has no
  `project-overview` yet; main is not merged into this branch. `openspec
  validate --strict` passes while change 2 is unarchived; archive is the gate
  for the MODIFIED base. If change 2's text moves before it archives, these
  blocks re-align before this change is ratified, and any sentence lane
  openRepoProject-4 asks for comes as a follow-up commit.
- **Lane openRepoProject-4's agreement gates the spec text (C-7, C-9).**
  "Overview is local and read-only" and the ADDED requirement were committed
  after lane openRepoProject-4 read them (2026-10-11). The block of
  "Overview bounds its work and reports what it omitted", its new scenario,
  and the ADDED requirement's edits for C-9 and L-10 are committed only
  after lane openRepoProject-4 agrees their diff.
- **Archives after change 2 (L-5).** Change 2 archives after change 1 and
  after feature 005 merges (APO design.md, Migration Plan 5); this change
  archives after change 2 archives.
- **Realized after feature 005 (lane openRepoProject-4's terms).** Feature 005
  is specified from change 2 as ratified, local only, with no `--remote`, and
  does not anticipate this change. This change edits none of change 2's files
  and nothing of feature 005; what its realization needs from 005's code is
  under Open Questions, addressed to lane openRepoProject-4, never stated
  here as a fact.
- **Beside its two siblings (L-5).** `add-project-clean-cache-disposal`
  (issue #24) archives after change 1 and, since it carries a MODIFIED block
  of change 2's "Overview reuses the cleanup classifier and merge target"
  (B-14), after change 2 as well; `add-project-clean-branch-retirement`
  (issue #23) archives after it. This change shares no requirement with
  either, depends on neither, and never alters feature 004's or 005's order.
- **PR #19 is not a dependency.** At its head `c462d87`, still a draft on
  2026-10-18 (L-15), it keeps "Children
  other than Git SHALL keep 15 s." and exempts only `clean`'s push child from
  the protocol pins; neither moves what this change reads.
- **Harvest.** `09af8c8` is reference only: none of its `clean` or `doctor`
  behaviour returns. Its two open Copilot threads are answered here: the
  remote target "only from a checked-out target worktree" (3989411802) by
  C-3, and remote evidence "bypassed when the feature's own upstream was
  deleted" (3989411854) by C-6; doctor's non-goal thread (3989411958) is moot,
  doctor staying local.

## Out of Scope

- **Network use by `clean`, `status` or `doctor`** (C-1; CAS/pc:5-9;
  CAS/cmd:6).
- **A no-network comparison against the merge target's remote-tracking ref**
  (`09af8c8`'s `merged_into_remote_target`; C-2), recommended as its own small
  change: it costs one repository-wide child and would change fields or the
  classifier that changes 1 and 2 own.
- **Squash-merge equivalence as a removal proof** (BA:195-199; SY:225-226;
  change 1's open question on squash-merged branches).
- **Persistent remote caching** (DI:1060), and `gh`'s own `--cache`.
- **Hosts other than `github.com`**, GitHub Enterprise included: such a remote
  is `unavailable`.
- **A fetch option** (archived `2026-10-07-add-project-clean-command`
  design.md:39-43).
- **Branch retirement and cache disposal**: issues #23 and #24.

## Decisions Taken by This Proposal

Each is a proposal decision, open to ratification. The lane's rulings are
applied as listed; where the sources and the rulings are silent, this
proposal decided and records the alternative.

The lane's common rulings: **L-1** (drafted on change 2's ratified text at
`961c405`, unarchived until feature 005 merges, APO design.md, Migration
Plan 5; archives after it), **L-2** (packet cited at `da33d92`; nothing
under `ideation/brainstorm/` edited), **L-3** (stays in `project-overview`;
PR #2's `project-clean-remote-merge-status` capability is not reused; only
the two texts the opt-in contradicts are MODIFIED, "Overview is local and
read-only" and, for the probe count, "Overview bounds its work and reports
what it omitted" (C-9), and the new contract is ADDED under a name no change
2 requirement has), **L-4** (a row sub-record and an envelope object stated
in the ADDED requirement; no stage, ladder or finding value;
CAS/pc:1129-1131 and APO/ov:655-658 disagree on enums; Open Questions), **L-5**
(archive order), **L-6** (issue #25 and the Status line), **L-7** (the
feature number at `/speckit.specify`), **L-8** (the flow: draft here,
reviews by the lane) and **L-9** (no host-absolute path; the bidi check).

From the addendum of 2026-10-18: **L-10** (the row `remote` and the envelope
`remote` are present only in a `--remote` run and absent, never null,
otherwise; the row's only on a queried row, Decisions below), **L-12** (CI is
Linux only since PR #32: the `tests` workflow's `test (3.10)` and `test
(3.12)` on `ubuntu-latest`; no statement here rested on macOS CI alone),
**L-13** (commit trailers), **L-15** (written on change 2's text at main
`e9d6711`, whose `openspec/` equals `961c405`'s; main is not merged into this
branch), and **C-9** and **C-10** below. L-14 waits for this change's first
alignment review.

Packet open decisions taken, each citing the text that leaves it open:

- **Scope, C-1** (DI:72-75 calls `project overview --remote` a possible later
  interface; DI:1484-1486, OV:357-358 and HO:47-50 leave the remote
  integration to its own decision, and nothing says whether `clean` or doctor
  gets it): `project overview --remote` only. Rejected: `09af8c8`'s queries
  from plain `clean` and `doctor`, against CAS/pc:5-9 and change 1's OQ-22
  (CAS proposal.md:844-847).
- **The remote-tracking comparison, C-2** (not addressed by the packet): Out
  of Scope, recommended as its own change.
- **The remote target, C-3** (DI:1039-1042 asks for "a validated canonical
  GitHub remote" without naming which remote): the merge-target branch's
  `branch.<target>.remote` and `.merge`, never a worktree row's upstream or a
  checked-out target worktree; the identity accepted by PRS:32's rule.
- **The client and bounds, C-4** (DI:1056-1057, "Use the normal GitHub
  client authentication path", names no client): `gh api`, one child per
  request, under the packet's bounds verbatim; the 5 s is this child kind's
  own limit within the overview, beside CAS/cmd:189's "Children other than
  Git SHALL keep 15 s." (Open Questions).
- **The evidence fields, C-5** (DI:1036-1060 names no output form;
  APO/ov:421-422 closes the finding table for schema version 1): the row
  sub-record `remote {state, number, url, head_sha, reason}`, an envelope
  `remote` object with the freshness sentence, and no finding code.
- **Dedupe and expiry, C-6** (DI:1044, DI:1051-1053): keyed by host,
  repository and exact head; every queried row asked by its head, a row whose
  upstream was deleted included; expiry cancels what is unsent and aborts
  what is in flight, each `unknown`.
- **The two blocks, C-7** (APO/ov:710 forbids every network connection, and no
  change 2 requirement has room for remote evidence): MODIFIED "Overview is
  local and read-only" with the opt-in carve-out and nothing else loosened,
  and ADDED "Overview reports remote merge evidence on request". Lane
  openRepoProject-4, the owner of change 2 and feature 005, read the two
  headers and that MODIFIED block's difference from change 2's text and agreed
  them on three edits (2026-10-11), applied before the delta file was
  committed: its own wording of the carve-out, with the credential clause
  split; the `gh` requests counted in the `remote` object's `requests`, never
  in `probes` (its edit (b), whose other half, the remote-target reads kept
  out of the envelope's `probes`, its fourth option has since replaced:
  C-9); and `gh`'s update-notifier and prompt switches set and asserted from
  the fake `gh`'s recorded environment.
  The `remote` keys are absent, not null, without `--remote`, the condition
  for reading them as additive.
- **Tests, C-8**: offline, with a fake `gh` on `PATH`.
- **The probe count, C-9** (lane openRepoProject-4's fourth option,
  2026-10-11, in place of the remote-target half of its edit (b);
  APO/ov:248-254, where "`performed` counts every Git child started" and
  `estimated` is the exact count paired with it): the remote-target reads are
  counted in the envelope's `probes`, in both `estimated` and `performed`, so
  a run has one count of Git children, and the first draft's `remote.probes`
  is dropped. `performed` keeps change 2's definition, under which the reads
  fall as Git children. `estimated` gains a term in a `--remote` run only,
  stated in a MODIFIED block of "Overview bounds its work and reports what it
  omitted" that carries change 2's whole requirement and its thirteen
  scenarios with additions only, and one added scenario pins `estimated`
  equal to `performed` in a complete `--remote` run. A run without
  `--remote` counts exactly as change 2 does, and the `gh` requests stay in
  `remote.requests {estimated, performed}`. `schema_version` stays 1: a run
  without `--remote` reports what change 2 defines byte for byte, and
  `estimated` keeps its meaning, the Git children the run needs, paired with
  the Git children it started. Two readings of the ruling, both in the block
  lane openRepoProject-4 is to agree: its sample sentence, "2 per distinct
  repository whose merge target's remote is read", is written as 1 per
  repository with a queried row plus 1 more where that first read names a
  usable remote, because a merge target that names no remote takes one read,
  not two, and a flat 2 would leave `estimated` above `performed` in a
  complete run, which the pinning scenario forbids; and the block also says
  that a remote-phase child that reaches its limit or is stopped at the
  deadline is recorded in its rows' `remote`, never as a row or scan error,
  because once the reads are counted as that requirement's Git children its
  "its row recorded `probe-timeout`" and "recorded `deadline-exceeded`"
  (APO/ov:176-178) would otherwise make them row errors, against the ADDED
  requirement's isolation clause, and L-3 settles such a contradiction in the
  MODIFIED block, not from the ADDED one. Rejected: the first draft's own
  `remote.probes` beside the envelope's (two counts of Git children, and
  change 2's "every Git child" read as collection's alone).
- **CI, C-10**: L-12 applied to the proposal, design and tasks; every CI
  statement names the current matrix.

Decisions where the sources and the rulings are silent:

- **The query set**: rows on a branch other than the merge target with a
  known head and `merged_into_target` false. Rejected: every row (spends
  requests on rows local ancestry already proves); only `pushed-unmerged` and
  `remote-gone` rows (misses a dirty or unpublished worktree whose branch was
  squash-merged).
- **The request**: a GraphQL commit lookup of associated pull requests, which
  answers an unknown commit with a null object (`not-found`) and states a
  further page in the body. Rejected: REST `commits/{sha}/pulls`, which
  answers an unknown commit with HTTP 422, an `unknown` under DI:1055-1056, and
  signals a further page only in a header; `gh pr list` (`09af8c8`), which
  looks up by branch name, hides the page information and stops at gh's
  default of 30.
- **Matching**: the head object id exactly the row's head, the base branch
  the merge ref's branch and the base repository the identity; then `merged`
  before `open` before `closed`, the highest number within a state. Rejected:
  the highest number first, as `09af8c8` chose, which a suppressed Copilot
  finding faulted for picking before checking the state.
- **A remote phase after collection**, its 30 s starting with the first
  request. Rejected: interleaving requests with collection, which would need
  a hook in feature 005's scheduler and make dispatch depend on completion
  order.
- **At most two Git children per repository for the remote target**, the
  second only when the first names a usable remote, counted in the
  envelope's `probes` (C-9). Rejected: parsing
  `<common_dir>/config`, which includes and `insteadOf` would make disagree
  with Git, as change 2's design rejected for `core.worktree` (APO
  design.md:218-219); listing the whole configuration, which would read values
  such as `http.<url>.extraHeader` that may hold a token.
- **Fields only in a `--remote` run, and the row's only on a queried row**;
  absent, never null, elsewhere. L-10 settles the first half; the second is
  this proposal's reading of it, since L-10 forbids null for "not
  applicable" and a row outside the query set was not asked. Rejected:
  `remote: null` on every row of every run, which would change the default
  document feature 005 builds; in a `--remote` run, `remote: null` outside
  the query set, as the first draft had, which would say "unknown" where
  nothing was asked (null keeps change 1's meaning, unknown or not
  established, CAS/pc:1128-1129); and a seventh state such as `not-queried`
  on every row, which would only restate the row's own `branch`, `head` and
  `merged_into_target`.
- **No effect on `completeness` or the exit.** The `remote` object carries its
  own `completeness`. Rejected: an `unknown` result making the run incomplete,
  which contradicts APO/ov:654-655, unmodified here, and would make every
  rate-limited `--remote` run exit 1.
- **No early stop** after a rate limit or a `gh` that needs authentication:
  each key is answered on its own. Rejected: stopping at the first, which
  saves at most 63 fast failures but makes which rows are answered depend on
  completion order, against APO/ov:244-246.
- **gh's own traffic off.** Each `gh` child runs with
  `GH_NO_UPDATE_NOTIFIER=1`, `GH_NO_EXTENSION_UPDATE_NOTIFIER=1`,
  `GH_PROMPT_DISABLED=1`, `GH_TELEMETRY=false` and `NO_COLOR=1` (gh 2.96.0's
  `gh help environment`), and without `GH_DEBUG`, `DEBUG`, `GH_HOST`,
  `GH_REPO`, `GH_FORCE_TTY` or `CLICOLOR_FORCE`, so that it sends nothing but
  the query, checks for no update and writes none of the state it keeps for
  that check, prompts for nothing, logs nothing and prints plain output; the
  new scenario of "Overview is local and read-only" asserts the first three.
  An addition: without it a `gh` child could send data other than the query,
  against DI:1038-1039's read-only boundary, or write a file, against that
  block's "no ... file write".

Departures, each naming what it departs from:

- **The merged-row wording** (C-5's example, "merged on GitHub by squash;
  local ancestry does not prove it; never retired"): GitHub's answer does not
  say how a pull request was merged, and a merge-commit merge not yet fetched
  gives the same picture, so the line names both causes and the number:
  "merged on GitHub as pull request #N; local ancestry does not prove it (a
  squash or rebase merge, or a merge target not fetched since); never retired
  on this evidence".
- **"exactly these fields"** (APO/ov:607-608) and the human layout
  (APO/ov:802-813) in a `--remote` run: read with APO/ov:655-658, "adding a
  field or an enum value is additive"; the fields and lines appear only in a
  `--remote` run, and without it the `remote` keys are absent, not null
  (L-4, L-10). The first draft's departure on `probes` (APO/ov:248-254) is
  gone: C-9 modifies that requirement instead.

Readings of packet text:

- **"It reads no credential files"** (DI:310) and "Use the normal GitHub
  client authentication path" (DI:1056-1057): under `--remote` the `gh`
  child reads gh's own credential store, as the second requires, and the
  `project` process reads none, as the first requires.
- **"each is recorded as unknown"** (DI:1053): as the row's
  `remote.state`, never as a row error or scan error, so change 2's completeness
  and exit rules stay as written.

## Corrections to the Packet

None.

## Open Questions

Each is before Brett Heap with a recommendation; the third is addressed to
lane openRepoProject-4 first.

1. **Enum closure (L-4).** Change 1 says "Enums SHALL be closed within a
   schema version" (CAS/pc:1129-1131); change 2 says "adding a field or an
   enum value is additive" (APO/ov:655-658). This change adds no value to any
   existing enum: it adds a row sub-record and an envelope object, in a
   `--remote` run only, whose own `state` enum is new and closed.
   Recommendation: the sub-records make the disagreement moot for this
   change; the overview keeps `schema_version: 1`, and the disagreement is
   settled where it bites, by a change that adds a value to an existing enum.
2. **The client and the non-Git default (C-4).** `gh api`, or direct HTTPS
   from `project`? Recommendation: `gh`. It is the packet's "normal GitHub
   client authentication path" (DI:1056-1057), so `project` never handles a
   token; direct HTTPS would have `project` read a token, against
   DI:1057-1058.
   And CAS/cmd:189 gives "Children other than Git" 15 s, where the packet
   gives each request 5 s: recommendation, the 5 s stands as the `gh` child's
   own limit within the overview, stated in this change's ADDED requirement,
   and change 1's 15 s stays the default for every other non-Git child, with
   `project-command` unmodified.
3. **Seams in feature 005 (to lane openRepoProject-4).** None is needed. The
   `--remote` flag is an argument error in feature 005 until this change's
   realization adds it; the `remote` fields, the remote phase after collection
   and the `gh` child's handle are all added by that realization, after 005
   lands; so is the `--remote` term of `probes.estimated`, while the
   remote-target reads enter `probes.performed` through the count feature
   005 already keeps of every Git child started. Recommendation: feature 005
   reserves no flag, field or hook.

## Questions Resolved by the Alignment Review

| Findings | Severity | Ruling | Section edited |
| --- | --- | --- | --- |

### Council Verdicts

| Concern | Severity | Verdict | Section changed |
| --- | --- | --- | --- |
