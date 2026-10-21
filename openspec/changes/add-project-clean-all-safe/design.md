Lane: openRepoProject-2

# Design

## Context

See `proposal.md` for why and what, and the deltas under `specs/` for the
requirements. The council's noted constraints, `clarifications.md` N1 to N5, are
answered by D1 to D5; D6 to D19, and D21 for Brett Heap's ruling LQ-13, give
the how of the proposal's decisions, and D20 maps the packet's 35 validation
scenarios to the deltas. The binding rulings
(D-A to D-AF, X1, X2, V1 to V12 with V2 as amended, lane 3's M1 to M7, and the
lead's R-4, R-8 and R-9, R-11 to R-15, R-17, R-19 and R-21 to R-25) are already
in `proposal.md`, with the sections each edited; R-15 edited Context, D10, D14,
D18, D19, Risks and the Migration Plan here; R-17 edited Context and D14, and
R-19 edited Context, D14 and D19; R-21 edited Context, D6 and D17; R-22 edited
Context and D20; R-23 edited Context, D6, D9, D11 and D20; R-24 edited D5, D9,
D11, D12, D18, Risks and the Migration Plan; R-25 edited Context, D6, D9, D11,
D20 and Risks; the push-child exception, before Brett Heap, edits D6, D11, D20,
Risks and Open Questions; and Brett Heap's ruling Q9 B of 2026-10-21, given
through lane openRepoProject-4's spec 005 clarify round and recorded in
`proposal.md` Decisions, edits Context, D6, D11, D17, D20 and Risks. Brett
Heap's rulings of 2026-10-21 on lane openRepoProject-3's recommendations LQ-10
to LQ-15, recorded in `proposal.md` Decisions, edit here: LQ-15, Context, D6,
D11, D16, D18, D20 and Risks; LQ-10, Context, D9, D11, D20 and Risks; LQ-12,
Context, D6, D16 and D20; LQ-11, Context, D6, D7, D14, D20 and Risks; LQ-13,
Context, D7, D12, D14, D18, D20, D21 and Risks. Brett Heap's ruling
of 2026-10-09 on open question 1, that a local ancestry proof outranks
`remote-gone` for worktree rows, is in `proposal.md` Decisions and edited
Context, D6, D7, D20, Risks, the Migration Plan and Open Questions here.

Citations are `file:line` at `da33d92`: `BA`, `DI`, `OV` and `HO` are the
packet's batch-cleanup, project-discovery, overview and handoff documents, and
`project:N` the executable. At `7a9134b`, `project` from `discover` onward sits
141 lines lower and the cited tests 383 lower; feature 004 re-pins every
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
| the combined `status` probe in a clone made with `--no-checkout --filter=tree:0`, whose `remote.origin.uploadpack` is a script that logs each run | unpinned, the probe fetches HEAD's tree from the promisor remote and the script runs once; with `-c protocol.allow=never` alone it exits 128 with `transport 'file' not allowed` and the script never runs, yet a `protocol.file.allow=always` setting in the clone's configuration lets the fetch and the script run again, as does `GIT_ALLOW_PROTOCOL=file` in the environment even beside every pin, since Git consults that list before any configuration or `-c`; with the six per-protocol pins beside `protocol.allow` the configured `always` is refused, and with `GIT_ALLOW_PROTOCOL` removed from the environment the run is refused with the script never run; `GIT_ALLOW_PROTOCOL=always` names no protocol and refuses `file` by itself, so the check sets `file`; identical on Git 2.36.6, 2.40.4 and 2.43.0 (R-23, R-25) |

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

Every Git child but the push child of `clean --action push` runs through one
loop, the one-wide driver of D2; the push child runs through `execute()`, with
D6's scrubbed environment but for `GIT_ALLOW_PROTOCOL`, as D11 states.

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
in `clean`, `status`, `doctor` and `update` uses it, but for the push child
(D11).

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
005 drives up to four handles from its own selector loop, feeds the same
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

Task 2.1 ran it on 2026-10-09 in the `py-bench` container: the cold cache by
`sync` and per-file eviction (`posix_fadvise`, the mechanism of `vmtouch -e`),
confirmed with `mincore`, because `drop_caches` is impossible there; drvfs was
not available and is unmeasured; the fit rejected no cap, so the caps were
measured and stand, with two degraded cases and one residual that its survey
found recorded under Risks (R-24).

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
| 4c | `config --file <common_dir>/config --type=bool --get extensions.worktreeConfig` | once per common directory, after row 4, in the command directory (D7, LQ-11) |
| 5 | row 3 repeated in the command directory | only when row 3 ran elsewhere |
| 6 | one `for-each-ref` over `refs/heads` and `refs/remotes` | command directory |
| 7 | `for-each-ref --merged=<merge-target sha> --format=%(refname) refs/heads` | command directory |

No row runs, row 1 included, when a configuration path fails D11's test
(Brett Heap's ruling LQ-15).

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
child per option, counted, rather than guessed at. F is therefore at most 8,
BA:615-616's 7 and row 4c, plus row 4b in the gitfile layout and the rare
repeat.

Per row: the identity reads (`lstat` without following, the `.git` file, the
admin `gitdir` file), each a filesystem call on a daemon `threading.Thread`
waited for with `min(5 s, work remaining)` and abandoned after it (C4; never a
`concurrent.futures` pool, whose shutdown would wait for a stuck call); then, in
a linked row of a repository whose row 4c read true, the effective-work-tree
probe of D7; then the combined status probe in that worktree (D11). Rows 3 to 7
are memoized by common
directory within an invocation, which matters to `status` and `doctor`, whose
legs are other repositories. Where `root` is null (a bare repository, a missing
main worktree, or a gitfile checkout whose main worktree cannot be named), rows
4 to 7 run in the common directory for a bare repository and otherwise where
row 3 ran, as the evidence model states; `clean` refuses those layouts (D8), so
only a reader that reports them, such as `add-project-overview`, probes there.

The scrubbed environment is a copy of the caller's with thirty-one variables
removed, unconditionally and before any Git call, from a fixed list that is
hard-coded rather than queried: the fifteen of BA:244-250, which Git 2.40 and
later print from `rev-parse --local-env-vars`; `GIT_INTERNAL_SUPER_PREFIX`,
which 2.36 through 2.39 also print and which makes every command on 2.36 fail
closed when it is set (D17, R-21); `GIT_ALLOW_PROTOCOL`, which Git does not
print and which, set to a protocol list, is consulted before every `-c` pin
(D11, R-25); and the fourteen trace variables that Git 2.36 through 2.43 read,
`GIT_TRACE`, `GIT_TRACE_BARE`, `GIT_TRACE_CURL`, `GIT_TRACE_CURL_NO_DATA`,
`GIT_TRACE_FSMONITOR`, `GIT_TRACE_PACKET`, `GIT_TRACE_PACKFILE`,
`GIT_TRACE_PACK_ACCESS`, `GIT_TRACE_PERFORMANCE`, `GIT_TRACE_REDACT`,
`GIT_TRACE_REFS`, `GIT_TRACE_SETUP`, `GIT_TRACE_SHALLOW` and
`GIT_TRACE_WORKING_TREE_ENCODING`, twelve of them trace keys, which create or
append to the file that an absolute-path value names, and two modifiers that
open nothing (D11, D17; Brett Heap's ruling Q9 B). It then sets `GIT_TRACE2`,
`GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF` to `0` for every kind of child, the
push child included (D11, Q9 B). `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`
are not in that list and stay; D11's `-c` pins and those three variables
override them.

Every owner tool that `update --apply` invokes, for any component, runs
through `execute()` with the push child's scrub, the thirty-one names but
`GIT_ALLOW_PROTOCOL` removed, and with nothing set (Brett Heap's ruling LQ-12,
2026-10-21). At `a040790` an owner tool
gets the caller's environment (`project:157-162`), so a caller's `GIT_DIR`,
`GIT_WORK_TREE` or `GIT_INDEX_FILE` could point it at another repository than
the one the dirty check before it inspected through the scrub (lane
openRepoProject-3's F5 M-3 at `2cf34d3`). `GIT_ALLOW_PROTOCOL` stays, as for
the push child: Git children lose it only because the protocol pins take its
place, an owner tool takes no pin, and removing it would lift a restriction
that the caller set, where the ruling only tightens. Nothing is set: no
`GIT_OPTIONAL_LOCKS`, since the tool may write, and no trace2 variable, since
Brett Heap's ruling Q9 B binds Git children and the tool is not one.

Every child in the table, `git --version` and D9's removal child included, also
runs with `-c protocol.allow=never` and the six per-protocol pins (D11, R-23,
R-25); the push child, which is not in the table, is the exception D11 states,
and its environment keeps a caller's `GIT_ALLOW_PROTOCOL`.

`repo_state()` and `cleanup_report()` become thin readers of this pipeline, and
the ladder becomes a pure function of a row's evidence (OQ-28). Its one
reordering, by Brett Heap's ruling on open question 1, tests
`merged_into_target` before the `remote-gone` rung for a row whose upstream is
configured and whose `remote_present` is false: true gives `merged-removable`,
or `merged-current` for the current worktree, and anything else `remote-gone`;
the row's `upstream`, `ahead` and `behind` stay as row 6 gives them. Value parity
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

A linked row's effective work tree must be its registered path (Brett Heap's
ruling LQ-11, 2026-10-21). Two-way registration does not prove it: Git applies
a `core.worktree` or `core.bare` to a linked worktree only where the
repository's own `config` sets `extensions.worktreeConfig`, and then from the
worktree's `config.worktree` and from that `config` alike
(`check_repository_format_gently` and `check_repo_format` in `setup.c`, which
read `config.worktree` and clear `has_common` under the extension, at
`setup.c:637-657` and `:600` in 2.36.6 and `:665-685` and `:629` in 2.43.7).
Lane openRepoProject-5's reader RB found the gap (its `e7`): with a
per-worktree `core.worktree` naming a decoy, every probe read the decoy's tree,
the row read clean, and Git's non-force removal deleted the registered
directory with its ignored `local.env`, because Git's own check runs with
`GIT_WORK_TREE` set to the registered path (`check_clean_worktree` in
`builtin/worktree.c`) and is not misled. Row 4c reads the extension once per
common directory, from the common `config` alone and without includes, as
Git's own format check reads it; an unset value is false and any other failure
counts as true. Where it is true, each linked row whose registration agrees
gets one more worktree probe, `git rev-parse --path-format=absolute
--show-toplevel`, after its identity reads and before its status probe, and a
toplevel whose realpath differs from the registered path's, a failed probe (as
under `core.bare=true`, `fatal: this operation must be run in a work tree`) or
output that is not one line makes the row's registration disagree, so the row
is `registration-mismatch`, `inspection-error` and unprobed. Asking Git covers
every way the extension can redirect a row, without parsing configuration in
`project`, and the probe runs only in such repositories. Checked here on Git
2.36.6 and 2.43.0: the extension read exits 1 when unset and prints `true` when
set; the probe prints the decoy for a `core.worktree` in `config.worktree` and
for one in the common `config`, and fails with 128 under `core.bare=true`.

Revalidation is BA:677-707's targeted check, in its order, stopping at the first
difference: the identity probe; the manifest re-read (a file read, 1 MiB cap);
the registry listing; a narrowed ref listing whose patterns name the merge
target, the manifest's candidate, the branch the plan's `origin/HEAD` named,
`main`, `master`, `refs/remotes/origin/HEAD`, and the selected branches and
their upstreams; the target's identity and `modules` check by filesystem reads,
and, where the plan's row 4c read true, its effective-work-tree probe, whose
difference is `identity-changed`; then, inside the target worktree, the
combined status probe, which must print nothing, the hidden-state probe, and
D21's `logs/HEAD` re-read and reachability probe, which must print nothing.
Row 4c itself is not re-read, which keeps revalidation at six Git children in
a repository without the extension: an extension turned on after the plan, with
a `core.worktree` for a target, is a concurrent writer's change outside the
contract (Risks). Ancestry needs no child: it is a function
of the branch head and the merge-target SHA, both compared. The reflog of D10 is
not re-read: a moved branch is already `branch-changed`. The HEAD reflog of D21
is re-read, as D21 states. A selected row whose
upstream was deleted (D6) records `upstream_oid`, `ahead` and `behind` null,
and revalidation compares them as recorded, by the review-safety rule that a
value null in the plan and null at revalidation is no difference while a value
that cannot be re-read is one: the narrowed listing still showing no
remote-tracking ref for it is no difference, and one that reappears is
`state-changed`.

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
origin/HEAD, main, or master." (`project:403`), which the existing test reads
(Migration Plan).

The 1 MiB cap binds only the merge-target resolution. `status`, `doctor` and
`update` read the manifest through `snapshot()` for its kind and legs, which
this change leaves alone.

### D9. The removal child: never signalled, the ceiling and the reserve

The removal child is a D2 handle of kind `removal`: the scrubbed environment
without `GIT_OPTIONAL_LOCKS`, and the argument vector `git -c
status.showUntrackedFiles=normal -c core.untrackedCache=false -c
core.fsmonitor=false -c core.trustctime=true -c core.checkStat=default -c
protocol.allow=never -c protocol.file.allow=never -c
protocol.ssh.allow=never -c protocol.git.allow=never -c
protocol.http.allow=never -c protocol.https.allow=never -c
protocol.ext.allow=never -C <command directory> worktree remove <path>`, both
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
slower; task 2.1 measured it, the 20,000-file removal taking 0.66 s warm and
0.72 s cold at low load and 14.1 s at worst under saturation, 21 times under
the ceiling.

The 10 s reserve counts from the child's exit or the ceiling, each rescan child
getting `min(5 s, reserve remaining)`. A run with no removal in flight therefore
ends within 64 s of its start, not counting the time blocked at the confirmation
question: 50 s of work, the 10 s reserve, and up to 4 s to stop a probe child
(SIGTERM, the 2 s grace, SIGKILL, a reap wait of up to 2 s), the figure the
overview states; a removal in flight adds up to 300 s (M5). A call stuck in the
kernel, and the push and delete-branch children that D-W leaves unbounded
(D11), are the exceptions.

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
core.fsmonitor=false -c core.trustctime=true -c core.checkStat=default -C
<worktree> status --porcelain=v1 -z --untracked-files=normal
--ignored=matching`, the removal as D9 states, and the hidden-state probe
carries the same four pins for uniformity; the last two are Brett Heap's ruling
LQ-10, below. The council's
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
helped; task 2.1 measured the pinned probe at 42 to 49 ms warm for 10,000
entries and 215 to 232 ms for 100,000. One consequence crosses changes: feature
005's fixtures that rely on a running fsmonitor (DI:1233-1237, DI:1249-1254)
must be rewritten, as the lead's ruling records.

`core.trustctime=true` and `core.checkStat=default` restore Git's full stat
comparison (Brett Heap's ruling LQ-10, 2026-10-21). Git compares an index
entry's ctime with the file's only while both settings keep these values
(`match_stat_data`, `read-cache.c:185` and `:192` at 2.36.6, `statinfo.c:40`
and `:47` at 2.43.7), and `core.checkStat=minimal` also drops the inode, owner
and sub-second checks. Under either repository setting an edit that keeps a
file's size and restores its mtime matches the index entry, so the status probe
and Git's own check both read the worktree clean and the removal deletes the
edit (lane openRepoProject-3's F1 H-3 at `2cf34d3`). Checked here on Git 2.36.6
and 2.43.0: with `core.trustctime=false` and `core.checkStat=minimal` in the
repository's configuration, such an edit gives no record under the two older
pins and ` M` under all four. The pins follow `core.fsmonitor=false` on every
status probe, the hidden-state probe and the removal, and like them outrank
every configuration file; the removal's pins reach Git's own check, which runs
in a child of the removal. A ctime or inode that changes without an edit makes
Git compare the content instead, which is slower and never a wrong answer
(Risks).

Every Git child, of every kind, except the push child of `clean --action push`,
also carries `-c protocol.allow=never -c protocol.file.allow=never -c
protocol.ssh.allow=never -c protocol.git.allow=never -c
protocol.http.allow=never -c protocol.https.allow=never -c
protocol.ext.allow=never` (R-23, R-25), `git --version` and the removal
included. The push child of `clean --action push` is the one exception, because
its purpose is to reach a remote and the pins would refuse every transport, the
`file` one included: it keeps the scrub but for `GIT_ALLOW_PROTOCOL`, runs
unbounded in `project`'s own process group as `execute` runs it today, so that
a credential prompt can read the terminal and an interrupt reaches it, carries
none of the pins, and no evidence comes from it (Open Questions).

Git 2.43 has no `GIT_NO_LAZY_FETCH` or
other switch against lazy fetches, so a read-only probe in a partial (promisor)
clone that needs an object the clone does not hold can fetch it from the
network. `protocol.allow` is only the default policy: a `protocol.<name>.allow`
setting in a configuration file overrides it for that protocol, and
`GIT_ALLOW_PROTOCOL` in the environment, which Git consults before any
configuration, overrides every `-c`. The six per-protocol pins therefore stand
beside it, a `-c` outranking `protocol.allow` and every `protocol.<name>.allow`
in every configuration file, and the scrub removes `GIT_ALLOW_PROTOCOL` (D6), as
it removes `GIT_CONFIG_PARAMETERS` and `GIT_CONFIG_COUNT`, so a caller cannot
inject a contrary `-c` or an allow list. With the pins Git's transport check
refuses the fetch locally, the probe fails with `probe-failed`, and the row is
`inspection-error`, never a network call; the Context table records the check
on Git 2.36.6, 2.40.4 and 2.43.0. The residual, recorded under Risks, is a
remote-helper protocol of another name, which no pin names.

Trace output is turned off for every Git child, the push child included
(Brett Heap's ruling Q9 B, 2026-10-21, through lane openRepoProject-4's spec
005 clarify round). Git reads a trace2 target only from `GIT_TRACE2`,
`GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF` and from the `trace2.normalTarget`,
`trace2.eventTarget` and `trace2.perfTarget` settings, which it reads early,
from the system and global configuration alone, ignoring the repository's and
the command line's, so no `-c` pin reaches them; a non-empty variable replaces
its setting, and `0` turns that target off. D6 therefore sets the three
variables to `0` in every child's environment, which also overrides the files
that `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` name. The older trace
variables, `GIT_TRACE` and the thirteen `GIT_TRACE_*` names, have no
configuration setting, and the scrub removes them (D6). The other
`GIT_TRACE2_*` names stay as the caller set them: read in the sources of every
release from 2.36.6 to 2.43.7, none opens a file while the three targets are
off. The push child carries the same environment, because trace output changes
nothing about where a push reaches; the cost is recorded under Risks.

A relative configuration path is refused before any Git child starts (Brett
Heap's ruling LQ-15, 2026-10-21, on the model of C-44 in
`add-project-overview-remote-merge-status`, which refuses a relative
`GH_CONFIG_DIR`, `XDG_CONFIG_HOME` or `HOME`). Git reads the user's
configuration from `$HOME/.gitconfig` and from `$XDG_CONFIG_HOME/git/config`,
or `$HOME/.config/git/config` where `XDG_CONFIG_HOME` is empty or unset; it
takes its default `core.excludesFile` and its global attributes file from the
same directory (`git/ignore` and `git/attributes`); and it reads the files that
`GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` name in place of the user's and the
system's. Each path is built from the variable as it is spelled
(`xdg_config_home_for` and `interpolate_path` in `path.c`, `git_global_config`
and `git_system_config` in `config.c`, and the defaults in `dir.c` and `attr.c`,
read at 2.36.6 and 2.43.7), so a value that does not begin with `/` resolves
against the directory a Git child runs in: the worktree for every worktree
probe, and the main worktree for every other child. Files a repository holds,
tracked ones included, are then read as the user's or the system's own, and no
pin of this section reaches what they set. Two risks follow:

- Code execution. A planted configuration's `filter.<name>.clean`, which a
  `.gitattributes` the repository tracks can select, runs in every status
  probe, and so in every preview, report, `status`, `doctor` and revalidation;
  its `core.hooksPath` runs a planted hook in the removal; and its
  `core.sshCommand` or `credential.helper` reaches the push child, which
  carries no pin. Lane openRepoProject-3's reader RA reproduced the first two
  at `2cf34d3` with a relative `HOME`, `XDG_CONFIG_HOME` and `GIT_CONFIG_GLOBAL`
  alike (the lead's R-105), lane openRepoProject-4 reproduced the filter on Git
  2.43.0 with a relative `HOME`, where an absolute `HOME` or
  `GIT_CONFIG_GLOBAL=/dev/null` ran nothing, and lane openRepoProject-5's
  reader RC raised the push child's exposure (R-101).
- Removal. The planted ignore file is the default `core.excludesFile`, so
  untracked files it names read as ignored: checked here on Git 2.36.6 and
  2.43.0, a relative `XDG_CONFIG_HOME` turns the pinned probe's `?? work.txt`
  into `!! work.txt`. Such a row is then `ignored-local-files` and still kept
  out of every plan, but Git's own non-force check, the last defense, no longer
  refuses for such a file, and `worktree remove` deletes ignored files; and a
  planted attributes file can select a filter for a tracked file.

The test therefore runs first in every subcommand that inspects a Git
repository, before `git --version`: `HOME` or `XDG_CONFIG_HOME` set to a
non-empty value whose first byte is not `/` makes the subcommand start no Git
child (`relative-config-path`). `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`,
Git's own variables naming a configuration file and the analogue of C-44's
`GH_CONFIG_DIR`, are tested the same way; they are the lead's extension of the
ruling, which Brett Heap may strike, and RA's reproduction with
`GIT_CONFIG_GLOBAL` is why that one is in the list. The test is made on the raw
bytes: ` /x`, `~/x` and `.` fail it, as does a first byte that is not UTF-8,
and `/` alone passes. An empty or unset variable passes, because it names no
relative file: Git treats an empty `XDG_CONFIG_HOME` as unset, an empty `HOME`
gives `/.gitconfig` and `/.config/git/`, and an empty `GIT_CONFIG_GLOBAL` or
`GIT_CONFIG_SYSTEM` names no file Git can open. The test holds whichever of the
variables Git would use, so a relative `HOME` beside an absolute
`GIT_CONFIG_GLOBAL` fails it too, the ignore and attributes files still coming
from `HOME`. `clean` then refuses with `relative-config-path`, exit 2, in every
mode; `status`, `doctor` and `update` report it as they report a Git below the
floor (D16). The values are read only for this test, are passed to every child
unchanged when it passes, and are never printed: the message names each
variable that fails the test (D18). The test covers these variables only; other
relative paths in the environment that a Git child resolves against its
directory are outside it.

### D12. The 16-per-run deferral (V5)

Gates are evaluated in canonical order. Rows that pass every gate before
`deferred-target-cap` are counted; the first 16 go on to the `modules` check and
the hidden-state probe, and the rest are excluded as `deferred-target-cap` with
no index probe, so at most 16 hidden-state probes run and E is at most 16; at
most 16 of D21's reachability probes run likewise. A row
an index gate then excludes keeps its place, so a run can select fewer than 16
while rows stay deferred, and 16 rows that an index gate always excludes, ahead
of a backlog, stop it until a person handles them; when every one of the 16 is
`contains-submodule`, the human text says why the deferred rows will not drain
(D18, R-24). The plan stays complete and apply allowed; each re-run plans and
revalidates afresh, draining 16 at a time. `plan_digest` covers only `selected`,
so a deferred row's change leaves a preview valid, and the report mode defers
alike. The `target-cap` refusal (BA:96-101, BA:1004, BA:1367-1371) is retired, a
departure ratified with the merge of PR #11; the code survives only as the
overview's limiting gate.

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

At BA's 150 ms per Git child, with F = 8 (row 4c of LQ-11 included):

| Mode | Children | Time | Fits the 50 s work deadline |
| --- | --- | --- | --- |
| report, 256 rows | 8 + 256 + 16 + 16 = 296 | 44.4 s | yes |
| report, 512 rows | 8 + 512 + 16 + 16 = 552 | 82.8 s | no |
| all-safe, 128 rows, 16 targets | 8 + 128 + 16 + 16 + 96 + 3 = 267, and 16 removals | 40.05 s + about 4.8 s = 44.85 s | yes; the 16th removal spawns at 44.1 s with 5.9 s left (BA:753-756) |
| single, 128 rows plus P | 8 + 129 + 1 + 1 + 6 + 3 = 148, and 1 removal | 22.2 s + about 0.3 s | yes |

The report builds no apply plan, so its worst case is the planning term alone,
and 256 is the largest power of two that fits (D-V, OQ-29). Row 4b and the rare
row 3 repeat add 0.15 s each; the reflog reads add no child. In a repository
whose row 4c reads true, each linked row adds its effective-work-tree probe and
each target's revalidation adds it again, so a large plan there reaches the
deadline sooner and goes incomplete with `deadline-exceeded`, never unsafe
(LQ-11). D21's reachability probe adds one child for each of at most 16 rows
and one to each revalidation (LQ-13); its walk is unmeasured, and at task 2.1's
`for-each-ref` cost over 1,000 loose branches, 240 ms warm, those 32 children
would add about 7.7 s, which the measured fit's 26.4 s margin absorbs, a slower
walk making a plan incomplete, never unsafe. Under D9 a removal
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
memoized version check runs, unless D11's configuration-path test failed, in
which case no Git child runs at all (LQ-15); a failed test, an old or unusable
Git, or a failed or timed-out status probe gives the dict `classification:
"inspection-error"` and `errors` (`{code, message, path?, path_valid_utf8?,
reason?}`: `relative-config-path`, `git-too-old`, `git-unavailable`,
`probe-failed`, `probe-timeout` or `os-error`), `present` null when the test or
the version check failed, and null for every value not established. An
inspected dict has neither field, so the JSON stays additive and unversioned.
The marker is `classification`, the field worktree rows carry, as V11 asked the
delta to name, with `errors` for the cause. Every `path` in these dicts, the
root, leg and worktree rows and `errors` entries alike, carries
`path_valid_utf8` beside it, written by `clean`'s escaping rule, each
`ignored_samples` entry is `{path, path_valid_utf8}`, and the report's top-level
`root`, and each nested family member's `root`, gains `root_valid_utf8` beside
it; all are additive too.

`check_rows()`: the `git` tool row reports the version check, `ok` with the
version or `error` with its code, or `error` with `relative-config-path` where
D11's test failed and no Git child ran, where today a missing `git` is a warning
(`project:755-757`); a root, leg or worktree row classified `inspection-error`,
a null `present` and a null `dirty` each add an `error` row naming the cause;
nulls that mean "none" add nothing, so a fresh project with no remote passes.
The exit rule is unchanged (`project:828-829`). `status` prints `Git:
inspection-error (<codes>)` in place of the branch line. `update` tests `dirty
is not False` for the root and every child (`project:863`, `:869`), and its
`tools` and `workflow` components need no Git (`project:884-885`, `:905-906`):
with an old Git their report shows `inspection-error` rows and the delegate
still runs. Every delegate runs with D6's push-child scrub (LQ-12).

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
| the variables of `rev-parse --local-env-vars` | measured by task 2.2: 2.36.6 prints sixteen, 2.40.4 and 2.43.0 fifteen (BA:244-250); the extra name, `GIT_INTERNAL_SUPER_PREFIX`, is printed through 2.39, and with it set 2.36 fails closed in every command with `fatal: version doesn't support --super-prefix`; resolved by scrubbing it, sixteen names then and seventeen with R-25's `GIT_ALLOW_PROTOCOL` (R-21), the floor staying 2.36; thirty-one since Brett Heap's ruling Q9 B added the fourteen trace variables, which every release from 2.36.6 to 2.43.7 reads alike (D6) |

Governance task 2.2 verifies the floor before the handoff: Git v2.36.x built
from its release tarball in a scratch directory, first on PATH, and a scratch
script comparing each row's output with Git 2.43's. If any row differs, the
floor rises to the lowest version on which every row holds, and the deltas
change before the handoff. Task 2.2 ran it on Git 2.36.6, 2.40.4 and 2.43.0
(75 captures): rows 1 to 6 are identical on all three, and row 7 differs as the
table records. By the rule above the floor would rise to 2.40; R-21 keeps 2.36
and adds the one name to the scrub, because raising the floor would exclude
Debian 12's Git 2.39 for a one-name difference. That departs from the rule and
was ratified with the merge of PR #11 (proposal, Decisions). Feature 004 adds a
CI job that builds the floor version, cached, and runs the `clean`, `status` and
`doctor` tests with it first on PATH.

### D18. What the person sees

All new text is ASCII, with `ROOT`, `PATH`, `BRANCH`, `N`, `K`, `M` and `REASON`
substituted (paths by the escaping requirement), and the tests pin it.

The preview, after the baseline's `Cleanup plan for ROOT`, `Merge target: NAME
(SOURCE)` and `Freshness:` lines, prints `Selected (N):` with one line `  remove
PATH [BRANCH]` per row; `Excluded (M):` with, per reason, `  REASON (K): NEXT
STEP` and one line `    PATH [BRANCH]` per row, an `ignored-local-files` row
adding `: N ignored; first: SAMPLE` (`at least N` when truncated); for the
deferral, `  deferred-target-cap (K): this run removes up to 16; run again:
project clean ROOT --all-safe --apply`, and, when every one of the 16 rows taken
past the cap is excluded as `contains-submodule`, the line `  these deferred
rows will not drain while the 16 rows ahead of them are contains-submodule;
review those worktrees, then remove them yourself` (R-24); the
residual-window line, `Not protected: ignored files created, index flags set or
worktree-only commits made after the last check, and any change after Git's own
check.` (its third item by LQ-13); and, when a
complete plan selects nothing, `No eligible worktrees`.

The next steps by reason: `dirty` "commit or preserve the changes";
`ignored-local-files` "move or delete the ignored files by hand";
`unstarted-branch` "no commit was made on this branch here since it was created;
review, then git worktree remove yourself"; `reflog-unavailable` "the branch's
reflog is missing, expired or undecidable; review, then git worktree remove
yourself"; `contains-submodule` and `hidden-local-state` "review, then remove
the worktree yourself"; `worktree-only-commits` "a commit is, or may be, held
only by this worktree's HEAD reflog or refs/worktree; keep it on a branch or
tag, or review, then git worktree remove yourself" (LQ-13);
`registration-mismatch` and `inspection-error` "review,
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
or re-run". `relative-config-path` prints one line per variable that fails
D11's test, in the order `HOME`, `XDG_CONFIG_HOME`, `GIT_CONFIG_GLOBAL`,
`GIT_CONFIG_SYSTEM`: `NAME is set to a path that does not begin with /; make it
absolute or unset it.`, never the value; doctor's `error` row and status's
`errors` entry carry the same text.

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
classification and "Inspect and diagnose", and the ruling on open question 1
under the classification; R10, R11, D-T and the manifest cap
under Git-first resolution; V1 to V4, M3 and M4 under retirement; OQ-10, OQ-16
and M1 under the JSON and the result; V9, R-23, R-25, the push-child
exception and Brett Heap's ruling Q9 B under the evidence model; D-D under
push; D-R under maintenance; R-22 under revalidation. Brett Heap's rulings of
2026-10-21: LQ-15 under the evidence model and the report; LQ-10 under the
evidence model; LQ-12 under maintenance; LQ-11 under the evidence model; LQ-13
under the batch and revalidation.

### D21. Commits held only by a worktree (LQ-13)

Brett Heap's ruling LQ-13 of 2026-10-21 keeps a worktree in place when a
commit that only its own HEAD reflog or its `refs/worktree/` holds is
unreachable from every branch, tag and remote ref. `git worktree remove`
deletes the worktree's administrative directory, and with it `logs/HEAD` and
every ref under `refs/worktree/`, which live there and are never packed
(`common_list` in `path.c`; `should_pack_ref` in `refs/files-backend.c`, at
2.36.6 and 2.43.7); such a commit is then held by nothing and is left to
garbage collection. Lane openRepoProject-3 found the gap (F1 H-1 at
`2cf34d3`). Each decision below is the simple, conservative one:

- Reason. A new exclusion reason, `worktree-only-commits`, in the gates'
  kebab-case. No existing reason fits: `reflog-unavailable` names the branch's
  reflog and its remedy says that reflog is missing, expired or undecidable;
  `unstarted-branch` says the opposite, that no work was done; and
  `inspection-error` would make the whole plan incomplete for a state that is
  fully established.
- Place. The last gate, after `hidden-local-state`. It is a protection, so it
  runs before any row is selected, in every mode, `mode: "single"` included,
  where an excluded P refuses `target-excluded`; a row an earlier gate excludes,
  as every row with work in its index or tree is, needs no such protection. It
  sits past `deferred-target-cap` with the index gates because it costs a Git
  child, which bounds it at 16 rows per run (D12).
- Reads. One bounded filesystem read of `logs/HEAD` in the worktree's
  administrative directory, at most 64 KiB, the cap of D10's branch reflog, and
  counted in the filesystem budget, each line parsed as D10 parses one; every
  non-zero old and new object it names is a candidate. Then, after the
  hidden-state probe, one Git child in the worktree, with the scrub, the pins
  and `GIT_OPTIONAL_LOCKS=0` of every read-only probe:
  `git -C <worktree> rev-list --max-count=1 --glob=refs/worktree <candidates>
  --not --branches --tags --remotes <branch reflog objects>`.
  `--glob=refs/worktree` adds the worktree's own per-worktree refs, which only
  that worktree sees. The negative side is every branch, tag and
  remote-tracking ref and every object that the row's branch reflog names,
  which D10 already read and which survives the removal in the common
  directory, so that an amend, a reset or a rebase of the row's own branch is
  not taken for lost work: such a commit is not held only by the worktree. The
  child prints a commit exactly when one is reachable from the candidates or
  from `refs/worktree/` and from none of the negatives.
- Bounds. The read takes the filesystem budget and the child `min(5 s, work
  remaining)`, as every read and child do; `--max-count=1` keeps the output to
  one line.
- Fail closed. A missing (`ENOENT` or `ENOTDIR`) or empty `logs/HEAD` gives no
  candidate, since no reflog then holds anything. A printed commit gives
  `worktree-only-commits`, and so does every outcome that cannot decide: the
  64 KiB bound reached, a line that does not parse, any other error on the
  read, and a child that exits nonzero, as on a missing object (`fatal: bad
  object`, 128), runs past its budget, or prints anything but one object name;
  `reflog-unavailable` does not fit there, since its remedy names the branch's
  reflog. A read not finished within the filesystem budget leaves the row
  unprobed and the plan incomplete with `inspection-incomplete`, and the
  deadline gives `deadline-exceeded`, as for every read and child.
- Revalidation. After the hidden-state probe, revalidation reads `logs/HEAD`
  again and runs the same child, with the plan's branch reflog objects; a
  printed commit, or any outcome that cannot decide, refuses the target with
  `worktree-only-commits`. That is the sixth Git child of a revalidation (D7,
  D14), and it catches a commit made, or a ref under `refs/worktree/` created,
  after the plan, which no step read before (lane openRepoProject-3's reader RB
  at `2cf34d3`, whose cases were all removed with exit 0; R-107). After that
  revalidation such a commit is in the residual window, whose line names it
  (D18).
- Rendering. The reason appears where every gate's does: an `excluded`
  entry's `reason`, a `target-excluded` refusal's `reason` and a `refused`
  target's `reason`, so no JSON field is added and the closed enums gain one
  value within `schema_version: 1`, before any release. The human preview
  groups it with its next step (D18).

Checked here on Git 2.36.6 and 2.43.0: the child prints nothing for a worktree
whose HEAD reflog holds only commits a branch reaches, and nothing with no
candidate at all; it prints the commit made on a detached HEAD and left there,
and nothing once that commit is tagged; run in the worktree, it prints the
commit that only `refs/worktree/keep` holds, and run in the main worktree it
does not; that ref stays loose after `git pack-refs --all`; it exits 128 on a
missing object; and for a branch amended and reset in the worktree it prints
the pre-amend commit with only the refs as negatives, and nothing once the
branch reflog's objects are negatives too. On Git 2.43.0, after an interactive
rebase onto a merge target that had moved, with one pick turned into a fixup,
it prints the intermediate commit that the fixup replaced (Risks).

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
- [A worktree whose HEAD reflog names commits of no value that nothing else
  holds, such as the intermediate commits of an interactive rebase that
  rewrote its picks and then squashed or fixed them up, or the commits of a
  branch checked out there and
  since deleted, is excluded as `worktree-only-commits`; so is one whose HEAD
  reflog exceeds 64 KiB] -> Fails closed, as Brett Heap's ruling LQ-13 asks;
  the remedy says to keep any such commit on a branch or tag, or to review and
  remove the worktree by hand (D18, D21).
- [A branch created from a remote branch that already had commits, then merged
  elsewhere, reads as unstarted, because nothing moved it here since its
  creation entry] -> Fails closed as `unstarted-branch`; the remedy says that no
  commit was made on the branch here since it was created (D18).
- [`extensions.worktreeConfig` turned on after the plan, in a repository where
  the plan read it unset, together with a `core.worktree` for a target, is not
  re-read at revalidation, so that target's status probe there reads the other
  tree] -> A concurrent writer's change, outside the contract; Git's own check
  still reads the registered tree, so modified and untracked files there still
  refuse the removal, and only ignored files created there after the plan are
  exposed. Re-reading row 4c for every target would add a child to every
  revalidation (D7, D14; LQ-11).
- [A live session in a started, merged worktree is not protected] -> D3's
  residual; the README asks for sessions to be closed, and no commit can be
  lost.
- [The pins turn off the untracked cache and fsmonitor, so status probes on
  large trees are slower] -> Task 2.1 measured it (42 to 49 ms warm for 10,000
  entries, 215 to 232 ms for 100,000); a slow probe makes a plan incomplete,
  never unsafe.
- [The stat pins override a repository's `core.trustctime=false` or
  `core.checkStat=minimal`, set where ctimes or inodes change without an edit,
  as under some backup tools and network filesystems, so Git compares those
  files' content on every probe] -> Accepted (Brett Heap's ruling LQ-10): the
  probe is slower there, never wrong, and a slow probe makes a plan incomplete,
  never unsafe (D11).
- [A repository whose every worktree carries a gitlink, the V5 deferral's
  motivating repository (Opensoft-Tenant: 20 rows pass every gate before
  `deferred-target-cap` and all 20 are `contains-submodule` after it), yields 0
  removable rows each run, and its deferred count never drains, because
  `contains-submodule` is an index gate tested after the deferral] -> The order
  stays, since the index gates cost a probe per row and the deferral keeps those
  probes to 16 (D12); the human report says why the deferred rows will not drain
  when every one of the 16 rows past the cap is `contains-submodule` (D18); 16
  rows that any index gate excludes ahead of a backlog stall it alike; V5's
  caveat was ratified with the deferral at the merge of PR #11.
- [Rows of 100,000-entry indexes: the fit of BA:729-735 would give 64 rows, 16
  targets and a report cap of 128, since the plan term alone for 128 such rows
  is 46.6 s] -> The caps measured at 10,000 entries stand; a plan over such rows
  goes incomplete with `deadline-exceeded`, never unsafe (BA:772-774) (task
  2.1, R-24).
- [CPU saturation: at load 165 on 32 threads wall times rise about eight times,
  a 128-row plan takes 77 s, where the rule would give no cap at 16 targets, 16
  rows and 8 targets once lowered, and a report cap of 64, and a 20,000-file
  removal took up to 14.1 s, past the 5 s floor] -> The caps stand; the plan
  goes incomplete with `deadline-exceeded`, never unsafe, and a removal started
  within the floor is waited for (D9, V1). Whether to design for a saturated
  workstation is Brett Heap's call (task 2.1, R-24).
- [A remote-helper protocol of another name, with its own `allow=always` in the
  repository's configuration, is not among the pins, and `GIT_ALLOW_PROTOCOL`
  is scrubbed rather than pinned] -> Accepted as rare: such a helper could still
  fetch for a probe in a partial clone, the probe would then succeed rather than
  fail, and no unsafe removal follows (D11, R-25).
- [The push child carries no protocol pin and follows the configuration as `git
  push` would: an `ext::` origin that `protocol.ext.allow=always` allows, a
  `pushurl`, `url.<base>.pushInsteadOf`, `remote.<name>.receivepack`,
  `core.sshCommand` or remote helper that sends it elsewhere or runs a command,
  a pre-push hook and a credential helper included, while the confirmation
  names only the remote; and the scrub removes a caller's
  `GIT_CONFIG_PARAMETERS` and `GIT_CONFIG_COUNT`, so a `-c` given through the
  environment does not reach it] -> Accepted: the push is the person's
  explicit act on the remote they configured, as the baseline push is, and a
  `GIT_ALLOW_PROTOCOL` list the caller set still binds it; the scrub makes it
  act on the repository and configuration the run inspected; every inspection
  child stays pinned, so no evidence comes from such a configuration (D11, the
  push-child exception).
- [No Git child of `project`, the push child included, writes a trace: a
  caller's `GIT_TRACE` variables are scrubbed and the three trace2 targets are
  off, so a person cannot trace a Git child through `project`] -> Accepted
  (Brett Heap's ruling Q9 B): trace output is a side effect that writes files,
  never evidence, and a person who needs a trace runs the Git command by hand
  (D6, D11).
- [A caller whose `HOME`, `XDG_CONFIG_HOME`, `GIT_CONFIG_GLOBAL` or
  `GIT_CONFIG_SYSTEM` is set to a relative path cannot run `clean`, and
  `status`, `doctor` and `update` inspect no repository for it, even where the
  path names nothing a repository holds] -> Accepted (Brett Heap's ruling
  LQ-15): it fails closed, the message names each such variable and the remedy,
  an absolute path, and the alternative, anchoring the value elsewhere, would
  rewrite the caller's environment; deliberate over-refusal, as C-44's is (D11,
  D18).
- [Squash-merged branches never prove ancestry, so squash-merging
  repositories select little] -> Before Brett Heap (Open Questions).
- [A merged worktree whose upstream was deleted is removed on local ancestry
  alone, with no remote evidence] -> Brett Heap's ruling on open question 1:
  the branch is kept, so its commits stay reachable from it and from the merge
  target, and every other gate still applies (D6).
- [The caps and the Git floor were unverified until tasks 2.1 and 2.2] -> Both
  ran before the handoff: the caps stand as measured (D5, the degraded cases
  above) and the floor stays 2.36 with the scrub extended (D17, R-21).
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

Users meet five behaviour changes first: plain `project clean` exits 1 when its
report is incomplete; `clean` refuses below Git 2.36; `--worktree P` refuses a
freshly created merged worktree whose branch has no commit of its own, with the
remedy "no commit was made on this branch here since it was created; review,
then git worktree remove yourself"; a merged worktree whose branch reflog keeps
no decisive entry (no activity for `gc.reflogExpire`, 90 days by default, D10)
is refused as `reflog-unavailable` in single mode as well as withheld from the
batch, with the remedy "the branch's reflog is missing, expired or undecidable;
review, then git worktree remove yourself"; and `--worktree P` removes a merged
worktree whose upstream was deleted, as `merged-removable` when its gates pass,
its branch kept, where `a040790` refuses it as `unpublished` (D6, Brett Heap's
ruling on open question 1). The README's clean section states them first.

1. Ratification by Brett Heap's word on PR #11 (`tasks.md` 1.6), which
   ratified the V5 deferral and left the squash-merge question before him; the
   push-child exception waits for his word on the pull request that amends
   this change (`tasks.md` 1.7).
2. Governance tasks 2.1 (measurement) and 2.2 (the Git floor) ran before the
   handoff, and neither forced a change to a cap or the floor: the caps stand as
   measured, and the floor stays 2.36 with a scrub of one more name (R-21).
3. Local `main` is synced to `origin/main`, then `/speckit.specify` creates
   feature `004-project-clean-all-safe` on branch `004-project-clean-all-safe`,
   recorded once in `tasks.md` under "Speckit Handoff"; `/opsx:apply` runs only
   then.
4. Feature 004 implements D1 to D19 and the CI floor job (D17), merging `main`
   into its branch as `main` moves and never rebasing.
5. README: "Clean up Git worktrees" opens with the five behaviour changes, then
   the preview and apply, `--expect-plan`, the gates, the deferral, the narrow
   guarantee and residual window, the result record and recovery, and the
   advice to close sessions first (D3); "Apply
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
   headers after this lands, then is ratified and implemented as feature 005.
8. The change is archived after the realization PR merges.

Rollback: revert the realization commit on `main`. Installed `project` artifacts
follow workBenches' pin, so a revert before the pin moves reaches nobody
downstream.

## Open Questions

Each is before Brett Heap with a recommendation; the deltas implement the
reading stated, and a different ruling edits the deltas before the archive.

- Squash-merged branches never put their tip into the target's ancestry
  (BA:195-199). Recommendation: a local patch-equivalence proof (`git cherry` or
  patch IDs against the target) as a follow-on change, not in the MVP.
- The push-child exception: the pins on every Git child (D11, R-23, R-25) refuse
  a push over every protocol (a local-path `origin` fails with `fatal: transport
  'file' not allowed`, exit 128), yet the change keeps the explicit push of
  `clean --action push`, whose child must reach its remote. Recommendation:
  amend the change in place before its archive, as this draft does, so that the
  push child is the one Git child without the pins. The alternative is a
  follow-up change after the archive, as `fix-parent-obstacle-wording` followed
  `prefer-triad-in-project-new`, which costs a second archive and leaves the
  archived spec wrong in between.

Ruled on 2026-10-09: a merged worktree whose remote branch was deleted is
`merged-removable`, Brett Heap having ruled that a local ancestry proof
outranks `remote-gone` for worktree rows (D6; `proposal.md` Decisions). The V5
deferral (D12) and the other departures were ratified with the merge of PR #11
(Brett Heap: "ratify, merge #11 and run the runbook").
