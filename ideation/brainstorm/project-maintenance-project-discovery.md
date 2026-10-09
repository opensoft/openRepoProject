# Project Overview and Attention — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Discover local projects in bounded canonical order and report their Git health, work to preserve, and safe housekeeping in a versioned overview that keeps partial results visible.
Topics: project-maintenance, overview-discovery, project-command, project-doctor-repository-health
Repository context: opensoft/openRepoProject; local discovery and reporting using existing owner tools.
Captured: 2026-09-11

## Possible feats

- A bounded local project overview with an attention filter, linked-worktree grouping, partial-result reporting, and a shared JSON representation.

## Focus and baseline

The current CLI inspects a selected project. The proposed MVP answers
“Which of my local projects needs attention?” across explicitly configured
roots. This is exploratory design, not a specification: every command, flag,
and output in this document is illustrative and proposed. The contracts
(types, enums, units, exit codes, and orderings) are nevertheless written
precisely so that a later proposal can adopt or reject each one deliberately.

This revision, made on 2026-10-07, resolves the overview-side findings of the
2026-09-11 [fix handoff](next-session-project-maintenance-fix-handoff.md):
bounded and shared probes (finding 3), the overview JSON and repository
handoff contract (finding 4), and discovery scope and acceptance (finding 5).

The design contract baseline is `a040790`. `origin/main` is now `7a9134b`, which
merged PR #13 (lane openRepoProject-1's archive of the
`prefer-triad-in-project-new` OpenSpec change, `openspec/` only) after `d7f6b0e`
merged PR #8 (feature 002, "offer the Triad first in `project new`") on
2026-10-08. Before them, `da33d92` merged PR #7 (this packet) on 2026-10-07,
PR #4 archived the completed OpenSpec changes and promoted their specs to
`openspec/specs/`, and PR #5 (merged 2026-10-07T10:02Z) added the
`prefer-triad-in-project-new` OpenSpec proposal under `openspec/changes/`. PR #8
added about 141 lines to `project`, in the project-creation code between
`choose()` and the end of `new()`, and 1,163 lines to `tests/test_project.py`;
the cleanup, status, doctor, and update paths are unchanged in content but sit
about 141 lines lower, so every `project` line citation stays pinned at
`a040790`, whose `project` is byte-identical through `da33d92`. The later
`cleanup` branch (PR #2, closed unmerged on 2026-10-07; branch retained on
origin at `bb91a49`) adds behavior in `5fc2b51`, `acf0133`, `80fdef3`,
`1789ad9`, `09af8c8`, and `bb91a49`; those commits are extension evidence and
are not assumed by the overview MVP. The old `12db36a` review-closure commit is
not a health or cache implementation anchor.

The overview reuses these baseline helpers and names: `projects_dirs` for the
default roots, `manifest` for manifest reads, the `default_branch` resolution
order, and the classification ladder inside `cleanup_report`; `repo_state`
and `cleanup_report` move onto the shared probes described below. The
overview mirrors `discover`'s marker and family-holder rules
(`<dir>/<dir name>/family.yaml`) but never calls `discover`, whose uncounted
`rev-parse --show-toplevel` child would escape the deadline and the probe
count, and it never calls `snapshot`, which recursively follows family
members and project legs. Two baseline behaviors shape the path rules below:
`repo_state` parses newline-delimited `git worktree list --porcelain` and
`git status` output, and the `probe` helper decodes Git output as text. A
scratch check on 2026-10-07 (Git 2.43) confirmed the consequences: a worktree
whose path contains a newline is misread as a truncated path and classified
`stale-worktree`, and a worktree path containing the byte `0xFF` makes
`project clean --json` stop with an uncaught `UnicodeDecodeError` (exit 1, not
the refusal exit 2).

## User interface

```sh
project overview
project overview --root ../projects
project overview --attention
project overview --json
project overview --strict
```

Proposed default: `overview` shows every discovered local project;
`--attention` filters the display of the same collected result to the repair,
preserve, and housekeeping categories defined below. Repeatable `--root`
arguments replace the `projects_dirs()` defaults (`PROJECTS_DIR`, or
`~/projects` and `~/Projects`). Avoid a second persistent registry.

`project attention` and `project overview --remote` remain possible later
interfaces. They are not MVP requirements. If the alias is retained, it must
call the same collector and renderer; if remote inspection is added, it must
follow the remote boundary below.

Each row shows the project name and absolute canonical path, kind, local Git
health, worktree count, findings grouped by attention category, and a concrete
next command when one applies. Per-worktree detail is expanded only when it
explains a finding. Duplicate names stay unambiguous because every row prints
its absolute path.

Illustrative output, not a report of current repositories:

```text
atlas    /home/user/projects/atlas
  housekeeping  feature/export is merged; its worktree is removable
                /home/user/worktrees/atlas-export
  next          project clean /home/user/projects/atlas --all-safe
ledger   /home/user/projects/ledger
  repair        manifest-invalid: unexpected kind in project.yaml
odd      $'/home/user/projects/odd\u000aname'
  preserve      dirty: uncommitted changes in the checkout
Incomplete: /home/user/archive could not be read (root-unreadable).
3 projects; 2 errors; preserve 1, housekeeping 1, informational 2.
```

## Discovery scope and ordering

### Roots

Roots come from repeatable `--root` (source `argument`), otherwise from
`PROJECTS_DIR` (source `environment`), otherwise from `~/projects` and
`~/Projects` (source `default`), exactly as `projects_dirs()` selects them.
Each root is expanded, canonicalised with `realpath`, deduplicated by realpath
and by `(st_dev, st_ino)` (so `~/projects` and `~/Projects` on a
case-insensitive filesystem count once), and sorted by the bytes of its
canonical path. At most 32 roots are listed; any further root is reported
with state `omitted`, and one `scan-limit` error reports the omitted count as
exact. A default root that does not exist is reported as `absent` without an
error. An argument or environment root that does not exist, is not a
directory, or cannot be listed is reported as `unreadable` with a
`root-unreadable` scan error; an unreadable root is never an exit 2.

### Candidates

Discovery examines each root itself and the root's immediate entries only; it
never recurses. Each root is listed in full with `os.scandir`, up to 4,096
entries per root, and every entry counts whatever its type. A root with more
entries is marked `truncated` and gets a `scan-limit` error for
`root_entries` whose omitted count is unknown. A symbolic-link entry is
resolved once with `realpath`; because discovery never recurses, a link cannot
cause traversal, and a link that resolves to a directory already seen is an
alias that adds nothing.

A canonical directory `D` is a candidate when filesystem checks (no Git
child) find a marker. The first matching row decides, mirroring the order in
which `discover` and `manifest` look, without calling either:

| Marker | Candidate path | Kind |
| --- | --- | --- |
| `D/<name of D>/family.yaml` is a file | `D/<name of D>`, the holder `discover` returns | `family-holder` |
| `D/project.yaml` is a file | `D` | `project-manifest` |
| `D/family.yaml` is a file | `D` | `family-holder` |
| `D/.git` exists as a file or directory | `D` | `single` |
| `D/.project.json` is a file or `D/.devcontainer` is a directory | `D` | `single` |

A directory with no marker is neither a candidate nor reported. The marker
checks for an entry directory `D` come from one `os.scandir` pass over `D`,
using each `DirEntry`'s type information rather than a `stat` per marker,
plus one `stat` of `D/<name of D>/family.yaml` only when `D` holds a
directory with its own name. `ENOENT` and `ENOTDIR` mean “no marker”. The
checks for one directory run inside that directory's part of the
per-candidate wrapper (see "Collector boundary and error isolation"). Any
other `OSError`, such as the `PermissionError` from listing a mode-000
directory, makes `D` an error row: `path` is the candidate path `D`, `name`
is its basename, `path_valid_utf8` follows the usual rule, `kind` is null,
`status` is `"error"`, `findings` is `[]`, `errors` holds one `os-error`
naming the path, and `repository`, `merge_target`, `git`, `worktrees`, and
`suggested_command` are null. That row is sorted by `path` and capped like
any other, and the scan continues.

### Ordering, truncation, and omitted counts

Every root is listed before any candidate is chosen. Candidate paths are then
canonicalised, deduplicated by realpath and by `(st_dev, st_ino)`, and sorted
by their bytes, and only then truncated to the first 128. Sorting before
truncation makes the selected set independent of directory-listing order,
except within a root whose listing was cut short. In a root truncated at 4,096
entries, which entries were read at all depends on that order; in a root cut
by the 5 s per-root listing bound, or by the deadline, the cut depends on
timing as well. Every cap that drops work reports
`omitted: {count, exactness}`:

| `exactness` | When | `count` |
| --- | --- | --- |
| `exact` | The whole population was enumerated within the same entry and time budget | integer: the number dropped |
| `lower-bound` | An enumeration that could add to the population stopped early: a truncated, unreadable, or deadline-cut root listing, or an unread worktree registry | integer: the number known to be dropped |
| `unknown` | The population itself was not enumerated, as with the per-root entry cap | `null` |

### Caps and their arithmetic

The caps are 32 roots, 128 candidate project directories, and 512 worktree
rows estate-wide (`limits.worktree_rows`), plus the 4,096-entry listing cap
per root. A worktree row is every entry of `git worktree list`, including
each main worktree, because each costs the same single status probe; batch
cleanup counts its cap in the same unit.

Both documents derive their caps at 150 ms per Git child, a 1.5× margin over
the 100 ms assumption that the proposal must measure, as the largest values
whose worst case fits. Batch cleanup's fit test additionally requires its
last removal to be spawned with `removal_floor_seconds` left, as its "Cap
arithmetic" section states; the overview spawns no removal and so has no
floor. The overview's caps are candidates and worktree rows, each a power
of two. Its worst case runs four children at once across repositories, keeps
the earlier ratio of four worktree rows per candidate, and must fit the 60 s
deadline together with the listing phase. Listing time is bounded by the
deadline rather than by a fixed allowance. It is estimated, with a warm cache,
at about 6 s for 32 full roots of 4,096 entries on the reference machine; the
proposal must measure it, and that measurement must include a cold-cache pass.
The verification review's 5.9 s on WSL2 timed a different call pattern, five
`stat` calls per entry rather than one `os.scandir` pass per entry directory,
and is not a measurement of this design. At the warm estimate that leaves
about 54 s for Git work. Rendering is small at these caps and is not counted.

| Work at the caps | Units | Git children each | Children | Serial, 100 ms | Four at once, 100 ms | Four at once, 150 ms |
| --- | --- | --- | --- | --- | --- | --- |
| Git version check | 1 invocation | 1 | 1 | 0.1 s | 0.1 s (runs alone, first) | 0.15 s |
| Root listing and marker checks | 32 roots × 4,096 entries | 0 | 0 | about 6 s, estimated | about 6 s, estimated | about 6 s, estimated |
| Repository-wide set: identity, registry, ref listing, merged set | 128 candidates | 4 | 512 | 51.2 s | 12.8 s | 19.2 s |
| Worktree status probe | 512 worktree rows | 1 | 512 | 51.2 s | 12.8 s | 19.2 s |
| Every cap reached at once, Git work | | | 1,025 | 102.5 s | 25.7 s (257 serial-equivalent) | about 38.6 s |

At 150 ms the Git work at the caps needs 257 serial-equivalent children,
about 38.6 s; with the listing estimate that is about 44.6 s, which fits
60 s. Doubling either cap does not: 256 candidates with 512 rows, or 128
candidates with 1,024 rows, need 385 serial-equivalent children, about
57.8 s, or about 63.8 s with listing, and doubling both needs 513, about
77 s before listing. The 32-root cap is unchanged; roots cost no Git child,
and their listing is the estimated term. These caps
replace the earlier 256 candidates and 1,024 linked worktrees, which need
2,049 children under the same model: about 205 s serially at 100 ms, and
about 77 s even with four concurrent children at the margin rate, so they
fail the rule.

The caps fit only with that concurrency. With about 54 s left for Git work,
the break-even is about 53 ms per child serially (54 s ÷ 1,025) and about
210 ms with four children (54 s ÷ 257). The four-way figures assume work
from at least four repositories is ready at any time. One repository's
children always run serially, so a single repository with 512 worktree rows
needs 517 children (1 + 4 + 512): about 52 s at 100 ms, which fits with the
listing estimate, but about 78 s at the margin rate, which ends at the
deadline with an incomplete result. The
deadline remains the bound in every case: a cap hit or deadline expiry yields
an incomplete result and exit 1, never a silently shortened complete one. An
informal check on a three-worktree scratch repository measured medians of 3
to 10 ms per child and a 77 ms 95th percentile for `git status`; that is not
the proposal's measurement, which must use a realistic estate.

