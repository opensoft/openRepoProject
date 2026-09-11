## Context

See proposal.md for the user-facing ambiguity. Cleanup already determines
local target ancestry and records branch tracking state without fetching. The
target branch's own upstream is the only reliable local evidence for the
corresponding remote target. GitHub can report that an exact branch head was
merged even when squash or rebase history prevents an ancestry proof.

## Goals / Non-Goals

**Goals:**

- Distinguish remote-target merge evidence from local-target merge evidence in
  both human and JSON reports.
- Make the "not merged" message accurate when both Git ref and GitHub evidence
  are available.
- Preserve local ancestry as the sole eligibility proof for destructive cleanup.

**Non-Goals:**

- Fetch, pull, reconcile branches, compare patch equivalence, or treat
  squash/rebase merges as ancestry.
- Change cleanup actions, remote branch handling, or the read-only default.

## Decisions

1. **Use the local target worktree's configured upstream as the remote target.**
   It supports repositories whose primary remote is not named `origin` and
   avoids guessing from a feature branch upstream. A missing or non-resolvable
   upstream produces an explicit unknown state rather than an assumed result.

2. **Use an exact-head GitHub PR lookup when ancestry is inconclusive.** A
   one-shot `gh pr list` query is scoped to the target repository, base branch,
   feature branch, and recorded head SHA. A merged result identifies a squash
   or rebase merge without conflating a later branch reuse with an older PR.
   An unavailable CLI, identity, or query result remains unknown rather than
   being interpreted as unmerged.

3. **Expose separate local, remote-ref, and GitHub PR evidence.** The audit retains
   `merged_into_target` for local safety decisions and adds the last-fetched
   remote target plus `merged_into_remote_target` and exact-head GitHub state
   for explanation. Any remote `merged` result with a local `false` receives a
   distinct, non-removable classification.

4. **Keep local ancestry as the removal proof.** GitHub PR state improves the
   explanation but cannot make a worktree removable; only the local target can
   establish the safe branch-deletion relationship.

## Risks / Trade-offs

- [A remote ref is stale] → Every human message and JSON report retains the
  last-fetch freshness label; no action follows from remote evidence alone.
- [A GitHub lookup is unavailable or slow] → The bounded one-shot query is
  reported as unavailable and the audit remains non-destructive.
- [A branch is reused after an earlier PR] → Matching the current head SHA
  prevents an older merged PR from being used as evidence for newer commits.

## Migration Plan

Add disposable Git fixtures for remote-only ancestry, exact-head GitHub merge,
neither-target merge, and unavailable evidence. Update the human and JSON
report contract, run the isolated test suite plus strict OpenSpec validation,
and roll back through a normal code revert if needed.
