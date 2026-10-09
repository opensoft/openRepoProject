## MODIFIED Requirements

### Requirement: Inspect and diagnose
Status and doctor SHALL support human and JSON reports for single repositories,
project manifests, families, worktrees and local tooling. Missing or malformed
state SHALL be visible; inspection SHALL never fetch, reset, or bootstrap.

Status and doctor SHALL inspect Git repositories through the evidence model that
"Repository inspection requires Git 2.36 and shares one evidence model" defines,
and SHALL NOT refuse for Git's version or for a repository they cannot inspect.
Doctor SHALL report a Git older than 2.36, or a `git` that is missing or
unusable, as an `error` check row naming `git-too-old` or `git-unavailable`,
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

#### Scenario: Default report
- **WHEN** update is run without --apply
- **THEN** it reports a plan without modifying repositories or installing software.

#### Scenario: A leg's probe times out
- **WHEN** a leg's status probe times out at 15 s and `update --apply --component shape` runs
- **THEN** the update refuses with exit 2 and the owner tool is never invoked

#### Scenario: Tools and workflow need no Git
- **WHEN** Git 2.35 is first on PATH and `update --apply --component workflow --yes` runs
- **THEN** it is not refused for Git's version, and the workflow command runs as before

## ADDED Requirements

### Requirement: Repository inspection requires Git 2.36 and shares one evidence model
Every subcommand that inspects a Git repository SHALL use this evidence model.

Version: it SHALL run `git --version` once per invocation, and SHALL NOT inspect
a repository with a Git older than 2.36 (`git-too-old`) or with a `git` that is
missing, fails, times out or prints an unparseable version (`git-unavailable`);
whether the subcommand then refuses or reports is its own requirement's rule.

Environment: every Git child SHALL run in its own process group, with these
sixteen variables removed from its environment, unconditionally and before any
Git call, from a fixed list that is never queried from Git: the fifteen that
`git rev-parse --local-env-vars` prints on Git 2.40 and later
(`GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_CONFIG`, `GIT_CONFIG_PARAMETERS`,
`GIT_CONFIG_COUNT`, `GIT_OBJECT_DIRECTORY`, `GIT_DIR`, `GIT_WORK_TREE`,
`GIT_IMPLICIT_WORK_TREE`, `GIT_GRAFT_FILE`, `GIT_INDEX_FILE`,
`GIT_NO_REPLACE_OBJECTS`, `GIT_REPLACE_REF_BASE`, `GIT_PREFIX`,
`GIT_SHALLOW_FILE` and `GIT_COMMON_DIR`), and `GIT_INTERNAL_SUPER_PREFIX`, which
Git 2.36 through 2.39 also print and which makes every command on those
versions fail when it is set. Read-only probes SHALL also set
`GIT_OPTIONAL_LOCKS=0`. Every status probe SHALL pass `-c
core.untrackedCache=false -c core.fsmonitor=false`, which also override
`GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`.

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
`<common_dir>/worktrees/<admin_id>`, and that directory's `gitdir` file SHALL
name `<path>/.git`, relative values resolved against the directory holding the
file and both comparisons made between realpaths. A row whose registration
disagrees SHALL get no status probe and SHALL be `inspection-error`. A
registered path whose `lstat` fails because it does not exist SHALL be `present:
false`; any other failure SHALL give `present: null`, an `os-error`,
`inspection-error` and no probe.

Probes: for each repository, once per common directory, the identity probe; the
registry listing, `worktree list --porcelain -z`; one ref listing over
`refs/heads` and `refs/remotes`, NUL-separated, carrying each ref's name,
object, symref, upstream, upstream short name and upstream track; and the merged
set of local branches against the merge target's SHA. For each present,
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
the row `inspection-error`.

Termination: each Git child's standard output SHALL be read as bytes as it
streams, and its standard error SHALL be drained while standard output is read,
and capped. A child stopped at its bound, past its budget or by a signal SHALL
receive SIGTERM to its process group and, 2 s later, SIGKILL; its reap SHALL
wait at most a further 2 s, after which the child SHALL be abandoned and its row
recorded `probe-timeout`. On every exit path, exceptions and signals included, a
subcommand SHALL kill the process groups of the probe children it started. A
removal child SHALL instead be waited for, and SHALL NOT be signalled before its
300 s ceiling.

Budgets: under an invocation deadline, as `project clean` has, each Git child
SHALL get `min(5 s, work remaining)`. Without one, as in status, doctor and
update, each Git child SHALL get 15 s, and those subcommands SHALL have no
invocation deadline and no row cap; a row whose probe is unreadable or times out
SHALL show as `inspection-error`. Children other than Git SHALL keep 15 s.

Manifest: every subcommand that resolves a merge target from a project manifest
SHALL read at most 1 MiB of it, and a larger manifest SHALL be
`manifest-invalid`. A manifest over the cap SHALL be detected from its `st_size`
before the read, and the read itself SHALL never exceed 1 MiB.

Values SHALL equal those of the inspection this model replaces, except where a
requirement states a change.

#### Scenario: A git that floods standard error
- **WHEN** a fake `git` writes more than 64 KiB to standard error before printing its status records
- **THEN** the probe completes with its records and no `probe-timeout`, and the standard error kept is capped

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

#### Scenario: The sixteenth scrubbed name on Git 2.36
- **WHEN** Git 2.36 is first on PATH and `GIT_INTERNAL_SUPER_PREFIX` is set in the caller's environment
- **THEN** every Git child runs with `GIT_INTERNAL_SUPER_PREFIX` removed from its environment, and the inspection succeeds, where with that variable kept every command on 2.36 fails closed

#### Scenario: The pinned status configuration
- **WHEN** `core.untrackedCache` and `core.fsmonitor` are set to true in the file that `GIT_CONFIG_GLOBAL` names
- **THEN** a counting `git` wrapper records `-c core.untrackedCache=false -c core.fsmonitor=false` on every status child and on every removal child
