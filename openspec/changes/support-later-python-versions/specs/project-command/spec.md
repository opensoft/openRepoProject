Lane: openRepoProject-4

## ADDED Requirements

### Requirement: Supported Python versions are stated and tested
`README.md` SHALL state the supported Python versions as one closed range of
CPython minor versions, from its lowest to its highest, SHALL say that CI tests
each version in it, and SHALL call every later version untested. Wherever
`README.md` names the range, it SHALL name the same range. The CI `test` job
SHALL run the full test suite on every minor version in that range and on no
other, so that the README claims only versions CI runs. The lowest supported
version SHALL be 3.10. A minor version SHALL join the range only at its final
release, by one change that adds it both to the README's range and to the
`test` job's versions; no pre-release SHALL run in that job.

#### Scenario: Every version in the README's range is tested in CI
- **WHEN** the README's range and the `test` job's Python versions are read
- **THEN** the job's versions are exactly the minor versions from the range's lowest to its highest, and each runs the full test suite
- **AND** every place in the README that names the range names the same range

#### Scenario: The lowest supported version is 3.10
- **WHEN** the README's range is read
- **THEN** its lowest version is 3.10

#### Scenario: A version above the range is called untested
- **WHEN** a person reads the README's Python sentence
- **THEN** it names the range, says that CI tests each version in it, and says that later versions are untested

### Requirement: A parent that is a symbolic-link loop is refused before the question
On every supported Python version, `project new` SHALL refuse a looped parent
before the creation question and before any path's own steps. A parent is
looped when resolving it without requiring that it exist (the non-strict
`resolve()`) raises the interpreter's symbolic-link-loop error, or when the
system's status read of the resolved parent (`os.stat()`) fails with `ELOOP`.
This covers a symbolic link to itself, two symbolic links to each other, a
missing path below such a loop, and a loop below a symbolic link to a
directory, whether the parent is given by `--into`, by the positional parent,
by `PROJECTS_DIR` or as the default projects directory. A path that leaves a
loop by `..` and so resolves to an existing directory is not looped. Only the
resolution SHALL be read for the loop error: an error from expanding `~` SHALL
NOT be reported as a loop.

The refusal SHALL be the system's error for `ELOOP`, printed on standard error
as `REFUSED: [Errno N] TEXT: 'PARENT'`, where N and TEXT are the system's
number and text for `ELOOP`, with exit status 2, creating and changing
nothing, with or without `--dry-run`. PARENT SHALL be the parent as given,
before any resolution: the `--into` value, the positional parent, the value of
`PROJECTS_DIR`, or the default projects directory, with `~` expanded and made
absolute against the working directory as the system reports it, keeping `..`
components and symbolic links. It SHALL be the same string on every supported
version and by every route.

The refusal SHALL come after the refusals of an invalid name, of a positional
parent together with `--into`, and of a family that is not a single folder
name, and before the existing-destination check, the creation question, the
refusal of `--workflow` without `setup-openspeckit` on PATH, the refusal of
`--org`, `--visibility`, `--family` or `--elected-by` without `--shape`, the
shape path's own refusals, generator selection, the destination and plan, any
confirmation and any creation. It SHALL apply however the path would be
chosen: by flag, `--shape` included, by an invocation that is not asked the
creation question, or by a person at the terminal with no choosing flag.

#### Scenario: A looped parent by each route
- **WHEN** a single repository is chosen by flag with `--type` and `--yes`, and the parent is a symbolic link to itself, given by `--into`, by the positional parent, by `PROJECTS_DIR`, or as the default projects directory (a looping link at that path, `PROJECTS_DIR` unset)
- **THEN** the command refuses with exit status 2 with the system's `ELOOP` error naming the parent as given
- **AND** it prints no destination or plan and creates nothing

#### Scenario: A missing path below a loop
- **WHEN** the parent is `LOOP/sub`, where `LOOP` is a symbolic link to itself, or the parent is one of two symbolic links to each other
- **THEN** the command refuses with exit status 2 with the system's `ELOOP` error naming that parent as given

