Lane: openRepoProject-2

# Design

## Context

See `proposal.md` for why and what, and the deltas under `specs/` for the
requirements. The council's noted constraints, `clarifications.md` N1 to N5, are
answered by D1 to D5; D6 to D19 give the how of the proposal's decisions, and
D20 maps the packet's 35 validation scenarios to the deltas. The binding rulings
(D-A to D-AF, X1, X2, V1 to V12 with V2 as amended, lane 3's M1 to M7, and the
lead's R-4, R-8 and R-9, R-11 to R-15, R-17 and R-19) are already in
`proposal.md`, with the sections each edited; R-15 edited Context, D10, D14,
D18, D19, Risks and the Migration Plan here; R-17 edited Context and D14, and
R-19 edited Context, D14 and D19.

Citations are `file:line` at `da33d92`: `BA`, `DI`, `OV` and `HO` are the
packet's batch-cleanup, project-discovery, overview and handoff documents, and
`project:N` the executable. At `7a9134b`, `project` from `discover` onward sits
141 lines lower and the cited tests 383 lower; feature 003 re-pins every
citation.

What in `project` shapes the approach:

- `probe()` (`project:60-65`) is `subprocess.run` with a fixed 15 s timeout and
  `GIT_OPTIONAL_LOCKS=0`, killing only the single child on a timeout;
  `execute()` (`project:157-162`) runs a delegate unbounded and maps a signal
  death to 128 plus its number.
- `discover()` (`project:285-319`) applies its family-holder and
  manifest-ancestor redirections (`project:307-313`) to paths as well as names;
  `repo_state()` (`project:322-373`) parses the registry by line, runs two
  `status` calls and two upstream calls per worktree, and raises `Refused` when
  the root's status fails (`project:326-328`); `default_branch()`
  (`project:376-386`) and `ancestor()` (`project:389-393`) spend a child per
  candidate and per branch.
- `cleanup_report()` (`project:396-474`) holds the fifteen-class ladder
  (`project:418-468`), testing `dirty is None` after the merge-target branch
  (`project:421-426`); `clean()` (`project:521-595`) refuses `--json` with
  `--apply` (`project:523-524`), confirms through `confirm()`
  (`project:152-154`), revalidates by recomputing the report (`project:508-518`)
  and removes through `execute()`.
- `snapshot()` (`project:674-719`) feeds `status`, `doctor` and `update` through
  `repo_state()` (`project:681`, `:699`); `check_rows()` (`project:728-758`)
  lists `git` as a tool presence row (`project:755-757`); `update()` tests
  `dirty` by truthiness (`project:863`, `:869`); `main()` (`project:977-1003`)
  maps `Refused` and `OSError` to 2, printing `{"error"}` under `--json`, and an
  interrupt or end of input to `Cancelled.` and 130.
- Tests: 94 at `7a9134b`, run by `python3 -m unittest discover -s tests -v` on
  `ubuntu-latest` and `macos-latest` with Python 3.10 and 3.12; `run_cli` runs
  the file as a subprocess with `input=""`.

Facts checked here on Git 2.43.0, beside the council's fixtures in
`clarifications.md` (`k`, 20,000 files; `k3`, the untracked cache; `z`, the
unstarted branch):

| Probe | Observed |
| --- | --- |
| `git worktree add -b x`, then `git push -u origin x`, no commit | the branch reflog holds one entry, its old object all zeros, message `branch: Created from HEAD`; the push adds no branch reflog entry |
| a branch with one commit, then merged with `--no-ff` | the reflog holds the creation entry, then a `commit:` entry with a different new object |
| `git branch -m x x2` on an unstarted branch | the reflog moves with the branch and gains one entry whose old and new objects are equal |
| `git worktree add -B x <path> main` on an existing branch `x` with a commit of its own | the reflog gains `branch: Reset to main`, its old object `x`'s previous head and its new object `main`'s tip; `git branch -f` and `git checkout -B` on an existing branch also write `branch: Reset to` |
| `git fetch origin feat:f1`, `git update-ref refs/heads/f2 HEAD` and `git push . main:f3`, each creating a branch | each new reflog holds one entry, its old object all zeros; the messages are `fetch origin feat:f1: storing head` (`fetch -q origin feat:f1: storing head` with `-q`), none (the line ends after the time zone, with no tab) and `push`; a later `git branch -u origin/feat f1` or `git worktree add <path> f1` adds no entry to that reflog |
| `git reflog expire --all` at its defaults on a branch created 100 days and committed to 95 days earlier, then renamed 10 days earlier | only the rename entry survives, its old and new objects equal |
| `git init --separate-git-dir` | the first `worktree list` record is the git directory; `core.worktree` is unset |
| `rev-parse --show-toplevel --git-common-dir --show-superproject-working-tree` | three lines in a submodule checkout, the third the superproject's toplevel; two in a plain checkout |

## Goals / Non-Goals

**Goals:**

- One evidence pipeline, one bounded runner and one termination path for
  `clean`, `status`, `doctor` and `update`, which `add-project-overview` drives
  without forking it (D1, D2, D6); one mutation sequence for single-target and
  batch removal (D7, D9, D13).
- Fixed human text pinned by tests (D18), a test for every delta scenario (D20),
  and measured caps and a verified Git floor before the handoff (D5, D17).

**Non-Goals:**

- Any change to `new`, `benches`, or `confirm()` as `new`, `update` and
  `clean`'s push and branch deletion use it; bounding `push` and `delete-branch`
  children (D-W); versioning the JSON of `status` and `doctor`, or a doctor
  health section (OQ-22).
- An `in-use` gate (D3), cache disposal, paired retirement, remote evidence,
  squash-merge retirement, bare repositories, configurable limits, and any lock.

## Decisions

### D1. The runner's loop (N1)

Every Git child runs through one loop, the one-wide driver of D2.

Both pipes in one selector. The driver registers the child's standard output and
standard error, both non-blocking, and the read end of a wakeup pipe in one
`selectors.DefaultSelector`. Standard error is read whenever readable, so a
chatty Git never blocks on a full 64 KiB pipe; the first 4 KiB are kept for the
row's message and the rest counted and discarded. No temporary file is used.

A short tick and a wakeup. The selector timeout is the least of 100 ms, the
child's remaining budget, the work deadline's remaining time and, for a removal
child, its remaining ceiling. At start, `signal.set_wakeup_fd` gets the
non-blocking write end of an `os.pipe()` (`warn_on_full_buffer=False`), so a
signal wakes `select()` at once, although PEP 475 would retry it after a
flag-only handler; the tick is the backstop.

Handlers that only record. For SIGINT, SIGTERM and SIGHUP the handler stores the
first signal number received, which sets the exit status (OQ-16), and does
nothing else; a later SIGINT counts only for D15's reconciliation rule. After
each wake the driver reads the slot: while planning, a set slot makes it stop
its child (`terminate_group()`, then `reap()`) and raise a private
`Interrupted`; in the apply phase the seam reads the slot between steps (D15).
Only at the confirmation question does the handler raise instead, because
`input()` would otherwise be retried and Ctrl-C would seem to do nothing; no
child runs there. `status`, `doctor` and `update` install the same handlers, so
SIGTERM and SIGHUP unwind through the same cleanup and exit 143 and 129.

Cleanup on every exit path. A module-level registry holds every live probe
handle; the driver's `finally` and an outer `finally` around each subcommand's
inspection call `terminate_group()` and `reap()` on each, so no exception,
`BaseException` included, leaves a probe group running. A removal handle is
outside that set: the outer `finally` waits for it, up to its ceiling (D9), and
never signals it before then.

The residual, recorded: SIGKILL of `project` runs no `finally`, so probe
children run on, read-only, to their own end, and a removal child to its own end
(D4); a filesystem call stuck in the kernel can outlive its abandonment (D6).

Tests run the proposal's fake `git`s through this loop: one floods standard
error past 64 KiB and must not time out; one ignores SIGTERM, and SIGTERM to
`project` during a planning probe of it must give exit 143, no mutation and
`os.killpg(pgid, 0)` raising `ProcessLookupError` afterwards; one prints 5,000
`!!` records and must end complete at the bound.

### D2. The child handle and its parsers (N2)

The runner is split so that `add-project-overview` can multiplex children
without a second termination path or environment scrub.

The child handle. `start(argv, cwd, kind)` runs `subprocess.Popen` with standard
input from `/dev/null`, both outputs piped, `close_fds=True`,
`start_new_session=True` (never `process_group=0`, which needs Python 3.11, nor
`preexec_fn`; C4) and D6's scrubbed environment, with `GIT_OPTIONAL_LOCKS=0` for
kind `probe` only. It exposes both descriptors, the process ID (also the group
ID), its start time and kind, and registers itself (D1).
`terminate_group(grace=2.0)` sends SIGTERM to the group, polls
`waitpid(WNOHANG)` for the grace, then sends SIGKILL, ignoring
`ProcessLookupError`; `reap(grace=2.0)` waits at most the grace, then marks the
handle abandoned, records `probe-timeout` and never waits on it again (P6-1).
The handle reads nothing.

The one-wide driver. `run_bounded(spec, parser, budget)` starts one handle, runs
D1's loop, feeds standard output to the parser, and returns `complete`,
`complete-at-bound`, `failed`, `timeout`, `deadline` or `interrupted`, with the
parser's result, the exit status and the standard-error head. Every serial call
in `clean`, `status`, `doctor` and `update` uses it.

Pure incremental parsers. Each takes byte chunks through `feed()`, does no I/O,
holds at most one partial record, exposes `bound_reached`, and on `finish()`
returns its records or reports a truncated last record as a failure. The status
parser reads `status --porcelain=v1 -z` (two status letters, a space, a
NUL-terminated path; a rename or copy consumes a second path uncounted), keeps
`dirty`, the ignored count, up to 8 samples as raw bytes (each serialized as an
object `{path, path_valid_utf8}`) and D4's deletion flag, and reaches its bound
at the 65th ignored or the 4,097th record. The registry parser reads
`worktree list --porcelain -z` (NUL-terminated attributes, entries separated by
an empty record); the ref parser reads D6's format (NUL-separated fields, a line
feed per record); the merged-set parser one refname per line; and the
hidden-state parser `ls-files -v --stage -z`, stopping at the first mode
`160000` and otherwise setting one flag for a lowercase tag or `S`.

