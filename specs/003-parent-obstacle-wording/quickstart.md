Lane: openRepoProject-1

# Quickstart: validating the parent obstacle wording

A validation guide, not an implementation. The automated tests are the
authority (every delta scenario has one; see `traceability.md`); the hand runs
below show each user story at a real terminal. Exact text:
`openspec/changes/fix-parent-obstacle-wording/design.md` D2.

## Prerequisites

Python 3.10 or later and `bash`, run from the feature worktree root
(`openRepoProject-worktrees/003-parent-obstacle-wording`). No network and no
GitHub credentials are needed or used. The suite runs locally in the
`py-bench` container, which mounts the projects tree at the same path.

## Run the tests

```bash
docker exec py-bench bash -lc "cd '$PWD' && python3 -m unittest discover -s tests"                 # the whole suite
docker exec py-bench bash -lc "cd '$PWD' && python3 -m unittest discover -s tests -v -k test_pty_"  # the pty tests only
```

Expected after the realization: `Ran 96 tests`, `OK`: the 94 existing tests
with no existing assertion or case edited, plus the two new pty tests of D3.
On a host with Python 3.10 or later, `python3 -m unittest discover -s tests`
gives the same.

## Set up a fixture for hand runs (bash)

```bash
REPO=$PWD; T=$(mktemp -d)
mkdir -p "$T/wb/config" "$T/wb/devBenches/testBench/scripts" "$T/bin" "$T/home" "$T/realdir" "$T/projects"
printf '#!/bin/bash\nmkdir -p "$2/$1"\n' > "$T/wb/devBenches/testBench/scripts/new-test.sh"
printf '{"benches": {"testBench": {"path": "devBenches/testBench", "project_scripts": [{"name": "test", "script": "scripts/new-test.sh"}]}}}\n' > "$T/wb/config/bench-config.json"
printf '#!/bin/sh\necho "openRepoShape ran: $*" >&2; exit 1\n' > "$T/bin/openRepoShape"; chmod +x "$T/bin/openRepoShape"
printf 'keep\n' > "$T/afile"            # a regular file
ln -s "$T/afile" "$T/tofile"            # a symbolic link to it
ln -s "$T/nowhere" "$T/dangling"        # a dangling symbolic link
ln -s "$T/realdir" "$T/todir"           # a symbolic link to a directory
printf 'keep\n' > "$T/home/projects"    # the default ~/projects, as a regular file
mkfifo "$T/fifo"                        # a FIFO
export WORKBENCHES_ROOT="$T/wb" PROJECTS_DIR="$T/projects" CI=
export PATH="$T/bin:$(dirname "$(command -v bash)"):$(dirname "$(command -v python3)")"
p() { python3 "$REPO/project" "$@"; echo "exit=$?"; }
```

`CI=` is empty, which counts as false, so the question is asked. The fake
`openRepoShape` keeps that obstacle away; it must never run in these runs, and
says so on stderr if it does. Paths below are shown as `$T/...`; the command
prints them resolved (on macOS, under `/private/var`).

The two parent lines, exactly one of which appears under entry 1 when the
parent is not an existing directory:

```text
     Not possible here: The parent directory PARENT does not exist; a Triad is created inside an existing directory.
     Not possible here: The parent PARENT exists but is not a directory; choose a parent that is a directory.
```

Call them the missing line and the new line below.

## User Story 1: a parent that is not a directory is named truthfully

End input (Ctrl-D) at `Create it as a Triad? [Y/n or 1/2]:` in each run.

