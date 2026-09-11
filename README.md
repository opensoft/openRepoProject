# openRepoProject

The `project` command creates, inspects, diagnoses and maintains projects using
[openRepoShape](https://github.com/opensoft/openRepoShape),
[openRepoTools](https://github.com/opensoft/openRepoTools), and
[workBenches](https://github.com/opensoft/workBenches).

## Install

workBenches installs the executable from an exact commit, verified by SHA-256:

```sh
python3 scripts/setup-project-command.py    # from workBenches
project --help
```

It also runs during workBenches setup and command installation. Python 3.10+
is required. YAML project/family/workspace inspection requires PyYAML (available
in the development bench); other commands use Python's standard library.
For source development, run `python3 project --help` in this checkout.

## Create a project

```sh
project benches
project new
project new MyApp --bench flutterBench --type flutter --dry-run
project new MyApp ~/projects --bench flutterBench --type flutter --workflow
project new MyApp --description "a Flutter mobile app" --dry-run
```

The registry is `workBenches/config/bench-config.json`. Paths are relative to
that checkout. The list reports missing scripts and excludes updater entries.
Descriptions produce local keyword recommendations; they are never uploaded.
Ambiguous choices require an explicit selection.

Before running, the command shows the generator and destination and asks for
`yes`. `--yes` confirms bench creation for scripted use. `--dry-run` prints the
plan without creating even the parent directory. Existing destinations refuse.
Generator errors pass through unchanged. The generator owns language runtime
requirements and environment creation: run it in the appropriate bench.

`--workflow` runs `setup-openspeckit --repo PATH` after successful creation.
A small `.project.json` records the selected bench/type for later inspection.

Shape scaffolding delegates directly to openRepoShape:

```sh
project new Atlas --shape --org example --visibility private --into ~/projects
project new Atlas --shape --org example --visibility public --family Products --dry-run
```

Shape mode retains openRepoShape's own confirmation prompts even when `--yes`
is supplied here. It can pass `--family` and `--elected-by`. Its output names any
remaining family-membership step. Shape mode creates the repository structure;
combining it with a bench application generator requires a future adapter.

Legacy `onp NAME [PARENT]` and `new-project.sh NAME [PARENT]` in workBenches
forward to `project new` and also accept its new flags.

## Understand a project

```sh
project status
project status Atlas --json
project doctor /path/to/Atlas
project doctor --validate
project doctor --strict --json
```

Targets may be paths or names under `PROJECTS_DIR` (otherwise `~/projects`
or `~/Projects`). From a nested directory, the nearest estate manifest wins.
A family folder resolves to its holder. Family reports inspect working siblings;
project reports inspect declared legs. Single-repository feature worktrees are
reported as their own checkouts, along with the owning repository's worktree list.

Status shows Git branches, dirty state, local tracking differences, worktrees,
the declared bench/container, and matching local parked-work records.
Doctor adds missing-checkout/tooling findings, workflow readiness and credential
configuration presence. No credential values are read or printed; presence does
not prove a working login.

Default inspection does not fetch, pull, reset, install, or bootstrap.
Tracking and handoff information are explicitly local and may be stale.
`doctor --validate` additionally runs project-owned validators; those validators
can access upstream and their output is preserved. Pin correctness is delegated
to them and is not implied by a normal status report.

## Clean up Git worktrees

```sh
project clean
project clean /path/to/project --json
project clean --apply --action push --branch 001-feature --yes
project clean --apply --action remove --worktree /path/to/feature-tree --yes
project clean --apply --action delete-branch --branch 001-feature --yes
```

`clean` is read-only by default. It inspects all linked worktrees using local
refs and labels remote comparisons as of the last fetch. It protects the
default branch and preserves dirty, detached, unpublished, remote-gone and
unmerged work. A pushed-but-unmerged branch is handed off to the repository's
normal pull-request or merge process.

Apply actions are always explicit and target one branch or worktree. Pushes
are normal non-force pushes. A worktree can be removed only when it is clean,
non-current and verified merged into the local default branch; deleting its
local branch is a separate action. `clean` never fetches, stashes, resets,
force-pushes, creates or merges pull requests, or replaces `park`/`resume`.

A portable profile may declare:

```json
{
  "schema_version": 1,
  "bench": "flutterBench",
  "type": "flutter",
  "container": "flutter-bench"
}
```

Container state is queried only for an explicitly declared container. Missing
profile data is reported as unknown. Profiles contain no credentials or host paths.

## Coordinate updates

```sh
project update Atlas
project update Atlas --json
project update Atlas --apply --component workflow --dry-run
project update Atlas --apply --component workflow
project update MyApp --apply --component bench
project update Atlas --apply --component shape --shape-source ../openRepoShape --at FULL_COMMIT_SHA
project update Atlas --apply --component tools
```

The default report shows local tracking state and maintenance owners; it does
not check remote versions or apply anything. `--apply` requires a component and
shows the commands before confirmation. `--dry-run` never executes the plan.

- `workflow`: invokes setup-openspeckit for the selected root.
- `shape`: runs update-shape check, shows its per-file findings, then confirms
  apply at an explicit commit on a shape update branch. Owner refusals remain.
- `bench`: invokes the exact registered update-TYPE script for the profile,
  passing the selected root. Missing adapters refuse.
- `tools`: opens workBenches setup, with its own installation choices/prompts.

Shape and bench changes require clean tracking checkouts and preserve feature
branches. Existing owner tools retain their own prompts and behavior.
No component silently pulls Git branches or implements pin/worktree mechanics.

## Configuration

| Setting | Purpose |
| --- | --- |
| `--workbenches PATH` / `WORKBENCHES_ROOT` | Explicit bench registry checkout |
| `PROJECTS_DIR` | Projects directory for discovery and default creation |
| `.project.json` | Portable project bench/type/container declarations |
| `~/.agents/workspace.yaml` | Existing park/resume workspace config, read-only here |
| `SPECKIT_WORKSPACE_PATH` | Override the local parked-work workspace path |
| `OPENREPOPROJECT_BIN_DIR` | Installation directory, default `~/.local/bin` |
| `WORKBENCHES_SKIP_PROJECT_COMMAND=1` | Skip workBenches project installation |

The installer records its workstation checkout in a host-local
`.workbenches-path` beside the command. Environment/CLI overrides take precedence.

## Ownership

| Responsibility | Owner |
| --- | --- |
| Shape scaffolding, adoption, pins, family and validation mechanics | openRepoShape |
| Park/resume and estate transport | openRepoTools and the Speckit extension |
| Benches, technology generators, tools and workstation setup | workBenches |
| Project selection, orchestration and reporting | openRepoProject |

[Migration review](docs/migration-review.md) records what changed from
workBenches' original new-project script. Generic coordinator code lives here;
bench-specific generators remain in their repositories.

## Development

```sh
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
```

Run development commands in the Python workBench. Tests create disposable local
repositories and fake generators, never real GitHub projects. CI covers Linux
and macOS. On Windows, use WSL2 for Bash generators and estate commands.

Exit codes: 0 success; 1 doctor findings (warnings only with `--strict`);
2 invalid input/missing prerequisite; 130 cancellation. Delegated failures
preserve their exit status.

## License

Apache-2.0. See [LICENSE](LICENSE).
