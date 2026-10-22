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
- Lane openRepoProject-2's binding flags were checked: the order departure is
  recorded with the time of Brett Heap's word; no test needs a running
  filesystem monitor (FR-049, C-6); every Git child carries the seven pins and
  [E]'s name scrub, with no push child and so no R-28 exception (FR-016, C-5);
  local ancestry outranks `remote-gone` (FR-028) and squash merges (LQ-2) are
  deferred to a follow-on change (EC-013, C-8); the MODIFIED capability is
  `project-review-safety` (C-7).
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
  A last pass moved #24's pin from `ca34644` to its final head `fe5b245`
  and #25's from `1c32667` to `129a4e2`, each cited range keeping its lines
  but three of #25's `proposal.md` ranges, which move by 4; no requirement
  changes.
  The fold of lane openRepoProject-3's R10 findings then completed Q17 D's
  statement of #25's replacement credential clause, and no recommendation
  changed letter; no requirement changes.
  A further pass moved #25's pin to its final head `05a424a`, every cited
  range keeping its lines, and added to Q17's option D the bounds #25 sets
  on its `gh` children and the clauses that still bind the `project`
  process and every Git child (lane openRepoProject-3's R11-1); no
  recommendation changed letter; no requirement changes.
- 2026-10-21: Brett Heap's answers to Q1 to Q17, "yes, recommended for Q1-Q17"
  (lane openRepoProject-4's session at about 10:31Z, recorded as a RULED line
  at 10:33:09Z), were folded into `spec.md` as C-55 to C-71, in a session of
  their own: Q1 A, Q2 A, Q3 B, Q4 D, Q5 A, Q6 A, Q7 A, Q8 D, Q9 B, Q10 A,
  Q11 A, Q12 A, Q13 A, Q14 A, Q15 A, Q16 B and Q17 A. Every sentence that
  pointed at an open question now states the decision and cites its C-id;
  FR-050 (the overview's small set in the `git-floor` job) and FR-051 (one
  `AGENTS.md` sentence) are added, with EC-034 (strings that are not paths
  carry no validity flag) and EC-035 (a signal that stops the write of a
  result). Dependencies names amendment A1,
  `amend-project-overview-clarify-answers`, lane openRepoProject-4's governed
  change to be proposed after this fold, as the carrier of the change-2
  amendments; lane openRepoProject-2's draft PR #19 as the carrier of Q9 B's
  change-1 part, which that lane agreed on 2026-10-21 to carry, its commit and
  the list's count left to a later pass; and the departures on Brett Heap's
  word (Q3 B, Q4 D, and Q17 A in the #24-first order). No pin moved. In
  `clarify-questions.md` the Status records the answers and the closing
  paragraph says they are folded; every question, option and Recommended
  paragraph is unchanged. In this folder, the 15 items open on a question and
  the 2 new questions now pass, CHK006 of `error-handling.md` passes on C-62
  with plan note PN-11 withdrawn, PN-6 and PN-12 are narrowed (C-66, C-68),
  PN-2 also takes a failed write's standard-error line (C-66), and the totals
  below were recounted by script. Re-validation: 16 of 16 items pass, with the
  checks of iteration 2 re-run by script on the edited spec.
- 2026-10-21, later the same day: a re-check that keeps every pin, of feature
  004 against its head `2cf34d3` (133 of 133 tasks ticked, not on `main`), of
  #25 against its draft PR's head `11a0ba2` and of #24 against its draft PR's
  head `e07cc42`, is recorded in a header paragraph and in the Dependencies.
  Lane openRepoProject-2's lead ruling R-67 (c), present rows that share a
  realpath or an admin id being `registration-mismatch`, is taken as a fill, as
  EC-033 takes R-61 (b), with its R-101's second identity check before each
  status probe: FR-007, FR-019, FR-049 and EC-031 say so. PR #19's Q9 B commit
  `423a532` is cited for [E]'s thirty-one names (C-63, FR-016, EC-022,
  Dependencies), C-5's seventeen staying as C-63 reads it. Brett Heap's answers
  to lane openRepoProject-2's LQ-10 to LQ-15, given in lane openRepoProject-3's
  session, are recorded as dependencies on PR #19 (FR-007, FR-016, FR-043 and a
  new Dependencies bullet), with EC-036 for a relative `HOME` or
  `XDG_CONFIG_HOME`; LQ-8, LQ-9, the bare entries that feature 004's
  `inspect-cap` leaves out, a failed ref listing's parity case and the
  `git-floor` job's change at `c9103ba` are recorded in the Dependencies, and
  C-22, C-58, EC-033 and FR-051 read the head. Lane openRepoProject-3's
  fidelity read of `c54d393` is applied: A1's bullet records Q7 A's open parity
  case (M1), states the interim rule for the six requirements folded ahead of
  A1 (M2) and gains design D1's restatement of Q15 A's rule (L6); the older
  session intros record the answers (L1); FR-049 and US10's Independent Test
  assert the trace2 pins (L3); FR-005, US6 s13 and US7 s1 and s5 put the path
  in `path` (L4); FR-005 names an absent default root's path as one of FR-038's
  exceptions (L5); FR-048's `AGENTS.md` pointer goes, FR-051 carrying it (L7);
  and C-64 quotes DI:126-128 (L8). `clarify-questions.md` is unchanged. In this
  folder, CHK010 of `classification.md` is fixed by the twin fill and CHK003 of
  `security.md` by EC-036; CHK002, CHK004, CHK010, CHK013, CHK014, CHK016 and
  CHK019 of `security.md`, CHK002, CHK004, CHK008, CHK011 to CHK013 and CHK025
  of `integration.md`, CHK016 of `discovery-identity.md`, CHK018 of
  `suggestions-gates.md`, CHK002, CHK004 and CHK014 of `testing-strategy.md`,
  and CHK019, CHK024 and CHK025 below were re-read, and the totals below were
  recounted by script. Re-validation: 16 of 16 items pass, with the checks of
  iteration 2 re-run by script on the edited spec.
