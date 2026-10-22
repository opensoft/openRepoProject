Lane: openRepoProject-1

# Tasks

This is the governance and handoff record only. The implementation tasks live
in the one Speckit feature named under "Speckit Handoff"; OpenSpec does not
duplicate them.

## 1. Governance record

- [x] 1.1 Proposal aligned: the alignment review's findings (stack architect: 1 mismatch, 5 drifts; QA lead: 1 mismatch, 9 gaps) are applied to `proposal.md` (`f8a6df2`); verified by the alignment review comment on PR #21 (https://github.com/opensoft/openRepoProject/pull/21#issuecomment-6104257573).
- [x] 1.2 Council resolved: twelve concerns (product 4, architect 4, adversary 4); the seven VALID verdicts are applied to `proposal.md` (round 1 at `70d90e6`, round 2 at `d3b2ed1`), the NOTED ones recorded, and one dismissed; verified by those commits and by the council results comment on PR #21 (https://github.com/opensoft/openRepoProject/pull/21#issuecomment-6110918580).
- [x] 1.3 Clarifications recorded: the NOTED constraints, N1 to N6, are in `clarifications.md`; verified by `design.md`, which answers each with a named decision.
- [x] 1.4 Spec delta written: `specs/project-command/spec.md` adds "A parent blocked by a non-directory is refused before the single-repository path's steps", with ten scenarios, and modifies "Delegate project creation", "Creation question is asked only of a person choosing at the terminal", "Creation question offers the Triad first" and "Known Triad obstacles are named before the question and refused on a Triad answer", each as a full block changing only the statements this change makes false; verified by `openspec validate refuse-non-directory-parent-early --strict` passing.
- [x] 1.5 Design written: `design.md`, decisions D1 to D6, with no open question that changes what is built; verified by `openspec status --change refuse-non-directory-parent-early --json` showing every artifact done.
- [x] 1.6 Ratified by Brett Heap's word "ratify 21" (2026-10-21), quoted with its link on PR #21 (https://github.com/opensoft/openRepoProject/pull/21#issuecomment-6313890629); PR #21 landed by squash as b23333397f989462d13cf625c69e41bee8da8700 (of 8f3ca2d); verified by that quote. No implementation started before it.

## 2. Speckit handoff

- [x] 2.1 Exactly one Speckit feature owns the implementation: `specs/NNN-<slug>/`, created by `/speckit.specify` after 1.6 from a local main synced to origin/main, where NNN is the next number free that day (`001` to `003` exist; lane openRepoProject-2 holds `004`, `add-project-clean-all-safe`, in progress, and expects `005`, `add-project-overview`; no number is fixed here); verified when "Speckit Handoff" below names its feature identifier, branch and repo-relative `tasks.md` path, filled in once. Created: feature 006-refuse-non-directory-parent-early on branch 006-refuse-non-directory-parent-early (worktree ../openRepoProject-worktrees/006-refuse-non-directory-parent-early, cut from main at b233333; 006 was the next free number on 2026-10-21), spec at specs/006-refuse-non-directory-parent-early/spec.md.
- [x] 2.2 `/opsx:apply` is not run until "Speckit Handoff" names exactly one feature; verified by reading that section before the first `/opsx:apply`. Met: the handoff named feature 006-refuse-non-directory-parent-early at baea233 before the first implementation commit 7dcaf5f.

## 3. Landing and archive readiness

- [ ] 3.1 The realization PR, whose body says "Closes #20", is merged with green checks on every job of `.github/workflows/tests.yml` (since #32, two: `ubuntu-latest` on Python 3.10 and 3.12) and closes issue #20; verified by citing its merge sha here, from `gh pr view <number> --json mergeCommit,statusCheckRollup`.
- [ ] 3.2 If workBenches#145 is still open when the realization merges, one comment is posted on it naming the merge sha and the sha256 of `project` at that sha as an alternative pin target that carries the early refusal, and no new issue is opened (design D5); verified by the comment's URL, or, where nothing is posted, by #145's closed state at the merge.
- [ ] 3.3 The change is archived with `/opsx:archive` only after 3.1 and 3.2; verified by `openspec validate --all --strict` passing after the archive.

## Speckit Handoff

Implementation is tracked exclusively in one Speckit feature, created
by `/speckit.specify` after ratification. The feature covers the read and the
head refusal (`design.md` D1 and D2) in `project`, the README texts of D2, and
the tests of D3, and its spec carries the supersession statement of D4.

- Feature identifier: 006-refuse-non-directory-parent-early
- Branch: 006-refuse-non-directory-parent-early (worktree ../openRepoProject-worktrees/006-refuse-non-directory-parent-early, cut from main at b233333)
- Tasks: specs/006-refuse-non-directory-parent-early/tasks.md (created by /speckit.tasks)

`/opsx:apply` is not run until this section names exactly one feature.
