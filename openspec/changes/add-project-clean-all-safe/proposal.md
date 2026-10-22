Lane: openRepoProject-2

# Proposal: add-project-clean-all-safe

Status: ratified by Brett Heap on 2026-10-09, in his words to lane
openRepoProject-2, "ratify, merge #11 and run the runbook". It lands by
squash-merge of PR #11, with the Speckit handoff `004-project-clean-all-safe`
to follow.
Revised after the alignment review and the council (resolved below and on
PR #11; the council's noted constraints are in `clarifications.md`); it adds
Decisions and Corrections sections because it adopts a non-normative packet,
and Open Questions for the two questions still before Brett Heap.

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
  worktree remove yourself (--force if it holds a submodule)". A merged worktree
  whose branch reflog keeps no decisive entry (the branch saw no activity for
  `gc.reflogExpire`, 90 days by default) is likewise refused in single mode
  (`target-excluded`, reason `reflog-unavailable`) as well as withheld from the
  batch, with the remedy "the branch's reflog is missing, expired or
  undecidable; review, then git worktree remove yourself (--force if it holds a
  submodule)". And where `a040790` refuses a merged worktree whose upstream was
  deleted as `unpublished`, `--worktree P` now removes it as `merged-removable`
  when its gates pass, its branch kept (Brett Heap's ruling of 2026-10-09;
  Decisions). The README's clean section states these five first.
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
  `registration-mismatch` (two-way admin registration, and a linked
  worktree's effective work tree being its registered path, LQ-11),
  `locked-worktree`, the
  baseline classification when not `merged-removable`, `not-requested`,
  `unstarted-branch`, `deferred-target-cap` (Bounded work),
  `contains-submodule` (any gitlink or admin `modules` entry),
  `hidden-local-state` (any entry flagged assume-unchanged or skip-worktree),
  `operation-in-progress` (a merge, autostash, notes merge, cherry-pick,
  revert, `am`, rebase or bisect marker in the worktree's administrative
  directory; Brett Heap's ruling LQ-14) and `worktree-only-commits` (a commit
  that only the worktree's HEAD reflog or `refs/worktree/` holds, which no
  branch, tag, remote-tracking ref or the branch's reflog reaches, or a HEAD
  reflog over its 64 KiB bound or with a line that does not parse; Brett Heap's
  ruling LQ-13), the last four read in the row's own worktree or administrative
  directory (`BA:113-150`, `BA:629-675`, `BA:554-583`). A merged worktree whose
  upstream was deleted is `merged-removable` and faces these gates like any
  other merged row, since local ancestry outranks `remote-gone` for worktree
  rows (Brett Heap's ruling of 2026-10-09; Decisions). Local ancestry is the
  only removal proof, and it proves that a branch adds nothing, not that its
  work began. Nor does a head equal to the merge-target SHA prove that the work
  never began, because a branch fast-forward merged into the target sits at the
  target's tip, so the gate reads the branch's reflog in every case. Its anchor
  is the last surviving entry whose old object is all zeros, as every entry that
  creates the branch has, whatever its message (`git fetch origin feat:f1`,
  `update-ref` and `push .` write no `branch:` message), or whose message begins
  `branch: Created from` or `branch: Reset to` (`worktree add -B`, `branch -f`
  and `checkout -B` write the second; R-15). An entry whose old object is all
  zeros is never a movement, and a movement is a later entry, or any entry when
  no anchor survives, whose old and new objects are non-zero and differ (a
  rename's are equal). A branch whose anchor survives with no movement after it,
  at the anchor's new object, is excluded as `unstarted-branch`, so a freshly
  created and published lane worktree, whose push adds no reflog entry, is never
  swept, nor one reset to the target's tip by `worktree add -B` or created there
  by `git fetch origin feat:f1`; a branch with a movement, at the target's tip
  or not, is merged and stays eligible. The reflog is a bounded filesystem read
  of `logs/refs/heads/<branch>` in the common directory, at most 64 KiB, counted
  in the filesystem budget and never a Git child, so the fit test is unchanged.
  One outcome rule decides the read (M3; R-12): a missing, empty (0 byte) or
  bound-reaching reflog, one whose surviving entries cannot decide, and one
  whose last entry's new object is not the head fail closed as
  `reflog-unavailable`, at the same gate position; any other error on the read
  is the row's `inspection-error`; a read not finished within the filesystem
  budget leaves the row unprobed (`inspection-incomplete`); and one that the
  work deadline cuts leaves it unprobed with `deadline-exceeded` (Brett Heap's
  ruling O-1 of 2026-10-22; Decisions, amendments). The gate applies in single
  mode too (M4).
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
  a manual remedy: `git worktree prune`, `git worktree repair`, unsetting
  `core.worktree` and `core.bare` in the repository's `config` or in a
  worktree's `config.worktree`, or removing that row by hand, as the cause fits;
  where any row's path could not be read, it leaves `git worktree prune` out and
  warns against it, as do the preview's next steps for `inspection-error` and
  `registration-mismatch` rows (design D18; lane openRepoProject-3's W87 M-1,
  the lead's R-307 and R-310, which Brett Heap confirmed on 2026-10-22,
  "R-307: yes; R-310: yes"). The recommendations of a stale worktree do the
  same where any row's path could not be read, and the `inspect-cap` remedy
  always, its rows past the cap never being read (design D18; lane
  openRepoProject-3's W86 NM-1, the lead's R-320, which Brett Heap ruled on
  2026-10-22, "R-320: yes"). Every one of those warnings, with the ceiling's
  third text, also names `git worktree remove` and `git gc` beside `git worktree
  prune` (design D18; lane openRepoProject-3's W91 MEDIUM-2 and W95, and W80
  L-6; Brett Heap's "R-324: yes" of 2026-10-22, the lead's R-343). `push` and
  `delete-branch` change in argument resolution (`BA:424-425`) and two refusals
  (MODIFIED `:39`, `:49`); with either, `--apply --json` stays refused with
  `invalid-arguments`, exit 2.
- **One mutation seam, `retire_worktree(plan, target)`.** Revalidate; spawn the
  non-force `git -c status.showUntrackedFiles=normal -c
  core.untrackedCache=false -c core.fsmonitor=false -c core.trustctime=true -c
  core.checkStat=default -c protocol.allow=never -c
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
  hand" where its `.git` file and registry entry both remain, and "inspect, then
  `git worktree prune` and delete `<path>` by hand" where either is gone, which
  Git's forced removal refuses, exit 128, while the path remains, though not
  once the path itself is gone (Brett Heap's ruling F-1 of 2026-10-22), but
  "inspect `<path>` by hand; its `.git` could not be read, so do not run `git
  worktree prune`, `git worktree remove` or `git gc` until it can" where the
  rescan cannot read its `.git` file, since `git worktree prune` deletes a live
  worktree's administrative directory when Git cannot stat its `.git` (the
  lead's R-284, which Brett Heap confirmed on 2026-10-22, "R-284: yes"); the
  reason `removal-ceiling` names the ceiling cause, and the run exits 1
  (Decisions).
- **Targeted revalidation under a narrow guarantee.** Each target is
  revalidated with at most six Git children, the sixth the reachability probe
  of `worktree-only-commits` (LQ-13), and seven in a repository whose
  `extensions.worktreeConfig` the plan read as true (LQ-11), three more, and
  three more in the final rescan, where the path of the repository's root or of
  its common directory holds a line feed (lane openRepoProject-5's RI-3), a
  manifest re-read, a `modules` check and the `operation-in-progress` listing
  (LQ-14), never the full report (`BA:677-719`), against recorded
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
  up to 300 s. `push` and `delete-branch` children stay unbounded as today:
  the push child runs by `execute` (`project:157-162`), as the push-child
  exception states, and the delete-branch child in its own process group,
  pinned. Caps of 128 worktree rows (256
  for the plain report, OQ-29) and 16 targets, and ignored-file bounds of 64,
  4,096 and 8 (`BA:721-814`). A cap or deadline hit is an incomplete plan
  (`inspect-cap`, `inspection-incomplete`, `deadline-exceeded`, with `omitted`)
  that blocks apply (preview exit 1). When more than 16 rows pass every gate
  before `deferred-target-cap`, the first 16 in canonical order go on to the
  gates after it and the rest are excluded `deferred-target-cap` with the
  next command; the plan stays complete, apply is allowed, and re-running drains
  the backlog 16 at a time, the fresh plan and revalidation unchanged; when
  every one of those 16 is then excluded by a gate after the cap, such as
  `contains-submodule`, no re-run reaches a deferred row, and the human report
  says why. The `target-cap`
  refusal is retired; the code survives only as `add-project-overview`'s
  limiting gate reason (Decisions). Plans and results report `probes` and
  `operations` as `{estimated, performed}`, a removal counted under `operations`
  and every other Git child under `probes`, once (`BA:816-830`). The caps were
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
  (`BA:585-652`) under `-c core.untrackedCache=false -c core.fsmonitor=false
  -c core.trustctime=true -c core.checkStat=default`, the last two by Brett
  Heap's ruling LQ-10 and on the hidden-state probe and the removal too (pins
  that also override `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`, which the
  scrub leaves), every Git child except the push child also under `-c
  protocol.allow=never` and the six per-protocol pins (`protocol.file`, `ssh`,
  `git`, `http`, `https` and `ext`, each `.allow=never`), with
  `GIT_ALLOW_PROTOCOL` in the scrub, so that a lazy fetch in a partial
  (promisor) clone fails locally and its row is `inspection-error` (R-23, R-25),
  and every Git child, the push child included, with `GIT_TRACE2`,
  `GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF` set to `0` and with `GIT_TRACE` and
  the thirteen `GIT_TRACE_*` names Git 2.36 to 2.43 read in the scrub, so that
  no Git child writes a trace file (Brett Heap's ruling Q9 B; Decisions),
  all parsed NUL-delimited, with the scrubbed environment of `BA:243-253` and
  those trace names, through a new bounded runner (Impact). A probe
  `project` stops at its record bound is complete, never `probe-failed`; after
  SIGKILL the reap waits at most the 2 s grace, then abandons the child and
  records `probe-timeout`; every exit path terminates the probe groups it
  started, and a running removal child is waited for, per V1 ("A started removal
  is never interrupted"); stderr is drained and capped. A Git child gets `min(5
  s, work_remaining)` under `clean`'s deadline, the push and delete-branch
  children excepted, and 15 s in `status`, `doctor` and `update`, which have
  none (Decisions). The ladder keeps its names, and its
  order but for one test: a row whose upstream was deleted is tested for local
  ancestry before `remote-gone`, so a merged one is `merged-removable` (or
  `merged-current`) and only an unmerged one is `remote-gone` (Brett Heap's
  ruling of 2026-10-09; Decisions). Its text changes for that and for the
  partial-removal note (MODIFIED `:25`), and it becomes a pure function over
  evidence (OQ-28). Git 2.36 is required as R6 scopes it. Before any Git child
  starts, `git --version` included, a `HOME`, `XDG_CONFIG_HOME`,
  `GIT_CONFIG_GLOBAL` or `GIT_CONFIG_SYSTEM` set to a non-empty value whose
  first byte is not `/` refuses `clean` with `relative-config-path`, exit 2,
  and `status`, `doctor` and `update` report it as they report a Git below the
  floor, a baseline behavior change (Brett Heap's ruling LQ-15; Decisions).
  The visible consequences are the baseline behavior changes of
  `BA:1200-1274`, less `BA:1255-1256`, with `BA:1238-1240` and `BA:1268-1274` narrowed (Decisions)
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
  and `core.fsmonitor` off, untracked files listed, ctime trusted and the
  default stat check (What Changes, seam; LQ-10).
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
    below it, R6, and its refusal of a relative configuration path before any
    Git child, `relative-config-path`, LQ-15); an unreadable path is one
    `inspection-error` row with
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
    Three additions; the rest stays. Push refuses a branch on its deleted
    upstream itself, whatever its row's class (`remote-gone` when unmerged;
    `merged-removable` or `merged-current` when merged, under Brett Heap's
    ruling), because it must be reviewed before it is republished
    (`project:545-555` would push to it), with refusal reason `remote-gone`,
    exit 2, and refuses with `inspection-incomplete`, `inspect-cap` or
    `deadline-exceeded`, exit 2, when its re-inspection is incomplete. Added
    scenario: WHEN push is requested for a branch whose upstream was deleted,
    THEN it refuses with `remote-gone` and runs no push. By the lead's R-147,
    a sentence names the refusals the baseline makes and this change keeps,
    each before the plan, with exit 2, no code and the baseline's message, the
    upstream mapping refusal's trigger widened by the lead's R-130, with the
    added scenario "Push refuses a branch it may not push"; that scenario
    leaves `review-required` out, since the evidence model gives no row that
    class and only an in-process test reaches it (lane openRepoProject-3's W26
    F-2, F-3).
  - MODIFIED (`:55`):
    `### Requirement: Clean can explicitly retire verified worktrees`.
    "remove one named linked worktree" (`:57`) becomes one named worktree or
    the `--all-safe` set, through `retire_worktree`, the gates
    (`unstarted-branch`, `operation-in-progress` and `worktree-only-commits`
    included) and the pinned
    removal command, stopping at
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
    `partially-removed`, the reason `removal-ceiling` either way, its recovery
    text naming `git worktree prune` and a deletion by hand once the `.git` file
    or the registry entry is gone (Brett Heap's ruling F-1), and instead warning
    against `git worktree prune`, `git worktree remove` and `git gc` where the
    `.git` file cannot be read, whatever the rescan finds of the registry entry
    (R-284, which Brett Heap confirmed on 2026-10-22, "R-284: yes", and R-324,
    "R-324: yes", the lead's R-343); after `project` and its child are killed
    with SIGKILL mid-deletion, the report shows the partial-removal note beside
    the `dirty` advice. By the lead's R-147, a sentence after `:59-61` names
    branch deletion's refusals, the default branch, a branch a present linked
    worktree holds, a branch the main worktree holds and a branch the plan's
    evidence does not show merged into the merge target, with the added scenario
    "Branch deletion refuses a branch it may not delete"; by the lead's R-248,
    the main worktree's refusal names detaching HEAD there, or checking out the
    merge target there, and then retrying (lane openRepoProject-3's W52 F-5).
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
    By Brett Heap's rulings LQ-14 and LQ-13 the gate order ends with
    `operation-in-progress` and `worktree-only-commits`, with the added
    scenarios "An operation in progress", "A squash merge that holds an
    autostash" (R-126) and "A commit held only by the worktree".
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
    (sparse checkouts included), `registration-mismatch` (an effective work
    tree that is not the registered path included, LQ-11),
    `unsupported-path-bytes`, `unstarted-branch`, `reflog-unavailable`,
    `operation-in-progress` (LQ-14), `worktree-only-commits` (LQ-13) and
    unreadable worktrees to the preserved states. Both scenarios (`:27-36`)
    stay.
  - MODIFIED (`:49`): `### Requirement: Cleanup revalidates destructive actions`.
    Removal revalidates by the targeted check against the recorded identity
    objects, and the effective work tree where the plan read it (LQ-11),
    refusing with `identity-changed`, `branch-changed`,
    `state-changed`, `contains-submodule`, `hidden-local-state`, or, for an
    operation in progress or a commit held only by the worktree that the
    re-read finds, with the added scenarios "An operation started after the
    plan" and "A worktree-only commit made after the plan",
    `operation-in-progress` (LQ-14) or `worktree-only-commits` (LQ-13); push
    and
    `delete-branch` keep the full re-inspection (`project:508-518`) and refuse
    with `inspection-incomplete`, `inspect-cap` or `deadline-exceeded`, exit
    2, when it is incomplete. The MUST is scoped to the revalidation
    immediately before each spawn; changes after it are the residual window
    the ADDED guarantee states, and Git's own non-force check is the last
    defense only on the pinned configuration (`status.showUntrackedFiles`,
    `core.untrackedCache`, `core.fsmonitor`, and `core.trustctime` and
    `core.checkStat` by LQ-10; the protocol pins on every Git
    child except the push child are no part of it). A value null in the plan and
    null at revalidation, as a deleted upstream's `upstream_oid`, `ahead` and
    `behind` are, is no difference, while a value that cannot be re-read is
    (Brett Heap's ruling of 2026-10-09; Decisions); a Git child or filesystem
    call that fails, or runs past its own budget while the deadline is not the
    limit, is `state-changed` whatever its step, and one that the work deadline
    cuts leaves the target `not-attempted` with `deadline-exceeded` (the lead's
    R-171 and R-208). The scenario (`:55-58`) stays; a worktree that becomes
    dirty after revalidation is refused by Git (`failed`, `git-refused`, exit
    128) and is still preserved (`BA:298`).
  - Untouched (`:9`, `current` keeps its baseline meaning):
    `### Requirement: Cleanup protects the process worktree`.
  - Untouched (`:38`, a push still uses the configured mapping):
    `### Requirement: Cleanup respects configured upstream mappings`.
  - ADDED:
    `### Requirement: Cleanup states a narrow guarantee and its residual window`.
    Concurrent writers outside the contract, no lock, the guarantee, the
    residual-window line, and the branch race; the guarantee and the line name
    worktree-only commits by LQ-13 and operations in progress by LQ-14.
- `project-command` (all ten at `7a9134b` accounted for; line numbers are at
  `da33d92`; at `7a9134b` `Inspect and diagnose`, `Explicit maintenance` and
  `Distribution and compatibility` sit 22 lines lower, their text unchanged):
  - MODIFIED (`:22`): `### Requirement: Inspect and diagnose`. Minimal text
    per R6: doctor's `error` check row for old or unusable Git, or for a
    relative configuration path (LQ-15), status's
    `inspection-error` marker on a root or leg dict in a field matching
    worktree rows (R7), and `present: false` for a directory with no `.git`.
    Doctor shows as an `error` check row, never `ok` (`:24-25`), a null that
    means "not established" (`present`, a `dirty` a failed probe left null,
    any `inspection-error` row), never one that means "none" (`upstream`,
    `ahead`, `behind` without an upstream, `merged_into_target` when detached;
    `BA:897-900`, `DI:781-785`), so a fresh project with no remote passes.
    "Missing leg" and the rest stay. Added scenario: WHEN doctor runs with no
    `git` on PATH, THEN it reports `git-unavailable` as an error row, exit 1.
  - MODIFIED (`:31`): `### Requirement: Explicit maintenance`. Two changes:
    `update --apply` for a project-modifying component (`shape`, `bench`)
    refuses whenever the root's or any child's `dirty` is not exactly
    `false`, as push already does (`project:541`; `project:863` and `:869`
    test truthiness, which `null` passes). Added scenario: WHEN a leg's
    status probe times out at 15 s, THEN `update --apply` refuses and the
    owner tool is never invoked. By Brett Heap's ruling LQ-12, every owner
    tool runs with the push child's scrub, so that it acts on the repository
    the check inspected, with the added scenario "Owner tools see the
    repository the check inspected".
  - ADDED:
    `### Requirement: Repository inspection requires Git 2.36 and shares one evidence model`.
    Its readers are named generically, "every subcommand that inspects a Git
    repository" (today `clean`, and `status`, `doctor` and `update` through
    `snapshot`, `project:681`, `:699`, `:789`, `:846`). It carries the
    evidence model: the version check (`BA:593`), R6's timing not stated as a
    rule for every reader; the configuration-path test before any Git child,
    `relative-config-path`, and its scenario "A relative configuration path in
    status, doctor and update" (Brett Heap's ruling LQ-15); the probe directory
    rule (`BA:554-583`); the identity rule, under which a linked worktree whose
    effective work tree is not its registered path disagrees with its
    registration, read where `extensions.worktreeConfig` is set, by a probe
    whose output is read as one path that may hold line feeds (the lead's R-287
    and R-291), with the scenario "A linked worktree whose work tree is
    redirected" (Brett Heap's ruling LQ-11), and whose administrative
    `commondir` must name the common directory, with the scenario "A commondir
    that names another repository" (R-125); the scrub
    with `GIT_OPTIONAL_LOCKS=0` (`BA:243-253`); NUL parsing; the combined
    probe, its pins and bounds (`BA:629-652`, `BA:793-814`), among them
    `core.trustctime=true` and `core.checkStat=default` on the status and
    hidden-state probes, with the scenario "An edit that keeps its size and
    restores its mtime" (Brett Heap's ruling LQ-10), and the `-c
    protocol.allow=never` pin and the six per-protocol pins on every Git child
    except the push child, with `GIT_ALLOW_PROTOCOL` in the scrub, against lazy
    fetches (R-23, R-25); `GIT_TRACE2`, `GIT_TRACE2_EVENT` and
    `GIT_TRACE2_PERF` at `0` on every Git child, the push child included, and
    the fourteen trace variables in the scrub, each by name, thirty-one names
    in all, against trace files (Brett Heap's ruling Q9 B);
    the 1 MiB cap on the manifest read that resolves a merge target, a larger
    manifest being `manifest-invalid`; the runner's outcomes (What Changes,
    evidence model); its every-exit-path termination rule, stated in its own
    words: the probe groups it started are killed in a `finally` on every exit
    path, and a running removal child is waited for, per V1, never signalled
    before the 300 s ceiling (M7); and `min(5 s, work_remaining)` per Git child
    under a deadline, the push and delete-branch children excepted, 15 s
    otherwise. `status`, `doctor` and `update` get no deadline or row cap; an
    unreadable or timed-out row shows as `inspection-error`. Non-Git children
    (docker, doctor validators;
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
  probes, under one deadline in `clean`. Git children other than the push
  child run through a new bounded runner, not the baseline `probe()` (a
  departure from `BA:1212-1213`): each is a `Popen` in its own process group
  (C4), with the environment scrubbed of `BA:243-253`'s variables and of the
  fourteen trace variables, and with the three trace2 variables set to `0`
  (Brett Heap's ruling Q9 B); its stdout is read as bytes and streamed, so a
  probe can stop at its record bound. The push child runs through `execute()`
  with the same scrub but for `GIT_ALLOW_PROTOCOL`, and the same three trace2
  variables at `0`, in `project`'s process group (the push-child exception).
  `probe()` stays for non-Git children. The owner tools that `update --apply`
  invokes run through `execute()` with the push child's scrub and nothing set
  (Brett Heap's ruling LQ-12). The runner's shape
  (clarifications N2) lets
  `add-project-overview` drive four children without forking it.
  The ladder becomes a pure function; `status`, `doctor` and `update` gain the
  Git version check (R6), and every subcommand that inspects a Git repository
  gains the configuration-path test before it (LQ-15). No new flag outside
  `clean`, no network, no new dependency.
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
  corrected. Install (README:17-19) states the Git 2.36 requirement, and that
  `HOME`, `XDG_CONFIG_HOME`, `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` must
  be absolute paths when set (LQ-15), and the exit-code line (README:194-196)
  gains `clean`'s 1 for an incomplete preview, 143 and 129, Git's own status
  passing through.
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
  this change, and re-aligned if this change moves before ratification. Its
  quotes of this change's status pins as the two older ones (its
  `specs/project-overview/spec.md:202-204` and `design.md:650-652` at
  `961c405`) are stale after Brett Heap's ruling LQ-10, and are
  `add-project-overview`'s to restate.
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

Each is a proposal decision. Those that PR #11 carried were ratified with its
merge by Brett Heap's word of 2026-10-09, "ratify, merge #11 and run the
runbook". This amendment adds others: the departures from packet decisions
below say which of their entries are which, the council's push-child exception
names its own standing, before Brett Heap, and of the amendments of ratified
text after the departures, the first group rests on his words of 2026-10-22 and
the second on the lead's rulings, waiting on his ratification of #19; every
other entry was carried by PR #11. OQ numbers are the lane's decision list.
Packet open decisions taken, each citing the packet text that leaves it open:

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

Departures from packet decisions, each citing the decision departed from. They
are of two kinds. The first eleven, from OQ-23 to local ancestry outranking a
deleted upstream, were ratified with the merge of PR #11, and the next seven,
from trace output to an operation in progress, carry Brett Heap's own rulings of
2026-10-21, each entry naming its ruling and any lane ruling it adds. The last
four, a revalidation read or child that the work deadline cuts, push's wider
upstream refusal, branch deletion's message for a branch the main worktree holds
and the line-feed exception to the revalidation and rescan bounds, were declared
by this amendment's own rounds on the lead's rulings and are not ratified, and
nor are the parts of four of the seven that the lead's rulings added: the
extension of LQ-15's test to `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` (R-102
(c) 3), the `commondir` check of LQ-11's registration (R-125), the branch
reflog's non-zero objects among LQ-13's negatives (R-124 (c), R-127), the drain
line's naming of the reasons of the gates after the cap (R-146) and the three
markers that LQ-14's gate gained (R-126) (lane openRepoProject-3's W70 LOW-5 and
W87 OBS-3). They take effect only when Brett Heap ratifies this amendment.

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
  floor to 2.40; the lead kept 2.36 and added the name to the scrub, because
  raising would exclude Debian 12's Git 2.39 for a one-name difference. The
  scrub held sixteen names then and seventeen with R-25's `GIT_ALLOW_PROTOCOL`,
  and holds thirty-one since Brett Heap's ruling Q9 B added the fourteen trace
  variables, which every release from 2.36.6 to 2.43.7 reads alike. Ratified
  with the merge of PR #11.
- **OQ-24, JSON compatibility** (`BA:949-953`; `HO:210`): one
  `schema_version: 1` envelope for every `clean --json`, not an "additive
  superset" (R7). Baseline keys keep their names and types, the scope the
  packet's phrase meant; `root`, the meaning of `ignored_files` and a `null`
  `present` are the listed baseline changes.
- **OQ-5, the target cap's refusal** (`BA:96-101`, `BA:1004`,
  `BA:1367-1371`), ratified with the merge of PR #11: retired for the
  deferral (What Changes), the council's survey having found about 20 such
  rows in Opensoft-Tenant. Rows a gate after the cap then excludes keep their
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
- **Trace output turned off on every Git child** (Brett Heap's ruling Q9 B of
  2026-10-21, given through lane openRepoProject-4's spec 005 clarify round in
  his words "yes, recommended for Q1-Q17", on option B of that round's Q9,
  `specs/005-project-overview/clarify-questions.md` at `acd8cef`; an addition
  to `BA:243-253`, whose scrub names no trace variable): Git honours trace
  targets, which append to files, so a read-only probe could still write a
  file that a caller's environment or the configuration names. Every Git
  child, the push child included, therefore runs with `GIT_TRACE2`,
  `GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF` set to `0`, which outrank the
  `trace2.*` targets of the system and global configuration, the only
  configuration from which Git reads them and one that no `-c` reaches; and
  the scrub gains `GIT_TRACE` and the thirteen `GIT_TRACE_*` names Git 2.36 to
  2.43 read, each by name (`GIT_TRACE_BARE`, `GIT_TRACE_CURL`,
  `GIT_TRACE_CURL_NO_DATA`, `GIT_TRACE_FSMONITOR`, `GIT_TRACE_PACKET`,
  `GIT_TRACE_PACKFILE`, `GIT_TRACE_PACK_ACCESS`, `GIT_TRACE_PERFORMANCE`,
  `GIT_TRACE_REDACT`, `GIT_TRACE_REFS`, `GIT_TRACE_SETUP`, `GIT_TRACE_SHALLOW`
  and `GIT_TRACE_WORKING_TREE_ENCODING`), thirty-one names in all, which
  `clean`, `status` and `doctor` share. The fourteen were read from the
  sources of every release from 2.36.6 to 2.43.7 and are the same in each; the
  other `GIT_TRACE2_*` names stay, since none opens a file while the three
  targets are off. The push child carries both, because trace output changes
  nothing about where a push reaches. The ruling's other half, which accepts a
  repository's filters and the configuration files themselves as residuals,
  belongs to `add-project-overview` (design D6, D11, Risks).
- **A relative configuration path refused before any Git child** (Brett
  Heap's ruling LQ-15 of 2026-10-21, in his words to lane openRepoProject-2,
  "LQ-15: yes, refuse relative HOME like #29", and in lane openRepoProject-3's
  session, "yes to all six recommendations, LQ-10 to LQ-15", on lane
  openRepoProject-3's recommendation "Yes: refuse such a value up front, the
  same way #29 now refuses relative gh config paths."; an addition to
  `BA:243-253` and `BA:593`, which test no configuration path): Git builds the
  paths of the user's and the system's configuration, and of its global ignore
  and attributes files, from `HOME`, `XDG_CONFIG_HOME`, `GIT_CONFIG_GLOBAL` and
  `GIT_CONFIG_SYSTEM` as they are spelled, so a relative value resolves inside
  the directory a Git child runs in, where files a repository holds would run a
  filter in every status probe, a hook in the removal and a command in the
  push child, or turn untracked work into ignored files that Git's own check
  passes over. Before any Git child starts, `git --version` included, `clean`,
  `status`, `doctor` and `update` therefore test `HOME` and `XDG_CONFIG_HOME`
  for a non-empty value whose first byte is not `/`, on its raw bytes. They
  test `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` the same way, the lead's
  extension, which Brett Heap may strike. `clean` refuses such a value with the
  new code `relative-config-path`, exit 2, in every mode, and `status`,
  `doctor` and `update` report it as they report a Git below the floor (R6),
  starting no Git child. A baseline behavior change: `a040790` runs every child
  under such a value (design D6, D11, D16, D18, Risks). The test binds
  `project overview` too, through the evidence model that
  `add-project-overview` adopts, so the overview starts no Git child under
  such a value; its code and exit status there belong to
  `add-project-overview`, since the ruling names only `clean`, `status`,
  `doctor` and `update`.
- **The stat pins** (Brett Heap's ruling LQ-10 of 2026-10-21, in lane
  openRepoProject-3's session, "yes to all six recommendations, LQ-10 to
  LQ-15", on lane openRepoProject-3's recommendation "Approve. It is stricter
  than the spec and only adds protection."; an addition to `BA:307-317` and
  to the council's pinned status configuration): Git compares a file's ctime only while both
  `core.trustctime` and `core.checkStat` keep their defaults, so under a
  repository's `core.trustctime=false` or `core.checkStat=minimal` an edit
  that keeps a file's size and restores its mtime is invisible to the status
  probe and to Git's own check, and the removal deletes it (lane
  openRepoProject-3's F1 H-3 at `2cf34d3`). Every status probe, the
  hidden-state probe and the removal therefore also pass `-c
  core.trustctime=true -c core.checkStat=default`, after `-c
  core.fsmonitor=false`, and like the other pins they outrank every
  configuration file. The hidden-state probe's two older pins, which design
  D11 gave it for uniformity, become a requirement with the two new ones
  (design D9, D11, Risks).
- **Owner tools see the repository the check inspected** (Brett Heap's
  ruling LQ-12 of 2026-10-21, in lane openRepoProject-3's session, "yes to all
  six recommendations, LQ-10 to LQ-15", on lane openRepoProject-3's
  recommendation "Approve. Stricter."; an addition, no packet text behind it,
  since `BA:243-253` scrubs Git children only): at `a040790` an owner tool
  gets the caller's environment (`project:157-162`), so the dirty check before
  `update --apply`, which runs under the scrub, and the owner tool could see
  different repositories through a caller's `GIT_DIR`, `GIT_WORK_TREE` or
  `GIT_INDEX_FILE` (lane openRepoProject-3's F5 M-3 at `2cf34d3`). Every owner
  tool that `update --apply` invokes therefore runs with the push child's
  scrub, the thirty-one names but `GIT_ALLOW_PROTOCOL` removed, and with
  nothing set: it is not a Git child, so it takes no `-c` pin, no
  `GIT_OPTIONAL_LOCKS` and no trace2 variable, and a caller's
  `GIT_ALLOW_PROTOCOL` still binds any Git it runs, as it binds the push
  child, because only the protocol pins that the tool lacks would replace it
  (design D6, D16).
- **A redirected work tree is a registration mismatch** (Brett Heap's ruling
  LQ-11 of 2026-10-21, in lane openRepoProject-3's session, "yes to all six
  recommendations, LQ-10 to LQ-15", on lane openRepoProject-3's
  recommendation "Approve. Stricter, protective."; an addition to the two-way
  registration of `BA:203-235`, and a departure from `BA:615`'s F of at most 7
  and `BA:679`'s at most five revalidation children): where a repository sets
  `extensions.worktreeConfig`, Git applies a `core.worktree` or `core.bare`
  from a linked worktree's `config.worktree`, or from the repository's own
  `config`, to that worktree, so every probe of a row whose registration
  agrees can read another directory's tree while Git's non-force removal,
  whose own check reads the registered path, deletes the registered directory
  and its ignored files (lane openRepoProject-5's reader RB, its `e7`). A
  linked row whose effective work tree is not its registered path therefore
  disagrees with its registration and is `registration-mismatch`: the
  repository's `extensions.worktreeConfig` is read once per common directory,
  and where it is true each linked row's effective work tree is read by `git
  rev-parse --path-format=absolute --show-toplevel` in it, before its status
  probe, and again at revalidation; the registration also requires the
  administrative `commondir` to name the common directory, so that row 4c
  reads the `config` Git reads (lane openRepoProject-3's W9 M2, R-125). Row
  4c, the per-row probe and the `commondir` read reach `project overview`
  through the evidence model that `add-project-overview` adopts, as Q9 B's
  pins do; the overview's probe count and its scenario "One probe set per
  repository" are `add-project-overview`'s to restate (design D6, D7, D14,
  Risks).
- **A commit held only by the worktree keeps it** (Brett Heap's ruling LQ-13
  of 2026-10-21, in lane openRepoProject-3's session, "yes to all six
  recommendations, LQ-10 to LQ-15", on lane openRepoProject-3's
  recommendation "Yes, add a protection. Leave the worktree in place if any
  such commit is unreachable from every branch, tag and remote ref. This needs
  an amendment to change 1."; extends the gates of `BA:113-165` and the
  revalidation of `BA:677-707`): `git worktree remove` deletes the worktree's
  administrative directory with its `logs/HEAD` and its `refs/worktree/`, so a
  commit that only they hold is left to garbage collection (lane
  openRepoProject-3's F1 H-1 at `2cf34d3`). A new last gate,
  `worktree-only-commits`, reads `logs/HEAD` (at most 64 KiB) and runs one
  `rev-list` in the worktree, the candidates being the reflog's objects and
  `refs/worktree/`, and the negatives every branch, tag and remote-tracking ref
  and the non-zero objects that the branch's own reflog names, which survives
  the removal, so that an amend, reset or rebase of the branch is not taken for
  lost work, a part that the lead's rulings added (R-124 (c), R-127). A printed
  commit, or a `logs/HEAD` over its 64 KiB bound or with a line that does not
  parse, excludes the row, and a read or child that fails or times out is
  `inspection-error`, as every other evidence read is (`BA:188-192`,
  `BA:642-644`; the lead's R-124); revalidation runs the check again, so a
  commit made after the plan refuses the target with the same reason (lane
  openRepoProject-3's reader RB, R-107), and the residual-window line names such
  a commit made after that check. The drain line's naming of the reasons of the
  gates after the cap, which LQ-13 and LQ-14 added to, is a second part that the
  lead's rulings added (R-146; W21 L-f). No JSON field is added (design D7, D12,
  D14, D18, D21, Risks).
- **An operation in progress keeps the worktree** (Brett Heap's ruling LQ-14
  of 2026-10-21, in lane openRepoProject-3's session, "yes to all six
  recommendations, LQ-10 to LQ-15", on lane openRepoProject-3's
  recommendation "Yes, add a protection. Never remove a worktree with an
  operation in progress. This also needs an amendment to change 1."; extends
  the gates of `BA:113-165` and the revalidation of `BA:677-707`): Git keeps
  the state of a merge and its autostash, a notes merge, a cherry-pick or
  revert, an `am`, a rebase or a bisect in the worktree's administrative
  directory, so one that stopped with the
  index and tree equal to the branch head reads clean and the removal deletes
  its state (lane openRepoProject-3's F1 H-2 at `2cf34d3`). A new gate,
  `operation-in-progress`, after `hidden-local-state` and before
  `worktree-only-commits`, lists that directory once and excludes the row when
  it holds `MERGE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `BISECT_LOG`,
  `BISECT_START`, `rebase-apply`, `rebase-merge` or `sequencer`, the markers
  of Git's own state detection, or `MERGE_AUTOSTASH`, `NOTES_MERGE_PARTIAL` or
  `NOTES_MERGE_REF`, which a held autostash and a stopped notes merge leave
  (lane openRepoProject-3's W14 M1, R-126), all read in its sources at 2.36.6
  and 2.43.7; a listing that fails is `inspection-error` (R-124). Revalidation
  lists it again with no new Git child, so an operation started after the plan
  refuses the target with the same reason (lane openRepoProject-3's reader RB,
  R-107), and the residual-window line names an operation started after that
  check. No JSON field is added (design D7, D18, D21, D22, Risks).
- **A revalidation read or child that the work deadline cuts is no difference**
  (the lead's R-124 (a), R-171, R-187 and R-190; a departure from `BA:271-272`,
  "A value that cannot be re-read, including a filesystem call that times out,
  counts as a mismatch", a mismatch refusing the target with exit 2,
  `BA:270-271`): at revalidation a Git child or filesystem call that the work
  deadline cuts counts as no difference, and the target and every later one are
  `not-attempted` with `deadline-exceeded`, as when less than the 5 s removal
  floor remains (`BA:392-394`, `BA:437-441`), and the run exits 1; one that
  fails, or runs past its own budget while the deadline is not the limit, still
  counts as a difference, `state-changed` (the lead's R-208). A deadline that
  runs out establishes no difference in the target, so the target is left
  `not-attempted`, as every target the deadline stops is, not refused
  (Capabilities, review-safety `:49`; design D7, D21, D22; the delta `Cleanup
  revalidates destructive actions`).
- **Push refuses a wider set of upstream mappings** (the lead's R-130, on lane
  openRepoProject-3's F2 H-2; a departure from `BA:424-425`, "`push` and
  `delete-branch` keep their behavior apart from argument resolution"): push
  refuses a configured upstream that is not one remote other than `.` with one
  branch under `refs/heads/`, where `a040790` refused only an upstream whose
  short name lacked a remote or a branch part; the trigger is wider and the
  message is the baseline's. It only refuses more, so it allows no push that
  `a040790` refused (Capabilities `:39`; the delta `Clean can explicitly push
  safe feature branches`).
- **Branch deletion's message for a branch the main worktree holds** (the lead's
  R-248, on lane openRepoProject-3's W52 F-5 and lane openRepoProject-5's RI-4;
  a departure from `BA:424-425`, "`push` and `delete-branch` keep their behavior
  apart from argument resolution"): branch deletion refuses a branch B that the
  main worktree holds with `Branch B is checked out in the main worktree; detach
  HEAD there, or check out T there, then retry.`, T the merge target, where the
  baseline prints one message for any present holder, the main worktree
  included, `Remove the linked worktree first; branch deletion is a separate
  action.` (`project:730` at `15504f1`, `project:582` at `a040790`), which names
  a removal that Git refuses for the main worktree, `git worktree remove` of it
  exiting 128. The trigger, the exit status and every other message are the
  baseline's; only that message changes, so it allows no deletion that the
  baseline refused (Capabilities `:55`; design D18; the delta `Clean can
  explicitly retire verified worktrees` and its scenario "Branch deletion
  refuses a branch it may not delete").
- **The line-feed exception to the revalidation and rescan bounds** (the lead's
  R-259, on lane openRepoProject-5's RI-3; a departure from `BA:679`,
  "Revalidating one target spawns at most five children", `BA:725-727`, "an
  `--apply` run spawns at most F + W + E children to plan, 5T to revalidate, 3
  for the final rescan, and T removals", and `BA:743`, the cost table's row
  "Final rescan | 3 | 0.3 s | 0.45 s"): where the path of the repository's root
  or of its common directory holds a line feed, the identity probe, which prints
  one value per line and has no NUL form, is read one option per child, four
  children in place of one, so that revalidating one target spawns at most nine
  Git children, ten where the plan read `extensions.worktreeConfig` as true,
  against the packet's five, which LQ-13 and LQ-11 made six and seven, and the
  final rescan at most six, against the packet's three; the plan's
  `probes.estimated` counts the extra children, three per target and three for
  the final rescan. It widens the count change that LQ-11's entry declares, on
  the lead's ruling rather than Brett Heap's, and lane openRepoProject-3's W70
  measured nine, ten and six on Git 2.43.0 and 2.36.6 (its M-3; What Changes,
  revalidation; design D6, D7, D14; the deltas `Clean bounds its Git work and
  reports omitted work` and `Cleanup revalidates destructive actions`).

Amendments of ratified text, each replacing a sentence that the merge of PR #11
ratified, on Brett Heap's word of 2026-10-22, "F-2: yes; F-1: prune-then-delete;
O-1: deadline-exceeded" (the lead's R-263), and on his "R-284: yes" (the lead's
R-290), "R-307: yes; R-310: yes" (the lead's R-319), "R-320: yes" (the lead's
R-321) and "R-324: yes" (the lead's R-343) of the same day:

- **A locked worktree's recovery text** (lane openRepoProject-3's W52 F-2;
  amends `0050f3e` pcl:135-138): a locked linked worktree whose status records
  are all deletions of tracked files shows the recovery text "inspect, unlock
  it, then `git worktree remove --force <path>` by hand", since `git worktree
  remove --force` refuses a locked worktree; every other such row keeps the
  ratified text; a `partially-removed` ceiling target is no report row and is
  shown one of the three ceiling texts below, never this one, the third where
  the rescan cannot read its `.git` file, locked or not (the delta `Clean
  classifies preservation and cleanup actions` and its scenario "Only
  tracked-file deletions"; design D4, D18; for the ceiling target, lane
  openRepoProject-3's W80 M-1 and W87 LOW-3 and the lead's R-294).
- **The ceiling's recovery text** (W52 F-1; amends `0050f3e` pcl:253-256 and
  pcl:922-926): a `partially-removed` target shows "inspect, then `git worktree
  remove --force <path>` by hand" only where the rescan finds both its `.git`
  file and its registry entry present, and otherwise "inspect, then `git
  worktree prune` and delete `<path>` by hand", since Git deletes the work tree
  before the administrative directory and refuses the forced removal once the
  `.git` file or the entry is gone while the path remains, exit 128 on Git
  2.43.0 and 2.36.6, and accepts it once the path itself is gone (W70 LOW-1);
  the rescan reads the `.git` file by one `lstat`, a filesystem call, so it
  still spawns at most three Git children, and where that read fails or is cut
  the third text below takes precedence over both, whatever the rescan finds of
  the registry entry (lane openRepoProject-3's W80 L-1; the deltas `Clean can
  explicitly retire verified worktrees`, with its scenario "A removal past the
  hard ceiling", and `Clean records a reconcilable result for every removal
  target`; design D9, D18).
- **The ceiling's recovery text where the `.git` file cannot be read** (lane
  openRepoProject-3's W73 M-1; the lead's R-284, which refines how F-1 applies
  to a read that fails, and which Brett Heap confirmed on 2026-10-22, "R-284:
  yes" (the lead's R-290); amends `0050f3e` pcl:253-256 and pcl:922-926 with
  F-1): a `partially-removed` target whose `.git` file the rescan cannot read,
  its `lstat` failing other than for the file's absence or cut at its budget,
  shows, whatever the rescan finds of its registry entry and whether or not the
  worktree is locked, "inspect `<path>` by hand; its `.git` could not be read,
  so do not run `git worktree prune`, `git worktree remove` or `git gc` until it
  can", since `git worktree prune` deletes a live worktree's administrative
  directory where Git cannot stat its `.git`, and so, once it is unlocked, does
  `git worktree remove`, with or without `--force` (round (i); for the lock,
  lane openRepoProject-3's W80 M-1 and the lead's R-294, by R-284's letter, "A
  `.git` read that fails or is cut gets a third note", though a ceiling target
  is shown no locked text, which is a report row's own, and a locked one whose
  `.git` file and registry entry the rescan reads present is shown the first
  text, whose forced removal Git refuses while it is locked, so that it fails
  safe (W87 LOW-3); the deltas `Clean can explicitly retire verified worktrees`,
  with an AND clause in its scenario "A removal past the hard ceiling", and
  `Clean records a reconcilable result for every removal target`; What Changes;
  Capabilities `:55`; design D4, D9, D18). The warning that closes the third
  text names `git worktree prune`, `git worktree remove` and `git gc`, as his
  "R-324: yes" (the lead's R-343) extended it, in the last entry of this group.
- **Gate 7's read that the deadline cuts** (lane openRepoProject-5's O-1;
  amends `0050f3e` pcl:606-608): a branch reflog read that the work deadline
  cuts records `deadline-exceeded` and leaves the row unprobed and the plan
  incomplete with `deadline-exceeded`, whose remedy names no repair, as the
  `worktree-only-commits` gate's reads do, where the ratified sentence made it
  `inspection-incomplete`; a read not finished within the filesystem budget
  while the deadline is not the limit still leaves the plan incomplete with
  `inspection-incomplete` (the delta `Clean previews and applies a batch of
  eligible worktree removals in one repository`; design D10).
- **No prune advice where a row's path could not be read** (lane
  openRepoProject-3's W87 M-1; the lead's R-307 and R-310; amends `0050f3e`
  design:757-758, the next step of `registration-mismatch` and
  `inspection-error`, "review, then git worktree repair or git worktree prune,
  or remove the row by hand", and design:775-777, the remedy of
  `inspection-incomplete`, "repair or remove the inspection-error rows first:
  git worktree repair, git worktree prune, or remove the row by hand after
  review", and qualifies pcl:649-651, "Every refusal that blocks a plan, in
  either mode, SHALL name a manual remedy: `git worktree prune`, `git worktree
  repair`, or removing the offending row by hand, as the cause fits."): where
  Git cannot stat a worktree's path, as under `EACCES` on a directory above it,
  `git worktree prune` deletes that live worktree's administrative directory,
  its index, `HEAD`, per-worktree refs and reflog with it, on Git 2.43.0 and
  2.36.6, the hazard of the lead's R-284 met one stage earlier, at planning,
  where R-284 met it after a removal; yet both ratified sentences name it for a
  row whose planning `lstat` of its path failed other than for the path's
  absence, or was cut at its budget, a row with `present: null`, an `os-error`
  and classification `inspection-error`, and feature 004 at `3bc1d68` printed
  that remedy for such a row in report mode. Such a row's next step is now
  "inspect the row by hand; its path could not be read, so do not run git
  worktree prune, git worktree remove or git gc until it can", in place of the
  ratified words, and the plan's `inspection-incomplete` remedy is "repair or
  remove the inspection-error rows first: git worktree repair, or remove the row
  by hand after review; a row's path could not be read, so do not run git
  worktree prune, git worktree remove or git gc until it can" or, where any row
  it counts is excluded as `registration-mismatch`, "repair or remove the
  inspection-error rows first: git worktree repair, unset core.worktree and
  core.bare in the repository's config or in a worktree's config.worktree, or
  remove the row by hand after review; a row's path could not be read, so do not
  run git worktree prune, git worktree remove or git gc until it can", in place
  of the ratified remedy and round (h)'s variant of it, which name `git worktree
  prune` too. The unread forms take precedence wherever any row of the plan has
  such a path, a row whose `lstat` the deadline stopped included, since omitting
  prune advice never harms. Nor is the hazard confined to that row: `git
  worktree prune` acts on the whole repository, so a prune run for another row's
  sake deletes the unread row's directory too (checked on Git 2.43.0), and by
  the lead's R-310, while any row of the plan has such a path, the next step of
  every other `inspection-error` row is "review, then git worktree repair, or
  remove the row by hand; a row's path could not be read, so do not run git
  worktree prune, git worktree remove or git gc until it can" and that of every
  `registration-mismatch` row is "review, then git worktree repair, unset
  core.worktree and core.bare in the repository's config, or in that worktree's
  config.worktree, or remove the row by hand; a row's path could not be read, so
  do not run git worktree prune, git worktree remove or git gc until it can",
  each the next step as it stood, round (g)'s for `registration-mismatch`, with
  " or git worktree prune" removed and the warning appended. The delta states
  the rule as an AND clause of its scenario "An unreadable worktree is one row",
  the "as the cause fits" of pcl:649-651, now pcl:836-840, governing it, so that
  the scenario counts stay 71, 22 and 24 (the delta `Clean reports local
  worktree state`; What Changes; design D18). Brett Heap confirmed the five
  texts, three next steps and two remedies on 2026-10-22, in his words "R-307:
  yes; R-310: yes" (the lead's R-319). The warning that closes each of the five
  names `git worktree prune`, `git worktree remove` and `git gc`, as his "R-324:
  yes" (the lead's R-343) extended it, in the last entry of this group.
- **No prune advice in the stale recommendations or the cap remedy** (lane
  openRepoProject-3's W86 NM-1, through lane openRepoProject-4; the lead's
  R-320; amends `0050f3e` design:777-779, the remedy of `inspect-cap`, "N rows
  exceed the row cap of M; remove worktrees explicitly, or prune stale entries
  by hand", and design:759-760, "every other class its recommendation", which
  carries the ladder's recommendation for a `stale-worktree` row, "Review and
  prune stale worktree metadata manually." (`project:568` at `0050f3e`)): `git
  worktree prune`, run for a stale entry's sake, deletes the administrative
  directory of a worktree whose path Git cannot stat too (W86 NM-1, on Git
  2.43.0 and 2.36.6), the hazard of R-307 and R-310 met at two more texts, yet
  both ratified sentences advise it beside such a row. Where any row of the same
  plan has a path that could not be read, a row whose planning `lstat` failed
  other than for the path's absence, or was cut at its budget, a row whose
  `lstat` the deadline stopped included, so that its `present` is null, a
  `stale-worktree` row's recommendation is "Review and prune stale worktree
  metadata manually; a row's path could not be read, so do not run git worktree
  prune, git worktree remove or git gc until it can." and a locked one's, which
  only the report's row recommendation carries, in the human report and in
  `--json`, since the preview excludes a locked stale row as `locked-worktree`,
  "unlock it yourself if it should go", the form that lane openRepoProject-3's
  W52 F-10 gave feature 004 and this change did not state, is "Review, unlock
  it, then prune stale worktree metadata manually; a row's path could not be
  read, so do not run git worktree prune, git worktree remove or git gc until it
  can."; with no such row both print unchanged. The `inspect-cap` remedy, whose
  rows past the cap are never read, is always "{N} rows exceed the row cap of
  {M}; remove worktrees explicitly, or prune stale entries by hand; if a
  worktree's path cannot be read, do not run git worktree prune, git worktree
  remove or git gc until it can" in place of the ratified remedy. Design D18
  states the three texts beside the sentences they qualify, and the delta states
  the cap remedy as an AND clause of its scenario "Row cap and planning
  failures", so that the scenario counts stay 71, 22 and 24 (the delta `Clean
  bounds its Git work and reports omitted work`; What Changes; design D18); no
  delta lists the stale recommendation, the baseline report's text, so none
  states the first two. Brett Heap ruled all three on 2026-10-22, in his words
  "R-320: yes" (the lead's R-321). The warning that closes each of the three
  names `git worktree prune`, `git worktree remove` and `git gc`, as his "R-324:
  yes" (the lead's R-343) extended it, in the last entry of this group.
- **The warnings also name `git worktree remove` and `git gc`** (lane
  openRepoProject-3's W91 MEDIUM-2 and W95, and its W80 L-6 and E6; the lead's
  R-324 and R-343; amends the third ceiling text above and the eight texts of
  the two entries before this one, which replace `0050f3e` pcl:253-256,
  pcl:922-926, design:757-758, design:775-779 and design:759-760): `git worktree
  prune` is not the only command that deletes the administrative directory of a
  worktree whose path Git cannot stat. `git worktree remove`, with or without
  `--force`, deletes it on Git 2.43.0 and 2.36.6 (W91 MEDIUM-2; W95), and so
  does `git gc`, whose automatic worktree prune deletes it once the directory's
  index is older than `gc.worktreePruneExpire`, three months by default (W80
  L-6, E6), yet each of the nine warnings named `git worktree prune` alone. The
  lead put one question to Brett Heap in R-324, and he ruled on 2026-10-22, in
  his words "R-324: yes" (the lead's R-343), that every no-prune warning
  extends: the third ceiling text, the five texts of the first of those two
  entries and the two stale recommendations of the second now end "so do not run
  git worktree prune, git worktree remove or git gc until it can", and the cap
  remedy now reads "if a worktree's path cannot be read, do not run git worktree
  prune, git worktree remove or git gc until it can", every other word of the
  nine texts staying; where the third text stands with its commands in code
  spans, each of the three has its own. Design D18 and the deltas carry the
  extended texts at every site that quotes them (the deltas `Clean reports local
  worktree state`, in its scenario "An unreadable worktree is one row"; `Clean
  can explicitly retire verified worktrees`, in its requirement and in its
  scenario "A removal past the hard ceiling"; `Clean records a reconcilable
  result for every removal target`, in its requirement; and `Clean bounds its
  Git work and reports omitted work`, in its scenario "Row cap and planning
  failures"; What Changes; design D18), and the reasons that they give for `git
  worktree prune` stand. The sentence of design D18 and of round (k)'s entry
  that said naming `git worktree remove` or `git gc` in the third text waits on
  his word (W80 M-1, second part, with L-6) is closed by the same words. F-1's
  (b), which can print in single mode beside a row whose path could not be read,
  stays open in design Open Questions as worded.

Amendments of ratified text on lane rulings, waiting on his ratification of #19:
each replaces a sentence that the merge of PR #11 ratified, on a ruling of the
lead's rather than his word, and takes effect only when Brett Heap ratifies this
amendment (lane openRepoProject-3's W70 M-1, the lead's R-285):

- **The line-feed exception to the bounds** (lane openRepoProject-5's RI-3; the
  lead's R-259; amends `0050f3e` pcl:825-826, "Revalidating one target SHALL
  spawn at most five Git children and never recompute the full report, and the
  final rescan at most three.", and rs:69-70, "at most five Git children"):
  Brett Heap's rulings LQ-13 and LQ-11 made the five six and seven (departures),
  and RI-3 adds that where the path of the repository's root or of its common
  directory holds a line feed, a revalidation spawns at most nine Git children,
  ten where the plan read `extensions.worktreeConfig` as true, and the final
  rescan at most six, which the plan's `probes.estimated` counts, since ratified
  design D6 (`0050f3e` design:298-302) already read the identity probe again one
  child per option where a value holds a line feed (the deltas `Clean bounds its
  Git work and reports omitted work` and `Cleanup revalidates destructive
  actions`; What Changes, revalidation; departures, the line-feed exception;
  design D7, D14).
- **The next steps for a worktree that holds a submodule** (lane
  openRepoProject-3's W52 F-7 and F-8; the lead's R-248 and R-252, and R-253 for
  W59's G-4; amends `0050f3e` design:753-757, design:744-746, design:942-947 and
  proposal:84-91): the ratified remedies of `unstarted-branch` and
  `reflog-unavailable`, each ending "review, then git worktree remove yourself",
  end "review, then git worktree remove yourself (--force if it holds a
  submodule)", since both are gate 7, ahead of `contains-submodule`, and Git
  refuses a plain `git worktree remove` of a worktree that holds a submodule
  with exit 128; `contains-submodule`'s, "review, then remove the worktree
  yourself", which the ratified text gave it with `hidden-local-state`, is
  "review, then git worktree remove --force yourself"; and the non-drain line's
  "review those worktrees, then remove them yourself" gains "(--force for any
  that holds a submodule)" (What Changes, first bullet; design D18 and the
  Migration Plan).
- **The cap's re-run** (lane openRepoProject-3's W31 L-7; the lead's R-187 and
  R-190, in `2e819ad`; amends `0050f3e` pcl:810-811): the ratified "re-running
  SHALL take the next 16, each run building its own fresh plan and revalidating
  each of its targets" reads "re-running SHALL take the next 16 as the rows
  ahead of them are removed or excluded by a gate before the cap, each run
  building its own fresh plan and revalidating each of its targets, so that a
  run that removes none of its 16, as when the deadline leaves every target
  `not-attempted`, leaves its 16 to the next run" (the delta `Clean bounds its
  Git work and reports omitted work`).
- **The count split** (`cecb4fc`, which names no ruling, a reading of
  `BA:816-830`; amends `0050f3e` pcl:819-820, pcl:868 and proposal:258-259): the
  ratified "every Git child counted" reads "every Git child counted once, a
  removal under `operations` and every other child under `probes`", What
  Changes, bounded work, says the same, and in the scenario "Bounded
  revalidation work" the ratified "`probes.performed` equals the wrapper's
  count" gains "of children other than the three removals, and its
  `operations.performed` is 3" (the delta `Clean bounds its Git work and reports
  omitted work`).
- **The identity probe's line count** (lane openRepoProject-4's finding, through
  the lead, in round (i)'s `b60f6ac`, which names no ruling; lane
  openRepoProject-3's W80 M-3; amends `0050f3e` design:298-301, "Two lines mean
  a plain checkout and three a submodule checkout; a value containing a line
  feed makes the count exceed what was asked, and the probe is then repeated as
  one child per option, counted, rather than guessed at."): three lines mean a
  submodule checkout or a line feed in a path, which the count cannot tell
  apart, so on any count but two the probe is repeated one option per child, as
  feature 004's `identity_probe()` does; every submodule checkout's probe is
  therefore repeated, three more children, and a plain checkout whose one value
  holds a line feed is no longer read as a submodule checkout (design D6).

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
- **Lazy fetches pinned off, the push child excepted** (R-23, R-25; an addition
  to `BA:243-253` and `BA:307-317`, which pin no protocol policy): Git 2.43 has
  no `GIT_NO_LAZY_FETCH`, so a read-only probe in a partial (promisor) clone can
  fetch a missing object from the network. `-c protocol.allow=never` makes the
  fetch fail locally and the row `inspection-error`, but it is only the default
  policy: a `protocol.<name>.allow` setting in the repository's configuration
  outranks it for that protocol, and so does `GIT_ALLOW_PROTOCOL` in the
  caller's environment. Every Git child except the push child therefore also
  pins `-c protocol.file.allow=never -c protocol.ssh.allow=never -c
  protocol.git.allow=never -c protocol.http.allow=never -c
  protocol.https.allow=never -c protocol.ext.allow=never`, which outrank every
  configuration file, and the scrub removes `GIT_ALLOW_PROTOCOL`, which no `-c`
  outranks, seventeen names in all then and thirty-one since Brett Heap's ruling
  Q9 B (departures). Accepted residual: a remote-helper protocol
  of another name with its own `allow=always` in the repository's configuration
  could still fetch; the probe then succeeds rather than fails, and no unsafe
  removal follows (design Context, D11, Risks). The push-child exception (R-23,
  R-25 and R-28; before Brett Heap; Open Questions, the push-child exception;
  lane 2's LQ-3): the push child of `clean --action push` reaches a remote,
  which the pins would refuse over every protocol, so it keeps the scrub but for
  `GIT_ALLOW_PROTOCOL`, the other thirty names removed and a caller's
  `GIT_ALLOW_PROTOCOL` kept (R-28), runs unbounded in `project`'s process group
  as `execute` runs it today, carries none of the pins, and no evidence comes
  from it. Its process group departs from `BA:1238-1240`, by which every Git
  child runs in its own process group, and from `BA:465-468`, by which probe
  children run in their own process groups, so that a terminal Ctrl-C reaches
  only `project`, which then sends SIGTERM to the group of a child in flight.
  Accepted residual of the exception: the push child follows the configuration
  as `git push` would, an `ext::` origin that `protocol.ext.allow=always` allows
  included, and takes no `-c` from the caller's environment (design Risks).
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
  (3.2+) for each child's own process group (the push child excepted), never
  `preexec_fn`, and runs abandonable filesystem calls on daemon
  `threading.Thread`s, not a `concurrent.futures` pool.

## Open Questions

- **Squash-merged branches.** A squash merge never puts the branch tip into
  the target's ancestry (`BA:195-199`), and this repository's `main` has no
  merge commit, so in squash-merging repositories the MVP selects little.
  Before Brett Heap, recommending a local patch-equivalence proof (`git
  cherry` or patch IDs against the target) as a follow-on change.
- **The push-child exception.** The pins on every Git child (R-23, R-25) refuse
  a push over every protocol (a local-path `origin` fails with `fatal: transport
  'file' not allowed`, exit 128), yet this change keeps the explicit push of
  `clean --action push`, whose child must reach its remote. Before Brett Heap,
  recommending that the change be amended in place before its archive, as this
  draft does, so that the push child is the one Git child without the pins; the
  alternative is a follow-up change after the archive, as
  `fix-parent-obstacle-wording` followed `prefer-triad-in-project-new`, which
  costs a second archive and leaves the archived spec wrong in between.
- **LQ-20, the fit where `extensions.worktreeConfig` is true.** RESOLVED on
  2026-10-22: Brett Heap chose step (i), in his words to lane openRepoProject-2,
  "LQ-20: go with (i), measure first" (the lead's R-236). The two probes were
  measured on task 2.1's protocol, in the same container and at a 1-minute load
  of 15 to 21 on 32 threads: LQ-11's work-tree probe at 5.8 ms warm, 8.7 ms with
  the margin, and LQ-13's `rev-list` at 106.9 ms warm, 160.3 ms with the margin,
  its walk covering a whole history of 9,940 commits (design D14; `tasks.md`
  2.1). The cap test, rerun on those costs, passes on the measured basis: at 128
  rows and 16 targets where `extensions.worktreeConfig` is true, all 16 removals
  fit, the 16th spawning at 30.0 s with 20.0 s left (37.7 s with 20,000-file
  removals). Options (a) to (d) are therefore not needed, and none is taken; the
  deltas stand as written. The question as it stood before the ruling follows,
  kept as the record of what was costed; its measured basis is at the stand-ins
  that step (i) replaced. LQ-11's effective-work-tree probe runs for every
  linked row at plan time, and the question's first step is the basis (design
  D14, Risks; the lead's R-178, R-190, R-207 and R-208). The cap test is D5's,
  at task 2.1's measured costs and its 10,000-file removal, but task 2.1
  measured neither that probe nor LQ-13's `rev-list`. At D14's flat 150 ms per
  child a 128-row `--all-safe --apply` in such a repository reaches its first
  removal at 45.3 s, past the 45 s spawn limit (the 50 s work deadline less the
  5 s removal floor), and removes nothing, which is safe. At the measured costs,
  with the identity probe's 19.7 ms and the full ref listing's 359.7 ms standing
  in for the two unmeasured probes, all 16 removals fit (15 with 20,000-file
  removals), the 16th only while the work-tree probe costs at most about 69 ms
  with the margin and the `rev-list` about 581 ms or less, each with the other
  at its stand-in. On the mixed basis, the measured costs plus 150 ms for each
  child added since, 11 fit. Before Brett Heap, with no recommendation here:
  first, (i) measure those two probes on task 2.1's protocol and rerun the cap
  test, or (ii) decide which basis the cap test uses, the measured one as D5 was
  ratified, the mixed one, or BA's flat 150 ms, which would change D5 and fails
  the case at once, so that an option has to be chosen with it; then, only if
  the case fails on that basis, one of these, each with its result at 128 rows
  on each basis:
  - (a) accept that worst case (not taken):
    - 150 ms: no removal on this run or any re-run, since a re-run builds the
      same plan, so a re-run does not continue there; from 127 rows, one removal
      a run at first; a `--worktree` removal still fits;
    - measured: 16 a run;
    - mixed: 11, then 13, then 16 a run;
  - (b) bound the plan-time work-tree probe to the selected targets, at most 16,
    and report the other rows' identity as unverified (not taken):
    - 150 ms: 13 of 16, so (c) or (d) would be needed as well;
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

  None was recommended, and none is taken: the case passes on the measured
  basis, so the deltas stand as written.

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
protocol.allow=never` on every Git child except the push child, so that a lazy
fetch in a partial clone fails locally and the row is `inspection-error`; What
Changes, seam and
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
policy, so every Git child except the push child also pins the six per-protocol
policies and the scrub gains `GIT_ALLOW_PROTOCOL`, seventeen names then and
thirty-one since Brett Heap's ruling Q9 B, with the residual of a
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
`Cleanup revalidates destructive actions`). Brett Heap's ruling Q9 B of
2026-10-21, given through lane openRepoProject-4's spec 005 clarify round in
the words the departures quote, sets `GIT_TRACE2`, `GIT_TRACE2_EVENT` and
`GIT_TRACE2_PERF` to `0` on every Git child, the push child included, and adds
the fourteen trace variables to the scrub, thirty-one names (What Changes,
evidence model; Capabilities, `project-command` ADDED; Impact, `project`;
Decisions, departures and council; this list; design Context, D6, D11, D17,
D20, Risks; `tasks.md` 1.2, 1.4; the delta `project-command` ADDED evidence
model, its scenario "The push child reaches its remote" and its added scenario
"Trace targets are never written"). Brett Heap's rulings of 2026-10-21 on lane
openRepoProject-3's recommendations LQ-10 to LQ-15, each in the words the
departures quote: LQ-15 refuses a relative `HOME`, `XDG_CONFIG_HOME`,
`GIT_CONFIG_GLOBAL` or `GIT_CONFIG_SYSTEM` before any Git child,
`relative-config-path` (What Changes, evidence model; Capabilities `:10`,
`:22` and `project-command` ADDED; Impact, `project` and README; Decisions,
departures; this list; design Context, D6, D11, D16, D18, D20, Risks;
`tasks.md` 1.2, 1.4; the deltas' `Clean reports local worktree state` and its
added scenario "A relative configuration path", `Clean plans and refusals are
versioned JSON`, `Inspect and diagnose`, and the `project-command` ADDED
evidence model and its added scenario "A relative configuration path in
status, doctor and update"); LQ-10 adds `-c core.trustctime=true -c
core.checkStat=default` to every status probe, the hidden-state probe and the
removal (What Changes, seam and evidence model; Rules This Change Keeps;
Capabilities, review-safety `:49` and `project-command` ADDED; Decisions,
departures; this list; design Context, D9, D11, D20, Risks; `tasks.md` 1.2,
1.4; the deltas' `Clean can explicitly retire verified worktrees`, `Cleanup
revalidates destructive actions`, and the `project-command` ADDED evidence
model, its scenario "The pinned status configuration" and its added scenario
"An edit that keeps its size and restores its mtime"); LQ-12 runs every owner
tool of `update --apply` with the push child's scrub (Capabilities, `:31`;
Impact, `project`; Decisions, departures; this list; design Context, D6, D16,
D20; `tasks.md` 1.2, 1.4; the delta `Explicit maintenance` and its added
scenario "Owner tools see the repository the check inspected"); LQ-11 makes a
linked worktree whose effective work tree is not its registered path
`registration-mismatch` (What Changes, eligibility and revalidation;
Capabilities, review-safety `:21`, `:49` and `project-command` ADDED;
Decisions, departures; this list; design Context, D6, D7, D14, D20, Risks;
`tasks.md` 1.2, 1.4; the deltas' `Clean classifies preservation and cleanup
actions`, `Clean bounds its Git work and reports omitted work`, `Cleanup
preserves all local work not proven disposable`, `Cleanup revalidates
destructive actions`, `Cleanup states a narrow guarantee and its residual
window`, and the `project-command` ADDED evidence model and its added scenario
"A linked worktree whose work tree is redirected"); LQ-13 adds the gate
`worktree-only-commits` and its revalidation (What Changes, eligibility and
revalidation; Capabilities `:55`, batch, review-safety `:21`, `:49` and its
ADDED; Decisions, departures; this list; design Context, D7, D12, D14, D18,
D20, D21, Risks; `tasks.md` 1.2, 1.4; the deltas' `Clean previews and applies
a batch of eligible worktree removals in one repository` and its added scenario
"A commit held only by the worktree", `Clean bounds its Git work and reports
omitted work` and its scenario "Bounded revalidation work", `Clean records a
reconcilable result for every removal target`, `Cleanup preserves all local
work not proven disposable`, `Cleanup revalidates destructive actions` and its
added scenario "A worktree-only commit made after the plan", and `Cleanup
states a narrow guarantee and its residual window`). Lane openRepoProject-3's
W8 read of LQ-15 at `cc000ea` (HIGH 0, MEDIUM 1, LOW 7, nothing departing)
adds the pointer that leaves the overview's code and exit status to
`add-project-overview` (M1; Decisions, departures), a list of the sites that
striking `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` touches, with the system's
configuration named only in their own sentence (L2), C-44's "does not follow
the order of precedence" and an AND for it (L4), the order after
`invalid-arguments` (L3), the fill label on D18's message (L1), `update`'s
message (L5) and the ignore-file risk's weight (L6) (this list; design Context,
D11, D16, D18; `tasks.md` 1.2; the deltas' `Clean reports local worktree
state` and its scenario "A relative configuration path", and the
`project-command` ADDED evidence model); its L7, interim wording that holds
once LQ-10 to LQ-14 are recorded, needs no edit. LQ-14 adds the gate
`operation-in-progress` and its revalidation (What Changes, eligibility;
Capabilities `:55`, batch, review-safety `:21`, `:49` and its ADDED;
Decisions, departures; this list; design Context, D7, D18, D20, D21, D22,
Risks; `tasks.md` 1.2, 1.4; the deltas' `Clean previews and applies a batch of
eligible worktree removals in one repository` and its added scenario "An
operation in progress", `Clean bounds its Git work and reports omitted work`,
`Clean records a reconcilable result for every removal target`, `Cleanup
preserves all local work not proven disposable`, `Cleanup revalidates
destructive actions` and its added scenario "An operation started after the
plan", and `Cleanup states a narrow guarantee and its residual window`). Lane
openRepoProject-3's W10 read of LQ-12 and LQ-13 at `93de4bb` (HIGH 1, MEDIUM
1, LOW 8; its H1 departing from `BA:188-192`), under the lead's rulings R-124
and R-127, makes a failed or timed-out LQ-13 or LQ-14 check `inspection-error`
in the plan and `state-changed` at revalidation, only a decided result giving
the gate's reason (H1); takes the branch reflog's non-zero objects as the
negatives (M1); names all four gates past the cap (L1); and records L2 to L5,
L7 and L8, L3's stricter revalidation kept because it fails safe and L5's
`logs/refs/worktree/` as a risk (What Changes, eligibility and deferral;
Capabilities `:31`; Decisions, departures; this list; design Context, D6, D12,
D14, D21, D22, Risks; `tasks.md` 1.2; the deltas' `Clean previews and applies
a batch of eligible worktree removals in one repository` and its scenarios "An
operation in progress" and "A commit held only by the worktree", `Clean bounds
its Git work and reports omitted work`, `Cleanup preserves all local work not
proven disposable` and `Cleanup revalidates destructive actions`). Lane
openRepoProject-3's W9 read of LQ-10 and LQ-11 at `ea697ba` and `addd346`
(HIGH 0, MEDIUM 2, LOW 9, nothing departing), under the lead's R-125, adds the
`commondir` file to the two-way registration and its scenario "A commondir
that names another repository" (M2), the pointer that row 4c and the per-row
probe reach `project overview` (M1), and L1 to L9: the non-racy precondition,
the filter risk under LQ-16, the hidden-state pins made a requirement, the
stale quote in `add-project-overview`, `USE_NSEC`, the remedy that unsets
`core.worktree` and `core.bare`, the citations of `BA:615` and `BA:679`, two
scenarios said to run without the extension, and D17's table said not to be
exhaustive (Capabilities project-command ADDED; Decisions, departures;
Dependencies and Sequencing; this list; design Context, D6, D7, D11, D17,
D18, Risks; `tasks.md` 1.2, 1.4; the deltas' `Clean reports local worktree
state` and its scenario "The plain report exits by completeness", `Clean
previews and applies a batch of eligible worktree removals in one repository`,
`Clean bounds its Git work and reports omitted work` and its scenario "Bounded
revalidation work", and the `project-command` ADDED evidence model with its
scenarios "An edit that keeps its size and restores its mtime" and "A
commondir that names another repository"). Lane openRepoProject-3's W14 read
of LQ-14 at `43f7107` (HIGH 1, MEDIUM 1, LOW 4; its H1, a failed listing,
already fixed by R-124 (b)), under the lead's R-126, adds `MERGE_AUTOSTASH`,
`NOTES_MERGE_PARTIAL` and `NOTES_MERGE_REF` to the markers, eleven in all, and
the scenario "A squash merge that holds an autostash" (M1); cites, for a
failed re-listing at revalidation, the rule by which a value that cannot be
re-read counts as a difference, with `state-changed` (H1); and records L1 (the
four gates past the cap, fixed by R-124), L2 (the listing in What Changes), L3
(that `43f7107` also re-wrapped the lines of `Cleanup revalidates destructive
actions` naming the target's worktree identity and two-way registration, with
no change of words) and L4 ("never by a Git child") (What Changes, eligibility
and revalidation; Capabilities batch; Decisions, departures; this list; design
Context, D18, D22; `tasks.md` 1.2, 1.4; the deltas' `Clean previews and
applies a batch of eligible worktree removals in one repository` with its
scenario "An operation in progress" and its added scenario "A squash merge
that holds an autostash", and `Cleanup preserves all local work not proven
disposable`). Lane openRepoProject-3's W21 confirm read of R-124 to R-126 at
`1ebdd90` (HIGH 0, MEDIUM 0, LOW 6), under the lead's R-146 and R-147, adds
the scenario "A check that fails at revalidation" (L-a); "non-zero" in the
LQ-13 departures entry and the gate's first sentence (L-b); `git commit` in
the `operation-in-progress` next step for a squash merge that holds an
autostash, which no abort ends (L-c); the fast-forward squash, which applies
the autostash at once (L-d); this declaration that the commits of R-124, R-125
and R-126 also re-wrapped the paragraphs their edits lengthened, the
proposal's eligibility bullet among them, with no other change of words
(L-e); and the drain message naming every gate after the cap (L-f). It cites
the Git source lines of D7, D11, D21 and D22 by release, tags `v2.36.6` and
`v2.43.7`, as read in those tarballs. By R-147 it adds the push refusals the
baseline makes and this change keeps, with the scenario "Push refuses a
branch it may not push", and branch deletion's refusals, with the scenario
"Branch deletion refuses a branch it may not delete", both checked against
`project` and lane openRepoProject-2's tests at `2439838` (What Changes,
deferral; Capabilities `:39` and `:55`; Decisions, departures; this list;
design Context, D7, D12, D18, D21, D22, Risks; `tasks.md` 1.2, 1.4; the
deltas' `Clean can explicitly push safe feature branches`, `Clean can
explicitly retire verified worktrees`, `Clean previews and applies a batch of
eligible worktree removals in one repository`, `Clean bounds its Git work and
reports omitted work` and `Cleanup revalidates destructive actions`). Lane
openRepoProject-3's W26 confirm read of that round at `6f2cb54` (HIGH 0,
MEDIUM 0, LOW 6), under the lead's R-171, corrects D22 and D18: `git reset
--hard` and `git merge --quit` also end a held autostash, saving the edit to
the stash list (F-1); calls the upstream mapping refusal's trigger R-130's
widening (F-2); adds the case of a branch that no worktree holds to the push
scenario and says why `review-required` stays out (F-3); writes R-171's rule,
that at revalidation only a decided effective work tree that is not the
target's path gives `identity-changed`, and the rule for every revalidation
child, that a deadline cut gives `deadline-exceeded` and a failure or a
timeout `state-changed` (F-4); declares that R-146's commit and the commits of
this entry and the R-178 entry below also re-wrapped the paragraphs their edits
lengthened, with no other change of words (F-5); and says "a gate after the cap"
in OQ-5 (F-6) (Capabilities `:39`; Decisions, OQ-5; this list; design Context,
D7, D18, D22; `tasks.md` 1.2; the deltas' `Clean can explicitly push safe
feature branches` and its scenario "Push refuses a branch it may not push",
`Clean records a reconcilable result for every removal target` and `Cleanup
revalidates destructive actions`). Under the lead's R-178, design D14 restates
the fit at 150 ms per child with writer G's measured counts: the planning term
counts LQ-11's per-row probe where `extensions.worktreeConfig` is true, seven
children per target would fit 14 removals rather than 16 at a hypothetical P of
168, and at 128 rows in such a repository the first removal would spawn at 45.3
s, so none is made, safely; open question LQ-20 names the three options before
Brett Heap, choosing none. No requirement changes: no sentence of `Clean bounds
its Git work and reports omitted work` is false under the restated figures,
since it bounds children per target and targets per run and promises no number
of removals (Open Questions; this list; design Context, D14, Risks, Open
Questions; `tasks.md` 1.2). Lane openRepoProject-3's W31 confirm read of that
round at `a664799` (HIGH 0, MEDIUM 2, LOW 8), under the lead's R-187 and R-190,
with lane openRepoProject-5's A10 read of the same commit, which the lead
relayed: lets the rule for a revalidation child decide a read that the work
deadline cuts, and says "its own budget" where the earlier wording left the
deadline out (M-1); states that the cap test is D5's, at task 2.1's measured
costs, names the two probes that task 2.1 did not measure and the stand-ins
costed for them, gives the fit on D14's flat 150 ms basis, on that measured
basis and on the mixed basis, and restates LQ-20 so that its first step is to
measure those probes or to decide the basis, with the rule's own step, lowering
the caps, as option (d) and no option chosen (M-2); drops R-171's rationale that
planning makes a failed probe a row error, since there it makes the row's
registration disagree (L-1, the lead's R-187 erratum); adds the scenario "A
work-tree probe at revalidation", which pins R-171's three arms (L-2); limits
D22's `git merge --abort` claim to a squash, which writes no `MERGE_HEAD`, and
says that `git commit` keeps in the stash list an edit that conflicts with what
the merge brought, both checked on Git 2.43.0 and 2.56.0 (L-3); labels the 14
removals for seven children per target, here and in D14, as a hypothetical P of
168 (L-4); gives each single-target run to its end in D14's table (L-5);
replaces the stale 26.4 s margin (L-6); says that re-running takes the next 16
as the rows ahead of them are removed, so that a run that the deadline stops
before any removal leaves its 16 to the next, which the R-178 entry above missed
when it found no sentence of `Clean bounds its Git work and reports omitted
work` false (L-7); widens the W26 entry's declaration of re-wrapped paragraphs
to both commits of that round (L-8); and declares that this commit also
re-wrapped the paragraphs its edits lengthened, with no other change of words
(Open Questions; this list; design Context, D7, D14, D21, D22, Risks, Open
Questions; `tasks.md` 1.2, 1.4; the deltas' `Clean bounds its Git work and
reports omitted work` and `Cleanup revalidates destructive actions`, with its
added scenario "A work-tree probe at revalidation"). Lane openRepoProject-3's
W36 confirm read of that round at `2e819ad` (HIGH 0, MEDIUM 2, LOW 6), under the
lead's R-207 and R-208, with its W32 read of LQ-14 in feature 004 (the lead's
R-200): rewords LQ-20's option (c) as a longer work deadline where
`extensions.worktreeConfig` is true, the 5 s removal floor kept, since a larger
floor would remove fewer, and calls 45 s the spawn limit (M-A, R-207); gives
each option's result on each basis, among them that under (a) a 128-row
repository at 150 ms per child removes nothing on every re-run, and that (b)
fits 13 of 16 there (M-B); gives (d)'s 150 ms time with E = T, 33.15 s (L-a);
cites PR #11 and its rule for D14's costs (L-b); names the 10,000-file removal
as the cap test's (L-c); excepts LQ-20 from the Open Questions preamble's
recommendation (L-d); names the three bases of LQ-20's step (ii), BA's flat one
as a change to D5 (L-e); and says where D14's Time column stops (L-f). By W32's
L1 and R-208, a listing of the `operation-in-progress` gate, or a `logs/HEAD`
read of the `worktree-only-commits` gate, not finished within the filesystem
budget makes the row `inspection-error` with `probe-timeout`, as feature 004
builds both, where the text said the row was left unprobed. By R-208, at
revalidation a filesystem call that fails, or runs past its own budget while the
deadline is not the limit, gives `state-changed` whatever its step, as a Git
child does, a decided value keeping its step's reason, a path found missing
deciding that it is absent, and a deadline cut giving `deadline-exceeded`; the
scenario "A check that fails at revalidation" gains an unreadable `.git` file.
R-208 is a reading of BA:271-276, by which "a value that cannot be re-read,
including a filesystem call that times out, counts as a mismatch": a read that
fails decides no identity difference, so its mismatch is the packet's "any
other" difference, `state-changed`; this reading went to Brett Heap to confirm,
as O-2, on 2026-10-22. This commit also re-wrapped the paragraphs its edits
lengthened, with no other change of words (Capabilities `:49`; Open Questions;
this list; design Context, D7, D14, D21, D22, Risks, Open Questions; `tasks.md`
1.2; the deltas' `Clean previews and applies a batch of eligible worktree
removals in one repository` and `Cleanup revalidates destructive actions`, with
its scenario "A check that fails at revalidation"). Lane openRepoProject-3's W38
confirm read of that round at `9267303` (HIGH 0, MEDIUM 0, LOW 6), under the
lead's R-213 and R-216: adds the `rev-list`'s limit, about 581 ms, to the pass
test of LQ-20's step (i) (L-1); says that the `worktree-only-commits` gate's
outcome rule differs from the branch reflog's for a read not finished within the
filesystem budget (L-3); makes an administrative directory that the
`operation-in-progress` listing finds absent at revalidation a registration
difference, `identity-changed`, as feature 004 builds it (L-4); writes "SHALL
NOT" (L-5); says that option (c) also moves the ratified 60 s invocation
deadline there, to 80.55 s on the 150 ms basis and 65.0 s on the mixed one, and
that choosing the flat basis at step (ii) fails the case at once, so that an
option has to be chosen with it (L-6); and records R-208 as a reading of
BA:271-276 that went to Brett Heap as O-2 (O-2). W38's L-2 touched only the
lead's question file. This commit also re-wrapped the paragraphs its edits
lengthened in `design.md` and this file, with no other change of words (Open
Questions; this list; design Context, D7, Open Questions; `tasks.md` 1.2; the
deltas' `Clean previews and applies a batch of eligible worktree removals in one
repository` and `Cleanup revalidates destructive actions`).

Round (f): Brett Heap's ruling of 2026-10-22 on LQ-20, in his words to lane
openRepoProject-2, "LQ-20: go with (i), measure first" (the lead's R-236), chose
its step (i): LQ-11's work-tree probe and LQ-13's `rev-list` were measured on
task 2.1's protocol, in the same `py-bench` container at a 1-minute load of 15
to 21, at 5.8 ms and 106.9 ms warm, 8.7 ms and 160.3 ms with the margin, neither
reading the index, and the cap test, rerun on those costs, passes on the
measured basis: at 128 rows and 16 targets where `extensions.worktreeConfig` is
true all 16 removals fit, the 16th spawning at 30.0 s with 20.0 s left (37.7 s
with 20,000-file removals), and they would stop fitting only at about 114 ms for
the work-tree probe or 630 ms for the `rev-list`, with the margin. Options (a)
to (d) are therefore not needed and none is taken; they stay, each marked not
taken, as the record of what was costed. D14's measured column and reachability
sentence, and the Risks entry, take the measured costs, and D14's mixed basis,
restated with them, fits all 16 as well. With it, lane openRepoProject-3's W42
confirm read of round (e) at `f0bf538` (HIGH 0, MEDIUM 0, LOW 2): D14 says that
option (c) also moves the ratified 60 s invocation deadline, to 80.55 s on the
150 ms basis and 65.0 s on the mixed one, where it named only the 64 s run bound
(L-1); and D7 and D22's Revalidation bullet carry W38's L-4 clause, that an
administrative directory that the `operation-in-progress` listing finds absent
is a registration difference, `identity-changed` (L-2). By the lead's R-245, on
lane openRepoProject-3's W53 departure ledger, the departures gain two entries,
a revalidation read or child that the work deadline cuts counting as no
difference (`BA:271-272`; its 19-10) and push's wider upstream-mapping refusal
(`BA:424-425`; its 19-11), and the push-child exception names the packet lines
its process group departs from, `BA:1238-1240` and `BA:465-468`, with R-28 and
its open question (Open Questions, the push-child exception; lane 2's LQ-3; its
19-08). No requirement changes and no delta is edited. This commit also
re-wrapped the paragraphs its edits lengthened in `design.md` and this file,
with no other change of words (Decisions, departures and council; Open
Questions; this list; design Context, D7, D14, D22, Risks, Open Questions;
`tasks.md` 1.2, 2.1).

Round (g), lane openRepoProject-3's W52 read of next steps that tell a person to
do what Git refuses, at `f0bf538` and feature 004's `e69f6ef`, each finding
confirmed on Git 2.43.0 and on the 2.36.6 floor, under the lead's R-248:
`registration-mismatch`'s next step, and the plan-blocking remedy that `Clean
previews and applies a batch of eligible worktree removals in one repository`
names, unset `core.worktree` and `core.bare` in the repository's `config`, or in
that worktree's `config.worktree`, where they named only `config.worktree`,
since with the setting in the repository's own `config` the unset finds nothing
and `git worktree repair` and `git worktree prune` change nothing (F-3); branch
deletion's refusal of a branch that the main worktree holds names detaching HEAD
there, or checking out the merge target there, and then retrying, where the
baseline's `Remove the linked worktree first` names a removal that Git refuses
for the main worktree with exit 128 (F-5, lane openRepoProject-5's RI-4); the
next steps of `unstarted-branch` and `reflog-unavailable`, gate 7, which comes
before `contains-submodule`, add `--force` where Git refuses the removal for a
submodule (F-7); `contains-submodule`'s next step names `git worktree remove
--force` (F-8); `operation-in-progress`'s adds, for a marker left with nothing
in progress, the operation's `--quit`, since an empty `sequencer` or
`rebase-merge` fails `--abort` (F-9); and a locked worktree's partial-removal
note says to unlock it first, since `git worktree remove --force` refuses a
locked worktree (F-2), a sentence that for a locked row replaces the ratified
recovery text of `0050f3e`, which the delta keeps for every other row, and so
waited on Brett Heap's word together with F-1, the ceiling's recovery text,
until he ruled both on 2026-10-22 (round (h)). The scenario "Branch deletion
refuses a branch it may not delete" quotes the new refusal, and the scenario
counts stay. W52's F-6 and F-10 are baseline report texts that this change
neither states nor quotes, D14 keeping the baseline report's layout, and are
feature 004's; its F-4 is feature 004's `delete-branch` argv, and its F-11 and
F-12 are lane openRepoProject-5's. Its F-1, the ceiling's recovery text, amends
ratified text and waited on Brett Heap, and is unchanged here; he ruled it on
2026-10-22 (round (h)). This commit also re-wrapped the paragraphs its edits
lengthened, with no other change of words (What Changes, first bullet;
Capabilities `:55`; this list; design Context, D4, D18, Risks, Migration Plan;
`tasks.md` 1.2; the deltas' `Clean classifies preservation and cleanup actions`,
`Clean can explicitly retire verified worktrees` and its scenario "Branch
deletion refuses a branch it may not delete", and `Clean previews and applies a
batch of eligible worktree removals in one repository`).

Round (g2), lane openRepoProject-4's A1 on change 2's overview (PR #34), under
the lead's R-252: the overview mirrors the remedies of `unstarted-branch` and
`reflog-unavailable` under a 200-character message rule, so the clause that
round (g) added to them (F-7) is shortened. Both remedies now end "review, then
git worktree remove yourself (--force if it holds a submodule)", in What
Changes, first bullet, and in design D18 and the Migration Plan. The advice, the
gate order and the scenario counts stay, and no delta is edited. This commit
also re-wrapped the paragraphs its edits shortened or lengthened, with no other
change of words (What Changes, first bullet; this list; design Context, D18,
Migration Plan; `tasks.md` 1.2).

Round (g3), lane openRepoProject-3's W59 read of round (f) at `662be89` (HIGH 0,
MEDIUM 0, LOW 4) and of round (g) at `4f1c0e0` (HIGH 0, MEDIUM 2, LOW 4), under
the lead's R-253: step (i)'s runs are 40 to 48 a case, where design D14 and
`tasks.md` 2.1 said 30 to 48 (LOW-1); its load is stated as measured, a 1-minute
load of 15 to 21 on 32 threads, where Open Questions, here and in the design,
called it comparable with task 2.1's, a load this change does not record
(LOW-2); the push-child exception's council entry and round (f)'s entry cite the
question as Open Questions, the push-child exception, lane 2's LQ-3, where they
named only LQ-3, a label no section here carries (LOW-3); and the two paragraphs
left ragged, design D7's and this file's LQ-20 question, are re-wrapped, and
`tasks.md` 2.1 reads "measured, by the same protocol, the two children that
LQ-11 and LQ-13 added" (LOW-4). F-2's sentence in `Clean classifies preservation
and cleanup actions`, which round (g) declared added beside the ratified
recovery text of `0050f3e`, replaces that text for a locked row: the sentence
stays as written, and round (g)'s entry, design D4 and D18 now say that it
replaces the ratified text for locked rows and waits on Brett Heap's word
together with F-1, the ceiling's recovery text (G-1), as both did until he
ruled them on 2026-10-22 (round (h)). Branch deletion's message
for a branch the main worktree holds, round (g)'s F-5, is declared among the
departures, against `BA:424-425` and the baseline's `project:730` at `15504f1`,
as push's wider refusal is (G-2). Two AND clauses pin round (g)'s two unpinned
clauses, so the scenario counts stay 71, 22 and 24: "Only tracked-file
deletions" gains a locked worktree's recovery text, and "A linked worktree whose
work tree is redirected" the remedy that its `registration-mismatch` group
names, unsetting `core.worktree` and `core.bare` in the repository's `config` or
in a worktree's `config.worktree` (G-3). D18's non-drain line ends "(--force for
any that holds a submodule)", W52's F-8 at its second site (G-4);
`operation-in-progress`'s next step, in D18 and Risks, gives the operation's
`--quit` "where --abort fails for a marker with nothing in progress", since for
an empty `rebase-merge` `git status` still reports a rebase in progress (G-5);
and rounds (g), (g2) and (g3) are entries of their own, each with one sentence
on its re-wrapping (G-6). This commit also re-wrapped the paragraphs its edits
shortened or lengthened, with no other change of words (Decisions, departures
and council; Open Questions; this list; design Context, D4, D7, D14, D18, Risks,
Open Questions; `tasks.md` 1.2, 2.1); the deltas only gained their AND lines, in
the scenarios "Only tracked-file deletions" of `Clean classifies preservation
and cleanup actions` and "A linked worktree whose work tree is redirected" of
the `project-command` ADDED evidence model, and no delta line was re-wrapped
(lane openRepoProject-3's W64 L-4, round (h)).

Round (h), lane openRepoProject-2's open points after writer E, under the lead's
R-258, R-259 and R-260, with writer E's report on feature 004 at `d764c26`, lane
openRepoProject-5's RI-3 and O-1, lane openRepoProject-3's W64 read of rounds
(g2) and (g3) at `6bf9f77` (HIGH 0, MEDIUM 1, LOW 5), and Brett Heap's ruling of
2026-10-22, in his words to lane openRepoProject-2, "F-2: yes; F-1:
prune-then-delete; O-1: deadline-exceeded" (the lead's R-263), which ends
R-260's holding of O-1 and the round's first brief, which kept F-1
byte-identical and O-1 pending. The Decisions opening and the departures list
now separate their kinds: the decisions that PR #11 carried, the first eleven
departures among them, were ratified with its merge; the next seven departures
carry Brett Heap's rulings of 2026-10-21; and the last three, the work
deadline's cut at revalidation, push's wider upstream refusal and branch
deletion's message for a branch the main worktree holds, were declared by this
amendment's rounds and wait on his ratification of it, as the push-child
exception does; design Open Questions says the same, and no entry's text changes
(R-258; W64's point 1). Every refusal that a `core.worktree` or `core.bare`
redirect of a linked worktree causes is `inspection-incomplete`: in the batch's
preview, apply and report, in push and branch deletion, and in a single-target
removal naming the redirected row, whose own `inspection-error` makes its plan
incomplete before any gate's exclusion. Feature 004 at `d764c26` showed this on
Git 2.43.0 and 2.36.6, with the redirect in the worktree's `config.worktree`
(`core.worktree` or `core.bare`) and in the repository's `config`
(`core.worktree` naming the main worktree), and its remedy named repair, prune
and removal by hand but not the unset, which the delta's plan-blocking SHALL
requires as the cause fits (R-258, W64 M-1). D18 therefore gives the refusal a
variant where any row it counts is `registration-mismatch`, "repair or remove
the inspection-error rows first: git worktree repair, git worktree prune, unset
core.worktree and core.bare in the repository's config or in a worktree's
config.worktree, or remove the row by hand after review"; What Changes names the
unset beside the other remedies; and the scenario "A linked worktree whose work
tree is redirected" pins the refusal's remedy and gains an AND for the
repository's own `config` (W64 L-5). A redirect of the main worktree itself is
refused at resolution with `target-not-repository-root`, before any plan. The
bounds sentence of `Clean bounds its Git work and reports omitted work`, and the
revalidation bound of `Cleanup revalidates destructive actions`, carry RI-3's
exception: where the path of the repository's root or of its common directory
holds a line feed, the identity probe is read one option per child, so a
revalidation spawns at most nine Git children, ten where the plan read
`extensions.worktreeConfig` as true, and the final rescan at most six, as writer
E measured on both Git builds for a root and this round for a separate git
directory; the plan's `probes.estimated` counts them, where feature 004 at
`d764c26` falls three short per target and three for the rescan (What Changes,
revalidation; design D7, D14; R-259). `operation-in-progress`'s next step, in
design D18 and Risks, adds "or, where Git leaves such a marker in place, delete
it by hand from that worktree's git directory", since writer E's table, re-run
here on both builds, shows markers that no Git command clears: an empty
`CHERRY_PICK_HEAD`, `REVERT_HEAD` or `MERGE_AUTOSTASH`, whose `--abort` exits
128 and whose `--quit` exits 0 and leaves it, a lone `BISECT_LOG`, an empty
`MERGE_HEAD` directory, a notes-merge marker file, and a `rebase-apply`,
`rebase-merge` or `sequencer` that is an empty file; deleted by hand from the
worktree's git directory, each such row is selected (R-259). Change 2's overview
(PR #34's A1) does not mirror this next step, so the 200-character rule of R-252
does not bind it. D18 also says that this change states no argument vector for
branch deletion, and that feature 004 runs `git -C ROOT branch -d -- BRANCH`
(W52 F-4, R-259). By Brett Heap's ruling: F-2's recovery text for a locked row
stands as written and is now ruled, in design D4 and D18 and in the entries of
rounds (g) and (g3); F-1's ceiling recovery text keeps `git worktree remove
--force` only where the rescan finds both the target's `.git` file and its
registry entry present, and otherwise reads
"inspect, then `git worktree prune` and delete `<path>` by hand", at both of its
sites in the deltas, with an AND clause in the scenario "A removal past the hard
ceiling", and in What Changes, Capabilities and design D9 and D18, the rescan
reading the `.git` file by one `lstat`, so that its bound of three Git children
holds; and O-1's gate-7 sentence gives a read that the deadline cuts
`deadline-exceeded`, the row unprobed and the plan incomplete with
`deadline-exceeded`, while a read not finished within the filesystem budget, the
deadline not being the limit, keeps `inspection-incomplete`, in What Changes and
design D10. A list of amendments of ratified text, after the departures, records
the three against `0050f3e`: pcl:135-138 for F-2, pcl:253-256 and pcl:922-926
for F-1, and pcl:606-608 for O-1. From W64, round (f) gets its label inside the
shared paragraph above (L-3); round (g3)'s entry no longer says that two deltas
were re-wrapped, since each only gained a line (L-4); design Context and
`tasks.md` 1.2 record F-1 and F-2 as ruled (L-2); and L-1 is settled as designed
(R-264). The scenario counts stay 71, 22 and 24. This round's commits also
re-wrapped the paragraphs their edits lengthened, round (f)'s among them after
its label, with no other change of words (What Changes; Capabilities `:55`;
Decisions, departures and amendments; this list; design Context, D4, D7, D9,
D10, D14, D18, Risks, Open Questions; `tasks.md` 1.2; the deltas' `Clean can
explicitly retire verified worktrees`, `Clean previews and applies a batch of
eligible worktree removals in one repository`, `Clean bounds its Git work and
reports omitted work`, `Clean records a reconcilable result for every removal
target` and `Cleanup revalidates destructive actions`); the scenarios "A removal
past the hard ceiling" and "A linked worktree whose work tree is redirected"
only gained or extended AND lines, and the `project-command` ADDED evidence
model's text is unchanged (lane openRepoProject-3's W70 LOW-2, round (j)).

Round (i), round (h)'s open point, under the lead's R-271: a redirect of the
main worktree, by a `core.worktree` or `core.bare` in the repository's `config`,
or in the main worktree's `config.worktree` where `extensions.worktreeConfig` is
true, is refused at resolution with `target-not-repository-root` where the root
is passed by an absolute path, or by a bare name that `discover()` resolves to
the root itself (lane openRepoProject-3's W80 M-2, round (k)), rightly, since no
main worktree is there to clean, but feature 004's message for that code, `Not
the main worktree of a repository: PATH; pass the repository root.`, asks a
person who passed the root to pass it. The message is feature 004's, from its
contract, not the baseline's (`project` at `961c405` holds no such text), so
the rule that keeps baseline wording does not hold it. Fixtures on Git 2.43.0
and 2.36.6, against feature 004 at `7164d7f`, give the same output on both
builds: with `core.bare` true, from either file, the identity probe exits 128
with `fatal: this operation must be run in a work tree`, while `git rev-parse
--path-format=absolute --git-dir --git-common-dir --is-bare-repository` prints
the checkout's `.git` twice and `true`; with `core.worktree` naming another
directory, a missing one included where the value is absolute, from either file,
the identity probe prints that directory as the toplevel while the registry's
first record is the checkout (a relative value naming a missing directory makes
both probes and `git config --unset` exit 128 with `fatal: cannot chdir to
'<value>'`, so the refusal keeps the plain message, in the plain layout, the
`.git`-file layout and a submodule checkout moved by hand alike; W80 L-2, W81
M-1, round (k)); without the extension Git ignores `config.worktree` and the
root resolves; a separate git directory whose `core.worktree` names another
directory, or whose `core.bare` is true, is refused the same way; and once
`core.worktree` and `core.bare` are unset in both files, every one of these
roots resolves. Design D18 therefore gives the refusal a variant that names the
redirect, `Not the main worktree of a repository: PATH; core.worktree or
core.bare redirects the main worktree; unset both in the repository's config, or
in the main worktree's config.worktree, then run again.`, printed only where the
directory the resolution examined holds its own `.git`, whose realpath is the
repository's common directory, and Git run there uses another work tree or
none; and D6 adds row 3b, the one child that shows `core.bare` true where the
identity probe failed, run only on that refusal and only where the directory
holds a `.git`, so that a run that resolves spawns no child for it. A `git init
--bare` repository passed by its own directory keeps the plain message, as do a
subdirectory, a linked worktree, a linked worktree that its own
`config.worktree` redirects, a submodule checkout whose own configuration
redirects nothing (W80 L-5, W81 L-1, round (k)) and a directory outside any
repository; a repository made by `git init --bare X/.git` and passed as X cannot
be told from a checkout at X whose `core.bare` is true by anything Git reads,
and takes the variant, which is true of it, since with `core.bare` unset X
resolves. Design D6 also no longer says that three lines from the identity probe
mean a submodule checkout: a plain checkout whose toplevel or common directory
holds a line feed in its path prints three lines too where only one of the two
holds it, as a separate git directory may, or four where a toplevel holding it
has its common directory under it (W80 L-3, round (k)), and on any count but two
the probe is read again one option per child, which tells the two apart, as
feature 004's `identity_probe()` does at `7164d7f` (lane openRepoProject-4's
finding, through the lead). No delta states this code's message text, so neither
of those items edits a delta. Lane openRepoProject-3's W73 M-1 reproduced on Git
2.43.0 and 2.36.6, and this round again, that where Git cannot stat a worktree's
`.git`, as under `EACCES` on its path, `git worktree prune` deletes that live
worktree's administrative directory, its index, `HEAD`, per-worktree refs and
reflog with it, while F-1's text sent a `partially-removed` target whose `.git`
the rescan could not read, a read that failed or was cut, to `git worktree
prune`, the case being unspecified. By the lead's R-284, which refines how Brett
Heap's F-1 ruling applies to a read that fails and was put to him to confirm, as
he did on 2026-10-22 in his words "R-284: yes" (the lead's R-290), such a
target's recovery text is "inspect `<path>` by hand; its `.git`
could not be read, so do not run `git worktree prune`, `git worktree remove` or
`git gc` until it can", whatever the rescan finds of the registry entry, while
"where either is gone" keeps a `.git` file shown absent and an entry gone where
the `.git` file was read (W80 L-1, round (k)); the deltas `Clean can explicitly
retire verified worktrees` and `Clean records a reconcilable result for every
removal target` state it, the scenario "A removal past the hard ceiling" gains
an AND clause, and What Changes, Capabilities, the amendments list and design D9
and D18 carry it. Design D18 also narrows round (h)'s sentence that a redirect
of the main worktree is refused at resolution to an absolute path or a bare
name, and says what a relative path or no argument from the root does: refused
the same way under `core.bare` true, where Git finds no worktree there, but
under a `core.worktree` not refused, the plan reading the main row where
`core.worktree` points, as round (i)'s fixtures show, exit 0, or 1 with an
incomplete plan (lane openRepoProject-3's W70 LOW-3); the variant's unset is the
remedy wherever the refusal prints (W80 L-4, round (k)). The scenario counts
stay 71, 22 and 24. The round's commits also re-wrapped the paragraphs their
edits lengthened, with no other change of words (What Changes; design Context,
D6, D9 and D18), and `tasks.md` 1.2 names the round.

Round (j), lane openRepoProject-3's W70 confirm read of round (h) at `b3228bb`
(HIGH 0, MEDIUM 3, LOW 5; validate 9 of 9, the scenario counts 71, 22 and 24),
under the lead's R-285, R-287 and R-291, with Brett Heap's confirmation of R-284
on 2026-10-22, in his words "R-284: yes" (the lead's R-290). LQ-11's work-tree
probe asks Git for one value, but the evidence model read output that was not
exactly one line as a disagreeing registration, so a linked worktree whose own
path holds a line feed read `registration-mismatch` wherever
`extensions.worktreeConfig` is true, its plan incomplete and its remedy naming
an unset where nothing is set, against the ratified scenario "Control-character
and non-UTF-8 paths" (W70 M-2, reproduced on Git 2.43.0 and 2.36.6). By the
lead's R-287, with R-291's refinement, which the evidence model now words so:
"the probe's standard output, less the one line feed Git ends it with, SHALL be
read as one path, which may itself hold line feeds; output that is empty, that
names no path, or that does not end in a line feed SHALL make the row's
registration disagree", and the scenario "A linked worktree whose work tree is
redirected" gains an AND clause for such a worktree, which is selected. At
revalidation, output read as one path other than the target's, even over several
lines, is `identity-changed`, and output that is empty, names no path or does
not end in a line feed is `state-changed`, a value that cannot be re-read, so
the scenario "A work-tree probe at revalidation" moves a directory whose name
holds a line feed to `identity-changed` and pins `state-changed` for a wrapper's
output without the line feed Git ends it with, the scenario counts unchanged
(the `project-command` ADDED evidence model and `Cleanup revalidates destructive
actions`; Capabilities, `project-command` ADDED; design D7). The amendments of
ratified text gain a second group, on lane rulings, waiting on his ratification
of #19, each entry with the `0050f3e` sentence it replaces: the line-feed
exception to the bounds (RI-3, R-259), the next steps for a worktree that holds
a submodule (F-7 and F-8, R-248, R-252 and R-253), the cap's re-run (R-187,
R-190) and the count split (`cecb4fc`) (W70 M-1); the Decisions opening and
design Open Questions name both groups. The departures gain the line-feed
exception, against `BA:679`, `BA:725-727` and `BA:743`, each quoted (W70 M-3).
The departures' preamble and design Open Questions count among what waits on his
ratification the parts of four of his rulings of 2026-10-21 that the lead's
rulings added, `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` in LQ-15's test
(R-102 (c) 3), the `commondir` check (R-125), the branch reflog's non-zero
objects among LQ-13's negatives (R-124 (c) and R-127, now named in its entry)
and LQ-14's three added markers (R-126) (W70 LOW-5). The reason that Git refuses
`git worktree remove --force` is narrowed to the states it refuses, while the
path remains, since the forced removal exits 0 once the path itself is gone, in
the deltas `Clean can explicitly retire verified worktrees` and `Clean records a
reconcilable result for every removal target`, What Changes, the ceiling's
amendments entry and design D18 (W70 LOW-1); F-1's three texts and F-2's text
are unchanged, byte for byte. Round (h)'s entry names What Changes among RI-3's
sites (W70 LOW-4), and no longer says that the scenarios "A removal past the
hard ceiling" and "A linked worktree whose work tree is redirected", or the
`project-command` ADDED evidence model, were re-wrapped, since those scenarios
only gained or extended AND lines (W70 LOW-2). By R-290, What Changes,
Capabilities `:55`, the amendments list, round (i)'s entry and design D9 and D18
say that Brett Heap confirmed R-284's third text, and its amendments entry
stands beside those of F-2, F-1 and O-1, its words unchanged. The scenario
counts stay 71, 22 and 24. This round's commit also re-wrapped the paragraphs
its edits lengthened, with no other change of words (What Changes; Capabilities
`:55` and `project-command` ADDED; Decisions, departures and amendments; this
list; design Context, D7, D9, D18, Open Questions; `tasks.md` 1.2; the deltas'
`Clean can explicitly retire verified worktrees`, `Clean records a reconcilable
result for every removal target`, `Cleanup revalidates destructive actions` and
the `project-command` ADDED evidence model).

Round (k), lane openRepoProject-3's W80 confirm read of round (i) at `e0c91bb`
(HIGH 0, MEDIUM 3, LOW 6; validate 9 of 9, the scenario counts 71, 22 and 24),
under the lead's R-294 and R-299, with the two findings of its W81 read of
feature 004 at `2707ff2` that bear on this text, M-1 and L-1, which the lead
relayed. Where Git cannot stat a worktree's `.git`, `git worktree remove`, with
or without `--force`, deletes its administrative directory as `git worktree
prune` does, on Git 2.43.0 and 2.36.6, so that the locked note's unlock and
forced removal would delete it too (W80 M-1, its E5 and E7): design D18 now says
that the third ceiling text takes precedence over the locked note wherever the
`.git` file cannot be read, as R-284's letter gives it, "A `.git` read that
fails or is cut gets a third note", and design D4 and the amendments list's F-2
and R-284 entries say the same. The third text's words stayed as Brett Heap
confirmed them: naming `git worktree remove` in them, or `git gc`, whose
automatic worktree prune deletes such a directory once its index is three months
old (W80 L-6), would change his ruled text and waited on his word, which he gave
on 2026-10-22, "R-324: yes" (the lead's R-343, round (n)). The scenario "A
removal past the hard ceiling", Capabilities `:55` and the amendments list's F-1
entry now say that the third text applies whatever the rescan finds of the
registry entry, and round (i)'s entry that "where either is gone" keeps an entry
gone where the `.git` file was read (W80 L-1). Design D18's sentence that a
redirect of the main worktree is refused at resolution where the root is passed
by a bare name held only where `discover()` resolves the name to the root
itself, through a family holder or a manifest there; otherwise a bare name takes
Git's toplevel, the redirect target, which is refused with the plain message, or
resolves where it is a work tree, inside the repository or another repository's
root, and under a `core.bare` true the run is refused with
`repository-not-found`, as D18 and round (i)'s entry now say (W80 M-2, reading
feature 004's `discover()` at `2707ff2`). Round (i)'s `b60f6ac` replaced a
ratified sentence of design D6 on lane openRepoProject-4's finding, which names
no ruling, so that every submodule checkout's identity probe is now repeated,
three more children; it joins the second group of amendments of ratified text,
quoting `0050f3e` design:298-301, and design Open Questions counts it (W80 M-3).
A relative `core.worktree` naming a missing directory makes the identity probe,
row 3b and `git config --unset`, run in the checkout, exit 128 with `fatal:
cannot chdir to '<value>'`, so the refusal keeps the plain message, in the plain
layout, the `.git`-file layout and a submodule checkout moved by hand, and round
(i)'s "a missing one included" holds for an absolute value only, as D18's
variant sentence and round (i)'s entry now say (W80 L-2, W81 M-1); this round
found on Git 2.43.0 that `git config --file` fails the same way in the checkout
and clears the setting when run outside the repository. A toplevel that holds
one line feed, with its common directory under it, prints four lines, not three,
in design D6 and round (i)'s entry (W80 L-3). D18's relative path resolves the
same way from any directory, not only from the root, and round (i)'s "the remedy
in every form" reads "the remedy wherever the refusal prints" (W80 L-4). D18 no
longer says that a submodule checkout keeps the plain message because it is
excluded first: one keeps it only where its own configuration redirects nothing,
while one whose module's `config` sets `core.bare` true, or a `core.worktree`
naming another directory, a sibling submodule's checkout among them, takes the
variant and, after the remedy, is refused again with the plain message, as does
a copy of a checkout whose gitfile names the module take the variant, known
limits that D18 records and round (i)'s entry reflects (W80 L-5, W81 L-1). By
the lead's R-299, on lane openRepoProject-4's finding that two readers took it
for a cut-off clause, the THEN line of the scenario "A work-tree probe at
revalidation" ends "since the probe's two lines are read as one path, which is
D's", where round (j)'s wording ended "the probe's two lines being read as one
path, D's", its meaning unchanged. The delta edits are the AND clause of the
scenario "A removal past the hard ceiling", in `Clean can explicitly retire
verified worktrees`, and that THEN line, in `Cleanup revalidates destructive
actions`; F-1's three texts and F-2's text are unchanged, byte for byte, and the
scenario counts stay 71, 22 and 24. This round's commit also re-wrapped the
lines after each of its edits, up to where the old line breaks resume, with no
other change of words (Capabilities `:55`; Decisions, amendments; this list;
design Context, D4, D6, D18, Open Questions; `tasks.md` 1.2; the deltas' `Clean
can explicitly retire verified worktrees`, its scenario "A removal past the hard
ceiling", and `Cleanup revalidates destructive actions`, its scenario "A
work-tree probe at revalidation").

Round (l), lane openRepoProject-3's W87 confirm read of rounds (j) and (k) at
`173d83c` (HIGH 0, MEDIUM 1, LOW 3, observations 5; validate 9 of 9, the
scenario counts 71, 22 and 24, every item of W70 and W80 applied or declared),
under the lead's R-307 and R-310. Where Git cannot stat a worktree's path, `git
worktree prune` deletes that live worktree's administrative directory, as R-284
found for a `.git` file one stage later, yet the ratified next step of an
`inspection-error` row and the plan's `inspection-incomplete` remedy, in its
plain form and in round (h)'s variant, named it for a row whose planning `lstat`
failed, and feature 004 at `3bc1d68` printed that remedy in report mode (W87
M-1). Design D18 now gives five texts, put to Brett Heap to confirm, as R-284's
was (he confirmed them on 2026-10-22, "R-307: yes; R-310: yes", the lead's
R-319, round (m), which moved their amendments entry to the first group): the
next step of such an `inspection-error` row, and the plan's remedy in its plain
form and in its redirect variant, each leaving `git worktree prune` out and the
remedies adding that a row's path could not be read, the unread forms taking
precedence wherever any row of the plan has such a path, a row whose `lstat` the
deadline stopped included; and, since `git worktree prune` acts on the whole
repository (R-310), the next steps of the other `inspection-error` rows and of
the `registration-mismatch` rows, which drop it too while any row of the plan
has such a path. The amendments list, second group, quotes them in an entry of
its own beside the `0050f3e` sentences they qualify, design:757-758 and
design:775-777, and design Open Questions counts it; the delta states the rule
as an AND clause of the scenario "An unreadable worktree is one row",
pcl:836-840's "as the cause fits" governing it; and What Changes names it. D7
and round (j)'s entry no longer present the evidence model's sentence as R-291's
words, a composite that no record holds: it is the lead's R-287, with R-291's
refinement, which the evidence model words so (W87 LOW-1). Design D18 says that
under a `core.bare` true a bare name that finds a directory holding a
`.project.json` file or a `.devcontainer` directory is taken by `discover()`
after row 2 fails, and the variant prints, where it said that the run is refused
with `repository-not-found` (W87 LOW-2, in report mode on Git 2.43.0 and
2.36.6). Design D18 also says that the locked note is the report row's own form,
that a ceiling target shows the first, the second or the third note, and that
the first on a locked target fails safe, Git refusing `git worktree remove
--force` while the worktree is locked; round (k)'s precedence sentences, in D18,
D4 and the F-2 and R-284 entries, now read so, and the third note's words are
unchanged (W87 LOW-3). The RI-3 departures entry, and round (j)'s mention of it,
cite `BA:725-727` for the quote whose first word ends at `BA:725` (W87 OBS-1),
and LQ-13's lane parts name R-146, the drain line's naming of the gates' reasons
(W87 OBS-3). F-1's three texts and F-2's text are unchanged, byte for byte, and
the scenario counts stay 71, 22 and 24. This round's commits also re-wrapped the
lines after each of their edits, up to where the old line breaks resume, with no
other change of words (What Changes; Decisions, departures and amendments; this
list; design Context, D4, D7, D18, Open Questions; `tasks.md` 1.2; the delta
`Clean reports local worktree state`, its scenario "An unreadable worktree is
one row").

Round (m), Brett Heap's two rulings of 2026-10-22, on round (l)'s five texts and
on lane openRepoProject-3's W86 NM-1, with the recording of one open question,
at `ccc52b9` (validate 9 of 9, the scenario counts 71, 22 and 24), under the
lead's R-319 and R-321. In his words "R-307: yes; R-310: yes" (R-319) he
confirmed the five texts, three next steps and two remedies that round (l) put
to him, as R-284's third text was confirmed: the next step of an
`inspection-error` row whose path could not be read and the plan's
`inspection-incomplete` remedy in its plain form and in its redirect variant
(R-307), and the next steps of the other `inspection-error` rows and of the
`registration-mismatch` rows while any row of the plan has such a path (R-310).
Their amendments entry, "No prune advice where a row's path could not be read",
moves from the second group of amendments of ratified text, on lane rulings,
waiting on his ratification of #19, to the first, on his own words of
2026-10-22, beside those of F-2, F-1, O-1 and R-284, its `0050f3e` quotes and
its texts unchanged, byte for byte, and its last sentence saying that he
confirmed them; the first group's heading line names his words, and the second
group keeps five entries, the line-feed exception, the submodule next steps, the
cap's re-run, the count split and the identity probe's line count. What Changes,
round (l)'s entry, which gains a clause and is otherwise history, design D18 and
design Open Questions now say that he confirmed them. In his words "R-320: yes"
(R-321) he ruled the lead's proposal on W86 NM-1, which lane openRepoProject-4
relayed: `git worktree prune`, run for a stale entry's sake, deletes the
administrative directory of a worktree whose path Git cannot stat too, on Git
2.43.0 and 2.36.6, so that while any row of the same plan has such a path, the
recommendation of a `stale-worktree` row and the locked form of it leave prune
out and warn against it, and the `inspect-cap` remedy, whose rows past the cap
are never read, always does. The amendments list's first group gains an entry of
its own for the three texts, quoting `0050f3e` design:777-779 and design:759-760
and the ladder's `project:568`; design D18 states them beside the sentences they
qualify; the delta `Clean bounds its Git work and reports omitted work` states
the cap remedy as an AND clause of its scenario "Row cap and planning failures",
the only edit of a delta, which changes no requirement's text; and What Changes
names them. No delta lists the stale recommendation, the baseline report's text,
so none states it; W52's F-10, which round (g) left to feature 004, is named by
D18 only for its locked form, which takes the second of the two recommendations
where a path could not be read. One question stays open and is recorded in
design Open Questions, in the lead's words, before Brett Heap and not ruled:
F-1's (b), "inspect, then git worktree prune and delete PATH by hand", can print
in single mode for a ceiling-cut P beside a row whose path could not be read,
and whether it should carry the same warning there (from R-310); no text it
names changes. Round (l)'s five texts, F-1's three texts and F-2's text are
unchanged, byte for byte, and the scenario counts stay 71, 22 and
24. This round's commit also re-wrapped the lines after each of its edits, up to
where the old line breaks resume, with no other change of words (What Changes;
Decisions, amendments; this list; design Context, D18, Open Questions;
`tasks.md` 1.2; the delta's `Clean bounds its Git work and reports omitted
work`, its scenario "Row cap and planning failures").

Round (n), lane openRepoProject-3's W91 confirm read of round (l) at `ccc52b9`
(HIGH 0, MEDIUM 2, LOW 1) and W95 confirm read of round (m) at `20084cd` (HIGH
0, MEDIUM 1, LOW 3), under the lead's R-341, with Brett Heap's answer of
2026-10-22 to the one question that the lead's R-324 put to him, "R-324: yes"
(the lead's R-343) (validate 9 of 9, the scenario counts 71, 22 and 24). The
labels T1 to T8 are W91's and W95's: T1 is the next step of an
`inspection-error` row whose path could not be read; T2 and T3 are the plan's
`inspection-incomplete` remedy in its plain form and in its redirect variant; T4
and T5 are the next steps of the other `inspection-error` rows and of the
`registration-mismatch` rows; T6 and T7 are the recommendation of a
`stale-worktree` row and its locked form; T8 is the `inspect-cap` remedy. The
unread forms, T1 to T7, now state one condition in the same words at every site:
any row of the plan has a path whose planning `lstat` failed other than for the
path's absence, or was cut at its budget, a row whose `lstat` the deadline
stopped included, so that its `present` is null (W91 MEDIUM-1, W95 MEDIUM-1;
held for this round by the lead's R-324). D18's definition of the unread
`inspection-error` row, which T4 and T5 refer back to, and the condition of T6
and T7, in D18 and in the entry for T6 to T8, gain the clause that T2 and T3 and
the entry for T1 to T5 already had. That entry says "stopped", as D18's remedies
and R-311 do, where it said "cut", and round (l)'s entry words the clause as the
others do. The meaning does not change: a row whose `lstat` the deadline stopped
is `present: null` either way, the requirement `Clean bounds its Git work and
reports omitted work` leaving the values of a filesystem call that the deadline
stopped null. Round (l)'s entry and the entry for T1 to T5 place the "as the
cause fits" sentence (`0050f3e` pcl:649-651) at pcl:836-840, where they placed
it at pcl:815-819, which round (l)'s own AND clause had moved (W91 LOW-A). D18,
the entry for T6 to T8 and round (m)'s entry say "plan" where they said "plan or
listing", the plain report being a plan in `mode: "report"` (W95 LOW-2). The
locked form of the stale recommendation, T7, is stated as the report row's
recommendation alone, in the human report and in `--json`, because the preview
excludes a locked stale row as `locked-worktree`, ahead of its class, so that no
preview group has it as its next step, as feature 004 at `0a82a62` builds it;
design D18 and the entry for T6 to T8 say so (W95 LOW-3). Design D18 says once
that T8's `{N}` and `{M}` stand for the row count and the cap, the ratified
remedy's `N` and `M`, which are the only braced placeholders of a text in this
change (W95 LOW-1). In his words "R-324: yes" Brett Heap ruled that every
no-prune warning, the ceiling's third text (R-284's) and T1 to T8, extends to
name `git worktree remove` and `git gc` beside `git worktree prune`: each ends
"so do not run git worktree prune, git worktree remove or git gc until it can",
and the cap remedy "if a worktree's path cannot be read, do not run git worktree
prune, git worktree remove or git gc until it can", every other word of the nine
texts staying (W91 MEDIUM-2 and W95: `git worktree remove`, with or without
`--force`, deletes the administrative directory of a worktree whose path Git
cannot stat; W80 L-6 and E6: so does the automatic worktree prune of `git gc`,
once that directory's index is older than `gc.worktreePruneExpire`, three months
by default). The nine texts are edited at every site that quotes them, and the
sentences that name the third text's warning with them: design D9 and D18, What
Changes, Capabilities `:55`, the amendments list's entries for R-284, T1 to T5
and T6 to T8, round (j)'s entry's quote of the third text, and the deltas `Clean
reports local worktree state` (its scenario "An unreadable worktree is one
row"), `Clean can explicitly retire verified worktrees` (its requirement and its
scenario "A removal past the hard ceiling"), `Clean records a reconcilable
result for every removal target` (its requirement) and `Clean bounds its Git
work and reports omitted work` (its scenario "Row cap and planning failures");
where the third text stands with its commands in code spans, each of the three
has its own. The first group's heading names his words, an entry of its own
records the ruling, and design D18's sentence on the third note, like round
(k)'s entry, no longer says that naming `git worktree remove` or `git gc` there
waits on his word (W80 M-1, second part, with L-6); What Changes, design Context
and Open Questions say the same. The requirements `Clean can explicitly retire
verified worktrees` and `Clean records a reconcilable result for every removal
target` change in the third recovery text alone, and the three scenarios named
above change in their ANDs; no requirement or scenario is added or removed, the
reasons that the deltas give for `git worktree prune` stand, and the scenario
counts stay 71, 22 and 24. Apart from that closing clause, T1 to T8 and the
third text are unchanged, and F-1's (a) and (b) and F-2's text are unchanged,
byte for byte; F-1's (b) beside an unread row stays open in design Open
Questions as worded. This round's commit also re-wrapped the lines after each of
its edits, up to where the old line breaks resume, with no other change of words
(this list; the amendments list; What Changes; Capabilities `:55`; design
Context, D9, D18, Open Questions; `tasks.md` 1.2; the deltas named above).

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
