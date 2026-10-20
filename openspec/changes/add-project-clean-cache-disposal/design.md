Lane: openRepoProject-5

# Design

## Context

See `proposal.md` for why and what, and the deltas under `specs/` for the
requirements. Citations follow the proposal's key: the packet at `da33d92`
(`BA`, `SY`, `OV`, `HO`), change 1 (`CAS`, `CAS/pc`, `CAS/rs`, `CAS/cmd`) and
change 2 (`APO`, `APO/ov`) at `961c405`, draft PR #19 at `c462d87` (`PR19/pc`,
`PR19/rs`), and `project:N` at `961c405`; main is now `e9d6711`, with the same
`openspec/`, `ideation/` and `project` (L-15). The lane's rulings are L-1 to
L-17 and B-1 to B-42, and A-9, A-23 and A-24 for #23; this change's own
decisions are CD-1 to CD-18 in `proposal.md`, and the alignment review's
findings (SA-n, QA-n, G1 to G5) are resolved in its table. The council (P-n,
S-n and AE-n) read `9ebe9f0`; its VALID verdicts, ruled as B-16 to B-24, are
applied below and in the deltas, and its one NOTED item, S-4, is in
`clarifications.md`, which D4, D14, the Migration Plan and `tasks.md` 2.3 and
3.1 answer. Codex's two findings on `90d18ee` and lane openRepoProject-3's
re-read of `e906c2f`, ruled as B-25 to B-27, and the lead's B-28 are applied in
round B3 (proposal, "Re-read and Codex Findings (round B3)"). Lane
openRepoProject-4's re-align step and wording of 2026-10-20, lane 3's delta
read of `cf57956` and Codex's two findings on `cf57956`, ruled as B-29 to B-33,
are applied in round B4 (proposal, "Re-read and Codex Findings (round B4)").
Codex's two findings on `e1049b2`, ruled as B-34 and B-37, and the lead's B-35
and B-36 (D4's account of #26 at `9ff8202`; `tasks.md` 2.2 ticked again on lane
4's byte check) are applied in round B5 (proposal, "Re-read and Codex Findings
(round B5)"). Lane 3's folded read of `cf57956..fffc194` and Codex's finding on
`fffc194`, ruled as B-38 and B-39, the last two LOWs of lane 3's read, ruled as
B-40, the lead's B-41 on this round's own signal sentence and B-42 on D4's
account of #26 are applied in round B6 (proposal, "Re-read and Codex Findings
(round B6)").

How the packet's contract and the rulings map to the decisions below:

| Source | What it asks | Decision |
| --- | --- | --- |
| `BA:1318-1322`, B-8 | a stage of its own before the worktree removal, inside the seam and its deadline, mutations in `operations.estimated`, bounds in `limits` | D1, D4, D12 |
| `BA:1324-1325`, B-1 | a symlink candidate or ancestor is ineligible and preserved | D2, D7 |
| `BA:1326-1330` | descriptor-relative, no-follow operations; the opened directory checked against the planned device and inode; fail closed where the platform cannot; no check-then-recursive-delete | D5, D7, D9 |
| `BA:1332-1336`, B-6 | each path reported; a partial phase recorded, rescanned and retried; no worktree mutation after a failed preflight | D7, D8 |
| `BA:1336-1337`, B-3 | hard limits on entries and bytes, in the plan estimate | D4 |
| `BA:1632-1634` | symlink candidates and ancestor swaps rejected, external targets intact, each path reported after a partial failure, no broad recursive deletion | D7, D8, D14 |
| `BA:1640-1643` | stop on the first failure | D8 (CD-1) |
| B-2 | an enumeration of its own, bounded, in `probes` and the fit | D3, D4 |
| B-4 | identities of every cache directory and ancestor; cache paths in `plan_digest` | D5 |
| B-5, B-9 | the rung reads blocking paths; disposable and blocking counts, `null` when unknown | D6, D11 |
| B-7 | the residual window stated | D13 |
| L-4, L-10, B-13 | values only in sub-records, present only where this change acts | D11 |
| CD-4 | revalidating a cache target | D10 |
| B-10, L-11 | the digest, the narrow guarantee and the deletion exception in MODIFIED blocks | D5, D8, D13 |
| B-12 | the sample test before any enumeration, and the stall stated | D2, D4 |
| B-14, B-22 | the overview's equality clause excepts the cache-proven case, and the carried "Every protected classifier" scenarios name a non-cache ignored file | D6, D14 |
| L-12, B-15 | CI on Linux only; macOS not verified by CI | D9, D14 |
| B-16 | the stage's removals waited for as change 1 waits for its removal child; the hand-off of the first removal as the commit point | D1, D4, D8, D12 |
| B-17 | the second check immediately before that hand-off; a target whose stage ended `disposed` and whose removal was not spawned | D1, D8, D11, D12 |
| B-18 | the partial-stage rescan by the descriptor chain, under the reserve | D8, D12 |
| B-19 | the residual window widened by the cache stage, stated and bounded | D13 |
| B-20 | a cache directory the user cannot change kept at plan time | D2, D3, D9, D11 |
| B-21 | the stall and deadline lines name their cause | D4, D11 |
| B-23 | `.pytest_cache` before Brett Heap; the measured benefit | Non-Goals, Open Questions |
| B-24 | `candidate_block` names what really keeps a cache-only row | D2, D11 |
| S-4 (NOTED) | measured dispatch cost; the gates of task 2.3 and 3.1 | `clarifications.md`, D4, D14, Migration Plan |
| B-25 | the plan-time walk bounded at 16 x 512 = 8,192 entries, the rows the invocation's totals reject included; the fit and every figure that depends on the walk restated | D4, D13 |
| B-26 | the preflight keeps the run's byte total of the bytes it measures and refuses a target that would take it past 1 GiB | D1, D4, D5, D7, D8 |
| B-27 | lane 3's re-read of `e906c2f`: the ceiling in the exit table, the `not-attempted` stage of a `disposed` stage, the signal paragraph, one relative clause, the citations of `tasks.md` 2.2 | D8 |
| B-28 | "because clean's cache enumeration proved", as the committed `project-overview` delta reads | D6 |
| B-29 | lane openRepoProject-4's re-align step: before `/opsx:archive`, the `project-overview` block re-read against main's text of its requirement and re-copied, keeping any amendment | Migration Plan |
| B-30 | the overview's SHALL NOT holds for the same working directory and refs, in lane 4's words | D6 |
| B-31 | lane 3's delta read of `cf57956`: the removal ceiling beside a signal and the deadline in the stage's exit sentence; the 16th target of D4's case listing no cache | D4, D8 |
| B-32 | the stall test on persistent reasons, never on `blocking` alone; a per-worktree cap told from the totals by the row's counts | D4, D11 |
| B-33 | every recorded directory counts toward the per-worktree cap of 512; the walk opens each recorded directory once, and the stage one chain per directory with removals in each pass; the worst case, depth times those directories, and its limit put to Brett Heap | D3, D4, D5, D7, D14, Risks, Open Questions |
| B-34 | a read of the preflight that the removal floor or the deadline stops before the first removal deletes nothing and changes no state: the stage is `not-attempted` with `target-stopped`, the target `not-attempted` with `deadline-exceeded`, exit 1, the human line naming the deadline, never `refused` with `cache-changed`; a real difference, or a read past its own 5 s budget with no signal received (B-39, B-41), stays `refused`; Codex's P2 at `specs/project-clean-review-safety/spec.md:353` on `e1049b2` is the same item | D1, D7, D8, D11, D12, D14, Risks |
| B-35 | D4 describes #23's joint fit as #26 states it, first at `9ff8202` and, since B-42, at `9b67e8c`, under A-23 and A-24: 81 children, and at the packet's model with cache disposal 10 of 16 targets removed and 9 branches retired through one worker | D4, D13 |
| B-36 | `tasks.md` 2.2 ticked again on lane openRepoProject-4's byte check of B-30's commit, quoted from its log | D6, Migration Plan |
| B-37 | an unsupported platform withholds the cache proof only from a row that reaches the `ignored-local-files` rung; a row that an earlier rung classified, a `dirty` one among them, keeps its classification (Codex's P2 at `specs/project-clean-review-safety/spec.md:383` on `e1049b2`) | D9 |
| B-38 | lane 3's folded read of `cf57956..fffc194`: the last AND of "No time for a cache stage" reads "at least 10 s of work remaining", the complement of the first half's budget under 5 s; "no difference was found"; the packet's reapplication rule cited beside its fit rule; the walk's call count behind D4's 28.3 s | D4, D7, D14 |
| B-39 | a signal received before a preflight read's stop is classified outranks it, and B-41 widens that to every preflight outcome: a read that reaches its own 5 s budget, or the floor or the deadline, after a signal ends the stage `not-attempted` with `target-stopped` and the target `not-attempted` with `interrupted`, never `refused` with `cache-changed`; Codex's P2 at `specs/project-clean-review-safety/spec.md:354` on `fffc194` | D1, D7, D8, D11, D12, D14, Risks |
| B-40 | lane 3's last two LOWs on `fffc194`: B-30's row cites the SHALL NOT sentence's end at `spec.md:35-36`; the quotations of #26's `ca96701` ("13 of its 16 targets ... 11 in the worst case") and of B-19 ("13 at `ca96701`") are verbatim | D4 |
| B-41 | a signal received before the stage classifies any outcome of its preflight, a difference, an error, a byte total past either cap, a `probe-timeout` or a floor or deadline stop, takes the signal's outcome: the stage `not-attempted` with `target-stopped`, nothing deleted, the target and every later one `not-attempted` with `interrupted`, the exit status the signal's; the lead's ruling on this round's own sentence that left a found difference `refused`, which B-39 widened | D1, D7, D8, D11, D12, D14, Risks |
| B-42 | D4 restates #26 at `9b67e8c` exactly, in #26's own words for its counts: 9 of 16 through their stage, 8 in the worst case of the reflog proof, through one worker; at least 5, or 3, at a thread per call, 6, or 5, in the worst order a run can take; all 16 fit through a worker at change 1's measured costs, and at a thread per call at least the 16th target is deferred, where D4 had quoted #26's counts from before its round A5 ("5 and 5, or 4 and 3") | D4 |

What in `project` shapes the approach:

- `repo_state()` runs one ignored-file probe per worktree, `git status
  --porcelain=v1 --ignored=matching`, with no `--untracked-files` and no bound,
  and keeps only the count of `!! ` lines (`project:505-507`); under
  `status.showUntrackedFiles=no` that probe fails, which change 1 records (CAS
  proposal.md:51-53). No list of ignored paths survives it.
- `cleanup_report()` tests `ignored_files is None` (`inspection-error`) and then
  any non-zero count (`ignored-local-files`) before every merge test
  (`project:578-583`), so a merged worktree holding a single `.pyc` file is
  never `merged-removable` today.
- `cleanup_signature()` compares `ignored_files` and `classification`
  (`project:642-645`), and `require_unchanged_cleanup_state()` recomputes the
  whole report to revalidate (`project:656-666`).
- The remove path builds `git -C <root> worktree remove <path>`, shows it,
  confirms it, revalidates and runs it through `execute()` (`project:707-722`,
  `project:736-743`; `execute()` is `project:157-162`); nothing in `project`
  deletes a file today.
- Feature 004 replaces all of this (its `plan.md` slices 2, 3, 5 and 6 on
  `origin/004-project-clean-all-safe`): the bounded runner and its parsers,
  filesystem calls on daemon threads under `min(5 s, work remaining)`, the
  evidence pipeline and pure ladder, the gates and plans, and the seam
  `retire_worktree(plan, target)` with the targeted revalidation. This change
  attaches to that code, so its feature starts after feature 004 merges.

Facts checked here, on Git 2.43.0 and Linux 6.18, with Python 3.10.21 and
3.12.3, in scratch fixtures outside the repository:

| Probe | Observed |
| --- | --- |
| `status --porcelain=v2 -z --untracked-files=normal --ignored=matching` under the ignore rules `__pycache__/` and `*.py[co]` | one record per ignored `__pycache__` directory (`! src/pkg/__pycache__/`), its contents, nested `__pycache__` included, unlisted; one per loose file (`! loose/old.pyc`); porcelain v1 gives the same records with `!!` |
| the same under `*.pyc` and `*.pyo` alone | one record per file (`! src/pkg/__pycache__/a.cpython-312.pyc` and so on); the directories themselves are never listed |
| `--ignored=matching` with `--untracked-files=no`, or with `status.showUntrackedFiles=no` and no `--untracked-files` | `fatal: Unsupported combination of ignored and untracked-files arguments`, exit 128 |
| a symbolic link named `__pycache__` | ignored (`! __pycache__`) under the rule `__pycache__`; untracked (`? __pycache__`) under `__pycache__/`, which makes the row `dirty` |
| a symbolic link named `link.pyc` | ignored under `*.pyc` |
| `os.open(name, O_RDONLY \| O_DIRECTORY \| O_NOFOLLOW, dir_fd=fd)` on a symbolic link to a directory | fails with `ENOTDIR` |
| `os.rmdir(name, dir_fd=fd)` on a directory still holding a file | fails with `ENOTEMPTY`; the file is intact |
| `O_NOFOLLOW`, `O_DIRECTORY`; `open`, `stat`, `unlink`, `rmdir` in `os.supports_dir_fd`; `stat` in `os.supports_follow_symlinks`; `listdir`, `scandir` in `os.supports_fd` | all present on both Pythons on Linux; macOS was not checked here and is not verified by CI, whose jobs `test (3.10)` and `test (3.12)` run on `ubuntu-latest` only (D9) |
| `status --porcelain=v1 -z --untracked-files=normal --ignored=matching` with eight ignored `a0.pyc` to `a7.pyc`, an ignored `__pycache__/` and an ignored `zz.env` | ignored records in path order, so the first eight, the combined probe's samples, are the `.pyc` files and `zz.env` comes after them |
| `os.access` in `os.supports_dir_fd`, `os.supports_effective_ids` and `os.supports_follow_symlinks`; `os.access("__pycache__", os.W_OK \| os.X_OK, dir_fd=fd, effective_ids=True, follow_symlinks=False)` on a `__pycache__` of mode 0555, as a user other than root | all three present; the check returns false, and an `os.unlink` of an entry relative to that directory fails with `EACCES` (errno 13); checked on Python 3.12.3 only, on 2026-10-19 (B-20) |

## Goals / Non-Goals

**Goals:**

- Admit a merged worktree whose only ignored content is Python bytecode, with
  no change for any worktree that holds no ignored file: same plan, digest,
  question, stages and exit status as change 1 (D5, D11).
- Delete nothing that the confirmed plan did not list, never through a symbolic
  link, never outside the worktree, never recursively, and say exactly what was
  and was not deleted when a stage stops (D7, D8).
- Keep change 1's bounds: the 50 s work deadline, the 64 s run bound, the
  removal floor, at most five children per revalidation, and the fit (D4, D12).

**Non-Goals:**

- Any cache kind but `__pycache__`, `.pyc` and `.pyo` (`.pytest_cache` is
  before Brett Heap, B-23, and is added only on his answer); any disposal
  without the worktree's removal; any change to `status`, `doctor` or what `project
  overview` collects (only its equality clause gains the cache exception, D6);
  configurable caps or allowlists; continuing past a failed target.

## Decisions

### D1. The cache stage in the removal sequence

For a selected target whose `cache_disposal.paths` is not empty,
`retire_worktree` runs, in this order:

1. the targeted revalidation of change 1, with D10's status child in place of
   the combined probe;
2. the slot check that change 1 already makes before a spawn, and the start
   condition: more than `removal_floor_seconds` of the work deadline left;
   otherwise the target and every later one are `not-attempted` with
   `interrupted` or `deadline-exceeded`, and nothing is deleted;
3. the whole-list preflight (D7), which also keeps the run's byte total
   (B-26), then the reopening of the first listed cache's chain; a read of
   either that the floor or the deadline stops ends the stage with step 2's
   outcome, nothing deleted, never `refused` (B-34), and a signal recorded by
   the time the stage classifies any outcome of either, a difference, an error,
   a byte total past a cap, a read past its own 5 s budget or a stop by the
   floor or the deadline, is checked first and gives step 2's `interrupted`
   outcome in its place (B-39, B-41);
3a. immediately before the hand-off of the first removal, the floor and slot
   checks of step 2 again, with the same outcome; a signal recorded after this
   check is handled as one received during the removals (B-17), and the
   hand-off that follows is the stage's first removal for every rule of the
   two ADDED requirements (B-16);
4. the removals (D7), each handed over only while more than the floor remains
   and waited for until it returns (D12), then, on any failure, the rescan
   (D8);
5. change 1's floor and slot checks, then the spawn, the wait and the
   reconciliation, unchanged; a target whose stage ended `disposed` and whose
   spawn these checks refuse is `not-attempted`, with its reconciliation (D8).

A target with no listed cache skips steps 2 to 4, so its sequence is change 1's
exactly. The one clause inserted into "Clean can explicitly retire verified
worktrees" names steps 2 to 4 as one step; the ADDED requirement holds the
rest.
Nothing runs between step 4 and the spawn but the checks of step 5, so the
revalidation that the narrow guarantee names is, for a cache target, the one of
step 1, as the MODIFIED "Cleanup states a narrow guarantee and its residual
window" states (B-10; D13).

### D2. The allowlist, candidates and blocking paths

A listed cache is decided from Git's record and from `lstat` results read
without following a symbolic link (D3, D7), by byte comparison only: a directory
record whose last component is exactly `__pycache__`, whose walk finds only
regular files whose names end exactly `.pyc` or `.pyo` and directories named
exactly `__pycache__` that pass the same walk; or a file record whose name ends
exactly `.pyc` or `.pyo` and whose `lstat` is a regular file. Python's own
temporary names (`*.pyc.<number>`, left by an interrupted write) and any
`__PYCACHE__` on a case-insensitive filesystem are blocking. A record's parent
directories may have any name (the `bb91a49` review finding at `project:759`
of that commit, where a parent not named `__pycache__` was refused after
confirmation); each must be a non-symlink directory on the worktree root's
device (CD-8), recorded in `directories` (D5).

A candidate is decided from evidence the plan already holds before any
enumeration: the combined probe established `dirty` false with at least one
ignored record; the sample test passes; with the ignored-files rung skipped,
the pure ladder gives `merged-removable`; and the gates before
`deferred-target-cap` pass (`main-worktree`, `unsupported-path-bytes`,
`registration-mismatch`, `locked-worktree`, `not-requested`, and the reflog
gate, read for the candidate as change 1 reads it for each row it checks: one
more bounded filesystem read of at most 64 KiB and no Git child). In single
mode only P can pass `not-requested`. The plan takes candidates in canonical
order and enumerates the first 16 (D4).

The sample test (B-12) is a pure function of the row's `ignored_samples`, the
up to 8 ignored paths that change 1's incremental status parser keeps (CAS
design.md:164-171), which it takes as Git prints them, in path order (Context):
a sample that is not valid UTF-8, or whose last component, a
trailing `/` disregarded, is neither exactly `__pycache__` nor a name ending
exactly `.pyc` or `.pyo`, is blocking whatever it holds, so the row is not a
candidate. It stays `ignored-local-files` with `not-candidate`, its counts
`null`, and its rejected samples in `blocking_samples`, so the preview can name
the path that keeps it. The test spends no child and no filesystem call, and it
keeps every row with a sampled `local.env` out of the 16 enumerations (D4).

A row that holds ignored records and passes the sample test but is still not a
candidate carries `candidate_block` (B-24): the class the pure ladder gives it
with the ignored-files rung skipped, when that class is not `merged-removable`,
or else the first gate before `deferred-target-cap` that it fails. The candidate
test already computes both: the ladder's inputs are the repository-wide ref
listing and merged set and the row's own combined probe, and the gates before
`deferred-target-cap` read the registry, the lock, the path's bytes and the
reflog file, which the candidate test reads for exactly the rows whose answer
depends on it. So `candidate_block` spawns no Git child, and there is no gap to
record. Its values are existing class names and gate reasons (L-4, CD-16). The
preview prints it after the unknown counts (D11), so that a detached,
unpublished or unmerged row whose sampled ignored files are all caches is told
what really keeps it rather than to delete its caches; squash-merged worktrees
are among those rows while question 2 is open. Every other row carries
`candidate_block` null.

A record is blocking when it is not a listed cache. A directory record stops its
walk at the first entry that is not allowed, and counts once as blocking. Up to
8 blocking records are kept, in the order Git prints them, as
`blocking_samples`.

### D3. The cache enumeration's child and parser

The child is a D2 handle of change 1's kind `probe`: the scrubbed environment
with `GIT_OPTIONAL_LOCKS=0`, the seven protocol pins, `-c
core.untrackedCache=false -c core.fsmonitor=false`, and `-C <worktree>` after
the row's identity check, with the argument vector `status --porcelain=v2 -z
--untracked-files=normal --ignored=matching`. `--untracked-files=normal` is
there because Git refuses `--ignored=matching` otherwise (Context; CD-5), as a
user's `status.showUntrackedFiles=no` would make it.

A sixth incremental parser, beside change 1's five, reads porcelain v2 with
`-z`: an ignored record is `! `, then a NUL-terminated path, a directory's path
ending `/`; any other record type (`1`, `2`, `u`, `?`) sets an `other` flag and
stops the child, since the combined probe had established `dirty` false and the
row has changed under the plan. The parser stops at the 513th record, holds at
most one partial record, and is fed byte by byte and whole in its tests, as
change 1's parsers are. Git prints changed and untracked entries before ignored
ones, so a non-ignored record arrives first when there is one.

The walk then takes the records in canonical order, depth-first: it opens each
directory it records once, from the worktree root down, relative to its
parent's descriptor and checking that it is a non-symlink directory on the
root's device, keeping open only the directories above the current record; it
`lstat`s each listed file relative to its parent, lists each listed cache
directory, `lstat`s each entry relative to it and descends into each entry
named `__pycache__` that is a directory, counting every object it records,
entries and directories alike, toward the per-worktree cap of 512 (B-33),
summing the regular files' `st_size`, and stopping at the first entry outside
the shape or at a per-worktree cap. Opening each recorded directory once keeps
the walk's opens within its recorded objects, where a chain per record would
cost depth times records (D4).

For a row whose walk finished with `blocking` 0 and within the per-worktree
caps, the walk then checks each directory that its stage would change, each
listed cache directory, each nested `__pycache__` and the parent of each listed
path, with `os.access(name, os.W_OK | os.X_OK, dir_fd=parent,
effective_ids=True, follow_symlinks=False)`, one filesystem call under the
per-call budget (B-20). A false result leaves the row `ignored-local-files`
with `cache-unwritable`, its counts, paths and directories established; it is
not selected, its entries are not counted toward the invocation's totals, and
it stops nothing, by the principle of A-17 for a refusal the plan can see. A
`__pycache__` that a root-run container or `sudo python` wrote is the usual
cause; none was found on this workstation (the council's measurement of
2026-10-19). A check that times out leaves the row `cache-unverified`, as any
walk call does. What the check cannot see, a sticky directory or a read-only
filesystem, fails the stage's first removal instead, which then ends the stage
`refused` with `cache-changed` and nothing deleted (D8).

### D4. The caps and the fit

| Limit | Value | Scope | Reached |
| --- | --- | --- | --- |
| `cache_rows` | 16 | enumerations per invocation | later candidates `cache-cap` |
| `cache_entries` | 512 | Git records, and recorded objects, the cache entries and every directory the plan records (B-33), per worktree | `cache-cap` |
| `cache_bytes` | 268,435,456 (256 MiB) | `lstat` sizes of regular files per worktree | `cache-cap` |
| `cache_entries_total` | 4,096 | cache entries over the invocation's cache-only rows | that row `cache-cap`, its entries uncounted |
| `cache_bytes_total` | 1,073,741,824 (1 GiB) | bytes, likewise, and at each cache stage's preflight the bytes it measures (B-26) | likewise; at a preflight, that target `refused` with `cache-changed` |

A cap reached keeps the row `ignored-local-files` and the plan complete, so the
batch removes everything else, and a later run takes the rest unless each of
the 16 enumerated candidates stays at the rung. A candidate left at the rung
keeps its place among the 16, as change 1's index gates keep theirs. The sample
test (D2) keeps out every row whose samples show a blocking name; what can
still hold a place is a candidate whose samples all have cache names while it
holds a blocking path beyond its 8 samples, a cache-named path that is blocking
by its type, contents or device (a symbolic link named `__pycache__`, a
`__pycache__` holding `notes.txt`, a mount), more than a per-worktree cap
allows, an enumeration that failed, or a directory the user cannot change
(B-20). The stall line (B-21, D11) is printed only when each of the first 16
candidates in canonical order is held at the rung for a persistent reason, any
one of these: `blocking` above 0; `cache-cap` from a per-worktree cap;
`cache-unverified`; or `cache-unwritable` (B-32). The test reads those reasons
and never `blocking` alone, which is null for `cache-cap` and
`cache-unverified` and 0 for `cache-unwritable`, so that sixteen rows held by
those three print the line too (Codex's P2 at `specs/project-clean/spec.md:910`
on `cf57956`). The report tells a per-worktree cap from the invocation's totals
by the counts the row already carries: a per-worktree cap stops the enumeration
and leaves them null, while a row left only by the totals keeps them
established, `blocking` 0, and drains on the next run, printing none; the
16-enumeration cap leaves only candidates past the 16th. One run cannot
tell that an enumeration "fails each time", so a `cache-unverified` row is
named as one to re-run and, if it repeats, to inspect, never as one to remove
by hand. Bytes are the apparent sizes
that `lstat` reports at plan time; a sparse file counts at its apparent size,
which only errs toward a cap.

The invocation's byte total is applied twice. At plan time the totals count,
in canonical order, the planned entries and bytes of the rows that pass every
per-worktree check (the `cache-cap` rule). At each cache stage the preflight
applies the byte total again, to the sizes it measures (B-26, Codex's P2 at
`specs/project-clean-review-safety/spec.md:341` on `90d18ee`): a `.pyc`
recompiled in place keeps its name, its type and its cache's number of
entries, so it passes the revalidation and the preflight's count, but it can
grow, and five targets planned with tiny caches could each reach the 256 MiB
per-worktree cap, 1.25 GiB in all. So the preflight keeps the run's byte
total, the bytes it measures for this target added to those it measured for
every earlier target whose stage passed its preflight in this run, and a
target whose bytes would take that total past 1 GiB ends `refused` with
`cache-changed`, nothing deleted, as one past the per-worktree cap at its
preflight does; the run then stops at that target (CD-1), exit 2, and the
earlier targets keep their results. Entries need no running total, since the
preflight requires each listed cache's entries to equal the plan's, whose sum
the plan already capped at 4,096. The check adds no filesystem call: the
preflight already `lstat`s every entry it re-lists.

The fit is change 1's (CAS design D14; `BA:729-735`) at 150 ms per Git child and
0.3 s per removal, with the enumerations added:

| Mode | Children | Time | Fits the 50 s work deadline |
| --- | --- | --- | --- |
| all-safe, 128 rows, 16 enumerations, 16 targets | 7 + 128 + 16 + 16 + 80 + 3 = 250, and 16 removals | 37.5 s + about 4.8 s = 42.3 s | yes for the Git children and removals: the 16th target reaches its cache stage or spawn after 247 children and 15 removals, at about 41.55 s, with 8.45 s left before the walk's and the stages' filesystem time; with that time at B-25's bound, no at the top of the measured cost, 15 of 16 targets reaching their stage (below); in B-33's worst shapes fewer, or none at a thread per call (below) |
| report, 256 rows | 7 + 256 + 16 + 16 = 295 | 44.25 s, plus the walk's about 2.0 s (B-25): about 46.3 s, and 44.25 + 5.6 = about 49.85 s at a thread per call | yes for ordinary trees, by about 0.15 s at a thread per call; in B-33's directory shape only at 169 us (below) |
| single, 128 rows plus P | 7 + 129 + 1 + 1 + 5 + 3 = 146, and 1 removal | 21.9 s + about 0.3 s | yes |
| all-safe, one enumeration per candidate (no `cache_rows`) | 7 + 128 + 127 + 16 + 80 + 3 = 361 | 54.15 s + 4.8 s | no |
| report, likewise | 7 + 256 + 255 + 16 = 534 | 80.1 s | no |

The last two rows are why CD-6 adds `cache_rows`. A cache stage spawns no
child. In each of its two passes, the preflight and the removals, it opens one
chain per directory that holds a listed path (B-33): the worktree root by its
path and each directory below it down to that one, each open checking its
identity, and then the listed caches in that directory from its descriptor.
Beyond the chains it makes two calls per cache entry that is a file (its
`lstat` at the preflight, its unlink after it) and five per one that is a
directory (its `lstat`, open and listing at the preflight, its open and removal
after it). For an ordinary tree, `__pycache__` directories of `.pyc` files
under package directories a few levels deep, that is about 1,100 calls for 512
entries and about 8,500 for the 4,096 of a run. The plan-time walk makes one
call per directory open, per listing and per entry `lstat`, and one access
check per directory a stage would change (B-20); it opens each directory it
records once and counts every directory it records toward the per-worktree cap
with the entries (D3, B-33). It walks more than the stages remove: each of the
16 enumerated rows can be walked to its per-worktree cap of 512 recorded
objects before the invocation's totals reject it, and a row that the totals
reject is uncounted from the 4,096 but was walked (B-25, Codex's P2 at
`design.md:294` on `90d18ee`). The walk's bound is therefore 16 x 512 = 8,192
recorded objects: about 9,000 calls for ordinary trees, whose objects are
mostly files, and at most four calls an object, a nested `__pycache__`
directory's `lstat`, open, listing and access check, about 32,800 where every
object is a directory.
Through one daemon worker per stage (D12), the hand-off measured 169-224 us a
call at load 30 to 37 on this workstation, and 393-622 us for a thread per
call, the shape of feature 004's `fs_call` (`clarifications.md`, S-4): at
224 us, 8,500 stage calls take 1.9 s and the walk's 9,000 take 2.0 s, about
2 s each; at 622 us, a thread per call, 5.3 s and 5.6 s. A 512-entry stage
took about 0.25 s here (AE-4's 1,248 calls in 236 to 273 ms).

The fit for ordinary trees, restated with those costs, with the walk's bound of
B-25 and with the stage's removals waited for (B-16); B-33's worst case follows
it. At the packet's 150 ms model, target k
reaches its cache stage, or its spawn when it lists no cache, after the 167
planning children (7 + 128 + 16 + 16), the 5k revalidation children of it and
the targets before it, and k - 1 removals: at 0.15 x (167 + 5k) + 0.3 x (k - 1)
= 24.75 + 1.05k s, plus the walk and the earlier stages. A stage starts only
while more than the 5 s floor remains, and a removal child is spawned only
while at least that floor remains, so each must come by about 45 s.
The walk's bound and the stages' come together: of the 16 enumerated rows, 8
of 512 entries fill the run's 4,096 and are selected, and 8 more are walked to
the 512 recorded objects of their cap and kept by it, so 8 cache targets share
the 16 targets with 8 that list no cache. Through one worker at 224 us a call,
the 16th target, which lists no cache once the 8 stages come before it, then
arrives at its spawn at 41.55 + 2.0 + 1.9 = about 45.5 s, with about 4.5 s
left, under the floor, while the 15th arrives at 40.5 + 2.0 + 1.9 = 44.4 s,
with 5.6 s left:
15 of 16 targets reach their stage, and the 16th is `not-attempted` with
`deadline-exceeded`, exit 1, and the next run takes it, never unsafe. At
169 us a call (1.5 s of walk, 1.4 s of stages) the 16th arrives at about
44.5 s, with about 5.5 s left, and all 16 fit. At a thread per call the 16th
would arrive at 41.55 + 5.6 + 5.3 = about 52.4 s, past the work deadline
itself: with the 8 cache targets first in canonical order the 9th arrives at
34.2 + 5.6 + 5.3 = about 45.1 s, so 8 of 16 targets reach their stage, and
with them last, 12 of 16. Before B-25 these figures read about 44.6 s with
about 5.4 s left (41.55 + 1 + 2, the walk counted only over the 4,096 entries
the totals admit) and about 49.65 s at a thread per call (41.55 + 2.8 + 5.3).
So at B-25's bound the all-safe mode no longer fits at the top of the measured
cost: through one worker the floor refuses the spawn of the 16th target, which
lists no cache, at the packet's model (B-31, lane 3's delta read), and at a
thread per call as few as 8 targets reach their stage, the rest deferred to the
next run with exit 1. No cap changes (B-25): B-3 and CD-6 stay
Brett Heap's question (proposal, Open Questions), and task 2.3's measurement
decides under the rule below. At change 1's measured costs (CAS `tasks.md`
2.1: the 16th removal spawning at 23.6 s with 26.4 s left), the 16
enumerations add at most about 3.7 s and the walk and stages at most about
10.9 s (5.6 + 5.3, at a thread per call), the 16th then spawning by about
38.2 s, and all 16 fit. A removal is handed over only while
more than the floor remains and is waited for until it returns, as change 1
waits for its removal child; an unlink returns in microseconds, so in the
normal case this costs nothing, and the floor stays for the spawn. A hung
mount costs what a hung removal child costs: up to the 300 s removal ceiling,
counted from the hand-off, after which that cache is `removed: null`, the
stage ends `partial`, the later targets are `not-attempted` with
`deadline-exceeded`, and the run reconciles in its reserve, counted from the
return or the ceiling; the 64 s run bound keeps its two exceptions, a removal
in flight and a filesystem call stuck in the kernel. B-19 adds no Git child,
B-20 only filesystem calls, and B-24 none.

The worst case of B-33. Counting every recorded directory toward the 512
bounds a row's depth and its number of directories with removals, but the
stage opens one chain per such directory in each pass, so a pass costs the sum,
over those directories, of one plus each one's depth below the worktree root:
depth times directories at worst (Codex's P2 at `design.md:323` on `cf57956`).
Under the 512-object cap that sum is largest for a chain of 341 directories
whose deepest 171 each hold one loose `.pyc` (341 + 171 = 512 objects): 172 +
173 + ... + 342 = 43,947 opens per pass, and 88,236 calls for the target with
the files' `lstat` calls and unlinks, about 14.9 s at 169 us, 19.8 s at 224 us
and 54.9 s at 622 us. Sixteen such targets list 2,736 entries, within the
run's 4,096, and would need about 1.41 million calls, 239 to 878 s. Nothing is
unsafe, but no fit holds that: at 224 us the first such target reaches its stage
at about 28.3 s (the 172 Git children before it, 25.8 s at the packet's 150 ms,
and the walk of those 16 rows at 683 calls a row, 10,928 calls and 2.45 s: 341
directory opens, 171 file `lstat` calls and 171 access checks, besides the
worktree root's own open), its preflight takes about 9.9 s, and the floor ends
its removals about 7 s later, `partial`, exit 1, so each run removes part of its
caches and no worktree while it comes first; at 169 us one such target is
removed in a run, and at a thread per call its preflight alone runs into the
floor, which ends the stage before its first removal with nothing deleted,
`not-attempted` with `deadline-exceeded` and no change of state (B-34). So
the fit cannot hold without a new limit. A limit on depth alone would not do:
a row 8 levels deep still holds 252 directories with removals, 2,268 opens per
pass, and 16 such targets need 72,576 opens in their two passes. The proposal
therefore puts a limit on the chains to Brett Heap beside B-3 and CD-6
(proposal, Open Questions). It recommends `limits.cache_opens`, 512 opens per
pass per worktree, the sum above as the walk computes it, past which a row
stays `ignored-local-files` with `cache-cap` from a per-worktree cap, so that a
run's chains are at most 16 x 2 x 512 = 16,384 opens, about 3.7 s at 224 us and
10.2 s at 622 us. The deltas do not add it, and no cap changes (B-33).

The other worst shape is every recorded object a directory, as in 16 rows each
holding 512 nested `__pycache__` directories, whose chains stay short. The walk
then makes four calls an object, about 32,800 calls, 5.5 s at 169 us, 7.3 s at
224 us and 20.4 s at 622 us, and the 8 targets that the totals select make
five calls an entry, about 20,500 calls, 3.5 s to 12.7 s. With those 8 targets
first, through one worker, 10 of 16 targets reach their stage or spawn at
169 us and 8 at 224 us, the 9th arriving at about 46.1 s; at a thread per call
the walk ends planning at about 45.5 s, so none does, and the report mode,
44.25 s of Git children and the walk, exceeds the work deadline, about 51.6 s
at 224 us and 64.7 s at 622 us, its plan incomplete with `deadline-exceeded`,
fitting only at 169 us, about 49.8 s. With the recommended limit as well, a
run makes at most about 69,700 filesystem calls (the walk's 32,800, the
chains' 16,384 and the stages' other 20,480), about 11.8 s at 169 us and 15.6 s
at 224 us, and through one worker at least 9 of 16 targets reach their stage
or spawn at 169 us and at least 7 at 224 us. At change 1's measured costs that
worst case adds at most about 15.6 s through one worker at 224 us, the 16th
removal then spawning by about 42.9 s, so all 16 fit, while at a thread per
call the walk alone, about 20.4 s, takes the 16th past the floor. This shape
is within the existing caps, so its remedy is B-3 and CD-6's rule below, which
task 2.3's deep-tree measurement applies; no cap changes now, and the modes of
the table above fit as it says for ordinary trees only.

Governance task 2.3 measures the enumeration, the walk at 16 rows of 512
recorded objects with the invocation's totals reached (8,192 walked, 4,096
counted; B-25), the deep-tree worst case of B-33 (the chain of 341 directories
and the rows of nested `__pycache__` directories) and the stage before the
handoff, through `fs_call`, idle and at the workstation's usual load, as
change 1's task 2.1 measured its probes; a measured cost that breaks the fit
lowers `cache_rows` in steps of 4 and the entry caps in powers of two before
the feature starts. The fit sentence of the bounds block counts the Git
children and states the walk's and the stages' filesystem calls as outside
it, and a target whose stage or spawn cannot start under the floor is
`not-attempted` with `deadline-exceeded` as for every removal (QA-5), so the
margins above are design arithmetic, not a promise of the spec.

With `--retire-branches` (#23, PR #26) a run spawns branch children too, and #26
states the joint fit at `9b67e8c` (its design.md D7), under A-23, A-24 and A-25
(B-35, B-42). A flagged run adds at most 81 children: 64 for the retirement
stage, four for each retired branch (the re-read's listing, its re-proof of the
reflog, the branch child and the post-check), and 17 reflog children, one for
the repository and one per selected row. With this change's walk and earlier
stages added whole as B-25 gives them, for ordinary trees, B-33's worst shapes
staying under this change's own questions (A-25), #26 says: "So at the packet's
150 ms model a flagged run with cache disposal brings 9 of its 16 targets
through their stage before the floor, 8 in the worst case of the reflog proof,
through one worker per stage, and at least 5, or 3, at a thread per call, 6, or
5, in the worst order a run can take; change 1's own deadline rule makes the
rest `not-attempted` with `deadline-exceeded`, the run exits 1, and the next run
takes them, never unsafe (`BA:772-774`). At change 1's measured costs all 16 fit
through a worker; at a thread per call at least the 16th target is deferred,
with one reflog child as in the worst case." Its bullets give those counts as
removals and branch children. Through one worker per stage they are 10 and 9,
and 8 and 8 in the worst case of 17 reflog children; at a thread per call 5 and
5, and 4 and 3; in the worst order, which puts first the 8 cache targets that
this change's totals select, each stage spending an eighth of the stage time
just before its own removal, 6 and 6, and 5 and 5, at a thread per call, and
through a worker the counts of the first bullet. Its draft at `ca96701` read "13
of its 16 targets ... 11 in the worst case" and left the cache-stage filesystem
time out. #26, which archives after this change, states that joint fit (A-9, the
alignment review's G3), which stays Brett Heap's question, `limits.targets`
staying 16. The inputs it needs from this change, as rounds B3 and B4 restate
them:

- Git children: 16 cache enumerations per invocation under `probes`, 2.4 s at
  the model; none added at revalidation, where the enumeration's child takes
  the combined probe's place (CD-4); and no status probe after a `disposed`
  stage, which B-19 rejected.
- Plan-time filesystem calls: the walk's at most 8,192 recorded objects, 16
  rows of 512 with the rows the invocation's totals reject included and every
  directory it records counted, each opened once (B-33), and the access
  checks, at most one per planned directory: for ordinary trees about 9,000
  calls, about 2 s through one worker per stage and up to about 5.6 s at a
  thread per call (B-25); at most four calls an object, about 32,800 calls,
  7.3 s and 20.4 s, where every object is a directory.
- Stage filesystem calls: for ordinary trees about 1,100 per target and 8,500
  per run, about 0.25 s for a 512-entry stage, about 2 s per run through one
  worker, up to about 5.3 s at a thread per call; at worst one chain per
  directory with removals in each pass, up to 43,947 opens a pass for one
  target under the 512-object cap, which the Open Question's limit would hold
  to 512 (16,384 for a run's two passes), and five calls an entry, 20,480 for a
  run (B-33).
- Start and hand-off: a stage starts, and hands over each removal, only while
  more than the 5 s floor remains; a removal handed over is waited for up to
  the 300 s ceiling and counts as a removal in flight.
- Counts: `operations.estimated` and `performed` gain one per cache entry, the
  latter only for removals that returned.
- The residual-window line of a run that selects a cache target is D13's, so a
  flagged run with a cache target re-bases its line on it.

### D5. Planned identities and the digest

The plan records, for each candidate whose enumeration finished, every
directory the stage will open below the worktree root: each directory on the way
down to a listed cache, each listed cache directory and each nested
`__pycache__` directory, as `{path, path_valid_utf8, dev, ino}`, the device and
inode from an `lstat` that follows no symbolic link. The worktree root's own
identity is change 1's `{path, dev, ino, admin_id}` of the selected entry. Each
of those directories counts toward the per-worktree cap of 512 recorded objects
with the cache entries, once however many listed paths lie below it (B-33), so
the depth of a listed path and the number of directories above the caches are
bounded with the entries.

Files carry no identity. Unlinking a name inside a directory whose identity was
just checked can only remove that name: a file replaced by a symbolic link loses
only the link, and a hard link only its name in the worktree. Python writes a
`.pyc` by renaming a temporary file over it, so a file's inode changes whenever
Python recompiles, and an identity in the plan would refuse `--expect-plan` and
the preflight for no safety gain. Each listed file is instead checked for its
type at the preflight, and each listed cache for its planned number of entries
(D7, QA-1): a `.pyc` written into a listed directory adds an entry and
refuses, while a `.pyc` recompiled in place keeps the count and passes, its
new size counted at the preflight toward the per-worktree cap and the run's
byte total (D4, B-26). A file
renamed within a listed directory keeps the count too; it is an allowlisted
cache either way, so the stage still removes nothing but caches.

The canonical text of `plan_digest` is change 1's (CAS/pc:629-632): the four
repository identity fields, the merge target's name and SHA, and the selected
`[path, branch, head]` triples. For a selected target with listed caches, its
triple is followed by its `paths` as `[path, kind]` and its `directories` as
`[path, dev, ino]`, each in canonical order by raw bytes; a plan with no such
target serializes exactly as change 1's, so its digest is unchanged (CD-14).
The MODIFIED "Clean previews and applies a batch of eligible worktree removals
in one repository" states this beside change 1's digest sentence (B-10). A new
`__pycache__` beside a listed one, or a listed directory moved out and made
again, changes the digest; a `.pyc` recompiled in place does not. Tests move a
directory out of the worktree before making its replacement, since a deleted
directory's inode number can be reused at once on ext4 (QA-6).

### D6. The ladder, the counts and the overview

The pure ladder gains one input per row, the cache proof, which is true only
when the row's enumeration finished with `reason` null and `blocking` 0. The
ignored-files rung tests `ignored_files` as before, except that a row with the
proof passes it. A row whose enumeration did not run or did not finish has no
proof and stays at the rung, `cache_disposal.reason` saying why; a failed
enumeration never makes the row `inspection-error` (CD-9), because its combined
probe already established its state.

`disposable` and `blocking` count Git records, which for a directory record is
one `__pycache__` tree; they can exceed `ignored_files`, which change 1 caps at
64. Both are `null` whenever the enumeration did not run or did not finish,
which is the `1789ad9` thread that APO proposal.md:804-809 hands to this
change: unknown is never printed as 0. A row with no ignored record carries no
`cache_disposal` at all (L-10, B-13): its `ignored_files` of 0 already says
there is nothing to count, and a `null` object would read as unknown.

`status` and `doctor` keep their evidence; doctor classifies no worktree.
`project overview` feeds the same ladder from evidence that has no cache proof,
so it reads a cache-only candidate `ignored-local-files` where `project clean`
reads it `merged-removable`, against change 2's equality clause
(APO/ov:381-386). The overview's suggestion for that row is then the read-only
form, whose report shows the row selectable, so no suggestion becomes unsafe.
B-14 settles the clause in this change: its `project-overview` delta appends
two sentences to the equality clause, agreed by lane openRepoProject-4 on
2026-10-19 and committed as `b4d3e12`. B-22 rewords them, since lane 3 found
cache-proven rows that `project clean` classifies `merged-removable` and then
excludes (as `contains-submodule`, `deferred-target-cap` or
`hidden-local-state`), which the first wording missed (M4), and a second
sentence that read at the gate level contradicted change 2's carried rule that
a gate finding replaces the housekeeping finding "while the classification
stays" (M5): the exception now covers a worktree that `project clean`
classifies `merged-removable` because clean's cache enumeration proved every
ignored path a listed cache, and the overview SHALL NOT classify a worktree
`merged-removable` where `project clean` classifies it otherwise for the same
working directory and refs. Lane 4 agreed the edit on 2026-10-19, with one
optional point that the committed text takes, "clean's" for "its" before
"cache enumeration", and it is committed as `9f30fb9` (`tasks.md` 2.2). B-30
adds "for the same working directory and refs", lane 4's own words of
2026-10-20, since read alone the sentence bound runs from different
directories, where the current worktree decides `merged-current` against
`merged-removable`; it is committed as `4d5855a`, the added scenario's AND
following it, and lane 4 byte-checked it on 2026-10-20 (B-36; `tasks.md` 2.2).
The council measured 3 such submodule rows on this workstation on 2026-10-19.
Feature 005's spec (`specs/005-project-overview/spec.md` on
`origin/005-project-overview` at `33a1214`, User Story 3 scenario 6) names the
`ignored-local-files` row of its "Every protected classifier" fixture by its
class only, and feature 005 has no plan or test yet. Once feature 005 has
landed, any of its tests asserting that the overview and `project clean`
classify identically gets the cache case excluded in this change's
realization, never in feature 005 (D14).

### D7. The whole-list preflight and descriptor-relative removal

Descriptor chains. Every directory is reached from the worktree root by a chain
of `os.open(component, O_RDONLY | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC,
dir_fd=parent)`, each opened descriptor checked by `os.fstat` against its
planned `dev` and `ino`. The root itself is opened by its recorded path with
`O_DIRECTORY | O_NOFOLLOW` and checked against the target's worktree identity;
the root's own ancestors are change 1's concern, checked at revalidation through
the realpath and identity comparison, so `BA:1324-1325`'s "any ancestor" is read
as any directory between the worktree root and the cache (lane 3's LOW 3). The
stage handles one directory holding a listed path at a time (B-33): in each
pass it opens the chain to that directory once, checking every identity on it,
deals with every listed path in it, reaching a listed cache directory and its
nested ones from that directory's descriptor, and closes the chain before the
next, except a descriptor given to a call still outstanding, which stays open
until `project` exits (D12). So at most that chain's descriptors and those of
the nesting below it, and those of an outstanding call, are open at once, a
number the 512-object cap bounds and an ordinary tree keeps far below any
platform's default descriptor limit; an open that fails, `EMFILE` included, is
an error like any other (D8). One chain per directory, rather than one per
listed path, is what bounds the stage's opens by depth times directories with
removals (D4).

The preflight, before any removal: for each directory holding a listed path, in
canonical order, open its chain once, checking every identity; then for each
listed cache in it: for a directory, list it and `lstat` each entry relative to
it, require the allowlisted shape, require each nested `__pycache__` to carry
its planned identity, require the cache to hold exactly its planned number of
entries, and record the names to remove; for a file, `lstat` it relative to
that directory and require a regular file with an allowed suffix; keep the
target's running byte total within the per-worktree cap; and
keep the run's byte total, this target's measured bytes added to those
measured at the preflight of every earlier target whose stage passed it in
this run, within the invocation's 1 GiB (B-26, D4). Any `OSError` (`ENOTDIR`
or `ELOOP` from a swapped symlink, `ENOENT`, `EACCES`), any identity, shape or
entry-count difference, either byte cap exceeded, or a call past its own 5 s
budget (`probe-timeout`) ends the stage `refused` with `cache-changed`, unless a
signal was received first (B-41, below). A read of the preflight, or of the
reopening of the first listed cache's chain after it, that the removal floor or
the deadline stops is not one of these (B-34, Codex's P2 at
`specs/project-clean-review-safety/spec.md:353` on `e1049b2`): the read's budget
is `min(5 s, work remaining less the removal floor)`, so a read that outlives
the second term, where it is the smaller, ran into the deadline, recorded
`deadline-exceeded` as change 1's bounds rule records it, and a read that cannot
start because no more than the floor remains has no budget at all. Neither has
found a difference: nothing was deleted, and no difference was found before the
read stopped, so the stage ends `not-attempted` with `target-stopped`, as at the
check before the first hand-off (D1, step 3a), and the target `not-attempted`
with `deadline-exceeded`. Which budget ran out tells a slow run from a changed
worktree, and a read past the 5 s budget is still a preflight error, where no
signal was received. The signal comes first (B-39, B-41; Codex's P2 at
`specs/project-clean-review-safety/spec.md:354` on `fffc194`): the stage reads
the slot before it classifies any outcome of the preflight, or of the reopening,
whether a difference, an error, a byte total past a cap, a `probe-timeout`, or a
stop by the floor or the deadline, and a signal recorded by then gives the check
before the first hand-off's outcome instead: the stage `not-attempted` with
`target-stopped`, the target and every later one `not-attempted` with
`interrupted`, the exit status the signal's, never `refused` with
`cache-changed` and never `deadline-exceeded`. The signal has stopped the run,
so nothing is acted on that the preflight found: nothing is deleted in either
reading, and a re-run's preflight sees any real difference again. This is the
whole-list check that PR #2's open thread 3989548481 asked for: no path is
removed until every path has passed.

The removals: for each directory holding a listed path, in canonical order,
open its chain again, once, checking every identity again; then for each listed
cache in it, remove the names fixed at the preflight, depth-first, files by
`os.unlink(name, dir_fd=directory)` and each emptied nested directory by
`os.rmdir(name, dir_fd=parent)`, then the listed directory by `os.rmdir`
relative to that directory; a listed file by `os.unlink` relative to it.
Nothing listed after the preflight is removed, and `rmdir` refuses a
directory that holds anything else, so a file placed in a cache directory at any
time before that directory's removal survives (Context, `ENOTEMPTY`) and ends
the stage `partial`, or `refused` when no entry had yet been removed (D8). Each
unlink and directory removal is handed to the worker
only while more than the removal floor remains and is waited for until it
returns (D12). No recursive deletion, no `shutil.rmtree`, no path-name
deletion and no child process is used.

### D8. The partial phase and the target's result

The stage's first removal is the hand-off of its first unlink or directory
removal to the worker, not the first one completed (B-16). After it, any
failure (an `OSError` from an unlink, a removal or a chain open, `ENOENT`
included, since something else is changing the worktree), a read past its
budget, a removal still outstanding when the 300 s removal ceiling, counted
from its hand-off, ends its wait, or the removal floor reached at the next
hand-off ends the removals. A stage that has handed over a removal ends
`disposed` or `partial`, never `refused`, with one exception: when every
removal handed over has returned and none removed its entry, as when the first
unlink meets a sticky directory or a read-only filesystem that the plan's
access check cannot see (B-20), it ends `refused` with `cache-changed`, nothing
deleted. Otherwise the stage then rescans each listed cache (B-18): on threads
of its own, never the stage's worker, each call a reconciliation probe under
`min(5 s, reserve remaining)`, it opens the chain to the cache's parent as in D7,
checking every identity, and `lstat`s the cache's name relative to it with
`follow_symlinks=False`; absent is `removed: true`, present `removed: false`,
and a chain that no longer opens or carries another identity is `removed:
null`, while the first call past its budget leaves that cache and every later
one `removed: null`. A cache with a removal still outstanding is `removed:
null` whatever the rescan finds, since that call can still complete. Its
`cache_disposal` is `partial` with `cache-partial`, the planned `entries`, and
`entries_removed` counting the removals that returned having removed their
entry, as `operations.performed` does; an outstanding removal counts in
neither. The rescan of the listed paths, beside the target's reconciliation,
is this change's reading of `BA:1334`'s "the report rescans the worktree"
(lane 3's LOW 2): a status of the worktree would add a Git child and would not
say which listed path remains.

| Stage outcome | `cache_disposal` | Target | Later targets | Exit (first matching row of change 1's table) |
| --- | --- | --- | --- | --- |
| every listed cache removed | `disposed`, null | the sequence goes on to the spawn | as change 1 | as change 1 |
| preflight difference, error or call past its 5 s budget with no signal received (B-41), either byte cap included (B-26) | `refused`, `cache-changed`; each `removed` false where the preflight found the path, null where it did not | `refused`, `state-changed`, reconciliation, nothing spawned | `not-attempted`, `batch-stopped` | 2 |
| every removal handed over returned and none removed its entry (B-20) | `refused`, `cache-changed`; each `removed` false | likewise | likewise | 2 |
| failure after an entry was removed | `partial`, `cache-partial` | likewise | likewise | 2 |
| the floor reached at a hand-off after the first removal | `partial`, `cache-partial` | likewise | `not-attempted`, `deadline-exceeded` | 1 (the deadline stopped work) |
| a removal still outstanding at the 300 s removal ceiling (B-16) | `partial`, `cache-partial`; that cache `removed: null` | likewise | `not-attempted`, `deadline-exceeded` | 1 |
| a signal after the first hand-off, then a finished stage | `disposed`, null | `not-attempted`, `interrupted`, with its reconciliation (B-17) | `not-attempted`, `interrupted`, `reconciliation: null` | 130, 143 or 129 |
| a finished stage, then less than the floor at the spawn check | `disposed`, null | `not-attempted`, `deadline-exceeded`, with its reconciliation (B-17) | `not-attempted`, `deadline-exceeded` | 1 |
| no start, a preflight read that the floor or the deadline stops (B-34), any preflight outcome after a signal was received (B-41), or the check before the first hand-off fails (floor or signal) | `not-attempted`, `target-stopped` | `not-attempted`, `deadline-exceeded` or `interrupted`, `reconciliation: null` | likewise | 1, or the signal's |
| target refused at revalidation, or never reached | `not-attempted`, `target-stopped` | as change 1 | as change 1 | as change 1 |

Mapping a cache failure onto the target's `refused` with `state-changed`, rather
than new reasons, is CD-2, and the MODIFIED "Clean records a reconcilable result
for every removal target" widens its `refused` stage to name a cache stage that
ended `refused` or `partial` and gives the stage's deletions as the one
exception to "never ... delete a directory itself" (B-10); stopping the run is
CD-1. The same block's `not-attempted` stage now names a target whose cache
stage ended `disposed` and whose removal was not spawned, for a signal or the
floor, so that it does not also match a stage that ended `refused` or
`partial`, which the `refused` stage names (lane 3's re-read MEDIUM 2), and
such a target carries its reconciliation once its stage removed an entry
(B-17, lane 3's M2), so the carried rule "a `not-attempted` target SHALL carry
null" no longer contradicts the ADDED requirement. Its signal paragraph lets a
cache stage that has handed over its first removal run to its end, since one
that has not yet handed it over stops at the check before it (lane 3's
re-read LOW 1). The ceiling row is this design's reading of B-16: past 300 s
the work deadline has passed, so the later targets meet the floor, and the run
exits 1 as change 1's `removal-ceiling` does. The target itself is `refused`
with `state-changed`, not `removal-ceiling`, so the same block's exit table
names the case in its row 2, "a cache stage's removal reached the removal
ceiling", and an only or last target also exits 1 (lane 3's re-read MEDIUM 1,
B-27). The ADDED requirement's exit sentence says the same: 2 unless a signal,
the deadline or the removal ceiling decides it, and 1 when the floor or the
ceiling ended the stage unless a signal decides it, as the table's first two
rows order them (B-31, lane 3's delta read). The retry is a re-run: the
fresh plan enumerates the caches that remain, the revalidation and preflight run
again, and a persistent failure stops at the same target each time, which the
human line says (D11). A stage that the floor or the deadline stops in a read
before its first removal is no cache failure and is not mapped onto `refused`
(B-34): the target is `not-attempted` with `deadline-exceeded` and
`reconciliation: null`, as at the check before the first hand-off, the later
targets are `not-attempted` likewise, and the exit status is 1 by the deadline
row; the retry is the same re-run. Where a signal was received before the stage
classified any outcome of its preflight, a difference, an error, a byte total
past a cap, a read past its own 5 s budget or a stop by the floor or the
deadline, the stage is not mapped onto `refused` either (B-39, B-41): the target
is `not-attempted` with `interrupted` and `reconciliation: null`, the later
targets likewise, and the exit status is the signal's, 130, 143 or 129.

### D9. The platform check

Once per invocation, before any enumeration, a pure function checks
`hasattr(os, "O_NOFOLLOW")` and `hasattr(os, "O_DIRECTORY")`; `os.open`,
`os.stat`, `os.unlink`, `os.rmdir` and `os.access` in `os.supports_dir_fd`;
`os.stat` and `os.access` in `os.supports_follow_symlinks`; `os.access` in
`os.supports_effective_ids` (B-20); and `os.listdir` in `os.supports_fd`. False
makes every row that reaches the `ignored-local-files` rung holding ignored
records `cache-unsupported-platform` with null counts, runs no enumeration, and
leaves the batch as change 1's (CD-3). A row that an earlier rung classified
(`stale-worktree`, `protected-default`, `inspection-error` or `dirty`) keeps
that classification, and its sub-record, `not-candidate` where it holds ignored
records, as where the calls exist (B-37, Codex's P2 at
`specs/project-clean-review-safety/spec.md:383` on `e1049b2`): the check
withholds the cache proof and does not rewrite the ladder, whose order is a
function of the row's evidence alone, so a dirty worktree that also holds an
ignored file keeps the dirty advice, which is the actionable one, where "every
row holding ignored records" had forced it to `ignored-local-files`. The check
never falls back to a flag of 0, as `bb91a49` did. Tests stub it to false; CI
runs the real check and the descriptor scenarios on `ubuntu-latest` only (`test
(3.10)` and `test (3.12)`), so macOS's support is not verified by CI (L-12,
B-15), and where it is missing the check fails closed.

### D10. Revalidating a cache target

The targeted revalidation keeps change 1's order and its limit of five Git
children. In the target worktree, a target with listed caches runs the D3 child
instead of the combined probe: it must read no record other than ignored ones,
and its ignored records must be exactly the plan's `paths` as `[path, kind]`,
the trailing `/` of a directory record giving `directory`; the baseline
signature's `ignored_files` is recomputed from those records with the combined
probe's bound of 64. A difference, a failure or a timeout refuses the target
with `state-changed` (a value that cannot be re-read is a difference,
CAS/rs:92-93), before any cache is touched. The hidden-state probe follows as
before.

### D11. JSON and what the person sees

`cache_disposal` in the plan (worktree rows and `selected` entries) and in the
apply record (targets) is exactly as the ADDED requirement lists it, present
only where this change acts and absent otherwise, never `null` (L-10, B-13): on
a worktree row whose `ignored_files` is above 0, and on a `selected` entry and
an apply-result target whose plan lists at least one cache; the codes
are the sub-records' own: `reason` in the plan `not-candidate`, `cache-cap`,
`cache-unverified`, `cache-unwritable` (B-20) or `cache-unsupported-platform`;
`candidate_block` in the plan null or an existing class name or gate reason
(B-24); `stage` in the record `disposed`, `refused`, `partial` or
`not-attempted`, with `reason` null, `cache-changed`, `cache-partial` or
`target-stopped`. Every path is written by change 1's escaping rule with
`path_valid_utf8` beside it, which is always true in `paths` and `directories`,
since a cache path that is not valid UTF-8 is blocking, and can be false in
`blocking_samples`, as for the 0xFF path of "A symlink named like a cache is
never disposable" (lane 3's LOW 13). `limits` gains the five keys of D4. No
existing enum gains a value and `schema_version` stays 1 (CD-16).

The text is ASCII, pinned by the tests, with `PATH`, `CPATH`, `BPATH`, `ROOT`,
`N`, `E`, `B`, `D`, `K`, `C`, `U`, `W`, `CLASS`, `NEXT STEP` and `REASON`
substituted:

- Preview, under `  remove PATH [BRANCH]`: `    caches: N paths, E entries, B
  bytes; first: CPATH`.
- Preview, an `ignored-local-files` row, after change 1's `: N ignored; first:
  SAMPLE`: `; disposable D, blocking K; first blocking: BPATH` when the counts
  are established and `blocking` is above 0; `; disposable D, blocking 0; not
  disposed: REASON` for a row the invocation's totals left, and, for
  `cache-unwritable`, `; disposable D, blocking 0; not disposed:
  cache-unwritable; fix the ownership or mode of PATH, then re-run`, `PATH`
  being the worktree's (B-20); `; disposable unknown, blocking unknown
  (REASON)` when they are null, followed by `; first blocking: BPATH` when the
  sample test rejected a sample (D2), or by `; kept as CLASS: NEXT STEP` when
  the row has a `candidate_block`, `NEXT STEP` being change 1's next step for
  that class or gate (CAS design.md:751-760), so that the line names what
  really keeps the row and not the advice to delete its ignored files (B-24).
- The plain report, a row holding ignored records: one more line, `  caches:
  disposable D, blocking K` or `  caches: disposable unknown, blocking unknown
  (REASON)`, with the same `; kept as CLASS: NEXT STEP` ending.
- Success, after `Removed N; branches kept: B1, B2.`: `Caches disposed: N paths
  in K worktrees.` (`1 path` when N is 1, `1 worktree` when K is 1).
- The stall line (B-21), printed under the `ignored-local-files` group only
  when each of the first 16 candidates in canonical order is held at the rung
  for a persistent reason, any one of `blocking` above 0, `cache-cap` from a
  per-worktree cap, `cache-unverified` or `cache-unwritable`, the test never
  on `blocking` alone (B-32, D4), and built from those rows' reasons with
  every zero count left out, a `cache-cap` row counting as one past a
  per-worktree cap when its counts are null: `  these cache-cap rows will not
  drain while the 16 candidates
  ahead of them stay kept: K hold ignored files that are not caches (review
  them), C exceed a per-worktree cache cap (delete their caches, then re-run),
  U could not be enumerated (re-run; if it repeats, inspect them), W cannot be
  changed by this user (fix their ownership or mode, then re-run)`, in the form
  of change 1's index-gate line (CAS design.md:743-746). It never tells the
  person to remove by hand a worktree whose state was not established. The `W`
  part is this design's completion of B-21 for B-20's reason, since 16
  `cache-unwritable` rows stall the same way.
- A stop at a cache stage, before the stop block: `Cache disposal at PATH
  refused (cache-changed); nothing was deleted.`, printed only when no entry was
  removed and no removal is outstanding and, for a stage that ended before its
  first removal, no signal had been received by then (B-41); or `Cache disposal
  at PATH partial (cache-partial): removed K of N cache paths; remaining: C1,
  C2. A fresh plan lists the rest: project clean ROOT --all-safe`, with `; may
  still be removed: C3` after the remaining paths for a cache whose removal is
  still outstanding (B-16); or, when the work deadline ended the stage, `Cache
  disposal at PATH partial (cache-partial): the work deadline ended it after
  removing K of N cache paths; remaining: C1, C2. A fresh plan lists the rest:
  project clean ROOT --all-safe` (B-21), so that a deadline does not read as a
  change of state. The stop block that follows is change 1's, its reason the
  target's.
- A stop after a stage that ended `disposed` and before the spawn, before the
  stop block: `Cache disposal at PATH: removed N cache paths; the worktree was
  not removed.` (B-17).
- A stop at a target whose cache stage the floor or the deadline stopped in a
  read before its first removal, no signal having been received by then (B-39,
  B-41), before the stop block: `Cache disposal at PATH not attempted
  (deadline-exceeded); nothing was deleted.` (B-34), so that the deadline is
  named and a change of state is not claimed. The `refused` line above is
  printed only for a difference or a preflight error, with no signal received.
- The question is change 1's, unchanged (CD-15).

### D12. Time, threads and signals in the stage

The stage starts only while more than `removal_floor_seconds` of the work
deadline remains (D1). It runs its calls through one daemon worker thread per
stage, fed one call at a time, and treats the two kinds of call as change 1
does (B-16): its reads, as change 1 treats its identity reads (CAS
design.md:304-306), and its unlinks and directory removals, as change 1 treats
its removal child.

- A read (an open, a listing, an `lstat`) is waited for by the main thread with
  `min(5 s, work remaining - removal_floor_seconds)`. A read past that wait
  abandons the worker and ends the stage: `partial` after the first removal;
  before it, the slot is read first (B-39, B-41), and a signal recorded by then
  ends the stage `not-attempted` with the target `interrupted`, whichever wait
  it was; otherwise `refused` when 5 s was the wait, which holds when at least
  10 s of work remained, and `not-attempted` when the wait was the smaller `work
  remaining - removal_floor_seconds`, which is the deadline's limit, as it is
  when a read cannot start because no more than the floor remains (B-34).
- A removal is handed to the worker only while more than the floor remains,
  and the hand-off of the first one is the stage's first removal for every rule
  of the two ADDED requirements. A removal handed over is waited for until it
  returns, never abandoned at the per-call budget, and counts as a removal in
  flight for the run bound and for signals. Only the 300 s removal ceiling,
  counted from the hand-off, ends that wait; its cache is then `removed: null`
  and the stage ends `partial`, never `refused`. The reconciliation reserve
  counts from the return or from that ceiling.
- A worker with a call still outstanding gets no further call, and no
  descriptor given to an outstanding call is closed before `project` exits, so
  that `os.open`, which returns the lowest free number, never hands that number
  to a later chain or to the rescan. Without that rule a late `unlinkat`
  against a reused number could remove a same-named entry in a directory the
  plan never checked, as AE-1 reproduced.
- The rescan of a partial stage (D8) never runs on the stage's worker: each of
  its calls runs on a thread of its own, as a reconciliation probe under
  `min(5 s, reserve remaining)` (B-18).

The floor is therefore left for the spawn whenever every removal returns in
time, and the 64 s run bound keeps change 1's two exceptions, a removal in
flight, up to its ceiling, and a filesystem call stuck in the kernel. The
earlier design abandoned removals as well as reads; Codex's P1 on `3c08613`,
S-1 and AE-1 showed that an abandoned unlink could finish after the record had
said "nothing was deleted".

Signals keep change 1's handlers, which only record. The stage reads the slot
before its preflight and again immediately before the hand-off of its first
removal, after the preflight and once the first listed cache's chain is reopened
(D1, steps 2 and 3a, B-17), and not again until the spawn check, except that it
reads the slot when the preflight, or the reopening of that chain, reaches an
outcome, before it classifies it, whether a difference, an error, a byte total
past a cap, the end of a read's wait or a stop by the floor or the deadline
(B-39, B-41). The handler only records, so a signal received while a read is
held changes nothing until then, and without that read the target would be
reported `refused` with a change of state, or `not-attempted` with
`deadline-exceeded`, for a run that a signal had already stopped. A signal
recorded before that second check stops the target with nothing deleted; one
recorded after it is handled as one received during the removals, which finish,
and then stops the target before its spawn (CD-11): its caches are either
untouched or all removed, and a target whose caches were removed is
`not-attempted` with its reconciliation. Every check-then-act has a window like
this; masking signals around the check would only move it, since Python runs
handlers in the main thread between bytecodes.

### D13. The guarantee and the residual window

The stage removes an entry only if, at its preflight, the entry had the allowed
shape, its listed cache held its planned number of entries, and every directory
from the worktree root down to it carried its planned identity, and, at its
removal, the chain to it carried those identities again. For a cache target the
narrow guarantee's revalidation is D1's step 1, and the window it leaves,
ignored files created after it, covers a cache that Python writes again after
the stage: Git's non-force removal deletes it with the worktree
(`BA:319-323`). The MODIFIED "Cleanup states a narrow guarantee and its
residual window" states both, and gives the stage's guarantee as the one for
the cache entries it removes, beside the one for a worktree removal (B-10,
SA-2).

For a cache target the window is wider than change 1's (B-19, lane 3's M1,
S-3, AE-4). The last check that covers ignored files outside the listed caches
is that revalidation, before the stage, so an ignored file created during the
stage outside the listed caches, a `local.env` at the worktree root or an
editor's swap file, is deleted with the worktree by Git's non-force removal,
which deletes ignored files and refuses only untracked or modified ones
(`BA:319-321`). The packet's window is "one child start-up plus Git's own
status check, typically well under a second" (`BA:323-324`); a cache target's
adds the stage, which took about 0.25 s for 512 entries on this workstation
(AE-4's measurement, 2026-10-19), and which task 2.3 re-measures. A file placed
in a listed cache directory is still protected, since `rmdir` refuses a
directory that holds it (D7), which is the sense in which CD-18 calls the stage
safer. The window is stated, not closed: one combined status probe after each
`disposed` stage would close it at one Git child per cache target, at most 266
children and 16 removals, 39.9 s + 4.8 s = about 44.7 s at the packet's model
before any filesystem time. With the walk and the stages at B-25's bound
through one worker (D4), it costs about one target: each earlier cache target
delays target k by 0.15 s more, and 16 cache targets and an 8,192-entry walk
cannot come together, since 16 selected targets hold the walk to the 4,096
entries they list. With 16 cache targets the 15th arrives at 40.5 + 2.1 + 1.0
+ 1.9 = about 45.5 s, and with 8 cache targets ahead of it and 8,192 entries
walked at 40.5 + 1.2 + 2.0 + 1.9 = about 45.6 s, under the floor either way,
while the 14th arrives by about 44.6 s: 14 of 16 targets reach their stage,
against 15 of 16 without the probe. Under #23's flag B-19 put the probe's
cost at about one target fewer than #23's 13 of 16 at `ca96701`, 12, with the
cache-stage filesystem time excluded; #26 restates its own count under A-23
and A-24, which D4 gives (B-35). That would buy a window that concurrent
writers, outside the contract, alone can use (B-19; proposal, Decisions).

When the plan selects a cache target, change 1's residual-window line becomes
`Not protected: ignored files created or index flags set after the last check
or during a cache stage, caches recreated after it, and any change after Git's
own check.`; otherwise it is change 1's line, unchanged.

### D14. Tests

The deltas hold 55 scenarios in `project-clean` (5 classification, 14 retire,
11 batch, 6 bounds, 8 reconcilable result and 11 ADDED), 28 in
`project-clean-review-safety` (6 preservation, 11 revalidation, 4 narrow
guarantee and 7 ADDED, B-26's among them) and 8 in `project-overview` (the one
MODIFIED block of B-14). The new ones, 1 + 1 + 1 + 11 + 1 + 1 + 1 + 7 + 1 = 25,
each get a test
named after it. Of the 66 carried ones, which keep the tests of features 004
and 005, 62 are byte-exact and four are edited, each to name its ignored file
as not a Python bytecode cache: "Ignored-file bound" and "A merged worktree has
ignored local files", as before, and, under B-22 and lane openRepoProject-4's
precision, change 1's "Every protected classifier" in the batch block and
change 2's "Every protected classifier" in the overview block, whose THEN
would otherwise fail on a fixture whose ignored files are caches (lane 3's
LOW 11). The overview edit departs from B-14's "plus one scenario", and lane 4
agreed it on 2026-10-19 with the rest of B-22. The new tests' names begin
`test_clean_`, so that feature 004's `git-floor` job, which runs `-k
test_clean_ -k test_status_ -k test_doctor_` with Git 2.36.6 first on PATH,
runs them (S-4, `clarifications.md`). The deferred
scenario of `BA:1632-1634` is covered by "A symlink named like a cache is never
disposable", "An ancestor swapped for a symlink before the stage", "A partial
cache phase" and "A file placed in a cache directory during the stage".

- Fixtures write `.pyc` and `.pyo` bytes directly, so no compiler runs, under
  explicit ignore rules (`__pycache__/` with `*.py[co]`, or `*.pyc` alone, or
  `__pycache__` for the symlink case) in the worktree's `.gitignore` or
  `info/exclude`; the 256 MiB cap uses sparse files made by `os.truncate`.
- Hooks: between the revalidation and the stage, after the preflight, while
  the first listed cache's chain is reopened, before the n-th hand-off, and on
  the n-th unlink, holding it or making it fail, through `patch.object` on the
  stage's call table, the removal ceiling patched short; `os.close` stubbed to
  record the numbers the stage closes, so that a test can assert that no
  number given to an outstanding call is reused; the stage's and the walk's
  call tables counting their opens, so that a test asserts one chain per
  directory holding a listed path in each pass and one open per recorded
  directory in the walk (B-33); a preflight read held until the budget that
  the patched clock leaves to the deadline is spent, or until no more than the
  floor remains, against the same read held past 5 s with at least 10 s
  remaining (B-34, B-38), and each of them again with SIGINT delivered while
  it is held, and a preflight that finds a changed entry again with SIGINT
  delivered before it does, in each of these the stage then `not-attempted`,
  the target `interrupted` and the exit status 130, never `refused` (B-39,
  B-41); the access check stubbed to false where the runner is root; the
  platform check stubbed to false; the counting `git` wrapper of change 1 for
  the enumeration's argument vector, directory and count.
- Every existing test keeps passing, among them
  `test_clean_preserves_ignored_files_in_an_otherwise_merged_worktree`
  (tests:949, `local.env`) and feature 004's tests, whose fixtures hold no
  cache; a feature 004 test whose fixture holds a cache, should one exist when
  this feature starts, is listed in its plan and its fixture changes to a
  non-cache ignored file, as change 1's "Every protected classifier"
  (CAS/pc:670-683), edited in this change's MODIFIED batch block, now says.
- Once feature 005 has landed, any of its tests asserting that the overview
  and `project clean` classify identically, "Every protected classifier"
  among them, gets the cache case excluded in this change's realization (its
  `ignored-local-files` fixture row given a non-cache ignored file, as the
  edited overview scenario now says, or a cache-only row left out of the
  equality check), never in feature 005 (B-14); the new overview scenario pins
  the exception itself.
- `python3 -m unittest discover -s tests -v`, which CI runs as `test (3.10)`
  and `test (3.12)` on `ubuntu-latest`; macOS is not verified by CI (L-12).

## Risks / Trade-offs

- [A `.gitignore` that names `*.pyc` but not `__pycache__/` lists every cache
  file as its own record, so a large tree reaches 512 records sooner] -> The row
  stays `ignored-local-files` with `cache-cap` and the plan stays complete; the
  stage leaves empty `__pycache__` directories for Git's removal to delete with
  the worktree.
- [A worktree with more than 512 recorded cache objects, or 256 MiB, is never
  disposed of by `project`] -> It is preserved as change 1 preserves it, and
  its preview says `cache-cap`; the person deletes the caches and re-runs.
- [A cache tree that is deep and spread over many directories] -> Every
  directory the plan records counts toward the 512 objects, the walk opens each
  once, and the stage opens one chain per directory with removals in each pass
  (B-33), so the work is bounded; but depth times those directories can reach
  43,947 opens a pass for one target, which no fit holds, so until Brett Heap
  answers the Open Question on a limit for them, such a target takes its run
  to the floor and ends `partial`, exit 1, never unsafe, each run removing
  part of its caches (D4).
- [Python running in the worktree between the plan and the stage rewrites
  caches] -> A new cache refuses at revalidation, a replaced directory at the
  preflight, a new file in a listed directory refuses at the preflight, or
  ends the stage `partial` when it arrives after it; a re-run plans afresh. A
  `.pyc` recompiled in place changes nothing (D5), unless its growth takes the
  target past 256 MiB or the run's byte total past 1 GiB, which its preflight
  refuses with nothing deleted (B-26).
- [Sixteen candidates that each keep a blocking path the samples did not show
  sort first, so no run enumerates a later cache-only candidate] -> The sample
  test keeps out every row whose samples show a blocking name (D2); the rest is
  a stall the human report names, as change 1 names its index-gate stall, with
  how many of the 16 stay for each cause and each cause's next step (B-21),
  never advising the person to remove by hand a worktree whose state was not
  established (D4, D11).
- [A partial phase leaves some caches removed and the worktree in place] ->
  `__pycache__` entries are regenerable; a loose `.pyc` may be sourceless,
  since Python 3 writes bytecode only into `__pycache__/` and a loose one is
  what Python 2 or `compileall -b` left, imported when its source is absent.
  Each path is reported removed, remaining or not established, and a re-run
  finishes the job or stops at the same place with the same report.
- [A `__pycache__` the user cannot change, such as one a root-run container
  wrote] -> The plan's access check keeps the row `cache-unwritable`, not
  selected and stopping nothing, its line saying to fix the ownership or mode
  and re-run (B-20). Only a failure the check cannot see, a sticky directory
  or a read-only filesystem, stops the run at that target, `refused` with
  `cache-changed` and nothing deleted, and the human line names it each time.
- [The overview reads a cache-proven row as `ignored-local-files` where
  `project clean` reads it `merged-removable`, whether or not `project clean`
  then excludes it] -> The safe direction: its suggestion is the read-only
  report, which shows the row's state, and change 2's equality clause states
  the exception as B-22 words it, the edit agreed by lane openRepoProject-4
  (B-14, B-22; `tasks.md` 2.2).
- [A filesystem call stuck in the kernel during the stage] -> A read is
  abandoned after its budget and ends the stage `refused` or `partial`, or
  `not-attempted` where the deadline set the budget, or a signal was received,
  before any removal (B-34, B-39); a removal is waited for up to the 300 s
  removal ceiling, as a removal child is, its cache then `removed: null`; the
  worker gets no further call and its descriptors stay open until `project`
  exits, and the rescan, on threads of its own, records `removed: null` where it
  cannot tell (D12).
- [An ignored file created outside the listed caches during a cache stage is
  deleted with the worktree] -> The residual-window line names it; the stage
  took about 0.25 s for 512 entries here, and concurrent writers are outside
  the contract (D13, B-19).
- [The change frees fewer rows than its first evidence suggested: of the 37
  merged, clean, published rows kept for ignored files measured on 2026-10-19,
  13] -> `.pytest_cache`, which alone keeps 16 more, is before Brett Heap with
  a recommendation to admit it here (B-23; proposal, Open Questions).
- [Bind mounts and other devices inside a worktree] -> A cache path or a
  directory above it on another device is blocking (CD-8), so disposal never
  reaches a mounted tree.
- [Case-insensitive filesystems and temporary names] -> Only exact names count;
  anything else is blocking, so the row is kept.
- [#23, which archives after this change, must carry five blocks re-based on
  this change's archived text] -> Dependencies and Sequencing names each of
  them, and #23's own tasks re-base them before it archives (L-11, A-13).
- [The descriptor calls are verified here on Linux only, and CI runs on Linux
  only] -> D9's check fails closed on any platform without them; macOS is not
  verified by CI (L-12).

## Migration Plan

1. Ratification by Brett Heap's word on this change's pull request (`tasks.md`
   1.6), with the five Open Questions of `proposal.md` before him; an answer
   admitting `.pytest_cache` adds it to the deltas before ratification (B-23),
   and so does one adopting the limit on the stage's directory opens (B-33).
2. Before the Speckit handoff (`tasks.md` section 2): change 1 archived after
   feature 004 merges, with PR #19's amendment of change 1 landed (L-16), or
   PR #19 closed, and the two blocks written on its text re-checked; lane
   openRepoProject-4's agreement on the `project-overview` delta's diff, given
   on 2026-10-19 for `b4d3e12`, and again on B-22's diff before its commit as
   `9f30fb9` (B-14, B-22), and its byte check of B-30's `4d5855a`, given on
   2026-10-20 (B-30, B-36); the enumeration, the walk and the stage measured
   (task 2.3).
3. Local `main` is synced to `origin/main`, then `/speckit.specify` creates the
   one feature under the next free number, 006 or later, recorded once in
   `tasks.md` under "Speckit Handoff"; `/opsx:apply` runs only then.
4. The feature implements D1 to D14 on feature 004's code, merging `main` into
   its branch as `main` moves and never rebasing.
5. README: the "Clean up Git worktrees" section gains the cache paragraph: what
   is disposed of and what blocks, the caps, the residual window, the partial
   phase and its re-run.
6. Tests per D14, the feature 005 exclusion included once feature 005 has
   landed.
7. The realization PR merges with green checks on every job of the workflow on
   its base, feature 004's `git-floor` job included beside `test (3.10)` and
   `test (3.12)` on `ubuntu-latest`, and closes issue #24 (S-4).
8. The change is archived after that merge and after the archives of change 1
   and change 2. Before `/opsx:archive`, its `project-overview` block is
   re-read against main's text of "Overview reuses the cleanup classifier and
   merge target" and re-copied from it, keeping any amendment of change 2 that
   landed there meanwhile, such as lane openRepoProject-4's planned one for
   feature 005's open Q7 A, which the archive would otherwise drop silently,
   since a MODIFIED block replaces its requirement whole; a `diff -u` of main's
   block against this change's shows additions only, and the validation passes
   again (B-29, `tasks.md` 3.2). `add-project-clean-branch-retirement` archives
   after this change, writing its blocks of the five requirements both changes
   modify on this change's archived text.

Rollback: revert the realization commit on `main`. `__pycache__` entries
already disposed of are written again by Python on the next import; a loose
`.pyc` already disposed of may have been sourceless and is not written again
(B-17). A worktree already removed stays removed as under change 1, its branch
kept; installed `project` artifacts follow workBenches' pin.

## Open Questions

The five questions of `proposal.md` are before Brett Heap: enum closure and
`schema_version`, `.pytest_cache`, the other cache kinds, the caps, and a limit
on the cache stage's directory opens (B-33). Change 2's equality clause, the
fourth in the draft, is settled by B-14 and B-22. The deltas implement each
recommendation but two: `.pytest_cache`, which recommends admitting it in this
change, and the opens limit, which recommends a new per-worktree cap; each is
added only on his answer (B-23, B-33), and no cap changes before it. A
different ruling edits the deltas before ratification. No other question
changes what is built.
