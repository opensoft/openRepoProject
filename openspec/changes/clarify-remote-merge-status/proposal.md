## Why

`project clean` currently labels a pushed feature as "locally unmerged" when
the local target branch does not contain it. That wording is technically true
but confusing when the last-fetched remote target branch already contains the
feature, because it does not tell the user that local reconciliation—not an
unmerged GitHub review—is the remaining step.

## What Changes

- Compare each feature head with both the local target branch and its
  last-fetched remote-tracking counterpart when that counterpart is available.
- When ancestry does not establish a merge, inspect GitHub pull-request state
  for the exact feature head when the repository has a usable GitHub identity.
- Report a feature as merged remotely but awaiting local reconciliation when
  either remote target ancestry or its exact-head GitHub pull request is
  merged.
- Report a feature as not merged only when remote evidence establishes that;
  preserve an explicit unknown state when remote comparison cannot be
  established.
- Keep cleanup destructive actions gated on local merge verification; the
  audit remains read-only and does not fetch or reconcile branches.

## Capabilities

### New Capabilities

- `project-clean-remote-merge-status`: Accurate, last-fetched remote merge
  status in cleanup and doctor repository-health reports.

### Modified Capabilities

None. Existing active change records are not archived baseline specifications;
this change defines the additional remote-status contract separately.

## Impact

The `project` cleanup audit and doctor repository-health output, their JSON
contracts and tests, plus README guidance change. The read-only audit may make
a one-shot GitHub pull-request status query; it does not fetch, merge, remove
branches, or change confirmed cleanup eligibility.
