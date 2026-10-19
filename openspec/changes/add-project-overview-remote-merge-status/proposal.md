Lane: openRepoProject-5

# Proposal: add-project-overview-remote-merge-status

Status: draft; alignment review resolved on PR #29; council pending; nothing
here is ratified. Governing issue: opensoft/openRepoProject#25, claimed by lane
openRepoProject-5 (comment 6111242617); refs #6, the record of the project
maintenance design packet. Proposed on Brett Heap's word "usage reset, resume
all. read handoff and resume and fan out wide and do as much as possible in
parallel" (2026-10-11), read by lanes openRepoProject-4 and openRepoProject-5
as a go for the candidate list they put to him.

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
(CAS/cmd:90), is [E]. The lane's rulings are cited as L-1 to L-9 and C-1 to C-8
(2026-10-11), L-10 to L-15, B-14, C-9 and C-10 (2026-10-18), and L-16, L-17 and
C-11 to C-14 (2026-10-19). `PR19/cmd` is draft PR #19's
`openspec/changes/add-project-clean-all-safe/specs/project-command/spec.md` at
`c462d87`.

## Why

The overview change 2 defines, like `project clean`, judges merges by local
ancestry as of the last fetch (APO/ov:709-717; CAS/pc:5-9). A branch merged on
GitHub by squash generally does not put the branch tip into the merge target's
local ancestry (BA:195-199), so its worktree reads `pushed-unmerged`, or
`remote-gone` once GitHub deleted its branch, and nothing in either output says
why it is kept. The person has to open GitHub to learn that the work is merged.

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
  every Git child and does not bind the `gh` children of the ADDED requirement,
  which are started only with its argv and environment, what a `gh` child does
  beyond them being the GitHub client's own; every other clause holds for the
  `project` process and every Git child, its credential clause excepted; and in
  place of that clause the `project` process reads no credential file and no
  profile data the scan does not need, a `gh` child authenticates by the GitHub
  client's own means, reading what that client reads, and the overview reads,
  tests, infers, prints and forwards no credential value, the caller's
  environment excepted, which it passes to a `gh` child unread (C-7). The
  alignment review narrows the `gh` clause to what `project` starts and
  restores the packet's "infers" (QA-1, SA-11; C-13).
- **One addition to "Overview bounds its work and reports what it
  omitted"**, lane openRepoProject-4's fourth option (C-9). The remote-target
  reads are Git children, so `probes.performed` counts them as it counts every
  Git child started, and in a `--remote` run `probes.estimated` gains 1 per
  repository with a queried row and 1 more per such repository whose merge
  target names a usable remote, so that the reads add the same number to both
  counts. A remote-phase child that exits nonzero, reaches its limit or is
  stopped at the deadline is recorded in its rows' `remote`, never as a row or
  scan error. Without `--remote` both counts are change 2's, byte for byte; the
  `gh` requests are counted in `remote.requests` alone, and the `remote`
  object keeps no `probes` of its own, so a run has one count of Git
  children.
- **One sentence each in the Termination and Budgets paragraphs of change 1's
  evidence model**, on draft PR #19's text (C-11). A remote-target read that
  is stopped, reaped or abandoned is recorded in its rows' `remote`, never as
  a row's `probe-timeout`, and a `gh` child gets the ADDED requirement's
  limit, `min(5 s, remote budget remaining)`, in place of the 15 s that [E]
  keeps for children other than Git. Lane openRepoProject-2, the owner of
  change 1 and PR #19, reads the block's difference from PR #19's text before
  it is committed.
- **One paragraph in "Overview prints a versioned JSON envelope"** (C-12,
  L-11). In a run with `--remote`, the envelope's `remote`, after
  `scan_errors`, and each queried row's `remote`, after `classification`, are
  the only exceptions to its "exactly these fields, every one always present"
  (APO/ov:607-608); without `--remote` the document holds exactly change 2's
  fields. Lane openRepoProject-4, the owner of change 2, reads the block's
  difference from change 2's text before it is committed.

## Rules This Change Keeps

- **Remote evidence is never a removal proof** (DI:1059-1060; SY:224-225;
  HO:167). Local ancestry stays the cleanup gate: a merged pull request
  explains a kept row, never makes it removable, and `project clean` never sees
  it. Whether a local patch-equivalence proof may join local ancestry is change
  1's open question on squash-merged branches (CAS proposal.md:1001-1005),
  which the overview would inherit (APO proposal.md:901-902) and which this
  change neither decides nor forecloses.
