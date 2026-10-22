Lane: openRepoProject-4

# Contract: `project overview`

The command line, streams, exits, JSON document and human report of the
overview, and every text it prints, in one place. The sources govern where
this restates them: change 2's delta as amended by A1 (`A1:N`, its
`specs/project-overview/spec.md` at `e4a30fc`) and A1's design D3, D4, D5
and D10; [spec.md](../spec.md) settles their readings, and
[research.md](../research.md) the plan's own choices (PN-1 to PN-18).

**Reading the texts.** A quoted text that does not fit one line continues
on the next line, indented; each line break inside a quoted text reads as
one space. Placeholders are in capitals (`PATH`, `N`, `M`, `CAUSE`), each
replaced by an escaped value ([P]; FR-038). A row marked **HELD** is an
item of research.md R20 that waits on Brett Heap; the text above it is the
one built until his word, the text after it the other answer. Each held
item changes only its own rows.

## Invocation

```text
project overview [--root D]... [--attention] [--json] [--strict]
```

| Option | Meaning |
| --- | --- |
| `--root D` | a root to scan; repeatable (source `argument`) |
| `--attention` | show only what needs attention; display only |
| `--json` | print one JSON document, `schema_version: 1` |
| `--strict` | a finding of severity `warning` also makes the exit 1 |

Without `--root`: `PROJECTS_DIR` when set and not empty (source
`environment`), else `~/projects` and `~/Projects` (source `default`).
No other option, variable or file changes a limit or a time (FR-047).

### Help texts (PN-3)

- `help.command` (in `project --help`): "Report which local projects need
  attention (read-only)"
- `help.description`: "A local, read-only report of every project under
  the roots. A suggested command is advice to review, never permission;
  nothing is fetched or changed."
- `help.root`: "Directory to scan; repeatable. Default: PROJECTS_DIR, else
  ~/projects and ~/Projects"
- `help.attention`: "Show only rows that need attention"
- `help.json`: "Print one JSON document"
- `help.strict`: "Warnings also make the exit status 1"

`--root` takes `metavar="D"`. Adding the subcommand adds one line to
`project --help`; no other subcommand's output changes (FR-047).

## Argument checks (before any Git child)

- An unknown option or a missing value: argparse's usage message on
  standard error, exit 2, no JSON (FR-039).
- An empty `--root` value (PN-13): the same, the option's type check
  failing with `error.empty-root`: "an empty path names no directory".

## Order of a run

1. Parse the arguments (above); the invocation's deadline is set as it is
   entered (60 s, no reserve).
2. The configuration-path test of [E] (feature 004's
   `relative_config_paths`, `project:963`): a variable that fails it
   refuses with `relative-config-path`, exit 2, before any Git child.
3. The version check, once (`git --version`): `git-too-old` or
   `git-unavailable`, exit 2, and no other Git child.
4. `Scanning N roots...` on standard error, only when it is a terminal, N
   the roots given or the defaults, before canonicalisation.
5. Discovery, then collection (research.md R5 to R7); on the deadline,
   every in-flight child is terminated together and nothing more starts.
6. Every child reaped or abandoned; the report rendered whole.
7. The report written inside the raising span (research.md R15).

## Streams

- Standard output: the JSON document, or the human report; nothing else.
- Standard error: `Scanning N roots...`, `REFUSED: MESSAGE`, `Cancelled.`,
  the failed-write line and argparse's usage. Every write to it is
  best-effort, an `OSError` ignored.
- Both are written as UTF-8 whatever the locale; every fixed text is ASCII.

## Exit statuses (FR-042)

| Status | When |
| --- | --- |
| 0 | complete, no `error` finding (none of `warning` under `--strict`) |
| 1 | incomplete, an `error` finding, or `--strict` and a `warning` |
| 2 | invalid invocation; a refusal; a failed write; an exception (below) |
| 130, 143, 129 | SIGINT, SIGTERM, SIGHUP, over every other status |

