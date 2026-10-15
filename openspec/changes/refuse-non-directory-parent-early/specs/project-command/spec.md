Lane: openRepoProject-1

## ADDED Requirements

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
not a single folder name, an existing destination, and, for an invocation that
is asked, the refusal of `--workflow` without `setup-openspeckit` on PATH and
the creation question) and after the refusal of `--org`, `--visibility`,
`--family` or `--elected-by` without `--shape`. It SHALL come before generator
selection, the refusal of `--workflow` without `setup-openspeckit` on PATH for
an invocation that is not asked, the destination and plan, the `yes`
confirmation, any creation, and the return of a dry run.

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
that is not an existing directory. The step SHALL read no permission:
`--dry-run` reads no permissions, and a parent that is a directory the person
cannot write, or a missing parent whose nearest existing path above it is such
a directory, still passes the dry run and fails at creation, as before: the
creation of such a missing parent is refused with the system's error and exit
status 2, and in such a directory the generator's own error and exit status
pass through.

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
- **WHEN** the parent does not exist, the nearest existing path above it is a directory the person cannot write, and the person is not the superuser
- **THEN** a dry run prints the plan and exits with status 0
- **AND** a confirmed run prints the plan and is then refused with the system's permission error and exit status 2, without this requirement's message

#### Scenario: The parent refusal comes after the earlier refusals
- **WHEN** the parent is blocked by a non-directory and the invocation also has an invalid name, a family that is not a single folder name, or `--org`, `--visibility`, `--family` or `--elected-by` without `--shape`
- **THEN** that earlier refusal is made, as before, with exit status 2

#### Scenario: The parent refusal comes before generator selection
- **WHEN** the parent is blocked by a non-directory and the invocation, not asked the question, also names a generator that does not match, or gives `--workflow` without `setup-openspeckit` on PATH
- **THEN** the command refuses with this requirement's message and exit status 2

#### Scenario: The shape branch's parent refusal is unchanged
- **WHEN** the Triad is chosen by flag, with `--shape`, `--org` and `--visibility`, and the parent is not an existing directory
- **THEN** the command refuses with exit status 2 with the shape path's own refusal, as before, before any destination or plan and with or without `--dry-run`, and not with this requirement's message

## MODIFIED Requirements

### Requirement: Delegate project creation
The command SHALL list usable generators, accept a name and parent, present a
plan, preserve generator failures, and refuse an existing destination. Shape
creation SHALL require explicit organization and visibility and retain owner
prompts; an organization and a visibility that the person types at the
command's own prompts after a Triad answer SHALL count as explicit.

Where a person at the terminal creates a project without choosing by flag, the
command SHALL offer the Triad (openRepoShape's three-repository shape: an
assembly root with a spec leg and a code leg) first, through the creation
question. Where a single repository is created without that question, the
command SHALL follow the creation with the creation advisory on standard error.

The command SHALL create no repository that the person has not confirmed. The
creation question is not a confirmation: the Triad path ends at openRepoShape's
own typed confirmation, and the single-repository path ends at the command's
`yes` confirmation or at a `--yes` the person gave.

#### Scenario: Preview
- **WHEN** creation is requested with --dry-run, whether the path was chosen by flag or by an answer to the creation question, and no refusal precedes that path's plan
- **THEN** the command prints the destination and the command it would run (the selected generator for a single repository, or the openRepoShape command for a Triad) without writes
- **AND** it prints no creation advisory

#### Scenario: Existing project
- **WHEN** the destination already exists
- **THEN** the command refuses before running the generator.

#### Scenario: Shape chosen by flag
- **WHEN** creation is requested with --shape, --org and --visibility, with or without --yes
- **THEN** no creation question is asked and no creation advisory is printed
- **AND** openRepoShape is run without --yes, so its own typed confirmation is retained

#### Scenario: An answer is not a confirmation
- **WHEN** a person takes either answer at the creation question
- **THEN** no repository is created until the person has typed openRepoShape's confirmation (Triad) or the command's `yes` confirmation (single repository)
- **AND** a person who declines that confirmation is left with nothing created

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
is chosen: an invalid name, a positional parent together with `--into`, and an
existing destination. For an invocation that will be asked the question, the
refusal of `--workflow` without `setup-openspeckit` on PATH SHALL also come
before the question. Every invocation that is not asked the question SHALL keep
its existing order of refusals, except that a parent blocked by a non-directory
is refused before generator selection. The question SHALL come before the chosen
path's own steps, prompts and confirmation.

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
- **WHEN** the name is invalid, or a positional parent is given together with --into, or the destination already exists
- **THEN** the command refuses with exit status 2
- **AND** the creation question is never shown

