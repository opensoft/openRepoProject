Lane: openRepoProject-1

# Proposal: fix-parent-obstacle-wording

Status: draft; alignment review and council resolved (see PR #15); design in
the same pull request; nothing here is ratified. Governing issue:
opensoft/openRepoProject#14, claimed by lane openRepoProject-1. Proposed on
Brett Heap's word "propose the D3 wording follow-up as a new change"
(2026-10-09).

Source of the current wording: the archived change
`openspec/changes/archive/2026-10-08-prefer-triad-in-project-new/` (design D3
and D13), realized by PR #8 as `d7f6b0e`. The lead's ruling on PR #8, recorded
in PR #8's description (the first lead ruling under Notes for the reviewer;
the label R-A is the lane handoff's), reads: "the ratified D13 parent-obstacle
wording ("does not exist") stays although the check is `is_dir()`, logged as a
wording follow-up". This change is that follow-up.

## Why

`project new` reads the parent obstacle as `parent.is_dir()` (`project:244`)
but words it, under the Triad entry and inside the composed refusal on a Triad
answer, as "The parent directory PARENT does not exist; a Triad is created
inside an existing directory." When the parent exists and is not a directory,
the refusal is right and the sentence is false. The ratified text named the
fact two ways: the archived proposal and the main spec say "the parent
directory exists" (`openspec/specs/project-command/spec.md:204-205` and
`:248`), while D3 fixed the read as `parent.is_dir()`.

Observed at this branch's base `7a9134b` (Python 3.12.3, a pty, a fake
`openRepoShape` on PATH): `project new MyApp --into <a regular file>` prints
"Not possible here: The parent directory <the file> does not exist; ..." and,
on Enter, refuses with the same sentence, exit 2. "Does not exist" sends the
person to `mkdir`, which fails on that path ("File exists"). The case is
reachable however the parent is given (`--into`, the positional parent,
`PROJECTS_DIR`, or the default `~/projects`), and the criterion for the fix is
that each parent sentence is true of the path it names.

## What Changes

