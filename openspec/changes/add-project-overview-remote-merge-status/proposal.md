Lane: openRepoProject-5

# Proposal: add-project-overview-remote-merge-status

Status: draft; alignment review and council resolved on PR #29, round C4's
spec edits committed on lane openRepoProject-4's agreement of 2026-10-20;
round C5's edits for lane openRepoProject-3's delta read and Codex's findings
on `e198548` (C-24 to C-29) applied, their `project-overview` spec edits
committed on lane openRepoProject-4's agreement of 2026-10-20; round C6's
edits for Codex's finding on `67e43ae`, three points found in applying it
and lane openRepoProject-3's folded read of `e198548..67e43ae` (C-30 to C-34)
applied, their `project-overview` spec edits committed on lane
openRepoProject-4's agreement of 2026-10-20, and C-35, lane
openRepoProject-3's narrowing of the per-directory rule of the lookup of
`gh`, applied in `design.md` alone, with no spec edit; ratification
by Brett Heap pending; nothing here is ratified. Governing issue:
opensoft/openRepoProject#25, claimed by lane openRepoProject-5 (comment
6111242617); refs #6, the record of the project
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
(2026-10-11), L-10 to L-15, B-14, C-9 and C-10 (2026-10-18), L-16, L-17 and
C-11 to C-14 (2026-10-19), and F-3 and C-15 to C-35 (2026-10-20, C-16 to C-22
being the council's verdicts). `PR19/cmd` is draft PR #19's
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
and local ancestry the cleanup gate (DI:1059-1060). Change 2 leaves exactly
this to "a remote-queries proposal" (APO proposal.md:566-568, :810-812), and
the packet keeps remote queries a separately governed extension (HO:47-50;
OV:142-146; CAS proposal.md:756-757, OQ-27). This is that proposal. The
closed PR #2's `09af8c8` is the harvest source, for reference only: it
queried GitHub from plain `clean` and `doctor` with no opt-in and no bounds,
put the answer inside the revalidation signature and added ladder classes.

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
  is one `gh api` child, started by the absolute path that the run's one
  lookup found in an absolute directory of `PATH` (C-22), with a fixed
  read-only GraphQL query for the queried repository's `nameWithOwner` and at
  most 100 pull requests associated with that commit, one page, never
  paginated or cached. At most 64 requests, four at once, each `min(5 s,
  remote time remaining)`, inside a 30 s remote budget, counted from the
  first request after collection, that is part of the 60 s deadline, not
  added to it; at most 1 MiB of each body kept, one byte more read to tell a
  longer body (DI:1045-1051; C-4, C-27). On expiry,
  requests within the cap not yet sent are `unknown` with `cancelled` and
  requests in flight are stopped and `unknown` with `aborted` (DI:1051-1053),
  while a key past the 64th stays `request-cap` (C-28).
- **Explicit results.** A row's `remote` is `{state, number, url, head_sha,
  reason}` with `state` `merged`, `open`, `not-found`, `unavailable` or
  `unknown`, from pull requests whose head is exactly the row's head and whose
  base is the merge target's remote branch in the repository that GitHub
  resolves for the identity (C-5, C-19). A pull request closed without merging
  has no state of its own: GitHub's commit association does not return one
  (F-3), so such a head reads `not-found`, whose text names only merged and
  open pull requests (C-16). A further page, a body cut at 1 MiB, a timeout, a
  401, a 403, a rate limit, a body that cannot be parsed or any other failure
  is `unknown` with its reason, never a partial answer, and no other response
  text, `gh` error output or credential appears in either output
  (DI:1055-1058). No `gh` in an absolute directory of `PATH`, a lookup of it
  that fails or runs out of time, or a `gh` that needs authentication, is
  `unavailable`, and when no request can be sent or answered for one of
  these, so are the keys past the 64th, never `request-cap` (C-25, C-26).
- **Evidence, never permission.** Remote evidence changes no classification,
  finding, suggestion, gate, row status, summary count, `completeness` or exit
  status, and is kept nowhere beyond the invocation, so it can never feed a
  `project clean` eligibility gate, `plan_digest` or revalidation (DI:1059-1060;
  SY:129-130; HO:167). No finding code, ladder class or stage value is added
  (L-4).
- **What the person sees.** Under a kept worktree's finding a `remote` line
  says, for a merged one (C-18, C-20), "merged on GitHub as pull request #N at
  this exact head; uncommitted and ignored files here are not part of it;
  local ancestry does not prove it (a squash or rebase merge, or a local merge
  target not brought up to date since); never retired on this evidence"; one
  summary line gives the `gh` requests started, the counts by state and the
  sentence (C-17) "Remote evidence, where GitHub answered, was read live from
  github.com and may already be stale; it never authorizes cleanup."
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
  environment excepted, which it passes to a `gh` child unread (C-7), and a
  remote's URL excepted, which it holds in memory only while it derives the
  `owner/repository` and detects the URL's user information, the read's
  standard error being discarded unexamined; after that no part of the user
  information is retained or compared, none is ever printed, logged, sent or
  used to authenticate, and the URL is never forwarded with it (C-30, C-31).
  The alignment review narrows the `gh` clause to what `project` starts and
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
  change 1 and PR #19, agreed the block on 2026-10-19 with one fix to the
  Termination sentence, and it is committed.
- **One paragraph in "Overview prints a versioned JSON envelope"** (C-12,
  L-11). In a run with `--remote`, the envelope's `remote`, after
  `scan_errors`, and each queried row's `remote`, after `classification`, are
  the only exceptions to its "exactly these fields, every one always present"
  (APO/ov:607-608); without `--remote` the document holds exactly change 2's
  fields. Lane openRepoProject-4, the owner of change 2, agreed the block on
  2026-10-19 with two wording fixes in the Isolation passage of the ADDED
  requirement, and it is committed.

## Rules This Change Keeps

- **Remote evidence is never a removal proof** (DI:1059-1060; SY:224-225;
  HO:167). Local ancestry stays the cleanup gate: a merged pull request
  explains a kept row, never makes it removable, and `project clean` never sees
  it. Whether a local patch-equivalence proof may join local ancestry is change
  1's open question on squash-merged branches (CAS proposal.md:1001-1005),
  which the overview would inherit (APO proposal.md:901-902) and which this
  change neither decides nor forecloses. This change's `merged` is explanation
  measured only as `design.md`'s tool facts and Risks state; a ruling on that
  question that admitted remote merge evidence would need its own
  verification, never this change's states (C-21).
- **Opt-in and read-only** (DI:1038-1039). A default overview opens no
  connection (APO/ov:710); a `--remote` run starts `gh` only with the fixed
  query and the switches that turn off its update check, prompts and telemetry,
  and `project` writes, mutates and keeps nothing (DI:1060, "Persistent remote
  caching is deferred"); what `gh` does beyond its documented switches is
  GitHub's (What This Repository Does Not Own).
- **Credentials are never kept, shown or used by `project`** (DI:1056-1058).
  The `project` process reads, tests, infers, prints and forwards no
  credential value, the caller's environment excepted, which it passes to a
  `gh` child unread, and a remote's URL excepted, which it holds in memory
  only while it derives the `owner/repository` and detects the URL's user
  information, discarding unexamined what the read writes to standard error,
  keeping and comparing no part of the user information afterwards, never
  printing, logging, sending or authenticating with any of it, and never
  forwarding the URL with it (C-30, C-31); `gh` authenticates by its own path,
  and a URL with embedded credentials is refused unprinted.
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
    pass the caller's environment to a `gh` child unread and bound the
    in-memory inspection of a remote's URL to deriving the `owner/repository`
    and detecting its user information, the read's standard error discarded
    unexamined (C-30, C-31), and remote evidence labelled as live. Added
    scenario: a `--remote` run with a fake `gh` leaves
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
  children at once through the overview's control loop, each started by the
  absolute path of the `gh` found in `PATH`'s absolute directories (C-22),
  reads their bounded output, and adds the `remote` fields and lines. No other
  subcommand changes. No new dependency: `gh` is optional at run time, its
  absence giving `unavailable`, and nothing is imported. `probe()`
  (`project:60-65`, one child, 15 s, no process group) is not used for `gh`.
- **`README.md`**: the overview section gains `--remote`: what it asks, that
  it needs an authenticated `gh`, its bounds, what `unknown` and `unavailable`
  mean, that the answer is live, and that it never authorizes cleanup, and
  what the person can do next: for a `merged` row, bring the local merge
  target up to date and run the overview again, after which local ancestry
  decides a merge-commit merge; a squash-merged row stays kept, and whether a
  local patch-equivalence proof may ever retire it is change 1's open question
  on squash-merged branches (CAS proposal.md:1001-1005); for `gh-unavailable`,
  install `gh`, or check that `PATH`'s directories are reachable (C-26); for
  `gh-unauthenticated`, run `gh auth login`; for
  `no-remote-target`, give the merge target an upstream (for example
  `git branch --set-upstream-to=origin/main main`); for
  `credential-bearing-remote`, take the credential out of the remote's URL;
  for `malformed-remote`, give the remote a URL that names an
  `owner/repository` on `github.com`, with no user but `git` and no port; and
  for `not-github`, nothing, since only `github.com` is queried (C-18). These
  next steps are advice, not a `suggested_command`. It also says that a merge
  target which tracks the person's own fork asks about the fork, so every
  queried row reads `not-found` (C-21).
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
  archives after PR #19's amendment lands or, if PR #19 closes, after the
  block is re-based on change 1's text (tasks 2.4); if PR #19 closes unmerged
  before ratification, that re-base is made first, on change 1's text at main
  (CAS/cmd:90-231). Lane openRepoProject-2, the owner of
  change 1 and PR #19, did not widen PR #19 before Brett Heap rules on it and
  holds the two clauses as its LQ-6 (2026-10-19); if Brett Heap has PR #19
  absorb them, this block is dropped and PR #19 stays a dependency. Lane
  openRepoProject-2 agreed the block on 2026-10-19 with one fix to the
  Termination sentence, and it is committed. Ratifying this change ratifies its
  block of [E] only for its two added sentences and its added scenario, as
  written on PR #19's text at `c462d87`; PR #19's own sentences stay PR #19's
  to ratify (lane openRepoProject-3's re-read, MEDIUM-1).
- **Lane openRepoProject-4's agreement gated the spec text (C-7, C-9).**
  "Overview is local and read-only" and the ADDED requirement were committed
  after lane openRepoProject-4 read them (2026-10-11). Lane
  openRepoProject-4 agreed the block of "Overview bounds its work and reports
  what it omitted", its new scenario, and the ADDED requirement's edits for
  C-9 and L-10 on 2026-10-19, and they are committed with its fixes applied
  (Decisions, "Lane openRepoProject-4's check").
- **Both spec files were agreed by their owners and committed in round C3
  (C-11 to C-13, L-17).** `specs/project-command/spec.md`, the MODIFIED block
  of change 1's evidence model, was agreed by lane openRepoProject-2 on
  2026-10-19 with one fix to its Termination sentence. The revised
  `specs/project-overview/spec.md`, with the MODIFIED block of "Overview prints
  a versioned JSON envelope" (C-12), the review's edits to the sentences lane
  openRepoProject-4 agreed (C-13) and its other spec edits, was agreed by lane
  openRepoProject-4 on 2026-10-19 with two wording fixes in the Isolation
  passage of the ADDED requirement. Both files are committed, and no part was
  declined, so the review's Outcomes B to D are not taken (C-12, C-13).
- **Round C4's spec edits were agreed by lane openRepoProject-4 and are
  committed (the council verdicts' "Held text").** The council's edits (C-16
  to C-22) and lane openRepoProject-3's LOWs 5, 6 and 10, all in the ADDED
  requirement of `specs/project-overview/spec.md`, were held in one diff for
  lane openRepoProject-4, which answered on 2026-10-20: "yes, lane 4 agrees
  to #29's held-C4 overview file (sha256 6deab04e399c4fe9..., the same bytes I
  read in py-bench), with nothing declined". It byte-checked the three
  MODIFIED blocks against `621715a` and found them equal, only the ADDED
  requirement having changed, and the file is committed exactly as held
  (`d73d25d`). `specs/project-command/spec.md` is unchanged in this round:
  [E]'s Termination paragraph binds Git children, so the ADDED requirement,
  which starts the `gh` children, says that they are stopped on every exit
  path (LOW-6), and nothing was held for lane openRepoProject-2.
- **Round C5's spec edits were agreed by lane openRepoProject-4 and are
  committed (C-24 to C-29).** One sentence added to the added paragraph of
  "Overview bounds its work and reports what it omitted", naming the lookup of
  `gh` beside the remote-target reads and the `gh` children (C-26, L-11); in
  the ADDED requirement, the request cap's precedence (C-25) and its hold at
  an expiry (C-28), the lookup that fails or runs out of time (C-26), the
  sentinel byte past 1 MiB of body and past 64 KiB of status and headers
  (C-27) and past 64 KiB of each remote-target read's output (C-29), and the
  lookup in the isolation clause (C-26); and five ANDs, which change no count:
  two on "No gh, or a gh without authentication" (lane openRepoProject-3's F3;
  C-26), one on "The chosen pull request and a rejected answer" (F4), one on
  "The request bounds" (C-25) and one on "Expiry cancels queued and in-flight
  requests" (C-28). They were held in one file for lane openRepoProject-4,
  which agreed on 2026-10-20. Its NOTED, `lanes/log/openRepoProject-4.md:70`
  on the register's `origin/main`, added in `7835b98be` and unchanged at
  `85f9c2648`, reads "YES to lane 5's held C5 overview spec for #29
  (opensoft/openRepoProject#25), sha256 3b4a7b0e39b19c74 (#29 at 8fed841;
  register copy 8d1209cb9 byte-equal). Byte-checked: [J] and [L] identical to
  the C4 text lane 4 agreed (d73d25d, 6deab04e); [B] adds one sentence inside
  its --remote paragraph" and, further on, "Nothing declined." The held file's
  full sha256, lane openRepoProject-5's own record, is
  3b4a7b0e39b19c74205df9631a7a404475f6bc436aa3675570695b2990796251, and the
  file is committed exactly as held (`6fe8a5e`).
  `specs/project-command/spec.md` is unchanged in this round, and nothing was
  held for lane openRepoProject-2.
- **Round C6's spec edits were agreed by lane openRepoProject-4 and are
  committed (C-30 to C-34).** In the second paragraph of "Overview is local
  and read-only", the clause that replaces the credential clause names a remote's
  URL beside the caller's environment as its second exception, and three
  sentences bound it (Codex's P2 on `67e43ae`, spec.md:27): the URL a
  remote-target read prints on standard output is held in memory only while
  the overview derives the `owner/repository` and detects its user
  information, which it tests only as the ADDED requirement's
  `credential-bearing-remote` and `malformed-remote` reasons state; after that
  no part of the user information is retained or compared, none is ever
  printed, logged, sent or used to authenticate, and the URL is never
  forwarded with it (C-30); and the read's standard error is drained and
  discarded unexamined (C-31). In the ADDED requirement, the Remote target
  paragraph says "drained and discarded unexamined" too (C-31); the AND of
  "Remotes that give no request" names the URL's user part beside `s3cr3t`
  (C-32), that part being the token `u9zq-kx7w` in its WHEN and its AND
  (C-33); and the Requests paragraph drops the gloss "`request-cap` applies
  only when requests can be sent and the cap stops them", false for a lookup
  that the deadline cuts, since its expiry sentence and the Results paragraph
  state the whole order alone (lane openRepoProject-3's folded read, L4;
  C-34). No scenario is added and no count changes. The second paragraph is in
  the block lane openRepoProject-4 agreed, so the whole file was held for it
  to read against its agreement of 2026-10-20, and it answered the same day.
  Its NOTED, `lanes/log/openRepoProject-4.md:79` on the register's
  `origin/main`, added in brett-wip `18d493381` and unchanged at `bfef1f515`,
  reads "YES to lane 5's held C6 overview spec for #29
  (opensoft/openRepoProject#25), sha256
  2ecd3d72b7cd32595d12f66206b7dd3c71df2cdfb9430122dd1ab0414ff1fe3e (#29 at
  dd2306a, whose committed spec is the C5 file 3b4a7b0e). Byte-checked: [B]
  and [J] identical to the committed file; [L] adds only to change 2's text at
  main (+33/-0), every change inside #25's --remote paragraph (a remote's URL
  excepted from the credential clause within stated bounds: held in memory
  only to derive owner/repository and detect user information, never retained,
  compared, printed, logged, sent or used to authenticate, never forwarded
  with it; the read's standard error drained and discarded unexamined); [R]'s
  three hunks are C-31, C-34 and C-32/C-33; one ADDED requirement, no other
  MODIFIED block. Nothing declined." The held file's sha256 is the one it
  names, 2ecd3d72b7cd32595d12f66206b7dd3c71df2cdfb9430122dd1ab0414ff1fe3e, and
  the file is committed exactly as held, alone (`233df0b`).
  `specs/project-command/spec.md` is unchanged in this round, and nothing was
  held for lane openRepoProject-2.
- **Archives after change 2 (L-5).** Change 2 archives after change 1 and
  after feature 005 merges (APO design.md, Migration Plan 5); this change
  archives after change 2 archives. Its block of change 1's evidence model
  archives after change 1, which change 2 already follows, and after PR #19's
  amendment lands or, if PR #19 closes, after the block is re-based on change
  1's text (tasks 2.4).
- **Realized after feature 005 (lane openRepoProject-4's terms).** Feature 005
  is specified from change 2 as ratified, local only, with no `--remote`, and
  does not anticipate this change. This change edits none of change 2's files
  and nothing of feature 005; what its realization needs from 005's code was
  Open Questions 3, which lane openRepoProject-4 answered on 2026-10-20
  (C-23): feature 005 reserves no flag, field or hook for `--remote`, as its
  spec records in its Dependencies (`specs/005-project-overview/spec.md` on
  `005-project-overview` at `282a20e`). Lane openRepoProject-4 also flagged
  feature 005's pending Q16 (`specs/005-project-overview/clarify-questions.md`
  on `005-project-overview` at `4ba9faa`): change 2's design D1 and
  clarifications N1 start each child with SIGINT, SIGTERM and SIGHUP blocked
  (APO design.md:115-119; APO clarifications.md:45-46), and its
  recommendation B amends both to start children unblocked under handlers
  that only record the signal, where its option A would instead record a
  departure from them on Brett Heap's word; `gh` children follow whatever D1
  and N1 say, or the departure from them that feature 005 records, and if
  feature 005's Q16 amends, or records a departure from, change 2's design D1
  or clarifications N1 before change 2 archives, task 2.3's re-read picks it
  up, `design.md` D7's spawning sentence and the scenario "Expiry cancels
  queued and in-flight requests", whose process exits within 64 s, included
  (lane openRepoProject-3's delta read, F2; C-24).
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
- **Closed pull requests** (C-16): a head-branch lookup matched by exact
  `headRefOid` (S-1's option), recommended as its own follow-on change if
  Brett Heap wants a `closed` state, once F-3's unchecked cases are checked
  live: a fork's pull request whose head branch name collides, a reused branch
  name, a rebase merge, a pull request of more than one commit whose head
  moved after it closed, and a name with more than one page of pull requests.
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
lane openRepoProject-2 has checked its diff, which it did for this change's
block on 2026-10-19, with one fix), and **C-11** to **C-14** below. From the
rulings and council verdicts of 2026-10-20: **F-3** (the lead's live check
that GitHub's commit association returns no pull request closed without
merging), **C-15** (the council's inputs), **C-16** to **C-22** (the council's
verdicts, below), **C-23** (Open Questions 3), **C-24** to **C-29** (round
C5: lane openRepoProject-3's delta read of `e198548`, Codex's three findings
on it and two points found in applying them; Decisions and Readings below,
and "Re-read and Codex Findings (round C5)"), **C-30** to **C-34** (round
C6: Codex's finding on `67e43ae`, the bounded inspection of a remote's URL,
three points found in applying it, and lane openRepoProject-3's folded read
of `e198548..67e43ae`; Decisions and Readings below, and "Re-read and Codex
Findings (round C6)") and **C-35** (the lookup of `gh`'s per-directory rule,
lane openRepoProject-3's narrowing, applied in `design.md` alone; "Re-read and
Codex Findings (round C6)").

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
  what is in flight, each `unknown`; a key past the 64-request cap is no
  queued request, since the cap decides before any request whether a key is
  sent, so it stays `request-cap` at an expiry, and only keys within the cap
  are `cancelled` or `aborted` (C-28).
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
  Heap; if he has PR #19 absorb them, this block is dropped. Lane
  openRepoProject-2 agreed the block on 2026-10-19 with one fix: in the added
  Termination sentence, "as a probe child past its budget is above" replaces
  "in the same way", which, coming right after the push-child sentence, would
  read as the push child's treatment, and the push child is never signalled.
  The Budgets clause and the added scenario stand as written, and the block is
  committed.
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
  drop it on 2026-10-19. Lane openRepoProject-4 then agreed the revised
  `project-overview` file as a whole, C-12's block and C-13's edits, on
  2026-10-19, answering "yes ... (C-12 and C-13), with two wording fixes in the
  Isolation passage", and the file is committed with both fixes: the carve-out
  for an exception that the remote phase raises and this requirement records as
  none of its reasons now opens the first isolation sentence ("Unless the
  remote phase raises an exception that this requirement records as none of its
  reasons, a `--remote` run and the same run without it SHALL agree ...") in
  place of closing it with "except when", and the last sentence is two: "A
  remote result SHALL be kept nowhere beyond the invocation, so it can never be
  a `project clean` eligibility, `plan_digest` or revalidation input" and
  "Remote evidence SHALL never be a removal proof".
- **Closed pull requests, C-16** (DI:1036-1060 names "a merged pull request"
  (DI:1059-1060) and no other pull-request state; C-5 listed `closed`):
  `closed` is
  dropped, a departure named under Departures ("No `closed` state"), and the
  head-branch lookup that S-1 proposed is a follow-on (Out of Scope).
- **The freshness sentence and the count, C-17** (C-5 asks for a staleness
  sentence; the packet gives no wording): `freshness` stays one constant,
  "Remote evidence, where GitHub answered, was read live from github.com and
  may already be stale; it never authorizes cleanup.", true in every run,
  one with no `gh`, with no usable remote, with every worktree merged or with
  a `gh` that exits 4 before it connects included; and the `Remote:` line
  counts the `gh` requests started, which is all `project` knows. Rejected:
  "queried live from github.com" (the first draft), false in those runs
  (Codex's third finding); a second sentence chosen when `observed_at` is
  null (S-3), still false for a `gh` that exits 4 after `observed_at` is set;
  and "requests to github.com", which counts children that never reached it.
- **The `merged` line, C-18 and C-20** (C-5's example): the line names the
  exact head, says that the worktree's uncommitted and ignored files are not
  part of the pull request, since a row kept for its files is queried like
  any other, and names the remedy that works, a local merge target brought up
  to date, since a fetch moves only its remote-tracking ref (APO/ov:358-365);
  the README gives the next steps (Impact). See Departures, "The merged-row
  wording".
- **The live contract check and the resolved repository, C-19 and C-21** (G4
  and F-3 checked answers, not `gh`'s output under D5's argv): `tasks.md` 2.5
  runs D5's exact argv once by hand before the Speckit handoff and records in
  `design.md`'s tool facts the status line, the header names as `gh` prints
  them and an answer for each state and case it names, and a state or case
  with no live answer is dropped or re-specified first; header names compare
  without case, as HTTP defines them; and a pull request's base repository is
  matched against the `nameWithOwner` that the same answer gives for the
  queried repository, the repository GitHub resolved, so a renamed remote
  gets its real answer (Decisions, "Matching").
- **Parser failures and which `gh` runs, C-22** (DI:1055-1056: any "other API
  failure" is an explicit unknown): a body that cannot be decoded or parsed,
  for any cause, its nesting depth and the size of its integers included, is
  `api-error`, so it never reaches C-14's exit 2; and `gh` is looked up once
  per run in the absolute directories of `PATH` only, an empty or relative
  entry skipped, and each child is started by the absolute path found, so a
  `gh` planted in the caller's working directory never receives the caller's
  `GH_TOKEN` (the council's adversary-engineer showed both by offline
  fixtures; `design.md`, D5 and D6).
- **Run-wide unavailability, C-25 and C-26** (DI:1045 caps the requests at 64
  and DI:1041-1042 makes an unusable remote `unavailable`, and neither says
  which a key past the cap takes when no request can be sent; DI:1055-1056
  names no outcome for a lookup of the client that fails): with no `gh`
  found, or when each request that the cap allows ends in exit 4 with nothing
  on standard output, every keyed row, past the 64th key included, is
  `unavailable` with that reason, so that the order is the run-wide
  `unavailable`, then `request-cap`, then an expiry's `cancelled` (C-25,
  C-28, C-34); and a lookup of `gh` that fails or
  reaches its 5 s limit, as on an unreachable `PATH` directory, gives what one
  that finds none gives, `gh-unavailable`, never a row or scan error, while
  one that the deadline stops first leaves its rows as an expiry does,
  `cancelled` within the cap and `request-cap` past it (C-26, C-28).
  Rejected: `request-cap` for those keys, one of the two outcomes that
  Codex's P1 on `e198548` found both applying, because it would make
  `remote.completeness` `incomplete` in a run where nothing was cut, the
  reason "`unavailable` beyond DI:1041-1042" below gives for `unknown` (C-25);
  and a row or scan error for the lookup, which the isolation clause forbids
  (Codex's P2 on `e198548`).

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
- **The request**: a GraphQL commit lookup of associated pull requests, with
  the queried repository's `nameWithOwner` in the same answer (C-19), which
  answers an unknown commit with a null object (`not-found`) and states a
  further page in the body. Rejected: REST `commits/{sha}/pulls`, which
  answers an unknown commit with HTTP 422, an `unknown` under DI:1055-1056, and
  signals a further page only in a header; `gh pr list` (`09af8c8`), which
  looks up by branch name, hides the page information and stops at gh's
  default of 30; and a head-branch lookup beside the association in the same
  request (S-1), weighed under Departures ("No `closed` state").
- **Matching**: the head object id exactly the row's head, the base branch
  the merge ref's branch and the base repository the one GitHub resolved for
  the identity, its `nameWithOwner` from the same answer (C-19); then
  `merged` before `open`, the highest number within a state, a closed pull
  request never matching (C-16). Rejected: the highest number first, as
  `09af8c8` chose, which a suppressed Copilot finding faulted for picking
  before checking the state; and the identity read from the URL as the base
  to match, which would read every queried row of a renamed repository
  `not-found` (S-2).
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
  established, CAS/pc:1128-1129); and a sixth state such as `not-queried`
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
  `GH_REPO`, `GH_FORCE_TTY` or `CLICOLOR_FORCE`, so that it checks for no
  update and writes none of the state it keeps for that check, prompts for
  nothing, logs nothing and prints plain output; the new scenario of "Overview
  is local and read-only" asserts the first three. An addition, made against
  DI:1038-1039; what gh does beyond its documented switches is the client's
  (What This Repository Does Not Own).

Departures, each naming what it departs from:

- **The merged-row wording** (C-5's example, "merged on GitHub by squash;
  local ancestry does not prove it; never retired"): GitHub's answer does not
  say how a pull request was merged, and a merge-commit merge that the local
  merge target does not hold yet gives the same picture, so the line names
  both causes and the number, and, since a row kept for its uncommitted or
  ignored files is queried too, says that those files are not part of the
  pull request (C-18, C-20): "merged on GitHub as pull request #N at this
  exact head; uncommitted and ignored files here are not part of it; local
  ancestry does not prove it (a squash or rebase merge, or a local merge
  target not brought up to date since); never retired on this evidence".
- **No `closed` state** (C-5 lists `closed`; C-16): GitHub's commit
  association returns no pull request closed without merging (ruling F-3: PR
  #2's head `bb91a49`, `totalCount` 0), so D5's query cannot produce it; a
  returned `CLOSED` node stays valid and never matches, and the not-found text
  names only merged and open pull requests. Rejected: a head-branch lookup,
  which needs the head branch name, re-keys DI:1044's exact-head dedupe and
  lets same-named fork pull requests fill the page. S-1's form of it, a
  `pullRequests(headRefName:)` lookup added to the same request and matched
  by exact `headRefOid`, is rejected with it: the name it needs is an
  upstream's published name, which an `unpublished` row lacks; rows sharing a
  head under two names need two requests or aliased lookups; it reverses the
  rejection of a by-name lookup (Decisions, "The request"); and under
  DI:1049-1051 a further page on its list makes the key `unknown`, so
  same-named fork pull requests could hide the `merged` answer. It is a
  follow-on change if Brett Heap wants `closed` (Out of Scope), after F-3's
  unchecked cases are checked live.

Readings of packet and ratified text:

- **"It reads no credential files"** (DI:310) and "Use the normal GitHub
  client authentication path" (DI:1056-1057): under `--remote` the `gh`
  child reads gh's own credential store, as the second requires, and the
  `project` process reads none, as the first requires.
- **"the overview never tests, displays, or infers credential values, and
  redacts any URL credentials it encounters"** (DI:1057-1058), read with
  DI:1039-1042, which has the overview derive the identity from the remote,
  "never print or forward URL-embedded credentials" and give a
  credential-bearing remote `unavailable` without a request: the packet
  expects the overview to meet a URL that carries a credential and to tell
  that it does, so the rule bounds that inspection rather than forbidding it.
  The overview holds the URL in memory only while it derives the
  `owner/repository` and detects the URL's user information; after that it
  keeps and compares no part of that information, never prints, logs, sends
  or authenticates with any of it, and never forwards the URL with it; a
  read's standard error, where Git may echo the URL, is discarded unexamined;
  and since no URL appears in either output, in a `gh` argv or in any message,
  nothing is left to redact (C-30, C-31; Codex's P2 on `67e43ae`).
- **"each is recorded as unknown"** (DI:1053): as the row's
  `remote.state`, never as a row error or scan error, so change 2's completeness
  and exit rules stay as written.
- **The human layout** (APO/ov:802-813) lists what each shown row prints and
  never says that no other line may be printed; the `remote` line and the
  summary's `Remote:` line, printed only in a `--remote` run, add to it without
  contradicting it, so it is not modified.
- **"Every field listed above is always present"** (DI:823): the rule covers
  the fields the packet lists; the two `remote` keys are fields added under
  DI:834-835 ("Adding a field or an enum value is additive within version 1,
  and consumers ignore fields they do not know"), present only in a
  `--remote` run and absent, never null, otherwise (L-10), as the MODIFIED
  block of "Overview prints a versioned JSON envelope" states for change 2's
  own "every one always present" (C-12; lane openRepoProject-3's re-read,
  LOW-7).
- **"Read at most 1 MiB of each response body"** (DI:1048-1049) and "a body
  cut at 1 MiB" (DI:1049-1050): a body cut at 1 MiB can be told from one of
  exactly 1 MiB only by the byte past it, so the reader reads that one byte
  more and keeps at most 1 MiB, nothing past it entering a result, and such a
  body is `truncated` (C-27); the 64 KiB bounds on status and headers and on
  each remote-target read's output, this change's own, are read the same way
  (C-27, C-29).

## Corrections to the Packet

None.

## Open Questions

The first two are before Brett Heap with a recommendation; the third, put to
lane openRepoProject-4 first, is resolved by its answer (C-23).

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
3. **Seams in feature 005 (to lane openRepoProject-4): resolved (C-23).**
   None is needed. The `--remote` flag is an argument error in feature 005
   until this change's realization adds it; the `remote` fields, the remote
   phase after collection and the `gh` child's handle are all added by that
   realization, after 005 lands; so is the `--remote` term of
   `probes.estimated`, while the remote-target reads enter `probes.performed`
   through the count feature 005 already keeps of every Git child started.
   Recommendation: feature 005 reserves no flag, field or hook. Lane
   openRepoProject-4 answered on 2026-10-20, by message to lane
   openRepoProject-5: feature 005 reserves no flag, field or hook for
   `--remote`, and its spec records this in its Dependencies, in lane
   openRepoProject-4's fold pass (`specs/005-project-overview/spec.md` on
   `005-project-overview` at `282a20e`).

## Questions Resolved by the Alignment Review

The alignment review (stack-architect and qa-lead) ran on `563d19d`
(2026-10-19); the lane's rulings of 2026-10-19 bind where they differ, and
the last five rows are the rulings that answered its five GAPs. Its
judgements of the writer's items (i) to (iv) are carried by SA-1, SA-6, SA-7
and QA-9. Both spec deltas are agreed by their owners and committed: the
`project-command` delta by lane openRepoProject-2 on 2026-10-19 with one fix,
and the `project-overview` delta by lane openRepoProject-4 on 2026-10-19 with
two wording fixes in its Isolation passage (Dependencies and Sequencing).

| Findings | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| SA-1: "local ancestry stays the only removal proof" presumes change 1's open question on squash-merged branches | MISMATCH | applied under C-13, as Appendix C carries it, with the final pass's HO:167 | `project-overview` delta (Isolation); Rules This Change Keeps |
| SA-2: the `remote` keys outside [J]'s "exactly these fields" recorded as a departure, against L-11 | MISMATCH | applied with change under C-12: Appendix B and the final pass's corrections; the [H] reading moved to Readings; the Capabilities entry and a What Changes bullet for [J] are worded in this round | `project-overview` delta (MODIFIED [J]); What Changes, Capabilities, Dependencies, Decisions (L-3, C-7), Departures, Readings; `design.md` Context, D8, D11 |
| SA-3: an abandoned remote-target read contradicts [E]'s Termination sentence | MISMATCH | overtaken by C-11: the interim bullet is not added, and SA-13 and SA-14 carry the ruling | as SA-13 and SA-14 |
| SA-4: the `gh` child's 5 s overrides [E]'s "Children other than Git SHALL keep 15 s." from an ADDED requirement | MISMATCH | overtaken by C-11: carried in the MODIFIED block of [E] (SA-13); Open Questions 2 replaced as Appendix D (f) gives | `project-command` delta; Open Questions 2 |
| SA-5: an internal exception in the remote phase exits 2, against the Isolation paragraph's exit status | MISMATCH | applied with change under C-14 (option A): Appendix C, the proposal sentence and the D10 edit; the proposal names "Overview exits by completeness and severity" where the review wrote [X], a label only `design.md` defines | `project-overview` delta (Isolation); Decisions ("No effect on `completeness` or the exit"); `design.md` D10 |
| SA-6: the notwithstanding list names "Overview isolates one candidate's failure", whose table ends at classification | DRIFT | applied with change: Appendix C; the proposal cites `design.md`, D1 where the review wrote D1 | `project-overview` delta (Isolation); Decisions ("Lane openRepoProject-4's check") |
| SA-7: the three departures lane openRepoProject-4 agreed are not named | DRIFT | applied with change: departure (2) as the final pass words it under C-11; the list follows the sentence that holds the quote, so that sentence stays whole | Decisions ("Lane openRepoProject-4's check", "Fields only in a `--remote` run") |
| SA-8: OV:179-180's harvest rule is not addressed | DRIFT | applied | Dependencies and Sequencing (Harvest) |
| SA-9: `unavailable` reasons beyond DI:1041-1042 have no decision | DRIFT | applied | Decisions ("`unavailable` beyond DI:1041-1042") |
| SA-10: the query set's ruling is not cited, and a scenario title nearly repeats change 2's | DRIFT | applied, with the final pass's citation of CAS proposal.md:811-813 | Decisions (query set); `project-overview` delta (scenario renamed); `design.md` D11 |
| SA-11: the credential clause drops the packet's "infers" | DRIFT | applied under C-13 | `project-overview` delta ([L] paragraph); What Changes; Rules This Change Keeps |
| SA-12: three imprecise ranges and two wording drifts | DRIFT | applied | Why; Impact; Decisions (C-1, "No early stop"); `design.md` Context |
| SA-13: [E]'s Termination and Budgets sentences contradict this change, and L-11 needs a MODIFIED block | MISMATCH | applied under C-11: Appendix A, with its added scenario and, on lane openRepoProject-2's agreement of 2026-10-19, one fix to the Termination sentence; committed | `project-command` delta |
| SA-14: the proposal, design and tasks say `project-command` is untouched and PR #19 no dependency | DRIFT | applied with change: Appendix D (a) to (l) with G2 taken, 46 scenarios; 1.4 unticked as D (j) says, and 1.5 with it, since its two INFO lines needed the then-held files, both ticked once the last held file was committed (2026-10-19); the citation key and the rulings paragraph also name L-11, L-14, L-16, L-17 and C-12 to C-14; C-4's bullet and tasks 2.2 and 2.3 follow C-11 and C-12 | citation key; What Changes; Capabilities; Dependencies and Sequencing; Decisions; Open Questions 2; `design.md` Context, D2, D7, D11; `tasks.md` 1.4, 1.5, 2.2 to 2.4, 3.4 |
| SA-15: [B]'s added paragraph departs from its own first paragraph without saying so | DRIFT | applied under C-13 | `project-overview` delta ([B] paragraph) |
| SA-16: the design lists the identity pattern's forms incompletely | DRIFT | applied | `design.md` Context |
| QA-1: SHALLs bind the `gh` client's own behaviour, which no fake can observe | MISMATCH | applied with change under C-13: spec and design as written; the proposal keeps DI:1060 on the clause it supports; What Changes and Capabilities describe the narrowed clause, and What This Repository Does Not Own gains the entry the Rules sentence points to | `project-overview` delta ([L] paragraph and scenario); What Changes; Rules; What This Repository Does Not Own; Capabilities; `design.md` D5 |
| QA-2: "No part of a response body" against the row's `number` and `url` | MISMATCH | applied, with the final pass's "No remote's URL" | `project-overview` delta (Results, Remote target) |
| QA-3: `gh-unauthenticated` for any exit 4, against D6 | MISMATCH | applied | `project-overview` delta (Results) |
| QA-4: "standard input closed" against D5's null device | MISMATCH | applied | `project-overview` delta (Requests) |
| QA-5: no scenario for the precedence, the `url` check or the other human lines | GAP | applied, with the final pass's sixth row | `project-overview` delta ("The chosen pull request and a rejected answer"); Capabilities; `design.md` D11 |
| QA-6: `observed_at` null is not pinned | GAP | applied; its optional half is carried by QA-13 and QA-14, as the final pass says | `project-overview` delta ("No gh, or a gh without authentication") |
| QA-7: `reason` and `counts` are not closed | GAP | applied | `project-overview` delta (Fields) |
| QA-8: the determinism sentence covers a timestamp | MISMATCH | applied | `project-overview` delta (Results) |
| QA-9: no test seam fails a remote-target read | GAP | applied, with the final pass's extension for SA-13's scenario | `design.md` D11 |
| QA-10: `head_sha` for rows never asked | MISMATCH | applied | `project-overview` delta (Fields) |
| QA-11: "stay equal in a complete run" claims more than change 2 gives | MISMATCH | applied | What Changes; `design.md` D2 |
| QA-12: a merge target without `branch.<target>.merge` has no upstream | MISMATCH | applied with change: the scenario's added clause follows the URL clause, so that "whose URL" still names `upstream`'s | `project-overview` delta (Remote target; "The remote target comes from the merge target's branch configuration"); `design.md` Context, D2 |
| QA-13: the line between `rate-limited` and `forbidden` is left to D6 | GAP | applied (Appendix E) | `project-overview` delta (Results; "API failures stay unknown"); `design.md` D11 |
| QA-14: the response rules live in D6 alone | GAP | applied (Appendix E) | `project-overview` delta (Results; "API failures stay unknown") |
| QA-15: the forbidden switches and "read-only" are not named | GAP | applied | `project-overview` delta (Requests; "The request bounds") |
| QA-16: no scenario stops a read at the deadline or cancels an unread target | GAP | applied | `project-overview` delta ("Expiry cancels queued and in-flight requests") |
| QA-17: "Every queried row ... SHALL be `unavailable`" reads unconditionally | MISMATCH | applied | `project-overview` delta (Remote target) |
| QA-18: two kinds of URL refusal are unnamed | MISMATCH | applied | `project-overview` delta (Remote target) |
| QA-19: `"detached"` and a null `merged_into_target` | GAP | applied | `project-overview` delta (Query set; "One request per exact head") |
| QA-20: `schema_version` and the key positions | GAP | applied, its first sentence only, since C-12 takes G2 | `project-overview` delta (Fields) |
| QA-21: the `Remote:` line and where the `remote` line goes | GAP | applied (Appendix E) | `project-overview` delta (Human report) |
| QA-22: the reads' directory, caps and "no fallback to `origin`" are in the design only | GAP | applied (Appendix E) | `project-overview` delta (Remote target; "Remotes that give no request") |
| QA-23: no `PATH` lookup and the `oid` check are in the design only | GAP | applied (Appendix E) | `project-overview` delta (opening paragraph; Requests) |
| QA-24: whose merge ref, and the case of the base repository | GAP | applied, its optional AND taken | `project-overview` delta (Results; "One request per exact head") |
| QA-25: no scenario for the determinism sentence (optional) | GAP | applied with change: QA-8's "`remote.observed_at` apart" added, since `observed_at` is a timestamp and differs between the two runs | `project-overview` delta ("The request bounds") |
| QA-26: `--remote` with `--attention` is not exercised (optional) | GAP | applied | `project-overview` delta ("A squash-merged branch is explained and kept") |
| QA-27: D6's "stopped" entry also covers the body and header stops | MISMATCH | applied | `design.md` D6 |
| QA-28: the Risk's fallback changes [B]'s count | MISMATCH | applied | `design.md` Risks |
| QA-29: the central case had no recorded check | GAP | applied (Appendix E), recording G4 | `design.md` Context, Risks |
| C-11 (G1; SA-3, SA-4): change 1's evidence model | GAP | ruling: MODIFY it whole on PR #19's text with two clauses and one scenario (Appendix A), agreed by lane openRepoProject-2 on 2026-10-19 with one fix, and committed; this change archives after PR #19's amendment of change 1 lands (L-16) and re-bases on `add-project-clean-branch-retirement`'s archived block if that change archives first (L-17) | `project-command` delta; What Changes; Capabilities; Dependencies and Sequencing; Decisions; Open Questions 2; `design.md`; `tasks.md` 1.4, 2.4, 3.4 |
| C-12 (G2; SA-2): "exactly these fields" | GAP | ruling: MODIFY change 2's "Overview prints a versioned JSON envelope" (Appendix B), agreed by lane openRepoProject-4 on 2026-10-19 with two wording fixes in the Isolation passage, and committed, so the review's Outcome B, for a decline, is not taken | `project-overview` delta; as SA-2 |
| C-13 (G3): the sentences lane openRepoProject-4 agreed | GAP | ruling: QA-1 and SA-11 at spec.md:13-27, SA-15 at :129-142 and Appendix C at :328-342 applied and sent to lane openRepoProject-4 in one diff with C-12's block, which agreed it on 2026-10-19 with two wording fixes in the Isolation passage, and committed; the review's Outcomes B to D, and SA-1 to Brett Heap, were for a decline and are not taken | `project-overview` delta; Dependencies and Sequencing |
| G4 (lane openRepoProject-3's L4): the association for a squash-merged head | GAP | ruling: answered live on #31 and #17 and recorded with its limits (QA-29); D5's query and the scope of Open Questions 2 stand | `design.md` Context, Risks |
| C-14 (G5; SA-5): the exit status of an internal remote-phase exception | GAP | ruling: option A, Appendix C, with no MODIFIED block of "Overview exits by completeness and severity" | as SA-5 |

### Council Verdicts

The council (product-advocate, systems-architect and adversary-engineer, each
read-only) read this change at `c928cb2` on 2026-10-20, with Codex's three
findings on `1229e79` and the lead's live check F-3 beside it, and the lane's
lead ruled its twelve concerns VALID, none NOTED and none DISMISSED (C-16 to
C-22, the verdicts of 2026-10-20). The rows below are those twelve concerns,
Codex's three findings and ruling C-23; the spec edits they bring were agreed
by lane openRepoProject-4 on 2026-10-20, nothing declined, and are committed
(Dependencies and Sequencing).

| Concern | Severity | Verdict | Section changed |
| --- | --- | --- | --- |
| P-1: D5's commit association never returns a pull request closed without merging, so `closed` is unreachable and such a head reads a false not-found line | HIGH | C-16 (VALID): applied as AE-1's edits 1 to 7: `closed` dropped, a `CLOSED` node kept valid and never matching, and the not-found text "no merged or open pull request on GitHub was found for this exact head" | `project-overview` delta (Results, Fields, Human report; "The chosen pull request and a rejected answer"); What Changes; Decisions (C-16, "Matching"); Departures ("No `closed` state"); Out of Scope; `design.md` Goals, D6, D8, D9, Risks |
| P-2: the freshness sentence says "queried live" in runs that queried nothing, and a run with every worktree merged has no scenario | MEDIUM | C-17 (VALID): applied with change: AE-4's sentence in place of P-2's; P-2's AND taken, its "0 requests" written `0 gh requests started`, as C-17 counts | `project-overview` delta (Fields, Human report; "No gh, or a gh without authentication"); What Changes; Decisions (C-17); `design.md` D9 |
| P-3: the `merged` line's remedy, "a merge target not fetched since", does not work, since a fetch moves only the remote-tracking ref, and the README gives no next step | MEDIUM | C-18 (VALID): applied with change: P-3's texts as written, and the README's next steps also name `malformed-remote` and `not-github`, since C-18 asks for each `unavailable` reason | `project-overview` delta (Human report; "A squash-merged branch is explained and kept"); What Changes; Impact (`README.md`); Decisions (C-18 and C-20); Departures ("The merged-row wording"); `design.md` Risks |
| P-4: only `MERGED` and the absence of `CLOSED` were checked live, and no task waits for a live answer per state | MEDIUM | C-19 (VALID): applied: task 2.5 with the cases C-19 and C-21 list, and the Risk list gains a base other than the default branch | `tasks.md` 2.5; Decisions (C-19 and C-21); `design.md` Context (tool facts), D11, Risks, Migration Plan |
| S-1: as P-1, with a head-branch lookup added to the same request as its fix | HIGH | C-16 (VALID as a defect): the fix not taken, for AE-1's reasons (it re-keys DI:1044 or needs aliased name lookups, reverses the rejection of a by-name lookup, needs a published name that an `unpublished` row lacks, and a further page on its list would hide the `merged` answer); recorded as a follow-on | Departures ("No `closed` state"); Out of Scope; Decisions ("The request") |
| S-2: the response rules rest on unobserved details of `gh api --include`: the case of header names, and the base repository of a renamed remote | MEDIUM | C-19 (VALID): applied: header names compared without case; the base repository matched against the `nameWithOwner` that the answer gives for the queried repository, added to D5's query; task 2.5 records the status line and the header names, and D11's fixture table uses the recorded forms; a `data.repository.nameWithOwner` that is not a valid GitHub `owner/repository` makes the key `api-error`, the field validated as each node's `baseRepository.nameWithOwner` is, cited in `design.md` D6 in round C5 (C-24) | `project-overview` delta (Requests, Results); Decisions ("Matching", C-19 and C-21); `design.md` D5, D6, D11; `tasks.md` 2.5 |
| S-3: the freshness sentence is false in runs that sent no request | MEDIUM | C-17 (VALID): applied with change: AE-4's constant in place of S-3's second sentence for a null `observed_at`, which a `gh` that exits 4 after `observed_at` is set would leave false | as P-2 |
| AE-1: `closed` is unreachable; the options attacked; drop it | HIGH | C-16 (VALID): applied with change: edits 1 to 7 as written, except that edit 4's placeholders are re-lettered `<a>` to `<e>`, with no gap, on the lead's follow-up to round C4, and edit 5's THEN keeps "and null `number` and `url`" | as P-1 |
| AE-2: the `merged` line reads as an all-clear under a row kept for its files | MEDIUM | C-20 (VALID): applied with change: the line as C-20 gives it; the AND names the dirty worktree's branch as one that local ancestry does not prove merged, so that the row is in the query set | `project-overview` delta (Human report; "A squash-merged branch is explained and kept"; "Remote evidence changes nothing local"); What Changes; Departures ("The merged-row wording"); `design.md` D9 |
| AE-3: `merged` was checked only for squash merges into the default branch; a base other than the default branch, a rebase merge and a merge target that tracks the person's fork are not covered | MEDIUM | C-21 (VALID): applied with change: task 2.5 holds its two cases and its rule for an answer with no `MERGED` node; its two Risks cite the ADDED requirement's base-repository rule, not spec line numbers, which move; the README says the fork case; its question sentence reads "that question" for "change 1's question 2", since the bullet names change 1's open question just before and this proposal's Open Questions 2 is another question | `tasks.md` 2.5; `design.md` Risks; Rules This Change Keeps; Impact (`README.md`) |
| AE-4: the freshness sentence and the `Remote:` count claim a query to github.com in runs where none reached it, a `gh` that exits 4 included | MEDIUM | C-17 (VALID): applied: its sentence, its count wording and its AND | `project-overview` delta (Fields, Human report; "No gh, or a gh without authentication"); What Changes; Decisions (C-17); `design.md` D9 |
| AE-5: a body that Python's parser rejects with an error other than `JSONDecodeError` exits 2 and drops the local overview, and the `gh` lookup can start a `gh` planted in the caller's directory | LOW | C-22 (VALID): applied with change: the spec text and AND as given; `design.md` records the two points in D5 (the lookup) and D6 (the parse), D6 being where a response is parsed, where the verdict names D2, which parses no body; AE-5's fixtures are cited by their results, not their scratch paths (L-9); its suggested Results text also carries the rule that a response holding more than 100 pull requests is `api-error`, cited in `design.md` D6 in round C5 (C-24) | `project-overview` delta (opening paragraph, Results; "API failures stay unknown"); What Changes; Impact (`project`); Decisions (C-22); `design.md` D5, D6, D10, D11 |
| Codex 1 (P1, on `1229e79`): `closed` is unreachable through `Commit.associatedPullRequests` | P1 | holds (F-3): C-16 | as P-1 |
| Codex 2 (P1, on `1229e79`): no part of a body may appear in either output, against the row's `number` and `url` | P1 | does not hold at `c928cb2`, QA-2's edit having landed in `621715a`; its optional tightening applied: "no other response text" | What Changes ("Explicit results") |
| Codex 3 (P2, on `1229e79`): the freshness text claims a live query when none ran | P2 | holds: C-17 | as P-2 |
| C-23: Open Questions 3, the seams in feature 005 | ruling | resolved: lane openRepoProject-4's message of 2026-10-20 says that feature 005 reserves no flag, field or hook for `--remote`, which its spec records in its Dependencies (`282a20e`) | Open Questions 3; Dependencies and Sequencing ("Realized after feature 005"); `design.md` Open Questions; `tasks.md` 1.1 |

### Re-read Findings (round C4)

Lane openRepoProject-3's read-only verifier re-read this change at `c928cb2`
on 2026-10-20 against the packet at `da33d92`, change 2 at `961c405`, PR #19
at `c462d87`, #26 at `ca96701` and #27 at `e906c2f`, and found 43 of its 44
earlier ids FIXED and M4 PARTLY, with no HIGH, one MEDIUM and ten LOW new
findings. The lane's lead accepted every item as lane openRepoProject-3 words
its fix (council verdicts, C-15), and LOWs 5, 6 and 10 edit the
`project-overview` delta, which lane openRepoProject-4 agreed and which is
committed.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| MEDIUM-1: ratifying this change would also ratify PR #19's pending sentences in its block of [E] | MEDIUM | C-15: applied: #26's scope sentence, in lane openRepoProject-3's wording, after the PR #19 bullet and in `tasks.md` 1.6; 2.4 returns to Brett Heap a re-base that changes the block's added text | Dependencies and Sequencing; `tasks.md` 1.6, 2.4 |
| LOW-1: "local ancestry the only cleanup gate", where DI:1059 has no "only" | LOW | C-15: applied | Why |
| LOW-2 (M4's residual): three passages still promise gh's own behaviour | LOW | C-15: applied | Decisions ("gh's own traffic off"); `project-overview` delta (Requests); `design.md` Goals |
| LOW-3: "CAS/cmd:90-214" for [E] at main, which runs to :231 | LOW | C-15: applied | Dependencies and Sequencing |
| LOW-4: the archive waits for PR #19's text though PR #19 may close, and Migration step 4 omits 2.4 and the L-17 re-base | LOW | C-15: applied | Dependencies and Sequencing; `design.md` Migration Plan |
| LOW-5: "whose remote target was not yet read" also covers a read in flight | LOW | C-15: applied | `project-overview` delta (Requests) |
| LOW-6: nothing stops in-flight `gh` children on C-14's exit 2 | LOW | C-15: applied with change: lane openRepoProject-3's words in the ADDED requirement, which starts the children, with [E] named beside [B] and [X], since [E] kills a probe child's group on every exit path; [E]'s Termination paragraph binds Git children only, so no `project-command` edit is needed and nothing was held for lane openRepoProject-2 | `project-overview` delta (Requests); `design.md` D7 |
| LOW-7: DI:823 is not named | LOW | C-15: applied | Readings |
| LOW-8: 1.5 ties both INFO lines to change 2, and 1.1 lists the rulings only to C-10 | LOW | C-15: applied with change: 1.1 lists the rulings through C-23, where the verdicts say C-19, since this round also applies C-20 to C-23 | `tasks.md` 1.1, 1.5 |
| LOW-9: [E]'s pins sentence, "its row is `inspection-error`", is not carved out for the remote-target reads | LOW | C-15: applied: G1 note (c) recorded in D2 as reasoning, not a test | `design.md` D2 |
| LOW-10: no scenario sends a 403 with `Retry-After` | LOW | C-15: applied: a tenth key in "API failures stay unknown", its header name written as `gh` prints it (C-19) | `project-overview` delta ("API failures stay unknown"); `design.md` D11 |

### Re-read and Codex Findings (round C5)

Lane openRepoProject-3's read-only verifier read the delta `c928cb2..e198548`
on 2026-10-20, a partial read at the lead's order (shared meter 92%), and found
no HIGH and no MEDIUM, all eleven of its earlier items applied (LOW-6 and LOW-8
with changes it judged sound) and seven LOWs; Codex re-reviewed `e198548` on
2026-10-20 (comments 4324567339, 4324567350 and 4324567356) with one P1 and two
P2s. The lane's lead accepted all ten (C-24 to C-27, the rulings of
2026-10-20) and ruled on two points the writer found in applying them (C-28,
C-29), the last two rows; C-24's items 3 and 4 and C-25 to C-29 edit
`specs/project-overview/spec.md`; lane openRepoProject-4 agreed those edits on
2026-10-20 with nothing declined, and they are committed with the rest
(Dependencies and Sequencing).

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| F1: "a seventh state such as `not-queried`", where C-16 leaves five states | LOW | C-24: applied: "a sixth state" | Decisions ("Fields only in a `--remote` run") |
| F2: Q16's option A, a departure from D1 and N1, would trigger no re-read, and D7 states D1's mask as fact | LOW | C-24: applied with change: the trigger reads "amends, or records a departure from, change 2's design D1 or clarifications N1 before change 2 archives", with "or" between D1 and N1 as C-24 words it, where lane openRepoProject-3's fix has "and", so that a change to either fires it; the Dependencies sentence also names option A and says that `gh` children follow a recorded departure as they follow D1 and N1, which it would otherwise misstate; D7's pointer, in lane openRepoProject-3's words, sits inside the parenthesis that cites D1 | Dependencies and Sequencing ("Realized after feature 005"); `tasks.md` 2.3; `design.md` D7 |
| F3: the absolute-`PATH` lookup (C-22) has no AND and no D11 seam | LOW | C-24: applied: lane openRepoProject-3's AND, a planted `gh` in the working directory behind an empty entry and `.`, and the planted `gh` in D11 | `project-overview` delta ("No gh, or a gh without authentication"); `design.md` D11 |
| F4: the renamed-repository rule has a D11 seam and no scenario | LOW | C-24: applied: an AND in which the answer gives `acme/gizmo` as the queried repository's `nameWithOwner`, so that the open node whose base repository carries that name matches and the merged node carrying the name asked does not; D11's seam names it | `project-overview` delta ("The chosen pull request and a rejected answer"); `design.md` D11 |
| F5: task 2.5's "one of them" has no antecedent | LOW | C-24: applied, in lane openRepoProject-3's words | `tasks.md` 2.5 |
| F6: "DI:1036-1060 names no states", where the packet names "a merged pull request" | LOW | C-24: applied as C-24 words it: the decision now says that DI:1036-1060 names "a merged pull request" (DI:1059-1060) and no other state, in place of lane openRepoProject-3's "names no `closed` state, and gives no state set"; the phrase spans DI:1059-1060, where C-24 cites DI:1059 | Decisions ("Closed pull requests, C-16") |
| F7: two `api-error` rules trace to no ruling: more than 100 pull requests, and a `data.repository.nameWithOwner` that is not a valid `owner/repository` | LOW | C-24: applied: the first is AE-5's suggested Results text, taken by C-22; the second comes with the `nameWithOwner` field that S-2 adds and C-19 takes, validated as each node's `baseRepository.nameWithOwner` is, S-2's text adding the field without stating the check in words; both are cited in `design.md` D6, where the design states them, and in the AE-5 and S-2 rows above, the spec carrying no citations | `design.md` D6; Council Verdicts (AE-5, S-2) |
| Codex 4 (P1, on `e198548`, spec.md:453): with more than 64 keys and no `gh`, the rows past the 64th key are both `gh-unavailable` and `request-cap` | P1 | C-25: applied with change: `request-cap` applies only when requests can be sent and the cap stops them; with no `gh` found, or when each of the 64 requests that the cap allows ends in exit 4 with nothing on standard output, every keyed row, past the 64th key included, is `unavailable` with that reason; the AND on "The request bounds" covers no `gh` and also the exit-4 case, which C-25 names beside it | `project-overview` delta (Requests, Results; "The request bounds"); What Changes ("Explicit results"); Decisions ("Run-wide unavailability, C-25 and C-26"); `design.md` D4, D5, D6 |
| Codex 5 (P2, on `e198548`, spec.md:342): a lookup of `gh` that fails or times out has no remote outcome | P2 | C-26: applied with change: such a lookup gives every keyed row `gh-unavailable`, never a row or scan error, the AND cutting it at 5 s on a slow `PATH` directory, and the README's next step reads "install `gh`, or check that `PATH`'s directories are reachable"; [B]'s added paragraph names the lookup beside the remote-target reads and the `gh` children, since [B]'s bounded-task rule would otherwise record its `probe-timeout` and L-11 settles that in the MODIFIED block; and a lookup that the deadline stops before its 5 s end leaves its rows as an expiry does, `cancelled` within the cap and, by C-28 below, `request-cap` past it, so that `gh-unavailable` and `cancelled` never both apply | `project-overview` delta ([B] paragraph; Results, Isolation; "No gh, or a gh without authentication"); What Changes; Impact (`README.md`); Decisions ("Run-wide unavailability, C-25 and C-26"); `design.md` D5, D10, D11, Risks |
| Codex 6 (P2, on `e198548`, spec.md:416): reading at most 1 MiB cannot tell a body of exactly 1 MiB from a longer one, nor 64 KiB of status and headers from more | P2 | C-27: applied: at most 1 MiB and one byte of the body is read and at most 1 MiB kept, a longer body being `truncated`, and likewise 64 KiB and one byte of status and headers, more being `api-error`; recorded as a reading of DI:1048-1050 | `project-overview` delta (Results); What Changes ("One bounded request per exact head"); Readings; `design.md` D6 |
| C-28: at an expiry, the rows of a key past the 64th could read as `request-cap` or as `cancelled`, a point older than this round (found by the writer) | ruling | C-28: applied: the expiry sentence gives `cancelled` only to a key within the cap not yet sent, keeps `aborted` for a request in flight, and says that the rows of a key past the 64th stay `request-cap` whether or not the remote budget or the deadline expires, the run-wide `unavailable` outranking both; a lookup that the deadline stops leaves its rows to that rule; one AND, with 70 keys, on "Expiry cancels queued and in-flight requests"; the ruling's "queued or in flight" is read as the expiry's two outcomes, `cancelled` for a queued key and `aborted` for one in flight, as DI:1051-1053 and the spec have them, not as `cancelled` for a request in flight | `project-overview` delta (Requests, Results; "Expiry cancels queued and in-flight requests"); What Changes ("One bounded request per exact head"); Decisions (C-6, "Run-wide unavailability, C-25 and C-26"); `design.md` D4, D5, D7 |
| C-29: the remote-target reads' 64 KiB output cap cannot tell exactly 64 KiB from more (found by the writer) | ruling | C-29: applied: at most 64 KiB and one byte of each read's standard output is read and at most 64 KiB kept, a longer output failing the read, which is `remote-target-unread`, as C-27 has it for a response | `project-overview` delta (Remote target); Readings; `design.md` D2 |

### Re-read and Codex Findings (round C6)

Codex's inline finding on `67e43ae` (comment 4327505442, 2026-10-20) is one
P2, and the lane's lead accepted it (C-30, the rulings of 2026-10-20) and
ruled on three points the writer found in applying it (C-31 to C-33). Lane
openRepoProject-3's read-only verifier then read the delta
`e198548..67e43ae` on 2026-10-20, folded with round C4's open items, and
found no HIGH, no MEDIUM and six LOWs (L1 to L6, its lines at `67e43ae`),
which the lead accepted (C-34), six rows. C-30 to C-33 and L4 edit
`specs/project-overview/spec.md`, C-30 and C-31 in "Overview is local and
read-only", the block lane openRepoProject-4 agreed; lane openRepoProject-4
agreed those edits too on 2026-10-20 with nothing declined, and they are
committed with the rest (Dependencies and Sequencing). After that agreement
the lead ruled on the rest of lane openRepoProject-3's L3, a `PATH` directory
that gives an error (C-35, as lane openRepoProject-3's narrowing amended it
before any edit), the last row; it edits `design.md` alone, and the agreed
spec text is unchanged.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Codex 7 (P2, on `67e43ae`, spec.md:27): the overview must read and test a remote's URL to derive the identity and give `credential-bearing-remote`, which the unconditional "read, test, infer, print and forward no credential value" forbids, so no implementation can satisfy both | P2 | C-30: applied with change: in the second paragraph of "Overview is local and read-only", a remote's URL is the replacement clause's second exception, beside the caller's environment, held in memory only while the overview derives the `owner/repository` and detects its user information, which it tests only as the ADDED requirement's `credential-bearing-remote` and `malformed-remote` reasons state; after that no part of the user information is retained or compared, none is ever printed, logged, sent or used to authenticate, and the URL is never forwarded with it. Two changes to the ruling's words: "compared" joins "retained" under "after that" rather than "ever", because deriving the identity, which the ruling's first bullet allows, compares the user with `git` (`malformed-remote`; `design.md` D3, step 3); and "the identity" is written "the GitHub `owner/repository`", since change 2's "repository identity" is `{root, common_dir, dev, ino}`. The `project` process's other credential clauses are unchanged: it reads no credential file and no profile data the scan does not need, a `gh` child authenticates by the GitHub client's own means, and the caller's environment passes to it unread. No AND is added: the AND of "Remotes that give no request" already says that neither output, no argv and no message contains `s3cr3t` or the credential-bearing URL, and what the process keeps in memory after the derivation is not observable from outside it; C-32 below extends that AND to the user part on its own. The copies follow, the Rules entry retitled from "never touched", since `project` now reads such a URL, and DI:1057-1058 gains a Reading | `project-overview` delta ("Overview is local and read-only", second paragraph); What Changes ("One carve-out"); Capabilities; Dependencies and Sequencing; Rules This Change Keeps; Readings; `design.md` Context, Goals, D2, D3 |
| Writer C6's point 1: Git may echo a remote's URL, user information included, on a remote-target read's standard error, which the ADDED requirement drains and discards, text that C-30's bounds did not cover | ruling | C-31: applied, after the check it asks for: no classification reads that standard error, since `no-remote-target` for a remote that is not configured comes from the exit status 2 of `git remote get-url` (checked again on Git 2.43.0 in this round: exit 2 with "error: No such remote" on standard error alone, and a credential-bearing URL on standard output alone, nothing on standard error), and every other reason comes from standard output, the exit status or a limit; the Remote target paragraph of the ADDED requirement reads "drained and discarded unexamined", and the exception in "Overview is local and read-only" names the URL a read "prints on standard output" and ends "Such a read's standard error SHALL be drained and discarded unexamined", so that URL stays the only credential-bearing text the overview inspects; `design.md` D2 says the exit status decides, never Git's message | `project-overview` delta ("Overview is local and read-only", second paragraph; Remote target); What Changes ("One carve-out"); Capabilities; Dependencies and Sequencing; Rules This Change Keeps; Readings; `design.md` Context, D2 |
| Writer C6's point 2: the AND of "Remotes that give no request" checks `s3cr3t` and the whole URLs, not the user part on its own, which C-30 also forbids | ruling | C-32: applied: the AND reads "neither output, no argv and no message contains `alice`, `s3cr3t` or any of those URLs"; in that scenario `alice` appears only in the credential-bearing URL of its WHEN, so the URL is unchanged; its other use, the fork `alice/widget`, is in "The remote target comes from the merge target's branch configuration", another fixture; C-33 below replaces `alice` with a token | `project-overview` delta ("Remotes that give no request"); Dependencies and Sequencing; `design.md` Context, D3 |
| Writer C6's point 3: `alice` would fail C-32's AND in a test run under a path or user name that holds it, such as pytest's per-user temporary directory, `pytest-of-<user>` | ruling | C-33: applied: the user part of the credential-bearing URL in the WHEN of "Remotes that give no request" is now `u9zq-kx7w`, and the AND reads "neither output, no argv and no message contains `u9zq-kx7w`, `s3cr3t` or any of those URLs"; the token is a valid user part, its hyphen and its letters outside hexadecimal keep it out of every object id and every `tempfile` name, and it occurs nowhere else in the repository | `project-overview` delta ("Remotes that give no request"); Dependencies and Sequencing; `design.md` D3 |
| L1: the Dependencies sentence quotes lane openRepoProject-4's agreement of round C5 in words that its NOTED at `lanes/log/openRepoProject-4.md:70` does not hold | LOW | C-34: applied: the sentence quotes the NOTED exactly, read at `7835b98be` and on the register's `origin/main` at `85f9c2648`, where line 70 is unchanged, as B-27 LOW 3 did; the full sha256 stays as lane openRepoProject-5's own record | Dependencies and Sequencing ("Round C5's spec edits were agreed") |
| L2: nothing tests a part of exactly 1 MiB of body, 64 KiB of status and headers or 64 KiB of a remote-target read's output, the off-by-one the byte past each bound guards against | LOW | C-34: applied, design only as C-34 rules: D11's fake `gh` can send exactly 1 MiB of body and a status and header block of exactly 64 KiB, and the bounded reader is unit-tested at N-1, N and N+1 bytes for the three bounds; no spec AND | `design.md` D11 |
| L3: D1 does not place the lookup of `gh`, which the rule for a lookup that the deadline cuts presumes comes after the remote-target reads | LOW | C-34: applied: D1 runs the lookup once, between its two steps, after the reads or the deadline and before the first request, so that every key exists when it ends | `design.md` D1 |
| L4: "`request-cap` applies only when requests can be sent and the cap stops them" is false for a lookup that the deadline cuts, which leaves the keys past the 64th `request-cap` | LOW | C-34: applied, by dropping the gloss, as C-34 prefers, since the Requests paragraph's expiry sentence and the Results paragraph then state the whole order alone: the run-wide `unavailable`, then `request-cap`, then `cancelled`; the copies follow: `design.md` D4 makes the rest `request-cap` unless the run-wide `unavailable` applies, a lookup the deadline cuts being no such case, and the Decisions bullet states the order; the round C5 row for Codex 4 keeps the gloss as that round's record | `project-overview` delta (Requests); Decisions ("Run-wide unavailability, C-25 and C-26"); Dependencies and Sequencing; `design.md` D4 |
| L5: "and no other state", where the packet also names unavailable and unknown results | LOW | C-34: applied: "and no other pull-request state" | Decisions ("Closed pull requests, C-16") |
| L6: the rejected `request-cap` alternative credits Codex's P1 on `e198548` with the completeness reason, which that P1 does not give | LOW | C-34: applied: the P1 is cited for the conflict it found, the two outcomes both applying, and the reason is the proposal's own, the one "`unavailable` beyond DI:1041-1042" gives, with C-25 | Decisions ("Run-wide unavailability, C-25 and C-26") |
| L3, the rest: a `PATH` directory that gives an error, for which the lookup of `gh` states no rule, a missing directory being common | LOW | C-35, as amended by lane openRepoProject-3's narrowing, which the lead adopted before any edit in place of C-35's first wording (a directory skipped for any reason): applied, design only: the lookup skips a directory where `gh` is absent, as POSIX `execvp`'s search and a shell's own search skip it (ENOENT, ENOTDIR or EACCES on the directory or on its `gh` entry, or an entry that is not a regular file with execute permission), so that the `gh` found is the one the person's shell would run; any other error from a directory or its entry, such as EIO, ELOOP or ESTALE, fails the lookup, and every queried row with a key is then `unavailable` with `gh-unavailable`, as the spec's "fails" already states; the 5 s limit and the deadline stay the only cuts of the lookup as a whole; the spec's "finds none, fails, or reaches its 5 s limit" speaks of the lookup as a whole, so the rule fills D5 and changes no spec text; D11 gains two tests, a mode-000 directory before the real `gh`'s directory, which finds `gh`, and a directory whose `gh` is an ELOOP symlink, before it, which gives `gh-unavailable`; the writer checked both cases on 2026-10-20 with a prototype of the rule (the mode-000 directory is skipped and `gh` found; the ELOOP symlink fails the lookup), and recorded in D5 what glibc 2.39's `execvp`, bash 5.2.21, zsh 5.9 and dash do with each error, so that its rationale rests on what was observed | `design.md` D5, D11 |