#### Scenario: The workflow prerequisite is refused before the question
- **WHEN** --workflow is given by an invocation that will be asked the question and `setup-openspeckit` is not on PATH
- **THEN** the command refuses with exit status 2 before the creation question is shown

#### Scenario: The refusal order of an invocation not asked the question is unchanged
- **WHEN** an invocation that is not asked the question gives --workflow without `setup-openspeckit` on PATH and also names a generator that does not match, and its parent is not blocked by a non-directory
- **THEN** it is refused for the generator that does not match, as before this change

### Requirement: Creation question offers the Triad first
The creation question SHALL ask one question, Triad or single repository, with
its lines on standard output. The Triad SHALL be listed first, as entry 1, and
marked as the default answer, and its entry SHALL state the posture beside the
preference: preferred, not required; elective; confers nothing. The single
repository SHALL be listed second, as entry 2; it SHALL be accepted without a
reason being asked, and its entry SHALL name, in one clause,
`single-repository.yaml` as the ratified way to record staying single. The
command SHALL NOT write `single-repository.yaml`. The question's prompt SHALL
behave as the command's existing prompts do, and SHALL read naturally with the
answers: a yes takes the Triad and a no the single repository.

An empty answer (Enter), `1`, `y` or `yes` SHALL take the Triad, and `2`, `n` or
`no` SHALL take the single repository; letters SHALL be compared
case-insensitively and surrounding whitespace SHALL be ignored. Any other
answer SHALL be asked again once; a second unrecognised answer SHALL refuse
with exit status 2. End of input at the question SHALL refuse with exit status
2. Each such refusal SHALL state that nothing was created. An interrupt at the
question SHALL print `Cancelled.` and exit with status 130.

The question SHALL create nothing. A Triad answer SHALL continue into the Triad
path and a single-repository answer into the existing single-repository path,
with its generator selection, plan and `yes` confirmation where the parent is
not blocked by a non-directory; a creation that went through the question SHALL
be followed by no creation advisory.

#### Scenario: The question's entries
- **WHEN** the creation question is asked
- **THEN** standard output shows the Triad first, marked as the default, with "preferred, not required", "elective" and "confers nothing" beside it
- **AND** it shows the single repository second, naming `single-repository.yaml` as the ratified way to record staying single, and no `single-repository.yaml` is written

#### Scenario: Answers that take the Triad
- **WHEN** the answer is Enter, `1`, `y`, `yes`, `Y` or ` YES `
- **THEN** the Triad path continues

#### Scenario: Answers that take a single repository
- **WHEN** the answer is `2`, `n`, `no`, `N` or ` No `, and the parent is not blocked by a non-directory
- **THEN** the existing single-repository path continues with its generator selection, plan and `yes` confirmation
- **AND** no creation advisory follows the creation

#### Scenario: One unrecognised answer
- **WHEN** the first answer is not recognised, such as `3` or `maybe`, and the second is recognised
- **THEN** the question is asked once more and the second answer is taken

#### Scenario: Two unrecognised answers
- **WHEN** two answers in a row are not recognised
- **THEN** the command refuses with exit status 2, stating that nothing was created
- **AND** no generator and no openRepoShape command is run, and nothing is created

#### Scenario: End of input at the question
- **WHEN** input ends at the creation question
- **THEN** the command refuses with exit status 2, stating that nothing was created

#### Scenario: An interrupt at the question
- **WHEN** the person interrupts at the creation question
- **THEN** the command prints `Cancelled.` and exits with status 130, and nothing is created

#### Scenario: End of input at an existing prompt is unchanged
- **WHEN** input ends at the existing name prompt or at the `yes` confirmation
- **THEN** the command prints `Cancelled.` and exits with status 130, as before this change

