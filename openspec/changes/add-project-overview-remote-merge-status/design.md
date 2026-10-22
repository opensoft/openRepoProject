Lane: openRepoProject-5

# Design

## Context

See `proposal.md` for why and what, and the deltas under `specs/` for the
requirements. `specs/project-overview/spec.md` modifies "Overview bounds its
work and reports what it omitted" (fourteen scenarios, one of them new),
"Overview prints a versioned JSON envelope" (seven scenarios, one of them new)
and "Overview is local and read-only" (two scenarios, one of them new), and
adds "Overview reports remote merge evidence on request" (thirteen scenarios);
`specs/project-command/spec.md` modifies change 1's "Repository inspection
requires Git 2.36 and shares one evidence model" on draft PR #19's text (ten
scenarios, one of them new; C-11). The council (product-advocate,
systems-architect and adversary-engineer) read `c928cb2` on 2026-10-20, and
the lane's lead ruled all twelve of its concerns VALID and none NOTED (C-16 to
C-22), so there is no `clarifications.md`: the decisions below carry the
verdicts, and round C4's edits to `specs/project-overview/spec.md`, agreed
by lane openRepoProject-4 on 2026-10-20, are committed (`proposal.md`,
Dependencies and Sequencing). Round C5 applies lane openRepoProject-3's delta
read of `e198548` and Codex's three findings on it (C-24 to C-27), with the
lead's C-28 and C-29 on two points found in applying them; its edits to
`specs/project-overview/spec.md`, agreed by lane openRepoProject-4 on
2026-10-20, are committed (`6fe8a5e`; `proposal.md`, Dependencies and
Sequencing). Round C6 applies Codex's finding on `67e43ae` (C-30), the
bounded inspection of a remote's URL, with the lead's C-31 to C-33 on three
points found in applying it, and lane openRepoProject-3's folded read of
`e198548..67e43ae` (C-34); its edits to `specs/project-overview/spec.md`,
agreed by lane openRepoProject-4 on 2026-10-20, are committed (`233df0b`;
`proposal.md`, Dependencies and Sequencing). After that agreement, C-35, as
lane openRepoProject-3's narrowing amends it, fills D5 with the lookup's
per-directory rule and D11 with two tests, and edits no spec text. Round C7 then
applies lane openRepoProject-3's confirm read of round C6c (C-36), which rewords
D5's rationale to what was observed, and Codex's P2 on `1c32667` (C-37), which
has D6 bound an integer literal at parse time and D11 test it with one test;
neither edits spec text. Round C8 then applies lane openRepoProject-3's confirm
read of round C7 (C-38), four LOWs: D5 records the shells' runs on the errors
the lookup skips and names the twelve errors injected, D6 and D11 give the
source of Python's limit on integer-string conversion and say that 3.10.0 to
3.10.6 were emulated, not run, and D11 serves a `number` of 2,147,483,647 too;
it edits no spec text either. Round C9 then applies Codex's P2 on `05a424a`
(C-39) and the lead's point found in applying it (C-40): D6's parse rejects
the constants `NaN`, `Infinity` and `-Infinity` with a `parse_constant` hook,
and decodes the body's bytes as strict UTF-8 itself, never giving `json.loads`
bytes, and D11 tests both with one test; they edit no spec text either. Round
C10 then applies Codex's P2 on `f34dfe2` (C-41) and lane openRepoProject-3's
confirm read of round C9 (C-42, its MEDIUM-1, and C-43, its four LOWs): C-41 is
declined as a design change and kept as a residual, which D5 and Risks record,
since, as the spec then had it, the `gh` child ran in the filesystem root with
every other variable passed on unread; D6 states the check of `number` by type
and inside the parse's boundary, and what a float literal and an escape of a
lone surrogate do; D2 decodes a remote-target read's output as strict UTF-8; and
D11 tests C-41's decision and C-42; they edit no spec text either. Round C11
then applies C-44, the lead's ruling on lane openRepoProject-3's and lane
openRepoProject-4's planted-configuration point, refined on lane
openRepoProject-3's six points, which replaces C-41's residual with a refusal:
the lookup of `gh` counts as failing when any of `GH_CONFIG_DIR`,
`XDG_CONFIG_HOME` and `HOME` is set to a non-empty value whose first byte is not
`/`, so that every keyed row is `gh-unavailable` and no child starts. D4, D5,
D11 and Risks record it, and its edit to `specs/project-overview/spec.md`, one
sentence in the Requests paragraph, a clause in the Results paragraph and one
AND on an existing scenario, was agreed by lane openRepoProject-4 on 2026-10-21
with two edits ("may name" for "names" in the sentence, and a relative
`XDG_CONFIG_HOME` in the AND) and is committed (`2b89bfc`): the Requests
paragraph now says that every other variable is passed on unchanged. Round C12
then applies lane openRepoProject-3's confirm read of rounds C10 and C11 (C-45),
six LOWs, with no spec edit: D6's sentence on an escape of a lone surrogate, in
which a stray placeholder had stood, is completed; the account of C-41 above
says what the spec then had; D2's list of failures names an output that does not
decode as UTF-8, and D11 pins it with one fixture; D5 says that the test refuses
a value whose first byte is any byte other than `/`; Risks names
`XDG_DATA_HOME`, `XDG_STATE_HOME` and `XDG_CACHE_HOME` in its general class,
each with only what is known of it; and task 1.5 records the validation runs on
the committed files. Round C13 then applies the read of `e11d755` by lane
openRepoProject-5's reader RC (C-46 and C-47), with no spec edit: D11's test
`PATH` holds a directory of links to `git`, `bash` and the interpreter and never
their own directories, so that a `gh` installed beside them is not found; its
fake `gh` writes a start record and an end record, so that a stopped child is
still seen; and its in-process runs fix the proxy, token and configuration
variables (M4, M5, L6). D3 says how a URL's host is read, and that a URL with no
`://` and no `:` before its first `/` is a local path to Git; D2 says what
`transfer.credentialsInUrl=die` gives; and D10 counts the reads' addition to
`probes` (L2 to L4). `proposal.md` changes its README step and Open Question 1
(L2, L5). C-48, RC's M1, M2, M3, L1 and L4's spec part, was held for lane
openRepoProject-4 in that round. Round C14 commits C-48's spec text on lane
openRepoProject-4's YES of 2026-10-21 (`c0062f9`), the file it agreed, held
revision 3, sha256
`8ef40dcabe1974d52a059ef6a513f883aa48af692759e74dea3f772a8d3145bc`, which
carries the two points the lead ruled into it and lane openRepoProject-4's
clause for a failed write to standard output: a deadline that expires in the
remote phase records no `deadline-exceeded` scan error (M1); a remote whose
fetch refspecs do not map the merge ref is `no-remote-target` (M2); the
comparison at concurrency 1 excepts `remote.limits.concurrency` (M3); a
repository whose first read named a usable remote and whose second never
started is `cancelled` (L1); and Isolation excepts a signal that ends the run
and a failed write (L4). The tool fact below, D2, D8, D10, D11 and Risks follow
it; D7, which those edits also reach, waits with task 2.3 for amendment A1's
alignment, as lane openRepoProject-4 asked. Round C14 also applies lane
openRepoProject-3's confirm read of round C13 (C-49), eight LOWs with no spec
edit, in this paragraph, D2, D3 and D11, and D5 records, on lane
openRepoProject-4's call 4, that the caller's `GIT_TRACE*` names reach the `gh`
children, a residual. Round C15 applies lane openRepoProject-3's confirm read of
round C14 (C-50), with no spec edit: D3's step 3 refuses an explicit port
itself, before the identity pattern runs, as the spec lists it; the forms in
which D3 reads a host otherwise than Git are examples, not a complete list, and
two more are named; and D5 cites PR #19 at `423a532` for Q9 B. It also applies
reader RF's M1 (C-51): the Migration Plan checks each re-read and re-base of a
block by a second diff, from this change's own block at its ratified head, and
returns any change to this change's ratified words to Brett Heap.

Citations follow `proposal.md`: the packet at `da33d92`; APO, CAS, PRS and
`project:N` at main `961c405`, which main `15504f1` holds unchanged for them
(L-15). [E] is cited on PR #19's `specs/project-command/spec.md` at `c462d87`
(C-11). Change 2's requirements are cited by header under these labels: [B]
`Overview bounds its work and reports what it omitted`, which this change
modifies for the probe count (C-9), [J] `Overview prints a versioned JSON
envelope`, which this change modifies for the two `remote` keys, [H] `Overview
renders a readable human report` and [X] `Overview exits by completeness and
severity`; change 1's evidence model is [E], which this change modifies on
PR #19's text for a stopped remote-target read and the `gh` child's limit
(C-11), and the ADDED requirement is [R].

The rulings and the packet's boundary map to the decisions:

| Source | Decision |
| --- | --- |
| C-1; DI:72-75: `project overview --remote` only | D1 |
| C-3; DI:1039-1042; PRS:32: the remote target and the identity | D2, D3 |
| C-6; DI:1044: one request per exact head, upstream-gone rows included | D4 |
| C-4; DI:1045-1051, DI:1056-1057: `gh api` and the bounds | D5, D6, D7 |
| C-5; DI:1049-1056: the fields and the explicit unknowns | D6, D8, D9 |
| C-6; DI:1051-1053: expiry cancels and aborts | D7 |
| SY:129-130; BA:195-199; DI:1059-1060: evidence, never permission | D10 |
| C-8: offline tests with a fake `gh` | D11 |
| C-9; APO/ov:248-254: the remote-target reads in the envelope's `probes` | D2, D7, D8 |
| L-10: `remote` present only where this change acts, never null | D8 |
| C-11; L-11: [E]'s Termination and Budgets sentences | D2, D7 |
| C-12; L-11: [J]'s two `remote` keys | D8 |
| C-14; APO/ov:765-766: an exception the remote phase records as none of its reasons exits 2 | D10 |
| C-16; F-3: no `closed` state, a `CLOSED` node never matching | D6, D8, D9, Risks |
| C-17: the freshness sentence and the `gh` requests started | D9 |
| C-18, C-20: the `merged` line | D9, Risks |
| C-19, C-21: the live contract check, header names without case, the resolved repository | D5, D6, D11, Risks |
| C-22: parser failures and which `gh` runs | D5, D6, D10 |
| Lane openRepoProject-3's re-read of `c928cb2`, LOW-6 and LOW-9 | D2, D7 |
| C-24: lane openRepoProject-3's delta read of `e198548`: the Q16 pointer, the lookup's test seams and the sources of two `api-error` rules | D6, D7, D11 |
| C-25: no request can be sent or answered, so `unavailable` outranks the request cap | D4, D5, D6 |
| C-26: a lookup of `gh` that fails or runs out of time | D5, D10, D11, Risks |
| C-27: one sentinel byte past each read bound | D6 |
| C-28: a key past the 64th stays `request-cap` at an expiry | D4, D5, D7 |
| C-29: one sentinel byte past each remote-target read's 64 KiB | D2 |
| C-30: a remote's URL held in memory only to derive the `owner/repository` and detect its user information | D2, D3 |
| C-31: a remote-target read's standard error drained and discarded unexamined | D2 |
| C-32: the user part of a credential-bearing URL checked on its own in the outputs | D3 |
| C-33: that user part a token no path, user or test name plausibly holds | D3 |
| C-34: lane openRepoProject-3's folded read of `e198548..67e43ae`: the lookup's place, the request cap's precedence and the exact-size tests | D1, D4, D11 |
| C-35: lane openRepoProject-3's narrowing of the lookup's per-directory rule: a directory where `gh` is absent is skipped, any other error fails the lookup | D5, D11 |
| C-36: lane openRepoProject-3's confirm read of C6c: D5's rationale claims only what was observed | D5 |
| C-37: Codex's P2 on `1c32667` at design.md:457: integer literals bounded at parse time by a `parse_int` hook, on every supported Python | D6, D11 |
| C-38: lane openRepoProject-3's confirm read of C7: D5's shell runs on the skipped errors and the twelve errors named, D6's source for Python's integer-string limit, D11's `number` of 2,147,483,647 | D5, D6, D11 |
| C-39: Codex's P2 on `05a424a` at design.md:484: the constants `NaN`, `Infinity` and `-Infinity` are no JSON, so a `parse_constant` hook rejects them wherever they stand, on every supported Python | D6, D11 |
| C-40: the lead's point found in applying C-39: the parse decodes the body's bytes as strict UTF-8 itself and gives `json.loads` the string, so that UTF-16, UTF-32, an encoded surrogate and a UTF-8 byte order mark are `api-error` | D6, D11 |
| C-41: Codex's P2 on `f34dfe2` at design.md:381: a relative `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` or `HOME` resolves against `/` when the child starts there; declined as an anchoring and kept in round C10 as a residual, which C-44 replaced | D5, D11, Risks |
| C-42: lane openRepoProject-3's MEDIUM-1 on round C9: a node's `number` is accepted only when its parsed type is exactly `int`, and every check on the parsed answer runs inside the parse's catch-everything boundary | D6, D11 |
| C-43: lane openRepoProject-3's four LOWs on round C9: no `parse_float` hook, by decision; the escape of a lone surrogate; each remote-target read's output decoded as strict UTF-8; and three wordings | D2, D6, D11 |
| C-44: the lead's ruling on lane openRepoProject-3's and lane openRepoProject-4's planted-configuration point, refined on lane openRepoProject-3's six points: the lookup of `gh` counts as failing when any of `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` and `HOME` is set to a non-empty value whose first byte is not `/`, so every keyed row is `gh-unavailable` and no child starts; other relative paths that `/` re-anchors stay residuals (Risks); its spec sentence is committed on lane openRepoProject-4's YES of 2026-10-21 (`2b89bfc`) | D4, D5, D11, Risks |
| C-45: lane openRepoProject-3's confirm read of rounds C10 and C11, six LOWs, applied in the design and tasks with no spec edit: D6's escape sentence completed, the Context's tense, tasks 1.5's record of the validation runs on the committed files, D2's list of failures and D11's fixture for an output that does not decode as UTF-8, D5's wording of a first byte, and the three XDG variables in Risks | D2, D5, D6, D11, Risks |
| C-46: reader RC's M4, M5 and L6: D11's test `PATH` holds a directory of links to `git`, `bash` and the interpreter and never their own directories, so that a `gh` beside them (on `ubuntu-latest`, `/usr/bin/gh` beside `/usr/bin/git`) is not found; the fake `gh` writes a start record, with its pid and process group, and an end record, so that a stopped or killed child is still seen; in-process runs set the proxy variables in the environment the overview passes on, remove `NO_PROXY`, `no_proxy`, `GH_TOKEN` and `GITHUB_TOKEN`, and fix `GH_CONFIG_DIR` and `XDG_CONFIG_HOME` as absolute or unset | D11 |
| C-47: reader RC's L2 (the design part), L3, L4 (the design part) and L5, with no spec edit: D3 says how a URL's host is read, and that a URL with no scheme and no `:` before its first `/` is a local path to Git with no host, so `not-github`; D2 says that with `transfer.credentialsInUrl=die` a password-bearing remote reads `remote-target-unread` and that nothing leaks; D10 counts the reads' addition to `probes`; the README's next steps and Open Question 1 change in `proposal.md` | D2, D3, D10 |
| C-48: reader RC's M1, M2, M3, L1 and L4's spec part, held in round C13 and committed in round C14 on lane openRepoProject-4's YES of 2026-10-21 (`c0062f9`), with the lead's two points and lane openRepoProject-4's clause for a failed write: no `deadline-exceeded` scan error at an expiry in the remote phase; `no-remote-target` for a remote whose fetch refspecs do not map the merge ref; `remote.limits.concurrency` excepted from the comparison at concurrency 1; `cancelled` for a repository whose second read never started; Isolation's exceptions for a signal and a failed write; D7's follow-ons wait with task 2.3 for amendment A1's alignment | Context, D2, D8, D10, D11, Risks |
| C-49: lane openRepoProject-3's confirm read of round C13, eight LOWs, with no spec edit: a `:` begins a port only when digits follow it, and `ssh://git@github.com:acme/widget.git` is a residual; a local path is a URL with no `://` and no `:` before its first `/`; the `die` rule from Git 2.37.0, whose release notes introduce `transfer.credentialsInUrl`; the in-process environment's linked `PATH`; the packet's `github.com/owner/repository` an identity, not a form of URL; step 1's conservative reading of a user that holds a `:`; and, in `proposal.md` and `tasks.md`, Status, Decisions, the round C13 row of L2 and task 1.3 | Context, D2, D3, D11 |
| Lane openRepoProject-4's call 4 on C-48 (2026-10-21): the caller's `GIT_TRACE*` names reach the `gh` children unread, recorded as a residual, as tested | D5 |
| C-50: lane openRepoProject-3's confirm read of round C14 (W16), with no spec edit: step 3 refuses an explicit port before the identity pattern runs, as the spec lists it, since before a one-segment path the pattern gives an identity; D3's forms in which its host differs from Git's are examples, not a complete list, `:+22` and a bracketed `[github.com]` added; D5 cites PR #19 at `423a532` for Q9 B | D3, D5 |
| C-51: reader RF's M1: each re-read or re-base of a block is also diffed from this change's own block at its ratified head, and any change it shows to this change's ratified words returns to Brett Heap | Migration Plan |
| C-10, L-12: CI on Linux only | Migration Plan |

What in `project` shapes the approach (at `961c405`; features 004 and 005
move these lines, and this change's feature re-pins them):

- `probe()` (`project:60-65`) runs a child through `subprocess.run` with a
  fixed 15 s timeout and `GIT_OPTIONAL_LOCKS=0`, killing the one process,
  never its group. It is not used for `gh`: a request needs its own process
  group, a 5 s limit, a streamed and capped standard output, and termination
  together with the overview's other children.
- `github_repository_identity()` (`project:759-763`) accepts an `owner` and a
  `repository` by one pattern each, and `remote_repository_identity()`
  (`project:766-769`) accepts `https://github.com/` and `http://github.com/`,
  and `github.com` followed by `:` or `/` with an optional `ssh://` and an
  optional `git@` before it, strips `.git`, and matches no other user, so
  `https://user@github.com/...` never yields an identity. Together they are the
  rule PRS:32 states for status and doctor, where `handoff()`
  (`project:772-783`) takes the identity from `git remote get-url origin`. D3
  reuses both, adds the reason that tells a credential-bearing URL from a
  foreign host or a malformed path, and gives a URL that Git reads as a local
  path no host, whatever the pattern makes of it (C-47).
- `cleanup_report()` (`project:544-622`) is where `09af8c8` attached its
  lookup and its three extra classes; this change touches nothing of `clean`.
- The parser (`project:1074`) has no `overview` yet. Feature 005 adds the
  subcommand; this change's feature adds `--remote` to it.
- The tests' fakes: `fake_bin()` (tests:148) is the temporary bin directory,
  `write_fake()` (tests:172) writes a fake tool into it, and `question_env()`
  (tests:154-170) builds a `PATH` of that directory and the directories of
  `bash`, `git` and the interpreter, dropping `GH_TOKEN` and `GITHUB_TOKEN`.
  D11 builds on all three, and puts a directory of links to `bash`, `git` and
  the interpreter in that `PATH` in place of their directories (C-46).
- After features 004 and 005: the overview's control loop on the main thread
  with its in-flight child registry, self-pipe and signal handling (APO
  design.md, D1), its two-phase scheduler (D6) and its renderers (D10), driving
  change 1's child handle (start, readable descriptors, `terminate_group` with
  the 2 s grace, reap). The realization adds a phase and a child kind to that
  loop and asks nothing of feature 005 in advance (`proposal.md`, Open
  Questions 3). Feature 004's handle is not yet that start path for `gh`
  (reader RE's RE-15, sharpened by reader RI's RI-6; C-57): `ChildHandle.start`
  always spawns with `env=git_env(kind)` (004 `project:1049` at `e69f6ef`),
  which removes the Git names, sets `TRACE2_OFF` and takes only a `GIT_KINDS`
  key, so it cannot yet give a `gh` child the environment that the Requests
  paragraph and D5 specify, with the Git scrub not applying and every other
  variable passed on unchanged (`specs/project-overview/spec.md:405-417`, this
  bullet and `design.md:579-584`, at `2ab3743`). A `gh` row in `GIT_KINDS` would
  break that "unchanged"; the realization needs a start path that takes its own
  environment, and that path is not built.
- Tool facts checked for this design: Git 2.43.0 answers
  `for-each-ref --format='%(upstream:remotename)%00%(upstream:remoteref)'`
  from `branch.<name>.remote` and `.merge` with no remote-tracking ref
  present, prints `.` for a local remote and empty fields for a remote given as
  a URL, for a branch with either key unset, or for a remote whose fetch
  refspecs do not map the merge ref, its `remote.<name>.fetch` unset or covering
  other branches only, where `git remote add` writes one that maps every branch
  (C-48's M2: reader RC's cases, repeated by the writer of the held file), and
  `git remote get-url <name>`
  expands `url.<base>.insteadOf` and exits 2 for a remote that is not
  configured. `gh` 2.96.0 documents exit status 4 for a command that "requires
  authentication" (`gh help exit-codes`) and the environment switches D5 sets
  (`gh help environment`); with no token, an empty configuration directory and
  its proxy pointed at a closed local port, `gh api` exited 4 with nothing on
  standard output instead of failing on the unreachable proxy.
  `Commit.associatedPullRequests` was checked live on 2026-10-19 by two
  read-only GraphQL queries of D5's shape against `opensoft/openRepoProject`:
  for the head commit of the squash-merged pull request #31 (`e3ad3cc`, one
  commit, its branch still present, outside `main`'s ancestry, squashed as
  `63dd4ad`) and of #17 (`0764624`, five commits, its head branch deleted,
  outside `main`'s ancestry, squashed as `f401e06`), each answer held exactly
  that pull request, with `state` `MERGED`, `headRefOid` equal to the commit,
  `baseRefName` `main`, `baseRepository.nameWithOwner`
  `opensoft/openRepoProject` and `hasNextPage` false. Offline, with empty
  configuration, state and cache directories and its proxy at a closed port,
  `gh` 2.96.0 under D5's switches wrote no file, both when it exited 4 for want
  of a token and when it exited 1 on the refused connection with nothing on
  standard output. The lane's lead checked one more case live on 2026-10-20
  (ruling F-3): for the head commit of PR #2, closed without merging
  (`cleanup`, `bb91a49`), `Commit.associatedPullRequests` returned
  `totalCount` 0, so D5's query answers such a head with no node and its row
  reads `not-found` (C-16). Neither check recorded `gh`'s output under D5's
  exact argv, so task 2.5 runs it once by hand before the Speckit handoff and
  records here, verbatim, the status line, the header names as `gh` prints
  them and an answer for each state and case it names (C-19, C-21).

## Goals / Non-Goals

**Goals:**

- Beside each kept worktree, say whether GitHub holds a merged or an open
  pull request for exactly its head, within the overview's 64 s bound.
- Give every failure one explicit reason, and let nothing remote reach a
  local result.
- Let `project` keep, show and use no credential, inspecting a remote's URL
  in memory only to derive the `owner/repository` and detect its user
  information (C-30), and let `project` start `gh` only with the fixed query
  and its switches.
- Make an uncut `--remote` run's `remote` fields a function of the answers
  alone.

**Non-Goals:**

- Network use anywhere but `project overview --remote`.
- A fetch, a comparison with the merge target's remote-tracking ref, or a
  squash-equivalence proof.
- Hosts other than `github.com`, GitHub Enterprise included.
- Any cache, `project`'s or `gh`'s.
- Explaining rows local ancestry already proves (`merged-removable`,
  `merged-current`).

## Decisions

### D1. The opt-in and the remote phase

`--remote` is a flag of `project overview` only. Without it no code path of
this change runs: no `PATH` lookup, no remote-target read, no field and no
line, so the default document and report are change 2's.

With it, the remote phase runs on the overview's control loop after
collection, that is, after every candidate is collected or cut and every row
is classified and gated. It has two steps:

1. The remote-target reads (D2), for the repositories with a queried row, in
   rank order, under change 2's concurrency rule (at most four Git children,
   one per repository at a time) and [B]'s per-child budget,
   `min(5 s, deadline - now)`.
2. The requests (D5), once step 1 has finished for every such repository or
   the deadline has passed. The remote budget ends at
   `min(start of the first request + 30 s, deadline)`.

