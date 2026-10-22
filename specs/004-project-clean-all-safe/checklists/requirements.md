Lane: openRepoProject-2

# Specification Quality Checklist: Safe batch worktree cleanup

**Purpose**: Validate specification completeness and quality before
proceeding to planning
**Created**: 2026-10-09
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs): passes on a
  recorded deviation, not outright. Flags, codes, JSON fields and Git
  settings are behaviour the ratified deltas fix (spec, Assumptions). Two
  more mechanisms are named because the change fixes them: the interpreter's
  Unicode category source in FR-039, and the test launcher, counting `git`
  wrapper and fake Gits in FR-066.
- [x] Focused on user value and business needs: each of the nine stories
  says what the person gains and why it has its priority.
- [x] Written for non-technical stakeholders: passes on the deviation the
  spec records, as in features 002 and 003; its readers own, review and use
  `project` and the tools that read its JSON.
- [x] All mandatory sections completed: User Scenarios & Testing,
  Requirements and Success Criteria are filled, in the template's order,
  followed by Assumptions, Dependencies and Out of Scope.

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain: 0 in the spec, passing on a
  recorded deviation. Two questions still stand before Brett Heap, open
  question 2 (squash merges; LQ-2) and the push-child exception (draft PR #19;
  LQ-3). Each is recorded in the Assumptions, which keep the ratified text
  until he rules, instead of being marked; neither is settled or deferred by
  this spec.
- [x] Requirements are testable and unambiguous: passes on a recorded
  deviation. 67 FRs, each a MUST with an observable outcome and a trace to a
  requirement header or decision by name; the review's corrections to FR-016,
  FR-018, FR-021, FR-022, FR-034, FR-039, FR-046, FR-055, FR-066 and FR-067 are
  applied, and so are lane 3's restatements of FR-010, FR-029, FR-030, FR-033,
  FR-034, FR-036, FR-040, FR-047, FR-049, FR-051, FR-055 and FR-059, which
  close its contradictions between the run and budget bounds and the unbounded
  push and branch-deletion children, and between FR-049 and FR-014. The one
  contradiction left is the ratified text's own: FR-054 and SC-003 against
  FR-010's push, US3 scenario 6 and two baseline tests, pending Brett Heap's
  word on draft PR #19 (Assumptions).
- [x] Success criteria are measurable: 14 SCs, each a count, bound, ratio or
  verbatim match (64 s, 300 s, 5 s, 128/256 rows, 16 targets, 0 network
  calls, 100 scenarios, 96 tests), SC-014 a review of named contents of the
  README section; SC-002, SC-004, SC-005, SC-008 and SC-013 were restated to
  say what the deltas say, no more and no less, and SC-006 now says which Git
  children `probes.performed` counts and which `operations.performed` counts.
- [x] Success criteria are technology-agnostic (no implementation details):
  passes on the same recorded deviation. The earlier note, that no test
  mechanism is named, was wrong: SC-003 and SC-006 name a counting wrapper
  and SC-012 names the shared handling of Git children, because those
  criteria are measured through them.
- [x] All acceptance scenarios are defined: 73 Given/When/Then scenarios over
  9 stories, which list all 100 delta scenario titles, each exactly once;
  the review's 11 clause-level gaps (N-1 a to k) are closed, as are lane 3's
  remaining gaps in US2 scenario 7, US4 scenarios 4 and 6 and US8 scenario 1,
  and none of the 73 was added, moved or renumbered.
- [x] Edge cases are identified: EC-001 to EC-019, drawn from the design's
  Risks, D3, D10 and D14 and the deltas' boundary scenarios; EC-004 now says
  that reflog entries expire only when `git reflog expire` runs, EC-001 that
  open question 2 is still before Brett Heap, and EC-012 that the stuck-call
  exception covers runs with no removal, push or branch-deletion child in
  flight.
- [x] Scope is clearly bounded: Out of Scope follows the proposal's Out of
  Scope and the design's Non-Goals, and names every untouched requirement.
- [x] Dependencies and assumptions identified: features 001 to 003, the
  archived fix-parent-obstacle-wording, add-project-overview, governance
  tasks, runtime and CI; twelve assumptions, three of them recording the open
  squash-merge question, the push conflict and the count of probes and
  operations, and draft PR #19 as a dependency.

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria: every
  delta-traced FR is exercised by the delta scenarios its stories list;
  SC-012 measures FR-062, FR-064, FR-066 and FR-067, and SC-014 FR-065.
  FR-063 restates rules that SC-002, SC-003 and SC-011 measure; its clause
  that `project` never runs `git worktree prune`, `repair`, `lock` or
  `unlock` has no criterion of its own and is observable only in the
  counting wrapper's record of every child (FR-066).
- [x] User scenarios cover primary flows: preview, apply, named removal,
  push, plain report, JSON, and status, doctor and update.
- [x] Feature meets measurable outcomes defined in Success Criteria: each SC
  rests on FRs (SC-004 on FR-029 and FR-030, SC-008 on FR-037, SC-013 on
  FR-050 and FR-052, and so on).
