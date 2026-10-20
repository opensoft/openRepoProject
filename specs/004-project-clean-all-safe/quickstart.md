Lane: openRepoProject-2

# Quickstart: validating safe batch worktree cleanup

A validation guide, not an implementation. The automated tests are the
authority: every delta scenario has at least one test named after it,
recorded in `traceability.md` during implementation. The hand runs below show
each user story at a real terminal once the feature is built. Exact text:
`design.md` D18 and D14, named by the labels of
[contracts/project-clean.md](contracts/project-clean.md); stages and exit
statuses: [data-model.md](data-model.md).

## Prerequisites

Python 3.10 or later, Git 2.36 or later, `bash`, run from the feature
worktree (`openRepoProject-worktrees/004-project-clean-all-safe`). No network
and no GitHub credentials are needed or used; every remote below is a local
bare repository. The permission steps need a user other than root.

## Run the tests

In the Python workBench (`py-bench`), which mounts the projects tree at the
same path, or in any shell with the prerequisites:

```bash
python3 -m unittest discover -s tests -v                        # whole suite
docker exec py-bench bash -lc \
    "cd '$PWD' && python3 -m unittest discover -s tests -v"     # from the host
python3 -m unittest discover -s tests -v -k test_clean_          # one family
python3 -m unittest discover -s tests -v -k test_status_ -k test_doctor_
```

Expected: every test passes; at `961c405` there are 96, and all but
`test_clean_revalidates_a_worktree_after_confirmation` pass unchanged
(research.md R15). Test names start `test_clean_`, `test_status_`,
`test_doctor_` or `test_update_` followed by the delta scenario's title; an
evidence-model scenario that names no subcommand uses `test_status_`
(research.md R11). Skips, each printing its reason: non-UTF-8 path tests on
macOS (a local run; no CI job runs macOS), permission tests when run as root,
and "The sixteenth scrubbed name on Git 2.36" unless the `git` on PATH is 2.36
to 2.39. Time-bound tests run through `tests/launch_project.py`, which loads
`project`, replaces entries of its timing table with the factor or values each
test names, and calls `main()` in a child process (research.md R10); nothing in
the environment scales `project`'s time.

## The Git 2.36 floor run

The CI job `git-floor` does this with a cached build (research.md R11). By
hand, in a scratch directory outside the repository:

```bash
REPO=$PWD; F=$(mktemp -d); cd "$F"
U=https://mirrors.edge.kernel.org/pub/software/scm/git
SUM=3a54356dd0a6b23d7d0742952d5c86958ad8f797cbe41bd1952bc83ec429ea94
curl -fsSLO "$U/git-2.36.6.tar.xz"
echo "$SUM  git-2.36.6.tar.xz" | sha256sum -c
tar -xJf git-2.36.6.tar.xz && cd git-2.36.6
make -j"$(nproc)" NO_GETTEXT=1 NO_TCLTK=1 NO_PERL=1 NO_PYTHON=1 \
    NO_CURL=1 NO_OPENSSL=1 prefix="$F/install" install >"$F/build.log"
cd "$REPO"
PATH="$F/install/bin:$PATH" git --version
PATH="$F/install/bin:$PATH" python3 -m unittest discover -s tests -v \
    -k test_clean_ -k test_status_ -k test_doctor_
```

Expected: `git version 2.36.6`, then every selected test passes, "The
sixteenth scrubbed name on Git 2.36" among them (it runs only here). The
checksum is kernel.org's published value, the one task 2.2 checked. At
`961c405` the same selection ran 15 tests, OK, in 7.7 s on that build.

## Set up a fixture for hand runs (bash)

