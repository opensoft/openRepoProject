# Batch Cleanup of Eligible Worktrees — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Extend the current explicit worktree-removal action to retire a bounded set of eligible linked worktrees through one fresh identity-checked plan, one shared deadline-bounded mutation seam, and reconcilable per-target results.
Topics: project-maintenance, batch-cleanup, project-clean, project-clean-worktree-removal
Repository context: opensoft/openRepoProject; explicit cleanup within one Git repository.
Captured: 2026-09-11

## Possible feats

- A repository-scoped `clean --all-safe` plan and explicit batch apply that shares one identity-checked, deadline-bounded worktree-removal seam with the existing single-target `remove` action.

## Focus and baseline

The proposed batch command reduces repeated selection and confirmation when
several worktrees are already eligible for cleanup. It does not make new
classes of work eligible. Every command, flag, and output in this document is
an illustrative design sketch, not an installed interface; the contracts
around them (types, enums, units, exit codes, and orderings) are nevertheless
stated precisely so that a later proposal can adopt or reject them as written.

This revision, made on 2026-10-07, resolves the batch-side findings that the
2026-09-11
[design-fix handoff](next-session-project-maintenance-fix-handoff.md)
recorded: the safety boundary, reconcilable execution and interruption,
bounded and shared probe work, the repository and JSON contracts, and the
batch acceptance scenarios.

The design contract baseline is `a040790`. `origin/main` is now `d7f6b0e`,
which merged PR #8 (feature 002, "offer the Triad first in `project new`")
on 2026-10-08. Before it, `da33d92` merged PR #7 (this packet) on
2026-10-07, PR #4 archived the completed OpenSpec changes and promoted their
specs to `openspec/specs/`, and PR #5 (merged 2026-10-07T10:02Z) added the
`prefer-triad-in-project-new` OpenSpec proposal under `openspec/changes/`.
PR #8 added about 141 lines to `project`, all in `choose()` and `new()`, and
1,163 lines to `tests/test_project.py`; the cleanup, status, doctor, and
update paths are unchanged in content but sit about 141 lines lower, so every
`project` line citation stays pinned at `a040790`, whose `project` is
byte-identical through `da33d92`. The
governing cleanup specification is `openspec/specs/project-clean/spec.md`
with `openspec/specs/project-clean-review-safety/spec.md`. That contract has
separate `remove` and `delete-branch` actions: removing a worktree leaves its
local branch intact, and branch deletion requires a later explicit action.
The `cleanup` branch (PR #2, closed unmerged on 2026-10-07; branch retained
on origin at `bb91a49`) contains unmerged changes in `5fc2b51` (paired
branch retirement), `acf0133` (doctor repository health), `80fdef3`
(health-warning fixes and regressions), `1789ad9` (disposable cache
handling), `09af8c8` (remote merge status), and `bb91a49` (cache deletion
hardening). `12db36a` is review closure only.

Baseline facts this design builds on: `clean` resolves its target with
`discover`, builds `cleanup_report`, and already runs
`git -C <root> worktree remove <path>` from the resolved repository root.
After confirmation, `require_unchanged_cleanup_state` recomputes the whole
report and compares `cleanup_signature`: `path`, `branch`, `head`, `present`,
`dirty`, `ignored_files`, `upstream`, `ahead`, `behind`, `remote_present`,
`merged_into_target`, `current`, and `classification`, plus `target_branch`.
`Refused` and `OSError` exit 2, a keyboard interrupt or end of input exits
130, `--json` with `--apply` is refused, and a worktree row's
`ignored_files` is an integer count or `null`. Only the children run through
`probe()` have a timeout, a fixed 15 s; the `push`, `remove`, and
`delete-branch` children run through `execute()` have none, and the run as
a whole has no deadline.

This MVP deliberately targets the current contract. It batches worktree
removal only. It does not silently depend on paired branch retirement or cache
disposal from the cleanup branch. If a future proposal adopts either
extension, it must update the governing cleanup specification and add the
extension's failure and recovery contract first. The PR #2 decision record
requires a paired-retirement proposal to be written as a MODIFIED
requirement on `project-clean`, because it changes the governed `remove`
action, which PR #2's change did not declare.

## User interface and selection

```sh
project clean /home/user/projects/Atlas --all-safe
project clean /home/user/projects/Atlas --all-safe --json
project clean /home/user/projects/Atlas --all-safe --apply
project clean /home/user/projects/Atlas --all-safe --apply --yes \
  --expect-plan <plan_digest>
```

`--all-safe` without `--apply` prints a read-only, advisory plan. `--apply`
builds its own fresh plan, prints it, and asks the user to confirm the exact
listed worktrees and their retained local branches. `--yes` accepts that
fresh plan for scripted use, and the optional `--expect-plan` makes the
acceptance conditional on the fresh plan matching an earlier preview; its
value must be 64 lowercase hexadecimal characters. Without `--apply`,
`--json` stays read-only, matching the existing interface; with `--apply` it
is accepted for `--all-safe` and `--action remove` only and prints the apply
result record defined below ("Machine-readable apply results"), and with
`--action push` or `delete-branch` it stays refused. `--all-safe` cannot be
combined with `--action`, `--branch`, or `--worktree`, and `--expect-plan`
requires `--all-safe --apply`; a violation is `invalid-arguments` with exit 2,
so scope is never ambiguous.

The target is normally the canonical repository root that the overview
suggests; "Command directory and repository resolution" defines how every
argument form resolves to one repository identity.

