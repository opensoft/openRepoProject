Lane: openRepoProject-2

# Proposal: add-project-clean-all-safe

Status: draft, awaiting Brett Heap's ratification. Nothing here is ratified.

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
executable. The packet's tables are cited here, not restated.

## Why

Finished work is retired one worktree at a time: `project clean <root>
--apply --action remove --worktree P` removes one named linked worktree per
run (`project-clean/spec.md:55-61`), each run with its own selection,
confirmation and full report. Several merged worktrees need as many runs.

Designing a batch on top of that action showed that the action itself is not
safe enough to repeat. At `da33d92`, whose `project` and tests are unchanged
since the packet's `a040790` baseline (`git diff a040790 da33d92 -- project
tests/` is empty):

- A worktree whose only change is an edit to a file flagged assume-unchanged
  is classified `merged-removable`, and `--apply --action remove` deletes it
  with exit 0, edit included. This was reproduced for this proposal on a
  scratch fixture with Git 2.43; the cause is `BA:139-142`.
- A worktree holding a submodule can be offered for removal, which Git then
  refuses with exit 128 (`BA:1263-1267`).
- The removal command does not override `status.showUntrackedFiles`, so under
  `no` Git's own cleanliness check misses untracked files (`BA:307-317`), and
  every clean, non-default worktree classifies `inspection-error`
  (`DI:1130-1134`).
- Worktree paths are parsed by line, so a newline path is misread and a
  non-UTF-8 path ends the run with an uncaught exception (`BA:1223-1224`).
- One unreadable worktree path refuses the whole repository with exit 2
  (`project:339`, `:995-1000`).
- A deleted upstream classifies `unpublished`, exactly like one never
  configured (re-run for this proposal; Corrections, C2).
- An absolute path is silently redirected by `discover` to a family holder or
  a manifest ancestor (`project:307-313`; `BA:862-869`).
- Each Git child has a fixed 15 s timeout and the run has no deadline
  (`project:60-65`).

The packet resolved these into one reviewed design (`BA`; review trail
`HO:190-353`), and issue #6 is done only when "a later OpenSpec proposal picks
the packet up as input". This change is that proposal for the batch. It goes
first because the overview's `--all-safe` suggestion exists only through the
batch's gates and refusal codes (`SY:287-306`).

## What Changes

- **`project clean <root> --all-safe` previews a batch.** It plans every
  eligible linked worktree of one resolved repository: `selected` and
  `excluded`, each exclusion with one reason in the fixed gate order
  (`BA:152-165`), both in canonical raw-byte path order, which is also the
  execution order (`BA:107-111`). Nothing eligible prints "No eligible
  worktrees" and exits 0. The spelling is `project clean <root> --all-safe
  [--json] [--apply [--yes] [--expect-plan D]]` (`BA:65-85`); `--all-safe`
  cannot be combined with `--action`, `--branch` or `--worktree`, and
  `--expect-plan` requires `--all-safe --apply`, else `invalid-arguments` and
  exit 2.
- **`--apply` removes only what its own fresh plan selected.** It always
  recomputes, prints and confirms its plan; the preview is advisory and never
  reused. `--yes` accepts the fresh plan, and the optional `--expect-plan
  <plan_digest>` refuses a plan whose digest differs with
  `plan-digest-mismatch`, before any prompt (`BA:345-379`). Targets run in
  canonical order, and the batch stops after the first target that is not a
  plain `removed`. Every local branch remains, and the result says so.
- **Eligibility is `merged-removable` plus gates.** The main-worktree,
  path-byte, two-way admin registration and lock gates, then the two index
  gates: `contains-submodule` (any gitlink, or an admin `modules` entry) and
  `hidden-local-state` (any entry flagged assume-unchanged or skip-worktree),
  read inside the row's own worktree (`BA:113-150`, `BA:629-675`, probe
  directory rule `BA:554-583`). Local ancestry is the only removal proof.
- **Single-target `remove` becomes a strict one-item batch.** Its interface is
  unchanged. It builds the same full plan (`mode: "single"`) under the same
  caps, lists every other eligible row as `not-requested`, and shares the
  seam, refusal codes, stages and exit codes of a batch whose only target is
  P; it adds `worktree-not-found` and `target-excluded`, and an inspection
  error anywhere in the repository refuses it (`BA:413-423`). `push` and
  `delete-branch` change only in argument resolution (`BA:424-425`).
- **One mutation seam, `retire_worktree(plan, target)`.** Revalidate; spawn
  the non-force `git -c status.showUntrackedFiles=normal -C <command
  directory> worktree remove <path>` in its own process group, only while the
  removal floor remains; reap; reconcile by rescan (`BA:381-411`). `project`
  never forces, never retries, and never deletes a directory itself.
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
  (stage table `BA:485-494`), a reconciliation record on every `removed`,
  `refused`, `failed` or `unknown` target, and `removed` only on rescan
  evidence, never on the exit status alone (`BA:496-526`). Exit codes follow
  `BA:528-550`, Git's own status passing through. SIGINT, deadline expiry and
  exceptions follow `BA:460-483`; SIGTERM and SIGHUP get the SIGINT treatment
  in the apply phase (Decisions, OQ-16).
- **Bounded work.** One monotonic 60 s deadline with a 10 s reconciliation
  reserve, 5 s per Git child and per filesystem call, a 5 s removal floor, a
  2 s TERM-to-KILL grace and serial probing (`BA:427-458`); caps of 128
  worktree rows and 16 targets and ignored-file bounds of 64, 4,096 and 8
  (`BA:721-814`). A cap or deadline hit is an incomplete plan
  (`inspect-cap`, `inspection-incomplete`, `deadline-exceeded`, with
  `omitted`) that blocks apply; more than 16 eligible rows is a complete plan
  refused with `target-cap`. Plans and results report `probes` and
  `operations` as `{estimated, performed}` (`BA:816-830`). The caps are
  provisional until measured (Decisions, OQ-4).
- **Git-first resolution in every `clean` mode.** The read-only report,
  `--json`, `--all-safe` and every `--apply --action` resolve their argument
  by the table at `BA:856-860`: an absolute path must be exactly a main
  worktree root, else `target-not-repository-root`; a relative path or no
  argument resolves to the repository Git finds there; only a bare name keeps
  `discover`, its Git child counted and bounded. The report's `root` names
  the command directory, and the manifest is read at `repository.root`. Bare
  repositories are refused in this MVP (Decisions, OQ-15).
- **One evidence model for `clean`, `status`, `doctor` and `update`.**
  `repo_state` and `cleanup_report` move onto the shared probe set: one
  `git --version`, four repository-wide children memoized per `common_dir`
  (identity, `worktree list --porcelain -z`, one `for-each-ref` in the shared
  format, the merged set), and one combined bounded status probe per row
  (`BA:585-652`), all parsed NUL-delimited, with the scrubbed environment of
  `BA:243-253`. The ladder keeps its names, order and text and becomes a pure
  function over evidence (OQ-28). Git 2.36 or newer is required
  (`git-too-old`, `git-unavailable`) by `clean`, `status`, `doctor` and
  `update` (OQ-23). The visible consequences are the baseline behavior
  changes (`BA:1200-1274`, plus R1 and R2), and the deltas carry each one.
- **Every `clean --json` prints one versioned envelope.** `schema_version: 1`
  with the plan fields of `BA:947-976`, `mode` being `report`, `single` or
  `all-safe` (OQ-29); refusals as `{code, message, path?, reason?}` with the
  codes of `BA:987-1015`; the extended error object when no plan can be built
  (`BA:978-985`). `--apply --json` prints the apply result record
  (`BA:1017-1042`) as the one stdout document, with the human plan, prompt
  and progress on stderr (OQ-10). The plan is not called an "additive
  superset" (OQ-24).
- **Every path is exact or excluded.** JSON carries a valid UTF-8 path
  exactly with `path_valid_utf8: true`; a non-UTF-8 path is escaped, excluded
  as `unsupported-path-bytes` and never a removal operand; human output
  prints control, bidirectional, format and undecodable characters in the
  `$'...'` form of `BA:913-939`.
- **README and tests** describe and cover all of the above (Impact).

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
- **The current and the main worktree are never removed**
  (`project-clean-review-safety/spec.md:9-13`).
- **Revalidate before every destructive action**
  (`project-clean-review-safety/spec.md:49-53`), and stop at the first
  failure: no continuation, rollback or automatic retry.
- **One repository per invocation.** Never siblings, family members, mounted
  legs, pinned member copies or independent clones (`BA:103-105`).

## What This Repository Does Not Own

- **Git's own refusals**: non-force `git worktree remove` is the last line of
  defense; this change adds a gate in front of it, never a bypass.
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
    The report comes from the shared evidence model (NUL parsing, the
    combined bounded probe, the 5 s and 60 s budgets, Git 2.36); an
    unreadable path is one `inspection-error` row with `present: null` and an
    `os-error`, not a whole-command exit 2; `ignored_files` counts ignored
    records observed, at least, beside `ignored_files_truncated`; `root`
    names the command directory. The staleness sentence (`:16`) and the audit
    scenario stay.
  - MODIFIED (`:25`):
    `### Requirement: Clean classifies preservation and cleanup actions`.
    `:27-28` names 7 classes and the ladder has 15 (`project:418-468`); the
    text names all 15 in ladder order, a deleted upstream becomes
    `remote-gone`, and unreadable, mismatched and probe-failed rows are
    `inspection-error` directly (R1).
  - MODIFIED (`:55`):
    `### Requirement: Clean can explicitly retire verified worktrees`.
    "remove one named linked worktree" (`:57`) becomes one named worktree or
    the `--all-safe` set, through `retire_worktree`, the gates and
    `-c status.showUntrackedFiles=normal`, stopping at the first failure.
    `:59-61` (branch deletion separate; never force) stay verbatim.
  - MODIFIED (`:70`): `### Requirement: Clean hands off work requiring review`.
    `:75-76` requires "explicit confirmation and action targets", and
    `--all-safe --apply --yes` names no single target, so the text defines
    `--all-safe` as an explicit action target, the set the fresh plan
    selects. The pull-request hand-off and its scenario stay.
  - Untouched (`:39`):
    `### Requirement: Clean can explicitly push safe feature branches`.
    Only argument resolution changes, carried by the first ADDED requirement.
  - ADDED: `### Requirement: Clean resolves its target Git-first`. The
    resolution table for every mode, `target-not-repository-root`, and bare
    repositories refused.
  - ADDED:
    `### Requirement: Clean previews and applies a batch of eligible worktree removals in one repository`.
    `--all-safe`, the gate order, the fresh plan, `plan_digest` and
    `--expect-plan`, and single-target removal as a one-item batch.
  - ADDED:
    `### Requirement: Clean bounds its Git work and reports omitted work`.
    The deadline, budgets, caps, `omitted`, `probes`, `operations`, `limits`
    and `budget`, and incompleteness blocking apply.
  - ADDED:
    `### Requirement: Clean records a reconcilable result for every removal target`.
    Stages, reasons, the reconciliation record, exit codes, interruption,
    and recovery.
  - ADDED:
    `### Requirement: Clean reports every path exactly or excludes it`.
    NUL parsing, `path_valid_utf8`, and the JSON and human escaping rules.
  - ADDED: `### Requirement: Clean plans and refusals are versioned JSON`.
    The `schema_version: 1` envelope for every `clean --json`, refusal
    objects, the extended error object, and the apply result record.
