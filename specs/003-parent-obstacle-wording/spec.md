Lane: openRepoProject-1

# Feature Specification: Parent obstacle wording

**Feature Branch**: `003-parent-obstacle-wording`

**Created**: 2026-10-09

**Status**: Draft

**Input**: User description: "Realize the ratified OpenSpec change
fix-parent-obstacle-wording: a parent that exists but is not a directory is
named as such, not as missing (opensoft/openRepoProject#14)."

**Source of truth**: `openspec/changes/fix-parent-obstacle-wording/`
(proposal, `project-command` spec delta, design D1 to D6, clarifications N1 to
N6), ratified by Brett Heap ("ratify 15", 2026-10-09,
https://github.com/opensoft/openRepoProject/pull/15#issuecomment-6073098640),
landed on main by squash as `26a5668`. Where this summary is shorter than the
spec delta, the delta governs.

**Supersession**: For the parent fact, this feature supersedes feature 002's
FR-012 "whether the parent directory exists" and "the missing parent
directory" (`specs/002-triad-first-project-new/spec.md:367` and `:370-371`)
with two cases: a parent that does not exist, named with the unchanged
sentence, and a parent that exists but is not a directory, named with the new
one. Feature 002's other statements of the parent fact (its `spec.md:130-132`,
`:140`, `:151-154`, `:156` and `:459-460`, `quickstart.md:118`,
`traceability.md:37`, `tasks.md:137` and `:143`) describe the missing case and
stay true of it. Feature 002's record is not edited; the delta keeps the title
"The parent directory is missing", which its `traceability.md:37` names.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A parent that is not a directory is named truthfully (Priority: P1)

A person at a terminal runs `project new` with no choosing flag, and the parent
is a regular file. Today the Triad's entry says the parent does not exist,
which sends the person to create a directory that cannot be created there. The
entry instead says that it exists and is not a directory, and what to do.

**Why this priority**: The sentence is false here and its repair fails.

**Independent Test**: At a terminal, give a regular file as the parent by each
of the four routes, end input at the question, and read the Triad's entry.

**Acceptance Scenarios**:

1. **Given** the parent given by `--into` is a regular file, or a symbolic link
   to one, **When** the creation question is asked, **Then** the Triad is
   still first and the default, and its entry carries one parent line, the
   existing `Not possible here: ` prefix and the new sentence fixed in
   `design.md` D2, naming the resolved file (a link by its target).
2. **Given** the regular file is given as the positional parent, by
   `PROJECTS_DIR`, or as the default `~/projects` with `PROJECTS_DIR` unset,
   **When** the question is asked, **Then** the entry names the resolved file
   with the same sentence; in every case above no line of the question
   contains `--into` or says that the parent does not exist, and the file is
   still a regular file with its content.
3. **Given** the README, **When** its known-obstacles paragraph is read,
   **Then** the clause "or a parent directory that does not exist." is
   replaced by the README text fixed in `design.md` D2.

---

### User Story 2 - The refusal repeats the sentence the question printed (Priority: P1)

The person presses Enter, which takes the Triad. The command refuses at once in
the same words and creates nothing; a dry run refuses the same way.

**Why this priority**: The refusal must agree with the question it follows.

**Independent Test**: With a regular file as `--into`, take the Triad with and
without `--dry-run`, and check the refusal, the exit status and the tree.

**Acceptance Scenarios**:

1. **Given** the parent exists and is not a directory, **When** the answer
   takes the Triad, **Then** it refuses with exit status 2 with the composed
   refusal fixed in `design.md` D2, carrying the parent sentence the question
   printed and stating that nothing was created, asks for no organization or
   visibility, runs no openRepoShape, makes no network access, and leaves the
   temporary tree and the file's type and content unchanged.
2. **Given** the name `my-app`, no `openRepoShape` on PATH and a regular file
   as the parent, **When** the answer takes the Triad, **Then** the refusal
   names the three obstacles in the order name, openRepoShape, parent.
3. **Given** `--dry-run` and a parent that is a regular file, a symbolic link
   to one, or a dangling symbolic link, **When** the answer takes the Triad,
   **Then** it refuses with exit status 2, naming the parent with the sentence
   the question printed, stating that nothing was created, and writing nothing.

---

### User Story 3 - Every other case reads and ends as it does today (Priority: P2)

A missing parent, a symbolic link to a directory, the other two obstacles and
a single-repository answer behave exactly as before.

**Why this priority**: The common case, a missing parent, must not change.

**Independent Test**: Run the existing tests unchanged, then the dangling,
linked-directory and single-repository cases at a terminal.

**Acceptance Scenarios**:

1. **Given** the parent, including the default projects directory, does not
   exist or is a dangling symbolic link, **When** the question is asked,
   **Then** the entry carries the missing sentence fixed in `design.md` D2,
   byte for byte as today, naming the resolved path (a dangling link by its
   target) without presenting it as an `--into` value the person typed.
2. **Given** the name fits the Triad name form, openRepoShape is on PATH and
   the parent is an existing directory or a symbolic link that resolves to
   one, **When** the question is asked, **Then** the entry names no obstacle.
3. **Given** the name `my-app`, or no `openRepoShape` on PATH, **When** the
   question is asked, **Then** the Triad stays first and the default, and the
   entry carries the same name or openRepoShape line as today.
4. **Given** a known obstacle, including a parent that exists and is not a
   directory, **When** the answer takes the single repository, **Then** the
   path continues with its generator selection, plan and `yes` confirmation,
   and ends with the same exit status, standard output from the plan on and
   refusal, if any, as the same name and parent with the generator chosen by
   flag at a terminal without `--yes`; no creation advisory follows.

---

### Edge Cases

- **EC-001**: A FIFO, or a file given with a trailing slash (`FILE/`), exists
  and is not a directory, and gets the new sentence (`design.md` D1).
- **EC-002**: A missing parent beneath a component that is not a directory
  (`FILE/sub`) keeps the missing sentence, true of it; the single-repository
  refusal there (`Not a directory`, exit 2) is unchanged. An accepted residual
  dead end (`design.md` D6), and the one case where the README's "A
  single-repository answer creates a missing parent" does not hold.
- **EC-003**: For a parent that exists and is not a directory, the
  single-repository path shows the plan, asks for `yes` and only then refuses
  (`File exists`, exit 2), and its dry run exits 0; `--shape` by flag keeps
  its own refusal. Known limitations, unchanged (`design.md` D6).
- **EC-004**: On CI's runtime versions a symbolic-link loop errors when the
  parent is resolved, and a parent under an unsearchable directory is refused
  (exit 2), both before the question as today; later versions print the
  missing sentence for them, residuals out of scope (`clarifications.md` N1).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Before asking, the command MUST still read exactly three local
  facts, in the order name, openRepoShape, parent, with no network access and
  no other program run: whether the name fits the assembly-root form
  `^[A-Za-z][A-Za-z0-9]*$`, whether `openRepoShape` is on PATH, and whether
  the parent is an existing directory. They MUST predict only refusals
  openRepoShape is certain to make; its own checks stay authoritative.
- **FR-002**: The parent fact MUST be read on the resolved parent, however it
  was given (`--into`, the positional parent, `PROJECTS_DIR` or the default
  `~/projects`), a symbolic link as its target. The obstacle MUST hold exactly
  when the resolved parent is not an existing directory; whether that same
  path exists MUST then choose its sentence (`design.md` D1).
- **FR-003**: A parent that does not exist, including the default projects
  directory and a dangling symbolic link named by its target, MUST be named
  with the missing sentence fixed in `design.md` D2, byte for byte as today.
- **FR-004**: A parent that exists and is not a directory, including a
  symbolic link to a file named by its target, MUST be named with the new
  sentence fixed in `design.md` D2, which says that it exists and is not a
  directory and to choose a parent that is a directory, and MUST NOT be named
  with the missing sentence.
- **FR-005**: When the obstacle holds, exactly one parent sentence MUST appear,
  on one line under the Triad's entry after the existing `Not possible here: `
  prefix, naming the resolved parent and not presenting it as an `--into`
  value the person typed.
- **FR-006**: The Triad MUST stay first and the default in every case; the
  name and openRepoShape obstacles MUST keep their sentences and conditions,
  and the parent sentence MUST stay last.
- **FR-007**: A Triad answer with any known obstacle, including a parent that
  exists and is not a directory, MUST refuse at once with exit status 2, in a
  dry run as in a real run, with the composed refusal fixed in `design.md` D2
  built from the sentences the question printed, not from a second read:
  before the organization and visibility prompts and any network access,
  without running openRepoShape, and creating or writing nothing.
- **FR-008**: A single-repository answer MUST be unaffected by these facts: it
  continues with its generator selection, plan and `yes` confirmation, ends as
  the same name and parent end with the generator chosen by flag (created, or
  that path's own refusal and exit status), and gets no creation advisory.
- **FR-009**: Where the name fits the form, `openRepoShape` is on PATH and the
  parent is an existing directory or a symbolic link that resolves to one, the
  Triad's entry MUST name no obstacle.
- **FR-010**: The README's clause "or a parent directory that does not exist."
  MUST be replaced by the README text fixed in `design.md` D2, the rest of
  that paragraph unchanged apart from rewrapping.
- **FR-011**: Every changed string and added line of the command, its tests
  and the README MUST be ASCII; untouched existing text is not this feature's
  to check or change (`clarifications.md` N4).
- **FR-012**: Automated tests over temporary fixtures MUST cover the cases
  listed in `design.md` D3, with the new sentence pinned as fixed text, and
  MUST leave every existing test, case and assertion unchanged; the
  feature's traceability record maps each delta scenario by title to its
  tests (`design.md` D4).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A person at a terminal whose parent is a regular file reads, in
  every run and by each of the four routes, the new sentence fixed in
  `design.md` D2, character for character and ASCII only, naming that file;
  0 such runs print "does not exist".
- **SC-002**: A missing parent prints byte for byte today's question line and
  refusal in every run.
- **SC-003**: A symbolic link to a directory gets 0 parent obstacle lines.
- **SC-004**: In every run where a Triad answer meets a parent that exists and
  is not a directory, with or without `--dry-run`, the refusal carries the
  sentence the question printed, the exit status is 2, no organization prompt
  appears, openRepoShape never starts, and the temporary tree is unchanged.
- **SC-005**: A single-repository answer with such a parent ends with the same
  exit status, standard output from the plan on and refusal line as the
  flag-chosen run, with no `warning:` line.
- **SC-006**: All 94 existing tests pass unchanged (no existing assertion or
  case edited), every delta scenario has at least one automated test, and the
  four CI jobs (Linux and macOS, two runtime versions each) stay green.
- **SC-007**: A reader of the README alone can tell that a parent that exists
  but is not a directory blocks both answers.
- **SC-008**: `onp` and `new-project.sh` users get the corrected sentence once
  workBenches moves its pinned `project` to the realization's merge commit or
  a later one, on its owner's act; this feature edits nothing in workBenches.

## Scope

**In scope**: `project new`'s creation question only: one new sentence, the
read that chooses it, the refusal built from it (its shape unchanged), the
README sentence and the tests (`design.md` D2, D3).

**Out of scope** (`design.md` D6; proposal, Out of Scope): any other string or
behaviour, including what EC-002 to EC-004 keep; the CI matrix and the
README's supported-version line; any new flag, environment variable,
configuration, surface or form; every other subcommand; feature 002's record
and the archived change; openRepoShape, setup-openspeckit and workBenches,
including the comment on workBenches#145, a lane step after the realization
merges (`design.md` D5).

## Assumptions

- The spec names flags, paths, streams and exit statuses because the ratified
  delta fixes them as behaviour, which outranks the template's advice to stay
  technology-agnostic (as in feature 002); its readers own, review and use
  `project`. Exact wording is cited from `design.md` D2, never changed here.
- `.specify/memory/constitution.md` is still the unfilled template, so the
  ratified packet alone governs; no clarification marker is used, as
  `design.md` records no open question that changes what is built.
- The single-repository baseline is the same name and parent with the
  generator chosen by flag at a terminal without `--yes`, so both runs reach
  the same `yes` confirmation; the comparison leaves the creation advisory
  out (`design.md` D3; re-verification of the packet).
- The four ways of giving the parent are tested with the regular file only,
  since the parent is resolved the same way for each (`clarifications.md`
  N6); the link and dangling cases are tested by `--into` (`design.md` D3).
- "Unchanged" existing tests means that no existing assertion and no existing
  case's expected values are edited; adding new cases beside them is allowed
  (re-verification of the packet).
- PR #11's feature (lane openRepoProject-2) edits the same files; whichever
  merges second merges main in, never by rebase (`design.md`, Risks).
