Lane: openRepoProject-1

# Traceability: delta scenarios to tests

One row per scenario of the ratified spec delta
(`openspec/changes/fix-parent-obstacle-wording/specs/project-command/spec.md`),
by requirement and scenario title, in file order. The FRs column names the
functional requirements of `spec.md` the scenario realizes; FR-010 (the README
sentence, checked by `tasks.md` T014), FR-011 (ASCII, T013) and FR-012 (this
record) are not tied to one scenario. The Tests column names the test methods
in `tests/test_project.py` that cover the scenario: the two new methods, the
extended ones (the new rows and tables, named in `tasks.md` T004 to T006), and,
where a scenario's behaviour is unchanged, the existing tests that pin it
(`tasks.md` T002, T017). The scenario "The parent directory is missing" keeps
its title, so that feature 002's `traceability.md:37` still points at it.

| # | Requirement | Scenario | FRs | Tests |
| --- | --- | --- | --- | --- |
| 1 | Known Triad obstacles are named before the question and refused on a Triad answer | A name outside the assembly-root form | FR-001, FR-006 | `test_pty_name_outside_the_assembly_form_is_named` |
| 2 | Known Triad obstacles are named before the question and refused on a Triad answer | openRepoShape is not on PATH | FR-001, FR-006 | `test_pty_missing_openreposhape_is_named` |
| 3 | Known Triad obstacles are named before the question and refused on a Triad answer | The parent directory is missing | FR-002, FR-003, FR-005 | `test_pty_missing_parent_is_named_without_into`, `test_pty_triad_answer_with_an_obstacle_refuses` (the `parent` and `dangling link parent` rows), `test_inproc_triad_obstacle_runs_nothing` (the same rows), `test_pty_dry_run_with_an_obstacle_refuses` (the `parent` and `dangling link parent` rows) |
| 4 | Known Triad obstacles are named before the question and refused on a Triad answer | The parent exists but is not a directory | FR-002, FR-004, FR-005, FR-006 | `test_pty_missing_parent_is_named_without_into` (the file as parent by `--into`, by the positional parent, by `PROJECTS_DIR` and as the default `~/projects`), `test_pty_triad_answer_with_an_obstacle_refuses` (the `file parent`, `link to the file parent` and `all three with the file parent` rows), `test_inproc_triad_obstacle_runs_nothing` (the same rows), `test_pty_dry_run_with_an_obstacle_refuses` (the `file parent` and `link to the file parent` rows) |
| 5 | Known Triad obstacles are named before the question and refused on a Triad answer | A Triad answer with a known obstacle | FR-001, FR-004, FR-006, FR-007 | `test_pty_triad_answer_with_an_obstacle_refuses`, `test_inproc_triad_obstacle_runs_nothing` |
| 6 | Known Triad obstacles are named before the question and refused on a Triad answer | A dry run with a known obstacle | FR-007 | `test_pty_dry_run_with_an_obstacle_refuses` |
| 7 | Known Triad obstacles are named before the question and refused on a Triad answer | A single-repository answer is unaffected | FR-008 | `test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path`, `test_pty_single_answer_is_unaffected_by_obstacles` |
| 8 | Known Triad obstacles are named before the question and refused on a Triad answer | No known obstacle | FR-009 | `test_pty_symbolic_link_to_a_directory_names_no_obstacle`, `test_pty_no_known_obstacle_names_none` |