- `project-clean-review-safety` (all four accounted for):
  - MODIFIED (`:21`):
    `### Requirement: Cleanup preserves all local work not proven disposable`.
    Adds locked, `contains-submodule`, `hidden-local-state` (sparse checkouts
    included), `registration-mismatch`, `unsupported-path-bytes` and
    unreadable worktrees to the preserved states. Both scenarios (`:27-36`)
    stay.
  - MODIFIED (`:49`): `### Requirement: Cleanup revalidates destructive actions`.
    Removal revalidates by the targeted check against the recorded identity
    objects, refusing with `identity-changed`, `branch-changed`,
    `state-changed`, `contains-submodule` or `hidden-local-state`; push and
    `delete-branch` keep the full re-inspection (`project:508-518`).
  - Untouched (`:9`, `current` keeps its baseline meaning):
    `### Requirement: Cleanup protects the process worktree`.
  - Untouched (`:38`, push is unchanged):
    `### Requirement: Cleanup respects configured upstream mappings`.
  - ADDED:
    `### Requirement: Cleanup states a narrow guarantee and its residual window`.
    Concurrent writers outside the contract, no lock, the guarantee, the
    residual-window line, and the branch race.
- `project-command`:
  - ADDED:
    `### Requirement: Repository inspection requires Git 2.36 and shares one evidence model`.
    `status`, `doctor` and `update` read `repo_state` through `snapshot`
    (`project:681`, `:699`, `:789`, `:846`), so they share `clean`'s probes
    and refuse old or unusable Git with exit 2 and, under `--json`,
    `{"error", "code"}`.
  - Untouched: `Delegate project creation` (`:9`, which the in-flight
    `prefer-triad-in-project-new` modifies), `Inspect and diagnose` (`:22`),
    `Explicit maintenance` (`:31`) and `Distribution and compatibility`
    (`:40`).
