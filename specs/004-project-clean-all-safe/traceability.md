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
| project-clean | Clean reports local worktree state | Audit a repository with a feature worktree | US6 |  |
| project-clean | Clean reports local worktree state | The plain report exits by completeness | US6 |  |
| project-clean | Clean reports local worktree state | An unreadable worktree is one row | US6 |  |
| project-clean | Clean reports local worktree state | A failed status probe on the merge-target checkout | US6 |  |
| project-clean | Clean reports local worktree state | A failed status in the repository root | US6 |  |
| project-clean | Clean reports local worktree state | Git older than 2.36 | US9 |  |
| project-clean | Clean classifies preservation and cleanup actions | Dirty or unmerged work is preserved | US2 |  |
| project-clean | Clean classifies preservation and cleanup actions | A deleted upstream is remote-gone | US2 |  |
| project-clean | Clean classifies preservation and cleanup actions | A merged worktree whose upstream was deleted | US2 |  |
| project-clean | Clean classifies preservation and cleanup actions | Only tracked-file deletions | US5 |  |
| project-clean | Clean can explicitly push safe feature branches | Push an unpushed feature branch | US3 |  |
| project-clean | Clean can explicitly push safe feature branches | Push refuses a branch whose upstream was deleted | US3 |  |
| project-clean | Clean can explicitly push safe feature branches | Push refuses an incomplete inspection | US3, US6 |  |
| project-clean | Clean can explicitly push safe feature branches | Push and branch deletion stay human-only | US3 |  |
| project-clean | Clean can explicitly retire verified worktrees | Remove a merged clean worktree | US3 |  |
| project-clean | Clean can explicitly retire verified worktrees | Every branch remains after a batch | US1 |  |
| project-clean | Clean can explicitly retire verified worktrees | A published branch with no commit of its own | US2 |  |
| project-clean | Clean can explicitly retire verified worktrees | A fast-forward-merged branch at the target's tip stays eligible | US2 |  |
| project-clean | Clean can explicitly retire verified worktrees | A branch reset to the merge target's tip stays unstarted | US2 |  |
| project-clean | Clean can explicitly retire verified worktrees | A branch fetched at the merge target's tip stays unstarted | US2 |  |
| project-clean | Clean can explicitly retire verified worktrees | A branch whose reflog is missing, empty or expired | US2 |  |
| project-clean | Clean can explicitly retire verified worktrees | Git's own check runs on the pinned configuration | US4 |  |
| project-clean | Clean can explicitly retire verified worktrees | A named removal beside another row's inspection error | US3 |  |
| project-clean | Clean can explicitly retire verified worktrees | A named removal among seventeen eligible rows | US3 |  |
| project-clean | Clean can explicitly retire verified worktrees | A named removal beyond the row cap | US3 |  |
| project-clean | Clean can explicitly retire verified worktrees | Single target equals a one-item batch | US3 |  |
| project-clean | Clean can explicitly retire verified worktrees | A removal past the hard ceiling | US5 |  |
| project-clean | Clean can explicitly retire verified worktrees | project killed during a deletion | US5 |  |
| project-clean | Clean hands off work requiring review | Pushed feature branch has an open review path | US2 |  |
| project-clean | Clean hands off work requiring review | A noninteractive batch needs --yes | US1 |  |
| project-clean | Clean resolves its target Git-first | Absolute path that is not a repository root | US7 |  |
| project-clean | Clean resolves its target Git-first | Overview handoff keeps identity | US7 |  |
| project-clean | Clean resolves its target Git-first | A bare repository reached from a linked worktree | US7 |  |
| project-clean | Clean resolves its target Git-first | A separate git directory | US7 |  |
| project-clean | Clean resolves its target Git-first | A submodule checkout | US7 |  |
| project-clean | Clean resolves its target Git-first | Merge target missing, invalid, or conflicting | US7 |  |
| project-clean | Clean resolves its target Git-first | A tracking branch spelled with its remote | US7 |  |
| project-clean | Clean resolves its target Git-first | A manifest over 1 MiB | US7 |  |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Stable order and preserved work | US1 |  |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Every protected classifier | US2 |  |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Hidden local state | US2, US4 |  |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Submodules | US2, US4 |  |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Paths and empty plans | US1 |  |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Preview is advisory | US1 |  |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Plan digest mismatch | US1 |  |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Invalid argument combinations | US1 |  |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | Only yes confirms | US1 |  |
| project-clean | Clean previews and applies a batch of eligible worktree removals in one repository | The preview says what keeps each row | US1 |  |
| project-clean | Clean bounds its Git work and reports omitted work | Row cap and planning failures | US6 |  |
| project-clean | Clean bounds its Git work and reports omitted work | Twenty rows pass every gate before deferred-target-cap | US6 |  |
| project-clean | Clean bounds its Git work and reports omitted work | Ignored-file bound | US6 |  |
| project-clean | Clean bounds its Git work and reports omitted work | Bounded revalidation work | US6 |  |
| project-clean | Clean bounds its Git work and reports omitted work | Deadline expiry mid-batch | US6 |  |
| project-clean | Clean records a reconcilable result for every removal target | Exit 0 without evidence | US5 |  |
| project-clean | Clean records a reconcilable result for every removal target | A signal during a removal | US5 |  |
| project-clean | Clean records a reconcilable result for every removal target | SIGTERM before the apply phase | US5 |  |
| project-clean | Clean records a reconcilable result for every removal target | Git leaves an orphaned directory | US5 |  |
| project-clean | Clean records a reconcilable result for every removal target | Git refuses the removal | US5 |  |
| project-clean | Clean records a reconcilable result for every removal target | Unreadable path after removal | US5 |  |
| project-clean | Clean records a reconcilable result for every removal target | Exception after the apply phase begins | US5 |  |
| project-clean | Clean records a reconcilable result for every removal target | The stop block | US5 |  |
| project-clean | Clean reports every path exactly or excludes it | Control-character and non-UTF-8 paths | US8 |  |
| project-clean | Clean reports every path exactly or excludes it | Non-UTF-8 repository root | US8 |  |
| project-clean | Clean plans and refusals are versioned JSON | Apply with JSON prints one document | US8 |  |
| project-clean | Clean plans and refusals are versioned JSON | The plain report in JSON | US8 |  |
| project-clean-review-safety | Cleanup preserves all local work not proven disposable | A merged worktree has ignored local files | US2 |  |
| project-clean-review-safety | Cleanup preserves all local work not proven disposable | Default branch cannot be established locally | US2 |  |
| project-clean-review-safety | Cleanup preserves all local work not proven disposable | An edit hidden by assume-unchanged survives | US2 |  |
| project-clean-review-safety | Cleanup preserves all local work not proven disposable | A worktree holding a submodule is never offered | US2 |  |
| project-clean-review-safety | Cleanup preserves all local work not proven disposable | The main worktree and a locked worktree | US2 |  |
| project-clean-review-safety | Cleanup revalidates destructive actions | Worktree changes while confirmation is pending | US4 |  |
| project-clean-review-safety | Cleanup revalidates destructive actions | Target directory replaced | US4 |  |
| project-clean-review-safety | Cleanup revalidates destructive actions | Admin registration changed | US4 |  |
| project-clean-review-safety | Cleanup revalidates destructive actions | Parent directory swapped | US4 |  |
| project-clean-review-safety | Cleanup revalidates destructive actions | New worktree and pre-removal changes | US4 |  |
| project-clean-review-safety | Cleanup revalidates destructive actions | State changes before revalidation | US4 |  |
| project-clean-review-safety | Cleanup revalidates destructive actions | Changed later target | US4 |  |
| project-clean-review-safety | Cleanup revalidates destructive actions | Untracked file under status.showUntrackedFiles=no | US4 |  |
| project-clean-review-safety | Cleanup revalidates destructive actions | Branch advances before removal | US4 |  |
| project-clean-review-safety | Cleanup revalidates destructive actions | Deleted upstream reappears before revalidation | US4 |  |
| project-clean-review-safety | Cleanup states a narrow guarantee and its residual window | Ignored file in the residual window | US4 |  |
| project-clean-review-safety | Cleanup states a narrow guarantee and its residual window | Branch advances after removal | US4 |  |
| project-clean-review-safety | Cleanup states a narrow guarantee and its residual window | Repository replaced mid-batch | US4 |  |
| project-command | Inspect and diagnose | Missing leg | US9 |  |
| project-command | Inspect and diagnose | Git older than 2.36 in status and doctor | US9 |  |
| project-command | Inspect and diagnose | No git on PATH | US9 |  |
| project-command | Inspect and diagnose | Not established is an error, none is not | US9 |  |
| project-command | Inspect and diagnose | A failed root status is reported | US9 |  |
| project-command | Inspect and diagnose | A deleted upstream in status and doctor | US9 |  |
| project-command | Explicit maintenance | Default report | US9 |  |
| project-command | Explicit maintenance | A leg's probe times out | US9 |  |
| project-command | Explicit maintenance | Tools and workflow need no Git | US9 |  |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | A git that floods standard error | US9 |  |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | A git that ignores SIGTERM | US9 |  |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | Five thousand ignored records | US9 |  |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | User status configuration | US9 |  |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | A caller's Git environment is ignored | US9 |  |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | The sixteenth scrubbed name on Git 2.36 | US9 |  |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | The pinned status configuration | US9 |  |
| project-command | Repository inspection requires Git 2.36 and shares one evidence model | A lazy fetch in a partial clone is refused locally | US9 |  |
| project-command (PR #19 draft) | Repository inspection requires Git 2.36 and shares one evidence model | The push child reaches its remote | US3 |  |

T126's writer fills the Tests cells from the merged tests (lead ruling R-32b).

The last row is PR #19's draft scenario, from branch
`change/amend-clean-all-safe-push-pins` (`specs/project-command/spec.md`), not
yet on `main`; its Delta cell carries the mark "(PR #19 draft)". T126 reads its
title from `main`'s delta once PR #19 has landed, otherwise from that branch.