- **The parent obstacle gets two sentences, chosen by which case holds**
  (recommended; Alternatives below). A parent that does not exist keeps
  today's sentence, unchanged: `The parent directory PARENT does not exist; a
  Triad is created inside an existing directory.` A parent that exists and is
  not a directory gets a new sentence, `The parent PARENT exists but is not a
  directory; choose a parent that is a directory.`, which names PARENT, says
  that it exists and is not a directory, and states its repair. Its clause
  after the semicolon is deliberately not Triad-specific, because nothing can
  be created inside such a parent on either path; "a Triad is created inside
  an existing directory" stays only in the missing case's sentence. The design
  that follows fixes every new string character for character, as D13 did,
  and the tests pin it as a fixture.
- **The check is unchanged and the facts stay three.** The obstacle holds
  exactly when `parent.is_dir()` is false; which sentence is printed is read
  as `parent.exists()` on the same resolved path, only when that is false, and
  the design restates D3 item 3 that way (the docstring says three local
  facts). A symlink to a directory still counts as a parent and is asked with
  no parent obstacle, as today. The three local reads of D3 stay in the order
  name, openRepoShape, parent; telling the two parent cases apart looks only
  at the same path, locally, with no network and no subprocess.
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
- **`README.md`** line 60 reads "or a parent that is missing or is not a
  directory. A single-repository answer creates a missing parent; a parent
  that exists but is not a directory blocks both answers, so choose another
  parent." in place of "or a parent directory that does not exist."

### Alternatives

- **(A) One sentence true in both cases**, for example `PARENT is not an
  existing directory; a Triad is created inside one.` Cheaper: one string and
  no branch. Not recommended: it changes the text the common case, a missing
  parent, prints today, and it does not state the file-parent case's repair.
- **(B) Two case-specific sentences, the missing case unchanged.**
  Recommended: the common case prints exactly what it prints today, and each
  case gets a sentence that is true of it. The new sentence also states its
  repair, choosing a parent that is a directory; the missing case's sentence
  keeps today's text, whose implied repair, creating the directory, fails
  beneath a component that is not a directory (Out of Scope).
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
  typed. The scenario "The parent directory is missing" keeps its title and
  its text, and its WHEN gains a parent given as a dangling symbolic link,
  named by its target; a new scenario, "The parent exists but is not a
  directory", states the other case: the Triad's entry names the parent with
  the new sentence (a symbolic link to a file by its target), and the Triad
  stays first and the default. Feature 002's traceability.md:37 therefore
  still points at an existing title. "No known obstacle" reads "the parent is
  an existing directory, or a symbolic link that resolves to one". The
  scenarios "A Triad answer with a known obstacle" and "A dry run with a known
  obstacle" each gain the case of a parent that exists and is not a directory:
  the refusal exits with status 2, names the same parent sentence the question
  printed, and states that nothing was created; for the Triad answer it also
  asks for no organization or visibility, runs no openRepoShape command and
  creates nothing. "A single-repository answer is unaffected" reads: THEN the
  single-repository path continues with its generator selection, plan and
  `yes` confirmation, and ends as that path ends for the same name and parent
  when the generator is chosen by flag: the repository is created, or that
  path's own refusal is made with its exit status; AND no creation advisory
  follows, since a creation that went through the question is followed by
  none (main spec, "Creation question offers the Triad first"). No other
  requirement changes.

## Impact

- **`project`**: one new string, and one branch in `known_obstacles()`
  (`project:235-247`) choosing between the two sentences. The composed refusal
  in `new()` (`project:338-339`), `print_creation_question()`, the order of
  the reads and the shape branch are untouched. No new flag, environment
  variable, network access or import; all text ASCII.
- **`tests/test_project.py`**: the fixture `OBSTACLE_PARENT` (line 35) stays,
  since the missing case's text is unchanged, and one fixture is added for the
  new sentence, after the `End D13 fixtures` marker, under its own header
  naming this change's design, so the D13 block stays a verbatim copy of the
  archived design. New cases for a parent that exists and is not a directory
  (a regular file, and a symlink to one, named by its target), and, for a
  dangling symlink, named by its target with today's `does not exist`
  sentence: its line in the question, for a parent given by --into, by the
  positional parent, by PROJECTS_DIR and by the default ~/projects, with no
  question line containing --into; the composed refusal on
  a Triad answer, exit 2, with no organization prompt and no `openRepoShape`
  run; the dry run, exit 2; and a single-repository answer unaffected, ending
  where the flag-chosen bench path ends for the same parent (observed today:
  `parent.mkdir` refuses with `[Errno 17] File exists`, exit 2). A symlink to a
  directory is asked with no parent obstacle. The new cases are added as new
  rows of known_obstacle_cases() or as new tests, and each file-parent case is
  also run in test_inproc_triad_obstacle_runs_nothing; one row combines the
  file parent with the name and openRepoShape obstacles, the parent sentence
  last. `test_pty_missing_parent_is_named_without_into`,
  `test_pty_triad_answer_with_an_obstacle_refuses`,
  `test_pty_dry_run_with_an_obstacle_refuses`,
  `test_pty_single_answer_is_unaffected_by_obstacles` and
  `test_inproc_triad_obstacle_runs_nothing` (through `known_obstacle_cases()`)
  keep passing with every existing row and assertion unchanged: where they name
  a parent obstacle it is a missing parent, and where they name none the parent
  is an existing directory, as in `test_pty_no_known_obstacle_names_none`.
- **`README.md`** line 60, and **`openspec/specs/project-command/spec.md`**
  through the delta above, at archive.
- **`specs/002-triad-first-project-new/`** stays the record of feature 002 and
  is not edited. Its statements of the parent fact are spec.md:130-132, :140,
  :151-154, :156, :367, :370-371 and :459-460 (User Story 3, FR-012, Key
  Entities: "the parent directory exists", "a missing parent directory"),
  quickstart.md:118 (today's sentence), traceability.md:37 and tasks.md:137,
  :143; data-model.md:53 already reads parent.is_dir(). Each is true of the
  case it describes. The new feature's spec.md states that, for the parent
  fact, it supersedes FR-012's "whether the parent directory exists" and "the
  missing parent directory" with the two cases above, and its traceability.md
  names the delta's scenarios under their titles, the missing case's
  unchanged and the new case's "The parent exists but is not a directory".
- **Speckit handoff**: implementation goes to exactly one new Speckit
  feature, created after ratification as the next free `specs/NNN-<slug>/`
  when `/speckit.specify` runs from a main synced to origin: `001` and `002`
  exist; lane openRepoProject-2's PR #11 names `003`
  (add-project-clean-all-safe) and PR #12 names `004` (add-project-overview),
  so this feature takes the next number free that day, recorded in the
  tasks.md handoff when created. Its realization edits `project` and
  `tests/test_project.py`, as PR #11's feature will; whichever merges second
  merges main in. OpenSpec `tasks.md` holds governance boxes and that one
  handoff only, as the archived change's does.
- **Handoffs after landing**: no new issue, and one comment at most.
  workBenches#145 already asks for the pin move to `d7f6b0e`, which carries
  today's sentence; the corrected sentence reaches `onp` and `new-project.sh`
  when workBenches later moves its pin to a sha at or after this change's
  realization, on its owner's act. This lane opens no new workBenches issue.
  When the realization merges, it posts one comment on workBenches#145 if that
  issue is still open, naming the realization's merge sha and the sha256 of
  `project` at that sha as an alternative pin target that carries the
  corrected sentence. If #145 is closed by then, nothing is posted, and the
  sentence reaches `onp` at the owner's next pin move.

## Out of Scope

- Any string or behaviour other than the parent sentence: the name and
  openRepoShape obstacles, the question's other lines, its prompts and its
  answers.
- The shape path's own refusal, `Shape creation requires an existing --into
  parent directory.` (`project:364-365`): it belongs to the pre-existing
  `--shape` path, not to the question.
- A known limitation of the pre-existing bench path, out of this change's
  scope, which is a wording change: for a parent that exists and is not a
  directory, the single-repository path, asked or chosen by flag, shows the
  plan, asks for `yes`, and only then refuses (`parent.mkdir` raises
  `[Errno 17] File exists`, exit 2), and its dry run exits 0. An earlier
  refusal would be its own change, on Brett Heap's word; no issue is opened
  for it now.
- On Python 3.10 and 3.12, the CI matrix, a parent whose status cannot be
  read: `destination.exists()` raises `PermissionError` at `project:321`, in
  the existing-destination refusal, before `known_obstacles()` is reached
  (observed for a parent inside a directory without search permission:
  `REFUSED: [Errno 13] Permission denied: '<parent>/MyApp'`), and `main()`
  refuses with exit 2 before the question, as today.
- A parent that does not exist beneath a path component that is not a directory
  (for example --into FILE/sub): it does not exist, so it keeps today's
  sentence, and the single-repository path's parent.mkdir refusal ([Errno 20]
  Not a directory, exit 2) is unchanged. It is a known residual dead end and
  an accepted gap: the sentence is true and the repair it suggests fails with
  Not a directory.
- On Python 3.10 and 3.12, the CI matrix, a parent that is a symbolic-link
  loop: `Path.resolve()` at `project:315` raises `RuntimeError` before the
  question (a traceback, observed on Python 3.12.3); unchanged by this change
  and not one of its two cases.
- On Python 3.13 and later a symbolic-link loop no longer raises at resolve()
  and prints today's missing-parent sentence; on 3.14 an existing directory
  under an unsearchable ancestor is no longer refused at destination.exists()
  and prints the missing-parent sentence: both are the pre-existing wording on
  versions CI does not run, recorded as residuals and unchanged here. The loop
  on 3.13 and later is a residual dead end like FILE/sub: the repair the
  sentence suggests, creating the directory, fails there too.
- Any new surface or form. The change rewords one line of the existing
  question on `project new`'s creation path, and its refusal, inside the
  closed list the archived proposal kept ("only at such surfaces and only in
  these forms", openxFactory `prefer-triad-project-shape`). `status`, `doctor`
  and every other subcommand are untouched.
- The archived change `2026-10-08-prefer-triad-in-project-new` (an immutable
  record, cited and never edited), setup-openspeckit, openRepoShape and
  workBenches.
