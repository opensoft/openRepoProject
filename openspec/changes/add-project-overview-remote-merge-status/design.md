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
`e198548..67e43ae` (C-34); this design describes
`specs/project-overview/spec.md` as round C6 leaves it, written but held for
lane openRepoProject-4 and not committed, and until it agrees the committed
file is the one it agreed in round C5 (`6fe8a5e`).

Citations follow `proposal.md`: the packet at `da33d92`; APO, CAS, PRS and
`project:N` at main `961c405`, which main `e9d6711` holds unchanged for them
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
  reuses both and adds the reason that tells a credential-bearing URL from a
  foreign host or a malformed path.
- `cleanup_report()` (`project:544-622`) is where `09af8c8` attached its
  lookup and its three extra classes; this change touches nothing of `clean`.
- The parser (`project:1074`) has no `overview` yet. Feature 005 adds the
  subcommand; this change's feature adds `--remote` to it.
- The tests' fakes: `fake_bin()` (tests:148) is the temporary bin directory,
  `write_fake()` (tests:172) writes a fake tool into it, and `question_env()`
  (tests:154-170) builds a `PATH` of that directory and the directories of
  `bash`, `git` and the interpreter, dropping `GH_TOKEN` and `GITHUB_TOKEN`.
  D11 builds on all three.
- After features 004 and 005: the overview's control loop on the main thread
  with its in-flight child registry, self-pipe and signal handling (APO
  design.md, D1), its two-phase scheduler (D6) and its renderers (D10), driving
  change 1's child handle (start, readable descriptors, `terminate_group` with
  the 2 s grace, reap). The realization adds a phase and a child kind to that
  loop and asks nothing of feature 005 in advance (`proposal.md`, Open
  Questions 3).
- Tool facts checked for this design: Git 2.43.0 answers
  `for-each-ref --format='%(upstream:remotename)%00%(upstream:remoteref)'`
  from `branch.<name>.remote` and `.merge` with no remote-tracking ref
  present, prints `.` for a local remote and empty fields for a remote given as
  a URL or for a branch with either key unset, and `git remote get-url <name>`
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
   `branch.<target>.remote` or no `branch.<target>.merge`, or a remote given as
   a URL), a remote of `.`, or a merge ref outside `refs/heads/` gives
   `no-remote-target`, and the second child does not run.
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
user information included, there (C-31). The URL that standard output carries
is the only credential-bearing text the overview inspects: it lives in memory
only while D3 derives the `owner/repository` and detects the URL's user
information; after that no part of the user information is retained or
compared, none is ever printed, logged, sent or used to authenticate, and the
URL is never forwarded with it (C-30).

