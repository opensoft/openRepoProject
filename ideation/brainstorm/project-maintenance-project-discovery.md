# Project Overview and Attention — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Discover local projects once and show their health and unfinished work in a compact workstation overview.
Topics: project-maintenance, overview-discovery, project-command, project-doctor-repository-health
Repository context: opensoft/openRepoProject; local discovery and reporting using existing owner tools.
Captured: 2026-09-11

## Possible feats

- Project overview with an attention filter, family grouping, partial-result reporting, and a shared JSON representation.

## Focus and baseline

The current CLI inspects a selected project. The proposed feature answers
“Which of my projects needs attention?” across a configured projects directory.
This is exploratory design only; all command examples below are proposed.

Baseline inspected: the first CLI at commit `562fdc7` and the later cleanup
work at `12db36a`. The later work adds repository health, disposable-cache
classification, and GitHub merge evidence. Recheck the implementation when an
OpenSpec proposal is created; these notes do not describe the current remote tip.

## User interface

```sh
project overview
project overview --root ../projects
project overview --attention
project attention
project overview --json
project overview --remote
```

Proposed default: `overview` shows every discovered project; `attention` is an
alias for `overview --attention`. Both use the same collector and renderer.
The default roots come from the existing `PROJECTS_DIR` resolution; repeatable
`--root` arguments replace those defaults. Avoid a second persistent registry.

Each project row shows its name, kind, location, health summary, worktree count,
unpushed-work count, parked-feature count when known, bench/container state,
and a concrete next command. Expand children only where they explain a finding.
Duplicate names include enough relative path information to distinguish them.

Illustrative output, not a report of current repositories:

```text
Atlas     2 items    feature/login has unpushed commits; container stopped
Ledger    1 item     feature/export is merged locally and eligible for cleanup
Notes     unknown   Git inspection failed; other project results are complete
```

Attention includes failures, incomplete inspection, missing declared checkouts,
dirty work, unpushed or diverged branches, unavailable declared environments,
and eligible cleanup opportunities. Ordinary unmerged work with no other
problem remains informational. Parked features are contextual, not inherently
a problem. Unknown optional profile fields do not become false failures.
The presentation distinguishes “needs repair”, “work to preserve”, and
“housekeeping available” without forcing the user to interpret raw Git flags.

## Bounded discovery

1. Inspect each configured root itself and its immediate children for Git,
   `project.yaml`, `family.yaml`, `.project.json`, or `.devcontainer` markers.
2. Recognize the established `Family/Family` holder layout and inspect declared
   working siblings. Do not recursively crawl arbitrary descendant folders.
3. For projects, follow declared leg paths for reporting. Represent pinned
   family members separately from working siblings; pinned copies are not
   independent working projects or cleanup targets.
4. Discover linked worktrees from Git's worktree registry, including paths
   outside the scan root. Display these as children of their repository.

Deduplicate aliases by resolved directory. Group linked worktrees by the Git
common-directory identity, not merely by remote URL. Independent clones of the
same remote remain distinct local workspaces. Family membership is a display
relationship and does not confer authority or exclusive ownership.
Show one inspection result per checkout even when several family relationships
refer to it. Preserve all those relationships as references.

Do not descend through arbitrary directory symlinks. Explicit roots may resolve
through symlinks, while declared paths retain existing containment checks.
Use a visited set for cycles. Malformed manifests remain visible as findings;
they must not disappear from the list because normal discovery refused them.
An explicit root that cannot be read contributes an incomplete-scan result.

## Collection and data model

Reuse `discover`, `repo_state`, `snapshot`, and the existing health classifiers.
Separate evidence gathering from rendering and optional remote lookup so that
overview does not inherit an unconditional GitHub query from repository health.
The same fact should have the same meaning in overview, doctor, and clean.

Proposed JSON envelope: `schema_version`, `observed_at`, `roots`, `projects`,
`relationships`, `summary`, and `scan_errors`. Each finding includes a stable
code, category, severity, checkout identity, evidence source, observation time,
and suggested next command. Include an explicit completeness indicator and
retain unknown values rather than converting failed probes to zero or false.

Report Git comparisons as last-fetched local refs. No default fetch or GitHub
request. `--remote` opts into bounded read-only PR queries for the exact branch
head; report local and remote evidence separately, with their observation times.
API failure produces “remote status unavailable”, not “unmerged”. This mode
does not alter refs or invoke validators. Cache repeated probes only within
the current invocation; persistent caching is deferred.

Bound concurrency and timeouts per probe so one unavailable checkout or Docker
daemon does not stall the estate. Cache workstation-wide tool and registry
checks once, and group shared failures once with affected project references.
Read only the existing public profile fields and park-record summary fields;
never dump credential files or unrelated profile data.

## Result semantics

Proposed exits: 0 for a complete scan without errors (warnings and housekeeping
may be present); 1 for project errors or an incomplete scan; 2 for invalid
invocation; 130 for cancellation. A proposed `--strict` additionally makes
warnings return 1. The attention filter affects display, not collection or exit
status. A successful scan with no projects says so explicitly and exits 0.

## Validation scenarios for a later implementation

- A family holder, working sibling, mounted member, and linked feature produce
  understandable relationships without duplicate project counts.
- Two independent clones with the same origin remain distinct; duplicate names
  and symlink aliases remain unambiguous.
- Unreadable folders, invalid manifests, missing legs, and timed-out Git probes
  return useful partial results and a nonzero exit.
- Default inspection makes no remote request or filesystem mutation;
  `--remote` keeps unavailable PR evidence explicitly unknown.
- Attention filtering and JSON preserve severity, freshness, and completeness;
  public output excludes extra secret-like profile fields.

## Alternatives and open decisions

An arbitrary-depth recursive scan would find more nested repositories but would
be slower and prone to discovering dependency/vendor trees. Prefer bounded
discovery with explicit additional roots for the first version.

Confirm later whether the `attention` alias merits a separate command and whether
active clean unmerged work should have an opt-in attention category. Prototype
large-estate output before fixing default column widths or concurrency limits.
Exact bench/type validation is useful existing-doctor follow-up work, not an
additional feature silently included in this design.

## Relationships

The [maintenance flow](project-maintenance-synthesis-inspect-and-retire.md)
connects this view to [batch cleanup](project-maintenance-batch-cleanup.md).
The [packet overview](project-maintenance-overview.md) defines the scope.
