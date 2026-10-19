Lane: openRepoProject-4

# Clarify questions: Project overview

**Path**: `specs/005-project-overview/clarify-questions.md`

**Status**: Open, for Brett Heap; not answered here. Asked by lane
openRepoProject-4 for feature `005-project-overview` on 2026-10-11, after the
spec's specify step. Each question is one the ratified change
(`openspec/changes/add-project-overview/`) and feature 004 leave genuinely
open; what their text settles is in `spec.md`, Clarifications, C-1 to C-54.
No requirement changes until an answer is given; answers join the spec's
Clarifications as a later session. Q6 to Q13 were added on 2026-10-19 from
three read-only reviews of the spec at `3d28710`, and Q14 and Q15 the same
day, from the evaluation of the spec against the checklists of the
no-argument `/speckit.checklist` run.

Fifteen questions, in one block: Q1 to Q5 asked on 2026-10-11, Q6 to Q15
added on 2026-10-19.

---

## Q1. A Triad assembly given as `--root`

**Context**: A root is examined itself (C-1), and the README's check of one
project is `project overview --root <dir>` (proposal, Impact). A Triad's
assembly repository holds its spec and code legs as submodules at `spec/`
and `code/` (openRepoShape's README), so both legs are immediate entries of
that root, and the change gives every submodule checkout an
`unsupported-layout` repair finding of severity error (POD:97-102; design
D3, item 1). The check of one Triad therefore reports two error rows and
exits 1 on every run (spec EC-014). A default-root run is unaffected: the
legs are not immediate entries of the projects directory.

**Question**: How should feature 005 treat the one-project check for a
Triad?

**Recommended:** Option A - It builds the ratified rule ("unknown is never
healthy", and the overview never suggests what `project clean` refuses) at
no cost now, and a later change can relax it once real runs show the need.

| Option | Description |
|--------|-------------|
| A | Build as ratified: each leg row carries `unsupported-layout`, the run exits 1, and the README says so for Triad assemblies. |
| B | Build as ratified, and open a follow-on OpenSpec change now that makes a submodule checkout declared as a leg of an examined assembly an informational row instead. |
| C | Amend change 2 before the plan (a spec fix on `main`), so feature 005 builds the leg treatment from the start; the plan waits for it. |

---

## Q2. What must exist before feature 005's plan is written

**Context**: The change creates feature 005 only after feature 004 merges
(proposal, Status; `tasks.md` 3.1). Brett Heap's word of
2026-10-11T16:14:21Z moved the specify step only, and the record says the
plan and the implementation "still wait for feature 004's code and for his
word". Feature 004 carries its reviewed plan and its tasks at `66d60b6` on
its branch, and its `project` holds only empty regions and imports. The
overview drives feature 004's child handle, driver and parsers (spec,
Dependencies), and the plan re-pins every code citation against `main`.

**Question**: Which state of feature 004 must exist before the plan starts?

**Recommended:** Option A - The runner's interface, the shared constants
and the citations are what feature 004's review may still change, so
planning against an unmerged branch risks a second plan; A is also the
order the change already sets.

| Option | Description |
|--------|-------------|
| A | Feature 004 merged into `main`; the plan pins against that `main`. |
| B | Feature 004's runner, parsers and evidence model (its plan slices 2 and 3) pushed on its branch; the plan pins against that branch and re-pins after the merge. |
| C | No standing rule: Brett Heap's word at the time decides. |

---

## Q3. The overview's tests and the Git 2.36 floor job

**Context**: Feature 004 adds a CI job that builds Git 2.36 and runs the
`clean`, `status` and `doctor` tests with it first on PATH (feature 004
FR-067; change 1's design D17). The overview refuses a Git older than 2.36
and so claims to work at 2.36 (spec FR-043), but change 2's Impact lists
only `project`, the README and the tests, and no CI change.

**Question**: Should the overview's tests also run in the Git 2.36 floor
job?

**Recommended:** Option B - It proves the overview's own claim at 2.36 on
the probes it drives for little CI time, while the shared probes are
already proven there by feature 004's tests; A adds the cap-scale fixtures
to the floor job's run.

| Option | Description |
|--------|-------------|
| A | Yes, all of them: the floor job's selection gains the overview tests, a CI change beyond change 2's Impact list. |
| B | A small set: the version refusal and one end-to-end run over a fixture with linked worktrees, merge targets and a gated suggestion. |
| C | No: the floor stays proven by feature 004's tests of the shared probes the overview reuses. |

---

## Q4. Telling agents that a suggestion is not permission

**Context**: "Evidence is not permission" reaches people through the
README (spec FR-048). Agents working in this repository read `AGENTS.md`,
which covers `project new` (feature 002) and says nothing of the overview;
change 2's Impact names no `AGENTS.md` change. An agent reading `project
overview --json` could run a suggested `project clean <root> --all-safe`
with `--apply --yes` on its own.

**Question**: Should agents be told in `AGENTS.md` that an overview
suggestion is advice to review, and that applying it needs the person's
word?

**Recommended:** Option C - The guidance matters for agent safety, but it
also concerns feature 004's `--apply --yes`, so one governed change can say
it for both while feature 005 stays within its ratified scope.

| Option | Description |
|--------|-------------|
| A | No `AGENTS.md` change: the README section carries the rule, as the change scopes it. |
| B | Add one `AGENTS.md` paragraph in feature 005, recorded as a departure from change 2's Impact on Brett Heap's word. |
| C | A separate small OpenSpec change for agent guidance on the overview and the batch apply, after feature 005. |

---

## Q5. Feature 004's partial-removal note in the overview

**Context**: Feature 004 adds the advisory row note `partially-removed` to
a dirty linked worktree whose status records are all deletions of tracked
files, the trace a removal killed midway leaves, shown beside the `dirty`
advice with recovery text (feature 004 FR-009; change 1's design D4).
Change 2's worktree row is a closed field list for schema 1 with no `notes`
(POD:632-638), so the overview shows that worktree as a plain `dirty`
finding, whose read-only suggestion leads to `project clean <root>`, which
shows the note.

**Question**: Should the overview surface the partial-removal note?

**Recommended:** Option A - The case is rare, its recovery happens in
`project clean`, to which the overview already points, and option B stays
open later without a schema change, a new field being additive
(POD:655-658).

| Option | Description |
|--------|-------------|
| A | No, as ratified: the `dirty` finding's read-only suggestion leads to `project clean`, which shows the note. |
| B | Yes, as an additive worktree-row `notes` field within schema 1, through a follow-on OpenSpec change. |
| C | Yes, in the `dirty` finding's message, through a follow-on change to the fixed message text. |

---

## Q6. What `limit` and `omitted` hold on `deadline-exceeded` errors

**Context**: The error object adds `limit` and `omitted` on `scan-limit`
and `deadline-exceeded` errors (POD:646-648), and the packet defines
`limit` as "a key of `limits`" (DI:824-825). The change fixes only the
deadline scan error's count, the candidates not started (POD:181), and
its exactness (spec C-30). No `limits` key names the deadline, which
`budget` reports as `invocation_timeout_seconds`, and row-level
`deadline-exceeded` errors (an in-flight child cut, an unstarted
candidate's row) are error objects too, with nothing defined for either
field (fidelity review F-19).

**Question**: What do `limit` and `omitted` hold on `deadline-exceeded`
errors?

**Recommended:** Option A - It keeps the one count the change defines,
gives a consumer one fixed key to read, and drops two fields that would
hold nothing on a row error.

| Option | Description |
|--------|-------------|
| A | Amend change 2: only the one `deadline-exceeded` scan error carries them, `limit` being `"invocation_timeout_seconds"` (the `budget` key) and `omitted` the candidates not started; row-level `deadline-exceeded` errors carry neither. |
| B | Build as written: every `deadline-exceeded` error carries both, `limit` being `"invocation_timeout_seconds"` and a row error's `omitted` being `{"count": null, "exactness": "unknown"}`. |
| C | Leave both values to the plan, fixed once and recorded in the feature's traceability record. |

---

## Q7. A working directory the overview cannot resolve

**Context**: `current` decides `merged-current` from `merged-removable`
(change 1's [L]) and means that the overview's working directory lies
inside the worktree (spec C-25). Design D8 takes the working directory's
realpath in one bounded task at start. When that task fails (a working
directory deleted after the shell entered it) or is cut (a hung mount),
the change names no error and no rule for `current`. A null read as false
would make the worktree the person stands in `merged-removable` with
`--all-safe`, which the batch then excludes as current (adversarial
review A-4).

**Question**: What happens when the working directory's realpath cannot
be established?

**Recommended:** Option A - It needs no new code or field: the scan error
makes the run incomplete, and `inspection-incomplete`, a gate the table
already has, withholds `--all-safe`, in line with [L]'s rule for evidence
that could not be established.

| Option | Description |
|--------|-------------|
| A | Amend change 2: one scan error records it (`os-error`, `probe-timeout` or `deadline-exceeded`, naming the working directory as given), every `current` is null, and each row the ladder would classify `merged-removable` or `merged-current` is `inspection-error` instead, so `inspection-incomplete` withholds `--all-safe` for its repository. |
| B | As A, but those rows keep a null classification, and their repository's `--all-safe` is withheld under a new gate code added to the gate table (additive within schema 1). |
| C | Amend change 2's exit rule: the run refuses with exit 2 and `os-error` before listing any root, as for a Git refusal. |

---

## Q8. Strings that are not paths: names, branch names and Git's error text

**Context**: The path rules escape a path's control, format and separator
code points and its undecodable bytes, and flag it (POD:660-675; spec
FR-038, FR-045). The change gives no rule for the other strings the report
takes from the filesystem, a manifest or Git: a row's `name` (a directory
name, which can hold byte `0xE9` or a newline), a manifest `name` holding
U+202E, branch names in `branch`, `upstream`, `merge_target.name` and the
`merge-target-conflict` message (Git allows such bytes and characters in
them), and the first line of Git's standard error in an error `message`
and on the `Incomplete:` line. A raw newline there can forge report lines,
a bidirectional control can reorder them, and an undecodable byte can fail
the JSON encoding, an exception outside the collector that ends the run
with exit 2 (adversarial review A-6).

**Question**: How should the overview decode and print strings that are
not paths?

**Recommended:** Option A - It reuses the path rule the change already
ratified, so a hostile name stays inside its row and no field is added;
a validity flag can follow later, additively within schema 1.

| Option | Description |
|--------|-------------|
| A | Amend change 2: every such string follows [P]'s path rule, decoded as a path is, each undecodable byte written `\xHH`, each Cc, Cf, Zl or Zp code point escaped by JSON and written `\uXXXX` in human output; no new field. |
| B | As A, plus a validity flag beside each such field (`name_valid_utf8`, `branch_valid_utf8` and the like), additive within schema 1. |
| C | Build as written and leave the rule to the plan. |

---

## Q9. Read-only and no-network claims beyond what the pins and the scrub prove

**Context**: The change promises no file write and no network connection
(POD:710-717; spec FR-040). What change 1's evidence model guarantees is
narrower: seven protocol pins, seventeen scrubbed names and
`GIT_OPTIONAL_LOCKS=0` (CMD:98-122). Git still reads the user's and the
system's configuration and the variables outside the seventeen
(`GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`, `GIT_CONFIG_NOSYSTEM`, `HOME`,
`XDG_CONFIG_HOME`, `GIT_CEILING_DIRECTORIES`); it honours trace targets
(`GIT_TRACE`, `GIT_TRACE2_EVENT`, `trace2.*` settings), which append to
files; and the status probe runs the clean and process filters a
repository's attributes name (git-lfs, git-crypt) when it re-hashes a
tracked file. Such a program can write files or open connections outside
the pins (spec EC-022; adversarial review A-7). EC-006 records one
residual only. The user's configuration also carries settings such as
`status.showUntrackedFiles`, which change 1's scenario "User status
configuration" expects Git to read, so emptying the configuration
wholesale would break that scenario.

**Question**: How should the feature treat these residuals?

**Recommended:** Option B - Trace output is a pure side effect and its
variables are cheap to scrub for every subcommand at once; filters and
the configuration files cannot be switched off in general, so they are
recorded honestly beside EC-006 and the read-only wording says what is
proved.

| Option | Description |
|--------|-------------|
| A | Accept every one as a recorded residual beside EC-006 (spec EC-022), and amend change 2's read-only wording to claim only what the pins and the scrub prove. |
| B | As A for filters and the configuration files; and amend change 1 to add the trace variables (`GIT_TRACE`, `GIT_TRACE2`, `GIT_TRACE2_EVENT`, `GIT_TRACE2_PERF` and the other `GIT_TRACE_*` names) to [E]'s scrub, which `clean`, `status` and `doctor` then share. |
| C | Amend change 1 to run every Git child with no global or system configuration (`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`), which also drops user settings that change 1's scenarios read and changes `clean`'s results. |

---

## Q10. Two layouts the marker table leaves unreported

**Context**: The first matching marker decides a candidate (POD:24-31).
Two layouts leave a repository out of a complete run (spec EC-025;
adversarial review A-24): (1) a Git repository `D` whose holder directory
`D/<name of D>`, holding `family.yaml`, has no `.git`: the holder is the
candidate, a row with no Git child (spec FR-004), and `D`'s own repository
is never inspected; (2) a directory whose only marker would be a `.git`
that is a dangling symbolic link, which "exists as a file or a directory"
only when the link resolves, so the directory has no marker at all.

**Question**: Should the overview report these repositories?

**Recommended:** Option A - Both layouts are rare, and the marker table
mirrors the order in which `discover` and `manifest` look (DI:126-128), so
changing it touches how families are found; recording them costs nothing
now, and a later change can widen the table once a real case appears.

| Option | Description |
|--------|-------------|
| A | No: build the ratified table and keep both layouts as recorded edge cases (spec EC-025). |
| B | Amend change 2: a `D/.git` beside the holder marker makes `D` a candidate as well (kind `single`), and a `.git` entry that exists as any file type, a dangling link included, is a marker, the probe then failing visibly on that row. |
| C | Amend change 2 for layout (1) only, keeping a dangling `.git` link as a recorded edge case. |

---

## Q11. A candidate's `.git` that Git does not accept

**Context**: A directory is a `single` candidate when `D/.git` exists as a
file or a directory (POD:29). When that `.git` is not a repository Git
accepts (a directory without `HEAD`, a half-deleted clone), Git's
discovery skips it and walks upward, so the identity probe in `D` can
report an ancestor's toplevel and common directory, such as a dotfiles
repository in the home directory above `--root ~/mono/packages`. Nothing
in change 2 ties the probe's answer to the candidate, so `D` would create
or join a row for a repository outside every root, with its worktrees,
its merge target and possibly `project clean <ancestor> --all-safe`, and
`D`'s broken state would vanish from the report. That breaks "within
configured roots only" (POD:10) and "Unknown is never healthy"
(adversarial review A-2).

**Question**: What should the overview do when a candidate's identity
probe reports a toplevel other than the candidate itself?

**Recommended:** Option A - It keeps discovery inside the roots and shows
the broken checkout as an error on its own row, with a code the collector
table already has.

| Option | Description |
|--------|-------------|
| A | Amend change 2: such a candidate is an error row (`refused`, its message naming the toplevel Git found) and creates or joins no repository row. |
| B | Build as written: the candidate joins the repository Git reports, even one outside every root. |
| C | Record it as an edge case only, with no change to the behaviour. |

---

## Q12. Output failures, the output encoding and the exit-2 codes outside the collector

**Context**: Change 2 does not cover a failed write to standard output
(`project overview --json | head -c 100` gives `EPIPE`; a full disk gives
`ENOSPC`) or human output under a locale that cannot encode a printable
non-ASCII path (`LANG=en_US.ISO-8859-1`). Either raises outside the
collector, where the change maps every exception to `internal-error` with
exit 2 (POD:705-707), possibly after part of the output was written. The
same requirement lists `refused` and `os-error` as exit-2 codes under
`--json` (POD:675-679), but never says when either applies instead of
`internal-error` (adversarial review A-19).

**Question**: How should these cases end?

**Recommended:** Option A - Rendering before writing avoids a partial
document, UTF-8 output keeps paths exact whatever the locale, and the
mapping gives each listed code a meaning.

| Option | Description |
|--------|-------------|
| A | Amend change 2: the whole document or report is rendered before its first byte is written, as UTF-8 whatever the locale; a failed write ends the run with exit 2, no traceback and no retry, every child already reaped; outside the collector a refusal maps to `refused`, an `OSError` to `os-error` and any other exception to `internal-error`. |
| B | As A for the codes and the failed write, but human output follows the locale's encoding, writing what it cannot encode as `\uXXXX`. |
| C | Build as written: every such case is `internal-error` with exit 2, and the plan decides rendering and encoding. |

---

## Q13. A root whose canonicalisation is cut

**Context**: Roots are canonicalised, deduplicated by canonical path and
by device and inode, sorted by their canonical bytes and capped at 32
(POD:14-16, :217-222). "A root on a hung mount" cuts a root whose
canonicalisation or listing takes too long and reports it `truncated`
with a `probe-timeout` scan error (POD:303-306). When canonicalisation
itself is cut, the root has no canonical path, so its root object's
`path`, its place in canonical order, its deduplication and its count
under the root cap are all undefined, while the report's order must be
fixed (adversarial review A-21).

**Question**: How is such a root reported?

**Recommended:** Option A - It uses the only path the overview holds,
keeps the order total and stable, and errs toward reporting a root twice
rather than hiding one.

| Option | Description |
|--------|-------------|
| A | Its `path` is the expanded path as given; it sorts by those bytes among the canonical paths, is never deduplicated, and counts toward the 32-root cap. |
| B | As A, but it sorts after every canonical root and does not count toward the cap. |
| C | Leave it to the plan, fixed once and recorded in the feature's traceability record. |

---

## Q14. A bare repository's own record, and the `.bare` layout

**Context**: A bare repository's registry lists the repository itself
first, marked `bare`, at its common directory, and on Git 2.43.0 `git
status` there fails with "this operation must be run in a work tree"
(reproduced for this question). Change 2 leaves `repository.root` null for
"a bare main entry" (POD:102-104) and withholds every clean suggestion with
`target-not-repository-root` (design D3, item 2), but says nothing of that
record as a worktree row: whether it is listed, whether it is status-probed,
what its classification is, and whether it counts toward the 512-row cap and
the row count of `inspect-cap` and `suggestion_gate_rows` (spec C-46). For
the submodule and the unnamed gitfile records, design D3 (items 1 and 3)
keeps the main worktree row with the record's path, its `present` from
`lstat`, and null status fields and classification. Probing the bare record
would make every bare repository with linked worktrees `inspection-error`,
an error finding, and exit 1 on every run. Separately, a candidate whose
`.git` file names a bare repository (the layout that keeps it in `.bare`
beside its worktrees) fails its identity probe as written, since the probe
asks for a toplevel, so the repository appears only as a `probe-failed`
error row with none of its worktrees (spec EC-030, C-54).

**Question**: How should a bare repository be reported?

**Recommended:** Option A - It reuses design D3's ratified treatment of a
record that has no work tree, needs no amendment, counts every registry
entry as `project clean` counts rows, and leaves the `.bare` layout recorded
until a real run shows the need.

| Option | Description |
|--------|-------------|
| A | The bare record is the main worktree row, as D3 keeps an unnamed gitfile record: its path the common directory, `present` from `lstat`, no status probe, null status fields and classification, no finding of its own, and counted toward the caps and the row count. The `.bare` layout stays a `probe-failed` error row, recorded as EC-030. |
| B | As A, and amend change 2 so that a candidate whose identity probe fails for want of a work tree takes one more counted child asking for its common directory alone, and joins that repository's row as a linked worktree of a bare repository does, listing its worktrees with `target-not-repository-root` on every clean suggestion. |
| C | The bare record is no worktree row: `worktrees` lists the linked worktrees only, and the record counts toward no cap. The `.bare` layout as in A. |

---

## Q15. A signal while the result is being written

**Context**: On SIGINT, SIGTERM or SIGHUP the overview prints no result
document and exits with that signal's status, which takes precedence over 1
(POD:776-780; spec FR-044), and on exit 0 or 1 it prints the full result
(POD:767). The change's scenarios send the signal during collection
(POD:792-799), and design D1 handles signals around the collection loop,
while rendering follows that loop (design D6). A signal that arrives after
the first byte of the result reaches standard output, and before the last,
cannot meet both rules: the bytes written cannot be withdrawn, and exiting 0
or 1 would ignore the signal. Question Q12 asks how output failures end; it
does not cover a signal.

**Question**: What should a signal that arrives while the result is being
written do?

**Recommended:** Option A - It keeps Ctrl-C responsive and keeps one rule
for consumers, that an exit of 129, 130 or 143 carries no result, at no
cost; rendering before writing, as Q12's option A has it, narrows the window
to the write itself.

| Option | Description |
|--------|-------------|
| A | Record it as a residual beside EC-015: the write stops at the signal, `Cancelled.` follows on standard error, and the run exits with the signal's status; standard output may then hold part of a result, which an exit of 129, 130 or 143 marks as no result. |
| B | Block the three signals from the first byte of the result to the last, then exit 0 or 1 as the result says, dropping the signal; a consumer that stops reading the pipe then leaves the run unstoppable by Ctrl-C until it reads. |
| C | Leave it to the plan, fixed once and recorded in the feature's traceability record. |

---

You can reply with the option letter for each question (e.g., "Q1 A, Q2 A,
Q3 B, Q4 C, Q5 A, Q6 A, Q7 A, Q8 A, Q9 B, Q10 A, Q11 A, Q12 A, Q13 A,
Q14 A, Q15 A"),
accept every recommendation by saying "yes" or "recommended", or give your
own short answer for any of them.

**Path**: `specs/005-project-overview/clarify-questions.md`
