Lane: openRepoProject-2

# Tasks

This is the governance and handoff record only. The implementation tasks live
in the one Speckit feature named under "Speckit Handoff"; OpenSpec does not
duplicate them.

## 1. Governance record

- [x] 1.1 Proposal written and revised: `proposal.md` adopts the design packet's overview contracts one by one, with "Decisions Taken by This Proposal", "Corrections to the Packet" and "Open Questions", and carries lane openRepoProject-3's final delta read (N-1 to N-6 and two LOW items) and the lead's rulings P6-1 to P6-6; verified by `openspec status --change add-project-overview --json` showing `proposal` done and by "Questions Resolved by the Alignment Review" naming each applied item.
- [x] 1.2 Alignment resolved: the alignment review's SA-1 to SA-18 and QA-1 to QA-21 are applied under the lead's rulings D-A to D-L and later rulings (`6204234`), SA-3 superseded by D-J; verified by the findings table in "Questions Resolved by the Alignment Review" and the resolution on PR #12.
- [x] 1.3 Council resolved: verdicts V1 to V12 are applied to `proposal.md` and the noted constraints N1 to N4 recorded in `clarifications.md` (`083fcd0`); verified by "Council Verdicts" and by `design.md`, which answers N1 to N4 with D1 to D4.
- [x] 1.4 Spec deltas and design written: `specs/project-overview/spec.md` adds twelve requirements with 61 scenarios, `specs/project-review-safety/spec.md` modifies "YAML decoding errors are structured refusals" with its existing scenario kept and the overview carve-out added, and `design.md` holds decisions D1 to D13 with the reconciliation list in D12; verified by `openspec status --change add-project-overview --json` showing every artifact done.
- [x] 1.5 Validation passes: `openspec validate add-project-overview --strict` and `openspec validate --all --strict` both pass; verified by their output, quoted in the message of the commit that adds these artifacts.
- [ ] 1.6 Ratified by Brett Heap's word, quoted with its link on PR #12, after `add-project-clean-all-safe` (PR #11) is ratified; verified by that quote. No implementation starts before it.

## 2. Before the handoff

- [x] 2.1 OQ-4 measurement recorded: measured on 2026-10-09 in py-bench (the WSL2 dev container, Linux 6.18, 32 threads, Git 2.43.0, a loaded shared host) on Linux filesystem paths, never a Windows drive, warm and cold, the cold cache made by `posix_fadvise` eviction plus a first-touch projection because `drop_caches` is not permitted there, and with drvfs not available on this workstation, so the degraded case is unmeasured; the one 4,096-directory root lists in 0.36 s warm and 2.6 s projected cold, against the 5 s per-root listing bound; `for-each-ref` on 1,000 branches takes 247 ms warm and 939 ms cold with loose refs, and on 10,000 loose refs 8.65 s cold, over the 5 s per-child bound, a `probe-timeout` and an incomplete run, never a wrong one; the status probe's median cost per child at four at once is 124 ms warm and 147 ms cold at 10,000 index entries, within the 150 ms margin rate, and 704 ms and 733 ms at 100,000, 4.7 times it and under the 5 s bound; the caps' worst case takes 48.3 s of the 60 s deadline, so the caps stand as measured, 128 candidates and 512 worktree rows (256 candidates fail at 65.6 s with loose refs, and 1,024 rows fail); the workstation survey found 213 repositories and 421 worktree rows, 37 of them eligible for `--all-safe` (17 with no gate, 20 limited by `target-cap`) and none under any withholding gate, and a default root of 219 candidates, so a default-root run here is incomplete with 91 omitted; the probe guard the survey needed became R-23, `-c protocol.allow=never` on every Git child, completed by R-25's six per-protocol `allow=never` pins and the removal of `GIT_ALLOW_PROTOCOL` by [E]'s scrub; each measured repository's eligible-row count is recorded beside its timing; verified by the results posted on PR #12 and by the spec delta's caps, confirmed and unchanged, before 3.1.
- [x] 2.2 Reconciled with change 1 after its phase 6: every item of `design.md` D12 ([E], [L], [G], [R], [P] and the fixture rewrite) was re-read against `add-project-clean-all-safe`'s spec deltas and design at `0b3c33d` and the moved items applied in `996a181`, then re-read against change 1's head at `4f2162b`, which carries R-15, and the lead's R-12, R-13 (b), R-14, R-15, R-16 and R-18 applied in the commits after `996a181`, then Brett Heap's ruling of 2026-10-09 on open question 1, which moves [L], mirrored in requirement 6 and its scenario in the commit titled 'Apply Brett Heap's ruling: local ancestry proof outranks remote-gone'; verified by D12 naming each item confirmed or changed and by `openspec validate add-project-overview --strict` passing afterwards.

## 3. Speckit handoff

- [ ] 3.1 Exactly one Speckit feature owns the implementation, `005-project-overview`, created by `/speckit.specify` after 1.6, 2.1 and 2.2 and after feature 004 (change 1's) merges, from the `main` of that day; verified when "Speckit Handoff" below records it as created, filled in once.
- [ ] 3.2 `/opsx:apply` is not run until "Speckit Handoff" names exactly one created feature; verified by reading that section before the first `/opsx:apply`.

## Speckit Handoff

Implementation is tracked exclusively in one Speckit feature, to be created by
`/speckit.specify` after ratification and after feature 004 merges. The
feature covers the `project overview` subcommand of `specs/project-overview/spec.md`,
the `project-review-safety` carve-out, the README section and the tests of
`design.md` D13.

Numbering: after `002-triad-first-project-new` (merged by PR #8),
`003-parent-obstacle-wording` is lane openRepoProject-1's feature (PR #17) and
`004-project-clean-all-safe` is change 1's, so this change's feature is
`005-project-overview`.

- Feature identifier: 005-project-overview (to be created by `/speckit.specify`)
- Branch: 005-project-overview
- Tasks: specs/005-project-overview/tasks.md (reserved; created by `/speckit.tasks`)

`/opsx:apply` is not run until this section names exactly one created feature.