When the driver sees `bound_reached` it stops the child with `terminate_group()`
and returns `complete-at-bound`, never `probe-failed`. The overview's feature
004 drives up to four handles from its own selector loop, feeds the same
parsers, and relies on the same registry for termination (its
`clarifications.md`, N1). A test feeds each parser a recorded stream one byte at
a time and whole, and expects the same records and the same bound either way.

### D3. No `in-use` gate in this change (N3)

Declined for the MVP, so the deltas carry no such gate:

- It sees least where sessions live: a `/proc/<pid>/cwd` scan sees one Linux
  instance, so editors and agents on the Windows side of WSL2 are invisible to
  it, and macOS has no `/proc`.
- It has no honest failure mode: another user's `/proc/<pid>/cwd` is unreadable,
  so failing closed excludes every row on a shared host, and best effort claims
  a protection it cannot give.
- It adds little over `unstarted-branch`, which already keeps a freshly created
  and published lane worktree out (fixture `z`); what remains is a started,
  merged worktree with a live session, where the kept branch means no commit is
  lost, only work the session has not yet written. And an answer that depends on
  unrelated processes makes the preview and `plan_digest` less repeatable.

The residual, recorded: such a session can see its worktree removed by
`--all-safe --apply --yes`. The README says to close sessions before a batch
apply, and the confirmation lists every path. A later change may add the gate
with its own delta, after `locked-worktree`, scanned once per run under the
deadline, failing closed only on the invoking user's own unreadable entries, and
saying what it cannot see.

### D4. Detecting a probable partial removal (N4)

From evidence the report already holds. The status parser (D2) keeps a flag that
is true while every non-ignored record read is a tracked file deleted in the
working tree (status letters space and `D`) and at least one was read; any other
record clears it, and ignored records leave it alone. After classification a
separate function, never the ladder (OQ-28), adds the row note
`partially-removed` to a linked worktree (never the main one) that is present,
registration-verified (so its `.git` file and registry entry exist) and `dirty`,
with the flag set. A stream stopped at its 4,097-record bound is judged on the
prefix read; the note says "probable" either way, since a person's own `rm` of
every tracked file looks the same. The note is advisory: no classification, gate
or eligibility changes; JSON shows `notes: ["partially-removed"]` on the row,
and the human report prints it on its own line under the `dirty` advice with the
recovery text (D18).

When Git had already deleted `<path>/.git` (readdir order decides), the
registration check fails, no status probe runs, and the row is excluded as
`registration-mismatch` with classification `inspection-error`, with no note but
the named manual remedy (D18).

The proposal's scenario is the test: `project` and its removal child killed with
SIGKILL mid-deletion, then a report, once with fewer deletions than the record
bound and once with more, asserting the note or the `registration-mismatch` row
as the surviving `.git` file decides. A second test deletes tracked files by
hand to pin the flag's rules without timing.

### D5. The OQ-4 measurement protocol (N5)

Governance task 2.1 carries it, before the Speckit handoff, with its fixtures
and script in a scratch directory, never in the repository.

