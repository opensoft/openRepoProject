## Why

Python creates ignored bytecode caches whenever the CLI or its tests run. Those
known generated artifacts currently block an otherwise safe linked-worktree
retirement and force an operator to clean up harmless files by hand.

## What Changes

- Classify ignored artifacts into a fixed disposable Python-cache allowlist and
  unknown blocking files in the read-only cleanup report.
- Let confirmed removal of a named, clean, non-current, locally merged
  worktree remove only its listed disposable Python caches before retiring the
  worktree and paired local branch.
- Show each planned disposable-cache deletion in the confirmation plan and
  revalidate the exact classified paths before performing it.
- Preserve the existing refusal for every ignored artifact outside the
  allowlist, including symlinks and paths that are not safely contained in the
  selected worktree.

## Capabilities

### New Capabilities

- `project-clean-disposable-cache-artifacts`: Confirmed cleanup can discard a
  small, explicit class of reproducible ignored Python bytecode artifacts.

### Modified Capabilities

None. The active cleanup change records are not archived baseline
specifications; this change defines the additional disposable-artifact
contract separately.

## Impact

The `project` cleanup inspection/executor, human and JSON reports, disposable
Git worktree tests, and README guidance change. The default audit remains
read-only. No arbitrary ignored file, remote branch, fetch, force-delete,
reset, or unconfirmed cleanup action is introduced.
