Lane: openRepoProject-2

# Proposal: add-project-clean-all-safe

Status: ratified by Brett Heap on 2026-10-09, in his words to lane
openRepoProject-2, "ratify, merge #11 and run the runbook". It lands by
squash-merge of PR #11, with the Speckit handoff `004-project-clean-all-safe`
to follow.
Revised after the alignment review and the council (resolved below and on
PR #11; the council's noted constraints are in `clarifications.md`); it adds
Decisions and Corrections sections because it adopts a non-normative packet,
and Open Questions for the one question still before Brett Heap.

Governing issue: opensoft/openRepoProject#9, claimed by lane openRepoProject-2
(comment 6069500401); refs #6, the record of the project maintenance design
packet. Input: that packet, under `ideation/brainstorm/`, merged design-only
by PR #7 as `da33d92`. The packet is non-normative brainstorm material
(`OV:16-19`); this proposal adopts, narrows or corrects it, and only the spec
deltas that follow will be normative.

This is change 1 of two. `add-project-overview` (`project overview` and its
`--attention` filter) is governed separately and depends on this change
(Dependencies and Sequencing).

Citations are `file:line` at `da33d92`. `BA`, `SY`, `OV` and `DI` are the
packet's `project-maintenance-` files `batch-cleanup.md`,
`synthesis-inspect-and-retire.md`, `overview.md` and `project-discovery.md`;
`HO` is `next-session-project-maintenance-fix-handoff.md`; `project:N` is the
executable at `da33d92` (Dependencies and Sequencing). The packet's tables
are cited here, not restated.

## Why

Finished work is retired one worktree at a time: `project clean <root>
--apply --action remove --worktree P` removes one named linked worktree per
run (`project-clean/spec.md:55-61`), each run with its own selection,
confirmation and full report. Several merged worktrees need as many runs.

Designing a batch on top of that action showed that the action itself is not
safe enough to repeat. At `da33d92`, whose `project` and tests are unchanged
since the packet's `a040790` baseline (`git diff a040790 da33d92 -- project
tests/` is empty), and still at `7a9134b`, whose `project` gained only
PR #8's `project new` code, all above `discover`:

- A worktree whose only change is an edit to a file flagged assume-unchanged
  is classified `merged-removable`, and `--apply --action remove` deletes it
  with exit 0, edit included. This was reproduced for this proposal on a
  scratch fixture with Git 2.43; the cause is `BA:139-142`.
- A worktree holding a submodule can be offered for removal, which Git then
  refuses with exit 128 (`BA:1263-1267`).
- Under `status.showUntrackedFiles=no` the ignored-file probe fails, so every
  clean, non-default worktree classifies `inspection-error` (`DI:1130-1134`)
  and none is removable; fixing that probe requires the removal command to
  override the setting too, or Git's own cleanliness check would miss
  untracked files (`BA:307-317`).
- Worktree paths are parsed by line, so a newline path is misread and a
  non-UTF-8 path ends the run with an uncaught exception (`BA:1223-1224`).
- One unreadable worktree path refuses the whole repository with exit 2
  (`project:339`, `:995-1000`); here it is one `inspection-error` row, so
  another named removal proceeds and the batch records it, naming a remedy.
- A deleted upstream classifies `unpublished`, exactly like one never
  configured (re-run for this proposal; R9).
- An absolute path is silently redirected by `discover` to a family holder or
  a manifest ancestor (`project:307-313`; `BA:862-869`).
- Each Git probe has a fixed 15 s timeout, the removal child has none, and
  the run has no deadline (`project:60-65`, `:157-162`).

The packet resolved these into one reviewed design (`BA`; review trail
`HO:190-353`), and issue #6 is done only when "a later OpenSpec proposal picks
the packet up as input". This change is that proposal for the batch. It goes
first because the overview's `--all-safe` suggestion exists only through the
batch's gates and refusal codes (`SY:287-306`). Its yield is bounded on
purpose: the batch removes only worktrees with no ignored files; caches such
as `__pycache__` keep a worktree out until the cache-disposal change (Out of
Scope).

## What Changes

- **Behaviour changes users will notice.** Plain `project clean` exits 1 when
  its report is incomplete, where today it exits 0 whenever it prints (R2);
  `clean` refuses below Git 2.36 with `git-too-old`, exit 2 (R6); and
  `--apply --action remove --worktree P` refuses a freshly created merged
  worktree whose branch has no commit of its own (`target-excluded`, reason
  `unstarted-branch`), where `a040790` removes it (M4), with the remedy "no
  commit was made on this branch here since it was created; review, then git
  worktree remove yourself". A merged worktree whose branch reflog keeps no
  decisive entry (the branch saw no activity for `gc.reflogExpire`, 90 days
  by default) is likewise refused in single mode (`target-excluded`, reason
  `reflog-unavailable`) as well as withheld from the batch, with the remedy
  "the branch's reflog is missing, expired or undecidable; review, then git
  worktree remove yourself". And where `a040790` refuses a merged worktree
  whose upstream was deleted as `unpublished`, `--worktree P` now removes it
  as `merged-removable` when its gates pass, its branch kept (Brett Heap's
  ruling of 2026-10-09; Decisions). The README's clean section states these
  five first.
- **`project clean <root> --all-safe` previews a batch.** It plans every
  eligible linked worktree of one resolved repository: `selected` and
  `excluded`, each exclusion with one reason in the fixed gate order
  (`BA:152-165`), both in canonical raw-byte path order, which is also the
  execution order (`BA:107-111`). A complete plan with nothing eligible prints
  "No eligible worktrees" and exits 0. The spelling is `project clean <root>
  --all-safe [--json] [--apply [--yes] [--expect-plan D]]` (`BA:65-85`);
  `--all-safe` cannot be combined with `--action`, `--branch` or `--worktree`,
  and `--expect-plan` requires `--all-safe --apply`, else `invalid-arguments`
  and exit 2, as is an `--expect-plan` value that is not 64 lowercase
  hexadecimal characters (`BA:79-80`, `BA:991`).
- **`--apply` removes only what its own fresh plan selected.** It always
  recomputes, prints and confirms its plan; the preview is advisory and never
  reused. `--yes` accepts the fresh plan, and the optional `--expect-plan
  <plan_digest>` refuses a plan whose digest differs with
  `plan-digest-mismatch`, before any prompt (`BA:345-379`). The order is
  `BA:350-354`'s: an incomplete plan is refused first (a preview or report
  exits 1, and `--apply` refuses with exit 2 before asking), then an
  `--expect-plan` mismatch (exit 2), and only then does a complete plan that
  selects nothing print "No eligible worktrees" and exit 0 without asking; a
  single-target removal whose P a gate excludes refuses `target-excluded`,
  exit 2, and is not an empty selection. Targets run in
  canonical order, and the batch stops after the first target that is not a
  plain `removed`. Every local branch remains, and the result says so.
- **What the person sees.** The preview lists the selected rows, then the
  excluded rows grouped by reason, each group with its next step; an
  `ignored-local-files` exclusion shows its bounded count and the first
  ignored path already probed (`ignored_samples`, `BA:804-806`). Apply asks
  one default-No question naming the count, such as `Remove 7 worktrees,
  keeping 7 branches? [yes/N]`; `yes` stays the only accepting answer and
  anything else is `cancelled` (`BA:354`, `BA:1009`; M2). It replaces `Type
  yes to run this plan:` (`project:153`) for `clean`'s removal apply only
  (`--all-safe` and `--action remove`); `confirm()` as `new`, `update` and
  `clean`'s `push` and `delete-branch` use it is unchanged. Success prints
  `Removed 7; branches kept: ...`; a stop, `Stopped at P (reason). Removed k
  of n. Not attempted: ... Next: <command>` (`BA:1276-1312`).
- **Eligibility is `merged-removable` plus gates**, in this order
  (`BA:152-160` as extended by V2 and V5, the council's AE-2 and PA-1):
  `main-worktree`, `unsupported-path-bytes`,
  `registration-mismatch` (two-way admin registration), `locked-worktree`, the
  baseline classification when not `merged-removable`, `not-requested`,
  `unstarted-branch`, `deferred-target-cap` (Bounded work),
  `contains-submodule` (any gitlink or admin `modules` entry) and
  `hidden-local-state` (any entry flagged assume-unchanged or skip-worktree),
  the last two read in the row's own worktree (`BA:113-150`, `BA:629-675`,
  `BA:554-583`). A merged worktree whose upstream was deleted is
  `merged-removable` and faces these gates like any other merged row, since
  local ancestry outranks `remote-gone` for worktree rows (Brett Heap's
  ruling of 2026-10-09; Decisions). Local ancestry is the only removal proof,
  and it proves that a branch adds nothing, not that its work began. Nor
  does a head equal to
  the merge-target SHA prove that the work never began, because a branch
  fast-forward merged into the target sits at the target's tip, so the gate
  reads the branch's reflog in every case. Its anchor is the last surviving
  entry whose old object is all zeros, as every entry that creates the
  branch has, whatever its message (`git fetch origin feat:f1`, `update-ref`
  and `push .` write no `branch:` message), or whose message begins
  `branch: Created from` or `branch: Reset to` (`worktree add -B`,
  `branch -f` and `checkout -B` write the second; R-15). An entry whose old
  object is all zeros is never a movement, and a movement is a later entry,
  or any entry when no anchor survives, whose old and new objects are
  non-zero and differ (a rename's are equal). A branch whose anchor survives
  with no movement after it, at the anchor's new object, is excluded as
  `unstarted-branch`, so a freshly created and published lane worktree,
  whose push adds no reflog entry, is never swept, nor one reset to the
  target's tip by `worktree add -B` or created there by
  `git fetch origin feat:f1`; a branch with a movement, at the target's tip
  or not, is merged and stays eligible. The reflog is a bounded
  filesystem read of `logs/refs/heads/<branch>` in the common directory, at
  most 64 KiB, counted in the filesystem budget and never a Git child, so the
  fit test is unchanged. One outcome rule decides the read (M3; R-12): a
  missing, empty (0 byte) or bound-reaching reflog, one whose surviving
  entries cannot decide, and one whose last entry's new object is not the
  head fail closed as `reflog-unavailable`, at the same gate position; any
  other error on the read is the row's `inspection-error`; and a read not
  finished within the filesystem budget leaves the row unprobed
  (`inspection-incomplete`). The gate applies in single mode too (M4).
- **Single-target `remove` becomes a one-item batch.** Flags unchanged,
  `--apply --json` now accepted (OQ-10). It builds the same plan (`mode:
  "single"`), lists every other eligible row as `not-requested`, and shares
  the seam, refusal codes, stages and exit codes of a batch whose only
  target is P, adding `worktree-not-found` and `target-excluded`
  (`BA:413-423`). Its completeness is the repository-wide evidence plus P's
  own row: another row's `inspection-error`, `inspect-cap` or unprobed state
  is a non-blocking omission recorded in the plan, while P's own
  revalidation stays fully strict (Decisions). P is probed first and is
  exempt from the 128-row cap, which counts registered rows, `present: false`
  included; the 16-target limit counts P alone, as `not-requested` precedes
  the counted gates. Every plan-blocking refusal left, in either mode, names
  a manual remedy: `git worktree prune`, `git worktree repair`, or removing
  that row by hand. `push` and `delete-branch` change in argument resolution
  (`BA:424-425`) and two refusals (MODIFIED `:39`, `:49`); with either,
  `--apply --json` stays refused with `invalid-arguments`, exit 2.
- **One mutation seam, `retire_worktree(plan, target)`.** Revalidate; spawn the
  non-force `git -c status.showUntrackedFiles=normal -c
  core.untrackedCache=false -c core.fsmonitor=false -c protocol.allow=never -c
  protocol.file.allow=never -c protocol.ssh.allow=never -c
  protocol.git.allow=never -c protocol.http.allow=never -c
  protocol.https.allow=never -c protocol.ext.allow=never -C <command
  directory> worktree remove <path>` in its own process group, only while the
  removal floor remains; wait; reconcile by rescan (`BA:381-411`).
  Once spawned, the child is never signalled: SIGINT, SIGTERM, SIGHUP and the
  work deadline wait for it to exit, and only a separate 300 s hard ceiling, for
  a hung mount, kills its group. For that child, or one whose exit could not be
  observed, the rescan decides: the target is `removed` when its registry entry
  and path are gone, and otherwise `unknown` with the note `partially-removed`
  and the recovery text "inspect, then `git worktree remove --force <path>` by
  hand"; the reason `removal-ceiling` names the ceiling cause, and the run exits
  1 (Decisions).
- **Targeted revalidation under a narrow guarantee.** Each target is
  revalidated with at most five Git children, a manifest re-read and a
  `modules` check, never the full report (`BA:677-719`), against recorded
  repository, worktree and merge-target identity objects (`BA:203-235`).
  Concurrent writers are outside the contract and no lock is claimed; the
  guarantee is `BA:261-268`, its outcomes are the changes-after-confirmation
  table (`BA:282-303`) and the branch race (`BA:327-341`), and the
  confirmation and result each state the residual window in one line
  (`BA:305-325`).
- **Every target ends reconcilable.** The closed stage enum and its reasons
  (stage table `BA:485-494`, plus `removal-ceiling` and the target note
  `partially-removed`), a reconciliation record on every `removed`, `refused`,
  `failed` or `unknown` target, and `removed` only on rescan evidence, never on
  the exit status alone (`BA:496-526`). The table's `interrupted` and
  `deadline-exceeded` apply to targets not yet started. A removal child that
  exits nonzero on its own is `failed` with Git's status, `git-refused` for 128
  and `git-failed` otherwise, whether or not a signal reached `project`, and one
  that exits 0 is `removed` only on rescan evidence. Only for a child that
  `project` killed at the ceiling, or whose exit could not be observed, does the
  rescan decide between `removed` and `unknown` with the note
  `partially-removed`; `removal-ceiling` names the ceiling cause. The run exits
  per the 130 row, 130, 143 or 129, whenever a signal arrived (M1). Exit codes
  follow `BA:528-550`, Git's status passing through; SIGINT, deadline expiry and
  exceptions follow `BA:460-483` but for that deferral; SIGTERM and SIGHUP exit
  143 and 129, with the SIGINT treatment in the apply phase (Decisions, OQ-16).
  A registered row with only tracked-file deletions stays `dirty`, the report
  showing the partial-removal note and recovery text beside, never instead of,
  the dirty advice.
- **Bounded work.** One monotonic 60 s deadline with a 10 s reconciliation
  reserve, so a 50 s work deadline; `min(5 s, work_remaining)` per Git child and
  per filesystem call, a 5 s removal floor, a 2 s TERM-to-KILL grace for probe
  children and serial probing (`BA:427-458`). The deadline bounds inspection and
  gates only the start of a removal: a removal child still running at the
  deadline is waited for, so the run overruns, bounded only by the 300 s hard
  ceiling, and its reconciliation reserve counts from its exit. A run with no
  removal in flight therefore ends within 64 s of its start, not counting the
  time blocked at the confirmation question (50 s of work, the
  10 s reserve, and up to 4 s to stop a probe child: SIGTERM, the 2 s grace,
  SIGKILL, then a reap wait of up to 2 s), the figure `add-project-overview`
  states, not "within about 60 s" (`BA:456-458`; M5); a removal in flight adds
  up to 300 s. `push` and `delete-branch` children, run by `execute`
  (`project:157-162`), stay unbounded as today. Caps of 128 worktree rows (256
  for the plain report, OQ-29) and 16 targets, and ignored-file bounds of 64,
  4,096 and 8 (`BA:721-814`). A cap or deadline hit is an incomplete plan
  (`inspect-cap`, `inspection-incomplete`, `deadline-exceeded`, with `omitted`)
  that blocks apply (preview exit 1). When more than 16 rows pass every gate
  before the two index gates, the first 16 in canonical order go on to those
  gates and the rest are excluded `deferred-target-cap` with the next command;
  the plan stays complete, apply is allowed, and re-running drains the backlog
  16 at a time, the fresh plan and revalidation unchanged; when every one of
  those 16 is then excluded as `contains-submodule`, no re-run reaches a
  deferred row, and the human report says why. The `target-cap`
  refusal is retired; the code survives only as `add-project-overview`'s
  limiting gate reason (Decisions). Plans and results report `probes` and
  `operations` as `{estimated, performed}` (`BA:816-830`). The caps were
  measured by governance task 2.1 and stand (Decisions, OQ-4).
- **Git-first resolution in every `clean` mode.** The read-only report,
  `--json`, `--all-safe` and every `--apply --action` resolve their argument
  by the table at `BA:856-860`: an absolute path must be exactly a main
  worktree root, else `target-not-repository-root`; a relative path or no
  argument resolves to the repository Git finds there; only a bare name keeps
  `discover`, its Git child counted and bounded. The report's `root` names
  the command directory, and the manifest is read at `repository.root`. Bare
  repositories are refused in every mode (Decisions, OQ-15; R10); a gitfile
  main checkout is supported, and a submodule checkout refused (R11).
- **One evidence model for `clean`, `status`, `doctor` and `update`.**
  `repo_state` and `cleanup_report` move onto the shared probe set: one `git
  --version`, four repository-wide children memoized per `common_dir`
  (identity, `worktree list --porcelain -z`, one `for-each-ref` in the shared
  format, the merged set), and one combined bounded status probe per row
  (`BA:585-652`) under `-c core.untrackedCache=false -c core.fsmonitor=false`
  (pins that also override `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`, which
  the scrub leaves), every Git child also under `-c protocol.allow=never` and
  the six per-protocol pins (`protocol.file`, `ssh`, `git`, `http`, `https` and
  `ext`, each `.allow=never`), with `GIT_ALLOW_PROTOCOL` in the scrub, so that a
  lazy fetch in a partial (promisor) clone fails locally and its row is
  `inspection-error` (R-23, R-25), all parsed NUL-delimited, with the scrubbed
  environment of `BA:243-253`, through a new bounded runner (Impact). A probe
  `project` stops at its record bound is complete, never `probe-failed`; after
  SIGKILL the reap waits at most the 2 s grace, then abandons the child and
  records `probe-timeout`; every exit path terminates the probe groups it
  started, and a running removal child is waited for, per V1 ("A started removal
  is never interrupted"); stderr is drained and capped. A Git child gets `min(5
  s, work_remaining)` under `clean`'s deadline and 15 s in `status`, `doctor`
  and `update`, which have none (Decisions). The ladder keeps its names, and its
  order but for one test: a row whose upstream was deleted is tested for local
  ancestry before `remote-gone`, so a merged one is `merged-removable` (or
  `merged-current`) and only an unmerged one is `remote-gone` (Brett Heap's
  ruling of 2026-10-09; Decisions). Its text changes for that and for the
  partial-removal note (MODIFIED `:25`), and it becomes a pure function over
  evidence (OQ-28). Git 2.36 is required as R6 scopes it. The visible
  consequences are the baseline behavior changes of `BA:1200-1274`, less
  `BA:1255-1256`, with `BA:1238-1240` and `BA:1268-1274` narrowed (Decisions)
  and `BA:1241-1245` (R6), plus R1, R2, R10, R11, `unstarted-branch` and
  `reflog-unavailable` in single mode (M4), a merged worktree whose upstream was
  deleted reading `merged-removable` where `a040790` reads it `unpublished`
  (that ruling), and the manifest cap; the deltas carry each, and the
  `ignored_samples` objects are a packet departure (Decisions). The manifest
  read that resolves a merge target is capped at 1 MiB, a larger manifest being
  `manifest-invalid`, so every reader resolves the same target; at `a040790`
  `clean` reads a manifest of any size, so a larger one refusing `clean` with
  `manifest-invalid`, exit 2, is a baseline behavior change beside R1 and R10.
- **Every `clean --json` prints one versioned envelope.** `schema_version: 1`
  with the plan fields of `BA:947-976`, `mode` being `report`, `single` or
  `all-safe` (OQ-29); refusals as `{code, message, path?, path_valid_utf8?,
  reason?}` with the
  codes of `BA:987-1015`; the extended error object when no plan can be built
  (`BA:978-985`). `--apply --json` (removal only, OQ-10) prints exactly one
  stdout document: the plan envelope or the extended error object when the
  run stops before the apply phase, otherwise the apply result record
  (`BA:1017-1042`); the human plan, prompt and progress go to stderr. Only
  a parser usage error, and SIGINT, SIGTERM or SIGHUP before the apply phase,
  or end of input at the question (`Cancelled.` on stderr, exit 130, 143 or
  129), print no JSON document.
- **Every path is exact or excluded.** JSON carries a valid UTF-8 path
  exactly with `path_valid_utf8: true`; a non-UTF-8 path is escaped, excluded
  as `unsupported-path-bytes` and never a removal operand. Every path value
  carries its validity flag beside it, so an escaped `\xHH` never reads as a
  valid path holding those four characters: `path_valid_utf8` beside each
  `path`, each `ignored_samples` entry an object `{path, path_valid_utf8}`, and
  `root_valid_utf8` and `common_dir_valid_utf8` in `repository`. JSON escapes,
  and human output prints in the `$'...'` form of `BA:913-939`, every code
  point of Unicode general category Cc, Cf, Zl or Zp, the packet's list of
  control, bidirectional and format characters kept as examples; human output
  does the same for undecodable bytes. A `repository.root` or `common_dir`
  that is not valid UTF-8 refuses with `unsupported-path-bytes`, exit 2,
  before any plan or digest (`BA:368-370`).

## Rules This Change Keeps

- **Never force.** No forced worktree removal, force push, `branch -D`,
  reset, stash or fetch; canonical "MUST never use a force removal, reset, or
  deletion of unmerged work" (`project-clean/spec.md:61`) stays verbatim.
- **Removing a worktree leaves its branch.** Branch deletion stays the
  separate explicit `delete-branch` action (`project-clean/spec.md:59-60`),
  which remains the retry path after a batch (`BA:1281-1293`).
- **Nothing is removed unconfirmed.** The person confirms the exact listed
  set, or passes `--yes` for that fresh plan; noninteractive stdin without
  `--yes` refuses with `confirmation-required`.
- **Local evidence only.** No fetch, no remote or GitHub query, staleness
  stated (`project-clean/spec.md:12-16`); remote evidence never proves a
  removal (`SY:219-226`).
- **What is not proven disposable is preserved.** Uncertainty fails closed:
  an unknown value is `null`, never `false` or `0`, and keeps a row out.
- **The current worktree is never removed**
  (`project-clean-review-safety/spec.md:9-13`). The main worktree is never
  removed either, through the new `main-worktree` gate this change adds.
- **Revalidate before every destructive action**
  (`project-clean-review-safety/spec.md:49-53`), and stop at the first
  failure: no continuation, rollback or automatic retry.
- **A started removal is never interrupted.** Signals and the deadline wait
  for the removal child; only the 300 s hard ceiling kills it.
- **Git's own check runs on pinned configuration.** `core.untrackedCache`
  and `core.fsmonitor` off, untracked files listed (What Changes, seam).
- **One repository per invocation.** Never siblings, family members, mounted
  legs, pinned member copies or independent clones (`BA:103-105`).
- **Never prune, repair, lock or unlock.** `project` never runs
  `git worktree prune` or `repair`, and it leaves an orphaned directory for
  the person to inspect (`BA:192-193`, `BA:1300-1303`, `BA:1537-1538`); a
  refusal may name them as the person's own remedy.

## What This Repository Does Not Own

- **Git's own refusals**: the pinned, non-force `git worktree remove` is the
  last line of defense; this change adds a gate in front of it, never a bypass.
- **Feature worktrees and park/resume**: the Speckit git extension and
  setup-openspeckit's overlay. `clean` never replaces `park`/`resume`
  (README:110).
- **Family membership, legs and pins**: openRepoShape and the family
  tooling; the batch never traverses them.
- **The installed `project` artifact**: workBenches pins it on its owner's
  act; this change does not move the pin.

## Capabilities

### New Capabilities

None. The overview's capability belongs to `add-project-overview`.

### Modified Capabilities

Headers are quoted verbatim, one per line; ADDED headers are proposed text.

- `project-clean` (all five canonical requirements accounted for):
  - MODIFIED (`:10`): `### Requirement: Clean reports local worktree state`.
    The report comes from the shared evidence model (NUL parsing, the combined
    bounded probe, the 5 s and 60 s budgets, Git 2.36 and `clean`'s refusal
    below it, R6); an unreadable path is one `inspection-error` row with
    `present: null` and an `os-error`, not a whole-command exit 2;
    `ignored_files` counts ignored records observed, at least, beside
    `ignored_files_truncated`; `root` names the command directory. The
    staleness sentence (`:16`) and the audit scenario stay.
  - MODIFIED (`:25`):
    `### Requirement: Clean classifies preservation and cleanup actions`.
    `:27-28` names 7 classes and the ladder has 15 (`project:418-468`); the
    text names all 15 in ladder order, an unmerged deleted upstream becomes
    `remote-gone`, and unreadable, mismatched and probe-failed rows are
    `inspection-error` directly (R1). By Brett Heap's ruling of 2026-10-09 a
    row whose upstream was deleted is tested for local ancestry before
    `remote-gone`: merged, it is `merged-removable` (or `merged-current`)
    with that class's recommendation, and only an unmerged one is
    `remote-gone` (Decisions); a `dirty` row whose only working changes are
    deleted tracked files carries the partial-removal note beside its advice.
    Names are unchanged, and the order changes only by that ancestry test
    (OQ-28). The scenario (`:32-37`) stays; the added scenario "A merged
    worktree whose upstream was deleted" has `--all-safe` select it and
    `--worktree` remove it, and an unmerged one stay `remote-gone`.
  - MODIFIED (`:39`):
    `### Requirement: Clean can explicitly push safe feature branches`.
    Two additions; the rest stays. Push refuses a branch on its deleted
    upstream itself, whatever its row's class (`remote-gone` when unmerged;
    `merged-removable` or `merged-current` when merged, under Brett Heap's
    ruling), because it must be reviewed before it is republished
    (`project:545-555` would push to it), with refusal reason `remote-gone`,
    exit 2, and refuses with `inspection-incomplete`, `inspect-cap` or
    `deadline-exceeded`, exit 2, when its re-inspection is incomplete. Added
    scenario: WHEN push is requested for a branch whose upstream was deleted,
    THEN it refuses with `remote-gone` and runs no push.
  - MODIFIED (`:55`):
    `### Requirement: Clean can explicitly retire verified worktrees`.
    "remove one named linked worktree" (`:57`) becomes one named worktree or
    the `--all-safe` set, through `retire_worktree`, the gates
    (`unstarted-branch` included) and the pinned removal command, stopping at
    the first failure; the removal child is never signalled before the 300 s
    ceiling; a named P's completeness is the repository-wide evidence plus its
    own row. `:59-61` (branch deletion separate; never force) and the
    scenario (`:63-68`) stay verbatim. Added scenarios: WHEN `--all-safe
    --apply` removes every selected worktree, THEN every local branch remains
    and the result says so (`BA:1281`, `BA:1353-1356`); `worktree add -b x`
    then `push -u` with no commit, its reflog holding only the creation entry,
    is excluded `unstarted-branch`, and `--worktree` on it refuses
    `target-excluded` (M4); a branch fast-forward merged into the target, at
    the target's tip with a commit in its reflog, stays eligible; a branch
    reset to the target's tip by `worktree add -B` stays `unstarted-branch`,
    as does one created there by `git fetch origin feat:f1` and never
    committed to here (R-15); a missing, empty or expired reflog is
    `reflog-unavailable`, and
    `--worktree` on such a worktree refuses `target-excluded`; with the
    untracked cache on, `core.checkStat=minimal` and an index-writing status
    run, a file created after revalidation is refused by Git with 128 and
    survives; `--worktree P` removes P beside another row's
    `inspection-error`, among 17 eligible rows, and among more than 128 rows;
    a removal past the ceiling is decided by the rescan, `removed` when the
    registry entry and path are gone and otherwise `unknown` with
    `partially-removed`, the reason `removal-ceiling` either way; after
    `project` and its child are killed with SIGKILL mid-deletion, the report
    shows the partial-removal note beside the `dirty` advice.
  - MODIFIED (`:70`): `### Requirement: Clean hands off work requiring review`.
    `:75-76` requires "explicit confirmation and action targets", and
    `--all-safe --apply --yes` names no single target, so the text defines
    `--all-safe` as an explicit action target, the set the fresh plan
    selects. The pull-request hand-off and its scenario stay.
  - ADDED: `### Requirement: Clean resolves its target Git-first`. The
    resolution table for every mode, `target-not-repository-root`, bare
    repositories refused (R10), and the merge target (`BA:167-184`): the
    first local branch of the manifest `tracking_branch` less any `origin/`
    prefix (`DI:576`, `project:383`; `BA:169-177` omits this strip), the
    `origin/HEAD` `%(symref)` less `refs/remotes/origin/`, `main`, `master`,
    as `{name, source, sha}`; a manifest conflicting with `origin/HEAD` wins
    with a `merge-target-conflict` note; `no-merge-target` and
    `manifest-invalid` (a manifest over the evidence model's 1 MiB cap
    included) refuse with exit 2 before any mutation. Scenario:
    `tracking_branch: origin/develop` resolves to `refs/heads/develop`,
    never falling back silently; a manifest over 1 MiB refuses
    `manifest-invalid`, exit 2, before any probe of a worktree row. It
    carries R11, with scenarios for a `--separate-git-dir` main checkout that
    resolves and a submodule checkout refused `target-not-repository-root`.
  - ADDED:
    `### Requirement: Clean previews and applies a batch of eligible worktree removals in one repository`.
    `--all-safe`, the gate order, the fresh plan, `plan_digest` and
    `--expect-plan`, single-target removal as a one-item batch, and what the
    person sees: the preview layout, the default-No prompt, the success line.
  - ADDED:
    `### Requirement: Clean bounds its Git work and reports omitted work`.
    The deadline, budgets, caps, `omitted`, `probes`, `operations`, `limits`
    and `budget`, incompleteness blocking apply, the 16-per-run
    `deferred-target-cap` deferral (`target-cap` refusal retired), and the
    deadline gating only a removal's start, a removal past it overrunning up
    to the 300 s ceiling. Scenario: twenty rows pass every gate before
    `deferred-target-cap`; sixteen are selected, four deferred, and a second
    run removes those four.
  - ADDED:
    `### Requirement: Clean records a reconcilable result for every removal target`.
    Stages, reasons (`removal-ceiling` added to `removed` and `unknown`;
    the target note `partially-removed`), the
    reconciliation record, exit codes, interruption deferred while a removal
    runs, and recovery. Scenario: the stop block names the stopping target
    and reason, the count removed, the targets not attempted, the next command.
  - ADDED:
    `### Requirement: Clean reports every path exactly or excludes it`.
    NUL parsing, `path_valid_utf8`, and the JSON and human escaping rules.
  - ADDED: `### Requirement: Clean plans and refusals are versioned JSON`.
    The `schema_version: 1` envelope for every `clean --json`, refusal
    objects, the extended error object, and the apply result record.
