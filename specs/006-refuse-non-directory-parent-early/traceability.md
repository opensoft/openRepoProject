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
| 1 | A parent blocked by a non-directory is refused before the single-repository path's steps | A flag-chosen single repository with a parent that is not a directory | FR-001, FR-003, FR-005 | `test_blocked_parent_by_flag_is_refused_before_the_plan`, `test_blocked_parent_is_refused_without_a_terminal`, `test_pty_blocked_parent_by_type_without_yes_is_refused`, `test_pty_blocked_parent_is_refused_where_ci_is_true`, `test_pty_blocked_parent_is_refused_for_a_workspace_name` |
| 2 | A parent blocked by a non-directory is refused before the single-repository path's steps | A flag-chosen single repository below a path that is not a directory | FR-001, FR-003, FR-005 | `test_blocked_parent_by_flag_is_refused_before_the_plan`, `test_pty_blocked_parent_by_type_without_yes_is_refused` |
| 3 | A parent blocked by a non-directory is refused before the single-repository path's steps | A single-repository dry run with a parent blocked by a non-directory | FR-003, FR-005 | `test_blocked_parent_by_flag_is_refused_before_the_plan`, `test_pty_blocked_parent_is_refused_for_a_workspace_name`, `test_pty_single_answer_with_a_blocked_parent_is_refused_at_once` |
| 4 | A parent blocked by a non-directory is refused before the single-repository path's steps | A single repository taken at the question with a parent blocked by a non-directory | FR-003, FR-005 | `test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path`, `test_pty_single_answer_with_a_blocked_parent_is_refused_at_once` |
| 5 | A parent blocked by a non-directory is refused before the single-repository path's steps | A parent repaired or broken while the question waits | FR-004 | `test_inproc_parent_repaired_while_the_question_waits_is_created`, `test_inproc_parent_broken_while_the_question_waits_is_refused` |
| 6 | A parent blocked by a non-directory is refused before the single-repository path's steps | A single repository with a parent that is not blocked | FR-001, FR-008 | `test_dangling_link_parent_is_created_as_before`, `test_new_preserves_paths_with_spaces_and_writes_profile`, `test_dry_run_creates_no_parent` |
| 7 | A parent blocked by a non-directory is refused before the single-repository path's steps | A parent the person cannot write still fails only at creation | FR-010 | `test_unwritable_directory_child_passes_dry_run_and_fails_at_creation` |
| 8 | A parent blocked by a non-directory is refused before the single-repository path's steps | The parent refusal comes after the earlier refusals | FR-003 | `test_earlier_refusals_keep_their_text_with_a_blocked_parent` |
| 9 | A parent blocked by a non-directory is refused before the single-repository path's steps | The parent refusal comes before generator selection | FR-003 | `test_blocked_parent_is_refused_before_later_faults` |
| 10 | A parent blocked by a non-directory is refused before the single-repository path's steps | The shape branch's parent refusal is unchanged | FR-009 | `test_shape_by_flag_keeps_its_parent_refusal_with_a_blocked_parent` |
| 11 | Delegate project creation | Preview | FR-005, FR-008 | `test_pty_dry_run_single_answer_prints_the_generator_plan`, `test_advisory_silent_cases`, `test_dry_run_creates_no_parent` |
| 12 | Delegate project creation | Existing project | FR-011 | `test_pty_refusals_before_a_path_come_first` |
| 13 | Delegate project creation | Shape chosen by flag | FR-011 | `test_pty_shape_chosen_by_flag_keeps_openreposhape_confirmation`, `test_advisory_silent_cases` |
| 14 | Delegate project creation | An answer is not a confirmation | FR-011 | `test_pty_single_answer_is_not_a_confirmation`, `test_pty_triad_delegates_without_yes_and_keeps_its_confirmation` |
| 15 | Creation question is asked only of a person choosing at the terminal | A person at the terminal without a choosing flag | FR-011 | `test_pty_question_is_asked_once_the_name_is_known` |
| 16 | Creation question is asked only of a person choosing at the terminal | A choosing flag skips the question | FR-011 | `test_pty_choosing_flags_skip_the_question` |
| 17 | Creation question is asked only of a person choosing at the terminal | Not at a terminal | FR-011 | `test_inproc_person_at_terminal_rule`, `test_new_without_a_terminal_is_not_asked`, `test_inproc_stdout_not_a_terminal_is_not_asked` |
| 18 | Creation question is asked only of a person choosing at the terminal | CI is set | FR-011 | `test_inproc_person_at_terminal_rule`, `test_pty_ci_decides_the_question` |
| 19 | Creation question is asked only of a person choosing at the terminal | A workspace name | FR-011 | `test_pty_workspace_name_is_not_asked_or_advised`, `test_workspace_name_by_flag_gives_no_advisory` |
| 20 | Creation question is asked only of a person choosing at the terminal | A dry run asks too | FR-003, FR-005 | `test_pty_dry_run_single_answer_prints_the_generator_plan`, `test_pty_single_answer_with_a_blocked_parent_is_refused_at_once` |
| 21 | Creation question is asked only of a person choosing at the terminal | Refusals before a path is chosen come first | FR-011 | `test_pty_refusals_before_a_path_come_first` |
| 22 | Creation question is asked only of a person choosing at the terminal | The workflow prerequisite is refused before the question | FR-011 | `test_pty_workflow_prerequisite_is_refused_before_the_question` |
| 23 | Creation question is asked only of a person choosing at the terminal | The refusal order of an invocation not asked the question is unchanged | FR-003 | `test_workflow_refusal_order_unchanged_when_not_asked` |
| 24 | Creation question offers the Triad first | The question's entries | FR-011 | `test_pty_question_entries` |
| 25 | Creation question offers the Triad first | Answers that take the Triad | FR-011 | `test_pty_answers_that_take_the_triad` |
| 26 | Creation question offers the Triad first | Answers that take a single repository | FR-003, FR-008 | `test_pty_single_answers_take_the_bench_path`, `test_pty_single_answer_with_a_blocked_parent_is_refused_at_once` |
| 27 | Creation question offers the Triad first | One unrecognised answer | FR-011 | `test_pty_one_unrecognised_answer_is_asked_again` |
| 28 | Creation question offers the Triad first | Two unrecognised answers | FR-011 | `test_pty_two_unrecognised_answers_refuse` |
| 29 | Creation question offers the Triad first | End of input at the question | FR-011 | `test_pty_end_of_input_at_the_question_refuses` |
| 30 | Creation question offers the Triad first | An interrupt at the question | FR-011 | `test_pty_interrupt_at_the_question_cancels` |
| 31 | Creation question offers the Triad first | End of input at an existing prompt is unchanged | FR-011 | `test_pty_end_of_input_at_existing_prompts_is_unchanged` |
| 32 | Known Triad obstacles are named before the question and refused on a Triad answer | A name outside the assembly-root form | FR-011 | `test_pty_name_outside_the_assembly_form_is_named` |
| 33 | Known Triad obstacles are named before the question and refused on a Triad answer | openRepoShape is not on PATH | FR-011 | `test_pty_missing_openreposhape_is_named` |
| 34 | Known Triad obstacles are named before the question and refused on a Triad answer | The parent directory is missing | FR-006 | `test_pty_missing_parent_is_named_without_into`, `test_pty_triad_answer_with_an_obstacle_refuses` (the `parent` and `dangling link parent` rows), `test_inproc_triad_obstacle_runs_nothing` (the same rows), `test_pty_dry_run_with_an_obstacle_refuses` (the `parent` and `dangling link parent` rows) |
| 35 | Known Triad obstacles are named before the question and refused on a Triad answer | The parent exists but is not a directory | FR-006 | `test_pty_missing_parent_is_named_without_into` (the file as parent by `--into`, by the positional parent, by `PROJECTS_DIR` and as the default `~/projects`), `test_pty_triad_answer_with_an_obstacle_refuses` (the `file parent`, `link to the file parent` and `all three with the file parent` rows), `test_inproc_triad_obstacle_runs_nothing` (the same rows), `test_pty_dry_run_with_an_obstacle_refuses` (the `file parent` and `link to the file parent` rows) |
| 36 | Known Triad obstacles are named before the question and refused on a Triad answer | The parent would be created below a path that is not a directory | FR-006, FR-007 | `test_pty_triad_answer_with_an_obstacle_refuses`, `test_inproc_triad_obstacle_runs_nothing`, `test_pty_dry_run_with_an_obstacle_refuses`, `test_pty_triad_answer_below_a_file_leaves_the_file_intact`, `test_inproc_triad_answer_below_a_file_leaves_the_file_intact` |
| 37 | Known Triad obstacles are named before the question and refused on a Triad answer | A Triad answer with a known obstacle | FR-007 | `test_pty_triad_answer_with_an_obstacle_refuses`, `test_inproc_triad_obstacle_runs_nothing`, `test_pty_triad_answer_below_a_file_leaves_the_file_intact`, `test_inproc_triad_answer_below_a_file_leaves_the_file_intact` |
| 38 | Known Triad obstacles are named before the question and refused on a Triad answer | A dry run with a known obstacle | FR-007 | `test_pty_dry_run_with_an_obstacle_refuses` |
| 39 | Known Triad obstacles are named before the question and refused on a Triad answer | A single-repository answer is unaffected | FR-008 | `test_pty_single_answer_is_unaffected_by_obstacles` |
| 40 | Known Triad obstacles are named before the question and refused on a Triad answer | No known obstacle | FR-011 | `test_pty_symbolic_link_to_a_directory_names_no_obstacle`, `test_pty_no_known_obstacle_names_none` |
