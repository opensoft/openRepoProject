## Context

See proposal.md. The command is intentionally local-first, delegates shape and
bench ownership, and now needs the review findings fixed without turning a
diagnostic command into a source of data loss or arbitrary configuration errors.

## Goals / Non-Goals

**Goals:**

- Fail closed before deleting ignored work, guessing a default branch, or
  applying changed cleanup state.
- Normalize untrusted local configuration at the existing command boundary.
- Preserve the owning shape tool's authority over its confirmation prompt.

**Non-Goals:**

- Fetch remote state, resolve divergent branches, or change PR/merge policy.
- Interpret unknown profile fields as configuration; they remain private data.
- Change Speckit hook behavior or invent project governance beyond the current
  review findings.

## Decisions

1. **Filter rather than reject unknown profile fields.** The profile reader will
   return only the documented schema keys. This prevents report leakage while
   remaining forward-compatible with private workstation metadata. Rejecting an
   otherwise valid profile would make existing projects unusable for a field
   that this command does not own.

2. **Validate registry structure once at every consumer boundary.** A helper
   will return a validated benches mapping and validate the selected entry and
   generator rows before doctor or update use them. Reusing the full generator
   listing would change error selection and path handling, so consumers retain
   their purpose-specific logic after shared structural validation.

3. **Constrain parked-work identity before path construction.** Remote and
   manifest identities must match GitHub owner/repository syntax before their
   owner portion names a workspace directory. Treat an invalid value as unknown
   identity rather than an exceptional filesystem condition.

4. **Fail closed in cleanup.** A worktree records tracked changes and ignored
   files separately; ignored files block removal but do not redefine ordinary
   status output. Default branch selection has no current-branch fallback.
   Ahead-and-behind state is a distinct divergent classification. A second
   cleanup report after confirmation must agree with the selected action's
   safety evidence.

5. **Shape confirmation belongs to openRepoShape.** The coordinator runs the
   owner check, then invokes owner apply without synthesizing `--yes` or an
   additional coordinator prompt. This retains the owner's wording and
   interaction contract.

6. **Normalize child state for update safety.** A small recursive iterator
   yields repository state from project legs and family-member snapshots so the
   same guard can reject missing, dirty, detached, or feature state.

7. **Distinguish a full estate snapshot from shallow leg state.** Only a child
   with both a manifest kind and repository snapshot can recurse in human or
   validation reports; a project leg remains a one-line repository state.

8. **Treat invalid YAML text as invalid YAML input.** The YAML reader catches
   decoding errors alongside filesystem and parser errors so normal CLI error
   formatting remains the sole error path.

9. **Match registered Claude commands to local skill bundles.** The Git
   extension's `claude` registry lists commands invoked by core/hook workflows;
   each name maps from dots to hyphens to a committed `.claude/skills` bundle.

## Risks / Trade-offs

- [Ignored generated files block a cleanup] → Preservation is preferable; a
  user can remove or relocate the files deliberately before retrying.
- [No local default-branch evidence] → Refusal requires a manifest tracking
  branch or conventional/remote default configuration, preventing accidental
  deletion in atypical repositories.
- [Second inspection sees concurrent changes] → The command refuses instead of
  applying an action that no longer matches the displayed plan.
- [A generated skill bundle drifts from its source] → Copy the matching
  user-global Claude bundle and verify every registered command has a local
  `SKILL.md`.

## Migration Plan

Add regression tests with disposable repositories and registries, run the full
suite, then push the review-fix commit to the existing PR. Rollback is a normal
revert; no cleanup action is performed during this remediation.
