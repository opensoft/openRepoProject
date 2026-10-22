Lane: openRepoProject-1

# Quickstart: validating the early refusal of a non-directory parent

A validation guide, not an implementation. The automated tests are the
authority (every delta scenario has one; see `traceability.md`); the hand runs
below show each user story at a real terminal, and the check blocks (`# check: ID`,
listed under "Checks on the realization") hold, in full, every check the plan's
verify cells name; each exits 0 on a pass and non-zero on any mismatch. Every
check is run as one command, `bash specs/006-refuse-non-directory-parent-early/qs.sh
ID [NAME=VALUE ...]` (the committed runner `qs.sh`, beside this file; its text is
in the plan), so that no check needs a variable from an earlier block or call.
Exact text: `openspec/changes/refuse-non-directory-parent-early/design.md` D2.

**Clarify answers**: follows Brett Heap's clarify answers of 2026-10-22, "all
recommended" (Q1 B, Q2 A, Q3 A, Q4 B, Q5 A), recorded in the spec's
Clarifications. Commands or counts that depend on one carry its tag; the
plan's appendix, "Options not taken", says what changes under another option.

## Environment

Run everything from the feature worktree
(`openRepoProject-worktrees/006-refuse-non-directory-parent-early`), in bash or
zsh; `qs.sh` finds the top of the worktree itself, the other commands want it as
the current directory. No network and no GitHub credentials are needed or used,
except where a step says so. In zsh, brace every `"${REV}:path"` as written
below: a bare `"$REV:path"` is a zsh modifier and `git show` then reads nothing.

**Shell state.** No check, verify or build task relies on a variable, function
or file made by an earlier block or call: every check block is run by `qs.sh`
with what it needs passed as `NAME=VALUE`, and every other block below defines
what it uses inside itself. The one deliberate exception is the hand-run
fixture ("Set up a fixture for hand runs") with its `$T` and `p`: the hand walk
types the runs of User Stories 1 to 5, and "Clean up", into the shell (two
shells for User Story 4) that holds that fixture, at a real terminal; it is the
lead's or Brett Heap's walk, a lane step, not a dispatched verify.

- **Python 3.12**: the `py-bench` container (Python 3.12.3, PyYAML installed)
  mounts the projects tree at the same path, so
  `docker exec py-bench bash -lc "cd '$PWD' && ..."` runs a command here.
- **Python 3.10 with PyYAML** (CI installs `requirements.txt`, PyYAML 6). Any
  3.10 interpreter serves once PyYAML is importable. Offline, link an
  installed PyYAML's package directory into a directory of its own and put that
  directory on `PYTHONPATH`; PyYAML 6 falls back to pure Python when its C
  extension does not match the interpreter:

  ```bash
  Y=$(mktemp -d)
  ln -s "$(python3 -c 'import os, yaml; print(os.path.dirname(yaml.__file__))')" "$Y/yaml"
  PYTHONPATH="$Y" "$(uv python find 3.10)" -c 'import sys, yaml; print(sys.version.split()[0], yaml.__version__, yaml.__with_libyaml__)'
  # 3.10.x 6.0.3 False
  ```

  This works on the host (`uv` there finds 3.10.18) and inside `py-bench`
  (run the three lines there; its `uv` finds 3.10.21). Check `suite` does the
  same link itself when its `PY` lacks PyYAML, so the gate needs none of this
  by hand. With network, a virtual environment does the same, in one block:

  ```bash
  V=$(mktemp -d) && "$(uv python find 3.10)" -m venv "$V" && "$V/bin/pip" install -r requirements.txt \
    && "$V/bin/python" -m unittest discover -s tests
  ```
- **OpenSpec**: `/usr/bin/openspec` (1.6.0) or the `openspec` in `py-bench`,
  never the outdated 1.2.0 first on the host `PATH`. Without network, 1.6.0
  first prints a harmless telemetry error (an `AbortError`, or a PostHog
  network error); the result line follows it.

## Run the tests

```bash
docker exec py-bench bash -lc "cd '$PWD' && python3 -m unittest discover -s tests"                 # 3.12.3
docker exec py-bench bash -lc "cd '$PWD' && python3 -m unittest discover -s tests -v -k test_pty_"  # the pty tests only
```

The gate, on 3.12 and on 3.10 with PyYAML, is check `suite`; it links PyYAML in
itself when its `PY` lacks it, and compares the count with `N0` (below):

```bash
bash specs/006-refuse-non-directory-parent-early/qs.sh suite ADDED=0                        # before the realization, python3
bash specs/006-refuse-non-directory-parent-early/qs.sh suite PY="$(uv python find 3.10)"    # 3.10; ADDED defaults to 15 [Q2]
```

Run them in the foreground: in a background job SIGINT is ignored and three
interrupt tests fail.

**The expected count is relative.** Main gains PR #33's tests before this
feature lands, so no count is fixed here. `N0` is the number of tests at the
merge base, measured on an export of it:

```bash
BASE=$(git merge-base origin/main HEAD); E=$(mktemp -d)
git archive "$BASE" | tar -x -C "$E"
( cd "$E" && python3 -c 'import unittest; print(unittest.defaultTestLoader.discover("tests").countTestCases())' )   # N0
```

Before the realization the suite must give `Ran N0 tests`, `OK`; after it,
`Ran N0+15 tests`, `OK` `[Q2]` (the existing tests, one of them rewritten, plus
15 new), on 3.12 and on 3.10 with PyYAML. At `d47e8a4`, `N0` is 96. The check
`suite` below measures `N0` and compares.

```bash
# check: suite
# Run: bash specs/006-refuse-non-directory-parent-early/qs.sh suite [PY=python3] [ADDED=15]   (in the foreground)
# ADDED is the number of tests this feature has added so far: 0 for slices S1 and T1, 15 [Q2] from I1 on.
# PY may be a 3.10 interpreter, for example PY="$(uv python find 3.10)"; PyYAML is linked in when it lacks it.
PY=${PY:-python3}; ADDED=${ADDED:-15}
BASE=${BASE:?run through qs.sh}
if ! "$PY" -c 'import yaml' 2>/dev/null; then
  Y=$(mktemp -d) && ln -s "$(python3 -c 'import os, yaml; print(os.path.dirname(yaml.__file__))')" "$Y/yaml" || exit 1
  export PYTHONPATH="$Y${PYTHONPATH:+:$PYTHONPATH}"
fi
"$PY" -c 'import yaml' || { echo "suite: $PY cannot import PyYAML" >&2; exit 1; }
E=$(mktemp -d) && git archive "$BASE" | tar -x -C "$E" || exit 1
N0=$(cd "$E" && "$PY" -c 'import unittest; print(unittest.defaultTestLoader.discover("tests").countTestCases())') || exit 1
OUT=$("$PY" -m unittest discover -s tests 2>&1); RC=$?
RAN=$(printf '%s\n' "$OUT" | sed -n 's/^Ran \([0-9][0-9]*\) tests\{0,1\} in .*/\1/p')
printf '%s\n' "$OUT" | tail -n 3
echo "suite: N0 = $N0 at $BASE; expected Ran $((N0 + ADDED)); got Ran ${RAN:-nothing}; unittest exit $RC"
[ "$RC" -eq 0 ] && [ "$RAN" = "$((N0 + ADDED))" ]
```