### Requirement: Known Triad obstacles are named before the question and refused on a Triad answer
Before asking the creation question, the command SHALL read three local facts,
with no network access: whether the name matches openRepoShape's assembly-root
name form `^[A-Za-z][A-Za-z0-9]*$` (a letter first, then letters and digits
only); whether `openRepoShape` is on PATH; and whether the parent is an
existing directory. The parent fact SHALL be read on the resolved parent, so
that a symbolic link is read as its target, as `parent.is_dir()` and, only
when that is false, `parent.exists()` on the same path, which tells a parent
that is missing from one that exists but is not a directory, and, only for a
missing parent, `exists()` on each path above it up to the first that exists,
then that path's `is_dir()`, which tells a missing parent below a directory
from one below a path that exists but is not a directory. The Triad SHALL
stay first and the default answer in every case. The Triad's entry SHALL name
each known obstacle: where the name is the problem, it SHALL name the given
name and the form a Triad name needs; where `openRepoShape` is missing, it
SHALL say so; where the parent is missing, it SHALL name that directory; where
the parent is missing and the nearest existing path above it exists but is not
a directory, it SHALL also name that path, say that the parent cannot be
created because that path exists but is not a directory, and say to choose a
parent that is a directory; where the parent exists but is not a directory, it
SHALL name it, say that it exists and is not a directory, and say to choose a
parent that is a directory. In each parent case it SHALL name the resolved
parent and SHALL NOT present it as an `--into` value the person typed.

A Triad answer with a known obstacle SHALL refuse at once with exit status 2,
naming the obstacles and stating that nothing was created (for a missing
`openRepoShape`, with the instruction to install openRepoShape through
workBenches first). It SHALL refuse before the organization and visibility
prompts, before any network access, and without running openRepoShape, and it
SHALL do so for a dry run too. A single-repository answer SHALL be unaffected
by these facts. These checks SHALL predict only refusals openRepoShape is
certain to make; openRepoShape's own checks remain authoritative.

#### Scenario: A name outside the assembly-root form
- **WHEN** the name is `my-app` and the creation question is asked
- **THEN** the Triad is still listed first and is still the default
- **AND** the Triad's entry names `my-app` and says that a Triad name is a letter first, then letters and digits only

#### Scenario: openRepoShape is not on PATH
- **WHEN** `openRepoShape` is not on PATH and the creation question is asked
- **THEN** the Triad's entry says that openRepoShape is not on PATH

#### Scenario: The parent directory is missing
- **WHEN** the parent directory, including the default projects directory, does not exist, or is given as a dangling symbolic link, named by its target, and the creation question is asked
- **THEN** the Triad's entry names that directory without presenting it as an --into value the person typed

#### Scenario: The parent exists but is not a directory
- **WHEN** the parent, including the default projects directory, exists but is not a directory, such as a regular file or a symbolic link to one, and the creation question is asked
- **THEN** the Triad is still listed first and is still the default
- **AND** the Triad's entry names the parent, a symbolic link to a file by its target, and says that it exists but is not a directory, not that it does not exist, and to choose a parent that is a directory, without presenting it as an --into value the person typed

#### Scenario: The parent would be created below a path that is not a directory
- **WHEN** the parent does not exist, the nearest existing path above it, such as `FILE` for `FILE/sub`, exists but is not a directory, and the creation question is asked
- **THEN** the Triad is still listed first and is still the default
- **AND** the Triad's entry names the parent and that path, and says that the parent cannot be created because that path exists but is not a directory, and to choose a parent that is a directory, without presenting the parent as an --into value the person typed
- **AND** a Triad answer, with or without --dry-run, refuses with exit status 2, naming the parent with the same sentence the question printed and stating that nothing was created

#### Scenario: A Triad answer with a known obstacle
- **WHEN** the answer takes the Triad and any known obstacle holds, including a parent that exists but is not a directory
- **THEN** the command refuses with exit status 2, naming the obstacles and stating that nothing was created
- **AND** where the parent exists but is not a directory, the refusal names it with the same sentence the question printed
- **AND** it asks for no organization or visibility, runs no openRepoShape command, makes no network access and creates nothing

#### Scenario: A dry run with a known obstacle
- **WHEN** --dry-run is given, the answer takes the Triad, and a known obstacle holds, including a parent that exists but is not a directory
- **THEN** the command refuses with exit status 2
- **AND** where the parent exists but is not a directory, the refusal names it with the same sentence the question printed and states that nothing was created

#### Scenario: A single-repository answer is unaffected
- **WHEN** a known obstacle holds and the answer takes the single repository
- **THEN** the single-repository path continues, and ends as that path ends for the same name and parent when the generator is chosen by flag: the repository is created, or that path's own refusal is made with its exit status
- **AND** no creation advisory follows

#### Scenario: No known obstacle
- **WHEN** the name matches the assembly-root form, `openRepoShape` is on PATH and the parent is an existing directory, or a symbolic link that resolves to one
- **THEN** the Triad's entry names no obstacle
