## MODIFIED Requirements

### Requirement: Inspect and diagnose
Status and doctor SHALL support human and JSON reports for single repositories,
project manifests, families, worktrees and local tooling. Missing or malformed
state SHALL be visible; inspection SHALL never fetch, reset, or bootstrap.

Status and doctor SHALL inspect Git repositories through the evidence model that
"Repository inspection requires Git 2.36 and shares one evidence model" defines,
and SHALL NOT refuse for Git's version, for a relative configuration path or for
a repository they cannot inspect. Doctor SHALL report a Git older than 2.36, or
a `git` that is missing or unusable, as an `error` check row naming
`git-too-old` or `git-unavailable`, and a configuration path that fails that
evidence model's test as an `error` check row naming `relative-config-path`,
keeping its exit status for error rows; status SHALL mark each repository root,
leg or worktree row it cannot inspect `inspection-error`. A directory with no
`.git` SHALL keep `present: false` and needs no Git version check. A root or leg
whose state cannot be established, a failed or timed-out status probe included,
SHALL be reported as a row-level `inspection-error` and SHALL NOT end the
command with exit status 2.

In JSON, which stays unversioned for status and doctor, a root or leg state that
could not be inspected SHALL carry `classification: "inspection-error"` and an
`errors` list of `{code, message, path?, path_valid_utf8?, reason?}` objects,
the fields that worktree rows carry, and each of its values that was not
established SHALL be null. Doctor SHALL render as an `error` check row, never as
`ok`, every null that means "not established": a `present` that is null, a
`dirty` left null by a failed or timed-out probe, and any row classified
`inspection-error`. Doctor SHALL NOT render as an error a null that means
"none": `upstream`, `ahead` and `behind` for a branch with no upstream, and
`merged_into_target` for a detached head. For a branch whose configured
upstream's remote-tracking ref was deleted, a row's `upstream` SHALL be the
configured short name and its `ahead` and `behind` null. Each path value in that
JSON SHALL be written by the JSON rule that "Clean reports every path exactly or
excludes it" states, with `path_valid_utf8` beside every `path`, in root, leg
and worktree rows, `errors` entries and `ignored_samples` entries alike, and
with `root_valid_utf8` beside the report's top-level `root` and the `root` of
each family member it nests.

#### Scenario: Missing leg
- **WHEN** a project's declared leg has no checkout
- **THEN** doctor reports an actionable failure and returns nonzero.

#### Scenario: Git older than 2.36 in status and doctor
- **WHEN** status and doctor run on a project with Git 2.35 first on PATH
- **THEN** doctor reports `git-too-old` as an `error` check row and exits 1, and status marks the repository root `inspection-error` and exits 0
- **AND** neither refuses, and a directory with no `.git` still reads `present: false`

#### Scenario: No git on PATH
- **WHEN** doctor runs with no `git` on PATH
- **THEN** it reports `git-unavailable` as an `error` check row and exits 1

#### Scenario: Not established is an error, none is not
- **WHEN** doctor runs on a fresh project with no remote, so that its `upstream`, `ahead` and `behind` are null
- **THEN** none of those nulls is an error, and doctor passes
- **AND** when a leg's `dirty` is null because its status probe failed, doctor reports an `error` check row for that leg and exits 1

#### Scenario: A failed root status is reported
- **WHEN** the status probe of a project's root repository fails
- **THEN** status and doctor report the root with `classification: "inspection-error"`, its `errors` and a null `dirty`, instead of refusing with exit 2, and doctor exits 1

#### Scenario: A deleted upstream in status and doctor
- **WHEN** a checkout's branch has a configured upstream whose remote-tracking ref was deleted
- **THEN** its status and doctor row's `upstream` is the configured short name, such as `origin/<branch>`, and its `ahead` and `behind` are null, where before this change `upstream` was null

### Requirement: Explicit maintenance
Update SHALL report local tracking state and named owning commands by default.
Applying an update SHALL require a component and confirmation, preserve failures,
and reject dirty project state for project-modifying delegates.

`update --apply --component shape` or `--component bench` SHALL refuse unless
the root's `dirty` and every child's `dirty` are exactly false, as an explicit
cleanup push already requires; a `dirty` left null by a failed or timed-out
probe SHALL refuse as dirty work does, and the owner tool SHALL NOT be invoked.
`update --apply --component tools` or `--component workflow` SHALL NOT require
Git.