#### Scenario: A loop below a linked directory is named as given
- **WHEN** the parent is given as `LINK/loop`, by `--into` or by `PROJECTS_DIR`, where `LINK` is a symbolic link to a directory that holds the looping link `loop`
- **THEN** the refusal names `LINK/loop` made absolute, not the directory `LINK` resolves to

#### Scenario: A relative looped parent is named from the working directory
- **WHEN** a looped parent is given as a relative path, by `--into` or by `PROJECTS_DIR`, and the working directory was entered through a symbolic link
- **THEN** the refusal names the parent joined to the working directory as the system reports it, the physical path, not the path through the link

#### Scenario: A looped parent's dry run
- **WHEN** `--dry-run` is given and the parent is looped
- **THEN** the command refuses with exit status 2 with the same line as without `--dry-run`, and prints no plan

#### Scenario: A looped parent with the shape chosen by flag
- **WHEN** the Triad is chosen by flag, with `--shape`, `--org` and `--visibility`, and the parent is looped
- **THEN** the command refuses with exit status 2 with the system's `ELOOP` error, not with the shape path's own refusal

#### Scenario: A looped parent at the terminal is not asked
- **WHEN** the parent is looped and standard input and standard output are terminals, `CI` is unset and no choosing flag is given, or the invocation is not asked the question because `CI` is set or standard input is not a terminal
- **THEN** the command refuses with exit status 2 with the system's `ELOOP` error, and no creation question line is printed

#### Scenario: A looped parent with a family that is not a single folder name
- **WHEN** the parent is looped and `--shape` is given with a `--family` that is not a single folder name
- **THEN** the command refuses for the family, as before, with exit status 2, and not with the `ELOOP` error

