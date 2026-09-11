Lane: project-command

CLAIMED — lane project-command for the CLI and workBenches migration. Sibling
search found no existing openRepoProject issues, PRs, or feature branches;
workBenches project search found no competing CLI migration.

## Why

The generic workBenches creation script resolves registry paths against the
wrong directory and mixes update scripts into its creation menu. Developers
also need one command to inspect project readiness and coordinate updates.

## What Changes

- Introduce project new, status, doctor, update, and benches.
- Keep name/parent positional compatibility through onp and new-project.sh.
- Delegate generators, shape creation/updates and workflow bootstrap.
- Install project through workBenches using a pinned source artifact.

## Capabilities

### New Capabilities

- project-command: guided creation, read-only reporting and explicit updates.

### Modified Capabilities

None.

## Impact

openRepoProject owns the executable and tests; workBenches gains installation
and compatibility wrappers. Bench generators and openRepoTools stay authoritative.
The user's implementation request authorizes this scope. Implementation tasks
belong to the Speckit feature, not a second list here.
