Lane: openRepoProject-5

# Proposal: add-project-overview-remote-merge-status

Status: draft; alignment review and council resolved on PR #29, round C4's spec
edits committed; rounds C5 and C6 (C-24 to C-34), their spec edits committed, on
lane openRepoProject-4's 2026-10-20 agreement; and C-35 to C-43, in `design.md`
alone with no spec edit, C-41 also in Impact: lane openRepoProject-3's narrowing
of the `gh` lookup's directory rule (C-35), its confirm reads of rounds C6c, C7
and C9 and Codex's findings, with the lead's C-40; round C11's C-44, a refusal
of a relative `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` or `HOME`, in `design.md` and
Impact, its spec edit committed on lane openRepoProject-4's YES; rounds C12 and
C13 (C-45 to C-47: lane openRepoProject-3's six LOWs; reader RC's M4, M5, L6 and
L2 to L5), with no spec edit, in `design.md` and `tasks.md`, C-47 also in Impact
and Open Question 1; round C14's C-48, RC's other five findings, its spec edit
committed on lane openRepoProject-4's YES of 2026-10-21, and C-49, lane
openRepoProject-3's eight LOWs, both also in `design.md`, Impact and `tasks.md`;
and rounds C15 to C22 (C-50 to C-68: W16, RF's M1, W22, W28, RH's M4, RI-6,
W57-1, RH's L4, W53's cites, W61, W66), in `design.md` and `tasks.md`, C-58,
C-66, C-67 also in the spec, C-63, C-65 in Decisions; ratification by Brett Heap
pending; nothing here is ratified. Governing issue: opensoft/openRepoProject#25,
claimed by lane openRepoProject-5 (comment 6111242617); refs #6, the record of
the project maintenance design packet. Proposed on Brett Heap's word "usage
reset, resume all. read handoff and resume and fan out wide and do as much as
possible in parallel" (2026-10-11), read by lanes openRepoProject-4 and
openRepoProject-5 as a go for the candidate list they put to him.

