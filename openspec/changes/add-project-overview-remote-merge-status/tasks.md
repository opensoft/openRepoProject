Lane: openRepoProject-5

# Tasks

This is the governance and handoff record only. The implementation tasks live
in the one Speckit feature named under "Speckit Handoff"; OpenSpec does not
duplicate them.

## 1. Governance record

- [x] 1.1 Proposal written: `proposal.md` adopts the packet's deferred remote boundary (DI:1036-1060) for `project overview --remote` under the lane's rulings L-1 to L-9 and C-1 to C-8, with "Decisions Taken by This Proposal", "Corrections to the Packet" (none) and three Open Questions, the third addressed to lane openRepoProject-4; verified by its Capabilities section accounting for all twelve of change 2's `project-overview` requirements.
- [ ] 1.2 Alignment resolved: the stack-architect and qa-lead findings are applied or ruled, MISMATCH and DRIFT fixed and each GAP put to Brett Heap; verified by the table "Questions Resolved by the Alignment Review" in `proposal.md` and the later-rulings list under it.
- [ ] 1.3 Council resolved: the product-advocate, systems-architect and adversary-engineer concerns are ruled VALID, NOTED or DISMISSED, the VALID ones applied to `proposal.md` and the NOTED ones recorded in `clarifications.md`; verified by "Council Verdicts" in `proposal.md` and by `design.md`, which answers each NOTED item with a named decision.
- [x] 1.4 Spec deltas and design written: `specs/project-overview/spec.md` modifies "Overview is local and read-only" (2 scenarios: change 2's one, kept verbatim, and one added) and adds "Overview reports remote merge evidence on request" (11 scenarios), 13 scenarios in all; `design.md` holds D1 to D11; the delta is committed after lane openRepoProject-4 has read its two headers and the MODIFIED block's difference from change 2's text; verified by `/usr/bin/openspec status --change add-project-overview-remote-merge-status --json` showing every artifact done.
- [x] 1.5 Validation passes: `/usr/bin/openspec validate add-project-overview-remote-merge-status --strict` reports the change valid, its one INFO line (archive needs a `project-overview` spec) expected while change 2 is unarchived; `/usr/bin/openspec validate --all --strict` passes every item; and `/usr/bin/openspec status --change add-project-overview-remote-merge-status --json` shows every artifact done; verified by running the three commands on this branch after 1.4.
- [ ] 1.6 Ratified by Brett Heap's word on the pull request for this change, quoted with its link here; verified by that quote. No implementation starts before it.

## 2. Before the Speckit handoff

- [ ] 2.1 Feature 005 (`005-project-overview`, change 2's) has merged to `main`; verified by its merge sha cited here. Feature 005 is specified from change 2 as ratified, with no `--remote`, and nothing of it is changed for this change.
- [ ] 2.2 Change 2, `add-project-overview` (issue #10), is archived, after change 1's archive and feature 005's merge, so that `openspec/specs/project-overview/spec.md` holds "Overview is local and read-only"; verified by that file and by `/usr/bin/openspec validate add-project-overview-remote-merge-status --strict` passing without the INFO line that archive needs a `project-overview` spec.
- [ ] 2.3 This change's MODIFIED block re-read against the archived "Overview is local and read-only" and its ADDED requirement against the archived `project-overview` requirements it cites; any sentence that moved is re-aligned by a follow-up commit, and any sentence lane openRepoProject-4 asked for is in; verified by `diff -u` of the archived block against this change's MODIFIED block showing additions only, and by the validation of 1.5 passing again.

## 3. Landing and archive readiness

- [ ] 3.1 Exactly one Speckit feature owns the implementation: `specs/NNN-<slug>/`, created by `/speckit.specify` after 1.6 and section 2, from a local `main` synced to `origin/main`, where NNN is the next number free that day (006 or later); verified when "Speckit Handoff" below names its feature identifier, branch and repo-relative `tasks.md` path, filled in once.
- [ ] 3.2 `/opsx:apply` is not run until "Speckit Handoff" names exactly one feature; verified by reading that section before the first `/opsx:apply`.
- [ ] 3.3 The realization PR is merged with green checks on both CI jobs of the `tests` workflow, `test (3.10)` and `test (3.12)` on `ubuntu-latest` (Linux only since PR #32, `.github/workflows/tests.yml` at `origin/main`), and closes issue #25; verified by citing its merge sha here, from `gh pr view <number> --json mergeCommit,statusCheckRollup`.
- [ ] 3.4 The change is archived with `/opsx:archive` only after 3.3 and after change 2's archive (2.2); verified by `/usr/bin/openspec validate --all --strict` passing after the archive.

## Speckit Handoff

Implementation is tracked exclusively in one Speckit feature, created by
`/speckit.specify` after ratification (1.6) and after section 2. The feature
covers `project overview --remote` as `specs/project-overview/spec.md`
defines it, the README paragraph of `proposal.md`'s Impact and the tests of
`design.md` D11.

- Feature identifier: to be created by /speckit.specify after 1.6 (006 or the next free number)
- Branch: to be created by /speckit.specify after 1.6 (006 or the next free number)
- Tasks: to be created by /speckit.specify after 1.6 (006 or the next free number), at specs/<feature identifier>/tasks.md

`/opsx:apply` is not run until this section names exactly one feature.
