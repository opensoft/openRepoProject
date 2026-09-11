## Purpose

Keep project reports and owner-delegated maintenance safe when local metadata or
workBench configuration is incomplete, malformed, or contains private fields.

## ADDED Requirements

### Requirement: Reports expose only the portable profile schema

Status and doctor reports SHALL expose only `schema_version`, `bench`, `type`,
and `container` from a valid `.project.json` profile. Additional profile fields
MUST NOT be rendered in either human-readable or JSON output.

#### Scenario: Profile contains an unrecognized secret-like field

- **WHEN** a valid profile also contains an unrecognized `token` field
- **THEN** status and doctor reports omit that field while retaining supported
  profile data

### Requirement: Bench configuration errors are structured

Doctor and bench update SHALL validate the workBench registry and the selected
bench entry before accessing their fields. Malformed registry data MUST produce
a normal refusal with exit code 2, including JSON error output when requested.

#### Scenario: Selected bench entry is not a mapping

- **WHEN** the registry names a selected bench with a non-mapping value
- **THEN** doctor and bench update refuse without a traceback or delegated write

### Requirement: Parked-work inspection constrains repository identity

Before locating a parked-work record, status and doctor SHALL accept only a
valid GitHub `owner/repository` identity derived from the remote or manifest.
An invalid identity MUST NOT influence the local records path or cause unrelated
workspace files to be read.

#### Scenario: Remote contains a path-like owner

- **WHEN** a local remote contains an owner component such as `..`
- **THEN** the report states that no GitHub repository identity is available and
  does not inspect unrelated workspace records

### Requirement: Updates preserve estate and owner safeguards

Before applying a shape or bench update, the command SHALL refuse if any
declared child checkout is missing, dirty, detached, or not on its tracking
branch. Shape updates MUST retain the shape owner's confirmation interaction.

#### Scenario: A declared child checkout is missing

- **WHEN** an update targets a project with a declared leg that is absent
- **THEN** the command refuses before invoking an owner tool

#### Scenario: Shape update is requested without explicit confirmation

- **WHEN** a user applies a shape update without `--yes`
- **THEN** the delegated shape command retains its own confirmation prompt

### Requirement: Reports safely distinguish nested estates from project legs

Human-readable status and doctor reports SHALL recurse only into full nested
estate snapshots. A declared project leg represented by repository state SHALL
be rendered as a single leg row without requiring family-snapshot fields.

#### Scenario: Human-readable report includes a checked-out project leg

- **WHEN** a project manifest declares a present leg
- **THEN** status and doctor render the leg state without a traceback

### Requirement: YAML decoding errors are structured refusals

Every YAML input read by the command SHALL turn an invalid text encoding into a
normal refusal. JSON mode MUST preserve its structured error output and exit
code 2 rather than printing a traceback.

#### Scenario: Manifest is not valid UTF-8 text

- **WHEN** a project or family manifest contains invalid UTF-8 bytes
- **THEN** status refuses with structured JSON error output and no traceback
