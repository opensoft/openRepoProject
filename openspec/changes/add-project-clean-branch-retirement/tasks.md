Lane: openRepoProject-5

# Tasks

This is the governance and handoff record only. The implementation tasks live
in the one Speckit feature named under "Speckit Handoff"; OpenSpec does not
duplicate them.

## 1. Governance record

- [x] 1.1 Proposal written: `proposal.md` adopts the packet's paired-retirement
  contract (`BA:1339-1345`) under the lane's rulings L-1 to L-9 and A-1 to A-7,
  on change 1's text at `961c405` and PR #19's at `c462d87` (`d66d02c`);
  verified by its Capabilities section accounting for every canonical
  requirement of `project-clean` and `project-clean-review-safety` and every
  requirement change 1 adds to them.
- [x] 1.2 Alignment resolved: the stack-architect and qa-lead findings on
  `e7f3e65` (SA-1 to SA-5, QA-1 to QA-4) are applied, MISMATCH and DRIFT at
  once and qa-lead's GAP (QA-3) by its own scenario text, and the review's
  GAPs for the lane are settled by the lane's rulings of 2026-10-18 (A-5
  amended, L-10, A-9 to A-13), the two that need Brett Heap's word (A-9, A-10)
  put to him as Open Questions; applied by `0f89873`, `8227772`, `7689028` and
  the commit that ticks this task; verified by the table "Questions Resolved by
  the Alignment Review" in `proposal.md`, one row per finding id with its
  severity, the ruling and the section edited, and by the lane's alignment
  comment on PR #26.
