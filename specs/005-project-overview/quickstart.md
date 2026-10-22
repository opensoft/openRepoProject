Lane: openRepoProject-4

# Quickstart: validating the project overview

A validation guide for the built feature, not an implementation; nothing
here was run at the plan step. The automated tests are the authority:
every delta scenario has at least one test named after it, recorded in
`traceability.md` during implementation. The hand runs below show each user
story once at a real terminal. They are read-only towards everything but
one scratch directory: the overview writes nothing, and the fixtures are
made only under `$F`. Exact text: the
[contract](contracts/project-overview.md); states and exits:
[data-model.md](data-model.md).

## Prerequisites

Python 3.10 or later with PyYAML, Git 2.36 or later, `bash`, run from the
feature worktree (`openRepoProject-worktrees/005-project-overview`). No
network and no credentials are needed; every remote below is a local bare
repository. The permission steps need a user other than root.

## Run the tests

```bash
python3 -m unittest discover -s tests -v                  # whole suite
python3 -m unittest discover -s tests -v -k test_overview_
python3 -m unittest discover -s tests -v -k test_overview_floor_
```

The suite must pass with every test that existed on `main` unchanged
(FR-049).

## The 004-touching changes (lane openRepoProject-2's conditions)

Slice 1's three changes to feature 004's code (research.md R3) are checked
before its pull request is read by lane openRepoProject-2 or
openRepoProject-3; the pull request quotes each result.

```bash
F=$(mktemp -d)                            # a scratch directory
B=$(git merge-base HEAD origin/main)      # the base: main after PR #33
# (a) feature 004's tests and helpers unedited, and the suite green
git diff --stat "$B" HEAD -- tests/test_clean_*.py \
    tests/test_status_doctor_update.py tests/test_project.py \
    tests/clean_support.py tests/launch_project.py     # expect no output
python3 -m unittest discover -s tests -v
# (d) clean's help unchanged; the top-level help gains one line only
mkdir "$F/base" && git show "${B}:project" > "$F/base/project" \
    && chmod +x "$F/base/project"       # same name, so usage lines match
diff <("$F/base/project" clean --help) <(./project clean --help)
diff <("$F/base/project" --help) <(./project --help)
# expect only the subcommand list's new name and the overview's help line
```

(c) is a unit test of the split: `Invocation("clean")` keeps `work_end` 50 s
and `reserve_end` 60 s after its start under the real table, and feature
004's timing tests pass unedited.

(b), the side-by-side run: one script builds each fixture at a fixed path
with fixed `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE`, so that object names
agree between builds, and runs the same commands against
`$F/base/project` and `./project`, the counting wrapper first on `PATH`;
an `--apply` command runs on a fresh build for each. Fixtures: a merged
worktree; a dirty one; an unstarted branch; 17 merged worktrees (the
target cap); 257 registered rows (the report cap); a failed status probe
and a held one (fake Gits); a reflog read and a status probe cut by the
deadline through `tests/launch_project.py --timing=...` (the
deadline-stopped marker); a bare repository. Commands: `clean ROOT --json`,
`clean ROOT --all-safe --json`, `clean ROOT --all-safe --apply --yes
--json`. Compared: exit statuses, `probes` and `operations`, each document
with every `observed_at` masked, and the wrapper's logs with process IDs
and times masked. Every comparison is identical, or the slice stops.

## The Git 2.36 floor run

With a Git 2.36.6 built as feature 004's `git-floor` job builds it, first
on `PATH`:

```bash
git --version          # git version 2.36.6
python3 -m unittest discover -s tests -v \
    -k test_clean_ -k test_status_ -k test_doctor_ -k test_overview_floor_
```

## Set up a fixture (bash)

Every path is under a fresh scratch directory; `HOME` and `PROJECTS_DIR`
point into it, so no real projects directory is read.

```bash
P="$PWD/project"                      # the feature's script
F=$(mktemp -d)
export HOME="$F/home" PROJECTS_DIR="$F/root"
mkdir -p "$HOME" "$PROJECTS_DIR"
g() { git -c user.name=t -c user.email=t@example.invalid \
          -c init.defaultBranch=main "$@"; }
g init -q --bare "$F/origin.git"
g clone -q "$F/origin.git" "$PROJECTS_DIR/atlas" 2>/dev/null
cd "$PROJECTS_DIR/atlas"
g commit -q --allow-empty -m base && g push -q -u origin main
# merged: a published branch with one commit, merged into main
g worktree add -q -b feat "$F/atlas-feat"
(cd "$F/atlas-feat" && g commit -q --allow-empty -m feat \
    && g push -q -u origin feat)
g merge -q --ff-only feat && g push -q origin main
# dirty: a worktree with an untracked file
g worktree add -q -b wip "$F/atlas-wip" && echo x > "$F/atlas-wip/n.txt"
# ignored local file, kept out of #24's cache rules (C-71)
printf 'local.env\n' > .git/info/exclude && touch local.env
cd "$F"
```

Snapshot the fixture before and after each run (PN-14; access times left
out on purpose):

```bash
snap() { find "$F" -path "$F/home" -prune -o \
    -printf '%P %y %m %s %T@ %C@\n' | sort; \
    find "$F" -path "$F/home" -prune -o -type f -print0 | sort -z \
    | xargs -0 sha256sum; }
snap > "$F.before"
```

