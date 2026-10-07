Lane: openRepoProject-1

# Traceability: delta scenarios to tests

One row per scenario of the ratified spec delta
(`openspec/changes/prefer-triad-in-project-new/specs/project-command/spec.md`),
by requirement and scenario title, in file order. The Tests column names the
test methods in `tests/test_project.py` that cover the scenario; each test task
fills it as its test lands (`tasks.md` T002), and T066 checks that no cell is
empty and that every named test is defined.

| # | Requirement | Scenario | Tests |
| --- | --- | --- | --- |
| 1 | Delegate project creation | Preview | `test_pty_dry_run_single_answer_prints_the_generator_plan`, `test_pty_dry_run_triad_answer_prints_the_openreposhape_plan` |
| 2 | Delegate project creation | Existing project | `test_pty_refusals_before_a_path_come_first` |
| 3 | Delegate project creation | Shape chosen by flag | |
| 4 | Delegate project creation | An answer is not a confirmation | `test_pty_single_answer_is_not_a_confirmation`, `test_pty_triad_delegates_without_yes_and_keeps_its_confirmation` |
| 5 | Creation question is asked only of a person choosing at the terminal | A person at the terminal without a choosing flag | `test_pty_question_is_asked_once_the_name_is_known` |
| 6 | Creation question is asked only of a person choosing at the terminal | A choosing flag skips the question | |
| 7 | Creation question is asked only of a person choosing at the terminal | Not at a terminal | `test_inproc_person_at_terminal_rule` |
| 8 | Creation question is asked only of a person choosing at the terminal | CI is set | `test_inproc_person_at_terminal_rule` |
| 9 | Creation question is asked only of a person choosing at the terminal | A workspace name | |
| 10 | Creation question is asked only of a person choosing at the terminal | A dry run asks too | `test_pty_dry_run_single_answer_prints_the_generator_plan`, `test_pty_dry_run_triad_answer_prints_the_openreposhape_plan` |
| 11 | Creation question is asked only of a person choosing at the terminal | Refusals before a path is chosen come first | `test_pty_refusals_before_a_path_come_first` |
| 12 | Creation question is asked only of a person choosing at the terminal | The workflow prerequisite is refused before the question | |
| 13 | Creation question is asked only of a person choosing at the terminal | The refusal order of an invocation not asked the question is unchanged | |
| 14 | Creation question offers the Triad first | The question's entries | `test_pty_question_entries` |
| 15 | Creation question offers the Triad first | Answers that take the Triad | `test_pty_answers_that_take_the_triad` |
| 16 | Creation question offers the Triad first | Answers that take a single repository | `test_pty_single_answers_take_the_bench_path` |
| 17 | Creation question offers the Triad first | One unrecognised answer | `test_pty_one_unrecognised_answer_is_asked_again` |
| 18 | Creation question offers the Triad first | Two unrecognised answers | `test_pty_two_unrecognised_answers_refuse` |
| 19 | Creation question offers the Triad first | End of input at the question | `test_pty_end_of_input_at_the_question_refuses` |
| 20 | Creation question offers the Triad first | An interrupt at the question | `test_pty_interrupt_at_the_question_cancels` |
| 21 | Creation question offers the Triad first | End of input at an existing prompt is unchanged | `test_pty_end_of_input_at_existing_prompts_is_unchanged` |
| 22 | Known Triad obstacles are named before the question and refused on a Triad answer | A name outside the assembly-root form | |
| 23 | Known Triad obstacles are named before the question and refused on a Triad answer | openRepoShape is not on PATH | |
| 24 | Known Triad obstacles are named before the question and refused on a Triad answer | The parent directory is missing | |
| 25 | Known Triad obstacles are named before the question and refused on a Triad answer | A Triad answer with a known obstacle | |
| 26 | Known Triad obstacles are named before the question and refused on a Triad answer | A dry run with a known obstacle | |
| 27 | Known Triad obstacles are named before the question and refused on a Triad answer | A single-repository answer is unaffected | |
| 28 | Known Triad obstacles are named before the question and refused on a Triad answer | No known obstacle | |
| 29 | A Triad answer asks for the organization and the visibility | Organization first, then visibility | `test_pty_organization_then_visibility` |
| 30 | A Triad answer asks for the organization and the visibility | The visibility is a full word | `test_pty_visibility_is_a_full_word` |
| 31 | A Triad answer asks for the organization and the visibility | Asked once more, then refused | `test_pty_two_misses_at_organization_or_visibility_refuse` |
| 32 | A Triad answer asks for the organization and the visibility | End of input at the organization or visibility prompt | `test_pty_end_of_input_at_organization_or_visibility_refuses` |
| 33 | A Triad answer asks for the organization and the visibility | An interrupt at the organization or visibility prompt | `test_pty_interrupt_at_organization_or_visibility_cancels` |
| 34 | A Triad answer asks for the organization and the visibility | The restating line | `test_pty_restating_line_precedes_the_plan` |
| 35 | A Triad answer asks for the organization and the visibility | Delegation keeps openRepoShape's confirmation | `test_pty_triad_delegates_without_yes_and_keeps_its_confirmation` |
| 36 | A Triad answer asks for the organization and the visibility | openRepoShape refuses | `test_pty_openreposhape_refusal_passes_through` |
| 37 | Creation advisory follows a single repository created without the question | A single repository chosen by flag | |
| 38 | Creation advisory follows a single repository created without the question | A single repository created where the question is not asked | |
| 39 | Creation advisory follows a single repository created without the question | The advisory's content | |
| 40 | Creation advisory follows a single repository created without the question | A generator that initialises no Git repository | |
| 41 | Creation advisory follows a single repository created without the question | Silent cases | |
| 42 | Creation advisory follows a single repository created without the question | Standard error cannot be written | |
| 43 | Creation advisory follows a single repository created without the question | Never a report input | |
| 44 | Creation offer precedes the workflow follow-up | Two advisories back to back | |
| 45 | Creation offer precedes the workflow follow-up | The follow-up fails | |
| 46 | Creation offer precedes the workflow follow-up | A single-repository answer with --workflow | |
| 47 | Creation offer precedes the workflow follow-up | A workspace name with --workflow | |
