Lane: openRepoProject-2

# Data Model: Safe batch worktree cleanup

Nothing is stored. Every `project clean` run builds its plan fresh and never
stores or reuses it (FR-025); these are the values one invocation reads,
derives and reports. JSON shapes are in
[contracts/project-clean.md](contracts/project-clean.md); exact human text is
`design.md` D18 and D14. Line citations are at `961c405`.

## Entities

### Repository identity (D7, D8; FR-016, FR-017, FR-055)

| Field | Source |
| --- | --- |
| `root` | realpath of the main worktree, decided in D8's order; also the envelope's `root` and the command directory |
| `common_dir` | realpath of row 3's `--git-common-dir`; never a worktree row |
| `dev`, `ino` | `lstat` of `common_dir`, not following a symlink |
| `root_valid_utf8`, `common_dir_valid_utf8` | the escaping rule; always true in `clean` |

Validation: an absolute argument's realpath must equal `root`, and `root`
must be the main worktree; a bare repository, a submodule checkout and a
linked worktree whose main checkout cannot be named refuse with
`target-not-repository-root`; a `root` or `common_dir` that is not valid
UTF-8 refuses with `unsupported-path-bytes` before any plan or digest. The
four identity fields go into the plan and its digest, and are compared at
every revalidation and first in every rescan; `dev` and `ino` are host-local,
so a remount that renumbers them fails closed.

