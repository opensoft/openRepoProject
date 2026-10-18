Lane: openRepoProject-5

# Design

## Context

See `proposal.md` for why and what, and the deltas under `specs/` for the
requirements. Citations follow the proposal's key: the packet at `da33d92`
(`BA`, `SY`, `OV`, `HO`), change 1 (`CAS`, `CAS/pc`, `CAS/rs`, `CAS/cmd`) and
change 2 (`APO`, `APO/ov`) at `961c405`, draft PR #19 at `c462d87` (`PR19/pc`,
`PR19/rs`), and `project:N` at `961c405`; main is now `e9d6711`, with the same
`openspec/`, `ideation/` and `project` (L-15). The lane's rulings are L-1 to
L-15 and B-1 to B-15, and A-9 for #23; this change's own decisions are CD-1 to
CD-18 in `proposal.md`, and the alignment review's findings (SA-n, QA-n, G1 to
G5) are resolved in its table. No council has run yet, so there is no
`clarifications.md` and no NOTED item to answer; the lane adds one if the
council notes any.

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
| B-14 | the overview's equality clause excepts the cache case | D6, D14 |
| L-12, B-15 | CI on Linux only; macOS not verified by CI | D9, D14 |

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

- Any cache kind but `__pycache__`, `.pyc` and `.pyo`; any disposal without the
  worktree's removal; any change to `status`, `doctor` or what `project
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
3. the whole-list preflight (D7);
3a. the floor and slot checks of step 2 again, with the same outcome;
4. the removals (D7), then, on any failure, the rescan (D8);
5. change 1's floor and slot checks, then the spawn, the wait and the
   reconciliation, unchanged.

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

The walk then runs per directory record, top-down: open the record's directory
by a descriptor chain from the worktree root (D7), list it, `lstat` each entry
relative to it, and descend into each entry named `__pycache__` that is a
directory, counting entries and summing the regular files' `st_size`, stopping
at the first entry outside the shape or at the per-worktree caps.

### D4. The caps and the fit

| Limit | Value | Scope | Reached |
| --- | --- | --- | --- |
| `cache_rows` | 16 | enumerations per invocation | later candidates `cache-cap` |
| `cache_entries` | 512 | Git records, and cache entries, per worktree | `cache-cap` |
| `cache_bytes` | 268,435,456 (256 MiB) | `lstat` sizes of regular files per worktree | `cache-cap` |
| `cache_entries_total` | 4,096 | cache entries over the invocation's cache-only rows | that row `cache-cap`, its entries uncounted |
| `cache_bytes_total` | 1,073,741,824 (1 GiB) | bytes, likewise | likewise |

A cap reached keeps the row `ignored-local-files` and the plan complete, so the
batch removes everything else, and a later run takes the rest unless each of
the 16 enumerated candidates stays at the rung. A candidate left at the rung
keeps its place among the 16, as change 1's index gates keep theirs, so a run
whose 16 enumerations all stay at the rung is a stall that every re-run
repeats, and the human report names it as change 1 names the index-gate stall.
The sample test (D2) keeps out every row whose samples show a blocking name;
what can still stall is a candidate whose samples all have cache names while it
holds a blocking path beyond its 8 samples, a cache-named path that is blocking
by its type, contents or device (a symbolic link named `__pycache__`, a
`__pycache__` holding `notes.txt`, a mount), more than a per-worktree cap
allows, or an enumeration that fails each time. Bytes are the apparent sizes
that `lstat` reports at plan time; a sparse file counts at its apparent size,
which only errs toward a cap.

The fit is change 1's (CAS design D14; `BA:729-735`) at 150 ms per Git child and
0.3 s per removal, with the enumerations added:

| Mode | Children | Time | Fits the 50 s work deadline |
| --- | --- | --- | --- |
| all-safe, 128 rows, 16 enumerations, 16 targets | 7 + 128 + 16 + 16 + 80 + 3 = 250, and 16 removals | 37.5 s + about 4.8 s = 42.3 s | yes; the 16th target reaches its cache stage after 247 children and 15 removals, at about 41.55 s, with 8.45 s left |
| report, 256 rows | 7 + 256 + 16 + 16 = 295 | 44.25 s | yes |
| single, 128 rows plus P | 7 + 129 + 1 + 1 + 5 + 3 = 146, and 1 removal | 21.9 s + about 0.3 s | yes |
| all-safe, one enumeration per candidate (no `cache_rows`) | 7 + 128 + 127 + 16 + 80 + 3 = 361 | 54.15 s + 4.8 s | no |
| report, likewise | 7 + 256 + 255 + 16 = 534 | 80.1 s | no |

