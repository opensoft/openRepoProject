## MODIFIED Requirements

### Requirement: Overview is local and read-only
The overview SHALL open no network connection and SHALL make no filesystem or
Git mutation: no fetch, pull, reset, bootstrap, validator run or file write;
no worktree created, pruned, repaired, locked or unlocked; and no index
rewritten, every Git child running read-only as `Repository inspection
requires Git 2.36 and shares one evidence model` defines. It SHALL read no
credential file and no profile data the scan does not need, and SHALL keep no
state beyond one invocation. Ahead, behind and merge evidence SHALL be
observations as of the last fetch, and both outputs SHALL say so.

Without `--remote`, this requirement holds as written. With `--remote`, the
network clause of the first sentence SHALL still bind the `project` process
and every Git child, and SHALL NOT bind the `gh` children that `Overview
reports remote merge evidence on request` defines; each of those SHALL query
GitHub's API for the host `github.com` only and SHALL send only that
requirement's read-only query. Every other clause of this requirement SHALL
hold in a `--remote` run, its credential clause excepted: no fetch, mutation
or file write, and no remote answer kept beyond the invocation. In place of
that clause, the `project` process SHALL read no credential file and no
profile data the scan does not need; a `gh` child authenticates by the GitHub
client's own means, reading what that client reads; and the overview SHALL
read, test, print and forward no credential value, the caller's environment
excepted, which it passes to a `gh` child unread. Both outputs SHALL label
remote evidence as queried live, apart from the local evidence, which stays
as of the last fetch.

#### Scenario: Local and read-only
- **WHEN** the overview runs with default options over any fixture of this capability, with networking disabled for the process
- **THEN** it opens no network connection, and the before and after snapshots of `git for-each-ref`, `git worktree list --porcelain -z`, each checkout's status, each index file's modification time and the directory tree under every root are identical
- **AND** the JSON preserves severity, freshness, unknown values and completeness, and a complete scan that finds no project says so and exits 0

#### Scenario: A remote run stays read-only apart from its queries
- **WHEN** the overview runs with `--remote` over a fixture whose worktree rows need remote evidence, with a fake `gh` first on `PATH` that records each argv, environment and working directory, and with networking disabled for the `project` process
- **THEN** the `project` process opens no network connection, every Git child carries the protocol pins that `Repository inspection requires Git 2.36 and shares one evidence model` defines, and the before and after snapshots named in "Local and read-only" are identical
- **AND** every recorded `gh` argv carries the read-only query of `Overview reports remote merge evidence on request` and no mutation, every recorded `gh` environment sets `GH_NO_UPDATE_NOTIFIER=1`, `GH_NO_EXTENSION_UPDATE_NOTIFIER=1` and `GH_PROMPT_DISABLED=1`, so that `gh` writes no update-check state of its own, neither output carries a credential value, and a second run sends the same requests again, nothing having been kept from the first

### Requirement: Overview bounds its work and reports what it omitted
The overview SHALL bound each run by its own invocation deadline, 60 s on a
monotonic clock set before any root is listed, and each Git child by the
per-child budget that
`Repository inspection requires Git 2.36 and shares one evidence model` gives
under an invocation deadline, which with no reserve is
`min(5 s, deadline - now)`; a child whose budget is not positive SHALL NOT
start. Each child SHALL run in its own process group; a child that reaches its
budget, or whose output the overview stops reading early, SHALL receive SIGTERM
to its group, then SIGKILL after 2 s, and SHALL be reaped within a further 2 s
grace or abandoned, its row recorded `probe-timeout`. On deadline expiry no
further child SHALL start, every in-flight child SHALL be terminated together
in the same way and recorded `deadline-exceeded`, each candidate whose
collection never started SHALL still be a row carrying only filesystem facts,
status `error` and a `deadline-exceeded` error, and one `deadline-exceeded`
scan error SHALL count the candidates not started.

