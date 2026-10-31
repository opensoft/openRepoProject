Lane: openRepoProject-1

# Clarify questions: feature 006-refuse-non-directory-parent-early

**Questions file**: `/workspace/projects/openRepoProject-worktrees/006-refuse-non-directory-parent-early/specs/006-refuse-non-directory-parent-early/clarify-questions.md`

**Spec**: `specs/006-refuse-non-directory-parent-early/spec.md` at `447f2a8`
(base `b233333`).

**Packet**: `openspec/changes/refuse-non-directory-parent-early/`, ratified by
Brett Heap ("ratify 21", 2026-10-21).

**Drafted**: 2026-10-21 by lane openRepoProject-1's clarify drafter. Answered
2026-10-22 by Brett Heap, verbatim "all recommended"; recorded in spec.md's
Clarifications (Session 2026-10-22).

**Corrected**: 2026-10-21, before any answer was given: Q5's precedent and option A now say that feature 003 ticked 2.2 after its first implementation commit, not before (`90a4cee` left it open; `f401e06` has it ticked).

**Count**: 5 questions (cap 25). The spec writer recorded 5 ambiguities. Two
of them are asked here (Q1, Q2). The other three are decided by the packet's
text and dropped (see "Decided by the packet"). The coverage scan added three
questions (Q3 to Q5).

**How to answer**: for each question, reply with the option letter, "yes" or
"recommended" for the recommended option, or a short answer of 5 words or
fewer. For example: "Q1 B, Q2 A, Q3 recommended, Q4 B, Q5 A".

Line citations are at `447f2a8`, where `project`, `tests/test_project.py`,
`README.md` and the change's files are as at `b233333`. Main has since moved to
`15504f1` (#28), which adds only
`openspec/changes/support-later-python-versions/` and changes none of the cited
files.

## Questions

### Q1. How broad is the test matrix for the head refusal?

The proposal's acceptance criterion 1 (AC1) lists the kinds:

- "(a) a regular file, a symbolic link to a file, a FIFO and `FILE/` ...,
  given by `--into`, the positional parent, `PROJECTS_DIR` and the default
  `~/projects`";
- "(b) `FILE/sub` and `FILE/a/b` by `--into`".

It then says "Each with `--type test` (with `--yes`, at a pty without it, and
with `--dry-run`), and not asked without a choosing flag (`CI=true`, a
non-terminal stdin, a workspace name)".

`design.md` D3 is narrower in two places:

- Item 2 runs `--type test` without `--yes` at a terminal "for `FILE` and
  `FILE/sub`" only.
- Item 3 runs the three not-asked ways with "the file as `--into`" only.

The spec's Assumptions ("Test breadth") and SC-001 make D3's matrix the
minimum, so the plan is left to choose any wider set.

Below, "kinds" means D3 item 1's seven required kinds:

- case (a): `FILE`, a link to `FILE`, a FIFO and `FILE/`;
- case (b): `FILE/sub`, `FILE/a/b` and a link to `FILE/x`.

Q3 decides the socket and `/dev/null`. In every option, the runs that answer
`2` stay at `FILE` and `FILE/sub`, since AC2 and D3 item 4 name no other kind.
Cost: at `447f2a8` on Python 3.12.3, 13 terminal runs took 1.18 s, about
0.09 s each.

**Recommended:** Option B - every kind meets every form AC1 names, and every
route meets every form through the file, so no reading of "each" is left open
to review. C's extra pairs differ only in how `new()` resolves the parent,
which happens before the step is reached.

| Option | Description |
| --- | --- |
| A | D3's matrix exactly, the spec's reading. Every kind by `--into` with `--yes` and with `--dry-run`. The file also by the positional parent, `PROJECTS_DIR` and `~/projects` in those two forms. `FILE` and `FILE/sub` at a terminal without `--yes`. `FILE` alone in the three not-asked ways. About 25 runs. |
| B | AC1's six forms for every kind. Each kind by `--into`, and the file by each of its three other routes, in all six forms: `--yes`, `--dry-run`, a terminal without `--yes`, `CI=true` at a terminal, a standard input that is not a terminal, and `alice-wip` at a terminal. About 60 runs, 30 of them at a terminal. |
| C | The full cross product. Every case (a) kind by every route it can take (`FILE/` has no `~/projects` form), and the case (b) kinds by `--into`, each in all six forms. About 108 runs. |
| Short | Another breadth (<=5 words) |

### Q2. How do the case (b) rows prove that `FILE` stays intact (report A, A1)?

FR-014 says that every case (b) run must show that `FILE` is still a regular
file with its content, and that the tree is unchanged. Two existing tests make
that check only for a parent that itself exists and is not a directory:

- `test_pty_triad_answer_with_an_obstacle_refuses` (`tests/test_project.py:1433`);
- `test_inproc_triad_obstacle_runs_nothing` (`:1452`).

Their guard, `file_parent = parent.exists() and not parent.is_dir()`
(`:1439`, `:1460`), is False for `FILE/sub`. The new D3 item 5 rows would
therefore pass through them unchecked.

On one side, the packet says that one existing test changes:

- `clarifications.md` N3: "Exactly one existing test changes";
- the proposal's AC5: "every existing test passes unchanged but" the
  rewritten one.

On the other side, the spec's Assumptions define "unchanged" as no existing
assertion or expected value being edited. Under that definition, feature 003's
`f401e06` added this very guard to feature 002's two tests.

The dry-run obstacle test needs neither option. It already checks the tree for
each row and the file after its loop (`:1494-1502`).

**Recommended:** Option A - it keeps N3's "exactly one existing test changes"
and AC5 true to the letter, at the cost of running two rows once more (about
0.2 s).

| Option | Description |
| --- | --- |
| A | A new test, the spec's choice. It takes each case (b) row of `known_obstacle_cases()` through a Triad answer at a terminal and in process, as the two existing tests do, and checks `FILE` and the tree. The two existing tests stay byte for byte. |
| B | Widen the guard in the two existing tests. The guard also holds for a missing parent whose nearest existing path is not a directory, and the check reads that path. No assertion or expected value changes, which is feature 003's precedent. |
| Short | Another way (<=5 words) |

### Q3. Are the optional kinds, a socket and `/dev/null`, built?

AC1 and D3 item 1 make a socket and `/dev/null` optional: "a socket (skipped
when binding raises `OSError`, as an AF_UNIX path can be too long on macOS)
and `/dev/null`". EC-001 says that both are case (a). CI has run Linux only
since #32 (`.github/workflows/tests.yml:10`, `runs-on: ubuntu-latest`), so the
macOS reason no longer applies to CI. Neither the packet nor the spec says
whether the plan includes them.

**Recommended:** Option A - both build on the Linux CI and pin EC-001's
statement for each kind, for two more rows. The skip rule keeps a local macOS
run green.