- Where: this workstation (Git 2.43.0, WSL2, Python 3.12) on a Linux filesystem
  path, the instance's own ext4 volume; and drvfs, the Windows drive mount,
  measured the same way and recorded as a degraded case, never used for the fit.
- Fixtures: repositories of about 10,000 and 100,000 tracked files, each with
  one linked worktree; one with about 1,000 branches, each with an upstream on a
  local bare remote; and a linked worktree of 20,000 files for removal, fixture
  `k`'s size.
- Timed: the combined status probe with its pins (D11), `for-each-ref` in D6's
  format, the registry listing, the identity probe, the merged set, `ls-files -v
  --stage -z`, and the removal of the 20,000-file worktree against the 5 s floor
  and the 300 s ceiling.
- Warm and cold: warm is five runs after a discarded one, reported as median and
  maximum; cold drops the page cache before each run (`sync`, then 3 written to
  `/proc/sys/vm/drop_caches` as root in the instance; without root, `vmtouch -e`
  on the repository or a fresh clone), the method recorded beside each number.
- The fit: BA:729-735 reapplied with the measured warm medians and the status
  and ref-listing costs at 10,000 files and 1,000 branches, with the 1.5 margin,
  for the apply pair (128, 16) and the report cap (256); a failing cap is
  lowered by the rule's steps and the deltas edited before the handoff. The
  100,000-file and cold numbers record where a plan goes incomplete, which is
  never unsafe (BA:772-774).
- Survey: for every repository under the configured projects directories here,
  the rows per gate outcome beside the timings, in particular those excluded
  only for `reflog-unavailable` (M3) or `unstarted-branch`; the council's survey
  found about 20 eligible rows in Opensoft-Tenant.

Until then the deltas mark the caps provisional.

### D6. The evidence pipeline

The children of one `clean` invocation, in order, numbered as BA:591-599 numbers
them:

| Row | Child | When |
| --- | --- | --- |
| 1 | `git --version` | once per invocation, before any other Git child |
| 2 | `discover`'s `rev-parse --show-toplevel` | a bare-name argument only |
| 3 | `rev-parse --path-format=absolute --show-toplevel --git-common-dir --show-superproject-working-tree` | at the directory the argument resolves to |
| 4 | `worktree list --porcelain -z` | at the same directory while the main worktree is unknown, otherwise the command directory |
| 4b | `config --get core.worktree` | only when the first registry record is the common directory (D8) |
| 5 | row 3 repeated in the command directory | only when row 3 ran elsewhere |
| 6 | one `for-each-ref` over `refs/heads` and `refs/remotes` | command directory |
| 7 | `for-each-ref --merged=<merge-target sha> --format=%(refname) refs/heads` | command directory |

Row 6 uses the packet's shared format, BA:605-607: refname, object name, symref,
upstream, upstream short name and `upstream:track,nobracket`, NUL-separated,
each record ending in a line feed. It yields every branch's head; `upstream` as
the configured short name even when its ref is gone (C3); `ahead` and `behind`
from the track field (`ahead N`, `behind M`, both, or empty for equal);
`remote_present` false when the track is `gone`; and `origin/HEAD`'s symref. It
replaces `default_branch()`'s calls and the per-worktree `rev-parse` and
`rev-list` calls (BA:617-621); row 7 replaces `ancestor()`.

Row 3 prints one value per line, and Git has no NUL form for it. Two lines mean
a plain checkout and three a submodule checkout; a value containing a line feed
makes the count exceed what was asked, and the probe is then repeated as one
child per option, counted, rather than guessed at. F is therefore at most 7, as
BA:615-616 states, plus row 4b in the gitfile layout and the rare repeat.

Per row: the identity reads (`lstat` without following, the `.git` file, the
admin `gitdir` file), each a filesystem call on a daemon `threading.Thread`
waited for with `min(5 s, work remaining)` and abandoned after it (C4; never a
`concurrent.futures` pool, whose shutdown would wait for a stuck call); then the
combined status probe in that worktree (D11). Rows 3 to 7 are memoized by common
directory within an invocation, which matters to `status` and `doctor`, whose
legs are other repositories. Where `root` is null (a bare repository, a missing
main worktree, or a gitfile checkout whose main worktree cannot be named), rows
4 to 7 run in the common directory for a bare repository and otherwise where
row 3 ran, as the evidence model states; `clean` refuses those layouts (D8), so
only a reader that reports them, such as `add-project-overview`, probes there.

The scrubbed environment is a copy of the caller's with the fifteen variables of
BA:244-250 removed, hard-coded from Git 2.43's `rev-parse --local-env-vars`
rather than queried (D17 checks the list on 2.36). `GIT_CONFIG_GLOBAL` and
`GIT_CONFIG_SYSTEM` are not in that list and stay; D11's `-c` pins override
them.

`repo_state()` and `cleanup_report()` become thin readers of this pipeline, and
the ladder becomes a pure function of a row's evidence (OQ-28). Value parity
with the baseline is tested on fixtures, except for the changes the deltas list.

### D7. Identity objects, revalidation and the residual window

The plan records the four objects of BA:208-213: `repository` `{root,
common_dir, dev, ino}`; each selected worktree's `{path, dev, ino, admin_id}`;
its branch evidence `{branch, head, upstream, upstream_oid, ahead, behind}`; and
`merge_target` `{name, source, sha}`. Each selected entry also records the
baseline signature fields (`project:494-497`) and `locked`.

In JSON each of these objects carries a validity flag beside every path value
(the escaping requirement): `repository` adds `root_valid_utf8` and
`common_dir_valid_utf8`, always true in `clean`, which refuses an invalid root
or common directory, and kept so that `add-project-overview`, which can report
such a repository, draws the same object; every object with a `path` (a
selected or excluded entry, a result target, a refusal, a row error) adds
`path_valid_utf8`, so an escaped `\xHH` never reads as a valid path holding
those four characters.

Revalidation is BA:677-707's targeted check, in its order, stopping at the first
difference: the identity probe; the manifest re-read (a file read, 1 MiB cap);
the registry listing; a narrowed ref listing whose patterns name the merge
target, the manifest's candidate, the branch the plan's `origin/HEAD` named,
`main`, `master`, `refs/remotes/origin/HEAD`, and the selected branches and
their upstreams; the target's identity and `modules` check by filesystem reads;
then, inside the target worktree, the combined status probe, which must print
nothing, and the hidden-state probe. Ancestry needs no child: it is a function
of the branch head and the merge-target SHA, both compared. The reflog of D10 is
not re-read: a moved branch is already `branch-changed`.

The first target's three repository children are the preflight for every target
(BA:709-711). After target k's child is reaped, its rescan runs the same three,
with the manifest re-read between the first two; when target k is a plain
`removed` they double as target k+1's repository part and count in its
`probes_performed`, and after the last spawned target, or when target k stops
the run, they are the final rescan (BA:712-719).