- **Opt-in and read-only** (DI:1038-1039). A default overview opens no
  connection (APO/ov:710); a `--remote` run starts `gh` only with the fixed
  query and the switches that turn off its update check, prompts and telemetry,
  and `project` writes, mutates and keeps nothing (DI:1060, "Persistent remote
  caching is deferred"); what `gh` does beyond its documented switches is
  GitHub's (What This Repository Does Not Own).
- **Credentials are never touched** (DI:1056-1058). The `project` process
  reads, tests, infers, prints and forwards no credential value, the caller's
  environment excepted, which it passes to a `gh` child unread; `gh`
  authenticates by its own path, and a URL with embedded credentials is
  refused unprinted.
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
- **What a `gh` child reads, writes or sends beyond its argv and the switches
  `project` sets**: the GitHub client's own (`design.md`, Risks).
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
Line numbers are APO/ov's at `961c405`; for `project-command`, PR19/cmd's for
its one modified requirement and those of
`openspec/specs/project-command/spec.md` at `961c405` for the rest.

- `project-overview` (all twelve of change 2's requirements accounted for; it
  has no canonical spec until change 2 archives):
  - MODIFIED (`:166`):
    `### Requirement: Overview bounds its work and reports what it omitted`.
    Change 2's whole block and its thirteen scenarios stay untouched; one
    paragraph is added (C-9): in a `--remote` run the remote-target reads are
    Git children that `probes.performed` counts, `probes.estimated` gains 1
    per repository with a queried row and 1 more per such repository whose
    merge target names a usable remote, the `gh` children are counted in
    neither, and a remote-phase child that exits nonzero or is stopped at its
    limit or at the deadline is recorded in its rows' `remote`, never as a row
    or scan error; without `--remote` both counts stay as change 2 states
    them. Added scenario: in a complete run `estimated` equals `performed`
    with and without `--remote`, the `--remote` run's counts exceeding the
    other's by exactly the remote-target reads, and the `gh` request counted
    only in `remote.requests`.
  - MODIFIED (`:606`):
    `### Requirement: Overview prints a versioned JSON envelope`.
    Change 2's whole block and its six scenarios stay untouched; one paragraph
    is added (C-12, L-11): in a run with `--remote` the envelope also carries
    `remote`, after `scan_errors`, and each worktree row the ADDED requirement
    queries carries `remote`, after `classification`, the only exceptions to
    "exactly these fields, every one always present"; without `--remote` the
    document holds exactly the fields listed. Added scenario: a `--remote`
    run's document carries exactly the listed fields plus those two keys in
    those positions, and no other row has a `remote` key.
  - MODIFIED (`:709`):
    `### Requirement: Overview is local and read-only`.
    Change 2's whole block and its one scenario stay untouched; a second
    paragraph, in lane openRepoProject-4's wording, says that without
    `--remote` the requirement holds as written, and that with it the network
    clause still binds the `project` process and every Git child and does not
    bind the `gh` children of the ADDED requirement, which are started only
    with its argv and environment, every other clause holding for the `project`
    process and every Git child (no fetch, mutation or file write; nothing
    kept) but the credential clause, which is replaced by three clauses that
    pass the caller's environment to a `gh` child unread, and remote evidence
    labelled as live. Added scenario: a `--remote` run with a fake `gh` leaves
    the zero-mutation snapshots identical, opens no connection from `project`,
    sends only the fixed query, again on a second run, and every recorded
    `gh` environment sets `GH_NO_UPDATE_NOTIFIER=1`,
    `GH_NO_EXTENSION_UPDATE_NOTIFIER=1` and `GH_PROMPT_DISABLED=1`.
  - ADDED:
    `### Requirement: Overview reports remote merge evidence on request`.
    The opt-in; the query set; the remote target from the merge target's
    branch configuration and the identity rule; the dedupe key; the request,
    its argv and environment; the 64-request, four-at-once, 5 s, 30 s,
    one-page, 100-item and 1 MiB bounds; the explicit `unknown` and
    `unavailable` results with their reasons; cancellation on expiry; the row
    `remote` sub-record, on queried rows only, and the envelope `remote`
    object, each absent, never null, where it does not apply (L-10); the
    freshness sentence; isolation from every local result, a failed, cut or
    stopped remote-target read or `gh` child included, and from `project
    clean`; and the human lines. Thirteen scenarios.
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
  - Untouched (`:724`):
    `### Requirement: Overview reports default-branch health`
  - Untouched (`:761`):
    `### Requirement: Overview exits by completeness and severity`
  - Untouched (`:801`):
    `### Requirement: Overview renders a readable human report`
    (a `remote` line and a summary line added in a `--remote` run only)
- `project-command` (change 1's delta, unarchived, on canonical
  `openspec/specs/project-command/spec.md`):
  - MODIFIED (change 1's ADDED requirement, PR19/cmd `:90`):
    `### Requirement: Repository inspection requires Git 2.36 and shares one evidence model`.
    PR #19's whole block and its nine scenarios stay untouched; one sentence
    is added to Termination, so that a remote-target read stopped, reaped or
    abandoned is recorded in its rows' `remote`, never as a row's
    `probe-timeout`, and one to Budgets, so that a `gh` child gets the limit
    the ADDED requirement of `project-overview` gives it in place of the 15 s
    of "Children other than Git" (C-11). Added scenario: a held remote-target
    read records no `probe-timeout`, and a held `gh` child is stopped at 5 s,
    not 15 s.
  - Untouched (`:7`): `### Requirement: Delegate project creation`
  - Untouched (`:44`): `### Requirement: Inspect and diagnose` (change 1
    modifies it; this change does not)
  - Untouched (`:53`): `### Requirement: Explicit maintenance` (likewise)
  - Untouched (`:62`): `### Requirement: Distribution and compatibility`
  - Untouched (`:70`): `### Requirement: Creation question is asked only of a person choosing at the terminal`
  - Untouched (`:140`): `### Requirement: Creation question offers the Triad first`
  - Untouched (`:200`): `### Requirement: Known Triad obstacles are named before the question and refused on a Triad answer`
  - Untouched (`:265`): `### Requirement: A Triad answer asks for the organization and the visibility`
  - Untouched (`:324`): `### Requirement: Creation advisory follows a single repository created without the question`
  - Untouched (`:381`): `### Requirement: Creation offer precedes the workflow follow-up`
- `project-clean`, `project-clean-review-safety`, `project-review-safety`
  (change 2's MODIFIED "YAML decoding errors are structured refusals"
  included) and `speckit-extension-integration`: untouched.

In sum: three MODIFIED and one ADDED requirement in `project-overview`, 36
scenarios (14, 2, 7 and 13), and one MODIFIED requirement in `project-command`,
10 scenarios; 46 in all, nothing else.

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
  tests run with `python3 -m unittest discover -s tests -v`, and CI runs
  `python -m unittest discover -s tests -v` (`.github/workflows/tests.yml:17`)
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

- **Written on change 2's text (L-1, L-15).** The three `project-overview`
  MODIFIED blocks are change 2's "Overview bounds its work and reports what it
  omitted" (APO/ov:166-315), "Overview prints a versioned JSON envelope"
  (APO/ov:606-707) and "Overview is local and read-only" (APO/ov:709-722) as
  merged at `961c405`, which main still holds at `e9d6711` with change 2
  unarchived (2026-10-18), not `openspec/specs/`, which has no
  `project-overview` yet; main is not merged into this branch. `openspec
  validate --strict` passes while change 2 is unarchived; archive is the gate
  for the MODIFIED base. If change 2's text moves before it archives, these
  blocks re-align before this change is ratified, and any sentence lane
  openRepoProject-4 asks for comes as a follow-up commit.
- **Written on PR #19's text for change 1's evidence model (C-11, L-11).**
  The MODIFIED block of "Repository inspection requires Git 2.36 and shares
  one evidence model" in `specs/project-command/spec.md` carries that
  requirement whole as draft PR #19 (`c462d87`) rewrites it in change 1's
  `specs/project-command/spec.md` (PR19/cmd:90-255), with its nine scenarios,
  and adds one sentence to its Termination paragraph, one to its Budgets
  paragraph and one scenario. PR #19 is therefore a dependency: this change
  archives after change 1 archives with PR #19's text in it, and if PR #19
  closes unmerged, the block is re-based on change 1's text at main
  (CAS/cmd:90-214) before ratification. Lane openRepoProject-2, the owner of
  change 1 and PR #19, did not widen PR #19 before Brett Heap rules on it and
  holds the two clauses as its LQ-6 (2026-10-19); if Brett Heap has PR #19
  absorb them, this block is dropped and PR #19 stays a dependency. Lane
  openRepoProject-2 reads the block's difference from PR #19's text before it
  is committed.
- **Lane openRepoProject-4's agreement gated the spec text (C-7, C-9).**
  "Overview is local and read-only" and the ADDED requirement were committed
  after lane openRepoProject-4 read them (2026-10-11). Lane
  openRepoProject-4 agreed the block of "Overview bounds its work and reports
  what it omitted", its new scenario, and the ADDED requirement's edits for
  C-9 and L-10 on 2026-10-19, and they are committed with its fixes applied
  (Decisions, "Lane openRepoProject-4's check").
- **Two spec files are held for their owners (C-11 to C-13, L-17).** This
  proposal and `design.md` describe the spec text as the alignment review of
  2026-10-19 left it, which is written but not committed:
  `specs/project-command/spec.md`, the MODIFIED block of change 1's evidence
  model, held for lane openRepoProject-2 to read against PR #19's text; and the
  revised `specs/project-overview/spec.md`, with the MODIFIED block of
  "Overview prints a versioned JSON envelope" (C-12), the review's edits to the
  sentences lane openRepoProject-4 agreed (C-13) and its other spec edits, held
  for lane openRepoProject-4 to read against change 2's text and its own
  agreement. Until each lane agrees its diff, the committed
  `specs/project-overview/spec.md` is the text lane openRepoProject-4 agreed on
  2026-10-19 and no `specs/project-command/spec.md` is committed; a part lane
  openRepoProject-4 declines takes the review's Outcomes B to D (C-12, C-13).
- **Archives after change 2 (L-5).** Change 2 archives after change 1 and
  after feature 005 merges (APO design.md, Migration Plan 5); this change
  archives after change 2 archives. Its block of change 1's evidence model
  archives after change 1, which change 2 already follows, and after PR #19's
  text is in change 1.
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
  (issue #23) archives after it. This change shares one requirement with
  `add-project-clean-branch-retirement`, change 1's evidence model, which both
  modify on PR #19's text; by L-11, whichever of the two archives second
  re-bases its block on the other's archived block before it archives. It
  shares no requirement with `add-project-clean-cache-disposal`, depends on
  neither sibling, and never alters feature 004's or 005's order.
- **PR #19's other text.** At `c462d87`, still a draft on 2026-10-19, PR #19
  also exempts `clean`'s push child from [E]'s process groups, from its scrub
  of `GIT_ALLOW_PROTOCOL` and from its protocol pins, and keeps `clean`'s push
  and delete-branch children unbounded; this change's block carries that text
  unchanged and adds nothing about those children.
- **Harvest.** `09af8c8` is reference only: none of its `clean` or `doctor`
  behaviour returns. Its two open Copilot threads are answered here: the
  remote target "only from a checked-out target worktree" (3989411802) by
  C-3, and remote evidence "bypassed when the feature's own upstream was
  deleted" (3989411854) by C-6; doctor's non-goal thread (3989411958) is moot,
  doctor staying local. OV:179-180's "Each extension needs its own proposal
  that updates the governing cleanup specification first" does not bind here:
  `09af8c8`'s lookup moves out of `clean` into `project overview --remote`, and
  no cleanup specification changes, since `clean`, `status` and `doctor` stay
  local (C-1; CAS proposal.md:756-757, OQ-27).

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
PR #2's `project-clean-remote-merge-status` capability is not reused; only the
texts the opt-in contradicts are MODIFIED: "Overview is local and read-only",
"Overview bounds its work and reports what it omitted" for the probe count
(C-9), "Overview prints a versioned JSON envelope" for the two `remote` keys,
and change 1's "Repository inspection requires Git 2.36 and shares one evidence
model" for a stopped remote-target read and the `gh` child's limit (C-11), and
the new contract is ADDED under a name no change 2 requirement has), **L-4** (a
row sub-record and an envelope object stated in the ADDED requirement; no
stage, ladder or finding value; CAS/pc:1129-1131 and APO/ov:655-658 disagree on
enums; Open Questions), **L-5** (archive order), **L-6** (issue #25 and the
Status line), **L-7** (the feature number at `/speckit.specify`), **L-8** (the
flow: draft here, reviews by the lane) and **L-9** (no host-absolute path; the
bidi check).

From the addendum of 2026-10-18: **L-10** (the row `remote` and the envelope
`remote` are present only in a `--remote` run and absent, never null,
otherwise; the row's only on a queried row, Decisions below), **L-11** (a
contradiction of change 1's or change 2's text is settled in a MODIFIED block
of that requirement, never from the ADDED one or as a departure: C-9, C-11 and
C-12), **L-12** (CI is Linux only since PR #32: the `tests` workflow's `test
(3.10)` and `test (3.12)` on `ubuntu-latest`; no statement here rested on macOS
CI alone), **L-13** (commit trailers), **L-14** (the Status paragraph and tasks
1.2, after this change's first alignment review), **L-15** (written on change
2's text at main `e9d6711`, whose `openspec/` equals `961c405`'s; main is not
merged into this branch), and **C-9** and **C-10** below. From the addendum of
2026-10-19: **L-16** (a block of a requirement that draft PR #19 also amends is
written on PR #19's text, and this change archives after PR #19's amendment of
change 1 lands), **L-17** (change 1's evidence model, which this change and
`add-project-clean-branch-retirement` both modify: whichever archives second
re-bases its block on the other's archived block, and each block is held until
lane openRepoProject-2 has checked its diff), and **C-11** to **C-14** below.

Packet open decisions taken, each citing the text that leaves it open:

- **Scope, C-1** (DI:72-75 calls `project overview --remote` a possible later
  interface; DI:1483-1485, OV:357-358 and HO:47-50 leave the remote integration
  to its own decision, and nothing says whether `clean` or doctor gets it):
  `project overview --remote` only. Rejected: `09af8c8`'s queries from plain
  `clean` and `doctor`, against CAS/pc:5-9 and change 1's OQ-22 (CAS
  proposal.md:844-847).
- **The remote-tracking comparison, C-2** (not addressed by the packet): Out
  of Scope, recommended as its own change.
- **The remote target, C-3** (DI:1039-1042 asks for "a validated canonical
  GitHub remote" without naming which remote): the merge-target branch's
  `branch.<target>.remote` and `.merge`, never a worktree row's upstream or a
  checked-out target worktree; the identity accepted by PRS:32's rule.
- **The client and bounds, C-4** (DI:1056-1057, "Use the normal GitHub
  client authentication path", names no client): `gh api`, one child per
  request, under the packet's bounds verbatim; the 5 s is this child kind's own
  limit within the overview, which this change's MODIFIED block of [E] gives a
  `gh` child in place of CAS/cmd:189's "Children other than Git SHALL keep
  15 s." (C-11; Open Questions 2).
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
  lane openRepoProject-4 agreed on 2026-10-19: its sample sentence, "2 per
  distinct repository whose merge target's remote is read", is written as 1 per
  repository with a queried row plus 1 more where that first read names a
  usable remote, because a merge target that names no remote takes one read,
  not two, and a flat 2 would leave `estimated` above `performed` in a
  complete run, which the pinning scenario forbids; and the block also says
  that a remote-phase child that exits nonzero, reaches its limit or is
  stopped at the deadline is recorded in its rows' `remote`, never as a row
  or scan error, because once the reads are counted as that requirement's Git
  children its "its row recorded `probe-timeout`" and "recorded
  `deadline-exceeded`" (APO/ov:176-178) would otherwise make them row errors,
  against the ADDED requirement's isolation clause, and L-3 settles such a
  contradiction in the MODIFIED block, not from the ADDED one. Rejected: the
  first draft's own `remote.probes` beside the envelope's (two counts of Git
  children, and change 2's "every Git child" read as collection's alone).
- **CI, C-10**: L-12 applied to the proposal, design and tasks; every CI
  statement names the current matrix.
- **Change 1's evidence model, C-11** (the lane's ruling of 2026-10-19, after
  lane openRepoProject-2 declined to widen draft PR #19 before Brett Heap
  rules on it and recorded the two clauses as its LQ-6; L-11): the
  remote-target reads are [E]'s Git children, so [E]'s Termination sentence,
  "after which the child SHALL be abandoned and its row recorded
  `probe-timeout`" (PR19/cmd:189-192; CAS/cmd:177-180), and its Budgets
  sentence, "Children other than Git SHALL keep 15 s." (PR19/cmd:206;
  CAS/cmd:189), contradict this change, and L-11 settles each in a MODIFIED
  block of [E], not from the ADDED requirement. The block carries [E] whole on
  PR #19's text, with its nine scenarios, adds one sentence to each paragraph
  and one scenario, and lifts the extension brief's "no change to
  project-command" (C-11). Rejected: the general clauses put to lane
  openRepoProject-2 for PR #19 (a child whose output is no row's local
  evidence recorded where its requirement says; children whose requirement
  sets a shorter limit), which lane openRepoProject-2 holds as LQ-6 for Brett
  Heap; if he has PR #19 absorb them, this block is dropped.
- **Lane openRepoProject-4's check, 2026-10-19** (its check of the held spec
  against change 2's text at `961c405`, which found that the carve-out's
  "every other sentence" still bound a `gh` child to read no credential
  file, that "forward no credential value" conflicted with the environment
  passed to `gh`, and that a failed, cut or stopped remote-target read was
  only implied to leave the local result unchanged): lane openRepoProject-4
  agreed on 2026-10-19 with "YES to all three departures" and "Commit H with
  these fixes in place of c8a9f30's spec. That needs no further round with
  me: your bounds block and the three departures stand as agreed", and its
  fixes are applied in its wording. The three departures are: (1)
  `probes.estimated` counts 1 configuration read per repository with a queried
  row, plus 1 URL read only where that read names a usable remote, in place of
  C-9's sample "2 per distinct repository whose merge target's remote is read"
  (Decisions, C-9); (2) a remote-phase child that exits nonzero, reaches its
  limit or is stopped is recorded in its rows' `remote`, never as a row or scan
  error, departing from APO/ov:176-178's "its row recorded `probe-timeout`" and
  "recorded `deadline-exceeded`", which the MODIFIED block of "Overview bounds
  its work and reports what it omitted" now states, and from [E]'s Termination
  sentence (CAS/cmd:177-180; PR19/cmd:189-192), which this change's MODIFIED
  block of [E] now carries (C-11); and (3) in a `--remote` run a worktree row
  outside the query set carries no `remote` key, departing from L-10's C clause
  read alone, because L-10 also forbids null for "not applicable" (Decisions,
  "Fields only in a `--remote` run"). Its credential fix: in "Overview is local
  and read-only", every other clause holds in a `--remote` run, its credential
  clause excepted, and in place of that clause the `project` process reads no
  credential file and no profile data the scan does not need, a `gh` child
  reads what the GitHub client reads, and the caller's environment, `GH_TOKEN`
  included, passes to a `gh` child unread rather than counting as a forwarded
  credential value. Its three isolation fixes: the ADDED requirement's
  isolation sentence makes the failure, cut or stop of a remote-target read or
  of a `gh` child never a row error, a scan error or a finding, `probe-failed`,
  `probe-timeout` and `deadline-exceeded` notwithstanding, leaving every local
  result as it is without `--remote`; the block of "Overview bounds its work
  and reports what it omitted" names a child that exits nonzero beside one that
  reaches its limit or is stopped; and the ADDED requirement gains the scenario
  "A failed or held remote-target read stays unknown", its twelfth. Its two
  optional tightenings of "Probe counts in a remote run" are taken: the first
  repository's merge target tracks `refs/heads/main`, and the `--remote` run
  is one in which `remote.completeness` and the envelope's `completeness`
  are both `complete`. The isolation sentence's last clause, that a remote
  result is kept nowhere beyond the invocation and so is never a `project
  clean` input, stays, as a sentence of its own after lane openRepoProject-4's.
  That sentence names only "Overview bounds its work and reports what it
  omitted", which this change modifies. "Overview isolates one candidate's
  failure" is neither named nor modified: its table covers what is "Raised or
  observed while collecting one candidate" inside a boundary that ends at
  classification (APO/ov:318-326), and the remote-target reads run after
  collection (`design.md`, D1), so naming it would read as an ADDED requirement
  overriding a requirement of change 2 (L-11); lane openRepoProject-4 agreed to
  drop it on 2026-10-19.

Decisions where the sources and the rulings are silent:

- **The query set**: rows on a branch other than the merge target with a
  known head and `merged_into_target` false. Rejected: every row (spends
  requests on rows local ancestry already proves); only `pushed-unmerged` and
  `remote-gone` rows (misses a dirty or unpublished worktree whose branch was
  squash-merged). A row that local ancestry proves merged is `merged-removable`
  even when its upstream was deleted, under Brett Heap's ruling "yes, local
  ancestry proof outranks remote-gone, apply it" (2026-10-09; CAS
  proposal.md:811-813; APO proposal.md:896-900), so it is never queried; a
  `remote-gone` row is one that local ancestry does not prove.
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
- **`unavailable` beyond DI:1041-1042.** The packet makes a credential-bearing,
  malformed or non-GitHub remote `unavailable` with no request; this change
  gives the same state where no answer can come for want of a target or a
  client: `no-remote-target`, `gh-unavailable`, and `gh-unauthenticated` (sent,
  but gh's exit 4 says nothing can be answered without a login). Rejected:
  `unknown` for these, which would make `remote.completeness` `incomplete` on a
  machine without `gh` though nothing was cut.
- **Fields only in a `--remote` run, and the row's only on a queried row**;
  absent, never null, elsewhere. L-10 settles the first half; the second
  departs from L-10's C clause read alone, as lane openRepoProject-4 agreed on
  2026-10-19 (departure 3 of "Lane openRepoProject-4's check"), since L-10
  forbids null for "not applicable" and a row outside the query set was not
  asked. Rejected: `remote: null` on every row of every run, which would change
  the default document feature 005 builds; in a `--remote` run, `remote: null`
  outside the query set, as the first draft had, which would say "unknown"
  where nothing was asked (null keeps change 1's meaning, unknown or not
  established, CAS/pc:1128-1129); and a seventh state such as `not-queried`
  on every row, which would only restate the row's own `branch`, `head` and
  `merged_into_target`.
- **No effect on `completeness` or the exit.** The `remote` object carries its
  own `completeness`, and a remote result, or a failed, cut or stopped
  remote-target read or `gh` child, leaves the envelope's `completeness` and
  the exit status as they are without `--remote`. Rejected: an `unknown`
  result making the run incomplete, which contradicts APO/ov:654-655,
  unmodified here, and would make every rate-limited `--remote` run exit 1. An
  internal exception in the remote phase, which no reason records, exits 2, as
  change 2's "Overview exits by completeness and severity" (APO/ov:765-766)
  gives any exception outside the per-candidate boundary (C-14). Rejected:
  catching every exception as `api-error`, which contradicts that sentence of
  change 2 and would need a MODIFIED block (L-11).
- **No early stop** after a rate limit or a `gh` that needs authentication:
  each key is answered on its own. Rejected: stopping at the first, which
  saves at most 63 fast failures but makes which rows are answered depend on
  completion order, against APO/ov:243-246.
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

Readings of packet and ratified text:

- **"It reads no credential files"** (DI:310) and "Use the normal GitHub
  client authentication path" (DI:1056-1057): under `--remote` the `gh`
  child reads gh's own credential store, as the second requires, and the
  `project` process reads none, as the first requires.
- **"each is recorded as unknown"** (DI:1053): as the row's
  `remote.state`, never as a row error or scan error, so change 2's completeness
  and exit rules stay as written.
- **The human layout** (APO/ov:802-813) lists what each shown row prints and
  never says that no other line may be printed; the `remote` line and the
  summary's `Remote:` line, printed only in a `--remote` run, add to it without
  contradicting it, so it is not modified.

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
   own limit, stated in this change's ADDED requirement and carried into
   change 1's evidence model by this change's MODIFIED block of it (C-11,
   L-11), and change 1's 15 s stays the default for every other non-Git child.
   Lane openRepoProject-2 holds a general form of that clause for PR #19 as
   its LQ-6.
3. **Seams in feature 005 (to lane openRepoProject-4).** None is needed. The
   `--remote` flag is an argument error in feature 005 until this change's
   realization adds it; the `remote` fields, the remote phase after collection
   and the `gh` child's handle are all added by that realization, after 005
   lands; so is the `--remote` term of `probes.estimated`, while the
   remote-target reads enter `probes.performed` through the count feature
   005 already keeps of every Git child started. Recommendation: feature 005
   reserves no flag, field or hook.

## Questions Resolved by the Alignment Review

The alignment review (stack-architect and qa-lead) ran on `563d19d`
(2026-10-19); the lane's rulings of 2026-10-19 bind where they differ, and
the last five rows are the rulings that answered its five GAPs. Its
judgements of the writer's items (i) to (iv) are carried by SA-1, SA-6, SA-7
and QA-9. The spec edits are held for their owners' check: the
`project-command` delta for lane openRepoProject-2 and the `project-overview`
delta for lane openRepoProject-4 (Dependencies and Sequencing).

| Findings | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| SA-1: "local ancestry stays the only removal proof" presumes change 1's open question on squash-merged branches | MISMATCH | applied under C-13, as Appendix C carries it, with the final pass's HO:167 | held `project-overview` delta (Isolation); Rules This Change Keeps |
| SA-2: the `remote` keys outside [J]'s "exactly these fields" recorded as a departure, against L-11 | MISMATCH | applied with change under C-12: Appendix B and the final pass's corrections; the [H] reading moved to Readings; the Capabilities entry and a What Changes bullet for [J] are worded in this round | held `project-overview` delta (MODIFIED [J]); What Changes, Capabilities, Dependencies, Decisions (L-3, C-7), Departures, Readings; `design.md` Context, D8, D11 |
| SA-3: an abandoned remote-target read contradicts [E]'s Termination sentence | MISMATCH | overtaken by C-11: the interim bullet is not added, and SA-13 and SA-14 carry the ruling | as SA-13 and SA-14 |
| SA-4: the `gh` child's 5 s overrides [E]'s "Children other than Git SHALL keep 15 s." from an ADDED requirement | MISMATCH | overtaken by C-11: carried in the MODIFIED block of [E] (SA-13); Open Questions 2 replaced as Appendix D (f) gives | held `project-command` delta; Open Questions 2 |
| SA-5: an internal exception in the remote phase exits 2, against the Isolation paragraph's exit status | MISMATCH | applied with change under C-14 (option A): Appendix C, the proposal sentence and the D10 edit; the proposal names "Overview exits by completeness and severity" where the review wrote [X], a label only `design.md` defines | held `project-overview` delta (Isolation); Decisions ("No effect on `completeness` or the exit"); `design.md` D10 |
| SA-6: the notwithstanding list names "Overview isolates one candidate's failure", whose table ends at classification | DRIFT | applied with change: Appendix C; the proposal cites `design.md`, D1 where the review wrote D1 | held `project-overview` delta (Isolation); Decisions ("Lane openRepoProject-4's check") |
| SA-7: the three departures lane openRepoProject-4 agreed are not named | DRIFT | applied with change: departure (2) as the final pass words it under C-11; the list follows the sentence that holds the quote, so that sentence stays whole | Decisions ("Lane openRepoProject-4's check", "Fields only in a `--remote` run") |
| SA-8: OV:179-180's harvest rule is not addressed | DRIFT | applied | Dependencies and Sequencing (Harvest) |
| SA-9: `unavailable` reasons beyond DI:1041-1042 have no decision | DRIFT | applied | Decisions ("`unavailable` beyond DI:1041-1042") |
| SA-10: the query set's ruling is not cited, and a scenario title nearly repeats change 2's | DRIFT | applied, with the final pass's citation of CAS proposal.md:811-813 | Decisions (query set); held `project-overview` delta (scenario renamed); `design.md` D11 |
| SA-11: the credential clause drops the packet's "infers" | DRIFT | applied under C-13 | held `project-overview` delta ([L] paragraph); What Changes; Rules This Change Keeps |
| SA-12: three imprecise ranges and two wording drifts | DRIFT | applied | Why; Impact; Decisions (C-1, "No early stop"); `design.md` Context |
| SA-13: [E]'s Termination and Budgets sentences contradict this change, and L-11 needs a MODIFIED block | MISMATCH | applied under C-11: Appendix A exactly, with its added scenario; held for lane openRepoProject-2 | held `project-command` delta |
| SA-14: the proposal, design and tasks say `project-command` is untouched and PR #19 no dependency | DRIFT | applied with change: Appendix D (a) to (l) with G2 taken, 46 scenarios; 1.4 unticked as D (j) says, and 1.5 with it, since its two INFO lines need the held files; the citation key and the rulings paragraph also name L-11, L-14, L-16, L-17 and C-12 to C-14; C-4's bullet and tasks 2.2 and 2.3 follow C-11 and C-12 | citation key; What Changes; Capabilities; Dependencies and Sequencing; Decisions; Open Questions 2; `design.md` Context, D2, D7, D11; `tasks.md` 1.4, 1.5, 2.2 to 2.4, 3.4 |
| SA-15: [B]'s added paragraph departs from its own first paragraph without saying so | DRIFT | applied under C-13 | held `project-overview` delta ([B] paragraph) |
| SA-16: the design lists the identity pattern's forms incompletely | DRIFT | applied | `design.md` Context |
| QA-1: SHALLs bind the `gh` client's own behaviour, which no fake can observe | MISMATCH | applied with change under C-13: spec and design as written; the proposal keeps DI:1060 on the clause it supports; What Changes and Capabilities describe the narrowed clause, and What This Repository Does Not Own gains the entry the Rules sentence points to | held `project-overview` delta ([L] paragraph and scenario); What Changes; Rules; What This Repository Does Not Own; Capabilities; `design.md` D5 |
| QA-2: "No part of a response body" against the row's `number` and `url` | MISMATCH | applied, with the final pass's "No remote's URL" | held `project-overview` delta (Results, Remote target) |
| QA-3: `gh-unauthenticated` for any exit 4, against D6 | MISMATCH | applied | held `project-overview` delta (Results) |
| QA-4: "standard input closed" against D5's null device | MISMATCH | applied | held `project-overview` delta (Requests) |
| QA-5: no scenario for the precedence, the `url` check or the other human lines | GAP | applied, with the final pass's sixth row | held `project-overview` delta ("The chosen pull request and a rejected answer"); Capabilities; `design.md` D11 |
| QA-6: `observed_at` null is not pinned | GAP | applied; its optional half is carried by QA-13 and QA-14, as the final pass says | held `project-overview` delta ("No gh, or a gh without authentication") |
| QA-7: `reason` and `counts` are not closed | GAP | applied | held `project-overview` delta (Fields) |
| QA-8: the determinism sentence covers a timestamp | MISMATCH | applied | held `project-overview` delta (Results) |
| QA-9: no test seam fails a remote-target read | GAP | applied, with the final pass's extension for SA-13's scenario | `design.md` D11 |
| QA-10: `head_sha` for rows never asked | MISMATCH | applied | held `project-overview` delta (Fields) |
| QA-11: "stay equal in a complete run" claims more than change 2 gives | MISMATCH | applied | What Changes; `design.md` D2 |
| QA-12: a merge target without `branch.<target>.merge` has no upstream | MISMATCH | applied with change: the scenario's added clause follows the URL clause, so that "whose URL" still names `upstream`'s | held `project-overview` delta (Remote target; "The remote target comes from the merge target's branch configuration"); `design.md` Context, D2 |
| QA-13: the line between `rate-limited` and `forbidden` is left to D6 | GAP | applied (Appendix E) | held `project-overview` delta (Results; "API failures stay unknown"); `design.md` D11 |
| QA-14: the response rules live in D6 alone | GAP | applied (Appendix E) | held `project-overview` delta (Results; "API failures stay unknown") |
| QA-15: the forbidden switches and "read-only" are not named | GAP | applied | held `project-overview` delta (Requests; "The request bounds") |
| QA-16: no scenario stops a read at the deadline or cancels an unread target | GAP | applied | held `project-overview` delta ("Expiry cancels queued and in-flight requests") |
| QA-17: "Every queried row ... SHALL be `unavailable`" reads unconditionally | MISMATCH | applied | held `project-overview` delta (Remote target) |
| QA-18: two kinds of URL refusal are unnamed | MISMATCH | applied | held `project-overview` delta (Remote target) |
| QA-19: `"detached"` and a null `merged_into_target` | GAP | applied | held `project-overview` delta (Query set; "One request per exact head") |
| QA-20: `schema_version` and the key positions | GAP | applied, its first sentence only, since C-12 takes G2 | held `project-overview` delta (Fields) |
| QA-21: the `Remote:` line and where the `remote` line goes | GAP | applied (Appendix E) | held `project-overview` delta (Human report) |
| QA-22: the reads' directory, caps and "no fallback to `origin`" are in the design only | GAP | applied (Appendix E) | held `project-overview` delta (Remote target; "Remotes that give no request") |
| QA-23: no `PATH` lookup and the `oid` check are in the design only | GAP | applied (Appendix E) | held `project-overview` delta (opening paragraph; Requests) |
| QA-24: whose merge ref, and the case of the base repository | GAP | applied, its optional AND taken | held `project-overview` delta (Results; "One request per exact head") |
| QA-25: no scenario for the determinism sentence (optional) | GAP | applied with change: QA-8's "`remote.observed_at` apart" added, since `observed_at` is a timestamp and differs between the two runs | held `project-overview` delta ("The request bounds") |
| QA-26: `--remote` with `--attention` is not exercised (optional) | GAP | applied | held `project-overview` delta ("A squash-merged branch is explained and kept") |
| QA-27: D6's "stopped" entry also covers the body and header stops | MISMATCH | applied | `design.md` D6 |
| QA-28: the Risk's fallback changes [B]'s count | MISMATCH | applied | `design.md` Risks |
| QA-29: the central case had no recorded check | GAP | applied (Appendix E), recording G4 | `design.md` Context, Risks |
| C-11 (G1; SA-3, SA-4): change 1's evidence model | GAP | ruling: MODIFY it whole on PR #19's text with two clauses and one scenario (Appendix A), held for lane openRepoProject-2; this change archives after PR #19's amendment of change 1 lands (L-16) and re-bases on `add-project-clean-branch-retirement`'s archived block if that change archives first (L-17) | held `project-command` delta; What Changes; Capabilities; Dependencies and Sequencing; Decisions; Open Questions 2; `design.md`; `tasks.md` 1.4, 2.4, 3.4 |
| C-12 (G2; SA-2): "exactly these fields" | GAP | ruling: MODIFY change 2's "Overview prints a versioned JSON envelope" (Appendix B), held for lane openRepoProject-4; if it declines, the review's Outcome B | held `project-overview` delta; as SA-2 |
| C-13 (G3): the sentences lane openRepoProject-4 agreed | GAP | ruling: QA-1 and SA-11 at spec.md:13-27, SA-15 at :129-142 and Appendix C at :328-342 applied and sent to lane openRepoProject-4 in one diff with C-12's block; if it declines a part, the review's Outcomes B to D, and SA-1 to Brett Heap | held `project-overview` delta; Dependencies and Sequencing |
| G4 (lane openRepoProject-3's L4): the association for a squash-merged head | GAP | ruling: answered live on #31 and #17 and recorded with its limits (QA-29); D5's query and the scope of Open Questions 2 stand | `design.md` Context, Risks |
| C-14 (G5; SA-5): the exit status of an internal remote-phase exception | GAP | ruling: option A, Appendix C, with no MODIFIED block of "Overview exits by completeness and severity" | as SA-5 |

### Council Verdicts

| Concern | Severity | Verdict | Section changed |
| --- | --- | --- | --- |