Row 4, the registry listing, runs in the directory the argument resolves to,
where row 3 ran, in every layout, "while the main worktree is not yet
known", as the `project-command` delta says (its `spec.md:124-133` at `0050f3e`,
the ratified copy; the paragraph is at `:192-201` at `4512441`). Rows 6 and 7
run in the main worktree where it is known; where `root` is null, in
the common directory for a bare repository only, and otherwise where row 3
ran (lead ruling R-75 (j)). Row 4c, `extensions.worktreeConfig` read from
the common directory's own `config` file, runs there too, once per common
directory and before row 6; where an earlier probe failed and it was not
read, it counts as true, failing closed (Brett Heap's ruling LQ-11; lane E's
report). It is false where Git prints `false`, or exits 1 having printed nothing on
either stream, which is `config --get`'s answer for a key that is not set, and
only from a child that failed with `probe-failed`; every other outcome is
true, an exit 1 that printed anything on standard output or on standard error,
or a cut child's exit 1, included (R-332; #19's design D7, "an unset value is
false and any other failure counts as true"; writer's `c8e23cd`). Where row 5 fails, `repository.root` stays null, and the
resolution still names the main worktree as the command directory from the
evidence's `main_path`, the path `main_worktree()` named before row 5 ran
(the plan review's F2; lead ruling R-101 (c)).

### Merge target (D8; FR-018, FR-060)

| Field | Value |
| --- | --- |
| `name` | the first candidate that exists as a local branch |
| `source` | `manifest`, `origin-head`, `main` or `master` |
| `sha` | the branch's head from row 6 when the plan is built |

Candidates, in order: the manifest's `tracking_branch` less a leading
`origin/`; the symref of `refs/remotes/origin/HEAD` less
`refs/remotes/origin/`; `main`; `master`. A name that no ref can hold, such as
the lone surrogate of a manifest's `"\ud800"`, which YAML builds and
`str.encode` cannot encode, names no local branch and is no candidate, so the
next candidate is taken (FR-018; T7, lane 2's wave 22 triage, sr-evidence M-3;
lead R-373 and R-385, writer's `e702a65`): `status` exits 0, and the
revalidation's narrowed ref listing leaves such a name out. The manifest is
read at `root` by one bounded filesystem call per candidate file:
`project.yaml`, then `family.yaml` when there is no `project.yaml`, by
`Path.is_file()`'s test, as `manifest()` picks it (lead ruling R-73 (e)). An
`st_size` over 1 MiB is `manifest-invalid` without a read, and an unreadable
manifest, one that is not a mapping or has the wrong kind, and a missing PyYAML
are `manifest-invalid` too, with the contract's messages. No candidate refuses
with `no-merge-target` and its baseline message (`project:551`). A manifest
and `origin/HEAD` naming different existing branches: the manifest wins,
with the plan note `merge-target-conflict`.

### Worktree row (FR-006, FR-042, FR-056, FR-057)

One registry entry, the main worktree included. Baseline keys keep their
names and types; the last six are added.

| Field | Value | Null means |
| --- | --- | --- |
| `path` | the registered path, from the NUL-delimited registry | never null |
| `present` | true; false when `lstat` fails with `ENOENT` or `ENOTDIR` | any other `lstat` failure (with an `os-error`) |
| `branch` | short name, or the text `detached` for a detached HEAD; the row's own `detached` flag, true where the registry record has no branch, tells that HEAD from a branch named `detached`, and no document writes the flag (T10) | (baseline) |
| `head` | full object name | not established |
| `upstream` | configured short name, also when its remote-tracking ref is gone | none configured; not established for a branch named `HEAD` (below) |
| `remote_present` | false when the track is `gone` | none configured, or not established, a branch named `HEAD` among them |
| `ahead`, `behind` | from the track field | none configured, ref gone, or not established |
| `dirty` | from the combined probe | probe not run, failed or timed out |
| `ignored_files` | ignored records read; a lower bound when truncated | probe not run or failed, or stopped before any ignored record |
| `current` | the working directory is inside it (baseline) | |
| `merged_into_target` | head is in row 7's merged set | detached, or not established, row 7 having failed (T19) |
| `classification`, `recommendation` | the ladder below; the recommendation keeps its baseline text, except for the main worktree's row where the ladder says `merged-removable` or `merged-current`, and a locked `stale-worktree` row (lane 3's W52 F-6 and F-10; lead ruling R-259) | |
| `prunable` | `true` when the record says `prunable`, else absent | |
| `locked` | from the registry's `locked` attribute | never null |
| `ignored_files_truncated` | the probe stopped at a bound | probe not run or failed |
| `ignored_samples` | at most 8 `{path, path_valid_utf8}`, paths relative to the worktree | probe not run or failed |
| `path_valid_utf8` | the path is valid UTF-8 | never null |
| `errors` | `{code, message, path?, path_valid_utf8?, reason?}`: `os-error`, `probe-failed`, `probe-timeout`, `deadline-exceeded`; each present row on a branch also carries the errors of row 6, or of row 7 where row 6 was read, when that listing failed (below; T19) | |
| `notes` | `partially-removed` (D4) or empty | |

Null means unknown or not established, never a default false or 0, in every
field this change adds (FR-043, FR-045); `upstream`, `ahead`, `behind` and
`merged_into_target` keep their baseline "none" meaning where the table says
so, which doctor never reports as an error (FR-051).

### Worktree identity and registration (D7; FR-055)

`{path, dev, ino, admin_id}` together, recorded for each selected row. The
registration holds in both directions between realpaths: `<path>/.git` is a
regular file whose `gitdir:` line names `<common_dir>/worktrees/<admin_id>`,
and that directory's `gitdir` file names `<path>/.git`, relative values
resolved against the directory holding the file; and that directory's
`commondir` file, read as Git's `get_common_dir_noenv()` reads it, a
relative value resolved against the directory, names `<common_dir>`, a
missing file naming the directory itself, so that a `commondir` rewritten to
name another repository is `registration-mismatch` and a read that fails is
`inspection-error` (LQ-11 as amended for lead ruling R-125; draft PR #19 at
`93f3194`). Each row's identity is read twice: once with the other rows,
and again immediately before its own status probe, its `lstat`, realpath and
two-way registration in one bounded filesystem call, since the probes of the
rows before it may take their whole budgets; a row whose identity changed
gets no probe and is `inspection-error`, and once the work deadline has
passed no probe starts (lane 3's F3; lead ruling R-101 (e)). A read of either
file whose content holds a NUL byte, which Git reads as a C string and Python's
`os.path.realpath()` and `lstat` refuse with a `ValueError`, is an `os-error`
row error with Python's own text and no error number, as a failed read is
(`_fs()` and `_direct()` catch it; T7, lane 2's wave 22 triage, sr-evidence
M-2; lead R-373 and R-385, writer's `e702a65`): the row is `inspection-error`
and gets no probe, `status` exits 0, and `clean` is incomplete, where `status`
ended in a traceback and every `clean` was refused `internal-error`. Then,
where row 4c is not false, each linked row's effective work tree is probed
(`rev-parse --path-format=absolute --show-toplevel` in it); its output, less
the one closing line feed, is read as one path, which may hold line feeds,
since a worktree whose own path holds one prints that path over two lines or
more: a work tree other than its path, a failure, or output that is empty, a
line feed alone or without a closing line feed is `registration-mismatch`,
unprobed, and a probe cut at its budget or the deadline is a row error,
`inspection-error` (LQ-11; lead rulings R-113 and R-287; lane 3's W70 M-2). A
row with `present: false` is decided first: it gets no registration check, no
shared-path check and no probe, and its reason is its class, `stale-worktree`
(lead rulings R-57 and R-59 D5). Otherwise a row whose registration disagrees
gets no status probe and is `inspection-error`, excluded as
`registration-mismatch`. Two registry entries naming one path, compared by
the registry records' raw path bytes as listed, fail closed: each is
`registration-mismatch`, since the porcelain listing does not name the admin
directory, so the two-way check alone cannot tell them apart (lead rulings
R-57, withdrawing R-51(c)'s known limit, and R-59 D5). The rule extends to
present rows spelled differently with the same realpath, or with the same
admin id, which both pass the two-way check: each is
`registration-mismatch` too, in `--all-safe` and in single mode (lead
ruling R-67 (c), lane 3's L-4). It is built, as `shared_identities()` in
region `evidence` (evidence follow-up 2, merged as `a5156a5`; lead ruling
R-81 (a)). The comparison is among the present rows one `worktree_rows()`
call inspects together, before any status probe, so that neither twin is
probed; in single mode `match_target()` matches P against the whole
registry by realpath, so P's twins are among P's rows. A twin made after
planning is seen at revalidation, which US6 built as `registry_twin()`, step
5 of the table in "Revalidation step and `probes_performed`" below (lead
rulings R-81 (a) and R-89 (a)): every entry of the fresh registry listing,
a row past the cap included, is read as `worktree_rows()` reads a row and
compared by `shared_identities()`, by realpath and by admin id; under the
two-way check's regular-file rule (`_gitfile()` takes `<path>/.git` only as a
regular file, so a `.git` that is a symbolic link gives no admin id), two
registered entries with one admin id also share a realpath, so the admin-id
comparison is a second guard that never decides alone (R-81 (a); lane 3's
final delta read, LOW-6; lead ruling R-101 (e)), and a present entry sharing a
checked row's realpath or admin id gives `identity-changed`. An entry whose
lstat or realpath fails other than with `ENOENT` or `ENOTDIR`, a call cut at
its probe budget included, is a difference too, since a twin could stand
behind it and a value that cannot be re-read is a difference (the
`project-clean-review-safety` delta's `spec.md:92-93`), as planning fails
closed on such an entry alike: `state-changed` since the lead's R-208, a read
that decided nothing, where it was `identity-changed` (writer G's `73d8888`,
merged as `9ab996e`).
One entry is none: a row the plan itself read as `present: null`, whose
lstat fails again, null in the plan and null again (the same delta's
`spec.md:89-92`); in single mode the plan recorded it as another row's
non-blocking `inspection-error`, which does not refuse P (the `project-clean`
delta's `spec.md:258-262`). An entry the plan never read, new since planning
or left past the row cap, is not one of them and refuses, failing closed; an
entry whose lstat or realpath gives `ENOENT` or `ENOTDIR` is absent and
compared by neither (R-36) (lead rulings R-93 (e), LOW-3, and R-95 (c)).
Three residuals remain, the last two recorded and not fixed (lead ruling
R-95 (d)): at planning, a twin past the row cap is not compared, the plan
being `inspect-cap` anyway; an entry whose registration alone cannot be read
is compared by its realpath only (R-57 L2); and in single mode a twin of P
that existed at planning and is spelled through an unsearchable directory is
not caught, since `match_target()`'s non-strict realpath does not raise on
`EACCES` and the null-and-null rule applies, though no work is lost, because
both spellings name one clean, merged worktree (lane 3, LOW-3); closing it
would conflict with the `project-clean` delta's `spec.md:258-262`.

Two more rules of registration are `clean`'s plan alone, not part of the
evidence model that `status`, `doctor` and `update` share (lane 3's W139
MEDIUM-1; lead R-409): Brett Heap's Q2 (1), that a linked row whose path is, or
is an ancestor of, the common directory, the main worktree or another row's
path is `registration-mismatch` (`enclosing_rows()`), and his Q9 (b), that a
linked row whose registered path is a symbolic link is (`_read_row()`'s read of
the `lstat` it makes already). They are his rulings on `clean`'s review safety,
which #19 states in the `project-clean-review-safety` delta (`spec.md:13-17` at
`54e869b`); the `project-command` delta states neither, so its parity rule
(`spec.md:311-312`, "Values SHALL equal those of the inspection this model
replaces, except where a requirement states a change.") keeps the three
commands at the baseline's values (#19's `design.md:591-598` at `54e869b`).
`worktree_rows(repo, run, records=None, for_clean=False)` and `_read_row()`
take `for_clean`, which `match_target()`, `build_plan()` and `registry_twin()`
set and `repo_state()` does not, so `status`, `doctor` and `update` read such a
row as the baseline does, probed and with its own `dirty`, as `f3724fc` did,
where `41759a4` made both `inspection-error` and `doctor` exit 1. R-67 (c)'s
shared-path and twin rows are not gated: they stay `registration-mismatch` in
every command.

### Branch evidence (D6, D7)

`{branch, head, upstream, upstream_oid, ahead, behind}` from row 6, recorded
for each selected row. For a branch whose configured upstream's
remote-tracking ref was deleted, `upstream` is the short name and
`upstream_oid`, `ahead` and `behind` are null; at revalidation a value null
in the plan and null again is no difference, and one that reappears is
`state-changed` (D7, D20). For a branch named `HEAD` (`refs/heads/HEAD`),
`git for-each-ref` reports the current branch's upstream, so row 6 cannot
establish its upstream: its `upstream`, `remote_present`, `ahead` and
`behind` are null, meaning not established, never "none configured", and
the row is `inspection-error` with `probe-failed`, `git for-each-ref failed:
unparseable output` (lead rulings R-61 and R-64 (a); built by lane G's
follow-up). Since a status probe whose standard error holds anything but
Git's advice lines establishes nothing (contract, "Git children"), and, under
Git's default `core.warnAmbiguousRefs`, Git warns `refname 'HEAD' is ambiguous.`
in every worktree of such a repository, every row there is `inspection-error`
too, failing closed (lead ruling R-116, which narrows R-61 (b)'s effect), a rule
that counts a blank line as such a
line and the empty text after the last line end as none, and that #19's
`project-command` delta states at round (q), `818311a`, with this consequence
(Brett Heap's Q8, ruled on 2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9";
lead R-380; lane 2's wave 22 triage T9; writer's `70345ee`), and at round (r),
`4512441`, with the qualifier (lane 3's W131 LOW-3; lead R-391). With
`core.warnAmbiguousRefs` false, in the repository's configuration or the user's,
which no pin overrides, the same pinned probe exits 0 with empty standard error,
on Git 2.43.0 and 2.36.6, so that no row is `inspection-error` on that account,
a run of `add-project-clean-branch-retirement` can retire `refs/heads/HEAD`, and
that change's `Retired HEAD` restore line is then the restore that works; 004
adds no pin for it and changes no behaviour (#19's design D1 at `4512441`).
Where row 6 gives no listing, because it or a probe before it failed, each
present row on a
branch carries that probe's row errors and is `inspection-error`, its upstream
fields null, where every row once printed as `unpublished` (the plan review's
F3; lead ruling R-101 (c)). Row 7 is read the same way (T19; lane 3's W121
MEDIUM-2; lead R-374 and R-385, writer's `e702a65`): where row 6 gave its
listing, a merge target is named and row 7 failed, no row's
`merged_into_target` is established, so each present row on a branch carries
row 7's errors and is `inspection-error`, never `review-required`; a detached
row needs no merged set.

A row whose `present` is null is unread: `path_unread(row)` is `row["present"]
is None`, and `unread_paths(plan)` is the set of the raw paths of such rows of
`plan.rows`, from what planning recorded and nothing read again (the
revalidation's registry-twin check reads it too). Wherever it is not empty, a
deadline-stopped row and a row the refusal does not count included, the plan
prints no `git worktree prune` advice, since prune deletes the admin directory
of a live worktree whose path Git cannot stat: `TEXT`'s `next_step_unread_row`
for the unread row, `next_step_inspection_error_unread` and
`next_step_registration_mismatch_unread` for the other two reasons' groups,
and `remedy_inspection_incomplete_unread` or
`remedy_inspection_incomplete_redirect_unread` for the refusal, each as the
contract's "The unread forms" gives it (#19's round (l); lane 3's W87 M-1;
lead rulings R-307 and R-310, confirmed by Brett Heap (R-319); writer's
`e569564`, merged as `1edf64e`). R-320 (lane 3's W86 NM-1; ruled by Brett
Heap, "R-320: yes", lead R-321; writer's `dfc2baa`, merged as `12c1821`) adds
`recommendation_stale_worktree_unread`, or, locked,
`recommendation_stale_locked_unread`, as each `stale-worktree` row's
recommendation wherever the set is not empty, set by `stale_recommendations()`
once every row is gated, and makes the `inspect-cap` remedy
`remedy_inspect_cap`, which carries the same warning always, since the rows
past the cap are never read. R-324 (ruled by Brett Heap, "R-324: yes", lead
R-343; #19's round (n) at `2250830`; writer's `e8dda2a`) makes each of these
warnings, and `partial_removal_note_unread`'s, also name `git worktree remove`
and `git gc`. R-365 (ruled by Brett Heap on 2026-10-23, "Yes, warn
(Recommended)" for lane 3's W52 F-1 (b) and "Yes, add T9 (Recommended)" for T9;
lead R-365; writer's `7a20789`, merged as `d8724e2`) carried the same warning
into two texts outside the plan: the result's ceiling note, which was
`partial_removal_note_prune_unread` in place of `partial_removal_note_prune`
wherever the set was not empty, and which Brett Heap's Q3 (a) superseded (ruled
on 2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; "Target
result and reconciliation record" below), and `status`'s stale recommendation,
which `repo_state()` ends with the warning wherever any row of its listing is
unread ("Classification" below), and which stands. Q3 (b) (ruled on
2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; writer's
`da5502d`) ends the plain forms of the texts that name `git worktree prune`,
where the set is empty, with a dry-run warning, `; git worktree prune also
deletes the entry, and so the HEAD reflog, of every other worktree whose path
is missing, one moved or on an unmounted drive included, so run git worktree
prune --dry-run first and remount or repair any it lists that still exists`
(the contract's "The unread forms" and the paragraph after it). Only texts
change: no field, code, class or reason does, though a stale row's
`recommendation` in the report and in `--json`, and in `status --json` and
`doctor --json`, carries the new text.

Brett Heap's M3 (a) (ruled on 2026-10-23T21:10:31Z, "yes, recommended for M1
and M3"; lead R-413; lane 3's W133 MEDIUM-3; #19's round (t) at `54e869b`,
design D18 at `design.md:1477-1492`; writer's `d640539`) gives a
`registration-mismatch` row whose path is, or holds, the main worktree, the
common directory or another worktree (Q2 (1)), or which shares its path with
another row (R-57 L3, R-67 (c)), `TEXT`'s
`next_step_registration_mismatch_holds` in place of the class's step, since the
class's "or remove the row by hand" would delete what the row's path holds:
`its path is or holds the main worktree, the common directory or another
worktree, so do not delete it by hand or with git worktree remove; review its
registration with git worktree list --porcelain` (197 characters, copied from
`project` by script). It names no `git worktree prune`, so it takes no Q3 (b)
warning, has no unread form and is the same in every mode. `WorktreeRow.holds`,
a flag that `worktree_rows()` sets and no output serializes, marks such a row,
and the preview prints those rows in a group of their own under
`registration-mismatch`, first, ahead of the class's group
(`excluded_groups()`; the contract's paragraph after the
`registration-mismatch` next step). Only a text and the preview's grouping
change: no field, code, class or reason does.

### Classification (D6; FR-007)

First, a row whose evidence could not be established (`present` null, a
registration that disagrees, a status probe that failed or timed out, or branch
evidence row 6 or row 7 could not establish, a branch named `HEAD` with its
`probe-failed` row error, R-61 and R-64, a failed merged set, T19) is
`inspection-error` directly, whatever its branch, so a failed probe on the
merge-target checkout is never `protected-default`. Every other row takes the
first rung that holds, in this order (names unchanged; the one reorder is
marked):

| Rung | Holds when |
| --- | --- |
| `stale-worktree` | `present` is false |
| `protected-default` | `branch` is the merge target, a detached HEAD being none (the `detached` flag, not the text; T10) |
| `inspection-error` | `dirty` is null |
| `dirty` | `dirty` is true |
| `ignored-local-files` | `ignored_files` is non-zero |
| `detached` | the row's `detached` flag: the registry record has no branch (T10); a branch named `detached` is a branch |
| `unpublished` | no upstream configured |
| `remote-gone` | `remote_present` is false; but first (the reorder) a merged row is `merged-removable`, or `merged-current` when it is current |
| `review-required` | defensive; no value of the evidence model reaches it, a failed row 7 giving `inspection-error` (T19) |
| `diverged` | `ahead` and `behind` both positive |
| `remote-ahead` | `behind` positive |
| `unpushed` | `ahead` positive |
| `merged-removable` | merged and not current |
| `merged-current` | merged and current |
| `pushed-unmerged` | otherwise |

The ladder is a pure function of the row (OQ-28). The partial-removal note is
added after it by a separate function (D4): a present, registration-verified,
`dirty` linked worktree whose status records read are all tracked-file
deletions (`" D"`), judged on the records read when the stream stopped at its
bound. It changes no class, rung or gate. Its text names its check first,
`Probable partial removal: check that git -C PATH status --short --ignored
lists only deleted files, then git worktree remove --force PATH by hand.`, and
for a locked row `Probable partial removal: check that git -C PATH status
--short --ignored lists only deleted files, unlock it, then git worktree remove
--force PATH by hand.`, because a status stream stopped at its record bound
leaves untracked and modified files unread, and an ignored record leaves the
flag alone, so that `--force` could delete either (Brett Heap's Q4 (a) and (b),
ruled on 2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; lane
2's wave 22 triage T4, sr-removal F3 and F4; writer's `c6daebc`); no detection
rule changes. The recommendation is the ladder's too, but in three cases
`row_evidence()` replaces it after the ladder has run
(lane 3's W52 F-6 and F-10; writer E's `02aa71d`, merged as `d764c26`; lead
ruling R-259): the main worktree's row, where the ladder says
`merged-removable` or `merged-current`, takes `The main worktree is never
removed by project clean.`, since no removal of it can succeed, and a locked
`stale-worktree` row takes `Review, unlock it, then prune stale worktree
metadata manually; git worktree prune also deletes the entry, and so the HEAD
reflog, of every other worktree whose path is missing, one moved or on an
unmounted drive included, so run git worktree prune --dry-run first and remount
or repair any it lists that still exists.`, since `git worktree prune` keeps a
locked entry, and any other `stale-worktree` row takes `Review and prune stale
worktree metadata manually; git worktree prune also deletes the entry, and so
the HEAD reflog, of every other worktree whose path is missing, one moved or on
an unmounted drive included, so run git worktree prune --dry-run first and
remount or repair any it lists that still exists.`, since `git worktree prune`
acts on the whole repository (Brett Heap's Q3 (b), ruled on
2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; writer's
`da5502d`: both end with the dry-run warning, where the baseline's texts ended
after `manually`; `classify()` still returns the baseline's `Review and prune
stale worktree metadata manually.`). The class is unchanged in all three. Where
any row of the plan is unread (`unread_paths(plan)`),
`stale_recommendations()`, which `build_plan()` calls
once every row is gated, replaces each `stale-worktree` row's recommendation
by `Review and prune stale worktree metadata manually; a row's path could not
be read, so do not run git worktree prune, git worktree remove or git gc until
it can.` (`recommendation_stale_worktree_unread`) or, locked, `Review, unlock
it, then prune stale worktree metadata manually; a row's path could not be
read, so do not run git worktree prune, git worktree remove or git gc until it
can.` (`recommendation_stale_locked_unread`), from what planning recorded and
nothing read again (R-320; lane 3's W86 NM-1; ruled by Brett Heap, "R-320:
yes", lead R-321). `status` reads no plan, and `stale_recommendations()` does
not set its text: its `repo_state()` keeps the baseline's `Review the stale
worktree metadata before pruning it manually.` for every stale entry, a locked
one included, so that it still omits unlocking for a locked entry, a known
residual left to a follow-on change (lane 3's W65 LOW-3; lead ruling R-269;
contracts/project-clean.md, "`status`, `doctor` and `update`"), except that
where any row of the listing it reads has a path that could not be read
(`path_unread(row)`: `present` null) each stale entry's recommendation is
`Review the stale worktree metadata before pruning it manually; a row's path
could not be read, so do not run git worktree prune, git worktree remove or
git gc until it can.` (T9; ruled by Brett Heap on 2026-10-23, "Yes, add T9
(Recommended)"; lead R-365; writer's `7a20789`, merged as `d8724e2`).

### Gate (FR-020 to FR-023; D10, D12, D13)

A row is selected only when it passes every gate; every excluded row
carries one `reason`, its first failing gate, never null. A row left
unprobed, whose reflog read did not finish, the filesystem budget or the work
deadline having cut it (T066's read, the unprobed marker's only setter), is
excluded as `reflog-unavailable` with its classification kept and its marker
set, and the plan is incomplete with `inspection-incomplete` where the budget
cut the read, and with `deadline-exceeded`, not `inspection-incomplete`, where
the deadline did; no reason value and no group of its own are added for it
(lead ruling R-67 (a), withdrawing R-56's null reason for R-53's P-3; Brett
Heap's ruling "O-1: deadline-exceeded" of 2026-10-22, lead rulings R-263 and
R-278, which amends ratified text, the `project-clean` delta's `spec.md:606-608`
at `0050f3e`; #19 at `b3228bb`, `spec.md:713-718`; writer G's `99848dd`, merged
as `3bc1d68`):

| Order | Reason | Fails when |
| --- | --- | --- |
| 1 | `main-worktree` | the row is the main worktree |
| 2 | `unsupported-path-bytes` | the path is not valid UTF-8 |
| 3 | `registration-mismatch` | the two-way registration was read and disagrees (`registered is False`), its `commondir` and, where row 4c is not false, its effective work tree included (LQ-11); a row whose registration was never read, a `present: false` one among them, passes and is excluded at gate 5 by its class (lead ruling R-53 P-16); or, in `clean`'s plan alone (`for_clean`; lead R-409), the row's path is, or holds, the common directory, the main worktree or another row's path (`enclosing_rows()`; Brett Heap's Q2 (1), ruled on 2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; writer's `5eeaedd`), the row then unprobed and `inspection-error`, as a shared path is; or, in `clean`'s plan alone, the row's registered path is a symbolic link (`_read_row()`, from its `lstat`; Brett Heap's Q9 (b), ruled on 2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; lane 2's wave 22 triage T12, sr-removal F7; writer's `338edb0`), which reads its registration as disagreeing, the row again unprobed and `inspection-error`; a row whose path is, holds or shares another row's is in a group of its own, first, with `next_step_registration_mismatch_holds` (Brett Heap's M3 (a), lead R-413; "Branch evidence" above) |
| 4 | `locked-worktree` | `locked` is true |
| 5 | the classification | the class is not `merged-removable` |
| 6 | `not-requested` | single mode, an eligible row other than P |
| 7 | `unstarted-branch` or `reflog-unavailable` | the reflog rule below |
| 8 | `deferred-target-cap` | beyond the first 16 rows that passed gates 1 to 7 |
| 9 | `contains-submodule` | a gitlink in the row's index, or `modules` in its admin directory, or an entry of any type named `.git` in a directory of the worktree that holds an index entry, found by an `lstat` (`nested_git_check()`; Brett Heap's Q2 (2), ruled on 2026-10-23T13:30:27Z, "yes, recommended for Q1-Q9"; lead R-380; writer's `5eeaedd`), which revalidation's step 7 makes again (below) |
| 10 | `hidden-local-state` | an index entry flagged assume-unchanged or skip-worktree |
| 11 | `operation-in-progress` | an entry of any kind named by one of the eleven markers in the row's administrative directory, `<common_dir>/worktrees/<admin_id>`: `MERGE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `BISECT_LOG`, `BISECT_START`, `rebase-apply`, `rebase-merge`, `sequencer`, `MERGE_AUTOSTASH`, `NOTES_MERGE_PARTIAL` and `NOTES_MERGE_REF` (`NOTES_MERGE_WORKTREE`, which a notes merge leaves behind, is none) |
| 12 | `worktree-only-commits` | a commit that only the row's own HEAD reflog or `refs/worktree/` holds: the reachability probe prints an object, or the row's `logs/HEAD` was read to its 64 KiB bound or holds a line that cannot be parsed |

Gates 9 and 10 read the row's own index, inside its worktree, and gate 11
lists its administrative directory, one filesystem call (`os.listdir`,
OPERATION `listdir`) within the filesystem budget and no Git child, only for
rows that passed gates 1 to 8; at most 16 rows reach them. Gate 9 also makes
one filesystem call of its own, OPERATION `lstat`, in the same budget and with
no Git child: an `lstat` of `<dir>/.git` for each directory of gate 10's index
listing that holds an entry, in byte order, which `HiddenStateParser` collects
as `directories` (Q2 (2)). Git's directory walk skips every entry named `.git`
and recurses into a tracked directory without asking whether it holds a
repository, so a nested repository shows in no status record and passes Git's
own check; it is found here, and a `.git` entry beside a flagged entry still
names `contains-submodule`, gate 9 coming first. Revalidation's step 7 makes the
same `lstat`s again over the directories of its own fresh listing (below). Gate
12 runs only
for a row that passed gate 11, so that a row with an operation in progress
spawns no child for it. It reads `logs/HEAD` in the row's administrative
directory by one filesystem call (OPERATION `read`, at most 64 KiB, as gate 7
reads the branch's reflog), every non-zero object it names a candidate, a
missing or empty file naming none; then it runs one Git child in the
worktree, the reachability probe, `rev-list --max-count=1
--glob=refs/worktree CANDIDATES --not --branches --tags --remotes
NEGATIVES`, the negatives the non-zero objects that the branch's reflog named
when gate 7 read it, so that the commits an amended and reset branch's own
reflog still holds are not counted (design D21). A `logs/HEAD` read to its
bound or holding a line that cannot be parsed is `worktree-only-commits` with
no child; a probe that prints an object is `worktree-only-commits`, and one
that prints nothing passes. A row a gate after the cap excludes keeps its
place among the 16. Gate 11 is Brett Heap's ruling LQ-14 (design D22; draft
PR #19 at `43f7107` and `1ebdd90`; lead rulings R-102, R-124, R-126 and
R-180), built by lane G at `2405880` and merged as `e0c589a`; gate 12 is his
ruling LQ-13 (design D21; draft PR #19 at `93de4bb` and `2b86a5f`; lead
rulings R-102, R-124 and R-146), built by writer G at `8ae0bb5` and merged as
`93a3ae9`.

A gate whose own read cannot finish decides nothing: a reflog read error
other than `ENOENT` or `ENOTDIR`, a failed or timed-out `modules` read,
hidden-state probe, nested `.git` lstat or gate 11 listing, or gate 12's
`logs/HEAD` read failing other than with `ENOENT` or `ENOTDIR` or its
reachability probe failing (as on an object the repository does not hold, exit
128) or timing out, makes the row `inspection-error`
(classification and `reason`), its `errors` naming `os-error`,
`probe-failed`, `probe-timeout` or `deadline-exceeded`, and the plan
incomplete (`inspection-incomplete`, or `deadline-exceeded` where only the
deadline cut it); only a marker present gives `operation-in-progress`, and an
administrative directory that cannot be listed is `inspection-error`, not
`operation-in-progress` (lead ruling R-124 (b)), and only a decided result
gives `worktree-only-commits`; a null flag never passes gate 9, 10, 11 or 12,
while gate 3 fails only on a
registration read and found to disagree (R-53 P-16). A reflog read not
finished, the filesystem budget or the work deadline having cut it, follows
the `project-clean` delta's reflog outcome rule instead: the row is left
unprobed, its marker set and its class kept, and excluded as
`reflog-unavailable`, "where the reflog cannot decide it", never selected; the
read's row error, `probe-timeout` or `deadline-exceeded`, is the row's one
error, and the plan is incomplete with `inspection-incomplete` for the first
and with `deadline-exceeded` for the second, whose refusal names no repair (R-67
(a) and R-278). Gate 7 is the only gate whose deadline cut leaves a row
unprobed: every other gate's read that the deadline cuts makes the row
`inspection-error` with that `deadline-exceeded` error.

### Reflog anchor and movement (D10; FR-021, FR-022)

Read from `logs/refs/heads/<branch>` under `common_dir`, at most 64 KiB, by a
filesystem call (never a Git child). The read asks for no more than 65,536
bytes and needs no `fstat`: a read that returns 65,536 bytes has reached the
bound, and one that returns 65,535 is decided by its entries (lead ruling
R-33). Each line is `<old> <new> <identity> <time> <zone>`, then a tab and a
message when there is one.

- Anchor: the last surviving entry whose old object is all zeros, or whose
  message begins `branch: Created from` or `branch: Reset to`.
- Movement: an entry after the anchor, or any entry when no anchor survives,
  whose old and new objects are non-zero and differ (a rename's are equal).

| Outcome | When (first that holds) |
| --- | --- |
| `reflog-unavailable` | missing (`ENOENT`, `ENOTDIR`), 0 bytes, or the read reached its 64 KiB bound (65,536 bytes read) |
| `inspection-error` | any other error on the read |
| `reflog-unavailable`, the row left unprobed (its marker set, its class kept, `probe-timeout` in its `errors` and the plan `inspection-incomplete` where the filesystem budget cut the read, `deadline-exceeded` in its `errors` and the plan `deadline-exceeded`, with no repair remedy, where the work deadline did; R-67 (a), R-73 (c), R-278) | the read did not finish |
| `reflog-unavailable` | a line that is not `<old> <new> ...`, a truncated last line included: the entries cannot decide, never `inspection-error` (lead ruling R-53 P-22) |
| `reflog-unavailable` | the last entry's new object is not the head |
| pass | a movement survives |
| `unstarted-branch` | an anchor survives with no movement after it, its new object the head |
| `reflog-unavailable` | anything else, no anchor and no movement included |

### Plan (FR-003, FR-019, FR-024, FR-025, FR-031, FR-032; D12 to D14)

What one invocation would do in one repository. Built fresh by every run,
from the resolution's evidence: `resolve_clean_target()` returns `root` and
`evidence`, `inspect_repository()`'s dict, and `build_plan()` reuses that
evidence, so that row 3 runs once, where the argument resolves (contract,
"Git children"). A caller that passes no evidence gets that read and its
check as before, and the baseline's `Cannot inspect Git repository at ROOT`
remains only for such a caller (lead rulings R-71 (b) and R-72 (g)).

| Mode | Spelled | Row cap | Selection |
| --- | --- | --- | --- |
| `report` | every other invocation without `--all-safe`: plain `project clean`, with or without `--json`, and flags without `--apply` | 256 | what `--all-safe` would select at 128 rows or fewer; null above 128, with the note `inspect-cap` and `rows` |
| `all-safe` | `--all-safe`, preview or `--apply` | 128 | every row passing every gate, at most 16 |
| `single` | `--apply --action remove --worktree P` | 128, P exempt, its row and gates first, unless a realpath read fails (below) | P alone |
| `single`, push and delete-branch | `--apply --action push` or `--action delete-branch`, which take single mode's cap and bounds only (below) | 128, no exemption | the named branch; completeness the batch's |

`clean_mode(args)` (T035) decides the mode as this table spells it: `single`
for `--apply` with any `--action` (lead rulings R-49 and R-57).

The row cap counts the registry entries that become rows, the main worktree
and missing rows included: a bare repository's `bare` entry, and a first
record equal to `common_dir` with no main worktree named, are no rows (D8),
so neither counts (lead ruling R-73 (d), a fill of the delta's "every
registry entry counting"). In mode single, when the realpath of P or of any
other entry cannot be read, P's match is undecided: no entry is exempt from
the cap, a fill of FR-013 and of the delta's `spec.md:262-263`, which
presumes a P that is a known entry; the rows inspected are the main worktree
and the 127 linked worktrees with the smallest paths, as the delta's
scenario "Row cap and planning failures" takes them, and the plan refuses
with `inspection-incomplete` (lead rulings R-73 (d), R-74 (a), R-78 (b) and
R-91 LOW F).

Fields, in the delta's envelope order: `schema_version`, `observed_at`,
`mode`, the baseline `root`, `target_branch` and `tracking_freshness`,
`worktrees`, the identity (`repository`), the merge target, `limits`,
`budget`, `probes`, `operations`, `selected`, `excluded`, `omitted`
(`{count, exactness: "exact"}`), `notes`, `completeness`, `apply_allowed`,
`refusals` and `plan_digest` (R12 in research.md).
`probes` counts every Git child other than a removal and `operations` the
removals, each child once (lead ruling R-27; research.md R8). `probes.estimated`
adds, for each selected target, the children of one revalidation (6, or 7
where row 4c read true) and, once, those of the final rescan (3), and counts 3
more of each where the path of the repository's root or of its common
directory, as the plan read them, holds a line feed, since the identity probe
is then read one option per child (9, or 10, and 6; "Revalidation step and
`probes_performed`", below; lane 5's RI-3; #19's round (h) at `b3228bb`;
writer G's `c26e44b`, merged as `7164d7f`). Rows are ordered
main worktree first, then by raw path bytes; `selected`, `excluded` and the
execution order are by raw path bytes.

Completeness: a plan is `incomplete` when the row cap is exceeded
(`inspect-cap`), a repository-wide probe failed, a row is
`inspection-error`, or, in mode single, P matches several entries or its
match is undecided, any entry's realpath unread among the causes
(`inspection-incomplete`; lead rulings R-67 (b), R-73 (d), R-75 (b) and
R-78 (b)), or the deadline passed while planning (`deadline-exceeded`), each
row it stopped being `inspection-error` with a `deadline-exceeded` row error,
or, where it cut gate 7's reflog read alone, left unprobed with that error and
excluded as `reflog-unavailable` (lead rulings R-67 (a), R-69 and R-278;
T099); either way the plan is `deadline-exceeded` and not
`inspection-incomplete`. In single mode
those three are non-blocking notes about other rows, and only P's own row,
P's match and the repository-wide probes decide (D13; lane 3's L-7). P's
row is established first there, its status probe then its gates, before any
other row is inspected, which is how D13's "inspects P's row first:
identity, status probe, gates" is built, a fill of FR-013's "probed first":
a work deadline reached among the other rows leaves P's row decided and the
plan complete (lead ruling R-93 (d)), while one that cuts a read of P's own
row refuses `deadline-exceeded`, as a one-item batch's plan is refused, where
P's row is one the deadline stopped, and `inspection-incomplete` where it left
P's match undecided (lead ruling R-283; writer G's `a038961`). When P's match
is undecided, none of
the three notes is recorded, since each says that rows "do not block" P
beside the plan's refusal of P, `inspection-incomplete`, which speaks alone;
a P that matches several entries is decided, so the notes stay (lead
rulings R-93 (e) and R-94 (b)). In report mode above 128 rows, the
`inspect-cap` note alone does not make it incomplete. `apply_allowed` is
false for every report and for any plan that is incomplete or carries a
refusal.

Push and delete-branch take single mode's 128-row cap and bounds only:
their completeness is the batch's, so any `inspection-error` row, the cap
or the deadline refuses them (`inspection-incomplete`, `inspect-cap`,
`deadline-exceeded`), exit 2, before and after confirmation (FR-010).

### Refusal (FR-043)

`{code, message, path?, path_valid_utf8?, reason?}`. `path_valid_utf8` is
present exactly when `path` is; `reason` only on `target-excluded`. The
nineteen codes and their phases are in the contract: the eighteen the delta
lists, and `relative-config-path` after `git-too-old`, Brett Heap's ruling
LQ-15 (draft PR #19; lead rulings R-102 and R-173). `invalid-arguments`,
`internal-error` and every resolve refusal print the extended error object;
every other code prints the plan envelope with `apply_allowed: false`
(contract, "Streams").

### Target result and reconciliation record (FR-034, FR-035; D19)

One per selected target, in canonical order: `path`, `path_valid_utf8`,
`branch`, `planned_sha`, `stage`, `reason`, `notes`, `command` (the planned
argument vector, present even when nothing ran), `exit_status`,
`probes_performed` and `reconciliation`.

`exit_status` is null unless a child was spawned and reaped, and is 128
plus the number of the signal that ended it, whoever sent it, as
`BA:1035-1039` (at `da33d92`) and `execute()` report it: 143 when SIGTERM
ends it, at the ceiling too, and 137 only for a child that outlives SIGTERM
until SIGKILL (lead ruling R-68 (b)).

`reconciliation` is an object on every `removed`, `refused`, `failed` or
`unknown` target and null on a `not-attempted` one:

| Field | Value |
| --- | --- |
| `registry_entry_present` | the registry still lists the planned path; true, false or null |
| `path_present` | `lstat` of the planned path succeeds; false only on `ENOENT` or `ENOTDIR`; null on any other error or a timeout |
| `branch_present`, `branch_sha` | from the ref listing |
| `reconciled` | true only when the three presence fields are non-null and `branch_sha` is non-null whenever `branch_present` is true |

The rescan first re-establishes the repository identity; where it differs,
every field is null and `reconciled` is false. A `refused` target's values
come from the revalidation that refused it, plus an `lstat` of the planned
path when that revalidation stopped before its own, run with the reserve's
budget, `min(5 s, reserve remaining)`, so that a difference found as the work
deadline passes still records the path's presence (`reserve_budget()`; lead
ruling R-101 (d), the apply review's F3); a field from a listing that did not
run is null (`BA:1163-1174` at `da33d92` shows a ref-listing
refusal with `path_present: true`). A spawned target's values come from the
rescan after the child is reaped. Target notes: `orphaned-directory` (entry
gone, path present) and `partially-removed` (a child killed at the ceiling,
or whose exit was not observed, left its entry or path). The
`partially-removed` note appears only when the rescan shows the entry or the
path remaining (the `project-clean` delta's `spec.md:922-925`), which is how
its `spec.md:253-256`, "otherwise `unknown` with the note
`partially-removed`", is read: a ceiling target whose rescan established
nothing is `unknown` with `removal-ceiling` and no note, failing safe (lead
ruling R-76 (c)).

Where the rescan shows the registry entry and the path both present, its last
read is one `lstat` of the target's `.git` (`git_file_presence()`; the
reserve's budget as for any rescan read, no Git child, so the rescan's three
Git children stand). The result is kept on the `Target` object as
`git_file_present` (true, false on `ENOENT` or `ENOTDIR`, or null where the
read was not made, failed, was cut at its budget or was abandoned by a second
SIGINT), with `git_file_read`, whether the read was made, false until the
rescan makes it, and in no record, so that no document carries either: the
reconciliation record, `notes` and the JSON result are unchanged. Only the
human partial-removal note of the result reads them
(`partial_removal_text()`), in this order. First, where `git_file_read` is
true and `git_file_present` is null, or where the reconciliation record's
`path_present` is null (the lstat of the target's own path failed other than
for absence, as where a directory above the target denies search, so that no
read was made), whatever the record shows of the entry (the read is made only
where the rescan shows the entry and the path present), `Probable partial
removal: inspect PATH by hand; its .git could not be read, so do not run git
worktree prune, git worktree remove or git gc until it can.`, since `git
worktree prune` deletes the admin directory of a live worktree whose `.git`
Git cannot stat (`EACCES`, for a worktree directory the process may not
search; #19's round (i) at `1a4785e`; lane 3's W73 M-1; lead ruling R-284,
which Brett Heap ruled "R-284: yes", R-290; writer G's `6a32d10`, merged as
`3bc1d68`; for the null path, lane 3's W90 M-1, lead ruling R-329, which
applies Brett Heap's R-284 as ruled; writer's `b96b335`, merged as `7149e08`).
Otherwise D18's `git worktree remove --force` form,
`partial_removal_note_ceiling`, which has no check first, since the target was
clean at its revalidation (Brett Heap's Q4, ruled on 2026-10-23T13:30:27Z,
"yes, recommended for Q1-Q9"; lead R-380; writer's `c6daebc`), where
`registry_entry_present` and `git_file_present` are both true, and `Probable
partial removal: inspect, then delete PATH and its administrative directory
ADMIN by hand.` (`partial_removal_note_prune`) for the rest, since Git refuses
`git worktree remove --force` once the `.git` file is gone ("validation
failed", as a kill part way through a removal usually leaves it) or the entry
is gone ("is not a working tree"); a value not established never shows both
present. ADMIN is `<common_dir>/worktrees/<admin_id>` in the command form
(`partial_removal_admin(target)`, from the plan's repository identity and the
target's row, both verified again at its revalidation, nothing read; `unknown`
for a plain dict, which carries neither). The note names no `git worktree
prune`, which acts on the whole repository with an expiry of now and deletes
the administrative directory, and with it the HEAD reflog, of every unlocked
entry whose path is missing, a worktree moved or on a drive not mounted among
them: the person deletes the path and its own directory by hand, after looking,
and no other worktree's entry is touched. So the note is the same in every mode
and beside any row of the plan, and `partial_removal_text(target)` takes the
target alone (Brett Heap's Q3 (a), ruled on 2026-10-23T13:30:27Z, "yes,
recommended for Q1-Q9"; lead R-380; writer's `da5502d`). It supersedes R-365's
form, `partial_removal_note_prune_unread`, `Probable partial removal: inspect,
then delete PATH by hand; a row's path could not be read, so do not run git
worktree prune, git worktree remove or git gc until it can.`, which
`partial_removal_text(target, plan_unread)` chose where
`bool(unread_paths(plan))`, which `print_result()` passed, was true (`present`
null, a deadline-stopped row included); that key and its selection are gone
from `project`, and R-365's record stands as superseded.
`partial_removal_note_ceiling`, which has the text that `partial_removal_note`
had until Q4, and `partial_removal_note_unread` never changed, since `git
worktree remove --force PATH` acts on PATH alone and the second already advises
no prune (lead R-365, ruled by Brett Heap on 2026-10-23, "Yes, warn
(Recommended)"; writer's `7a20789`, merged as `d8724e2`). A report row's note
is `partial_removal_note`, whose check comes first (D4, above), its `.git` file
and entry being present (lane 3's W52 F-1; Brett Heap's ruling "F-1:
prune-then-delete" of 2026-10-22, lead ruling R-263, which amends ratified
text, the `project-clean` delta's `spec.md:253-256` and `:922-926` at
`0050f3e`; #19 at `b3228bb`; writer G's `3eb2e9c`, merged as `7164d7f`).

### Revalidation step and `probes_performed` (D7; FR-046, FR-047)

Each target's revalidation runs these steps in order and stops at the first
difference, which refuses the target, spawns nothing and attempts no later
target:

| Step | Read by | A difference gives |
| --- | --- | --- |
| 1. the identity probe (row 3 at `root`), then the realpaths of the toplevel and the common directory and the common directory's lstat | Git child, then filesystem | `identity-changed` (a decided different identity, or a path the reads find absent, `ENOENT` or `ENOTDIR`); `state-changed` (a probe that decides nothing, the lead's R-195, or a read that fails otherwise or runs past its own budget, R-208) |
| 2. the manifest re-read | filesystem | `state-changed` (manifest or merge target); a `tracking_branch` that is not a string, YAML's `.nan` among them, reads as none on both sides, as planning reads it (`as_candidate()`; lead ruling R-101 (d), the apply review's F2) |
| 3. the registry listing | Git child | `identity-changed` (a checked row's path missing or listed twice); `state-changed` (lock, or a listing that decides nothing; R-195) |
| 4. the narrowed ref listing | Git child | `branch-changed` (branch name or head); `state-changed` (upstream, `upstream_oid`, `ahead`, `behind`, merge target, or a listing that decides nothing) |
| 5. the target's identity and registration (its `commondir` included), a twin of a checked row, the `modules` check and gate 11's listing of its administrative directory, by filesystem reads; then, where row 4c read true, its effective work tree, so that a filesystem check that refuses spares the probe's child (the lead's R-198; writer G's `963fccf`) | filesystem, then one Git child for the work tree | `identity-changed` (the identity or registration decided different; the target's path, its `.git` or its administrative directory found absent, `ENOENT` or `ENOTDIR`, the listing that finds no administrative directory included, writer G's reading of a gap in #19 at `9267303`, lead ruling R-220; or another present entry of the fresh registry listing sharing a checked row's realpath or admin id, `registry_twin()`, R-81 (a)); `contains-submodule` (a `modules` entry); `operation-in-progress` (a marker, LQ-14); `state-changed` for a read that fails other than with `ENOENT` or `ENOTDIR` or runs past its own budget: the target's lstat, its registration reads (a `.git` that cannot be read among them), a registry entry's lstat or realpath in the twin check, unless the plan read its lstat as failed too, null and null again (R-95 (c)), the `modules` check and the listing (the lead's R-208; lead rulings R-124 and R-127); for the work-tree probe, `identity-changed` only for a work tree the probe decides is not the target's path, its output read as one path (R-287), and `state-changed` for one that fails, runs past its own budget or prints output that is empty, a line feed alone or without a closing line feed (LQ-11; the lead's R-171 and R-287) |
| 6. the combined status probe in the target, which must print nothing | Git child | `state-changed` (a record, or a probe that decides nothing) |
| 7. the hidden-state probe, which lists the target's index again, and then the nested `.git` lstats of Q2 (2) over the directories of that listing that hold an index entry | Git child, then filesystem | `contains-submodule` (a gitlink, or an entry named `.git`, made after the plan, in a directory that holds an index entry); `hidden-local-state` (a flagged entry); `state-changed` (a probe that decides nothing, R-195, or an lstat that fails other than with `ENOENT` or `ENOTDIR` or runs past its own budget); `deadline-exceeded` (an lstat that the work deadline cuts, the target and every later one `not-attempted`) |
| 8. gate 12's check in the target: `logs/HEAD` read again and the reachability probe run again, the negatives the plan's, taken as they were | filesystem, then one Git child | `worktree-only-commits` (an object printed, or a `logs/HEAD` read to its bound or holding a line that cannot be parsed); `state-changed` (a read that fails or times out, or a probe that decides nothing; LQ-13, lead rulings R-124 and R-127) |

Step 7 runs Q2 (2)'s nested `.git` check again, as #19's round (r) (at
`4512441`; lane 3's W133 MEDIUM-2; the lead's R-391 and R-395) words
it in the `project-clean-review-safety` delta, as it stands at `54e869b` after
round (s): the hidden-state probe, "with the `lstat` of `<dir>/.git` for every
directory that its listing shows holding an index entry directly or below it,
other than the worktree's own top level" (`spec.md:112-114`).
`hidden_state_probe()` runs gate 10's listing
again, the step's one Git child, and then `nested_git_check()` makes one
`fs_call()` of those `lstat`s, counted in the filesystem budget, so that a
`.git` entry made after the plan, which neither step 6's status probe nor Git's
own check reports, refuses the target as `contains-submodule`, the reason
that delta gives "for a new gitlink, `modules` entry or `.git` entry"
(`:133-134`; its scenario "A nested repository made after the plan"), and the
nested repository remains. The `lstat`s are filesystem calls only, no Git
child, so the bounds of six, seven, nine and ten children below stand; one
that fails or runs past its budget is `state-changed`, and one that the work
deadline cuts is `deadline-exceeded`, by the rule below. The loop is one `_fs()`
call (`project:5557` at `c0841aa`), under `min(5 s, the work remaining)`;
measured warm (Python 3.12.3, Git 2.43.0) at 1,000, 10,000 and 50,000 tracked
directories, planning stays eligible at `41759a4` as at `e702a65`, adding about
0.25 s at 50,000 (medians of 11 runs, 2.216 s and 2.461 s); cold-cache cost and
deep nesting are unmeasured, and both fail closed, `inspection-error` at
planning and `state-changed` at revalidation (lead R-398 and R-406).

At most six Git children (steps 1, 3, 4, 6, 7 and 8), as T084 built them and
LQ-13 added step 8's probe (lead ruling R-75 (i)), and seven where row 4c read
`extensions.worktreeConfig` as true, step 5's work-tree probe added (LQ-11;
lane E's report), `LIMITS["revalidation_children"]` and
`LIMITS["revalidation_children_worktree_config"]` (lead ruling R-165); where a
filesystem check of step 5 refuses first, the work-tree probe does not run
(R-198); the identity probe counted once: a line feed in the root's or the
common directory's path makes step 1 read row 3 again, one child per option, as
design D6 allows for "the rare repeat" (`design.md:298-302`), so that a
revalidation then runs up to 9 children, 10 with the work-tree probe, and the
final rescan up to 6, a fill of the `project-clean` delta's bound (its
`spec.md:825-826`; lead ruling R-82 (c), lane 3's LOW-4). The plan's
`probes.estimated` counts those 3 extra children for each revalidation and 3
for the final rescan (`identity_split_children()`, `revalidation_children()`
and `rescan_children()`), so that it equals `probes.performed` on such a path,
as #19's round (h) requires of it (its `spec.md:1050-1056` at `b3228bb`; lane
5's RI-3, lead ruling R-259; writer G's `c26e44b`, merged as `7164d7f`); it
fell three short for each target and three for the rescan before. A value
null in the plan and null again is no difference; a value that cannot be
re-read is a difference. One rule decides every read of these steps that does
not finish with a value: a Git child that fails, runs past its own budget while
the deadline is not the limit, or, as the work-tree probe can, prints output
that names no path (empty, a line feed alone or without a closing line feed;
R-287), and a filesystem call that fails other than with `ENOENT` or
`ENOTDIR`, or runs past its own budget while the deadline is not the limit,
gives `state-changed`, whatever its step, and a read gives its step's own
reason only for a value it decided (the lead's R-171, R-195, R-198 and R-208;
draft PR #19 at `4485678`, `2e819ad` and `9267303`; writer G's `73d8888`,
merged as `9ab996e`). The filesystem calls are step 1's identity reads, step
5's lstat of the target, its registration reads, the twin check's reads, the
`modules` check and the listing, step 7's nested `.git` lstats (one `fs_call()`
over its fresh listing's directories, counted in the filesystem budget), and
step 8's read of `logs/HEAD`; the `modules` check that fails gave
`contains-submodule` and the others `identity-changed` before R-208. `ENOENT` or
`ENOTDIR` decides that the path is absent, which keeps the step's reason,
`identity-changed` for an absent target, `.git` or administrative directory;
step 8's missing `logs/HEAD` names no candidate. A read the work deadline cut is
none: `revalidate()` returns its distinct `deadline-exceeded`, and that target
and every later one are `not-attempted` with that reason and no reconciliation
(T099; lead ruling R-80 P-2), `registry_twin()` giving it too when the deadline
cut one of its reads, so that no twin goes unread for want of time. A signal in
the slot before a read starts is no difference either: `revalidate()` returns
`interrupted`, its own return beside the deadline's, and that target and every
later one are `not-attempted` with `interrupted` and no reconciliation (T093;
lead ruling R-95 (a)). The first target's revalidation is the preflight of
every selected target: its steps 3 and 4 and its filesystem reads compare every
selected target's registration, `locked` and filesystem identity, branch tip
and upstream object, beside the merge-target SHA, and a difference on any
target refuses the first target with that step's reason, nothing removed and
later targets `not-attempted` with `batch-stopped`; step 5's `modules` check,
listing and work-tree probe, and steps 6 to 8 (the target's ignored-file state,
classification and worktree-only commits among them) read the target alone, in
its own revalidation (research.md R16, lead ruling R-41; lane 3's W32 L2).
After target k's removal child is reaped, its rescan runs steps 1 to 4 again,
as built: the identity probe, the manifest re-read, the registry listing and
row 6's full ref listing (`refs/heads refs/remotes`), three Git children and a
file read. The full listing is a superset of step 4's narrowed one, which is
how design D7's "its rescan runs the same three" (`design.md:374`) is read
(lead rulings R-77 (a) and R-82 (a); lane 3's LOW-3). When k ends as a plain
`removed` they are target k+1's steps 1 to 4, and otherwise, or after the last
spawned target, they are the final rescan.

`probes_performed` counts the Git children of that target's revalidation,
the three it shares with the previous target's rescan included: at most 6,
or 7 where row 4c read true, 3 more where a line feed repeats the identity
probe, fewer when it stopped at a difference, and 0 when it was never
revalidated.
The record's `probes.performed` is the plan's count plus each target's
`probes_performed` plus the final rescan, which is 3 (6 where a line feed
repeats the identity probe) when the rescan after the last spawned target
counted toward no later target and 0 otherwise (`BA:816-830` and
`BA:1039-1042` at `da33d92`); the plan's `probes.estimated` counts those
extra children (above).

### Apply result record (FR-044)

`schema_version`, `observed_at`, `repository`, `merge_target`,
`plan_digest`, `probes`, `operations`, `targets`, `exit_code`,
`completeness` (complete when every target whose `reconciliation` is an
object has `reconciled: true`).

### Residual window (D7; FR-048)

Ignored files created, index flags set, operations started and commits
made that only the target's HEAD reflog or `refs/worktree/` holds, after the
last revalidation, and any change after Git's own check. Stated in one line
(D18) in the confirmation and in the result: `Not protected: ignored files
created, index flags set, operations started or worktree-only commits made
after the last check, and any change after Git's own check.` The third item
is LQ-14's and the fourth LQ-13's (`TEXT["residual_window_line"]` at
`93a3ae9`).

### Root and leg state outside `clean` (D16; FR-050 to FR-052)

Each root, leg and nested member keeps its baseline dict. A directory with no
`.git` is `present: false` with no Git child. A present one that cannot be
inspected (an old, missing or unusable Git, a configuration path that fails
D11's test, a failed or timed-out status probe) adds `classification:
"inspection-error"` and `errors` (`git-too-old`, `git-unavailable`,
`relative-config-path`, `probe-failed`, `probe-timeout` or `os-error`), with
`present` null when the version check failed or the configuration-path test
stood in its place (LQ-15) and every value not established
null, `worktrees` among them; an inspected dict has neither field (lead
ruling R-56). A `git-too-old` or
`git-unavailable` entry carries the contract's command-neutral message, never
`clean`'s refusal text (lead ruling R-48). Every `path` gains
`path_valid_utf8`, every `root` gains `root_valid_utf8`, and
`ignored_samples` entries are objects. A deleted upstream shows its short
name with `ahead` and `behind` null. `ignored_files` is the evidence model's
bounded count, capped at 64 (`ignored_entries`), so 64 means "64 or more";
no key is added for it (lead ruling R-66 (d)). The version check runs once
per invocation, memoized, when a repository is inspected; doctor's `git` row
runs it itself when none was, and `status` never runs it for nothing (lead
ruling R-56). `handoff()` runs its `git remote get-url origin` only for a
root whose repository was inspected, present and past the version check;
otherwise it returns the same no-identity state with no child (lead ruling
R-66 (c)). Under a `HOME` that fails D11's test, `~`, `~/x` and `~user`
among them, `project` reads nothing under it and expands no `~` path against
it: `handoff()` reads no workspace configuration and takes a `~` workspace
path as not configured, doctor's credential presence checks read no file
under it, the default projects directories and the workBenches root and
marker are not taken from it, and a `~` target refuses with
`relative-config-path` (`home_directory()`, `expand_user()`; lead rulings
R-202 and R-205; lane H's `22f95d1`). A stale entry's `recommendation` there
is the baseline's text, except that where any row of the listing has a null
`present` it ends with the warning against `git worktree prune`
("Classification" above; T9, lead R-365).

### Child handle (D2; lead ruling R-30, research.md R14)

One spawned Git child other than the push child. It records its kind (`probe`,
read-only with `GIT_OPTIONAL_LOCKS=0`; `removal`; or `delegate`, the
`git branch -d` child), its process ID, which is also its process group ID, its
start time, its budget end (none for a removal or delegate handle), a removal's
300 s ceiling, its kill and reap deadlines once set, and the first 4 KiB of its
standard error. Termination never blocks: `terminate_group()` sends SIGTERM,
sets the kill deadline and returns at once, and the handle's `advance(now)`,
called by the driver loop on every tick, takes it on:

| State | Entered when | Leaves |
| --- | --- | --- |
| `running` | `start()` spawned and registered it | to `reaped` when its streams end and `Popen.poll()` returns a status; to `terminating` when its budget passes, its parser reaches a bound, the slot is read set while planning, a `finally` cleanup runs, or, for a removal, its ceiling passes |
| `terminating` | SIGTERM went to its group; kill deadline = now + grace | to `killing` at the kill deadline, or at once when its leader has exited |
| `killing` | SIGKILL went to its group, sweeping any member left; reap deadline = now + reap wait | to `reaped` when `Popen.poll()` returns a status; to `abandoned` at the reap deadline |
| `reaped` | its status was observed | final; it leaves the registry |
| `abandoned` | the reap deadline passed | final; `probe-timeout` recorded; never waited on again; it stays registered, so its group is killed again on exit |

The driver calls `advance()` on every `terminating` and `killing` handle on
each tick, and the selector's timeout counts their deadlines, so no handle's
grace delays another's. The grace and the reap wait (2 s each in the real
table) are read from `TIMING` when each step starts, never passed as an
argument. A `finally` cleanup moves every live probe handle to `terminating` at
once and ticks until each is `reaped` or `abandoned`, at most grace plus reap
wait (4 s) however many handles run. A removal handle reaches `terminating`
only at its ceiling, a delegate handle never, and the signal slot moves
neither.

### Driver outcome (D2)

`run_bounded()` returns one outcome per probe handle, with the parser's
result, the exit status and the standard-error head:

| Outcome | When | Row error |
| --- | --- | --- |
| `complete` | the child exited 0 and its streams ended | none |
| `complete-at-bound` | its parser reached its bound and the handle was terminated | none; never `probe-failed` |
| `failed` | it exited nonzero or by a signal, could not be spawned, or its parser's `finish()` raised `ParseError` (a truncated last record, or a record not in its format) | `probe-failed` |
| `timeout` | its budget passed | `probe-timeout` |
| `deadline` | the work deadline was the limit | `deadline-exceeded` |
| `interrupted` | the slot was read set while planning | none: D1's `Interrupted` is raised |

A handle abandoned at its reap deadline records `probe-timeout` (D2). The
version check maps any outcome but `complete`, and an unparseable
version, to `git-unavailable`.

### Invocation (D1; lead ruling R-44)

The per-run state of one `main()` call, a context manager in region `runner`
that `main()` enters fresh for every call: the per-child budget (5 s under
`clean`, 15 s otherwise), the clock (the work deadline and the reserve,
paused while a question waits), the probe and removal counters, the
per-invocation memos (the version check's result, the common-directory
evidence), and the phase: `planning` by default, then `apply` once the apply
phase begins, then `reconciling`. Outside any scope, `current_invocation()`
returns a fresh default: the 15 s budget and no signal handler. Its shell,
`Invocation(command=None)` with the phase and the signal slot, is T023's,
since the slot records with the phase; its budget, clock, counters and memos
are T024's (lead ruling R-47). A `signal_scope` entered with no `Invocation`
in force enters a default one for its own span, so that its handler and the
driver read one slot (R-47). So a direct `clean()` call, which only tests
make, runs on that scope's own default `Invocation`, whose command is None:
15 s per Git child and no 60 s deadline (lead ruling R-63 (e)).

### Signal slot (D1, D15)

The driver reads the slot by the `Invocation`'s phase: it raises
`Interrupted` only in `planning`, or on a second SIGINT in `reconciling`
(lead ruling R-44).

| Event | Effect |
| --- | --- |
| the first SIGINT, SIGTERM or SIGHUP | the handler stores its number and does nothing else; it decides the exit status (130, 143, 129) |
| a later signal | the slot keeps the first; a later SIGINT counts only in phase `reconciling` |
| the slot read set in phase `planning` (after each wake of the driver) | the child is terminated and `Interrupted` raised: cancelled |
| the slot read set at a seam of phase `apply` (before each revalidation and each spawn, and before each read a revalidation starts) | that target and every later one `not-attempted` with `interrupted`; reconciling follows |
| a second SIGINT while a rescan runs in phase `reconciling` | the remaining rescans are abandoned: the running group is terminated and fields not established stay null (the `project-clean` delta's `spec.md:936-937`); the target's stage is then the stage rule's on that unfinished record: after exit 0, `unknown` with `reconciliation-incomplete`, but a child that exited nonzero on its own stays `failed`, `git-refused` or `git-failed`, and one killed at the ceiling keeps `removal-ceiling` (its `spec.md:899-902` and `:910-914`; lead rulings R-87 (c) and R-91 LOW D) |
| `raising_signals` entered with the slot already set | it raises at once, `KeyboardInterrupt` for SIGINT and `Terminated` for SIGTERM or SIGHUP, so no signal falls between reading the slot and installing its handlers (lead ruling R-47) |
| `default_signals` entered | the handlers in force before the outermost scope was entered are restored for its span (R-47) |
| a signal while a removal, push or `git branch -d` child runs | recorded only; the child is never signalled and is waited for |

Design D15 places the seams "before each revalidation and before each spawn"
(`design.md:660-661`), and the `project-clean` delta says the first signal
stops scheduling "so that no further probe or removal starts" (its
`spec.md:931-933`). Phase `apply` stops no child by itself, so the build
reads the slot before each read a revalidation starts too (`slot_set()`): the
Git children of its steps 1, 3, 4, 6, 7 and 8, the manifest re-read, and step
5's identity, twin and `modules` reads, its listing and its work-tree probe.
A signal gives `interrupted` and no
later read starts; a step that has already read is decided first, so a
difference it found stands. D15 stays as written and this is the reading of
it (lead ruling R-95 (a), lane 3's LOW-1; T093's
`test_clean_a_signal_during_a_removal_sigint_during_a_revalidation`).

A signal the caller ignored on entry (`SIG_IGN`, as under `nohup` or in a
shell's `&` job) stays ignored in every scope, as the baseline left it: no
handler is installed for it, so it never reaches the slot, and FR-036 does
not reach a signal the caller ignored (lead ruling R-101 (b), the runner
review's F2; lane O's `0e93044`). A test suite run as a `&` job therefore
fails wherever a test sends SIGINT to `project`, unless the module resets
SIGINT in its children, as the revalidation, timing, push and apply modules
now do; a foreground run and CI are unaffected (lane O's report).

## States of a `project clean` run

| State | Meaning |
| --- | --- |
| resolving | arguments checked, the configuration paths tested, `git --version` run, the argument resolved, the merge target found |
| planning | rows inspected under the deadline, caps and budgets; gates applied |
| reported | a preview or report printed; the run ends |
| asking | the removal question is on the human stream (`--apply` without `--yes`) |
| applying | the apply phase: per target, revalidate, spawn, wait, rescan |
| reconciling | the final rescan within the reserve; the record printed |
| refused | a refusal; nothing mutated, exit 2 |
| cancelled | a signal before the apply phase, or end of input at the question |

### Transitions

| From | Event | To |
| --- | --- | --- |
| (start) | invalid argument combination; parser usage error | refused (exit 2; a usage error prints no JSON) |
| resolving | a configuration path that fails D11's test (`relative-config-path`, before any Git child); Git missing, unusable or older than 2.36; a resolve refusal | refused |
| resolving | resolved | planning |
| resolving to asking | unexpected exception | refused (`internal-error`) |
| planning | preview or report built | reported (exit 0 complete, 1 incomplete) |
| planning, `--apply` | incomplete; then `--expect-plan` mismatch | refused (exit 2), in that order |
| planning, `--apply` | complete `all-safe` plan selecting nothing | reported (`No eligible worktrees`, exit 0, no question) |
| planning, single | P matches no entry; P matches several, or one not decided (R-67 (b), R-69); a gate excludes P | refused (`worktree-not-found`; `inspection-incomplete`; `target-excluded`) |
| planning, `--apply` | standard input not a terminal, no `--yes` | refused (`confirmation-required`) |
| planning, `--apply` | `--yes` | applying |
| planning, `--apply` | otherwise | asking |
| asking | `yes` | applying |
| asking | any other answer | refused (`cancelled`) |
| asking | end of input, SIGINT, SIGTERM, SIGHUP | cancelled (130, 130, 143, 129) |
| resolving, planning | SIGINT, SIGTERM, SIGHUP | cancelled (130, 143, 129; probe groups killed and reaped) |
| reported | SIGINT, SIGTERM, SIGHUP recorded while the plan is written | cancelled (130, 143, 129; the slot read before the run exits, research.md R4) |
| applying | a target ends a plain `removed` and another follows | applying (next target) |
| applying | a target ends otherwise, the last target ends, a signal or the deadline | reconciling |
| applying, reconciling | an unexpected exception | reconciling (an in-flight removal waited for; that target `unknown` with `internal-error`, later ones `not-attempted`; research.md R6) |
| reconciling | record printed | exit by the table below |

The `Invocation`'s phase follows these states. The pipeline sets `apply`
after the confirmation and the slot read (lead ruling R-56 Q-1 and Q-2);
then `reconciling` is set before every rescan, and `apply` again before
the next target's own steps when the target ended a plain `removed` and the
slot is empty, so that each rescan child gets
`min(5 s, reserve remaining)` and a second SIGINT counts during every
rescan, a fail-safe reading; the reserve counted from the exit stays
T099's (lead rulings R-83 P-3 and R-80 P-3; T093).

### States of push and delete-branch

| From | Event | To |
| --- | --- | --- |
| (start), resolving | an argument check; a resolve refusal | refused (exit 2) |
| resolving | resolved | planning: the full inspection under single mode's row cap and bounds, with the batch's completeness |
| planning | incomplete; `remote-gone` (push); a baseline refusal | refused (exit 2, no delegate) |
| planning | accepted | confirming: `Cleanup action:` and the plan printed, then `confirm()` with the process's own handlers and the clock paused |
| confirming | `yes` or `--yes` | re-inspecting: the full re-inspection |
| confirming | another answer; no terminal and no `--yes`; Ctrl-C or end of input | refused (`confirm()`'s baseline messages, exit 2); cancelled (130) |
| re-inspecting | incomplete, or the state changed | refused (exit 2, no delegate) |
| re-inspecting | unchanged, and the slot read just before the spawn is empty | delegating: the push child through `execute()`, or the `git branch -d` handle through the driver; unbounded, never signalled, waited for |
| re-inspecting | the slot read just before the spawn is set | cancelled (`Cancelled.`; 130, 143 or 129; no child run; lane 3's N13, lead ruling R-177) |
| delegating | the child exits | exit: with a signal recorded, `Interrupted; the push had started and was waited for, and git exited with status N.` (`the branch deletion` for delete-branch) on standard error, never `Cancelled.`, and 130, 143 or 129, the phase being `apply` once the child is reaped (lead rulings R-101 (e) and R-108 (a)); otherwise the child's status |
| resolving, planning, re-inspecting | SIGINT, SIGTERM, SIGHUP | cancelled (130, 143, 129; probe groups killed and reaped) |

### Target stages

`pending` leads to exactly one final stage. It is never printed: the plan
lists the selected rows, and each target's one progress line prints at its
final stage (lead ruling R-56 Q-10).

| Stage | Reasons |
| --- | --- |
| `removed` | null, `branch-advanced-after-removal`, `branch-missing-after-removal`, `removal-ceiling` |
| `refused` | `identity-changed`, `branch-changed`, `state-changed`, `contains-submodule`, `hidden-local-state`, `operation-in-progress` (LQ-14), `worktree-only-commits` (LQ-13) |
| `failed` | `git-refused` (128), `git-failed` (any other status), `spawn-error` |
| `unknown` | `unconfirmed-removal`, `reconciliation-incomplete`, `internal-error`, `removal-ceiling` |
| `not-attempted` | `batch-stopped`, `interrupted`, `deadline-exceeded` |

A child that exits nonzero on its own is `failed`, signal or not; only a
child killed at the 300 s ceiling, or whose exit was not observed, is decided
by the rescan between `removed` and `unknown`. No target is retried.

A spawned target is `removed` only when the rescan shows its registry entry
and its path both gone and `reconciled` is true (FR-034; the
`project-clean` delta's `spec.md:891-895`; lane 3's L-5). A rescan read
that fails or is cut marks the record: the identity probe, while the
planned root and common directory are still there by `lstat`, the registry
listing, the ref listing or the `lstat` of the planned path. After exit 0,
a marked record, or one whose entry and path are gone with `reconciled`
false, is `unknown` with `reconciliation-incomplete` (its
`spec.md:1012-1018`; `BA:518-526` at `da33d92`); an unmarked unreconciled
record is `unknown` with `unconfirmed-removal`, reached only when every
read succeeded and showed the removal not done (its `spec.md:966-970`), or
when the identity was found lost or different (the
`project-clean-review-safety` delta's `spec.md:215-217`); a child killed at
the ceiling, or whose exit was not observed, keeps `removal-ceiling`. The
mark is the record's class, `UnfinishedRescan`, a `dict` subclass, so that
equality and every document are unchanged (lead ruling R-78 (e), second
amendment; T085).

Three overlaps of the delta's rules are decided this way, as built (lead
ruling R-82 (a), lane 3's LOW-6):

- Exit 0, nothing removed, and a rescan read that fails: `unknown` with
  `reconciliation-incomplete`, by the mark, where `BA:520-521` (at
  `da33d92`) reads "exit 0 without that evidence is `unknown` with
  `unconfirmed-removal`"; the delta's `spec.md:966-970` speaks only of
  reads that succeed, and the stage and exit status, `unknown` and 1, are
  the same either way.
- A ceiling child whose repository the rescan finds replaced: `unknown`
  with `removal-ceiling`, every field null and no note. The
  `project-clean-review-safety` delta's `spec.md:215-217` gives a replaced
  repository `unconfirmed-removal`, and the `project-clean` delta's
  `spec.md:253-256` gives the ceiling `removal-ceiling` "in both cases";
  the build takes the second (R-78 (e)), exit 1 either way.
- A ceiling child whose branch also moved or was deleted:
  `removal-ceiling` covers it, the target `removed` when its entry and path
  are gone and reconciled, so `branch-advanced-after-removal` and
  `branch-missing-after-removal` do not show, one reason per target (the
  `project-clean` delta's `spec.md:889-895`), and the run exits 1, where a
  branch reason alone would give 2 (D19, its 1 row first); the record's
  `branch_present` and `branch_sha` still show the branch.

Later targets take `interrupted` after a signal, `deadline-exceeded` when
the floor stopped the run or a revalidation read was cut at the work
deadline, and `batch-stopped` after a target that ended otherwise, a rescan
cut at the reserve's end included (lead ruling R-93 (e), lane 3's LOW-6).

## Exit statuses

A run with `--apply`, first matching row (FR-037, D19):

| Exit | When |
| --- | --- |
| 130, 143, 129 | a signal was received, the first deciding; 130 when input ended at the question |
| 1 | the deadline stopped work after the apply phase began, any target is `unknown`, or any reason is `removal-ceiling` |
| Git's own status | a target is `failed` with `git-refused` or `git-failed`, passed through even when it equals one of `project`'s own |
| 2 | any refusal; a `refused` target; `removed` with a branch-after-removal reason; `failed` with `spawn-error` |
| 0 | every selected target `removed` with reason null, or nothing eligible |

A preview or report: 2 only for a refusal raised before a plan is built, 1 for
an incomplete plan, 0 otherwise, and 130, 143 or 129 when a signal ends it;
a write that fails after its plan is built is `internal-error`, exit 2, by
the delta's rule for an unexpected exception before the apply phase, which
conflicts with the preview rule above (research.md R4; lead rulings R-55 and
R-59; LQ-7).
A signal recorded while the push or `git branch -d` child runs is not
passed on: `project` never signals either child and waits for it. The run
then exits by D19's first row: 130, 143 or 129 when a signal was recorded,
otherwise the child's status (128 plus the signal number for a signal
death); a refusal exits 2. `status` keeps 0; `doctor` exits 1 on an `error`
check row, its rule unchanged; `update --apply --component shape` or
`bench` exits 2 when any `dirty` is not exactly false.

## Constants

| Name | Value |
| --- | --- |
| Git floor | 2.36 |
| deadline, reserve, work deadline | 60 s, 10 s, 50 s (time at the question not counted) |
| per Git child, per filesystem call | `min(5 s, work remaining)`; rescans `min(5 s, reserve remaining)` |
| per Git child in `status`, `doctor`, `update` | 15 s; no deadline, no row cap |
| per filesystem call in `status`, `doctor`, `update` | 15 s |
| grace, reap wait | 2 s, 2 s |
| removal floor, ceiling | 5 s of work deadline left; 300 s after spawn |
| row caps | 128 (`all-safe`, `single`), 256 (`report`) |
| targets per run | 16 |
| `ignored_entries`, `status_records`, `ignored_samples` | 64, 4,096, 8 |
| reflog read, manifest read | 64 KiB, 1 MiB |
| revalidation, final rescan | at most 6 and 3 Git children, 7 for revalidation where row 4c read true (LQ-11, LQ-13); 9 (10) and 6 when a line feed repeats the identity probe (D6), which `probes.estimated` counts (lane 5's RI-3; #19's round (h)) |

The timing values live in one module-level table, `TIMING`, read at call
time only, never captured in a default argument or a derived constant
(research.md R10, lead ruling R-29); `budget` and `limits` report the values
in force.
