Lane: openRepoProject-2

# Design

## Context

See `proposal.md` for why and what, and the two spec deltas for the
requirements this design builds: `specs/project-overview/spec.md`, twelve
ADDED requirements, and `specs/project-review-safety/spec.md`, one MODIFIED
requirement. The council's noted constraints are `clarifications.md` N1 to
N4, each answered by a decision below (N1 D1, N2 D2, N3 D3, N4 D4). D5 to D11
give the how of the proposal's own decisions, D12 records the reconciliation
with change 1's text, and D13 fixes the test seams and the scenario map.

Citations follow `proposal.md`. `DI:N` is line N of the packet's discovery
document at `da33d92`, and `project:N` the executable at `da33d92`. Change 1,
`add-project-clean-all-safe`, is cited by requirement header under the
proposal's labels: [E] `Repository inspection requires Git 2.36 and shares
one evidence model` (project-command), [L] `Clean classifies preservation and
cleanup actions`, [G] `Clean previews and applies a batch of eligible
worktree removals in one repository` with `Clean bounds its Git work and
reports omitted work`, [R] `Clean resolves its target Git-first`, and [P]
`Clean reports every path exactly or excludes it` (all project-clean).
What this design reads from change 1 is cited, never restated; D12 names the
commit it was reconciled against.

What in `project` and the plan shapes the approach:

- `project` is one Python file on the standard library, plus PyYAML for
  manifests. `read_yaml` (project:37) raises `Refused` for a missing library,
  an `OSError`, a `UnicodeError` or a YAML error; `manifest()` (project:274)
  reads `project.yaml` or `family.yaml` through it. `main()` turns `Refused`
  and `OSError` into exit 2 and an interrupt into `Cancelled.` and 130
  (project:995-1003). At `7a9134b` the code from `manifest()` onward,
  `main()` included, sits 141 lines lower, as the proposal says, while
  `read_yaml` and `probe()` (below) are unmoved; feature 004 re-pins every
  citation against the `main` of its day.
- Every Git child goes through `probe()` (project:60), a `subprocess.run`
  with a fixed 15 s timeout that kills one process, never a group. Feature
  003 replaces it for Git with change 1's bounded runner, a child handle that
  starts a child in its own session, exposes its stdout and stderr, stops its
  group with the 2 s grace and reaps it (proposal, Dependencies; change 1's
  cross-change item X1). The overview drives that handle; it does not fork
  it.
- Feature 003 also brings the shared probes and their incremental byte
  parsers, the ladder as a pure function over evidence (change 1's OQ-28),
  the version check and Git-first resolution. The overview adds discovery,
  the per-candidate collector, the scheduler, the gates and two renderers.
  Feature 004 is created only after feature 003 merges.
- Tests run with `python3 -m unittest discover -s tests -v`; 94 pass at
  `7a9134b`. CI runs Ubuntu and macOS on Python 3.10 and 3.12, so nothing
  may rely on Python 3.11's `process_group` (proposal, Corrections).

## Goals / Non-Goals

**Goals:**

- One main thread drives every Git child, filesystem task, timer and signal
  from one loop, so each 5 s and 60 s bound holds and no child outlives the
  run (D1).
- The JSON of an uncut run is a function of the estate alone, not of
  concurrency or completion order (D6).
- Every suggestion gate is computed from evidence the overview holds, with no
  Git child of its own beyond D3's `core.worktree` read, and one bounded
  reflog read per remaining `merged-removable` row (D5).
- Every string the person reads is fixed here and pinned by a test (D4, D5,
  D10).

**Non-Goals:**

- Changing `project clean`, `status`, `doctor` or `update`: change 1 owns
  them, and this change alters nothing they print.
- A second classifier, resolution order or path escaper: the overview calls
  change 1's.
- Remote, family, bench, container or park evidence (proposal, Out of Scope).
- Bounding a call stuck in the kernel: it is abandoned, as DI:480-485
  allows, and process exit may wait for it.
- A per-repository row cap or configurable limits (OQ-7, OQ-8).

## Decisions

### D1. The control loop, signals and termination (N1)

The overview runs one control loop on the main thread, built on `selectors`.
Registered with it are the stdout and stderr of every running Git child and
the read end of one self-pipe, which the filesystem workers and the signal
handlers write to. Each wait's timeout is the nearest of every running
child's budget end, every pending task's wait end, every terminating child's
grace end and the deadline.

Collection runs as continuations. Each candidate's collector is a generator
that yields requests (start this Git child; run this filesystem task) and is
resumed with their results. The collector boundary of spec requirement 4
wraps every resume: an exception raised inside one generator becomes that
candidate's row error by the collector table (DI:528-537), and only that
generator is dropped. The scheduler (D6) decides which yielded child request
starts and when. A child's stdout feeds its incremental parser as bytes
arrive; a parser that reaches its record bound asks the loop to stop the
child, a deliberate early stop that records nothing (DI:464). Its stderr is
drained throughout and its first 200 characters kept for the error message
(DI:544-545), so no child blocks on a full 64 KiB pipe.

Signals: the handlers for SIGINT, SIGTERM and SIGHUP only record the first
signal received; `signal.set_wakeup_fd` on the self-pipe wakes the loop. The
loop then raises a cancellation derived from `BaseException`, not
`Exception`, so the collector boundary, which catches `Exception` (DI:534),
cannot turn it into an `internal-error` row. Termination runs in one
`finally` around the loop: SIGTERM to every registered process group, up to
2 s, SIGKILL to the rest, a reap within a further 2 s, and abandonment of
whatever remains (P6-1). After a signal no result document is printed,
`Cancelled.` is written to stderr with any `OSError` swallowed (after SIGHUP
the terminal may be gone, and the write fails with EIO), and the exit status
is 128 plus the signal number.

Spawning: each child is started and entered in the in-flight registry while
SIGINT, SIGTERM and SIGHUP are blocked with `signal.pthread_sigmask`, and
they are unblocked only after registration, so no signal can fall between
`Popen` and the registry. `pthread_sigmask` is POSIX-only, as `project`
already is.

Recorded, not designed away: SIGKILL of `project` itself orphans its
read-only children, which then run untimed.

Rejected: one thread per repository (signals still land on the main
thread, and termination and canonical output would need cross-thread
locking); `asyncio` subprocesses (child-watcher behaviour differs between
Python 3.10 and 3.12, and change 1's runner is a synchronous handle); a
`concurrent.futures` pool for filesystem work (its threads are joined at
exit, so an abandoned call would hold exit past the deadline); a handler
that raises an `Exception` subclass (the collector would catch it, N1).

### D2. Listing workers stop once their root is abandoned (N2)

Each root is one task on a daemon thread: canonicalise, `stat` for the device
and inode dedupe, one `os.scandir` pass over the root, and for each entry
directory one `os.scandir` pass for the markers plus the holder `stat`
(DI:138-142). The worker appends each finished entry to the root's result
under a lock and checks the root's cancel flag between entries. When the
root's wait ends, at 5 s or at the deadline, the loop sets the flag,
snapshots the entries read so far, records `probe-timeout` or
`deadline-exceeded` as a scan error with the root `truncated`, and ignores
anything the worker adds after the snapshot. A worker stuck inside one
kernel call stays abandoned (DI:480-485); every other worker stops at its
next entry. Workers never touch the loop's selector or the registry; they
only post their completion to the queue and the self-pipe.

Tests inject a slow `scandir` and assert that no entry is read after the cut
(D13). Rejected: one handoff per filesystem call (too costly, DI:469-470);
letting abandoned workers run on (they compete with the Git phase, N2).

### D3. Naming the main checkout: submodule, bare, gitfile and missing (N3)

[E]'s identity probe and the registry give each repository its `common_dir`
and the registry's first record. The overview follows [R]'s precedence in
every repository, not only in the gitfile layout (the lead's R-2): the
submodule test first, then the bare refusal, then `core.worktree`, then the
candidate toplevel. Change 1's design runs the submodule test inside the
identity probe (its D6, row 3: `rev-parse --path-format=absolute
--show-toplevel --git-common-dir --show-superproject-working-tree`, whose
third line names the superproject), so applying it everywhere adds no child.

1. Submodule: the identity probe of a candidate that reached the repository
   reports a superproject working tree. `repository.root` is null with
   `unsupported-layout` (repair, error; N-6), whose message is "submodule
   checkout, which project clean refuses; review it yourself", and no
   `core.worktree` child runs. The rest is as for an unnamed gitfile
   checkout in case 3: the repository-wide probes run in the candidate, and
   the main worktree row keeps the record's path, its `present` from
   `lstat`, and null status fields and classification. A null root gets no
   clean suggestion and no gate code (P6-2), so the overview never suggests
   what [R] refuses.
2. Bare: the first record is marked `bare`. `repository.root` is null, the
   repository-wide probes run in `common_dir` (DI:385-387), and every
   finding that would suggest a clean command gets `suggested_command: null`
   with `suggestion_gate: target-not-repository-root`, because [R] refuses
   a bare repository.
3. Gitfile: the first record's path equals `common_dir`, as for a
   `--separate-git-dir` repository. In the candidate that reached the
   repository, the overview reads `core.worktree` by one counted and bounded
   child, serial with the repository's other children and counted in
   `probes.estimated` ("1 per Git child needed to name the main checkout",
   spec requirement 3). A relative `core.worktree` is resolved against
   `common_dir` by [E]'s registration rule (relative values resolved,
   realpaths compared; BA:230-232). Where `core.worktree` is unset, as `git
   init --separate-git-dir` leaves it on Git 2.43 (N3), the checkout is the
   toplevel of a candidate whose identity probe reported this `common_dir`
   and whose `.git` file, read by a bounded task, names `common_dir` itself
   and not `common_dir/worktrees/<id>`. When no candidate seen so far
   matches, a later one in canonical order still may, so that repository's
   second phase also waits until every candidate's identity probe has
   completed or failed (D6). The main worktree row then names
   `repository.root` and takes its status probe there, so the checkout's
   dirty state is reported (AE-2's hidden-dirty case); the git-directory
   record is never a probed row. With no checkout named, `repository.root`
   is null with `unsupported-layout` (repair, error; N-6), whose message
   carries "set core.worktree or move the checkout", and the main worktree
   row keeps the record's path, its `present` from `lstat`, and null status
   fields and classification.
4. Missing main worktree: the first record's `lstat`, a bounded task, fails
   with "no such entry" or "not a directory". `repository.root` is null. The
   ref listing and merged set run in the candidate, where the registry
   already ran (DI:388-390). The manifest is read at the row's `path`, which
   is the candidate while the root is null (DI:748): DI:583-585 reads it at
   `repository.root` only so that a suggestion and the overview agree, and
   here no suggestion is given. The main worktree row keeps the ladder's
   `stale-worktree` classification, but its finding is
   `main-worktree-missing` (repair, warning) in place of the `stale-worktree`
   housekeeping finding, because `git worktree prune` never removes a main
   worktree and no read-only `project clean` can be suggested; its message
   carries "restore or prune the main worktree by hand".
5. Ordinary: the first record is a worktree path, the main worktree, and
   `repository.root` names it whichever candidate reached the repository
   first. The identity probe's toplevel names it only when that candidate
   is the main worktree itself; when that candidate is a linked worktree,
   `repository.root` is the canonical path of the first record, never the
   linked worktree's toplevel (the lead's R-14).

Rejected: parsing `<common_dir>/config` for `core.worktree` (includes and
conditional includes could make it disagree with [R]); the submodule test as
a child of its own (the identity probe already carries it); status-probing
the git-directory record (Git refuses, "this operation must be run in a work
tree", exit 128, N3, turning an ordinary layout into `inspection-error`).

### D4. The default-branch finding set (N4)

On a worktree row that [L] classifies `protected-default`, the overview
computes, from the row's `dirty`, `upstream`, upstream track state, `ahead`
and `behind` and from the ref listing's remote-copy flag (D9), with no new
probe:

1. `dirty` (preserve, warning) when `dirty` is true; then
2. at most one, tested in this order: `unpublished` when no upstream is
   configured and the remote-copy flag is set; `remote-gone` when the track
   state is `gone`; `diverged` when `ahead` and `behind` are both above 0;
   `unpushed` when `ahead` is above 0; `remote-ahead` (informational, info)
   when `behind` is above 0. All but `remote-ahead` are preserve warnings.

Each has the row as its `checkout` and the attention table's evidence source
(`worktree-status` for `dirty`, `local-refs` for the others), and carries
`suggested_command: null` and `suggestion_gate: null`; none sets the row's
`suggested_command` (OQ-20). Findings are emitted in DI:755's order, by
checkout path then code, so the computation order never shows in output.
Ignored files on that checkout raise nothing.

Fixed messages, ASCII, pinned by tests:

| Code | Message |
| --- | --- |
| `dirty` | Uncommitted work on the merge-target branch; preserve it before updates. |
| `unpublished` | merge-target branch has no upstream; local commits are unverified |
| `remote-gone` | merge-target branch's upstream is gone; local commits are unverified |
| `diverged` | merge-target branch and its upstream have diverged; reconcile through the normal Git workflow. |
| `unpushed` | merge-target branch is ahead of its upstream; push through the repository's normal process. |
| `remote-ahead` | merge-target branch is behind its upstream as of the last fetch. |

The `unpublished` text is the proposal's. The `dirty` text follows doctor's
warning, which DI:626-630 names. The other three replace the ladder's
worktree advice, which speaks of cleanup and removal, wrong for a checkout
that is never a removal target.

A checkout on the merge-target branch whose status probe failed, timed out or
was cut by the deadline is `inspection-error`, set directly as [L] defines
(change 1's R1; the lead's D-A), with that code's repair error and none of
the six findings.

N-1 narrows N4's `unpublished` case. N4 has it fire on "no upstream" alone,
which would warn on every fresh repository with no remote; it now also needs
the remote-copy flag, and a repository with no remote copy of its merge target
is ordinary work.

Rejected: `acf0133`'s first-match chain (council AE-1, V1).

### D5. Suggestion gates from the overview's own evidence

Per repository, after every row is classified or left null, one pass
computes:

- the per-worktree gates on each `merged-removable` row, in [G]'s order and
  from evidence already held: `main-worktree` (the first registry record),
  `unsupported-path-bytes` (`path_valid_utf8` false),
  `registration-mismatch` (the two-way check failed) and `locked-worktree`
  (the registry's `locked`). The first failure replaces the housekeeping
  finding with its own, and the classification stays (DI:661-673);
- `unstarted-branch` and `reflog-unavailable` from the reflog, mirroring [G]'s
  gate at `4f2162b` (change 1's D10; the lead's amended V2, R-1, R-12 and R-15;
  P6-5 for the finding): for each remaining `merged-removable` row, one bounded
  filesystem task (D8) reads `logs/refs/heads/<branch>` under `common_dir`,
  each `/` of the branch name a directory level, at most 64 KiB, the bound [G]
  states for the same read. Each line is `<old> <new> <identity> <time>
  <zone>`, then a tab and the message only when the command wrote one:
  `git update-ref` without `-m` writes neither, so such a line ends after
  the time zone and is still an anchor by its all-zeros old object. The
  anchor is the last surviving entry whose
  old object is all zeros, a creation written by any command (`worktree add
  -b`, `branch` and `checkout -b`, and also `fetch <remote> <ref>:<branch>`,
  `update-ref` and `push .`), or whose message begins `branch: Created from`
  or `branch: Reset to`, the latter written by `worktree add -B`, `branch -f`
  and `checkout -B` on an existing branch; the two are independent
  alternatives, and the lead's R-15 added the all-zeros one. A movement is
  an entry after the anchor, or any entry when no anchor survives, whose old
  and new objects are non-zero and differ: an entry whose old object is all
  zeros is never a movement, nor is a rename's entry, old and new objects
  equal. The tests run
  in this order: a last entry whose new object differs from the head gives
  `reflog-unavailable`, because the reflog then does not describe the branch;
  otherwise a movement passes the gate, whatever the head, the ancestry
  already established deciding that the branch is merged; an anchor with no
  movement after it, its new object equal to the head, gives
  `unstarted-branch`, whether or not that head equals `merge_target.sha`; and
  no anchor and no movement, or any other combination, gives
  `reflog-unavailable`. One outcome rule governs the read: `ENOENT` or
  `ENOTDIR`, a file of 0 bytes, the 64 KiB bound reached, or surviving entries
  that cannot decide give `reflog-unavailable`; any other `OSError` records
  `os-error` on the row and makes it `inspection-error`, like any failed row
  probe; and a read not finished inside its wait records `probe-timeout`, or
  `deadline-exceeded` where the deadline was the limit, and leaves the row
  unprobed for the gate, as for every other filesystem read. Either of the
  last two makes the batch's plan incomplete, so `inspection-incomplete` then
  withholds `--all-safe`. A branch fast-forward merged into the target sits
  at its tip with a commit after its anchor, and passes; a branch with
  commits of its own that `worktree add -B` resets to the target's tip
  anchors at that entry and is `unstarted-branch` until it gains a commit.
  Either code keeps the finding and gives the read-only suggestion with that
  `suggestion_gate`. Only the index gates `contains-submodule` and
  `hidden-local-state` stay residual exclusions the batch applies;
- the repository gates, computed from the overview's rows as [G] computes
  its plan's refusals: `inspection-incomplete` when any row is
  `inspection-error` (a failed or timed-out status probe, an unreadable
  path, a registration mismatch, a reflog read failing with an `OSError`)
  or is unprobed for the reflog gate because its read did not finish;
  `inspect-cap` when the registered rows,
  `present: false` included, exceed `limits.batch_row_cap`; and `scan-limit`
  or `deadline-exceeded` when the overview's own worktree-row cap or
  deadline left any row with `classification: null`. Each withholds the
  `--all-safe` form for every row of the repository and leaves the read-only
  form. None predicts a plan cut by the batch's own deadline (proposal,
  Dependencies);
- the report cap: when the registered rows exceed `limits.report_row_cap`,
  every read-only suggestion of the repository is limited by `inspect-cap`,
  since that report would be incomplete;
- `target-cap`: when more `merged-removable` findings still carry
  `--all-safe` than `limits.targets`, each keeps it, limited by
  `target-cap`. Change 1's council V5 has the batch select up to the limit in
  canonical order and defer the rest as `deferred-target-cap`, apply
  allowed, re-runs draining. The overview's count can exceed what the batch
  would select, since the batch's index gates may exclude some rows; the
  message is advice either way;
- the root gates: a null root from a bare repository withholds every clean
  suggestion with `target-not-repository-root`; a root or `common_dir` that
  is not valid UTF-8 withholds every clean suggestion with
  `unsupported-path-bytes` and adds that repository-level finding
  (DI:862-864), since [P] refuses either (the lead's R-3). A root left null
  by `unsupported-layout`, a submodule checkout's included, or by
  `main-worktree-missing` carries no gate code (P6-2).

Each finding's `suggestion_gate` is the first code that changed its own
suggestion, in the order of spec requirement 7's table:
`target-not-repository-root`, `unsupported-path-bytes`,
`inspection-incomplete`, `inspect-cap`, `scan-limit`, `deadline-exceeded`,
`unstarted-branch`, `reflog-unavailable`, `target-cap`. A code that did not
change a finding's suggestion is not recorded on it: a `dirty` finding in an
`inspection-incomplete` repository keeps its read-only suggestion and a null
gate. `suggestion_gate_rows` is the repository's registered row count when the
code is `inspect-cap`, else null; with `limits` it tells the two `inspect-cap`
bands apart.

The remedy texts are spec requirement 7's. N is the row count and M is read
from `limits` when the message is built, so a cap that change 1's
measurement moves carries over (N-3). A gated finding's `message` is its own
text, then `; `, then the remedy, within the 200-character limit; when both
do not fit, the finding's own text is shortened with `...` and the remedy
kept whole. The `--root <repository parent>` remedy names the parent
directory of `repository.root`, printed by [P]'s rules.

Rejected: a row-level gate field (rows and findings both carry
`suggested_command` in DI:756 and DI:819, and one row can hold findings gated
by different codes); predicting the batch's index exclusions, which need
probes the overview does not run (DI:688-702).

### D6. Scheduling: the two conditions and the identity barrier

[E]'s probes run through change 1's runner handle; the scheduler owns four
slots and one rule per repository.

Phase 1 dispatches candidates in canonical order. A candidate's identity
probe may start whenever a slot is free, ahead of earlier candidates'
completions (speculative dispatch; identity probes take no lock and may
overlap, DI:436-438). On completion the memo is consulted by the
`(dev, ino)` of `common_dir`: a hit merges the candidate into that
repository, a miss creates the repository, whose repository-wide probes
(registry, ref listing, merged set, and D3's tests for a gitfile layout) then
run one at a time. No two children with one known `common_dir` run at once.

A repository's rank is the canonical position of the first candidate that
reached it, and it is final only when every candidate earlier in canonical
order has completed or failed its identity probe: until then an earlier
candidate could still reach a new repository that ranks ahead. That is the
first condition, the identity barrier. The second is DI:446-448's: every
repository earlier in canonical order has finished its first phase, so the
number of worktree rows ranked ahead is known. Only with both may a
repository's second phase start and the 512-row cap select its rows; with
either missing, a run in which that cap binds would select rows by
completion order (N-2). D3's unnamed gitfile layout adds a third wait for
that repository alone.

Ready work starts lowest rank first, a throughput choice and not part of the
contract. Output is rendered after collection in canonical order: rows by
path bytes; worktrees main first, then by path bytes; findings by checkout
path, then code; row errors in each candidate's own step order, which is
serial and so fixed; and scan errors in canonical collection order, not
wall-clock order: root errors by root order, then the candidate cap, then
deadline and worktree-row errors by rank. With that, an uncut run's JSON at
probe concurrency 1 and 4 differs only in timestamps and
`budget.probe_concurrency` (spec requirement 3). A cut run reports each cut
unit with `omitted` and DI:165-169's exactness, and what it selected may
depend on timing (proposal, Decisions, "Determinism scoped").

Rejected: DI:446-448's rank condition alone, which assumes ranks fixed at
dispatch and fails under speculative dispatch; one global barrier after all
identity probes, deterministic but holding every repository's second phase
behind the slowest identity probe.

### D7. Identity grouping and the canonical-first spelling

Rows are keyed by `repository` and memoized by the no-follow `lstat` of
`common_dir` (DI:232-236). A memo hit merges the candidate into the existing
row, which keeps the first candidate's rank. The row's `path` is
`repository.root`, or the candidate when that is null (DI:748). Its `kind`
is the kind of the candidate whose path equals that `path` when there is
one, else that of the canonically first candidate that reached the
repository; its `name` is the manifest name at that `path`, else its
directory name.

Where a bind mount or a second spelling gives two paths for one device and
inode, the dedupe keeps the canonically first spelling (smallest bytes) for
roots and candidates. Where the canonically first candidate that reached the
repository is a spelling of the main worktree directory itself,
`repository.root` comes from that candidate's identity probe, so a
suggestion names one stable path; where it is a linked worktree,
`repository.root` is the canonical path of the registry's first record (D3,
item 5), never that worktree's toplevel. Independent clones have distinct
`common_dir` identities and stay apart (DI:248-250), and a family holder is
one row that
claims no member (DI:278-290).

Rejected: keying by the root string or by name (DI:80-81).

### D8. Bounded filesystem tasks and the manifest bound

Every filesystem call runs in a daemon-thread task that posts back through
the queue and the self-pipe (D1), waited for with `min(5 s, deadline -
now)`:

- one task per root: canonicalisation, the dedupe `stat`, the listing and
  the marker checks (D2);
- one task per manifest read, through the shared manifest reader, so that name,
  kind and `tracking_branch` follow [R] exactly. The reader applies [E]'s
  manifest cap as change 1's design reads it: a manifest whose `st_size`, taken
  from the opened file before the read, exceeds 1 MiB is `manifest-invalid`
  without being read, and the read itself never exceeds 1 MiB (the lead's R-4);
- one task per worktree row: `lstat` of the path and reads of its `.git` file
  and the matching `gitdir` file (DI:392-394); the missing-main `lstat` and
  D3's `.git` read take the same shape;
- one task per reflog read of D5's gates, `logs/refs/heads/<branch>` under
  `common_dir`, at most 64 KiB, under D5's one outcome rule: a missing
  (`ENOENT`, `ENOTDIR`), empty or bound-reaching file is
  `reflog-unavailable` for the gate, any other `OSError` the row's
  `os-error` and `inspection-error`, and a missed wait leaves the row
  unprobed for the gate, recorded as below;
- one task at start for the realpath of the working directory, which
  `current` needs.

A task that misses its wait records `probe-timeout`, or `deadline-exceeded`
when the deadline was the smaller limit, on its root or row, and every field
it would have established stays null. No filesystem call runs on the main
thread, so a hung mount never blocks the loop (spec requirement 11).
Abandoned workers are bounded by the number of tasks started (at most 32
roots, 128 manifests, 512 rows, 512 reflog reads and a handful more), not by
time.

Rejected: a size check by path before opening (a race).

### D9. The ref listing's remote-copy flag (N-1)

The ref listing (DI:344-356, format DI:366-368) is parsed as its bytes
arrive, record by record. `for-each-ref` sorts by refname, so every
`refs/heads/` record arrives before any `refs/remotes/` record, and by then
the parser knows every head and the upstream each names. Of the remote
records it keeps only those upstreams and `refs/remotes/origin/HEAD` with its
`%(symref)`.

For N-1 it also keeps one flag per merge-target candidate name known before
the listing starts: the manifest's `tracking_branch` less any `origin/`
prefix (the manifest is read before the repository-wide probes,
DI:519-521), `main` and `master`. A flag is set when a record
`refs/remotes/<remote>/<name>` streams by for that name, with at least one
path component as `<remote>`. When the merge target comes from
`origin/HEAD`, its remote copy is the symref's own target, listed by
construction. After resolution the row's flag is that of the resolved name.
No probe is added, and memory stays bounded by the heads.

A remote whose name contains `/` can make the suffix match a branch of
another remote (a `refs/remotes/origin/feature/main` read as a copy of
`main`). The flag then reads set and the result is an `unpublished` warning,
never a silent pass, which is the direction in which the overview errs
("Unknown is never healthy").

Rejected: a `git remote` child to list remote names, a counted child in
every repository for a rare ambiguity; keeping every remote ref, unbounded on
a large-ref repository.

### D10. The human report and the withheld or limited rule

Layout on stdout, in DI:83-96's shape, pinned by tests:

- a header line per shown row: the name, two spaces, the absolute path;
- per shown finding: two spaces, the category padded to 14 columns, then
  `code: message`; for a worktree's finding, the worktree path on the next
  line, indented to the message column. Row errors show the same way under
  the repair category;
- one `next` line when the row has a suggested command or a gate decided it:
  two spaces, `next` padded to 14 columns, the command with POSIX shell
  quoting or in the `$'...'` form for a path [P] marks, or `none` when there
  is no command, then two spaces and `(withheld: <remedy>)` or
  `(limited: <remedy>)`;
- after the rows, one `Incomplete: <message> (<code>).` line per scan error,
  in the JSON's order;
- always the summary line, `N projects; E errors; repair a, preserve b,
  housekeeping c, informational d. Findings reflect local refs as of the
  last fetch.`, which under `--attention` with no row shown begins
  `Nothing needs attention: `;
- when every root is `absent`, the line `No projects directory found; pass
  --root D or set PROJECTS_DIR.` before the summary.

The `next` line names the gate that decided the row's own suggested command:
the first code, in D5's order, among the findings whose suggestion fed the
row's command or would have. It reads `withheld` for
`target-not-repository-root`, `unsupported-path-bytes`,
`inspection-incomplete`, `inspect-cap` over the batch's row cap, `scan-limit`,
`deadline-exceeded`, `unstarted-branch` and `reflog-unavailable`, where no
`--all-safe` form or no suggestion at all was given; and `limited` for
`target-cap`, and for `inspect-cap` over the report's row cap on the read-only
command (P6-3). A repository over both caps shows the batch remedy as withheld,
and its read-only findings carry the report remedy in their own messages.

`Scanning N roots...` goes to stderr once, after the version check and before
listing, only when stderr is a terminal; stdout is identical either way.
Every human write to stderr swallows `OSError`, as after SIGHUP.

Rejected: a gate line per finding (noise at 17 eligible rows).

### D11. The envelope's `limits` keys and path flags

`limits` carries DI:729's seven keys plus `batch_row_cap`, `report_row_cap` and
`targets` (P6-4; the last under the name a clean plan's `limits` gives the
same constant, as the lead's R-14 rules), read at run time from the shared
constants that [G]
defines in the same file (the row caps of the `all-safe` and `report` modes,
and the per-run target limit), never from literals of the overview's own and
never from a clean plan, whose `limits.worktree_rows` holds only its own mode's
cap (the lead's R-7). The overview enforces none of the three; it reports them
so a consumer can read M and tell the `inspect-cap` bands apart with
`suggestion_gate_rows`. New keys are additive within `schema_version: 1`
(DI:834-837).

Every serialized path carries its own validity flag (the lead's R-9, on
Codex's finding on PR #12). DI:724-819 flags only the root object's, the
project row's and the worktree row's `path`, so a `\xHH` in an
`ignored_samples` string, a finding's `checkout.path` or
`repository.common_dir` could not be told from a valid path holding those
four characters. Now `path_valid_utf8` sits beside each `path` (the root
object, project row, worktree row, finding `checkout` and error object) and
speaks for that path alone; `repository` carries `root_valid_utf8` and
`common_dir_valid_utf8`, null only beside a null path and false beside the
repository's `unsupported-path-bytes` finding (D5); and each
`ignored_samples` entry is a `{path, path_valid_utf8}` object, its `path`
relative to its worktree, the shape change 1 adopts for its own JSON. A
root object's `entries` is a count and needs no flag, and a suggestion's
argv never holds a path that is not valid UTF-8 (D5's root gates).

Escaping follows [P] as the lead's R-8 generalises it: every code point of
Unicode general category Cc, Cf, Zl or Zp, as the running interpreter's
`unicodedata.category` reports it, is escaped in JSON and puts its path in the
`$'...'` form in human output, written `\uXXXX`, or `\UXXXXXXXX` above U+FFFF
for the tag characters U+E0020 to U+E007F; [P]'s enumerated characters are
examples, and U+200B, U+FEFF and U+00AD are caught as well.

Rejected: a separate `batch_limits` object (P6-4 places the keys in
`limits`); M in message text only (N-3 asks the JSON to carry the values);
one flag per row for every path in it (DI:748's meaning), which cannot say
which path is the invalid one.

### D12. Reconciliation with add-project-clean-all-safe

Task 2.2 re-read every item this section listed, [E]'s evidence model, budgets,
manifest cap and termination rule, [L]'s ladder and its merged `remote-gone`
text, [G]'s gates, caps and refusals, [R]'s resolution order and [P]'s path
rules, against change 1's spec deltas and design at `0b3c33d`, and applied the
lead's amended V2 and R-1 to R-9 to this change's deltas, D3, D5, D8, D11 and
D13 (commit `996a181`). R-12 (the reflog anchor, its one outcome rule and
the remedy texts), R-13 (b) and R-14 then landed at `fa9f0be`, against
change 1 at `d6aaa9a`, in the deltas, Context, D3, D5, D7, D8, D11, D13 and
Risks, and were re-read against change 1 at `4f2162b` at `ef288fe`, which
applied R-16 (the `inspection-incomplete` remedy fitted to unprobed rows).
R-18 landed at `fd4b05a` and `568c477`. The current reconciliation is
against change 1 at `7e2589f`; R-19 changed only change 1's report band and
ruling records, nothing the overview reads. [G]'s reflog gate and its two
remedies moved and are mirrored, and change 1 carries R-15's all-zeros anchor
and its `reflog-unavailable` remedy, as this change's text states them; its
report-mode text (`selected: null` above 128 rows, R-15; R-17 added only what
`excluded` and `plan_digest` hold in that band) changes nothing the overview
reads; [E]'s new sentence on where repository-wide probes run when `root` is
null (R-13 (a)) agrees with requirement 2 and D3; every other item is
confirmed. The 64 s run bound agrees (D13). No item stays open.

### D13. Test seams, fixtures and the scenario map

- Every scenario runs in human and `--json` form against temporary fixtures,
  with a scratch `HOME`, `PROJECTS_DIR` set or unset explicitly, and the
  zero-mutation snapshot of DI:1177-1183 taken before and after.
- A counting `git` wrapper first on `PATH` records each child's argv, `-C`
  directory, process group and times, can hold a chosen argv, and asserts
  that no argv fetches, pulls, pushes or reaches a remote. It serves the
  probe-count, concurrency, hold, deadline and signal scenarios.
- In-process tests set the scheduler's concurrency constant to 1 or 4 and
  patch the filesystem task functions to inject a slow `scandir`, `lstat` or
  manifest read where no FUSE mount can be made. A FUSE fixture runs only
  where FUSE is present; otherwise that case is skipped with its reason.
- Network: in-process runs install an audit hook failing `socket.connect`.
- Signals: a subprocess run with one held child and one large-output child at
  concurrency 4, then SIGTERM or SIGHUP; the test asserts the exit status, an
  empty stdout, and `os.killpg(pgid, 0)` raising `ProcessLookupError` for
  every group the wrapper recorded (N1).
- Non-UTF-8 path scenarios run on Linux only and are skipped on macOS with
  that reason; the `$'...'` rendering is asserted as a string, never by a
  shell round trip on macOS's bash 3.2.
- The deadline scenario patches the 60 s deadline and the 5 s budget down
  in-process, keeping their ratio, so the suite stays fast; the full-length
  run belongs to task 2.1's measurement.
- Fixture rewrite: change 1 pins `-c core.fsmonitor=false` and
  `-c core.untrackedCache=false` on every status probe ([E]), so the
  packet's fixtures that hold `git status` with a `core.fsmonitor` hook
  (DI:1233-1237, the probe timeout; DI:1249-1254, bounded concurrency) hold
  nothing. Feature 004 rewrites them to hold the status probe with the
  counting `git` wrapper above, which sleeps before running the real `git`
  for a `status` argv and passes every other argv through unchanged.
- Reflog fixtures: an unstarted branch (`worktree add -b`, then `push -u`),
  a branch given one commit and fast-forward merged into the target, a
  branch renamed with `git branch -m`, a merged branch reset to the target's
  tip by `worktree add -B`, a branch created by `git fetch origin feat:f1`
  at the target's tip and given an upstream by `git branch -u origin/feat f1`,
  which writes no reflog entry, a deleted reflog file and an empty one, one
  expired to its rename entry alone, one whose ref was rewritten without a
  reflog entry, and one unreadable for a permission error; none needs a Git
  child to read.

Scenario map, by the proposal's requirement numbers: the packet's MVP
scenarios (DI:1185-1446) are covered as written except where noted, and the
added ones come from the council, the lead's rulings or this design.

| Requirement | Packet scenarios | Added scenarios |
| --- | --- | --- |
| 1 discovery | clones and aliases; unreadable candidate; family holder | every root absent |
| 2 identity | one probe set; external present, missing, unreadable | separate git directory; submodule; deleted main worktree; bare |
| 3 bounds | candidate cap, twice; root and row caps; probe timeout; hung call; deadline; concurrency; ignored files; status configuration | JSON independent of concurrency; hung root; hung repository root; manifest over the bound |
| 4 isolation | one helper failure | no YAML library |
| 5 classifier | the six merge targets; every protected classifier | none |
| 6 attention | attention filter | merged worktree with its upstream deleted |
| 7 suggestions | gated merged worktrees; canonical identity | 17 eligible rows; two inspect-cap bands; unprobed row; unstarted branch, with the reset, fetch-created and fast-forward-merged branches; reflog cannot decide |
| 8 JSON | control characters; non-UTF-8 path | non-UTF-8 common directory; argument error; envelope fields; internal error |
| 9 read-only | local and read-only | none |
| 10 default branch | none | pushed without `-u`; no remote; dirty and ahead; failed probe |
| 11 exits | Git version refusal | Git unavailable; SIGTERM or SIGHUP; SIGINT |
| 12 human report | none | nothing needs attention; gated suggestion; scanning notice |

The probe-timeout and bounded-concurrency scenarios use the fixture rewrite
above. The invocation-deadline scenario allows 64 s where DI:1248 allows
62 s: the 60 s deadline, then up to 2 s from SIGTERM to SIGKILL and a reap
wait of up to 2 s before abandonment (D1; [E]'s termination rule, P6-1),
where `clean`'s run bound is 50 + 10 + 4. The merge-target scenarios compare
with `project clean <root> --json` at the same commit, not at `a040790`.

## Risks / Trade-offs

- [A call stuck in the kernel holds process exit] -> Its worker is
  abandoned; exit may wait for it (DI:480-485), and the README says so.
- [SIGKILL of `project` orphans read-only children] -> Recorded (D1).
- [The caps do not fit the deadline on a real estate] -> They are marked
  provisional, and task 2.1 measures warm and cold on a Linux filesystem path
  and lowers them before the handoff; a run that hits them is incomplete,
  never silently short.
- [A Windows drive mounted into WSL2 makes every listing slow] -> Measured
  as a degraded case only; the README says such roots can truncate on every
  run.
- [Change 1's final text moves a gate, code, cap or probe] -> D12 and task
  2.2; the overview copies no number (N-3, D11).
- [`target-cap` disagrees with the batch, which sees the index gates the
  overview does not] -> The suggestion is advice; `project clean` recomputes
  and shows its own plan.
- [Repositories without file reflogs (the reftable backend,
  `core.logAllRefUpdates=false`) give every merged row `reflog-unavailable`,
  and so does a branch with no surviving decisive reflog entry, because it
  saw no activity for `gc.reflogExpire` (90 days by default)] -> Fails
  closed with the read-only suggestion and its remedy, as change 1's batch
  excludes the same rows.
- [A reflog over 64 KiB (about 300 entries) fails closed as
  `reflog-unavailable` even when it records movement, because the head test
  runs first and the bound ends the read] -> Fails closed with the read-only
  suggestion; the remedy calls the reflog undecidable, as change 1's batch
  excludes the same rows.
- [A branch created from a remote branch that already had commits, then
  merged elsewhere, reads as unstarted, because nothing moved it here since
  its anchor] -> Fails closed as `unstarted-branch` with the read-only
  suggestion; the remedy says that no commit was made on the branch here
  since it was created, as change 1's batch excludes the same row.
- [The remote-copy flag reads set for a remote whose name contains `/`] ->
  It errs toward an `unpublished` warning (D9).
- [A gitfile repository whose checkout lies outside every root reads
  `unsupported-layout`, an error] -> Ruled (N-6): an unnamed checkout is
  unknown; the message names the remedy, and adding the checkout's parent
  with `--root` names it.
- [Squash-merging repositories yield few `merged-removable` rows] -> Open
  Questions.

## Migration Plan

Nothing migrates for users: `project overview` is new, and no other
subcommand's output, flags or exits change through this change.

1. Change 1 is ratified first, then this change by Brett Heap's word on PR
   #12 (task 1.6).
2. Task 2.2 reconciles this change's deltas with change 1's text after its
   phase 6 (D12), and task 2.1 records the OQ-4 measurement; both precede
   the handoff.
3. Feature 003 (change 1) merges. `/speckit.specify` then creates exactly
   one feature, `004-project-overview`, from the `main` of that day, and its
   plan re-pins every `project:N` citation; feature 004 merges `main` into
   its branch and never rebases.
4. Feature 004 adds the `overview` subcommand, the README section that the
   proposal's Impact lists, and D13's tests, at least one per scenario.
5. This change archives after change 1, once feature 004 has merged.

Rollback: revert feature 004's merge; no data, configuration or other
subcommand depends on the overview.

## Open Questions

Neither changes this change's specs, the approach or the task list: each
would change change 1's ladder or gates, which the overview cites by name.

- `remote-gone` versus local ancestry. A merged worktree whose upstream was
  deleted classifies `remote-gone`, so under head-branch auto-delete with
  `fetch.prune` the overview never suggests `--all-safe` for the commonest
  merged case. Lane openRepoProject-3 recommends that a local ancestry proof
  outrank `remote-gone` for worktree rows; until Brett Heap rules, the
  overview follows the ladder, its message is change 1's merged
  `remote-gone` recommendation where the merged set shows the ancestry, and
  its suggestion only reviews.
- Squash merges. A squash merge never puts the branch tip into the target's
  ancestry, so in squash-merging repositories few worktrees are
  `merged-removable` and housekeeping findings are rare. Change 1 recommends
  a local patch-equivalence proof as a follow-on change, which the overview
  would inherit through [L].