### Repositories and linked worktrees

Identity uses the packet's shared vocabulary. A repository is
`{root, common_dir, dev, ino}`. `root` is the canonical toplevel of the main
worktree and `common_dir` the canonical common directory, both printed by
`git rev-parse --path-format=absolute --show-toplevel --git-common-dir`. `dev`
and `ino` come from a no-follow `os.lstat` of `common_dir`. A path string alone
is never an identity. When a linked worktree is reached first, in canonical
candidate order, the first `git worktree list` entry names the main worktree; a
bare main entry leaves `root` null, which suppresses clean suggestions. When
that first record's path equals `common_dir`, the main checkout is a gitfile
checkout: `repository.root` is the realpath of `core.worktree`, else the
`--show-toplevel` of a candidate that is that checkout, else null with an
`unsupported-layout` repair finding and no suggestion, and that record is never
a status-probe row. Git 2.43 leaves `core.worktree` unset after
`git init --separate-git-dir`, so for such a checkout the second case applies,
the candidate toplevel whose `.git` file names `common_dir` (change 1's R11),
and when only linked worktrees of such a repository are candidates the third
applies, as `clean` refuses such a linked worktree with
`target-not-repository-root`. `clean` tests a submodule checkout first, by a
non-empty `git rev-parse --show-superproject-working-tree`, before
`core.worktree` and the candidate toplevel, and refuses it the same way (R11's
precedence, settled by lane openRepoProject-2's ruling of 2026-10-09). The
overview follows that precedence in every repository (lane openRepoProject-2
ruling R-2, 2026-10-09, change 2 at `996a181`), which moved the submodule test
into the identity probe, so the test adds no child: a submodule checkout gets
`repository.root: null` with an `unsupported-layout` error whose message is
"submodule checkout, which project clean refuses; review it yourself", and no
gate code, and `target-not-repository-root` covers only a bare repository, where
change 2 at `5094e4e` also gave it to a submodule checkout. A main-worktree path
that does not exist gives `repository.root: null` with a `main-worktree-missing`
repair finding, which replaces the `stale-worktree` finding on the main
worktree's row (change 2 phase 6 (5094e4e), lane openRepoProject-2, 2026-10-09),
and the repository-wide probes then run in the candidate.

A worktree is `{path, dev, ino, admin_id}`. `path` is canonical from
`git worktree list --porcelain -z`, and `dev` and `ino` come from
`os.lstat(path)`. `admin_id` is the `<id>` in the worktree's `.git` file
(`gitdir: <common_dir>/worktrees/<id>`), accepted only when
`<common_dir>/worktrees/<id>/gitdir` names `<path>/.git` in return. The main
worktree has `admin_id: null`. Registration is checked as batch cleanup
checks it: relative values resolve against the directory holding the file,
and both comparisons use realpaths. Where a bind mount gives two root
spellings for one `(dev, ino)`, the one first in canonical order wins.

Rows are keyed by repository identity. A linked worktree that is also an
immediate child of a root therefore merges into its repository's row, and
independent clones of one remote stay distinct. Every registered worktree is
listed, including paths outside every root, because the registry is the
source of truth for one repository. Each registered path falls into exactly
one of these cases:

| Case | `present` | Status probe | `classification` | Error or finding |
| --- | --- | --- | --- | --- |
| `lstat` fails with `ENOENT` or `ENOTDIR` | `false` | none | `stale-worktree`, from the ladder | housekeeping finding |
| `lstat` fails with any other `OSError`, such as `EACCES` | `null` | none | `inspection-error`, set directly | `os-error` in `errors[]` |
| Registration disagrees in either direction | `true` | none | `inspection-error`, set directly | `registration-mismatch` finding |
| Present and registered; the status probe fails, times out, or is cut by the deadline | `true` | ran | `inspection-error`, set directly | `probe-failed`, `probe-timeout`, or `deadline-exceeded` in `errors[]` |
| Present and registered; the status probe succeeds | `true` | ran | the ladder's result | per the attention table |

The three rows set directly bypass the ladder on purpose. The ladder would
read an unknown presence as `stale-worktree`, and it tests the merge-target
branch before cleanliness, so a mismatched row on that branch, or a
merge-target checkout whose status probe failed, would otherwise read
`protected-default`, as batch cleanup's identical rule avoids. A failed,
timed-out or deadline-cut status probe sets the row to `inspection-error`
directly, on the merge-target branch too, with that code's repair finding of
severity error. A
registration-mismatched worktree gets no status probe, because a `.git` file
that is missing or names another admin directory would make `git status`
fail or report another worktree's index. Its `admin_id`, `dirty`, and
`ignored_files` stay null, the `registration-mismatch` finding replaces the
classifier's `inspection-error` finding, and because the probe was skipped
deliberately rather than failed it adds no error and leaves completeness
unaffected. The overview runs no probe in a path it could not `lstat`, and it
never creates, prunes, repairs, locks, or unlocks a worktree.

### Family holders

A `family.yaml` holder is exactly one row of kind `family-holder`, counted
once in `summary.projects`. The overview reads the holder through `manifest()`
only for its name and kind check; it never reads the members list and never
visits declared siblings, pinned member copies, or mounted legs.
`relationships` is always `[]` in the MVP.

Probe ownership follows the directory. The holder receives Git probes only
when its own directory has a `.git` entry and the identity probe confirms that
directory is the toplevel; otherwise its `repository`, `merge_target`, `git`,
and `worktrees` are null, and it carries no error. A member directory that is
itself an immediate child of a configured root is an ordinary candidate with
its own row and its own probes; the holder neither claims it nor lends it
probes.

## Probe model and deadline

Every Git child runs as `git -C <dir> …` with the variables that
`git rev-parse --local-env-vars` lists removed from its environment, so
`-C <dir>` alone selects the repository; under an inherited `GIT_DIR`, every
identity probe would otherwise name the same repository. The list is
hard-coded, because obtaining it would cost a child:
`GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_CONFIG`, `GIT_CONFIG_PARAMETERS`,
`GIT_CONFIG_COUNT`, `GIT_OBJECT_DIRECTORY`, `GIT_DIR`, `GIT_WORK_TREE`,
`GIT_IMPLICIT_WORK_TREE`, `GIT_GRAFT_FILE`, `GIT_INDEX_FILE`,
`GIT_NO_REPLACE_OBJECTS`, `GIT_REPLACE_REF_BASE`, `GIT_PREFIX`,
`GIT_SHALLOW_FILE`, and `GIT_COMMON_DIR`, the fifteen that Git 2.40 and later
print. The list adds a sixteenth name, `GIT_INTERNAL_SUPER_PREFIX`, which Git
2.36 through 2.39 also print and which makes every command on those versions
fail when it is set, and all sixteen are unset unconditionally, as change 1
ruling R-21 (lane 2, 2026-10-09, `c873c81`) fixed the shared scrub. Every
overview child is a read-only probe, so each also runs with
`GIT_OPTIONAL_LOCKS=0`, as the baseline `probe` helper already sets, and
`status` never rewrites the index. Standard input is closed and output is
read as bytes. The overview uses local refs only: it never fetches, pulls,
resets, bootstraps, runs validators, writes files, or contacts the network.
Ahead, behind, and merge status are observations as of the last fetch, and
both outputs say so. It reads no credential files or unrelated profile data.
The memo is invocation-local; there is no persistent cache.

### Git version check

`git worktree list --porcelain -z` requires Git 2.36 or newer. The overview
runs one `git --version` child once per invocation, after the deadline is set
and before any root is listed, with the same `min(5, deadline - now)`
timeout; it is not part of the per-repository set. An older Git refuses
with code `git-too-old`, and a missing `git` executable, a failed or
timed-out `git --version`, or an unparseable version string refuses with
`git-unavailable`, the same codes batch cleanup uses. Either refusal comes
before any repository probe: exit 2 with a clear message, such as “project
overview needs Git 2.36 or newer; found 2.34.1”, printed under `--json` as
the baseline error object with the code added,
`{"error": "<message>", "code": "<code>"}`. It never becomes a `scan-limit`
or any other incompleteness.

### Repository-wide probes

These run once per repository, memoized by the `(dev, ino)` of its
`common_dir`, and fan out to every row and worktree of that repository. They
are the canonical list that batch cleanup also uses:

1. Identity:
   `git rev-parse --path-format=absolute --show-toplevel --git-common-dir`,
   run in the candidate, plus `lstat` of the common directory. It runs once
   per Git candidate because it is how the memo key is found; it is counted
   and deadline-bounded like every child, and a memo hit ends that
   candidate's own Git work. It answers the question `discover`'s
   `rev-parse --show-toplevel` would ask, without that call's uncounted 15 s
   timeout.
2. Registry: `git worktree list --porcelain -z`, which also yields `locked`
   and `prunable`.
3. Ref listing: one `git for-each-ref` over `refs/heads` and `refs/remotes`
   with the format below. `%(symref)` on `refs/remotes/origin/HEAD` gives the
   `origin/HEAD` target, printed as `refs/remotes/origin/<branch>`; the
   `refs/heads` rows say which merge-target
   candidates exist and give the merge-target SHA and every branch's head;
   `%(upstream)`, `%(upstream:short)`, and `%(upstream:track,nobracket)` give
   each branch's upstream, its short form (such as `origin/main`), and its
   ahead and behind counts or `gone`; and the remote rows of the same
   snapshot give each upstream's object id and presence. It replaces
   `default_branch`'s `symbolic-ref` and per-candidate `show-ref --verify`
   calls, and the baseline's per-worktree `rev-parse --abbrev-ref
   @{upstream}`, `rev-list --left-right --count`, and `rev-parse --verify`
   calls.
4. Merged set: one `git for-each-ref --merged=<merge-target sha>
   --format=%(refname) refs/heads`, replacing one `merge-base --is-ancestor`
   per worktree. Querying by SHA keeps the merged set and `merge_target.sha`
   on the same commit.

The ref listing's format string, identical in both documents, separates
fields with NUL and ends each record in LF, which is safe because ref names
cannot contain control characters:

```text
%(refname)%00%(objectname)%00%(symref)%00%(upstream)%00%(upstream:short)%00%(upstream:track,nobracket)
```

The fixed repository-wide term is these four children. Batch cleanup's fixed
term is the same four plus the version check and its resolution children; the
version check is counted separately here, and both documents count the main
worktree's status probe as a worktree row. Merge-target resolution itself
spawns no child: the manifest read is a file read, and every candidate's
existence and SHA come from the ref listing.

### Worktree-specific probes

These run once per worktree row within the cap that is present and
registration-verified (see the table under "Repositories and linked
worktrees"), in row order. Every worktree-specific probe runs as
`git -C <worktree path>` against that worktree's own index, and only after
the row's identity (`dev`, `ino`, and admin registration) is verified: each
linked worktree has its own index, so the same probe run anywhere else would
read the wrong one. Repository-wide probes run as `git -C <repository.root>`
(`common_dir` for a bare repository), except the identity probe, which runs in
the candidate because that is how the repository is found. When a linked
worktree is reached first in canonical candidate order, the registry probe
also runs in the candidate, because the main worktree's path, and so
`repository.root`, comes from that listing; when the main worktree is missing,
the repository-wide probes run there too. Where `root` is null (a bare
repository, a missing main worktree, or a gitfile checkout whose main worktree
cannot be named), the repository-wide probes run in `common_dir` for a bare
repository and otherwise where the identity probe ran; `clean` refuses those
layouts and the overview reports them, so the shared evidence model carries the
rule and the overview records no departure (lane openRepoProject-2 ruling R-13,
R-13a in its messages, 2026-10-09; change 1 at `4f2162b`). Batch cleanup states
the same rule for a repository with a root.

1. Registration: `lstat` of the path and reads of its `.git` file and the
   matching `gitdir` file. These are filesystem reads, not children, and a
   mismatch skips the status probe.
2. Status: one streamed
   `git status --porcelain=v1 -z --untracked-files=normal --ignored=matching`,
   run with `-c core.untrackedCache=false -c core.fsmonitor=false`, gives
   both the dirty and the ignored state. The explicit
   `--untracked-files=normal` is required: without it, a user's
   `status.showUntrackedFiles=no` makes Git refuse the `--ignored`
   combination with “Unsupported combination of ignored and untracked-files
   arguments” (exit 128), which would turn every row into `inspection-error`.
   Git prints changed entries, then untracked (`??`) entries, then ignored
   (`!!`) entries; the 2026-10-07 scratch check confirmed that grouping, and
   the proposal must pin it with a test. A rename or copy record (`R` or `C`)
   carries a second NUL-terminated field, the original path, which the parser
   consumes as part of that record and never reads or counts as a record of
   its own. `dirty` is true as soon as any record is not `!!`, and false when
   the first `!!` record or the end of the stream arrives with none seen, so
   `dirty` is established even when reading stops early. Reading stops when a
   65th ignored record or a 4,097th record of any kind arrives, so a stream
   that ends within 64 ignored and 4,096 total records is complete.
   `ignored_files` keeps its baseline name and integer type but now means the
   number of ignored records read, a lower bound when
   `ignored_files_truncated` is true. A stream stopped before any ignored
   record was read leaves `ignored_files` null; `dirty` is then true, because
   every record read was a change or an untracked entry, so the ladder
   classifies the row `dirty`, never `inspection-error`. The first eight
   ignored paths, relative to the worktree, are kept as `ignored_samples`;
   the full list is never held in memory or emitted. Under lane
   openRepoProject-2 ruling R-9 (2026-10-09), a departure from the packet, each
   sample is an object `{path, path_valid_utf8}` in both changes.

That is one Git child per probed row, where the baseline spends two. Batch
cleanup uses the identical probe, so both documents cost a worktree row the
same way. A worktree's branch and head come from the registry; its upstream,
ahead, behind, upstream object id, and remote presence come from the ref
listing; `merged_into_target` comes from the merged set; and `current` keeps
its baseline meaning, the worktree that contains the overview process's
working directory.

### Scheduling and concurrency

At most four read-only Git children run at once (`probe_concurrency`, 4),
and never two once their `common_dir` is known to be the same. Parallelism
is across repositories only. Each repository's memoized probes
and fan-out therefore stay single-threaded, and no two children of one
invocation contend for one repository's lock files, which complements
`GIT_OPTIONAL_LOCKS=0`. The identity probe is the one child that runs before
its repository is known; it only reads and takes no lock, so identity probes
for two candidates that turn out to share a repository may overlap.

Scheduling has two phases so that, in a run in which no child, task, or
root listing reaches its budget and the deadline does not expire, the result
never depends on timing. In the first, repositories are dispatched in
canonical candidate order, and each runs its repository-wide probes
serially. A repository's rank is the canonical position of the first
candidate that reached it. In the second, worktree rows are ranked by
repository rank and then row order, the worktree cap selects the first 512,
and the selected rows' worktree-specific probes run, serially within each
repository. A repository's worktree probes may start as soon as every
repository ranked before it has finished its first phase, because the ranks
of its rows are then fixed, and, as a barrier added to that condition, only
after every candidate earlier in canonical order has finished its identity
probe, completed or failed, since only then is the repository's own rank
fixed; speculative first-phase dispatch stays allowed. Output order is
canonical whatever the completion order, and a run that a budget or the
deadline cuts reports each cut unit with `omitted` and the exactness of
"Ordering, truncation, and omitted counts".

### Deadline and timeouts

At start, before any root is listed, the overview sets
`deadline = time.monotonic() + 60` (`invocation_timeout_seconds`). Each child
gets a timeout of `min(5, deadline - now)` seconds (`probe_timeout_seconds`),
replacing the baseline `probe()` helper's fixed 15 s; when that value is not
positive, the child is not started. Children are started with
`subprocess.Popen(..., start_new_session=True)`, each in its own session and
so in its own process group, whose id is the child's pid, so a Ctrl-C at the
terminal reaches only `project`, whose SIGINT handler runs the termination
sequence. `start_new_session` works on Python 3.10, the project's floor,
where `process_group=0` needs 3.11; `preexec_fn` is never used, because it
is unsafe in a process with threads. The baseline `probe()` is not reused as
it is, because its `subprocess.run` sends SIGKILL to a single process on a
timeout. A child
that reaches its timeout, or whose stream the overview stops reading early,
receives SIGTERM to its process group, then SIGKILL if it has not exited
within 2 s; the reap then waits at most the same 2 s grace, after which the
child is abandoned and its row recorded `probe-timeout`. A deliberate early
stop at a record bound is a complete outcome that records nothing, never
`probe-failed`. Every exit path terminates the process groups the overview
started, and each child's standard error is drained and capped. On
deadline expiry or SIGINT the overview stops scheduling and terminates every
in-flight child together in the same way; on deadline expiry each is
recorded as a timeout (`deadline-exceeded`).

Filesystem work runs in daemon threads as coarse tasks, never one handoff
per call, and a task that does not return in time is abandoned. It never
runs on a `concurrent.futures` pool, because the interpreter joins a pool's
worker threads at exit, so an abandoned pool thread would block it. Every
filesystem call the overview makes, root canonicalization and deduplication,
marker and holder checks, and manifest reads included, runs in such a
bounded daemon task with `min(5, deadline - now)`, and the main thread never
blocks in an unbounded filesystem call.
Discovery is one task per root, holding its `os.scandir` listing
and the marker checks of every entry; root tasks run concurrently, and the
listing phase counts against the same monotonic deadline. Each root's task
is waited for with `min(5, deadline - now)`: a root still unfinished then
records a scan error, `deadline-exceeded` when the global deadline was the
smaller limit and otherwise `probe-timeout`, and counts as `truncated`, so
one unresponsive mount cannot hold every other root's candidates until the
deadline. During collection, each worktree row's `lstat` and registration
reads form one task with the same wait, and a task that does not return in
time records `probe-timeout` or `deadline-exceeded` for its row. The
overview then moves on. A call stuck in the
kernel on an unresponsive mount (NFS, sshfs, or a sleeping network share)
cannot be interrupted from user space: its daemon thread is abandoned, and
process exit itself can block until the call returns. A run therefore ends
within the deadline plus at most 4 s, the 2 s from SIGTERM to SIGKILL and
the 2 s reap grace, and the time to render, except while such a call is
stuck (change 2 phase 6 (5094e4e), lane openRepoProject-2, 2026-10-09).

A child stopped by the 5 s limit records `probe-timeout`; one stopped or
never started because the global deadline was the smaller limit records
`deadline-exceeded`. Either way the fields that probe would have established
stay null, the row's status becomes `error`, and the candidate's independent
probes continue while time remains. A failed identity, registry, or ref
listing probe leaves the probes that depend on it unrun.

Once the deadline passes, no further child starts. Each candidate whose
first phase never started is still emitted as a row carrying only filesystem
facts, status `error`, and a `deadline-exceeded` error; a row whose worktree
probes were not reached keeps its repository-wide evidence and gets the same
error. One `deadline-exceeded` scan error reports how many candidates were
not started: exact when discovery finished, otherwise a lower bound.

### Probe accounting

The envelope reports `probes: {estimated, performed}`, both integers.
`performed` counts every Git child started, including timed-out and stopped
ones; because the overview never calls `discover`, every identity probe is among
them. `estimated` applies the per-unit costs of the arithmetic table to the
units known when collection ended: 1 for the version check, 1 per Git candidate,
3 more per distinct repository whose identity was established (registry, ref
listing, merged set), 1 per worktree row within the cap that is present and
registration-verified, and, for a repository whose first registry record equals
its `common_dir`, 1 per Git child needed to name the main checkout. That is at
most one, the `core.worktree` read, beyond the identity probe, because lane
openRepoProject-2 ruling R-2 moved the submodule test into the identity probe
(change 2 at `996a181`, 2026-10-09), where change 2 phase 6 (5094e4e) counted at
most 2; the identity probe and the per-worktree status probes remain Git
children. It is a planning figure, not a promise, and it differs from
`performed` when collection stopped early.

## Collector boundary and error isolation

Collection is one wrapper per candidate, `collect(candidate) -> result`,
dispatched in canonical candidate order under the scheduling rules above.
The wrapper encloses every step for that candidate, in this order: the
marker checks for its directory entry, which run before sorting and capping
but inside the same boundary; the identity probe; `manifest()` at
`repository.root`, or at the candidate for a row without Git; the memoized
repository-wide probes; merge-target resolution in the `default_branch`
order; the registration checks and status probes of its worktree rows; and
the classification ladder from `cleanup_report`. Path candidates are never
passed to `discover`: the marker table already applies its rules, and the
identity probe asks its Git question within the deadline and the probe
count. The wrapper converts failures into data:

| Raised or observed while collecting one candidate | Error code |
| --- | --- |
| `Refused` from `manifest()`: an unreadable manifest (one that is not valid UTF-8 included), a malformed one, or one of the wrong kind | `manifest-invalid` |
| `Refused` from any other baseline helper the proposal reuses | `refused` |
| `OSError`, including `PermissionError` from a marker check | `os-error` |
| `UnicodeDecodeError` from a helper that still decodes text | `undecodable-output` |
| Any other `Exception`; the message names the exception class | `internal-error` |
| A Git child exits nonzero | `probe-failed` |
| A Git child or filesystem call reaches the 5 s limit | `probe-timeout` |
| The global deadline ends a child or call, or prevents its start | `deadline-exceeded` |

A manifest larger than 1 MiB by `st_size` is `manifest-invalid` too, before it
is read (lane openRepoProject-2 ruling R-4, 2026-10-09): the cap applies to the
merge-target manifest read in both commands (shared evidence model, change 1 at
`0669a20`). Every `manifest-invalid` is a row error, whichever case raised it,
and the overview exits 1 for it. The exit 2 that the `project-review-safety`
requirement "YAML decoding errors are structured refusals" sets for a manifest
that is not valid UTF-8 applies to `project clean` and the other commands that
refuse as a whole, not to an overview row.

An exception raised by a marker check or inside an existing helper stops
that candidate's remaining steps. The overview's own per-worktree filesystem
checks and Git children never raise: a failed `lstat` records `os-error`, a
failed or timed-out child or call records its code, and each nulls only the
fields it and its dependants would have established. Each error is
`{code, message, path?}`: `message` has at most 200 characters (for a failed
probe, the first line of Git's standard error), and `path` names the file or
directory involved. Evidence gathered before a failure is kept, and every
field not established stays null. A result whose `errors` is non-empty has
`status: "error"`; otherwise its status is `ok`. The wrapper never catches
`KeyboardInterrupt` or `SystemExit`.

A repository with no resolvable merge target is not an error, because the
absence is established. Its row gets `merge_target: null` and a
`no-merge-target` finding (category repair, severity error, no cleanup
suggestion). The classification ladder is not run, so `cleanup_report`'s
refusal never fires, and its worktree rows keep their probe evidence with
`classification: null`. If merge-target resolution could not run because the
ref listing failed or timed out, the row records that error instead of
`no-merge-target`, because absence was not established.

The guarantee is that every candidate entering collection yields exactly one
row or merges into exactly one existing repository row. A failure in one
candidate never removes, reorders, or changes another row or an earlier scan
error; collected rows are always rendered; and `completeness` and the exit
status report the failure. This is the overview's failure policy only: batch
cleanup stops at the first failed mutation and does not share this
catch-and-continue wrapper.

## Merge target and classification reuse

The merge target keeps the baseline `default_branch` order. The first
candidate name that is an existing local branch (`refs/heads/<name>`) in the
ref listing wins:

| Order | Candidate name | `source` |
| --- | --- | --- |
| 1 | the manifest's `tracking_branch` at `repository.root`, minus any `origin/` prefix | `manifest` |
| 2 | the `%(symref)` target of `refs/remotes/origin/HEAD`, printed as `refs/remotes/origin/<branch>`, minus `refs/remotes/origin/` | `origin-head` |
| 3 | `main` | `main` |
| 4 | `master` | `master` |

The row records `merge_target: {name, source, sha}`, where `sha` is that
branch's full object id from the same ref listing; resolution spawns no
child. The manifest is read at `repository.root` deliberately: that is the
directory the suggested clean command names, so both commands resolve the
target from the same manifest and refs.

Two cases are fixed. Conflicting: when the manifest and `origin/HEAD` name
different branches that both exist locally, the manifest wins, `source` is
`manifest`, and an informational `merge-target-conflict` finding names both
branches; it is the same code that batch cleanup carries as a plan note.
Missing: when no candidate name exists, the overview records the
`no-merge-target` finding described above, with severity error and no
cleanup suggestion, while batch cleanup refuses with exit 2 before any
mutation.

Overview, doctor, and clean share classifier meanings. Worktree
classification is `cleanup_report`'s ladder unchanged: the same names, the same
test order, and the same recommendation text, fed from the memoized evidence
instead of per-worktree probes, as a pure function over that evidence, except
that the proposals, by Brett Heap's ruling of 2026-10-09 (applied at `b772195`
and `cc43860`), test a deleted upstream for local ancestry before the
`remote-gone` rung. The ladder
runs on a worktree row only when the row is within the cap, its presence is
established, and the repository-wide probes it reads (registry, ref listing,
merged set) succeeded; otherwise `classification` is null, because the ladder
would read an unknown upstream as `unpublished`. Unreadable and
registration-mismatched rows, and rows whose status probe failed, timed out,
or was cut by the deadline, are the exceptions: all three are set to
`inspection-error` directly, as the table under "Repositories and linked
worktrees" shows, so none of them reads as `protected-default` on the
merge-target branch.

`review-required` stays in the ladder as a defensive branch, but under the
shared evidence model no Git state reaches it: `%(upstream:track)` always
yields ahead and behind counts for an upstream that exists, the merged set
always yields true or false, and a failed probe leaves `classification` null
instead of reaching the ladder. Acceptance therefore covers it with a
classifier test on an injected evidence row.

The packet keeps one evidence model: the proposal must move `repo_state` and
`cleanup_report` onto the same probes, so overview, doctor, and clean always
read the same evidence and overview and clean always produce the same
classification. The classification changes this causes are listed under
"Baseline behavior changes". Apart from them, a worktree's classification
must equal what `project clean <root> --json` reports at `a040790` from the
same working directory.

Doctor's existing checks keep their meanings. The ladder tests
`protected-default` before cleanliness, so a dirty default-branch checkout is
still classified `protected-default`; the overview additionally emits a
`dirty` preserve finding for it, matching doctor's “Uncommitted work; preserve
it before updates” warning. The overview never invents a parallel classifier.

## Attention categories

Every finding has exactly one category. This table is the complete MVP list
of finding codes; the classifier codes are exactly `cleanup_report`'s
classification names, and `<root>` is the absolute `repository.root`.

| Code | Category | Severity | Evidence source | Suggested command |
| --- | --- | --- | --- | --- |
| `inspection-error` | repair | error | `worktree-status` | none |
| `review-required` | repair | warning | `local-refs` | `project clean <root>` |
| `no-merge-target` | repair | error | `local-refs` | none |
| `registration-mismatch` | repair | warning | `worktree-registry` | none |
| `unsupported-path-bytes` | repair | warning | `filesystem` | none |
| `unsupported-layout` | repair | error (lane openRepoProject-2 ruling N-6, confirmed as P6-6, 2026-10-09; `warning` at change 2's `a8cef41`) | `worktree-registry` | none |
| `main-worktree-missing` | repair | warning | `worktree-registry` | none |
| `dirty` | preserve | warning | `worktree-status` | `project clean <root>` |
| `ignored-local-files` | preserve | warning | `worktree-status` | `project clean <root>` |
| `detached` | preserve | warning | `worktree-registry` | `project clean <root>` |
| `unpublished` | preserve | warning | `local-refs` | `project clean <root>` |
| `remote-gone` | preserve | warning | `local-refs` | `project clean <root>` |
| `diverged` | preserve | warning | `local-refs` | `project clean <root>` |
| `unpushed` | preserve | warning | `local-refs` | `project clean <root>` |
| `merged-removable` | housekeeping | info | `local-refs` | `project clean <root> --all-safe`, or `project clean <root>` under the repository gate |
| `stale-worktree` | housekeeping | warning | `worktree-registry` | `project clean <root>` |
| `pushed-unmerged` | informational | info | `local-refs` | none |
| `remote-ahead` | informational | info | `local-refs` | none |
| `merged-current` | informational | info | `local-refs` | none |
| `main-worktree` | informational | info | `worktree-registry` | none |
| `locked-worktree` | informational | info | `worktree-registry` | `project clean <root>` |
| `merge-target-conflict` | informational | info | `manifest` | none |

On a `protected-default` checkout, `dirty`, one of `diverged`, `unpushed`,
or `remote-ahead`, `unpublished`, and `remote-gone` apply with
`suggested_command: null`, as the paragraph on `protected-default` below
states.

A worktree the ladder classifies `merged-removable` yields the
`merged-removable` housekeeping finding, and with it the `--all-safe`
suggestion, only when it also passes batch cleanup's gates, checked in the
batch's order: it is not the main worktree, its path is valid UTF-8, its
registration agrees in both directions, and Git reports it unlocked. The
first failing gate's finding replaces the housekeeping finding:
`main-worktree` (informational, with no suggestion, because the main
checkout is never a target), `unsupported-path-bytes` (repair),
`registration-mismatch` (repair), or `locked-worktree` (informational,
suggesting the read-only `project clean <root>`). The row's `classification`
stays what the ladder computed. Independently of classification, a worktree
whose path is not valid UTF-8 always carries `unsupported-path-bytes`, and a
registration-mismatched one always carries `registration-mismatch`.

A fifth gate applies to the whole repository. When any of its worktree rows
is `inspection-error` (a failed status probe, an unreadable path, or a
registration-mismatched row), the batch plan for that repository would be
refused as `inspection-incomplete`, so the overview withholds every
`--all-safe` suggestion for it. The same applies when the repository has
more worktree rows than batch cleanup inspects (128 in its `--all-safe` plan; a
plan's `limits.worktree_rows` holds only its own mode's cap, so the overview
reads both caps, 128 for the batch and 256 for the report, from the shared
constants and reports them in its own `limits` as `batch_row_cap` and
`report_row_cap`, beside the batch's target limit of 16, named `targets` since
ruling R-14 (`target_limit` at `996a181`): lane openRepoProject-2 ruling R-7,
landed in change 2 at `996a181`, 2026-10-09), because that plan would be
incomplete with `inspect-cap`, and when
any of its worktree rows went unprobed, its classification null because the
512-row cap or the deadline cut it, because the batch plan for that
repository is then not known to be complete. Its `merged-removable`
housekeeping findings remain, but each suggests only the read-only
`project clean <root>`, and so does the row. Each such finding carries
`suggestion_gate`, beside its `suggested_command`, naming the code of the
gate that withheld `--all-safe`, and `suggestion_gate_rows`, the worktree-row
count behind an `inspect-cap` gate. A repository of 129 to 256 worktree rows
keeps the plain read-only `project clean <root>` suggestion, with
`suggestion_gate: "inspect-cap"` only on a `merged-removable` finding whose
`--all-safe` was withheld; over 256 rows, the plain report's own cap, every
read-only suggestion carries `inspect-cap`, because the report itself would
be incomplete. The gate changes suggestions only; it does not change how
completeness is computed, so a registration-mismatched row still leaves the
result complete. `target-cap` is a limiting gate, not a withholding one:
with more than 16 gate-passing `merged-removable` rows the `--all-safe`
suggestion stays and its findings carry `suggestion_gate: "target-cap"`,
whose message names the 16-target limit, says the preview is complete, and
says the batch takes 16 per run, so re-running drains the backlog.

Each `suggestion_gate` code has a fixed remedy, carried in the finding's message
and in the human `next` line as "(withheld: ...)" or "(limited: ...)", as change
2 states them (lane openRepoProject-2, 2026-10-09; read at `996a181`, and at
`4495ae7` (R-20; unchanged at `cc43860`)): `target-not-repository-root`, "run
project clean from the main worktree root"; `unsupported-path-bytes`, "rename
the path to valid UTF-8"; `inspection-incomplete`, "repair the inspection-error
rows, or re-run for the rows left unprobed, first", since lane openRepoProject-2
ruling R-16 (change 2 at `ef288fe`), where `996a181` read "repair the
inspection-error rows first"; `inspect-cap`, "N rows exceed the batch's row cap
of M; remove explicitly" or "N rows exceed the report's row cap of M; the report
would be incomplete", the two bands that `suggestion_gate_rows` tells apart,
with M read at run time from the shared constants (N-3) where the packet had
written 128 and 256 into the text; `scan-limit` or `deadline-exceeded`, "re-run
with --root <repository parent>", naming the repository's parent directory;
`unstarted-branch`, "no commit was made on this branch here since it was
created; review, then git worktree remove yourself"; `reflog-unavailable`, "the
branch's reflog is missing, expired or undecidable; review, then git worktree
remove yourself"; and `target-cap`, "limited to the batch's target limit of M
per run; re-run to drain the backlog". The `unstarted-branch` and
`reflog-unavailable` remedies take the form of change 1's D18 under lane
openRepoProject-2 rulings R-12 M6, R-14 M-B, and R-15 (2026-10-09), which
supersede R-10 and the earlier wordings of change 2 at `996a181`; change 1
carries the same wording since its R-15 commit, `9eeac52`. The code set, in the
order in which a finding records the first that applies, is
`target-not-repository-root`, `unsupported-path-bytes`, `inspection-incomplete`,
`inspect-cap`, `scan-limit`, `deadline-exceeded`, `unstarted-branch`,
`reflog-unavailable`, and `target-cap`; lane openRepoProject-2 ruling P6-5 added
`unstarted-branch`, and change 2 at `996a181` added `reflog-unavailable`.

Batch cleanup may still exclude a suggested worktree for reasons only its deeper
probes see. It runs bounded `git ls-files` checks in each selected target's own
worktree and one `lstat` in its admin directory, and excludes a target with
`hidden-local-state` (assume-unchanged or skip-worktree entries) or
`contains-submodule`, and it excludes as `unstarted-branch` a row whose branch
has no commit of its own. The overview applies that gate itself: an unstarted
worktree keeps its `merged-removable` finding but gets only the read-only
suggestion, with `suggestion_gate: "unstarted-branch"` and the unstarted remedy
above (lane openRepoProject-2 rulings N-5 and P6-5, 2026-10-09). Those rulings
decided it from the head alone, a head equal to the merge-target SHA, and left
the reflog-based part a residual exclusion that only the batch applied. The D10
amendment (landed in change 1 at `0b3c33d` and mirrored in change 2 at
`996a181`, lane openRepoProject-2, 2026-10-09) reads the branch's reflog in
every case, and ruling R-12 (2026-10-09; change 1 at `4f2162b`) states the test
as a movement after an anchor, as Batch "Eligibility and merge-target
terminology" records, so a head at the merge-target SHA with a movement recorded
is merged, the fast-forward case. Change 2 mirrors the read, from the creation
entry at `996a181` and, since its fix round at `fa9f0be`, from R-12's anchor
with ruling R-15's all-zeros anchor (R-13 (b), R-14, the R-12 mirror, and R-15),
a movement there being, as in change 1, an entry after the anchor, or any entry
when no anchor survives, "whose old and new objects are non-zero and differ"
(lane openRepoProject-2 ruling R-18, change 2 at `568c477`), where `fa9f0be` had
"both not all zeros and differ"; its line-format note says that `git update-ref`
without `-m` writes no tab and no message, the line still an anchor. The
overview reads the reflog itself, one bounded filesystem read of at most 64 KiB
within its filesystem budget (its requirement 3), never a Git child. A merged
row whose reflog is missing (`ENOENT` or `ENOTDIR`), empty (0 bytes), or read to
its 64 KiB bound, or whose surviving entries cannot decide, keeps its
`merged-removable` finding, which suggests only the read-only form, with
`suggestion_gate: "reflog-unavailable"`, the `reflog-unavailable` remedy above,
and no `--all-safe` suggestion; the finding code stays `merged-removable`,
`reflog-unavailable` being only the gate value, and
`project clean <root> --all-safe` excludes the same rows as `reflog-unavailable`
(change 2 at `fa9f0be`, 2026-10-09). A read cut by its wait or by the deadline
records `probe-timeout` or `deadline-exceeded` and leaves the row unprobed for
the gate, where reaching the bound is `reflog-unavailable`, and any other error
on the read makes the row `inspection-error` with an `os-error`; the repository
gates count both, so `inspection-incomplete` withholds `--all-safe` for the
whole repository, with the R-16 remedy above (ruling R-12; change 2 at `fa9f0be`
and `ef288fe`). The submodule gate has two triggers: a gitlink (mode `160000`)
entry in the target's index, found by the `git ls-files` check, or a
`<common_dir>/worktrees/<admin_id>/modules` entry, found by the `lstat`, which
is where a linked worktree's submodule repositories live. On Git 2.43,
non-force `git worktree remove` refuses with exit status 128 whenever the
submodule is or was populated, that is whenever that admin `modules` directory
exists, even after `submodule deinit` and even with no gitlink in the index; a
worktree whose gitlink was never populated is removed. The batch excludes
every gitlink and every worktree with that directory, so the gate fails
closed. The overview does not run those probes, and each such exclusion is
listed in the batch plan.

`protected-default` produces no finding by itself, but on a
`protected-default` checkout the overview emits every applicable finding,
not a first match: `dirty` (see "Merge target and classification reuse"),
plus one of `diverged`, `unpushed`, or `remote-ahead` (the proposal's OQ-20
drift findings); `unpublished`, with the message "merge-target branch has no
upstream; local commits are unverified", when no upstream is configured; and
`remote-gone` when the upstream is gone. Every one of them carries
`suggested_command: null` and never sets the row's `suggested_command`,
because `project clean` offers no action for the merge-target checkout. That
narrows, for that checkout only and on purpose, the per-code suggestions the
table above gives these codes. Row errors and scan errors
are not findings, but they display in the repair category. A finding of
severity `error` makes the exit 1; `warning` does so only with `--strict`;
`info` never affects the exit.

`--attention` shows every scan error, every row with status `error`, and every
row with at least one repair, preserve, or housekeeping finding; within a
shown row it hides informational findings. The filter is display-only. It
never changes what is collected, the summary counts, the JSON document, or
the exit status. `--attention --json` prints the full envelope, and consumers
filter on `findings[].category`.

## JSON contract

`project overview --json` prints one new envelope with `schema_version: 1`.
It has no compatibility constraint with the clean report, but it reuses the
clean report's field names and meanings wherever it carries the same fact.

### Envelope

| Field | Type | Meaning |
| --- | --- | --- |
| `schema_version` | integer | `1` |
| `observed_at` | string | collection start, RFC 3339 UTC |
| `roots` | array of root objects | canonical byte order |
| `limits` | object of integers | `roots` 32, `candidates` 128, `worktree_rows` 512, `root_entries` 4096, `ignored_entries` 64, `status_records` 4096, `ignored_samples` 8 |
| `budget` | object of integers | `probe_timeout_seconds` 5, `invocation_timeout_seconds` 60, `probe_concurrency` 4 |
| `probes` | object of integers | `estimated`, `performed` |
| `projects` | array of project rows | sorted by the bytes of `path` |
| `relationships` | array | always `[]` in version 1 |
| `summary` | object of integers | `projects`, `repositories`, `worktrees`, `errors`, and `findings` counted by category |
| `completeness` | string enum | `complete` or `incomplete` |
| `scan_errors` | array of error objects | in canonical collection order, not occurrence order, so the promise of "Scheduling and concurrency" holds (change 2 phase 6 (5094e4e), lane openRepoProject-2, 2026-10-09) |

A root object is `{path, path_valid_utf8, source, state, entries}`. `source`
is `argument`, `environment`, or `default`; `state` is `listed`, `truncated`,
`absent`, `unreadable`, or `omitted`; and `entries` is the integer number of
directory entries read, or null when the root was not listed.

### Project row

| Field | Type | Meaning |
| --- | --- | --- |
| `name` | string | manifest `name`, else the directory name |
| `path` | string | canonical project directory: `repository.root` for a Git row (the candidate when `root` is null), the holder for a family holder, else the candidate |
| `path_valid_utf8` | boolean | false when `path`, `repository.root`, or `repository.common_dir` is not valid UTF-8 |
| `kind` | string enum or null | `single`, `project-manifest`, or `family-holder`; null when the marker checks failed |
| `repository` | object or null | `{root, common_dir, dev, ino}`; `root` is null for a bare main entry |
| `merge_target` | object or null | `{name, source, sha}` |
| `git` | object or null | the checkout at `path`, typed below |
| `worktrees` | array or null | worktree rows, main worktree first, then by path bytes |
| `findings` | array | finding objects, by checkout path, then code |
| `suggested_command` | array of strings or null | the row's single next command, as argv |
| `status` | string enum | `error` when `errors` is non-empty, else `ok` |
| `errors` | array | error objects in probe order, which is fixed; only `scan_errors` and the collection order are canonical (lane openRepoProject-2, 2026-10-09) |

`git` mirrors `repo_state`'s top-level fields for the checkout at `path`:
`branch`, `head`, `dirty`, `upstream`, `ahead`, and `behind` have the types
and null rules of the same fields in that checkout's worktree row, and
`tracking_freshness` is a string that is never null.

A worktree row has these fields. Their meanings match the clean report at
`a040790`, including `branch: "detached"` for a detached head, and the
recommendation text travels in the finding's `message` rather than in the
row.

| Field | Type | Null when |
| --- | --- | --- |
| `path` | string | never |
| `path_valid_utf8` | boolean | never |
| `dev`, `ino` | integer or null | `lstat` of the path failed |
| `admin_id` | string or null | the main worktree, a missing or unreadable path, or a registration mismatch |
| `present` | boolean or null | `lstat` failed with an error other than `ENOENT` or `ENOTDIR` |
| `locked`, `prunable` | boolean | never; both come from the registry |
| `current` | boolean or null | `present` is null |
| `branch` | string | never; `"detached"` for a detached head |
| `head` | string or null | the registry reports no `HEAD` |
| `upstream` | string or null | no upstream is configured, or the ref listing failed |
| `upstream_oid` | string or null | no upstream, the upstream ref is gone, or the ref listing failed |
| `ahead`, `behind` | integer or null | no upstream, the upstream ref is gone, or the ref listing failed |
| `remote_present` | boolean or null | no upstream, or the ref listing failed |
| `merged_into_target` | boolean or null | a detached head, a missing path, no merge target, or a failed merged-set probe |
| `dirty` | boolean or null | the status probe did not run or failed |
| `ignored_files` | integer or null | as for `dirty`, or the stream stopped before any ignored record |
| `ignored_files_truncated` | boolean or null | the status probe did not run or failed |
| `ignored_samples` | array of strings or null (objects `{path, path_valid_utf8}` under lane openRepoProject-2 ruling R-9 (2026-10-09), a departure from the packet) | the status probe did not run or failed; `[]` when it found none |
| `classification` | string or null | the ladder did not run (see "Merge target and classification reuse") |

`summary` counts the whole collection, whatever `--attention` shows:

| Field | Type | Meaning |
| --- | --- | --- |
| `projects` | integer | project rows, error rows included |
| `repositories` | integer | distinct repositories whose identity was established |
| `worktrees` | integer | worktree rows across all project rows, main worktrees included |
| `errors` | integer | row errors plus scan errors |
| `findings` | object of integers | finding counts keyed `repair`, `preserve`, `housekeeping`, and `informational` |

The row's `suggested_command` is null unless a finding supplies one: it is
the `--all-safe` form when the row has a `merged-removable` finding, which
exists only after the per-worktree gates in "Attention categories", and the
repository gate does not apply; otherwise the read-only
`project clean <root>` when any finding suggests it; otherwise null.

### Finding object

| Field | Type | Meaning |
| --- | --- | --- |
| `code` | string enum | a code from the attention table |
| `category` | string enum | `repair`, `preserve`, `housekeeping`, or `informational` |
| `severity` | string enum | `error`, `warning`, or `info` |
| `checkout` | object or null | `{path, dev, ino, admin_id}` of the worktree, or null for a repository-level finding |
| `evidence_source` | string enum | `worktree-status`, `worktree-registry`, `local-refs`, `manifest`, or `filesystem` |
| `message` | string | the classifier's recommendation text, or a fixed sentence for other codes |
| `observed_at` | string | RFC 3339 UTC time at which the deciding probe completed |
| `suggested_command` | array of strings or null | argv, per the attention table |
| `suggestion_gate` | string or null | the code of the gate that withheld or limited `suggested_command` (see "Attention categories"); null when none did |
| `suggestion_gate_rows` | integer or null | the repository's worktree-row count behind an `inspect-cap` gate; null otherwise |

### Representation rules

- Every field listed above is always present. Only an error object's `path` is
  optional, and only `scan-limit` and `deadline-exceeded` errors add `limit`
  (a key of `limits`) and `omitted` (`{count, exactness}`).
- Integers are JSON integers, never strings. Object ids are full lowercase
  hexadecimal (40 characters in a SHA-1 repository). Times are RFC 3339 UTC
  with a `Z` suffix. Durations are integer seconds in fields ending in
  `_seconds`.
- `null` means unknown or not established. It is never shorthand for
  `false`, `0`, or an empty list; `false`, `0`, and `[]` are observations.
  `findings` is always an array: on a row with status `error`, an empty
  array means that no finding was computed, not that the project is clean.
- Enums are closed within a version. Adding a field or an enum value is
  additive within version 1, and consumers ignore fields they do not know.
  Renaming or removing a field, or changing its type or meaning, increments
  `schema_version`.
- Error codes are those in the collector table, plus `scan-limit` (a row or
  scan error) and `root-unreadable` (a scan error).
- `completeness` is `incomplete` exactly when `scan_errors` is non-empty or
  any row has status `error`; otherwise it is `complete`.
- Paths are absolute and canonical, except `ignored_samples` (relative to the
  worktree) and an absent default root (expanded but unresolved). Under lane
  openRepoProject-2 ruling R-9 (2026-10-09), a departure from the packet, every
  nested JSON path value carries a validity flag beside it, and an
  `ignored_samples` entry is an object `{path, path_valid_utf8}`.
- Output size is bounded by the caps: at most 128 project rows, 512 worktree
  rows, eight samples per worktree row, and 200-character messages.

### Repository identity and the clean handoff

Every Git row carries `repository: {root, common_dir, dev, ino}`, where `dev`
and `ino` identify `common_dir`. A clean suggestion is exactly
`["project", "clean", "<repository.root>", "--all-safe"]` or
`["project", "clean", "<repository.root>"]` with the absolute canonical root. It
is emitted for a cleanup opportunity whenever `repository.root` is non-null; a
bare repository has no root and gets no clean suggestion. The `--all-safe` form
is withheld for the whole repository while any of its worktree rows is
`inspection-error`, or while it has more worktree rows than batch cleanup
inspects, because the batch plan would then be refused as
`inspection-incomplete` or `inspect-cap`, and while any of its rows went
unprobed, because that plan is then not known to be complete; the read-only form
is suggested instead. An unstarted worktree's `merged-removable` finding also
suggests only the read-only form, with `suggestion_gate: "unstarted-branch"`,
and so does one whose reflog cannot decide, with
`suggestion_gate: "reflog-unavailable"` (rulings N-5 and P6-5, with the reflog
read of the D10 amendment and ruling R-12, change 1 at `0b3c33d` and `4f2162b`,
mirrored in change 2 at `4495ae7` (R-20; unchanged at `cc43860`); see "Attention
categories"). A suggestion never names a project by bare name and never includes
`--apply` or `--yes`. A root that is not valid UTF-8 cannot be carried exactly
in a JSON argv array, so such a row gets the `unsupported-path-bytes` finding
instead of a suggestion.

Every `project clean` invocation whose target is an absolute path resolves it
Git-first: the read-only report with or without `--json`, `--all-safe`, and
`--apply --action push|remove|delete-branch` alike. The rule is specified
once, in batch cleanup's "Command directory and repository resolution": an
absolute path that is a main worktree toplevel resolves to itself even where
`discover` would redirect it, and a path that is not one (a subdirectory, a
linked-worktree path, a bare repository, or a non-repository) is refused
with `target-not-repository-root` and exit 2. For the overview, both
suggestion forms name `repository.root`, the main worktree toplevel by
construction, so either one acts on exactly the repository the row describes
without a round-trip check. The change is listed under "Baseline behavior
changes".

The plan of [batch cleanup](project-maintenance-batch-cleanup.md) records the
same `repository` and `merge_target` objects. A script that follows a
suggestion can compare the plan's `repository` `{common_dir, dev, ino}` with
the overview row's; a mismatch means the directory now holds a different
repository. The overview is evidence, never permission: the batch
recomputes, displays, and confirms its own plan, and it may exclude a
suggested worktree for reasons only its deeper probes see, as "Attention
categories" notes.

### Path encoding

Git output is read as bytes. The registry and the status probe are split on
NUL (`-z`); the ref listing separates fields with `%00` and ends each record
in LF, which is safe because ref names cannot contain control characters. No
path is parsed from newline-delimited output, so newlines, tabs, and other
control characters in paths are supported. For filesystem use each path is
decoded with the filesystem encoding's `surrogateescape` handler.
`git worktree list --porcelain -z` requires Git 2.36 or newer; the version
check under the probe model refuses older Git rather than fall back to
newline parsing.

In JSON, a path that is valid UTF-8 is emitted exactly, using JSON's own
escapes such as `\n`, `\t`, `\u0007`, and `\u202e`: the serializer escapes
every control, bidirectional, and format code point, so the document never
carries one raw. A path that is not valid UTF-8 is
emitted in escaped form: each undecodable byte becomes the four characters
`\xHH` (lowercase hexadecimal), each literal backslash is doubled, and the
owning object carries `path_valid_utf8: false`. That row or worktree gets an
`unsupported-path-bytes` finding, never contributes to a clean suggestion,
and is excluded from batch apply with reason `unsupported-path-bytes`.

In human output, a path that contains no control character (U+0000 to U+001F
or U+007F to U+009F), no bidirectional or format character (U+200E, U+200F,
U+2028, U+2029, U+202A to U+202E, or U+2066 to U+2069), and no undecodable
byte prints verbatim in prose and with POSIX shell quoting in commands. Any
other path prints in `$'…'` form, with the escaping both documents share:
each undecodable byte as `\xHH` and each decoded control, bidirectional,
or format code point as `\uXXXX`, both with lowercase hexadecimal digits
(a newline is `\u000a` and U+202E is `\u202e`), each backslash doubled,
and each single quote as `\'`. The terminal therefore
cannot reorder or hide part of the displayed path. The same form is used in
prose and in commands, so a printed command can be pasted into bash or zsh
unchanged under a UTF-8 locale. Under the C locale that holds only for
escapes below U+0080, such as `\u000a`: bash can leave a non-ASCII escape
such as `\u202e` unexpanded, and zsh can reject it with “character not in
range”. Results varied between environments on 2026-10-07, and only a path
with bidirectional, format, or C1 characters is affected. Pasting also needs
bash 4.2 or newer, the first bash whose `$'…'` form expands `\u`; the
stock bash 3.2 of macOS lacks it. Lane openRepoProject-2 ruling R-8
(2026-10-09), a departure from the packet, names the code points escaped in the
`$'…'` form and in JSON as those of the Unicode general categories Cc, Cf, Zl,
and Zp, the enumeration above kept as examples within that category rule (change
1 at `0b3c33d`). In the `$'…'` form a code point above U+FFFF is escaped as
`\UXXXXXXXX`, with eight hexadecimal digits.

### Fixture

Two roots are given, `/home/user/projects` and an unreadable
`/home/user/archive`. `atlas` is healthy with one housekeeping finding;
`ledger` has a wrong-kind `project.yaml`, so collection stopped after its
identity probe.

```json
{
  "schema_version": 1,
  "observed_at": "2026-10-07T14:03:12Z",
  "roots": [
    {"path": "/home/user/archive", "path_valid_utf8": true,
     "source": "argument", "state": "unreadable", "entries": null},
    {"path": "/home/user/projects", "path_valid_utf8": true,
     "source": "argument", "state": "listed", "entries": 5}
  ],
  "limits": {"roots": 32, "candidates": 128, "worktree_rows": 512,
             "root_entries": 4096, "ignored_entries": 64,
             "status_records": 4096, "ignored_samples": 8},
  "budget": {"probe_timeout_seconds": 5, "invocation_timeout_seconds": 60,
             "probe_concurrency": 4},
  "probes": {"estimated": 11, "performed": 8},
  "projects": [
    {"name": "atlas", "path": "/home/user/projects/atlas",
     "path_valid_utf8": true, "kind": "single",
     "repository": {"root": "/home/user/projects/atlas",
                    "common_dir": "/home/user/projects/atlas/.git",
                    "dev": 2049, "ino": 1310722},
     "merge_target": {"name": "main", "source": "origin-head",
                      "sha": "9f3b2c4d5e6f708192a3b4c5d6e7f8091a2b3c4d"},
     "git": {"branch": "main",
             "head": "9f3b2c4d5e6f708192a3b4c5d6e7f8091a2b3c4d",
             "dirty": false, "upstream": "origin/main", "ahead": 0,
             "behind": 0, "tracking_freshness": "local refs only; no fetch"},
     "worktrees": [
       {"path": "/home/user/projects/atlas", "path_valid_utf8": true,
        "dev": 2049, "ino": 1310721, "admin_id": null, "present": true,
        "locked": false, "prunable": false, "current": false,
        "branch": "main",
        "head": "9f3b2c4d5e6f708192a3b4c5d6e7f8091a2b3c4d",
        "upstream": "origin/main",
        "upstream_oid": "9f3b2c4d5e6f708192a3b4c5d6e7f8091a2b3c4d",
        "ahead": 0, "behind": 0, "remote_present": true,
        "merged_into_target": true, "dirty": false, "ignored_files": 2,
        "ignored_files_truncated": false,
        "ignored_samples": [".venv/", "build/"],
        "classification": "protected-default"},
       {"path": "/home/user/worktrees/atlas-export", "path_valid_utf8": true,
        "dev": 2049, "ino": 1442817, "admin_id": "atlas-export",
        "present": true, "locked": false, "prunable": false,
        "current": false, "branch": "feature/export",
        "head": "c41d7e2a9b0f3586e1d2c3b4a5968778695a4b3c",
        "upstream": "origin/feature/export",
        "upstream_oid": "c41d7e2a9b0f3586e1d2c3b4a5968778695a4b3c",
        "ahead": 0, "behind": 0, "remote_present": true,
        "merged_into_target": true, "dirty": false, "ignored_files": 0,
        "ignored_files_truncated": false, "ignored_samples": [],
        "classification": "merged-removable"}
     ],
     "findings": [
       {"code": "merged-removable", "category": "housekeeping",
        "severity": "info",
        "checkout": {"path": "/home/user/worktrees/atlas-export",
                     "dev": 2049, "ino": 1442817, "admin_id": "atlas-export"},
        "evidence_source": "local-refs",
        "message":
          "This clean, merged, non-current worktree may be removed explicitly.",
        "observed_at": "2026-10-07T14:03:13Z",
        "suggested_command": ["project", "clean",
                              "/home/user/projects/atlas", "--all-safe"],
        "suggestion_gate": null, "suggestion_gate_rows": null}
     ],
     "suggested_command": ["project", "clean", "/home/user/projects/atlas",
                           "--all-safe"],
     "status": "ok", "errors": []},
    {"name": "ledger", "path": "/home/user/projects/ledger",
     "path_valid_utf8": true, "kind": "project-manifest",
     "repository": {"root": "/home/user/projects/ledger",
                    "common_dir": "/home/user/projects/ledger/.git",
                    "dev": 2049, "ino": 1572866},
     "merge_target": null, "git": null, "worktrees": null, "findings": [],
     "suggested_command": null, "status": "error",
     "errors": [
       {"code": "manifest-invalid",
        "message":
          "Unexpected kind in /home/user/projects/ledger/project.yaml; expected project-manifest",
        "path": "/home/user/projects/ledger/project.yaml"}
     ]}
  ],
  "relationships": [],
  "summary": {"projects": 2, "repositories": 2, "worktrees": 2, "errors": 2,
              "findings": {"repair": 0, "preserve": 0, "housekeeping": 1,
                           "informational": 0}},
  "completeness": "incomplete",
  "scan_errors": [
    {"code": "root-unreadable",
     "message": "[Errno 13] Permission denied: '/home/user/archive'",
     "path": "/home/user/archive"}
  ]
}
```

This fixture keeps the packet's path shape, which ruling R-9 departs from.

`performed` is 8: one version check; for `atlas`, four repository-wide
children (identity, registry, ref listing, and merged set; its target came
from `origin/HEAD` through the listing, with no extra child) and one status
probe for each of its two worktree rows; and one identity child for
`ledger`. `estimated` is 11 because it also counts `ledger`'s three unrun
repository-wide children. The exit is 1 because the result is incomplete.

## Deferred remote inspection boundary

If a later proposal adds an explicit `--remote`, it must be opt-in and
read-only. Derive the query identity from a validated canonical GitHub remote
(`github.com/owner/repository`); strip an optional `.git` suffix and never
print or forward URL-embedded credentials. A credential-bearing, malformed,
or non-GitHub remote produces `remote status unavailable` without a request.

Deduplicate requests by `(host, owner/repository, exact feature-head SHA)`.
Use at most 64 requests per invocation, at most four concurrently, a 5 s
per-request timeout, and a 30 s remote budget that is part of the 60 s
invocation deadline, not added to it. Request at most 100 items per page and
read exactly one page per query, never following pagination. Read at most
1 MiB of each response body. A response that indicates a further page, or a
body cut at 1 MiB, yields an explicit unknown result rather than a partial
answer. When the remote budget or the global deadline expires, queued
requests are cancelled before they are sent and in-flight requests are
aborted; each is recorded as unknown.

A rate limit, 401, 403, timeout, truncation, or other API failure produces an
explicit unknown result and no private metadata in output. Use the normal
GitHub client authentication path; the overview never tests, displays, or
infers credential values, and redacts any URL credentials it encounters.
Local ancestry remains the cleanup gate even when a remote query reports a
merged pull request. Persistent remote caching is deferred.

Bench/container status, park records, and family relationships have
equivalent deferred boundaries: opt-in probes, bounded time, explicit unknown
values, and no mutation. They do not belong in the MVP acceptance contract.

## Result semantics

Proposed exits:

| Exit | When |
| --- | --- |
| 0 | `completeness` is `complete` and no finding has severity `error`; warnings, housekeeping, and informational findings may be present |
| 1 | `completeness` is `incomplete`, or a finding has severity `error`, or `--strict` is given and a finding has severity `warning` |
| 2 | invalid invocation, Git older than 2.36 (`git-too-old`) or no usable `git` (`git-unavailable`), or an exception raised outside the collector boundary |
| 130, 143, 129 | cancellation by SIGINT (130), SIGTERM (143), or SIGHUP (129) |

`completeness` is `incomplete` after any scan error (`scan-limit` for roots,
root entries, candidates, or worktree rows; `root-unreadable`; or
`deadline-exceeded`) and after any row error (`probe-failed`,
`probe-timeout`, `deadline-exceeded`, a worktree-cap `scan-limit`, or a
caught exception). The error-severity findings are `inspection-error` and
`no-merge-target`. On exit 0 or 1 the full result is printed. A root problem
is never exit 2; it is a scan error. Exit 2 keeps the baseline `main`
behavior for `Refused` and `OSError`, and any other exception outside the
collector boundary also exits 2, never with Python's default exit 1. Under
`--json`, every overview exit 2 prints the baseline error object with a
`code` added, `{"error": "<message>", "code": "<code>"}`, where the code is
`git-too-old`, `git-unavailable`, or the collector-table code for the
exception (`refused`, `os-error`, or `internal-error`). Argument errors are
argparse's usage message on standard error, with no JSON. The overview has
no plan envelope to extend, which is why this object is smaller than batch
cleanup's extended error object.

On SIGINT, SIGTERM, or SIGHUP every in-flight child is terminated and reaped
as for a timeout, `Cancelled.` goes to standard error (on a best-effort basis
after SIGHUP, when the terminal may be gone), no result document is printed,
and 130, 143, or 129 takes precedence over 1. The attention filter
affects display, not collection
or exit status. A complete scan with no projects says so explicitly and exits
0.

## Baseline behavior changes

A proposal built on this design must list these changes to `a040790` and
carry them into the governing cleanup specifications,
`openspec/specs/project-clean/spec.md` and
`openspec/specs/project-clean-review-safety/spec.md`. The batch document
lists the same shared items plus its batch-only items: those in the last
item below, and also the resolution of relative paths and the no-argument
default, the meaning of the plan's `root`, the refusal of bare repositories,
`push`'s refusal of a `remote-gone` branch (on the deleted upstream itself,
whatever the row's class, since the ruling applied at `b772195`), the gitfile
and submodule checkout rules, the plain report's 256-row cap, `--apply --json`,
the `unstarted-branch` gate, single-target `remove` included, where `a040790`
removes a fresh merged worktree named with `--worktree`, and the single-target
refusal, with reason `reflog-unavailable`, of a merged worktree whose reflog
keeps no decisive entry. The deferred target cap is listed there too, though it
is not a change to `a040790`, which has no target cap, but change 1 council V5's
departure from this packet's `target-cap` refusal. Each observation of `a040790`
below was confirmed in the 2026-10-07 scratch checks.

- Git-first resolution: every `project clean` invocation whose target is an
  absolute path (the read-only report, `--json`, `--all-safe`, and
  `--apply --action push|remove|delete-branch`) resolves Git-first and
  refuses `target-not-repository-root` unless the path is exactly a main
  worktree root. Today `discover` redirects `/outer/leg` to `/outer` when
  `/outer/project.yaml` exists, and `/Atlas` to `/Atlas/Atlas` when
  `/Atlas/Atlas/family.yaml` exists. Bare names keep the baseline lookup,
  whose Git child becomes counted and deadline-bounded, because every
  inspection Git child runs through a new bounded runner (`push` and
  `delete-branch` excepted, ruling D-W): `Popen` with
  `start_new_session=True`, a scrubbed environment, and output streamed as
  bytes, while `probe()` stays for non-Git children; the overview itself
  never calls `discover`.
- Shared probes: `repo_state` and `cleanup_report` move onto the probes
  described under "Probe model and deadline", so overview, doctor, and clean
  read one evidence model. Its visible consequences:
  - Deleted upstream: the baseline `rev-parse --abbrev-ref @{upstream}` cannot
    distinguish a never-configured upstream from a deleted one, and `a040790`
    reports `unpublished` for both. The ref listing's `%(upstream:track)`
    reports a deleted upstream as `gone`, so overview and clean both classify it
    `remote-gone`, and doctor reads the same evidence. Both are preserve states,
    so nothing becomes removable, except that a merged row with a deleted
    upstream is, by Brett Heap's ruling of 2026-10-09 (applied at `b772195` and
    `cc43860`), tested for local ancestry first and reads `merged-removable`.
  - Status configuration: the baseline ignored-file probe omits
    `--untracked-files=normal`, so under `status.showUntrackedFiles=no` Git
    refuses it, `ignored_files` becomes null, and `a040790` classifies every
    clean, present, non-default worktree `inspection-error` (dirty ones stay
    `dirty`). The combined status probe classifies them from real evidence.
  - Unreadable registered path: `a040790`'s `Path.is_dir()` raises
    `PermissionError`, so `project clean` refuses the whole repository with
    exit 2. The row now has `present: null`, an `os-error`, and
    `inspection-error`, and the other rows are still reported.
  - Failed root status: at `a040790` a failed `git status` in the
    repository root raises `Refused` in `repo_state`, ending `clean`,
    `status`, `doctor`, and `update` with exit 2. The main worktree's row is
    now `inspection-error`, and the other rows are still reported.
  - Registration mismatch: a worktree whose admin registration disagrees is
    no longer status-probed; it is `inspection-error` with a
    `registration-mismatch` finding.
  - Probe cost: each worktree row costs one combined status probe instead of
    two.
- Path parsing: Git output is parsed NUL-delimited, so a worktree path with a
  newline is no longer misread as a truncated path and classified
  `stale-worktree`, and a path with non-UTF-8 bytes no longer stops
  `project clean --json` with an uncaught `UnicodeDecodeError`.
- `ignored_files` becomes the number of ignored entries read: a lower bound
  when the new `ignored_files_truncated` is true, and null when the probe
  stopped before any ignored entry.
- The manifest's `tracking_branch` is read at `repository.root`, not at
  whichever directory `discover` returned.
- A manifest larger than 1 MiB by `st_size` is `manifest-invalid` before it is
  read (lane openRepoProject-2 ruling R-4, 2026-10-09), at the merge-target
  manifest read, where `a040790` reads a manifest of any size: `clean`
  refuses with exit 2, and the overview records a row error (change 2
  council V7; the shared evidence model of change 1 at `0669a20`).
- Timeouts: under the overview's and `clean`'s 60 s monotonic deadlines,
  every inspection Git child gets `min(5 s, remaining)` and runs in its own
  process group, instead of the baseline `probe()` helper's fixed 15 s with
  no invocation deadline; `status`, `doctor`, and `update` have no deadline
  and keep 15 s per Git child, and `push` and `delete-branch` stay unbounded
  (ruling D-W).
- Git 2.36 or newer is required for `worktree list -z`. The version check
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
  no `code`, which these refusals add. The `inspection-error` mark that `status`
  and `doctor` set is `classification: "inspection-error"` with `errors` beside
  it, on the root and leg dicts (change 1 phase 6 (`90854a3`), lane
  openRepoProject-2, 2026-10-09).
- Batch cleanup only, specified there: single-target `remove` runs on the
  shared removal seam, its completeness limited to the repository-wide
  evidence and its own row; the removal command gains
  `-c status.showUntrackedFiles=normal`, `-c core.untrackedCache=false`, and
  `-c core.fsmonitor=false`, so Git's own cleanliness check sees untracked
  files; selected targets get bounded `git ls-files` checks, run in each
  target's own worktree, and an `lstat` of each target's admin `modules`
  path, which exclude `hidden-local-state` and `contains-submodule`; and a
  branch with no commit of its own is excluded as `unstarted-branch`, by
  single-target `remove` too, so a fresh merged worktree named with
  `--worktree` is refused where `a040790` removes it; and a merged worktree
  whose reflog keeps no decisive entry, as after 90 days without activity under
  the default `gc.reflogExpire`, is refused in single-target mode as
  `target-excluded` with reason `reflog-unavailable`, where `a040790` removes it
  (change 1 at `0b3c33d`, worded so at `4f2162b`, lane openRepoProject-2,
  2026-10-09).

The path and status-configuration changes replace a wrong or failed
classification with one drawn from real evidence. A worktree they newly show
as `merged-removable` is removable only under the same ladder, gates, and
batch revalidation as any other, and a non-UTF-8 path stays excluded from
apply.

## MVP validation scenarios

Each scenario runs `project overview` in human and `--json` form against fixture
repositories under `/home/user/projects`, with networking disabled for the
process. Each asserts zero mutation: the before and after snapshots of
`git for-each-ref`, `git worktree list --porcelain -z`, each checkout's
`git status --porcelain=v1 -z --untracked-files=normal --ignored=matching` (a
test-harness snapshot command, not the overview's status probe, so it carries no
`-c` pins), each index file's modification time, and the directory tree under
every root are identical. The scenarios that need a non-UTF-8 path,
**Gated merged worktrees.** and **Non-UTF-8 path.**, cannot be built on macOS
APFS; they are Linux-only and are skipped elsewhere with a reason.

Discovery, identity, and caps:

- **Independent clones and aliases.** Given clones of one origin at
  `/home/user/projects/atlas` and `/home/user/work/atlas`, and a symlink
  `/home/user/projects/atlas-link` to the first; when both parent directories
  are roots; then there are exactly two `atlas` rows whose `repository`
  `{common_dir, dev, ino}` differ, the symlink adds no row, and each human row
  prints its absolute path.
- **One probe set per repository.** Given a repository with a main worktree
  and three linked worktrees, one of them an immediate child of the root and
  one at `/home/user/worktrees/atlas-hotfix` outside every root; when the
  overview runs; then there is one project row with four worktree rows, the
  external worktree adds no project, the repository-wide set (the identity
  probe, the registry, the single ref listing, and the single merged-set
  query) runs once, each present row gets one combined status probe, and
  `probes.performed` equals one version check, plus one identity probe per
  Git candidate, plus three, plus four status probes.
- **Unreadable candidate directory.** Given candidates `alpha`, `locked`, and
  `zeta` under one root, where `locked` has mode 000, and a second root that
  cannot be listed; when the overview runs; then `locked` appears in its
  sorted position with `path` the candidate path, `name` `locked`,
  `kind: null`, `status: "error"`, `findings: []`, one `os-error` naming its
  path, and every Git-derived field null, `alpha` and `zeta` are complete, the
  second root adds a `root-unreadable` scan error, and the exit is 1, never
  2.
- **Candidate cap after sorting, exact count.** Given one root holding 130
  candidate directories `p000` to `p129` created in reverse order; when the
  overview runs; then the rows are `p000` to `p127` whatever the listing
  order, and one `scan-limit` scan error has `limit: "candidates"` and
  `omitted: {"count": 2, "exactness": "exact"}`; the result is incomplete and
  the exit is 1.
- **Candidate cap with an incomplete listing.** Given that root plus a second
  root with 4,100 entries; when the overview runs; then the second root is
  `truncated` with a `root_entries` `scan-limit` error whose omitted count is
  null with exactness `unknown`, and the candidate-cap error reports the known
  excess with exactness `lower-bound`; the exit is 1.
- **Root and worktree-row caps.** Given 33 distinct roots; then the last in
  canonical order is `omitted` with an exact count of 1. Given repositories
  totalling 520 worktree rows; then the first 512 rows in rank order
  (repository rank, then row order) are probed on every run whatever the
  completion order, the other 8 keep registry and branch evidence with
  `dirty`, `ignored_files`, and `classification` null, their project rows
  carry `scan-limit` errors, and the scan error has
  `limit: "worktree_rows"` and `{"count": 8, "exactness": "exact"}`; the exit
  is 1.

Probes, deadline, and bounds:

- **Probe timeout.** Given a worktree whose `git status` is held for 10 s by
  a fixture `core.fsmonitor` hook; when the overview runs; then that child is
  stopped at 5 s and reaped, the row records `probe-timeout` with
  `dirty: null` and classification `inspection-error`, every other row is
  complete, and the exit is 1. The proposals pin `core.fsmonitor=false` for
  every status probe, so this fixture cannot occur as written; feature 005
  rewrites it, producing the hung child with an injected slow `git`.
- **Hung filesystem call.** Given an external worktree on a fixture FUSE
  mount whose `lstat` sleeps for 10 s; when the overview runs; then the call
  is abandoned at 5 s, that worktree records `probe-timeout`, every other row
  is complete, and the exit is 1. A call that never returns from the kernel
  is outside the time bound, as "Deadline and timeouts" states.
- **Invocation deadline.** Given enough held probes to exceed 60 s; when the
  overview runs; then no child starts after the deadline, every in-flight
  child is terminated, killed after 2 s if still alive, and reaped or
  abandoned within the 2 s grace, and recorded as `deadline-exceeded`,
  unstarted candidates appear as rows with `deadline-exceeded`, the scan
  error's omitted count is exact, and the process exits 1 within 64 s plus
  rendering (change 2 phase 6 (5094e4e), lane openRepoProject-2, 2026-10-09).
- **Bounded concurrency.** Given eight single-worktree repositories whose
  `git status` probe a fixture hook holds for 1 s; when the overview runs;
  then the process table never shows more than four of its Git children at
  once or two with the same `common_dir`, the eight held probes take about
  2 s rather than 8 s, and the JSON equals that of a run limited to one child
  apart from timestamps and `budget.probe_concurrency`. The proposals pin
  `core.fsmonitor=false` for every status probe, so this fixture cannot occur
  as written; feature 005 rewrites it, holding the probes with an injected
  slow `git`.
- **Bounded ignored files.** Given a clean merged worktree with 10,000 ignored
  files; when the overview runs; then the stream stops early,
  `ignored_files` is 64 with `ignored_files_truncated: true`,
  `ignored_samples` has eight entries, `dirty` is still established as false
  because Git lists ignored records last, and the classification is
  `ignored-local-files`, a preserve finding. With exactly 64 ignored files,
  `ignored_files` is 64 with `ignored_files_truncated: false`. With 4,097
  untracked files and no ignored ones, the stream stops at the record bound,
  `dirty` is true, `ignored_files` is null, and the classification is
  `dirty`, not `inspection-error`.
- **User status configuration.** Given `status.showUntrackedFiles=no` in the
  user's Git configuration and a clean, pushed, merged linked worktree; when
  the overview runs; then the combined status probe succeeds, `ignored_files`
  is 0, and the worktree is `merged-removable`, where `a040790` classifies it
  `inspection-error` because its ignored-file probe fails.
- **Git version refusal.** Given a `git` that reports version 2.34.1; when
  the overview runs; then it exits 2 with code `git-too-old` and a message
  naming the 2.36 minimum before listing any root or starting any other Git
  child, and under `--json` prints only
  `{"error": "<message>", "code": "git-too-old"}`. With no `git` on `PATH`,
  it does the same with code `git-unavailable`.

Collector boundary:

- **One helper failure is isolated.** Given candidates `alpha`, `ledger`, and
  `zeta`, where `ledger/project.yaml` declares `kind: other` so the existing
  `manifest()` raises `Refused`; when the overview runs; then `alpha` and
  `zeta` are complete, and `ledger` appears in its sorted position with
  `status: "error"`, a `manifest-invalid` error, its repository identity
  retained, and null `merge_target`, `git`, and `worktrees`. The exit is 1,
  where the same `Refused` ends `project clean` today with a whole-command
  exit 2. This is the wrong-kind case. A `ledger/project.yaml` that is not
  valid UTF-8 is the unreadable case, for which the `project-review-safety`
  requirement on YAML decoding sets exit 2 on `clean`; the overview gives it
  the same `manifest-invalid` row error and exit 1.

Merge targets (where a target exists, each also asserts that its name equals
the `target_branch` that `project clean <root> --json` reports at `a040790`,
that the merged set was computed at `merge_target.sha`, and that resolution
spawned no Git child beyond the ref listing; in the missing case `a040790`
refuses):

- **Manifest target.** Given a `project.yaml` with
  `tracking_branch: origin/develop`, a local `develop`, and no `origin/HEAD`;
  then `merge_target` is `develop` with source `manifest` and the SHA of
  `refs/heads/develop`, and classification is relative to `develop`.
- **`origin/HEAD` target.** Given no manifest, `origin/HEAD` naming
  `origin/trunk`, and local `trunk` and `main`; then the target is `trunk`
  with source `origin-head` and the SHA of `refs/heads/trunk`.
- **`main` target.** Given no manifest and no `origin/HEAD`, and local `main`
  and `master`; then the target is `main` with source `main` and its SHA.
- **`master` target.** Given only a local `master`; then the target is
  `master` with source `master` and its SHA.
- **Conflicting targets.** Given a manifest naming `develop` and
  `origin/HEAD` naming `main`, both existing locally; then the target is
  `develop` with source `manifest` and its SHA, and one informational
  `merge-target-conflict` finding names both branches; the exit is 0 when
  nothing else is found.
- **Missing target.** Given a manifest naming an absent `release`, no
  `origin/HEAD`, and neither `main` nor `master`; then `merge_target` is
  null, the row has a `no-merge-target` repair finding of severity `error`
  with no suggested command, every worktree's classification is null,
  `cleanup_report` was never called, and the exit is 1. On the same fixture,
  `project clean <root> --all-safe` refuses with exit 2 before any mutation.

Classification and attention:

- **Every protected classifier.** Given one repository whose worktrees are
  classified `protected-default`, `dirty`, `ignored-local-files`, `detached`,
  `unpublished`, `remote-gone`, `diverged`, `remote-ahead`, `unpushed`,
  `merged-current`, and `pushed-unmerged`, plus one gate-passing
  `merged-removable`, and a second repository holding the `inspection-error`
  case (a worktree whose corrupted index makes its status probe fail), kept
  apart so that the repository gate does not withhold the first repository's
  `--all-safe` suggestion; when the
  overview runs from inside the `merged-current` worktree; then every
  classification equals the `a040790` output of `project clean <root> --json`
  run from the same directory, except that the deleted-upstream row is
  `unpublished` there; each finding has the category and severity of the
  attention table; the only housekeeping finding and the only `--all-safe`
  suggestion belong to the `merged-removable` worktree; and no other worktree
  appears in the `selected` list of the batch preview that suggestion runs.
  Making the `protected-default` checkout dirty adds one `dirty` preserve
  finding without changing its classification. `review-required`, which no
  Git state reaches under the shared evidence model, is covered by a
  classifier test on an injected evidence row.
- **Gated merged worktrees.** Given four worktrees the ladder would otherwise
  classify `merged-removable`: one locked with `git worktree lock`, one whose
  `.git` file was edited to name another admin directory, one whose path
  contains the byte `0xFF`, and the main worktree checked out on a merged
  non-target branch while the overview runs elsewhere; when the overview
  runs; then the
  locked one has a `locked-worktree` informational finding suggesting the
  read-only `project clean <root>`, the mismatched one gets no status probe,
  is `inspection-error`, and has a `registration-mismatch` repair finding,
  the non-UTF-8 one has `unsupported-path-bytes`, and the main worktree has a
  `main-worktree` informational finding, and none of the four produces a
  housekeeping finding. Given also a fifth, gate-passing `merged-removable`
  worktree in the same repository; then it keeps its housekeeping finding,
  but because the mismatched row is `inspection-error`, both its suggestion
  and the row's are the read-only `project clean <root>`, not `--all-safe`.
  After `git worktree repair` fixes the mismatched registration, that
  worktree is clean, merged, published, and unlocked, so it is eligible
  again: the `--all-safe` suggestion returns, and the batch preview of the
  repository selects the repaired worktree and the fifth.
- **Attention filter per category.** Given four projects whose only findings
  are `pushed-unmerged` (informational), `unpushed` (preserve),
  `merged-removable` (housekeeping), and `no-merge-target` (repair); when
  `project overview` and `project overview --attention` run, each also with
  `--json`; then `--attention` hides the informational-only project and shows
  the other three under their category headings, the two JSON documents are
  identical apart from their timestamps, and both runs exit 1. Without the
  repair project both runs exit 0, and with `--strict` both exit 1 because of
  the preserve warning.

External linked worktrees:

- **Present eligible external worktree.** Given `atlas` with a clean, pushed,
  merged linked worktree at `/home/user/worktrees/atlas-export`, outside every
  root; when the overview runs; then it appears among `atlas`'s worktrees with
  `dev`, `ino`, and a two-way-verified `admin_id`, classification
  `merged-removable`, a housekeeping finding, and the suggestion
  `project clean /home/user/projects/atlas --all-safe`; the project count is
  unchanged.
- **Missing external worktree.** Given that directory deleted without
  `git worktree prune`; when the overview runs; then its row has
  `present: false`, classification `stale-worktree`, and a housekeeping
  warning suggesting the read-only `project clean /home/user/projects/atlas`;
  no probe runs in the missing path; the exit is 0, or 1 with `--strict`.
- **Unreadable external worktree.** Given the worktree's parent directory made
  unsearchable so that `lstat` fails with `EACCES`; when the overview runs;
  then the worktree has `present: null` and classification
  `inspection-error`, the project row has an `os-error` in `errors[]` and
  status `error`, the other rows are reported, and the exit is 1, where
  `a040790` refuses the whole repository with exit 2. When only the
  worktree's own status probe fails, the row records `probe-failed` and
  `inspection-error`, set directly, instead.

Paths:

- **Control and format characters in paths.** Given a repository at
  `/home/user/projects/odd` + newline + `name` whose linked worktrees' names
  contain a tab, U+0007, and U+202E; when the overview runs; then each JSON
  `path` is exact (with the escapes `\n`, `\t`, `\u0007`, and `\u202e`) with
  `path_valid_utf8: true`, each worktree is classified from its real state
  rather than as the `stale-worktree` that the `a040790` newline parse
  yields, the human output prints each such path in `$'…'` form (the newline
  as `\u000a`, the tab as `\u0009`, U+0007 as `\u0007`, and U+202E as
  `\u202e`), and the printed suggestion, pasted into bash under a UTF-8
  locale, names the same repository root.
- **Non-UTF-8 path.** Given a clean merged worktree whose name contains the
  byte `0xFF`; when the overview runs; then it completes where `a040790`
  exits 1 with an uncaught `UnicodeDecodeError`, the worktree's `path` shows
  the byte as `\xff` with `path_valid_utf8: false`, the row has an
  `unsupported-path-bytes` repair finding, the worktree contributes nothing to
  the `--all-safe` suggestion, and batch cleanup excludes it with reason
  `unsupported-path-bytes`.

Handoff and family:

- **Canonical identity through the handoff.** Given two projects named
  `atlas` at `/home/user/projects/atlas` and `/home/user/work/atlas`, each
  with a merged-removable worktree; when the overview runs; then the rows'
  `suggested_command` values are
  `["project", "clean", "/home/user/projects/atlas", "--all-safe"]` and
  `["project", "clean", "/home/user/work/atlas", "--all-safe"]`. When each is
  run, `project clean` resolves the absolute path Git-first (its realpath
  equals the main worktree toplevel), and each plan's `repository` (`root`,
  `common_dir`, `dev`, `ino`) and `merge_target` equal that overview row's.
  Given a root that is an assembly with a `project.yaml` and an
  immediate-child leg `api` that is its own repository with one dirty and one
  merged-removable worktree; then the leg's row suggests
  `["project", "clean", "<leg root>", "--all-safe"]`, its `dirty` finding
  suggests the read-only `["project", "clean", "<leg root>"]`, and running
  either reports `root` equal to the leg, where `a040790`'s `discover` would
  redirect that path to the assembly. Given the same command with a
  linked-worktree path or a subdirectory instead of the root,
  `project clean` refuses with exit 2 and `target-not-repository-root` before
  any mutation.
