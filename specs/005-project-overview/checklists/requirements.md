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
- Items marked incomplete require spec updates before `/speckit-clarify` or `/speckit-plan`

## Cross-cutting Requirements Quality (no-argument `/speckit.checklist`, 2026-10-19)

**Purpose**: The cross-cutting dimensions that the user-global `speckit-checklist` skill adds to this file on a no-argument run: completeness, clarity, consistency, acceptance criteria quality, dependencies and assumptions, and ambiguities and conflicts. The domain checklists of the same run sit beside this file. The 16 items above and their notes are unchanged; the items below are numbered from CHK001 because the items above carry no ids.
**Review Ownership**: These items are reviewer-owned, as in the domain checklists: `[x]` means the requirements-quality criterion is satisfied, never that implementation work is complete.

### Requirement Completeness

- [ ] CHK001 Does every ADDED and MODIFIED requirement of change 2's deltas map to at least one functional requirement? [Completeness, Traceability, Spec Appendix Requirements]
- [ ] CHK002 Does every delta scenario map to at least one functional requirement and exactly one story scenario? [Completeness, Traceability, Spec Appendix Scenarios]
- [ ] CHK003 Does each of FR-001 to FR-046 realize at least one row of the traceability tables, with FR-047 to FR-049 traced to the proposal's Impact and design D13? [Traceability, Spec Appendix Coverage]
- [ ] CHK004 Are requirements present for every scenario class the feature has: primary (a healthy estate), alternate (layouts, `--attention`, `--strict`), exception (one row's failure, a failure outside the boundary), recovery (remedies, repair, re-runs) and non-functional (bounds, read-only, determinism)? [Coverage, Spec US1 to US11, FR-011 to FR-022, FR-040]
- [ ] CHK005 Are the points the delta leaves to design D1 to D13 cited to the decision rather than restated in another form? [Completeness, Spec Requirements preamble, Assumptions]
- [ ] CHK006 Is every citation key the spec uses (`POD`, `PRSD`, `DI`, `CMD`, `CLN`, [E], [L], [G], [R], [P]) defined with the file and the commit it points at? [Traceability, Gap, Spec header]
- [ ] CHK007 Are the points the change leaves open recorded as questions for Brett Heap rather than settled in the spec? [Completeness, Spec Assumptions]
- [ ] CHK008 Is each clarification applied where its "Where applied" line says? [Consistency, Traceability, Spec Clarifications]

### Requirement Clarity

- [ ] CHK009 Are the bounds stated as numbers with units rather than adjectives? [Clarity, Spec FR-011 to FR-018, FR-033]
- [ ] CHK010 Are approximate quantities ("about 300 entries", "about 355 rows", "about 2 s") confined to edge cases, assumptions and scenarios that give an exact threshold beside them? [Clarity, Spec EC-004, EC-009, US6 s9]
- [ ] CHK011 Is every obligation written with MUST or MUST NOT, never as "no X MUST"? [Clarity, Spec Functional Requirements]
- [ ] CHK012 Does the spec say what and why, naming no function, module or file of the implementation? [Clarity, Spec Assumptions]

### Requirement Consistency

- [ ] CHK013 Are codes, classifications and field names spelled identically across stories, requirements, entities and criteria? [Consistency]
- [ ] CHK014 Do the stories' acceptance scenarios agree with the delta scenarios they realize? [Consistency, Spec Appendix Scenarios]
- [ ] CHK015 Are the exit rules consistent across FR-029, FR-042, FR-043, FR-044 and the stories? [Consistency, Spec FR-042]

### Acceptance Criteria Quality

- [ ] CHK016 Is each success criterion objectively measurable (a count, a percentage, a byte comparison or a time bound)? [Measurability, Spec SC-001 to SC-014]
- [ ] CHK017 Does each success criterion measure requirements that exist, by citation or by content? [Traceability, Spec SC-001 to SC-014]
- [ ] CHK018 Is every success criterion achievable, none requiring what a run cannot meet? [Measurability, Spec SC-004, SC-005]

### Dependencies and Assumptions

- [ ] CHK019 Is the dependency on feature 004 stated with the commit it is read at, and is the open choice of its state before the plan recorded? [Dependency, Spec Dependencies]
- [ ] CHK020 Are the measured assumptions stated with their source and date (48.3 s, 219 candidates, 96 tests)? [Assumption, Spec Assumptions]
- [ ] CHK021 Is the assumption that no other process changes the estate stated where determinism depends on it? [Assumption, Spec FR-019, EC-023]
- [ ] CHK022 Is the departure from the change's order (specify before feature 004 merges) recorded with its authority and its limit? [Assumption, Spec header, Clarifications C-21]

### Ambiguities and Conflicts

- [ ] CHK023 Is every point left to the plan named as such? [Ambiguity, Spec Assumptions]
- [ ] CHK024 Are the differences between change 2 and feature 004 recorded with which text governs? [Conflict, Spec Assumptions, Clarifications C-33]
- [ ] CHK025 Are the recorded residuals (EC-001, EC-002, EC-006, EC-022, EC-025 to EC-030) kept apart from requirements, so that none reads as a promise? [Ambiguity, Spec Edge Cases]
