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
requirement's read-only query. Every other sentence of this requirement SHALL
hold in a `--remote` run: no fetch, mutation or file write, and no remote
answer kept beyond the invocation. The `project` process SHALL read no
credential file; a `gh` child authenticates by the GitHub client's own means;
and the overview SHALL read, test, print and forward no credential value. Both
outputs SHALL label remote evidence as queried live, apart from the local
evidence, which stays as of the last fetch.

#### Scenario: Local and read-only
- **WHEN** the overview runs with default options over any fixture of this capability, with networking disabled for the process
- **THEN** it opens no network connection, and the before and after snapshots of `git for-each-ref`, `git worktree list --porcelain -z`, each checkout's status, each index file's modification time and the directory tree under every root are identical
- **AND** the JSON preserves severity, freshness, unknown values and completeness, and a complete scan that finds no project says so and exits 0

#### Scenario: A remote run stays read-only apart from its queries
- **WHEN** the overview runs with `--remote` over a fixture whose worktree rows need remote evidence, with a fake `gh` first on `PATH` that records each argv, environment and working directory, and with networking disabled for the `project` process
- **THEN** the `project` process opens no network connection, every Git child carries the protocol pins that `Repository inspection requires Git 2.36 and shares one evidence model` defines, and the before and after snapshots named in "Local and read-only" are identical
- **AND** every recorded `gh` argv carries the read-only query of `Overview reports remote merge evidence on request` and no mutation, every recorded `gh` environment sets `GH_NO_UPDATE_NOTIFIER=1`, `GH_NO_EXTENSION_UPDATE_NOTIFIER=1` and `GH_PROMPT_DISABLED=1`, so that `gh` writes no update-check state of its own, neither output carries a credential value, and a second run sends the same requests again, nothing having been kept from the first

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
exists; every other worktree row SHALL carry `remote: null`.

Remote target: after collection, for each repository with a queried row, the
overview SHALL read the merge-target branch's `branch.<target>.remote` and
`branch.<target>.merge`, then that remote's URL as Git expands it, by at most
two Git children run one at a time in that repository; it SHALL never take the
remote target from a worktree row's upstream or require the merge target to be
checked out. These children SHALL be read-only probes with the environment,
pins and scrub that `Repository inspection requires Git 2.36 and shares one
evidence model` defines and the per-child budget that `Overview bounds its
work and reports what it omitted` gives. They SHALL be counted in the `remote`
object's own `probes`, never in the envelope's `probes`, which SHALL keep in
every run the exact count that requirement defines. Every queried row of a
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

Fields: in a `--remote` run, every worktree row SHALL carry `remote`, null
outside the query set and otherwise `{state, number, url, head_sha, reason}`:
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
(`request_timeout_seconds` 5, `remote_budget_seconds` 30); `probes`
(`estimated`, 1 for each repository with a queried row and 1 more for each
whose first read succeeded and named a remote other than `.` with a merge ref
under `refs/heads/`, and `performed`, the remote-target reads started);
`requests` (`estimated`, the distinct keys, and `performed`, the `gh` children
started); `counts` (the queried rows by `state`); and `completeness`
(`incomplete` exactly when a queried row is `unknown`, else `complete`). These
fields SHALL appear only in a `--remote` run: without `--remote` the worktree
row's `remote` key and the envelope's `remote` key SHALL be absent, not null.
This requirement SHALL add no value to any enum, finding code or
classification that the other requirements of this capability define, and
SHALL change no field that they define.

Isolation: remote evidence SHALL be explanation only. A `--remote` run and the
same run without it SHALL agree on every classification, finding,
`suggested_command`, `suggestion_gate`, row `status`, row error, scan error,
summary count, the envelope's `probes`, `completeness` and exit status. A
remote result SHALL never be a row error, a scan error or a finding, and SHALL
be kept nowhere beyond the invocation, so it can never be a `project clean`
eligibility, `plan_digest` or revalidation input; local ancestry stays the
only removal proof.

Human report: for each shown worktree finding whose row has a non-null
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
- **AND** a `merged-removable` worktree, a detached worktree and the main worktree on `main` carry `remote: null` and cause no request

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
- **THEN** the two JSON documents differ only in timestamps and in the envelope's and the worktree rows' `remote`, the envelope's `probes` being equal, and every classification, finding, suggestion, `suggestion_gate`, summary count, `completeness` and exit status is equal
- **AND** the run without `--remote` starts no `gh` child and no remote-target read, its document has no `remote` key at all, absent rather than null, and its human report no `remote` line

#### Scenario: A signal while requests run
- **WHEN** SIGTERM is sent while four `gh` children are held
- **THEN** the exit status is 143, no result document is printed, `Cancelled.` is printed to standard error when it can be, and no process of any `gh` child's group remains
- **AND** with SIGINT instead the exit status is 130