```bash
REPO=$PWD; T=$(mktemp -d)
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
export GIT_AUTHOR_NAME=Test GIT_AUTHOR_EMAIL=test@example.invalid
export GIT_COMMITTER_NAME=Test GIT_COMMITTER_EMAIL=test@example.invalid
R="$T/repo"; W="$T/wt"
git init -q --bare "$T/origin.git"
git init -q -b main "$R"
printf '*.cache\n' > "$R/.gitignore"
git -C "$R" add .gitignore && git -C "$R" commit -q -m init
git -C "$R" remote add origin "$T/origin.git"
git -C "$R" push -q -u origin main && git -C "$R" remote set-head origin main
# wt BRANCH [DIR]: a worktree with a commit of its own, published
wt() { git -C "$R" worktree add -q -b "$1" "${2:-$W/$1}" &&
       echo "$1" > "${2:-$W/$1}/$1.txt" && git -C "${2:-$W/$1}" add "$1.txt" &&
       git -C "${2:-$W/$1}" commit -q -m "$1" &&
       git -C "${2:-$W/$1}" push -q -u origin "$1"; }
# merged BRANCH [DIR]: the same, merged into main
merged() { wt "$@" && git -C "$R" merge -q --no-ff -m "merge $1" "$1"; }
merged a; merged b; merged c
wt u                                                  # pushed, not merged
merged d && echo edit >> "$W/d/d.txt"                 # dirty
merged g && touch "$W/g/x.cache"                      # ignored local file
merged l && git -C "$R" worktree lock "$W/l"          # locked
git -C "$R" worktree add -q -b f "$W/f" &&
  git -C "$W/f" push -q -u origin f                   # no commit of its own
git -C "$R" push -q origin main
p() { python3 "$REPO/project" "$@"; echo "exit=$?" >&2; }
```

`exit=` goes to standard error so that standard output can be piped into a
JSON parser. Today's `project clean "$R"` reads `f` and `l` as
`MERGED-REMOVABLE`; after this feature they are kept as `unstarted-branch`
and `locked-worktree`. Rebuild the fixture (a new `T`) before each story.

## User Story 1: retire every safe worktree in one run