Citations are `file:line`. The packet is cited at `da33d92`, equal to main
`961c405` for `ideation/`: `DI`, `SY`, `BA` and `OV` are its
`project-maintenance-` files `project-discovery.md`,
`synthesis-inspect-and-retire.md`, `batch-cleanup.md` and `overview.md`, and
`HO` is `next-session-project-maintenance-fix-handoff.md`. Everything else is
cited at main `961c405` (L-15), whose `project`, `tests/` and `openspec/` main
holds unchanged at `15504f1`, two added changes aside, where PR #16 (`e45155a`)
revised `ideation/`: `APO` is `openspec/changes/add-project-overview/` (change
2, ratified and unarchived) and `APO/ov` its `specs/project-overview/spec.md`,
the text this change's deltas are written on; `CAS` is
`openspec/changes/add-project-clean-all-safe/` (change 1), with `CAS/pc` and
`CAS/cmd` its `specs/project-clean/spec.md` and `specs/project-command/spec.md`;
`PRS` is `openspec/specs/project-review-safety/spec.md`; and `project:N` is the
executable. Change 1's evidence model, `Repository inspection requires Git 2.36
and shares one evidence model` (CAS/cmd:90), is [E]. The lane's rulings are
cited as L-1 to L-9 and C-1 to C-8 (2026-10-11), L-10 to L-15, B-14, C-9 and
C-10 (2026-10-18), L-16, L-17 and C-11 to C-14 (2026-10-19), and F-3 and C-15 to
C-68 (2026-10-20 to 2026-10-22, C-16 to C-22 being the council's verdicts).
`PR19/cmd` is draft PR #19's
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
  scan error; an expiry in the remote phase records no `deadline-exceeded` scan
  error (C-48). Without `--remote` both counts are change 2's, byte for byte;
  the `gh` requests are counted in `remote.requests` alone, and the `remote`
  object keeps no `probes` of its own, so a run has one count of Git children.
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
    or scan error (nor is an expiry in the remote phase, C-48); without
    `--remote` both counts stay as change 2 states them. Added scenario: in a
    complete run `estimated` equals `performed` with and without `--remote`, the
    `--remote` run's counts exceeding the other's by exactly the remote-target
    reads, and the `gh` request counted only in `remote.requests`.
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
- **`README.md`**: the overview section gains `--remote`: what it asks, that it
  needs `gh` logged in, its bounds, what `unknown` and `unavailable` mean, that
  the answer is live and never authorizes cleanup, and the next steps: for a
  `merged` row, bring the local merge target up to date and rerun it, after
  which local ancestry decides a merge-commit merge; a squash-merged row stays
  kept; whether a local patch-equivalence proof may ever retire it is change 1's
  open question (CAS proposal.md:1001-1005); for `gh-unavailable`, install `gh`,
  check that `PATH`'s directories are reachable, or make a relative
  `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` or `HOME` absolute (C-26, C-44); for
  `gh-unauthenticated`, run `gh auth login`; for `no-remote-target`, give the
  merge target an upstream that its remote's fetch refspec maps, as `git remote
  add`'s does (C-48); for `credential-bearing-remote`, take the credential out
  of the URL; for `malformed-remote`, use an https, ssh or scp-like URL, not
  `git://`, with an `owner/repository` on `github.com`, no user but `git` and no
  port; and for `not-github`, nothing, as only `github.com` is queried, but use
  `https://github.com/acme/widget.git` for `GitHub.com` or a URL with no `://`
  and no `:` before its first `/`, a local path to Git (C-18, C-47, C-49). They
  are advice, not a `suggested_command`. It also says a merge target tracking a
  fork asks about the fork, so every queried row is `not-found` (C-21).
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
  main `15504f1`; L-12).
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
  merged at `961c405`, which main still holds at `15504f1` with change 2
  unarchived (2026-10-22), not `openspec/specs/`, which has no
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
rulings and council verdicts of 2026-10-20: **F-3** (the lead's live check that
GitHub's commit association returns no pull request closed without merging),
**C-15** (the council's inputs), **C-16** to **C-22** (its verdicts, below),
**C-23** (Open Questions 3), **C-24** to **C-29** (C5: lane openRepoProject-3's
delta read, Codex's three findings and two points found in applying them),
**C-30** to **C-34** (C6: Codex's finding, the lead's three points and lane
openRepoProject-3's folded read), **C-35** to **C-40** (the lookup's rule; D5's
rationale; `parse_int`; four LOWs on C7; `parse_constant`; strict UTF-8),
**C-41** (Codex's P2; **C-44** replaces it), **C-42** (lane openRepoProject-3's
MEDIUM-1, `number` by type), **C-43** (its four LOWs), **C-44** (a relative
`GH_CONFIG_DIR`, `XDG_CONFIG_HOME` or `HOME` fails the lookup of `gh`), **C-45**
(lane openRepoProject-3's six LOWs), **C-46** and **C-47** (RC's M4, M5 and L2
to L6), **C-48** (its other five) and **C-49** (lane openRepoProject-3's eight
LOWs on C13); all are applied in `design.md`, C-45 to C-49 also in `tasks.md`,
C-41, C-44 and C-47 to C-49 in Impact, C-47 in Open Question 1, and C-44's and
C-48's spec edits committed on lane openRepoProject-4's YES (C5-C14).

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
  `unavailable`, then `request-cap`, then an expiry's `cancelled` (C-25, C-28,
  C-34); and a lookup of `gh` that fails, as for a relative `GH_CONFIG_DIR`,
  `XDG_CONFIG_HOME` or `HOME` (C-44; C-58 for the last two), or reaches its 5 s
  limit, as on an unreachable `PATH` directory, gives what one that finds none
  gives, `gh-unavailable`, never a row or scan error, while one that the
  deadline stops first leaves its rows as an expiry does, `cancelled` within the
  cap and `request-cap` past it (C-26, C-28). Rejected: `request-cap` for those
  keys, one of the two outcomes that Codex's P1 on `e198548` found both
  applying, because it would make `remote.completeness` `incomplete` in a run
  where nothing was cut, the reason "`unavailable` beyond DI:1041-1042" below
  gives for `unknown` (C-25); and a row or scan error for the lookup, which the
  isolation clause forbids (Codex's P2 on `e198548`).

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
- **Matching**: the head object id exactly the row's head, the base branch the
  merge ref's branch and the base repository the one GitHub resolved for the
  identity, its `nameWithOwner` from the same answer (C-19); then `merged`
  before `open`, the highest number within a state, a closed pull request never
  matching (C-16). Rejected: the highest number first, as `09af8c8` chose, which
  a suppressed Copilot finding faulted for picking before checking the state;
  and the identity read from the URL as the base to match, which would read
  every queried row of a renamed repository `not-found` (S-2).
- **A remote phase after collection**, its 30 s starting with the first request.
  Rejected: interleaving requests with collection, which would need a hook in
  feature 005's scheduler and make dispatch depend on completion order.
- **At most two Git children per repository for the remote target**, the
  second only when the first names a usable remote, counted in the
  envelope's `probes` (C-9). Rejected: parsing
  `<common_dir>/config`, which includes and `insteadOf` would make disagree
  with Git, as change 2's design rejected for `core.worktree` (APO
  design.md:218-219); listing the whole configuration, which would read values
  such as `http.<url>.extraHeader` that may hold a token.
- **`unavailable` beyond DI:1041-1042.** The packet makes a credential-bearing,
  malformed or non-GitHub remote `unavailable` with no request (DI:1041-1042),
  and a failed or timed-out request an explicit unknown (DI:1055-1056); this
  change departs from both where no answer can come for want of a target or a
  client, and gives `unavailable` also to `no-remote-target`, `gh-unavailable`
  (no `gh`, a failed lookup, or one past its 5 s limit) and `gh-unauthenticated`
  (sent, but gh's exit 4 says nothing can be answered without a login), so
  `remote.completeness` stays `complete`. Rejected: `unknown` for these, which
  would make it `incomplete` on a machine without `gh` though nothing was cut.
- **Fields only in a `--remote` run, and the row's only on a queried row**;
  absent, never null, elsewhere. L-10 settles the first half; the second departs
  from L-10's C clause read alone, as lane openRepoProject-4 agreed on
  2026-10-19 (departure 3 of "Lane openRepoProject-4's check"), since L-10
  forbids null for "not applicable" and a row outside the query set was not
  asked. Rejected: `remote: null` on every row of every run, which would change
  the default document feature 005 builds; in a `--remote` run, `remote: null`
  outside the query set, as the first draft had, which would say "unknown" where
  nothing was asked (null keeps change 1's meaning, unknown or not established,
  CAS/pc:1128-1129); and a sixth state such as `not-queried` on every row, which
  would only restate the row's own `branch`, `head` and `merged_into_target`.
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
- **gh's own traffic off.** Each `gh` child runs with `GH_NO_UPDATE_NOTIFIER=1`,
  `GH_NO_EXTENSION_UPDATE_NOTIFIER=1`, `GH_PROMPT_DISABLED=1`,
  `GH_TELEMETRY=false` and `NO_COLOR=1` (gh 2.96.0's `gh help environment`), and
  without `GH_DEBUG`, `DEBUG`, `GH_HOST`, `GH_REPO`, `GH_FORCE_TTY` or
  `CLICOLOR_FORCE`, so that it checks for no update and writes none of the state
  it keeps for that check, prompts for nothing, logs nothing and prints plain
  output; the new scenario of "Overview is local and read-only" asserts the
  first three. An addition, made against DI:1038-1039 ("opt-in and read-only"),
  with no Git scrub; what a `gh` child reads, writes or sends beyond its argv
  and these switches is the client's own, a residual (What This Repository Does
  Not Own) against that line and DI:307-308 ("never ... writes files").

Departures from C-5, each naming what it departs from:

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

1. **Enum closure (L-4).** Change 1: "Enums SHALL be closed within a schema
   version" (CAS/pc:1129-1131); change 2: "adding a field or an enum value is
   additive" (APO/ov:655-658). This change adds no value to an existing enum:
   it adds a row sub-record and an envelope object, in a `--remote` run only,
   with a new, closed `state` enum. Recommendation: the sub-records make it
   moot for this change, which keeps `schema_version: 1`; it is settled where
   it bites, and the first change it reaches is this change's own `closed`
   follow-on (Out of Scope; C-47), which adds a value to `remote.state`.
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
| L3, the rest: a `PATH` directory that gives an error, for which the lookup of `gh` states no rule, a missing directory being common | LOW | C-35, as amended by lane openRepoProject-3's narrowing, which the lead adopted before any edit in place of C-35's first wording (a directory skipped for any reason): applied, design only: the lookup skips a directory where `gh` is absent, as POSIX `execvp`'s search and a shell's own search skip it (ENOENT, ENOTDIR or EACCES on the directory or on its `gh` entry, or an entry that is not a regular file with execute permission), so that the `gh` found is the one the person's shell would run; any other error from a directory or its entry, such as EIO, ELOOP or ESTALE, fails the lookup, and every queried row with a key is then `unavailable` with `gh-unavailable`, as the spec's "fails" already states; the 5 s limit and the deadline stay the only cuts of the lookup as a whole; the spec's "finds none, fails, or reaches its 5 s limit" speaks of the lookup as a whole, so the rule fills D5 and changes no spec text; D11 gains two tests, a mode-000 directory before the real `gh`'s directory, which finds `gh`, and a directory whose `gh` is an ELOOP symlink, before it, which gives `gh-unavailable`; the writer checked both cases on 2026-10-20 with a prototype of the rule (the mode-000 directory is skipped and `gh` found; the ELOOP symlink fails the lookup), and recorded in D5 what glibc 2.39's `execvp` does with each of twelve injected errors and what bash 5.2.21, zsh 5.9 and dash do with an ELOOP `gh`, so that its rationale rests on what was observed (round C7 rewords that rationale, C-36; round C8 names the twelve errors, ENOEXEC among them, and adds the shells' runs on the three errors the lookup skips, C-38) | `design.md` D5, D11 |

### Re-read and Codex Findings (round C7)

Lane openRepoProject-3's read-only verifier read the delta `233df0b..1c32667`
on 2026-10-20 (its confirm read of rounds C6c and B7, `brett-wip` d48a20d65)
and found no HIGH, no MEDIUM and one LOW on this change, which the lead
accepted (C-36). Codex re-reviewed `1c32667` on 2026-10-20 (21:12:35Z) with one
P2 at `design.md:457`, which the lead accepted (C-37). Both edit `design.md`
and this file only: no spec file changed, `specs/project-overview/spec.md` is
still the file lane openRepoProject-4 agreed, sha256
`2ecd3d72b7cd32595d12f66206b7dd3c71df2cdfb9430122dd1ab0414ff1fe3e`, and
`specs/project-command/spec.md` is unchanged.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| LOW-1 (lane openRepoProject-3's confirm read, `design.md` D5 and the round C6 table's C-35 row): D5 says the lookup "does not choose between searches that disagree, and so is stricter than glibc's on ESTALE, ENODEV and ETIMEDOUT too", but the shells were run on ELOOP only, so no disagreement was seen on those three; "too" has no antecedent; the glibc list omits ENAMETOOLONG, ENOMEM and E2BIG; and the row's "what glibc, bash, zsh and dash do with each error" says more than was run | LOW | C-36: applied: the rule is unchanged; D5 now says that the lookup skips only what every search checked skips, and that an error that not every search was seen to skip fails it; that glibc 2.39's `execvp` stops on ELOOP, EIO, ENAMETOOLONG, ENOMEM and E2BIG and goes on past ENOENT, EACCES, ENOTDIR, ESTALE, ENODEV and ETIMEDOUT (eleven of the twelve errors injected; ENOEXEC, the twelfth, is named in round C8, C-38); that bash 5.2.21, zsh 5.9 and dash were recorded for ELOOP only, which each of them skips, going on to the later `gh`, where glibc stops; and that ESTALE, ENODEV and ETIMEDOUT, which glibc goes on past and the shells were not run on, are not known to be skipped by every search, and so fail the lookup with the rest; the C-35 row above now says what glibc does with each of twelve injected errors and what the shells do with an ELOOP `gh`; no other copy of the sentence stands in the three files; round C8 completes the record in D5 (the twelve errors and the shells' runs on the errors the lookup skips, C-38) | `design.md` D5; the C-35 row of round C6 |
| Codex 8 (P2, on `1c32667`, `design.md:457`, 2026-10-20T21:12:35Z): D6 relies on `json.loads` raising `ValueError` for a `number` of 5,000 digits, which is Python's limit of 4,300 digits on converting a string to an integer, present only from 3.10.7 and 3.11 while AGENTS.md says Python 3.10+, so on 3.10.0 to 3.10.6 such a body parses, its `number` passes the positive-integer check and a matching `url` passes too, against "API failures stay unknown", which makes it `api-error` | P2 | C-37: applied, design only, since the spec already requires the outcome: the parse passes `json.loads` a `parse_int` hook that receives each integer literal's text and raises, before converting it, when the text has more than 10 digits, a sign not counted (GraphQL's `Int`, which `number` is, is a signed 32-bit integer, at most 2,147,483,647, which has 10 digits); the parse then fails and the key is `api-error` by D6's rule that the parse catches every exception, so the outcome no longer depends on the interpreter's limit, and the cost of converting an integer literal within the 1 MiB body is bounded where it is quadratic; the node check also requires a `number` of at most 2,147,483,647; D6's account of the council's measurement is reworded as evidence, with the check of this round (the hook receives the literal's text, an exception raised there propagates unwrapped, a plain `json.loads` of 5,000 digits returns after `sys.set_int_max_str_digits(0)` and the hook raises, on Python 3.10.21, 3.11.16, 3.12.3, 3.13.15 and 3.15.0rc2); D11 gains the one test the ruling names, with the limit set to 0 where the interpreter has it, standing for 3.10.0 to 3.10.6, the 5,000-digit body giving `api-error` and the hook rejecting the literal before converting it, and the same test also pins the bound's edges (the hook accepts the texts 2147483647 and -2147483648 and rejects an 11-digit text, and a `number` of 2,147,483,648 fails the node check; round C8 adds the node check's accept edge, a `number` of 2,147,483,647, C-38), which the ruling does not name; the spec's "positive integer `number`" is not edited, and the design's upper bound is stricter than it only for a number that GraphQL's `Int` cannot hold | `design.md` D6, D11 |

### Re-read and Codex Findings (round C8)

Lane openRepoProject-3's read-only verifier read the delta `1c32667..129a4e2` on
2026-10-20 (its confirm read of round C7, `confirm-c7-findings.md`, brett-wip
7fd7b2cd6) and found no HIGH, no MEDIUM and four LOWs on this change, which the
lead accepted together (C-38). Codex has no new finding: it declined its request
on `129a4e2`, its usage limit being reached. The four edit `design.md` and this
file only: no spec file changed, `specs/project-overview/spec.md` is still the
file lane openRepoProject-4 agreed, sha256
`2ecd3d72b7cd32595d12f66206b7dd3c71df2cdfb9430122dd1ab0414ff1fe3e`, and
`specs/project-command/spec.md` is unchanged.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Lane openRepoProject-3's confirm read of round C7, four LOWs. LOW-1 (`design.md` D5): the rule skips ENOENT, ENOTDIR and EACCES, but D5 records the shells for ELOOP only, so those three skips rest on POSIX alone, although lane openRepoProject-3 reproduced bash, zsh and dash skipping all three. LOW-2 (D5, and the C-35 and C-36 rows): "each error" and "each injected error" are said where twelve were injected and D5 names eleven, ENOEXEC being unnamed. LOW-3 (D6 and D11): "only since 3.10.7 and 3.11" is said flatly, with no source, and 3.10.0 to 3.10.6 were not run. LOW-4 (D11): the test serves a `number` of 2,147,483,648 but none of 2,147,483,647, so a node check written `<` in place of `<=` passes it | LOW (four) | C-38: all four applied, design only, with no rule changed and no spec text. LOW-1: D5 records, crediting lane openRepoProject-3's reproduction (as a user other than root; bash 5.2.21, zsh 5.9, dash 0.5.12; `PATH=d1:d2`, the real `gh` in d2), that each shell, like glibc's `execvp`, ran d2's `gh` past a mode-000 directory (EACCES), a regular file where the entry's directory should be (ENOTDIR), a dangling link and a missing directory (ENOENT), and past a `gh` that is a directory or a regular file without execute permission, so that the skips of ENOENT, ENOTDIR and EACCES no longer rest on POSIX alone, and "recorded for ELOOP only" is reworded: the shells were run on ELOOP too, where each skips and glibc stops, and not on the other errors that fail the lookup; the writer re-ran this lane's round C6c prototype on 2026-10-20 and got the same results (the ruled lookup and each shell's `command -v gh` name d2's `gh` past each of those cases). LOW-2: D5 says that twelve errors were injected, one at a time, into the first `execve` of glibc 2.39's `execvp`, and names them as `inject-results.txt` of round C6c lists them: it stopped on ELOOP, EIO, ENAMETOOLONG, ENOMEM and E2BIG, went on past ENOENT, EACCES, ENOTDIR, ESTALE, ENODEV and ETIMEDOUT, and for ENOEXEC ran the first `gh` through its `sh` fallback, which is no stop; and D5 says what the lookup does with ENOEXEC: it never executes an entry, so an entry that is a regular file with execute permission is found, and whether it then runs is the child's matter, never the lookup's; the C-35 and C-36 rows above say twelve in place of each. LOW-3: D6 attributes the limit to Python's documentation, as Python's integer-string conversion length limit, added in 3.11 as a mitigation for CVE-2020-10735 and backported to 3.10.7 (read on 2026-10-20: the standard types page, "Added in version 3.11" and "added in security patch releases in versions before 3.12"; the 3.10 changelog, "Python 3.10.7 final", Security, gh-95778, "a mitigation for CVE-2020-10735"), and says that 3.10.0 to 3.10.6 were not run here, only emulated with `sys.set_int_max_str_digits(0)`; D6's check sentence and D11 say "emulates" in place of "stands for". LOW-4: D11's test also serves a `number` of 2,147,483,647, which passes the hook and the node check and gives a matched row, not `api-error`, so that the node check's `<=` edge is pinned; the writer ran a prototype of the hook and the node check's `number` clause on Python 3.10.21, 3.11.16, 3.12.3 and 3.13.15 (12 of 12 checks on each): D11's test as round C7 left it does not tell `<` from `<=`, since 2,147,483,648 gives `api-error` under both, and the added case does, since 2,147,483,647 gives `api-error` under `<`; the C-37 row above now says what its test pinned | `design.md` Context and its table, D5, D6, D11; the C-35 row of round C6 and the C-36 and C-37 rows of round C7 |

### Re-read and Codex Findings (round C9)

Codex re-reviewed `05a424a` on 2026-10-20 (22:45:56Z) with one P2 at
`design.md:484`, which the lead accepted (C-39); in applying it the lead found a
second point (C-40). Both edit `design.md` and this file only: no spec file
changed, `specs/project-overview/spec.md` is still the file lane
openRepoProject-4 agreed, sha256
`2ecd3d72b7cd32595d12f66206b7dd3c71df2cdfb9430122dd1ab0414ff1fe3e`, and
`specs/project-command/spec.md` is unchanged.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Codex 9 (P2, on `05a424a`, `design.md:484`, 2026-10-20T22:45:56Z): D6's parse passes `json.loads` only a `parse_int` hook, and `json.loads` accepts `NaN`, `Infinity` and `-Infinity` by default, so a 200 body that carries one in an otherwise unused field, such as a GraphQL `extensions` object, parses and its row can be `merged`, `open` or `not-found`, though a non-JSON body must be `api-error`; Codex asks for a rejecting `parse_constant` hook and a fixture | P2 | C-39: applied, design only, since the spec already requires the outcome (the added requirement's "A 200 body SHALL be UTF-8 JSON", `specs/project-overview/spec.md:461-462`, and `api-error` for a response "that cannot be decoded or parsed for any cause", :453-454): the parse also passes `json.loads` a `parse_constant` hook that raises for every text it is given, so that such a body fails the parse, wherever the constant stands, and its key is `api-error` by D6's rule that the parse catches every exception, on every supported Python; the writer checked on 2026-10-20 on Python 3.10.21, 3.11.16, 3.12.3, 3.13.15 and 3.14.7 that `json.loads` calls the hook with exactly those three texts and never for a string, `true`, `false`, `null` or a number (`1e999` included), that `NaNx` calls it on its `NaN` prefix, that `nan`, `-NaN`, `infinity`, `+Infinity` and `Inf` fail `json.loads` itself, and, with a prototype of D6's parse and node checks, that a valid answer carrying one constant in its `extensions` object gives `merged` with the `parse_int` hook alone, as round C8 left the parse, and `api-error` under this one, the same answer without the constant giving `merged` under both; D11 gains one test, for this ruling and C-40 together, with one fixture per constant, as the ruling words it, each in an `extensions` object the parse never reads; D6 also says that a float literal needs no bound, as C-40's "Not ruled" has it, with the writer's timing (a literal of 1,048,560 bytes, in its fraction, its integer part or before an exponent, parsed in under 10 ms on each interpreter, the slowest 9.8 ms, where the ruling's note says under 2 ms) | `design.md` Context and its table, D6, D11 |
| C-40 (the lead's point, found in applying C-39): D6 says that a body that cannot be decoded or parsed is `api-error` but not who decodes it; given bytes, `json.loads` detects UTF-8, UTF-16 and UTF-32 and decodes with the `surrogatepass` error handler, so a body that is not UTF-8, and so not what the spec requires, would parse and could be answered | ruling | C-40: applied, design only: the parse decodes the body's bytes itself, with Python's UTF-8 codec and its default `strict` error handler, and passes `json.loads` that string, never the bytes, so that a body in UTF-16 or UTF-32, a string holding ED A0 80 (an encoded surrogate) and a body that begins with a UTF-8 byte order mark each fail and are `api-error` (RFC 8259 section 8.1 allows a parser to treat the byte order mark as an error); the writer re-ran the lead's `probe.py` and `probe2.py` with `-I` on Python 3.10.21, 3.11.16, 3.12.3, 3.13.15 and 3.14.7, with 15 of 15 on `probe2.py` and 16 of 19 on `probe.py` on each, the three FAIL lines of `probe.py` being the probe's own expectations (`NaNx` calls the hook on its `NaN` prefix; UTF-16 and UTF-32 without a byte order mark decode as UTF-8 and then fail the string parse), and D6 records what it saw: `json.loads` of bytes parsed UTF-16 and UTF-32 (little-endian, big-endian and with a byte order mark), the ED A0 80 body and the byte order mark body, and the strict decode raised `UnicodeDecodeError` for the UTF-16 and UTF-32 bodies with a byte order mark and for ED A0 80 and accepted the other four, which `json.loads` of the string refused with `JSONDecodeError`, as it did the UTF-8 byte order mark; D11's one test serves each as an otherwise valid answer that gives `merged` without the rule and `api-error` with it: UTF-16 and UTF-32, each little-endian without a byte order mark and with one (the ruling says only "UTF-16 and in UTF-32"; the forms are the writer's choice, one for each of the decode's failure and the parse's), ED A0 80 in a string of an `extensions` object, and a UTF-8 byte order mark first; it also serves the same answer in plain UTF-8, which gives `merged` (a control the ruling does not name, so that each failure comes from the rule and no other fault of the answer), and the fake `gh` writes a body as bytes, the seam these fixtures need; the test is no scenario | `design.md` Context and its table, D6, D11 |

### Re-read and Codex Findings (round C10)

Codex re-reviewed `f34dfe2` on 2026-10-20 (read 23:21Z) with one P2 at
`design.md:381` (2026-10-20T23:14:10Z), on which the lead ruled (C-41), and lane
openRepoProject-3's read-only verifier read the delta `05a424a..f34dfe2` (its
confirm read of round C9, `confirm-c9-findings.md`, brett-wip 1d878441d) and
found no HIGH, one MEDIUM and four LOWs, which the lead accepted (C-42, C-43).
They edit `design.md`, this file and `tasks.md` only: no spec file changed,
`specs/project-overview/spec.md` is still the file lane openRepoProject-4
agreed, sha256
`2ecd3d72b7cd32595d12f66206b7dd3c71df2cdfb9430122dd1ab0414ff1fe3e`, and
`specs/project-command/spec.md` is unchanged.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Codex 10 (P2, on `f34dfe2`, `design.md:381`, 2026-10-20T23:14:10Z): D5 starts the `gh` child in `/`, and `gh` resolves a relative `GH_CONFIG_DIR` against its own working directory, so a caller whose credentials sit under a relative path reads `gh-unauthenticated`; Codex confirmed it with `gh` 2.96.0 and asks to resolve the variable against the original working directory before switching directories, or otherwise to preserve its path semantics | P2 | C-41: declined as a design change, kept as a residual. The ruling as first issued had D5 join each of `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` and `HOME` that is not empty and does not begin with `/` to the realpath of the working directory; the lead amended it before it was applied, on lane openRepoProject-3's finding that `specs/project-overview/spec.md:404-411`, agreed by lane openRepoProject-4, has the `gh` child run in the filesystem root with every other variable passed on unread: anchoring the three would read and rewrite them, and the spec would need an edit, which is not made. A second reason is lane openRepoProject-4's offline check on `gh` 2.96.0 on 2026-10-20, with fake tokens: starting in `/` keeps the caller's working directory, which may lie inside a scanned repository, from supplying `gh`'s configuration (an empty `HOME` makes `gh` read `./.config/gh` from its working directory, which found a planted token from the caller's directory and none from `/`; an empty `GH_CONFIG_DIR` or `XDG_CONFIG_HOME` is treated as unset) and from receiving what `gh` writes (it rewrote `hosts.yml` into its multi-account form and created `config.yml` in the directory it used). D5 now says that a relative `GH_CONFIG_DIR` or `XDG_CONFIG_HOME`, or a relative or empty `HOME`, resolves against `/`: normally that names no configuration and the rows are `unavailable` with reason `gh-unauthenticated`, and if the resolved path exists `gh` reads the configuration there; an absolute path works; the writer's own run on `gh` 2.96.0 found each of the three relative values from the directory it was relative to, missed it from `/`, and found each made absolute from `/`. Risks gains the residual, naming `SSL_CERT_FILE` and `SSL_CERT_DIR` as the same kind of case and recording the lead's check that a `gh` configuration holding `http_unix_socket` made `gh api` send its request as plain HTTP over that socket with the token in the clear, so that a configuration planted in a world-writable directory under `/` could capture the token and serve a wrong answer, which authorizes nothing (D10); D11 pins by one short test that `GH_CONFIG_DIR`, relative or empty, reaches the fake `gh` byte for byte with working directory `/`; the README bullet of Impact adds, to the next step for `gh-unauthenticated`, to make a relative `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` or `HOME` absolute | `design.md` Context and its table, D5, D11, Risks; Impact (README bullet) |
| Lane openRepoProject-3's confirm read of round C9, MEDIUM-1 (`design.md:572-578`, :550-551): D6 says "a positive integer `number`" but not by type, and C9's "no field the parse reads is a float" leans on it; a check written `isinstance(n, int)` accepts JSON `true`, which the kept row would print as a boolean `number`, and one written `n == int(n)` accepts `1.0` and `true` and raises `OverflowError` on `1e999`, outside the parse's catch, so that it reaches exit 2 | MEDIUM | C-42: applied, design only, since `specs/project-overview/spec.md:466` already says "a positive integer": `number` is accepted only when `type(number) is int`, never a `bool` and never a `float`, and from 1 to 2,147,483,647; every check D6 makes on the parsed answer runs inside the parse's catch-everything boundary, so that a check that raises is `api-error` too; D11's 2,147,483,648 test gains `true`, `1.0` and `1e999` as `number`, each with a `url` ending `/pull/1`; the writer prototyped it with `-I` on Python 3.10.21, 3.11.16, 3.12.3, 3.13.15 and 3.14.7, with identical output: by type, `api-error` for `true`, `false`, `1.0`, `1e999` and 2,147,483,648 and `merged` for 2,147,483,647 and for 7; by `isinstance(number, int)`, `true` gave `merged`; by `number == int(number)`, `true` and `1.0` gave `merged` and `1e999` raised `OverflowError` outside the boundary | `design.md` Context and its table, D6, D11 |
| Lane openRepoProject-3's confirm read of round C9, four LOWs. LOW-1 (D6): `1e999` is named but not what a body that carries one does. LOW-2 (D6): an escape of a lone surrogate is unruled, and D6 does not say why it is harmless. LOW-3 (D2, optional): D2 does not say how its two Git children's output is decoded. LOW-4 (D6, D11 and the C-39 row of round C9): (a) "A prototype of this parse and of D6's checks on a node" says more than the prototype's `answer()` checks; (b) D6 lists six UTF-16 and UTF-32 forms and D11 serves four without saying they are chosen; (c) "the five interpreters above" is ambiguous between two lists | LOW (four) | C-43: all four applied in `design.md`, with no rule changed beyond LOW-3's and no spec text. LOW-1: D6 says there is no `parse_float` hook, by decision, since a float literal outside the range of a double, such as `1e999` or `-1e999`, is grammatical JSON (RFC 8259 section 6 leaves range to the implementation, unlike `NaN`) and parses as `inf`: in a field the parse never reads the key is still answered, and as `number` it fails C-42's type check; the writer's prototype answered `merged` for `1e999` and `-1e999` in an `extensions` object on the five interpreters. LOW-2: D6 says that the escape (a backslash, `u` and D800, written in prose here and in D6) is ASCII, valid UTF-8 JSON, and parses, that no field the row keeps can hold one, `state`, `number`, `url` and `head_sha` being closed forms and the two open fields, `baseRefName` and `errors[].type`, being compared and never kept, so that C-40 concerns the body's bytes and not its strings; the prototype answered `merged` for that escape in an `extensions` string. LOW-3: D2 decodes each remote-target read's output as strict UTF-8, never with `surrogateescape`, an output that does not decode failing the read, which is `remote-target-unread` (the spec's "fails for any other cause", `specs/project-overview/spec.md:387-388`; the ruling cites :388-389), so a `baseRefName` can equal only a merge ref that is valid UTF-8 text. LOW-4: (a) D6 says "A prototype of D6's parse and of the node checks its fixtures need"; (b) D11 says its four fixtures are chosen from D6's six forms: little-endian, without and with a byte order mark, for each; (c) D6's C-39 paragraph names Python 3.10.21, 3.11.16, 3.12.3, 3.13.15 and 3.14.7. The ruling also asks for (a) in the C-39 row of round C9 above; that row stays as written, because lane openRepoProject-4's pin keeps lines 1252 to 1330 of this file byte for byte, and this row is its correction: that row's "this parse and of D6's checks on a node" is read as D6 now words it | `design.md` Context and its table, D2, D6, D11 |

### Re-read and Codex Findings (round C11)

The lead ruled on lane openRepoProject-3's and lane openRepoProject-4's
planted-configuration point against round C10's residual (C-44, refined at
23:5xZ on lane openRepoProject-3's six points, which found no hole in its core),
and lane openRepoProject-3 corrected the reason that `LD_LIBRARY_PATH` is left
out of it. The ruling edits `design.md` (the Context and its table, D4, D5, D11
and Risks), this file (Status, the citation key, Impact's README bullet and
Decisions) and `tasks.md`, and one spec file: its edit to
`specs/project-overview/spec.md` was HELD for lane openRepoProject-4 as one
file, written in the working tree and not committed, until its YES of 2026-10-21
(01:0xZ). Round C11b then committed it (`2b89bfc`) with the two edits that the
lane asked for and nothing else changed: "names" became "may name" in the
rationale, and a relative `XDG_CONFIG_HOME` joined the AND. The committed spec
file's sha256 is now
`ce57ed5eca8085d1edc5687c7b25b10c5c603e777694bda13c481f6fe94be19a` (it was
`2ecd3d72b7cd32595d12f66206b7dd3c71df2cdfb9430122dd1ab0414ff1fe3e` before this
round), and `specs/project-command/spec.md` is unchanged. The edit changes no
scenario count (36 and 10, 46 in all). Lane openRepoProject-4 agreed in
principle at 23:5xZ, on the lead's account, on two conditions that the committed
file keeps: `:13-39` stays untouched and the new sentence says that the three
values "hold no credential value", and nothing before `:243` moves. Line numbers
of the spec below are those of the committed file; `design.md` cites it at
`:387-388`, `:459-460`, `:467-468` and `:472`, the last three having been
`:453-454`, `:461-462` and `:466` in the file before the edit moved them by 6
lines.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Lane openRepoProject-3's and lane openRepoProject-4's planted-configuration point on round C10's residual (C-41 as amended): from `/`, a relative `GH_CONFIG_DIR` or `XDG_CONFIG_HOME`, or a relative or empty `HOME`, normally names no configuration, but where the resolved path exists `gh` reads the configuration there, and a tree under `/` that any local user can write, such as `tmp`, `var/tmp` or `dev/shm`, would let another user plant one; the lead's check on `gh` 2.96.0 found that a configuration whose `config.yml` held `http_unix_socket` made `gh api` send its request as plain HTTP over that socket, with the token in the clear, so that "never a wrong answer" did not cover the token | ruling | C-44: applied in `design.md` and in the spec edit, committed on lane openRepoProject-4's YES (the last row). The lookup of `gh` counts as failing when any of `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` and `HOME` is set to a non-empty value whose first byte is not `/`; a failed lookup gives what one already gives, every keyed row `unavailable` with reason `gh-unavailable`, whether or not its key is past the 64th, and no child starts; an empty or unset value is not refused; the three hold no credential value, are read only for that test, and every variable a child gets is passed unchanged, `GH_TOKEN`, `GITHUB_TOKEN` and the proxy variables unread. D5 replaces C-41's residual with this rule and keeps the evidence: the lead's socket check, and lane openRepoProject-4's checks of empty values and of `gh`'s writes. D4 and D5 name the cause where they list what a failed lookup gives, and so does the Decisions paragraph on run-wide unavailability. The README's next step for `gh-unavailable` gains "or make a relative `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` or `HOME` absolute" and C-41's same text on `gh-unauthenticated` moves there. The reason stays `gh-unavailable`: it already covers two causes, and a distinct reason would cost an enum value for one cause that the README makes discoverable. No separate open question goes to Brett Heap: #29's ratification summary names this change from C10's residual and gives the token capture as its reason | `design.md` Context and its table, D4, D5; Impact (README bullet); Decisions (run-wide unavailability); `project-overview` delta (Requests, Results) |
| C-44, as refined on lane openRepoProject-3's six points (23:5xZ): the test must hold whichever of the three `gh` would use and not depend on its precedence; an empty or unset value; the cause named; the general class of relative paths; and the spec edit's place | ruling | C-44 as refined: applied as worded. The test is on the raw bytes, by design: ` /x`, `~/x` and `.` are refused, and a relative `XDG_CONFIG_HOME` or `HOME` beside an absolute `GH_CONFIG_DIR` is refused too, a deliberate, fail-safe over-refusal that does not depend on `gh` keeping its order; the writer's prototype of the test, on `os.environb` and on `os.environ`, agreed with the rule on 18 cases on Python 3.10.21, 3.11.16, 3.12.3, 3.13.15 and 3.14.7. An empty or unset value is not refused: the writer's offline run on `gh` 2.96.0 found that with all three variables unset, and with all three empty, `gh` read `./.config/gh` from its working directory, found from the directory that held it and missed from `/`, so from `/` it reads `/.config/gh`, which only root can create on a normal system. `gh-unavailable` names the cause in the spec's Results paragraph and in D4, D5 and the README's step, so that a person with a relative `HOME` does not go looking for `gh` on `PATH`. Risks names the general class, that `/` re-anchors every relative path in the environment, and leaves out `SSL_CERT_FILE`, `SSL_CERT_DIR` and `LD_LIBRARY_PATH`, each for its own reason (next row). The spec edit is placed at `:411` and after, so that nothing before `:243` moves, and `:411`'s "passed on unread" becomes "passed on unchanged" in the same sentence, which says that the three "hold no credential value", as `:26-28` reads, with `:13-39` untouched | `design.md` D4, D5, D11, Risks; `project-overview` delta (Requests, Results) |
| Lane openRepoProject-3's correction of the reason that `LD_LIBRARY_PATH` is left out (00:0xZ): C-44 as first worded said that each of the two named cases needs more than a planted file, but a library planted where a relative entry resolves under `/` runs inside a dynamically linked `gh` and needs nothing more | correction | applied in Risks: `LD_LIBRARY_PATH` is left out because it is not `gh`'s configuration and because a relative entry is already the caller's own hazard in every directory they run anything from, running in `/` only fixing where it resolves; release builds of `gh` are static, so the case needs a distribution build (the `gh` 2.96.0 binary checked here is static: `ldd` prints "not a dynamic executable"). `SSL_CERT_FILE` and each element of `SSL_CERT_DIR`, which Go's `crypto/x509` splits on `:`, keep their own reason, that a planted CA also needs a network position to be of use; lane openRepoProject-4 read that from Go's source, and no test of `gh` shows it | `design.md` Risks |
| Lane openRepoProject-4's check of extensions (offline, `gh` 2.96.0, a fake token): run in `/` under a relative `HOME` beside an absolute `GH_CONFIG_DIR`, `gh` listed planted `gh-api` and `gh-zzz` extensions and ran `gh zzz` by its own name, but `gh api` ran `gh`'s own client, and `gh` wrote no file under that `HOME` | evidence | recorded in D5 and Risks: D5's argv always begins with `api`, so it never runs an extension, and the rule's refusal of that case is deliberate over-refusal, not a fix for a demonstrated hole | `design.md` D5, Risks |
| The tests of the AND, and of the rule beyond it | ruling | applied in D11: C-41's short test is replaced by one test of C-44's rule, with the fake `gh` first on `PATH` and recording `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` and `HOME` as set or unset and byte for byte. Refused, each giving both rows `gh-unavailable` and no child: `GH_CONFIG_DIR=.gh-config`, `XDG_CONFIG_HOME=cfg`, `HOME=h`, each of the last two beside an absolute `GH_CONFIG_DIR`, each of the three beside the other two absolute, and ` /x`, `~/x` and `.` as `GH_CONFIG_DIR`. Not refused, each starting the children and recording every value unchanged with `/` as the working directory: an absolute `GH_CONFIG_DIR`, an empty `GH_CONFIG_DIR`, an empty `XDG_CONFIG_HOME` and an empty `HOME`, all three unset, and all three absolute. With 70 keys and a relative `GH_CONFIG_DIR`, all 70 are `gh-unavailable`, none `request-cap`. No test runs a real `gh`. After lane openRepoProject-4's YES, D11's account of the AND names the cases it takes: `GH_CONFIG_DIR=.gh-config`, `XDG_CONFIG_HOME=cfg`, a relative `HOME` beside an absolute `GH_CONFIG_DIR`, and the absolute and the empty `GH_CONFIG_DIR` | `design.md` D11 |
| The spec edit, committed | ruling | Committed (`2b89bfc`) on lane openRepoProject-4's YES of 2026-10-21 (01:0xZ), which it gave after checking the held sha256 `75d4bc0215b1dc51ed972306f9ebfa89c54dd6fa8ed6d806c703d2620ec5078a`, `:1-410` byte for byte against its `05a424a` pin (so that `:13-39` and every range it cites, all at or before `:243`, hold), that its Q17 D needs no text change (the re-pin is the sha only) and that "hold no credential value" is present. The committed diff is the held file plus the two edits the lane asked for, and nothing else: "names" became "may name" in the rationale at `:417` ("such a value may name a configuration other than the caller's"), the old wording being inexact twice, since a relative `HOME` beside an absolute `GH_CONFIG_DIR` names no `gh` configuration and, for a caller whose own working directory is `/`, a relative value names the caller's own (lane openRepoProject-3 made the same point; the three lines are re-wrapped and the line count is kept); and the AND at `:610` also takes "separately when `XDG_CONFIG_HOME` is set to a relative value", so that a test that leaves `XDG_CONFIG_HOME` out of the check fails. The whole edit is one sentence in the Requests paragraph after "every other variable passed on unchanged" (`:411-417`), naming the three variables, the raw-byte test and the failed lookup and saying that they "hold no credential value"; one clause in the Results paragraph (`:478-480`) that names this cause where it says when the lookup fails; and one AND on "No gh, or a gh without authentication" (`:610`): with `GH_CONFIG_DIR` set to the relative `.gh-config`, separately with `HOME` relative beside an absolute `GH_CONFIG_DIR`, and separately with a relative `XDG_CONFIG_HOME`, no `gh` child starts and both rows are `gh-unavailable`, while with an absolute or an empty `GH_CONFIG_DIR` the children start. "unread" became "unchanged" at `:411` deliberately: "unread" was never exact, since the lookup reads `PATH` and now also tests the three configuration paths, and "unchanged" says what the child receives; credential values stay unread under `:26-28` ("read, test, infer, print and forward no credential value, the caller's environment excepted, which it passes to a `gh` child unread"), which lane openRepoProject-4's Q17 D restates, so nothing is weakened: the overview reads no credential value, and every variable reaches the child as the caller set it. No scenario is added, `:1-410` is byte-identical to the file at 4013734, and `specs/project-command/spec.md` is unchanged | `project-overview` delta (Requests, Results; "No gh, or a gh without authentication"); `tasks.md` 1.3, 1.4, 1.5 |

### Re-read and Codex Findings (round C12)

Lane openRepoProject-3's read-only verifier read the delta `f34dfe2..21846c3`
(its confirm read of rounds C10 and C11, `confirm-c11-findings.md`, brett-wip
77da4ac71) and found no HIGH, no MEDIUM and six LOWs, all in the design, with
its checks 1 to 7 passing: the spec diff is `2b89bfc` alone, C-42 reproduces,
the C-44 rule agrees on 38 of 38 cases, the moved cites land, and `validate`
passes 8 of 8. The lead accepted all six (C-45, 2026-10-21). They edit
`design.md` and `tasks.md`, and this file only for Status, the citation key, the
Decisions list and this section: no spec file changed,
`specs/project-overview/spec.md` is still the file lane openRepoProject-4
agreed, sha256
`ce57ed5eca8085d1edc5687c7b25b10c5c603e777694bda13c481f6fe94be19a`, with its 36
scenarios, `specs/project-command/spec.md` is unchanged with its 10, and the
count stays 46. Lines 1252 to 1385 of this file, rounds C6 to C11, are
unchanged, and this section follows them. To hold each paragraph's line count,
Status drops "(every keyed row `gh-unavailable`)", "all" before "on lane
openRepoProject-4's agreement" and "a relative configuration path kept unread"
from C-41's note, and says "the lead's three points" for "three points found in
applying it"; the Decisions list drops its two pointers to the section titles of
rounds C5 and C6 and names "rounds C5-C12" once; and the citation key says
"2026-10-20 and 2026-10-21".

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Lane openRepoProject-3's confirm read of rounds C10 and C11, L1 (design D6, at :635; a real defect): the sentence on a JSON escape of a lone surrogate holds a stray two-letter placeholder where its reason should stand (the words "it is ASCII,", the placeholder, then "which concerns the body's bytes and not its strings, leaves it"), so that C-43's LOW-2 sentence did not land as worded; it has stood since `af9a5a0`, and the sentence never says that the escape parses | LOW | C-45: applied as worded: D6 now reads "it is ASCII, valid UTF-8 JSON, and parses, and C-40, which concerns the body's bytes and not its strings, leaves it", the content that round C10's pinned LOW-2 row records. The lead's verification of round C10 read D5 and the node bullet, not this sentence. Before committing, the writer grepped `design.md`, `proposal.md` and `tasks.md` for the stray placeholder, the usual placeholder words, a marker between two at signs, a bracketed ellipsis, a doubled word and a doubled comma or period, and read each paragraph and list item for a cut-off ending: no other placeholder and no cut-off sentence remains; the ellipses that remain are an example URL and a form of URL, in the Context's list of facts about `project` and in D3, a GraphQL spread in D5's query and quotations in this file, and the Speckit Handoff lines of `tasks.md` end without a full stop by their template | `design.md` D6 |
| L2 (design Context, :47-51): a present-tense statement the committed spec no longer makes: C-41 was kept "since the spec has the `gh` child run in the filesystem root with every other variable passed on unread", and the committed spec says "unchanged" (C-44, `2b89bfc`) | LOW | C-45: applied: the Context says "as the spec then had it, the `gh` child ran in the filesystem root with every other variable passed on unread" and its next sentences, on C-44, already say that the committed spec now says "unchanged"; the Context's account of C-45 and its table gain an entry | `design.md` Context and its table |
| L3 (tasks 1.5): "and in round C11 on the committed tree and again with the held spec file in place": the spec is no longer held, and 1.5 records no validation after `2b89bfc` | LOW | C-45: applied: 1.5 records the three validation commands on the committed files, at 21846c3 (valid with the two INFO lines, 8 of 8, every artifact done, as lane openRepoProject-3 also found) and at round C12's head, in place of the run with the held spec file; 1.1 names C-45, and 1.3 carries a round C12 clause and this section in its list. A commit cannot hold its own sha, so 1.5 says "that round's head" and the head is in the round's report | `tasks.md` 1.1, 1.3, 1.5 |
| L4 (D2 :297-299 and D11): LOW-3's decode failure is in D2's body but not in D2's own list of failures, and nothing pins it: (a) the list reads "exits nonzero, reaches its budget, overruns its output cap or is stopped at the deadline"; (b) D11's counting `git` wrapper can set an exit status and a stderr line or hold past a budget, but not emit chosen stdout bytes, so no test shows a merge ref with the byte FF giving `remote-target-unread`, though C-40's decode has a D11 test; (c) "which is the spec's 'fails for any other cause'" holds by analogy with `specs/project-overview/spec.md:371-373` ("a longer one, which fails the read"), not quite by the letter | LOW | C-45: applied as worded: D2's list now reads "exits nonzero, reaches its budget, overruns its output cap, gives output that does not decode as UTF-8 (C-43) or is stopped at the deadline"; D11 gains one fixture, placed after the counting wrapper's bullet, a repository whose merge target's `branch.<target>.merge` is `refs/heads/` followed by the byte 0x80, set with `git config`, which gives its queried rows `unknown` with reason `remote-target-unread`, starts no second read and no request for them, and sits beside a second repository whose merge ref is valid UTF-8 and is answered as usual, so that the byte is the only fault; a `remote.<name>.url` that holds the byte is the same fixture for the second read. The fixture needs no wrapper control: the writer saw, in a scratch repository on Git 2.43.0, that `git config` took the byte, that `git for-each-ref` with D2's format and `git remote get-url` each printed it, and that `bytes.decode("utf-8")` of the first output raised `UnicodeDecodeError` ("invalid start byte"). It is no scenario, as the ruling words it: the spec's "fails for any other cause" (`specs/project-overview/spec.md:387-388`) already requires the outcome, and lane openRepoProject-3's note (c) is recorded here, not acted on: the anchor needs no spec edit | `design.md` D2, D11 |
| L5 (D5 :446-447): "a value whose first byte is not UTF-8" is imprecise: EF is a valid UTF-8 lead byte, and the prototype (D5) refuses both FF and EF because neither is `/` | LOW | C-45: applied as worded: D5 now reads "a value whose first byte is any byte other than `/`, a non-ASCII byte included"; the rest of the paragraph, including the prototype's 18 cases, is unchanged, and its aside that a decoded string leaves a first byte that is not UTF-8 as no `/` is left as it stands, since it describes the string writing's decoding and not the rule | `design.md` D5 |
| L6 (Risks, optional): the general class leaves out three more relative-path variables that `gh` reads: its binary holds `XDG_DATA_HOME`, `XDG_STATE_HOME` and `XDG_CACHE_HOME` (one string each), D5's extension check covers the data directory only through a relative `HOME`, so that a relative one of the three alone is neither refused nor named, and the design does not say that the reasons look like the extension check's | LOW (optional) | C-45: applied: Risks names the three in its general class and gains one nested bullet with three sub-bullets, each saying only what is known. The writer's offline checks on `gh` 2.96.0 on 2026-10-21, with a fake token that no output held, the working directory a scratch directory standing for `/`, and, where a request was answered, a small server on a Unix socket standing in for the API (`gh` reaches it through `http_unix_socket`, as the lead's check in D5 showed): `gh help environment` documents `XDG_CONFIG_HOME` and none of the three, and the binary holds each name once (the writer repeated lane openRepoProject-3's count). Data: under a relative `XDG_DATA_HOME` that held planted `gh-api` and `gh-zzz` extensions, `gh zzz` ran the planted extension, while `gh api --help` and D5's argv, whether the request was refused at a closed proxy port or answered by the stand-in, ran `gh`'s own command and client and never the planted `gh-api`, and `gh` wrote no file there; lane openRepoProject-4's check, in D5, had run the same under a relative `HOME`. State: `gh help environment` documents the update check (once every 24 hours) and the two switches that D5 sets, and does not name the directory; D5's argv wrote no file under a relative or an absolute `XDG_STATE_HOME`; the writer could not make the update check itself run offline (in a pseudo-terminal, with the switches unset and a stand-in for the release endpoint, no request for it came), so the bullet says "as far as `gh` documents them" and that the check's use of the directory is not observed. Cache: `gh api --cache 1h`, answered by the stand-in, wrote a file under an absolute `$XDG_CACHE_HOME/gh`, and `gh api` without it, which D5's argv is, wrote none under a relative or an absolute value. No rule changes: D5's refusal stays on the three configuration variables, and the README's next steps do not name these three, as they do not name the others | `design.md` Risks |

### Re-read and Codex Findings (round C13)

Reader RC, a read-only adversarial reader of lane openRepoProject-5, read this
change at `e11d755`: D1 to D4 and D7 to D10, D11's seams against the 13
scenarios of the ADDED requirement, and the three MODIFIED blocks against change
2's text (`RC-findings.md`, in the lane's scratch). It found no HIGH, five
MEDIUM (M1 to M5) and six LOW (L1 to L6), and re-raised no settled ruling. It
also found the three `project-overview` blocks and [E] adding only to the text
they modify, the composed `project-overview` at 13 requirements and 77 scenarios
with no scenario name twice, and the citations of D1 to D4 and D7 to D10 landing
on their quoted text. It could not verify Git 2.36 (only 2.43.0 was on its
bench), the runner's `gh` itself (no Actions run), live `gh` answers (task 2.5)
or whether feature 005's code writes a scan error with a count of 0 at an expiry
(005 has its spec only); the writer had Git 2.43.0 alone too.

The lead ruled on 2026-10-21 (12:3xZ, on team-01h; `rulings-2026-10-20.md`,
"Rulings on the 2026-10-21 review wave, part 1"): C-46 (M4, M5 and L6) and C-47
(L2's design part, L3, L4's design part and L5) are applied, and C-48 (M1, M2,
M3, L1 and L4's spec part) is HELD for lane openRepoProject-4 as one file
together with amendment A1's alignment, since M1 touches "Expiry cancels queued
and in-flight requests", which Q16 B also reaches. This section records C-48 as
held, with no spec text and no design text, and the other rows apply as the
ruling words them. Round C14 then committed C-48's spec text on lane
openRepoProject-4's YES of 2026-10-21 (`c0062f9`); the five held rows below say
so, and its own section records it. Round C13 edits `design.md` (the Context and
its table, D2, D3, D10 and D11), this file (Status, the citation key, Impact's
README bullet, the Decisions list, Open Question 1 and this section) and
`tasks.md` (1.1, 1.3 and 1.5, in place, 45 lines still). No spec file changed:
`git diff e11d755 -- '*/specs/*'` is empty, `specs/project-overview/spec.md` is
still the file lane openRepoProject-4 agreed, sha256
`ce57ed5eca8085d1edc5687c7b25b10c5c603e777694bda13c481f6fe94be19a`, with its 36
scenarios, `specs/project-command/spec.md` is unchanged with its 10, and the
count stays 46.

Lines 1252 to 1417 of this file, rounds C6 to C12, are unchanged (`cmp` against
`e11d755`), and this section follows them; lines 334-345, 367-370 and 430-438
are `cmp`-identical to `e11d755` too, as are `tasks.md` lines 20-23; and every
paragraph of this file before line 1252 keeps its line count, the five edits
there (Status at 5-26, the citation key at 45, Impact's README bullet at
377-395, the Decisions list at 655-678 and Open Question 1 at 1070-1077) each
replacing as many lines as they had. To hold the counts, Status says "rounds C5
and C6 (C-24 to C-34: ...)" for the two longer clauses of those rounds, and
drops "a `parse_int` hook", "a `parse_constant` hook" and "a residual" from
C-37, C-39 and C-41, "`project-overview`" before "spec edits", and "one" and
"with two edits" from C-44's spec edit, and moves "with no spec edit" to the
end, where it covers both rounds; the Decisions list shortens the descriptions
of C-35 to C-40, drops "of `e198548..67e43ae`" and the pointer to the section
titles; the README bullet says "the next steps" for "what the person can do
next", "run it again", "on squash-merged branches" dropped, "a fork" for "the
person's fork" and "They are advice" for "These next steps are advice", with a
few smaller word changes in the same lines; and Open Question 1 says "Change 1:"
and "change 2:" for "Change 1 says" and "change 2 says", "an" for "any" existing
enum and "with a new, closed `state` enum", and words its recommendation in
fewer words, which it keeps.

The writer ran these on 2026-10-21, on Git 2.43.0, in a scratch repository and
with `project` as it stands at `961c405`: the identity pattern on thirteen URL
shapes (L2), `git ls-remote github.com/acme/widget` against a local bare
repository at that path (L2), the two remote-target reads of a password-bearing
remote under `transfer.credentialsInUrl` `die` and `warn` and beside a clean
merge-target remote (L3), and a simulation of the runner's `PATH` layout against
a directory of links (M4). Validation, run before the round's edits were
committed and again at its head (a commit cannot hold its own sha; the head is
in the round's report):
`/usr/bin/openspec validate add-project-overview-remote-merge-status --strict`
reports the change valid with its two INFO lines,
`/usr/bin/openspec validate --all --strict` passes 8 of 8, and
`openspec status --change add-project-overview-remote-merge-status --json` shows
every artifact done. The added text holds no non-ASCII character, bidi control,
host path or literal backslash-u, and a grep of the three files for placeholders
found none.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Reader RC's M4 (D11's seams cannot keep `gh` off `PATH` in CI, where `gh` sits beside `git`): D11 builds its `PATH` on `question_env()` (tests:154-170), the fake bin directory plus the directories of `bash`, `git` and the interpreter; the `tests` workflow runs only on `ubuntu-latest` (main `e9d6711`), whose image installs `gh` at `/usr/bin/gh`, beside `/usr/bin/git`; so the three parts of "No gh, or a gh without authentication" (its WHEN and its planted-`gh` AND) and of "The request bounds" (its last AND) that need no `gh` on `PATH` would find the runner's real `gh`, start it and read `gh-unauthenticated` or `api-error` with `remote.requests.performed` 2 or 64, not `gh-unavailable` and 0, while on a bench that keeps `gh` apart from `git` the same tests pass; D11 says "No test needs `gh` installed", and its converse, a test that needs `gh` absent, is not provided for | MEDIUM | C-46: applied as the ruling words it, which is wider than RC's fix (the runs that need `gh` absent): the test `PATH` of every run holds the fake bin directory and one directory of links to `git`, `bash` and the interpreter, never their whole directories, and the counting `git` wrapper runs the real `git` by the absolute path of its link; before a run that needs `gh` absent the test asserts `assert_absent_from_path(env, "gh")` (tests:200, a helper the file already has), and where the fake is present `assert_fake_on_path(env, "gh")` (tests:196). D11 says the runner's layout is inferred and not run: the image's `install-github-cli.sh` does an `apt-get install` of cli/cli's Linux `.deb`, and cli/cli's `.goreleaser.yml` has `nfpms` with `bindir: /usr` and `binary: bin/gh` (RC's copies of both files; no Actions run was made). The writer's simulation, with `git`, `bash`, `gh` and an interpreter in one directory as on the runner: `question_env()`'s `PATH` found that `gh`; the directory of links found none, and `git`, `bash` and the interpreter each ran through its link, `git for-each-ref` on a scratch repository included | `design.md` D11 (the `PATH` bullet and its sub-bullets), Context and its table |
| RC's M5 (the fake `gh`'s one record per run cannot show children that were stopped or signalled): D11's fake appends one JSON record per run that holds its start and end times and no pid or process group, and a record that carries the end time is written only when the fake exits on its own; a child stopped at its limit, at the expiry or on a signal is killed by SIGTERM or SIGKILL and writes none, so the record cannot show that every child started before the expiry and none after it, when a held child started, or which process groups to probe ("A signal while requests run" needs them, as change 2's signal test probes "every group the wrapper recorded", APO design.md:642), and counting overlaps from start and end times misses killed children; the stops of "API failures stay unknown" (the held child at 5 s), "Expiry cancels queued and in-flight requests" and [E]'s new scenario (`specs/project-command/spec.md:179`) have the same gap | MEDIUM | C-46: applied: the fake `gh` writes a start record the moment it starts, before it answers or holds, with the argv, the environment fields, its pid and process group and its start time, and an end record when it exits on its own (pid, end time, exit status). The signal, expiry, API-failure and [E] tests read the start records and probe each recorded group with `os.killpg(pgid, 0)`; the concurrency bullet reads start and end records for runs whose children end on their own, and a stopped child's start record and group probe otherwise. The writer adds one detail that RC's fix does not state: each record is one JSON line written in one call on a descriptor opened for append, so that the records of concurrent children do not interleave. The C-44 test's "the fake `gh`'s record empty" now reads "no start record of the fake `gh`" | `design.md` D11 (the fake `gh` bullet, the C-44 test bullet and the concurrency bullet) |
| RC's L6 (the `gh` children of in-process runs are outside the network guard): the audit hook binds the test interpreter and not its children, the proxy variables are set only for subprocess runs, and several in-process runs start `gh` children (the expiry scenario, the AND at concurrency 1 and the `set_int_max_str_digits(0)` test), each given the test process's own environment, since D5 passes the caller's on; so a real `gh` reached by mistake (M4) would connect with whatever `GH_TOKEN` or configuration that environment holds, and `self.env` copies `os.environ` (tests:133), so the children also inherit a `NO_PROXY` or `no_proxy` that covers github.com and any `GH_CONFIG_DIR` or `XDG_CONFIG_HOME` | LOW | C-46: applied: an in-process run replaces `os.environ` for its duration with the environment that a subprocess run gets, `self.env` with the changes below, and restores it after; that environment sets `HTTPS_PROXY` and `HTTP_PROXY` to the closed port; every run removes `NO_PROXY`, `no_proxy`, `GH_TOKEN` and `GITHUB_TOKEN`, setting a fake token only where a test asserts one (the AND on `GH_TOKEN` in "The request bounds"), and fixes `GH_CONFIG_DIR` and `XDG_CONFIG_HOME` as absolute paths or unset, `HOME` being the test's own absolute `home` already (tests:133-134). The writer's reading of how the ruling meets C-44's test: that test sets the three configuration variables on purpose, each case its own run, and a refused case starts no child while an accepted case has the fake `gh` first on `PATH`, so it is the one exception and cannot reach a real `gh` | `design.md` D11 (the network and environment sub-bullets) |
| RC's L2 (D3 leaves the parsing of steps 1 and 2 unstated, and two README steps mislead): D3 names `remote_repository_identity()` for step 3 but no parser for the host; the pattern (`project:766-769`) accepts `github.com/acme/widget` and `github.com/acme/widget.git` as `acme/widget`, which Git reads as a relative local path (`git ls-remote github.com/acme/widget` exits 0 against a local bare repository there), so an implementation that took `github.com` for the host of a URL with no scheme and no `:` would send a GitHub request about a local directory; `git@GitHub.com:acme/widget.git` and `https://GitHub.com/...` are `not-github`, since the host must be exact, so the README's "nothing, as only `github.com` is queried" misleads; `git://github.com/...` and `git+ssh://git@github.com/...` are `malformed-remote`, and the README's step for it ("a URL naming an `owner/repository` on `github.com`, with no user but `git` and no port") is one that these URLs already meet; and `ssh://git@github.com:acme/widget.git` passes the pattern though Git reads `acme` as a port (corrected in round C14, C-49: Git reads no port there, taking the host `github.com:acme`) | LOW | C-47: applied in the design and the README as the ruling words it. D3 says how the host is read (after the scheme and any user information of a URL with `://`; between any `user@` and the `:` that begins the path of an scp-like URL), that the host and the scheme compare as written, never without case, and that a URL with no `://` and no `:` before its first `/` is a local path to Git with no host, so `not-github` and never sent; it names `GitHub.com` hosts as `not-github` and `HTTPS://github.com/...` and `git://github.com/...` as `malformed-remote`. The README's `not-github` step now says to write `https://github.com/acme/widget.git` for `GitHub.com` or a URL with no scheme, and its `malformed-remote` step names an https, ssh or scp-like URL, not `git://`. The writer ran the pattern as `project` has it at `961c405` and saw `acme/widget` for `github.com/acme/widget`, `github.com/acme/widget.git` and `github.com:acme/widget`, and no identity for `git@GitHub.com:acme/widget.git`, `https://GitHub.com/acme/widget`, `HTTPS://github.com/acme/widget`, `git://github.com/acme/widget.git` and `git+ssh://git@github.com/acme/widget.git`; and that the three forms the README names, `https://github.com/acme/widget.git`, `ssh://git@github.com/acme/widget.git` and `git@github.com:acme/widget.git`, each give `acme/widget`. `ssh://git@github.com:acme/widget.git`, which RC rated harmless, stands: the ruling takes no action on it (round C14's C-49 then reads it as Git does, `not-github`, and records it as a residual in D3) | `design.md` D3, Context (the identity bullet); Impact (README bullet) |
| RC's L3 (under Git's `transfer.credentialsInUrl=die`, a credential-bearing merge-target remote reads `remote-target-unread`): Git 2.43 exits 128 on both reads of a remote whose URL holds a password ("fatal: URL '...' uses plaintext credentials"), so the rows are `unknown`, `remote.completeness` is `incomplete`, and the README's step for `credential-bearing-remote` is never shown; a credential-bearing remote that the merge target does not use leaves both reads alone; the case fails closed and leaks nothing, standard error being discarded (C-31); under `warn`, Git's standard error carries the user part with the password redacted, which confirms why C-31 discards it | LOW | C-47: applied in D2 as the ruling words it: with `transfer.credentialsInUrl=die` a password-bearing merge-target remote reads `remote-target-unread`, never `credential-bearing-remote`, and nothing leaks. The writer repeated RC's runs on Git 2.43.0: under `die` the first read exited 128 with nothing on standard output and the second read exited 128; under `warn` both exited 0 with a redacted warning on standard error; under `die` both exited 0 for a clean merge-target remote beside the credential-bearing one. Not applied: RC's fix also asked for a README sentence that names `remote-target-unread` under that setting; the ruling words L3 for D2 alone, and the brief limits the README edit to L2's steps, so the README's `credential-bearing-remote` step stands as it was. No spec text: the spec's "fails for any other cause" (`:387-389`) already requires the outcome | `design.md` D2, Context |
| RC's L4, the design part (D10's "writes only into the `remote` slots" leaves out `probes`): D2's reads add to the envelope's `probes`, as D10's own last clause says; the spec part, that [R]'s "exit status" leaves out a signal that ends a `--remote` run, is in the held row below | LOW | C-47: applied: D10 says that the phase writes only into the `remote` slots and into the envelope's `probes`, which D2's remote-target reads raise by the same number in `estimated` and in `performed` in an uncut remote phase and by nothing else, and keeps its last clause | `design.md` D10 |
| RC's L5 (Open Question 1 should name this change's own follow-on as the change where the enum disagreement bites): Open Question 1 recommends that the sub-records make L-4's disagreement moot and settles it "by a change that adds a value to an existing enum"; the follow-on recommended under Out of Scope, a `closed` state (C-16), is that change, since it adds a value to `remote.state`, a closed enum in schema version 1, which is additive under APO/ov:655-658 and needs a new schema version under CAS/pc:1129-1131 | LOW | C-47: applied in this file with the item's eight lines kept: Open Question 1 now says that the first change the disagreement reaches is this change's own `closed` follow-on (Out of Scope), which adds a value to `remote.state`; the recommendation is as it was: the overview keeps `schema_version: 1`, and the disagreement is settled where it bites | Open Questions (1) |
| RC's M1 (a deadline that expires in the remote phase: [B]'s carried sentence asks for a scan error that [R] forbids): [B] keeps "On deadline expiry no further child SHALL start ... and one `deadline-exceeded` scan error SHALL count the candidates not started" (spec:61-66), [B]'s added paragraph exempts the records of the remote children and of the lookup but not that scan error (spec:141-157), and [R]'s Isolation paragraph requires a `--remote` run and the run without it to agree on every scan error, `completeness` and exit status (spec:531-543); so a `--remote` run whose collection finishes and whose deadline then expires in the remote phase (Risks, and the AND at spec:634) reads literally as one `deadline-exceeded` scan error counting 0 candidates, `incomplete` and exit 1, where the run without `--remote` can exit 0; feature 005's FR-012 states the sentence with no condition (F005:1713-1724), change 2's design never says whether a scan error with a count of 0 is written, and no scenario checks the scan errors, `completeness` or exit status at an expiry | MEDIUM | C-48: HELD for lane openRepoProject-4, as one file with amendment A1's alignment, since this item touches "Expiry cancels queued and in-flight requests", which Q16 B also reaches. No spec text and no design text here: D7 and D10 already say that nothing remote is a scan error, and RC rates the item MEDIUM, not HIGH, because [R] and D10 state the intended outcome. Applied in round C14 on lane openRepoProject-4's YES of 2026-10-21 (`c0062f9`; that section's rows) | none (held); round C14's rows |
| RC's M2 (a configured remote whose fetch refspec does not map the merge ref): Git prints `%(upstream:remotename)` and `%(upstream:remoteref)` only when it can name the upstream as a remote-tracking ref, which needs a fetch refspec that maps `branch.<target>.merge`; for a remote configured with a URL whose `remote.<name>.fetch` is unset or does not cover the merge ref, D2's first read prints empty fields and the rows are `no-remote-target`, a cause that the spec's list (spec:378-381) and the Context's tool fact do not name, and the README's step for it, `git branch --set-upstream-to=origin/main main`, fails (RC's cases A to G on Git 2.43.0; today the case fails closed, no request is sent and no answer is wrong); RC also notes a trap in D11's fixtures: a second remote created with `git config remote.<n>.url` alone makes every fixture row read `no-remote-target`, while `git remote add` writes a default refspec | MEDIUM | C-48: HELD as above. RC's two ways are (a) a clause in the spec's `no-remote-target` list, with the tool fact, the README step and D11's fixtures corrected, or (b) reading the two keys with `git config --get`, which changes [B]'s count; lane openRepoProject-4 and the lead choose. RC's fixture note belongs to this item and waits with it: D11's Fixtures bullet, the Context's tool fact and the README's `no-remote-target` step are not changed here. Applied in round C14, option (a), on lane openRepoProject-4's YES of 2026-10-21 (`c0062f9`; that section's rows) | none (held); round C14's rows |
| RC's M3 (`remote.limits.concurrency` and the comparison at concurrency 1): the AND of "The request bounds" (spec:628) requires the `remote` fields of the run with the `gh` concurrency set to 1 and of the run at 4, `remote.observed_at` apart, to be byte-identical, while `remote.limits` carries `concurrency` 4 (spec:518); change 2 reports its concurrency in `budget.probe_concurrency` and excludes exactly that field from its own byte-identical comparison (spec:130 and :195); an implementation that builds `remote.limits.concurrency` from the patched constant prints 1 and fails the AND, and one that hard-codes 4 passes but misstates the concurrency in force; the spec does not say which is meant | MEDIUM | C-48: HELD as above. RC offers two readings: an exception for `remote.limits.concurrency` at spec:628 and in the determinism sentence at spec:496-498, as change 2 excepts `budget.probe_concurrency`, or a statement at spec:517-518 that `limits` gives the constants and not the values in force; D8 follows either. Applied in round C14, the first reading, on lane openRepoProject-4's YES of 2026-10-21 (`c0062f9`; that section's rows) | none (held); round C14's rows |
| RC's L1 (no reason is stated for a repository whose first remote-target read finished and whose second never started): the expiry sentence gives `cancelled` to rows "whose remote-target read never started" and `remote-target-unread` to rows whose read the deadline stopped, and a repository whose first read named a usable remote and whose second read waited for a slot when the deadline passed, or found its budget not positive (spec:57-58), is neither; the AND at spec:635, with several repositories and held reads, can reach it without meaning to | LOW | C-48: HELD as above, as a wording edit of the spec (RC: "whose remote-target reads did not all start", read as `cancelled`). RC notes that it could be D7 alone if the lane reads "read" as either of the two reads; the ruling holds it with the spec edits, so D7 is not changed. Applied in round C14 in [B]'s own words, on lane openRepoProject-4's YES of 2026-10-21 (`c0062f9`; that section's rows) | none (held); round C14's rows |
| RC's L4, the spec part ([R]'s Isolation paragraph agrees a `--remote` run and the same run without it on the exit status "unless the remote phase raises an exception", but a signal during the remote phase exits 143 or 130, as "A signal while requests run" has it, and the run without `--remote` never sees that signal) | LOW | C-48: HELD as above: RC's "or a signal ends the run" for [R] is spec wording. D7 already says that [X]'s exits 130, 143 and 129 hold with no result document, and D10's exit-status clause is left as it was. Applied in round C14 with lane openRepoProject-4's clause for a failed write to standard output, on its YES of 2026-10-21 (`c0062f9`; that section's rows) | none (held); round C14's rows |
| RC's note outside its sections (not counted): with a relative `HOME` or `XDG_CONFIG_HOME`, a Git child run with `-C <dir>` reads its global configuration from inside that directory (from `/`, `HOME=h git -C <repo> config --show-origin --get user.name` printed `file:h/.gitconfig` with the planted value); in this change C-44 already stops every request under a relative `HOME`, but change 1's and change 2's collection probes run with the same environment, so a tracked `h/.gitconfig` in a scanned worktree would supply their global configuration | not counted | routed by the lead to lanes openRepoProject-2 and openRepoProject-4, with C-44 as the precedent; nothing here changes | none |

### Re-read and Codex Findings (round C14)

Round C14 (2026-10-21, on team-01j) commits C-48's spec text and applies its
follow-ons, C-49 and lane openRepoProject-4's call 4, on the lead's brief for
the round. Lane openRepoProject-4 said YES to C-48 at 13:4xZ. Its NOTED,
`lanes/log/openRepoProject-4.md:132` on the register's `origin/main`, added in
brett-wip `c7614c0bc`, reads "C-48 YES to lane 5 (held file at brett-wip
ffcee2ea1, spec.md sha256 ad5c6edd...; its five items), plus Isolation's
stdout-write exception added now (it names no exit status). D7 and task 2.3
under Q16 B wait for the A1 alignment. Q9 B does not extend to gh
children; #29's D5 and spec 005 record the GIT_TRACE* residual as tested." The
held file's revision 3 is revision 2 (sha256
`ad5c6edd07fe7ec81d3179072eb970dc02c33916d88a5ef3ff5ede583dd291fc`, the file at
brett-wip `ffcee2ea1`) with that exception in lane openRepoProject-4's words and
nothing else: between the two, `diff -u` shows one hunk, which re-wraps two
lines of the Isolation sentence and moves no line. Revision 3 is the register
copy at brett-wip `fbc171d1f`, sha256
`8ef40dcabe1974d52a059ef6a513f883aa48af692759e74dea3f772a8d3145bc`, and the
committed `specs/project-overview/spec.md` is that file byte for byte
(`c0062f9`, committed alone), so C-48's spec text is committed on lane
openRepoProject-4's YES of 2026-10-21 with that sha256. The file it replaces, at
`11a0ba2`, had sha256
`ce57ed5eca8085d1edc5687c7b25b10c5c603e777694bda13c481f6fe94be19a`;
`specs/project-command/spec.md` is unchanged; and the scenario counts stay 36
and 10, 46 in all.

