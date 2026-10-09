Lane: openRepoProject-2

# Specification Quality Checklist: Safe batch worktree cleanup

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-10-09
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs): no language,
  framework, module or function is named; flags, codes, JSON fields and Git
  settings are behaviour the ratified deltas fix (spec, Assumptions).
- [x] Focused on user value and business needs: each of the nine stories
  says what the person gains and why it has its priority.
- [x] Written for non-technical stakeholders: passes on the deviation the
  spec records, as in features 002 and 003; its readers own, review and use
  `project` and the tools that read its JSON.
- [x] All mandatory sections completed: User Scenarios & Testing,
  Requirements and Success Criteria are filled, in the template's order,
  followed by Assumptions, Dependencies and Out of Scope.

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain: 0 in the spec; open question
  2 (squash merges) is deferred to a follow-on change, not left open here.
- [x] Requirements are testable and unambiguous: 67 FRs, each a MUST with an
  observable outcome and a trace to a requirement header or decision by name.
- [x] Success criteria are measurable: 14 SCs, each a count, bound, ratio or
  verbatim match (64 s, 300 s, 5 s, 128/256 rows, 16 targets, 0 network
  calls, 100 scenarios, 96 tests).
- [x] Success criteria are technology-agnostic (no implementation details):
  passes on the same recorded deviation; no language or test mechanism named.
- [x] All acceptance scenarios are defined: 73 Given/When/Then scenarios over
  9 stories, which list all 100 delta scenario titles, each exactly once.
- [x] Edge cases are identified: EC-001 to EC-019, drawn from the design's
  Risks, D3, D10 and D14 and the deltas' boundary scenarios.
- [x] Scope is clearly bounded: Out of Scope follows the proposal's Out of
  Scope and the design's Non-Goals, and names every untouched requirement.
- [x] Dependencies and assumptions identified: features 001 to 003, the
  archived fix-parent-obstacle-wording, add-project-overview, governance
  tasks, runtime and CI; nine assumptions.

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria: every
  delta-traced FR is exercised by the delta scenarios its stories list;
  FR-062 and FR-064 to FR-067 carry their own criteria (SC-012, SC-014).
- [x] User scenarios cover primary flows: preview, apply, named removal,
  push, plain report, JSON, and status, doctor and update.
- [x] Feature meets measurable outcomes defined in Success Criteria: each SC
  rests on FRs (SC-004 on FR-029 and FR-030, SC-008 on FR-037, and so on).
- [x] No implementation details leak into specification: the one leak found
  (a test file path in FR-066) was removed in iteration 1.

## Notes

- Final state: 16 of 16 items pass after 3 validation iterations (of 3
  allowed).
- Iteration 1 failed two items, both fixed in the spec:
  - "Requirements are testable and unambiguous": US1 scenario 4 said any
    change to a selected row changes the digest, though the digest covers
    only `[path, branch, head]` (now "a selected row's branch advances");
    US2 scenario 4's rename clause read as applying to the named removal;
    US6 scenario 4 said a failed probe on the merge-target checkout refused
    with exit 2 before this change (only an unreadable path and a failed
    root status did); FR-007 gave `remote-gone` to "unmerged" rows where the
    delta says "otherwise" (a null `merged_into_target` included); FR-021
    let a branch with a movement pass "whatever its head", skipping the
    head test (now conditioned on FR-022); FR-047 pointed branch deletion's
    incomplete-inspection refusal at FR-010, which covers push only; EC-014
    called every report above 128 rows complete; US6's priority note
    credited the survey with the fit test's result; and US4 scenario 1
    lacked "Admin registration changed"'s fresh-plan clause.
  - "No implementation details leak into specification": FR-066's trace
    named the test file; it now cites the proposal's Impact.
- Iteration 2 failed one item, fixed in the spec:
  - "Dependencies and assumptions identified": the feature 003 dependency
    implied this branch took it by a merge, though the branch was cut from a
    `main` already holding it; and the assumption on quoted texts omitted the
    README sentence that FR-065 quotes from the proposal.
- Iteration 3: every item passes. Checked by script: all 100 delta scenario
  titles listed once; all 17 requirement headers traced by at least one FR;
  no dangling FR reference; every quoted output text verbatim in the change;
  ASCII only; no line over 79 columns; no host-absolute path; 0 markers.
- The 10 canonical scenarios the modified requirements keep were compared by
  script with `openspec/specs/` and are byte-identical in the deltas (SC-011).
- The existing suite on this branch at `961c405` ran 96 tests, all passing
  (`python3 -m unittest discover -s tests -v`), the figure SC-012 states.
- Items marked incomplete require spec updates before `/speckit-clarify` or `/speckit-plan`
