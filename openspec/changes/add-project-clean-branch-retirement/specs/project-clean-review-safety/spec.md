## MODIFIED Requirements

### Requirement: Cleanup states a narrow guarantee and its residual window

Concurrent writers (editors, other agents, other `project` invocations, and Git
commands run by anyone else) SHALL be outside the safe contract, and cleanup
SHALL claim no lock, lease or writer-quiescence handoff. Its one guarantee SHALL
be that a removal child is spawned only if, at the revalidation performed
immediately before spawning it, the repository identity, the target's worktree
identity and branch evidence, every baseline signature field of the target, its
`locked` flag, the absence of submodules and of hidden local state in its own
index (read inside the target worktree), the manifest's `tracking_branch`, and
the merge target's name, source and SHA all equal the values in the confirmed
plan. Under `--retire-branches` the guarantee SHALL extend to the branch child:
it is spawned only if the confirmed plan proved every commit that the branch's
reflog names an ancestor of the merge target's SHA, the rescan that proved the
removal re-established the repository identity, and, at the re-read performed
immediately before spawning it, the branch's head equals the reconciliation
record's `branch_sha`, its `upstream`, `upstream_oid`, `ahead` and `behind`, the
manifest's `tracking_branch`, and the merge target's name, source and SHA equal
the values in the confirmed plan, and no registered worktree had the branch
checked out at the rescan, as "Clean retires a removed worktree's branch only
on fresh head and ancestry evidence" states. Under `--retire-branches`, when a
target's revalidation takes its repository-wide values from the previous
target's rescan, those values SHALL be the ones read before that previous
target's branch stage, so that a change to them during that stage is outside
the contract for the target's removal; the target's branch evidence and the
merge target SHALL be compared again by its own re-read before any branch
child.

Ignored files created, and index flags set, after that revalidation, and any
change made after Git's own check, SHALL be outside the contract; the
confirmation and the result SHALL each state this residual window in one line.
Without `--retire-branches`, cleanup SHALL never delete a branch, so that a
branch race cannot lose commits: a branch change seen at revalidation SHALL
refuse the target with `branch-changed`, and one seen only by the rescan after
Git removed the worktree SHALL leave the target `removed` with
`branch-advanced-after-removal`, the branch present at a different SHA, or
`branch-missing-after-removal`, stop the run, and exit 2. Under
`--retire-branches` those outcomes SHALL hold unchanged and such a target's
branch SHALL never be deleted; a branch change seen by the re-read SHALL retain
the branch with `branch-changed`, stop the run, and exit 2; and a branch change
after that re-read SHALL be outside the contract, guarded only by Git's own
non-force check on the value Git reads, so that the residual-window line under
the flag SHALL also name a branch changed after its last check, after every
other clause the run's line names, those for a cache stage included when the
plan also selects a cache target, and before its last clause, any change after
Git's own check. A repository
found replaced by the rescan after a removal SHALL make that target `unknown`
with `unconfirmed-removal`, every reconciliation field null and `reconciled`
false, and SHALL stop the run with exit status 1.

#### Scenario: Ignored file in the residual window

- **WHEN** a test hook creates an ignored file in a target after its
  revalidation and before its removal child starts
- **THEN** Git removes the worktree with exit 0, the target is `removed`, the
  file is gone, and the result text carries the residual-window line, which the
  confirmation also carried; this documents the boundary rather than a guarantee

#### Scenario: Branch advances after removal

- **WHEN** a test hook advances a target's branch after Git removed the worktree
  and before the rescan
- **THEN** the target is `removed` with `branch-advanced-after-removal`, its
  reconciliation has `registry_entry_present: false`, `path_present: false`,
  `branch_present: true` and a `branch_sha` that differs from `planned_sha`,
  later targets are `not-attempted`, no commit is lost, and the exit status is 2
- **AND** a hook that deletes the branch instead yields
  `branch-missing-after-removal` with `branch_present: false` and exit 2

#### Scenario: Repository replaced mid-batch

- **WHEN** in a three-target plan, after the first target's removal child exits
  0 and before the rescan that follows it, the repository root is renamed and
  another clone is moved into its path, or the root's parent directory is
  replaced by a symlink to a copy
- **THEN** the rescan's identity probe finds a different repository, the first
  target is `unknown` with `unconfirmed-removal`, every reconciliation field
  null and `reconciled: false`, the second and third are `not-attempted` with
  `batch-stopped`, and the exit status is 1
- **AND** when the same replacement happens before the first target's
  revalidation, the first target is `refused` with `identity-changed`, the later
  targets are `not-attempted`, nothing is removed, and the exit status is 2

#### Scenario: A branch changed after the re-read meets Git's own check

- **WHEN** under `--retire-branches` a test hook moves a target's branch to a
  new commit, merged into neither the merge target nor the branch's upstream,
  after the target's re-read and before its branch child starts
- **THEN** Git's own check refuses the deletion with exit status 1, the branch
  survives at the new commit, the target's `branch_retirement` is `retained`
  with `git-refused`, later targets are `not-attempted`, no commit is lost, and
  the exit status is 2
- **AND** the confirmation and the result carry the residual-window line, which
  under the flag reads `Not protected: ignored files created or index flags set
  after the last check, a branch changed after its last check, and any change
  after Git's own check.`
