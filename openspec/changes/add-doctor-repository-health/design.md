## Context

See proposal.md for motivation and the repository-health specification for the
observable contract. `project clean` already derives a local-ref worktree
report with classifications and recommendations; doctor currently prints only
the branch name and worktree paths, leaving that decision context separate.

## Goals / Non-Goals

**Goals:**

- Reuse the cleanup audit's evidence and recommendations without making doctor
  invoke a cleanup action.
- Make default-branch ahead/behind state prominent even though the default
  branch remains protected from cleanup.
- Keep human and JSON output aligned and let strict doctor treat unhealthy
  local repository states as warnings.

**Non-Goals:**

- Add a `cleanup` command alias or change `project clean` command semantics.
- Fetch remote refs, determine pull-request state, mutate Git state, or make
  a repository-health warning an ordinary doctor error.
- Replace the existing detailed `clean` plan or its explicit confirmation and
  revalidation gates.

## Decisions

1. **Build doctor health from the cleanup report.** Doctor will transform the
   existing `cleanup_report` data into a `repository_health` object rather than
   reimplementing Git state inspection. This keeps classifications and
   recommendations consistent between diagnosis and cleanup. An alternative
   independent inspection would risk two commands disagreeing about the same
   worktree.

2. **Add doctor-specific health status without changing cleanup classification.**
   Each row retains its cleanup `classification` and gains a `health_level` and
   `health_status`. A protected default with ahead/behind drift is therefore
   reported as `diverged-default` for doctor while remaining protected in
   cleanup. Changing the cleanup classifier's precedence would unnecessarily
   alter its action contract.

3. **Treat unavailable health as a warning payload.** `cleanup_report` can
   refuse when no local default can be established. Doctor catches only that
   diagnostic refusal, emits an unavailable health object and warning check,
   and continues with workflow, tooling, and validation checks. Git inspection
   failures remain described rather than hidden.

4. **Attach health to each complete snapshot.** Recursive project/family
   snapshots receive their own repository-health object; raw missing leg rows
   continue to use their existing missing-checkout diagnostics. This gives a
   family or nested project the same health contract as a directly inspected
   repository.

## Risks / Trade-offs

- [Local remote refs are stale] → State the no-fetch freshness boundary in both
  report forms and preserve the existing explicit cleanup revalidation.
- [The doctor output becomes more verbose] → Keep the new section compact,
  one line plus recommendation per worktree, and retain the existing summary.
- [A new warning changes strict-mode exit status] → Strict mode already treats
  warnings as failures; the new warnings accurately expose states that need
  human attention without changing ordinary doctor success.

## Migration Plan

Add focused disposable-repository tests for default divergence, linked
worktree warnings, and unavailable default detection. Update README guidance,
run the full suite inside py-bench, validate the change strictly, and roll back
with a normal code revert if needed.