- [x] 1.3 Council resolved: each product-advocate, systems-architect and
  adversary-engineer concern on the aligned proposal at `874d1ad` (P-1 to P-4,
  S-1 to S-4, AE-1 to AE-4) is VALID (applied to `proposal.md` and, where its
  contract requires, the deltas and `design.md`), NOTED (S-4, recorded in
  `clarifications.md`, which `design.md` D2 answers) or DISMISSED (none), under
  the lane lead's verdicts of 2026-10-19 (A-16 to A-20, A-1, A-4 and A-5 as
  amended, P-2, P-4), with lane openRepoProject-3's packet-fidelity findings on
  `874d1ad` (H1, M1 to M6, L1 to L12) and council B's three refinements
  (recorded in the lane's handoff at the register's `c3a9b3767`, line 50)
  applied in the same round; applied by `79a71ec`, `909425b`, `f93073b`,
  `6d237fe`, `36f3eef`, `15cf7ed`, `e012757`, `a5a95eb`, which ticks this
  task, `785a45e` (A-16 as amended, recorded at
  `lanes/log/openRepoProject-5.md:33`, and `branch_plan` on each selected
  entry), `16051d1`, the project-command block lane openRepoProject-2 agreed
  (ruling A-20), and `ca96701`, which records that agreement and lane 2's note
  for feature 006; verified by "Council Verdicts" in `proposal.md`, one row per
  council concern id and per lane 3 id, by `clarifications.md`, and by the
  council comment on the pull request. Round A3, on `ca96701`, applied lane
  openRepoProject-3's re-read of that head (ruling A-21, its M1, M4 and L4 of
  review 26 among it), Codex's three findings on `785a45e` (A-22), B2's third
  escalation (A-23) and the lead's note on #29's committed block, by
  `3150af3` (the spec deltas), `a54c56e` (the design), `3e875e2` (the
  proposal's body) and the commit that records the round's table and updates
  this task; verified by "Re-read and Codex Findings (round A3)" in
  `proposal.md`, one row per item.
- [x] 1.4 Spec deltas and design written: `specs/project-clean/spec.md`
  modifies five requirements and adds one (67 scenarios: 43 carried unchanged
  from change 1 and PR #19, 6, 14, 10, 5 and 8 by block, and 24 added, the
  24th in round A3),
  `specs/project-clean-review-safety/spec.md` modifies one (4 scenarios: 3
  carried, 1 added), and `specs/project-command/spec.md` modifies one on PR
  #19's text (9 scenarios carried, none added; agreed by lane
  openRepoProject-2 on 2026-10-19 and committed in `16051d1`, ruling A-20),
  every scenario of
  each modified requirement's source text kept byte for byte; `design.md`
  holds D1 to D10 (`8341954`, `d0b33ce`, and the commit titled 'Settle which
  later targets carry branch-retention-stop'), revised by the alignment fix
  round (1.2), the council round (1.3) and round A3; verified by `grep -c
  '^#### Scenario:'` on each spec file and by a scenario-carry script run
  after the council round and again after round A3 over all seven MODIFIED
  blocks, every source scenario present byte for byte and in order.
- [x] 1.5 Validation passes: `/usr/bin/openspec validate
  add-project-clean-branch-retirement --strict` reports the change valid,
  `/usr/bin/openspec validate --all --strict` reports 8 passed, 0 failed, and
  `/usr/bin/openspec status --change add-project-clean-branch-retirement
  --json` shows every artifact done; verified by running the three on this
  branch after 1.4, after the alignment fix round, after the council round
  and after round A3
  (build 1.13.1, which notes only as INFO that archive would refuse the
  MODIFIED blocks whose base still sits in change 1).
- [ ] 1.6 Ratified by Brett Heap's word on the pull request, quoted with its
  link here, the proposal's six Open Questions before him, the project-command
  block that lane openRepoProject-2 agreed being dropped if PR #19 absorbs its
  clauses (lane openRepoProject-2's LQ-6) and also a Budgets exception that
  covers the re-read's shorter budget, which LQ-6 does not list for this
  change (its Budgets clause, recorded under A-20; `proposal.md`, Dependencies
  and Sequencing). Ratifying this change ratifies the
  two blocks written on PR #19's text, "Clean bounds its Git work and reports
  omitted work" and "Repository inspection requires Git 2.36 and shares one
  evidence model", only as written there at `c462d87`, never PR #19's own
  sentences, and 2.2 then re-reads them before the handoff (lane
  openRepoProject-3's M1); verified by that quote. No implementation starts
  before it.

## 2. Before the Speckit handoff

- [ ] 2.1 Change 1 (`add-project-clean-all-safe`, issue #9) archived after
  feature 004 merges, so that "Clean previews and applies a batch of eligible
  worktree removals in one repository", "Clean bounds its Git work and reports
  omitted work", "Clean records a reconcilable result for every removal
  target" and "Cleanup states a narrow guarantee and its residual window" are
  canonical and the seam this change attaches to is on `main`; verified by
  those headers in `openspec/specs/` and by `/usr/bin/openspec validate
  add-project-clean-branch-retirement --strict` passing with no archive notice.
- [ ] 2.2 PR #19 resolved: when it lands, the two blocks written on its text,
  "Clean bounds its Git work and reports omitted work" and "Repository
  inspection requires Git 2.36 and shares one evidence model", are re-read
  against the text that landed and re-based if that text moved past
  `c462d87`; when it closes unmerged, both are re-based on change 1's archived
  text; a re-base that changes either block's text returns that block to
  Brett Heap for ratification before the handoff (lane openRepoProject-3's
  re-read, LOW-8); verified by a diff of each block's carried text against the
  canonical requirement.
- [ ] 2.3 `add-project-clean-cache-disposal` (issue #24) checked: the five
  requirements both changes MODIFY under the lane's rulings B-10 and A-13
  ("Clean can explicitly retire verified worktrees", one cache clause; "Clean
  previews and applies a batch of eligible worktree removals in one
  repository", the cache digest; "Clean bounds its Git work and reports
  omitted work", the counting sentence merged, this change's incompleteness
  clause kept, and the cache fit sentence, which at `e906c2f` counts "at most
  250 Git children besides the 16 removals, about 42.3 s", or its restatement
  under the lane's ruling B-25, scoped to runs without the flag; "Clean
  records a reconcilable result for
  every removal target", the cache-deletion exception; "Cleanup states a
  narrow guarantee and its residual window", the cache target's revalidation)
  are listed here with the cache change's state, and if it has archived, this
  change's five blocks are re-based on its archived text now, otherwise 3.2
  holds the re-base (L-11). At the re-base the flagless digest becomes
  byte-identical to the cache change's, `retire` follows its per-target cache
  data, and the two stage sentences after the removal floor sit side by side.
  At that re-base, and only then, "A flagged preview's digest binds the
  flagged apply" gains this AND, which tests the cache change's own
  requirement (lane openRepoProject-3's re-read, MEDIUM-2): "**AND** when the
  flagged plan also selects a target whose plan lists caches, as "Clean
  disposes of listed caches before a worktree removal" states, the canonical
  text carries that target's cache data after its triple and `retire` after
  both, so that a change to one of its listed caches, or to a branch the plan
  retires, gives another digest and the flagged apply refuses with
  `plan-digest-mismatch` and exit 2". If PR #27 is not ratified, the five
  blocks re-base on change 1's archived text instead, that AND is not added,
  and A-9's joint fit is moot; verified by `/usr/bin/openspec validate --all
  --strict` passing after any re-base.
- [ ] 2.4 `add-project-overview-remote-merge-status` (issue #25, PR #29)
  checked: its MODIFIED block of "Repository inspection requires Git 2.36 and
  shares one evidence model" is committed at `f66ed58`, on PR #19's text,
  agreed by lane openRepoProject-2 with one fix and unchanged at its head
  `c928cb2`, and by L-11 and L-17 whichever of it and this change archives
  second re-bases that block on the other's archived block; verified by
  `/usr/bin/openspec validate --all --strict` passing after any re-base.

## 3. Landing and archive readiness

- [ ] 3.1 The realization PR is merged with green checks on every job of
  `.github/workflows/tests.yml` at its merge (at `origin/main` `e9d6711`, the
  `test` job on `ubuntu-latest` for Python 3.10 and 3.12; feature 004 adds
  `git-floor`) and closes issue #23; verified by citing its merge sha here,
  from `gh pr view <number> --json mergeCommit,statusCheckRollup`.
- [ ] 3.2 If `add-project-clean-cache-disposal` is ratified, it is archived
  before this change, all five of this change's MODIFIED blocks, each shared
  with it, carry its archived text (L-5, L-11, A-13), and the AND of 2.3 is
  added; if it is not ratified, the five blocks carry change 1's archived text
  and the AND is not added (lane openRepoProject-3's re-read, MEDIUM-2; its
  review 26, M4); verified by `/usr/bin/openspec validate
  add-project-clean-branch-retirement --strict` passing against the main specs
  that archive left.
- [ ] 3.3 The change is archived with `/opsx:archive` only after 3.1 and 3.2,
  and after PR #19 is resolved: after its amendment of change 1 has landed,
  or, if it closed unmerged, after both blocks on its text were re-based on
  change 1's archived text (2.2, 2.4; lane openRepoProject-3's re-read,
  LOW-8); verified by `/usr/bin/openspec validate --all --strict` passing
  after the archive.

## Speckit Handoff

Implementation is tracked exclusively in one Speckit feature, to be created by
`/speckit.specify` after ratification (1.6) and section 2, from a local `main`
synced to `origin/main`. The feature covers the flag, the branch stage and its
record in `project` (`design.md` D1 to D8 and D10), the README's "Clean up Git
worktrees", and the tests of D9.

- Feature identifier: to be created by /speckit.specify after 1.6 (006 or the next free number)
- Branch: to be created by /speckit.specify after 1.6 (006 or the next free number)
- Tasks: to be created by /speckit.specify after 1.6 (006 or the next free number), then written by /speckit.tasks

`/opsx:apply` is not run until this section names exactly one feature and that
feature exists.