After every run below, `snap | diff "$F.before" -` prints nothing.

## User Story 1: every local project in one report

```bash
"$P" overview; echo "exit $?"
```

One `atlas` header with its absolute path; the merged `feat` worktree
under `housekeeping` with its path on the next line; `wip` under
`preserve` (`dirty`); a `next` line naming `project clean
'.../root/atlas' --all-safe`; the summary line; exit 0 or 1 by severity
(`dirty` is a warning). Add a symbolic link `atlas-link` to `atlas` in the
root and a second clone under another `--root`: still one row per
repository, and two `atlas` rows for the two clones.

## User Story 2: only what needs attention

```bash
"$P" overview --attention; echo "exit $?"
"$P" overview --strict; echo "exit $?"
```

Informational findings hidden, the same exit as without `--attention`;
`--strict` exits 1 on the `dirty` warning.

## User Story 3: the same verdict as `project clean`

```bash
"$P" overview --json > "$F/o.json"
"$P" clean "$PROJECTS_DIR/atlas" --json > "$F/c.json"
python3 -I -c 'import json,sys
o=json.load(open(sys.argv[1])); c=json.load(open(sys.argv[2]))
a={w["path"]:w["classification"] for p in o["projects"]
   for w in p["worktrees"] or []}
b={w["path"]:w["classification"] for w in c["worktrees"]}
print("equal" if all(a[k]==v for k,v in b.items()) else "DIFFER")' \
    "$F/o.json" "$F/c.json"
```

Prints `equal`.

## User Story 4: a next command to review, never permission

The `next` command is an argument vector naming the canonical root, never
a bare name, never `--apply` or `--yes`. Lock the merged worktree (`git -C
"$PROJECTS_DIR/atlas" worktree lock "$F/atlas-feat"` in a copy of the
fixture): its finding becomes `locked-worktree` and the command falls back
to the read-only form. Delete its reflog file in another copy:
`reflog-unavailable`, `(withheld: ...)` on the `next` line.

## User Story 5: one versioned JSON document

```bash
"$P" overview --json | python3 -I -m json.tool > /dev/null && echo ok
"$P" overview --json --bogus; echo "exit $?"   # usage on stderr, exit 2
```

## User Story 6: bounded, and says what it omitted

A root with 129 directories holding `.project.json`: 128 rows and one
`scan-limit` error, `limit: "candidates"`, `omitted.count: 1`, exit 1.
The deadline, the hung call and the concurrency limits are left to the
tests, whose wrapper holds a chosen child.

## User Story 7: one failure stays in its row

Make `ledger/project.yaml` hold `kind: other`: `ledger` is an error row
(`manifest-invalid`), the other rows complete, exit 1. Replace it with the
byte `0xff`: the same row error, CAUSE `not valid UTF-8 text`, while
`"$P" status "$PROJECTS_DIR/ledger" --json` still refuses with exit 2
(PRSD).

## User Story 8: unusual layouts are named

`git init --separate-git-dir "$F/sep.git" "$PROJECTS_DIR/sep"`: the row's
root comes from its checkout. A bare repository with a linked worktree
under the root: `repository.root` null, its findings withheld with
`target-not-repository-root`. A deleted main worktree:
`main-worktree-missing` with its remedy in the message.

## User Story 9: the merge-target checkout's own health

Commit on `main` without pushing: `unpushed` (preserve, warning) on the
`atlas` checkout, no suggestion of its own. Push it and remove the
upstream with `git branch --unset-upstream`: `unpublished`, since
`origin/main` exists.

## User Story 10: local, read-only and stoppable

```bash
GIT_TRACE="$F/trace" "$P" overview > /dev/null; ls "$F/trace" 2>&1
HOME=rel "$P" overview; echo "exit $?"       # relative-config-path, 2
"$P" overview & sleep 0.2; kill -TERM $!; wait $!; echo "exit $?"
```

No trace file appears (the name is scrubbed); the relative `HOME` refuses
before any Git child; SIGTERM ends the run with 143 and `Cancelled.` on
standard error. The snapshot is unchanged after each.

## User Story 11: exact paths, whatever their bytes

`mkdir "$PROJECTS_DIR/$(printf 'b\xffd')"` holding `.project.json`: its
row's `path_valid_utf8` is false and the human header prints the path in
the `$'...'` form. A directory named with U+202E prints escaped as
`\u202e`.

## The full-length timing (SC-005)

Once, by hand, outside CI: a root of 128 candidates and 512 worktree rows
in all, run under `time`; the run ends within 64 s of its start plus
rendering, and every cut is reported. Governance task 2.1 measured the
caps' worst case at 48.3 s of the 60 s deadline.

## Checks on the realization

```bash
git diff --stat origin/main...HEAD
# Expect only: project; tests/test_overview_*.py; tests/overview_support.py;
# README.md; AGENTS.md (FR-051, only if T123 lands); .github/workflows/
# tests.yml (FR-050, one -k prefix); specs/005-project-overview/.
git diff origin/main...HEAD -- project | grep '^+' | LC_ALL=C grep -nP \
    '[^\x00-\x7F]'                       # expect no output
/usr/bin/openspec validate --all --strict   # 1.6.0 or later
```

Remove the scratch directory `$F` when done.