Every filesystem call, root canonicalisation and deduplication, marker and
holder checks, registration reads, manifest reads and branch reflog reads
(each at most 64 KiB and never a Git child) included, SHALL run in a bounded
task waited for with `min(5 s, deadline - now)`; a task that does not finish
in time SHALL record `probe-timeout`, or `deadline-exceeded` when the deadline
was the smaller limit, for its root or row, and the overview SHALL move on, a
reflog read cut this way leaving its row unprobed for the gate that
`Overview suggests only gated clean commands` states. A root cut this way
SHALL count as `truncated`, and its listing SHALL read no further entry once
the root is abandoned. A manifest whose `st_size`, taken before the read,
exceeds the 1 MiB that
`Repository inspection requires Git 2.36 and shares one evidence model` allows
SHALL be `manifest-invalid` on its row without being read, and the manifest
reader's read SHALL never exceed 1 MiB. The ref listing SHALL be parsed as it
streams, keeping only the local heads, `origin/HEAD`, the remote refs named as
upstreams and one flag recording whether a remote copy of the merge target
exists. The status probe and its record bounds SHALL be those that requirement
defines. Every Git child SHALL also run with
`-c protocol.allow=never -c protocol.file.allow=never -c protocol.ssh.allow=never -c protocol.git.allow=never -c protocol.http.allow=never -c protocol.https.allow=never -c protocol.ext.allow=never`,
pinned beside the environment and the status pins that requirement defines
(`GIT_OPTIONAL_LOCKS=0`, and on a status probe
`-c core.untrackedCache=false -c core.fsmonitor=false`), because Git 2.43
has no `GIT_NO_LAZY_FETCH`: without the pins a read-only probe in a partial
clone could fetch missing objects from the network, and with them that fetch
fails locally, so the failed probe is recorded as `probe-failed` on its row,
a failed status probe leaves its worktree `inspection-error`, and no
network call is made. The per-protocol pins sit beside `protocol.allow`
because it is only the default policy: a per-protocol `allow=always` in a
config file or `GIT_ALLOW_PROTOCOL` in the caller's environment would still
allow the fetch (R-25). `GIT_ALLOW_PROTOCOL` is therefore among the seventeen
names that the child-environment scrub of that requirement removes before any
Git call, a scrub this requirement carries by citation. That requirement
carries the same pins.

The caps SHALL be 32 roots, 4,096 entries per root, 128 candidates and 512
worktree rows across the run, main worktrees included. The OQ-4 measurement
of governance task 2.1, made on a Linux filesystem, confirmed them, and they
stand as measured; the values in force are always reported in `limits`. The
root, candidate and worktree-row caps SHALL apply after canonical sorting,
and the entry cap in listing order. Each cap that drops work SHALL be
reported as a
`scan-limit` error naming the cap in `limit` and carrying `omitted: {count,
exactness}`: `exact` with the count dropped when the whole population was
enumerated; `lower-bound` with the count known to be dropped when an
enumeration that could add to it stopped early (a truncated, unreadable or
deadline-cut root listing, or an unread worktree registry); `unknown` with
count null when the population was not enumerated, as with the entry cap.
Worktree rows SHALL be ranked by repository rank, the canonical position of
the candidate that first reached the repository, then by row order; rows past
the cap SHALL keep their registry and branch evidence with `dirty`,
`ignored_files` and `classification` null, and their project rows SHALL carry
`scan-limit` errors.

At most four Git children SHALL run at once, never two once their
`common_dir` is known to be the same, and one repository's children SHALL run
one at a time. Collection SHALL run in two canonical phases: the identity and
repository-wide probes, then the worktree status probes. A repository's
second phase SHALL start only when every candidate earlier in canonical order
has completed or failed its identity probe and every repository earlier in
canonical order has finished its first phase; identity probes may still be
dispatched ahead of that point. In a run in which no child, task or root
listing reaches its budget and the deadline does not expire, the JSON
document, apart from timestamps and `budget.probe_concurrency`, SHALL NOT
depend on concurrency or completion order.