### Requirement: A destination that cannot be read is refused before the question
On every supported Python version, the existing-destination check of `project
new` SHALL read the destination with one status read that does not follow a
final symbolic link (`os.lstat()`). The destination is the resolved parent
joined with the project name, or, with `--shape` and a `--family` that is not
the parent's own folder name, the resolved parent joined with the family and
the name. Where the read succeeds, the destination exists, a symbolic link
included, and the command SHALL refuse with `Destination already exists:
DESTINATION`. Where it fails with `ENOENT`, `ENOTDIR`, `EBADF` or `ELOOP`, the
destination SHALL be read as absent and the command SHALL continue. Where it
fails with any other error, the destination cannot be read, and the command
SHALL refuse with the system's error, printed on standard error as `REFUSED:
[Errno N] TEXT: 'DESTINATION'`, where N and TEXT are the system's number and
text for that error, with exit status 2, creating and changing nothing, with
or without `--dry-run`.

A destination that cannot be read includes one beneath a directory the person
cannot search (`EACCES`): a parent beneath such a directory, existing or not,
and a parent that is such a directory. It also includes one with a component
longer than the system's name limit, whether a component of the parent, the
project name or the `--family` folder, and one whose whole path is longer than
the system's path limit (`ENAMETOOLONG`). DESTINATION SHALL be the destination
built on the resolved parent, as the existing-destination refusal names it,
never the parent as given.

The check SHALL stay where it is: after the refusal of a looped parent, and
before the creation question, the refusal of `--workflow` without
`setup-openspeckit` on PATH, the refusal of `--org`, `--visibility`, `--family`
or `--elected-by` without `--shape`, the shape path's own refusals, generator
selection, the destination and plan, any confirmation and any creation,
however the path would be chosen.

#### Scenario: An existing directory beneath a directory without search permission
- **WHEN** the person is not the superuser and the parent is an existing directory beneath a directory the person cannot search
- **THEN** the command refuses with exit status 2 with the system's permission error naming the destination, before the creation question and before any plan

#### Scenario: A missing path beneath one
- **WHEN** the person is not the superuser and the parent is a missing path beneath a directory the person cannot search
- **THEN** the command refuses with exit status 2 with the system's permission error naming the destination, and creates nothing

#### Scenario: A parent without search permission
- **WHEN** the person is not the superuser and the parent is itself a directory the person cannot search
- **THEN** the command refuses with exit status 2 with the system's permission error naming the destination, and runs no generator

#### Scenario: A parent with a component longer than the system allows
- **WHEN** the parent has one component longer than the system's name limit
- **THEN** the command refuses with exit status 2 with the system's file-name-too-long error naming the destination

#### Scenario: An over-long name, family or path
- **WHEN** the project name is longer than the system's name limit and the parent is an existing directory, or `--shape`, `--org`, `--visibility` and a `--family` longer than that limit are given, or the parent's whole path is longer than the system's path limit
- **THEN** the command refuses with exit status 2 with the system's file-name-too-long error naming the destination, and prints no plan

#### Scenario: An unreadable destination's dry run
- **WHEN** `--dry-run` is given and the destination cannot be read
- **THEN** the command refuses with exit status 2 with the same line as without `--dry-run`, and prints no plan

#### Scenario: An unreadable destination with the shape chosen by flag
- **WHEN** the Triad is chosen by flag, with `--shape`, `--org` and `--visibility`, and the destination cannot be read
- **THEN** the command refuses with exit status 2 with the system's error naming the destination, not with the shape path's own refusal

#### Scenario: An unreadable destination at the terminal is not asked
- **WHEN** the destination cannot be read, whether the invocation would be asked the creation question or is not asked it
- **THEN** the command refuses with exit status 2, and no creation question line is printed

#### Scenario: An existing destination is refused as before
- **WHEN** the destination is an existing directory, a regular file, a dangling symbolic link or a symbolic link to itself
- **THEN** the command refuses with exit status 2 with `Destination already exists: DESTINATION`, as before

#### Scenario: A destination that is a symbolic link is refused as existing
- **WHEN** the person is not the superuser and the destination is a symbolic link whose target lies beneath a directory the person cannot search
- **THEN** the command refuses with exit status 2 with `Destination already exists: DESTINATION`, not with the permission error

#### Scenario: A destination below a looping folder is read as absent
- **WHEN** `--shape`, `--org`, `--visibility`, `--family FAMILY` and `--dry-run` are given, `openRepoShape` is on PATH, the parent is an existing directory, and `PARENT/FAMILY` is a symbolic link to itself
- **THEN** the destination is read as absent, and the command prints the plan and exits with status 0, as before

## MODIFIED Requirements

### Requirement: Creation question is asked only of a person choosing at the terminal
The command SHALL ask the creation question exactly when all of the following
hold, and this one terminal rule SHALL decide it:

- standard input and standard output are both terminals;
- the `CI` environment variable is unset, or its value, stripped of surrounding
  whitespace and compared case-insensitively, is one of empty, `0`, `false` or
  `no`;
- none of `--shape`, `--org`, `--visibility`, `--family`, `--elected-by`,
  `--bench`, `--type`, `--description` or `--yes` is given;
- the project name does not match `^[a-z0-9]+(?:-[a-z0-9]+)*-wip$`, the
  `<user>-wip` workspace form of openRepoShape's naming policy.

`--dry-run`, `--workflow`, `--into` or the positional parent, and
`--workbenches` choose nothing and SHALL NOT prevent the question. The
command's existing prompts (the name, the generator number and the `yes`
confirmation) SHALL keep their existing behaviour. No per-person setting,
configuration file or new option SHALL suppress the question.

The question SHALL come after the name is known, whether given or asked at the
existing name prompt, and after the refusals the command makes before a path
is chosen: an invalid name, a positional parent together with `--into`, a
looped parent, and an existing destination or one that cannot be read. For an
invocation that will be asked the question, the refusal of `--workflow`
without `setup-openspeckit` on PATH SHALL also come before the question. Every
invocation that is not asked the question SHALL keep its existing order of
refusals, except that a looped parent and a destination that cannot be read
are refused before every refusal that follows the existing-destination check,
and a parent blocked by a non-directory is refused before generator selection.
The question SHALL come before the chosen path's own steps, prompts and
confirmation.

#### Scenario: A person at the terminal without a choosing flag
- **WHEN** standard input and standard output are terminals, `CI` is unset, and a project is created with no choosing flag
- **THEN** the creation question is asked once the name is known
- **AND** it is asked before any generator list, organization prompt, plan or confirmation

#### Scenario: A choosing flag skips the question
- **WHEN** any one of --shape, --org, --visibility, --family, --elected-by, --bench, --type, --description or --yes is given at a terminal
- **THEN** no creation question is asked
- **AND** the invocation follows the path its flags choose, with its existing prompts and refusals

#### Scenario: Not at a terminal
- **WHEN** standard input or standard output is not a terminal
- **THEN** no creation question is asked

#### Scenario: CI is set
- **WHEN** `CI` is set to `true`, or to any value other than empty, `0`, `false` or `no`, at a terminal
- **THEN** no creation question is asked
- **AND** when `CI` is empty, `0`, `false` or `no`, in any letter case and with surrounding whitespace, the question is asked

#### Scenario: A workspace name
- **WHEN** the project name matches `^[a-z0-9]+(?:-[a-z0-9]+)*-wip$`
- **THEN** no creation question is asked and no creation advisory is printed
- **AND** the creation runs exactly as it would without this requirement

#### Scenario: A dry run asks too
- **WHEN** --dry-run is given at a terminal with no choosing flag
- **THEN** the creation question is asked
- **AND** a Triad answer prints the openRepoShape plan and a single-repository answer prints the generator plan, unless a refusal precedes that plan, and neither writes anything

#### Scenario: Refusals before a path is chosen come first
- **WHEN** the name is invalid, or a positional parent is given together with --into, or the parent is looped, or the destination already exists or cannot be read
- **THEN** the command refuses with exit status 2
- **AND** the creation question is never shown

#### Scenario: The workflow prerequisite is refused before the question
- **WHEN** --workflow is given by an invocation that will be asked the question and `setup-openspeckit` is not on PATH
- **THEN** the command refuses with exit status 2 before the creation question is shown

#### Scenario: The refusal order of an invocation not asked the question is unchanged
- **WHEN** an invocation that is not asked the question gives --workflow without `setup-openspeckit` on PATH and also names a generator that does not match, and its parent is neither blocked by a non-directory nor looped, and its destination can be read
- **THEN** it is refused for the generator that does not match, as before this change

### Requirement: A parent blocked by a non-directory is refused before the single-repository path's steps
The single-repository path SHALL refuse a parent blocked by a non-directory as
its first step, however the path was chosen: by flag, by an invocation that is
not asked the creation question, or by an answer that takes the single
repository. A parent is blocked by a non-directory when the resolved parent, or
the nearest existing path above it, exists and is not a directory. The command
SHALL read this afresh, locally and with no network access, when the path
reaches that step: `is_dir()` on the resolved parent, then `exists()`, then
`exists()` on each path above it up to the first that exists, then that path's
`is_dir()`. It SHALL NOT reuse the facts read for the creation question.

The step SHALL come after the refusals made before the single-repository path
(an invalid name, a positional parent together with `--into`, a family that is
not a single folder name, a looped parent, an existing destination or one that
cannot be read, and, for an invocation that is asked, the refusal of
`--workflow` without `setup-openspeckit` on PATH and the creation question)
and after the refusal of `--org`, `--visibility`, `--family` or `--elected-by`
without `--shape`. It SHALL come before generator selection, the refusal of
`--workflow` without `setup-openspeckit` on PATH for an invocation that is not
asked, the destination and plan, the `yes` confirmation, any creation, and the
return of a dry run.

The refusal SHALL exit with status 2, with or without `--dry-run`, and SHALL
create and change nothing. Where the parent itself exists and is not a
directory, it SHALL name the resolved parent, say that it exists but is not a
directory, and say to choose a parent that is a directory. Where the parent is
missing and the nearest existing path above it is not a directory, it SHALL
name the resolved parent and that path, say that the parent cannot be created
because that path exists but is not a directory, and say to choose a parent
that is a directory. In either case it SHALL state that nothing was created.

A missing parent whose nearest existing path above it is a directory SHALL NOT
be refused by this step. The shape path SHALL keep its own refusal of a parent
that passes those earlier refusals and is not an existing directory. The step
SHALL read no permission: `--dry-run` reads no permissions, and a parent that
is a directory the person can search but cannot write, or a missing parent
whose nearest existing path above it is such a directory, still passes the dry
run and fails at creation, as before: the creation of such a missing parent is
refused with the system's error and exit status 2, and in such a directory the
generator's own error and exit status pass through.

#### Scenario: A flag-chosen single repository with a parent that is not a directory
- **WHEN** the single repository is chosen by flag, such as `--type`, or by an invocation that is not asked the creation question, and the parent, given by `--into`, by the positional parent, by `PROJECTS_DIR` or as the default projects directory, exists but is not a directory, such as a regular file, a symbolic link to one or a FIFO
- **THEN** the command refuses with exit status 2, naming the resolved parent, saying that it exists but is not a directory and to choose a parent that is a directory, and stating that nothing was created
- **AND** it prints no destination or plan, asks for no `yes` confirmation, runs no generator and creates nothing

#### Scenario: A flag-chosen single repository below a path that is not a directory
- **WHEN** the single repository is chosen by flag and the parent does not exist, and the nearest existing path above it, such as `FILE` for `FILE/sub` or `FILE/a/b`, exists but is not a directory
- **THEN** the command refuses with exit status 2, naming the resolved parent and that path, saying that the parent cannot be created because that path exists but is not a directory and to choose a parent that is a directory, and stating that nothing was created
- **AND** it prints no destination or plan, asks for no `yes` confirmation and creates nothing

#### Scenario: A single-repository dry run with a parent blocked by a non-directory
- **WHEN** `--dry-run` is given, the single-repository path is chosen by flag or by an answer, and the parent is blocked by a non-directory
- **THEN** the command refuses with exit status 2 with the same message as without `--dry-run`, and prints no plan

#### Scenario: A single repository taken at the question with a parent blocked by a non-directory
- **WHEN** the creation question is asked, the parent is blocked by a non-directory, and the answer takes the single repository
- **THEN** the command refuses at once with exit status 2, with the same message as the flag-chosen path for that parent
- **AND** it shows no generator list, asks for no generator number, prints no plan and asks for no `yes` confirmation

#### Scenario: A parent repaired or broken while the question waits
- **WHEN** the creation question is asked and, before the answer that takes the single repository, a regular file at the parent is replaced by a directory, or a directory at the parent by a regular file
- **THEN** the step reads the parent as it is when the step is reached
- **AND** the repaired parent continues to generator selection, the plan and the `yes` confirmation, and the repository is created once confirmed, while the broken parent is refused with the message for a parent that exists but is not a directory

#### Scenario: A single repository with a parent that is not blocked
- **WHEN** the single-repository path is chosen and the parent is an existing directory, or does not exist and the nearest existing path above it is a directory, including a dangling symbolic link to such a path
- **THEN** this step refuses nothing, and the path continues with its generator selection, plan and `yes` confirmation as before

#### Scenario: A parent the person cannot write still fails only at creation
- **WHEN** the parent does not exist, the nearest existing path above it is a directory the person can search but cannot write, and the person is not the superuser
- **THEN** a dry run prints the plan and exits with status 0
- **AND** a confirmed run prints the plan and is then refused with the system's permission error and exit status 2, without this requirement's message

#### Scenario: The parent refusal comes after the earlier refusals
- **WHEN** the parent is blocked by a non-directory and the invocation also has an invalid name, a family that is not a single folder name, or `--org`, `--visibility`, `--family` or `--elected-by` without `--shape`
- **THEN** that earlier refusal is made, as before, with exit status 2

#### Scenario: The parent refusal comes before generator selection
- **WHEN** the parent is blocked by a non-directory and the invocation, not asked the question, also names a generator that does not match, or gives `--workflow` without `setup-openspeckit` on PATH
- **THEN** the command refuses with this requirement's message and exit status 2

#### Scenario: The shape branch's parent refusal is unchanged
- **WHEN** the Triad is chosen by flag, with `--shape`, `--org` and `--visibility`, and the parent is not an existing directory, while it is not looped and the destination can be read
- **THEN** the command refuses with exit status 2 with the shape path's own refusal, as before, before any destination or plan and with or without `--dry-run`, and not with this requirement's message
