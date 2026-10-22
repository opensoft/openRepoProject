Lane: openRepoProject-2

# Design

## Context

See `proposal.md` for why and what, and the deltas under `specs/` for the
requirements. The council's noted constraints, `clarifications.md` N1 to N5, are
answered by D1 to D5; D6 to D19, and D21 and D22 for Brett Heap's rulings LQ-13
and LQ-14, give the how of the proposal's decisions, and D20 maps the packet's
35 validation scenarios to the deltas. The binding rulings
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
Context, D7, D12, D14, D18, D20, D21 and Risks; lane openRepoProject-3's W8
read of LQ-15, Context, D11, D16 and D18; LQ-14, Context, D7, D18, D20, D21,
D22 and Risks; and lane openRepoProject-3's W10 read of LQ-12 and LQ-13, under
the lead's rulings R-124 and R-127, Context, D6, D12, D14, D21, D22 and Risks;
and its W9 read of LQ-10 and LQ-11, under the lead's R-125, Context, D6, D7,
D11, D17, D18 and Risks; its W14 read of LQ-14, under the lead's R-126,
Context, D18 and D22; and its W21 read of R-124 to R-126 with the round of the
lead's R-146 and R-147, Context, D7, D12, D18, D21, D22 and Risks; and its
W26 read of that round, with the lead's R-171, Context, D7, D18 and D22; and
the restated fit of the lead's R-178, Context, D14, Risks and Open Questions;
and lane openRepoProject-3's W31 read of that round and of the fit, with the
lead's R-187 and R-190 and lane openRepoProject-5's A10 read, Context, D7, D14,
D21, D22, Risks and Open Questions; and its W36 read of round (c), with its W32
read of LQ-14 in feature 004 and the lead's R-200, R-207 and R-208, Context, D7,
D14, D21, D22, Risks and Open Questions; and its W38 read of round (d), with the
lead's R-213 and R-216, Context, D7 and Open Questions; and Brett Heap's ruling
of 2026-10-22 on LQ-20, choosing its step (i), with that step's measurement, and
lane openRepoProject-3's W42 read of round (e), under the lead's R-236, Context,
D7, D14, D22, Risks and Open Questions; and its W52 read of next steps that Git
refuses, under the lead's R-248, Context, D4, D18, Risks and the Migration Plan,
its F-1, the ceiling's recovery text, and, by W59's G-1, its F-2, a locked row's
recovery text, left for Brett Heap, who ruled both on 2026-10-22 (round (h));
and the shortening of F-7's clause, under the lead's R-252, Context, D18 and the
Migration Plan; and lane openRepoProject-3's W59 read of rounds (f) and (g),
under the lead's R-253, Context, D4, D7, D14, D18, Risks and Open Questions; and
round (h), under the lead's R-258, R-259, R-260 and R-263, with writer E's
report, lane openRepoProject-5's RI-3 and O-1, lane openRepoProject-3's W64 read
of rounds (g2) and (g3), and Brett Heap's ruling of 2026-10-22 on F-2, F-1 and
O-1, Context, D4, D7, D9, D10, D14, D18, Risks and Open Questions; and round
(i), round (h)'s open point, the message of a redirected main worktree's
refusal, under the lead's R-271, with lane openRepoProject-4's finding on the
identity probe and lane openRepoProject-3's W73 M-1 under the lead's R-284,
Context, D6, D9 and D18; and round (j), lane openRepoProject-3's W70 read of
round (h), under the lead's R-285, R-287 and R-291, with Brett Heap's
confirmation of R-284 on 2026-10-22, "R-284: yes" (the lead's R-290), Context,
D7, D9, D18 and Open Questions; and round (k), lane openRepoProject-3's W80 read
of round (i), with its W81 read of feature 004 at `2707ff2`, under the lead's
R-294, Context, D4, D6, D18 and Open Questions; and round (l), lane
openRepoProject-3's W87 read of rounds (j) and (k), under the lead's R-307 and
R-310, Context, D4, D7, D18 and Open Questions; and round (m), Brett Heap's
confirmation of round (l)'s five texts on 2026-10-22, "R-307: yes; R-310: yes"
(the lead's R-319), and his "R-320: yes" (the lead's R-321) on the stale
recommendations and the cap remedy, with F-1's (b) beside an unread row recorded
as open, Context, D18 and Open Questions; and round (n), lane
openRepoProject-3's W91 and W95 reads of rounds (l) and (m) and its W100 LOW-A,
under the lead's R-341 and R-336, with Brett Heap's "R-324: yes" (the lead's
R-343), Context, D7, D8, D9, D18 and Open Questions. Brett Heap's ruling of
2026-10-09 on open question 1, that a local ancestry proof outranks
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
recovery text, which for a locked worktree says to unlock it first (D18; lane
openRepoProject-3's W52 F-2, R-248). For a locked row that text replaces the
ratified recovery text of `0050f3e`, which the delta keeps for every other row,
by Brett Heap's ruling of 2026-10-22, "F-2: yes" (lane openRepoProject-3's W59
G-1, R-253; R-263). A report row's `.git` file and registry entry are present,
so its note keeps `git worktree remove --force`; the ceiling's recovery text for
a target whose `.git` file or entry is gone is D9's, and so is its third text,
which a target whose `.git` file the rescan cannot read shows whether or not it
is locked, a ceiling target showing the first, second or third of D9's texts and
never the locked one, which is a report row's own (D18; lane openRepoProject-3's
W80 M-1 and W87 LOW-3).

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
| 3b | `rev-parse --path-format=absolute --git-dir --git-common-dir --is-bare-repository` | only on a `target-not-repository-root` refusal, at the directory row 3 ran in, where row 3 failed and that directory holds its own `.git` (D18) |
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
a plain checkout. Three lines mean a submodule checkout, whose third line is the
superproject's toplevel, or a line feed in a path, and more than three a line
feed: a plain checkout prints three lines where only one of its two values holds
one line feed, as where a separate git directory holding one serves a toplevel
that holds none, and four where its toplevel holds one and its common directory
lies under that toplevel, carrying the same line feed, on Git 2.43.0 and 2.36.6
(lane openRepoProject-3's W80 L-3). The count cannot tell the two apart, so on
any count but two the probe is repeated as one child per option, each child's
output one value, counted, rather than guessed at, and that tells them apart
(lane openRepoProject-4's finding; feature 004's `identity_probe()` at
`7164d7f`, `project:2663-2689`). F is therefore at most 8, BA:615-616's 7 and
row 4c, plus row 4b in the gitfile layout and the rare repeat. Row 3b runs only
when the resolution refuses, before any plan, so no plan counts it.

Per row: the identity reads (`lstat` without following, the `.git` file, the
admin `gitdir` and `commondir` files), each a filesystem call on a daemon
`threading.Thread` waited for with `min(5 s, work remaining)` and abandoned
after it (C4; never a `concurrent.futures` pool, whose shutdown would wait for a
stuck call); then, in a linked row of a repository whose row 4c read true, the
effective-work-tree probe of D7; then the combined status probe in that worktree
(D11). Rows 3 to 7 are memoized by common directory within an invocation, which
matters to `status` and `doctor`, whose legs are other repositories. Where
`root` is null (a bare repository, a missing main worktree, or a gitfile
checkout whose main worktree cannot be named), rows 4 to 7 run in the common
directory for a bare repository and otherwise where row 3 ran, as the evidence
model states; `clean` refuses those layouts (D8), so only a reader that reports
them, such as `add-project-overview`, probes there.

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
Brett Heap's ruling Q9 B binds Git children and the tool is not one. The
scenario "Owner tools see the repository the check inspected" sets three of
the thirty names, `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE`, as a
sample, which is enough (lane openRepoProject-3's W10 L8, R-124 (d)).

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
`builtin/worktree.c:978-995` at 2.36.6 and `:1256-1273` at 2.43.7) and is not
misled. The Git source lines of D7, D11, D21 and D22 are cited from the release
tarballs of Git 2.36.6 and 2.43.7, tags `v2.36.6` and `v2.43.7`, each
tarball's sha256 matching kernel.org's `sha256sums.asc`, and were read there
(lane openRepoProject-3's W21, which could not check them, R-146). Row 4c reads
the extension once per common directory, from the common `config` alone and
without includes, as Git's own format check reads it; an unset value is false
and any other failure counts as true. Where it is true, each linked row whose
registration agrees gets one more worktree probe, `git rev-parse
--path-format=absolute --show-toplevel`, after its identity reads and before its
status probe. That probe asks for one value, and by the lead's R-287, with
R-291's refinement, which the evidence model words so, "the probe's standard
output, less the one line feed Git ends it with, SHALL be read as one path,
which may itself hold line feeds; output that is empty, that names no path, or
that does not end in a line feed SHALL make the row's registration disagree"
(output that is only a line feed names no path); a toplevel whose realpath
differs from the registered path's and a failed probe (as under
`core.bare=true`, `fatal: this operation must be run in a work tree`) make it
disagree too, so the row is `registration-mismatch`, `inspection-error` and
unprobed. A linked worktree whose own path holds a line feed is therefore read
as its own path, as the ratified scenario "Control-character and non-UTF-8
paths" requires, where reading the output as one line made it
`registration-mismatch` wherever the extension is true, with a remedy that names
an unset where nothing is set (lane openRepoProject-3's W70 M-2, reproduced on
Git 2.43.0 and 2.36.6); unlike row 3, which asks for three values (D6), this
probe needs no second child for it. Asking Git covers every way the extension
can redirect a row, without parsing configuration in `project`, and the probe
runs only in such repositories. Checked here on Git 2.36.6 and 2.43.0: the
extension read exits 1 when unset and prints `true` when set; the probe prints
the decoy for a `core.worktree` in `config.worktree` and for one in the common
`config`, and fails with 128 under `core.bare=true`. Row 4b reads
`core.worktree` the same way: an exit 1 with nothing printed is the key unset,
and any other failure, an exit 1 that printed anything included, makes the main
worktree unreadable, so the run is refused `target-not-repository-root` (lane
openRepoProject-3's W100 LOW-A; the lead's R-336).

The two-way registration also reads the administrative directory's `commondir`
file, from which Git takes a linked worktree's common directory
(`get_common_dir_noenv`, `setup.c:301-325` at 2.36.6 and `:316-340` at 2.43.7:
the file's trailing line feeds and carriage returns removed, a relative value
resolved against that directory, then its realpath; with no such file the
administrative directory is its own common directory), and requires it to name
`<common_dir>`, by a filesystem read with no Git child; otherwise the
registration disagrees, and a read that fails makes the row
`inspection-error`. Row 4c then reads the `config` that Git reads. Lane
openRepoProject-3's W9 M2 planted a `commondir` naming a shared clone X whose
own `config` set the extension, beside a `config.worktree` decoy: row 4c,
reading the registered repository's `config`, read the extension unset, no
probe ran, and the removal deleted the ignored `local.env` (the lead's R-125).
Checked here on Git 2.36.6 and 2.43.0: `git worktree add` writes `../..`,
which resolves to `<common_dir>`; the planted value moves Git's common
directory in the worktree to X and its toplevel to the decoy; and the
non-force removal exits 0 and deletes the ignored file.

Revalidation is BA:677-707's targeted check, in its order, stopping at the first
difference: the identity probe; the manifest re-read (a file read, 1 MiB cap);
the registry listing; a narrowed ref listing whose patterns name the merge
target, the manifest's candidate, the branch the plan's `origin/HEAD` named,
`main`, `master`, `refs/remotes/origin/HEAD`, and the selected branches and
their upstreams; the target's identity, `modules` check and D22's listing of its
administrative directory, by filesystem reads, and, where the plan's row 4c read
true, its effective-work-tree probe, its output read as at planning: output read
as one path that is not the target's, even over several lines, is a decided
difference, `identity-changed`, while a probe that fails, runs past its own
budget or prints output that is empty, names no path or does not end in a line
feed is `state-changed`, a value that cannot be re-read, and one that the
deadline cuts leaves the target `not-attempted` with `deadline-exceeded`, as for
every revalidation child (the lead's R-171, R-287 and R-291; at planning such a
probe makes the row's registration disagree instead, as above, by the lead's
R-187 erratum); then, inside the target worktree, the combined
status probe, which must print nothing, the hidden-state probe, and D21's
`logs/HEAD` re-read and reachability probe, which must print nothing. Every
filesystem read of these steps follows the rule of a Git child (the lead's
R-208): one that fails, or runs past its own budget while the deadline is not
the limit, is `state-changed` whatever its step, so that a failed read of the
repository's or the target's identity or registration is `state-changed`, not
`identity-changed`; one that finds its path missing (`ENOENT` or `ENOTDIR`)
decides that the path is absent, a value that keeps its step's reason, and an
administrative directory that D22's `operation-in-progress` listing finds absent
is a registration difference, `identity-changed` (lane openRepoProject-3's W38
L-4 and W42 L-2); and one that the deadline cuts leaves the target
`not-attempted` with `deadline-exceeded`. R-208 is a reading of BA:271-276, by
which "a value that cannot be re-read, including a filesystem call that times
out, counts as a mismatch": a read that fails decides no identity difference, so
its mismatch is the packet's "any other" difference, `state-changed`; this
reading went to Brett Heap to confirm, as O-2, on 2026-10-22. Row 4c itself is
not re-read, which keeps revalidation at six Git children in a repository
without the extension (nine where the path of its root or common directory holds
a line feed, D14): an extension turned on after the plan, with a
`core.worktree` for a target, is a concurrent writer's change outside the
contract (Risks). Ancestry needs no child: it is a function of the branch head
and the merge-target SHA, both compared. The reflog of D10 is not re-read: a
moved branch is already `branch-changed`. The HEAD reflog of D21 is re-read, as
D21 states. A selected row whose upstream was deleted (D6) records
`upstream_oid`, `ahead` and `behind` null, and revalidation compares them as
recorded, by the review-safety rule that a value null in the plan and null at
revalidation is no difference while a value that cannot be re-read is one: the
narrowed listing still showing no remote-tracking ref for it is no difference,
and one that reappears is `state-changed`.

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
   4b, whose failure rule D7 gives); where that is unset, as `git init
   --separate-git-dir` leaves it, it is the candidate toplevel whose `.git`
   file's `gitdir:` line names the common directory; where neither names it, as
   from a linked worktree of such a repository, the argument is refused. The
   common directory is never probed as a row.
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
its reason is `removal-ceiling` either way, and the run exits 1 (D19). The
note's recovery text names `git worktree remove --force` only where the rescan
finds both the target's `.git` file and its registry entry present, and
otherwise `git worktree prune` and a deletion of the path by hand, because Git
deletes the work tree first and the administrative directory after, so that a
removal cut short can leave the path and the entry without the `.git` file, or
the path alone, and Git refuses the forced removal of either (D18; W52 F-1;
Brett Heap's ruling of 2026-10-22, "F-1: prune-then-delete", R-263). The rescan
reads the `.git` file by one `lstat`, a filesystem call under the reserve's
budget, so it still spawns at most three Git children. Where that `lstat` fails
other than for the file's absence, or is cut at its budget, the recovery text
names neither and warns against `git worktree prune`, `git worktree remove` and
`git gc` until the `.git` file can be read (Brett Heap's "R-324: yes", the
lead's R-343): where Git cannot stat a worktree's `.git`, as under `EACCES` on
its path, `git worktree prune` deletes that live worktree's administrative
directory, its index, `HEAD`, per-worktree refs and reflog with it, on Git
2.43.0 and 2.36.6 (lane openRepoProject-3's W73 M-1; the lead's R-284, which
refines how Brett Heap's F-1 ruling applies to a read that fails and which he
confirmed on 2026-10-22, "R-284: yes" (R-290); round (i) reproduced it on both
builds). 300 s is about two hundred times fixture `k`'s 1.27 s, ample even for
drvfs at ten times slower; task 2.1 measured it, the 20,000-file removal taking
0.66 s warm and 0.72 s cold at low load and 14.1 s at worst under saturation, 21
times under the ceiling.

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
   `os-error`, like any failed row probe; a read not finished inside the
   filesystem budget, the deadline not being the limit, leaves the row unprobed
   and the plan incomplete with `inspection-incomplete`; and a read that the
   deadline cuts records `deadline-exceeded` and leaves the row unprobed and the
   plan incomplete with `deadline-exceeded`, whose remedy names no repair, as
   for every other filesystem read and as D21's `logs/HEAD` read has it (lane
   openRepoProject-5's O-1; Brett Heap's ruling of 2026-10-22, "O-1:
   deadline-exceeded", R-263, which amends `0050f3e` pcl:606-608).
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
and sub-second checks (where Git is built with `USE_NSEC`). Under either
repository setting an edit that keeps a file's size and restores its mtime
matches the index entry, so the status probe and Git's own check both read the
worktree clean and the removal deletes the edit (lane openRepoProject-3's F1 H-3
at `2cf34d3`). Checked here on Git 2.36.6 and 2.43.0: with
`core.trustctime=false` and `core.checkStat=minimal` in the repository's
configuration, such an edit gives no record under the two older pins and ` M`
under all four. The pins follow `core.fsmonitor=false` on every status probe,
the hidden-state probe and the removal, and like them outrank every
configuration file; the removal's pins reach Git's own check, which runs in a
child of the removal. A ctime or inode that changes without an edit makes Git
compare the content instead, which is slower and never a wrong answer (Risks).

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
  planted attributes file can select a filter for a tracked file. This risk is
  not a relative path's alone: a tracked `.gitignore`, or the repository's own
  `info/exclude`, already turns an untracked file into an ignored one with an
  absolute `HOME` (lane openRepoProject-3's W8 read, on both releases), so the
  code-execution risk is the one that motivates the test.

The test therefore runs first in every subcommand that inspects a Git
repository, before `git --version`: `HOME` or `XDG_CONFIG_HOME` set to a
non-empty value whose first byte is not `/` makes the subcommand start no Git
child (`relative-config-path`). `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`,
Git's own variables naming a configuration file and the analogue of C-44's
`GH_CONFIG_DIR`, are tested the same way; they are the lead's extension of the
ruling, which Brett Heap may strike, and RA's reproduction with
`GIT_CONFIG_GLOBAL` is why that one is in the list. Striking them touches these
sites, which name the two variables for the extension and for nothing else:

- `specs/project-command/spec.md`: the sentence of the evidence model's
  "Configuration paths" paragraph that applies the test to them, which also
  carries the paragraph's only mention of the system's configuration, so that
  nothing else in the paragraph depends on it; and the AND naming them in the
  scenario "A relative configuration path in status, doctor and update";
- `specs/project-clean/spec.md`: the AND naming them in the scenario "A
  relative configuration path", and the words "and `GIT_CONFIG_GLOBAL` and
  `GIT_CONFIG_SYSTEM` unset" in its last AND;
- this section: the clause on the files that they name in the list of files
  Git reads above, with the words "or the system's" that follow from it; the
  two sentences before this list, the list itself, and the clause on an empty
  `GIT_CONFIG_GLOBAL` or `GIT_CONFIG_SYSTEM` in the empty-value sentence
  below; D18's variable order; and the list of variables in the Risks entry
  for LQ-15;
- `proposal.md`: What Changes (evidence model), Impact (README Install), the
  LQ-15 departures entry and its line in the later-rulings list.

The other mentions of the two variables stay: the pins and the trace2
variables that override the files they name, RA's and lane
openRepoProject-4's evidence, and the precedence example below with its AND in
"A relative configuration path", where an absolute `GIT_CONFIG_GLOBAL` is a
condition, not a value the test refuses. The test is made on the raw
bytes: ` /x`, `~/x` and `.` fail it, as does a first byte that is not UTF-8,
and `/` alone passes. An empty or unset variable passes, because it names no
relative file: Git treats an empty `XDG_CONFIG_HOME` as unset, an empty `HOME`
gives `/.gitconfig` and `/.config/git/`, and an empty `GIT_CONFIG_GLOBAL` or
`GIT_CONFIG_SYSTEM` names no file Git can open. As in C-44, the test does not
follow Git's order of precedence: it applies to each variable whether or not
Git would read a file through it, so a relative `HOME` beside an absolute
`XDG_CONFIG_HOME` and an absolute `GIT_CONFIG_GLOBAL` fails it too, though Git
would then read no configuration file under `HOME`; that over-refusal is
deliberate, fail-safe and independent of Git keeping its order. `clean` then
refuses with `relative-config-path`, exit 2, in every mode, after its argument
checks, which start no Git child and so refuse `invalid-arguments` first, and
before its version check; `status`, `doctor` and `update` report it as they
report a Git below the floor (D16). The values are read only for this test,
are passed to every child unchanged when it passes, and are never printed: the
message names each variable that fails the test (D18). The test covers these
variables only; other relative paths in the environment that a Git child
resolves against its directory are outside it.

### D12. The 16-per-run deferral (V5)

Gates are evaluated in canonical order. Rows that pass every gate before
`deferred-target-cap` are counted; the first 16 go on to the gates after it,
the `modules` check, the hidden-state probe and the gates of D22 and D21, and
the rest are excluded as `deferred-target-cap` with no index probe, so at most
16 hidden-state probes run and E is at most 16; at most 16 of D21's
reachability probes run likewise. A row that a gate after the cap then
excludes keeps its place, so a run can select fewer than 16 while rows stay
deferred, and 16 rows that such a gate always excludes, ahead of a backlog,
stop it until a person handles them; when every one of the 16 is excluded by
a gate after the cap, the human text says why the deferred rows will not
drain, naming those reasons (D18, R-24; lane openRepoProject-3's W21 L-f). The
plan stays complete and apply allowed; each re-run plans and revalidates afresh,
draining 16 at a time. `plan_digest` covers only `selected`, so a deferred row's
change leaves a preview valid, and the report mode defers alike. The
`target-cap` refusal (BA:96-101, BA:1004, BA:1367-1371) is retired, a departure
ratified with the merge of PR #11; the code survives only as the overview's
limiting gate.

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

The cap test is D5's: BA:729-735 reapplied at task 2.1's measured warm medians
with the 1.5 margin, a failing cap lowered by the rule's steps (BA:766-771).
Task 2.1 ran it before LQ-11 and LQ-13 added children that it did not measure,
so this section gives the fit on three bases (LQ-20); LQ-20's step (i), which
Brett Heap chose on 2026-10-22, has since measured those children, and the case
passes on the measured basis, D5's as ratified. At BA's flat 150 ms per Git
child, with F = 8 (row 4c of LQ-11 included), the Time column giving a run to
its end, or to the point where it stops, every child and removal counted:

| Mode | Children | Time | Fits the 50 s work deadline |
| --- | --- | --- | --- |
| report, 256 rows | 8 + 256 + 16 + 16 = 296 | 44.4 s | yes |
| report, 512 rows | 8 + 512 + 16 + 16 = 552 | 82.8 s to plan, so the run stops at the 50 s work deadline | no |
| all-safe, 128 rows, 16 targets, row 4c false | 8 + 128 + 16 + 16 + 96 + 3 = 267, and 16 removals | 40.05 s + about 4.8 s = 44.85 s | yes; the 16th removal spawns at 44.1 s with 5.9 s left (BA:753-756) |
| all-safe, 128 rows, 16 targets, row 4c true | 8 + 128 + 127 + 16 + 16 = 295 before the first revalidation, then 7 | 44.25 s, and 45.3 s at the first spawn | no removal: less than the 5 s floor remains, so every target is `not-attempted` with `deadline-exceeded`, exit 1 |
| report, 256 rows, row 4c true | 8 + 256 + 255 + 16 + 16 = 551 | 82.65 s to plan, so the run stops at the 50 s work deadline | no; incomplete with `deadline-exceeded` above 147 rows |
| single, 128 rows plus P, row 4c false | 8 + 129 + 1 + 1 + 6 + 3 = 148, and 1 removal | 22.2 s + about 0.3 s = 22.5 s | yes |
| single, 128 rows plus P, row 4c true | 8 + 129 + 128 + 1 + 1 + 7 + 3 = 277, and 1 removal | 41.55 s + about 0.3 s = 41.85 s | yes; the removal spawns at 41.1 s |

The report builds no apply plan, so its worst case is the planning term alone,
and 256 is the largest power of two that fits (D-V, OQ-29). Row 4b and the rare
row 3 repeat add 0.15 s each; the reflog reads add no child.

The planning term counts what a plan runs: F; one status probe per present
row; where row 4c reads true, one effective-work-tree probe per linked row
(LQ-11); and, past the cap, at most 16 hidden-state probes and 16 reachability
probes (LQ-13). Writer G measured these counts with a logging Git wrapper at
`f0fdbc2`, before LQ-13 was built (the lead's R-178): one status child per
present row, one `rev-parse --show-toplevel` per linked row where row 4c reads
true, one `ls-files` per row past the cap, and five children per
revalidation, six where row 4c reads true, to which LQ-13's reachability probe
adds one, giving the six and seven of D7. On this basis removal k spawns at (P +
V k) x 0.15 s + (k - 1) x 0.3 s, P the planning children and V the children per
revalidation, and only while that is at most 45 s, the spawn limit, which is the
50 s work deadline less the 5 s removal floor. With P = 168 and V = 6, row 4c
false, the 16th removal spawns at 44.1 s, as the table says. Seven children per
target come only where row 4c reads true, and there the per-row probes make P =
39 + 2R for R rows (8 + R + (R - 1) + 32): all 16 removals fit up to 59 rows, 15
at 64 rows, 14 at 65 and 7 at 100, the first fits up to 127 rows (at 45.0 s),
and at 128 rows it would spawn at 45.3 s, so nothing is removed, every target is
`not-attempted` with `deadline-exceeded` and the run exits 1, which is safe,
since no removal starts; a plain report there goes incomplete with
`deadline-exceeded` above 147 rows. The 14 removals that R-178 gave for seven
children per target held P at 168, a hypothetical, since P = 168 means R of
about 64.5 there; at that P the 14th would spawn at 43.8 s and the 15th at
45.15 s (lane openRepoProject-3's W31 L-4). Before this restatement D14 counted
P as 168 in every repository, which left the per-row probe out (lane
openRepoProject-5's A9, R-178). Writer G's run also found the build's
`probes.estimated` short where row 4c reads true, 37 children performed against
34 estimated, which is the build's to correct. Where the path of the
repository's root or of its common directory holds a line feed, row 3 is read
one option per child (D6), four children in place of one, wherever it runs, so a
revalidation spawns nine children, ten where row 4c reads true, and the final
rescan six: writer E measured nine, ten and six on Git 2.43.0 and 2.36.6 for a
root holding one, and round (h) the same for a separate git directory holding
one under a plain root (lane openRepoProject-5's RI-3, R-259). The delta states
that exception beside the six, seven and three, and has `probes.estimated` count
the extra children, three per target and three for the final rescan, which
feature 004 at `d764c26` leaves out. On the measured basis below, the 51 extra
children before a 16th spawn cost about 1.0 s at the identity probe's 19.7 ms,
so the case still fits.

On the measured basis, D5's, each child costs task 2.1's warm median times 1.5,
the larger median of its runs 2 and 3, as its record posted on PR #11 gives them
(version 5.9 ms, identity probe 19.7 ms, registry listing 33.8 ms, full ref
listing over 1,000 loose branches 359.7 ms, narrowed listing 101.6 ms, merged
set 72.6 ms, status probe 74.1 ms and `ls-files` 26.1 ms, at 10,000 files), and
a removal 0.604 s, the 10,000-file removal, which task 2.1's verdict took and
the cap test here takes as well, with the 20,000-file removal, 1.118 s, as its
sensitivity case (lane openRepoProject-3's W36 L-b and L-c). Task 2.1 measured
neither kind of child added since; LQ-20's step (i), which Brett Heap chose on
2026-10-22 (the lead's R-236), measured both on its protocol, in the same
`py-bench` container with Git 2.43.0 and Python 3.12.3, at a 1-minute load of 15
to 21 on 32 threads, the larger median of two runs of 40 to 48 each: LQ-11's
per-row `rev-parse --path-format=absolute --show-toplevel`, 5.8 ms warm and 9.8
ms cold, so 8.7 ms with the margin, and LQ-13's `rev-list`, 106.9 ms warm and
686 ms cold, so 160.3 ms, its walk covering the whole history of a repository of
10,001 files, 1,000 branches with their upstreams, 1,991 loose refs and 9,940
commits with no commit-graph; neither child reads the index, so the 10,000-file
fixture is the one. Row 4c's read keeps the identity probe's 19.7 ms. On those
costs, where row 4c reads true, all 16 removals fit at 128 rows, the first
spawning at 14.55 s and the 16th at 30.0 s with 20.0 s left, and with
20,000-file removals all 16 as well, the 16th at 37.7 s with 12.3 s left; the
case passes on the measured basis, as D5 ratified it, and needs none of LQ-20's
options there. It would stop passing only if the work-tree probe cost about 114
ms with the margin, a warm median of about 76 ms, or the `rev-list` about 630
ms, about 420 ms warm, each with the other at its measured cost (about 60 ms and
389 ms with 20,000-file removals). On the mixed basis as first stated, task
2.1's measured costs stand for the children it measured, its 16th removal
spawning at 23.6 s, and each child added since costs 150 ms: 33 before the 16th
spawn where row 4c reads false (row 4c's read, 16 reachability probes at plan
time and one per revalidation) and 176 where it reads true (also 127 per-row
probes and a second child per revalidation). When the mixed basis is restated
after step (i), with the two kinds that step (i) measured at their measured
costs, only row 4c's read keeps 150 ms, and all 16 fit where row 4c reads true,
the 16th at 30.1 s (37.8 s with 20,000-file removals). The table's mixed column,
and the options' after it, keep the mixed basis as first stated. Every figure in
the 150 ms and mixed columns is arithmetic on task 2.1's numbers and D14's
counts, with no timing run for them (the lead's R-190, on lane
openRepoProject-3's W31 M-2 and lane openRepoProject-5's A10 read), and every
figure in the measured column is arithmetic on those and step (i)'s two measured
costs (the lead's R-236):

| Case | 150 ms basis | Measured basis | Mixed basis |
| --- | --- | --- | --- |
| all-safe, 128 rows, 16 targets, row 4c false | 16 removals; the 16th spawns at 44.1 s | 16; the 16th at 28.7 s, 21.3 s left (36.4 s with 20,000-file removals) | 16; the 16th at 28.5 s |
| all-safe, 128 rows, 16 targets, row 4c true | none; the first would spawn at 45.3 s | 16; the 16th at 30.0 s, 20.0 s left; with 20,000-file removals 16, the 16th at 37.7 s | 11; the 12th would spawn at 45.3 s, the 16th at 50.0 s |
| report, 256 rows, row 4c true | 82.65 s; incomplete above 147 rows | 24.7 s | 60.7 s; incomplete above 208 rows |
| single, 128 rows plus P, row 4c true | 41.85 s | 12.6 s | 30.9 s |

Each option of LQ-20 had this result on each basis as costed before step (i),
its measured column at the stand-ins that step (i) replaced, the work-tree probe
at the identity probe's 19.7 ms and the `rev-list` at the full ref listing's
359.7 ms, for a 128-row, 16-target `--all-safe --apply` where row 4c reads true,
the 45 s spawn limit and the 5 s removal floor kept except where (c) moves the
limit. None was taken, since the case passes on the measured basis; the table
stays as the record of what was costed (Open Questions):

| Option | 150 ms basis | Measured basis | Mixed basis |
| --- | --- | --- | --- |
| (a) accept the worst case | 0 removals on every run, since a re-run builds the same plan; from 127 rows 1 a run at first (1, 1, 1, 1, 1, 2, 2, 3, 3, ...); a `--worktree` removal fits, at 41.85 s | 16 a run | 11, then 13, then 16 a run |
| (b) bound the plan-time work-tree probe to the selected targets | 13: the 13th spawns at 44.85 s and the 14th would at 46.2 s; a 256-row report completes at 46.8 s | 16; the 16th at 35.7 s | 16; the 16th at 33.3 s |
| (c) a longer work deadline where row 4c reads true | at least 70.55 s, the 16th spawning at 65.55 s; the 60 s invocation deadline becomes 80.55 s and the 64 s run bound 84.55 s; a 256-row report would need 82.65 s | none needed | at least 55.0 s, the 16th spawning at 49.98 s; an invocation deadline of 65.0 s and a run bound of 69.0 s; a 256-row report would need 60.7 s |
| (d) the rule's own step, BA:766-771 | 64 rows and 8 targets, the 8th at 33.15 s; or, with the row cap chosen first, 32 rows and 16 targets, the 16th at 36.75 s; a report cap of 128 | none needed | 128 rows and 8 targets, the 8th at 39.3 s; or, with the row cap chosen first, 64 rows and 16 targets, the 16th at 35.6 s; a report cap of 128 |

(d) lowers the target cap in steps of 8 and the row cap in powers of two,
keeping the row cap as large as it can, which gives the first pair; choosing the
row cap first, as BA:733-734 does, gives the second; each takes E = T, as BA:731
does (lane openRepoProject-3's W36 L-a). On the 150 ms basis (b) alone still
fails the cap test and would need (c) or (d) as well. (c) keeps the 5 s removal
floor and moves the spawn limit, and with it the ratified 60 s invocation
deadline, `budget.invocation_timeout_seconds` in every plan record (80.55 s on
the 150 ms basis, 65.0 s on the mixed one), and the 64 s run bound of "Clean
bounds its Git work and reports omitted work", later (lane openRepoProject-3's
W42 L-1). On the measured basis, at step (i)'s measured costs and with
10,000-file or 20,000-file removals, no cap fails and no option is needed. Which
basis the cap test uses, or what the two probes then unmeasured cost, was the
first step of open question LQ-20; Brett Heap chose its step (i), to measure
them, on 2026-10-22, and since the case passes on the measured basis none of its
options is taken (Risks, Open Questions; the lead's R-207 and R-208, on lane
openRepoProject-3's W36 M-A and M-B, and R-236).

D21's reachability probe adds one child for each of at most 16 rows
and one to each revalidation (LQ-13); its walk, measured by LQ-20's step (i)
over a whole history of 9,940 commits at 106.9 ms warm, makes those 32 children
about 3.4 s, or 5.1 s with the margin, which the measured basis above counts,
leaving 21.3 s at the 16th spawn where row 4c reads false; task 2.1's 26.4 s
was the margin before LQ-11 and LQ-13 added children (W31 L-6). A slower
walk is never unsafe: one stopped at its 5 s budget makes its row
`inspection-error` and the plan incomplete, one that the deadline cuts gives
`deadline-exceeded`, and at revalidation one that runs past its own budget while
the deadline is not the limit refuses the target with `state-changed`, while one
that the deadline cuts there leaves it `not-attempted` with `deadline-exceeded`
(D21, R-124, R-171). Under D9 a removal running past the deadline is bounded by
its ceiling, not by the fit. The report keeps the baseline layout and adds
`Report: complete` or `Report: incomplete (CODES)`, and, for a repository of at
most 128 worktree rows, `--all-safe would select N`; above 128, where
`--all-safe` itself would be incomplete, it prints `--all-safe would be
incomplete (inspect-cap)` instead, while its JSON carries `selected: null` and a
`notes` entry with code `inspect-cap` and `rows`, the count of registered
worktree rows (R-15); the note does not make the report incomplete. Above 128
the gates still run per inspected row, so `excluded` lists every inspected row a
gate excludes with its reason as in any report, and only the selection step is
withheld (R-17). Above 128 the `plan_digest` is computed over the same canonical
text as any plan, which covers only the repository's identity fields, the merge
target and `selected`, with `selected` null, and `--expect-plan` never consumes
it, because an apply there is an incomplete plan and is refused before the
digest is compared; at most 128 rows a report's digest equals the `--all-safe`
preview's for the same repository identity, merge target and selection, since
the mode is not in the digest, and an `--expect-plan` carrying it matches, which
is intended; the digest also covers the merge target's name and SHA, so a target
that advances between the report and the preview gives `plan-digest-mismatch`,
which is safe (R-19). It exits 0, 1 or 2 by completeness (R2).

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
still runs. Every delegate runs with D6's push-child scrub (LQ-12). Where
D11's configuration-path test failed, `update`'s report rows carry D18's
`relative-config-path` text in their `errors`, while its refusal of `--apply
--component shape` or `bench` keeps the message it gives for any checkout whose
`dirty` is not exactly false, as it does for an old Git: the form of Brett
Heap's ruling LQ-15, the lead's R-102 (c) 3, has `update` refuse as it does
below the floor, and no more.

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

The table is not exhaustive. Behaviours that Brett Heap's rulings LQ-10 and
LQ-11 rely on, `core.trustctime`, `core.checkStat`, `config --type=bool`,
`extensions.worktreeConfig` and the `commondir` file, are all older than 2.36
and were checked alike on 2.36.6 and 2.43.0 (lane openRepoProject-3's W9 L9,
R-125; D7, D11).

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
past the cap is excluded by a gate after the cap, the line `  these deferred
rows will not drain while the 16 rows ahead of them are REASONS; review those
worktrees, then remove them yourself (--force for any that holds a submodule)`
(R-24), REASONS those rows' reasons, each once, in gate order and joined by
`, `, so that it reads as before when all 16 are `contains-submodule` (W21 L-f,
R-146), but for its closing clause, which names `--force` because Git refuses a
plain `git worktree remove` of a worktree that holds a submodule (lane
openRepoProject-3's W59 G-4, R-253); the residual-window line, `Not protected:
ignored files created, index flags set, operations started or worktree-only
commits made after the last check, and any change after Git's own check.` (its
third item by LQ-14, its fourth by LQ-13); and, when a complete plan selects
nothing, `No eligible worktrees`.

The next steps by reason: `dirty` "commit or preserve the changes";
`ignored-local-files` "move or delete the ignored files by hand";
`unstarted-branch` "no commit was made on this branch here since it was created;
review, then git worktree remove yourself (--force if it holds a submodule)";
`reflog-unavailable` "the branch's reflog is missing, expired or undecidable;
review, then git worktree remove yourself (--force if it holds a submodule)",
since both are gate 7, ahead of `contains-submodule`, and a plain `git worktree
remove` of a worktree holding a submodule exits 128 (lane openRepoProject-3's
W52 F-7, R-248); `contains-submodule` "review, then git worktree remove --force
yourself" (W52 F-8, R-248); `hidden-local-state` "review, then remove the
worktree yourself"; `operation-in-progress` "a git am, merge, notes merge,
cherry-pick, revert, rebase or bisect is, or may be, in progress there; finish
or abort it (a squash merge that holds an autostash ends with git commit,
--allow-empty where nothing is staged, or with git merge --quit, which keeps the
edit in the stash list), or, where --abort fails for a marker with nothing in
progress, its --quit, or, where Git leaves such a marker in place, delete it by
hand from that worktree's git directory, then run again" (LQ-14, R-126, R-146,
R-171), the `--quit` clause for a marker left with nothing in progress, such as
an empty `sequencer` or `rebase-merge` directory, where `--abort` fails and only
`--quit` clears it (W52 F-9, R-248), the clause naming the failed `--abort`,
since for an empty `rebase-merge` `git status` still reports a rebase in
progress (W59 G-5, R-253), and the by-hand clause for a leftover marker that no
Git command clears, on Git 2.43.0 and 2.36.6 alike: an empty `CHERRY_PICK_HEAD`,
`REVERT_HEAD` or `MERGE_AUTOSTASH`, file or directory, whose `--abort` exits 128
and whose `--quit` exits 0 and leaves it; a lone `BISECT_LOG` or an empty
`BISECT_START`, which `git bisect reset` leaves, there being no `--quit`, and on
2.36.6 a `BISECT_START` naming a branch that another worktree has checked out,
whose reset exits 1; an empty `MERGE_HEAD` directory, which `git merge --abort`
and `--quit` leave; a `NOTES_MERGE_REF` or `NOTES_MERGE_PARTIAL` file, which
`git notes merge --abort` leaves; and a `rebase-apply`, `rebase-merge` or
`sequencer` that is an empty file, which every `--abort` and `--quit` fails or
leaves (writer E's table, R-259; round (h) re-ran it on both builds, and deleted
eight such markers by hand from the worktree's `git rev-parse --git-dir`, after
which `--all-safe` selected all eight rows);
`worktree-only-commits` "a commit is, or may be, held only by this worktree's
HEAD reflog or refs/worktree; keep it on a branch or tag, or review, then git
worktree remove yourself" (LQ-13); `registration-mismatch` "review, then git
worktree repair or git worktree prune, unset core.worktree and core.bare in the
repository's config, or in that worktree's config.worktree, or remove the row by
hand" (LQ-11, R-125), naming both files from which Git applies the redirect (W52
F-3, R-248), and, where any row of the plan has a path that could not be read,
as below, "review, then git worktree repair, unset core.worktree and core.bare
in the repository's config, or in that worktree's config.worktree, or remove the
row by hand; a row's path could not be read, so do not run git worktree prune,
git worktree remove or git gc until it can" in its place (W87 M-1; the lead's
R-310); `inspection-error` "review, then git worktree repair or git worktree
prune, or remove the row by hand", and, for an `inspection-error` row whose path
could not be read, its planning `lstat` failing other than for the path's
absence or cut at its budget, a row whose `lstat` the deadline stopped included,
so that its `present` is null, "inspect the row by hand; its path could not be
read, so do not run git worktree prune, git worktree remove or git gc until it
can", which the preview prints for such rows in a group of their own under
`inspection-error`, since `git worktree prune` deletes the administrative
directory of a live worktree whose path Git cannot stat (D9; lane
openRepoProject-3's W73 M-1 and W87 M-1; the lead's R-307), and, where any row
of the plan has such a path, "review, then git worktree repair, or remove the
row by hand; a row's path could not be read, so do not run git worktree prune,
git worktree remove or git gc until it can" for any other `inspection-error`
row, since `git worktree prune` acts on the whole repository and so deletes the
directory of the row whose path could not be read, whichever row it is run for
(the lead's R-310); `locked-worktree` "unlock it yourself if it should go";
every other class its recommendation. The `stale-worktree` class's, "Review and
prune stale worktree metadata manually.", and its locked form, which lane
openRepoProject-3's W52 F-10 gave feature 004, become, where any row of the same
plan has a path that could not be read, a row whose planning `lstat` failed
other than for the path's absence, or was cut at its budget, a row whose `lstat`
the deadline stopped included, so that its `present` is null, "Review and prune
stale worktree metadata manually; a row's path could not be read, so do not run
git worktree prune, git worktree remove or git gc until it can." and, for a
locked row, in the report's row recommendation alone, "Review, unlock it, then
prune stale worktree metadata manually; a row's path could not be read, so do
not run git worktree prune, git worktree remove or git gc until it can.", since
`git worktree prune`, run for a stale entry's sake, deletes the administrative
directory of a worktree whose path Git cannot stat too, on Git 2.43.0 and 2.36.6
(lane openRepoProject-3's W86 NM-1, through lane openRepoProject-4; the lead's
R-320, which Brett Heap ruled on 2026-10-22, "R-320: yes", R-321); with no such
row they print unchanged. A locked stale row is excluded in the preview as
`locked-worktree`, whose gate comes ahead of its class, with the next step
"unlock it yourself if it should go", so the locked form is never a preview
group's next step: it prints only as the report row's recommendation, in the
human report and in `--json`, as feature 004 at `0a82a62` builds it (lane
openRepoProject-3's W95 LOW-3).

The question: `Remove N worktrees, keeping N branches? [yes/N]`, in the singular
for one. The wait line, at most once: `Waiting for git worktree remove PATH to
finish; a started removal is never interrupted (at most 300 s).` Success:
`Removed N; branches kept: B1, B2.` A stop: `Stopped at PATH (REASON). Removed K
of N. Not attempted: P1, P2. Next: project clean ROOT --all-safe`, then the
retained branches and the residual-window line. The partial-removal note, under
the `dirty` advice, or on a `partially-removed` target whose `.git` file and
registry entry the rescan finds present: `Probable partial removal: inspect,
then git worktree remove --force PATH by hand.` On a `partially-removed` target
where the rescan finds either gone, the note reads `Probable partial removal:
inspect, then git worktree prune and delete PATH by hand.`, since `git worktree
remove --force` then exits 128 on Git 2.43.0 and 2.36.6 while the path remains,
with `validation failed, cannot remove working tree: 'PATH/.git' does not exist`
once the `.git` file is gone and `'PATH' is not a working tree` once the entry
is, and exits 0 once the path itself is gone, the entry remaining, as lane
openRepoProject-3's W70 LOW-1 found on both builds, while `git worktree prune`
and a deletion by hand succeed (W52 F-1; R-285; Brett Heap's ruling of
2026-10-22, "F-1: prune-then-delete", R-263). On a `partially-removed` target
whose `.git` file the rescan cannot read, its `lstat` failing other than for the
file's absence or cut at its budget, whatever it finds of the registry entry,
the note reads `Probable partial removal: inspect PATH by hand; its .git
could not be read, so do not run git worktree prune, git worktree remove or git
gc until it can.`, since `git worktree prune` deletes the administrative
directory of a live worktree whose `.git` Git cannot stat (D9; lane
openRepoProject-3's W73 M-1; the lead's R-284, which Brett Heap confirmed on
2026-10-22, "R-284: yes", R-290). For a locked worktree, which `git worktree
remove --force` refuses, the note reads `Probable partial removal: inspect,
unlock it, then git worktree remove --force PATH by hand.` (W52 F-2, R-248). For
a locked row that note replaces the ratified recovery text of `0050f3e`, which
the delta keeps for every other row, by Brett Heap's ruling of 2026-10-22, "F-2:
yes" (W59 G-1, R-253; R-263); a report row needs no other text, since its `.git`
file and registry entry are present (D4). The locked note is the report row's
own form: a ceiling target, which is no report row, shows the first, the second
or the third note and never the locked one, since the deltas give it no locked
form and feature 004 builds none (`partial_removal_text()` at `3bc1d68`; lane
openRepoProject-3's W87 LOW-3). A locked ceiling target whose `.git` file and
registry entry the rescan finds present therefore shows the first note, and its
`git worktree remove --force` fails safe: Git refuses it while the worktree is
locked, exit 128 on Git 2.43.0 and 2.36.6, and removes nothing. Where the `.git`
file cannot be read, a ceiling target shows the third note, locked or not and
whatever the rescan finds of the registry entry, by R-284's letter, "A `.git`
read that fails or is cut gets a third note", and the third note would take
precedence over a locked one, as over the entry's state, were a ceiling target
ever given it: Git treats a path it cannot stat as missing, so that once such a
worktree is unlocked, `git worktree remove`, with or without `--force`, deletes
its administrative directory as `git worktree prune` does, on Git 2.43.0 and
2.36.6 (lane openRepoProject-3's W80 M-1; the lead's R-294). The third note's
words name `git worktree prune`, `git worktree remove` and `git gc`, the last
because its automatic worktree prune deletes such a directory once its index is
three months old (W80 L-6), as Brett Heap ruled on 2026-10-22, "R-324: yes" (the
lead's R-343).

Refusal messages keep the baseline wording where a test reads it:
`target-excluded` for the current worktree, `Cannot remove the current
worktree.`; for a class that is not removable, `Worktree is CLASS; only clean
merged worktrees may be removed.`; for a gate, `Worktree is excluded: REASON;
NEXT STEP`. Branch deletion keeps the baseline's refusals, except for a branch
that the main worktree holds, where the baseline's `Remove the linked worktree
first; branch deletion is a separate action.` names a removal that Git refuses
for the main worktree (`git worktree remove` of it exits 128, "is a main working
tree"): `Branch BRANCH is checked out in the main worktree; detach HEAD there,
or check out NAME there, then retry.`, NAME the merge target, a detach being
named first because Git refuses a checkout of the merge target while a linked
worktree holds it (lane openRepoProject-3's W52 F-5, lane openRepoProject-5's
RI-4, R-248). This change does not state branch deletion's delegated argument
vector; feature 004 runs it as `git -C ROOT branch -d -- BRANCH`, the `--`
ending the options, so that a branch whose name begins with `-` is deleted
rather than read as an option (W52 F-4, R-259). A plan-blocking refusal names
its remedy: `inspection-incomplete` "repair or remove the inspection-error rows
first: git worktree repair, git worktree prune, or remove the row by hand after
review", and, where any row it counts is excluded as `registration-mismatch`,
"repair or remove the inspection-error rows first: git worktree repair, git
worktree prune, unset core.worktree and core.bare in the repository's config or
in a worktree's config.worktree, or remove the row by hand after review"; but
where any row of the plan has a path that could not be read, its planning
`lstat` failing other than for the path's absence, or cut at its budget, a row
whose `lstat` the deadline stopped included, the remedy is instead "repair or
remove the inspection-error rows first: git worktree repair, or remove the row
by hand after review; a row's path could not be read, so do not run git worktree
prune, git worktree remove or git gc until it can", or, where any row it counts
is excluded as `registration-mismatch`, "repair or remove the inspection-error
rows first: git worktree repair, unset core.worktree and core.bare in the
repository's config or in a worktree's config.worktree, or remove the row by
hand after review; a row's path could not be read, so do not run git worktree
prune, git worktree remove or git gc until it can", since `git worktree prune`
deletes the administrative directory of a live worktree whose path Git cannot
stat, and omitting prune advice never harms (lane openRepoProject-3's W87 M-1;
the lead's R-307 and R-310, which Brett Heap confirmed on 2026-10-22 in his
words "R-307: yes; R-310: yes", R-319); `inspect-cap` "N rows exceed the row cap
of M; remove worktrees explicitly, or prune stale entries by hand", which is
always, in place of the ratified remedy, "{N} rows exceed the row cap of {M};
remove worktrees explicitly, or prune stale entries by hand; if a worktree's
path cannot be read, do not run git worktree prune, git worktree remove or git
gc until it can", its `{N}` and `{M}` standing for the row count and the cap,
the ratified remedy's `N` and `M`, since the rows past the cap are never read
(lane openRepoProject-3's W86 NM-1; the lead's R-320, which Brett Heap ruled on
2026-10-22, "R-320: yes", R-321); `deadline-exceeded` "the run ran out of time;
remove worktrees explicitly or re-run". Every warning of this section, the third
note's too, ends "do not run git worktree prune, git worktree remove or git gc
until it can", the cap remedy's "if a worktree's path cannot be read" before it,
as Brett Heap ruled on 2026-10-22, "R-324: yes" (the lead's R-343): `git
worktree remove`, with or without `--force`, deletes the administrative
directory of a worktree whose path Git cannot stat, as `git worktree prune` does
(lane openRepoProject-3's W91 MEDIUM-2 and W95), and so does the automatic
worktree prune of `git gc` once that directory's index is older than
`gc.worktreePruneExpire`, three months by default (W80 L-6, E6); every other
word of those texts stands. Every refusal that a `core.worktree` or `core.bare`
redirect of a linked worktree causes is that `inspection-incomplete` one, with
the variant remedy, in its unread form where any row of the plan has a path that
could not be read: in the preview, the apply and the report of the batch; in
push and branch deletion, which count every row; and in a single-target removal
naming the redirected row, whose own row is `inspection-error`, so that its
incomplete plan is refused before any gate's exclusion, never with
`target-excluded` and the class wording. A redirect of the main worktree itself,
by a `core.worktree` or `core.bare` in the repository's `config` or in the main
worktree's `config.worktree`, is refused earlier, at resolution, with
`target-not-repository-root`, before any plan is built, where the root is passed
by an absolute path, or by a bare name that `discover()` resolves to the root
itself, through a family holder or a manifest there (round (h), with feature 004
at `d764c26` on Git 2.43.0 and 2.36.6; lane openRepoProject-3's W64 M-1 and W80
M-2). Otherwise a bare name takes Git's toplevel, row 2, as D8 and BA:860 have
it, and under a `core.worktree` that toplevel is the redirect target: a target
outside any repository, or a missing one, is refused with the plain message
quoted below, which names that target; one inside the repository resolves to the
repository; and another repository's root resolves to that other repository.
Under a `core.bare` true row 2 fails, and the run is refused with
`repository-not-found`, `No project found at PATH; supply a path or name.`,
unless the directory X that the name finds holds a `.project.json` file or a
`.devcontainer` directory, which `discover()` takes after row 2 fails, and then
the variant prints (W80 M-2, reading feature 004's `discover()` at `2707ff2`,
with row 2 run on Git 2.43.0 and 2.36.6; lane openRepoProject-3's W87 LOW-2, a
bare name through the projects directory in report mode on both builds,
`discover()` at `3bc1d68`, `project:549`). A relative path naming the root, from
any directory, as `./X` from its parent or `../X` from a sibling, or no argument
run from the root, resolves as "Clean resolves its target Git-first" states, to
the repository Git finds there with `root` set to its main worktree: under a
`core.bare` true Git finds no worktree there, and the run is refused the same
way, but under a `core.worktree` it is not refused and builds a plan whose main
row Git reads where `core.worktree` points (lane openRepoProject-3's W70 LOW-3
and W80 L-4; round (i)'s fixtures, where such runs exit 0, or 1 with an
incomplete plan). A refusal at resolution names the redirect, since feature
004's plain message for the code, `Not the main worktree of a repository: PATH;
pass the repository root.`, asks for the root that was passed: it reads `Not the
main worktree of a repository: PATH; core.worktree or core.bare redirects the
main worktree; unset both in the repository's config, or in the main worktree's
config.worktree, then run again.` It does so only where the directory the
resolution examined holds its own `.git`, a directory or a gitfile, whose
realpath is the repository's common directory, and Git run there uses another
work tree or none: another where row 3 succeeded and its toplevel is not that
directory, which only a `core.worktree` gives, and none where row 3 failed and
row 3b prints that `.git` as both the git directory and the common directory,
and `true`, which only a `core.bare` true gives, each from the repository's
`config` or the main worktree's `config.worktree`. A relative `core.worktree`
naming a missing directory redirects too, but Git run there uses no work tree at
all: row 3 and row 3b each exit 128 with Git's own `fatal: cannot chdir to
'<value>'`, so the plain message prints, in the plain layout, the `.git`-file
layout and a submodule checkout moved by hand alike (lane openRepoProject-3's
W80 L-2 and W81 M-1, on Git 2.43.0 and 2.36.6); run there, `git config --unset`
fails the same way, as does `git config --file`, while run outside the
repository `git config --file X/.git/config --unset core.worktree` clears it
(round (k), on Git 2.43.0). Where row 3 succeeded the decision reads only the
filesystem (the `lstat` of the `.git`, its gitdir line and the realpaths). Every
other `target-not-repository-root` refusal keeps the plain message: a
subdirectory, a linked worktree, a linked worktree that its own
`config.worktree` redirects, a directory outside any repository, a submodule
checkout whose own configuration redirects nothing, and a `git init --bare`
repository passed by its own directory, which holds no `.git` and which an unset
of `core.bare` does not make a work tree. A repository made by `git init --bare
X/.git` and passed as X has the configuration of a checkout at X whose
`core.bare` is true, and nothing Git reads tells the two apart, so it takes the
variant, which is true of it: with `core.bare` unset, X resolves. A main
checkout whose `.git` is a file and whose `core.worktree` names that checkout
resolves as before (D8); one whose `core.worktree` names another directory, or
whose `core.bare` is true, takes the variant. A submodule checkout keeps the
plain message only where its own configuration redirects nothing, its toplevel
then being its own directory, or where, moved by hand, its relative
`core.worktree` names a missing directory; feature 004's check that excludes a
checkout whose row 3 prints a superproject decided no outcome in any fixture
that W80 or W81 built. One whose module's `config`, `modules/<name>/config`,
sets `core.bare` true, or a `core.worktree` naming another directory, a sibling
submodule's checkout among them, takes the variant, which is true of the
redirect, and so does a copy of a submodule checkout whose gitfile names the
module, where row 3 run in the copy finds no gitlink and prints two lines.
Unsetting the redirect does not make any of them a main worktree: the first
three are then refused again, with the plain message, and the superproject's
root is what resolves, so a person is refused twice, and for the copy the remedy
may not clear the cause either. These are known limits, recorded and not fixed
(W80 L-5 and W81 L-1, on Git 2.43.0 and 2.36.6). Row 3b runs only on that
refusal, after the resolution has decided to refuse, counted and bounded as row
3 is, and only where the directory holds a `.git`, so a run that resolves spawns
no child for it, and a row 3b that fails or is cut leaves the plain message
(round (i), with feature 004 at `7164d7f` on Git 2.43.0 and 2.36.6; the lead's
R-271). `relative-config-path` prints one line per variable that fails D11's
test, in the order `HOME`, `XDG_CONFIG_HOME`, `GIT_CONFIG_GLOBAL`,
`GIT_CONFIG_SYSTEM`: `NAME is set to a path that does not begin with /; make it
absolute or unset it.`, never the value; doctor's `error` row and status's
`errors` entry carry the same text. The line and its order are a fill of this
change: Brett Heap's ruling LQ-15 names the code and the refusal, not the text.

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
and LQ-14 under the batch and revalidation.

### D21. Commits held only by a worktree (LQ-13)

Brett Heap's ruling LQ-13 of 2026-10-21 keeps a worktree in place when a
commit that only its own HEAD reflog or its `refs/worktree/` holds is
unreachable from every branch, tag and remote ref. `git worktree remove`
deletes the worktree's administrative directory, and with it `logs/HEAD` and
every ref under `refs/worktree/`, which live there and are never packed
(`common_list`, `path.c:111` at 2.36.6 and `:116` at 2.43.7, which lists
`logs/HEAD`, `logs/refs/worktree` and `refs/worktree` as per-worktree;
`should_pack_ref`, `refs/files-backend.c:1176` at 2.36.6 and `:1174` at
2.43.7); such a commit is then held by nothing and is left to
garbage collection. Lane openRepoProject-3 found the gap (F1 H-1 at
`2cf34d3`). Each decision below is the simple, conservative one:

- Reason. A new exclusion reason, `worktree-only-commits`, in the gates'
  kebab-case. No existing reason fits: `reflog-unavailable` names the branch's
  reflog and its remedy says that reflog is missing, expired or undecidable;
  `unstarted-branch` says the opposite, that no work was done; and
  `inspection-error` would make the whole plan incomplete for a state that is
  fully established. A check that fails, which establishes nothing, is
  `inspection-error` as every other failed read is (Fail closed).
- Place. The last gate, after `hidden-local-state` and LQ-14's
  `operation-in-progress` (D22), so that a row with an operation in progress
  runs no reachability child. It is a protection, so it
  runs before any row is selected, in every mode, `mode: "single"` included,
  where an excluded P refuses `target-excluded`; a row an earlier gate excludes,
  as every row with work in its index or tree is, needs no such protection. It
  sits past `deferred-target-cap` with the index gates because it costs a Git
  child, which bounds it at 16 rows per run (D12).
- Reads. One bounded filesystem read of `logs/HEAD` in the worktree's
  administrative directory, at most 64 KiB, the cap of D10's branch reflog, and
  counted in the filesystem budget, each line parsed as D10 parses one; every
  non-zero old and new object it names is a candidate. Then, after the
  hidden-state probe, one Git child in the worktree, with the scrub, the
  protocol pins and `GIT_OPTIONAL_LOCKS=0` of every read-only probe:
  `git -C <worktree> rev-list --max-count=1 --glob=refs/worktree <candidates>
  --not --branches --tags --remotes <non-zero branch reflog objects>`.
  `--glob=refs/worktree` adds the worktree's own per-worktree refs, which only
  that worktree sees. The negative side is every branch, tag and
  remote-tracking ref and every non-zero object that the row's branch reflog
  names (its creation entry's all-zeros object would make the child exit 128,
  lane openRepoProject-3's W10 M1, R-124 (c)), which D10 already read and
  which survives the removal in the common directory, so that an amend, a reset
  or a rebase of the row's own branch is not taken for lost work: such a commit
  is not held only by the worktree. The child prints a commit exactly when one
  is reachable from the candidates or from `refs/worktree/` and from none of the
  negatives.
- Bounds. The read takes the filesystem budget and the child `min(5 s, work
  remaining)`, as every read and child do; `--max-count=1` keeps the output to
  one line.
- Fail closed. A missing (`ENOENT` or `ENOTDIR`) or empty `logs/HEAD` gives no
  candidate, since no reflog then holds anything. Only a decided result gives
  `worktree-only-commits`, as only a decided result gives `reflog-unavailable`
  for the branch's reflog (D10): a child that exits 0 and prints anything, and
  a `logs/HEAD` whose content cannot be decided, read to the 64 KiB bound or
  holding a line that does not parse. A read or child that fails establishes
  nothing and is treated as every other evidence read is (`BA:188-192`,
  `BA:642-644`): any other error on the read, and a child that cannot be
  started or exits nonzero, as on a missing object (`fatal: bad object`, 128),
  make the row `inspection-error`, and so does a child stopped at its 5 s
  budget, which records `probe-timeout`, so that the plan is incomplete with
  `inspection-incomplete`; a read not finished within the filesystem budget
  does the same, recording `probe-timeout`, as feature 004 builds it (lane
  openRepoProject-3's W32 L1, R-200, R-208); and a read or child that the
  deadline cuts gives `deadline-exceeded` (the lead's R-124 (a), on lane
  openRepoProject-3's W10 H1, which found the first form of this rule departing
  from the packet).
- Revalidation. After the hidden-state probe, revalidation reads `logs/HEAD`
  again and runs the same child, with the non-zero objects of the plan's
  branch reflog; a printed commit, the 64 KiB bound or a line that does not
  parse refuses the target with `worktree-only-commits`, and a read or child
  that fails or runs past its own budget while the deadline is not the limit,
  which cannot make a plan incomplete there, is a value that cannot be re-read
  and refuses it with `state-changed`, as a status probe that fails there does,
  while one that the deadline cuts leaves the target `not-attempted` with
  `deadline-exceeded` (R-124, R-127, R-171). That is the sixth Git child of a
  revalidation (D7, D14), and it catches a commit made, or a ref under
  `refs/worktree/` created, after the plan, which no step read before (lane
  openRepoProject-3's reader RB at `2cf34d3`, whose cases were all removed with
  exit 0; R-107). After that revalidation such a commit is in the residual
  window, whose line names it (D18). Taking the plan's branch reflog objects as
  they were makes revalidation stricter than planning: a commit made on the
  branch after the plan and reset away, which the branch's reflog then holds,
  refuses the target. That is kept, since it fails safe (lane
  openRepoProject-3's W10 L3, R-124 (d)).
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
missing object, which makes the row `inspection-error`; and for a branch
amended and reset in the worktree it prints the pre-amend commit with only the
refs as negatives, and nothing once the branch reflog's objects are negatives
too. On Git 2.43.0, after an interactive rebase onto a merge target that had
moved, with one pick turned into a fixup, it prints the intermediate commit that
the fixup replaced (Risks).

### D22. Operations in progress (LQ-14)

Brett Heap's ruling LQ-14 of 2026-10-21 never removes a worktree with an
operation in progress. Git keeps the state of a merge and its autostash, a
notes merge, a cherry-pick or revert, an `am`, a rebase or a bisect in the
worktree's own git directory, its
administrative directory for a linked worktree, since none of these names is
in `common_list` (`path.c:111` at 2.36.6, `:116` at 2.43.7). An operation that
stopped with the index and the working tree equal to the branch head reads clean
to the status probe and to Git's own check, and the removal deletes its state: a
failed `am`, a merge or a cherry-pick sequence resolved to the branch's own
content, a bisect with `--no-checkout` (lane openRepoProject-3's F1 H-2 at
`2cf34d3`), a squash merge holding an autostash and a notes merge stopped at a
conflict (its W14 M1). Each decision below is the simple, conservative one:

- Reason. A new exclusion reason, `operation-in-progress`. No existing reason
  fits: the row is not dirty, `hidden-local-state` names index flags,
  `reflog-unavailable` a branch reflog, and `inspection-error` would make the
  whole plan incomplete for a state that is fully established.
- Place. After `hidden-local-state` and before `worktree-only-commits`: a
  protection, so before any selection and in every mode; past
  `deferred-target-cap` with the other gates that read the worktree's own
  state, and before the gate that costs a Git child, so that a row with an
  operation in progress runs none. Most operations stopped with work in the
  index or the tree, or with a detached head, are already `dirty` or
  `detached`, and those reasons stand.
- Markers. Taken from Git's own state detection, read in the release sources
  of 2.36.6 and 2.43.7 (tags `v2.36.6` and `v2.43.7`, D7), not from memory:
  - `MERGE_HEAD`, `rebase-apply` (an `am` when it holds `applying`, otherwise
    a rebase), `rebase-merge`, `CHERRY_PICK_HEAD`, `REVERT_HEAD` and
    `BISECT_LOG`, which `wt_status_get_state`, `wt_status_check_rebase` and
    `wt_status_check_bisect` test (`wt-status.c:1745-1781`, `:1675-1700` and
    `:1702-1713` at 2.36.6; `:1773-1809`, `:1703-1728` and `:1730-1741` at
    2.43.7);
  - `sequencer`, whose `todo` `sequencer_get_last_command` reads for a
    cherry-pick or revert sequence (`sequencer.c:2513` at 2.36.6, `:2660` at
    2.43.7), taken as the whole directory because `create_seq_dir` creates it
    with `mkdir`, which fails while it exists (`sequencer.c:3033` and `:3065`
    at 2.36.6, `:3194` and `:3226` at 2.43.7), so its presence alone stops a
    new sequence;
  - `BISECT_START`, which `git bisect reset` tests to decide that a bisect is
    in progress (`builtin/bisect--helper.c:718` at 2.36.6,
    `builtin/bisect.c:791` at 2.43.7) and which `bisect_clean_state` removes
    last (`bisect.c:1179-1182` at 2.36.6, `:1198-1201` at 2.43.7), so a
    cleanup cut short can leave it alone;
  - `MERGE_AUTOSTASH`, the stash commit that `git merge --autostash`, or
    `merge.autoStash`, saves before a merge and that only that file names
    until the merge ends (`git_path_merge_autostash`, `path.c:1559` at 2.36.6
    and `:1593` at 2.43.7, which `builtin/merge.c` applies and removes); a
    `git merge --squash` that does not fast-forward keeps it until the squash
    is committed on 2.40.4 and 2.43.0, while a fast-forward squash, and every
    squash on 2.36.6, applies it at once, so a worktree that reads clean can
    hold a person's edit only there (lane openRepoProject-3's W14 M1, R-126;
    its W21 L-d). `git stash pop` does not end it, since it finds no stash
    entry, and nor, after a squash, which writes no `MERGE_HEAD`, does `git
    merge --abort`, which refuses where no `MERGE_HEAD` exists before it reads
    `MERGE_AUTOSTASH` (`builtin/merge.c:1333-1334` at 2.36.6, `:1324-1325` at
    2.43.7); after a merge that writes `MERGE_HEAD`, with `--no-commit` or
    stopped at a conflict, `git merge --abort` ends it and applies the edit
    back. `git commit` (`--allow-empty` where nothing is staged) applies the
    edit back, or, where the edit conflicts with what the merge brought, ends it
    with the edit kept in the stash list and conflict markers in the file, and
    `git merge --quit` and `git reset --hard` end it by saving the edit to the
    stash list, which the common directory holds and a removal keeps: both call
    `remove_merge_branch_state`, which calls `save_autostash`
    (`branch.c:705-712` at 2.36.6, `:814-821` at 2.43.7;
    `builtin/merge.c:1350-1356` and, through `remove_branch_state`,
    `builtin/reset.c:564` at 2.36.6, `:1341-1347` and `:511` at 2.43.7). D18's
    next step names `git commit` and `git merge --quit` (lane
    openRepoProject-3's W26 F-1, R-171, which corrects W21's L-c, whose `git
    reset --hard` was cut short by its own pipe). Checked here on Git 2.43.0 and
    2.56.0: after `git merge --squash --autostash -s ours` with an edited file,
    `git reset --hard` and `git merge --quit` each print `Autostash exists;
    creating a new stash entry.`, leave no `MERGE_AUTOSTASH` and add one stash
    entry; `git commit --allow-empty` prints `Applied autostash.` and restores
    the edit; `git merge --abort` exits 128 and `git commit` alone finds nothing
    to commit, each leaving the marker; and after `git merge --autostash
    --no-commit -s ours`, which writes `MERGE_HEAD`, `git merge --abort` and
    `git commit` each print `Applied autostash.`, leave neither marker and
    restore the edit, while a `git commit` that ends a `--no-commit` merge whose
    edit conflicts with what the merge brought reports that applying the
    autostash resulted in conflicts, leaves no `MERGE_AUTOSTASH`, adds one stash
    entry and writes conflict markers into the file (lane openRepoProject-3's
    W31 L-3, R-190);
  - `NOTES_MERGE_PARTIAL` and `NOTES_MERGE_REF`, which a `git notes merge`
    stopped at a conflict leaves and which its `--commit` and `--abort`
    delete (`merge_abort`, `builtin/notes.c:686` with the deletions at
    `:691-698` at 2.36.6, and `:786` with `:791-798` at 2.43.7; `merge_commit`
    calls it, `:704` and `:804`).
  An entry of one of these eleven names, of any kind, is a marker; the set is
  a superset of what `git status` reports, never a subset, and wider by the
  last three, which `git status` does not report. `NOTES_MERGE_WORKTREE`,
  which holds a notes merge's resolutions, is not a marker, since `--abort`
  and `--commit` leave it behind and it would keep a worktree out for
  nothing; nor is `SQUASH_MSG`, which a squash undone by hand leaves (R-126).
- Reads. One listing of `<common_dir>/worktrees/<admin_id>`, a filesystem
  call under the filesystem budget like D6's identity reads, and no Git child:
  a status-like child would read the same files and cost a child per row.
- Bounds. The listing takes `min(5 s, work remaining)` as every filesystem
  call does; a directory too large to list in that time makes the row
  `inspection-error` with `probe-timeout`.
- Fail closed. Only a marker present gives `operation-in-progress`. An error
  on the listing establishes nothing and makes the row `inspection-error`, as
  every failed read does, so that the plan is incomplete with
  `inspection-incomplete` (the lead's R-124 (b), the rule of D21 kept for
  consistency); a listing not finished within the filesystem budget records
  `probe-timeout` and makes the row `inspection-error` too, as feature 004
  builds it, like its `modules` check (lane openRepoProject-3's W32 L1, R-200,
  R-208), and the deadline gives `deadline-exceeded`, as for every read.
- Revalidation. The same listing runs again in revalidation's filesystem step,
  beside the target's identity and `modules` check, with no new Git child; a
  marker refuses the target with `operation-in-progress`; an administrative
  directory that the `operation-in-progress` listing finds absent is a
  registration difference, `identity-changed`, as feature 004 builds it (lane
  openRepoProject-3's W38 L-4 and W42 L-2); and a listing that fails, or runs
  past its own budget while the deadline is not the limit, refuses it with
  `state-changed`, as every filesystem call of that step does, by the one rule
  of `Cleanup revalidates destructive actions`, while one that the deadline cuts
  leaves the target `not-attempted` with `deadline-exceeded` (R-124, R-126,
  R-127, R-208). It catches an operation started after the plan, which no step
  read before (lane openRepoProject-3's reader RB at `2cf34d3`, whose cases were
  all removed with exit 0; R-107). An operation started after that revalidation
  is in the residual window, whose line names it (D18).
- Rendering. The reason appears where every gate's does, so no JSON field is
  added and the closed enums gain one value within `schema_version: 1`, before
  any release; the human preview groups it with its next step (D18).

Checked here on Git 2.36.6 and 2.43.0, in a linked worktree each time: a `git
am` of a patch that does not apply leaves `rebase-apply`; a `git cherry-pick`
of a range stopped at a conflict leaves `CHERRY_PICK_HEAD` and `sequencer`,
holding `todo`; a `git merge --no-commit -s ours` leaves `MERGE_HEAD`; and a
`git bisect start --no-checkout` leaves `BISECT_LOG` and `BISECT_START`, which
`git bisect reset` removes. In each case the pinned status probe printed no
record once the index and tree matched the branch head. On Git 2.43.0 a `git
merge --squash --autostash -s ours` with an edited tracked file leaves
`MERGE_AUTOSTASH` and `SQUASH_MSG`, an empty `git stash list` and no record
from the probe, while 2.36.6 applies the autostash at once and the probe shows
the edit; on both, a `git notes merge` stopped at a conflict leaves
`NOTES_MERGE_PARTIAL`, `NOTES_MERGE_REF` and `NOTES_MERGE_WORKTREE` with no
record from the probe, and its `--abort` leaves `NOTES_MERGE_WORKTREE` alone.

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
  reflog exceeds 64 KiB] -> Fails closed, as Brett Heap's ruling LQ-13 asks,
  and as D21's bound sets for an oversized reflog; the remedy says to keep any
  such commit on a branch or tag, or to review and remove the worktree by hand
  (D18, D21).
- [A commit that only the reflog of a ref under `refs/worktree/` holds, in
  `logs/refs/worktree/` of the administrative directory, which exists only
  under `core.logAllRefUpdates=always`, is no candidate, so a removal can leave
  it to garbage collection] -> Accepted, not widened (R-124 (d), R-127): Brett
  Heap's ruling LQ-13 names the HEAD reflog and `refs/worktree/`, and a ref's
  own reflog is outside its words (lane openRepoProject-3's W10 L5).
- [A marker left behind with nothing in progress, such as a `sequencer`
  directory after a crash or a lone `BISECT_START` after a cut-short `git
  bisect reset`, keeps its worktree out as `operation-in-progress`] -> Fails
  closed, as Brett Heap's ruling LQ-14 asks; the remedy says to finish or abort
  the operation; where `--abort` fails for a marker with nothing in progress, to
  use its `--quit`, which clears an empty `sequencer` directory (`git
  cherry-pick --quit`); and, where Git leaves such a marker in place, as `git
  bisect reset` leaves a lone `BISECT_LOG` or an empty `BISECT_START` and every
  command leaves an empty `sequencer` file, to delete it by hand from that
  worktree's git directory, after which the row is selected; Git itself refuses
  a new sequence while a `sequencer` directory exists (D18, D22; lane
  openRepoProject-3's W52 F-9, R-248, and W59 G-5, R-253; writer E's table,
  R-259, and round (h)).
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
  never unsafe (D11). Where the repository defines a clean filter, a ctime-only
  change under `core.trustctime=false` now runs that filter once per probe,
  where it ran none before, which widens the filter residual that LQ-16 leaves
  open with Brett Heap; a filter whose command is missing gives a false
  `dirty` or a failed probe, and both fail closed (lane openRepoProject-3's W9
  L2, R-125).
- [A repository whose every worktree carries a gitlink, the V5 deferral's
  motivating repository (Opensoft-Tenant: 20 rows pass every gate before
  `deferred-target-cap` and all 20 are `contains-submodule` after it), yields 0
  removable rows each run, and its deferred count never drains, because
  `contains-submodule` is an index gate tested after the deferral] -> The order
  stays, since the index gates cost a probe per row and the deferral keeps those
  probes to 16 (D12); the human report says why the deferred rows will not drain
  when every one of the 16 rows past the cap is excluded by a gate after the
  cap, `contains-submodule` among them (D18); 16 such rows ahead of a backlog
  stall it alike; V5's
  caveat was ratified with the deferral at the merge of PR #11.
- [In a repository whose `extensions.worktreeConfig` is true, LQ-11's
  effective-work-tree probe runs for every linked row at plan time. At BA's flat
  150 ms per child a 128-row `--all-safe --apply` there reaches its first
  removal at 45.3 s, past the 45 s spawn limit, and removes nothing, on every
  re-run as well, and a report goes incomplete above 147 rows; on D5's measured
  basis, with the two probes that task 2.1 did not measure at the costs that
  LQ-20's step (i) measured, 8.7 ms and 160.3 ms with the margin, all 16
  removals fit, the 16th spawning at 30.0 s (37.7 s with 20,000-file removals);
  on the mixed basis as first stated 11 do (D14)] -> Fails safe: a target that
  the floor stops is `not-attempted` with `deadline-exceeded`, as is every later
  one, and the run exits 1. Open question LQ-20 is resolved: Brett Heap chose
  its step (i) on 2026-10-22, those two probes were measured on task 2.1's
  protocol, and the case passes on the measured basis, D5's as ratified, so none
  of its options is taken: (a) accept it; (b) bound the plan-time work-tree
  probe to the selected targets, at most 16, and report the other rows' identity
  as unverified; (c) a longer work deadline where `extensions.worktreeConfig` is
  true, the 5 s removal floor kept; and (d) the rule's own step, lowering the
  caps (BA:766-771). D14 and Open Questions give each option's result on each
  basis as costed before the measurement (the lead's R-178, R-190, R-207, R-208
  and R-236).
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
  above) and the floor stays 2.36 with the scrub extended (D17, R-21). The
  children that LQ-11 and LQ-13 added since were measured by LQ-20's step (i) on
  2026-10-22, and the caps still stand (D14, LQ-20).
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
then git worktree remove yourself (--force if it holds a submodule)"; a merged
worktree whose branch reflog keeps no decisive entry (no activity for
`gc.reflogExpire`, 90 days by default, D10) is refused as `reflog-unavailable`
in single mode as well as withheld from the batch, with the remedy "the branch's
reflog is missing, expired or undecidable; review, then git worktree remove
yourself (--force if it holds a submodule)" (D18; lane openRepoProject-3's W52
F-7, R-248); and `--worktree P` removes a merged worktree whose upstream was
deleted, as `merged-removable` when its gates pass, its branch kept, where
`a040790` refuses it as `unpublished` (D6, Brett Heap's ruling on open
question 1). The README's clean section states them first.

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

Each is before Brett Heap with a recommendation, except LQ-20, which he resolved
on 2026-10-22 and which stays below as the record of what was costed, and the
last, F-1's (b) beside an unread row, which is put to him as a question, with no
recommendation here, and is not ruled; the deltas implement the reading stated,
and a different ruling edits the deltas before the archive.

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
- LQ-20, the fit where `extensions.worktreeConfig` is true (D14, Risks).
  RESOLVED on 2026-10-22: Brett Heap chose step (i), in his words to lane
  openRepoProject-2, "LQ-20: go with (i), measure first" (the lead's R-236). The
  two probes were measured on task 2.1's protocol, in the same container and at
  a 1-minute load of 15 to 21 on 32 threads: LQ-11's work-tree probe at 5.8 ms
  warm, 8.7 ms with the margin, and LQ-13's `rev-list` at 106.9 ms warm, 160.3
  ms with the margin, its walk covering a whole history of 9,940 commits (D14;
  `tasks.md` 2.1). The cap test, rerun on those costs, passes on the measured
  basis: at 128 rows and 16 targets where row 4c reads true, all 16 removals
  fit, the 16th spawning at 30.0 s with 20.0 s left (37.7 s with 20,000-file
  removals). Options (a) to (d) are therefore not needed, and none is taken; the
  deltas stand as written. The question as it stood before the ruling follows,
  kept as the record of what was costed; its measured basis is at the stand-ins
  that step (i) replaced. Its first step is the basis. The cap test is D5's, at
  task 2.1's measured costs and its 10,000-file removal, but task 2.1 measured
  neither LQ-11's per-row `rev-parse --show-toplevel` nor LQ-13's `rev-list`.
  For a 128-row `--all-safe --apply` there: at D14's flat 150 ms per child the
  first removal would spawn at 45.3 s, past the 45 s spawn limit (the 50 s work
  deadline less the 5 s removal floor), so none is made, safely; at the measured
  costs, with those two probes costed at the identity probe's 19.7 ms and the
  full ref listing's 359.7 ms, all 16 removals fit (15 with 20,000-file
  removals), the 16th only while the work-tree probe costs at most about 69 ms
  with the margin and the `rev-list` about 581 ms or less, each with the other
  at its stand-in; and on the mixed basis, the measured costs plus 150 ms for
  each child added since, 11 fit. So the first step is either (i) to measure
  those two probes on task 2.1's protocol, at a load comparable with its runs,
  and rerun the cap test, or (ii) to decide which basis the cap test uses: the
  measured basis, D5's as ratified, with the two probes at those stand-in costs;
  the mixed basis, which prices only those two at 150 ms; or BA's flat 150 ms,
  which would change D5 and fails the case at once, so that an option below has
  to be chosen with it. If the case then passes, no option is needed and the
  deltas stand. If it fails, the options are these, each with its result at 128
  rows on each basis:
  - (a) accept that worst case (not taken):
    - 150 ms: no removal on this run or any re-run, since a re-run builds the
      same plan, so a re-run does not continue there; from 127 rows, one removal
      a run at first; a `--worktree` removal still fits, at 41.85 s;
    - measured: 16 a run;
    - mixed: 11, then 13, then 16 a run;
  - (b) bound the plan-time work-tree probe to the selected targets, at most 16,
    and report the other rows' identity as unverified (not taken):
    - 150 ms: 13 of 16, so (b) alone still fails the cap test and would need (c)
      or (d) as well;
    - measured: 16;
    - mixed: 16;
  - (c) a longer work deadline where `extensions.worktreeConfig` is true, so
    that later removals can still start, the 5 s removal floor kept, which there
    also moves the ratified 60 s invocation deadline,
    `budget.invocation_timeout_seconds` in every plan record (not taken):
    - 150 ms: at least 70.55 s, which moves the invocation deadline to 80.55 s
      and the 64 s run bound to 84.55 s;
    - measured: none needed;
    - mixed: at least 55.0 s, an invocation deadline of 65.0 s and a run bound
      of 69.0 s;
  - (d) the rule's own step, lowering the caps (BA:766-771; not taken):
    - 150 ms: 64 rows and 8 targets, or 32 rows and 16 targets with the row cap
      chosen first, and a report cap of 128;
    - measured: none needed;
    - mixed: 128 rows and 8 targets, or 64 rows and 16 targets with the row cap
      chosen first, and a report cap of 128.

  This draft recommended none of them, and none is taken: the case passes on the
  measured basis, so the deltas stand as written.

- F-1's (b) beside an unread row (from R-310; before Brett Heap, not ruled):
  F-1's (b), 'inspect, then git worktree prune and delete PATH by hand', can
  print in single mode for a ceiling-cut P beside a row whose path could not be
  read; since git worktree prune acts on the whole repository, that prune would
  delete that row's administrative directory. Should (b) carry the same warning
  there?

Ruled on 2026-10-09: a merged worktree whose remote branch was deleted is
`merged-removable`, Brett Heap having ruled that a local ancestry proof outranks
`remote-gone` for worktree rows (D6; `proposal.md` Decisions). The V5 deferral
(D12) and the other departures that PR #11 carried were ratified with its merge
(Brett Heap: "ratify, merge #11 and run the runbook"). Of those this amendment
adds, seven carry his own rulings of 2026-10-21, Q9 B and LQ-10 to LQ-15, each
named in its entry, but the parts of four of them that the lead's rulings added
wait on his ratification of it: the extension of LQ-15's test to
`GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` (R-102 (c) 3), the `commondir` check
of LQ-11's registration (R-125), the branch reflog's non-zero objects among
LQ-13's negatives (R-124 (c), R-127), the drain line's naming of the reasons of
the gates after the cap (R-146) and the three markers that LQ-14's gate gained
(R-126). So do the four departures that the amendment's rounds declared, a
revalidation read or child that the work deadline cuts (D7), push's wider
upstream refusal and branch deletion's message for a branch the main worktree
holds (D18) and the line-feed exception to the revalidation and rescan bounds
(D7, D14), as does the push-child exception (Open Questions above). His word of
2026-10-22, "F-2: yes; F-1: prune-then-delete; O-1: deadline-exceeded", amends
three ratified sentences: a locked row's recovery text (D4, D18), the ceiling's
recovery text (D9, D18) and gate 7's read that the deadline cuts (D10); his
"R-284: yes" of the same day confirms the ceiling's third text, for a `.git` the
rescan cannot read (D9, D18), and his "R-307: yes; R-310: yes" of the same day
(the lead's R-319) confirms the five texts, three next steps and two remedies,
of the prune advice where a row's path could not be read (D18; lane
openRepoProject-3's W87 M-1, the lead's R-307 and R-310), and his "R-320: yes"
of the same day (the lead's R-321) amends two more ratified sentences, the
remedy of `inspect-cap` and the ladder's recommendation for a `stale-worktree`
row, which leave `git worktree prune` out beside a row whose path could not be
read, the cap remedy always (D18; lane openRepoProject-3's W86 NM-1), and his
"R-324: yes" of the same day (the lead's R-343) extends the warnings of all
those texts, and the ceiling's third text, to `git worktree remove` and `git gc`
beside `git worktree prune` (D18; lane openRepoProject-3's W91 MEDIUM-2, W95 and
W80 L-6). Five more amendments of ratified sentences rest on lane rulings and
findings rather than his word, and wait on his ratification of this amendment:
the line-feed exception to the bounds (D7, D14), the next steps of F-7 and F-8
(D18, the Migration Plan), the cap's re-run and the count split (`proposal.md`
Decisions), and the identity probe's line count, which repeats the probe on any
count but two (D6; lane openRepoProject-3's W80 M-3).
