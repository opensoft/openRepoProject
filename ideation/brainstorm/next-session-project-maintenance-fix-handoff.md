# Next Session: Project Maintenance Design Fixes — Brainstorm

Status: brainstorm
Kind: process
Summary: Handoff for resolving the remaining pre-PR review findings in the project maintenance design packet.
Topics: next-session, project-maintenance, review-followup
Repository context: opensoft/openRepoProject; follow-up work for the project maintenance brainstorm packet.
Captured: 2026-09-11

## Possible feats

- A final design review that is traceable from each safety concern to a concrete contract, scenario, and later OpenSpec decision.

## Current state

The design branch is `docs/project-maintenance-design` at commit `e3a5288`.
It is clean, pushed to origin, and has no pull request. The four-document
packet passes the brainstorm packet validator:

- [Packet overview](project-maintenance-overview.md)
- [Project overview and attention](project-maintenance-project-discovery.md)
- [Batch cleanup](project-maintenance-batch-cleanup.md)
- [Inspect and retire synthesis](project-maintenance-synthesis-inspect-and-retire.md)

The packet remains design-only. Do not create an OpenSpec proposal, change
implementation code, or open the PR until the findings below are resolved and
the packet has passed a fresh review.

## Next-session objective

Make the design packet precise enough to open for review against
`origin/main`, whose current cleanup baseline is `a040790`. Keep the MVP
bounded to local overview reporting and explicit batch worktree removal. Keep
branch deletion, cache disposal, remote queries, family traversal, bench,
container, and park integrations as separately governed extensions unless a
later decision brings one into scope.

## Priority findings to resolve

### 1. Define the batch safety boundary

The [batch design](project-maintenance-batch-cleanup.md) still describes
path-based removal after revalidation while acknowledging that editors or
other processes may change the checkout between those steps. Decide and write
one deterministic guarantee:

- either establish a writer-quiescence/ownership handoff and stable identity
  checks before removal, or
- narrow the guarantee explicitly so concurrent writers are outside the safe
  contract and any identity change causes a refusal.

Define the observable identity as the Git common-directory and worktree-admin
registration plus no-follow device/inode checks for the repository and target
path. A path string by itself is insufficient. State what happens when the
target directory, repository parent, branch, or ignored files change after
confirmation.

Choose one deterministic branch-race result. The MVP keeps the local branch,
so a changed branch must produce a refused target, exit 2, and no later target
attempts. If removal succeeds before the change is observed, the postcondition
must rescan and report the removed worktree plus the retained branch SHA.

### 2. Make execution and interruption reconcilable

Clarify that `--apply` recomputes, displays, and confirms its own fresh plan;
the earlier read-only preview is advisory and is never silently reused. Define
one shared mutation seam so single-target removal and a one-item batch have the
same plan, revalidation, command, and refusal behavior.

Use one global deadline that covers Git probes and the removal subprocess, with
an explicit timeout unit. Cancellation or deadline expiry must stop new work,
terminate and reap the in-flight child when possible, rescan the Git worktree
registry, target path, repository identity, and retained branch, then report
`outcome-unknown` when state cannot be established. Return a nonzero result and
never claim a target completed from a subprocess exit alone.

Post-operation reconciliation must define stages for removed, refused, failed,
and unknown outcomes. It must record whether the Git registry entry exists,
whether the target path exists, and whether the local branch and SHA remain.

### 3. Bound and share the expensive work

The current design has limits, but the next revision must make their execution
model implementable:

- Separate repository-wide probes from worktree-specific probes. Memoize one
  common-directory probe and fan it out; use targeted per-worktree revalidation
  instead of recomputing the full report for every target.
- Define the five-second probe and sixty-second invocation deadlines against a
  monotonic global deadline. Include subprocess cancellation and omitted-result
  reporting. Reduce the 1,024-worktree and 100-target caps if the measured
  operation count cannot meet the deadline.
- Sort canonical candidate paths before applying discovery caps. An omitted
  count after early stop is a lower bound or unknown unless it was obtained
  within the same directory-entry/time budget.
- Bound ignored-file inspection and report size with count/truncation fields;
  do not materialize an unbounded `git status --ignored` result in memory or
  JSON.
- If remote inspection remains in the deferred text, add response page,
  item, and byte limits. A global deadline must cancel queued and in-flight
  requests and classify truncation as unknown.

### 4. Make the repository and JSON contracts explicit

The batch command must not require a merge-target worktree if the current
`origin/main` operation can execute from the resolved repository root. Define
the command directory as the canonical resolved repository root, subject to
the identity checks above, and preserve the existing explicit branch action.

Define the overview JSON and batch JSON separately or state an additive
compatibility plan. Preserve existing cleanup fields such as `root`,
`target_branch`, `tracking_freshness`, and `worktrees` when compatibility is
required. For every proposed envelope, record required field types, stable
identity rules, enum values, unknown/error representation, completeness, and
schema evolution. Add representative fixtures rather than only listing field
names.

Suggested commands and JSON rows must carry the canonical repository path or
common-directory identity, so duplicate project names and independent clones
cannot hand off to an ambiguous `project clean` invocation.

### 5. Close discovery scope and acceptance gaps

In the MVP, a `family.yaml` marker is reported as a holder-only local project.
Do not traverse siblings, pinned members, or mounted legs until a family
integration is separately proposed. Add a scenario proving the holder count,
relationship handling, and probe ownership.

Define the collector boundary before calling existing helpers: malformed,
unreadable, no-merge-target, and timed-out candidates become visible result
records with errors, while healthy projects continue. Existing helpers that
raise for one candidate must not erase the rest of the scan.

Add acceptance scenarios for:

- manifest-declared, `origin/HEAD`, `main`, `master`, conflicting, and missing
  merge targets, including source and SHA selection and zero mutation;
- every protected cleanup classifier, with only `merged-removable` selected;
- `--attention` filtering repair, preservation, housekeeping, and ordinary
  unmerged informational work while keeping exit semantics stable;
- a present eligible external linked worktree and a missing/unreadable one;
- newline, tab, and control-character paths, using NUL-delimited Git output or
  an explicit supported-byte refusal;
- canonical repository identity through the overview-to-clean handoff.

## Deferred remote boundary

Keep remote inspection deferred unless the next session intentionally scopes it
into a separate design. If the detailed constraints remain in the packet,
require canonical GitHub identity, rejection of credential-bearing remotes,
bounded deduplicated requests, response-size/page limits, redaction, and
explicit unknown results for 401, 403, rate-limit, timeout, and truncation.
Remote evidence remains explanatory and never authorizes cleanup.

## Suggested work order

1. Reconcile the batch contract with `origin/main` and remove any remaining
   prerequisite inherited from unmerged cleanup commits.
2. Specify identity, writer/race behavior, global deadlines, cancellation, and
   post-operation reconciliation.
3. Specify the shared single-target/batch mutation seam and exact JSON fields.
4. Narrow and formalize overview collection, family-holder behavior, caps,
   probe accounting, and error isolation.
5. Add the acceptance scenarios and deferred-extension boundaries above.
6. Run the packet validator, whitespace checks, and a fresh pre-PR review. Open
   the PR only when the review has no actionable findings.

## Completion gate

The next session is complete when the four packet documents plus this handoff
are clean and pushed, the packet validator passes, every high/P1 finding has a
written contract and scenario, and no implementation or OpenSpec proposal has
been created. The PR description should state that the branch contains design
only and link this handoff for the review trail.
