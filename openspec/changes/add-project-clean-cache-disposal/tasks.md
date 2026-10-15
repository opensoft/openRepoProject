Lane: openRepoProject-5

# Tasks

This is the governance and handoff record only. The implementation tasks will
live in the one Speckit feature named under "Speckit Handoff"; OpenSpec does not
duplicate them, and nothing here is an implementation step.

## 1. Governance record

- [x] 1.1 Proposal written: `proposal.md` adopts the packet's cache-disposal
  contract (`BA:1314-1337`) under the lane's rulings L-1 to L-9 and B-1 to B-9,
  names three departures from B-6 and one from B's list of modified
  requirements (CD-1 to CD-4) with the rest of its own decisions (CD-5 to
  CD-18), and puts four Open Questions before Brett Heap; verified by its
  Capabilities section accounting for every requirement of `project-clean` and
  `project-clean-review-safety`, canonical and change 1's ADDED alike.
- [ ] 1.2 Alignment resolved: the alignment review (stack-architect and
  qa-lead) runs on this draft and its findings are applied under the lane's
  rulings; verified by the table "Questions Resolved by the Alignment Review" in
  `proposal.md` and the review's comment on this change's pull request.
- [ ] 1.3 Council resolved: the council (product-advocate, systems-architect
  and adversary-engineer) runs on the aligned proposal, its VALID verdicts are
  applied to `proposal.md` and its NOTED constraints recorded in
  `clarifications.md`, which `design.md` then answers; verified by "Council
  Verdicts" in `proposal.md` and the council's comment on the pull request.
- [x] 1.4 Spec deltas and design written: `specs/project-clean/spec.md`
  modifies three requirements and adds one (34 scenarios: 5, 14, 6 and 9), and
  `specs/project-clean-review-safety/spec.md` modifies two and adds one (23
  scenarios: 6, 11 and 6), every scenario of each modified requirement's source
  text kept; `design.md` holds D1 to D14; verified by `grep -c '^#### Scenario'`
  on each delta and by `design.md`'s headings.
- [x] 1.5 Validation passes: `/usr/bin/openspec validate
  add-project-clean-cache-disposal --strict` reports the change valid,
  `/usr/bin/openspec validate --all --strict` passes every item, and
  `/usr/bin/openspec status --change add-project-clean-cache-disposal --json`
  shows every artifact done; verified by running the three commands on this
  branch after 1.4. The one INFO line, that the archive would refuse the
  MODIFIED block of "Clean bounds its Git work and reports omitted work" until
  change 1 is archived, is the expected state for a block written on a sister
  change.
- [ ] 1.6 Ratified by Brett Heap's word on this change's pull request, quoted
  with its link here, with the four Open Questions of `proposal.md` before him;
  verified by that quote. No implementation starts before it.

## 2. Before the Speckit handoff

- [ ] 2.1 Change 1 archived: `add-project-clean-all-safe` is archived after
  feature 004 merges, with draft PR #19 landed or closed first, and the two
  MODIFIED blocks written on PR #19's text ("Clean bounds its Git work and
  reports omitted work" and "Cleanup revalidates destructive actions")
  re-checked against the archived text and rewritten where it differs; verified
  by `openspec/specs/project-clean/spec.md` and
  `openspec/specs/project-clean-review-safety/spec.md` holding both
  requirements, and by `/usr/bin/openspec validate
  add-project-clean-cache-disposal --strict` reporting no archive refusal.
- [ ] 2.2 Change 2's equality clause settled (Open Questions): "Overview reuses
  the cleanup classifier and merge target" (APO/ov:381-386) excepts the rows
  whose ignored paths only `project clean` proves to be listed caches, or Brett
  Heap rules otherwise and the deltas follow; verified by the amended text, or
  the ruling, quoted here with its link.
- [ ] 2.3 Enumeration and stage measured (Open Questions, the caps): the cache
  enumeration's child and the cache stage timed warm and cold by change 1's
  protocol (its design D5) on a Linux filesystem path, at 512 entries per
  worktree and 4,096 per run, and the fit of `design.md` D4 reapplied; verified
  by the numbers posted on this change's pull request and summarised here; a
  cap the fit rejects is lowered in the deltas before the handoff, otherwise the
  caps stand as measured.

## 3. Landing and archive readiness

- [ ] 3.1 The realization PR is merged with green checks on all four CI jobs
  (`ubuntu-latest` and `macos-latest`, Python 3.10 and 3.12) and closes issue
  #24; verified by citing its merge sha here, from `gh pr view <number> --json
  mergeCommit,statusCheckRollup`.
- [ ] 3.2 The change is archived with `/opsx:archive` only after 3.1 and 2.1,
  and before `add-project-clean-branch-retirement` (#23) archives; verified by
  `/usr/bin/openspec validate --all --strict` passing after the archive.

## Speckit Handoff

Implementation is tracked exclusively in one Speckit feature, to be created by
`/speckit.specify` after ratification (1.6) and after section 2, from a local
`main` synced to `origin/main`. The feature covers the cache enumeration, the
plan's and the record's `cache_disposal`, the cache stage and the revalidation
of a cache target in `project` (`design.md` D1 to D13), the README paragraph,
and the tests of `design.md` D14.

- Feature identifier: to be created by /speckit.specify after 1.6 (006 or the
  next free number)
- Branch: to be created by /speckit.specify after 1.6 (006 or the next free
  number)
- Tasks: to be created by /speckit.specify after 1.6 (006 or the next free
  number), at specs/<that feature>/tasks.md by /speckit.tasks

`/opsx:apply` is not run until this section names exactly one feature and that
feature exists.
