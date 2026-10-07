Lane: openRepoProject-1

# Proposal: prefer-triad-in-project-new

Status: draft, proposal only, revised after the alignment review (the
resolution of every finding is recorded on PR #5). The council and the design
follow in the same pull request. Nothing here is ratified.

Governing issue: opensoft/openRepoProject#3, claimed by lane openRepoProject-1
(comment 6027807471). Contract: task 5.6 of openxFactory's ratified change
`prefer-triad-project-shape` (`openspec/changes/prefer-triad-project-shape/`
on opensoft/openxFactory main `e63809650d39586134c4ec4fdb6e9effc87a7860`,
ratified by Brett Heap on 2026-10-06, "ratify 1249 as recommended").

"Triad" is the estate's name for openRepoShape's three-repository shape: an
assembly root with a spec leg and a code leg. "Three-leg project" and
"three-repository project" stay synonyms; no machine key is renamed.

## Why

Task 5.6, verbatim, is this change's contract: "**New-project creation offers
the Triad first.** workBenches' `openspec/changes/project-command`
(`scripts/new-project.sh`, `onp`) is held by lane `project-command` and
forwards creation to `opensoft/openRepoProject`'s `project new`, whose
`--shape` mode is opt-in today. The Triad-first offer routes THROUGH that
lane's claim and openRepoProject's own governance, never around them; no
repository is created that the person has not confirmed." The packet's
`code_surface:` names this repository for exactly that: "new-project creation,
reached through workBenches' `project-command` change". Issue #3 hands the
task to this repository's governance, and this change is that governance.

The task routes through workBenches lane `project-command`'s claim as well
(`openspec/changes/project-command/`, active on workBenches main). This change
edits nothing that claim holds: `scripts/new-project.sh`, `scripts/onp` and
`config/openrepoproject-pin.json` stay as they are. `onp` runs
`new-project.sh`, which runs workBenches' `project` launcher, which runs the
artifact pinned in `config/openrepoproject-pin.json` (today `a0407904`) in the
same terminal. The scripts therefore need no edit, and they carry this
change's behaviour only once workBenches advances that pin on its owner's act.
When the realization merges, its merge sha is posted on issue #3 for
codeXfactory-5's bookkeeping (comment 6028076490), which records the 5.6 tick
in openxFactory.

The other work-start surfaces already speak the preference: the shared agent
protocol tells a session to offer the Triad first when a person creates a
project (brettheap/new-workstation#52, merged `e081c5ab`); setup-openspeckit
advises at bootstrap (opensoft/workBenches#139, merged `9fbe609c`); and
openRepoShape's scaffold, adopt and doctor carry it (opensoft/openRepoShape#164,
merged `1a9fc537`). `project new` is the one creation surface that does not:
its default is a single repository from a bench generator, and the Triad is
reached only by typing `--shape`.

## What Changes

- **`project new` offers the Triad first to a person at the terminal who has
  not chosen by flag.** It asks one question: Triad or single repository. The
  Triad is listed first and is the pre-selected answer (ratified design D2:
  "In an interactive creation the Triad is listed first and is the
  pre-selected answer"), with its posture beside it: preferred, not required;
  elective; confers nothing. A single repository is accepted without a reason
  being asked. The question creates nothing and is not a confirmation: the
  Triad answer continues into today's `--shape` path, whose openRepoShape
  typed confirmation is kept, and the single answer continues into today's
  bench path, whose `Type yes` confirmation is kept. No repository is created
  that the person has not confirmed.
- **One helper decides whether a person is at the terminal.** stdin and stdout
  are both terminals, and `CI` is unset or, stripped and compared
  case-insensitively, one of `""`, `0`, `false`, `no`. This mirrors
  setup-openspeckit's decision 1 (`is_interactive_run()`, workBenches
  `9fbe609c`). The helper decides whether the question, the interactive form of
  the offer, is shown on stdout; a single-repository creation that does not go
  through the question gets the stderr advisory instead, unless it has a
  workspace name (both below). It is a new
  pattern in `project`: `ask()` checks `sys.stdin.isatty()` only
  (`project:146-149`), and `CI` is read nowhere today. `ask()` keeps that rule
  for today's prompts (the name, the generator number, `Type yes`).
- **Flags that choose skip the question.** It is not asked when any of
  `--shape`, `--org`, `--visibility`, `--family`, `--elected-by`, `--bench`,
  `--type`, `--description` or `--yes` is given, when stdin or stdout is not a
  terminal, or when `CI` is truthy. `--dry-run`, `--workflow`, `--into` or the
  positional parent, and `--workbenches` choose nothing, so a dry run at a
  terminal asks too (setup-openspeckit's decision 10, "Dry runs ask too"). Its
  Triad answer prints today's `--shape --dry-run` plan, its single answer
  today's bench plan, and neither writes.
- **Where the question sits.** After the name is known (given, or asked by
  today's `Project name:` prompt) and after every pre-flight refusal today
  makes before a path is chosen: an invalid name, `parent` together with
  `--into`, an existing destination, and `--workflow` without
  `setup-openspeckit` on PATH. A refused invocation never sees the question.
  The question comes before the chosen path's own steps and confirmation, and
  the refusals that belong to one path (an invalid organisation or a missing
  parent directory for the Triad, no matching generator for single) follow the
  answer, as today. Invocations that skip the question keep today's order of
  refusals.
- **The answers.** Enter takes the Triad. `1` takes the Triad and `2` the
  single repository, numbered as `choose()` numbers its generator list, with
  surrounding whitespace stripped as `ask()` strips every answer. Any other
  input is asked again once; a second unrecognised answer refuses with exit 2
  and creates nothing. End-of-file at the question refuses with exit 2 and
  creates nothing (today's prompts let end-of-file fall through to
  `Cancelled.` and 130, so the question handles it itself). An interrupt exits
  130 with `Cancelled.`, as today (`project:1001-1003`). The exact prompt text
  is design's.
- **The Triad answer and its prerequisites.** The Triad stays first and the
  default in every case. A Triad answer never carries `--org` or
  `--visibility`, since either would have skipped the question, so `project`
  asks for the organisation, checked by today's organisation check
  (`project:223`), and then for the visibility, one of `public`, `private` or
  `internal`, with no default. `project` must ask rather than pass nothing
  through, because openRepoShape would default the visibility to `private`
  (`setup-project.py`, `1a9fc537`). This proposal reads a typed answer as an
  explicit one, so canonical "Shape creation SHALL require explicit
  organization and visibility" holds as written. When `openRepoShape` is not
  on PATH, the question says so beside the Triad, and a Triad answer refuses at
  once with exit 2 and today's "Install openRepoShape through workBenches
  first.", creating nothing.
- **Names.** `project` accepts `[A-Za-z0-9][A-Za-z0-9_-]*` (`project:206`),
  while openRepoShape requires an assembly-root name to be "ONE CamelCase
  token, no hyphen, underscore, dot or space" (`setup-project.py`,
  `1a9fc537`). The question states that constraint beside the Triad. `project`
  adds no second validator: a Triad answer for a name such as `my-app` reaches
  openRepoShape, and the refusal is openRepoShape's own.
- **A flag-chosen or non-interactive creation of a single repository keeps
  today's behaviour and adds the advisory on stderr** (ratified D2: "A
  non-interactive invocation does what its flags say, and prints the
  recommendation when it creates a single repository"). Stdout, prompts,
  refusals, created files, `.project.json` and exit status stay as today. Once
  the repository exists (the generator succeeded, the destination is a
  directory, `.project.json` is written) and before any `--workflow` step,
  `project` flushes stdout and writes the advisory to stderr, so a later
  workflow failure does not suppress it. A dry run creates nothing and prints
  no advisory. A Triad creation prints none. A creation that went through the
  question prints none, because the question was the offer.
- **The advisory's words.** Two lines on stderr, each prefixed `warning:`
  (setup-openspeckit's convention, `9fbe609c:2370`), carrying every element the
  ratified text requires (packet `spec.md:58-59` and `:103-105`): the
  preference with its posture (preferred, not required; elective; confers
  nothing); openRepoShape's `adopt-project.py`, run by a person deciding for
  that project, as the way to convert; `single-repository.yaml` as the way to
  stop meeting it; and that nothing changes. These are the elements of
  openRepoShape's `advisory_lines()` (`scripts/shape_advisory.py`, `1a9fc537`),
  which says "when a person deciding for this project runs it".
  setup-openspeckit's `TRIAD_ADVISORY_LINES` omits that clause; the divergence
  is recorded here and is not this change's to fix. The exact text is design's.
- **Silent for a workspace name.** The one ratified exemption readable from a
  declared fact at creation is the `<user>-wip` `workspace` form of the pinned
  naming policy, `^[a-z0-9]+(?:-[a-z0-9]+)*-wip$` (openRepoShape
  `contracts/repository-naming.yaml`, `1a9fc537`), applied to the new
  repository's name. Such a creation gets neither the question nor the stderr
  advisory, and runs exactly as today. The ratified text exempts a workspace
  repository from the advisory but is silent on the creation question for a
  workspace name; that point is carried to clarifications.
- **README and tests** describe and cover all of the above (see Impact).

## Rules This Change Keeps

The ratified packet's rules (issue #3), as non-negotiables:

- **The Triad is PREFERRED, and stays ELECTIVE and confers NOTHING**: no gate,
  no floor, no grant, no clearance eligibility, no lifecycle state and no review
  difference. Wherever `project` states the preference, in the question or in
  the advisory, it states that posture beside it.
- **A single repository stays a supported, fully conformant answer**: chosen
  without a reason asked, and created exactly as today. The only additions are
  the question before it and, where the question was not asked, the advisory
  on stderr after it.
- **No repository is created that the person has not confirmed.** The question
  is not the confirmation and creates nothing. The Triad default ends at
  openRepoShape's own typed confirmation, so no run creates three repositories
  on a default (ratified D2); the single answer ends at today's `Type yes`, or
  at the `--yes` the person typed. `project` never runs `adopt-project.py`,
  never converts an existing repository, never writes `single-repository.yaml`
  or a manifest on the advisory's account, and records nothing about having
  advised.
- **Never a gate, check or review input.** The advisory is never a `checks`
  row, never a `--json` field and never review output, and it changes no exit
  status. Where it is printed (a flag-chosen or non-interactive creation) it
  goes to stderr and changes no stdout byte. The question is asked only of a
  person at the terminal. No CI step or validator in this repository reads any
  repository's shape; the new tests run over temporary fixtures only.

## What This Repository Does Not Own

- **`single-repository.yaml`**: its schema
  (`contracts/single-repository-record.yaml`), template and silencing rule are
  openRepoShape's. Governed by opensoft/openRepoShape#163 (closed, completed)
  and realized by PR #164, squash-merged 2026-10-06 as openRepoShape main
  `1a9fc537`. This change names the file in the advisory and neither reads nor
  writes it.
- **Scaffolding, adoption and shape diagnosis**: openRepoShape (the
  `openRepoShape` launcher, `scaffold-project.py`, `adopt-project.py`,
  `shape-doctor.py`), each with its own prompts, name rules and exits.
- **The `onp` and `new-project.sh` forwarders, the launcher and the pinned
  install of `project`**: workBenches (lane `project-command`).
- **The doctrine, the advisory's meaning, its forms and its exemptions list**:
  openxFactory's ratified packet (lane codeXfactory-5). The agent-session form
  is the shared protocol's; the bootstrap form is setup-openspeckit's.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `project-command`: archive PR #4 merged as `67efa80`, so the five canonical
  specs (`project-command`, `project-review-safety`, `project-clean`,
  `project-clean-review-safety`, `speckit-extension-integration`) are on main
  under `openspec/specs/`. The spec phase writes this change's delta in
  `specs/project-command/spec.md`: a MODIFIED "Delegate project creation" for
  the question, the organisation and visibility asked at the terminal, and the
  stderr advisory; and ADDED requirements for the question and for the
  creation advisory. The standalone `project-triad-preference` capability the
  first draft named is dropped: the archived reason for standalone
  capabilities ("The existing change specifications have not yet been
  archived into the baseline specification set",
  `2026-10-07-resolve-pr-review-findings`) no longer applies. "Inspect and
  diagnose" and the `project-review-safety` requirements are untouched, because
  the inspection advisory is out of scope and the creation path reads no YAML;
  "Explicit maintenance" and "Distribution and compatibility" are untouched too.

## Impact

- **`project`**: `new()` gains the question and its routing, the organisation
  and visibility prompts for a Triad answer, and the stderr advisory after a
  single-repository creation that did not go through the question; one new
  helper decides whether a person is at the terminal. `ask()`, `confirm()`,
  `choose()`, the shape and bench paths after the answer, and every other
  subcommand are unchanged. No new flag and no network; the change reads
  nothing beyond the arguments, PATH and `CI`.
- **`README.md`**: "Create a project" describes the question (its default, its
  answers, what skips it, that a dry run asks too) and the stderr advisory, and
  its sentence "Before running, the command shows the generator and destination
  and asks for `yes`" is corrected for the new first question. The
  Configuration table gains a `CI` row. "Understand a project" is unchanged.
- **`tests/test_project.py`**:
  - a new `pty`-based helper beside `run_cli` for the question tests (stdin and
    stdout on a pseudo-terminal, stderr captured apart), on Linux and macOS as
    CI runs;
  - every question and advisory test sets `CI` and `AGENT_PROTOCOL_ROOT`
    explicitly, because the harness copies `os.environ` (`self.env`) and
    GitHub Actions sets `CI=true`; in-process `module.main()` tests patch
    `isatty` and the environment the same way;
  - a fake `openRepoShape` executable on PATH for the Triad path, recording its
    argv (no `--yes`; the typed organisation and visibility) and reading its
    own typed confirmation;
  - expected prompts, refusals and advisory lines pinned as fixtures in the
    tests, with no comparison against "today's" output, since CI checks out at
    depth 1;
  - cases for Enter, `1`, `2`, unrecognised input (asked again once, then
    refused), end-of-file, an interrupt, a hyphenated name answered Triad,
    `openRepoShape` missing, `--dry-run` at a terminal, every choosing flag,
    non-terminal stdout, `CI=true`, a `-wip` name, and the stderr advisory after
    a `--workflow` failure.
- **Speckit handoff**: implementation goes to exactly one Speckit feature,
  `specs/002-<slug>/`, created later by `/speckit.specify` (numbering is
  sequential and only `specs/001-project-command` exists). OpenSpec `tasks.md`
  holds governance boxes and that one handoff only, as the archived
  `2026-10-07-project-command/tasks.md` does.
- **No new dependency.** Handoffs this change does not perform: workBenches
  advances its pinned `project` artifact on its owner's act (lane
  `project-command`); the realization's merge sha is posted on issue #3, and
  openxFactory's archiving actor checks task 5.6's box citing it (packet
  `tasks.md` § 6).

## Out of Scope

**The inspection advisory.** Issue #3's sketch ("One possible shape. The
owning lane decides.") had `project status` and `project doctor` give the
advisory as well. That is outside the ratified text: the requirement says the
advisory "SHALL be given only at such surfaces and only in these forms" and
names three (an agent session addressing a person, the workstation bootstrap,
and openRepoShape's scaffold, adopt and doctor), and the packet's
`code_surface:` confines this repository to new-project creation. Adding it
would need the doctrine owner (openxFactory, lane codeXfactory-5) to amend the
packet, or Brett Heap's word. This change discharges task 5.6 fully without
it. So that a design can pick it up if the scope is ever extended, the review's
detection findings are recorded here:

- Configuration root: `project` reads `Path.home() / ".agents/workspace.yaml"`
  (`project:626`), while openRepoShape and setup-openspeckit read
  `${AGENT_PROTOCOL_ROOT:-$HOME/.agents}/workspace.yaml`.
- Keys read: `project` takes `SPECKIT_WORKSPACE_PATH`, then
  `orgs.<org>.path`, then `path` (`project:645`); openRepoShape reads `path`
  and every `orgs.*.path`; setup-openspeckit reads `path` and a `repository:`
  matched against `origin`'s owner and name.
- Name checked: openRepoShape checks both the directory's name and the
  `origin` name, while setup-openspeckit checks the `origin` name only ("No
  directory name, other remote, or other heuristic is read").
- Remote parsing: `project`'s `remote_repository_identity` accepts only
  `github.com` URLs (`project:618-621`), while both other readers take the last
  path segment of any remote.
- Record rule: openRepoShape silences on a `single-repository.yaml` that
  parses, by its own stdlib YAML subset, as a mapping whose `kind` is
  `single-repository-record`; setup-openspeckit reads only the top-level
  `kind:` line of a regular, non-symlink file; `project` parses YAML with
  PyYAML (`read_yaml`, `project:37-48`).

The exemptions stay the packet's ratified five: an elected Triad root, a leg
clone, a family holder, a `<user>-wip` workspace repository, and a project that
recorded staying single. A directory that is not a Git repository is not a
repository at all (openRepoShape's `not-a-repository`), not a sixth exemption.

**Pre-existing and untouched:** `project doctor --validate --strict` already
exits 1 for any single repository, because `--validate` adds the `warning` row
"No shape validators apply to this single repository" (`project:812-813`) and
`--strict` turns any warning into exit 1 (`project:828-829`). This change
neither causes nor alters that.

Also out of scope:

- Converting an existing repository, or wrapping `adopt-project.py` in
  `project`.
- Writing `single-repository.yaml` from any prompt (setup-openspeckit holds the
  same out, its decision 3).
- Any gate, check, CI step, review output or `--json` field.
- The output of `project status`, `doctor`, `update`, `clean` and `benches`.
- A bench generator inside a Triad: choosing the Triad creates openRepoShape's
  structure only, as `--shape` does today ("requires a future adapter").
- setup-openspeckit's advisory wording, which omits "run by a person deciding
  for that project": workBenches' to fix.
- workBenches' forwarders, launcher and pin (see Why).

## Questions Resolved by the Alignment Review

- **OQ-1, the inspection advisory:** not admitted by the ratified list of forms;
  the change is creation-only (Out of Scope).
- **OQ-2, D2's stderr line:** allowed and owed; a flag-chosen or non-interactive
  single-repository creation keeps today's stdout, prompts, refusals, files,
  `.project.json` and exit status, and adds the two-line advisory on stderr once
  the repository exists.
- **OQ-3, reading exemptions offline:** moot at creation; the one exemption read
  is the `-wip` name form, and the inspection-time divergences are recorded
  under Out of Scope.
- **OQ-4, the Triad answer's prerequisites:** the Triad stays first and the
  default; the organisation and visibility are asked, with no default
  visibility; a missing `openRepoShape` is stated in the question and refused
  on a Triad answer; the CamelCase constraint is stated and its refusal stays
  openRepoShape's.

Carried to clarifications: whether the creation question is owed for a
workspace (`-wip`) name, on which the ratified text is silent.
