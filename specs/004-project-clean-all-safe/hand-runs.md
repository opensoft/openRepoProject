Lane: openRepoProject-2

# Hand runs of feature 004 (T132)

The lead walked quickstart.md's hand runs for User Stories 1 to 9 at a real
terminal on 2026-10-21, from about 09:15Z to 09:36Z. Lead ruling R-50 says
the lead runs them through tmux and no subagent dispatches them.

- Code under test: `project` at e48de37. Every code lane is merged there, and
  its `project` equals c813869's.
- Terminal: a tmux pane (a pseudo-terminal) in the py-bench container, with
  bash 5.2.21 (history expansion off, `set +H`), Git 2.43.0 and Python 3.12.3.
- Fixture: quickstart.md's "Set up a fixture for hand runs (bash)",
  verbatim, except that `T` came from `mktemp -d` under the session's scratch
  directory. The fixture was rebuilt before each story, and before a run that
  needed a fresh one. Paths below write that directory as `$T`, `$T/repo` as
  `$R` and `$T/wt` as `$W`.
- The changes "at the question" in User Story 4 were made from a second
  shell on the same host while the question waited, then `yes` was typed.

Result: every run matched quickstart.md. There is no divergence, so no
defect is recorded against the tasks.

## User Story 1: retire every safe worktree in one run

| Run | Observed | Verdict |
| --- | --- | --- |
| `p clean "$R" --all-safe` | `Selected (3):` a, b, c. `Excluded (6):` main-worktree, locked-worktree, dirty, ignored-local-files (`1 ignored; first: x.cache`), pushed-unmerged, unstarted-branch, each with its next step. Then the `Not protected:` line, and `exit=0` | MATCH |
| `--all-safe --json` | one document: mode `all-safe`, `apply_allowed` true, selected a, b and c, a `plan_digest` | MATCH |
| `--all-safe --apply`, answered `y` | `Remove 3 worktrees, keeping 3 branches? [yes/N]`, then `REFUSED: Cancelled; no command was run.`, `exit=2`; all 9 worktrees remain | MATCH |
| the same, answered `yes` | `removed` a, b and c in that order; `Removed 3; branches kept: a, b, c.`; `exit=0`; the three branches remain | MATCH |
| `--all-safe --apply --yes` again | `No eligible worktrees`, `exit=0`, no question | MATCH |
| `--all-safe --apply < /dev/null` (fresh) | `REFUSED: Standard input is not a terminal; pass --yes to apply this plan.`, `exit=2` (confirmation-required) | MATCH |
| `--all-safe --worktree "$W/a"`; `--all-safe --apply --expect-plan abc` | each `REFUSED` (invalid-arguments), `exit=2`. A logging Git wrapper first on PATH recorded 0 Git children | MATCH |
| digest pinning: a commit on a, then `--apply --yes --expect-plan "$D"` | the fresh plan printed (a now `unpushed`, `Selected (2):`), then `REFUSED: The fresh plan's digest ... differs from --expect-plan ...; nothing was changed.`, `exit=2`; nothing removed | MATCH |
| the same with only `$W/d` changed | the digest held at `D`; the apply removed 3, `exit=0` | MATCH |

## User Story 2: work not proven disposable is never removed

