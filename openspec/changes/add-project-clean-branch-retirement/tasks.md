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
- [ ] 1.2 Alignment resolved: the stack-architect and qa-lead findings on this
  draft are applied, MISMATCH and DRIFT at once and each GAP put to Brett
  Heap; verified by the table "Questions Resolved by the Alignment Review" in
  `proposal.md` and the alignment comment on the pull request.
- [ ] 1.3 Council resolved: each product-advocate, systems-architect and
  adversary-engineer concern on the aligned proposal is VALID (applied to
  `proposal.md`), NOTED (recorded in a `clarifications.md` that `design.md`
  then answers) or DISMISSED; verified by "Council Verdicts" in `proposal.md`
  and the council comment on the pull request.
- [x] 1.4 Spec deltas and design written: `specs/project-clean/spec.md`
  modifies four requirements and adds one (52 scenarios: 37 carried unchanged
  from change 1 and PR #19, 15 added), and
  `specs/project-clean-review-safety/spec.md` modifies one (4 scenarios: 3
  carried, 1 added), every scenario of each modified requirement's source text
  kept byte for byte; `design.md` holds D1 to D10 (`8341954`, `d0b33ce`);
  verified by `grep -c '^#### Scenario:'` on each spec file.
- [x] 1.5 Validation passes: `/usr/bin/openspec validate
  add-project-clean-branch-retirement --strict` reports the change valid,
  `/usr/bin/openspec validate --all --strict` reports 8 passed, 0 failed, and
  `/usr/bin/openspec status --change add-project-clean-branch-retirement
  --json` shows every artifact done; verified by running the three on this
  branch after 1.4 (build 1.13.1, which notes only as INFO that archive would
  refuse the MODIFIED blocks whose base still sits in change 1).
- [ ] 1.6 Ratified by Brett Heap's word on the pull request, quoted with its
  link here, the proposal's three Open Questions before him; verified by that
  quote. No implementation starts before it.

## 2. Before the Speckit handoff

- [ ] 2.1 Change 1 (`add-project-clean-all-safe`, issue #9) archived after
  feature 004 merges, so that "Clean previews and applies a batch of eligible
  worktree removals in one repository", "Clean bounds its Git work and reports
  omitted work", "Clean records a reconcilable result for every removal
  target" and "Cleanup states a narrow guarantee and its residual window" are
  canonical and the seam this change attaches to is on `main`; verified by
  those headers in `openspec/specs/` and by `/usr/bin/openspec validate
  add-project-clean-branch-retirement --strict` passing with no archive notice.
- [ ] 2.2 PR #19 resolved: when it lands, "Clean bounds its Git work and
  reports omitted work" is compared with the text that landed and re-based if
  that text moved past `c462d87`; when it closes unmerged, the block is
  re-based on change 1's text; verified by a diff of the block's carried text
  against the canonical requirement.
- [ ] 2.3 `add-project-clean-cache-disposal` (issue #24) checked: every
  requirement both changes MODIFY is listed here with the cache change's
  state, and if it has archived, this change's blocks are re-based on its
  archived text now, otherwise 3.2 holds the re-base; verified by
  `/usr/bin/openspec validate --all --strict` passing after any re-base.

## 3. Landing and archive readiness

- [ ] 3.1 The realization PR is merged with green checks on all four CI jobs
  (`ubuntu-latest` and `macos-latest`, Python 3.10 and 3.12) and closes issue
  #23; verified by citing its merge sha here, from `gh pr view <number> --json
  mergeCommit,statusCheckRollup`.
- [ ] 3.2 `add-project-clean-cache-disposal` is archived before this change,
  and this change's shared MODIFIED blocks carry its archived text (L-5);
  verified by `/usr/bin/openspec validate add-project-clean-branch-retirement
  --strict` passing against the main specs that archive left.
- [ ] 3.3 The change is archived with `/opsx:archive` only after 3.1 and 3.2;
  verified by `/usr/bin/openspec validate --all --strict` passing after the
  archive.

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
