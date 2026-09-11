# Project Overview and Attention — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Discover local projects once and show their Git health and unfinished work in a compact bounded workstation overview.
Topics: project-maintenance, overview-discovery, project-command, project-doctor-repository-health
Repository context: opensoft/openRepoProject; local discovery and reporting using existing owner tools.
Captured: 2026-09-11

## Possible feats

- A bounded local project overview with an attention filter, linked-worktree grouping, partial-result reporting, and a shared JSON representation.

## Focus and baseline

The current CLI inspects a selected project. The proposed MVP answers
“Which of my local projects needs attention?” across explicitly configured
roots. This is exploratory design only; all command examples below are
proposed.

The current remote baseline is `origin/main` at `a040790`. It provides local
project discovery, Git state, and cleanup reporting. The later cleanup branch
adds behavior in `5fc2b51`, `1789ad9`, and `bb91a49`; those commits are
extension evidence and are not assumed by the overview MVP. The old `12db36a`
review-closure commit is not a health or cache implementation anchor.

## User interface

```sh
project overview
project overview --root ../projects
project overview --attention
project overview --json
```

Proposed default: `overview` shows every discovered local project;
`--attention` filters the same collected result to findings that need repair,
work preservation, or available housekeeping. Repeatable `--root` arguments
replace the existing `PROJECTS_DIR` defaults. Avoid a second persistent
registry.

`project attention` and `project overview --remote` remain possible later
interfaces. They are not MVP requirements. If the alias is retained, it must
call the same collector and renderer; if remote inspection is added, it must
follow the remote boundary below.

Each MVP row shows the project name and location, kind when recognized, local
Git health, linked-worktree count, preservation findings, cleanup opportunities
when known, and a concrete next command. Per-worktree detail is expanded only
when it explains a finding. Duplicate names include enough relative path
information to distinguish them.

Illustrative output, not a report of current repositories:

```text
Atlas     2 items    feature/login has unpushed commits; one worktree is removable
Ledger    1 item     feature/export is merged locally and eligible for cleanup
Notes     unknown    Git inspection failed; other project results are complete
```

Attention includes failures, incomplete inspection, dirty work, unpushed or
diverged branches, and eligible worktree cleanup opportunities. Ordinary
unmerged work with no other problem remains informational. The presentation
distinguishes “needs repair”, “work to preserve”, and “housekeeping available”
without forcing the user to interpret raw Git flags.

## MVP scope and hard bounds

The MVP inspects each explicit root itself and its immediate child directories
for Git or project markers (`project.yaml`, `family.yaml`, `.project.json`, or
`.devcontainer`). It does not recursively crawl arbitrary descendants. The
initial design limits one invocation to 32 roots, 256 candidate project
directories, and 1,024 linked worktrees. A proposal may tune these defaults,
but it must keep hard limits and expose them in the result.

When a limit is reached, stop adding candidates, retain the results already
collected, add a `scan-limit` error with the limit and omitted-count status,
mark the scan incomplete, and return the incomplete-scan exit. Do not silently
turn an incomplete overview into a complete one.

Discover linked worktrees from Git's worktree registry, including paths outside
the configured root, because the registry is the source of truth for one local
repository. A missing or unreadable external path remains visible as an
unknown/incomplete child result. The overview does not enter that path or
change it as part of discovery.

Deduplicate aliases by resolved directory. Group linked worktrees by the Git
common-directory identity, not merely by remote URL. Perform one canonical
repository probe per common-directory identity and fan its shared state out to
the checkout rows; perform worktree-specific status probes once per linked
path. Independent clones of the same remote remain distinct local workspaces.

Do not descend through arbitrary directory symlinks. Explicit roots may resolve
through symlinks, while declared paths retain existing containment checks. Use
a visited set for cycles. Malformed manifests remain visible as findings;
they must not disappear because normal discovery refused them. An explicit
root that cannot be read contributes an incomplete-scan result.

Family holders, declared siblings, mounted members, and parked-work records
are deferred integrations. When a later design adds them, it must preserve
one inspection result per checkout, retain relationship references separately,
and avoid counting pinned copies as independent working projects.

## Collection and data model

Reuse `discover`, `repo_state`, and the existing local health classifiers.
Separate evidence gathering from rendering so the overview can continue after
one project fails. The same local fact should have the same meaning in
overview, doctor, and clean.