- `project-review-safety` and `speckit-extension-integration`: untouched.
  Every `clean` refusal, `manifest-invalid` included, exits 2 with structured
  JSON, as `project-review-safety/spec.md:80-82` requires.

## Impact

- **`project`**: `clean()` gains `--all-safe` and `--expect-plan`, the plan
  builder, `retire_worktree`, targeted revalidation, reconciliation, apply-
  phase signal handling and the JSON envelope. `repo_state`,
  `cleanup_report`, `default_branch` and `discover`'s Git child move onto the
  shared bounded probes under one deadline; `probe()` gains a timeout
  argument and per-child process groups; the ladder becomes a pure function.
  `status`, `doctor` and `update` gain the Git version check. No new flag
  outside `clean`, no network, and no new dependency.
- **`README.md`**: "Clean up Git worktrees" describes the batch preview and
  apply, `--expect-plan`, the gates, the narrow guarantee and residual
  window, the result record and recovery; its sentence "Apply actions are
  always explicit and target one branch or worktree" (README:106) is
  corrected. Install (README:17-19) states the Git 2.36 requirement, and the
  exit-code line (README:194-196) gains `clean`'s codes, Git's own status
  passing through.
- **`tests/test_project.py`**: disposable-repository tests for the packet's
  35 batch scenarios (`BA:1347-1628`) as the deltas carry them; a counting
  `git` wrapper that pins each child's `-C` directory and the probe counts;
  hooks for the residual window, the branch race, deadline expiry and SIGINT;
  value-parity tests against the baseline except the listed changes. The 43
  existing tests keep passing, except an expectation a listed baseline change
  alters, which the delta names. The command is `python3 -m unittest
  discover -s tests -v`, on Linux and macOS with Python 3.10 and 3.12, as CI
  runs (`.github/workflows/tests.yml:9-18`).