A 3.10 run without PyYAML is informational only. It fails these 11 tests at
the base too, and must fail no other: `test_doctor_validate_reports_missing_owner_scripts`,
`test_doctor_validate_with_a_project_leg_has_structured_output`,
`test_family_name_prefers_holder_and_inspects_working_sibling`,
`test_handoff_reads_matching_record_without_changing_it`,
`test_handoff_rejects_non_github_host_before_record_lookup`,
`test_handoff_rejects_path_like_remote_identity_before_record_lookup`,
`test_human_reports_render_present_project_leg_state`,
`test_shape_skips_assembly_dot_and_reports_missing_legs`,
`test_shape_update_runs_check_then_apply_and_propagates_failure`,
`test_update_refuses_a_dirty_family_member`,
`test_update_refuses_missing_child_and_retains_shape_owner_prompt`.

## Set up a fixture for hand runs (bash)

Run this block once, in the shell at a real terminal where the hand walk types
User Stories 1 to 5. It is the one place that leaves shell state behind on
purpose. The second shell of User Story 4 gets the same `T`, `REPO`,
`WORKBENCHES_ROOT`, `PROJECTS_DIR`, `CI` and `PATH` and the same `p`, not a
second fixture.

```bash
REPO=$PWD; T=$(mktemp -d)
mkdir -p "$T/wb/config" "$T/wb/devBenches/testBench/scripts" "$T/bin" "$T/home" "$T/realdir" "$T/projects" "$T/emptywb" "$T/bdir"
printf '#!/bin/bash\nmkdir -p "$2/$1"\n' > "$T/wb/devBenches/testBench/scripts/new-test.sh"
printf '{"benches": {"testBench": {"path": "devBenches/testBench", "project_scripts": [{"name": "test", "script": "scripts/new-test.sh"}, {"name": "second", "script": "scripts/new-test.sh"}]}}}\n' > "$T/wb/config/bench-config.json"
printf '#!/bin/sh\necho "openRepoShape ran: $*" >&2; exit 1\n' > "$T/bin/openRepoShape"; chmod +x "$T/bin/openRepoShape"
printf 'keep\n' > "$T/afile"            # FILE, a regular file
printf 'keep\n' > "$T/rfile"            # a file to repair while the question waits (US4)
ln -s "$T/afile" "$T/tofile"            # a symbolic link to FILE
ln -s "$T/afile/x" "$T/tobelow"         # a symbolic link to a path below FILE
ln -s "$T/nowhere" "$T/dangling"        # a dangling symbolic link (below a directory)
ln -s "$T/realdir" "$T/todir"           # a symbolic link to a directory
mkfifo "$T/fifo"                        # a FIFO
python3 -c 'import socket, sys; s = socket.socket(socket.AF_UNIX); s.bind(sys.argv[1]); s.close()' "$T/sock"   # a socket [Q3]
printf 'keep\n' > "$T/home/projects"    # the default ~/projects, as a regular file
mkdir "$T/locked"; chmod 555 "$T/locked"   # a directory the person cannot write (skip as root)
export WORKBENCHES_ROOT="$T/wb" PROJECTS_DIR="$T/projects" CI=
export PATH="$T/bin:$(dirname "$(command -v bash)"):$(dirname "$(command -v python3)")"
p() { python3 "$REPO/project" "$@"; echo "exit=$?"; }
find "$T" | sort > "$T.before"
```

`CI=` is empty, which counts as false, so the question is asked where no other
rule skips it. The fake `openRepoShape` keeps that obstacle away; it must never
run in these runs, and says so on stderr if it does. `setup-openspeckit` is not
on `PATH`. The registry has two available generators, so a single-repository
path that reaches `choose()` without `--type` prints a list and asks
`Select a generator number`. Paths below are shown as `$T/...`; the command
prints them resolved.

The lines, with `PARENT` and `ANCESTOR` resolved paths:

```text
     Not possible here: The parent directory PARENT does not exist; a Triad is created inside an existing directory.
     Not possible here: The parent PARENT exists but is not a directory; choose a parent that is a directory.
     Not possible here: The parent PARENT cannot be created because ANCESTOR exists but is not a directory; choose a parent that is a directory.
REFUSED: The parent PARENT exists but is not a directory; choose a parent that is a directory. Nothing was created.
REFUSED: The parent PARENT cannot be created because ANCESTOR exists but is not a directory; choose a parent that is a directory. Nothing was created.
```

Call them the missing line, line (a), line (b), and the head refusals (a) and
(b) below.

## User Story 1: a flag-chosen or not-asked single repository is refused before the plan

Each run prints nothing on standard output, ends with the head refusal named,
and `exit=2`; no `Create:`, plan, `Type yes to run this plan:` or question line
appears.

| Run | Head refusal |
| --- | --- |
| `p new MyApp --into "$T/afile" --type test --yes` | (a), PARENT `$T/afile` |
| the same with `--dry-run` in place of `--yes` | the same |
| the same with neither (at the terminal) | the same |
| `CI=true p new MyApp --into "$T/afile"` | the same |
| `p new MyApp --into "$T/afile" < /dev/null` (standard input not a terminal) | the same |
| `p new alice-wip --into "$T/afile"`, and with `--dry-run` (both at the terminal) | the same |
| `--into "$T/tofile"`, `"$T/afile/"`, `"$T/fifo"`, `"$T/sock"` `[Q3]`, `/dev/null` `[Q3]`, each `--type test --yes` | (a), PARENT `$T/afile`, `$T/afile`, `$T/fifo`, `$T/sock`, `/dev/null` |
| `p new MyApp "$T/afile" --type test --yes` (positional) | (a), PARENT `$T/afile` |
| `PROJECTS_DIR="$T/afile" p new MyApp --type test --yes` | the same |
| `(unset PROJECTS_DIR; HOME="$T/home" p new MyApp --type test --yes)` | (a), PARENT `$T/home/projects` |
| `--into "$T/afile/sub"`, `"$T/afile/a/b"`, `"$T/tobelow"`, each `--type test --yes`, and `--dry-run` | (b), PARENT `$T/afile/sub`, `$T/afile/a/b`, `$T/afile/x`; ANCESTOR `$T/afile` |
| `p new MyApp --into "$T/afile" --type nomatch --yes` | (a), not `No matching generator; run project benches.` |
| `p new MyApp --into "$T/afile" --type test --workflow --yes` | (a), not `--workflow requires setup-openspeckit on PATH.` |
| `p new MyApp --into "$T/afile" --type test --yes --workbenches "$T/emptywb"` `[Q4]` | (a), not `Cannot find workBenches; set WORKBENCHES_ROOT or --workbenches PATH.` |

Before the realization (observed at `d47e8a4` on Python 3.12.3 in a scratch
copy): `--yes` printed `Create:` and the plan and ended
`REFUSED: [Errno 17] File exists: '$T/afile'` (`[Errno 20] Not a directory`
below the file); `--dry-run` printed the plan and exited 0; at the terminal the
run stopped at `Type yes to run this plan:`; `nomatch`, `--workflow` and the
empty `--workbenches` gave their own sentences.

## User Story 2: a single-repository answer is refused at once

