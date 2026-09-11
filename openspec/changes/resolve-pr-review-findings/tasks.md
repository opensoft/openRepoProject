## 1. Report and update safety

- [x] 1.1 Filter profile output to the public schema fields and add JSON report regression coverage for an extra secret-like field.
- [x] 1.2 Add validated workBench registry access for doctor and bench update, with malformed mapping/list tests that assert structured refusal.
- [x] 1.3 Refuse unsafe or missing project/family children before shape or bench updates, and retain openRepoShape's own confirmation interaction; verify delegated arguments and refusal paths.
- [x] 1.4 Constrain remote/manifest GitHub identities before parked-work record lookup; verify crafted owner paths cannot read unrelated workspace records.
- [x] 1.5 Safely distinguish full nested snapshots from shallow project-leg state in human-readable reports; verify a present leg renders without a traceback.
- [x] 1.6 Convert invalid YAML text encodings into structured refusals; verify JSON output and exit status.
- [x] 1.7 Install and verify the Claude skill bundles for every Git extension command registered for Claude.

## 2. Cleanup safety

- [x] 2.1 Detect ignored files separately from normal status and make them block worktree removal; verify a disposable ignored file survives a refused cleanup.
- [x] 2.2 Fail closed without a determinable default branch, classify divergent/behind upstream state for review, and support differently named configured upstreams; verify each with disposable Git repositories.
- [x] 2.3 Revalidate the selected action after confirmation and before execution; verify changed worktree state refuses without removal.

## 3. Review closure

- [x] 3.1 Run the complete test suite, diff checks, OpenSpec validation, and focused cleanup smoke audit; record evidence for each current Copilot thread and identify any stale thread.
- [x] 3.2 Push the reviewed remediation to the existing PR and resolve or reply to each current Copilot thread with the corresponding test evidence.
- [x] 3.3 Run the full verification set, push this follow-up, and resolve or reply to every new review thread with evidence.
