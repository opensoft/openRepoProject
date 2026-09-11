## 1. Remote merge evidence

- [x] 1.1 Resolve the cleanup target's configured remote-tracking ref and,
  when needed, exact-head GitHub pull-request state; record local and remote
  evidence while preserving an explicit unavailable state.
- [x] 1.2 Classify remote-only merges separately from branches unmerged in
  both targets, preserve local-only removal eligibility, and expose the
  distinction through clean and doctor human/JSON reports.

## 2. Documentation and verification

- [x] 2.1 Add disposable Git fixture coverage for remote-only ancestry,
  squash-style exact-head GitHub merge, neither-target merge, unavailable
  evidence, and refusal to remove a remote-only merge; verify the existing
  local-removal path is unchanged.
- [x] 2.2 Update README guidance with the last-fetched remote comparison and
  the reconciliation boundary; verify it matches the cleanup plan.
- [x] 2.3 Run the full py-bench suite, diff checks, strict OpenSpec validation,
  and live clean/doctor audits; verify all pass before review.
- [x] 2.4 Commit and push the governed change on cleanup, update PR #2,
  request review, and resolve any resulting findings with regression evidence.
