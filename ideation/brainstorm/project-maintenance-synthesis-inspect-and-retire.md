# Synthesis: Inspect Projects and Retire Finished Work — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Connect broad project discovery to narrowly scoped cleanup through shared evidence and a fresh explicit plan.
Topics: project-maintenance, maintenance-flow, overview-discovery, batch-cleanup, synthesis
Repository context: opensoft/openRepoProject; boundaries between workstation reporting and repository mutation.
Captured: 2026-09-11

## Possible feats

- Consistent “inspect this repository next” navigation from the workstation overview into a newly computed cleanup plan.

## Members and their joints

Members: [overview and attention](project-maintenance-project-discovery.md) and
[batch cleanup](project-maintenance-batch-cleanup.md). These are exploratory
designs, not approved contracts or an implementation task list.

### Scope narrows before action

Overview discovers many local projects and identifies maintenance opportunities.
Its suggested next command names a single repository and requests a cleanup
preview. The user reviews that preview before asking for batch apply. Overview
does not emit an apply command with confirmation already bypassed.

```text
overview → choose repository → clean --all-safe preview → confirmed apply
```

Independent clones stay independent throughout this flow. Family grouping does
not grant permission to clean every sibling. Spec/code legs and pinned member
mounts retain their owning tool's rules and never become implicit batch targets.

### Evidence is reusable; permission is not

Use shared checkout identities and classification meanings across reports.
Overview observations may be stale by the time cleanup starts. Cleanup always
recomputes eligibility, freezes its own plan, and revalidates before mutation.
Do not treat overview JSON, a green badge, or a merged PR as deletion approval.

Default overview remains local and bounded. An optional remote inspection can
explain an exact-head PR merge, but the cleanup gate uses local ancestry.
Preserve that distinction when sharing collectors: remote visibility is not a
new retirement proof. A squash merge remains a separate unresolved lifecycle
case even if both screens recognize that it happened on GitHub.

### Different failure policies serve different purposes

Overview continues after individual project failures so the rest of the estate
stays visible; its completeness and exit status expose omissions. Cleanup stops
on the first failed mutation or changed target because earlier successful
retirements cannot be rolled back as a transaction. These policies can coexist
over a common evidence model without sharing one catch-and-continue wrapper.

## Emergent behavior and boundaries

The combined experience lets a user find finished work across projects and
retire it repository by repository with fewer repetitive commands. A subsequent
overview reflects the actual remaining work; there is no automatic apply loop,
daemon, cross-project cleanup, or new park/resume implementation.

Keep facts, diagnostics, planning, and execution as distinct interfaces inside
the existing CLI. Share bounded read-only probes and public schemas; keep the
single-target and batch retirement operations on one implementation path.
This is a design direction, not a mandate for a particular module/file split.

## Tensions and open decisions

The broad view benefits from speed while cleanup needs exact fresh evidence.
Prefer an invocation-local cache for overview and fresh probes for cleanup.
“Attention” should not make normal ongoing work look broken; keep housekeeping
opportunities distinct from warnings and errors.

Decide later how much per-worktree detail fits in the default overview and
whether users need category filters before they need a second command alias.
Shared JSON finding codes can later support a dashboard without authorizing a
dashboard to execute cleanup. That is a recombination possibility, not scope
for these two features.

Return to the [packet overview](project-maintenance-overview.md).
