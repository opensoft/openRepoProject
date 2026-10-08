Lane: openRepoProject-1

# Feature Specification: Triad-first project creation

**Feature Branch**: `002-triad-first-project-new`

**Created**: 2026-10-07

**Status**: Implemented (PR #8)

**Input**: User description: "Realize the ratified OpenSpec change
prefer-triad-in-project-new: `project new` offers the Triad first to a person
at the terminal, and advises on standard error after a single repository
created without that offer (opensoft/openRepoProject#3; task 5.6 of
openxFactory's prefer-triad-project-shape)."

**Source of truth**: `openspec/changes/prefer-triad-in-project-new/` (proposal,
`project-command` spec delta, design D1 to D14, clarifications N1 to N6),
ratified by Brett Heap ("ratify 5", 2026-10-07,
https://github.com/opensoft/openRepoProject/pull/5#issuecomment-6035631740),
landed on main as `ca4c615`. Where this summary is shorter than the spec delta,
the delta governs.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Offered the Triad first at the terminal (Priority: P1)

A person at a terminal runs `project new` without a choosing flag. Once the
name is known and the early refusals have passed, the command asks one
question: Triad or single repository. The Triad is first and pre-selected, with
its posture beside it (preferred, not required; elective; confers nothing).
Enter takes the Triad; a single repository is accepted without a reason. The
question creates nothing: each answer continues into its existing path, which
keeps its own confirmation.

**Why this priority**: It is task 5.6's contract ("New-project creation offers
the Triad first"), and `project new` is the one creation surface in the estate
that does not offer it yet.

**Independent Test**: At a terminal with `CI` unset and no choosing flag, run
`project new NAME` against temporary fixtures, give each answer in turn, and
check which path continues and that the destination stays absent until that
path's own confirmation is typed.

**Acceptance Scenarios**:

1. **Given** standard input and standard output are terminals, `CI` is unset
   and no choosing flag is given, **When** the person runs `project new` with
   the name given or typed at the name prompt, **Then** the creation question
   is asked once the name is known, before any generator list, organization
   prompt, plan or confirmation.
2. **Given** the question is asked, **When** it appears, **Then** standard
   output shows the Triad as entry 1, marked as the default, with "preferred,
   not required", "elective" and "confers nothing" beside it, and the single
   repository as entry 2, naming `single-repository.yaml` as the ratified way
   to record staying single; no `single-repository.yaml` is ever written.
3. **Given** the question is asked, **When** the answer is Enter, `1`, `y`,
   `yes`, `Y` or ` YES `, **Then** the Triad path continues (User Story 2);
   **When** it is `2`, `n`, `no`, `N` or ` No `, **Then** the existing
   single-repository path continues with its generator selection, plan and
   `yes` confirmation, and no creation advisory follows the creation.
4. **Given** a first answer that is not recognised (such as `3` or `maybe`),
   **When** the second is recognised, **Then** the question is asked once more
   and the second answer is taken; **When** the second is not recognised
   either, **Then** the command refuses with exit status 2, stating that
   nothing was created, and runs no generator and no openRepoShape command.
5. **Given** the question is asked, **When** input ends, **Then** the command
   refuses with exit status 2, stating that nothing was created; **When** the
   person interrupts, **Then** it prints `Cancelled.`, exits with status 130,
   and nothing is created.
6. **Given** either answer was taken, **When** the person declines that path's
   confirmation (openRepoShape's typed confirmation, or the `yes`
   confirmation), **Then** nothing is created.
7. **Given** `--dry-run` at a terminal with no choosing flag, **When** the
   question is answered, **Then** a Triad answer, after its organization and
   visibility prompts and restating line, prints the destination and the
   openRepoShape command; a single-repository answer prints the destination and
   the generator command; nothing is written and no creation advisory is
   printed.

---

### User Story 2 - Creating the Triad from the answer (Priority: P1)

After a Triad answer with no known obstacle, the command asks for the GitHub
organization and then the visibility, restates the choice in one line, and
hands creation to openRepoShape, whose own typed confirmation is the
confirmation.

**Why this priority**: The Triad answer cannot complete without both values,
and leaving the visibility to openRepoShape's default would let a default
decide who can read three repositories.

**Independent Test**: At a terminal, with a stand-in for openRepoShape that
records how it was called and asks for its own typed confirmation, take the
Triad, type an organization and a visibility, and check the restating line,
the recorded call, and that nothing exists until the stand-in's confirmation
is typed.

**Acceptance Scenarios**:

1. **Given** a Triad answer and no known obstacle, **When** the command
   continues, **Then** it asks for the organization and then the visibility,
   and an organization that fails the existing organization-name check is
   asked again before any visibility prompt.
2. **Given** the visibility prompt, **When** the answer is `PUBLIC` or
   ` private `, **Then** it is accepted as `public` or `private`; `1`, `2`, `3`
   or an empty answer is not accepted.
3. **Given** the organization or the visibility prompt, **When** two answers in
   a row are empty or not accepted, or input ends, **Then** the command refuses
   with exit status 2, stating that nothing was created, and runs no
   openRepoShape command; **When** the person interrupts, **Then** it prints
   `Cancelled.`, exits with status 130, and nothing is created.
4. **Given** both answers are accepted, **When** the command continues,
   **Then** one line on standard output restates the name, the organization
   and the visibility before the plan is shown, and for `public` that line
   states that anyone can read the repositories.
5. **Given** the Triad path without `--dry-run`, **When** the command
   delegates, **Then** openRepoShape is run with the typed organization, the
   visibility as its lowercase word and the parent directory, without `--yes`,
   and nothing exists until the person types openRepoShape's own confirmation.
6. **Given** openRepoShape exits with a nonzero status (its own refusal or a
   declined confirmation), **When** the command returns, **Then** it exits
   with that same status; no particular status is promised.

---

### User Story 3 - Known obstacles named beside the Triad (Priority: P2)

Before asking, the command reads three local facts: whether the name can be a
Triad name, whether openRepoShape is installed, and whether the parent
directory exists. The Triad stays first and the default, its entry names any
obstacle, and a Triad answer that meets one is refused at once, before any
further prompt and without network access.

**Why this priority**: A Triad answer that openRepoShape is certain to refuse
must not lead the person through two more prompts and a network fetch first.

**Independent Test**: At a terminal, run with the name `my-app`, then with
openRepoShape absent, then with a missing parent directory; read the Triad
entry, answer Triad and check exit status 2 with openRepoShape never started,
then answer single repository and check that the bench path proceeds.

**Acceptance Scenarios**:

1. **Given** the name `my-app`, **When** the question is asked, **Then** the
   Triad is still first and the default, and its entry names `my-app` and says
   that a Triad name is a letter first, then letters and digits only.
2. **Given** openRepoShape is not on PATH, **When** the question is asked,
   **Then** the Triad's entry says that openRepoShape is not on PATH.
3. **Given** the parent directory, including the default projects directory,
   does not exist, **When** the question is asked, **Then** the Triad's entry
   names that directory without presenting it as an `--into` value the person
   typed.
4. **Given** the name fits the Triad name form, openRepoShape is on PATH and
   the parent directory exists, **When** the question is asked, **Then** the
   Triad's entry names no obstacle.
5. **Given** any known obstacle, **When** the answer takes the Triad, with or
   without `--dry-run`, **Then** the command refuses with exit status 2, naming
   the obstacles and stating that nothing was created, and asks for no
   organization or visibility, runs no openRepoShape command, makes no network
   access and creates nothing.
6. **Given** any known obstacle, **When** the answer takes the single
   repository, **Then** the single-repository path proceeds exactly as it would
   without the obstacle.

---

### User Story 4 - Scripted creation keeps its path and is advised on standard error (Priority: P2)

A creation that chooses by flag, or that does not run at a person's terminal,
is never asked the question and does exactly what its flags say. When it
creates a single repository, two `warning:` lines follow on standard error;
standard output, prompts, refusals, created files, `.project.json` and the exit
status stay as they were.

**Why this priority**: Scripts, CI and agents need a predictable path, and the
ratified text still owes a single repository created without the offer the
recommendation.

**Independent Test**: Create a single repository with `--type` and `--yes`
through a pipe against a test generator; compare standard output, the files,
`.project.json` and the exit status with pinned expectations and check
standard error for the two lines; repeat with standard error closed, on a
broken pipe and on a full device.

**Acceptance Scenarios**:

1. **Given** a terminal, **When** any one of `--shape`, `--org`,
   `--visibility`, `--family`, `--elected-by`, `--bench`, `--type`,
   `--description` or `--yes` is given, **Then** no creation question is
   asked, and the invocation follows the path its flags choose with its
   existing prompts and refusals.
2. **Given** `--shape`, `--org` and `--visibility`, with or without `--yes`,
   **When** the creation runs, **Then** no question is asked, no creation
   advisory is printed, and openRepoShape is run without `--yes`, so its own
   typed confirmation is retained.
3. **Given** standard input or standard output is not a terminal, **When**
   `project new` runs, **Then** no creation question is asked.
4. **Given** a terminal and no choosing flag, **When** `CI` is `true` or any
   value other than empty, `0`, `false` or `no`, **Then** no creation question
   is asked; **When** `CI` is empty, `0`, `false` or `no`, in any letter case
   and with surrounding whitespace, **Then** the question is asked.
5. **Given** a single repository created with `--type` and `--yes`, or created
   after the person types `yes` where `CI` is `true` or standard output is not
   a terminal, **When** the repository exists, **Then** standard error carries
   the two `warning:` lines, and standard output, the created files,
   `.project.json` and the exit status are what they would be without them.
6. **Given** the creation advisory is given, **When** its lines are read,
   **Then** both begin `warning:` and are ASCII only, and together they state
   the preference with "preferred, not required", "elective" and "confers
   nothing", name `adopt-project.py` run by a person deciding for that project,
   name `single-repository.yaml`, and say that nothing changes.
7. **Given** `--dry-run` with choosing flags, **When** the command runs,
   **Then** it prints the destination and the command it would run (the
   selected generator, or the openRepoShape command for `--shape`) without
   writes, and prints no creation advisory.

---

### User Story 5 - Workspace names and the workflow follow-up (Priority: P3)

A `<user>-wip` workspace name is created exactly as before, with no question
and no advisory. Under `--workflow`, the command gives its own offer first and
then runs the workflow follow-up (`setup-openspeckit`) exactly as before.

**Why this priority**: Both follow from the ratified exemptions and from
chaining two ratified surfaces, and they concern a minority of creations.

**Independent Test**: Create `alice-wip` and check that no question and no
advisory appear; then, with a stand-in follow-up that prints a marker, create a
single repository with `--yes --workflow`, both streams captured together, and
check that the two `warning:` lines come before the marker.

**Acceptance Scenarios**:

1. **Given** a name matching `^[a-z0-9]+(?:-[a-z0-9]+)*-wip$` (such as
   `alice-wip`), **When** it is created at a terminal or by flag, **Then** no
   creation question is asked, no creation advisory is printed, and the
   creation runs exactly as it would without this feature.
2. **Given** a single repository created with `--yes` and `--workflow`,
   **When** the follow-up runs, **Then** the command's two `warning:` lines are
   written before any output of the follow-up, and the follow-up's own output,
   including any advisory of its own, follows unchanged.
3. **Given** the same creation, **When** the follow-up exits with a nonzero
   status, **Then** the creation advisory has already been given, the command
   reports that the project was created and workflow setup failed, and it exits
   with the follow-up's status.
4. **Given** a person at the terminal answers `2` and `--workflow` is given,
   **When** the creation succeeds, **Then** the follow-up runs with the same
   arguments as before, its output follows unchanged, and the command adds no
   creation advisory of its own.
5. **Given** a workspace name with `--workflow`, **When** the single repository
   is created, **Then** the command gives no creation advisory and runs the
   follow-up as before.

---

### Edge Cases

- **EC-001**: An invalid name, a positional parent together with `--into`, or
  an existing destination is refused with exit status 2 before any generator or
  openRepoShape command runs, and the question is never shown.
- **EC-002**: `--workflow` without `setup-openspeckit` on PATH, for an
  invocation that will be asked the question, is refused with exit status 2
  before the question is shown.
- **EC-003**: An invocation that is not asked the question, gives `--workflow`
  without `setup-openspeckit` on PATH and names a generator that does not match
  is refused for the generator, as before.
- **EC-004**: End of input at the existing name prompt, generator number or
  `yes` confirmation still prints `Cancelled.` and exits with status 130.
- **EC-005**: A generator that creates the destination without initialising
  Git still counts as creating a single repository; the advisory is given.
- **EC-006**: No creation advisory is given for a dry run, a Triad creation, a
  creation that went through the question, a workspace name, a generator that
  fails, or a generator that succeeds without creating the destination.
- **EC-007**: With standard error closed, on a pipe whose reading end is
  closed, or on a full device, the repository is still created, standard output
  and the exit status are unchanged, and the advisory never appears on
  standard output.
- **EC-008**: `project status` and `project doctor`, in human or JSON form,
  report the same on a repository whether or not the advisory was given, and
  nothing in the repository records it.
- **EC-009**: A name outside the Triad name form given with `--shape` skips the
  question and its pre-check and reaches openRepoShape, whose own refusal
  passes through with its own status.
- **EC-010**: A choosing flag present with an empty value still counts as
  given, so the question is skipped and the flag's path follows.
- **EC-011**: Under `--workflow` at a terminal, a person who answered `2` may
  be advised and asked again by `setup-openspeckit`, whose `n` stops it; the
  command then reports that workflow setup failed and exits 130. This known
  consequence of chaining two ratified surfaces is not changed here.
- **EC-012**: Ctrl-C while openRepoShape runs keeps today's behaviour: the
  command prints `Cancelled.` and exits 130 after a moment, and openRepoShape's
  output may follow. It is documented, not changed.
- **EC-013**: An agent driving the command through a pseudo-terminal looks like
  a person and meets the question; Enter still ends at openRepoShape's typed
  confirmation, which an agent does not answer on a person's behalf.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `project new` MUST keep its existing creation behaviour: list
  usable generators, accept a name and a parent, present a plan, preserve
  generator failures and their exit status, and refuse an existing destination
  before running any generator or openRepoShape command.
- **FR-002**: Triad (shape) creation MUST require an explicit organization and
  visibility and MUST retain openRepoShape's own prompts; an organization and a
  visibility typed at the command's own prompts after a Triad answer count as
  explicit.
- **FR-003**: The command MUST create no repository the person has not
  confirmed. The creation question is not a confirmation: the Triad path ends
  at openRepoShape's own typed confirmation, and the single-repository path at
  the command's `yes` confirmation or a `--yes` the person gave. Declining that
  confirmation leaves nothing created.
- **FR-004**: With `--dry-run`, whether the path was chosen by flag or by an
  answer, the command MUST print the destination and the command it would run
  (the selected generator, or the openRepoShape command for a Triad), write
  nothing, and give no creation advisory.
- **FR-005**: With `--shape`, `--org` and `--visibility`, with or without
  `--yes`, the command MUST ask no question, give no creation advisory, and run
  openRepoShape without `--yes`.
- **FR-006**: One terminal rule MUST decide the question, which is asked
  exactly when: standard input and standard output are both terminals; `CI` is
  unset or its value, stripped of surrounding whitespace and compared
  case-insensitively, is empty, `0`, `false` or `no`; no choosing flag
  (`--shape`, `--org`, `--visibility`, `--family`, `--elected-by`, `--bench`,
  `--type`, `--description`, `--yes`) is given; and the name is not a
  workspace name (FR-021).
- **FR-007**: `--dry-run`, `--workflow`, `--into` or the positional parent, and
  `--workbenches` MUST NOT prevent the question. The command MUST offer no
  per-person setting, configuration file or new option that suppresses it. The
  existing prompts (the name, the generator number, the `yes` confirmation)
  MUST keep their existing behaviour, including `Cancelled.` and exit status
  130 at end of input.
- **FR-008**: The question MUST come after the name is known and after the
  refusals made before a path is chosen (an invalid name, a positional parent
  together with `--into`, an existing destination), and before the chosen
  path's own steps, prompts and confirmation. For an invocation that will be
  asked, the refusal of `--workflow` without `setup-openspeckit` on PATH MUST
  also come before the question; an invocation that is not asked MUST keep its
  existing order of refusals.
- **FR-009**: The question MUST ask one thing, Triad or single repository, with
  its lines on standard output: the Triad as entry 1, marked as the default,
  with its posture beside the preference (preferred, not required; elective;
  confers nothing); the single repository as entry 2, accepted without a reason
  being asked, naming in one clause `single-repository.yaml` as the ratified way
  to record staying single. The command MUST NOT write
  `single-repository.yaml`. The prompt MUST behave as the existing prompts do
  and read naturally with its answers: a yes takes the Triad, a no the single
  repository.
- **FR-010**: Enter, `1`, `y` or `yes` MUST take the Triad, and `2`, `n` or
  `no` the single repository, with letters compared case-insensitively and
  surrounding whitespace ignored. Any other answer MUST be asked once more; a
  second unrecognised answer, or end of input, MUST refuse with exit status 2,
  stating that nothing was created. An interrupt MUST print `Cancelled.` and
  exit with status 130.
- **FR-011**: The question MUST create nothing. A Triad answer MUST continue
  into the Triad path (FR-013 to FR-016) and a single-repository answer into
  the existing single-repository path with its generator selection, plan and
  `yes` confirmation. A creation that went through the question MUST be
  followed by no creation advisory.
- **FR-012**: Before asking, the command MUST read three local facts, with no
  network access: whether the name fits openRepoShape's assembly-root form
  `^[A-Za-z][A-Za-z0-9]*$` (a letter first, then letters and digits only),
  whether `openRepoShape` is on PATH, and whether the parent directory exists.
  The Triad MUST stay first and the default in every case, and its entry MUST
  name each known obstacle: the given name and the form a Triad name needs;
  that openRepoShape is not on PATH; or the missing parent directory, without
  presenting it as an `--into` value the person typed.
- **FR-013**: A Triad answer with any known obstacle MUST refuse at once with
  exit status 2, naming the obstacles and stating that nothing was created
  (for a missing openRepoShape, with the instruction to install it through
  workBenches first), before the organization and visibility prompts, before
  any network access and without running openRepoShape, in a dry run as in a
  real run. A single-repository answer MUST be unaffected by these facts. They
  predict only refusals openRepoShape is certain to make; its own checks stay
  authoritative.
- **FR-014**: After a Triad answer with no known obstacle, the command MUST ask
  for the GitHub organization and then the visibility, and MUST NOT leave the
  visibility to openRepoShape's default. The organization MUST pass the
  existing organization-name check (a letter or digit first, then letters,
  digits and hyphens) before the visibility is asked. The visibility MUST be
  typed as a full word, compared case-insensitively, from a list that reads
  `private`, `public`, `internal` in that order, with no numbers and no
  default.
- **FR-015**: At either prompt, an empty answer or one the prompt does not
  accept MUST be asked once more and then refused with exit status 2, and end
  of input MUST refuse with exit status 2; each refusal states that nothing was
  created and runs no openRepoShape command. An interrupt MUST print
  `Cancelled.` and exit with status 130.
- **FR-016**: Once both answers are accepted, and before the plan is shown (in
  a dry run as in a real run), the command MUST print one line on standard
  output restating the name, the organization and the visibility; for
  `public`, that line states that anyone can read the repositories. It MUST
  then run openRepoShape with the typed organization, the visibility as its
  lowercase word and the parent directory, without `--yes`. A nonzero exit of
  openRepoShape, whether its own refusal or a declined confirmation, MUST pass
  through with openRepoShape's own status; no particular status is promised.
- **FR-017**: When a single repository is created without the question having
  been asked (chosen by flag, or the terminal rule does not hold) and the name
  is not a workspace name, the command MUST give the creation advisory once the
  repository exists (the generator succeeded, the destination is a directory
  and its `.project.json` exists, whether or not Git was initialised), after
  standard output has been flushed and before any `--workflow` step.
- **FR-018**: The creation advisory MUST be two lines on standard error, each
  beginning `warning:`, in ASCII only, together carrying: the preference with
  its posture (preferred, not required; elective; confers nothing);
  openRepoShape's `adopt-project.py`, run by a person deciding for that
  project, as the way to convert; `single-repository.yaml` as the way to stop
  meeting the advisory; and that nothing changes.
- **FR-019**: The creation advisory MUST NOT be written to standard output in
  any case and MUST NOT change the exit status, standard output, prompts,
  refusals, created files or `.project.json`; it MUST NOT be a `checks` row, a
  `--json` field or review output. A failure to write it (a closed standard
  error, a broken pipe, a full device) MUST be ignored.
- **FR-020**: The command MUST NOT give the creation advisory for a dry run, a
  Triad creation, a creation that went through the question, a workspace name,
  or a creation that did not succeed, and MUST record nothing about having
  given it. It MUST NOT run `adopt-project.py`, convert an existing repository,
  or write a manifest or record on the advisory's account.
- **FR-021**: A name matching `^[a-z0-9]+(?:-[a-z0-9]+)*-wip$`, the `<user>-wip`
  workspace form of openRepoShape's naming policy, MUST get neither the
  question nor the creation advisory, and its creation MUST run exactly as it
  would without this feature, with or without `--workflow`.
- **FR-022**: Under `--workflow`, the command MUST give its own offer first
  (the question before creation, or the creation advisory after a
  single-repository creation it covers) and MUST then run the workflow
  follow-up exactly as before, with the same arguments, so that the
  follow-up's own output comes after the offer. It MUST neither suppress nor
  coordinate with the follow-up's own advisory or question. A failure of the
  follow-up MUST keep its existing report and pass its exit status through,
  with the creation advisory already given.
- **FR-023**: Every new line of text (the question and its obstacle lines, the
  three prompts, the retry lines, the refusals, the restating line and the
  advisory) MUST be ASCII and MUST match the wording fixed in the ratified
  change's `design.md`, D13.
- **FR-024**: The README's "Create a project" section MUST describe the
  question (its default, its answers, the obstacles named beside the Triad,
  what skips it, and that a dry run asks too), the organization and visibility
  prompts, the advisory on standard error, the second offer under
  `--workflow`, and what Ctrl-C does while openRepoShape runs; its sentence
  that the command shows the generator and destination and asks for `yes`
  before running MUST be corrected for the new first question, and its
  Configuration table MUST list `CI`. `AGENTS.md` and the README MUST tell an
  agent to offer the Triad in conversation, then run `project new` with a
  choosing flag, and never answer the question, the organization, the
  visibility or openRepoShape's confirmation on a person's behalf.

### Key Entities

- **Triad**: openRepoShape's three-repository shape, an assembly root with a
  spec leg and a code leg ("three-leg project" and "three-repository project"
  are synonyms); preferred, not required; elective; confers nothing.
- **Creation question**: the one question, Triad (entry 1, default) or single
  repository (entry 2), asked only where the terminal rule holds (FR-006).
- **Choosing flag**: any of the nine flags listed in FR-006.
- **Known obstacle**: a name outside the assembly-root form, openRepoShape
  missing from PATH, or a missing parent directory.
- **Creation advisory**: the two `warning:` lines on standard error after a
  single repository created without the question.
- **Workspace name**: a name of the `<user>-wip` form (FR-021).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A person at a terminal who runs `project new NAME` with no
  choosing flag, presses Enter at the question, types an organization and a
  visibility, and types openRepoShape's own confirmation ends with a Triad
  created through openRepoShape, started in every such run without `--yes` and
  with the typed organization and visibility.
- **SC-002**: Nothing is created before the person confirms: across every
  answer, refusal, interrupt and declined confirmation in the scenarios above,
  the destination is absent unless the person typed openRepoShape's
  confirmation or `yes`, or gave `--yes`.
- **SC-003**: Every refusal this feature adds exits with status 2, states that
  nothing was created and leaves the destination absent; every interrupt at the
  question or at the organization or visibility prompt exits with status 130
  after `Cancelled.`.
- **SC-004**: The question appears in 0 runs where `CI` is set to a value other
  than empty, `0`, `false` or `no`, where standard input or standard output is
  not a terminal, where any choosing flag is given, or where the name is a
  workspace name.
- **SC-005**: For a flag-chosen or non-interactive single-repository creation,
  standard output, the created files, `.project.json` and the exit status match
  the expectations pinned without the advisory, and standard error gains
  exactly the two `warning:` lines.
- **SC-006**: The advisory never breaks a creation: with standard error closed,
  on a pipe whose reading end is closed, or on a full device, the repository is
  created, the exit status stays 0, and no `warning:` line appears on standard
  output.
- **SC-007**: In every run where a Triad answer meets a known obstacle, the
  command refuses before any organization prompt, openRepoShape is never
  started, and no network access is made.
- **SC-008**: Every new line the command prints matches the text fixed in
  `design.md` D13 character for character and contains only ASCII characters.
- **SC-009**: Under `--workflow`, the command's two `warning:` lines precede the
  first line of the follow-up's output in every run.
- **SC-010**: All 43 existing tests keep passing unchanged, every scenario of
  the ratified spec delta has at least one automated test over temporary
  fixtures, and the repository's four CI jobs (Linux and macOS, each on two
  supported runtime versions) stay green.
- **SC-011**: A reader of the README alone can name the question's default, the
  answers that take each path, the flags that skip the question, and how to
  create a single repository without being asked.

## Scope

**In scope**: `project new` only: the creation question, the known obstacles,
the organization and visibility prompts and the restating line, the creation
advisory and its guarded write, the order of output under `--workflow`, the
README and `AGENTS.md` text, and automated tests over temporary fixtures.

**Out of scope**: any new flag, any environment variable other than reading
`CI`, any configuration file or per-person setting; any change to `status`,
`doctor`, `update`, `clean` or `benches` or to their human or JSON output (the
inspection advisory is outside the ratified list of forms); any edit to
workBenches, including `scripts/new-project.sh`, `scripts/onp`,
`config/openrepoproject-pin.json` and `setup-openspeckit`; converting an
existing repository or running `adopt-project.py`; writing
`single-repository.yaml` or any manifest; any gate, check, CI step, review
output or `--json` field; a bench generator inside a Triad; suppressing or
coordinating with `setup-openspeckit`'s own advisory; changing interrupt
handling while openRepoShape runs; and any change to openRepoShape's prompts,
name rules or exit statuses.

## Assumptions

- The spec names flags, standard streams, exit statuses, `CI`, file names and
  the two name patterns because the ratified delta
  (`openspec/changes/prefer-triad-in-project-new/specs/project-command/spec.md`)
  fixes them as behaviour, and faithfulness to it outranks the template's
  advice to stay technology-agnostic.
- The readers are the owners and reviewers of `project` and the people who
  create projects with it at a terminal, so the spec is written for them rather
  than for non-technical stakeholders, again by faithfulness to the packet.
- Exact wording is cited from the ratified change's `design.md`, D13, rather
  than repeated, and nothing here changes it.
- `.specify/memory/constitution.md` is still the unfilled template, so the
  ratified packet is the only governing source for this feature.
- No clarification marker is used: `tasks.md` 1.5 records that no open question
  changes what is built, and the two questions `design.md` leaves to the lead
  (filing the D9 alternative, notes for the workBenches issue) change nothing
  here.
- Typed organization and visibility answers count as explicit (delta,
  MODIFIED "Delegate project creation"; proposal, "The organisation and
  visibility prompts").
- The question is not owed for a `-wip` name, and only the name form is read
  at creation (`clarifications.md`, "Is the creation question owed for a `-wip`
  name?"; `design.md` D10, which keeps this unless the doctrine owner,
  openxFactory lane codeXfactory-5, says otherwise).
- A valued choosing flag counts as given when it is on the command line, even
  with an empty value (`design.md` D1).
- A single repository counts as created once its destination is a directory and
  its `.project.json` exists, whether or not Git was initialised (proposal,
  "What counts as creating a single repository").
- The restating line is printed in a dry run too (`design.md` D5), since the
  delta places it before the plan and a dry run shows the plan.
- An agent at a pseudo-terminal is not detected, and for such a run the
  guarantee rests on the typed confirmations and the agent instructions
  (`clarifications.md`, "Agents at a pseudo-terminal look like people";
  `design.md` D11).
- Which standard stream the question's prompt appears on is left unspecified
  and untested, because it follows the existing prompts and differs between a
  real terminal and a test harness (`clarifications.md`, "The prompt's stream
  differs between harnesses"; `design.md` D4).
- Ctrl-C while openRepoShape runs keeps today's behaviour and is documented,
  not changed (`clarifications.md`, "Ctrl-C while openRepoShape runs";
  `design.md` D9).
- No exit status is promised for openRepoShape's own refusals, only that they
  pass through (`clarifications.md`, "Exit codes on the Triad path";
  `design.md` D12).
- Two offers in one `--workflow` run are an accepted consequence, and real
  suppression is a workBenches follow-up (`clarifications.md`, "The interactive
  double question under `--workflow`"; `design.md` D8).
- openRepoShape, the bench generators and `setup-openspeckit` keep their own
  behaviour, and both name forms are pinned from openRepoShape
  `contracts/repository-naming.yaml` at `1a9fc537` (`design.md` D3 and D10).
- workBenches' `onp` and `new-project.sh` reach this behaviour only after
  workBenches moves its pinned `project` artifact on its owner's act, and this
  feature edits nothing in workBenches (proposal, "Why" and Impact,
  "Handoffs").