The residual window is BA:305-325's, narrowed by D11: ignored files created and
index flags set between the last revalidation and Git's own check, and any
change after that check. The confirmation and the result each print it in one
line (D18). The branch race keeps BA:327-341's outcomes, because the MVP never
deletes a branch.

### D8. Git-first resolution, the merge target and the gitfile rule

Resolution follows BA:856-869 for every `clean` mode. An absolute path must have
a realpath equal to row 3's toplevel, and that toplevel must be the main
worktree; a relative path, or none, is joined to the working directory, and row
3 there decides; only a bare name goes through `discover()`, whose one Git child
runs through the driver, and whose result is then resolved as a worktree
toplevel. A path argument never reaches `discover()`, so its redirections never
apply to it.

The main worktree is decided in this order (M6, R11):

1. Row 3's third line, the superproject's toplevel, is present: the argument is
   a submodule checkout, refused with `target-not-repository-root`.
2. The first registry record is `bare`: refused with
   `target-not-repository-root` in every mode (R10, OQ-15).
3. The first registry record equals the common directory (a main checkout whose
   `.git` is a file): the main worktree is the realpath of `core.worktree` (row
   4b); where that is unset, as `git init --separate-git-dir` leaves it, it is
   the candidate toplevel whose `.git` file's `gitdir:` line names the common
   directory; where neither names it, as from a linked worktree of such a
   repository, the argument is refused. The common directory is never probed as
   a row.
4. Otherwise the main worktree is the first record's realpath.

The merge target follows the resolution order the deltas state, over row 6's
listing: the manifest's `tracking_branch` with `origin/` removed (as
`project:383` already does; BA:169-177 omits it, D-T), the `%(symref)` of
`refs/remotes/origin/HEAD` with `refs/remotes/origin/` removed, `main`,
`master`. The manifest is read at `repository.root` by a bounded filesystem
call: a manifest whose `st_size`, taken before the read, exceeds 1 MiB is
`manifest-invalid` without being read, the read itself never exceeds 1 MiB, and
a wrong kind is `manifest-invalid` too (`project:280`). `no-merge-target` keeps
the baseline message, "Cannot determine the default branch from the manifest,
origin/HEAD, main, or master." (`project:401`), which the existing test reads
(Migration Plan).

The 1 MiB cap binds only the merge-target resolution. `status`, `doctor` and
`update` read the manifest through `snapshot()` for its kind and legs, which
this change leaves alone.

### D9. The removal child: never signalled, the ceiling and the reserve

The removal child is a D2 handle of kind `removal`: the scrubbed environment
without `GIT_OPTIONAL_LOCKS`, and the argument vector `git -c
status.showUntrackedFiles=normal -c core.untrackedCache=false -c
core.fsmonitor=false -C <command directory> worktree remove <path>`, both
operands absolute and the path passed as the raw bytes the registry gave. It is
spawned only while at least 5 s of the work deadline remains (BA:437-441).

Once spawned it is waited for by D1's loop with no budget: the deadline passing
changes nothing and a signal is only recorded, the first of either printing
D18's wait line. This departs from BA:396, BA:401-402, BA:437-439, BA:456-458
and BA:466-468, and from the Resolution record (HO:208, HO:247-249), on the
council's evidence that a TERM at 0.25 s left 18,333 of fixture `k`'s 20,000
files and a `dirty` tree (V1).

The ceiling is 300 s from the spawn, on the monotonic clock: `terminate_group()`
(SIGTERM, then SIGKILL after 2 s) and a bounded `reap()`, abandoning a child
stuck in uninterruptible sleep on a hung mount. For such a child, or one whose
exit could not be observed, the rescan decides: `removed` when its registry
entry and path are gone, otherwise `unknown` with the note `partially-removed`;
its reason is `removal-ceiling` either way, and the run exits 1 (D19). 300 s is
about two hundred times fixture `k`'s 1.27 s, ample even for drvfs at ten times
slower; D5 measures it.

The 10 s reserve counts from the child's exit or the ceiling, each rescan child
getting `min(5 s, reserve remaining)`. A run with no removal in flight therefore
ends within 64 s of its start, not counting the time blocked at the confirmation
question: 50 s of work, the 10 s reserve, and up to 4 s to stop a probe child
(SIGTERM, the 2 s grace, SIGKILL, a reap wait of up to 2 s), the figure the
overview states; a removal in flight adds up to 300 s (M5). A call stuck in the
kernel is the one exception.

### D10. `unstarted-branch` from the reflog (V2 as amended, M3, M4, R-12, R-15)

A head equal to `merge_target.sha` is not by itself proof of an unstarted
branch, because a branch fast-forward merged into the target sits at the
target's tip. The gate therefore reads the branch's reflog in every case, and
nothing else decides it. It runs for each row that is `merged-removable` and was
not excluded by an earlier gate, in `mode: "single"` as well as the others (M4):

1. The branch's reflog, `logs/refs/heads/<branch>` under the common directory
   (each `/` of the branch name a directory level), is read by one bounded
   filesystem call (D6), at most 64 KiB, never by a Git child. One outcome rule
   holds: `ENOENT` or `ENOTDIR`, a file of 0 bytes, the 64 KiB bound reached, or
   surviving entries that cannot decide give `reflog-unavailable` for that row;
   any other OS error on the read is that row's `inspection-error` with
   `os-error`, like any failed row probe; and a read not finished inside the
   filesystem budget leaves the row unprobed and the plan incomplete with
   `inspection-incomplete`, as for every other filesystem read.
2. Each line is `<old> <new> <identity> <time> <zone>`, then a tab and the
   message when there is one; an `update-ref` without `-m` writes neither
   (Context). The anchor is the last surviving entry whose old object is all
   zeros, or whose message begins `branch: Created from` or
   `branch: Reset to`. Every command that creates a branch writes an all-zeros
   old object, whatever its message: `worktree add -b`, `branch` and
   `checkout -b` write `branch: Created from`, while
   `git fetch <remote> <ref>:<branch>`, `update-ref` and `push .` write no
   `branch:` message at all (Context). `worktree add -B`, `branch -f` and
   `checkout -B` on an existing branch write `branch: Reset to`, its old object
   the branch's previous head. An entry whose old object is all zeros is never a
   movement. A movement is an entry after the anchor, or any entry when no
   anchor survives, whose old and new objects are non-zero and differ; a
   rename's entry has equal objects, so it is no movement.
3. A last entry whose new object differs from the current head gives
   `reflog-unavailable`, because the reflog then does not describe the branch.
4. Otherwise a movement means the branch moved after its anchor: the gate
   passes, whatever the head, and the ancestry already established decides
   that it is merged.