- **Speckit handoff**: implementation goes to exactly one Speckit feature,
  `specs/003-<slug>/`, created by `/speckit.specify` after ratification
  (`002` is lane openRepoProject-1's `002-triad-first-project-new`). OpenSpec
  `tasks.md` holds governance boxes and that one handoff only.
- **workBenches**: `onp` carries the batch once its owner moves the pin.

## Dependencies and Sequencing

- **This change depends on nothing unmerged.** It targets the canonical
  specs at `da33d92` and the `a040790` executable. It does not depend on
  PR #2's commits (closed unmerged; harvest source only). The in-flight
  `prefer-triad-in-project-new` MODIFIES `Delegate project creation` in
  `project-command`, while this change ADDS a separate requirement there, so
  the two deltas archive in either order.
- **`add-project-overview` depends on this change.** Its `--all-safe`
  suggestion is gated by this change's gates and refusal codes
  (`SY:287-306`), and it reuses this change's evidence model, ladder function
  and Git 2.36 refusal (`SY:39-51`, `SY:78-109`). It should be ratified after
  this change, and re-aligned if this change moves before ratification.
- **Implementation order.** Feature `003-<slug>` lands before the overview's
  `004-<slug>`. Draft PR #8 (`002-triad-first-project-new`) also edits
  `project` and `tests/test_project.py`; whichever lands second merges
  `main` into its branch. Never rebase: the organisation ruleset refuses
  force pushes.

## Out of Scope

- **Paired retirement (branch deletion with the worktree).** The PR #2
  decision record (comment 6035824335, on Brett Heap's word "go with your
  recommendation", 2026-10-07) requires any future paired-retirement
  proposal to be a MODIFIED requirement on `project-clean`, "Clean can
  explicitly retire verified worktrees" (`project-clean/spec.md:55`), because
  it changes `remove` (`BA:56-63`; `HO:36-39`). Its post-removal stage
  contract is `BA:1339-1345`; harvest source `5fc2b51`.
- **Cache disposal** (`OV:144`, `OV:151-152`; `BA:1314-1337`).
- **Remote, GitHub and PR queries** (`DI:72-75`, `DI:1036-1060`; `HO:160-167`).
- **Family traversal and relationships** (`SY:34-37`; `DI:276-290`).
- **Bench, container and park integrations** (`OV:142-146`; `DI:1062-1064`).
- **`project overview`, `--attention` and the doctor repository-health
  absorption** (`acf0133`, `80fdef3`): `add-project-overview`.
- **Also excluded by the packet**: estate-wide destructive batches, merge
  or branch reconciliation, squash-merge retirement (`BA:195-199`), a lock
  or writer-quiescence protocol (`BA:1645-1650`), a persistent cache or
  resumable plan, continuing after a failure (`BA:1640-1643`), and the exact
  bench/type doctor check (`OV:148-157`, `OV:361-366`; `SY:233-235`).
- **Bare-repository support and user-configurable limits** (OQ-15, OQ-8).

## Decisions Taken by This Proposal

Each is a proposal decision, open to ratification. OQ numbers are the lane's
open-decision list; each cites the packet text that leaves it open.

- **OQ-1, one change or two**: two, batch first (this change).
- **OQ-3, revise the packet first**: no; the packet stays the PR #7 record,
  and this proposal states its readings and corrections.
- **OQ-4, measured costs** (`BA:723-724`; `OV:314-319`): not yet measured.
  Design measures warm-child and removal cost on this workstation (Git 2.43,
  WSL2) and reapplies the fit test of `BA:729-735`.
- **OQ-5, batch caps and bounds**: keep 128 rows, 16 targets, and 64,
  4,096 and 8 (`BA:966`), subject to OQ-4.
- **OQ-8, configurable limits** (`OV:332`): none; fixed values are reported
  in `limits` and `budget`.
- **OQ-9, deadlines** (`BA:427-458`, `BA:467-468`): keep 60 s, 5 s per
  child, the 10 s reserve, the 5 s floor and the 2 s grace.
- **OQ-10, `--apply --json`** (`BA:1189-1198`; `project:523-524`): allowed,
  as the packet recommends.
- **OQ-11, `--expect-plan` with `--yes`** (`BA:377-379`): optional.
- **OQ-12, relative path or no argument** (`BA:1664-1666`): resolve to the
  repository Git finds there.
- **OQ-13, sparse skip-worktree entries** (`BA:1667-1668`): not safe;
  `hidden-local-state`.
- **OQ-14, a never-populated gitlink** (`BA:1669-1671`): not removable;
  `contains-submodule`.
- **OQ-15, bare repositories** (`BA:1662-1663`): refused in this MVP with
  `target-not-repository-root`. The packet sketches support (`BA:215-226`);
  this proposal defers it.
- **OQ-16, SIGTERM and SIGHUP** (`BA:1660-1661`): the SIGINT treatment in
  the apply phase, exiting 143 and 129.
- **OQ-22, a doctor health section**: none; this change alters doctor only
  through the shared evidence and the Git 2.36 refusal.
- **OQ-23, Git 2.36 scope** (`OV:231-234`): `clean`, `status`, `doctor` and
  `update`, as the one ADDED `project-command` requirement (R6).
- **OQ-24, JSON compatibility** (`BA:949-953`): one `schema_version: 1`
  envelope for every `clean --json` (R7).
- **OQ-25, batch exit codes** (`BA:528-543`): keep Git's status passing
  through, as `project:157-162` does; the record disambiguates.
- **OQ-26, spelling** (`OV:356`): keep `--all-safe` and `--expect-plan`.
- **OQ-27, extensions**: cache, paired retirement, remote, family, bench,
  container and park each need their own change (`OV:357-359`).
- **OQ-28, the ladder** (`DI:599-600`): a pure function over evidence.
- **OQ-29, the plain report**: the same plan builder with `mode: "report"`,
  under the 128-row cap and the deadline, with `completeness` and `omitted`
  (R2).

Left to `add-project-overview`: OQ-2, OQ-6, OQ-7, OQ-17 to OQ-21, and the
overview halves of OQ-5, OQ-9, OQ-25 and OQ-26.

Readings of packet gaps:

- **R1, failed status probe on the merge-target row.** The ladder tests the
  merge-target branch before `dirty is None` (`project:421-426`), so such a
  row reads `protected-default`, while `BA:641-644` and `BA:789-790` make a
  failed probe `inspection-error`. Reading: a failed or timed-out status
  probe sets the row to `inspection-error` directly, as unreadable and
  mismatched rows already are (`DI:263-266`), so the plan is incomplete. This
  is one more baseline behavior change.
- **R2, the plain report under caps and deadline** (`BA:91-101`,
  `BA:413-419`; `OV:228-230`). Reading: OQ-29; it exits as a preview does,
  0 complete, 1 incomplete, 2 when no report can be built (`BA:547-549`).
  That is a baseline change: plain `clean` exits 0 whenever it prints today.
- **R3, the classification list**: MODIFIED `:25` names all 15 classes.
- **R4, noninteractive targets**: MODIFIED `:70` names `--all-safe` as a
  target.
- **R5, `project-review-safety`'s exit 2**: consistent with every `clean`
  refusal; its conflict is with the overview, which `add-project-overview`
  resolves.
- **R6, Git 2.36 scope** (`OV:231-234`; `BA:1241-1245`): `status` and
  `update` read `repo_state` as `doctor` does (`project:788-789`,
  `:844-846`), so all three refuse through the existing `Refused` path with
  exit 2; under `--json` the baseline `{"error"}` (`project:996-997`) gains
  `code` for these two refusals only.
- **R7, "additive superset"** (`BA:949-953`): dropped. `root`, the meaning of
  `ignored_files` and a `null` `present` are meaning changes, which the
  packet's own rule (`BA:943-945`) versions; `schema_version: 1` lists them
  against the unversioned baseline.
- **R8, the test command**: `python3 -m unittest discover -s tests -v`. A
  bare `python3 -m unittest` from the root runs 0 tests, since `tests/` has
  no `__init__.py`.

## Corrections to the Packet

The packet is not edited; these corrections bind this change.

- **C1, stale baseline sentences.** `DI:28` and `BA:30` say `origin/main` "is
  now `ca4c615`", and `OV:163` and `HO:200` that it "has since advanced to
  `ca4c615`"; it is `da33d92`. `HO:377-380` says PR #7 "is open for review";
  it merged as `da33d92`. `DI:33-35` and `BA:39-42` omit `acf0133` and
  `09af8c8`, which `OV:176-178` lists; the PR #2 decision record's harvest
  table is the authority.
- **C2, the deleted upstream.** The claim that `a040790` reports
  `unpublished` (`BA:1214-1220`; `DI:1124-1129`) rested on the packet's
  scratch checks. Re-run for this proposal at `da33d92` with Git 2.43:
  `rev-parse --abbrev-ref @{upstream}` fails, the row classifies
  `unpublished` like a never-configured upstream, and `for-each-ref` reports
  `gone`. The claim holds; the `remote-gone` rung (`project:442`) is
  unreachable for a deleted upstream today.
- **C3, doctor and `remote-gone`.** `BA:1219-1220`, `OV:210-211`,
  `SY:107-108` and `HO:296-298` say doctor reports `remote-gone`. Doctor
  classifies no worktree (`project:728-758`; `repo_state` sets only
  `stale-worktree`, `project:352`); `DI:1127-1129` is right that doctor
  "reads the same evidence". What changes there is the values its rows
  carry, which design fixes under the ADDED `project-command` requirement.
- **C4, Python 3.10.** `BA:397-398` starts the removal child with
  `Popen(..., process_group=0)`, which Python added in 3.11, while README:17
  requires 3.10+ and CI runs 3.10. The process-group requirement stands;
  design picks a mechanism available on 3.10.

## Questions Resolved by the Alignment Review

None yet. The alignment review and the council have not run; their findings
and verdicts are resolved on this change's pull request, and noted
constraints go to `clarifications.md`.
