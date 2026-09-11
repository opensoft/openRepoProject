## 1. Disposable-artifact cleanup

- [x] 1.1 Classify exact ignored paths into the Python bytecode allowlist and
  blocking artifacts in cleanup reports; verify human and JSON output preserve
  the distinction without changing a read-only audit.
- [x] 1.2 Extend confirmed remove to revalidate and delete only listed,
  contained non-symlink caches before worktree and branch retirement; verify
  cache-deletion failure or changed classification stops later destructive steps.
- [x] 1.3 Anchor post-removal Git commands to the surviving target-branch
  worktree; verify cleanup invoked from the retiring worktree still retires its
  verified local branch.

## 2. Documentation and verification

- [x] 2.1 Add disposable Git fixture coverage for successful Python-cache
  retirement, unknown/symlink blockers, failure containment, and exact-path
  revalidation; verify no broad ignored-file deletion is used.
- [x] 2.2 Update README guidance with the current disposable-cache allowlist
  and the preserved unknown-file boundary; verify documented behavior matches
  the cleanup plan.
- [x] 2.3 Run the full py-bench suite, diff checks, strict OpenSpec validation,
  and a read-only cleanup audit; verify all pass before review.
- [x] 2.4 Commit and push the governed change on cleanup, update PR #2, request
  review, and resolve any resulting findings with regression evidence.
