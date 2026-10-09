## Purpose

Answer "which of my local projects needs attention?" in one bounded, local and
read-only report: every project found within the configured roots, its Git
health and linked worktrees, findings by attention category, and at most one
gated next command per row, which is advice to review and never permission.

## ADDED Requirements

### Requirement: Overview discovers projects within configured roots only
`project overview [--root D]... [--attention] [--json] [--strict]` SHALL take
its roots from the repeatable `--root` option (source `argument`), else from
`PROJECTS_DIR` (source `environment`), else from the default projects
directories `~/projects` and `~/Projects` (source `default`). Each root SHALL
be expanded, canonicalised, deduplicated by canonical path and by device and
inode, and sorted by the bytes of its canonical path.

Discovery SHALL examine each root and its immediate entries only and SHALL
never recurse. A symbolic-link entry SHALL be resolved once, and one that
resolves to a directory already seen SHALL add nothing. A canonical directory
`D` SHALL be a candidate when a marker holds, the first matching marker
deciding the candidate and its kind, with no Git child:

| Marker | Candidate | Kind |
| --- | --- | --- |
| `D/<name of D>/family.yaml` is a file | `D/<name of D>` | `family-holder` |
| `D/project.yaml` is a file | `D` | `project-manifest` |
| `D/family.yaml` is a file | `D` | `family-holder` |
| `D/.git` exists as a file or a directory | `D` | `single` |
| `D/.project.json` is a file or `D/.devcontainer` is a directory | `D` | `single` |

A directory with no marker SHALL be neither a candidate nor reported. Candidate
paths SHALL be canonicalised, deduplicated by canonical path and by device and
inode, and sorted by their bytes before any candidate cap applies. The
overview SHALL NOT use the command's project lookup by name or its recursive
project snapshot, and SHALL NOT read a family's member list: a family holder
SHALL be exactly one row of kind `family-holder`, `relationships` SHALL be
`[]`, the holder SHALL receive Git probes only when its own directory is a Git
toplevel, and a member directory that is itself an immediate entry of a root
SHALL be an ordinary candidate with its own row.

A default root that does not exist SHALL be reported with state `absent` and
no error. An argument or environment root that does not exist, is not a
directory or cannot be listed SHALL be reported with state `unreadable` and a
`root-unreadable` scan error, and SHALL never cause exit status 2. A marker
check that fails with an error other than "no such entry" SHALL make that
directory an error row: `kind` null, status `error`, `findings` empty, one
`os-error` naming its path, and every Git-derived field null, sorted and
capped like any other row. When every root is `absent`, the human output SHALL
say that no projects directory was found and SHALL name `--root` and
`PROJECTS_DIR`.

#### Scenario: Independent clones and aliases
- **WHEN** clones of one origin exist at `atlas` under root A and at `atlas` under root B, root A also holds a symbolic link `atlas-link` to its `atlas`, and both A and B are given with `--root`
- **THEN** there are exactly two `atlas` rows whose `repository` `common_dir`, `dev` and `ino` differ
- **AND** the symbolic link adds no row, and each human row prints its absolute path

#### Scenario: Unreadable candidate directory
- **WHEN** one root holds candidates `alpha`, `locked` and `zeta`, `locked` has mode 000, and a second root given with `--root` cannot be listed
- **THEN** `locked` appears in its sorted position with `path` the candidate path, `name` `locked`, `kind` null, status `error`, `findings` empty, one `os-error` naming its path and every Git-derived field null
- **AND** `alpha` and `zeta` are complete, the second root adds a `root-unreadable` scan error, and the exit status is 1, never 2

#### Scenario: Family holder count, relationships and probe ownership
- **WHEN** a root holds `acme/acme/family.yaml` in a Git toplevel that declares members at `acme/web` and `acme/api`, plus an ordinary repository `tools`
- **THEN** there are exactly two rows, a `family-holder` at `acme/acme` and `tools`, `summary.projects` is 2, `relationships` is `[]`, no row and no Git child exists for `acme/web` or `acme/api`, and the holder's repository-wide probes run once and belong to its row
- **AND** without `acme/acme/.git` the holder row has null `repository`, `merge_target`, `git` and `worktrees`, status `ok`, no error and no Git child
- **AND** with `acme` itself as the root, `web` and `api` are ordinary rows of their own and `relationships` stays `[]`

#### Scenario: Every root is absent
- **WHEN** no `--root` is given, `PROJECTS_DIR` is unset, and neither default projects directory exists
- **THEN** both roots are reported `absent` with no scan error, the result is complete and the exit status is 0
- **AND** the human output says that no projects directory was found and names `--root` and `PROJECTS_DIR`

### Requirement: Overview groups worktrees by repository identity
Rows SHALL be keyed by repository identity `{root, common_dir, dev, ino}`,
never by a path string or a name: `common_dir` from the identity probe, `dev`
and `ino` from the no-follow `lstat` of the common directory that `Repository
inspection requires Git 2.36 and shares one evidence model` defines, and
`root` as this requirement names it. A linked worktree
that is also a candidate SHALL merge into its repository's row, independent
clones SHALL stay distinct, and every registered worktree, those outside
every root included, SHALL be listed under its repository, main worktree
first and then by path bytes, each with the identity `{path, dev, ino,
admin_id}` and the two-way registration check that requirement defines. The
candidate that reached a repository first SHALL mean the first in canonical
candidate order; where two spellings of one directory, such as a bind mount,
give one device and inode, the canonically first spelling SHALL win.

Each registered path SHALL fall into exactly one case: `lstat` fails with "no
such entry" or "not a directory" (`present: false`, no status probe); `lstat`
fails otherwise (`present: null`, no status probe, an `os-error`, and
`inspection-error` set directly); registration disagrees in either direction
(no status probe, `inspection-error` set directly, a `registration-mismatch`
finding and no error); otherwise the status probe runs in that worktree. No
probe SHALL run in a path the overview could not `lstat`.

