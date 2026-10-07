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
designs, not approved contracts or an implementation task list. Both were
revised on 2026-10-07, and the joints below use their shared vocabulary
exactly.

### Scope narrows before action

The overview MVP discovers bounded local projects and identifies maintenance
opportunities. Its suggested next command names one repository and requests a
read-only cleanup report or `--all-safe` preview. The user reviews that
preview before asking for batch apply. Overview never emits `--apply` or
`--yes`, so it cannot hand off a command with confirmation already bypassed.

```text
overview → choose repository → clean --all-safe preview → confirmed worktree removal
```

Independent clones stay independent throughout this flow. Family grouping,
when added later, does not grant permission to clean every sibling. Spec/code
legs and pinned member mounts retain their owning tool's rules and never become
implicit batch targets.

### Shared vocabulary

Both documents use these objects and codes with the same names, so a caller
can compare an overview row with a cleanup plan field by field.

| Object | Fields | Rule |
| --- | --- | --- |
| repository identity | `{root, common_dir, dev, ino}` | one identity probe, `git rev-parse --path-format=absolute --show-toplevel --git-common-dir` (`--git-common-dir` alone in a bare repository); `root` is the realpath of the main worktree toplevel, or `null` for a bare repository; `common_dir` is the realpath of the common directory; `dev` and `ino` come from a no-follow `os.lstat` of `common_dir`; the four fields together are the identity, and a path or name alone never is |
| worktree identity | `{path, dev, ino, admin_id}` | `path` is the realpath from `git worktree list --porcelain -z`; `dev` and `ino` come from `os.lstat` of `path`; `admin_id` is the `<id>` in the worktree's `.git` file, accepted only when that file and `<common_dir>/worktrees/<id>/gitdir` name each other |
| merge target | `{name, source, sha}` | `source` is `manifest`, `origin-head`, `main`, or `master`; the manifest is read at `repository.root`; the first candidate that exists as a local branch in the ref listing wins, and `sha` is its tip; a manifest that conflicts with `origin/HEAD` wins with an informational `merge-target-conflict`; a manifest that cannot be read or has the wrong kind is `manifest-invalid`; no candidate at all is `no-merge-target`, a batch refusal and an overview repair finding |
| bounds | `limits`, `budget` | `worktree_rows` counts every registry entry, the main worktree included (overview 512, batch 128); `ignored_entries` 64, `status_records` 4096, and `ignored_samples` 8 in both; the overview adds `roots` 32, `candidates` 128, and `root_entries` 4096, and the batch adds `targets` 16; `probe_timeout_seconds` 5, `invocation_timeout_seconds` 60, and `probe_concurrency` (overview 4, batch 1) in both, and the batch adds `reconciliation_reserve_seconds` 10 and `removal_floor_seconds` 5 |
| work accounting | `probes`, `omitted` | `probes: {estimated, performed}` counts Git probe children, timed-out and stopped ones included (the batch counts removals separately in `operations`); `omitted: {count, exactness}`, with `exactness` `exact`, `lower-bound`, or `unknown`, reports work a cap or the deadline dropped |
| errors | `{code, message, path?}` | row codes `os-error`, `probe-failed`, `probe-timeout` (one probe or filesystem call reached its own 5 s limit), and `deadline-exceeded` (the global deadline was the limit); `git-too-old` (Git older than 2.36) and `git-unavailable` (a missing `git`, or a failed, timed-out, or unparseable `git --version`) refuse with exit 2 before any repository probe; under `--json` an exit-2 refusal prints the baseline error object with a `code` added, `{"error", "code"}`, which batch cleanup extends with its plan fields, and an argument error prints no JSON; `null` means unknown, never `false` or `0` |

### The Git-first handoff

An overview row's `suggested_command` is `null` unless a finding supplies one.
When present it is a JSON argument vector naming the absolute canonical
`repository.root`: `["project", "clean", "<root>", "--all-safe"]` when the row
has a `merged-removable` housekeeping finding, no worktree row of the repository
is `inspection-error`, and the repository has no more than 128 worktree rows,
otherwise the read-only `["project", "clean", "<root>"]`. It is never a shell
string or a bare name, it never carries `--apply` or `--yes`, and a row whose
`root` is `null` or not valid UTF-8 gets no clean suggestion.

Every `project clean` mode (the read-only report, `--json`, `--all-safe`,
and `--apply --action push|remove|delete-branch`) resolves an absolute path
Git-first: its realpath must equal the toplevel Git reports there, and that
toplevel must be the main worktree, or the run refuses with
`target-not-repository-root` and exit 2 and substitutes no other directory.
`discover`'s manifest-ancestor and family-holder redirections never apply to
a path. A relative path or no argument resolves to the repository Git finds
there; only a bare name keeps the baseline `discover` lookup, its one Git
child counted and deadline-bounded, and the overview never calls `discover`
at all. The plan reports the same `repository` and `merge_target` as the
overview row, so a script can detect that the directory now holds a
different repository, and `--expect-plan <plan_digest>` binds a scripted
apply to one preview.

