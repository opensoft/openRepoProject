# Synthesis: Inspect Projects and Retire Finished Work — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Connect bounded project discovery to narrowly scoped worktree cleanup through shared local evidence and a fresh explicit plan.
Topics: project-maintenance, maintenance-flow, overview-discovery, batch-cleanup, synthesis
Repository context: opensoft/openRepoProject; boundaries between workstation reporting and repository mutation.
Captured: 2026-09-11

## Possible feats

- Consistent “inspect this repository next” navigation from the workstation overview into a newly computed batch worktree-removal plan.

## Members and their joints

Members: [overview and attention](project-maintenance-project-discovery.md) and
[batch cleanup](project-maintenance-batch-cleanup.md). These are exploratory
designs, not approved contracts or an implementation task list.

### Scope narrows before action

The overview MVP discovers bounded local projects and identifies maintenance
opportunities. Its suggested next command names one repository and requests a
cleanup preview. The user reviews that preview before asking for batch apply.
Overview does not emit an apply command with confirmation already bypassed.

```text
overview → choose repository → clean --all-safe preview → confirmed worktree removal
```

Independent clones stay independent throughout this flow. Family grouping,
when added later, does not grant permission to clean every sibling. Spec/code
legs and pinned member mounts retain their owning tool's rules and never become
implicit batch targets.

### Evidence is reusable; permission is not

Use shared checkout identities, merge-target resolution, and classification
meanings across reports. Overview observations may be stale by the time
cleanup starts. Cleanup always recomputes eligibility, freezes its own plan,
and revalidates before mutation. The overview's common-directory memoization
is a performance aid; cleanup still records and verifies its own evidence.

Do not treat overview JSON, a green badge, a merged PR, or a remote status as
deletion approval. The current cleanup MVP removes only the linked worktree;
the local branch stays available for the existing separate `delete-branch`
action. Any later paired-retirement or cache extension needs its own contract.

### Local evidence and deferred remote visibility

Default overview and cleanup use local refs and state as of the last fetch. A
future opt-in remote overview may explain an exact-head pull request, using a
validated canonical repository identity, bounded deduplicated requests, and
explicit unknown results for credentials or API failures. Remote visibility
never becomes a cleanup proof. A squash merge remains a separate unresolved
lifecycle case unless a new preservation/equivalence design is approved.

### Different failure policies serve different purposes

Overview continues after individual project failures so the rest of the local
estate stays visible; its completeness and exit status expose omissions.
Cleanup stops on the first failed mutation or changed target because earlier
successful removals cannot be rolled back as a transaction. These policies can
coexist over a common evidence model without sharing one catch-and-continue
wrapper.

## Emergent behavior and boundaries

The combined MVP lets a user find finished work across local projects and
remove eligible worktrees repository by repository with fewer repetitive
commands. A subsequent overview reflects the actual remaining work. There is
no automatic apply loop, daemon, cross-project cleanup, implicit branch
deletion, cache deletion, or new park/resume implementation.

Keep facts, diagnostics, planning, and execution as distinct interfaces inside
the existing CLI. Share bounded read-only probes and public schemas; keep the
single-target worktree-removal action and the batch action on one implementation
path. Group Git probes by common-directory identity, while preserving one
worktree-specific status result for each linked checkout, including external
paths reported by Git.

## Tensions and open decisions

The broad view benefits from speed while cleanup needs exact fresh evidence.
Prefer invocation-local caches for overview and fresh probes for cleanup.
“Attention” should not make normal ongoing work look broken; keep housekeeping
opportunities distinct from warnings and errors.

Before proposal, decide whether the MVP limits should be configurable, whether
the `attention` alias merits a separate command, and whether family, remote,
bench, container, park, cache, or paired-branch behavior warrants a separate
change. Keep each extension bounded and preserve explicit ownership and
recovery semantics.

Return to the [packet overview](project-maintenance-overview.md).