The last two rows are why CD-6 adds `cache_rows`. A cache stage spawns no child;
its filesystem calls are about two per cache entry (a listing or `lstat` at the
preflight, an unlink or directory removal after it) plus the directory opens,
so at most about 1,100 calls for 512 entries and about 8,500 for the 4,096 of a
run. Through one daemon worker per stage (D12), whose hand-off costs tens of
microseconds a call, that is tenths of a second in a run, inside the margin the
table leaves. Governance task 2.3 measures the enumeration and the stage before
the handoff, as change 1's task 2.1 measured its probes; a measured cost that
breaks the fit lowers `cache_rows` in steps of 4 and the entry caps in powers of
two before the feature starts. The fit sentence of the bounds block counts the
Git children and states the stage's filesystem calls as outside it, and a
target whose stage or spawn cannot start under the floor is `not-attempted`
with `deadline-exceeded` as for every removal (QA-5), so the 8.45 s margin of
the first row is design arithmetic, not a promise of the spec.

With `--retire-branches` (#23) a run spawns branch children too. At the
packet's 150 ms model only 13 of 16 targets then reach their stage before the
removal floor, and change 1's deadline rule defers the rest to the next run
(exit 1, never unsafe); at change 1's measured costs all 16 fit. #23, which
archives after this change, states that joint fit (A-9, the alignment review's
G3).

### D5. Planned identities and the digest

The plan records, for each candidate whose enumeration finished, every
directory the stage will open below the worktree root: each directory on the way
down to a listed cache, each listed cache directory and each nested
`__pycache__` directory, as `{path, path_valid_utf8, dev, ino}`, the device and
inode from an `lstat` that follows no symbolic link. The worktree root's own
identity is change 1's `{path, dev, ino, admin_id}` of the selected entry.

Files carry no identity. Unlinking a name inside a directory whose identity was
just checked can only remove that name: a file replaced by a symbolic link loses
only the link, and a hard link only its name in the worktree. Python writes a
`.pyc` by renaming a temporary file over it, so a file's inode changes whenever
Python recompiles, and an identity in the plan would refuse `--expect-plan` and
the preflight for no safety gain. Each listed file is instead checked for its
type at the preflight, and each listed cache for its planned number of entries
(D7, QA-1): a `.pyc` written into a listed directory adds an entry and
refuses, while a `.pyc` recompiled in place keeps the count and passes. A file
renamed within a listed directory keeps the count too; it is an allowlisted
cache either way, so the stage still removes nothing but caches.

The canonical text of `plan_digest` is change 1's (CAS design D7, D14): the four
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
lane openRepoProject-4's two sentences, which except that case and forbid the
overview to classify as removable a worktree that `project clean` would refuse,
and it is committed once lane 4 agrees its diff (`tasks.md` 2.2). Feature
005's spec (`specs/005-project-overview/spec.md` on
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
the realpath and identity comparison. The stage handles one listed cache at a
time and closes its chain before the next, so at most the path's depth plus two
descriptors are open at once, far below any platform's default descriptor
limit.

The preflight, before any removal: for each listed cache in canonical order,
open its chain, checking every identity; for a directory, list it and `lstat`
each entry relative to it, require the allowlisted shape, require each nested
`__pycache__` to carry its planned identity, require the cache to hold exactly
its planned number of entries, and record the names to remove; for a file,
`lstat` it relative to its parent and require a regular file with an allowed
suffix; and keep the running byte total within the per-worktree cap. Any
`OSError` (`ENOTDIR` or `ELOOP` from a swapped symlink,
`ENOENT`, `EACCES`), any identity, shape or entry-count difference, the byte
cap exceeded, or a call past its budget ends the stage `refused` with
`cache-changed`. This is the
whole-list check that PR #2's open thread 3989548481 asked for: no path is
removed until every path has passed.

The removals: for each listed cache in canonical order, open its chain again,
checking every identity again; remove the names fixed at the preflight,
depth-first, files by `os.unlink(name, dir_fd=directory)` and each emptied
nested directory by `os.rmdir(name, dir_fd=parent)`, then the listed directory
by `os.rmdir` relative to its parent; a listed file by `os.unlink` relative to
its parent. Nothing listed after the preflight is removed, and `rmdir` refuses a
directory that holds anything else, so a file placed in a cache directory at any
time before that directory's removal survives (Context, `ENOTEMPTY`) and ends
the stage `partial`. No recursive deletion, no `shutil.rmtree`, no path-name
deletion and no child process is used.

### D8. The partial phase and the target's result

After the first removal, any failure (an `OSError` from an unlink, a removal or
a chain open, `ENOENT` included, since something else is changing the worktree),
a call past its budget, or the removal floor reached ends the removals. The
stage then rescans each listed cache: it opens the chain to the cache's parent
as in D7 and `lstat`s the cache's name relative to it with
`follow_symlinks=False`; absent is `removed: true`, present `removed: false`,
and a chain that no longer opens, or a call past its budget, `removed: null`.
Its `cache_disposal` is `partial` with `cache-partial`, the planned `entries`
and the `entries_removed` counted as they succeeded.

| Stage outcome | `cache_disposal` | Target | Later targets | Exit (first matching row of change 1's table) |
| --- | --- | --- | --- | --- |
| every listed cache removed | `disposed`, null | the sequence goes on to the spawn | as change 1 | as change 1 |
| preflight difference | `refused`, `cache-changed`; each `removed` false where the preflight found the path, null where it did not | `refused`, `state-changed`, reconciliation, nothing spawned | `not-attempted`, `batch-stopped` | 2 |
| failure after the first removal | `partial`, `cache-partial` | likewise | likewise | 2 |
| the floor reached after the first removal | `partial`, `cache-partial` | likewise | `not-attempted`, `deadline-exceeded` | 1 (the deadline stopped work) |
| a signal, then a finished stage | `disposed`, null | `not-attempted`, `interrupted` | `not-attempted`, `interrupted` | 130, 143 or 129 |
| no start (floor or signal) | `not-attempted`, `target-stopped` | `not-attempted`, `deadline-exceeded` or `interrupted` | likewise | 1, or the signal's |
| target refused at revalidation, or never reached | `not-attempted`, `target-stopped` | as change 1 | as change 1 | as change 1 |

Mapping a cache failure onto the target's `refused` with `state-changed`, rather
than new reasons, is CD-2, and the MODIFIED "Clean records a reconcilable result
for every removal target" widens its `refused` stage to name a cache stage that
ended `refused` or `partial` and gives the stage's deletions as the one
exception to "never ... delete a directory itself" (B-10); stopping the run is
CD-1. The retry is a re-run: the
fresh plan enumerates the caches that remain, the revalidation and preflight run
again, and a persistent failure stops at the same target each time, which the
human line says (D11).

### D9. The platform check

Once per invocation, before any enumeration, a pure function checks
`hasattr(os, "O_NOFOLLOW")` and `hasattr(os, "O_DIRECTORY")`; `os.open`,
`os.stat`, `os.unlink` and `os.rmdir` in `os.supports_dir_fd`; `os.stat` in
`os.supports_follow_symlinks`; and `os.listdir` in `os.supports_fd`. False makes
every row holding ignored records `cache-unsupported-platform` with null counts,
runs no enumeration, and leaves the batch as change 1's (CD-3). The check never
falls back to a flag of 0, as `bb91a49` did. Tests stub it to false; CI runs
the real check and the descriptor scenarios on `ubuntu-latest` only (`test
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
`cache-unverified` or `cache-unsupported-platform`; `stage` in the record
`disposed`, `refused`, `partial` or `not-attempted`, with `reason` null,
`cache-changed`, `cache-partial` or `target-stopped`. Every path is written by
change 1's escaping rule with `path_valid_utf8` beside it (always true, since a
cache path that is not valid UTF-8 is blocking). `limits` gains the five keys of
D4. No existing enum gains a value and `schema_version` stays 1 (CD-16).

The text is ASCII, pinned by the tests, with `PATH`, `CPATH`, `BPATH`, `ROOT`,
`N`, `E`, `B`, `D`, `K` and `REASON` substituted:

- Preview, under `  remove PATH [BRANCH]`: `    caches: N paths, E entries, B
  bytes; first: CPATH`.
- Preview, an `ignored-local-files` row, after change 1's `: N ignored; first:
  SAMPLE`: `; disposable D, blocking K; first blocking: BPATH` when the counts
  are established and `blocking` is above 0; `; disposable D, blocking 0; not
  disposed: REASON` for a row the invocation's totals left; `; disposable
  unknown, blocking unknown (REASON)` when they are null, followed by `; first
  blocking: BPATH` when the sample test rejected a sample (D2).
- The plain report, a row holding ignored records: one more line, `  caches:
  disposable D, blocking K` or `  caches: disposable unknown, blocking unknown
  (REASON)`.
- Success, after `Removed N; branches kept: B1, B2.`: `Caches disposed: N paths
  in K worktrees.` (`1 path` when N is 1, `1 worktree` when K is 1).
- When each of the 16 enumerated candidates stayed at the rung, under the
  `ignored-local-files` group: `  these cache-cap rows will not drain while the
  16 rows ahead of them keep ignored files that are not caches; review those
  worktrees, then remove them yourself`, in the form of change 1's index-gate
  line (CAS design.md:743-746).
- A stop at a cache stage, before the stop block: `Cache disposal at PATH
  refused (cache-changed); nothing was deleted.` or `Cache disposal at PATH
  partial (cache-partial): removed K of N cache paths; remaining: C1, C2. A
  fresh plan lists the rest: project clean ROOT --all-safe`.
- The question is change 1's, unchanged (CD-15).

### D12. Time, threads and signals in the stage

The stage starts only while more than `removal_floor_seconds` of the work
deadline remains (D1). It runs its calls through one daemon worker thread per
stage, fed one call at a time, each waited for by the main thread with
`min(5 s, work remaining - removal_floor_seconds)`: a call past that wait
abandons the worker, as change 1 abandons a filesystem call stuck in the kernel,
and ends the stage, `refused` before the first removal and `partial` after it.
The floor is therefore always left for the spawn, and the run bound of 64 s
keeps its one exception, a call stuck in the kernel.

Signals keep change 1's handlers, which only record. The stage reads the slot
before its preflight and again before its first removal (D1, steps 2 and 3a),
and not again until the spawn check, so a signal during the preflight stops the
target with nothing deleted, and a signal during the removals lets them finish
and then stops the target before its spawn (CD-11): its caches are either
untouched or all removed.

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
SA-2). When the plan selects a cache target, change 1's
residual-window line becomes `Not protected: ignored files created or index
flags set after the last check, caches recreated after the cache stage, and any
change after Git's own check.`; otherwise it is change 1's line, unchanged.

### D14. Tests

The deltas hold 54 scenarios in `project-clean` (5 classification, 14 retire,
11 batch, 6 bounds, 8 reconcilable result and 10 ADDED), 26 in
`project-clean-review-safety` (6 preservation, 11 revalidation, 4 narrow
guarantee and 5 ADDED) and 8 in `project-overview` (the one MODIFIED block of
B-14). The new ones, 1 + 1 + 1 + 10 + 1 + 1 + 1 + 5 + 1 = 22, each get a test
named after it; the carried ones keep the tests of features 004 and 005, the
14 retire, 10 batch, 8 reconcilable result, 3 narrow guarantee and 7 overview
scenarios all byte-exact; and the two edited ones are the ignored-file
scenarios whose files are named as not caches. The deferred
scenario of `BA:1632-1634` is covered by "A symlink named like a cache is never
disposable", "An ancestor swapped for a symlink before the stage", "A partial
cache phase" and "A file placed in a cache directory during the stage".

- Fixtures write `.pyc` and `.pyo` bytes directly, so no compiler runs, under
  explicit ignore rules (`__pycache__/` with `*.py[co]`, or `*.pyc` alone, or
  `__pycache__` for the symlink case) in the worktree's `.gitignore` or
  `info/exclude`; the 256 MiB cap uses sparse files made by `os.truncate`.
- Hooks: between the revalidation and the stage, after the preflight, and on
  the n-th unlink, through `patch.object` on the stage's call table; the
  platform check stubbed to false; the counting `git` wrapper of change 1 for
  the enumeration's argument vector, directory and count.
- Every existing test keeps passing, among them
  `test_clean_preserves_ignored_files_in_an_otherwise_merged_worktree`
  (tests:949, `local.env`) and feature 004's tests, whose fixtures hold no
  cache; a feature 004 test whose fixture holds a cache, should one exist when
  this feature starts, is listed in its plan and its fixture changes to a
  non-cache ignored file, since change 1's "Every protected classifier"
  (CAS/pc:670-683), carried byte-exact in this change's MODIFIED batch block,
  holds only for one.
- Once feature 005 has landed, any of its tests asserting that the overview
  and `project clean` classify identically, "Every protected classifier"
  among them, gets the cache case excluded in this change's realization (its
  `ignored-local-files` fixture row given a non-cache ignored file, or a
  cache-only row left out of the equality check), never in feature 005 (B-14);
  the new overview scenario pins the exception itself.
- `python3 -m unittest discover -s tests -v`, which CI runs as `test (3.10)`
  and `test (3.12)` on `ubuntu-latest`; macOS is not verified by CI (L-12).

## Risks / Trade-offs

- [A `.gitignore` that names `*.pyc` but not `__pycache__/` lists every cache
  file as its own record, so a large tree reaches 512 records sooner] -> The row
  stays `ignored-local-files` with `cache-cap` and the plan stays complete; the
  stage leaves empty `__pycache__` directories for Git's removal to delete with
  the worktree.
- [A worktree with more than 512 cache entries, or 256 MiB, is never disposed of
  by `project`] -> It is preserved as change 1 preserves it, and its preview
  says `cache-cap`; the person deletes the caches and re-runs.
- [Python running in the worktree between the plan and the stage rewrites
  caches] -> A new cache refuses at revalidation, a replaced directory at the
  preflight, a new file in a listed directory refuses at the preflight, or
  ends the stage `partial` when it arrives after it; a re-run plans afresh. A
  `.pyc` recompiled in place changes nothing (D5).
- [Sixteen candidates that each keep a blocking path the samples did not show
  sort first, so no run enumerates a later cache-only candidate] -> The sample
  test keeps out every row whose samples show a blocking name (D2); the rest is
  a stall the human report names, as change 1 names its index-gate stall, and
  the person keeps or removes those rows by hand (D4).
- [A partial phase leaves some caches removed and the worktree in place] ->
  Caches are regenerable, each path is reported removed or remaining, and a
  re-run finishes the job or stops at the same place with the same report.
- [A persistent cache failure, such as a `__pycache__` the user cannot write,
  stops every run at that target, holding back the targets after it] -> The
  human line names it each time; the person fixes the permission or removes the
  worktree by hand, as change 1's stalled index gates require.
- [The overview reads a cache-only candidate as `ignored-local-files` where
  `project clean` reads it `merged-removable`] -> The safe direction: its
  suggestion is the read-only report, which shows the row selectable, and
  change 2's equality clause states the exception, as lane openRepoProject-4
  asked (B-14; `tasks.md` 2.2).
- [A filesystem call stuck in the kernel during the stage] -> Its worker is
  abandoned after its budget and the stage ends `refused` or `partial`; the
  rescan records `removed: null` where it cannot tell, as change 1 records a
  stuck call.
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
   1.6), with the three Open Questions of `proposal.md` before him.
2. Before the Speckit handoff (`tasks.md` section 2): change 1 archived after
   feature 004 merges, with PR #19 landed or closed and the two blocks written
   on its text re-checked; lane openRepoProject-4's agreement on the
   `project-overview` delta's diff, which is then committed (B-14); the
   enumeration and the stage measured (task 2.3).
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
7. The realization PR merges with green checks on CI's two jobs, `test (3.10)`
   and `test (3.12)` on `ubuntu-latest`, and closes issue #24.
8. The change is archived after that merge and after the archives of change 1
   and change 2; `add-project-clean-branch-retirement` archives after this
   change, writing its blocks of the five requirements both changes modify on
   this change's archived text.

Rollback: revert the realization commit on `main`. Caches already disposed of
are written again by Python on the next import, and a worktree already removed
stays removed as under change 1, its branch kept; installed `project` artifacts
follow workBenches' pin.

## Open Questions

The three questions of `proposal.md` are before Brett Heap: enum closure and
`schema_version`, other cache kinds, and the caps. Change 2's equality clause,
the fourth in the draft, is settled by B-14. The deltas implement each
recommendation, and a different ruling edits the deltas before ratification.
No other question changes what is built.
