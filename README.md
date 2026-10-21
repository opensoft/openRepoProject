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
Git 2.36 or later is required wherever `project` inspects a repository:
`project clean` refuses an older Git, and `project status` and `project doctor`
report it as an inspection error.
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

Five behaviour changes come first. Each differs from what `project clean` did
before:

1. An incomplete report exits 1. Plain `project clean` used to exit 0 for every
   report it printed. It now prints `Report: complete` or `Report: incomplete
   (CODES)`, and exits 1 when the report is incomplete: a worktree or probe it
   could not inspect (`inspection-incomplete`), more worktrees than the row cap
   (`inspect-cap`: above 256 for the plain report, above 128 for an
   `--all-safe` preview), or a run that ran out of time (`deadline-exceeded`).
   A plain report of 129 to 256 rows is still complete and exits 0; it only
   says `--all-safe would be incomplete (inspect-cap)`. A preview ends the
   same way.
2. `clean` refuses below Git 2.36. An older Git ends the run with
   `git-too-old`, and a missing or unusable one with `git-unavailable`, exit 2,
   before any repository is probed.
3. `--worktree P` refuses a freshly created merged worktree as
   `unstarted-branch`. A branch just created at the merge target counts as
   merged, and as published once it is pushed, so such a worktree used to look
   removable. It is now refused, exit 2, with the remedy `no commit was made on
   this branch here since it was created; review, then git worktree remove
   yourself`.
4. `--worktree P` refuses a merged worktree whose branch reflog keeps no
   decisive entry as `reflog-unavailable`: the reflog is missing, expired (no
   activity for `gc.reflogExpire`, 90 days by default) or undecidable. The
   remedy is `the branch's reflog is missing, expired or undecidable; review,
   then git worktree remove yourself`, and a batch withholds such a worktree
   too.
5. `--worktree P` removes a merged worktree whose upstream was deleted, and
   keeps its branch. A branch merged and then deleted on the remote used to be
   refused as `unpublished`; it is now `merged-removable` when it passes the
   gates below.

```sh
project clean
project clean /path/to/project --json
project clean /path/to/project --all-safe
project clean /path/to/project --all-safe --json
project clean /path/to/project --all-safe --apply
project clean /path/to/project --all-safe --apply --expect-plan DIGEST
project clean --apply --action push --branch 001-feature --yes
project clean --apply --action remove --worktree /path/to/feature-tree --yes
project clean --apply --action delete-branch --branch 001-feature --yes
```

`clean` is read-only by default. It inspects the linked worktrees, up to the row
caps below, using local refs and labels remote comparisons as of the last
fetch. It protects the default branch and preserves dirty, detached,
unpublished, remote-gone and unmerged work. Ignored local files, remote
divergence, and an unknown default branch also stop destructive cleanup. A
pushed-but-unmerged branch is handed off to the repository's normal
pull-request or merge process. With no argument it uses the repository Git
finds at the current directory; an absolute path must be the repository's main
worktree, or `clean` refuses with `target-not-repository-root` (exit 2).

Apply actions are explicit. `--all-safe --apply` always builds its own fresh
plan, never reusing a preview, and removes that plan's worktrees, at most 16 a
run; `--action push`, `--action remove` and `--action delete-branch` each
target one branch or worktree. Pushes are normal non-force pushes, and a push
refuses (`remote-gone`, exit 2) when the branch's upstream was deleted. A
worktree can be removed only when it is clean, non-current, verified merged into
the local merge target and past every gate below; removing it never deletes its
local branch, which is a separate action. `clean` never fetches, stashes,
resets, force-pushes, creates or merges pull requests, or replaces
`park`/`resume`. It rechecks the selected state after confirmation and before
executing each action.

### Preview and apply

