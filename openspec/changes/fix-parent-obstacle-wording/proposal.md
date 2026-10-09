Lane: openRepoProject-1

# Proposal: fix-parent-obstacle-wording

Status: draft, proposal only; alignment review and council next; nothing here
is ratified. Governing issue: opensoft/openRepoProject#14, claimed by lane
openRepoProject-1. Proposed on Brett Heap's word "propose the D3 wording
follow-up as a new change" (2026-10-09).

Source of the current wording: the archived change
`openspec/changes/archive/2026-10-08-prefer-triad-in-project-new/` (design D3
and D13), realized by PR #8 as `d7f6b0e`. The lead's ruling R-A on PR #8,
recorded in the lane handoff and in PR #8's description, reads: "the ratified
D13 parent-obstacle wording ("does not exist") stays although the check is
`is_dir()`, logged as a wording follow-up". This change is that follow-up.

## Why

`project new` reads the parent obstacle as `parent.is_dir()` (`project:244`)
but words it, under the Triad entry and inside the composed refusal on a Triad
answer, as "The parent directory PARENT does not exist; a Triad is created
inside an existing directory." When the parent exists and is not a directory,
the refusal is right and the sentence is false. The ratified text named the
fact two ways: the archived proposal and the main spec say "the parent
directory exists" (`openspec/specs/project-command/spec.md:204`), while D3
fixed the read as `parent.is_dir()`.

Observed at this branch's base `7a9134b` (Python 3.12.3, a pty, a fake
`openRepoShape` on PATH): `project new MyApp --into <a regular file>` prints
"Not possible here: The parent directory <the file> does not exist; ..." and,
on Enter, refuses with the same sentence, exit 2. "Does not exist" sends the
person to `mkdir`, which fails on that path ("File exists"). The case is
reachable however the parent is given: `--into`, the positional parent,
`PROJECTS_DIR`, or the default `~/projects`.

## What Changes

