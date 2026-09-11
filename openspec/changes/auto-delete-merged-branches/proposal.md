## Why

Removing a safe linked worktree currently leaves its already-merged local
branch behind, so a cleanup run does not fully retire work the command has
proved unnecessary. Confirmed cleanup should remove that branch as part of the
same local retirement operation.

## What Changes

- Make the confirmed removal of a clean, merged, non-current worktree retire
  its paired local branch after the worktree is removed.
- Show the planned worktree and branch operations before confirmation and keep
  their safety evidence tied to the same cleanup report.
- Preserve the read-only default, the explicit single-branch deletion action
  for orphaned branches, and every existing refusal for dirty, ignored,
  detached, unmerged, current, or default-branch work.
- Delete only the verified local branch with normal Git deletion; never delete
  a remote branch or force deletion.

## Capabilities

### New Capabilities

- `project-clean-branch-retirement`: Confirmed worktree cleanup retires its
  proven-unneeded paired local branch.

### Modified Capabilities

None. The existing cleanup change has not been archived into baseline specs;
this change records the additional branch-retirement contract separately.

## Impact

The `project` cleanup executor, human cleanup plan, disposable Git worktree
tests, README usage guidance, and workBench-distributed executable pin are
affected. No default command, remote branch, or branch containing unproven work
is changed.