Every owner tool that `update --apply` invokes, for any component, SHALL run
with the thirty-one variables that "Repository inspection requires Git 2.36 and
shares one evidence model" lists removed from its environment, but
`GIT_ALLOW_PROTOCOL`, as the push child of `clean --action push` has them
removed, so that it acts on the repository that the check before it inspected,
never on one that a caller's `GIT_DIR`, `GIT_WORK_TREE` or `GIT_INDEX_FILE`
names. An owner tool is not a Git child: `project` SHALL pass it no `-c` pin
and SHALL set no `GIT_OPTIONAL_LOCKS` and no trace2 variable for it, and a
protocol list that the caller set in `GIT_ALLOW_PROTOCOL` SHALL still bind any
Git it runs.

#### Scenario: Default report
- **WHEN** update is run without --apply
- **THEN** it reports a plan without modifying repositories or installing software.

#### Scenario: A leg's probe times out
- **WHEN** a leg's status probe times out at 15 s and `update --apply --component shape` runs
- **THEN** the update refuses with exit 2 and the owner tool is never invoked

#### Scenario: Tools and workflow need no Git
- **WHEN** Git 2.35 is first on PATH and `update --apply --component workflow --yes` runs
- **THEN** it is not refused for Git's version, and the workflow command runs as before

#### Scenario: Owner tools see the repository the check inspected
- **WHEN** `update --apply --component shape --yes` runs on a clean project with, in the caller's environment, `GIT_DIR` and `GIT_WORK_TREE` naming another repository, `GIT_INDEX_FILE` set and `GIT_ALLOW_PROTOCOL=file`, and a fake owner tool that records its environment
- **THEN** the check before it reads the project's own repository, and the owner tool records none of the thirty-one names but `GIT_ALLOW_PROTOCOL`, which it records as `file`, where before this change it received the caller's `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE`
- **AND** it records no `GIT_OPTIONAL_LOCKS`, `GIT_TRACE2`, `GIT_TRACE2_EVENT` or `GIT_TRACE2_PERF`, the caller having set none

## ADDED Requirements

### Requirement: Repository inspection requires Git 2.36 and shares one evidence model
Every subcommand that inspects a Git repository SHALL use this evidence model.

Version: it SHALL run `git --version` once per invocation, and SHALL NOT inspect
a repository with a Git older than 2.36 (`git-too-old`) or with a `git` that is
missing, fails, times out or prints an unparseable version (`git-unavailable`);
whether the subcommand then refuses or reports is its own requirement's rule.

Configuration paths: before any Git child starts, `git --version` included,
every subcommand that inspects a Git repository SHALL test whether `HOME` or
`XDG_CONFIG_HOME` is set to a non-empty value whose first byte is not `/`.
The same test SHALL apply to `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`, which
name the user's and the system's configuration files.
The test SHALL be made on the raw bytes of each value, an empty or unset
variable passing it, and SHALL apply to each of these variables whether or not
Git would read a file through it, not following Git's order of precedence.
Where any fails it, the subcommand SHALL start no Git child and SHALL inspect no
repository (`relative-config-path`), because Git resolves such a value against
the directory a Git child runs in, so that files a repository holds would be
read as the user's configuration and as the global ignore and attributes files;
whether the subcommand then refuses or reports is its own requirement's rule,
as for the version.