`project clean ROOT --all-safe` previews and changes nothing, ROOT being the
repository's main worktree. After the header (`Cleanup plan for ROOT`, `Merge
target: NAME (SOURCE)`, `Freshness:`) it prints `Selected (N):` with one
`  remove PATH [BRANCH]` line for each worktree a batch would remove, then
`Excluded (M):` with a group `  REASON (K): NEXT STEP` for each reason and its
worktrees beneath (each heading prints only when it has rows), then, when a
worktree is selected, `Not protected: ...` (see "What is guaranteed"). When a
complete plan selects nothing it prints `No eligible worktrees` and exits 0.
The plain report adds `Report: complete` or `Report: incomplete (CODES)` and
`--all-safe would select N`. A plain report inspects up to 256 worktrees and
`--all-safe` up to 128; a report of more than 128 says `--all-safe would be
incomplete (inspect-cap)` in place of the count and withholds the selection;
such a report, up to 256 worktrees, is still complete and exits 0.

`--apply` runs the plan. `clean` plans again, prints the plan, and asks
`Remove N worktrees, keeping N branches? [yes/N]` (singular for one). Only
`yes`, surrounding spaces ignored, goes on; any other answer is refused as
`cancelled` (exit 2, nothing removed), and Ctrl-C or end of input prints
`Cancelled.` and exits 130. `--yes` accepts the fresh plan without asking.
Standard input that is not a terminal, without `--yes`, refuses with
`confirmation-required` (exit 2) after printing the plan, so a script must say
`--yes`. An incomplete plan under `--apply` is refused before any question,
exit 2 (a preview of it exits 1): `The plan is incomplete (CODE): REMEDY.` For
`inspection-incomplete` the remedy is to repair or remove the inspection-error
rows first (`git worktree repair`, `git worktree prune`, or remove the row by
hand after review); for `inspect-cap`, to remove worktrees explicitly or prune
stale entries by hand; for `deadline-exceeded`, to remove worktrees explicitly
or re-run.

`--all-safe` cannot be combined with `--action`, `--branch` or `--worktree`,
and `--expect-plan` needs `--all-safe` and `--apply`: each is
`invalid-arguments`, exit 2, with nothing run, as is an `--expect-plan` value
that is not 64 lowercase hexadecimal characters. `--apply --json` stays refused
for `--action push` and `--action delete-branch`. `--apply --action remove
--worktree P` gives the one worktree P the same gates and checks, asks the same
question and takes `--yes` and `--json`; it prints the other worktrees as
`not-requested`, a gate that excludes P refuses with `target-excluded`, exit 2,
and no match is `worktree-not-found`. This mode differs on completeness: P's row
and its gates come first, and only the repository-wide evidence and P's own row
must be complete. Another row's inspection error, rows past the cap of 128 and
rows the deadline stopped are noted and do not block P. If the deadline has
passed, P is `not-attempted` (`deadline-exceeded`) and the run exits 1. The
`target-excluded` message is `Worktree is excluded: REASON; NEXT STEP` for a
gate, and the older wording, with no next step, for the current worktree
(`Cannot remove the current worktree.`) and for a class that is not removable
(`Worktree is CLASS; only clean merged worktrees may be removed.`).

With `--json`, a report or preview prints one JSON document (`mode`,
`selected`, `excluded`, `completeness`, `apply_allowed`, `plan_digest`, and
more), and `--apply --json` prints one document: the result record below once
the apply phase has begun, otherwise the plan (or the error object) with its
refusal. The plan, the question and the progress go to standard error. An empty
plan, `No eligible worktrees`, is no refusal and exits 0. A refusal under
`--json` is a JSON document with its `code`, not a `REFUSED:` line.

### Pin a preview with `--expect-plan`

The preview's digest is `plan_digest` in `project clean ROOT --all-safe
--json`: 64 lowercase hexadecimal characters over the repository's identity, the
merge target and the selected worktrees (path, branch, head). The human preview
does not print it. Pass it back with `--apply --expect-plan DIGEST` and `clean`
rebuilds the plan first; when the fresh digest differs it refuses with
`plan-digest-mismatch`, exit 2, prints the fresh plan and changes nothing, so
the apply removes what was previewed and nothing else. A change to a worktree
the preview excluded leaves the digest alone; a change to a selected one, or to
the merge target, does not. A report above 128 worktrees withholds its
selection, so its digest cannot be pinned.

```sh
project clean ROOT --all-safe --json      # read plan_digest
project clean ROOT --all-safe --apply --expect-plan DIGEST
```

### Gates and next steps

A worktree is selected only if it passes every gate, checked in this order. An
excluded worktree is listed under the first gate it fails, and each reason
carries its next step:

| Reason | Next step |
| --- | --- |
| `main-worktree` | never removed by project clean |
| `unsupported-path-bytes` | rename the path to valid UTF-8 |
| `registration-mismatch` | review, then git worktree repair or git worktree prune, or remove the row by hand |
| `locked-worktree` | unlock it yourself if it should go |
| `inspection-error` | review, then git worktree repair or git worktree prune, or remove the row by hand |
| `dirty` | commit or preserve the changes |
| `ignored-local-files` | move or delete the ignored files by hand |
| any other class, such as `pushed-unmerged` | the report's recommendation for that class |
| `not-requested` | name it with --worktree to plan its removal |
| `unstarted-branch` | no commit was made on this branch here since it was created; review, then git worktree remove yourself |
| `reflog-unavailable` | the branch's reflog is missing, expired or undecidable; review, then git worktree remove yourself |
| `deferred-target-cap` | this run removes up to 16; run again: project clean ROOT --all-safe --apply |
| `contains-submodule` | review, then remove the worktree yourself |
| `hidden-local-state` | review, then remove the worktree yourself |

The first four reasons are facts about the row. The next four are its
classification, one gate, and only a `merged-removable` row passes it.
`not-requested` applies to `--worktree P` only. `unstarted-branch` and
`reflog-unavailable` come from the branch's reflog, read from the filesystem.
`contains-submodule` and `hidden-local-state` read the worktree's own index (a
gitlink; an assume-unchanged or skip-worktree flag) and its administrative
directory (a `modules` entry), for the 16 worktrees a run can take.

A run removes at most 16 worktrees. Further eligible worktrees show as
`deferred-target-cap`, and each run plans afresh, so run the same command again
until none are left; the preview digest covers only the selected worktrees, so a
deferred one's change leaves a preview valid. When every one of the 16 worktrees
ahead of the deferred ones is excluded as `contains-submodule`, the preview says
`these deferred rows will not drain while the 16 rows ahead of them are
contains-submodule; review those worktrees, then remove them yourself`.

### What is guaranteed

`clean` takes no lock and does not stop other writers. Its one guarantee is that
it spawns a removal only if, at the revalidation immediately before it, what
the plan recorded still holds: the repository and the worktree (identity,
registration, lock), the branch's name and tip, its upstream, the merge target,
the manifest, a clean status, and no submodule or hidden index flag. The first
target's repository-wide checks serve every target, so a difference found there
removes nothing at all. A difference refuses that target (`refused`), starts no
removal, attempts no later target and exits 2. Git's own `git worktree remove`,
never forced, is the last check.

The residual window is stated in one line in the preview when a worktree is
selected, in the confirmation and in the result: `Not protected: ignored files
created or index flags set after the last check, and any change after Git's own
check.` A removal never deletes a branch, so a branch that moves during a run
loses no commit; one seen only after Git removed the worktree leaves the target
`removed` with `branch-advanced-after-removal` or
`branch-missing-after-removal`, stops the run and exits 2.

### The result and recovery

An apply prints one line per target as it ends, `  removed PATH` or
`  STAGE PATH (REASON)`, then either `Removed N; branches kept: B1, B2.` or a
stop block, and the residual-window line:

```text
Stopped at PATH (REASON). Removed K of N. Not attempted: P1, P2. Next: project clean ROOT --all-safe
Branches kept: B1, B2.
```

A branch that read absent after its removal, or was not read back, is left out
of that line and listed on its own, `Branches not confirmed: B1.`, and the kept
line reads `Branches kept: none.` when no branch is left.

The run stops at the first target that does not end as a plain `removed`, and
every later target is `not-attempted`. The `Next:` command is a preview, not an
apply: run it, read what changed, then apply again; nothing from the stopped run
is reused. Each target ends in one stage: `removed`; `refused` (revalidation
found a difference, and no removal started); `failed` (Git refused or failed,
its status in `exit_status`); `unknown` (what happened could not be confirmed);
or `not-attempted`. The result record, which `--apply --json` prints, carries
for each target its `stage`, `reason`, `notes`, `command`, `exit_status` and
`reconciliation` (whether its registry entry, path and branch are still there),
beside `exit_code` and `completeness`.

A started removal is never interrupted. A signal during the apply is only
recorded, and when a signal or the deadline arrives during a removal, `Waiting
for git worktree remove PATH to finish; a started removal is never interrupted
(at most 300 s).` prints once and the removal is waited for. After a signal,
later targets are `not-attempted` (`interrupted`) and the run exits 130, 143
(SIGTERM) or 129 (SIGHUP); once less than 5 s of work time is left, later
targets are `not-attempted` (`deadline-exceeded`) and the run exits 1. At 300 s
the removal is killed, and its target is `removed` or `unknown` with reason
`removal-ceiling` by what a rescan finds, exit 1. A removal that Git refuses or
fails ends the run with Git's own status.

A removal killed at the ceiling, or whose exit was not seen, can leave the
worktree's registry entry or directory behind. The note `Probable partial
removal: inspect, then git worktree remove --force PATH by hand.` appears on
that target (`partially-removed`), and under the `dirty` advice of a worktree
whose tracked files are all deleted, which is how an interrupted removal looks
and why the note says "probable". The forced removal is the person's own step,
after looking, never `clean`'s. A target with the note `orphaned-directory` has
lost its registry entry but its directory is still there. When Git had already
deleted the worktree's `.git` file, the row is `registration-mismatch`: use
`git worktree repair` or `git worktree prune`, or remove the row by hand.

### Close sessions first

Close every session (editor, terminal, agent) whose directory is in a selected
worktree before a batch apply. `clean` does not look for them, since no process
scan sees all of them: an editor on the Windows side of WSL2, another user's
shell and a macOS process are invisible to it. A session left open can find its
worktree removed. The branch is kept, so no commit is lost, but work the session
had not yet written is. The plan lists every path before the question.

### Profile and container state

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
only. On Windows, use WSL2 for Bash generators and estate commands.

Exit codes: 0 success; 1 doctor findings (warnings only with `--strict`), and
for `clean` an incomplete report or preview, or an apply that ends `unknown`, at
the removal ceiling or past the deadline; 2 invalid input/missing prerequisite,
and any `clean` refusal; 130 cancellation; 143 and 129 `clean` stopped by
SIGTERM or SIGHUP. Delegated failures preserve their exit status, and so does
Git's own status from a `clean` removal, even when it equals one of these.

## License

Apache-2.0. See [LICENSE](LICENSE).
