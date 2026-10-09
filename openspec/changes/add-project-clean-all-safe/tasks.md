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
  and R-4, R-8, R-9, R-11 to R-15, R-17, R-19 and R-22 to R-25 (`9ea2f02`,
  `0b3c33d`, `d6aaa9a`, the commit that anchors the reflog test on the creation
  entry, R-15, `4f2162b`, R-17, the commit that scopes the digest rule to the
  band above 128 rows, R-19, the commit titled 'Add the reappearing-upstream
  revalidation scenario (R-22)', the commit titled 'Pin protocol.allow=never on
  every Git child against lazy fetches (R-23)', and the commit titled 'Tick task
  2.1 with the OQ-4 measurement and close the lazy-fetch gap (R-24, R-25)'), and
  Brett Heap's ruling of
  2026-10-09 on open question 1, local ancestry outranking `remote-gone` for
  worktree rows (the commit titled 'Apply Brett Heap's ruling: local ancestry
  proof outranks remote-gone'); verified by the table "Questions Resolved by the
  Alignment Review" in `proposal.md` and the later-rulings list under it, which
  name the section each ruling edited.
- [x] 1.3 Council resolved: every concern is VALID, none dismissed, the verdicts
  V1 to V12 applied to `proposal.md` (`ea9c73b`) and the five NOTED constraints
  recorded as N1 to N5 in `clarifications.md` (`1d4ed5b`); verified by
  `design.md`, whose D1 to D5 answer N1 to N5 one for one.
- [x] 1.4 Spec deltas and design written: `specs/project-clean/spec.md` modifies
  five requirements and adds six (65 scenarios),
  `specs/project-clean-review-safety/spec.md` modifies two and adds one (18
  scenarios, the last added under R-22), and `specs/project-command/spec.md`
  modifies two and adds one (17 scenarios, the last added under R-23), every
  canonical scenario of each modified requirement kept; `design.md` holds D1 to
  D20, mapping the packet's 35 validation scenarios to the deltas (D20);
  verified by the scenario counts in the commit that adds them.
- [x] 1.5 Validation passes: `openspec validate add-project-clean-all-safe
  --strict` reports the change valid, `openspec validate --all --strict` passes
  every item, and `openspec status --change add-project-clean-all-safe` shows
  every artifact done; verified by running the three commands on this branch
  after 1.4.
- [x] 1.6 Ratified by Brett Heap's word on PR #11, quoted with its link here,
  the V5 deferral and the squash-merge open question of `design.md` before him;
  verified by that quote. No implementation starts before it. Done: his word to
  lane openRepoProject-2 on 2026-10-09, verbatim: "ratify, merge #11 and run the
  runbook".

## 2. Before the Speckit handoff

- [x] 2.1 OQ-4 measured by the protocol of `design.md` D5 (clarifications N5):
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
  caps stand as measured. Done: measured 2026-10-09 in the `py-bench` dev
  container on WSL2 (Git 2.43.0, Python 3.12.3; fixtures on the container's
  overlayfs, the real repositories on ext4), the cold cache by `sync` and
  per-file eviction (`posix_fadvise`, the mechanism of `vmtouch -e`) confirmed
  with `mincore`, since `drop_caches` is impossible in the container, and drvfs
  not available, so unmeasured. Medians, warm / cold: the status probe 42-49 /
  38-63 ms at 10,000 entries and 215-232 / 244-248 ms at 100,000; `for-each-ref`
  at 1,000 branches 108-112 / 121 ms packed and 240 / 838 ms loose; the merged
  set 17-48 ms; the 20,000-file removal 0.66 / 0.72 s, at worst 14.1 s under CPU
  saturation (low load leaves 3.6 to 4.3 s under the 5 s floor, and the worst
  case is 21 times under the 300 s ceiling). The fit of BA:729-735 rejects no
  cap: at 128 rows and 16 targets the 16th removal spawns at 23.6 s with 26.4 s
  left and the worst case ends at 24.3 s; 256 report rows take 19.9 s; and the
  64 s run bound, the 15 s per child, `min(5 s, remaining)`, the 5 s floor and
  the 300 s ceiling all hold. Two degraded cases are recorded as risks in
  `design.md`, not as cap changes: rows of 100,000-entry indexes (the rule would
  give 64 rows) and CPU saturation at load 165 (a 128-row plan takes 77 s); a
  plan then goes incomplete, never unsafe. The survey covers 355 repositories,
  296 resolving, with 561 rows, and selects 17; per gate: main-worktree 296,
  locked-worktree 1, stale-worktree 7, dirty 25, ignored-local-files 102,
  detached 11, unpublished 23, remote-gone 2 (unmerged), remote-ahead 5,
  unpushed 1, pushed-unmerged 51, deferred-target-cap 4, contains-submodule 16,
  and 0 for unsupported-path-bytes, registration-mismatch, protected-default,
  inspection-error, review-required, diverged, merged-current,
  hidden-local-state, `unstarted-branch` and `reflog-unavailable` (all 37 rows
  that reach the reflog gate show a movement). In Opensoft-Tenant, the V5
  deferral's motivating repository, 20 rows pass every gate before
  `deferred-target-cap` and all are `contains-submodule` after it, so it yields
  no removable row each run and its deferred count never drains (design Risks,
  R-24). Results posted on PR #11; the caps stand as measured.
- [x] 2.2 The Git 2.36 floor verified by the approach of `design.md` D17: each
  behaviour in its table checked on a pinned Git 2.36 build in a scratch
  directory, or by a CI job, against Git 2.43's output; verified by the results
  posted on PR #11. If any behaviour differs, the floor is raised to the lowest
  version verified and the deltas' Git version text and refusal are edited
  before the handoff. Done: Git 2.36.6, 2.40.4 and 2.43.0 compared on 75
  captures; rows 1 to 6 identical; row 7's extra variable,
  `GIT_INTERNAL_SUPER_PREFIX`, scrubbed under R-21, the floor kept at 2.36
  rather than raised to 2.40 (a departure listed in `proposal.md`, open to
  Brett Heap at ratification); results posted on PR #11 on 2026-10-09.
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
#8, and `003-parent-obstacle-wording` is lane openRepoProject-1's feature, PR
#17, so this change's feature is the next free number, 004.

- Feature identifier: 004-project-clean-all-safe (to be created by
  /speckit.specify after ratification)
- Branch: 004-project-clean-all-safe
- Tasks: specs/004-project-clean-all-safe/tasks.md (reserved; created by
  /speckit.tasks)

`/opsx:apply` is not run until this section names exactly one feature and that
feature exists.
