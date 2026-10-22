Lane: openRepoProject-4

# Feature Specification: Project overview

**Feature Branch**: `005-project-overview`

**Created**: 2026-10-11

**Status**: Draft. Created before feature 004 merges, on Brett Heap's word
(below); the plan and the implementation wait for feature 004's merge into
`main` and for his word given after it (Clarifications, C-56).

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
`specs/project-review-safety/spec.md`, both at `961c405`; `CMD:N` and `CLN:N`
are line N of change 1's `specs/project-command/spec.md` and
`specs/project-clean/spec.md`, at the same commit, where change 1 stands as
`0050f3e` (PR #11) landed it (Clarifications, C-37); requirement and scenario
names are the deltas' headers. Change 1, `add-project-clean-all-safe`, is cited
by requirement header under the change's labels: [E] "Repository inspection
requires Git 2.36 and shares one evidence model" (project-command); [L] "Clean
classifies preservation and cleanup actions"; [G] "Clean previews and applies a
batch of eligible worktree removals in one repository" with "Clean bounds its
Git work and reports omitted work"; [R] "Clean resolves its target Git-first";
and [P] "Clean reports every path exactly or excludes it" (all project-clean).
Feature 004's names for the same concepts (classifications, gate reasons,
refusal and row error codes, `omitted`, `schema_version`, exit statuses) are
used unchanged, with two exceptions the delta makes: `omitted` keeps 004's
`{count, exactness}` shape with the exactness enum extended to `lower-bound`
and `unknown`, `count` null under `unknown`, and is carried on `scan-limit`
errors and on the one `deadline-exceeded` scan error that counts the candidates
not started (POD:224-229, :646-648, as Clarifications C-60 amends them), and
`limits.worktree_rows` is the overview's own 512-row cap, the batch's caps
being `batch_row_cap`, `report_row_cap` and `targets` (POD:610-617). They are
cited from `specs/004-project-clean-all-safe/` (`spec.md`, `data-model.md`,
`contracts/project-clean.md`) at `d81b3d9`, where lane openRepoProject-2's doc
rounds 3 to 5 (rulings R-39 to R-51) merged them on branch
`004-project-clean-all-safe`, as `acc822e`, `5a02c1a` and `d81b3d9`, except
EC-031 and EC-033, which cite the branch's head, and EC-002 and the
Dependencies, which cite its `project` there. The head they pin, `96a08d4`,
changes the documents after `d81b3d9` by the tier tags, file and verify fields
and ticks of `tasks.md`, two additions to `plan.md` and its doc round 6
(rulings R-55 to R-57 and R-59 to R-62, with the items of R-53 and R-54 that
they settle), no document differing from `6ae927f`'s but in the ticks of
`tasks.md`; its code, which changed after `a32d20b` by its T047 (`clean` as the
frozen pipeline, merged as `6fb0fb7`), by lane G's follow-up to its evidence
model (merged as `6ae927f`) and by its US1 plan lane (merged as `2733dea`, lead
ruling R-69), has its tasks T001 to T040 and T047 to T053 built (47 of 133),
among them its five incremental parsers, four of which the overview drives
(Dependencies), its child handle and its one-wide driver, with the state, phase
and signal slot of its "Invocation" entity, and its evidence model (tasks T027
to T033), merged into that branch as `cce8dbd`; none of it is on `main`. The
change pins its code citations at `da33d92`; this spec cites no line of
`project`, `README.md` or `.github/workflows/tests.yml` as `main` has them, its
only lines of feature 004's `project` being those of EC-031, EC-033 and the
Dependencies, at `96a08d4`, and those that EC-031 and the Dependencies cite for
the re-check below, at `2cf34d3`; the plan re-pins every citation against the
`main` of its day (proposal, "Dependencies and Sequencing").

**Re-checked on 2026-10-21**: Every pin above stays. Feature 004's branch head
is now `2cf34d3`, which changes the documents after `96a08d4` by doc rounds 7
to 12 (lead rulings R-63 to R-96; merged as `3de0e69`, `48d6c08`, `3527eb2`,
`e87e57c`, `e7448a3` and `1057942`), the hand-run record `hand-runs.md` (T132)
and its traceability record, and its code by every remaining task: the US1
apply lane (`4253b52`), US2's reflog and index gates (`d6b2e23`, `83a2ac7`,
`4cab53d`), US3's named removal, row caps and push (`df8ad84`, `e81b8a3`,
`630111d`), US4's revalidation (`1b3e852`), US5's text and removal lanes
(`fdb6da1`, `359c835`), US6's bounds (`0d7d5bc`), US7's Git-first resolution
(`d075a91`), US8's paths (`b10ef9f`), US9's `status`, `doctor` and `update`
(`7f75819`), the evidence follow-up of lead ruling R-67 (c) (`a5156a5`), and
the polish, test-hygiene and final-fix lanes, with `main` at `e45155a` merged
in (`05e6218`). All 133 of its tasks are ticked, the final gates T128 to T131
at `2cf34d3`. Its five incremental parsers, its child handle and its
"Invocation" state, phase and signal slot are those of `96a08d4`; its one-wide
driver gains two parser hooks (T077, T092), and its evidence model a pure
decider for two spellings of one worktree, with each row's reads split around
it (R-67 (c)). None of it is on `main`; its feature PR, #33, is a draft. Every
line that this spec and `clarify-questions.md` cite from it is found at
`2cf34d3` by text, at new lines, each claim holding there, except where this
re-check rewrites the citing text: the twin rule, which FR-007 and EC-031 take
as a fill; the account of its evidence model and driver, its open items LQ-8
and LQ-9 and a failed ref listing's parity case (Dependencies); EC-033's
fields, four of which its documents now name; C-22's cut-reflog wording; T123's
section, now written (C-58; FR-051); and its state, above. In
`clarify-questions.md`, which stays the record, Q2's state of the head, Q4's
T123, Q14's quotation of T031's "rows 4 to 7", which now places row 4 where row
3 ran (its `tasks.md:859`; lead ruling R-75 (j)), and Q14's account of `status`
(Dependencies) read differently there. `c9103ba`, after `2cf34d3`, changes only
CI's `git-floor` build (Dependencies, Runtime and CI). The plan re-pins every
citation against the `main` that feature 004's merge produces (Clarifications,
C-56). #25's change (`add-project-overview-remote-merge-status`) stays pinned
at `05a424a`: at `11a0ba2`, its draft PR #29's head after its round C13, every
range that this spec and `clarify-questions.md` cite is byte-identical, its
overview spec's lines 1 to 410 included; at `3965dfb`, after its round C14, the
same ranges are byte-identical, three of them at new lines; and at `86324ff`,
after its round C15, and at `2eeaec4`, which commits C-51's edits of its tasks
2.3 and 2.4, they are byte-identical as at `3965dfb`, except those two tasks,
`tasks.md:22-23`, which gain C-51's second diff; and at `6b5bf8f`, after its
round C16, at `2ab3743`, after its round C17, at `e1a9f84`, after its round
C18, and at `a6080a7` and `a529310`, after its rounds C19 (`9a3f684`) and C20
and its rounds C21 (`8276945`) and C22, they are byte-identical as at
`2eeaec4`, C18, C20 and C21 editing its overview spec only in the ADDED
requirement's `gh` lookup, which the LQ-15 item cites in its C21 form, and some
sit at new lines, its design's D5 residual and D7 from `e1a9f84` (now :574-601
and :954-989) and its scenario "Expiry cancels queued and in-flight requests"
(now :645-651), except its task 2.4, `tasks.md:23`, which at `9a3f684` gains,
on lane openRepoProject-4's YES, a re-base of its block of [E] where change 1's
archived block moved past PR #19's text at `c462d87` (C-62; Dependencies).
#24's change (`add-project-clean-cache-disposal`) stays pinned at `fe5b245`: at
`e07cc42`, its draft PR #27's head after its round B9, every pinned range is
byte-identical at new lines, which the Dependencies list for a later re-pin; at
`d4e960b`, after its round B10, they are byte-identical at new lines again,
compared by `cmp`, except its task 3.2, which gains reader RF's M1; and at
`25f7333`, after its rounds B11 (`f170079`) and B12, and at `bced895`,
`69cb7a1` and `8d34525`, after its rounds B13, B14 and B15, they are
byte-identical at new lines once more, by `cmp`, its task 3.2 and its
`project-overview` block unchanged; and at `57bfc15`, after its round B16, they
are byte-identical at new lines again but for one line of its Archive order
sentence, which on lane openRepoProject-4's YES now names the blocks "written
on PR #19's text" (its B-77; Dependencies).

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

Each entry up to C-54 settles a point from the change's own text, cited; none
re-decides what the change decided. `DI:N` is line N of the packet's discovery
document at `da33d92`, as the change cites it. The questions that text leaves
genuinely open were asked in `clarify-questions.md`, and Brett Heap answered
all seventeen on 2026-10-21; his answers join this section as the session of
that date, C-55 to C-71, each entry saying where an answer amends change 2 or
change 1, or records a departure on his word, and Dependencies naming the
carrier of each.

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

Settled at the merge of `main` at `e9d6711` and the re-pin of feature 004 to
`66d60b6`. It answers no question of `clarify-questions.md`; those stay open
for Brett Heap (answered 2026-10-21, C-55 to C-71).

- **C-22** Q: What does a branch reflog read decide at its two bounds? -> A:
  Change 2's own text decides both. A read not finished within the filesystem
  budget leaves its row unprobed for the gate, recording `probe-timeout` or
  `deadline-exceeded`, and never makes it `inspection-error` (POD:521-524;
  design D5), as feature 004's data model also reads it at `d81b3d9` (its plan
  review, M5). The read asks for at most 64 KiB (POD:503-504), and a reflog
  "read to its 64 KiB bound" is `reflog-unavailable` (POD:516-517; design D5,
  "the 64 KiB bound reached", and D8, a "bound-reaching file"): a read that
  returns 65,536 bytes has reached that bound, so a reflog of 65,536 bytes or
  more is `reflog-unavailable` and one of 65,535 bytes is decided by its
  entries. Lane openRepoProject-2's ruling R-33 concurs for feature 004: its
  data model at `d81b3d9`, "Reflog anchor and movement", carries it in its text
  and in its table of outcomes, which reads `reflog-unavailable` where the read
  reached its 64 KiB bound (65,536 bytes read). Its task T059 names R-33 in
  place of plan review m10, and its T066 reads the bound as R-33 does. Its
  EC-005 now reads the same: "A reflog of 64 KiB (65,536 bytes) or more, about
  300 entries, is `reflog-unavailable`" (R-33). At the branch's head `2cf34d3`
  that data model words the cut read's outcome `reflog-unavailable`, the row
  left unprobed (its marker set, its class kept, `probe-timeout` or
  `deadline-exceeded` in its errors, the plan `inspection-incomplete`; its
  "Reflog anchor and movement", :237-261 there; lead rulings R-67 (a) and R-73
  (c)), still never `inspection-error`, so the claim is unchanged. PR #19's
  round (h) at `b3228bb` amends the ratified sentence for [G]'s own gate
  (`0050f3e` pcl:606-608), so that a read that the deadline cuts ends its plan
  `deadline-exceeded`, not `inspection-incomplete` (O-1, its
  `specs/project-clean/spec.md:713-718`); the overview's outcome follows
  amendment A1, held for Brett Heap (FR-034). Where applied: FR-033; FR-049;
  EC-009.

### Session 2026-10-19

Settled from the change's text, and change 1's shared evidence model, while
applying three read-only reviews of `3d28710`. It answers no question of
`clarify-questions.md`; the points those reviews found the change leaves open
are added there as Q6 to Q13, for Brett Heap, unanswered then (answered
2026-10-21, C-55 to C-71).

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
  (DI:778). A working directory whose realpath cannot be established leaves
  every `current` null, as C-61 records. Where applied: FR-013; FR-026.
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
  DI:165-169's exactness"). Its `limit` is `"invocation_timeout_seconds"`, and
  no other `deadline-exceeded` error carries either field (C-60). Where
  applied: FR-012.
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
added there as Q14 and Q15, for Brett Heap, unanswered then (answered
2026-10-21, C-55 to C-71).

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
  listed. Such a repository stays a `probe-failed` error row (C-68). Where
  applied: EC-030.

### Session 2026-10-21, Brett Heap's answers

Brett Heap answered every question of `clarify-questions.md` in lane
openRepoProject-4's session at about 2026-10-21T10:31Z, in his words "yes,
recommended for Q1-Q17", recorded by that lane as a RULED line at 10:33:09Z:
Q1 A, Q2 A, Q3 B, Q4 D, Q5 A, Q6 A, Q7 A, Q8 D, Q9 B, Q10 A, Q11 A, Q12 A,
Q13 A, Q14 A, Q15 A, Q16 B and Q17 A, each the recommended option. Each entry
encodes its option as `clarify-questions.md` words it, with the reasons and
costs its Context and Recommended paragraph give. Where an answer amends change
2 or change 1, or records a departure on his word, the entry says so, and
Dependencies names the carrier: for change 2, amendment A1,
`amend-project-overview-clarify-answers`, lane openRepoProject-4's governed
change, proposed after this fold as draft PR #34 and ratified by Brett Heap on
2026-10-22, at about 12:04Z in lane openRepoProject-4's session, in his words
"ratify 34", recorded by that lane as a RULED line at 12:06:26Z,
https://github.com/opensoft/brett-wip/blob/13257af5b39798741fd762ca770c180cef2dae28/lanes/log/openRepoProject-4.md#L184,
PR #34 landing after PR #19's ratification of the commits that A1's four LQ
items follow, under A1's ordering rule, or sooner without those items on his
word (Dependencies); for change 1, lane openRepoProject-2's draft PR #19, which
that lane agreed on 2026-10-21 to carry it in.

- **C-55** Q: How does feature 005 treat the one-project check of a Triad
  assembly? -> A: Q1 A: As ratified. A `--root` naming a Triad assembly
  examines it itself (C-1), its submodule legs at `spec/` and `code/` are
  immediate entries, and each leg row carries the `unsupported-layout` repair
  finding of severity error that change 2 gives every submodule checkout
  (POD:97-102; design D3, item 1), so the run exits 1; the README says so for
  Triad assemblies. Change 2 is not amended: this builds the ratified rule that
  unknown is never healthy and that the overview never suggests what `project
  clean` refuses, and a later change can relax it once real runs show the need.
  Where applied: EC-014; FR-048.
- **C-56** Q: Which state of feature 004 must exist before the plan starts? ->
  A: Q2 A: Feature 004 merged into `main`; the plan starts on Brett Heap's word
  given after that merge, and pins against that `main`. It is the order the
  change already sets (proposal, Status; change `tasks.md` 3.1), and planning
  against an unmerged branch would risk a second plan, the runner's interface,
  the shared constants and the citations being what feature 004's review may
  still change. Where applied: header, Status; Assumptions; Dependencies.
- **C-57** Q: Should the overview's tests also run in the Git 2.36 floor job?
  -> A: Q3 B: A small set: the version check accepting Git 2.36, and one
  end-to-end run over a fixture with linked worktrees, merge targets and a
  gated suggestion, selected in feature 004's `git-floor` job by one more `-k`
  prefix. Change 2's Impact lists `project`, the README and the tests, and no
  CI change (proposal, Impact); the answer records this "as a departure from
  change 2's Impact on Brett Heap's word (or carried in the change-2
  amendment's Impact)", and amendment A1 takes the second branch: its Impact
  gains a `.github/workflows/tests.yml` bullet after the tests bullet
  (proposal.md:441-449; its `proposal.md:456-461` at `e4a30fc`), ratified by
  Brett Heap in PR #34 (Dependencies). It proves FR-043's claim at 2.36 on the
  probes the overview drives for little CI time, the shared probes being proven
  there already by feature 004's tests. Where applied: FR-050; Dependencies;
  Appendix, Coverage.
- **C-58** Q: Should agents be told in `AGENTS.md` that an overview suggestion
  is advice to review, and that applying it needs the person's word? -> A:
  Q4 D: Yes, after feature 004 lands, in one sentence on the overview added to
  the `AGENTS.md` section that feature 004's task T123 adds, "Cleaning up
  worktrees for a person" (written at feature 004's head `2cf34d3`,
  `AGENTS.md:53-70` there, not yet on `main`), recorded as a departure from
  change 2's Impact, which names no `AGENTS.md` change, on Brett Heap's word,
  as feature 004 records its own (its lead ruling R-32). That section forbids
  answering the removal question, or passing `--yes`, on a person's behalf (its
  `AGENTS.md:64-66` there), so the agent guidance stays in one place; the
  sentence follows the section's title and wording if either changes at feature
  004's merge. If Brett Heap declines feature 004's T123 departure, the
  question's option C applies instead: a separate small OpenSpec change, after
  feature 005, carries agent guidance on the overview and the batch apply.
  Where applied: FR-051; Dependencies.
- **C-59** Q: Should the overview surface feature 004's partial-removal note?
  -> A: Q5 A: No, as ratified. Change 2's worktree row is a closed field list
  for schema 1 with no `notes` (POD:632-638), so a worktree that a removal
  killed midway is a plain `dirty` finding, whose read-only suggestion leads to
  `project clean <root>`, which shows the note (feature 004 FR-009; change 1's
  design D4). The case is rare, and an additive `notes` field stays open for a
  later change within schema 1 (POD:655-658). Change 2 is not amended. Where
  applied: FR-036.
- **C-60** Q: What do `limit` and `omitted` hold on `deadline-exceeded` errors?
  -> A: Q6 A: Amend change 2: only the `deadline-exceeded` scan error that
  counts the candidates not started (POD:180-181) carries them, `limit` being
  `"invocation_timeout_seconds"`, the `budget` key, and `omitted` the
  candidates not started, with C-30's exactness; every other
  `deadline-exceeded` error, row or scan, carries neither; and a row-level
  `scan-limit` error, on which POD:646-648 adds the same two fields, carries
  `limit: "worktree_rows"` and `omitted` counting that repository's rows past
  the cap, exactness `exact`. This departs from POD:646-648, which adds both
  fields on every `deadline-exceeded` error, and, for the one deadline error,
  from the packet's definition of `limit` as "a key of `limits`" (DI:824-825);
  amendment A1 carries it. Where applied: header, Citations; C-30; FR-012;
  FR-018; FR-036; Key Entities, Row error and scan error; US6 s2 and s8;
  Dependencies.