"All" means every eligible linked worktree of one resolved Git repository,
under two hard caps per run: at most 128 worktree rows (every registry
entry, the main worktree included, except a bare repository's first record,
a later extension) are inspected, and at most 16 targets are selected. "Cap
arithmetic" states the rule, row cap first and target cap second, that
yields both. If the row cap or the deadline is reached, the plan is
incomplete and apply is refused. If more than 16 rows pass every gate before
the two index gates (`contains-submodule` and `hidden-local-state`), the
plan selects the first 16 in canonical order, lists the rest in `excluded`
as `deferred-target-cap` with the next command, and apply is allowed;
re-running drains the backlog 16 at a time, and the fresh plan and
revalidation are unchanged. Plain read-only `project clean`, with or without
`--json`, runs as `mode: "report"` under the same deadline, with the same
completeness fields, `completeness` and `omitted`, but caps its worktree
rows at 256, because it spawns no revalidation and no removal (see "Cap
arithmetic"); above 256 rows the report is incomplete.

It does not mean all projects in a folder, family members, mounted spec/code
legs, pinned member copies, or independent clones. Inspection from a family or
assembly root must not silently broaden retirement to child repositories.

The plan lists selected entries and excluded entries with reasons. An empty
eligible set prints "No eligible worktrees" and returns 0 without prompting.
`selected` and `excluded` are sorted by raw path bytes, which is code-point
order for UTF-8 paths, and that canonical order is the execution order. A
worktree registered after the plan is frozen is never added.

## Eligibility and merge-target terminology

The baseline `merged-removable` classification is a prerequisite, and batch
gates add to it. A worktree is selected only when all of these hold:

- It is a present, linked (not the main), non-current worktree that is clean
  and on a named branch other than the merge target.
- Its exact branch tip is an ancestor of the merge target's recorded SHA.
- Its upstream state is known and acceptable under the current classifier:
  an upstream is configured, its remote-tracking ref exists, and ahead and
  behind are both 0.
- `ignored_files` is exactly 0 and `ignored_files_truncated` is false.
- Git reports no `locked` flag for it.
- Its branch has a commit of its own (`unstarted-branch`, below).
- Its path is valid UTF-8 and its worktree-admin registration agrees in both
  directions (see "Safety boundary").
- Its index holds no gitlink (mode `160000`) entry, and its admin directory
  `<common_dir>/worktrees/<admin_id>` holds no `modules` entry.
- Its index flags no entry assume-unchanged or skip-worktree.

These two index gates are checked last. The first exists because Git 2.43
refuses, with exit status 128, to remove a worktree that holds a populated
submodule or whose admin directory holds `modules`, where a linked worktree's
submodule repositories live, even after `submodule deinit`; without the gate
such a row would be selected, refused by Git, and selected again by every
later plan, so every batch would stall on it. Git does remove a worktree whose
gitlink was never populated, but the gate excludes every gitlink, which fails
closed. The second exists because Git's status, and therefore both the
combined probe and Git's own pre-removal check, skips files whose index entry
carries either flag, so edits to such files are invisible and would be
deleted. The `modules` check and the hidden-state probe that apply both gates
("Worktree-specific probes") run only for rows that pass every other gate, and
the probe runs inside the row's own worktree. A sparse checkout marks its
omitted files skip-worktree, so a sparse worktree is excluded as well, which
fails closed; so is every worktree of a repository with
`core.ignoreStat=true`, because Git then marks assume-unchanged each entry it
writes, those of `git add` and of a new worktree's checkout included. The
overview does not run this probe, so the batch may exclude a row that the
overview suggested; the plan lists that exclusion.

The `unstarted-branch` gate excludes a row whose branch has no commit of
its own: its head equals the merge-target SHA, or its head is an ancestor of
the target and the branch's creation reflog entry shows no commit since
creation; a missing reflog fails closed, excluded with the reason stated. At
`a040790` such a row, for example one made by `git worktree add -b x` and
pushed with `git push -u` before any commit, classifies `merged-removable`.

Each excluded row carries one `reason`: the first failing gate in the fixed
order `main-worktree`, `unsupported-path-bytes`, `registration-mismatch`,
`locked-worktree`, `unstarted-branch`, then the row's baseline
classification when that is not `merged-removable` (`stale-worktree`,
`protected-default`, `inspection-error`, `dirty`, `ignored-local-files`,
`detached`, `unpublished`, `remote-gone`, `review-required`, `diverged`,
`remote-ahead`, `unpushed`, `merged-current`, or `pushed-unmerged`), then
`not-requested` for an eligible row other than the named one in
single-target mode, then `deferred-target-cap` for an eligible row beyond
the first 16, then `contains-submodule`, and last `hidden-local-state`. A
path that is not
valid UTF-8 is excluded because neither the confirmation text nor the JSON
plan can show the user exactly what would be removed. `review-required`
stays in the shared classifier as a defensive branch only: under the shared
evidence model a failed probe leaves its values `null` instead, so no Git
state reaches it.

Use `merge target` as the one canonical term for the local branch whose tip
proves ancestry. Its record is `merge_target: {name, source, sha}`, with
`source` one of `manifest`, `origin-head`, `main`, or `master`. Resolution
order is unchanged from the baseline, and so are its two `origin/` strips: a
manifest `tracking_branch`, minus any `origin/` prefix, so that
`origin/develop` names `refs/heads/develop`; the local branch
`refs/heads/<b>`, where `<b>` is the `%(symref)` of
`refs/remotes/origin/HEAD`, which prints `refs/remotes/origin/<b>`, with that
`refs/remotes/origin/` prefix removed; `main`; then `master`. The manifest is
read at `repository.root`; a bare repository has no manifest candidate, and a
manifest that cannot be read or has the wrong kind refuses with
`manifest-invalid`. The first candidate that exists as a local branch wins,
and `sha` is its tip when the plan is built. When the manifest and
`origin/HEAD` name different existing branches, the manifest wins, `source`
is `manifest`, and the plan carries an informational `merge-target-conflict`
note, the same code the overview reports as a finding. When no candidate
exists, the batch refuses with code `no-merge-target` and exit 2 before any
mutation. `default branch` is a human-facing synonym only. `upstream` or
`tracking ref` means the feature branch's configured remote-tracking ref, a
separate piece of evidence.

Preserve dirty, detached, unpublished, unpushed, remote-gone, remotely ahead,
diverged, current, merge-target, locked, submodule-holding, hidden-state, or
uncertain worktrees. An inspection failure for any worktree row
(classification `inspection-error`, which includes an unreadable path and a
broken registration) makes a batch plan incomplete and blocks its apply; in
single-target removal it blocks only when it is the named target's own row,
and is otherwise a non-blocking omission ("One mutation seam"). An ordinary,
fully understood exclusion does not block other eligible targets. Do not
prune stale worktree metadata as a side
effect.

Local ancestry is the only removal proof in this MVP. GitHub or remote-target
merge evidence is outside the batch gate. A squash merge generally does not
put the original branch tip into local merge-target ancestry, so such a branch
stays excluded with a clear reason. Supporting squash-merge retirement would
require a separate preservation/equivalence design.

## Safety boundary

### Identity

A path string alone is never an identity. The plan records these objects,
using the packet's shared field names:

| Object | Fields | Source |
| --- | --- | --- |
| `repository` | `root`, `common_dir`, `dev`, `ino` | realpath of the main worktree's `rev-parse --show-toplevel` (`null` for a bare repository); realpath of `rev-parse --git-common-dir`; `os.lstat` (no follow) of `common_dir` |
| worktree | `path`, `dev`, `ino`, `admin_id` | realpath of the entry in `worktree list --porcelain -z`; `os.lstat` of `path`; the `<id>` in the worktree's `.git` file |
| branch evidence | `branch`, `head`, `upstream`, `upstream_oid`, `ahead`, `behind` | the registry entry and one ref listing |
| `merge_target` | `name`, `source`, `sha` | the resolution order above |

The main worktree is the first record of the registry listing, and the
command directory is `repository.root`. A bare repository has no main
worktree, so its `root` is `null`: `rev-parse --show-toplevel` fails there,
and the identity probe asks only for `--git-common-dir`. The MVP refuses a
bare repository in every `clean` mode with `target-not-repository-root` and
exit 2, whichever argument form reaches it: an absolute path to the bare
directory or to a linked worktree, or a relative path, no argument, or a
bare name from inside one of its linked worktrees (see "Command directory
and repository resolution"). The clauses elsewhere in this document that
name `common_dir` as a bare repository's command directory, or that handle
a bare repository's first registry record, sketch a later extension; the
MVP never reaches them.

Worktree-admin registration is checked in both directions: `<path>/.git` must
be a regular file whose `gitdir:` line names `<common_dir>/worktrees/<id>`,
and `<common_dir>/worktrees/<id>/gitdir` must name `<path>/.git`. Relative
values resolve against the directory holding the file, and both comparisons
use realpaths. A row whose registration disagrees gets no status probe, has
classification `inspection-error`, and is excluded as `registration-mismatch`;
like every `inspection-error` it makes the plan incomplete. At revalidation a
disagreement refuses the target as `identity-changed`.

A registered path whose `lstat` fails with `ENOENT` or `ENOTDIR` has
`present: false` and the baseline `stale-worktree` classification. Any other
failure, such as `EACCES`, gives `present: null`, an `os-error` in the row's
`errors`, and classification `inspection-error`, and no probe runs in that
path.

Every Git child runs with the variables that `git rev-parse --local-env-vars`
lists removed from its environment, hard-coded from Git 2.43 rather than
queried with another child: `GIT_ALTERNATE_OBJECT_DIRECTORIES`,
`GIT_CONFIG`, `GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_COUNT`,
`GIT_OBJECT_DIRECTORY`, `GIT_DIR`, `GIT_WORK_TREE`,
`GIT_IMPLICIT_WORK_TREE`, `GIT_GRAFT_FILE`, `GIT_INDEX_FILE`,
`GIT_NO_REPLACE_OBJECTS`, `GIT_REPLACE_REF_BASE`, `GIT_PREFIX`,
`GIT_SHALLOW_FILE`, and `GIT_COMMON_DIR`. `-C <directory>` alone therefore
selects the repository, and also the worktree whose index a probe reads,
which is why "Probe directory rule" fixes each child's directory. Read-only
probes also set `GIT_OPTIONAL_LOCKS=0`; the removal child does not. The scrub
does not cover `GIT_CONFIG_GLOBAL` or `GIT_CONFIG_SYSTEM`, so the settings a
result depends on are pinned with `-c` instead, which no configuration file
overrides: every status probe and the removal child carry
`-c core.untrackedCache=false -c core.fsmonitor=false`.

### The narrow guarantee

Concurrent writers (editors, other agents, other `project` invocations, and
Git commands run by anyone else) are outside the safe contract. The MVP claims
no lock, lease, or writer-quiescence handoff. Its one guarantee is:

> A removal subprocess is spawned only if, at the revalidation performed
> immediately before spawning it, the repository identity, the target's
> worktree identity and branch evidence, every baseline signature field of
> the target, its `locked` flag, the absence of submodules and of hidden
> local state in its own index (read inside the target worktree), the
> manifest's `tracking_branch`, and the merge target's name, source
> (re-resolved from a fresh read of the manifest), and SHA all equal the
> values in the confirmed plan.

Any mismatch makes the target `refused`, spawns nothing, attempts no later
target, and exits 2. A value that cannot be re-read, including a filesystem
call that times out, counts as a mismatch. The reason is `identity-changed`
for a repository or worktree identity difference or a missing registry entry,
`branch-changed` for a different branch name or head, `state-changed` for any
other signature, lock, manifest, or merge-target difference,
`contains-submodule` for a new gitlink or admin `modules` entry, and
`hidden-local-state` for a newly flagged index entry. Revalidation runs its
checks in the order that "Preflight and targeted revalidation" lists, stops
at the first difference, and reports that difference's reason; the three
children it shares with the previous target's rescan always all run.

### Changes after confirmation

| Change after confirmation | How it is observed | Result |
| --- | --- | --- |
| Target directory replaced, moved, or made a symlink | realpath, `dev`, `ino`, or `admin_id` differs | `refused`, `identity-changed` |
| A parent directory of the target swapped | the target's realpath differs | `refused`, `identity-changed` |
| Target re-registered or repaired | the registration cross-check differs | `refused`, `identity-changed` |
| Repository root, its parent, or the common directory replaced | a `repository` field differs at the next identity probe | before any removal, `refused`, `identity-changed`, exit 2; after a removal, that target `unknown`, `unconfirmed-removal`, exit 1 (see "Repository replaced mid-batch"); the whole batch stops |
| Branch head moves before revalidation | the ref listing | `refused`, `branch-changed` |
| Branch head moves after revalidation | the post-removal rescan | see "Branch race" |
| Ignored files appear before revalidation | the ignored count is no longer 0 | `refused`, `state-changed` |
| Ignored files appear after revalidation | not observable | destroyed with the worktree (residual window) |
| An index entry flagged assume-unchanged or skip-worktree before revalidation | the hidden-state probe | `refused`, `hidden-local-state` |
| An index flag set after revalidation | not observable | edits it hides are destroyed (residual window) |
| A gitlink staged, or an admin `modules` entry created, before revalidation | the combined probe (a staged gitlink is a change), the admin `lstat`, or the hidden-state probe | `refused`, `state-changed` or `contains-submodule` |
| A submodule populated after revalidation | Git's own check | `failed`, `git-refused`, exit status 128 |
| Tracked or untracked changes appear after revalidation, before Git's own check | Git's non-force check, forced to list untracked files | `failed`, `git-refused`, exit status 128 |
| Lock added | the registry `locked` flag | `refused`, `state-changed` (Git would also refuse) |
| Manifest `tracking_branch` edited or made unparseable | the manifest re-read | `refused`, `state-changed` |
| Merge target moves, is renamed, or changes source, or `origin/HEAD` is repointed | the manifest re-read and the ref listing | `refused`, `state-changed` |
| Upstream, tracking OID, or ahead/behind changes | the ref listing | `refused`, `state-changed` |
| A new linked worktree is registered | not consulted | never added to the confirmed plan |

### Residual window

The last line of defense is Git's non-force `worktree remove`, under the
configuration the removal command pins. In Git 2.43 it refuses, with exit
status 128, a locked worktree, the main worktree, a worktree with modified or
untracked files, a worktree whose admin linkage fails its own validation, and
a worktree that holds a populated submodule or whose admin directory holds
`modules`. Its cleanliness check honors `status.showUntrackedFiles`, so under
a `no` setting it would not see untracked files, and in a fixture with the
untracked cache on, `core.checkStat=minimal`, and an index-writing status
already run, it deleted an untracked file with exit 0. The removal command
therefore pins all three settings:

```sh
git -c status.showUntrackedFiles=normal -c core.untrackedCache=false -c core.fsmonitor=false -C <command directory> worktree remove <path>
```

The check considers neither ignored files nor edits hidden by
assume-unchanged or skip-worktree flags, so a worktree whose only extra
content is of those kinds is deleted with exit 0. Ignored files created, and
index flags set, between revalidation and deletion are therefore outside the
contract, as is any change made after Git's own check. The window spans one
child start-up plus Git's own status check, typically well under a second.
The confirmation text and the result text each state this in one line.

### Branch race

The MVP never deletes a branch, so a branch race cannot lose commits. The
result depends only on where the change is observed:

- At revalidation: the target is `refused` with `branch-changed`, every later
  target is `not-attempted`, and the exit status is 2.
- Only by the post-removal rescan, after Git removed the worktree: the target
  is `removed`, because the rescan proved its registry entry and path are
  gone, with reason `branch-advanced-after-removal`. Its reconciliation shows
  `branch_present: true` and a `branch_sha` that differs from `planned_sha`
  (any difference, including a rewind). Every later target is
  `not-attempted` and the exit status is 2. If the branch no longer exists,
  the reason is `branch-missing-after-removal` with `branch_present: false`,
  and the same stop and exit status apply.

## Execution model

### Fresh plan and plan digest

`--all-safe --apply` always recomputes a fresh plan, prints it, and confirms
it unless `--yes` is given. The read-only preview is advisory; no later
invocation stores, reuses, or trusts it, so a change since the preview simply
shows up in the fresh plan. Within one apply run the order is: resolve the
repository; build the plan; refuse if it is incomplete or over a cap; refuse
if `--expect-plan` differs; stop with exit 0 if nothing is eligible; print the
plan; confirm; then begin the apply phase. The apply phase begins when the
prompt is answered `yes` or `--yes` is accepted.

The plan carries `plan_digest`, the lowercase hexadecimal SHA-256 of the UTF-8
encoding of this canonical JSON text, with `selected` in canonical order:

```python
value = {"repository": {"root": root, "common_dir": common_dir,
                        "dev": dev, "ino": ino},
         "merge_target": {"name": name, "sha": sha},
         "selected": [[t.path, t.branch, t.head] for t in selected]}
json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
```

`ensure_ascii=False` applies only to this digest input, never to the
emitted document. A `repository.root` or `common_dir` that is not valid
UTF-8 refuses with `unsupported-path-bytes` and exit 2 before any plan or
digest is built.
`--expect-plan <plan_digest>` refuses with code `plan-digest-mismatch` and
exit 2, before the prompt and before any mutation, when the fresh plan's
digest differs; the fresh plan is still printed so the caller can see what
changed. The digest covers what would be removed, not excluded rows or
observation time, so a change to an excluded worktree does not invalidate a
preview. `dev` and `ino` are host-local, so a remount or reboot that
renumbers them changes the digest and fails closed. `--expect-plan` stays
optional with `--yes`.

### One mutation seam

Single-target and batch removal share one internal operation,
`retire_worktree(plan, target)`:

1. Revalidate the target against the confirmed plan under the "Probe
   directory rule": the repository-wide children run as
   `git -C <command directory>`, and the combined status probe and the
   hidden-state probe run as `git -C <target path>`, inside the target
   worktree, only after its identity has been verified again. A mismatch
   returns `refused` without spawning anything.
2. If less than `removal_floor_seconds` (5 s) of the work deadline remains,
   stop: the target and every later one are `not-attempted` with
   `deadline-exceeded`. Otherwise spawn the non-force removal command shown
   under "Residual window", from the command directory, in its own process
   group, with no timeout but the 300 s hard ceiling. Both operands are
   absolute paths, so neither can be read as an option. The child is started
   with `Popen(..., start_new_session=True)`, not through the baseline
   `probe()`, whose `subprocess.run` sends SIGKILL to the single child on a
   timeout or any exception. The new session puts the child in its own
   process group, whose id is the child's pid. `start_new_session` works on
   Python 3.10, the project's floor, where `process_group=0` needs 3.11;
   `preexec_fn` is never used, because it is unsafe in a process with
   threads.
3. Reap the child. Once it is spawned, `project` never signals it: SIGINT,
   SIGTERM, SIGHUP, and the work deadline are deferred until it exits, and
   only the 300 s hard ceiling ends the wait ("Interruption and expiry").
4. Reconcile: rescan, then record the stage, reason, notes, exit status, probe
   count, and reconciliation record.

Before the first removal, the preflight described under "Preflight and
targeted revalidation" checks every selected target's repository-wide
evidence. If any target fails it, the first failing target in canonical order
is `refused`, all others are `not-attempted`, and nothing is removed. The
batch then calls the seam for each target in canonical order and stops after
the first result that is not a plain `removed`.

`project clean <root> --apply --action remove --worktree P` keeps its
interface and runs on the same seam. It builds the full plan
(`mode: "single"`), selects only P, lists every other eligible row in
`excluded` with reason `not-requested`, and has the same `selected` entry,
command, stages, and exit codes as a batch whose only target is P. Its
completeness is the repository-wide evidence plus P's own row: other rows'
`inspection-error`, `inspect-cap`, and unprobed states are recorded as
non-blocking omissions in the plan, while P's own revalidation stays fully
strict. P is probed first, so the 128-row cap, which counts registered rows,
`present: false` included, and exempts P, never omits it, and the 16-target
cap counts P alone, because `not-requested` precedes the counted gates. A P
that matches no registry entry refuses with `worktree-not-found`, and a P
that a gate excludes refuses with `target-excluded`, whose `reason` carries
the exclusion reason; every refusal that remains names a manual remedy in its
message (`git worktree prune`, `git worktree repair`, or removing that row by
hand). These tighten the baseline and are listed under "Baseline behavior
changes".
Plain read-only `project clean` builds the same full plan too, with
`mode: "report"`, under the same deadline and its own 256-row cap.
`push` and `delete-branch` keep their behavior apart from argument
resolution and two refusals. Under the shared ref listing a deleted
upstream fills `upstream`, where `a040790` leaves it null, so the command
`push` builds would change from `push -u origin <branch>` to
`push <remote> <branch>:<remote branch>`; instead `push` refuses a
`remote-gone` branch, which must be reviewed before it is republished, with
refusal reason `remote-gone` and exit 2. Both refuse with
`inspection-incomplete`, `inspect-cap`, or `deadline-exceeded` and exit 2
when their re-inspection is incomplete.

### Deadline and budgets

At start the invocation sets
`deadline = monotonic() + invocation_timeout_seconds` (60 s) and holds back
`reconciliation_reserve_seconds` (10 s), so the work deadline is 50 s after
start. Time spent blocked at the confirmation prompt is not work: when the
prompt returns, both deadlines move later by exactly the time spent waiting,
so a slow reader never causes a mid-batch expiry. Every Git probe, including
the one `discover` runs for a bare name, gets
`min(probe_timeout_seconds, work_remaining)`, with `probe_timeout_seconds`
set to 5 s. A removal child is spawned only when `work_remaining` is at least
`removal_floor_seconds` (5 s), so that no removal starts with too little time
to finish, and it then runs until it exits: the deadline gates only the start
of a removal, never its completion; otherwise the batch stops with
`deadline-exceeded`, that target and every later one are `not-attempted`,
and the exit status is 1. Reconciliation probes run inside the reserve with
`min(5 s, reserve_remaining)`. All budgets are in seconds, and the plan's
`budget` object names each duration with a `_seconds` suffix. Its last
member, `probe_concurrency: 1`, records that batch probing is serial by
design because it works inside one repository; the overview's own
concurrency rule is as its document states it. A probe that times out is
terminated and reaped like any other child, and the values it would have
produced become `null`. A deadline that passes while the plan is being built
makes the plan incomplete (refusal `deadline-exceeded`), so no removal starts.
The deadline bounds the inspection children and the batch's removal
children only: the `push` and `delete-branch` children, run through
`execute()`, stay without a timeout, as at `a040790`.

Every filesystem call (`lstat`, `realpath`, and the `.git` and `gitdir`
reads) runs in a daemon thread and is abandoned after
`min(probe_timeout_seconds, work_remaining)`, never on a `concurrent.futures`
pool, because the interpreter joins a pool's worker threads at exit, so an
abandoned pool thread would block it; an abandoned call records
`probe-timeout`, or `deadline-exceeded` when the global deadline was the
limit that cut it short, and leaves its values `null`. A call stuck inside
the kernel on an unresponsive mount cannot be interrupted from user space, so
a `--yes` run ends within about 60 s of wall time, and any run within the
deadline plus the 2 s reaping grace, except while such a call is outstanding
or a removal child is still running, which only the 300 s hard ceiling
bounds.

### Interruption and expiry

On SIGINT, or when the work deadline passes, `project` stops scheduling: no
further probe or removal starts. During the apply phase a SIGINT handler sets
a flag that the seam checks, rather than letting `KeyboardInterrupt` unwind
through a running child; probe children also run in their own process groups,
so a terminal Ctrl-C reaches only `project`. If a probe child is in flight,
`project` sends SIGTERM to its process group, waits at most 2 s, sends
SIGKILL if the group is still alive, and then waits at most the same 2 s
grace to reap it, after which the child is abandoned and its row recorded
`probe-timeout`. Every exit path terminates the process groups `project`
started, and each child's standard error is drained and capped. A removal
child is the exception: once it is spawned, `project` does not signal it.
SIGINT, SIGTERM, SIGHUP, and the work deadline are deferred until it exits,
and a separate hard ceiling of 300 s, for a hung mount, ends the wait by
killing the group and recording the target `unknown` with a
`partially-removed` note and the recovery text "inspect, then
`git worktree remove --force <path>` by hand". `project` then reconciles
every attempted target inside the reserve and prints the per-target record;
targets never reached are `not-attempted` with reason `interrupted` or
`deadline-exceeded`. A second SIGINT during reconciliation abandons the
remaining rescans and leaves their fields `null`. SIGINT or end of input
before the apply phase, while planning or at the prompt, exits 130 with zero
mutation, as in the baseline. SIGTERM and SIGHUP get the SIGINT treatment in
the apply phase, exiting 143 and 129, and the first signal received sets the
status; before the apply phase they terminate and reap probe children as
SIGINT does and exit 143 and 129 with zero mutation. After SIGHUP the
terminal may be gone, so output is printed on a best-effort basis. Other
termination signals are outside the MVP contract: the process may end
without a record, and a fresh read-only plan is the recovery path.

Once the apply phase begins, every exception raised while handling a target
is caught for that target and recorded as `unknown` with reason
`internal-error`; later targets are `not-attempted`, the result record is
printed (best effort after SIGHUP), and the exit status is 1 (130, 143, or
129 after SIGINT, SIGTERM, or SIGHUP). An unexpected
exception before the apply phase refuses with `internal-error` and exit 2.

### Stages and reconciliation

| Stage | Meaning | `reason` values |
| --- | --- | --- |
| `pending` | selected and not yet reached; shown in the printed plan and progress, never in a final record | `null` |
| `removed` | the child exited 0, the rescan shows the registry entry and path both absent, and `reconciled` is true | `null`, `branch-advanced-after-removal`, `branch-missing-after-removal` |
| `refused` | revalidation found a mismatch; nothing was spawned | `identity-changed`, `branch-changed`, `state-changed`, `contains-submodule`, `hidden-local-state` |
| `failed` | the child exited nonzero on its own, or could not be spawned | `git-refused` (exit 128, Git's pre-removal refusals), `git-failed` (any other nonzero status, including 128 plus the signal number when a signal that `project` did not send ended the child), `spawn-error` |
| `unknown` | a child ran, or an exception interrupted the target, and removal is not proven; a removal child killed at the 300 s hard ceiling also carries the `partially-removed` note | `unconfirmed-removal`, `interrupted`, `deadline-exceeded`, `reconciliation-incomplete`, `internal-error` |
| `not-attempted` | the batch stopped before reaching it, or before spawning its removal because less than `removal_floor_seconds` remained | `batch-stopped`, `interrupted`, `deadline-exceeded` |

Every `removed`, `refused`, `failed`, or `unknown` target carries a
`reconciliation` object with `registry_entry_present`, `path_present`,
`branch_present`, `branch_sha`, and `reconciled`; `pending` and
`not-attempted` targets carry `null`, including one that passed revalidation
before the removal floor stopped the batch. The three
presence fields are `true`, `false`, or `null`; `branch_sha` is a full object
name or `null`; `reconciled` is a boolean that is true only when the three
presence fields are non-null and `branch_sha` is non-null whenever
`branch_present` is true. A `refused` target's values come from the
revalidation scan that refused it, which shows what changed; every spawned
target's values come from a rescan after the child is reaped.
`registry_entry_present` says whether `worktree list --porcelain -z` still has
an entry for the planned path. `path_present` is `true` when `os.lstat` of
the planned path succeeds, `false` only when it fails with `ENOENT` or
`ENOTDIR`, and `null` for any other error or a timeout. `branch_present` and
`branch_sha` come from the ref listing. The rescan first re-establishes the
repository identity; if that differs from the plan, every field is `null` and
`reconciled` is false, because registry answers from another repository prove
nothing. A target's `notes` lists `orphaned-directory` whenever its
reconciliation shows `registry_entry_present: false` with
`path_present: true`: Git unregistered the worktree but left its directory.

`removed` requires rescan evidence (registry entry absent and path absent)
and `reconciled: true`, as well as an exit status of 0. The child's exit
status alone never proves removal: exit 0 without
that evidence is `unknown` with `unconfirmed-removal`, and exit 0 with that
evidence but an unfinished rescan or unreadable branch is `unknown` with
`reconciliation-incomplete`. A nonzero exit by the child itself is always
`failed`: `git-refused` for exit 128, which Git uses for its pre-removal
refusals, and `git-failed` for any other status, such as 255 when Git
unregistered the worktree but could not delete its directory.

### Exit codes

| Exit | Condition (the first matching row wins) |
| --- | --- |
| 130, 143, 129 | SIGINT (130), SIGTERM (143), or SIGHUP (129) was received, the first signal received setting the status, or input ended at the prompt (130) |
| 1 | the deadline stopped work after the apply phase began (a target is `not-attempted` or `unknown` because of it), or any target is `unknown` |
| Git's status | a target is `failed` with `git-refused` (128) or `git-failed` (any other nonzero status, such as 255) |
| 2 | any refusal code; a `refused` target; `removed` with a branch-after-removal reason; `failed` with `spawn-error` |
| 0 | every selected target is `removed` with `reason: null`, or nothing is eligible |

Git's status passes through unchanged, as at `a040790`, even when it is 1, 2,
or 130 and so equals one of `project`'s own statuses; the record's `stage`,
`reason`, and `exit_status` tell them apart. A removal child ended by a
signal that `project` did not send has exited on its own: it is `failed`
with `git-failed`, and its `exit_status`, and so the process exit status, is
128 plus the signal number, as the baseline `execute` reports signals.

`--yes` is the only way to apply on noninteractive stdin. Argument-parser
usage errors exit 2 with the parser's own message and no JSON object, as in
the baseline. A read-only preview or report exits 0 when the plan is
complete, rows deferred as `deferred-target-cap` included, 1 when it is
incomplete, and 2 when no plan can be built. Excluded protected work is
reported without
implying a batch failure.

## Probe accounting and limits

### Probe directory rule

Each linked worktree has its own index, so the directory a Git child runs in
decides which index it reads. Every child follows this rule, the same rule
the overview states:

- Worktree probes, the combined status probe and the hidden-state probe, run
  as `git -C <worktree path>` against that worktree's own index, and only
  after its identity (no-follow `dev` and `ino`, and the two-way admin
  registration) has been verified immediately before. The main worktree's
  status probe therefore runs in the command directory, which is its own
  worktree.
- Repository-wide probes run as `git -C <repository.root>`, or
  `git -C <common_dir>` for a bare repository, which is the command
  directory, except the identity probe (row 3), which runs in the candidate
  directory the argument resolves to. Resolution needs two more children
  there, before the command directory is known: `discover`'s child for a
  bare name (row 2) and the registry listing (row 4), which names the main
  worktree; both coincide with the command directory unless the argument
  resolved elsewhere. Row 1 needs no repository. Every revalidation and
  rescan child other than the two worktree probes runs in the command
  directory.
- The removal child runs as `git -C <command directory>`, as the baseline's
  does.

Run from the command directory, `ls-files -v` reads the main worktree's
index: on Git 2.43, with `a` flagged assume-unchanged only in the target's
index, it prints `H a` there and `h a` in the target. The hidden-state gate
would then pass a worktree whose hidden edits Git deletes. The proposal's
tests pin each child's directory with the counting `git` wrapper.

### Repository-wide probes

The plan builder runs repository-wide probes once per `common_dir`, memoizes
them, and fans the results out to every row. It runs worktree-specific probes
once per inspected row, and revalidation never recomputes the full report.

| Row | Child | Yields |
| --- | --- | --- |
| 1 | `git --version`, once per invocation | Git 2.36 or newer, needed for `worktree list -z`; older refuses with `git-too-old`, and a missing `git`, a timeout, or an unparseable version with `git-unavailable` |
| 2 | `discover`'s `rev-parse --show-toplevel`, for a bare-name argument only and at most once | the directory the name lookup selects |
| 3 | `rev-parse --path-format=absolute --show-toplevel --git-common-dir` at the resolved directory (`--git-common-dir` alone in a bare repository) | toplevel and `common_dir`; `os.lstat` adds `dev` and `ino` |
| 4 | `worktree list --porcelain -z` | the main worktree, and every linked path with its `HEAD`, branch, `locked`, and `prunable` |
| 5 | row 3 repeated in the command directory, only when row 3 ran elsewhere | confirms `root` and `common_dir` |
| 6 | one `for-each-ref` over `refs/heads` and `refs/remotes` in the format below | the `origin/HEAD` target; which merge-target candidates exist; the merge-target SHA; every branch's head, upstream, `upstream_oid`, ahead, behind, and `remote_present` |
| 7 | `for-each-ref --merged=<merge-target sha> --format=%(refname) refs/heads` | `merged_into_target` for every branch at once |

Every Git behavior this document cites was verified on Git 2.43 only, so
the 2.36 floor is unverified: the proposal must verify the probe set, the
scrubbed variable list, and the removal refusals on a pinned Git 2.36, or
raise the floor.

Row 6 passes this format string, identical in both packet documents, to
`--format=`; fields are NUL-separated and each record ends in a line feed,
which is safe because a refname cannot contain a control character:

```text
%(refname)%00%(objectname)%00%(symref)%00%(upstream)%00%(upstream:short)%00%(upstream:track,nobracket)
```

Rows 3, 4, 6, and 7 are the repository set: 4 children per repository, the
fixed per-repository term both packet documents state. F contains the same
four repository-wide children the overview counts (identity, registry
listing, ref listing, and merged set), plus the version check (row 1) and the
resolution children (rows 2 and 5); the main worktree's status probe is
counted with the worktree rows under W, as the overview also counts it, so it
is not part of F. F ≤ 7: 5 for an absolute path, which must already be the
root, and 6 or 7 for the other argument forms. Row 6 replaces the
baseline's `symbolic-ref` and per-candidate `show-ref --verify` calls in
`default_branch`, and its per-worktree `rev-parse --abbrev-ref @{upstream}`,
`rev-list --left-right --count`, and `rev-parse --verify` calls; row 7
replaces per-branch `merge-base --is-ancestor`; the one worktree probe below
replaces the separate dirty and ignored `status` calls. Overview, doctor, and
clean share this one evidence model, and the proposal proves value parity
with the baseline through fixture tests, except for the changes listed under
"Baseline behavior changes", of which the visible one is that a deleted
upstream reports `remote-gone`. A failed repository-wide probe leaves every
row's classification `null` and makes the plan incomplete
(`inspection-incomplete`).

### Worktree-specific probes

Each present, registration-consistent worktree row, the main one included,
gets exactly one child, the combined bounded probe, which runs inside that
row's own worktree ("Probe directory rule"):

```sh
git -c core.untrackedCache=false -c core.fsmonitor=false -C <worktree path> status --porcelain=v1 -z --untracked-files=normal --ignored=matching
```

Git prints tracked changes, then untracked entries, then ignored (`!!`)
entries, and the proposal's fixture tests pin that order. `dirty` is therefore
true as soon as a non-`!!` record arrives, and false as soon as a `!!` record
arrives first or an empty stream ends normally; a probe that fails or times
out before either leaves `dirty` `null`, records `probe-failed`,
`probe-timeout`, or `deadline-exceeded`, and makes the row `inspection-error`.
A failed, timed-out or deadline-cut status probe sets the row to
`inspection-error` directly, on the merge-target branch too, with that code's
repair finding of severity error. The ladder tests the merge-target branch
before cleanliness, so such a row would otherwise read `protected-default`
and leave the plan complete; set directly, it makes the plan incomplete. The
repair finding is the overview's, since the batch reports no findings.
A rename or copy record (`R` or `C`) carries a second NUL-terminated field,
its original path, which the parser consumes without counting. The probe
passes `--untracked-files=normal` explicitly because, under a user's
`status.showUntrackedFiles=no`, `--ignored` alone fails with "Unsupported
combination of ignored and untracked-files arguments". Identity needs no
child: `os.lstat` of the path plus reads of its `.git` file and its admin
`gitdir` file. A row whose path is missing, is unreadable, or fails the
registration check gets no probe.

A row that passes every other gate is checked last by the two index gates.
First, an `lstat` of `<common_dir>/worktrees/<admin_id>/modules`: any entry
there excludes the row as `contains-submodule`, and an error other than
`ENOENT` or `ENOTDIR` records an `os-error` and makes the row
`inspection-error`. Otherwise the row gets the hidden-state probe, which also
runs inside the row's own worktree:

```sh
git -C <worktree path> ls-files -v --stage -z
```

Git 2.43 combines `-v` with `--stage` (verified): each record is
`<tag> <mode> <object> <stage>`, a tab, and the path, ending in NUL, so an
assume-unchanged file reads `h 100644 <object> 0` and a gitlink
`H 160000 <object> 0`. The probe stops at the first gitlink (mode `160000`),
which excludes the row as `contains-submodule`; otherwise it reads the
stream to its end, because `contains-submodule` comes first in the gate
order, and a lowercase tag (assume-unchanged) or `S` (skip-worktree) on any
entry excludes the row as `hidden-local-state`. Gitlinks therefore cost no
extra child. The probe streams the index and keeps one flag, so its memory
does not grow with the worktree. At most 16 rows reach it, because rows
beyond the first 16 are deferred as `deferred-target-cap` before it runs.

### Preflight and targeted revalidation

Revalidating one target spawns at most five children and never the full
report. It runs these checks in this order and stops at the first
difference:

1. The identity probe, in the command directory.
2. A fresh read of the manifest at `repository.root` (a file read, no
   child), before the ref listing is built. Its `tracking_branch`, or its
   absence, must equal the value read when the plan was built; any
   difference, or a manifest that no longer parses, is `state-changed`,
   whatever the ref listing contains.
3. `worktree list --porcelain -z`, in the command directory.
4. One `for-each-ref` in the row 6 format, in the command directory, whose
   patterns name explicitly `refs/heads/<merge_target.name>`, the
   manifest's candidate under `refs/heads/` when there is one, the
   `refs/heads/` branch that the plan's `origin/HEAD` symref named, if any,
   `refs/heads/main`, `refs/heads/master`, `refs/remotes/origin/HEAD`, and
   the selected branches and their upstreams. The merge target is
   re-resolved over that listing, so a changed name, source, or SHA is
   `state-changed`, and so is an `origin/HEAD` symref that now names a
   branch outside the listing, whose existence the listing cannot show.
5. The target's identity and its `modules` check, filesystem reads only.
6. Inside the target worktree, as `git -C <target path>`: the combined
   probe, which must print no record at all, and then the hidden-state
   probe, which must find no gitlink and no flagged entry.

A selected target was clean with zero ignored files, so an empty combined
stream means exactly "still clean and still no ignored files", and the first
record ends the probe. Ancestry needs no child: it is a function of the
branch head and the merge-target SHA, and both must be unchanged.

The first target's three repository children are the preflight: their
listing names every selected branch, so they revalidate every target's
repository-wide evidence, lock, and filesystem identity before any removal.
After target k's child is reaped, the rescan runs the same three children,
with the manifest re-read between the first two, and all three always run,
because target k's reconciliation needs every one of them. When target k
ends as a plain `removed`, they double as the repository part of target
k+1's revalidation, which follows with nothing in between, and they count in
target k+1's `probes_performed`. After the last spawned target, or when
target k's result stops the batch, they are the final rescan instead, and a
target k+1 is `not-attempted` with `probes_performed: 0`.

### Cap arithmetic

Assumption, to be measured by the proposal: at most 100 ms per warm Git child
and about 0.3 s per removal of a clean worktree. With W worktree rows
inspected, E rows reaching the hidden-state probe, and T targets selected, an
`--apply` run spawns at most F + W + E children to plan, 5T to revalidate, 3
for the final rescan, and T removals.

The caps are derived by one rule, applied at 150 ms per child (a 1.5×
margin over the assumption) with removals unchanged, with the worst case
taking F = 7 and E = T. A cap pair fits when its worst case completes within
the 50 s work deadline and spawns its last removal with at least
`removal_floor_seconds` (5 s) left. The row cap is chosen first: it is the
largest power of two for which at least 16 targets fit. The target cap is
chosen second: it is the largest multiple of 8 that fits with that row cap.
The fit test is per run: rows beyond the target cap are deferred as
`deferred-target-cap`, and re-running drains them 16 at a time.

| Term | Children | At 100 ms | At 150 ms |
| --- | ---: | ---: | ---: |
| Fixed term F | 7 | 0.7 s | 1.05 s |
| Worktree rows, 1 × 128 | 128 | 12.8 s | 19.2 s |
| Hidden-state probes at plan time, 1 × 16 | 16 | 1.6 s | 2.4 s |
| Revalidation, 5 × 16 targets | 80 | 8.0 s | 12.0 s |
| Final rescan | 3 | 0.3 s | 0.45 s |
| Removals, 16 × about 0.3 s | 16 | about 4.8 s | about 4.8 s |
| Worst case | 250 | about 28.2 s | about 39.9 s |

Row cap first: with 256 rows, 16 targets need 7 + 256 + 16 + 80 + 3 = 362
probe children, 54.3 s, or 59.1 s with their removals, so 256 rows are
rejected; even 8 targets (314 children, 47.1 s, or 49.5 s with removals)
would spawn their last removal at 48.75 s with only 1.25 s left. With 128
rows, 16 targets take 39.9 s, so 128 is the row cap.

Target cap second: with 128 rows and T targets, target k's removal is
spawned after 7 + 128 + T + 5k probe children and k - 1 removals. With 16
targets that is 22.35 + 1.05k s, so the 16th removal is spawned at 39.15 s
with 10.85 s of the work deadline left, and 16 is the target cap. 24 targets
would fit the deadline alone, with a worst case of 49.5 s and the 24th
removal spawned at 48.75 s, but their spawn times are 23.55 + 1.05k s, so
the 21st removal would start at 45.6 s, with 4.4 s left, inside the floor;
that is why 24 is not the cap. At the 100 ms assumption the caps leave about
21.8 s of headroom, and the 16th removal is spawned at 27.6 s.

The caps replace the earlier 1,024 inspected worktrees and 100 targets,
which could not meet the deadline even at 100 ms: inspecting 1,024 rows alone
needs 7 + 1,024 = 1,031 children, about 103 s, and 100 targets need about
100 × (0.6 s + 0.3 s) = 90 s. If measurement disagrees with the assumption,
the proposal reapplies the same rule with the same fit test: a higher
measured cost lowers the target cap in steps of 8 and the row cap in powers
of two, and the rule keeps the row cap as large as it can, since a smaller
target cap only splits work across runs while a smaller row cap makes more
plans incomplete.
Overrunning the estimate is never unsafe: the deadline and the removal floor
stop scheduling, unreached targets are `not-attempted`, and the run exits 1
with a reconcilable record.

The plain read-only report (`mode: "report"`) spawns no revalidation,
rescan, or removal, so the same fit test, applied to its own children,
F + W + E = 7 + W + 16, gives it a larger row cap: 256 rows need 279
children, about 41.85 s at 150 ms, inside the 50 s work deadline, while 512
rows would need 535, about 80.25 s. Its `limits.worktree_rows` is therefore
256, and "Inspection order and omitted work" applies to it with 256 in place
of 128; the `--all-safe` and single-target `remove` plans keep 128 rows and
16 targets.

### Inspection order and omitted work

The registry listing is read completely, in one child, before any cap
applies. Rows are ordered main worktree first, then by raw path bytes (Git
itself sorts linked entries case-insensitively under `core.ignoreCase`, so
the batch re-sorts), and the first 128 are inspected: with more rows, the
main worktree and the 127 linked worktrees with the smallest paths. The rest
are not probed: the plan is incomplete with refusal code `inspect-cap`, and
`omitted: {count, exactness}` counts them. In single-target mode P is probed
first and exempt from the cap, and the omission does not block it ("One
mutation seam"). Because the registry was listed in
full, `exactness` is always `exact` in a printed plan: a listing that failed
or timed out builds no plan, so the overview's `lower-bound` and `unknown`
never appear here. A deadline during inspection likewise leaves the
remainder in `omitted` with refusal code `deadline-exceeded`, and a probe
timeout turns its row into `inspection-error` with refusal code
`inspection-incomplete`. Omitted and timed-out work is therefore always
visible, and either blocks apply.

### Bounded ignored-file inspection

The combined probe streams its NUL-delimited output and stops reading,
terminating the child, when a 65th ignored (`!!`) record or a 4,097th record
of any kind arrives; a probe that `project` stops at its record bound is a
complete outcome, never `probe-failed`. A stream that ends within
`ignored_entries` (64)
ignored and `status_records` (4,096) total records is complete; neither
memory nor JSON grows with the worktree, and the full list is never
materialized. `ignored_files` keeps its baseline name and type (an integer,
or `null` when not established) but now means the number of ignored records
read, a lower bound when `ignored_files_truncated` is true. Exactly 64
ignored entries is therefore an exact count and is not truncated.
`ignored_samples` holds at most `ignored_samples` (8) observed ignored paths,
relative to the worktree and escaped like any other path. Both
`ignored_files_truncated` and `ignored_samples` are `null` when the status
probe did not run or failed. A row's `locked` is a boolean, never `null`: it
comes from the registry listing, and without that listing no row exists and
no plan is built. A stream stopped
before any ignored record was read leaves `ignored_files` `null`; `dirty` is
then `true`, because every record read was a change or an untracked entry,
and the ladder classifies the row `dirty`, so the plan stays complete.
Truncation therefore yields `dirty` or `ignored-local-files`, never
`inspection-error`.

### Probe and operation estimates

The plan reports `probes: {estimated, performed}` and
`operations: {estimated, performed}` as integers, and so does the apply
result record. `probes.estimated` is the upper bound F + W + E + 5T + 3 for
an `--apply` run of this plan, using the F of this invocation's argument
form, and `probes.performed` counts every Git child this invocation spawned,
`discover`'s included. In the apply result record, `probes.performed` equals
the plan's count plus each target's `probes_performed` plus the final rescan,
which is 3 when the rescan after the last spawned target counted toward no
later target, and 0 otherwise.
`operations.estimated` is T, one removal per selected target, and
`operations.performed` counts removals spawned, which is 0 in a preview.
Together with `limits` and `budget` they show why a plan is incomplete or
close to its deadline.

## Repository and JSON contract

### Command directory and repository resolution

Every repository-wide Git command after resolution and the removal run as
`git -C <command directory>`, where the command directory is
`repository.root`, or `common_dir` for a bare repository. Each
worktree-specific probe, the combined status probe and the hidden-state
probe, runs instead as `git -C <worktree path>` inside that row's own
worktree, after the row's identity is verified, because each linked worktree
has its own index: run from the command directory, the hidden-state probe
would read the main worktree's index and miss the target's flags. "Probe
directory rule" states this for every child. The baseline already removes
worktrees from the resolved repository root, so no surviving merge-target
worktree is needed, and this revision drops that earlier requirement. The
command directory is the main worktree (or the bare directory, a later
extension), which `git worktree remove` never removes, so it survives every
target, and it is
identity-checked at every revalidation with the rest of `repository`.

Every `project clean` mode (the read-only report, `--json`, `--all-safe`, and
`--apply --action push|remove|delete-branch`) resolves its argument the same
way, always ending in the design's own counted, deadline-bounded identity
probe:

| Argument | Resolution | Refused with |
| --- | --- | --- |
| Absolute path | identity probe at the path; its realpath must equal the toplevel Git reports there, and that toplevel must be the main worktree, the first registry record | `target-not-repository-root` for a subdirectory, a linked worktree, a bare repository, or a path outside any repository |
| Relative path, or no argument | made absolute against the working directory; identity probe there; the repository Git finds, with `root` set to its main worktree | `target-not-repository-root` when Git finds no worktree there, a bare repository included |
| Bare name (one path component) | the baseline `discover` name lookup, its one Git child counted and bounded; then the identity probe at the directory it returns, which must be a worktree toplevel | `ambiguous-name`, `repository-not-found`, `target-not-repository-root` |

When the resolved directory is a linked worktree, `root` still names the main
worktree, and row 5 confirms it there. When the first registry record's path
equals `common_dir`, the main checkout is a gitfile checkout: the main
worktree is the realpath of `core.worktree`, and a command root equal to it
resolves. A submodule checkout, whose first record lies under
`.git/modules`, is refused with `target-not-repository-root`.
`discover`'s manifest-ancestor and
family-holder redirections are never applied to a path argument: a repository
root they would redirect resolves to itself, and a non-repository directory
they would redirect is refused. This is a baseline behavior change: today
`discover` redirects `/outer/leg`, a repository nested under an `/outer`
directory holding `project.yaml`, to `/outer`, and `/Atlas`, a repository
root containing `Atlas/family.yaml`, to the holder `/Atlas/Atlas`.

The overview's rows carry `repository.root` and `common_dir`. A row or
finding carries `suggested_command` only when a finding supplies one, and it
is otherwise `null`; when present it is a JSON argument vector such as
`["project", "clean", "/home/user/projects/Atlas", "--all-safe"]`, never a
shell string and never a bare name. Because the plan reports all four
`repository` fields, a caller can compare them with the overview row before
applying, and `--expect-plan` binds the apply to one preview.

### Representation rules

These rules apply to both envelopes defined here, the plan and the apply
result.

- Types are JSON string, integer, boolean, array, object, or `null`, as the
  field tables state. Paths are absolute realpaths, except `ignored_samples`
  entries, which are relative to their worktree, and a bare repository's
  `null` root. Object names are full lowercase hexadecimal: 40 characters, or
  64 in a SHA-256 repository. Times are RFC 3339 UTC with second precision
  and a `Z` suffix. Durations are integer seconds in fields ending in
  `_seconds`.
- Identity: a `repository` is identified by all four of its fields together,
  and a selected worktree by `path`, `dev`, `ino`, and `admin_id` together; a
  path or project name alone is never an identity.
- Enums are closed within a schema version; this document lists every value.
  The plan's `notes` codes are `merge-target-conflict`, and a target's `notes`
  codes are `orphaned-directory` and `partially-removed`.
- `null` means unknown or not established, never a default `false` or `0`.
  The rule binds every field this design adds; baseline row fields keep their
  baseline meaning (a row's `upstream: null`, for example, means none was
  resolved).
- Errors and refusals are `{code, message, path?, reason?}` objects: `code`
  is a stable kebab-case string, `message` is human text that may change,
  `path` appears only when one path is at fault, and `reason` appears only on
  `target-excluded`. A row's `errors` use the same shape with the codes
  `os-error`, `probe-failed`, `probe-timeout` (one probe or filesystem call
  reached its own limit), and `deadline-exceeded` (the global deadline was the
  limit).
- `completeness` is `complete` or `incomplete`. A plan is complete when every
  worktree row within the cap was inspected within the deadline, every
  repository-wide probe succeeded, and no row is `inspection-error`. An apply
  result is complete when every target whose `reconciliation` is an object
  has `reconciled: true`.
- Paths: Git output is read NUL-delimited (`-z`) everywhere, so newline, tab,
  and other control characters are supported. A valid UTF-8 path is an
  ordinary JSON string, exact after JSON unescaping, with
  `path_valid_utf8: true`. The JSON output escapes every control,
  bidirectional, and format code point, as the baseline's default
  `json.dumps` does (it writes every non-ASCII code point and every control
  character, U+007F included, as a JSON escape: the short form, such as
  `\n` or `\t`, where JSON has one, and `\uXXXX` otherwise), so the
  document never carries one raw. A path that is not valid UTF-8 is emitted in
  escaped form, each undecodable byte as the four characters `\xHH`
  (lowercase hexadecimal) and each literal backslash doubled, with
  `path_valid_utf8: false`; it is excluded with `unsupported-path-bytes` and
  is never a removal operand. In human output, a path prints verbatim in prose
  and with POSIX shell quoting in commands unless it contains a control
  character (U+0000 to U+001F, U+007F to U+009F), a bidirectional or format
  character (U+200E, U+200F, U+2028, U+2029, U+202A to U+202E, U+2066 to
  U+2069), or an undecodable byte. Such a path prints in `$'…'` form, in
  prose and commands alike: each undecodable byte as `\xHH`, each decoded
  control, bidirectional, or format code point as `\uXXXX`, both with
  lowercase hexadecimal digits (a newline is `\u000a` and U+202E is
  `\u202e`), each backslash doubled, and each single quote as `\'`. The
  overview uses the same form, so a path prints identically in both, and
  under a UTF-8 locale a printed command pastes into bash or zsh unchanged
  and shows the path that will be removed. Under the C locale that holds
  only for escapes below U+0080, such as `\u000a`: bash can leave a
  non-ASCII escape such as `\u202e` unexpanded, and zsh can reject it with
  "character not in range". Pasting also needs bash 4.2 or newer, the first
  bash whose `$'…'` form expands `\u`; the stock bash 3.2 of macOS lacks
  it.
- Order: `worktrees` lists the main worktree first, then the rest by raw path
  bytes, and this order is not part of the compatibility contract; `selected`,
  `excluded`, and `targets` use canonical path order.
- Evolution: `schema_version` is an integer, 1 for this design. Within a
  version, changes are additive and consumers ignore unknown fields; a rename,
  removal, type change, or meaning change increments it.

### Plan envelope

Every `project clean --json` prints this one `schema_version: 1` envelope,
not only `--all-safe`: plain `project clean <root> --json` prints it with
`mode: "report"`. The baseline keys keep their names and types, and every
new key is listed here. `root` now always names the command directory, a
row's `present` may be `null`, and `ignored_files` counts the ignored
records read, all listed under "Baseline behavior changes".

| Field | Type | Contract |
| --- | --- | --- |
| `schema_version` | integer | 1 |
| `observed_at` | string | RFC 3339 UTC time the plan was frozen |
| `mode` | string | `all-safe`; `single` marks the one-item plan of single-target removal; `report` marks the plan of plain read-only `project clean` |
| `root` | string | baseline key; the command directory: `repository.root`, or `common_dir` for a bare repository |
| `target_branch` | string | baseline; equals `merge_target.name` |
| `tracking_freshness` | string | baseline, unchanged text |
| `worktrees` | array | baseline rows plus `locked` (boolean, never `null`), `ignored_files_truncated` (boolean, or `null` when the status probe did not run or failed), `ignored_samples` (array of at most 8 strings, or `null` likewise), `path_valid_utf8` (boolean), and `errors` (array of `{code, message, path?}`); `present` may be `null` |
| `repository` | object | `root` (string, or `null` for a bare repository); `common_dir` (string); `dev`, `ino` (integers) |
| `merge_target` | object | `name`, `source`, `sha` (strings); `source` is `manifest`, `origin-head`, `main`, or `master` |
| `limits` | object | `worktree_rows` (128, or 256 in `mode: "report"`), `targets` (16), `ignored_entries` (64), `status_records` (4096), `ignored_samples` (8) |
| `budget` | object | `probe_timeout_seconds` (5), `invocation_timeout_seconds` (60), `reconciliation_reserve_seconds` (10), `removal_floor_seconds` (5), `probe_concurrency` (1) |
| `probes`, `operations` | object | `estimated`, `performed` (integers) |
| `selected` | array | `path`, `branch`, `head`, `upstream`, `upstream_oid` (strings); `ahead`, `behind`, `dev`, `ino` (integers); `admin_id` (string); `operation` (`{kind: "worktree-remove", argv}`, with `argv` the exact argument vector) |
| `excluded` | array | `path` (string); `path_valid_utf8` (boolean); `branch` (string or `null`); `classification` (string, or `null` if never classified); `reason` (string) |
| `omitted` | object | `count` (integer); `exactness` (always `exact` in a plan; see "Inspection order and omitted work") |
| `notes` | array | informational `{code, message}` objects; never affect `apply_allowed` |
| `completeness` | string | `complete` or `incomplete` |
| `apply_allowed` | boolean | true only for a complete plan within both caps with no refusal |
| `refusals` | array | `{code, message, path?, reason?}` objects |
| `plan_digest` | string | 64 lowercase hexadecimal characters |

When no plan can be built, `--json` prints the baseline error object
`{"error": "<message>"}` extended first with `code`, the first refusal's
code, which is the one key the overview adds to the same baseline object,
and then with `schema_version`, `observed_at`, `mode`, `repository` and
`merge_target` (each `null` unless established),
`completeness: "incomplete"`, `apply_allowed: false`, and `refusals`. The
overview has no plan to describe, so its object stops at `code`; a consumer
that reads `error` and `code` handles both.

### Refusal codes

| Code | Phase | Raised when |
| --- | --- | --- |
| `invalid-arguments` | resolve | a flag combination is invalid, or `--expect-plan` is not 64 lowercase hexadecimal characters |
| `internal-error` | any, before apply | an unexpected exception; the message names its class |
| `git-unavailable` | resolve | `git` is missing, or `git --version` failed, timed out, or printed an unparseable version |
| `git-too-old` | resolve | Git is older than 2.36 |
| `repository-not-found` | resolve | a bare name resolves to no project directory |
| `ambiguous-name` | resolve | a bare name matches more than one project |
| `target-not-repository-root` | resolve | the argument fails the resolution table |
| `unsupported-path-bytes` | resolve | `repository.root` or `common_dir` is not valid UTF-8 |
| `manifest-invalid` | resolve | the manifest at `repository.root` cannot be read or has the wrong kind |
| `no-merge-target` | resolve | no merge-target candidate exists as a local branch |
| `inspection-incomplete` | plan | a repository-wide probe failed or a row is `inspection-error` |
| `inspect-cap` | plan | more worktree rows are registered than `limits.worktree_rows` (128, or 256 in `mode: "report"`) |
| `deadline-exceeded` | plan | the work deadline passed while planning |
| `target-cap` | retired | no longer a refusal: rows beyond the first 16 that pass every gate before `contains-submodule` are excluded as `deferred-target-cap`, and the code survives only as the overview's limiting `suggestion_gate` |
| `worktree-not-found` | select | single-target `--worktree` matches no registry entry |
| `target-excluded` | select | a gate excludes the single-target worktree; `reason` carries the exclusion reason |
| `plan-digest-mismatch` | confirm | the fresh digest differs from `--expect-plan` |
| `confirmation-required` | confirm | `--apply` ran on noninteractive stdin without `--yes` |
| `cancelled` | confirm | the prompt was answered with anything other than `yes` |

A `resolve` refusal builds no plan and prints the extended error object under
`--json`. A `plan` or `select` refusal prints the plan with
`apply_allowed: false`, and a `confirm` refusal prints a complete plan and
stops before the apply phase. Under `--apply`, every refusal exits 2 with
zero mutation.

### Apply result record

The apply phase always ends with this record, which the MVP renders as human
text.

| Field | Type | Contract |
| --- | --- | --- |
| `schema_version` | integer | 1 |
| `observed_at` | string | RFC 3339 UTC time reconciliation finished |
| `repository`, `merge_target` | object | as in the plan |
| `plan_digest` | string | digest of the plan that was applied |
| `probes`, `operations` | object | `estimated`, `performed` (integers) for the whole invocation |
| `targets` | array | one entry per selected target, in canonical order |
| `exit_code` | integer | the process exit status, per "Exit codes" |
| `completeness` | string | `complete` or `incomplete` |

Each `targets` entry has `path`, `branch`, and `planned_sha` (strings);
`stage` and `reason` from the stage table, where `reason` may be `null`;
`notes`, an array of codes; `command`, the planned argument vector, present
even when nothing ran; `exit_status`, an integer or `null`, which is `null`
unless a child was spawned and reaped and is 128 plus the signal number when
a signal ended the child, whoever sent it, as the baseline `execute` reports
signals; `probes_performed`, the Git children of that target's
revalidation, the three it shares with the previous target's rescan included
(at most 5, fewer when it stopped at a difference, and 0 when it was never
revalidated); and `reconciliation`, an object or `null`.

### Fixtures

Both fixtures are illustrative and use fake paths; each `plan_digest` is the
real digest of its own `repository`, `merge_target`, and selection, and each
probe count follows the estimate formula for an absolute-path argument
(F = 5). This plan has three worktree rows, selects one worktree, and
excludes two:

```json
{
  "schema_version": 1,
  "observed_at": "2026-10-07T14:03:12Z",
  "mode": "all-safe",
  "root": "/home/user/projects/Atlas",
  "target_branch": "main",
  "tracking_freshness": "local refs only; remote information is as of the last fetch; no fetch performed",
  "repository": {"root": "/home/user/projects/Atlas",
                 "common_dir": "/home/user/projects/Atlas/.git",
                 "dev": 66306, "ino": 3407873},
  "merge_target": {"name": "main", "source": "origin-head",
                   "sha": "39f33f71eba7ca23d258c75ebcc8b9a0ec9995d9"},
  "limits": {"worktree_rows": 128, "targets": 16, "ignored_entries": 64,
             "status_records": 4096, "ignored_samples": 8},
  "budget": {"probe_timeout_seconds": 5, "invocation_timeout_seconds": 60,
             "reconciliation_reserve_seconds": 10,
             "removal_floor_seconds": 5, "probe_concurrency": 1},
  "probes": {"estimated": 17, "performed": 9},
  "operations": {"estimated": 1, "performed": 0},
  "worktrees": [
    {"path": "/home/user/projects/Atlas", "present": true,
     "head": "39f33f71eba7ca23d258c75ebcc8b9a0ec9995d9", "branch": "main",
     "dirty": false, "ignored_files": 0, "current": false,
     "upstream": "origin/main", "ahead": 0, "behind": 0,
     "merged_into_target": true, "remote_present": true,
     "classification": "protected-default",
     "recommendation": "Keep the default branch; use the repository's normal push or PR process.",
     "locked": false, "ignored_files_truncated": false,
     "ignored_samples": [], "path_valid_utf8": true, "errors": []},
    {"path": "/home/user/projects/Atlas-worktrees/feature-login",
     "present": true, "head": "635e8931ebd09939ab00fb1598598f6e43fdaf41",
     "branch": "feature/login", "dirty": false, "ignored_files": 0,
     "current": false, "upstream": "origin/feature/login",
     "ahead": 0, "behind": 0, "merged_into_target": true,
     "remote_present": true, "classification": "merged-removable",
     "recommendation": "This clean, merged, non-current worktree may be removed explicitly.",
     "locked": false, "ignored_files_truncated": false,
     "ignored_samples": [], "path_valid_utf8": true, "errors": []},
    {"path": "/home/user/projects/Atlas-worktrees/feature-report",
     "present": true, "head": "fc2afa49af6ee0111f0de91e16b6e651af506f2a",
     "branch": "feature/report", "dirty": true, "ignored_files": 0,
     "current": false, "upstream": "origin/feature/report",
     "ahead": 2, "behind": 0, "merged_into_target": false,
     "remote_present": true, "classification": "dirty",
     "recommendation": "Preserve or commit the working changes before cleanup.",
     "locked": false, "ignored_files_truncated": false,
     "ignored_samples": [], "path_valid_utf8": true, "errors": []}
  ],
  "selected": [
    {"path": "/home/user/projects/Atlas-worktrees/feature-login",
     "branch": "feature/login",
     "head": "635e8931ebd09939ab00fb1598598f6e43fdaf41",
     "upstream": "origin/feature/login",
     "upstream_oid": "635e8931ebd09939ab00fb1598598f6e43fdaf41",
     "ahead": 0, "behind": 0, "dev": 66306, "ino": 3540993,
     "admin_id": "feature-login",
     "operation": {"kind": "worktree-remove",
                   "argv": ["git", "-c", "status.showUntrackedFiles=normal",
                            "-c", "core.untrackedCache=false",
                            "-c", "core.fsmonitor=false",
                            "-C", "/home/user/projects/Atlas",
                            "worktree", "remove",
                            "/home/user/projects/Atlas-worktrees/feature-login"]}}
  ],
  "excluded": [
    {"path": "/home/user/projects/Atlas", "path_valid_utf8": true,
     "branch": "main", "classification": "protected-default",
     "reason": "main-worktree"},
    {"path": "/home/user/projects/Atlas-worktrees/feature-report",
     "path_valid_utf8": true, "branch": "feature/report",
     "classification": "dirty", "reason": "dirty"}
  ],
  "omitted": {"count": 0, "exactness": "exact"},
  "notes": [],
  "completeness": "complete",
  "apply_allowed": true,
  "refusals": [],
  "plan_digest": "7495756d199ba217f41ed4d648c241c95608b4f353c46952e9a7f4cddc17f3bc"
}
```

This apply result comes from a different run whose plan had four worktree
rows and selected three worktrees. The first was removed; the second target's
branch gained a commit after that removal, so its revalidation refused it at
the third child; the third was not attempted. No final rescan ran, because
the last spawned target was reconciled by the second target's revalidation.

```json
{
  "schema_version": 1,
  "observed_at": "2026-10-07T14:05:47Z",
  "repository": {"root": "/home/user/projects/Atlas",
                 "common_dir": "/home/user/projects/Atlas/.git",
                 "dev": 66306, "ino": 3407873},
  "merge_target": {"name": "main", "source": "origin-head",
                   "sha": "39f33f71eba7ca23d258c75ebcc8b9a0ec9995d9"},
  "plan_digest": "cf2d0bea641d01e4fc1acb2abe6aef545f7ea38295ccd11c141bd801e0b55c98",
  "probes": {"estimated": 30, "performed": 20},
  "operations": {"estimated": 3, "performed": 1},
  "targets": [
    {"path": "/home/user/projects/Atlas-worktrees/feature-login",
     "branch": "feature/login",
     "planned_sha": "635e8931ebd09939ab00fb1598598f6e43fdaf41",
     "stage": "removed", "reason": null, "notes": [],
     "command": ["git", "-c", "status.showUntrackedFiles=normal",
                 "-c", "core.untrackedCache=false",
                 "-c", "core.fsmonitor=false",
                 "-C", "/home/user/projects/Atlas", "worktree", "remove",
                 "/home/user/projects/Atlas-worktrees/feature-login"],
     "exit_status": 0, "probes_performed": 5,
     "reconciliation": {"registry_entry_present": false,
                        "path_present": false, "branch_present": true,
                        "branch_sha": "635e8931ebd09939ab00fb1598598f6e43fdaf41",
                        "reconciled": true}},
    {"path": "/home/user/projects/Atlas-worktrees/feature-search",
     "branch": "feature/search",
     "planned_sha": "368a133b9d8f342efb77df84a4c37ca69283f999",
     "stage": "refused", "reason": "branch-changed", "notes": [],
     "command": ["git", "-c", "status.showUntrackedFiles=normal",
                 "-c", "core.untrackedCache=false",
                 "-c", "core.fsmonitor=false",
                 "-C", "/home/user/projects/Atlas", "worktree", "remove",
                 "/home/user/projects/Atlas-worktrees/feature-search"],
     "exit_status": null, "probes_performed": 3,
     "reconciliation": {"registry_entry_present": true,
                        "path_present": true, "branch_present": true,
                        "branch_sha": "c7b81a093423d9b1be2e8619471834a5cbcbe0d7",
                        "reconciled": true}},
    {"path": "/home/user/projects/Atlas-worktrees/fix-typo",
     "branch": "fix/typo",
     "planned_sha": "72e5554760d7cea17ea436028406d94f0f3f48e8",
     "stage": "not-attempted", "reason": "batch-stopped", "notes": [],
     "command": ["git", "-c", "status.showUntrackedFiles=normal",
                 "-c", "core.untrackedCache=false",
                 "-c", "core.fsmonitor=false",
                 "-C", "/home/user/projects/Atlas", "worktree", "remove",
                 "/home/user/projects/Atlas-worktrees/fix-typo"],
     "exit_status": null, "probes_performed": 0, "reconciliation": null}
  ],
  "exit_code": 2,
  "completeness": "complete"
}
```

### Machine-readable apply results

`--apply --json` is accepted for single-target removal and the batch,
`--action remove` and `--all-safe`, and nowhere else: with `--action push`
or `--action delete-branch` it stays refused as `invalid-arguments`, exit 2.
Standard output then carries exactly one JSON document (the plan envelope,
or the extended error object, when the run stops before the apply phase,
otherwise the apply result record), while the human plan, the confirmation
prompt, and progress go to standard error.

## Baseline behavior changes

A proposal built on this design must list these changes to `a040790` and
carry them into the governing cleanup specification. The overview document
lists the same shared items; the batch-only items follow them.

Shared with the overview:

- In every `project clean` mode, `push` and `delete-branch` included, an
  absolute path must be exactly a main worktree root or is refused with
  `target-not-repository-root`; today `discover` redirects `/outer/leg` to
  `/outer` and `/Atlas` to `/Atlas/Atlas`. A bare name still uses
  `discover`, whose Git child becomes counted and deadline-bounded: every
  inspection Git child runs through a new bounded runner (`Popen` with
  `start_new_session=True`, a scrubbed environment, and output streamed as
  bytes), and `probe()` stays for non-Git children (`push` and
  `delete-branch` excepted, ruling D-W).
- `repo_state` and `cleanup_report` move onto the shared probes, so overview,
  doctor, and clean report the same values. The baseline's
  `rev-parse --abbrev-ref @{upstream}` cannot distinguish a never-configured
  upstream from one whose remote-tracking ref was deleted, so `a040790`
  reports `unpublished` for both; the shared `for-each-ref` with
  `%(upstream:track)` can, so overview and clean classify the deleted one
  `remote-gone`. Doctor never classifies a deleted upstream; its only
  worktree classification is `repo_state`'s `stale-worktree`, shown under
  `--json`. Both are preserve states. The promise that
  baseline row fields are unchanged covers field names and types (with
  `present` gaining `null`), not the probe that fills them.
- Git output is parsed NUL-delimited, so a newline path is no longer misread
  and a non-UTF-8 path no longer ends the run with an uncaught exception.
- One combined status probe with explicit `--untracked-files=normal`, run
  with `-c core.untrackedCache=false -c core.fsmonitor=false`, replaces the
  separate dirty and ignored probes, which fixes the failure under
  `status.showUntrackedFiles=no`.
- A registration-mismatched row is no longer status-probed; it is
  `inspection-error`.
- An unreadable worktree path gives that row `present: null`, an `os-error`,
  and `inspection-error`; at `a040790`, `main()` catches the `OSError` and
  refuses the whole repository with exit 2.
- A failed `git status` in the repository root gives the main worktree's
  row `inspection-error`, and the other rows are still reported; at
  `a040790`, `repo_state` raises `Refused` for it, ending `clean`,
  `status`, `doctor`, and `update` with exit 2.
- `ignored_files` becomes "observed, at least", is paired with
  `ignored_files_truncated`, and is `null` when the probe stopped before any
  ignored entry.
- The manifest's `tracking_branch` is read at `repository.root`, not at
  whichever directory `discover` returned.
- Under `clean`'s 60 s invocation deadline, where the baseline had none,
  each inspection Git child gets `min(5 s, work_remaining)` instead of the
  baseline `probe()` value of 15 s, and runs in its own process group;
  `status`, `doctor`, and `update` have no deadline and keep 15 s per Git
  child, and the `push` and `delete-branch` children stay unbounded (ruling
  D-W).
- Git 2.36 or newer is required to inspect a repository. The version check
  runs only when a Git repository is about to be inspected; a directory with
  no `.git` keeps `present: false`. `clean` and `overview` refuse with
  `git-too-old` or `git-unavailable`, exit 2, before any probe; under
  `--json` they print `{"error", "code"}`. `status`, `doctor` and `update`
  never refuse: `doctor` reports an old or unusable Git as an error check
  row and keeps its exit semantics for error rows; `status` marks rows it
  cannot inspect `inspection-error`;
  `update --apply --component tools|workflow` does not require Git. The
  overview checks once before any root is listed (ruling D-AF). The
  baseline `main()` prints a `Refused` under `--json` as `{"error"}`, with
  no `code`, which these refusals add.

Batch only (these concern `clean` resolution, removal, and the batch plan,
which the overview does not perform):

- A relative path or no argument resolves to the repository Git finds there,
  with `root` set to its main worktree, instead of going through `discover`.
- The report's `root` always names the command directory, the main worktree
  (or the bare directory, a later extension); at `a040790` it names whatever
  `discover` returned,
  such as a linked worktree's toplevel when `clean` runs inside one.
- A bare repository is refused in every `clean` mode with
  `target-not-repository-root` and exit 2, where at `a040790`, reached from
  one of its linked worktrees, its first registry record is reported as an
  `inspection-error` checkout.
- `push` refuses a `remote-gone` branch with refusal reason `remote-gone`
  and exit 2, where at `a040790` the branch reads `unpublished` and `push`
  republishes it with `push -u origin`; `push` and `delete-branch` also
  refuse with `inspection-incomplete`, `inspect-cap`, or `deadline-exceeded`
  and exit 2 when their re-inspection is incomplete.
- A gitfile main checkout, whose first registry record's path equals
  `common_dir`, resolves through `core.worktree`, and a submodule checkout,
  whose first record lies under `.git/modules`, is refused with
  `target-not-repository-root`; at `a040790` `clean` handles both with
  exit 0.
- Plain read-only `clean` runs as `mode: "report"` under the deadline with a
  256-row cap; above it the report is incomplete and exits 1, where at
  `a040790` plain `clean` exits 0 whenever it prints.
- `--apply --json` is accepted for `--all-safe` and `--action remove`,
  printing the apply result record, where `a040790` refuses `--json` with
  `--apply`; with `push` or `delete-branch` it stays refused.
- The removal command, single-target and batch alike, gains
  `-c status.showUntrackedFiles=normal`, `-c core.untrackedCache=false`, and
  `-c core.fsmonitor=false` (see "Residual window"), so Git's own check sees
  untracked files whatever the user's configuration.
- A worktree whose branch has no commit of its own is excluded as
  `unstarted-branch`; at `a040790` it classifies `merged-removable`.
- More than 16 eligible rows no longer block apply: the first 16 are
  selected and the rest deferred as `deferred-target-cap`.
- A worktree whose index flags an entry assume-unchanged or skip-worktree is
  never removed (`hidden-local-state`); sparse checkouts are therefore
  excluded.
- A worktree whose index holds a gitlink, or whose admin directory holds
  `modules`, is excluded as `contains-submodule`; at `a040790` it can be
  classified `merged-removable` and offered for removal, which Git then
  refuses with exit 128 whenever the submodule is populated or `modules`
  exists.
- Single-target `remove` runs through `retire_worktree` on the batch's seam.
  It gains the identity checks; the main-worktree, path-byte, registration,
  lock, unstarted-branch, submodule, and hidden-state gates; a plan whose
  completeness is the repository-wide evidence plus its own row, other
  rows' inspection errors and omissions being recorded as non-blocking; the
  refusal codes `worktree-not-found` and `target-excluded`, each refusal
  naming a manual remedy; the `unknown` outcome with exit 1; the removal
  floor; and its own process group for the removal child.

## Partial completion and recovery

The batch is ordered and not transactional, and it never rolls back a
completed removal by creating new work.

The normal successful result explicitly says that each local branch remains.
If a user later wants a retained branch deleted, the existing explicit command
is the recovery path:

```sh
project clean /home/user/projects/Atlas \
  --apply --action delete-branch --branch feature/login
```

That command creates a fresh report, rechecks local merge-target ancestry and
the current branch tip, and leaves the branch intact if Git refuses deletion.
It gives a retry path after a worktree-only batch without inventing an implicit
branch operation. Remote branches remain untouched.

An `unknown` or `failed` target is never retried automatically, and `project`
never forces a removal or deletes a directory itself. The target's
reconciliation record says what remains, and a fresh read-only plan shows the
current state:

- Registry entry absent and path present (`orphaned-directory`): Git
  unregistered the worktree but could not delete its directory, for example
  after a permission error with exit 255. No later plan lists the directory;
  the user inspects it and deletes it by hand.
- Registry entry present with `.git` intact but tracked files missing: a later
  plan reports the row `dirty` and preserves it, and when its only working
  changes are deletions of tracked files the report's ladder text carries
  the partial-removal note beside, never instead of, the dirty
  classification.
- A removal killed at the 300 s hard ceiling: the target is `unknown` with
  the `partially-removed` note and the recovery text "inspect, then
  `git worktree remove --force <path>` by hand".
- `.git` already deleted: Git lists the entry as `prunable`, the registration
  check fails, and a later plan reports the row as `registration-mismatch`
  with classification `inspection-error`, which keeps every plan for the
  repository incomplete until the user repairs or prunes the entry by hand
  after review.

In every case the branch remains merged and retained.

## Deferred cache and paired-retirement extension

Cache disposal and paired local-branch retirement are separate future design
options because neither is part of `origin/main`'s current batch contract.
The batch removes only worktrees with no ignored files, so caches such as
`__pycache__` keep a worktree out until the cache-disposal change; in one
surveyed repository 20 of 29 merged worktrees were excluded for caches
alone, which is the evidence for that follow-on. They must not be smuggled
into the MVP's `removed` stage. Either extension
would run inside `retire_worktree` under the same deadline, with stage values
of its own (cache disposal before the worktree removal, branch deletion after
`removed` is proven by rescan), and would count its mutations in
`operations.estimated` and its bounds in `limits`.

If cache disposal is proposed later, a candidate path or any ancestor that is
a symlink is ineligible for cache deletion and is preserved. The implementation
must use descriptor-relative, no-follow operations (`O_NOFOLLOW`/equivalent),
verify the opened directory identity against the planned device/inode, and
fail closed when the platform cannot provide those guarantees. A pathname
check followed by recursive deletion is insufficient because a writable parent
could be replaced between the check and the delete.

The cache extension must report each cache path separately. If a later path
fails, earlier removals remain recorded as permanent partial cache completion;
the report rescans the worktree, marks the cache phase partial, and gives
retry guidance. It must stop before worktree or branch mutation when cache
preflight fails. A proposal must also set hard limits for cache entries and
bytes and include them in the plan estimate.

If paired retirement is proposed later, branch deletion remains a separate
post-removal stage with an immediate branch-head and local-ancestry check that
uses the reconciliation record's `branch_sha` as the expected head. A changed
head or a Git refusal retains the branch, stops later targets, and reports the
already removed worktree plus the surviving branch. The existing explicit
`delete-branch` command remains the retry path. No future composite operation
may force-delete or force-push.

## Validation scenarios

Each scenario also asserts that nothing outside its stated removals changes.
Three platform limits apply: the non-UTF-8 path scenarios cannot be built on
macOS APFS; raw-byte order differs from Git's `core.ignoreCase` order on a
case-insensitive APFS volume; and a WSL2 `/mnt/c` mount does not guarantee
stable inode numbers. The scenarios that depend on them are Linux-only and
are skipped elsewhere with a reason.

### Selection, caps, and probe work

- **Stable order and preserved work.** Several eligible trees retire in
  canonical path order; current, merge-target, dirty, locked, remote-ahead,
  and unmerged trees remain, every retained local branch is reported, and no
  push, fetch, force option, branch deletion, or remote deletion occurs. The
  same holds when the merge-target branch is checked out in no worktree, the
  main worktree being on another branch: every removal runs from the command
  directory and succeeds.
- **Row cap and planning failures.** More than 128 registered worktree rows,
  or a probe timeout or deadline during planning, produces an incomplete
  read-only plan (`inspect-cap`, `inspection-incomplete`, or
  `deadline-exceeded`) with `omitted` and the timed-out rows visible; with
  more than 128 rows, the main worktree and the 127 linked worktrees with the
  smallest paths are the ones inspected. The preview exits 1, and `--apply`
  refuses with exit 2 before any mutation.
- **Target cap.** More than 16 rows that pass every gate before
  `contains-submodule` produce a complete read-only plan that selects the
  first 16 in canonical order and lists the rest as `deferred-target-cap`
  with the next command, `apply_allowed` is true, and the preview exits 0;
  `--apply --yes` removes the 16, and a re-run selects the next 16.
- **Unstarted branch.** Given `git worktree add -b x` followed by
  `git push -u` with no commit, when the batch previews, then that worktree
  is excluded as `unstarted-branch`.
- **Every protected classifier.** Given one repository whose linked
  worktrees are stale, detached, dirty, holding ignored files, unpublished,
  remote-gone (an upstream whose remote-tracking ref is missing), diverged,
  remote-ahead, unpushed, pushed-unmerged, merged but current, merged but
  locked, merged with a non-UTF-8 path, merged with an initialized
  submodule, and merged with an assume-unchanged entry, plus the main
  worktree on the merge target and exactly one plain merged, clean,
  published worktree, when the batch previews and applies, then only that
  last worktree is selected and removed, every other row is excluded with the
  reason the gate order gives, and the exit status is 0. A copy that
  adds one unreadable worktree, or one with a broken admin registration,
  yields `inspection-error`, an incomplete plan, and exit 2 under `--apply`
  with zero mutation. `review-required` is not constructible from Git state
  under the shared evidence model; it stays in the ladder as a defensive
  branch and is covered by classifier tests on injected rows.
- **Hidden local state.** Given otherwise eligible worktrees, one with an
  edit to a file flagged assume-unchanged and one with a file flagged
  skip-worktree, each flag set only in that worktree's own index while the
  main worktree's index flags nothing, when the batch previews, then both are
  excluded with `hidden-local-state`, because the hidden-state probe ran
  inside each worktree, and the edits survive. When a flag is set on a
  selected target after confirmation and before its revalidation, that
  target is `refused` with `hidden-local-state`, later targets are
  `not-attempted`, and the exit status is 2.
- **Submodules.** Given otherwise eligible worktrees, one whose submodule is
  initialized, one whose submodule was initialized and then deinitialized,
  one whose gitlink was never initialized, and one whose branch no longer
  has a gitlink but whose admin directory still holds `modules`, plus one
  plain eligible worktree, when the batch previews and applies, then the
  first four are excluded with `contains-submodule`, the third through its
  gitlink record in the hidden-state probe and the others through the
  `modules` check, and only the plain worktree is removed. Given a confirmed
  plan, when a `modules` directory is created in a selected target's admin
  directory before its revalidation, then that target is `refused` with
  `contains-submodule`, later targets are `not-attempted`, and the exit
  status is 2.
- **Ignored-file bound.** Given a merged, clean worktree holding 70 ignored
  files, when the plan is built, then the probe stops when the 65th ignored
  record arrives, the row has `ignored_files: 64`,
  `ignored_files_truncated: true`, and 8 `ignored_samples` paths, and it is
  excluded as `ignored-local-files`. With exactly 64 ignored files, the row
  has `ignored_files: 64` with `ignored_files_truncated: false` and is still
  excluded as `ignored-local-files`. Given a worktree with 4,097 untracked
  entries and no ignored ones, the probe stops at the 4,097th record, the row
  has `ignored_files: null`, `ignored_files_truncated: true`, `dirty: true`,
  and classification `dirty`, and the plan stays complete.
- **Bounded revalidation work.** Given five worktree rows (the main worktree
  and four linked worktrees), three of them selected, and a counting `git`
  wrapper on `PATH`, when `project clean <root> --all-safe --apply --yes`
  runs, then before the apply phase it spawns F + 5 + 3 probe children; after
  it, every target's `probes_performed` is at most 5, the final rescan spawns
  3, three removals run, no `for-each-ref --merged` and no status probe of a
  non-selected worktree runs, the post-confirmation probe total is at most
  5T + 3 whatever the row count, and the record's `probes.performed` equals
  the wrapper's count. The wrapper also records each child's `-C` directory:
  every `status` and `ls-files` child names its own worktree, and every other
  child after resolution, the removals included, names the command
  directory.
- **Paths and empty plans.** Space-containing paths, missing external paths,
  empty plans, locked worktrees, and incomplete inspection keep the same
  safety rules as the single-target command.

### Safety boundary

- **Target directory replaced.** Given a confirmed plan whose first target P
  has recorded `dev`, `ino`, and `admin_id`, when P is moved aside and a new
  directory or a symlink is put at P before its revalidation, then P is
  `refused` with `identity-changed`, no child is spawned, later targets are
  `not-attempted`, and the exit status is 2.
- **Admin registration changed.** Given the same plan, when P's `.git` file is
  rewritten to name another admin directory, or P's admin `gitdir` file is
  changed to name another path, then P is `refused` with `identity-changed`
  and exit 2; a fresh plan reports the row as `registration-mismatch` with
  classification `inspection-error` and is incomplete.
- **Parent directory swapped.** Given a target under
  `/home/user/projects/Atlas-worktrees`, when that directory is replaced by a
  symlink to a copy of it, then the target's realpath differs, and it is
  `refused` with `identity-changed` and exit 2.
- **Repository replaced mid-batch.** Given a three-target plan, when the
  repository root is renamed and another clone is moved into its path, or
  the root's parent directory is replaced by a symlink to a copy, after the
  first target's removal child exits 0 and before the rescan that follows
  it, then that rescan's identity probe finds a different `repository`, so
  the first target is `unknown` with `unconfirmed-removal`, every
  reconciliation field `null`, and `reconciled: false`, although its removal
  may have succeeded; the second and third targets are `not-attempted` with
  `batch-stopped`, the rescan's three children are the final rescan, and the
  exit status is 1. When the same replacement happens before the first
  target's revalidation instead, it is observed before any spawn: the first
  target is `refused` with `identity-changed`, the later targets are
  `not-attempted`, nothing is removed, and the exit status is 2.
- **New worktree and pre-removal changes.** A new linked worktree registered
  after confirmation is not selected. A changed merge-target SHA, feature
  branch tip, upstream OID, lock, ignored-file state, or classification of any
  target before the first removal causes zero mutations and exits 2 with the
  matching reason.
- **State changes before revalidation.** Given a confirmed plan, when an
  ignored file is created in a target, the merge target gains a commit, the
  manifest's `tracking_branch` is edited to name another existing branch, or
  the manifest is made unparseable, before that target's revalidation, then
  it is `refused` with `state-changed` and exit 2; a change that the preflight
  finds removes nothing at all. The same holds for a plan resolved through
  `origin/HEAD` when the manifest gains a `tracking_branch` naming an
  existing branch, such as `release`, that the narrowed ref listing does not
  name, and when `refs/remotes/origin/HEAD` is repointed to another existing
  branch.
- **Changed later target.** A target that changed after earlier removals
  stops the batch and the record reports the earlier targets' retained
  branches and completed stages accurately.
- **Untracked file under `status.showUntrackedFiles=no`.** Given that setting
  in the user's configuration and a test hook that creates an untracked file
  in the target after its revalidation, when the batch runs, then Git refuses
  with exit 128, the target is `failed` with `git-refused` and its
  reconciliation shows the registry entry and path present, the file
  survives, later targets are `not-attempted`, and the exit status is 128.
- **Untracked cache.** Given `core.untrackedCache=true`,
  `core.checkStat=minimal`, and an index-writing `git status` already run in
  the target, when a test hook creates an untracked file after the target's
  revalidation, then Git, run with the pinned configuration, refuses with
  exit 128, the target is `failed` with `git-refused`, and the file
  survives.
- **Ignored file in the residual window.** Given a test hook that creates an
  ignored file after the target's revalidation and before the child starts,
  when the batch runs, then Git removes the worktree with exit 0, the target
  is `removed`, the file is gone, and the result text carries the
  residual-window line; this documents the boundary rather than a guarantee.
- **Branch advances before removal.** Given a confirmed plan, when the
  target's branch gains a commit before its revalidation, then it is
  `refused` with `branch-changed`, its reconciliation shows the new
  `branch_sha`, later targets are `not-attempted`, the branch is retained at
  the new commit, and the exit status is 2.
- **Branch advances after removal.** Given a test hook that advances the
  target's branch after Git removed the worktree and before the rescan, when
  the batch runs, then the target is `removed` with
  `branch-advanced-after-removal`, its reconciliation has
  `registry_entry_present: false`, `path_present: false`,
  `branch_present: true`, and a `branch_sha` that differs from `planned_sha`,
  later targets are `not-attempted`, no commit is lost, and the exit status is
  2. A hook that deletes the branch instead yields
  `branch-missing-after-removal` with `branch_present: false` and exit 2.

### Execution, interruption, and recovery

- **Deadline expiry mid-batch.** Given three targets and a test Git whose
  removal of the second target outlasts the work deadline, when the deadline
  passes, then `project` does not signal the removal child; when the child
  exits, the second target is reconciled as usual, the third is
  `not-attempted` with `deadline-exceeded`, and the exit status is 1. Given
  instead a test Git whose first removal is slow enough that less than
  `removal_floor_seconds` (5 s) of the work deadline remains when the second
  target passes revalidation, then no second child is spawned, the second
  and third targets are `not-attempted` with `deadline-exceeded` and
  `reconciliation: null`, and the exit status is 1.
- **Hard ceiling.** Given a test Git whose removal never exits, when 300 s
  pass, then its group is killed, the target is `unknown` with the
  `partially-removed` note and the recovery text, later targets are
  `not-attempted`, and the exit status is 1. Given `project` killed with
  SIGKILL during a deletion, a rerun of the report shows the partial-removal
  note beside the row's `dirty` classification.
- **Exit 0 without evidence.** Given a test Git that exits 0 without removing
  anything, when the batch runs, then the target is `unknown` with
  `unconfirmed-removal`, later targets are `not-attempted`, and the exit
  status is 1.
- **SIGINT.** Given a batch whose second removal is in flight, when SIGINT
  arrives, then `project` does not signal the removal child, waits for it to
  exit, and reconciles it; later targets are `not-attempted` with
  `interrupted`, and the exit status is 130 even though the second target's
  outcome would otherwise make it 1; SIGINT or end of input at the
  confirmation prompt exits 130 with zero mutation.
- **Git leaves an orphaned directory.** Given a target containing a
  subdirectory without write permission, when Git unregisters the worktree but
  fails to delete its directory and exits 255, then the target is `failed`
  with `git-failed` and `exit_status: 255`, its reconciliation shows
  `registry_entry_present: false`, `path_present: true`, and the retained
  branch with its SHA, its `notes` is `["orphaned-directory"]`, later targets
  are `not-attempted`, and the exit status is 255. No later plan lists the
  directory, and nothing deletes it.
- **Git refuses the removal.** Given a lock added to a target after its
  revalidation, when the batch runs, then Git refuses with exit 128, the
  target is `failed` with `git-refused`, the record holds the command, the
  exit status 128, and a reconciliation with registry entry and path present,
  later targets are `not-attempted`, every retained branch is reported, and
  the exit status is 128.
- **Unreadable path after removal.** Given a test hook that makes the target's
  parent directory unreadable after Git exits 0, when the rescan runs, then
  `lstat` fails with `EACCES`, `path_present` is `null`, `reconciled` is
  false, the target is `unknown` with `reconciliation-incomplete`, the record
  is printed, and the exit status is 1.
- **Exception after the apply phase begins.** Given a fault injected into the
  first target's reconciliation, when the batch runs, then that target is
  `unknown` with `internal-error`, later targets are `not-attempted`, the
  result record is printed, and the exit status is 1.
- **Single target equals a one-item batch.** Given two fresh copies of a
  repository, used in turn at the same path, in which P is the only eligible
  linked worktree, when one runs
  `project clean <root> --apply --action remove --worktree P --yes` and the
  other `project clean <root> --all-safe --apply --yes`, then both plans show
  the same `selected` entry for P (apart from `dev` and `ino`), both run the
  same argument vector, and both end with P `removed` and exit 0. When P is
  made dirty between confirmation and revalidation in both copies, both refuse
  with `state-changed`, the same message, and exit 2. When another worktree in
  the repository is unreadable, the batch refuses with
  `inspection-incomplete`, while the single-target run records that row as a
  non-blocking omission and removes P; with 17 eligible rows, or more than
  128 registered rows, `--worktree P` still removes P.
  `--worktree` naming an unregistered path refuses with `worktree-not-found`,
  and naming a dirty worktree refuses with `target-excluded` and
  `reason: "dirty"`.
- **Preview is advisory.** Given a preview that selects only P1, when P1
  becomes dirty before `project clean <root> --all-safe --apply --yes` runs
  without `--expect-plan`, then the fresh plan excludes P1 as `dirty`, prints
  "No eligible worktrees", and exits 0 without prompting.
- **Plan digest mismatch.** Given a preview with digest D that selects P1,
  when a second merged worktree becomes eligible, or P1's branch advances,
  before `project clean <root> --all-safe --apply --yes --expect-plan D` runs,
  then the fresh plan is printed with a different digest, the run refuses with
  `plan-digest-mismatch` and exit 2 before any prompt or removal, and nothing
  changes. When only an excluded worktree changed, the digest is still D and
  the apply proceeds.

### Paths, resolution, and handoff

- **Control-character and non-UTF-8 paths.** Given eligible linked worktrees
  whose paths contain a newline, a tab, U+0001, and U+202E, and an otherwise
  eligible one whose path contains byte 0xFF, when the batch previews and
  applies, then the first four are selected with exact JSON strings and
  `path_valid_utf8: true`, the human plan prints them in `$'…'` form with
  `\u000a`, `\u0009`, `\u0001`, and `\u202e`, Git receives each raw path as
  one argument, and a rescan proves each removed. The fifth is excluded with
  `unsupported-path-bytes`, shown with `\xff` and `path_valid_utf8: false` in
  both `worktrees` and `excluded`, never passed to a removal command, and
  still present afterwards.
- **Non-UTF-8 repository root.** Given a repository whose root path contains
  byte 0xFF, when `project clean <that root> --all-safe` runs, then it refuses
  with `unsupported-path-bytes` and exit 2, no plan or digest is built, and
  nothing changes.
- **Overview handoff keeps identity.** Given an overview row whose
  `repository` holds the Atlas root, common directory, `dev`, and `ino`, a
  housekeeping finding that supplies the row's `suggested_command`
  `["project", "clean", "/home/user/projects/Atlas", "--all-safe"]`, and an
  independent clone also named Atlas under a second configured projects
  directory, when that argument vector runs without a shell, then the path
  resolves Git first, the plan's `repository` equals the row's four fields,
  and the other clone is never inspected. The same holds when an ancestor of
  the Atlas root holds `project.yaml` or the root contains
  `Atlas/family.yaml`, the two cases in which the baseline `discover` would
  redirect: the plan still names the Atlas repository itself, and the
  read-only `["project", "clean", "/home/user/projects/Atlas"]` reports
  `root` as the Atlas root too. In the base fixture, without the family
  holder, running `project clean Atlas --all-safe` keeps the baseline name
  lookup and is refused with `ambiguous-name` and exit 2.
- **Absolute path that is not a repository root.** Given absolute paths to a
  subdirectory of the Atlas root, to one of its linked worktrees, to a
  directory outside any repository, and to a bare repository, when each is
  passed to `project clean <path>` in the read-only form, with
  `--all-safe --apply --yes`, and with `--apply --action remove`, `push`, or
  `delete-branch`, then each is refused with `target-not-repository-root` and
  exit 2 before any plan is built, no other directory is substituted, and
  nothing changes.
- **Gitfile main checkout and submodule checkout.** Given a repository made
  with `git init --separate-git-dir`, whose first registry record's path
  equals `common_dir`, when `project clean` runs on the realpath of its
  `core.worktree`, then it resolves and plans as usual; given a submodule
  checkout, whose first registry record lies under `.git/modules`, it is
  refused with `target-not-repository-root` and exit 2.
- **Merge target missing, invalid, or conflicting.** Given a repository with
  no manifest `tracking_branch`, no `origin/HEAD`, and neither `main` nor
  `master`, when the batch runs, then it refuses with `no-merge-target` and
  exit 2 before any mutation, and `--json` prints the extended error object.
  A manifest of the wrong kind refuses with `manifest-invalid` the same way.
  Given a manifest naming `release` and `origin/HEAD` naming `main`, both
  existing, then `merge_target` is `release` with `source: manifest` and its
  SHA, the plan carries a `merge-target-conflict` note, and apply is allowed.
  Given no manifest candidate, local `trunk` and `main`, and
  `refs/remotes/origin/HEAD` pointing at `refs/remotes/origin/trunk`, then
  `merge_target` is `trunk` with `source: origin-head`, not `main`.

### Deferred extensions

- A future cache extension rejects symlink candidates and ancestor swaps,
  leaves external targets intact, reports each path after partial failure, and
  never follows a symlink or uses broad recursive deletion.
- A future paired-retirement extension retains a branch when its head changes
  after revalidation and permits retry through explicit `delete-branch`.

## Alternatives and open decisions

Continuing after failures would maximize cleanup but make partial state harder
to reason about. Prefer stop-on-first-failure, consistent with current
retirement. A persistent resumable plan adds stale-state and storage contracts;
defer it.

A writer-quiescence or ownership handoff, in which editors, agents, and other
`project` invocations honor a lock or lease before removal, was the other way
to close the safety finding. The MVP rejects it because nothing on the
workstation honors such a lock today; the narrow guarantee plus Git's own
refusals is what the MVP can actually deliver, and a later design may add a
handoff on top of the same seam.

Open proposal decisions:

- The measured per-child and per-removal costs, and therefore the final caps
  under the stated rule; the caps stay provisional until measured.
- For Brett Heap: whether a local ancestry proof should outrank
  `remote-gone` for worktree rows. Lane openRepoProject-3 raised it,
  recommending yes, and lane openRepoProject-2 carries it in both proposals.
  The ladder tests remote presence before merge state, as the baseline does;
  GitHub's head-branch auto-delete with `fetch.prune` leaves a merged
  branch's upstream gone; and the MVP never deletes a branch, so under the
  baseline order such a worktree is never eligible for `--all-safe`, and
  `push` now refuses its branch. Measured here: 4 of about 90 merged
  worktrees, `fetch.prune` unset everywhere, and auto-delete on 2 of 21
  repositories. Until it is ruled, the packet keeps the baseline ladder; a
  `remote-gone` row whose `merged_into_target` is true carries the
  recommendation "Merged locally, upstream deleted: not removable by
  `project` until the open question is ruled; review, then
  `git worktree remove` yourself", and the overview's `remote-gone` message
  says whether the branch tip is already an ancestor of the merge target
  when its evidence establishes that, its suggestion only reviewing.
- For Brett Heap: squash merges never satisfy the ancestry proof, so the MVP
  selects little in a squash-merge repository. The recommendation is a local
  patch-equivalence proof (`git cherry` or patch-id against the merge
  target), designed as a follow-on change, not in the MVP.
- Change 1 council V4, single-target `remove` completeness (other rows'
  inspection errors no longer block it): departure, open to Brett Heap's
  ratification.
- Change 1 council V5, the deferred target cap (more than 16 eligible rows
  are drained 16 per run instead of refused): departure, open to Brett
  Heap's ratification.
Every other open decision this document listed is decided: the 2026-10-08
proposals took them as proposal decisions, open to ratification, as the
[fix handoff](next-session-project-maintenance-fix-handoff.md) records under
"Decisions taken by the proposals — 2026-10-08".

## Relationships

The [maintenance flow](project-maintenance-synthesis-inspect-and-retire.md)
explains the boundary with [project overview](project-maintenance-project-discovery.md).
The [packet overview](project-maintenance-overview.md) describes the overall scope.