### One evidence model; permission is not shared

Overview, doctor, and clean read one evidence model. Every Git child runs with
the variables `git rev-parse --local-env-vars` lists removed from its
environment, from a list hard-coded from Git 2.43, and read-only children also
set `GIT_OPTIONAL_LOCKS=0`. One `git --version` child runs per invocation. Each
repository then costs the same four repository-wide children, memoized per
`common_dir` and fanned out to every row: identity; the registry listing,
`git worktree list --porcelain -z`, which also yields `locked` and `prunable`;
the ref listing, one `for-each-ref` over `refs/heads` and `refs/remotes` whose
NUL-separated format string is identical in both documents and gives the
`origin/HEAD` target and every branch's head, upstream, upstream object id,
ahead and behind counts, and `gone` state; and the merged set, one
`for-each-ref --merged=<merge-target sha>` over `refs/heads`. Merge-target
resolution spawns no child. Each present, registration-verified worktree row,
the main worktree included, gets exactly one combined bounded probe,
`git status --porcelain=v1 -z --untracked-files=normal --ignored=matching`,
which stops reading at a 65th ignored record or a 4,097th record of any kind; a
row whose path is missing, unreadable, or fails the two-way registration check
gets none, and an unreadable or registration-mismatched row is set to
`inspection-error` directly, so a mismatched row on the merge-target branch
never reads as `protected-default`. Every worktree-specific probe runs as
`git -C <worktree path>` against that worktree's own index, only after its
identity is verified, because each linked worktree has its own index;
repository-wide probes run as `git -C <repository.root>` (`common_dir` for a
bare repository), except the identity probe, which runs in the candidate. When a
linked worktree is reached first, the registry listing also runs in the
candidate, because the main worktree's path comes from that listing; that
changes which directory the command runs in, never which index a probe reads.
Because they share the ref listing, overview, doctor, and clean all report a
deleted upstream as `remote-gone`, where the baseline reports `unpublished`;
both are preserve states.

Batch cleanup adds two index gates the overview never applies, checked last for
a row that passes every other gate: an `lstat` of its admin `modules` directory
and one bounded `git -C <worktree path> ls-files -v --stage -z` inside the row's
own worktree. Any gitlink (mode `160000`) or `modules` entry excludes the row as
`contains-submodule`, because non-force `git worktree remove` refuses a worktree
that holds a populated submodule or whose admin directory holds `modules`, so
such a row would otherwise stall every batch. An entry flagged assume-unchanged
or skip-worktree excludes it as `hidden-local-state`, because Git's status, and
so both the combined probe and Git's own pre-removal check, cannot see edits to
such files; a sparse checkout is therefore excluded too.

Evidence is reusable; permission is not. Overview observations may be stale by
the time cleanup starts, and the overview's memo lives only for one invocation.
Cleanup always recomputes eligibility, freezes its own plan, and revalidates
each target before mutation with at most five children (the identity probe, the
registry listing, a ref listing narrowed to the merge-target candidates,
`origin/HEAD`, and the selected branches and their upstreams, and, inside the
target worktree, the combined probe and the hidden-state probe) plus a re-read
of the manifest and the target's `modules` check. Do not treat overview JSON, a
green badge, a merged PR, or a remote status as deletion approval.

### One mutation seam and the narrow guarantee

Single-target `--apply --action remove --worktree P` and the batch call the same
`retire_worktree(plan, target)`: revalidate; then, only while at least
`removal_floor_seconds` (5 s) of the work deadline remains, spawn the non-force
removal from the command directory in its own process group,

```sh
git -c status.showUntrackedFiles=normal -C <command directory> worktree remove <path>
```

reap; and reconcile by rescan. With less than the floor left, the target and
every later one are `not-attempted` with `deadline-exceeded`, and the run exits
with status 1. Single-target removal is strictly a one-item batch: it builds the
same full plan (`mode: "single"`) under the same caps, selects only P, and lists
every other eligible row as `not-requested`. It refuses with
`worktree-not-found` when P matches no registry entry, with `target-excluded`,
whose `reason` carries the exclusion reason, when a gate excludes P, and with
`inspection-incomplete` when any row of the repository is `inspection-error`. It
therefore shares the plan entry, command, refusal codes and messages, stages,
and exit codes with a batch whose only target is P.

