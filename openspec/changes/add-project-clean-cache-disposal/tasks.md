Lane: openRepoProject-5

# Tasks

This is the governance and handoff record only. The implementation tasks will
live in the one Speckit feature named under "Speckit Handoff"; OpenSpec does not
duplicate them, and nothing here is an implementation step.

## 1. Governance record

- [x] 1.1 Proposal written: `proposal.md` adopts the packet's cache-disposal
  contract (`BA:1314-1337`) under the lane's rulings L-1 to L-17 and B-1 to
  B-40, names three departures from B-6 as first written, which B-11 accepted,
  and one from B's list of modified requirements (CD-1 to CD-4) with the rest
  of its own decisions (CD-5 to CD-18), and puts five Open Questions before
  Brett Heap; verified by its Capabilities section accounting for every
  requirement of `project-clean` and `project-clean-review-safety`, canonical
  and change 1's ADDED alike, and for change 2's `project-overview`.
- [x] 1.2 Alignment resolved: the alignment review (stack-architect and
  qa-lead) ran on `7290100`, and its findings are applied under the lane's
  rulings of 2026-10-11 and 2026-10-18; verified by the table "Questions
  Resolved by the Alignment Review" in `proposal.md`, one row per finding id
  with its severity, the ruling and the section edited, and one row per lane
  ruling that answered the review's five GAPs.
- [x] 1.3 Council resolved: each product-advocate, systems-architect and
  adversary-engineer concern on the aligned proposal at `9ebe9f0` (P-1 to P-4,
  S-1 to S-4, AE-1 to AE-5) is VALID (applied to `proposal.md` and, where its
  contract requires, the deltas and `design.md`), NOTED (S-4, recorded in
  `clarifications.md`, which `design.md` D4 and D14, its Migration Plan and
  2.3 and 3.1 below answer) or DISMISSED (none), under the lane lead's verdicts
  of 2026-10-19 (B-16 to B-24), with Codex's three findings on `3c08613` and
  lane openRepoProject-3's packet-fidelity findings on `3c08613` and `9ebe9f0`
  (M1 to M5, LOW 1 to LOW 17) applied in the same round; applied by `47242d1`,
  `b6653c0`, `e0a0ad0` and the commit that ticks this task, the
  `project-overview` delta's B-22 edit then held uncommitted, and committed as
  `9f30fb9` once lane openRepoProject-4 agreed it (2.2); verified by
  "Council Verdicts" in `proposal.md`, one row per council concern id, per
  Codex finding and per lane 3 id, by `clarifications.md`, and by the council
  comment on the pull request.
- [x] 1.4 Spec deltas and design written: `specs/project-clean/spec.md`
  modifies five requirements and adds one (55 scenarios: 5, 14, 11, 6, 8 and
  11), and `specs/project-clean-review-safety/spec.md` modifies three and adds
  one (28 scenarios: 6, 11, 4 and 7, B-26's among the 7), every scenario of
  each modified
  requirement's source text kept by name, in order and byte-exact except four,
  whose ignored files are now named as not Python bytecode caches:
  "Ignored-file bound", "A merged worktree has ignored local files", and,
  under B-22, change 1's "Every protected classifier" in the batch block and
  change 2's "Every protected classifier" in the overview block (proposal,
  Capabilities); `specs/project-overview/spec.md` modifies one requirement of
  change 2 (8 scenarios: 6 byte-exact, 1 edited and 1 added), committed as
  `b4d3e12`, its B-22 edit agreed by lane openRepoProject-4 on 2026-10-19
  and committed as `9f30fb9`, and B-30's scope, lane 4's own words, committed
  as `4d5855a` (2.2); `design.md` holds D1 to D14 and `clarifications.md` the
  NOTED S-4; verified by `grep -c '^#### Scenario'` on each delta, by a script
  run after the council round and again after rounds B3, B4, B5 and B6 that
  compares every scenario of each of the nine MODIFIED blocks with its source
  text, and by `design.md`'s headings.