5. An anchor with no movement after it, whose new object equals the current
   head, gives `unstarted-branch`, whether or not that head equals
   `merge_target.sha`. No anchor and no movement, or any other combination,
   gives `reflog-unavailable`.

A branch fast-forward merged into the target therefore passes: checked here on
Git 2.43, its reflog holds the creation entry, then its own `commit:` entry,
while its head equals the target's. So does a branch fast-forwarded to the
target, whose reflog also records the move. A branch made by `worktree add -b`,
published by `push -u` and never committed to holds only its creation entry and
is `unstarted-branch` (Context). A branch with commits of its own that
`worktree add -B` resets to the target's tip anchors at that `branch: Reset to`
entry and is `unstarted-branch` until it gains a commit, where reading from its
creation entry would count its earlier commits as movement. A branch created by
`git fetch origin feat:f1` at the target's tip, given its upstream by
`git branch -u` (which writes no entry) and never committed to here, anchors at
that fetch entry, whose old object is all zeros, and is `unstarted-branch`;
anchored on messages alone, that entry would have read as a movement and passed
the gate at the target's tip (R-15).

Entries expire. `git gc` runs `git reflog expire`, whose `gc.reflogExpire`
defaults to 90 days. A branch whose anchor has expired while a later movement
survives still passes. A branch with no surviving decisive entry, because it
saw no activity for that long, reads `reflog-unavailable` and is never removable
by `project` in either mode, a residual recorded under Risks beside the
reftable and `core.logAllRefUpdates=false` one. When every entry of a reflog has
expired, Git leaves the file in place with 0 bytes: checked here on Git 2.43
with `git reflog expire --all` at its defaults, a 100-day-old creation entry and
rename entry expired to an empty file, while an 80-day-old creation entry
stayed; and a branch created 100 days and committed to 95 days earlier, then
renamed 10 days earlier, kept only the rename entry, so that neither an anchor
nor a movement survives (Context). An empty file therefore reads as a missing
one does. No child is added, so the fit is unchanged (M3).

### D11. The pinned configuration (V3)

Every combined status probe runs as `git -c core.untrackedCache=false -c
core.fsmonitor=false -C <worktree> status --porcelain=v1 -z
--untracked-files=normal --ignored=matching`, the removal as D9 states, and the
hidden-state probe carries the same two pins for uniformity. The council's
fixture `k3` (the untracked cache on, `core.checkStat=minimal`, an index-writing
status run) showed Git's own pre-removal check missing a file created after
revalidation and deleting it with exit 0; with the pins it refuses with 128. A
`-c` on the command line outranks every configuration file, those that
`GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` name included, and the scrub removes
`GIT_CONFIG_PARAMETERS` and `GIT_CONFIG_COUNT`, so a caller cannot inject a
contrary `-c`.

`core.fsmonitor=false` is read as a boolean from Git 2.36, when the built-in
monitor arrived; older Git reads the value as a hook path, one more reason for
the floor (D17). The cost is a full untracked scan where the cache would have
helped; D5 measures it. One consequence crosses changes: feature 004's fixtures
that rely on a running fsmonitor (DI:1233-1237, DI:1249-1254) must be rewritten,
as the lead's ruling records.

### D12. The 16-per-run deferral (V5)

Gates are evaluated in canonical order. Rows that pass every gate before
`deferred-target-cap` are counted; the first 16 go on to the `modules` check and
the hidden-state probe, and the rest are excluded as `deferred-target-cap` with
no index probe, so at most 16 hidden-state probes run and E is at most 16. A row
an index gate then excludes keeps its place, so a run can select fewer than 16
while rows stay deferred, and 16 rows that an index gate always excludes, ahead
of a backlog, stop it until a person handles them; the human text names that
case. The plan stays complete and apply allowed; each re-run plans and
revalidates afresh, draining 16 at a time. `plan_digest` covers only `selected`,
so a deferred row's change leaves a preview valid, and the report mode defers
alike. The `target-cap` refusal (BA:96-101, BA:1004, BA:1367-1371) is retired, a
departure open to Brett Heap; the code survives only as the overview's limiting
gate.

### D13. Single-mode completeness (V4)

In `mode: "single"`, the plan builder runs rows 1 to 7, matches P against the
registry (`worktree-not-found` if absent), and inspects P's row first: identity,
status probe, gates. Then it inspects the other rows in canonical order up to
the row cap, P not counted. The plan is complete when the repository-wide probes
succeeded and P's row is established. Another row's `inspection-error` is
recorded as the plan note `inspection-incomplete`, rows beyond the cap as
`omitted` with the note `inspect-cap`, and rows the deadline left as the note
`deadline-exceeded`; none of them blocks P, while P's own revalidation stays
strict and P's removal still needs the 5 s floor. Refusing P would leave a raw
`git worktree remove`, which skips every gate. This departs from BA:188-192,
BA:419-420, BA:1268-1272, BA:1562-1563, HO:208 and HO:247-249; the batch keeps
full-repository completeness.

### D14. Report mode at 256 rows, and the fit arithmetic

At BA's 150 ms per Git child, with F = 7:

| Mode | Children | Time | Fits the 50 s work deadline |
| --- | --- | --- | --- |
| report, 256 rows | 7 + 256 + 16 = 279 | 41.85 s | yes |
| report, 512 rows | 7 + 512 + 16 = 535 | 80.25 s | no |
| all-safe, 128 rows, 16 targets | 7 + 128 + 16 + 80 + 3 = 234, and 16 removals | 35.1 s + about 4.8 s = 39.9 s | yes; the 16th removal spawns at 39.15 s with 10.85 s left (BA:753-756) |
| single, 128 rows plus P | 7 + 129 + 1 + 5 + 3 = 145, and 1 removal | 21.75 s + about 0.3 s | yes |

The report builds no apply plan, so its worst case is the planning term alone,
and 256 is the largest power of two that fits (D-V, OQ-29). Row 4b and the rare
row 3 repeat add 0.15 s each; the reflog reads add no child. Under D9 a removal
running past the deadline is bounded by its ceiling, not by the fit. The report
keeps the baseline layout and adds `Report: complete` or `Report: incomplete
(CODES)`, and, for a repository of at most 128 worktree rows, `--all-safe would
select N`; above 128, where `--all-safe` itself would be incomplete, it prints
`--all-safe would be incomplete (inspect-cap)` instead, while its JSON carries
`selected: null` and a `notes` entry with code `inspect-cap` and `rows`, the
count of registered worktree rows (R-15); the note does not make the report
incomplete. Above 128 the gates still run per inspected row, so `excluded` lists
every inspected row a gate excludes with its reason as in any report, and only
the selection step is withheld (R-17). Above 128 the `plan_digest` is computed
over the same canonical text as any plan, which covers only the repository's
identity fields, the merge target and `selected`, with `selected` null, and
`--expect-plan` never consumes it, because an apply there is an incomplete plan
and is refused before the digest is compared; at most 128 rows a report's digest
equals the `--all-safe` preview's for the same repository identity, merge target
and selection, since the mode is not in the digest, and an `--expect-plan`
carrying it matches, which is intended; the digest also covers the merge
target's name and SHA, so a target that advances between the report and the
preview gives `plan-digest-mismatch`, which is safe (R-19). It exits 0, 1 or 2
by completeness (R2).

