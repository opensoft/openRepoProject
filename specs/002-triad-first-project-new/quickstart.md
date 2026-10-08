Lane: openRepoProject-1

# Quickstart: validating Triad-first project creation

A validation guide, not an implementation. The automated tests are the
authority (every delta scenario has one; see `traceability.md`); the hand runs
below show each user story at a real terminal. Exact text: `design.md` D13.
Contract: [contracts/project-new.md](contracts/project-new.md).

## Prerequisites

Python 3.10 or later, `bash` and `git`, run from the feature worktree
(`openRepoProject-worktrees/002-triad-first-project-new`). No network and no
GitHub credentials are needed or used.

## Run the tests

```bash
python3 -m unittest discover -s tests -v              # the whole suite
python3 -m unittest discover -s tests -v -k test_pty_ # the pty-driven tests only
```

Expected: every test passes, the 43 existing tests among them. Every pty test
name starts with `test_pty_` (a `tasks.md` naming rule). `/dev/full` exists on
Linux only, so that one guarded-stderr test is skipped on macOS, where the
closed-pipe test covers the same guard.

## Set up a fixture for hand runs (bash)

```bash
REPO=$PWD; T=$(mktemp -d)
mkdir -p "$T/wb/config" "$T/wb/devBenches/testBench/scripts" "$T/bin" "$T/projects"
printf '#!/bin/bash\nmkdir -p "$2/$1"\n' > "$T/wb/devBenches/testBench/scripts/new-test.sh"
printf '{"benches": {"testBench": {"path": "devBenches/testBench", "project_scripts": [{"name": "test", "script": "scripts/new-test.sh"}]}}}\n' > "$T/wb/config/bench-config.json"
cat > "$T/bin/openRepoShape" <<'FAKE'
#!/bin/bash
printf '%s\n' "$*" >> "$(dirname "$0")/openRepoShape.argv"
name=$1 into=
while [ $# -gt 0 ]; do [ "$1" = --into ] && into=$2; shift; done
printf 'Type yes to continue: '; read -r answer
if [ "$answer" = yes ]; then mkdir -p "$into/$name"; exit "${FAKE_SHAPE_STATUS:-0}"; fi
echo 'not confirmed; nothing was created.'; exit 1
FAKE
cat > "$T/bin/setup-openspeckit" <<'FAKE'
#!/bin/bash
echo "FOLLOWUP $*"; echo "FOLLOWUP $*" >&2; exit "${FAKE_FOLLOWUP_STATUS:-0}"
FAKE
chmod +x "$T/bin/openRepoShape" "$T/bin/setup-openspeckit"
unset GH_TOKEN GITHUB_TOKEN $(compgen -e | grep '^OPENREPOSHAPE_')
export WORKBENCHES_ROOT="$T/wb" PROJECTS_DIR="$T/projects" CI=
export PATH="$T/bin:$(dirname "$(command -v bash)"):$(dirname "$(command -v git)"):$(dirname "$(command -v python3)")"
p() { python3 "$REPO/project" "$@"; echo "exit=$?"; }
```

`CI=` is empty, which counts as false, so the question is asked. Remove each
created directory (`rm -rf "$T/projects/NAME"`) before repeating a run. Paths
below are shown as `$T/...`; the command prints them resolved.

## User Story 1: offered the Triad first

`p new MyApp` prints, before its prompt `Create it as a Triad? [Y/n or 1/2]:`:

```text
How should MyApp be created? Nothing is created until you confirm.
  1. Triad (default): an assembly root with a spec leg and a code leg, made by openRepoShape. It is preferred, not required: it stays elective and confers nothing.
  2. Single repository: fully supported, and no reason is asked. single-repository.yaml is the ratified way to record staying single.
```

| Answers typed | Expected |
| --- | --- |
| `2`, then `yes` at `Type yes to run this plan:` | `Create:` and the generator plan, `Created: $T/projects/MyApp`, `exit=0`; no `warning:` line |
| `n` or ` No `, then `no` at `Type yes` | `REFUSED: Cancelled; no command was run.`, `exit=2`; MyApp absent |
| `3`, then `maybe` | the line `Answer y or 1 for the Triad, n or 2 for a single repository; Enter takes the Triad.`, then `REFUSED: No recognised answer to the Triad question; nothing was created.`, `exit=2` |
| Ctrl-D | `REFUSED: No answer to the Triad question (end of input); nothing was created.`, `exit=2` |
| Ctrl-C | `Cancelled.`, `exit=130` |

`p new` asks `Project name:` first and the question after it; Ctrl-D at
`Project name:` still gives `Cancelled.` and `exit=130`. `p new MyApp
--dry-run` asks too: `2` prints the plan, `exit=0`, and `ls "$T/projects"`
stays empty.

## User Story 2: creating the Triad from the answer

`p new MyApp`, then Enter, `example` at `GitHub organization for the Triad:`
and `PUBLIC` at `Visibility (private, public or internal):` prints:

```text
Triad MyApp in organization example, visibility public: anyone can read the repositories.
Create: $T/projects/MyApp
  openRepoShape MyApp --org example --visibility public --into $T/projects
```

