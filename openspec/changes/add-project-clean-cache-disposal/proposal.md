Lane: openRepoProject-5

# Proposal: add-project-clean-cache-disposal

Status: draft; alignment review and council pending (lane openRepoProject-5
runs them on this draft); nothing here is ratified. Governing issue:
opensoft/openRepoProject#24, claimed by lane openRepoProject-5 (comment
6111257933); refs #6, the record of the project maintenance design packet.
Proposed on Brett Heap's word "usage reset, resume all. read handoff and resume
and fan out wide and do as much as possible in parallel" (2026-10-11), read by
lanes openRepoProject-4 and openRepoProject-5 as a go for the candidate list
they put to him.

Citations are `file:line` at `da33d92`, which equals `961c405` for
`ideation/`. `BA`, `SY`, `OV` and `HO` are the packet's `project-maintenance-`
files `batch-cleanup.md`, `synthesis-inspect-and-retire.md` and `overview.md`,
and `next-session-project-maintenance-fix-handoff.md`. `CAS` is
`openspec/changes/add-project-clean-all-safe/` (change 1) and `APO` is
`openspec/changes/add-project-overview/` (change 2), both ratified and
unarchived at `961c405`; `CAS/pc`, `CAS/rs`, `CAS/cmd` and `APO/ov` are their
`project-clean`, `project-clean-review-safety`, `project-command` and
`project-overview` deltas. `PR19/pc` is `CAS/pc` as draft PR #19 amends it
(branch `change/amend-clean-all-safe-push-pins`, head `c462d87`, whose spec
text equals the `5ce23d7` that the lane's rulings name), and `PR19/rs` is
`CAS/rs` as PR #19 amends it at that head. `project:N` is the
executable at `961c405`. L-n and B-n are the lane's rulings of 2026-10-11 for
the three extensions and for this one; CD-n are this proposal's own decisions.
The packet is non-normative brainstorm material (`OV:16-19`); only the deltas
that follow will be normative.

## Why

Change 1 removes only worktrees with no ignored files, on purpose: "caches
such as `__pycache__` keep a worktree out until the cache-disposal change"
(CAS proposal.md:72-75). A merged, clean, published worktree whose only extra
content is Python bytecode is therefore classified `ignored-local-files` and
kept, run after run, although nothing in it is work. Change 1's measurement
found `ignored-local-files` the largest exclusion, 102 of 561 rows
(CAS tasks.md:85-87), and its council found 20 of Omnigent-Install's 29 merged
worktrees excluded for caches alone (CAS proposal.md:697-699; PR #16 at
`841c7dc` cites the same count as the evidence for this change). Change 1
names cache disposal "the first follow-on change" (CAS proposal.md:697).

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
`OV:188-192`).

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
  `project clean <root> --all-safe` and removable by `--apply --action remove
  --worktree P`: the preview lists its caches, and apply disposes of them in a
  cache stage, then removes the worktree exactly as change 1 does, its branch
  kept. A worktree holding any other ignored file stays `ignored-local-files`,
  and its preview now says how many of its ignored paths are disposable and how
  many block it, naming the first that blocks. For a worktree with no ignored
  files nothing changes: its plan, digest, question, stages and exit status are
  change 1's.
- **The allowlist (B-1).** A listed cache is an ignored path that is either a
  directory named `__pycache__` whose entries are only regular files whose
  names end `.pyc` or `.pyo` and directories named `__pycache__` of the same
  shape, or a regular file whose name ends `.pyc` or `.pyo`, none of them a
  symbolic link. Every directory between the worktree root and a listed path
  must be a non-symlink directory on the worktree root's device, and the path
  must be valid UTF-8 (CD-8). Every other ignored path is blocking. Other cache
  kinds are out of scope (Open Questions).