Every repository SHALL first take the submodule test of `Clean resolves its
target Git-first`: when Git reports a superproject working tree for a
candidate that reached the repository, it is a submodule checkout, and
`repository.root` SHALL be null with an `unsupported-layout` repair finding of
severity error, a message naming a submodule checkout and no suggestion,
because that requirement refuses a submodule checkout. Otherwise a bare main
entry SHALL leave `repository.root` null, as that requirement refuses a bare
repository; and when the first registry record's path equals `common_dir`,
the main checkout is a gitfile checkout: `repository.root` SHALL be the
realpath of `core.worktree`, a relative value resolved against the git
directory, else the toplevel of a candidate whose identity probe reported
this `common_dir` and whose `.git` file names `common_dir` itself, else null
with an `unsupported-layout` repair finding of severity error, no suggestion
and the message remedy "set core.worktree or move the checkout". The
git-directory record SHALL NOT be a status-probed row; when `repository.root`
is named, the main worktree row SHALL name it and take its status probe there.
In the ordinary layout, where the first registry record is a worktree path,
`repository.root` SHALL be the main worktree: the identity probe's toplevel
when the candidate that reached the repository first is the main worktree
itself, and otherwise, that candidate being a linked worktree, the canonical
path of the first registry record, never the linked worktree's toplevel.

A main worktree path that does not exist SHALL give `repository.root: null`
and a `main-worktree-missing` repair finding of severity warning on that row
in place of its `stale-worktree` finding, with the message remedy "restore or
prune the main worktree by hand" and no suggestion; the repository-wide
probes SHALL then run in the candidate. A suggestion for a gitfile checkout
SHALL follow `Clean resolves its target Git-first`.

#### Scenario: One probe set per repository
- **WHEN** a repository has a main worktree and three linked worktrees, one of them an immediate entry of the root and one outside every root
- **THEN** there is one project row with four worktree rows, and the external worktree adds no project
- **AND** the identity probe, the registry, the single ref listing and the single merged-set query run once for the repository, each present row gets one status probe, and `probes.performed` equals one version check, plus one identity probe per Git candidate, plus three, plus four
- **AND** when the main worktree lies outside every root, so that a linked worktree reaches the repository first, `repository.root` is the canonical path of the first registry record, never that linked worktree's toplevel

#### Scenario: Present eligible external worktree
- **WHEN** `atlas` has a clean, pushed, merged linked worktree outside every root, whose branch has a commit of its own
- **THEN** it appears among `atlas`'s worktrees with `dev`, `ino` and a two-way-verified `admin_id`, classification `merged-removable` and a housekeeping finding
- **AND** the suggestion is `project clean <atlas root> --all-safe`, and the project count is unchanged

#### Scenario: Missing external worktree
- **WHEN** that external worktree's directory was deleted without `git worktree prune`
- **THEN** its row has `present: false`, classification `stale-worktree`, and a housekeeping warning suggesting the read-only `project clean <atlas root>`
- **AND** no probe runs in the missing path, and the exit status is 0, or 1 with `--strict`

#### Scenario: Unreadable external worktree
- **WHEN** the external worktree's parent directory is made unsearchable, so that `lstat` fails with a permission error
- **THEN** the worktree has `present: null` and classification `inspection-error`, the project row has an `os-error` and status `error`, the other rows are reported, and the exit status is 1
- **AND** when instead only that worktree's status probe fails, the row records `probe-failed` and is `inspection-error`

#### Scenario: A separate git directory
- **WHEN** a root holds the checkout of a repository created with `git init --separate-git-dir`, whose git directory has no `core.worktree`
- **THEN** `repository.root` is that checkout, its main worktree row is status-probed there and reports its dirty state, and the git-directory record is never status-probed
- **AND** when only a linked worktree of that repository is a candidate and its checkout is not, `repository.root` is null with an `unsupported-layout` repair finding of severity error, no suggestion, and the exit status 1

#### Scenario: A submodule checkout under a root
- **WHEN** an immediate entry of a root is the checkout of a submodule, whose `core.worktree` is relative to its git directory
- **THEN** its row has `repository.root: null` and an `unsupported-layout` repair finding of severity error whose message names a submodule checkout, the submodule test having decided before `core.worktree` was read, so that no `core.worktree` child ran for it
- **AND** it gets no clean suggestion, every finding's `suggestion_gate` is null, because `Clean resolves its target Git-first` refuses a submodule checkout, and the exit status is 1

#### Scenario: A deleted main worktree
- **WHEN** a repository's main worktree directory was deleted while a linked worktree under the root remains
- **THEN** the row has `repository.root: null`, the main worktree row has `present: false` and a `main-worktree-missing` repair warning, the repository-wide probes run in the linked worktree, and no clean suggestion is given

#### Scenario: A bare repository with a linked worktree
- **WHEN** a linked worktree of a bare repository is an immediate entry of a root
- **THEN** the row has `repository.root: null` and no clean suggestion, each finding that would have suggested one naming `target-not-repository-root` in `suggestion_gate`
- **AND** its repository-wide probes run in the common directory

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
defines.

The caps SHALL be 32 roots, 4,096 entries per root, 128 candidates and 512
worktree rows across the run, main worktrees included. They are provisional:
a measurement on a Linux filesystem may lower them before implementation,
and the values in force are always reported in `limits`. The root, candidate
and worktree-row caps SHALL apply after canonical sorting, and the entry cap
in listing order. Each cap that drops work SHALL be reported as a
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

### Requirement: Overview isolates one candidate's failure
Each candidate SHALL be collected inside one boundary that encloses, in order,
its marker checks, its identity probe, the manifest read at
`repository.root` (or at the candidate for a row without Git), its
repository's probes, merge-target resolution, the registration checks and
status probes of its worktree rows, and classification. Inside that boundary
a failure SHALL become data on that candidate's row and SHALL NOT change,
remove or reorder any other row or an earlier scan error:

| Raised or observed while collecting one candidate | Error code |
| --- | --- |
| a refusal from the manifest reader: unreadable, malformed, wrong-kind or over its size bound | `manifest-invalid` |
| a refusal from any other reused helper | `refused` |
| an operating-system error | `os-error` |
| output a reused helper could not decode | `undecodable-output` |
| any other exception, its message naming the exception class | `internal-error` |
| a Git child exits nonzero | `probe-failed` |
| a Git child or filesystem task reaches its 5 s limit | `probe-timeout` |
| the deadline ends a child or task, or prevents its start | `deadline-exceeded` |

