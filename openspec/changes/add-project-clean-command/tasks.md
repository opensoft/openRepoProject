## 1. Cleanup state model

- [x] 1.1 Extend local Git inspection to collect each linked worktree's path, branch, cleanliness, upstream, ahead/behind counts, detached state, and merged ancestry; verify with disposable repositories and confirm no fetch or write occurs.
- [x] 1.2 Classify cleanup findings, protect the default branch, and generate equivalent human/JSON plans; verify dirty, detached, unpublished, unpushed, pushed-unmerged, merged-removable, and stale-ref scenarios.

## 2. Explicit cleanup actions

- [x] 2.1 Add the `clean` parser, help text, and read-only default report; verify target discovery works from a nested directory and the report states its local-ref freshness.
- [x] 2.2 Implement confirmed non-force feature-branch push delegation with upstream handling and per-target failure propagation; verify failed pushes preserve repository state.
- [x] 2.3 Implement confirmed removal of only clean, merged, non-current worktrees; verify dirty, current, detached, and unmerged worktrees are refused without force.
- [x] 2.4 Implement separately confirmed deletion of only verified merged local branches after worktree removal; verify unmerged and default branches cannot be deleted.
- [x] 2.5 Report pull-request/merge handoffs for pushed-but-unmerged branches and refuse unsafe/noninteractive apply requests; verify no PR or merge command runs implicitly.

## 3. Documentation and verification

- [x] 3.1 Document command syntax, classifications, safety guarantees, and the distinction between cleanup and `park`/`resume`; verify examples match help output.
- [x] 3.2 Run the complete test suite and focused read-only smoke checks against the existing openRepoProject worktrees; verify the feature branch is clean and no remote or local work is changed by the default command.
