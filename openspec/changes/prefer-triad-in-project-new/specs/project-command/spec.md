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
- **WHEN** creation is requested with --dry-run, whether the path was chosen by flag or by an answer to the creation question
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

## ADDED Requirements

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
its existing order of refusals. The question SHALL come before the chosen
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
- **AND** a Triad answer prints the openRepoShape plan, a single-repository answer prints the generator plan, and neither writes anything

#### Scenario: Refusals before a path is chosen come first
- **WHEN** the name is invalid, or a positional parent is given together with --into, or the destination already exists
- **THEN** the command refuses with exit status 2
- **AND** the creation question is never shown

#### Scenario: The workflow prerequisite is refused before the question
- **WHEN** --workflow is given by an invocation that will be asked the question and `setup-openspeckit` is not on PATH
- **THEN** the command refuses with exit status 2 before the creation question is shown

#### Scenario: The refusal order of an invocation not asked the question is unchanged
- **WHEN** an invocation that is not asked the question gives --workflow without `setup-openspeckit` on PATH and also names a generator that does not match
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
with its generator selection, plan and `yes` confirmation; a creation that went
through the question SHALL be followed by no creation advisory.

#### Scenario: The question's entries
- **WHEN** the creation question is asked
- **THEN** standard output shows the Triad first, marked as the default, with "preferred, not required", "elective" and "confers nothing" beside it
- **AND** it shows the single repository second, naming `single-repository.yaml` as the ratified way to record staying single, and no `single-repository.yaml` is written

#### Scenario: Answers that take the Triad
- **WHEN** the answer is Enter, `1`, `y`, `yes`, `Y` or ` YES `
- **THEN** the Triad path continues

#### Scenario: Answers that take a single repository
- **WHEN** the answer is `2`, `n`, `no`, `N` or ` No `
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
only); whether `openRepoShape` is on PATH; and whether the parent directory
exists. The Triad SHALL stay first and the default answer in every case. The
Triad's entry SHALL name each known obstacle: where the name is the problem, it
SHALL name the given name and the form a Triad name needs; where `openRepoShape`
is missing, it SHALL say so; where the parent directory is missing, it SHALL
name that directory and SHALL NOT present it as an `--into` value the person
typed.

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
- **WHEN** the parent directory, including the default projects directory, does not exist and the creation question is asked
- **THEN** the Triad's entry names that directory without presenting it as an --into value the person typed

#### Scenario: A Triad answer with a known obstacle
- **WHEN** the answer takes the Triad and any known obstacle holds
- **THEN** the command refuses with exit status 2, naming the obstacles and stating that nothing was created
- **AND** it asks for no organization or visibility, runs no openRepoShape command, makes no network access and creates nothing

#### Scenario: A dry run with a known obstacle
- **WHEN** --dry-run is given, the answer takes the Triad, and a known obstacle holds
- **THEN** the command refuses with exit status 2

#### Scenario: A single-repository answer is unaffected
- **WHEN** a known obstacle holds and the answer takes the single repository
- **THEN** the single-repository path proceeds exactly as it would without the obstacle

#### Scenario: No known obstacle
- **WHEN** the name matches the assembly-root form, `openRepoShape` is on PATH and the parent directory exists
- **THEN** the Triad's entry names no obstacle

### Requirement: A Triad answer asks for the organization and the visibility
After a Triad answer with no known obstacle, the command SHALL ask for the
GitHub organization and then for the visibility, and SHALL NOT leave the
visibility to openRepoShape's default. The organization SHALL be checked by
the command's existing organization-name check before the visibility is asked.
The visibility SHALL be typed as a full word, compared case-insensitively, from
a list that reads `private`, `public`, `internal` in that order, with no numbers
and no default.

At either prompt, an empty answer or one the prompt does not accept SHALL be
asked once more and then refused with exit status 2; end of input SHALL refuse
with exit status 2; each such refusal SHALL state that nothing was created. An
interrupt at either prompt SHALL print `Cancelled.` and exit with status 130.

Once both answers are accepted, and before the plan is shown, the command SHALL
print one line on standard output restating the name, the organization and the
visibility; for `public`, that line SHALL state that anyone can read the
repositories. The command SHALL then run openRepoShape with the typed
organization and visibility and without `--yes`, so that openRepoShape's typed
confirmation remains the confirmation. A refusal by openRepoShape SHALL be
passed through with openRepoShape's own exit status, and the command SHALL
promise no particular status for it.

#### Scenario: Organization first, then visibility
- **WHEN** the answer takes the Triad and no known obstacle holds
- **THEN** the command asks for the organization and then for the visibility
- **AND** an organization that fails the organization-name check is asked again before any visibility prompt

#### Scenario: The visibility is a full word
- **WHEN** the visibility answer is `PUBLIC` or ` private `
- **THEN** it is accepted as `public` or `private`
- **AND** an answer of `1`, `2`, `3` or an empty answer is not accepted

#### Scenario: Asked once more, then refused
- **WHEN** two answers in a row at the organization prompt, or at the visibility prompt, are empty or not accepted
- **THEN** the command refuses with exit status 2, stating that nothing was created, and runs no openRepoShape command

#### Scenario: End of input at the organization or visibility prompt
- **WHEN** input ends at the organization prompt or at the visibility prompt
- **THEN** the command refuses with exit status 2, stating that nothing was created

