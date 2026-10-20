Lane: openRepoProject-4

# Specification Quality Checklist: Project overview

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-10-11
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

- Final state: 16 of 16 items pass after 2 validation iterations (of 3
  allowed). The spec was first read against the change and feature 004 by
  a separate read-only review of the WIP at `3d67394` (19 findings), whose
  valid findings were applied in `c1e7e22` before this validation.
- Iteration 1 failed three items, each fixed in the spec:
  - "All functional requirements have clear acceptance criteria": some
    requirements, or parts of them, are exercised by no delta scenario
    (FR-004's candidates that are not family holders, FR-010, FR-020's
    `estimated` count, FR-021's `refused` and `undecodable-output` codes,
    FR-022's 200-character message bound, FR-037's order), while FR-049
    required tests only per delta scenario. FR-049 now requires at least
    one test for each such requirement, named in the feature's
    traceability record.
  - "Requirements are testable and unambiguous": five requirements used the
    construction "no X MUST ...", readable as either a prohibition or an
    empty obligation (FR-007, FR-012, FR-014, FR-044, FR-049); each now
    reads "MUST NOT".
  - "Success criteria are measurable": SC-004 required every ungated
    `--all-safe` worktree to be selected or index-excluded in the preview
    it leads to, which a preview cut by its own deadline cannot meet, and
    the change says the overview does not predict that cut (proposal,
    "Dependencies and Sequencing"). SC-004 now excludes that case.
- Iteration 2: every item passes. Checks run for it: no function or module
  name of the implementation, no [NEEDS CLARIFICATION] marker, no TODO or
  vague adjective, and no character outside ASCII in `spec.md`; every
  delta scenario and requirement mapped (13 of 13 requirements, 63 of 63
  scenarios, by script against the delta headers); every `C-n`, `FR-n`,
  `EC-n` and `USn sk` cited exists.
- "Written for non-technical stakeholders" and "Success criteria are
  technology-agnostic" pass only on the deviation recorded under the spec's
  Assumptions, as in features 002 to 004: the ratified deltas fix flags,
  codes, JSON fields, Git settings, standard streams and exit statuses as
  behaviour, so the requirements and criteria name them, and the readers
  are the people who own, review and use `project`. A reader without that
  background will find the requirements dense; the user stories carry the
  plain account.
- "No implementation details" passes on the same deviation: the spec names
  no language, function, module or file of the implementation, but it does
  state behaviour the deltas fix in mechanism terms (process groups, the
  streamed ref listing, the two collection phases, the counting `git`
  wrapper of the tests).
- "No [NEEDS CLARIFICATION] markers remain" holds because the spec follows
  the ratified change; five genuinely open questions are in
  `clarify-questions.md` for Brett Heap, unanswered, and none alters a
  requirement until he answers. One point is left to the plan on purpose:
  where a repository-level finding sorts among a row's findings
  (Assumptions).
- Lane openRepoProject-2's binding flags were checked: the order departure
  is recorded with the time of Brett Heap's word; no test needs a running
  filesystem monitor (FR-049, C-6); every Git child carries the seven pins
  and the seventeen-name scrub, with no push child and so no R-28
  exception (FR-016, C-5); local ancestry outranks `remote-gone` (FR-028)
  and squash merges (LQ-2) are deferred to a follow-on change (EC-013,
  C-8); the MODIFIED capability is `project-review-safety` (C-7).
- Feature 004's citations were re-pinned from `dd923ee` to `5a71f83` after
  this validation, on lane openRepoProject-2's word relayed by the lead.
  Every feature 004 term the spec uses was re-checked there: no shared term
  was renamed, the cited FR-009, FR-062 and FR-067 and the contract's "Git
  children" section are unchanged, and `prunable`, restored there, is
  already in the overview's worktree row. The new "Child handle" entity is
  named under Dependencies only, and the two reflog outcomes feature 004 now
  reads more narrowly than the changes are recorded there for the plan to
  reconcile (both removed at the re-pin to `66d60b6`, next note).