- `project-clean-review-safety` (all four accounted for):
  - MODIFIED (`:21`):
    `### Requirement: Cleanup preserves all local work not proven disposable`.
    Adds the main worktree, locked, `contains-submodule`, `hidden-local-state`
    (sparse checkouts included), `registration-mismatch`,
    `unsupported-path-bytes`, `unstarted-branch`, `reflog-unavailable` and
    unreadable worktrees to the preserved states. Both scenarios (`:27-36`)
    stay.
  - MODIFIED (`:49`): `### Requirement: Cleanup revalidates destructive actions`.
    Removal revalidates by the targeted check against the recorded identity
    objects, refusing with `identity-changed`, `branch-changed`,
    `state-changed`, `contains-submodule` or `hidden-local-state`; push and
    `delete-branch` keep the full re-inspection (`project:508-518`) and refuse
    with `inspection-incomplete`, `inspect-cap` or `deadline-exceeded`, exit
    2, when it is incomplete. The MUST is scoped to the revalidation
    immediately before each spawn; changes after it are the residual window
    the ADDED guarantee states, and Git's own non-force check is the last
    defense only on the pinned configuration (`status.showUntrackedFiles`,
    `core.untrackedCache`, `core.fsmonitor`; the protocol pins on every Git
    child are no part of it). A value null in the plan and null
    at revalidation, as a deleted upstream's `upstream_oid`, `ahead` and
    `behind` are, is no difference, while a value that cannot be re-read is
    (Brett Heap's ruling of 2026-10-09; Decisions). The scenario (`:55-58`)
    stays; a worktree that becomes dirty after revalidation is refused by Git
    (`failed`, `git-refused`, exit 128) and is still preserved (`BA:298`).
  - Untouched (`:9`, `current` keeps its baseline meaning):
    `### Requirement: Cleanup protects the process worktree`.
  - Untouched (`:38`, a push still uses the configured mapping):
    `### Requirement: Cleanup respects configured upstream mappings`.
  - ADDED:
    `### Requirement: Cleanup states a narrow guarantee and its residual window`.
    Concurrent writers outside the contract, no lock, the guarantee, the
    residual-window line, and the branch race.
- `project-command` (all ten at `7a9134b` accounted for; line numbers are at
  `da33d92`; at `7a9134b` `Inspect and diagnose`, `Explicit maintenance` and
  `Distribution and compatibility` sit 22 lines lower, their text unchanged):
  - MODIFIED (`:22`): `### Requirement: Inspect and diagnose`. Minimal text
    per R6: doctor's `error` check row for old or unusable Git, status's
    `inspection-error` marker on a root or leg dict in a field matching
    worktree rows (R7), and `present: false` for a directory with no `.git`.
    Doctor shows as an `error` check row, never `ok` (`:24-25`), a null that
    means "not established" (`present`, a `dirty` a failed probe left null,
    any `inspection-error` row), never one that means "none" (`upstream`,
    `ahead`, `behind` without an upstream, `merged_into_target` when detached;
    `BA:897-900`, `DI:781-785`), so a fresh project with no remote passes.
    "Missing leg" and the rest stay. Added scenario: WHEN doctor runs with no
    `git` on PATH, THEN it reports `git-unavailable` as an error row, exit 1.
  - MODIFIED (`:31`): `### Requirement: Explicit maintenance`. One sentence:
    `update --apply` for a project-modifying component (`shape`, `bench`)
    refuses whenever the root's or any child's `dirty` is not exactly
    `false`, as push already does (`project:541`; `project:863` and `:869`
    test truthiness, which `null` passes). Added scenario: WHEN a leg's
    status probe times out at 15 s, THEN `update --apply` refuses and the
    owner tool is never invoked.
  - ADDED:
    `### Requirement: Repository inspection requires Git 2.36 and shares one evidence model`.
    Its readers are named generically, "every subcommand that inspects a Git
    repository" (today `clean`, and `status`, `doctor` and `update` through
    `snapshot`, `project:681`, `:699`, `:789`, `:846`). It carries the
    evidence model: the version check (`BA:593`), R6's timing not stated as a
    rule for every reader; the probe directory rule (`BA:554-583`); the scrub
    with `GIT_OPTIONAL_LOCKS=0` (`BA:243-253`); NUL parsing; the combined
    probe, its pins and bounds (`BA:629-652`, `BA:793-814`), among them the `-c
    protocol.allow=never` pin and the six per-protocol pins on every Git child,
    with `GIT_ALLOW_PROTOCOL` in the scrub, against lazy fetches (R-23, R-25);
    the 1 MiB cap on the manifest read that resolves a merge target, a larger
    manifest being `manifest-invalid`; the runner's outcomes (What Changes,
    evidence model); its every-exit-path termination rule, stated in its own
    words: the probe groups it started are killed in a `finally` on every exit
    path, and a running removal child is waited for, per V1, never signalled
    before the 300 s ceiling (M7); and `min(5 s, work_remaining)` per Git child
    under a deadline, 15 s otherwise. `status`, `doctor` and `update` get no
    deadline or row cap; an unreadable or timed-out row shows as
    `inspection-error`. Non-Git children (docker, doctor validators;
    `project:715`, `:817`) keep 15 s.
  - Untouched (`:9`; `:7` at `7a9134b`, with the MODIFIED text PR #13
    archived from `prefer-triad-in-project-new`):
    `### Requirement: Delegate project creation`.
  - Untouched (`:40`): `### Requirement: Distribution and compatibility`.
  - Untouched, ADDED by PR #13's archive (`:70`, `:140`, `:200`, `:251`,
    `:310` and `:367` at `7a9134b`):
    - `### Requirement: Creation question is asked only of a person choosing at the terminal`
    - `### Requirement: Creation question offers the Triad first`
    - `### Requirement: Known Triad obstacles are named before the question and refused on a Triad answer`
    - `### Requirement: A Triad answer asks for the organization and the visibility`
    - `### Requirement: Creation advisory follows a single repository created without the question`
    - `### Requirement: Creation offer precedes the workflow follow-up`
