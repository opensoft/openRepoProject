## Purpose

Provide a single discoverable command for project creation, local inspection,
readiness diagnosis and explicit maintenance across the OpenSoft tool repositories.

## ADDED Requirements

### Requirement: Delegate project creation
The command SHALL list usable generators, accept a name and parent, present a
plan, preserve generator failures, and refuse an existing destination. Shape
creation SHALL require explicit organization and visibility and retain owner prompts.

#### Scenario: Preview
- **WHEN** creation is requested with --dry-run
- **THEN** the command prints the selected generator and destination without writes.

#### Scenario: Existing project
- **WHEN** the destination already exists
- **THEN** the command refuses before running the generator.

### Requirement: Inspect and diagnose
Status and doctor SHALL support human and JSON reports for single repositories,
project manifests, families, worktrees and local tooling. Missing or malformed
state SHALL be visible; inspection SHALL never fetch, reset, or bootstrap.

#### Scenario: Missing leg
- **WHEN** a project's declared leg has no checkout
- **THEN** doctor reports an actionable failure and returns nonzero.

### Requirement: Explicit maintenance
Update SHALL report local tracking state and named owning commands by default.
Applying an update SHALL require a component and confirmation, preserve failures,
and reject dirty project state for project-modifying delegates.

#### Scenario: Default report
- **WHEN** update is run without --apply
- **THEN** it reports a plan without modifying repositories or installing software.

### Requirement: Distribution and compatibility
workBenches SHALL install a verified project artifact and retain onp and
new-project.sh as forwarding entrypoints accepting the old name/parent arguments.

#### Scenario: Failed download
- **WHEN** installation cannot obtain or verify the artifact
- **THEN** an existing project command remains unchanged.
