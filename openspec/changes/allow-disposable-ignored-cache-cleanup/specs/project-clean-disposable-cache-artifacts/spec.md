## Purpose

Allow confirmed cleanup to discard a narrow, reproducible class of ignored
Python bytecode artifacts without weakening preservation of unknown local work.

## ADDED Requirements

### Requirement: Cleanup distinguishes disposable and blocking ignored artifacts

The read-only cleanup report SHALL list the ignored artifacts classified as
disposable and those that remain blocking. The initial disposable allowlist
SHALL contain only non-symlink `__pycache__` directories and non-symlink
regular `.pyc` or `.pyo` files that are contained by the inspected worktree.
Every other ignored artifact MUST remain blocking.

#### Scenario: Python bytecode caches are the only ignored artifacts

- **WHEN** an otherwise clean linked worktree contains only ignored
  `__pycache__` directories or `.pyc`/`.pyo` files
- **THEN** the cleanup report identifies them as disposable rather than
  classifying the worktree as blocked by ignored local files

#### Scenario: An unknown ignored artifact is present

- **WHEN** a linked worktree contains an ignored artifact outside the
  disposable allowlist
- **THEN** cleanup reports that artifact as blocking and refuses worktree
  removal until it is preserved or relocated

### Requirement: Confirmed worktree cleanup may discard listed cache artifacts

When confirmed cleanup removes a named, non-current, locally merged worktree
whose only ignored artifacts are listed as disposable, it SHALL show every
cache artifact that will be discarded and remove those artifacts before
removing the worktree and retiring its paired local branch. The existing
confirmation for the selected remove action SHALL be sufficient; audit mode
MUST remain read-only.

#### Scenario: Retire a merged worktree with Python caches

- **WHEN** a user confirms removal of a merged worktree that contains only
  disposable Python bytecode artifacts
- **THEN** cleanup deletes the listed cache artifacts, removes the worktree,
  and retires the locally merged branch without an additional prompt

### Requirement: Disposable artifact cleanup preserves safety boundaries

Before deletion, cleanup MUST revalidate the selected worktree and exact
artifact classification. It MUST NOT follow or delete a symlink, delete a path
outside the selected worktree, use a broad ignored-file deletion command, or
continue to worktree/branch retirement when cache deletion fails. Commands
needed after worktree removal MUST run from a surviving linked worktree.

#### Scenario: Cache state changes after confirmation

- **WHEN** a disposable cache path changes into an unknown or unsafe ignored
  artifact after the removal plan is displayed
- **THEN** cleanup refuses before deleting any artifact, worktree, or branch

#### Scenario: Cleanup is invoked from the worktree being retired

- **WHEN** the requested cleanup target is itself the merged linked worktree
- **THEN** cleanup can complete its branch retirement from the surviving target
  branch worktree