- 2026-10-18: `main` at `e9d6711` merged into the branch (#31,
  `single-repository.yaml`; #32, CI on Linux only), and feature 004's
  citations re-pinned from `5a71f83` to `66d60b6` after diffing its
  `spec.md`, `data-model.md`, `contracts/project-clean.md` and `tasks.md`
  between them. The CI change reaches the spec's Runtime and CI dependency,
  EC-017, FR-049 and the citation notes of its header and Assumptions; no
  line of `README.md` or the workflow is cited. On lane openRepoProject-2's ruling that both
  reflog readings are feature 004's to settle, the "Readings to reconcile"
  dependency is gone, FR-033 and EC-009 follow the delta with the 65,536-byte
  boundary of ruling R-33, recorded as C-22 in a session that answers none of
  `clarify-questions.md`, and FR-049 names a test for that boundary. The
  child-handle kinds read `probe`, `removal` and `delegate`. Re-validation:
  16 of 16 items pass, with the checks of iteration 2 re-run by script on the
  edited spec.
- 2026-10-19: feature 004's citations re-pinned from `66d60b6` to `d1e7c56`
  (lane openRepoProject-2's doc round, rulings R-32 to R-36) after diffing
  its `spec.md`, `plan.md`, `data-model.md`, `research.md` and
  `contracts/project-clean.md` between them. Here, C-22 now records that
  feature 004's data model carries R-33's 65,536-byte boundary while its
  EC-005 still reads "over 64 KiB", for lane openRepoProject-2 to align; C-33
  now records that feature 004 reads `ENOENT` or `ENOTDIR` for `present:
  false` and resolves a relative `core.worktree` against the git directory
  (R-36), so neither is a difference on its side; the header and Assumptions
  say what its branch holds (code at `c4ed704` for T001 to T017, T022 and
  T023, among them its five incremental parsers and its child handle, but not
  yet the driver, and none of it on `main`) in place of "only empty regions
  and imports"; and the Runtime and CI dependency names its two `test` jobs
  and `git-floor` as its plan's "CI shape" does (R-35). The other citations
  read the same at both pins. Re-validation: 16 of 16 items pass, with the
  checks of iteration 2 re-run by script on the edited spec.
- 2026-10-19: three read-only reviews of `3d28710` (fidelity to change 2,
  F-1 to F-20; consistency with feature 004, C-1 to C-13; adversarial, A-1
  to A-25) were applied. Points the change's text, or change 1's shared
  evidence model, settles are recorded as C-23 to C-36 and folded into the
  requirements, stories, edge cases (EC-022 to EC-025) and criteria; C-22
  now rests on change 2's own text, with R-33 cited only as concurring for
  feature 004. Points the change leaves open are Q6 to Q13 of
  `clarify-questions.md`, unanswered, each recorded as an open edge case or
  a cited question where the spec meets it. Re-validation: 16 of 16 items
  pass; "Requirements are testable and unambiguous" and "Success criteria
  are measurable" were re-read against the review findings (SC-009,
  SC-012 and SC-013 rewritten, FR-049's test rules made exact).
- 2026-10-19: feature 004 re-pinned from `d1e7c56` to `acc822e` (doc round
  3, rulings R-39 to R-47) and then to `5a02c1a` (doc round 4, R-47 and
  R-48), after diffing its `spec.md`, `plan.md`, `data-model.md`,
  `research.md`, `contracts/project-clean.md`, `quickstart.md` and
  `tasks.md` between them; its branch's head, `fe91f2c`, changes only task
  ticks in them. Here, C-22 now records that feature 004's EC-005 reads
  R-33's 65,536-byte boundary too, so nothing is left there for lane
  openRepoProject-2 to align; the header and Assumptions say what that head
  holds (code for T001 to T026, T034 and T035, the driver and the
  `Invocation` state among them, and not yet the evidence model, none of it
  on `main`); the
  Dependencies name its `Invocation` entity (R-44, R-47), its command-neutral
  `git-too-old` and `git-unavailable` texts for `status` and `doctor` rows
  (R-48) and its one message per row-error code (R-45), whose `probe-failed`
  text carries no line of Git's standard error where FR-022 takes the first,
  a difference in which the change governs (Assumptions); and the Runtime
  and CI dependency names `git-floor` beside every job of the `test` matrix,
  as its plan's "CI shape" now reads (R-46). Its `main_worktree()` now
  returns no main worktree, with its cause, instead of refusing (analyze H4,
  R-42), as FR-008 already reads for a bare repository; no requirement,
  story, edge case or Clarification answer changes. In
  `clarify-questions.md`, the Contexts of Q2, Q3, Q4, Q12, Q14 and Q15 state
  feature 004's facts at `5a02c1a`, and its code state at `fe91f2c`; no
  Question line, option or recommendation changed. The other citations read
  the same at both pins.
  Re-validation: 16 of 16 items pass, with the checks of iteration 2 re-run
  by script on the edited spec.
- 2026-10-20: four read-only reviews were folded into the spec, as stage 1 of
  their findings (the factual fixes; the questions followed at `4ba9faa`, as
  the next note says), and feature 004 was re-pinned. The four are lane
  openRepoProject-3's packet-fidelity read, lane openRepoProject-4's
  cross-check of feature 004's built runtime, a review of the recommended
  answers as one set, and a review of lane openRepoProject-5's #24 and #25.
  Lane openRepoProject-3's fidelity read of `9899eae` against the packet and
  change 2: the `registration-mismatch` warning replaces the
  `inspection-error` finding of a row whose registration disagrees and adds
  no error, so that row no longer exits 1 by itself (H1; C-26, FR-007,
  US4 s1); an exception outside the per-candidate boundary maps to
  `refused`, `os-error` or `internal-error` by its kind, and the exit-2
  text is cited (H2, L9; FR-039, FR-043, US5 s3); a holder whose probe
  reports another toplevel has null Git fields and no error (M2;
  FR-003); a child the deadline cuts is `deadline-exceeded` (L1;
  FR-011); a missing or non-regular `<path>/.git` is a registration
  disagreement (L2; FR-007); unreached worktree probes keep their
  repository's evidence (L3; FR-012); a complete scan that finds no
  project says so (L4; FR-045); FR-001, FR-003, FR-006, FR-013, FR-022,
  FR-036, FR-038, FR-039 and FR-048 cite their open questions (L5); C-29 and
  US1 s1 cite DI:1190-1191 (L6); FR-036 names C-23 and C-35 (L7); FR-019's
  estate condition is marked a reading (L8). Lane openRepoProject-4's
  cross-check of feature 004's runtime: EC-002 now says a SIGINT before the
  handlers are installed ends the run with `Cancelled.` and status 130
  (X-13), and EC-031 and EC-032 record feature 004's duplicate-registry-path
  limit and the repeated identity probe's effect on `probes.performed`
  (X-14, X-16). Feature 004's citations moved from `5a02c1a` to `d81b3d9`
  (doc round 5, rulings R-49 to R-51) after checking that every passage the
  spec cites reads the same there: round 5 changed only `data-model.md`
  (the registration limit and the mode table, neither cited before) and
  `tasks.md`; the header, Assumptions and Dependencies say that its branch's
  head, `a32d20b`, has T001 to T035 built, the evidence model merged as
  `cce8dbd`, and none of it on `main`, and Dependencies record lane
  openRepoProject-2's ruling R-54. Dependencies and Out of Scope also name
  the three open changes of lane openRepoProject-5 (issues #23 to #25) and
  their order against this feature, which reserves no flag, field or hook
  for `--remote`. In this folder, CHK006 of `ux.md` (its plan note PN-2
  withdrawn), CHK004 and CHK021 of `error-handling.md` and CHK006 of
  `api.md` now read as fixed in the spec, and the totals below were
  recounted by script. No requirement was added or removed; the tables'
  edge-case cells gain EC-031 and EC-032 and scenario 50 gains FR-045. The
  next note revises the registration limit of EC-031, the code state named
  above and CHK006 of `ux.md`. Re-validation: 16 of 16 items pass, with the
  checks of iteration 2 re-run by script on the edited spec.
- 2026-10-20: lane openRepoProject-3's delta read of that fold (`9899eae` to
  `282a20e`; 1 medium and 11 low findings, D1 to D12) was applied to
  `spec.md` and to this folder, and the questions pass that followed the fold
  (stage 2) is recorded. Finding D1: feature 004 withdrew the limit that
  EC-031 had recorded as inherited (lead ruling R-57, its data model at
  `b0243e5`), so EC-031 now says that two registry entries naming one path
  fail closed, each a registration disagreement, FR-006 points to it, SC-001
  reads one row per registry entry, and the header and Assumptions say that
  EC-031 reads feature 004's head. D2 and D3: FR-003's pointer to Q11 excepts
  a family holder, as FR-006's now does, and a holder carries no error for
  the Git probes it does not get, a manifest error still recorded (FR-004).
  D4: a missing administrative `gitdir` file is a registration disagreement
  too (FR-007, C-23). D5: FR-039 declares its reading of POD:705-707, and
  FR-049 lists FR-039's `refused` and `os-error` outputs among the parts that
  need a test. D6: FR-039 cites the `REFUSED:` literal in feature 002's
  contract, and CHK006 of `ux.md` no longer says that no human line follows
  an exception of any other kind, which no source says: PN-2 returns,
  narrowed to that case. D7: the header and Assumptions name feature 004's
  head, `b0243e5`, whose code is unchanged since `a32d20b` and whose
  documents changed after `d81b3d9` only by the tier tags, file and verify
  fields and ticks of `tasks.md`, one line of `plan.md` and the first part of
  its doc round 6 (R-55 to R-57, with R-53's P-16 and P-22 and R-54's X-3);
  the R-54 sentence is worded as lane openRepoProject-2 told it, since
  feature 004's `tasks.md` names R-54 only as the X-3 of its T047 (line 1113)
  and records no decider split. D9 to D11: the amendment note of Dependencies
  names #24's block of requirement 5 beside #25's blocks, FR-011's first
  clause says "where the 5 s limit was the smaller", and trace row 37 gains
  FR-007. D12: the count of reviews in the note above now reads four. D8:
  `clarify-questions.md`, untouched by that fold, carried its own items in
  the questions pass of `4ba9faa`: Q2 names feature 004's head `b0243e5` and
  its code since `a32d20b`, so that option B's precondition is met; Q12 takes
  the mapping of exceptions to codes as FR-039 states it and records ruling
  R-55 for a failed write, as Q15 records R-55's stalled-reader residual; the
  dated readings of Q3 (T003) and Q4 (T123), at `fe91f2c`, and of Q14 and
  Q15, at `5a02c1a`, were left in that pass and moved to `b0243e5` by
  `fdbcebb`, each cited claim holding there; Q16 and Q17 were added.
  The totals below were recounted by script: PN-2's return moves one item
  from fixed to plan note. Re-validation: 16 of 16 items pass, with the
  checks of iteration 2 re-run by script on the edited spec. The later folds
  are `fdbcebb`, `3dceaec`, `d6e4ec5`, `7eb64de` and `143a0ea`, which edited
  only `spec.md` and `clarify-questions.md`, with this file also at `7eb64de`
  and `143a0ea`, and this one, which moves feature 004's head to `6ae927f`,
  where its code has changed (its T047 and lane G's follow-up) and EC-031 and
  the R-54 sentence read it, moves the dated readings of Q2, Q3, Q4, Q12, Q14
  and Q15 there, each cited claim holding (Q8's option D keeps its `b0243e5`
  citation of the contract, now at `:331`), and applies lane
  openRepoProject-3's R6-1 to R6-3. After it, EC-033 records a present
  worktree on a branch named `HEAD` as a fill of the inspection-error rule
  (feature 004's lead ruling R-61(b)), the header, the Assumptions and
  requirement rows 4 and 5 of the traceability table name it, and CHK025
  below reads EC-025 to EC-033; no requirement changes. A later pass, taking
  lane openRepoProject-3's R7 findings (R7-1 to R7-4) and its R8 findings on
  EC-033 (L1 to L7), moves feature 004 from `6ae927f` to its head `96a08d4`,
  where its US1 plan lane is built (tasks T001 to T040 and T047 to T053, 47
  of 133) and no document differs but the ticks of `tasks.md`: every line of
  its `project` that EC-031, EC-033 and the Dependencies cite moves by 15
  with its text unchanged, each cited claim holding, and Q2, Q3, Q4, Q12,
  Q14 and Q15 read it there. It also re-pins #24 from `fffc194` to
  `ca34644`, whose overview delta is unchanged, and #25 from `67e43ae` to
  `1c32667`, whose overview spec changed in its first requirement, so that
  the cites after it moved, in Q17 and in the Dependencies; and it names
  `e45155a` where the 96 tests of `main` are counted. The Dependencies
  sentence that had every parser the overview drives report a reached record
  bound now says that only the status parser does and that FR-015's
  keep-filter is this feature's own to build (lead ruling R-70(b)), plan
  note PN-16 of `integration.md`; EC-033's wording follows R8, and plan note
  PN-17 of `testing-strategy.md` has the plan's test list name it; no
  requirement changes. The fold of lane openRepoProject-3's R9 findings then
  added to Q17's option D what #25's replacement of the credential clause
  allows (a remote's URL held and tested within bounds, a read's standard
  error drained and discarded unexamined), cited change 1's design D2 and
  D6 for the parsers' bounds, added FR-015's remote-copy flag to the
  keep-filter's list and named R-70(b) as CHK025's cause; no requirement
  changes.
- Items marked incomplete require spec updates before `/speckit-clarify` or `/speckit-plan`

## Cross-cutting Requirements Quality (no-argument `/speckit.checklist`, 2026-10-19)

**Purpose**: The cross-cutting dimensions that the user-global `speckit-checklist` skill adds to this file on a no-argument run: completeness, clarity, consistency, acceptance criteria quality, dependencies and assumptions, and ambiguities and conflicts. The domain checklists of the same run sit beside this file. The 16 items above and their notes are unchanged; the items below are numbered from CHK001 because the items above carry no ids.
**Review Ownership**: These items are reviewer-owned, as in the domain checklists: `[x]` means the requirements-quality criterion is satisfied, never that implementation work is complete.

### Requirement Completeness

- [x] CHK001 Does every ADDED and MODIFIED requirement of change 2's deltas map to at least one functional requirement? [Completeness, Traceability, Spec Appendix Requirements]
  - Result: pass. 13 of 13, by script against the delta headers.
- [x] CHK002 Does every delta scenario map to at least one functional requirement and exactly one story scenario? [Completeness, Traceability, Spec Appendix Scenarios]
  - Result: pass. 63 of 63, by script.
- [x] CHK003 Does each of FR-001 to FR-046 realize at least one row of the traceability tables, with FR-047 to FR-049 traced to the proposal's Impact and design D13? [Traceability, Spec Appendix Coverage]
  - Result: pass, by script over the tables' FR ranges.
- [x] CHK004 Are requirements present for every scenario class the feature has: primary (a healthy estate), alternate (layouts, `--attention`, `--strict`), exception (one row's failure, a failure outside the boundary), recovery (remedies, repair, re-runs) and non-functional (bounds, read-only, determinism)? [Coverage, Spec US1 to US11, FR-011 to FR-022, FR-040]
  - Result: pass.
- [x] CHK005 Are the points the delta leaves to design D1 to D13 cited to the decision rather than restated in another form? [Completeness, Spec Requirements preamble, Assumptions]
  - Result: pass.
- [x] CHK006 Is every citation key the spec uses (`POD`, `PRSD`, `DI`, `CMD`, `CLN`, [E], [L], [G], [R], [P]) defined with the file and the commit it points at? [Traceability, Gap, Spec header]
  - Result: fixed in spec.md, C-37. `CMD:N` and `CLN:N` were used eight times and defined nowhere.
- [x] CHK007 Are the points the change leaves open recorded as questions for Brett Heap rather than settled in the spec? [Completeness, Spec Assumptions]
  - Result: pass. Q1 to Q13, and Q14 and Q15 from this run.
- [x] CHK008 Is each clarification applied where its "Where applied" line says? [Consistency, Traceability, Spec Clarifications]
  - Result: pass, by script: every target a C-n names exists and cites it or carries its rule.

### Requirement Clarity

- [x] CHK009 Are the bounds stated as numbers with units rather than adjectives? [Clarity, Spec FR-011 to FR-018, FR-033]
  - Result: pass.
- [x] CHK010 Are approximate quantities ("about 300 entries", "about 355 rows", "about 2 s") confined to edge cases, assumptions and scenarios that give an exact threshold beside them? [Clarity, Spec EC-004, EC-009, US6 s9]
  - Result: pass.
- [x] CHK011 Is every obligation written with MUST or MUST NOT, never as "no X MUST"? [Clarity, Spec Functional Requirements]
  - Result: pass, by search: each hit of `no ... MUST` has another subject.
- [x] CHK012 Does the spec say what and why, naming no function, module or file of the implementation? [Clarity, Spec Assumptions]
  - Result: pass. It names behaviour the deltas fix in mechanism terms, as the Assumptions record.

### Requirement Consistency

- [x] CHK013 Are codes, classifications and field names spelled identically across stories, requirements, entities and criteria? [Consistency]
  - Result: pass, by search for each gate code, class and finding code.
- [x] CHK014 Do the stories' acceptance scenarios agree with the delta scenarios they realize? [Consistency, Spec Appendix Scenarios]
  - Result: pass.
- [x] CHK015 Are the exit rules consistent across FR-029, FR-042, FR-043, FR-044 and the stories? [Consistency, Spec FR-042]
  - Result: pass.

### Acceptance Criteria Quality

- [x] CHK016 Is each success criterion objectively measurable (a count, a percentage, a byte comparison or a time bound)? [Measurability, Spec SC-001 to SC-014]
  - Result: pass.
- [x] CHK017 Does each success criterion measure requirements that exist, by citation or by content? [Traceability, Spec SC-001 to SC-014]
  - Result: pass.
- [x] CHK018 Is every success criterion achievable, none requiring what a run cannot meet? [Measurability, Spec SC-004, SC-005]
  - Result: pass with C-48, which aligns SC-005's reference point with FR-011.

### Dependencies and Assumptions

- [x] CHK019 Is the dependency on feature 004 stated with the commit it is read at, and is the open choice of its state before the plan recorded? [Dependency, Spec Dependencies]
  - Result: pass; the choice is existing question Q2.
- [x] CHK020 Are the measured assumptions stated with their source and date (48.3 s, 219 candidates, 96 tests)? [Assumption, Spec Assumptions]
  - Result: pass. 96 tests re-counted in `tests/test_project.py` at this commit.
- [x] CHK021 Is the assumption that no other process changes the estate stated where determinism depends on it? [Assumption, Spec FR-019, EC-023]
  - Result: pass.
- [x] CHK022 Is the departure from the change's order (specify before feature 004 merges) recorded with its authority and its limit? [Assumption, Spec header, Clarifications C-21]
  - Result: pass.

### Ambiguities and Conflicts

- [x] CHK023 Is every point left to the plan named as such? [Ambiguity, Spec Assumptions]
  - Result: pass. The spec names its one; this run's plan notes PN-1 to PN-17, PN-2 narrowed on 2026-10-20 to an exception of any other kind in human mode, are listed in the domain checklists' Evaluation sections.
- [x] CHK024 Are the differences between change 2 and feature 004 recorded with which text governs? [Conflict, Spec Assumptions, Clarifications C-33]
  - Result: pass.
- [x] CHK025 Are the recorded residuals (EC-001, EC-002, EC-006, EC-022, EC-025 to EC-033) kept apart from requirements, so that none reads as a promise? [Ambiguity, Spec Edge Cases]
  - Result: pass.

## Evaluation

Evaluated on 2026-10-19 against `spec.md` at `8f433f7`. 25 items: 24 pass, 1
fixed in the spec, 0 open, 0 plan notes, 0 new questions. An open item waits
on the question or residual its result names; a plan note is for the plan, not
the spec; a new question is asked in `clarify-questions.md`.
The counts are for the cross-cutting section above; the 16 built-in items
before it carry no ids and are not counted.

Plan notes: none.

All 17 checklists: 413 items: 357 pass, 22 fixed in the spec, 15 open, 17
plan notes (PN-1 to PN-17; PN-2 narrowed to an exception of any other kind
in human mode), 2 new questions. Recounted by script on 2026-10-20.
