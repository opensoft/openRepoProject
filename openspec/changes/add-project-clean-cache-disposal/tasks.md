Lane: openRepoProject-5

# Tasks

This is the governance and handoff record only. The implementation tasks will
live in the one Speckit feature named under "Speckit Handoff"; OpenSpec does not
duplicate them, and nothing here is an implementation step.

## 1. Governance record

- [x] 1.1 Proposal written: `proposal.md` adopts the packet's cache-disposal
  contract (`BA:1314-1337`) under the lane's rulings L-1 to L-15 and B-1 to
  B-15, names three departures from B-6 as first written, which B-11 accepted,
  and one from B's list of modified requirements (CD-1 to CD-4) with the rest
  of its own decisions (CD-5 to CD-18), and puts three Open Questions before
  Brett Heap; verified by its Capabilities section accounting for every
  requirement of `project-clean` and `project-clean-review-safety`, canonical
  and change 1's ADDED alike, and for change 2's `project-overview`.
- [x] 1.2 Alignment resolved: the alignment review (stack-architect and
  qa-lead) ran on `7290100`, and its findings are applied under the lane's
  rulings of 2026-10-11 and 2026-10-18; verified by the table "Questions
  Resolved by the Alignment Review" in `proposal.md`, one row per finding id
  with its severity, the ruling and the section edited, and one row per lane
  ruling that answered the review's five GAPs.
- [ ] 1.3 Council resolved: the council (product-advocate, systems-architect
  and adversary-engineer) runs on the aligned proposal, its VALID verdicts are
  applied to `proposal.md` and its NOTED constraints recorded in
  `clarifications.md`, which `design.md` then answers; verified by "Council
  Verdicts" in `proposal.md` and the council's comment on the pull request.
- [x] 1.4 Spec deltas and design written: `specs/project-clean/spec.md`
  modifies five requirements and adds one (54 scenarios: 5, 14, 11, 6, 8 and
  10), and `specs/project-clean-review-safety/spec.md` modifies three and adds
  one (26 scenarios: 6, 11, 4 and 5), every scenario of each modified
  requirement's source text kept by name and byte-exact except "Ignored-file
  bound" and "A merged worktree has ignored local files", whose ignored files
  are now named as not caches (proposal, Capabilities);
  `specs/project-overview/spec.md` modifies one requirement of change 2 (8
  scenarios: its 7 byte-exact and 1 added) and is committed once lane
  openRepoProject-4 agrees its diff (2.2); `design.md` holds D1 to D14;
  verified by `grep -c '^#### Scenario'` on each delta, by a script that
  compares every scenario of each MODIFIED block with its source text, and by
  `design.md`'s headings.
- [x] 1.5 Validation passes: `/usr/bin/openspec validate
  add-project-clean-cache-disposal --strict` reports the change valid,
  `/usr/bin/openspec validate --all --strict` passes every item, and
  `/usr/bin/openspec status --change add-project-clean-cache-disposal --json`
  shows every artifact done; verified by running the three commands on this
  branch after 1.4. The INFO lines, that the archive would refuse a delta
  whose MODIFIED requirement change 1 or change 2 adds until that change is
  archived, are the expected state for blocks written on sister changes.
- [ ] 1.6 Ratified by Brett Heap's word on this change's pull request, quoted
  with its link here, with the three Open Questions of `proposal.md` before
  him; verified by that quote. No implementation starts before it.

## 2. Before the Speckit handoff

- [ ] 2.1 Change 1 archived: `add-project-clean-all-safe` is archived after
  feature 004 merges, with draft PR #19 landed or closed first, and the two
  MODIFIED blocks written on PR #19's text ("Clean bounds its Git work and
  reports omitted work" and "Cleanup revalidates destructive actions")
  re-checked against the archived text and rewritten where it differs, as every
  other block written on change 1's text is; verified by
  `openspec/specs/project-clean/spec.md` and
  `openspec/specs/project-clean-review-safety/spec.md` holding every requirement
  this change modifies, and by `/usr/bin/openspec validate
  add-project-clean-cache-disposal --strict` reporting no archive refusal for
  those two deltas.
- [ ] 2.2 The overview exception agreed (B-14): lane openRepoProject-4, owner
  of change 2 and feature 005, agrees the diff of
  `specs/project-overview/spec.md`, which carries change 2's "Overview reuses
  the cleanup classifier and merge target" (APO/ov:358) whole with lane 4's two
  sentences appended to its equality clause and one scenario, and the delta is
  then committed on this branch; verified by lane 4's agreement quoted here
  with its link and by the commit's sha.
- [ ] 2.3 Enumeration and stage measured (Open Questions, the caps): the cache
  enumeration's child and the cache stage timed warm and cold by change 1's
  protocol (its design D5) on a Linux filesystem path, at 512 entries per
  worktree and 4,096 per run, and the fit of `design.md` D4 reapplied; verified
  by the numbers posted on this change's pull request and summarised here; a
  cap the fit rejects is lowered in the deltas before the handoff, otherwise the
  caps stand as measured.

## 3. Landing and archive readiness

- [ ] 3.1 The realization PR is merged with green checks on CI's two jobs,
  `test (3.10)` and `test (3.12)` on `ubuntu-latest`, and closes issue #24;
  verified by citing its merge sha here, from `gh pr view <number> --json
  mergeCommit,statusCheckRollup`.
- [ ] 3.2 The change is archived with `/opsx:archive` only after 3.1, 2.1 and
  change 2's archive (B-14), and before `add-project-clean-branch-retirement`
  (#23) archives; verified by `/usr/bin/openspec validate --all --strict`
  passing after the archive.

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