The envelope SHALL report `probes: {estimated, performed}`: `performed`
counts every Git child started, timed-out and stopped ones included;
`estimated` counts 1 for the version check, 1 per Git candidate, 3 more per
distinct repository whose identity was established, 1 per Git child needed
to name the main checkout of a repository whose first registry record equals
its `common_dir`, and 1 per worktree row within the cap that is present and
registration-verified.

In a run with `--remote`, the remote-target reads that `Overview reports
remote merge evidence on request` starts after collection SHALL be Git
children under this requirement, and `performed` SHALL count them as it counts
every Git child started; `estimated` SHALL also count, per distinct
repository with a worktree row that requirement queries, 1 for the read of
its merge target's `branch.<target>.remote` and `branch.<target>.merge`, and
1 more when that read succeeds and names a remote other than `.` with a merge
ref under `refs/heads/`, for the read of that remote's URL. That
requirement's `gh` children are not Git children and SHALL be counted in
neither. A remote-target read or a `gh` child that exits nonzero, reaches its
limit, whose output the overview stops reading early, or that the deadline
stops SHALL be recorded as that requirement states, in the `remote` field of
the rows it serves, never as a row error or a scan error. Without `--remote`,
both counts stay exactly as stated above.

#### Scenario: Candidate cap after sorting, with an exact count
- **WHEN** one root holds 130 candidate directories `p000` to `p129`, created in reverse order
- **THEN** the rows are `p000` to `p127` whatever the listing order, and one `scan-limit` scan error has `limit: "candidates"` and `omitted: {"count": 2, "exactness": "exact"}`
- **AND** the result is incomplete and the exit status is 1

#### Scenario: Candidate cap with an incomplete listing
- **WHEN** that root is given together with a second root holding 4,100 entries
- **THEN** the second root is `truncated` with a `root_entries` `scan-limit` error whose omitted count is null with exactness `unknown`
- **AND** the candidate-cap error reports the known excess with exactness `lower-bound`, and the exit status is 1

#### Scenario: Root and worktree-row caps
- **WHEN** 33 distinct roots are given
- **THEN** the last in canonical order is `omitted`, with an exact omitted count of 1
- **AND** when the repositories total 520 worktree rows, the first 512 in rank order are probed on every run whatever the completion order, the other 8 keep registry and branch evidence with `dirty`, `ignored_files` and `classification` null, their project rows carry `scan-limit` errors, the scan error has `limit: "worktree_rows"` and `{"count": 8, "exactness": "exact"}`, and the exit status is 1

#### Scenario: Probe timeout
- **WHEN** one worktree's status probe does not finish within 10 s
- **THEN** that child is stopped at 5 s and reaped, the row records `probe-timeout` with `dirty: null` and classification `inspection-error`
- **AND** every other row is complete and the exit status is 1

#### Scenario: Hung filesystem call on an external worktree
- **WHEN** the `lstat` of an external worktree's path takes 10 s, on a fixture mount where one is available and by an injected slow call otherwise
- **THEN** the call is abandoned at 5 s, that worktree records `probe-timeout`, every other row is complete, and the exit status is 1

#### Scenario: Invocation deadline
- **WHEN** enough held probes are given to exceed 60 s
- **THEN** no child starts after the deadline, and every in-flight child is terminated, reaped within the grace and recorded `deadline-exceeded`
- **AND** unstarted candidates appear as rows with `deadline-exceeded`, the scan error's omitted count is exact, and the process exits 1 within 64 s plus rendering

#### Scenario: Bounded concurrency
- **WHEN** eight single-worktree repositories each have a status probe held for 1 s
- **THEN** the process table never shows more than four of the overview's Git children at once, nor two with the same `common_dir`
- **AND** the eight held probes take about 2 s rather than 8 s

#### Scenario: The JSON does not depend on concurrency
- **WHEN** one fixture, including repositories whose worktree rows exceed the worktree-row cap, is collected with probe concurrency 1 and with probe concurrency 4, and no budget or deadline is reached
- **THEN** the two JSON documents are byte-identical apart from timestamps and `budget.probe_concurrency`, and the same rows are probed