### D15. Signals before and during the apply phase (OQ-16, M1)

The apply phase begins when the question is answered `yes` or `--yes` is
accepted (BA:350-354). Before the question, BA:350-354's order holds: an
incomplete plan is refused first (a preview or report exits 1, a run with
`--apply` exits 2 before asking), then an `--expect-plan` mismatch
(`plan-digest-mismatch`, exit 2), and only then does a complete `--all-safe`
plan that selects nothing print `No eligible worktrees` and exit 0 without
asking; in single mode an excluded P is `target-excluded`, exit 2, not an empty
selection. Before the apply phase, an `Interrupted` from the driver, or the
question's raising handler, unwinds through the `finally` clauses, which
terminate and reap every probe group; `main()` prints `Cancelled.` on standard
error, on a best-effort basis and with no JSON document under `--json`, and
returns 130 for SIGINT or end of input, 143 for SIGTERM and 129 for SIGHUP,
with nothing mutated, returning the status rather than re-raising it.

During it, the handler only records. The seam reads the slot before each
revalidation and before each spawn; a set slot makes that target and every later
one `not-attempted` with `interrupted`. A removal already spawned is waited for
(D9) and ends by its own exit: nonzero is `failed` with Git's status
(`git-refused` for 128, `git-failed` otherwise), whether or not a signal reached
`project`, and 0 is `removed` on rescan evidence, else `unknown` with
`unconfirmed-removal` (M1); the rescan alone decides, with `partially-removed`,
only for a child killed at the ceiling or whose exit was not observed (D9). A
SIGINT after the first recorded signal, while a rescan runs, abandons the
remaining rescans (BA:473-474): the running group is terminated, unestablished
fields stay null, and the target is `unknown` with `reconciliation-incomplete`.
Every write of the record is guarded against `OSError`, since after SIGHUP the
terminal may answer `EIO`. The exit status is D19's first matching row: 130, 143
or 129 whenever a signal arrived.

### D16. Status and doctor: error rows and JSON placement (R6, R7, D-S)

For a root or leg, `repo_state()` first checks `<path>/.git` with `lstat`:
absent, the dict is `present: false` with no Git child, as today. Present, the
memoized version check runs; an old or unusable Git, or a failed or timed-out
status probe, gives the dict `classification: "inspection-error"` and `errors`
(`{code, message, path?, path_valid_utf8?, reason?}`: `git-too-old`,
`git-unavailable`, `probe-failed`, `probe-timeout` or `os-error`), `present`
null when the version check failed, and null for every value not established. An
inspected dict has neither field, so the JSON stays additive and unversioned.
The marker is `classification`, the field worktree rows carry, as V11 asked the
delta to name, with `errors` for the cause. Every `path` in these dicts, the
root, leg and worktree rows and `errors` entries alike, carries
`path_valid_utf8` beside it, written by `clean`'s escaping rule, each
`ignored_samples` entry is `{path, path_valid_utf8}`, and the report's top-level
`root`, and each nested family member's `root`, gains `root_valid_utf8` beside
it; all are additive too.

`check_rows()`: the `git` tool row reports the version check, `ok` with the
version or `error` with its code, where today a missing `git` is a warning
(`project:755-757`); a root, leg or worktree row classified `inspection-error`,
a null `present` and a null `dirty` each add an `error` row naming the cause;
nulls that mean "none" add nothing, so a fresh project with no remote passes.
The exit rule is unchanged (`project:828-829`). `status` prints `Git:
inspection-error (<codes>)` in place of the branch line. `update` tests `dirty
is not False` for the root and every child (`project:863`, `:869`), and its
`tools` and `workflow` components need no Git (`project:884-885`, `:905-906`):
with an old Git their report shows `inspection-error` rows and the delegate
still runs.

### D17. Verifying the Git 2.36 floor (OQ-23)

The design relies on these Git behaviours, with the release that brought each:

| Behaviour | Since |
| --- | --- |
| `worktree list --porcelain -z` | 2.36 |
| `core.fsmonitor` read as a boolean | 2.36 |
| `rev-parse --path-format=absolute` | 2.31 |
| `status --ignored=matching` with `--untracked-files=normal` and `-z` | 2.16 |
| `--show-superproject-working-tree` | 2.13 |
| `ls-files -v` combined with `--stage`, and `worktree remove`'s refusals for a populated submodule and an admin `modules` entry | verified on 2.43 only (BA:132-137, BA:665-668) |
| the fifteen variables of `rev-parse --local-env-vars` | taken from 2.43 (BA:244-250) |

Governance task 2.2 verifies the floor before the handoff: Git v2.36.x built
from its release tarball in a scratch directory, first on PATH, and a scratch
script comparing each row's output with Git 2.43's. If any row differs, the
floor rises to the lowest version on which every row holds, and the deltas
change before the handoff. Feature 003 adds a CI job that builds the floor
version, cached, and runs the `clean`, `status` and `doctor` tests with it first
on PATH.

### D18. What the person sees

All new text is ASCII, with `ROOT`, `PATH`, `BRANCH`, `N`, `K`, `M` and `REASON`
substituted (paths by the escaping requirement), and the tests pin it.

The preview, after the baseline's `Cleanup plan for ROOT`, `Merge target: NAME
(SOURCE)` and `Freshness:` lines, prints `Selected (N):` with one line `  remove
PATH [BRANCH]` per row; `Excluded (M):` with, per reason, `  REASON (K): NEXT
STEP` and one line `    PATH [BRANCH]` per row, an `ignored-local-files` row
adding `: N ignored; first: SAMPLE` (`at least N` when truncated); for the
deferral, `  deferred-target-cap (K): this run removes up to 16; run again:
project clean ROOT --all-safe --apply`; the residual-window line, `Not
protected: ignored files created or index flags set after the last check, and
any change after Git's own check.`; and, when a complete plan selects nothing,
`No eligible worktrees`.

