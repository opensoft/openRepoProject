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