The MVP JSON envelope is proposed as `schema_version`, `observed_at`, `roots`,
`projects`, `relationships`, `summary`, `completeness`, and `scan_errors`.
Each finding includes a stable code, category, severity, checkout identity,
evidence source, observation time, and suggested next command. Unknown values
remain unknown; failed probes never become zero or false. A cap hit or
unreadable external worktree is represented in `scan_errors` and affects
`completeness`.

Use local refs only. Do not fetch, pull, reset, bootstrap, run validators, or
make filesystem mutations during the overview MVP. Report ahead/behind and
merge status as observations based on the last-fetched refs, with their
freshness stated in both human and JSON output. Give each Git probe a five
second timeout and the invocation a sixty second budget; a timeout records an
incomplete result and leaves other projects eligible for inspection.

Cache workstation-wide checks only when they exist in the MVP; memoize shared
Git probes by common-directory identity and fan out the result. Do not read
credential files or unrelated profile data.

## Deferred remote inspection boundary

If a later proposal adds an explicit `--remote`, it must be opt-in and
read-only. Derive the query identity from a validated canonical GitHub remote
(`github.com/owner/repository`); strip an optional `.git` suffix and never
print or forward URL-embedded credentials. A credential-bearing, malformed,
or non-GitHub remote produces `remote status unavailable` without a request.

Deduplicate requests by `(host, owner/repository, exact feature-head SHA)`;
use at most 64 requests per invocation, at most four concurrently, a five
second per-request timeout, and a thirty-second remote budget. A rate limit,
401, 403, or other API failure produces an explicit unknown result and no
private metadata in output. Use the normal GitHub client authentication path;
the overview never tests, displays, or infers credential values. Local ancestry
remains the cleanup gate even when a remote query reports a merged pull
request. Persistent remote caching is deferred.

Bench/container status, park records, and family relationships have equivalent
deferred boundaries: opt-in probes, bounded time, explicit unknown values, and
no mutation. They do not belong in the MVP acceptance contract.

## Result semantics

Proposed exits: 0 for a complete scan without errors (warnings and housekeeping
may be present); 1 for project errors, a cap hit, or an incomplete scan; 2 for
invalid invocation; 130 for cancellation. A proposed `--strict` additionally
makes warnings return 1. The attention filter affects display, not collection
or exit status. A complete scan with no projects says so explicitly and exits 0.

## MVP validation scenarios

- Two independent clones with the same origin remain distinct; duplicate names
  and symlink aliases remain unambiguous.
- One repository with several linked worktrees receives one common-directory
  probe and one status probe per checkout; a worktree outside the configured
  root is grouped under that repository without increasing the project count.
- An external linked-worktree path that is missing or unreadable remains visible
  with an explicit unknown/incomplete result and does not abort other projects.
- Unreadable roots, invalid manifests, and timed-out Git probes return useful
  partial results and a nonzero incomplete-scan exit.
- Root, candidate, and worktree caps stop discovery with a `scan-limit` error;
  the report names the cap and does not claim complete coverage.
- Default inspection makes no network request or filesystem mutation. JSON
  preserves severity, freshness, unknown values, and completeness.

## Deferred validation scenarios

- A remote request with a canonical URL is deduplicated by exact head; malformed
  and credential-bearing URLs are rejected without exposing credentials, and
  401/403 responses remain unknown.
- A family holder, working sibling, mounted member, and parked record are
  represented as relationships without duplicate checkout probes when those
  integrations are separately proposed.

## Alternatives and open decisions

An arbitrary-depth recursive scan would find more nested repositories but would
be slower and prone to discovering dependency/vendor trees. Prefer bounded
discovery with explicit additional roots for the first version.

Confirm later whether the `attention` alias merits a separate command and
whether large-estate limits should be user-configurable. Decide whether
remote, family, bench, container, and park integrations deserve separate
changes after the local MVP is proven. Exact bench/type validation remains
existing-doctor follow-up work.

## Relationships

The [maintenance flow](project-maintenance-synthesis-inspect-and-retire.md)
connects this view to [batch cleanup](project-maintenance-batch-cleanup.md).
The [packet overview](project-maintenance-overview.md) defines the scope.
