Lane: openRepoProject-4

# Feature Specification: Project overview

**Feature Branch**: `005-project-overview`

**Created**: 2026-10-11

**Status**: Draft. Created before feature 004 merges, on Brett Heap's word
(below); the plan and the implementation wait for feature 004's code and for
his word.

**Input**: User description: "Realize the ratified OpenSpec change
add-project-overview: a read-only `project overview [--root D]...
[--attention] [--json] [--strict]` answers which local projects need
attention across the configured roots, with at most one gated next command
per row (opensoft/openRepoProject#10)."

**Source of truth**: `openspec/changes/add-project-overview/` (proposal; spec
deltas for `project-overview`, 12 ADDED requirements and 61 scenarios, and
`project-review-safety`, one MODIFIED requirement with 2 scenarios; design
D1 to D13; clarifications N1 to N4), ratified by Brett Heap on 2026-10-09 in
his words to lane openRepoProject-2, "ratify, merge #11 and run the runbook"
(proposal, Status; governance task 1.6), landed on main by squash as
`961c405` (PR #12). Where this summary is shorter than the deltas, the deltas
govern. Exact human text is fixed in the delta's remedy table and in design
D3, D4, D5 and D10, and is cited, never restated in another form.

**Citations**: `POD:N` is line N of the change's
`specs/project-overview/spec.md`, and `PRSD:N` line N of its
`specs/project-review-safety/spec.md`, both at `961c405`; requirement and
scenario names are the deltas' headers. Change 1,
`add-project-clean-all-safe`, is cited by requirement header under the
change's labels: [E] "Repository inspection requires Git 2.36 and shares one
evidence model" (project-command); [L] "Clean classifies preservation and
cleanup actions"; [G] "Clean previews and applies a batch of eligible
worktree removals in one repository" with "Clean bounds its Git work and
reports omitted work"; [R] "Clean resolves its target Git-first"; and [P]
"Clean reports every path exactly or excludes it" (all project-clean).
Feature 004's names for the same concepts (classifications, gate reasons,
refusal and row error codes, `omitted`, `schema_version`, exit statuses) are
used unchanged, cited from `specs/004-project-clean-all-safe/` (`spec.md`,
`data-model.md`, `contracts/project-clean.md`) at `dd923ee` on branch
`004-project-clean-all-safe`, whose plan is still under review. The change
pins its code citations at `da33d92`; this spec cites no line of `project`,
and the plan re-pins them against the `main` of its day (proposal,
"Dependencies and Sequencing").

**Created before feature 004 merges**: The change creates this feature only
after feature 004 merges (proposal, Status and "Dependencies and
Sequencing"; `tasks.md` 3.1 and "Speckit Handoff"; design, "Migration Plan"
step 3). Brett Heap's word, typed in lane openRepoProject-4's pane at
2026-10-11T16:14:21Z, "lane 4 specifies 005 now", recorded by that lane as a
RULED line at 16:15:00Z, moves that order for this specify step only. The
plan and the implementation still wait for feature 004's code and for his
word. Lane openRepoProject-2 released issue #10 at 16:17:06Z, and lane
openRepoProject-4 claimed it
(https://github.com/opensoft/openRepoProject/issues/10#issuecomment-6111064469).

**Relations to earlier features**: `project overview` is a new subcommand;
no earlier feature specified it. It absorbs the doctor repository health of
the closed, unmerged PR #2 (`acf0133`, `80fdef3`) as local-only, read-only
reporting, and supersedes that branch's unmerged
`project-doctor-repository-health` capability (proposal, "Absorbing Doctor
Repository Health from the Closed PR #2"). Features 001 to 003 are
untouched. Feature 004 builds the shared evidence model this feature reads
and changes `clean`, `status`, `doctor` and `update`; this feature changes
no other subcommand's output, flags or exits. The capability this feature
MODIFIES is `project-review-safety`, not change 1's
`project-clean-review-safety`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - See every local project in one report (Priority: P1)

A person with dozens of repositories under their projects directory runs
`project overview` and reads one row per project, each with its absolute
path, each repository once however many of its worktrees sit under a root
or elsewhere, with every registered worktree listed under it. Today
`status`, `doctor` and `clean` each inspect one selected project, and the
person correlates them by hand (proposal, "Why").

**Why this priority**: It is the change's purpose, the packet's question
"Which of my local projects needs attention?" (issue #10).

**Independent Test**: In a temporary root, build independent clones, a
symbolic-link alias, a family holder and a repository with linked worktrees
inside and outside the root; run human and `--json`, and check the rows, the
worktree rows and the probe count.

**Acceptance Scenarios**:

1. **Given** clones of one origin at `atlas` under root A and at `atlas`
   under root B, and a symbolic link `atlas-link` in A to its `atlas`,
   **When** both roots are given with `--root`, **Then** there are exactly
   two `atlas` rows whose `repository` `common_dir`, `dev` and `ino`
   differ, the link adds no row, and each human row prints its absolute
   path.
2. **Given** a root holding `acme/acme/family.yaml` in a Git toplevel that
   declares members at `acme/web` and `acme/api`, plus an ordinary
   repository `tools`, **When** the overview runs, **Then** there are
   exactly two rows, a `family-holder` at `acme/acme` and `tools`,
   `summary.projects` is 2, `relationships` is `[]`, no row and no Git
   child exists for either member, and the holder's repository-wide probes
   run once and belong to its row; without `acme/acme/.git` the holder row
   has null `repository`, `merge_target`, `git` and `worktrees`, status
   `ok`, no error and no Git child; and with `acme` itself as the root,
   `web` and `api` are rows of their own and `relationships` stays `[]`.
3. **Given** a repository with a main worktree and three linked worktrees,
   one an immediate entry of the root and one outside every root, **When**
   the overview runs, **Then** there is one project row with four worktree
   rows, main worktree first and then by path bytes, the external worktree
   adds no project, the identity probe, the registry, the ref listing and
   the merged-set query run once for the repository, each present row gets
   one status probe, and `probes.performed` is one version check, plus one
   identity probe per Git candidate, plus three, plus four; when the main
   worktree lies outside every root, so that a linked worktree reaches the
   repository first, `repository.root` is the canonical path of the first
   registry record, never that linked worktree's toplevel.
4. **Given** that external worktree is clean, pushed and merged, with a
   commit of its own, **When** the overview runs, **Then** it appears among
   its repository's worktrees with `dev`, `ino` and a two-way-verified
   `admin_id`, classification `merged-removable` and a housekeeping
   finding, the suggestion is `project clean <atlas root> --all-safe`, and
   the project count is unchanged.
5. **Given** that external worktree's directory was deleted without `git
   worktree prune`, **When** the overview runs, **Then** its row has
   `present: false`, classification `stale-worktree` and a housekeeping
   warning suggesting the read-only `project clean <atlas root>`, no probe
   runs in the missing path, and the exit status is 0, or 1 with
   `--strict`.
6. **Given** no `--root`, `PROJECTS_DIR` unset and neither default projects
   directory present, **When** the overview runs, **Then** both roots are
   reported `absent` with no scan error, the result is complete, the exit
   status is 0, and the human output says that no projects directory was
   found and names `--root` and `PROJECTS_DIR`.
7. **Given** standard error on a terminal, and again on a pipe, **When** the
   overview runs, **Then** the first run writes one `Scanning N roots...`
   line to standard error before listing and the second writes none, and
   standard output is identical in both runs.
8. **Given** `--root` naming one project's own directory, **When** the
   overview runs, **Then** that directory is itself examined as a
   candidate, together with its immediate entries, so the project is
   reported (Clarifications, C-1).

**Delta scenarios**: "Independent clones and aliases"; "Family holder
count, relationships and probe ownership"; "One probe set per repository";
"Present eligible external worktree"; "Missing external worktree"; "Every
root is absent"; "The scanning notice".

---

### User Story 2 - Only what needs attention, and an exit that says so (Priority: P1)

The person wants to read only what needs action, and a script wants an exit
status it can trust. Every finding carries one code, one category (repair,
preserve, housekeeping or informational) and one severity; `--attention`
hides the projects with nothing to do and the informational findings, and
changes neither the JSON, the summary nor the exit. A merged worktree whose
upstream was deleted is housekeeping like any merged worktree, by Brett
Heap's ruling of 2026-10-09 that local ancestry proof outranks
`remote-gone`.

**Why this priority**: "Ordinary work is not trouble" and "Incomplete is
visible" (proposal, "Rules This Change Keeps"); without the categories and
the exit rule, the report is a listing, not an answer.

**Independent Test**: Build four projects with one finding each, run with
and without `--attention`, `--json` and `--strict`, and compare what is
shown, the JSON and the exit statuses.

**Acceptance Scenarios**:

1. **Given** four projects whose only findings are `pushed-unmerged`,
   `unpushed`, `merged-removable` and `no-merge-target`, **When** `project
   overview` and `project overview --attention` each run with and without
   `--json`, **Then** `--attention` hides the informational-only project
   and shows the other three under their categories, the two JSON documents
   are identical apart from their timestamps, and every run exits 1;
   without the repair project every run exits 0, and with `--strict` every
   run exits 1 because of the preserve warning.
2. **Given** a clean linked worktree whose branch, with a commit of its own,
   is an ancestor of the merge target and whose upstream branch was deleted
   and pruned, **When** the overview runs, **Then** it is `merged-removable`,
   as `project clean <root> --json` classifies it, with the housekeeping
   finding whose message is the ladder's `merged-removable` recommendation,
   suggests `project clean <root> --all-safe`, and no Git child beyond the
   shared probe set ran for it; a worktree whose upstream branch was
   deleted and pruned and whose tip is not an ancestor is `remote-gone`,
   with a preserve warning carrying the ladder's own `remote-gone`
   recommendation, and suggests only the read-only `project clean <root>`.
3. **Given** projects whose only findings are informational, **When**
   `project overview --attention` runs, **Then** no row is shown, the
   summary line says that nothing needs attention, gives the counts and
   states that findings reflect local refs as of the last fetch, and the
   exit status is 0.
4. **Given** a row error and a scan error, **When** `--attention` runs,
   **Then** both are shown, in the repair category, and neither is counted
   as a finding.

**Delta scenarios**: "Attention filter per category"; "A merged worktree
whose upstream was deleted"; "Nothing needs attention".

---

### User Story 3 - The same verdict `project clean` would give (Priority: P1)

The overview never second-guesses `project clean`. It classifies each
worktree with the same ladder over the same evidence and resolves the same
merge target, so a person who follows a suggestion sees the same picture in
the plan it leads to.

**Why this priority**: "One classifier, one evidence model" (proposal,
"Rules This Change Keeps"); every suggestion relies on it.

**Independent Test**: Build the merge-target fixtures and the repository of
"Every protected classifier", and compare each row's `merge_target` and
each worktree's classification with `project clean <root> --json` run from
the same directory at the same commit.

**Acceptance Scenarios**:

1. **Given** a `project.yaml` with `tracking_branch: origin/develop`, a
   local `develop` and no `origin/HEAD`, **When** the overview runs,
   **Then** `merge_target` is `develop` with source `manifest` and the
   object id of `refs/heads/develop`, classification is relative to it, the
   merged set was computed at that object id, resolution spawned no Git
   child beyond the ref listing, and the name equals the merge target that
   `project clean <root> --json` reports.
2. **Given** no manifest, `origin/HEAD` naming `origin/trunk`, and local
   `trunk` and `main`, **When** the overview runs, **Then** the target is
   `trunk` with source `origin-head` and the object id of
   `refs/heads/trunk`.
3. **Given** no manifest and no `origin/HEAD`, with local `main` and
   `master`, or with only a local `master`, **When** the overview runs,
   **Then** the target is `main` with source `main`, or `master` with
   source `master`, and that branch's object id.
4. **Given** a manifest naming `develop` and `origin/HEAD` naming `main`,
   both existing locally, **When** the overview runs, **Then** the target is
   `develop` with source `manifest`, one informational
   `merge-target-conflict` finding names both branches, and the exit status
   is 0 when nothing else is found.
5. **Given** a manifest naming an absent `release`, no `origin/HEAD`, and
   neither `main` nor `master`, **When** the overview runs, **Then**
   `merge_target` is null, the row has a `no-merge-target` repair finding of
   severity error with no suggested command, every worktree's
   classification is null, and the exit status is 1; on the same fixture
   `project clean <root> --all-safe` refuses with exit status 2 before any
   mutation.
6. **Given** one repository whose worktrees are classified
   `protected-default`, `dirty`, `ignored-local-files`, `detached`,
   `unpublished`, `remote-gone`, `diverged`, `remote-ahead`, `unpushed`,
   `merged-current` and `pushed-unmerged`, plus one gate-passing
   `merged-removable`, and a second repository holding an
   `inspection-error` worktree whose corrupted index makes its status probe
   fail, **When** the overview runs from inside the `merged-current`
   worktree, **Then** every classification equals what `project clean
   <root> --json` reports from the same directory, each finding has the
   category and severity of the attention table, and the only housekeeping
   finding and the only `--all-safe` suggestion belong to the
   `merged-removable` worktree, the only worktree in the `selected` list of
   the batch preview that suggestion runs.

**Delta scenarios**: "Manifest target"; "origin/HEAD target"; "main
target"; "master target"; "Conflicting targets"; "Missing target"; "Every
protected classifier".

---

### User Story 4 - A next command to review, never permission (Priority: P1)

Each row offers at most one next command, an argument vector naming the
repository's absolute root: `project clean <root> --all-safe` only for a
merged worktree that passes the batch gates the overview can evaluate from
its own evidence, otherwise the read-only `project clean <root>`, and never
`--apply`, `--yes` or a bare name. When a gate withholds or limits a
suggestion, the finding names the gate and the person reads its remedy.
`project clean` still recomputes, shows and confirms its own plan.

**Why this priority**: "Evidence is not permission" (proposal, "Rules This
Change Keeps"); a suggestion must never point at what `project clean`
refuses.

**Independent Test**: Build gated worktrees, seventeen eligible ones, 130
and 260 registered rows, a row the worktree-row cap leaves unprobed and the
reflog fixtures; check `suggested_command`, `suggestion_gate`,
`suggestion_gate_rows`, the messages and the human `next` line, and run the
suggested command's preview.

**Acceptance Scenarios**:

1. **Given** four worktrees the ladder would classify `merged-removable`,
   one locked with `git worktree lock`, one whose `.git` file names another
   administrative directory, one whose path contains the byte `0xFF`, and
   the main worktree checked out on a merged non-target branch while the
   overview runs elsewhere, **When** the overview runs, **Then** the locked
   one has a `locked-worktree` finding suggesting the read-only `project
   clean <root>`, the mismatched one gets no status probe and is
   `inspection-error` with a `registration-mismatch` finding, the non-UTF-8
   one has `unsupported-path-bytes`, the main worktree has `main-worktree`,
   and none produces a housekeeping finding; a fifth, gate-passing
   `merged-removable` worktree in the same repository keeps its
   housekeeping finding with the read-only suggestion and
   `suggestion_gate: "inspection-incomplete"`, and the row suggests the
   read-only form; after `git worktree repair` fixes the registration, the
   `--all-safe` suggestion returns and the batch preview selects the
   repaired worktree, whose branch has a commit of its own, and the fifth.
2. **Given** projects named `atlas` under two roots, each with a
   `merged-removable` worktree whose branch has a commit of its own,
   **When** the overview runs, **Then** the rows suggest `["project",
   "clean", "<first atlas root>", "--all-safe"]` and `["project", "clean",
   "<second atlas root>", "--all-safe"]`, and each, when run, resolves its
   path Git-first to a plan whose `repository` and `merge_target` equal
   that row's; for an assembly root with a `project.yaml` whose
   immediate-entry leg `api` is its own repository with one dirty and one
   such `merged-removable` worktree, the leg's row suggests `--all-safe` on
   the leg's root, its `dirty` finding suggests the read-only form, and
   either reports `root` equal to the leg; the same command with a
   linked-worktree path or a subdirectory instead of the root is refused by
   `project clean` with exit status 2 and `target-not-repository-root`
   before any mutation.
3. **Given** one repository with 17 gate-passing `merged-removable`
   worktrees and the batch's target limit at 16, **When** the overview runs,
   **Then** each of the 17 findings and the row suggest `--all-safe` with
   `suggestion_gate: "target-cap"` and a message ending "limited to the
   batch's target limit of 16 per run; re-run to drain the backlog", the
   human `next` line ends `(limited: ...)` with that remedy, and the exit
   status is 0.
4. **Given** one repository with 130 worktree rows, the batch's row cap at
   128 and the report's at 256, including a gate-passing `merged-removable`
   worktree and a `dirty` one, **When** the overview runs, **Then** the
   `merged-removable` finding suggests the read-only form with
   `suggestion_gate: "inspect-cap"`, `suggestion_gate_rows: 130` and the
   remedy "130 rows exceed the batch's row cap of 128; remove explicitly",
   and the `dirty` finding's read-only suggestion carries no gate; in a
   repository with 260 worktree rows every read-only suggestion carries
   `suggestion_gate: "inspect-cap"`, `suggestion_gate_rows: 260` and the
   remedy "260 rows exceed the report's row cap of 256; the report would be
   incomplete".
5. **Given** the worktree-row cap leaves one row of a repository
   unclassified while another of its worktrees is gate-passing
   `merged-removable`, **When** the overview runs, **Then** that finding
   suggests the read-only form with `suggestion_gate: "scan-limit"` and the
   remedy "re-run with --root <repository parent>", naming the repository's
   parent directory.
6. **Given** a linked worktree created with a new branch at the merge
   target's tip and published with `git push -u`, with no commit of its
   own, so that its reflog holds only its `branch: Created from` entry,
   **When** the overview runs, **Then** it keeps its `merged-removable`
   finding, which suggests only the read-only form with `suggestion_gate:
   "unstarted-branch"` and a message ending "no commit was made on this
   branch here since it was created; review, then git worktree remove
   yourself", and no `--all-safe` suggestion is given for the repository on
   its account; after `git branch -m` it is still `unstarted-branch`; so
   are a branch with commits of its own that `git worktree add -B` reset to
   the target's tip with no commit after, and a branch created by `git
   fetch origin feat:f1` at the target's tip and given an upstream by `git
   branch -u origin/feat f1`; and a branch given one commit and then
   fast-forward merged into the target, its head equal to the target's tip,
   keeps the `--all-safe` suggestion with no gate.
7. **Given** gate-passing `merged-removable` worktrees whose branches have,
   in turn, no reflog file, an empty reflog file, a reflog expired to a lone
   rename entry, and a reflog recording a commit of their own after which
   the ref was moved directly to another merged commit, **When** the
   overview runs, **Then** each keeps its finding, which suggests only the
   read-only form with `suggestion_gate: "reflog-unavailable"` and a message
   ending "the branch's reflog is missing, expired or undecidable; review,
   then git worktree remove yourself", no Git child reads any reflog, and
   `project clean <root> --all-safe` excludes all four as
   `reflog-unavailable`; in a second repository, a worktree whose reflog
   cannot be read for a permission error records an `os-error` and is
   `inspection-error`, and another gate-passing worktree there suggests
   only the read-only form with `suggestion_gate: "inspection-incomplete"`.
8. **Given** a repository holding a gate-passing `merged-removable` worktree
   and another worktree whose status probe failed, **When** the human
   report prints, **Then** the row's `next` line carries `project clean
   <root>` followed by `(withheld: repair the inspection-error rows, or
   re-run for the rows left unprobed, first)`, and the finding lines show
   the repair finding and the housekeeping finding with their worktree
   paths.

**Delta scenarios**: "Gated merged worktrees"; "Canonical identity through
the handoff"; "More eligible worktrees than the batch's target limit"; "The
two inspect-cap bands"; "A row left unprobed closes the repository gate";
"An unstarted branch"; "A branch whose reflog cannot decide"; "A gated
suggestion".

---

### User Story 5 - Every run is bounded and says what it omitted (Priority: P2)

An estate with hundreds of repositories, a hung mount or a huge index must
neither hang the overview nor be half-read in silence. Every run has one
60 s deadline, a 5 s budget per Git child and per filesystem call, fixed
caps and at most four Git children at once; every cut is reported with what
it omitted and how exactly that is known, and the result is then
incomplete and exits 1.

**Why this priority**: Bounds keep the report predictable, yet most estates
fit them: governance task 2.1 measured the caps' worst case at 48.3 s of
the 60 s deadline.

**Independent Test**: Under a counting `git` wrapper that can hold a status
probe and with injected slow filesystem calls, build 130 candidates, a root
of 4,100 entries, 33 roots, 520 worktree rows, 10,000 ignored files and a
manifest over 1 MiB, and compare completeness, `omitted`, exit statuses,
the process table and the JSON at probe concurrency 1 and 4.

**Acceptance Scenarios**:

1. **Given** one root holding 130 candidate directories `p000` to `p129`,
   created in reverse order, **When** the overview runs, **Then** the rows
   are `p000` to `p127` whatever the listing order, one `scan-limit` scan
   error has `limit: "candidates"` and `omitted: {"count": 2,
   "exactness": "exact"}`, the result is incomplete and the exit status is
   1; given also a second root of 4,100 entries, that root is `truncated`
   with a `root_entries` `scan-limit` error whose count is null with
   exactness `unknown`, and the candidate-cap error reports the known excess
   with exactness `lower-bound`.
2. **Given** 33 distinct roots, or repositories totalling 520 worktree rows,
   **When** the overview runs, **Then** the last root in canonical order is
   `omitted` with an exact omitted count of 1; and the first 512 worktree
   rows in rank order are probed on every run whatever the completion
   order, the other 8 keep registry and branch evidence with `dirty`,
   `ignored_files` and `classification` null, their project rows carry
   `scan-limit` errors, the scan error has `limit: "worktree_rows"` and
   `{"count": 8, "exactness": "exact"}`, and the exit status is 1.
3. **Given** one worktree's status probe held for 10 s by the counting
   `git` wrapper, **When** the overview runs, **Then** that child is stopped
   at 5 s and reaped, its row records `probe-timeout` with `dirty: null`
   and classification `inspection-error`, every other row is complete, and
   the exit status is 1.
4. **Given** the `lstat` of an external worktree's path, the canonicalising
   or listing of one `--root`, or every filesystem call on a repository's
   main checkout takes 10 s, on a fixture mount where one can be made and
   by an injected slow call otherwise, **When** the overview runs, **Then**
   each such call is abandoned at 5 s with `probe-timeout` on its row or
   root, a cut root counts as `truncated` and none of its entries is read
   after the cut, every other row is complete, the run ends within the
   deadline, and the exit status is 1.
5. **Given** enough held probes to exceed 60 s, **When** the overview runs,
   **Then** no child starts after the deadline, every in-flight child is
   terminated, reaped within the grace and recorded `deadline-exceeded`,
   unstarted candidates appear as rows with `deadline-exceeded`, the scan
   error's omitted count is exact, and the process exits 1 within 64 s plus
   rendering.
6. **Given** eight single-worktree repositories whose status probes the
   counting `git` wrapper holds for 1 s each, **When** the overview runs,
   **Then** the process table never shows more than four of its Git
   children at once, nor two with the same `common_dir`, and the eight held
   probes take about 2 s rather than 8 s.
7. **Given** one fixture whose worktree rows exceed the worktree-row cap,
   **When** it is collected at probe concurrency 1 and at 4 and no budget or
   deadline is reached, **Then** the two JSON documents are byte-identical
   apart from timestamps and `budget.probe_concurrency`, and the same rows
   are probed.
8. **Given** a clean merged worktree holding 10,000 ignored files, **When**
   the overview runs, **Then** the status stream stops early,
   `ignored_files` is 64 with `ignored_files_truncated: true`,
   `ignored_samples` has eight entries, `dirty` is false and the
   classification is `ignored-local-files`, a preserve finding; exactly 64
   ignored files give `ignored_files_truncated: false`; and 4,097 untracked
   files with no ignored one stop the stream at the record bound with
   `dirty` true, `ignored_files` null and classification `dirty`, not
   `inspection-error`.
9. **Given** the user's Git configuration sets
   `status.showUntrackedFiles=no` and a linked worktree is clean, pushed
   and merged, **When** the overview runs, **Then** the status probe
   succeeds, `ignored_files` is 0 and the worktree is `merged-removable`.
10. **Given** a candidate's `project.yaml` larger than the manifest size
    bound, **When** the overview runs, **Then** its row carries a
    `manifest-invalid` error naming the manifest and the bound, the file is
    neither read nor parsed, the other rows are complete, and the exit
    status is 1.

**Delta scenarios**: "Candidate cap after sorting, with an exact count";
"Candidate cap with an incomplete listing"; "Root and worktree-row caps";
"Probe timeout"; "Hung filesystem call on an external worktree";
"Invocation deadline"; "Bounded concurrency"; "The JSON does not depend on
concurrency"; "Bounded ignored files"; "User status configuration"; "A root
on a hung mount"; "A repository root on a hung mount"; "A manifest over the
size bound".

---

### User Story 6 - One project's failure stays in its row (Priority: P2)

An unreadable directory, a malformed or wrongly typed manifest, a manifest
whose text is not valid UTF-8, a missing YAML library or a failing Git
child becomes data on that candidate's row. Every other row is collected and
printed, no traceback appears, and the run exits 1, not 2. For a manifest
with an invalid text encoding this is the one exception the overview makes
to the review-safety rule that every other command keeps.

**Why this priority**: One broken project must not hide the others, but the
common case is a healthy estate.

**Independent Test**: Put an unreadable candidate, a wrong-kind manifest, an
invalid-UTF-8 manifest and an unsearchable external worktree beside healthy
projects, run with and without `--json` and without the YAML library, and
check that every healthy row is unchanged and the exit status is 1.

**Acceptance Scenarios**:

1. **Given** one root holding candidates `alpha`, `locked` and `zeta`, with
   `locked` at mode 000, and a second `--root` that cannot be listed,
   **When** the overview runs, **Then** `locked` appears in its sorted
   position with `path` the candidate path, `name` `locked`, `kind` null,
   status `error`, `findings` empty, one `os-error` naming its path and
   every Git-derived field null, `alpha` and `zeta` are complete, the
   second root adds a `root-unreadable` scan error, and the exit status is
   1, never 2.
2. **Given** an external worktree whose parent directory is made
   unsearchable, so that `lstat` fails with a permission error, **When** the
   overview runs, **Then** the worktree has `present: null` and
   classification `inspection-error`, the project row has an `os-error` and
   status `error`, the other rows are reported, and the exit status is 1;
   when instead only that worktree's status probe fails, the row records
   `probe-failed` and is `inspection-error`.
3. **Given** a root holding `alpha`, `ledger` and `zeta`, where
   `ledger/project.yaml` declares `kind: other`, **When** the overview runs,
   **Then** `alpha` and `zeta` are complete, `ledger` appears in its sorted
   position with status `error`, a `manifest-invalid` error, its repository
   identity retained, and null `merge_target`, `git` and `worktrees`, and
   the exit status is 1.
4. **Given** the overview runs without the YAML library over `alpha`, with
   only a `.git` directory, and `ledger`, with a `project.yaml`, **When** it
   runs, **Then** `ledger` carries a `manifest-invalid` error naming the
   missing library, `alpha` is complete with no error, and the exit status
   is 1.
5. **Given** `ledger/project.yaml` contains invalid UTF-8 bytes beside
   `alpha` and `zeta`, **When** `project overview --json` runs, **Then**
   `ledger`'s row has status `error` and one `manifest-invalid` error naming
   that manifest, with no traceback, `alpha` and `zeta` are complete, the
   JSON document is printed, and the exit status is 1, not 2.
6. **Given** a project or family manifest containing invalid UTF-8 bytes,
   **When** `project status --json` reads it, **Then** status still refuses
   with structured JSON error output, exit status 2 and no traceback, as
   before this feature.

**Delta scenarios**: "Unreadable candidate directory"; "Unreadable external
worktree"; "One helper failure is isolated"; "The YAML library is not
installed"; "Overview keeps a manifest with invalid text in its row"; and
the kept canonical scenario "Manifest is not valid UTF-8 text".

---

### User Story 7 - Unusual layouts are named, never guessed (Priority: P2)

Submodule checkouts, bare repositories, checkouts made with a separate git
directory and repositories whose main worktree was deleted are reported
truthfully: the overview names the main checkout as `project clean` would
resolve it, or says why it cannot and gives no clean suggestion, so it
never suggests what `project clean` refuses.

**Why this priority**: These layouts are rare, but a wrong root in a
suggestion would send the person to a refusal or the wrong repository.

**Independent Test**: Under a root, place a `--separate-git-dir` checkout
with and without its checkout among the candidates, a submodule checkout, a
repository whose main worktree was deleted and a linked worktree of a bare
repository, and check `repository.root`, the layout findings, the probe
directories and the suggestions.

**Acceptance Scenarios**:

1. **Given** a root holding the checkout of a repository created with `git
   init --separate-git-dir`, whose git directory has no `core.worktree`,
   **When** the overview runs, **Then** `repository.root` is that checkout,
   its main worktree row is status-probed there and reports its dirty
   state, and the git-directory record is never status-probed; when only a
   linked worktree of that repository is a candidate and its checkout is
   not, `repository.root` is null with an `unsupported-layout` repair
   finding of severity error and no suggestion, and the exit status is 1.
2. **Given** an immediate entry of a root that is a submodule's checkout,
   whose `core.worktree` is relative to its git directory, **When** the
   overview runs, **Then** its row has `repository.root: null` and an
   `unsupported-layout` repair finding of severity error whose message names
   a submodule checkout, no `core.worktree` child ran for it, it gets no
   clean suggestion, every finding's `suggestion_gate` is null, and the exit
   status is 1.
3. **Given** a repository whose main worktree directory was deleted while a
   linked worktree under the root remains, **When** the overview runs,
   **Then** the row has `repository.root: null`, the main worktree row has
   `present: false` and a `main-worktree-missing` repair warning, the
   repository-wide probes run in the linked worktree, and no clean
   suggestion is given.
4. **Given** a linked worktree of a bare repository is an immediate entry of
   a root, **When** the overview runs, **Then** the row has
   `repository.root: null` and no clean suggestion, each finding that would
   have suggested one naming `target-not-repository-root` in
   `suggestion_gate`, and its repository-wide probes run in the common
   directory.

**Delta scenarios**: "A separate git directory"; "A submodule checkout under
a root"; "A deleted main worktree"; "A bare repository with a linked
worktree".

---

### User Story 8 - The merge-target checkout's own health (Priority: P2)

The checkout of the merge-target branch is never a removal target, but
unverified local commits there still need attention. It keeps its
`protected-default` classification and gains every finding that applies,
not only the first: `dirty` when dirty, and at most one of `unpublished`,
`remote-gone`, `diverged`, `unpushed` or `remote-ahead`, each with no
suggested command. A repository with no remote copy of its merge target is
ordinary work and raises nothing.

**Why this priority**: It completes the closed PR #2's doctor health, which
its decision record assigned to this design; most merge-target checkouts
are healthy.

**Independent Test**: Build a `main` pushed without `-u` and then given two
commits, a repository with no remote, a dirty `main` three commits ahead,
and a `main` checkout whose status probe fails; check the findings, the
`--attention` display and the exit with and without `--strict`.

**Acceptance Scenarios**:

1. **Given** `main` was pushed with `git push origin main`, without `-u`,
   and then given two local commits, **When** the overview runs, **Then**
   its checkout stays `protected-default` and has an `unpublished` preserve
   warning with the message "merge-target branch has no upstream; local
   commits are unverified" and no suggested command, `project overview
   --attention` shows that row, and the exit status is 0, or 1 with
   `--strict`.
2. **Given** a repository with no remote, local commits on `main` and
   nothing else to report, **When** the overview runs, **Then** its checkout
   has no finding, `--attention` does not show the row, and the exit status
   is 0 with or without `--strict`.
3. **Given** the checkout of `main` is dirty and 3 commits ahead of its
   upstream, **When** the overview runs, **Then** it stays
   `protected-default` and carries both a `dirty` and an `unpushed` preserve
   warning, each with no suggested command.
4. **Given** the status probe of the checkout of `main` fails, **When** the
   overview runs, **Then** that row is `inspection-error` with a repair
   finding of severity error and the `probe-failed` error, it carries none
   of the default-branch findings, and the exit status is 1.

**Delta scenarios**: "A default branch pushed without an upstream"; "A
repository with no remote"; "A dirty default branch ahead of its upstream";
"A failed status probe on the default branch".

---

### User Story 9 - Local, read-only and stoppable (Priority: P2)

The overview never fetches, writes or connects anywhere; it refuses an old
or missing Git before listing anything; and when the person presses Ctrl-C,
or the terminal or a supervisor ends it, no Git child outlives it and no
partial document is printed.

**Why this priority**: Read-only is a rule the change keeps (proposal,
"Rules This Change Keeps"), and a scan across an estate must be safe to
interrupt; both matter less to the daily answer than the earlier stories.

**Independent Test**: Run over every fixture with networking disabled and
before-and-after snapshots; with Git 2.34.1 and with no `git` first on
PATH; and send SIGINT, SIGTERM and SIGHUP during collection at probe
concurrency 4 while one child hangs and another writes a large output.

**Acceptance Scenarios**:

1. **Given** any fixture of this feature and networking disabled for the
   process, **When** the overview runs with default options, **Then** it
   opens no network connection, the before and after snapshots of `git
   for-each-ref`, `git worktree list --porcelain -z`, each checkout's
   status, each index file's modification time and the directory tree under
   every root are identical, the JSON preserves severity, freshness,
   unknown values and completeness, and a complete scan that finds no
   project says so and exits 0.
2. **Given** `git` reports version 2.34.1, or no `git` is on PATH, **When**
   the overview runs, **Then** it exits 2 with code `git-too-old`, and a
   message naming the 2.36 minimum, or with code `git-unavailable`, before
   listing any root or starting any other Git child, and under `--json` it
   prints only `{"error": "<message>", "code": "<code>"}`.
3. **Given** one Git child hung and another writing a large output at probe
   concurrency 4, **When** SIGTERM is sent, **Then** the exit status is 143,
   no result document is printed, `Cancelled.` is printed to standard error
   when it can be, and every child's process group is gone; with SIGHUP the
   exit status is 129.
4. **Given** children running and a finding of severity error already
   collected, **When** SIGINT is sent, **Then** every in-flight child is
   terminated and reaped, no result document is printed, `Cancelled.` goes
   to standard error, and the exit status is 130, not 1.

**Delta scenarios**: "Local and read-only"; "Git too old"; "Git
unavailable"; "SIGTERM or SIGHUP during collection"; "SIGINT during
collection".

---

### User Story 10 - Exact paths and one versioned JSON document (Priority: P3)

Scripts read `project overview --json`: one versioned document with a fixed
set of fields, every path exact or flagged, never a traceback. Paths
holding newlines, control, format or bidirectional characters, or bytes that
are not UTF-8, are reported exactly or escaped and flagged, and a root or
worktree whose path is not UTF-8 never feeds a clean suggestion.

**Why this priority**: It serves automation and rare paths; the person at a
terminal is served by the earlier stories.

**Independent Test**: On Linux, create a repository whose directory name
holds a newline and worktrees whose names hold a tab, U+0007, U+202E,
U+200B and the byte `0xFF`, plus a git directory whose name holds `0xFF`;
parse standard output as JSON, and run the argument-error and
internal-error cases.

**Acceptance Scenarios**:

1. **Given** a repository directory name holding a newline and linked
   worktree names holding a tab, U+0007, U+202E and U+200B, **When** the
   overview runs, **Then** each JSON `path`, the findings' `checkout` paths
   and `repository.root` are exact with the escapes `\n`, `\t`, `\u0007`,
   `‮` and `​`, every `path_valid_utf8` and `root_valid_utf8` is
   true, each worktree is classified from its real state rather than as
   `stale-worktree`, the human output prints each such path in `$'...'`
   form, the newline as `\u000a`, the tab as `\u0009`, U+0007 as `\u0007`,
   U+202E as `‮` and U+200B as `​`, and the printed suggestion,
   pasted into bash under a UTF-8 locale, names the same repository root.
2. **Given** a clean merged worktree whose name holds the byte `0xFF`,
   **When** the overview runs, **Then** it completes, the worktree's `path`
   and its finding's `checkout.path` show the byte as `\xff`, each with
   `path_valid_utf8: false`, the row has an `unsupported-path-bytes` repair
   finding, the worktree contributes nothing to the `--all-safe`
   suggestion, and `project clean <root> --all-safe` excludes it with
   reason `unsupported-path-bytes`; and when another worktree holds two
   ignored files, one named with the byte `0xFF` and one named with the four
   characters `\xff`, its two `ignored_samples` entries have the same
   decoded `path` and differ only in `path_valid_utf8`, false and true.
3. **Given** the checkout of a repository made with `git init
   --separate-git-dir` into a git directory whose name holds the byte
   `0xFF`, with a dirty linked worktree, **When** the overview runs,
   **Then** `repository.common_dir` shows the byte as `\xff` with
   `common_dir_valid_utf8: false` while `root_valid_utf8` is true, the row
   has a repository-level `unsupported-path-bytes` repair finding, neither
   the row nor any finding carries a clean suggestion, each finding that
   would have suggested one names `unsupported-path-bytes` in
   `suggestion_gate`, and `project clean <root>` refuses with
   `unsupported-path-bytes` and exit status 2.
4. **Given** `project overview --json --bogus`, **When** it runs, **Then**
   standard output is empty, standard error carries the usage message, and
   the exit status is 2.
5. **Given** one healthy repository holding one `merged-removable` worktree
   and one unreadable root, **When** `project overview --json` runs,
   **Then** the document carries exactly the envelope's fields with their
   types, `limits` includes `batch_row_cap`, `report_row_cap` and `targets`
   equal to the shared constants, read without building a clean plan,
   every finding carries `suggestion_gate` and `suggestion_gate_rows`,
   every `path` has `path_valid_utf8` beside it, `repository` carries
   `root_valid_utf8` and `common_dir_valid_utf8`, and `completeness` is
   `incomplete`.
6. **Given** an exception raised outside the per-candidate boundary during a
   `--json` run, **When** it reaches the top, **Then** standard output holds
   only `{"error": "<message>", "code": "internal-error"}`, the message
   naming the exception class, no traceback is printed, and the exit status
   is 2.

**Delta scenarios**: "Control and format characters in paths"; "Non-UTF-8
path"; "Non-UTF-8 common directory"; "An argument error under --json";
"Every envelope field is present"; "An internal error outside the collector
under --json".

---

### Edge Cases

- **EC-001**: A filesystem call stuck in the kernel is abandoned at its
  budget so the run never blocks on it, but process exit may wait for it;
  it is the one exception to the run bound, and the README says so
  (design D1, D2 and Risks).
- **EC-002**: SIGKILL of `project` itself runs no cleanup: its read-only Git
  children run on, untimed, to their own end (design D1, Risks).
- **EC-003**: A default root holding more than 128 candidates is incomplete
  on every run by design: governance task 2.1 found 219 on the measuring
  workstation, a `scan-limit` error on `candidates` with 91 omitted, and no
  cap moves for it (proposal, OQ-4).
- **EC-004**: A repository with more than about 355 worktree rows, or about
  75 when its index holds 100,000 entries, ends at the deadline, visibly
  incomplete; there is no per-repository row cap (proposal, OQ-7).
- **EC-005**: Roots on a Windows drive mounted into WSL2 can make every
  listing slow and truncate on every run; that case was not measured, and
  the README says so (design, Risks).
- **EC-006**: A remote-helper protocol of another name, with its own
  `allow=always` in the repository's configuration, is not among the pins
  and could still fetch for a probe in a partial clone; the probe then
  succeeds rather than fails, and no unsafe advice follows, the overview
  being read-only (design D13, Risks; R-25).
- **EC-007**: `target-cap` counts gate-passing rows the batch's index gates
  may still exclude, so the overview's count can exceed what the batch
  selects; the suggestion is advice either way (design D5, Risks).
- **EC-008**: Repositories without file reflogs (the reftable backend, or
  `core.logAllRefUpdates=false`), and branches whose decisive entries
  expired after `gc.reflogExpire`, give every merged row
  `reflog-unavailable`, failing closed with the read-only suggestion
  (design, Risks).
- **EC-009**: A reflog over 64 KiB (about 300 entries) is
  `reflog-unavailable` even when it records movement, because the bound
  ends the read (design, Risks; R-18).
- **EC-010**: A branch created from a remote branch that already had
  commits, then merged elsewhere and never moved here, reads
  `unstarted-branch` and fails closed (design, Risks).
- **EC-011**: A remote whose name contains `/` can make the remote-copy flag
  read set for another remote's branch, giving an `unpublished` warning,
  the direction in which the overview errs (design D9, Risks).
- **EC-012**: A gitfile repository whose checkout lies outside every root
  reads `unsupported-layout`, an error; adding the checkout's parent with
  `--root` names it (design, Risks; N-6).
- **EC-013**: A squash merge never puts the branch tip into the merge
  target's ancestry, so squash-merging repositories yield few
  `merged-removable` rows. Open question 2 of `add-project-clean-all-safe`
  (the lead's LQ-2), a local patch-equivalence proof, is still before Brett
  Heap, is deferred to a follow-on change, and is not decided here; the
  overview would inherit its ruling through [L] (design, Open Questions).
- **EC-014**: A Triad assembly root given as `--root` is examined itself,
  and its spec and code legs are immediate entries whose checkouts are
  submodules, so each leg row gets the `unsupported-layout` error and the
  run exits 1, as the change rules for every submodule checkout (POD:97-102;
  design D3; see `clarify-questions.md`).
- **EC-015**: After SIGHUP the terminal may answer writes with an error, so
  `Cancelled.` is printed on a best-effort basis (proposal, Decisions).
- **EC-016**: The pasteable `$'...'` form assumes bash 4.2 or newer, or zsh;
  macOS's bash 3.2 is not a target, and tests assert the rendered string
  (proposal, Decisions, "Suggestion display string").
- **EC-017**: Non-UTF-8 path scenarios cannot run on macOS, whose
  filesystems reject such names, and are skipped there with that reason
  (proposal, Impact; design D13).
- **EC-018**: Two spellings of one directory, such as a bind mount or
  `~/projects` and `~/Projects` on a case-insensitive filesystem, count
  once, and the canonically first spelling wins (POD:14-16, :85-87; design
  D7).
- **EC-019**: A Git child stopped at its record bound is a complete
  outcome, never `probe-failed` or `probe-timeout` (design D1; [E];
  Clarifications, C-2).
- **EC-020**: A reflog read that does not finish leaves its row unprobed,
  which withholds `--all-safe` for the whole repository with
  `inspection-incomplete` (POD:521-529; R-16).
- **EC-021**: Ignored files in the merge-target checkout raise no finding,
  since a `.venv` would otherwise warn on most projects (proposal, OQ-20).