- **Detection by a bounded enumeration of its own (B-2).** The combined status
  probe stops at the 65th ignored record and keeps eight samples
  (CAS/cmd:161-173), so it cannot prove a whole worktree disposable. A
  candidate row is a linked worktree whose combined probe read ignored records
  and nothing else and which, its ignored records aside, would be
  `merged-removable` and pass every gate before `deferred-target-cap` (CD-7).
  For each, in canonical order and at most 16 per invocation (CD-6), `project
  clean` runs one more Git child in that worktree, `status --porcelain=v2 -z
  --untracked-files=normal --ignored=matching`, under the evidence model's
  scrub, protocol pins and directory rule and with the status pins (CD-5),
  reading at most 512 records, then walks each listed `__pycache__`
  directory descriptor-relatively. A row whose enumeration reaches a cap
  stays `ignored-local-files` with the reason `cache-cap`; one whose
  enumeration fails, times out, or reads anything but ignored records stays
  `ignored-local-files` with `cache-unverified`, and the plan stays complete
  (CD-9).
- **Caps (B-3, CD-6).** Per worktree, 512 cache entries (every file and
  directory the stage would remove) and 256 MiB, the `lstat` sizes of its
  regular files summed at plan time; per invocation, 4,096 entries, 1 GiB and
  16 enumerations. `limits` reports them as `cache_entries`, `cache_bytes`,
  `cache_entries_total`, `cache_bytes_total` and `cache_rows`. The enumeration
  children count in `probes`, and each entry a cache stage removes counts in
  `operations` beside the removal children (CD-12; `BA:1321-1322`,
  `BA:1336-1337`). The 50 s fit still holds with the 16 enumerations (design
  D4).
- **The ladder reads blocking paths (B-5).** The `ignored-local-files` rung
  keeps its name and its place and applies to a row holding an ignored path
  that is not proven a listed cache; a row whose every ignored path is a listed
  cache passes it, and the rungs below classify it, so a merged one is
  `merged-removable`. No ladder class, gate reason, stage value, reason value,
  refusal code or note code is added (L-4).
- **The plan records identities (B-4).** Each worktree row and each `selected`
  entry carries a `cache_disposal` object: the `disposable` and `blocking`
  counts, `null` and never 0 when not established (B-9); a `reason`; `entries`
  and `bytes`; the listed cache paths; and the device and inode of every
  directory the stage will open, each ancestor up to the worktree root and each
  cache directory. A selected target's listed caches and those identities enter
  the canonical text of `plan_digest`; a plan that lists none keeps change 1's
  digest (CD-14).
- **The cache stage (B-6, B-8).** In the removal sequence, after the target's
  revalidation and before its removal child is spawned, inside the same
  deadline: a whole-list preflight opens every directory of every listed path
  descriptor-relatively with `O_NOFOLLOW`, checks each against its planned
  device and inode, and re-lists each cache directory against the allowlist,
  all before the first unlink; then files are unlinked and emptied directories
  removed one entry at a time, never by a recursive deletion, and a directory
  that is no longer empty is never removed. The stage starts only while more
  than the 5 s removal floor remains, and each of its filesystem calls gets
  `min(5 s, work remaining less the removal floor)` on change 1's daemon
  threads (CD-10); once its first entry is removed it runs to its end, a signal
  only being recorded (CD-11).
- **Failure and recovery (B-6).** A preflight difference deletes nothing. A
  failure after the first removal leaves the earlier removals as permanent
  partial cache completion, rescans the listed paths, and reports each one
  removed or remaining, with the retry: re-run `project clean <root>
  --all-safe`, whose fresh plan lists what remains (`BA:1332-1336`). Either
  way the target's removal child is not spawned: the target is `refused` with
  `state-changed`, its `cache_disposal` records `refused` with `cache-changed`
  or `partial` with `cache-partial` (CD-2), and the run stops there, as change
  1 stops at any target that is not a plain `removed` (CD-1; `BA:1640-1643`),
  with exit status 2.
- **Fail closed per platform (B-6, CD-3).** Where the running Python cannot
  provide `O_NOFOLLOW`, `O_DIRECTORY` and the descriptor-relative calls, no row
  gets a cache plan: it keeps `ignored-local-files` with the reason
  `cache-unsupported-platform`, no enumeration runs, and the batch behaves as
  change 1's.