#### Scenario: Bounded ignored files
- **WHEN** a clean merged worktree holds 10,000 ignored files
- **THEN** the status stream stops early, `ignored_files` is 64 with `ignored_files_truncated: true`, `ignored_samples` has eight entries, `dirty` is false, and the classification is `ignored-local-files`, a preserve finding
- **AND** with exactly 64 ignored files `ignored_files` is 64 with `ignored_files_truncated: false`, and with 4,097 untracked files and no ignored ones the stream stops at the record bound, `dirty` is true, `ignored_files` is null and the classification is `dirty`, not `inspection-error`

#### Scenario: User status configuration
- **WHEN** the user's Git configuration sets `status.showUntrackedFiles=no` and a linked worktree is clean, pushed and merged
- **THEN** the status probe succeeds, `ignored_files` is 0 and the worktree is `merged-removable`

#### Scenario: A root on a hung mount
- **WHEN** canonicalising or listing one root given with `--root` takes 10 s, on a fixture mount where one is available and by an injected slow call otherwise
- **THEN** that root is cut at 5 s with a `probe-timeout` scan error and counts as `truncated`, no entry of it is read after the cut, and every other root's candidates are collected
- **AND** the exit status is 1

#### Scenario: A repository root on a hung mount
- **WHEN** a linked worktree under a root belongs to a repository whose main checkout is on a mount where every filesystem call takes 10 s
- **THEN** each bounded task on that path records `probe-timeout` at 5 s on that row, the scan continues and every other row is complete
- **AND** the run ends within the deadline and the exit status is 1

#### Scenario: A manifest over the size bound
- **WHEN** a candidate's `project.yaml` is larger than the manifest size bound
- **THEN** its row carries a `manifest-invalid` error naming the manifest and the bound, the file is neither read nor parsed, the other rows are complete, and the exit status is 1

#### Scenario: Probe counts in a remote run
- **WHEN** one root holds two repositories, each with one linked worktree whose branch is not merged into its merge target, the first's merge target tracking `refs/heads/main` of a remote whose URL is `https://github.com/acme/widget.git` and the second's naming no remote, and the overview runs once without `--remote` and once with it, a fake `gh` answering at once, so that no child, task or root listing reaches its budget and the deadline does not expire, and the `--remote` run is one in which `remote.completeness` and the envelope's `completeness` are both `complete`
- **THEN** in each run `probes.estimated` equals `probes.performed`, and in the `--remote` run each is 3 more than in the run without it: two reads for the first repository and one for the second, whose merge target names no remote
- **AND** the run without `--remote` starts no remote-target read, the `--remote` run's one `gh` request is counted only in `remote.requests`, as `{"estimated": 1, "performed": 1}`, and its `remote` object has no `probes` key

## ADDED Requirements

### Requirement: Overview reports remote merge evidence on request
`project overview --remote` SHALL add explanatory pull-request evidence from
GitHub to the worktree rows whose merge local ancestry does not prove, and
SHALL change nothing else that the other requirements of this capability
define. `--remote` SHALL combine with every other overview option and SHALL be
an option of `project overview` alone; `project clean`, `status` and `doctor`
stay local as their own requirements state. Without `--remote` the overview
SHALL start no `gh` child and SHALL print no field or line that this
requirement adds.

Query set: a worktree row SHALL be queried when its `branch` names a branch
other than the merge target, its `head` is known and its `merged_into_target`
is false, whatever its classification and whether or not its upstream still
exists; no other worktree row SHALL carry a `remote` key.