- **The parent obstacle gets two sentences, chosen by which case holds**
  (recommended; Alternatives below). A parent that does not exist keeps
  today's sentence, unchanged: `The parent directory PARENT does not exist; a
  Triad is created inside an existing directory.` A parent that exists and is
  not a directory gets a new sentence, such as `The parent PARENT exists but is
  not a directory; a Triad is created inside an existing directory.` The
  design that follows fixes every new string character for character, as D13
  did, and the tests pin it as a fixture.
- **The check is unchanged.** The obstacle holds exactly when
  `parent.is_dir()` is false, so a symlink to a directory still counts as a
  parent and is asked with no parent obstacle, as today. The three local reads
  of D3 stay three, in the order name, openRepoShape, parent; telling the two
  parent cases apart looks only at the same path, locally, with no network and
  no subprocess, and the design chooses that read.
- **PARENT stays the resolved path** `new()` already computes
  (`project:315`), so each sentence is true of the path it names: a symlink to
  a file is named by its target, which exists and is not a directory, and a
  dangling symlink by its target, which does not exist (both observed).
- **Everything around the sentence is unchanged.** The line keeps its
  `Not possible here: ` prefix. The composed refusal stays `A Triad cannot be
  created here. `, the sentences of the obstacles that hold in D3 order, then
  ` Nothing was created.`, built from whichever parent sentence applied.
  Exit status 2, the dry run's refusal, the Triad's first place and default,
  and the single-repository answer are unchanged.
- **`README.md`** "Create a project" names both cases where it now says "a
  parent directory that does not exist" (line 60).

### Alternatives

- **(A) One sentence true in both cases**, for example `PARENT is not an
  existing directory; a Triad is created inside one.` Cheaper: one string and
  no branch. Not recommended: it changes the text the common case, a missing
  parent, prints today, and it no longer says which repair applies.
- **(B) Two case-specific sentences, the missing case unchanged.**
  Recommended: the common case prints exactly what it prints today, and each
  case gets a sentence that is true and points at its own repair (create the
  directory, or choose a parent that is one).
- **(C) Change nothing.** Rejected: the text is false in a reachable case,
  and "does not exist" sends the person to `mkdir`, which then fails on the
  file.
- **(D) Read `exists()` instead.** Rejected: a file cannot host a Triad. With
  no obstacle named, a Triad answer would go on to the organization and
  visibility prompts and then meet the shape branch's own refusal, "Shape
  creation requires an existing --into parent directory." (`project:364-365`,
  observed with `--shape`): later, after two prompts, and naming an `--into`
  the person may not have typed.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `project-command`: the spec phase writes a MODIFIED block for "Known Triad
  obstacles are named before the question and refused on a Triad answer"
  (`openspec/specs/project-command/spec.md:200-249`). Its prose reads the
  parent fact as whether the parent is an existing directory, and names the
  parent in either case without presenting it as an `--into` value the person
  typed. The scenario "The parent directory is missing" becomes one scenario
  for each case (whether the first keeps its name is the spec phase's call),
  and "No known obstacle" reads "the parent is an existing directory". No
  other requirement changes.

## Impact

- **`project`**: one new string, and one branch in `known_obstacles()`
  (`project:235-248`) choosing between the two sentences. The composed refusal
  in `new()` (`project:338-339`), `print_creation_question()`, the order of
  the reads and the shape branch are untouched. No new flag, environment
  variable, network access or import; all text ASCII.
- **`tests/test_project.py`**: the fixture `OBSTACLE_PARENT` (line 35) stays,
  since the missing case's text is unchanged, and one fixture is added for the
  new sentence. New cases for a parent that exists and is not a directory (a
  regular file, and a symlink to one, named by its target): its line in the
  question; the composed refusal on a Triad answer, exit 2, with no
  organization prompt and no `openRepoShape` run; the dry run, exit 2; and a
  single-repository answer unaffected, ending where the flag-chosen bench path
  ends for the same parent (observed today: `parent.mkdir` refuses with
  `[Errno 17] File exists`, exit 2). A symlink to a directory is asked with no
  parent obstacle. `test_pty_missing_parent_is_named_without_into`,
  `test_pty_triad_answer_with_an_obstacle_refuses`,
  `test_pty_dry_run_with_an_obstacle_refuses` and
  `test_pty_single_answer_is_unaffected_by_obstacles` use a missing parent and
  keep passing unchanged.
- **`README.md`** line 60, and **`openspec/specs/project-command/spec.md`**
  through the delta above, at archive.
- **`specs/002-triad-first-project-new/`** stays the record of feature 002 and
  is not edited, although its `spec.md:152` and `quickstart.md:118` carry
  today's wording.
- **Speckit handoff**: implementation goes to exactly one new Speckit
  feature, `specs/003-<slug>/`, created by `/speckit.specify` after
  ratification (`001` and `002` exist). OpenSpec `tasks.md` holds governance
  boxes and that one handoff only, as the archived change's does.
- **Handoffs after landing**: none. workBenches#145 already asks for the pin
  move to `d7f6b0e`, which carries today's sentence; the corrected sentence
  reaches `onp` and `new-project.sh` when workBenches later moves its pin to a
  sha at or after this change's realization, on its owner's act. This lane
  opens no new workBenches issue for it.

## Out of Scope

- Any string or behaviour other than the parent sentence: the name and
  openRepoShape obstacles, the question's other lines, its prompts and its
  answers.
- The shape path's own refusal, `Shape creation requires an existing --into
  parent directory.` (`project:364-365`): it belongs to the pre-existing
  `--shape` path, not to the question.
- The single-repository path's outcome for a file parent (`parent.mkdir`
  raising `File exists` once the plan is confirmed, exit 2): unchanged.
- A parent whose status cannot be read: `is_dir()` raises `PermissionError`
  (observed for a path inside a directory without search permission), and
  `main()` refuses with exit 2 before the question, as today.
- Any new surface or form. The change rewords one line of the existing
  question on `project new`'s creation path, and its refusal, inside the
  closed list the archived proposal kept ("only at such surfaces and only in
  these forms", openxFactory `prefer-triad-project-shape`). `status`, `doctor`
  and every other subcommand are untouched.
- The archived change `2026-10-08-prefer-triad-in-project-new` (an immutable
  record, cited and never edited), setup-openspeckit, openRepoShape and
  workBenches.
