## Purpose

Ensure cleanup only changes a Git worktree or branch after local state proves
the action safe, while preserving ignored and remotely divergent work.

## ADDED Requirements

### Requirement: Cleanup preserves all local work not proven disposable

Cleanup SHALL treat ignored local files, dirty work, detached state, an unknown
default branch, and remote divergence as preservation or review states. It MUST
not offer destructive removal for those states.

#### Scenario: A merged worktree has ignored local files

- **WHEN** a non-current merged worktree contains ignored files
- **THEN** cleanup reports a preservation state and refuses its removal

#### Scenario: Default branch cannot be established locally

- **WHEN** neither the manifest, remote HEAD, nor a conventional local default
  branch identifies a merge target
- **THEN** cleanup refuses instead of guessing from the current branch

### Requirement: Cleanup respects configured upstream mappings

An explicit cleanup push SHALL use the branch's configured remote and remote
branch name, even when that remote branch differs from the local branch name.
It SHALL refuse a branch whose local and remote state has diverged.

#### Scenario: Local and upstream branch names differ

- **WHEN** a clean local branch tracks a differently named upstream branch
- **THEN** cleanup plans and performs a normal non-force push to that upstream

### Requirement: Cleanup revalidates destructive actions

Cleanup SHALL re-inspect the selected target after confirmation and before a
push, worktree removal, or local branch deletion. It MUST refuse when the
state no longer matches the reviewed plan.

#### Scenario: Worktree changes while confirmation is pending

- **WHEN** a selected worktree becomes dirty after the plan is shown
- **THEN** cleanup refuses removal and preserves the worktree
