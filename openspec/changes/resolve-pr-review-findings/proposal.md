## Why

PR #1 is mechanically mergeable, but current review findings show unsafe cleanup
deletion, potential profile-data disclosure, malformed-configuration crashes,
and delegated update paths that can bypass owner safety checks. These defects
need correction before the command becomes the project-facing entry point.

## What Changes

- Make `project clean` fail closed for ignored files, uncertain default-branch
  detection, diverged/behind remote state, and changed state after confirmation.
- Preserve configured upstream mappings when pushing a local branch whose remote
  branch name differs.
- Limit portable profile data to the supported public schema fields before it is
  rendered in status or doctor output.
- Centralize validation of workBench registry structures so doctor and bench
  updates return structured refusals instead of tracebacks.
- Require complete, safe child checkouts before updates and retain the owning
  shape tool's confirmation prompt.
- Add regression coverage for every corrected review path and close stale review
  feedback with evidence rather than an unrelated code change.

## Capabilities

### New Capabilities

- `project-review-safety`: Safe configuration parsing, profile reporting, and
  owner-delegated update behavior for the project command.
- `project-clean-review-safety`: Fail-closed cleanup classifications and actions
  that preserve local Git work not proven safe to retire.

### Modified Capabilities

None. The existing change specifications have not yet been archived into the
baseline specification set; this remediation records the tightened contracts
as standalone review-safety capabilities.

## Impact

The `project` executable, its disposable Git/configuration tests, README safety
guidance, and PR review state are affected. No dependencies, remotes, or user
worktrees are changed by the remediation itself.
