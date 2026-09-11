## 1. Paired branch retirement

- [x] 1.1 Extend confirmed safe-worktree removal to plan and execute normal local branch deletion after successful worktree removal; verify a merged feature worktree and its local branch are both retired while its remote branch remains.
- [x] 1.2 Preserve partial-failure safety when normal branch deletion fails after worktree removal; verify the failure is returned and no force-delete is attempted.

## 2. Documentation and verification

- [x] 2.1 Update cleanup documentation to describe paired local branch retirement and retained safety boundaries; verify documented commands match CLI behavior.
- [x] 2.2 Run the complete offline test suite, diff checks, strict OpenSpec validation, and a read-only cleanup audit; verify all pass before review.
- [x] 2.3 Commit and push the governed change on `cleanup`, request review, and resolve any resulting review findings with regression evidence.
