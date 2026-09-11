## Purpose

Retire the local branch paired with a safely removable linked worktree so
confirmed cleanup leaves no unnecessary local branch behind.

## ADDED Requirements

### Requirement: Safe worktree removal retires its paired local branch

When confirmed cleanup removes a clean, merged, non-current linked worktree,
it SHALL then delete that worktree's local branch using normal verified Git
branch deletion. The plan SHALL show both operations before confirmation.

#### Scenario: Merged feature worktree is removed

- **WHEN** a linked feature worktree is clean, non-current, and its branch is
  locally proven merged into the cleanup target
- **THEN** confirmed removal removes the worktree and its local feature branch

### Requirement: Branch retirement preserves unproven work

Cleanup MUST NOT retire a remote branch or force-delete a local branch. It
MUST preserve the branch when the worktree is dirty, ignored, detached,
current, default, unmerged, or cannot be verified as merged.

#### Scenario: Feature worktree is not proven removable

- **WHEN** cleanup classifies a feature worktree as anything other than a
  clean merged removable worktree
- **THEN** worktree removal and paired branch retirement refuse

### Requirement: Branch deletion failure is reported without force

If normal local branch deletion fails after a worktree is removed, cleanup
SHALL return that failure and leave the remaining branch untouched. It MUST NOT
retry with a force-delete option.

#### Scenario: Branch deletion is refused by Git

- **WHEN** the planned local branch deletion exits nonzero
- **THEN** cleanup reports failure without running a force-delete command