Every target ends in the closed stage enum
`pending | removed | refused | failed | unknown | not-attempted`, where
`pending` never appears in a final record. Every `removed`, `refused`, `failed`,
or `unknown` target carries a reconciliation record, `registry_entry_present`,
`path_present`, `branch_present`, `branch_sha`, and `reconciled`, while a
`not-attempted` target carries `null`, even one that passed revalidation before
the removal floor stopped the batch; `removed` needs rescan evidence that the
registry entry and the path are both gone with `reconciled: true`, never the
child's exit status alone. The plan and the apply result record both report
`probes` and `operations` as `{estimated, performed}`, and each target its
`probes_performed`. The MVP removes only the linked worktree; the local branch
stays available for the separate `delete-branch` action, and a later
paired-retirement or cache extension needs its own stages and contract inside
the same seam.

The safety guarantee is narrow. Concurrent writers (editors, other agents, other
`project` invocations, and Git commands run by anyone else) are outside the safe
contract, and no lock, lease, or writer-quiescence handoff is claimed. A removal
child is spawned only if, at the revalidation immediately before spawning it,
the repository identity, the target's worktree identity and branch evidence,
every baseline signature field, its `locked` flag, the absence of submodules and
of hidden local state in its own index, the manifest's `tracking_branch`, and
the merge target's name, source (re-resolved from a fresh read of the manifest),
and SHA all equal the confirmed plan. Git's own non-force refusal is the last
line of defense, and the `status.showUntrackedFiles=normal` override keeps its
untracked-file check working whatever the user's configuration. Ignored files
created, and index flags set, between revalidation and removal fall in a
documented residual window, not under the guarantee.

### Different failure policies serve different purposes

The overview continues after individual project failures so the rest of the
local estate stays visible. Its collector turns each candidate's failure into
an error row, `completeness` and the exit status expose omissions, and it
exits 0, 1 (incomplete, an error-severity finding, or a warning under
`--strict`), 2 (invalid invocation, `git-too-old` or `git-unavailable`, or an
exception raised outside the collector boundary), or 130 (SIGINT).

Cleanup stops after the first target whose result is not a plain `removed`: a
`refused`, `failed`, or `unknown` target, or a removal followed by a branch
change. Earlier successful removals cannot be rolled back as a transaction, so
every later target is `not-attempted`. The first matching exit wins: 130
(SIGINT, or input ended at the prompt); 1 (the deadline stopped work after the
apply phase began, including a removal not spawned because less than
`removal_floor_seconds` (5 s) of the work deadline remained, or any target is
`unknown`, including one whose handling raised an exception); the Git child's
own status for a target `failed` with `git-refused` (128) or `git-failed` (any
other nonzero status, such as 255); 2 (any refusal code, a `refused` target, a
removal with a branch-after-removal reason, or `failed` with `spawn-error`);
otherwise 0. A read-only preview exits 0 for a complete plan, even one that
`target-cap` blocks, 1 for an incomplete one, and 2 when no plan can be built.
The two policies share the evidence model, not one catch-and-continue wrapper.

### Concurrency across repositories, never inside one

The overview runs at most four read-only Git children at once
(`probe_concurrency: 4`), across distinct repositories and never two once
their `common_dir` is known to be the same. Only the identity probe, which
runs before its repository is known and takes no lock, may overlap for
candidates that turn out to share a repository. Batch cleanup works inside
one repository and probes serially by design (`probe_concurrency: 1`). Apart
from that read-only identity overlap, work inside one repository is serial in
both features, and the overview's two-phase scheduling keeps its output
order canonical whatever the completion order.

### Local evidence and deferred remote visibility

Default overview and cleanup use local refs and state as of the last fetch. A
future opt-in remote overview may explain an exact-head pull request, using a
validated canonical repository identity, bounded deduplicated requests, and
explicit unknown results for credentials or API failures. Remote visibility
never becomes a cleanup proof. A squash merge remains a separate unresolved
lifecycle case unless a new preservation/equivalence design is approved.

## Emergent behavior and boundaries

The combined MVP lets a user find finished work across local projects and
remove eligible worktrees repository by repository with fewer repetitive
commands. A subsequent overview reflects the actual remaining work. There is
no automatic apply loop, daemon, cross-project cleanup, implicit branch
deletion, cache deletion, persistent cache, lock or quiescence protocol, or
new park/resume implementation.

