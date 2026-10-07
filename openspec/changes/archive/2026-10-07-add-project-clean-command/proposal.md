## Why

`project status` and `project doctor` can explain repository drift, but they do
not help a person finish or retire the linked worktrees that caused it. A
project can therefore remain cluttered with pushed, unpushed, merged, dirty,
or detached branches even after its feature work is complete. We need an
explicit cleanup workflow that carries safe work to its remote branch and
retires only worktrees that are demonstrably safe to remove.

## What Changes

- Add `project clean` to inspect linked worktrees and their branches and print
  a deterministic cleanup plan.
- Classify each worktree as dirty, unpushed, unpublished, remote-gone,
  merged, removable, or requiring human review.
- Add explicit apply actions for safe branch pushes and clean worktree/local
  branch removal, with confirmation before each write.
- Preserve dirty work, detached work, feature branches without a remote, and
  branches whose merge state cannot be established; never force-push, reset,
  stash, or delete a branch containing unmerged work.
- Report the normal next step for work that needs a pull request or human
  merge instead of silently merging or bypassing repository policy.
- Extend JSON and human reports and add disposable Git/worktree tests for all
  cleanup classifications and refusal paths.

## Capabilities

### New Capabilities

- `project-clean`: Explicit, safety-first cleanup of local worktrees and their
  branches.

### Modified Capabilities

None. The new command is specified as a standalone capability; the existing
CLI surface will be extended as an implementation consequence.

## Impact

The `project` executable, its CLI parser, local Git inspection helpers, README,
and tests are affected. The command will operate on local Git state by default
and will not require a network fetch. Distribution through workBenches will
need the updated executable pin after this change lands. Existing repositories
and remote branches are unchanged unless the user explicitly applies a
particular cleanup action.