#### Scenario: An interrupt at the organization or visibility prompt
- **WHEN** the person interrupts at the organization prompt or at the visibility prompt
- **THEN** the command prints `Cancelled.` and exits with status 130, and nothing is created

#### Scenario: The restating line
- **WHEN** the organization and the visibility have been accepted
- **THEN** one line on standard output restates the name, the organization and the visibility before the plan is shown
- **AND** for `public`, that line states that anyone can read the repositories

#### Scenario: Delegation keeps openRepoShape's confirmation
- **WHEN** the Triad path runs without --dry-run
- **THEN** openRepoShape is run with the typed organization, the visibility as its lowercase word, and the parent directory, without --yes
- **AND** openRepoShape's own typed confirmation follows

#### Scenario: openRepoShape refuses
- **WHEN** openRepoShape exits with a nonzero status
- **THEN** the command exits with that same status

### Requirement: Creation advisory follows a single repository created without the question
When the command creates a single repository without the creation question
having been asked (chosen by flag, or not at a terminal) and the name is not a
workspace name, it SHALL give the creation advisory once the repository exists:
the generator has succeeded, the destination is a directory and its
`.project.json` exists, whether or not Git was initialised. The advisory SHALL
come before any `--workflow` step, after standard output has been flushed.

The advisory SHALL be two lines on standard error, each prefixed `warning:`,
in ASCII only. Together they SHALL carry: the preference with its posture
(preferred, not required; elective; confers nothing); openRepoShape's
`adopt-project.py`, run by a person deciding for that project, as the way to
convert; `single-repository.yaml` as the way to stop meeting the advisory; and
that nothing changes.

The advisory SHALL NOT be written to standard output in any case. It SHALL NOT
change the exit status, standard output, prompts, refusals, created files or
`.project.json`, and it SHALL NOT be a `checks` row, a `--json` field or review
output. A failure to write it, including a closed standard error, a broken pipe
or a full device, SHALL be ignored. The command SHALL NOT give it for a dry
run, a Triad creation, a creation that went through the creation question, a
workspace name, or a creation that did not succeed, and SHALL record nothing
about having given it.

#### Scenario: A single repository chosen by flag
- **WHEN** a single repository is created with --type and --yes
- **THEN** standard error carries the two `warning:` lines after the repository exists
- **AND** standard output, the created files, `.project.json` and the exit status are what they would be without the advisory

#### Scenario: A single repository created where the question is not asked
- **WHEN** `CI` is `true`, or standard output is not a terminal, and a single repository is created after the person types `yes`
- **THEN** standard error carries the two `warning:` lines after the repository exists

#### Scenario: The advisory's content
- **WHEN** the creation advisory is given
- **THEN** both lines begin `warning:` and are ASCII only
- **AND** together they state the preference with "preferred, not required", "elective" and "confers nothing", name `adopt-project.py` run by a person deciding for that project, name `single-repository.yaml`, and say that nothing changes

#### Scenario: A generator that initialises no Git repository
- **WHEN** the generator succeeds and creates the destination directory without initialising Git
- **THEN** the creation advisory is given

#### Scenario: Silent cases
- **WHEN** the creation is a dry run, a Triad creation, a creation that went through the creation question, a creation with a workspace name, a creation whose generator fails, or a creation whose generator succeeds without creating the destination
- **THEN** no creation advisory is given

#### Scenario: Standard error cannot be written
- **WHEN** standard error is closed, or is a pipe whose reading end is closed, or is a full device
- **THEN** the repository is created, and standard output and the exit status are what they would be without the advisory
- **AND** the advisory does not appear on standard output

#### Scenario: Never a report input
- **WHEN** status or doctor, in human or JSON form, is run on a repository after the advisory was given
- **THEN** their output is what it would be had no advisory been given, and nothing in the repository records the advisory

### Requirement: Creation offer precedes the workflow follow-up
Under `--workflow`, the command SHALL give its own offer first (the creation
question before creation, or the creation advisory after a single-repository
creation that the advisory covers) and SHALL then run the workflow follow-up
exactly as before, with the same arguments, so that the follow-up's own output
comes after the command's offer. The command SHALL neither suppress the
follow-up's own advisory or question nor coordinate with it. A failure of the
follow-up SHALL keep its existing report and pass its exit status through, and
the creation advisory SHALL already have been given.

#### Scenario: Two advisories back to back
- **WHEN** a single repository is created with --yes and --workflow
- **THEN** the command's two `warning:` lines are written before any output of the workflow follow-up
- **AND** the follow-up's own output, including any advisory of its own, follows unchanged

#### Scenario: The follow-up fails
- **WHEN** the workflow follow-up exits with a nonzero status after a single repository was created with --yes
- **THEN** the creation advisory has already been given
- **AND** the command reports that the project was created and workflow setup failed, and exits with the follow-up's status

#### Scenario: A single-repository answer with --workflow
- **WHEN** a person at the terminal answers the creation question with `2` and --workflow is given
- **THEN** after creation the workflow follow-up runs with the same arguments as before, and its output follows unchanged
- **AND** the command adds no creation advisory of its own

#### Scenario: A workspace name with --workflow
- **WHEN** a single repository with a workspace name is created with --workflow
- **THEN** the command gives no creation advisory and runs the workflow follow-up as before
