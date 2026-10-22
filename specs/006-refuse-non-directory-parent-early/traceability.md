Lane: openRepoProject-1

# Traceability: delta scenarios to tests

One row per scenario of the ratified spec delta
(`openspec/changes/refuse-non-directory-parent-early/specs/project-command/spec.md`),
by requirement and scenario title, in file order: 40 rows. The FRs column names
the functional requirements of `spec.md` the scenario realizes; no row names
FR-002 or FR-012 to FR-016, which are not tied to one scenario. The Tests
column names the test methods in `tests/test_project.py` that cover the
scenario. For the 20 scenarios that this feature adds, alters or re-pins
(plan.md, "Coverage map"), the cell reads `pending (T028)` until `tasks.md`
T028 fills it with the tests the plan maps. The other 20 scenarios are
unchanged by this feature (FR-011): their cells are feature 002's
`traceability.md` cells for the same title, copied byte for byte, except "No
known obstacle", which takes feature 003's cell
(`specs/003-parent-obstacle-wording/traceability.md`, row 8).

| # | Requirement | Scenario | FRs | Tests |
| --- | --- | --- | --- | --- |
| 1 | A parent blocked by a non-directory is refused before the single-repository path's steps | A flag-chosen single repository with a parent that is not a directory | FR-001, FR-003, FR-005 | pending (T028) |
| 2 | A parent blocked by a non-directory is refused before the single-repository path's steps | A flag-chosen single repository below a path that is not a directory | FR-001, FR-003, FR-005 | pending (T028) |
| 3 | A parent blocked by a non-directory is refused before the single-repository path's steps | A single-repository dry run with a parent blocked by a non-directory | FR-003, FR-005 | pending (T028) |
| 4 | A parent blocked by a non-directory is refused before the single-repository path's steps | A single repository taken at the question with a parent blocked by a non-directory | FR-003, FR-005 | pending (T028) |
| 5 | A parent blocked by a non-directory is refused before the single-repository path's steps | A parent repaired or broken while the question waits | FR-004 | pending (T028) |
| 6 | A parent blocked by a non-directory is refused before the single-repository path's steps | A single repository with a parent that is not blocked | FR-001, FR-008 | pending (T028) |
| 7 | A parent blocked by a non-directory is refused before the single-repository path's steps | A parent the person cannot write still fails only at creation | FR-010 | pending (T028) |
| 8 | A parent blocked by a non-directory is refused before the single-repository path's steps | The parent refusal comes after the earlier refusals | FR-003 | pending (T028) |
| 9 | A parent blocked by a non-directory is refused before the single-repository path's steps | The parent refusal comes before generator selection | FR-003 | pending (T028) |
| 10 | A parent blocked by a non-directory is refused before the single-repository path's steps | The shape branch's parent refusal is unchanged | FR-009 | pending (T028) |
| 11 | Delegate project creation | Preview | FR-005, FR-008 | pending (T028) |
| 12 | Delegate project creation | Existing project | FR-011 | `test_pty_refusals_before_a_path_come_first` |
| 13 | Delegate project creation | Shape chosen by flag | FR-011 | `test_pty_shape_chosen_by_flag_keeps_openreposhape_confirmation`, `test_advisory_silent_cases` |
| 14 | Delegate project creation | An answer is not a confirmation | FR-011 | `test_pty_single_answer_is_not_a_confirmation`, `test_pty_triad_delegates_without_yes_and_keeps_its_confirmation` |
| 15 | Creation question is asked only of a person choosing at the terminal | A person at the terminal without a choosing flag | FR-011 | `test_pty_question_is_asked_once_the_name_is_known` |
| 16 | Creation question is asked only of a person choosing at the terminal | A choosing flag skips the question | FR-011 | `test_pty_choosing_flags_skip_the_question` |
| 17 | Creation question is asked only of a person choosing at the terminal | Not at a terminal | FR-011 | `test_inproc_person_at_terminal_rule`, `test_new_without_a_terminal_is_not_asked`, `test_inproc_stdout_not_a_terminal_is_not_asked` |
| 18 | Creation question is asked only of a person choosing at the terminal | CI is set | FR-011 | `test_inproc_person_at_terminal_rule`, `test_pty_ci_decides_the_question` |
| 19 | Creation question is asked only of a person choosing at the terminal | A workspace name | FR-011 | `test_pty_workspace_name_is_not_asked_or_advised`, `test_workspace_name_by_flag_gives_no_advisory` |
| 20 | Creation question is asked only of a person choosing at the terminal | A dry run asks too | FR-003, FR-005 | pending (T028) |
| 21 | Creation question is asked only of a person choosing at the terminal | Refusals before a path is chosen come first | FR-011 | `test_pty_refusals_before_a_path_come_first` |
| 22 | Creation question is asked only of a person choosing at the terminal | The workflow prerequisite is refused before the question | FR-011 | `test_pty_workflow_prerequisite_is_refused_before_the_question` |
| 23 | Creation question is asked only of a person choosing at the terminal | The refusal order of an invocation not asked the question is unchanged | FR-003 | pending (T028) |
| 24 | Creation question offers the Triad first | The question's entries | FR-011 | `test_pty_question_entries` |
| 25 | Creation question offers the Triad first | Answers that take the Triad | FR-011 | `test_pty_answers_that_take_the_triad` |
| 26 | Creation question offers the Triad first | Answers that take a single repository | FR-003, FR-008 | pending (T028) |
| 27 | Creation question offers the Triad first | One unrecognised answer | FR-011 | `test_pty_one_unrecognised_answer_is_asked_again` |
| 28 | Creation question offers the Triad first | Two unrecognised answers | FR-011 | `test_pty_two_unrecognised_answers_refuse` |
| 29 | Creation question offers the Triad first | End of input at the question | FR-011 | `test_pty_end_of_input_at_the_question_refuses` |
| 30 | Creation question offers the Triad first | An interrupt at the question | FR-011 | `test_pty_interrupt_at_the_question_cancels` |
| 31 | Creation question offers the Triad first | End of input at an existing prompt is unchanged | FR-011 | `test_pty_end_of_input_at_existing_prompts_is_unchanged` |
| 32 | Known Triad obstacles are named before the question and refused on a Triad answer | A name outside the assembly-root form | FR-011 | `test_pty_name_outside_the_assembly_form_is_named` |
| 33 | Known Triad obstacles are named before the question and refused on a Triad answer | openRepoShape is not on PATH | FR-011 | `test_pty_missing_openreposhape_is_named` |
| 34 | Known Triad obstacles are named before the question and refused on a Triad answer | The parent directory is missing | FR-006 | pending (T028) |
| 35 | Known Triad obstacles are named before the question and refused on a Triad answer | The parent exists but is not a directory | FR-006 | pending (T028) |
| 36 | Known Triad obstacles are named before the question and refused on a Triad answer | The parent would be created below a path that is not a directory | FR-006, FR-007 | pending (T028) |
| 37 | Known Triad obstacles are named before the question and refused on a Triad answer | A Triad answer with a known obstacle | FR-007 | pending (T028) |
| 38 | Known Triad obstacles are named before the question and refused on a Triad answer | A dry run with a known obstacle | FR-007 | pending (T028) |
| 39 | Known Triad obstacles are named before the question and refused on a Triad answer | A single-repository answer is unaffected | FR-008 | pending (T028) |
| 40 | Known Triad obstacles are named before the question and refused on a Triad answer | No known obstacle | FR-011 | `test_pty_symbolic_link_to_a_directory_names_no_obstacle`, `test_pty_no_known_obstacle_names_none` |