- [x] 1.5 Validation passes: `/usr/bin/openspec validate
  add-project-clean-cache-disposal --strict` reports the change valid,
  `/usr/bin/openspec validate --all --strict` passes every item, and
  `/usr/bin/openspec status --change add-project-clean-cache-disposal --json`
  shows every artifact done; verified by running the three commands on this
  branch after 1.4, after the alignment fix round, after the council round
  (the last with the B-22 `project-overview` edit not yet committed), again
  after lane 4's agreement and that edit's commit, after round B3, after round
  B4, after round B5 and after round B6. The INFO
  lines, that the archive would refuse a delta
  whose MODIFIED requirement change 1 or change 2 adds until that change is
  archived, are the expected state for blocks written on sister changes.
- [ ] 1.6 Ratified by Brett Heap's word on this change's pull request, quoted
  with its link here, with the five Open Questions of `proposal.md` before
  him; verified by that quote. No implementation starts before it.

## 2. Before the Speckit handoff

- [ ] 2.1 Change 1 archived: `add-project-clean-all-safe` is archived after
  feature 004 merges, with draft PR #19's amendment of change 1 landed first
  (L-16), or PR #19 closed, and the two
  MODIFIED blocks written on PR #19's text ("Clean bounds its Git work and
  reports omitted work" and "Cleanup revalidates destructive actions")
  re-checked against the archived text and rewritten where it differs, as every
  other block written on change 1's text is; verified by
  `openspec/specs/project-clean/spec.md` and
  `openspec/specs/project-clean-review-safety/spec.md` holding every requirement
  this change modifies, and by `/usr/bin/openspec validate
  add-project-clean-cache-disposal --strict` reporting no archive refusal for
  those two deltas.
- [x] 2.2 The overview exception agreed (B-14, B-22, B-30, B-36): lane
  openRepoProject-4, owner of change 2 and feature 005, agrees the diff of
  `specs/project-overview/spec.md`, which carries change 2's "Overview reuses
  the cleanup classifier and merge target" (APO/ov:358) whole with two
  sentences appended to its equality clause, lane 4's precision in its carried
  "Every protected classifier" and one added scenario, and the delta is then
  committed on this branch; verified by lane 4's agreement, cited here from
  the lane register's logs (`lanes/log/openRepoProject-4.md` and
  `lanes/log/openRepoProject-5.md`, read on the register's `origin/main` at
  `384f71e3c`), and by the commits' shas. Lane 4 agreed the first diff on
  2026-10-19: lane 4's log, line 32 (NOTED of 2026-10-19T22:02:09Z), records
  "Lane 5 sent both held overview diffs: #24's classifier block YES", and lane
  openRepoProject-5's log, line 27 (NOTED of 2026-10-19T22:11:58Z), "lane 4
  agreed #24's overview block as sent". That delta was committed as
  `b4d3e12`, which lane 4's log, line 37 (NOTED of 2026-10-19T22:24:43Z),
  records as "cmp-identical to the reviewed held copy". The council's B-22
  reopened this task: its rewording of the two sentences, the third worktree
  in the new scenario's fixture and lane 4's precision in "Every protected
  classifier" were written in the worktree and held uncommitted until lane 4
  agreed their diff. Lane 4's log, line 47 (NOTED of 2026-10-19T23:46:27Z),
  records "Agreed lane 5's held-B2 diff to #27 (opensoft/openRepoProject#24)
  against lane 4's b4d3e12 classifier block, all three edits as written", and
  "One optional readability note was given ("its" to "clean's")." That point
  is applied in the delta as committed, `9f30fb9`, which lane 4's log, line 49
  (NOTED of 2026-10-19T23:56:15Z), records: "its project-overview/spec.md is
  the held-B2 file plus lane 4's readability point (line 32, "because clean's
  cache enumeration") and nothing else." Both agreements are cited by the lane
  logs in place of a link, since lane 4 gave them by lane message and not on
  the pull request (lane 3's LOW 16 and its re-read LOW 3). Reopened in round
  B4: B-30 ends the second sentence with lane 4's own words of 2026-10-20, "for
  the same working directory and refs", and the added scenario's AND follows
  them; lane 4's handoff, line 132 on the register's `origin/main` at
  `971bc6eda`, records that B-30 takes lane 4's "for the same working
  directory and refs", and the edit is committed alone as `4d5855a`. Ticked
  again in round B5 (B-36) on lane 4's byte check of `4d5855a`, which its log
  records at line 64 (NOTED of 2026-10-20T11:50:06Z, brett-wip `fab1e721d`,
  read on the register's `origin/main` at `fa9800bad`, where it is still line
  64): "YES to lane 5's B-30 on #27 (opensoft/openRepoProject#24): lane 4 agrees
  the words "for the same working directory and refs" as committed in
  4d5855a. Byte-checked: the project-overview delta differs from the agreed
  9f30fb9 only by those words, on the SHALL NOT sentence (now :35-36) and on
  the cache scenario's last AND (:74), +3/-2, and it is unchanged from 4d5855a
  to head e1049b2. Lane 5 may cite this line for tasks 2.2." Round B5 leaves
  `specs/project-overview/spec.md` as it was at `e1049b2`, and round B6 leaves
  it so, its blob at `fffc194` being the same.
- [ ] 2.3 Enumeration, walk and stage measured (Open Questions, the caps and
  the opens limit; S-4): the cache enumeration's child, the plan-time walk with
  its access checks, and the cache stage timed warm and cold by change 1's
  protocol (its design D5) on a Linux filesystem path, the walk at 16 rows of
  512 recorded objects with the invocation's totals reached (8,192 walked,
  4,096 counted; B-25), the stage at 512 entries per worktree and 4,096 per
  run, and B-33's deep-tree worst case (a chain of 341 directories whose
  deepest 171 each hold one loose `.pyc`, walked and disposed of, and 16 rows
  of 512 nested `__pycache__` directories, walked, the 8 that the totals
  select disposed of), through feature 004's `fs_call`, idle and at the
  workstation's usual load, and the fit of `design.md` D4 reapplied; and the
  enumeration's argument vector checked on Git 2.36.6 by change 1's D17 method
  (the `! ` record, the trailing `/` of a directory record, the untracked-files
  refusal and the order of ignored records); verified by the numbers posted on
  this change's pull request and summarised here; a cap the fit rejects is
  lowered in the deltas before the handoff, otherwise the caps stand as
  measured, and the limit on the stage's directory opens is set as Brett Heap
  answers its Open Question.

