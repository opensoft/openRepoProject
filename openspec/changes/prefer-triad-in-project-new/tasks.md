Lane: openRepoProject-1

# Tasks

This is the governance and handoff record only. The implementation tasks live
in the one Speckit feature named under "Speckit Handoff"; OpenSpec does not
duplicate them.

## 1. Governance record

- [x] 1.1 Proposal aligned: the alignment review's rulings R1 to R14 are applied to `proposal.md` (`7f7c91d`, wording pass `b8d566b`); verified by the resolution comment on PR #5 (issuecomment-6028469515).
- [x] 1.2 Council resolved: eleven VALID verdicts are applied to `proposal.md` and three are DISMISSED (`92e4d2c`); verified by the council resolution comment on PR #5 (issuecomment-6028843582).
- [x] 1.3 Clarifications recorded: the six NOTED constraints, N1 to N6, are in `clarifications.md`; verified by `design.md`, which answers each with a named decision.
- [x] 1.4 Spec delta written: `specs/project-command/spec.md` modifies "Delegate project creation" and adds six requirements; verified by `openspec validate prefer-triad-in-project-new --strict` passing.
- [x] 1.5 Design written: `design.md`, decisions D1 to D14, with no open question that changes what is built; verified by `openspec status --change prefer-triad-in-project-new --json` showing every artifact done.
- [ ] 1.6 Ratified by Brett Heap's word, quoted with its link on PR #5; verified by that quote. No implementation starts before it.

## 2. Speckit handoff

- [ ] 2.1 Exactly one Speckit feature owns the implementation: `specs/002-<slug>/`, to be created by `/speckit.specify` after 1.6 (numbering is sequential, and only `specs/001-project-command` exists); verified when "Speckit Handoff" below names its feature identifier, branch and repo-relative `tasks.md` path, filled in once.
- [ ] 2.2 `/opsx:apply` is not run until "Speckit Handoff" names exactly one feature; verified by reading that section before the first `/opsx:apply`.

## 3. Landing and archive readiness

- [ ] 3.1 The realization PR is merged with green checks on all four CI jobs (`ubuntu-latest` and `macos-latest`, Python 3.10 and 3.12) and closes issue #3; verified by citing its merge sha here, from `gh pr view <number> --json mergeCommit,statusCheckRollup`.
- [ ] 3.2 The merge sha is posted on issue #3 for codeXfactory-5's bookkeeping, with the link to the workBenches issue of 3.3 and the statement that `onp` and `new-project.sh` offer nothing until workBenches moves its pin; verified by the comment's URL.
- [ ] 3.3 Exactly one issue is opened on opensoft/workBenches, addressed to lane `project-command`, carrying the merge sha, the sha256 of `project` at that sha, and the optional "already offered" follow-up; verified by its URL, and by no file in that lane's claim having been edited.
- [ ] 3.4 openxFactory's task 5.6 box is checked by codeXfactory-5, never by this lane; verified by reading openxFactory's record of the tick, which cites the evidence of 3.1 to 3.3.
- [ ] 3.5 The change is archived with `/opsx:archive` only after 3.1 to 3.3; verified by `openspec validate --all --strict` passing after the archive.

## Speckit Handoff

Implementation is tracked exclusively in one Speckit feature, to be created by
`/speckit.specify` after ratification. The feature covers the creation
question, the known Triad obstacles, the organization and visibility prompts,
the creation advisory and its guarded write, the README and `AGENTS.md` text,
and the tests of `design.md` D14.

- Feature identifier: to be filled in once (`002-<slug>`, to be created by `/speckit.specify`)
- Branch: to be filled in once
- Tasks: to be filled in once (`specs/002-<slug>/tasks.md`)

`/opsx:apply` is not run until this section names exactly one feature.
