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
thirty-one names below from every Git child's environment, never from its own,
except that the push child keeps `GIT_ALLOW_PROTOCOL` (R-28), and sets the
three trace2 targets to `0` in every Git child's (Brett Heap's ruling Q9 B).

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
equals it, or else when its realpath, one bounded call each, does. A
realpath that cannot be read, P's own or any entry's, a call cut at the work
deadline included, makes P's match undecided, failing closed (lead rulings
R-69 and R-78 (b)). Exactly one decided match names P's row; no match is
`worktree-not-found`; more than one match, by raw bytes or by realpath, or
one not decided, selects nothing and leaves P's own evidence incomplete, so
the run refuses with `inspection-incomplete`, exit 2, before any
`target-excluded`, because P's own evidence is strict and an incomplete plan
is refused first (lead rulings R-57, R-62 and R-67 (b)). A path two entries
share is such a case, both entries also `registration-mismatch`,
`inspection-error` rows. So is a P whose match is undecided, whichever entry's
realpath could not be read: every entry the row cap takes counts as a match,
none is exempt from the cap, a fill of FR-013 and of the delta's
`spec.md:262-263` ("P SHALL be probed first and SHALL be exempt from the row
cap"), which presumes a P that is a known entry, so the rows inspected are
the main worktree and the 127 linked worktrees with the smallest paths, as
the delta's scenario "Row cap and planning failures" takes them, never more
than the cap's 128, and the run refuses with `inspection-incomplete`, exit 2
(lead rulings R-73 (d), R-74 (a), R-78 (b) and R-91 LOW F).

## Order of a run

1. Argument checks.
2. The configuration-path test, before any Git child, then `git
   --version`, once (row 1): `relative-config-path`, then `git-unavailable`
   or `git-too-old`, exit 2, before any repository is probed. The test
   (design D11; Brett Heap's ruling LQ-15, draft PR #19 at `cc000ea` and
   `9fb22fa`; lead rulings R-102 (c) 3 and R-173): `HOME`,
   `XDG_CONFIG_HOME`, `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`, each read as
   its raw bytes, fail it when set to a value that is not empty and whose
   first byte is not `/`, so that ` /x`, `~/x`, `.` and a first byte that is
   not UTF-8 fail and `/` alone passes. Any failure refuses with
   `relative-config-path`, exit 2, in every mode, push and delete-branch
   included, so that no Git child starts. The test reads each value for itself
   alone, never in Git's order of precedence and whether or not Git would read
   a file through it; the values reach every child unchanged, and nothing
   prints them. The last two names are the lead's extension of the ruling,
   which Brett Heap may strike (`CONFIG_PATH_EXTENSION`; R-102 (c) 3).
3. Resolution (below), then `unsupported-path-bytes` for a `root` or
   `common_dir` that is not valid UTF-8.
4. The manifest read at `root`, row 6, and the merge target over row 6's
   listing: `manifest-invalid`, `no-merge-target`.
5. Planning under the deadline (row 7, then each row in order; in
   single mode for `--action remove` P is matched first,
   `worktree-not-found` if absent, and its row is established first, its
   status probe then its gates (1 to 7, the deferral with P alone, then 9
   to 12), before any other row is inspected; then the other rows in order and
   their gates), then `plan_digest`.
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

Steps 3 and 4 give the order of the refusals, not of the reads. The
`project-clean` delta asks only that `unsupported-path-bytes` come "before
any plan or digest is built" (its `spec.md:1067-1069`) and fixes no order
between that check and the manifest read, so the contract's order, the
UTF-8 check before the manifest read, is a reading of the delta, and the
code's is another: `resolve_clean_target()` makes one `inspect_repository()`
call, which runs rows 4, 6 and 7 and reads the manifest at `root`, and only
then checks `root` and `common_dir` for UTF-8, before the merge target's
own refusals (`manifest-invalid`, `no-merge-target`) and before any plan or
digest, no row being probed (lead rulings R-80 P-13 and R-92 (d)).

In single mode, step 5's order is design D13's, "inspects P's row first:
identity, status probe, gates" (`design.md:594-599`), which the delta's "P
SHALL be probed first" (its `spec.md:262-263`) and FR-013's "probed first"
say in short: a fill, not a departure. `build_plan()` runs gates 1 to 7,
gate 8 (P alone) and gates 9 to 12 over P's row, gate 10's `ls-files`,
gate 11's listing and gate 12's `logs/HEAD` read and reachability probe
included, right after it builds that row and before `worktree_rows()` takes
any other row, and no gate reads another row to decide P. A work deadline
reached among the other rows then leaves P's row decided and the plan
complete beside the non-blocking note `deadline-exceeded`, and the apply
phase's removal floor gives P `not-attempted` with `deadline-exceeded`,
exit 1 (D19, row 2); a deadline that cuts P's own read leaves P's row
incomplete, and the run refuses it as a one-item batch's plan is refused: with
`deadline-exceeded`, the deadline's remedy and no repair remedy, where P's row
is one the deadline stopped, whichever of its reads it cut (gate 7's reflog
read, gate 11's listing, the status probe), and with `inspection-incomplete`
where P's match was left undecided, a realpath read cut among them, or P's row
is `inspection-error` or unprobed for another cause (lead rulings R-93 (d) and
R-283; T070's
`test_clean_single_target_a_deadline_among_other_rows_leaves_p_decided`, and
`test_clean_single_target_p_s_reflog_read_cut_by_the_deadline`,
`test_clean_single_target_p_s_admin_listing_cut_by_the_deadline` and
`test_clean_single_target_p_s_status_probe_cut_by_the_deadline`).

## Resolution (FR-016, FR-017; D8)

| Argument (after `expanduser`) | Resolves to | Refusal |
| --- | --- | --- |
| absolute path | itself, when its realpath equals the toplevel Git reports there and that toplevel is the main worktree | `target-not-repository-root` |
| relative path: any relative argument containing a `/` (`./x`, `x/`), `.`, `..`, or none | the repository Git finds at that directory joined to the working directory; `root` is its main worktree | `target-not-repository-root` where Git finds no worktree |
| bare name: a relative argument with no `/`, not `.` or `..`, research.md R13's reading of the `project-clean` delta's "one path component" (its `spec.md:459`), so that `..`, `./x` and `x/` are not bare names (lead ruling R-73 (e)) | `discover()`'s name lookup, its one Git child counted and bounded, then the directory it returns resolved as a worktree toplevel | `ambiguous-name`, `repository-not-found` |

Then, in this order (M6): a submodule checkout (row 3 prints a third line) is
refused; a first registry record that is `bare` is refused; a first record
equal to `common_dir` takes the realpath of `core.worktree` (row 4b; a
relative value resolves against the git directory) or else the candidate
toplevel whose `.git` file names `common_dir`, and is refused when neither
names it, row 4b's exit 1 with nothing printed being the key unset and any
other failure of that read, an exit 1 that printed anything included, making
the main worktree `unreadable` and so refusing too (R-336); otherwise the
first record is the main worktree. Every refusal here is
`target-not-repository-root`, exit 2, before any plan. The family-holder and
manifest-ancestor redirections (`project:455-461`) never apply to a path
argument. The command directory is `root`: every repository-wide Git child
after resolution, every removal and the manifest read use it.

The refusal takes a variant message, `Not the main worktree of a repository:
PATH; core.worktree or core.bare redirects the main worktree; unset both in the
repository's config, or in the main worktree's config.worktree, then run
again.` (`target_not_repository_root_redirect`), only where a `core.worktree` or
`core.bare` of the repository's own explains it: #19's round (i) at `1a4785e`
(design D6 and D18; lead ruling R-271; writer G's `2707ff2`, merged as
`60631eb`). That is so only where the directory examined, the one that PATH
names, holds its own `.git`, a directory, a link to one or a gitfile that names
a git directory, whose realpath is the repository's common directory, so that
the directory is where the main worktree would be, and Git run there uses
another work tree or none. Where row 3 succeeded and printed no third line,
that is a toplevel that is not the directory's own realpath, which only a
`core.worktree` in the repository's `config` or in the main worktree's
`config.worktree` gives, and no Git child runs, only filesystem reads. Where
row 3 failed, as it does under `core.bare=true`, row 3b runs: one `probe` child
in the directory, `rev-parse --path-format=absolute --git-dir --git-common-dir
--is-bare-repository`, which needs no work tree, counted and bounded as row 3
is; it prints the git directory, the common directory, both that `.git`, and
`true`, which only a `core.bare` of true in one of those files gives. Row 3b
runs once, only on this refusal and only where the directory holds a `.git`,
and never in a run that resolves. Every other refusal keeps the plain message:
a directory outside any repository, a repository made by `git init --bare` and
passed by its own directory, which an unset `core.bare` would not make a work
tree, a subdirectory, a linked worktree, a linked worktree that its own
`config.worktree` redirects, a submodule checkout with its normal
configuration, and a working directory that is gone; so does a read that fails
or is cut, and a row 3b that fails, is cut or prints anything else. Two limits
of the variant are declared in #19's round (k) (lane 3's W81, M-1 and L-1):
a relative `core.worktree` that names a missing directory gets the plain
message, because Git itself fails in rows 3 and 3b (`fatal: cannot chdir to
...`, exit 128), a missing directory named absolutely taking the variant; and
a submodule whose own configuration redirects, by `core.bare` or by a
`core.worktree` that names another directory, takes the variant, after which,
the redirect gone, the plain refusal prints, and passing the superproject
root resolves it. A repository made by `git init --bare X/.git` and passed as
X has the configuration of a checkout at X whose `core.bare` is true, which
nothing Git reads tells apart, so it takes the variant, and the variant fits
it: with `core.bare` unset, X resolves.

A name the lookup cannot examine, `~user` for no such user, a name too long
for a path component (256 bytes or more), or one looked up from a working
directory that is gone, is `repository-not-found` with `discover()`'s message
`Directory does not exist: PATH`; a relative path, or none, from a working
directory that is gone is `target-not-repository-root`, naming the argument
as given, or `.`; and a relative path's refusal names the directory Git
examined, its realpath, not its lexical form (the plan review's F4; lane 3's
US7/US9 L-1 to L-3; lead ruling R-101 (c); lane E's `085a43b`).

## The removal question (FR-026; research.md R3)

| Aspect | Contract |
| --- | --- |
| Asked | `--all-safe --apply` or `--action remove`, without `--yes`, standard input a terminal, after the plan is printed |
| Text | "D18 question", the singular for one; written by `project` to the human stream (below), never by `input()` |
| Accepts | `yes`, surrounding whitespace ignored |
| Any other answer (`y`, empty, `no`, ...), or one standard input cannot decode, such as the byte 0xE9 under a strict UTF-8 decoder | refusal `cancelled`, exit 2, nothing removed; `ask_removal()` returns an undecodable answer as `""` (lead ruling R-101 (c); plan review F1) |
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
question. A run whose standard error fails before the apply phase still
prints one: the plan envelope is written only while no write has failed, so
the run ends as `internal-error`, exit 2, and its object is the one document
(`print_plan()`; lead ruling R-101 (b), the runner review's F1). A standard
output that is closed when `project` starts counts as a failed write too, so
`clean --json` refuses with `internal-error`, exit 2, with no traceback, R-55
extended (R-101 (b), F3), and so does an `--apply --json` run, `--all-safe` or
single, before any removal: it writes nothing to standard output before the
apply phase, so `check_writes()` records the closed stream as the failed write
`write_document()` records for it, EBADF, where `sys.stdout` is None under
`--json` (R-322 (Codex's P2 on PR #33); the result record, written after the removals, was
the first write to fail); a reader that disconnects once the apply phase has
begun stays best-effort, the removals continuing and the failed write recorded;
a closed human stream does not refuse, which lane 3 records as open (its F4 L-2).

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
| "D18 preview layout" | `Selected (N):` with one `  remove PATH [BRANCH]` per row; `Excluded (M):` with one `  REASON (K): NEXT STEP` group per reason and `    PATH [BRANCH]` rows; an `ignored-local-files` row adds its count and first sample; an `inspection-error` row whose path could not be read (`present` null) is a group of its own, first under that reason, with `next_step_unread_row`, and where any row of the plan is unread the other `inspection-error` rows and the `registration-mismatch` rows take `next_step_inspection_error_unread` and `next_step_registration_mismatch_unread`, and the `stale-worktree` rows `recommendation_stale_worktree_unread` (`excluded_groups()`; "The unread forms" below) |
| "D18 deferral line", "D18 non-drain line" | the `deferred-target-cap` group; under it, when a gate after the cap excludes all 16 rows the cap took, `  these deferred rows will not drain while the 16 rows ahead of them are REASONS; follow each group's next step for those worktrees`, REASONS their reasons, each once, in gate order, joined by `, ` (`AFTER_CAP_REASONS`; D18 at draft PR #19 `2e819ad`; lead ruling R-146, lane 3's W21 L-f; writer G's `310f97d`); its closing clause was `review those worktrees, then remove them yourself (--force for any that holds a submodule)` (lane 3's W59 G-4, #19's round (g3) at `6bf9f77`, lead ruling R-259, writer E's `02aa71d`), which sent the person past the next steps of the groups that those 16 rows are in, `worktree-only-commits`'s "keep it on a branch or tag" and `operation-in-progress`'s "finish or abort it" among them, so that Brett Heap's Q5 (ruled on 2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; lane 2's wave 22 triage T5, sr-removal F6; writer's `c28c9ea`) defers to those steps, which the preview prints above the line |
| "D18 next steps" | the next step for each reason |
| "D18 residual-window line" | the confirmation and the result |
| "D18 empty line" | `No eligible worktrees` |
| "D18 question", "D18 wait line" | above; the wait line once, at the first signal or deadline during a removal (D9) |
| "D18 success line", "D18 stop block" | the result; the stop block names the retained branches and the residual window |
| "D18 partial-removal note" | in three places (lead ruling R-79 P-11): in the report, on the line right after the row's recommendation line, two spaces in; in the preview, right after the row of the `dirty` group, six spaces in; in the result, first, before the stop block, one line per `partially-removed` target in canonical order, its path in the command form, whose text follows the rescan: D18's `Probable partial removal: inspect, then git worktree remove --force PATH by hand.` (`partial_removal_note_ceiling`, with no check first, since the target was clean at its revalidation: Brett Heap's Q4, ruled on 2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; writer's `c6daebc`) only where the rescan shows the target's registry entry and its `.git` file both present, `Probable partial removal: inspect PATH by hand; its .git could not be read, so do not run git worktree prune, git worktree remove or git gc until it can.` (`partial_removal_note_unread`) wherever the rescan made its `.git` lstat and it gave no value, since it failed for a reason other than the file's absence, as `EACCES` does for a worktree directory the process may not search, or was cut at its budget or abandoned by a second SIGINT, or wherever the rescan's lstat of the target's own path failed other than for absence (`path_present` null in the record, as where a directory above the target denies search), so that no `.git` read was made, whatever else the record shows, because `git worktree prune` deletes the admin directory of a live worktree whose `.git` Git cannot stat (#19's round (i) at `1a4785e`; lane 3's W73 M-1; lead ruling R-284, which Brett Heap ruled "R-284: yes", R-290; writer G's `6a32d10`, merged as `3bc1d68`; and, for the null path, lane 3's W90 M-1, lead ruling R-329, which applies Brett Heap's R-284 as ruled, with #19's ceiling scenario, "as when a directory above it denies search"; writer's `b96b335`, merged as `7149e08`; its warning also names `git worktree remove` and `git gc`, R-324, ruled by Brett Heap, "R-324: yes", lead R-343; #19's round (n) at `2250830`; writer's `e8dda2a`), and otherwise `Probable partial removal: inspect, then delete PATH and its administrative directory ADMIN by hand.` (`partial_removal_note_prune`; ADMIN is the target's own administrative directory, `<common_dir>/worktrees/<admin_id>`, in the command form, taken from the plan's repository identity and the target's row, both verified again at its revalidation, and `unknown` for a plain dict, which carries neither: `partial_removal_admin()`), the `.git` shown absent, or the entry gone or not established, since Git refuses `git worktree remove --force` once the `.git` file ("validation failed") or the registry entry ("is not a working tree") is gone; the note no longer names `git worktree prune`, which acts on the whole repository with an expiry of now and deletes the administrative directory, and with it the HEAD reflog, of every unlocked entry whose path is missing, a worktree moved or on a drive not mounted among them, so it names the target's own directory alone, and it is the same in every mode and beside any row of the plan, `partial_removal_text(target)` taking the target and no plan (Brett Heap's Q3 (a), ruled on 2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; lane 2's wave 22 triage T3, sr-removal F2; writer's `da5502d`, on `impl/004-q-build`). That supersedes R-365's form of the note beside a row whose path could not be read at planning (`unread_paths(plan)` not empty: `present` null, a row the work deadline stopped included), `Probable partial removal: inspect, then delete PATH by hand; a row's path could not be read, so do not run git worktree prune, git worktree remove or git gc until it can.` (`partial_removal_note_prune_unread`; lane 3's W52 F-1 (b) beside an unread row; lead ruling R-365, ruled by Brett Heap on 2026-10-23, "Yes, warn (Recommended)"; writer's `7a20789`, merged as `d8724e2`), which `print_result()` chose by passing `bool(unread_paths(plan))` to `partial_removal_text(target, plan_unread)`: that key and its selection are gone from `project`, and R-365's record stands as superseded. `partial_removal_note_ceiling`, which has the text that `partial_removal_note` had, and `partial_removal_note_unread` never changed, since `git worktree remove --force PATH` acts on PATH alone and the second already advises no prune; the rescan reads the `.git` by one `lstat`, no Git child, only where it shows the entry and the path both present (a path it could not look at leaves the `.git` unread), and keeps the read, and whether it was made (`git_file_read`), on the target and in no record, so that the JSON result is unchanged, and a report's or a preview's note is `partial_removal_note`, which names its check first (the end of this row), since its `.git` file and entry are present (lane 3's W52 F-1; Brett Heap's ruling "F-1: prune-then-delete" of 2026-10-22, lead ruling R-263, which amends ratified text, the `project-clean` delta's `spec.md:253-256` and `:922-926` at `0050f3e`; #19 at `b3228bb`; writer G's `3eb2e9c`, merged as `7164d7f`); a locked row's note, in the report and the preview, is `Probable partial removal: check that git -C PATH status --short --ignored lists only deleted files, unlock it, then git worktree remove --force PATH by hand.` (`partial_removal_note_locked`; it was `Probable partial removal: inspect, unlock it, then git worktree remove --force PATH by hand.` until Q4), since `git worktree remove --force` refuses a locked worktree, and the result never takes it, since a locked row is excluded at gate 4 and is never a target (lane 3's W52 F-2; #19 at `4f1c0e0`; lead ruling R-248); it replaces ratified text (`spec.md:135-138` at `0050f3e`), and Brett Heap ruled it on 2026-10-22, "F-2: yes" (lead ruling R-263), in its own commit, `64ad453`, which stays (lead ruling R-259); Brett Heap's Q4 (a) and (b) (ruled on 2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; lane 2's wave 22 triage T4, sr-removal F3 and F4; writer's `c6daebc`) name the check in the note of a report or preview row, which D4 judges on the status records read: `Probable partial removal: check that git -C PATH status --short --ignored lists only deleted files, then git worktree remove --force PATH by hand.` (`partial_removal_note`, PATH twice, each in the command form), so that a stream stopped at its record bound, past which an untracked or modified file can lie, and an ignored record, which leaves the flag alone, are shown to the person before `--force` could delete them; every detection rule stands, which keeps the scenario "project killed during a deletion" of a large target, and the result's own note, `partial_removal_note_ceiling`, keeps its text |
| "D18 refusal messages", "D18 remedies" | `target-excluded` (the current-worktree and class messages kept), gates, and the plan-blocking remedies |

Lines D18 leaves open are fixed here before tasks: the `Report:` and
`--all-safe would ...` lines follow `Freshness:`; `Excluded` groups follow
the gate order, classes in ladder order; the three reasons D18 gives no next
step take one each, in D18's form: `main-worktree` "never removed by project
clean", `unsupported-path-bytes` "move it to a valid UTF-8 path with git
worktree move, or mv it and then git worktree repair NEWPATH" (P6-2; since lane
3's W120 L-1, N10, and lane 2's wave 22 triage T14, lead R-373 and R-385,
writer's `e702a65`: a plain `mv` leaves the registry entry stale, and `git
worktree move` refuses a worktree that holds a submodule, so the step names the
two moves that mend it), and `not-requested` "name it with --worktree to plan
its removal", so that every group carries a next step, and so does every gate's
`target-excluded` message but the class gate's, which keeps its message with
none (lead rulings R-57, withdrawing R-45(3), R-59 D9 and R-62); a report
prints the baseline layout, each null as `unknown`, except a null `upstream`,
which means none configured (data-model.md, "Worktree row") and prints `none`,
as the baseline did, a branch named `HEAD` showing `inspection-error` by its
class (lead rulings R-69, reading 5, and R-72 (f)); an `--all-safe` plan,
and a single-mode `--action remove` plan, print "D18 preview layout", the
single-mode one with `Selected (1):` and the `not-requested` group among the
excluded ones, then "D18 residual-window line" only when something is
selected, since D7 prints the residual window at the confirmation and at the
result, and a plan that selects nothing has neither (lead ruling R-72 (e), a
fill); push and delete-branch print no plan layout, only their `Cleanup
action:` output as today (lead ruling R-56 Q-11); a row left unprobed
prints in the `reflog-unavailable` group, its reason, with that group's next
step, and no group of its own is added, whether the filesystem budget or the
work deadline cut its read (lead rulings R-67 (a), withdrawing R-56's, and
R-278); one progress line per target, printed at its final stage,
`  STAGE PATH` or `  STAGE PATH (REASON)`, `pending` never printed (R-56
Q-10); "D18 success line" followed by "D18 residual-window line", as the
stop block is (R-56 Q-9): a stopped run's human result is the stop block,
then `Branches kept:`, then "D18 residual-window line", D18's order
(`design.md:765-767`), the partial-removal notes printing before the stop
block (R-79 P-11, above), the residual window being the result's too (the
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
residual-window line", `Branches not confirmed: B2.`, a `TEXT` key,
`branches_not_confirmed`, the text lane adds (T094, a lead-approved
contracts edit), and the line reads
`Branches kept: none.` when every branch is left out; D18 has neither form,
its stop and its success lines (`design.md:765-768`) naming no branch the
run could not confirm, so both are a fill (lead rulings R-76 (f), R-79 P-10
and R-86 (d)); a stop block with no target `not-attempted`, as when the last
selected target stops the run, reads `Not attempted: none.`, a fill, since
D18's stop block has no such form (lead ruling R-68 (a)); the stop block's
`Next: project clean ROOT --all-safe` prints in single mode too, though that
run named one worktree, since D18 fixes the line as it is (lead ruling R-73
(f)); a plan-blocking refusal prints the plan, then `REFUSED: MESSAGE`; each
code with no baseline message gets one here:

| Code | Message |
| --- | --- |
| `invalid-arguments` | `--all-safe cannot be combined with --action, --branch or --worktree.`; `--expect-plan requires --all-safe and --apply.`; `--expect-plan takes 64 lowercase hexadecimal characters.`; the baseline messages for the baseline cases |
| `internal-error` | before the apply phase, `TYPE: TEXT`, the exception's class and text, so `REFUSED: RuntimeError: boom` (research.md R6); after it, no text (below) |
| `git-unavailable` | `Git is unavailable (DETAIL); clean needs Git 2.36 or later.`, DETAIL one of `not found`, `exit N`, `timed out`, `unparseable version`; clean's refusal only, a status or doctor row taking the command-neutral text in "Codes" (lead ruling R-48) |
| `git-too-old` | `Git VERSION is older than 2.36; clean needs Git 2.36 or later.`; clean's refusal only, as above (R-48) |
| `relative-config-path` | D18's line, `NAME is set to a path that does not begin with /; make it absolute or unset it.`, one line per variable that fails the configuration-path test, in the order `HOME`, `XDG_CONFIG_HOME`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`, never its value; a human refusal prints `REFUSED: ` before the first line only; status's `errors` entry and doctor's rows carry the same lines (LQ-15; R-102, R-131 (b)) |
| `target-not-repository-root` | `Not the main worktree of a repository: PATH; pass the repository root.`, or, where a `core.worktree` or `core.bare` of the repository's own redirects the main worktree away from the directory examined (see "Resolution"), `Not the main worktree of a repository: PATH; core.worktree or core.bare redirects the main worktree; unset both in the repository's config, or in the main worktree's config.worktree, then run again.` (`target_not_repository_root_redirect`) |
| `unsupported-path-bytes` | `The repository path is not valid UTF-8: PATH` |
| `manifest-invalid` | `Manifest PATH is larger than 1 MiB.`; otherwise the baseline messages of `read_yaml()` and `manifest()`: `Cannot read PATH: ...` (an `OSError`, a read cut at its budget, or a parse error), `Expected a mapping in PATH`, `Unexpected kind in PATH; expected project-manifest` or `expected family-manifest`, and, where PyYAML is missing, `read_yaml()`'s own `YAML inspection needs PyYAML; use a workBench with python3-yaml installed.` (lead ruling R-73 (e)) |
| `inspection-incomplete`, `inspect-cap`, `deadline-exceeded` | `The plan is incomplete (CODE): REMEDY.`, REMEDY being "D18 remedies": for `inspection-incomplete`, `repair or remove the inspection-error rows first: git worktree repair, git worktree prune, or remove the row by hand after review; git worktree prune also deletes the entry, and so the HEAD reflog, of every other worktree whose path is missing, one moved or on an unmounted drive included, so run git worktree prune --dry-run first and remount or repair any it lists that still exists` (`remedy_inspection_incomplete`) and, where any row the refusal counts is excluded as `registration-mismatch`, `repair or remove the inspection-error rows first: git worktree repair, git worktree prune, unset core.worktree and core.bare in the repository's config or in a worktree's config.worktree, or remove the row by hand after review; git worktree prune also deletes the entry, and so the HEAD reflog, of every other worktree whose path is missing, one moved or on an unmounted drive included, so run git worktree prune --dry-run first and remount or repair any it lists that still exists` (`remedy_inspection_incomplete_redirect`, below), each in its unread form where any row of the plan has a path that could not be read (`remedy_inspection_incomplete_unread` and `remedy_inspection_incomplete_redirect_unread`, "The unread forms" below); for `inspect-cap`, `N rows exceed the row cap of M; remove worktrees explicitly, or prune stale entries by hand; if a worktree's path cannot be read, do not run git worktree prune, git worktree remove or git gc until it can; git worktree prune also deletes the entry, and so the HEAD reflog, of every other worktree whose path is missing, one moved or on an unmounted drive included, so run git worktree prune --dry-run first and remount or repair any it lists that still exists` (`remedy_inspect_cap`, always, "The unread forms" below); for `deadline-exceeded`, `the run ran out of time; remove worktrees explicitly or re-run` |
| `plan-digest-mismatch` | `The fresh plan's digest DIGEST differs from --expect-plan EXPECTED; nothing was changed.` |
| `confirmation-required` | `Standard input is not a terminal; pass --yes to apply this plan.` (the removal question; `confirm()` keeps its own) |
| push, `remote-gone` | `Cannot push BRANCH; its upstream UPSTREAM was deleted (remote-gone); review it before it is republished.` |
| delete-branch, a branch the main worktree holds | `Branch BRANCH is checked out in the main worktree; detach HEAD there, or check out NAME there, then retry.`, NAME the merge target; a branch that a linked worktree holds keeps the baseline's `Remove the linked worktree first; branch deletion is a separate action.`; the message for the main worktree is a departure from BA:424-425, as #19 declares it (`proposal.md:1136-1150` at `b3228bb`), and from the baseline's one message for any present holder (`branch_held_by_main_worktree`; lane 3's W52 F-5, lane 5's RI-4; #19 at `4f1c0e0`; lead ruling R-248) |

The redirect variant of the `inspection-incomplete` remedy
(`remedy_inspection_incomplete_redirect`) is #19's round (h) at `b3228bb`,
design D18 (lead ruling R-258; writer G's `63e4573`, merged as `7164d7f`). It
prints wherever any row that the refusal counts is excluded as
`registration-mismatch`, whatever caused the mismatch, since the refusal reads
the exclusion reason and nothing else: a linked worktree that `core.worktree`
or `core.bare` redirects, which is `inspection-error`, but also a broken admin
registration or a path that two registry entries share, which no redirect
causes, as #19's wording requires, or, since Q2 (1) and Q9 (b) (R-380), a
linked worktree whose path is, or holds, the common directory, the main
worktree or another row's path, or whose registered path is a symbolic link.
The rows the refusal counts are those that make the plan
`inspection-incomplete`, an `inspection-error` or unprobed row
that the work deadline did not stop (`deadline_stopped()`; such a row is
`deadline-exceeded`'s and is never counted for the variant), in every mode that
counts every row (the report, the `--all-safe` preview and apply, push and
delete-branch), and, in single mode for `--action remove`, P's own rows, counted
the same way, where P's own incompleteness refuses: where P matches several
entries, or where P's row is `inspection-error` or unprobed and the work
deadline did not stop it. A refusal of that mode that comes earlier, for a
repository-wide read, counts none of P's rows and keeps the base remedy (lead
ruling R-287 (a); lane 3's W73 L-2; writer G's `ded85bb`, merged as
`3bc1d68`). A plain `inspection-error` row, as a reflog read that fails with
`EISDIR` makes, keeps the base remedy unless a counted row beside it is a
registration mismatch; `inspect-cap` and `deadline-exceeded` keep their
remedies.

The unread forms are #19's round (l) at `ccc52b9`, design D18 (lane 3's W87
M-1; the lead's R-307 and R-310, confirmed by Brett Heap (R-319); writer's
`e569564`, merged as `1edf64e`). A row is unread where its path could not be
read at planning: its `lstat` failed for a reason other than the path's
absence, or was cut at its budget or at the work deadline, so that `present`
is null and the row is `inspection-error` (`path_unread()`;
`unread_paths(plan)` collects the raw paths of such rows of `plan.rows`, from
what planning recorded, nothing read again). `git worktree prune` deletes the
admin directory of a live worktree whose path Git cannot stat (`EACCES`, for a
directory the process may not search), and acts on the whole repository, so
wherever any row of the plan is unread, a deadline-stopped row and a row the
refusal does not count included, the plan prints no prune advice, and every
warning also names `git worktree remove` and `git gc` (R-324, ruled by Brett
Heap, "R-324: yes", lead R-343; #19's round (n) at `2250830`; writer's
`e8dda2a`). The `inspection-incomplete` remedy is
`remedy_inspection_incomplete_unread`, `repair or remove the inspection-error
rows first: git worktree repair, or remove the row by hand after review; a
row's path could not be read, so do not run git worktree prune, git worktree
remove or git gc until it can`, and, where the redirect variant would print,
`remedy_inspection_incomplete_redirect_unread`, `repair or remove the
inspection-error rows first: git worktree repair, unset core.worktree and
core.bare in the repository's config or in a worktree's config.worktree, or
remove the row by hand after review; a row's path could not be read, so do not
run git worktree prune, git worktree remove or git gc until it can`; the
variant's counting is unchanged, a single removal that names the unread row
counts P's rows alone, none redirected, so it takes the first, and
`deadline-exceeded` keeps its remedy, and the `inspect-cap` remedy is
`remedy_inspect_cap`, `N rows exceed the row cap of M; remove worktrees
explicitly, or prune stale entries by hand; if a worktree's path cannot be
read, do not run git worktree prune, git worktree remove or git gc until it
can; git worktree prune also deletes the entry, and so the HEAD reflog, of
every other worktree whose path is missing, one moved or on an unmounted drive
included, so run git worktree prune --dry-run first and remount or repair any
it lists that still exists`, always, whether or not any row is unread, because
the rows past the cap are never read and no run can tell whether their paths
can be (R-320, ruled by Brett Heap ("R-320: yes", lead R-321); lane 3's W86
NM-1; writer's `dfc2baa`, merged as `12c1821`). In the preview the unread rows
form a group of their own under `inspection-error`, printed first, with
`next_step_unread_row`, `inspect the row by hand; its path could not be read,
so do not run git worktree prune, git worktree remove or git gc until it can`;
the other `inspection-error` rows take `next_step_inspection_error_unread`,
`review, then git worktree repair, or remove the row by hand; a row's path
could not be read, so do not run git worktree prune, git worktree remove or git
gc until it can`, and the `registration-mismatch` rows
`next_step_registration_mismatch_unread`, `review, then git worktree repair,
unset core.worktree and core.bare in the repository's config, or in that
worktree's config.worktree, or remove the row by hand; a row's path could not
be read, so do not run git worktree prune, git worktree remove or git gc until
it can`. Where any row of the plan is unread, `stale_recommendations()`, which
`build_plan()` calls once every row is gated, also gives each `stale-worktree`
row the recommendation `recommendation_stale_worktree_unread`, `Review and
prune stale worktree metadata manually; a row's path could not be read, so do
not run git worktree prune, git worktree remove or git gc until it can.`, or,
for a locked row, `recommendation_stale_locked_unread`, `Review, unlock it,
then prune stale worktree metadata manually; a row's path could not be read, so
do not run git worktree prune, git worktree remove or git gc until it can.`, in
the report, the plan envelope's `worktrees` and `plan.report`, and the
preview's `stale-worktree` group takes the first as its next step
(`UNREAD_NEXT_STEPS`; a locked stale row is excluded as `locked-worktree`, gate
4), from what planning recorded, the class unchanged (R-320, ruled by Brett
Heap ("R-320: yes", lead R-321)). Where no row is unread every text is its
plain form, which since Q3 (b) ends with the dry-run warning (the next
paragraph). `status`'s stale recommendation takes the no-prune warning beside
an unread row, as the paragraph under "`status`, `doctor` and `update`" gives
it (T9, R-365, ruled by Brett Heap on 2026-10-23, "Yes, add T9 (Recommended)").
R-365 gave the result's ceiling note a form beside an unread row too,
`partial_removal_note_prune_unread`; Q3 (a) superseded it ("D18 partial-removal
note" above).

The plain forms carry a warning of their own (Brett Heap's Q3 (b), ruled on
2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; lane 2's wave
22 triage T3, sr-removal F2, sr-evidence M-1; writer's `da5502d`). `git
worktree prune` has an expiry of now and acts on the whole repository, so it
also deletes the administrative directory, and with it the HEAD reflog and any
commit that only that reflog holds, of every other unlocked worktree whose path
is missing, one moved or on a drive that is not mounted. Such a row is
`stale-worktree`, its `lstat` having given `ENOENT`, and not an unread row, so
the unread forms do not cover it. Each plain text that names `git worktree
prune` therefore ends with `PRUNE_DRY_RUN`, `; git worktree prune also deletes
the entry, and so the HEAD reflog, of every other worktree whose path is
missing, one moved or on an unmounted drive included, so run git worktree prune
--dry-run first and remount or repair any it lists that still exists`, and the
two recommendations end in `.` after it, with no clause trailing:

- `remedy_inspection_incomplete`: `repair or remove the inspection-error rows
  first: git worktree repair, git worktree prune, or remove the row by hand
  after review; git worktree prune also deletes the entry, and so the HEAD
  reflog, of every other worktree whose path is missing, one moved or on an
  unmounted drive included, so run git worktree prune --dry-run first and
  remount or repair any it lists that still exists`
- `remedy_inspection_incomplete_redirect`: `repair or remove the
  inspection-error rows first: git worktree repair, git worktree prune, unset
  core.worktree and core.bare in the repository's config or in a worktree's
  config.worktree, or remove the row by hand after review; git worktree prune
  also deletes the entry, and so the HEAD reflog, of every other worktree whose
  path is missing, one moved or on an unmounted drive included, so run git
  worktree prune --dry-run first and remount or repair any it lists that still
  exists`
- `remedy_inspect_cap`: `N rows exceed the row cap of M; remove worktrees
  explicitly, or prune stale entries by hand; if a worktree's path cannot be
  read, do not run git worktree prune, git worktree remove or git gc until it
  can; git worktree prune also deletes the entry, and so the HEAD reflog, of
  every other worktree whose path is missing, one moved or on an unmounted
  drive included, so run git worktree prune --dry-run first and remount or
  repair any it lists that still exists`
- the `registration-mismatch` next step: `review, then git worktree repair or
  git worktree prune, unset core.worktree and core.bare in the repository's
  config, or in that worktree's config.worktree, or remove the row by hand; git
  worktree prune also deletes the entry, and so the HEAD reflog, of every other
  worktree whose path is missing, one moved or on an unmounted drive included,
  so run git worktree prune --dry-run first and remount or repair any it lists
  that still exists`
- the `inspection-error` next step: `review, then git worktree repair or git
  worktree prune, or remove the row by hand; git worktree prune also deletes
  the entry, and so the HEAD reflog, of every other worktree whose path is
  missing, one moved or on an unmounted drive included, so run git worktree
  prune --dry-run first and remount or repair any it lists that still exists`
- `recommendation_stale_worktree`: `Review and prune stale worktree metadata
  manually; git worktree prune also deletes the entry, and so the HEAD reflog,
  of every other worktree whose path is missing, one moved or on an unmounted
  drive included, so run git worktree prune --dry-run first and remount or
  repair any it lists that still exists.`
- `recommendation_stale_locked`: `Review, unlock it, then prune stale worktree
  metadata manually; git worktree prune also deletes the entry, and so the HEAD
  reflog, of every other worktree whose path is missing, one moved or on an
  unmounted drive included, so run git worktree prune --dry-run first and
  remount or repair any it lists that still exists.`

`recommendation_stale_worktree` is a new `TEXT` key: a `stale-worktree` row's
recommendation, in the report and in the `worktrees` rows of `--json`, is it,
or `recommendation_stale_locked` for a locked row, where no row of the plan is
unread (`row_evidence()` gives it after the ladder has run, and
`next_step("stale-worktree")` gives the preview's group the same text);
`RECOMMENDATIONS["stale-worktree"]`, which `classify()` returns, keeps the
baseline's `Review and prune stale worktree metadata manually.`, and `status`'s
own advice for a stale entry is not touched (below). Where any row is unread
the forms above, `recommendation_stale_worktree_unread` and
`recommendation_stale_locked_unread`, stay as they are, and so do the unread
remedies and next steps; the texts that name `git worktree prune` as the
person's own remedy stand (FR-027's list). Only these texts change: no field,
key, code, class or exit status does.

`repository-not-found`, `ambiguous-name`, `no-merge-target`,
`worktree-not-found` and `cancelled` keep the baseline's messages, and
`target-excluded` is "D18 refusal messages". `remote-gone` is a reason, not
a twentieth code, since the delta, with LQ-15's `relative-config-path`,
closes the nineteen: push, which prints
no JSON, refuses with no code and the reason `remote-gone`, printing
`REFUSED: ` and the message above (lead ruling R-45); delete-branch, which
prints no JSON either, refuses with no code, printing `REFUSED: ` and its
message, the one above for a branch the main worktree holds included.

Two of the baseline messages print the user's own argument raw in
`discover()`: `Directory does not exist: PATH` and `No project found at
PATH; supply a path or name.`, which reach clean as `repository-not-found`,
where the delta's human-output rule (`spec.md:1061-1066`) escapes a path
that holds a code point to escape. `resolve_clean_target()` prints the PATH
of both through `human_path()`, in the `$'...'` form for such a path,
taking it out of `discover()`'s message by the message's fixed head and
tail (`escaped_not_found()`, region `resolution`), for a refusal
`discover()` already codes and for one it leaves uncoded alike. The JSON
stays `{code, message}` with no `path`, since the contract lists none for
that code and `tests/test_clean_resolution.py` asserts the shape: `error`
and the refusal's `message` carry the escaped text the human line shows.
`discover()` itself is unchanged, since `status`, `doctor` and `update`
share it (lead rulings R-92 (c) and R-94 (a); T112's tests in
`tests/test_clean_paths.py`, one for an argument holding U+202E and, under
`linux_paths`, one for the byte 0xFF).

`internal-error` prints its exception's type and text only where it is a
refusal, before the apply phase. After the apply phase begins, an exception
while handling a target makes that target `unknown` with `internal-error`
and prints no exception type and no text, neither on a stream nor in the
result record, so the cause is lost, though the stage fails closed; and a
fault while rendering a progress line, the human result or the apply result
record is dropped silently by `best_effort()`, changing no stage, since a
proven removal stays proven, and no exit status, which D19 has decided
already. The `project-clean` delta's rule (`spec.md:938-941`) names the
stage and the reason and no text, so this is the contract's reading of it.
Whether to print the exception's type on standard error goes to Brett Heap
in LQ-7's group, since it touches the error streams (lead ruling R-87 (c);
LQ-7, listed for him in the feature PR body).

The delta's rule that every plan-blocking refusal names `git worktree
prune`, `git worktree repair` or removing the offending row by hand, "as the
cause fits", is read to let a cause that no repair fixes name its own remedy:
D18's `deadline-exceeded` remedy, "the run ran out of time; remove worktrees
explicitly or re-run", names none of the three and stands (lead ruling R-45;
LQ-5, listed for Brett Heap in the feature PR body). Since #19's round (h) at
`b3228bb` the rule also names a fourth remedy, unsetting `core.worktree` and
`core.bare` in the repository's `config` or in a worktree's `config.worktree`,
which the redirect variant above carries.

Brett Heap's ruling LQ-14 adds gate 11, `operation-in-progress`, after
`hidden-local-state` (design D22; draft PR #19 at `43f7107`, `2b86a5f` and
`1ebdd90`; lead rulings R-102, R-121, R-124, R-126 and R-180), and his
ruling LQ-13 gate 12, `worktree-only-commits`, after it, the last gate
(design D21; draft PR #19 at `93de4bb` and `2b86a5f`; lead rulings R-102,
R-124 and R-146; data-model.md, "Gate"), and with them three lines. Gate
11's group's next step is #19's as round (b) words it at `4485678`, with
the tail of round (g3) at `6bf9f77` and the by-hand clause of round (h) at
`b3228bb`, and `NEXT_STEPS` in `project` at `7164d7f` prints it: `a git am,
merge, notes merge, cherry-pick, revert, rebase or bisect is, or may be, in
progress there; finish or abort it (a squash merge that holds an autostash
ends with git commit, --allow-empty where nothing is staged, or with git
merge --quit, which keeps the edit in the stash list), or, where --abort
fails for a marker with nothing in progress, its --quit, or, where Git
leaves such a marker in place, delete it by hand from that worktree's git
directory, then run again`. Round (a)'s `... ends only with git commit` was
false, since `git merge --quit` and `git reset --hard` also end a held
autostash, saving the edit to the stash list (lane 3's W26 F-1 and W32 M1;
lead rulings R-171 and R-200; writer G's `c15ec02`, merged as `e2e423d`);
the tail from `or, where --abort fails` on, as far as `its --quit`, is lane
3's W52 F-9, worded as W59's G-5 has it (lead rulings R-248 and R-259;
writer E's `02aa71d`, merged as `d764c26`). The by-hand clause, `or, where
Git leaves such a marker in place, delete it by hand from that worktree's git
directory`, is #19's round (h) (writer E's table of markers that no Git
command clears, lead ruling R-259, re-run in #19 on both Git builds: an
empty `CHERRY_PICK_HEAD`, `REVERT_HEAD` or `MERGE_AUTOSTASH`, whose
`--abort` exits 128 and whose `--quit` exits 0 and leaves it, a lone
`BISECT_LOG`, an empty `MERGE_HEAD` directory, a notes-merge marker file, and
a `rebase-apply`, `rebase-merge` or `sequencer` that is an empty file;
writer G's `457a20f`, merged as `7164d7f`, tests the empty `sequencer` file,
which `git cherry-pick` and `git revert` refuse to clear with `--quit` and
`--abort`, on Git 2.43.0 and 2.36.6): with that marker deleted by hand from
the worktree's git directory, which `git rev-parse --git-dir` there prints,
the row passes gate 11 and, in the test's fixture, is selected. Gate 12's group's next step is D18's at
`2e819ad`: `a commit is, or may be, held only by this worktree's HEAD
reflog or refs/worktree; keep it on a branch or tag, or review, then git
worktree remove yourself`. The residual-window line gains LQ-14's third
item and LQ-13's fourth: `Not protected: ignored files created, index flags
set, operations started or worktree-only commits made after the last check,
and any change after Git's own check.` In the preview the
`operation-in-progress` and `worktree-only-commits` groups follow
`hidden-local-state`, in gate order (`EXCLUDED_GROUP_ORDER`).
`registration-mismatch`'s next step, as `NEXT_STEPS` in `project` at
`d764c26` prints it, names R-125's `config.worktree` remedy and, since lane
3's W52 F-3, the repository's config beside it, the two files from which
Git applies the redirect: `review, then git worktree repair or git worktree
prune, unset core.worktree and core.bare in the repository's config, or in that
worktree's config.worktree, or remove the row by hand; git worktree prune also
deletes the entry, and so the HEAD reflog, of every other worktree whose path
is missing, one moved or on an unmounted drive included, so run git worktree
prune --dry-run first and remount or repair any it lists that still exists`
(LQ-11; with Q3 (b)'s dry-run warning at its end, R-380; D18 at
draft PR #19 `2e819ad`, F-3's wording at `4f1c0e0`; lead rulings R-125 L6
and R-248; writer G's `f57ecf9`, merged as `e2e423d`; writer E's `02aa71d`,
merged as `d764c26`). Where any row of the plan has a path that could not be read, it
is `next_step_registration_mismatch_unread` instead, which names no `git worktree
prune` (#19's round (l); "The unread forms" above).

Note, 2026-10-22 (doc round 18; lead ruling R-259): writer E's `02aa71d`
and `64ad453`, merged into 004 as `d764c26`, bring `project` to lane 3's
W52 (F-2 to F-10) and W59 (G-4 and G-5), and their strings equal draft PR
#19's at `6bf9f77`, round (g3), for F-2, F-3, F-5, F-7, F-8, F-9 (G-5) and
G-4 (lead rulings R-248 and R-259). Beyond the texts quoted above,
`NEXT_STEPS` had, for gate 7's two reasons, a clause that Git needs where the
worktree holds a submodule (F-7): `unstarted-branch` was `no commit was made on
this branch here since it was created; review, then git worktree remove
yourself (--force if it holds a submodule)` and `reflog-unavailable` was `the
branch's reflog is missing, expired or undecidable; review, then git worktree
remove yourself (--force if it holds a submodule)`; and, for gate 9, which a
plain removal of a worktree that holds a submodule would fail,
`contains-submodule` was `review, then git worktree remove --force yourself`
(F-8). Brett Heap's Q4 (c) and Q5 (ruled on 2026-10-23T13:30:27Z, "yes,
recommended for Q1-Q9"; lead R-380; lane 2's wave 22 triage T4 and T5,
sr-removal F5, sr-classification M-2 and M-3; writers' `c6daebc` and `c28c9ea`)
change all three. A submodule initialized in a linked worktree keeps its
repository in `<admin>/modules/<name>`, which `--force` deletes with its
unpushed commits, so `contains-submodule` is `push or otherwise keep each
submodule's commits first, since --force deletes its repository with this
worktree's git directory, then git worktree remove --force yourself`, and gate
7's two parentheticals read `(--force if it holds a submodule, once its commits
are kept)`. Gate 7 also precedes gates 9 to 12, which therefore did not run for
a row it excludes, though a plain removal could delete a commit that only its
HEAD reflog holds or an assume-unchanged edit, so its two steps name the checks
those gates would have made: `unstarted-branch` is `no commit was made on this
branch here since it was created; its later gates did not run, so check git log
-g HEAD, git ls-files -v and git status there, then git worktree remove
yourself (--force if it holds a submodule, once its commits are kept)` and
`reflog-unavailable` is `the branch's reflog is missing, expired or
undecidable; its later gates did not run, so check git log -g HEAD, git
ls-files -v and git status there, then git worktree remove yourself (--force if
it holds a submodule, once its commits are kept)`. Two report recommendations
are 004's own texts, which #19 at `4f1c0e0` does not carry (F-6 and F-10): the
main worktree's row, where the ladder says `merged-removable` or
`merged-current`, reads `The main worktree is never removed by project
clean.` (`recommendation_main_worktree`), since no removal of it can
succeed, and a locked `stale-worktree` row reads `Review, unlock it, then prune
stale worktree metadata manually` and, since Q3 (b) (R-380), the dry-run
warning that the paragraph after "The unread forms" gives
(`recommendation_stale_locked`: `Review, unlock it, then prune stale worktree
metadata manually; git worktree prune also deletes the entry, and so the HEAD
reflog, of every other worktree whose path is missing, one moved or on an
unmounted drive included, so run git worktree prune --dry-run first and remount
or repair any it lists that still exists.`), since `git worktree prune` keeps a
locked entry; the class is unchanged in both, and every other row keeps its
class's baseline recommendation, but that each `stale-worktree` row takes
`recommendation_stale_worktree_unread` (locked,
`recommendation_stale_locked_unread`) where any row of the plan is unread ("The
unread forms" above; R-320). The partial-removal note for a locked row (F-2) is
in the "D18 partial-removal note" row above, and delete-branch's refusal (F-5)
and its `--` (F-4) are in the code table and the spawn table below. F-2
replaces ratified text; Brett Heap ruled it on 2026-10-22, "F-2: yes" (lead
ruling R-263), and it is in its own commit, `64ad453`, which stays.

Note, 2026-10-22 (doc round 19; lead rulings R-258, R-259, R-263, R-271,
R-274, R-278, R-283, R-284, R-287 and R-290): Brett Heap ruled at 15:24Z,
verbatim, "F-2: yes; F-1: prune-then-delete; O-1: deadline-exceeded" (R-263).
Each replaces a sentence that the merge of PR #11 ratified (`0050f3e`; the
`project-clean` delta's `spec.md:135-138` for F-2, `:253-256` and `:922-926`
for F-1, `:606-608` for O-1), as #19 records them at `b3228bb` under
"Amendments of ratified text". Writer G built F-1 (`3eb2e9c`), O-1 (`c33f761`,
then `99848dd` and, for a named removal, `a038961`) and the strings of #19's
round (h) (`457a20f`, `63e4573` and `c26e44b`), merged into 004 as `7164d7f`
(R-274) and `3bc1d68`, which also carry round (i)'s refusal (`2707ff2`), R-284's
note for a `.git` the rescan cannot read (`6a32d10`; Brett Heap, "R-284: yes",
R-290), the work-tree probe's output read as one path (`4dfd6f5`; R-287) and the
variant remedy's counting in single mode (`ded85bb`). Where each is
documented: the "D18 partial-removal note" row above and "Apply result record"
(F-1, R-284), gate 7's reflog read and the paragraph on the rows the work
deadline stopped (O-1), gate 11's paragraph (the by-hand clause of
`operation-in-progress`), the "Codes" table and its paragraphs (the redirect
variant of the `inspection-incomplete` remedy, and `target-not-repository-root`'s
variant under "Resolution"), the plan envelope's `probes` row and the "Git
children" bounds (the estimate's extra children for a line feed in the root's or
the common directory's path, lane 5's RI-3; row 3b, and the work-tree probe's
output).

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
| `probes`, `operations` | `{estimated, performed}` integers: `probes` counts every Git child other than a removal, `operations` the removals, each child once (lead ruling R-27); `estimated` is the upper bound for an `--apply` run of this plan in every mode, previews included: the planning children this invocation ran (F + W + E, with LQ-11's work-tree probes and gate 12's reachability probes among them) + RT + S, R being 6, or 7 where row 4c read `extensions.worktreeConfig` as true (`revalidation_children()`), S being 3 (`rescan_children()`), and R and S each 3 more where the path of the repository's root or of its common directory, as the plan read them, holds a line feed, so that the identity probe is read one option per child (lane 5's RI-3; #19's round (h) at `b3228bb`; "Git children" below), and T (research.md R8) |
| `selected` | array in canonical order, or null in a report above 128 rows; each entry: `path`, `path_valid_utf8`, `branch`, `head`, `upstream`, `upstream_oid`, `ahead`, `behind`, `dev`, `ino`, `admin_id`, `locked`, the baseline signature fields (`present`, `dirty`, `ignored_files`, `remote_present`, `merged_into_target`, `current`, `classification`), and `operation` (`{kind: "worktree-remove", argv}`, the exact argument vector) |
| `excluded` | array in canonical order: `path`, `path_valid_utf8`, `branch` (or null), `classification` (or null when never classified), `reason` (a string, the first failing gate, never null: a row left unprobed, its reflog read not finished, is `reflog-unavailable`, keeps its classification and makes the plan incomplete: with `inspection-incomplete` where the filesystem budget cut the read, its row error `probe-timeout`, and with `deadline-exceeded`, never `inspection-incomplete`, where the work deadline cut it, its row error `deadline-exceeded`; lead rulings R-67 (a), withdrawing R-56's null, and R-278) |
| `omitted` | `{count, exactness: "exact"}` |
| `notes` | `{code, message}` objects; `merge-target-conflict`; in single mode the non-blocking `inspection-incomplete`, `inspect-cap`, `deadline-exceeded`, none of them when P's match is undecided (below); in a report above 128 rows `inspect-cap` with `rows` |
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
values in data-model.md). The record carries nothing of the rescan's read of
the target's `.git`: that read picks the human text of the ceiling's
partial-removal note ("D18 partial-removal note", above), among its three
forms, together with the reconciliation's `path_present`, null where the lstat
of the target's own path failed (lane 3's W90 M-1; lead ruling R-329), and is
kept on the target, with whether it was made, so the JSON result is unchanged,
`notes` and `reconciliation` keeping their keys and values (lane 3's W52 F-1,
W73 M-1 and W90 M-1; lead rulings R-263, R-284 and R-329).

### Codes

| Refusal code | Phase | Raised when |
| --- | --- | --- |
| `invalid-arguments` | arguments | the argument checks above |
| `internal-error` | any, before the apply phase | an unexpected exception (research.md R6) |
| `git-unavailable` | resolve | `git` missing, failing, timing out or printing an unparseable version |
| `git-too-old` | resolve | Git older than 2.36 |
| `relative-config-path` | resolve | `HOME`, `XDG_CONFIG_HOME`, `GIT_CONFIG_GLOBAL` or `GIT_CONFIG_SYSTEM` set to a value that is not empty and does not begin with `/`, tested after the argument checks and before `git --version` ("Order of a run"; Brett Heap's ruling LQ-15, lead ruling R-102) |
| `repository-not-found` | resolve | a bare name resolves to no project directory |
| `ambiguous-name` | resolve | a bare name matches more than one |
| `target-not-repository-root` | resolve | the resolution rules above |
| `unsupported-path-bytes` | resolve | `root` or `common_dir` not valid UTF-8 |
| `manifest-invalid` | resolve | unreadable, not a mapping, wrong kind, over 1 MiB by `st_size`, or PyYAML missing |
| `no-merge-target` | resolve | no candidate exists as a local branch |
| `inspection-incomplete` | plan | a repository-wide probe failed, a row is `inspection-error`, a row was left unprobed (gate 7's reflog read cut at its filesystem budget), or, in single mode, P matches several entries or its match is undecided, any entry's realpath unread among the causes (lead rulings R-67 (b), R-73 (d), R-75 (b) and R-78 (b)) |
| `inspect-cap` | plan | more rows than the mode's cap, which counts the registry entries that become rows, the main worktree and missing rows included; a bare repository's `bare` entry and a first record equal to `common_dir` with no main worktree are no rows (D8; lead ruling R-73 (d)) |
| `deadline-exceeded` | plan | the work deadline passed while planning, or cut a read of a row (gate 7's reflog read among them, which leaves that row unprobed); in single mode, one that cut a read of P's own row (lead rulings R-278 and R-283) |
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
filesystem call (`lstat`, `realpath`, `read`, gate 12's read of `logs/HEAD`
among them, or `listdir`, gate 11's listing of the row's administrative
directory; LQ-13, LQ-14). The lane that first prints
each adds its `TEXT` key as a lead-approved contracts edit, with its fixture
in `tests/clean_support.py`: the plan notes the plan lane (T049, T051), the
row errors lane G (T031, T032), and the two status and doctor texts the US9
lane (T117, T119). Those two are command-neutral: they never say "clean
needs", and clean's own refusals keep their messages above (lead ruling
R-48).

| Code | Kind | Message |
| --- | --- | --- |
| `merge-target-conflict` | plan note | `The manifest names NAME and origin/HEAD names OTHER; NAME is the merge target.` |
| `inspection-incomplete` | plan note, single mode, not when P's match is undecided | `K other rows are inspection-error or were left unprobed; they do not block PATH.` |
| `inspect-cap` | plan note, single mode, not when P's match is undecided | `K rows past the row cap of M were not inspected; they do not block PATH.` |
| `deadline-exceeded` | plan note, single mode, not when P's match is undecided | `K rows were stopped at the work deadline; they do not block PATH.` (lead ruling R-75 (g); T099) |
| `inspect-cap` | plan note, report above 128 rows, beside `rows` | `N rows exceed the --all-safe row cap of M; --all-safe would be incomplete (inspect-cap).` |
| `os-error` | row error | `OPERATION failed: STRERROR`, STRERROR the error number's text, or Python's own text for a `ValueError`, which a path holding a NUL byte raises (a `.git` file or an admin `commondir` file that a worktree's own content makes so), with no error number, such as `embedded null byte` (T7; lane 2's wave 22 triage, sr-evidence M-2; lead R-373, writer's `e702a65`) |
| `probe-failed` | row error | `OPERATION failed: DETAIL`, DETAIL one of `exit N`, `signal N`, `cannot spawn (STRERROR)`, `unparseable output` |
| `probe-timeout` | row error | `OPERATION timed out after S s`, S the budget in force |
| `deadline-exceeded` | row error | `OPERATION stopped at the work deadline` |
| `git-too-old` | status or doctor row error, and doctor's `git` row | `Git VERSION is older than 2.36; repository inspection needs Git 2.36 or later.` |
| `git-unavailable` | status or doctor row error, and doctor's `git` row | `Git is unavailable (DETAIL); repository inspection needs Git 2.36 or later.`, DETAIL as for clean's refusal |
| `relative-config-path` | status or doctor row error, and doctor's `git` row | D18's lines, as for clean's refusal; no Git child ran (LQ-15) |

The rows the work deadline stopped are `deadline-exceeded`'s: each has only
`deadline-exceeded` row errors and is either `inspection-error`, excluded
with reason `inspection-error`, never a null reason and never carrying the
unprobed marker, or, for gate 7 alone, the row whose reflog read the deadline
cut, which stays unprobed: excluded as `reflog-unavailable`, its marker set,
its classification and recommendation kept, `deadline-exceeded` its one row
error. The marker's only setter is T066's reflog read, whether the filesystem
budget (`probe-timeout`) or the work deadline (`deadline-exceeded`) cut it, and
only the second row is `deadline-exceeded`'s (lead rulings R-67 (a), R-69,
R-75 (g) and R-278; Brett Heap's ruling "O-1: deadline-exceeded", R-263).
T099 decides which single-mode note counts them, and brings the
`deadline-exceeded` note's `TEXT` key and its fixture to the message above.

When P's match is undecided, none of the three single-mode notes is recorded:
each says that rows "do not block PATH" beside the plan's refusal of P,
`inspection-incomplete`, which speaks alone, and the `inspect-cap` note would
count P among the rows past the cap. A P that matches several entries is a
decided match, so the notes about the other rows stay beside its refusal
(lead rulings R-93 (e) and R-94 (b); T069's
`test_clean_single_target_p_s_own_realpath_unread_keeps_the_cap` pins it at the
real cap of 128).

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
for a refusal; a signal recorded before the child is spawned prints
`Cancelled.` and runs no child, and one recorded once the child has run
prints `Interrupted; the push had started and was waited for, and git exited
with status N.`, or `the branch deletion` in place of `the push`, never
`Cancelled.`, since `project` cannot prove that nothing changed (lead rulings
R-101 (e), R-108 (a) and R-177; lane 3's F2 M-1 and N13).

## Git children

Every Git child but the push child is a D2 handle: its own session
(`start_new_session=True`), standard input from `/dev/null`, both outputs
read by the driver. Every Git child but the push child has these thirty-one
names removed from its environment, unconditionally, from this fixed list
(FR-054): the seventeen of the change as ratified, then the fourteen trace
names of Brett Heap's ruling Q9 B, through which a caller could make a child
create or append to a file (draft PR #19; lead rulings R-99 (b) and (d) and
R-103); the push child has every name but the seventeenth removed and keeps
the caller's `GIT_ALLOW_PROTOCOL` (lead ruling R-28):

```text
GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_CONFIG GIT_CONFIG_PARAMETERS
GIT_CONFIG_COUNT GIT_OBJECT_DIRECTORY GIT_DIR GIT_WORK_TREE
GIT_IMPLICIT_WORK_TREE GIT_GRAFT_FILE GIT_INDEX_FILE GIT_NO_REPLACE_OBJECTS
GIT_REPLACE_REF_BASE GIT_PREFIX GIT_SHALLOW_FILE GIT_COMMON_DIR
GIT_INTERNAL_SUPER_PREFIX GIT_ALLOW_PROTOCOL
GIT_TRACE GIT_TRACE_BARE GIT_TRACE_CURL GIT_TRACE_CURL_NO_DATA
GIT_TRACE_FSMONITOR GIT_TRACE_PACKET GIT_TRACE_PACKFILE GIT_TRACE_PACK_ACCESS
GIT_TRACE_PERFORMANCE GIT_TRACE_REDACT GIT_TRACE_REFS GIT_TRACE_SETUP
GIT_TRACE_SHALLOW GIT_TRACE_WORKING_TREE_ENCODING
```

Every Git child, the push child included, also gets `GIT_TRACE2=0`,
`GIT_TRACE2_EVENT=0` and `GIT_TRACE2_PERF=0` over any value the caller set;
`0` turns each trace2 target off and outranks the `trace2.normalTarget`,
`trace2.eventTarget` and `trace2.perfTarget` of the system and global
configuration, which no `-c` pin reaches, and the other `GIT_TRACE2_*` names
stay as the caller set them (Q9 B; `TRACE2_OFF`).

`GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` stay; with `HOME` and
`XDG_CONFIG_HOME` they are read only by the configuration-path test (D11;
"Order of a run" and "`status`, `doctor` and `update`", below), and reach every
child unchanged. Read-only probes add
`GIT_OPTIONAL_LOCKS=0`; the removal and the delegates add none, and a value
the caller set reaches them unchanged, as every child received it before this
change (`GIT_OPTIONAL_LOCKS` is not among the thirty-one; D2 sets it for probes
only). The owner tools that `update --apply` runs are no Git children of
`project`'s, yet run in the push child's scrub: every name of the list but
`GIT_ALLOW_PROTOCOL` removed, and nothing added, no `-c` pin, no
`GIT_OPTIONAL_LOCKS` and no trace2 variable (`delegate_env()`; Brett Heap's
ruling LQ-12, draft PR #19 at `eae1a79`; lead rulings R-102 and R-111).

The protocol pins, on every Git child except the push child (the push-child
exception, LQ-3, awaiting Brett Heap's word on draft PR #19; research.md
R1):

```text
-c protocol.allow=never -c protocol.file.allow=never
-c protocol.ssh.allow=never -c protocol.git.allow=never
-c protocol.http.allow=never -c protocol.https.allow=never
-c protocol.ext.allow=never
```

The status pins, on every status probe, the hidden-state probe and the removal:
`-c core.untrackedCache=false -c core.fsmonitor=false -c core.trustctime=true
-c core.checkStat=default -c core.ignoreCase=false`. The third and fourth,
Brett Heap's ruling LQ-10 (draft PR #19 at `ea697ba`; lead rulings R-102 and
R-110 (b)), compare every stat field, so that an edit which keeps a file's size
and restores its mtime still shows by its ctime under a repository's
`core.trustctime=false` or `core.checkStat=minimal`. The fifth, `-c
core.ignoreCase=false`, is his Q1 (ruled on 2026-10-23T13:30:27Z, "yes,
recommended for Q1-Q9"; lead R-380; lane 2's wave 22 triage T1;
sr-classification H-2, sr-evidence H-1 and H-2, sr-removal F1; writer's
`9d5c2fb`): under `core.ignoreCase=true` on a case-sensitive file system, which
a repository made on `/mnt/c` or on macOS, a `config.worktree`, an include or
the caller's global configuration can set, Git leaves out of the status records
an untracked file whose name differs only in case from a tracked one, so that a
worktree holding it reads clean and is removed with it, and `git worktree
remove PATH` resolves PATH to another worktree whose path differs only in case,
the first in readdir order, which can be one that gate 12 excluded, its commit
with it; the pin makes Git compare names as they are spelled, and on a file
system that is truly case-insensitive it can only add records, so it fails
closed. It reaches the three kinds that carry the status pins (`GIT_KINDS`),
`STATUS_PINS` being one tuple, and not the push child.

| Child | Argument vector after `git` and its pins (its status pins first, then the protocol pins; D9, D11) | Directory |
| --- | --- | --- |
| row 1 | `--version` | the working directory |
| row 2 | `-C DIR rev-parse --show-toplevel` | the name lookup's directory (bare name only) |
| row 3 | `-C DIR rev-parse --path-format=absolute --show-toplevel --git-common-dir --show-superproject-working-tree` | where the argument resolves |
| row 3b | `-C DIR rev-parse --path-format=absolute --git-dir --git-common-dir --is-bare-repository` | the directory the refusal examined, only on a `target-not-repository-root` refusal where row 3 failed and that directory holds its own `.git`, once; never in a run that resolves; a `probe` child through the driver, counted and bounded as row 3 is; it needs no work tree, so that it answers under `core.bare=true`; a failure, a cut, or output other than the git directory, the common directory, both that `.git`, and `true` leaves the plain message (#19's round (i) at `1a4785e`, design D6; lead ruling R-271; "Resolution") |
| row 4 | `-C DIR worktree list --porcelain -z` | there while the main worktree is unknown, else `root` |
| row 4b | `-C DIR config --get core.worktree` | only when the first record is `common_dir`; an exit 1 with nothing on standard output and nothing on standard error, from a child that failed with `probe-failed` and had no bytes counted past the 4 KiB kept, is the key unset (`config_key_unset()`, which row 4c shares); any other failure, an exit 1 that printed anything (Git's `hint:` lines included) or a cut child's among them, makes the main worktree `unreadable`, refused `target-not-repository-root`, exit 2 (R-336, as R-332 for row 4c; #19's design D7, "an unset value is false and any other failure counts as true"; writer's `b3f7e0b`) |
| row 4c | `-C DIR config --file COMMON_DIR/config --type=bool --get extensions.worktreeConfig` | where rows 6 and 7 run, once per common directory, before row 6: true, false (Git prints `false`, or exits 1 with nothing on standard output and nothing on standard error, which is how `config --get` answers a key that is not set, from a child that failed with `probe-failed`), or not read where an earlier probe failed, which is read as true; any other outcome is true, failing closed: an exit 1 that printed anything on standard output or on standard error (Git's `hint:` lines, and any byte past the 4 KiB of standard error the runner keeps, count), a cut child's exit 1 included, another exit status, a signal, a timeout, or other output (R-332; #19's design D7, "an unset value is false and any other failure counts as true"; writer's `c8e23cd`; Brett Heap's ruling LQ-11; draft PR #19 at `addd346`; lead rulings R-101 (g) and R-113) |
| work tree | `-C WORKTREE rev-parse --path-format=absolute --show-toplevel` | each present linked row whose identity and registration hold, before its status probe, only where row 4c is not false; at revalidation the target's, only where row 4c read true; its output, less the one closing line feed Git ends it with, is read as one path, which may hold line feeds of its own, and where that path's realpath is the row's own realpath it holds; another path, a failure such as exit 128 under `core.bare=true`, or output that is empty, a line feed alone or without a closing line feed, which names no path, makes the row `registration-mismatch`, unprobed; a probe cut at its budget or the deadline, or a realpath read that fails, is a row error instead, the row `inspection-error` (LQ-11; lane E's report; lane 3's W70 M-2, lead ruling R-287; writer G's `4dfd6f5`, merged as `fc0019e`). At revalidation a work tree the probe decides is not the target's path, two lines of output included, since they are one path, is `identity-changed`, and a probe that fails, runs past its own budget or prints empty output, a line feed alone or output without a closing line feed is `state-changed` (the lead's R-171 and R-287; writer G's `6dec3f4`); it runs after step 5's filesystem checks, the `modules` check and the listing among them, so that one of them that refuses spares its child (the lead's R-198; writer G's `963fccf`, merged as `e2e423d`) |
| row 5 | row 3 again | `root`, only when row 3 ran elsewhere |
| row 6 | `-C ROOT for-each-ref --format=%(refname)%00%(objectname)%00%(symref)%00%(upstream)%00%(upstream:short)%00%(upstream:track,nobracket) refs/heads refs/remotes` | `root` |
| row 7 | `-C ROOT for-each-ref --merged=SHA --format=%(refname) refs/heads` | `root` |
| status | `-c core.untrackedCache=false -c core.fsmonitor=false -c core.trustctime=true -c core.checkStat=default -c core.ignoreCase=false` + protocol pins + `-C WORKTREE status --porcelain=v1 -z --untracked-files=normal --ignored=matching` | the row's worktree |
| hidden state | `-c core.untrackedCache=false -c core.fsmonitor=false -c core.trustctime=true -c core.checkStat=default -c core.ignoreCase=false` + protocol pins + `-C WORKTREE ls-files -v --stage -z` | the target's worktree |
| reachability (gate 12) | `-C WORKTREE rev-list --max-count=1 --glob=refs/worktree CANDIDATES --not --branches --tags --remotes NEGATIVES`, CANDIDATES the non-zero objects that the row's `logs/HEAD` names, NEGATIVES those that its branch's reflog named when gate 7 read it (design D21; LQ-13) | the row's worktree, for each row that passed gate 11, at most 16, and at revalidation the target's, after its hidden-state probe; a `logs/HEAD` read to its 64 KiB bound or holding a line that cannot be parsed runs no child |
| narrowed ref listing (revalidation) | row 6's format with patterns naming the merge target, the manifest's candidate, the branch `origin/HEAD` named, `main`, `master`, `refs/remotes/origin/HEAD`, and the selected branches and their upstreams | `root` |
| remote URL | `-C ROOT remote get-url origin` | `root` (push; `handoff()` in `status` and `doctor`, for an inspected repository only, R-66 (c)) |
| removal | `-c status.showUntrackedFiles=normal -c core.untrackedCache=false -c core.fsmonitor=false -c core.trustctime=true -c core.checkStat=default -c core.ignoreCase=false` + protocol pins + `-C ROOT worktree remove PATH` | `root`; PATH the registry's raw bytes, one argument, never `--force` |
| branch deletion | protocol pins + `-C ROOT branch -d -- BRANCH` | `root`; a D2 handle run by the driver with no budget, its output relayed to `project`'s streams; `--` ends the options, as push's has, so that a name that begins with `-` is a branch and never an option (lane 3's W52 F-4; lead ruling R-259; a departure, declared below the table) |
| upstream mapping | `-C ROOT config --get-all branch.BRANCH.remote`, then `branch.BRANCH.merge` | push only, for a branch with a configured upstream, after the plan's checks; one value each, REMOTE not `.` and MERGE under `refs/heads/` and not that prefix alone, or `Unsupported upstream mapping for BRANCH: U` (lead ruling R-101 (e); lane 3's F2 H-2) |
| push | `-C ROOT push -- REMOTE refs/heads/BRANCH:MERGE`, or, with no upstream, `push -u -- origin refs/heads/BRANCH:refs/heads/BRANCH` after `remote get-url origin` finds an `origin`; never a `+`, `--` ending the options; no protocol pins (lead ruling R-101 (e); lane 3's F2 H-1, M-1) | `root`; run by `execute()`, not the driver: `project`'s own streams, never read or capped; `project`'s process group, in the terminal's foreground when `project` is; never signalled, waited for, unbounded; yields no evidence |

The `--` in branch deletion's vector is an accepted departure, declared
here beside its row, since it changes a printed line: the `Cleanup action:`
command line and the child's own words read `branch -d -- BRANCH`, where
the baseline's read `branch -d BRANCH`. It departs from the packet's
sentence (BA:424-425 at `da33d92`), "`push` and `delete-branch` keep their
behavior apart from argument resolution", which states no `branch -d` vector
and so leaves the printed line to the baseline's. Without the `--` Git reads
a branch named `-f` as an option (`fatal: branch name required`, exit 128,
the branch kept), so the retry `--branch=-f` that #26 prints could never
succeed; with it, as push's vector has it, `git branch -d -- -f` deletes the
branch (lane 3's W52 F-4; writer E's `02aa71d`, merged as `d764c26`). It
rests on lane 2's ruling R-259 alone, for Brett Heap's yes or no. #19 states
it at `b3228bb`: design D18 (`design.md:1309`) says that #19 states no
argument vector for branch deletion and that feature 004 runs `git -C ROOT
branch -d -- BRANCH`, the `--` ending the options, and its proposal repeats
it (`proposal.md:1975`).

Row 6 cannot establish the upstream of a branch named `HEAD`
(`refs/heads/HEAD`), because `git for-each-ref` reports the current branch's
upstream for it. Such a row has `upstream`, `remote_present`, `ahead` and
`behind` null and is `inspection-error`, its row error `probe-failed` with
`git for-each-ref failed: unparseable output`, filling the delta's rule that
evidence not established is `inspection-error` (lead rulings R-61 and R-64
(a); built by lane G's follow-up). Since lane E's status-probe rule (below),
a repository holding `refs/heads/HEAD` makes every row `inspection-error`,
not only that branch's, because Git warns `refname 'HEAD' is ambiguous.` in
every worktree's status probe; that fails closed and narrows R-61 (b)'s effect
(lead ruling R-116).

Row 7, the merged set, is read the same way (T19; lane 3's W121 MEDIUM-2; lead
R-374 and R-385, writer's `e702a65`). Where row 6 listed the refs, a merge
target is named and row 7 failed, no row's merge state is established, so each
present row on a branch carries row 7's row errors, as it carries row 6's, and
is `inspection-error`, the plan incomplete with `inspection-incomplete`, and
never `review-required`, the rung that no value of the evidence model reaches
(the `project-clean` delta's `spec.md:178-179`); a detached row needs no merged
set and is unchanged. `status` read the same failure as `inspection-error` all
along. Before the fix such a row was `review-required` with no row error, and
the refusal counted `inspection-error` rows that the plan did not hold.

A status probe that exits 0 has still established nothing when its standard
error holds a line other than Git's advice lines (`hint:` alone or `hint:
TEXT`), or a byte past the 4 KiB the runner keeps: it is `probe-failed` with
DETAIL `unparseable output` (`git status failed: unparseable output`), the row
`inspection-error` with `dirty` null, and at revalidation a `state-changed`
difference (`status_warned()`; lane 3's US2 M-1; lead ruling R-116). Git prints
nothing there on a clean run, and it translates its `warning:` and `error:`
prefixes under a localized catalogue, so the rule reads no prefix but the
advice one; no DETAIL form is added. A blank line is such a line, and only the
empty text after the last line end is none: the rule skipped a blank line until
Brett Heap's Q8 (ruled on 2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9";
lead R-380; lane 2's wave 22 triage T9, lane 3's W115 MEDIUM-1; writer's
`70345ee`), which states it in #19's `project-command` delta at round (q),
`818311a`, with its consequence that a repository holding `refs/heads/HEAD`,
for which Git warns `refname 'HEAD' is ambiguous.` in every status probe, has
every row `inspection-error`, and which words the scenario "A git that floods
standard error" so that the probe completes with no `probe-timeout`, the
standard error kept is capped, and the row is `inspection-error` with
`probe-failed`. Git exits 0 when it cannot read a directory and leaves what it
could not read out of its records, so a row whose untracked directory is
unreadable no longer reads clean.

A linked row whose path encloses another repository path is
`registration-mismatch` (Brett Heap's Q2 (1), ruled on 2026-10-23T13:30:27Z,
"yes, recommended for Q1-Q9"; lead R-380; lane 2's wave 22 triage T2;
sr-classification H-1, sr-evidence H-3; writer's `5eeaedd`). Git's directory
walk skips every entry named `.git`, so where the main worktree or the common
directory sits in a tracked directory of a linked worktree, as `git worktree
repair` can leave it, that worktree reads clean and its removal deletes the
whole repository, its branches and stash with it. `enclosing_rows()`, a pure
function of values already read, nothing read again, marks each present linked
row whose raw path or realpath is, or is an ancestor of, the common directory,
the main worktree, another registry entry's raw path (an entry the call builds
no row for, one past the row cap, included) or another built row's realpath.
The row is `registration-mismatch`, unprobed and `inspection-error`, as a
shared path is (`worktree_rows()`, before any status probe), so the plan is
incomplete with `inspection-incomplete`, exit 1 for a preview and 2 under
`--apply`, in batch and in single mode, and nothing is removed. A path that
only shares a prefix is not enclosed, and the main worktree's own row is never
one, gate 1 keeping it.

A linked row whose registered path is a symbolic link
is `registration-mismatch` too (Brett Heap's Q9 (b), ruled on
2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; lane 2's wave
22 triage T12, sr-removal F7; writer's `338edb0`). A worktree moved by hand,
with a link left at its registered path, agrees with its registration through
the link and its status prints nothing, but `git worktree remove` empties the
link's target, fails to remove the link, exits 255 and still deletes the
administrative directory; the result is `failed`, `git-failed`, with
`orphaned-directory` in the JSON alone. `_read_row()` already makes the `lstat`
of the registered path, and where it shows a symbolic link for a linked row it
reads the registration as disagreeing (`registered` false, no admin id), so the
row is `registration-mismatch`, unprobed and `inspection-error`, as a shared
path is: the plan is incomplete with `inspection-incomplete`, exit 1 for a
preview, which still selects a clean worktree beside it, and 2 under `--apply`,
in batch and in single mode, with nothing removed and the link's target keeping
its files. The main worktree's row is never read so.

Gate 9 also looks for a `.git` inside a tracked directory (Q2 (2), the same
ruling and triage item; writer's `5eeaedd`). Git's directory walk recurses into
a directory that the index tracks without asking whether it holds a repository,
so a repository nested there, or any entry named `.git`, shows in no status
record and passes Git's own check, and the removal deletes it, the inner
repository's commits with it. `HiddenStateParser` keeps `directories`, every
directory above an index entry that it read before its bound, the worktree's
top level aside (a gitlink ends the listing). Then `hidden_state_probe()`, once
its gitlink test has failed and before its flagged-entry test, runs
`nested_git_check()`: one `fs_call()`, through `_fs()` with OPERATION `lstat`,
counted in the filesystem budget and bound by `min(5 s, work remaining)`, no
Git child, which makes an `lstat` of `<dir>/.git` for each of those directories
in byte order (`nested_git_entry()`). An entry of any type is
`contains-submodule`, and so names the row's reason even beside a flagged
entry, gate 9 coming before gate 10; `ENOENT` or `ENOTDIR` for every one, or no
directory, passes; any other error is the row's `os-error` and the row
`inspection-error`, the plan incomplete; and a call cut at its budget is
`probe-timeout`, or `deadline-exceeded` where the work deadline was the limit.
It runs for the rows that reach gate 9, at most 16, and again at revalidation
inside the hidden-state probe, step 7 (data-model.md, "Revalidation step and
`probes_performed`"): an entry is `contains-submodule`, a read that fails
`state-changed`, and one that the work deadline cuts `deadline-exceeded`. No
Git child is added, so `probes` is unchanged.

At revalidation (data-model.md, "Revalidation step and `probes_performed`")
one rule decides every read that does not finish with a value: a Git child
that fails, runs past its own budget while the deadline is not the limit, or,
as the work-tree probe can, prints output that names no path (empty, a line
feed alone, or without a closing line feed; R-287), and a filesystem
call that fails other than with `ENOENT` or `ENOTDIR`, or runs past its own
budget while the deadline is not the limit, gives `state-changed`, whatever
its step; a read gives its step's own reason only for a value it decided;
and one that the work deadline cuts gives `deadline-exceeded`, the target and
every later one `not-attempted` (draft PR #19 at `4485678`, `2e819ad` and
`9267303`, "Cleanup revalidates destructive actions"; the lead's R-171,
R-195, R-198 and R-208; writer G's `6dec3f4`, `f6082db` and `73d8888`). So the
identity probe, the registry listing and the hidden-state probe, which gave
`identity-changed` or `hidden-local-state` for a failure until R-195, give
`state-changed`, and since R-208 so do step 1's identity reads (the
realpaths and the common directory's lstat), step 5's lstat of the target,
its registration reads (a `.git` that cannot be read among them), the twin
check's lstat and realpath of a registry entry, and the `modules` check,
which gave `identity-changed` or, for the `modules` check, `contains-submodule`
before. `ENOENT` or `ENOTDIR` is no failure: it decides that the path is
absent, which keeps the step's reason, so that an absent target or `.git`
is `identity-changed`, and so is a listing that finds no administrative
directory, writer G's reading of a gap in #19 at `9267303`, which lane 3's
W38 L-4 asks #19's round (e) to state (lead ruling R-220).

Bounds: each probe child gets `min(5 s, work remaining)` under `clean`'s 60 s
deadline (50 s of work, a 10 s reserve, time at the question excluded), each
rescan child `min(5 s, reserve remaining)`; a child past its budget, at its
record bound or on a signal gets SIGTERM to its group, SIGKILL 2 s later, and a
reap wait of at most 2 s more, then is abandoned as `probe-timeout`. The
removal is spawned only while 5 s of the work deadline remains, is never
signalled before its 300 s ceiling, and is waited for. Push and branch deletion
stay unbounded: no budget and no deadline. A signal recorded while the push or
`git branch -d` child runs is not passed on: `project` never signals either
child, waits for it, and then exits by D19's first row (data-model.md, "Exit
statuses"); the slot is read just before either child is spawned, so a signal
recorded by then runs no child (lane 3's N13; lead ruling R-177). Probing is
serial; termination never blocks (data-model.md, "Child handle"). Revalidation
spawns at most six Git children per target, gate 12's reachability probe the
sixth (LQ-13), and seven where row 4c read `extensions.worktreeConfig` as true
(the work-tree probe; LQ-11), the final rescan at most three, the identity
probe counted once: a line feed in the root's or the common directory's path
repeats it, one child per option, so that they run up to 9 (10 with the
work-tree probe) and 6 (design D6, "the rare repeat"; data-model.md,
"Revalidation step and `probes_performed`"; lead ruling R-82 (c)). The
work-tree probe runs after step 5's filesystem checks, so that where one of
them refuses first its child, the seventh where row 4c read true, does not run
(R-198). Gate 11's listing and gate 12's `logs/HEAD` read are filesystem reads,
no child (LQ-14, LQ-13). `LIMITS["revalidation_children"]` is 6 and
`LIMITS["revalidation_children_worktree_config"]` 7, and the plan's estimate
counts 6T + 3, or 7T + 3 where row 4c read true, the number
`revalidation_children()` picks, so that `probes.estimated` equals
`probes.performed` there too (lead rulings R-165 and R-201; writer G's
`8ae0bb5`). Where a line feed in the root's or the common directory's path
repeats the identity probe, the estimate counts the repeat too, 3 more
children for each revalidation (`revalidation_children()` gives 9, or 10 where
row 4c read true) and 3 more for the final rescan (`rescan_children()` gives
6), the three being the options of `IDENTITY_OPTIONS` that run beside the
combined child (`identity_split_children()`, read from the root and the
common directory as the plan read them), so that `probes.estimated` equals
`probes.performed` on such a path as well: #19's delta says that the plan's
`probes.estimated` counts those extra children (its `spec.md:1050-1056` at
`b3228bb`; lane 5's RI-3, writer E's measure, lead ruling R-259; writer G's
`c26e44b`, merged as `7164d7f`), and the estimate before it fell three short
for each target and three for the rescan on such a path. Whether these bounds fit the 50 s work deadline is D14's to say:
draft PR #19 at `2e819ad` gives the fit on three bases, BA's flat 150 ms per
child, task 2.1's measured costs with stand-ins for the two probes it did not
measure, and a mixed basis, and chooses none; which basis the cap test uses, or
what those two probes cost, is the first step of open question LQ-20, before
Brett Heap (lead rulings R-196 and R-197).

## `status`, `doctor` and `update` (FR-050 to FR-053, FR-059; D16)

| Aspect | Contract |
| --- | --- |
| Git check | `git --version` once per invocation, memoized, when a repository is inspected; doctor's `git` row runs it itself when none was, and `status` never runs it for nothing (lead ruling R-56); never a refusal |
| Configuration paths | the test of "Order of a run", step 2, at each command's entry, before any Git child: a failure is memoized in the version check's place with code `relative-config-path` and D18's lines, so that no Git child starts, `git --version`, `discover()`'s lookup and `handoff()`'s remote read included, and each command reports it where it reports a Git below the floor (`hold_git_for_config_paths()`; Brett Heap's ruling LQ-15; lead rulings R-102, R-131 (a) and R-173); a `HOME` that begins with `~` (`~`, `~/x`, `~user`) fails it as any relative value does, and nothing is read or expanded against a `HOME` that fails it: no workspace configuration, credential presence file, default projects directory, workBenches root or marker, or `~` path, so that `Path.home()`, which raises for such a `HOME`, is never called on it (`home_directory()`, `expand_user()`; lead rulings R-202 and R-205; lane H's `22f95d1`, merged as `0b7dd94`) |
| A `~` target under such a `HOME` | a target argument that needs `~` expanded, `~` alone or `~/...`, refuses with `relative-config-path` and D18's `HOME` line, exit 2, no Git child, where it raised a traceback; `~user` is read from the user database, never from `HOME`, and expands as before (`discover()`; lead ruling R-205 (a)) |
| `handoff()`'s remote read | `git remote get-url origin` only for a root whose repository was inspected, present and past the version check; otherwise the same no-identity state and no child (lead ruling R-66 (c)) |
| No `.git` | `present: false`, no Git child, as today |
| Uninspectable root, leg or worktree | `classification: "inspection-error"`, `errors`, unestablished values null, `worktrees` among them (R-56); status exits 0; a failed configuration-path test gives the root `present` null and one `errors` entry, `relative-config-path` with D18's lines |
| Doctor's `git` row | `ok` with the detail `PATH (git version X)`, or `error` with the detail `CODE: MESSAGE`, CODE `git-too-old` or `git-unavailable` and MESSAGE its command-neutral text, or CODE `relative-config-path` and MESSAGE D18's lines ("Codes"; lead rulings R-48 and R-57; LQ-15); doctor then exits 1 by its error rows |
| Doctor's error rows | one per null `present`, null `dirty` from a failed or timed-out probe, and `inspection-error` row; none for a null that means "none" |
| Human `status` and `doctor` | `Git: inspection-error (CODES)` in place of the branch line |
| Deleted upstream | `upstream` is the configured short name; `ahead`, `behind` null |
| Paths in JSON | `path_valid_utf8` beside every `path`, `root_valid_utf8` beside every `root`, `ignored_samples` entries as objects |
| Budgets | 15 s per Git child, no deadline, no row cap; non-Git children keep 15 s |
| `update --apply --component shape` or `bench` | refuses with exit 2, invoking no owner tool, unless the root's and every child's `dirty` are exactly false; a failed configuration-path test leaves the root's `dirty` null, so it refuses with its existing message, `Project updates require a clean tracking checkout; preserve feature work first.`, as for a Git below the floor (D16 as amended for LQ-15; lead ruling R-131 (a)) |
| `update --apply --component tools` or `workflow` | needs no Git; not refused for Git's version or for the configuration-path test |
| Owner tools of `update --apply` | run with the push child's scrub, every one of the thirty-one names but `GIT_ALLOW_PROTOCOL` removed and nothing added (`delegate_env()`; LQ-12; "Git children" above) |
| Signals | SIGTERM and SIGHUP during inspection exit 143 and 129 after the probe groups are killed; at `Type yes` and during a delegate, as today |

The JSON of `status` and `doctor` stays unversioned; every change to it is
additive.

A known residual, recorded and not fixed here: `status` prints the
baseline's advice for a stale worktree, `Review the stale worktree metadata
before pruning it manually.` (`repo_state()`), which omits unlocking for a
locked stale entry, though `git worktree prune` keeps a locked entry, on Git
2.43.0 and 2.36.6 alike, while `clean`'s report says `Review, unlock it, then
prune stale worktree metadata manually.` (F-10; `recommendation_stale_locked`;
data-model.md, "Classification"). It is left to a follow-on change, because
FR-064 keeps the baseline's functions unchanged (lane 3's W65 LOW-3, read
again in W72; lead ruling R-269). Q3 (b)'s dry-run warning does not reach it
either: `status`'s text names pruning, not the command, and the warning was
ruled for `clean`'s texts that name `git worktree prune`, so it stays with the
same follow-on change (R-380).

An accepted departure from FR-064, ruled by Brett Heap on 2026-10-23, "Yes,
add T9 (Recommended)" (T9; lead R-365; writer's `7a20789`, merged as
`d8724e2`): `status` lacked the warning against `git worktree prune` that
`clean`'s recommendation takes beside an unread row
(`recommendation_stale_worktree_unread`; R-320, lane 3's W86 NM-1), though
`git worktree prune` deletes the admin directory of a live worktree whose path
Git cannot stat (`EACCES`), whichever row it is run for. So where any row of
the listing has a path that could not be read (`path_unread(row)`: its `lstat`
failed other than for the path's absence, `present` null), `repo_state()`,
which `status`, `doctor` and `update` share, gives each stale entry's
`recommendation`, a locked one included, `Review the stale worktree metadata
before pruning it manually; a row's path could not be read, so do not run git
worktree prune, git worktree remove or git gc until it can.`, in `status
--json` and `doctor --json`; with every path readable it is the baseline's
text above, byte for byte. Only that text changes: no field, key, class or
exit status does.

`new`, outside this feature, takes the same rule as an accepted departure:
with no parent argument, no `--into` and no `PROJECTS_DIR`, under a `HOME`
that fails the test it has no default parent and refuses with D18's `HOME`
line, exit 2, where it raised a traceback or created the project under a
relative `h/projects` (lead ruling R-205 (b), for Brett Heap in #33's body).
`new --into ~/x` under a `~` `HOME` still raises, outside LQ-15 (R-205's LOW
follow-up).
