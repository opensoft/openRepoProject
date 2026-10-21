Lane: openRepoProject-2

# Traceability: delta scenarios to tests

One row per scenario of the three spec deltas of the ratified change
`openspec/changes/add-project-clean-all-safe/` (`specs/project-clean/spec.md`,
`specs/project-clean-review-safety/spec.md` and `specs/project-command/spec.md`
under it), in each file's order: the 100 scenarios on `main`, then PR #19's
scenario "The push child reaches its remote" as the 101st (`tasks.md` T002,
T074). The Delta column is the capability, the directory under `specs/`; the
Requirement column is the `### Requirement:` title the scenario sits under; the
Scenario column is the `#### Scenario:` title exactly. The Story column names
the user stories (`spec.md`, US1 to US9) whose test tasks in `tasks.md` list the
scenario, each one when two stories test it. The Tests column names the test
methods that cover the scenario.

| Delta | Requirement | Scenario | Story | Tests |
| --- | --- | --- | --- | --- |
| project-clean | Clean reports local worktree state | Audit a repository with a feature worktree | US6 | `test_clean_audit_a_repository_with_a_feature_worktree` |
| project-clean | Clean reports local worktree state | The plain report exits by completeness | US6 | `test_clean_the_plain_report_exits_by_completeness` |
| project-clean | Clean reports local worktree state | An unreadable worktree is one row | US6 | `test_clean_an_unreadable_worktree_is_one_row` |
| project-clean | Clean reports local worktree state | A failed status probe on the merge-target checkout | US6 | `test_clean_a_failed_status_probe_on_the_merge_target_checkout` |
| project-clean | Clean reports local worktree state | A failed status in the repository root | US6 | `test_clean_a_failed_status_in_the_repository_root` |
| project-clean | Clean reports local worktree state | Git older than 2.36 | US9 | `test_clean_git_older_than_2_36` |
| project-clean | Clean classifies preservation and cleanup actions | Dirty or unmerged work is preserved | US2 | `test_clean_dirty_or_unmerged_work_is_preserved` |
| project-clean | Clean classifies preservation and cleanup actions | A deleted upstream is remote-gone | US2 | `test_clean_a_deleted_upstream_is_remote_gone` |
| project-clean | Clean classifies preservation and cleanup actions | A merged worktree whose upstream was deleted | US2 | `test_clean_a_merged_worktree_whose_upstream_was_deleted` |
| project-clean | Clean classifies preservation and cleanup actions | Only tracked-file deletions | US5 | `test_clean_only_tracked_file_deletions` |
| project-clean | Clean can explicitly push safe feature branches | Push an unpushed feature branch | US3 | `test_clean_push_an_unpushed_feature_branch` |
| project-clean | Clean can explicitly push safe feature branches | Push refuses a branch whose upstream was deleted | US3 | `test_clean_push_refuses_a_branch_whose_upstream_was_deleted` |
| project-clean | Clean can explicitly push safe feature branches | Push refuses an incomplete inspection | US3, US6 | `test_clean_push_refuses_an_incomplete_inspection`, `test_clean_push_refuses_an_incomplete_inspection_deadline` |
| project-clean | Clean can explicitly push safe feature branches | Push and branch deletion stay human-only | US3 | `test_clean_push_and_branch_deletion_stay_human_only` |
| project-clean | Clean can explicitly retire verified worktrees | Remove a merged clean worktree | US3 | `test_clean_remove_a_merged_clean_worktree` |
| project-clean | Clean can explicitly retire verified worktrees | Every branch remains after a batch | US1 | `test_clean_every_branch_remains_after_a_batch` |
| project-clean | Clean can explicitly retire verified worktrees | A published branch with no commit of its own | US2 | `test_clean_a_published_branch_with_no_commit_of_its_own` |
| project-clean | Clean can explicitly retire verified worktrees | A fast-forward-merged branch at the target's tip stays eligible | US2 | `test_clean_a_fast_forward_merged_branch_at_the_target_s_tip_stays_eligible` |
| project-clean | Clean can explicitly retire verified worktrees | A branch reset to the merge target's tip stays unstarted | US2 | `test_clean_a_branch_reset_to_the_merge_target_s_tip_stays_unstarted` |
| project-clean | Clean can explicitly retire verified worktrees | A branch fetched at the merge target's tip stays unstarted | US2 | `test_clean_a_branch_fetched_at_the_merge_target_s_tip_stays_unstarted` |
| project-clean | Clean can explicitly retire verified worktrees | A branch whose reflog is missing, empty or expired | US2 | `test_clean_a_branch_whose_reflog_is_missing_empty_or_expired` |
| project-clean | Clean can explicitly retire verified worktrees | Git's own check runs on the pinned configuration | US4 | `test_clean_git_s_own_check_runs_on_the_pinned_configuration` |
| project-clean | Clean can explicitly retire verified worktrees | A named removal beside another row's inspection error | US3 | `test_clean_a_named_removal_beside_another_row_s_inspection_error` |
| project-clean | Clean can explicitly retire verified worktrees | A named removal among seventeen eligible rows | US3 | `test_clean_a_named_removal_among_seventeen_eligible_rows` |
| project-clean | Clean can explicitly retire verified worktrees | A named removal beyond the row cap | US3 | `test_clean_a_named_removal_beyond_the_row_cap` |
| project-clean | Clean can explicitly retire verified worktrees | Single target equals a one-item batch | US3 | `test_clean_single_target_equals_a_one_item_batch` |
| project-clean | Clean can explicitly retire verified worktrees | A removal past the hard ceiling | US5 | `test_clean_a_removal_past_the_hard_ceiling` |
| project-clean | Clean can explicitly retire verified worktrees | project killed during a deletion | US5 | `test_clean_project_killed_during_a_deletion` |
| project-clean | Clean hands off work requiring review | Pushed feature branch has an open review path | US2 | `test_clean_pushed_feature_branch_has_an_open_review_path` |
| project-clean | Clean hands off work requiring review | A noninteractive batch needs --yes | US1 | `test_clean_a_noninteractive_batch_needs_yes` |
| project-clean | Clean resolves its target Git-first | Absolute path that is not a repository root | US7 | `test_clean_absolute_path_that_is_not_a_repository_root` |
| project-clean | Clean resolves its target Git-first | Overview handoff keeps identity | US7 | `test_clean_overview_handoff_keeps_identity` |
| project-clean | Clean resolves its target Git-first | A bare repository reached from a linked worktree | US7 | `test_clean_a_bare_repository_reached_from_a_linked_worktree` |
| project-clean | Clean resolves its target Git-first | A separate git directory | US7 | `test_clean_a_separate_git_directory`, `test_clean_a_separate_git_directory_with_a_relative_core_worktree` |
| project-clean | Clean resolves its target Git-first | A submodule checkout | US7 | `test_clean_a_submodule_checkout` |
| project-clean | Clean resolves its target Git-first | Merge target missing, invalid, or conflicting | US7 | `test_clean_merge_target_missing_invalid_or_conflicting`, `test_clean_merge_target_missing_invalid_or_conflicting_unreadable_manifest` |
| project-clean | Clean resolves its target Git-first | A tracking branch spelled with its remote | US7 | `test_clean_a_tracking_branch_spelled_with_its_remote` |
| project-clean | Clean resolves its target Git-first | A manifest over 1 MiB | US7 | `test_clean_a_manifest_over_1_mib` |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Stable order and preserved work | US1 | `test_clean_stable_order_and_preserved_work`, `test_clean_stable_order_and_preserved_work_target_not_checked_out` |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Every protected classifier | US2 | `test_clean_every_protected_classifier`, `test_clean_every_protected_classifier_incomplete_copy` |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Hidden local state | US2, US4 | `test_clean_hidden_local_state`, `test_clean_hidden_local_state_after_confirmation` |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Submodules | US2, US4 | `test_clean_submodules`, `test_clean_submodules_after_confirmation` |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Paths and empty plans | US1 | `test_clean_paths_and_empty_plans`, `test_clean_paths_and_empty_plans_paths_with_spaces_are_removed` |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Preview is advisory | US1 | `test_clean_preview_is_advisory` |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Plan digest mismatch | US1 | `test_clean_plan_digest_mismatch`, `test_clean_plan_digest_mismatch_unchanged_digest_applies` |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Invalid argument combinations | US1 | `test_clean_invalid_argument_combinations`, `test_clean_invalid_argument_combinations_unrefused_flags` |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Only yes confirms | US1 | `test_clean_only_yes_confirms` |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | The preview says what keeps each row | US1 | `test_clean_the_preview_says_what_keeps_each_row`, `test_clean_the_preview_says_what_keeps_each_row_single_mode`, `test_clean_the_preview_says_what_keeps_each_row_single_mode_shared_path` |
| project-clean | Clean bounds its Git work and reports omitted work | Row cap and planning failures | US6 | `test_clean_row_cap_and_planning_failures`, `test_clean_row_cap_and_planning_failures_an_unreadable_realpath_in_single_mode` |
| project-clean | Clean bounds its Git work and reports omitted work | Twenty rows pass every gate before deferred-target-cap | US6 | `test_clean_twenty_rows_pass_every_gate_before_deferred_target_cap` |
| project-clean | Clean bounds its Git work and reports omitted work | Ignored-file bound | US6 | `test_clean_ignored_file_bound` |
| project-clean | Clean bounds its Git work and reports omitted work | Bounded revalidation work | US6 | `test_clean_bounded_revalidation_work` |
| project-clean | Clean bounds its Git work and reports omitted work | Deadline expiry mid-batch | US6 | `test_clean_deadline_expiry_mid_batch`, `test_clean_deadline_expiry_mid_batch_a_rescan_read_cut_at_the_deadline`, `test_clean_deadline_expiry_mid_batch_a_revalidation_read_cut_at_the_deadline`, `test_clean_deadline_expiry_mid_batch_a_revalidation_read_cut_at_its_probe_budget` |
| project-clean | Clean records a reconcilable result for every removal target | Exit 0 without evidence | US5 | `test_clean_exit_0_without_evidence` |
| project-clean | Clean records a reconcilable result for every removal target | A signal during a removal | US5 | `test_clean_a_signal_during_a_removal`, `test_clean_a_signal_during_a_removal_sigint_during_a_revalidation` |
| project-clean | Clean records a reconcilable result for every removal target | SIGTERM before the apply phase | US5 | `test_clean_sigterm_before_the_apply_phase`, `test_clean_sigterm_before_the_apply_phase_after_the_last_probe`, `test_clean_sigterm_before_the_apply_phase_while_the_plan_is_written` |
| project-clean | Clean records a reconcilable result for every removal target | Git leaves an orphaned directory | US5 | `test_clean_git_leaves_an_orphaned_directory` |
| project-clean | Clean records a reconcilable result for every removal target | Git refuses the removal | US5 | `test_clean_git_refuses_the_removal` |
| project-clean | Clean records a reconcilable result for every removal target | Unreadable path after removal | US5 | `test_clean_unreadable_path_after_removal` |
| project-clean | Clean records a reconcilable result for every removal target | Exception after the apply phase begins | US5 | `test_clean_exception_after_the_apply_phase_begins` |
| project-clean | Clean records a reconcilable result for every removal target | The stop block | US5 | `test_clean_the_stop_block` |
| project-clean | Clean reports every path exactly or excludes it | Control-character and non-UTF-8 paths | US8 | `test_clean_control_character_and_non_utf_8_paths` |
| project-clean | Clean reports every path exactly or excludes it | Non-UTF-8 repository root | US8 | `test_clean_non_utf_8_repository_root`, `test_clean_non_utf_8_repository_root_common_directory` |
| project-clean | Clean plans and refusals are versioned JSON | Apply with JSON prints one document | US8 | `test_clean_apply_with_json_prints_one_document` |
| project-clean | Clean plans and refusals are versioned JSON | The plain report in JSON | US8 | `test_clean_the_plain_report_in_json` |
| project-clean-review-safety | Cleanup preserves all local work not proven disposable | A merged worktree has ignored local files | US2 | `test_clean_a_merged_worktree_has_ignored_local_files` |
| project-clean-review-safety | Cleanup preserves all local work not proven disposable | Default branch cannot be established locally | US2 | `test_clean_default_branch_cannot_be_established_locally` |
| project-clean-review-safety | Cleanup preserves all local work not proven disposable | An edit hidden by assume-unchanged survives | US2 | `test_clean_an_edit_hidden_by_assume_unchanged_survives` |
| project-clean-review-safety | Cleanup preserves all local work not proven disposable | A worktree holding a submodule is never offered | US2 | `test_clean_a_worktree_holding_a_submodule_is_never_offered` |
| project-clean-review-safety | Cleanup preserves all local work not proven disposable | The main worktree and a locked worktree | US2 | `test_clean_the_main_worktree_and_a_locked_worktree` |
| project-clean-review-safety | Cleanup revalidates destructive actions | Worktree changes while confirmation is pending | US4 | `test_clean_worktree_changes_while_confirmation_is_pending` |
| project-clean-review-safety | Cleanup revalidates destructive actions | Target directory replaced | US4 | `test_clean_target_directory_replaced` |
| project-clean-review-safety | Cleanup revalidates destructive actions | Admin registration changed | US4 | `test_clean_admin_registration_changed`, `test_clean_admin_registration_changed_a_twin_made_after_planning`, `test_clean_admin_registration_changed_a_twin_spelled_through_an_unsearchable_directory` |
| project-clean-review-safety | Cleanup revalidates destructive actions | Parent directory swapped | US4 | `test_clean_parent_directory_swapped` |
| project-clean-review-safety | Cleanup revalidates destructive actions | New worktree and pre-removal changes | US4 | `test_clean_new_worktree_and_pre_removal_changes` |
| project-clean-review-safety | Cleanup revalidates destructive actions | State changes before revalidation | US4 | `test_clean_state_changes_before_revalidation` |
| project-clean-review-safety | Cleanup revalidates destructive actions | Changed later target | US4 | `test_clean_changed_later_target` |
| project-clean-review-safety | Cleanup revalidates destructive actions | Untracked file under status.showUntrackedFiles=no | US4 | `test_clean_untracked_file_under_status_showuntrackedfiles_no` |
| project-clean-review-safety | Cleanup revalidates destructive actions | Branch advances before removal | US4 | `test_clean_branch_advances_before_removal` |
| project-clean-review-safety | Cleanup revalidates destructive actions | Deleted upstream reappears before revalidation | US4 | `test_clean_deleted_upstream_reappears_before_revalidation` |
| project-clean-review-safety | Cleanup states a narrow guarantee and its residual window | Ignored file in the residual window | US4 | `test_clean_ignored_file_in_the_residual_window` |
| project-clean-review-safety | Cleanup states a narrow guarantee and its residual window | Branch advances after removal | US4 | `test_clean_branch_advances_after_removal` |
| project-clean-review-safety | Cleanup states a narrow guarantee and its residual window | Repository replaced mid-batch | US4 | `test_clean_repository_replaced_mid_batch` |
| project-command | Inspect and diagnose | Missing leg | US9 | `test_doctor_missing_leg` |
| project-command | Inspect and diagnose | Git older than 2.36 in status and doctor | US9 | `test_status_git_older_than_2_36_in_status_and_doctor` |
| project-command | Inspect and diagnose | No git on PATH | US9 | `test_doctor_no_git_on_path` |
| project-command | Inspect and diagnose | Not established is an error, none is not | US9 | `test_doctor_not_established_is_an_error_none_is_not` |
| project-command | Inspect and diagnose | A failed root status is reported | US9 | `test_status_a_failed_root_status_is_reported` |
| project-command | Inspect and diagnose | A deleted upstream in status and doctor | US9 | `test_status_a_deleted_upstream_in_status_and_doctor` |
| project-command | Explicit maintenance | Default report | US9 | `test_update_default_report` |
| project-command | Explicit maintenance | A leg's probe times out | US9 | `test_update_a_leg_s_probe_times_out` |
| project-command | Explicit maintenance | Tools and workflow need no Git | US9 | `test_update_tools_and_workflow_need_no_git` |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | A git that floods standard error | US9 | `test_status_a_git_that_floods_standard_error` |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | A git that ignores SIGTERM | US9 | `test_status_a_git_that_ignores_sigterm` |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | Five thousand ignored records | US9 | `test_status_five_thousand_ignored_records` |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | User status configuration | US9 | `test_status_user_status_configuration` |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | A caller's Git environment is ignored | US9 | `test_status_a_caller_s_git_environment_is_ignored` |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | The sixteenth scrubbed name on Git 2.36 | US9 | `test_status_the_sixteenth_scrubbed_name_on_git_2_36` |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | The pinned status configuration | US9 | `test_status_the_pinned_status_configuration` |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | A lazy fetch in a partial clone is refused locally | US9 | `test_status_a_lazy_fetch_in_a_partial_clone_is_refused_locally` |
| project-command (PR #19 draft) | Repository inspection requires Git 2.36 and shares one evidence model | The push child reaches its remote | US3 | `test_clean_the_push_child_reaches_its_remote`, `test_clean_the_push_child_reaches_its_remote_at_a_terminal` |

T126's writer fills the Tests cells from the merged tests (lead ruling R-32b).

The last row is PR #19's draft scenario, from branch
`change/amend-clean-all-safe-push-pins` (`specs/project-command/spec.md`), not
yet on `main`; its Delta cell carries the mark "(PR #19 draft)". T126 reads its
title from `main`'s delta once PR #19 has landed, otherwise from that branch.
