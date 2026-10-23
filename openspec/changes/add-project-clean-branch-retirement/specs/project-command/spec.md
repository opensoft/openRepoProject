## MODIFIED Requirements

### Requirement: Repository inspection requires Git 2.36 and shares one evidence model
Every subcommand that inspects a Git repository SHALL use this evidence model.

Version: it SHALL run `git --version` once per invocation, and SHALL NOT inspect
a repository with a Git older than 2.36 (`git-too-old`) or with a `git` that is
missing, fails, times out or prints an unparseable version (`git-unavailable`);
whether the subcommand then refuses or reports is its own requirement's rule.

Environment: every Git child but the push child of `clean --action push` SHALL
run in its own process group, and every Git child SHALL have these seventeen
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
versions fail when it is set; and `GIT_ALLOW_PROTOCOL`, which Git does not print
and which, when it names a protocol, is consulted before every `-c` pin and
would allow the fetch that the pins below refuse. Read-only probes SHALL also
set `GIT_OPTIONAL_LOCKS=0`. Every status probe SHALL pass `-c
core.untrackedCache=false -c core.fsmonitor=false`, which also override
`GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`. Every Git child, of every kind,
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
reach a remote: it SHALL run with the seventeen names but `GIT_ALLOW_PROTOCOL`
removed from its environment, so that it acts on the repository the run
inspected while a protocol list the caller set still binds it, as it binds the
push before this change, and with none of the seven protocol pins, so that the
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
300 s ceiling. The push child of `clean --action push` is outside this
paragraph: its standard input, output and error SHALL be `project`'s own, never
read or capped by `project`, and `project` SHALL NOT signal it and SHALL wait
for it to exit. The branch child of `clean --retire-branches` is outside this
paragraph's rule for probe children: `project` SHALL wait for it on every exit
path, exceptions and signals included, as for a removal child, and SHALL
signal it only past the budget that "Clean retires a removed worktree's branch
only on fresh head and ancestry evidence" gives it, as a child past its budget
is signalled above; it is none of the delete-branch children that Budgets
leaves unbounded.

Budgets: under an invocation deadline, as `project clean` has, each Git child
SHALL get `min(5 s, work remaining)`, except the push and delete-branch
children of `clean`, which SHALL stay unbounded, as "Clean bounds its Git work
and reports omitted work" states, and the re-read of a `clean
--retire-branches` branch stage, which SHALL get `min(5 s, work remaining less
the removal floor)`, as "Clean retires a removed worktree's branch only on
fresh head and ancestry evidence" states. Without one, as in status,
doctor and update,
each Git child SHALL get 15 s, and those subcommands SHALL have no invocation
deadline and no row cap; a row whose probe is unreadable or times out SHALL
show as `inspection-error`. Children other than Git SHALL keep 15 s.

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

#### Scenario: A lazy fetch in a partial clone is refused locally
- **WHEN** a status probe runs in a partial clone made with `--no-checkout --filter=tree:0`, so that the probe needs a tree object the clone does not hold, and the clone's `remote.origin.uploadpack` names a script that logs each run
- **THEN** a counting `git` wrapper records `-c protocol.allow=never` and the six per-protocol pins on the child, Git refuses the fetch of the missing object locally and exits nonzero, the probe is recorded `probe-failed`, and the row is `inspection-error`
- **AND** the logging script never runs, so no connection to the remote is attempted
- **AND** with `GIT_ALLOW_PROTOCOL=file` in the caller's environment and `protocol.file.allow=always` in the repository's configuration, the pinned probe is still refused and the logging script still never runs

#### Scenario: The push child reaches its remote
- **WHEN** `project clean <root> --apply --action push --branch B --yes` runs, with `<root>` the absolute path of the main worktree and, in the caller's environment, `GIT_DIR` naming another repository and `GIT_CONFIG_PARAMETERS` set, for a clean feature branch B that the push action accepts (B is not the default branch, its upstream `origin/B` exists, lacks a commit that B holds and holds none that B lacks, and no other worktree row is `inspection-error`), whose `origin` is a local path (the `file` protocol)
- **THEN** a counting `git` wrapper records the push child with none of the seven protocol pins and with the seventeen names but `GIT_ALLOW_PROTOCOL` removed from its environment, and records all seven pins on every other Git child of the run
- **AND** the wrapper records that the push child shares `project`'s process group, where every other Git child of the run has a process group of its own
- **AND** the push exits 0 and `origin` holds B at the commit it has locally
- **AND** with a `pre-push` hook that sleeps 7 s, the push still exits 0 and `origin` holds B, no signal having reached the push child