### Exit-2 outputs (FR-039)

| Cause | `--json` | human |
| --- | --- | --- |
| argument error | usage on stderr, no JSON | usage on stderr |
| `relative-config-path` | error object | `REFUSED:` line |
| `git-too-old`, `git-unavailable` | error object | `REFUSED:` line |
| a refusal outside the boundary | error object, `refused` | `REFUSED:` line |
| an `OSError` outside the boundary | error object, `os-error` | `REFUSED:` |
| any other exception there | error object, `internal-error` | `REFUSED:` |
| failed write to standard output | `line.write-failed` on stderr | the same |

The error object is exactly `{"error": MESSAGE, "code": CODE}`.
`relative-config-path` with exit 2 is ratified ("ratify 34"); only the two
names of LQ-15's extension stay open with PR #19 (O10).

## JSON (FR-036 to FR-039)

Written as `json.dumps(document, indent=2, ensure_ascii=True)` plus one line
feed (PN-6), every key always present, in these orders:

- envelope: `schema_version`, `observed_at`, `roots`, `limits`, `budget`,
  `probes`, `projects`, `relationships`, `summary`, `completeness`,
  `scan_errors`;
- root: `path`, `path_valid_utf8`, `source`, `state`, `entries`;
- `limits`: `roots`, `candidates`, `worktree_rows`, `root_entries`,
  `ignored_entries`, `status_records`, `ignored_samples`, `batch_row_cap`,
  `report_row_cap`, `targets`;
- `budget`: `probe_timeout_seconds`, `invocation_timeout_seconds`,
  `probe_concurrency`;
- `probes`: `estimated`, `performed`;
- project row: `name`, `path`, `path_valid_utf8`, `kind`, `repository`,
  `merge_target`, `git`, `worktrees`, `findings`, `suggested_command`,
  `status`, `errors`;
- `repository`: `root`, `common_dir`, `dev`, `ino`, `root_valid_utf8`,
  `common_dir_valid_utf8`;
- `merge_target`: `name`, `source`, `sha`;
- `git`: `branch`, `head`, `dirty`, `upstream`, `ahead`, `behind`,
  `tracking_freshness` (always "local refs only; no fetch");
- worktree row: `path`, `path_valid_utf8`, `dev`, `ino`, `admin_id`,
  `present`, `locked`, `prunable`, `current`, `branch`, `head`, `upstream`,
  `upstream_oid`, `ahead`, `behind`, `remote_present`,
  `merged_into_target`, `dirty`, `ignored_files`,
  `ignored_files_truncated`, `ignored_samples`, `classification`;
- `ignored_samples` entry: `path` (relative to its worktree),
  `path_valid_utf8`;
- finding: `code`, `category`, `severity`, `checkout`, `evidence_source`,
  `message`, `observed_at`, `suggested_command`, `suggestion_gate`,
  `suggestion_gate_rows`;
- `checkout`: `path`, `path_valid_utf8`, `dev`, `ino`, `admin_id`;
- `summary`: `projects`, `repositories`, `worktrees`, `errors`,
  `findings`; `findings`: `repair`, `preserve`, `housekeeping`,
  `informational`;
- error: `code`, `message`, then `path` and `path_valid_utf8` when a path
  is involved, then `limit` and `omitted` (`count`, `exactness`) on a
  `scan-limit` error and on the one `deadline-exceeded` scan error that
  counts the candidates not started (`limit:
  "invocation_timeout_seconds"`).

Arrays: `roots` by canonical bytes; `projects` by the bytes of `path`, a
tie by rank (PN-8); `worktrees` main first, then by path bytes; `findings`
by checkout path bytes, a null `checkout` first, then by code; `errors` in
step order; `scan_errors` in A1 design D6's order (research.md R11).

## Human report (FR-045, FR-046; A1 design D10)

For each shown row, in the JSON's order:

- a header: the name, two spaces, the absolute path;
- per shown finding: two spaces, the category left-justified in 14
  columns, then `code: message`; for a worktree's finding, the worktree
  path on the next line, indented to the message column (16 spaces);
- per row error, the same under category `repair`, a row error with a
  `path` followed by that path on the next line, indented the same;
- when the row has a suggested command or a gate decided it: two spaces,
  `next` left-justified in 14 columns, the command (POSIX shell quoting, or
  the `$'...'` form for a path [P] marks) or `none`, then two spaces and
  `(withheld: REMEDY)` or `(limited: REMEDY)`.

Then one line per scan error, `line.incomplete-path` or `line.incomplete`;
the all-absent line when every root is `absent`; and always the summary
line. Under `--attention` a row is shown when it has status `error` or a
repair, preserve or housekeeping finding, informational findings are
hidden within it, every scan error is shown, and the `next` line stays.
The `next` line names the first gate, in the gate table's order, among
the findings whose suggestion fed the row's command or would have:
`withheld` for every gate but `target-cap` and `inspect-cap` over the
report's row cap, which read `limited`.

```text
atlas  /projects/atlas
  preserve      dirty: Preserve or commit the working changes before cleanup.
                /projects/atlas-wip
  next          project clean /projects/atlas
```

Count nouns are D10's for every count: `1 projects`, `Scanning 1 roots...`
(PN-5).

## Git children (FR-016; FR-040)