The lookup of `gh` (D5) runs once, between the two steps: after step 1 has
finished for every such repository or the deadline has passed, and before the
first request, under `min(5 s, deadline - now)`. Every key therefore exists
when it ends, as the rule for a lookup that the deadline cuts presumes: such
a lookup leaves its keys `cancelled` within the cap and `request-cap` past it
(C-26, C-28; lane openRepoProject-3's folded read, L3; C-34).

The loop's wait already takes the nearest of every child's limit end and the
deadline (APO design.md, D1); the remote budget's end joins that set.

Rejected: interleaving requests with collection, which needs a hook in
feature 005's scheduler and makes dispatch depend on completion order;
cutting collection to 30 s under `--remote` to reserve the remote budget,
which changes [B]'s deadline for collection, a sentence this change does not
modify.

### D2. Reading the remote target

Per repository with a queried row, in the directory [E] names for
repository-wide probes, with [E]'s scrub, `GIT_OPTIONAL_LOCKS=0` and the seven
protocol pins:

1. `git for-each-ref --format=%(upstream:remotename)%00%(upstream:remoteref)%00 refs/heads/<target>`,
   where `<target>` is `merge_target.name`. An empty remote name (no
   `branch.<target>.remote` or no `branch.<target>.merge`, a remote given as a
   URL, or a remote whose fetch refspecs do not map the merge ref, so that Git
   names no upstream for the merge target, C-48's M2), a remote of `.`, or a
   merge ref outside `refs/heads/` gives `no-remote-target`, and the second
   child does not run.
2. `git remote get-url <remote name>`, which prints the URL as Git expands
   `url.<base>.insteadOf`. Exit 2, Git's status for "No such remote", gives
   `no-remote-target`: the exit status decides, never Git's message (C-31).
   The name is passed as Git printed it; a name Git would read as an option
   only makes the child fail.

Any other failure, a budget reached or a stop at the deadline gives
`remote-target-unread` (D7). Each child's standard output is read to at most
64 KiB and one byte and kept to at most 64 KiB, the byte past the cap telling
an output of exactly 64 KiB from a longer one, which fails the read (C-29),
and its standard error is drained and discarded unexamined, never read for a
reason or kept for a message, because Git may echo the remote's name or URL,
user information included, there (C-31). The loop decodes each read's standard
output itself, as strict UTF-8 (`bytes.decode("utf-8")`, its default `strict`
error handler), never with `surrogateescape`; an output that does not decode
fails the read and gives `remote-target-unread`, as an output past 64 KiB does
(C-29), which is the spec's "fails for any other cause"
(`specs/project-overview/spec.md:392-393`), so a `baseRefName` (D6) can equal
only a merge ref that is valid UTF-8 text (C-43). The URL that standard output
carries is the only credential-bearing text the overview inspects: it lives in
memory only while D3 derives the `owner/repository` and detects the URL's user
information; after that no part of the user information is retained or
compared, none is ever printed, logged, sent or used to authenticate, and the
URL is never forwarded with it (C-30). Under a Git configuration that sets
`transfer.credentialsInUrl` to `die`, a Git that honours the setting refuses a
URL that holds a password: Git 2.43.0 exits 128 on each of the two reads of a
merge target whose remote's URL holds one, the first with nothing on standard
output, so that no second read starts and the repository's queried rows are
`unknown` with reason `remote-target-unread`, as for any other failing read, and
never `credential-bearing-remote`, which D3 reaches only when the reads succeed.
Nothing leaks: Git's message gives the URL's user part, with the password
redacted, on standard error, which is discarded unexamined (C-31), and under
`warn` Git writes the same warning there and both reads succeed. A
credential-bearing remote that the merge target does not use leaves both reads
alone; the writer saw each of these on Git 2.43.0 on 2026-10-21 (C-47). Git
honours the setting from 2.37.0, whose release notes introduce it: in Git's
`Documentation/RelNotes/2.37.0.adoc`, read on 2026-10-21, the variable
`transfer.credentialsInURL` "controls what happens when a URL with embedded
login credential is used on either" fetch or push. Both reads meet it though
neither fetches or pushes: in Git's `remote.c` at `v2.37.0`, as at `v2.43.0`,
the check runs whenever a remote is looked up, which `git remote get-url` does
and the upstream atoms do through the merge target's branch, and `v2.36.0`
has no such check. So on the 2.36 floor the setting is unknown, both reads
succeed, and D3 gives such a remote `credential-bearing-remote`; no request is
sent either way. Lane openRepoProject-3 saw a 2.36.6 build give both reads exit
0 under `die` and `warn`, and a 2.40.4 build refuse both under `die`; Git 2.37
to 2.39 were not run (C-49).

The two reads are counted in the envelope's `probes`, as lane
openRepoProject-4's fourth option has it (C-9): they are Git children, so
[B]'s `performed`, "every Git child started", counts them unchanged, and
[B]'s added paragraph gives `estimated` 1 per repository with a queried row
and 1 more per such repository whose first read named a usable remote, so the
reads add the same number to both counts in an uncut remote phase. A run
without `--remote` counts exactly as [B] does at `961c405`. The `remote` object
has no `probes` of its own, and the `gh` children, which are not Git children,
are counted only in `remote.requests` (D5). A read that exits nonzero, reaches
its budget, overruns its output cap, gives output that does not decode as UTF-8
(C-43) or is stopped at the deadline is `remote-target-unread` on its rows'
`remote` and never a row error or a scan error, the exception that [B]'s added
paragraph and [E]'s added Termination sentence state (D7, D10).

[E]'s pins sentence, "with the pins the fetch fails locally, the probe fails,
and its row is `inspection-error`" (PR19/cmd:123-125), does not reach these
reads: `for-each-ref` with only upstream atoms and `remote get-url` read no
object, so no lazy fetch can arise for them, and a read that fails for any
other cause is `remote-target-unread` on its rows' `remote`, as [B]'s added
paragraph states. This is reasoning, not a test (the alignment review's G1
note (c); lane openRepoProject-3's re-read, LOW-9).

Rejected: parsing `<common_dir>/config` (includes, conditional includes and
`insteadOf` in other files would disagree with Git, as change 2's design
found for `core.worktree`); `git config --list` (it would read every value,
an `http.<url>.extraHeader` token included); falling back to `origin` when
the merge target has no remote (C-3 names the merge target's configuration
alone, and a guess could ask the wrong repository); counting the reads in a
`remote.probes` of their own beside an envelope `probes` kept at
collection's count (the first draft, which left a run two counts of Git
children and read [B]'s "every Git child" as collection's alone); and a flat
2 reads per repository in `estimated`, which a merge target that names no
remote, read once, would leave above `performed` in an uncut run.

### D3. Judging the URL

In this order, the first that applies deciding:

1. `credential-bearing-remote`: a URL of the form `scheme://userinfo@host...`
   whose user information holds a `:`, or that has any user information when
   the scheme is `http` or `https`; or an scp-like `user@host:path` whose user
   holds a `:`.
2. `not-github`: a host other than exactly `github.com`, so `evilgithub.com`,
   `github.com.example.org` and `api.github.com` are refused.
3. `malformed-remote`: `remote_repository_identity()` (`project:766-769`)
   yields no identity, as for `https://github.com/acme` or a user other than
   `git`. An explicit port is also refused here, before that function runs
   and whatever identity it would give, as
   `specs/project-overview/spec.md:389-390` lists an explicit port among this
   reason's causes beside the identity rule (C-50): before a one-segment path
   the function gives an identity, `22/widget` for
   `ssh://git@github.com:22/widget` and `99999/widget` for
   `ssh://git@github.com:99999/widget`, so a step 3 that left the port to it
   would ask GitHub about the wrong repository.

Every step reads the host as Git reads the URL, except in forms such as those
that the next two paragraphs name, which are examples and not a complete list
(C-50), for none of which a request is sent; the host and the scheme compare as
written, never without case (C-47, C-49). A URL with `://` has
its scheme before it, then any user information before an `@`, then the host, up
to the next `/` or a `:` that begins a port, which a `:` does only when digits
alone follow it up to that `/`, as Git reads a port (C-49). An scp-like URL has
no `://` and a `:` before its first `/`, and its host is what stands after any
`user@` and before the `:` that begins the path. A URL with neither, no `://`
and no `:` before its first `/`, is a path on the local disk to Git and has no
host, so it is `not-github` at step 2 however it reads: `github.com/acme/widget`
and `github.com/acme/widget.git`, which `remote_repository_identity()`'s pattern
alone gives as `acme/widget`, are never sent. The packet's
`github.com/owner/repository` (DI:1039-1042) names the identity derived from a
remote, not a form of URL that is accepted: as a URL, that string is such a
local path (C-49). The writer saw, on 2026-10-21, that function, taken from
`project` at `961c405`, give `acme/widget` for both, and `git ls-remote
github.com/acme/widget` on Git 2.43.0 list the refs of a local bare repository
at that relative path and exit 0. By the same reading
`git@GitHub.com:acme/widget.git` and `https://GitHub.com/acme/widget` are
`not-github`, the host not being exactly `github.com`, while
`HTTPS://github.com/acme/widget` and `git://github.com/acme/widget.git` pass
step 2, the host being exact, and are `malformed-remote`, that function giving
no identity for either; the README's next steps say so.

The writer ran four forms on Git 2.43.0 on 2026-10-21 through a
`GIT_SSH_COMMAND` stand-in that logged its arguments and connected nowhere
(C-49). `ssh://git@github.com:acme/widget.git`, which the pattern alone gives as
`acme/widget`, has no port, `acme` not being digits, so its host is
`github.com:acme`, as Git's is: Git ran the stand-in on `git@github.com:acme`
for the path `/widget.git`. It is `not-github` at step 2 and is never sent; that
its reason is `not-github` and not `malformed-remote`, for a URL that names
`github.com`, is a residual, which the README's next steps do not name, and Git
cannot fetch it either. Git drops a `:` that nothing follows up to the `/`, so
that `ssh://git@github.com:/acme/widget.git` has the host `github.com`, and
keeps digits past 65535 in the host, so that
`ssh://git@github.com:99999/acme/widget.git` has the host `github.com:99999`
and no port. D3 reads the first host as `github.com:` and the second as
`github.com` with a port, so the first is `not-github` and the second
`malformed-remote`, and neither is sent. And step 1's reading of a user that
holds a `:` is deliberately conservative, not Git's: for the scp-like
`u:pw@github.com:acme/widget`, Git ran the stand-in on the host `u`, what stands
before the first `:`, for the path `pw@github.com:acme/widget`, while step 1
refuses that URL as `credential-bearing-remote` before any host is read; no
request is sent either way.

The writer ran four more forms the same way on Git 2.43.0 on 2026-10-21 (C-50).
Before a one-segment path, Git ran the stand-in for
`ssh://git@github.com:22/widget` on `git@github.com` with `-p 22`, and for
`ssh://git@github.com:99999/widget` on `git@github.com:99999` with no port, each
for the path `/widget`, while `remote_repository_identity()`, taken from
`project` at `961c405`, gave `22/widget` and `99999/widget`; step 3 refuses both
by their port before that function runs, so neither is sent. For the signed port
of `ssh://git@github.com:+22/acme/widget.git`, Git ran the stand-in on
`git@github.com` with `-p +22`, while D3, `+22` not being digits alone, reads
the host `github.com:+22`; and for the bracketed host of
`ssh://git@[github.com]/acme/widget.git`, Git, dropping the brackets, ran it on
`git@github.com`, while D3 reads the host `[github.com]`. Both are `not-github`
at step 2 and never sent: each fails closed. Lane openRepoProject-3's property
check in its confirm read of round C14 generated 3,619 URLs, applied D3 as
worded here, with the port refused at step 3, and ran Git 2.43.0 through such a
stand-in for each of the 30 that D3 would send: Git ran each on the host
`github.com`, with no port, for the same `owner/repository`.

What passes is `owner/repository`, the only part of the URL kept. The dedupe
key compares it without case. No reason carries the URL, and nothing of the
URL is logged. The user information is tested only by steps 1 and 3, for its
presence, for a `:` and for a user other than `git`, and it is dropped with
the URL once the judgement is made, whatever its outcome; the comparison with
`git` is part of deriving the identity, never made after it (C-30). "Remotes
that give no request" checks that no output, argv or message holds the user
part on its own, beside the password and the whole URL (C-32); that part is
`u9zq-kx7w`, a token no path, user or test name plausibly holds, so that a
run under a directory or user name that a common name would match cannot fail
the check (C-33).

### D4. The query set, the keys and their order

A worktree row is queried when `branch` is not `"detached"` and differs from
`merge_target.name`, `head` is known, and `merged_into_target` is `false`; a
null `merged_into_target`, as when no merge target resolved, is not `false`.
The upstream's state plays no part, so a `remote-gone` row is asked by its
head (C-6; Copilot 3989411854).

Keys are `(github.com, lowercased owner/repository, head)`. They are
collected in canonical order, repositories by rank (APO design.md, D6) and
then rows in row order (main worktree first, then path bytes), each key at
its first appearance. The first 64 are sent; the rest are `request-cap`,
unless the run-wide `unavailable` of D5 and D6 applies: with no `gh` found, or a
lookup that fails, as it does for a relative `GH_CONFIG_DIR`, `XDG_CONFIG_HOME`
or `HOME` (D5; C-44), or when each of the 64 requests sent exits 4 with nothing
on standard output (D6), they are `gh-unavailable` or `gh-unauthenticated`, as
every other key is (C-25). A lookup that the deadline cuts is no such case, and
leaves them `request-cap` (D1; lane openRepoProject-3's folded read, L4; C-34).
The cap decides before any request whether a key is sent, so a key past the
64th stays `request-cap` when the remote budget or the deadline expires, and
only keys within the cap are `cancelled` or `aborted` (D7; C-28).
`requests.estimated` is the number of distinct keys. Rows sharing a
key share the response, and each row is matched against it with its own
repository's base branch (D6), since two clones of one repository can have
different merge targets.

### D5. The request

One `gh` child per key:

    gh api --hostname github.com --include graphql \
      -f query=<Q> -f owner=<owner> -f name=<repository> -f oid=<head>

never with `--paginate`, `--slurp`, `--cache` or `--method`, and with `gh` the
absolute path that the lookup below found, never the bare name (C-22).
`<owner>` and `<repository>` passed D3's pattern, and `<head>` is 40 or 64
lowercase hexadecimal digits, checked before the argv is built; `-f` passes
each as a GraphQL variable, so no data enters the query text. `<Q>` is a
constant:

    query($owner: String!, $name: String!, $oid: GitObjectID!) {
      repository(owner: $owner, name: $name) {
        nameWithOwner
        object(oid: $oid) {
          ... on Commit {
            associatedPullRequests(first: 100) {
              pageInfo { hasNextPage }
              nodes {
                number state url headRefOid baseRefName
                baseRepository { nameWithOwner }
              }
            }
          }
        }
      }
    }

`nameWithOwner` names the repository GitHub resolved for `owner` and `name`,
which D6 matches each pull request's base repository against (C-19). GraphQL
carries a query in an HTTP POST; `<Q>` holds no `mutation`, and a test pins
the argv's query to the constant.

The child starts with `start_new_session=True`, never `preexec_fn` (change 1's
C4), standard input from `/dev/null`, working directory `/`, and standard
output and standard error read as bytes by the loop. Its environment is the
caller's, less `GH_DEBUG`, `DEBUG`, `GH_HOST`, `GH_REPO`, `GH_FORCE_TTY` and
`CLICOLOR_FORCE`, plus `GH_PROMPT_DISABLED=1`, `GH_NO_UPDATE_NOTIFIER=1`,
`GH_NO_EXTENSION_UPDATE_NOTIFIER=1`, `GH_TELEMETRY=false` and `NO_COLOR=1`.
`GH_TOKEN`, `GITHUB_TOKEN` and the proxy variables pass unread: that is gh's
own authentication path (DI:1056-1057). `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` and
`HOME` hold no credential value and are read only for the test below (C-44);
every variable a child gets passes unchanged. The two update
notifier switches keep `gh` from its update check, once every 24 hours by its
own help text, and from the state it writes for it, as far as gh documents
them; "Overview is local and read-only" binds `project` and its Git children,
and gh's behaviour beyond its switches is the client's; the fake `gh` of D11
records the values, and that block's new scenario asserts them. [E]'s Git scrub
does not apply; this is not a Git child. So the caller's `GIT_TRACE` and its
other `GIT_TRACE*` names reach a `gh` child unread, with every other variable:
feature 005's Q9 B (PR #19 at `423a532`, C-50), which reaches [E]'s scrub of Git
children, does not extend to `gh` children, and this is recorded as a residual,
as tested (lane openRepoProject-4's call 4 on C-48, 2026-10-21). `gh` 2.96.0,
run offline on 2026-10-21 with D5's flags, switches and query, from `/`, with a
fake token, its proxy at a closed local port, its configuration, state, cache
and data directories empty, `GIT_TRACE`, `GIT_TRACE2` and `GIT_TRACE2_EVENT`
naming files and a fake `git` first on `PATH`, exited 1 on the refused
connection with nothing on standard output, started no `git`, created no trace
file and wrote no file. The path of a 200 answer is not verified. If Brett Heap
wants the residual closed, it is one clause in D5 at ratification, removing
those names beside `GH_DEBUG` and `DEBUG`.

The child starts in `/`, which re-anchors every relative path in its
environment. So the lookup of `gh` counts as failing when any of
`GH_CONFIG_DIR`, `XDG_CONFIG_HOME` and `HOME` is set to a non-empty value whose
first byte is not `/` (C-44). Those are the three that `gh help environment`
names for the configuration directory (`GH_CONFIG_DIR`, else
`$XDG_CONFIG_HOME/gh`, else on Windows only `$AppData/GitHub CLI`, else
`$HOME/.config/gh`), and `gh`, started in `/`, resolves a relative one against
`/` and not against the caller's working directory. Normally that names no
configuration; but if the resolved path exists, `gh` reads the configuration
there, and a tree under `/` that any local user can write, such as `tmp`,
`var/tmp` or `dev/shm`, would let another user plant one, which can capture the
token `gh` sends (the lead's check, below). A failed lookup gives what one
already gives, below: every keyed row, whether or not its key is past the 64th,
is `unavailable` with reason `gh-unavailable`, and no child starts. The reason
stays `gh-unavailable`, which already covers more than one cause: a distinct
reason would cost an enum value for a cause that the README's next step makes
discoverable.

The test is made on the raw bytes of each value, by design: ` /x`, `~/x` and `.`
are all refused, and so is a value whose first byte is any byte other than `/`,
a non-ASCII byte included, while a value that is `/` alone is not. It does not
follow `gh`'s order of precedence and holds whichever of the three `gh` would
use, so a relative `XDG_CONFIG_HOME` or `HOME` beside an absolute
`GH_CONFIG_DIR` is refused too: that over-refusal is deliberate, fail-safe, and
independent of `gh` keeping its order. An empty or unset value is not refused.
`gh` treats an empty `GH_CONFIG_DIR` or `XDG_CONFIG_HOME` as unset, and when all
three are empty or unset it reads `.config/gh` from its working directory, here
`/.config/gh`, which only root can create on a normal system. The test needs no
filesystem call and is the lookup's first step, before the search of `PATH`, so
that a refused value gives `gh-unavailable` whether or not a `gh` lies on
`PATH`. The three hold no credential value: the overview reads them only for
this test, opens nothing they name, and never prints, logs or compares them
otherwise, and every variable a child gets, these three included, is passed
unchanged, as the Requests paragraph of `specs/project-overview/spec.md` says,
lane openRepoProject-4 having agreed "unchanged" for "unread" there on
2026-10-21 (`2b89bfc`). A prototype of the test, written once on `os.environb`
and once on `os.environ` (a `startswith` of `/` on the string, whose decoding
leaves a first byte that is not UTF-8 as no `/`), agreed with the rule on 18
cases on Python 3.10.21, 3.11.16, 3.12.3, 3.13.15 and 3.14.7: each of the three
alone and relative, a relative `XDG_CONFIG_HOME` or `HOME` beside an absolute
`GH_CONFIG_DIR`, ` /x`, `~/x`, `.`, a first byte of FF and one of EF, which are
refused, and `/` alone, empty, unset and all three absolute, which are not.

Two texts that land before this change refuse a relative `HOME` or
`XDG_CONFIG_HOME` before any child starts, so that such a run has no lookup and
no row to be `gh-unavailable` (C-58, the lead's ruling on reader RH's M4 and the
alignment reader AL1's conflict C1). Change 1's evidence model, on draft PR
#19's text at `f0bf538` (`PR19/cmd:116-128`, LQ-15 there), tests `HOME` and
`XDG_CONFIG_HOME`, and `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`, before any
Git child, `git --version` included, and where one is relative the subcommand
starts no Git child and inspects no repository (`relative-config-path`). Change
2's `Overview exits by completeness and severity`, as amendment A1 words it
(ratified by Brett Heap; `add-project-overview/specs/project-overview/spec.md`
:868-876 at `e4a30fc`), refuses the overview for the same two variables, with
that code and status 2. This change's own bases hold neither: its block of the
evidence model is PR #19's text at `c462d87`, change 2 at `961c405` has no such
refusal, and neither defines `relative-config-path`. So the spec keeps C-44's
rule whole for `GH_CONFIG_DIR`, which neither text tests, and states it for
`XDG_CONFIG_HOME` and `HOME` only in a run that neither requirement refuses
before any child starts; the AND on "No gh, or a gh without authentication"
says the same for those two cases and keeps "no `gh` child starts" on every
base, and adds no scenario, so the counts stay 36 and 10. AL1's proposed edit,
which has those two cases exit 2 with `relative-config-path`, is not taken: it
names a code that this change's own base does not define. D4, D11, Risks and
the rest of this decision state C-44's refusal for all three variables without
that condition; they are read with this paragraph, and are re-aligned, with
A1's other places, when this change's blocks are re-read against the archived
texts (task 2.3).

The evidence was observed offline on `gh` 2.96.0 on 2026-10-20 with fake tokens,
and none of it is a test of this change. The lead's check, with the token
variables unset and D5's five switches set, found that a configuration directory
whose `config.yml` held `http_unix_socket` made `gh api` send its request as
plain HTTP over that socket, with no TLS handshake and the token in the clear,
and exit 1 when the server closed: a configuration that someone else can write
can capture the token `gh` sends and serve the answer. Lane openRepoProject-4's
check, with `env -i` plus D5's five switches and `gh auth token -h github.com`,
found that an empty `HOME` makes `gh` read `./.config/gh` relative to its own
working directory, which found a planted token from the caller's directory and
none from `/`; that `gh` treats an empty `GH_CONFIG_DIR` or `XDG_CONFIG_HOME` as
unset, from either directory, and falls through to `HOME`; and that `gh` writes
to the configuration directory it uses on first use, rewriting `hosts.yml` into
its multi-account form and creating `config.yml`, so that a configuration
directory anchored to the working directory would let a scanned repository both
supply `gh`'s configuration and receive what `gh` writes.

Lane openRepoProject-4's check of extensions, on `gh` 2.96.0 on 2026-10-20 with
a fake token, asked whether a relative `HOME` beside an absolute
`GH_CONFIG_DIR`, which the rule refuses, can do harm through `gh`'s data
directory, where extensions live. Run in `/` under a relative `HOME`, `gh`
listed planted `gh-api` and `gh-zzz` extensions and ran `gh zzz` by its own
name, but `gh api --help` and a `gh api` request ran `gh`'s own command and
client, not the planted `gh-api`, and `gh` wrote no file under that `HOME`. So
D5's argv, which always begins with `api`, never runs an extension, and the
rule's refusal of that case is deliberate over-refusal, not a fix for a
demonstrated hole.

The writer ran `gh` 2.96.0 too on 2026-10-20, offline, with a fake token in each
probe configuration file, `GH_TOKEN`, `GITHUB_TOKEN`, `GH_ENTERPRISE_TOKEN` and
`GITHUB_ENTERPRISE_TOKEN` unset under `env -i`, `GH_NO_UPDATE_NOTIFIER=1`,
`GH_PROMPT_DISABLED=1` and `GH_TELEMETRY=false` set, and `gh auth token
--hostname github.com`, printing only whether the probe token was found: a
relative `GH_CONFIG_DIR`, a relative `XDG_CONFIG_HOME` and a relative `HOME`
were each found when run in the directory they were relative to and missed when
run in `/`, each of the same three values made absolute was found when run in
`/`, and with no variable naming the probe none was found; an empty `HOME` with
a probe file at `./.config/gh` was found from the directory that held it and
missed from `/`; and an empty `GH_CONFIG_DIR`, or an empty `XDG_CONFIG_HOME`,
with an absolute `HOME` that held the probe, was found from either directory. A
second run of the same kind in round C11, with all three variables unset and
then with all three empty, found the probe at `./.config/gh` from the directory
that held it and missed it from `/`, where no `/.config` exists. Those runs did
not record `gh api`'s output under D5's argv (task 2.5).

`gh` is looked up once per run, by one bounded filesystem task as [B]
requires of every filesystem call, in the absolute directories of `PATH`
only: an empty or relative entry, which names the caller's working directory
or a path under it, is skipped, and each child is started by the absolute
path found (C-22). When none is found, every keyed row is `gh-unavailable`
and no child starts. The council's adversary-engineer showed both risks
offline on 2026-10-20: with a trailing colon in `PATH`, `shutil.which` found
a `gh` planted in the caller's directory, which, started by its absolute
path, received the caller's `GH_TOKEN`; and with `.` in `PATH` the lookup
returned the relative `./gh`, which raised `FileNotFoundError` when started
in `/`.

Inside that lookup a directory where `gh` is absent is skipped, as POSIX
`execvp`'s search and a shell's own search skip it: ENOENT, ENOTDIR or EACCES
on the directory or on its `gh` entry, or an entry that is not a regular file
with execute permission. So the `gh` found is the one the person's shell
would run, and a `PATH` that names directories that do not exist, as many
do, does not turn every `--remote` run into `gh-unavailable`. Any other
error from a directory or its entry, such as EIO, ELOOP or ESTALE, fails the
lookup, which then gives what one that fails gives, below. Skipping such a
directory could run a later `gh` that one of the searches would not pick, so
the lookup skips only what every search checked skips, and an error that not
every search was seen to skip fails it. Checked on 2026-10-20 by injecting
twelve errors, one at a time, into the first `execve` that glibc 2.39's `execvp`
made for `gh`, with a second `gh` later on `PATH`: it stopped on ELOOP, EIO,
ENAMETOOLONG, ENOMEM and E2BIG, and went on past ENOENT, EACCES, ENOTDIR,
ESTALE, ENODEV and ETIMEDOUT; for ENOEXEC it ran the first `gh` through its `sh`
fallback, which is no stop. The lookup never executes an entry, so it has no
ENOEXEC to meet: an entry that is a regular file with execute permission is
found, and whether it then runs is the child's matter, never the lookup's. Lane
openRepoProject-3 reproduced the shells on 2026-10-20, in its confirm read of
round C6c, as a user other than root: with `PATH=d1:d2` and the real `gh` in d2,
bash 5.2.21, zsh 5.9 and dash 0.5.12 each ran d2's `gh`, as glibc's `execvp`
did, past a mode-000 directory (EACCES), a regular file where the entry's
directory should be (ENOTDIR), a dangling symbolic link `gh` and a missing
directory (ENOENT), and past a `gh` that is a directory or a regular file
without execute permission, so that the skips of ENOENT, ENOTDIR and EACCES rest
on those runs and no longer on POSIX alone. For ELOOP, each shell skipped a `gh`
that is a symbolic link to itself and went on to the later one, where glibc
stops. The shells were not run on the other errors that fail the lookup, so
ESTALE, ENODEV and ETIMEDOUT, which glibc goes on past, are not known to be
skipped by every search, and fail the lookup with the rest. The 5 s limit and
the deadline stay the only cuts of the lookup as a whole, and the spec's "finds
none, fails, or reaches its 5 s limit" speaks of the lookup as a whole, so this
per-directory rule fills D5 and is no change to the spec (C-35; its rationale
reworded to what was observed, C-36, and its record of the twelve errors and of
the shells completed, C-38).

A lookup that fails, on the test of the three configuration variables above or
on an error from a `PATH` directory, or that reaches its 5 s limit, as on an
unreachable `PATH` directory, gives what one that finds none gives: every keyed
row, whether or not its key is past the 64th, is `gh-unavailable`, and no child
starts (C-25, C-26, C-44). [B]'s bounded-task rule would otherwise record
`probe-timeout`; [B]'s added paragraph and [R]'s isolation clause record the
lookup's failure or cut only in the rows' `remote`, never as a row or scan
error (D10). A lookup that the deadline stops before its 5 s end leaves its
rows as an expiry does (D7), `cancelled` within the cap and `request-cap` past
it (C-28), just as [B] tells `deadline-exceeded` from `probe-timeout` and D7
tells `aborted` from `timeout`. The README's next step for `gh-unavailable`
names all three causes: install `gh`, check that `PATH`'s directories are
reachable, or make a relative `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` or `HOME`
absolute, so that a person with a relative `HOME` does not go looking for `gh`
on `PATH` (C-26, C-44); its next step for `gh-unauthenticated` is `gh auth
login` alone.

Rejected: REST `commits/{sha}/pulls` (an unknown commit is HTTP 422, an
`unknown` under DI:1055-1056, and a further page shows only in a `Link`
header); `gh pr list` (by branch name, page information hidden, 30 items by
default); direct HTTPS from `project` (`proposal.md`, Open Questions 2); and
anchoring a relative `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` or `HOME` to the
caller's working directory, which would have the overview rewrite variables that
the spec passes on and, for an empty one, let a scanned repository supply `gh`'s
configuration and receive what `gh` writes (C-41, C-44; the checks above).

### D6. Reading a response

With `--include`, standard output is the status line, the header lines, a
blank line and the body. The loop reads at most 64 KiB and one byte of status
and headers, keeping at most 64 KiB, and at most 1 MiB and one byte of body,
keeping at most 1 MiB: the one byte past each bound tells a part of exactly
that size, which is read whole, from a longer one (C-27). Status and headers
longer than 64 KiB make the key `api-error`; at the byte past 1 MiB of body
the loop stops reading, stops the child (D7) and records `truncated`.

- Exit 4 with nothing on standard output: `gh-unauthenticated`; when each of
  the 64 requests sent ends so, the keys past the 64th are `gh-unauthenticated`
  too, never `request-cap` (D4; C-25).
- A child the loop stopped at its limit, at the remote budget's end or at the
  deadline: `timeout` or `aborted` (D7); one stopped for a body past 1 MiB is
  `truncated`, and one whose status and headers passed 64 KiB is `api-error`.
- Otherwise the status line decides, whatever the exit status, since `gh`
  exits 1 on HTTP errors and on GraphQL errors: 401 gives `unauthorized`; 429,
  or 403 with `X-RateLimit-Remaining: 0` or a `Retry-After` header, gives
  `rate-limited`; any other 403 gives `forbidden`; any status but 200, or no
  status line, gives `api-error`. Header names compare without case, as HTTP
  defines them: `gh` prints them in its own form, which task 2.5 records, and
  Go, in which `gh` is written, canonicalises `X-RateLimit-Remaining` as
  `X-Ratelimit-Remaining` (S-2, not observed here; C-19).
- A 200 body must be UTF-8 JSON, and a body that cannot be decoded or parsed,
  for any cause, is `api-error`: the parse catches every exception it raises,
  not only `JSONDecodeError`, so no such body reaches C-14's exit 2 (C-22).
  The parse decodes the body's bytes itself, with Python's UTF-8 codec
  (`bytes.decode("utf-8")`) and its default `strict` error handler, and passes
  `json.loads` that string, never the bytes (C-40). Given bytes, `json.loads`
  picks the encoding itself, detecting UTF-8, UTF-16 and UTF-32, and decodes
  with the `surrogatepass` error handler, so a body that is not UTF-8 would
  parse. Checked on 2026-10-20 on Python 3.10.21, 3.11.16, 3.12.3, 3.13.15 and
  3.14.7, on each of which `json.loads` of bytes parsed a JSON body encoded in
  UTF-16 and in UTF-32, each little-endian, big-endian and with a byte order
  mark; a body with a string that held the bytes ED A0 80, an encoded surrogate;
  and a body that began with a UTF-8 byte order mark. The strict decode raised
  `UnicodeDecodeError` for the UTF-16 and UTF-32 bodies with a byte order mark
  and for ED A0 80, and accepted the other four UTF-16 and UTF-32 bodies, whose
  NUL bytes are valid UTF-8, which `json.loads` of the string then refused with
  `JSONDecodeError`, as it did the UTF-8 byte order mark ("Unexpected UTF-8
  BOM"); each such body is `api-error` by the rule above. RFC 8259 section 8.1
  requires UTF-8 for JSON exchanged outside a closed ecosystem, and lets a
  parser treat a byte order mark as an error, which one at the start of a body
  is here. A JSON escape of a lone surrogate, a backslash, `u` and D800, six
  ASCII characters, is another matter: it is ASCII, valid UTF-8 JSON, and
  parses, and C-40, which concerns the body's bytes and not its strings, leaves
  it. No field the row keeps can hold one: `state`, `number`, `url` and
  `head_sha` are closed forms (below and D9), and the two open fields,
  `baseRefName` and `errors[].type`, are compared and never kept (C-43). The
  parse passes `json.loads` a `parse_int` hook, which receives the text of each
  integer literal of the body, wherever it stands, and raises before converting
  it when the text has more than 10 digits, a sign not counted.
  GraphQL's `Int`, which `number` is, is a signed 32-bit integer, at most
  2,147,483,647, which has 10 digits. The parse then fails, and the key is
  `api-error` by the rule above, whatever the interpreter's own limit on
  converting a string to an integer; and the cost of converting an integer
  literal within the 1 MiB body is bounded, on interpreters where it is
  quadratic (C-37). The evidence: the council's adversary-engineer measured
  two failures that are not `JSONDecodeError` on Python 3.12.3 on 2026-10-20,
  a body under 1 MiB nested in `[`, which raised `RecursionError`, and a
  `number` of 5,000 digits, which raised a plain `ValueError` ("Exceeds the
  limit (4300 digits) for integer string conversion"). That is Python's
  integer-string conversion length limit, added in 3.11 as a mitigation for
  CVE-2020-10735 and backported to 3.10.7, as Python's documentation states (its
  standard types page and its 3.10 changelog, gh-95778, read on 2026-10-20),
  while AGENTS.md says Python 3.10+, and CI's Python 3.10 was not checked.
  Python 3.10.0 to 3.10.6, which have no such limit, were not run here, only
  emulated with `sys.set_int_max_str_digits(0)`; so the limit is no mechanism of
  this rule, and on those versions that body would parse without the hook.
  Checked on 2026-10-20 on Python 3.10.21, 3.11.16, 3.12.3, 3.13.15 and
  3.15.0rc2: `json.loads` calls
  the hook with each integer literal's text, its sign included, and with no
  float or string, and an exception raised there leaves `json.loads` as
  raised, never wrapped in `JSONDecodeError`; with
  `sys.set_int_max_str_digits(0)`, which emulates 3.10.0 to 3.10.6, a plain
  `json.loads` of the 5,000-digit body returns, and with the hook it raises;
  and with that setting a literal of 1,000,000 digits took 5.2 s to convert
  on 3.10.21 and 4.5 s on 3.11.16, about 0.6 s on 3.12.3 and later, and under
  3 ms for the hook to reject.
  The parse also passes `json.loads` a `parse_constant` hook that raises for
  every text it is given (C-39). By default `json.loads` accepts `NaN`,
  `Infinity` and `-Infinity` and returns `nan` and `inf`, though RFC 8259
  section 6 permits no numeric value that its grammar cannot represent, such as
  those; a body that holds one in a field the parse never reads, as the
  `extensions` object of a GraphQL response may, would parse, and its key could
  be answered. With the hook such a body fails the parse, wherever the constant
  stands, and its key is `api-error` by the rule above, on every supported
  Python. Checked on Python 3.10.21, 3.11.16, 3.12.3, 3.13.15 and 3.14.7:
  `json.loads` called the hook with exactly `NaN`, `Infinity` and `-Infinity`;
  an exception raised there left `json.loads` as raised, never wrapped in
  `JSONDecodeError`; the hook was not called for a string (the strings "NaN" and
  "Infinity" included), `true`,
  `false`, `null` or a number, `1e999` (which parses as `inf`) included; `NaNx`
  called it on its `NaN` prefix; and `nan`, `-NaN`, `infinity`, `+Infinity` and
  `Inf` failed `json.loads` itself with `JSONDecodeError`. A float literal needs
  no bound: no field the parse reads may hold a float, since `number` is checked
  by type (C-42), and a literal of 1,048,560 bytes, in its fraction, its integer
  part or before an exponent, parsed in under 10 ms on each interpreter, the
  slowest 9.8 ms (3.10.21, its fraction; worst of seven runs). There is no
  `parse_float` hook, by decision: a float literal outside the range of a
  double, such as `1e999` or `-1e999`, is grammatical JSON, since RFC 8259
  section 6 leaves range to the implementation, unlike `NaN`, `Infinity` and
  `-Infinity`, and parses as `inf` or `-inf`; in a field the parse never reads
  the key is still answered, and as a node's `number` it fails the type check
  below (C-43). A prototype of D6's parse and of the node checks its fixtures
  need, run on Python 3.10.21, 3.11.16, 3.12.3, 3.13.15 and 3.14.7, answered
  `merged` for each of these bodies when `json.loads` was given its bytes with
  the `parse_int` hook alone, and `api-error` under this parse: a valid answer
  with `NaN`, `Infinity` or `-Infinity` as the value of a key of its
  `extensions` object; that answer in
  each of the six UTF-16 and UTF-32 forms above; and that answer with ED A0 80
  in a string of its `extensions` object, or with a UTF-8 byte order mark before
  it. The answer in plain UTF-8 was `merged` under both.
  An `errors` entry of type `RATE_LIMITED` gives
  `rate-limited`, and any other `errors` entry, a null
  `data.repository`, or a `data.repository.nameWithOwner` that fails D3's
  pattern (the field S-2 adds and C-19 takes, validated as each node's
  `baseRepository.nameWithOwner` is), gives `api-error`. A null
  `data.repository.object` gives `not-found`: GitHub holds no such commit.
  Otherwise `associatedPullRequests` must hold a boolean
  `pageInfo.hasNextPage`, which when true gives `further-page`, and a list of
  at most 100 `nodes`, more being `api-error` (AE-5's suggested text, taken by
  C-22).
- Each node must have a `number` whose parsed type is exactly `int`
  (`type(number) is int`): never a `bool`, so not `true` or `false`, and never a
  `float`, so not `1.0` or `1e999`. The spec already says "a positive integer
  `number`" (`specs/project-overview/spec.md:479`), and C-42 reads that as a
  JSON integer literal. It must also be at least 1 and at most 2,147,483,647,
  the largest GraphQL `Int` (the hook above bounds the literal's text, this
  bounds its value, C-37); a `state` of `OPEN`, `CLOSED` or `MERGED`; a
  `headRefOid` of 40 or 64 hexadecimal digits; a string `baseRefName`; a
  `baseRepository.nameWithOwner` that passes D3's pattern; and a `url`
  exactly `https://github.com/` plus that `nameWithOwner`, `/pull/` and the
  number. One invalid node makes the whole key `api-error`, never a partial
  answer. Every check this section makes on the parsed answer, these included,
  runs inside the same catch-everything boundary as the parse, so a check that
  raises, an `OverflowError` for instance, is `api-error` too, never an
  exception that reaches C-14's exit 2 (C-42). A prototype of the checks on
  `number`, run on Python 3.10.21, 3.11.16, 3.12.3, 3.13.15 and 3.14.7, answered
  `api-error` for a `number` of `true`, `false`, `1.0`, `1e999` and
  2,147,483,648, each with a `url` that a check by value would accept, and
  `merged` for 2,147,483,647 and for 7; a check written
  `isinstance(number, int)` answered `merged` for `true`, and one written
  `number == int(number)` answered `merged` for `true` and for `1.0` and,
  outside the boundary, raised `OverflowError` on `1e999`, which would exit 2
  (D10); and `1e999` and `-1e999`, and an escape of a lone surrogate, in a field
  the parse never reads gave `merged` (C-42, C-43).

Per row: the nodes whose `headRefOid` equals the row's `head`, whose
`baseRefName` equals the row's merge ref less `refs/heads/`, and whose
`baseRepository.nameWithOwner` equals, without case, the answer's
`data.repository.nameWithOwner`, the repository GitHub resolved for the
identity: the identity itself unless the repository was renamed or
transferred, when a remote URL that still names the old name gets its real
answer instead of `not-found` on every row, which task 2.5 checks if a
renamed repository is at hand (C-19). A `MERGED` node wins over an `OPEN`
one, a `CLOSED` node never matches (C-16; F-3 found that the association
returns none), and the highest `number` wins within a state; none gives
`not-found`. The row keeps `state`, `number`,
`url` and `head_sha`; nothing else of the body is kept, and standard error is
drained, capped and discarded.

### D7. Limits, cancellation and the run bound

At most four `gh` children run at once. Each child's limit ends at `min(its
start + 5 s, the remote budget's end)`. This is the shorter limit that [E]'s
Budgets paragraph, as this change modifies it, gives a `gh` child in place of
15 s. At its limit the loop sends SIGTERM to its group, SIGKILL 2 s later, and
waits 2 s more for the reap before abandoning it, as [E] and [B] stop a Git
child; the key is `timeout` when the child's own 5 s ended first and `aborted`
when the budget or the deadline did.

When the remote budget ends or the deadline passes, no child starts; every
key within the cap not yet sent, and every row whose remote-target read never
started, is `cancelled`; every request in flight is stopped as above and
`aborted`; a key past the 64th stays `request-cap`, since the cap decided
before any request that it is never sent (D4; C-28); the run-wide
`unavailable` of D5 and D6 outranks both `cancelled` and `request-cap`
(C-25, C-28); and a remote-target read in flight is stopped and its rows
`remote-target-unread`.
None of these is a row error or a scan error, and none is [B]'s `probe-timeout`
or `deadline-exceeded` on a row: [B] and [E], as this change modifies them,
record them in the rows' `remote` (D2, D10). Everything starts inside the 60 s
deadline and the last stop adds at most 2 s + 2 s, so [B]'s 64 s bound holds;
rendering follows.

Each `gh` child enters the in-flight registry while SIGINT, SIGTERM and SIGHUP
are blocked, as a Git child does (APO design.md, D1, as D1 reads at `961c405`;
feature 005's Q16 may change it, and `tasks.md` 2.3 re-reads this sentence),
so a signal terminates and reaps it with the rest, and [X]'s exits 130, 143
and 129 hold with no result document. On every other exit path, C-14's exit 2
included, the loop kills every in-flight `gh` child's group, as [E] kills a
probe child's (lane openRepoProject-3's re-read, LOW-6).

No key stops another (`proposal.md`, Decisions): after a rate limit or an
exit 4, the remaining keys still run, each failing fast on its own, so which
rows hold which answer never depends on completion order.

### D8. The JSON fields

In a `--remote` run only:

- each queried worktree row gains `remote` after `classification`,
  `{state, number, url, head_sha, reason}` as [R] defines; a row outside the
  query set gains no key (L-10);
- the envelope gains `remote` after `scan_errors`: `host`, `observed_at` (RFC
  3339 UTC with `Z`, null when no request started), `freshness`, `limits`,
  `budget`, `requests` (the `gh` children, D5), `counts` (the five states as
  keys, each an integer, zeros included) and `completeness`; it has no
  `probes`, the remote-target reads being in the envelope's (D2).

`remote.limits.concurrency` reports the `gh` concurrency in force: 4 in every
run, and 1 only where an in-process test patches the concurrency to 1, as
change 2's `budget.probe_concurrency` reports the probe concurrency in force
(APO design.md, D6, where the JSON at probe concurrency 1 and 4 differs only in
timestamps and that field). So [R]'s determinism sentence and the AND at
concurrency 1 of "The request bounds" except it beside `remote.observed_at`, as
change 2's determinism sentence and its scenario except
`budget.probe_concurrency` (C-48's M3).

Without `--remote` both `remote` keys are absent, not null, so a document of a
run without `--remote` is exactly [J]'s, as [J], as this change modifies it,
states; in a `--remote` run a row outside the query set has no `remote` key
either, never a null one, since null means unknown or not established
(CAS/pc:1128-1129) and such a row was not asked. The envelope's `probes` gains
D2's reads in a `--remote` run only.

Integers are JSON integers and the `_seconds` fields integers, as [J]
requires. No existing key or enum changes, `probes` counts as [B], as
modified, states, and `schema_version` stays 1 (`proposal.md`, Decisions
C-9, Open Questions 1).

### D9. The human lines

The `remote` line takes [H]'s finding layout (APO design.md, D10): two spaces,
`remote` padded to 14 columns, then [R]'s fixed text, placed after the path
line of the worktree's first shown finding. Only the validated number is
printed, never a URL, a repository name taken from a response, or a reason
other than [R]'s codes, so every printed character is ASCII. After [H]'s
summary line a `--remote` run prints:

    Remote: N gh requests started; merged a, open b, not found c,
    unavailable d, unknown e. Remote evidence, where GitHub answered, was
    read live from github.com and may already be stale; it never authorizes
    cleanup.

as one line. Under `--attention` only shown findings' worktrees get a
`remote` line, and the summary's `Remote:` line always prints. The count is
of `gh` children started, which is all `project` knows: a `gh` without a
token is started, so `observed_at` is set, and exits 4 before it connects,
and the freshness sentence stays true in that run and in one that starts no
child (C-17). The `merged` text names the exact head and says that the
worktree's uncommitted and ignored files are not part of the pull request,
since a row kept for its files (`dirty`, `ignored-local-files`,
`inspection-error`) is queried like any other (C-20), and its remedy is a
local merge target brought up to date, since a fetch moves only the
remote-tracking ref (C-18).

### D10. Isolation from the local result

The remote phase starts after classification, findings, gates, suggestions,
summary counts and completeness are computed, and it writes only into the
`remote` slots and into the envelope's `probes`, which D2's remote-target reads
raise by the same number in `estimated` and in `performed` in an uncut remote
phase and by nothing else (C-47). Nothing it records is a row error, a scan
error or a finding, [B]'s added paragraph saying so for its children that exit
nonzero or are stopped, for a lookup of `gh` that fails or does not finish in
time (C-26) and for a deadline that expires after collection has finished,
during the remote phase, which records no `deadline-exceeded` scan error, its
effects shown only in the `remote` fields and in `probes` (C-48's M1), and [R]'s
isolation clause for every failure, cut or stop of a remote-target read, of that
lookup or of a `gh` child, `probe-failed`, `probe-timeout` and
`deadline-exceeded` notwithstanding, so [X]'s exit status and [J]'s
`completeness` are what they are without `--remote`, unless the remote phase
raises an exception that [R] records as none of its reasons, which exits 2 as
[X] gives any exception outside the per-candidate boundary (a body that the
parser rejects, for any cause, is `api-error`, one of [R]'s reasons, never such
an exception: C-22), or a signal ends the run or a write to standard output
fails, the two other cases that [R]'s Isolation paragraph excepts (C-48's L4,
the second clause on lane openRepoProject-4's YES): a signal ends the run with
[X]'s exit status and no result document (D7), and a `--remote` document is
longer than the same run's without `--remote`, so that a reader that closes
early can fail the one write and not the other; and the envelope's `probes`
differs only by D2's reads. Nothing is written to disk or kept past the run,
`gh` never gets `--cache`, and `project clean` has neither the option nor a
reader of these fields, so remote evidence never reaches an eligibility gate, a
`plan_digest` or a revalidation (SY:129-130; DI:1059-1060).

### D11. Test seams and the scenario map

- A fake `gh`, a Python script that `write_fake()` puts in `fake_bin()`,
  reads its argv, takes the `oid` field, looks it up in a JSON answer table
  beside it, and writes a status line, headers, a blank line and a body, the
  status line and the header names in the forms that task 2.5 records `gh`
  printing (C-19); it writes the body as bytes, which the table gives as a
  text and an encoding or in hexadecimal digits (C-40). Per key the table can
  hold the child for N seconds, exit 4
  with no output, send exactly 1 MiB of body, answered from its nodes, or
  1 MiB and one byte, set `hasNextPage`, answer
  401, 403, 429, a 403 with `X-RateLimit-Remaining: 0` or with a
  `Retry-After` header, a 200 body with an `errors` entry of a given type, a
  null `data.repository`, a status and header block of exactly 64 KiB,
  answered as any other, or over 64 KiB, a body of 1 MiB of `[` or with a
  `number` of 5,000 digits (C-22), one whose `number` is `true`, `1.0` or
  `1e999` (C-42), one that carries `NaN`, `Infinity` or `-Infinity` in its
  `extensions` object (C-39), one written in UTF-16 or UTF-32, one that holds
  the bytes ED A0 80 in a string or one that begins with a UTF-8 byte order mark
  (C-40), or 502, give the
  queried repository's `nameWithOwner` as the owner and name asked or, to
  stand for a renamed repository, as another, as the last AND of "The chosen
  pull request and a rejected answer" does (lane openRepoProject-3's delta
  read, F4), or name pull requests with any head, base and state. It places
  each pull request only in the list GitHub returned it in, the association,
  in a state that task 2.5 recorded there;
  the `CLOSED` nodes of "The chosen pull request and a rejected answer" are
  the one exception, a defensive input that pins that such a node never
  matches (C-16, C-19). It appends two kinds of JSON line to a record file
  beside it, each written in one call on a descriptor opened for append, so that
  the records of concurrent children do not interleave (C-46). The start record
  is written the moment the child starts, before it answers or holds: the argv,
  the names of the environment variables set, the values of
  `GH_NO_UPDATE_NOTIFIER`, `GH_NO_EXTENSION_UPDATE_NOTIFIER`,
  `GH_PROMPT_DISABLED`, `GH_TELEMETRY` and `NO_COLOR`, whether each of
  `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` and `HOME` is set and its value (C-44),
  whether `GH_TOKEN` equals the caller's, the working directory, its pid and
  process group, and its start time. The end record is written when it exits on
  its own: its pid, its end time and its exit status. A child that the loop
  stops, at its limit, at the expiry or on a signal, is killed and writes no end
  record, so a record per run that held the end time would leave out just the
  children whose stops are tested. Their start records show that each started,
  in what order and when, and `os.killpg(pgid, 0)` raising `ProcessLookupError`
  on a recorded group shows that the loop reaped it, as change 2's signal test
  does for the groups its wrapper recorded (APO design.md, D13). The tests of
  "API failures stay unknown", "Expiry cancels queued and in-flight requests"
  and "A signal while requests run", and the test of [E]'s new scenario, read
  the start records and probe each recorded group so.
- One test sets the interpreter's limit on converting a string to an integer to
  0, with `sys.set_int_max_str_digits(0)` where the interpreter has it, and
  restores it after; that emulates Python 3.10.0 to 3.10.6, which have no such
  limit (D6) and were not run here (C-37, C-38). With the limit at 0 the body
  whose `number` has 5,000 digits still gives `api-error` for its key's rows,
  and the hook, called on that literal's text with the conversion it would
  otherwise make replaced by a stand-in that fails the test if called, raises,
  which shows that the hook rejects the literal before converting it. The same
  test passes the hook `2147483647` and `-2147483648`, which it accepts, and an
  11-digit text, which it rejects, and serves two values of `number`, each of 10
  digits, which pass the hook: 2,147,483,647, which passes the node check too
  and gives its row, a matched pull request with that number and not
  `api-error`, so that the node check's `<=` edge is pinned and a check written
  `<` fails the test (C-38); and 2,147,483,648, whose key is `api-error` by the
  node check. The same test serves `true`, `1.0` and `1e999` as `number`, which
  the hook never sees, each with a `url` ending `/pull/1`, which a check by
  value accepts for `true` and `1.0`, so that the type is the only fault, and
  each gives `api-error` for its key's rows (C-42): a check written
  `isinstance(number, int)` gives `merged` for `true`, and one written
  `number == int(number)` gives `merged` for `true` and for `1.0` and, outside
  the parse's boundary, raises `OverflowError` on `1e999`, which would exit 2
  (D10), so each by-value writing fails the test. It tests the parse and the
  node checks and is no scenario: "API failures stay unknown" already requires
  the 5,000-digit outcome, and the added requirement's "a positive integer
  `number`" (`specs/project-overview/spec.md:479`) the others.
- One test serves 200 answers that D6's parse refuses though each is otherwise
  valid (C-39, C-40). Each is a matched, merged pull request that would give
  its key's rows `merged` if it parsed, and each gives `api-error` with D6's
  parse: the answer with `NaN`, `Infinity` or `-Infinity` as the value of a key
  of an `extensions` object that the parse never reads (three fixtures); the
  answer encoded in UTF-16 and in UTF-32, each little-endian without a byte
  order mark and with one (four, chosen from D6's six forms: little-endian,
  without and with a byte order mark, for each of the two encodings); the answer
  with the bytes ED A0 80 in a string of that object (one); and the answer with
  a UTF-8 byte order mark before its first byte (one). The same answer in plain
  UTF-8 is served too and gives `merged`, so that each failure comes from the
  rule and from no other
  fault of the answer. The test checks the parse and is no scenario: the added
  requirement's "A 200 body SHALL be UTF-8 JSON"
  (`specs/project-overview/spec.md:474-475`), and its `api-error` for a
  response "that cannot be decoded or parsed for any cause" (:466-467),
  already require each outcome.
- A planted `gh`, a second fake that records each run, sits in the working
  directory of a run whose `PATH` begins with an empty entry and `.`, so that
  "No gh, or a gh without authentication" shows it never runs, and the fake
  `gh`'s recorded argv shows the absolute path each child was started by
  (C-22; lane openRepoProject-3's delta read, F3). For the same scenario the
  lookup's filesystem task takes the injected slow call that change 2's
  design patches into its filesystem tasks (APO design.md, D13), on a chosen
  `PATH` directory, so that the lookup is cut at 5 s (C-26).
- One test pins C-44's rule, with the fake `gh` first on `PATH` and two queried
  rows with distinct heads, each case its own run that changes only the three
  variables, the rest of the caller's environment being the same:
  - Refused: `GH_CONFIG_DIR=.gh-config`; `XDG_CONFIG_HOME=cfg`; `HOME=h`; a
    relative `XDG_CONFIG_HOME` or `HOME` beside an absolute `GH_CONFIG_DIR`,
    since the rule holds whichever of the three `gh` would use and does not
    depend on its order; each of the three relative beside the other two
    absolute; and, for `GH_CONFIG_DIR`, the values ` /x` (a leading space),
    `~/x` and `.`, since the test is on the raw bytes. Each gives both rows
    `unavailable` with reason `gh-unavailable`, `remote.requests.performed` 0,
    `remote.observed_at` null, no start record of the fake `gh` although it lies
    first on `PATH`, and the exit status and every local field those of the run
    without `--remote`.
  - Not refused: an absolute `GH_CONFIG_DIR`; an empty `GH_CONFIG_DIR`; an empty
    `XDG_CONFIG_HOME` and an empty `HOME`; all three unset; and all three
    absolute. Each starts the `gh` children, answers both rows, and has the fake
    `gh` record each of the three as set or unset and, when set, byte for byte
    as the caller set it, with `/` as the working directory: nothing is
    rewritten.
  - With 70 distinct keys and a relative `GH_CONFIG_DIR`, all 70 keys are
    `gh-unavailable`, none `request-cap`, as with no `gh` on `PATH`.
  - The AND of "No gh, or a gh without authentication" takes
    `GH_CONFIG_DIR=.gh-config`, `XDG_CONFIG_HOME=cfg`, a relative `HOME` beside
    an absolute `GH_CONFIG_DIR`, and the absolute and the empty `GH_CONFIG_DIR`;
    the relative `XDG_CONFIG_HOME` case is in it because lane openRepoProject-4
    asked, on 2026-10-21, that a test that leaves `XDG_CONFIG_HOME` out of the
    check fail. The rest of the cases test the sentence of the Requests
    paragraph and the Results paragraph's clause, which the scenario does not
    enumerate. A refused case starts no `gh` child, so no test runs a real `gh`
    for it; the checks of D5 are evidence and no test.
- Two `PATH` fixtures, built in the test's temporary tree, test the lookup's
  per-directory rule (C-35). A directory of mode 000 placed before the
  directory that holds the fake `gh` is skipped, and the lookup finds that
  `gh` (a mode does not bind a process running as root, so the test needs
  another user, or is skipped). A directory whose `gh` is a symbolic link to
  itself, an ELOOP, placed before it fails the lookup: every queried row that
  has a key is `gh-unavailable`, and the fake `gh` after it never runs.
  Neither is a scenario, since the spec's "fails" speaks of the lookup as a
  whole.
- The counting `git` wrapper of change 2's design (APO design.md, D13), which
  can hold a chosen argv, gains one fixture control: for a chosen argv in a
  chosen repository it exits with a given status and a fixed line on standard
  error, without running Git, or, for a chosen argv, ignores SIGTERM and holds
  past its budget. "A failed or held remote-target read stays unknown" uses it
  to make the first remote-target read exit 128 in one repository and to hold
  it past 10 s in another, and "The overview's remote-phase children" to hold
  one past its budget while it ignores SIGTERM; this extends the test file
  only, never change 2's text.
- One fixture pins D2's strict decode (C-43, C-45) and needs no control of the
  wrapper above: a repository whose merge target's `branch.<target>.merge` is
  `refs/heads/` followed by the byte 0x80, set with `git config`, so that the
  first remote-target read's output holds a byte that is not UTF-8. Its queried
  rows are `unknown` with reason `remote-target-unread`, no second read starts
  there and no request is made for its rows, as for a read that exits 128, while
  a second repository in the same run, whose merge ref is valid UTF-8, is
  answered as usual, so that the byte is the only fault. A `remote.<name>.url`
  that holds the byte is the same fixture for the second read. It is no
  scenario: `specs/project-overview/spec.md:392-393`'s "fails for any other
  cause" already requires the outcome (D2). The writer saw, in a scratch
  repository on Git 2.43.0, that `git config` took the byte, that `git
  for-each-ref` with D2's format and `git remote get-url` each printed it, and
  that `bytes.decode("utf-8")` of the first output raised `UnicodeDecodeError`
  ("invalid start byte").
- The bounded reader is unit-tested at N-1, N and N+1 bytes for each of its
  three bounds: the 1 MiB body, the 64 KiB of status and headers, and the
  64 KiB of a remote-target read's standard output. At N-1 and N the part is
  read whole and kept; at N+1 it is cut, giving `truncated`, `api-error` or a
  failed read, `remote-target-unread`. With the fake `gh`'s exact-size answers
  above, these pin the byte past each bound (C-27, C-29); they are tests only,
  and no scenario changes (lane openRepoProject-3's folded read, L2; C-34).
- The `PATH` and the environment of every run (C-46). No test needs `gh`
  installed, and some need it absent, which `question_env()`'s `PATH` cannot
  give where `gh` lies beside the tools it keeps. That `PATH` holds the fake bin
  directory and the directories of `bash`, `git` and the interpreter, and on
  `ubuntu-latest`, the one runner of CI (L-12), `gh` is installed at
  `/usr/bin/gh`, beside `/usr/bin/git`. So the three parts of "No gh, or a gh
  without authentication" and "The request bounds" that need no `gh` on `PATH`
  would find the runner's real `gh`, start it, and read `gh-unauthenticated` or
  `api-error` with 2 or 64 requests where the spec requires `gh-unavailable` and
  0, while on a bench that keeps `gh` apart from `git` the same tests pass. The
  layout is inferred, not run: from the image's `install-github-cli.sh`
  (actions/runner-images, `images/ubuntu/scripts/build/install-github-cli.sh`),
  whose `apt-get install` takes cli/cli's Linux `.deb`, and from cli/cli's
  `.goreleaser.yml`, whose `nfpms` entry has `bindir: /usr` and
  `binary: bin/gh`, both read by reader RC on 2026-10-21; no Actions run was
  made.
  - `PATH` holds the fake bin directory and one temporary directory, built in
    the test's own tree, of symbolic links to `git`, `bash` and the interpreter,
    and never the directories that those tools live in; the counting `git`
    wrapper above runs the real `git` by the absolute path of its link. The
    writer's simulation of the runner's layout, with `git`, `bash`, `gh` and an
    interpreter in one directory, on 2026-10-21: `question_env()`'s `PATH` found
    that `gh`, the directory of links found none, and `git`, `bash` and the
    interpreter each ran through its link, `git for-each-ref` on a scratch
    repository included, on Git 2.43.0.
  - A run that needs `gh` absent first asserts
    `assert_absent_from_path(env, "gh")` (tests:200), which fails the test when
    `shutil.which("gh", path=env["PATH"])` finds one, and a run that has the
    fake `gh` asserts `assert_fake_on_path(env, "gh")` (tests:196), so that a
    `gh` found anywhere else fails the test and not the product.
  - No real network: in-process runs install an audit hook that fails
    `socket.connect` (APO design.md, D13), which binds the test's interpreter
    and not its children. The `gh` children of an in-process run, as in the
    expiry scenario, the AND at concurrency 1 and the integer-limit test above,
    receive the environment that the overview passes on, which is the caller's
    (D5), and `os.environ` is the developer's own. So an in-process run replaces
    `os.environ` for its duration with the environment that a subprocess run
    gets, `self.env` (tests:133-134) with the `PATH` of the first sub-bullet
    above, the fake bin directory and the directory of links, in place of the
    developer's, and with the changes below, and restores it after, so that the
    lookup of `gh` reads that `PATH` (C-49); and that environment sets
    `HTTPS_PROXY` and `HTTP_PROXY` to a closed local port, as subprocess runs
    do, so that even a real `gh` reached by mistake could not connect.
  - That environment, which every subprocess run gets as well, removes
    `NO_PROXY` and `no_proxy`, either of which could exempt `github.com` from
    that proxy, and `GH_TOKEN` and `GITHUB_TOKEN`, setting a fake token only
    where a test asserts one, as the AND on `GH_TOKEN` in "The request bounds"
    does; and it fixes `GH_CONFIG_DIR` and `XDG_CONFIG_HOME` as absolute paths
    or leaves them unset, `HOME` being the absolute path of the test's own
    `home` already, so that a real `gh` reached by mistake would read no
    developer's token or configuration. C-44's test sets the three configuration
    variables on purpose, each case its own run: a refused case starts no child,
    and an accepted case has the fake `gh` first on `PATH`.
- Fixtures: a bare repository takes the pushes; the merge target's
  `branch.main.remote` names a second remote whose URL is a `github.com` URL
  that nothing contacts; a squash merge is made in a publisher clone with
  `git merge --squash`, pushed and fetched. That second remote is made with
  `git remote add`, which writes a default fetch refspec that maps
  `refs/heads/main`, and `branch.main.remote` and `branch.main.merge` are set
  with `git config`, since `git branch --set-upstream-to` needs the
  remote-tracking ref to exist; a remote made with
  `git config remote.<name>.url` alone has no fetch refspec, so that every row
  of the fixture would read `no-remote-target` (C-48's M2; reader RC's trap).
  One more fixture, a test and no scenario, gives a merge target's remote the
  fetch refspec `+refs/heads/develop:refs/remotes/<name>/develop` alone: its
  queried rows are `unavailable` with reason `no-remote-target` after one read,
  no second read starts and no request is made for them (C-48's M2).
- The expiry scenario patches the 30 s budget, the 5 s limit and the 60 s
  deadline down in-process, keeping their ratios, as change 2's design does
  for its deadline. The fixture of its first AND, in which collection leaves
  less than 30 s, is also run without `--remote`, and the two runs' scan errors,
  `completeness` and exit status are compared (C-48's M1). The case of a
  repository whose first remote-target read named a usable remote and whose
  second never started, `cancelled` under the Requests paragraph (C-48's L1),
  is not tested: D1 dispatches the reads in rank order, so a repository's second
  read takes the slot its first read freed, and a first read's budget ends at
  the deadline or before, so the case arises only when the deadline passes
  between the reaping of a first read and the dispatch of the second, an
  instant that none of these seams can place. If that race happens in the
  fixture of the second AND, its rows are `cancelled` like those of every other
  repository not in flight, so the AND's outcome is the same either way.
- Concurrency: in a run whose children end on their own, as in "The request
  bounds", the fake's start and end records show at most four overlapping
  children; a stopped child writes no end record, so the tests of stops read its
  start record and probe its group instead (C-46). The AND at concurrency 1 of
  "The request bounds" compares the `remote` fields of its two runs with
  `remote.observed_at` and `remote.limits.concurrency` apart, the second
  reporting 1 in the patched run and 4 in the other (D8; C-48's M3).

| Scenario | Requirement |
| --- | --- |
| [B]'s thirteen scenarios (kept) | MODIFIED [B] |
| Probe counts in a remote run | MODIFIED [B] |
| [J]'s six scenarios (kept) | MODIFIED [J] |
| The remote keys of a --remote run | MODIFIED [J] |
| Local and read-only (kept) | MODIFIED, local and read-only |
| A remote run stays read-only apart from its queries | MODIFIED, local and read-only |
| A squash-merged branch is explained and kept | [R] |
| A squash-merged branch whose upstream was deleted | [R] |
| The remote target comes from the merge target's branch configuration | [R] |
| One request per exact head | [R] |
| The chosen pull request and a rejected answer | [R] |
| Remotes that give no request | [R] |
| No gh, or a gh without authentication | [R] |
| API failures stay unknown | [R] |
| A failed or held remote-target read stays unknown | [R] |
| The request bounds | [R] |
| Expiry cancels queued and in-flight requests | [R] |
| Remote evidence changes nothing local | [R] |
| A signal while requests run | [R] |
| [E]'s nine scenarios (kept, PR #19's text) | MODIFIED [E] |
| The overview's remote-phase children | MODIFIED [E] |

Each has a test named after it; the packet's deferred scenario (DI:1450-1454)
is covered by "One request per exact head", "Remotes that give no request",
"API failures stay unknown" and "Expiry cancels queued and in-flight
requests".

## Risks / Trade-offs

- [GitHub's commit association returns no pull request closed without merging
  (F-3)] -> `closed` is not a state, and the not-found text says that no
  merged or open pull request was found.
- [The association was checked live only for squash merges in one repository,
  not for a rebase merge, a pull request from a fork, a commit that two pull
  requests share or a pull request whose base is not the repository's default
  branch] -> The `not-found` text says that no merged or open pull request was
  found, never that none exists; task 2.5 checks these cases live before the
  Speckit handoff; and no answer ever makes a row removable.
- [The merge target is not the repository's default branch (CAS/pc:482-485),
  or the merge was a rebase] -> Not verified live until task 2.5; a miss
  reads `not-found`, never `merged`.
- [The merge target tracks the person's fork] -> The identity is the fork
  (C-3), so a pull request into its parent never meets [R]'s base-repository
  rule and every queried row reads `not-found`; the README's `--remote`
  paragraph says so.
- [A merge-commit merge that the local merge-target branch does not hold yet
  reads like a squash merge] -> The merged line names both causes; bringing
  that local branch up to date lets local ancestry decide, since a fetch
  alone moves only its remote-tracking ref (APO/ov:358-365).
- [Rate limits on a large estate] -> At most 64 requests a run; each limited
  key is `rate-limited`, and the rest of the run is unaffected.
- [`gh` versions differ] -> The argv uses long-standing `gh api` options; a
  `gh` that rejects it exits without a status line, which is `api-error`,
  never a wrong answer; switches a version does not know are ignored.
- [A `gh` child could write its own state or reach other endpoints beyond its
  documented switches] -> The switches gh documents are set, the
  zero-mutation snapshots cover every root, and gh's configuration directory
  lies outside them; gh's own behaviour beyond that is GitHub's
  (`proposal.md`, What This Repository Does Not Own).
- [`GH_TOKEN` reaches the child] -> It is the normal authentication path;
  `project` never reads it, and no output or message carries an environment
  value.
- [A `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` or `HOME` set to a non-empty value that
  does not begin with `/` makes every keyed row `gh-unavailable` and starts no
  child (C-44)] -> A caller whose configuration sits under a relative path gets
  no remote evidence, which fails closed and is never a wrong answer, and the
  README's next step for `gh-unavailable` says to make the path absolute, so
  that a person with a relative `HOME` does not go looking for `gh` on `PATH`.
  The refusal holds whichever of the three `gh` would use, on the raw bytes, and
  so covers a relative `HOME` beside an absolute `GH_CONFIG_DIR`, which lane
  openRepoProject-4's check of extensions found harmless today, since the argv
  begins with `api` (D5): that is deliberate over-refusal, not the fix of a
  demonstrated hole. The reason for refusing at all is the lead's check on `gh`
  2.96.0 (D5): from `/`, a relative value lands in a root-owned tree except a
  tree that any local user can write, such as `tmp`, `var/tmp` or `dev/shm`
  under `/`, where another local user could plant a `gh` configuration, and a
  configuration that held `http_unix_socket` made `gh api` send its request as
  plain HTTP over that socket with the token in the clear. Remote evidence never
  reaches an eligibility gate (D10), so a wrong answer would authorize nothing;
  the refusal protects the token.
- [`gh`, started in `/`, resolves every relative path in the caller's
  environment against `/`, not only the three that name its configuration; the
  rule leaves out `SSL_CERT_FILE`, `SSL_CERT_DIR`, `LD_LIBRARY_PATH`,
  `XDG_DATA_HOME`, `XDG_STATE_HOME` and `XDG_CACHE_HOME`] -> Each is left out
  because it is not `gh`'s documented configuration, each for its own reason
  below, and the remedy for each is the same, an absolute path. The README's
  next steps do not name them.
  - `SSL_CERT_FILE`, and each element of `SSL_CERT_DIR`, which Go's
    `crypto/x509` splits on `:`: a relative value resolves against `/`, so a CA
    planted in a tree that any local user can write, such as `tmp`, `var/tmp` or
    `dev/shm` under `/`, could let TLS be intercepted and the token exposed, but
    a planted CA is of use only to a party that also holds a network position
    from which to intercept, so the case is left as a residual. Lane
    openRepoProject-4 read this from Go's source; it is no test of `gh`.
  - `LD_LIBRARY_PATH`, as lane openRepoProject-3 corrected the reason: a library
    planted where a relative entry resolves under `/` runs inside a dynamically
    linked `gh` and needs nothing more. It is left out because it is not `gh`'s
    configuration, and because a relative entry is already the caller's own
    hazard in every directory they run anything from: running in `/` only fixes
    where it resolves. Release builds of `gh` are static, so the case needs a
    distribution build that links dynamically; the `gh` 2.96.0 binary checked
    here is a static executable, `ldd` printing "not a dynamic executable".
  - `XDG_DATA_HOME`, `XDG_STATE_HOME` and `XDG_CACHE_HOME`, each left out for
    what is known of it and no more (C-45): `gh help environment` documents
    `XDG_CONFIG_HOME` and names none of these three, though the `gh` 2.96.0
    binary holds each name once (lane openRepoProject-3's count, which the
    writer repeated), and a relative value of any of them resolves against `/`,
    as the others do. The checks below were run offline on 2026-10-21 with a
    fake token, in a scratch directory standing for `/`; where a request was
    answered, a small server on a Unix socket answered it, which `gh` reaches
    through `http_unix_socket`, as the lead's check in D5 showed.
    - The data directory holds extensions, which D5's argv never runs, since it
      begins with `api` (lane openRepoProject-4's check, D5, run under a
      relative `HOME`). The writer's own, under a relative `XDG_DATA_HOME` that
      held planted `gh-api` and `gh-zzz` extensions: `gh zzz` ran the planted
      extension, while `gh api --help` and D5's argv, whether the request failed
      to connect or the stand-in answered it, ran `gh`'s own command and client
      and never the planted `gh-api`, and `gh` wrote no file there.
    - The state directory serves the update check, which the two notifier
      switches turn off as far as `gh` documents them. `gh help environment`
      documents the check, once every 24 hours, and both switches, which D5
      sets, and does not name this directory; D5's argv, with the switches set,
      wrote no file under a relative or an absolute `XDG_STATE_HOME`; and the
      writer could not make the update check itself run offline (in a
      pseudo-terminal with the switches unset and a stand-in for the release
      endpoint, no request for that endpoint came), so that the check's use of
      this directory is not observed here.
    - The cache serves `--cache`, which D5 never passes: `gh api --cache 1h`,
      answered by the stand-in, wrote a file under an absolute
      `$XDG_CACHE_HOME/gh`, and `gh api` without it, as D5's argv runs, wrote
      none under a relative or an absolute `XDG_CACHE_HOME`.
- [Collection used most of the 60 s] -> The requests end at the deadline as
  `cancelled` or `aborted`, and `remote.completeness` says `incomplete`.
- [A `PATH` directory on an unreachable mount ahead of the one holding `gh`]
  -> The lookup is cut at 5 s and every keyed row is `gh-unavailable`, never
  a row or scan error, though a `gh` lies further on; the README's next step
  says to check that `PATH`'s directories are reachable (C-26).
- [The `for-each-ref` atoms on the Git 2.36 floor] -> Checked on 2.43 here;
  the realization checks them on 2.36 as change 1 checked its probes. Reading
  the two keys with `git config --get` in their place, the fallback this entry
  named, was rejected in C-48 (reader RC's M2, its option (b)): it costs one
  more child per repository, changes the count that [B]'s added paragraph
  states, and gives up Git's own reading of the upstream, by which a remote
  whose fetch refspecs do not map the merge ref is `no-remote-target`, as the
  spec now says, so it would need spec changes before the Speckit handoff.
- [A response's `url` in an unexpected form] -> The key is `api-error`; an
  unchecked string is never printed.
- [Two clones of one repository with different merge targets share a key] ->
  Each row is matched with its own base branch (D4, D6).
- [A tool compares `probes` between a run with `--remote` and one without]
  -> The difference is exactly D2's reads, stated in [B]'s added paragraph
  and pinned by its new scenario; without `--remote` nothing differs.

## Migration Plan

Nothing migrates: without `--remote` no output, flag or exit changes.

1. Ratification by Brett Heap's word on the pull request the lane opens for
   this change.
2. After feature 005 has landed and change 2 is archived, with this change's
   MODIFIED blocks re-read against the archived text and task 2.5's live
   contract check recorded, `/speckit.specify`,
   from a `main` synced to `origin/main`, creates the one feature under the
   next free number, 006 or later; it is recorded once in `tasks.md` under
   "Speckit Handoff", and `/opsx:apply` runs only then.
3. The realization PR merges with green checks on both CI jobs of the
   `tests` workflow, `test (3.10)` and `test (3.12)` on `ubuntu-latest`
   (Linux only since PR #32; L-12), and closes issue #25.
4. The change is archived after that merge, after change 2's archive, which
   itself follows change 1's archive and feature 005's merge, and after task
   2.4: PR #19's amendment landed or, if PR #19 closed, the block of [E]
   re-based on change 1's text, re-read against change 1's archived block and
   re-based on it if that block moved past PR #19's text at `c462d87`, and that
   block re-based on `add-project-clean-branch-retirement`'s archived block if
   that change archives first (L-17).

Each re-read or re-base of a block in steps 2 and 4 (tasks 2.3 and 2.4) is
checked by two diffs (reader RF's M1; C-51). The first, `diff -u` of the
archived block against this change's re-based block, shows additions only, as
tasks 2.3 and 2.4 say, and is kept. It cannot see a change to this change's own
words, which after the earlier change archives are all additions to the archived
block, so a re-base that reworded them would still show additions only, validate
and archive. The second, `diff -u` of this change's block as committed at its
ratified head against the re-based block, shows only the archived block's own
text carried in: for the block of [E], change 1's archived text in place of
PR #19's at `c462d87`, with the additions of
`add-project-clean-branch-retirement` if that change archived first; for the
three `project-overview` blocks, change 2's archived text in place of its text
at `961c405`. Any change that the second diff shows to this change's own
ratified words, the two added sentences and the added scenario of [E] and the
added paragraphs and scenarios of the three `project-overview` blocks, returns
the block to Brett Heap before the Speckit handoff (step 2) or before the
archive (step 4); a sentence that task 2.3 re-aligns, or that lane
openRepoProject-4 asks for, is such a change. The ADDED requirement has no
archived block, so a `diff -u` of it as committed at the ratified head against
the re-read text shows any change to it, and such a change returns to Brett Heap
in the same way. Tasks 2.3 and 2.4 name both diffs, on lane openRepoProject-4's
YES of 2026-10-21.

Rollback: revert the realization's merge; `--remote` goes away, and the
default overview, which nothing here changed, is untouched.

## Open Questions

`proposal.md` puts two questions before Brett Heap; the third, put to lane
openRepoProject-4 first, is resolved by its answer of 2026-10-20 (C-23):
feature 005 reserves no flag, field or hook. Taken as recommended, none
changes what is built.
The second, if decided for direct HTTPS, would replace D5's client and part
of D6, so it is settled before the Speckit handoff.
