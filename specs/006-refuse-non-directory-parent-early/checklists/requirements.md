Lane: openRepoProject-1

# Specification Quality Checklist: Refuse a non-directory parent early

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-10-21
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

- **Final state**: 16 of 16 items pass, after 3 validation iterations (of
  3 allowed). The spec has 0 `[NEEDS CLARIFICATION]` markers.
- **Iteration 1** failed two items, each fixed in the spec:
  - "No implementation details leak into specification". FR-014's notes A1
    and A3 described test code: a fixture literal, a composing helper and
    the format fields `{PARENT}` and `{ANCESTOR}`. FR-011 named an
    "import". FR-014 now states only what the tests must establish: `FILE`
    and the tree unchanged for every case (b) run, and the head refusal's
    end pinned as fixed text of its own. FR-011 now says "dependency".
  - "Requirements are testable and unambiguous", three issues:
    - FR-001's last clause ("and neither may the target of a dangling
      symbolic link in that position") was unclear. It now says that a
      dangling link whose target is such a missing parent is included.
    - FR-011's "Nothing else MUST change" now reads "The feature MUST NOT
      change any other behaviour".
    - FR-012's README grep now says "exactly once", as User Story 6 and
      SC-009 do.
- **Iteration 2** failed one item, fixed in the spec:
  - "Requirements are testable and unambiguous". SC-001 said that the tests
    cover "each case (a) and case (b) kind in each of these forms", which
    contradicts the Assumptions entry "Test breadth". That entry makes
    `design.md` D3's matrix the minimum. SC-001 now reads "Across the kinds
    of `design.md` D3, the runs include each of these forms".
- **Iteration 3**: every item passes. The mechanical checks gave 0 markers,
  0 template placeholders and 0 non-ASCII characters, and every quoted
  string matches its source verbatim. The quoted strings are the README
  phrases "or a parent that is missing or is not a directory." and
  "Existing destinations refuse.", and the `design.md` D2 phrases
  "exactly as they would be without the question" and "unless a refusal
  comes first". One coverage gap was closed in the same pass: User Story 3
  scenario 4 now says "with or without `--dry-run`", for the delta's "A
  dry run with a known obstacle" on case (a) and the missing parent.
- **Delta coverage.** All 40 scenarios of the delta's 5 requirements are
  accounted for, and 24 of them are named by title in the spec:
  - User Story 5 scenario 8 names 22: the 20 scenarios that the feature
    does not alter, and 2 altered ones, for a parent that is not blocked;
  - FR-015 names 2 more.

  The tables below map each of the 20 scenarios that the feature adds or
  alters to the acceptance scenarios that realize it. 16 of them are named
  nowhere else in the spec.
  - ADDED requirement:

    | Delta scenario | Realized by |
    | --- | --- |
    | "A flag-chosen single repository with a parent that is not a directory" | US1 scenarios 1, 3 and 5 |
    | "A flag-chosen single repository below a path that is not a directory" | US1 scenarios 2 and 3 |
    | "A single-repository dry run with a parent blocked by a non-directory" | US1 scenario 4; US2 scenario 2 |
    | "A single repository taken at the question with a parent blocked by a non-directory" | US2 scenarios 1 and 3 |
    | "A parent repaired or broken while the question waits" | US4 scenarios 1 and 2 |
    | "A single repository with a parent that is not blocked" | US5 scenario 1 |
    | "A parent the person cannot write still fails only at creation" | US5 scenarios 4 and 5 |
    | "The parent refusal comes after the earlier refusals" | US5 scenario 2 |
    | "The parent refusal comes before generator selection" | US1 scenario 6 |
    | "The shape branch's parent refusal is unchanged" | US5 scenario 3 |

  - MODIFIED requirements:

    | Delta scenario | Realized by |
    | --- | --- |
    | "Preview" | US5 scenario 6 |
    | "A dry run asks too", for a blocked parent | US2 scenario 2 |
    | "The refusal order of an invocation not asked the question is unchanged" | US5 scenario 7 |
    | "Answers that take a single repository", for a blocked parent | US2 scenario 1 |
    | "The parent directory is missing" | US3 scenario 4 |
    | "The parent exists but is not a directory" | US3 scenario 4 |
    | "The parent would be created below a path that is not a directory" | US3 scenarios 1 to 3 |
    | "A Triad answer with a known obstacle" | US3 scenarios 2 and 4 |
    | "A dry run with a known obstacle" | US3 scenarios 3 and 4 |
    | "A single-repository answer is unaffected" | US2 scenario 4 |

  - The changed requirement bodies are FR-002 and FR-006 (the parent read),
    FR-003 (the refusal order) and FR-008 (the continuation clause).
- **Content-quality deviation.** "Written for non-technical stakeholders"
  and "Success criteria are technology-agnostic" pass on the deviation
  recorded under the spec's Assumptions, as in features 002 and 003. The
  ratified delta fixes flags, paths, standard streams and exit statuses as
  behaviour. SC-006 names the CI jobs, as 003's SC-006 did. No language,
  function, module, test method or test-harness API is named. FR-014 states
  test obligations only at the level that `design.md` D3 and D4 and report
  A's notes fix them.
- **Report notes.** Report A's notes are carried where they belong: A1 and
  A3 in FR-014, A2 in FR-003, and P1 in the Supersession. Agent K's
  symbolic-link loop is under Scope, owned by PR #28.
- The fixed strings are cited from `design.md` D2 and never restated in a
  different form.
- Items marked incomplete require spec updates before `/speckit-clarify` or `/speckit-plan`.