- [x] No implementation details leak into specification: passes on the same
  recorded deviation. The one leak found in iteration 1 (a test file path
  in FR-066) was removed; FR-039 names the interpreter's
  `unicodedata.category` and FR-066 the test launcher, as the change does.

## Notes

- Final state: 16 of 16 items pass, six of them (items 1, 3, 5, 6, 8 and 16) on
  a recorded deviation. The first pass marked 16 of 16 after 3 validation
  iterations (of 3 allowed) and overclaimed in the places listed under the
  review rounds below; this file re-assesses every item against the spec as
  fixed.
- Iteration 1 failed two items, both fixed in the spec:
  - "Requirements are testable and unambiguous": US1 scenario 4 said any
    change to a selected row changes the digest, though the digest covers
    only `[path, branch, head]` (now "a selected row's branch advances");
    US2 scenario 4's rename clause read as applying to the named removal;
    US6 scenario 4 said a failed probe on the merge-target checkout refused
    with exit 2 before this change (only an unreadable path and a failed
    root status did); FR-007 gave `remote-gone` to "unmerged" rows where the
    delta says "otherwise" (a null `merged_into_target` included); FR-021
    let a branch with a movement "pass whatever its head", skipping the
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
- Iteration 3: every item passed on the checks then run: all 100 delta
  scenario titles listed once; all 17 requirement headers traced by at least
  one FR; no dangling FR reference; every quoted output text verbatim in the
  change; ASCII only; no host-absolute path; 0 markers. Its claim of no
  line over 79 columns was false: nine headings of the spec and two lines
  of this file were longer.
- Adversarial review round on `4e4b00f`: 4 blockers (B-1 to B-4), 7 majors
  (J-1 to J-7) and 13 minors (N-1 to N-13), all applied to the spec with no
  id renumbered and no scenario added. Overclaims in this file, corrected
  above: the 79-column claim; FR-062 and FR-064 credited with criteria that
  no SC stated (SC-012 now states them); no language, function, module or
  test mechanism named, when FR-039, FR-066 and three SCs name one; and a
  16 of 16 pass that did not separate the deviations.
- Second review round, lane 3 on `4e4b00f` (1 HIGH, 9 MEDIUM and 11 LOW
  findings), applied under the lead's dispositions of 2026-10-11 with no id
  renumbered and no scenario added. Already fixed at `aadd709`: M4, M6, M7, L2
  and L3. Applied here: H1 as an Assumption, with "exhaustively specified"
  dropped and FR-054 and SC-003 kept as ratified; M1, the squash-merge question
  restated as open in EC-001, the Assumptions and Out of Scope; M2 and M3 as
  restatements of FR-029, FR-030, FR-059, EC-012 and FR-049; M5 in FR-051; M8
  in FR-033 and the Assumptions; M9 in this file; and L1, L4 to L11 in FR-010,
  FR-040, FR-034, FR-047, FR-036, US7 scenario 6, FR-007, the acceptance
  scenarios and FR-055. L10 is closed in US4 scenarios 4 and 6 and US8 scenario
  1, and US2 scenario 7 only gains the cause of an expired reflog, its head
  variants being in since `aadd709`.
- Checked again after the fixes, by script or command: all 100 delta
  scenario titles are listed exactly once (65, 18 and 17 by capability;
  the after-confirmation clauses that "Hidden local state" and "Submodules"
  share with User Story 4 scenario 2 sit in a paragraph outside the
  lists); 73 acceptance scenarios (9, 10, 9, 8, 9, 8, 6, 4, 10); 67 FRs, 14
  SCs and 19 ECs in order; 17 requirement headers traced; every quoted
  output text verbatim in the change; ASCII only; no line over 79 columns;
  no em dash or host-absolute path; no line-number citation but the two
  baseline tests of the push conflict, pinned at `961c405`, in the Assumptions;
  0 markers.
- The 10 canonical scenarios the modified requirements keep were compared by
  script with `openspec/specs/` and are byte-identical in the deltas
  (SC-011).
- The existing suite on this branch ran 96 tests, all passing
  (`python3 -m unittest discover -s tests -v`), at `961c405` and again in
  the review round on the tree of `4e4b00f`; the figure SC-012 states, and once
  more after the second review round's fixes, where it ran 96 tests, all
  passing.
- Doc round 13 (2026-10-21) brought spec.md to 004 at `cceb6d7` and to
  draft PR #19 at `6f2cb54`, for Brett Heap's rulings Q9 B and LQ-10 to
  LQ-15 that 004 builds (LQ-13 held): FR-068 makes 68 FRs; User Story 9
  gains acceptance scenario 11, 74 in all; the delta-scenario lists of User
  Stories 2, 3, 4 and 9 add the thirteen of PR #19's titles that 004 builds,
  each once, which traceability.md traces. The
  counts above are those of the review rounds.
- Items marked incomplete require spec updates before `/speckit-clarify`
  or `/speckit-plan`