- 2026-10-21, a third pass: lane openRepoProject-3's W6 read of `8082d3b` and
  PR #19's LQ-15 (`cc000ea`) and LQ-10 (`ea697ba`) commits are applied. FR-007
  decides, within change 2's lists, the outcome of a row that its identity
  re-verification does not confirm: the class's `inspection-error` finding, no
  row error where a re-read value differs, and the fitting code where the
  re-read itself fails, so that the run exits 1 (W6 M2); plan note PN-18 has
  the plan re-read it against feature 004's fix. FR-043 and the LQ-15 bullet
  take LQ-15 from `cc000ea`, pending #19's ratification, keep
  `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` in a sentence of their own, and
  leave the overview's code and exit status open for A1 (W6 M1); FR-016 and the
  LQ-10 bullet take LQ-10 from `ea697ba`. EC-036 credits lane
  openRepoProject-4's reproduction as R-101 (j) records it, uses the present
  tense of `cc000ea` and adds a relative `GIT_CONFIG_GLOBAL` (W6 L2 to L4);
  LQ-14 takes R-102 (b)'s list (L5); FR-019 names the realpath read (L6);
  EC-031 says "of one registered worktree" (L7); the Dependencies name the five
  incremental parsers and the new `RelayParser` (L8); and the LQ-13 and LQ-14
  bullet says that a new class or code would need an amendment of change 2
  (L9). No pin moves, and `clarify-questions.md` is unchanged. In this folder,
  CHK026 of `integration.md` is added as plan note PN-18; CHK002 to CHK004,
  CHK014, CHK016 and CHK019 of `security.md`, CHK016 of `discovery-identity.md`
  and CHK023 below were re-read, and the totals below were recounted by script.
  Re-validation: 16 of 16 items pass, with the checks of iteration 2 re-run by
  script on the edited spec.
