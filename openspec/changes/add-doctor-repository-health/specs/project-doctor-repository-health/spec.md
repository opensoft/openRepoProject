## Purpose

Provide a read-only, actionable repository-health view in doctor so operators
can assess local branch and linked-worktree state before choosing a Git action.

## ADDED Requirements

### Requirement: Doctor reports cleanup-aware repository health

`project doctor` SHALL report the local default branch and every linked
worktree's cleanup classification, relevant local Git facts, and recommended
next step. The human report SHALL distinguish a healthy protected default from
default-branch drift, and SHALL label all tracking observations as local-ref
information with no fetch performed.

#### Scenario: Default branch is locally diverged

- **WHEN** the default branch is both ahead of and behind its configured upstream
- **THEN** doctor reports a warning for the default worktree that identifies
  divergent local and remote history and recommends normal reconciliation

#### Scenario: A linked worktree is blocked by ignored local files

- **WHEN** a linked worktree contains ignored local files
- **THEN** doctor reports its ignored-local-files classification and recommends
  preserving or relocating those files before cleanup

### Requirement: Doctor exposes machine-readable repository health

`project doctor --json` SHALL include a `repository_health` object containing
the local merge target, tracking-freshness statement, and the worktree health
rows used by the human report. Each row SHALL preserve the cleanup
classification and include a doctor health level and status.

#### Scenario: Automation reads a linked worktree warning

- **WHEN** doctor is requested with JSON output for a repository that has an
  unpublished linked worktree
- **THEN** `repository_health` includes that worktree with its unpublished
  cleanup classification and warning health level

### Requirement: Repository-health inspection is non-destructive and resilient

Repository-health inspection MUST NOT fetch, push, merge, reset, remove a
worktree, delete a branch, or read credential values. If doctor cannot
determine a local default branch, it SHALL report repository health as
unavailable with the reason and continue its remaining diagnostics.

#### Scenario: No default branch can be determined

- **WHEN** doctor inspects a repository whose local branches do not identify a
  default branch
- **THEN** doctor completes and returns a repository-health unavailable warning
  instead of failing the entire report
