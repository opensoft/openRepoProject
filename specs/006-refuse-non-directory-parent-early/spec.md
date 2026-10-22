Lane: openRepoProject-1

# Feature Specification: Refuse a non-directory parent early

**Feature Branch**: `006-refuse-non-directory-parent-early`

**Created**: 2026-10-21

**Status**: Draft

**Input**: User description: "Refuse a parent blocked by a non-directory at
the head of project new's single-repository path, before generator selection,
the plan, the yes confirmation and any creation, dry run included
(realization of OpenSpec change refuse-non-directory-parent-early, issue
#20)."

**Source of truth**: the OpenSpec change `refuse-non-directory-parent-early`,
at `openspec/changes/refuse-non-directory-parent-early/`: the proposal, the
`project-command` spec delta (one ADDED and four MODIFIED requirements),
design D1 to D6 and clarifications N1 to N6. Governing issue:
opensoft/openRepoProject#20. Packet: PR #21
(https://github.com/opensoft/openRepoProject/pull/21), ratified by Brett Heap
("ratify 21", 2026-10-21, quoted at
https://github.com/opensoft/openRepoProject/pull/21#issuecomment-6313890629)
and landed on main by squash as `b233333` (of
`8f3ca2d`). This is the change's one linked Speckit feature (its `tasks.md`
2.1). Where this summary is shorter than the spec delta, the delta governs.
Fixed strings are those of `design.md` D2; they are quoted here only
verbatim.

**Supersession**: For a parent blocked by a non-directory, and only for such
a parent, this feature supersedes the statements that the change makes false
(`design.md` D4; proposal, Impact):

- In `specs/003-parent-obstacle-wording/`:
  - spec.md's Supersession note where it names a parent that does not exist
    with the unchanged sentence (`:25-26`);
  - User Story 3's title and intro (`:94-97`), its acceptance scenario 1
    (`:106-110`) and scenario 4's clause "the path continues with its
    generator selection, plan and `yes` confirmation" (`:118-119`);
  - EC-002 (`:130-134`), and EC-003 (`:135-138`) but its `--shape` clause
    (`:137-138`);
  - FR-002's "whether that same path exists MUST then choose its sentence"
    (`:157-158`), FR-003 (`:159-161`), and FR-008's "it continues with its
    generator selection, plan and `yes` confirmation" (`:180-181`);
  - SC-002 (`:207-208`), and the Assumptions baseline's "so both runs reach
    the same `yes` confirmation" (`:250-251`);
  - quickstart.md `:53-54`, `:113` and `:116-125` (the late refusal and the
    dry run exiting 0).
- In `specs/002-triad-first-project-new/`:
  - spec.md User Story 1 scenario 3's single-repository clause (`:59-61`)
    and scenario 7's single-repository clause (`:77-78`), User Story 3
    scenario 6 (`:163-165`) and User Story 4 scenario 7 (`:214-217`);
  - EC-003 (`:267-269`), FR-004 (`:317-320`), FR-008's "an invocation that
    is not asked MUST keep its existing order of refusals" (`:342-343`), and
    FR-011's "a single-repository answer into the existing single-repository
    path with its generator selection, plan and `yes` confirmation"
    (`:360-362`);
  - contracts/project-new.md step 7 (`:55-58`), its sentence "A run that is
    not asked keeps today's order exactly" (`:60`), and the cells of its
    table of inputs that skip the question: "the path the flags choose, with
    today's prompts and refusals" (`:35`) and "today's flow" (`:36-38`);
  - data-model.md's "A dry run ends after the plan with status 0 and nothing
    written" (`:95-96`).
- Feature 003's README check (its FR-010 `:187-189`, quickstart.md `:86` and
  spec.md `:60-62`) is superseded by this feature's README check (FR-012).

The `:35` cell of feature 002's contract is added here beyond the packet's
list. It is false in the same way as the listed `:36-38` cells, and as the
README sentence at `README.md:75-77` that the change itself rewords.
`design.md` D4 gives the statement "in substance", and this spec is its
agreed home (report A, P1; see Assumptions). Line numbers are those at
`b233333`, where both features' records read as the packet cites them. The
other statements of features 002 and 003 stay true (such as 003 SC-005 and
002 FR-013), and neither record is edited.

## Clarifications

### Session 2026-10-22

Brett Heap answered the five questions of `clarify-questions.md` on
2026-10-22, in his words "all recommended": Q1 B, Q2 A, Q3 A, Q4 B and Q5 A
(Q5 A as corrected at `f700336`).

- Q: How broad is the test matrix for the head refusal? -> A: Option B
  (recommended). AC1's six forms for every kind: each kind by `--into`, and
  the file by each of its three other routes (the positional parent,
  `PROJECTS_DIR`, the default `~/projects`), in all six forms (`--yes`,
  `--dry-run`, a terminal without `--yes`, `CI=true` at a terminal, a standard
  input that is not a terminal, and `alice-wip` at a terminal). About 60 runs
  before Q3's two kinds. The runs that answer `2` stay at `FILE` and
  `FILE/sub`.
- Q: How do the case (b) rows prove that `FILE` stays intact (report A, A1)?
  -> A: Option A (recommended). A new test takes each case (b) row of the
  known-obstacle cases through a Triad answer at a terminal and in process, as
  the two existing tests do, and checks `FILE` and the tree. The two existing
  tests stay byte for byte.
- Q: Are the optional kinds, a socket and `/dev/null`, built? -> A: Option A
  (recommended). Both are included, in the forms Q1 picks for the `--into`
  kinds. The socket is skipped when binding it raises `OSError` (`design.md`
  D3 item 1's rule).
- Q: Which faults does the order test pin against the head refusal? -> A:
  Option B (recommended). `design.md` D3 item 9 plus two runs with `FILE` as
  the parent: an invalid `--family`, refused with its own sentence; and
  `--type test --yes` with `--workbenches` naming a directory that has no
  `config/bench-config.json`, refused with the head refusal and not "Cannot
  find workBenches; ...".
- Q: Where are the change's governance tasks ticked, given FR-016? -> A:
  Option A (recommended). On this feature's branch, as PR #17 did. Before the
  first implementation commit, the change's `tasks.md` gets the 1.6 tick with
  the quote and its link, the 2.1 tick and the Speckit Handoff fields. The 2.2
  tick follows in the same PR once the first implementation step has run after
  reading that section, as feature 003 did. 3.1 to 3.3 wait for the archive.
  FR-016 narrows to the change's proposal, design, clarifications and spec
  delta, and to its `tasks.md` beyond those entries.

## User Scenarios & Testing *(mandatory)*

In every scenario below, `FILE` is a regular file with known content in a
temporary tree, `MyApp` is the name, and every path the command prints is
the resolved path. A parent is **blocked by a non-directory** when the
resolved parent, or the nearest existing path above a missing parent, exists
and is not a directory: case (a) is the parent itself, and case (b) is a
missing parent below such a path (FR-001). The **head refusal** is the
refusal of FR-005.

### User Story 1 - A flag-chosen single repository with a blocked parent is refused before the plan (Priority: P1)

A person runs `project new` and chooses the single repository by flag, or in
a way that is not asked the creation question (`CI` set, a standard input
that is not a terminal, a workspace name). The parent cannot hold the new
repository, because it, or the nearest existing path above it, exists and is
not a directory. Today the command prints the destination and the plan, asks
for `yes`, and only then fails with a raw system error; its dry run exits 0.
Instead, it refuses at once, before the plan, and names what blocks the
parent.

**Why this priority**: Today a person confirms a plan that cannot run, and a
dry run reports success for a run that cannot succeed (issue #20).

**Independent Test**: Run `project new MyApp --into FILE --type test` with
`--yes`, with `--dry-run`, and at a terminal without either, then the same
with `--into FILE/sub`. Check the refusal, the exit status, the empty
standard output and the unchanged tree.

**Acceptance Scenarios**:

1. **Given** a parent that exists and is not a directory, **When** the
   single repository is chosen by flag (`--type test --yes`), **Then** the
   command:
   - exits with status 2, prints nothing on standard output, and prints on
     standard error exactly the head refusal for case (a) of `design.md` D2,
     naming the resolved parent (a symbolic link by its target);
   - prints no `Create:` line or plan, asks for no `yes`, runs no generator,
     and leaves the temporary tree unchanged and `FILE` a regular file with
     its content.

   The parent is a regular file, a symbolic link to one, a FIFO, a socket,
   `/dev/null`, or the file given as `FILE/`, each given by `--into`
   (Clarifications, Q3). The regular file is also given as the positional
   parent, by `PROJECTS_DIR`, and as the default `~/projects` with
   `PROJECTS_DIR` unset.
2. **Given** a parent that does not exist and whose nearest existing path
   above it is `FILE` (`FILE/sub`, `FILE/a/b`, or a symbolic link to
   `FILE/x`), given by `--into`, **When** the single repository is chosen by
   flag, **Then** the command refuses in the same way. The message is the
   head refusal for case (b) of `design.md` D2, naming the resolved parent and
   `FILE` as the path that blocks it.
3. **Given** `FILE` or `FILE/sub` as the parent at a terminal, **When**
   `--type test` is given without `--yes`, **Then** the same refusal is
   made, and neither a `Create:` line nor the `Type yes to run this plan:`
   prompt appears.
4. **Given** any parent of scenarios 1 and 2, **When** `--type test
   --dry-run` is given, **Then** the command refuses with exit status 2 with
   the same message as without `--dry-run`, and prints no plan.
5. **Given** `FILE` as `--into` and no choosing flag, **When** the invocation
   is not asked the question, **Then** the head refusal is made with exit
   status 2 and no line of the creation question appears. The three ways not
   to be asked are `CI=true` at a terminal, a standard input that is not a
   terminal, and the workspace name `alice-wip` at a terminal.
6. **Given** `FILE` as the parent and an invocation that is not asked,
   **When** it also has a later fault, **Then** the command refuses with the
   head refusal and exit status 2, not with the later fault's sentence. The
   later faults are:
   - a generator that does not match (`--type nomatch --yes`);
   - `--workflow` without `setup-openspeckit` on PATH (`--type test
     --workflow --yes`);
   - any fault found by the workBenches lookup or its generator registry,
     such as `--workbenches` naming a directory that has no
     `config/bench-config.json`, refused as the head refusal and not as
     "Cannot find workBenches; ..." (Clarifications, Q4).

---

### User Story 2 - A single-repository answer with a blocked parent is refused at once (Priority: P1)

A person at a terminal is asked the creation question, the parent is blocked
by a non-directory, and the person answers `2`. Today the command goes on to
the generator list, the plan and `yes`, and then fails with a raw error; with
`--dry-run` it exits 0. Instead, it refuses at once, with the same message as
the flag-chosen path.

**Why this priority**: The answer `2` must not lead the person through
prompts and a plan that cannot run.

**Independent Test**: With two available generators in the registry and
`FILE` as `--into`, answer `2` at a terminal, with and without `--dry-run`,
and compare with the `--type test` run.

**Acceptance Scenarios**:

1. **Given** a registry with two available generators, and `FILE` or
   `FILE/sub` as the parent at a terminal with no choosing flag, **When** the
   answer is `2`, **Then**:
   - the question's parent line for that case is printed under entry 1,
     then the head refusal at once;
   - none of these appears: a generator list line, `Select a generator
     number`, a `Create:` line, or `Type yes to run this plan:`;
   - the exit status is 2 and the tree is unchanged.

   With two generators, generator selection would otherwise print its list
   and ask for a number, so these runs show that the refusal comes before
   it.
2. **Given** the same, **When** `--dry-run` is given and the answer is `2`,
   **Then** the same refusal is made with exit status 2 and no plan is
   printed.
3. **Given** `FILE` as the parent, **When** one run is asked and answers `2`
   and a baseline run gives `--type test` with no further input, **Then**:
   - both exit with status 2 with the same `REFUSED:` line, which equals the
     head refusal for `FILE`;
   - neither standard output contains `Create:`, and no `warning:` line
     appears;
   - the tree and the file are unchanged.
4. **Given** a known obstacle (the name or `openRepoShape`) and a parent
   that is not blocked, **When** the answer is `2`, **Then** the
   single-repository path continues as today, with its generator selection,
   plan and `yes` confirmation. It ends as the same name and parent end with
   the generator chosen by flag, and no creation advisory follows.

---

### User Story 3 - A missing parent below a non-directory is named truthfully at the question (Priority: P1)

A person at a terminal gives `FILE/sub` as the parent. Today the Triad's
entry says that the parent directory does not exist, and the README says
that a single-repository answer creates a missing parent; neither can happen
here. Instead, the entry names the parent and the file that blocks it, and
says to choose a parent that is a directory. A Triad answer is refused with
the same sentence.

**Why this priority**: The question's sentence must be true of the parent,
and the repair it suggests must be possible.

**Independent Test**: At a terminal with `FILE/sub` as `--into`, end input at
the question and read entry 1. Then answer Enter, with and without
`--dry-run`.

**Acceptance Scenarios**:

1. **Given** `FILE/sub` as `--into` at a terminal, **When** the creation
   question is asked, **Then**:
   - the Triad is still first and the default;
   - its entry carries exactly one parent line, last, made of the existing
     `Not possible here: ` prefix and sentence (b) of `design.md` D2,
     naming the resolved parent and `FILE`;
   - the line does not present the parent as an `--into` value the person
     typed, and no line says that the parent does not exist.
2. **Given** `FILE/sub` alone, or together with the name and `openRepoShape`
   obstacles, **When** the answer takes the Triad, **Then** the command
   refuses at once with exit status 2:
   - the refusal is the composed Triad refusal of `design.md` D2, with the
     sentences in the order name, openRepoShape, parent, and the parent
     sentence as the question printed it;
   - it states that nothing was created;
   - it asks for no organization or visibility, runs no openRepoShape
     command and makes no network access;
   - the tree and the file are unchanged.
3. **Given** `FILE/sub`, **When** `--dry-run` is given and the answer takes
   the Triad, **Then** the same refusal is made with exit status 2 and
   nothing is written.
4. **Given** either of these parents, **When** the question is asked and the
   answer takes the Triad, with or without `--dry-run`, **Then** the parent
   line and the Triad refusal are byte for byte as today:
   - a parent that exists and is not a directory, which gets sentence (a);
   - a missing parent whose nearest existing path above it is a directory,
     a dangling symbolic link named by its target included, which gets the
     missing sentence.

---

### User Story 4 - The parent is read as it is when the single-repository path is taken (Priority: P2)

The creation question can wait for an answer while the person repairs, or
breaks, the parent in another terminal. The single-repository path reads the
parent afresh when it reaches its first step. A repaired parent is then
created, and a broken one is refused there.

**Why this priority**: Reusing the question's read would turn a repaired
parent into a false refusal (council verdict V2).

**Independent Test**: In process, replace the answer prompt so that the
parent changes before the answer `2` is returned.

**Acceptance Scenarios**:

1. **Given** the creation question with `FILE` as the parent, **When** `FILE`
   is replaced by a directory before the answer `2`, and `yes` is then
   typed, **Then** the path continues to generator selection, the plan and
   the `yes` confirmation. The repository is created inside that directory
   with its project record, exit status 0.
2. **Given** the creation question with a directory as the parent, **When**
   the directory is replaced by a regular file before the answer `2`,
   **Then** the command refuses with the head refusal for case (a) naming
   it, exit status 2, asks nothing further, and creates nothing.

---

### User Story 5 - Every parent that is not blocked, and every other refusal, behaves as before (Priority: P2)

Some cases must behave exactly as today:

- parents that are directories, or that can be created;
- the shape branch and the earlier refusals;
- parents the person cannot write.

**Why this priority**: The common cases must not change, and the change
must not promise more than it checks.

**Independent Test**: Run the existing suite unchanged, then the dangling
link, the order, the shape-by-flag and the permission cases.

**Acceptance Scenarios**:

1. **Given** a dangling symbolic link to a missing path below a directory,
   by `--into`, **When** `--type test --yes` is given, **Then** the target
   and the repository are created, exit status 0, as today. A missing parent
   below a directory, and an existing directory, are likewise used as today.
2. **Given** `FILE` as the parent, **When** the invocation also has one of
   these faults, **Then** that earlier refusal is made with its own text,
   exit status 2, as before:
   - an invalid name;
   - a family that is not a single folder name, refused with its own
     sentence, "Family must be a single folder name." (Clarifications, Q4);
   - `--org`, `--visibility`, `--family` or `--elected-by` without `--shape`
     (such as `--org example --yes`).
3. **Given** `FILE` or `FILE/sub` as `--into`, **When** the Triad is chosen by
   flag with `--shape --org example --visibility private`, with or without
   `--dry-run`, **Then** the shape path's own refusal is made with its text
   unchanged, exit status 2, before any destination or plan, and the head
   refusal is not.
4. **Given** a missing parent directly below a directory the person cannot
   write, and a person who is not the superuser, **When** `--type test
   --dry-run` is given, **Then** the plan is printed and the exit status is
   0.
5. **Given** the same parent, **When** `--type test --yes` is given,
   **Then** `Create:` and the plan are printed, and the run is then refused
   with the system's permission error (`REFUSED: [Errno 13] Permission
   denied: 'PARENT'`), exit status 2, without `Nothing was created.`.
6. **Given** a parent that is not blocked, **When** `--dry-run` is given, by
   flag or by an answer, and no refusal precedes the plan, **Then** the
   command prints the destination and the command it would run, writes
   nothing, and prints no creation advisory, as today.
7. **Given** an invocation that is not asked the question and a parent that
   is not blocked, **When** it gives `--workflow` without `setup-openspeckit`
   on PATH and names a generator that does not match, **Then** it is refused
   for the generator that does not match, as today.
8. **Given** a scenario of the four MODIFIED requirements that this feature
   does not alter, **When** the existing tests that pin it run, **Then**
   they pass unchanged. These scenarios are, by requirement:
   - "Delegate project creation": "Existing project", "Shape chosen by
     flag" and "An answer is not a confirmation";
   - "Creation question is asked only of a person choosing at the
     terminal": "A person at the terminal without a choosing flag", "A
     choosing flag skips the question", "Not at a terminal", "CI is set", "A
     workspace name", "Refusals before a path is chosen come first" and "The
     workflow prerequisite is refused before the question", and, for a
     parent that is not blocked, "A dry run asks too";
   - "Creation question offers the Triad first": "The question's entries",
     "Answers that take the Triad", "One unrecognised answer", "Two
     unrecognised answers", "End of input at the question", "An interrupt at
     the question" and "End of input at an existing prompt is unchanged",
     and, for a parent that is not blocked, "Answers that take a single
     repository";
   - "Known Triad obstacles are named before the question and refused on a
     Triad answer": "A name outside the assembly-root form", "openRepoShape
     is not on PATH" and "No known obstacle".

---

### User Story 6 - The README says what a blocked parent does (Priority: P3)

A reader of the README learns three things:

- a parent blocked by a non-directory blocks both answers;
- such a parent is refused before the plan and the `yes` confirmation,
  `--dry-run` included;
- `--dry-run` reads no permissions.

**Why this priority**: Today the README says that a single-repository answer
creates a missing parent, which fails below a file.

**Independent Test**: Grep the README for each fixed text.

**Acceptance Scenarios**:

1. **Given** the README, **When** the four places that `design.md` D2 edits
   are read, **Then** each carries its fixed text exactly once (rewrapped to
   the README's line width), and the phrases it replaces are gone. The four
   places are the known-obstacles paragraph, the choosing-flag sentence, the
   dry-run sentence, and the text after "Existing destinations refuse.".
   Lines 53-55 are unchanged.

---

### Edge Cases

- **EC-001**: The reads never open the parent. A FIFO is classed without
  being opened, and the reads create nothing. A socket and `/dev/null` are
  case (a) too. Tests of both are required (Clarifications, Q3): each is a
  kind of FR-014, and meets every form that the `--into` kinds meet. The
  socket's runs are skipped where binding the socket raises `OSError`, since
  a socket path can be too long on macOS (`design.md` D3 item 1).
- **EC-002**: `FILE/` (with a trailing slash) is case (a), named as the
  resolved `FILE`. A symbolic link to `FILE` is case (a), named by its
  target. A symbolic link to `FILE/x` is case (b), with `FILE` as the path
  that blocks it.
- **EC-003**: Some dangling symbolic links are not blocked: those whose
  target's nearest existing path above it is a directory. For such a link,
  the question keeps the missing sentence, and a single repository creates
  the target, as today.
- **EC-004**: The question's line and the head refusal can differ when the
  parent changed while the question waited; this is intended. A parent that
  becomes blocked after the head read meets the late failure at creation,
  with the raw system error and exit status 2, as today.
- **EC-005**: For a blocked parent, no answer to the question can succeed:
  one answer is wasted, and the Triad refusal does not say that the single
  repository is blocked too. This is accepted, to keep the ratified question
  line reachable (`clarifications.md` N6). The README says that neither
  answer can create anything in such a parent.
- **EC-006**: An invocation with two faults names the parent first when the
  other fault is found later on the single-repository path: the workBenches
  lookup or its registry, the generator, or the late `--workflow` check. Its
  exit status stays 2. Two family faults come before the head refusal:
  - an invalid `--family` is refused at the family check;
  - a valid `--family` without `--shape` meets the shape-only refusal.

  Both orders, the two family faults before the head refusal and the later
  faults after it, are pinned by tests (FR-014; Clarifications, Q4).
- **EC-007**: For an invocation that is asked, `--workflow` without
  `setup-openspeckit` on PATH is refused before the question, and so before
  the head refusal, as today.
- **EC-008**: The permission boundary covers these cases, each failing late
  or early exactly as today:
  - an existing parent the person cannot write passes the dry run and the
    parent creation step, and the generator's own error and exit status pass
    through;
  - a read-only mount or a full disk fails late;
  - an unsearchable ancestor is refused before the question by the
    existing-destination check (`[Errno 13]`, exit 2) on the CI runtime
    versions.

  The superuser bypasses mode bits, so the permission test is skipped for
  the superuser.
- **EC-009**: Today, a symbolic-link loop as the parent, or a looped
  `PROJECTS_DIR`, ends in a traceback (exit 1) when the parent is resolved.
  This happens before the question, on the CI runtime versions (3.10 and
  3.12). This feature does not change it (report K); see Scope.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A parent MUST count as blocked by a non-directory in exactly
  two cases:
  - case (a): the resolved parent exists and is not a directory;
  - case (b): the parent does not exist, and the nearest existing path above
    it exists and is not a directory. That path is the ancestor that the
    message names.

  A missing parent whose nearest existing path above it is a directory MUST
  NOT count as blocked. This includes a dangling symbolic link whose target
  is such a missing parent.
- **FR-002**: The command MUST decide the case from local reads only, with
  no network access, no other program run, no permission read and no new
  dependency. The reads MUST go in this order, and only as far as needed
  (`design.md` D1):
  1. whether the resolved parent is a directory;
  2. whether it exists;
  3. for a missing parent, whether each path above it exists, from the
     nearest, up to the first that does;
  4. whether that path is a directory.

  The reads MUST open nothing, and they always end, since the root always
  exists.
- **FR-003**: The single-repository path MUST refuse a blocked parent as its
  first step, however the path was chosen:
  - by flag;
  - by an invocation that is not asked the creation question (`CI` set, a
    standard input or output that is not a terminal, or a workspace name);
  - by an answer that takes the single repository.

  The step MUST come after these refusals:
  - those made before the path is chosen: an invalid name, a positional
    parent together with `--into`, a family that is not a single folder
    name, and an existing destination;
  - for an invocation that is asked, `--workflow` without
    `setup-openspeckit` on PATH, and the creation question itself;
  - `--org`, `--visibility`, `--family` or `--elected-by` without
    `--shape`.

  The step MUST come before:
  - the workBenches lookup (finding workBenches and reading its generator
    registry) and generator selection;
  - for an invocation that is not asked, the refusal of `--workflow` without
    `setup-openspeckit` on PATH;
  - the destination line and the plan, the return of a dry run, the `yes`
    confirmation, and any creation.

  The delta's "generator selection" includes the workBenches lookup and its
  generator registry. The proposal's "One refusal at the head" bullet says
  so: a not-asked invocation with "a fault found later (workBenches or its
  registry, the generator, the late `--workflow` check)" gets the parent
  sentence first (report A, A2).
- **FR-004**: The step MUST read the parent afresh when it is reached, and
  MUST NOT reuse the facts read for the creation question.
- **FR-005**: The refusal MUST be printed on standard error, with exit status
  2, as `REFUSED: ` followed by sentence (a) or (b) of `design.md` D2 for
  the parent's case and then ` Nothing was created.`. The text MUST be the
  same whether the path was chosen by flag or by an answer, and with or
  without `--dry-run`. The refusal MUST print nothing on standard output, and
  MUST create, change or run nothing.
- **FR-006**: The creation question MUST keep one read, made once before it
  is asked. That read feeds both the question's lines and the Triad answer's
  composed refusal, so the two cannot diverge. When the parent is not an
  existing directory, exactly one parent line MUST appear under entry 1, last,
  after the existing `Not possible here: ` prefix:
  - the missing sentence, byte for byte as today, for a missing parent that
    is not blocked;
  - sentence (a), byte for byte as today, for case (a);
  - sentence (b) for case (b).

  Each parent line MUST name the resolved parent, and MUST NOT present it as
  an `--into` value the person typed. The Triad MUST stay first and the
  default, and the name and openRepoShape lines MUST stay unchanged.
- **FR-007**: A Triad answer with a case (b) parent MUST refuse at once with
  exit status 2, with or without `--dry-run`. The refusal is the composed
  refusal of `design.md` D2, its shape unchanged, carrying sentence (b) as
  the question printed it. It MUST come before the organization and
  visibility prompts and any network access, MUST NOT run openRepoShape, and
  MUST create nothing.
- **FR-008**: A parent that is not blocked MUST NOT be refused by this step.
  The single-repository path MUST continue with its generator selection,
  plan and `yes` confirmation as before. An answer `2` given with a name or
  openRepoShape obstacle MUST end as the flag-chosen path ends for the same
  name and parent, with no creation advisory.
- **FR-009**: The shape branch MUST keep its own refusal of a parent that is
  not an existing directory, with its text and place unchanged, before the
  destination line and plan, with or without `--dry-run`. It MUST never print
  this feature's refusal.
- **FR-010**: The step MUST read no permission, so a parent the person
  cannot write MUST still pass the dry run and fail only at creation, as
  before. This covers a parent that is such a directory, and a missing
  parent whose nearest existing path above it is such a directory:
  - creating such a missing parent is refused with the system's error and
    exit status 2;
  - in such an existing directory, the generator's own error and exit status
    pass through.

  The backstop MUST stay unchanged: the late refusal at parent creation, and
  the command's handling of system errors. The backstop MUST NOT say
  `Nothing was created.`.
- **FR-011**: The feature MUST NOT change any other behaviour. These stay as
  they are:
  - the shape branch and the Triad refusal's composition;
  - the command's top-level error handling;
  - the question's printing and prompts, and generator selection;
  - the delegate's run, and everything from project discovery down.

  The feature MUST NOT add a flag, environment variable, configuration file,
  dependency, network access or program run.
- **FR-012**: The README MUST carry the four edits fixed in `design.md` D2.
  Each edit is exact, and the rest of its paragraph stays unchanged except
  for rewrapping to the README's line width:
  - lines 60-64: the replacement from "or a parent that is missing or is not
    a directory." to the end of that paragraph;
  - lines 75-77: the choosing-flag sentence in its relative form, "exactly as
    they would be without the question";
  - lines 81-82: "unless a refusal comes first" added to the dry-run
    sentence;
  - lines 95-96: the two sentences inserted after "Existing destinations
    refuse.".

  Lines 53-55 MUST stay unchanged. A grep for each fixed text MUST find it
  exactly once, and a grep for each replaced phrase MUST find nothing. This
  check supersedes feature 003's README check.
- **FR-013**: Every changed string and added line of the command, its tests
  and the README MUST be ASCII. Untouched existing text is not this feature's
  to check or change (archived N4).
- **FR-014**: Automated tests over temporary fixtures MUST cover the cases of
  `design.md` D3, items 1 to 10, which realize the proposal's acceptance
  criteria 1 to 9. They MUST run on both CI runtime versions, with the new
  strings pinned as fixed text.

  The matrix is the wider one that Brett Heap chose (Clarifications, Q1 and
  Q3); the matrix of `design.md` D3 is the least that the tests cover. The
  kinds are:
  - case (a): `FILE`, a symbolic link to it, a FIFO, `FILE/`, a socket and
    `/dev/null`;
  - case (b): `FILE/sub`, `FILE/a/b` and a symbolic link to `FILE/x`.

  Every kind by `--into`, and `FILE` by each of its three other routes (the
  positional parent, `PROJECTS_DIR` and the default `~/projects`), MUST meet
  all six forms of the proposal's acceptance criterion 1:
  - `--type test` with `--yes`, with `--dry-run`, and at a terminal without
    `--yes`;
  - not asked, without a choosing flag: with `CI=true` at a terminal, with a
    standard input that is not a terminal, and with the workspace name
    `alice-wip` at a terminal.

  The runs that answer `2` stay at `FILE` and `FILE/sub`. The socket's runs
  are skipped where binding the socket raises `OSError`.

  Every existing test, case and assertion MUST stay unchanged except one:
  the test that pins today's late refusal for a single-repository answer
  with a file parent. It is rewritten in its comparison form (User Story 2,
  scenario 3).

  Case (b) MUST enter the existing table of known-obstacle cases as new
  rows, alone and with the name and openRepoShape obstacles, the parent line
  last. The existing dry-run obstacle test MUST gain a `FILE/sub` row, and no
  existing row may change. In addition:
  - **FILE intact for case (b)** (report A, A1). Every case (b) run MUST
    also show that `FILE` is still a regular file with its content, and that
    the tree is unchanged. The existing tests of a Triad answer with an
    obstacle check the file only for a parent that itself exists and is not
    a directory, so they would not check it for the new rows. Those tests
    stay byte for byte, and their guards are not widened (Clarifications,
    Q2); a new test MUST instead take each case (b) row through a Triad
    answer, at a terminal and in process, in the same ways those tests do,
    and make the check. The existing dry-run obstacle test already checks the
    tree for each row and the file after all its rows.
  - **The order runs** (Clarifications, Q4). Besides the order runs of
    `design.md` D3 item 9, two runs with `FILE` as the parent:
    - an invalid `--family` is refused with its own sentence ("Family must
      be a single folder name."), not with the head refusal;
    - `--type test --yes` with `--workbenches` naming a directory that has no
      `config/bench-config.json` is refused with the head refusal, not with
      "Cannot find workBenches; ...".
  - **The end of the head refusal** (report A, A3). The tests MUST pin the
    head refusal's end, ` Nothing was created.`, as fixed text of its own,
    as `design.md` D3 item 1 asks. It equals the end of the Triad refusal in
    value, but is pinned separately, because the two refusals belong to
    different requirements. Sentence (b)'s question line is pinned as fixed
    text too, with the parent and the ancestor as its only variable parts.
  - The permission test MUST be skipped when run by the superuser.
- **FR-015**: The feature's traceability record MUST map each scenario of
  the delta to its tests, by requirement and title. Two mappings are fixed:
  - the rewritten test maps to "A single repository taken at the question
    with a parent blocked by a non-directory";
  - the existing test that a single-repository answer is unaffected by
    obstacles stays mapped to the narrowed "A single-repository answer is
    unaffected" (feature 003's `traceability.md:25`, row 7).
- **FR-016**: The records of features 002 and 003, and the OpenSpec change's
  proposal, design, clarifications and spec delta, MUST NOT be edited. The
  change's `tasks.md` MUST NOT be edited either, except for the entries and
  fields below, which are edited on this feature's branch, as feature 003's
  realization did (Clarifications, Q5):
  - before the first implementation commit, 1.6 is ticked with the quote of
    Brett Heap's word and its link, 2.1 is ticked, and the Speckit Handoff
    fields name this feature's identifier, branch and repo-relative
    `tasks.md` path;
  - 2.2 is ticked later in the same pull request, once the first
    implementation step has run after reading that section.

  The other entries of that `tasks.md` stay unedited; 3.1 to 3.3 wait for the
  archive. This spec carries the supersession (above). The main spec changes
  only when the change is archived.

### Key Entities

- **Parent case**: the result of the reads of FR-002 for a resolved parent.
  It is one of four:
  - a directory;
  - not a directory (case (a), the parent itself);
  - below a non-directory (case (b), with the ancestor that blocks it);
  - missing (below a directory).

  Only cases (a) and (b) are blocked.
- **Ancestor**: in case (b), the nearest existing path above the missing
  parent, resolved. Sentence (b) names it.
- **Head refusal**: the refusal of FR-005, the first step of the
  single-repository path.
- **Question parent line**: the one line under entry 1 described in FR-006.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every test run that takes a blocked parent onto the
  single-repository path exits with status 2, and its standard error is the
  head refusal of `design.md` D2, character for character. The runs include
  every kind of FR-014 by `--into`, and `FILE` by each of its other routes,
  in each of the six forms of the first two bullets below (Clarifications, Q1
  and Q3; Assumptions, Test breadth):
  - by flag with `--yes`, at a terminal without it, and with `--dry-run`;
  - not asked, in each of the three ways;
  - by an answer `2`, with and without `--dry-run`, at `FILE` and
    `FILE/sub`.

  0 such runs print `Create:`, a plan, a generator list, `Select a generator
  number` or `Type yes to run this plan:`, and 0 change the temporary tree
  or the file.
- **SC-002**: 0 dry runs with a blocked parent exit 0. At `b233333`, every
  one does.
- **SC-003**: In every run with a case (b) parent at the question, the parent
  line and any Triad refusal carry sentence (b), naming the parent and the
  ancestor. 0 such runs say that the parent does not exist.
- **SC-004**: For parents that are not blocked, the question's lines, the
  plan and the outcome are byte for byte those at `b233333`. These parents
  are an existing directory, a symbolic link to one, a missing parent below
  a directory, and a dangling link to such a path.
- **SC-005**: In every run, these refusals keep their text: the earlier
  refusals of FR-003, the shape-only flag refusal, and the shape path's
  parent refusal. With a blocked parent, an `--org` without `--shape` keeps
  its own sentence.
- **SC-006**: All existing tests pass, unchanged except the one rewritten.
  Every scenario of the delta has at least one automated test in the
  traceability record, and both CI jobs (Linux, runtime versions 3.10 and
  3.12) are green.
- **SC-007**: In every run, a parent repaired while the question waits is
  created (exit 0), and a parent broken while it waits is refused with the
  head refusal (exit 2, nothing created).
- **SC-008**: For a person who is not the superuser, a missing parent below
  an unwritable directory behaves as today: its dry run exits 0, and its
  confirmed run ends with the system's permission error and exit 2, with no
  `Nothing was created.`.
- **SC-009**: A reader of the README alone can tell that a blocked parent
  blocks both answers, that it is refused before the plan (`--dry-run`
  included), and that `--dry-run` reads no permissions. Each fixed README
  text is found once, and each replaced phrase 0 times.
- **SC-010**: The changed strings and added lines hold 0 non-ASCII
  characters.
- **SC-011**: `onp` and `new-project.sh` users get the early refusal once
  workBenches moves its pinned `project` to the realization's merge commit
  or a later one, by its owner's act. This feature edits nothing in
  workBenches.

## Scope

**In scope**: only `project new`'s single-repository path and creation
question (`design.md` D1 to D3):

- the parent read, and its new sentence (b);
- the head refusal;
- the README edits;
- the tests;
- the entries of the change's `tasks.md` that FR-016 allows (1.6, 2.1, 2.2
  and the Speckit Handoff fields);
- this feature's records (spec, plan, tasks, traceability, quickstart).

**Out of scope** (proposal, Out of Scope; `design.md` D6):

- **Symbolic-link loops.** A symbolic-link loop as the parent, and a looped
  `PROJECTS_DIR`, belong to lane openRepoProject-4's change
  `support-later-python-versions` (PR #28, issue #22) and its follow-ups
  (report K). So do the archived N1 residuals on runtime versions that CI
  does not run (the 3.13-and-later loop, the 3.14 unsearchable ancestor);
  these read as missing here and behave as today.
- **Permissions, read-only mounts and a full disk.** No writability is read;
  these cases keep today's late failure, stated as the boundary (FR-010).
  Rewording the backstop's raw error is a possible follow-up. An
  unsearchable ancestor is already refused at the existing-destination
  check.
- A raw status read classified by error number (archived N5).
- A new flag, environment variable or configuration file.
- A line under entry 2, which would be a new form of the question.
- The Triad answer's refusal text and composition, beyond sentence (b)
  entering as a parent sentence.
- The shape branch's sentence, which is already early and true (archived
  D6).
- The CI matrix, and the README's supported-version line.
- Everything from project discovery down, and every subcommand but `new`.
  These are lane openRepoProject-2's surface, or untouched.
- **Other owners' code**: workBenches, openRepoShape and setup-openspeckit,
  and the archived changes.
- **Lane steps after the realization merges**, not this feature's: the
  merge sha cited in the change's `tasks.md` 3.1, the comment on
  workBenches#145 (`design.md` D5), and the change's archive (its `tasks.md`
  3.2 and 3.3).
- The records of features 002 and 003, and the OpenSpec change's files except
  the entries of its `tasks.md` that FR-016 allows.

## Assumptions

- **Exact names.** The spec names flags, paths, streams and exit statuses
  because the ratified delta fixes them as behaviour. That outranks the
  template's advice to stay technology-agnostic, as in features 002 and 003,
  and the spec's readers own, review and use `project`. Exact wording is
  cited from `design.md` D2, never changed here.
- **Governance.** `.specify/memory/constitution.md` is still the unfilled
  template, so the ratified packet alone governs. No clarification marker is
  used, since `design.md` records no open question that changes what is
  built.
- **The base.** The base is `b233333`. There, `project` and
  `tests/test_project.py` are byte-identical to the packet's base `961c405`.
  `README.md` differs only at line 282 (#32), which is outside every cited
  range, so the packet's line citations hold. Report A re-observed every row
  of the proposal's Observed table at `e9d6711`, and found the suite at 96
  tests, all passing on 3.12.3.
- **Test breadth.** The proposal's acceptance criterion 1 lists every form
  for "each" kind. `design.md` D3 items 2 and 3 narrow two groups of runs:
  the runs at a terminal without `--yes` to `FILE` and `FILE/sub`, and the
  not-asked runs to `FILE` by `--into`. Brett Heap chose the wider reading
  (Clarifications, Q1 B), and the socket and `/dev/null` are built (Q3 A):
  the tests cover the kinds and forms of FR-014, and D3's matrix is the least
  they cover. The behaviour holds for every kind and route (FR-003).
- **"Unchanged" tests.** "Unchanged" existing tests means that no existing
  assertion, and no existing case's expected values, is edited. New cases
  may be added beside them, as in feature 003.
- **The reports cited.** Reports A (realization readiness), H (conflict risk
  and placement) and K (parent residuals) are lane openRepoProject-1's
  reviews of the ratified packet, made on 2026-10-20 and kept outside the
  repository. Their notes are carried here where they bind the realization:
  - A1, A2 and A3 in FR-014 and FR-003;
  - P1 in the Supersession;
  - K's symbolic-link loop under Scope.

  A D1 prototype, which the PR #21 re-verification wrote, is a head start
  for the plan. It is not committed anywhere.
- **Other lanes' work.** Lane openRepoProject-2's features 004 and 005 edit
  `project` below project discovery, and their own tests. Whichever merges
  second merges main in, never by rebase or force push. Report H found:
  - no textual conflict when the two new helpers sit just before the reader
    of known obstacles, and a conflict with 004 when they sit right after
    project discovery, so the plan carries the first placement;
  - four verify commands in 004's tasks that read their baseline from
    `961c405`, and so fail once this realization is on main. Re-basing them
    is lane 2's work, not this feature's.

  Lane openRepoProject-4's PR #28 orders its realization after this one.