| Run | Expected |
| --- | --- |
| `p clean "$R" --all-safe` | "D18 preview layout": `Selected (3):` with `$W/a`, `$W/b`, `$W/c`; `Excluded (6):` grouped by reason in gate order, classes in ladder order (`main-worktree`, `locked-worktree`, `dirty`, `ignored-local-files` with `1 ignored; first: x.cache`, `pushed-unmerged`, `unstarted-branch`), each with its next step ("D18 next steps", and the contract's for `main-worktree`: `  main-worktree (1): never removed by project clean`); "D18 residual-window line"; `exit=0`; nothing changes |
| `p clean "$R" --all-safe --json \| python3 -m json.tool` | one document, `mode: "all-safe"`, `apply_allowed: true`, three `selected`, a `plan_digest` |
| `p clean "$R" --all-safe --apply`, answering `y` | "D18 question" `Remove 3 worktrees, keeping 3 branches? [yes/N]`; `cancelled`, `exit=2`; nothing removed |
| the same, answering `yes` | `$W/a`, `$W/b`, `$W/c` removed in that order; "D18 success line" naming `a, b, c`; `exit=0`; `git -C "$R" branch --list a b c` lists all three |
| `p clean "$R" --all-safe --apply --yes` again | "D18 empty line", `exit=0`, no question |
| `p clean "$R" --all-safe --apply < /dev/null` (fresh fixture) | `confirmation-required`, `exit=2` |
| `p clean "$R" --all-safe --worktree "$W/a"`; `p clean "$R" --all-safe --apply --expect-plan abc` | `invalid-arguments`, `exit=2`, no Git child run |

Digest pinning on a fresh fixture: take `D` from the preview's JSON, then
commit once more on `a` (`echo x >> "$W/a/a.txt"; git -C "$W/a" commit -qam
x; git -C "$R" merge -q --no-ff -m m a`) and run `p clean "$R" --all-safe
--apply --yes --expect-plan "$D"`: the fresh plan prints with a new digest,
`plan-digest-mismatch`, `exit=2`, nothing removed. With only `$W/d` changed
instead, the digest is still `D` and the apply proceeds.

## User Story 2: work not proven disposable is never removed

| Run | Expected |
| --- | --- |
| `p clean "$R" --apply --action remove --worktree "$W/f" --yes` | `target-excluded`, reason `unstarted-branch`, "D18 next steps" text, `exit=2`; `$W/f` remains |
| `rm "$R/.git/logs/refs/heads/c"`, then `p clean "$R" --all-safe` | `$W/c` excluded as `reflog-unavailable`; the same with `: > "$R/.git/logs/refs/heads/c"` |
| `git -C "$W/b" update-index --assume-unchanged b.txt; echo hidden >> "$W/b/b.txt"`, then `p clean "$R" --apply --action remove --worktree "$W/b" --yes` | `target-excluded`, reason `hidden-local-state`, `exit=2`; the edit survives |
| `git -C "$R" update-ref -d refs/remotes/origin/a`, then `p clean "$R" --all-safe` | `$W/a` still selected (`merged-removable`, upstream deleted); `upstream_oid`, `ahead`, `behind` null in JSON |
| `git -C "$R" branch -m main trunk` with no `origin/HEAD` (`git -C "$R" remote set-head origin -d`), then `p clean "$R"` | `no-merge-target` with its baseline message, `exit=2` |

Submodules, sparse checkouts and the other classifier rows are covered by the
tests "Submodules", "Hidden local state" and "Every protected classifier".

## User Story 3: a named action gains the batch's checks

| Run | Expected |
| --- | --- |
| `p clean "$R" --apply --action remove --worktree "$W/a" --yes --json` | one document: the apply result record, one `removed` target whose `command` is the pinned removal vector of the contract, `exit_code: 0`; the plan on standard error; branch `a` kept |
| `p clean "$R" --apply --action remove --worktree "$T/nowhere" --yes` | `worktree-not-found`, `exit=2` |
| `p clean "$R" --apply --action remove --worktree "$W/d" --yes` | `target-excluded`, reason `dirty`, `exit=2` |
| `cd "$W/b"; p clean "$R" --apply --action remove --worktree "$W/b" --yes` | `Cannot remove the current worktree.`, `exit=2` |
| `git -C "$R" update-ref -d refs/remotes/origin/u`, then `p clean "$R" --apply --action push --branch u --yes` | refused, reason `remote-gone`, `exit=2`, no push |
| `p clean "$R" --apply --action push --branch u --json` | `invalid-arguments`, `exit=2` |

## User Story 4: a change after the plan stops the removal

Run `p clean "$R" --all-safe --apply` and, while the question waits, change
the repository from a second shell, then answer `yes`:

| Change at the question | Expected |
| --- | --- |
| `echo new > "$W/a/new"` | `$W/a` `refused` with `state-changed`; `$W/b`, `$W/c` `not-attempted`; "D18 stop block" `Stopped at $W/a (state-changed). Removed 0 of 3. ...`; `exit=2` |
| a commit on `b` | `$W/a` `refused` with `branch-changed` at the preflight; nothing removed; `$W/b`, `$W/c` `not-attempted` with `batch-stopped`; `exit=2` (research.md R16) |
| a commit on `main` | the first target refused with `state-changed` at the preflight; nothing removed; `exit=2` |

The residual window, the branch race and a repository replaced mid-batch need
hooks between steps and are covered by their tests.

## User Story 5: every removal ends in a reconcilable record

| Run | Expected |
| --- | --- |
| `mkdir "$W/c/sub" && echo s > "$W/c/sub/s.txt" && git -C "$W/c" add sub && git -C "$W/c" commit -qm sub && git -C "$W/c" push -q && git -C "$R" merge -q --no-ff -m m c && chmod a-w "$W/c/sub"`, then `p clean "$R" --all-safe --apply --yes --json` | `$W/a`, `$W/b` `removed`; then `$W/c` `failed`, `git-failed`, `exit_status: 255`, `notes: ["orphaned-directory"]`, reconciliation `registry_entry_present: false`, `path_present: true`; `exit=255`; the directory stays (`chmod -R u+w "$W/c"` before cleaning up) |
| Ctrl-C at the question | `Cancelled.`, `exit=130`, nothing removed |
| Ctrl-D at the question | `Cancelled.`, `exit=130` |

Signals during a removal, the 300 s ceiling and an exit 0 without removal
need fake Gits and the launcher; their tests are "A signal during a removal",
"A removal past the hard ceiling" and "Exit 0 without evidence".

## User Story 6: every run is bounded and says what it omits

```bash
p clean "$R" --json | python3 -c 'import json, sys
d = json.load(sys.stdin)
print(d["mode"], d["completeness"], d["limits"], d["budget"])'
for i in $(seq -w 1 20); do merged "m$i"; done
p clean "$R" --all-safe
```

Expected: `report complete` with `worktree_rows: 256` and the budget values
of the contract; then a preview selecting 16 rows (`a`, `b`, `c` and `m01`
to `m13`, by path order) with the "D18 deferral line" for the other seven
(`m14` to `m20`), `exit=0`. `--apply --yes` removes those 16; a second run
removes the seven. Row caps, the deadline and the ignored-file bounds are
covered by "Row cap and planning failures", "Deadline expiry mid-batch" and
"Ignored-file bound".

## User Story 7: acting on exactly the repository given

| Run | Expected |
| --- | --- |
| `mkdir "$R/sub"; p clean "$R/sub"` | `target-not-repository-root`, `exit=2` |
| `p clean "$W/a"`; `p clean "$T/origin.git"` | `target-not-repository-root`, `exit=2` |
| `(cd "$W/a" && p clean)` | the report of `$R`, `root` naming `$R` |
| `git -C "$R" branch develop; printf 'kind: project-manifest\ntracking_branch: origin/develop\nlegs: []\n' > "$R/project.yaml"; p clean "$R" --json` | `merge_target` `{name: "develop", source: "manifest", ...}` |
| `printf 'kind: family-manifest\n' > "$R/project.yaml"; p clean "$R"` | `manifest-invalid`, `exit=2` |

## User Story 8: exact paths and one JSON document per run

```bash
merged t1 "$W/$(printf 'tab\there')"
merged t2 "$W/$(printf 'bad\377')"                     # Linux only
p clean "$R" --all-safe
p clean "$R" --all-safe --apply --yes --json 2>/dev/null | python3 -m json.tool
```

Expected: the tab path printed as `$'.../tab\u0009here'` and selected; the
`\377` path shown with `\xff`, excluded as `unsupported-path-bytes` with
`path_valid_utf8: false`, and still present after the apply; standard output
of the apply parses as exactly one JSON document.

## User Story 9: status, doctor and update share the evidence

```bash
mkdir -p "$T/old"
cat > "$T/old/git" <<FAKE
#!/bin/sh
case " \$* " in *" --version "*) echo "git version 2.35.0"; exit 0;; esac
exec $(command -v git) "\$@"
FAKE
chmod +x "$T/old/git"
PATH="$T/old:$PATH" p clean "$R"
PATH="$T/old:$PATH" p status "$R"
PATH="$T/old:$PATH" p doctor "$R"
mkdir -p "$T/nogit" && ln -s "$(command -v python3)" "$T/nogit/python3"
PATH="$T/nogit" p doctor "$R"
```

Expected: `clean` refuses with `git-too-old`, `exit=2`; `status` prints
`Git: inspection-error (git-too-old)`, `exit=0`; `doctor` reports a `git`
error row naming `git-too-old`, `exit=1`; with no `git` on PATH, `doctor`
reports `git-unavailable`, `exit=1` (research.md R2). The flooding,
SIGTERM-ignoring and 5,000-record fake Gits and the partial clone are covered
by their tests.

## Checks on the realization

```bash
# Added lines are ASCII; expect no output.
git diff -U0 main...HEAD -- project tests README.md AGENTS.md .github |
    grep '^+' | grep -nP '[^\x00-\x7F]'
# Expect only project; under tests/, the new modules tests/test_clean_*.py and
# tests/test_status_doctor_update.py, tests/clean_support.py,
# tests/launch_project.py, and tests/test_project.py (one method and one loader
# line, T046 and T009); README.md; AGENTS.md; .github/workflows/tests.yml;
# specs/004-project-clean-all-safe/ and the change's tasks.md.
git diff --stat main...HEAD
# 1.6.0 or later; the openspec first on some PATHs is 1.2.0.
/usr/bin/openspec validate --all --strict
python3 -m unittest discover -s tests -v 2>&1 | tail -n 3
```

## Clean up

```bash
chmod -R u+w "$T"; rm -rf "$T"
```