The next steps by reason: `dirty` "commit or preserve the changes";
`ignored-local-files` "move or delete the ignored files by hand";
`unstarted-branch` "no commit was made on this branch here since it was created;
review, then git worktree remove yourself"; `reflog-unavailable` "the branch's
reflog is missing, expired or undecidable; review, then git worktree remove
yourself"; `contains-submodule` and `hidden-local-state` "review, then remove
the worktree yourself"; `registration-mismatch` and `inspection-error` "review,
then git worktree repair or git worktree prune, or remove the row by hand";
`locked-worktree` "unlock it yourself if it should go"; every other class its
recommendation.

The question: `Remove N worktrees, keeping N branches? [yes/N]`, in the singular
for one. The wait line, at most once: `Waiting for git worktree remove PATH to
finish; a started removal is never interrupted (at most 300 s).` Success:
`Removed N; branches kept: B1, B2.` A stop: `Stopped at PATH (REASON). Removed K
of N. Not attempted: P1, P2. Next: project clean ROOT --all-safe`, then the
retained branches and the residual-window line. The partial-removal note, under
the `dirty` advice or on a `partially-removed` target: `Probable partial
removal: inspect, then git worktree remove --force PATH by hand.`

Refusal messages keep the baseline wording where a test reads it:
`target-excluded` for the current worktree, `Cannot remove the current
worktree.`; for a class that is not removable, `Worktree is CLASS; only clean
merged worktrees may be removed.`; for a gate, `Worktree is excluded: REASON;
NEXT STEP`. A plan-blocking refusal names its remedy: `inspection-incomplete`
"repair or remove the inspection-error rows first: git worktree repair, git
worktree prune, or remove the row by hand after review"; `inspect-cap` "N rows
exceed the row cap of M; remove worktrees explicitly, or prune stale entries by
hand"; `deadline-exceeded` "the run ran out of time; remove worktrees explicitly
or re-run".

### D19. Stages, notes and exit codes, as normalised

The stage table is BA:487-494 with V1 and M1 applied (D15): `removed` and
`unknown` gain `removal-ceiling`, `failed` holds whether or not a signal
arrived, and `interrupted` and `deadline-exceeded` are reasons of
`not-attempted` only. Notes: the plan's `merge-target-conflict`; in report mode
above 128 rows, `inspect-cap` with `rows`, which does not make the report
incomplete (D14, R-15); and, in single mode, the non-blocking
`inspection-incomplete`, `inspect-cap` and `deadline-exceeded` (D13); a target's
`orphaned-directory`, and `partially-removed` when its child was killed at the
ceiling, or its exit could not be observed, and the rescan shows its registry
entry or path remaining; a row's `partially-removed` (D4).

| Exit | First matching row |
| --- | --- |
| 130, 143 or 129 | a signal was received, the first deciding, or input ended at the question |
| 1 | the deadline stopped work after the apply phase began, any target is `unknown`, or any target's reason is `removal-ceiling` |
| Git's status | a target is `failed` with `git-refused` or `git-failed` |
| 2 | any refusal; a `refused` target; `removed` with a branch-after-removal reason; `failed` with `spawn-error` |
| 0 | every selected target `removed` with reason null, or nothing eligible |

The table governs runs with `--apply`. A preview or report exits 2 only for a
refusal raised before a plan is built, 1 for an incomplete plan, and 0
otherwise, the signal exits of D15 excepted (BA:547-549, R2). Git's status
passes through even when it equals one of `project`'s own (BA:538-543, OQ-25).

### D20. The packet's validation scenarios, mapped

Each of BA:1347-1628's 35 scenarios is a delta scenario of the same name, in the
requirement below; the proposal's changes to a scenario are noted. The two
deferred-extension scenarios (BA:1630-1636) belong to later changes.

| BA lines | Scenario | Requirement | Change |
| --- | --- | --- | --- |
| 1353-1359 | Stable order and preserved work | batch | |
| 1360-1366 | Row cap and planning failures | bounds | |
| 1367-1371 | Target cap | bounds, as "Twenty rows pass every gate before deferred-target-cap" | V5 deferral |
| 1372-1386 | Every protected classifier | batch | the plain row has a commit of its own (V2) |
| 1387-1395 | Hidden local state | batch | |
| 1396-1407 | Submodules | batch | |
| 1408-1417 | Ignored-file bound | bounds | |
| 1418-1429 | Bounded revalidation work | bounds | |
| 1430-1432 | Paths and empty plans | batch | |
| 1436-1440 | Target directory replaced | revalidates | |
| 1441-1445 | Admin registration changed | revalidates | |
| 1446-1449 | Parent directory swapped | revalidates | |
| 1450-1462 | Repository replaced mid-batch | narrow guarantee | |
| 1463-1467 | New worktree and pre-removal changes | revalidates | |
| 1468-1477 | State changes before revalidation | revalidates | |
| 1478-1480 | Changed later target | revalidates | |
| 1481-1486 | Untracked file under `status.showUntrackedFiles=no` | revalidates | |
| 1487-1491 | Ignored file in the residual window | narrow guarantee | |
| 1492-1496 | Branch advances before removal | revalidates | |
| 1497-1505 | Branch advances after removal | narrow guarantee | |
| 1509-1521 | Deadline expiry mid-batch | bounds | the child is waited for (V1) |
| 1522-1525 | Exit 0 without evidence | reconcilable | |
| 1526-1530 | SIGINT | reconcilable, as "A signal during a removal" | V1, M1; 143 and 129 added |
| 1531-1538 | Git leaves an orphaned directory | reconcilable | |
| 1539-1544 | Git refuses the removal | reconcilable | |
| 1545-1549 | Unreadable path after removal | reconcilable | |
| 1550-1553 | Exception after the apply phase begins | reconcilable | |
| 1554-1566 | Single target equals a one-item batch | retire | V4: single removes P beside an unreadable row |
| 1567-1570 | Preview is advisory | batch | |
| 1571-1577 | Plan digest mismatch | batch | |
| 1581-1590 | Control-character and non-UTF-8 paths | paths | |
| 1591-1594 | Non-UTF-8 repository root | paths | |
| 1595-1609 | Overview handoff keeps identity | Git-first | |
| 1610-1617 | Absolute path that is not a repository root | Git-first | |
| 1618-1628 | Merge target missing, invalid, or conflicting | Git-first | |

The proposal's own scenarios are traced by their labels in the deltas'
requirements: R1, R2, R6, D-N and OQ-29 under the reports; R9 and C3 under the
classification and "Inspect and diagnose"; R10, R11, D-T and the manifest cap
under Git-first resolution; V1 to V4, M3 and M4 under retirement; OQ-10, OQ-16
and M1 under the JSON and the result; V9 under the evidence model; D-D under
push; D-R under maintenance.

## Risks / Trade-offs

- [A started removal cannot be interrupted for up to 300 s, so Ctrl-C seems to
  do nothing] -> The wait line says why and for how long (D18); a SIGKILL of
  `project` leaves the removal running in its own session, and D4's note reports
  what it left.