- **Family holder count, relationships, and probe ownership.** Given a root
  containing `acme/acme/family.yaml` in a Git toplevel that declares members
  at `acme/web` and `acme/api`, plus an ordinary repository `tools`; when the
  overview runs; then there are exactly two rows, a `family-holder` at
  `/home/user/projects/acme/acme` and `tools`, `summary.projects` is 2,
  `relationships` is `[]`, no row and no Git child exists for `acme/web` or
  `acme/api`, and the holder's repository-wide probes run once and belong to
  its row. Without `acme/acme/.git`, the holder row has null `repository`,
  `merge_target`, `git`, and `worktrees`, status `ok`, no error, and no Git
  child. With `/home/user/projects/acme` itself as the root, `web` and `api`
  become ordinary rows of their own and `relationships` stays `[]`.
- **Local and read-only.** Given any fixture above; when the overview runs
  with default options; then it opens no network connection and makes no
  filesystem or Git mutation, and the JSON preserves severity, freshness,
  unknown values, and completeness. A complete scan with no projects says so
  and exits 0.

## Deferred validation scenarios

- A remote request with a canonical URL is deduplicated by exact head;
  malformed and credential-bearing URLs are rejected without exposing
  credentials; 401, 403, rate-limit, timeout, a response that needs a second
  page, and a body over 1 MiB all remain unknown; and expiry of the remote
  budget or the global deadline cancels queued and in-flight requests.
