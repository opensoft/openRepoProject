## 1. Repository-health reporting

- [x] 1.1 Build doctor repository-health rows from the cleanup audit, including
  default-branch drift status and unavailable-health handling; verify JSON
  preserves cleanup classifications and adds health level/status fields.
- [x] 1.2 Render the repository-health summary and aggregate doctor check for
  every complete project/family snapshot; verify ordinary doctor remains
  read-only while strict mode recognizes health warnings.

## 2. Documentation and verification

- [x] 2.1 Add disposable Git fixture coverage for default divergence, linked
  worktree warnings, and unknown-default resilience; verify human and JSON
  reports identify the relevant health state.
- [x] 2.2 Update README guidance to distinguish diagnostic doctor health from
  explicit project clean maintenance; verify commands and safety statements
  match the implementation.
- [x] 2.3 Run the complete test suite in py-bench, diff checks, strict OpenSpec
  validation, and a read-only doctor audit; verify all pass before review.
- [x] 2.4 Commit and push the governed change on cleanup, update PR #2, request
  review, and resolve any resulting review findings with regression evidence.
