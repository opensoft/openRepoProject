# Batch Cleanup of Eligible Worktrees — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Extend the current explicit worktree-removal action to retire a bounded set of eligible linked worktrees with one reviewed plan and immediate per-target revalidation.
Topics: project-maintenance, batch-cleanup, project-clean, project-clean-worktree-removal
Repository context: opensoft/openRepoProject; explicit cleanup within one Git repository.
Captured: 2026-09-11

## Possible feats

- A repository-scoped `clean --all-safe` plan and explicit batch apply that reuses the current safe worktree-removal operation.

## Focus and baseline

The proposed batch command reduces repeated selection and confirmation when
several worktrees are already eligible for cleanup. It does not make new
classes of work eligible. All examples are design sketches, not installed
flags.

The current remote baseline is `origin/main` at `a040790`. Its governing
cleanup contract has separate `remove` and `delete-branch` actions: removing a
worktree leaves its local branch intact, and branch deletion requires a later
explicit action. The cleanup branch contains later unmerged changes in
`5fc2b51` (paired branch retirement), `1789ad9` (disposable cache handling),
and `bb91a49` (cache deletion hardening). `12db36a` is review closure only.

This MVP deliberately targets the current contract. It batches worktree
removal only. It does not silently depend on paired branch retirement or cache
disposal from the cleanup branch. If a future proposal adopts either
extension, it must update the cleanup specification and add the extension's
failure and recovery contract first.

## User interface and selection

```sh
project clean Atlas --all-safe
project clean Atlas --all-safe --json
project clean Atlas --all-safe --apply
project clean Atlas --all-safe --apply --yes
```

`--all-safe` without `--apply` prints a read-only plan. Apply confirms the exact
listed worktrees and their retained local branches. `--yes` explicitly accepts
that selected plan for scripted use. Keep `--json` read-only, matching the
existing cleanup interface; machine-readable apply results can be designed
separately. Reject combinations with individual `--action`, `--branch`, or
`--worktree` selectors so scope is never ambiguous.

“All” means at most 100 eligible linked worktrees of one resolved Git
repository. The hard target cap prevents an accidental unbounded destructive
batch. Inspect at most 1,024 linked worktrees, allow five seconds per Git
probe, and allow sixty seconds for the invocation. If an inspection limit is
reached, mark the plan incomplete and refuse apply. If more than 100 entries
qualify within the inspection limits, the plan is complete for inspection but
also refuses apply and tells the user to narrow the target or make a later
explicitly designed larger batch. The plan reports the eligible count, target
cap, inspection limits, number of Git probes, and estimated worktree
operations.

It does not mean all projects in a folder, family members, mounted spec/code
legs, pinned member copies, or independent clones. Resolve the target through
existing discovery, then expose the selected repository and common-directory
identity in the plan. Inspection from a family or assembly root must not
silently broaden retirement to child repositories.

List selected entries and excluded entries with reasons. An empty eligible set
prints “No eligible worktrees” and returns 0 without prompting. Sort by a stable
canonical path ordering. New worktrees appearing after confirmation are never
added.

## Eligibility and merge-target terminology

Use the existing `merged-removable` decision as a prerequisite, plus explicit
batch checks for worktree locks and incomplete inspection. Every target needs:

- A readable, clean, named non-merge-target branch in a non-current linked
  worktree.
- Its exact tip proven to be an ancestor of the local merge target.
- A known acceptable upstream state under the current cleanup classifier:
  upstream ref present, tracking ref resolvable, ahead and behind counts
  known, and neither local work nor remote divergence present.
- No blocking ignored files and no unresolved inspection error.
- No Git worktree lock or unavailable parent/common-directory identity.

Use `merge target` as the one canonical term for the local branch whose tip is
used by `merge-base --is-ancestor`. Resolve it in this order: a manifest
`tracking_branch`, the local branch named by `origin/HEAD` after removing the
`origin/` prefix, `main`, then `master`. Select the first existing local
branch, record both its name and resolution source, and record its current SHA.
`default branch` is a human-facing synonym only. `upstream` or `tracking ref`
means the feature branch's configured remote-tracking ref and is a separate
piece of evidence.

Preserve dirty, detached, unpublished, unpushed, remote-gone, remotely ahead,
diverged, current, merge-target, locked, or uncertain worktrees. An inspection
failure for any linked worktree makes the batch plan incomplete and blocks
apply; an ordinary fully understood exclusion does not block other eligible
targets. Do not prune stale worktree metadata as a side effect.

Local ancestry is the only removal proof in this MVP. GitHub or remote-target
merge evidence is outside the batch gate. A squash merge generally does not
put the original branch tip into local merge-target ancestry, so such a branch
stays excluded with a clear reason. Supporting squash-merge retirement would
require a separate preservation/equivalence design.

## Plan and execution model

The in-memory plan records repository/common-directory identity, merge-target
name, resolution source and SHA, the surviving command directory, exact
selected worktree paths, branch names and SHAs, upstream ref and tracking-ref
OID, ahead/behind counts, cleanliness, lock state, ignored paths, and the
concrete worktree-removal operations. Its JSON preview also includes schema
version, observation time, the 100-target and 1,024-worktree caps, probe and
time budgets, estimated probe/operation counts, exclusions, and completeness.