| Run | Observed | Verdict |
| --- | --- | --- |
| `--apply --action remove --worktree "$W/f" --yes` | `REFUSED: Worktree is excluded: unstarted-branch; no commit was made on this branch here since it was created; review, then git worktree remove yourself`, `exit=2`; `$W/f` remains | MATCH |
| c's reflog removed, then emptied; `--all-safe` | `$W/c` under `reflog-unavailable (1): the branch's reflog is missing, expired or undecidable; review, then git worktree remove yourself` | MATCH |
| `b.txt` assume-unchanged plus an edit; remove `$W/b` | `REFUSED: Worktree is excluded: hidden-local-state; review, then remove the worktree yourself`, `exit=2`; the edit survives | MATCH |
| `refs/remotes/origin/a` deleted; `--all-safe --json` | a still selected, `merged-removable`; `upstream_oid`, `ahead` and `behind` null | MATCH |
| main renamed trunk, `origin/HEAD` removed; `p clean "$R"` | `REFUSED: Cannot determine the default branch from the manifest, origin/HEAD, main, or master.`, `exit=2` (no-merge-target, the baseline message) | MATCH |

## User Story 3: a named action gains the batch's checks

| Run | Observed | Verdict |
| --- | --- | --- |
| `--apply --action remove --worktree "$W/a" --yes --json` | one document: `exit_code` 0, one target `removed`, whose `command` is the pinned vector (`git`, the eleven `-c` pins, `-C` ROOT, `worktree remove` PATH); the plan on standard error; branch a kept | MATCH |
| `--apply --action remove --worktree "$W/a" < /dev/null` | `Selected (1):` with `$W/a`; `not-requested (3): name it with --worktree to plan its removal` over `$W/b`, `$W/c` and `$W/f`; the `Not protected:` line; then the confirmation-required refusal, `exit=2` | MATCH |
| `--worktree "$T/nowhere" --yes` | `REFUSED: No unique linked worktree found at $T/nowhere`, `exit=2` (worktree-not-found) | MATCH |
| `--worktree "$W/d" --yes` | `REFUSED: Worktree is dirty; only clean merged worktrees may be removed.`, `exit=2` (target-excluded, the class message) | MATCH |
| from inside `$W/b`, `--worktree "$W/b" --yes` | `REFUSED: Cannot remove the current worktree.`, `exit=2` | MATCH |
| `origin/u` deleted; `--apply --action push --branch u --yes` | `REFUSED: Cannot push u; its upstream origin/u was deleted (remote-gone); review it before it is republished.`, `exit=2`; the remote's u unchanged | MATCH |
| `--apply --action push --branch u --json` | one JSON document with `invalid-arguments` (`--json cannot be combined with --apply; use JSON for the read-only plan.`), `exit=2` | MATCH |

## User Story 4: a change after the plan stops the removal

| Change at the question | Observed | Verdict |
| --- | --- | --- |
| `echo new > "$W/a/new"` | a `refused` (state-changed); b and c `not-attempted` (batch-stopped); `Stopped at $W/a (state-changed). Removed 0 of 3. Not attempted: $W/b, $W/c. Next: project clean $R --all-safe`; `Branches kept: a, b, c.`; `exit=2` | MATCH |
| a commit on b | a `refused` (branch-changed) at the preflight; b and c batch-stopped; nothing removed; `exit=2` | MATCH |
| a commit on main | a `refused` (state-changed) at the preflight; nothing removed; `exit=2` | MATCH |

## User Story 5: every removal ends in a reconcilable record

| Run | Observed | Verdict |
| --- | --- | --- |
| c given an unwritable `sub`; `--all-safe --apply --yes --json` | a and b `removed`. c `failed`, `git-failed`, `exit_status` 255, notes `["orphaned-directory"]`, `registry_entry_present` false, `path_present` true. The document's `exit_code` and the process exit status are both 255, and `$W/c` stays | MATCH |
| Ctrl-C at the question | `Cancelled.`, `exit=130`, nothing removed | MATCH |
| Ctrl-D at the question | `Cancelled.`, `exit=130`, nothing removed | MATCH |

## User Story 6: every run is bounded and says what it omits

| Run | Observed | Verdict |
| --- | --- | --- |
| `p clean "$R" --json` | `report complete`. Limits: `worktree_rows` 256, `targets` 16, `ignored_entries` 64, `status_records` 4096, `ignored_samples` 8. Budget: probe 5, invocation 60, reconciliation reserve 10, removal floor 5, removal ceiling 300, probe concurrency 1 | MATCH |
| 20 more merged worktrees; `--all-safe` | `Selected (16):` a, b, c and m01 to m13, in path order; m14 to m20 under `deferred-target-cap (7): this run removes up to 16; run again: project clean $R --all-safe --apply`; `exit=0` | MATCH |
| `--all-safe --apply --yes`, twice | first run `Removed 16; ...`, `exit=0`; second run removed m14 to m20, `Removed 7; ...`, `exit=0` | MATCH |

## User Story 7: acting on exactly the repository given

| Run | Observed | Verdict |
| --- | --- | --- |
| `p clean "$R/sub"`, `p clean "$W/a"`, `p clean "$T/origin.git"` | each `REFUSED: Not the main worktree of a repository: PATH; pass the repository root.`, `exit=2` (target-not-repository-root) | MATCH |
| `(cd "$W/a" && p clean)` | the report of `$R`, its `repository.root` naming `$R` | MATCH |
| branch develop and a project-manifest naming `origin/develop`; `--json` | `merge_target` `{name: develop, source: manifest, sha: ...}` | MATCH |
| `kind: family-manifest` | `REFUSED: Unexpected kind in $R/project.yaml; expected project-manifest`, `exit=2` (manifest-invalid) | MATCH |

## User Story 8: exact paths and one JSON document per run

| Run | Observed | Verdict |
| --- | --- | --- |
| t1 at a path holding a tab, and t2 at one holding the byte 0xFF; `--all-safe` | the tab path printed `$'$T/wt/tab\u0009here'` and selected. The 0xFF path printed `$'$T/wt/bad\xff'` under `unsupported-path-bytes (1): rename the path to valid UTF-8`, in gate order after main-worktree; `exit=0` | MATCH |
| `--all-safe --json` | that row excluded `unsupported-path-bytes`, with `path_valid_utf8` false | MATCH |
| `--all-safe --apply --yes --json` | standard output parsed as exactly one JSON document; 4 targets removed (a, b, c, t1); the 0xFF path still present | MATCH |

## User Story 9: status, doctor and update share the evidence

| Run | Observed | Verdict |
| --- | --- | --- |
| a fake Git printing `git version 2.35.0`; `p clean "$R"` | `REFUSED: Git 2.35.0 is older than 2.36; clean needs Git 2.36 or later.`, `exit=2` (git-too-old) | MATCH |
| the same; `p status "$R"` | `Git: inspection-error (git-too-old)`, `exit=0` | MATCH |
| the same; `p doctor "$R"` | `ERROR git: git-too-old: Git 2.35.0 is older than 2.36; repository inspection needs Git 2.36 or later.`, `exit=1` | MATCH |
| no Git on PATH; `p doctor "$R"` | `ERROR git: git-unavailable: Git is unavailable (not found); repository inspection needs Git 2.36 or later.`, `exit=1` | MATCH |

## Not walked by hand

quickstart.md assigns these cases to their tests, which the suite runs:
- signals during a removal;
- the 300 s ceiling;
- an exit 0 without removal;
- the residual window;
- the branch race;
- a repository replaced mid-batch;
- the row caps, the deadline and the ignored-file bounds;
- submodules and hidden local state beyond User Story 2's case;
- the flooding, SIGTERM-ignoring and 5,000-record fake Gits;
- the partial clone.

The Git 2.36 floor is T129, and the checks on the realization are T131.
