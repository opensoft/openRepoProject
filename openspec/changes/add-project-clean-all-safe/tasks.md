Lane: openRepoProject-2

# Tasks

This is the governance and handoff record only. The implementation tasks will
live in the one Speckit feature named under "Speckit Handoff"; OpenSpec does not
duplicate them, and nothing here is an implementation step.

## 1. Governance record

- [x] 1.1 Proposal written: `proposal.md` adopts, narrows or corrects the
  project maintenance design packet for the batch (`fed64d4`), restated against
  `main` at `7a9134b` (`0669a20`); verified by its Capabilities section
  accounting for every requirement of `project-clean`,
  `project-clean-review-safety` and `project-command`.
- [x] 1.2 Alignment resolved: the SA and QA findings and the lead's rulings D-A
  to D-AF are applied (`0ed2f59`, then `ea9c73b`), lane 3's delta read M1 to M7
  with the ceiling precision (`ba9f7c3`, `4b0c149`), and the lead's V2 amended
  and R-4, R-8, R-9, R-11 to R-15, R-17 and R-19 (`9ea2f02`, `0b3c33d`,
  `d6aaa9a`, the commit that anchors the reflog test on the creation entry,
  R-15, `4f2162b`, R-17, and the commit that scopes the digest rule to the band
  above 128 rows, R-19); verified by the table "Questions Resolved by the
  Alignment Review" in `proposal.md` and the later-rulings list under it, which
  name the section each ruling edited.
- [x] 1.3 Council resolved: every concern is VALID, none dismissed, the verdicts
  V1 to V12 applied to `proposal.md` (`ea9c73b`) and the five NOTED constraints
  recorded as N1 to N5 in `clarifications.md` (`1d4ed5b`); verified by
  `design.md`, whose D1 to D5 answer N1 to N5 one for one.
- [x] 1.4 Spec deltas and design written: `specs/project-clean/spec.md` modifies
  five requirements and adds six, `specs/project-clean-review-safety/spec.md`
  modifies two and adds one, and `specs/project-command/spec.md` modifies two
  and adds one, every canonical scenario of each modified requirement kept;
  `design.md` holds D1 to D20, mapping the packet's 35 validation scenarios to
  the deltas (D20); verified by the scenario counts in the commit that adds
  them.
- [x] 1.5 Validation passes: `openspec validate add-project-clean-all-safe
  --strict` reports the change valid, `openspec validate --all --strict` passes
  every item, and `openspec status --change add-project-clean-all-safe` shows
  every artifact done; verified by running the three commands on this branch
  after 1.4.
- [ ] 1.6 Ratified by Brett Heap's word on PR #11, quoted with its link here,
  the V5 deferral and the two open questions of `design.md` before him; verified
  by that quote. No implementation starts before it.

## 2. Before the Speckit handoff

- [ ] 2.1 OQ-4 measured by the protocol of `design.md` D5 (clarifications N5):
  the combined status probe and `for-each-ref` timed warm and cold, the cold
  method recorded, on a Linux filesystem path against indexes of about 10,000
  and 100,000 entries and about 1,000 branches; the removal of a 20,000-file
  worktree timed against the 5 s floor and the 300 s ceiling; drvfs measured the
  same way and recorded as a degraded case, never used for the fit; the fit of
  BA:729-735 reapplied with the measured costs; and, for every repository under
  the projects directories of this workstation, the rows per gate outcome beside
  the timings, among them the rows excluded only for `reflog-unavailable`.
  Verified by the numbers posted on PR #11 and summarised here; a cap the fit
  rejects is lowered in the deltas before the handoff, otherwise the deltas'
  provisional caps stand as measured.
- [ ] 2.2 The Git 2.36 floor verified by the approach of `design.md` D17: each
  behaviour in its table checked on a pinned Git 2.36 build in a scratch
  directory, or by a CI job, against Git 2.43's output; verified by the results
  posted on PR #11. If any behaviour differs, the floor is raised to the lowest
  version verified and the deltas' Git version text and refusal are edited
  before the handoff.
- [ ] 2.3 Dependent change noted: `add-project-overview` (issue #10, PR #12)
  depends on this change and reconciles its deltas against this change's final
  requirement headers after this change lands, then is ratified after it;
  verified by that change's own governance record, never by a box here being
  ticked for it.

## Speckit Handoff

Implementation is tracked exclusively in one Speckit feature, to be created by
`/speckit.specify` after ratification (1.6) and after 2.1 and 2.2, from a local
`main` synced to `origin/main`. Numbering is sequential:
`002-triad-first-project-new` is lane openRepoProject-1's feature, merged by PR
#8.

- Feature identifier: 003-project-clean-all-safe (to be created by
  /speckit.specify after ratification)
- Branch: 003-project-clean-all-safe
- Tasks: specs/003-project-clean-all-safe/tasks.md (reserved; created by
  /speckit.tasks)

`/opsx:apply` is not run until this section names exactly one feature and that
feature exists.
