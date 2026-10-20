Lane: openRepoProject-4

# Feature Specification: Project overview

**Feature Branch**: `005-project-overview`

**Created**: 2026-10-11

**Status**: Draft. Created before feature 004 merges, on Brett Heap's word
(below); the plan and the implementation wait for feature 004's code and for
his word.

**Input**: User description: "Realize the ratified OpenSpec change
add-project-overview: a read-only `project overview [--root D]...
[--attention] [--json] [--strict]` answers which local projects need
attention across the configured roots, with at most one gated next command
per row (opensoft/openRepoProject#10)."

**Source of truth**: `openspec/changes/add-project-overview/` (proposal; spec
deltas for `project-overview`, 12 ADDED requirements and 61 scenarios, and
`project-review-safety`, one MODIFIED requirement with 2 scenarios; design
D1 to D13; clarifications N1 to N4), ratified by Brett Heap on 2026-10-09 in
his words to lane openRepoProject-2, "ratify, merge #11 and run the runbook"
(proposal, Status; governance task 1.6), landed on main by squash as
`961c405` (PR #12). Where this summary is shorter than the deltas, the deltas
govern. Exact human text is fixed in the delta's remedy table and in design
D3, D4, D5 and D10, and is cited, never restated in another form.

**Citations**: `POD:N` is line N of the change's
`specs/project-overview/spec.md`, and `PRSD:N` line N of its
`specs/project-review-safety/spec.md`, both at `961c405`; `CMD:N` and
`CLN:N` are line N of change 1's `specs/project-command/spec.md` and
`specs/project-clean/spec.md`, at the same commit, where change 1 stands as
`0050f3e` (PR #11) landed it (Clarifications, C-37); requirement and
scenario names are the deltas' headers. Change 1,
`add-project-clean-all-safe`, is cited by requirement header under the
change's labels: [E] "Repository inspection requires Git 2.36 and shares one
evidence model" (project-command); [L] "Clean classifies preservation and
cleanup actions"; [G] "Clean previews and applies a batch of eligible
worktree removals in one repository" with "Clean bounds its Git work and
reports omitted work"; [R] "Clean resolves its target Git-first"; and [P]
"Clean reports every path exactly or excludes it" (all project-clean).
Feature 004's names for the same concepts (classifications, gate reasons,
refusal and row error codes, `omitted`, `schema_version`, exit statuses) are
used unchanged, with two exceptions the delta makes: `omitted` keeps 004's
`{count, exactness}` shape with the exactness enum extended to `lower-bound`
and `unknown`, `count` null under `unknown`, and is carried on `scan-limit`
and `deadline-exceeded` errors (POD:224-229, :646-648), and
`limits.worktree_rows` is the overview's
own 512-row cap, the batch's caps being `batch_row_cap`, `report_row_cap`
and `targets` (POD:610-617). They are cited from
`specs/004-project-clean-all-safe/` (`spec.md`, `data-model.md`,
`contracts/project-clean.md`) at `d81b3d9`, where lane openRepoProject-2's
doc rounds 3 to 5 (rulings R-39 to R-51) merged them on branch
`004-project-clean-all-safe`, as `acc822e`, `5a02c1a` and `d81b3d9`, except
EC-031 and EC-033, which cite the branch's head, and EC-002 and the
Dependencies, which cite its `project` there. That head, `96a08d4`, changes
the documents after `d81b3d9` by the tier tags, file and verify fields and
ticks of `tasks.md`, two additions to `plan.md` and its doc round 6 (rulings
R-55 to R-57 and R-59 to R-62, with the items of R-53 and R-54 that they
settle), no document differing from `6ae927f`'s but in the ticks of
`tasks.md`; its code, which changed after `a32d20b` by its T047 (`clean` as
the frozen pipeline, merged as `6fb0fb7`), by lane G's follow-up to its
evidence model (merged as `6ae927f`) and by its US1 plan lane (merged as
`2733dea`, lead ruling R-69), has its tasks T001 to T040 and T047 to T053
built (47 of 133), among them its five incremental parsers, four of which
the overview drives (Dependencies), its child handle and its one-wide
driver, with the state, phase and signal slot of its "Invocation" entity,
and its evidence model (tasks T027 to T033), merged into that branch as
`cce8dbd`; none of it is on `main`. The change pins its code citations at
`da33d92`; this spec cites no line of `project`, `README.md` or
`.github/workflows/tests.yml` as `main` has them, its only lines of feature
004's `project` being those of EC-031, EC-033 and the Dependencies at
`96a08d4`, and the plan re-pins every citation against the `main` of its day
(proposal, "Dependencies and Sequencing").

**Created before feature 004 merges**: The change creates this feature only
after feature 004 merges (proposal, Status and "Dependencies and
Sequencing"; `tasks.md` 3.1 and "Speckit Handoff"; design, "Migration Plan"
step 3; and feature 004's spec, Dependencies). Brett Heap's word, typed in
lane openRepoProject-4's pane at 2026-10-11T16:14:21Z, "lane 4 specifies 005
now", recorded by that lane as a RULED line at 16:15:00Z, moves that order
for this specify step only. The plan and the implementation still wait for
feature 004's code and for his word. Issue #10 was released by lane
openRepoProject-2 at 16:17:06Z and claimed by lane openRepoProject-4
(https://github.com/opensoft/openRepoProject/issues/10#issuecomment-6111064469).

**Relations to earlier features**: `project overview` is a new subcommand;
no earlier feature specified it. It absorbs the doctor repository health of
the closed, unmerged PR #2 (`acf0133`, `80fdef3`) as local-only, read-only
reporting, and supersedes that branch's unmerged
`project-doctor-repository-health` capability (proposal, "Absorbing Doctor
Repository Health from the Closed PR #2"). Features 001 to 003 are
untouched. Feature 004 builds the shared evidence model this feature reads
and changes `clean`, `status`, `doctor` and `update`; this feature changes
no other subcommand's output, flags or exits. The capability this feature
MODIFIES is `project-review-safety`, not change 1's
`project-clean-review-safety`: its requirement "YAML decoding errors are
structured refusals", from the archived change `resolve-pr-review-findings`,
which had no Speckit feature.

## Clarifications

Each entry settles a point from the change's own text, cited; none
re-decides what the change decided. `DI:N` is line N of the packet's
discovery document at `da33d92`, as the change cites it. The questions that
text leaves genuinely open are in `clarify-questions.md`, for Brett Heap,
unanswered; when he answers, his answers join this section as a later
session.

### Session 2026-10-11

- **C-1** Q: Is a root itself a candidate, or only its immediate entries? ->
  A: The root itself too. Discovery "SHALL examine each root and its
  immediate entries only" (POD:18-19; the packet, adopted by the proposal,
  says "Discovery examines each root itself", DI:117), the marker table
  deciding for the root as for any entry, and the README's check of one
  project is `project overview --root <dir>` (proposal, Impact, README). A
  root on which no marker holds is still listed and adds no row. Where
  applied: US1 s8; FR-002.
- **C-2** Q: Does a Git child that the overview stops at a record bound
  count as a failed or timed-out probe? -> A: Not when it is reaped. A probe
  stopped at its bound is a complete outcome, never `probe-failed` ([E],
  "Combined probe"; design D1, "a deliberate early stop that records
  nothing"; change 1's design D2, `complete-at-bound`; feature 004's data
  model, "Driver outcome"), and its end through the overview's own SIGTERM
  is not "a Git child exits nonzero" (POD:333). The stopped child still gets
  SIGTERM to its group and SIGKILL 2 s later, and one not reaped within the
  further 2 s is abandoned and recorded `probe-timeout` (POD:172-176; [E],
  "Termination"); that row's classification is then the one `project clean`
  gives the same row (POD:383-386). Where applied: EC-019; FR-011.
- **C-3** Q: What does `PROJECTS_DIR` hold, and is an empty value a root? ->
  A: One directory, read as the command's existing projects-directory rule
  reads it, an empty value counting as unset so that the defaults apply
  (proposal, What Changes, "Discovery is bounded and local"; DI:103-104,
  "exactly as" that rule selects them). A set `PROJECTS_DIR` naming a
  missing directory is an `environment` root reported `unreadable`
  (POD:43-45). Where applied: FR-001.
- **C-4** Q: Does a candidate with no `.git` entry (a manifest-only project,
  or a directory marked by `.project.json` or `.devcontainer`) get Git
  probes or an error? -> A: Neither. `probes.estimated` counts an identity
  probe only per Git candidate (POD:250); a family holder gets Git probes
  only when its own directory is a Git toplevel, and otherwise null Git
  fields, status `ok` and no error (POD:38-39, :66; DI:284-287); the
  manifest of a row without Git is read at the candidate (POD:319-321); and
  the absorption table rules that "no Git checkout" gives a row with null
  `repository` and `git` and no finding (proposal, "Absorbing Doctor
  Repository Health from the Closed PR #2"). Where applied: FR-004.
- **C-5** Q: Is any Git child of the overview exempt from the protocol pins
  or the environment scrub, as `clean`'s push child is? -> A: No. Every Git
  child carries the seven protocol pins and runs with the seventeen names
  removed, `GIT_ALLOW_PROTOCOL` included (POD:200-215; R-23, R-25). Feature
  004's exception (lead ruling R-28; LQ-3, draft PR #19) covers `clean`'s
  push child alone, and the overview starts no push (feature 004,
  `contracts/project-clean.md`, "Git children"). Where applied: FR-016;
  US10.
- **C-6** Q: May a test rely on a running filesystem monitor to hold a
  status probe, as the packet's fixtures did? -> A: No. [E] pins
  `core.fsmonitor=false` and `core.untrackedCache=false` on every status
  probe (change 1's D11), so the packet's fixtures at DI:1233-1237 (the
  probe timeout) and DI:1249-1254 (bounded concurrency) hold nothing; design
  D13's fixture rewrite holds the status probe with the counting `git`
  wrapper instead. Where applied: FR-049; US6 s4 and s9.
- **C-7** Q: Which capability does this feature modify, and in what order do
  the two changes archive? -> A: `project-review-safety`, one MODIFIED
  requirement ("YAML decoding errors are structured refusals"), not change
  1's `project-clean-review-safety`; and change 2 archives after change 1
  (proposal, Capabilities; design, Migration Plan step 5). Where applied:
  FR-023; Dependencies.
- **C-8** Q: Does a squash-merged branch count as merged? -> A: Not under
  the ratified [L]. A squash merge never puts the tip into the merge
  target's ancestry; change 1's open question 2 (the lane's LQ-2, a local
  patch-equivalence proof) is still before Brett Heap, with the lead's
  recommendation of a follow-on change, and is deferred to it; until he
  rules, ancestry alone proves a branch merged, and the overview would
  inherit any ruling through [L], a contrary ruling amending the changes and
  this spec first (EC-013) (design, Open Questions; proposal, Open
  Questions; feature 004's spec, EC-001 and Assumptions). Where applied:
  EC-013.
- **C-9** Q: What does a `scan-limit` error's `limit` hold for each cap, and
  how is the root cap reported? -> A: The cap's `limits` key, as the
  scenarios spell three of them (`candidates`, `root_entries` and
  `worktree_rows`; POD:258, :263, :269) and the packet defines `limit` ("a
  key of `limits`", DI:824-825), so `roots` for the root cap, whose dropped
  roots have state `omitted` and an exact count (POD:268, :623). Where
  applied: FR-017.
- **C-10** Q: Is a merge-target checkout whose status probe failed
  `protected-default`, or `inspection-error`? -> A: `inspection-error`, set
  directly as [L] defines it on that branch too, with that code's repair
  finding of severity error and none of the default-branch findings
  (POD:739-742; proposal, Corrections, "A failed status probe on the
  merge-target branch"; design D4). Where applied: FR-041; US9 s4.
- **C-11** Q: How does a gated finding's message carry its own text and the
  remedy within 200 characters, and what does `<repository parent>` name? ->
  A: Its own text, then `; `, then the remedy; when both do not fit, the own
  text is shortened with `...` and the remedy kept whole. N and M are read
  from the repository's row count and from `limits` when the message is
  built, and `<repository parent>` is the parent directory of
  `repository.root`, printed by [P]'s rules (design D5). Where applied:
  FR-035.
- **C-12** Q: What time does a finding's `observed_at` hold? -> A: The time
  at which its deciding probe completed, RFC 3339 UTC; the envelope's
  `observed_at` is the collection start (POD:610; proposal, What Changes,
  adopting DI:724-819's fields and types; DI:727, :818). Both are
  timestamps, which the comparison across concurrency excludes
  (POD:244-246). Where applied: FR-037.
- **C-13** Q: Where do the project row's `git` values come from? -> A: From
  the evidence already held for the checkout at the row's `path`, with no
  probe of its own (POD:630-631; the probe count of POD:129 and :248-254 has
  no term for it), null where nothing was established, except
  `tracking_freshness`, which is never null (POD:631; Clarifications,
  C-32). Where applied: FR-036.
- **C-14** Q: When a row's findings are gated differently, which gate does
  the human `next` line name, and which remedy shows over both row caps? ->
  A: The first code, in the gate table's order, among the findings whose
  suggestion fed the row's command or would have; it reads `withheld` for a
  withholding code and `limited` for `target-cap` and for `inspect-cap` over
  the report's row cap; a repository over both caps shows the batch remedy
  as withheld, and its read-only findings carry the report remedy in their
  own messages (design D10). Where applied: FR-045.
- **C-15** Q: For the `unpublished` default-branch finding, which remote
  holds "a remote copy of the merge target"? -> A: Any: a
  `refs/remotes/<remote>/<name>` record for the merge target's name, with at
  least one path component as `<remote>`, or the `origin/HEAD` symref's own
  target when the merge target came from it; a remote whose name contains
  `/` can set the flag for another remote's branch, erring toward a warning
  (design D9; EC-011). Where applied: FR-015, FR-041.
- **C-16** Q: The packet allows 62 s for a run cut by the deadline; which
  bound holds? -> A: 64 s plus rendering: the 60 s deadline, then up to 2 s
  from SIGTERM to SIGKILL and up to 2 s of reap wait before abandonment
  (design D13 and D1; P6-1). Where applied: FR-011; US6 s8.
- **C-17** Q: Is the JSON independent of timing in every run? -> A: Only in
  a run in which no child, task or root listing reaches its budget and the
  deadline does not expire; a cut run reports each cut with `omitted` and
  its exactness, and what it selected may depend on timing (POD:243-246;
  proposal, Decisions, "Determinism scoped"). Where applied: FR-019; SC-007.
- **C-18** Q: Does Brett Heap's ruling of 2026-10-09, that local ancestry
  outranks `remote-gone`, change the merge-target checkout's `remote-gone`
  finding? -> A: No. That finding reads the checkout's own upstream, not the
  ladder, and stays a preserve warning (proposal, Decisions, "Local ancestry
  outranks a deleted upstream"; design D4). Where applied: FR-028, FR-041.
- **C-19** Q: When several candidates reach one repository, which gives the
  row its `path`, `kind` and `name`? -> A: `path` is `repository.root`, or
  the candidate when that is null; `kind` is that of the candidate whose
  path equals `path`, else of the canonically first candidate that reached
  the repository; `name` is the manifest name at `path`, else its directory
  name (POD:625; design D7). Where applied: FR-010.
- **C-20** Q: Does `--attention` show a row whose only finding is
  informational but suggests the read-only command, such as
  `locked-worktree`? -> A: No. It shows a row only for a scan error, an
  error status or a repair, preserve or housekeeping finding, and hides
  informational findings (POD:466-469); `locked-worktree` is informational
  (POD:448). The JSON, the summary and the exit are unchanged (POD:469-471).
  Where applied: FR-030.
- **C-21** Q: May this feature be specified before feature 004 merges? -> A:
  The specify step only, on Brett Heap's word typed at 2026-10-11T16:14:21Z,
  "lane 4 specifies 005 now"; the plan and the implementation still wait for
  feature 004's code and for his word (header; change `tasks.md` 3.1 and
  Speckit Handoff). This one rests on his word, not on the change's text.
  Where applied: Dependencies.

### Session 2026-10-18

Settled at the merge of `main` at `e9d6711` and the re-pin of feature 004
to `66d60b6`. It answers no question of `clarify-questions.md`; those stay
open for Brett Heap.

- **C-22** Q: What does a branch reflog read decide at its two bounds? ->
  A: Change 2's own text decides both. A read not finished within the
  filesystem budget leaves its row unprobed for the gate, recording
  `probe-timeout` or `deadline-exceeded`, and never makes it
  `inspection-error` (POD:521-524; design D5), as feature 004's data model
  also reads it at `d81b3d9` (its plan review, M5). The read asks for at
  most 64 KiB (POD:503-504), and a reflog "read to its 64 KiB bound" is
  `reflog-unavailable` (POD:516-517; design D5, "the 64 KiB bound reached",
  and D8, a "bound-reaching file"): a read that returns 65,536 bytes has
  reached that bound, so a reflog of 65,536 bytes or more is
  `reflog-unavailable` and one of 65,535 bytes is decided by its entries.
  Lane openRepoProject-2's ruling R-33 concurs for feature 004: its data
  model at `d81b3d9`, "Reflog anchor and movement", carries it in its text
  and in its table of outcomes, which reads `reflog-unavailable` where the
  read reached its 64 KiB bound (65,536 bytes read). Its task T059 names
  R-33 in place of plan review m10, and its T066 reads the bound as R-33
  does. Its EC-005 now reads the same: "A reflog of 64 KiB (65,536 bytes)
  or more, about 300 entries, is `reflog-unavailable`" (R-33). Where
  applied: FR-033; FR-049; EC-009.

### Session 2026-10-19

Settled from the change's text, and change 1's shared evidence model, while
applying three read-only reviews of `3d28710`. It answers no question of
`clarify-questions.md`; the points those reviews found the change leaves
open are added there as Q6 to Q13, for Brett Heap, unanswered.

- **C-23** Q: What is a worktree row whose `lstat`, `.git` file read or
  administrative `gitdir` read fails, or does not finish within its budget
  or before the deadline? -> A: `inspection-error`, set directly (a missing
  or non-regular `.git`, and a missing administrative `gitdir` file, are a
  disagreement and not a failed read: FR-007, C-26). [L] sets every row
  "whose evidence could not be established (a path that cannot be read, a
  registration that disagrees, or a status probe that failed or timed out)"
  to `inspection-error` directly (CLN:114-116); a filesystem call cut by its
  budget records `probe-timeout`, or `deadline-exceeded`, and leaves its
  values null (POD:183-190; CLN:773-776; design D8); and no status probe
  runs where the worktree's identity was not verified (CMD:124-126;
  POD:94-95). The row's repository is then refused as
  `inspection-incomplete` by [G] (CLN:800-803), so the overview withholds
  `--all-safe` there (POD:526-529; design D5, "an unreadable path"). Where
  applied: FR-007; FR-034; US6 s5.
- **C-24** Q: When the manifest read at `repository.root` (or at the row's
  `path`) fails, is refused, or does not finish, may merge-target
  resolution fall back to `origin/HEAD`, `main` or `master`? -> A: No. A
  refusal ends that candidate's collection at the manifest step, leaving
  `merge_target`, `git` and `worktrees` null (POD:318-324; the scenario "One
  helper failure is isolated", POD:349-352); a cut read leaves the
  manifest's values null (design D8), and null means unknown, never absent
  (POD:652-653), so absence of a `tracking_branch` is not established, as
  for a failed ref listing (POD:368-373). Where applied: FR-025.
- **C-25** Q: What is a worktree's `current`? -> A: True exactly when the
  overview's working directory lies inside the worktree, its baseline
  meaning (DI:425-427, adopted with DI:724-819 by the proposal, What
  Changes), from one bounded task at start that takes the working
  directory's realpath (design D8), and null when `present` is null
  (DI:778). A working directory whose realpath cannot be established is
  question Q7 of `clarify-questions.md`. Where applied: FR-013; FR-026.
- **C-26** Q: Which findings does a row whose registration disagrees carry,
  and what does it do to the exit? -> A: One `registration-mismatch` finding
  (repair, warning). Every classification but `protected-default` yields its
  own finding (POD:426-428, :451-452, :460-462; DI:635), but for this row
  the `registration-mismatch` finding replaces the `inspection-error`
  finding that classification would yield, the classification staying
  `inspection-error` as set directly (POD:92-94; DI:259, :270-273,
  :671-673). The probe was skipped deliberately and not failed, so the row
  has no error and the run stays complete (DI:271-273, :684-686), and the
  finding, a warning, gives exit 0, or 1 under `--strict` (POD:465-466). The
  row's repository still withholds `--all-safe` as `inspection-incomplete`
  (DI:675-678; POD:526-529), and the `registration-mismatch` gate of FR-032
  keeps [G]'s order without deciding a `merged-removable` row. Where
  applied: FR-007; FR-032; US4 s1. (Corrected 2026-10-20 after lane
  openRepoProject-3's packet-fidelity read: DI:270-273.)
- **C-27** Q: What is a default root that exists but is not a directory or
  cannot be listed? -> A: `unreadable`, with a `root-unreadable` scan
  error, as an argument or environment root is. Only a default root that
  does not exist is `absent` (POD:42-45); the root states are a closed set
  (POD:622-624), of which only `unreadable` fits a root that exists and
  cannot be listed; and "Incomplete is visible" (proposal, "Rules This
  Change Keeps"). A default root is canonicalised first (POD:14-16), so a
  dangling symbolic link names a path that does not exist and is `absent`.
  Where applied: FR-005.
- **C-28** Q: When does an unnamed gitfile checkout's repository start its
  second phase? -> A: Only once every candidate's identity probe has
  completed or failed, since a later candidate in canonical order may still
  name the checkout (design D3, item 3; design D6, "a third wait for that
  repository alone"), so that FR-019's independence from completion order
  holds. Where applied: FR-019.
- **C-29** Q: Must two clones' `dev` differ, as the scenario "Independent
  clones and aliases" reads? -> A: Their identities differ: the identity is
  the tuple `{root, common_dir, dev, ino}` (POD:75-76), and independent
  clones "have distinct `common_dir` identities" (design D7). The packet's
  own scenario, which the delta words as "`common_dir`, `dev` and `ino`
  differ" (POD:55), says that the `repository` tuple `{common_dir, dev, ino}`
  differs (DI:1190-1191), so a difference in the tuple is what it asks for.
  Two clones on one filesystem share `dev` and differ in `common_dir` and
  `ino`. Where applied: US1 s1.
- **C-30** Q: What exactness does the `deadline-exceeded` scan error's
  `omitted` carry? -> A: The packet's rule, as for a cap: `exact` when every
  root listing completed, as in "Invocation deadline" (POD:283), and
  `lower-bound` when a root listing was cut, since more candidates could
  then exist (POD:224-229; design D6, "each cut unit with `omitted` and
  DI:165-169's exactness"). What `limit` holds there, and whether row
  errors carry the two fields, is question Q6. Where applied: FR-012.
- **C-31** Q: Which code does a Git child record when it reaches its budget
  and is then reaped? -> A: `probe-timeout`, reaped or abandoned
  (POD:173-176; the scenario "Probe timeout", POD:271-274; CMD:171-173);
  only a child stopped at its record bound and reaped is a complete outcome
  (C-2). Where applied: FR-011.
- **C-32** Q: What does `git.tracking_freshness` hold? -> A: The text
  `local refs only; no fetch`: `git` mirrors the baseline `repo_state`'s
  top-level fields for the checkout at `path`, `tracking_freshness` being a
  string never null (DI:760-763, the packet's example at DI:961), which the
  proposal adopts with DI:724-819's fields and types (What Changes). Where
  applied: FR-036.
- **C-33** Q: Is a registered path whose `lstat` fails with "not a
  directory" present, and how does a relative `core.worktree` resolve? ->
  A: `present: false` (POD:89-91; design D3, item 4; DI:776), change 1's
  "does not exist" (CMD:144-146) reading the same; and against the git
  directory (POD:105-106; design D3, item 3). Feature 004's text at
  `d81b3d9` reads the same, under lane openRepoProject-2's ruling R-36: its
  data model, "Worktree row", gives `present: false` for `ENOENT` or
  `ENOTDIR`, and its FR-017 resolves a relative `core.worktree` against the
  git directory. FR-026's parity stands as ratified. Where applied: FR-007;
  FR-008.
- **C-34** Q: What counts as one of the overview's Git children? -> A: A
  process the overview starts, each in its own process group (CMD:98;
  design D1's registry; design D13's wrapper first on `PATH`). Processes
  Git itself starts run in that child's group, take the `-c` pins from Git,
  which passes them on in `GIT_CONFIG_PARAMETERS`, and are outside the
  wrapper's assertions and the four-child count. Where applied: FR-016;
  FR-049; SC-002; SC-005.
- **C-35** Q: What do discovery's odd entries and the rows past the
  worktree-row cap get? -> A: Only a canonical directory is examined for
  markers (POD:20-22; DI:138-142), so an entry that resolves to a file, or
  a link that dangles, is no directory and adds nothing, while a marker
  check inside a directory that fails with an error other than "no such
  entry" makes that directory an error row (POD:46-49). A row past
  the 512-row cap gets no filesystem task, the tasks being bounded at 512
  rows (design D8), so its presence, identity and registration fields stay
  null. Where applied: FR-002; FR-018.
- **C-36** Q: What is N in `Scanning N roots...`? -> A: The number of roots
  given, or the defaults, before canonicalisation: the notice is written
  after the version check and before listing (design D10), and
  canonicalisation and deduplication happen inside each root's listing task
  (design D2). Where applied: FR-046.

### Session 2026-10-19, checklist run

Settled from the change's text, and change 1's shared evidence model, while
evaluating this spec against the checklists of the no-argument
`/speckit.checklist` run (`checklists/`). It answers no question of
`clarify-questions.md`; the points the run found the change leaves open are
added there as Q14 and Q15, for Brett Heap, unanswered.

- **C-37** Q: What do `CMD:N` and `CLN:N` cite? -> A: Line N of change 1's
  spec deltas: `CMD` its `specs/project-command/spec.md`, which holds [E],
  and `CLN` its `specs/project-clean/spec.md`, which holds [L], [G], [R]
  and [P]. They are read at `961c405`, as `POD:N` is, where change 1 stands
  as its squash merge `0050f3e` (PR #11) landed it, no later commit having
  touched it. Where applied: header, Citations.
- **C-38** Q: What does the 5 s filesystem budget bound: one call, or one
  task? -> A: One bounded task. Every filesystem call "SHALL run in a
  bounded task", whose miss is recorded "for its root or row"
  (POD:183-189); the proposal fixes "5 s per child and per root listing"
  (Decisions, OQ-9); and design D2 and D8 make a root's canonicalisation,
  deduplication `stat`, listing and marker and holder checks one task, each
  worktree row's `lstat` and registration reads one task, and each manifest
  read, branch reflog read and the working directory's realpath a task of
  its own. A root is therefore cut at 5 s as a whole, as "A root on a hung
  mount" reads (POD:303-306). Where applied: FR-013.
- **C-39** Q: What are the main worktree's `admin_id` and registration
  check? -> A: `admin_id` is null, and the main worktree has no
  administrative registration to check. The two-way check is a linked
  worktree's, whose `.git` file names `<common_dir>/worktrees/<admin_id>`
  (CMD:139-144), and the packet the proposal adopts for rows and fields says
  "The main worktree has `admin_id: null`" (DI:241-246, :775; proposal, What
  Changes, adopting DI:230-274 and DI:724-819). The main worktree's identity
  is its `dev` and `ino` from `lstat` (DI:382-384), so FR-007's two
  registration cases apply to linked worktrees only. Where applied: FR-006;
  FR-007.
- **C-40** Q: What do the `summary` counts hold, and when is each row field
  null? -> A: What the packet's JSON contract says, which the proposal adopts
  with its fields and types (What Changes, "A versioned JSON envelope",
  DI:724-819), except where the delta, design D11 or this section changes
  it (the validity flags, `ignored_samples` objects, `omitted`'s exactness,
  a cut task, C-23, and rows past the cap, C-35). `projects` counts project
  rows, error rows included; `repositories` the distinct repositories whose
  identity was established; `worktrees` the worktree rows of every project
  row, main worktrees included; `errors` row errors plus scan errors; and
  `findings` the findings keyed `repair`, `preserve`, `housekeeping` and
  `informational` (DI:792-800). Each worktree-row field is null exactly in
  the case its "Null when" column names (DI:770-790), and the `git` object's
  fields follow the same rules for the checkout at `path` (DI:760-763). The
  nulls that mean none, an observation and not an error, are those the
  proposal names: `upstream`, `ahead` and `behind` with no upstream
  configured, and `merged_into_target` on a detached head (proposal, Rules
  This Change Keeps, "Unknown is never healthy"). Where applied: FR-036;
  FR-037; Key Entities, Summary.
- **C-41** Q: Which codes may a row error or a scan error carry in schema
  version 1? -> A: The collector table's eight (`manifest-invalid`,
  `refused`, `os-error`, `undecodable-output`, `internal-error`,
  `probe-failed`, `probe-timeout` and `deadline-exceeded`; POD:326-335),
  `scan-limit` on a row or scan error (POD:222-224, :233-234) and
  `root-unreadable` on a scan error (POD:43-45), as the packet lists them
  (DI:838-839); the delta names no other, and its enums are closed within a
  version (POD:655-656). The exit-2 error object's codes are FR-039's.
  Where applied: FR-022.
- **C-42** Q: Which manifest states let merge-target resolution go past
  the manifest? -> A: A manifest shown absent, and one read with no
  `tracking_branch` or with one that names no local branch. [R] takes "the
  first of these candidates that exists as a local branch" (CLN:482-485),
  the manifest's `tracking_branch` being only the first candidate, and the
  delta resolves "in the order that" [R] "defines" (POD:359-360). Only a
  read that failed, was refused, timed out or was cut stops resolution
  (C-24). Where applied: FR-025.
- **C-43** Q: In what order does the human report print rows, findings,
  row errors and `Incomplete:` lines? -> A: In the JSON document's order
  (FR-037): output "is rendered after collection in canonical order"
  (design D6), and the `Incomplete:` lines follow "in the JSON's order"
  (design D10). Where applied: FR-045.
- **C-44** Q: When does a row print a `next` line? -> A: Only "when the row
  has a suggested command or a gate decided it", the line reading `none`
  where a gate left no command (design D10). A row with neither, such as one
  whose root `unsupported-layout` or `main-worktree-missing` left null with
  no gate code (FR-035), prints none. Where applied: FR-045.
- **C-45** Q: Over what does `target-cap` count? -> A: One repository. The
  gates are computed "Per repository" (design D5), `target-cap` applies
  "when more `merged-removable` findings still carry `--all-safe` than
  `limits.targets`" there (design D5), the batch's target limit being per
  run of one repository's plan (CLN:791-793, :807-811), and the scenario
  builds it in "one repository" (POD:579). Where applied: FR-034.
- **C-46** Q: Which rows count toward `inspect-cap` and
  `suggestion_gate_rows`? -> A: Every registry entry of the repository, the
  main worktree and the rows with `present: false` included, within the
  overview's 512-row cap or past it: design D5 counts "the registered rows,
  `present: false` included" and makes `suggestion_gate_rows` "the
  repository's registered row count", as [G] counts "every registry entry
  ..., the main worktree and missing rows included" (CLN:791-794). Where
  applied: FR-034; FR-035.
- **C-47** Q: What does "best-effort" mean for `Cancelled.`, the scanning
  notice and the other human writes to standard error? -> A: The write is
  attempted once and an `OSError` from it is swallowed, changing neither
  the output nor the exit status: `Cancelled.` "is written to stderr with
  any `OSError` swallowed" (design D1), and "Every human write to stderr
  swallows `OSError`" (design D10). Where applied: FR-044; FR-046.
- **C-48** Q: From when does SC-005's 64 s bound count? -> A: From the
  moment the deadline is set, as FR-011 states: the 60 s deadline is "set
  before any root is listed" (POD:167-168), and the bound is that deadline,
  2 s from SIGTERM to SIGKILL and 2 s of reap wait (design D13; C-16), so the
  time a process spends starting before then lies outside it. Where
  applied: SC-005.
- **C-49** Q: What migrates, and how is the feature rolled back? -> A:
  "Nothing migrates for users", `project overview` being new and no other
  subcommand changing; and rollback is a revert of feature 005's merge, "no
  data, configuration or other subcommand" depending on the overview
  (design, Migration Plan). Where applied: Assumptions.
- **C-50** Q: What does default-branch health report when no worktree has
  the merge-target branch checked out? -> A: Nothing for that branch. Its
  findings are added "For a checkout that" [L] "classifies
  `protected-default`" (POD:725-727), and with no such checkout none is,
  while the row's `git` object describes the checkout at the row's `path`
  (FR-036). Where applied: EC-026.
- **C-51** Q: Can `dev` or `ino` exceed what every JSON consumer reads
  exactly? -> A: Yes. They are JSON integers (POD:650), exact in the
  document, and some filesystems report values above 2^53, which a consumer
  that reads JSON numbers as IEEE 754 doubles rounds. The overview keys its
  rows on the exact values. Where applied: EC-027.
- **C-52** Q: Does a worktree row's `branch` tell a detached head from a
  branch named `detached`? -> A: No. `branch` is `"detached"` for a
  detached head (POD:633-634), the meaning of the clean report at `a040790`
  that the packet keeps (DI:765-766), and Git accepts `detached` as a branch
  name. Where applied: EC-028.
- **C-53** Q: What does a repository with thousands of loose refs do to a
  run? -> A: Its ref listing can pass the 5 s per-child budget: governance
  task 2.1 measured `for-each-ref` over 10,000 loose refs at 8.65 s on a
  cold cache, "a `probe-timeout` and an incomplete run, never a wrong one"
  (change `tasks.md` 2.1). Where applied: EC-029.
- **C-54** Q: What becomes of a candidate whose `.git` file names a bare
  repository, as in the layout that keeps one in a `.bare` directory beside
  its linked worktrees? -> A: Its identity probe fails. The probe asks Git
  for the toplevel (design D3, citing change 1's identity probe,
  `--show-toplevel`), which a bare repository has none of: on Git 2.43.0
  the probe exits 128 with "this operation must be run in a work tree",
  reproduced for this record. "A Git child exits nonzero" is `probe-failed`
  on the candidate's row (POD:333), and the repository's worktrees are not
  listed. Whether to report such a repository otherwise is question Q14 of
  `clarify-questions.md`. Where applied: EC-030.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - See every local project in one report (Priority: P1)

A person with dozens of repositories under their projects directory runs
`project overview` and reads one row per project, each with its absolute
path, each repository once however many of its worktrees sit under a root
or elsewhere, with every registered worktree listed under it. Today
`status`, `doctor` and `clean` each inspect one selected project, and the
person correlates them by hand (proposal, "Why").

**Why this priority**: It is the change's purpose, the packet's question
"Which of my local projects needs attention?" (issue #10).

**Independent Test**: In a temporary root, build independent clones, a
symbolic-link alias, a family holder and a repository with linked worktrees
inside and outside the root; run human and `--json` with networking
disabled and before-and-after snapshots, as every story's fixtures run
(FR-040), and check the rows, the worktree rows and the probe count.

**Acceptance Scenarios**:

1. **Given** clones of one origin at `atlas` under root A and at `atlas`
   under root B, and a symbolic link `atlas-link` in A to its `atlas`,
   **When** both roots are given with `--root`, **Then** there are exactly
   two `atlas` rows whose repository identities differ, with distinct
   `common_dir` and `ino` and a `dev` that differs only where the two roots
   lie on different filesystems (Clarifications, C-29; the packet's own
   scenario says that the `repository` tuple `{common_dir, dev, ino}`
   differs, DI:1190-1191, where POD:55 lists the three fields), the link
   adds no row, and each human row prints its absolute path.
2. **Given** a root holding `acme/acme/family.yaml` in a Git toplevel that
   declares members at `acme/web` and `acme/api`, plus an ordinary
   repository `tools`, **When** the overview runs, **Then** there are
   exactly two rows, a `family-holder` at `acme/acme` and `tools`,
   `summary.projects` is 2, `relationships` is `[]`, no row and no Git
   child exists for either member, and the holder's repository-wide probes
   run once and belong to its row; without `acme/acme/.git` the holder row
   has null `repository`, `merge_target`, `git` and `worktrees`, status
   `ok`, no error and no Git child; and with `acme` itself as the root,
   `web` and `api` are ordinary rows of their own and `relationships` stays
   `[]`.
3. **Given** a repository with a main worktree and three linked worktrees,
   one an immediate entry of the root and one outside every root, **When**
   the overview runs, **Then** there is one project row with four worktree
   rows, main worktree first and then by path bytes, the external worktree
   adds no project, the identity probe, the registry, the ref listing and
   the merged-set query run once for the repository, each present row gets
   one status probe, and `probes.performed` is one version check, plus one
   identity probe per Git candidate, plus three, plus four; when the main
   worktree lies outside every root, so that a linked worktree reaches the
   repository first, `repository.root` is the canonical path of the first
   registry record, never that linked worktree's toplevel.
4. **Given** `atlas` has a clean, pushed, merged linked worktree outside
   every root, whose branch has a commit of its own, **When** the overview
   runs, **Then** it appears among `atlas`'s worktrees with `dev`, `ino` and
   a two-way-verified `admin_id`, classification `merged-removable` and a
   housekeeping finding, the suggestion is `project clean <atlas root>
   --all-safe`, and the project count is unchanged.
5. **Given** that external worktree's directory was deleted without `git
   worktree prune`, **When** the overview runs, **Then** its row has
   `present: false`, classification `stale-worktree` and a housekeeping
   warning suggesting the read-only `project clean <atlas root>`, no probe
   runs in the missing path, and the exit status is 0, or 1 with
   `--strict`.
6. **Given** no `--root`, `PROJECTS_DIR` unset and neither default projects
   directory present, **When** the overview runs, **Then** both roots are
   reported `absent` with no scan error, the result is complete, the exit
   status is 0, and the human output says that no projects directory was
   found and names `--root` and `PROJECTS_DIR`.
7. **Given** standard error on a terminal, and again on a pipe, **When** the
   overview runs, **Then** the first run writes one `Scanning N roots...`
   line to standard error before listing and the second writes none, and
   standard output is identical in both runs.
8. **Given** `--root` naming one project's own directory, **When** the
   overview runs, **Then** that directory is itself examined as a
   candidate, together with its immediate entries, so the project is
   reported (POD:18-19; proposal, Impact, README; Clarifications, C-1).

**Delta scenarios**: "Independent clones and aliases"; "Family holder
count, relationships and probe ownership"; "One probe set per repository";
"Present eligible external worktree"; "Missing external worktree"; "Every
root is absent"; "The scanning notice".

---

### User Story 2 - Only what needs attention, and an exit that says so (Priority: P1)

The person wants to read only what needs action, and a script wants an exit
status it can trust. Every finding carries one code, one category (repair,
preserve, housekeeping or informational) and one severity; `--attention`
hides the projects with nothing to do and the informational findings, and
changes neither the JSON, the summary nor the exit. A merged worktree whose
upstream was deleted is housekeeping like any merged worktree, by Brett
Heap's ruling of 2026-10-09 that local ancestry proof outranks
`remote-gone`.

**Why this priority**: "Ordinary work is not trouble" and "Incomplete is
visible" (proposal, "Rules This Change Keeps"); without the categories and
the exit rule, the report is a listing, not an answer.

**Independent Test**: Build four projects with one finding each, run with
and without `--attention`, `--json` and `--strict`, and compare what is
shown, the JSON and the exit statuses.

**Acceptance Scenarios**:

1. **Given** four projects whose only findings are `pushed-unmerged`,
   `unpushed`, `merged-removable` and `no-merge-target`, **When** `project
   overview` and `project overview --attention` each run with and without
   `--json`, **Then** `--attention` hides the informational-only project
   and shows the other three under their categories, the two JSON documents
   are identical apart from their timestamps, and every run exits 1;
   without the repair project every run exits 0, and with `--strict` every
   run exits 1 because of the preserve warning.
2. **Given** a clean linked worktree whose branch, with a commit of its own,
   is an ancestor of the merge target and whose upstream branch was deleted
   and pruned, **When** the overview runs, **Then** it is `merged-removable`,
   as `project clean <root> --json` classifies it, with the housekeeping
   finding whose message is the ladder's `merged-removable` recommendation,
   suggests `project clean <root> --all-safe`, and no Git child beyond the
   shared probe set ran for it; a worktree whose upstream branch was
   deleted and pruned and whose tip is not an ancestor is `remote-gone`,
   with a preserve warning carrying the ladder's own `remote-gone`
   recommendation, and suggests only the read-only `project clean <root>`.
3. **Given** projects whose only findings are informational, **When**
   `project overview --attention` runs, **Then** no row is shown, the
   summary line says that nothing needs attention, gives the counts and
   states that findings reflect local refs as of the last fetch, and the
   exit status is 0.
4. **Given** a row error and a scan error, **When** `--attention` runs,
   **Then** both are shown, in the repair category, and neither is counted
   as a finding (POD:462-468).

**Delta scenarios**: "Attention filter per category"; "A merged worktree
whose upstream was deleted"; "Nothing needs attention".

---

### User Story 3 - The same verdict `project clean` would give (Priority: P1)

The overview never second-guesses `project clean`. It classifies each
worktree with the same ladder over the same evidence and resolves the same
merge target, so a person who follows a suggestion sees the same picture in
the plan it leads to.

**Why this priority**: "One classifier, one evidence model" (proposal,
"Rules This Change Keeps"); every suggestion relies on it.

**Independent Test**: Build the merge-target fixtures and the repository of
"Every protected classifier", and compare each row's `merge_target` and
each worktree's classification with `project clean <root> --json` run from
the same directory at the same commit.

**Acceptance Scenarios**:

1. **Given** a `project.yaml` with `tracking_branch: origin/develop`, a
   local `develop` and no `origin/HEAD`, **When** the overview runs,
   **Then** `merge_target` is `develop` with source `manifest` and the
   object id of `refs/heads/develop`, classification is relative to it, the
   merged set was computed at that object id, resolution spawned no Git
   child beyond the ref listing, and the name equals the merge target that
   `project clean <root> --json` reports.
2. **Given** no manifest, `origin/HEAD` naming `origin/trunk`, and local
   `trunk` and `main`, **When** the overview runs, **Then** the target is
   `trunk` with source `origin-head` and the object id of
   `refs/heads/trunk`.
3. **Given** no manifest and no `origin/HEAD`, with local `main` and
   `master`, or with only a local `master`, **When** the overview runs,
   **Then** the target is `main` with source `main`, or `master` with
   source `master`, and that branch's object id.
4. **Given** a manifest naming `develop` and `origin/HEAD` naming `main`,
   both existing locally, **When** the overview runs, **Then** the target is
   `develop` with source `manifest`, one informational
   `merge-target-conflict` finding names both branches, and the exit status
   is 0 when nothing else is found.
5. **Given** a manifest naming an absent `release`, no `origin/HEAD`, and
   neither `main` nor `master`, **When** the overview runs, **Then**
   `merge_target` is null, the row has a `no-merge-target` repair finding of
   severity error with no suggested command, every worktree's
   classification is null, and the exit status is 1; on the same fixture
   `project clean <root> --all-safe` refuses with exit status 2 before any
   mutation.
6. **Given** one repository whose worktrees are classified
   `protected-default`, `dirty`, `ignored-local-files`, `detached`,
   `unpublished`, `remote-gone`, `diverged`, `remote-ahead`, `unpushed`,
   `merged-current` and `pushed-unmerged`, plus one gate-passing
   `merged-removable`, and a second repository holding an
   `inspection-error` worktree whose corrupted index makes its status probe
   fail, **When** the overview runs from inside the `merged-current`
   worktree, **Then** every classification equals what `project clean
   <root> --json` reports from the same directory, each finding has the
   category and severity of the attention table, and the only housekeeping
   finding and the only `--all-safe` suggestion belong to the
   `merged-removable` worktree, and no other worktree appears in the
   `selected` list of the batch preview that suggestion runs.

**Delta scenarios**: "Manifest target"; "origin/HEAD target"; "main
target"; "master target"; "Conflicting targets"; "Missing target"; "Every
protected classifier".

---

### User Story 4 - A next command to review, never permission (Priority: P1)

Each row offers at most one next command, an argument vector naming the
repository's absolute root: `project clean <root> --all-safe` only for a
merged worktree that passes the batch gates the overview can evaluate from
its own evidence; otherwise the read-only `project clean <root>` where the
attention table names it; no clean suggestion for a code the table marks
none, a finding on the merge-target checkout, a null `repository.root`, or a
root or common directory that is not valid UTF-8; and never `--apply`,
`--yes` or a bare name. When a gate withholds or limits a suggestion, the
finding names the gate and the person reads its remedy. `project clean`
still recomputes, shows and confirms its own plan.

**Why this priority**: "Evidence is not permission" (proposal, "Rules This
Change Keeps"); a suggestion must never point at what `project clean`
refuses.

**Independent Test**: Build gated worktrees, seventeen eligible ones, 130
and 260 registered rows and the reflog fixtures; check `suggested_command`,
`suggestion_gate`, `suggestion_gate_rows`, the messages and the human `next`
line, and run the suggested command's preview.

**Acceptance Scenarios**:

1. **Given** four worktrees the ladder would classify `merged-removable`,
   one locked with `git worktree lock`, one whose `.git` file names another
   administrative directory, one whose path contains the byte `0xFF`, and
   the main worktree checked out on a merged non-target branch while the
   overview runs elsewhere, **When** the overview runs, **Then** the locked
   one has a `locked-worktree` finding suggesting the read-only `project
   clean <root>`, the mismatched one gets no status probe and is
   `inspection-error`, a `registration-mismatch` finding replacing its
   `inspection-error` finding and adding no error, the non-UTF-8 one has
   `unsupported-path-bytes`, the main worktree has `main-worktree`, and none
   produces a housekeeping finding; a fifth, gate-passing
   `merged-removable` worktree in the same repository keeps its
   housekeeping finding with the read-only suggestion and
   `suggestion_gate: "inspection-incomplete"`, and the row suggests the
   read-only form; after `git worktree repair` fixes the registration, the
   `--all-safe` suggestion returns and the batch preview selects the
   repaired worktree, whose branch has a commit of its own, and the fifth.
2. **Given** projects named `atlas` under two roots, each with a
   `merged-removable` worktree whose branch has a commit of its own,
   **When** the overview runs, **Then** the rows suggest `["project",
   "clean", "<first atlas root>", "--all-safe"]` and `["project", "clean",
   "<second atlas root>", "--all-safe"]`, and each, when run, resolves its
   path Git-first to a plan whose `repository` and `merge_target` equal
   that row's; for an assembly root with a `project.yaml` whose
   immediate-entry leg `api` is its own repository with one dirty and one
   such `merged-removable` worktree, the leg's row suggests `--all-safe` on
   the leg's root, its `dirty` finding suggests the read-only form, and
   either reports `root` equal to the leg; the same command with a
   linked-worktree path or a subdirectory instead of the root is refused by
   `project clean` with exit status 2 and `target-not-repository-root`
   before any mutation.
3. **Given** one repository with 17 gate-passing `merged-removable`
   worktrees and the batch's target limit at 16, **When** the overview runs,
   **Then** each of the 17 findings and the row suggest `--all-safe` with
   `suggestion_gate: "target-cap"` and a message ending "limited to the
   batch's target limit of 16 per run; re-run to drain the backlog", the
   human `next` line ends `(limited: ...)` with that remedy, and the exit
   status is 0.
4. **Given** one repository with 130 worktree rows, the batch's row cap at
   128 and the report's at 256, including a gate-passing `merged-removable`
   worktree and a `dirty` one, **When** the overview runs, **Then** the
   `merged-removable` finding suggests the read-only form with
   `suggestion_gate: "inspect-cap"`, `suggestion_gate_rows: 130` and the
   remedy "130 rows exceed the batch's row cap of 128; remove explicitly",
   and the `dirty` finding's read-only suggestion carries no gate; in a
   repository with 260 worktree rows every read-only suggestion carries
   `suggestion_gate: "inspect-cap"`, `suggestion_gate_rows: 260` and the
   remedy "260 rows exceed the report's row cap of 256; the report would be
   incomplete".
5. **Given** a linked worktree created with a new branch at the merge
   target's tip and published with `git push -u`, with no commit of its own,
   so that its reflog holds only its `branch: Created from` entry, **When**
   the overview runs, **Then** it keeps its `merged-removable` finding,
   which suggests only the read-only form with `suggestion_gate:
   "unstarted-branch"` and a message ending "no commit was made on this
   branch here since it was created; review, then git worktree remove
   yourself"; no `--all-safe` suggestion is given for that repository on its
   account, and after `git branch -m`, whose entry has equal old and new
   objects, it is still `unstarted-branch`; a branch with commits of its
   own, merged into the merge target and then reset to the target's tip by
   `git worktree add -B <branch> <path> <merge target>` with no commit after
   it, anchors at that `branch: Reset to` entry and is `unstarted-branch`
   too, its earlier commits not counting as movement; a branch created by
   `git fetch origin feat:f1` while `origin/feat` sits at the merge target's
   tip, given an upstream by `git branch -u origin/feat f1`, which writes no
   reflog entry, then checked out in a linked worktree with no commit,
   anchors at that fetch entry, whose old object is all zeros, and is
   `unstarted-branch` too, never passing as a movement; and a branch given
   one commit and then fast-forward merged into the merge target, so that
   its head equals the target's tip while its reflog records that commit
   after its anchor, keeps the `--all-safe` suggestion with no gate.
6. **Given** one gate-passing `merged-removable` worktree whose branch has
   no reflog file, another whose reflog file is empty, a third whose reflog
   keeps only a rename entry after `git reflog expire` removed its creation
   and commit entries, and a fourth whose branch, whose reflog records a
   commit of its own, was then moved to another merged commit by writing its
   ref directly, so that its last entry's new object differs from its head,
   **When** the overview runs, **Then** each keeps its `merged-removable`
   finding, which suggests only the read-only form with `suggestion_gate:
   "reflog-unavailable"` and a message ending "the branch's reflog is
   missing, expired or undecidable; review, then git worktree remove
   yourself", no Git child is started to read any of the four reflogs, and
   `project clean <root> --all-safe` excludes all four as
   `reflog-unavailable`; in a second repository, where one gate-passing
   worktree's reflog cannot be read for a permission error, that worktree
   records an `os-error` and is `inspection-error`, and another gate-passing
   `merged-removable` worktree there suggests only the read-only form with
   `suggestion_gate: "inspection-incomplete"`.
7. **Given** a repository holding a gate-passing `merged-removable` worktree
   and another worktree whose status probe failed, **When** the human
   report prints, **Then** the row's `next` line carries `project clean
   <root>` followed by `(withheld: repair the inspection-error rows, or
   re-run for the rows left unprobed, first)`, and the finding lines show
   the repair finding and the housekeeping finding with their worktree
   paths.

**Delta scenarios**: "Gated merged worktrees"; "Canonical identity through
the handoff"; "More eligible worktrees than the batch's target limit"; "The
two inspect-cap bands"; "An unstarted branch"; "A branch whose reflog cannot
decide"; "A gated suggestion".

---

### User Story 5 - One versioned JSON document (Priority: P1)

A script, or a person piping the report to another tool, reads `project
overview --json`: one document with `schema_version: 1` and a fixed set of
fields, every one always present, where `null` means unknown and never
stands for false, zero or an empty list. An argument error or a failure
outside the per-candidate boundary prints no traceback and no partial
document.

**Why this priority**: The other P1 stories are tested through this
document, which carries the rows, identities, merge targets, findings and
suggestions they check, and the change makes it the interface scripts rely
on (proposal, What Changes, "A versioned JSON envelope").

**Independent Test**: Over one healthy repository holding one
`merged-removable` worktree and one unreadable root, parse standard output
as JSON and check every field and its type; then run with an unknown option,
and with an exception injected outside the per-candidate boundary.

**Acceptance Scenarios**:

1. **Given** one healthy repository holding one `merged-removable` worktree
   and one unreadable root, **When** `project overview --json` runs,
   **Then** the document carries exactly the envelope's fields with their
   types, `limits` includes `batch_row_cap`, `report_row_cap` and `targets`
   equal to the shared constants, read without building a clean plan, every
   finding carries `suggestion_gate` and `suggestion_gate_rows`, every
   `path` has `path_valid_utf8` beside it, `repository` carries
   `root_valid_utf8` and `common_dir_valid_utf8`, and `completeness` is
   `incomplete`.
2. **Given** `project overview --json --bogus`, **When** it runs, **Then**
   standard output is empty, standard error carries the usage message, and
   the exit status is 2.
3. **Given** an exception that is neither a refusal nor an
   operating-system error, raised outside the per-candidate boundary during
   a `--json` run, **When** it reaches the top, **Then** standard output
   holds only `{"error": "<message>", "code": "internal-error"}`, the message
   naming the exception class, no traceback is printed, and the exit status
   is 2.

**Delta scenarios**: "Every envelope field is present"; "An argument error
under --json"; "An internal error outside the collector under --json".

---

### User Story 6 - Every run is bounded and says what it omitted (Priority: P2)

An estate with hundreds of repositories, a hung mount or a huge index must
neither hang the overview nor be half-read in silence. Every run has one
60 s deadline, a 5 s budget per Git child and per filesystem call, fixed
caps and at most four Git children at once; every cut is reported with what
it omitted and how exactly that is known, and the result is then
incomplete and exits 1.

**Why this priority**: Bounds keep the report predictable: governance task
2.1 measured the caps' worst case at 48.3 s of the 60 s deadline (proposal,
OQ-4), and an estate past a cap is reported incomplete, never silently
short; the P1 stories are already right on an estate inside the caps.

**Independent Test**: Under a counting `git` wrapper that can hold a status
probe and with injected slow filesystem calls, build 130 candidates, a root
of 4,100 entries, 33 roots, 520 worktree rows (one repository among them
holding a gate-passing `merged-removable` worktree beside a row the cap
leaves unprobed), 10,000 ignored files and a manifest over 1 MiB, and
compare completeness, `omitted`, suggestions, exit statuses, the process
table and the JSON at probe concurrency 1 and 4.

**Acceptance Scenarios**:

1. **Given** one root holding 130 candidate directories `p000` to `p129`,
   created in reverse order and listed once in sorted and once in reverse
   order through an injected listing, **When** the overview runs, **Then**
   the rows are `p000` to `p127` in both runs, one `scan-limit` scan error
   has `limit: "candidates"` and `omitted: {"count": 2, "exactness":
   "exact"}`, the result is incomplete and the exit status is 1; given also
   a second root of 4,100 entries none of which holds a marker, that root is
   `truncated` with `entries` 4,096 and a `root_entries` `scan-limit` error
   whose count is null with exactness `unknown`, and the candidate-cap error
   reports the known excess, `{"count": 2, "exactness": "lower-bound"}`.
2. **Given** 33 distinct roots, or repositories totalling 520 worktree rows,
   **When** the overview runs, **Then** the last root in canonical order is
   `omitted` with an exact omitted count of 1; and the first 512 worktree
   rows in rank order are probed on every run whatever the completion order,
   the other 8 keep registry and branch evidence with `dirty`,
   `ignored_files` and `classification` null, their project rows carry
   `scan-limit` errors, the scan error has `limit: "worktree_rows"` and
   `{"count": 8, "exactness": "exact"}`, and the exit status is 1.
3. **Given** the worktree-row cap leaves one row of a repository
   unclassified while another of its worktrees is gate-passing
   `merged-removable`, **When** the overview runs, **Then** that finding
   suggests the read-only form with `suggestion_gate: "scan-limit"` and the
   remedy "re-run with --root <repository parent>", naming the repository's
   parent directory.
4. **Given** one worktree's status probe held for 10 s by the counting `git`
   wrapper, **When** the overview runs, **Then** that child is stopped at
   5 s and reaped, its row records `probe-timeout` with `dirty: null` and
   classification `inspection-error`, every other row is complete, and the
   exit status is 1.
5. **Given** the `lstat` of an external worktree's path takes 10 s, on a
   fixture mount where one is available and by an injected slow call
   otherwise, **When** the overview runs, **Then** the call is abandoned at
   5 s, that worktree records `probe-timeout` with `present: null` and
   classification `inspection-error`, a gate-passing `merged-removable`
   worktree of the same repository suggests only the read-only form with
   `suggestion_gate: "inspection-incomplete"` (Clarifications, C-23), every
   other row is complete, and the exit status is 1.
6. **Given** canonicalising or listing one root given with `--root` takes
   10 s, on a fixture mount where one is available and by an injected slow
   call otherwise, **When** the overview runs, **Then** that root is cut at
   5 s with a `probe-timeout` scan error and counts as `truncated`, no entry
   of it is read after the cut, every other root's candidates are collected,
   and the exit status is 1.
7. **Given** a linked worktree under a root belongs to a repository whose
   main checkout is on a mount where every filesystem call takes 10 s,
   **When** the overview runs, **Then** each bounded task on that path
   records `probe-timeout` at 5 s on that row, the scan continues and every
   other row is complete, the run ends within the deadline, and the exit
   status is 1.
8. **Given** enough held probes to exceed 60 s, **When** the overview runs,
   **Then** no child starts after the deadline, every in-flight child is
   terminated, reaped within the grace and recorded `deadline-exceeded`,
   unstarted candidates appear as rows with `deadline-exceeded`, the scan
   error's omitted count is exact, and the process exits 1 within 64 s plus
   rendering.
9. **Given** eight single-worktree repositories whose status probes the
   counting `git` wrapper holds for 1 s each, **When** the overview runs,
   **Then** the process table never shows more than four of its Git children
   at once, nor two with the same `common_dir`, and the eight held probes
   take about 2 s rather than 8 s, as the counting wrapper's log of each
   child's start and end times and directory shows: at most four of its
   intervals overlap, no two in one repository, and the last held probe
   ends less than 4 s after the first one starts.
10. **Given** one fixture whose worktree rows exceed the worktree-row cap,
    **When** it is collected at probe concurrency 1 and at 4 and no budget
    or deadline is reached, **Then** the two JSON documents are
    byte-identical apart from timestamps and `budget.probe_concurrency`, and
    the same rows are probed.
11. **Given** a clean merged worktree holding 10,000 ignored files, **When**
    the overview runs, **Then** the status stream stops early,
    `ignored_files` is 64 with `ignored_files_truncated: true`,
    `ignored_samples` has eight entries, `dirty` is false and the
    classification is `ignored-local-files`, a preserve finding; exactly 64
    ignored files give `ignored_files` 64 with `ignored_files_truncated:
    false`; and 4,097 untracked files with no ignored one stop the stream at
    the record bound with `dirty` true, `ignored_files` null and
    classification `dirty`, not `inspection-error`.
12. **Given** the user's Git configuration sets
    `status.showUntrackedFiles=no` and a linked worktree is clean, pushed
    and merged, **When** the overview runs, **Then** the status probe
    succeeds, `ignored_files` is 0 and the worktree is `merged-removable`.
13. **Given** a candidate's `project.yaml` larger than the manifest size
    bound, **When** the overview runs, **Then** its row carries a
    `manifest-invalid` error naming the manifest and the bound, the file is
    neither read nor parsed, the other rows are complete, and the exit
    status is 1.

**Delta scenarios**: "Candidate cap after sorting, with an exact count";
"Candidate cap with an incomplete listing"; "Root and worktree-row caps"; "A
row left unprobed closes the repository gate"; "Probe timeout"; "Hung
filesystem call on an external worktree"; "A root on a hung mount"; "A
repository root on a hung mount"; "Invocation deadline"; "Bounded
concurrency"; "The JSON does not depend on concurrency"; "Bounded ignored
files"; "User status configuration"; "A manifest over the size bound".

---

### User Story 7 - One project's failure stays in its row (Priority: P2)

An unreadable directory, a malformed or wrongly typed manifest, a manifest
whose text is not valid UTF-8, a missing YAML library or a failing Git
child becomes data on that candidate's row. Every other row is collected and
printed, no traceback appears, and the run exits 1, not 2. For a manifest
with an invalid text encoding this is the one exception the overview makes
to the review-safety rule that every other command keeps.

**Why this priority**: One broken project must not hide the others, but the
common case is a healthy estate.

**Independent Test**: Put an unreadable candidate, a wrong-kind manifest, an
invalid-UTF-8 manifest and an unsearchable external worktree beside healthy
projects, run with and without `--json` and without the YAML library, and
check that every healthy row is unchanged and the exit status is 1.

**Acceptance Scenarios**:

1. **Given** one root holding candidates `alpha`, `locked` and `zeta`, with
   `locked` at mode 000, and a second `--root` that cannot be listed,
   **When** the overview runs, **Then** `locked` appears in its sorted
   position with `path` the candidate path, `name` `locked`, `kind` null,
   status `error`, `findings` empty, one `os-error` naming its path and
   every Git-derived field null, `alpha` and `zeta` are complete, the
   second root adds a `root-unreadable` scan error, and the exit status is
   1, never 2.
2. **Given** an external worktree whose parent directory is made
   unsearchable, so that `lstat` fails with a permission error, **When** the
   overview runs, **Then** the worktree has `present: null` and
   classification `inspection-error`, the project row has an `os-error` and
   status `error`, the other rows are reported, and the exit status is 1;
   when instead only that worktree's status probe fails, the row records
   `probe-failed` and is `inspection-error`.
3. **Given** a root holding `alpha`, `ledger` and `zeta`, where
   `ledger/project.yaml` declares `kind: other`, **When** the overview runs,
   **Then** `alpha` and `zeta` are complete, `ledger` appears in its sorted
   position with status `error`, a `manifest-invalid` error, its repository
   identity retained, and null `merge_target`, `git` and `worktrees`, and
   the exit status is 1.
4. **Given** the overview runs without the YAML library over `alpha`, with
   only a `.git` directory, and `ledger`, with a `project.yaml`, **When** it
   runs, **Then** `ledger` carries a `manifest-invalid` error naming the
   missing library, `alpha` is complete with no error, and the exit status
   is 1.
5. **Given** `ledger/project.yaml` contains invalid UTF-8 bytes beside
   `alpha` and `zeta`, **When** `project overview --json` runs, **Then**
   `ledger`'s row has status `error` and one `manifest-invalid` error naming
   that manifest, with no traceback, `alpha` and `zeta` are complete, the
   JSON document is printed, and the exit status is 1, not 2.
6. **Given** a project or family manifest containing invalid UTF-8 bytes,
   **When** `project status --json` reads it, **Then** status still refuses
   with structured JSON error output, exit status 2 and no traceback, as
   before this feature.

**Delta scenarios**: "Unreadable candidate directory"; "Unreadable external
worktree"; "One helper failure is isolated"; "The YAML library is not
installed"; "Overview keeps a manifest with invalid text in its row"; and
the kept canonical scenario "Manifest is not valid UTF-8 text".

---

### User Story 8 - Unusual layouts are named, never guessed (Priority: P2)

Submodule checkouts, bare repositories, checkouts made with a separate git
directory and repositories whose main worktree was deleted are reported
truthfully: the overview names the main checkout as `project clean` would
resolve it, or says why it cannot and gives no clean suggestion, so it
never suggests what `project clean` refuses.

**Why this priority**: These layouts are rare, but a wrong root in a
suggestion would send the person to a refusal or the wrong repository.

**Independent Test**: Under a root, place a `--separate-git-dir` checkout
with and without its checkout among the candidates, a submodule checkout, a
repository whose main worktree was deleted and a linked worktree of a bare
repository, and check `repository.root`, the layout findings, the probe
directories and the suggestions.

**Acceptance Scenarios**:

1. **Given** a root holding the checkout of a repository created with `git
   init --separate-git-dir`, whose git directory has no `core.worktree`,
   **When** the overview runs, **Then** `repository.root` is that checkout,
   its main worktree row is status-probed there and reports its dirty
   state, and the git-directory record is never status-probed; when only a
   linked worktree of that repository is a candidate and its checkout is
   not, `repository.root` is null with an `unsupported-layout` repair
   finding of severity error and no suggestion, and the exit status is 1.
2. **Given** an immediate entry of a root that is a submodule's checkout,
   whose `core.worktree` is relative to its git directory, **When** the
   overview runs, **Then** its row has `repository.root: null` and an
   `unsupported-layout` repair finding of severity error whose message names
   a submodule checkout, no `core.worktree` child ran for it, it gets no
   clean suggestion, every finding's `suggestion_gate` is null, and the exit
   status is 1.
3. **Given** a repository whose main worktree directory was deleted while a
   linked worktree under the root remains, **When** the overview runs,
   **Then** the row has `repository.root: null`, the main worktree row has
   `present: false` and a `main-worktree-missing` repair warning, the
   repository-wide probes run in the linked worktree, and no clean
   suggestion is given.
4. **Given** a linked worktree of a bare repository is an immediate entry of
   a root, **When** the overview runs, **Then** the row has
   `repository.root: null` and no clean suggestion, each finding that would
   have suggested one naming `target-not-repository-root` in
   `suggestion_gate`, and its repository-wide probes run in the common
   directory.

**Delta scenarios**: "A separate git directory"; "A submodule checkout under
a root"; "A deleted main worktree"; "A bare repository with a linked
worktree".

---

### User Story 9 - The merge-target checkout's own health (Priority: P2)

The checkout of the merge-target branch is never a removal target, but
unverified local commits there still need attention. It keeps its
`protected-default` classification and gains every finding that applies, not
only the first: `dirty` when dirty, and at most one of `unpublished`,
`remote-gone`, `diverged`, `unpushed` or `remote-ahead`, each with no
suggested command. A repository with no remote copy of its merge target is
ordinary work and raises no `unpublished` finding.

**Why this priority**: It completes the closed PR #2's doctor health, which
its decision record assigned to this design; most merge-target checkouts
are healthy.

**Independent Test**: Build a `main` pushed without `-u` and then given two
commits, a repository with no remote, a dirty `main` three commits ahead,
and a `main` checkout whose status probe fails; check the findings, the
`--attention` display and the exit with and without `--strict`.

**Acceptance Scenarios**:

1. **Given** `main` was pushed with `git push origin main`, without `-u`,
   and then given two local commits, **When** the overview runs, **Then**
   its checkout stays `protected-default` and has an `unpublished` preserve
   warning with the message "merge-target branch has no upstream; local
   commits are unverified" and no suggested command, `project overview
   --attention` shows that row, and the exit status is 0, or 1 with
   `--strict`.
2. **Given** a repository with no remote, local commits on `main` and
   nothing else to report, **When** the overview runs, **Then** its checkout
   has no finding, `--attention` does not show the row, and the exit status
   is 0 with or without `--strict`.
3. **Given** the checkout of `main` is dirty and 3 commits ahead of its
   upstream, **When** the overview runs, **Then** it stays
   `protected-default` and carries both a `dirty` and an `unpushed` preserve
   warning, each with no suggested command.
4. **Given** the status probe of the checkout of `main` fails, **When** the
   overview runs, **Then** that row is `inspection-error` with a repair
   finding of severity error and the `probe-failed` error, it carries none
   of the default-branch findings, and the exit status is 1.

**Delta scenarios**: "A default branch pushed without an upstream"; "A
repository with no remote"; "A dirty default branch ahead of its upstream";
"A failed status probe on the default branch".

---

### User Story 10 - Local, read-only and stoppable (Priority: P2)

The overview writes nothing and opens no network connection: every Git child
carries pins that make a lazy fetch fail locally, and none of [E]'s
seventeen scrubbed variables reaches it (EC-006 and EC-022 record what the
pins and the scrub do not cover; question Q9 of `clarify-questions.md`). It
refuses an old or missing Git before listing anything; and when the person
presses Ctrl-C, or the terminal or a supervisor ends it, no Git child
outlives it and no result document is printed.

**Why this priority**: Read-only is a rule the change keeps (proposal,
"Rules This Change Keeps"), and a scan across an estate must be safe to
interrupt. The read-only snapshots and the network block run under every
story's fixtures from P1 on (FR-040); this story adds the dedicated
whole-suite check, the version refusal and the signals, which matter less to
the daily answer than the earlier stories.

**Independent Test**: Run over every fixture with networking disabled and
before-and-after snapshots, the counting `git` wrapper asserting that every
Git child's argument vector carries the seven protocol pins and that none of
the seventeen scrubbed names, `GIT_ALLOW_PROTOCOL` included, reaches any
child (R-23, R-25; the overview has no push child, so feature 004's
push-child exception, R-28, never applies); run with Git 2.34.1 first on
PATH and with no `git` on PATH; and send SIGINT, SIGTERM and SIGHUP during
collection at probe concurrency 4 while one child hangs and another writes a
large output.

**Acceptance Scenarios**:

1. **Given** any fixture of this feature and networking disabled for the
   process, **When** the overview runs with default options, **Then** it
   opens no network connection, the before and after snapshots of `git
   for-each-ref`, `git worktree list --porcelain -z`, each checkout's
   status, each index file's modification time and the directory tree under
   every root are identical, the JSON preserves severity, freshness,
   unknown values and completeness, and a complete scan that finds no
   project says so and exits 0.
2. **Given** `git` reports version 2.34.1, or no `git` is on PATH, **When**
   the overview runs, **Then** it exits 2 with code `git-too-old`, and a
   message naming the 2.36 minimum, or with code `git-unavailable`, before
   listing any root or starting any other Git child, and under `--json` it
   prints only `{"error": "<message>", "code": "<code>"}`.
3. **Given** one Git child hung and another writing a large output at probe
   concurrency 4, **When** SIGTERM is sent, **Then** the exit status is 143,
   no result document is printed, `Cancelled.` is printed to standard error
   when it can be, and every child's process group is gone; with SIGHUP the
   exit status is 129.
4. **Given** children running and a finding of severity error already
   collected, **When** SIGINT is sent, **Then** every in-flight child is
   terminated and reaped, no result document is printed, `Cancelled.` goes
   to standard error, and the exit status is 130, not 1.

**Delta scenarios**: "Local and read-only"; "Git too old"; "Git
unavailable"; "SIGTERM or SIGHUP during collection"; "SIGINT during
collection".

---

### User Story 11 - Exact paths, whatever their bytes (Priority: P3)

Paths holding newlines, control, format or bidirectional characters, or
bytes that are not UTF-8, are reported exactly or escaped and flagged, in
JSON and in human output, and a root, common directory or worktree whose
path is not UTF-8 never feeds a clean suggestion.

**Why this priority**: It serves rare paths; the person at a terminal and
the scripts reading ordinary paths are served by the earlier stories.

**Independent Test**: On Linux, create a repository whose directory name
holds a newline and worktrees whose names hold a tab, U+0007, U+202E, U+200B
and the byte `0xFF`, plus a git directory whose name holds `0xFF`; parse
standard output as JSON and read the human output.

**Acceptance Scenarios**:

1. **Given** a repository directory name holding a newline and linked
   worktree names holding a tab, U+0007, U+202E and U+200B, **When** the
   overview runs, **Then** each JSON `path`, the findings' `checkout` paths
   and `repository.root` are exact with the escapes `\n`, `\t`, `\u0007`,
   `\u202e` and `\u200b`, every `path_valid_utf8` and `root_valid_utf8` is
   true, each worktree is classified from its real state rather than as
   `stale-worktree`, the human output prints each such path in `$'...'`
   form, the newline as `\u000a`, the tab as `\u0009`, U+0007 as `\u0007`,
   U+202E as `\u202e` and U+200B as `\u200b`, and the printed suggestion,
   pasted into bash under a UTF-8 locale, names the same repository root.
2. **Given** a clean merged worktree whose name holds the byte `0xFF`,
   **When** the overview runs, **Then** it completes, the worktree's `path`
   and its finding's `checkout.path` show the byte as `\xff`, each with
   `path_valid_utf8: false`, the row has an `unsupported-path-bytes` repair
   finding, the worktree contributes nothing to the `--all-safe` suggestion,
   and `project clean <root> --all-safe` excludes it with reason
   `unsupported-path-bytes`; and when another worktree holds two ignored
   files, one named with the byte `0xFF` and one named with the four
   characters `\xff`, its two `ignored_samples` entries have the same
   decoded `path` and differ only in `path_valid_utf8`, false and true.
3. **Given** the checkout of a repository made with `git init
   --separate-git-dir` into a git directory whose name holds the byte
   `0xFF`, with a dirty linked worktree, **When** the overview runs,
   **Then** `repository.common_dir` shows the byte as `\xff` with
   `common_dir_valid_utf8: false` while `root_valid_utf8` is true, the row
   has a repository-level `unsupported-path-bytes` repair finding, neither
   the row nor any finding carries a clean suggestion, each finding that
   would have suggested one names `unsupported-path-bytes` in
   `suggestion_gate`, and `project clean <root>` refuses with
   `unsupported-path-bytes` and exit status 2.

**Delta scenarios**: "Control and format characters in paths"; "Non-UTF-8
path"; "Non-UTF-8 common directory".

### Edge Cases

- **EC-001**: A filesystem call stuck in the kernel is abandoned at its
  budget so the run never blocks on it, but process exit may wait for it;
  it is the one exception to the run bound, and the README says so
  (design D1, D2 and Risks).
- **EC-002**: SIGKILL of `project` itself runs no cleanup: its read-only Git
  children run on, untimed, to their own end (design D1, Risks). The same
  holds for any other signal the overview does not handle (SIGQUIT,
  SIGUSR1, SIGUSR2 or SIGALRM, for example), which ends the process without
  its cleanup; and a SIGINT that arrives before the overview installs its
  handlers, while no child has started, ends the run through the shared
  command's own handling, `Cancelled.` on standard error and status 130, as
  for any other subcommand; only a SIGINT during interpreter start-up or
  argument parsing, before that handling is entered, gives the
  interpreter's own report (feature 004's `project` at `96a08d4`).
- **EC-003**: A default root holding more than 128 candidates is incomplete
  on every run by design: governance task 2.1 found 219 on the measuring
  workstation, a `scan-limit` error on `candidates` with 91 omitted, and no
  cap moves for it (proposal, OQ-4).
- **EC-004**: A repository with more than about 355 worktree rows, if
  children cost the 150 ms margin rate (governance task 2.1 measured about
  426 rows at 10,000 index entries, 284 with the margin, and about 75 at
  100,000), ends at the deadline, visibly incomplete; there is no
  per-repository row cap (proposal, OQ-7).
- **EC-005**: Roots on a Windows drive mounted into WSL2 can make every
  listing slow and truncate on every run; that case was not measured, and
  the README says so (design, Risks).
- **EC-006**: A remote-helper protocol of another name, with its own
  `allow=always` in the repository's configuration, is not among the pins
  and could still fetch for a probe in a partial clone; the probe then
  succeeds rather than fails, so no unsafe removal follows, the overview
  being read-only; the case is rare and is the accepted residual of "opens
  no network connection" (design D13, Risks; R-25).
- **EC-007**: `target-cap` counts gate-passing rows the batch's index gates
  may still exclude, so the overview's count can exceed what the batch
  selects; the suggestion is advice either way (design D5, Risks).
- **EC-008**: Repositories without file reflogs (the reftable backend, or
  `core.logAllRefUpdates=false`), and branches whose decisive entries
  expired after `gc.reflogExpire`, give every merged row
  `reflog-unavailable`, failing closed with the read-only suggestion
  (design, Risks).
- **EC-009**: A reflog of 64 KiB or more (65,536 bytes or more, about 300
  entries) is `reflog-unavailable` even when it records movement, because
  the bound ends the read: a read that returns 65,536 bytes has reached it,
  while a reflog of 65,535 bytes is decided by its entries (design, Risks;
  R-18; Clarifications, C-22).
- **EC-010**: A branch created from a remote branch that already had
  commits, then merged elsewhere and never moved here, reads
  `unstarted-branch` and fails closed (design, Risks).
- **EC-011**: A remote whose name contains `/` can make the remote-copy flag
  read set for another remote's branch, giving an `unpublished` warning,
  the direction in which the overview errs (design D9, Risks).
- **EC-012**: A gitfile repository whose checkout lies outside every root
  reads `unsupported-layout`, an error; adding the checkout's parent with
  `--root` names it (design, Risks; N-6).
- **EC-013**: A squash merge never puts the branch tip into the merge
  target's ancestry, so squash-merging repositories yield few
  `merged-removable` rows. Open question 2 of `add-project-clean-all-safe`
  (the lane's question LQ-2), a local patch-equivalence proof, is still
  before Brett Heap, with the lead's recommendation of a follow-on change,
  and is deferred to it; until he rules, the overview inherits the ratified
  rule through [L], ancestry alone proving a branch merged, and a contrary
  ruling amends the changes and this spec first (design, Open Questions;
  feature 004's spec, EC-001).
- **EC-014**: Where a Triad assembly's legs are submodule checkouts, as
  openRepoShape's README describes the Triad (the assembly repository holds
  `project.yaml` and "the two legs as submodules", at `spec/` and `code/`),
  a `--root` naming the assembly examines it itself (C-1), its legs are
  immediate entries, and each leg row gets the `unsupported-layout` error,
  so the run exits 1, as the change rules for every submodule checkout
  (POD:97-102; design D3, item 1). Whether that is the wanted answer for the
  README's one-project check is question Q1 of `clarify-questions.md`.
- **EC-015**: After SIGHUP the terminal may answer writes with an error, so
  `Cancelled.` is printed on a best-effort basis (proposal, Decisions).
- **EC-016**: The pasteable `$'...'` form assumes bash 4.2 or newer, or zsh;
  macOS's bash 3.2 is not a target, and tests assert the rendered string
  (proposal, Decisions, "Suggestion display string").
- **EC-017**: Non-UTF-8 path scenarios cannot run on macOS, whose
  filesystems reject such names, and are skipped there with that reason
  (proposal, Impact; design D13). CI runs on Linux only (README,
  Development), so every CI job runs them, and the skip serves only a local
  run on macOS.
- **EC-018**: Two spellings of one directory, such as a bind mount or
  `~/projects` and `~/Projects` on a case-insensitive filesystem, count
  once, and the canonically first spelling wins (POD:14-16, :85-87; design
  D7).
- **EC-019**: A Git child stopped at its record bound is a complete outcome,
  never `probe-failed` (design D1; [E]); it is still stopped by SIGTERM to
  its group, and only a child not reaped within the grace is abandoned and
  recorded `probe-timeout` (POD:172-176; Clarifications, C-2).
- **EC-020**: A reflog read that does not finish leaves its row unprobed,
  which withholds `--all-safe` for the whole repository with
  `inspection-incomplete` (POD:521-529; R-16).
- **EC-021**: Ignored files in the merge-target checkout raise no finding,
  since a `.venv` would otherwise warn on most projects (proposal, OQ-20).
- **EC-022**: The pins and the scrub do not cover everything Git does with
  the caller's setup. Git still reads the user's and the system's
  configuration and the variables outside [E]'s seventeen
  (`GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`, `GIT_CONFIG_NOSYSTEM`, `HOME`,
  `XDG_CONFIG_HOME` and `GIT_CEILING_DIRECTORIES` among them); it honours
  trace targets (`GIT_TRACE`, `GIT_TRACE2_EVENT`, `trace2.*` settings),
  which append to files; and the status probe runs the clean and process
  filters a repository's attributes name when it re-hashes a tracked file,
  a program that can write files or open connections outside the pins
  (CMD:98-122). How the feature treats these residuals is question Q9 of
  `clarify-questions.md`.
- **EC-023**: Each field is as of its own probe. A commit, a new worktree or
  a recreated repository during the scan can mix moments within one row, in
  which case the reflog's head test fails closed (FR-033); and a common
  directory deleted, and another created during the scan, can reuse its
  device and inode and so merge two repositories' rows. FR-019's
  independence from completion order holds for an estate that no other
  process changes during the run.
- **EC-024**: Under `--attention`, a shown row's `next` line carries the
  row's suggested command even when the only finding that fed it is
  informational and hidden, such as `locked-worktree` beside an
  `unsupported-path-bytes` repair finding that suggests nothing; the delta
  fixes both the filter and the `next` line (POD:466-471, :805-806), and
  the exit is unaffected.
- **EC-025**: Two layouts leave a repository unreported in a complete run,
  as the marker table is ratified (POD:24-31): a Git repository `D` whose
  holder directory `D/<name of D>`, holding `family.yaml`, has no `.git`,
  the holder being the candidate and `D` never inspected; and a directory
  whose only marker would be a `.git` that is a dangling symbolic link,
  which exists as neither a file nor a directory. Whether to report them is
  question Q10 of `clarify-questions.md`.
- **EC-026**: A merge-target branch that no worktree has checked out gets no
  default-branch finding, its unpushed or unpublished local commits
  included: those findings attach to a checkout [L] classifies
  `protected-default` (POD:725-727), and the row's `git` object describes
  the checkout at the row's `path` (Clarifications, C-50).
- **EC-027**: `dev` and `ino` are exact JSON integers (FR-037), and some
  filesystems report values above 2^53, which a consumer that reads JSON
  numbers as IEEE 754 doubles rounds, so that two identities can compare
  equal there; the overview's own grouping uses the exact values
  (Clarifications, C-51).
- **EC-028**: A worktree row's `branch` does not tell a detached head from a
  branch named `detached`, reading `"detached"` for a detached head as the
  clean report always has (POD:633-634; DI:765-766); the row's
  classification is the one [L] gives it, as for every row (FR-026;
  Clarifications, C-52).
- **EC-029**: A repository with about 10,000 loose refs can pass the 5 s
  per-child budget with its ref listing on a cold cache (8.65 s measured by
  governance task 2.1), giving `probe-timeout` and an incomplete run, never
  a wrong one (Clarifications, C-53).
- **EC-030**: A candidate whose `.git` file names a bare repository, as in
  the layout that keeps one in a `.bare` directory beside its linked
  worktrees, fails its identity probe, which asks for a toplevel a bare
  repository lacks: it is an error row with `probe-failed`, and its
  repository's worktrees are not listed (Clarifications, C-54). Whether to
  report such a repository otherwise, and how a bare repository's own first
  registry record is reported, is question Q14 of `clarify-questions.md`.
- **EC-031**: Two registry entries naming one path fail closed: the registry
  listing does not name the administrative directory, so the two-way
  registration check alone cannot tell the two entries apart, and each is a
  registration disagreement, whose outcome in either direction is no status
  probe, `inspection-error` set directly, a `registration-mismatch` finding
  in place of that class's `inspection-error` finding, and no error (FR-007;
  DI:259, :267-272). The packet names no case of two entries for one path.
  Feature 004, for the evidence model the overview shares, refuses them
  too, and gives three parts of that outcome: no status probe,
  `inspection-error` and `registration-mismatch` (its data model,
  "Worktree identity and registration" at `96a08d4`; lead ruling R-57,
  withdrawing R-51(c)'s known limit, and R-59 D5, which compares the
  registry records' raw path bytes). Its code builds the refusal at that
  head (`7880023`, as `7d70b02` later split it, the lines being those of
  `96a08d4`): `shared_paths` (`project:2634-2641`) names the raw paths that
  more than one entry lists, `worktree_rows` (:2762-2816) tells `_read_row`
  (:2725-2759) whether a row's path is one of them, and that reader looks at
  presence first, so a row not present goes no further and stays
  `stale-worktree` with no duplicate check (R-57 L2, R-59 D5), while any
  present row on such a path gets `registered` false with no registration
  read. The finding in place of the class's `inspection-error` finding and
  the absence of an error are the packet's rule (DI:267-272), not stated by
  feature 004. The rows keep the registry's order, so the output stays
  deterministic.
- **EC-032**: When a value of the identity probe holds a line feed, as the
  name of a repository directory can (US11 s1), the probe is repeated, one
  child per option, each counted (change 1's design D6, row 3), so that for
  such a path `probes.performed` exceeds `probes.estimated`, which counts 1
  identity probe per Git candidate (FR-020; POD:248-254). No scenario
  asserts the two equal there, and FR-020 stands as ratified.
- **EC-033**: A present worktree on a branch named `HEAD`
  (`refs/heads/HEAD`) fails closed. Its `branch` and `head` come rightly
  from the registry, its `merged_into_target` from the merged set and its
  status from its own probe, but its `upstream`, `upstream_oid`,
  `remote_present`, `ahead` and `behind` come from the ref listing
  (DI:423-425; CMD:149-153), which for that ref prints the upstream and
  track of the branch that `HEAD` names where the listing runs, whatever
  `branch.HEAD.*` says. Reproduced for this record on Git 2.43.0 with the
  fixture of feature 004's `8bea203`, and by lane openRepoProject-3 on Git
  2.36.6 and 2.40.4, the listing exiting 0 with nothing on standard error on
  all three: run at `repository.root`, whose checkout is on `main`, the
  listing credits `refs/heads/HEAD` with `origin/main`, and with `ahead 1`
  once `main` is a commit ahead while that ref stays at `origin/main`; at
  `ahead 0` the worktree then reads as pushed and merged and, as feature 004
  found, `merged-removable`, and at `ahead 1` as `unpushed`. Those five
  fields are therefore not established: they stay null (feature 004's
  documents and its lead ruling R-61(b) name three of them, `upstream`,
  `ahead` and `behind`; its R-64(a), within R-61(b)'s fill, adds
  `remote_present`, and `upstream_oid` stays unset, `project:2186`), and the
  row is `inspection-error` set directly (POD:340-342, :378-381;
  CLN:114-116), as feature 004's `project clean` classifies it at `96a08d4`
  (POD:381-384 then makes the overview equal to it). That is a fill of
  change 2's rule, not a departure, as feature 004's lead ruling R-61(b)
  fills [L]'s for `project clean` (`8bea203`, merged by `6ae927f`; its data
  model, "Branch evidence", and its contract at `96a08d4`); change 2's table
  (POD:328-335) names no code for a Git child that exits 0 with output that
  cannot be trusted, so the overview takes feature 004's `probe-failed`
  (R-61(b)), and it reads the cause list of CLN:114-116 as feature 004 does,
  as examples. The project row carries a `probe-failed` error and status
  `error` (the collector table's code for a Git child that exits nonzero,
  POD:333, which feature 004 also gives one whose output yields no usable
  value, `unparseable output`; Dependencies), the worktree's finding is
  `inspection-error` (repair, error, no suggestion; POD:428), the run is
  incomplete and exits 1, and `inspection-incomplete` withholds `--all-safe`
  for the repository (FR-034); where the checkout at the row's `path` is on
  that branch, the `git` object's `upstream`, `ahead` and `behind` are null
  too (C-13). Feature 004's guard sits in its row decider, not in the
  listing or its parser: `row_evidence` (`project:2656`) tests
  `HEAD_BRANCH_REF` (:2161-2165) before it reads any upstream, and adds the
  error (:2694-2697) that the ladder's first test reads (:2042-2044). The
  overview inherits that guard only where its rows are built by that decider
  (Dependencies, R-54); a row built from its own parse of the listing
  (FR-015; design D9) is not covered by it, and the same fill applies there.
  Git writes nothing to standard error for the listing, so FR-022's message,
  the first line of that stream, has no line to take; feature 004's text is
  `git for-each-ref failed: unparseable output`, and which text the overview
  prints falls under question Q8 of `clarify-questions.md`: its option D
  adopts it, and under its options A to C that first line is empty.

## Requirements *(mandatory)*

Each requirement names the delta text it realizes (`POD:N`, `PRSD:N`) and,
where the delta defers to it, the design decision; the traceability appendix
maps every delta requirement and scenario back to them. [E], [L], [G], [R]
and [P] are change 1's requirements as the header names them.

### Functional Requirements

**Discovery**

- **FR-001**: `project overview [--root D]... [--attention] [--json]
  [--strict]` MUST take its roots from the repeatable `--root` option
  (source `argument`), else from `PROJECTS_DIR` (source `environment`), else
  from `~/projects` and `~/Projects` (source `default`), and MUST expand,
  canonicalise, deduplicate (by canonical path and by device and inode) and
  sort them by the bytes of their canonical paths (POD:11-16;
  Clarifications, C-3). A root whose canonicalisation is cut is question Q13
  of `clarify-questions.md`.
- **FR-002**: Discovery MUST examine each root itself and its immediate
  entries only, never recursing. A symbolic-link entry MUST be resolved once
  and MUST add nothing when it resolves to a directory already seen. A
  canonical directory MUST be a candidate exactly when a marker of the
  delta's marker table holds, the first matching marker deciding the
  candidate and its kind (`family-holder`, `project-manifest` or `single`),
  with no Git child; a directory with no marker MUST be neither a candidate
  nor reported, and an entry that resolves to a file, or a link that
  dangles, adds nothing (POD:18-32; Clarifications, C-1 and C-35).
- **FR-003**: Candidates MUST be canonicalised, deduplicated by canonical
  path and by device and inode, and sorted by their bytes before the
  candidate cap applies, the canonically first spelling of one directory
  winning. The overview MUST NOT use the command's project lookup by name or
  its recursive project snapshot, and MUST NOT read a family's member list:
  a family holder MUST be exactly one row of kind `family-holder`,
  `relationships` MUST be `[]`, the holder MUST receive Git probes only when
  its own directory is a Git toplevel, a holder whose directory has no `.git`
  entry, or whose identity probe reports another toplevel, MUST have null
  `repository`, `merge_target`, `git` and `worktrees` and carry no error for
  the Git probes it does not get, and a member directory that is itself an
  immediate entry of a root MUST be an ordinary candidate with its own row
  (POD:32-40, :85-87; DI:284-287; design D7). What the identity probe of a
  candidate other than a family holder does when it reports another toplevel
  is question Q11 of `clarify-questions.md`.
- **FR-004**: A candidate whose directory holds no `.git` entry MUST get no
  Git child: its row MUST have null `repository`, `merge_target`, `git` and
  `worktrees`, no finding for the missing checkout, and status `ok` unless
  an error, such as its manifest's, is recorded (POD:38-39, :66, :319-321;
  proposal, "Absorbing Doctor Repository Health", the "no Git checkout" row;
  Clarifications, C-4).
- **FR-005**: A default root that does not exist, its canonical path naming
  nothing, MUST be reported with state `absent` and no error. An argument or
  environment root that does not exist, is not a directory or cannot be
  listed, and a default root that exists but is not a directory or cannot be
  listed, MUST be reported `unreadable` with a `root-unreadable` scan error,
  and MUST never cause exit status 2 (Clarifications, C-27). A marker check
  that fails with any error other than "no such entry" MUST make that
  directory an error row (`kind` null, status `error`, `findings` empty, one
  `os-error` naming its path, every Git-derived field null), sorted and
  capped like any other row. When every root is `absent`, the human output
  MUST say that no projects directory was found, naming `--root` and
  `PROJECTS_DIR`, in the line design D10 fixes (POD:42-51; design D10).

**Repository identity and layouts**

- **FR-006**: Rows MUST be keyed by repository identity `{root, common_dir,
  dev, ino}`, never by a path string or a name: `common_dir` from [E]'s
  identity probe, and `dev` and `ino` from the no-follow `lstat` of the
  common directory. A linked worktree that is also a candidate MUST merge
  into its repository's row, independent clones MUST stay distinct, and
  every registered worktree, those outside every root included, MUST be
  listed under its repository, main worktree first and then by path bytes,
  each with the worktree identity `{path, dev, ino, admin_id}`; a linked
  worktree's registration MUST take [E]'s two-way check, while the main
  worktree has `admin_id: null` and no administrative registration to check
  (Clarifications, C-39). "The candidate that reached a repository first"
  MUST mean the first in canonical candidate order (POD:75-87; design D7).
  Two registry entries that name one path fail closed as a registration
  disagreement (FR-007; EC-031); and what a candidate other than a family
  holder, whose identity probe reports another toplevel, creates or joins is
  question Q11 of `clarify-questions.md`.
- **FR-007**: Each registered path MUST fall into exactly one case: `lstat`
  fails with "no such entry" or "not a directory" (`present: false`, no
  status probe); `lstat` fails otherwise, or does not finish within its
  filesystem budget or before the deadline (`present: null`, no status
  probe, an `os-error`, or `probe-timeout` or `deadline-exceeded` for a cut
  call, and `inspection-error` set directly); the registration check cannot
  be completed, a read of `<path>/.git` or of the administrative `gitdir`
  file failing with an error that shows no disagreement, or being cut (no
  status probe, the same codes, `inspection-error` set directly);
  registration disagrees in either direction, a `<path>/.git` that is
  missing (`ENOENT` or `ENOTDIR`) or not a regular file, or an
  administrative `gitdir` file that is missing (`ENOENT` or `ENOTDIR`),
  being a disagreement and not such an error (no status probe,
  `inspection-error` set directly, a `registration-mismatch` finding in
  place of that class's `inspection-error` finding, and no error); otherwise
  one status probe in that worktree. The two registration cases apply to
  linked worktrees only (C-39). A probe MUST NOT run in a path the overview
  could not `lstat`, nor a status probe in a worktree whose registration it
  could not verify (POD:89-95; CMD:124-126, :139-142; CLN:114-116;
  DI:244-245, :267-273; Clarifications, C-23, C-26, C-33 and C-39).
- **FR-008**: Every repository MUST first take [R]'s submodule test: when
  Git reports a superproject working tree for a candidate that reached the
  repository, `repository.root` MUST be null with an `unsupported-layout`
  repair finding of severity error, whose message (design D3, item 1) names
  a submodule checkout, with no suggestion and no read of `core.worktree`.
  Otherwise a bare main entry MUST leave `repository.root` null, its
  repository-wide probes running in the common directory (how that entry is
  itself reported among the worktree rows is question Q14 of
  `clarify-questions.md`); and where the
  first registry record's path equals `common_dir`, `repository.root` MUST
  be the realpath of `core.worktree` (a relative value resolved against the
  git directory), else the toplevel of a candidate whose identity probe
  reported this `common_dir` and whose `.git` file names `common_dir`
  itself, else null with an `unsupported-layout` repair finding of severity
  error, no suggestion and the remedy "set core.worktree or move the
  checkout". The git-directory record MUST never be a status-probed row;
  when `repository.root` is named, the main worktree row MUST name it and
  take its status probe there (POD:97-112; design D3, items 1 to 3).
- **FR-009**: In the ordinary layout `repository.root` MUST be the main
  worktree: the identity probe's toplevel when the candidate that reached
  the repository first is the main worktree itself, and otherwise the
  canonical path of the first registry record, never a linked worktree's
  toplevel. A main worktree path that does not exist MUST give
  `repository.root: null` and a `main-worktree-missing` repair finding of
  severity warning in place of its `stale-worktree` finding, with the remedy
  "restore or prune the main worktree by hand" and no suggestion, the
  repository-wide probes running in the candidate and the manifest being
  read at the row's `path`. A suggestion for a gitfile checkout MUST follow
  [R] (POD:113-124; design D3, items 4 and 5).
- **FR-010**: A row's `path` MUST be `repository.root`, or the candidate
  when that is null; its `kind` MUST be the kind of the candidate whose path
  equals that `path`, else that of the canonically first candidate that
  reached the repository; and its `name` MUST be the manifest name at that
  `path`, else its directory name (POD:625; design D7).

**Bounds**

- **FR-011**: Each run MUST be bounded by its own 60 s invocation deadline
  on a monotonic clock, set before any root is listed, and each Git child by
  [E]'s per-child budget under an invocation deadline, `min(5 s, work
  remaining)`, which with the overview's no reserve is `min(5 s, deadline -
  now)`; a child whose budget is not positive MUST NOT start. Each child
  MUST run in its own process group; a child that reaches its budget, or
  whose output the overview stops reading early, MUST receive SIGTERM to its
  group, SIGKILL 2 s later, and be reaped within a further 2 s or abandoned.
  Whether a child inherits SIGINT, SIGTERM and SIGHUP blocked from the
  parent's spawn, as design D1 sets up, with the result that SIGTERM cannot
  stop it before SIGKILL, is question Q16 of `clarify-questions.md`.
  A child that reaches its budget, where the 5 s limit was the smaller, and
  any child stopped for its own budget or at a record bound and then
  abandoned after the reap wait, MUST record `probe-timeout` on its row,
  while a child stopped at its record bound and reaped is a complete
  outcome, and a child the deadline cuts, reaped or abandoned, records
  `deadline-exceeded` (FR-012; Clarifications, C-2 and C-31). A run MUST end
  within 64 s of the moment its deadline is set, plus rendering, except
  while a filesystem call stuck in the kernel is outstanding (EC-001)
  (POD:167-181, :282; CMD:185-186; design D1 and D13).
- **FR-012**: On deadline expiry a further child MUST NOT start, every
  in-flight child MUST be terminated together in the same way and recorded
  `deadline-exceeded`, each candidate whose collection never started MUST
  still be a row carrying only filesystem facts, status `error` and a
  `deadline-exceeded` error, a row whose worktree probes were not reached
  MUST keep its repository-wide evidence and get the same error, and one
  `deadline-exceeded` scan error MUST count the candidates not started in
  `omitted`, whose exactness is `exact` when every root listing completed, as
  in "Invocation deadline", and `lower-bound` when a root listing was cut
  (POD:176-181, :224-229, :283, :335; DI:496-497; design D6; Clarifications,
  C-30).
- **FR-013**: Every filesystem call MUST run in a bounded task waited for
  at most `min(5 s, deadline - now)`, the tasks being those change 2 groups
  the calls into (Clarifications, C-38): one per root, enclosing its
  canonicalisation, deduplication `stat`, listing and marker and holder
  checks, so that a root's whole listing has one budget; one per worktree
  row, enclosing its `lstat` and registration reads; one per manifest read;
  one per branch reflog read of at most 64 KiB, never by a Git child; and
  one for the realpath of the working directory taken at start. A task that
  does not finish MUST record `probe-timeout`, or `deadline-exceeded` where
  the deadline was the smaller limit, on its root or row, and the overview
  MUST move on without blocking on it. A root cut this way MUST count as
  `truncated`, and its listing MUST read no further entry once the root is
  abandoned; a reflog read cut this way MUST leave its row unprobed for the
  repository gate of FR-034, and a worktree row's `lstat` or registration
  read cut this way MUST make that row `inspection-error` as FR-007 states
  (POD:183-192, :781; clarifications N2; design D2 and D8; Clarifications,
  C-23, C-25 and C-38). A root whose canonicalisation is itself cut is
  question Q13 of `clarify-questions.md`.
- **FR-014**: A manifest whose size, taken before the read, exceeds [E]'s
  1 MiB MUST be `manifest-invalid` on its row without being read, and a
  manifest read MUST NOT exceed 1 MiB (POD:192-196; design D8).
- **FR-015**: The ref listing MUST be consumed as it streams, keeping only
  the local heads, `origin/HEAD`, the remote refs named as upstreams and one
  flag recording whether a remote copy of the merge target exists, so that
  what it keeps is bounded by the heads; the status probe and its record
  bounds (64 ignored entries, 4,096 records, 8 samples) MUST be [E]'s
  (POD:196-200; design D9).
- **FR-016**: Every Git child of the overview, the version check included,
  MUST carry the seven protocol pins `-c protocol.allow=never -c
  protocol.file.allow=never -c protocol.ssh.allow=never -c
  protocol.git.allow=never -c protocol.http.allow=never -c
  protocol.https.allow=never -c protocol.ext.allow=never`, MUST run with the
  seventeen names of [E]'s environment scrub removed, `GIT_ALLOW_PROTOCOL`
  included, and with `GIT_OPTIONAL_LOCKS=0`, and every status probe MUST
  also carry `-c core.untrackedCache=false -c core.fsmonitor=false`. No Git
  child of the overview is exempt: it starts no push child, so feature 004's
  push-child exception (lead ruling R-28) never applies. A lazy fetch in a
  partial clone MUST therefore fail locally and be recorded `probe-failed`
  on its row, a failed status probe leaving its worktree `inspection-error`,
  with no network call. A Git child is a process the overview starts;
  processes Git itself starts run in that child's process group and take
  the pins from Git (POD:200-215; R-23, R-25; Clarifications, C-5 and
  C-34).
- **FR-017**: The caps MUST be 32 roots, 4,096 entries per root, 128
  candidates and 512 worktree rows across the run, main worktrees included,
  reported in `limits` as the values in force; the root, candidate and
  worktree-row caps MUST apply after canonical sorting and the entry cap in
  listing order. Each cap that drops work MUST be reported as a `scan-limit`
  error naming the cap in `limit` by its `limits` key (`roots`,
  `root_entries`, `candidates` or `worktree_rows`) and carrying `omitted:
  {count, exactness}`: `exact` with the count dropped when the whole
  population was enumerated; `lower-bound` with the count known to be
  dropped when an enumeration that could add to it stopped early (a
  truncated, unreadable or deadline-cut root listing, or an unread worktree
  registry); `unknown` with count null when the population was not
  enumerated, as with the entry cap (POD:217-229; Clarifications, C-9).
- **FR-018**: Worktree rows MUST be ranked by repository rank, the canonical
  position of the candidate that first reached the repository, then by row
  order; rows past the cap MUST keep their registry and branch evidence with
  `dirty`, `ignored_files` and `classification` null, MUST get no
  filesystem task, so that their presence, identity and registration fields
  stay null, and their project rows MUST carry `scan-limit` errors
  (POD:230-234; design D8; Clarifications, C-35).
- **FR-019**: At most four Git children MUST run at once, never two once
  their `common_dir` is known to be the same, one repository's children
  running one at a time. Collection MUST run in two canonical phases, the
  identity and repository-wide probes and then the worktree status probes; a
  repository's second phase MUST start only when every candidate earlier in
  canonical order has completed or failed its identity probe and every
  repository earlier in canonical order has finished its first phase,
  identity probes still being free to start ahead of that point; a
  repository whose first registry record equals its `common_dir` and whose
  checkout no candidate has yet named MUST also wait until every candidate's
  identity probe has completed or failed. In a run in which no child, task
  or root listing reaches its budget and the deadline does not expire, over
  an estate that no other process changes during the run (this feature's
  reading, a condition POD:243-246 does not state; EC-023), the JSON
  document, apart from timestamps and `budget.probe_concurrency`, MUST NOT
  depend on concurrency or completion order (POD:236-246; design D3, item 3,
  and D6; Clarifications, C-28; EC-023).
- **FR-020**: The envelope MUST report `probes: {estimated, performed}`:
  `performed` counting every Git child started, timed-out and stopped ones
  included, and `estimated` counting 1 for the version check, 1 per Git
  candidate, 3 more per distinct repository whose identity was established,
  1 per Git child needed to name the main checkout of a repository whose
  first registry record equals its `common_dir`, and 1 per worktree row
  within the cap that is present and registration-verified (POD:248-254;
  design D3, item 3).

**Isolation**

- **FR-021**: Each candidate MUST be collected inside one boundary
  enclosing, in order, its marker checks, its identity probe, the manifest
  read at `repository.root` (or at the candidate for a row without Git), its
  repository's probes, merge-target resolution, the registration checks and
  status probes of its worktree rows, and classification. A failure inside
  it MUST become data on that candidate's row, coded by the delta's table
  (`manifest-invalid`, `refused`, `os-error`, `undecodable-output`,
  `internal-error` with a message naming the exception class,
  `probe-failed`, `probe-timeout`, `deadline-exceeded`), and MUST NOT
  change, remove or reorder any other row or an earlier scan error. The
  boundary MUST NOT catch an interrupt or an exit request (POD:318-335,
  :344-345; clarifications N1; design D1).
- **FR-022**: Each error MUST be `{code, message, path?}`, with
  `path_valid_utf8` beside a present `path` and a message of at most 200
  characters (for a failed probe, the first line of Git's standard error),
  its `code` one of schema version 1's closed set: the collector table's
  eight, `scan-limit` and `root-unreadable` (Clarifications, C-41).
  Evidence gathered before a failure MUST be kept and every field not
  established MUST stay null; a row whose `errors` is non-empty MUST have
  status `error`, else `ok`; and every candidate entering collection MUST
  yield exactly one row or merge into exactly one existing repository row.
  Without the YAML library the manifest reader needs, each row whose
  directory holds a manifest MUST carry a `manifest-invalid` error naming
  that cause, and the run MUST continue (POD:337-347; Clarifications,
  C-41). How the first line of Git's standard error, like every other string
  that is not a path, is decoded and printed is question Q8 of
  `clarify-questions.md`.
- **FR-023**: In `project overview` alone, a project or family manifest
  with an invalid text encoding MUST be a `manifest-invalid` error on its
  candidate's row, in human and JSON mode alike, never a traceback; the
  other rows MUST still be collected and printed, and the run MUST exit 1
  rather than 2. Every other command MUST keep turning an invalid text
  encoding in any YAML input it reads into a normal refusal, JSON mode
  keeping its structured error output and exit status 2 (PRSD:5-12).

**Classifier and merge target**

- **FR-024**: The merge target MUST be resolved in [R]'s order (the
  manifest's `tracking_branch` less a leading `origin/`; the branch
  `origin/HEAD` names, less `refs/remotes/origin/`; `main`; `master`), from
  the manifest read at `repository.root` (at the row's `path` when that is
  null) and the ref listing alone, spawning no Git child, and MUST be
  recorded as `merge_target: {name, source, sha}`, `source` being
  `manifest`, `origin-head`, `main` or `master` and `sha` that branch's full
  object id from the same listing; the merged set MUST be computed at that
  `sha`. Where the manifest and `origin/HEAD` name different branches that
  both exist locally, the manifest MUST win and one informational
  `merge-target-conflict` finding MUST name both (POD:359-368).
- **FR-025**: When no candidate branch exists, `merge_target` MUST be null,
  the row MUST carry a `no-merge-target` repair finding of severity error
  with no suggestion, the ladder MUST NOT run, and every worktree's
  `classification` MUST be null; when the ref listing failed or timed out,
  the row MUST record that error instead, absence not being established.
  When the manifest read at `repository.root` (or at the row's `path`)
  failed, was refused, timed out or was cut by the deadline, resolution
  MUST NOT fall back to `origin/HEAD`, `main` or `master`: `merge_target`
  MUST be null with no `no-merge-target` finding, the ladder MUST NOT run,
  and the row MUST carry that error. Only a manifest shown absent, or one
  read with no `tracking_branch` or with one that names no local branch,
  lets resolution continue to `origin/HEAD`, `main` and `master`
  (POD:318-324, :359-360, :368-373, :652-653; Clarifications, C-24 and
  C-42).
- **FR-026**: Each worktree row MUST be classified by [L]'s ladder, with its
  names, order and recommendation text, fed from the overview's collected
  evidence and spawning no probe of its own; the ladder MUST run on a row
  only when the row is within the cap, its presence is established, and the
  registry, ref listing and merged set succeeded, `classification` being
  null otherwise except for the rows set to `inspection-error` directly. For
  every row that `project clean <repository.root> --json` inspects, from the
  same working directory and the same refs, the row's classification MUST
  equal that report's. A row's `current`, which decides `merged-current`
  from `merged-removable`, MUST be true exactly when the overview's working
  directory lies inside its path, and null when `present` is null; a
  working directory whose realpath cannot be established is question Q7 of
  `clarify-questions.md` (POD:375-386; DI:425-427, :778; Clarifications,
  C-25).
  Whether this feature realizes the exception to that equality which
  `add-project-clean-cache-disposal` (#24) proposes is question Q17 of
  `clarify-questions.md`.

**Findings and attention**

- **FR-027**: Every finding MUST carry exactly one code, category, severity
  and evidence source from the delta's attention table, the complete list of
  22 codes for schema version 1, and the suggested command that table names,
  subject to FR-031 to FR-035 and FR-041 (POD:421-449).
- **FR-028**: A finding that reports a worktree's classification MUST carry
  the ladder's recommendation text as its `message`, and every other finding
  a fixed sentence (design D3, D4 and D5). A worktree that reaches the
  `remote-gone` rung, its upstream's remote-tracking ref gone, and whose tip
  the merged set shows to be an ancestor of the merge target MUST be
  classified as [L] classifies it, `merged-removable` or `merged-current`,
  with that class's finding, message and suggestion and no further probe;
  only such a worktree whose tip is not an ancestor MUST be `remote-gone`,
  with the ladder's own recommendation and the read-only command as its only
  suggestion (Brett Heap's ruling of 2026-10-09). `protected-default` MUST
  produce no finding by itself apart from FR-041's. Row errors and scan
  errors MUST NOT be findings and MUST display in the repair category
  (POD:451-463).
- **FR-029**: A finding of severity `error` MUST make the exit status 1;
  `warning` MUST do so only under `--strict`; and `info` MUST never affect
  it (POD:465-466).
- **FR-030**: `--attention` MUST show every scan error, every row with
  status `error` and every row with at least one repair, preserve or
  housekeeping finding, and MUST hide informational findings within a shown
  row. It MUST change only the display, never what is collected, the summary
  counts, the JSON document or the exit status, and `--attention --json`
  MUST print the full envelope (POD:466-471).

**Suggestions and gates**

- **FR-031**: A suggestion MUST be an argument vector, exactly `["project",
  "clean", "<root>", "--all-safe"]` or `["project", "clean", "<root>"]`,
  `<root>` being the absolute canonical `repository.root`; it MUST never
  name a project by bare name and never include `--apply` or `--yes`. A row
  whose `repository.root` is null, or whose root or common directory is not
  valid UTF-8, MUST get no clean suggestion, the latter carrying an
  `unsupported-path-bytes` finding instead. A row's `suggested_command` MUST
  be the `--all-safe` form when one of its findings suggests it, else the
  read-only form when any finding suggests it, else null (POD:484-492).
- **FR-032**: The `--all-safe` form MUST be suggested only for a worktree
  [L] classifies `merged-removable` that passes, in [G]'s order, the gates
  the overview can evaluate from its own evidence: `main-worktree`,
  `unsupported-path-bytes`, `registration-mismatch` and `locked-worktree`,
  whose first failure replaces the housekeeping finding with its own while
  the classification stays (a row whose registration disagrees being
  `inspection-error` already, by FR-007, that gate keeps [G]'s order without
  deciding a `merged-removable` row; Clarifications, C-26); then
  `unstarted-branch` or `reflog-unavailable`. The index gates
  (`contains-submodule`, `hidden-local-state`) MUST remain exclusions only
  the batch applies (POD:494-502, :525-526; design D5).
- **FR-033**: For every row that gate checks, the branch's reflog,
  `logs/refs/heads/<branch>` under `common_dir`, MUST be read by one bounded
  filesystem read of at most 64 KiB (65,536 bytes), never by a Git child,
  and decided as [G] decides it: the anchor is the last surviving entry
  whose old object is all zeros or whose message begins `branch: Created
  from` or `branch: Reset to`; a movement is an entry after the anchor, or
  any entry when no anchor survives, whose old and new objects are non-zero
  and differ; a branch whose last entry's new object differs from its head
  is `reflog-unavailable`, this test first; otherwise a branch with a
  movement passes, and one whose anchor survives with no movement after it,
  the anchor's new object equal to its head, is `unstarted-branch`. A reflog
  that is missing (`ENOENT` or `ENOTDIR`), empty (0 bytes), read to its 64
  KiB bound, or whose surviving entries cannot decide, no anchor and no
  movement surviving included, MUST make that row `reflog-unavailable`, a
  read that returns 65,536 bytes having reached the bound, so that a reflog
  of 65,536 bytes or more is `reflog-unavailable` and one of 65,535 bytes is
  decided by its entries; any other operating-system error MUST record an
  `os-error` and make the row `inspection-error`; and a read not finished
  within the filesystem budget MUST leave the row unprobed for the gate,
  recording `probe-timeout` or `deadline-exceeded`, never making it
  `inspection-error`. Either reflog code MUST keep the `merged-removable`
  finding with the read-only suggestion (POD:502-525; design D5;
  Clarifications, C-22).
- **FR-034**: The `--all-safe` form MUST also be withheld for every worktree
  of a repository whose batch plan [G] would refuse as
  `inspection-incomplete` (any worktree row `inspection-error`, a row whose
  presence or registration read failed or was cut included, or any row
  unprobed because its reflog read did not finish) or as `inspect-cap` (more
  worktree rows than the batch's row cap), each computed from the overview's
  own evidence, and of a repository with any row the overview's own cap or
  deadline left unclassified; those findings MUST suggest the read-only
  form. A repository's worktree rows, for both row caps, MUST be every
  registry entry of the repository, the main worktree and the rows with
  `present: false` included, within the overview's 512-row cap or past it
  (Clarifications, C-46). A repository with more worktree rows than the
  report's row cap MUST have its read-only suggestions limited by
  `inspect-cap`; and when more of one repository's `merged-removable`
  worktrees keep the `--all-safe` form than the batch's target limit, each
  MUST keep it, limited by `target-cap` (Clarifications, C-45). `project
  clean` MUST remain free to recompute, show and confirm its own plan and to
  exclude a suggested worktree (POD:526-537, :563-564; design D5).
- **FR-035**: Each finding MUST carry `suggestion_gate`, null unless a gate
  withheld or limited its own suggestion, else the first applicable code in
  the order of the delta's gate table (`target-not-repository-root`,
  `unsupported-path-bytes`, `inspection-incomplete`, `inspect-cap`,
  `scan-limit`, `deadline-exceeded`, `unstarted-branch`,
  `reflog-unavailable`, `target-cap`), and `suggestion_gate_rows`, the
  repository's worktree-row count as FR-034 counts it when that code is
  `inspect-cap`, else null. The finding's `message` and the human text MUST carry the code's
  fixed remedy from that table, its numbers (the batch's row cap, the
  report's row cap and the batch's target limit) taken at run time from the
  shared constants that [G]'s "Clean bounds its Git work and reports
  omitted work" defines, as `limits` reports them, never from a clean plan,
  and the `--root <repository parent>` remedy naming the parent
  directory of `repository.root`. A root left null by `unsupported-layout`
  or `main-worktree-missing` MUST carry no gate code (POD:539-562; design
  D5; Clarifications, C-11 and C-46).

**JSON document**

- **FR-036**: `--json` MUST print exactly one JSON document with
  `schema_version: 1` and exactly the fields the delta lists for the
  envelope, the root object, the project row, `repository`, `git`, the
  worktree row, the finding, `summary` and the error object, every one
  always present (an error's `path` optional, and `limit` and `omitted` only
  on `scan-limit` and `deadline-exceeded` errors); `limits` MUST carry
  `roots`, `candidates`, `worktree_rows`, `root_entries`, `ignored_entries`,
  `status_records`, `ignored_samples`, `batch_row_cap`, `report_row_cap` and
  `targets`, the last three read from the shared constants that [G]'s
  "Clean bounds its Git work and reports omitted work" defines and never
  from a clean plan, and `budget` MUST carry `probe_timeout_seconds`,
  `invocation_timeout_seconds` and `probe_concurrency`. The `git` object
  MUST come from the evidence already held for the checkout at `path`, with
  no probe of its own, and its `tracking_freshness` MUST be the text `local
  refs only; no fetch`. Each field's type and the condition under which it
  is null, and what each `summary` count counts, MUST be those of the
  packet's JSON contract that the proposal adopts, except where the delta,
  design D11 or two of these clarifications, C-23 (a failed or cut task) and
  C-35 (rows past the cap), both from design D8, change them (POD:607-648;
  design D11; Clarifications, C-13, C-32 and C-40). Whether a worktree row
  also shows feature 004's partial-removal note is question Q5 of
  `clarify-questions.md`.
- **FR-037**: Integers MUST be JSON integers, object ids full lowercase
  hexadecimal, times RFC 3339 UTC with a `Z` suffix, and durations integer
  seconds in fields ending `_seconds`. `null` MUST mean unknown or not
  established, apart from the nulls that mean none (Clarifications, C-40),
  and never stand for `false`, `0` or an empty list, an empty
  `findings` on an error row meaning that no finding was computed;
  `completeness` MUST be `incomplete` exactly when `scan_errors` is
  non-empty or any row has status `error`; the envelope's `observed_at` MUST
  be the collection start, and a finding's `observed_at` the time its
  deciding probe completed; and enums MUST be closed within a version,
  adding a field or an enum value being additive, and a rename, a removal
  or a change of type or meaning MUST increment `schema_version`.
  Projects MUST be ordered by the bytes of `path`, worktrees main first and
  then by path bytes, findings by checkout path and then code, row errors in
  their candidate's step order, and scan errors in canonical collection
  order (POD:619-621, :650-658; design D6; Clarifications, C-12 and C-40).
- **FR-038**: Every path MUST be parsed and emitted as [E] and [P] define:
  exactly when it is valid UTF-8, with every code point of Unicode general
  category Cc, Cf, Zl or Zp, as the running interpreter's Unicode database
  reports it, escaped by JSON; otherwise escaped, each undecodable byte as
  `\xHH`. Every serialized path MUST carry its own validity flag
  (`path_valid_utf8` beside each `path`; `root_valid_utf8` and
  `common_dir_valid_utf8` in `repository`), false exactly when that path is
  not valid UTF-8 and null only beside a null path; and a worktree path,
  root or common directory that is not valid UTF-8 MUST get an
  `unsupported-path-bytes` finding and contribute to no clean suggestion
  (POD:660-672; design D11). How strings that are not paths are decoded and
  printed is question Q8 of `clarify-questions.md`.
- **FR-039**: Under `--json`, an exit status 2 other than an argument error
  MUST print only `{"error": "<message>", "code": "<code>"}`, the code being
  `git-too-old` or `git-unavailable` for a version refusal, and otherwise
  that of an exception raised outside the per-candidate boundary, mapped by
  its kind: a refusal gives `refused`, an operating-system error `os-error`,
  and any other exception `internal-error` with a message naming the
  exception class, each with exit status 2 and no traceback. Without
  `--json`, a refusal or an operating-system error MUST keep the baseline
  report, `REFUSED: <message>` on standard error (feature 002,
  `contracts/project-new.md:121`, "Streams"), and an exception of any other
  kind MUST also exit 2, never with the interpreter's default 1. An argument
  error MUST print the command-line parser's usage message on standard error
  and no JSON (POD:675-679, :705-707; DI:1083-1090). POD:705-707 says only
  "an exception" and gives `internal-error`; this feature's reading, which
  narrows that scenario's WHEN, is an exception of the kind the collector
  table maps to `internal-error`, the other two kinds having the outputs
  above, and the scenario's test keeps its name. A failed write to the
  output, and the output's encoding, are question Q12 of
  `clarify-questions.md`.

**Local and read-only**

- **FR-040**: The overview MUST open no network connection and make no
  filesystem or Git mutation: no fetch, pull, reset, bootstrap, validator
  run or file write; no worktree created, pruned, repaired, locked or
  unlocked; and no index rewritten, every Git child running read-only as [E]
  defines. It MUST read no credential file and no profile data the scan does
  not need, and MUST keep no state beyond one invocation. Ahead, behind and
  merge evidence MUST be presented as observations as of the last fetch, and
  both outputs MUST say so (POD:710-717).

**Default-branch health**

- **FR-041**: For a checkout [L] classifies `protected-default`, the
  overview MUST keep that classification and add, from evidence it already
  holds and with no further probe, every finding that applies: `dirty`
  (preserve, warning) when the checkout is dirty; and at most one, tested in
  this order, of `unpublished` (preserve, warning) when no upstream is
  configured and the ref listing holds a remote copy of the merge target,
  `remote-gone` (preserve, warning) when its upstream is gone, `diverged`
  (preserve, warning) when it is both ahead of and behind its upstream,
  `unpushed` (preserve, warning) when it is only ahead, or `remote-ahead`
  (informational, info) when it is only behind. Each MUST carry the message
  design D4 fixes, `suggested_command: null` and `suggestion_gate: null`,
  and MUST NOT set the row's `suggested_command`. A merge-target branch with
  no remote copy at all MUST raise no `unpublished` finding, ignored files
  in that checkout MUST raise no finding, and a merge-target checkout whose
  status probe failed, timed out or was cut by the deadline MUST be
  `inspection-error`, with that code's repair finding of severity error and
  none of these findings (POD:725-742; design D4).

**Exits and signals**

- **FR-042**: The overview MUST exit 0 when `completeness` is `complete` and
  no finding has severity `error`; 1 when the result is incomplete, a
  finding has severity `error`, or `--strict` is given and a finding has
  severity `warning`; 2 for an invalid invocation, an exception raised
  outside the per-candidate boundary, or a Git refusal; and 130, 143 or 129
  on SIGINT, SIGTERM or SIGHUP. On 0 or 1 the full result MUST be printed,
  and a root problem MUST never cause status 2 (POD:762-768).
- **FR-043**: The overview MUST run [E]'s version check once per invocation,
  after the deadline is set and before any root is listed, and MUST refuse a
  Git older than 2.36 with `git-too-old`, and a missing `git`, a failed or
  timed-out version child or an unparseable version with `git-unavailable`,
  each with exit status 2, a message naming the 2.36 minimum, such as the
  packet's "project overview needs Git 2.36 or newer; found 2.34.1"
  (DI:322-323), and no other Git child; such a refusal MUST never be
  reported as an incompleteness (POD:770-776).
- **FR-044**: On SIGINT, SIGTERM or SIGHUP the overview MUST stop
  scheduling, terminate and reap every child as FR-011 states, abandoning
  one still unreaped 2 s after SIGKILL, print no result document, print
  `Cancelled.` to standard error on a best-effort basis (Clarifications,
  C-47), and exit with that signal's status, which takes precedence over 1;
  a signal MUST never become a row error, and a Git child MUST NOT outlive
  the run, except one abandoned while still unreaped 2 s after SIGKILL
  (EC-001) and under EC-002. A signal that arrives while the result is
  being written is question Q15 of `clarify-questions.md` (POD:776-781;
  clarifications N1; design D1).
  Whether its Git children start with those three signals blocked, as
  design D1 has it, is question Q16 of `clarify-questions.md`.

**Human report**

- **FR-045**: Without `--json`, the overview MUST print to standard output,
  for each shown row, one header line with the name and the absolute path;
  one line per shown finding with its category, code and message, followed
  by the worktree path for a worktree's finding; and, when the row has a
  suggested command or a gate decided it, one `next` line carrying that
  command, shell-quoted or in the `$'...'` form, or `none` where a gate left
  no command (Clarifications, C-44), followed by `(withheld: <remedy>)` when
  a gate removed the `--all-safe` form or every clean suggestion, or by
  `(limited: <remedy>)` when a suggestion is given but capped, the deciding
  gate chosen as design D10 states. Rows, the findings and row errors within
  a row, and the `Incomplete:` lines MUST follow the JSON document's order
  (FR-037; Clarifications, C-43). Row errors MUST display in the repair
  category; one
  `Incomplete:` line MUST follow per scan error; and the summary line MUST
  always be printed, giving the counts of projects, errors and findings by
  category and stating that findings reflect local refs as of the last
  fetch, and saying that nothing needs attention under `--attention` when no
  row is shown; a complete scan that finds no project says so through that
  line, which then reads `0 projects`, and exits 0 (POD:722; DI:1097-1098;
  design D10). A path holding a code point of FR-038's categories or an
  undecodable byte MUST print in the `$'...'` form, each such code point
  written `\uXXXX`, or `\UXXXXXXXX` above U+FFFF. The layout and fixed lines
  MUST read as design D10 fixes them, their fixed text in ASCII, while
  interpolated names, paths and numbers follow FR-038 and [P] (POD:672-675,
  :722, :802-817; DI:1097-1098; design D4, D6 and D10; Clarifications, C-43
  and C-44).
- **FR-046**: When standard error is a terminal, and only then, the overview
  MUST write one `Scanning N roots...` line to standard error before
  listing, N being the number of roots given, or of the defaults, before
  canonicalisation, standard output being identical either way, and every
  human write to standard error MUST be best-effort (POD:817-819; design D2
  and D10; Clarifications, C-36 and C-47).

**Scope, documentation and tests**

- **FR-047**: The feature MUST add the `overview` subcommand and change no
  other subcommand's output, flags or exits beyond what feature 004 changes;
  MUST add no flag outside `overview`, no environment variable, file or
  setting that changes a limit or a time (the values in force being reported
  in `limits` and `budget`), and no new dependency, manifests being read
  through the existing YAML requirement; and MUST keep running on every
  runtime version the README supports and CI runs (proposal, Impact and
  Corrections; design, Non-Goals and Migration Plan; OQ-8).
- **FR-048**: The README MUST gain a section for `project overview` covering
  roots and `PROJECTS_DIR`, the caps, `--attention`, `--strict`, the exits,
  the JSON envelope, and that a suggestion is advice to review, not
  permission; how to check one project (`project overview --root <dir>`,
  replacing the closed PR #2's doctor health); that `git fetch` refreshes
  merge evidence; that roots on a Windows drive mounted into WSL2 can
  truncate on every run; that a filesystem call stuck in the kernel can hold
  process exit; and that a merged worktree whose upstream was deleted gets
  the gated `--all-safe` suggestion like any merged worktree, while an
  unmerged `remote-gone` one gets only the read-only `project clean <root>`,
  which reviews it (proposal, Impact; design, Risks). Whether `AGENTS.md`
  says so too is question Q4 of `clarify-questions.md`.
- **FR-049**: Automated tests over temporary fixtures MUST cover every delta
  scenario with at least one test named after it, a skipped test not
  counting, in human and `--json` form, with a scratch home directory,
  `PROJECTS_DIR` set or unset explicitly, networking disabled and the
  zero-mutation snapshots taken before and after. Networking disabled MUST
  mean that in-process runs install an audit hook that fails the test on
  `socket.connect`, that the counting wrapper checks every Git child as
  below, and that the partial-clone fixture's `remote.origin.uploadpack`
  names a logging script that never runs (design D13; CMD:227-231); a
  network namespace MAY be added where an unprivileged one can be made. A
  counting `git` wrapper first on PATH MUST record each child's arguments,
  directory, process group and start and end times, MUST be able to hold a
  chosen status probe, and MUST assert that no argument vector fetches,
  pulls, pushes or reaches a remote, that every one carries the seven
  protocol pins, and that none of the seventeen scrubbed names reaches a
  child, a child being a process the overview starts (Clarifications, C-34);
  the concurrency limits MUST be checked from that log's intervals, and
  fixtures MUST lie outside every Git work tree. A test MUST NOT need a
  running filesystem monitor: the packet's fixtures that held the status
  probe through a `core.fsmonitor` hook (its probe-timeout and
  bounded-concurrency fixtures) MUST hold it through the wrapper instead,
  since [E] pins `core.fsmonitor=false` on every status probe. A hung
  filesystem call MUST always be tested by an injected slow call, and a FUSE
  fixture MUST run in addition where a mount can be made, only that variant
  being skipped, with its reason, where none can; where the injected call
  stands in for a hung main checkout ("A repository root on a hung mount"),
  the wrapper MUST also hold each Git child that runs in that checkout
  (design D13). The device-and-inode deduplication of roots and candidates,
  and the canonically first spelling, MUST be tested through an injected
  file-status call that reports one device and inode for two realpaths. Only
  the invocation-deadline scenario MUST shorten the deadline and the
  per-child budget, in-process and keeping their ratio, the grace and the
  reap wait staying 2 s each, so that its bound is the shortened deadline
  plus 4 s from the moment the deadline is set (design D13); a cap or
  concurrency fixture that asserts an uncut run MUST fail, never skip, when
  its run reports a `probe-timeout` or a `deadline-exceeded`. A fixture that
  depends on a permission being refused MUST be skipped, with that reason,
  when the tests run as root. Non-UTF-8 path tests MUST run on Linux, where
  every CI job runs, and be skipped on macOS with that reason, the `$'...'`
  form asserted as a string; the signal tests MUST assert that every child's
  process group is gone, apart from abandoned ones; every functional
  requirement, or part of one, that no delta scenario exercises (among them
  FR-004's candidates that are not family holders, FR-010, FR-020's
  `estimated` count, FR-021's `refused` and `undecodable-output` codes,
  FR-022's message bound, FR-033's reflogs of 65,535 and 65,536 bytes,
  FR-037's order and FR-039's `refused` and `os-error` outputs) MUST be
  covered by at least one test as well, the feature's traceability record
  naming it; and every existing test on `main` when the feature is
  implemented MUST keep passing unchanged (proposal, Impact; design D13;
  Clarifications, C-6).

### Key Entities *(include if feature involves data)*

- **Root**: a directory the scan starts from: its canonical `path` and
  validity flag, `source` (`argument`, `environment` or `default`), `state`
  (`listed`, `truncated`, `absent`, `unreadable` or `omitted`) and
  `entries`, the count read, null when it was not listed.
- **Candidate**: a root or an immediate entry of one, canonical and
  deduplicated, on which a marker holds; its kind is `family-holder`,
  `project-manifest` or `single`, and its canonical position ranks
  repositories and decides which candidate reached a repository first; rows
  are ordered by the bytes of their `path`.
- **Project row**: one per repository identity, or per candidate without
  Git: `name`, `path` and its flag, `kind`, `repository`, `merge_target`,
  `git`, `worktrees`, `findings`, `suggested_command`, `status` (`ok` or
  `error`) and `errors`.
- **Repository identity**: `{root, common_dir, dev, ino}`, with
  `root_valid_utf8` and `common_dir_valid_utf8`; `root` is null for a bare
  repository, a submodule checkout, a gitfile checkout that cannot be named
  and a missing main worktree.
- **Worktree row**: one registry entry, the main worktree included: the
  worktree identity `{path, dev, ino, admin_id}`, `present`, `locked`,
  `prunable`, `current`, branch evidence (`branch`, `head`, `upstream`,
  `upstream_oid`, `ahead`, `behind`, `remote_present`,
  `merged_into_target`), `dirty`, the bounded ignored-file count with its
  truncation flag and samples, and `classification`, one of [L]'s fifteen
  classes or null.
- **Merge target**: `{name, source, sha}`, the local branch whose ancestry
  proves a worktree merged, resolved in [R]'s order.
- **Finding**: one code with its category (repair, preserve, housekeeping or
  informational), severity (error, warning or info) and evidence source; its
  `checkout` (a worktree identity with its flag, or null for a
  repository-level finding), `message`, `observed_at`, `suggested_command`,
  `suggestion_gate` and `suggestion_gate_rows`.
- **Suggestion**: an argument vector naming `repository.root`, the
  `--all-safe` form or the read-only form; advice to review, never
  permission.
- **Gate**: a code that withheld or limited a finding's suggestion, from the
  delta's gate table, with its fixed remedy.
- **Reflog anchor and movement**: as feature 004 names them; with the head
  test they decide `unstarted-branch` or `reflog-unavailable` at the gate.
- **Row error** and **scan error**: `{code, message, path?}`, with a
  validity flag beside `path`; `scan-limit` and `deadline-exceeded` errors
  add `limit` and `omitted: {count, exactness}`, exactness being `exact`,
  `lower-bound` or `unknown`.
- **Envelope**: the one versioned document: `schema_version`, `observed_at`,
  `roots`, `limits`, `budget`, `probes`, `projects`, `relationships`,
  `summary`, `completeness` and `scan_errors`.
- **Summary**: the counts of project rows, error rows included; of the
  distinct repositories whose identity was established; of worktree rows,
  main worktrees included; of row errors plus scan errors; and of findings
  by category; over the whole collection, whatever `--attention` shows
  (Clarifications, C-40).
- **Bounds**: the 60 s deadline, the 5 s budget per Git child and per
  filesystem call, the four caps and four-wide concurrency, reported as the
  values in force in `limits` and `budget`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In every fixture within the caps, each candidate yields
  exactly one row or merges into exactly one repository row, each repository
  appears once however many of its worktrees are candidates, and each
  registered worktree, external ones included, appears once under it, one
  row per registry entry (EC-031).
- **SC-002**: In 100% of runs over the feature's fixtures with networking
  disabled as FR-049 defines it, the audit hook records 0 connections, the
  partial-clone fixture's logging script never runs, and the before and
  after snapshots (refs, the worktree registry, each checkout's status, each
  index file's modification time and the directory tree under every root)
  are identical; a counting `git` wrapper finds the seven protocol pins on
  100% of the overview's Git children (Clarifications, C-34), 0 scrubbed
  names in any child's environment, and 0 argument vectors that fetch,
  pull, push or reach a remote.
- **SC-003**: For 100% of worktree rows that `project clean <root> --json`
  inspects from the same directory at the same refs, the overview's
  classification equals clean's, and for 100% of repositories with a merge
  target its name equals the one clean reports.
- **SC-004**: 0 suggestions carry `--apply` or `--yes` or name a project by
  bare name; 0 rows with a null root, or a root or common directory that is
  not valid UTF-8, carry a clean suggestion; and in every fixture, each
  worktree whose finding carries the `--all-safe` form with no withholding
  gate is, in the preview that suggestion runs when that preview's own
  deadline does not cut it, either selected or excluded only as
  `deferred-target-cap`, `contains-submodule` or `hidden-local-state`, or,
  when that preview's own index-gate read fails or times out, made
  `inspection-error` in a preview that is then incomplete (CLN:800-803).
- **SC-005**: Every run ends within 64 s of the moment its deadline is set,
  plus rendering (Clarifications, C-48), except while a filesystem call
  stuck in the kernel is outstanding; no Git child
  is waited for more than 4 s past its budget; and the counting wrapper's
  interval log never shows more than four of the overview's Git children at
  once, nor two in one repository (Clarifications, C-34).
- **SC-006**: 100% of runs in which a cap, a budget or the deadline cut work
  report `completeness: "incomplete"`, name each cut in a row or scan error,
  with `omitted` wherever a population was dropped, and exit 1 unless a
  signal decides.
- **SC-007**: For every fixture collected without a cut, the JSON at probe
  concurrency 1 and at 4 is byte-identical apart from timestamps and
  `budget.probe_concurrency`, and the same worktree rows are probed.
- **SC-008**: In every fixture with one failing candidate (unreadable, a
  wrong-kind manifest, a manifest that is not valid UTF-8, a missing YAML
  library, a failing Git child), every other row's JSON object equals its
  object in the same fixture without that failure, apart from observation
  times; 0 tracebacks are printed; and the exit status is 1, never 2.
- **SC-009**: In 100% of `--json` runs that exit 0 or 1, standard output
  parses as exactly one JSON document with `schema_version: 1` carrying
  every field the delta lists; in 100% of `--json` runs that exit 2 other
  than an argument error, it is only `{"error": "<message>", "code":
  "<code>"}` (FR-039); every valid UTF-8 path round-trips exactly; and
  every other path carries a false validity flag and feeds no suggestion.
- **SC-010**: Human output contains 0 raw characters of general category Cc,
  Cf, Zl or Zp and 0 undecodable bytes from a path, and every fixed line,
  message and remedy matches design D3, D4, D5 and D10 and the delta's gate
  table character for character in its fixed text, which is ASCII.
- **SC-011**: Every run's exit status is the one FR-042 gives; after SIGINT,
  SIGTERM or SIGHUP, 0 of the overview's child process groups remain, apart
  from children abandoned while still unreaped 2 s after SIGKILL, and no
  result document has been printed.
- **SC-012**: Each of the 63 delta scenarios has at least one automated test
  named after it that runs, a skipped test not counting; every test on
  `main` when the feature is implemented keeps passing unchanged; the CI
  jobs stay green; the requirements file gains no dependency; and no
  subcommand but `overview` changes its output, flags or exits.
- **SC-013**: The README's overview section covers 100% of FR-048's items,
  confirmed by a review checklist with one line per item, so that a reader
  of that section alone can say how to scan the default roots, check one
  project, read `--attention`, `--strict` and the exit statuses, and
  refresh merge evidence, and why a suggestion is advice and not
  permission.
- **SC-014**: The kept canonical scenario "Manifest is not valid UTF-8 text"
  still passes for `project status --json`, and the overview's carve-out
  scenario passes.

## Assumptions

- The spec names flags, codes, JSON fields, Git settings, standard streams
  and exit statuses because the ratified deltas fix them as behaviour, which
  outranks the template's advice to stay technology-agnostic, as in features
  002 to 004; its readers own, review and use `project` and the tools that
  read its JSON. It names no function, module or file of the implementation.
- `.specify/memory/constitution.md` is still the unfilled template, so the
  ratified change alone governs this feature.
- No clarification marker is used: the change specifies the behaviour, and
  the spec follows it as ratified. The points this spec settles from the
  change's own text are listed under Clarifications; the questions genuinely
  left open are in `clarify-questions.md`, for Brett Heap, and none of them
  alters a requirement until he answers.
- The caps and budgets stand as governance task 2.1 measured them on
  2026-10-09: the caps' worst case takes 48.3 s of the 60 s deadline on a
  Linux filesystem; a Windows drive mounted into WSL2 was not measured
  (proposal, OQ-4; design, Risks).
- The change pins its code citations at `da33d92`. Features 003 and 004
  change `project` and the tests after it, and the CI change of `e9d6711`
  (#32) moved the two workflow lines the change cites,
  `.github/workflows/tests.yml:10` and `:18`, to lines 9 and 17, so this
  spec cites no line of `project`, `README.md` or the workflow as `main` has
  them, its only lines of feature 004's `project` being those of EC-031,
  EC-033 and the Dependencies at `96a08d4`, and the plan re-pins every
  citation against the `main` of its day (proposal, "Dependencies and
  Sequencing").
- Feature 004's names (classifications, gate and refusal codes, row error
  codes, `schema_version`, exit statuses, the shared constants) are taken
  from its spec, data model and contract at `d81b3d9`, apart from EC-031 and
  EC-033, which read its branch's head, `96a08d4`; that head's documents
  change after `d81b3d9` by the tier tags, file and verify fields and ticks
  of `tasks.md`, two additions to `plan.md` and its doc round 6 (rulings
  R-55 to R-57 and R-59 to R-62, with the items of R-53 and R-54 that they
  settle), none differing from `6ae927f`'s but in the ticks of `tasks.md`,
  and its code, which changed after `a32d20b` by its T047, by lane G's
  follow-up to its evidence model and by its US1 plan lane (`2733dea`), has
  its tasks T001 to T040 and T047 to T053 built (47 of 133), among them its
  five incremental parsers, its child handle, its driver and its evidence
  model (merged as `cce8dbd`), and none of it is on `main`; where the change
  and feature 004 differ for the overview, the change governs, and the plan
  reconciles against feature 004's text at the state that question Q2 of
  `clarify-questions.md` settles.
- "Every existing test" means the suite on `main` when the feature is
  implemented: 96 tests at `961c405`, still 96 at `e45155a`, plus feature
  004's. Two test conditions are this spec's own, not the change's: a test
  named after each delta scenario, for the traceability record features 002
  to 004 keep, where design D13 asks only for at least one test per
  scenario; and existing tests passing unchanged, which follows from the
  overview changing no other subcommand's output, flags or exits (design,
  Migration Plan).
- Exact human text is fixed in design D3, D4, D5 and D10 and in the delta's
  gate table, and is cited, never restated in another form; the texts quoted
  here are verbatim from the deltas or the design.
- Where a repository-level finding (a null `checkout`) sorts among a row's
  findings, which FR-037's order leaves open, is fixed once by the plan,
  since the determinism of FR-019 needs only that it be fixed.
- Nothing migrates for users: `project overview` is new and no other
  subcommand changes. Rollback is a revert of feature 005's merge, no data,
  configuration or other subcommand depending on the overview (design,
  Migration Plan; Clarifications, C-49).
- The order departure is recorded with its time: this feature was created
  before feature 004 merges on Brett Heap's word of 2026-10-11T16:14:21Z,
  for the specify step only (header; change `tasks.md` 3.1 and Speckit
  Handoff).
- workBenches' `onp` and any other installed copy of `project` gain the
  overview only when their owners move their pins; this feature edits
  nothing outside this repository (proposal, "What This Repository Does Not
  Own").

## Dependencies

- **Feature 004** (`004-project-clean-all-safe`, change 1
  `add-project-clean-all-safe`, issue #9), a plan-stage dependency. The plan
  waits for feature 004's code and for Brett Heap's word, as recorded with
  the specify step; which state of feature 004 must exist first is question
  Q2 of `clarify-questions.md`. The overview drives feature 004's runner as
  change 1's clarification N2 shapes it, which feature 004's FR-062 commits
  it to share (several children at once through one environment scrub,
  termination path and set of parsers) and its plan and tasks realize as:
  the child handle (start a Git child in its own process group under the
  scrubbed environment, expose its standard output and standard error, stop
  its group with the 2 s grace, reap it); the one-wide driver of that
  handle, the serial path every other subcommand uses, beside which the
  overview drives up to four handles from its own loop (this change's
  clarification N1); and the pure incremental parsers of the status,
  registry, ref-listing and merged-set outputs, fed chunks and doing no I/O.
  Of the four, only the status parser reports a reached record bound (its
  65th ignored or 4,097th record); the registry parser
  (`WorktreeListParser`, `project:1783`), `RefParser` (:1829) and
  `MergedSetParser` (:1869) keep every record, each documented "No bound" at
  `96a08d4`, which change 1's design leaves unbounded for the last two: its
  D2 (`design.md:164-176` at `96a08d4`) gives a bound to the status parser
  alone, and its D6 says of row 6 only that it "yields every branch's head"
  (`design.md:291`) and of row 7 nothing (lead ruling R-70(b)). FR-015's
  keep-filter, which keeps only the local heads, `origin/HEAD`, the remote
  refs named as upstreams and one flag recording whether a remote copy of
  the merge target exists (POD:196-200), is therefore this feature's own to
  build, as R-54's X-2 leaves to it the factoring of `start_child` and
  `conclude` out of `run_bounded`, and feature 004 adds no hook for it.
  Feature 004's data
  model at `d81b3d9` records that handle, plan-stage detail for this
  feature, as its "Child handle" entity, with the states `running`,
  `terminating`, `killing`, `reaped` and `abandoned`, the kinds `probe`,
  `removal` and `delegate` (the `git branch -d` child), of which the
  overview starts only `probe` handles, and a termination that never blocks
  (lead ruling R-30); and, as its "Invocation" entity, the state of one run
  of `project`: the per-child budget (5 s under `clean`, 15 s otherwise),
  the clock, the counters, the memos, and the phase by which the driver
  reads the signal slot, raising `Interrupted` only in phase `planning` or
  on a second SIGINT in phase `reconciling` (lead rulings R-44 and R-47).
  Its contract fixes a human message for each refusal code that had none,
  which the plan may adapt for `git-too-old` and `git-unavailable`, naming
  `overview` where it names `clean`; beside `clean`'s two texts it gives
  command-neutral ones for a `status` or `doctor` row, "Git VERSION is older
  than 2.36; repository inspection needs Git 2.36 or later." for
  `git-too-old` and its counterpart for `git-unavailable` (lead ruling
  R-48). It also fixes one message per row-error code (lead ruling R-45),
  the `probe-failed` one being `OPERATION failed: DETAIL`, DETAIL one of
  `exit N`, `signal N`, `cannot spawn (STRERROR)` and `unparseable output`,
  with no line of Git's standard error, which FR-022 takes from change 2
  (POD:337-338). It also reads feature 004's evidence model [E] with the
  version check, the seventeen-name scrub and the pins, the ladder [L] as a
  pure function of a row's evidence, the gates and refusal codes [G] with
  the shared constants (the 128-row and 256-row caps and the 16-target
  limit, which feature 004 keeps in its own constants table and the overview
  reports as `batch_row_cap`, `report_row_cap` and `targets`), Git-first
  resolution [R], the path rules [P] and the 1 MiB manifest read (proposal,
  "Dependencies and Sequencing"; `add-project-clean-all-safe` clarifications
  N2 and design D2). Lane openRepoProject-2's ruling R-54 (2026-10-20) has
  feature 004 separate each evidence step's reads from a pure decision that
  this feature's own loop can call, the evidence keyed by device and inode,
  with the repeated identity probe at the root skippable; that split is
  built in feature 004's `project` at `96a08d4` (commit `7d70b02`, a
  refactor with no behaviour change). The deciders run no Git child and make
  no filesystem call: `presence_from_lstat` (`project:2278`),
  `registration_verdict` (:2469), `main_worktree_decision` (:2384) and
  `row_evidence` (:2656), with `gitdir_line` (:2343) and `shared_paths`
  (:2634). The wrappers read in the evidence's order and keep their return
  shapes: `main_worktree` (:2423), `verify_registration` (:2497),
  `inspect_repository` (:2534) and `worktree_rows` (:2762), which also takes
  the registry records to build rows for (`records=None`, R-53(d)), its
  reads of one row being `_read_row` (:2725). The memo of
  `inspect_repository` is keyed by the common directory's (dev, ino)
  (:2580-2583), and row 5, the repeated identity probe at the main worktree,
  sits behind the keyword `repeat_identity_at_root`, on by default, a result
  without it being memoized apart (:2534, :2597). Feature 004's `tasks.md`
  at that head still records no such split: it names R-54 only as the X-2
  and X-3 of its tasks (:1846, :1172). The driver's start and outcome rules
  stay inside feature 004's one-handle driver, unchanged at `96a08d4`, and
  this feature's plan factors them out, without changing behaviour, after
  feature 004 lands.
- **Change 1's archive order**: change 2 archives after change 1. This
  feature realizes change 2's MODIFIED `project-review-safety` requirement,
  not change 1's `project-clean-review-safety` (proposal, Capabilities;
  design, Migration Plan step 5).
- **Open items elsewhere that do not block this spec**: change 1's open
  question 2 (the lane's LQ-2: squash merges and a local patch-equivalence
  proof) is still before Brett Heap and deferred, on the lead's
  recommendation, to a follow-on change, which the overview would inherit
  through [L] (EC-013); and feature 004's push-child exception (LQ-3, draft
  PR #19, lead ruling R-28), also awaiting his word, concerns `clean`'s push
  child alone, which the overview never starts (FR-016).
- **Open changes that modify change 2, none ratified** (lane
  openRepoProject-5): this feature neither waits for them nor realizes them
  (except as question Q17 decides), as each orders itself.
  - `add-project-clean-cache-disposal` (issue #24, draft PR #27) MODIFIES
    "Overview reuses the cleanup classifier and merge target" (requirement
    5), appending to its equality clause two sentences that lane
    openRepoProject-4 agreed at `9f30fb9` (the words "for the same
    working directory and refs" agreed at `4d5855a`, unchanged at
    `fe5b245`): a worktree that `project clean` classifies
    `merged-removable` because clean's cache enumeration proved every
    ignored path a listed cache is `ignored-local-files` in the overview,
    which collects no cache evidence, and the overview never classifies a
    worktree `merged-removable` where `project clean` classifies it
    otherwise for the same working directory and refs. It also names the
    ignored file of "Every protected classifier" as not a Python bytecode
    cache, and adds the scenario "Caches that only project clean proves
    disposable". The overview's collection and code are the same either way,
    and that change's own feature excludes the cache case from this
    feature's parity tests "once feature 005 has landed ... never in feature
    005" (its proposal, Impact). Which feature takes its block if its
    realization merges first is question Q17 of `clarify-questions.md`.
  - `add-project-overview-remote-merge-status` (issue #25, draft PR #29)
    MODIFIES "Overview bounds its work and reports what it omitted",
    "Overview prints a versioned JSON envelope" and "Overview is local and
    read-only" (requirements 3, 8 and 9), keeping each whole and adding a
    paragraph that applies only under `--remote`; it ADDS "Overview reports
    remote merge evidence on request", and MODIFIES [E] on draft PR #19's
    text. Its feature is created only after this feature merges and change 2
    archives (its `tasks.md` 2.1 and 2.2). As its Open Question 3,
    addressed to lane openRepoProject-4, recommends, this feature reserves
    no flag, field or hook for it: `--remote` stays an invalid invocation
    here (FR-039, FR-042; whether this feature adds it is question Q17 of
    `clarify-questions.md`). Without `--remote` each of its blocks holds
    change 2's text as written, so no requirement here changes.
  - `add-project-clean-branch-retirement` (issue #23, draft PR #26) leaves
    `project-overview` untouched. It MODIFIES [E], [G]'s two requirements
    and other `project-clean` requirements for `clean --retire-branches`
    alone, moving no gate, refusal code or shared constant that FR-032 to
    FR-036 read; no suggestion carries its flag (FR-031).
  - An answer to Q6, Q7, Q8, Q9, Q12, Q13 or Q14 that amends change 2 or [E]
    rewrites text that these changes carry in MODIFIED blocks, among them
    #24's block of requirement 5, where an answer to Q7 amends the ladder's
    run rule (POD:378-381), and #25's blocks (Q13's options A and B rewrite
    POD:217-222, :303-306, :610-611 and :622-624, the root object's `path`,
    which #25 carries at its `spec.md:102-107`, `:206-209`, `:229-230` and
    `:241-243`; Q14's option B rewrites POD:238-243's phase condition, which
    #25 carries at `:123-128`, all at `129a4e2`); #25 re-aligns its blocks
    to such an amendment (its proposal, "Dependencies and Sequencing"; its
    `tasks.md` 2.3 and 2.4). An answer to Q16 that amends, or records a
    departure from, change 2's design D1 or clarifications N1 reaches #25 as
    well: if the amendment or the recorded departure comes before change 2
    archives, #25's task 2.3 re-read picks it up, the spawning sentence of
    #25's design D7 and its scenario "Expiry cancels queued and in-flight
    requests" included (its proposal, "Dependencies and Sequencing"; its
    `tasks.md` 2.3). Before its `/opsx:archive`, #24 re-reads its block of
    requirement 5 against the text of that requirement on `main` and
    re-copies the block from that text, keeping every amendment along with
    its own additions, so that an answer that amends requirement 5, such as
    Q7 A, is not dropped by its archive (its proposal, "Dependencies and
    Sequencing"; its `tasks.md` 3.2).
- **Features 001 to 003** (`specs/001-project-command/`,
  `specs/002-triad-first-project-new/`,
  `specs/003-parent-obstacle-wording/`): untouched; their tests join the
  suite this feature keeps passing.
- **Governance**: change 2's tasks 1.1 to 1.6, 2.1 and 2.2 are done; 3.1 is
  ticked with its `Created:` record; 3.2 (`/opsx:apply` only once the
  handoff names one feature) stays open.
- **Runtime and CI**: Git 2.36 or later; the runtime versions the README
  supports (Python 3.10 or newer) and CI runs, on Linux only since `e9d6711`
  (#32): Python 3.10 and 3.12 on `ubuntu-latest`, two `test` jobs, the
  README's Development section saying that CI covers Linux only (change 2's
  design, Context, written before it, still names Ubuntu and macOS);
  feature 004's Git 2.36 floor job (its FR-067), `git-floor` on
  `ubuntu-latest` with Python 3.10 beside every job of the `test` matrix
  (its plan, "CI shape", at `d81b3d9`, which no longer counts those jobs,
  lead ruling R-46), which the overview's tests join or not as question Q3 of
  `clarify-questions.md` decides; and the existing YAML requirement for
  manifests.

## Out of Scope

As the change defers it (proposal, "Out of Scope"; design, Non-Goals), each
extension needing its own proposal (OQ-27):

- Branch deletion, cache disposal, and paired retirement of a worktree with
  its branch; the last two are proposed as `add-project-clean-cache-disposal`
  (#24) and `add-project-clean-branch-retirement` (#23) (Dependencies).
- Remote, GitHub or pull-request queries, a `project overview --remote`, and
  the closed PR #2's remote merge-target and pull-request lookups; the
  overview's `--remote` is proposed as
  `add-project-overview-remote-merge-status` (#25), realized after this
  feature (Dependencies).
- Family traversal and relationships beyond `relationships: []`; bench,
  container and park integrations.
- Patch-equivalence retirement of squash-merged branches (LQ-2, still before
  Brett Heap), which the lead recommends as a follow-on change.
- An estate-wide destructive batch, merge or branch reconciliation, a lock
  or quiescence protocol, a persistent cache or plan, an arbitrary-depth
  scan, and the exact bench or type doctor check.
- A `project attention` alias, user-configurable limits and a per-repository
  row cap (OQ-17, OQ-8, OQ-7).
- Any change to `project clean`, `status`, `doctor`, `update`, `new` or
  `benches`, which feature 004 or no feature owns, and a doctor health
  section (OQ-22).
- Bounding a filesystem call stuck in the kernel (EC-001), and the installed
  artifact's pin in workBenches, openRepoShape and setup-openspeckit.

## Appendix: Traceability

Every requirement and scenario of change 2's spec deltas
(`specs/project-overview/spec.md` and `specs/project-review-safety/spec.md`
at `961c405`), by header, mapped to the functional requirements, user
stories and edge cases of this spec that realize it. Requirement numbers are
the proposal's (1 to 12); PRS is the MODIFIED `project-review-safety`
requirement. A story scenario is written `USn sk`. The test names come with
the tasks, in the feature's `traceability.md`, as feature 003 records them.

### Requirements

| # | Delta requirement | Source | FRs | Stories | Edge cases |
| --- | --- | --- | --- | --- | --- |
| 1 | Overview discovers projects within configured roots only | POD:10 | FR-001 to FR-005 | US1, US7 | EC-003, EC-014, EC-018, EC-025 |
| 2 | Overview groups worktrees by repository identity | POD:74 | FR-006 to FR-010 | US1, US7, US8 | EC-012, EC-018, EC-030, EC-031 |
| 3 | Overview bounds its work and reports what it omitted | POD:166 | FR-011 to FR-020 | US6, US10 | EC-001 to EC-006, EC-019, EC-023, EC-029, EC-032 |
| 4 | Overview isolates one candidate's failure | POD:317 | FR-021, FR-022 | US7 | EC-033 |
| 5 | Overview reuses the cleanup classifier and merge target | POD:358 | FR-024 to FR-026 | US3 | EC-013, EC-033 |
| 6 | Overview reports findings by attention category | POD:420 | FR-027 to FR-030 | US2 | EC-024 |
| 7 | Overview suggests only gated clean commands | POD:483 | FR-031 to FR-035 | US4, US6 | EC-007 to EC-010, EC-020 |
| 8 | Overview prints a versioned JSON envelope | POD:606 | FR-036 to FR-039 | US5, US11 | EC-016, EC-017, EC-027, EC-028 |
| 9 | Overview is local and read-only | POD:709 | FR-040, FR-016 | US10 | EC-006, EC-022 |
| 10 | Overview reports default-branch health | POD:724 | FR-041 | US9 | EC-011, EC-021, EC-026 |
| 11 | Overview exits by completeness and severity | POD:761 | FR-042 to FR-044 | US10 | EC-002, EC-015 |
| 12 | Overview renders a readable human report | POD:801 | FR-045, FR-046 | US1, US2, US4 | EC-016 |
| PRS | YAML decoding errors are structured refusals (MODIFIED) | PRSD:3 | FR-023 | US7 | none |

### Scenarios

| # | Req | Delta scenario | FRs | Story scenario | Edge cases |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Independent clones and aliases | FR-001, FR-002, FR-003, FR-006 | US1 s1 | EC-018 |
| 2 | 1 | Unreadable candidate directory | FR-005, FR-022, FR-042 | US7 s1 | none |
| 3 | 1 | Family holder count, relationships and probe ownership | FR-003, FR-004, FR-010, FR-020 | US1 s2 | none |
| 4 | 1 | Every root is absent | FR-005, FR-045 | US1 s6 | none |
| 5 | 2 | One probe set per repository | FR-006, FR-009, FR-010, FR-020 | US1 s3 | none |
| 6 | 2 | Present eligible external worktree | FR-006, FR-007, FR-031, FR-032 | US1 s4 | none |
| 7 | 2 | Missing external worktree | FR-007, FR-027, FR-029 | US1 s5 | none |
| 8 | 2 | Unreadable external worktree | FR-007, FR-022 | US7 s2 | none |
| 9 | 2 | A separate git directory | FR-008 | US8 s1 | EC-012 |
| 10 | 2 | A submodule checkout under a root | FR-008, FR-031, FR-035 | US8 s2 | EC-014 |
| 11 | 2 | A deleted main worktree | FR-009 | US8 s3 | none |
| 12 | 2 | A bare repository with a linked worktree | FR-008, FR-035 | US8 s4 | none |
| 13 | 3 | Candidate cap after sorting, with an exact count | FR-003, FR-017 | US6 s1 | EC-003 |
| 14 | 3 | Candidate cap with an incomplete listing | FR-017 | US6 s1 | none |
| 15 | 3 | Root and worktree-row caps | FR-017, FR-018, FR-019 | US6 s2 | EC-004 |
| 16 | 3 | Probe timeout | FR-011, FR-021 | US6 s4 | EC-019 |
| 17 | 3 | Hung filesystem call on an external worktree | FR-013 | US6 s5 | EC-001 |
| 18 | 3 | Invocation deadline | FR-011, FR-012 | US6 s8 | EC-001 |
| 19 | 3 | Bounded concurrency | FR-019 | US6 s9 | none |
| 20 | 3 | The JSON does not depend on concurrency | FR-019, FR-037 | US6 s10 | none |
| 21 | 3 | Bounded ignored files | FR-015 | US6 s11 | EC-019 |
| 22 | 3 | User status configuration | FR-015, FR-016 | US6 s12 | none |
| 23 | 3 | A root on a hung mount | FR-013 | US6 s6 | EC-005 |
| 24 | 3 | A repository root on a hung mount | FR-011, FR-013 | US6 s7 | EC-001 |
| 25 | 3 | A manifest over the size bound | FR-014 | US6 s13 | none |
| 26 | 4 | One helper failure is isolated | FR-021, FR-022 | US7 s3 | none |
| 27 | 4 | The YAML library is not installed | FR-022 | US7 s4 | none |
| 28 | 5 | Manifest target | FR-024 | US3 s1 | none |
| 29 | 5 | origin/HEAD target | FR-024 | US3 s2 | none |
| 30 | 5 | main target | FR-024 | US3 s3 | none |
| 31 | 5 | master target | FR-024 | US3 s3 | none |
| 32 | 5 | Conflicting targets | FR-024, FR-029 | US3 s4 | none |
| 33 | 5 | Missing target | FR-025 | US3 s5 | none |
| 34 | 5 | Every protected classifier | FR-026, FR-027, FR-032 | US3 s6 | none |
| 35 | 6 | Attention filter per category | FR-029, FR-030 | US2 s1 | none |
| 36 | 6 | A merged worktree whose upstream was deleted | FR-028, FR-032 | US2 s2 | none |
| 37 | 7 | Gated merged worktrees | FR-007, FR-032, FR-034, FR-035 | US4 s1 | none |
| 38 | 7 | Canonical identity through the handoff | FR-031 | US4 s2 | none |
| 39 | 7 | More eligible worktrees than the batch's target limit | FR-034, FR-035 | US4 s3 | EC-007 |
| 40 | 7 | The two inspect-cap bands | FR-034, FR-035 | US4 s4 | none |
| 41 | 7 | A row left unprobed closes the repository gate | FR-034, FR-035 | US6 s3 | none |
| 42 | 7 | An unstarted branch | FR-033, FR-035 | US4 s5 | EC-010 |
| 43 | 7 | A branch whose reflog cannot decide | FR-033, FR-034, FR-035 | US4 s6 | EC-008, EC-009 |
| 44 | 8 | Control and format characters in paths | FR-038, FR-045 | US11 s1 | EC-016 |
| 45 | 8 | Non-UTF-8 path | FR-032, FR-038 | US11 s2 | EC-017 |
| 46 | 8 | Non-UTF-8 common directory | FR-031, FR-035, FR-038 | US11 s3 | EC-017 |
| 47 | 8 | An argument error under --json | FR-039 | US5 s2 | none |
| 48 | 8 | Every envelope field is present | FR-036, FR-037 | US5 s1 | none |
| 49 | 8 | An internal error outside the collector under --json | FR-039 | US5 s3 | none |
| 50 | 9 | Local and read-only | FR-016, FR-040, FR-045 | US10 s1 | EC-006 |
| 51 | 10 | A default branch pushed without an upstream | FR-029, FR-041 | US9 s1 | EC-011 |
| 52 | 10 | A repository with no remote | FR-041 | US9 s2 | none |
| 53 | 10 | A dirty default branch ahead of its upstream | FR-041 | US9 s3 | none |
| 54 | 10 | A failed status probe on the default branch | FR-041 | US9 s4 | none |
| 55 | 11 | Git too old | FR-039, FR-043 | US10 s2 | none |
| 56 | 11 | Git unavailable | FR-039, FR-043 | US10 s2 | none |
| 57 | 11 | SIGTERM or SIGHUP during collection | FR-044 | US10 s3 | EC-015 |
| 58 | 11 | SIGINT during collection | FR-044 | US10 s4 | none |
| 59 | 12 | Nothing needs attention | FR-030, FR-045 | US2 s3 | none |
| 60 | 12 | A gated suggestion | FR-035, FR-045 | US4 s7 | none |
| 61 | 12 | The scanning notice | FR-046 | US1 s7 | none |
| 62 | PRS | Manifest is not valid UTF-8 text | FR-023 | US7 s6 | none |
| 63 | PRS | Overview keeps a manifest with invalid text in its row | FR-021, FR-023 | US7 s5 | none |

### Coverage

Delta requirements mapped: 13 of 13 (12 ADDED in `project-overview`, 1
MODIFIED in `project-review-safety`). Delta scenarios mapped: 63 of 63 (61
and 2), each to at least one FR and exactly one story scenario; "main
target" and "master target" share US3 s3, the two candidate-cap scenarios
share US6 s1, and "Git too old" and "Git unavailable" share US10 s2.
Functional requirements traced: FR-001 to FR-046 each realize at least one
row above; FR-047 (scope), FR-048 (README) and FR-049 (tests) trace to the
proposal's Impact and design D13, not to one scenario. Story scenarios with
no delta scenario of their own: US1 s8 (POD:18-19; C-1) and US2 s4
(POD:462-468).
