Lane: openRepoProject-4

# Tasks

This is the governance and handoff record only. The implementation tasks live
in the one Speckit feature named under "Speckit Handoff"; OpenSpec does not
duplicate them.

This change archives after `refuse-non-directory-parent-early` (#21), whose
delta its two MODIFIED blocks are written against, and its realization lands
after #21's realization, merging main in first (issue #22; design D6 and D7).

## 1. Governance record

- [x] 1.1 Proposal aligned: the alignment review of `0096c98` (stack architect SA-1 to SA-11, QA lead QA-1 to QA-9; 2 BLOCKER, 9 MAJOR, 9 MINOR) is applied to `proposal.md` (`461a010`); verified by the proposal's "Review resolution", which records each item, and by the alignment review comment on PR #28 (https://github.com/opensoft/openRepoProject/pull/28#issuecomment-6257808062; the lead relayed the review when it was made, on 2026-10-11, and it was posted late).
- [x] 1.2 Council resolved: nineteen concerns (product-advocate 5, systems-architect 7, adversary-engineer 7); the seven VALID verdicts are applied to `proposal.md` (PO-5 and AR-6 at `4318638`, the rest at `5bde39b`), the twelve NOTED ones recorded, none dismissed; verified by those commits and by the council results comment on PR #28 (https://github.com/opensoft/openRepoProject/pull/28#issuecomment-6254996548).
- [x] 1.3 Clarifications recorded: the NOTED constraints, N1 to N12, are in `clarifications.md`; verified by `design.md`, which answers each with a named decision.
- [x] 1.4 Spec delta written: `specs/project-command/spec.md` adds "Supported Python versions are stated and tested" (three scenarios), "A parent that is a symbolic-link loop is refused before the question" (eight) and "A destination that cannot be read is refused before the question" (eleven), and modifies "Creation question is asked only of a person choosing at the terminal" and #21's ADDED "A parent blocked by a non-directory is refused before the single-repository path's steps", each as a full block of #21's delta text at `8f3ca2d` changing only the statements this change makes false; verified by `openspec validate support-later-python-versions --strict` passing.
- [x] 1.5 Design written: `design.md`, decisions D1 to D10, with no open question that changes what `project` or the tests do; verified by `openspec status --change support-later-python-versions --json` showing every artifact done.
- [x] 1.6 Ratified by Brett Heap's word ratifying #28 (such as "ratify 28"), quoted with its link on PR #28, with Decisions 3 and 12 answered or left as recorded; PR #28 lands by squash; verified by that quote. No implementation starts before it. If Decision 12 takes the alternative, the second MODIFIED block and design D4's README replacement are dropped before PR #28 lands (design D6). Done 2026-10-21: "ratify 28, recommended for SA-2 and SA-7", quoted at https://github.com/opensoft/openRepoProject/pull/28#issuecomment-6315794017; Decision 3 A1, Decision 12 the recommendation; it lands by squash.

## 2. Speckit handoff

- [ ] 2.1 Exactly one Speckit feature owns the implementation: `specs/NNN-<slug>/`, created by `/speckit.specify` after 1.6 from a local main synced to origin/main, where NNN is the next number free that day (`001` to `003` exist on main; lane openRepoProject-2 holds `004`, `add-project-clean-all-safe`, and `005`, `add-project-overview`, in progress; #21's realization takes its own; no number is fixed here); verified when "Speckit Handoff" below names its feature identifier, branch and repo-relative `tasks.md` path, filled in once.
- [ ] 2.2 `/opsx:apply` is not run until "Speckit Handoff" names exactly one feature; verified by reading that section before the first `/opsx:apply`.

## 3. Landing and archive readiness

- [ ] 3.1 The realization PR, whose body says "Closes #22", is merged after #21's realization has landed on main and after merging main in, with green checks on all six `test` jobs (`ubuntu-latest`, Python 3.10, 3.11, 3.12, 3.13, 3.14 and 3.15) and on every other job on main then, and it closes issue #22; verified by citing its merge sha here, from `gh pr view <number> --json mergeCommit,statusCheckRollup`, with #21's realization merge sha shown to be its ancestor (`git merge-base --is-ancestor`), each `test` job's resolved Python version from setup-python's log, the 3.15 job's pip log for PyYAML (built from source while no `cp315` wheel exists), and the `-v` output showing no test of the new module skipped.
- [ ] 3.2 If workBenches#145 is still open when the realization merges, one comment is posted on it naming the merge sha and the sha256 of `project` at that sha as an alternative pin target, and no new issue is opened (design D9); verified by the comment's URL, or, where nothing is posted, by #145's closed state at the merge.
- [ ] 3.3 The archive order holds (clarifications N5, design D6): before `/opsx:archive` runs here, `refuse-non-directory-parent-early` is under `openspec/changes/archive/` on main, `openspec validate support-later-python-versions --strict` prints no "Archive would refuse" line, and each MODIFIED block's base text equals main's requirement text, or the block is first rewritten against main; verified by quoting those outputs here.
- [ ] 3.4 The change is archived with `/opsx:archive` only after 3.1, 3.2 and 3.3; verified by `openspec validate --all --strict` passing after the archive.

## Speckit Handoff

Implementation is tracked exclusively in one Speckit feature, to be created
by `/speckit.specify` after ratification. The feature covers the supported
range in `.github/workflows/tests.yml` and `README.md` (`design.md` D1), S1
and S2 in `project` (D2 and D3), the README texts of D4, and the test module
of D5, and its spec carries the supersession statement of D8.

- Feature identifier: to be created by `/speckit.specify` after ratification (the next free number that day)
- Branch: to be created with the feature
- Tasks: `specs/<feature>/tasks.md` (to be created by `/speckit.tasks`)

`/opsx:apply` is not run until this section names exactly one feature.