C-49 is the lead's ruling on lane openRepoProject-3's confirm read of round C13
(`wave01i-c13-findings.md`, brett-wip `238d4bc5e`: no HIGH, no MEDIUM and eight
LOWs, W3-1 to W3-8; `rulings-2026-10-20.md`, "Rulings on lane
openRepoProject-3's confirm reads of 2026-10-21"), all accepted for this round
with no spec edit. The round edits `design.md` (`79d196a`: the Context and its
table, the tool fact, D2, D3, D5, D8, D10, D11 and Risks), and in its last
commit this file (Status, the citation key, Impact's README bullet, the
Decisions list, the round C13 section's introduction, its row of RC's L2 and its
five held rows, and this section) and `tasks.md` (1.1, 1.3, 1.4 and 1.5, in
place, 45 lines still). It does not edit `design.md` D7 or `tasks.md` 2.3, which
wait for amendment A1's alignment, as lane openRepoProject-4 asked, and it
aligns nothing to A1, draft PR #34. The design's citations of the spec move with
the committed file: `:387-388` to `:392-393`, `:459-460` to `:466-467`,
`:467-468` to `:474-475` and `:472` to `:479`. The rows of the round C13 section
cite the spec as it stood at `11a0ba2`, and the rows below cite the committed
file.

Lines 1252 to 1417 of this file, rounds C6 to C12, are unchanged (`cmp` against
`11a0ba2`), as are lines 334-345, 367-370 and 430-438 and `tasks.md` lines
20-23, lane openRepoProject-4's pinned ranges; and every paragraph of this file
before line 1252 keeps its line count, the four edits there (Status at 5-26, the
citation key at 45, Impact's README bullet at 377-395 and the Decisions list at
645-678) each replacing as many lines as they had. To hold the counts, Status
drops "delta and folded" before "reads", "on `e198548` and `67e43ae`" after
Codex's findings, the lists "(C-36, C-38, C-42, C-43)" and "(C-37, C-39, C-41)",
and "which replaces C-41's residual with" before C-44's refusal, and names
rounds C12 and C13 together; the README bullet says "`gh` logged in" for "an
authenticated `gh`", "rerun it" for "run it again" and "use" for "write"; and
the Decisions list drops "of `e198548`", "on it", "on `67e43ae`" and "on
`f34dfe2`", says "its verdicts" for "the council's verdicts" and drops "also"
twice in its last sentence.

The writer checked these on 2026-10-21. The committed spec's sha256 equals the
held file's and the register copy's. Git's release notes for 2.36.0 to 2.36.2,
2.37.0 to 2.37.3, 2.38.0, 2.38.1, 2.39.0, 2.39.1 and 2.40.0
(`Documentation/RelNotes/`, read from Git's repository) name
`transfer.credentialsInUrl` only in 2.37.0, which introduces it, and in 2.39.0,
which changes only its tests; Git's `remote.c` has no such check at `v2.36.0`
and the same check at `v2.37.0` and `v2.43.0`, run from the lookup of a remote.
Seven URLs ran on Git 2.43.0 through a `GIT_SSH_COMMAND` stand-in that logged
its arguments and connected nowhere: the four forms that D3 names;
`ssh://git@github.com:22/acme/widget.git`, which Git ran on `git@github.com`
with `-p 22`; and `ssh://git@github.com/acme/widget.git` and
`git@github.com:acme/widget.git`, each run on `git@github.com`. `gh` 2.96.0 ran
offline with D5's flags, switches and query and the three trace variables set.
The carry check of every MODIFIED block against its source passes: "Overview is
local and read-only" 1 of 1 scenarios byte for byte, +33/-0; "Overview bounds
its work and reports what it omitted" 13 of 13, +26/-0; "Overview prints a
versioned JSON envelope" 6 of 6, +12/-0, against change 2 at `961c405`; and [E]
9 of 9, +11/-0, against PR #19 at `c462d87`. Validation, run before each of the
round's commits and again at its head (a commit cannot hold its own sha; the
head is in the round's report): `/usr/bin/openspec validate
add-project-overview-remote-merge-status --strict` reports the change valid with
its two INFO lines, `/usr/bin/openspec validate --all --strict` passes 8 of 8,
and `/usr/bin/openspec status --change add-project-overview-remote-merge-status
--json` shows every artifact done. The added text holds no non-ASCII character,
bidi control, host path or literal backslash-u, and a grep of the three files
for placeholders found none.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| RC's M1, held in round C13 (a deadline that expires in the remote phase: [B]'s carried sentence asks for a scan error that [R]'s Isolation paragraph forbids) | MEDIUM | C-48: applied as held, on lane openRepoProject-4's YES. [B]'s added paragraph gains, after its sentence on the lookup of `gh` (spec:156-160), "A deadline that expires after collection has finished, during that requirement's remote phase, SHALL record no `deadline-exceeded` scan error; its effects are recorded only in the `remote` fields and in the counts above", the last five words ruled in by the lead at 13:3xZ, since a cut remote phase also shows in `probes.estimated` and `probes.performed`; change 2's carried sentence (spec:61-66) stays as it is, so [B] still only adds to change 2's text. The first AND of "Expiry cancels queued and in-flight requests" (spec:643) gains "and the scan errors, `completeness` and exit status equal those of the same run without `--remote`", the case's first check. D10 names the expiry's scan error among what the phase never records, and D11's expiry test also runs that AND's fixture without `--remote` and compares the three. D7's sentence on the same stops is not edited (the row on D7 below) | `project-overview` delta ([B] paragraph; "Expiry cancels queued and in-flight requests"); `design.md` D10, D11 |
| RC's M2, held in round C13 (a configured remote whose fetch refspec does not map the merge ref) | MEDIUM | C-48: applied as RC's option (a), Git's own reading, which adds no read and leaves [B]'s count alone: the Remote target paragraph's `no-remote-target` list gains "or a remote whose fetch refspecs do not map the merge ref, so that Git names no upstream for the merge target" (spec:383-386). The held file's writer repeated RC's cases on Git 2.43.0: with the default refspec the first read names the remote, and with no `remote.<name>.fetch`, or one that maps `refs/heads/develop` only, it prints empty fields while both keys and the URL read are intact. The follow-ons: the README's `no-remote-target` step names the fetch refspec in place of `git branch --set-upstream-to=origin/main main`, which fails where the remote-tracking ref is absent; the Context's tool fact and D2's step 1 name the cause; D11's fixture remote is made with `git remote add`, its `branch.main.*` set with `git config` (RC's trap), and one more fixture, a test and no scenario, reads `no-remote-target` for a refspec that maps `refs/heads/develop` alone (the optional fixture that the held file's notes offered); and Risks records the `git config --get` fallback it named, RC's option (b), as rejected | `project-overview` delta (Remote target); Impact (README bullet); `design.md` Context (tool fact), D2, D11, Risks |
| RC's M3, held in round C13 (`remote.limits.concurrency` and the comparison at concurrency 1) | MEDIUM | C-48: applied as RC's first reading: the determinism sentence (spec:502-506) and the second AND of "The request bounds" (spec:637) except `remote.limits.concurrency` beside `remote.observed_at`, as change 2 excepts `budget.probe_concurrency` (APO/ov:243-246, :292), and `remote.limits` still lists `concurrency` 4 (spec:525-526). D8 now says what the field reports, which the held file's notes left to it: the `gh` concurrency in force, 4 in every run and 1 only where an in-process test patches it, as change 2's `budget.probe_concurrency` reports the probe concurrency in force (APO design.md, D6, where the JSON at probe concurrency 1 and 4 differs only in timestamps and that field), so both comparisons except it. D11's comparison at concurrency 1 follows | `project-overview` delta (Results; "The request bounds"); `design.md` D8, D11 |
| RC's L1, held in round C13 (a repository whose first remote-target read finished and whose second never started) | LOW | C-48: applied in the words the lead ruled in at 13:3xZ, [B]'s own for when the second read is due (spec:145-148): the expiry sentence (spec:437-440) gives `cancelled` to a queried row "whose first remote-target read never started, or whose first read succeeded and named a remote other than `.` with a merge ref under `refs/heads/` and whose second never started", in place of the held file's first wording, "whose remote-target reads did not all start", which could take in a repository whose first read decided its outcome; a first read that failed stays `remote-target-unread`, and one that named no usable remote `no-remote-target`. The AND at spec:644 is unchanged. D11 says that the case is not tested and why, the alternative that the held file's notes offered beside a clock seam: it arises only when the deadline passes between the reaping of a first read and the dispatch of the second, which none of D11's seams can place, and the AND's outcome is the same either way. D7's sentence "every row whose remote-target read never started, is `cancelled`" is not edited (the row on D7 below) | `project-overview` delta (Requests); `design.md` D11 |
| RC's L4, the spec part, held in round C13 (a signal during the remote phase) | LOW | C-48: applied: Isolation (spec:539-542) reads "Unless the remote phase raises an exception that this requirement records as none of its reasons, or a signal ends the run or a write to standard output fails, a `--remote` run and the same run without it SHALL agree ...", the signal clause in RC's words: "A signal while requests run" exits 143 or 130 with no result document, which the run without `--remote` never shares. D10 carries both of the paragraph's new clauses, the signal and the failed write (two rows below), with their reasons | `project-overview` delta (Isolation); `design.md` D10 |
| The lead's two points on the held file's first revision (13:3xZ, on its writer's finding) | ruling | Applied within the rows of M1 and L1 above: "and in the counts above" in M1's clause, and [B]'s own words for when the second read is due in L1's; the held file's revision 2 carried both | as M1 and L1 |
| Lane openRepoProject-4's call 1 on its YES (13:4xZ): Isolation also excepts a failed write to standard output | lane openRepoProject-4's call | Applied as held revision 3, in lane openRepoProject-4's words, "or a signal ends the run or a write to standard output fails". A `--remote` document is longer than the same run's without `--remote`, by the `remote` keys and the `Remote:` line, so a reader that closes early can fail one run's write and not the other's; the clause names no exit status and so carries none of amendment A1's text, and it holds without A1. It came from the held file's writer's review of C-48 against A1 (draft PR #34 at `d46681e`), which found every held item composing with A1; nothing here is aligned to A1. D10 carries it | `project-overview` delta (Isolation); `design.md` D10 |
| Lane openRepoProject-4's YES, and the commit of the spec | lane openRepoProject-4's call | Committed alone (`c0062f9`), byte for byte as held revision 3, sha256 `8ef40dcabe1974d52a059ef6a513f883aa48af692759e74dea3f772a8d3145bc`. Against `11a0ba2`, `diff -u` shows six hunks holding the seven replacements; no scenario is added, removed, renamed or moved (36 and 10); [B] still only adds to change 2's text, and [L], [J] and the ADDED requirement's other paragraphs are unchanged. The design's four citations of the spec move with it, as the introduction above lists | `project-overview` delta; `design.md` D2, D6, D11 |
| The held file's follow-ons for `design.md` D7 and `tasks.md` 2.3 | not applied | Not made in this round, on lane openRepoProject-4's NOTED ("D7 and task 2.3 under Q16 B wait for the A1 alignment") and the lead's brief: D7's sentence on rows whose remote-target read never started (L1), a note that an expiry in the remote phase records no scan error (M1) and any citation of Isolation's signal clause (L4) wait with D7's spawning sentence and task 2.3 for amendment A1's alignment while draft PR #34 is unratified. Until then D7's "every row whose remote-target read never started, is `cancelled`" reads more loosely than the spec's expiry sentence, which governs | none |
| The held file's follow-ons in this file and `tasks.md` | follow-on | Applied: the round C13 section's introduction and its five held rows say that this round applies them; Status and the Decisions list say that C-48 is applied, its spec edit committed; the citation key runs to C-49; `tasks.md` 1.1 lists C-45 to C-49, 1.3 gains a round C14 clause and this section's title, 1.4 records the committed spec edits with `c0062f9`, and 1.5 records this round's validation | Status; citation key; Decisions; the round C13 section; `tasks.md` 1.1, 1.3, 1.4, 1.5 |
| Lane openRepoProject-3's W3-1 (D3 says that a `:` begins a port, where Git takes a port only when digits follow, and the round C13 row of RC's L2 says that Git reads `acme` as a port) | LOW | C-49: applied: D3 says that a `:` begins a port only when digits alone follow it up to the next `/`, as Git reads a port, so `ssh://git@github.com:acme/widget.git` has the host `github.com:acme`, as Git has it, and is `not-github`, never sent; that is recorded as a residual, its reason being `not-github` and not `malformed-remote`, with no README step, for a URL that Git cannot fetch either. The writer saw Git 2.43.0 run the stand-in on `git@github.com:acme` for `/widget.git`. Added beyond the ruling, from the same runs: Git drops a `:` that nothing follows (`ssh://git@github.com:/acme/widget.git`, run on `git@github.com`) and keeps digits past 65535 in the host (`:99999`), where D3 reads `github.com:` and a port, giving `not-github` and `malformed-remote`; so D3's first sentence now says that it reads the host as Git does except in the forms it names, for none of which a request is sent, and the sentence that W3-1 found false holds as written. The round C13 row of RC's L2 is corrected in place | `design.md` D3; the round C13 row of RC's L2 |
| W3-2 ("a URL with no scheme is a local path to Git" is wrong for an scp-like URL) | LOW | C-49: applied: "a URL with no scheme" becomes "a URL with no `://` and no `:` before its first `/`" in the Context's account of round C13 and in the README bullet's `not-github` step, since `git@github.com:acme/widget.git` has no scheme and is not a local path; D3's own rule and the C-47 row of the design's table already said so | `design.md` Context; Impact (README bullet) |
| W3-3 (D2's `die` rule is stated without Git's version) | LOW | C-49: applied with the version taken from Git's release notes and not from either reading: `Documentation/RelNotes/2.37.0.adoc` introduces `transfer.credentialsInURL`, which "controls what happens when a URL with embedded login credential is used on either" fetch or push, and no later note up to 2.40.0 changes it, 2.39.0 naming only tests of it; so the first version is 2.37.0, not the 2.39 that lane openRepoProject-3 gave. In Git's `remote.c` at `v2.37.0` the check runs whenever a remote is looked up, which `git remote get-url` does and a branch's upstream does through its merge configuration, so both reads meet it though neither fetches or pushes; the check and its caller are the same at `v2.43.0`, and `v2.36.0` has none. D2 says so, that on the 2.36 floor the setting is unknown, both reads succeed and D3 gives `credential-bearing-remote`, with no request either way, and that Git 2.37 to 2.39 were not run; lane openRepoProject-3 ran 2.36.6, 2.40.4 and 2.43.0 | `design.md` D2 |
| W3-4 (the in-process replacement environment does not name `PATH`) | LOW | C-49: applied: an in-process run's replacement environment is `self.env` with the `PATH` of D11's first `PATH` sub-bullet, the fake bin directory and the directory of links, in place of the developer's, and with the changes listed, so that the lookup of `gh` reads that `PATH` | `design.md` D11 |
| W3-5 (task 1.3 says that the held rows are "written nowhere else") | LOW | C-49: applied: 1.3's round C13 clause says "its text written nowhere else", since the ids are named elsewhere (the design's Context and table, Status, the Decisions list and task 1.1) while the held text was not | `tasks.md` 1.3 |
| W3-6 (Status and Decisions omit files that C-46 to C-48 edit) | LOW | C-49: applied within the line counts: Status names `tasks.md` and Open Question 1 for rounds C12 and C13, and the Decisions list says "C-45 to C-49 also in `tasks.md`" and "C-47 in Open Question 1" | Status; Decisions |
| W3-7 (the packet's canonical form against D3's local-path rule) | LOW | C-49: applied: D3 says that the packet's `github.com/owner/repository` (DI:1039-1042) names the identity derived from a remote, not a form of URL that is accepted, since as a URL that string is a local path; the outcome the packet gives a non-GitHub remote, unavailable with no request, is the same, so "Corrections to the Packet" stays none | `design.md` D3 |
| W3-8 (step 1's reading of a user that holds a `:` is not Git's) | LOW | C-49: applied: D3 says that step 1's reading is deliberately conservative and not Git's: for `u:pw@github.com:acme/widget` the writer saw Git 2.43.0 run the stand-in on the host `u` for the path `pw@github.com:acme/widget`, while step 1 refuses that URL as `credential-bearing-remote`; no request is sent either way | `design.md` D3 |
| Lane openRepoProject-4's call 4 on its YES (13:4xZ): record `GIT_TRACE*` reaching `gh` as a residual in D5 | lane openRepoProject-4's call | Applied in D5: the caller's `GIT_TRACE` and other `GIT_TRACE*` names reach a `gh` child unread, with every other variable, since [E]'s Git scrub does not apply and feature 005's Q9 B, which reaches that scrub for Git children, does not extend to `gh` children. `gh` 2.96.0, run offline by the writer on 2026-10-21 with D5's flags, switches and query, from `/`, with a fake token, its proxy at a closed local port, empty configuration, state, cache and data directories, `GIT_TRACE`, `GIT_TRACE2` and `GIT_TRACE2_EVENT` naming files and a fake `git` first on `PATH`, exited 1 on the refused connection with nothing on standard output, started no `git`, created no trace file and wrote no file, as the held file's writer had seen with a shorter query; the path of a 200 answer is not verified. If Brett Heap wants it closed, it is one clause in D5 at ratification, beside `GH_DEBUG` and `DEBUG`. No spec text: the Requests paragraph already passes every other variable on unchanged | `design.md` D5, Context and its table |

### Re-read and Codex Findings (round C15)

Round C15 (2026-10-21, on team-01k) applies C-50 and C-51 on the lead's brief
for the round (`rulings-2026-10-20.md`: C-50 under the bullet "W16 on #29's
round C14", and C-51 under "Rulings on reader RF's final composition read").
C-50 is the lead's ruling on lane openRepoProject-3's confirm read of round C14,
`11a0ba2..3965dfb` (W16, `confirm-c14-findings.md`, brett-wip `8a08f9a5d`: no
HIGH, one MEDIUM, three LOWs and no undeclared departure, W16-1 to W16-4), all
accepted for `design.md` and this section, with no spec edit. W16 also found
C-49's eight fixes applied, seven as written and W3-3 with the ruled change to
2.37.0, W3-1's two new shapes reproduced on Git 2.36.6, 2.40.4 and 2.43.0, the
held file's follow-ons made where its notes said, D5 agreeing with Q9 B at
`423a532`, lane openRepoProject-4's pinned ranges `cmp`-identical, and
validation at 8 of 8 with 36 and 10 scenarios. C-51 is the lead's ruling on the
M1 of reader RF, a read-only reader of lane openRepoProject-5 that re-ran the
composition of #27, #26 and this change at their final heads (`RF-findings.md`,
in the lane's scratch): each draft's re-base check diffs the archived block
against the re-based block, which cannot see a change to the re-basing draft's
own ratified words, so each re-base step gains a second diff, from the draft's
own committed block, and a return to Brett Heap for any change it shows. RF's
other findings are for #27 and #26 (B-54 and A-37), and it found nothing else
for this change. Codex's review of `3965dfb` found no major issues (the last
row).

The round edits `design.md` (`770e935`: the Context and its table, D3, D5 and
the Migration Plan), and in its last commit this file (Status, the citation
key, the What Changes bullet and the Capabilities entry for "Overview bounds its
work and reports what it omitted", and this section) and `tasks.md` (1.1, 1.3
and 1.5, in place, 45 lines still). No spec file changed: `git diff 3965dfb --
'*/specs/*'` is empty, `specs/project-overview/spec.md` is still the file lane
openRepoProject-4 agreed, sha256
`8ef40dcabe1974d52a059ef6a513f883aa48af692759e74dea3f772a8d3145bc`, with its 36
scenarios, `specs/project-command/spec.md` is unchanged with its 10, and the
count stays 46. C-51's edits of `tasks.md` 2.3 and 2.4 are not made: both tasks
lie in lane openRepoProject-4's pinned `tasks.md` lines 20-23, which the brief
keeps byte-identical, and the brief stops an edit that cannot keep a pin; the
Migration Plan states the second diff and governs until those tasks name it
(the row of RF's M1).

Lines 1252 to 1417 of this file, rounds C6 to C12, are unchanged (`cmp` against
`3965dfb`), as are lines 334-345, 367-370 and 430-438 and `tasks.md` lines
20-23, lane openRepoProject-4's pinned ranges; lines 1418 to 1612, rounds C13
and C14, are unchanged too, and this section follows them; and every paragraph
of this file before line 1252 keeps its line count, the four edits there
(Status at 5-26, the citation key at 45, the What Changes bullet at 160-171 and
the Capabilities entry at 257-270) each replacing as many lines as they had. To
hold the counts, Status drops "on `1c32667`, `05a424a` and `f34dfe2`" after
Codex's findings, and "applied" and "of 2026-10-21" from C-44's clause, and its
"and" moves from round C14 to round C15; the citation key says C-51 for C-49;
and the What Changes bullet and the Capabilities entry only add their clause.

The writer checked these on 2026-10-21, in a scratch directory.
`remote_repository_identity()`, taken from `project` at `961c405`, gave
`22/widget` for `ssh://git@github.com:22/widget` and for
`ssh://github.com:22/widget`, `99999/widget` for
`ssh://git@github.com:99999/widget`, `acme/widget` for
`ssh://git@github.com/acme/widget.git`, and no identity for
`ssh://git@github.com:22/acme/widget.git`,
`ssh://git@github.com:99999/acme/widget.git`,
`ssh://git@github.com:+22/acme/widget.git` and
`ssh://git@[github.com]/acme/widget.git`. Git 2.43.0 ran `ls-remote` on the
same eight URLs through a `GIT_SSH_COMMAND` stand-in that logged its arguments
and connected nowhere: with `-p 22` on `git@github.com` for the two `:22` URLs
with a user and on `github.com` for the one without; on `git@github.com:99999`,
with no port, for the two `:99999` URLs; with `-p +22` on `git@github.com` for
the signed port; and on `git@github.com`, with no port, for the bracketed host
and for `ssh://git@github.com/acme/widget.git`; each for the URL's own path.
Codex's receipt on #29 at 2026-10-21T14:48:10Z, read from the lead's record of
the pull request, says "Didn't find any major issues" for `3965dfbdb8`. The
carry check of every MODIFIED block against its source passes, as in round C14:
"Overview is local and read-only" 1 of 1 scenarios byte for byte, +33/-0;
"Overview bounds its work and reports what it omitted" 13 of 13, +26/-0;
"Overview prints a versioned JSON envelope" 6 of 6, +12/-0, against change 2 at
`961c405`; and [E] 9 of 9, +11/-0, against PR #19 at `c462d87`. Validation, run
before each of the round's commits and again at its head (a commit cannot hold
its own sha; the head is in the round's report): `/usr/bin/openspec validate
add-project-overview-remote-merge-status --strict` reports the change valid with
its two INFO lines, `/usr/bin/openspec validate --all --strict` passes 8 of 8,
and `/usr/bin/openspec status --change add-project-overview-remote-merge-status
--json` shows every artifact done. The added text holds no non-ASCII character,
bidi control, host path or literal backslash-u, and a grep of the three files
for placeholders found none.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Lane openRepoProject-3's W16-1 (D3's step 3 leaves the explicit-port refusal to `remote_repository_identity()`, which gives an identity for a port before a one-segment path, `22/widget` for `ssh://git@github.com:22/widget` and `99999/widget` for `ssh://git@github.com:99999/widget`, so that D3 taken as written would ask about the wrong repository; the spec lists an explicit port as its own cause of `malformed-remote`, spec:389-390, and round C14's "neither is sent" held only for the three-segment URLs it named) | MEDIUM | C-50: applied as worded, in D3: step 3 keeps its sentence and gains one clause, that an explicit port is refused at this step itself, before that function runs and whatever identity it would give, as `specs/project-overview/spec.md:389-390` lists an explicit port among this reason's causes beside the identity rule, with its reason: before a one-segment path the function gives an identity, so a step 3 that left the port to it would ask GitHub about the wrong repository. A paragraph after round C14's four forms records what the writer saw on Git 2.43.0 through the stand-in: Git ran `ssh://git@github.com:22/widget` on `git@github.com` with `-p 22`, and `ssh://git@github.com:99999/widget` on `git@github.com:99999` with no port, each for `/widget`, while the function gave `22/widget` and `99999/widget`; step 3 refuses both by their port, so neither is sent. Round C14's "neither is sent", for the three-segment `:99999` URL, now holds by the port refusal too. No spec text: the spec already governs, as lane openRepoProject-3 notes | `design.md` D3 (step 3, and the paragraph after round C14's forms), Context and its table |
| W16-2 (D3's "except in the forms that the next paragraph names" reads as a complete list, though more forms read a host otherwise than Git: a signed port, `ssh://git@github.com:+22/acme/widget.git`, which Git runs on `git@github.com` with `-p +22`, and a bracketed host, `ssh://git@[github.com]/acme/widget.git`, which Git runs on `git@github.com`; both fail closed) | LOW | C-50: applied: the sentence reads "except in forms such as those that the next two paragraphs name, which are examples and not a complete list (C-50), for none of which a request is sent", and the new paragraph names both forms with what the writer saw on Git 2.43.0: Git ran the signed port on `git@github.com` with `-p +22` and the bracketed host on `git@github.com`, while D3 reads the hosts `github.com:+22`, `+22` not being digits alone, and `[github.com]`, so both are `not-github` at step 2 and never sent. The paragraph also records lane openRepoProject-3's property check, as its finding file gives it: 3,619 generated URLs through D3 as worded, with the port refused at step 3, and, for each of the 30 that D3 would send, Git 2.43.0 through such a stand-in ran it on the host `github.com`, with no port, for the same `owner/repository`. The blank-led port that W16-2 also names (`: 22`) is not added, since the ruling names the two forms above | `design.md` D3 |
| W16-3 (round C14 grew the round C13 section's introduction from 4 lines to 6, so that the section's later lines moved by 2, and round C14's introduction says that the introduction was edited, not that the rows moved) | LOW | C-50: applied here, as the ruling words it. Round C14's edit of the round C13 section's introduction, lines 1441-1444 at `11a0ba2` and 1441-1446 at `3965dfb`, grew it from 4 lines to 6, so that the section's later lines, 1445-1503 at `11a0ba2`, are 1447-1505 at `3965dfb` and here: the row of RC's L2 moved from 1494 to 1496, and the five held rows from 1498-1502 to 1500-1504, where lane openRepoProject-5's notes for the held file, the rulings and lane openRepoProject-3's findings on round C13 cite them. That range is not pinned, no citation inside this change points into it, and its lines are not moved back. The writer checked the shift with a line diff of `11a0ba2` against `3965dfb`, whose only unequal ranges before round C14's section are Status, the citation key, the README bullet, the Decisions list, that introduction, the L2 row and the five held rows | this section |
| W16-4 (D5 and the round C14 row of lane openRepoProject-4's call 4 name feature 005's Q9 B without locating it) | LOW | C-50: applied in D5, as the ruling words it: "feature 005's Q9 B (PR #19 at `423a532`, C-50)". The writer read `423a532`, "Pin trace2 and scrub the trace names on every Git child (Q9 B)": its text is about Git children and names no `gh` child, as D5 says. The round C14 row stays as that round's record, the ruling naming D5 alone | `design.md` D5 |
| Reader RF's M1 (every draft's re-base check is "archived block against re-based block, additions only", which cannot see a change to the re-basing draft's own ratified words, since after the earlier change archives they are all additions; RF changed two of #26's words in its composed blocks, and that check, `validate` and the archive all passed; for this change, task 2.4, and task 2.3's re-read onto A1, which the A1 map checks the same way) | MEDIUM | C-51: applied in `design.md`, with its `tasks.md` part not made. The Migration Plan gains a paragraph after its four steps: each re-read or re-base of a block in steps 2 and 4 (tasks 2.3 and 2.4) is checked by two diffs; the first, `diff -u` of the archived block against this change's re-based block, additions only, is kept; the second, `diff -u` of this change's block as committed at its ratified head against the re-based block, shows only the archived block's own text carried in, for [E] change 1's archived text in place of PR #19's at `c462d87`, with `add-project-clean-branch-retirement`'s additions if that change archived first, and for the three `project-overview` blocks change 2's archived text in place of its text at `961c405`; and any change it shows to this change's own ratified words returns the block to Brett Heap before the Speckit handoff (step 2) or before the archive (step 4), a sentence that task 2.3 re-aligns or that lane openRepoProject-4 asks for included. Added beyond the ruling: the ADDED requirement, which has no archived block, returns to Brett Heap in the same way for any change that a `diff -u` from its committed text shows. Not made: the in-place edits of tasks 2.3 and 2.4, which lie in lane openRepoProject-4's pinned `tasks.md` lines 20-23; the brief keeps those lines byte-identical and stops an edit that cannot keep a pin, so the two tasks still name the first diff alone, and the Migration Plan says that it governs until they name both; the text the writer drafted for them is in the lane's scratch, not in this change. C-51's note that this change ratifies its PR #19 block on `c462d87`, as #26 does, needs no edit: task 1.6 and Dependencies and Sequencing already say so | `design.md` Migration Plan, Context and its table |
| Round C14's follow-up, named in C-50's timing: RC's M1 clause in What Changes and Capabilities, only if it fits within their line counts | follow-up | Applied within the counts. The What Changes bullet on "Overview bounds its work and reports what it omitted" adds "an expiry in the remote phase records no `deadline-exceeded` scan error (C-48)" after "never as a row or scan error", in 12 lines still; its Capabilities entry adds "(nor is an expiry in the remote phase, C-48)" at the same place, in 14 lines still, a shorter form, since the longer one takes a fifteenth line. The spec's sentence (spec:156-159) governs both | What Changes; Capabilities |
| The round's record in this file and `tasks.md` | follow-on | Applied: Status names round C15 within its 22 lines, the citation key runs to C-51, and `tasks.md` 1.1 lists C-45 to C-51, 1.3 gains a round C15 clause and this section's title, and 1.5 records this round's validation, each in place, 45 lines still. The Decisions list is not edited: the brief names Status and the citation key, and the list's 34 lines leave no room for C-50 and C-51 without shortening the descriptions of earlier rulings | Status; citation key; `tasks.md` 1.1, 1.3, 1.5 |
| Codex's review of `3965dfb` (its receipt on #29, 2026-10-21T14:48:10Z) | no finding | "Didn't find any major issues", for `3965dfbdb8`; nothing to apply. The same record shows every check on `3965dfb` passed, SonarCloud's included, as W16 also found | none |

Addendum (2026-10-21, after round C15). Lane openRepoProject-4 said YES to
C-51's edits of `tasks.md` 2.3 and 2.4 as the C15 writer drafted them, with one
word corrected ("such as a re-aligned or added sentence included"), in its
message of 2026-10-21T15:44:09Z, recorded in the lead's NOTED line in
`lanes/log/openRepoProject-5.md`. The two tasks now name both diffs, and their
lines stay at 22 and 23. The Migration Plan's interim sentence, which governed
until they did, now says that they do, and Status names `tasks.md` for C-51.
Lane openRepoProject-4's other pinned lines are unchanged. This addendum
supersedes the three statements above that those edits are not made
(`:1647-1651`, `:1653-1656` and the C-51 row at `:1703`), which record the state
at `86324ff` and stay as they are, and the cmp of `tasks.md` lines 20-23, which
now holds for lines 20-21.

### Re-read and Codex Findings (round C16)

Round C16 (2026-10-21, on team-01l) applies C-52 on the lead's brief for the
round (`rulings-2026-10-20.md`: C-52 under the bullet "W22 on #29's round C15").
C-52 is the lead's ruling on lane openRepoProject-3's confirm read of round C15,
`3965dfb..2eeaec4` (W22, `confirm-c15-findings.md`, brett-wip `11861d276`: no
HIGH, no MEDIUM, two LOWs and no undeclared departure, W22-1 and W22-2, with the
observation W22-3). It accepts W22-1 and W22-2 as W22 words them and takes W22-3
too, for `design.md`, this file and `tasks.md`, with no spec edit. W22 found
C-50 applied (`ssh://git@github.com:22/widget` refuses at the explicit-port
step, with Git's ssh argv identical on 2.36.6, 2.40.4 and 2.43.0; W16-2 to W16-4
applied with change, faithful to C-50; the 3,619-URL check re-run with no
mismatch) and C-51 applied (a synthetic tamper shows 0 removed lines in the
first diff and 2 in the second, and tasks 2.3 and 2.4 as committed are the held
text plus lane openRepoProject-4's "as"), the pins `cmp`-identical, the spec's
sha256 unchanged, and validation at 8 of 8 with 36 and 10 scenarios. It did not
verify lane openRepoProject-4's YES, which was not then on the register and
which the lead has since recorded in a NOTED line, nor D3's port parsing against
Git 2.56.0's `connect.c`, which is not on the bench. C-52 says that the rest of
W22's observations need no edit, and names two: the Decisions list's "C-49",
which the round C15 section declares (its row at `:1705`), and "such as ...
included" in task 2.3, which is lane openRepoProject-4's own word. Codex's
review of `2eeaec4` found no major issues (the last row).

The round edits `design.md` (`7bbc7e0`: D3's step 3, the paragraph's ten lines
and the file's 1512 kept) and, in its last commit, this file (Status, the
citation key, the round C15 section's addendum and this section) and `tasks.md`
(1.1, 1.3 and 1.5, in place, 45 lines still; 1.3 for W22-1's clause alone, as
the brief names it). No spec file changed: `git diff 2eeaec4 -- '*/specs/*'` is
empty, `specs/project-overview/spec.md` is still the file lane openRepoProject-4
agreed, sha256
`8ef40dcabe1974d52a059ef6a513f883aa48af692759e74dea3f772a8d3145bc`, with its 36
scenarios, `specs/project-command/spec.md` is unchanged with its 10, and the
count stays 46.

Lines 1252 to 1417 of this file, rounds C6 to C12, are unchanged (`cmp` against
`2eeaec4`), as are lines 334-345, 367-370 and 430-438 and `tasks.md` lines
20-23, lane openRepoProject-4's pinned ranges, which hold at `2eeaec4`, where
2.3 and 2.4 already name both diffs. No range of this file moved: lines 1 to
1707 keep their numbers, so that the three statements the addendum supersedes
stay at `:1647-1651`, `:1653-1656` and `:1703`; the addendum grows from 7 lines
(1708-1714) to 12 (1708-1719), and this section follows it. Every paragraph of
this file before line 1252 keeps its line count, the two edits there (Status at
5-26 and the citation key at 45) each replacing as many lines as they had. To
hold the counts, Status drops "applied" from two clauses (rounds C5 and C6, and
C-35 to C-43), says "2026-10-20 agreement" for "agreement of 2026-10-20", and
names rounds C15 and C16 in one clause, with the ids W16, RF's M1 and W22; the
citation key says C-52 for C-51.

The writer checked these on 2026-10-21, in a scratch directory outside this
tree. The carry check of every MODIFIED block against its source passes, as in
round C15, the spec file being byte for byte the one it checked: "Overview is
local and read-only" 1 of 1 scenarios byte for byte, +33/-0; "Overview bounds
its work and reports what it omitted" 13 of 13, +26/-0; "Overview prints a
versioned JSON envelope" 6 of 6, +12/-0, against change 2 at `961c405`; and [E]
9 of 9, +11/-0, against PR #19 at `c462d87`. Validation, run before each of the
round's commits and again at its head (a commit cannot hold its own sha; the
head is in the round's report): `/usr/bin/openspec validate
add-project-overview-remote-merge-status --strict` reports the change valid with
its two INFO lines, `/usr/bin/openspec validate --all --strict` passes 8 of 8,
and `/usr/bin/openspec status --change add-project-overview-remote-merge-status
--json` shows every artifact done. The added text holds no non-ASCII character,
bidi control, host path or literal backslash-u, and a grep of the three files
for placeholders found none.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Lane openRepoProject-3's W22-1 (four "not made" statements are false at the head: `tasks.md:13`, task 1.3, checked, says that C-51's edits of 2.3 and 2.4 are not made, beside 2.3 and 2.4 (`:22-23`), which now hold them, and the round C15 section says the same in three places that `2eeaec4` did not touch, `proposal.md:1647-1651`, `:1653-1656` (the cmp of `tasks.md` 20-23, true now for 20-21 only) and the C-51 row at `:1703`; the addendum does not say that it supersedes them) | LOW | C-52: applied as W22 words it, in two places. In `tasks.md` 1.3 the clause "and C-51's edits of 2.3 and 2.4 are not made, those lines being lane openRepoProject-4's pinned lines 20-23 of this file" becomes "and C-51's edits of 2.3 and 2.4 are made on lane openRepoProject-4's YES (round C15's addendum), 2.3's follow-on for amendment A1 still waiting", the rest of the line kept. The addendum gains its last sentence, that it supersedes the three statements above that those edits are not made and the cmp of `tasks.md` 20-23, which now holds for 20-21. The three statements are left as they are: they record the state at `86324ff`. Not edited: 1.3's round C14 clause "`design.md` D7 and 2.3 waiting for amendment A1's alignment", which W22 notes beside the committed 2.3 but gives no fix for and C-52 does not take up; it records that round, and the new words say that 2.3's follow-on for A1 still waits | `tasks.md` 1.3; the round C15 section's addendum |
| W22-2 (D3 step 3's first sentence, `design.md:416-418`, lists "an explicit port" among the cases where `remote_repository_identity()` "yields no identity", while the sentences after it say that before a one-segment path the function gives one, `22/widget`; the row at `:1699` declares that step 3 "keeps its sentence and gains one clause", so this is wording) | LOW | C-52: applied as W22 words it: the first sentence ends at "a user other than `git`", and the next begins "An explicit port is also refused here, before that function runs and whatever identity it would give", the rest of its words kept. One word beyond W22's: "or" for the comma before "a user other than `git`", since removing "or an explicit port" leaves two cases and not three. The paragraph keeps its ten lines, the new breaks falling in its second to fourth lines, and `design.md` its 1512. The row at `:1699` stays as round C15's record | `design.md` D3 |
| W22-3 (observation: the addendum says that lane openRepoProject-4 "said YES" with no time or log line, where the round C14 section cites lane openRepoProject-4's NOTED for C-48's YES; lane openRepoProject-4's register log has no NOTED for this YES through 16:04:29Z) | observation | C-52: taken: the addendum cites the YES by its message time, 2026-10-21T15:44:09Z, and by the lead's NOTED line in `lanes/log/openRepoProject-5.md`, which records it beside lane openRepoProject-4's YES of 16:13:14Z on #27's task 3.2 | the round C15 section's addendum |
| Codex's review of `2eeaec4` (15:55:35Z) | no finding | "Didn't find any major issues", as Codex's receipt reads, for `2eeaec489c` (round C17, W28-1, corrects the quotation), with CI's six test jobs and SonarCloud passing; nothing to apply | none |

### Re-read and Codex Findings (round C17)

Round C17 (2026-10-22, on team-01l) applies C-53 and C-54 on the lead's brief
for the round (`rulings-2026-10-20.md`: C-53 under the bullet "W28 on #29's
round C16", and C-54 in the lead's wave of 2026-10-22, 12:0xZ). C-53 is the
lead's ruling on lane openRepoProject-3's confirm read of round C16,
`2eeaec4..6b5bf8f` (W28, `confirm-c16-findings.md`: no HIGH, no MEDIUM, two LOWs
and no undeclared departure, W28-1 and W28-2), accepted for this round, with no
spec edit. W28 found C-52 applied (W22-1 and W22-2 as worded, with one declared
word beyond W22's, and W22-3), lane openRepoProject-4's pinned ranges
`cmp`-identical to `2eeaec4`, the spec's sha256 unchanged, and validation at 8
of 8 with 36 and 10 scenarios. C-54 adds a currency check: every place in the
proposal, design and tasks that states the current head of PR #19
(`origin/change/amend-clean-all-safe-push-pins`, now `f0bf538`) or of main (now
`15504f1`) is brought to it, and history, text that names a sha as the state at
an earlier round, is left as it is. This change ratifies its PR #19 blocks on
`c462d87`, so no block is re-based in this round. Codex's review of `6b5bf8f`
(2026-10-21T16:40:00Z) found no major issues (the last row).

The round edits `design.md` (`120b98c`: one sha in the Citations paragraph, its
1512 lines kept) and, in its last commit, this file (Status, the Citations
paragraph with the citation key, Impact's CI bullet, the first bullet of
Dependencies and Sequencing, the round C16 section's last row and this section)
and `tasks.md` (1.1, 1.3 and 1.5, in place, 45 lines still; 1.3 for W28-2's
clause alone, as the brief names it, so that 1.3 records round C16 and not yet
this round). No spec file changed: `git diff 6b5bf8f -- '*/specs/*'` is empty,
`specs/project-overview/spec.md` is still the file lane openRepoProject-4
agreed, sha256
`8ef40dcabe1974d52a059ef6a513f883aa48af692759e74dea3f772a8d3145bc`, with its 36
scenarios, `specs/project-command/spec.md` is unchanged with its 10, and the
count stays 46.

Lines 1252 to 1417 of this file, rounds C6 to C12, are unchanged (`cmp` against
`6b5bf8f`), as are lines 334-345, 367-370 and 430-438 and `tasks.md` lines
20-23, lane openRepoProject-4's pinned ranges. No range of this file moved:
lines 1 to 1790 keep their numbers, the round C16 section's last row being
edited in place, and this section follows it. Every paragraph of this file
before line 1252 keeps its line count, the four edits there (Status at 5-26, the
Citations paragraph at 28-48 with the citation key, Impact's CI bullet at
396-406 and the first bullet of Dependencies and Sequencing at 419-429) each
replacing as many lines as they had. To hold the counts, Status says "rounds C15
to C17" for "rounds C15 and C16", and the Citations paragraph is re-wrapped from
its line 33 on, its citation key reading "C-15 to C-54 (2026-10-20 to
2026-10-22".

The writer checked these on 2026-10-22, in a scratch directory outside this
tree. The heads, read with `git ls-remote origin` before each of the round's
commits, were `f0bf538` for PR #19's branch and `15504f1` for main, as the brief
names them, with no move. At main, `git diff 961c405 15504f1` is empty for
`project`, `tests/`, `openspec/changes/add-project-overview`,
`openspec/changes/add-project-clean-all-safe` and `openspec/specs`; for
`openspec/` as a whole it adds the 12 files of two changes,
`refuse-non-directory-parent-early` (#21) and `support-later-python-versions`
(#28); it modifies the five packet files under `ideation/brainstorm/` (PR #16,
`e45155a`), while `da33d92`, `961c405` and `e9d6711` are equal for `ideation/`;
`.github/workflows/tests.yml` is the same at `e9d6711` and `15504f1`, with `test
(3.10)` and `test (3.12)` on `ubuntu-latest`; and `openspec/specs/` holds no
`project-overview`, change 2 being unarchived. PR #19's branch is 24 commits
after `c462d87`, and Q9 B's scrub of Git children in its `design.md` is the same
nine lines at `f0bf538` (358-366) as at `423a532` (331-339). The carry check of
every MODIFIED block against its source passes, as in round C16, the spec file
being byte for byte the one it checked: "Overview is local and read-only" 1 of 1
scenarios byte for byte, +33/-0; "Overview bounds its work and reports what it
omitted" 13 of 13, +26/-0; "Overview prints a versioned JSON envelope" 6 of 6,
+12/-0, against change 2 at `961c405`; and [E] 9 of 9, +11/-0, against PR #19 at
`c462d87`. Validation, run on the tree of the design commit, before the last
commit and again at its head (a commit cannot hold its own sha; the head is in
the round's report): `/usr/bin/openspec validate
add-project-overview-remote-merge-status --strict` reports the change valid with
its two INFO lines, `/usr/bin/openspec validate --all --strict` passes 8 of 8,
and `/usr/bin/openspec status --change add-project-overview-remote-merge-status
--json` shows every artifact done. The added text holds no non-ASCII character,
bidi control, host path or literal backslash-u, and a grep of the three files
for placeholders found none.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Lane openRepoProject-3's W28-1 (the round C16 row of Codex's review, `proposal.md:1791`, puts quotation marks round "Found no major issues", words that are neither Codex's, whose receipt reads "Didn't find any major issues. Chef's kiss.", nor the lead's, whose record in `rulings-2026-10-20.md` has no quotation marks) | LOW | C-53: applied as W28 words it, in the first of its two forms: the row quotes Codex, "Didn't find any major issues", as the round C15 row at `:1706` does, names the commit that Codex's receipt reviewed, `2eeaec489c`, and says that round C17 corrects the quotation. The round C16 introduction's paraphrase, "found no major issues", which W28 finds fair, is left as it is | the round C16 section (its last row) |
| W28-2 (task 1.3 has W22-1's clause but no round C16 clause and no "Re-read and Codex Findings (round C16)" in its verified-by list, which ends at round C15, while 1.1 lists C-52 and 1.5 names C16; the round C16 section declares it) | LOW | C-53: applied as W28 words it: `tasks.md` 1.3 gains, after its round C15 clause, "in round C16, lane openRepoProject-3's confirm read of round C15 (W22: two LOWs and an observation, C-52) is applied in `design.md` (D3's step 3 ...), in `tasks.md` (the round C15 clause above ...) and in `proposal.md` (the round C15 addendum ...), with no spec edit, the sha256 unchanged", and its verified-by list gains "Re-read and Codex Findings (round C16)". The task is still one line, and `tasks.md` 45 lines. 1.3 does not yet record this round: the brief names 1.3 for W28-2's clause alone, as round C16's named it for W22-1's | `tasks.md` 1.3 |
| C-54, the lead's currency check: every place in the proposal, design and tasks that states the current head of PR #19 (now `f0bf538`) or of main (now `15504f1`) is brought to it, and history is left as it is | ruling | C-54: applied in four places, with every other place that names a sha of main or of PR #19 read and left. Edited: (1) the Citations paragraph, `:28-48`, whose "main still holds unchanged at `e9d6711`" for `openspec/`, `ideation/`, `project` and `tests/` is false at `15504f1` for two of the four, `openspec/` having gained two changes and `ideation/` five revised packet files, and which now says that main `15504f1` holds `project`, `tests/` and `openspec/` unchanged from `961c405`, two added changes aside, where PR #16 (`e45155a`) revised `ideation/`, with "(L-15)", the ruling that sets the base, after "main `961c405`"; (2) `design.md:113-114`, "which main `e9d6711` holds unchanged for them" (APO, CAS, PRS and `project:N`), now `15504f1`, which the diffs above bear out; (3) Impact's CI bullet, `:405-406`, "`.github/workflows/tests.yml` at main `e9d6711`", now `15504f1`, the file being the same at both; (4) the first bullet of Dependencies and Sequencing, `:423-424`, "which main still holds at `e9d6711` with change 2 unarchived (2026-10-18)", now `15504f1` and 2026-10-22, change 2's directory being unchanged and `openspec/specs/` holding no `project-overview`. Read and left: `:28-30`, the packet at `da33d92`, equal to main `961c405` for `ideation/`, which stays true; L-15's entry in the Decisions list (`:654`), the ruling of 2026-10-18 as worded when main was `e9d6711`; the round C13 row of RC's M4 (`:1493`, "main `e9d6711`") and that round's runs at `961c405` (`:1475`); `design.md:231-234`, the pull requests #31 and #17 squashed as `63dd4ad` and `f401e06`, live checks of 2026-10-19; the register's shas in the round sections, which name where a line was read; every `c462d87`, the base on which this change ratifies its PR #19 blocks (the citation key, Dependencies and Sequencing, `design.md`'s Context and Migration Plan, tasks 1.4, 1.6 and 2.4, and the round sections), which the brief keeps and which lane openRepoProject-4's pins at `:430-438` hold byte for byte; and every `423a532` (`design.md:107` and `:582`, and the round C15 section at `:1626` and `:1702`), a citation of feature 005's Q9 B at the sha where it was read (C-50, W16-4), whose scrub of Git children reads the same on PR #19's branch at `f0bf538`. `tasks.md` names no sha of main's or of PR #19's head: 3.3 reads `origin/main` without one. Not checked: the word "draft" for PR #19, which is no head claim, and for which no GitHub read was made. PR #19 is 24 commits past `c462d87`, and its block of [E] runs to 252 lines there (`:108-359`), from 166 (`:90-255` at `c462d87`), the counts that round C18 corrected from "253 lines, from 167" (W57-1); this change's block stays on `c462d87`, its ratification base (1.6), and a re-base waits for task 2.4 and its second diff (C-51) | Citations paragraph, Impact, Dependencies and Sequencing; `design.md` Citations paragraph |
| Codex's review of `6b5bf8f` (2026-10-21T16:40:00Z) | no finding | "Didn't find any major issues", as Codex's receipt reads, for `6b5bf8fe51`; the lead's late read (16:42Z) found the pull request MERGEABLE with its six test jobs passing, and SonarCloud's quality gate passed at 16:41:18Z; nothing to apply | none |

### Re-read and Codex Findings (round C18)

Round C18 (2026-10-22, on team-01l) applies C-56, C-57 and C-58 on the lead's
brief for the round (`rulings-2026-10-20.md`: C-56 under the bullet "C17 on #29
at 2ab3743", C-57 under "Reader RI reported", C-58 under "RH reported"), and
C-61, which the lead added to the round by message. C-58 is the lead's ruling on
reader RH's M4 and on the alignment reader AL1's conflict C1, both on #29's
ADDED requirement and a relative `HOME` or `XDG_CONFIG_HOME`; C-57 is its ruling
on reader RI's RI-6, which sharpens RE-15; C-56 ends task 1.3's lag of one round;
C-61 is its ruling on lane openRepoProject-3's W57-1, the one LOW of W57's read
of round C17, `6b5bf8f..2ab3743` (0 HIGH, 0 MEDIUM, 1 LOW). Reader RH's L4 and
AL1's note on task 2.3 touch lane openRepoProject-4's pinned lines 20-23 of
`tasks.md`, so their wording is drafted and held for lane openRepoProject-4's
YES, and written nowhere in this change. C-59, the lead's ruling that AL1's held
blocks go to lane openRepoProject-4 now, as one file with C1, and land as a
round on each draft after #34 merges, is not applied here. Codex's review of
`2ab3743` found no major issues (the last row).

The round edits `specs/project-overview/spec.md` (`51e854b`: the ADDED
requirement alone, in its Requests paragraph, the parenthesis of its Results
paragraph and the last AND of "No gh, or a gh without authentication"),
`design.md` (`78d6c84` and `b0d7c2a`: D5 gains the paragraph of C-58, and the
Context's realization bullet gains C-57's note; 1512 lines become 1547) and, in
its last commit, this file (Status, the citation key, the round C17 section's
C-54 row and this section) and `tasks.md` (1.1, 1.3, 1.4 and 1.5, in place, 45
lines still). The spec file is now sha256
`dee66d4f6608b3c53a2d9ae0464af023f4c87662719247543ca74cdb6ce3c46f`, where lane
openRepoProject-4 agreed `8ef40dcabe1974d52a059ef6a513f883aa48af692759e74dea3f772a8d3145bc`;
it holds 36 scenarios, none added, removed, renamed or moved, and
`specs/project-command/spec.md` is unchanged (`git diff 2ab3743` on it is empty,
sha256 `208c06c36656194d2560614c44251cf404786cce90c54c9d8f6a0d6a5f2b601d`) with
its 10, so that the count stays 46. The lead sends the spec edit to lane
openRepoProject-4 for its view (C-58); it is committed, as the brief orders, and
not a held file.

Lines 1252 to 1417 of this file, rounds C6 to C12, are unchanged (`cmp` against
`2ab3743`), as are lines 334-345, 367-370 and 430-438 and `tasks.md` lines
20-23, lane openRepoProject-4's pinned ranges. No range of this file moved:
lines 1 to 1873 keep their numbers, the round C17 section's C-54 row being
edited in place, and this section follows them. Every paragraph of this file
before line 1252 keeps its line count, the two edits there (Status at 5-26 and
the citation key at 45) each replacing as many lines as they had. To hold the
counts, Status says "rounds C15 to C18" for "rounds C15 to C17", names the
round's ids, and drops the words after "(C-24 to C-34" in its clause on rounds
C5 and C6 and the "per-" of "per-directory"; the citation key reads "C-15 to
C-61", a span that includes C-55 and C-60, which this change cites nowhere, and
C-59, which it cites as not applied.

The writer checked these on 2026-10-22, in a scratch directory outside this
tree. The heads, read with `git ls-remote origin` before the round's last
commit, were `f0bf538` for PR #19's branch, `e4a30fc` for amendment A1's and
`15504f1` for main, with no move. The cites of C-58 were read with `git show`:
`PR19/cmd` at `f0bf538`, :116-129, is the "Configuration paths" paragraph (a
test of `HOME` and `XDG_CONFIG_HOME`, and of `GIT_CONFIG_GLOBAL` and
`GIT_CONFIG_SYSTEM`, before any Git child, `git --version` included, and where
one is relative the subcommand starts no Git child and inspects no repository,
`relative-config-path`); and `:868-876` of change 2's
`specs/project-overview/spec.md` at `e4a30fc`, in the commit "A1: ratified by
Brett Heap ('ratify 34'); task 1.7", is the paragraph "Once its arguments are
parsed", which refuses the overview with `relative-config-path` and status 2.
Feature 004's `ChildHandle.start` reads `env=git_env(kind)` at `project:1049`
at `e69f6ef`, with `GIT_KINDS` at :956-969 and `git_env` at :972-982 there. The
carry check of every MODIFIED block against its source passes, as in round C17
(the spec file's MODIFIED blocks being untouched): "Overview is local and
read-only" 1 of 1 scenarios byte for byte, +33/-0; "Overview bounds its work and
reports what it omitted" 13 of 13, +26/-0; "Overview prints a versioned JSON
envelope" 6 of 6, +12/-0, against change 2 at `961c405`; and [E] 9 of 9, +11/-0,
against PR #19 at `c462d87`. Validation, run before each of the round's commits
and again at its head (a commit cannot hold its own sha; the head is in the
round's report): `/usr/bin/openspec validate
add-project-overview-remote-merge-status --strict` reports the change valid with
its two INFO lines, `/usr/bin/openspec validate --all --strict` passes 8 of 8,
and `/usr/bin/openspec status --change add-project-overview-remote-merge-status
--json` shows every artifact done. The added text holds no non-ASCII character,
bidi control, host path or literal backslash-u, and a grep of the three files
for placeholders found none.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Reader RH's M4 and the alignment reader AL1's conflict C1 (the ADDED requirement says that a relative `HOME` or `XDG_CONFIG_HOME` gives no `gh` child and both rows `unavailable` with `gh-unavailable`: the Requests paragraph at `:417-422`, the Results paragraph at `:484-489` and the last AND of "No gh, or a gh without authentication" at `:619`, unchanged at `2ab3743`; but change 1's evidence model on PR #19's text (`PR19/cmd` at `f0bf538`, :116-129, LQ-15) and change 2's requirement 11 as amendment A1 words it (`e4a30fc`, `:868-876`) refuse such a run before any child starts, so that it has no row to be `gh-unavailable`, and a test written to the AND fails on either text; the queued A1 re-alignment does not cover this ADDED requirement) | MEDIUM | C-58: applied, in a form that holds on any base. The Requests paragraph and the Results paragraph's parenthesis keep the rule whole for `GH_CONFIG_DIR` and state it for `XDG_CONFIG_HOME` and `HOME` only in a run that neither `Repository inspection requires Git 2.36 and shares one evidence model` nor `Overview exits by completeness and severity` refuses before any child starts, the spec naming the two requirements by header and never A1's code, which this change's own base does not define; the two texts, with their cites, are named in `design.md` D5 and not in the spec. The AND keeps its relative `GH_CONFIG_DIR` case as it was, with the absolute and empty cases, and for the relative `HOME` and relative `XDG_CONFIG_HOME` cases says that no `gh` child starts on every base and that both rows are `unavailable` with `gh-unavailable` where neither requirement refuses the run first. The scenario count stays 36 in either form, since the AND edits an existing scenario; the form was chosen on what the scenario tests: moving the two cases out of the AND would leave the property that no `gh` child starts under a relative `HOME` or `XDG_CONFIG_HOME` (C-44's planted-configuration point) with no scenario at all on a base that has neither text, where the conditional AND keeps it tested on every base, a test of it being able to pass on each. AL1's proposed edit (the two cases exit 2 with `relative-config-path`) is not taken: it names A1's code, which this change's own base, change 2 at `961c405` and PR #19's block at `c462d87`, does not define, and it would contradict this change on a base without A1; the ruling prefers the conditional form. Not edited, and read with D5's new paragraph: D4, the rest of D5, D10, D11 and Risks in `design.md`, Impact's README bullet and the Decisions entry for C-44 here, which restate C-44's refusal for all three variables without the condition, and the 21 other places of AL1's list, which join the A1 alignment rounds (C-59) | spec, ADDED requirement (Requests, Results, "No gh, or a gh without authentication"); `design.md` D5 |
| Reader RI's RI-6, which sharpens RE-15 (feature 004's `ChildHandle.start(argv, cwd, kind)` always spawns with `env=git_env(kind)`, `project:1049` at `e69f6ef`, which removes the Git names, sets `TRACE2_OFF` and takes only a `GIT_KINDS` key; a `gh` row there would break the spec's "every other variable passed on unchanged" and D5's tested residual; the start path that takes its own environment is not built) | LOW | C-57: applied as RI words its fix, a design note and no spec edit. This change records no item called RE-15 (a search of the three files found none); the finding's text, "adds a phase and a child kind to that loop", stands in the Context's realization bullet, so the note is added there, with the cites of the brief (the spec's `:405-417`, that bullet and D5's `:579-584`, at `2ab3743`): feature 004 cannot yet give a `gh` child the environment this change specifies, and the start path is not built | `design.md` Context (realization bullet) |
| C-56, the lead's ruling: task 1.3's lag of one round ends in round C18 (each brief named 1.3 for the previous round's clause only, so that 1.3 always lagged by one round; lane openRepoProject-3's W28-2 found it, and round C17 repeated it) | ruling | C-56: applied: `tasks.md` 1.3 gains, after its round C16 clause, a round C17 clause (W28 and the currency check, C-53 and C-54) and a round C18 clause (C-56, C-57, C-58 and C-61, the spec edit and its sha256, and what is held, described and not reproduced), and its verified-by list gains "Re-read and Codex Findings (round C17)" and "Re-read and Codex Findings (round C18)"; 1.1 lists C-45 to C-61 and 1.5 names round C18. 1.4 gains one clause, for C-58's committed spec edit, which is beyond the brief's list: 1.4 records each round's committed spec edit, and the clause says that this one is committed on the lead's ruling for lane openRepoProject-4's view. The task is still one line, and `tasks.md` 45 lines. Each later round records itself in 1.3 | `tasks.md` 1.1, 1.3, 1.4, 1.5 |
| Reader RH's L4 (task 2.4, `tasks.md:23`, says "re-read" for the case where PR #19 lands first and #26 has not archived, though its own check, `diff -u` of the archived block against this change's block "showing additions only", and the second `diff -u`, can pass only after a re-base, PR #19's block at `f0bf538` differing from the text this change carries by about 1,371 words and five scenarios; #26's task 2.2 says "re-based if that text moved past `c462d87`") | LOW | C-58 carries it, held: the wording of 2.4 is drafted, with the old and the new line, and not committed, since the line is inside lane openRepoProject-4's pinned lines 20-23; `cmp` of those lines against `2ab3743` holds. It is held for lane openRepoProject-4's YES, which the lead will ask for; `design.md`'s Migration Plan, step 4, takes the same clause in the round that commits it | none (held for lane openRepoProject-4) |
| AL1's note that task 2.3's condition ("if feature 005's Q16 amends, or records a departure from, change 2's design D1 or clarifications N1 before change 2 archives") is now met, since amendment A1 is ratified and its design D1 holds the paragraph "Spawning: each child is started with SIGINT, SIGTERM and SIGHUP unblocked, then entered in the in-flight registry" (`e4a30fc`, `:116-120`) | note | C-58 carries it, held, in the same file as the wording of 2.4, with an offered line for 2.3 that states the fact in place of the condition; the note asks no wording change by itself, and `tasks.md:22` is inside lane openRepoProject-4's pinned lines | none (held for lane openRepoProject-4) |
| C-59, the lead's ruling: AL1's held blocks (requirements 3, 5, 8 and 9, four blocks built by three-way merge, validating at 8 of 8 with the counts unchanged) go to lane openRepoProject-4 now, as one held file with C1, and land as a round on each draft only after #34 merges; the 21 other places join those rounds | ruling | not applied here: this round takes C1's place only, in the form above, and leaves the four blocks, which would change this change's MODIFIED blocks, and the 21 places to those rounds. AL1's contingency stands: A1 allows #34 to land without its four LQ items, and then C1 does not arise | none |
| Lane openRepoProject-3's W57 on round C17 (`6b5bf8f..2ab3743`) | 0 HIGH, 0 MEDIUM, 1 LOW | W57 found one LOW, W57-1 (the next row); nothing else to apply, as the lead's message reports | none |
| W57-1 (the C-54 row of the round C17 table says that PR #19's block of [E] "runs to 253 lines there, from 167"; by the file it is 252 lines (`:108-359`) at `f0bf538` and 166 (`:90-255`) at `c462d87`, the range that `:436` cites) | LOW | C-61: applied: counted again here with `git show` of `specs/project-command/spec.md` at both shas, the block being the last in the file at each, 359 lines in all at `f0bf538` with the block's header at 108, and 255 at `c462d87` with it at 90, so 252 and 166. The round C17 section's C-54 row now reads "252 lines there (`:108-359`), from 166 (`:90-255` at `c462d87`)" and says that round C18 corrected them (W57-1), in place; every other earlier round row keeps its words as history. Round C18 corrects the counts; the row at `:1872` is the only place that gave them | the round C17 section (its C-54 row) |
| Codex's review of `2ab3743` (2026-10-22T12:48:43Z) | no finding | "Didn't find any major issues", as the lead's late read of 12:55:48Z records it, which also found CI and SonarCloud passing at `2ab3743`; nothing to apply | none |

### Re-read and Codex Findings (round C19)

Round C19 (2026-10-22, on team-01m) applies C-62 and C-63 on the lead's brief
for the round (`rulings-2026-10-20.md`: C-62 under the bullets "Lane 4 on C18's
held file" and "C-62, the lead's ruling, for C19", and C-63 under "A-54, B-75
and C-63"). Lane openRepoProject-4 answered round C18's held file
(`held-task-2.4.md`, sha256
`65e41f03d58531fdbb61c46434f0ffe51330d7536e6c17c653cb590c70c2a7bf`), as the lead
received it at 13:17:48Z and lane openRepoProject-4 noted it at 13:17:56Z
(`lanes/log/openRepoProject-4.md:195`, register commit `d72029d50`): YES to its
item 1, task 2.4 (reader RH's L4), and NO to its item 2, the offered line for
task 2.3, since amendment A1 is ratified but has not landed and the offered line
drops "or clarifications N1"; C-59's alignment round records the fact once #34
lands. C-62 commits task 2.4 as held, with the Migration Plan's step 4 taking
the same clause, and leaves task 2.3 as it is. C-63 is the lead's ruling on lane
openRepoProject-3's W53 departure ledger (`departure-ledger.md`, received at
13:17:04Z, read from lane openRepoProject-3's attachments on the register's
`origin/main`), which has 3 departure rows for this change, 29-01 to 29-03, each
lane-only, and one inherited row, 29-R. W53 finds 29-01 and 29-02 declared in
this proposal but not cited against the packet line each changes, and C-63 has
the proposal cite those lines, so that the packet revision can take them as
written; the rows go to Brett Heap with the packet revision. Codex's review of
`e1a9f84` found no major issues (the last row).

The round edits `design.md` (`d38b282`: the Migration Plan's step 4 takes task
2.4's clause, six lines becoming seven, so that the file is 1548 lines, from
1547) and, in its last commit, this file (Status, the citation key, two
Decisions bullets edited and three re-wrapped, the heading of the Departures
list and this section) and `tasks.md` (1.1, 1.3, 1.5 and 2.4, in place, 45 lines
still). No spec file changed: `git diff e1a9f84 -- '*/specs/*'` is empty,
`specs/project-overview/spec.md` is still sha256
`dee66d4f6608b3c53a2d9ae0464af023f4c87662719247543ca74cdb6ce3c46f` with its 36
scenarios, and `specs/project-command/spec.md` is unchanged (sha256
`208c06c36656194d2560614c44251cf404786cce90c54c9d8f6a0d6a5f2b601d`) with its 10,
so that the count stays 46. Spec 005 re-checks #25 once, at the head that
commits task 2.4, which is this round's last commit (the head is in the round's
report, a commit not being able to hold its own sha).

Lines 1252 to 1417 of this file, rounds C6 to C12, are unchanged (`cmp` against
`e1a9f84`), as are lines 334-345, 367-370 and 430-438 and `tasks.md` lines
20-22, lane openRepoProject-4's pinned ranges. Line 23 of `tasks.md`, task 2.4,
is the one change inside those pins, agreed by lane openRepoProject-4's YES, and
is the held file's new line byte for byte: the sha256 of lines 20-23 is now
`2e177de7a91d644759bb5e12177696c749be9d9e90a763ce9899e238e7c0e2c0`, from
`f81b5eb94bdb1faf87395cee093d408278f0426586c705b1b18498a6a4082053`, that of
lines 20-22 alone is `21be1248e5c178f7` at its first 16 digits before and after,
and that of line 23 alone is now
`6289ab629aa6d849f7ef61a9514dea22f65b898145100909041ae933f8615986`. Every
paragraph of this file before line 1252 keeps its line count and its place (55
blocks, each with the same first line and length, and the same blank lines):
Status (5-26, its clause on rounds C15 to C19 re-wrapped from line 18 on) and
the citation key (45) in place, the heading of the Departures list in place, and
the Decisions list's block of 82 lines (906-987), in which the two edited
bullets take more lines than they had, "`unavailable` beyond DI:1041-1042" two
and "gh's own traffic off" one, from three bullets with a line to spare,
"Matching", "A remote phase after collection" and "Fields only in a `--remote`
run", re-wrapped at 80 columns with their words unchanged (checked word for
word). The bullets between move: "A remote phase after collection" from 933 to
932, "At most two Git children per repository for the remote target" from 937 to
935, "`unavailable` beyond DI:1041-1042" from 944 to 942, "No effect on
`completeness` or the exit" from 963 to 962, "No early stop" from 974 to 973 and
"gh's own traffic off" from 978 to 977; no line outside 924-987 moves, so every
other cite of this file's lines holds.

W53's 29-R, that this proposal's own "Departures" list (`:989-1016`) departs
from lane 5's ruling C-5 (its example wording and its listed `closed` state) and
from no packet line, is why the cites go where they do. The list's two entries,
the merged-row wording and no `closed` state, are departures from C-5, a lane
ruling, and stay as they are; its heading now says so, "Departures from C-5,
each naming what it departs from:". W53's 29-01 and 29-02 are departures from
the packet, which this proposal declared in its Decisions list, as
"`unavailable` beyond DI:1041-1042" and "gh's own traffic off", the first citing
DI:1041-1042 only and the second DI:1038-1039 only, with no cite of
DI:1055-1056, which 29-01 changes, or of DI:307-308, which 29-02's residual
stands against. The cites are added to those two entries, in place, so that the
list is not mixed with them and no departure's meaning changes. The lines were
read with `git show` of the packet's `project-maintenance-project-discovery.md`
at `da33d92`, the pin that every DI cite here uses: DI:1041-1042 "A
credential-bearing, malformed, or non-GitHub remote produces `remote status
unavailable` without a request"; DI:1055-1056 "A rate limit, 401, 403, timeout,
truncation, or other API failure produces an explicit unknown result";
DI:1038-1039 "it must be opt-in and read-only"; DI:307-308 "it never fetches,
pulls, resets, bootstraps, runs validators, writes files, or contacts the
network". The numbers are `da33d92`'s, as W53 gives them; main's packet is
revision 1 (`e45155a`), and W53's open item 5, main's line for each row, is not
taken here.

The writer checked these on 2026-10-22, in a scratch directory outside this
tree. The heads, read with `git ls-remote origin` before the round's commits,
were `662be89` for PR #19's branch (also `refs/pull/19/head`), `8f6fa31` for
feature 004 (branch `004-project-clean-all-safe`, pull request #33), `e4a30fc`
for amendment A1's, `15504f1` for main and `e1a9f84` for this change's, with no
move. The currency check read every place in the three files that names a head
of PR #19, of feature 004 or of main, by a search of each file for `f0bf538`,
`423a532`, `c462d87`, `e69f6ef`, `15504f1`, `662be89` and `8f6fa31`. PR #19's
round (f) at `662be89` changes `design.md`, `proposal.md` and `tasks.md` of
change 1 only (`git diff --stat f0bf538 662be89`: 3 files, 228 insertions, 93
deletions) and no spec: `specs/project-command/spec.md` there is byte for byte
the file at `f0bf538`, 359 lines with the block of [E] at `:108-359`, 252 lines,
as round C18's correction counts it. No place in this change's three files
states PR #19's current head as live text. Every mention of `f0bf538` is in the
round C17 and C18 sections, which record the head as it stood, in the round C18
clause of task 1.3, or is a cite of the spec text read there (D5's `PR19/cmd` at
`f0bf538`, :116-129, `design.md:650`), which round (f) leaves equal; so nothing
moves to `662be89`, and history stays. Every `c462d87` stays as the ratification
base. Every `423a532` (`design.md:107`, `:174` and `:591`, and the round C15
section) cites feature 005's Q9 B at the sha where it was read: the nine lines
of PR #19's design on the scrub of Git children are `:331-339` at `423a532`,
`:358-366` at `f0bf538` and `:361-369` at `662be89`, byte for byte equal at the
three, so the cite is true at the new head, and stays. Feature 004 at `8f6fa31`
holds `project` byte for byte as at `e69f6ef` (`git diff e69f6ef 8f6fa31 --
project` is empty; only `tests/test_clean_revalidation.py` differs):
`ChildHandle.start` still spawns with `env=git_env(kind)` at `project:1049`,
with `GIT_KINDS` at `:956` and `git_env` at `:972`, so RI-6's note stands at the
new head, and its `e69f6ef` cite (`design.md:215` and the round C18 section)
stays as the sha it was read at. Main is still at `15504f1`, so the places that
name it stay. Places edited for currency: none.

The carry check of every MODIFIED block against its source passes, as in round
C18 (the spec file untouched): "Overview is local and read-only" 1 of 1
scenarios byte for byte, +33/-0; "Overview bounds its work and reports what it
omitted" 13 of 13, +26/-0; "Overview prints a versioned JSON envelope" 6 of 6,
+12/-0, against change 2 at `961c405`; and [E] 9 of 9, +11/-0, against PR #19 at
`c462d87`. Validation, run before each of the round's commits and again at its
head (a commit cannot hold its own sha; the head is in the round's report):
`/usr/bin/openspec validate add-project-overview-remote-merge-status --strict`
reports the change valid with its two INFO lines, `/usr/bin/openspec validate
--all --strict` passes 8 of 8, and `/usr/bin/openspec status --change
add-project-overview-remote-merge-status --json` shows every artifact done. The
added text holds no non-ASCII character, bidi control, host path or literal
backslash-u, and a grep of the three files for placeholders found none.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Reader RH's L4 (task 2.4, `tasks.md:23`, says only "re-read" for the case where PR #19 lands first and #26 has not archived, though its own first `diff -u`, of the archived block against this change's block "showing additions only", and its second can pass only after a re-base, PR #19's block having moved past the text this change carries at `c462d87`), held in round C18 for lane openRepoProject-4's YES | LOW | C-62: applied on lane openRepoProject-4's YES (13:17:48Z, noted at 13:17:56Z), as held and byte for byte: the line gains "and re-based on it if the archived block moved past PR #19's text at `c462d87`," after "re-read against the archived block", the credit "reader RH's L4" after "C-51", and "as re-based where it was," in the first `diff -u`; `design.md`'s Migration Plan step 4 takes the same clause, as "re-read against change 1's archived block and re-based on it if that block moved past PR #19's text at `c462d87`", after the block of [E] re-based on change 1's text (`d38b282`). The re-base rule is unchanged in effect: a re-base that changes the block's added text still returns it to Brett Heap before the archive (C-51). It is the one change inside lane openRepoProject-4's pinned lines 20-23. The round C18 section says that this wording is held and written nowhere in this change; this row supersedes that for task 2.4, as the round C15 addendum did for C-51's edits | `tasks.md` 2.4; `design.md` Migration Plan (step 4) |
| AL1's note that task 2.3's condition is met, and the line offered for 2.3 in the held file's item 2, inside lane openRepoProject-4's pinned `tasks.md:22` | note | C-62: lane openRepoProject-4 said NO to the offered line: amendment A1 is ratified but has not landed, and the offered line drops "or clarifications N1". Task 2.3 stays exactly as it is, `tasks.md` lines 20-22 byte for byte as at `e1a9f84` (`cmp`), and C-59's alignment round records the fact once #34 lands | none |
| W53's 29-01 (#29, DI, lane-only: "`unavailable` beyond DI:1041-1042" says that `unavailable` also covers `no-remote-target`, `gh-unavailable` and `gh-unauthenticated`, so `remote.completeness` stays `complete`, and cites DI:1041-1042 only, while the packet makes a failed or timed-out request unknown, DI:1055-1056) | ruling | C-63: applied: the entry cites both lines at `da33d92` with what each says (the first: a credential-bearing, malformed or non-GitHub remote is `unavailable` with no request; the second: "a rate limit, 401, 403, timeout, truncation, or other API failure" gives an explicit unknown), says that this change departs from both where no answer can come for want of a target or a client, and gives `unavailable` also to the three reasons, with the three causes of `gh-unavailable` (no `gh`, a failed lookup, or one past its 5 s limit) and the effect that `remote.completeness` stays `complete`; its gloss of exit 4 and its rejected alternative are kept. No departure's meaning changes: the rule and the three reasons are those the entry had, those of C-25 and C-26 and those of the spec | Decisions ("`unavailable` beyond DI:1041-1042") |
| W53's 29-02 (#29, DI, lane-only: "gh's own traffic off" says that each `gh` child runs with six variables removed and five set, and cites DI:1038-1039 only, while the Git scrub does not apply and what a `gh` child reads, writes or sends beyond its argv and those switches is the GitHub client's own, a residual, against the packet's "read-only" and "never ... writes files") | ruling | C-63: applied: the entry's last sentence cites DI:1038-1039 with the packet's words ("opt-in and read-only"), says that the Git scrub does not apply, names what a `gh` child reads, writes or sends beyond its argv and these switches as the client's own, a residual (What This Repository Does Not Own), and cites DI:307-308 ("never ... writes files") beside DI:1038-1039 as the lines that residual stands against. The six removed and five set variables are unchanged; the words "beyond its documented switches" became "beyond its argv and these switches", those of the third bullet of What This Repository Does Not Own. No departure's meaning changes | Decisions ("gh's own traffic off") |
| W53's 29-R and its note that #29's own "Departures" list rests on C-5 and not on the packet (the list's two entries depart from C-5's example wording and its listed `closed` state, lane 4's three departures from change 2's text and L-10, and none from a packet line; the MODIFIED block of [E] carries PR #19's rows) | note | C-63: kept as W53 has it: the list's two departures, the merged-row wording and no `closed` state, stay as they are, resting on C-5 and cited to it, and the cites of 29-01 and 29-02 go into the two Decisions entries that declare the packet departures, so that the Departures list is not mixed with them. Its heading, "Departures, each naming what it departs from:", now reads "Departures from C-5, each naming what it departs from:", so that a reader takes the list as departures from a lane ruling and finds the two packet departures in Decisions. No departure's meaning changes | Departures list (heading) |
| W53's 29-03 (five readings of the packet: the credential store, the URL's user information, "recorded as unknown", the two keys against "Every field ... is always present", and the 1 MiB body) | ruling | C-63: nothing to cite: W53 marks the row DECLARED as readings, and "Readings of packet and ratified text" already cites DI:310, DI:1056-1058, DI:1053, DI:823 with DI:834-835, and DI:1048-1050; its packet line to change is optional clarifying clauses. Left as it is | none |
| The lead's currency check for round C19: PR #19 is now at `662be89` (round (f): design, proposal and tasks only, with spec text equal to `f0bf538`'s), feature 004 at `8f6fa31` | ruling | applied by reading every place, and no place edited: no place in the proposal, design or tasks states PR #19's current head as live text, so none moves to `662be89`. Read and left: every `f0bf538` (the round C17 and C18 sections, the round C18 clause of task 1.3 and D5's `PR19/cmd` at `f0bf538`, :116-129 (`design.md:650`), whose spec text is the same at `662be89`); every `c462d87`, the ratification base; every `423a532`, Q9 B's nine lines, equal at `423a532`, `f0bf538` and `662be89`; RI-6's `e69f6ef`, since `project` at `8f6fa31` is byte for byte `e69f6ef`'s; and main's `15504f1`, still main's head. The paragraph above gives each | none |
| The record: Status, the citation key, and tasks 1.1, 1.3 and 1.5, in place | ruling | C-56 and C-63's record: Status says "rounds C15 to C19" and "C-50 to C-63" and names RH's L4 and W53's cites, within its 22 lines; the citation key reads "C-15 to C-63", a span that still includes C-55 and C-60, which this change cites nowhere, and C-59, which it cites as not applied; `tasks.md` 1.1 lists C-45 to C-63, 1.3 gains a round C19 clause (C-62, C-63 and the currency check, this round recording itself as C-56 orders) and "Re-read and Codex Findings (round C19)" in its verified-by list, and 1.5 names round C19; the tasks file is 45 lines still | Status; citation key; `tasks.md` 1.1, 1.3, 1.5 |
| Codex's review of `e1a9f84` (2026-10-22T13:19:21Z) | no finding | "Didn't find any major issues", as the lead's late read of 13:25:49Z records it, which also found CI and SonarCloud passing at `e1a9f84`; nothing to apply | none |

### Re-read and Codex Findings (round C20)

Round C20 (2026-10-22, on team-01m) applies C-65 on the lead's brief for the
round (`rulings-2026-10-20.md`: the bullets "Lane 3's W61 on C18" and "C-65"),
and C-66, which the lead sent to the running round. Lane openRepoProject-3's W61
(`confirm-c18-findings.md`, received by the lead at 14:13:13Z) read round C18,
`2ab3743..e1a9f84`, and found 0 HIGH, 0 MEDIUM and 4 LOW, with nothing that
departs from a ruling, the packet or ratified text: C-56, C-57, C-58 and C-61
are applied, the spec's sha256 and the counts are as recorded, lane
openRepoProject-4's pins are cmp-identical, and 8 of 8 validate. W61 also
answered the lead's question on the passages that C18 left unedited, which D5
had declared were read with its paragraph and re-aligned with task 2.3. D4, D10,
Impact's README bullet and the Decisions index entry for C-44 are right, as read
with D5 or as history. D5's restatement of the rule, D11's test and Risks' entry
are not, and the Decisions bullet "Run-wide unavailability, C-25 and C-26" in
this file, which the lead's list had left out, reads like D4 without D5's cite
and is misleading in the same way. C-65 applies those answers, in the design and
this file only. W61's third LOW (C18-3), that the spec says "refuses" of change
1's evidence model, which only bars every Git child, is a spec edit: C-65 held
it for lane openRepoProject-4's decision, lane openRepoProject-4 said YES to the
wording at 14:16:29Z, outside its pins, and C-66 lifts the brief's "no spec
edit" for that item alone, in lane openRepoProject-4's form, each verb paired
with its own requirement and not "refuses or bars" for both.

The round edits `specs/project-overview/spec.md` (`e053ad6`, committed first:
the ADDED requirement's Requests paragraph and the parenthesis of its Results
paragraph, 660 lines becoming 661), `design.md` (`6527f73`: D5 at two places,
D11 and Risks, 1548 lines becoming 1560) and, in its last commit, this file
(Status, the citation key, the Decisions bullet "Run-wide unavailability, C-25
and C-26", the cite of `PR19/cmd` in the round C18 and C19 sections, and this
section) and `tasks.md` (1.1, 1.3, 1.4 and 1.5, in place, 45 lines still). The
spec file is now sha256
`6fda0ae8c5c60dab3a94c453af58503e11a6f19f62ddbde4d5ed7d098d26ee6c`, which
replaces `dee66d4f6608b3c53a2d9ae0464af023f4c87662719247543ca74cdb6ce3c46f`, the
sha that the round C18 and C19 sections record as it stood; it holds 36
scenarios, none added, removed, renamed or moved, and
`specs/project-command/spec.md` is unchanged (`git diff 9a3f684` on it is empty,
sha256 `208c06c36656194d2560614c44251cf404786cce90c54c9d8f6a0d6a5f2b601d`) with
its 10, so that the count stays 46.

The spec edit, as `git diff --word-diff` against `9a3f684` shows it: in the
Requests paragraph, the clause "in a run that neither `Repository inspection
requires Git 2.36 and shares one evidence model` nor `Overview exits by
completeness and severity` refuses before any child starts" now reads "in a run
that neither `Repository inspection requires Git 2.36 and shares one evidence
model` (by barring every Git child and inspecting no repository) nor `Overview
exits by completeness and severity` (by refusing the run) stops it before any
child starts", and the paragraph takes one line more, 6 becoming 7; in the
parenthesis of the Results paragraph, "not refused" now reads "not stopped",
with the line count unchanged. The two headers are as the spec already names
them, and the scenario AND on "No gh, or a gh without authentication" is not
edited, so that it keeps "no `gh` child starts" for every case. That AND still
says, for the relative `HOME` and `XDG_CONFIG_HOME` cases, "where neither
`Repository inspection requires Git 2.36 and shares one evidence model` nor
`Overview exits by completeness and severity` refuses the run before any child
starts", one verb for both. The clause is outside the places that lane
openRepoProject-4 agreed and that C-66 names, so the round leaves it as it is
and reports it to the lead, whose call it is; the fix would be one word, "stops"
for "refuses". Lines 1 to 419 of the spec are byte for byte as at `9a3f684`, the
three MODIFIED blocks (:1-342) and lines 1 to 410, which spec 005's Dependencies
list compares, among them; lines 426 to 660 of `9a3f684` are lines 427 to 661
now, but for that one word.

`design.md`: D5's "(C-44)" at the former :606 reads "(C-44; `XDG_CONFIG_HOME`
and `HOME` as the "Two texts" paragraph says, C-58)", naming the paragraph by
its opening words and not by its line. That paragraph, at :646-670, now says
that the two texts "stop a run under" a relative `HOME` or `XDG_CONFIG_HOME`
before any child starts; that change 1's evidence model, on PR #19's text, tests
the four variables before any Git child and, where one is relative, "bars every
Git child and inspects no repository (`relative-config-path`), whether the
subcommand then refuses or reports being its own requirement's rule", which
echoes `PR19/cmd` at `f0bf538`, :128-129; that change 2's exit rule, as
amendment A1 words it, "refuses the overview" with that code and status 2; and
that the spec states the rule for those two variables only in a run that neither
requirement "stops" before any child starts. Its last sentence names "D4 and the
rest of this decision" as the places that state the rule without the condition,
D11 and Risks having been corrected. D11's Refused list is split in two
(:1181-1201), the `GH_CONFIG_DIR` cases kept as they were, and Risks' bracket
(:1412-1414) gains "for `XDG_CONFIG_HOME` and `HOME`, where C-58's condition
holds". The two D5 edits are line for line, :603-619 staying 17 lines and
:646-670 staying 25, so that D5's residual :574-601 (sha256 `da48e5684e354a9d`
at its first 16 digits) and D7 :954-989 (`8a03ba68b8166c74`) keep their lines
and bytes; D11 takes 11 more lines and Risks one, and nothing before :1181
moved.

This file: the Decisions bullet "Run-wide unavailability, C-25 and C-26" reads
"(C-44; C-58 for the last two)" at its cite of C-44, re-wrapped within its 11
lines at :892-902. The cite of `PR19/cmd` is written "`PR19/cmd` at `f0bf538`,
:116-129" wherever it appeared: in `design.md` D5 (:650), in the round C18
section (its paragraph on the cites of C-58, at :1927, and its first row) and in
the round C19 section (its paragraph on the currency check, at :2067, and its
currency row), each re-wrapped within the lines it had, with the other words of
those sections left as history. The key still defines `PR19/cmd` at `c462d87`,
and `design.md:396`'s `PR19/cmd:123-125` is a cite at that sha (the pins
sentence is :123-125 at `c462d87`), so it stays. Status, within its 22 lines,
and the citation key, at :45, name round C20 and C-66.

Lines 1252 to 1417 of this file, rounds C6 to C12, are unchanged (`cmp` against
`9a3f684`), as are lines 334-345, 367-370 and 430-438, "Dependencies and
Sequencing" (181 lines, sha256 `c4d7a1797d240880` at its first 16 digits) and
"Open Questions" (39 lines, `ca53d0f392adc7e5`), each compared whole by sha256,
and `tasks.md` lines 20-23 (sha256
`2e177de7a91d644759bb5e12177696c749be9d9e90a763ce9899e238e7c0e2c0`, the one that
the round C19 section records): lane openRepoProject-4's pinned ranges. No line
of this file moved: lines 1 to 2106 keep their numbers, this section following
them, and every paragraph before line 1252 keeps its line count and its place
(55 paragraphs, each with the same first line and length), Status (5-26), the
citation key (45) and the Decisions bullet (892-902) each replacing as many
lines as they had. To hold Status's 22 lines, its clause on rounds C15 to C20
reads "C-58, C-66 also in the spec, C-63, C-65 in Decisions" and names "W61" and
not its LOWs.

The writer checked these on 2026-10-22, in a scratch directory outside this
tree. W61's report was read from lane openRepoProject-3's attachments on the
register's `origin/main` with `git show`, and its lines were found at this head
by their text. The "Configuration paths" paragraph was read from PR #19's
`specs/project-command/spec.md` with `git show`: at `f0bf538` it begins at :116
("Configuration paths: before any Git child starts") and ends at :129 ("as for
the version."), and that file is the same sha256
(`d4cb310646343df40119a5fdeca3da8f475b5d9b5427492d834c053965ed0f71`) at
`f0bf538`, `662be89` and `4f1c0e0`, so the cite holds at each. The carry check
of every MODIFIED block against its source is as in round C19, since lines 1 to
342 of the overview spec and the whole `project-command` spec are byte for byte
as at `9a3f684`: "Overview is local and read-only" 1 of 1 scenarios, +33/-0;
"Overview bounds its work and reports what it omitted" 13 of 13, +26/-0;
"Overview prints a versioned JSON envelope" 6 of 6, +12/-0, against change 2 at
`961c405`; and [E] 9 of 9, +11/-0, against PR #19 at `c462d87`. Validation, run
before each of the round's commits and again at its head (a commit cannot hold
its own sha; the head is in the round's report): `/usr/bin/openspec validate
add-project-overview-remote-merge-status --strict` reports the change valid with
its two INFO lines, `/usr/bin/openspec validate --all --strict` passes 8 of 8,
and `/usr/bin/openspec status --change add-project-overview-remote-merge-status
--json` shows every artifact done. The added text holds no non-ASCII character,
bidi control, host path or literal backslash-u, and a grep of the three files
for placeholders found none.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Lane openRepoProject-3's W61 on round C18 (`2ab3743..e1a9f84`, `confirm-c18-findings.md`, received by the lead at 14:13:13Z) | 0 HIGH, 0 MEDIUM, 4 LOW | C-65: W61 found 0 HIGH, 0 MEDIUM and 4 LOW (C18-1 to C18-4) and six observations, none of them a departure from a ruling, the packet or ratified text; C-56, C-57, C-58 and C-61 are applied, the spec's sha256 and the counts are as recorded (`dee66d4f...`, 36 and 10), lane openRepoProject-4's pins are cmp-identical, and 8 of 8 validate. Its four LOWs and its answers on the seven passages are the rows below; nothing else to apply | none |
| W61's C18-1 (D11's test of C-44's rule, the Refused list at the former `design.md:1181-1196`, gives both rows `gh-unavailable` for a relative `XDG_CONFIG_HOME` or `HOME` and says that each case gives them, though on a base with amendment A1 those runs exit 2 before any row exists: WRONG there as a test map, right on this change's own bases) | LOW | C-65: applied: D11's Refused list is split in two. The first, "Refused on every base", keeps the `GH_CONFIG_DIR` cases as they were (`GH_CONFIG_DIR=.gh-config`, a relative `GH_CONFIG_DIR` beside an absolute `XDG_CONFIG_HOME` and an absolute `HOME`, and the values ` /x`, `~/x` and `.`), with their results. The second, "Refused only where neither requirement stops the run first (C-58, C-66)", takes the `XDG_CONFIG_HOME` and `HOME` cases (`XDG_CONFIG_HOME=cfg`, `HOME=h`, either one relative beside an absolute `GH_CONFIG_DIR`, and each of the two relative beside the other two absolute): where neither `Repository inspection requires Git 2.36 and shares one evidence model` nor `Overview exits by completeness and severity` stops the run before any child starts, each gives the first list's results; where either does, the run has no lookup and no row, and the case asserts only that no `gh` child starts and that the run ends as that requirement says (status 2 with `relative-config-path` under amendment A1's requirement). The "Not refused" cases, the 70-key case and the AND's cases are as they were | `design.md` D11 (:1181-1201) |
| W61's C18-2 for D5 (the restatement of the rule at the former `design.md:604-606`, "the lookup of `gh` counts as failing when any of `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` and `HOME` is set ... (C-44)", is the first thing a reader meets, 40 lines before the condition at :646: MISLEADING; the rest of D5 is right as read with it) | LOW | C-65: applied: the sentence now ends "(C-44; `XDG_CONFIG_HOME` and `HOME` as the "Two texts" paragraph says, C-58)", pointing at the paragraph by its opening words ("Two texts that land before this change", still at :646) and not by its line. The paragraph :603-619 keeps its 17 lines by re-wrapping, and the edit lies after D5's residual :574-601, which stays `cmp`-identical to `9a3f684`. The rest of D5 is right as W61 reads it and is not edited | `design.md` D5 (:603-619) |
| W61's C18-2 for Risks (the bracket of the entry at the former `design.md:1401-1403`, "makes every keyed row `gh-unavailable` and starts no child (C-44)", states the outcome for all three variables: MISLEADING; the rest of the entry stays true) | LOW | C-65: applied: the bracket now ends "starts no child (C-44; for `XDG_CONFIG_HOME` and `HOME`, where C-58's condition holds)", the brief's clause in the same parenthesis as C-44's cite; the rest of the entry is as it was | `design.md` Risks (:1412-1414) |
| W61's C18-2 for this file (the Decisions bullet "Run-wide unavailability, C-25 and C-26", at the former `proposal.md:892-893`, "a lookup of `gh` that fails, as for a relative `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` or `HOME` (C-44)": MISLEADING in the same way as D4, with no cite of D5; a place that the lead's list omitted) | LOW | C-65: applied: "(C-44; C-58 for the last two)", the bullet re-wrapped within its 11 lines (:892-902) so that every paragraph before the round C6 section keeps its line count | Decisions ("Run-wide unavailability, C-25 and C-26") |
| W61's C18-4 (`PR19/cmd:116-128` is `f0bf538`'s text, but this file's key defines `PR19/cmd` at `c462d87`, where :116-128 is the push child's protocol pins; and the "Configuration paths" paragraph runs to :129, the clause that hands refuse-or-report to the subcommand) | LOW | C-65: applied: written "`PR19/cmd` at `f0bf538`, :116-129" in `design.md` D5 (:650), in the round C18 section (its paragraph on the cites of C-58 and its first row) and in the round C19 section (its paragraph on the currency check and its currency row). Read with `git show`: at `f0bf538` the paragraph is :116-129, and the file is byte for byte the same at `662be89` and `4f1c0e0` (sha256 `d4cb3106...`), so the cite holds at each of the three; the key keeps `c462d87`, and `design.md:396`'s `PR19/cmd:123-125` is a cite at `c462d87` and stays | `design.md` D5; the round C18 and C19 sections |
| W61's C18-3 (the spec says that change 1's evidence model "refuses" the run, in the Requests paragraph and the Results paragraph's parenthesis, and D5's first sentence says "refuse"; but [E] only bars every Git child and inspects no repository, leaving "whether the subcommand then refuses or reports" to its own requirement (`PR19/cmd` at `f0bf538`, :124-129; #19's proposal leaves the overview's code and exit status to change 2); the refusal with exit 2 is change 2's requirement 11 as A1 words it) | LOW | C-65: held, a spec edit, for lane openRepoProject-4's decision; its words were to be "refuses or bars every Git child". Lane openRepoProject-4 then said YES at 14:16:29Z, outside its pins, in the form that pairs each verb with its own requirement, and C-66 (next row) applies it | none here (see C-66) |
| C-66, the lead's ruling, sent to the running round: the spec edit in lane openRepoProject-4's form, with no scenario added and lane openRepoProject-4's cited spec spans byte for byte | ruling | C-66: applied, in `e053ad6`, committed first. Change 1's evidence model bars every Git child and inspects no repository, change 2's exit rule refuses the run, and `gh-unavailable` holds for a relative `XDG_CONFIG_HOME` or `HOME` only in a run that neither stops first: the Requests paragraph says "neither `Repository inspection requires Git 2.36 and shares one evidence model` (by barring every Git child and inspecting no repository) nor `Overview exits by completeness and severity` (by refusing the run) stops it before any child starts", the Results paragraph's parenthesis says "not stopped" for "not refused", and D5's paragraph pairs the verbs the same way (the design commit). The headers are as the spec already names them, no scenario is added or removed (36 and 10), the AND's "no `gh` child starts" holds for every case, and lines 1 to 419 of the spec are byte for byte as at `9a3f684`. New sha256 `6fda0ae8c5c60dab3a94c453af58503e11a6f19f62ddbde4d5ed7d098d26ee6c`, 661 lines, replacing `dee66d4f...`. Not edited, and reported to the lead: the AND on "No gh, or a gh without authentication" says "neither ... nor ... refuses the run before any child starts" for both requirements; it is not in C-66's list and not in the wording that lane openRepoProject-4 agreed | spec, ADDED requirement (Requests; Results); `design.md` D5 (:646-670) |
| W61's answers on the passages that C18 left unedited and found right: D4 (`design.md:524-527`, names the cause as an example and cites D5), D10 (names none of the three variables and not C-44; the lead's list read C-26's row), Impact's README bullet (the list of remedies for a code a person sees; on a base with A1 the two extra variables are inert and never harmful) and the C-44 index entry in Decisions (history), and W61's observations OBS-1 to OBS-6 | note | C-65: left as they are. The rest of D5, which W61 finds right as read with its paragraph, is left too. OBS-3 (D5's "Two texts that land before this change" states an order, though amendment A1 is not a named dependency; "that are to land before this change is re-read (tasks 2.3, 2.4)" would be exact) is harmless and not taken | none |
| The record: Status, the citation key, and tasks 1.1, 1.3, 1.4 and 1.5, in place | ruling | C-65 and C-66's record: Status says "rounds C15 to C20" and "C-50 to C-66" and names W61, within its 22 lines (the clause reading "C-58, C-66 also in the spec, C-63, C-65 in Decisions" to hold them); the citation key reads "C-15 to C-66", a span that still includes C-55 and C-60, which this change cites nowhere, and C-59, which it cites as not applied; `tasks.md` 1.1 lists C-45 to C-66, 1.3 gains a round C20 clause (this round recording itself, as C-56 orders) and "Re-read and Codex Findings (round C20)" in its verified-by list, 1.4 gains one clause for C-66's committed spec edit, which is beyond the brief's list as C18's was (1.4 records each round's committed spec edit), and 1.5 names round C20; the tasks file is 45 lines still | Status; citation key; `tasks.md` 1.1, 1.3, 1.4, 1.5 |

### Re-read and Codex Findings (round C21)

Round C21 (2026-10-22, on team-01n) applies C-67 on the lead's brief for the
round (`rulings-2026-10-20.md`: the bullets "C20 on #29 at a6080a7", whose
writer's notes were queued for C21, "Lane 4 (received 14:34:27Z): YES to
"refuses" becoming "stops"" and "C-67"). The brief also gives #29's late read at
`a6080a7` (2026-10-22T15:21:40Z): CI, all six test jobs, and SonarCloud pass.
The `@codex review` request of 14:33:52Z drew Codex's usage-limit reply at
14:34:11Z, so Codex did not review round C20, and no Codex finding is waiting
for this round. The round applies the round C20 writer's notes (a) and (b) and
records note (c).

The round edits `specs/project-overview/spec.md` (`1cd73fb`, committed first:
one word), `design.md` (`266a30f`: four cites, on four lines) and, in its last
commit, this file (Status, the citation key and this section) and `tasks.md`
(1.1, 1.3, 1.4 and 1.5, in place, 45 lines still).

The spec edit, as `git diff --word-diff` against `a6080a7` shows it, is
`[-refuses-]{+stops+}` and nothing else, in the last AND of the scenario "No gh,
or a gh without authentication" (:624), which now reads "... and where neither
`Repository inspection requires Git 2.36 and shares one evidence model` nor
`Overview exits by completeness and severity` stops the run before any child
starts, `remote.requests.performed` is 0 and both rows are `unavailable` with
reason `gh-unavailable`": one verb for both requirements, as the Requests
paragraph says "stops it before any child starts" (:421-424) since C-66. That
paragraph's parenthesis "(by refusing the run)" (:423-424) says what change 2's
exit rule does to the run, is not part of the note, and is not edited. No
scenario is added, removed, renamed or moved (36 and 10, so the count stays 46),
the spec file is 661 lines still, and lines 1 to 419 of it, lane
openRepoProject-4's cited span, are byte for byte as at `a6080a7` (`cmp`). The
spec file is now sha256
`d42139fb5e6c26952e30aa953173cfcc5efb01f01f82e1f496e34bad6d77d306`, which
replaces `6fda0ae8c5c60dab3a94c453af58503e11a6f19f62ddbde4d5ed7d098d26ee6c`, the
sha that the round C20 section records as it stood;
`specs/project-command/spec.md` is unchanged (sha256
`208c06c36656194d2560614c44251cf404786cce90c54c9d8f6a0d6a5f2b601d`) with its 10.

`design.md`: four cites of the spec's ADDED requirement read lines that the spec
no longer holds there, and each now reads the line or lines that hold the text
it names. At :918 and :1152, `specs/project-overview/spec.md:479` for "a
positive integer `number`" is now `:483` ("SHALL have a positive integer
`number`" begins that line). At :1167, `:474-475` for "A 200 body SHALL be UTF-8
JSON" is now `:478-479` ("A 200 body" ends :478, "SHALL be UTF-8 JSON" is on
:479). At :1168, `(:466-467)` for a response "that cannot be decoded or parsed
for any cause", which the brief ordered checked beside the :1167 cite, is now
`(:470-471)` ("one that cannot be decoded or" ends :470, "parsed for any cause"
is on :471). All four were exact at `c0062f9`, round C14's spec edit, where the
`number` line was :479 and the UTF-8 sentence :474-475; `51e854b` (C-58) added
three lines before them and `e053ad6` (C-66) one more, which is the note's
"stale at `9a3f684`, and C20's added line moves them by one more". Each new cite
is as wide as the one it replaces, so `design.md` stays 1560 lines and no line
is re-wrapped; it lies after D5's residual :574-601 and D7 :954-989, which stay
`cmp`-identical to `a6080a7`.

The other cites of a spec line in the three files were checked against the text
each names at this head, and none other needs a correction. In `design.md`: :350
and :1246 (`:392-393`, "fails for any other cause") and :429 (`:389-390`, an
explicit port among the causes of `malformed-remote`) are exact; :219
(`:405-417`) is qualified "at `2ab3743`" and records what was true there; :396,
:650 and :657 cite change 1's and change 2's specs at a named sha. In
`proposal.md`: the cites in the sections for rounds C5 to C20 and in the table
"Questions Resolved by the Alignment Review" (`spec.md:13-27` and the like)
record what was read at the commit each names, or at that round's head; :508, in
"Dependencies and Sequencing", is qualified "on `67e43ae`"; and the cites in
"Modified Capabilities" (`:166`, `:606` and the rest) are, as that section says,
APO/ov's and `openspec/specs/project-command/spec.md`'s at `961c405`. In
`tasks.md`, the one cite, `PR19/cmd` at `f0bf538`, :116-129, is qualified. All
of these stay. Two groups lie inside parts that lane openRepoProject-4 cites,
:508 and the rows of rounds C6 to C12; both are history by the same rule and are
not edited, so nothing is left unedited as stale and reported.

This file: Status, within its 22 lines, says "rounds C15 to C21", "C-50 to C-67"
and "C-58, C-66, C-67 also in the spec", and, to hold those 22 lines, no longer
lists "the currency check" among the sources of rounds C15 to C21 (the round C19
section still records it); the citation key, at :45, reads "C-67". No line of
this file moved: lines 1 to 2255 keep their numbers, this section following
them, and every paragraph before line 1252 keeps its line count and its place
(55 paragraphs, each with the same first line and the same line count). Lane
openRepoProject-4's pinned ranges are `cmp`-identical to `a6080a7`: lines 1252
to 1417 of this file, rounds C6 to C12, and lines 334-345, 367-370 and 430-438;
"Dependencies and Sequencing" (181 lines, sha256 `c4d7a1797d240880` at its first
16 digits) and "Open Questions" (39 lines, `ca53d0f392adc7e5`), each compared
whole by sha256; `tasks.md` lines 20-23 (sha256
`2e177de7a91d644759bb5e12177696c749be9d9e90a763ce9899e238e7c0e2c0`); D5's
residual :574-601 and D7 :954-989 of `design.md`; and lines 1 to 419 of the
spec.

The writer checked these on 2026-10-22, in a scratch directory outside this
tree, from the late read and the rulings the brief names. The cites above were
read against the spec at this head by their text, and the line history of the
`number` line was read with `git show` of the spec at each commit that touched
it (`c0062f9` :479, `51e854b` :482, `e053ad6` :483). The carry check of every
MODIFIED block against its source is as in round C19 and C20, since lines 1 to
342 of the overview spec and the whole `project-command` spec are byte for byte
as at `9a3f684`. Validation, run before each of the round's commits and again at
its head (a commit cannot hold its own sha; the head is in the round's report):
`/usr/bin/openspec validate add-project-overview-remote-merge-status --strict`
reports the change valid with its two INFO lines, `/usr/bin/openspec validate
--all --strict` passes 8 of 8, and `/usr/bin/openspec status --change
add-project-overview-remote-merge-status --json` shows every artifact done. The
added text holds no non-ASCII character, bidi control, host path or literal
backslash-u, and a grep of the three files for placeholders found none.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| #29's late read at `a6080a7` (2026-10-22T15:21:40Z), as the brief for this round gives it: CI, all six test jobs, and SonarCloud pass; the `@codex review` request of 14:33:52Z drew Codex's usage-limit reply at 14:34:11Z | no finding | Codex did not review round C20, so no Codex finding exists to apply; nothing to apply | none |
| The round C20 writer's note (a): the last AND of the scenario "No gh, or a gh without authentication" (:624) says that `Overview exits by completeness and severity` "refuses the run before any child starts", for both requirements, where C-66's Requests paragraph says "stops it before any child starts" (:421-424); one word, "stops", would match it, and lane openRepoProject-4 was asked for a YES | note | C-67 (a): applied, in `1cd73fb`, committed first: "refuses" becomes "stops", that one word and nothing else (`git diff --word-diff` against `a6080a7` shows `[-refuses-]{+stops+}` alone). The parenthesis "(by refusing the run)" in the Requests paragraph, which says what change 2's exit rule does to the run, is not edited. No scenario is added or removed (36 and 10), the spec is 661 lines still, lines 1 to 419 are byte for byte as at `a6080a7`, and `specs/project-command/spec.md` is unchanged (`208c06c3...`). New sha256 `d42139fb...`, replacing `6fda0ae8...` | spec, ADDED requirement ("No gh, or a gh without authentication", last AND) |
| Lane openRepoProject-4 (received by the lead at 14:34:27Z): YES to "refuses" becoming "stops" in the AND of the scenario "No gh, or a gh without authentication", which lies outside spec 005's cited spans | ruling | C-67 (a): applied as the previous row, one word in that AND; the AND is at :624 and the span that lane openRepoProject-4 cites is :1-419, which the edit does not reach. The sentence that it brings the AND into line with, C-66's Requests paragraph, is as lane openRepoProject-4 agreed it at 14:16:29Z | spec (as above) |
| The round C20 writer's note (b): `design.md` :918 and :1152 cite the spec's `number` line as `:479`, and :1167 cites `:474-475` for "A 200 body SHALL be UTF-8 JSON"; already stale at `9a3f684`, and round C20's added line moves them by one more | note | C-67 (b): applied, in `266a30f`: `:479` becomes `:483` at :918 and :1152, `:474-475` becomes `:478-479` at :1167, and the `(:466-467)` at :1168 for a response "that cannot be decoded or parsed for any cause", which the brief ordered checked with the :1167 cite, becomes `(:470-471)`. All four were exact at `c0062f9` (the `number` line at :479, the UTF-8 sentence at :474-475), and `51e854b` and `e053ad6` added four lines before them. Each cite keeps its width, so `design.md` stays 1560 lines and no line is re-wrapped | `design.md` D6 (:918), D11 (:1152, :1167-1168) |
| C-67 (b), every other cite of a spec line in `design.md`, `proposal.md` and `tasks.md`, checked against the text it names at this head | ruling | C-67 (b): none other needs a correction. `design.md` :350, :1246 (`:392-393`) and :429 (`:389-390`) are exact; :219 (`:405-417`) is qualified "at `2ab3743`"; :396, :650 and :657 cite change 1's and change 2's specs at a named sha. In `proposal.md`, the cites in the round C5 to C20 sections and the "Questions Resolved by the Alignment Review" table record what was true then, :508 is qualified "on `67e43ae`", and the Capabilities cites are APO/ov's and the canonical `project-command` spec's at `961c405`. In `tasks.md` the one cite is `PR19/cmd` at `f0bf538`. All stay. :508 and the rows of rounds C6 to C12 lie inside parts that lane openRepoProject-4 cites, and are history by the same rule and not edited, so nothing is reported as stale | none |
| The round C20 writer's note (c): the commit messages of `a6080a7` and `6527f73` hold small slips | note | C-67: recorded and not amended, since amending a pushed commit would need a force push, which the house rules bar; they stand as history. In `a6080a7`'s, "the round C20 section with its eleven rows": its table holds 10. In `6527f73`'s, "design.md 1548 to 1560 lines, all of it after D7 but 1 to 602 and 671 to 1180 equal to 9a3f684's": D5's two edits (:603-619 and :646-670) lie before D7 (:954), so "all of it after D7" is wrong, though the line counts and the two equal ranges are right (`cmp` shows lines 1 to 602 and 671 to 1180 equal). The lead's note names the first slip; the second is the one the writer found. The commit messages of `1cd73fb` and `266a30f` were read against the same checks and hold no slip that the writer saw | none |
| The record: Status, the citation key, and tasks 1.1, 1.3 (this round records itself, C-56), 1.4 and 1.5, in place | ruling | C-67's record: Status says "rounds C15 to C21", "C-50 to C-67" and "C-58, C-66, C-67 also in the spec", within its 22 lines, by no longer listing "the currency check" among its sources (the round C19 section still records it); the citation key reads "C-15 to C-67"; `tasks.md` 1.1 lists C-45 to C-67, 1.3 gains a round C21 clause (this round recording itself, as C-56 orders) and "Re-read and Codex Findings (round C21)" in its verified-by list, 1.4 gains one clause for the committed one-word spec edit, which is beyond the brief's list as C18's and C20's were (1.4 records each round's committed spec edit), and 1.5 names round C21; the tasks file is 45 lines still | Status; citation key; `tasks.md` 1.1, 1.3, 1.4, 1.5 |

### Re-read and Codex Findings (round C22)

Round C22 (2026-10-22, on team-01n) applies C-68 on the lead's brief for the
round (`rulings-2026-10-20.md`: the bullets "Lane 3's W66 on C19 and C20" and
"C-68"). Lane openRepoProject-3's W66 (`confirm-c19c20-findings.md`, brett-wip
`4ea08c0b3`, received by the lead at 15:34:53Z) read rounds C19 and C20,
`e1a9f84..a6080a7`, and found 0 HIGH, 0 MEDIUM and 4 LOW, with nothing that
departs from a ruling, the packet or ratified text, and six observations that
ask for no edit. Two of the four LOWs, C20-1 and C20-2, are the items that round
C21 applied (`1cd73fb` and `266a30f`); the other two, C20-3 and C20-4, are this
round's. The brief also has PR #19's current head read against every place that
cites it, and asks for a report, with no edit, of the places that carry the
three texts that Brett Heap's ruling R-263 (15:24Z) had PR #19's round (h)
carry. The lead's message to the running round moved that head from `6bf9f77` to
`b3228bb`, where round (h) is accepted, and had the three texts quoted from
`b3228bb` itself. The `@codex review` request of 15:36:19Z on `8276945` drew
Codex's usage-limit reply at 15:36:31Z, as the lead's late read of 15:52:41Z
records, so Codex did not review round C21 and no Codex finding is applied here;
that read also finds CI, all six test jobs, and SonarCloud passing on #29 at
`bbe8d53`, the first commit of this round.

The round edits `design.md` (`bbe8d53`, committed first: three lines of D5's
paragraph on the two texts) and, in its last commit, this file (Status, the
citation key and this section) and `tasks.md` (1.1, 1.3 and 1.5, in place, 45
lines still). It edits no spec: `specs/project-overview/spec.md` is still sha256
`d42139fb5e6c26952e30aa953173cfcc5efb01f01f82e1f496e34bad6d77d306` with its 36
scenarios and `specs/project-command/spec.md` still
`208c06c36656194d2560614c44251cf404786cce90c54c9d8f6a0d6a5f2b601d` with its 10,
so that the count stays 46, and `git diff 8276945` on both is empty.

The design edit is two changes in one sentence of D5's paragraph "Two texts that
land before this change" and nothing else (`git diff --word-diff` against
`8276945`): a semicolon for the comma after "(`relative-config-path`)", and "is
left to" for "being". At :653-654 the sentence read "... bars every Git child
and inspects no repository (`relative-config-path`), whether the subcommand then
refuses or reports being its own requirement's rule", where "being" had no verb
to follow (W66's C20-3). It now ends its clause at the code and goes on ";
whether the subcommand then refuses or reports is left to its own requirement's
rule": the sense of `PR19/cmd` at `f0bf538`, :128-129 ("whether the subcommand
then refuses or reports is its own requirement's rule, as for the version"),
with the lead's "left to". The brief's "refuses the run or reports" is written
without "the run": with it the paragraph takes 26 lines at 80 columns and D7
moves, and #19's own words give "refuses" no object either. The paragraph keeps
its 25 lines (:646-670): three lines re-wrap, :653 to :655, "Change 2's" now
splitting across :654 and :655, and the rest is as it was. Lines 1 to 652 and
656 to 1560 of `design.md` are byte for byte as at `8276945`, so the file stays
1560 lines, and D5's residual :574-601 (sha256 `da48e5684e354a9d` at its first
16 digits) and D7 :954-989 (`8a03ba68b8166c74`) are `cmp`-identical to it. W66
adds that the round C20 section quotes the sentence; that quotation (:2177-2178
of this file), like the message of `6527f73`, records what that commit wrote and
stands as history, since a round's record is not edited.

The currency check. The heads, read with `git ls-remote origin` at the start of
the round, were `6bf9f77` for PR #19's branch, `d764c26` for feature 004 (branch
`004-project-clean-all-safe`, pull request #33), `e4a30fc` for amendment A1's
(pull request #34), `15504f1` for main and `8276945` for this change's. After
the lead's message a second read of the same refs gave `b3228bb` for PR #19's
branch (also `refs/pull/19/head`), `b60792c` for feature 004, `e4a30fc` and
`15504f1` again, and `bbe8d53`, the round's design commit, for this change's.
Round C19 read PR #19 at `662be89` (round (f)); it has since moved to `4f1c0e0`
(round (g)), `3dcd2d8` (g2), `6bf9f77` (g3) and `b3228bb` (round (h), R-258 to
R-263, four commits: `e322f52`, `324192f`, `fc95766` and `b3228bb`), and feature
004 from `8f6fa31` to `d764c26` and `b60792c`. The check read every place in the
three files that names a head of PR #19, of feature 004 or of main, by a search
of each file for `f0bf538`, `662be89`, `4f1c0e0`, `3dcd2d8`, `6bf9f77`,
`b3228bb`, `c462d87`, `423a532`, `e69f6ef`, `8f6fa31`, `d764c26`, `b60792c`,
`e4a30fc` and `15504f1`, and for each mention of PR #19 and of `PR19/cmd` in the
design, the tasks and the proposal before its round sections.

Rounds (g) to (h) change six files of change 1 (`git diff --name-only 662be89
b3228bb`): its `design.md`, `proposal.md`, `tasks.md`,
`specs/project-clean/spec.md`, `specs/project-clean-review-safety/spec.md` and
`specs/project-command/spec.md`. The last is the file this change's block of [E]
is written on. It is two lines longer at `b3228bb` (361 lines, sha256
`fa8e7c21db35e86c7c6fa9b949a689eb974634ce8772bdd38b2e7b39db073258`) than at
`f0bf538`, `662be89`, `4f1c0e0` and `3dcd2d8` (359 lines, `d4cb310646343df4...`,
the same at all four), and one line longer than at `6bf9f77` (360 lines,
`cca102e8078bc18e...`). `git diff -U0 f0bf538 b3228bb` on it is two hunks, `@@
-313,0 +314 @@` and `@@ -315,0 +317 @@`, both in the scenario "A linked worktree
whose work tree is redirected" (:311-318), after the "Configuration paths"
paragraph: the AND on `registration-mismatch` that round (g3) added at :314,
which round (h) extends in place, so that the `inspection-incomplete` refusals
name the same unsetting in their remedy, and a new AND at :317 for a repository
`config` that sets `core.worktree` to the main worktree's path. Lines 1 to 313
are the same at `f0bf538`, `6bf9f77` and `b3228bb` (sha256 `070d8434cad8b1e2` at
its first 16 digits). So the block of [E] is `:108-361`, 254 lines, at
`b3228bb`, where it was `:108-360`, 253 lines, at `6bf9f77` (W66's OBS-4) and
`:108-359`, 252 lines, at `f0bf538`, and the cite `PR19/cmd` at `f0bf538`,
:116-129 holds at `b3228bb`: the paragraph begins at :116 ("Configuration paths:
before any Git child starts") and ends at :129 ("as for the version."), the same
lines in both.

No place in this change's three files states PR #19's current head as live text,
so none moves to `b3228bb`, and history stays. `proposal.md:1961`, the W57-1 row
of the round C18 table, says that the block is 252 lines (`:108-359`) at
`f0bf538`: a round's record, qualified by its sha and true there. `tasks.md:13`
holds `662be89` in its round C19 clause ("PR #19's head, now `662be89`"): the
record of what round C19 read, as every "now" in a round's clause is; the round
C22 clause added beside it gives `b3228bb`. Every other `f0bf538`, `662be89` and
`4f1c0e0` is in the sections for rounds C17 to C21 or in task 1.3's clauses for
them, records of the head each round read, but for `design.md:650`, `PR19/cmd`
at `f0bf538`, :116-129, a cite qualified by its sha and true at `b3228bb`. The
other places that speak of PR #19 in the live text (`design.md:14`, :107, :114,
:121, :396, :591, :659, :1369 and :1521-1536; `proposal.md:46`, :173-178, :251,
:336-338, :430-447, :548-549, :578-582, :656-657, :760-776, :799 and :1088) cite
`c462d87`, `f0bf538` or `423a532`, or say nothing of its head, and none says
what the head is now. Every `c462d87` stays as the ratification base, which the
key defines for `PR19/cmd`, and so do the cites of `PR19/cmd` at that base
(:123-125 at `design.md:396`, :189-192 and :206 at `proposal.md:764-765` and
:799).

Every `423a532` (`design.md:107`, :174 and :591, and the round C15 section)
cites feature 005's Q9 B at the sha where it was read: the nine lines of
PR #19's design on the scrub of Git children are `:331-339` at `423a532`,
`:358-366` at `f0bf538`, `:361-369` at `662be89`, `:364-372` at `4f1c0e0`,
`:365-373` at `3dcd2d8`, `:370-378` at `6bf9f77` and `:377-385` at `b3228bb`,
byte for byte equal at the seven, so the cite is true at the new head, and
stays. Feature 004's `project` at `b60792c` is no longer byte for byte as at
`e69f6ef`, as it still was at `8f6fa31` (`git diff --shortstat e69f6ef b60792c
-- project`: 78 insertions and 24 deletions), but `ChildHandle.start` still
spawns with `env=git_env(kind)` at `project:1077`, with `GIT_KINDS` at :984 and
`git_env` at :1000, the same lines as at `d764c26`, so RI-6's note stands at the
new head, and its `e69f6ef` cite (`design.md:215` and the round C18 section)
stays as the sha it was read at. A1 is still at `e4a30fc`, so D5's ":868-876 at
`e4a30fc`" (`design.md:657`) stays, and main is still at `15504f1`, so the
places that name it stay. Places edited for currency: none.

The report on PR #19's round (h), with no edit, quoted from `b3228bb` itself.
Brett Heap ruled F-1, F-2 and O-1 at 15:24Z (R-263), and round (h) carries them,
in change 1's `specs/project-clean/spec.md`. F-1 gives the ceiling's recovery
text two forms: "inspect, then `git worktree remove --force <path>` by hand"
"where the rescan finds both its `.git` file and its registry entry present",
and "inspect, then `git worktree prune` and delete `<path>` by hand" "otherwise,
as where either is gone, since Git then refuses `git worktree remove --force`"
(the ceiling paragraph, :321-331; its scenario, :500-504; the reconcilable
block, :1158-1162). O-1 gives gate 7's budget-cut sentence gate 11's form: "a
read not finished within the filesystem budget, the deadline not being the
limit, SHALL leave the row unprobed and the plan incomplete with
`inspection-incomplete`; and a read that the deadline cuts SHALL record
`deadline-exceeded` and leave the row unprobed and the plan incomplete with
`deadline-exceeded`, not `inspection-incomplete`, as for every other filesystem
read" (:713-718). F-2 stands as written, its locked-worktree text being
"inspect, unlock it, then `git worktree remove --force <path>` by hand"
(:170-172 and :211-212, the same lines as at `6bf9f77`).

This change carries or restates none of the three. A search of the five files,
before this section was added, for "worktree remove", "inspect, then", "inspect,
unlock", "unlock it", "git worktree prune", "delete `<path>`",
`partially-removed`, `removal-ceiling`, "hard ceiling", "recovery text",
`inspection-incomplete`, "filesystem budget", "the deadline not",
`reflog-unavailable`, "gate 7", "--force" and "worktreeConfig" found no line,
and "ceiling", "300 s", "unprobed" and "unlock" gave three places that come near
them, none a restatement. `specs/project-command/spec.md:107-108` is the carried
Termination sentence of [E], as PR #19 has it at `c462d87` and still at
`b3228bb` ("A removal child SHALL instead be waited for, and SHALL NOT be
signalled before its 300 s ceiling"): it names the ceiling and not the recovery
text. `specs/project-overview/spec.md:71-75` is change 2's own sentence on a
task cut by its bound, "a reflog read cut this way leaving its row unprobed for
the gate that `Overview suggests only gated clean commands` states", which is
not gate 7's sentence and does not repeat its cases.
`specs/project-overview/spec.md:6` says "no worktree created, pruned, repaired,
locked or unlocked", the read-only guarantee, which is no recovery text. So this
change has no site that re-bases on round (h). Round (h)'s change to the
`project-command` spec lies at :314 and :317, in the scenario "A linked worktree
whose work tree is redirected", which this change's block does not carry: the
block carries PR #19's nine scenarios as at `c462d87`, which has no such
scenario (`grep` of that file for "redirected" finds none), and adds its own
tenth.

This file: Status, within its 22 lines, says "rounds C15 to C22" and "C-50 to
C-68" and names "W66"; its clause "C-58, C-66, C-67 also in the spec, C-63, C-65
in Decisions" is as it was, C-68 being in `design.md` alone; and the citation
key, at :45, reads "C-68". No line of this file moved: lines 1 to 2368 keep
their numbers, this section following them, and every paragraph before line 1252
keeps its line count and its place (55 paragraphs, each with the same first line
and the same line count). Lane openRepoProject-4's pinned ranges are
`cmp`-identical to `8276945`: lines 1252 to 1417 of this file, rounds C6 to C12,
and lines 334-345, 367-370 and 430-438; "Dependencies and Sequencing" (181
lines, sha256 `c4d7a1797d240880` at its first 16 digits) and "Open Questions"
(39 lines, `ca53d0f392adc7e5`), each compared whole by sha256; `tasks.md` lines
20-23 (sha256
`2e177de7a91d644759bb5e12177696c749be9d9e90a763ce9899e238e7c0e2c0`); D5's
residual :574-601 and D7 :954-989 of `design.md`; and lines 1 to 419 of the
spec.

The writer checked these on 2026-10-22, in a scratch directory outside this
tree. W66's report was read from lane openRepoProject-3's attachments on the
register's `origin/main` with `git show`, and its lines were found at this head
by their text; PR #19's files were read with `git show` at each head named
above. The carry check of every MODIFIED block against its source is as in
rounds C19 to C21, since both spec files are byte for byte as at `8276945`:
"Overview is local and read-only" 1 of 1 scenarios, +33/-0; "Overview bounds its
work and reports what it omitted" 13 of 13, +26/-0; "Overview prints a versioned
JSON envelope" 6 of 6, +12/-0, against change 2 at `961c405`; and [E] 9 of 9,
+11/-0, against PR #19 at `c462d87`. Validation, run before each of the round's
commits and again at its head (a commit cannot hold its own sha; the head is in
the round's report): `/usr/bin/openspec validate
add-project-overview-remote-merge-status --strict` reports the change valid with
its two INFO lines, `/usr/bin/openspec validate --all --strict` passes 8 of 8,
and `/usr/bin/openspec status --change add-project-overview-remote-merge-status
--json` shows every artifact done. The added text holds no non-ASCII character,
bidi control, host path or literal backslash-u, and a grep of the three files
for placeholders found none.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Lane openRepoProject-3's W66 on rounds C19 and C20 (`e1a9f84..a6080a7`, `confirm-c19c20-findings.md`, brett-wip `4ea08c0b3`, received by the lead at 15:34:53Z) | 0 HIGH, 0 MEDIUM, 4 LOW | C-68: W66 found 0 HIGH, 0 MEDIUM and 4 LOW (C20-1 to C20-4) and six observations (OBS-1 to OBS-6), and no departure from a ruling, the packet or ratified text. C-62, C-63, C-65 and C-66 are applied: task 2.4 equals lane openRepoProject-4's held new line byte for byte, with task 2.3 unchanged; the four packet quotes in the two Decisions entries match `da33d92`; the Departures heading is right; D11's split list, D5's append, Risks' bracket and the Decisions bullet carry C-58; the cite "`PR19/cmd` at `f0bf538`, :116-129" stands at every old site; and the spec's sha256 and counts are as recorded at `a6080a7` (`6fda0ae8...`, 36 and 10). Lane openRepoProject-4's pins are `cmp`-identical, `validate --strict` is valid, `--all --strict` passes 8 of 8, and every hunk is declared. Its four LOWs are the next rows. The observations ask for no edit: OBS-1 (D5's append points at the paragraph and C-58, acceptable as applied), OBS-2 (29-01's "departs from both", harmless), OBS-3 (a cite in W62's own row, lane openRepoProject-3's file), OBS-5 (task 1.3's C18 clause still says "a run that neither refuses first", history beside round C20's wording) and OBS-6 (D11 on a base with [E] and no A1, not new to C20, and D11 names the A1 case only) are left as they are, and OBS-4 (#19 had moved) is the currency row's | none |
| W66's C20-3 (`design.md:653-654`: "whether the subcommand then refuses or reports being its own requirement's rule" does not parse; #19's text is "whether the subcommand then refuses or reports is its own requirement's rule, as for the version", `PR19/cmd` at `f0bf538`, :128-129; W66's fix ends the clause at "(`relative-config-path`)", adds the "; whether ..." clause, and corrects the quotation in the round C20 section) | LOW | C-68: applied to the design, in `bbe8d53`, committed first: the clause ends at the code and goes on "; whether the subcommand then refuses or reports is left to its own requirement's rule", the lead's "left to" for #19's "is", and without the brief's "the run", which would take the paragraph to 26 lines and move D7. The paragraph keeps its 25 lines (:646-670) and `design.md` its 1560, with D5's residual :574-601 and D7 :954-989 `cmp`-identical to `8276945`. Declined, for the quotation in the round C20 section (:2177-2178): it records what `6527f73` wrote, and a round's record is history that this round does not edit | `design.md` D5 (:653-655) |
| W66's C20-4 (optional: the round C20 table has no row for Codex's review of `9a3f684`, as the round C18 and C19 tables have rows for their heads) | LOW | C-68: recorded as this row, since round tables are history and no earlier table is edited. Codex's review of `9a3f684` (2026-10-22T14:17:24Z) found no major issue ("Didn't find any major issues"), as the lead's late read of 14:23:00Z records it, with SonarCloud passing; the head had already moved to `e053ad6`, round C20's first commit, as that read notes. Nothing to apply | none |
| W66's C20-1 (the last AND of the scenario "No gh, or a gh without authentication", `specs/project-overview/spec.md:624`, says "refuses the run" of both requirements) and C20-2 (four cites of the overview spec in `design.md`, :918, :1152, :1167 and :1168, are stale; W66 adds the fourth to the three that lane 5 queued) | LOW | C-68: both are the items that round C21 applied, which W66 found real: "refuses" became "stops" in `1cd73fb`, and the four cites became `spec.md:483` (:918 and :1152), `:478-479` (:1167) and `(:470-471)` (:1168) in `266a30f`. Recorded here as applied in round C21, whose table holds their rows, with nothing to apply again; at this head :624 says "stops" and the four cites read as above | none |
| The lead's currency check for round C22, as the lead's message moved it: PR #19 is now at `b3228bb` (round (g) at `4f1c0e0`, (g2) at `3dcd2d8`, (g3) at `6bf9f77` and round (h) at `b3228bb`, after round (f) at `662be89`), its `project-command` spec two lines longer than at `f0bf538` (361 lines, sha256 `fa8e7c21...`), feature 004 at `b60792c`, A1 (#34) at `e4a30fc` and main at `15504f1`; W66's OBS-4 had it at `6bf9f77` | ruling | applied by reading every place, and no place edited: no place in the proposal, design or tasks states PR #19's current head as live text, so none moves to `b3228bb`. The block of [E] is `:108-361`, 254 lines, at `b3228bb` (`:108-360`, 253 lines, at `6bf9f77`; `:108-359`, 252 lines, at `f0bf538`), the two added lines lying at :314 and :317 in the scenario "A linked worktree whose work tree is redirected", and the cite `PR19/cmd` at `f0bf538`, :116-129 holds there. Read and left: `proposal.md:1961` (a row of the round C18 table, "252 lines (`:108-359`) at `f0bf538`", qualified by its sha); `tasks.md:13` (`662be89` in the round C19 clause, the record of what round C19 read); every other `f0bf538`, `662be89` and `4f1c0e0` (rounds C17 to C21); `design.md:650`; every `c462d87`, the ratification base; every `423a532` (Q9 B's nine lines, equal at seven heads, `:377-385` at `b3228bb`); RI-6's `e69f6ef` (`ChildHandle.start` still spawns with `env=git_env(kind)` at `b60792c`, `project:1077`); A1's `e4a30fc` (`design.md:657`); and main's `15504f1`. The paragraphs above give each | none |
| Report only, with no edit: PR #19's round (h), accepted at `b3228bb` (Brett Heap's ruling R-263 of 15:24Z: F-1 prune-then-delete, F-2 yes, O-1 deadline-exceeded), which carries the ceiling's two recovery texts (PR #19's `specs/project-clean/spec.md` at `b3228bb`, :321-331, :500-504 and :1158-1162), gate 7's budget-cut sentence (:713-718) and F-2's locked-worktree text (:170-172 and :211-212) | report | C-68: this change carries or restates none of the three, and no line is edited. A search of the five files for the texts' words found no line; the three places that come near them are `specs/project-command/spec.md:107-108` (the carried Termination sentence, "A removal child SHALL instead be waited for, and SHALL NOT be signalled before its 300 s ceiling", which names the ceiling and not the recovery text), `specs/project-overview/spec.md:71-75` (change 2's own sentence on a cut reflog read, which is not gate 7's) and `:6` (the read-only guarantee's "locked or unlocked"). The paragraphs above quote the three texts and give the search. Round (h)'s change to the `project-command` spec (:314 and :317) lies in a scenario that this change's block does not carry (the block has PR #19's nine scenarios as at `c462d87`, and its own tenth) | none |
| The `@codex review` request on `8276945`, round C21's head, of 15:36:19Z (comment 6344720178), and the lead's late read of 15:52:41Z | no finding | Codex's usage-limit reply came at 15:36:31Z, so Codex did not review round C21, and there is no Codex finding to apply; the late read finds CI, all six test jobs, and SonarCloud passing on #29 at `bbe8d53`, this round's first commit. Nothing to apply | none |
| The record: Status, the citation key, and tasks 1.1, 1.3 and 1.5, in place | ruling | C-68's record: Status says "rounds C15 to C22" and "C-50 to C-68" and names W66, within its 22 lines (its clause "C-58, C-66, C-67 also in the spec, C-63, C-65 in Decisions" is as it was, C-68 being in `design.md` alone); the citation key reads "C-15 to C-68"; `tasks.md` 1.1 lists C-45 to C-68, 1.3 gains a round C22 clause (this round recording itself, as C-56 orders) and "Re-read and Codex Findings (round C22)" in its verified-by list, and 1.5 names round C22; 1.4 is not edited, since no spec edit is committed; the tasks file is 45 lines still | Status; citation key; `tasks.md` 1.1, 1.3, 1.5 |