- **C-61** Q: What happens when the working directory's realpath cannot be
  established? -> A: Q7 A: Amend change 2: one scan error records it,
  `os-error` or `probe-timeout`, with feature 004's fixed text for that code
  and OPERATION `realpath` (its contract, lead ruling R-45), its `path` the
  `PWD` environment value when that is set and absolute, else omitted, and
  first among the scan errors; every `current` is null; and each row the ladder
  would classify `merged-removable` or `merged-current` is `inspection-error`
  instead, so `inspection-incomplete`, a gate the table already has, withholds
  `--all-safe` for its repository, in line with [L]'s rule for evidence that
  could not be established. That `path` is taken raw, absolute as the
  environment gives it and unresolved, a further exception to DI:842-843's rule
  that paths are canonical, which already excepts `ignored_samples` and an
  absent default root: four exceptions with C-67's. The null `current` of every
  worktree row, a present one included, also departs from the packet's DI:778,
  by which `current` is null only where `present` is null (lane
  openRepoProject-3's W7 read of A1, M2). Amendment A1 carries it in
  requirement 5, a new paragraph after its equality clause (after POD:386),
  leaving POD:378-386 as ratified, and in design D6's scan-error order
  (design.md:410-412) and D8's realpath task (design.md:470-471), its own map
  at `e4a30fc`, which records the DI:778 departure as well (its
  `proposal.md:1146-1157`; Dependencies). Where applied: C-25; FR-013; FR-026;
  FR-037; FR-038; Dependencies.
- **C-62** Q: How are strings that are not paths decoded and printed? -> A:
  Q8 D: Amend change 2 so that every row and scan error's message is a fixed
  text for its code, naming no path, the path going in `path`: feature 004's
  for `os-error`, `probe-failed` and `probe-timeout` (its contract, lead ruling
  R-45); `OPERATION stopped at the invocation deadline` for
  `deadline-exceeded`, the overview's own term, where feature 004's contract
  reads `OPERATION stopped at the work deadline`
  (`contracts/project-clean.md:303` at `b0243e5`, re-checked at feature 004's
  `e256b59`, where it is :433 and the three texts above are :430-432); and
  texts amendment A1 fixes for `manifest-invalid` (naming the cause, the size
  bound or the missing library, never the reader's own text), `refused`,
  `undecodable-output`, `internal-error` (the exception's class only),
  `scan-limit` and `root-unreadable`. A1 edits POD:337-338 to "with a message
  of at most 200 characters, the fixed text of its code, which names no path";
  design D1 (design.md:99-101) so that a child's standard error is "drained and
  capped as [E] requires (CMD:175-177), and never shown"; and clarifications N1
  (clarifications.md:35-36 and :46-47), whose "first 200 characters kept" goes
  the same way. Those three texts follow the packet's DI:544-545 ("for a failed
  probe, the first line of Git's standard error"), from which A1 departs. No
  text from Git's standard error then reaches a message or the `Incomplete:`
  line, and names, branch names, admin ids and every other string the report
  takes from the filesystem, a manifest or Git follow [P]'s path rule: decoded
  as a path is, each undecodable byte written `\xHH`, each Cc, Cf, Zl or Zp
  code point escaped by JSON and written `\uXXXX` in human output, with no new
  field. Git's own reason is then not shown: the person re-runs the Git command
  to see it. A1 at `e4a30fc` writes those texts as a table after POD:347, with
  OPERATION `git SUBCOMMAND` for a Git child, the filesystem call (`lstat`,
  `stat`, `realpath`, `scandir` or `read`) for a filesystem task, and
  `collection` for a candidate whose collection never started and for the scan
  error that counts such candidates, its own texts and the values `stat`,
  `scandir` and `collection` being its drafted fill, ratified by Brett Heap
  with A1 (its `specs/project-overview/spec.md:385-403`; FR-022), and records
  the `e256b59` re-check above (its `proposal.md:1158-1185`). Where applied:
  FR-022; FR-038; EC-033; EC-034; Key Entities, Row error and scan error;
  Dependencies.
- **C-63** Q: How does the feature treat the residuals beyond what the pins and
  the scrub prove? -> A: Q9 B: Filters and the configuration files are accepted
  as recorded residuals beside EC-006 (EC-022), and change 2's read-only
  wording (POD:710-717) is amended to claim only what the pins and the scrub
  prove; amendment A1 carries it. Change 1 is amended to set `GIT_TRACE2`,
  `GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF` to `0` on every Git child, which
  overrides `trace2.*` targets in the system and global configuration, and to
  add `GIT_TRACE` and the `GIT_TRACE_*` names Git 2.36 to 2.43 reads, each
  listed by name, to [E]'s scrub (CMD:98-122), which `clean`, `status` and
  `doctor` then share. The answer proposes that this change-1 amendment ride in
  lane openRepoProject-2's draft PR #19, which already edits [E]'s Environment
  paragraph and held no trace pin at `c462d87`, and that, if feature 004 merges
  first, it builds the narrower scrub and the wider one follows as a change-1
  amendment. Lane openRepoProject-2 agreed on 2026-10-21 that PR #19 carries
  the trace pins and the trace-variable scrub names as a commit of its own, and
  that feature 004's draft (#33) builds the wider scrub and the pins; this spec
  therefore cites [E]'s list as PR #19 amends it, which PR #19 does at
  `423a532`: thirty-one names, with `GIT_TRACE2`, `GIT_TRACE2_EVENT` and
  `GIT_TRACE2_PERF` set to `0` on every Git child (its
  `specs/project-command/spec.md:98-124`). Change 2's "seventeen names"
  (POD:212-213) becomes a citation of [E]'s list, in A1, and this spec's count
  of seventeen, C-5's included, reads as that list. The amended wording narrows
  the packet's DI:307-308, "it never fetches, pulls, resets, bootstraps, runs
  validators, writes files, or contacts the network", for the overview's Git
  children to what the pins and the scrub prove, the filters and the
  configuration files being outside that claim (A1's
  `specs/project-overview/spec.md:809-815` at `e4a30fc`, whose Q9 B entry
  records the narrowing, its `proposal.md:1186-1202`; lane openRepoProject-3's
  W7 read of A1, M3). Trace output is a pure side effect, cheap to pin and
  scrub for every subcommand at once, while filters and the configuration files
  cannot be switched off in general. Where applied: US10; FR-016; FR-040;
  FR-049; SC-002; EC-022; Dependencies.
- **C-64** Q: Should the overview report the two layouts the marker table
  leaves unreported? -> A: Q10 A: No. Feature 005 builds the ratified marker
  table (POD:24-31) and keeps both layouts as recorded edge cases: both are
  rare, the table mirrors "the order in which `discover` and `manifest` look"
  (DI:126-128), so changing it touches how families are found, and a later
  change can widen it once a real case appears. Change 2 is not amended. Where
  applied: EC-025.
- **C-65** Q: What does the overview do when a candidate's identity probe
  reports a toplevel other than the candidate itself? -> A: Q11 A: Amend change
  2: a candidate other than a family holder whose identity probe reports a
  toplevel that is a proper ancestor of the candidate is an error row
  (`refused`, its `path` the candidate's `.git`, its message a fixed text
  saying that Git did not accept it and reported an enclosing repository), and
  creates or joins no repository row; a family holder whose probe reports
  another toplevel keeps null `repository`, `merge_target`, `git` and
  `worktrees` and no error, as DI:284-287 and FR-003 have it; and a toplevel
  elsewhere that Git reports for a layout it accepts, such as a `core.worktree`
  naming another directory, is unaffected. Discovery so stays within the roots
  (POD:10), and the broken checkout shows as an error on its own row, with a
  code the collector table already has; amendment A1 carries it. Where applied:
  FR-003; FR-006; Dependencies.
- **C-66** Q: How are a failed write to standard output and the output encoding
  handled? -> A: Q12 A: Amend change 2: the whole document or report is
  rendered before its first byte is written, as UTF-8 whatever the locale, the
  JSON document with ASCII escapes as feature 004 writes its own (its lead
  ruling R-38), every interpolated string already escaped by [P]'s rule; a
  failed write to standard output ends the run with exit 2, no traceback and no
  retry; nothing more goes to standard output, and one line goes to standard
  error on a best-effort basis; this is, besides an argument error, the one
  exit 2 under `--json` that prints no error object, carved out of POD:675-679
  and the packet's DI:1086-1089, and with no error object there is no code to
  print, so R-55's `internal-error` is not kept; every child is already reaped
  or abandoned. A recorded signal decides the status, also over the exit 2 of a
  failed write. This matches lane openRepoProject-2's ruling R-55 for feature
  004's phase before apply: the failed stream gets nothing more, the error is
  recorded on the run, and a recorded signal outranks it. Every other exception
  outside the collector ends as FR-039 maps it. Amendment A1 carries it. Where
  applied: FR-036; FR-039; SC-009; Dependencies.
- **C-67** Q: How is a root whose canonicalisation is cut reported? -> A:
  Q13 A: Amend change 2: its `path` is the given path made absolute (expanded,
  and joined to the working directory when relative) but not resolved:
  absolute, as DI:842-843 has every path, and a further exception to its rule
  that paths are canonical, four exceptions with C-61's; it sorts by those
  bytes among the canonical paths, is never deduplicated, and counts toward the
  32-root cap, a root past the cap being `omitted` whether or not its
  canonicalisation was cut. It uses the only path the overview holds, keeps the
  order total and stable, and errs toward reporting a root twice rather than
  hiding one. It departs from POD:14-16, :217-222, :303-306, :610-611 and
  :622-624; amendment A1 carries it. Where applied: FR-001; FR-013; FR-038; Key
  Entities, Root; US6 s6; Dependencies.
- **C-68** Q: How is a bare repository reported? -> A: Q14 A: Its first
  registry record, the bare record, is the main worktree row, as design D3
  keeps an unnamed gitfile record: its path the common directory, `present`
  from `lstat`, no status probe, null status fields and classification, no
  finding of its own, and counted toward the caps and the row count, as
  POD:217-218 counts main worktree rows and C-46 every registry entry. It adds
  no status probe to `probes.estimated`, and its null classification is not one
  the overview's cap or deadline left. The `.bare` layout stays a
  `probe-failed` error row, recorded as EC-030. This follows design D3, as for
  the unnamed gitfile record, and needs no amendment; feature 004's model never
  makes the common directory a worktree row, and its `clean` refuses a bare
  repository. Where applied: C-54; FR-008; FR-020; FR-034; EC-030; US8 s4.
- **C-69** Q: What does a signal that arrives while the result is being written
  do? -> A: Q15 A: It stops the write. Change 2's "print no result document"
  (POD:778-779, and the packet's rule too, DI:1094-1096) is amended to "start
  no result document once the signal is read, and stop one that is being
  written", and the partial result is recorded as a residual beside EC-015: the
  write stops at the signal, `Cancelled.` follows on standard error, and the
  run exits with the signal's status; standard output may then hold part of a
  result, which an exit of 129, 130 or 143 marks as no result. A signal
  recorded before the run exits decides its status, also over the exit 2 of a
  write that fails after it. The raising span around the write is entered
  before the first byte is written, so a signal recorded while rendering prints
  nothing, and output not yet written is discarded, never flushed at exit.
  Ctrl-C stays answered even when a reader stalls, and consumers keep one rule,
  that an exit of 129, 130 or 143 carries no result; the span is feature 004's
  mechanism (its lead ruling R-47), and the overview's result records nothing a
  re-run cannot read again. Amendment A1 carries it. Where applied: US10;
  FR-044; SC-011; EC-035; Dependencies.
- **C-70** Q: How does feature 005 start its Git children? -> A: Q16 B: With
  SIGINT, SIGTERM and SIGHUP unblocked, under handlers that only record the
  signal. Amendment A1, the same amendment that carries the other answers,
  changes design D1's spawning paragraph (design.md:115-119) and the spawn line
  of clarifications N1 (clarifications.md:45-47) so that each child starts with
  those three signals unblocked, and strikes N1's "or raise a `BaseException`
  subclass" (clarifications.md:42-44), so that the handlers only record the
  signal, as D1's signals paragraph already has them (design.md:103-107), which
  keeps a termination pass from missing a child. A child started with them
  blocked survives SIGTERM to its group and needs SIGKILL at every stop
  (runtime cross-check X-7); the ratified design then stays true rather than
  carrying a standing departure. Read with C-69's raising span, the handlers
  only record the signal while a child can run, and raise only during the span,
  which is entered only after every child is reaped or abandoned, as A1
  reconciles the two (its design D1, design.md:116-127, its clarifications N1,
  clarifications.md:42-45, and its `proposal.md:1454-1457`, at `e4a30fc`;
  FR-044). Where applied: FR-011; FR-044; Dependencies.
- **C-71** Q: Does feature 005 realize the overview parts of #24 and #25? -> A:
  Q17 A: No, in every order: both stay in their own features, as #25 sets (its
  `tasks.md:20-21` at `05a424a`) and as #24 states for its overview part,
  "never in feature 005" (its `proposal.md:569-572` at `fe5b245`). Feature 005
  builds change 2 as ratified and as the other answers amend it, reserves no
  flag, field or hook for `--remote`, and gives every fixture it compares with
  `project clean` that has an ignored file one such as `local.env`, which no
  cache rule #24 proposes admits. If #24's realization merges first, a
  cache-only worktree is `ignored-local-files` in the overview and
  `merged-removable` in `project clean`: a departure, on Brett Heap's word,
  from change 2's equality clause (POD:381-386, on DI:620-624), which #24's own
  design calls "against change 2's equality clause" (its `design.md:658-661` at
  `fe5b245`), until #24's overview block is archived, after which that block
  records the same divergence as a lasting exception. In the other order the
  same divergence arrives with #24's code as #24's own change, its D14
  excluding the cache case from feature 005's parity tests once feature 005 has
  landed; so the divergence reaches `main` in every order, and only this
  feature's own departure belongs to the #24-first order. It is the cautious
  direction, and no feature 005 test depends on it. Where applied: FR-026;
  FR-049; SC-003; Dependencies; Out of Scope.

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
3. **Given** a repository that does not set `extensions.worktreeConfig`, with a
   main worktree and three linked worktrees, one an immediate entry of the root
   and one outside every root, **When** the overview runs, **Then** there is
   one project row with four worktree rows, main worktree first and then by
   path bytes, the external worktree adds no project, the identity probe, the
   registry, the ref listing, the merged-set query and the
   `extensions.worktreeConfig` read run once for the repository, each present
   row gets one status probe, and `probes.performed` is one version check, plus
   one identity probe per Git candidate, plus four, plus four, as amendment A1
   at `e4a30fc` words the scenario (its
   `specs/project-overview/spec.md:151-155`), ratified (FR-020; Dependencies);
   when the main worktree lies outside every root, so that a linked worktree
   reaches the repository first, `repository.root` is the canonical path of the
   first registry record, never that linked worktree's toplevel.
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
   the other 8 keep registry and branch evidence with `dirty`, `ignored_files`
   and `classification` null, their project rows carry `scan-limit` errors,
   each with `limit: "worktree_rows"` and an exact count of that repository's
   rows past the cap (C-60), the scan error has `limit: "worktree_rows"` and
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
   5 s with a `probe-timeout` scan error and counts as `truncated`, no entry of
   it is read after the cut, every other root's candidates are collected, and
   the exit status is 1; when the cut falls in its canonicalisation, its root
   object's `path` is the given path made absolute but not resolved, sorted by
   those bytes among the canonical paths (C-67).
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
   error's omitted count is exact and its `limit` is
   `"invocation_timeout_seconds"`, no row's `deadline-exceeded` error carries
   `limit` or `omitted` (C-60), and the process exits 1 within 64 s plus
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
13. **Given** a candidate's `project.yaml` larger than the manifest size bound,
    **When** the overview runs, **Then** its row carries a `manifest-invalid`
    error whose `path` is the manifest and whose message names the size bound,
    the file is neither read nor parsed, the other rows are complete, and the
    exit status is 1.

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
   `locked` at mode 000, and a second `--root` that cannot be listed, **When**
   the overview runs, **Then** `locked` appears in its sorted position with
   `path` the candidate path, `name` `locked`, `kind` null, status `error`,
   `findings` empty, one `os-error` whose `path` is that candidate path and
   every Git-derived field null, `alpha` and `zeta` are complete, the second
   root adds a `root-unreadable` scan error, and the exit status is 1, never 2.
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
5. **Given** `ledger/project.yaml` contains invalid UTF-8 bytes beside `alpha`
   and `zeta`, **When** `project overview --json` runs, **Then** `ledger`'s row
   has status `error` and one `manifest-invalid` error whose `path` is that
   manifest, with no traceback, `alpha` and `zeta` are complete, the JSON
   document is printed, and the exit status is 1, not 2.
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
   directory; its main worktree row is the bare record, at the common
   directory, with `present` from `lstat`, no status probe, null status fields
   and classification, and no finding of its own (C-68).

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
carries pins that make a lazy fetch fail locally, and none of the variables
[E]'s scrub removes reaches it (EC-006 and EC-022 record what the pins and the
scrub do not cover, and the read-only claim stops at what they prove;
Clarifications, C-63). It refuses an old or missing Git before listing
anything; and when the person presses Ctrl-C, or the terminal or a supervisor
ends it, no Git child outlives it, no result document is started, and one being
written is stopped (C-69).

**Why this priority**: Read-only is a rule the change keeps (proposal,
"Rules This Change Keeps"), and a scan across an estate must be safe to
interrupt. The read-only snapshots and the network block run under every
story's fixtures from P1 on (FR-040); this story adds the dedicated
whole-suite check, the version refusal and the signals, which matter less to
the daily answer than the earlier stories.

**Independent Test**: Run over every fixture with networking disabled and
before-and-after snapshots, the counting `git` wrapper asserting that every Git
child's argument vector carries the seven protocol pins and that none of the
names [E]'s scrub removes, `GIT_ALLOW_PROTOCOL` included, reaches any child,
and that each child has `GIT_TRACE2`, `GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF`
set to `0` (R-23, R-25; C-63; the overview has no push child, so feature 004's
push-child exception, R-28, never applies); run with Git 2.34.1 first on PATH
and with no `git` on PATH; and send SIGINT, SIGTERM and SIGHUP during
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
5. **Given** `HOME` set to the relative `h`, or `XDG_CONFIG_HOME` to the
   relative `cfg` beside an absolute `HOME`, **When** the overview runs,
   **Then** it exits 2 with code `relative-config-path` and a message naming
   that variable, never its value, before listing any root or starting any Git
   child, `git --version` included, and under `--json` it prints only
   `{"error": "<message>", "code": "relative-config-path"}`; the same holds for
   a relative `HOME` beside an absolute `XDG_CONFIG_HOME` and an absolute
   `GIT_CONFIG_GLOBAL`, although Git would then read no configuration file
   under `HOME`, since the test does not follow Git's order of precedence
   (FR-043; LQ-15, pending #19's ratification; A1's
   `specs/project-overview/spec.md:908-912` at `e4a30fc`, ratified).

**Delta scenarios**: "Local and read-only"; "Git too old"; "Git unavailable";
"A relative configuration path" (A1's, FR-043); "SIGTERM or SIGHUP during
collection"; "SIGINT during collection".

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
- **EC-007**: `target-cap` counts gate-passing rows the batch's index gates,
  and the two gates that FR-032 adds after them once PR #19 is ratified, may
  still exclude, so the overview's count can exceed what the batch selects; the
  suggestion is advice either way (design D5, Risks).
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
  (POD:97-102; design D3, item 1). Feature 005 builds it so, and the README
  says so for Triad assemblies (FR-048; Clarifications, C-55).
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
- **EC-020**: A reflog read that does not finish leaves its row unprobed, which
  withholds `--all-safe` for the whole repository with `inspection-incomplete`
  (POD:521-529; R-16). Since PR #19's round (h) (O-1), [G] ends its plan
  `deadline-exceeded` where the deadline cut the read; the overview's code here
  follows amendment A1, held for Brett Heap (FR-034).
- **EC-021**: Ignored files in the merge-target checkout raise no finding,
  since a `.venv` would otherwise warn on most projects (proposal, OQ-20).
- **EC-022**: The pins and the scrub do not cover everything Git does with the
  caller's setup. Git still reads the user's and the system's configuration and
  the variables outside [E]'s scrub (`GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`,
  `GIT_CONFIG_NOSYSTEM`, `HOME`, `XDG_CONFIG_HOME` and
  `GIT_CEILING_DIRECTORIES` among them); it honours trace targets (`GIT_TRACE`,
  `GIT_TRACE2_EVENT`, `trace2.*` settings), which append to files; and the
  status probe runs the clean and process filters a repository's attributes
  name when it re-hashes a tracked file, a program that can write files or open
  connections outside the pins (CMD:98-122). Filters and the configuration
  files are accepted as recorded residuals beside EC-006, and FR-040 claims
  only what the pins and the scrub prove; the trace targets are closed by the
  trace pins and names that PR #19 adds to [E]'s list at `423a532` (FR-016;
  Clarifications, C-63). LQ-10's two new status pins widen the filter residual:
  where a repository defines a clean filter, a ctime-only change under
  `core.trustctime=false` now runs that filter once per status probe, where it
  ran none before, and a filter whose command is missing gives a false `dirty`
  or a failed probe, both failing closed, as #19's design Risks accepts on
  Brett Heap's ruling LQ-10 (its `design.md:1420-1425` at `1ebdd90`, pending)
  and as amendment A1 at `e4a30fc` records beside requirement 9's sentence
  after POD:717 (its `proposal.md:1443-1452`), ratified; that widens the filter
  residual that lane openRepoProject-2's LQ-16, its question to Brett Heap on
  neutralizing configured clean and process filters in the read-only probes,
  leaves open with him (lane openRepoProject-3's W25 L10). A relative `HOME` or
  `XDG_CONFIG_HOME` is EC-036's case. Q9 B does not extend to `gh` children,
  which the overview never starts (FR-039): #25 (draft PR #29) would start them
  under `--remote` with the caller's environment less `GH_DEBUG` and five other
  names, every variable a child gets passing unchanged and [E]'s Git scrub not
  applying, so that the `GIT_TRACE*` names reach `gh` unread (its design D5,
  `design.md:467-482` at `11a0ba2`). Lane openRepoProject-5's round C14 records
  this in D5 as a residual, in lane openRepoProject-4's words, pending #29's
  ratification (`design.md:530-557` at `79d196a`): `gh` 2.96.0, run offline
  with D5's flags, switches and query, exited 1 on the refused connection,
  started no `git`, created no trace file and wrote no file, and the path of a
  200 answer is not verified. Re-checked at `86324ff`, #29's head after its
  round C15, at `2eeaec4`, at `6b5bf8f`, its head after round C16, at
  `2ab3743`, its head after round C17, at `e1a9f84`, its head after round C18,
  at `a6080a7`, its head after round C20, and at `a529310`, its head after
  round C22: the residual reads the same, at `design.md:565-592` up to
  `2ab3743` and at :574-601 from `e1a9f84`, apart from D5 now locating Q9 B at
  PR #19's `423a532` (C-50).
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
  which exists as neither a file nor a directory. Feature 005 builds the
  ratified table and keeps both layouts as recorded edge cases (Clarifications,
  C-64).
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
  repository's worktrees are not listed (Clarifications, C-54); it stays so. A
  bare repository's own first registry record is its main worktree row, with no
  status probe (FR-008). Feature 004's model never makes the common directory a
  worktree row, and its `clean` refuses a bare repository (Clarifications,
  C-68).
- **EC-031**: Two registry entries naming one path fail closed: the registry
  listing does not name the administrative directory, so the two-way
  registration check alone cannot tell the two entries apart, and each is a
  registration disagreement, whose outcome in either direction is no status
  probe, `inspection-error` set directly, a `registration-mismatch` finding in
  place of that class's `inspection-error` finding, and no error (FR-007;
  DI:259, :267-272). The packet names no case of two entries for one path.
  Feature 004, for the evidence model the overview shares, refuses them too,
  and gives three parts of that outcome: no status probe, `inspection-error`
  and `registration-mismatch` (its data model, "Worktree identity and
  registration" at `96a08d4`; lead ruling R-57, withdrawing R-51(c)'s known
  limit, and R-59 D5, which compares the registry records' raw path bytes). Its
  code builds the refusal at that head (`7880023`, as `7d70b02` later split it,
  the lines being those of `96a08d4`): `shared_paths` (`project:2634-2641`)
  names the raw paths that more than one entry lists, `worktree_rows`
  (:2762-2816) tells `_read_row` (:2725-2759) whether a row's path is one of
  them, and that reader looks at presence first, so a row not present goes no
  further and stays `stale-worktree` with no duplicate check (R-57 L2, R-59
  D5), while any present row on such a path gets `registered` false with no
  registration read. The finding in place of the class's `inspection-error`
  finding and the absence of an error are the packet's rule (DI:267-272), not
  stated by feature 004. The rows keep the registry's order, so the output
  stays deterministic. At the branch's head `2cf34d3` (re-checked 2026-10-21),
  feature 004's lead ruling R-67 (c) extends the rule to present rows spelled
  differently that share a realpath, or an admin id: both spellings of one
  worktree pass the two-way check, with one admin id, since both read one
  `.git` file, [E]'s comparisons being made between realpaths (CMD:139-144),
  and each is `registration-mismatch` too, so `inspection-error` with no status
  probe (its data model, "Worktree identity and registration", :91-145 there;
  built by its evidence follow-up 2, merged as `a5156a5`, lead ruling R-81
  (a)). Its code decides it in `shared_identities` (`project:2766-2783` there),
  a pure decider over the reads of the rows that one `worktree_rows` call
  builds (:2911-2982): every row is read first, by `_read_row` (:2867-2895),
  the twins are found among those reads, and only then is each row probed, by
  `_read_status` (:2898-2908); `shared_paths` is unchanged, at :2756-2763. A
  row not present, or whose realpath was not read, is compared by neither, and
  only a registration that held gives an admin id to compare. Change 2 names no
  case of two spellings of one registered worktree, and FR-007 as change 2
  words it would probe and classify both, so FR-026's equality with `project
  clean` needs the same outcome: the overview takes R-67 (c) as a fill of
  change 2's rule, not a departure, as EC-033 takes R-61(b), with the finding
  and the absence of an error of two entries on one path, deciding the twins
  from all of a repository's row reads before any of its status probes (FR-007,
  FR-019). Lane openRepoProject-2's ruling R-101 keeps that pass, which lane
  openRepoProject-3 found to depart from CMD:124-126's identity "verified
  immediately before" the probe, and adds that each row's own identity is
  verified again immediately before that row's probe, a changed identity making
  the row `inspection-error` and leaving it unprobed; it is queued as a code
  fix in feature 004, not built at `2cf34d3`, and the overview takes it with
  the fill, deciding within change 2's closed lists what R-101 leaves open: the
  class's `inspection-error` finding, no row error where a re-read value
  differs, a re-read failing with `ENOENT` or `ENOTDIR` counting as one, and
  the fitting code of change 2's table where the re-read itself fails (FR-007).
  When feature 004's fix is built, the plan re-reads that outcome against it
  (R-101 (e) and (j); Dependencies). The overview inherits feature 004's
  decider only where its rows are built by it (Dependencies, R-54); where they
  are not, the same fill applies. As in feature 004 (its lead ruling R-95 (d)),
  a twin past the row cap is not compared, and the row the cap left withholds
  `--all-safe` for its repository (FR-034).
- **EC-032**: When a value of the identity probe holds a line feed, as the name
  of a repository directory can (US11 s1), the probe is repeated, one child per
  option, each counted (change 1's design D6, row 3), so that for such a path
  `probes.performed` exceeds `probes.estimated`, which counts 1 identity probe
  per Git candidate (FR-020; POD:248-254). No scenario asserts the two equal
  there, and FR-020's identity-probe count stands as ratified. PR #19's round
  (h) at `b3228bb` has `project clean`'s `probes.estimated` count those extra
  children (RI-3, its `specs/project-clean/spec.md:1050-1056`); A1's
  re-alignment of the overview's count is held for Brett Heap with #19's
  ratification (FR-020). PR #19's round (i) at `e0c91bb` has D6 repeat the
  probe on any count of lines but two, since a submodule checkout's probe
  prints three lines as a line feed in a path can (its `design.md:353-364`;
  lane openRepoProject-4's finding), so that, read as D6 now reads it, a
  submodule candidate's probe is repeated too and `probes.performed` exceeds
  `probes.estimated` for it; this spec's count follows A1, A1's re-alignment of
  it held with the line-feed case (FR-020).
- **EC-033**: A present worktree on a branch named `HEAD` (`refs/heads/HEAD`)
  fails closed. Its `branch` and `head` come rightly from the registry, its
  `merged_into_target` from the merged set and its status from its own probe,
  but its `upstream`, `upstream_oid`, `remote_present`, `ahead` and `behind`
  come from the ref listing (DI:423-425; CMD:149-153), which for that ref
  prints the upstream and track of the branch that `HEAD` names where the
  listing runs, whatever `branch.HEAD.*` says. Reproduced for this record on
  Git 2.43.0 with the fixture of feature 004's `8bea203`, and by lane
  openRepoProject-3 on Git 2.36.6 and 2.40.4, the listing exiting 0 with
  nothing on standard error on all three: run at `repository.root`, whose
  checkout is on `main`, the listing credits `refs/heads/HEAD` with
  `origin/main`, and with `ahead 1` once `main` is a commit ahead while that
  ref stays at `origin/main`; at `ahead 0` the worktree then reads as pushed
  and merged and, as feature 004 found, `merged-removable`, and at `ahead 1` as
  `unpushed`. Those five fields are therefore not established: they stay null
  (feature 004's documents and its lead ruling R-61(b) name three of them,
  `upstream`, `ahead` and `behind`; its R-64(a), within R-61(b)'s fill, adds
  `remote_present`, and `upstream_oid` stays unset, `project:2186`; at its head
  `2cf34d3` those documents name four of them, `remote_present` included, with
  R-64 (a): its data model, :70-71 and "Branch evidence", :146-160, its
  contract, :539-546, and its T031, `tasks.md:911-914`, there), and the row is
  `inspection-error` set directly (POD:340-342, :378-381; CLN:114-116), as
  feature 004's `project clean` classifies it at `96a08d4` (POD:381-384 then
  makes the overview equal to it). That is a fill of change 2's rule, not a
  departure, as feature 004's lead ruling R-61(b) fills [L]'s for `project
  clean` (`8bea203`, merged by `6ae927f`; its data model, "Branch evidence",
  and its contract at `96a08d4`); change 2's table (POD:328-335) names no code
  for a Git child that exits 0 with output that cannot be trusted, so the
  overview takes feature 004's `probe-failed` (R-61(b)), and it reads the cause
  list of CLN:114-116 as feature 004 does, as examples. The project row carries
  a `probe-failed` error and status `error` (the collector table's code for a
  Git child that exits nonzero, POD:333, which feature 004 also gives one whose
  output yields no usable value, `unparseable output`; Dependencies), the
  worktree's finding is `inspection-error` (repair, error, no suggestion;
  POD:428), the run is incomplete and exits 1, and `inspection-incomplete`
  withholds `--all-safe` for the repository (FR-034); where the checkout at the
  row's `path` is on that branch, the `git` object's `upstream`, `ahead` and
  `behind` are null too (C-13). Feature 004's guard sits in its row decider,
  not in the listing or its parser: `row_evidence` (`project:2656`) tests
  `HEAD_BRANCH_REF` (:2161-2165) before it reads any upstream, and adds the
  error (:2694-2697) that the ladder's first test reads (:2042-2044). The
  overview inherits that guard only where its rows are built by that decider
  (Dependencies, R-54); a row built from its own parse of the listing (FR-015;
  design D9) is not covered by it, and the same fill applies there. The row
  error's message is the fixed text of `probe-failed`, feature 004's `git
  for-each-ref failed: unparseable output`, no line of Git's standard error
  reaching it (FR-022; Clarifications, C-62). Feature 004's fix of lane
  openRepoProject-3's finding F1 M-1, whose commit lane openRepoProject-2 has
  not yet named, makes a status probe whose standard error holds any line other
  than a hint, or more than 4 KiB, `probe-failed` with DETAIL `unparseable
  output` (lane openRepoProject-2's ruling R-116, which accepts the consequence
  below as failing closed), a DETAIL that feature 004's contract and A1's table
  already give, so FR-022's texts do not change; pending that fix, the
  overview's status probe takes the same rule once it lands, as FR-026's parity
  needs. Its consequence here is wider than this row: a repository that holds
  `refs/heads/HEAD` then makes every worktree row whose status probe runs
  `inspection-error`, each with a `probe-failed` error, `git status failed:
  unparseable output`, because Git warns "refname 'HEAD' is ambiguous." on that
  probe's standard error in each worktree. Reproduced for this record on Git
  2.43.0 with the status probe's arguments and status pins, in the main
  worktree and in a linked one: the probe printed that warning twice, exited 0
  and printed nothing on standard output; lane openRepoProject-3's W17 read
  reproduced the same on Git 2.36.6.
- **EC-034**: Names, branch names and admin ids carry no validity flag of
  their own (FR-038; Clarifications, C-62), so in JSON a valid UTF-8 name
  holding the four characters `\xff` and a name holding the byte `0xFF` decode
  to the same string, as two `ignored_samples` paths do (US11 s2), with no
  flag to tell them apart; a validity flag can still follow later, additively
  within schema 1.
- **EC-035**: Beside EC-015: a signal that arrives while the result is being
  written stops the write, so standard output may hold part of a result, which
  the exit of 129, 130 or 143 marks as no result; a consumer reads no result
  from a run with one of those statuses (FR-044; Clarifications, C-69).
- **EC-036**: A relative `HOME` or `XDG_CONFIG_HOME` makes each Git child read
  its user configuration from inside the directory it runs in: with `HOME=h`,
  `git -C <dir>` reads `<dir>/h/.gitconfig`, which `git config --show-origin`
  prints as `file:h/.gitconfig`, and `GIT_CONFIG_GLOBAL=/dev/null` neutralises
  it. Lane openRepoProject-5's reader RC found it, confirmed by lane
  openRepoProject-4's reproduction (lane openRepoProject-2's ruling R-101 (j));
  the baseline has the same exposure. A file inside a candidate, which a clone
  can carry, then acts as the user's configuration for the overview's Git
  children there. The status probe's `--untracked-files=normal` and
  `--ignored=matching` outrank a planted `status.showUntrackedFiles`, but a
  planted `safe.directory` is honoured as the user's own; and, reproduced for
  this record on Git 2.43.0 with `HOME=h`, the status probe's arguments and the
  two status pins that [E] carried before LQ-10 (FR-016), a clean filter that
  such a file defines runs when the probe re-hashes a path that the
  repository's own `.gitattributes` gives that filter, while an absolute `HOME`
  or `GIT_CONFIG_GLOBAL=/dev/null` runs none (EC-022; lane openRepoProject-2's
  ruling R-105 (c) records it). A relative `GIT_CONFIG_GLOBAL` beside an
  absolute `HOME` runs the filter the same way (lane openRepoProject-3's reader
  W6, and reader RA's H5 in lane openRepoProject-2's ruling R-105), and with a
  relative `GIT_CONFIG_SYSTEM` Git reads a file the repository holds as the
  system's configuration, on Git 2.43.0 and 2.36.6 (lane openRepoProject-3's W8
  read of LQ-15 on PR #19, its check 2): the evidence for [E]'s separate
  sentence on `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`. The overview starts
  no push child, through which lane openRepoProject-2 finds feature 004 exposed
  to a planted `core.hooksPath`, `core.sshCommand` or `credential.helper`.
  Brett Heap's "yes to all six recommendations, LQ-10 to LQ-15" (2026-10-21,
  lane openRepoProject-3's session) decides it as lane openRepoProject-2's
  LQ-15, not built: PR #19 amends [E] at `cc000ea` and `9fb22fa`, pending its
  ratification, so that every subcommand that inspects a Git repository tests
  these values before any Git child starts, and the overview makes the same
  test (FR-043; Dependencies).

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
  sort them by the bytes of their canonical paths (POD:11-16; Clarifications,
  C-3). A root whose canonicalisation is cut MUST take as its `path` the given
  path made absolute (expanded, and joined to the working directory when
  relative) but not resolved, MUST sort by those bytes among the canonical
  paths, MUST never be deduplicated, and MUST count toward the 32-root cap, a
  root past the cap being `omitted` whether or not its canonicalisation was cut
  (Clarifications, C-67).
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
  (POD:32-40, :85-87; DI:284-287; design D7). A candidate other than a family
  holder whose identity probe reports a toplevel that is a proper ancestor of
  the candidate MUST be an error row, as FR-006 states (Clarifications, C-65).
- **FR-004**: A candidate whose directory holds no `.git` entry MUST get no
  Git child: its row MUST have null `repository`, `merge_target`, `git` and
  `worktrees`, no finding for the missing checkout, and status `ok` unless
  an error, such as its manifest's, is recorded (POD:38-39, :66, :319-321;
  proposal, "Absorbing Doctor Repository Health", the "no Git checkout" row;
  Clarifications, C-4).
- **FR-005**: A default root that does not exist, its path expanded but not
  resolved, one of FR-038's exceptions to canonical paths (DI:842-843), MUST be
  reported with state `absent` and no error. An argument or environment root
  that does not exist, is not a directory or cannot be listed, and a default
  root that exists but is not a directory or cannot be listed, MUST be reported
  `unreadable` with a `root-unreadable` scan error, and MUST never cause exit
  status 2 (Clarifications, C-27). A marker check that fails with any error
  other than "no such entry" MUST make that directory an error row (`kind`
  null, status `error`, `findings` empty, one `os-error` whose `path` is that
  directory, every Git-derived field null), sorted and capped like any other
  row. When every root is `absent`, the human output MUST say that no projects
  directory was found, naming `--root` and `PROJECTS_DIR`, in the line design
  D10 fixes (POD:42-51; design D10).

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
  disagreement (FR-007; EC-031). A candidate other than a family holder whose
  identity probe reports a toplevel that is a proper ancestor of the candidate
  MUST be an error row, its error `refused`, its `path` the candidate's `.git`
  and its message a fixed text saying that Git did not accept it and reported
  an enclosing repository, and MUST create or join no repository row; a
  toplevel elsewhere that Git reports for a layout it accepts, such as a
  `core.worktree` naming another directory, is unaffected (Clarifications,
  C-65). Where the main worktree's own `core.worktree` names another directory,
  `project clean` refuses that checkout, passed by its absolute path, with
  `target-not-repository-root`, as PR #19's round (h) records, its round (i) at
  `e0c91bb` giving that refusal a message that names the redirect (R-271; its
  design D18, `design.md:1353-1394`), and its resolution refuses an absolute
  path that is not the toplevel Git reports there (its
  `specs/project-clean/spec.md:566-570`), so that a suggestion naming the
  checkout or that toplevel as the root (FR-009) is refused, or, where the
  toplevel is another repository's root, reaches that repository; A1's
  re-alignment for that layout is held for Brett Heap's ruling for change 2,
  and this spec follows A1 as ratified until then (Dependencies).
- **FR-007**: Each registered path MUST fall into exactly one case: `lstat`
  fails with "no such entry" or "not a directory" (`present: false`, no status
  probe); `lstat` fails otherwise, or the row's task, which encloses its
  `lstat` and registration reads (FR-013), does not finish within its
  filesystem budget or before the deadline (`present: null`, no status probe,
  an `os-error`, or `probe-timeout` or `deadline-exceeded` for a cut call, and
  `inspection-error` set directly); the registration check cannot be completed,
  a read of `<path>/.git`, of the administrative `gitdir` file or of its
  `commondir` file failing with an error that shows no disagreement (no status
  probe, the same codes, `inspection-error` set directly); registration
  disagrees in either direction, a `<path>/.git` that is missing (`ENOENT` or
  `ENOTDIR`) or not a regular file, an administrative `gitdir` file that is
  missing (`ENOENT` or `ENOTDIR`), or an administrative `commondir` file that
  is missing (`ENOENT` or `ENOTDIR`) or does not name `<common_dir>`, being a
  disagreement and not such an error (no status probe, `inspection-error` set
  directly, a `registration-mismatch` finding in place of that class's
  `inspection-error` finding, and no error); otherwise one status probe in that
  worktree. The two registration cases apply to linked worktrees only (C-39).
  The third case is change 2's own text as amendment A1 at `e4a30fc` adds it to
  requirement 2's closed case list, after its second case, in this
  requirement's words for the reads, with no cut of them (its
  `specs/project-overview/spec.md:109-114`, amending POD:89-95), ratified,
  words that also take the toplevel realpath's failure other than with `ENOENT`
  or `ENOTDIR` and the effective-work-tree read's own cut, below, its one cut
  being the realpath's and that read's, "or that realpath or that read itself
  being cut" (its :113): a case that departs from the packet's DI:251-261,
  whose table of the cases a registered path falls into has none for a check
  that cannot be completed. A1's disagreement case takes this requirement's
  tie-break, a `.git` that is missing or not a regular file and a `gitdir` or
  `commondir` file that is missing being a disagreement and not such an error
  (its :114-119), and its second case the cut of the row's task, "its
  filesystem task reaches its 5 s limit or the deadline ends it or prevents its
  start", as this requirement's second case now does (its :105-109) (A1's
  `proposal.md:1393-1422` and :1459-1477; lane openRepoProject-3's W25 M1, W29
  L1, W29 O2 and, for the third case's cut and the second case's task, W34
  LOW-1). The second case names the row's task, and the third case's reads name
  no cut, a fix of words within Brett Heap's answers that leaves every outcome
  as it was: a cut of the row's one task, its `lstat` and registration reads
  together (FR-013), is the second case's, and the cuts of the toplevel
  realpath and of the effective-work-tree read stay with the third case, below
  (lane openRepoProject-3's W34 LOW-1). The `commondir` file, from which Git
  takes the worktree's common directory, MUST be read by the filesystem with no
  Git child, as Git reads it, its trailing line feeds and carriage returns
  removed and a relative value resolved against the administrative directory,
  and compared by realpath with `common_dir`, as PR #19 amends [E] at `93f3194`
  for lane openRepoProject-2's ruling R-125, pending #19's ratification (its
  `specs/project-command/spec.md:204-214`), so that the overview classifies
  such a row as `project clean` does (Dependencies). Present rows of one
  repository that share a realpath, or an admin id, MUST each be a registration
  disagreement as above, the main worktree included when it shares its
  realpath, decided from all of that repository's row reads before any of its
  status probes, a row not present or whose realpath was not read being
  compared by neither, and only a linked row whose registration held having an
  admin id to compare: lane openRepoProject-2's ruling R-67 (c), taken as a
  fill of change 2's rule (EC-031). Immediately before each status probe the
  row's own identity MUST be verified again, and a row that this
  re-verification does not confirm MUST be `inspection-error` set directly with
  no status probe (lane openRepoProject-2's ruling R-101 (j)), with the class's
  `inspection-error` finding: where a re-read value differs, or a re-read, of
  the `lstat`, the realpath or a registration file alike, fails with `ENOENT`
  or `ENOTDIR`, which counts as a differing value, the row carries no row
  error; where a re-read fails in any other way, it carries the code of change
  2's table that fits the failure (POD:326-335), `os-error` for an `lstat`,
  realpath or registration read that fails so, `probe-timeout` for one whose
  filesystem task reaches its limit and `deadline-exceeded` for one that the
  deadline ends or prevents, the re-verification starting no Git child. Either
  way the row keeps the identity of its first read, the one from which its
  twins were decided, the re-read only detecting the change, and the finding's
  severity `error` makes the run exit 1 (POD:762-764), and FR-034's
  `inspection-incomplete` withholds `--all-safe` for the repository (EC-031). A
  linked row whose effective work tree is not its registered path MUST be a
  registration disagreement as above, as PR #19 amends [E] at `addd346` for
  lane openRepoProject-2's LQ-11, pending #19's ratification (its
  `specs/project-command/spec.md:206-219` and :224-232, at :214-227 and
  :232-240 at `93f3194`), the overview classifying such a row exactly as
  `project clean` does. Once per common directory, after the registry listing
  and with its other repository-wide probes, the overview MUST read the
  repository's `extensions.worktreeConfig` by `git config --file
  <common_dir>/config --type=bool --get extensions.worktreeConfig` (change 1's
  design D6, row 4c): `true` reads as true and `false` as false; an exit of 1
  with nothing printed on standard output or standard error, Git's report of a
  value not set, reads as false with no error, as amendment A1 at `e4a30fc`
  excepts it in change 2's table, "the `extensions.worktreeConfig` read's exit
  1 with nothing printed on standard output or standard error, by which Git
  reports the value not set, read as false with no error" (its
  `specs/project-overview/spec.md:369`, amending POD:333), ratified, an
  exception that departs from the packet's collector table, DI:535 ("A Git
  child exits nonzero | `probe-failed`"), an exit of 1 with a warning, as for
  an unreadable `config`, being no such report; and any other outcome counts as
  true, as [E] states, recording on the project row the code that change 2's
  table gives it (POD:333-335), `probe-failed`, its DETAIL `unparseable output`
  for output that is not one of those values, or `probe-timeout` or
  `deadline-exceeded` for a cut read (FR-011, FR-012), the ladder still running
  on the rows' own evidence. Where the extension reads or counts as true, each
  linked row whose registration agrees MUST take `git rev-parse
  --path-format=absolute --show-toplevel` in that worktree, after its identity
  reads and before its re-verification and status probe: a toplevel whose
  realpath, taken in a bounded task (FR-013), is not the realpath of the row's
  registered path, that realpath failing with `ENOENT` or `ENOTDIR` included, a
  probe that fails, by an exit other than 0 (128 under `core.bare=true`), a
  signal or a spawn that fails (`probe-failed`'s `cannot spawn`, FR-022), and
  output that is not exactly one line each make the registration disagree, with
  no error, a rev-parse that cannot be spawned being, on the lane
  openRepoProject-4 lead's ruling, "a probe that fails" in [E]'s words
  (`addd346`, :216-219 there and :224-227 at `93f3194`); only a cut of the
  probe, by its budget or by the deadline ending it or preventing its start,
  and a realpath that fails otherwise or is cut leave the check not completed,
  as in the third case above, with the code of change 2's table that fits it.
  That a cut leaves the check not completed is a fill of [E]'s "a probe that
  fails", which names no cut, decided as change 2's table needs (POD:334-335),
  the class being `inspection-error` either way, which A1's new case of
  requirement 2 carries in change 2's text, "or that realpath or that read
  itself being cut" (its :113), ratified; and the probe's failure, as under
  `core.bare=true` (exit 128, a per-worktree `core.bare=true` included, as lane
  openRepoProject-3's W20 read measured on Git 2.43.0 and 2.36.6), which change
  2's table would make `probe-failed` (POD:333), is the disagreement with no
  error that `addd346` makes it, as amendment A1 at `e4a30fc` excepts the
  effective-work-tree read in the same row of change 2's table, "where a probe
  that fails, as it does under `core.bare=true` and as a probe that cannot be
  spawned does, and output that is not exactly one line each make the row's
  registration disagree, with no error" (its :369), ratified, naming the spawn
  failure on the same ruling (lane openRepoProject-3's W25 L8 and L12). Where
  the extension reads false, no such probe runs. Both children carry FR-016's
  pins and environment, the rev-parse, which is not a status probe, without the
  status pins. `project clean` re-runs the probe when it revalidates a removal
  target; the overview, which removes nothing, has no revalidation
  (Dependencies). A probe MUST NOT run in a path the overview could not
  `lstat`, nor a status probe in a worktree whose registration it could not
  verify or whose identity it could not verify again immediately before
  (POD:89-95; CMD:124-126, :139-142; CLN:114-116; DI:244-245, :267-273;
  Clarifications, C-23, C-26, C-33 and C-39).
- **FR-008**: Every repository MUST first take [R]'s submodule test: when
  Git reports a superproject working tree for a candidate that reached the
  repository, `repository.root` MUST be null with an `unsupported-layout`
  repair finding of severity error, whose message (design D3, item 1) names
  a submodule checkout, with no suggestion and no read of `core.worktree`.
  Otherwise a bare main entry MUST leave `repository.root` null, its
  repository-wide probes running in the common directory, and MUST itself be
  the main worktree row, as design D3 keeps an unnamed gitfile record: its path
  the common directory, `present` from `lstat`, no status probe, null status
  fields and classification, no finding of its own, and counted toward the caps
  and the row count (Clarifications, C-68); and where the
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
  Each child MUST start with SIGINT, SIGTERM and SIGHUP unblocked, under
  handlers that only record the signal, so that SIGTERM to its group can stop
  it before SIGKILL and no termination pass misses it (FR-044; Clarifications,
  C-70).
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
  in "Invocation deadline", and `lower-bound` when a root listing was cut, and
  MUST carry `limit: "invocation_timeout_seconds"`, the `budget` key; every
  other `deadline-exceeded` error, row or scan, MUST carry neither `limit` nor
  `omitted` (POD:176-181, :224-229, :283, :335; DI:496-497; design D6;
  Clarifications, C-30 and C-60).
- **FR-013**: Every filesystem call MUST run in a bounded task waited for at
  most `min(5 s, deadline - now)`, the tasks being those change 2 groups the
  calls into (Clarifications, C-38): one per root, enclosing its
  canonicalisation, deduplication `stat`, listing and marker and holder checks,
  so that a root's whole listing has one budget; one per worktree row,
  enclosing its `lstat` and registration reads, the `commondir` read that
  FR-007 takes from R-125 included (pending), as amendment A1 at `e4a30fc`
  names it in D8's per-row task (its design.md:480-483, amending
  design.md:461-462), ratified; one per linked row whose effective work tree
  FR-007 reads, for the realpath of the toplevel that read reports, compared
  with the realpath of the row's registered path, its `ENOENT` or `ENOTDIR`
  making the registration disagree with no error and any other operating-system
  error, or a cut task, leaving the check not completed, as FR-007 states: the
  task that amendment A1 at `e4a30fc` adds to design D8 with those outcomes,
  and with 512 toplevel realpaths in D8's bound of abandoned workers (its
  design.md:484-491 and :506-508), ratified with A1 (LQ-11, pending #19's;
  FR-007; Dependencies); one per manifest read; one per branch reflog read of
  at most 64 KiB, never by a Git child; and one for the realpath of the working
  directory taken at start, a realpath that cannot be established being
  recorded as FR-026 states (Clarifications, C-61). A task that does not finish
  MUST record `probe-timeout`, or `deadline-exceeded` where the deadline was
  the smaller limit, on its root or row, and the overview MUST move on without
  blocking on it. A root cut this way MUST count as `truncated`, and its
  listing MUST read no further entry once the root is abandoned; a reflog read
  cut this way MUST leave its row unprobed for the repository gate of FR-034,
  and a worktree row's `lstat`, registration read or toplevel realpath cut this
  way MUST make that row `inspection-error` as FR-007 states (POD:183-192,
  :781; clarifications N2; design D2 and D8; Clarifications, C-23, C-25 and
  C-38). A root whose canonicalisation is itself cut MUST be reported as FR-001
  states (Clarifications, C-67).
- **FR-014**: A manifest whose size, taken before the read, exceeds [E]'s
  1 MiB MUST be `manifest-invalid` on its row without being read, and a
  manifest read MUST NOT exceed 1 MiB (POD:192-196; design D8).
- **FR-015**: The ref listing MUST be consumed as it streams, keeping only
  the local heads, `origin/HEAD`, the remote refs named as upstreams and one
  flag recording whether a remote copy of the merge target exists, so that
  what it keeps is bounded by the heads; the status probe and its record
  bounds (64 ignored entries, 4,096 records, 8 samples) MUST be [E]'s
  (POD:196-200; design D9).
- **FR-016**: Every Git child of the overview, the version check included, MUST
  carry the seven protocol pins `-c protocol.allow=never -c
  protocol.file.allow=never -c protocol.ssh.allow=never -c
  protocol.git.allow=never -c protocol.http.allow=never -c
  protocol.https.allow=never -c protocol.ext.allow=never`, MUST run with the
  names of [E]'s environment scrub removed, `GIT_ALLOW_PROTOCOL` included,
  [E]'s list being taken as PR #19 amends it at `423a532`: thirty-one names,
  fourteen of them the trace variables that Git 2.36 to 2.43 read, `GIT_TRACE`
  among them, each listed by name (its `specs/project-command/spec.md:98-119`),
  and with `GIT_OPTIONAL_LOCKS=0` and `GIT_TRACE2`, `GIT_TRACE2_EVENT` and
  `GIT_TRACE2_PERF` set to `0`, which overrides `trace2.*` targets in the
  system and global configuration (:119-124 there; Clarifications, C-63), and
  every status probe MUST also carry [E]'s four status pins, `-c
  core.untrackedCache=false -c core.fsmonitor=false -c core.trustctime=true -c
  core.checkStat=default`, the last two as PR #19 adds them to [E] at `ea697ba`
  for lane openRepoProject-2's LQ-10, pending #19's ratification (its
  `specs/project-command/spec.md:140-147`), and the four as amendment A1 at
  `e4a30fc` restates them where change 2 quoted two, in requirement 3 (its
  `specs/project-overview/spec.md:230-232`, amending POD:202-204) and design
  D13 (its design.md:690-691, amending design.md:650-652), ratified
  (Dependencies). No Git child of the overview is exempt: it starts no push
  child, so feature 004's push-child exception (lead ruling R-28) never
  applies. A lazy fetch in a partial clone MUST therefore fail locally and be
  recorded `probe-failed` on its row, a failed status probe leaving its
  worktree `inspection-error`, with no network call. A Git child is a process
  the overview starts; processes Git itself starts run in that child's process
  group and take the pins from Git (POD:200-215; R-23, R-25; Clarifications,
  C-5 and C-34).
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
  stay null, and their project rows MUST carry `scan-limit` errors, each with
  `limit: "worktree_rows"` and `omitted` counting that repository's rows past
  the cap, exactness `exact` (POD:230-234; design D8; Clarifications, C-35 and
  C-60).
- **FR-019**: At most four Git children MUST run at once, never two once their
  `common_dir` is known to be the same, one repository's children running one
  at a time. Collection MUST run in two canonical phases, the identity and
  repository-wide probes, FR-007's extension read among them, and then the
  worktree probes, a row's effective-work-tree probe, where FR-007 gives it
  one, before its status probe (as amendment A1 at `e4a30fc` names the second
  phase "the worktree probes, effective-work-tree reads and status probes",
  amending POD:238-239, and adds a sentence after POD:246, its
  `specs/project-overview/spec.md:267-269` and :276-278, ratified;
  Dependencies); a repository's first worktree probe MUST wait until every one
  of its rows within the cap has finished the `lstat`, realpath and
  registration reads from which FR-007 decides its twins (EC-031); a
  repository's second phase MUST start only when every candidate earlier in
  canonical order has completed or failed its identity probe and every
  repository earlier in canonical order has finished its first phase, identity
  probes still being free to start ahead of that point; a repository whose
  first registry record equals its `common_dir` and whose checkout no candidate
  has yet named MUST also wait until every candidate's identity probe has
  completed or failed. In a run in which no child, task or root listing reaches
  its budget and the deadline does not expire, over an estate that no other
  process changes during the run (this feature's reading, a condition
  POD:243-246 does not state; EC-023), the JSON document, apart from timestamps
  and `budget.probe_concurrency`, MUST NOT depend on concurrency or completion
  order (POD:236-246; design D3, item 3, and D6; Clarifications, C-28; EC-023).
- **FR-020**: The envelope MUST report `probes: {estimated, performed}`:
  `performed` counting every Git child started, timed-out and stopped ones
  included, and `estimated` counting 1 for the version check, 1 per Git
  candidate, 3 more per distinct repository whose identity was established, 1
  per Git child needed to name the main checkout of a repository whose first
  registry record equals its `common_dir`, and 1 per worktree row within the
  cap that is present and registration-verified, a bare repository's main
  worktree row adding none, since it takes no status probe (POD:248-254; design
  D3, item 3; Clarifications, C-68). It MUST also count FR-007's two children
  (LQ-11, pending #19's ratification; FR-007), as amendment A1 at `e4a30fc`
  amends that rule (its `specs/project-overview/spec.md:280-290`), ratified: 4
  more per distinct repository whose identity was established in place of 3,
  the fourth being the extension read, and 1 more per worktree row within the
  cap that is present and registration-verified and is a linked worktree of a
  repository whose extension read is taken as true, for its effective-work-tree
  probe. These counts depart from the packet's DI:506-509 ("3 more per distinct
  repository") and DI:1193-1201 ("plus three"), as A1 records (Dependencies).
  Where the path of a repository's root or common directory holds a line feed,
  the count stays one identity probe per Git candidate, as A1 gives it, though
  the probe is then read one option per child (EC-032); PR #19's round (h) has
  `project clean`'s `probes.estimated` count those extra children (RI-3, its
  `specs/project-clean/spec.md:1050-1056` at `b3228bb`), and A1's re-alignment
  is held for Brett Heap with #19's ratification (Dependencies).

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
  `path_valid_utf8` beside a present `path`, its `code` one of schema version
  1's closed set: the collector table's eight, `scan-limit` and
  `root-unreadable` (Clarifications, C-41). Its message MUST be at most 200
  characters, the fixed text of its code in amendment A1's table (A1's
  `specs/project-overview/spec.md:385-403` at `e4a30fc`, after POD:347), which
  names no path, the path going in `path`: feature 004's text for `os-error`,
  `probe-failed` and `probe-timeout` (its contract, lead ruling R-45);
  `OPERATION stopped at the invocation deadline` for `deadline-exceeded`; and
  A1's own texts for `manifest-invalid` (`manifest is invalid (CAUSE)`, naming
  the cause, the size bound or the missing library, never the reader's own
  text), `refused`, `undecodable-output`, `internal-error` (`internal error
  (CLASS)`, the exception's class only), `scan-limit` and `root-unreadable`.
  OPERATION MUST be `git SUBCOMMAND` for a Git child, the filesystem call
  (`lstat`, `stat`, `realpath`, `scandir` or `read`) for a filesystem task, and
  `collection` for a candidate whose collection never started and for the scan
  error that counts such candidates. A1's own texts and the OPERATION values
  `stat`, `scandir` and `collection` are its drafted fill, ratified by Brett
  Heap in PR #34 (Dependencies). A Git child's standard error MUST be drained
  and capped as [E] requires (CMD:175-177), and never shown, so that no text
  from it reaches a message or the `Incomplete:` line; Git's own reason is then
  not shown, and the person re-runs the Git command to see it (Clarifications,
  C-62). Evidence gathered before a failure MUST be kept and every field not
  established MUST stay null; a row whose `errors` is non-empty MUST have
  status `error`, else `ok`; and every candidate entering collection MUST yield
  exactly one row or merge into exactly one existing repository row. Without
  the YAML library the manifest reader needs, each row whose directory holds a
  manifest MUST carry a `manifest-invalid` error naming that cause, and the run
  MUST continue (POD:337-347, its message rule as C-62 amends it;
  Clarifications, C-41 and C-62).
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
  equal that report's. A row's `current`, which decides `merged-current` from
  `merged-removable`, MUST be true exactly when the overview's working
  directory lies inside its path, and null when `present` is null (POD:375-386;
  DI:425-427, :778; Clarifications, C-25). When the working directory's
  realpath cannot be established, one scan error MUST record it, `os-error` or
  `probe-timeout`, with feature 004's fixed text for that code and OPERATION
  `realpath`, its `path` the `PWD` environment value when that is set and
  absolute, else omitted, and first among the scan errors; every `current` MUST
  be null; and each row the ladder would classify `merged-removable` or
  `merged-current` MUST be `inspection-error` instead, so that
  `inspection-incomplete` withholds `--all-safe` for its repository (FR-034;
  Clarifications, C-61). This feature MUST NOT realize the exception to that
  equality which `add-project-clean-cache-disposal` (#24) proposes: if #24's
  realization merges first, a cache-only worktree, a merged worktree whose only
  ignored files are Python bytecode caches, is `ignored-local-files` here and
  `merged-removable` in `project clean`, a departure on Brett Heap's word from
  change 2's equality clause (POD:381-386, on DI:620-624) until #24's overview
  block is archived (Clarifications, C-71; Dependencies).

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
- **FR-032**: The `--all-safe` form MUST be suggested only for a worktree [L]
  classifies `merged-removable` that passes, in [G]'s order, the gates the
  overview can evaluate from its own evidence: `main-worktree`,
  `unsupported-path-bytes`, `registration-mismatch` and `locked-worktree`,
  whose first failure replaces the housekeeping finding with its own while the
  classification stays (a row whose registration disagrees being
  `inspection-error` already, by FR-007, that gate keeps [G]'s order without
  deciding a `merged-removable` row; Clarifications, C-26); then
  `unstarted-branch` or `reflog-unavailable`. The index gates
  (`contains-submodule`, `hidden-local-state`) MUST remain exclusions only the
  batch applies (POD:494-502, :525-526; design D5), and so MUST the two gates
  that PR #19 adds after them in [G]'s order, pending #19's ratification:
  `operation-in-progress`, for lane openRepoProject-2's LQ-14 at `43f7107`, and
  then `worktree-only-commits`, for its LQ-13 at `93de4bb` (its
  `specs/project-clean/spec.md:609-616`, :650-666 and :668-690 at `1ebdd90`,
  after its rulings R-124 at `2b86a5f` and R-126 at `1ebdd90`). The overview
  evaluates neither: it makes no listing of a worktree's administrative
  directory and no `logs/HEAD` read for them, and starts no `rev-list` child.
  The overview MUST keep the `--all-safe` suggestion of such a worktree, which
  the batch then excludes itself. Amendment A1 at `e4a30fc` proposes this as an
  item of its own (its `proposal.md:1313-1352`), in requirement 7 (its
  `specs/project-overview/spec.md:590-597`, after POD:525-526) and design D5
  (its design.md:334-341, amending D5's "Only the index gates
  `contains-submodule` and `hidden-local-state` stay residual exclusions the
  batch applies", design.md:324-325), ratified by Brett Heap in PR #34
  (Dependencies): the route departs from the packet's OV:110-113 and
  DI:690-692, which name `hidden-local-state` and `contains-submodule` as the
  only exclusions the batch applies beyond the overview's gates, and the batch
  decides each gate itself, by the one outcome rule of each gate that R-124
  settles at `2b86a5f`, as #19's round (d) amends it at `9267303` (its
  `specs/project-clean/spec.md:719-722` and :741-746 there; lane
  openRepoProject-3's W32 L1 and lane openRepoProject-2's R-208), pending #19's
  ratification. It excludes the worktree on a decided result: a marker present;
  a `rev-list` child that exits 0 and prints anything; a `logs/HEAD` read to
  its 64 KiB bound or holding a line that cannot be parsed. An error on the
  listing, any other error on the read (a missing or empty `logs/HEAD` giving
  no candidate), and a child that cannot be started or exits nonzero make the
  worktree `inspection-error`; a child stopped at its 5 s budget, or a listing
  or read not finished within the filesystem budget, the deadline not being the
  limit, records `probe-timeout` and makes the worktree `inspection-error`; the
  deadline's cut records `deadline-exceeded`; and each of these leaves the
  batch's plan incomplete, as A1 words it in place of revision 3's "which R-124
  is to settle" (its :1324-1339), ratified (Dependencies).
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
- **FR-034**: The `--all-safe` form MUST also be withheld for every worktree of
  a repository whose batch plan [G], as amendment A1 words it, would refuse as
  `inspection-incomplete` (any worktree row `inspection-error`, a row whose
  presence or registration read failed or was cut included, or any row unprobed
  because its reflog read did not finish) or as `inspect-cap` (more worktree
  rows than the batch's row cap), each computed from the overview's own
  evidence, and of a repository with any row the overview's own cap or deadline
  left unclassified, a bare repository's main worktree row, whose
  classification FR-008 leaves null, not being such a row (Clarifications,
  C-68); those findings MUST suggest the read-only form. A repository's
  worktree rows, for both row caps, MUST be every registry entry of the
  repository, the main worktree and the rows with `present: false` included,
  within the overview's 512-row cap or past it (Clarifications, C-46). A
  repository with more worktree rows than the report's row cap MUST have its
  read-only suggestions limited by `inspect-cap`; and when more of one
  repository's `merged-removable` worktrees keep the `--all-safe` form than the
  batch's target limit, each MUST keep it, limited by `target-cap`
  (Clarifications, C-45). `project clean` MUST remain free to recompute, show
  and confirm its own plan and to exclude a suggested worktree (POD:526-537,
  :563-564; design D5). For a row whose reflog read the deadline cut, PR #19's
  round (h) at `b3228bb` has [G] end the plan `deadline-exceeded`, not
  `inspection-incomplete` (O-1, its `specs/project-clean/spec.md:713-718`), a
  read not finished within the filesystem budget while the deadline is not the
  limit staying `inspection-incomplete`; this spec keeps
  `inspection-incomplete` for both, as amendment A1 at `e4a30fc` gives it (its
  `specs/project-overview/spec.md:598-603` and :624), and A1's re-alignment of
  its seven sites is held for Brett Heap's ruling for change 2 (Dependencies).
- **FR-035**: Each finding MUST carry `suggestion_gate`, null unless a gate
  withheld or limited its own suggestion, else the first applicable code in the
  order of the delta's gate table (`target-not-repository-root`,
  `unsupported-path-bytes`, `inspection-incomplete`, `inspect-cap`,
  `scan-limit`, `deadline-exceeded`, `unstarted-branch`, `reflog-unavailable`,
  `target-cap`), and `suggestion_gate_rows`, the repository's worktree-row
  count as FR-034 counts it when that code is `inspect-cap`, else null. The
  finding's `message` and the human text MUST carry the code's fixed remedy
  from that table, its numbers (the batch's row cap, the report's row cap and
  the batch's target limit) taken at run time from the shared constants that
  [G]'s "Clean bounds its Git work and reports omitted work" defines, as
  `limits` reports them, never from a clean plan, and the `--root <repository
  parent>` remedy naming the parent directory of `repository.root`. A root left
  null by `unsupported-layout` or `main-worktree-missing` MUST carry no gate
  code (POD:539-562; design D5; Clarifications, C-11 and C-46). The remedies of
  `unstarted-branch` and `reflog-unavailable` are change 2's as amendment A1 at
  `e4a30fc` gives them (its `specs/project-overview/spec.md:629-630`), which
  US4 s5 and s6 quote; PR #19's round (g) amends `project clean`'s next steps
  for the same two gates (F-7, its `design.md:1191-1197` at `4f1c0e0`), and its
  round (g2) shortens that clause, so that at `3dcd2d8` they read "no commit
  was made on this branch here since it was created; review, then git worktree
  remove yourself (--force if it holds a submodule)" and "the branch's reflog
  is missing, expired or undecidable; review, then git worktree remove yourself
  (--force if it holds a submodule)" (its `design.md:1192-1195`; R-252); A1's
  re-alignment of its sites to #19's ratified wording is held for Brett Heap's
  review with #19's ratification (Dependencies).

**JSON document**

- **FR-036**: `--json` MUST print exactly one JSON document with
  `schema_version: 1` and exactly the fields the delta lists for the
  envelope, the root object, the project row, `repository`, `git`, the
  worktree row, the finding, `summary` and the error object, every one
  always present (an error's `path` optional, and `limit` and `omitted` only on
  `scan-limit` errors and on the `deadline-exceeded` scan error that counts the
  candidates not started, FR-012; Clarifications, C-60), the document being
  rendered whole before its first byte is written (FR-039; Clarifications,
  C-66); `limits` MUST carry
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
  design D11; Clarifications, C-13, C-32 and C-40). A worktree row carries no
  partial-removal note: a worktree that a removal killed midway is a plain
  `dirty` finding, whose read-only suggestion leads to `project clean <root>`,
  which shows feature 004's note (Clarifications, C-59).
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
  their candidate's step order, and scan errors in canonical collection order,
  a scan error for the working directory's realpath coming first (POD:619-621,
  :650-658; design D6; FR-026; Clarifications, C-12, C-40 and C-61).
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
  (POD:660-672; design D11). Every path MUST be absolute and canonical, as
  DI:842-843 has it, with four exceptions: `ignored_samples` paths, relative to
  their worktree, and an absent default root, the two DI:842-843 names; the
  `path` of the scan error for a working directory whose realpath cannot be
  established, the `PWD` value taken raw (FR-026; Clarifications, C-61); and
  the `path` of a root whose canonicalisation was cut, absolute but not
  resolved (FR-001; Clarifications, C-67). Names, branch names, admin ids and
  every other string the report takes from the filesystem, a manifest or Git
  MUST follow [P]'s path rule as a path does: decoded as a path is, each
  undecodable byte written `\xHH`, each Cc, Cf, Zl or Zp code point escaped by
  JSON and written `\uXXXX` in human output, with no validity flag of their own
  (EC-034; Clarifications, C-62).
- **FR-039**: Under `--json`, an exit status 2 other than an argument error or
  a failed write to standard output (below) MUST print only `{"error":
  "<message>", "code": "<code>"}`, the code being `git-too-old` or
  `git-unavailable` for a version refusal, `relative-config-path` for FR-043's
  refusal of a relative configuration path (A1's
  `specs/project-overview/spec.md:752-757` at `e4a30fc`, landing with PR #19's
  ratification of LQ-15's commits, as FR-043 and Dependencies state), and
  otherwise that of an exception raised outside the per-candidate boundary,
  mapped by its kind: a refusal gives `refused`, an operating-system error
  `os-error`, and any other exception `internal-error` with a message naming
  the exception class, each with exit status 2 and no traceback. Without
  `--json`, a refusal or an operating-system error MUST keep the baseline
  report, `REFUSED: <message>` on standard error (feature 002,
  `contracts/project-new.md:121`, "Streams"), and an exception of any other
  kind MUST also exit 2, never with the interpreter's default 1. An argument
  error MUST print the command-line parser's usage message on standard error
  and no JSON (POD:675-679, :705-707; DI:1083-1090). POD:705-707 says only "an
  exception" and gives `internal-error`; this feature's reading, which narrows
  that scenario's WHEN, is an exception of the kind the collector table maps to
  `internal-error`, the other two kinds having the outputs above, and the
  scenario's test keeps its name. The whole document or report MUST be rendered
  before its first byte is written, as UTF-8 whatever the locale, the JSON
  document with ASCII escapes as feature 004 writes its own (its lead ruling
  R-38), every interpolated string already escaped by [P]'s rule. A failed
  write to standard output MUST end the run with exit status 2, no traceback
  and no retry, every child being already reaped or abandoned: nothing more
  goes to standard output, and one line goes to standard error on a best-effort
  basis. Besides an argument error, it is the one exit 2 under `--json` that
  prints no error object, and so no code; a recorded signal decides the status,
  also over that exit 2 (FR-044). Every other exception outside the collector
  ends as this requirement maps it (POD:675-679 and the packet's DI:1086-1089,
  from which C-66 carves the failed write out; Clarifications, C-66).

**Local and read-only**

- **FR-040**: The overview MUST open no network connection and make no
  filesystem or Git mutation: no fetch, pull, reset, bootstrap, validator run
  or file write; no worktree created, pruned, repaired, locked or unlocked; and
  no index rewritten, every Git child running read-only as [E] defines, with
  FR-016's pins and scrub. For its Git children the guarantee extends only to
  what those pins and that scrub prove: the clean and process filters a
  repository's attributes name, a residual that LQ-10's status pins widen, as
  #19's design Risks and amendment A1 record it beside requirement 9's sentence
  after POD:717 (its `proposal.md:1443-1452` at `e4a30fc`, ratified), and what
  Git reads from the user's and the system's configuration, are recorded
  residuals beside EC-006 (EC-022), outside the guarantee, which reaches no
  `gh` child: the overview starts none, and #25's `gh` children would get the
  caller's environment, the `GIT_TRACE*` names included, unread (EC-022). It
  MUST read no credential file and no profile data the scan does not need, and
  MUST keep no state beyond one invocation. Ahead, behind and merge evidence
  MUST be presented as observations as of the last fetch, and both outputs MUST
  say so (POD:710-717, its read-only wording as C-63 amends it; Clarifications,
  C-63).

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

- **FR-042**: The overview MUST exit 0 when `completeness` is `complete` and no
  finding has severity `error`; 1 when the result is incomplete, a finding has
  severity `error`, or `--strict` is given and a finding has severity
  `warning`; 2 for an invalid invocation, an exception raised outside the
  per-candidate boundary, a Git refusal or a relative configuration path
  (FR-043); and 130, 143 or 129 on SIGINT, SIGTERM or SIGHUP. On 0 or 1 the
  full result MUST be printed, and a root problem MUST never cause status 2
  (POD:762-768, as A1's `specs/project-overview/spec.md:860-866` at `e4a30fc`
  amends it, landing with PR #19's ratification of LQ-15's commits, as FR-043
  and Dependencies state).
- **FR-043**: The overview MUST run [E]'s version check once per invocation,
  after the deadline is set and before any root is listed, and MUST refuse a
  Git older than 2.36 with `git-too-old`, and a missing `git`, a failed or
  timed-out version child or an unparseable version with `git-unavailable`,
  each with exit status 2, a message naming the 2.36 minimum, such as the
  packet's "project overview needs Git 2.36 or newer; found 2.34.1"
  (DI:322-323), and no other Git child; such a refusal MUST never be reported
  as an incompleteness (POD:770-776). Before that check, and once its arguments
  have passed the checks that refuse an invalid invocation, which start no Git
  child, so that such an invocation is refused first (FR-042), the overview
  MUST make the test of [E]'s "Configuration paths", as PR #19 amends [E] at
  `cc000ea` and `9fb22fa` for lane openRepoProject-2's LQ-15, pending #19's
  ratification (its `specs/project-command/spec.md:100-111` at `cc000ea` and
  :116-129 at `9fb22fa`), in the order that `9fb22fa` gives `project clean`
  (its `specs/project-clean/spec.md:13-18`): where `HOME` or `XDG_CONFIG_HOME`
  is set to a non-empty value whose first byte is not "/", the test made on the
  raw bytes, an empty or unset variable passing it, and applied to each
  variable whether or not Git would read a file through it, not following Git's
  order of precedence (:121-123 at `9fb22fa`, rewording `cc000ea`'s "whichever
  of these variables Git would use"), the overview MUST refuse, starting no Git
  child, the version check included, and inspecting no repository. The same
  test MUST apply to `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`, as that text
  has it (:103 at `cc000ea`, :119-120 at `9fb22fa`; EC-036): LQ-15's extension,
  which Brett Heap may strike (Dependencies). PR #19 leaves the overview's code
  and exit status for this refusal to `add-project-overview` (its
  `proposal.md:951-956` at `9fb22fa`), whose closed lists give [E]'s text none:
  amendment A1 at `e4a30fc` proposes `relative-config-path` with exit 2 as an
  item of its own, on the basis of Brett Heap's LQ-15 word, whose form the lead
  gave as `clean`, `status`, `doctor` and `update` (lane openRepoProject-2's
  ruling R-102 (c) 3; `9fb22fa` proposal.md:954-956), in requirement 8's exit-2
  codes (POD:677-678; its `specs/project-overview/spec.md:753-757`) and in
  requirement 11's exit rule (POD:765-768; FR-042), with a paragraph after it
  and the scenario "A relative configuration path" (its :860-876 and :908-912),
  ratified by Brett Heap in PR #34 (Dependencies). FR-039 and FR-042 restate
  those two sites, and US10 s5, SC-012 and the Appendix carry the scenario (the
  lane openRepoProject-4 lead's re-read against A1's ratified text, as A1's
  `proposal.md:1509-1510` at `e4a30fc` records that this spec does; lane
  openRepoProject-3's W55 L5). The code departs from the packet's closed list
  of exit-2 codes (DI:1086-1089); should he strike it, the fallback is
  `refused` with exit 2, inside change 2's lists, which departs from nothing
  (Dependencies).
- **FR-044**: On SIGINT, SIGTERM or SIGHUP the overview MUST stop scheduling,
  terminate and reap every child as FR-011 states, abandoning one still
  unreaped 2 s after SIGKILL, start no result document once the signal is read
  and stop one that is being written, print `Cancelled.` to standard error on a
  best-effort basis (Clarifications, C-47), and exit with that signal's status,
  which takes precedence over 1; a signal MUST never become a row error, and a
  Git child MUST NOT outlive the run, except one abandoned while still unreaped
  2 s after SIGKILL (EC-001) and under EC-002. A signal that arrives while the
  result is being written MUST stop the write, `Cancelled.` following on
  standard error, so that standard output may hold part of a result, which the
  signal's exit status marks as no result (EC-035); a signal recorded before
  the run exits MUST decide its status, also over the exit 2 of a write that
  fails after it (FR-039). The result MUST be written inside a raising span,
  entered before its first byte is written and only after every child is reaped
  or abandoned, so that a signal recorded while rendering prints nothing, and
  output not yet written MUST be discarded, never flushed at exit
  (Clarifications, C-69). While a Git child can run, the handlers for the three
  signals MUST only record the signal, and each Git child MUST start with the
  three unblocked, so that no termination pass misses a child; for the raising
  span alone the handlers MUST raise once they have recorded the signal, so
  that a write blocked on a stalled reader stops, and no child runs under them.
  That is the scope that amendment A1's design D1 gives Q15 A and Q16 B
  together (A1's design.md:116-127, its clarifications.md:42-45 and its
  `proposal.md:1454-1457`, at `e4a30fc`, ratified; POD:776-781, as C-69 amends
  it; clarifications N1, as C-70 amends it; design D1, as C-69 and C-70 amend
  it; FR-011; Clarifications, C-70).

**Human report**

- **FR-045**: Without `--json`, the overview MUST print to standard output, for
  each shown row, one header line with the name and the absolute path; one line
  per shown finding with its category, code and message, followed by the
  worktree path for a worktree's finding; and, when the row has a suggested
  command or a gate decided it, one `next` line carrying that command,
  shell-quoted or in the `$'...'` form, or `none` where a gate left no command
  (Clarifications, C-44), followed by `(withheld: <remedy>)` when a gate
  removed the `--all-safe` form or every clean suggestion, or by `(limited:
  <remedy>)` when a suggestion is given but capped, the deciding gate chosen as
  design D10 states. Rows, the findings and row errors within a row, and the
  `Incomplete:` lines MUST follow the JSON document's order (FR-037;
  Clarifications, C-43). Row errors MUST display in the repair category; one
  `Incomplete:` line MUST follow per scan error; a row error that carries a
  `path` MUST be followed by that path on the next line, indented to the
  message column, as a worktree's finding is by its worktree path, and the
  `Incomplete:` line of a scan error that carries a `path` MUST read
  `Incomplete: <path>: <message> (<code>).`, as the packet's human report names
  the root it concerns (DI:94), one that carries none reading `Incomplete:
  <message> (<code>).`, every such path printed by [P]'s rules, in the `$'...'`
  form where they mark it, since every message is a fixed text that names no
  path (FR-022): a fill that amendment A1 at `e4a30fc` declares under Q8 D, in
  design D10 (its design.md:548-550, :556-559 and :567-572, amending
  design.md:519-520 and :526-527) and requirement 12 (its
  `specs/project-overview/spec.md:934-938`, amending POD:812-813), ratified by
  Brett Heap in PR #34 (Dependencies; lane openRepoProject-3's W7 read of A1,
  M1); and the summary line MUST always be printed, giving the counts of
  projects, errors and findings by category and stating that findings reflect
  local refs as of the last fetch, and saying that nothing needs attention
  under `--attention` when no row is shown; a complete scan that finds no
  project says so through that line, which then reads `0 projects`, and exits 0
  (POD:722; DI:1097-1098; design D10). A path holding a code point of FR-038's
  categories or an undecodable byte MUST print in the `$'...'` form, each such
  code point written `\uXXXX`, or `\UXXXXXXXX` above U+FFFF. The layout and
  fixed lines MUST read as design D10 fixes them, their fixed text in ASCII,
  while interpolated names, paths and numbers follow FR-038 and [P]
  (POD:672-675, :722, :802-817; DI:1097-1098; design D4, D6 and D10;
  Clarifications, C-43 and C-44).
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
  roots and `PROJECTS_DIR`, the caps, `--attention`, `--strict`, the exits, the
  JSON envelope, and that a suggestion is advice to review, not permission; how
  to check one project (`project overview --root <dir>`, replacing the closed
  PR #2's doctor health); that `git fetch` refreshes merge evidence; that roots
  on a Windows drive mounted into WSL2 can truncate on every run; that a
  filesystem call stuck in the kernel can hold process exit; that a merged
  worktree whose upstream was deleted gets the gated `--all-safe` suggestion
  like any merged worktree, while an unmerged `remote-gone` one gets only the
  read-only `project clean <root>`, which reviews it (proposal, Impact; design,
  Risks); and that the check of one Triad assembly reports each submodule leg
  row with `unsupported-layout` and exits 1 (EC-014; Clarifications, C-55).
- **FR-049**: Automated tests over temporary fixtures MUST cover every delta
  scenario with at least one test named after it, a skipped test not counting,
  in human and `--json` form, with a scratch home directory, `PROJECTS_DIR` set
  or unset explicitly, networking disabled and the zero-mutation snapshots
  taken before and after. Networking disabled MUST mean that in-process runs
  install an audit hook that fails the test on `socket.connect`, that the
  counting wrapper checks every Git child as below, and that the partial-clone
  fixture's `remote.origin.uploadpack` names a logging script that never runs
  (design D13; CMD:227-231); a network namespace MAY be added where an
  unprivileged one can be made. A counting `git` wrapper first on PATH MUST
  record each child's arguments, directory, process group and start and end
  times, MUST be able to hold a chosen status probe, and MUST assert that no
  argument vector fetches, pulls, pushes or reaches a remote, that every one
  carries the seven protocol pins, that each child has `GIT_TRACE2`,
  `GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF` set to `0`, and that none of the
  names [E]'s scrub removes reaches a child, a child being a process the
  overview starts (FR-016; Clarifications, C-34 and C-63); the concurrency
  limits MUST be checked from that log's intervals, and fixtures MUST lie
  outside every Git work tree. Every fixture whose result is compared with
  `project clean` and that has an ignored file MUST make it one such as
  `local.env`, which no cache rule that #24 proposes admits, so that the parity
  tests hold whichever realization merges first (Clarifications, C-71). A test
  MUST NOT need a running filesystem monitor: the packet's fixtures that held
  the status probe through a `core.fsmonitor` hook (its probe-timeout and
  bounded-concurrency fixtures) MUST hold it through the wrapper instead, since
  [E] pins `core.fsmonitor=false` on every status probe. A hung filesystem call
  MUST always be tested by an injected slow call, and a FUSE fixture MUST run
  in addition where a mount can be made, only that variant being skipped, with
  its reason, where none can; where the injected call stands in for a hung main
  checkout ("A repository root on a hung mount"), the wrapper MUST also hold
  each Git child that runs in that checkout (design D13). The device-and-inode
  deduplication of roots and candidates, and the canonically first spelling,
  MUST be tested through an injected file-status call that reports one device
  and inode for two realpaths. Only the invocation-deadline scenario MUST
  shorten the deadline and the per-child budget, in-process and keeping their
  ratio, the grace and the reap wait staying 2 s each, so that its bound is the
  shortened deadline plus 4 s from the moment the deadline is set (design D13);
  a cap or concurrency fixture that asserts an uncut run MUST fail, never skip,
  when its run reports a `probe-timeout` or a `deadline-exceeded`. A fixture
  that depends on a permission being refused MUST be skipped, with that reason,
  when the tests run as root. Non-UTF-8 path tests MUST run on Linux, where
  every CI job runs, and be skipped on macOS with that reason, the `$'...'`
  form asserted as a string; the signal tests MUST assert that every child's
  process group is gone, apart from abandoned ones; every functional
  requirement, or part of one, that no delta scenario exercises (among them
  FR-004's candidates that are not family holders, FR-007's twins, its identity
  re-read before a status probe, and its extension read, effective-work-tree
  probe and `commondir` check, a counting wrapper recording no `rev-parse`
  child in a linked worktree where the extension reads false, FR-010, FR-020's
  `estimated` count, FR-021's `refused` and `undecodable-output` codes,
  FR-022's message bound, FR-033's reflogs of 65,535 and 65,536 bytes, FR-037's
  order and FR-039's `refused` and `os-error` outputs) MUST be covered by at
  least one test as well, the feature's traceability record naming it; and
  every existing test on `main` when the feature is implemented MUST keep
  passing unchanged (proposal, Impact; design D13; Clarifications, C-6).
- **FR-050**: Feature 004's Git 2.36 floor job, `git-floor` (its FR-067), MUST
  also run a small set of the overview's tests, selected by one more `-k`
  prefix beside the job's own: the version check accepting Git 2.36, and one
  end-to-end run over a fixture with linked worktrees, merge targets and a
  gated suggestion. Change 2's Impact as ratified lists `project`, the README
  and the tests and no CI change (proposal, Impact). Brett Heap's answer of
  2026-10-21 records this CI change "as a departure from change 2's Impact on
  Brett Heap's word (or carried in the change-2 amendment's Impact)", and
  amendment A1 takes the second branch: its Impact gains a
  `.github/workflows/tests.yml` bullet after the tests bullet
  (proposal.md:441-449; its `proposal.md:456-461` at `e4a30fc`), ratified by
  Brett Heap in PR #34 (Dependencies), so this requirement realizes A1's Impact
  and records no departure of its own (Clarifications, C-57; Dependencies).
- **FR-051**: After feature 004 lands, the feature MUST add one sentence on the
  overview to the `AGENTS.md` section that feature 004's task T123 adds,
  "Cleaning up worktrees for a person" (written at feature 004's head
  `2cf34d3`, `AGENTS.md:53-70` there, not yet on `main`), saying that an
  overview suggestion is advice to review and that applying it needs the
  person's word; the sentence follows that section's title and wording if
  either changes at feature 004's merge. It is a departure from change 2's
  Impact, which names no `AGENTS.md` change (proposal, Impact), recorded on
  Brett Heap's word of 2026-10-21 as feature 004 records its own departures
  (its lead ruling R-32). If Brett Heap declines feature 004's T123 departure,
  this requirement does not apply, and agent guidance on the overview and the
  batch apply goes instead to a separate small OpenSpec change after feature
  005 (Clarifications, C-58; Dependencies).

### Key Entities *(include if feature involves data)*

- **Root**: a directory the scan starts from: its canonical `path` (the given
  path made absolute but not resolved when its canonicalisation was cut;
  FR-001; C-67) and validity flag, `source` (`argument`, `environment` or
  `default`), `state`
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
- **Row error** and **scan error**: `{code, message, path?}`, the message the
  fixed text of its code, with a validity flag beside `path`; `scan-limit`
  errors and the `deadline-exceeded` scan error that counts the candidates not
  started add `limit` and `omitted: {count, exactness}`, exactness being
  `exact`, `lower-bound` or `unknown` (FR-012, FR-022, FR-036; C-60, C-62).
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
  100% of the overview's Git children (Clarifications, C-34), 0 scrubbed names
  in any child's environment, `GIT_TRACE2`, `GIT_TRACE2_EVENT` and
  `GIT_TRACE2_PERF` at `0` in 100% of them (FR-016; Clarifications, C-63), and
  0 argument vectors that fetch, pull, push or reach a remote.
- **SC-003**: For 100% of worktree rows that `project clean <root> --json`
  inspects from the same directory at the same refs, the overview's
  classification equals clean's, apart from a cache-only worktree once #24's
  realization is on `main` (FR-026; Clarifications, C-71), and for 100% of
  repositories with a merge target its name equals the one clean reports.
- **SC-004**: 0 suggestions carry `--apply` or `--yes` or name a project by
  bare name; 0 rows with a null root, or a root or common directory that is not
  valid UTF-8, carry a clean suggestion; and in every fixture, each worktree
  whose finding carries the `--all-safe` form with no withholding gate is, in
  the preview that suggestion runs when that preview's own deadline does not
  cut it, either selected or excluded only as `deferred-target-cap`,
  `contains-submodule` or `hidden-local-state`, or, once PR #19 is ratified,
  `operation-in-progress` or `worktree-only-commits` (FR-032), or, when that
  preview's own index-gate read fails or times out, or, for those two gates,
  its listing fails, its `logs/HEAD` read fails other than as missing, its
  `rev-list` child cannot be started or exits nonzero, or, the deadline not
  being the limit, its `rev-list` child is stopped at its 5 s budget or a
  listing or read of theirs does not finish within the filesystem budget, made
  `inspection-error` in a preview that is then incomplete (CLN:800-803; for the
  two gates, PR #19's `specs/project-clean/spec.md:650-666` and :668-690 at
  `1ebdd90`, after R-124 at `2b86a5f`, and :719-722 and :741-746 at `9267303`,
  after its round (d), pending).
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
  every field the delta lists; in 100% of `--json` runs that exit 2 other than
  an argument error or a failed write to standard output, it is only `{"error":
  "<message>", "code": "<code>"}` (FR-039; Clarifications, C-66); every valid
  UTF-8 path round-trips exactly; and
  every other path carries a false validity flag and feeds no suggestion.
- **SC-010**: Human output contains 0 raw characters of general category Cc,
  Cf, Zl or Zp and 0 undecodable bytes from a path or from any other string
  FR-038 escapes, names, branch names and admin ids among them (A1's
  `specs/project-overview/spec.md:748-752` at `e4a30fc`; the lane
  openRepoProject-4 lead's re-read against A1's ratified text, its second
  pass's N1), and every fixed line, message and remedy matches design D3, D4,
  D5 and D10, the delta's gate table and amendment A1's table of error messages
  (A1's `specs/project-overview/spec.md:385-403` at `e4a30fc`, ratified;
  FR-022), OPERATION taking only the values that table names, character for
  character in its fixed text, which is ASCII.
- **SC-011**: Every run's exit status is the one FR-042 gives, a recorded
  signal deciding it (FR-044); after SIGINT, SIGTERM or SIGHUP, 0 of the
  overview's child process groups remain, apart from children abandoned while
  still unreaped 2 s after SIGKILL, no result document was started after the
  signal was read, and one that was being written was stopped (EC-035;
  Clarifications, C-69).
- **SC-012**: Each of the 64 delta scenarios, 62 in
  `specs/project-overview/spec.md` and 2 in
  `specs/project-review-safety/spec.md` as amendment A1 at `e4a30fc` gives
  change 2's deltas (its "A relative configuration path" landing with PR #19's
  ratification of LQ-15's commits; FR-043), has at least one automated test
  named after it that runs, a skipped test not counting; every test on `main`
  when the feature is implemented keeps passing unchanged; the CI jobs stay
  green; the requirements file gains no dependency; and no subcommand but
  `overview` changes its output, flags or exits.
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
- No clarification marker is used: the change specifies the behaviour, and the
  spec follows it as ratified and as Brett Heap's answers amend it. The points
  this spec settles from the change's own text are listed under Clarifications;
  the questions genuinely left open were asked in `clarify-questions.md`, and
  his answers of 2026-10-21 are folded under Clarifications as C-55 to C-71.
- The caps and budgets stand as governance task 2.1 measured them on
  2026-10-09: the caps' worst case takes 48.3 s of the 60 s deadline on a
  Linux filesystem; a Windows drive mounted into WSL2 was not measured
  (proposal, OQ-4; design, Risks).
- The change pins its code citations at `da33d92`. Features 003 and 004 change
  `project` and the tests after it, and the CI change of `e9d6711` (#32) moved
  the two workflow lines the change cites, `.github/workflows/tests.yml:10` and
  `:18`, to lines 9 and 17, so this spec cites no line of `project`,
  `README.md` or the workflow as `main` has them, its only lines of feature
  004's `project` being those of EC-031, EC-033 and the Dependencies, at
  `96a08d4`, and those that EC-031 and the Dependencies cite for the re-check
  of 2026-10-21, at `2cf34d3` (header); the plan re-pins every citation against
  the `main` of its day (proposal, "Dependencies and Sequencing").
- Feature 004's names (classifications, gate and refusal codes, row error
  codes, `schema_version`, exit statuses, the shared constants) are taken from
  its spec, data model and contract at `d81b3d9`, apart from EC-031 and EC-033,
  which read its branch's head, `96a08d4`; that head's documents change after
  `d81b3d9` by the tier tags, file and verify fields and ticks of `tasks.md`,
  two additions to `plan.md` and its doc round 6 (rulings R-55 to R-57 and R-59
  to R-62, with the items of R-53 and R-54 that they settle), none differing
  from `6ae927f`'s but in the ticks of `tasks.md`, and its code, which changed
  after `a32d20b` by its T047, by lane G's follow-up to its evidence model and
  by its US1 plan lane (`2733dea`), has its tasks T001 to T040 and T047 to T053
  built (47 of 133), among them its five incremental parsers, its child handle,
  its driver and its evidence model (merged as `cce8dbd`), and none of it is on
  `main`; at its later head `2cf34d3`, re-checked on 2026-10-21 with the pins
  kept, all 133 tasks are ticked and none of it is on `main` either (header,
  "Re-checked on 2026-10-21"); where the change and feature 004 differ for the
  overview, the change governs, and where the change is silent and feature
  004's rule keeps FR-026's parity, this spec takes that rule as a fill and
  says so (EC-031, EC-033), and the plan reconciles against feature 004's text
  as merged into `main`, after which it starts (Clarifications, C-56).
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
  starts only once feature 004 has merged into `main`, on Brett Heap's word
  given after that merge, and pins against that `main` (Clarifications, C-56).
  The overview drives feature 004's runner as change 1's clarification N2
  shapes it, which feature 004's FR-062 commits it to share (several children
  at once through one environment scrub, termination path and set of parsers)
  and its plan and tasks realize as: the child handle (start a Git child in its
  own process group under the scrubbed environment, expose its standard output
  and standard error, stop its group with the 2 s grace, reap it); the one-wide
  driver of that handle, the serial path every other subcommand uses, beside
  which the overview drives up to four handles from its own loop (this change's
  clarification N1); and the pure incremental parsers of the status, registry,
  ref-listing and merged-set outputs, fed chunks and doing no I/O. Of the four,
  only the status parser reports a reached record bound (its 65th ignored or
  4,097th record); the registry parser (`WorktreeListParser`, `project:1783`),
  `RefParser` (:1829) and `MergedSetParser` (:1869) keep every record, each
  documented "No bound" at `96a08d4`, which change 1's design leaves unbounded
  for the last two: its D2 (`design.md:164-176` at `96a08d4`) gives a bound to
  the status parser alone, and its D6 says of row 6 only that it "yields every
  branch's head" (`design.md:291`) and nothing of a bound for rows 6 and 7
  (lead ruling R-70(b)). FR-015's keep-filter, which keeps only the local
  heads, `origin/HEAD`, the remote refs named as upstreams and one flag
  recording whether a remote copy of the merge target exists (POD:196-200), is
  therefore this feature's own to build, as R-54's X-2 leaves to it the
  factoring of `start_child` and `conclude` out of `run_bounded`, and feature
  004 adds no hook for it. Feature 004's data model at `d81b3d9` records that
  handle, plan-stage detail for this feature, as its "Child handle" entity,
  with the states `running`, `terminating`, `killing`, `reaped` and
  `abandoned`, the kinds `probe`, `removal` and `delegate` (the `git branch -d`
  child), of which the overview starts only `probe` handles, and a termination
  that never blocks (lead ruling R-30); and, as its "Invocation" entity, the
  state of one run of `project`: the per-child budget (5 s under `clean`, 15 s
  otherwise), the clock, the counters, the memos, and the phase by which the
  driver reads the signal slot, raising `Interrupted` only in phase `planning`
  or on a second SIGINT in phase `reconciling` (lead rulings R-44 and R-47).
  Its contract fixes a human message for each refusal code that had none, which
  the plan may adapt for `git-too-old` and `git-unavailable`, naming `overview`
  where it names `clean`; beside `clean`'s two texts it gives command-neutral
  ones for a `status` or `doctor` row, "Git VERSION is older than 2.36;
  repository inspection needs Git 2.36 or later." for `git-too-old` and its
  counterpart for `git-unavailable` (lead ruling R-48). It also fixes one
  message per row-error code (lead ruling R-45), the `probe-failed` one being
  `OPERATION failed: DETAIL`, DETAIL one of `exit N`, `signal N`, `cannot spawn
  (STRERROR)` and `unparseable output`, with no line of Git's standard error;
  FR-022 takes those texts for `os-error`, `probe-failed` and `probe-timeout`,
  amendment A1 changing POD:337-338 to match (Clarifications, C-62). It also
  reads feature 004's evidence model [E] with the version check, the scrub (its
  list as PR #19 amends it at `423a532`, thirty-one names; Clarifications,
  C-63) and the pins, the ladder [L] as a pure function of a row's evidence,
  the gates and refusal codes [G] with the shared constants (the 128-row and
  256-row caps and the 16-target limit, which feature 004 keeps in its own
  constants table and the overview reports as `batch_row_cap`, `report_row_cap`
  and `targets`), Git-first resolution [R], the path rules [P] and the 1 MiB
  manifest read (proposal, "Dependencies and Sequencing";
  `add-project-clean-all-safe` clarifications N2 and design D2). Lane
  openRepoProject-2's ruling R-54 (2026-10-20) has feature 004 separate each
  evidence step's reads from a pure decision that this feature's own loop can
  call, the evidence keyed by device and inode, with the repeated identity
  probe at the root skippable; that split is built in feature 004's `project`
  at `96a08d4` (commit `7d70b02`, a refactor with no behaviour change). The
  deciders run no Git child and make no filesystem call: `presence_from_lstat`
  (`project:2278`), `registration_verdict` (:2469), `main_worktree_decision`
  (:2384) and `row_evidence` (:2656), with `gitdir_line` (:2343) and
  `shared_paths` (:2634). The wrappers read in the evidence's order and keep
  their return shapes: `main_worktree` (:2423), `verify_registration` (:2497),
  `inspect_repository` (:2534) and `worktree_rows` (:2762), which also takes
  the registry records to build rows for (`records=None`, R-53(d)), its reads
  of one row being `_read_row` (:2725). The memo of `inspect_repository` is
  keyed by the common directory's (dev, ino) (:2580-2583), and row 5, the
  repeated identity probe at the main worktree, sits behind the keyword
  `repeat_identity_at_root`, on by default, a result without it being memoized
  apart (:2534, :2597). Feature 004's `tasks.md` at that head still records no
  such split: it names R-54 only as the X-2 and X-3 of its tasks (:1846,
  :1172). The driver's start and outcome rules stay inside feature 004's
  one-handle driver, unchanged at `96a08d4`, and this feature's plan factors
  them out, without changing behaviour, after feature 004 lands. Re-checked on
  2026-10-21 at feature 004's head `2cf34d3`, this account holds with these
  changes. The deciders also include `shared_identities` (`project:2766`), lead
  ruling R-67 (c)'s decider for two spellings of one worktree (EC-031), which
  that code names among the pure deciders "so that another driver (feature
  005's overview) can feed it values it read itself" (:2259-2269). A row's
  reads are now `_read_row` (:2867-2895), which runs no status probe, then that
  twin check over the reads of every row one `worktree_rows` call builds, then
  `_read_status` (:2898-2908); lane openRepoProject-2's ruling R-101 queues, as
  a code fix, a second verification of each row's own identity immediately
  before its probe (FR-007). Feature 004's `tasks.md` (:798, :878) and
  `plan.md` (:75) now record the split as R-54 X-1, the two lines cited above
  being at `tasks.md:2194` and `:1283`. `run_bounded` (:1472-1597) gains two
  parser hooks, `feed_stderr` (T077, `6167503`; lead rulings R-53 P-1 and R-54
  X-2) and `tick` (T092, `651b610`; lead ruling R-83 P-1, which amends R-54
  X-2), and this feature's factoring of `start_child` and `conclude` keeps
  both. Its five incremental parsers are identical to those of `96a08d4`, and
  `RelayParser`, T077's relay of `git branch -d` (`project:5759`), is new, so
  FR-015's keep-filter is still this feature's own to build. Its scrub still
  removes the seventeen names there, and its draft #33 builds [E]'s list as PR
  #19 amends it (lead ruling R-99 (b) and (d)). One defect found there reaches
  a parity case: a failed ref listing makes `project clean` print every row as
  `unpublished`, with no row errors (lane openRepoProject-2's plan review,
  finding F3, in its record R-100 (c)), where the overview records the error
  and runs no ladder (FR-025, FR-026), so that a parity test of that case
  differs until feature 004's fix, assigned by R-101 (c), lands.
- **Change 1's archive order**: change 2 archives after change 1. This
  feature realizes change 2's MODIFIED `project-review-safety` requirement,
  not change 1's `project-clean-review-safety` (proposal, Capabilities;
  design, Migration Plan step 5).
- **Open items elsewhere that do not block this spec**: change 1's open
  question 2 (the lane's LQ-2: squash merges and a local patch-equivalence
  proof) is still before Brett Heap and deferred, on the lead's recommendation,
  to a follow-on change, which the overview would inherit through [L] (EC-013);
  and feature 004's push-child exception (LQ-3, draft PR #19, lead ruling
  R-28), also awaiting his word, concerns `clean`'s push child alone, which the
  overview never starts (FR-016). Feature 004's plan at `2cf34d3` also lists
  two open items that reach the overview. LQ-8 (its `plan.md:403`; lead ruling
  R-61 (a)): a printed `$'...'` command holding a `\u` or `\U` escape reads
  differently outside a UTF-8 locale, so that a command pasted in a C locale
  can name a different path or branch; the recommendation, not applied, amends
  [P]'s command form to write non-ASCII code points as their UTF-8 bytes,
  `\xHH`, and the overview's printed commands follow [P] either way (FR-045;
  EC-016). LQ-9 (its `plan.md:412`; lead ruling R-75 (a)): feature 004's
  `status` leaves a bare repository's registry entry out of its `worktrees`
  (its T117, `tasks.md:3275`; lead ruling R-66 (f)), and Brett Heap is asked
  whether CLN:478, by which the common directory is never probed as a worktree
  row, covers that, or whether it departs from CMD:196-197; the overview reads
  no `status` output, and C-68 decides its own report of that entry. Feature
  004's `inspect-cap` also counts only the registry entries that become rows,
  leaving out a bare repository's `bare` entry and a first record equal to
  `common_dir` with no main worktree (its contract, "Codes", `:400` there; lead
  ruling R-73 (d)), where Q14 A counts every registry entry (C-46, C-68): a
  recorded divergence in the cap count, which changes no suggestion, since
  `repository.root` is null in both layouts and such a row gets no clean
  suggestion (FR-031).
- **Open changes that modify change 2, none ratified** (lane
  openRepoProject-5): this feature neither waits for them nor realizes them, in
  every order, as each orders itself (Clarifications, C-71).
  - `add-project-clean-cache-disposal` (issue #24, draft PR #27) MODIFIES
    "Overview reuses the cleanup classifier and merge target" (requirement 5),
    appending to its equality clause two sentences that lane openRepoProject-4
    agreed at `9f30fb9` (the words "for the same working directory and refs"
    agreed at `4d5855a`, unchanged at `fe5b245`): a worktree that `project
    clean` classifies `merged-removable` because clean's cache enumeration
    proved every ignored path a listed cache is `ignored-local-files` in the
    overview, which collects no cache evidence, and the overview never
    classifies a worktree `merged-removable` where `project clean` classifies
    it otherwise for the same working directory and refs. It also names the
    ignored file of "Every protected classifier" as not a Python bytecode
    cache, and adds the scenario "Caches that only project clean proves
    disposable". The overview's collection and code are the same either way,
    and that change's own feature excludes the cache case from this feature's
    parity tests "once feature 005 has landed ... never in feature 005" (its
    proposal, Impact). Its block stays in its own feature in every order. If
    its realization merges first, a cache-only worktree is this feature's
    departure, on Brett Heap's word, from change 2's equality clause until
    #24's overview block is archived, after which that block records the same
    divergence as a lasting exception; in the other order the divergence is
    #24's own change. This feature's fixtures compared with `project clean`
    keep an ignored file such as `local.env` (FR-026, FR-049; Clarifications,
    C-71). Its pin stays at `fe5b245`. Re-checked on 2026-10-21 at `e07cc42`,
    its draft PR #27's head after its round B9 (lane openRepoProject-5's line
    map, which lane openRepoProject-2's lead checked by `cmp`), every range of
    it that lane openRepoProject-4 pins, those that this spec and
    `clarify-questions.md` cite among them, is byte-identical at new lines: its
    `proposal.md` :545-548, :569-572, :596-607 and :625-626 at :571-574,
    :595-598, :628-639 and :657-658; its `design.md` :592-595, :658-661 and
    D14's :1159-1165 at :650-653, :729-732 and :1239-1245; and its `tasks.md`
    3.2, :161-172, at :169-180. Its `project-overview` block is unchanged
    there, so a later re-pin moves only those line numbers. Re-checked again at
    `d4e960b`, its head after round B10 (`e07cc42..d4e960b`: `166016b` in its
    spec deltas, `b14ea45` in its design, `d4e960b` in its proposal and tasks),
    by lane openRepoProject-5's line map and this spec's own `cmp` of each
    range against `e07cc42` and against the pin: its `proposal.md` ranges sit
    at :601-604, :625-628, :668-679 and :697-698, its `design.md` ranges at
    :706-709, :785-788 and D14's :1316-1322, and the first line of its task 3.2
    at :178, each byte-identical. Its task 3.2, now :178-193, gains reader RF's
    M1 on lane openRepoProject-4's YES of 2026-10-21T16:13:14Z: "a re-base that
    changes the block's added text returns it to Brett Heap before the
    archive", and a second `diff -u`, of the block as committed at its ratified
    head against the re-copied block, worded as #25's task 2.4 (its B-54). Its
    `project-overview` block is still unchanged. Re-checked once more at
    `25f7333`, its head after round B12 (`f10c1be` in its spec deltas,
    `6d723ad` in its design, `25f7333` in its proposal and tasks), with round
    B11 at `f170079` (`9306a3a`, `71e84f9` and `f170079`) recorded on the way,
    by lane openRepoProject-5's two line maps and this spec's own `cmp` of each
    range against `d4e960b` and against the pin: its `proposal.md` ranges sit
    at :637-640, :661-664, :708-719 and :737-738 (:626-629, :650-653, :695-706
    and :724-725 at `f170079`), its `design.md` ranges at :806-809, :885-888
    and D14's :1454-1460 (:789-792, :868-871 and :1424-1430 at `f170079`), and
    its task 3.2 at :178-193 throughout, each byte-identical, the task as at
    `d4e960b` and its first line as at the pin. Its `project-overview` block is
    unchanged, the same blob from `fe5b245` to `25f7333`. Re-checked at
    `bced895`, its head after round B13 (`de47a4f` in its spec deltas,
    `2152816` in its design, `bced895` in its proposal and tasks), by lane
    openRepoProject-5's line map and this spec's own `cmp` of each range
    against `25f7333` and against the pin: its `proposal.md` ranges sit at
    :648-651, :672-675, :721-732 and :750-751, its `design.md` ranges at
    :822-825, :901-904 and D14's :1476-1482, and its task 3.2 at :178-193, each
    byte-identical, the task as at `25f7333` and its first line as at the pin.
    Its `project-overview` block is unchanged, the same blob from `fe5b245` to
    `bced895`. Re-checked again at `69cb7a1`, its head after round B14
    (`8ee0a5e` in its design, `69cb7a1` in its proposal and tasks), a round
    that edits no spec, its `specs/` tree being that of `bced895`, by lane
    openRepoProject-5's line map and this spec's own `cmp` of each range
    against `bced895` and against the pin: its `proposal.md` ranges sit at
    :651-654, :675-678, :724-735 and :753-754, its `design.md` ranges at
    :829-832, :908-911 and D14's :1487-1493, and its task 3.2 at :178-193, each
    byte-identical, the task as at `bced895` and its first line as at the pin;
    its `project-overview` block is the same blob. Re-checked again at
    `8d34525`, its head after round B15 (`87165d5` in its spec deltas,
    `237bdd6` in its design, `8d34525` in its proposal and tasks), which
    re-bases six more of its blocks on PR #19's text at `f0bf538`, so that
    eight of them follow #19 (its B-69), by lane openRepoProject-5's line map
    and this spec's own `cmp` of each range against `69cb7a1` and against the
    pin: its `proposal.md` ranges sit at :682-685, :706-709, :762-773 and
    :791-792, its `design.md` ranges at :887-890, :966-969 and D14's
    :1559-1565, and its task 3.2 at :185-200, each byte-identical, the task as
    at `69cb7a1` and its first line as at the pin; its `project-overview` block
    is the same blob, `a40458cb`. Re-checked again at `57bfc15`, its head after
    round B16 (`4d41a98` in its spec deltas, `a183b5f` in its design, `57bfc15`
    in its proposal and tasks), which re-bases five of its blocks, the retire,
    batch, bounds, reconcilable-result and revalidation blocks, on PR #19's
    round (h) at `b3228bb` (its B-84) and its classification block on round
    (g3) at `6bf9f77` (B-80), its preservation and narrow-guarantee blocks
    staying on `f0bf538`, on lane openRepoProject-2's YES to the set, by lane
    openRepoProject-5's line map and this spec's own `cmp` of each range
    against `8d34525` and against the pin: its `proposal.md` ranges sit at
    :733-736, :757-760, :828-840 and :858-859, its `design.md` ranges at
    :979-982, :1058-1061 and D14's :1655-1661, and its task 3.2 at :189-204,
    each byte-identical, the task as at `8d34525` and its first line as at the
    pin, but for the Archive order sentence in `proposal.md` :828-840 (the
    pin's :596-607), which on lane openRepoProject-4's YES (its B-77) now reads
    "or PR #19 has closed and the blocks written on PR #19's text have been
    rewritten" where it read "the two blocks", so that the range grows from 12
    lines to 13, its other lines byte-identical; its `project-overview` block
    is the same blob, `a40458cb`. None of those eight blocks is one that this
    spec reads, the overview taking #24's `project-overview` block alone
    (FR-026; C-71), so nothing that this spec states moves.
  - `add-project-overview-remote-merge-status` (issue #25, draft PR #29)
    MODIFIES "Overview bounds its work and reports what it omitted", "Overview
    prints a versioned JSON envelope" and "Overview is local and read-only"
    (requirements 3, 8 and 9), keeping each whole and adding a paragraph that
    applies only under `--remote`; it ADDS "Overview reports remote merge
    evidence on request", and MODIFIES [E] on draft PR #19's text. Its feature
    is created only after this feature merges and change 2 archives (its
    `tasks.md` 2.1 and 2.2). As its Open Question 3, addressed to lane
    openRepoProject-4, recommends, this feature reserves no flag, field or hook
    for it: `--remote` stays an invalid invocation here (FR-039, FR-042;
    Clarifications, C-71). Without `--remote` each of its blocks holds change
    2's text as written, so no requirement here changes. Its pin stays at
    `05a424a`. Re-checked on 2026-10-21 at `11a0ba2`, its draft PR #29's head
    after its round C13, every range that this spec and `clarify-questions.md`
    cite is byte-identical there: its `specs/` tree is that of `e11d755`, its
    overview spec's lines 1 to 410 equal the pin's, its `proposal.md` :334-345,
    :367-370 and :430-438 and its `tasks.md` :20-23 are unchanged, and so are
    its design D7, its "Dependencies and Sequencing" and its tasks 2.1 to 2.5.
    Re-checked again at `3965dfb`, its head after round C14
    (`11a0ba2..3965dfb`), whose `c0062f9` commits C-48's five spec items,
    reader RC's M1, M2, M3 and L1 and L4's spec part, with Isolation's "or a
    write to standard output fails" beside L4's "or a signal ends the run":
    every range that this spec and `clarify-questions.md` cite is
    byte-identical there, compared by `cmp`. Its overview spec's lines 1 to 155
    equal the pin's, and the root-path lines `:206-209`, `:229-230` and
    `:241-243` sit at `:209-212`, `:232-233` and `:244-246`; its
    `project-command` spec is as at `11a0ba2`; and its `proposal.md` :334-345,
    :367-370 and :430-438, its `tasks.md` :20-23, its design D7, its
    "Dependencies and Sequencing" and its tasks 2.1 to 2.5 are unchanged, as
    lane openRepoProject-5 reports for lane openRepoProject-4's five pinned
    ranges. Re-checked again at `86324ff`, its head after round C15
    (`3965dfb..86324ff`: `770e935` in its design, C-50's edits, D3's own
    refusal of an explicit port among them, and C-51's second diff in each
    re-read and re-base check of its Migration Plan; `86324ff` in its proposal
    and tasks), and at `2eeaec4` (`86324ff..2eeaec4`), which commits C-51's
    edits of its tasks 2.3 and 2.4: neither edits a spec, its `specs/` tree
    being that of `3965dfb`, and every range that this spec and
    `clarify-questions.md` cite is byte-identical at both, compared by `cmp`,
    its `proposal.md` :334-345, :367-370 and :430-438, its `tasks.md` :20-21
    (tasks 2.1 and 2.2) and :24 (task 2.5), its design D7 and its "Dependencies
    and Sequencing" included, except its tasks 2.3 and 2.4 (`tasks.md:22-23`),
    which at `2eeaec4` gain C-51's second `diff -u`, of each block as committed
    at its ratified head against the re-aligned or re-based block, and return
    any change to its ratified words to Brett Heap, and which still re-read and
    re-align its overview blocks (2.3) and re-base its block of [E] (2.4), as
    this spec cites them. Re-checked again at `6b5bf8f`, its head after round
    C16 (`2eeaec4..6b5bf8f`: `7bbc7e0` rewords its design D3's step 3, which
    still refuses an explicit port at that step, and `6b5bf8f` records C-52 in
    its proposal and tasks): no spec is edited, its `specs/` tree still being
    that of `3965dfb`, and every range that this spec and
    `clarify-questions.md` cite is byte-identical to `2eeaec4`'s, compared by
    `cmp`, its `proposal.md` :334-345, :367-370 and :430-438, its `tasks.md`
    :20-24, its design D7, its "Dependencies and Sequencing" and its Open
    Question 3 included; its task 1.3 now records that C-51's edits of 2.3 and
    2.4 are made on lane openRepoProject-4's YES, 2.3's follow-on for amendment
    A1 still waiting. Re-checked again at `2ab3743`, its head after round C17
    (`6b5bf8f..2ab3743`: `120b98c` changes one sha in its design's Citations
    paragraph, and `2ab3743` records C-53 and C-54 in its proposal and tasks):
    no spec is edited, its `specs/` tree still being that of `3965dfb`, and
    every range that this spec and `clarify-questions.md` cite is
    byte-identical to `6b5bf8f`'s, compared by `cmp`, its `proposal.md`
    :334-345, :367-370 and :430-438 (byte-identical to the pin's as well), its
    `tasks.md` :20-24, its design D7 and its Open Question 3 included; its
    "Dependencies and Sequencing" changes only the currency of one sentence,
    main `15504f1` for `e9d6711` and the date (`proposal.md:423-424`); and its
    task 1.3 still records that C-51's edits of 2.3 and 2.4 are made on lane
    openRepoProject-4's YES, 2.3's follow-on for amendment A1 still waiting,
    and now also records round C16's application of W22 (C-52). Re-checked
    again at `e1a9f84`, its head after round C18 (`2ab3743..e1a9f84`: `51e854b`
    in its spec, `78d6c84` and `b0d7c2a` in its design, and `e1a9f84` in its
    proposal and tasks), the first of its rounds since C14 to edit a spec:
    `51e854b` applies C-58 to its ADDED requirement alone, at its overview
    spec's :420-424, :488-491 and :623, text that only the LQ-15 item below
    cites, so that a relative `XDG_CONFIG_HOME` or `HOME` fails its `gh` lookup
    only in a run in which neither [E] as PR #19 amends it (LQ-15), starting no
    Git child, nor "Overview exits by completeness and severity" as A1 words it
    (FR-043), refusing with exit 2, stops it before any child starts, while a
    relative `GH_CONFIG_DIR` keeps #25's C-44 rule whole, no `gh` child
    starting in any of the three cases, as the LQ-15 item below records; no
    scenario is added or removed (36 and 10), and its `project-command` spec is
    the blob of `11a0ba2`. Every other range that this spec and
    `clarify-questions.md` cite is byte-identical to `2ab3743`'s, compared by
    `cmp`: its overview spec's lines 1 to 419, which hold every other line of
    it that they cite, the pin's lines 1 to 155 and the root-path lines at
    `:209-212`, `:232-233` and `:244-246` among them, and its scenario "Expiry
    cancels queued and in-flight requests", now at :644-650; its `proposal.md`
    :334-345, :367-370 and :430-438 (byte-identical to the pin's as well) and
    :423-424, its "Dependencies and Sequencing", its Open Questions and its
    `tasks.md` :20-24; and its design D7, now at :954-989, and D5's residual,
    which EC-022 cites, now at :574-601, D5 gaining after it C-58's paragraph
    on the two texts that stop a run with a relative `HOME` or
    `XDG_CONFIG_HOME` before any child starts (:646-670). Its task 1.3 still
    records that C-51's edits of 2.3 and 2.4 are made on lane
    openRepoProject-4's YES, 2.3's follow-on for amendment A1 still waiting,
    and now records rounds C17 and C18 (C-56, C-57, C-58 and C-61), reader RH's
    L4, the wording of task 2.4 and A1's note that task 2.3's condition is met
    being drafted and held for lane openRepoProject-4's YES and written nowhere
    in that change. Re-checked again at `9a3f684`, its head after round C19
    (`d38b282` in its design, `9a3f684` in its proposal and tasks), and at
    `a6080a7`, its head after round C20 (`e053ad6` in its spec, `6527f73` in
    its design, `a6080a7` in its proposal and tasks), each by `cmp` against
    `e1a9f84`. Round C19 edits no spec and commits task 2.4 as held on lane
    openRepoProject-4's YES (C-62, reader RH's L4), so that `tasks.md:23` now
    re-reads its block of [E] against change 1's archived block and re-bases it
    there if that block moved past PR #19's text at `c462d87`, the design's
    Migration Plan step 4 taking the same clause; its pinned lines 20 to 23 are
    now as lane openRepoProject-5 holds them (sha256 `2e177de7a91d6447...`),
    :20-22 and :24 unchanged. Round C20 applies C-66 to its ADDED requirement
    alone (`e053ad6`, sha256 `6fda0ae8c5c60dab...`, 36 and 10 scenarios), at
    lines that the LQ-15 item below now cites in that form, on lane
    openRepoProject-4's YES to lane openRepoProject-3's W61: the Requests
    paragraph pairs each text with its own verb, [E] "by barring every Git
    child and inspecting no repository" and "Overview exits by completeness and
    severity" "by refusing the run", neither of which "stops it before any
    child starts" (:420-426), and the Results paragraph reads "not stopped"
    (:490), the scenario's AND still saying "refuses the run" of both (:624);
    every line after :425 moves down 1, the scenario "Expiry cancels queued and
    in-flight requests" to :645-651. Every other range that this spec and
    `clarify-questions.md` cite is byte-identical at its lines: its overview
    spec's lines 1 to 419, its `proposal.md` :334-345, :367-370, :430-438 and
    :423-424, its "Dependencies and Sequencing" and Open Questions (by sha256),
    and its design's D5 residual at :574-601 and D7 at :954-989, while D5's
    C-58 paragraph (:646), D11, Risks and `proposal.md:892-893` change outside
    them. Re-checked again at `8276945`, its head after round C21 (`1cd73fb` in
    its spec, `266a30f` in its design, `8276945` in its proposal and tasks),
    and at `a529310`, its head after round C22 (`bbe8d53` in its design,
    `a529310` in its proposal and tasks), each by `cmp` against `a6080a7`:
    `1cd73fb` changes only "refuses" to "stops" in that AND (:624; C-67 (a), on
    lane openRepoProject-4's YES), the spec's sha256 now `d42139fb5e6c2695...`,
    36 and 10 scenarios in 661 lines; round C22 edits no spec, its design
    changing at :653-655 (C-68) and D7 staying at :954-989; and every other
    pinned and cited range is byte-identical at its lines: its overview spec's
    lines 1 to 623 and 625 to 661, the scenario at :645-651 among them, its
    `proposal.md` :334-345, :367-370, :430-438 and :423-424, its `tasks.md`
    :20-24 (sha256 of :20-23 `2e177de7a91d6447...`), D5's residual at :574-601,
    D7, and its "Dependencies and Sequencing" and Open Questions (by sha256).
  - `add-project-clean-branch-retirement` (issue #23, draft PR #26) leaves
    `project-overview` untouched. It MODIFIES [E], [G]'s two requirements
    and other `project-clean` requirements for `clean --retire-branches`
    alone, moving no gate, refusal code or shared constant that FR-032 to
    FR-036 read; no suggestion carries its flag (FR-031).
  - The answers that amend change 2 or [E] (Q6 A, Q7 A, Q8 D, Q9 B, Q12 A and
    Q13 A; Clarifications, C-60 to C-63, C-66 and C-67) rewrite text that these
    changes carry in MODIFIED blocks, among them #24's block of requirement 5,
    where Q7 A adds a paragraph after its equality clause (after POD:386), and
    #25's blocks of requirements 3, 8 and 9, which Q6 A, Q8 D, Q9 B and Q12 A
    amend (A1's own map at `e4a30fc`). Q13 A adds a sentence to requirement 1
    (after POD:16), which no MODIFIED block carries, through which POD:217-222,
    :303-306, :610-611 and :622-624, the root object's `path`, read, lines that
    #25 carries unchanged at its `spec.md:102-107`, `:206-209`, `:229-230` and
    `:241-243`, all at `05a424a`. #25 re-aligns its blocks to such an amendment
    (its proposal, "Dependencies and Sequencing"; its `tasks.md` 2.3 and 2.4).
    Q16 B amends change 2's design D1 and clarifications N1 (Clarifications,
    C-70), which reaches #25 as well: if amendment A1 comes before change 2
    archives, #25's task 2.3 re-read picks it up, the spawning sentence of
    #25's design D7 and its scenario "Expiry cancels queued and in-flight
    requests" included (its proposal, "Dependencies and Sequencing"; its
    `tasks.md` 2.3). Before its `/opsx:archive`, #24 re-reads its block of
    requirement 5 against the text of that requirement on `main` and re-copies
    the block from that text, keeping every amendment along with its own
    additions, so that Q7 A's amendment of requirement 5 is not dropped by its
    archive (its proposal, "Dependencies and Sequencing"; its `tasks.md` 3.2).
- **Amendments and departures from Brett Heap's answers of 2026-10-21**
  (Clarifications, C-55 to C-71). This spec builds the behaviour the answers
  give; each departs from the text named here and is carried as stated.
  - Amendment A1, `amend-project-overview-clarify-answers`, lane
    openRepoProject-4's governed change, drafted as draft PR #34 and ratified
    by Brett Heap on 2026-10-22 in his words "ratify 34" (Clarifications,
    "Session 2026-10-21, Brett Heap's answers"), its ratification recorded in
    its task 1.7 at `e4a30fc` (its `tasks.md:17`), amends change 2
    (`openspec/changes/add-project-overview/`) in place, landing with PR #34
    under its ordering rule (below). Its own map at `e4a30fc` (its
    `proposal.md`, "Amendment A1", :1073-1510, which cites change 2's lines at
    `961c405`, as this spec does) gives these sites: for Q3 B, Impact, a new
    `.github/workflows/tests.yml` bullet after the tests bullet
    (proposal.md:441-449), the option's second branch (C-57); for Q6 A,
    requirement 3 (POD:180-181, :233-234) and requirement 8's error object
    (POD:646-648), with the packet's definition of `limit` (DI:824-825) for the
    deadline error (C-60); for Q7 A, requirement 5, a new paragraph after its
    equality clause (after POD:386), leaving POD:378-386 as ratified, and
    design D6's scan-error order (design.md:410-412) and D8's realpath task
    (design.md:470-471), with DI:842-843's exceptions and DI:778's null rule
    for `current` (C-61); for Q8 D, requirement 4 (POD:337-338, and a table of
    fixed texts after POD:347), requirement 8 (POD:675), design D1
    (design.md:99-101) and clarifications N1 (clarifications.md:35-36 and
    :46-47), departing from the packet's DI:544-545, with the human report's
    path fill in design D10 (design.md:519-520 and :526-527, and a paragraph
    after :533) and requirement 12 (POD:812-813) (C-62; FR-045); for Q9 B,
    requirement 3 (POD:212-215), where "seventeen names" becomes a citation of
    [E]'s list, requirement 9 (after POD:717), design D13 (design.md:661) and
    Risks (after design.md:726), and proposal.md:231-232, :477 and :1000,
    narrowing the packet's DI:307-308 for the overview's Git children (C-63);
    for Q11 A, requirement 2, a new paragraph after POD:87, and the `refused`
    row of requirement 4's new table (C-65); for Q12 A, requirement 8
    (POD:675-676, and a new paragraph after POD:679), departing from the
    packet's DI:1086-1089 (C-66); for Q13 A, requirement 1, a new sentence
    after POD:16, through which POD:217-222, :303-306, :610-611 and :622-624
    read, with DI:842-843 (C-67); for Q15 A, requirement 11 (POD:778-779, and
    new sentences after POD:781) and design D1 (design.md:110-111, in the same
    words, a new paragraph for the raising span, and the "Recorded" paragraph,
    design.md:121-122), departing from the packet's DI:1094-1096 (C-69); and
    for Q16 B, design D1's spawning paragraph (design.md:115-119) and
    clarifications N1 (clarifications.md:42-44 and :45-47) (C-70). Q4 D and
    Q17 A amend no text there, and Q1 A, Q2 A, Q5 A, Q10 A and Q14 A are not
    carried, since each changes only this spec. This list replaces this spec's
    forecast of A1's sites (lane openRepoProject-3's W6 read, L1, and its W7
    read of A1, check 4, item 3). A1 at `e4a30fc` records the two packet lines
    that lane openRepoProject-3's W7 read found undeclared, DI:778 and
    DI:307-308 (W7, M2 and M3). Four items of A1's own follow PR #19, not
    Q1-Q17, on Brett Heap's "yes to all six recommendations, LQ-10 to LQ-15"
    (its `proposal.md:1261-1452`), each declared for his review and ratified
    with A1: `relative-config-path` (LQ-15; FR-043), departing from
    DI:1086-1089, its fallback `refused` departing from nothing;
    `operation-in-progress` and `worktree-only-commits` as exclusions only the
    batch applies (LQ-14 and LQ-13; FR-032), departing from OV:110-113 and
    DI:690-692; LQ-11's counted reads and the change-2 sites that read against
    them (FR-007, FR-013, FR-019, FR-020), departing from DI:506-509 and
    DI:1193-1201 and, by the collector table's two exceptions, from DI:535 and,
    by requirement 2's new case for a check that cannot be completed, from
    DI:251-261; and LQ-10's stat pins, a restatement of [E]'s four status pins
    where change 2 quoted two (FR-016), departing from nothing, since no packet
    line quotes the two older pins (DI:396, DI:1181). Each lands only with or
    after PR #19's ratification of the commits it follows, and is re-aligned
    before A1 is ratified if one of those commits changes first, and, if A1 is
    ratified first, is re-aligned for Brett Heap's review before PR #34 merges;
    PR #34 does not merge before that ratification, and should Brett Heap want
    it sooner, the four items move to a later amendment of change 2 and A1
    lands without them, as A1 words it (its :1278-1284 and :1498-1500). Brett
    Heap ratified A1 first, with that rule: PR #34 stays a draft until #19's
    ratification of those commits, an item whose commits change before then is
    re-aligned for his review before PR #34 merges, and the four items move to
    a later amendment only on his word, which is not given (Change-1
    amendments, below). FR-011, FR-022, FR-039, FR-044, FR-045, FR-050, SC-009,
    SC-010 and SC-011 were folded here ahead of their carrier, A1, on Brett
    Heap's answers. A1 being ratified, the gate that nothing is planned or
    built from them before its ratification is met, and each is re-read against
    A1's text, now ratified, as A1 records (its `proposal.md:1509-1510` at
    `e4a30fc`, which names six of them: FR-011, FR-022, FR-039, FR-044, SC-009
    and SC-011). That the re-read comes before the plan builds from them, a
    gate beside A1's task 1.7, and that it takes FR-045, FR-050 and SC-010
    beside those six, are this spec's own; the re-read is done for all nine
    (the lane openRepoProject-4 lead's re-read against A1's ratified text, its
    first pass applied at `bbf1f7c` and its second pass's N1, for SC-010, at
    `49d66a8`; lane openRepoProject-3's W55 L2 and W58 L1); the plan itself
    still waits for Brett Heap's own word for it, after feature 004's merge
    (C-56; A1's task 1.7). The same holds for what follows A1's four items of
    its own, which also wait for #19's ratification of the commits they follow:
    FR-007's LQ-11 parity with FR-013, FR-019, FR-020 and US1 s3; FR-032's
    batch-only gates with SC-004 and EC-007; FR-043's code; and FR-016's four
    status pins. One point A1 leaves to Brett Heap, as this spec does, with no
    behaviour written (its proposal, "Open point", `proposal.md:1479-1486` at
    `e4a30fc`): Q7 A is silent on FR-026's parity with `project clean` run from
    the same working directory when that directory's realpath cannot be
    established, and at `2cf34d3` feature 004 gives every present row
    `inspection-error` there (its `project:2960-2962`, :2887-2888 and :2081),
    wider than the two classes Q7 A converts (C-61; lane openRepoProject-3's
    fidelity read of `c54d393`, M1).
  - Change 1's [E], for Q9 B: lane openRepoProject-2 agreed on 2026-10-21 that
    its draft PR #19, which already edits [E]'s Environment paragraph
    (CMD:98-122), carries the trace pins and the trace-variable scrub names
    (C-63) as a commit of its own, and that feature 004's draft (#33) builds
    the wider scrub and the pins. That commit is `423a532`, on PR #19's branch
    `change/amend-clean-all-safe-push-pins`: [E]'s scrub there lists thirty-one
    names, every Git child, the push child included, has `GIT_TRACE2`,
    `GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF` set to `0` (its
    `specs/project-command/spec.md:98-124`), and the scenario "Trace targets
    are never written" (:272) brings that delta to 19 scenarios. The overview
    follows [E] as amended there (FR-016); feature 004 at `2cf34d3` still
    removes the seventeen names, and its draft #33 builds the thirty-one and
    the pins (lead ruling R-99 (b) and (d)). The answer's fallback, a narrower
    scrub built by feature 004 and the wider one following as a change-1
    amendment, applies only if feature 004 merges without it.
  - Departures on Brett Heap's word: Q4 D's `AGENTS.md` sentence (FR-051;
    C-58), from change 2's Impact (proposal, Impact), where Q3 B's floor-job
    selection is carried by A1 instead (FR-050; C-57); and, only if #24's
    realization merges first, Q17 A's cache-only worktree, from change 2's
    equality clause (POD:381-386, on DI:620-624) until #24's overview block is
    archived (FR-026; C-71). FR-051 waits for Brett Heap's word on feature
    004's T123 departure (its lead ruling R-32); if he declines it, a separate
    small OpenSpec change after feature 005 carries agent guidance on the
    overview and the batch apply instead.
- **Change-1 amendments from Brett Heap's answers to lane openRepoProject-2's
  LQ-10 to LQ-15**: Brett Heap's "yes to all six recommendations, LQ-10 to
  LQ-15" (2026-10-21, lane openRepoProject-3's session), NOTED in that lane's
  log at 12:33:41Z, which lane openRepoProject-2 records as its ruling R-102.
  That lane's draft PR #19 carries every change-1 amendment, one commit per
  ruling (R-102 (c) 1); LQ-15, LQ-10, LQ-12, LQ-11, LQ-13 and LQ-14 are there
  as `cc000ea`, `ea697ba`, `eae1a79`, `addd346`, `93de4bb` and `43f7107`, with
  lane openRepoProject-3's W8 read of LQ-15 applied as `9fb22fa`, and lane
  openRepoProject-2's rulings R-124, R-125 and R-126 on that lane's later reads
  as `2b86a5f`, `93f3194` and `1ebdd90`, drafts cited as pending #19's
  ratification. The overview follows [E] as amended, as for Q9 B. Where an
  amendment reaches change 2's own text, amendment A1 at `e4a30fc` carries it
  as an item of its own, four in all, each following the commits its heading
  names (its `proposal.md:1261-1452`): `relative-config-path` (LQ-15),
  `cc000ea` and `9fb22fa`; the gates (LQ-14 and LQ-13), `43f7107`, `1ebdd90`,
  `93de4bb`, `2b86a5f` and `9267303`; the redirected work tree (LQ-11),
  `addd346` and `93f3194`; and the stat pins (LQ-10), a restatement, `ea697ba`,
  with its pointer at `93f3194`. Each such item lands only with or after #19's
  ratification of the commits it follows, and is re-aligned before A1 is
  ratified if one of those commits changes first, and, if A1 is ratified first,
  is re-aligned for Brett Heap's review before PR #34 merges (its :1272-1281).
  Brett Heap ratified A1 first (Amendment A1, above), so the second branch
  applies. R-124, R-125 and R-126 landed by `1ebdd90`. #19's round (a),
  `6f2cb54` (lane openRepoProject-2's rulings R-146 and R-147), follows it, and
  nothing that this spec cites from #19 at `1ebdd90` changes there but one word
  of the gate block, which the LQ-13 bullet already reads. Re-checked by
  script, as lane openRepoProject-3's W25 read also found: its
  `project-command` spec is unchanged; its `project-clean` spec's gate block
  (:609-690 at `1ebdd90`, :659-740 there) differs by one word, LQ-13's "from no
  object that its branch's reflog names" becoming "from no non-zero object that
  its branch's reflog names", and the three scenarios that the bullet cites
  keep their text, at :837, :860 and :875 there; and its review-safety spec
  keeps its lines 1 to 236, adding the scenario "A check that fails at
  revalidation" after them. #19's round (b), `4485678` (lane
  openRepoProject-3's W26 read and lane openRepoProject-2's R-171) and
  `a664799` (R-178), follows, and nothing that this spec cites changes there
  but the review-safety rule, which keeps the clause the LQ-13 bullet cites and
  gains R-171's rule for a Git child that does not finish with a value (its
  :103-104 and :117-127 at `a664799`). Re-checked by script against `6f2cb54`:
  its `project-command` spec is unchanged, and so is [G]'s "Clean bounds its
  Git work and reports omitted work"; its `project-clean` spec's gate block and
  the three scenarios keep their text, at :664-745, :842, :865 and :880 there;
  the two review-safety scenarios that the bullet cites keep theirs, at :226
  and :238; and its design keeps the Risk that EC-022 cites, at :1494-1499.
  R-171 governs `project clean`'s revalidation only. The overview has no
  revalidation, so no requirement of this spec moves, and the LQ-13 bullet's
  revalidation sentence stays pinned at `1ebdd90`. R-178 names LQ-20, open for
  Brett Heap (its `proposal.md:1273-1281` at `a664799`). This spec re-aligns
  only if #19 comes to bound [E]'s plan-time work-tree probe (its
  `specs/project-command/spec.md:221-227`, the same from `93f3194` to
  `a664799`) to the selected targets in [E] itself, rather than in `project
  clean`'s plan alone, or, under LQ-20's step (d) at `2e819ad` (its
  `proposal.md:1290-1293` and its design D14's `design.md:953-959`; round (c),
  below) and at `9267303` (its `proposal.md:1311-1316`; round (d), below),
  comes to lower the shared caps that this spec's Dependencies state and that
  US4 s3 and s4 assume: the 128-row and 256-row caps and the 16-target limit of
  [G]'s "Clean bounds its Git work and reports omitted work" (its
  `specs/project-clean/spec.md:984-987` at `2e819ad`), which US4 s3 and s4 take
  from change 2's ratified POD:579 and :584, lines that amendment A1 at
  `e4a30fc` keeps word for word at its `specs/project-overview/spec.md:651` and
  :656. The units that follow that probe are FR-007, FR-013's toplevel realpath
  task, FR-019, FR-020 and FR-049, and US1 s3 counts no such probe, its
  repository not setting `extensions.worktreeConfig`; the ordering rule above
  covers such a re-alignment. #19's round (c), `2e819ad` (lane
  openRepoProject-3's W31 read; lane openRepoProject-2's R-187 and R-190),
  follows, and settles W31 M-1, which set the rule's :113-114 against its
  :118-120 at `a664799` on a read that the deadline cuts at revalidation: the
  rule's clause now reads "runs past its own budget" and leaves a read that the
  work deadline cuts to R-171's rule (its :113-118 and :124-128 there), and the
  scenario "A work-tree probe at revalidation" is added (:260-280), the LQ-13
  bullet, which names only a failure and a run past the budget, still reading
  as the clause has it. Re-checked by script against `a664799`: its
  `project-command` spec is unchanged, its :221-227 included; [G]'s "Clean
  bounds its Git work and reports omitted work" changes only its re-run
  sentence for deferred targets (:1004-1014 there), which this spec cites only
  as change 1 ratified it (C-45's CLN:807-811), for a per-run, per-repository
  limit that the change keeps, SC-004 naming `deferred-target-cap` only as a
  preview's outcome; the gate block and the three scenarios keep their text and
  lines; the two review-safety scenarios keep theirs, at :227 and :239; and the
  Risk that EC-022 cites keeps its text, at :1557-1562. LQ-20, still open for
  Brett Heap, now takes as its first step measuring the two probes or deciding
  the basis (its `proposal.md:1273-1294` at `2e819ad`), and the re-align
  condition above now has two arms, #19 bounding the probe in [E] and LQ-20's
  step (d) lowering the caps (lane openRepoProject-3's W34 MEDIUM-1). #19's
  round (d), `9267303` (lane openRepoProject-3's W36 read and W32 L1; lane
  openRepoProject-2's R-207 and R-208), follows. Re-checked by script against
  `2e819ad`: its `project-command` spec is unchanged (`git diff --quiet`), its
  :221-227 included; its `project-clean` spec's gate block changes two
  sentences, a listing of `operation-in-progress` or a read of
  `worktree-only-commits` not finished within the filesystem budget, the
  deadline not being the limit, now recording `probe-timeout` and making the
  row `inspection-error` where it left the row unprobed (:719-722 and :741-746
  there), which FR-032, SC-004 and the LQ-13 bullet now follow, as A1 at
  `e4a30fc` does (its `proposal.md:1324-1339`); the rest of the gate block, now
  :664-746, and the three scenarios keep their text, at :843, :866 and :881;
  the caps and the re-run sentence of "Clean bounds its Git work and reports
  omitted work" keep theirs, at :985-988 and :1005-1015; the two review-safety
  scenarios keep theirs, at :232 and :244, and "A work-tree probe at
  revalidation" its own, at :268-288; and the Risk that EC-022 cites keeps its
  text, at :1586-1591. R-208 rewrites the review-safety rule for every
  filesystem call at revalidation (:113-133 there), which governs revalidation
  only, so no requirement of this spec moves, and the LQ-13 bullet's
  revalidation sentence, naming a failure and a run past the budget, still
  reads as the rule has it (:115-122 there). R-207 costs LQ-20's options on
  every basis (its `proposal.md:1277-1318` there): option (c), now a longer
  work deadline for `project clean`, moves no value this spec states, the
  overview's 60 s deadline being its own (FR-011; POD:167-168); option (b),
  bounding the plan-time work-tree probe, is the condition's first arm where
  #19 makes it in [E] itself; and step (d), lowering the caps (:1311-1316
  there), now states in the proposal that it lowers the report's row cap, the
  256-row cap that this spec's Dependencies state, that US4 s4 assumes and that
  the condition's second arm names, as design D14 already gave it at `2e819ad`
  (its `design.md:953-959`; POD:584; A1's :656 at `e4a30fc`; lane
  openRepoProject-3's W39 LOW-1 and W43 LOW-1). #19's round (e), `f0bf538`
  (lane openRepoProject-3's W38 read of round (d); lane openRepoProject-2's
  R-213 and R-216), follows. Re-checked by script against `9267303`: its
  `project-command` spec is unchanged (`git diff --quiet`), its :221-227
  included; its `project-clean` spec's gate block gains one clause, the
  `worktree-only-commits` outcome rule now split as the branch reflog's is
  "except that a read not finished within the filesystem budget makes the row
  `inspection-error` here" (:735-737 there), which keeps the outcome that
  FR-032 states and leaves the branch reflog's own unfinished read unprobed, as
  change 2's requirement 7 has it for the overview's gate (POD:521-524;
  FR-033); the lines after :736 move down 2, so that the rest of the gate
  block, now :664-748, keeps its text, :719-722 at the same lines and :741-746
  at :743-748, and so do the three scenarios, at :845, :868 and :883, and the
  caps and the re-run sentence of "Clean bounds", at :987-990 and :1007-1017;
  the review-safety rule capitalizes its "SHALL NOT" and makes an
  administrative directory that the `operation-in-progress` listing finds
  absent at revalidation a registration difference, `identity-changed`
  (:122-126 there), which governs revalidation only, so no requirement of this
  spec moves, and the LQ-13 bullet's revalidation sentence, naming a failure
  and a run past the budget, still holds; the two review-safety scenarios keep
  their text, at :234 and :246, and "A work-tree probe at revalidation" its
  own, at :270-290; and the Risk that EC-022 cites keeps its text, at
  :1592-1597. LQ-20's option (c) now also moves `project clean`'s ratified 60 s
  invocation deadline (its `proposal.md:1277-1324` there), which this spec does
  not state, and its step (d) keeps its text, at :1317-1322. #19's round (f),
  `662be89` (Brett Heap's ruling on LQ-20, in his words to lane
  openRepoProject-2, "LQ-20: go with (i), measure first"; lane
  openRepoProject-3's W42 read of round (e) and W53 departure ledger; lane
  openRepoProject-2's R-236 and R-245), follows, and edits no delta: its
  `specs/` tree is unchanged from `f0bf538` (`git diff --quiet`), so that every
  line this spec cites from its three specs at `f0bf538` holds at `662be89`,
  and its round record says that no requirement changes (its
  `proposal.md:1725-1755`). Its design D7 and D22's Revalidation bullet now
  carry the clause that the review-safety rule already had at `f0bf538`
  (:122-126), an administrative directory that the `operation-in-progress`
  listing finds absent being a registration difference, `identity-changed` (its
  `design.md:495-497` and :1529-1532; lane openRepoProject-3's W38 L-4 and W42
  L-2): round (f) brings the design into line with the delta, and no
  requirement of this spec moves; the Risk that EC-022 cites keeps its text, at
  :1625-1630. LQ-20 is resolved by measurement (its `proposal.md:1305-1318`,
  its design D14 at `design.md:956-987` and its task 2.1 at
  `tasks.md:145-155`): Brett Heap chose its step (i), and on task 2.1's
  protocol LQ-11's work-tree probe measured 5.8 ms warm, 8.7 ms with the
  margin, and LQ-13's `rev-list` 106.9 ms warm, 160.3 ms with the margin, so
  that at 128 rows and 16 targets where `extensions.worktreeConfig` is true all
  16 removals fit and the caps still stand (its `design.md:1712-1716`); none of
  options (a) to (d) is taken, each now so marked, and the deltas stand as
  written (its `proposal.md:1365-1366`). Round (f) therefore takes neither arm
  of the re-align condition above: #19 does not bound [E]'s plan-time work-tree
  probe, its :221-227 unchanged and option (b) not taken (:1344-1348), and step
  (d), lowering the caps, is not taken, its text kept at :1358-1363, its first
  line now adding "not taken"; both stay untaken pending #19's ratification,
  and nothing this spec states moves. Its two new departures (its
  `proposal.md:1087-1109`), that a revalidation read or child that the work
  deadline cuts counts as no difference and that push refuses a wider set of
  upstream mappings, each recorded for text its deltas already held, and its
  push-child exception, which now names the packet lines its process group
  departs from (:1164-1175), govern `Cleanup revalidates destructive actions`,
  `Clean can explicitly push safe feature branches` and the push child, none of
  which the overview runs: none of them changes what reaches the overview
  through [E] or [G]. #19's round (g), `4f1c0e0` (lane openRepoProject-3's W52
  read of next steps that Git refuses; lane openRepoProject-2's R-248),
  follows, and edits its `project-clean` spec, its `project-command` and
  review-safety specs unchanged (`git diff --quiet`). Re-checked by script
  against `662be89`: its four hunks there, :170-172, :336-341, :360-361 and
  :785-786 (:170-174, :338-347, :366-368 and :792-794 at `4f1c0e0`), touch no
  line that this spec cites from it, so that each cite keeps its text. The
  lines before :170 keep their numbers, among them the refusal paragraph at
  :11-24 and the scenario "A relative configuration path", at :112; the gate
  block moves down 7, to :671-755, its gate order (:664-671 at `662be89`) at
  :671-678, the clauses that FR-032 and SC-004 cite at :726-729 and :750-755,
  and round (e)'s clause at :742-744; the three scenarios move down 8, to :853,
  :876 and :891, and so do the caps and the re-run sentence of "Clean bounds",
  to :995-998 and :1015-1025; [E]'s :221-227 and the review-safety rule
  (:122-126) and scenarios (:234, :246 and :270-290) keep their lines; and the
  Risk that EC-022 cites keeps its text, at its `design.md:1649-1654`. The
  records above stay as written, each at the commit it names. Round (g)'s spec
  edits are three: `Clean classifies preservation and cleanup actions` gains,
  for a locked worktree, the recovery text "inspect, unlock it, then `git
  worktree remove --force <path>` by hand" (:170-174 at `4f1c0e0`; F-2, which
  Brett Heap's ruling at 15:24Z, "F-2: yes", settles in round (h), below;
  design D4, :254-255, and D18, :1224-1228); `Clean can explicitly retire
  verified worktrees` refuses a branch that the main worktree holds with a
  message that names detaching HEAD there or checking out the merge target
  there, then retrying (:338-347, which the scenario "Branch deletion refuses a
  branch it may not delete" quotes at :366-368; F-5; D18, :1234-1242); and the
  plan-blocking remedy of `Clean previews and applies a batch of eligible
  worktree removals in one repository` names "unsetting `core.worktree` and
  `core.bare` in the repository's `config` or in a worktree's
  `config.worktree`" (:792-794; F-3), as D18's `registration-mismatch` next
  step does (:1210-1214). D18's strings also change in the design alone:
  `operation-in-progress`'s next step adds, for a marker left with nothing in
  progress, "or, where Git says none is in progress, its --quit" (:1200-1207;
  F-9), with its Risk (:1617-1624); `contains-submodule`'s becomes "review,
  then git worktree remove --force yourself" (:1198-1199; F-8); and the next
  steps of `unstarted-branch` and `reflog-unavailable`, gate 7, ahead of
  `contains-submodule`, gain ", with --force where Git refuses it for a
  submodule" (F-7, R-248; D18, `design.md:1191-1197`, the Migration Plan,
  :1756-1763, and `proposal.md:86-87` and :92-93, all at `4f1c0e0`), a clause
  that lane openRepoProject-2's R-252 shortens in #19's round (g2), `3dcd2d8`.
  None of them reaches the overview through [E] or [G]: the overview starts no
  removal and no branch deletion, names no plan-blocking remedy and makes no
  `operation-in-progress` listing, and this spec quotes none of the texts that
  F-3 and F-9 edit, which came in at `93f3194` and `43f7107`, as A1 quotes none
  of them; so no requirement of this spec moves, and A1's four LQ items need no
  change. F-7's two remedies are change 2's as well: A1 at `e4a30fc` mirrors
  them at its `specs/project-overview/spec.md:629-630`, :666 and :674, its
  `proposal.md:311-314` and its design D12 (:646-648), and this spec's US4 s5
  and s6 quote them. Their re-alignment is held for Brett Heap with #19's
  ratification, A1's six sites following #19's ratified wording for his review,
  the choice being #19's strings as ratified, which lane openRepoProject-4
  recommends, or change 2's present texts as a departure that D12 records;
  until then this spec's texts follow A1 as ratified (FR-035). #19's rounds
  (g2), `3dcd2d8` (lane openRepoProject-2's R-252), and (g3), `6bf9f77` (lane
  openRepoProject-3's W59 read of rounds (f) and (g); lane openRepoProject-2's
  R-253), follow. Round (g2) edits no spec and shortens F-7's clause, so that
  each remedy ends "yourself (--force if it holds a submodule)", at #19's six
  sites (its `design.md:1193`, :1195, :1757 and :1762 and `proposal.md:86` and
  :91-92 at `3dcd2d8`). Round (g3) adds one AND to each of two scenarios, no
  scenario or requirement being added: "Only tracked-file deletions" in its
  `project-clean` spec pins F-2's locked recovery text (:211-212 at `6bf9f77`),
  as Brett Heap later ruled (round (h), below), and "A linked worktree whose
  work tree is redirected" in its `project-command` spec pins the remedy that
  the preview's `registration-mismatch` group names, unsetting `core.worktree`
  and `core.bare` in the repository's `config` or in a worktree's
  `config.worktree` (:314). Re-checked by script against `4f1c0e0`, its
  `project-command` spec changing for the first time since `93f3194`: there,
  every line before :314 keeps its number and text, among them the refusal
  codes at :8-17, the "Configuration paths" test at :116-129 with :124-125, the
  trace list and pins at :131-157, the status pins at :158-165, the
  registration lines at :204-214 and :232-240 with :211-213, [E]'s :221-227 and
  the redirected scenario's header at :311, and the scenarios after :314 move
  down 1, "A commondir that names another repository" to :319, "A relative
  configuration path in status, doctor and update" to :324, "The pinned status
  configuration" to :335, "An edit that keeps its size and restores its mtime"
  to :339 and "Trace targets are never written" to :356; in its `project-clean`
  spec every line up to :210 keeps its number, the refusal paragraph at :11-24,
  `project clean`'s refusal at :15-16, the scenario "A relative configuration
  path" at :112 and F-2's sentence, ruled in round (h), at :170-174 among them,
  and the rest move down 2, the gate block to :673-757, its gate order at
  :673-680, the clauses that FR-032 and SC-004 cite at :728-731 and :752-757
  and round (e)'s clause at :744-746, the three scenarios to :855, :878 and
  :893, the caps and the re-run sentence to :997-1000 and :1017-1027, and round
  (g)'s F-5 and F-3 to :340-349, :368-370 and :794-796, each keeping its text;
  and its review-safety spec is unchanged. Round (g3)'s design edits, at
  `6bf9f77`: D18's non-drain line ends "(--force for any that holds a
  submodule)" (its `design.md:1183-1190`; G-4); `operation-in-progress`'s next
  step ends "or, where --abort fails for a marker with nothing in progress, its
  --quit" (:1206-1215, and its Risk at :1628-1636; G-5); D4 and D18 say that
  F-2's text replaces the ratified recovery text of `0050f3e` for a locked row
  and waits on Brett Heap's word with F-1, the ceiling's recovery text
  (:257-261 and :1236-1239; G-1), a word that he gave at 15:24Z (round (h),
  below); and its proposal declares F-5 a departure from `BA:424-425`
  (`proposal.md:1113-1127`; G-2). None of them reaches the overview through [E]
  or [G]: the redirected scenario's AND states what `project clean`'s preview
  lists, not the evidence model's rule, which keeps its text, so that FR-007's
  LQ-11 reading and A1's, which follow `addd346` and `93f3194`, hold; and the
  overview shows no partial-removal note, no non-drain line and none of
  `project clean`'s next steps, its own `registration-mismatch` finding naming
  no command. No requirement of this spec moves. #19's round (h), `b3228bb`
  (`e322f52`, `324192f`, `fc95766` and `b3228bb`; lane openRepoProject-2's
  R-258 to R-263, with lane openRepoProject-5's RI-3 and O-1 and lane
  openRepoProject-3's W64), follows, and carries Brett Heap's ruling of
  2026-10-22 at 15:24Z, in his words to lane openRepoProject-2, "F-2: yes; F-1:
  prune-then-delete; O-1: deadline-exceeded" (R-263), which its proposal lists
  among its amendments of ratified text (its `proposal.md:1152-1183`): F-2's
  locked recovery text stands, replacing the ratified text for a locked row
  (design D4, :263-266, and D18, :1291-1294); F-1's ceiling recovery text is
  "inspect, then `git worktree remove --force <path>` by hand" only where the
  rescan finds both the target's `.git` file and its registry entry present,
  and otherwise "inspect, then `git worktree prune` and delete `<path>` by
  hand" (its `specs/project-clean/spec.md:327-331`, in `Clean can explicitly
  retire verified worktrees`, with an AND in its scenario "A removal past the
  hard ceiling" at :500-504, and :1159-1164, in `Clean records a reconcilable
  result for every removal target`); and O-1 has gate 7's branch reflog read
  that the deadline cuts record `deadline-exceeded` and leave the plan
  incomplete with `deadline-exceeded`, not `inspection-incomplete`, a read not
  finished within the filesystem budget while the deadline is not the limit
  still leaving it `inspection-incomplete` (:713-718, in `Clean previews and
  applies a batch of eligible worktree removals in one repository`; design D10,
  :648-657), the branch reflog's rule that the round (e) record above reads at
  `f0bf538`. Round (h) also gives `Clean bounds its Git work and reports
  omitted work` and the review-safety rule `Cleanup revalidates destructive
  actions` RI-3's exception for a root or common directory whose path holds a
  line feed, the identity probe then read one option per child, revalidation
  spawning at most nine Git children, ten where the plan read
  `extensions.worktreeConfig` as true, and the final rescan at most six, with
  `probes.estimated` counting the extra children (:1050-1056; review-safety
  :77-85); and, by R-258, D18 gives the `inspection-incomplete` refusal a
  variant remedy naming the unset of `core.worktree` and `core.bare` wherever a
  row it counts is `registration-mismatch` (`design.md:1311-1331`), which the
  `project-command` scenario "A linked worktree whose work tree is redirected"
  now pins in its AND at :314, with a new AND at :317 for a `core.worktree` in
  the repository's own `config`. Re-checked by script against `6bf9f77`, every
  cite of its three specs located by line alignment (156 rows: 45 of
  `project-command`, 83 of `project-clean` and 28 of the review-safety spec):
  in `project-command` every cited line through :316 keeps its number and text,
  :314's AND aside, and the five scenarios after it move down 1, to :320, :325,
  :336, :340 and :357; in `project-clean` the lines through :326 keep theirs,
  the refusal paragraph at :11-24, :15-16, :112, :170-174 and :211-212 among
  them, and the rest keep their text at new lines, F-5 at :344-353 and
  :372-374, F-3 at :806-808, the three scenarios at :867, :890 and :905, and
  the caps and the re-run sentence at :1009-1012 and :1029-1039, but for the
  gate block, now :682-769, whose gate-7 sentence O-1 rewrites, its cited parts
  keeping their text, the gate order at :682-689, the markers at :726-735, the
  clauses that FR-032 and SC-004 cite at :740-743 and :764-769 and round (e)'s
  clause at :756-758; in the review-safety spec RI-3's lines change (:77-85)
  and every cited line after them moves down 2, the rule's :122-126 at
  `f0bf538` to :124-128 and the scenarios to :236, :248 and :272-292; and the
  Risk that EC-022 cites keeps its text, at its `design.md:1739-1744`. Two of
  these reach what change 2 mirrors, and both are held. Change 2's overview
  gives the repository `inspection-incomplete` for a row whose reflog read did
  not finish, as [G] did before O-1 (A1's
  `specs/project-overview/spec.md:598-603` and :624, `design.md:321-329` and
  :342-346, and `proposal.md:291-294`, :532-537 and :713-715, at `e4a30fc`);
  A1's re-alignment of those seven sites is held for Brett Heap's ruling for
  change 2, between mirroring O-1, which lanes openRepoProject-4 and
  openRepoProject-2 recommend (R-273), and keeping `inspection-incomplete` with
  a difference that D12 records, and this spec's outcome follows A1 until then
  (FR-034; C-22, FR-033, EC-020). A1's `estimated` rule counts one identity
  probe per Git candidate, where round (h) has `project clean` count the extra
  children for a line-feed path; that re-alignment is held with #19's
  ratification, and this spec's count follows A1 (FR-020, EC-032). The rest
  reaches the overview through neither [E] nor [G]: it shows no partial-removal
  note and runs no removal (F-2, F-1), its own `inspection-incomplete` remedy
  is change 2's (A1's :624) rather than [G]'s (R-258), it has no revalidation
  (RI-3's review-safety bound), and the AND at :317 is a case of [E]'s
  unchanged rule, which FR-007 reads as A1 does. The records above that say F-2
  and F-1 wait on his word are settled by this ruling. #19's round (i),
  `e0c91bb` (`4204eb9`, `b60f6ac`, `1a4785e` and `e0c91bb`; the lead's R-271
  and R-284, with lane openRepoProject-4's finding on D6's identity probe and
  lane openRepoProject-3's W70 LOW-3 and W73 M-1), follows, and edits its
  `project-clean` spec alone, its `project-command` and review-safety specs
  unchanged (`git diff --quiet`), the scenario counts staying 71 in
  `project-clean`, 24 in `project-command` and 22 in the review-safety spec.
  Its three spec sites carry F-1's third text, by the lead's R-284, which
  refines how Brett Heap's F-1 ruling applies to a read that fails and is put
  to him to confirm, so that the text is pending his confirmation: where the
  rescan cannot read a `partially-removed` target's `.git` file, the read
  failing other than for the file's absence or cut at its budget, the recovery
  text is "inspect `<path>` by hand; its `.git` could not be read, so do not
  run `git worktree prune` until it can", since `git worktree prune` deletes
  the administrative directory of a worktree whose `.git` Git cannot stat, even
  a live one (its `specs/project-clean/spec.md:331-336`, in `Clean can
  explicitly retire verified worktrees`, an AND at :510-514 in its scenario "A
  removal past the hard ceiling", and :1174-1178, in `Clean records a
  reconcilable result for every removal target`; design D9,
  `design.md:632-640`, and D18, :1307-1313; `proposal.md:216-221`, :503-505 and
  :1180-1187). Its design also gives, with no delta edited, the
  `target-not-repository-root` refusal of a main worktree that a
  `core.worktree` or `core.bare` redirects a message that names the redirect,
  "Not the main worktree of a repository: PATH; core.worktree or core.bare
  redirects the main worktree; unset both in the repository's config, or in the
  main worktree's config.worktree, then run again.", with D6's row 3b, a child
  run only on that refusal (R-271; D18, :1353-1394, and D6, :333); narrows
  round (h)'s sentence on that refusal to a root passed by an absolute path or
  a bare name, a relative path or no argument run from the root being refused
  the same way under a `core.bare` true, but under a `core.worktree` building a
  plan whose main row Git reads where `core.worktree` points (W70 LOW-3); and
  has D6 repeat the identity probe one option per child on any count of lines
  but two, since a submodule checkout's three lines cannot be told by their
  count from those of a path that holds a line feed, as feature 004 does at
  `7164d7f` (:353-364). Its proposal records the round
  (`proposal.md:2019-2087`), and its `tasks.md` 1.2 names it (:79-85).
  Re-checked by script against `b3228bb`, every cite of its three specs located
  by line alignment (192 rows: the 156 above and the 36 places that the round
  (h) record gives at `b3228bb`): in `project-command` and the review-safety
  spec every cited line keeps its number and text, :314's and :317's ANDs and
  RI-3's :77-85 among them; in `project-clean` the lines through :330 keep
  theirs, the refusal paragraph at :11-24, :15-16, :112, :170-174 and :211-212
  among them, F-1's sentences at :327-331 and :1159-1164 gain the third text,
  now :327-336 and :1169-1178, and the rest keep their text at new lines, F-5
  at :349-358 and :377-379 and F-1's AND at :505-509, down 5, and, down 10, the
  gate block at :692-779, its gate order at :692-699, O-1 at :723-728, the
  markers at :736-745, the clauses that FR-032 and SC-004 cite at :750-753 and
  :774-779 and round (e)'s clause at :766-768, F-3 at :816-818, the three
  scenarios at :877, :900 and :915, the caps and the re-run sentence at
  :1019-1022 and :1039-1049, and RI-3's exception at :1060-1066; in its design,
  D4's F-2 sentence keeps its text at :267-270, D18's at :1316-1320, its lines
  re-wrapped, D10's O-1 at :667-676, D18's variant `inspection-incomplete`
  remedy at :1340-1343, and the Risk that EC-022 cites at :1802-1807. F-1's
  third text reaches the overview through neither [E] nor [G]: like F-1's first
  two texts it is a partial-removal note, which the overview, removing nothing,
  never shows, and A1 mirrors none of them. Two of the round's design edits
  meet what this spec states, and both are held. Where the main worktree's own
  `core.worktree` names another directory, this spec, as A1 does, leaves the
  toplevel that Git reports unaffected (FR-006; C-65) and names that toplevel
  or the checkout as `repository.root` (FR-009), while [R] refuses an absolute
  path that is not the toplevel Git reports there (its
  `specs/project-clean/spec.md:566-570`) and D18 now names the redirect in the
  checkout's refusal: a suggestion with that root is refused, or, where the
  toplevel is another repository's root, reaches that repository; A1's
  re-alignment for that layout (the lead's R-271) is held for Brett Heap's
  ruling for change 2, and this spec follows A1 as ratified until then
  (FR-006). And D6's repeat on any count but two re-reads a submodule
  candidate's identity probe too, so that `probes.performed` exceeds
  `probes.estimated` for it as for a line-feed path; this spec's count follows
  A1, A1's re-alignment of it held with the line-feed case (FR-020, EC-032). No
  requirement of this spec moves. So PR #34 does not merge before #19's
  ratification of those commits; should Brett Heap want #34 sooner, the four
  items move to a later amendment of change 2, and A1 lands without them (its
  :1281-1284), the parts of this spec that follow them following that amendment
  instead.
  - LQ-10, on PR #19 at `ea697ba`, pending its ratification: every status
    probe, the hidden-state probe and the removal pass `-c core.trustctime=true
    -c core.checkStat=default` after `-c core.fsmonitor=false`, four status
    pins in all, so that an edit that keeps a file's size and restores its
    modification time still shows where a repository sets
    `core.trustctime=false` or `core.checkStat=minimal` (its
    `specs/project-command/spec.md:140-147`; lane openRepoProject-3's finding
    F1 H-3; R-101 (e)). Its scenario "The pinned status configuration" records
    the four (:281), and the new scenario "An edit that keeps its size and
    restores its mtime" (:285) brings that delta to 21 scenarios. The
    overview's status probe carries the same pins (FR-016), so that by FR-026
    its dirty evidence stays at parity with `project clean`'s. Amendment A1 at
    `e4a30fc` restates the four where change 2 quoted [E]'s two older status
    pins, as an item of its own, a restatement following `ea697ba` and the
    pointer that #19 adds at `93f3194` (its `proposal.md:1423-1452`), ratified
    by Brett Heap in PR #34 (Amendment A1, above): requirement 3's quote
    (POD:202-204; its `specs/project-overview/spec.md:230-232`) and design
    D13's (design.md:650-652; its :690-691) each now read `-c
    core.untrackedCache=false -c core.fsmonitor=false -c core.trustctime=true
    -c core.checkStat=default` on a status probe, D13's fixture-rewrite item
    (design.md:664-665) keeping its words, since it names the two pins that
    disarm a `core.fsmonitor` hook; no packet line quotes the two older pins,
    the packet giving the status probe's argv with no `-c` pin (DI:396,
    DI:1181), so A1 declares no departure. FR-016 quotes the four as A1
    restates them. A1 also records #19's design Risk that, where a repository
    defines a clean filter, a ctime-only change under `core.trustctime=false`
    now runs that filter once per probe, which widens the clean-filter residual
    that LQ-16 leaves open (requirement 9's sentence after POD:717; its
    :1443-1452), as EC-022 and FR-040 record (lane openRepoProject-3's W25
    L10).
  - LQ-11, on PR #19 at `addd346`, pending its ratification: a linked row whose
    effective work tree is not its registered path, such as one whose
    per-worktree `core.worktree` names a decoy under
    `extensions.worktreeConfig` (lane openRepoProject-5's reader RB), is
    `registration-mismatch` (R-101 (g)). [E] reads the extension once per
    common directory, from the common `config` alone (change 1's design D6, row
    4c), and only where it is true gives each linked row whose registration
    agrees `git rev-parse --path-format=absolute --show-toplevel` before its
    status probe (its `specs/project-command/spec.md:206-219` and :224-232; the
    scenario "A linked worktree whose work tree is redirected", :303, brings
    that delta to 23 scenarios); `project clean`'s revalidation re-runs that
    probe for a target. R-125, on PR #19 at `93f3194`, adds to the two-way
    registration the administrative directory's `commondir` file, which must
    name `<common_dir>` as Git reads it, read by the filesystem with no Git
    child: a missing one, or one naming another directory, makes the
    registration disagree, and a failed read makes the row `inspection-error`
    (its `specs/project-command/spec.md:204-214`, where the lines above sit at
    :214-227 and :232-240, and the scenario "A commondir that names another
    repository", :318, bringing that delta to 24 scenarios); FR-007 and FR-013
    take it, pending, and A1 at `e4a30fc` records that it reaches the overview
    through the shared evidence model, by the registration check that
    requirement 2 cites (POD:84), with no Git child and no task or count of its
    own, and amends two texts for it: D8's per-row task, which now names the
    `commondir` file (design.md:461-462; its :480-483), and requirement 2's
    closed case list (POD:89-95; its `specs/project-overview/spec.md:104-120`),
    which gains FR-007's third case in FR-007's words, a registration check
    that cannot be completed, its disagreement case taking FR-007's tie-break,
    as [E] at `93f3194` has "a read of it that fails SHALL give the row
    `inspection-error` and no probe" (its
    `specs/project-command/spec.md:211-213`), departing from the packet's
    DI:251-261 (its `proposal.md:1393-1422`; lane openRepoProject-3's W25 M1
    and W29 L1), ratified. Lane openRepoProject-2 holds that the overview must
    classify such a row exactly as `project clean` does, with the same read and
    probe, and FR-007 does so, FR-013, FR-019, FR-020 and FR-049 following; the
    overview has no revalidation. Amendment A1 at `e4a30fc` amends change 2's
    texts that close or count the overview's children, as an item of its own
    (its `proposal.md:1353-1422`), ratified by Brett Heap in PR #34 (Amendment
    A1, above): requirement 3's `estimated` rule (POD:250-254; its
    `specs/project-overview/spec.md:280-290`) and the scenario "One probe set
    per repository" (POD:127-129; its :151-155), with design D6's
    repository-wide probes (design.md:390-392; its :407-410), the counts
    departing from the packet's DI:506-509 and DI:1193-1201; and, at the sites
    this spec recorded at `b511bdb`, the collector table's `probe-failed` row
    (POD:333; its :369), its two exceptions departing from the packet's DI:535:
    the extension read's exit 1 "with nothing printed on standard output or
    standard error, by which Git reports the value not set, read as false with
    no error", an exit 1 with a warning, as for an unreadable `config`, staying
    a failure that counts as true, as FR-007 reads it; and the
    effective-work-tree read, "where a probe that fails, as it does under
    `core.bare=true` and as a probe that cannot be spawned does, and output
    that is not exactly one line each make the row's registration disagree,
    with no error", a per-worktree `core.bare=true` included (exit 128,
    measured by lane openRepoProject-3's W20 read on Git 2.43.0 and 2.36.6), as
    `addd346` words the failing probe and the output (lane openRepoProject-3's
    W17 read, L2), and the spawn failure on the lane openRepoProject-4 lead's
    ruling (W25 L8); the second phase, which A1 names "the worktree probes,
    effective-work-tree reads and status probes" (POD:238-239; its :267-269),
    with a sentence after POD:246 (its :276-278); and design D8, with a task
    for the toplevel's realpath and its outcomes (its design.md:484-491) and
    512 toplevel realpaths in its bound of abandoned workers (:506-508), which
    FR-013 matches.
  - LQ-13, on PR #19 at `93de4bb`, and LQ-14, at `43f7107`, with the rulings
    R-124 at `2b86a5f` and R-126 at `1ebdd90`, pending its ratification: two
    protections of the batch, whose codes, gate order, markers, failure rule
    and scenarios are #19's own text. LQ-14's `operation-in-progress` keeps a
    worktree whose administrative directory holds a marker of [G]'s list at
    `1ebdd90` (its `specs/project-clean/spec.md:650-659`, after R-126), read by
    one listing and never by a Git child (the rule at :650-666 and the
    scenarios "An operation in progress", :787, and "A squash merge that holds
    an autostash", :810, there); LQ-13's `worktree-only-commits` keeps one
    whose HEAD reflog or `refs/worktree/` holds a commit that no branch, tag or
    remote-tracking ref reaches, nor a non-zero object of its branch's reflog,
    read from `logs/HEAD` and one `rev-list` child (:668-690 and the scenario
    "A commit held only by the worktree", :825, there). They are the last two
    gates, in that order, after `hidden-local-state` (:609-616 there). Since
    R-124, only a decided result gives either reason; an error on the listing,
    any other error on the `logs/HEAD` read, and a `rev-list` child that cannot
    be started or exits nonzero make the row `inspection-error`, a `rev-list`
    child stopped at its 5 s budget, or, since #19's round (d), a listing or
    read not finished within the filesystem budget, the deadline not being the
    limit, records `probe-timeout` and makes the row `inspection-error` (where
    the listing or read left the row unprobed before), the deadline's cut
    records `deadline-exceeded`, and each leaves the plan incomplete (:660-666
    and :679-690 there, and :719-722 and :741-746 at `9267303`; lane
    openRepoProject-3's W43 LOW-2); at revalidation, before each removal, a
    listing, read or child of either check that fails or runs past its budget
    refuses the target with `state-changed` (R-127; the review-safety rule,
    :101-118, and its scenarios "A worktree-only commit made after the plan"
    and "An operation started after the plan", :218 and :230, at `1ebdd90`).
    Neither is a class, so neither reaches the ladder or FR-026's parity; both
    are gates of the batch, which the overview leaves to it as it leaves the
    index gates: FR-032 lists them among the exclusions only the batch applies,
    and the overview evaluates neither, making no listing of a worktree's
    administrative directory and no `logs/HEAD` read for them and starting no
    `rev-list` child. Amendment A1 at `e4a30fc` proposes the same as an item of
    its own (its `proposal.md:1313-1352`), in requirement 7 (POD:525-526; its
    `specs/project-overview/spec.md:590-597`) and design D5 (design.md:324-325;
    its :334-341), with D5's `target-cap` item and Risks, ratified by Brett
    Heap in PR #34 (Amendment A1, above): the overview keeps the `--all-safe`
    suggestion of such a worktree, which the batch then decides itself, by
    R-124's rule above; and the route departs from the packet's OV:110-113 and
    DI:690-692. A1 takes R-124's settled rule in place of revision 3's "which
    R-124 is to settle", and cites [G]'s list at `1ebdd90` rather than naming
    the markers, ratified. SC-004 and EC-007 follow.
  - LQ-15, decided and not built (EC-036), on PR #19 at `cc000ea` and, after
    lane openRepoProject-3's W8 read, `9fb22fa`, pending its ratification:
    [E]'s new "Configuration paths" paragraph (its
    `specs/project-command/spec.md:100-111` at `cc000ea`, :116-129 at
    `9fb22fa`) has every subcommand that inspects a Git repository test, before
    any Git child starts, `git --version` included, whether `HOME` or
    `XDG_CONFIG_HOME` is set to a non-empty value whose first byte is not "/",
    on the raw bytes, an empty or unset variable passing it, and, as `9fb22fa`
    words it, for each variable whether or not Git would read a file through
    it, not following Git's order of precedence; where one fails, the
    subcommand starts no Git child and inspects no repository
    (`relative-config-path`). #25's C-44 (draft PR #29), in the form its rounds
    C18, C20 and C21 give it at `a529310` (its
    `specs/project-overview/spec.md:417-426`, :489-495 and :624), tests
    `GH_CONFIG_DIR`, `XDG_CONFIG_HOME` and `HOME` for `gh`: a relative
    `GH_CONFIG_DIR` makes the lookup of `gh` fail, every queried row being
    `unavailable` with `gh-unavailable`, on every base; a relative
    `XDG_CONFIG_HOME` or `HOME` does so only where neither text stops the run
    first, change 1's evidence model as #19 amends it starting no Git child and
    inspecting no repository (its `specs/project-command/spec.md:124-125` at
    `4f1c0e0`), and change 2's exit rule, as A1 words it, refusing with
    `relative-config-path` and exit 2 (A1's
    `specs/project-overview/spec.md:868-876` at `e4a30fc`; FR-043); and in
    every case no `gh` child starts. Where #29's text at `e1a9f84` said that
    both refuse, its rounds C20 and C21 pair each with its own verb: the
    Requests paragraph has the evidence model "by barring every Git child and
    inspecting no repository" and the exit rule "by refusing the run"
    (:422-424; its C-66, on lane openRepoProject-3's W61), the Results
    paragraph reads "not stopped" (:490), and the scenario's AND reads "stops"
    (:624; its C-67 (a)), all at `a529310`, the evidence model leaving the
    refusal to each command's own requirement, as `project clean`'s is at its
    `specs/project-clean/spec.md:15-16` at `4f1c0e0`. Brett Heap also gave
    LQ-15 to lane openRepoProject-2 directly, "yes, refuse relative HOME like
    #29" (R-102 (a)). `clean` refuses with `relative-config-path` and exit
    status 2 in every mode, once its arguments have passed the checks that
    refuse `invalid-arguments` and before its version check (its
    `specs/project-clean/spec.md:13-22` at `cc000ea`, :13-23 at `9fb22fa`, and
    the scenario "A relative configuration path", :109 at `cc000ea`); `doctor`
    reports it as an `error` check row and exits 1, `status` marks the
    repository root `inspection-error` with that code and exits 0, and `update
    --apply --component shape` refuses with exit 2 and never invokes the owner
    tool (project-command `:8-17`, and the scenario "A relative configuration
    path in status, doctor and update", :266, both at `cc000ea`). The overview
    follows [E] as amended, making the same test before any Git child, the
    version check included, once its arguments have passed its own checks
    (FR-043). `9fb22fa` leaves the overview's code and exit status under the
    test to `add-project-overview` (its `proposal.md:951-956`), and change 2's
    closed lists give [E]'s text none: its exit-2 codes (POD:677-678) and
    requirement 11's exit rule (POD:765-768; FR-042). Amendment A1 at `e4a30fc`
    proposes `relative-config-path` among those codes, with exit 2 under that
    rule, as an item of its own on the basis of Brett Heap's LQ-15 word, whose
    form the lead gave as `clean`, `status`, `doctor` and `update` (lane
    openRepoProject-2's ruling R-102 (c) 3; `9fb22fa` proposal.md:954-956; A1's
    `proposal.md:1286-1312`), ratified by Brett Heap in PR #34 (Amendment A1,
    above): the code departs from the packet's closed list of exit-2 codes
    (DI:1086-1089), and the fallback, should he strike it, is `refused` with
    exit 2, inside change 2's lists, which departs from nothing. If he strikes
    LQ-15's extension, A1's sentence on `GIT_CONFIG_GLOBAL` and
    `GIT_CONFIG_SYSTEM` is struck with PR #19's sites.
  - LQ-15's extension, in a sentence of its own that Brett Heap may strike: the
    same test applies to `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` (:103 at
    `cc000ea`, :119-120 at `9fb22fa`, whose design D11 lists every site a
    strike touches, design.md:753-777 there), lane openRepoProject-2's own
    addition (R-102 (c) 3), since a relative `GIT_CONFIG_GLOBAL` runs a
    candidate's filter as a relative `HOME` does (EC-036).
  - LQ-12, on PR #19 at `eae1a79`, `update`'s owner-tool environment, every
    owner tool of `update --apply` running with the push child's scrub, does
    not reach the overview, which starts no owner tool.
- **Features 001 to 003** (`specs/001-project-command/`,
  `specs/002-triad-first-project-new/`,
  `specs/003-parent-obstacle-wording/`): untouched; their tests join the
  suite this feature keeps passing.
- **Governance**: change 2's tasks 1.1 to 1.6, 2.1 and 2.2 are done; 3.1 is
  ticked with its `Created:` record; 3.2 (`/opsx:apply` only once the
  handoff names one feature) stays open.
- **Runtime and CI**: Git 2.36 or later; the runtime versions the README
  supports (Python 3.10 or newer) and CI runs, on Linux only since `e9d6711`
  (#32): Python 3.10 and 3.12 on `ubuntu-latest`, two `test` jobs, the README's
  Development section saying that CI covers Linux only (change 2's design,
  Context, written before it, still names Ubuntu and macOS); feature 004's Git
  2.36 floor job (its FR-067), `git-floor` on `ubuntu-latest` with Python 3.10
  beside every job of the `test` matrix (its plan, "CI shape", at `d81b3d9`,
  which no longer counts those jobs, lead ruling R-46), whose selection gains
  one `-k` prefix for the overview's small floor set (FR-050; Clarifications,
  C-57), at `c9103ba`, after `2cf34d3`, building Git with `-std=gnu17`,
  installing a hash-pinned PyYAML in place of `requirements.txt` and fetching
  Git's sources over HTTPS only, its `-k` selection unchanged; and the existing
  YAML requirement for manifests.

## Out of Scope

As the change defers it (proposal, "Out of Scope"; design, Non-Goals), each
extension needing its own proposal (OQ-27):

- Branch deletion, cache disposal, and paired retirement of a worktree with its
  branch; the last two are proposed as `add-project-clean-cache-disposal` (#24)
  and `add-project-clean-branch-retirement` (#23), #24's overview part realized
  in its own feature, never in this one, in every order (Dependencies;
  Clarifications, C-71).
- Remote, GitHub or pull-request queries, a `project overview --remote`, and
  the closed PR #2's remote merge-target and pull-request lookups; the
  overview's `--remote` is proposed as
  `add-project-overview-remote-merge-status` (#25), realized in its own feature
  after this one (Dependencies; Clarifications, C-71).
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
(`specs/project-overview/spec.md` and `specs/project-review-safety/spec.md` at
`961c405`), and the one scenario that amendment A1 at `e4a30fc` adds to them,
"A relative configuration path" (its `specs/project-overview/spec.md:908-912`),
whose row, 64, is A1's and lands with PR #19's ratification of LQ-15's commits
(FR-043; Dependencies), by header, mapped to the functional requirements, user
stories and edge cases of this spec that realize it. Requirement numbers are
the proposal's (1 to 12); PRS is the MODIFIED `project-review-safety`
requirement. A story scenario is written `USn sk`. The test names come with the
tasks, in the feature's `traceability.md`, as feature 003 records them.

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
| 8 | Overview prints a versioned JSON envelope | POD:606 | FR-036 to FR-039 | US5, US11 | EC-016, EC-017, EC-027, EC-028, EC-034 |
| 9 | Overview is local and read-only | POD:709 | FR-040, FR-016 | US10 | EC-006, EC-022, EC-036 |
| 10 | Overview reports default-branch health | POD:724 | FR-041 | US9 | EC-011, EC-021, EC-026 |
| 11 | Overview exits by completeness and severity | POD:761 | FR-042 to FR-044 | US10 | EC-002, EC-015, EC-035 |
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
| 64 | 11 | A relative configuration path | FR-042, FR-043 | US10 s5 | EC-036 |

### Coverage

Delta requirements mapped: 13 of 13 (12 ADDED in `project-overview`, 1 MODIFIED
in `project-review-safety`). Delta scenarios mapped: 64 of 64 (62 and 2, row 64
being A1's), each to at least one FR and exactly one story scenario; "main
target" and "master target" share US3 s3, the two candidate-cap scenarios share
US6 s1, and "Git too old" and "Git unavailable" share US10 s2. Functional
requirements traced: FR-001 to FR-046 each realize at least one row above;
FR-047 (scope), FR-048 (README) and FR-049 (tests) trace to the proposal's
Impact and design D13, not to one scenario; FR-050 (the Git 2.36 floor job)
traces to Brett Heap's answer C-57, which amendment A1 carries in that Impact;
and FR-051 (`AGENTS.md`) traces to his answer C-58, a departure from it. Story
scenarios with no delta scenario of their own: US1 s8 (POD:18-19; C-1) and
US2 s4 (POD:462-468).