## 3. Landing and archive readiness

- [ ] 3.1 The realization PR is merged with green checks on every job of the
  workflow on its base, feature 004's `git-floor` job included beside `test
  (3.10)` and `test (3.12)` on `ubuntu-latest` (S-4), and closes issue #24;
  verified by citing its merge sha here, from `gh pr view <number> --json
  mergeCommit,statusCheckRollup`.
- [ ] 3.2 This change's `project-overview` block re-aligned (B-29, lane
  openRepoProject-4's F2): before `/opsx:archive` (3.3), which follows change
  2's archive, this change's "Overview reuses the cleanup classifier and merge
  target" is re-read against main's text of that requirement, in
  `openspec/specs/project-overview/spec.md` once change 2 is archived, and
  re-copied from it, keeping every amendment that landed there after
  `961c405`, such as lane 4's planned one for feature 005's open Q7 A, with
  this change's two sentences, its precision in "Every protected classifier"
  and its added scenario, and any sentence lane openRepoProject-4 asks for is
  in; verified by a `diff -u` of main's block against this change's block
  showing additions only, its changed lines keeping every word of main's, and
  by the validation of 1.5 passing again.
- [ ] 3.3 The change is archived with `/opsx:archive` only after 3.1, 2.1,
  change 2's archive (B-14) and 3.2, and before
  `add-project-clean-branch-retirement` (#23) archives; verified by
  `/usr/bin/openspec validate --all --strict` passing after the archive.

## Speckit Handoff

Implementation is tracked exclusively in one Speckit feature, to be created by
`/speckit.specify` after ratification (1.6) and after section 2, from a local
`main` synced to `origin/main`. The feature covers the sample test, the cache
enumeration, the plan's and the record's `cache_disposal`, the cache stage and
the revalidation of a cache target in `project` (`design.md` D1 to D13), the
README paragraph, and the tests of `design.md` D14, among them, once feature
005 has landed, the exclusion of the cache case from any feature 005 test
asserting that the overview and `project clean` classify identically (B-14).

- Feature identifier: to be created by /speckit.specify after 1.6 (006 or the
  next free number)
- Branch: to be created by /speckit.specify after 1.6 (006 or the next free
  number)
- Tasks: to be created by /speckit.specify after 1.6 (006 or the next free
  number), at specs/<that feature>/tasks.md by /speckit.tasks

`/opsx:apply` is not run until this section names exactly one feature and that
feature exists.