Remote target: after collection, for each repository with a queried row, the
overview SHALL read the merge-target branch's `branch.<target>.remote` and
`branch.<target>.merge`, then that remote's URL as Git expands it, by at most
two Git children run one at a time in that repository; it SHALL never take the
remote target from a worktree row's upstream or require the merge target to be
checked out. These children SHALL be read-only probes with the environment,
pins and scrub that `Repository inspection requires Git 2.36 and shares one
evidence model` defines and the per-child budget that `Overview bounds its
work and reports what it omitted` gives. They SHALL be counted in the
envelope's `probes` as that requirement states for a run with `--remote`.
Every queried row of a
repository SHALL be `unavailable`, with no request, and with the first reason
that applies: no remote named for the merge target, a remote of `.`, given as
a URL or not configured, or a merge ref outside `refs/heads/`
(`no-remote-target`); a URL that carries a password, or any user name in an
`http` or `https` URL (`credential-bearing-remote`); a host other than exactly
`github.com` (`not-github`); and a path that, after an optional `.git` suffix
is stripped, does not give a valid GitHub `owner/repository` as `Parked-work
inspection constrains repository identity` accepts one (`malformed-remote`).
When one of these children fails for any other cause, reaches its budget or is
stopped by the deadline, those rows SHALL be `unknown` with reason
`remote-target-unread`. No remote URL, and nothing of one beyond its
`owner/repository`, SHALL appear in either output, in a `gh` argv or in any
message.

Requests: rows SHALL share one request per key `(host, owner/repository,
head)`, `owner/repository` compared without case, the keys taken in canonical
order: repositories by rank, then each repository's worktree rows in row
order. Each request SHALL be one `gh` child that runs `gh api` for the host
`github.com` with one fixed read-only GraphQL query asking, for that exact
commit, for at most 100 associated pull requests and whether a further page
exists. It SHALL read one page and never follow pagination, SHALL never use
gh's response cache, and SHALL run in the filesystem root with standard input
closed, with `GH_NO_UPDATE_NOTIFIER=1`, `GH_NO_EXTENSION_UPDATE_NOTIFIER=1`,
`GH_PROMPT_DISABLED=1`, `GH_TELEMETRY=false` and `NO_COLOR=1` set, so that gh
checks for no update, writes no state of its own, prompts for nothing, sends
no telemetry and prints no colour, and with `GH_DEBUG`, `DEBUG`, `GH_HOST`,
`GH_REPO`, `GH_FORCE_TTY` and `CLICOLOR_FORCE` removed from it, every other
variable passed on unread. At most 64 requests SHALL be sent per invocation; a
key past the 64th SHALL NOT be sent, and its rows SHALL be `unknown` with
reason `request-cap`. At most four `gh` children SHALL run at once. The
requests SHALL start after the remote-target reads, under a remote budget of
`min(30 s, deadline - now)` taken when the first request starts, part of the
60 s invocation deadline and never added to it. Each `gh` child SHALL get
`min(5 s, remote budget remaining)`, its own limit as a child of the overview,
and SHALL run in its own process group and be stopped, reaped or abandoned,
and terminated on a signal, as `Overview bounds its work and reports what it
omitted` and `Overview exits by completeness and severity` treat a Git child.
When the remote budget or the deadline expires, no further child SHALL start,
every queried row whose key was not yet sent or whose remote target was not
yet read SHALL be `unknown` with reason `cancelled`, and every request in
flight SHALL be stopped and its rows `unknown` with reason `aborted`.

Results: at most 1 MiB of each response body SHALL be read, and a key's result
SHALL come from its whole response, never from a partial answer. For each row
of the key, a response SHALL give `merged`, `open` or `closed` from the
returned pull requests whose head object id equals the row's `head` exactly,
whose base branch is the merge ref's branch and whose base repository is the
identity, a merged one before an open one before a closed one and the highest
number within a state; and `not-found` when none matches or GitHub holds no
commit with that object id. It SHALL give `unknown` with reason `further-page`
for a response that reports a further page, `truncated` for a body cut at
1 MiB, `timeout` for a child stopped at its 5 s limit, `unauthorized` for an
HTTP 401, `rate-limited` for a rate limit, `forbidden` for any other HTTP 403,
and `api-error` for any other failure, a response that cannot be parsed or
whose fields fail validation included. When `gh` is not on `PATH`, every
queried row that has a key SHALL be `unavailable` with reason
`gh-unavailable` and no `gh` child SHALL start; a `gh` child that exits
with gh's authentication-required status, 4, SHALL make its key's rows
`unavailable` with reason `gh-unauthenticated`. Each key SHALL be answered
on its own, a failure never stopping another key's request. No part of a
response body, of a `gh` child's standard error or of its environment SHALL
appear in either output. In a `--remote` run in which no child reaches its
limit and neither budget expires, the `remote` fields SHALL depend only on
the answers, never on concurrency or completion order.

