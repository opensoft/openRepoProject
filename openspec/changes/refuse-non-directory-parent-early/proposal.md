Lane: openRepoProject-1

# Proposal: refuse-non-directory-parent-early

Status: draft; alignment review, council, design, spec delta and governance
tasks follow on the draft pull request; nothing is ratified. Governing issue:
opensoft/openRepoProject#20, claimed by lane openRepoProject-1. Proposed on
Brett Heap's word "propose the non-directory parent follow-up as a new
change" (2026-10-11).

Source: `openspec/changes/archive/2026-10-09-fix-parent-obstacle-wording/`
left two limitations to their own change: its design D6 ("An earlier refusal
is its own change, on Brett Heap's word") and the `FILE/sub` dead end of its
proposal's Out of Scope, recorded by feature 003 as EC-003 and EC-002
(`specs/003-parent-obstacle-wording/spec.md:130-138`), respectively. This
change is that earlier refusal.

## Why

`project new` resolves the parent once (`project:322`), but only the Triad
paths ask whether it can hold the new repository: the question names it
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

### Observed

At this branch's base `961c405`, Python 3.12.3 in `py-bench`, with the hand
fixture of `specs/003-parent-obstacle-wording/quickstart.md` (a fake bench
generator, a fake `openRepoShape` that never ran, `CI` unset, a pty for the
asked runs), the name `MyApp`, the parent given by `--into`. `FILE` is a
regular file; every run left it a regular file with its content.

| Parent | `--type test`, `yes` | its `--dry-run` | asked: `2`, `yes` | asked: Enter | `--shape` by flag |
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
parent, `PROJECTS_DIR` or `~/projects` give L17 without the prompt; a link
to a path below `FILE` gives P0 and Qm, Tm. With `FILE` as parent,
`--type nomatch`, `--org` without `--shape`, and `--workflow` without
`setup-openspeckit` are refused by their own sentences before `Create:`,
exit 2. `is_dir()` is False in every row and `exists()` True only in the
first three; the nearest existing path above the parent is `FILE` for
`FILE/sub`, `FILE/a/b` and that link, and a directory for the last two.

## What Changes

- **Which parents cannot hold the repository** (recommended; Alternatives
  below): those whose nearest existing path, at or above the resolved parent,
  is not a directory. (a) The parent exists and is not a directory: a regular
  file, a symbolic link to one, a FIFO, a socket, a device, `FILE/`. (b) The
  parent does not exist and the nearest existing path above it is not a
  directory: `FILE/sub`, `FILE/a/b`, a symbolic link to such a path. The read
  stays pathlib and local: `is_dir()`, then `exists()`, then `exists()` up
  `parent.parents` to the first that exists, then its `is_dir()`; no network,
  subprocess or new import. A missing parent whose nearest existing path above
  is a directory (a dangling link's target included) is created by
  `parent.mkdir` and not refused (observed: C). Permissions are not read.
- **One refusal at the head of the single-repository path**, after the
  check refusing shape-only flags (`project:383-384`) and before
  generator selection (`choose()`, `project:385`): before the late
  `--workflow` check (`project:388-390`), `Create:`, the plan, the dry run's
  return, `yes` and any creation. The flag-chosen path and an answer `2`
  reach it alike, the answer at once, with no generator list, plan or `yes`
  prompt; their dry runs exit 2, not 0. Earlier refusals keep their place:
  the name, a positional parent with `--into`, the family form, an existing
  destination, and when asked the hoisted `--workflow` check
  (`project:336-337`) and the question. A not-asked invocation with a fault
  found later (workBenches or its registry, the generator, the late
  `--workflow` check) now gets the parent sentence first, still exit 2.
- **The shape branch is unchanged**: its refusal (`project:371-372`) already
  comes before `Create:` and the dry run's return (observed: S), and the
  precedent kept it as an explicit non-change (archived design D6).
- **The question is still asked** when the parent blocks both answers. For
  (a) its line under entry 1 stays the precedent's, byte for byte; for (b) it
  names the parent with the new sentence instead of the missing sentence,
  which stays byte for byte for a missing parent that can be created. The
  Triad answer's composed refusal and its dry run carry the sentence the
  question printed, as today; an answer `2` is refused at the head of its path.
- **Fixed sentences**, ASCII; PARENT and ANCESTOR are resolved paths:
  - (a), verbatim from the archived design D2: `The parent PARENT exists but
    is not a directory; choose a parent that is a directory.`
  - (b), new: `The parent PARENT cannot be created because ANCESTOR exists but
    is not a directory; choose a parent that is a directory.` It names the
    parent given and the path that blocks it, with the same repair.
  - The single-repository refusal is the sentence, then ` Nothing was
    created.`, printed by `main()` as `REFUSED: ...` on standard error, exit 2,
    like every `Refused`; one text by flag or by answer, with or without
    `--dry-run`. For `FILE`: `REFUSED: The parent FILE exists but is not a
    directory; choose a parent that is a directory. Nothing was created.`
- **The late refusal stays as the backstop**: `parent.mkdir` (`project:398`)
  and `main()`'s `OSError` handler are unchanged, for a parent replaced after
  the check (say while `yes` waits) or not writable; no new exception handling.
- **`README.md`** (texts fixed by the design): lines 57-64 say that such a
  parent blocks both answers and is refused at once on either, while an
  answer `2` still creates a missing parent below a directory; lines 92-98,
  that it is refused before the plan, `--dry-run` included; lines 75-77 (a
  choosing flag restores "exactly" the path of before the question) gain a
  clause for this new refusal.

### Alternatives

- **Where.** (W1) The head of the single-repository path: recommended; no
  prompt is spent on a run that cannot succeed, and the ratified question line
  stays. (W2) Just before `Create:` (`project:392`): every existing refusal
  keeps its outcome, but an answer `2` can still meet the generator list and
  its prompt first. (W3) Before the question, after the existing-destination
  refusal (`project:328-329`), for every path: no question whose two answers
  both fail, one check for all paths; but the ratified (a) line and its
  composed refusal become unreachable, the shape-by-flag text changes for (a)
  and (b), path argument refusals (such as `--shape` without `--org`) give way
  to it, and the spec's list of refusals before the question changes.
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

- `project-command`:
  - ADDED: "A parent that cannot hold the repository is refused before the
    single-repository path's steps". Expected scenarios: "A parent that exists
    but is not a directory, chosen by flag"; "A missing parent below a path
    that is not a directory"; "A dry run with a parent that cannot hold the
    repository"; "A single-repository answer with a parent that cannot hold
    the repository"; "A parent that can be created is unaffected"; "Earlier
    refusals keep their place"; "A shape chosen by flag keeps its own
    refusal".
  - MODIFIED: "Known Triad obstacles are named before the question and
    refused on a Triad answer" (`openspec/specs/project-command/spec.md:200-263`).
    The parent fact gains case (b) and its read; "A single-repository answer
    SHALL be unaffected by these facts" narrows to the name and openRepoShape
    facts and a missing parent that can be created, citing the ADDED
    requirement. "The parent directory is missing" keeps its title, its WHEN
    narrowed to a parent whose nearest existing path above is a directory;
    "The parent exists but is not a directory" and "No known obstacle" stay;
    "The parent is missing below a path that is not a directory" is new; "A
    Triad answer with a known obstacle" and "A dry run with a known obstacle"
    gain case (b); "A single-repository answer is unaffected" keeps its title,
    its WHEN narrowed to obstacles that do not block a single repository.
  - Not modified, subject to the alignment review: "Delegate project
    creation" (its "Preview" stays general; the ADDED requirement states the
    exception, as is done for a Triad dry run) and "Creation question is asked
    only of a person choosing at the terminal" (W1 keeps its list).

## Impact

- **`project`**: one helper reading the parent's case, used by
  `known_obstacles()` (`project:247-253`) and at the head of the bench branch
  (`project:382-385`), and one new sentence. Unchanged: `main()`, the shape
  branch, `parent.mkdir`, `choose()`, the question's printing and prompts,
  everything from `discover` (`project:433`) down; nothing new imported.
- **Feasibility, observed** on a scratch copy at `961c405`, not committed:
  W1 printed the sentences above in every (a) and (b) row, refused both dry
  runs with exit 2, left the creatable rows as they are, and failed only
  `test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path`,
  which pins today's late refusal (and a `.specify/` test the copy lacks).
- **`tests/test_project.py`**: that one test is rewritten to the early
  refusal. New cases, each asserting the tree unchanged and `FILE` intact:
  the bench path by flag for each (a) and (b) kind and each route; the dry
  runs; the answer `2` refused at once, with no generator prompt, `Create:`
  or `yes` prompt; case (b) as new rows of `known_obstacle_cases()`, existing
  rows unchanged; creatable parents unaffected; earlier refusals and S kept.
- **`README.md`** lines 57-64, 75-77 and 92-98; the main spec at archive.
- **Feature 003's record** stays unedited; the new feature's spec states
  that it supersedes EC-002, EC-003, FR-008's "unaffected" and SC-005
  (`specs/003-parent-obstacle-wording/spec.md:130-138`, `:180-183`,
  `:214-216`) for the two cases.
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

1. For each (a) and (b) parent, `project new MyApp --into PARENT --type test`
   (with `--yes`, at a pty without it, and with `--dry-run`) exits 2 with the
   fixed refusal line, no `Create:`, plan or `yes` prompt, nothing changed.
2. Asked, `2`: the question's line for the case, then the same refusal at
   once, with no generator list, `Create:` or `yes` prompt; `--dry-run` too.
3. Asked, Enter: (a) as today; (b) the new line and refusal, its dry run too.
4. A missing parent below a directory, and a dangling link: as today.
5. The earlier refusals and the shape-by-flag refusal keep their text; every
   added line is ASCII; every existing test but the one named passes as is.

## Risks

- Two-fault invocations name the parent first (exit status unchanged); an
  asked person may still answer `2` and be refused at once (W3 would not ask);
  a parent changed after the check meets the backstop; the files shared with
  lane openRepoProject-2 need main merged in.

## Out of Scope

- A raw `os.stat` classified by errno: the pathlib reads suffice (N5).
- A new flag, environment variable or configuration file: none is needed.
- A line under entry 2: a new form of the question, beyond this change.
- The Triad answer's refusal text and composition: only the (b) sentence
  enters, as a parent sentence.
- The shape branch's sentence: already early and true (archived D6).
- Permissions: a writability read predicts refusals the system may not make
  (root, ACLs, read-only mounts), and an unsearchable ancestor is already
  refused at `destination.exists()` (`project:328`) on 3.10 and 3.12.
- The archived N1 residuals (3.13 and later loop, 3.14 unsearchable
  ancestor): versions CI does not run; by that record (not run here) the new
  read classes them as creatable, so they behave as today.
- The CI matrix (3.10 and 3.12, Linux and macOS) and "Python 3.10+": the
  realization's tests run on both as the matrix stands.
- Everything from `discover` down and every subcommand but `new`: lane
  openRepoProject-2's surface, or untouched.
- workBenches, openRepoShape, setup-openspeckit and the archived changes:
  other owners' code, or immutable records.