Each error SHALL be `{code, message, path?}`, with a message of at most 200
characters (for a failed probe, the first line of Git's standard error) and
`path` naming the file or directory involved, `path_valid_utf8` beside it
whenever it is present. Evidence gathered before a failure SHALL be kept and
every field not established SHALL stay null; a row whose `errors` is non-empty
SHALL have status `error`, else `ok`. Every candidate entering collection SHALL
yield exactly one row or merge into exactly one existing repository row. The
boundary SHALL NOT catch an interrupt or an exit request. When the YAML library
the manifest reader needs is not installed, each row whose directory holds a
manifest SHALL carry a `manifest-invalid` error naming that cause, and the run
SHALL continue.

#### Scenario: One helper failure is isolated
- **WHEN** a root holds `alpha`, `ledger` and `zeta`, and `ledger/project.yaml` declares `kind: other`
- **THEN** `alpha` and `zeta` are complete, and `ledger` appears in its sorted position with status `error`, a `manifest-invalid` error, its repository identity retained, and null `merge_target`, `git` and `worktrees`
- **AND** the exit status is 1

#### Scenario: The YAML library is not installed
- **WHEN** the overview runs without the YAML library over a root holding `alpha`, which has only a `.git` directory, and `ledger`, which has a `project.yaml`
- **THEN** `ledger` carries a `manifest-invalid` error naming the missing library, `alpha` is complete with no error, and the exit status is 1

### Requirement: Overview reuses the cleanup classifier and merge target
The merge target SHALL be resolved in the order that `Clean resolves its
target Git-first` defines, both `origin/` strips included, from the manifest
read at `repository.root` (at the row's `path` when `repository.root` is
null) and the ref listing alone, spawning no Git child, and SHALL be recorded
as `merge_target: {name, source, sha}`, with `source` one of `manifest`,
`origin-head`, `main` or `master` and `sha` that branch's full object id from
the same listing. The merged set SHALL be computed at that `sha`. When the
manifest and `origin/HEAD` name different branches that both exist locally,
the manifest SHALL win and one informational `merge-target-conflict` finding
SHALL name both. When no candidate branch exists, `merge_target` SHALL be
null, the row SHALL carry a `no-merge-target` repair finding of severity
error with no suggestion, the classification ladder SHALL NOT run, and every
worktree's `classification` SHALL be null; when the ref listing failed or
timed out, the row SHALL record that error instead, absence not being
established.

Each worktree row SHALL be classified by the ladder that `Clean classifies
preservation and cleanup actions` defines, with its names, order and
recommendation text, fed from the overview's collected evidence and spawning
no probe of its own. The ladder SHALL run on a row only when the row is within
the cap, its presence is established, and the registry, ref listing and
merged set succeeded; otherwise `classification` SHALL be null, except for the
rows that requirement sets to `inspection-error` directly. For every row that
the report of `project clean <repository.root> --json` inspects, from the same
working directory and the same refs, the row's classification SHALL equal what
that report gives it; that report leaves the rows beyond its own row cap
uninspected, while the overview classifies rows up to its own worktree-row cap
per run.

#### Scenario: Manifest target
- **WHEN** a `project.yaml` sets `tracking_branch: origin/develop`, a local `develop` exists, and there is no `origin/HEAD`
- **THEN** `merge_target` is `develop` with source `manifest` and the object id of `refs/heads/develop`, and classification is relative to `develop`
- **AND** the merged set was computed at that object id, resolution spawned no Git child beyond the ref listing, and the name equals the merge target `project clean <root> --json` reports

#### Scenario: origin/HEAD target
- **WHEN** there is no manifest, `origin/HEAD` names `origin/trunk`, and local `trunk` and `main` exist
- **THEN** the target is `trunk` with source `origin-head` and the object id of `refs/heads/trunk`

#### Scenario: main target
- **WHEN** there is no manifest and no `origin/HEAD`, and local `main` and `master` exist
- **THEN** the target is `main` with source `main` and its object id

#### Scenario: master target
- **WHEN** only a local `master` exists
- **THEN** the target is `master` with source `master` and its object id

#### Scenario: Conflicting targets
- **WHEN** a manifest names `develop` and `origin/HEAD` names `main`, both existing locally
- **THEN** the target is `develop` with source `manifest`, and one informational `merge-target-conflict` finding names both branches
- **AND** the exit status is 0 when nothing else is found

#### Scenario: Missing target
- **WHEN** a manifest names an absent `release`, there is no `origin/HEAD`, and neither `main` nor `master` exists
- **THEN** `merge_target` is null, the row has a `no-merge-target` repair finding of severity error with no suggested command, every worktree's classification is null, and the exit status is 1
- **AND** on the same fixture `project clean <root> --all-safe` refuses with exit status 2 before any mutation

#### Scenario: Every protected classifier
- **WHEN** one repository's worktrees are classified `protected-default`, `dirty`, `ignored-local-files`, `detached`, `unpublished`, `remote-gone`, `diverged`, `remote-ahead`, `unpushed`, `merged-current` and `pushed-unmerged`, plus one gate-passing `merged-removable`, a second repository holds an `inspection-error` worktree whose corrupted index makes its status probe fail, and the overview runs from inside the `merged-current` worktree
- **THEN** every classification equals what `project clean <root> --json` reports from the same directory, and each finding has the category and severity of the attention table
- **AND** the only housekeeping finding and the only `--all-safe` suggestion belong to the `merged-removable` worktree, and no other worktree appears in the `selected` list of the batch preview that suggestion runs

### Requirement: Overview reports findings by attention category
Every finding SHALL carry exactly one code, category and severity from this
table, the complete list for schema version 1, and the suggested command it
names, subject to the gates of `Overview suggests only gated clean commands`
and to `Overview reports default-branch health`:

| Code | Category | Severity | Evidence source | Suggested command |
| --- | --- | --- | --- | --- |
| `inspection-error` | repair | error | `worktree-status` | none |
| `review-required` | repair | warning | `local-refs` | read-only clean |
| `no-merge-target` | repair | error | `local-refs` | none |
| `registration-mismatch` | repair | warning | `worktree-registry` | none |
| `unsupported-path-bytes` | repair | warning | `filesystem` | none |
| `unsupported-layout` | repair | error | `worktree-registry` | none |
| `main-worktree-missing` | repair | warning | `worktree-registry` | none |
| `dirty` | preserve | warning | `worktree-status` | read-only clean |
| `ignored-local-files` | preserve | warning | `worktree-status` | read-only clean |
| `detached` | preserve | warning | `worktree-registry` | read-only clean |
| `unpublished` | preserve | warning | `local-refs` | read-only clean |
| `remote-gone` | preserve | warning | `local-refs` | read-only clean |
| `diverged` | preserve | warning | `local-refs` | read-only clean |
| `unpushed` | preserve | warning | `local-refs` | read-only clean |
| `merged-removable` | housekeeping | info | `local-refs` | `--all-safe`, or read-only clean under a gate |
| `stale-worktree` | housekeeping | warning | `worktree-registry` | read-only clean |
| `pushed-unmerged` | informational | info | `local-refs` | none |
| `remote-ahead` | informational | info | `local-refs` | none |
| `merged-current` | informational | info | `local-refs` | none |
| `main-worktree` | informational | info | `worktree-registry` | none |
| `locked-worktree` | informational | info | `worktree-registry` | read-only clean |
| `merge-target-conflict` | informational | info | `manifest` | none |

A finding that reports a worktree's classification SHALL carry the ladder's
recommendation text as its `message`, and any other finding a fixed sentence. A
worktree whose upstream's remote-tracking ref is gone and whose branch tip the
merged set shows to be an ancestor of the merge target SHALL be classified as
`Clean classifies preservation and cleanup actions` classifies it,
`merged-removable` or `merged-current`, with that class's finding, message and
suggestion, spawning no further probe; only such a worktree whose tip is not an
ancestor SHALL be `remote-gone`, with the ladder's own recommendation and the
read-only command as its only suggestion. `protected-default` SHALL produce no
finding by itself, apart from those of
`Overview reports default-branch health`. Row errors and scan errors SHALL
NOT be findings, and SHALL display in the repair category.

A finding of severity `error` SHALL make the exit status 1; `warning` SHALL do
so only under `--strict`; `info` SHALL never affect it. `--attention` SHALL
show every scan error, every row with status `error` and every row with at
least one repair, preserve or housekeeping finding, and SHALL hide
informational findings within a shown row. It SHALL change only the display:
never what is collected, the summary counts, the JSON document or the exit
status; `--attention --json` SHALL print the full envelope.

#### Scenario: Attention filter per category
- **WHEN** four projects have as their only findings `pushed-unmerged`, `unpushed`, `merged-removable` and `no-merge-target`, and `project overview` and `project overview --attention` each run with and without `--json`
- **THEN** `--attention` hides the informational-only project and shows the other three under their categories, the two JSON documents are identical apart from their timestamps, and every run exits 1
- **AND** without the repair project every run exits 0, and with `--strict` every run exits 1 because of the preserve warning

#### Scenario: A merged worktree whose upstream was deleted
- **WHEN** a clean linked worktree's branch, with a commit of its own, is an ancestor of the merge target and its upstream branch was deleted and pruned
- **THEN** it is classified `merged-removable`, as `project clean <root> --json` classifies it, with the housekeeping finding whose message is the ladder's `merged-removable` recommendation, and suggests `project clean <root> --all-safe`
- **AND** no Git child beyond the shared probe set ran for it, and a worktree whose upstream branch was deleted and pruned and whose tip is not an ancestor is classified `remote-gone`, with a preserve warning carrying the ladder's own `remote-gone` recommendation, and suggests only the read-only `project clean <root>`

### Requirement: Overview suggests only gated clean commands
A suggestion SHALL be an argv array, exactly `["project", "clean", "<root>",
"--all-safe"]` or `["project", "clean", "<root>"]`, where `<root>` is the
absolute canonical `repository.root`; it SHALL never name a project by bare
name and never include `--apply` or `--yes`. A row whose `repository.root` is
null, or whose root or common directory is not valid UTF-8, SHALL get no clean
suggestion, the latter carrying an `unsupported-path-bytes` finding instead,
as `Clean reports every path exactly or excludes it` refuses either. A row's
`suggested_command` SHALL be the `--all-safe` form when one of its findings
suggests it, else the read-only form when any finding suggests it, else null.

The `--all-safe` form SHALL be suggested only for a worktree that
`Clean classifies preservation and cleanup actions` classifies
`merged-removable` and that passes the gates of
`Clean previews and applies a batch of eligible worktree removals in one repository`
the overview can evaluate from its own evidence, in that requirement's order:
`main-worktree`, `unsupported-path-bytes`, `registration-mismatch` and
`locked-worktree`, whose first failure replaces the housekeeping finding with
its own while the classification stays; then `unstarted-branch` or
`reflog-unavailable`, mirroring that requirement's gate. The branch's reflog,
`logs/refs/heads/<branch>` under `common_dir`, SHALL be read for every row the
gate checks by one bounded filesystem read of at most 64 KiB, never by a Git
child. Its anchor SHALL be its last surviving entry whose old object is all
zeros, a creation written by any command, or whose message begins `branch:
Created from` or `branch: Reset to`; a movement SHALL be an entry after the
anchor, or any entry when no anchor survives, whose old and new objects are
non-zero and differ. An entry whose old object is all zeros SHALL never be a
movement, nor SHALL an entry whose old and new objects are equal, as a rename
writes. A branch whose last reflog entry's new object
differs from its current head SHALL be `reflog-unavailable`, this test first;
otherwise a branch with a movement SHALL pass the gate, its head equal to the
merge-target object id or not, and a branch whose anchor survives with no
movement after it, the anchor's new object equal to its current head, SHALL be
`unstarted-branch`. One outcome rule SHALL govern the read: a reflog that is
missing (`ENOENT` or `ENOTDIR`), empty (0 bytes) or read to its 64 KiB bound,
or whose surviving entries cannot decide, no anchor and no movement surviving
included, SHALL make that row `reflog-unavailable`; any other operating-system
error on the read SHALL record an `os-error` and make that row
`inspection-error`, as any failed row probe does; and a read not finished
within the filesystem budget SHALL leave that row unprobed for the gate, as
for every other filesystem read, recording `probe-timeout` or
`deadline-exceeded`. Either code SHALL keep the `merged-removable` finding
with the read-only suggestion. The index gates SHALL remain exclusions only the
batch applies. The `--all-safe` form SHALL also be withheld for every worktree
of a repository whose batch plan would be refused as `inspection-incomplete`
(any worktree row is `inspection-error`, or is unprobed for this gate because
its reflog read did not finish) or `inspect-cap` (more worktree rows
than the batch's row cap), as
`Clean bounds its Git work and reports omitted work` defines, each computed
from the overview's own evidence, and for a repository with any row the
overview's own cap or deadline left unclassified; those findings SHALL suggest
the read-only form. A repository with more worktree rows than the report's row
cap SHALL have its read-only suggestions limited by `inspect-cap`. When more
`merged-removable` worktrees keep the `--all-safe` form than the batch's target
limit, each SHALL keep it, limited by `target-cap`.

Each finding SHALL carry `suggestion_gate`, null unless a gate withheld or
limited its suggestion, else the first applicable code in this order, and
`suggestion_gate_rows`, the repository's worktree-row count when the code is
`inspect-cap`, else null. The finding's `message` and the human text SHALL
carry the code's fixed remedy, naming the batch's row cap, the report's row
cap and the batch's target limit with the numbers taken at run time from the
shared constants that `Clean bounds its Git work and reports omitted work`
defines, as `limits` reports them, never from a clean plan:

| Code | Effect | Fixed remedy |
| --- | --- | --- |
| `target-not-repository-root` | withholds every clean suggestion (a bare repository) | run project clean from the main worktree root |
| `unsupported-path-bytes` | withholds every clean suggestion (a root or common directory that is not valid UTF-8) | rename the path to valid UTF-8 |
| `inspection-incomplete` | withholds `--all-safe` (an `inspection-error` row, or a row whose reflog read did not finish) | repair the inspection-error rows, or re-run for the rows left unprobed, first |
| `inspect-cap` | withholds `--all-safe` over the batch's row cap | N rows exceed the batch's row cap of M; remove explicitly |
| `inspect-cap` | limits the read-only form over the report's row cap | N rows exceed the report's row cap of M; the report would be incomplete |
| `scan-limit` | withholds `--all-safe` for a row left unprobed by a cap | re-run with --root <repository parent> |
| `deadline-exceeded` | withholds `--all-safe` for a row left unprobed by the deadline | re-run with --root <repository parent> |
| `unstarted-branch` | withholds `--all-safe` for that worktree (an anchor with no movement after it) | no commit was made on this branch here since it was created; review, then git worktree remove yourself |
| `reflog-unavailable` | withholds `--all-safe` for that worktree (a reflog that cannot decide) | the branch's reflog is missing, expired or undecidable; review, then git worktree remove yourself |
| `target-cap` | limits `--all-safe` | limited to the batch's target limit of M per run; re-run to drain the backlog |

A root left null by `unsupported-layout` or `main-worktree-missing` SHALL
carry no gate code; that finding's message carries the remedy. `project
clean` SHALL remain free to recompute, show and confirm its own plan and to
exclude a suggested worktree.

#### Scenario: Gated merged worktrees
- **WHEN** four worktrees the ladder would classify `merged-removable` are one locked with `git worktree lock`, one whose `.git` file names another admin directory, one whose path contains the byte `0xFF`, and the main worktree checked out on a merged non-target branch while the overview runs elsewhere
- **THEN** the locked one has a `locked-worktree` finding suggesting the read-only `project clean <root>`, the mismatched one gets no status probe and is `inspection-error` with a `registration-mismatch` finding, the non-UTF-8 one has `unsupported-path-bytes`, the main worktree has `main-worktree`, and none produces a housekeeping finding
- **AND** a fifth, gate-passing `merged-removable` worktree in the same repository keeps its housekeeping finding with the read-only suggestion and `suggestion_gate: "inspection-incomplete"`, and the row suggests the read-only form
- **AND** after `git worktree repair` fixes the mismatched registration, the `--all-safe` suggestion returns and the batch preview selects the repaired worktree, whose branch has a commit of its own, and the fifth

#### Scenario: Canonical identity through the handoff
- **WHEN** projects named `atlas` under two roots each have a `merged-removable` worktree whose branch has a commit of its own
- **THEN** the rows suggest `["project", "clean", "<first atlas root>", "--all-safe"]` and `["project", "clean", "<second atlas root>", "--all-safe"]`, and each, when run, resolves its path Git-first to a plan whose `repository` and `merge_target` equal that row's
- **AND** for an assembly root with a `project.yaml` whose immediate-entry leg `api` is its own repository with one dirty and one `merged-removable` worktree whose branch has a commit of its own, the leg's row suggests `--all-safe` on the leg's root, its `dirty` finding suggests the read-only form, and either reports `root` equal to the leg
- **AND** the same command with a linked-worktree path or a subdirectory instead of the root is refused by `project clean` with exit status 2 and `target-not-repository-root` before any mutation

#### Scenario: More eligible worktrees than the batch's target limit
- **WHEN** one repository has 17 gate-passing `merged-removable` worktrees and the batch's target limit is 16
- **THEN** each of the 17 findings and the row suggest `--all-safe` with `suggestion_gate: "target-cap"` and a message ending "limited to the batch's target limit of 16 per run; re-run to drain the backlog"
- **AND** the human `next` line ends `(limited: ...)` with that remedy, and the exit status is 0

#### Scenario: The two inspect-cap bands
- **WHEN** one repository has 130 worktree rows, with the batch's row cap at 128 and the report's at 256, including a gate-passing `merged-removable` worktree and a `dirty` one
- **THEN** the `merged-removable` finding suggests the read-only form with `suggestion_gate: "inspect-cap"`, `suggestion_gate_rows: 130` and the message remedy "130 rows exceed the batch's row cap of 128; remove explicitly", and the `dirty` finding's read-only suggestion carries no gate
- **AND** in a repository with 260 worktree rows every read-only suggestion carries `suggestion_gate: "inspect-cap"`, `suggestion_gate_rows: 260` and the remedy "260 rows exceed the report's row cap of 256; the report would be incomplete"

#### Scenario: A row left unprobed closes the repository gate
- **WHEN** the worktree-row cap leaves one row of a repository unclassified while another of its worktrees is gate-passing `merged-removable`
- **THEN** that finding suggests the read-only form with `suggestion_gate: "scan-limit"` and the remedy "re-run with --root <repository parent>", naming the repository's parent directory

#### Scenario: An unstarted branch
- **WHEN** a linked worktree was created with a new branch at the merge target's tip and published with `git push -u`, with no commit of its own, so that its reflog holds only its `branch: Created from` entry
- **THEN** it keeps its `merged-removable` finding, which suggests only the read-only form with `suggestion_gate: "unstarted-branch"` and a message ending "no commit was made on this branch here since it was created; review, then git worktree remove yourself"
- **AND** no `--all-safe` suggestion is given for that repository on its account, and after `git branch -m`, whose entry has equal old and new objects, it is still `unstarted-branch`
- **AND** a branch with commits of its own, merged into the merge target and then reset to the target's tip by `git worktree add -B <branch> <path> <merge target>` with no commit after it, anchors at that `branch: Reset to` entry and is `unstarted-branch` too, its earlier commits not counting as movement
- **AND** a branch created by `git fetch origin feat:f1` while `origin/feat` sits at the merge target's tip, given an upstream by `git branch -u origin/feat f1`, which writes no reflog entry, then checked out in a linked worktree with no commit, anchors at that fetch entry, whose old object is all zeros, and is `unstarted-branch` too, never passing as a movement
- **AND** a branch given one commit and then fast-forward merged into the merge target, so that its head equals the target's tip while its reflog records that commit after its anchor, keeps the `--all-safe` suggestion with no gate

#### Scenario: A branch whose reflog cannot decide
- **WHEN** one gate-passing `merged-removable` worktree's branch has no reflog file, another's reflog file is empty, a third's reflog keeps only a rename entry after `git reflog expire` removed its creation and commit entries, and a fourth's branch, whose reflog records a commit of its own, was then moved to another merged commit by writing its ref directly, so that its last entry's new object differs from its head
- **THEN** each keeps its `merged-removable` finding, which suggests only the read-only form with `suggestion_gate: "reflog-unavailable"` and a message ending "the branch's reflog is missing, expired or undecidable; review, then git worktree remove yourself"
- **AND** no Git child is started to read any of the four reflogs, and `project clean <root> --all-safe` excludes all four as `reflog-unavailable`
- **AND** in a second repository, where one gate-passing worktree's reflog cannot be read for a permission error, that worktree records an `os-error` and is `inspection-error`, and another gate-passing `merged-removable` worktree there suggests only the read-only form with `suggestion_gate: "inspection-incomplete"`

### Requirement: Overview prints a versioned JSON envelope
`--json` SHALL print exactly one JSON document with `schema_version: 1` and
exactly these fields, every one always present:

- envelope: `schema_version`; `observed_at`, the collection start; `roots`, in
  canonical byte order; `limits`, of integers, keyed `roots`, `candidates`,
  `worktree_rows`, `root_entries`, `ignored_entries`, `status_records`,
  `ignored_samples`, `batch_row_cap`, `report_row_cap` and `targets`, the
  last three read from the shared constants that `Clean bounds its Git work
  and reports omitted work` defines, never from a clean plan, whose own
  `limits.worktree_rows` is only its mode's row cap, `targets` carrying the
  name a clean plan's `limits` gives the same constant; `budget`, of integers,
  keyed `probe_timeout_seconds`, `invocation_timeout_seconds` and
  `probe_concurrency`; `probes`; `projects`, sorted by the bytes of `path`;
  `relationships`, always `[]`; `summary`; `completeness`, `complete` or
  `incomplete`; `scan_errors`, in canonical collection order;
- root object: `path`, `path_valid_utf8`, `source` (`argument`,
  `environment` or `default`), `state` (`listed`, `truncated`, `absent`,
  `unreadable` or `omitted`) and `entries`, null when the root was not listed;
- project row: `name` (the manifest name, else the directory name), `path`,
  `path_valid_utf8`, `kind`, `repository`, `merge_target`, `git`,
  `worktrees`, `findings`, `suggested_command`, `status` and `errors`;
- `repository`: `root`, `common_dir`, `dev`, `ino`, `root_valid_utf8` and
  `common_dir_valid_utf8`;
- `git`, for the checkout at `path`: `branch`, `head`, `dirty`, `upstream`,
  `ahead`, `behind` and `tracking_freshness`, the last never null;
- worktree row: `path`, `path_valid_utf8`, `dev`, `ino`, `admin_id`,
  `present`, `locked`, `prunable`, `current`, `branch` (`"detached"` for a
  detached head), `head`, `upstream`, `upstream_oid`, `ahead`, `behind`,
  `remote_present`, `merged_into_target`, `dirty`, `ignored_files`,
  `ignored_files_truncated`, `ignored_samples` and `classification`, each
  `ignored_samples` entry being an object `{path, path_valid_utf8}` whose
  `path` is relative to its worktree;
- finding: `code`, `category`, `severity`, `checkout`
  (`{path, path_valid_utf8, dev, ino, admin_id}`, or null for a
  repository-level finding), `evidence_source`, `message`, `observed_at`,
  `suggested_command`, `suggestion_gate` and `suggestion_gate_rows`;
- `summary`: `projects`, `repositories`, `worktrees`, `errors` (row errors
  plus scan errors) and `findings` counted by category, over the whole
  collection whatever `--attention` shows;
- error object: `code`, `message` and an optional `path` with
  `path_valid_utf8` beside it, with `limit` and `omitted` added on
  `scan-limit` and `deadline-exceeded` errors.

Integers SHALL be JSON integers, object ids full lowercase hexadecimal, times
RFC 3339 UTC with a `Z` suffix, and durations integer seconds in fields ending
`_seconds`. `null` SHALL mean unknown or not established and never stand for
`false`, `0` or an empty list, and an empty `findings` on an error row SHALL
mean that no finding was computed. `completeness` SHALL be `incomplete`
exactly when `scan_errors` is non-empty or any row has status `error`. Enums
SHALL be closed within a version; adding a field or an enum value is
additive, and renaming or removing a field or changing its type or meaning
SHALL increment `schema_version`.

Every path SHALL be parsed and emitted as
`Repository inspection requires Git 2.36 and shares one evidence model` and
`Clean reports every path exactly or excludes it` define: exactly when it is
valid UTF-8, with every code point of Unicode general category Cc, Cf, Zl or
Zp, as the running interpreter's `unicodedata.category` reports it (control,
format, bidirectional, line and paragraph separator characters such as U+0007,
U+200B, U+202E and U+2028), escaped by JSON, and otherwise escaped. Every
serialized path SHALL carry its own validity flag: `path_valid_utf8` beside
each `path`, and `root_valid_utf8` and `common_dir_valid_utf8` in `repository`,
each false exactly when that path is not valid UTF-8 and null only beside a
null path. A worktree path, root or common directory that is not valid UTF-8
SHALL get an `unsupported-path-bytes` finding and contribute to no clean
suggestion. Human output SHALL print a path holding a code point of those
categories or an undecodable byte in the `$'...'` form that requirement
defines, each such code point written as `\uXXXX`, or as `\UXXXXXXXX` above
U+FFFF, as the tag characters need. Under `--json`, an exit status 2 other than
an argument error SHALL print only `{"error": "<message>", "code": "<code>"}`,
the code being `git-too-old`, `git-unavailable`, `refused`, `os-error` or
`internal-error`; an argument error SHALL print the command-line parser's usage
message on standard error and no JSON.

#### Scenario: Control and format characters in paths
- **WHEN** a repository's directory name contains a newline and its linked worktrees' names contain a tab, U+0007, U+202E and U+200B
- **THEN** each JSON `path`, findings' `checkout` paths included, and `repository.root` are exact, with the escapes `\n`, `\t`, `\u0007`, `\u202e` and `\u200b`, every `path_valid_utf8` and `root_valid_utf8` is true, and each worktree is classified from its real state rather than as `stale-worktree`
- **AND** the human output prints each such path in `$'...'` form, the newline as `\u000a`, the tab as `\u0009`, U+0007 as `\u0007`, U+202E as `\u202e` and U+200B as `\u200b`, and the printed suggestion, pasted into bash under a UTF-8 locale, names the same repository root

#### Scenario: Non-UTF-8 path
- **WHEN** a clean merged worktree's name contains the byte `0xFF`
- **THEN** the overview completes, the worktree's `path` and its finding's `checkout.path` show the byte as `\xff`, each with `path_valid_utf8: false`, the row has an `unsupported-path-bytes` repair finding, and the worktree contributes nothing to the `--all-safe` suggestion
- **AND** `project clean <root> --all-safe` excludes it with reason `unsupported-path-bytes`
- **AND** when another worktree holds two ignored files, one named with the byte `0xFF` and one named with the four characters `\xff`, its two `ignored_samples` entries have the same decoded `path` and differ only in `path_valid_utf8`, false and true

#### Scenario: Non-UTF-8 common directory
- **WHEN** a root holds the checkout of a repository made with `git init --separate-git-dir` into a git directory whose name contains the byte `0xFF`, and the repository has a dirty linked worktree
- **THEN** `repository.common_dir` shows the byte as `\xff` with `common_dir_valid_utf8: false` while `root_valid_utf8` is true, and the row has a repository-level `unsupported-path-bytes` repair finding
- **AND** neither the row nor any finding carries a clean suggestion, each finding that would have suggested one naming `unsupported-path-bytes` in `suggestion_gate`, and `project clean <root>` refuses with `unsupported-path-bytes` and exit status 2

#### Scenario: An argument error under --json
- **WHEN** `project overview --json --bogus` runs
- **THEN** standard output is empty, standard error carries the usage message, and the exit status is 2

#### Scenario: Every envelope field is present
- **WHEN** `project overview --json` runs over a fixture with one healthy repository holding one `merged-removable` worktree and one unreadable root
- **THEN** the document carries exactly the fields listed above with their types, `limits` includes `batch_row_cap`, `report_row_cap` and `targets` equal to the shared constants that `Clean bounds its Git work and reports omitted work` defines, read without building a clean plan, every finding carries `suggestion_gate` and `suggestion_gate_rows`, every `path` has `path_valid_utf8` beside it, `repository` carries `root_valid_utf8` and `common_dir_valid_utf8`, and `completeness` is `incomplete`

#### Scenario: An internal error outside the collector under --json
- **WHEN** an exception is raised outside the per-candidate boundary during a `--json` run
- **THEN** standard output holds only `{"error": "<message>", "code": "internal-error"}`, the message naming the exception class, no traceback is printed, and the exit status is 2

### Requirement: Overview is local and read-only
The overview SHALL open no network connection and SHALL make no filesystem or
Git mutation: no fetch, pull, reset, bootstrap, validator run or file write;
no worktree created, pruned, repaired, locked or unlocked; and no index
rewritten, every Git child running read-only as `Repository inspection
requires Git 2.36 and shares one evidence model` defines. It SHALL read no
credential file and no profile data the scan does not need, and SHALL keep no
state beyond one invocation. Ahead, behind and merge evidence SHALL be
observations as of the last fetch, and both outputs SHALL say so.

#### Scenario: Local and read-only
- **WHEN** the overview runs with default options over any fixture of this capability, with networking disabled for the process
- **THEN** it opens no network connection, and the before and after snapshots of `git for-each-ref`, `git worktree list --porcelain -z`, each checkout's status, each index file's modification time and the directory tree under every root are identical
- **AND** the JSON preserves severity, freshness, unknown values and completeness, and a complete scan that finds no project says so and exits 0

### Requirement: Overview reports default-branch health
For a checkout that `Clean classifies preservation and cleanup actions`
classifies `protected-default`, the overview SHALL keep that classification
and add, from evidence it already holds and with no further probe, every
finding that applies rather than only the first: `dirty` (preserve, warning)
when the checkout is dirty; and at most one of `unpublished` (preserve,
warning) when no upstream is configured and the ref listing holds a remote
copy of the merge target, with the message "merge-target branch has no
upstream; local commits are unverified"; `remote-gone` (preserve, warning)
when its upstream is gone; `diverged` (preserve, warning) when it is both
ahead of and behind its upstream; `unpushed` (preserve, warning) when it is
only ahead; or `remote-ahead` (informational, info) when it is only behind.
Each of these findings SHALL carry `suggested_command: null` and SHALL NOT
set the row's `suggested_command`. A merge-target branch with no remote copy
at all SHALL raise no `unpublished` finding, and ignored files in that
checkout SHALL raise no finding. A merge-target checkout whose status probe
failed, timed out or was cut by the deadline SHALL be `inspection-error`, as
`Clean classifies preservation and cleanup actions` defines, with that code's
repair finding of severity error, and SHALL get none of these findings.

#### Scenario: A default branch pushed without an upstream
- **WHEN** `main` was pushed with `git push origin main`, without `-u`, and then given two local commits
- **THEN** its checkout stays `protected-default` and has an `unpublished` preserve warning with the message "merge-target branch has no upstream; local commits are unverified" and no suggested command
- **AND** `project overview --attention` shows that row, and the exit status is 0, or 1 with `--strict`

#### Scenario: A repository with no remote
- **WHEN** a repository has no remote and local commits on `main`, and nothing else to report
- **THEN** its checkout has no `unpublished` finding and no other finding, `--attention` does not show the row, and the exit status is 0 with or without `--strict`

#### Scenario: A dirty default branch ahead of its upstream
- **WHEN** the checkout of `main` is dirty and 3 commits ahead of its upstream
- **THEN** it stays `protected-default` and carries both a `dirty` and an `unpushed` preserve warning, each with no suggested command

#### Scenario: A failed status probe on the default branch
- **WHEN** the status probe of the checkout of `main` fails
- **THEN** that row is `inspection-error` with a repair finding of severity error and the `probe-failed` error, it carries none of the default-branch findings, and the exit status is 1

### Requirement: Overview exits by completeness and severity
The overview SHALL exit with status 0 when `completeness` is `complete` and no
finding has severity `error`; 1 when the result is incomplete, a finding has
severity `error`, or `--strict` is given and a finding has severity
`warning`; 2 for an invalid invocation, an exception raised outside the
per-candidate boundary, or a Git refusal; and 130, 143 or 129 on SIGINT,
SIGTERM or SIGHUP. On 0 or 1 the full result SHALL be printed. A root problem
SHALL never cause status 2.

It SHALL run the version check of `Repository inspection requires Git 2.36
and shares one evidence model` once per invocation, after the deadline is
set and before any root is listed, and SHALL refuse Git older than 2.36 with
`git-too-old`, and a missing `git`, a failed or timed-out version child or an
unparseable version with `git-unavailable`, each with status 2, a message
naming the 2.36 minimum, and no other Git child; such a refusal SHALL never be
an incompleteness. On SIGINT, SIGTERM or SIGHUP it SHALL stop scheduling,
terminate and reap every child as `Overview bounds its work and reports what
it omitted` states, abandoning one still unreaped 2 s after SIGKILL, print no
result document, print `Cancelled.` to standard error on a best-effort basis,
and exit with that signal's status, which SHALL take precedence over 1. Its
main thread SHALL never block in an unbounded filesystem call.

#### Scenario: Git too old
- **WHEN** `git` reports version 2.34.1
- **THEN** the overview exits 2 with code `git-too-old` and a message naming the 2.36 minimum, before listing any root or starting any other Git child
- **AND** under `--json` it prints only `{"error": "<message>", "code": "git-too-old"}`

#### Scenario: Git unavailable
- **WHEN** no `git` is on `PATH`
- **THEN** the overview exits 2 with code `git-unavailable` before listing any root, and under `--json` prints only the error object with that code

#### Scenario: SIGTERM or SIGHUP during collection
- **WHEN** SIGTERM is sent while, at probe concurrency 4, one Git child is hung and another is writing a large output
- **THEN** the exit status is 143, no result document is printed, `Cancelled.` is printed to standard error when it can be, and every child's process group is gone
- **AND** with SIGHUP instead the exit status is 129

#### Scenario: SIGINT during collection
- **WHEN** SIGINT is sent while children are running and a finding of severity error has already been collected
- **THEN** every in-flight child is terminated and reaped, no result document is printed, `Cancelled.` goes to standard error, and the exit status is 130, not 1

### Requirement: Overview renders a readable human report
Without `--json`, the overview SHALL print to standard output, for each shown
row: one header line with the name and the absolute path; one line per shown
finding with its category, code and message, followed by the worktree path for
a worktree's finding; and one `next` line carrying the row's suggested command,
printed with shell quoting or in the `$'...'` form, followed by
`(withheld: <remedy>)` when a gate removed the `--all-safe` form or every clean
suggestion (`target-not-repository-root`, `unsupported-path-bytes`,
`inspection-incomplete`, `inspect-cap` over the batch's row cap, an unprobed
row, `unstarted-branch`, `reflog-unavailable`), or `(limited: <remedy>)` when a
suggestion is given but capped (`target-cap`, or `inspect-cap` over the
report's row cap on the read-only command). Row errors SHALL display in the
repair category. One `Incomplete:` line SHALL follow per scan error. The
summary line SHALL always be printed, even under `--attention` when no row is
shown, where it SHALL say that nothing needs attention, with the counts of
projects, errors and findings by category, and SHALL state that findings
reflect local refs as of the last fetch. When standard error is a terminal, and
only then, the overview SHALL write one `Scanning N roots...` line to standard
error before listing.

#### Scenario: Nothing needs attention
- **WHEN** `project overview --attention` runs over projects whose only findings are informational
- **THEN** no row is shown, and the summary line says that nothing needs attention, gives the counts, and states that findings reflect local refs as of the last fetch
- **AND** the exit status is 0

#### Scenario: A gated suggestion
- **WHEN** a repository holds a gate-passing `merged-removable` worktree and another worktree whose status probe failed
- **THEN** the row's `next` line carries `project clean <root>` followed by `(withheld: repair the inspection-error rows, or re-run for the rows left unprobed, first)`
- **AND** the finding lines show the repair finding and the housekeeping finding with their worktree paths

#### Scenario: The scanning notice
- **WHEN** the overview runs with standard error on a terminal, and again with standard error on a pipe
- **THEN** the first run writes one `Scanning N roots...` line to standard error before listing, and the second writes none
- **AND** standard output is identical in both runs