Fields: in a `--remote` run, every queried worktree row SHALL carry `remote`,
`{state, number, url, head_sha, reason}`:
`state` is `merged`, `open`, `closed`, `not-found`, `unavailable` or
`unknown`, a closed enum; `number` and `url` are the chosen pull request's,
`url` accepted only as `https://github.com/<owner>/<repository>/pull/<number>`
for that number, and both are null unless `state` is `merged`, `open` or
`closed`; `head_sha` is the row's `head` that was asked about; and `reason` is
null for the first four states and one of the codes above for the last two.
The envelope SHALL carry `remote`: `host` (`github.com`); `observed_at` (when
the first request started, null when none started); `freshness` (the sentence
"Remote evidence was queried live from github.com and may already be stale; it
never authorizes cleanup."); `limits` (`requests` 64, `concurrency` 4,
`page_items` 100, `pages` 1, `response_bytes` 1048576); `budget`
(`request_timeout_seconds` 5, `remote_budget_seconds` 30);
`requests` (`estimated`, the distinct keys, and `performed`, the `gh` children
started); `counts` (the queried rows by `state`); and `completeness`
(`incomplete` exactly when a queried row is `unknown`, else `complete`). These
fields SHALL appear only in a `--remote` run: without `--remote` the worktree
row's `remote` key and the envelope's `remote` key SHALL be absent, not null,
and in a `--remote` run a worktree row outside the query set SHALL have no
`remote` key, never a null one.
This requirement SHALL add no value to any enum, finding code or
classification that the other requirements of this capability define, and
SHALL change no field that they define.

Isolation: remote evidence SHALL be explanation only. A `--remote` run and the
same run without it SHALL agree on every classification, finding,
`suggested_command`, `suggestion_gate`, row `status`, row error, scan error,
summary count, `completeness` and exit status, and their envelopes' `probes`
SHALL differ only by the remote-target reads that `Overview bounds its work
and reports what it omitted` counts in a run with `--remote`. A remote result,
and the failure, cut or stop of a remote-target read or of a `gh` child, SHALL
never be a row error, a scan error or a finding, `probe-failed`,
`probe-timeout` and `deadline-exceeded` in `Overview isolates one candidate's
failure` and `Overview bounds its work and reports what it omitted`
notwithstanding, and SHALL leave the row's classification, findings,
suggestion, `status`, the scan's `completeness` and the exit status exactly as
they are without `--remote`. A remote result SHALL be kept nowhere beyond the
invocation, so it can never be a `project clean` eligibility, `plan_digest` or
revalidation input; local ancestry stays the only removal proof.

Human report: for each shown worktree finding whose row has a
`remote`, once per worktree, a `remote` line SHALL follow that worktree's
path, reading for `merged` "merged on GitHub as pull request #<n>; local
ancestry does not prove it (a squash or rebase merge, or a merge target not
fetched since); never retired on this evidence", for `open` "pull request
#<n> on GitHub is open for this exact head", for `closed` "pull request #<n>
on GitHub was closed without merging", for `not-found` "no pull request on
GitHub matched this exact head", for `unavailable` "remote status unavailable
(<reason>)" and for `unknown` "remote status unknown (<reason>)". In a
`--remote` run one line SHALL follow the summary line, giving the requests
sent, the queried rows by state and the freshness sentence.

