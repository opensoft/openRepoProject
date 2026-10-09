Lane: openRepoProject-1

# Tasks

This is the governance and handoff record only. The implementation tasks live
in the one Speckit feature named under "Speckit Handoff"; OpenSpec does not
duplicate them.

## 1. Governance record

- [x] 1.1 Proposal aligned: the alignment review's sixteen fixes (stack architect and QA lead) are applied to `proposal.md` (`6a93c8f`); verified by the alignment review comment on PR #15 (issuecomment-6072132040).
- [x] 1.2 Council resolved: thirteen concerns (product 4, architect 4, adversary 5); the VALID verdicts are applied to `proposal.md` and the NOTED ones recorded, none dismissed outright (`d13e419`); verified by that commit and by the council results comment on PR #15 (issuecomment-6072814758).
- [x] 1.3 Clarifications recorded: the six NOTED constraints, N1 to N6, are in `clarifications.md`; verified by `design.md`, which answers each with a named decision.
- [x] 1.4 Spec delta written: `specs/project-command/spec.md` modifies "Known Triad obstacles are named before the question and refused on a Triad answer", with its eight scenarios, one of them new; verified by `openspec validate fix-parent-obstacle-wording --strict` passing.
- [x] 1.5 Design written: `design.md`, decisions D1 to D6, with no open question that changes what is built; verified by `openspec status --change fix-parent-obstacle-wording --json` showing every artifact done.
- [ ] 1.6 Ratified by Brett Heap's word, quoted with its link on PR #15; verified by that quote. No implementation starts before it.

## 2. Speckit handoff

- [ ] 2.1 Exactly one Speckit feature owns the implementation: `specs/NNN-<slug>/`, created by `/speckit.specify` after 1.6 from a local main synced to origin/main, where NNN is the next number free that day (`001` and `002` exist, and lane openRepoProject-2's PRs #11 and #12 name `003` and `004`); verified when "Speckit Handoff" below names its feature identifier, branch and repo-relative `tasks.md` path, filled in once.
- [ ] 2.2 `/opsx:apply` is not run until "Speckit Handoff" names exactly one feature; verified by reading that section before the first `/opsx:apply`.

## 3. Landing and archive readiness

- [ ] 3.1 The realization PR is merged with green checks on all four CI jobs (`ubuntu-latest` and `macos-latest`, Python 3.10 and 3.12) and closes issue #14; verified by citing its merge sha here, from `gh pr view <number> --json mergeCommit,statusCheckRollup`.
- [ ] 3.2 If workBenches#145 is still open when the realization merges, one comment is posted on it naming the merge sha and the sha256 of `project` at that sha as an alternative pin target that carries the corrected sentence, and no new issue is opened (design D5); verified by the comment's URL, or, where nothing is posted, by #145's closed state at the merge.
- [ ] 3.3 The change is archived with `/opsx:archive` only after 3.1 and 3.2; verified by `openspec validate --all --strict` passing after the archive.

## Speckit Handoff

Implementation is tracked exclusively in one Speckit feature, to be created by
`/speckit.specify` after ratification. The feature covers the parent sentence
and its read (`design.md` D1 and D2) in `project`, the README sentence of D2,
and the tests of D3, and its spec carries the supersession statement of D4.

- Feature identifier: to be filled in once (`NNN-<slug>`, the next free number when `/speckit.specify` runs)
- Branch: to be filled in once
- Tasks: to be filled in once (`specs/NNN-<slug>/tasks.md`)

`/opsx:apply` is not run until this section names exactly one feature.
