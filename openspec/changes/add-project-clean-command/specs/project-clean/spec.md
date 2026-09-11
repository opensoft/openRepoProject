## Purpose

Provide a safe, explicit way to finish local Git worktree housekeeping without
losing uncommitted work, bypassing repository review policy, or deleting a
branch before its commits are preserved.

## ADDED Requirements

### Requirement: Clean reports local worktree state

`project clean` SHALL inspect the target repository and every linked worktree
using local Git state only. It SHALL report each worktree's path, branch or
detached state, cleanliness, upstream, ahead/behind counts as of the last
fetch, and whether its commits are merged into the target's tracking branch.
Human and JSON reports SHALL describe that remote information may be stale.

#### Scenario: Audit a repository with a feature worktree

- **WHEN** `project clean` is run without an apply action
- **THEN** it prints a cleanup plan for the main checkout and each linked
  worktree without fetching, committing, pushing, resetting, stashing, or
  removing anything

### Requirement: Clean classifies preservation and cleanup actions

The command SHALL classify work as dirty, detached, unpublished, unpushed,
pushed-but-unmerged, merged-and-removable, or protected default-branch work.
Dirty, detached, unpublished, and unmerged work SHALL be preserved and SHALL
include an actionable human handoff rather than being treated as removable.

#### Scenario: Dirty or unmerged work is preserved

- **WHEN** a worktree contains uncommitted changes or a branch is not merged
  into the target branch
- **THEN** the report identifies it as requiring preservation or review and
  proposes no destructive action for it

### Requirement: Clean can explicitly push safe feature branches

An apply operation SHALL be able to push a named non-default branch to its
configured upstream, or establish its explicitly named upstream when none
exists. It MUST use a normal non-force push, require confirmation unless
explicit confirmation was supplied, and preserve the delegated exit status and
output. It SHALL refuse to push a default branch or a branch with unresolved
local work.

#### Scenario: Push an unpushed feature branch

- **WHEN** the user requests an apply push for a clean feature branch with
  commits not present on its remote branch
- **THEN** the command shows the exact push plan, confirms it, and pushes
  without force; a failed push leaves the repository unchanged by the command

### Requirement: Clean can explicitly retire verified worktrees

An apply operation SHALL be able to remove one named linked worktree only when
it is clean, not the current worktree, and its branch is verified as merged
into the target branch. It SHALL remove a local branch only as a separate,
explicit action after the worktree is gone and the branch is verified merged.
It MUST never use a force removal, reset, or deletion of unmerged work.

#### Scenario: Remove a merged clean worktree

- **WHEN** the user requests removal of a clean linked worktree whose branch
  is an ancestor of the target branch
- **THEN** the command confirms and removes that worktree, while refusing to
  remove its branch unless the user separately requests branch deletion

### Requirement: Clean hands off work requiring review

For a clean branch that is pushed but not merged, the command SHALL report that
the branch must go through the repository's normal pull-request or merge
process. It SHALL not create, approve, merge, close, or delete a pull request
implicitly. Noninteractive execution SHALL refuse apply actions unless the
user supplied explicit confirmation and action targets.

#### Scenario: Pushed feature branch has an open review path

- **WHEN** a clean feature branch has an upstream branch but is not merged
- **THEN** the report says to continue through the normal pull-request or
  merge process and leaves the worktree and branch intact