- A family holder, working sibling, mounted member, and parked record are
  represented as relationships without duplicate checkout probes when those
  integrations are separately proposed.

## Alternatives and open decisions

An arbitrary-depth recursive scan would find more nested repositories but
would be slower and prone to discovering dependency/vendor trees. Prefer
bounded discovery with explicit additional roots for the first version.

The caps and the deadline must still be reconciled by measurement: the caps
are provisional until the proposal measures them, and if measured warm
children average more than about 210 ms even with concurrency, the caps must
fall or very large estates end incomplete. The proposals took this
section's other former open items as proposal decisions, open to
ratification, as the
[fix handoff](next-session-project-maintenance-fix-handoff.md) records under
"Decisions taken by the proposals — 2026-10-08": bounded concurrency of
four children across repositories, with the serial fallback of 32
candidates and 128 worktree rows (1 + 32 × 4 + 128 × 1 = 257 children, about
38.6 s at 150 ms, or about 44.6 s with the listing estimate) if design
rejects it; no per-repository row cap, so one repository with more than
about 355 worktree rows ends at the deadline, visibly incomplete; no
configurable limits; no `attention` alias; the full envelope under
`--attention --json`; argv-only suggested commands; the extra `dirty`
finding kept; and one separate change per remote, family, bench, container,
or park integration. Exact bench/type validation remains existing-doctor
follow-up work.