| Run | Answer | Expected |
| --- | --- | --- |
| `p new MyApp --into "$T/afile"` | `2` | the question with line (a) under entry 1, then at once the head refusal (a) (on the prompt's line of standard error), `exit=2`; no `1. testBench:test`, no `Select a generator number`, no `Create:`, no `Type yes to run this plan:` |
| the same with `--dry-run` | `2` | the same |
| `p new MyApp --into "$T/afile/sub"`, with and without `--dry-run` | `2` | line (b), then the head refusal (b), `exit=2`, nothing else |
| `p new MyApp --into "$T/afile" --type test` | none | the same `REFUSED:` line as the first row, `exit=2`, no question, no `Create:` |
| `p new my-app --into "$T/absent"` with `$T/bin/openRepoShape` moved aside | `2`, then `1` at `Select a generator number`, then `yes` | as today: the generator list, the plan, `Created: $T/absent/my-app`, `exit=0`, no `warning:` line |

Before the realization, the first row reached the generator list (two
generators) and, with one generator, the plan and `yes`, then `[Errno 17]`;
with `--dry-run` it printed the plan and exited 0.

## User Story 3: a missing parent below a file is named truthfully at the question

| Run | Answer | Expected |
| --- | --- | --- |
| `p new MyApp --into "$T/afile/sub"` | Ctrl-D | entry 1 is still first and the default; its one parent line is line (b), PARENT `$T/afile/sub`, ANCESTOR `$T/afile`; no line says `does not exist` or contains `--into`; `REFUSED: No answer to the Triad question (end of input); nothing was created.`, `exit=2` |
| the same | Enter | `REFUSED: A Triad cannot be created here. The parent $T/afile/sub cannot be created because $T/afile exists but is not a directory; choose a parent that is a directory. Nothing was created.`, `exit=2`, no `GitHub organization for the Triad:` prompt |
| the same with `--dry-run` | Enter | the same refusal, `exit=2` |
| `p new my-app --into "$T/afile/sub"` with `$T/bin/openRepoShape` moved aside | Enter | the composed refusal: the name, openRepoShape and (b) sentences in that order, `exit=2` |
| `p new MyApp --into "$T/afile"` | Ctrl-D, then Enter | line (a) and its Triad refusal, byte for byte as today |
| `p new MyApp --into "$T/absent"`, and `--into "$T/dangling"` | Ctrl-D | the missing line, PARENT `$T/absent` and `$T/nowhere`, as today |
| `p new MyApp --into "$T/todir"` | Ctrl-D | no `Not possible here:` line |

Before the realization, `$T/afile/sub` printed the missing line ("does not
exist") and its Triad refusal carried that sentence.

## User Story 4: the parent is read as it is when the path is taken

Two terminals, the same fixture exported in both.

1. `p new MyApp --into "$T/rfile"` in the first: line (a) under entry 1. In the
   second, `rm "$T/rfile" && mkdir "$T/rfile"`. Answer `2`, then `1` at
   `Select a generator number`, then `yes`: `Created: $T/rfile/MyApp`,
   `exit=0`.
2. `p new MyApp --into "$T/bdir"` in the first: no parent line. In the second,
   `rmdir "$T/bdir" && printf 'keep\n' > "$T/bdir"`. Answer `2`: at once the
   head refusal (a), PARENT `$T/bdir`, `exit=2`, no further prompt.

The automated tests do the same in process (plan N9, N10).

## User Story 5: parents that are not blocked, and the other refusals, behave as before

| Run | Expected |
| --- | --- |
| `p new MyApp --into "$T/afile" --shape --org example --visibility private`, with and without `--dry-run`; the same for `"$T/afile/sub"` | `REFUSED: Shape creation requires an existing --into parent directory.`, `exit=2`, no `Create:`; never the head refusal |
| `p new MyApp --into "$T/afile" --org example --yes` | `REFUSED: --org, --visibility, --family and --elected-by require --shape.`, `exit=2` |
| `p new "bad name" --into "$T/afile" --type test --yes` | `REFUSED: Project name must start with a letter or digit and contain letters, digits, _ or -.`, `exit=2` |
| `p new MyApp --into "$T/afile" --family 1bad --yes` `[Q4]` | `REFUSED: Family must be a single folder name.`, `exit=2` |
| `p new MyApp --into "$T/locked/child" --type test --dry-run` (not as root) | `Create: $T/locked/child/MyApp` and the plan, `exit=0` |
| the same with `--yes` | `Create:` and the plan, then `REFUSED: [Errno 13] Permission denied: '$T/locked/child'`, `exit=2`, no `Nothing was created.` |
| `p new MyApp --into "$T/realdir" --type test --dry-run` | the destination and the generator command, nothing written, no `warning:` line, `exit=0` |
| `p new MyApp --into "$T/dangling" --type test --yes` (run this last: it creates `$T/nowhere`) | `Create: $T/nowhere/MyApp`, the plan, `Created:`, the two `warning:` lines on stderr, `exit=0` |

All of these end the same way before the realization.

## User Story 6: the README says what a blocked parent does

Lines joined by single spaces; each count must be exactly the number shown.
`grep -oF ... | wc -l` counts occurrences; `grep -c` would print 1 for a text
found twice on the one joined line. The check prints each mismatch and exits 1
on any; it prints `README OK` and exits 0 when every count holds.

```bash
# check: readme-texts
# Run: bash specs/006-refuse-non-directory-parent-early/qs.sh readme-texts
BASE=${BASE:?run through qs.sh}
J=$(tr '\n' ' ' < README.md | tr -s ' ')
bad=0
want() {   # want COUNT TEXT: TEXT occurs exactly COUNT times in the joined README
  got=$(printf '%s' "$J" | grep -oF -e "$2" | wc -l | tr -d ' ')
  [ "$got" = "$1" ] || { echo "README: $got, want $1: $2" >&2; bad=1; }
}
want 1 'or a parent that is missing or is blocked by a non-directory. A single-repository answer creates a missing parent whose nearest existing path above it is a directory. A parent blocked by a non-directory (it, or the nearest existing path above it, exists and is not a directory) blocks both answers: neither answer can create anything in such a parent, and either is refused at once with exit 2, so choose another parent. The Triad stays first and the default. A Triad answer with an obstacle is refused at once with exit 2, before any further prompt; a single-repository answer is unaffected by the name and openRepoShape obstacles.'
want 1 'A choosing flag restores the path without the question: its prompts, refusals, standard output, files and exit status are exactly as they would be without the question.'
want 1 'then prints the plan of the path its answer chose, unless a refusal comes first, and writes nothing.'
want 1 'Existing destinations refuse. A parent blocked by a non-directory is refused before the plan and the `yes` confirmation, with exit 2, `--dry-run` included. `--dry-run` reads no permissions: a parent that is a directory the person cannot write still passes the dry run and fails at creation, as before, and so, for a single repository, does a missing parent whose nearest existing path above it is such a directory.'
want 1 'a parent that is a directory the person cannot write'   # lane 4 replaces this phrase later
for old in 'or a parent that is missing or is not a directory.' 'a parent that exists but is not a directory blocks both answers' \
           'a single-repository answer is unaffected.' 'without the question exactly' 'had before the question existed' \
           'its answer chose and writes nothing'; do
  want 0 "$old"
done
git show "${BASE}:README.md" > /dev/null || exit 1
diff <(git show "${BASE}:README.md" | sed -n 53,55p) <(sed -n 53,55p README.md) > /dev/null \
  || { echo "README: lines 53-55 changed" >&2; bad=1; }
[ "$bad" -eq 0 ] && echo "README OK"
```

These counts were observed on a scratch copy edited by the plan's rewrap
recipe (research R8). This check supersedes feature 003's README check (its
`quickstart.md:86-87`).

## Checks on the realization

Every check is run with the committed runner `qs.sh`, in the foreground, from
anywhere in the worktree:

```bash
bash specs/006-refuse-non-directory-parent-early/qs.sh <check-id> [NAME=VALUE ...]
```

`qs.sh` (its text is in the plan, "qs.sh (exact text)") changes to the top of
the worktree, takes the fenced block of this file whose first line is exactly
`# check: <check-id>`, exports `BASE` and every `NAME=VALUE`, runs the block
with bash, and exits with the block's status. `BASE` is `git merge-base
origin/main HEAD`, never a fixed sha, so the checks hold before and after main
(with #33) is merged in; a call that passes `BASE=<sha>` overrides it. If the
marker is missing, or starts more than one block, `qs.sh` prints a message and
exits 2, so 2 means "the runner could not run the check": a check that must
fail (mutant M4) is read as "exits 1", never as "non-zero". A path in a
`NAME=VALUE` is read after the change to the top of the worktree: give an
absolute path, or one relative to it. No call relies on a variable or a file
from an earlier call; every variable a check reads is in the table.

**Check blocks.** Every check is one fenced block whose first line is
`# check: ID`. Each is a bash script on its own: it computes what it needs,
exits 0 when everything it checks holds, and exits non-zero (printing what
differs) on any mismatch. "Run check ID" (the plan's verify cells) means
`qs.sh ID` with the variables the cell names; the plan's `STAGE=g1` check
`governance` is `qs.sh governance STAGE=g1`. The ids, in file order, with the
`NAME=VALUE` each reads (the default after it) besides `BASE`:

| Check | Reads |
| --- | --- |
| `suite` | `PY` (`python3`), `ADDED` (15 `[Q2]`) |
| `readme-texts` | nothing |
| `ascii-added` | nothing |
| `files-changed` | nothing |
| `fixed-text` | `PARTS` (`fixtures readme`) |
| `ast-project` | `PROJECT` (`project`) |
| `ast-tests` | `NEW_TESTS` (15 `[Q2]`) |
| `red-first` | `TESTS` (the whole list), `MUTANT`, `RF_MUST_FAIL` |
| `openspec` | `OPENSPEC` (`/usr/bin/openspec`) |
| `traceability` | `MODE` (`complete`, or `skeleton`) |
| `governance` | `STAGE` (`g1`, or `g2`), `OPENSPEC` |
| `merge-check` | `HEAD33` (required) |

### ASCII

Added lines are ASCII (FR-013). The whole files are not checked: `project`
carries em dashes at `:197`, `:915`, `:928` and `:1136`, and the test module
one at `:622`. The diff covers `project`, `tests/test_project.py`, `README.md`,
this feature's directory and `[Q5]` the change's `tasks.md`.

```bash
# check: ascii-added
# Run: bash specs/006-refuse-non-directory-parent-early/qs.sh ascii-added
BASE=${BASE:?run through qs.sh}
DIFF=$(git diff "$BASE" -- project tests/test_project.py README.md specs/006-refuse-non-directory-parent-early \
  openspec/changes/refuse-non-directory-parent-early/tasks.md) || exit 1
HITS=$(printf '%s\n' "$DIFF" | grep '^+' | grep -v '^+++' | LC_ALL=C grep -nP '[^\x00-\x7F]')
if [ -n "$HITS" ]; then printf 'non-ASCII added line: %s\n' "$HITS" >&2; exit 1; fi
echo "ASCII OK"
```

### Files changed

FR-016 `[Q5]`: the branch changes only `project`, `tests/test_project.py`,
`README.md`, `[Q5]` the change's `tasks.md`, and files under
`specs/006-refuse-non-directory-parent-early/`: `spec.md`,
`clarify-questions.md`, `checklists/requirements.md`, `plan.md`, `research.md`,
`quickstart.md`, `tasks.md`, `traceability.md` and the runner `qs.sh`. The
runner must be among the committed changes: every verify calls it.

```bash
# check: files-changed
# Run: bash specs/006-refuse-non-directory-parent-early/qs.sh files-changed
BASE=${BASE:?run through qs.sh}
NAMES=$(git diff --name-only "$BASE"..HEAD) || exit 1
EXTRA=$(printf '%s\n' "$NAMES" \
  | grep -vx -e project -e tests/test_project.py -e README.md -e openspec/changes/refuse-non-directory-parent-early/tasks.md \
  | grep -v -e '^specs/006-refuse-non-directory-parent-early/' -e '^$')
if [ -n "$EXTRA" ]; then printf 'outside FR-016: %s\n' "$EXTRA" >&2; exit 1; fi
printf '%s\n' "$NAMES" | grep -qx 'specs/006-refuse-non-directory-parent-early/qs.sh' \
  || { echo "the runner specs/006-refuse-non-directory-parent-early/qs.sh is not among the committed changes" >&2; exit 1; }
echo "files OK"
```

### Fixed text

The fixture texts equal `design.md` D2 character for character, and the README
holds each of the four texts once. Slice T1 runs it with `PARTS=fixtures`
(before the README is edited); by default it checks both parts.

```bash
# check: fixed-text
# Run: bash specs/006-refuse-non-directory-parent-early/qs.sh fixed-text [PARTS=fixtures]
# PARTS is "fixtures readme" by default; PARTS=fixtures alone before the README is edited.
PARTS=${PARTS:-fixtures readme} python3 - <<'EOF'
import os, sys
parts = os.environ["PARTS"].split()
d = open("openspec/changes/refuse-non-directory-parent-early/design.md").read().split("\n")
if "fixtures" in parts:
    sys.path.insert(0, "tests")
    import test_project as t
    b = t.OBSTACLE_PARENT_BELOW_A_NON_DIRECTORY.format(PARENT="PARENT", ANCESTOR="ANCESTOR")
    a = t.OBSTACLE_PARENT_NOT_A_DIRECTORY.format(PARENT="PARENT")
    assert t.OBSTACLE_PARENT.format(PARENT="PARENT") == d[135]
    assert a == d[136] and b == d[137]
    assert t.REFUSED + t.obstacles_refusal(b) == d[146]
    assert t.REFUSED + t.head_refusal(a) == d[154] and t.REFUSED + t.head_refusal(b) == d[155]
    assert t.HEAD_REFUSAL_END == " Nothing was created."
    assert 'HEAD_REFUSAL_END = " Nothing was created."' in open("tests/test_project.py").read()   # its own literal (A3)
    print("OK: fixtures equal design.md:136-138, :147 and :155-156")
if "readme" in parts:
    readme = " ".join(open("README.md").read().split())
    for n in (169, 177, 184, 190):
        assert readme.count(d[n - 1].strip()) == 1, n
    print("OK: README holds design.md:169, :177, :184 and :190 once each")
EOF
```

### The ast check of project

It proves the placement (D1), that `known_obstacles()` and `new()` are the only
functions changed, that `new()` gains one block of lines between the
shape-only refusal and the `row = choose(...)` line and nothing else, that the
span lane 4 edits (from `parent = Path(args.into ...` through the
existing-destination refusal) is the base's byte for byte, and that
`parent_case()` calls only `is_dir()` and `exists()` (no `open`, no permission
read, no subprocess, no network). `PROJECT=FILE` checks FILE in place of
`project` (mutant M4 must fail it).

```bash
# check: ast-project
# Run: bash specs/006-refuse-non-directory-parent-early/qs.sh ast-project [PROJECT=FILE]
BASE=${BASE:?run through qs.sh}
git show "${BASE}:project" > /dev/null || exit 1
python3 - <(git show "${BASE}:project") "${PROJECT:-project}" <<'EOF'
import ast, difflib, sys
old_src, new_src = open(sys.argv[1]).read(), open(sys.argv[2]).read()
def tops(src):
    tree, out, nodes = ast.parse(src), {"<module>": []}, {}
    for node in tree.body:
        seg = ast.get_source_segment(src, node)
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            out[node.name], nodes[node.name] = seg, node
        else:
            out["<module>"].append(seg)
    return out, nodes, [n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
a, _, _ = tops(old_src)
b, b_nodes, b_names = tops(new_src)
# Only the two helpers are new; nothing is removed; imports and module-level statements are unchanged.
assert sorted(set(b) - set(a)) == ["blocked_parent_sentence", "parent_case"], sorted(set(b) - set(a))
assert not set(a) - set(b), sorted(set(a) - set(b))
assert a["<module>"] == b["<module>"], "an import or module-level statement changed"
changed = sorted(k for k in a if k != "<module>" and a[k] != b[k])
assert changed == ["known_obstacles", "new"], changed
# The helpers sit just above known_obstacles(), above discover().
i = b_names.index("known_obstacles")
assert b_names[i - 2:i] == ["parent_case", "blocked_parent_sentence"], b_names[i - 2:i]
assert i < b_names.index("discover")
# new() gains lines only, and only between the shape-only refusal and the choose() line.
old_new, new_new = a["new"].splitlines(), b["new"].splitlines()
ops = difflib.SequenceMatcher(None, old_new, new_new, autojunk=False).get_opcodes()
assert all(tag in ("equal", "insert") for tag, *_ in ops), [op for op in ops if op[0] not in ("equal", "insert")]
inserts = [(j1, j2) for tag, i1, i2, j1, j2 in ops if tag == "insert"]
assert len(inserts) == 1, inserts
j1, j2 = inserts[0]
assert new_new[j1 - 1].strip() == 'raise Refused("--org, --visibility, --family and --elected-by require --shape.")', new_new[j1 - 1]
assert new_new[j2].strip() == "row = choose(registry(workbenches(args.workbenches)), args)", new_new[j2]
# The span lane 4 edits (the parent resolution through the existing-destination refusal) is byte for byte the base's.
start = next(k for k, l in enumerate(old_new) if l.startswith("    parent = Path(args.into or args.parent"))
end = next(k for k, l in enumerate(old_new) if 'raise Refused(f"Destination already exists: {destination}")' in l)
assert "\n".join(old_new[start:end + 1]) in "\n".join(new_new), "the parent-resolution span changed"
# parent_case() calls only is_dir() and exists(): no open, no permission read, no subprocess, no network.
calls = [n.func for n in ast.walk(b_nodes["parent_case"]) if isinstance(n, ast.Call)]
assert calls and all(isinstance(f, ast.Attribute) and f.attr in ("is_dir", "exists") for f in calls), \
    [ast.dump(f) for f in calls]
print("OK: two helpers just above known_obstacles(); only known_obstacles() and new() changed; new() gains one block,"
      " between the shape-only refusal and choose(); the parent-resolution span unchanged; parent_case() calls only"
      " is_dir() and exists(); imports and module-level statements unchanged")
EOF
```

Tested on scratch copies (research R10): a prototype of D1 passes; it fails for
M1, M2 and M3 below, for a stray line inside the parent-resolution span, and
for an `open()` call in `parent_case()`.

### The ast check of the tests

It proves that no existing module-level statement or member is removed or
changed except the one rewritten test, that `known_obstacle_cases()` and
`test_pty_dry_run_with_an_obstacle_refuses` gain lines only (FR-014, SC-006),
and that exactly 15 test methods are new `[Q2]`.

```bash
# check: ast-tests
# Run: bash specs/006-refuse-non-directory-parent-early/qs.sh ast-tests [NEW_TESTS=15]
BASE=${BASE:?run through qs.sh}
git show "${BASE}:tests/test_project.py" > /dev/null || exit 1
NEW_TESTS=${NEW_TESTS:-15} python3 - <(git show "${BASE}:tests/test_project.py") tests/test_project.py <<'EOF'
import ast, difflib, os, sys
REWRITTEN = {"test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path"}
GROWN = {"known_obstacle_cases", "test_pty_dry_run_with_an_obstacle_refuses"}  # added lines only
old_src, new_src = open(sys.argv[1]).read(), open(sys.argv[2]).read()
def parts(src):
    module, members = [], {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.ClassDef) and node.name == "ProjectTests":
            for item in node.body:
                seg = ast.get_source_segment(src, item)
                members[item.name if isinstance(item, ast.FunctionDef) else seg] = seg
        else:
            module.append(ast.get_source_segment(src, node))
    return module, members
a_mod, a_mem = parts(old_src)
b_mod, b_mem = parts(new_src)
missing = [seg.splitlines()[0] for seg in a_mod if seg not in b_mod]
assert not missing, f"module-level statements changed or removed: {missing}"
assert not set(a_mem) - set(b_mem), f"members removed: {sorted(set(a_mem) - set(b_mem))}"
changed = sorted(k for k in a_mem if a_mem[k] != b_mem[k])
assert set(changed) <= REWRITTEN | GROWN, f"existing members changed: {sorted(set(changed) - REWRITTEN - GROWN)}"
assert set(changed) >= REWRITTEN, "the one rewritten test is unchanged"
for name in GROWN & set(changed):
    removed = [l for l in difflib.unified_diff(a_mem[name].splitlines(), b_mem[name].splitlines(), lineterm="", n=0)
               if l.startswith("-") and not l.startswith("---")]
    assert not removed, (name, removed)
added = sorted(k for k in set(b_mem) - set(a_mem) if k.startswith("test_"))
assert len(added) == int(os.environ["NEW_TESTS"]), (len(added), added)
print(f"OK: one existing test rewritten; {sorted(GROWN & set(changed))} gained lines only;"
      f" {len(added)} new test methods: {added}")
EOF
```

Tested on scratch copies: a plausible change with 15 new methods passes; an
edited assertion, an unchanged rewritten test and a wrong method count each
fail.

### Red first

At the base, the pty runs that the realization ends early wait at a prompt for
`pty_timeout` (20 s): about 14 minutes for all of them `[Q1]` `[Q3]` (research
R6). So the red-first runner (`RF` in the plan) uses a scratch copy and lowers
the timeout for that process only; the committed test keeps 20 s. It judges
each test by its subtests: a red test must be red in exactly the number of
subtests below (skipped socket subtests count toward it), with none passing;
an existing test that gains rows must be red in exactly its new rows; a guard
must be green. Seven tests must also be red for their planned reason, read
from each failure's traceback and message (`maxDiff` is lifted for this
process so that the message holds its whole diff; `flat()` then splits
unittest's diff back into its two sides and joins the quoted pieces into which
pprint wraps a long string, so the verdict does not depend on the length of
the temporary path): N7, N8 and the three
existing tests that gain rows fail on the parent line: the failure shows
sentence (b) expected ("cannot be created because") and today's missing
sentence printed ("does not exist"), and never arises inside
`assert_parent_file_unchanged`; N6 fails
waiting at `Select a generator number` (so its second generator is in place,
which mutant M2 needs); N10 fails because `Type yes to run this plan:` is
asked (not on an error in its helper). A failure that does not match prints
`red for the wrong reason` and counts as not planned. It exits 0 with
`checkpoint as planned`, or 1 with `NOT as planned: [...]`.

With `MUTANT=FILE` the copy runs FILE in place of the base's `project`, and
`RF_MUST_FAIL="TEST ..."` names the tests that must be red: the check then
exits 0 with `mutant caught` when each of them is red, and 1 otherwise (the
mutation checks below).

```bash
# check: red-first
# Run: bash specs/006-refuse-non-directory-parent-early/qs.sh red-first ["TESTS=TEST ..."]   (the tests of one task; by default the whole list)
#      bash specs/006-refuse-non-directory-parent-early/qs.sh red-first MUTANT=FILE "RF_MUST_FAIL=TEST ..."
BASE=${BASE:?run through qs.sh}
S=$(mktemp -d) || exit 1
git archive HEAD | tar -x -C "$S" || exit 1
cp tests/test_project.py "$S/tests/test_project.py" || exit 1   # the tests as they stand now, committed or not
if [ -n "${MUTANT:-}" ]; then cp "$MUTANT" "$S/project"; else git show "${BASE}:project" > "$S/project"; fi || exit 1
cat > "$S/rf.py" <<'EOF'
import os, re, sys, unittest
sys.path.insert(0, "tests")
import test_project
test_project.ProjectTests.pty_timeout = 5
test_project.ProjectTests.maxDiff = None   # assertion messages carry their whole diff, so each reason can be read
# Red at the base, with the number of subtests each must be red in (0: no subtests, red as a whole).
RED = {"test_blocked_parent_by_flag_is_refused_before_the_plan": 24,          # [Q1] [Q3]
       "test_blocked_parent_is_refused_without_a_terminal": 12,               # [Q1] [Q3]
       "test_pty_blocked_parent_by_type_without_yes_is_refused": 12,          # [Q1] [Q3]
       "test_pty_blocked_parent_is_refused_where_ci_is_true": 12,             # [Q1] [Q3]
       "test_pty_blocked_parent_is_refused_for_a_workspace_name": 13,         # [Q1] [Q3]
       "test_pty_single_answer_with_a_blocked_parent_is_refused_at_once": 4,
       "test_pty_triad_answer_below_a_file_leaves_the_file_intact": 2,        # [Q2]
       "test_inproc_triad_answer_below_a_file_leaves_the_file_intact": 2,     # [Q2]
       "test_inproc_parent_broken_while_the_question_waits_is_refused": 0,
       "test_blocked_parent_is_refused_before_later_faults": 3,               # [Q4]
       "test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path": 0}
# Existing tests that gain rows: red in exactly their new rows at the base.
NEW_ROWS = {"[parent below a file]", "[all three with the parent below a file]"}
EXISTING = {"test_pty_triad_answer_with_an_obstacle_refuses": NEW_ROWS,
            "test_inproc_triad_obstacle_runs_nothing": NEW_ROWS,
            "test_pty_dry_run_with_an_obstacle_refuses": {"[parent below a file]"}}
# Guards: green at the base.
GREEN = ["test_inproc_parent_repaired_while_the_question_waits_is_created",
         "test_dangling_link_parent_is_created_as_before",
         "test_earlier_refusals_keep_their_text_with_a_blocked_parent",
         "test_shape_by_flag_keeps_its_parent_refusal_with_a_blocked_parent",
         "test_unwritable_directory_child_passes_dry_run_and_fails_at_creation"]
# Planned reasons: every failure of these tests, whole or subtest, must hold each NEED text and no AVOID text,
# each looked for in flat(failure text).
def flat(text):
    """The failure text with the renderers' line breaks undone, so that a phrase is found wherever pprint (80 columns)
    broke it, which depends on the length of the temporary path. unittest's ndiff of two pformat renderings is split
    back into its two sides (the lines marked "-" or unmarked, the lines marked "+" or unmarked); on each side, and on
    the text itself, a closing quote, whitespace or a newline and an opening quote (pprint's continuation of a long
    string) are removed; then every run of whitespace becomes one space."""
    sides = ["\n".join(line[2:] for line in text.splitlines() if line[:2] in ("  ", mark + " ")) for mark in "-+"]
    return " ".join(" ".join(re.sub(r"""["']\s*\n\s*["']""", "", part).split()) for part in (text, *sides))
B = "cannot be created because"                 # sentence (b): expected, absent at the base
TODAY = "does not exist"                        # the missing-parent sentence the base prints instead
FILE_CHECK = "in assert_parent_file_unchanged"   # a traceback frame of the file check
REASON = {"test_pty_triad_answer_below_a_file_leaves_the_file_intact": ([B, TODAY], [FILE_CHECK]),        # [Q2]
          "test_inproc_triad_answer_below_a_file_leaves_the_file_intact": ([B, TODAY], [FILE_CHECK]),     # [Q2]
          "test_pty_triad_answer_with_an_obstacle_refuses": ([B, TODAY], [FILE_CHECK]),
          "test_inproc_triad_obstacle_runs_nothing": ([B, TODAY], [FILE_CHECK]),
          "test_pty_dry_run_with_an_obstacle_refuses": ([B, TODAY], [FILE_CHECK]),
          "test_pty_single_answer_with_a_blocked_parent_is_refused_at_once": (["Select a generator number"], []),
          "test_inproc_parent_broken_while_the_question_waits_is_refused": (["Type yes to run this plan:"], [])}

class Log(unittest.TestResult):
    """Records every subtest: passed, red, or skipped."""
    def __init__(self):
        super().__init__()
        self.green_subtests, self.red_subtests, self.skipped_subtests = [], [], []
    def addSubTest(self, test, subtest, outcome):
        super().addSubTest(test, subtest, outcome)
        (self.green_subtests if outcome is None else self.red_subtests).append(subtest._subDescription())
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.skipped_subtests.append(test._subDescription() if hasattr(test, "test_case") else "(whole test)")

must_fail = os.environ.get("RF_MUST_FAIL", "").split()
bad, red_tests = [], []
for name in sys.argv[1:] or must_fail or [*RED, *EXISTING, *GREEN]:
    log = Log()
    test_project.ProjectTests(name).run(log)
    whole = [t for t, _ in log.failures + log.errors if not hasattr(t, "test_case")]
    red = bool(whole or log.red_subtests)
    if red:
        red_tests.append(name)
    print(f"{'RED  ' if red else 'GREEN'} {name}: {len(log.red_subtests)} red, {len(log.green_subtests)} passed,"
          f" {len(log.skipped_subtests)} skipped subtests{', red as a whole' if whole else ''}")
    for description in log.red_subtests:
        print("      red", description)
    if must_fail:
        continue
    if name in RED:
        want = RED[name]
        ok = (bool(whole) and not log.red_subtests and not log.green_subtests) if want == 0 else \
            (not whole and not log.green_subtests and len(log.red_subtests) >= 1
             and len(log.red_subtests) + len(log.skipped_subtests) == want)
    elif name in EXISTING:
        ok = not whole and set(log.red_subtests) == EXISTING[name]
    else:
        ok = name in GREEN and not red
    if red and name in REASON:
        need, avoid = REASON[name]
        wrong = [text for _, text in log.failures + log.errors
                 if not all(n in flat(text) for n in need) or any(a in flat(text) for a in avoid)]
        for text in wrong[:1]:
            raised = next((l for l in text.splitlines() if re.match(r"\w+(Error|Exception)\b", l)), text.splitlines()[-1])
            print(f"      red for the wrong reason ({len(wrong)} of {len(log.failures + log.errors)}): {raised[:160]}")
        ok = ok and not wrong
    if not ok:
        bad.append(name)
if must_fail:
    missed = [name for name in must_fail if name not in red_tests]
    print("mutant caught" if not missed else f"mutant NOT caught: {missed}")
    sys.exit(1 if missed else 0)
print("checkpoint as planned" if not bad else f"NOT as planned: {bad}")
sys.exit(1 if bad else 0)
EOF
cd "$S" && python3 rf.py ${TESTS:-}   # TESTS is word-split on purpose: test names hold no spaces or globs
```

Expected: `checkpoint as planned`, exit 0. The whole list takes about four
minutes at `pty_timeout = 5`. A task's verify names its own tests in `TESTS`,
for example, for T2, `bash specs/006-refuse-non-directory-parent-early/qs.sh red-first
"TESTS=test_pty_triad_answer_with_an_obstacle_refuses
test_inproc_triad_obstacle_runs_nothing test_pty_dry_run_with_an_obstacle_refuses"`
(one argument, the names separated by spaces).
The subtest counts follow the givens of research R5: under another answer to
Q1, Q2, Q3 or Q4, change the tagged numbers by R7's rules.

### Mutation checks

V3, in scratch copies only; never commit a mutant. Each of M1 to M3 moves the
plan's three-line head check (plan D1) in a copy of the realized `project`; if
the realization's lines differ from the plan's, make the same move by hand.
Each line of the table is one run of a check, which must exit 0 (the M4 run
must exit 1 on the check, which its trailing test turns into 0):

| Mutant | The move | The run that must exit 0 |
| --- | --- | --- |
| M1 | keep the check in the bench branch, but compute `kind, path = parent_case(parent)` once, right after the existing-destination refusal | `bash specs/006-refuse-non-directory-parent-early/qs.sh red-first MUTANT=M1 "RF_MUST_FAIL=test_inproc_parent_repaired_while_the_question_waits_is_created test_inproc_parent_broken_while_the_question_waits_is_refused"` |
| M2 | move the check after `row = choose(...)` (alternative W2) | `bash specs/006-refuse-non-directory-parent-early/qs.sh red-first MUTANT=M2 "RF_MUST_FAIL=test_blocked_parent_is_refused_before_later_faults test_pty_single_answer_with_a_blocked_parent_is_refused_at_once"` |
| M3 | move the check, dedented, to right after the existing-destination refusal, for every path (alternative W3) | `bash specs/006-refuse-non-directory-parent-early/qs.sh red-first MUTANT=M3 "RF_MUST_FAIL=test_inproc_parent_repaired_while_the_question_waits_is_created test_earlier_refusals_keep_their_text_with_a_blocked_parent test_shape_by_flag_keeps_its_parent_refusal_with_a_blocked_parent"` |
| M4 | add any line inside the parent-resolution span, or an `open(parent)` call in `parent_case()` | `bash specs/006-refuse-non-directory-parent-early/qs.sh ast-project PROJECT=M4; [ $? -eq 1 ]` (the ast check must fail on it with 1; a 2 means the runner did not run it) |

`M1` to `M4` stand for the mutant files' paths, absolute or relative to the
top of the worktree. M1 and M3 were observed on a scratch prototype by direct
probes, and M2 for `nomatch` and the `--workbenches` fault; M2's answer-`2` red
is by reading (research R10).

### OpenSpec

```bash
# check: openspec
# Run: bash specs/006-refuse-non-directory-parent-early/qs.sh openspec [OPENSPEC=/usr/bin/openspec]   (or the openspec in py-bench)
OS=${OPENSPEC:-/usr/bin/openspec}
ONE=$("$OS" validate refuse-non-directory-parent-early --strict 2>&1); RC1=$?
ALL=$("$OS" validate --all --strict 2>&1); RC2=$?
printf '%s\n' "$ONE" "$ALL" | grep -e ' is valid' -e '^Totals:'
[ "$RC1" -eq 0 ] && [ "$RC2" -eq 0 ] \
  && printf '%s\n' "$ONE" | grep -qF "Change 'refuse-non-directory-parent-early' is valid" \
  && printf '%s\n' "$ALL" | grep -q '^Totals: [0-9][0-9]* passed, 0 failed'
```

At `d47e8a4` the totals line reads `Totals: 9 passed, 0 failed (9 items)`.
Without network the telemetry error printed first does not change the exit
status.

### Traceability

`traceability.md` holds one row per scenario of the delta, by requirement and
title, in file order (the 003 precedent's columns: `#`, Requirement, Scenario,
FRs, Tests). `MODE=skeleton` (slice S2) checks the rows and the cells the
skeleton fills; the default (slice V7) also checks that every row names tests
that exist and the two mappings FR-015 fixes. In both modes "No known
obstacle" names feature 003's cell: `test_pty_symbolic_link_to_a_directory_names_no_obstacle`
and `test_pty_no_known_obstacle_names_none`.

```bash
# check: traceability
# Run: bash specs/006-refuse-non-directory-parent-early/qs.sh traceability [MODE=skeleton]
MODE=${MODE:-complete} python3 - <<'EOF'
import os, re
complete = os.environ["MODE"] != "skeleton"
want, req = [], None
for line in open("openspec/changes/refuse-non-directory-parent-early/specs/project-command/spec.md").read().split("\n"):
    if line.startswith("### Requirement: "):
        req = line[len("### Requirement: "):]
    elif line.startswith("#### Scenario: "):
        want.append((req, line[len("#### Scenario: "):]))
record = open("specs/006-refuse-non-directory-parent-early/traceability.md").read()
assert record.startswith("Lane: openRepoProject-1\n"), "the lane line comes first"
rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in record.split("\n") if re.match(r"\| \d+ \|", l)]
assert len(want) == 40 and len(rows) == 40, (len(want), len(rows))
assert [r[0] for r in rows] == [str(n) for n in range(1, 41)], "rows are numbered 1 to 40"
assert [(r[1], r[2]) for r in rows] == want, [(r[1], r[2]) for r in rows if (r[1], r[2]) not in want]
named = {r[2]: re.findall(r"`(test_\w+)`", r[-1]) for r in rows}
no_obstacle = {"test_pty_symbolic_link_to_a_directory_names_no_obstacle", "test_pty_no_known_obstacle_names_none"}
assert no_obstacle <= set(named["No known obstacle"]), named["No known obstacle"]
if complete:
    tests = open("tests/test_project.py").read()
    assert all(named.values()), [s for s, n in named.items() if not n]
    undefined = sorted({n for ns in named.values() for n in ns if f"    def {n}(self" not in tests})
    assert not undefined, undefined
    rewritten = "test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path"
    assert rewritten in named["A single repository taken at the question with a parent blocked by a non-directory"]
    assert rewritten not in named["A single-repository answer is unaffected"]
    assert "test_pty_single_answer_is_unaffected_by_obstacles" in named["A single-repository answer is unaffected"]
print("OK: 40 rows, the delta's requirements and titles in order; 'No known obstacle' names 003's tests"
      + ("; every row names defined tests; FR-015's two mappings hold" if complete else ""))
EOF
```

### Governance record

`[Q5]` The change's `tasks.md` after G1 and after G2 (plan, "G1 and G2 exact
text"). `check_ticks.py` rebuilds the file each step must produce from the
base's copy and the exact text in `plan.md`, and compares it with the file as
it stands. Run with `STAGE=g1` right after the G1 commit and with `STAGE=g2`
right after the G2 commit. Before writing G2, the writer prints the two shas
it needs with the same two `git log` commands as the `G1SHA=` and `FIRSTSHA=`
lines below. "The first implementation commit" is the first commit that
touches `project`, `tests/test_project.py` or `README.md`; commits under
`specs/` (spec, plan, tasks, `qs.sh`, the traceability skeleton) are record
commits, not implementation commits.

```bash
# check: governance
# Run: bash specs/006-refuse-non-directory-parent-early/qs.sh governance STAGE=g1|g2 [OPENSPEC=/usr/bin/openspec]
STAGE=${STAGE:-g1}
F=openspec/changes/refuse-non-directory-parent-early/tasks.md
PLAN=specs/006-refuse-non-directory-parent-early/plan.md
BASE=${BASE:?run through qs.sh}
G=$(mktemp -d) || exit 1
cat > "$G/check_ticks.py" <<'EOF'
import difflib, re, sys
# check_ticks.py PLAN BASE CURRENT g1 | g2 G1SHA FIRSTSHA
# Builds the change's tasks.md that G1 (or G1 then G2) of the plan's "G1 and G2 exact text" must produce from BASE,
# and compares it with CURRENT ("-" prints it instead).
plan, base, current, stage, *shas = sys.argv[1:]
text = open(plan).read()
def span(s, i):
    n = len(s[i:]) - len(s[i:].lstrip("`"))
    j = s.index("`" * n, i + n)
    while s[j + n:j + n + 1] == "`":
        j = s.index("`" * n, j + n + 1)
    body = s[i + n:j]
    if len(body) > 1 and body[0] == " " and body[-1] == " ":
        body = body[1:-1]
    return body, j + n
def bullets(block):
    out = {}
    for line in re.findall(r"^- Line \d+.*(?:\n  After: .*)?", block, re.M):
        number = int(re.match(r"- Line (\d+)", line).group(1))
        if ", before: " in line.split("\n")[0]:
            before, _ = span(line, line.index(", before: ") + 10)
            after, _ = span(line, line.index("\n  After: ") + 10)
            out[number] = ("whole", before, after)
        else:
            i = line.index("change its leading ") + 19
            old, i = span(line, i)
            new, i = span(line, line.index(" to ", i) + 4)
            end, i = span(line, line.index("after its final ", i) + 16)
            added, _ = span(line, line.index("one space and: ", i) + 15)
            out[number] = ("tick", old, new, end, added)
    return out
g1 = bullets(text[text.index("G1 replaces six whole lines"):text.index("G2 replaces one line")])
g2 = bullets(text[text.index("G2 replaces one line"):text.index("This follows feature 003")])
assert sorted(g1) == [16, 20, 31, 36, 37, 38] and sorted(g2) == [21], (sorted(g1), sorted(g2))
lines = open(base).read().split("\n")
def apply(edits, subst=()):
    for number, edit in edits.items():
        line = lines[number - 1]
        if edit[0] == "whole":
            assert line == edit[1], (number, line, edit[1])
            lines[number - 1] = edit[2]
        else:
            _, old, new, end, added = edit
            assert line.startswith(old + " ") and line.endswith(end), (number, line)
            for key, value in subst:
                added = added.replace(key, value)
            lines[number - 1] = new + line[len(old):] + " " + added
apply(g1)
if stage == "g2":
    g1sha, firstsha = shas
    apply(g2, (("G1SHA", g1sha), ("FIRSTSHA", firstsha)))
expected = "\n".join(lines)
assert expected.isascii(), "a non-ASCII character"
if current == "-":
    sys.stdout.write(expected)
    sys.exit(0)
actual = open(current).read()
if actual != expected:
    sys.stdout.writelines(difflib.unified_diff(expected.splitlines(True), actual.splitlines(True), "expected", "actual"))
    sys.exit(1)
print(f"OK: {current} is the base with the {stage.upper()} replacements of {plan}, nothing else")
EOF
git show "${BASE}:$F" > "$G/tasks.base.md" || exit 1
bad=0
want() {   # want EXPECTED GOT WHAT
  [ "$2" = "$1" ] || { printf 'governance: %s: got %s, want %s\n' "$3" "$2" "$1" >&2; bad=1; }
}
if [ "$STAGE" = g1 ]; then
  python3 -I "$G/check_ticks.py" "$PLAN" "$G/tasks.base.md" "$F" g1 || bad=1
  want 1 "$(grep -c '^- \[ \] 2\.2 ' "$F")" "2.2 still open"
  LINES=$(printf '6\t6')
else
  G1SHA=$(git log --reverse --format=%h "$BASE"..HEAD -- "$F" | head -n 1)
  FIRSTSHA=$(git log --reverse --format=%h "$BASE"..HEAD -- project tests/test_project.py README.md | head -n 1)
  { [ -n "$G1SHA" ] && [ -n "$FIRSTSHA" ] && [ "$G1SHA" != "$FIRSTSHA" ] \
    && git merge-base --is-ancestor "$G1SHA" "$FIRSTSHA"; } \
    || { echo "governance: G1 ($G1SHA) is not before the first implementation commit ($FIRSTSHA)" >&2; bad=1; }
  python3 -I "$G/check_ticks.py" "$PLAN" "$G/tasks.base.md" "$F" g2 "$G1SHA" "$FIRSTSHA" || bad=1
  want 1 "$(grep -c '^- \[x\] 2\.2 ' "$F")" "2.2 ticked"
  LINES=$(printf '1\t1')
fi
want 1 "$(grep -c '^- \[x\] 1\.6 ' "$F")" "1.6 ticked"
want 1 "$(grep -c '^- \[x\] 2\.1 ' "$F")" "2.1 ticked"
want 3 "$(grep -c '^- \[ \] 3\.[123] ' "$F")" "3.1 to 3.3 open"
want 0 "$(grep -c 'to be created' "$F")" "lines holding 'to be created'"
want "$F" "$(git diff --name-only HEAD~1 HEAD)" "paths of the last commit"
want "$LINES" "$(git diff --numstat HEAD~1 HEAD -- "$F" | cut -f1,2)" "lines added and removed by the last commit"
"${OPENSPEC:-/usr/bin/openspec}" validate refuse-non-directory-parent-early --strict > /dev/null 2>&1 \
  || { echo "governance: openspec validate failed" >&2; bad=1; }
[ "$bad" -eq 0 ] && echo "governance $STAGE OK"
```

After G1, 1.6 and 2.1 are ticked and 2.2 is still open; after G2, 2.2 is
ticked with its "Met:" line; 3.1 to 3.3 stay open for the lane's landing and
archive steps. Applied to a scratch copy of the file at `d47e8a4`, both
stages passed every part of this check that does not need a commit (research
R14).

### Merge check against PR #33

The lead's step before merging main in (plan, "Other lanes"): this branch's
`project`, README and tests file merge cleanly with #33's head. `HEAD33` is
that head (`git ls-remote origin refs/pull/33/head`), or `origin/main` once #33
is on main; fetch it first if `git cat-file -t "$HEAD33"` does not find it.

```bash
# check: merge-check
# Run: bash specs/006-refuse-non-directory-parent-early/qs.sh merge-check HEAD33=REV   (PR #33's head, or origin/main once #33 is on it)
: "${HEAD33:?set HEAD33 to the head of PR #33 or to origin/main}"
MB=$(git merge-base HEAD "$HEAD33") || exit 1
M=$(mktemp -d) || exit 1
bad=0
for f in project README.md tests/test_project.py; do
  n=$(printf '%s' "$f" | tr / _)
  git show "HEAD:$f" > "$M/ours.$n" && git show "${MB}:$f" > "$M/base.$n" && git show "${HEAD33}:$f" > "$M/theirs.$n" || exit 1
  git merge-file -p "$M/ours.$n" "$M/base.$n" "$M/theirs.$n" > "$M/merged.$n"; rc=$?
  echo "$f: git merge-file exit $rc"
  [ "$rc" -eq 0 ] || bad=1
done
python3 -c 'import ast, sys; ast.parse(open(sys.argv[1]).read())' "$M/merged.project" || bad=1
[ "$bad" -eq 0 ] && echo "merge check OK: HEAD with $HEAD33 over $MB"
```

## Clean up

In the shell that holds the hand-run fixture:

```bash
chmod 755 "$T/locked"
```

Then remove `$T`, `$T.before` and the directories the checks made with
`mktemp -d` (the `suite` check's PyYAML link and export, `red-first`'s scratch
copy, `governance`'s scratch files) by hand. (The lane's agents leave them:
their briefs forbid recursive deletes.)