then the fake's `Type yes to continue:`. Typing `no` gives `not confirmed;
nothing was created.` and `exit=1`, with MyApp absent. Repeated with ` private `
and `yes`: `Triad MyApp in organization example, visibility private.`, then
`Created:` and `exit=0`; `cat "$T/bin/openRepoShape.argv"` shows the typed
organization, `private` and `--into`, and never `--yes`.

| At | Typed | Expected |
| --- | --- | --- |
| organization | `-bad` twice | `An organization name starts with a letter or digit and has only letters, digits and hyphens.`, then `REFUSED: Invalid GitHub organization name. Nothing was created.`, `exit=2` |
| visibility | `1`, then Enter | `Type the visibility in full: private, public or internal.`, then `REFUSED: Visibility must be private, public or internal. Nothing was created.`, `exit=2` |
| organization | Ctrl-D | `REFUSED: No GitHub organization was given (end of input); nothing was created.`, `exit=2` |
| visibility | Ctrl-D | `REFUSED: No visibility was given (end of input); nothing was created.`, `exit=2` |
| either | Ctrl-C | `Cancelled.`, `exit=130` |

`FAKE_SHAPE_STATUS=5 p new MyApp` with Enter, `example`, `private`, `yes` ends
`exit=5` (passed through). `p new MyApp --dry-run` with Enter, `example`,
`private` prints the restating line and the openRepoShape plan, `exit=0`, and
the fake is not run.

## User Story 3: known obstacles named beside the Triad

| Run | Line under entry 1 | Enter (Triad) | `2` then `yes` |
| --- | --- | --- | --- |
| `p new my-app` | `Not possible here: my-app cannot be a Triad name; a Triad name is a letter first, then letters and digits only, such as MyApp.` | refused, `exit=2` | created, `exit=0` |
| `p new MyApp` with `$T/bin/openRepoShape` moved aside | `Not possible here: openRepoShape is not on PATH. Install openRepoShape through workBenches first.` | refused, `exit=2` | created, `exit=0` |
| `p new MyApp --into "$T/absent"`, or `PROJECTS_DIR="$T/absent"` with no `--into` | `Not possible here: The parent directory $T/absent does not exist; a Triad is created inside an existing directory.` | refused, `exit=2` | created (the parent is made as today), `exit=0` |

Each refusal reads `REFUSED: A Triad cannot be created here. ` followed by the
obstacle sentences and ` Nothing was created.`; for `my-app`:
`REFUSED: A Triad cannot be created here. my-app cannot be a Triad name; a Triad name is a letter first, then letters and digits only, such as MyApp. Nothing was created.`
No organization prompt appears and `openRepoShape.argv` does not grow. The same
holds with `--dry-run`. With no obstacle (`p new MyApp`, fake on PATH, parent
present) no `Not possible here:` line appears.

## User Story 4: scripted creation and the advisory on stderr

`p new Flagged --type test --yes` prints today's stdout (`Create:`, the plan,
`Created:`, `Next:`) and, on stderr:

```text
warning: Flagged was created as a single repository. The Triad (an assembly root with a spec leg and a code leg) is preferred, not required: it stays elective and confers nothing.
warning: openRepoShape's adopt-project.py converts a repository in place when a person deciding for this project runs it, and a project that stays single can say so in single-repository.yaml. Nothing here changes.
```

| Run | Expected |
| --- | --- |
| `p new Quiet --type test --yes 2>/dev/null` | the same stdout shape, no `warning:` line, `exit=0` |
| `CI=true p new CiApp`, then `yes` | no question; the two `warning:` lines after creation; `exit=0` |
| `p new Piped < /dev/null` | no question; today's refusal at `Type yes`, `exit=2` |
| `p new Out \| cat`, then `yes` | no question; created; the two `warning:` lines on the terminal (stderr) |
| `p new Shaped --shape --org example --visibility private --yes`, then `yes` | no question, no `warning:` line, the fake's confirmation still asked, no `--yes` in its argv |
| `p new App --bench testBench --dry-run` (any choosing flag) | no question; the plan; `exit=0`; no `warning:` line |

The three guarded-stderr checks, each expecting today's stdout with no
`warning:` in it, `exit=0`, and `$T/projects/NAME/.project.json` present:

```bash
p new Closed --type test --yes 2>&-                    # stderr closed
p new Full --type test --yes 2>/dev/full               # full device (Linux)
exec 3> >(true); sleep 1; p new Broken --type test --yes 2>&3; exec 3>&-   # broken pipe
```

`p status "$T/projects/Flagged" --json` and `p doctor "$T/projects/Flagged"`
say nothing about the advisory, and `ls -A "$T/projects/Flagged"` lists only
`.project.json`.

## User Story 5: workspace names and the workflow follow-up

| Run | Expected |
| --- | --- |
| `p new alice-wip`, then `yes` | no question, created, no `warning:` line, `exit=0` |
| `p new Flow --type test --yes --workflow 2>&1` | both `warning:` lines before `FOLLOWUP --repo $T/projects/Flow` |
| `FAKE_FOLLOWUP_STATUS=3 p new Flow2 --type test --yes --workflow` | the `warning:` lines, the follow-up's output, `Project created at $T/projects/Flow2; workflow setup failed.`, `exit=3` |
| `p new Flow3 --workflow`, then `2` and `yes` | the follow-up runs with `--repo $T/projects/Flow3`; no `warning:` line from `project` |
| `p new bob-wip --type test --yes --workflow` | no `warning:` line; the follow-up runs |
| `p new Flow4 --workflow` with `setup-openspeckit` moved aside | `REFUSED: --workflow requires setup-openspeckit on PATH.`, `exit=2`, no question line |
| `p new Flow5 --type nope --workflow` with `setup-openspeckit` moved aside | `REFUSED: No matching generator; run project benches.`, `exit=2` (today's order) |

## Clean up

```bash
rm -rf "$T"
```