Environment: every Git child but the push child of `clean --action push` SHALL
run in its own process group, and every Git child SHALL have these thirty-one
variables removed from its environment, `GIT_ALLOW_PROTOCOL` excepted for the
push child, unconditionally and before any Git call, from a fixed list that is
never queried from Git: the fifteen that
`git rev-parse --local-env-vars` prints on Git 2.40 and later
(`GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_CONFIG`, `GIT_CONFIG_PARAMETERS`,
`GIT_CONFIG_COUNT`, `GIT_OBJECT_DIRECTORY`, `GIT_DIR`, `GIT_WORK_TREE`,
`GIT_IMPLICIT_WORK_TREE`, `GIT_GRAFT_FILE`, `GIT_INDEX_FILE`,
`GIT_NO_REPLACE_OBJECTS`, `GIT_REPLACE_REF_BASE`, `GIT_PREFIX`,
`GIT_SHALLOW_FILE` and `GIT_COMMON_DIR`); `GIT_INTERNAL_SUPER_PREFIX`, which
Git 2.36 through 2.39 also print and which makes every command on those
versions fail when it is set; `GIT_ALLOW_PROTOCOL`, which Git does not print
and which, when it names a protocol, is consulted before every `-c` pin and
would allow the fetch that the pins below refuse; and the fourteen trace
variables that Git 2.36 through 2.43 read, `GIT_TRACE`, `GIT_TRACE_BARE`,
`GIT_TRACE_CURL`, `GIT_TRACE_CURL_NO_DATA`, `GIT_TRACE_FSMONITOR`,
`GIT_TRACE_PACKET`, `GIT_TRACE_PACKFILE`, `GIT_TRACE_PACK_ACCESS`,
`GIT_TRACE_PERFORMANCE`, `GIT_TRACE_REDACT`, `GIT_TRACE_REFS`,
`GIT_TRACE_SETUP`, `GIT_TRACE_SHALLOW` and `GIT_TRACE_WORKING_TREE_ENCODING`,
through which a caller could make a Git child create or append to a file it
names. Every Git child, the push child included, SHALL also have `GIT_TRACE2`,
`GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF` set to `0` in its environment: each
outranks the matching `trace2.normalTarget`, `trace2.eventTarget` or
`trace2.perfTarget` setting of the system and global configuration, the only
configuration from which Git reads a trace2 target and one that no `-c` pin
reaches, and `0` turns that target off, so that no trace2 target opens.
Read-only probes SHALL also set `GIT_OPTIONAL_LOCKS=0`. Every status probe,
and the hidden-state probe that reads a worktree's index flags, SHALL pass `-c
core.untrackedCache=false -c core.fsmonitor=false -c core.trustctime=true -c
core.checkStat=default -c core.ignoreCase=false`, which also override
`GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`; `core.trustctime` and
`core.checkStat` restore Git's full stat comparison, because Git compares a
file's ctime only while both settings keep these values, so that an edit that
keeps a file's size and restores its mtime would otherwise read unchanged, and
`core.ignoreCase=false` keeps in the records an untracked file whose name
differs only in case from a tracked one, which Git leaves out under
`core.ignoreCase=true` on a case-sensitive file system. Every Git child, of
every kind,
except the push child of `clean --action push`, SHALL also pass `-c
protocol.allow=never -c protocol.file.allow=never -c protocol.ssh.allow=never -c
protocol.git.allow=never -c protocol.http.allow=never -c
protocol.https.allow=never -c protocol.ext.allow=never`, because Git 2.43 has no
switch against lazy fetches, a probe in a partial (promisor) clone could
otherwise fetch a missing object from the network, and `protocol.allow` is only
the default policy, which a `protocol.<name>.allow` setting in the repository's
configuration overrides and a `-c` on the command line outranks; with the pins
the fetch fails locally, the probe fails, and its row is `inspection-error`,
never a network call. The push child is the one Git child whose purpose is to
reach a remote: it SHALL run with the thirty-one names but `GIT_ALLOW_PROTOCOL`
removed from its environment, so that it acts on the repository the run
inspected while a protocol list the caller set still binds it, as it binds the
push before this change, and with the three trace2 variables at `0`, as every
Git child has them, since trace output changes nothing about where a push
reaches, but with none of the seven protocol pins, so that the
remote it publishes to stays reachable over any protocol that list and the
configuration allow; it SHALL run as the push ran before this change, in the
process group of `project` itself, and so in the terminal's foreground whenever
`project` is, and unbounded, so that a credential prompt can read the terminal
and an interrupt from the terminal reaches it; no row's evidence comes from it.

Directory: a worktree probe SHALL run with `-C <worktree path>`, against that
worktree's own index, and only after that worktree's identity has been verified
immediately before. Repository-wide probes SHALL run in the repository's main
worktree, except the identity probe, which runs in the directory the argument
resolves to, and the registry listing, which runs there while the main worktree
is not yet known. Where `root` is null (a bare repository, a missing main
worktree, or a gitfile checkout whose main worktree cannot be named),
repository-wide probes SHALL run in the common directory for a bare repository
and otherwise in the directory where the identity probe ran; `project clean`
refuses those layouts.

Identity: a repository SHALL be identified by `{root, common_dir, dev, ino}`
together: the realpaths of its main worktree and of its common directory, from
one identity probe, and the device and inode of the common directory, read
without following a symlink. A worktree SHALL be identified by `{path, dev, ino,
admin_id}` together. Its registration SHALL be checked in both directions:
`<path>/.git` SHALL be a regular file whose `gitdir:` line names
`<common_dir>/worktrees/<admin_id>`, that directory's `gitdir` file SHALL
name `<path>/.git`, and that directory's `commondir` file, from which Git takes
the worktree's common directory, SHALL name `<common_dir>`, read by the
filesystem with no Git child, as Git reads it, its trailing line feeds and
carriage returns removed; relative values SHALL be resolved against the
directory holding the file and every comparison made between realpaths. A
`commondir` file that is missing or names another directory SHALL make the
registration disagree, and a read of it that fails SHALL give the row
`inspection-error` and no probe. A row whose registration disagrees SHALL get
no status probe and SHALL be `inspection-error`. A linked
worktree's effective work tree, the work tree that a Git command run in it
uses, SHALL be its registered path, and a row whose effective work tree is not
SHALL be treated as a row whose registration disagrees. Git gives a linked
worktree another work tree, or none, only through a `core.worktree` or a
`core.bare`, which it applies to that worktree, from the worktree's
`config.worktree` or from the repository's own `config`, only where that
`config` sets `extensions.worktreeConfig` to true. In such a repository, each
linked row whose registration agrees SHALL have its effective work tree read,
after its identity is verified and before its status probe, by `git rev-parse
--path-format=absolute --show-toplevel` run in it: the probe's standard output,
less the one line feed Git ends it with, SHALL be read as one path, which may
itself hold line feeds; output that is empty, that names no path, or that does
not end in a line feed SHALL make the row's registration disagree, and so SHALL
a toplevel whose realpath is not that of the row's registered path and a probe
that fails, as it does under `core.bare=true`. A registered path whose `lstat`
fails because it does not exist SHALL be `present: false`; any other failure
SHALL give `present: null`, an `os-error`, `inspection-error` and no probe.

Probes: for each repository, once per common directory, the identity probe; the
registry listing, `worktree list --porcelain -z`; one ref listing over
`refs/heads` and `refs/remotes`, NUL-separated, carrying each ref's name,
object, symref, upstream, upstream short name and upstream track; the merged
set of local branches against the merge target's SHA; and the repository's
`extensions.worktreeConfig`, read as Git reads it, as a boolean from the common
directory's own `config` file alone, by `git config --file <common_dir>/config
--type=bool --get extensions.worktreeConfig`, a value that is not set being
false and any other failure counting as true. For each present,
registration-verified worktree row, the main worktree's included, one combined
status probe: `status --porcelain=v1 -z --untracked-files=normal
--ignored=matching`. Every Git output that carries a path SHALL be parsed
NUL-delimited. A branch whose configured upstream's remote-tracking ref is
missing SHALL have `upstream` set to the configured short name, `remote_present`
false, and `ahead` and `behind` null.

Combined probe: `dirty` SHALL be true once a record other than an ignored one
arrives, and false once an ignored record arrives first or an empty stream ends
normally. The probe SHALL stop reading, and stop the child, at the 65th ignored
record or the 4,097th record of any kind, so that 64 ignored entries and 4,096
records are its bounds; a probe stopped at its bound SHALL be a complete
outcome, never `probe-failed`. `ignored_files` SHALL count the ignored records
read, a lower bound when `ignored_files_truncated` is true; `ignored_samples`
SHALL hold at most 8 ignored paths, each an object `{path, path_valid_utf8}`;
both SHALL be null when the probe did not run or failed, and a stream stopped
before any ignored record SHALL leave `ignored_files` null with `dirty` true. A
probe that fails or times out before `dirty` is established SHALL leave `dirty`
null, record `probe-failed`, `probe-timeout` or `deadline-exceeded`, and make
the row `inspection-error`. A probe that exits 0 having written to standard
error any line other than Git's advice lines (`hint:` alone or `hint: TEXT`),
or more than the 4 KiB kept, SHALL be treated as one that fails, since Git
exits 0 when it cannot read a directory and leaves what it could not read out
of its records; so, under Git's default `core.warnAmbiguousRefs`, a repository
holding `refs/heads/HEAD`, for which Git warns `refname 'HEAD' is ambiguous.`
in every status probe, has every row `inspection-error`.

Termination: each Git child's standard output SHALL be read as bytes as it
streams, and its standard error SHALL be drained while standard output is read,
and capped. A child stopped at its bound, past its budget or by a signal SHALL
receive SIGTERM to its process group and, 2 s later, SIGKILL; its reap SHALL
wait at most a further 2 s, after which the child SHALL be abandoned and its row
recorded `probe-timeout`. On every exit path, exceptions and signals included, a
subcommand SHALL kill the process groups of the probe children it started. A
removal child SHALL instead be waited for, and SHALL NOT be signalled before its
300 s ceiling. The push child of `clean --action push` is outside this
paragraph: its standard input, output and error SHALL be `project`'s own, never
read or capped by `project`, and `project` SHALL NOT signal it and SHALL wait
for it to exit.

Budgets: under an invocation deadline, as `project clean` has, each Git child
SHALL get `min(5 s, work remaining)`, except the push and delete-branch
children of `clean`, which SHALL stay unbounded, as "Clean bounds its Git work
and reports omitted work" states. Without one, as in status, doctor and update,
each Git child SHALL get 15 s, and those subcommands SHALL have no invocation
deadline and no row cap; a row whose probe is unreadable or times out SHALL
show as `inspection-error`. Children other than Git SHALL keep 15 s.

Manifest: every subcommand that resolves a merge target from a project manifest
SHALL read at most 1 MiB of it, and a larger manifest SHALL be
`manifest-invalid`. A manifest over the cap SHALL be detected from its `st_size`
before the read, and the read itself SHALL never exceed 1 MiB.

Stale entries: where any row of a repository's worktree listing has a path
that could not be read, its `lstat` failing other than for the path's absence,
or cut at its budget, so that its `present` is null, the `recommendation` of a
`stale-worktree` row of that listing, in `project status` and in `project
doctor` and `project update`, which share its inspection, SHALL read "Review
the stale worktree metadata before pruning it manually; a row's path could not
be read, so do not run git worktree prune, git worktree remove or git gc until
it can.", since `git worktree prune`, run for a stale entry's sake, also
deletes the administrative directory of a worktree whose path Git cannot stat;
with no such row it is the baseline's, "Review the stale worktree metadata
before pruning it manually."

Values SHALL equal those of the inspection this model replaces, except where a
requirement states a change.

#### Scenario: A git that floods standard error
- **WHEN** a fake `git` writes more than 64 KiB to standard error before printing its status records
- **THEN** the probe completes with no `probe-timeout`, the standard error kept is capped, and the row is `inspection-error` with `probe-failed`

#### Scenario: A git that ignores SIGTERM
- **WHEN** a fake `git` status probe ignores SIGTERM and outlives its budget
- **THEN** its process group receives SIGKILL 2 s after the SIGTERM, the row is recorded `probe-timeout` and classified `inspection-error`, and no process of that group remains

#### Scenario: Five thousand ignored records
- **WHEN** a fake `git` prints 5,000 ignored (`!!`) records for one worktree
- **THEN** the probe stops at the 65th, the row has `ignored_files: 64` and `ignored_files_truncated: true`, the outcome is complete rather than `probe-failed`, and the row is classified `ignored-local-files`

#### Scenario: User status configuration
- **WHEN** the user's configuration sets `status.showUntrackedFiles=no`
- **THEN** the combined probe still runs, and a clean worktree is classified by the ladder rather than `inspection-error`, where before this change every clean non-default worktree read `inspection-error`

#### Scenario: A caller's Git environment is ignored
- **WHEN** `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` are set in the caller's environment to name another repository
- **THEN** every probe reads the resolved repository, and each worktree probe reads that worktree's own index

#### Scenario: A linked worktree whose work tree is redirected
- **WHEN** a repository sets `extensions.worktreeConfig` to true, and the `config.worktree` of an otherwise eligible linked worktree W, which holds an ignored file `local.env`, sets `core.worktree` to a clean directory D elsewhere
- **THEN** W reads `registration-mismatch` with classification `inspection-error`, no status probe runs in W or in D, `project clean <root> --all-safe` is incomplete, `--all-safe --apply --yes` refuses with exit 2 and removes nothing, and W and `local.env` survive, where before this change W read clean from D's tree and Git's removal deleted W with `local.env`
- **AND** the preview of `project clean <root> --all-safe` lists W under `registration-mismatch`, whose next step names, as a manual remedy, unsetting `core.worktree` and `core.bare` in the repository's `config` or in a worktree's `config.worktree`, and the `inspection-incomplete` refusal of that preview, of `--all-safe --apply --yes` and of `--apply --action remove --worktree W --yes` names the same unsetting in its remedy
- **AND** `--apply --action remove --worktree W --yes` refuses with exit 2 and removes nothing, and `project status` marks W `inspection-error`
- **AND** the same holds when W's `config.worktree` sets `core.bare` to true instead
- **AND** when the repository's own `config` sets `core.worktree` to the main worktree's path instead, which leaves the main worktree's toplevel as it was while every linked worktree's becomes that path, W and every other linked worktree read `registration-mismatch` with classification `inspection-error`, `--all-safe --apply --yes` and `--apply --action remove --worktree W --yes` each refuse with `inspection-incomplete` and exit 2 and remove nothing, and that refusal's remedy names the same unsetting
- **AND** with the extension set and neither setting for W, W's effective work tree is its path and W is selected as before, and without the extension a counting `git` wrapper records no `rev-parse` child whose directory is a linked worktree
- **AND** with the extension set and neither setting for a linked worktree whose own path holds a line feed, the work-tree probe prints that path over two lines, which is read as one path, its registered path, so the worktree is not `registration-mismatch` and is selected where it is otherwise eligible, as the scenario "Control-character and non-UTF-8 paths" selects such a worktree

#### Scenario: A commondir that names another repository
- **WHEN** a linked worktree W of a repository R, which does not set `extensions.worktreeConfig`, holds an ignored file; a shared clone X of R sets `extensions.worktreeConfig` to true; the `config.worktree` in W's administrative directory sets `core.worktree` to a clean decoy directory D; and the `commondir` file in that administrative directory is rewritten to name X's git directory, while W's `.git` file and that directory's `gitdir` file still agree
- **THEN** W reads `registration-mismatch` with classification `inspection-error`, no status probe runs in W or in D, `project clean <root> --all-safe` is incomplete, and `--all-safe --apply --yes` refuses with exit 2 and removes nothing, so W and its ignored file stay, where with only the `gitdir` links compared the extension read from R's `config` was unset, the probe in W read D, and the removal deleted W with its ignored file
- **AND** with the `commondir` file as `git worktree add` wrote it, a relative path naming R's git directory, W's registration agrees as before

#### Scenario: A relative configuration path in status, doctor and update
- **WHEN** status, doctor and `update --apply --component shape --yes` run on a clean project whose root repository tracks `h/.gitconfig`, which defines a clean filter that writes a marker file, and a `.gitattributes` that selects that filter, with `HOME` set to the relative `h`
- **THEN** a counting `git` wrapper records no Git child, `git --version` included, and the marker file is never written
- **AND** doctor reports `relative-config-path` as an `error` check row and exits 1, status marks the repository root `inspection-error` with that code and exits 0, the update refuses with exit 2 and the owner tool is never invoked, and `update --apply --component workflow --yes` is not refused for it
- **AND** the same holds with `XDG_CONFIG_HOME` set to the relative `cfg` beside an absolute `HOME`, the repository tracking `cfg/git/config` instead
- **AND** the same holds with `GIT_CONFIG_GLOBAL` or `GIT_CONFIG_SYSTEM` set to the relative `h/.gitconfig` beside an absolute `HOME`

#### Scenario: The sixteenth scrubbed name on Git 2.36
- **WHEN** Git 2.36 is first on PATH and `GIT_INTERNAL_SUPER_PREFIX` is set in the caller's environment
- **THEN** every Git child runs with `GIT_INTERNAL_SUPER_PREFIX` removed from its environment, and the inspection succeeds, where with that variable kept every command on 2.36 fails closed

#### Scenario: The pinned status configuration
- **WHEN** `core.untrackedCache` and `core.fsmonitor` are set to true, `core.trustctime` to false, `core.checkStat` to `minimal` and `core.ignoreCase` to true in the file that `GIT_CONFIG_GLOBAL` names
- **THEN** a counting `git` wrapper records `-c core.untrackedCache=false -c core.fsmonitor=false -c core.trustctime=true -c core.checkStat=default -c core.ignoreCase=false` on every status child, every hidden-state child and every removal child

#### Scenario: An edit that keeps its size and restores its mtime
- **WHEN** a repository sets `core.trustctime=false` and `core.checkStat=minimal`, and a tracked file in an otherwise eligible linked worktree, whose index entry was written at least one second after the file's mtime so that the entry is not racily clean, is rewritten at least one second after that entry was recorded, keeping its size, and its mtime is then restored to the recorded value
- **THEN** the status probe reports the file modified, the row is classified `dirty` and excluded, and `--all-safe --apply --yes` leaves the worktree and the edit in place, where without the two stat pins the probe and Git's own check read the worktree clean and the removal deleted the edit

#### Scenario: A case-variant untracked file
- **WHEN** `core.ignoreCase=true` and an eligible worktree holds an untracked `WORK-FEAT` beside its tracked `work-feat`
- **THEN** the probe lists `?? WORK-FEAT`, the row is `dirty`, and the apply keeps it

#### Scenario: A lazy fetch in a partial clone is refused locally
- **WHEN** a status probe runs in a partial clone made with `--no-checkout --filter=tree:0`, so that the probe needs a tree object the clone does not hold, and the clone's `remote.origin.uploadpack` names a script that logs each run
- **THEN** a counting `git` wrapper records `-c protocol.allow=never` and the six per-protocol pins on the child, Git refuses the fetch of the missing object locally and exits nonzero, the probe is recorded `probe-failed`, and the row is `inspection-error`
- **AND** the logging script never runs, so no connection to the remote is attempted
- **AND** with `GIT_ALLOW_PROTOCOL=file` in the caller's environment and `protocol.file.allow=always` in the repository's configuration, the pinned probe is still refused and the logging script still never runs

#### Scenario: The push child reaches its remote
- **WHEN** `project clean <root> --apply --action push --branch B --yes` runs, with `<root>` the absolute path of the main worktree and, in the caller's environment, `GIT_DIR` naming another repository and `GIT_CONFIG_PARAMETERS` set, for a clean feature branch B that the push action accepts (B is not the default branch, its upstream `origin/B` exists, lacks a commit that B holds and holds none that B lacks, and no other worktree row is `inspection-error`), whose `origin` is a local path (the `file` protocol)
- **THEN** a counting `git` wrapper records the push child with none of the seven protocol pins and with the thirty-one names but `GIT_ALLOW_PROTOCOL` removed from its environment, and records all seven pins on every other Git child of the run
- **AND** the wrapper records that the push child shares `project`'s process group, where every other Git child of the run has a process group of its own
- **AND** the push exits 0 and `origin` holds B at the commit it has locally
- **AND** with a `pre-push` hook that sleeps 7 s, the push still exits 0 and `origin` holds B, no signal having reached the push child

#### Scenario: Trace targets are never written
- **WHEN** `project status <root>` and `project clean <root>` run for a repository with one linked worktree, with `GIT_TRACE`, `GIT_TRACE_PACKET`, `GIT_TRACE2` and `GIT_TRACE2_EVENT` each naming a file in the caller's environment and `trace2.eventTarget` naming a file in the file that `GIT_CONFIG_GLOBAL` names
- **THEN** a `git` wrapper that records each child's environment records `GIT_TRACE2`, `GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF` set to `0`, and none of the thirty-one names, on every Git child
- **AND** none of the named files is created or written
- **AND** with no trace variable in the caller's environment and `trace2.normalTarget`, `trace2.eventTarget` and `trace2.perfTarget` each naming a file in that global configuration, none of those files is created or written either

#### Scenario: A stale entry beside a worktree whose path cannot be read
- **WHEN** `project status --json`, `project doctor --json` and `project update --json` run on a project whose root repository has a stale worktree entry, its registered path missing, beside a linked worktree whose path cannot be read because its parent directory denies search permission
- **THEN** in each document the stale entry's `recommendation` is "Review the stale worktree metadata before pruning it manually; a row's path could not be read, so do not run git worktree prune, git worktree remove or git gc until it can.", where before this change it was "Review the stale worktree metadata before pruning it manually."
- **AND** once that worktree's path can be read again, the stale entry's `recommendation` is "Review the stale worktree metadata before pruning it manually." in each