The two reads are counted in the envelope's `probes`, as lane
openRepoProject-4's fourth option has it (C-9): they are Git children, so
[B]'s `performed`, "every Git child started", counts them unchanged, and
[B]'s added paragraph gives `estimated` 1 per repository with a queried row
and 1 more per such repository whose first read named a usable remote, so the
reads add the same number to both counts in an uncut remote phase. A run
without `--remote` counts exactly as [B] does at `961c405`. The `remote` object
has no `probes` of its own, and the `gh` children, which are not Git children,
are counted only in `remote.requests` (D5). A read that exits nonzero, reaches
its budget, overruns its output cap or is stopped at the deadline is
`remote-target-unread` on its rows' `remote` and never a row error or a scan
error, the exception that [B]'s added paragraph and [E]'s added Termination
sentence state (D7, D10).

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
   yields no identity, as for `https://github.com/acme`, a user other than
   `git`, or an explicit port.

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
unless the run-wide `unavailable` of D5 and D6 applies: with no `gh` found
(D5), or when each of the 64 requests sent exits 4 with nothing on standard
output (D6), they are `gh-unavailable` or `gh-unauthenticated`, as every other
key is (C-25). A lookup that the deadline cuts is no such case, and leaves
them `request-cap` (D1; lane openRepoProject-3's folded read, L4; C-34).
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
`GH_TOKEN`, `GITHUB_TOKEN`, `GH_CONFIG_DIR` and the proxy variables pass
unread: that is gh's own authentication path (DI:1056-1057). The two update
notifier switches keep `gh` from its update check, once every 24 hours by its
own help text, and from the state it writes for it, as far as gh documents
them; "Overview is local and read-only" binds `project` and its Git children,
and gh's behaviour beyond its switches is the client's; the fake `gh` of D11
records the values, and that block's new scenario asserts them. [E]'s Git scrub
does not apply; this is not a Git child.

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

A lookup that fails, or that reaches its 5 s limit, as on an unreachable
`PATH` directory, gives what one that finds none gives: every keyed row,
whether or not its key is past the 64th, is `gh-unavailable`, and no child
starts (C-25, C-26). [B]'s bounded-task rule would otherwise record
`probe-timeout`; [B]'s added paragraph and [R]'s isolation clause record the
lookup's failure or cut only in the rows' `remote`, never as a row or scan
error (D10). A lookup that the deadline stops before its 5 s end leaves its
rows as an expiry does (D7), `cancelled` within the cap and `request-cap` past
it (C-28), just as [B] tells `deadline-exceeded` from `probe-timeout` and D7
tells `aborted` from `timeout`. The README's next step for `gh-unavailable`
names both causes: install `gh`, or check that `PATH`'s directories are
reachable.

Rejected: REST `commits/{sha}/pulls` (an unknown commit is HTTP 422, an
`unknown` under DI:1055-1056, and a further page shows only in a `Link`
header); `gh pr list` (by branch name, page information hidden, 30 items by
default); direct HTTPS from `project` (`proposal.md`, Open Questions 2).

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
  The council's adversary-engineer measured two on Python 3.12.3 on
  2026-10-20: a body under 1 MiB nested in `[` raised `RecursionError`, and a
  `number` of 5,000 digits raised a plain `ValueError` ("Exceeds the limit
  (4300 digits) for integer string conversion"), a limit Python has had since
  3.10.7 and 3.11; CI's Python 3.10 was not checked. An `errors` entry of type
  `RATE_LIMITED` gives `rate-limited`, and any other `errors` entry, a null
  `data.repository`, or a `data.repository.nameWithOwner` that fails D3's
  pattern (the field S-2 adds and C-19 takes, validated as each node's
  `baseRepository.nameWithOwner` is), gives `api-error`. A null
  `data.repository.object` gives `not-found`: GitHub holds no such commit.
  Otherwise `associatedPullRequests` must hold a boolean
  `pageInfo.hasNextPage`, which when true gives `further-page`, and a list of
  at most 100 `nodes`, more being `api-error` (AE-5's suggested text, taken by
  C-22).
- Each node must have a positive integer `number`; a `state` of `OPEN`,
  `CLOSED` or `MERGED`; a `headRefOid` of 40 or 64 hexadecimal digits; a
  string `baseRefName`; a `baseRepository.nameWithOwner` that passes D3's
  pattern; and a `url` exactly `https://github.com/` plus that
  `nameWithOwner`, `/pull/` and the number. One invalid node makes the whole
  key `api-error`, never a partial answer.

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
`remote` slots. Nothing it records is a row error, a scan error or a finding,
[B]'s added paragraph saying so for its children that exit nonzero or are
stopped and for a lookup of `gh` that fails or does not finish in time
(C-26), and [R]'s isolation clause for every failure, cut or stop of a
remote-target read, of that lookup or of a `gh` child, `probe-failed`,
`probe-timeout` and `deadline-exceeded` notwithstanding, so [X]'s exit status
and [J]'s `completeness` are what they are without `--remote`, unless the
remote phase raises an exception that [R] records as none of its reasons,
which exits 2 as [X] gives any exception outside the per-candidate boundary
(a body that the parser rejects, for any cause, is `api-error`, one of [R]'s
reasons, never such an exception: C-22), and the envelope's `probes` differs
only by D2's reads. Nothing is written to disk or kept past the run, `gh`
never gets `--cache`, and `project clean` has neither the option nor a reader
of these fields, so remote evidence never reaches an eligibility gate, a
`plan_digest` or a revalidation (SY:129-130; DI:1059-1060).

### D11. Test seams and the scenario map

- A fake `gh`, a Python script that `write_fake()` puts in `fake_bin()`,
  reads its argv, takes the `oid` field, looks it up in a JSON answer table
  beside it, and writes a status line, headers, a blank line and a body, the
  status line and the header names in the forms that task 2.5 records `gh`
  printing (C-19). Per key the table can hold the child for N seconds, exit 4
  with no output, send exactly 1 MiB of body, answered from its nodes, or
  1 MiB and one byte, set `hasNextPage`, answer
  401, 403, 429, a 403 with `X-RateLimit-Remaining: 0` or with a
  `Retry-After` header, a 200 body with an `errors` entry of a given type, a
  null `data.repository`, a status and header block of exactly 64 KiB,
  answered as any other, or over 64 KiB, a body of
  1 MiB of `[` or with a `number` of 5,000 digits (C-22), or 502, give the
  queried repository's `nameWithOwner` as the owner and name asked or, to
  stand for a renamed repository, as another, as the last AND of "The chosen
  pull request and a rejected answer" does (lane openRepoProject-3's delta
  read, F4), or name pull requests with any head, base and state. It places
  each pull request only in the list GitHub returned it in, the association,
  in a state that task 2.5 recorded there;
  the `CLOSED` nodes of "The chosen pull request and a rejected answer" are
  the one exception, a defensive input that pins that such a node never
  matches (C-16, C-19). It
  appends one JSON record per run: the argv, the names of the environment
  variables set, the values of `GH_NO_UPDATE_NOTIFIER`,
  `GH_NO_EXTENSION_UPDATE_NOTIFIER`, `GH_PROMPT_DISABLED`, `GH_TELEMETRY` and
  `NO_COLOR`, whether `GH_TOKEN` equals the caller's, the working directory,
  and its start and end times.
- A planted `gh`, a second fake that records each run, sits in the working
  directory of a run whose `PATH` begins with an empty entry and `.`, so that
  "No gh, or a gh without authentication" shows it never runs, and the fake
  `gh`'s recorded argv shows the absolute path each child was started by
  (C-22; lane openRepoProject-3's delta read, F3). For the same scenario the
  lookup's filesystem task takes the injected slow call that change 2's
  design patches into its filesystem tasks (APO design.md, D13), on a chosen
  `PATH` directory, so that the lookup is cut at 5 s (C-26).
- The counting `git` wrapper of change 2's design (APO design.md, D13), which
  can hold a chosen argv, gains one fixture control: for a chosen argv in a
  chosen repository it exits with a given status and a fixed line on standard
  error, without running Git, or, for a chosen argv, ignores SIGTERM and holds
  past its budget. "A failed or held remote-target read stays unknown" uses it
  to make the first remote-target read exit 128 in one repository and to hold
  it past 10 s in another, and "The overview's remote-phase children" to hold
  one past its budget while it ignores SIGTERM; this extends the test file
  only, never change 2's text.
- The bounded reader is unit-tested at N-1, N and N+1 bytes for each of its
  three bounds: the 1 MiB body, the 64 KiB of status and headers, and the
  64 KiB of a remote-target read's standard output. At N-1 and N the part is
  read whole and kept; at N+1 it is cut, giving `truncated`, `api-error` or a
  failed read, `remote-target-unread`. With the fake `gh`'s exact-size answers
  above, these pin the byte past each bound (C-27, C-29); they are tests only,
  and no scenario changes (lane openRepoProject-3's folded read, L2; C-34).
- No real network: in-process runs install an audit hook that fails
  `socket.connect` (APO design.md, D13); subprocess runs set `HTTPS_PROXY`
  and `HTTP_PROXY` to a closed local port, so even a real `gh` reached by
  mistake could not connect. No test needs `gh` installed.
- Fixtures: a bare repository takes the pushes; the merge target's
  `branch.main.remote` names a second remote whose URL is a `github.com` URL
  that nothing contacts; a squash merge is made in a publisher clone with
  `git merge --squash`, pushed and fetched.
- The expiry scenario patches the 30 s budget, the 5 s limit and the 60 s
  deadline down in-process, keeping their ratios, as change 2's design does
  for its deadline.
- Concurrency: the fake's start and end times show at most four overlapping
  children.

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
- [Collection used most of the 60 s] -> The requests end at the deadline as
  `cancelled` or `aborted`, and `remote.completeness` says `incomplete`.
- [A `PATH` directory on an unreachable mount ahead of the one holding `gh`]
  -> The lookup is cut at 5 s and every keyed row is `gh-unavailable`, never
  a row or scan error, though a `gh` lies further on; the README's next step
  says to check that `PATH`'s directories are reachable (C-26).
- [The `for-each-ref` atoms on the Git 2.36 floor] -> Checked on 2.43 here;
  the realization checks them on 2.36 as change 1 checked its probes, or
  reads the two keys with `git config --get`, at one more child. That fallback
  changes the count that [B]'s added paragraph states, so it needs a spec
  change before the Speckit handoff.
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
   re-based on change 1's text, and that block re-based on
   `add-project-clean-branch-retirement`'s archived block if that change
   archives first (L-17).

Rollback: revert the realization's merge; `--remote` goes away, and the
default overview, which nothing here changed, is untouched.

## Open Questions

`proposal.md` puts two questions before Brett Heap; the third, put to lane
openRepoProject-4 first, is resolved by its answer of 2026-10-20 (C-23):
feature 005 reserves no flag, field or hook. Taken as recommended, none
changes what is built.
The second, if decided for direct HTTPS, would replace D5's client and part
of D6, so it is settled before the Speckit handoff.
