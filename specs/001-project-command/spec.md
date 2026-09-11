# Feature Specification: Project command

Branch: 001-project-command. Status: implementation authorized by user.

## User Scenarios & Testing

### Create a project (P1)

Given a registry containing installed and unavailable generators, a user can
list choices, select one by type or description, preview NAME/PARENT, confirm,
and run it. Existing destinations refuse and failures retain their exit code.
Legacy name/parent invocations through workBenches reach the same flow.

### Understand a project (P1)

From a repository, nested directory, feature worktree, named project or family,
status reports roots, legs, Git state, worktrees and declared environment.
Doctor reports missing checkouts/tools and supports optional owner validation.
Both have JSON output and perform no fetch/reset/bootstrap.

### Maintain a project (P2)

Update without apply prints the owner commands and local tracking status.
Explicit component selection plus confirmation invokes the owner. Dirty or
feature-branch state refuses shape/bench updates. Failed owners stay failed.

### Edge cases

Spaces in paths, missing runtime, invalid JSON/YAML, escaped registry paths,
ambiguous type/description, missing submodules, family cycles, missing upstream,
noninteractive stdin, symlink install targets and failed downloads.

## Requirements

FR-001: implement new, status, doctor, update and benches with contextual help.
FR-002: delegate generators and shape operations, preserving argv and exit status.
FR-003: use registry paths relative to workBenches; exclude updater entries.
FR-004: no writes during dry-run or default reporting; no secret values reported.
FR-005: retain old positional name/parent interface via forwarding scripts.
FR-006: install a checksum-verified executable atomically from workBenches.
FR-007: support .project.json schema_version 1 with bench and container fields.

## Success Criteria

Offline fixture tests exercise every command, legacy forwarding, installer
failure preservation and creation failure paths. A fresh install prints help
and discovers the configured workBenches registry from a different directory.

## Assumptions

Python 3.10+ is available; PyYAML is required only for YAML estate inspection.
Technology runtimes and generators remain bench-owned. Shape mode scaffolds
repositories; combining it with an application generator requires a future
adapter contract. Descriptions are matched locally and never uploaded.
