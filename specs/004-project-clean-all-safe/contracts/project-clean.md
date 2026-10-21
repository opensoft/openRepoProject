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
call, and matched against every registry row: a row matches when its path
equals it, or else when its realpath, one bounded call each, does, and a
realpath that cannot be read counts as a match, failing closed (lead ruling
R-69). Exactly one decided match names P's row; no match is
`worktree-not-found`; more than one match, by raw bytes or by realpath, or
one not decided, selects nothing and leaves P's own evidence incomplete, so
the run refuses with `inspection-incomplete`, exit 2, before any
`target-excluded`, because P's own evidence is strict and an incomplete plan
is refused first (lead rulings R-57, R-62 and R-67 (b)). A path two entries
share is such a case, both entries also `registration-mismatch`,
`inspection-error` rows. So is a P whose own realpath cannot be read: every
entry the row cap takes counts as a match, none is exempt from the cap, so
the rows inspected are the main worktree and the 127 linked worktrees with
the smallest paths, as the delta's scenario "Row cap and planning failures"
takes them, and the run refuses with `inspection-incomplete`, exit 2 (lead
rulings R-73 (d) and R-74 (a)).

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
| bare name: a relative argument with no `/`, not `.` or `..`, research.md R13's reading of the `project-clean` delta's "one path component" (its `spec.md:459`), so that `..`, `./x` and `x/` are not bare names (lead ruling R-73 (e)) | `discover()`'s name lookup, its one Git child counted and bounded, then the directory it returns resolved as a worktree toplevel | `ambiguous-name`, `repository-not-found` |

