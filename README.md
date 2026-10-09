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
project new MyApp
project new MyApp --bench flutterBench --type flutter --dry-run
project new MyApp ~/projects --bench flutterBench --type flutter --workflow
project new MyApp --description "a Flutter mobile app" --dry-run
```

The registry is `workBenches/config/bench-config.json`. Paths are relative to
that checkout. The list reports missing scripts and excludes updater entries.
Descriptions produce local keyword recommendations; they are never uploaded.
Ambiguous choices require an explicit selection.

At a terminal, without a choosing flag, `project new` asks one question once
the name is known, before any generator list, plan or confirmation:

```text
How should MyApp be created? Nothing is created until you confirm.
  1. Triad (default): an assembly root with a spec leg and a code leg, made by openRepoShape. It is preferred, not required: it stays elective and confers nothing.
  2. Single repository: fully supported, and no reason is asked. single-repository.yaml is the ratified way to record staying single.
Create it as a Triad? [Y/n or 1/2]:
```

The Triad is first and the default: Enter, `1`, `y` or `yes` takes it, and
`2`, `n` or `no` takes a single repository, with no reason asked. Letters are
compared case-insensitively and surrounding spaces are ignored. Any other
answer is asked once more; a second unrecognised answer, or end of input,
refuses with exit 2 and creates nothing. Ctrl-C prints `Cancelled.` and exits
130. The question is
not a confirmation and creates nothing: each answer still ends at its own
confirmation. `project` never writes `single-repository.yaml`.

Under the Triad entry, the question names any known obstacle, read locally
with no network access: a name that cannot be a Triad name (a letter first,
then letters and digits only, such as `MyApp`), `openRepoShape` missing from
`PATH`, or a parent that is missing or is not a directory. A single-repository
answer creates a missing parent; a parent that exists but is not a directory
blocks both answers, so choose another parent. The Triad stays first and the
default. A Triad answer with an obstacle is refused at once with exit 2, before
any further prompt; a single-repository answer is unaffected.

The question is not asked when:

- any choosing flag is given: `--shape`, `--org`, `--visibility`, `--family`,
  `--elected-by`, `--bench`, `--type`, `--description` or `--yes`, even with an
  empty value;
- stdin or stdout is not a terminal;
- `CI` is set to anything other than empty, `0`, `false` or `no`, in any letter case and ignoring surrounding spaces;
- the name is a `<user>-wip` workspace name, such as `alice-wip`.

A choosing flag restores the path without the question exactly: its prompts,
refusals, standard output, files and exit status are those `project new` had
before the question existed. To create a single repository without being
asked, name the generator, for example
`project new MyApp --bench flutterBench --type flutter`. `--dry-run`,
`--workflow`, `--into` or the positional parent, and `--workbenches` choose
nothing, so a dry run at a terminal asks too, then prints the plan of the path
its answer chose and writes nothing.

A Triad answer asks for the GitHub organization, then the visibility, typed in
full as `private`, `public` or `internal`, with no default. An empty or invalid
answer is asked once more, then refused with exit 2. One line then restates
the choice, such as `Triad MyApp in organization example, visibility private.`;
for `public` it says that anyone can read the repositories. The command then
runs openRepoShape without `--yes`, so openRepoShape's own typed confirmation
decides, and its exit status passes through.

After the question, when it is asked, the command shows the destination and
the command it will run. A single repository then asks for `yes` before
running its generator; a Triad ends at openRepoShape's own typed confirmation.
`--yes` confirms bench creation for scripted use. `--dry-run` prints the plan
without creating even the parent directory. Existing destinations refuse.
Generator errors pass through unchanged. The generator owns language runtime
requirements and environment creation: run it in the appropriate bench.

A single repository created without the question (chosen by flag, or not at a
person's terminal) is followed by two `warning:` lines on stderr once the
repository and its `.project.json` exist. They say that the Triad is preferred,
not required, stays elective and confers nothing; that openRepoShape's
`adopt-project.py` converts a repository in place when a person deciding for
the project runs it; that `single-repository.yaml` records staying single; and
that nothing changes. stdout, files, `.project.json` and the exit status are
unchanged, and a stderr that cannot be written is ignored. No advisory follows
a dry run, a Triad, a creation that went through the question, a workspace name
or a failed creation, and nothing records it.

`--workflow` runs `setup-openspeckit --repo PATH` after successful creation.
`project`'s own offer comes first (the question before creation, or the
advisory after it); then setup-openspeckit runs as before, and its own output
can include its own Triad advisory and, at a terminal, its own question. So
`--yes --workflow` prints two advisories back to back, and a person who
answered `2` may be asked again by setup-openspeckit, where `n` stops it:
`project` then reports that workflow setup failed and exits 130. When the
question will be asked, `--workflow` without `setup-openspeckit` on `PATH` is
refused before it.

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

Ctrl-C while openRepoShape runs reaches openRepoShape too; `project` stops
waiting after a moment and prints `Cancelled.`. Read openRepoShape's output,
and check the organization on GitHub, before retrying.

Legacy `onp NAME [PARENT]` and `new-project.sh NAME [PARENT]` in workBenches
forward to `project new` and also accept its new flags.

Agents offer the Triad in conversation, in the shared agent protocol's words
("When a person asks to create a new project, offer the Triad first as the
default"), then run `project new` with a choosing flag
(`--shape --org ORG --visibility VIS`, or `--bench` and `--type`), and never
answer the creation question, the organization, the visibility or
openRepoShape's confirmation on a person's behalf. The terminal check cannot
tell an agent at a pseudo-terminal from a person.

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
unmerged work. Ignored local files, remote divergence, and an unknown default
branch also stop destructive cleanup. A pushed-but-unmerged branch is handed
off to the repository's normal pull-request or merge process.

Apply actions are always explicit and target one branch or worktree. Pushes
are normal non-force pushes. A worktree can be removed only when it is clean,
non-current and verified merged into the local default branch; deleting its
local branch is a separate action. `clean` never fetches, stashes, resets,
force-pushes, creates or merges pull requests, or replaces `park`/`resume`.
It rechecks the selected state after confirmation and before executing an
action.

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
| `CI` | A value other than empty, `0`, `false` or `no` (any letter case, surrounding spaces ignored) means `project new` asks no creation question |
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
