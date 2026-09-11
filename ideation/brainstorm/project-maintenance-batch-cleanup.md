# Batch Cleanup of Eligible Worktrees — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Extend cleanup to retire a fixed set of eligible worktrees with one reviewed plan and immediate per-target revalidation.
Topics: project-maintenance, batch-cleanup, project-clean, project-clean-branch-retirement
Repository context: opensoft/openRepoProject; explicit cleanup within one Git repository.
Captured: 2026-09-11

## Possible feats

- A repository-scoped `clean --all-safe` plan and explicit batch apply using the existing retirement operation.

## Focus and baseline

The proposed batch command reduces repeated selection and confirmation when
several worktrees are already eligible for cleanup. It does not make additional
classes of work eligible. All examples are design sketches, not installed flags.

At inspected cleanup commit `12db36a`, confirmed worktree removal already removes
allowlisted disposable Python caches and retires the paired local branch with
normal `git branch -d`. The earlier suggestion to keep branch deletion as a
separate batch opt-in was based on older code. Proposed default here preserves
the newer combined operation and states both removals in the confirmation.
Independent branch-only cleanup remains outside this batch's first version.

## User interface and selection

```sh
project clean Atlas --all-safe
project clean Atlas --all-safe --json
project clean Atlas --all-safe --apply
project clean Atlas --all-safe --apply --yes
```

`--all-safe` without `--apply` prints a read-only plan. Apply confirms the exact
listed worktrees, paired local branches, and disposable cache paths. `--yes`
explicitly accepts that selected plan for scripted use. Keep `--json` read-only,
matching the existing cleanup interface; machine-readable apply results can be
designed separately. Reject combinations with individual `--action`, `--branch`,
or `--worktree` selectors so scope is never ambiguous.

“All” means eligible linked worktrees of one resolved Git repository. It does
not mean all projects in a folder, family members, or mounted spec/code legs.
Resolve the target through existing discovery, then expose the selected
repository in the plan. Inspection from a family or assembly root must not
silently broaden retirement to its child repositories.

List selected entries and excluded entries with reasons. An empty eligible set
prints “No eligible worktrees” and returns 0 without prompting. Sort by a stable
path ordering. New worktrees appearing after confirmation are never added.

## Eligibility

Use the existing `merged-removable` decision as a prerequisite, plus explicit
batch checks for worktree locks and incomplete inspection. Every target needs:

- A readable, clean, named non-default branch in a non-current linked worktree.
- Its exact tip proven to be an ancestor of the local cleanup target branch.
- Known acceptable upstream state under the current cleanup classifier.
- No blocking ignored files; only the existing disposable Python cache allowlist.
- No Git worktree lock or unavailable parent/common-directory identity.

Preserve dirty, detached, unpublished, unpushed, remote-gone, remotely ahead,
diverged, current, default, locked, or uncertain worktrees. An inspection failure
for any linked worktree makes the batch plan incomplete and blocks apply; an
ordinary fully understood exclusion does not block other eligible targets.
Do not prune stale worktree metadata as a side effect.

GitHub merge evidence is explanatory only. A squash merge generally does not
put the original branch tip into local main's ancestry, even after main is
updated. Such a branch stays excluded with a clear reason. Merely fetching or
reconciling main cannot be promised to make it eligible. Supporting squash-merge
retirement would require a separate preservation/equivalence design.

## Plan and execution model

The in-memory plan records repository/common-directory identity, local target
branch and SHA, surviving command directory, exact selected worktree paths,
branch names and SHAs, upstream evidence, current/locked state, ignored paths,
and the concrete cache/worktree/local-branch operations. Its JSON preview also
includes schema version, observation time, exclusions, and completeness.

Confirm the complete plan once. Then perform a full preflight revalidation
before the first mutation and revalidate each target immediately before acting.
Require the local merge target SHA, branch tip, ownership, cleanliness, lock
state, and relevant ignored-file state to still match the confirmed plan.
Changed safety evidence stops the batch and requires a fresh invocation.
Informational API availability alone should not invalidate otherwise identical
local deletion evidence; define a safety-specific comparison model.

For each selected worktree, reuse the same retirement primitive as a single
remove action: discard the inspected disposable caches, remove the worktree
without force, then recheck the branch tip and local ancestry and delete the
paired branch without force. Run follow-up commands from the validated surviving
default worktree. Refuse a plan without a suitable surviving command directory.

Do not follow symlinks during cache cleanup. A changed path, new symlink, lock,
or Git refusal stops execution. Revalidation reduces concurrency risk but is
not an atomic lock over editors and other agents; keep Git's own refusals and
fail closed rather than retrying forcefully.

## Partial completion and recovery

The batch is ordered and not transactional. Stop at the first changed target or
failed operation. Do not roll back successful retirement by creating new work.
Print per-target stages: pending, caches removed, worktree removed, local branch
deleted, refused, or failed. Mark all later entries “not attempted”, and report
the failing command and its exit status. Cancellation also reports completed
stages before exiting 130.

If branch deletion fails after worktree removal, explicitly report that the local
branch remains. If caches were removed before a later refusal, report that too;
disposable cache bytes are not recoverable through Git. Remote branches remain
untouched. The initial plan names the branch tips and retained local target so
that reconstruction instructions can be based on known retained commits.
Require a new plan for retry; do not resume from a stale saved selection.

Proposed exit behavior: 0 when every selected operation completes or the eligible
set is empty; 2 for invalid input or changed-state refusal; preserve a delegated
operation's nonzero exit code on execution failure. Excluded protected work is
reported without implying a batch failure. `--apply` without confirmation on
noninteractive stdin refuses before mutation.

## Validation scenarios for a later implementation

- Several eligible trees retire in order; current/default/dirty/locked trees
  remain, and no push, fetch, force option, or remote deletion occurs.
- A new target after confirmation is not selected. A changed target or changed
  main SHA before the first action causes zero mutations.
- A changed later target stops the batch after earlier successes and reports
  their completed stages accurately.
- Cache failure, worktree removal failure, and branch deletion failure each
  preserve later targets; the report accurately identifies what remains.
- A squash-merged exact-head PR does not become removable through remote evidence.
- Space-containing paths, ignored symlinks, cancelled input, empty plans, and
  incomplete inspection keep the same safety rules as single-target cleanup.

## Alternatives and open decisions

Continuing after failures would maximize cleanup but make partial state harder
to reason about. Prefer stop-on-first-failure, consistent with current retirement.
A persistent resumable plan adds stale-state and storage contracts; defer it.

Confirm the final flag spelling and whether a later version needs branch-only
batch retirement. Paired deletion is the recommended default based on the newer
cleanup behavior, rather than a newly approved product decision.

## Relationships

The [maintenance flow](project-maintenance-synthesis-inspect-and-retire.md)
explains the boundary with [project overview](project-maintenance-project-discovery.md).
The [packet overview](project-maintenance-overview.md) describes the overall scope.
