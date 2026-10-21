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

The CLI is the executable `project`, Python 3.10+, with Git 2.36 or later
wherever it inspects a repository (`project clean` refuses an older Git).
PyYAML is needed for YAML manifests. Run `python3 -m unittest discover -s tests -v`
in the Python workBench (`py-bench` in workBenches), with the checkout in the
bench's projects mount. Use temporary fixtures for creation tests; do not
create real GitHub projects.

The `clean` tests are the modules `tests/test_clean_*.py` and
`tests/test_status_doctor_update.py` (which also covers `status`, `doctor` and
`update`), with their helpers in `tests/clean_support.py` (import it by its bare
name) and the launcher `tests/launch_project.py`, which runs `project` with a
test's own timing table and never reads a time from the environment. Run them
alone with
`python3 -m unittest discover -s tests -v -k test_clean_ -k test_status_`:
unittest matches `-k` against `module.Class.method`, so those two prefixes take
every such module whole, and a new module must be named `test_clean_*` or
`test_status_*` to be taken.

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

## Cleaning up worktrees for a person

When a person asks to clean up or retire worktrees, preview first and show it:
`project clean ROOT --all-safe` changes nothing and lists what a batch would
remove and each excluded worktree with its reason and next step. Apply only
that plan, with `project clean ROOT --all-safe --apply --expect-plan DIGEST`,
DIGEST being the `plan_digest` that `project clean ROOT --all-safe --json`
printed for the same preview (the human preview does not print it), so a plan
that changed since the person looked is refused. Never answer the removal
question, or pass `--yes`, on a person's behalf unless they asked for that run;
otherwise give them the command to run at their own terminal. Ask that sessions
in the selected worktrees be closed first: `clean` cannot see them, and a
session left open can find its worktree removed. After a stopped batch, show the
stop block and run its `Next:` command, which is a preview, never the forced
removal a partial-removal note names.
