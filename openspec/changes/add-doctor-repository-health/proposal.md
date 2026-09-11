## Why

`project doctor` reports general checkout and tooling facts, but it does not
explain whether linked worktrees are safe to preserve, need reconciliation, or
are candidates for the explicit `project clean` workflow. Operators therefore
have to correlate the doctor and clean reports by hand when assessing a
repository's health.

## What Changes

- Add a read-only repository-health section to `project doctor` that reports
  the locally known default branch, branch drift, and every linked worktree's
  cleanup classification, facts, and recommended next step.
- Include the same structured repository-health report in `doctor --json` so
  automation can distinguish safe, blocked, and review-required states.
- Keep the report explicitly local-ref based and non-fatal when a default
  branch cannot be determined; doctor continues with a health-unavailable
  warning rather than changing the repository.
- Retain `project clean` as the only cleanup command and as the sole command
  that can plan or perform explicitly confirmed Git maintenance.

## Capabilities

### New Capabilities

- `project-doctor-repository-health`: Doctor exposes a diagnostic,
  cleanup-aware repository health summary for the root checkout and its linked
  worktrees.

### Modified Capabilities

None. The prior project-command and cleanup changes are still active change
records rather than archived baseline specifications.

## Impact

The `project` doctor report, its JSON output, disposable Git worktree tests,
and README guidance change. No command fetches, pushes, merges, removes a
worktree, deletes a branch, or reads credential values as part of this change.