- 2026-10-21, a fourth pass: the spec aligns with amendment A1 at `b020edc`
  (draft PR #34), whose side lane openRepoProject-3's W7 read found to match
  each option: FR-050 and C-57 cite A1's Impact for Q3 B, no longer a
  departure; FR-022, SC-010 and C-62 cite A1's requirement 4 table and its
  OPERATION values `stat`, `scandir` and `collection`, A1's drafted fill; the
  A1 bullet takes A1's own map of sites (W6 L1; W7 check 4, item 3); and FR-044
  and C-70 take design D1's scope, the handlers only recording while a child
  can run and raising only in the write span. W7's three MEDIUMs are mirrored:
  FR-045 prints an error's `path` (M1), C-61 records DI:778's null rule for
  `current` (M2) and C-63 the narrowing of DI:307-308 (M3). From PR #19,
  pending its ratification: FR-007 classifies a linked row whose effective work
  tree is not its registered path as `project clean` does, by the extension
  read and the effective-work-tree probe of LQ-11 (`addd346`), FR-013, FR-019,
  FR-020 and FR-049 following and the change-2 texts that read against the two
  children recorded for A1; FR-032, SC-004 and EC-007 make LQ-14's
  `operation-in-progress` (`43f7107`) and LQ-13's `worktree-only-commits`
  (`93de4bb`) exclusions only the batch applies; FR-043 takes `9fb22fa`'s order
  and wording, with A1's revision 2's proposed `relative-config-path` and the
  fallback `refused`, and LQ-12 cites `eae1a79`. EC-022 and FR-040 add the `gh`
  residual (#29's D5 at `11a0ba2`), and EC-033 the `refs/heads/HEAD`
  consequence of feature 004's F1 M-1 fix, pending. Lane openRepoProject-3's
  W11 read of `08d5d79` is applied: EC-036 drops a version R-101 (j) does not
  give and cites W8 for `GIT_CONFIG_SYSTEM` (L1, L2); FR-043 and security
  CHK016 carry the strike mark (L3); the LQ bullets cite every commit (L4);
  FR-007 keeps the first read's identity and counts an `ENOENT` or `ENOTDIR`
  re-read as a differing value (L5, L6); FR-043 takes `9fb22fa`'s wording (L7)
  and the A1 pointer names POD:765-766 (L8). No pin moves, and
  `clarify-questions.md` is unchanged. In this folder, results that cite the
  changed text were re-read in `deployment.md`, `integration.md`,
  `security.md`, `discovery-identity.md`, `observability.md`, `ux.md`,
  `error-handling.md`, `suggestions-gates.md`, `testing-strategy.md` and CHK015
  and CHK025 below, no category changing, and the totals below were recounted
  by script. Re-validation: 16 of 16 items pass, with the checks of iteration 2
  re-run by script on the edited spec.
- 2026-10-21, a fifth pass: every citation of amendment A1 moves from `b020edc`
  to its revision 3 at `367223a`, those of the items the fourth pass marked as
  A1's revision 2's included, each still proposed in draft PR #34 and pending
  Brett Heap's ratification under the interim rule, which now also names what
  follows A1's three items of its own. The A1 bullet and the LQ bullets mirror
  revision 3's ordering rule, each item landing only with or after PR #19's
  ratification of the commit it follows, with R-124 and R-125 named as still to
  come and none of their text, and its departure records: DI:506-509 and
  DI:1193-1201 for LQ-11's counts (FR-020), DI:1086-1089 for
  `relative-config-path`, its `refused` fallback departing from nothing
  (FR-043), and OV:110-113 and DI:690-692 for the batch-only gates (FR-032).
  LQ-11's change-2 sites are cited as A1 amends them: POD:333's exit-1
  exception (FR-007), the second-phase sentence after POD:246 (FR-019), the
  `estimated` rule (FR-020) and D8's toplevel realpath task (FR-013); US1 s3
  takes A1's "plus four, plus four". FR-045 prints a row error's `path` on the
  next line, indented to the message column, and a scan error's as `Incomplete:
  <path>: <message> (<code>).`, in D10's and requirement 12's words. #25 is
  re-checked at `3965dfb`, its pin `05a424a` kept, and EC-022 cites #29's D5 at
  `79d196a`. In this folder, CHK012 of `ux.md` is fixed in the spec, with plan
  note PN-4 withdrawn; results that cite A1 were re-read in `deployment.md`,
  `integration.md`, `security.md`, `observability.md`, `error-handling.md`,
  `suggestions-gates.md` and CHK015, CHK023 and CHK025 below; and the totals
  below were recounted by script. Re-validation: 16 of 16 items pass, with the
  checks of iteration 2 re-run by script on the edited spec.
- 2026-10-21, a sixth pass: lane openRepoProject-3's W17 read of `b511bdb`
  (HIGH 0, MEDIUM 2, LOW 7) and PR #19's rulings R-124 (`2b86a5f`), R-125
  (`93f3194`) and R-126 (`1ebdd90`) are applied, by the lead's decisions shared
  with A1's revision 4. W17's two MEDIUMs were met by the fifth pass (US1 s3's
  count, POD:129 among the LQ-11 sites, and FR-045's path line). Its LOWs:
  FR-007 declares its split of the effective-work-tree probe's outcomes as a
  fill of [E]'s "a probe that fails" (L1); the POD:333 record and FR-007 name
  the probe's failing exit as a disagreement with no error, as `addd346` has it
  and A1 revision 4 is to propose (L2); EC-032 says that FR-020's
  identity-probe count stands as ratified (L3); FR-043 and the LQ-15 bullet
  read the code as resting on Brett Heap's LQ-15 word, whose form the lead gave
  as `clean`, `status`, `doctor` and `update` (lane openRepoProject-2's ruling
  R-102 (c) 3; `9fb22fa` proposal.md:954-956) (L4); SC-004 cites PR #19's lines
  beside CLN:800-803 (L5); EC-033 cites R-116 and W17's reproduction on Git
  2.36.6 (L6); and FR-013's and FR-020's LQ-11 sentences carry their own
  pending mark (L7). From PR #19, pending its ratification: FR-032, SC-004 and
  the LQ-13 and LQ-14 bullet take R-124's settled failure rule; FR-007, FR-013,
  FR-049 and the LQ-11 bullet take R-125's `commondir` check; the bullet cites
  #19's list of eleven markers at `1ebdd90` rather than naming them (R-126);
  and the LQ intro names the commits each item now follows. A1 revision 4
  (draft PR #34) is cited with no sha. No pin moves, and `clarify-questions.md`
  is unchanged. In this folder, CHK016 of `discovery-identity.md`, CHK012 and
  CHK020 of `suggestions-gates.md`, CHK020 of `integration.md` and CHK002 of
  `testing-strategy.md` were re-read, no category changing, and the totals
  below were recounted by script. Re-validation: 16 of 16 items pass, with the
  checks of iteration 2 re-run by script on the edited spec.
- 2026-10-21, a seventh pass: lane openRepoProject-3's W20 read of A1 revision
  3 (HIGH 0, MEDIUM 2, LOW 8), by the lead's decisions D6 to D9 shared with
  A1's revision 4. FR-007 and the LQ-11 bullet record that the collector-table
  exception departs from the packet's DI:535, and the A1 bullet adds it to the
  LQ-11 item's departures (D6); FR-007 and the LQ-11 bullet name a per-worktree
  `core.bare=true` among the failures of the effective-work-tree probe that are
  a disagreement with no error, as W20 measured on Git 2.43.0 and 2.36.6 (D7);
  the LQ intro and the A1 bullet add the ordering rule's ratified-first case,
  PR #34 not merging before #19's ratification of the commits its LQ items
  follow, or those items moving to a later amendment if Brett Heap wants #34
  sooner (D8); and FR-013's toplevel realpath task gives FR-007's outcomes
  (D9). FR-007 also reads the extension read's exit 1 as a value not set only
  with nothing on either stream, an exit 1 with a warning, as for an unreadable
  `config`, counting as true (W20, section 4). A1 revision 4 (draft PR #34) is
  cited with no sha. No pin moves, and `clarify-questions.md` is unchanged. In
  this folder, CHK016 of `discovery-identity.md` was re-read, its category
  unchanged, and the totals below were recounted by script. Re-validation: 16
  of 16 items pass, with the checks of iteration 2 re-run by script on the
  edited spec.
- 2026-10-21, an eighth pass: A1's revision 5 at `3ee860c`, which restates the
  status pins after LQ-10, with the lead's commit 3f inputs. Every citation of
  A1 at `367223a`, and every "A1 revision 4 (draft PR #34)" placeholder, now
  cites `3ee860c` at its lines there: D8's toplevel realpath task and its bound
  move to design.md:484-491 and :506-508, D10's fill to :548-550, :556-559 and
  :567-572, the open point to proposal.md:1406-1413 and Q15 A and Q16 B to
  :1401-1404; requirement 7 (spec:580-587) and D5 (design.md:334-341) do not
  move. FR-019 and the LQ-11 bullet record that A1 now amends POD:238-239 as
  well, naming the second phase "the worktree probes, effective-work-tree reads
  and status probes" (its :257-259). FR-007 and the LQ-11 bullet quote both of
  A1's exceptions in the collector table (its :359); on the lead's ruling for
  `addd346`, a rev-parse that cannot be spawned is "a probe that fails", a
  disagreement with no error, only a cut leaving the check not completed, and
  FR-007's declared fill narrows to the cut. FR-032, SC-004 and the LQ-13 and
  LQ-14 bullet give R-124's outcome rule in `2b86a5f`'s words, and the bullet
  cites [G]'s list of markers at `1ebdd90` (:650-659) with no names and no
  count. The LQ intro and the A1 bullet count four LQ items, the fourth LQ-10's
  stat pins, a restatement, each with the commits it follows, and the merge
  order for PR #34; FR-016 and the LQ-10 bullet quote [E]'s four status pins as
  A1 restates them (requirement 3, spec:220-222; D13, design.md:690-691), and
  EC-036 names its reproduction's two pins as those [E] carried before LQ-10.
  #25 is re-checked at `86324ff` and `2eeaec4`, its pin `05a424a` kept: the
  cited ranges are byte-identical by `cmp`, except tasks 2.3 and 2.4
  (`tasks.md:22-23`), which gain C-51's second diff, and EC-022's D5 residual
  reads the same at `design.md:565-592` there. No pin moves, and
  `clarify-questions.md` is unchanged. In this folder, CHK006 of
  `deployment.md`, CHK012 and CHK020 of `integration.md`, CHK012 of `ux.md`,
  CHK003 and CHK011 of `observability.md`, CHK002, CHK003 and CHK019 of
  `security.md`, CHK016 of `discovery-identity.md`, CHK008 of `idempotency.md`,
  CHK012 and CHK020 of `suggestions-gates.md` and CHK015 here were re-read, no
  category changing, and the totals below were recounted by script.
  Re-validation: 16 of 16 items pass, with the checks of iteration 2 re-run by
  script on the edited spec.
- 2026-10-21, a ninth pass: A1's revision 6 at `d644517` and lane
  openRepoProject-3's W25 read of 3c to 3f and of A1's revisions 4 and 5 (HIGH
  0, MEDIUM 1, LOW 12), by the lead's commit 3g decisions. Every citation of A1
  now cites `d644517` at its lines there: its spec's lines from 112 on move
  down 5 (the collector-table row to :364), and its proposal's LQ items to
  :1251-1423, Q15 A and Q16 B to :1425-1428 and the open point to :1430-1437;
  its design and clarifications do not move. FR-007, the LQ-11 bullet and the
  A1 bullet record that requirement 2's closed case list now holds FR-007's
  third case as change 2's own text (A1's spec:107-111, amending POD:89-95),
  departing from the packet's DI:251-261 (W25 M1), and that A1's
  collector-table exception names a probe that cannot be spawned (L8); FR-007
  credits that reading to the lane openRepoProject-4 lead's ruling (L12).
  FR-043, the LQ-15 bullet and the sixth pass above credit the LQ-15 form to
  lane openRepoProject-2's ruling R-102 (c) 3 (L2); the LQ-13 and LQ-14 bullet
  cites the review-safety rule at :101-118 (L6); the LQ intro and the A1 bullet
  add the ratified-first re-alignment (L9); and EC-022, FR-040 and the LQ-10
  bullet record that LQ-10's pins widen the clean-filter residual, as #19's
  design Risks says and A1 records (L10). The LQ intro re-checks PR #19 at its
  round (a), `6f2cb54`: nothing this spec cites from #19 at `1ebdd90` changes
  there. #24's re-check at #27's round B10 waits for lane openRepoProject-5's
  sha and line map. No pin moves, and `clarify-questions.md` is unchanged. In
  this folder, CHK006 of `deployment.md`, CHK012 and CHK020 of
  `integration.md`, CHK012 of `ux.md`, CHK003 and CHK011 of `observability.md`,
  CHK002, CHK003 and CHK019 of `security.md`, CHK016 of
  `discovery-identity.md`, CHK012 of `suggestions-gates.md` and CHK015 here
  were re-read, no category changing, and the totals below were recounted by
  script. Re-validation: 16 of 16 items pass, with the checks of iteration 2
  re-run by script on the edited spec.
- 2026-10-21, a tenth pass: A1's revision 7 at `0394be4` and lane
  openRepoProject-3's W29 read of A1's revision 6 and of 3g (HIGH 0, MEDIUM 0,
  LOW 3), by the lead's commit 3h decisions. Every live citation of A1 now
  cites `0394be4` by A1's line map: its spec's lines from 116 on move down 5
  (the collector-table row to :369, the case list to :104-120), and its
  proposal's LQ-11 record to :1375-1403, the LQ-10 item to :1404-1433, Q15 A
  and Q16 B to :1435-1438 and the open point to :1455-1462. FR-007's record
  notes that A1's third case now takes FR-007's words, its disagreement case
  FR-007's tie-break and its second case a cut `lstat` (W29 L1 and O2),
  FR-007's own words unchanged; FR-040 cites A1's record of #19's Risk at
  :1424-1433 (W29 L2); and the LQ intro says that one word of #19's gate block
  changes at `6f2cb54` (W29 L3). The LQ intro re-checks #19's round (b),
  `4485678` and `a664799`: nothing this spec cites changes there but the
  review-safety rule, which keeps the clause the LQ-13 bullet cites and gains
  R-171's rule; the overview has no revalidation, so no requirement moves; and
  LQ-20 is cited, not restated, with the units that would follow if #19 bounded
  [E]'s plan-time work-tree probe in [E] itself. #25 is re-checked at
  `6b5bf8f`, its pin `05a424a` kept, every cited range byte-identical to
  `2eeaec4`'s by `cmp`. #24's re-check at #27's round B10 still waits for lane
  openRepoProject-5's sha and line map. No pin moves, and
  `clarify-questions.md` is unchanged. In this folder, CHK006 of
  `deployment.md`, CHK012 and CHK020 of `integration.md`, CHK012 of `ux.md`,
  CHK003 and CHK011 of `observability.md`, CHK002, CHK003 and CHK019 of
  `security.md`, CHK016 of `discovery-identity.md`, CHK012 of
  `suggestions-gates.md` and CHK015 here were re-read, no category changing,
  and the totals below were recounted by script. Re-validation: 16 of 16 items
  pass, with the checks of iteration 2 re-run by script on the edited spec.
- 2026-10-21, an eleventh pass: #24 is re-checked at its draft PR #27's head
  `d4e960b`, after round B10, its pin `fe5b245` kept, by lane
  openRepoProject-5's line map and this spec's own `cmp` of each range against
  `e07cc42` and the pin: every pinned range of its proposal and design is
  byte-identical at new lines, and so is the first line of its task 3.2, which
  now holds reader RF's M1, the return route and the second re-base diff, on
  lane openRepoProject-4's YES of 2026-10-21T16:13:14Z. The header paragraph
  and the Dependencies bullet record it; C-71 and `clarify-questions.md` keep
  their `fe5b245` pins unchanged. No checklist result changes, and the totals
  below were recounted by script. Re-validation: 16 of 16 items pass, with the
  checks of iteration 2 re-run by script on the edited spec.
- 2026-10-21, a twelfth pass: #19's round (c), `2e819ad` (lane
  openRepoProject-2's R-187 and R-190), is re-checked in the LQ intro. It
  settles lane openRepoProject-3's W31 M-1, so the round (b) sentences no
  longer call that clause open; the LQ-13 bullet stays pinned at `1ebdd90` and
  unchanged. Its `project-command` spec is unchanged; "Clean bounds" changes
  only a sentence this spec does not cite; the gate block, the three scenarios,
  the two review-safety scenarios and the Risk keep their text, at the lines
  the LQ intro states; and LQ-20 is cited at :1273-1294 there, with no figures
  or options, the re-align condition still holding. No checklist result
  changes, and the totals below were recounted by script. Re-validation: 16 of
  16 items pass, with the checks of iteration 2 re-run by script on the edited
  spec.
- 2026-10-22, a thirteenth pass: lane openRepoProject-3's W34 read of A1's
  revision 7 and of 3h to 3j (HIGH 0, MEDIUM 1, LOW 3), by the lead's commit 3k
  decisions, and A1's revision 8 at `177eadf`. The LQ intro's re-align
  condition now has two arms, #19 bounding [E]'s plan-time work-tree probe in
  [E] itself or, under LQ-20's step (d) at `2e819ad`, lowering the 128-row cap
  and the 16-target limit that the Dependencies state and US4 s3 and s4 assume
  (MEDIUM-1), with no figures of (d) and no other option restated; it cites
  R-171's rule at :103-104 and :117-127 (LOW-2), and the deferred-target
  sentence as C-45 cites its ratified form (LOW-3). FR-007's second case names
  the row's task (FR-013) and its third case's reads name no cut (LOW-1), every
  outcome as it was; FR-007's record notes that A1's third case's cut is now
  the realpath's and the effective-work-tree read's only and that its second
  case takes the row task's cut. Every live citation of A1 now cites `177eadf`
  by A1's line map: its spec's lines do not move, the case list rewording
  :113-120 in place, and POD:579 and :584 are its :651 and :656; its proposal's
  LQ-11 record moves to :1375-1404, the LQ-10 item and its Risk to :1405-1434
  and :1425-1434, Q15 A and Q16 B to :1436-1439, the record of requirement 2
  and design D8 to :1441-1459, the open point to :1461-1468 and the review's
  merge-order point to :1480-1482. No other pin moves, and
  `clarify-questions.md` is unchanged. In this folder, CHK006 of
  `deployment.md`, CHK012 and CHK020 of `integration.md`, CHK012 of `ux.md`,
  CHK003 and CHK011 of `observability.md`, CHK002, CHK003 and CHK019 of
  `security.md`, CHK016 of `discovery-identity.md`, CHK012 of
  `suggestions-gates.md` and CHK015 here were re-read, no category changing,
  and the totals below were recounted by script. Re-validation: 16 of 16 items
  pass, with the checks of iteration 2 re-run by script on the edited spec.
- 2026-10-22, a fourteenth pass: #19's round (d), `9267303` (lane
  openRepoProject-2's R-207 and R-208; lane openRepoProject-3's W36 read and
  W32 L1), and A1's revision 9 at `4261ff8`, by the lead's commit 3l decisions.
  For #19's two batch-only gates, a listing or read not finished within the
  filesystem budget, the deadline not being the limit, now records
  `probe-timeout` and makes the row `inspection-error`, where it left the row
  unprobed; FR-032, SC-004 and the LQ-13 bullet follow it, as A1 does, and so
  do CHK012 of `suggestions-gates.md` and CHK020 of `integration.md`, their
  categories unchanged; the overview's own branch-reflog gate (FR-033, FR-034)
  is unchanged. The LQ intro re-checks round (d): `project-command` is
  unchanged; the gate block changes those two sentences only; the scenarios,
  the caps of "Clean bounds" and the Risk keep their text at the lines it
  states; R-208 governs revalidation only, the LQ-13 bullet's revalidation
  sentence still holding; and R-207 costs LQ-20's options, (c) moving no value
  this spec states and step (d) now lowering the report's row cap too, so the
  re-align condition's second arm also takes the 256-row cap. Every live
  citation of A1 now cites `4261ff8` by A1's line map: its spec's lines do not
  move; its proposal's lines from :1323 on move down 4, the gates item to
  :1300-1338 and its outcome rule to :1311-1326, and its LQ intro's merge order
  ends at :1271. No other pin moves, and `clarify-questions.md` is unchanged.
  In this folder, CHK006 of `deployment.md`, CHK012 and CHK020 of
  `integration.md`, CHK012 of `ux.md`, CHK003 and CHK011 of `observability.md`,
  CHK002, CHK003 and CHK019 of `security.md`, CHK012 of `suggestions-gates.md`
  and CHK015 here were re-read, no category changing, and the totals below were
  recounted by script. Re-validation: 16 of 16 items pass, with the checks of
  iteration 2 re-run by script on the edited spec.
- 2026-10-22, a fifteenth pass: #24 is re-checked at its draft PR #27's head
  `25f7333`, after round B12, with round B11 at `f170079` recorded on the way,
  its pin `fe5b245` kept, by lane openRepoProject-5's two line maps and this
  spec's own `cmp` of each range against `d4e960b` and the pin: every pinned
  range of its proposal and design is byte-identical at new lines, its task 3.2
  is unchanged at :178-193, and its `project-overview` block is the same blob.
  The header paragraph and the Dependencies bullet record it; C-71 and
  `clarify-questions.md` keep their `fe5b245` pins unchanged, and A1 stays
  cited at `4261ff8`. No checklist result changes, and the totals below were
  recounted by script. Re-validation: 16 of 16 items pass, with the checks of
  iteration 2 re-run by script on the edited spec.
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
  - Result: pass. Q1 to Q17, answered by Brett Heap on 2026-10-21 and folded as
    C-55 to C-71.
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
  - Result: pass; FR-043's pointer also names FR-042's exit-2 causes
    (POD:765-766), for which amendment A1 at `4261ff8` proposes
    `relative-config-path` with exit 2, pending.

### Acceptance Criteria Quality

- [x] CHK016 Is each success criterion objectively measurable (a count, a percentage, a byte comparison or a time bound)? [Measurability, Spec SC-001 to SC-014]
  - Result: pass.
- [x] CHK017 Does each success criterion measure requirements that exist, by citation or by content? [Traceability, Spec SC-001 to SC-014]
  - Result: pass.
- [x] CHK018 Is every success criterion achievable, none requiring what a run cannot meet? [Measurability, Spec SC-004, SC-005]
  - Result: pass with C-48, which aligns SC-005's reference point with FR-011.

### Dependencies and Assumptions

- [x] CHK019 Is the dependency on feature 004 stated with the commit it is read at, and is the open choice of its state before the plan recorded? [Dependency, Spec Dependencies]
  - Result: pass; the plan starts once feature 004 has merged into `main`, on
    Brett Heap's word given after it (C-56). Re-checked on 2026-10-21 at its
    head `2cf34d3`, with the pins kept (header).
- [x] CHK020 Are the measured assumptions stated with their source and date (48.3 s, 219 candidates, 96 tests)? [Assumption, Spec Assumptions]
  - Result: pass. 96 tests re-counted in `tests/test_project.py` at this commit.
- [x] CHK021 Is the assumption that no other process changes the estate stated where determinism depends on it? [Assumption, Spec FR-019, EC-023]
  - Result: pass.
- [x] CHK022 Is the departure from the change's order (specify before feature 004 merges) recorded with its authority and its limit? [Assumption, Spec header, Clarifications C-21]
  - Result: pass.

### Ambiguities and Conflicts

- [x] CHK023 Is every point left to the plan named as such? [Ambiguity, Spec Assumptions]
  - Result: pass. The spec names its one; this run's plan notes PN-1 to PN-17,
    with PN-18 added on 2026-10-21 for FR-007's re-verification against feature
    004's fix, PN-2 narrowed on 2026-10-20 to an exception of any other kind in
    human mode and widened on 2026-10-21 to a failed write's standard-error
    line (C-66), PN-6 and PN-12 narrowed on 2026-10-21 (C-66, C-68), PN-11
    withdrawn then (C-62) and PN-4 later that day (FR-045), are listed in the
    domain checklists' Evaluation sections.
- [x] CHK024 Are the differences between change 2 and feature 004 recorded with which text governs? [Conflict, Spec Assumptions, Clarifications C-33]
  - Result: pass; since 2026-10-21 also where the change is silent: the twin
    fill of EC-031 and the recorded divergence in the cap count (Dependencies).
- [x] CHK025 Are the recorded residuals (EC-001, EC-002, EC-006, EC-022, EC-025
  to EC-036) kept apart from requirements, so that none reads as a promise?
  [Ambiguity, Spec Edge Cases]
  - Result: pass, EC-034 to EC-036 included since 2026-10-21. EC-022's `gh`
    residual and EC-033's `refs/heads/HEAD` consequence, added on the same day,
    are kept apart too, the first citing #29's D5 at `79d196a`.

## Evaluation

Evaluated on 2026-10-19 against `spec.md` at `8f433f7`; CHK007, CHK019, CHK023
and CHK025 re-read on 2026-10-21 after Brett Heap's answers (C-55 to C-71),
their results still pass, and CHK019, CHK024 and CHK025 again later that day,
after the re-check against feature 004's head `2cf34d3` and EC-036, theirs too,
and CHK023 after lane openRepoProject-3's W6 read, its result still pass, and
CHK015 and CHK025 after the fourth pass, theirs too, and CHK015, CHK023 and
CHK025 after the fifth. 25 items: 24 pass, 1 fixed in the spec, 0 open, 0 plan
notes, 0 new questions. An open item waits on the question or residual its
result names; a plan note is for the plan, not the spec; a new question is
asked in `clarify-questions.md`. The counts are for the cross-cutting section
above; the 16 built-in items before it carry no ids and are not counted.

Plan notes: none.

All 17 checklists: 414 items: 373 pass, 25 fixed in the spec, 0 open, 16 plan
notes (PN-1 to PN-18 but PN-4 and PN-11, withdrawn on 2026-10-21; PN-2 narrowed
to an exception of any other kind in human mode and widened to a failed write's
standard-error line), 0 new questions. Recounted by script on 2026-10-21, and
again after the re-check, after the W6 read and after the fourth to twelfth
passes of that day, and after the thirteenth to fifteenth passes on 2026-10-22.