Confirm the complete plan once. Then perform a full preflight revalidation
before the first mutation and revalidate each target immediately before acting.
Require the merge-target name, resolution source and SHA, feature branch tip,
ownership, cleanliness, lock state, ignored-file state, upstream ref identity,
tracking-ref OID, ahead/behind counts, and classification to still match the
confirmed plan. A changed upstream or tracking-ref state is safety evidence
and stops the batch, even when the worktree itself is unchanged. No fetch is
performed to refresh that evidence. Informational API availability is outside
this MVP and never invalidates local evidence.

For each selected worktree, invoke the same non-force `worktree remove`
operation as the existing single-target `remove` action. Run follow-up
commands from the validated surviving merge-target worktree. Refuse a plan
without a suitable surviving command directory. After removal, verify the
paired local branch still exists and report its retained SHA; branch deletion
is intentionally not part of this operation.

Revalidation reduces concurrency risk but is not an atomic lock over editors
and other agents. Keep Git's own refusals and fail closed. A branch advancing
after the final check cannot be silently deleted by this MVP because branch
deletion is separate; record the changed state and stop before later targets.

## Partial completion and recovery

The batch is ordered and not transactional. Stop at the first changed target
or failed operation. Do not roll back successful worktree retirement by
creating new work. Print per-target stages: pending, worktree removed, refused,
failed, or not attempted. Mark all later entries “not attempted”, and report
the failing command and its exit status. Cancellation reports completed stages
before exiting 130.

The normal successful result explicitly says that each local branch remains.
If a user later wants a retained branch deleted, the existing explicit command
is the recovery path:

```sh
project clean Atlas --apply --action delete-branch --branch feature/name --yes
```

That command creates a fresh report, rechecks local merge-target ancestry and
the current branch tip, and leaves the branch intact if Git refuses deletion.
It gives a retry path after a worktree-only batch without inventing an implicit
branch operation. Remote branches remain untouched.

Proposed exit behavior: 0 when every selected removal completes or the
eligible set is empty; 2 for invalid input, a target-cap refusal, or changed
state; preserve a delegated operation's nonzero exit code on execution
failure. Excluded protected work is reported without implying a batch failure.
`--apply` without confirmation on noninteractive stdin refuses before
mutation.

## Deferred cache and paired-retirement extension

Cache disposal and paired local-branch retirement are separate future design
options because neither is part of `origin/main`'s current batch contract.
They must not be smuggled into the MVP's “worktree removed” stage.

If cache disposal is proposed later, a candidate path or any ancestor that is
a symlink is ineligible for cache deletion and is preserved. The implementation
must use descriptor-relative, no-follow operations (`O_NOFOLLOW`/equivalent),
verify the opened directory identity against the planned device/inode, and
fail closed when the platform cannot provide those guarantees. A pathname
check followed by recursive deletion is insufficient because a writable parent
could be replaced between the check and the delete.

The cache extension must report each cache path separately. If a later path
fails, earlier removals remain recorded as permanent partial cache completion;
the report rescans the worktree, marks the cache phase partial, and gives
retry guidance. It must stop before worktree or branch mutation when cache
preflight fails. A proposal must also set hard limits for cache entries and
bytes and include them in the plan estimate.

If paired retirement is proposed later, branch deletion remains a separate
post-removal stage with an immediate branch-head and local-ancestry check. A
changed head or a Git refusal retains the branch, stops later targets, and
reports the already removed worktree plus the surviving branch. The existing
explicit `delete-branch` command remains the retry path. No future composite
operation may force-delete or force-push.

## Validation scenarios

- Several eligible trees retire in stable order; current, merge-target, dirty,
  locked, remote-ahead, and unmerged trees remain, every retained local branch
  is reported, and no push, fetch, force option, branch deletion, or remote
  deletion occurs.
- A new target after confirmation is not selected. A changed merge-target SHA,
  feature branch tip, upstream OID, lock, ignored-file state, or classification
  before the first action causes zero mutations.
- A changed later target stops the batch after earlier worktree removals and
  reports their retained branches and completed stages accurately.
- More than 1,024 linked worktrees or a probe/time budget hit produces an
  incomplete read-only plan and refuses apply before any mutation, with the
  limit and omitted or timed-out work visible.
- More than 100 eligible targets within the inspection limits produces a
  complete read-only plan and refuses apply before any mutation, with the cap
  and estimate visible.
- A branch advances after the final per-target check: the worktree removal
  either refuses safely or completes while retaining the changed branch; later
  targets are not attempted and the report identifies the state.
- A worktree-removal failure preserves later targets and identifies the failed
  command, exit status, and all retained branches.
- Space-containing paths, missing external paths, cancellation, empty plans,
  locked worktrees, and incomplete inspection keep the same safety rules as the
  single-target command.
- A future cache extension rejects symlink candidates and ancestor swaps,
  leaves external targets intact, reports each path after partial failure, and
  never follows a symlink or uses broad recursive deletion.
- A future paired-retirement extension retains a branch when its head changes
  after revalidation and permits retry through explicit `delete-branch`.

## Alternatives and open decisions

Continuing after failures would maximize cleanup but make partial state harder
to reason about. Prefer stop-on-first-failure, consistent with current
retirement. A persistent resumable plan adds stale-state and storage contracts;
defer it. Confirm the final flag spelling, the target cap, and whether cache
disposal or paired retirement deserves a separate proposal.

## Relationships

The [maintenance flow](project-maintenance-synthesis-inspect-and-retire.md)
explains the boundary with [project overview](project-maintenance-project-discovery.md).
The [packet overview](project-maintenance-overview.md) describes the overall scope.