- `project-review-safety` and `speckit-extension-integration`: untouched.
  Every `clean` resolve refusal (the extended error object, `manifest-invalid`
  included) and every refusal under `--apply` exits 2 with structured JSON,
  consistent with `project-review-safety/spec.md:80-82` for YAML decoding
  errors. A read-only preview or report whose plan carries `inspect-cap`,
  `inspection-incomplete` or `deadline-exceeded` exits 1, a complete one 0,
  deferred rows included (`BA:547-549`, `BA:1011-1015`). Its "Updates
  preserve estate and owner safeguards" (`:51-55`) is preserved, not
  modified, by MODIFIED `Explicit maintenance`.

## Impact

- **`project`**: `clean()` gains `--all-safe` and `--expect-plan`, the plan
  builder, `retire_worktree`, targeted revalidation, reconciliation, apply-
  phase signal handling and the JSON envelope. `repo_state`, `cleanup_report`,
  `default_branch` and `discover`'s Git child move onto the shared bounded
  probes, under one deadline in `clean`. Git children run through a new
  bounded runner, not the baseline `probe()` (a departure from
  `BA:1212-1213`): each is a `Popen` in its own process group (C4), with the
  environment scrubbed of `BA:243-253`'s variables, and its stdout is read as
  bytes and streamed, so a probe can stop at its record bound. `probe()`
  stays for non-Git children. The runner's shape (clarifications N2) lets
  `add-project-overview` drive four children without forking it.
  The ladder becomes a pure function; `status`, `doctor` and `update` gain the
  Git version check (R6). No new flag outside `clean`, no network, no new
  dependency.
