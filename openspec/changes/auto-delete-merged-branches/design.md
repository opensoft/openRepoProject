## Context

See proposal.md. Today the `remove` cleanup action verifies a linked worktree
is safe and removes it, while `delete-branch` requires a separate confirmed
invocation. That leaves completed local branches behind after ordinary
worktree cleanup.

## Goals / Non-Goals

**Goals:**

- Retire the paired local branch as part of one confirmed safe-worktree plan.
- Keep every existing preservation rule and reuse Git's non-force merged-branch
  deletion check as a final guard.
- Make partial completion explicit if the branch step fails after removal.

**Non-Goals:**

- Make the read-only `project clean` audit destructive.
- Delete remote branches, fetch, merge, force-delete, reset, stash, or resolve
  divergent work.
- Batch unrelated worktrees or change the explicit `delete-branch` action for
  already-orphaned local branches.

## Decisions

1. **Extend the existing explicit remove action.** A caller already names the
   worktree and confirms its removal, so its merged branch is the unambiguous
   paired branch. Adding a new broad default or batch action would expand the
   destructive surface beyond this request.

2. **Remove the worktree before its branch.** Git will not delete a branch
   checked out by a linked worktree. The command revalidates the displayed
   clean/merged/non-current evidence, removes the worktree, then runs `git
   branch -d` without force. If the latter fails, the remaining branch is the
   safe recovery point and the command reports the failure.

3. **Show both commands before the one confirmation.** The plan names the
   worktree removal and subsequent local branch deletion. The existing
   revalidation remains before either write; no remote refs are changed.

## Risks / Trade-offs

- [Branch deletion fails after worktree removal] → Return the failure and
  preserve the local branch; it can recreate a worktree.
- [Local ancestry is stale relative to a remote] → Continue to use local refs
  only, label the plan accordingly, and never delete a remote branch.
- [A user expects the audit to delete branches] → Keep audit mode read-only and
  require the existing `--apply --action remove --worktree` confirmation.

## Migration Plan

Add disposable worktree tests for successful paired retirement and a simulated
branch-deletion failure, update the README, and run the full test suite plus
strict OpenSpec validation. Rollback is a normal code revert; a successfully
deleted local branch can be restored from its remote branch or merge history.