#### Scenario: A squash-merged branch is explained and kept
- **WHEN** a linked worktree's branch `001-feature`, with a commit of its own, was pushed with `git push -u` and squash-merged into `main` on GitHub, local `main` was fast-forwarded to the squash commit, the merge target's remote is `https://github.com/acme/widget.git`, and a fake `gh` answers that merged pull request #7 into `main` of `acme/widget` has exactly the branch's head
- **THEN** `project overview --remote --json` keeps the row `pushed-unmerged` with its informational finding and no suggestion, and its `remote` is `{"state": "merged", "number": 7, "url": "https://github.com/acme/widget/pull/7", "head_sha": "<head>", "reason": null}`
- **AND** the human report prints under that worktree the `remote` line "merged on GitHub as pull request #7; local ancestry does not prove it (a squash or rebase merge, or a merge target not fetched since); never retired on this evidence", and after the summary line one line giving 1 request, 1 merged and the freshness sentence
- **AND** `project clean <root> --all-safe` on the same fixture excludes that worktree as `pushed-unmerged` and starts no `gh` child

#### Scenario: A merged branch whose upstream was deleted
- **WHEN** that branch's upstream is then deleted on the remote and pruned locally, so that the row is `remote-gone`, and the fake `gh` answers as before
- **THEN** the row is queried by its head like any other, and its `remote.state` is `merged`
- **AND** it stays `remote-gone` with its preserve warning and only the read-only `project clean <root>` as its suggestion

#### Scenario: The remote target comes from the merge target's branch configuration
- **WHEN** `branch.main.remote` names `upstream`, whose URL is `git@github.com:acme/widget.git`, the queried worktree's own branch tracks `origin`, a fork at `https://github.com/alice/widget.git`, and the main worktree is detached at `main`'s tip, so that no worktree has `main` checked out
- **THEN** the one request asks `acme/widget` about the row's head, and a returned pull request whose base repository is `alice/widget`, or whose base branch is not `main`, never matches
- **AND** when `upstream`'s URL is instead `gh:acme/widget` under `url.git@github.com:.insteadOf gh:`, the request still asks `acme/widget`

#### Scenario: One request per exact head
- **WHEN** two independent clones of `acme/widget` under one root each hold a linked worktree on branch `topic` at the same unmerged head, a third worktree is one commit ahead of that head, and a fourth holds a head that was never pushed, which GitHub does not hold
- **THEN** exactly three `gh` children run, one per distinct head, both clones' `topic` rows carry the answer of their shared request, and the fourth row is `not-found`, not `unknown`
- **AND** a `merged-removable` worktree, a detached worktree and the main worktree on `main` have no `remote` key, not even a null one, and cause no request

#### Scenario: Remotes that give no request
- **WHEN** the merge targets of four repositories have as their remote's URL `https://alice:s3cr3t@github.com/acme/widget.git`, `https://evilgithub.com/acme/widget` and `https://github.com/acme`, and no remote at all for the fourth
- **THEN** their queried rows are `unavailable` with reasons `credential-bearing-remote`, `not-github`, `malformed-remote` and `no-remote-target`, and no `gh` child starts
- **AND** neither output, no argv and no message contains `s3cr3t` or any of those URLs

#### Scenario: No gh, or a gh without authentication
- **WHEN** `gh` is not on `PATH` and two rows with distinct heads are queried
- **THEN** both are `unavailable` with reason `gh-unavailable`, no child starts, `remote.requests.performed` is 0, and the exit status is the one the run has without `--remote`
- **AND** when instead the fake `gh` exits 4 with nothing on standard output, both requests are sent, and both rows are `unavailable` with reason `gh-unauthenticated`

