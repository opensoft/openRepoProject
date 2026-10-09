# Agent Instructions

<!-- OPENSPEC-SPECKIT-GLOBAL:START -->
## Shared OpenSpec/Speckit Protocol

This repo uses the user-global OpenSpec/Speckit workflow instead of duplicating
process rules in every repository.

- Global agent entrypoint: `${AGENT_PROTOCOL_ROOT:-$HOME/.agents}/AGENTS.md`
- Workflow protocol: `${AGENT_PROTOCOL_ROOT:-$HOME/.agents}/protocols/openspec-speckit-workflow.md`
- Bootstrap contract: `${AGENT_PROTOCOL_ROOT:-$HOME/.agents}/protocols/project-agent-bootstrap.md`

Repo-local sections below remain authoritative for project-specific commands,
runtime prerequisites, source-of-truth docs, tests, and deployment constraints.
<!-- OPENSPEC-SPECKIT-GLOBAL:END -->

## Runtime and verification

The CLI is the executable `project`, Python 3.10+. PyYAML is needed for YAML
manifests. Run `python3 -m unittest discover -s tests -v` in the Python workBench
(`py-bench` in workBenches), with the checkout in the bench's projects mount.
Use temporary fixtures for creation tests; do not create real GitHub projects.
Generic orchestration belongs here; generators, shape mechanics and Git handoff
stay with their existing owners. See docs/migration-review.md.

## Creating a project for a person

When a person asks to create a new project, offer the Triad first as the
default, in conversation, as the shared protocol says: an assembly root with a
spec leg and a code leg, preferred, not required, elective, and conferring
nothing; accept a single repository without asking why. Then run `project new`
with a choosing flag: `--shape --org ORG --visibility VIS` for a Triad, or
`--bench BENCH --type TYPE` for a single repository. Never answer the creation
question, the organization, the visibility or openRepoShape's typed
confirmation on a person's behalf. The terminal check cannot tell an agent at a
pseudo-terminal from a person.
