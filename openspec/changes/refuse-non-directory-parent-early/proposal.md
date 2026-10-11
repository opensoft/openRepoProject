Lane: openRepoProject-1

# Proposal: refuse-non-directory-parent-early

Status: draft; alignment review and council round 1 applied (draft PR #21);
the rest of the council, design, spec delta and governance tasks follow;
nothing is ratified. Governing issue: opensoft/openRepoProject#20, claimed by
lane openRepoProject-1. Proposed on Brett Heap's word "propose the
non-directory parent follow-up as a new change" (2026-10-11).

Source: `openspec/changes/archive/2026-10-09-fix-parent-obstacle-wording/`
left two limitations to their own change: its design D6 ("An earlier refusal
is its own change, on Brett Heap's word") and the `FILE/sub` dead end of its
proposal's Out of Scope, recorded by feature 003 as EC-003 and EC-002
(`specs/003-parent-obstacle-wording/spec.md:130-138`), respectively. This
change is that earlier refusal.

## Why

`project new` resolves the parent once (`project:322`), but only the Triad
paths check whether it is a directory: the question names it
(`known_obstacles()`, `project:235-254`) and the shape branch refuses it
(`project:371-372`). The single-repository path prints `Create:` and the plan
(`project:392-393`), returns 0 on `--dry-run` (`project:394-395`), asks for
`yes` (`project:396-397`), and only then reaches
`parent.mkdir(parents=True, exist_ok=True)` (`project:398`), whose `OSError`
`main()` prints as a raw errno with exit 2 (`project:1143-1148`). So a person
confirms a plan that cannot run, a dry run reports success for a run that
cannot succeed, and for a missing parent below a file the question says only
"does not exist" while the README says that a single-repository answer
creates a missing parent (`README.md:60-61`).

This change covers only what the existing pathlib reads decide with
certainty: a parent blocked by a non-directory. A parent the person cannot
write keeps today's late failure and a dry run that exits 0; rewording that
backstop's raw error is a possible follow-up, not part of this change.

### Observed

At this branch's base `961c405`, Python 3.12.3 in `py-bench`, with the hand
fixture of `specs/003-parent-obstacle-wording/quickstart.md` (a fake bench
generator, a fake `openRepoShape` that never ran, `CI` empty or unset, a pty
for the asked runs), the name `MyApp`, the parent given by `--into`. `FILE` is
a regular file; every run left it a regular file with its content.

| Parent | `--type test`, `yes` | its `--dry-run` | asked: `2`, `yes` | asked: Enter | `--shape --org example --visibility private` |
| --- | --- | --- | --- | --- | --- |
| `FILE` | L17 | P0 | Qa, L17 | Qa, Ta | S |
| a symbolic link to `FILE` | L17 | P0 | Qa, L17 | Qa, Ta | S |
| a FIFO | L17 | P0 | Qa, L17 | Qa, Ta | S |
| `FILE/sub` | L20 | P0 | Qm, L20 | Qm, Tm | S |
| `FILE/a/b` | L20 | P0 | Qm, L20 | Qm, Tm | S |
| a dangling symbolic link | C | P0 | Qm, C | Qm, Tm | S |
| missing, below a directory | C | P0 | Qm, C | Qm, Tm | S |

- L17: `Create: PARENT/MyApp`, the plan, `Type yes to run this plan:`, then
  `REFUSED: [Errno 17] File exists: 'PARENT'`, exit 2, nothing created. L20:
  the same, ending `REFUSED: [Errno 20] Not a directory: 'PARENT'`.
- P0: `Create:` and the plan, exit 0; the answer `2` with `--dry-run` gave P0
  in every row too. C: the plan, `yes`, the parent and the repository
  created, exit 0 (by flag with the two `warning:` lines, by answer with none).
- Qa, under entry 1: `Not possible here: The parent PARENT exists but is not a
  directory; choose a parent that is a directory.` Qm: `Not possible here: The
  parent directory PARENT does not exist; a Triad is created inside an
  existing directory.` Ta, Tm: `REFUSED: A Triad cannot be created here.`, the
  same sentence, `Nothing was created.`, exit 2, no further prompt.
- S: `REFUSED: Shape creation requires an existing --into parent directory.`,
  exit 2, before `Create:`, with `--dry-run` too.

PARENT is the resolved path (a link is named by its target). Also observed,
with `--yes`: a socket, `/dev/null`, `FILE/`, and `FILE` as the positional
parent, `PROJECTS_DIR` or `~/projects` give L17 without the prompt. A link to
a path below `FILE` behaves as the `FILE/sub` row: L20 by flag, P0 on
`--dry-run`, Qm and Tm asked. With `FILE` as parent, `--type nomatch`, `--org`
without `--shape`, and `--workflow` without `setup-openspeckit` are refused by
their own sentences before `Create:`, exit 2; a workspace name, not asked
(`alice-wip --into FILE --dry-run`), prints the plan and exits 0.
`is_dir()` is False in every row and `exists()` True only in the first three;
the nearest existing path above the parent is `FILE` for `FILE/sub`,
`FILE/a/b` and that link, and a directory for the last two. As uid 1000, a
missing parent below a directory of mode 555 passes `--dry-run` (exit 0) and
is refused after `Create:` and the plan with `REFUSED: [Errno 13] Permission
denied: 'PARENT'`, exit 2; an existing parent of mode 555 passes
`parent.mkdir`, and the generator fails with its own error and status.

## What Changes

- **The term** (recommended; Alternatives below): a parent blocked by a
  non-directory is one where the resolved parent, or the nearest existing
  path above it, exists and is not a directory. Case (a), the parent itself:
  a regular file, a symbolic link to one, a FIFO, a socket, a device, `FILE/`.
  Case (b), the nearest existing path above a missing parent: `FILE/sub`,
  `FILE/a/b`, a symbolic link to such a path. The read stays pathlib and
  local: `is_dir()`, then `exists()`, then `exists()` up `parent.parents` to
  the first that exists, then its `is_dir()`; no network, subprocess or new
  import. A missing parent whose nearest existing path above is a directory
  (a dangling link's target included) is not blocked (observed: C). No
  permission is read.
- **Reads.** The question and the Triad refusal keep one read, as today
  (archived D1: the refusal composes the sentence the question printed, so
  the two cannot diverge). The head refusal below reads the parent afresh
  when it is reached, on every path, by flag or by an answer `2`: a parent
  repaired while the question waits is then created, as today, and one broken
  during the wait is refused at the head. The question's line and the head
  refusal can therefore differ when the parent changed during the wait; that
  is intended, as the refusal reflects the parent at the decision.
- **One refusal at the head of the single-repository path**, after the
  check refusing shape-only flags (`project:383-384`) and before generator
  selection (`choose()`, `project:385`): before the late `--workflow` check
  (`project:388-390`), `Create:`, the plan, the dry run's return, `yes` and
  any creation. The flag-chosen path, an invocation not asked (`CI` set, no
  terminal, a workspace name) and an answer `2` reach it alike, the answer at
  once, with no generator list, plan or `yes` prompt; their dry runs exit 2,
  not 0. Earlier refusals keep their place: the name, a positional parent with
  `--into`, the family form, an existing destination, and when asked the
  hoisted `--workflow` check (`project:336-337`) and the question. A not-asked
  invocation with a fault found later (workBenches or its registry, the
  generator, the late `--workflow` check) now gets the parent sentence first,
  still exit 2.
- **The shape branch is unchanged**: its refusal (`project:371-372`) already
  comes before `Create:` and the dry run's return (observed: S), and the
  precedent kept it as an explicit non-change (archived design D6).
- **The question is still asked** for a parent blocked by a non-directory.
  For (a) its line under entry 1 stays the precedent's, byte for byte; for (b)
  it names the parent with the new sentence instead of the missing sentence,
  which stays byte for byte for a missing parent that is not blocked. The
  Triad answer's composed refusal and its dry run carry the sentence the
  question printed, as today; an answer `2` is refused at the head of its path.
- **Fixed sentences**, ASCII; PARENT and ANCESTOR are resolved paths:
  - (a), verbatim from the archived design D2: `The parent PARENT exists but
    is not a directory; choose a parent that is a directory.`
  - (b), new: `The parent PARENT cannot be created because ANCESTOR exists but
    is not a directory; choose a parent that is a directory.` It names the
    resolved parent and the path that blocks it, with the same repair.
  - The single-repository refusal is the sentence, then ` Nothing was
    created.`, printed by `main()` as `REFUSED: ...` on standard error, exit 2,
    like every `Refused`; one text by flag or by answer, with or without
    `--dry-run`. For `FILE`: `REFUSED: The parent FILE exists but is not a
    directory; choose a parent that is a directory. Nothing was created.`
- **The permission boundary is stated, not checked**: `--dry-run` reads no
  permissions; a parent that is, or lies below, a directory it cannot write
  still passes the dry run and fails at creation, as before (below such a
  directory, `parent.mkdir` is refused with the system's error; in it, the
  generator's own error and exit status pass through).
- **The late refusal stays as the backstop**: `parent.mkdir` (`project:398`)
  and `main()`'s `OSError` handler are unchanged, for a parent changed after
  the head read, one that cannot be written, a read-only mount or a full disk;
  nothing is added.
- **`README.md`** (texts fixed by the design, checked by a grep): lines 57-64
  say that a parent blocked by a non-directory blocks both answers, that
  neither answer can create anything in such a parent, and that it is refused
  at once on either, while an answer `2` still creates a missing parent below
  a directory; lines 92-98, that it is refused before the plan, `--dry-run`
  included, and the permission boundary sentence above; lines 75-77 (a
  choosing flag restores "exactly" the path of before the question) gain a
  clause for this new refusal; lines 79-82 ("a dry run at a terminal asks
  too, then prints the plan of the path its answer chose and writes nothing")
  gain "unless the parent is blocked by a non-directory, which is refused".
  Lines 53-55 need nothing.

### Alternatives

- **Where.** (W1) The head of the single-repository path: recommended; no
  prompt after the question, and the ratified question line stays reachable.
  (W2) Just before `Create:` (`project:392`): every existing refusal keeps
  its outcome, but an answer `2` can still meet the generator list and its
  prompt first. (W3) Before the question, after the existing-destination
  refusal (`project:328-329`), for every path: no question whose two answers
  both fail, one check for all paths; rejected, since the ratified (a) line
  and its Triad refusal become unreachable, the shape-by-flag text changes for
  (a) and (b), path argument refusals (such as `--shape` without `--org`) give
  way to it, and the spec's list of refusals before the question changes.
- **The (b) wording.** Sentence (a) naming ANCESTOR is false of the parent
  given; keeping the missing sentence in the question would imply a creation
  that the answer `2` then refuses.
- **The composition.** A Triad-like prefix `A single repository cannot be
  created here. ` (a flag-chosen path never says "a single repository"
  outside the advisory); or the bare sentence (not saying the file was spared).
- **Rejected**: rewording the errno at `parent.mkdir` (the plan and `yes`
  still come first, the dry run still exits 0); a raw `os.stat` classified by
  errno (archived N5); changing nothing (the dry run's exit 0 is false).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

`project-command`: one ADDED and four MODIFIED requirements. Scenario titles
are provisional; the ADDED ones take a stem distinct from the existing titles
at `openspec/specs/project-command/spec.md:127`, `:136`, `:240`, `:251`.

- ADDED: "A parent blocked by a non-directory is refused before the
  single-repository path's steps". Its text defines the term, reads the
  parent afresh at the head, and states the permission boundary sentence
  above. Scenarios: "A flag-chosen single repository with a parent that is
  not a directory"; "A flag-chosen single repository below a path that is not
  a directory"; "A single-repository dry run with a parent blocked by a
  non-directory"; "A single repository taken at the question with a parent
  blocked by a non-directory"; "A parent repaired or broken while the question
  waits"; "A single repository with a parent that is not blocked"; "A parent
  the person cannot write still fails only at creation"; "The parent refusal
  comes after the earlier refusals and before generator selection"; "The
  shape branch's parent refusal is unchanged".
- MODIFIED: "Delegate project creation" (`spec.md:7-42`): "Preview"
  (`:25-28`) gets a qualified WHEN, such as "a creation path is chosen and no
  refusal precedes its plan", which also covers the precedent's Triad dry-run
  exception without changing behaviour; the design fixes the wording.
- MODIFIED: "Creation question is asked only of a person choosing at the
  terminal" (`spec.md:70-138`): its statements of an unchanged path for an
  invocation not asked gain the exception for a parent blocked by a
  non-directory, refused at the head of the single-repository path after the
  shape-only flag check and before generator selection, the late `--workflow`
  check, `Create:`, the plan, `yes` and any dry-run return.
- MODIFIED: "Creation question offers the Triad first" (`spec.md:140-198`):
  its prose (`:160-163`) and "Answers that take a single repository"
  (`:174-177`) are qualified for a parent that is not blocked by a
  non-directory.
- MODIFIED: "Known Triad obstacles are named before the question and refused
  on a Triad answer" (`spec.md:200-263`). The parent fact gains case (b) and
  its read; "A single-repository answer SHALL be unaffected by these facts"
  narrows to the name and openRepoShape facts and a missing parent that is not
  blocked, citing the ADDED requirement; "These checks SHALL predict only
  refusals openRepoShape is certain to make" (`:224-225`) is scoped to their
  Triad use, since the head refusal predicts `parent.mkdir`. "The parent
  directory is missing" keeps its title, its WHEN narrowed to a parent whose
  nearest existing path above is a directory; "The parent exists but is not a
  directory" and "No known obstacle" stay; "The parent would be created below
  a path that is not a directory" is new; "A Triad answer with a known
  obstacle" and "A dry run with a known obstacle" gain case (b); "A
  single-repository answer is unaffected" keeps its title, its WHEN narrowed
  to obstacles that do not block a single repository.

### Statements this change makes false, and their treatment

In `openspec/specs/project-command/spec.md`, each for a parent blocked by a
non-directory; every one is MODIFIED, none left to an override:

- "Delegate project creation", scenario "Preview" (`:25-28`): MODIFIED, its
  WHEN qualified.
- "Creation question is asked only of a person choosing at the terminal",
  prose "Every invocation that is not asked the question SHALL keep its
  existing order of refusals" (`:94-95`): MODIFIED.
- Same requirement, scenarios "A choosing flag skips the question"
  (`:103-106`), "A workspace name" (`:117-120`), "A dry run asks too"
  (`:122-125`) and "The refusal order of an invocation not asked the question
  is unchanged" (`:136-138`): MODIFIED.
- "Creation question offers the Triad first", prose (`:160-163`) and scenario
  "Answers that take a single repository" (`:174-177`): MODIFIED, qualified
  with the term.
- "Known Triad obstacles are named before the question and refused on a
  Triad answer", prose (`:223-225`) and scenario "A single-repository answer
  is unaffected" (`:256-259`): MODIFIED.

## Impact

- **`project`**: one helper reading whether the parent is blocked by a
  non-directory, called by `known_obstacles()` (`project:247-253`), whose one
  read feeds the question and the Triad refusal, and afresh at the head of
  the bench branch (`project:382-385`) on every path; one new sentence.
  Unchanged: `main()`, the shape branch, `parent.mkdir`, `choose()`, the
  question's printing and prompts, everything from `discover`
  (`project:433`) down; nothing new imported.
- **Feasibility, observed** on a scratch copy at `961c405`, not committed:
  W1 printed the sentences above in every (a) and (b) row, refused both dry
  runs with exit 2, left the unblocked rows as they are, and failed only
  `test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path`,
  which pins today's late refusal (and a `.specify/` test the copy lacks).
  The copy read the parent at the question and again at the head, as above.
- **`tests/test_project.py`**: that one test is rewritten to the early
  refusal. New cases, each asserting the tree unchanged and `FILE` intact,
  per the acceptance criteria below; case (b) as new rows of
  `known_obstacle_cases()`, existing rows unchanged; a test pinning the late
  permission refusal, skipped when `os.geteuid() == 0`.
- **`README.md`** lines 57-64, 75-77, 79-82 and 92-98; the spec at archive.
- **Feature records** stay unedited; the new feature's spec states that, for
  the two cases, it supersedes: in `specs/003-parent-obstacle-wording/`,
  spec.md EC-002 and EC-003 (`:130-138`), FR-008 (`:180-183`), SC-005
  (`:214-216`), User Story 3's intro (`:94-97`) and acceptance scenario 4
  (`:116-122`), the Assumptions baseline (`:249-252`), and quickstart.md
  `:116-125` (the dry run exiting 0); in `specs/002-triad-first-project-new/`,
  spec.md User Story 3 scenario 6 (`:163-165`), FR-004 (`:317-320`), the end
  of FR-008 (`:342-343`), FR-011 (`:359-363`) and FR-013 (`:377`).
- **Traceability, for the realization**: feature 003's traceability.md row 7
  (`:25`) points at the test being rewritten; the new feature's traceability
  maps that test to the ADDED single-repository scenario, and keeps
  `test_pty_single_answer_is_unaffected_by_obstacles` for the narrowed "A
  single-repository answer is unaffected".
- **Speckit handoff**: one feature, numbered when `/speckit.specify` runs
  from a main synced to origin (the next free number; none hard-coded). Lane
  openRepoProject-2's ratified `add-project-clean-all-safe` (feature 004, in
  progress) and `add-project-overview` (005 expected) edit `project` below
  `discover` and their own tests; this one edits `new()`, `known_obstacles()`
  and the creation tests. Whichever realization merges second merges main in
  (no rebase, no force push).
- **Handoffs after landing**: no new issue; whether one comment on
  workBenches#145 (open) names the realization as a pin target, as archived
  D5 did, is the design's to decide.

## Acceptance criteria

On Python 3.10 and 3.12 (CI), each by a test:

1. Kinds: (a) a regular file, a symbolic link to a file, a FIFO and `FILE/`
   (a socket and `/dev/null` optional: an AF_UNIX path can be too long on
   macOS CI), given by `--into`, the positional parent, `PROJECTS_DIR` and
   the default `~/projects`; (b) `FILE/sub` and `FILE/a/b` by `--into`. Each
   with `--type test` (with `--yes`, at a pty without it, and with
   `--dry-run`), and not asked without a choosing flag (`CI=true`, a
   non-terminal stdin, a workspace name), exits 2 with the fixed refusal
   line, no `Create:`, plan or `yes` prompt, and nothing changed.
2. Asked, `2`, with a registry of two available generators (so `choose()`
   would print its list and ask `Select a generator number`, `project:198`):
   the question's line, then the refusal of 1 at once, with no list, no
   `Select a generator number`, no `Create:`, no `Type yes to run this plan:`;
   exit 2; nothing changed; `--dry-run` too. (With one generator `choose()`
   prints nothing, `project:194`, so W1 and W2 would look alike.)
3. Asked, Enter: (a) as today; (b) the new line and refusal, its dry run too.
4. A missing parent below a directory, and a dangling link: as today.
5. The earlier refusals and the shape-by-flag refusal keep their text; every
   added line is ASCII; every existing test passes unchanged but
   `test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path`,
   which is rewritten to the early refusal.
6. With a parent blocked by a non-directory, `--type nomatch` and
   `--workflow` without `setup-openspeckit` exit 2 with the parent refusal;
   `--org` without `--shape` keeps its own sentence.
7. The README edits are checked by a grep of their fixed text, as feature
   003's quickstart did.
8. In process, with the answer prompt patched to replace `FILE` by a
   directory before answering `2` and `yes`, the repository is created, exit
   0; mirrored, with a directory parent replaced by a regular file before
   answering `2`, the head refusal (a), exit 2, nothing created.
9. The permission boundary is pinned: a missing parent below a directory of
   mode 555 passes `--dry-run` (exit 0) and, with `--yes`, is refused after
   `Create:` and the plan with `REFUSED: [Errno 13] Permission denied`, exit
   2; skipped when `os.geteuid() == 0`.

## Risks

- For a parent blocked by a non-directory no answer to the question can
  succeed: one answer is wasted, and the Triad refusal does not say that the
  single repository is blocked too (W3 would not ask; rejected above).
- Two-fault invocations name the parent first (exit status unchanged).
- The question's line and the head refusal can differ when the parent changed
  during the wait (intended); a parent changed after the head read meets the
  `parent.mkdir` backstop, as today.
- A parent the person cannot write still passes the dry run (stated in the
  requirement and the README); the files shared with lane openRepoProject-2
  need main merged in.

## Out of Scope

- A raw `os.stat` classified by errno: the pathlib reads suffice (N5).
- A new flag, environment variable or configuration file: none is needed.
- A line under entry 2: a new form of the question, beyond this change.
- The Triad answer's refusal text and composition: only the (b) sentence
  enters, as a parent sentence.
- The shape branch's sentence: already early and true (archived D6).
- Permissions, read-only mounts and a full disk: a writability read predicts
  refusals the system may not make (root, ACLs), so they keep today's late
  failure, stated as the boundary above; rewording the backstop's raw error
  is a possible follow-up. An unsearchable ancestor is already refused at
  `destination.exists()` (`project:328`) on 3.10 and 3.12.
- The archived N1 residuals (3.13 and later loop, 3.14 unsearchable
  ancestor): versions CI does not run; by that record (not run here) the new
  read classes them as not blocked, so they behave as today.
- The CI matrix (3.10 and 3.12, Linux and macOS) and "Python 3.10+": the
  realization's tests run on both as the matrix stands.
- Everything from `discover` down and every subcommand but `new`: lane
  openRepoProject-2's surface, or untouched.
- workBenches, openRepoShape, setup-openspeckit and the archived changes:
  other owners' code, or immutable records.
