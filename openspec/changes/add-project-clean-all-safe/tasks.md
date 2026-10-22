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
  proof outranks remote-gone'), and Brett Heap's ruling Q9 B of 2026-10-21,
  given through lane openRepoProject-4's spec 005 clarify round, the three
  trace2 variables at `0` on every Git child and the fourteen trace variables
  in the scrub (the commit titled 'Pin trace2 and scrub the trace names on
  every Git child (Q9 B)'), and Brett Heap's rulings of 2026-10-21 on lane
  openRepoProject-3's recommendations LQ-10 to LQ-15, each in its own commit
  titled 'Amend change 1 for LQ-<n> (Brett Heap, 2026-10-21): ...': LQ-15, a
  relative configuration path refused before any Git child; LQ-10, the stat
  pins `core.trustctime=true` and `core.checkStat=default`; LQ-12, the push
  child's scrub on every owner tool of `update --apply`; LQ-11, a redirected
  effective work tree read as `registration-mismatch`; LQ-13, the gate
  `worktree-only-commits` and its revalidation; LQ-14, the gate
  `operation-in-progress` and its revalidation; lane openRepoProject-3's W8
  read of LQ-15 (the commit titled 'Amend change 1 for LQ-15: lane 3's W8
  read'); and its W10 read of LQ-12 and LQ-13, under the lead's R-124 and
  R-127 (the commit titled 'Amend change 1 for LQ-13 and LQ-14: lane 3's W10
  read (R-124)'); and its W9 read of LQ-10 and LQ-11, under the lead's R-125
  (the commit titled 'Amend change 1 for LQ-10 and LQ-11: lane 3's W9 read');
  and its W14 read of LQ-14, under the lead's R-126 (the commit titled 'Amend
  change 1 for LQ-14: lane 3's W14 read (R-126)'); and its W21 read with the
  lead's R-146 and R-147 (the commit titled 'Amend change 1: lane 3's W21
  LOWs, the Git cites and two refusal scenarios (R-146, R-147)'); and its W26
  read with the lead's R-171 (the commit titled 'Amend change 1: lane 3's W26
  read and R-171's revalidation rule'); and the fit restated under the lead's
  R-178 (the commit titled 'Amend change 1: restate D14's fit with the
  measured counts, and name LQ-20 (R-178)'); and lane 3's W31 read of that round
  and of the fit, under the lead's R-187 and R-190 (the commit titled 'Amend
  change 1: lane 3's W31 read, the fit on three bases and LQ-20 (R-187,
  R-190)'); and its W36 read of round (c), with its W32 read of LQ-14 and the
  lead's R-200, R-207 and R-208 (the commit titled 'Amend change 1: lane 3's W36
  read, LQ-20's options costed, and filesystem reads at revalidation (R-207,
  R-208)'); and its W38 read of round (d), under the lead's R-213 and R-216 (the
  commit titled 'Amend change 1: lane 3's W38 read of round (d) (R-213,
  R-216)'); and Brett Heap's ruling of 2026-10-22 on LQ-20, its step (i), with
  that step's measurement, lane 3's W42 read of round (e) and the three
  departures of lane 3's W53 ledger, under the lead's R-236 and R-245 (the
  commit titled 'Amend change 1: LQ-20 resolved by measurement, lane 3's W42
  read and three departures (R-236, R-245)'); and lane 3's W52 read of next
  steps that Git refuses, under the lead's R-248, its F-1, and its F-2 for a
  locked row, left for Brett Heap, who ruled both on 2026-10-22 (the commit
  titled 'Amend change 1: lane 3's W52 read, next steps that Git refuses
  (R-248)'); and the shortening of F-7's clause, under the lead's R-252 (the
  commit titled 'Amend change 1: shorten the F-7 submodule clause (R-252)'); and
  lane 3's W59 read of rounds (f) and (g), under the lead's R-253 (the commit
  titled 'Amend change 1: lane 3's W59 read of rounds (f) and (g) (R-253)'); and
  round (h), lane 2's open points after writer E under the lead's R-258 to
  R-260, with lane 5's RI-3 and O-1, lane 3's W64 read of rounds (g2) and (g3),
  and Brett Heap's ruling of 2026-10-22, "F-2: yes; F-1: prune-then-delete; O-1:
  deadline-exceeded" (R-263) (the commits whose titles begin 'Amend change 1:
  round (h)', the first titled 'Amend change 1: round (h) text, Brett Heap's
  F-2, F-1 and O-1, and lane 2's open points (R-258 to R-263)'); and round (i),
  round (h)'s open point, the message of a redirected main worktree's refusal,
  under the lead's R-271, with lane 4's finding on D6's identity probe and lane
  3's W73 M-1, a `.git` the rescan cannot read, under the lead's R-284 (the
  commits whose titles begin 'Amend change 1: round (i)', the first titled
  'Amend change 1: round (i), name the redirect in a redirected main worktree's
  refusal (R-271)'); and round (j), lane 3's W70 read of round (h), under the
  lead's R-285, R-287 and R-291, with LQ-11's work-tree probe read as one path,
  and Brett Heap's confirmation of R-284 on 2026-10-22, "R-284: yes" (R-290)
  (the commit titled 'Amend change 1: round (j), lane 3's W70 read of round (h)
  and LQ-11's one-path probe (R-285, R-287, R-290, R-291)'); verified by the
  table "Questions Resolved by the Alignment Review" in `proposal.md` and the
  later-rulings list under it, which name the section each ruling edited.
- [x] 1.3 Council resolved: every concern is VALID, none dismissed, the verdicts
  V1 to V12 applied to `proposal.md` (`ea9c73b`) and the five NOTED constraints
  recorded as N1 to N5 in `clarifications.md` (`1d4ed5b`); verified by
  `design.md`, whose D1 to D5 answer N1 to N5 one for one.
- [x] 1.4 Spec deltas and design written: `specs/project-clean/spec.md` modifies
  five requirements and adds six (71 scenarios, one added under each of Brett
  Heap's rulings LQ-15, LQ-13 and LQ-14, one under the lead's R-126 and two
  under R-147), `specs/project-clean-review-safety/spec.md` modifies two and
  adds one (22 scenarios, one added under R-22, one under each of LQ-13 and
  LQ-14, one under R-146 and one under R-190), and
  `specs/project-command/spec.md` modifies two and adds one (24 scenarios, of
  which the push-child exception added one, Brett Heap's rulings Q9 B, LQ-15,
  LQ-10, LQ-12 and LQ-11 one each, and the lead's R-125 one), every canonical
  scenario of each modified requirement kept; `design.md` holds D1 to D22,
  mapping the packet's 35 validation scenarios to the deltas (D20), D21 and D22
  added under LQ-13 and LQ-14; verified by the scenario counts in the commit
  that adds them.
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
- [ ] 1.7 The push-child exception ratified by Brett Heap's word on the pull
  request that amends this change, quoted with its link here, the `design.md`
  Open Questions entry before him; verified by that quote. Feature 004 plans
  under the exception, and a different ruling edits this amendment and that
  plan. To fill when he rules: his words, verbatim, and the link to them.

## 2. Before the Speckit handoff

- [x] 2.1 OQ-4 measured by the protocol of `design.md` D5 (clarifications N5):
  the combined status probe and `for-each-ref` timed warm and cold, the cold
  method recorded, on a Linux filesystem path against indexes of about 10,000
  and 100,000 entries and about 1,000 branches; the removal of a 20,000-file
  worktree timed against the 5 s floor and the 300 s ceiling; drvfs measured the
  same way and recorded as a degraded case, never used for the fit; the fit of
  BA:729-735 at da33d92 reapplied with the measured costs; and, for every
  repository under the projects directories of this workstation, the rows per
  gate outcome beside the timings, among them the rows excluded only for
  `reflog-unavailable`. Verified by the numbers posted on PR #11 and summarised
  here; a cap the fit rejects is lowered in the deltas before the handoff,
  otherwise the deltas' caps stand as measured. Done: measured 2026-10-09 in the
  `py-bench` dev container on WSL2 (Git 2.43.0, Python 3.12.3; fixtures on the
  container's overlayfs, the real repositories on ext4), the cold cache by
  `sync` and per-file eviction (`posix_fadvise`, the mechanism of `vmtouch -e`)
  confirmed with `mincore`, since `drop_caches` is impossible in the container,
  and drvfs not available, so unmeasured. Medians, warm / cold: the status probe
  42-49 / 38-63 ms at 10,000 entries and 215-232 / 244-248 ms at 100,000;
  `for-each-ref` at 1,000 branches 108-112 / 121 ms packed and 240 / 838 ms
  loose; the merged set 17-48 ms; the 20,000-file removal 0.66 / 0.72 s, at
  worst 14.1 s under CPU saturation (low load leaves 3.6 to 4.3 s under the 5 s
  floor, and the worst case is 21 times under the 300 s ceiling). The fit of
  BA:729-735 at da33d92 rejects no cap: at 128 rows and 16 targets the 16th
  removal spawns at 23.6 s with 26.4 s left and the worst case ends at 24.3 s;
  256 report rows take 19.9 s; and the 64 s run bound, the 15 s per child,
  `min(5 s, remaining)`, the 5 s floor and the 300 s ceiling all hold. Two
  degraded cases are recorded as risks in `design.md`, not as cap changes: rows
  of 100,000-entry indexes (the rule would give 64 rows) and CPU saturation at
  load 165 (a 128-row plan takes 77 s); a plan then goes incomplete, never
  unsafe. The survey covers 355 repositories, 296 resolving, with 561 rows, and
  selects 17; per gate: main-worktree 296, locked-worktree 1, stale-worktree 7,
  dirty 25, ignored-local-files 102, detached 11, unpublished 23, remote-gone 2
  (unmerged), remote-ahead 5, unpushed 1, pushed-unmerged 51,
  deferred-target-cap 4, contains-submodule 16, and 0 for
  unsupported-path-bytes, registration-mismatch, protected-default,
  inspection-error, review-required, diverged, merged-current,
  hidden-local-state, `unstarted-branch` and `reflog-unavailable` (all 37 rows
  that reach the reflog gate show a movement). In Opensoft-Tenant, the V5
  deferral's motivating repository, 20 rows pass every gate before
  `deferred-target-cap` and all are `contains-submodule` after it, so it yields
  no removable row each run and its deferred count never drains (design Risks,
  R-24). Results posted on PR #11; the caps stand as measured. LQ-20's step (i)
  (Brett Heap, 2026-10-22; the lead's R-236) measured, by the same protocol, the
  two children that LQ-11 and LQ-13 added, in the same container, on a
  10,001-file fixture with `extensions.worktreeConfig` true, eight linked
  worktrees, 1,000 branches, 1,991 loose refs and 9,940 commits, at a 1-minute
  load of 15 to 21, 40 to 48 runs a case, the larger median of two runs:
  medians, warm / cold, the work-tree probe 5.8 / 9.8 ms and the `rev-list` over
  the whole history 106.9 / 686 ms, neither reading the index; with them the fit
  still rejects no cap, the 16th removal spawning at 30.0 s with 20.0 s left at
  128 rows and 16 targets where `extensions.worktreeConfig` is true (37.7 s with
  20,000-file removals).
- [x] 2.2 The Git 2.36 floor verified by the approach of `design.md` D17: each
  behaviour in its table checked on a pinned Git 2.36 build in a scratch
  directory, or by a CI job, against Git 2.43's output; verified by the results
  posted on PR #11. If any behaviour differs, the floor is raised to the lowest
  version verified and the deltas' Git version text and refusal are edited
  before the handoff. Done: Git 2.36.6, 2.40.4 and 2.43.0 compared on 75
  captures; rows 1 to 6 identical; row 7's extra variable,
  `GIT_INTERNAL_SUPER_PREFIX`, scrubbed under R-21, the floor kept at 2.36
  rather than raised to 2.40 (a departure listed in `proposal.md`, ratified with
  the merge of PR #11); results posted on PR #11 on 2026-10-09.
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