- [Repositories without file reflogs (the reftable backend,
  `core.logAllRefUpdates=false`) exclude every merged row as
  `reflog-unavailable`] -> Fails closed with its own reason; D5's survey counts
  such rows.
- [A branch with no surviving decisive reflog entry, because it saw no activity
  for `gc.reflogExpire` (90 days by default), reads `reflog-unavailable` and is
  never removable by `project` in either mode] -> Fails closed beside the
  reftable residual; the remedy names `git worktree remove` (D18), and D5's
  survey counts such rows.
- [A reflog over 64 KiB (about 300 entries) fails closed as
  `reflog-unavailable` even when it records movement, because the head test
  runs first and the bound ends the read] -> Fails closed; the remedy calls the
  reflog undecidable and names `git worktree remove` (D18), and D5's survey
  counts such rows.
- [A branch created from a remote branch that already had commits, then merged
  elsewhere, reads as unstarted, because nothing moved it here since its
  creation entry] -> Fails closed as `unstarted-branch`; the remedy says that no
  commit was made on the branch here since it was created (D18).
- [A live session in a started, merged worktree is not protected] -> D3's
  residual; the README asks for sessions to be closed, and no commit can be
  lost.
- [The pins turn off the untracked cache and fsmonitor, so status probes on
  large trees are slower] -> D5 measures it; a slow probe makes a plan
  incomplete, never unsafe.
- [Sixteen rows that an index gate always excludes stop the deferral from
  draining] -> The human text names the case; V5's caveat is before Brett Heap.
- [`remote-gone` keeps merged worktrees out wherever upstreams are auto-deleted
  and pruned, and squash-merged branches never prove ancestry] -> Both before
  Brett Heap (Open Questions); the recommendation text says so.
- [The caps and the Git floor are unverified until tasks 2.1 and 2.2] -> Both
  run before the handoff and edit the deltas if needed.
- [`doctor` now exits 1 where a probe fails, a worktree is unreadable or `git`
  is missing, and `push` refuses while any row is `inspection-error`] ->
  Intended (D-S, D-D); the error rows and refusals name the cause and the
  remedy.
- [A filesystem call stuck in the kernel keeps a daemon thread alive] ->
  Abandoned after its budget so the main thread never blocks; the run bound
  excludes it, as BA:456-458 does.
- [Non-UTF-8 path scenarios cannot run on macOS, whose filesystems reject such
  names] -> Skipped there with that reason; they run on Linux in CI.

## Migration Plan

Users meet four behaviour changes first: plain `project clean` exits 1 when its
report is incomplete; `clean` refuses below Git 2.36; `--worktree P` refuses a
freshly created merged worktree whose branch has no commit of its own, with the
remedy "no commit was made on this branch here since it was created; review,
then git worktree remove yourself"; and a merged worktree whose branch reflog
keeps no decisive entry (no activity for `gc.reflogExpire`, 90 days by default,
D10) is refused as `reflog-unavailable` in single mode as well as withheld from
the batch, with the remedy "the branch's reflog is missing, expired or
undecidable; review, then git worktree remove yourself". The README's clean
section states them first.

1. Ratification by Brett Heap's word on PR #11 (`tasks.md` 1.6), with the V5
   deferral and the two open questions before him.
2. Governance tasks 2.1 (measurement) and 2.2 (the Git floor) run before the
   handoff; any change they force to a cap or the floor is made in the deltas
   first.
3. Local `main` is synced to `origin/main`, then `/speckit.specify` creates
   feature `003-project-clean-all-safe` on branch `003-project-clean-all-safe`,
   recorded once in `tasks.md` under "Speckit Handoff"; `/opsx:apply` runs only
   then.
4. Feature 003 implements D1 to D19 and the CI floor job (D17), merging `main`
   into its branch as `main` moves and never rebasing.
5. README: "Clean up Git worktrees" opens with the behaviour changes, then the
   preview and apply, `--expect-plan`, the gates, the deferral, the narrow
   guarantee and residual window, the result record and recovery, the
   `remote-gone` limitation and the advice to close sessions first (D3); "Apply
   actions are always explicit and target one branch or worktree" (README:106)
   is corrected; Install (README:17-19) states the floor; the exit-code line
   (README:194-196) gains `clean`'s 1, 143 and 129 and Git's status passing
   through.
6. Tests in `tests/test_project.py`: one per delta scenario, named after it; the
   counting `git` wrapper recording each child's arguments and `-C` directory;
   the fake `git`s (D1); hooks for the residual window, the branch race,
   deadline expiry and signals; the parsers fed byte by byte (D2); value parity
   with the baseline. Four existing tests touch changed behaviour.
   `test_clean_revalidates_a_worktree_after_confirmation` (`:590-611` at
   `da33d92`, now `:973`) patches `confirm()` and expects `Refused`; it moves to
   the result record, expecting a `refused` target with `state-changed` and exit
   2 through the new question's hook.
   `test_clean_refuses_unmerged_worktree_removal` (`:409-425`, now `:792`),
   `test_clean_never_removes_the_worktree_containing_the_current_directory`
   (`:450-467`, now `:833`) and
   `test_clean_refuses_to_guess_a_nonstandard_default_branch` (`:542-546`, now
   `:925`) pass unchanged, because `target-excluded` and `no-merge-target` keep
   the wording they read (D8, D18). The other 90 pass unchanged.
7. `add-project-overview` reconciles its deltas against this change's final
   headers after this lands, then is ratified and implemented as feature 004.
8. The change is archived after the realization PR merges.

Rollback: revert the realization commit on `main`. Installed `project` artifacts
follow workBenches' pin, so a revert before the pin moves reaches nobody
downstream.

## Open Questions

Each is before Brett Heap with a recommendation; the deltas implement the
reading stated, and a different ruling edits the deltas before ratification.

- A merged worktree whose remote branch was deleted reads `remote-gone`, because
  the ladder tests `remote_present` before ancestry (`project:442` before
  `:457`), and push refuses it, so no `project` command retires it.
  Recommendation: a local ancestry proof outranks `remote-gone` for worktree
  rows, since the MVP never deletes the branch. Until ruled, the packet's ladder
  stands and the recommendation text says so.
- Squash-merged branches never put their tip into the target's ancestry
  (BA:195-199). Recommendation: a local patch-equivalence proof (`git cherry` or
  patch IDs against the target) as a follow-on change, not in the MVP.
- The V5 deferral (D12) replaces the packet's `target-cap` refusal with 16
  removals per run and `deferred-target-cap` for the rest: a departure from a
  packet decision, on the council's survey (about 20 eligible rows in
  Opensoft-Tenant), standing only on Brett Heap's ratification.
