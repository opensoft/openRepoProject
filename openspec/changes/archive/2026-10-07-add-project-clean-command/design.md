## Context

See `proposal.md` for the motivation. The existing `project` executable already
resolves repositories and linked worktrees and performs local Git inspection;
`status` and `doctor` intentionally do not mutate them. The new command must
add explicit maintenance without taking ownership of Git transport, review
policy, or the Speckit parking implementation.

## Goals / Non-Goals

**Goals:**

- Produce one deterministic local cleanup plan for the current repository and
  all of its linked worktrees.
- Safely carry clean feature branches to their remote branches with a normal
  push when explicitly requested.
- Retire only clean, merged, non-current worktrees, with branch deletion as a
  separate opt-in action.
- Make dirty, detached, unpublished, unmerged, and default-branch work
  visible and preserve it.

**Non-Goals:**

- Automatically fetch, merge, force-push, reset, stash, or reconcile divergent
  branches.
- Creating or merging pull requests, approving reviews, or bypassing branch
  protection.
- Reimplementing `park`, `resume`, Speckit worktree creation, or shape pinning.

## Decisions

1. **Plan first, one explicit action at a time.** `project clean` without an
   apply action is read-only. Apply mode accepts a specific operation and
   target (push a branch, remove a worktree, or delete a verified merged local
   branch); `--all-safe` may batch only operations already proven safe. This
   makes the output reviewable and prevents a broad cleanup from becoming an
   accidental merge or deletion.

2. **Use local refs and state by default.** Reuse the existing Git probe
   helpers with `GIT_OPTIONAL_LOCKS=0`. Compare branch tips with local
   remote-tracking refs and label every comparison "as of the last fetch".
   An explicit future fetch option can be added separately without changing
   the default safety contract.

3. **Protect the default branch.** The command may identify an ahead default
   branch and print the repository's normal push/PR handoff, but it will not
   push or delete it. Feature branch pushes require a clean checkout and use
   `git push` with an existing or explicitly selected upstream, never a force
   flag.

4. **Treat merge verification as ancestry, not a merge operation.** A local
   branch is removable only when its tip is an ancestor of the selected
   tracking branch and the worktree is clean. A pushed-but-unmerged branch is
   handed off to the normal PR process; the command does not infer approval or
   invoke a merge API.

5. **Keep action output machine-readable.** The report model will contain
   repository/worktree identity, classification, evidence, and proposed
   action. Human output will explain each decision; JSON will expose the same
   facts for workstation tooling and later automation.

## Risks / Trade-offs

- **Remote-tracking refs may be stale** → state the last-fetch limitation on
  every report and never claim remote freshness without an explicit fetch.
- **A local branch can be merged remotely but not locally** → classify it as
  review-required until local ancestry proves removal safe.
- **A clean worktree can still contain valuable unpublished commits** → require
  both ancestry and a safe remote/preservation state before removal; otherwise
  preserve it.
- **Batch cleanup can hide individual failures** → process each requested
  action independently, print per-target results, and return nonzero when any
  requested action is refused or fails.
- **Different repositories enforce different review policies** → keep PR and
  merge operations as handoffs and never bypass protected default branches.

## Migration Plan

Implement and test the command in `openRepoProject`, then update the pinned
artifact in workBenches after the source change lands on `main`. Run the new
read-only audit against the existing `openRepoProject` checkout first. Apply
only the explicitly confirmed push/removal actions that the audit identifies.
Rollback is a normal code revert; a removed worktree can be recreated from its
preserved branch, while no remote branch deletion is part of this change.
