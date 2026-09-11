## Purpose

Make cleanup and doctor distinguish genuinely unmerged feature work from a
feature that the last-fetched remote target already contains but local Git has
not yet reconciled.

## ADDED Requirements

### Requirement: Cleanup reports local, remote-target, and GitHub merge evidence

For every named feature worktree, `project clean` SHALL compare its head with
the local cleanup target and, when available, that target branch's configured
remote-tracking ref. When neither ancestry comparison establishes a merge and
the target identifies a GitHub repository, it SHALL inspect GitHub pull-request
state for the exact feature head. It SHALL expose the evidence and its source
in JSON, label Git ref evidence as current only as of the last fetch, and MUST
NOT fetch, merge, or mutate repository state during an audit.

#### Scenario: Feature is merged on the tracked remote target only

- **WHEN** a feature head is not contained by the local target branch but is
  contained by the target's configured remote-tracking ref
- **THEN** cleanup and doctor report that it is merged remotely and awaiting
  local target reconciliation

#### Scenario: Feature was squash-merged on GitHub

- **WHEN** neither local nor remote target ancestry contains a feature head but
  GitHub reports a merged pull request for that exact head
- **THEN** cleanup and doctor report that it is merged on GitHub and awaiting
  local target reconciliation rather than calling it unmerged

#### Scenario: Feature is not merged in either available target

- **WHEN** a feature head is contained by neither the local target branch nor
  its available remote-tracking ref and GitHub reports no merged pull request
  for that exact head
- **THEN** cleanup reports it as not merged and directs the user to the normal
  review or merge process without describing the state as only local

### Requirement: Unknown remote merge evidence remains explicit and safe

When cleanup cannot establish remote merge evidence from either a
remote-tracking target or a GitHub exact-head lookup, it SHALL report the
remote merge state as unknown and preserve the worktree. Remote-only merge
evidence MUST NOT make a worktree eligible for removal; confirmed removal
SHALL continue to require verified local target ancestry.

#### Scenario: Remote target evidence is unavailable

- **WHEN** the local target has no usable remote-tracking ref and GitHub
  merge state cannot be established
- **THEN** cleanup reports that remote merge status is unavailable and proposes
  no destructive cleanup action based on the unknown state
