Lane: openRepoProject-2

# Contract: `project clean`

The command-line contract of `project clean` after this feature, with the
changes it makes to `status`, `doctor` and `update` at the end. The exact
text of every new human line is fixed in `design.md` D18 (and D14 for the
report) and is named here by a label in quotes, such as "D18 question";
stages and exit statuses are D19's, tabled in
[data-model.md](../data-model.md). Unchanged behaviour is stated only where
this feature meets it. Line citations are at `961c405`.

## Invocation

```text
project clean [TARGET] [--json]
project clean [TARGET] --all-safe [--json] [--apply [--yes] [--expect-plan D]]
project clean [TARGET] --apply --action remove --worktree PATH [--yes] [--json]
project clean [TARGET] --apply --action push --branch BRANCH [--yes]
project clean [TARGET] --apply --action delete-branch --branch BRANCH [--yes]
```

New flags: `--all-safe` and `--expect-plan D` (FR-019); no flag is added
outside `clean` (FR-064). `project` reads no new environment variable, flag
or file to change a limit or a time (research.md R10). It removes the
seventeen names below from every Git child's environment, never from its own,
except that the push child keeps `GIT_ALLOW_PROTOCOL` (R-28).

## Argument checks (before any Git child)

Each refuses with `invalid-arguments` and exit 2 and runs nothing:

| Input | Note |
| --- | --- |
| `--all-safe` with `--action`, `--branch` or `--worktree` | new |
| `--expect-plan` without both `--all-safe` and `--apply` | new |
| an `--expect-plan` value that does not match `^[0-9a-f]{64}$` | new |
| `--apply --json` with `--action push` or `--action delete-branch` | kept refused (OQ-10) |
| `--apply` with neither `--all-safe` nor `--action`; push or delete-branch without `--branch`; remove without `--worktree` | baseline messages kept, now with this code |

`--apply --json` is accepted with `--all-safe` and with `--action remove`,
where the baseline refused it for every action (`project:671-672`). An
argument-parser usage error prints the parser's message, exits 2 and prints
no JSON document, as before.

Flags this table does not refuse keep the baseline's handling: without
`--apply`, `--yes`, `--action`, `--branch` and `--worktree` are ignored,
and an unused `--branch` or `--worktree` is ignored. `--worktree P` is
expanded, joined to the working directory and realpath'd by one bounded
call; it names the one registry row whose path equals it, or else whose
realpath does (`worktree-not-found` otherwise).

## Order of a run

1. Argument checks.
2. `git --version`, once (row 1): `git-unavailable` or `git-too-old`, exit
   2, before any repository is probed.
3. Resolution (below), then `unsupported-path-bytes` for a `root` or
   `common_dir` that is not valid UTF-8.
4. The manifest read at `root`, row 6, and the merge target over row 6's
   listing: `manifest-invalid`, `no-merge-target`.
5. Planning under the deadline (row 7, then each row in order; in
   single mode P is matched first, `worktree-not-found` if absent, and
   probed first), the gates and the deferral, then `plan_digest`.