Keep facts, diagnostics, planning, and execution as distinct interfaces inside
the existing CLI. Share the bounded read-only probes, the identity and
merge-target objects, and the classifier meanings; keep the single-target
worktree-removal action and the batch action on the one `retire_worktree` seam.
Group Git probes by `common_dir`, while preserving one combined status result
for each worktree row, including external paths reported by Git. Both features
require Git 2.36 or newer for `worktree list --porcelain -z` and read every path
NUL-delimited; a path that is not valid UTF-8 is reported escaped with
`path_valid_utf8: false` and is never a removal operand. Both print a path that
holds a control, bidirectional, or format character, or an undecodable byte, in
the same `$'…'` form: each undecodable byte as `\xHH`, each decoded control,
bidirectional, or format code point as `\uXXXX` (a newline is `\u000a`), both in
lowercase hexadecimal, and each backslash doubled. JSON escapes every such code
point, so neither document carries one raw, and pasting the `\uXXXX` form into
bash or zsh needs a UTF-8 locale.

Each feature bounds its own work under one monotonic 60 s invocation deadline
with 5 s per Git child, and both derive their caps at 150 ms per Git child, a
1.5× margin over an assumed 100 ms, with candidate and worktree-row caps in
powers of two. The overview's 128 candidates and 512 worktree rows fit the
deadline with four children at once across repositories after a listing phase
estimated at about 6 s, which leaves about 54 s for Git work; its 32 roots cost
no Git child, and each root's listing task is bounded at 5 s. The batch, serial
inside a 50 s work deadline that the 10 s reconciliation reserve leaves, uses
one fit test: a cap pair fits when its worst case completes within the work
deadline and spawns its last removal with at least `removal_floor_seconds` (5 s)
left. Its row cap is the largest power of two for which at least 16 targets fit,
and its target cap the largest multiple of 8 that fits with that row cap: 128
worktree rows and 16 targets, with a worst case of about 39.9 s. 256 rows admit
fewer than 16 targets under the test, and 24 targets would fit the deadline
alone, but the 21st removal would start inside the floor. A cap hit or a
deadline expiry is always visible as an incomplete result (`scan-limit` or
`deadline-exceeded` in the overview; `inspect-cap`, `inspection-incomplete`, or
`deadline-exceeded` in the batch), never a silently shortened complete one. The
batch's target cap instead keeps a complete plan that lists every row passing
every gate before the two index gates (`contains-submodule` and
`hidden-local-state`) and refuses apply with `target-cap`.

## Tensions and open decisions

The broad view benefits from speed while cleanup needs exact fresh evidence. The
overview keeps an invocation-local memo and cross-repository concurrency;
cleanup takes fresh probes serially and revalidates each target. Whether the
overview's caps survive measurement is open. If the proposal rejects
concurrency, the fallback is 32 candidates and 128 worktree rows run serially
(257 children, about 38.6 s at 150 ms, or about 44.6 s with the listing
estimate). And because one repository's children always run serially, a single
repository with more than about 355 worktree rows cannot complete at that rate
unless rows are capped per repository.

The overview's `--all-safe` suggestion follows the batch's own gates. A worktree
the ladder classifies `merged-removable` yields the housekeeping finding and the
suggestion only when it also passes, in the batch's order, the main-worktree,
path-byte, registration, and lock gates; otherwise the first failing gate's
finding (`main-worktree`, `unsupported-path-bytes`, `registration-mismatch`, or
`locked-worktree`, the same codes the batch uses as exclusion reasons) replaces
it, and the row's classification stays what the ladder computed. A fifth gate
covers the whole repository: while any of its worktree rows is
`inspection-error` (an unreadable path, a registration-mismatched row, or a
failed status probe), or while it has more than 128 worktree rows, the batch
plan would be refused as `inspection-incomplete` or `inspect-cap`, so the
overview withholds every `--all-safe` suggestion for that repository, and its
housekeeping findings and the row suggest only the read-only
`project clean <root>`. The gate changes suggestions only, not the overview's
completeness. The gates the overview cannot apply are the batch's two index
gates, read through its `git -C <worktree path> ls-files -v --stage -z` probe
and an `lstat` of its admin `worktrees/<id>/modules` directory, so a preview may
still exclude a suggested worktree as `hidden-local-state` or
`contains-submodule`; the plan lists that exclusion, and the suggestion is
advisory either way.

“Attention” should not make normal ongoing work look broken; keep housekeeping
opportunities distinct from warnings and errors.

Before proposal, decide the measured costs and therefore the final caps, whether
the MVP limits should be configurable, whether the `attention` alias merits a
separate command, whether `--apply --json` prints the apply result record,
whether `--expect-plan` is required with `--yes`, whether a relative path or the
default must name an exact repository root, whether a sparse checkout's
skip-worktree entries for absent files may count as safe, whether a
never-populated gitlink may count as removable, and whether family, remote,
bench, container, park, cache, or paired-branch behavior warrants a separate
change. The packet overview holds the full consolidated list. Keep each
extension bounded and preserve explicit ownership and recovery semantics.

Return to the [packet overview](project-maintenance-overview.md).
