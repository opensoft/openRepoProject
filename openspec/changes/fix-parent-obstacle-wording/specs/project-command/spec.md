## MODIFIED Requirements

### Requirement: Known Triad obstacles are named before the question and refused on a Triad answer
Before asking the creation question, the command SHALL read three local facts,
with no network access: whether the name matches openRepoShape's assembly-root
name form `^[A-Za-z][A-Za-z0-9]*$` (a letter first, then letters and digits
only); whether `openRepoShape` is on PATH; and whether the parent is an
existing directory. The parent fact SHALL be read on the resolved parent, so
that a symbolic link is read as its target, as `parent.is_dir()` and, only
when that is false, `parent.exists()` on the same path, which tells a parent
that is missing from one that exists but is not a directory. The Triad SHALL
stay first and the default answer in every case. The Triad's entry SHALL name
each known obstacle: where the name is the problem, it SHALL name the given
name and the form a Triad name needs; where `openRepoShape` is missing, it
SHALL say so; where the parent is missing, it SHALL name that directory; where
the parent exists but is not a directory, it SHALL name it, say that it exists
and is not a directory, and say to choose a parent that is a directory. In
either parent case it SHALL name the resolved parent and SHALL NOT present it
as an `--into` value the person typed.

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
- **THEN** the single-repository path continues with its generator selection, plan and `yes` confirmation, and ends as that path ends for the same name and parent when the generator is chosen by flag: the repository is created, or that path's own refusal is made with its exit status
- **AND** no creation advisory follows

#### Scenario: No known obstacle
- **WHEN** the name matches the assembly-root form, `openRepoShape` is on PATH and the parent is an existing directory, or a symbolic link that resolves to one
- **THEN** the Triad's entry names no obstacle