- **`README.md`**: "Clean up Git worktrees" opens with the five behaviour
  changes users will notice (R2, R6, the `unstarted-branch` and
  `reflog-unavailable` refusals in single mode, M4, and `--worktree P`
  removing a merged worktree whose upstream was deleted on its local
  ancestry, its branch kept, by Brett Heap's ruling; Decisions), then
  describes the batch preview and apply,
  `--expect-plan`, the gates, the 16-per-run deferral that re-running drains,
  the narrow guarantee and residual window, and the result record and
  recovery; its sentence "Apply actions are
  always explicit and target one branch or worktree" (README:106) is
  corrected. Install (README:17-19) states the Git 2.36 requirement, and the
  exit-code line (README:194-196) gains `clean`'s 1 for an incomplete
  preview, 143 and 129, Git's own status passing through.
- **`tests/test_project.py`**: each ADDED and MODIFIED requirement has a test
  named after its scenario; disposable-repository tests for the packet's 35
  batch scenarios (`BA:1347-1628`) as the deltas carry them; a counting `git`
  wrapper that pins each child's `-C` directory and the probe counts; hooks
  for the residual window, the branch race, deadline expiry and SIGINT;
  value-parity tests against the baseline except the listed changes; fake
  `git`s that flood stderr, ignore SIGTERM, or print 5,000 `!!` records;
  every scenario the council added (Capabilities); and scenarios for this
  proposal's own decisions: a failed status probe on the merge-target row,
  and a failed root status in `clean`, `status` and `doctor`, read
  `inspection-error` (R1); plain `clean` over 256 rows exits 1 (R2); under
  Git 2.35 `clean` exits 2 with `git-too-old`, `status` marks the row
  `inspection-error`, and `doctor` exits 1 on its error row (R6); a relative
  path inside a bare repository's linked worktree is refused (R10);
  `--apply --json` stdout holds one document and stderr the prompt (OQ-10);
  SIGTERM mid-removal waits for the child, then reconciles and exits 143
  (OQ-16); a deleted upstream's status and doctor rows carry the C3 values;
  a manifest over 1 MiB refuses `manifest-invalid`. The 94 existing tests at
  `7a9134b` (43 at `da33d92`, 51 added by PR #8) keep passing, except
  `test_clean_revalidates_a_worktree_after_confirmation`
  (`tests/test_project.py:590-611`), which moves to the result record; the
  message assertions at `:409-425`, `:450-467` and `:542-546` keep passing
  because `target-excluded` and `no-merge-target` keep the baseline wording.
  Non-UTF-8 path scenarios run on Linux only, skipped on macOS with that
  reason; ordering tests use names that differ by more than case; the OQ-4
  measurement fits the caps on a Linux path, drvfs only a degraded case. The
  command is `python3 -m unittest discover -s tests -v`, on Linux and macOS
  with Python 3.10 and 3.12, as CI runs (`.github/workflows/tests.yml:9-18`).
- **Speckit handoff**: implementation goes to exactly one Speckit feature,
  `specs/004-<slug>/`, created by `/speckit.specify` after ratification
  (`002` is lane openRepoProject-1's `002-triad-first-project-new`, merged by
  PR #8 at `d7f6b0e`). OpenSpec `tasks.md` holds governance boxes, the OQ-4
  measurement among them, and that one handoff only.
- **workBenches**: `onp` carries the batch once its owner moves the pin.

### Dependencies and Sequencing

- **This change depends on nothing unmerged.** This branch has merged `main`
  at `7a9134b`. PR #8 merged at `d7f6b0e` (`002-triad-first-project-new`, 141
  lines inserted in `project`, tests 43 to 94), and PR #13's archive of
  `prefer-triad-in-project-new` merged at `7a9134b`, so `project-command`
  now carries its MODIFIED `Delegate project creation` and six ADDED
  requirements. This change MODIFIES `Inspect and diagnose` and
  `Explicit maintenance`, both verbatim and unchanged at `7a9134b`, ADDS
  one requirement there and touches none of the archive's seven
  (Capabilities); `project-clean` and `project-clean-review-safety` are
  unchanged since `da33d92`. It does not depend on PR #2's commits (closed
  unmerged; harvest source only).
- **Citations stay pinned at `da33d92`.** At `7a9134b` lines 285 to 1007 of
  `da33d92`'s `project` (`discover` onward) sit 141 lines lower, with `probe`
  and `execute` unmoved, the cited test lines 383 lower and the README
  citations up to 88 lower, and feature 004's specify and plan re-pin every
  citation against the `main` of that day.
- **`add-project-overview` depends on this change.** Its `--all-safe`
  suggestion is gated by this change's gates and refusal codes
  (`SY:287-306`), and it reuses this change's evidence model, ladder function
  and Git 2.36 refusal (`SY:39-51`, `SY:78-109`). It should be ratified after
  this change, and re-aligned if this change moves before ratification.
- **Implementation order.** Feature `004-<slug>` lands before the overview's
  `005-<slug>`. PR #8 has landed, so feature 004 builds on its `project` and
  tests and merges `main` into its branch as `main` moves. Never rebase: the
  organisation ruleset refuses force pushes.

## Out of Scope

- **Paired retirement (branch deletion with the worktree).** The PR #2
  decision record (comment 6035824335, on Brett Heap's word "go with your
  recommendation", 2026-10-07) requires any future paired-retirement
  proposal to be a MODIFIED requirement on `project-clean`, "Clean can
  explicitly retire verified worktrees" (`project-clean/spec.md:55`), because
  it changes `remove` (`BA:56-63`; `HO:36-39`). Its post-removal stage
  contract is `BA:1339-1345`; harvest source `5fc2b51`.
- **Cache disposal, the first follow-on change** (`OV:144`, `OV:151-152`;
  `BA:1314-1337`): the council's survey found Omnigent-Install's 20 of 29
  merged worktrees excluded for caches alone.
- **Patch-equivalence retirement of squash-merged branches**, a follow-on
  change (`BA:195-199`; Open Questions).
- **Remote, GitHub and PR queries** (`DI:72-75`, `DI:1036-1060`; `HO:160-167`).
- **Family traversal and relationships** (`SY:34-37`; `DI:276-290`).
- **Bench, container and park integrations** (`OV:142-146`; `DI:1062-1064`).
- **`project overview`, `--attention` and the doctor repository-health
  absorption** (`acf0133`, `80fdef3`): `add-project-overview`.
- **Also excluded by the packet**: estate-wide destructive batches, merge
  or branch reconciliation, a lock or writer-quiescence protocol
  (`BA:1645-1650`), a persistent cache or resumable plan, continuing after a
  failure (`BA:1640-1643`), and the exact bench/type doctor check
  (`OV:148-157`, `OV:361-366`; `SY:233-235`).
- **Bare-repository support and user-configurable limits** (OQ-15, OQ-8).

## Decisions Taken by This Proposal

Each is a proposal decision, open to ratification; OQ numbers are the lane's
decision list. Packet open decisions taken, each citing the packet text that
leaves it open:

- **OQ-4, measured costs** (`BA:723-724`; `OV:314-319`): measured by governance
  task 2.1 on 2026-10-09, and the caps stand as measured. The measurement was
  the warm and cold-cache one (`DI:179-180`, `DI:189-190`, `DI:227-228`;
  `OV:314-319`) on this workstation (Git 2.43, WSL2) and a Linux filesystem
  path, reapplying the fit test of `BA:729-735`; it timed the combined probe
  and `for-each-ref` against index size and branch count and a large removal,
  and counted each repository's rows per gate beside the timing (N5). The fit
  rejects no cap; it rejects them only in two degraded cases, rows of
  100,000-entry indexes and CPU saturation, which design Risks record, where a
  plan goes incomplete and never unsafe. The survey also found that a
  repository whose every worktree carries a gitlink yields no removable row and
  its deferred count never drains (design Risks, D18). drvfs was not available
  on this workstation and is unmeasured (R-24).
- **OQ-8, configurable limits** (`OV:332`): none; fixed values are reported
  in `limits` and `budget`.
- **OQ-10, `--apply --json`** (`BA:1189-1198`; `project:523-524`): allowed
  for removal only (`--all-safe`, `--action remove`), as the packet
  recommends; with `--action push` or `delete-branch` it stays refused.
- **OQ-11, `--expect-plan` with `--yes`** (`BA:377-379`): optional.
- **OQ-12, relative path or no argument** (`BA:1664-1666`): resolve to the
  repository Git finds there.
- **OQ-13, sparse skip-worktree entries** (`BA:1667-1668`): not safe;
  `hidden-local-state`.
- **OQ-14, a never-populated gitlink** (`BA:1669-1671`): not removable;
  `contains-submodule`.
- **OQ-15, bare repositories** (`BA:1662-1663`): refused in every `clean`
  mode with `target-not-repository-root`, exit 2 (R10). The packet sketches
  support (`BA:215-226`); this proposal defers it.
- **OQ-16, SIGTERM and SIGHUP** (`BA:1660-1661`): in the apply phase the
  SIGINT treatment, exiting 143 and 129 in the 130 row of `BA:530-536` (the
  first signal received sets the status); before it, probe children are
  terminated and reaped as on SIGINT and the exit is 143 or 129 with zero
  mutation, where `BA:474-477` leaves them outside the contract. After
  SIGHUP output may fail with `EIO`, so the record is printed best effort.
  A removal child in flight is waited for, never signalled.
- **OQ-26, spelling** (`OV:356`): keep `--all-safe` and `--expect-plan`.
- **OQ-27, extensions** (`OV:357-359`): cache, paired retirement, remote,
  family, bench, container and park each need their own change.
- **OQ-28, the ladder** (`DI:599-600`): a pure function over evidence.

Departures from packet decisions, each citing the decision departed from:

- **OQ-23, Git 2.36 scope** (`BA:1241-1245`; `OV:231-234`): narrowed by R6.
  Design verifies each probe, the variable list and the removal refusals on
  Git 2.36 itself, by a fixture run against a pinned 2.36 build or a CI job,
  or raises the floor to the lowest version verified.
- **The 2.36 floor kept, with `GIT_INTERNAL_SUPER_PREFIX` scrubbed** (R-21; a
  departure from task 2.2's rule, "the floor is raised to the lowest version
  verified", and from D17's matching sentence): task 2.2 compared Git 2.36.6,
  2.40.4 and 2.43.0 on 75 captures and found rows 1 to 6 identical and one
  difference in row 7. `rev-parse --local-env-vars` prints
  `GIT_INTERNAL_SUPER_PREFIX` on 2.36 through 2.39 and not from 2.40, and with
  it set every command on 2.36 fails closed. Applying the rule would raise the
  floor to 2.40; the lead kept 2.36 and added the name to the scrub, sixteen
  names then and seventeen with R-25's `GIT_ALLOW_PROTOCOL`, because raising
  would exclude Debian 12's Git 2.39 for a one-name difference. Open to Brett
  Heap at ratification.
- **OQ-24, JSON compatibility** (`BA:949-953`; `HO:210`): one
  `schema_version: 1` envelope for every `clean --json`, not an "additive
  superset" (R7). Baseline keys keep their names and types, the scope the
  packet's phrase meant; `root`, the meaning of `ignored_files` and a `null`
  `present` are the listed baseline changes.
- **OQ-5, the target cap's refusal** (`BA:96-101`, `BA:1004`,
  `BA:1367-1371`), open to Brett Heap's ratification: retired for the
  deferral (What Changes), the council's survey having found about 20 such
  rows in Opensoft-Tenant. Rows an index gate then excludes keep their
  places, so 16 of them ahead of a backlog stop it until handled by hand.
- **Per-child budget without a deadline** (V10; `BA:1238-1240`,
  `OV:228-230`; M5): `status`, `doctor` and `update` keep 15 s (no deadline
  for 5 s to protect; a timeout there now fails doctor and refuses `update
  --apply`), withdrawing D-B's and D-M's 5 s.
- **Single-target completeness** (V4; `BA:188-192`, `BA:419-420`,
  `BA:1268-1272`, `BA:1562-1563`, and the Resolution record, `HO:208`,
  `HO:247-249`; M5): another row's state no longer refuses `--worktree P`;
  refusing it leaves a raw `git worktree remove`, which skips every gate.
- **The runner** (`BA:1212-1213`, which gives `probe()` a timeout argument):
  a new bounded runner instead (Impact).
- **Validity flags and sample objects** (R-9; `BA:804-806`, `BA:963-964`):
  each `ignored_samples` entry is an object `{path, path_valid_utf8}` where
  the packet has a bare path string, and every serialized path value carries
  its validity flag beside it (`path_valid_utf8`, and `root_valid_utf8` and
  `common_dir_valid_utf8` in `repository`), so an escaped `\xHH` never reads
  as a valid path holding those four characters.
- **Escaping by general category** (R-8; `BA:917-934`): every code point of
  Unicode general category Cc, Cf, Zl or Zp is escaped, where the packet
  enumerates control, bidirectional and format characters, and human output
  writes a code point above U+FFFF as `\UXXXXXXXX`, where the packet has the
  single `\uXXXX` form.
- **The manifest cap detected from `st_size`** (R-4; an addition, no packet
  text behind it): a manifest over the 1 MiB cap is detected from its
  `st_size` before the read, never by reading past the cap.
- **Local ancestry outranks a deleted upstream** (open question 1, ruled by
  Brett Heap on 2026-10-09 in his word to lane openRepoProject-2,
  "yes, local ancestry proof outranks remote-gone, apply it";
  `DI:596-598`, the ladder's "same test order" and "same
  recommendation text", and `BA:1214-1220`, `DI:1124-1129`, `SY:107-109`,
  `OV:210-212` and `HO:296-298`, where a deleted upstream is `remote-gone`
  and preserved whatever its merge state): for worktree rows the ladder
  tests `merged_into_target` before the `remote-gone` rung, so a merged row
  whose upstream was deleted is `merged-removable`, or `merged-current` when
  it is the current worktree, with that class's recommendation and the
  ordinary gates, and `remote-gone` is left to unmerged rows. The MVP never
  deletes the branch, so its commits stay reachable from the kept branch and
  the merge target. At `a040790` such a worktree reads `unpublished` (R9)
  and `--worktree P` refuses it; now `--worktree P` and `--all-safe --apply`
  remove it when its gates pass, a baseline behavior change and the fifth
  behaviour change users will notice (What Changes, first bullet). A
  selected row of this kind records its configured `upstream` with
  `upstream_oid`, `ahead` and `behind` null, where `BA:969` types them
  string and integer, and its revalidation counts a value null in the plan
  and null again as no difference (`Cleanup revalidates destructive
  actions`); push still refuses its branch with `remote-gone`, whatever its
  row's class (D-D). The interim recommendation that called such a row not
  removable is withdrawn.

Packet decisions adopted, not open: OQ-5, the caps and bounds of `BA:966`,
subject to OQ-4, less the target cap's refusal; OQ-9, the budgets of
`BA:427-458` and `BA:467-468`; OQ-25, Git's status passing through
(`BA:528-543`), as `project:157-162` does, the record disambiguating. Lane
additions, with no packet text behind them:

- **OQ-1, one change or two**: two, batch first (this change).
- **OQ-3, revise the packet first**: no; citations stay at `da33d92`, and the
  readings and corrections here bind until the packet revision merges.
- **OQ-22, a doctor health section**: none; doctor changes only through the
  shared evidence, its Git check row included (R6). `add-project-overview`
  records that `acf0133`'s unmerged `project-doctor-repository-health`
  capability is superseded by `project-overview` (its OQ-22).
- **OQ-29, the plain report**: the same plan builder with `mode: "report"`,
  under the deadline and a 256-row cap by the same fit rule (7 + W + 16
  children; 256 rows take 41.85 s at 150 ms), apply modes keeping 128 rows
  and 16 targets (R2); it carries every plan field, `selected` being what
  `--all-safe` would select (for at most 128 worktree rows; above 128
  `selected` is null and `notes` carries an `inspect-cap` entry with the row
  count, beside the human line saying that `--all-safe` itself would be
  incomplete with `inspect-cap`; R-15), `plan_digest` computed (above 128 rows
  over a null `selected`, never consumable by `--expect-plan` because the
  incomplete apply is refused first; at most 128 rows equal to the `--all-safe`
  preview's for the same repository identity, merge target and selection, an
  `--expect-plan` carrying it matching, which is intended, while a target that
  advances between the report and the preview gives `plan-digest-mismatch`,
  which is safe; R-17, R-19), `apply_allowed` false and the deferral applied
  as in a preview.

Council decisions, with the packet text each replaces or extends:

- **A started removal is never interrupted** (V1; a departure from
  `BA:396`, `BA:401-402`, `BA:437-439`, `BA:456-458`, `BA:466-468` and the
  Resolution record, `HO:208`, `HO:247-249`; M5): TERM at 0.25 s left 18,333
  of 20,000 files, a `dirty` tree (council).
- **Pinned status configuration** (`BA:307-317` pins only the untracked
  setting): unpinned, Git's own check missed and deleted a file (council).
- **Lazy fetches pinned off on every Git child** (R-23, R-25; an addition to
  `BA:243-253` and `BA:307-317`, which pin no protocol policy): Git 2.43 has
  no `GIT_NO_LAZY_FETCH`, so a read-only probe in a partial (promisor) clone
  can fetch a missing object from the network. `-c protocol.allow=never` makes
  the fetch fail locally and the row `inspection-error`, but it is only the
  default policy: a `protocol.<name>.allow` setting in the repository's
  configuration outranks it for that protocol, and so does `GIT_ALLOW_PROTOCOL`
  in the caller's environment. Every Git child therefore also pins `-c
  protocol.file.allow=never -c protocol.ssh.allow=never -c
  protocol.git.allow=never -c protocol.http.allow=never -c
  protocol.https.allow=never -c protocol.ext.allow=never`, which outrank every
  configuration file, and the scrub removes `GIT_ALLOW_PROTOCOL`, which no `-c`
  outranks, seventeen names in all. Accepted residual: a remote-helper protocol
  of another name with its own `allow=always` in the repository's configuration
  could still fetch; the probe then succeeds rather than fails, and no unsafe
  removal follows (design Context, D11, Risks).
- **A branch with no commit of its own is preserved** (V2 as amended, M3, M4;
  extends the gates of `BA:152-160`; R-12, R-15): the reflog, read from its
  anchor, the last entry whose old object is all zeros (a creation, whatever
  command wrote it) or whose message begins `branch: Created from` or
  `branch: Reset to`, decides `unstarted-branch` in every case, because a
  head equal to the merge-target SHA is also where a fast-forward-merged
  branch sits; a reflog that is missing, empty, bound-reaching or undecidable
  is `reflog-unavailable` (What Changes, eligibility).

Left to `add-project-overview`: OQ-2, OQ-6, OQ-7, OQ-17 to OQ-21, and the
overview halves of OQ-5, OQ-9, OQ-25 and OQ-26.

Readings of packet gaps:

- **R1, failed status probe on the merge-target row.** The ladder tests the
  merge-target branch before `dirty is None` (`project:421-426`), so such a
  row reads `protected-default`, while `BA:641-644` and `BA:789-790` make a
  failed probe `inspection-error`. Reading: a failed or timed-out status
  probe sets the row to `inspection-error` directly, as unreadable and
  mismatched rows already are (`DI:263-266`), so the plan is incomplete.
  Likewise a failed `git status` in a repository root or leg, which at
  `a040790` raises `Refused` (`project:326-328`, `:995-1000`) and ends
  `clean`, `status`, `doctor` and the `update` report with exit 2, becomes a
  row-level `inspection-error`: `clean` reports an incomplete plan, and the
  others report instead of refusing. Both are baseline behavior changes
  with parity tests.
- **R2, the plain report under caps and deadline** (`BA:91-101`,
  `BA:413-419`; `OV:228-230`). Reading: OQ-29; it exits as a preview does,
  0 complete, 1 incomplete, 2 when no report can be built (`BA:547-549`).
  That is a baseline change: plain `clean` exits 0 whenever it prints today.
- **R3, the classification list; R4, noninteractive targets**: MODIFIED
  `:25` names all 15 classes, and MODIFIED `:70` `--all-safe` as a target.
- **R5, `project-review-safety`'s exit 2**: consistent with every `clean`
  resolve refusal and every refusal under `--apply` (Capabilities); its
  conflict is with the overview, which `add-project-overview` resolves.
- **R6, Git 2.36 scope, narrowed.** The version check runs only before a Git
  repository is inspected; a directory with no `.git` keeps `present: false`
  (`project:317`, `:322-325`). `clean` refuses `git-too-old` or
  `git-unavailable`, exit 2, before any probe, its `{"error"}`
  (`project:996-997`) gaining `code`. `status`, `doctor` and `update` never
  refuse: doctor reports old or unusable Git as an `error` check row
  (`project:828-829`), status marks rows it cannot inspect `inspection-error`,
  and `update`'s `tools` and `workflow` components need no Git
  (`project:884-885`, `:905-906`). This deliberately departs from the packet's
  doctor refusal (`OV:231-234`, `DI:1156-1160` and `BA:1241-1245` agree),
  which would hide doctor's own `git` row (`project:755-757`).
- **R7, "additive superset"** (`BA:949-953`; the Resolution record, `HO:210`):
  dropped. `root`, the meaning of `ignored_files` and a `null` `present` are
  meaning changes, which the packet's own rule (`BA:943-945`) versions;
  `schema_version: 1` lists them against the unversioned baseline.
  `status --json` and `doctor --json` stay unversioned here; they gain an
  `inspection-error` marker on root and leg dicts (`project:370-373`, `:699`)
  in a field matching worktree rows (`repository.classification` or an
  `errors[]` list; the delta names one), nulls where they exit 2 today, C3's
  `upstream`, a lower-bound `ignored_files`, `path_valid_utf8` beside each
  `path` and `root_valid_utf8` beside `root`, and doctor's `error` rows (R6).
- **R8, the test command**: `python3 -m unittest discover -s tests -v`; a
  bare `python3 -m unittest` runs 0 tests (`tests/` has no `__init__.py`).
- **R9, deleted upstream re-verified** (`BA:1214-1220`; `DI:1124-1129`). The
  packet's scratch-check claim holds. Re-run at `da33d92` with Git 2.43:
  `rev-parse --abbrev-ref @{upstream}` fails, the row classifies
  `unpublished` like a never-configured upstream, and `for-each-ref` reports
  `gone`; the `remote-gone` rung (`project:442`) is unreachable today.
- **R10, bare repositories refused** (`BA:221-224`). In every `clean` mode a
  repository whose common directory has no main worktree (a bare one) is
  refused with `target-not-repository-root` and exit 2, including from a
  relative path, no argument or a bare name inside one of its linked
  worktrees. At `a040790` `clean` reports such a repository and can remove its
  worktrees (`project:337-352`). This replaces `BA:1255-1256` (OQ-15).
- **R11, gitfile and submodule checkouts** (`BA:215`, `BA:858`). Where `.git`
  is a file, Git 2.43 lists the git directory as the first registry record.
  Reading, in this order of precedence (M6): a submodule checkout is tested
  first, and where `rev-parse --show-superproject-working-tree` prints a path
  the argument is refused `target-not-repository-root`; otherwise, when that
  record equals `common_dir`, the main worktree is the realpath of
  `core.worktree` or, where that is unset (as `git init --separate-git-dir`
  leaves it, verified here), the candidate toplevel whose `.git` file names
  `common_dir` itself. A root equal to it resolves, the git directory is never
  a probed row, and a linked worktree whose main checkout cannot be named is
  refused `target-not-repository-root`; `a040790` exits 0 in both refused
  cases.

## Corrections to the Packet

Citations stay at `da33d92`. The packet author (lane openRepoProject-3) is
revising the packet for C1, C3, C4, `BA:169-177`, `BA:424-425`,
`BA:1212-1213`, `DI:1119-1120`, `DI:260`, `DI:607-609`, `DI:1387-1388` and
OQ-29's cap; these bind until that revision merges (C2 is now reading R9).

- **C1, stale baseline sentences.** `DI:28` and `BA:30` say `origin/main` "is
  now `ca4c615`", and `OV:163` and `HO:200` that it "has since advanced to
  `ca4c615`"; PR #7's squash `da33d92` superseded it. `HO:365-366` records
  PR #7 as opened and `HO:377-380` as "open for review"; it merged as
  `da33d92`. `DI:33-35` and `BA:39-42` omit `acf0133` and `09af8c8`, which
  `OV:176-178` lists, and all three omit `80fdef3`; the PR #2 decision
  record's harvest table is the authority.
- **C3, doctor and `remote-gone`.** `BA:1219-1220`, `OV:210-211`, `SY:107-108`
  and `HO:296-298` say doctor reports `remote-gone`. Doctor classifies no
  worktree (`project:728-758`; `repo_state` sets only `stale-worktree`,
  `project:352`); `DI:1127-1129` is right that doctor "reads the same
  evidence". What changes there is the values its rows carry, under the ADDED
  `project-command` requirement: for a deleted upstream a status or doctor
  row's `upstream` changes from `null` to the configured short name (such as
  `origin/<b>`, as R9's re-run shows) and `ahead` and `behind` stay `null`.
- **C4, Python 3.10.** `BA:397-398` starts the removal child with
  `Popen(..., process_group=0)`, which Python added in 3.11, while README:17
  requires 3.10+ and CI runs 3.10. Design uses `Popen(start_new_session=True)`
  (3.2+) for each child's own process group, never `preexec_fn`, and runs
  abandonable filesystem calls on daemon `threading.Thread`s, not a
  `concurrent.futures` pool.

## Open Questions

- **Squash-merged branches.** A squash merge never puts the branch tip into
  the target's ancestry (`BA:195-199`), and this repository's `main` has no
  merge commit, so in squash-merging repositories the MVP selects little.
  Before Brett Heap, recommending a local patch-equivalence proof (`git
  cherry` or patch IDs against the target) as a follow-on change.

The question of a merged worktree whose remote branch was deleted is closed:
Brett Heap ruled on 2026-10-09 that a local ancestry proof outranks
`remote-gone` for worktree rows (Decisions, departures).

## Questions Resolved by the Alignment Review

SA and QA findings on `fed64d4`; rulings D-A to D-L bind where they differ.

| Findings | Severity | Ruling | Section edited |
| --- | --- | --- | --- |
| SA-1, SA-8 | MISMATCH, DRIFT | applied per D-G | Impact (`project`); What Changes (evidence model); Corrections C4 |
| SA-2, SA-5, QA-5 | MISMATCH, DRIFT, GAP | applied per D-B (QA-5's refusal text superseded by it) | What Changes (evidence model); Capabilities (`project-command`); Impact; OQ-22, OQ-23; R6 |
| SA-3, QA-2, QA-10 | MISMATCH, MISMATCH, GAP | applied per D-C | What Changes (single-target, JSON); OQ-10 |
| QA-7 | GAP | applied per D-D | What Changes (single-target); Capabilities (`:39`, review-safety `:38`, `:49`) |
| SA-12, QA-3 | DRIFT, MISMATCH | applied per D-E (QA-3 as R10, not R9) | Why; What Changes (resolution, evidence model); Capabilities (Git-first); OQ-15; R9, R10; Corrections |
| SA-11, SA-13, QA-1, QA-9 | DRIFT, DRIFT, MISMATCH, GAP | applied per D-F | What Changes (reconcilable, bounded work); Capabilities (other capabilities); OQ-16; R5 |
| SA-14 | DRIFT | applied per D-K | Status; Impact (Dependencies and Sequencing) |
| QA-8 | GAP | applied; amended per D-T (both `origin/` strips) | Capabilities (Git-first ADDED) |
| QA-12 | GAP | applied; R6 scenario superseded by D-B, R2 scenario at 256 rows per D-V | Impact (tests) |
| QA-14 | GAP | applied; caps sentence superseded by D-Q | What Changes (spelling, eligibility, bounded work, paths); Impact (README, tests); Corrections C3 |
| SA-4, QA-13; SA-6, QA-6 | MISMATCH, GAP; DRIFT, GAP | applied | Rules This Change Keeps, Capabilities (review-safety `:21`); Capabilities (`:25`, `:55`, review-safety `:49`) |
| SA-7; QA-4; QA-11 | DRIFT; MISMATCH; GAP | applied | OQ-23; Why; OQ-29 |
| SA-9, SA-10 | DRIFT | applied; drvfs named instead of a host path (SA-9), measured as degraded per the council | Impact (tests) |

Later rulings from the packet author's fidelity reads: D-M (`project-command`
ADDED; its 5 s for `status`, `doctor`, `update` withdrawn by the council),
D-N and D-S (R1; `Inspect and diagnose`, D-S narrowed to nulls meaning "not
established"), D-B relabelled (R6), C1, C8 (R7), D-Q (OQ-4), D-R (`Explicit
maintenance`), D-T (Git-first), D-U, D-V and D-W (Bounded work; OQ-29; D-U's
refusal retired by the council), D-X (OQ-16), D-Y (Why), D-Z (Decisions),
D-AB (Corrections; OQ-3), D-AC (Impact; Decisions), D-AD (OQ-24), D-AF
(`project-command` ADDED), X2 (R11), the remote-gone question, and the 1 MiB
manifest cap from lane 3's final read of `add-project-overview` (What
Changes, evidence model; `project-command` ADDED; Git-first). Lane 3's delta
read at `ea9c73b`: M1 (What Changes, reconcilable), M2 (What Changes, person
sees), M3 and M4 (What Changes, first bullet, eligibility, evidence model;
Capabilities `:55`), M5 (What Changes, bounded work; Decisions), M6 (R11) and
M7 (What Changes, evidence model; `project-command` ADDED), with the manifest
cap listed as a baseline behavior change. The lead's V2 as amended (the reflog
read in every case; What Changes, eligibility; Capabilities `:55`; Decisions,
council; design D10, Risks), and the lead's rulings, hyphenated to keep them
apart from this proposal's readings R1 to R11: R-4 (the manifest cap's
`st_size` detection), R-8 (escaping by general category) and R-9 (validity
flags on every path value), each under What Changes and the departures in
Decisions; R-11 (the apply order, the exits of a preview, the report's row
limit, signals under `--json`, the 64 s bound; What Changes, batch preview,
fresh plan, bounded work, JSON; Capabilities `:10`, batch, bounds, result,
JSON, `Inspect and diagnose`; OQ-29; R7; design D9, D14 to D16, D19, D20);
R-12 (the reflog anchor and its one outcome rule, the expired-reflog
refusals, the departures, the remedies; What Changes, first bullet,
eligibility, evidence model; Capabilities batch, `:55`, review-safety `:21`;
Decisions, departures and council; Impact, README; this list; design
Context, D10, D18, Risks, Migration Plan); R-13 (the null `root` probe
directory; `project-command` ADDED; design D6); R-14 (the `unstarted-branch`
remedy and its Risks line; What Changes, first bullet; design D18, Risks,
Migration Plan); R-15 (the anchor on any entry whose old object is all
zeros, the `reflog-unavailable` remedy, the 64 KiB residual, the report's
JSON above 128 rows; What Changes, first bullet, eligibility; Capabilities
`:10`, batch, `:55`, JSON, review-safety `:21`; Decisions, OQ-29 and
council; this list; design Context, D10, D14, D18, D19, Risks, Migration Plan;
`tasks.md` 1.2); R-17 (the report above 128 rows runs the gates per inspected
row, so `excluded` lists every row a gate excludes and only the selection is
withheld, and the report's digest rule; `project-clean` plain-report
requirement, band text; Decisions, OQ-29; design Context, D14; `tasks.md`
1.2); R-19 (R-17's digest rule scoped to the band above 128 rows, the
report-mode `inspect-cap` note in the normalised notes, and R-15's credit on
D19; `project-clean` plain-report requirement, band text; Decisions, OQ-29;
design Context, D14, D19; `tasks.md` 1.2); R-21 (task 2.2's result:
`GIT_INTERNAL_SUPER_PREFIX` added to the scrub as a sixteenth name and the
2.36 floor kept; `project-command` ADDED, evidence model; Decisions,
departures; this list; design Context, D6, D17; `tasks.md` 2.2); R-22 (the
revalidation clause's other side, a deleted upstream that reappears before apply
is `state-changed`; `project-clean-review-safety` `Cleanup revalidates
destructive actions`, scenario "Deleted upstream reappears before revalidation";
this list; design Context, D20; `tasks.md` 1.2, 1.4); R-23 (`-c
protocol.allow=never` on every Git child, so that a lazy fetch in a partial
clone fails locally and the row is `inspection-error`; What Changes, seam and
evidence model; Capabilities, `project-command` ADDED and review-safety `Cleanup
revalidates destructive actions`; Decisions, departures; the deltas' `Clean can
explicitly retire verified worktrees`, `project-command` ADDED evidence model
and its scenario "A lazy fetch in a partial clone is refused locally"; this
list; design Context, D6, D9, D11, D20; `tasks.md` 1.2, 1.4); R-24 (the clean
OQ-4 measurement, task 2.1: the caps stand as measured, the fit's two
rejections, rows of 100,000-entry indexes and CPU saturation, are degraded
cases recorded as risks, and the residual of a repository whose every worktree
carries a gitlink, whose deferred count never drains, is recorded with the
human report's sentence saying why; What Changes, bounded work; Decisions, OQ-4;
the deltas' `Clean bounds its Git work and reports omitted work`, the caps and
deferral text; this list; design D5, D9, D11, D12, D18, Risks, Migration Plan;
`tasks.md` 1.2, 2.1); and R-25 (R-23's gap: `protocol.allow` is only the default
policy, so every Git child also pins the six per-protocol policies and the
scrub gains `GIT_ALLOW_PROTOCOL`, seventeen names, with the residual of a
remote-helper protocol of another name accepted; What Changes, seam and
evidence model; Capabilities, `project-command` ADDED evidence model and its
scenario "A lazy fetch in a partial clone is refused locally", and review-safety
`Cleanup revalidates destructive actions`; Decisions, departures; the deltas'
`Clean can explicitly retire verified worktrees`; this list; design Context, D6,
D9, D11, D20, Risks; `tasks.md` 1.2). Brett Heap's
ruling of 2026-10-09 on open question 1, given to lane openRepoProject-2 in the
words the departures quote, that a local ancestry proof outranks `remote-gone`
for worktree rows, closes that question and adds the fifth behaviour change
users will notice (What Changes, first bullet, eligibility and evidence model;
Capabilities `:25`, `:39`, review-safety `:49`; Decisions, departures; Impact,
README; Open Questions; this list; design Context, D6, D7, D20, Risks, Migration
Plan, Open Questions; `tasks.md` 1.2, 1.6; the deltas' `Clean classifies
preservation and cleanup actions` and its scenario "A merged worktree whose
upstream was deleted", `Clean can explicitly push safe feature branches` and
`Cleanup revalidates destructive actions`).

### Council Verdicts

The council reviewed `0ed2f59` (labels its own: PA product advocate, SA
systems architect, AE adversary engineer). Every concern is VALID, none
dismissed; the parts noted for design are `clarifications.md` N1 to N5.
The lead's verdict labels, cited above, map to concerns as V1 AE-1, V2 AE-2,
V3 AE-3, V4 SA-1 with AE-5, V5 PA-1, V6 PA-2, V7 PA-3, V8 PA-4, V9 SA-2, V10
SA-3, V11 SA-4 and V12 AE-4.

| Concern | Severity | Verdict | Section changed |
| --- | --- | --- | --- |
| PA-1 | HIGH | VALID; departure | What Changes (person sees, bounded work); Capabilities (bounds); Decisions (OQ-5, OQ-4); Impact (README) |
| PA-2 | HIGH | VALID | Why; What Changes (person sees); Out of Scope |
| PA-3 | MEDIUM | VALID | Capabilities (`:25`); Open Questions; Impact (README) |
| PA-4 | MEDIUM | VALID | What Changes (first bullet, person sees); Capabilities (batch, reconcilable); Impact (README) |
| SA-1, AE-5 | HIGH, MEDIUM | VALID; departure | Why; What Changes (single-target); Rules (never prune); Capabilities (`:55`); Decisions |
| SA-2 | MEDIUM-HIGH | VALID; loop mechanics NOTED (N1; X1 as N2) | What Changes (evidence model); Capabilities (`project-command` ADDED); Impact (`project`, tests) |
| SA-3 | MEDIUM | VALID; departure; protocol NOTED (N5) | What Changes (evidence model); Capabilities (`project-command`); Decisions (budget, OQ-4) |
| SA-4 | LOW-MEDIUM | VALID | Capabilities (`:22`); R7 |
| AE-1 | HIGH | VALID; detection NOTED (N4) | What Changes (seam, reconcilable, bounded work); Rules; Capabilities (`:25`, `:55`, bounds, result); Decisions (council, OQ-4, OQ-16); Impact (tests) |
| AE-2 | HIGH | VALID; `in-use` gate NOTED (N3) | What Changes (eligibility); Capabilities (`:55`, review-safety `:21`); Out of Scope; Open Questions |
| AE-3 | MEDIUM-HIGH | VALID | What Changes (seam, evidence model); Rules; Does Not Own; Capabilities (`:55`, review-safety `:49`); Decisions (council) |
| AE-4 | MEDIUM | VALID | Citations (pinned at `da33d92`); Why; Capabilities (`project-command`); Impact (tests, Speckit handoff; Dependencies and Sequencing), after merging `main` at `7a9134b`; Corrections C1 |