| Run | Line under entry 1 |
| --- | --- |
| `p new MyApp --into "$T/afile"` | the new line, PARENT `$T/afile` |
| `p new MyApp "$T/afile"` | the same |
| `PROJECTS_DIR="$T/afile" p new MyApp` | the same |
| `(unset PROJECTS_DIR; HOME="$T/home" p new MyApp)` | the new line, PARENT `$T/home/projects` |
| `p new MyApp --into "$T/tofile"` | the new line, PARENT `$T/afile` (the link's target) |
| `p new MyApp --into "$T/fifo"`, and `--into "$T/afile/"` | the new line, PARENT `$T/fifo` and `$T/afile` (EC-001) |

Each ends `REFUSED: No answer to the Triad question (end of input); nothing
was created.` and `exit=2`. The Triad is still entry 1 and the default, no line
of the question contains `--into` or `does not exist`, and `cat "$T/afile"`
still prints `keep`. Before the realization, these runs print the missing
line instead (observed at `26a5668` on Python 3.12.3 for `--into` the file and
the link).

The README sentence:

```bash
tr '\n' ' ' < README.md | tr -s ' ' | grep -c 'or a parent that is missing or is not a directory. A single-repository answer creates a missing parent; a parent that exists but is not a directory blocks both answers, so choose another parent.'   # 1
tr '\n' ' ' < README.md | tr -s ' ' | grep -c 'or a parent directory that does not exist'   # 0
```

## User Story 2: the refusal repeats the sentence the question printed

Take a snapshot first: `find "$T" | sort > "$T.before"`.

| Run | Answer | Expected |
| --- | --- | --- |
| `p new MyApp --into "$T/afile"` | Enter | `REFUSED: A Triad cannot be created here. The parent $T/afile exists but is not a directory; choose a parent that is a directory. Nothing was created.`, `exit=2`, no `GitHub organization for the Triad:` prompt |
| `p new my-app --into "$T/afile"` with `$T/bin/openRepoShape` moved aside | Enter | the composed refusal of D2: the name, openRepoShape and parent sentences in that order, the parent last; `exit=2` |
| `p new MyApp --into "$T/afile" --dry-run` | Enter | the refusal of the first row, `exit=2` |
| `p new MyApp --into "$T/tofile" --dry-run` | Enter | the same, naming `$T/afile` |
| `p new MyApp --into "$T/dangling" --dry-run` | Enter | `REFUSED: A Triad cannot be created here. The parent directory $T/nowhere does not exist; a Triad is created inside an existing directory. Nothing was created.`, `exit=2` |

Afterwards `find "$T" | sort | diff "$T.before" -` prints nothing, `test -f
"$T/afile" && ! test -L "$T/afile"` succeeds, and `cat "$T/afile"` prints
`keep`. No `openRepoShape ran:` line appears.

## User Story 3: every other case reads and ends as it does today

| Run (Ctrl-D at the question) | Line under entry 1 |
| --- | --- |
| `p new MyApp --into "$T/absent"` | the missing line, PARENT `$T/absent`, byte for byte as today |
| `p new MyApp --into "$T/dangling"` | the missing line, PARENT `$T/nowhere` |
| `p new MyApp --into "$T/todir"` | none: no `Not possible here:` line |
| `p new MyApp --into "$T/afile/sub"` | the missing line, PARENT `$T/afile/sub` (EC-002, an accepted residual) |
| `p new my-app`, or `p new MyApp` with `$T/bin/openRepoShape` moved aside | the name line or the openRepoShape line, as today |

The single-repository answer against its flag-chosen baseline:

| Run | Answers | Expected |
| --- | --- | --- |
| `p new MyApp --into "$T/afile"` | `2`, then `yes` at `Type yes to run this plan:` | `Create: $T/afile/MyApp`, the generator plan, then `REFUSED: [Errno 17] File exists: '$T/afile'`, `exit=2`; no `warning:` line |
| `p new MyApp --into "$T/afile" --type test` | `yes` | the same from `Create:` on, the same `REFUSED:` line, `exit=2` |

Both runs end this way today too (D6, a known limitation; EC-003).
`p new MyApp --into "$T/afile" --type test --dry-run` prints the plan and
exits 0, also unchanged.

## Checks on the realization

Run from the worktree root, with `BASE=$(git merge-base origin/main HEAD)`.

```bash
# Added lines are ASCII (FR-011, N4); expect no output.
git diff "$BASE" -- project tests/test_project.py README.md specs/003-parent-obstacle-wording \
  | grep '^+' | grep -v '^+++' | LC_ALL=C grep -nP '[^\x00-\x7F]'

# No existing assertion or row tuple is edited (FR-012, SC-006); expect exactly one line,
# the old "all three" row of known_obstacle_cases(), whose closing brace gave way.
git diff "$BASE" -- tests/test_project.py | grep '^-' | grep -v '^---'

# The change and every main spec validate; use /usr/bin/openspec (1.6.0) or the openspec in
# py-bench (1.13.1), not the outdated 1.2.0 first on the host PATH (plan.md, Risks and Notes).
/usr/bin/openspec validate fix-parent-obstacle-wording --strict
/usr/bin/openspec validate --all --strict
docker exec py-bench bash -lc "cd '$PWD' && openspec validate --all --strict"
```

## Clean up

```bash
rm -rf "$T" "$T.before"
```
