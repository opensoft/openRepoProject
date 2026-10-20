Lane: openRepoProject-5

# Proposal: add-project-clean-cache-disposal

Status: draft; alignment review and council resolved on PR #27; ratification
by Brett Heap pending; lane openRepoProject-3's re-read and Codex's findings of
2026-10-20 resolved in round B3 (B-25 to B-28), lane openRepoProject-4's
re-align step and wording, lane 3's delta read and Codex's re-review of
`cf57956` resolved in round B4 (B-29 to B-33), and Codex's re-review of
`e1049b2` with the lead's rulings of 2026-10-20 resolved in round B5 (B-34 to
B-37), lane 4's byte check of B-30's overview commit recorded in `tasks.md`
2.2, and lane 3's folded read of `cf57956..fffc194` with Codex's finding on
`fffc194` resolved in round B6 (B-38 to B-40); nothing here is ratified.
Governing issue:
opensoft/openRepoProject#24, claimed by lane
openRepoProject-5 (comment 6111257933); refs #6, the record of the project
maintenance design packet. Proposed on Brett Heap's word "usage reset, resume
all. read handoff and resume and fan out wide and do as much as possible in
parallel" (2026-10-11), read by lanes openRepoProject-4 and openRepoProject-5
as a go for the candidate list they put to him.

Citations are `file:line` at `da33d92`, which equals `961c405` for
`ideation/`. `BA`, `SY`, `OV` and `DI` are the packet's `project-maintenance-`
files `batch-cleanup.md`, `synthesis-inspect-and-retire.md`, `overview.md` and
`project-discovery.md`, and `HO` is its
`next-session-project-maintenance-fix-handoff.md`. `CAS` is
`openspec/changes/add-project-clean-all-safe/` (change 1) and `APO` is
`openspec/changes/add-project-overview/` (change 2), both ratified and
unarchived at `961c405`; main is now `e9d6711`, whose `openspec/`, `ideation/`
and `project` equal `961c405`'s (L-15). `CAS/pc`, `CAS/rs`, `CAS/cmd` and
`APO/ov` are their `project-clean`, `project-clean-review-safety`,
`project-command` and `project-overview` deltas. `PR19/pc` is `CAS/pc` as draft
PR #19 amends it (branch `change/amend-clean-all-safe-push-pins`, head
`c462d87`, whose spec text equals the `5ce23d7` that the lane's rulings first
named), and `PR19/rs` is `CAS/rs` as PR #19 amends it at that head.
`project:N` is the executable at `961c405`. L-n and B-n are the lane's rulings
for the three extensions and for this one: L-1 to L-9 and B-1 to B-9 of
2026-10-11, L-10 to L-15 and B-10 to B-15 of 2026-10-18, L-16 and L-17 of
2026-10-19 with B-16 to B-24, the lead's council verdicts of that date, and
B-25 to B-40 of 2026-10-20; A-n are the rulings for #23 that this proposal
cites. SA-n, QA-n and G1 to G5 are the alignment review's findings on this
draft at `7290100`. P-n, S-n and AE-n are the council's concerns
(product-advocate, systems-architect, adversary-engineer) on `9ebe9f0`, and M1
to M5 and LOW 1 to LOW 17 are lane openRepoProject-3's packet-fidelity findings
on `3c08613` and `9ebe9f0`; its re-read of `e906c2f` is cited as "re-read
MEDIUM 1" and so on, its delta read of `cf57956` as "delta read LOW (1)" and so
on, lane openRepoProject-4's review of 2026-10-20 by its findings F2 and F4,
and Codex's inline findings by their file and line. CD-n
are this proposal's own decisions. The packet is non-normative brainstorm
material (`OV:16-19`); only the deltas that follow will be normative.

## Why