Every child is `git` with the seven protocol pins, `-C DIRECTORY` and the
arguments below, in its own process group, standard input from
`/dev/null`, with the 31 scrubbed names removed, `GIT_TRACE2`,
`GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF` set to `0` and
`GIT_OPTIONAL_LOCKS=0` (feature 004's kind `probe`); the status probe adds
the four status pins (kind `status`). No other argument vector is started.

- `version`: `--version` (no `-C`), once.
- `identity`: `rev-parse --path-format=absolute --show-toplevel
  --git-common-dir --show-superproject-working-tree`, per Git candidate;
  on a line count other than two, `rev-parse --path-format=absolute
  OPTION` once per option (EC-032).
- `registry`: `worktree list --porcelain -z`, per repository.
- `core-worktree`: `config --get core.worktree`, where the first registry
  record is `common_dir` (A1 design D3, case 3).
- `extension`: `config --file COMMON_DIR/config --type=bool --get
  extensions.worktreeConfig`, per repository.
- `refs`: `for-each-ref --format=REF_FORMAT refs/heads refs/remotes`, read
  by the keep-filter (research.md R8).
- `merged`: `for-each-ref --merged=SHA --format=%(refname) refs/heads`.
- `work-tree`: `rev-parse --path-format=absolute --show-toplevel`, in each
  linked row whose registration agrees, where the extension is taken as
  true.
- `status`: `status --porcelain=v1 -z --untracked-files=normal
  --ignored=matching`, in each row FR-007's last case reaches.
- HELD (O4 (a)): `main-toplevel`, `rev-parse --path-format=absolute
  --show-toplevel` in the main worktree where it is no Git candidate.

## The attention table (FR-027; A1:491-514)

Suggests: `none`; `read-only`, `["project", "clean", ROOT]`; `--all-safe`,
`["project", "clean", ROOT, "--all-safe"]`, or the read-only form under a
gate.

| Code | Category | Severity | Source | Suggests |
| --- | --- | --- | --- | --- |
| `inspection-error` | repair | error | worktree-status | none |
| `review-required` | repair | warning | local-refs | read-only |
| `no-merge-target` | repair | error | local-refs | none |
| `registration-mismatch` | repair | warning | worktree-registry | none |
| `unsupported-path-bytes` | repair | warning | filesystem | none |
| `unsupported-layout` | repair | error | worktree-registry | none |
| `main-worktree-missing` | repair | warning | worktree-registry | none |
| `dirty` | preserve | warning | worktree-status | read-only |
| `ignored-local-files` | preserve | warning | worktree-status | read-only |
| `detached` | preserve | warning | worktree-registry | read-only |
| `unpublished` | preserve | warning | local-refs | read-only |
| `remote-gone` | preserve | warning | local-refs | read-only |
| `diverged` | preserve | warning | local-refs | read-only |
| `unpushed` | preserve | warning | local-refs | read-only |
| `merged-removable` | housekeeping | info | local-refs | `--all-safe` |
| `stale-worktree` | housekeeping | warning | worktree-registry | read-only |
| `pushed-unmerged` | informational | info | local-refs | none |
| `remote-ahead` | informational | info | local-refs | none |
| `merged-current` | informational | info | local-refs | none |
| `main-worktree` | informational | info | worktree-registry | none |
| `locked-worktree` | informational | info | worktree-registry | read-only |
| `merge-target-conflict` | informational | info | manifest | none |

The six default-branch findings (FR-041) carry no suggestion whatever this
table says, and none sets the row's `suggested_command`.

## Messages

Every text the overview prints, one entry each; a held item edits only its
own entries.

### Composer (A1 design D5; research.md R12)

`compose_message(own, remedy, warning=None)` returns the message of a
finding whose suggestion a gate withheld or limited: own text, `; `,
remedy, at most 200 characters; when both do not fit, the own text is cut
and ends `...`, the remedy whole. Every other finding's message is its own
text alone. Two held clauses apply only with `warning` given (a
`stale-worktree` message that carries the warning of O6):

- clause 1, HELD (O6): the warning is kept whole and the recommendation
  before it is cut instead; D5's "remedy kept whole" stands;
- clause 2, HELD (O4, with O6): where the warning and the remedy cannot
  both fit, which only the redirect remedy reaches (under O4 (a) through
  its new row, and under O4 (b) through sub-item (c)'s row), the
  recommendation is left out and the remedy cut with `...`, reversing
  D5's "remedy kept whole" for that one case.

### Row and scan errors (FR-022; A1:392-403)

OPERATION is `git SUBCOMMAND` (`git rev-parse`, `git worktree list`, `git
config`, `git for-each-ref`, `git status`), a filesystem call (`lstat`,
`stat`, `realpath`, `scandir`, `read`) or `collection`.

- `error.manifest-invalid`: "manifest is invalid (CAUSE)", CAUSE one of
  STRERROR (a manifest that cannot be read), "not valid UTF-8 text",
  "malformed", "wrong kind", "over the 1 MiB size bound", "PyYAML is not
  installed"
- `error.refused.enclosing`: "Git did not accept the candidate's .git and
  reported an enclosing repository"
- `error.refused`: "a shared check refused this candidate"
- `error.os-error`: "OPERATION failed: STRERROR"
- `error.undecodable-output`: "OPERATION printed output that could not be
  decoded"
- `error.internal-error`: "internal error (CLASS)"
- `error.probe-failed`: "OPERATION failed: DETAIL", DETAIL one of "exit N",
  "signal N", "cannot spawn (STRERROR)", "unparseable output"
- `error.probe-timeout`: "OPERATION timed out after S s"
- `error.deadline-exceeded`: "OPERATION stopped at the invocation deadline"
- `error.scan-limit`: "LIMIT cap of M reached"
- `error.root-unreadable`: "root is unreadable (CAUSE)", CAUSE one of "no
  such directory", "not a directory", STRERROR

### Findings from the ladder (FR-028; [L], `project:2328-2348`)

The class's recommendation, verbatim:

- `finding.stale-worktree`: "Review and prune stale worktree metadata
  manually."
  - HELD (O6): while any worktree row of the same repository has
    `present: null`: "Review and prune stale worktree metadata manually;
    a row's path could not be read, so do not run git worktree prune until
    it can."
  - HELD (O8): for a locked row, feature 004's "Review, unlock it, then
    prune stale worktree metadata manually.", with the same warning under
    O6's test; no text is drafted for change 2.
- `finding.inspection-error`: "Preserve this worktree; Git could not
  establish its clean state."; its second rung: "Preserve this worktree;
  Git could not establish its ignored-file state."
- `finding.dirty`: "Preserve or commit the working changes before cleanup."
- `finding.ignored-local-files`: "Preserve or relocate ignored local files
  before cleanup."
- `finding.detached`: "Preserve the detached commit or attach it to a named
  branch before cleanup."
- `finding.unpublished`: "Push or otherwise preserve the branch before
  removing its worktree."
- `finding.remote-gone`: "Confirm the branch should be republished before
  removing local work."
- `finding.review-required`: "Remote tracking state could not be
  established from local refs; preserve it for review."; its second rung:
  "Merge state could not be established from local refs; preserve it for
  review."
- `finding.diverged`: "Reconcile the diverged branch through the normal Git
  workflow before cleanup."
- `finding.remote-ahead`: "Fetch and reconcile the newer remote branch
  before cleanup."
- `finding.unpushed`: "Use an explicit clean push, then continue through
  the normal review process."
- `finding.merged-removable`: "This clean, merged, non-current worktree may
  be removed explicitly."
- `finding.merged-current`: "The branch is merged, but this is the current
  checkout; switch away before removal."
- `finding.pushed-unmerged`: "Continue through the repository's normal
  pull-request or merge process."

`protected-default` has no finding of its own (FR-028).

### Default-branch findings (FR-041; A1 design D4)

- `finding.default.dirty`: "Uncommitted work on the merge-target branch;
  preserve it before updates."
- `finding.default.unpublished`: "merge-target branch has no upstream;
  local commits are unverified"
- `finding.default.remote-gone`: "merge-target branch's upstream is gone;
  local commits are unverified"
- `finding.default.diverged`: "merge-target branch and its upstream have
  diverged; reconcile through the normal Git workflow."
- `finding.default.unpushed`: "merge-target branch is ahead of its
  upstream; push through the repository's normal process."
- `finding.default.remote-ahead`: "merge-target branch is behind its
  upstream as of the last fetch."

### Other findings (PN-1; A1 design D3)

- `finding.unsupported-layout.submodule`: "submodule checkout, which
  project clean refuses; review it yourself"
- `finding.unsupported-layout.redirect`, HELD (O4 (b)): "core.worktree or
  core.bare redirects the main worktree; unset both in the repository's
  config, or in the main worktree's config.worktree, then run again", no
  suggestion
- `finding.unsupported-layout.gitfile`: "The checkout of this git directory
  cannot be named; set core.worktree or move the checkout"
- `finding.main-worktree-missing`: "The main worktree is missing; restore
  or prune the main worktree by hand"
  - HELD (O7): while any worktree row of the same repository has
    `present: null`: "The main worktree is missing; restore or prune the
    main worktree by hand; a row's path could not be read, so do not run
    git worktree prune until it can"
- `finding.main-worktree`: "The main worktree is never removed by project
  clean." (feature 004's text, `project:864`)
- `finding.locked-worktree`: "This worktree is locked; unlock it before
  project clean can remove it."
- `finding.registration-mismatch`: "Git's registration of this worktree
  does not match its directory; review it with git worktree list before
  any cleanup."
- `finding.unsupported-path-bytes.worktree`: "This worktree's path is not
  valid UTF-8, so no clean command can name it; rename it to valid UTF-8."
- `finding.unsupported-path-bytes.repository`: "The repository's root or
  common directory is not valid UTF-8, so no clean command can name it;
  rename the path to valid UTF-8."
- `finding.no-merge-target`: "Cannot determine the default branch from the
  manifest, origin/HEAD, main, or master." (feature 004's, `project:883`),
  where change 1's `resolve_merge_target` refuses `no-merge-target`
- `finding.merge-target-conflict`: "The manifest names NAME and origin/HEAD
  names OTHER; NAME is the merge target." (feature 004's,
  `project:842-843`), where that resolver's `notes` holds the conflict;
  NAME and OTHER are escaped for the output's mode (FR-038)

### Remedies (FR-035; A1:620-631)

N is the repository's worktree-row count (every registry entry) and M read
from `limits` when the message is built.

- `remedy.target-not-repository-root`: "run project clean from the main
  worktree root"
  - HELD (O4 (a)), for a redirected main worktree, and (O4's sub-item
    (c), under (a) or (b)) for a bare entry whose path joined with `/.git`
    is `common_dir`: "core.worktree or core.bare redirects the main
    worktree; unset both in the repository's config, or in the main
    worktree's config.worktree, then run again"
- `remedy.unsupported-path-bytes`: "rename the path to valid UTF-8"
- `remedy.inspection-incomplete`: "repair the inspection-error rows, or
  re-run for the rows left unprobed, first"
- `remedy.inspect-cap.batch` (withheld): "N rows exceed the batch's row cap
  of M; remove explicitly"
- `remedy.inspect-cap.report` (limited): "N rows exceed the report's row
  cap of M; the report would be incomplete"
- `remedy.scan-limit`: "re-run with --root <repository parent>",
  `<repository parent>` the parent of `repository.root`, escaped by [P]
- `remedy.deadline-exceeded`: "re-run with --root <repository parent>"
  - HELD (O2 (A)): also the gate of a row whose reflog read the deadline
    cut, in place of `inspection-incomplete`
- `remedy.unstarted-branch`: "no commit was made on this branch here since
  it was created; review, then git worktree remove yourself"
  - HELD (O1 (A)): "no commit was made on this branch here since it was
    created; review, then git worktree remove yourself (--force if it holds
    a submodule)"
- `remedy.reflog-unavailable`: "the branch's reflog is missing, expired or
  undecidable; review, then git worktree remove yourself"
  - HELD (O1 (A)): "the branch's reflog is missing, expired or
    undecidable; review, then git worktree remove yourself (--force if it
    holds a submodule)"
- `remedy.target-cap` (limited): "limited to the batch's target limit of M
  per run; re-run to drain the backlog"

### Fixed lines (A1 design D10; FR-039, FR-043, FR-044, FR-046)

- `line.summary`: "N projects; E errors; repair A, preserve B, housekeeping
  C, informational D. Findings reflect local refs as of the last fetch."
- `line.summary.nothing`: "Nothing needs attention: " followed by
  `line.summary`, under `--attention` with no row shown
- `line.all-absent`: "No projects directory found; pass --root D or set
  PROJECTS_DIR."
- `line.incomplete-path`: "Incomplete: PATH: MESSAGE (CODE)."
- `line.incomplete`: "Incomplete: MESSAGE (CODE)."
- `line.scanning` (stderr): "Scanning N roots..."
- `line.cancelled` (stderr): "Cancelled."
- `line.refused` (stderr): "REFUSED: MESSAGE"
- `line.write-failed` (stderr; PN-2): "Cannot write the report to standard
  output (STRERROR)."
- `refusal.git-too-old`: "Git VERSION is older than 2.36; overview needs
  Git 2.36 or later."
- `refusal.git-unavailable`: "Git is unavailable (DETAIL); overview needs
  Git 2.36 or later.", DETAIL one of "not found", "exit N", "timed out",
  "unparseable version" (feature 004's details, `project:812-815`)
- `refusal.relative-config-path`: per failing variable, in the order
  `HOME`, `XDG_CONFIG_HOME`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`, one
  line "NAME is set to a path that does not begin with /; make it absolute
  or unset it.", the lines joined by a line feed (feature 004's
  `config_path_message`, `project:1003-1006`)
- `refusal.internal-error` (PN-2): "internal error (CLASS)"