#### Scenario: API failures stay unknown
- **WHEN** the fake `gh` answers seven keys with an HTTP 401, an HTTP 403, a rate limit, an HTTP 502, a page whose further-page flag is set, a body of 1 MiB and one byte, and nothing for 10 s
- **THEN** those rows are `unknown` with reasons `unauthorized`, `forbidden`, `rate-limited`, `api-error`, `further-page`, `truncated` and `timeout`, none carries a number or URL, the held child is stopped at 5 s and reaped, and `remote.completeness` is `incomplete`
- **AND** no part of a response body or of `gh`'s standard error appears in either output, and the overview's findings, `completeness` and exit status equal those of the run without `--remote`

#### Scenario: A failed or held remote-target read stays unknown
- **WHEN** one root holds two repositories, each with one linked worktree whose branch is not merged into its merge target, which tracks `refs/heads/main` of a remote whose URL is `https://github.com/acme/widget.git` in the first and `https://github.com/acme/gadget.git` in the second, and the overview runs once without `--remote` and once with it, a fake `gh` first on `PATH`, the first remote-target read of the `--remote` run exiting 128 in the first repository and not finishing within 10 s in the second
- **THEN** the first repository's queried row is `unknown` with reason `remote-target-unread`, no second remote-target read starts there, the failed read counts in `probes.performed`, and every classification, finding, suggestion, `completeness` and exit status equals that of the run without `--remote`
- **AND** the second repository's first remote-target read is stopped at 5 s and reaped, its queried row is `unknown` with reason `remote-target-unread` and the stopped read counts in `probes.performed`, neither row carries a `probe-failed`, `probe-timeout` or `deadline-exceeded` error, no `gh` child starts, and `remote.completeness` is `incomplete`

#### Scenario: The request bounds
- **WHEN** one root's repositories give 70 distinct queried heads and the fake `gh` holds each request 0.2 s
- **THEN** 64 `gh` children run, never more than four at once, the six keys last in canonical order are `unknown` with reason `request-cap`, and `remote.requests` is `{"estimated": 70, "performed": 64}`
- **AND** every argv runs `gh api` for the host `github.com` with the fixed query asking for at most 100 pull requests, with no pagination or cache option, in the filesystem root, and every recorded environment sets `GH_NO_UPDATE_NOTIFIER=1`, `GH_NO_EXTENSION_UPDATE_NOTIFIER=1`, `GH_PROMPT_DISABLED=1`, `GH_TELEMETRY=false` and `NO_COLOR=1`, lacks `GH_DEBUG`, `DEBUG`, `GH_HOST`, `GH_REPO`, `GH_FORCE_TTY` and `CLICOLOR_FORCE`, and keeps `GH_TOKEN` as the caller set it

#### Scenario: Expiry cancels queued and in-flight requests
- **WHEN** 40 distinct keys are queried and the fake `gh` holds every request 4 s, so that the 30 s remote budget expires with requests in flight and keys not yet sent
- **THEN** no `gh` child starts after the expiry, each key not yet sent is `unknown` with reason `cancelled`, each request in flight is stopped, reaped and `unknown` with reason `aborted`, and the process exits within 64 s plus rendering
- **AND** when collection leaves less than 30 s before the 60 s deadline, the requests end at the deadline in the same way

#### Scenario: Remote evidence changes nothing local
- **WHEN** one fixture with a `merged-removable`, a `pushed-unmerged`, a `remote-gone` and a dirty worktree runs with and without `--remote`, the fake `gh` answering `merged` for every key
- **THEN** the two JSON documents differ only in timestamps, in the envelope's `remote` and the queried worktree rows' `remote`, and in the envelope's `probes`, whose `estimated` and `performed` each grow by the remote-target reads alone, and every classification, finding, suggestion, `suggestion_gate`, summary count, `completeness` and exit status is equal
- **AND** the run without `--remote` starts no `gh` child and no remote-target read, its document has no `remote` key at all, absent rather than null, and its human report no `remote` line

#### Scenario: A signal while requests run
- **WHEN** SIGTERM is sent while four `gh` children are held
- **THEN** the exit status is 143, no result document is printed, `Cancelled.` is printed to standard error when it can be, and no process of any `gh` child's group remains
- **AND** with SIGINT instead the exit status is 130