| Option | Description |
| --- | --- |
| A | Include both, in the forms Q1 picks for the `--into` kinds. The socket is skipped when binding raises `OSError` (D3 item 1's rule). |
| B | Include `/dev/null` only. |
| C | Leave both out. |

### Q4. Which faults does the order test pin against the head refusal?

D3 item 9 tests these orders, with the file as the parent:

- the head refusal comes first, for `--type nomatch --yes` and for
  `--type test --workflow --yes` with no `setup-openspeckit`;
- their own refusals come first, for `--org example --yes` and for an invalid
  name;
- the shape-by-flag refusal is unchanged.

The spec orders two more faults that no D3 item tests:

- **An invalid `--family`** ("Family must be a single folder name.",
  `project:324`). It is refused before the head refusal (US5 scenario 2;
  the delta's "The parent refusal comes after the earlier refusals").
- **A fault in the workBenches lookup or its registry.** It is refused after
  the head refusal (US1 scenario 6, FR-003, EC-006; report A, A2). The lookup
  and generator selection are one call,
  `choose(registry(workbenches(args.workbenches)), args)` (`project:385`). A
  head check placed after `workbenches()` but before `choose()` would pass
  every run of D3 item 9.

**Recommended:** Option B - each added run is the only test of a fault that
the delta scenario or US1 scenario 6 names. C's further faults are named in
neither scenario, or share a check with a run already tested.

| Option | Description |
| --- | --- |
| A | D3 item 9 as it stands. |
| B | D3 item 9 plus two runs with `FILE` as the parent. First, an invalid `--family`, refused with its own sentence. Second, `--type test --yes` with `--workbenches` naming a directory that has no `config/bench-config.json`, refused with the head refusal and not "Cannot find workBenches; ...". |
| C | B plus: a positional parent together with `--into` (`project:321`); a malformed generator registry; and each of `--visibility`, `--family` and `--elected-by` without `--shape` (one check, `project:384`, which `--org` already pins). |

### Q5. Where are the change's governance tasks ticked, given FR-016?

FR-016 says "The records of features 002 and 003, and the OpenSpec change's
files, MUST NOT be edited". The change's own `tasks.md` needs edits before
implementation starts. On main, all three are still unticked, and the Speckit
Handoff still reads "to be created":

- 1.6: "Ratified by Brett Heap's word "ratify 21", quoted with its link on PR
  #21".
- 2.1: "verified when "Speckit Handoff" below names its feature identifier,
  branch and repo-relative `tasks.md` path, filled in once".
- 2.2: "`/opsx:apply` is not run until "Speckit Handoff" names exactly one
  feature".

Precedent: feature 003's realization PR #17 (`f401e06`) edited
`openspec/changes/fix-parent-obstacle-wording/tasks.md` on its own branch. It
ticked 1.6 and 2.1 and filled in the handoff fields at `90a4cee`, before the
first implementation commit `f492558`. It ticked 2.2 later in the same PR, and
2.2 is ticked in the squash `f401e06`. Its 3.1 to 3.3 were ticked at the archive
(#18, `d81bf8d`). This spec's Scope already leaves 3.2 and 3.3 to lane steps
after the merge.

**Recommended:** Option A - it follows the precedent, keeps the handoff record
in the PR that does the work, and needs no second PR.

| Option | Description |
| --- | --- |
| A | On this feature's branch, as PR #17 did. Before the first implementation commit, the change's `tasks.md` gets the 1.6 tick with the quote and its link, the 2.1 tick, and the Speckit Handoff fields. The 2.2 tick follows in the same PR once the first implementation step has run after reading that section, as feature 003 did. 3.1 to 3.3 wait for the archive. FR-016 narrows to the change's proposal, design, clarifications and spec delta, and to its `tasks.md` beyond those entries. |
| B | In a separate governance PR to main, before `/opsx:apply`. This branch then merges main in and never edits `openspec/`. FR-016 stands as written. |
| Short | Another place (<=5 words) |

## Decided by the packet (recorded ambiguities dropped)

- **The head refusal's end literal (report A, A3; recorded ambiguity 3).**
  `design.md` D3 item 1 lists the fixtures to add "After the precedent's
  fixture (`:58-62`), under a header naming this design's D2". Among them is
  "the literal ` Nothing was created.` for the head refusal's end", beside the
  sentence (b) literal and the composing helper. So the packet fixes a separate
  literal under the new header. Reusing `OBSTACLES_REFUSAL_END`
  (`tests/test_project.py:47`, the same value) would depart from D3 and would
  need Brett Heap's word. FR-014 already says this. Not asked.
- **The README range (recorded ambiguity 4).** The two citations describe one
  edit:
  - D2 fixes the place by its anchor text, "after "Existing destinations
    refuse."", which ends `README.md:96`. D2's "Lines 95-96" locates the
    dry-run sentence and that anchor.
  - D2's rule "the rest of its paragraph unchanged and rewrapped" bounds the
    rewrap by the paragraph, which is lines 92-98. That paragraph is the
    proposal's "92-98".
  - The proposal cites the whole paragraph for each edit in the same way:
    57-64 against D2's 60-64, and 79-82 against D2's 81-82.

  FR-012's grep check does not depend on the range. A note for the plan:
  rewrapping from the anchor to the paragraph's end leaves lines 92-95 byte
  for byte. Not asked.
- **A link to `FILE/x` as a case (b) kind (recorded ambiguity 5).** The packet
  includes it:
  - D3 item 1 lists "a symbolic link to `FILE/x`" among the required kinds;
  - D3 item 2 runs "Each kind by `--into`";
  - D1's table classes the link as "below a non-directory, ANCESTOR `FILE`";
  - the proposal's term names "a symbolic link to such a path" in case (b).

  AC1's shorter list is a subset, not a contrary rule. It stays in, as the
  spec has it. Not asked.

## Considered and not asked

- **Case (b) rows at the question beyond `FILE/sub`** (`FILE/a/b`, the link
  to `FILE/x`). `known_obstacles()` and the head step share one helper and one
  resolved parent. The head-refusal runs of Q1 therefore already exercise the
  walk and the link's naming, and D3 item 5's rows stay at `FILE/sub`.
- **A not-asked `--dry-run`**, such as `alice-wip --into FILE --dry-run`. It
  exits 0 at the base (the proposal's Observed) and takes the same branch as
  `--type test --dry-run`. The plan may add it under any answer to Q1.
- **The second generator in the registry** (D3 item 4). It can only be per
  test. The shared `setUp` registry feeds every test that answers `2` without
  `--type`, so no other reading keeps FR-014.
- **ASCII (FR-013) and the README texts (FR-012).** Both are checked by
  quickstart commands over the diff, as feature 003 did (its tasks T013, its
  quickstart.md:86-87). AC7 names that form for the README.
- **The Supersession's `:35` cell**, added beyond D4's list. It changes no
  file, test or plan task, since FR-016 keeps feature 002's records unedited.
- **An existing directory the person cannot write** (FR-010's second bullet).
  No delta scenario names it, and D3 item 10 tests only the missing child. It
  stays as today's behaviour, untested here.
- **#28 on main (`15504f1`).** It adds only its OpenSpec change. Its delta
  modifies this change's ADDED requirement, so it archives after this change.
  Its realization lands after this one and merges main in. Nothing in this
  feature's plan or tests turns on it.

## Coverage (taxonomy scan of the spec)

| Category | Status | Note |
| --- | --- | --- |
| Functional scope and behavior | Clear | Fixed by the delta and D1 to D3 |
| Domain and data model (parent case, ancestor) | Clear | D1's four kinds |
| Interaction and UX flow | Clear | Question lines and refusals are fixed text (D2) |
| Non-functional (performance, security, observability) | Clear | Local reads only, no network, nothing opened |
| Integration and external dependencies | Clear | SC-011, D5 |
| Edge cases and failure handling | Partial | Q3, Q4 |
| Constraints and tradeoffs | Clear | W1, with W2 and W3 rejected |
| Terminology | Clear | "blocked by a non-directory", "head refusal" |
| Completion signals (test breadth, governance record) | Partial | Q1, Q2, Q5 |
| Misc and placeholders | Clear | 0 markers; 3 recorded ambiguities decided by the packet |

**Questions file**: `/workspace/projects/openRepoProject-worktrees/006-refuse-non-directory-parent-early/specs/006-refuse-non-directory-parent-early/clarify-questions.md`