- **Revalidating a cache target (CD-4).** Change 1's revalidation requires the
  combined status probe in the target to print no record (CAS/rs:75-76), which
  every cache target fails. For a target whose plan lists caches, the
  revalidation runs the enumeration's status child instead, which must print
  exactly the ignored records the plan listed and nothing else; any other
  outcome refuses the target with `state-changed`, still within five Git
  children.
- **What the person sees (B-9, B-7).** The preview lists a selected target's
  caches under it (paths, entries, bytes and the first path); an
  `ignored-local-files` exclusion adds its disposable and blocking counts, or
  `unknown` with the reason, and its first blocking path. The question is
  change 1's, unchanged (CD-15). Success adds one line naming the caches
  disposed; a stop at a cache stage adds one line before the stop block, saying
  that nothing was deleted, or which cache paths were removed and which remain,
  with the re-run command. The residual-window line also names a cache
  recreated after the cache stage, which Git's non-force removal deletes with
  the worktree (`BA:319-323`).
- **Versioned JSON.** Worktree rows, `selected` entries and apply-result
  targets gain `cache_disposal`, and `limits` gains five keys. No value is
  added to any existing enum, and `schema_version` stays 1 (CD-16; Open
  Questions).

## Rules This Change Keeps

- **Never force, never a broad deletion.** No `git clean`, no recursive
  deletion and no deleting command run by `project`: caches go one entry at a
  time, and a directory only once `project` has emptied it (`BA:1329-1330`,
  `BA:1632-1634`; PR #2's design rejected `git clean -fdX` because it also
  deletes unknown ignored files). Change 1's "It MUST never use a force
  removal, reset, or deletion of unmerged work" stays verbatim.
- **What is not proven disposable is preserved.** An ignored path is
  disposable only when this invocation's enumeration proves it a listed cache
  within the caps; an unproven path is blocking, and `null` is never 0.
- **Never follow a symlink or leave the worktree.** A symlink candidate or
  ancestor is blocking (`BA:1324-1325`); every descent is descriptor-relative
  with `O_NOFOLLOW` and an identity check; a hard-linked `.pyc` loses only its
  name inside the worktree, and every external target stays intact
  (`BA:1632-1634`).
- **Stop before the worktree removal when the cache stage fails**
  (`BA:1335-1336`), and stop the run at the first target that is not a plain
  `removed`, as change 1 does (CAS/pc:246-248; `BA:1640-1643`).
