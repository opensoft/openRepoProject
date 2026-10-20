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

Seventeen questions, in one block: Q1 to Q5 asked on 2026-10-11, Q6 to Q15
added on 2026-10-19, and Q16 and Q17 on 2026-10-20. On 2026-10-19, after
feature 004's doc rounds 3 and 4 (`5a02c1a`), Q4, Q8 and Q15 each gained an
option D, and the recommendations of Q4 and Q8 moved to D. On 2026-10-20,
after four read-only reviews (lane openRepoProject-3's packet-fidelity read,
a cross-check of feature 004's built runtime, a review of the recommended
answers as one set, and a review of lane openRepoProject-5's #24 and #25),
Q2, Q3, Q4, Q6, Q7, Q8, Q9, Q11, Q12, Q13, Q14 and Q15 were corrected, and
Q16 and Q17 added; no recommendation changed letter. After lane
openRepoProject-3's delta reads, the questions were corrected again at
`fdbcebb`, `d6e4ec5`, `7eb64de` and in the fold of its R4 and R5 findings,
with the pins of Q3, Q4, Q14 and Q15 moved to feature 004's `b0243e5` at
`fdbcebb`, and no recommendation changed letter.

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
word". Feature 004's branch holds, since `a32d20b`, the code of its tasks
T001 to T035, all ticked, so that its Phase 1 and Phase 2 are complete: the
runner (its child handle and driver, with the `Invocation` state and the
signal slot), its five incremental parsers and its evidence model (T027 to
T033, merged as `cce8dbd`); its head, `b0243e5`, adds only documents, the
first part of doc round 6 (rulings R-55 to R-57, with R-53's P-16 and P-22
and R-54's X-3). Option B's precondition is therefore met, and none of it is
on `main`. The overview drives feature 004's child handle, driver and
parsers (spec, Dependencies), and the plan re-pins every code citation
against `main`.

**Question**: Which state of feature 004 must exist before the plan starts?

**Recommended:** Option A - The runner's interface, the shared constants
and the citations are what feature 004's review may still change, so
planning against an unmerged branch risks a second plan; A is also the
order the change already sets.

| Option | Description |
|--------|-------------|
| A | Feature 004 merged into `main`; the plan starts on Brett Heap's word given after it, and pins against that `main`. |
| B | Feature 004's runner, parsers and evidence model (its plan slices 2 and 3) pushed on its branch (met at `a32d20b`); the plan starts on Brett Heap's word, pins against that branch and re-pins after the merge. |
| C | No standing rule: Brett Heap's word at the time decides. |

---

## Q3. The overview's tests and the Git 2.36 floor job

**Context**: Feature 004 adds a CI job that builds Git 2.36 and runs the
`clean`, `status` and `doctor` tests with it first on PATH (feature 004
FR-067; change 1's design D17). Its task T003, ticked at `b0243e5`, put that
job, `git-floor`, in its branch's workflow beside every job of the `test`
matrix, selecting `-k test_clean_ -k test_status_ -k test_doctor_`; it is not
on `main`. The overview refuses a Git older than 2.36 and so claims to work
at 2.36 (spec FR-043), but change 2's Impact lists only `project`, the
README and the tests, and no CI change.

**Question**: Should the overview's tests also run in the Git 2.36 floor
job?

**Recommended:** Option B - It proves the overview's own claim at 2.36 on
the probes it drives for little CI time, while the shared probes are
already proven there by feature 004's tests; A adds the cap-scale fixtures
to the floor job's run.

| Option | Description |
|--------|-------------|
| A | Yes, all of them: the floor job's selection gains the overview tests, a CI change beyond change 2's Impact list. |
| B | A small set, recorded as a departure from change 2's Impact on Brett Heap's word (or carried in the change-2 amendment's Impact): the version check accepting Git 2.36, and one end-to-end run over a fixture with linked worktrees, merge targets and a gated suggestion, selected in the `git-floor` job by one more `-k` prefix. |
| C | No: the floor stays proven by feature 004's tests of the shared probes the overview reuses. |

---

## Q4. Telling agents that a suggestion is not permission

**Context**: "Evidence is not permission" reaches people through the
README (spec FR-048). Agents working in this repository read `AGENTS.md`,
which covers `project new` (feature 002) and says nothing of the overview;
change 2's Impact names no `AGENTS.md` change. An agent reading `project
overview --json` could run a suggested `project clean <root> --all-safe`
with `--apply --yes` on its own. Feature 004's task T123, open at
`b0243e5`, adds to `AGENTS.md` a short section, "Cleaning up worktrees for a
person", which says never to answer the removal question, or pass `--yes`,
on a person's behalf unless they asked for that run; its tasks list that
edit among its departures from change 1, stated in its feature PR body for
Brett Heap's word (lead ruling R-32). Option D depends on T123's final
wording: its sentence lands in a section feature 004 has not yet written,
and follows that section's title and wording if either changes at feature
004's merge.

**Question**: Should agents be told in `AGENTS.md` that an overview
suggestion is advice to review, and that applying it needs the person's
word?

**Recommended:** Option D - Feature 004's T123 already adds an `AGENTS.md`
section that forbids answering the removal question or passing `--yes` on a
person's behalf, as a departure awaiting Brett Heap's word (its R-32); one
sentence there saying that an overview suggestion is advice to review keeps
the agent guidance in one place. If that departure is declined, option C
carries the guidance for both commands.

| Option | Description |
|--------|-------------|
| A | No `AGENTS.md` change: the README section carries the rule, as the change scopes it. |
| B | Add one `AGENTS.md` paragraph in feature 005, recorded as a departure from change 2's Impact on Brett Heap's word. |
| C | A separate small OpenSpec change for agent guidance on the overview and the batch apply, after feature 005. |
| D | After feature 004 lands, add one sentence on the overview to the `AGENTS.md` section that feature 004's T123 adds ("Cleaning up worktrees for a person"), recorded as a departure from change 2's Impact on Brett Heap's word, as feature 004 records its own (its R-32). If Brett Heap declines feature 004's T123 departure, option C applies instead. |

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
hold nothing on the other `deadline-exceeded` errors. Its last clause, for
a row-level `scan-limit` error, is a proposal: an answer may take A with
"carries neither" there instead, a further amendment, since POD:646-648 and
POD:222-229 give such an error both fields.

| Option | Description |
|--------|-------------|
| A | Amend change 2: only the `deadline-exceeded` scan error that counts the candidates not started (POD:180-181) carries them, `limit` being `"invocation_timeout_seconds"` (the `budget` key) and `omitted` the candidates not started; every other `deadline-exceeded` error, row or scan, carries neither; and a row-level `scan-limit` error, on which POD:646-648 adds the same two fields, carries `limit: "worktree_rows"` and `omitted` counting that repository's rows past the cap, exactness `exact`. |
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
| A | Amend change 2: one scan error records it (`os-error` or `probe-timeout`, with feature 004's fixed text and OPERATION `realpath`, its `path` the `PWD` environment value when that is set and absolute, else omitted, and first among the scan errors), every `current` is null, and each row the ladder would classify `merged-removable` or `merged-current` is `inspection-error` instead, so `inspection-incomplete` withholds `--all-safe` for its repository. That `path` is taken raw, absolute as the environment gives it and unresolved, a further exception to DI:842-843's rule that paths are canonical, which already excepts `ignored_samples` and an absent default root: three exceptions with this one, four with Q13's option A as well. |
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
with exit 2 (adversarial review A-6). Feature 004's contract fixes one
message per row-error code (lead ruling R-45); its `probe-failed` message
is `OPERATION failed: DETAIL`, DETAIL being `exit N`, `signal N`, `cannot
spawn (STRERROR)` or `unparseable output`, so no text of Git's standard
error reaches it.

**Question**: How should the overview decode and print strings that are
not paths?

**Recommended:** Option D - It removes Git's text at its source rather than
escaping it, and gives the overview the fixed row-error texts of the
evidence model it shares with feature 004 (R-45), so the plan reuses
feature 004's texts where they fit and the amendment fixes the rest; names
and branch names take the path rule the change already ratified, as in A,
and a validity flag can still follow later, additively within schema 1.

| Option | Description |
|--------|-------------|
| A | Amend change 2: every such string follows [P]'s path rule, decoded as a path is, each undecodable byte written `\xHH`, each Cc, Cf, Zl or Zp code point escaped by JSON and written `\uXXXX` in human output; no new field. |
| B | As A, plus a validity flag beside each such field (`name_valid_utf8`, `branch_valid_utf8` and the like), additive within schema 1. |
| C | Build as written and leave the rule to the plan. |
| D | Amend change 2 so that every row and scan error's message is a fixed text for its code, naming no path, the path going in `path`: feature 004's for `os-error`, `probe-failed` and `probe-timeout` (its contract, lead ruling R-45); `OPERATION stopped at the invocation deadline` for `deadline-exceeded`, the overview's own term, where feature 004's contract reads `OPERATION stopped at the work deadline` (`contracts/project-clean.md:303` at `b0243e5`); and texts this amendment fixes for `manifest-invalid` (naming the cause, the size bound or the missing library, never the reader's own text), `refused`, `undecodable-output`, `internal-error` (the exception's class only), `scan-limit` and `root-unreadable`. The amendment edits POD:337-338 to "with a message of at most 200 characters, the fixed text of its code, which names no path"; design D1 (design.md:99-101) so that a child's standard error is "drained and capped as [E] requires (CMD:175-177), and never shown"; and clarifications N1 (clarifications.md:35-36 and :46-47), whose "first 200 characters kept" goes the same way; the three texts as they stand follow the packet's DI:544-545 ("for a failed probe, the first line of Git's standard error"), and this amendment departs from that rule; FR-022 is folded to match after it is ratified. No text from Git's standard error then reaches a message or the `Incomplete:` line, and names, branch names, admin ids and every other string the report takes from the filesystem, a manifest or Git follow [P]'s path rule as in A. Git's own reason is then not shown: the person re-runs the Git command to see it. |

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
variables are cheap to pin and scrub for every subcommand at once; filters
and the configuration files cannot be switched off in general, so they are
recorded honestly beside EC-006 and the read-only wording says what is
proved.

| Option | Description |
|--------|-------------|
| A | Accept every one as a recorded residual beside EC-006 (spec EC-022), and amend change 2's read-only wording to claim only what the pins and the scrub prove. |
| B | As A for filters and the configuration files; and amend change 1 to set `GIT_TRACE2`, `GIT_TRACE2_EVENT` and `GIT_TRACE2_PERF` to `0` on every Git child, which overrides `trace2.*` targets in the system and global configuration, and to add `GIT_TRACE` and the `GIT_TRACE_*` names Git 2.36 to 2.43 reads, each listed by name, to [E]'s scrub, which `clean`, `status` and `doctor` then share. The change-1 amendment is proposed to ride in lane openRepoProject-2's draft PR #19, which already edits [E]'s Environment paragraph (not yet agreed by lane openRepoProject-2; PR #19 holds no trace pin at `c462d87`); if feature 004 merges first it builds the narrower scrub and the wider one follows as a change-1 amendment; change 2's "seventeen names" becomes a citation of [E]'s list. |
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
repository in the home directory above `--root ~/mono/packages`. Change 2
ties the probe's answer to the candidate only for a family holder, which
receives Git probes only when its own directory is a Git toplevel
(POD:38-39); the packet adds that such a holder otherwise has null
`repository`, `merge_target`, `git` and `worktrees` and carries no error
(DI:284-287), as spec FR-003 states. For any other candidate nothing ties
them, so `D` would create or join a row for a repository outside every
root, with its worktrees, its merge target and possibly `project clean
<ancestor> --all-safe`, and `D`'s broken state would vanish from the
report. That breaks "within configured roots only" (POD:10) and "Unknown
is never healthy" (adversarial review A-2).

**Question**: What should the overview do when a candidate's identity
probe reports a toplevel other than the candidate itself?

**Recommended:** Option A - It keeps discovery inside the roots and shows
the broken checkout as an error on its own row, with a code the collector
table already has.

| Option | Description |
|--------|-------------|
| A | Amend change 2: a candidate other than a family holder whose identity probe reports a toplevel that is a proper ancestor of the candidate is an error row (`refused`, its `path` the candidate's `.git`, its message a fixed text saying that Git did not accept it and reported an enclosing repository), and creates or joins no repository row; a family holder whose probe reports another toplevel keeps null `repository`, `merge_target`, `git` and `worktrees` and no error, as DI:284-287 and spec FR-003 have it; and a toplevel elsewhere that Git reports for a layout it accepts, such as a `core.worktree` naming another directory, is unaffected. |
| B | Build as written: the candidate joins the repository Git reports, even one outside every root. |
| C | Record it as an edge case only, with no change to the behaviour. |

---

## Q12. A failed write to standard output, and the output encoding

**Context**: Change 2 does not cover a failed write to standard output
(`project overview --json | head -c 100` gives `EPIPE`; a full disk gives
`ENOSPC`) or human output under a locale that cannot encode a printable
non-ASCII path (`LANG=en_US.ISO-8859-1`). Either raises outside the
collector, possibly after part of the output was written. How an exception
outside the collector ends the run is settled and not asked here: exit 2
with no traceback, a refusal giving `refused`, an operating-system error
`os-error` and any other exception `internal-error` (DI:1083-1089;
proposal, Impact; spec FR-039). A failed write is an operating-system
error, so as written its `os-error` object is due under `--json` on the
very standard output that failed, since every exit 2 but an argument error
prints one (POD:675-679; DI:1086-1089; SC-009); an encoding failure is
`internal-error`. For `project clean`, lane openRepoProject-2's ruling R-55
(2026-10-20) now decides a failed write: the first one points that stream
at `/dev/null` and records the error on the run, so there is no second
traceback and no exit 120; before the apply phase the error is
`internal-error`, exit 2, nothing mutated, unless a recorded signal
outranks it (130, 143 or 129, with `Cancelled.`); after the apply phase
begins, writes are best-effort and the exit table decides; and a failed
advisory write (`Cancelled.`, `REFUSED:`) never changes the exit status
(feature 004's research.md R4 and T047 at `b0243e5`). Whether R-55's exit 2
holds for a `project clean` preview or report once its plan is built is
lane openRepoProject-2's LQ-7, pending with Brett Heap: change 1's
`project-clean` delta,
`openspec/changes/add-project-clean-all-safe/specs/project-clean/spec.md`,
reads both ways, refusing an unexpected exception before the apply phase
with `internal-error` and exit status 2 (`:940-941`), and letting a preview
or report exit 2 only for a refusal raised before a plan is built
(`:958-960`). R-55's reading stands until he rules, and Q12's options set
the overview's own exit, so they do not wait on LQ-7. Feature 004 writes
each `clean --json` document with `ensure_ascii=True` (its T035, lead
ruling R-38), so its JSON is ASCII whatever the locale; its human output
takes no position on the locale.

**Question**: How should a failed write to standard output and the output
encoding be handled?

**Recommended:** Option A - Rendering before writing avoids a partial
document, UTF-8 output keeps paths exact whatever the locale, and a failed
write ends as R-55 ends one in feature 004 before its apply phase, with
nothing more on the failed stream and no traceback.

| Option | Description |
|--------|-------------|
| A | Amend change 2: the whole document or report is rendered before its first byte is written, as UTF-8 whatever the locale, the JSON document with ASCII escapes as feature 004 writes its own (its R-38), every interpolated string already escaped by [P]'s rule; a failed write to standard output ends the run with exit 2, no traceback and no retry; nothing more goes to standard output, and one line goes to standard error on a best-effort basis; this is, besides an argument error, the one exit 2 under `--json` that prints no error object, carved out of POD:675-679 and the packet's DI:1086-1089 (FR-039 and SC-009 folded after), and with no error object there is no code to print, so R-55's `internal-error` is not kept; every child is already reaped or abandoned. A recorded signal decides the status, also over the exit 2 of a failed write. This matches lane openRepoProject-2's ruling R-55 for feature 004's phase before apply: the failed stream gets nothing more, the error is recorded on the run, and a recorded signal outranks it. Every other exception outside the collector ends as FR-039 maps it. |
| B | As A for the failed write and the JSON document, but human output follows the locale's encoding, writing what it cannot encode as `\uXXXX`. |
| C | Build as written: a failed write is an operating-system error raised outside the collector, so it is `os-error` with exit 2, its error object due under `--json` on the very standard output that failed; an encoding failure is `internal-error` with exit 2; and the plan decides rendering and encoding. |

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
| A | Amend change 2: its `path` is the given path made absolute (expanded, and joined to the working directory when relative) but not resolved: absolute, as DI:842-843 has every path, and a further exception to its rule that paths are canonical, which already excepts `ignored_samples` and an absent default root: three exceptions with this one, four with Q7's option A as well; it sorts by those bytes among the canonical paths, is never deduplicated, and counts toward the 32-root cap, a root past the cap being `omitted` whether or not its canonicalisation was cut. |
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
error row with none of its worktrees (spec EC-030, C-54). Feature 004 at
`b0243e5` reads a bare first record the same way for its own subcommands:
its `main_worktree()` returns no main worktree, with its cause, and never
raises, so `root` is null and rows 4 to 7 run in the common directory (its
T031, T107 and FR-055; analyze H4, lead ruling R-42); `clean` alone refuses
such a repository, with `target-not-repository-root`, while `status` and
`doctor` report a linked worktree of a bare repository and never exit 2 for
it (its T115). Its data model, "Repository identity", says the common
directory is "never a worktree row", as its FR-017 does for a first record
equal to it, and no document of feature 004 says more of how `status` or
`doctor` lists that record. H4 leaves the `.bare` layout as it was: feature
004's identity probe (its contract, row 3) runs before `main_worktree()`,
and in the holder directory it exits 128 with "this operation must be run
in a work tree" (reproduced on Git 2.43.0 for this question).

**Question**: How should a bare repository be reported?

**Recommended:** Option A - It reuses design D3's ratified treatment of a
record that has no work tree, needs no amendment, counts every registry
entry toward the caps, as POD:217-218 counts main worktree rows and C-46
every registry entry, and leaves the `.bare` layout recorded until a real
run shows the need.

| Option | Description |
|--------|-------------|
| A | The bare record is the main worktree row, as D3 keeps an unnamed gitfile record: its path the common directory, `present` from `lstat`, no status probe, null status fields and classification, no finding of its own, and counted toward the caps and the row count. It adds no status probe to `probes.estimated`, and its null classification is not one the overview's cap or deadline left. The `.bare` layout stays a `probe-failed` error row, recorded as EC-030. This follows design D3, as for the unnamed gitfile record; feature 004's model never makes the common directory a worktree row, and its `clean` refuses a bare repository. |
| B | As A, and amend change 2 so that a candidate whose identity probe fails for want of a work tree takes one more counted child asking for its common directory alone, and joins that repository's row as a linked worktree of a bare repository does, listing its worktrees with `target-not-repository-root` on every clean suggestion. |
| C | The bare record is no worktree row: `worktrees` lists the linked worktrees only, and the record counts toward no cap. The `.bare` layout as in A. |

---

## Q15. A signal while the result is being written

**Context**: On SIGINT, SIGTERM or SIGHUP the overview prints no result
document and exits with that signal's status, which takes precedence over 1
(POD:776-780 and the packet's DI:1094-1096; spec FR-044), and on exit 0 or
1 it prints the full result (POD:767). The change's scenarios send the
signal during collection (POD:792-799), and design D1 handles signals
around the collection loop, while rendering follows that loop (design D6).
A signal that arrives after the first byte of the result reaches standard
output, and before the last, cannot meet both rules: the bytes written
cannot be withdrawn, and exiting 0 or 1 would ignore the signal. Feature
004 decides this moment for `project clean` at `b0243e5`: its record-only
handlers stay installed "from the argument checks to the last write", so a
signal recorded while a preview or report is being written does not stop
the write, and the slot, read once more before the run exits, gives
`Cancelled.` and 130, 143 or 129 (its research.md R4, Decision;
data-model.md, the transition from `reported`). Its signal slot stores the
first signal, which decides that status, and its driver raises
`Interrupted` from it only in phase `planning` or on a second SIGINT in
phase `reconciling` (lead ruling R-44). Lane openRepoProject-2's ruling
R-55 (2026-10-20) has since decided the reader too, so that feature 004's
rule is now complete for its own report: a reader that closes the pipe
makes the first failed write point that stream at `/dev/null`, a recorded
signal outranking the error (Q12); and a stalled reader works as designed,
the residual recorded in its research.md R4: under a handler that only
records, Python resumes a write blocked on a stalled reader once the
handler returns (PEP 475), so a SIGTERM sent to the process alone waits for
the reader to drain or exit (checked on Python 3.12.3 for this question).
Question Q12 asks how a failed write ends, and its option A lets a recorded
signal decide the status over that write's exit 2; it does not ask what a
signal does to a write in progress.

**Question**: What should a signal that arrives while the result is being
written do?

**Recommended:** Option A - It keeps Ctrl-C answered even when a reader
stalls, and keeps one rule for consumers, that an exit of 129, 130 or 143
carries no result; its one mechanism, a raising span around the write, is
feature 004's `raising_signals` (R-47). Feature 004 writes its report in
full (option D) because that report records removals already made; the
overview's result records nothing a re-run cannot read again, so stopping
its write loses nothing. Rendering before writing, as Q12's option A has it,
narrows the window to the write itself.

| Option | Description |
|--------|-------------|
| A | Amend change 2's "print no result document" (POD:778-779, and the packet's rule too, DI:1094-1096) to "start no result document once the signal is read, and stop one that is being written" (FR-044 and SC-011 folded after), and record the partial result as a residual beside EC-015: the write stops at the signal, `Cancelled.` follows on standard error, and the run exits with the signal's status; standard output may then hold part of a result, which an exit of 129, 130 or 143 marks as no result. A signal recorded before the run exits decides its status, also over the exit 2 of a write that fails after it. The raising span around the write is entered before the first byte is written, so a signal recorded while rendering prints nothing, and output not yet written is discarded, never flushed at exit. |
| B | Block the three signals from the first byte of the result to the last, then exit 0 or 1 as the result says, dropping the signal; a consumer that stops reading the pipe then leaves the run unstoppable by Ctrl-C until it reads. |
| C | Leave it to the plan, fixed once and recorded in the feature's traceability record. |
| D | Follow feature 004's rule for `project clean` (its research.md R4): the handlers stay record-only through the write, so the result is written in full; the slot, read once more before the run exits, gives `Cancelled.` on standard error and the signal's status, 130, 143 or 129. Amend change 2's "print no result document" (POD:778-779, and the packet's rule too, DI:1094-1096) to "start no result document once the signal is read". A reader that stops reading leaves the signal unanswered until the write completes or fails. |

---

## Q16. Spawning Git children with signals blocked (change 2's design D1)

**Context**: Design D1 starts each child and enters it in the in-flight
registry "while SIGINT, SIGTERM and SIGHUP are blocked with
`signal.pthread_sigmask`", unblocking them only after registration, so that
no signal can fall between `Popen` and the registry (design.md:115-119), as
clarifications N1 asks (clarifications.md:45-47). A child started with
`Popen` inherits that mask, and Git does not reset it: reproduced on Git
2.43.0 and Python 3.12.3 for this question (runtime cross-check X-7),
`git hash-object --stdin` started with the three signals blocked shows
`SigBlk: 0000000000004003` in its `/proc` status and is still alive after
SIGTERM to its group, needing SIGKILL, while one started unblocked dies at
once. Every stop would then wait out the 2 s grace and need SIGKILL, at a
budget, at the deadline or after a signal, and also FR-011's stop at a
record bound (C-2); that cost is stated per stop, and whether a terminating
child frees its concurrency slot during the wait is not in design D6, so
its scale cost at record-bound stops is not quantified. The packet's rule,
that a child stopped early "receives SIGTERM to its process group, then
SIGKILL if it has not exited within 2 s" (DI:461-464), and [E]'s
(CMD:177-179) are met either way, and neither names a mask. Feature 004's
child start blocks nothing, and its handlers only record the signal (its
research.md R4), so no termination pass can miss a child: that is the
guarantee D1 wanted, and nothing in feature 004, its code included, or in
this spec names `pthread_sigmask`. The alternative, a pre-exec hook that
clears the mask in the child, is ruled out by change 1's correction C4,
which change 2's proposal repeats (Corrections to the Packet, "Process
groups on Python 3.10"): every Git child starts with
`start_new_session=True`, never `preexec_fn`.

**Question**: How should feature 005 start its Git children?

**Recommended:** Option B - The ratified design then stays true, rather
than carrying a standing departure, at no cost beyond the amendment the
answers already need.

| Option | Description |
|--------|-------------|
| A | Depart from design D1's spawning paragraph and the line of clarifications N1 that asks for the block, recorded as a departure on Brett Heap's word, as feature 004 records its own (its R-32), and start each child unblocked under handlers that only record the signal. |
| B | Amend change 2, in the same amendment that carries the other answers: design D1's spawning paragraph (design.md:115-119) and the spawn line of clarifications N1 (clarifications.md:45-47) change so that each child starts with SIGINT, SIGTERM and SIGHUP unblocked, and N1's "or raise a `BaseException` subclass" (clarifications.md:42-44) is struck, so that the handlers only record the signal, as D1's signals paragraph already has them (design.md:103-107), which keeps a termination pass from missing a child; FR-011 and FR-044 are folded after. |
| C | Keep D1 and N1 as written, and accept the 2 s wait and SIGKILL on every stop. |

---

## Q17. The open changes that modify change 2's overview (#24 and #25)

**Context**: Lane openRepoProject-5 has two open, unratified OpenSpec
changes that modify change 2's `project-overview` delta.
`add-project-overview-remote-merge-status` (issue #25, PR #29) keeps
"Overview is local and read-only", "Overview bounds its work and reports
what it omitted" and "Overview prints a versioned JSON envelope" whole,
adds to each a paragraph that applies only under `--remote`, and adds
"Overview reports remote merge evidence on request". Its feature is created
only after feature 005 merges and change 2 archives (its `tasks.md` 2.1 and
2.2), and its Open Question 3, addressed to lane openRepoProject-4,
recommends that feature 005 reserve no flag, field or hook.
`add-project-clean-cache-disposal` (issue #24, PR #27) lets `project clean`
classify a merged worktree whose only ignored files are Python bytecode
caches `merged-removable`, on evidence the overview does not collect, and
MODIFIES change 2's "Overview reuses the cleanup classifier and merge
target" with the two sentences lane openRepoProject-4 agreed at `9f30fb9` (the
words "for the same working directory and refs" agreed at `4d5855a`, unchanged
at `fffc194`): the overview classifies such a row `ignored-local-files`, and
never classifies a row `merged-removable` where `project clean` classifies it
otherwise for the same working directory and refs. It also names the
ignored file of "Every protected classifier" as not a Python bytecode
cache, and adds the scenario "Caches that only project clean proves
disposable". The overview's code is the same either way. That change does
the work on feature 005's side in its own feature, "once feature 005 has
landed ... never in feature 005" (its proposal, Impact), and its feature
writes the added scenario's test (its design D14); but its proposal also
says that feature "does not wait for feature 005" (Dependencies and
Sequencing). If it merges first, FR-026 and SC-003 would no longer hold for
cache-only rows when feature 005 is built against that `main`, a feature
005 fixture whose ignored file is a `.pyc` fails its parity test, and the
added scenario has no overview to run against. Taking the block into
feature 005 before the cache-disposal code exists would leave that
scenario's test unable to pass, and FR-049 counts no skipped test. Change 2
rules that each extension needs a proposal of its own (OQ-27, in change 2's
proposal.md:560-568 and :631, on OV:357-359) and lists cache disposal and
remote queries in its Out of Scope (proposal.md:565-568, on OV:142-146);
spec.md's Out of Scope names both.

**Question**: Should feature 005 realize the overview parts of #24 and #25
if they are ratified before its plan, or leave them to their own features?

**Recommended:** Option A - It is the order #25 sets (its tasks 2.1 and
2.2, `tasks.md:20-21` at `67e43ae`), and #24 allows it: #24 does not wait
for feature 005 (its `proposal.md:601-602` at `fffc194`) and says its
overview part is done in its own feature, never in feature 005
(`proposal.md:545-548`). It costs nothing now: the overview's code is the
same, and fixtures with an ignored `local.env` keep feature 005's parity
tests true in every order, so the plan is the same whichever realization
merges first and no second plan is needed. Its one cost is that departure,
in the order where #24's code merges first; option B avoids the departure,
by asking lane openRepoProject-5 to re-sequence #24, but not the divergence,
which #24's design makes in every order once its code is on `main`
(`design.md:592-595` and D14, `:1036-1042`, at `fffc194`).

| Option | Description |
|--------|-------------|
| A | Leave both to their own features in every order, as #25 sets and as #24 states for its overview part ("never in feature 005"). Feature 005 builds change 2 as ratified and as the other answers amend it, reserves no flag, field or hook for `--remote`, and gives every fixture it compares with `project clean` that has an ignored file one such as `local.env`, which no cache rule #24 proposes admits. If #24's realization merges first, a cache-only worktree is `ignored-local-files` in the overview and `merged-removable` in `project clean`: a departure, on Brett Heap's word, from change 2's equality clause (POD:381-386, on DI:620-624), which #24's own design calls "against change 2's equality clause" (its `design.md:592-595` at `fffc194`), until #24's overview block is archived, after which that block records the same divergence as a lasting exception. In the other order, the same divergence arrives with #24's code as #24's own change: its D14 excludes the cache case from feature 005's parity tests once feature 005 has landed. So the divergence reaches `main` in every order, and only the departure belongs to the #24-first order. It is the cautious direction, and no feature 005 test depends on it. |
| B | As A, and ask lane openRepoProject-5 to amend #24 so that its realization merges after feature 005, its proposal and tasks saying so. |
| C | Realize #24's block in feature 005 whenever #24 is ratified before feature 005's plan, whatever order the realizations merge in: a departure from #24's order, from OQ-27 and from change 2's Out of Scope, on Brett Heap's word. Feature 005 then cannot merge until #24's code is on `main`, since the added scenario's test cannot pass before it and FR-049 counts no skipped test. #25 stays its own feature. |
| D | Realize both in feature 005 if they are ratified before its plan, departing from the order of both, from OQ-27 and from change 2's Out of Scope on Brett Heap's word: `--remote` joins this feature, adding one requirement and 16 scenarios to the overview, and #25's `project-command` block, which MODIFIES [E] on draft PR #19's text (10 scenarios, one added). Feature 005 then inherits #25's dependency on PR #19 and on feature 004's runner (`proposal.md:311-322`, `:344-347` and `:407-415` at `67e43ae`), and amends spec 005's Out of Scope and Dependencies, which reverses "`--remote` stays an invalid invocation here", and the two requirements that sentence cites: FR-039 (an argument error prints usage and no JSON) and FR-042 (exit status 2 for an invalid invocation). It also changes FR-040 as #25's remote-only paragraph of "Overview is local and read-only" has it (its `spec.md:13-29` at `67e43ae`): the network clause stops binding the `gh` children that `--remote` runs, which make network requests, and only them, the `project` process and every Git child staying bound; the credential clause is replaced; and both outputs gain a "queried live" label beside "as of the last fetch". SC-002 stays true: its audit hook watches the `project` process, which opens no connection in a `--remote` run (#25's scenario "A remote run stays read-only apart from its queries", `spec.md:36-39`). |

---

You can reply with the option letter for each question (e.g., "Q1 A, Q2 A,
Q3 B, Q4 D, Q5 A, Q6 A, Q7 A, Q8 D, Q9 B, Q10 A, Q11 A, Q12 A, Q13 A,
Q14 A, Q15 A, Q16 B, Q17 A"),
accept every recommendation by saying "yes" or "recommended", or give your
own short answer for any of them.

**Path**: `specs/005-project-overview/clarify-questions.md`