Questions for Brett Heap, the first ruled on 2026-10-09 and applied at `b772195`
and `cc43860`, the second open:

- For Brett Heap, ruled and applied: whether a local ancestry proof should
  outrank `remote-gone` for worktree rows. Brett Heap ruled yes on 2026-10-09
  ("yes, local ancestry proof outranks remote-gone"; to lane openRepoProject-2,
  "yes, local ancestry proof outranks remote-gone, apply it"), and both
  proposals applied it: change 1 at `b772195`, change 2 at `cc43860`. Lane
  openRepoProject-3 raised it, recommending yes, and lane openRepoProject-2
  carried it in both proposals. The packet's own ladder tests remote presence
  before merge state, as the baseline does, and the packet designs no mechanism
  for the ruling; GitHub's head-branch auto-delete with `fetch.prune` leaves a
  merged branch's upstream gone, and the MVP never deletes a branch, so under
  that order such a worktree was never eligible for `--all-safe`. Measured here:
  4 of about 90 merged worktrees, `fetch.prune` unset everywhere, and
  auto-delete on 2 of 21 repositories. The proposals now test a branch whose
  configured upstream's remote-tracking ref no longer exists for local ancestry
  before the `remote-gone` rung: when it is merged into the target the row is
  `merged-removable` (`merged-current` when it is the current worktree), and
  otherwise it is `remote-gone`, so only an unmerged row is `remote-gone`. The
  interim `remote-gone` text, the recommendation that called a merged row not
  removable by `project`, is gone from the seven places that carried it. In
  change 1, `push` refuses on the deleted upstream itself, whatever the row's
  class; revalidation does not count a value null in the plan and null again as
  a difference; and `--worktree` removes a merged worktree whose upstream was
  deleted, where `a040790` refuses it as `unpublished`, which is the fifth
  user-visible change; the scenario "A merged worktree whose upstream was
  deleted" keeps its title and gains an AND clause for `--worktree`. In change
  2, requirement 6 and its scenario mirror the ladder, the departures bullet
  quotes Brett Heap's words and records that the ruling supersedes R-6, and
  requirement 10's default-branch finding is untouched.
- For Brett Heap: squash merges never satisfy the ancestry proof, so the MVP
  selects little in a squash-merge repository. The recommendation is a local
  patch-equivalence proof (`git cherry` or patch-id against the merge
  target), designed as a follow-on change, not in the MVP.

## Relationships

The [maintenance flow](project-maintenance-synthesis-inspect-and-retire.md)
connects this view to [batch cleanup](project-maintenance-batch-cleanup.md).
The [packet overview](project-maintenance-overview.md) defines the scope.