- **Removing a worktree leaves its branch.** Unchanged; paired retirement is
  `add-project-clean-branch-retirement` (#23).
- **Nothing beyond the confirmed plan.** The stage disposes of only the caches
  that the confirmed plan lists, in a target that plan selected; the main
  worktree and every row not selected are never touched.
- **Local evidence only.** No fetch and no network; remote evidence never
  proves anything disposable (`SY:129-130`).
- **A started removal is never interrupted.** Unchanged; a cache stage, once
  its first entry is removed, also runs to its end.

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
  collects (Open Questions).

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
    not proven a listed cache, and a row whose every ignored path is a listed
    cache passes it; a failed cache enumeration leaves the paths unproven and
    is never `inspection-error`. The fifteen names, the order and the ancestry
    test stay, with the four scenarios. Added scenario: cache-only ignored
    files pass the rung, and beside `local.env` they do not.
  - MODIFIED (`:55`; written on CAS/pc:230), one inserted clause only:
    `### Requirement: Clean can explicitly retire verified worktrees`.
    The one sequence gains "for a target whose plan lists caches, dispose of
    them as "Clean disposes of listed caches before a worktree removal"
    states;" between the revalidation and the spawn. Every other sentence and
    the fourteen scenarios stay as change 1 wrote them.
  - MODIFIED (change 1 ADDED; written on PR19/pc:767, draft PR #19's text):
    `### Requirement: Clean bounds its Git work and reports omitted work`.
    The cache stage's start under the removal floor and its call budget; the
    cache walk among the filesystem calls; the five cache caps in `limits`;
    the enumeration children in `probes` and in the fit; each removed cache
    entry in `operations`. The scenario "Ignored-file bound" names files that
    are not caches; the other four stay. Added scenario: the cache limits and
    counts.
  - ADDED:
    `### Requirement: Clean disposes of listed caches before a worktree removal`.
    The allowlist, candidate rows, the enumeration with its caps and reasons,
    the plan's `cache_disposal` with identities and counts, the digest, the
    cache stage's place, start and budget, the result's `cache_disposal`, the
    exit statuses through change 1's table, and the human lines.
  - Untouched (`:10`): `### Requirement: Clean reports local worktree state`.
    The plain report carries `cache_disposal` on its rows as every plan does,
    and its `selected` stays what `--all-safe` would select.
  - Untouched (`:39`):
    `### Requirement: Clean can explicitly push safe feature branches`.
    Push and delete-branch run no cache enumeration.
  - Untouched (`:70`): `### Requirement: Clean hands off work requiring review`.
  - Untouched (change 1 ADDED): `### Requirement: Clean resolves its target Git-first`.
  - Untouched (change 1 ADDED), extended for cache targets only by the ADDED
    requirement's digest text and preview lines (CD-14):
    `### Requirement: Clean previews and applies a batch of eligible worktree removals in one repository`.
  - Untouched (change 1 ADDED):
    `### Requirement: Clean records a reconcilable result for every removal target`.
    A cache stage's failure takes its `refused` stage, `state-changed` reason
    and reconciliation (CD-2).
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
    `partial`, refuse the target with `state-changed`. The ten scenarios stay.
    Added scenario: a cache target changes before revalidation.
  - ADDED:
    `### Requirement: Cache disposal never follows a symlink or leaves its worktree`.
    Symlink candidates, ancestors and entries blocking; descriptor-relative
    no-follow operations against planned identities; no recursive deletion; the
    whole-list preflight; the partial-phase record and retry; the per-platform
    fail-closed rule; the stage's guarantee and the residual window.
  - Untouched (`:9`): `### Requirement: Cleanup protects the process worktree`.
  - Untouched (`:38`): `### Requirement: Cleanup respects configured upstream mappings`.
  - Untouched (change 1 ADDED):
    `### Requirement: Cleanup states a narrow guarantee and its residual window`.
    Its guarantee holds at the revalidation before a cache target's stage, and
    its window, ignored files created after that revalidation, already covers a
    cache recreated after the stage; the ADDED requirement states both.
- `project-command`, `project-review-safety`, `speckit-extension-integration`
  and change 2's `project-overview`: untouched. The enumeration child is a Git
  child of `project clean` alone, carrying the evidence model's environment,
  protocol pins, status pins and directory rule (CAS/cmd:98-133) without
  changing that model's probe list; status and doctor gather no cache evidence.

## Impact

- **`project`**: after feature 004, the plan builder gains the candidate rule,
  the enumeration child (through the bounded runner, with a NUL parser for
  porcelain v2's ignored records) and the descriptor-relative walk; the plan,
  the digest and the envelope gain `cache_disposal`; the removal sequence gains
  the cache stage between the revalidation and the spawn; the targeted
  revalidation reads a cache target with the enumeration child; the human
  preview, success and stop output gain the cache lines. At `961c405` the
  attach points are the ignored probe and rung (`project:505-507`,
  `project:581-583`), the signature that compares `ignored_files` and
  `classification` (`project:642-645`) and the remove path (`project:707-722`,
  `project:736-743`); feature 004 replaces all of them, so this change's
  feature builds on feature 004's code. No new dependency: only `os` calls that
  Python 3.10 provides.
- **`README.md`**: the "Clean up Git worktrees" section gains the cache
  paragraph: what is disposed of and what blocks, the caps, the residual window,
  and the partial phase with its re-run.
- **`tests/test_project.py`**: a test named after each ADDED and MODIFIED
  scenario; fixtures write `.pyc` bytes directly and need no compiler run;
  `test_clean_preserves_ignored_files_in_an_otherwise_merged_worktree`
  (tests:949, whose ignored file is `local.env`) and change 1's cache-free
  scenarios keep passing; fault hooks for the preflight, the removals and the
  walk; a platform stub for `cache-unsupported-platform`. The command is
  `python3 -m unittest discover -s tests -v` on `ubuntu-latest` and
  `macos-latest` with Python 3.10 and 3.12, as CI runs.
- **Speckit handoff**: exactly one feature, numbered when `/speckit.specify`
  runs after ratification, 006 or later (L-7).

### Dependencies and Sequencing

- **Written on change 1 (L-1).** Every MODIFIED block but two is written on
  change 1's ratified text at `961c405`. "Clean bounds its Git work and reports
  omitted work", as the rulings direct, and "Cleanup revalidates destructive
  actions", whose last clause PR #19 also rewords (the protocol pins are carried
  by every Git child "except the push child"), are written on draft PR #19's
  text (`c462d87`, spec text equal to the `5ce23d7` the rulings name), and PR
  #19 is a dependency: if it merges, change 1's text equals both blocks' bases;
  if it closes unmerged, or changes either requirement again, the blocks are
  rewritten on the text of that day before this change is ratified.
  `validate --strict` passes while change 1 is unarchived; the archive is the
  gate (it fails "MODIFIED failed ... - not found" until change 1 is
  archived).
- **Archive order (L-5).** This change archives after change 1's archive,
  which follows feature 004's merge, and after PR #19 has landed or closed.
  `add-project-clean-branch-retirement` (#23) archives after this change and
  writes its MODIFIED blocks of "Clean can explicitly retire verified
  worktrees" and "Clean bounds its Git work and reports omitted work", which
  both changes modify, on this change's archived text.
  `add-project-overview-remote-merge-status` (#25) modifies none of this
  change's requirements and archives after change 2.
- **Implementation order.** This change's feature builds on feature 004
  (`004-project-clean-all-safe`): its removal sequence, runner, parsers, ladder
  function and envelope. It never alters feature 004's or feature 005's order
  and does not wait for feature 005, but the overview question under Open
  Questions is settled before its Speckit handoff (`tasks.md` 2.2). Whichever
  realization merges second merges `main` in; never rebase, since the
  organisation ruleset refuses force pushes.
- **Change 2.** This change adds no delta to `project-overview`. Its ladder
  change reaches the overview only through evidence the overview does not
  collect, which runs into APO/ov:381-386 (Open Questions).

## Out of Scope

- **Other cache kinds** (`.pytest_cache`, `.mypy_cache`, `.ruff_cache`,
  `node_modules`, virtual environments, build directories) (B-1; Open
  Questions).
- **Paired branch retirement** (#23) and **remote merge status** (#25), each
  its own change.
- **The overview and doctor beyond the shared ladder.** Doctor classifies no
  worktree (change 1's C3); `status` and `doctor` gather no cache evidence and
  their JSON gains nothing; the overview's collection is unchanged.
- **Disposal without removal.** No mode deletes caches and keeps the worktree;
  the stage runs only for a target about to be removed.
- **Configurable caps or allowlists** (change 1's OQ-8 holds) and the CI
  matrix.
- **Continuing after a failed target** (`BA:1640-1643`; CD-1).

## Decisions Taken by This Proposal

Each is a proposal decision, open to ratification. The lane's rulings applied,
each citing the packet or change text that left it open:

- **L-1, the base text.** Drafted on change 1 and change 2 at `961c405`, and
  "Clean bounds its Git work and reports omitted work" on PR #19 (Dependencies
  and Sequencing). This proposal reads the six requirements that lane
  openRepoProject-2 said PR #19 does not move as the six that the three
  extensions' ruled lists modify besides the bounds; "Cleanup revalidates
  destructive actions", which CD-4 adds, is not among them and PR #19 rewords
  its last clause, so its block is written on PR #19's text by the same
  logic. PR #19's head moved from the ruled `5ce23d7` to `c462d87`
  after the rulings; `git diff 5ce23d7 c462d87` touches only its `design.md`
  and `tasks.md`, so the spec text the block is written on is the ruled one.
- **L-2, citations** at `da33d92`; PR #16's added sentence is quoted as "PR #16
  at `841c7dc`" (Why).
- **L-3, capabilities.** The existing two only (PR #2's abandoned names not
  reused); a MODIFIED block carries its whole requirement and every scenario of
  its source text; the new contract is in two ADDED requirements whose names no
  other change uses.
- **L-4, sub-records.** Every new value lives in `cache_disposal`, whose
  `reason` and `stage` are its own enums. No value is added to the closed
  `stage` enum, the target reasons, the fifteen classes, the gate reasons, the
  refusal codes, the note codes or the overview's finding codes. The
  enum-closure disagreement (CAS/pc:1129-1131 against APO/ov:655-658) is under
  Open Questions.
- **L-5 to L-9.** The archive order above; issue #24 governs, and closing it
  ends this change; the feature is numbered at `/speckit.specify` time; the
  lane opens the draft PR and runs the alignment review and the council; no
  host-absolute path in any file here, and the bidi check runs on every edit.
- **B-1, the allowlist** (no cache defined in the packet; PR #2's `1789ad9`
  allowlist): applied as written, with CD-8; other kinds are an Open Question.
- **B-2, detection** (the combined probe's bounds, `BA:795-806`): applied, with
  CD-5 and CD-6.
- **B-3, the caps** (`BA:1336-1337` sets no number): the four as ruled, and CD-6
  adds the enumeration count; before Brett Heap under Open Questions.
- **B-4, identities and the digest** (`BA:1327`, "the planned device/inode",
  names no plan field): applied; the digest's placement is CD-14.
- **B-5, the ladder** (CAS/pc:107-111, the fifth rung): applied; doctor
  classifies no worktree, and the overview is under Open Questions.
- **B-6, preflight and partial phase** (`BA:1332-1337`; PR #2 thread
  3989548481): the whole-list preflight and the partial record applied, with
  three departures, CD-1 to CD-3.
- **B-7, the residual window** (`BA:319-323`): applied in the ADDED
  review-safety requirement and the residual-window line.
- **B-8, the stage order** (`BA:1318-1322`, "cache disposal before the worktree
  removal"): applied, with CD-10 and CD-11.
- **B-9, the counts** (APO proposal.md:804-809 hands this extension the zero
  `disposable` and `blocking` counts of `1789ad9`): applied; unknown is `null`
  in the plan, the report and the human `unknown`.

Departures from the rulings, each naming what it departs from:

- **CD-1, the run stops at a failed cache stage** (departs from B-6's "other
  targets continue"). Change 1's retire requirement says "Removal SHALL stop
  after the first target whose result is not a plain `removed`, with no
  continuation" (CAS/pc:246-248), and the packet prefers "stop-on-first-failure,
  consistent with current retirement" (`BA:1640-1643`). Continuing would need a
  second change to that requirement beyond the one clause B's brief allows, and
  would make a cache failure the one stop cause that does not stop. Later
  targets are `not-attempted` with `batch-stopped`; a re-run plans afresh.
- **CD-2, the target's result** (departs from B-6's `cache-changed` as the
  target's refusal and `not-attempted` with `cache-partial` as its removal's
  result). Those values would extend the closed reason lists of
  CAS/pc:896-908, and `not-attempted` carries a null reconciliation and matches
  no exit row (CAS/pc:906-908, the exit table), so they would need a MODIFIED
  "Clean records a reconcilable result for every removal target" that the
  rulings do not list, against L-4. Here the target is `refused` with
  `state-changed` (nothing was spawned; the plan no longer held), carries its
  reconciliation and exits 2 by the existing table, and `cache_disposal`
  carries `refused` with `cache-changed` or `partial` with `cache-partial`.
- **CD-3, the platform rule is per row** (departs from B-6's refusal of the
  whole apply as `cache-unsupported-platform`). A refusal code would extend the
  closed list of CAS/pc:1113-1119, against L-4, and refusing the whole apply
  would stop change 1's cache-free removals on that platform. Here no row gets
  a cache plan and each holding ignored records keeps `ignored-local-files`
  with `cache_disposal.reason` `cache-unsupported-platform`: nothing is
  deleted by `project`, which is the fail-closed outcome `BA:1328` asks for.
- **CD-4, one more MODIFIED block** (departs from B's list).
  `Cleanup revalidates destructive actions` requires "the combined status probe,
  which SHALL print no record" (CAS/rs:75-76), which every cache target fails,
  so by L-3 it is modified: for such a target the enumeration's child replaces
  that probe at revalidation and must print exactly the planned records, the
  cache stage's failures refuse with `state-changed`, and the revalidation the
  MUST names is the one before the stage. No other extension modifies it. Its
  block is written on PR #19's text (L-1 above).
- **CD-5, the enumeration's argument vector** (completes B-2). B-2 names
  `status --porcelain=v2 --ignored=matching -z`; this adds
  `--untracked-files=normal` and the status pins. Git 2.43 refuses
  `--ignored=matching` with `--untracked-files=no` ("Unsupported combination of
  ignored and untracked-files arguments", exit 128), and a user's
  `status.showUntrackedFiles=no` does the same, so without it the child fails
  for every such user, as change 1 found for its own probe (CAS
  proposal.md:51-53); every status child carries the two status pins
  (CAS/cmd:111-113).

Lane additions, with no packet or ruling text behind them:

- **CD-6, at most 16 enumerations per invocation** (`limits.cache_rows`). With
  one enumeration per candidate and up to 127 candidates, the plan of 128 rows
  and 16 targets needs 361 Git children, 54.15 s at the packet's 150 ms
  (`BA:729-735`), past the 50 s work deadline; with 16 it needs 250, 37.5 s,
  and the 16th removal still spawns before the floor (design D4). Candidates
  past the 16th keep `ignored-local-files` with `cache-cap` and drain on re-run,
  as the target deferral does.
- **CD-7, candidate rows.** Only a linked worktree whose combined probe read
  ignored records and nothing else, and which would otherwise be selectable, is
  enumerated, so the 16 enumerations are never spent on rows that a gate keeps
  anyway; in single mode that is P alone, since `not-requested` precedes the
  cap. Other rows' `cache_disposal` carries `not-candidate` with `null` counts.
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
  remains, and each call gets `min(5 s, work remaining less the floor)`, so the
  floor is always left for the spawn and no constant is added.
- **CD-11, signals in the stage.** Before its first removal a signal stops the
  target as change 1's slot check does; after it, the stage runs to its end and
  the slot is read before the spawn, so a signal leaves the target's caches
  either untouched or all removed, never half done.
- **CD-12, `operations` counts removed cache entries** (`BA:1321-1322` and
  `BA:1336-1337` put the mutations in the plan estimate): beside the removal
  children PR #19 places there, each unlink and directory removal counts once.
- **CD-13, the sub-records' shape.** Plan: `disposable`, `blocking`, `reason`,
  `entries`, `bytes`, `paths`, `directories`, `blocking_samples` (at most 8,
  `limits.ignored_samples`). Result: `stage`, `reason`, `paths` with a
  per-path `removed`, `entries`, `entries_removed`.
- **CD-14, the digest in the ADDED requirement** (B's brief places it there).
  Change 1 defines the digest's canonical text as the identity fields, the
  merge target and "the selected `[path, branch, head]` triples"
  (CAS/pc:629-632). The ADDED requirement extends a cache target's entry with
  its cache paths and identities and leaves every plan without a cache target
  at change 1's digest. Strictly that extends change 1's sentence for cache
  plans; the alternative, a MODIFIED batch requirement, would add a third
  requirement that #23 must also carry. Named here for the alignment review.
- **CD-15, the question is unchanged.** `Remove N worktrees, keeping N
  branches? [yes/N]` stays; the caches are listed in the plan printed above it,
  as PR #2's design held the remove confirmation sufficient. Changing it would
  modify the batch requirement and its scenario "Only yes confirms".
- **CD-16, `schema_version` stays 1.** No existing enum gains a value; the new
  objects and keys are additive. `merged-removable` keeps its meaning,
  removable by this tool's gates, and `ignored-local-files` its meaning, holding
  ignored local files not proven disposable (the title of
  `project-clean-review-safety`'s requirement); what grows is the proof. Before
  Brett Heap with L-4's question.
- **CD-17, the overview is not changed here.** See Open Questions.
- **CD-18, an explicit stage rather than letting Git delete.** Git's non-force
  removal deletes ignored files with the worktree (`BA:319-321`), so proving
  the caches at revalidation and leaving the deletion to Git would be simpler.
  The packet and B-8 fix a stage, and the stage is safer: Git sees an ignored
  `__pycache__/` as one record and deletes whatever it holds by then, while the
  stage re-lists each cache directory at its preflight and removes it only once
  it has emptied it, so a file placed in a cache directory before that
  directory's removal survives and stops the target.

## Corrections to the Packet

None to the packet itself. One to the PR #2 decision record's harvest row,
which the packet links (`OV:186`): "bb91a49's `O_NOFOLLOW`/`dir_fd` deletes
already match the packet's stated requirement" holds only in part, because
`bb91a49` records no planned device or inode and falls back to flag 0 where
`O_NOFOLLOW` is missing (`git show bb91a49 -- project`), where `BA:1326-1328`
asks for both a planned identity and a fail-closed refusal.

## Open Questions

Each is before Brett Heap with a recommendation; the deltas implement the
recommendation, and a different ruling edits them before ratification.

- **Enum closure and `schema_version` (L-4).** Change 1 says "Enums SHALL be
  closed within a schema version" (CAS/pc:1129-1131) and change 2 that "adding
  a field or an enum value is additive" (APO/ov:655-658). Recommendation: this
  change makes the question moot for `clean --json`, since it adds no value to
  any existing enum and puts its own values in the new `cache_disposal`
  sub-records; `schema_version` stays 1 (CD-16). If Brett Heap reads a
  widened `merged-removable` as a change of meaning, the deltas move
  `clean --json` to `schema_version: 2` instead.
- **Other cache kinds (B-1).** `.pytest_cache`, `.mypy_cache`, `.ruff_cache`,
  `node_modules` and virtual environments are larger, hold executables or
  installed state, and have no single safe shape. Recommendation: no; each
  would need its own allowlist shape, caps and evidence in its own change.
- **The caps (B-3, CD-6).** 512 entries and 256 MiB per worktree, 4,096 entries
  and 1 GiB per invocation, 16 enumerations. Recommendation: adopt them, and
  measure the enumeration and the stage before the handoff as change 1's OQ-4
  was (`tasks.md` 2.3); a measured cost that breaks the fit lowers them by that
  rule before the feature starts.
- **The overview's equality clause (CD-17).** Change 2 requires the overview's
  classification of every row to equal that of `project clean <root> --json`,
  and its ladder to spawn no probe of its own (APO/ov:375-386). After this
  change, `project clean` classifies a cache-only candidate `merged-removable`
  on evidence the overview does not collect, so the overview would read the
  same row `ignored-local-files`. That is the safe direction (its suggestion is
  the read-only form, which then shows the row selectable), but it breaks the
  equality as written. Recommendation: lane openRepoProject-4 amends
  `add-project-overview` in place, as PR #19 amends change 1, before feature
  005's specification is final, with one sentence excepting rows whose ignored
  paths only `project clean` proves to be listed caches; the alternative, the
  overview collecting the same evidence, costs its budget and is out of this
  change's scope.

## Questions Resolved by the Alignment Review

| Findings | Severity | Ruling | Section edited |
| --- | --- | --- | --- |

### Council Verdicts

| Concern | Severity | Verdict | Section changed |
| --- | --- | --- | --- |
