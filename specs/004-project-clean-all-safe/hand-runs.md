Lane: openRepoProject-2

# Hand runs of feature 004 (T132)

The lead of lane openRepoProject-2 walked quickstart.md's hand runs for User
Stories 1 to 9 at a real terminal on 2026-10-22, typing each command into a
tmux pane, as T132 and lead ruling R-50 require (lead ruling R-250). T132's
text and R-50 say that the lead walks these runs through tmux, or Brett Heap
does, and that no subagent dispatches them. The lead's first walk, at
e48de37 on 2026-10-21 from about 09:15Z to 09:36Z, matched every run
(6c84014); this record replaces it, since the code has moved on.

- Code under test: `project` at e69f6ef, a detached checkout. Feature 004's
  head, 8f6fa31, runs the same `project`: between e69f6ef and 8f6fa31 only
  `tests/test_clean_revalidation.py` changed (lane 3's W41 test gaps), and
  `git diff e69f6ef 8f6fa31 -- project` is empty. Since e48de37 the build has
  taken:
  - gate 11, `operation-in-progress` (LQ-14), and gate 12,
    `worktree-only-commits` (LQ-13);
  - the revalidation rules R-171 to R-208;
  - the drain line (R-146 L-f);
  - the HOME refusals (R-202, R-205);
  - the push fix, Q9 B's trace names, Brett Heap's rulings LQ-10 to LQ-15,
    and the fix lanes.
- Terminal: a tmux pane (a pseudo-terminal) in the py-bench container,
  window `openRepoProject-2-pyBench:handruns`. Pane 0 ran the commands;
  pane 1 was the second shell for User Story 4. bash ran with history
  expansion off (`set +H`). Git was 2.43.0 and Python 3.12.3.
- Accounts and times, on 2026-10-22:
  - User Stories 1 to 3 and 6 to 9, from about 12:58Z to 13:16Z, under
    account team-01l;
  - User Stories 4 and 5, from about 13:54Z to 13:57Z, under account
    team-01m.
- Fixture: quickstart.md's "Set up a fixture for hand runs (bash)", the
  block run as it stands from the tree root, so that `REPO=$PWD` names it;
  `T` came from `mktemp -d` under the walk's `TMPDIR`. The fixture was
  rebuilt before each story, and before a run that needed a fresh one. Paths
  below write that directory as `$T`, `$T/repo` as `$R` and `$T/wt` as `$W`.
- Environment: no run may reach the host's real tools or workBenches
  (R-202). Both panes started from `env -i`, through one helper, with HOME,
  PROJECTS_DIR, WORKBENCHES_ROOT, XDG_CONFIG_HOME and TMPDIR inside the
  fixture. WORKBENCHES_ROOT named a fake workBenches with an empty bench
  registry. PATH began with fake owner tools: claude, code, codex, copilot,
  devcontainer, docker, gemini, gh, node, npm, npx, openRepoShape, openspec,
  park, resume, setup-openspeckit, specify and uv, each of which logs its
  call and exits 97. Then came /usr/local/bin, /usr/bin and /bin. The other
  variables were LANG=C.UTF-8, TERM=xterm, SHELL, USER, LOGNAME and
  PYTHONDONTWRITEBYTECODE=1. The fake tools' log stayed empty: no owner tool
  ran. None of these runs is an `update`.
- The changes "at the question" in User Story 4 were typed in pane 1 while
  the question waited in pane 0; then `yes` was typed in pane 0.
- Cross-check: writer D, an opus-xhigh subagent (lead ruling R-237), walked
  the same runs on 2026-10-22 through a pseudo-terminal, from the same
  setup and the same environment helper, and matched 41 of 41. Under R-50
  that walk is a cross-check only, not this record. Each run below agrees
  with its row there. Writer D also ran e48de37's `project` on fresh
  fixtures from the same setup: 115 commands, of which, once digests, object
  names, times and inode numbers were masked, 87 printed the same output.
  The other 28 differ in three ways only, and the rows below do not repeat
  them:
  - the `Not protected:` line's text: at e48de37 it read "ignored files
    created or index flags set after the last check", and LQ-14 (2405880)
    and LQ-13 (8ae0bb5) added the middle two causes;
  - the planning probes and Git children: a plain `--all-safe` preview
    spawned 21 Git children where e48de37 spawned 17, and its JSON `probes`
    read estimated 42, performed 21 where e48de37's read 35 and 17 (LQ-11's
    6b83a8e adds 1 and 1, LQ-13's 8ae0bb5 adds 6 and 3); and the pinned
    vector of a removal holds twelve `-c` pins where e48de37's held ten,
    LQ-10's `core.trustctime=true` and `core.checkStat=default` (d1ef33e)
    being the two added (lead ruling R-174, L-2);
  - each removal target's `probes_performed`: 6, where e48de37 gave 5,
    because LQ-13's 8ae0bb5 adds the `refs/worktree` read to revalidation.
- Codes: the lead read the human output, which names a refusal by its
  message. The refusal codes in parentheses below are quickstart.md's, which
  writer D's `--json` pass read from each document's `refusals[].code` on
  fresh fixtures. Push refuses `--json` with `--apply`, so remote-gone's
  code is read from its message.

Result: every run matched quickstart.md, 41 of 41. Nothing diverges and
nothing is NOT DONE, so no defect is recorded against the tasks. No run
reaches gates 11 and 12, the revalidation rules R-171 to R-208, the drain
line or the HOME refusals as a reason; what the walk shows of them is noted
in the rows and under "Not walked by hand".

Note, 2026-10-22: writer E's next-step changes (lead ruling R-259) brought
004's head to d764c26, whose `project` prints lane 3's W52 and W59 texts,
which e69f6ef's does not. The lead walked User Story 1's first run
(`--all-safe`) and User Story 2's first two runs again at d764c26, in the
tmux window `openRepoProject-2-pyBench:handruns`, from 14:43Z to 14:48Z on
2026-10-22, under account team-01m. All three MATCH with the new texts,
which the two User Story 2 rows below quote: the `unstarted-branch` refusal
of `$W/f` and the `reflog-unavailable` group of `$W/c` each end ` (--force
if it holds a submodule)`. F-6 is not exercised by these fixtures, because
the main worktree's row there is `PROTECTED-DEFAULT`. The other rows were
walked at e69f6ef and are unchanged, so a plan they print lists
`unstarted-branch` with that commit's next step, not the new one.

## User Story 1: retire every safe worktree in one run

| Run | Observed | Verdict |
| --- | --- | --- |
| `p clean "$R" --all-safe` | `Selected (3):` a, b, c. `Excluded (6):` main-worktree, locked-worktree, dirty, ignored-local-files (`1 ignored; first: x.cache`), pushed-unmerged, unstarted-branch, each with its next step. Then the `Not protected:` line, which reads `Not protected: ignored files created, index flags set, operations started or worktree-only commits made after the last check, and any change after Git's own check.`, and `exit=0` | MATCH (re-run at d764c26) |
| `--all-safe --json`, through `python3 -m json.tool` | one document: mode `all-safe`, `apply_allowed` true, `completeness` complete, selected a, b and c, a 64-character `plan_digest`, no refusals; its `probes` read estimated 42, performed 21 | MATCH |
| `--all-safe --apply`, answered `y` | the plan, `Remove 3 worktrees, keeping 3 branches? [yes/N]`, then `REFUSED: Cancelled; no command was run.`, `exit=2`; nothing removed | MATCH |
| the same, answered `yes` | `removed` a, b and c in that order; `Removed 3; branches kept: a, b, c.`, then the `Not protected:` line again; `exit=0`; `branch --list` shows a, b and c | MATCH |
| `--all-safe --apply --yes` again | the plan's `Excluded (6):`, then `No eligible worktrees`, `exit=0`, no question | MATCH |
| `--all-safe --apply < /dev/null` (fresh) | the plan, then `REFUSED: Standard input is not a terminal; pass --yes to apply this plan.`, `exit=2` (confirmation-required); all 9 worktrees remain | MATCH |
| `--all-safe --worktree "$W/a"`; `--all-safe --apply --expect-plan abc` | `REFUSED: --all-safe cannot be combined with --action, --branch or --worktree.` and `REFUSED: --expect-plan takes 64 lowercase hexadecimal characters.`, each `exit=2` (invalid-arguments). A logging Git wrapper first on PATH counted 0 Git children for each | MATCH |
| digest pinning: a commit on a and a merge into main, then `--apply --yes --expect-plan "$D"` | the fresh plan printed (`Selected (2):`), then `REFUSED: The fresh plan's digest ... differs from --expect-plan ...; nothing was changed.`, `exit=2` (plan-digest-mismatch); all 9 worktrees remain | MATCH |
| the same with only `$W/d` changed (`echo more >> "$W/d/d.txt"`) | the digest held at `D`; the apply removed 3, `Removed 3; branches kept: a, b, c.`, `exit=0` | MATCH |

## User Story 2: work not proven disposable is never removed

| Run | Observed | Verdict |
| --- | --- | --- |
| `--apply --action remove --worktree "$W/f" --yes` | the plan, with `not-requested (3)` over a, b and c, then `REFUSED: Worktree is excluded: unstarted-branch; no commit was made on this branch here since it was created; review, then git worktree remove yourself (--force if it holds a submodule)`, `exit=2` (target-excluded); `$W/f` remains | MATCH (re-run at d764c26) |
| c's reflog removed, then emptied; `--all-safe` | each time `Selected (2):` a, b, and `$W/c` under `reflog-unavailable (1): the branch's reflog is missing, expired or undecidable; review, then git worktree remove yourself (--force if it holds a submodule)`; `exit=0` | MATCH (re-run at d764c26) |
| `b.txt` assume-unchanged plus an edit; remove `$W/b` | `REFUSED: Worktree is excluded: hidden-local-state; review, then remove the worktree yourself`, `exit=2` (target-excluded); the edit survives | MATCH |
| `refs/remotes/origin/a` deleted; `--all-safe`, then `--all-safe --json` | a still selected; in JSON `merged-removable`, upstream `origin/a`, and `upstream_oid`, `ahead` and `behind` null | MATCH |
| main renamed trunk, `origin/HEAD` removed; `p clean "$R"` | `REFUSED: Cannot determine the default branch from the manifest, origin/HEAD, main, or master.`, `exit=2` (no-merge-target, the baseline message) | MATCH |

## User Story 3: a named action gains the batch's checks

| Run | Observed | Verdict |
| --- | --- | --- |
| `--apply --action remove --worktree "$W/a" --yes --json`, standard output to a file | one document: `exit_code` 0, one target at stage `removed`, `probes_performed` 6; its `command` is the pinned vector (`git`, twelve `-c` pins, `-C` ROOT, `worktree remove` PATH). The pins are `status.showUntrackedFiles=normal`, `core.untrackedCache=false`, `core.fsmonitor=false`, LQ-10's `core.trustctime=true` and `core.checkStat=default`, and the seven protocol pins. The plan went to standard error; branch a kept | MATCH |
| `--apply --action remove --worktree "$W/a" < /dev/null` (fresh) | `Selected (1):` with `$W/a`; `not-requested (3): name it with --worktree to plan its removal` over `$W/b`, `$W/c` and `$W/f`; the `Not protected:` line; then the confirmation-required refusal, `exit=2`; nothing removed | MATCH |
| `--worktree "$T/nowhere" --yes` | `REFUSED: No unique linked worktree found at $T/nowhere`, `exit=2` (worktree-not-found) | MATCH |
| `--worktree "$W/d" --yes` | `REFUSED: Worktree is dirty; only clean merged worktrees may be removed.`, `exit=2` (target-excluded, the class message) | MATCH |
| from inside `$W/b`, `--worktree "$W/b" --yes` | the plan with `$W/b` under `merged-current (1)`, then `REFUSED: Cannot remove the current worktree.`, `exit=2` (target-excluded) | MATCH |
| `origin/u` deleted; `--apply --action push --branch u --yes` | `REFUSED: Cannot push u; its upstream origin/u was deleted (remote-gone); review it before it is republished.`, `exit=2`; the remote's u unchanged | MATCH |
| `--apply --action push --branch u --json` | one JSON document refusing with `invalid-arguments` (`--json cannot be combined with --apply; use JSON for the read-only plan.`), `exit=2` | MATCH |

## User Story 4: a change after the plan stops the removal

| Change at the question | Observed | Verdict |
| --- | --- | --- |
| `echo new > "$W/a/new"` | a `refused` (state-changed); b and c `not-attempted` (batch-stopped); `Stopped at $W/a (state-changed). Removed 0 of 3. Not attempted: $W/b, $W/c. Next: project clean $R --all-safe`; `Branches kept: a, b, c.`; `exit=2`; all 9 worktrees remain | MATCH |
| a commit on b (`echo y >> "$W/b/b.txt" && git -C "$W/b" commit -qam y`) | a `refused` (branch-changed) at the preflight, for b's change; b and c batch-stopped; nothing removed; `exit=2` | MATCH |
| a commit on main (`git -C "$R" commit -q --allow-empty -m main2`) | a `refused` (state-changed) at the preflight; b and c batch-stopped; nothing removed; `exit=2` | MATCH |

## User Story 5: every removal ends in a reconcilable record

| Run | Observed | Verdict |
| --- | --- | --- |
| c given an unwritable `sub`; `--all-safe --apply --yes --json` | a and b `removed`. c `failed`, `git-failed`, `exit_status` 255, notes `["orphaned-directory"]`, `registry_entry_present` false, `path_present` true. Standard error ends `Stopped at $W/c (git-failed). Removed 2 of 3. Not attempted: none. Next: project clean $R --all-safe` and `Branches kept: a, b, c.`. The document's `exit_code` and the process exit status are both 255, and `$W/c` stays | MATCH |
| Ctrl-C at the question | `Cancelled.`, `exit=130`; all 9 worktrees remain | MATCH |
| Ctrl-D at the question | `Cancelled.`, `exit=130`; all 9 worktrees remain | MATCH |

## User Story 6: every run is bounded and says what it omits

| Run | Observed | Verdict |
| --- | --- | --- |
| `p clean "$R" --json`, through quickstart's script | `report complete`. Limits: `worktree_rows` 256, `targets` 16, `ignored_entries` 64, `status_records` 4096, `ignored_samples` 8. Budget: probe 5, invocation 60, reconciliation reserve 10, removal floor 5, removal ceiling 300, probe concurrency 1 | MATCH |
| 20 more merged worktrees; `--all-safe` | `Selected (16):` a, b, c and m01 to m13, in path order; m14 to m20 under `deferred-target-cap (7): this run removes up to 16; run again: project clean $R --all-safe --apply`, with no drain line under it, since the 16 rows ahead are selected, not excluded by a later gate; `exit=0` | MATCH |
| `--all-safe --apply --yes`, twice | first run `Removed 16; ...`, `exit=0`; second run removed m14 to m20, `Removed 7; branches kept: m14 ... m20.`, `exit=0` | MATCH |

## User Story 7: acting on exactly the repository given

| Run | Observed | Verdict |
| --- | --- | --- |
| `p clean "$R/sub"`, `p clean "$W/a"`, `p clean "$T/origin.git"` | each `REFUSED: Not the main worktree of a repository: PATH; pass the repository root.`, `exit=2` (target-not-repository-root) | MATCH |
| `(cd "$W/a" && p clean)` | the report of `$R` (`Cleanup plan for $R`, `Report: complete`), `$W/a` as `MERGED-CURRENT`; with `--json`, `root` and `repository.root` name `$R` | MATCH |
| branch develop and a project-manifest naming `origin/develop`; `--json` | `merge_target` `{name: develop, source: manifest, sha: ...}`, the sha 40 characters | MATCH |
| `kind: family-manifest` | `REFUSED: Unexpected kind in $R/project.yaml; expected project-manifest`, `exit=2` (manifest-invalid) | MATCH |

## User Story 8: exact paths and one JSON document per run

| Run | Observed | Verdict |
| --- | --- | --- |
| t1 at a path holding a tab, and t2 at one holding the byte 0xFF; `--all-safe` | the tab path printed `$'$T/wt/tab\u0009here'` and selected. The 0xFF path printed `$'$T/wt/bad\xff'` under `unsupported-path-bytes (1): rename the path to valid UTF-8`, in gate order after main-worktree; `exit=0` | MATCH |
| `--all-safe --json` | the 0xFF row excluded `unsupported-path-bytes`, with `path_valid_utf8` false; the tab row selected, `path_valid_utf8` true | MATCH |
| `--all-safe --apply --yes --json`, through `python3 -m json.tool` | standard output parsed as exactly one JSON document; 4 targets removed (a, b, c, t1), `exit_code` 0; the 0xFF path still present | MATCH |

## User Story 9: status, doctor and update share the evidence

| Run | Observed | Verdict |
| --- | --- | --- |
| a fake Git printing `git version 2.35.0`; `p clean "$R"` | `REFUSED: Git 2.35.0 is older than 2.36; clean needs Git 2.36 or later.`, `exit=2` (git-too-old) | MATCH |
| the same; `p status "$R"` | `Git: inspection-error (git-too-old)`, `exit=0` | MATCH |
| the same; `p doctor "$R"` | the row's own `ERROR $R: inspection-error (git-too-old): ...`, then `ERROR git: git-too-old: Git 2.35.0 is older than 2.36; repository inspection needs Git 2.36 or later.`; `exit=1` | MATCH |
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

quickstart.md has no hand run for the behaviour built since e48de37, and no
row here takes those reasons. Their tests are:
- gate 11 (`operation-in-progress`) and gate 12 (`worktree-only-commits`):
  T063 and T083;
- the revalidation rules R-171 to R-208, a read that decides nothing giving
  `state-changed`, and the revalidation reads cut at the work deadline
  (R-241): T083, T084, T098 and T099;
- the drain line: T100;
- the HOME and configuration-path refusals: T048 and T114.

The walk shows these behaviours only in passing: the `Not protected:` line
and the probe counts of User Story 1, and `probes_performed` 6 in User
Story 3. User Story 6's preview prints no drain line, because the 16 rows
ahead of the deferred ones are selected.