Change 1 removes only worktrees with no ignored files, on purpose: "caches
such as `__pycache__` keep a worktree out until the cache-disposal change"
(CAS proposal.md:72-75). A merged, clean, published worktree whose only extra
content is Python bytecode is therefore classified `ignored-local-files` and
kept, run after run, although nothing in it is work. Change 1's measurement
found `ignored-local-files` the largest exclusion among linked worktrees, 102
of the 265 linked rows; only `main-worktree`, 296 of all 561 rows, is larger
(CAS tasks.md:85-87). Its council found 20 of one repository's 29 merged
worktrees excluded for caches alone (CAS proposal.md:697-699; PR #16 at
`841c7dc` cites the same count as the evidence for this change). Measured again
on 2026-10-19, those 20 rows are 13 whose ignored files are only `__pycache__`,
`.pyc` and `.pyo`, which this change disposes of, and 7 that also hold a
`.pytest_cache`, which it does not. Across the repositories with linked
worktrees on that workstation, 37 merged, clean, published rows are kept for
ignored files: this change makes 13 removable, 3 more are cache-only but stay
excluded as `contains-submodule`, 16 are kept by `.pytest_cache` alone, and 5
by other files (the council's P-1; Open Questions). Change 1 names cache
disposal "the first follow-on change" (CAS proposal.md:697).

The packet keeps cache deletion out of the first batch (`OV:150-152`,
`SY:232-235`, `HO:47-50`) and fixes the contract a later proposal must meet
(`BA:1314-1337`): a stage of its own before the worktree removal, inside
`retire_worktree` and its deadline, counting its mutations in
`operations.estimated` and its bounds in `limits` (`BA:1318-1322`); symlink
candidates and ancestors ineligible; descriptor-relative, no-follow operations
with each opened directory checked against its planned device and inode,
failing closed where the platform cannot do that (`BA:1324-1330`); each cache
path reported separately, a partial phase recorded as permanent partial
completion with retry guidance, no worktree mutation after a failed preflight,
and hard limits on entries and bytes in the plan estimate (`BA:1332-1337`). A
proposal that adopts the extension must update the governing cleanup
specification and add its failure and recovery contract first (`BA:56-60`,
`OV:178-180`).

The packet defines no cache: `grep -niE '__pycache__|\.pyc|disposable'` over
`ideation/brainstorm/` finds only the commit descriptions at `OV:177` and
`BA:41`. The allowlist exists only in the closed PR #2's code and in change
1's prose. PR #2's `1789ad9` and `bb91a49` are the harvest source and do not
meet the contract (`git show bb91a49 -- project`): no planned identity is
checked; the ignored listing is unbounded and no cap exists; each path is
revalidated only just before its own deletion (review thread 3989548481, open
at the close); a cache under a parent not named `__pycache__` is classified
disposable and then refused after confirmation (the open review finding at
`project:759` of `bb91a49`); and a missing `O_NOFOLLOW` falls back to flag 0
through `getattr(os, "O_NOFOLLOW", 0)` instead of failing closed.

## What Changes

- **Behaviour users will notice.** A merged, clean, published linked worktree
  whose ignored files are only Python bytecode caches is now selected by
  `project clean <root> --all-safe` (measured 2026-10-19: 13 of 37 such rows)
  and removable by `--apply --action remove --worktree P`: the preview lists
  its caches, and apply disposes of them in a cache stage, then removes the
  worktree exactly as change 1 does, its branch kept. `project overview` keeps
  reporting such a worktree as `ignored-local-files`, a preserve warning, whose
  suggestion is the read-only clean report. A worktree holding any other
  ignored file stays `ignored-local-files`, and its preview now says how many
  of its ignored paths are disposable and how many block it, or, when its
  sampled paths already show one that blocks, names that path without
  counting. A worktree whose only ignored files are caches but which is
  detached, unpublished or unmerged stays `ignored-local-files`, and its
  preview names that state, since disposing of its caches would not make it
  removable. Squash-merged worktrees are among them while question 2 is open.
  For a worktree with no ignored files nothing changes: its plan, digest,
  question, stages and exit status are change 1's.
- **The allowlist (B-1).** A listed cache is an ignored path that is either a
  directory named `__pycache__` whose entries are only regular files whose
  names end `.pyc` or `.pyo` and directories named `__pycache__` of the same
  shape, or a regular file whose name ends `.pyc` or `.pyo`, none of them a
  symbolic link. Every directory between the worktree root and a listed path
  must be a non-symlink directory on the worktree root's device, and the path
  must be valid UTF-8 (CD-8). Every other ignored path is blocking.
  `.pytest_cache` is before Brett Heap, with a recommendation to admit it here,
  and is added only on his answer (B-23); other cache kinds are out of scope
  (Open Questions).
- **Detection by a bounded enumeration of its own (B-2, B-12).** The combined
  status probe stops at the 65th ignored record and keeps eight samples
  (CAS/cmd:161-173), so it cannot prove a whole worktree disposable. A
  candidate row is a linked worktree whose combined probe read ignored records
  and nothing else, none of whose samples has a name or encoding that the
  allowlist rejects (the sample test, which spawns no child), and which, its
  ignored records aside, would be `merged-removable` and pass every gate before
  `deferred-target-cap` (CD-7). For each, in canonical order and at most 16 per
  invocation (CD-6), `project clean` runs one more Git child in that worktree,
  `status --porcelain=v2 -z --untracked-files=normal --ignored=matching`, under
  the evidence model's scrub, protocol pins and directory rule and with the
  status pins (CD-5), reading at most 512 records, then walks the listed caches
  descriptor-relatively, opening each directory it records once and counting
  it toward the per-worktree cap with the entries (B-33), and checking with one
  descriptor-relative access check per directory the stage would change that
  the running user may remove entries from it (B-20). A row whose enumeration
  reaches a cap stays `ignored-local-files` with the reason `cache-cap`; one
  whose enumeration fails, times out, or reads anything but ignored records
  stays `ignored-local-files` with `cache-unverified`; one whose caches the
  user cannot change stays `ignored-local-files` with `cache-unwritable`, its
  counts established, not selected and stopping nothing; and the plan stays
  complete (CD-9).
- **Caps (B-3, CD-6).** Per worktree, 512 recorded objects, its cache entries
  (every file and directory the stage would remove) and every directory the
  plan records for them, those above the caches included (B-33), and 256 MiB,
  the `lstat` sizes of its regular files summed at plan time; per invocation,
  4,096 entries, 1 GiB and 16 enumerations. `limits` reports them as
  `cache_entries`, `cache_bytes`, `cache_entries_total`, `cache_bytes_total`
  and `cache_rows`. The enumeration children count in `probes`, and each entry
  a cache stage removes counts in `operations` beside the removal children
  (draft PR #19, pending; CD-12; `BA:1321-1322`, `BA:1336-1337`). The 50 s fit
  of the Git children still holds with the 16 enumerations at the packet's
  150 ms per child. Design D4 restates it with the measured cost of the walk's
  and the stages' filesystem calls, the walk bounded at 16 x 512 = 8,192
  recorded objects because a row the invocation's totals reject was still
  walked (B-25), and with the stages' removals waited for (B-16, S-4): for
  ordinary trees, at the top of the measured cost, the 16th target, which then
  lists no cache, reaches its spawn under the removal floor, which refuses it,
  and it is deferred to the next run with exit 1, never unsafe (B-31). In
  B-33's worst case, a deep tree whose every directory with removals costs a
  chain from the worktree root, no fit holds without a new limit, which is put
  to Brett Heap beside the caps; the caps stay before him (Open Questions).
  Rows the caps leave drain on re-run unless each of the first 16 candidates
  stays at the rung for a persistent reason (B-32), a stall the human report
  names with each row's cause and next step (QA-2, B-21).
- **The ladder reads blocking paths (B-5).** The `ignored-local-files` rung
  keeps its name and its place and applies to a row holding an ignored path
  that is not proven, within the caps, a listed cache; a row whose every
  ignored path is a listed cache passes it, and the rungs below classify it, so
  a merged one is `merged-removable`. No ladder class, gate reason, stage
  value, reason value, refusal code or note code is added (L-4).
- **The plan records identities (B-4).** Each worktree row holding ignored
  records, and each `selected` entry whose plan lists caches, carries a
  `cache_disposal` object; any other row or entry carries no such key, never
  `null` (L-10, B-13). The object holds the `disposable` and `blocking` counts,
  `null` and never 0 when not established (B-9); a `reason`; `entries` and
  `bytes`; the listed cache paths; the device and inode of every directory the
  stage will open, each ancestor up to the worktree root and each cache
  directory; and up to eight blocking samples. A selected target's listed
  caches and those identities enter the canonical text of `plan_digest`, by a
  MODIFIED block of change 1's batch requirement (B-10, CD-14); a plan that
  lists none keeps change 1's digest.
- **The cache stage (B-6, B-8).** In the removal sequence, after the target's
  revalidation and before its removal child is spawned, inside the same
  deadline: a whole-list preflight opens every directory of every listed path
  descriptor-relatively with `O_NOFOLLOW`, as the removals do after it, one
  chain from the worktree root per directory holding a listed path (B-33),
  checks each against its planned
  device and inode, re-lists each cache directory against the allowlist and
  the number of entries the plan recorded for it, and keeps the run's byte
  total, refusing a target whose measured bytes would take it past the
  invocation's 1 GiB (B-26), all before the first unlink; then files are
  unlinked and emptied directories removed one entry at
  a time, never by a recursive deletion, and a directory that is no longer
  empty is never removed. The stage starts only while more than the 5 s
  removal floor remains and no signal has arrived, and checks both again
  immediately before it hands its first removal to its worker (B-17); each of
  its reads gets `min(5 s, work remaining less the removal floor)` on change
  1's daemon threads, while each unlink and directory removal is handed over
  only while more than the floor remains and is waited for until it returns,
  as change 1 waits for its removal child, up to the 300 s removal ceiling
  (CD-10, B-16). The hand-off of the first removal is the stage's commit point:
  once it is made the stage runs to its end, a signal only being recorded
  (CD-11). Change 1's rule that `project` never deletes a directory itself
  gains this stage as its one exception (B-10).
- **Failure and recovery (B-6, B-11).** A preflight difference deletes nothing,
  and so does a first removal refused by a sticky directory or a read-only
  filesystem that the plan's access check cannot see (B-20). A failure after an
  entry was removed leaves the earlier removals as permanent partial cache
  completion, rescans the listed paths by the same identity-checked descriptor
  chains the removals use (B-18), and reports each one removed, remaining, or
  not established, a path whose removal is still outstanding among the last,
  with the retry: re-run `project clean <root> --all-safe`, whose fresh plan
  lists what remains (`BA:1332-1336`). Either way the target's removal child is
  not spawned: the target is `refused` with `state-changed`, its
  `cache_disposal` records `refused` with `cache-changed` or `partial` with
  `cache-partial` (CD-2), and the run stops there, as change 1 stops at any
  target that is not a plain `removed` (CD-1; `BA:1640-1643`), with exit status
  2, or 1 when the removal floor ended the stage or the removal ceiling ended
  the wait for one of its removals, the later targets then being
  `not-attempted` with `deadline-exceeded`. A target whose stage removed every
  listed cache but whose removal a signal or the floor then stopped is
  `not-attempted` and carries its reconciliation (B-17). A target whose stage
  the floor or the work deadline stopped in a read before its first removal is
  `not-attempted` too, with nothing deleted, no difference found and no
  reconciliation, the later targets likewise and the exit status 1 (B-34); a
  read that outlives its own 5 s budget with at least 10 s of work left stays a
  preflight error, `refused` with `cache-changed` (B-38), unless a signal was
  received before the stop of a read is classified, in which case the stage is
  `not-attempted`, the target `interrupted` and the exit status the signal's,
  as at the check before the first hand-off (B-39).
- **Fail closed per platform (B-6, CD-3, B-37).** Where the running Python
  cannot provide `O_NOFOLLOW`, `O_DIRECTORY` and the descriptor-relative calls,
  no row gets a cache plan: a row that reaches the `ignored-local-files` rung
  with ignored records keeps it with the reason `cache-unsupported-platform`, a
  row that an earlier rung classified, a `dirty` one among them, keeps that
  classification and its `not-candidate` sub-record, no enumeration runs, and
  the batch behaves as change 1's.
- **Revalidating a cache target (CD-4).** Change 1's revalidation requires the
  combined status probe in the target to print no record (CAS/rs:75-76), which
  every cache target fails. For a target whose plan lists caches, the
  revalidation runs the enumeration's status child instead, which must print
  exactly the ignored records the plan listed and nothing else; any other
  outcome refuses the target with `state-changed`, still within five Git
  children. The narrow guarantee's revalidation is, for such a target, the one
  before its cache stage (B-10).
- **What the person sees (B-9, B-7).** The preview lists a selected target's
  caches under it (paths, entries, bytes and the first path); an
  `ignored-local-files` exclusion adds its disposable and blocking counts, or
  `unknown` with the reason, its first blocking path, and, for a row that is
  not a candidate, the class or gate that really keeps it with that next step
  (`candidate_block`, B-24). The question is change 1's, unchanged (CD-15).
  Success adds one line naming the caches disposed; a stop at a cache stage
  adds one line before the stop block, saying that nothing was deleted, only
  when nothing was and no removal is outstanding, or which cache paths were
  removed, which remain and which may still be removed, naming the work
  deadline when it ended the stage (B-16, B-21); a stop after a stage that
  disposed of every cache says so and that the worktree was not removed
  (B-17); a stop at a stage that the floor or the deadline stopped in a read
  before its first removal, and with no signal received by then, says that it
  was not attempted because of the deadline and that nothing was deleted (B-34,
  B-39). The stall line names, for the
  16 rows that hold the others back, how many stay for each cause, with its
  next step, and never tells the person to remove by hand a worktree whose
  state was not established (B-21). The residual-window line also names ignored
  files created during a cache stage and a cache recreated after it, which
  Git's non-force removal deletes with the worktree (`BA:319-323`, B-19).
- **Versioned JSON.** Worktree rows, `selected` entries and apply-result
  targets gain `cache_disposal` where this change acts (L-10), and `limits`
  gains five keys. No value is added to any existing enum, `candidate_block`
  takes its values from the existing class names and gate reasons (B-24), and
  `schema_version` stays 1 (CD-16; Open Questions).
- **The overview's equality clause (B-14, B-22, B-30).** Change 2's "Overview
  reuses the cleanup classifier and merge target" gains two sentences: the
  overview, which collects no cache evidence, SHALL classify
  `ignored-local-files` a worktree that `project clean` classifies
  `merged-removable` because clean's cache enumeration proved every ignored path
  a listed cache, and SHALL NOT classify a worktree `merged-removable` where
  `project clean` classifies it otherwise for the same working directory and
  refs.
  Lane openRepoProject-4 agreed the first wording on 2026-10-19 and it was
  committed as `b4d3e12`; B-22's rewording, a third worktree in the new
  scenario's fixture and lane 4's precision in the carried "Every protected
  classifier" were agreed by lane 4 on 2026-10-19 and committed as `9f30fb9`;
  B-30's scope, "for the same working directory and refs", is lane 4's own
  words of 2026-10-20, committed as `4d5855a`, which lane 4 byte-checked on
  2026-10-20 (`tasks.md` 2.2).

## Rules This Change Keeps

- **Never force, never a broad deletion.** No `git clean`, no recursive
  deletion and no deleting command run by `project`: caches go one entry at a
  time, and a directory only once `project` has emptied it (`BA:1329-1330`,
  `BA:1632-1634`; PR #2's design rejected `git clean -fdX` because it also
  deletes unknown ignored files). Change 1's "`project` SHALL never force a
  removal or delete a directory itself" gains one exception, this stage's
  descriptor-relative deletion of listed cache paths (B-10); its "It MUST never
  use a force removal, reset, or deletion of unmerged work" stays verbatim.
- **What is not proven disposable is preserved.** An ignored path is
  disposable only when this invocation's enumeration proves it a listed cache
  within the caps; an unproven path is blocking, and `null` is never 0.
- **Never follow a symlink or leave the worktree.** A symlink candidate or
  ancestor is blocking (`BA:1324-1325`, whose "any ancestor" this change reads
  as any directory between the worktree root and the cache, the root's own
  ancestors being covered by change 1's realpath and identity check and the
  root's identity checked when the stage opens it); every descent is
  descriptor-relative with `O_NOFOLLOW` and an identity check, and no
  descriptor given to a call still outstanding is closed and reused (B-16); a
  hard-linked `.pyc` loses only its name inside the worktree, and every
  external target stays intact (`BA:1632-1634`).
- **Stop before the worktree removal when the cache stage fails**
  (`BA:1335-1336`), and stop the run at the first target that is not a plain
  `removed`, as change 1 does (CAS/pc:246-248; `BA:1640-1643`).
- **Removing a worktree leaves its branch.** Unchanged; paired retirement is
  `add-project-clean-branch-retirement` (#23).
- **Nothing beyond the confirmed plan.** The stage disposes of only the caches
  that the confirmed plan lists, each holding the number of entries the plan
  recorded, in a target that plan selected; the main worktree and every row not
  selected are never touched.
- **Local evidence only.** No fetch and no network; remote evidence never
  proves anything disposable (`SY:129-130`).
- **A started removal is never interrupted.** Unchanged; a cache stage, once
  it has handed over its first removal, also runs to its end, and each removal
  it hands over is waited for as a removal child is (B-16).

## What This Repository Does Not Own

- **Python's caches.** Python writes them again on the next import; `project`
  decides only whether a worktree's caches are its only ignored content, and
  never whether Python writes them (`PYTHONDONTWRITEBYTECODE` and
  `PYTHONPYCACHEPREFIX` are the person's).
- **Git's ignore rules.** Which paths are ignored is the repository's
  `.gitignore`, `info/exclude` and `core.excludesFile`; `project` reads Git's
  verdict and never edits them.
- **Git's own refusals.** The pinned non-force `git worktree remove` stays the
  last defense after the cache stage.
- **The overview's evidence.** `project overview` is change 2's, owned by lane
  openRepoProject-4 with feature 005; this change does not alter what it
  collects, and amends only its equality clause, as lane 4 asked (B-14).

## Capabilities

### New Capabilities

None. PR #2's `project-clean-disposable-cache-artifacts` is not reused (L-3);
the contract lives in the two existing cleanup capabilities.

### Modified Capabilities

Headers are quoted verbatim, one per line; ADDED headers are proposed text. A
line number alone is the canonical spec's at `961c405`; each MODIFIED block
also names the delta text it is written on.

- `project-clean` (all five canonical requirements and change 1's six ADDED
  ones accounted for):
  - MODIFIED (`:25`; written on CAS/pc:105):
    `### Requirement: Clean classifies preservation and cleanup actions`.
    The `ignored-local-files` rung applies to a row holding an ignored path
    not proven, within the caps, a listed cache, or a listed cache in a
    directory the access check finds the user cannot change (B-20), and a row
    whose every ignored path is a listed cache that passes that check passes
    it; a failed cache enumeration leaves the
    paths unproven and is never `inspection-error`; its `inspection-error`
    sentence names the combined status probe; a row's cache proof is its
    evidence, though the caps can withhold it. The fifteen names, the order
    and the ancestry test stay, with the four scenarios. Added scenario:
    cache-only ignored files pass the rung, and beside `local.env` they do not.
  - MODIFIED (`:55`; written on CAS/pc:230), one inserted clause only:
    `### Requirement: Clean can explicitly retire verified worktrees`.
    The one sequence gains "for a target whose plan lists caches, dispose of
    them as "Clean disposes of listed caches before a worktree removal"
    states;" between the revalidation and the spawn. Every other sentence and
    the fourteen scenarios stay as change 1 wrote them.
  - MODIFIED (change 1 ADDED; written on CAS/pc:566), B-10:
    `### Requirement: Clean previews and applies a batch of eligible worktree removals in one repository`.
    The digest's canonical text carries, after each selected target's triple
    whose plan lists caches, its cache paths and planned cache directory
    identities; a plan that selects no such target carries none. Every other
    sentence stays. The scenario "Every protected classifier" names its
    ignored files as not Python bytecode caches (B-22, lane openRepoProject-4's
    precision); the other nine stay. Added scenario: cache paths are part of
    the plan digest.
  - MODIFIED (change 1 ADDED; written on PR19/pc:767, draft PR #19's text):
    `### Requirement: Clean bounds its Git work and reports omitted work`.
    The cache stage's start under the removal floor and its reads' budget; its
    removals handed over only while more than the floor remains and waited for
    as removals in flight up to the 300 s ceiling (B-16); the cache walk's
    opens, listings, `lstat` calls and access checks among the filesystem
    calls; the five cache caps in `limits`; the enumeration children in
    `probes` and in the fit, the walk's and the stages' filesystem calls
    outside it; each removed cache entry in `operations`. The scenario
    "Ignored-file bound" names files that are not caches; the other four stay.
    Added scenario: the cache limits and counts.
  - MODIFIED (change 1 ADDED; written on CAS/pc:886), B-10:
    `### Requirement: Clean records a reconcilable result for every removal target`.
    The `refused` stage also names a cache stage that ended `refused` or
    `partial`; the `not-attempted` stage also names a target whose cache stage
    ended `disposed` and whose removal a signal or the floor then stopped, and
    such a target carries its reconciliation once its stage removed an entry;
    the signal paragraph lets a cache stage that has handed over its first
    removal run to its end (B-17, lane 3's M2, its re-read MEDIUM 2 and LOW 1);
    the exit table's row 2 also names a cache stage's removal that reached the
    removal ceiling (re-read MEDIUM 1); "`project` SHALL never force a removal
    or delete a directory itself" gains its one exception, a cache stage's
    descriptor-relative deletion of listed cache paths. The eight scenarios
    stay.
  - ADDED:
    `### Requirement: Clean disposes of listed caches before a worktree removal`.
    The allowlist, the sample test, candidate rows, the enumeration with its
    caps, the per-worktree one counting recorded directories (B-33), the
    access check, reasons and the stall on persistent reasons (B-32), the
    plan's `cache_disposal`
    with identities, counts and `candidate_block` and its presence rule, the
    cache stage's place, start, checks, commit point and budget, the result's
    `cache_disposal`, the exit statuses through change 1's table, and the human
    lines, the one for a preflight that the deadline stopped included (B-34).
  - Untouched (`:10`): `### Requirement: Clean reports local worktree state`.
    The plain report carries `cache_disposal` on its rows holding ignored
    records as every plan does, and its `selected` stays what `--all-safe`
    would select.
  - Untouched (`:39`):
    `### Requirement: Clean can explicitly push safe feature branches`.
    Push and delete-branch run no cache enumeration.
  - Untouched (`:70`): `### Requirement: Clean hands off work requiring review`.
  - Untouched (change 1 ADDED): `### Requirement: Clean resolves its target Git-first`.
  - Untouched (change 1 ADDED):
    `### Requirement: Clean reports every path exactly or excludes it`.
    Cache paths are written by its rules.
  - Untouched (change 1 ADDED):
    `### Requirement: Clean plans and refusals are versioned JSON`.
    The new objects and keys are additive (CD-16).
- `project-clean-review-safety` (all four canonical requirements and change 1's
  ADDED one accounted for):
  - MODIFIED (`:21`; written on CAS/rs:3):
    `### Requirement: Cleanup preserves all local work not proven disposable`.
    Ignored local files stay a preservation state, except listed caches, which
    are disposable only by the cache stage of a selected target. The scenario
    "A merged worktree has ignored local files" names an ignored file that is
    not a cache; the other four stay. Added scenario: a worktree whose only
    ignored files are caches.
  - MODIFIED (`:49`; written on PR19/rs:60, which differs from CAS/rs:60 only
    in its last clause), beyond the ruled list (CD-4):
    `### Requirement: Cleanup revalidates destructive actions`.
    For a target whose plan lists caches the in-worktree status check is the
    enumeration's child, which must print exactly the listed cache records; the
    revalidation the MUST names is, for such a target, the one before its cache
    stage; a cache difference, and a cache stage that ends `refused` or
    `partial`, refuse the target with `state-changed`, with the exit status the
    ADDED requirement gives. The ten scenarios stay. Added scenario: a cache
    target changes before revalidation.
  - MODIFIED (change 1 ADDED; written on CAS/rs:194), B-10:
    `### Requirement: Cleanup states a narrow guarantee and its residual window`.
    The one guarantee for a worktree removal holds, for a target whose plan
    lists caches, at the revalidation before its cache stage; the stage carries
    the one guarantee for the cache entries it removes, and nothing runs
    between it and the spawn but the floor and signal checks; the residual
    window and its line name ignored files created during the stage outside
    the listed caches and a cache recreated after it (B-19). The three
    scenarios stay. Added scenario: a cache recreated after the cache stage.
  - ADDED:
    `### Requirement: Cache disposal never follows a symlink or leaves its worktree`.
    Symlink candidates, ancestors and entries blocking; descriptor-relative
    no-follow operations against planned identities, one chain per directory
    holding a listed path in each pass (B-33), no descriptor of an
    outstanding call reused; no recursive deletion; the whole-list preflight
    with its entry count and the run's byte total (B-26), and its outcome when
    the floor or the deadline stops a read of it (B-34), or a signal received
    first outranks the stop (B-39); the outcome once a
    removal is handed over; the
    partial-phase record, its chain rescan under the reserve, and retry; the
    per-platform fail-closed rule, which leaves a row that an earlier rung
    classified as it is (B-37); the stage's guarantee.
  - Untouched (`:9`): `### Requirement: Cleanup protects the process worktree`.
  - Untouched (`:38`): `### Requirement: Cleanup respects configured upstream mappings`.
- `project-overview` (change 2's twelve ADDED requirements accounted for; no
  canonical spec yet), B-14, B-22 and B-30, its first delta agreed by lane
  openRepoProject-4 on 2026-10-19 and committed as `b4d3e12`, B-22's edit
  agreed by lane 4 on 2026-10-19 and committed as `9f30fb9`, and B-30's scope,
  lane 4's own words of 2026-10-20, committed as `4d5855a` (`tasks.md` 2.2):
  - MODIFIED (change 2 ADDED; written on APO/ov:358):
    `### Requirement: Overview reuses the cleanup classifier and merge target`.
    Two sentences are appended to the equality clause: the exception for a
    worktree that `project clean` classifies `merged-removable` on its cache
    proof, and the classification-level SHALL NOT, for the same working
    directory and refs (B-22, lane 3's M4 and M5; B-30, lane 4's F4).
    The scenario "Every protected classifier" names its `ignored-local-files`
    worktree's ignored file as not a Python bytecode cache (lane 4's
    precision), a departure from B-14's "plus one scenario"; the other six
    stay. Added scenario: caches that only `project clean` proves disposable,
    with a third, submodule-holding worktree (B-22).
  - Untouched (change 2 ADDED):
    `### Requirement: Overview discovers projects within configured roots only`,
    `### Requirement: Overview groups worktrees by repository identity`,
    `### Requirement: Overview bounds its work and reports what it omitted`,
    `### Requirement: Overview isolates one candidate's failure`,
    `### Requirement: Overview reports findings by attention category`,
    `### Requirement: Overview suggests only gated clean commands`,
    `### Requirement: Overview prints a versioned JSON envelope`,
    `### Requirement: Overview is local and read-only`,
    `### Requirement: Overview reports default-branch health`,
    `### Requirement: Overview exits by completeness and severity`,
    `### Requirement: Overview renders a readable human report`.
    The overview collects no cache evidence, and its suggestion for a row it
    reads `ignored-local-files` stays the read-only clean command.
- `project-command`, `project-review-safety` and
  `speckit-extension-integration`: untouched. The enumeration child is a Git
  child of `project clean` alone, carrying the evidence model's environment,
  protocol pins, status pins and directory rule (CAS/cmd:98-133) without
  changing that model's probe list; status and doctor gather no cache evidence.

## Impact

- **`project`**: after feature 004, the plan builder gains the candidate rule
  with its sample test, the enumeration child (through the bounded runner, with
  a NUL parser for porcelain v2's ignored records) and the descriptor-relative
  walk; the plan, the digest and the envelope gain `cache_disposal`; the
  removal sequence gains the cache stage between the revalidation and the
  spawn; the targeted revalidation reads a cache target with the enumeration
  child; the human preview, success and stop output gain the cache lines. At
  `961c405` the attach points are the ignored probe and rung
  (`project:505-507`, `project:581-583`), the signature that compares
  `ignored_files` and `classification` (`project:642-645`) and the remove path
  (`project:707-722`, `project:736-743`); feature 004 replaces all of them, so
  this change's feature builds on feature 004's code. No new dependency: only
  `os` calls that Python 3.10 provides.
- **`README.md`**: the "Clean up Git worktrees" section gains the cache
  paragraph: what is disposed of and what blocks, the caps and their stall, the
  residual window, ignored files created during a cache stage included, and the
  partial phase with its re-run.
- **`tests/test_project.py`**: a test named after each ADDED and MODIFIED
  scenario that this change adds; fixtures write `.pyc` bytes directly and need
  no compiler run;
  `test_clean_preserves_ignored_files_in_an_otherwise_merged_worktree`
  (tests:949, whose ignored file is `local.env`) and change 1's cache-free
  scenarios keep passing; fault hooks for the preflight, the removals (held,
  failed or past the ceiling) and the walk; a platform stub for
  `cache-unsupported-platform`. The new tests' names begin `test_clean_`, so
  that feature 004's `git-floor` job, which runs them with Git 2.36.6 first on
  PATH, includes them (S-4). The command is `python3 -m unittest discover -s
  tests -v`, which CI runs on `ubuntu-latest` with Python 3.10 and 3.12 (the
  jobs `test (3.10)` and `test (3.12)`), and, once feature 004 merges, with Git
  2.36.6 in `git-floor`; macOS is not verified by CI (L-12).
- **Feature 005's tests**: once feature 005 has landed, any of its tests that
  asserts that the overview and `project clean` classify identically gets the
  cache case excluded in this change's realization, never in feature 005
  (B-14).
- **Speckit handoff**: exactly one feature, numbered when `/speckit.specify`
  runs after ratification, 006 or later (L-7).

### Dependencies and Sequencing

- **Written on change 1 and change 2 (L-1, L-15).** Every MODIFIED block of
  `project-clean` and `project-clean-review-safety` but two is written on
  change 1's ratified text at main (`e9d6711`, whose `openspec/` equals
  `961c405`'s), and the `project-overview` block on change 2's text there.
  "Clean bounds its Git work and reports omitted work", as the rulings direct,
  and "Cleanup revalidates destructive actions", whose last clause PR #19 also
  rewords (the protocol pins are carried by every Git child "except the push
  child"), are written on draft PR #19's text (`c462d87`, spec text equal to
  the `5ce23d7` the rulings first named), and PR #19 is a dependency: if it
  merges, change 1's text equals both blocks' bases; if it closes unmerged, or
  changes either requirement again, the blocks are rewritten on the text of
  that day before this change is ratified. Under L-16 this change archives
  after PR #19's amendment of change 1 lands, and the passages that rest on
  PR #19's wording are marked "(draft PR #19, pending)". `validate --strict` passes while
  changes 1 and 2 are unarchived; the archive is the gate (it reports "Archive
  would refuse this delta" for each delta file until change 1, and for the
  `project-overview` delta change 2, is archived).
- **Archive order (L-5, L-11, L-16, B-14, B-29).** This change archives after
  change 1's archive, which follows feature 004's merge, after PR #19's
  amendment of change 1 has landed, or PR #19 has closed and the two blocks
  have been rewritten, and after change 2's archive, its `project-overview`
  block first re-aligned with main's text (Change 2, below).
  `add-project-clean-branch-retirement` (#23) archives after this change and
  carries every requirement that both changes modify: "Clean can explicitly
  retire verified worktrees", "Clean previews and applies a batch of eligible
  worktree removals in one repository", "Clean bounds its Git work and reports
  omitted work" and "Clean records a reconcilable result for every removal
  target" in `project-clean`, and "Cleanup states a narrow guarantee and its
  residual window" in `project-clean-review-safety`, each re-based on this
  change's archived block before #23 archives (L-11, A-13). #23 also states the
  fit of a run with `--retire-branches` and cache disposal together (A-9, the
  alignment review's G3); the inputs it needs from this change, restated after
  the council and again in rounds B3 and B4, are listed in design D4: the
  stage's removals waited for up to the 300 s ceiling, the walk's and the
  stages' measured filesystem time, the walk bounded at 8,192 recorded objects
  (B-25, B-33), the stages' chains and B-33's worst case, no status probe
  after a `disposed` stage, and the residual-window line of D13,
  on which #23's line for a flagged run with a cache target re-bases (B-16,
  B-19, S-4). `add-project-overview-remote-merge-status` (#25)
  modifies none of this change's requirements (its `project-overview` blocks
  are "Overview is local and read-only", "Overview bounds its work and reports
  what it omitted" and "Overview prints a versioned JSON envelope", and its
  `project-command` block is "Repository inspection requires Git 2.36 and
  shares one evidence model", which #23 also modifies) and archives after
  change 2 and after PR #19's amendment of change 1.
- **Implementation order.** This change's feature builds on feature 004
  (`004-project-clean-all-safe`): its removal sequence, runner, parsers, ladder
  function and envelope. It never alters feature 004's or feature 005's order
  and does not wait for feature 005, but lane openRepoProject-4's agreement on
  the `project-overview` delta, given on 2026-10-19 for `b4d3e12` and again
  for B-22's edit, which is committed as `9f30fb9`, and its byte check of
  B-30's commit `4d5855a`, which carries lane 4's own words, given on
  2026-10-20 (B-36), precede its Speckit handoff (`tasks.md` 2.2).
  Whichever realization merges second merges `main` in; never rebase, since
  the organisation ruleset refuses force pushes.
- **Change 2.** This change modifies one requirement of change 2, "Overview
  reuses the cleanup classifier and merge target", with two sentences, one
  added scenario and a precision in one carried scenario (B-14, B-22, B-30).
  The overview's collection and its other requirements are unchanged. A
  MODIFIED block replaces its requirement whole, so an amendment of that
  requirement landing on main before this change archives, such as lane
  openRepoProject-4's planned one for feature 005's open Q7 A, would be
  dropped silently by this change's archive. Before `/opsx:archive`, this
  change's block is therefore re-read against main's text of the requirement
  and re-copied from it, keeping every amendment with this change's additions;
  a `diff -u` of main's block against this change's shows additions only, and
  the validation passes again (B-29, lane 4's F2; `tasks.md` 3.2).
- **Question 2, squash-merged worktrees.** Whether patch equivalence proves a
  squash-merged branch merged is change 1's open question 2 (CAS
  proposal.md:700-701; `OV:364-366`, `SY:225-226`, `BA:195-199`), and this
  change does not presume it: candidates follow the ladder's local-ancestry
  `merged-removable`, so squash-merged worktrees stay non-candidates, their
  `candidate_block` naming what keeps them (B-24), while it is open. A later
  ruling that admits patch equivalence would add candidates through the
  ladder, and the fit of design D4 would then be restated (lane 3's LOW 7).

## Out of Scope

- **`.pytest_cache`, until Brett Heap answers its Open Question.** The
  recommendation is to admit it in this change as a third listed form; if he
  declines, it is the next change, first in line, measured 2026-10-19 as the
  only blocker of 16 kept rows (B-23).
- **Other cache kinds** (`.mypy_cache`, `.ruff_cache`, `node_modules`, virtual
  environments, build directories) (B-1; Open Questions).
- **Paired branch retirement** (#23) and **remote merge status** (#25), each
  its own change.
- **The overview and doctor beyond the shared ladder.** Doctor classifies no
  worktree (change 1's C3); `status` and `doctor` gather no cache evidence and
  their JSON gains nothing; the overview's collection is unchanged, and only
  its equality clause gains the cache exception (B-14).
- **Disposal without removal.** No mode deletes caches and keeps the worktree;
  the stage runs only for a target about to be removed.
- **Configurable caps or allowlists** (change 1's OQ-8 holds) and the CI
  matrix.
- **Continuing after a failed target** (`BA:1640-1643`; CD-1).

## Decisions Taken by This Proposal

Each is a proposal decision, open to ratification. The lane's rulings applied,
each citing the packet or change text that left it open:

- **L-1 and L-15, the base text.** Drafted on change 1 and change 2 at
  `961c405` (main now `e9d6711`, with the same `openspec/`), and "Clean bounds
  its Git work and reports omitted work" on PR #19 (Dependencies and
  Sequencing). This proposal reads the six requirements that lane
  openRepoProject-2 said PR #19 does not move as the six that the three
  extensions' ruled lists modify besides the bounds. L-15 names only the
  bounds requirement as written on PR #19's text; "Cleanup revalidates
  destructive actions", which CD-4 adds, is not among the six, PR #19 rewords
  its last clause, and a block written on change 1's text would undo that
  clause when PR #19 lands, so its block stays on PR #19's text by the same
  logic, as the alignment review agreed (CD-4). PR #19 is still a draft at
  `c462d87` (2026-10-18); `git diff 5ce23d7 c462d87` touches only its
  `design.md` and `tasks.md`.
- **L-2, citations** at `da33d92`; PR #16's added sentence is quoted as "PR #16
  at `841c7dc`" (Why).
- **L-3 and L-11, capabilities and placement.** The existing capabilities only
  (PR #2's abandoned names not reused); a MODIFIED block carries its whole
  requirement and every scenario of its source text; the new contract is in two
  ADDED requirements whose names no other change uses. Where this change
  contradicts a sentence of change 1 or change 2 it modifies that requirement
  and never overrides it from an ADDED one (L-11): B-10 places the digest, the
  narrow guarantee's revalidation and the deletion exception in MODIFIED
  blocks, and B-14 the overview's equality clause.
- **L-4, L-10 and B-13, sub-records.** Every new value lives in
  `cache_disposal`, whose `reason` and `stage` are its own enums. No value is
  added to the closed `stage` enum, the target reasons, the fifteen classes,
  the gate reasons, the refusal codes, the note codes or the overview's finding
  codes. `cache_disposal` is present only where this change acts and absent
  otherwise, never `null` for "not applicable": on a `selected` entry and an
  apply-result target whose plan lists at least one cache, and on a worktree
  row whose `ignored_files` is above 0. L-10 names the target case; a row
  holding ignored records also carries the object because B-9 asks for its
  counts, `null` when unknown. The enum-closure disagreement (CAS/pc:1129-1131
  against APO/ov:655-658) is under Open Questions.
- **L-5 to L-9, L-12 to L-14.** The archive order above; issue #24 governs, and
  closing it ends this change; the feature is numbered at `/speckit.specify`
  time; the lane opens the draft PR and runs the alignment review and the
  council; no host-absolute path in any file here, and the bidi check runs on
  every edit. Since PR #32 (merged 2026-10-15) CI runs the suite on Linux only,
  as the jobs `test (3.10)` and `test (3.12)` on `ubuntu-latest`, so every
  statement here that only macOS CI could have checked reads "not verified by
  CI" (L-12, B-15). Commits carry the `Lane:` line and the attribution in force
  (L-13). The Status line and `tasks.md` 1.2 record the resolved review
  (L-14), and, after the council, the Status line reads "alignment review and
  council resolved on PR #27; ratification by Brett Heap pending".
- **L-16 and L-17.** This change's two blocks that PR #19 also amends, "Clean
  bounds its Git work and reports omitted work" and "Cleanup revalidates
  destructive actions", were already written on PR #19's text; under L-16 this
  change also archives after PR #19's amendment of change 1 lands, and the two
  passages that rest on PR #19's wording are marked pending (lane 3's LOW 9).
  L-17's evidence-model block is A's and C's: this change does not modify
  "Repository inspection requires Git 2.36 and shares one evidence model",
  since its cache removals are filesystem calls, not children, and the
  enumeration is a probe child that model already bounds.
- **B-1, the allowlist** (no cache defined in the packet; PR #2's `1789ad9`
  allowlist): applied as written, with CD-8; other kinds are an Open Question.
- **B-2, detection** (the combined probe's bounds, `BA:795-806`): applied, with
  CD-5 and CD-6.
- **B-3, the caps** (`BA:1336-1337` sets no number): the four as ruled, and CD-6
  adds the enumeration count; before Brett Heap under Open Questions.
- **B-4, identities and the digest** (`BA:1327`, "the planned device/inode",
  names no plan field): applied; the digest's placement is B-10 (CD-14).
- **B-5, the ladder** (CAS/pc:107-111, the fifth rung): applied; doctor
  classifies no worktree, and the overview's equality clause is B-14.
- **B-6, preflight and partial phase** (`BA:1332-1337`; PR #2 thread
  3989548481): the whole-list preflight and the partial record applied, read
  as CD-1 to CD-3, which B-11 accepted. `BA:1334`'s "the report rescans the
  worktree" is read as the rescan of the listed paths beside the target's
  reconciliation (lane 3's LOW 2; design D8).
- **B-7, the residual window** (`BA:319-323`): applied in the MODIFIED narrow
  guarantee and the residual-window line.
- **B-8, the stage order** (`BA:1318-1322`, "cache disposal before the worktree
  removal"): applied, with CD-10 and CD-11.
- **B-9, the counts** (APO proposal.md:804-809 hands this extension the zero
  `disposable` and `blocking` counts of `1789ad9`): applied; unknown is `null`
  in the plan, the report and the human `unknown`.
- **B-10, three more MODIFIED blocks** (the alignment review's G1, SA-1, SA-2
  and CD-14): "Clean previews and applies a batch of eligible worktree removals
  in one repository" for the digest, "Cleanup states a narrow guarantee and its
  residual window" for the revalidation before a cache stage and the stage's
  own guarantee, and "Clean records a reconcilable result for every removal
  target" for the deletion exception and the widened `refused` stage, each
  carrying its whole source text and every scenario.
- **B-11, CD-1 to CD-3 accepted** (G4): the consistent reading of B-6 under L-4
  and change 1's stop rule; B-6 is amended to match.
- **B-12, the sample test** (G5, QA-2): a candidate whose combined probe's
  `ignored_samples` hold a path the allowlist rejects by its name or encoding
  stays `ignored-local-files` as `not-candidate` without an enumeration, its
  rejected samples in `blocking_samples`. What can still stall is stated
  exactly (CD-6), and the drain is not claimed unconditionally.
- **B-14, the overview exception rides here** (G2; CD-17): a
  `project-overview` delta modifying change 2's "Overview reuses the cleanup
  classifier and merge target", lane openRepoProject-4's two sentences appended
  verbatim to its equality clause, with one scenario; this change archives
  after change 2. B-22 rewords the two sentences.

The council's verdicts, ruled by the lead on 2026-10-19 (B-16 to B-24, and S-4
NOTED; the table "Council Verdicts" below):

- **B-16, the stage's removals and its commit point** (S-1, AE-1, P-3 item 5,
  Codex's P1 on `3c08613`; change 1 waits for its removal child, CAS/cmd:181-183,
  and abandons only reads, CAS design.md:304-306). The stage's unlinks and
  directory removals are treated as change 1 treats its removal child, never as
  a read: each is handed over only while more than the removal floor remains
  and waited for until it returns; only the 300 s removal ceiling, counted from
  the hand-off, ends that wait, the listed cache it belongs to then being
  `removed: null`; the worker gets no further call, and no descriptor given to
  an outstanding call is closed before `project` exits. Reads keep `min(5 s,
  work remaining less the removal floor)`. The hand-off of the first removal is
  the stage's first removal for every rule of both ADDED requirements: after
  it the stage ends `disposed` or `partial`, except `refused`, nothing deleted,
  when every call handed over returned and none removed an entry (B-20);
  `entries_removed` and `operations.performed` count the removals that
  returned; "nothing was deleted" is printed only when nothing was removed and
  no call is outstanding, and the partial line names a path whose call is
  outstanding as one that may still be removed. That the ceiling case makes the
  later targets `not-attempted` with `deadline-exceeded` and exits 1 is this
  proposal's reading: past 300 s the work deadline has passed, and change 1's
  `removal-ceiling` exits 1. Since the target itself is `refused` with
  `state-changed`, the reconcilable-result block's exit table names the case
  in its row 2, so that an only or last target also exits 1 (re-read MEDIUM 1,
  B-27). The fit is restated in design D4.
- **B-17, signals and `not-attempted` after a cache stage** (AE-3, lane 3's M2,
  Codex's P2 on `3c08613`, P-3 item 3). The second floor and signal check sits
  immediately before the hand-off of the first removal, after the whole-list
  preflight and once the first listed cache's chain is reopened; a signal
  recorded after it is handled as one received during the removals. The
  MODIFIED "Clean records a reconcilable result for every removal target"
  widens its `not-attempted` stage to a target whose cache stage ended
  `disposed` and whose removal a signal or the floor stopped (re-read MEDIUM
  2), gives such a target its reconciliation once its stage removed an entry,
  and lets a cache stage that has handed over its first removal run to its end
  in its signal paragraph (L-11; re-read LOW 1). QA-3's
  `refused`/`state-changed` mapping for the floor case stays. A run that stops
  after a `disposed` stage and before the spawn prints `Cache disposal at PATH:
  removed N cache paths; the worktree was not removed.` before its stop block.
  The design's Risks and Rollback call only `__pycache__` entries regenerable,
  a loose `.pyc` possibly being sourceless.
- **B-18, the partial-stage rescan** (S-2, AE-1). It opens the
  identity-checked descriptor chain to each listed cache's parent, as the
  removals do, and `lstat`s the cache's name relative to it without following
  a symbolic link; a chain that does not open, or whose identity differs,
  leaves that cache `removed: null`; it runs as a reconciliation probe, each
  call on a thread of its own under `min(5 s, reserve remaining)`, never on the
  stage's worker, and its first call past budget leaves that cache and every
  later one `removed: null`. The draft's root-relative `lstat` followed a
  swapped ancestor out of the worktree (both council members reproduced it).
- **B-19, the widened residual window** (S-3, AE-4, lane 3's M1): stated, not
  closed. For a cache target the window includes ignored files created during
  its cache stage outside the listed caches, which Git's non-force removal
  deletes with the worktree, and the residual-window line names them; CD-18's
  "safer" is limited to files placed in a listed cache directory. The bound, as
  measured: a 512-entry stage took about 0.25 s on this workstation on
  2026-10-19, and task 2.3 re-measures it. Rejected alternative: one combined
  status probe in each target after a `disposed` stage, which would restore
  change 1's window at one Git child per cache target, at most 266 children
  and about 44.7 s at the packet's model before any filesystem time, and, with
  the walk and the stages at B-25's bound, about one target fewer: 14 of 16
  targets reach their stage with it, against 15 of 16 without (design D13).
  Under #23's flag B-19 put it at 12 of 16, one fewer than #23's 13 at
  `ca96701`, with the cache-stage filesystem time excluded; #26 restates its
  count under A-23 and A-24 (design D4, B-35).
  The packet bounds the residual window as "typically well under a
  second" (`BA:319-325`), and concurrent writers are outside the contract
  (CAS/rs:196-198).
- **B-20, a cache the user cannot change** (AE-2; A-17's principle for a
  refusal the plan can see). The plan-time walk checks, for each directory a
  stage would change (each listed cache directory, each nested `__pycache__`
  and the parent of each listed path), that the running user may remove
  entries from it: one descriptor-relative access check with effective ids,
  following no symbolic link, under the per-call budget. A failure keeps the
  candidate `ignored-local-files` with `cache_disposal.reason`
  `cache-unwritable` (the sub-record's own enum, L-4), its counts established,
  not selected and stopping nothing; its line says to fix the ownership or mode
  of the worktree's caches and re-run. A failure the check cannot see (a sticky
  directory, `EROFS`) ends the stage `refused` with `cache-changed`, nothing
  deleted, when every call handed over has returned and none removed an entry
  (B-16). The platform check gains the three `os.access` support checks.
- **B-21, stop and stall lines name their cause** (P-3 items 1 and 4, AE-5,
  Codex's P2 on `3c08613`). The stall line is printed only when each of the
  first 16 candidates in canonical order is held at the rung for a persistent
  reason, any one of `blocking` above 0, `cache-cap` from a per-worktree cap,
  `cache-unverified` or `cache-unwritable`, never on `blocking` alone (B-32),
  and is built from those rows' reasons, zero counts left out, each cause with
  its next
  step; it never tells the person to remove by hand a worktree whose state was
  not established. The `cache-unwritable` part is this proposal's completion
  of B-21 for B-20's reason, since sixteen such rows stall the same way. A
  partial stage that the work deadline ended says so, with the remaining paths
  and the fresh-plan command, and does not read as `state-changed`; the target's
  JSON stays as CD-2 has it, and change 1's stop block keeps its form.
- **B-22, the overview exception and the carried classifier scenarios** (P-4,
  lane 3's M4 and M5, lane openRepoProject-4's precision). The two sentences of
  the `project-overview` block become, as committed in `9f30fb9`: "Except: the
  overview collects no cache evidence, so a worktree that `project clean`
  classifies `merged-removable` because clean's cache enumeration proved every
  ignored path a listed cache SHALL be classified `ignored-local-files` by the
  overview. The overview SHALL NOT classify a worktree `merged-removable` where
  `project clean` classifies it otherwise." The new scenario's fixture gains a
  third cache-only, merged worktree holding an initialized submodule, which
  the overview classifies `ignored-local-files` and `project clean` classifies
  `merged-removable` and excludes as `contains-submodule`. Both carried
  "Every protected classifier" scenarios name their ignored file as not a
  Python bytecode cache. Lane openRepoProject-4 agreed the `project-overview`
  edit on 2026-10-19, with one optional point, "clean's" for "its" before
  "cache enumeration", which the committed text takes (`9f30fb9`; `tasks.md`
  2.2), and which this proposal's and the design's paraphrases now follow
  (B-28); the `project-clean` edit is committed. B-30 then scopes the second
  sentence to "the same working directory and refs", in lane 4's own words
  (`4d5855a`).
- **B-23, `.pytest_cache` and the benefit claimed** (P-1). Why gives the
  measured numbers, and "Behaviour users will notice" says "(measured
  2026-10-19: 13 of 37 such rows)", naming no repository and no host path. The
  Open Question "Other cache kinds" is split: `.pytest_cache` goes to Brett
  Heap with the recommendation to admit it here as a third listed form; the
  rest stays under the existing "no". This round does not add the third form;
  it is added only on his answer.
- **B-24, what really blocks a cache-only row** (P-2). A row whose
  `cache_disposal.reason` is `not-candidate` and whose samples pass the sample
  test carries `candidate_block`: the class the ladder gives it with the
  `ignored-local-files` rung skipped, when that class is not
  `merged-removable`, or else the first gate before `deferred-target-cap` that
  it fails, from the existing class and gate enums (L-4, CD-13, CD-16), printed
  with that class's or gate's next step. Computing it needs no Git child the
  classifier does not already run, since the candidate test already holds both
  answers, so there is no gap to record (design D2).
- **S-4 (NOTED), the pre-handoff and landing gates** are recorded in
  `clarifications.md` and answered by design D4 (the measured dispatch cost),
  D14 (test names), the Migration Plan's step 7 and `tasks.md` 2.3 and 3.1.

The re-read and Codex findings of 2026-10-20, ruled by the lead as B-25 to
B-28 (the table "Re-read and Codex Findings (round B3)" below):

- **B-25, the walk's bound** (Codex's P2 at design.md:294 on `90d18ee`). Each
  of the 16 enumerated rows can be walked to its per-worktree cap of 512
  entries before the invocation's totals reject it, and a rejected row is
  uncounted from the 4,096 but was walked, so the plan-time walk's bound is
  16 x 512 = 8,192 entries, about 9,000 calls, about 2 s through one worker
  and about 5.6 s at a thread per call (B-33 counts the recorded directories in
  those 512, and states the worst case of trees that are not ordinary). Design
  D4 restates the fit and every figure that depends on the walk, with the
  arithmetic: at the packet's model and the top of the measured cost the 16th
  target, which lists no cache there, reaches its spawn at about 45.5 s, with
  about 4.5 s left, under the floor (B-31), so 15 of 16 targets reach their
  stage or spawn and the 16th is deferred to the next run with exit 1,
  never unsafe; at a thread per call as few as 8 of 16; at change 1's measured
  costs all 16. No cap changes, and the caps stay before Brett Heap (Open
  Questions). Task 2.3 measures the walk at 16 rows of 512 entries with the
  totals reached.
- **B-26, the run's byte total at the preflight** (Codex's P2 at
  `specs/project-clean-review-safety/spec.md:341` on `90d18ee`). A `.pyc`
  recompiled in place keeps its name, type and entry count, so it passes the
  revalidation and the preflight's count, but it can grow, and five targets
  planned with tiny caches could each reach 256 MiB. The whole-list preflight
  therefore also keeps the run's byte total, the bytes it measures for this
  target and for every earlier target whose stage passed its preflight in this
  run, and a target that would take it past 1 GiB ends `refused` with
  `cache-changed`, nothing deleted, as one past the per-worktree cap does.
  Entries need no running total, since the preflight requires each listed
  cache's planned entry count. The scenario "Caches that grew after the plan
  cannot pass the run's byte cap" pins it (design D1, D4, D7).
- **B-27, lane openRepoProject-3's re-read of `e906c2f`.** Every item is
  applied as lane 3 words its fix, LOW 3 with a change: the exit table's row 2
  names a cache stage's removal that reached the removal ceiling; the
  `not-attempted` stage names a target whose cache stage ended `disposed`; the
  signal paragraph names a cache stage that has handed over its first removal;
  the residual window's two items share one relative clause; and `tasks.md` 2.2
  quotes lane 4 from lane openRepoProject-4's own log, at its lines 47 and 49
  for the second agreement as lane 3 words it, and, since those lines do not
  record the first agreement, at its lines 32 and 37 and lane 5's line 27 for
  that one, dropping the words found in no log, which is the change (delta
  read LOW (2), B-31). The counts of `tasks.md` 1.4 and design D14 were
  recounted at `e906c2f` and were right.
- **B-28, three paraphrases.** What Changes, the B-22 decision above and design
  D6 read "because clean's cache enumeration proved", as the committed
  `project-overview` delta (`9f30fb9`) does.

The findings of 2026-10-20 that followed round B3, ruled by the lead as B-29
to B-33 (the table "Re-read and Codex Findings (round B4)" below):

- **B-29, the overview block re-aligned before the archive** (lane
  openRepoProject-4's F2). This change's `project-overview` block MODIFIES
  change 2's "Overview reuses the cleanup classifier and merge target" whole,
  so an amendment of change 2 that lands before this change archives, such as
  lane 4's planned one for feature 005's open Q7 A, would be dropped silently
  at the archive. `tasks.md` gains 3.2, modeled on #29's 2.3: before
  `/opsx:archive`, the block is re-read against main's text and re-copied,
  keeping every amendment, verified by a `diff -u` of main's block against this
  change's showing additions only and by the validation passing again; the
  archive becomes 3.3. Dependencies and Sequencing (Change 2) and the design's
  Migration Plan say the same.
- **B-30, the SHALL NOT's scope** (lane 4's F4). Read alone, "The overview
  SHALL NOT classify a worktree `merged-removable` where `project clean`
  classifies it otherwise" bound runs from different directories, where the
  current worktree decides `merged-current` against `merged-removable`, though
  the sentence before it carries the scope. The sentence now ends "for the same
  working directory and refs", lane 4's own words, verbatim, and the added
  scenario's AND follows; the edit is committed alone as `4d5855a`, which went
  to lane 4 for a byte check, `tasks.md` 2.2 being reopened until that check
  was cited; lane 4 gave it on 2026-10-20 and 2.2 is ticked again (B-36).
  Design D6's paraphrase follows.
- **B-31, lane openRepoProject-3's delta read of `cf57956`.** It found no HIGH
  and no MEDIUM, every B-25 figure holding and B-26 and B-27 applied as worded,
  and its four optional LOWs are applied: (1) the ADDED requirement's exit
  sentence names the removal ceiling beside a signal and the deadline, and its
  "SHALL be 1" gains "unless a signal decides it", as the exit table orders
  them; (2) the B-27 decision above says that LOW 3 was applied with a change,
  as the round B3 table does; (3) What Changes, the B-25 decision and design D4
  say that in D4's case the 16th target lists no cache, so the floor refuses
  its removal's spawn, not a cache stage; (4) the Open Question on the caps
  says what the packet's rule would give if the filesystem time counted in the
  fit.
- **B-32, the stall test keys on reasons** (Codex's P2 at
  `specs/project-clean/spec.md:910` on `cf57956`). The data contract leaves
  `blocking` null for `cache-cap` and `cache-unverified` and 0 for
  `cache-unwritable`, so a test read on `blocking` could not print the line for
  rows held by those. The ADDED requirement now lists the persistent reasons as
  an explicit disjunction: `blocking` above 0; `cache-cap` from a per-worktree
  cap, never from the invocation's totals or the 16-enumeration cap;
  `cache-unverified`; `cache-unwritable`. The report tells a per-worktree cap
  from the totals by the counts the row already carries, null where a
  per-worktree cap stopped the enumeration and established where only the
  totals left the row, so no field is added. An AND of "Cache caps" pins
  sixteen rows held by `cache-unverified`, `cache-unwritable` and a
  per-worktree cap, none with `blocking` above 0, that print the line. Design
  D4 and D11 and the B-21 decision above follow.
- **B-33, directory opens bounded in the fit** (Codex's P2 at `design.md:323`
  on `cf57956`). The preferred form is applied: every directory the plan
  records, those between the worktree root and a listed path included, counts
  toward the per-worktree cap of 512, now a cap on recorded objects, entries
  and directories alike; the stage opens the chain from the root once per
  directory holding a listed path in each pass, not once per entry; and the
  walk, whose form the ruling leaves open, opens each directory it records
  once. Design D4 states the worst case. The chains cost depth times the
  directories with removals, under the 512-object cap at most 43,947 opens a
  pass for one target (a chain of 341 directories whose deepest 171 each hold
  one loose `.pyc`), about 19.8 s at 224 us, which no fit holds; a depth limit
  alone would not bound a run, so the new limit put to Brett Heap is on the
  chains' opens (Open Questions), and no cap changes. Counting a directory's
  calls as well, four in the walk and five in the stage, a tree of nested
  `__pycache__` directories needs about 32,800 walk calls and 20,480 stage
  calls in a run; the existing caps bound that, but in that shape the report
  mode fits only at 169 us and the all-safe mode brings no target to its stage
  at a thread per call. An AND of "Cache caps" pins the count (a loose `.pyc`
  600 directories deep stays `cache-cap`), design D14 adds a test of one chain
  per directory, and task 2.3 measures the deep-tree worst case.

The findings of 2026-10-20 that followed round B4, ruled by the lead as B-34
to B-37 (the table "Re-read and Codex Findings (round B5)" below):

- **B-34, a preflight that the floor or the deadline stops** (found in round
  B4; Codex's P2 at `specs/project-clean-review-safety/spec.md:353` on
  `e1049b2` is the same item). The preflight's closing sentence ended the stage
  `refused` with `cache-changed` for "a filesystem call that runs out of its
  budget", but a read's budget is `min(5 s, work remaining less the removal
  floor)`: where the second term is the smaller, a read that outlives it, or
  one that cannot start because no more than the floor remains, has found no
  difference, deleted nothing and changed no state, and the bounds rule records
  the first as `deadline-exceeded`. The delta now ends such a stage
  `not-attempted` with `target-stopped` and the target `not-attempted` with
  `deadline-exceeded`, as change 1's deadline rule makes every target whose
  removal cannot start, with `reconciliation: null` and exit status 1, and the
  human result prints `Cache disposal at PATH not attempted (deadline-exceeded);
  nothing was deleted.` before its stop block, so that the deadline is named and
  no change of state is claimed. A preflight that finds a real difference, an
  error, or a read that outlives its own 5 s budget with at least 10 s of work
  left (B-38) stays `refused` with `cache-changed` and exit 2; the last is the
  bounds rule's `probe-timeout`, an ordinary preflight error in Codex's words,
  not deadline exhaustion, though a signal received before its stop is
  classified outranks it (B-39). The new line is printed only for a read stopped
  before the first removal; a stage that never starts, and the check before the
  first hand-off, keep the stop block alone, as they did. CD-2's mapping of a
  floor-ended partial stage to `refused`, and the decline of lane 3's LOW 14,
  concern a stage that has removed an entry, and stand. One AND of "No time for
  a cache stage" pins both outcomes; design D1, D7, D8, D11, D12, D14 and Risks
  follow.
- **B-35, the two drafts describe each other at today's heads** (A-25 for
  #26). Design D4 described #23's joint fit at `ca96701`, "13 of its 16
  targets ... 11 in the worst case", with the cache-stage filesystem time
  excluded. It now describes
  #26 at `9ff8202`, under A-23 and A-24: a flagged run adds at most 81 children,
  64 for the stage and 17 reflog children, and at the packet's 150 ms model,
  with this change's walk and earlier stages added whole, 10 of 16 targets are
  removed and 9 branches retired through one worker per stage, 8 and 8 in the
  worst case of 17 reflog children. Every figure is #26's, read at `9ff8202`
  and checked against its stated arithmetic; none is recomputed here from other
  inputs. Design D13 says "13 of 16 at `ca96701`", and B-19 above "13 at
  `ca96701`". A-25 has #26's own D7 add this change's worst-case shapes at
  `e1049b2`.
- **B-36, `tasks.md` 2.2 ticked again.** Lane openRepoProject-4 agreed B-30 as
  committed in `4d5855a`, and its byte check found the overview delta differs
  from the agreed `9f30fb9` only by "for the same working directory and refs",
  on :35-36 and :74, +3/-2, unchanged through `e1049b2`. Task 2.2 quotes lane
  4's NOTED at line 64 of its log, brett-wip `fab1e721d`, read on the
  register's `origin/main`. This round does not edit the overview delta.
- **B-37, an unsupported platform keeps the earlier rungs** (Codex's P2 at
  `specs/project-clean-review-safety/spec.md:383` on `e1049b2`). "Every row
  that holds ignored records SHALL stay `ignored-local-files`" forced a dirty
  worktree that also holds an ignored file onto a rung that the ladder tests
  after `dirty`, replacing the dirty advice, which is the actionable one,
  merely because cache disposal is unavailable. `cache-unsupported-platform`
  now applies only to a row that reaches the `ignored-local-files` rung; a row
  that `stale-worktree`, `protected-default`, `inspection-error` or `dirty`
  classifies keeps that classification and, where it holds ignored records, its
  `not-candidate` sub-record, as where the calls exist. One AND of "No
  descriptor-relative calls on this platform" adds a dirty worktree that holds
  an ignored `local.env`; CD-3 and design D9 follow.

The findings of 2026-10-20 that followed round B5, ruled by the lead as B-38 to
B-40 (the table "Re-read and Codex Findings (round B6)" below):

- **B-38, lane 3's folded read of `cf57956..fffc194`** (no HIGH, one MEDIUM and
  three LOWs, all accepted; lane 3 confirmed that every B4 and B5 ruling holds
  and recomputed B-33's figures by brute force). The MEDIUM: the last AND of "No
  time for a cache stage" gave `refused` with `cache-changed` to a read held
  "past its 5 s per-call budget with more than 5 s of work remaining", which is
  not the complement of the first half, whose budget `work remaining less the
  removal floor` is under 5 s, so that with 5 to 10 s remaining both halves
  claimed the read. The floor is 5 s, so the first half holds while less than
  10 s of work remains and the second now reads "at least 10 s of work
  remaining", in the delta, in What Changes, in B-34 above and in design D12 and
  D14; no fit or arrival time cites the old threshold, so no figure moves. The
  three LOWs: D7 says "no difference was found" where it said "nothing differs",
  since a read that stopped has not shown that nothing differs; the caps' Open
  Question cites the packet's reapplication rule, `BA:766-771`, which lowers the
  target cap in steps of 8 under a higher measured cost, beside `BA:729-735`;
  and D4 states the call count behind its 28.3 s, 683 calls a row (341 directory
  opens, 171 file `lstat` calls and 171 access checks), 10,928 calls for 16
  rows, 2.45 s at 224 us, added to the 25.8 s of the 172 Git children before the
  first target's stage.
- **B-39, a pending signal outranks a preflight timeout** (Codex's P2 at
  `specs/project-clean-review-safety/spec.md:354` on `fffc194`). The preflight's
  closing sentence ended the stage `refused` with `cache-changed` for "a
  filesystem call that outlives its 5 s per-call budget" unconditionally, but
  the signal scenario of "Clean disposes of listed caches before a worktree
  removal" requires a signal during the whole-list preflight to leave the target
  `not-attempted` with `interrupted`. The handler only records, so a signal
  received while a read is held is seen only at the check before the hand-off,
  which a stage that a timeout has ended never reaches. The delta now says that
  the stage reads the slot before it classifies the stop of any preflight read,
  or of the reopening of the first listed cache's chain, whether a
  `probe-timeout`, the floor or the deadline: where a signal has been received,
  the stage is `not-attempted` with `target-stopped`, nothing deleted, the
  target and every later one `not-attempted` with `interrupted`, and the exit
  status the signal's, never `refused` with `cache-changed` and never
  `deadline-exceeded`. A difference or an error that the preflight did find
  stays `refused`, a finding about the worktree, with the signal's exit status
  as for any target. The line `Cache disposal at PATH not attempted
  (deadline-exceeded)` is printed only where no signal was received. One AND of
  "A signal during a cache stage" pins the outcome and no scenario is added;
  design D1, D7, D8, D11, D12, D14 and Risks, and CD-11, follow.
- **B-40, lane 3's last two LOWs on `fffc194`** (its citation pass resolved 111
  tokens and 25 more that its regex missed, each at the ref it names, and its
  ASCII and bidi grep of all 8 files found nothing; the figures are right). LOW
  1: B-30's row in the round B4 table put the end of the SHALL NOT sentence at
  `spec.md:35`, where it runs :34-36 with the added words on :35-36, so it now
  says `spec.md:35-36`, as `specs/project-overview/spec.md` stands and as lane
  4's byte check and `tasks.md` 2.2 give it; that file is not edited. LOW 2: the
  quotations are made verbatim. #26's draft at `ca96701` reads "13 of its 16
  targets ... 11 in the worst case" in its design.md, so that is what D4 and
  B-35 quote, and B-19 reads "13 at `ca96701`", while design D13 reads "13 of 16
  at `ca96701`", so B-35 says each. Lane 3 also notes that A-25 resolves only at
  #26's `9b67e8c`, where D4's figures hold; nothing was edited for it.

Departures from the rulings as first written, each naming what it departs
from. B-11 accepted CD-1 to CD-3 as the consistent reading of B-6 and amended
B-6 to match, so of these only CD-4 still departs from a ruling, besides
B-22's edit of change 2's carried "Every protected classifier", which departs
from B-14's "plus one scenario" on lane openRepoProject-4's precision and is
ruled by B-22:

- **CD-1, the run stops at a failed cache stage** (departed from B-6's "other
  targets continue"; accepted by B-11). Change 1's retire requirement says
  "Removal SHALL stop after the first target whose result is not a plain
  `removed`, with no continuation" (CAS/pc:246-248), and the packet prefers
  "stop-on-first-failure, consistent with current retirement"
  (`BA:1640-1643`). Continuing would need a second change to that requirement
  beyond the one clause B's brief allows, and would make a cache failure the
  one stop cause that does not stop. Later targets are `not-attempted` with
  `batch-stopped`, or `deadline-exceeded` when the removal floor ended the
  stage; a re-run plans afresh.
- **CD-2, the target's result** (departed from B-6's `cache-changed` as the
  target's refusal and `not-attempted` with `cache-partial` as its removal's
  result; accepted by B-11). Those values would extend the closed reason lists
  of CAS/pc:896-908, against L-4, and `not-attempted` carries a null
  reconciliation and, for a stage that failed, matches no exit row (CAS/pc:906-908,
  :916-919 and :945-956). For the floor case QA-3 kept the same mapping, the exit
  status then being 1 by the deadline row, and lane 3's LOW 14, which asked for
  `not-attempted` there, is declined under it; the human line names the
  deadline instead (B-21). The only `not-attempted` target that carries a
  reconciliation is one whose stage ended `disposed` and whose removal a
  signal or the floor then stopped (B-17, re-read MEDIUM 2).
  Here the target is `refused` with `state-changed` (nothing was spawned; the
  plan no longer held), carries its reconciliation and exits by the existing
  table, and `cache_disposal` carries `refused` with `cache-changed` or
  `partial` with `cache-partial`; the MODIFIED "Clean records a reconcilable
  result for every removal target" (B-10) widens the `refused` stage to name a
  cache stage that ended `refused` or `partial`.
- **CD-3, the platform rule is per row** (departed from B-6's refusal of the
  whole apply as `cache-unsupported-platform`; accepted by B-11). A refusal
  code would extend the closed list of CAS/pc:1113-1119, against L-4, and
  refusing the whole apply would stop change 1's cache-free removals on that
  platform. Here no row gets a cache plan and each that reaches the
  `ignored-local-files` rung holding ignored records keeps it with
  `cache_disposal.reason` `cache-unsupported-platform`, while a row that an
  earlier rung classified keeps that classification (B-37): nothing is deleted
  by `project`, which is the fail-closed outcome `BA:1328` asks for.
- **CD-4, one more MODIFIED block** (departs from B's list as B-10 extends it).
  `Cleanup revalidates destructive actions` requires "the combined status
  probe, which SHALL print no record" (CAS/rs:75-76), which every cache target
  fails, so by L-3 it is modified: for such a target the enumeration's child
  replaces that probe at revalidation and must print exactly the planned
  records, the cache stage's failures refuse with `state-changed`, and the
  revalidation the MUST names is the one before the stage. No other extension
  modifies it. Its block is written on PR #19's text (L-1 and L-15 above).
- **CD-5, the enumeration's argument vector** (completes B-2). B-2 names
  `status --porcelain=v2 --ignored=matching -z`; this adds
  `--untracked-files=normal` and the status pins. Git 2.43 refuses
  `--ignored=matching` with `--untracked-files=no` ("Unsupported combination of
  ignored and untracked-files arguments", exit 128), and a user's
  `status.showUntrackedFiles=no` does the same, so without it the child fails
  for every such user, as change 1 found for its own probe (CAS
  proposal.md:51-53); every status child carries the two status pins
  (CAS/cmd:111-113). This was observed with Git 2.43.0 on Linux (design,
  Context), the platform CI runs.

Lane additions, with no packet or ruling text behind them:

- **CD-6, at most 16 enumerations per invocation** (`limits.cache_rows`). With
  one enumeration per candidate and up to 127 candidates, the plan of 128 rows
  and 16 targets needs 361 Git children, 54.15 s at the packet's 150 ms
  (`BA:729-735`), past the 50 s work deadline; with 16 it needs 250, 37.5 s,
  and, counting Git children and removals, the 16th removal still spawns
  before the floor; with the walk's and the stages' filesystem time at B-25's
  bound, the 16th target is deferred to the next run at the top of the
  measured cost, and B-33's deep trees need a new limit (design D4; Open
  Questions). Candidates past the 16th keep `ignored-local-files` with
  `cache-cap` and drain on re-run unless the first 16 candidates stay held for
  a persistent reason (B-32), a stall the report names, as change 1 names the
  index-gate stall, with each cause and its next step (B-21). The sample test
  (CD-7, B-12) keeps out of the 16 every row whose
  samples show a blocking name; what can still hold a place is a candidate
  whose samples all have cache names while it holds a blocking path beyond its
  8 samples, a cache-named path that is blocking by its type, contents or
  device, more than a per-worktree cap allows, an enumeration that failed, or
  a directory the user cannot change (B-20).
- **CD-7, candidate rows.** Only a linked worktree whose combined probe read
  ignored records and nothing else, whose samples pass the sample test (B-12),
  and which would otherwise be selectable, is enumerated, so the 16
  enumerations are never spent on rows that a gate or a sampled blocking path
  keeps anyway; in single mode that is P alone, since `not-requested` precedes
  the cap. Other rows holding ignored records carry `not-candidate` with `null`
  counts, a row that only the sample test kept out carries the samples it
  rejected in `blocking_samples`, and a row whose samples pass carries the
  class or gate that keeps it in `candidate_block` (B-24).
- **CD-8, device and encoding.** A cache path, or a directory on its way down,
  on a device other than the worktree root's (a mount point inside the
  worktree) is blocking, so disposal never reaches into a mounted tree; a cache
  path that is not valid UTF-8 is blocking, as change 1 never uses such a path
  as an operand.
- **CD-9, a failed enumeration preserves the row, not the plan.** The row
  already has a complete combined probe; a failed, timed-out or inconsistent
  enumeration leaves its ignored paths unproven, `ignored-local-files` with
  `cache-unverified`, and does not make the row `inspection-error` or the plan
  incomplete, which would block every other row's removal. The deadline still
  makes the plan incomplete, as for every probe.
- **CD-10, the stage's time.** It starts only while more than the removal floor
  remains, and each read gets `min(5 s, work remaining less the floor)`; each
  removal is handed over only while more than the floor remains and waited for
  until it returns, up to the 300 s removal ceiling, as a removal child is
  (B-16). So the floor is left for the spawn whenever the removals return in
  time, and no constant is added.
- **CD-11, signals in the stage.** Before the hand-off of its first removal a
  signal stops the target as change 1's slot check does, the slot being read
  before the preflight and again immediately before that hand-off, and where a
  preflight read's wait ends before then, before its stop is classified (B-39);
  after it,
  the stage runs to its end and the slot is read before the spawn, so a signal
  leaves the target's caches either untouched or all removed, never half done
  (B-17).
- **CD-12, `operations` counts removed cache entries** (`BA:1321-1322` and
  `BA:1336-1337` put the mutations in the plan estimate): beside the removal
  children PR #19 places there (draft PR #19, pending), each unlink and
  directory removal that returned having removed its entry counts once.
- **CD-13, the sub-records' shape.** Plan: `disposable`, `blocking`, `reason`,
  `candidate_block` (B-24), `entries`, `bytes`, `paths`, `directories`,
  `blocking_samples` (at most 8, `limits.ignored_samples`). Result: `stage`,
  `reason`, `paths` with a per-path `removed`, `entries`, `entries_removed`.
  Presence follows L-10 and B-13 above.
- **CD-14, the digest** (B-10). Change 1 defines the digest's canonical text as
  the identity fields, the merge target and "the selected `[path, branch,
  head]` triples" (CAS/pc:629-632). The MODIFIED batch block extends a cache
  target's entry with its cache paths and identities and leaves every plan
  without a cache target at change 1's digest. The draft placed this in the
  ADDED requirement as a named departure; the alignment review asked for one
  placement ruling (G1), and B-10 moved it into a MODIFIED block, which #23
  also carries (L-11).
- **CD-15, the question is unchanged.** `Remove N worktrees, keeping N
  branches? [yes/N]` stays; the caches are listed in the plan printed above it,
  as PR #2's design held the remove confirmation sufficient. Changing it would
  change the question sentence that the MODIFIED batch block keeps verbatim,
  and its scenario "Only yes confirms".
- **CD-16, `schema_version` stays 1.** No existing enum gains a value; the new
  objects and keys are additive. Change 1's key lists read as additive
  ("Worktree rows SHALL add", "each target carrying", CAS/pc:1107-1109 and
  :1136-1140), and its `schema_version` rule names renames, removals, type
  changes and changes of meaning, not additions (CAS/pc:1129-1131), so
  "Clean plans and refusals are versioned JSON" needs no MODIFIED block; the
  realization extends feature 004's `WORKTREE_ROW_KEYS`, `SELECTED_KEYS` and
  `TARGET_RESULT_KEYS` in `project` with `cache_disposal` as an optional key,
  as `prunable` already is (lane 3's LOW 10). The packet's "stage values of
  its own" (`BA:1319-1320`) are read as the values of `cache_disposal.stage`,
  since change 1's `stage` enum is closed (CAS/pc:1129-1131; lane 3's LOW 1).
  `candidate_block` takes existing class names and gate reasons, and
  `cache-unwritable` is a value of the sub-record's own `reason` (B-20, B-24).
  `merged-removable` keeps its meaning,
  removable by this tool's gates, and `ignored-local-files` its meaning, holding
  ignored local files not proven disposable (the title of
  `project-clean-review-safety`'s requirement); what grows is the proof.
  `operations` keeps its meaning, the plan's mutations (`BA:1321-1322`), of
  which PR #19's wording (draft PR #19, pending) counts the one kind change 1
  has, the removal; a
  removed cache entry is one more mutation (CD-12), and a plan without caches
  counts as before. Before Brett Heap with L-4's question.
- **CD-17, the overview's equality clause** (B-14, B-22, B-30). Change 2
  requires the overview's classification of every row to equal that of
  `project clean <root> --json`, and its ladder to spawn no probe of its own
  (APO/ov:375-386),
  as the packet decided that overview and clean "always produce the same
  classification" (`DI:618-624`), from which this change departs for the cache
  case (lane 3's LOW 15). After this change, `project clean` classifies a
  cache-proven candidate `merged-removable` on evidence the overview does not
  collect, so the overview reads the same row `ignored-local-files`: the safe
  direction, since its suggestion for that class is the read-only clean
  command (APO/ov:436), but a break of the equality as written. Lane
  openRepoProject-4 asked on 2026-10-11 that the exception ride in this
  change; its two sentences, appended to the equality clause in this change's
  `project-overview` delta, were agreed by lane 4 on 2026-10-19 and committed
  as `b4d3e12`. B-22 rewords them to cover every cache-proven row, those that
  `project clean` then excludes included, and to state the second at the
  classification level, and that edit was agreed by lane 4 on 2026-10-19 and
  committed as `9f30fb9`; B-30 scopes the second to the same working directory
  and refs, in lane 4's own words, committed as `4d5855a` (`tasks.md` 2.2).
  The alternative, the overview
  collecting the same evidence, costs its budget and is out of this change's
  scope.
- **CD-18, an explicit stage rather than letting Git delete.** Git's non-force
  removal deletes ignored files with the worktree (`BA:319-321`), so proving
  the caches at revalidation and leaving the deletion to Git would be simpler.
  The packet and B-8 fix a stage, and the stage is safer for files placed in a
  listed cache directory: Git sees an ignored `__pycache__/` as one record and
  deletes whatever it holds by then, while the stage re-lists each cache
  directory at its preflight, requires the number of entries the plan
  recorded, and removes it only once it has emptied it, so a file placed in a
  cache directory before that directory's removal survives and stops the
  target. An ignored file created elsewhere in the worktree during the stage is
  deleted by Git's removal exactly as under change 1, only after a longer
  window (B-19).

## Corrections to the Packet

None to the packet itself. One to the PR #2 decision record's harvest row,
which the packet links (`OV:186`): "bb91a49's `O_NOFOLLOW`/`dir_fd` deletes
already match the packet's stated requirement" holds only in part, because
`bb91a49` records no planned device or inode and falls back to flag 0 where
`O_NOFOLLOW` is missing (`git show bb91a49 -- project`), where `BA:1326-1328`
asks for both a planned identity and a fail-closed refusal.

## Open Questions

Each is before Brett Heap with a recommendation; the deltas implement the
recommendation, and a different ruling edits them before ratification, except
`.pytest_cache` and the limit on the cache stage's directory opens, whose
recommendations the deltas do not yet implement: each is added only on his
answer (B-23, B-33).

- **Enum closure and `schema_version` (L-4).** Change 1 says "Enums SHALL be
  closed within a schema version" (CAS/pc:1129-1131) and change 2 that "adding
  a field or an enum value is additive" (APO/ov:655-658). Recommendation: this
  change makes the question moot for `clean --json`, since it adds no value to
  any existing enum and puts its own values in the new `cache_disposal`
  sub-records; `schema_version` stays 1 (CD-16). The same holds for
  `operations`, which now also counts removed cache entries. If Brett Heap
  reads a widened `merged-removable` as a change of meaning, the deltas move
  `clean --json` to `schema_version: 2` instead.
- **`.pytest_cache` (B-1, B-23).** Measured 2026-10-19 as the only blocker of
  16 of the 37 kept rows, 12 of which pass every later gate. Each of its 19
  instances has one shape: `.gitignore`, `CACHEDIR.TAG` with the
  cache-directory signature, `README.md` and `v/`; 4 or 5 regular files of at
  most 89 KB; no symbolic link and no executable file. Git prints it as those
  four records, since pytest's own `.gitignore` (`*`) ignores them.
  Recommendation: admit it in this change as a third listed form, under the
  same walk, identities, caps and stage. The form is the ignored records
  `D/.gitignore`, `D/CACHEDIR.TAG`, `D/README.md` and `D/v/` (or `D/` itself
  where an ignore rule names it), of a non-symlink directory `D` whose last
  component is exactly `.pytest_cache`. Its `D/CACHEDIR.TAG` must be a regular
  file whose first 43 bytes are `Signature: 8a477f597d28d172789f06886806bc55`,
  read descriptor-relatively under the per-call budget. Its `D/v/` must hold
  only regular files and non-symlink directories. The sample test accepts a
  sample whose parent component is `.pytest_cache` and whose last is one of
  those four names. The emptied `D` is left for Git's removal, as the Risks
  already say of an emptied `__pycache__`. Alternative: a follow-on change,
  first in line. The deltas do not yet admit it; this round adds the third form
  only on Brett Heap's answer.
- **Other cache kinds (B-1).** `.mypy_cache`, `.ruff_cache`, `node_modules` and
  virtual environments are larger, hold executables or installed state, and
  have no single safe shape. Recommendation: no; each would need its own
  allowlist shape, caps and evidence in its own change.
- **The caps (B-3, CD-6).** 512 recorded objects (the entries and the
  directories the plan records, B-33) and 256 MiB per worktree, 4,096 entries
  and 1 GiB per invocation, 16 enumerations. Recommendation: adopt them, and
  measure the enumeration and the stage before the handoff as change 1's OQ-4
  was (`tasks.md` 2.3); a measured cost that breaks the fit lowers them by that
  rule before the feature starts. Since B-25 bounded the walk at 8,192
  entries, design D4's arithmetic at the packet's 150 ms model brings 15 of 16
  targets through their stage at the top of the measured cost and as few as 8
  at a thread per call, the rest deferred to the next run with exit 1, while
  at change 1's measured costs all 16 fit. If the walk's and the stages'
  filesystem time counted in the fit, the packet's rule (`BA:729-735`), which
  takes the largest multiple of 8 that fits, and its reapplication under a
  higher measured cost (`BA:766-771`), which lowers the target cap in steps of
  8, would lower the target cap from 16 to 8, as #23's A-9 names it for a
  flagged run; this change counts that time outside the fit, as the bounds
  block states, and leaves change 1's
  `limits.targets` at 16 (B-31). B-33's tree of nested `__pycache__`
  directories, within these caps, costs more (design D4: the report mode then
  fits only at 169 us, and at a thread per call no target reaches its stage),
  and the measurement weighs it by the same rule; the caps are unchanged, and
  the measurement decides.
- **A limit on the cache stage's directory opens (B-33).** The 512-object cap
  bounds a row's depth and its number of directories with removals, but the
  stage opens one chain per such directory in each pass, and under that cap
  the opens of a pass reach 43,947 for one target (a chain of 341 directories
  whose deepest 171 each hold one loose `.pyc`), about 19.8 s through one
  worker at 224 us, which no fit holds (design D4). A depth limit alone would
  not bound a run: 8 levels deep, a row can still hold 252 directories with
  removals, 72,576 opens for 16 targets. Recommendation: a new per-worktree
  cap, `limits.cache_opens`, 512: the opens of one pass of the stage along its
  chains, the sum over the directories that hold a listed path of one plus
  each one's depth below the worktree root, as the walk computes it; a row past
  it stays `ignored-local-files` with `cache-cap` from a per-worktree cap, its
  counts null. An ordinary tree stays inside it (a hundred package directories
  four levels deep, each with a `__pycache__`, need 500), and a run's chains
  are then at most 16,384 opens, about 3.7 s at 224 us. Alternative: the stage
  opens each directory once per pass, keeping open the chain above the
  directory it is in, which bounds its opens by the recorded directories with
  no new cap, but checks an ancestor's identity once per pass rather than
  before each directory's removals, the form B-33 did not prefer. The deltas do
  not yet add the cap; it is added only on Brett Heap's answer, measured by
  `tasks.md` 2.3 with the others, and no cap changes before it.

## Questions Resolved by the Alignment Review

The alignment review (stack-architect and qa-lead) ran on `7290100`; the lane's
rulings of 2026-10-18 answered its five GAPs, recorded as the last five rows.

| Findings | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| SA-1: the cache stage removes directories against change 1's "never ... delete a directory itself" | MISMATCH | applied with change: the preferred MODIFY, under B-10; the exception worded as B-10 gives it; recorded as ruling B-10, not as a departure CD-19 | pc MODIFIED "Clean records a reconcilable result for every removal target"; proposal Capabilities, CD-2, Dependencies; design D8, D14, Migration Plan; tasks 1.4 |
| SA-2: the narrow guarantee's revalidation redefined from the ADDED requirement | DRIFT | applied with change: a MODIFIED block under B-10 and L-11 instead of the departure CD-20 | rs MODIFIED "Cleanup states a narrow guarantee and its residual window", rs ADDED last paragraph; proposal Capabilities; design D1, D13 |
| SA-3: "a status probe" makes a failed cache enumeration `inspection-error` | DRIFT | applied | pc MODIFIED classify; proposal Capabilities |
| SA-4: the cache proof depends on caps applied in canonical order | DRIFT | applied | pc MODIFIED classify, pc ADDED reasons |
| SA-5: `operations` widened without naming it | DRIFT | applied | proposal CD-16, Open Questions |
| SA-6: tasks 1.4 claims every scenario byte-exact | DRIFT | applied, with the counts B-10 and B-14 give | tasks 1.4 |
| SA-7: feature 005's fixture stated as fact; the batch requirement called untouched | DRIFT | applied with change: feature 005 has a spec and no plan at `33a1214`, so no fixture is asserted and B-14's test exclusion replaces the confirmation; D14 names the batch block as carried byte-exact | design D6, D14 |
| SA-8: the reflog read is new for an ignored row | DRIFT | applied | design D2 |
| QA-1: a `.pyc` written into a listed directory before revalidation is deleted | MISMATCH | applied | rs ADDED preflight, guarantee and "The whole list is checked before the first removal"; design D5, D7, Risks; proposal What Changes, CD-18 |
| QA-2: "drain on re-run" false when sixteen blocked candidates sort first | MISMATCH | applied with change: B-12's sample test taken; the stall stated exactly; the scenario's blocking path sits beyond the samples, and a `local.env` case shows the sample test | pc ADDED prose, "Cache caps", "Caches beside a blocking ignored file"; proposal What Changes, CD-6, CD-7; design D2, D4 |
| QA-3: the floor reached after the first removal: later targets and exit status | MISMATCH | applied | pc ADDED prose and "The removal floor reached during a cache stage"; rs MODIFIED revalidates; proposal What Changes, CD-1; design D8 |
| QA-4: a signal during the preflight lets every removal run | MISMATCH | applied; also pinned in "A signal during a cache stage" | pc ADDED prose and scenario; proposal CD-11; design D1, D12 |
| QA-5: the fit sentence counts Git children only, and #23 cannot carry it | MISMATCH | applied with change: "as change 1 applies it" dropped, since spec text names no change; the floor clause says "cannot start" so it does not contradict QA-3's refused target | pc MODIFIED bounds |
| QA-6: a recreated directory can reuse its inode on ext4 | MISMATCH | applied | pc MODIFIED batch scenario (moved there by B-10); rs ADDED "The whole list is checked before the first removal" |
| QA-7: no scenario for `cache-unverified` | GAP | applied | pc ADDED "A failed cache enumeration preserves the row, not the plan" |
| QA-8: which fields are null in each `cache-cap` case | GAP | applied with change: the rule also names `not-candidate`, `cache-unverified`, `cache-unsupported-platform` and `blocking_samples`, and B-12's sample-test exception | pc ADDED prose and "Cache caps" |
| QA-9: plan-time directory opens have no budget | GAP | applied | pc MODIFIED bounds, pc ADDED prose |
| QA-10: no scenario for CD-8's two blocking rules | GAP | applied with change: under B-12 the 0xFF path fails the sample test, so the scenario says so | rs ADDED "A symlink named like a cache is never disposable" |
| QA-11: no scenario for the success line, which said "1 worktrees" | GAP | applied with change: singular for a path as well as a worktree | pc ADDED "A merged worktree whose only ignored files are caches"; design D11 |
| B-10 (G1): one placement for the digest, the narrow guarantee and the deletion exception | GAP | ruling: MODIFY all three, each block whole | pc MODIFIED batch and reconcilable result; rs MODIFIED narrow guarantee; proposal Capabilities, Decisions; design D5, D13 |
| B-14 (G2): change 2's equality clause | GAP | ruling: the exception rides in this change as a `project-overview` delta, agreed by lane openRepoProject-4 on 2026-10-19 and committed; this change archives after change 2 | `specs/project-overview/spec.md`; proposal What Changes, Capabilities, Dependencies, CD-17, Open Questions; design D6, D14; tasks 2.2, 3.3 (3.2 before round B4) |
| A-9 (G3): the joint fit of branch retirement and cache disposal | GAP | ruling: #23, which archives second, states it | proposal Dependencies; design D4 |
| B-11 (G4): B-6 against L-4 and change 1's stop rule | GAP | ruling: CD-1 to CD-3 accepted, B-6 amended to match | proposal Decisions |
| B-12 (G5): the candidate pre-filter | GAP | ruling: take the sample test, state what still stalls | pc ADDED; proposal CD-6, CD-7; design D2, D4 |

### Council Verdicts

The council (product-advocate P-1 to P-4, systems-architect S-1 to S-4,
adversary-engineer AE-1 to AE-5, read-only) reviewed `9ebe9f0` on 2026-10-19;
the lane lead's verdicts bind: 12 VALID, 1 NOTED (S-4, in
`clarifications.md`), 0 DISMISSED, ruled as B-16 to B-24. Codex's three inline
findings on `3c08613` and lane openRepoProject-3's packet-fidelity read of
`3c08613` and `9ebe9f0` (M1 to M5, LOW 1 to LOW 17) were weighed by the council
and applied in the same round; their rows follow the council's, and lane
openRepoProject-4's precision is the last row.

| Concern | Severity | Verdict | Section changed |
| --- | --- | --- | --- |
| P-1: the evidence counts `.pytest_cache` as a cache, which the allowlist does not, so the change admits about a third of the rows it is sold on | HIGH | VALID (B-23): Why gives the measured 13 of the 20 and 13 of 37; "Behaviour users will notice" says "(measured 2026-10-19: 13 of 37 such rows)", naming no repository; the Open Question is split, `.pytest_cache` going to Brett Heap with the recommendation to admit it here; the third form is not added this round | Why; What Changes; Out of Scope; Decisions; Open Questions; `design.md` Non-Goals, Risks, Open Questions |
| P-2: a cache-only row that is not a candidate is told to delete its ignored files, though deleting its caches would not make it removable | MEDIUM | VALID (B-24): `candidate_block`, from the existing class and gate enums, printed with its next step; it needs no Git child, so no gap is recorded | What Changes; Decisions; CD-7, CD-13, CD-16; project-clean delta (ADDED, "Unknown counts are null, never zero"); `design.md` D2, D11 |
| P-3: what the person reads after a stage stops does not match what was deleted or what fixes it | MEDIUM | VALID (B-16, B-17, B-21): the stall line by cause; the line after a `disposed` stage; the deadline-ended partial line; "nothing was deleted" only when nothing was and no removal is outstanding | project-clean delta (ADDED); review-safety delta (ADDED); What Changes; `design.md` D11 |
| P-4: the overview exception is false for rows that exist today, and the carried "Every protected classifier" scenarios hold only by a design note | MEDIUM | VALID (B-22): the two sentences reworded, a third, submodule-holding worktree in the fixture, lane 4's precision in both carried scenarios, the overview edit agreed by lane 4 on 2026-10-19 and committed; "Behaviour users will notice" names the overview's report | project-overview delta; project-clean delta (batch block); What Changes; Capabilities; Decisions; CD-17; `design.md` D6, D14; `tasks.md` 1.4, 2.2 |
| S-1: the stage abandons its unlinks at a budget that shrinks to nothing near the floor, and ties its outcomes to the first removal completed | HIGH | VALID (B-16): removals waited for as change 1 waits for its removal child, up to the 300 s ceiling; the hand-off as the one commit point; the second check moved before it (B-17) | bounds and reconcilable-result blocks; both ADDED requirements; What Changes; Rules; Decisions; CD-10, CD-11; `design.md` D1, D4, D7, D8, D12 |
| S-2: the partial rescan establishes nothing at the floor, and its root-relative `lstat` follows a swapped ancestor | MEDIUM | VALID (B-18): S-2's text; the rescan never on the stage's worker | review-safety delta (ADDED); What Changes; `design.md` D8, D12 |
| S-3: the residual window widens over the cache stage | MEDIUM | VALID (B-19) as its stated form: the window stated and bounded as measured; the post-stage status probe rejected and recorded | narrow-guarantee block and its scenario; CD-18; Decisions; `design.md` D13, Risks |
| S-4: the pre-handoff and landing gates check the wrong axes | LOW | NOTED: the measured dispatch cost in D4; task 2.3 through `fs_call`, idle and loaded, the walk included, and on Git 2.36.6; task 3.1 and step 7 on every job, `git-floor` included; test names beginning `test_clean_` | `clarifications.md`; `design.md` D4, D14, Migration Plan; `tasks.md` 2.3, 3.1 |
| AE-1: an abandoned unlink can finish after the record, and a reused descriptor can send it to another directory | HIGH | VALID (B-16, B-18): as S-1 and S-2, with the descriptor rule and the scenario "A removal call that outlives its wait" | review-safety delta (ADDED); Rules; `design.md` D7, D12 |
| AE-2: a cache directory the user cannot write turns an exclusion into a stop of every run | MEDIUM | VALID (B-20): the plan-time access check and `cache-unwritable`; a failure the check cannot see ends the stage `refused`; D9's support checks; the scenario "An unwritable cache directory is kept, not a stop" | classify block; project-clean delta (ADDED); review-safety delta (ADDED); What Changes; Decisions; `design.md` Context, D3, D9, D11, Risks |
| AE-3: a target whose caches were deleted can end `not-attempted` with a null reconciliation, and a signal after the post-preflight check still lets every cache go | MEDIUM | VALID (B-17): the check moved; the reconcilable-result block widened (L-11); QA-3's floor mapping kept; "regenerable" limited to `__pycache__` | reconcilable-result block; project-clean delta (ADDED); CD-2, CD-11; `design.md` D1, D8, D12, Risks, Rollback |
| AE-4: the stage lengthens the residual window, and CD-18's "safer" holds only in the listed directories | LOW | VALID (B-19): its option (a), the window stated, about 0.25 s at 512 entries | as S-3 |
| AE-5: the stall line's text and trigger are wrong for some rows | LOW | VALID (B-21), applied with change: the trigger and text built from the rows' reasons, with a fourth part for B-20's `cache-unwritable`, which stalls the same way | project-clean delta (ADDED, "Cache caps"); CD-6; `design.md` D4, D11 |
| Codex P1, design.md:469 at `3c08613`: an abandoned mutating call can complete unreported | P1 | VALID (B-16) | as S-1 |
| Codex P2, design.md:478 at `3c08613`: a signal between the post-preflight check and the first unlink lets every removal run | P2 | VALID (B-17) | as AE-3 |
| Codex P2, design.md:455 at `3c08613`: the stall line gives one cause whatever the cause | P2 | VALID (B-21) | as AE-5 |
| M1: the residual window is silently widened by the cache stage | MEDIUM | applied (B-19) | as S-3 |
| M2: the signal case contradicts the reconcilable-result block it says it keeps | MEDIUM | applied (B-17) | as AE-3 |
| M3: the overview delta was missing while the change counted it | MEDIUM | resolved by `b4d3e12` | `specs/project-overview/spec.md` |
| M4: the overview exception does not cover every case where the two classifications differ | MEDIUM | applied (B-22), agreed by lane 4 and committed | project-overview delta; CD-17 |
| M5: the second sentence conflicts with change 2's gate rules read at the gate level | MEDIUM | applied (B-22), agreed by lane 4 and committed | project-overview delta; CD-17 |
| LOW 1: "stage values of its own" not acknowledged | LOW | applied: `BA:1319-1320` read as `cache_disposal.stage`'s values | CD-16 |
| LOW 2: "rescans the worktree" narrowed without saying so | LOW | applied: named as this change's reading | Decisions (B-6); `design.md` D8 |
| LOW 3: "any ancestor" narrowed to the directories below the root | LOW | applied: named as this change's reading | Rules; `design.md` D7 |
| LOW 4: "the largest exclusion" is wrong | LOW | applied: the largest among linked worktrees, `main-worktree` larger | Why |
| LOW 5: CAS/pc:906-908 covers only part of its sentence | LOW | applied: CAS/pc:916-919 and :945-956 added | CD-2 |
| LOW 6: OV:188-192 is imprecise | LOW | applied: OV:178-180 | Why |
| LOW 7: question 2 is never recorded | LOW | applied: under Dependencies and Sequencing, as A does | Dependencies and Sequencing; What Changes |
| LOW 8: no cache scenario exercises question 1 | LOW | applied: an upstream-gone, merged, cache-only row, as an AND | project-clean delta (ADDED, "A merged worktree whose only ignored files are caches") |
| LOW 9: two passages use PR #19's wording without saying it is pending | LOW | applied under L-16 | What Changes (Caps); CD-12, CD-16; Dependencies and Sequencing |
| LOW 10: the versioned-JSON requirement is called untouched though its lists grow | LOW | applied with change: one CD-16 sentence, the lists read as additive, no MODIFIED block | CD-16 |
| LOW 11: "Every protected classifier" keeps an unpinned fixture | LOW | applied (B-22), in both carried copies | batch block; project-overview delta; `design.md` D14; `tasks.md` 1.4 |
| LOW 12: some rules have no scenario | LOW | applied: one AND each, for the check before the first hand-off, `cache_bytes_total`, a deadline during an enumeration, `cache-unverified` for no ignored record and for a walk call, and the `refused` human line | project-clean delta (ADDED); review-safety delta (ADDED) |
| LOW 13: D11 says `path_valid_utf8` is always true | LOW | applied: limited to `paths` and `directories` | `design.md` D11 |
| LOW 14: a floor-ended partial stage is reported as `state-changed` | LOW | declined: QA-3 settled the mapping; the human line names the deadline instead (B-21) | CD-2; project-clean delta (ADDED, "The removal floor reached during a cache stage") |
| LOW 15: DI:618-624 is not named as departed from | LOW | applied | CD-17 |
| LOW 16: the task 2.2 tick weakens its own verification | LOW | applied: 2.2 reopened and citing lane 4's agreement by the lane's log records, in place of a link | `tasks.md` 2.2 |
| LOW 17: three wording issues in the overview delta | LOW | applied (B-22): SHALL wording and the third worktree; the paraphrase in What Changes aligned | project-overview delta; What Changes |
| Lane openRepoProject-4's optional precision on "Every protected classifier" | LOW | applied (B-22), in both carried copies, the overview one a departure from B-14's "plus one scenario" | as LOW 11; Decisions |

### Re-read and Codex Findings (round B3)

Lane openRepoProject-3's read-only re-reader re-read this change at `e906c2f`
from a checkpoint at `90d18ee`, and Codex reviewed `90d18ee` in answer to the
`@codex review` comment 6279844648, its two inline findings citing lines
unchanged at `e906c2f`; the lead ruled both on 2026-10-20 as B-25 to B-27 and
added B-28. Lane 3 found no HIGH, and of review-27's 22 ids 20 FIXED, LOW 14
DECLINED with its reason holding and LOW 16 PARTLY, which is its re-read LOW 3
below; of the 9 items here, 8 are applied, 1 is applied with change (re-read
LOW 3), and none is declined.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Codex (90d18ee) P2 at design.md:294: the fit counts the walk over the 4,096 entries the totals admit, though a row they reject was walked to its 512 | P2 | B-25: applied: the walk's bound is 16 x 512 = 8,192 entries, about 9,000 calls, about 2 s through one worker and 5.6 s at a thread per call; D4's fit, the all-safe and report rows, the thread-per-call figure, D13's probe cost and #23's inputs restated with the arithmetic; at the top of the measured cost the 16th target now arrives at about 45.5 s, under the floor (15 of 16 reach their stage; as few as 8 of 16 at a thread per call), which D4 says; no cap changed | `design.md` D4, D13; What Changes (Caps); Dependencies and Sequencing; Decisions (B-19, B-25); CD-6; Open Questions (the caps); `tasks.md` 2.3; `clarifications.md` S-4 |
| Codex (90d18ee) P2 at `specs/project-clean-review-safety/spec.md:341`: the preflight does not reapply the invocation's byte cap, so caches recompiled larger can take a run past 1 GiB | P2 | B-26: applied: the preflight keeps the run's byte total of the bytes it and the earlier passed preflights measured, and a target past 1 GiB ends `refused` with `cache-changed`, nothing deleted; one scenario | review-safety delta (ADDED preflight paragraph; "Caches that grew after the plan cannot pass the run's byte cap"); `design.md` D1, D4, D5, D7, D8, D14, Risks; What Changes (the cache stage); Capabilities; Decisions (B-26); `tasks.md` 1.4 |
| lane 3 re-read (e906c2f) MEDIUM 1: a cache stage's removal at the 300 s ceiling exits 1, but the carried exit table gives 2 when no later target exists | MEDIUM | B-27: applied: row 2 gains "or a cache stage's removal reached the removal ceiling" | project-clean delta (MODIFIED "Clean records a reconcilable result for every removal target"); Capabilities; Decisions (B-16); `design.md` D8 |
| lane 3 re-read (e906c2f) MEDIUM 2: the widened `not-attempted` bullet also matches a stage that ended `refused` or `partial` | MEDIUM | B-27: applied: "for a target whose cache stage ended `disposed`" | project-clean delta (same block); Capabilities; Decisions (B-17); CD-2; `design.md` D8 and its B-17 row |
| lane 3 re-read (e906c2f) LOW 1: "a started cache stage running to its end" conflicts with the commit point | LOW | B-27: applied: "a cache stage that has handed over its first removal" | project-clean delta (same block, signal paragraph); Capabilities; Decisions (B-17); `design.md` D8 |
| lane 3 re-read (e906c2f) LOW 2: the residual window says "which Git's non-force removal deletes with the worktree" twice | LOW | B-27: applied: one relative clause, "both of which" | review-safety delta (MODIFIED "Cleanup states a narrow guarantee and its residual window") |
| lane 3 re-read (e906c2f) LOW 3 (review-27's LOW 16, still PARTLY): `tasks.md` 2.2 quotes lane 4 from lane 5's log, which does not hold those words | LOW | B-27: applied with change: the second agreement and its commit are quoted exactly from lane openRepoProject-4's log at lines 47 and 49, as lane 3 words it; since those lines do not record the first agreement, it is quoted exactly from lane 4's log at lines 32 and 37 and lane 5's log at line 27, and the words found in no log are dropped | `tasks.md` 2.2 |
| lane 3 re-read (90d18ee checkpoint) N-L3: the counts in `tasks.md` 1.4 and design D14 | LOW | B-27: applied: recounted at `e906c2f` by the carry script: 66 carried scenarios, 62 byte-exact and 4 edited, the overview 6 byte-exact, 1 edited and 1 added; both passages were right, so nothing was fixed for N-L3, and only B-26's scenario moves the review-safety count to 28 | none for N-L3 (`tasks.md` 1.4 and design D14 changed for B-26) |
| lead B-28: three paraphrases say "because its cache enumeration proved" where the committed delta says "clean's" | not graded | B-28: applied | What Changes (the overview's equality clause); Decisions (B-22); `design.md` D6 |

### Re-read and Codex Findings (round B4)

Lane openRepoProject-4's review of 2026-10-20 (its findings F2 and F4; F2 is in
lane 4's log at line 55, and the words of F4's fix in its handoff at line 132,
read on the register's `origin/main` at `971bc6eda`), lane openRepoProject-3's
delta read of `e906c2f..cf57956`, sent by message, and Codex's re-review of
`cf57956`, in answer to the `@codex review` comment 6288232873, were ruled by
the lead on 2026-10-20 as B-29 to B-33. Lane 3 found no HIGH and no MEDIUM and
every B-25 figure holding; of the 8 items here, 8 are applied, none with
change and none declined, and B-33's fit puts a new limit to Brett Heap (Open
Questions).

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| lane 4 (2026-10-20) F2: no step re-aligns the `project-overview` block with change 2's text before this change archives, so an amendment of change 2 landing first would be dropped | LOW to MEDIUM | B-29: applied: `tasks.md` 3.2, modeled on #29's 2.3, re-reads the block against main's text before `/opsx:archive` and re-copies it, keeping every amendment, verified by a `diff -u` showing additions only and by the validation passing again; the archive becomes 3.3, and the B-14 row above points to it | `tasks.md` 3.2, 3.3; Dependencies and Sequencing (Archive order, Change 2); Decisions (B-29); `design.md` Migration Plan step 8 |
| lane 4 (2026-10-20) F4: "The overview SHALL NOT classify a worktree `merged-removable` where `project clean` classifies it otherwise" carries no scope, so read alone it binds runs from different directories | LOW | B-30: applied, in lane 4's words, verbatim: the sentence ends "for the same working directory and refs" at spec.md:35-36, the added scenario's AND following; committed alone as `4d5855a` for lane 4's byte check, and `tasks.md` 2.2 reopened until that check is cited | `specs/project-overview/spec.md` (`4d5855a`); What Changes; Capabilities; Dependencies (Implementation order, Change 2); Decisions (B-22, B-30); CD-17; `design.md` D6; `tasks.md` 1.4, 2.2 |
| lane 3 delta read (cf57956) LOW (1): the stage's exit sentence names a signal and the deadline but not the removal ceiling, and its "SHALL be 1" leaves out the signal row | LOW | B-31: applied: "2 unless a signal, the deadline or the removal ceiling decides it" and "SHALL be 1 unless a signal decides it", as the exit table's rows 1 and 2 order them | project-clean delta (ADDED "Clean disposes of listed caches before a worktree removal"); `design.md` D8 |
| lane 3 delta read (cf57956) LOW (2): the B-27 decision says every item was applied as worded, while the round B3 table applies LOW 3 with a change | LOW | B-31: applied | Decisions (B-27) |
| lane 3 delta read (cf57956) LOW (3): in D4's case the 16th target lists no cache, so the floor refuses its removal's spawn, not a cache stage | LOW | B-31: applied | What Changes (Caps); Decisions (B-25); `design.md` D4 |
| lane 3 delta read (cf57956) LOW (4): the caps' Open Question does not say what the packet's rule would give if the filesystem time counted in the fit | LOW | B-31: applied: the target cap would go from 16 to 8, as #23's A-9 names it; this change counts that time outside the fit and leaves `limits.targets` at 16 | Open Questions (the caps) |
| Codex (cf57956) P2 at `specs/project-clean/spec.md:910`: the stall test reads `blocking`, which is null for `cache-cap` and `cache-unverified` and 0 for `cache-unwritable`, so the line those rows need is never printed | P2 | B-32: applied: an explicit disjunction of the four persistent reasons, never `blocking` alone; a per-worktree cap told from the invocation's totals by the row's counts, null or established, so no field is added; an AND of "Cache caps" for sixteen rows held by `cache-unverified`, `cache-unwritable` and a per-worktree cap, none with `blocking` above 0, that print the line | project-clean delta (ADDED prose and "Cache caps"); `design.md` D4, D11; What Changes (Caps); Capabilities; Decisions (B-21, B-32); CD-6 |
| Codex (cf57956) P2 at `design.md:323`: the directories above a listed path are recorded, access-checked and reopened per path without counting toward the caps, so depth leaves the walk's and the stage's calls outside the fit | P2 | B-33: applied, the preferred form: every recorded directory counts toward the per-worktree cap of 512 recorded objects, the stage opens one chain per directory holding a listed path in each pass, and the walk opens each recorded directory once; D4 states the worst case, depth times directories with removals, at most 43,947 opens a pass for one target, which no fit holds, and the shape whose every object is a directory, at four walk calls and five stage calls an object; a limit on the chains' opens, 512 a pass per worktree recommended, put to Brett Heap as an Open Question, since a depth limit alone would not bound a run; no cap changed; an AND for a loose `.pyc` 600 directories deep; task 2.3 adds the deep-tree worst case | project-clean delta (bounds block; ADDED prose and "Cache caps"); review-safety delta (ADDED descriptor paragraph); `design.md` D3, D4, D5, D7, D14, Risks, Migration Plan step 1, Open Questions; What Changes (detection, Caps, the cache stage); Capabilities; Dependencies (Archive order); Decisions (B-25, B-33); CD-6; Open Questions (the caps, the opens limit); `tasks.md` 2.3; `clarifications.md` S-4 |

### Re-read and Codex Findings (round B5)

Codex re-reviewed this change at `e1049b2` and found two P2s (inline comments
4324625878 and 4324625890, read 2026-10-20), and the lead ruled on both on
2026-10-20 as B-34 and B-37, adding B-35, so that the two drafts describe each
other at today's heads, and B-36, lane openRepoProject-4's byte check of B-30's
commit. Lane openRepoProject-3's delta read of `cf57956..e1049b2` had not
arrived when this round was applied; a later round takes it. Of the 4 items
here, 4 are applied, none with change and none declined; B-34 and B-37 are the
rulings on Codex's two findings, each recorded as one item with its ruling.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| Codex (e1049b2) P2 at `specs/project-clean-review-safety/spec.md:353`, and the lead's B-34, found in round B4, the same item: a preflight read whose limiting budget is the deadline, or that the removal floor stops before the first removal, ends the stage `refused` with `cache-changed`, a state-change diagnosis, where the bounds rule records `deadline-exceeded` and makes every target whose removal cannot start `not-attempted` | P2 | B-34: applied: a read that cannot start because no more than the floor remains, or that outlives the budget that the deadline set, ends the stage `not-attempted` with `target-stopped` and the target `not-attempted` with `deadline-exceeded`, `reconciliation: null`, exit 1, and the human result prints `Cache disposal at PATH not attempted (deadline-exceeded); nothing was deleted.` before its stop block; a real difference, an error and a read past its own 5 s budget stay `refused` with `cache-changed`, exit 2; one AND of "No time for a cache stage" pins both outcomes | review-safety delta (ADDED preflight paragraph); project-clean delta (ADDED stage paragraph and human lines; "No time for a cache stage"); `design.md` D1, D4, D7, D8, D11, D12, D14, Risks; What Changes (Failure and recovery, What the person sees); Capabilities; Decisions (B-34) |
| lead B-35 (A-25 for #26): D4 still describes #23's joint fit at `ca96701`, "13 of its 16 targets ... 11 in the worst case", with the cache-stage filesystem time excluded | not graded | B-35: applied: D4 describes #26 at `9ff8202` under A-23 and A-24: at most 81 children, and at the packet's model with cache disposal 10 of 16 targets removed and 9 branches retired through one worker, 8 and 8 in the worst case of 17 reflog children; every figure is #26's, checked against its own arithmetic; no cap changed, `limits.targets` 16 and A-9 still Brett Heap's; D13 reads "13 of 16 at `ca96701`" and the B-19 decision "13 at `ca96701`" | `design.md` Context, D4, D13; Decisions (B-19, B-35) |
| lead B-36: `tasks.md` 2.2 stands reopened until lane openRepoProject-4's byte check of B-30's commit is cited | not graded | B-36: applied: ticked again, citing lane 4's NOTED at line 64 of `lanes/log/openRepoProject-4.md` (2026-10-20T11:50:06Z, brett-wip `fab1e721d`, an ancestor of the register's `origin/main` at `fa9800bad`), quoted exactly: the overview delta differs from the agreed `9f30fb9` only by "for the same working directory and refs", on :35-36 and :74, +3/-2, unchanged through `e1049b2`; `specs/project-overview/spec.md` is not edited this round | `tasks.md` 2.2; Status; What Changes; Dependencies (Implementation order); Decisions (B-30, B-36); `design.md` D6, Migration Plan |
| Codex (e1049b2) P2 at `specs/project-clean-review-safety/spec.md:383`, and the lead's B-37: on a platform without the descriptor-relative calls, "every row that holds ignored records" is forced to `ignored-local-files`, so a dirty worktree that also holds an ignored file loses the `dirty` classification, which the ladder tests first, and its actionable diagnosis | P2 | B-37: applied: `cache-unsupported-platform` applies only to a row that reaches the `ignored-local-files` rung; a row classified by `stale-worktree`, `protected-default`, `inspection-error` or `dirty` keeps that classification and, where it holds ignored records, its `not-candidate` sub-record as where the calls exist; one AND of "No descriptor-relative calls on this platform" adds a dirty worktree that holds an ignored `local.env` | review-safety delta (ADDED platform paragraph; "No descriptor-relative calls on this platform"); `design.md` D9; What Changes (Fail closed per platform); Capabilities; Decisions (B-37), CD-3 |

### Re-read and Codex Findings (round B6)

Lane openRepoProject-3's folded read of this change over `cf57956..fffc194`,
sent by message on 2026-10-20 at about 16:3xZ, with its two last checks, the
citation pass and the ASCII grep, and Codex's inline finding on `fffc194`
(comment 4327345826, 2026-10-20T16:16:38Z), were ruled by the lead on 2026-10-20
as B-38, B-39 and B-40, for a short round after the 20:50Z reset. Lane 3 found
no HIGH and confirmed that every B4 and B5 ruling holds, recomputing B-33's
figures by brute force; of the 7 items here, 7 are applied, none with change and
none declined. `specs/project-overview/spec.md` is not edited: none of the
rulings needs it, and its block is lane openRepoProject-4's.

| Finding | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| lane 3 folded read (fffc194) M1: the last AND of "No time for a cache stage" says "past its 5 s per-call budget with more than 5 s of work remaining", which is not the complement of the first half's `work remaining less the removal floor` being under 5 s, so with 5 to 10 s remaining both halves claim the read | MEDIUM | B-38: applied: "at least 10 s of work remaining", the floor being 5 s, in the delta, What Changes, B-34's decision and design D12 and D14; checked that no fit or arrival time cites the old threshold, so no figure changes | project-clean delta ("No time for a cache stage"); What Changes (Failure and recovery); Decisions (B-34, B-38); `design.md` D12, D14 |
| lane 3 folded read (fffc194) LOW 1: design D7 says "nothing differs" of a read that stopped before it finished | LOW | B-38: applied: "no difference was found before the read stopped" | `design.md` D7 |
| lane 3 folded read (fffc194) LOW 2: the caps' Open Question cites `BA:729-735` alone for the rule that lowers the target cap, where `BA:766-771` states its reapplication under a higher measured cost | LOW | B-38: applied: both cited, the second for the steps of 8 | Open Questions (the caps); Decisions (B-38) |
| lane 3 folded read (fffc194) LOW 3: design D4's 28.3 s for the first deep-tree target is stated without the walk's call count | LOW | B-38: applied: 683 calls a row (341 directory opens, 171 file `lstat` calls and 171 access checks), 10,928 for 16 rows, 2.45 s at 224 us, added to the 25.8 s of the 172 Git children before the target; the worktree root's own open is a 684th call a row, named in D4, which moves nothing at this precision (16 x 684 x 224 us is also 2.45 s) | `design.md` D4; Decisions (B-38) |
| Codex (fffc194) P2 at `specs/project-clean-review-safety/spec.md:354`, and the lead's B-39: a call past its 5 s budget is unconditionally `refused` with `cache-changed`, which contradicts the signal scenario when SIGINT arrived while the read was held | P2 | B-39: applied: the stage reads the slot before it classifies the stop of any preflight read, a `probe-timeout`, the floor or the deadline alike; where a signal has been received the stage is `not-attempted` with `target-stopped`, nothing deleted, the target and every later one `not-attempted` with `interrupted`, and the exit status the signal's, never `refused` with `cache-changed`; a difference or an error that the preflight did find stays `refused`; the deadline line is printed only where no signal was received; one AND of "A signal during a cache stage", so no scenario is added and the counts stay 55, 28 and 8 | review-safety delta (ADDED preflight paragraph); project-clean delta (ADDED stage paragraph and human lines; "A signal during a cache stage"); `design.md` D1, D7, D8, D11, D12, D14, Risks; What Changes (Failure and recovery, What the person sees); Capabilities; Decisions (B-34, B-39); CD-11 |
| lane 3's last checks (fffc194) LOW 1: B-30's row in the round B4 table says the SHALL NOT sentence ends "for the same working directory and refs" at `spec.md:35`, where it runs :34-36, the added words on :35-36 | LOW | B-40: applied: `spec.md:35-36`, re-checked against `specs/project-overview/spec.md` as it stands (the sentence on :34-36, "for" ending :35 and "the same working directory and refs." on :36); that file is not edited | the round B4 table (B-30's row); Decisions (B-40) |
| lane 3's last checks (fffc194) LOW 2: the quotations are not verbatim: D4 and the proposal quote #26's `ca96701` as "13 of 16, 11 in its worst case", where its design.md:573 reads "13 of its 16 targets ... 11 in the worst case", and say B-19 reads "13 of 16 at `ca96701`", where B-19 reads "13 at `ca96701`" and only design D13 reads "13 of 16 at `ca96701`" | LOW | B-40: applied: #26's words quoted as "13 of its 16 targets ... 11 in the worst case" in design D4, in B-35 and in the round B5 table's B-35 row, and B-35 now says that D13 reads "13 of 16 at `ca96701`" and B-19 "13 at `ca96701`"; the figures were right and none changes; the ca96701 text was read with `git show ca96701:openspec/changes/add-project-clean-branch-retirement/design.md` | `design.md` D4; Decisions (B-35, B-40); the round B5 table (B-35's row) |