6. Plan checks, in this order: an incomplete plan (a preview or report exits
   1; with `--apply`, exit 2 before any question, coded
   `inspection-incomplete`, `inspect-cap` or `deadline-exceeded`); an
   `--expect-plan` mismatch (`plan-digest-mismatch`, exit 2, the fresh plan
   still printed); a complete `all-safe` plan selecting nothing ("D18 empty
   line", exit 0, no question); in single mode, P excluded by a gate
   (`target-excluded`, exit 2).
7. A preview or report prints and ends. An apply prints its plan with "D18
   residual-window line", then: `--yes` accepts it; a standard input that is
   not a terminal refuses with `confirmation-required`, exit 2; otherwise
   "D18 question" is asked (below).
8. The apply phase: per target in canonical order, revalidate, spawn the
   removal while the 5 s floor remains, wait, rescan; continue only after a
   plain `removed`.
9. The final rescan within the 10 s reserve, the result, the exit status.

## Resolution (FR-016, FR-017; D8)

| Argument (after `expanduser`) | Resolves to | Refusal |
| --- | --- | --- |
| absolute path | itself, when its realpath equals the toplevel Git reports there and that toplevel is the main worktree | `target-not-repository-root` |
| relative path: any relative argument containing a `/` (`./x`, `x/`), `.`, `..`, or none | the repository Git finds at that directory joined to the working directory; `root` is its main worktree | `target-not-repository-root` where Git finds no worktree |
| bare name: a relative argument with no `/`, not `.` or `..` (research.md R13) | `discover()`'s name lookup, its one Git child counted and bounded, then the directory it returns resolved as a worktree toplevel | `ambiguous-name`, `repository-not-found` |

Then, in this order (M6): a submodule checkout (row 3 prints a third line)
is refused; a first registry record that is `bare` is refused; a first
record equal to `common_dir` takes `core.worktree` (row 4b) or else the
candidate toplevel whose `.git` file names `common_dir`, and is refused when
neither names it; otherwise the first record is the main worktree. Every
refusal here is `target-not-repository-root`, exit 2, before any plan. The
family-holder and manifest-ancestor redirections (`project:455-461`) never
apply to a path argument. The command directory is `root`: every
repository-wide Git child after resolution, every removal and the manifest
read use it.

## The removal question (FR-026; research.md R3)

| Aspect | Contract |
| --- | --- |
| Asked | `--all-safe --apply` or `--action remove`, without `--yes`, standard input a terminal, after the plan is printed |
| Text | "D18 question", the singular for one; written by `project` to the human stream (below), never by `input()` |
| Accepts | `yes`, surrounding whitespace ignored |
| Any other answer (`y`, empty, `no`, ...) | refusal `cancelled`, exit 2, nothing removed |
| End of input | `Cancelled.` on standard error, exit 130, no JSON document |
| SIGINT, SIGTERM, SIGHUP | `Cancelled.`, exit 130, 143 or 129, no JSON document |

It replaces `Type yes to run this plan:` for the removal apply only;
`confirm()` (`project:152-154`), as `new`, `update`, push and delete-branch
use it, is unchanged, and so are its signals (research.md R4).

## Streams (FR-044)

| Run | Standard output | Standard error |
| --- | --- | --- |
| report or preview | the human report or plan | `REFUSED: ...`, `Cancelled.` |
| report or preview, `--json` | one JSON document: the plan envelope, or the extended error object | `Cancelled.` |
| `--apply` (removal) | the plan, the question, progress, "D18 wait line", the result | `REFUSED: ...`, `Cancelled.` |
| `--apply --json` (removal) | one JSON document: the plan envelope or the extended error object when the run stops before the apply phase, otherwise the apply result record | the plan, the question, progress, "D18 wait line", the result text, `Cancelled.` |
| push, delete-branch | `Cleanup action: ...`, the plan (`Working directory:` and the command, through the path-escaping printer below), `Type yes` and the delegate's own output, as today | `REFUSED: ...`, `Cancelled.`, the delegate's own |

Under `--json` a refusal is a JSON document on standard output, never a
`REFUSED:` line. Three cases print no JSON document: a parser usage error;
SIGINT, SIGTERM or SIGHUP before the apply phase; and end of input at the
question.

`invalid-arguments`, `internal-error` and every resolve refusal print the
extended error object; `worktree-not-found`, `target-excluded`, the plan
codes, `plan-digest-mismatch`, `confirmation-required` and `cancelled`
print the plan envelope with `apply_allowed: false` and the refusal in
`refusals`. Every document is `json.dumps(doc, indent=2,
ensure_ascii=True)` and one newline, keys in the order tabled here. Row and
target `notes` are arrays of code strings; plan `notes` are `{code,
message}` objects, an `inspect-cap` note adding `rows`.

## Human output (D18, D14)

| Label | Where |
| --- | --- |
| baseline header | `Cleanup plan for ROOT`, `Merge target: NAME (SOURCE)`, `Freshness:` |
| "D14 completeness line" | report: `Report: complete` or `Report: incomplete (CODES)` |
| "D14 selection line" | report at 128 rows or fewer: `--all-safe would select N`; above: `--all-safe would be incomplete (inspect-cap)` |
| "D18 preview layout" | `Selected (N):` with one `  remove PATH [BRANCH]` per row; `Excluded (M):` with one `  REASON (K): NEXT STEP` group per reason and `    PATH [BRANCH]` rows; an `ignored-local-files` row adds its count and first sample |
| "D18 deferral line", "D18 non-drain line" | the `deferred-target-cap` group; the line shown when all 16 rows past the cap are `contains-submodule` |
| "D18 next steps" | the next step for each reason |
| "D18 residual-window line" | the confirmation and the result |
| "D18 empty line" | `No eligible worktrees` |
| "D18 question", "D18 wait line" | above; the wait line once, at the first signal or deadline during a removal (D9) |
| "D18 success line", "D18 stop block" | the result; the stop block names the retained branches and the residual window |
| "D18 partial-removal note" | under the `dirty` advice of a row, or on a `partially-removed` target |
| "D18 refusal messages", "D18 remedies" | `target-excluded` (the current-worktree and class messages kept), gates, and the plan-blocking remedies |

Lines D18 leaves open are fixed here before tasks: the `Report:` and
`--all-safe would ...` lines follow `Freshness:`; `Excluded` groups follow
the gate order, classes in ladder order; one progress line per target,
`  STAGE PATH` or `  STAGE PATH (REASON)`; the retained-branch line
`Branches kept: B1, B2.`; a plan-blocking refusal prints the plan, then
`REFUSED: MESSAGE`; each code with no baseline message gets one here:

| Code | Message |
| --- | --- |
| `invalid-arguments` | `--all-safe cannot be combined with --action, --branch or --worktree.`; `--expect-plan requires --all-safe and --apply.`; `--expect-plan takes 64 lowercase hexadecimal characters.`; the baseline messages for the baseline cases |
| `internal-error` | `TYPE: TEXT`, the exception's class and text, so `REFUSED: RuntimeError: boom` (research.md R6) |
| `git-unavailable` | `Git is unavailable (DETAIL); clean needs Git 2.36 or later.`, DETAIL one of `not found`, `exit N`, `timed out`, `unparseable version` |
| `git-too-old` | `Git VERSION is older than 2.36; clean needs Git 2.36 or later.` |
| `target-not-repository-root` | `Not the main worktree of a repository: PATH; pass the repository root.` |
| `unsupported-path-bytes` | `The repository path is not valid UTF-8: PATH` |
| `manifest-invalid` | `Manifest PATH is larger than 1 MiB.`; the baseline `Cannot read PATH: ...` and `Unexpected kind in PATH; expected project-manifest` otherwise |
| `inspection-incomplete`, `inspect-cap`, `deadline-exceeded` | `The plan is incomplete (CODE): REMEDY.`, REMEDY being "D18 remedies" |
| `plan-digest-mismatch` | `The fresh plan's digest DIGEST differs from --expect-plan EXPECTED; nothing was changed.` |
| `confirmation-required` | `Standard input is not a terminal; pass --yes to apply this plan.` (the removal question; `confirm()` keeps its own) |
| push, `remote-gone` | `Cannot push BRANCH; its upstream UPSTREAM was deleted (remote-gone); review it before it is republished.` |

`repository-not-found`, `ambiguous-name`, `no-merge-target`,
`worktree-not-found` and `cancelled` keep the baseline's messages, and
`target-excluded` is "D18 refusal messages".

All new text is ASCII. A path prints verbatim in prose and shell-quoted in
commands, unless it holds a code point of general category Cc, Cf, Zl or Zp
or an undecodable byte; then it prints as `$'...'` with `\xHH`, `\uXXXX` or
`\UXXXXXXXX` in lowercase hexadecimal, each backslash doubled and each single
quote as `\'` (FR-041). The baseline report keeps its other lines.

## JSON (FR-039 to FR-044)

Every `project clean --json` prints one document with `schema_version: 1`.
Paths: a valid UTF-8 path is an ordinary string with every Cc, Cf, Zl or Zp
code point as a JSON escape and `path_valid_utf8: true`; any other path
writes each undecodable byte as `\xHH` and each literal backslash doubled,
with `path_valid_utf8: false`. Null means unknown or not established. Enums
are closed within the version.

### Plan envelope

| Field | Type and contract |
| --- | --- |
| `schema_version` | 1 |
| `observed_at` | RFC 3339 UTC, seconds, `Z` |
| `mode` | `report`, `single` or `all-safe` |
| `root` | baseline key; the command directory, `repository.root` |
| `target_branch` | baseline key; `merge_target.name` |
| `tracking_freshness` | baseline key and text |
| `worktrees` | rows, main worktree first, then by raw path bytes (data-model.md) |
| `repository` | `root`, `common_dir` (strings), `dev`, `ino` (integers), `root_valid_utf8`, `common_dir_valid_utf8` (true) |
| `merge_target` | `name`, `source`, `sha` |
| `limits` | `worktree_rows` (the mode's cap, 128 or 256), `targets` (16), `ignored_entries` (64), `status_records` (4096), `ignored_samples` (8), the values in force |
| `budget` | `probe_timeout_seconds` (5), `invocation_timeout_seconds` (60), `reconciliation_reserve_seconds` (10), `removal_floor_seconds` (5), `removal_ceiling_seconds` (300), `probe_concurrency` (1), the values in force |
| `probes`, `operations` | `{estimated, performed}` integers: `probes` counts every Git child other than a removal, `operations` the removals, each child once (lead ruling R-27); `estimated` is the upper bound for an `--apply` run of this plan in every mode, previews included: F + W + E + 5T + 3 and T (research.md R8) |
| `selected` | array in canonical order, or null in a report above 128 rows; each entry: `path`, `path_valid_utf8`, `branch`, `head`, `upstream`, `upstream_oid`, `ahead`, `behind`, `dev`, `ino`, `admin_id`, `locked`, the baseline signature fields (`present`, `dirty`, `ignored_files`, `remote_present`, `merged_into_target`, `current`, `classification`), and `operation` (`{kind: "worktree-remove", argv}`, the exact argument vector) |
| `excluded` | array in canonical order: `path`, `path_valid_utf8`, `branch` (or null), `classification` (or null when never classified), `reason` |
| `omitted` | `{count, exactness: "exact"}` |
| `notes` | `{code, message}` objects; `merge-target-conflict`; in single mode the non-blocking `inspection-incomplete`, `inspect-cap`, `deadline-exceeded`; in a report above 128 rows `inspect-cap` with `rows` |
| `completeness` | `complete` or `incomplete` |
| `apply_allowed` | false for every report, and for any incomplete or refused plan |
| `refusals` | refusal objects |
| `plan_digest` | 64 lowercase hexadecimal characters (research.md R12) |

### Extended error object

When no plan can be built: the baseline `{"error": MESSAGE}` extended with
`code`, then `schema_version`, `observed_at`, `mode`, `repository` and
`merge_target` (each null unless established), `completeness:
"incomplete"`, `apply_allowed: false` and `refusals`. `error` keeps its
baseline messages where a test reads one (`Cannot determine the default
branch from the manifest, origin/HEAD, main, or master.`, `project:551`).

### Apply result record

`schema_version`, `observed_at` (when reconciliation finished),
`repository`, `merge_target`, `plan_digest`, `probes`, `operations`,
`targets`, `exit_code`, `completeness`. Each target: `path`,
`path_valid_utf8`, `branch`, `planned_sha`, `stage`, `reason`, `notes`,
`command`, `exit_status`, `probes_performed`, `reconciliation` (shapes and
values in data-model.md).

### Codes

| Refusal code | Phase | Raised when |
| --- | --- | --- |
| `invalid-arguments` | arguments | the argument checks above |
| `internal-error` | any, before the apply phase | an unexpected exception (research.md R6) |
| `git-unavailable` | resolve | `git` missing, failing, timing out or printing an unparseable version |
| `git-too-old` | resolve | Git older than 2.36 |
| `repository-not-found` | resolve | a bare name resolves to no project directory |
| `ambiguous-name` | resolve | a bare name matches more than one |
| `target-not-repository-root` | resolve | the resolution rules above |
| `unsupported-path-bytes` | resolve | `root` or `common_dir` not valid UTF-8 |
| `manifest-invalid` | resolve | unreadable, wrong kind, or over 1 MiB by `st_size` |
| `no-merge-target` | resolve | no candidate exists as a local branch |
| `inspection-incomplete` | plan | a repository-wide probe failed, a row is `inspection-error`, or a row was left unprobed |
| `inspect-cap` | plan | more rows than the mode's cap |
| `deadline-exceeded` | plan | the work deadline passed while planning |
| `worktree-not-found` | select | `--worktree` matches no registry entry |
| `target-excluded` | select | a gate excludes P; `reason` carries the gate |
| `plan-digest-mismatch` | confirm | the fresh digest differs from `--expect-plan` |
| `confirmation-required` | confirm | `--apply` on a standard input that is not a terminal, without `--yes` |
| `cancelled` | confirm | any answer other than `yes` |

`target-cap` is never raised by `project clean`. Row error codes:
`os-error`, `probe-failed`, `probe-timeout`, `deadline-exceeded`. Row note:
`partially-removed`. Target notes: `orphaned-directory`,
`partially-removed`. Stage and reason codes: data-model.md.

Push and delete-branch also refuse with `inspection-incomplete`,
`inspect-cap` or `deadline-exceeded` when their full inspection, before or
after confirmation, is incomplete, and push with the reason `remote-gone`
for a branch whose configured upstream's remote-tracking ref is gone,
whatever its class; each exits 2 and runs no delegate.

## Exit statuses

As tabled in data-model.md: with `--apply`, the first of 130, 143 or 129
(signal; 130 for end of input at the question), 1 (deadline after the apply
phase began, an `unknown` target, or `removal-ceiling`), Git's own status (a
`failed` target with `git-refused` or `git-failed`, passed through even when
it equals one of `project`'s own), 2 (any refusal, a `refused` target, a
branch-after-removal reason, `spawn-error`), 0. A preview or report: 2 for a
refusal before a plan is built, 1 incomplete, 0 otherwise, and the signal
exits. The baseline exited 0 for every printed report; it now exits 1 when
the report is incomplete (FR-005). Push and delete-branch exit 130, 143 or
129 when a signal was recorded, otherwise with the child's status, and 2
for a refusal.

## Git children

Every Git child but the push child is a D2 handle: its own session
(`start_new_session=True`), standard input from `/dev/null`, both outputs
read by the driver. Every Git child but the push child has these seventeen
names removed from its environment, unconditionally, from this fixed list
(FR-054); the push child has the first sixteen removed and keeps the
caller's `GIT_ALLOW_PROTOCOL` (lead ruling R-28):

```text
GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_CONFIG GIT_CONFIG_PARAMETERS
GIT_CONFIG_COUNT GIT_OBJECT_DIRECTORY GIT_DIR GIT_WORK_TREE
GIT_IMPLICIT_WORK_TREE GIT_GRAFT_FILE GIT_INDEX_FILE GIT_NO_REPLACE_OBJECTS
GIT_REPLACE_REF_BASE GIT_PREFIX GIT_SHALLOW_FILE GIT_COMMON_DIR
GIT_INTERNAL_SUPER_PREFIX GIT_ALLOW_PROTOCOL
```

`GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` stay. Read-only probes add
`GIT_OPTIONAL_LOCKS=0`; the removal and the delegates do not.

The protocol pins, on every Git child except the push child (the push-child
exception, LQ-3, awaiting Brett Heap's word on draft PR #19; research.md
R1):

```text
-c protocol.allow=never -c protocol.file.allow=never
-c protocol.ssh.allow=never -c protocol.git.allow=never
-c protocol.http.allow=never -c protocol.https.allow=never
-c protocol.ext.allow=never
```

The status pins, on every status probe, the hidden-state probe and the
removal: `-c core.untrackedCache=false -c core.fsmonitor=false`.

| Child | Argument vector after `git` and its pins | Directory |
| --- | --- | --- |
| row 1 | `--version` | the working directory |
| row 2 | `-C DIR rev-parse --show-toplevel` | the name lookup's directory (bare name only) |
| row 3 | `-C DIR rev-parse --path-format=absolute --show-toplevel --git-common-dir --show-superproject-working-tree` | where the argument resolves |
| row 4 | `-C DIR worktree list --porcelain -z` | there while the main worktree is unknown, else `root` |
| row 4b | `-C DIR config --get core.worktree` | only when the first record is `common_dir` |
| row 5 | row 3 again | `root`, only when row 3 ran elsewhere |
| row 6 | `-C ROOT for-each-ref --format=%(refname)%00%(objectname)%00%(symref)%00%(upstream)%00%(upstream:short)%00%(upstream:track,nobracket) refs/heads refs/remotes` | `root` |
| row 7 | `-C ROOT for-each-ref --merged=SHA --format=%(refname) refs/heads` | `root` |
| status | `-c core.untrackedCache=false -c core.fsmonitor=false -C WORKTREE status --porcelain=v1 -z --untracked-files=normal --ignored=matching` | the row's worktree |
| hidden state | `-c core.untrackedCache=false -c core.fsmonitor=false -C WORKTREE ls-files -v --stage -z` | the target's worktree |
| narrowed ref listing (revalidation) | row 6's format with patterns naming the merge target, the manifest's candidate, the branch `origin/HEAD` named, `main`, `master`, `refs/remotes/origin/HEAD`, and the selected branches and their upstreams | `root` |
| remote URL | `-C ROOT remote get-url origin` | `root` (push; `handoff()` in `status` and `doctor`) |
| removal | `-c status.showUntrackedFiles=normal -c core.untrackedCache=false -c core.fsmonitor=false` + protocol pins + `-C ROOT worktree remove PATH` | `root`; PATH the registry's raw bytes, one argument, never `--force` |
| branch deletion | protocol pins + `-C ROOT branch -d BRANCH` | `root`; a D2 handle run by the driver with no budget, its output relayed to `project`'s streams |
| push | `-C ROOT push REMOTE BRANCH:REMOTE_BRANCH`, or `push -u origin BRANCH`; no protocol pins | `root`; run by `execute()`, not the driver: `project`'s own streams, never read or capped; `project`'s process group, in the terminal's foreground when `project` is; never signalled, waited for, unbounded; yields no evidence |

Bounds: each probe child gets `min(5 s, work remaining)` under `clean`'s 60 s
deadline (50 s of work, a 10 s reserve, time at the question excluded), each
rescan child `min(5 s, reserve remaining)`; a child past its budget, at its
record bound or on a signal gets SIGTERM to its group, SIGKILL 2 s later, and
a reap wait of at most 2 s more, then is abandoned as `probe-timeout`. The
removal is spawned only while 5 s of the work deadline remains, is never
signalled before its 300 s ceiling, and is waited for. Push and branch
deletion stay unbounded: no budget and no deadline. A signal recorded while
the push or `git branch -d` child runs is not passed on: `project` never
signals either child, waits for it, and then exits by D19's first row
(data-model.md, "Exit statuses"). Probing is serial; termination never
blocks (data-model.md, "Child handle").
Revalidation spawns at most five Git children per target, the final rescan
at most three.

## `status`, `doctor` and `update` (FR-050 to FR-053, FR-059; D16)

| Aspect | Contract |
| --- | --- |
| Git check | `git --version` once per invocation, only when a repository is inspected; never a refusal |
| No `.git` | `present: false`, no Git child, as today |
| Uninspectable root, leg or worktree | `classification: "inspection-error"`, `errors`, unestablished values null; status exits 0 |
| Doctor's `git` row | `ok` with the version, or `error` naming `git-too-old` or `git-unavailable` |
| Doctor's error rows | one per null `present`, null `dirty` from a failed or timed-out probe, and `inspection-error` row; none for a null that means "none" |
| Human `status` and `doctor` | `Git: inspection-error (CODES)` in place of the branch line |
| Deleted upstream | `upstream` is the configured short name; `ahead`, `behind` null |
| Paths in JSON | `path_valid_utf8` beside every `path`, `root_valid_utf8` beside every `root`, `ignored_samples` entries as objects |
| Budgets | 15 s per Git child, no deadline, no row cap; non-Git children keep 15 s |
| `update --apply --component shape` or `bench` | refuses with exit 2, invoking no owner tool, unless the root's and every child's `dirty` are exactly false |
| `update --apply --component tools` or `workflow` | needs no Git; not refused for Git's version |
| Signals | SIGTERM and SIGHUP during inspection exit 143 and 129 after the probe groups are killed; at `Type yes` and during a delegate, as today |

The JSON of `status` and `doctor` stays unversioned; every change to it is
additive.