Then, in this order (M6): a submodule checkout (row 3 prints a third line) is
refused; a first registry record that is `bare` is refused; a first record
equal to `common_dir` takes the realpath of `core.worktree` (row 4b; a relative
value resolves against the git directory) or else the candidate toplevel whose
`.git` file names `common_dir`, and is refused when neither names it; otherwise
the first record is the main worktree. Every refusal here is
`target-not-repository-root`, exit 2, before any plan. The family-holder and
manifest-ancestor redirections (`project:455-461`) never apply to a path
argument. The command directory is `root`: every repository-wide Git child
after resolution, every removal and the manifest read use it.

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
| push, delete-branch | `Cleanup action: ...`, the plan (`Working directory:` in the path-escaping printer's prose form, and every word of the command in its command form, below; lead ruling R-74 (c)(1)) and the delegate's own output, as today; `Type yes` only when standard output is not a terminal | `REFUSED: ...`, `Cancelled.`, `Type yes` at a terminal, since `input()` writes its prompt to standard error when standard input and output are both terminals, and the delegate's own |

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
| baseline header | `Cleanup plan for ROOT` and `Freshness:` as the baseline prints them, around `Merge target: NAME (SOURCE)`, which is new text: the baseline prints `Merge target: NAME` (`project:630`), though D18 names the line among the baseline's |
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
the gate order, classes in ladder order; the three reasons D18 gives no next
step take one each, in D18's form: `main-worktree` "never removed by project
clean", `unsupported-path-bytes` "rename the path to valid UTF-8" (P6-2), and
`not-requested` "name it with --worktree to plan its removal", so that
every group carries a next step, and so does every gate's `target-excluded`
message but the class gate's, which keeps its message with none (lead
rulings R-57, withdrawing R-45(3), R-59 D9 and R-62); a report prints the
baseline layout, each null as `unknown`, except a null `upstream`, which
means none configured (data-model.md, "Worktree row") and prints `none`, as
the baseline did, a branch named `HEAD` showing `inspection-error` by its
class (lead rulings R-69, reading 5, and R-72 (f)); an `--all-safe` plan,
and a single-mode `--action remove` plan, print "D18 preview layout", the
single-mode one with `Selected (1):` and the `not-requested` group among the
excluded ones, then "D18 residual-window line" only when something is
selected, since D7 prints the residual window at the confirmation and at the
result, and a plan that selects nothing has neither (lead ruling R-72 (e), a
fill); push and delete-branch print no plan layout, only their `Cleanup
action:` output as today (lead ruling R-56 Q-11); a row left unprobed
prints in the `reflog-unavailable` group, its reason, with that group's next
step, and no group of its own is added (lead ruling R-67 (a), withdrawing
R-56's); one progress line per target, printed at its final stage,
`  STAGE PATH` or `  STAGE PATH (REASON)`, `pending` never printed (R-56
Q-10); "D18 success line" followed by "D18 residual-window line", as the
stop block is (R-56 Q-9): a stopped run's human result is the stop block,
then `Branches kept:`, then "D18 residual-window line", D18's order
(`design.md:765-767`), the residual window being the result's too (the
`project-clean-review-safety` delta's `spec.md:208-209`), which is how the
`project-clean` delta's "SHALL end its human result with `Stopped at ...`"
(its `spec.md:962-964`) is read (lead ruling R-76 (d)); the retained-branch
line `Branches kept: B1, B2.`, naming every selected target's branch in
canonical order, except a branch whose last read shows it absent
(`branch_present` false, at any stage) or that a spawned target's rescan
did not read back (`branch_present` null on a `removed`, `failed` or
`unknown` target), the branches of `refused` and `not-attempted` targets
otherwise staying listed, since nothing was spawned for them; the left-out
names print on one new line after `Branches kept:` and before "D18
residual-window line", `Branches not confirmed: B2.`, a `TEXT` key the
text lane adds (T094, a lead-approved contracts edit), and the line reads
`Branches kept: none.` when every branch is left out, since D18 has
neither form (lead rulings R-76 (f) and R-79 P-10); a stop block with
no target `not-attempted`, as when the last selected target stops the run,
reads `Not attempted: none.`, a fill, since D18's stop block has no such
form (lead ruling R-68 (a)); the stop block's `Next: project clean ROOT
--all-safe` prints in single mode too, though that run named one worktree,
since D18 fixes the line as it is (lead ruling R-73 (f)); a plan-blocking
refusal prints the plan, then `REFUSED: MESSAGE`; each code with no baseline
message gets one here:

| Code | Message |
| --- | --- |
| `invalid-arguments` | `--all-safe cannot be combined with --action, --branch or --worktree.`; `--expect-plan requires --all-safe and --apply.`; `--expect-plan takes 64 lowercase hexadecimal characters.`; the baseline messages for the baseline cases |
| `internal-error` | `TYPE: TEXT`, the exception's class and text, so `REFUSED: RuntimeError: boom` (research.md R6) |
| `git-unavailable` | `Git is unavailable (DETAIL); clean needs Git 2.36 or later.`, DETAIL one of `not found`, `exit N`, `timed out`, `unparseable version`; clean's refusal only, a status or doctor row taking the command-neutral text in "Codes" (lead ruling R-48) |
| `git-too-old` | `Git VERSION is older than 2.36; clean needs Git 2.36 or later.`; clean's refusal only, as above (R-48) |
| `target-not-repository-root` | `Not the main worktree of a repository: PATH; pass the repository root.` |
| `unsupported-path-bytes` | `The repository path is not valid UTF-8: PATH` |
| `manifest-invalid` | `Manifest PATH is larger than 1 MiB.`; otherwise the baseline messages of `read_yaml()` and `manifest()`: `Cannot read PATH: ...` (an `OSError`, a read cut at its budget, or a parse error), `Expected a mapping in PATH`, `Unexpected kind in PATH; expected project-manifest` or `expected family-manifest`, and, where PyYAML is missing, `read_yaml()`'s own `YAML inspection needs PyYAML; use a workBench with python3-yaml installed.` (lead ruling R-73 (e)) |
| `inspection-incomplete`, `inspect-cap`, `deadline-exceeded` | `The plan is incomplete (CODE): REMEDY.`, REMEDY being "D18 remedies" |
| `plan-digest-mismatch` | `The fresh plan's digest DIGEST differs from --expect-plan EXPECTED; nothing was changed.` |
| `confirmation-required` | `Standard input is not a terminal; pass --yes to apply this plan.` (the removal question; `confirm()` keeps its own) |
| push, `remote-gone` | `Cannot push BRANCH; its upstream UPSTREAM was deleted (remote-gone); review it before it is republished.` |

`repository-not-found`, `ambiguous-name`, `no-merge-target`,
`worktree-not-found` and `cancelled` keep the baseline's messages, and
`target-excluded` is "D18 refusal messages". `remote-gone` is a reason, not
a nineteenth code, since the delta closes the eighteen: push, which prints
no JSON, refuses with no code and the reason `remote-gone`, printing
`REFUSED: ` and the message above (lead ruling R-45).

The delta's rule that every plan-blocking refusal names `git worktree
prune`, `git worktree repair` or removing the offending row by hand, "as the
cause fits", is read to let a cause that no repair fixes name its own remedy:
D18's `deadline-exceeded` remedy, "the run ran out of time; remove worktrees
explicitly or re-run", names none of the three and stands (lead ruling R-45;
LQ-5, listed for Brett Heap in the feature PR body).

All new text is ASCII. A path prints verbatim in prose and shell-quoted in
commands, unless it holds a code point of general category Cc, Cf, Zl or Zp
or an undecodable byte; then it prints as `$'...'` with `\xHH`, `\uXXXX` or
`\UXXXXXXXX` in lowercase hexadecimal, each backslash doubled and each single
quote as `\'` (FR-041). The baseline report keeps its other lines.

Two notes on that form, documentation only, since the delta fixes the
printed lines and `project` adds no text about them (lead rulings R-60 and
R-61). A command printed with `$'...'` needs a shell that implements it:
bash, zsh, ksh93 or a POSIX.1-2024 shell; dash, Ubuntu's `/bin/sh`, does not
yet. And a `\u` or `\U` escape needs a UTF-8 locale: under `LC_ALL=C`
bash and zsh drop such an escape, so `$'a\U000e0041b'` reads as `ab`, a
different valid name, and for some code points bash keeps the escape as
text and zsh refuses the line, so a command pasted in a C locale can name a
different path or branch. LQ-8 asks Brett Heap whether the command form
should write non-ASCII code points as their UTF-8 bytes, `\xHH`, which every
such shell reads alike in any locale (plan.md, "Open questions for Brett
Heap").

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
| `excluded` | array in canonical order: `path`, `path_valid_utf8`, `branch` (or null), `classification` (or null when never classified), `reason` (a string, the first failing gate, never null: a row left unprobed, its reflog read not finished within the filesystem budget, is `reflog-unavailable`, keeps its classification and makes the plan incomplete with `inspection-incomplete`; lead ruling R-67 (a), withdrawing R-56's null) |
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
| `manifest-invalid` | resolve | unreadable, not a mapping, wrong kind, over 1 MiB by `st_size`, or PyYAML missing |
| `no-merge-target` | resolve | no candidate exists as a local branch |
| `inspection-incomplete` | plan | a repository-wide probe failed, a row is `inspection-error`, a row was left unprobed, or, in single mode, P matches several entries or its match is undecided, its own realpath unread among them (lead rulings R-67 (b), R-73 (d) and R-75 (b)) |
| `inspect-cap` | plan | more rows than the mode's cap, which counts the registry entries that become rows, the main worktree and missing rows included; a bare repository's `bare` entry and a first record equal to `common_dir` with no main worktree are no rows (D8; lead ruling R-73 (d)) |
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

Each plan note and row error carries one fixed message (lead ruling R-45).
OPERATION names what was cut: `git SUBCOMMAND` for a Git child, or the
filesystem call (`lstat`, `realpath` or `read`). The lane that first prints
each adds its `TEXT` key as a lead-approved contracts edit, with its fixture
in `tests/clean_support.py`: the plan notes the plan lane (T049, T051), the
row errors lane G (T031, T032), and the two status and doctor texts the US9
lane (T117, T119). Those two are command-neutral: they never say "clean
needs", and clean's own refusals keep their messages above (lead ruling
R-48).

| Code | Kind | Message |
| --- | --- | --- |
| `merge-target-conflict` | plan note | `The manifest names NAME and origin/HEAD names OTHER; NAME is the merge target.` |
| `inspection-incomplete` | plan note, single mode | `K other rows are inspection-error or were left unprobed; they do not block PATH.` |
| `inspect-cap` | plan note, single mode | `K rows past the row cap of M were not inspected; they do not block PATH.` |
| `deadline-exceeded` | plan note, single mode | `K rows were stopped at the work deadline; they do not block PATH.` (lead ruling R-75 (g); T099) |
| `inspect-cap` | plan note, report above 128 rows, beside `rows` | `N rows exceed the --all-safe row cap of M; --all-safe would be incomplete (inspect-cap).` |
| `os-error` | row error | `OPERATION failed: STRERROR`, STRERROR the error number's text |
| `probe-failed` | row error | `OPERATION failed: DETAIL`, DETAIL one of `exit N`, `signal N`, `cannot spawn (STRERROR)`, `unparseable output` |
| `probe-timeout` | row error | `OPERATION timed out after S s`, S the budget in force |
| `deadline-exceeded` | row error | `OPERATION stopped at the work deadline` |
| `git-too-old` | status or doctor row error, and doctor's `git` row | `Git VERSION is older than 2.36; repository inspection needs Git 2.36 or later.` |
| `git-unavailable` | status or doctor row error, and doctor's `git` row | `Git is unavailable (DETAIL); repository inspection needs Git 2.36 or later.`, DETAIL as for clean's refusal |

The rows the work deadline stopped are `deadline-exceeded`'s, never
unprobed: each is `inspection-error` with a `deadline-exceeded` row error,
excluded with reason `inspection-error`, never a null reason and never
carrying the unprobed marker, which only T066's reflog read past its
filesystem budget sets (lead rulings R-67 (a), R-69 and R-75 (g)). T099
decides which single-mode note counts them, and brings the `deadline-exceeded`
note's `TEXT` key and its fixture to the message above.

A doctor row (`level`, `check`, `detail`) has no code field, so doctor's `git`
row writes its detail as `CODE: MESSAGE`, such as `git-too-old: Git 2.35.0 is
older than 2.36; repository inspection needs Git 2.36 or later.`; in the ok
case its detail is `PATH (git version X)`. A status `errors` entry keeps the
message alone, its `code` beside it (lead ruling R-57).

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
exits; a write that fails after its plan is built is `internal-error`, exit
2, by the delta's rule for an unexpected exception before the apply phase,
which conflicts with its preview rule there (research.md R4; lead rulings
R-55 and R-59; LQ-7, listed for Brett Heap in the feature PR body). The
baseline exited 0 for every printed report; it now exits 1 when the report
is incomplete (FR-005). Push and delete-branch exit 130, 143 or
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
`GIT_OPTIONAL_LOCKS=0`; the removal and the delegates add none, and a value
the caller set reaches them unchanged, as every child received it before this
change (`GIT_OPTIONAL_LOCKS` is not among the seventeen; D2 sets it for probes
only).

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

| Child | Argument vector after `git` and its pins (its status pins first, then the protocol pins; D9, D11) | Directory |
| --- | --- | --- |
| row 1 | `--version` | the working directory |
| row 2 | `-C DIR rev-parse --show-toplevel` | the name lookup's directory (bare name only) |
| row 3 | `-C DIR rev-parse --path-format=absolute --show-toplevel --git-common-dir --show-superproject-working-tree` | where the argument resolves |
| row 4 | `-C DIR worktree list --porcelain -z` | there while the main worktree is unknown, else `root` |
| row 4b | `-C DIR config --get core.worktree` | only when the first record is `common_dir` |
| row 5 | row 3 again | `root`, only when row 3 ran elsewhere |
| row 6 | `-C ROOT for-each-ref --format=%(refname)%00%(objectname)%00%(symref)%00%(upstream)%00%(upstream:short)%00%(upstream:track,nobracket) refs/heads refs/remotes` | `root` |
| row 7 | `-C ROOT for-each-ref --merged=SHA --format=%(refname) refs/heads` | `root` |
| status | `-c core.untrackedCache=false -c core.fsmonitor=false` + protocol pins + `-C WORKTREE status --porcelain=v1 -z --untracked-files=normal --ignored=matching` | the row's worktree |
| hidden state | `-c core.untrackedCache=false -c core.fsmonitor=false` + protocol pins + `-C WORKTREE ls-files -v --stage -z` | the target's worktree |
| narrowed ref listing (revalidation) | row 6's format with patterns naming the merge target, the manifest's candidate, the branch `origin/HEAD` named, `main`, `master`, `refs/remotes/origin/HEAD`, and the selected branches and their upstreams | `root` |
| remote URL | `-C ROOT remote get-url origin` | `root` (push; `handoff()` in `status` and `doctor`, for an inspected repository only, R-66 (c)) |
| removal | `-c status.showUntrackedFiles=normal -c core.untrackedCache=false -c core.fsmonitor=false` + protocol pins + `-C ROOT worktree remove PATH` | `root`; PATH the registry's raw bytes, one argument, never `--force` |
| branch deletion | protocol pins + `-C ROOT branch -d BRANCH` | `root`; a D2 handle run by the driver with no budget, its output relayed to `project`'s streams |
| push | `-C ROOT push REMOTE BRANCH:REMOTE_BRANCH`, or `push -u origin BRANCH`; no protocol pins | `root`; run by `execute()`, not the driver: `project`'s own streams, never read or capped; `project`'s process group, in the terminal's foreground when `project` is; never signalled, waited for, unbounded; yields no evidence |

Row 6 cannot establish the upstream of a branch named `HEAD`
(`refs/heads/HEAD`), because `git for-each-ref` reports the current branch's
upstream for it. Such a row has `upstream`, `remote_present`, `ahead` and
`behind` null and is `inspection-error`, its row error `probe-failed` with
`git for-each-ref failed: unparseable output`, filling the delta's rule that
evidence not established is `inspection-error` (lead rulings R-61 and R-64
(a); built by lane G's follow-up).

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
at most three, the identity probe counted once: a line feed in the root's
or the common directory's path repeats it, one child per option, so that
they run up to 8 and 6 (design D6, "the rare repeat"; data-model.md,
"Revalidation step and `probes_performed`"; lead ruling R-82 (c)).

## `status`, `doctor` and `update` (FR-050 to FR-053, FR-059; D16)

| Aspect | Contract |
| --- | --- |
| Git check | `git --version` once per invocation, memoized, when a repository is inspected; doctor's `git` row runs it itself when none was, and `status` never runs it for nothing (lead ruling R-56); never a refusal |
| `handoff()`'s remote read | `git remote get-url origin` only for a root whose repository was inspected, present and past the version check; otherwise the same no-identity state and no child (lead ruling R-66 (c)) |
| No `.git` | `present: false`, no Git child, as today |
| Uninspectable root, leg or worktree | `classification: "inspection-error"`, `errors`, unestablished values null, `worktrees` among them (R-56); status exits 0 |
| Doctor's `git` row | `ok` with the detail `PATH (git version X)`, or `error` with the detail `CODE: MESSAGE`, CODE `git-too-old` or `git-unavailable` and MESSAGE its command-neutral text ("Codes"; lead rulings R-48 and R-57) |
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
