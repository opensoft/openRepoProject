Lane: openRepoProject-1

# Design

## Context

See `proposal.md` for why and what, and `specs/project-command/spec.md` for the
requirements this design builds. The council's noted constraints are in
`clarifications.md`; this design numbers them N1 to N6 in file order, as the
council resolution comment on PR #5 does: N1 the double question under
`--workflow`, N2 agents at a pseudo-terminal, N3 Ctrl-C while openRepoShape
runs, N4 the `-wip` name, N5 the prompt's stream, N6 exit codes on the Triad
path. Each is answered by a decision below (N1 D8, N2 D11, N3 D9, N4 D10, N5
D4 and D14, N6 D12).

What in `project` shapes the approach (its code on this branch is byte-identical
to main `67efa80`):

- `new()` is one function. It validates the name, the parent and the
  destination; branches on `args.shape` into the openRepoShape command or into
  `choose()` and a generator; checks `--workflow`; prints `Create:` and the
  plan; confirms (bench path only); runs the delegate; writes `.project.json`
  (bench path only); and runs the follow-up. Every refusal is a `Refused`,
  which `main()` prints as `REFUSED: ...` on stderr with exit 2; `OSError` is
  caught the same way; `KeyboardInterrupt` and `EOFError` become `Cancelled.`
  with 130.
- `ask()` refuses when stdin is not a terminal and otherwise calls `input()`
  with a trailing space and strips the answer. It does not catch end of input.
  `CI` is read nowhere.
- `execute()` is `subprocess.run` on inherited streams, mapping a signal death
  to 128 + n.
- Tests: `run_cli` runs the file as a subprocess with `input=""`, so stdin is
  never a terminal, and with `self.env`, a copy of `os.environ`; in-process
  tests call `module.main()`. CI runs `ubuntu-latest` and `macos-latest` on
  Python 3.10 and 3.12 from a depth-1 checkout. Baseline: 43 tests pass.

Five stream facts were checked on this workstation (Python 3.12.3), because the
guarded write and the test harness rest on them:

| Probe | Observed |
| --- | --- |
| `print("ADVISORY", file=sys.stderr)` with `2>&-` | `sys.stderr` is `None`, and `ADVISORY` appears on stdout; exit 0 |
| `sys.stderr.write()` and `flush()` with the `OSError` swallowed, `2>/dev/full` | `OSError` 28 swallowed; exit **120**, because the interpreter's final flush fails on the bytes left in the buffer |
| `os.write(sys.stderr.fileno(), ...)` with the `OSError` swallowed, `2>/dev/full` | `OSError` 28 swallowed; exit 0 |
| the same `os.write` into a pipe whose read end is closed | `BrokenPipeError` 32 swallowed; exit 0 |
| `input("PROMPT? ")` with stdin and stdout on a pty slave, stderr on a pipe | `PROMPT? ` arrives on the stderr pipe (bpo-1927); the typed answer is echoed on the pty; lines end `\r\n` |

The second row is the mechanism behind the proposal's observed exit 120.

## Goals / Non-Goals

**Goals:**

- One decision value, computed once in `new()`, drives the hoisted
  `--workflow` check, the question and the advisory.
- Both answers re-enter today's code: a Triad answer supplies an organization
  and a visibility to the existing `--shape` branch, and a single-repository
  answer continues into the existing bench branch.
- Every new string is fixed here (D13) and pinned in the tests as a fixture.
- A pty harness that runs headless on both CI runners, with no controlling
  terminal.

**Non-Goals:**

- Changing `ask()`, `confirm()`, `choose()`, `execute()`, the openRepoShape
  argv, `main()`'s handlers, or any subcommand other than `new`.
- Any new flag, any environment variable other than reading `CI`, or any
  configuration file.
- Changing interrupt handling around delegates (D9).
- Any signal or argument passed to setup-openspeckit (D8).
- Any YAML read, network access, or import from openRepoShape or
  setup-openspeckit on the creation path: the two name forms are copied and
  pinned by sha (D3, D10).

## Decisions

### D1. One terminal rule and one decision, computed once

A new helper, `person_at_terminal()`, returns true only when `CI`, stripped and
lower-cased, is one of `""`, `"0"`, `"false"`, `"no"` (unset reads as `""`),
and `sys.stdin` and `sys.stdout` are both not `None` and both `isatty()`;
`AttributeError`, `OSError` and `ValueError` read as false. This is
setup-openspeckit's `is_interactive_run()` and `CI_FALSE_VALUES` (workBenches
`d86ba59`, `setup-openspeckit:2273-2285` and `:131`), its decision 1 at
`9fbe609c`.

`new()` computes three values once, immediately after the existing-destination
refusal:

- `workspace`: the name matches the workspace form (D10);
- `chosen`: any of `--shape`, `--org`, `--visibility`, `--family`,
  `--elected-by`, `--bench`, `--type`, `--description` or `--yes` is given. A
  valued option counts as given when it is present on the command line (its
  value is not `None`, even if empty) and a switch when it is set, because any
  explicit choosing flag marks a scripted or deliberate choice;
- `offer = not workspace and not chosen and person_at_terminal()`.

`offer` is the one value the hoisted check (D2), the question (D4) and the
advisory (D7) read; nothing re-derives terminal state later. `ask()` keeps its
stdin-only test for today's prompts.

Rejected alternatives:

- Reusing `ask()`'s stdin-only test: a run with stdout redirected, or in CI
  under a runner that allocates a terminal, would meet the question, against
  the packet's D2: "A non-interactive invocation does what its flags say".
- A flag or environment variable that skips the question: "No setting stops
  the question" (the packet's A3 rejects per-person suppression); the choosing
  flags already serve scripted use.
- Detecting agents from process names, `TMUX` or `TERM` (N2): a guess, and the
  ratified guard rests on confirmations, not on detection (D11).

### D2. The order inside `new()`

1. Unchanged: the name (given, or the `Project name:` prompt), the name check,
   positional parent with `--into`, parent resolution, the family check, the
   destination, the existing-destination refusal.
2. Compute `workspace`, `chosen` and `offer` (D1).
3. If `offer` and `--workflow` and `setup-openspeckit` is not on PATH: today's
   refusal, with today's text, exit 2.
4. If `offer`: read the known obstacles (D3) and ask the question (D4).
   - Triad answer: refuse on any known obstacle (D3); otherwise ask the
     organization and the visibility (D5), set `args.shape`, `args.org` and
     `args.visibility` to the answers, and print the restating line.
   - Single-repository answer: set nothing.
5. Unchanged from here: the branch on `args.shape` (shape refusals and the
   openRepoShape command, or `choose()` and the generator); today's
   `--workflow` check, which repeats harmlessly for an asked invocation;
   `Create:` and the plan; the `--dry-run` return; `confirm()` and the parent
   `mkdir` (bench path); the delegate; the destination check; `.project.json`
   (bench path).
6. If the bench path ran and `not offer and not workspace`: the creation
   advisory (D7).
7. Unchanged: the follow-ups, then `Created:` and `Next:`.

A Triad answer sets exactly the fields the flags would, so step 5 re-runs
today's shape checks on them (the organization form, `parent.is_dir()`,
`shutil.which("openRepoShape")`), which all pass by then, and builds today's
argv. A Triad answer never carries `--family` or `--elected-by`, since either
would have skipped the question, so its destination stays `parent / name`, the
path the existing-destination refusal already checked.

Rejected alternatives:

- Hoisting the `--workflow` check for every invocation: it would change
  today's refusal order for flag-chosen and scripted runs, which the proposal
  keeps ("Where the question sits").
- A separate Triad path that builds its own openRepoShape argv: two argvs to
  keep in step, against the Impact's "the openRepoShape command ... unchanged".

### D3. Known obstacles: three local reads and one pinned form

Read only when `offer` is true, in this order, with no network and no
subprocess:

1. `ASSEMBLY_NAME.fullmatch(name)`, where
   `ASSEMBLY_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9]*$")` is copied from
   openRepoShape `contracts/repository-naming.yaml:345` (family `project-leg`,
   role `assembly`) at `1a9fc537bcce37301c85fc108fabd8a599b02000`, with that
   path and sha in a comment beside it;
2. `shutil.which("openRepoShape")`;
3. `parent.is_dir()`, for the resolved parent (`--into`, the positional
   parent, or `projects_dirs()[0]`, which is `PROJECTS_DIR` or `~/projects`).

`fullmatch` rather than `match`, so a trailing newline never satisfies `$`. The
form predicts only a refusal openRepoShape is certain to make (its name check
exits 1, `setup-project.py:1532-1535`); openRepoShape's validator stays
authoritative, and any other refusal of its own passes through (D12). A name
that fails the form can still reach openRepoShape by flag: `--shape` skips the
question and this pre-check.

Rejected alternatives:

- Asking openRepoShape: its launcher fetches `setup.sh` from GitHub
  (`openRepoShape:549`) and `setup-project.py` runs `gh` in its preflight
  before its name check (`setup-project.py:1848-1852`), so the question would
  wait on the network; and its naming validator,
  `scripts/validate-repository-naming.py`, lives in an openRepoShape checkout
  that `project` cannot assume.
- Refusing such a name before the question: the council kept the Triad first
  and the default and named the obstacle beside it.
- Importing openRepoShape's contract or `shape_advisory.py`: `project` is a
  single-file artifact installed by sha and cannot assume an openRepoShape
  checkout.

### D4. The question

Its lines are written with `print()` to stdout: a header, entry 1 (the Triad),
one line per known obstacle under entry 1, and entry 2 (a single repository).
Its prompt goes through `ask()` (N5), so it lands where today's prompts land:
on stderr at a real terminal (bpo-1927, the probe above) and on stdout in an
in-process test that redirects stdout.

One helper serves the question and both Triad prompts (D5), so the three share
one rule. It takes the prompt, the accepted answers, the line printed before
the second asking, the refusal for a second miss and the refusal for end of
input:

- it calls `ask()`, which already strips the answer, and compares it
  lower-cased: `""`, `"1"`, `"y"` or `"yes"` take the Triad; `"2"`, `"n"` or
  `"no"` take a single repository;
- any other answer prints the retry line on stdout and asks once more; a
  second miss raises `Refused`, exit 2;
- `EOFError` from `input()` is caught around each of its `ask()` calls and
  raised as `Refused`, exit 2, so `main()`'s `EOFError` to 130 path stays only
  for today's prompts;
- `KeyboardInterrupt` is not caught: `main()` prints `Cancelled.` and returns
  130, as today.

Rejected alternatives:

- `choose()`: it refuses on the first unrecognised answer and has no default
  and no yes or no.
- A prompt written with `print(..., end="")` and read with
  `sys.stdin.readline()`: it would diverge from today's prompts (N5), and tests
  would be tempted to pin a stream they must not pin.
- Treating an answer as the confirmation, so that Enter creates a Triad: the
  packet's D2 says "No surface creates three repositories on a default".

### D5. The organization and visibility prompts, and the restating line

Both prompts use the D4 helper:

- organization: accepted when it fully matches `[A-Za-z0-9][A-Za-z0-9-]*`, the
  existing check (`project:223`). An empty answer or one that fails the check
  is unrecognised: asked once more, then refused with today's "Invalid GitHub
  organization name." followed by "Nothing was created." Counting a failed
  check as unrecognised follows the proposal's "Both prompts follow the
  question's rules";
- visibility: accepted when the lower-cased answer is `private`, `public` or
  `internal`; the lower-case word is what openRepoShape receives. No numbers,
  no default.

The restating line is printed on stdout once both are accepted, before
`Create:` and the plan, in a dry run as well as a real run. A preview that hid
the `public` consequence would be a worse preview, and one code path keeps the
dry run and the real run alike.

Rejected alternatives:

- Leaving the visibility to openRepoShape, which defaults it to `private`
  (`setup-project.py:428`, `1a9fc537`), against canonical "Shape creation SHALL
  require explicit organization and visibility".
- A numbered visibility list or a default: a stray Enter or digit could make
  three repositories public.
- Printing the restating line only when about to delegate: the dry run would
  then show a plan whose visibility consequence was never stated.

### D6. The single-repository answer

It sets nothing, and step 5 continues into today's bench path: the
`--org`/`--visibility`/`--family`/`--elected-by` refusal (which cannot fire),
`choose()` (its refusals follow the answer, as today), the plan, `confirm()`,
the generator and `.project.json`. Because `offer` is true, no advisory
follows.

### D7. The creation advisory and its guarded write

Placement: after `.project.json` is written or found, and before the first
follow-up. That is the first moment the packet D2's "creates a single
repository" holds, and it comes before a `--workflow` failure can return
early. The dry-run return, the generator-failure return and the "did not
create" refusal all come earlier, so those cases are silent by construction.

The write:

1. If `sys.stdout` is not `None`, flush it. stdout is already empty here
   (`show_plan()` flushes it and nothing is printed between the plan and this
   point), so the flush only orders a merged `2>&1` log.
2. If `sys.stderr` is `None` (stderr was closed at start), write nothing and
   never fall back to another stream: `print(file=None)` would write to stdout
   (probe above).
3. Build the two lines, each `warning: ` + text + `\n`, and encode them as
   ASCII with `errors="replace"`. The text is ASCII by construction: its one
   variable, the name, passed `[A-Za-z0-9][A-Za-z0-9_-]*`.
4. If `sys.stderr.fileno()` succeeds, write the bytes with `os.write` on that
   descriptor, looping over short writes. If it does not (an in-process test's
   `StringIO` has no descriptor), write the text with `sys.stderr.write()`.
5. Swallow `OSError` (`EBADF`, `EPIPE`, `ENOSPC`, `EIO`), `ValueError` and
   `AttributeError` throughout steps 1 to 4. Nothing is raised, nothing is
   returned, and nothing is recorded.

The direct descriptor write is the decision. A swallowed buffered write leaves
its bytes in `sys.stderr`'s buffer, the interpreter's final flush fails, and
the exit becomes 120 (probe above); `os.write` leaves nothing pending. Python
ignores SIGPIPE, so a closed pipe arrives as `BrokenPipeError` and is
swallowed.

Rejected alternatives:

- `print(..., file=sys.stderr)`: it writes to stdout when stderr was closed at
  start, and on a full device it leaves bytes pending that turn the exit into
  120.
- setup-openspeckit's `emit_advisory_line` (`stream.write()` and `flush()`
  inside a `try`, `setup-openspeckit:2288-2296`): the same 120 on `/dev/full`.
  It is workBenches' code and not this change's to fix.
- Writing the advisory after `Created:`: a `--workflow` failure returns before
  it.
- Writing it to stdout in a non-interactive run: the packet's D2 and the
  proposal keep stdout byte-identical.

### D8. Output order under `--workflow` (N1)

The order is fixed: `project`'s offer first (the question before creation, or
the advisory after a single-repository creation that the advisory covers), then
`setup-openspeckit --repo <destination>` with today's arguments, whose own
output, including its bootstrap advisory and, at a terminal, its question,
follows. `project` neither suppresses nor coordinates with it. The order is
deterministic: `project` finishes its writes (`os.write` returns only when the
bytes are written) before `subprocess.run` starts the follow-up on the
inherited descriptors.

Known consequences, recorded and not fixed here:

- At a terminal, a person who answered `2` meets setup-openspeckit's question,
  where since `d86ba59` (#140) `n` stops by SIGINT
  (`setup-openspeckit:2320-2356`); `project` then prints "Project created at
  ...; workflow setup failed." and exits 130.
- `--yes --workflow` prints two advisories back to back: `project`'s two
  `warning:` lines, then setup-openspeckit's.
- A `-wip` creation is silent in `project`, but setup-openspeckit may advise,
  because it reads only `origin`, which a fresh directory lacks, or the
  person's `workspace.yaml` (`setup-openspeckit:2204-2209`).

Real suppression is workBenches' follow-up, an optional "already offered"
signal that setup-openspeckit could accept, carried in the handoff issue.

Rejected alternatives:

- Passing a flag or environment variable to setup-openspeckit now: no such
  interface exists at `d86ba59`, and adding one is workBenches' change.
- Dropping `project`'s advisory under `--workflow` because setup-openspeckit
  advises: setup-openspeckit can refuse before its advisory
  (`ensure_safe_specify_destination`, `preflight_source_roots` and
  `resolve_project_shape` run first, `setup-openspeckit:4059-4078`), which
  would leave the packet's D2 unmet, and it does not share the `-wip`
  reading.

### D9. Ctrl-C while openRepoShape runs (N3): document the existing behaviour

Chosen: keep today's behaviour and document it in the README. An interrupt at
a terminal reaches the whole foreground process group, so openRepoShape and its
children receive the SIGINT themselves. `project`'s `subprocess.run` then waits
0.25 seconds (the `Popen` instance's `_sigint_wait_secs`) and kills the
launcher if it has not exited, and `main()` prints `Cancelled.` and exits 130.
If the launcher was still running, its `trap 'rm -rf -- "$WORKDIR"' EXIT`
(`openRepoShape:114`) does not run and its temporary directory is left behind;
`setup-project.py` or `gh` may print after `Cancelled.`; any repository created
before the interrupt stays.

Why document rather than change it:

- It is the existing behaviour of every `--shape` creation and of `update
  --component shape`, neither of which this change's What Changes touches; the
  Impact keeps the openRepoShape command, `execute()` and every other
  subcommand unchanged.
- The ratified guarantee is untouched: an interrupt before openRepoShape's
  typed confirmation reaches openRepoShape's own prompt, which then creates
  nothing, and an interrupt after it stops work the person confirmed.
- Changing it for the Triad answer alone would make one openRepoShape command
  behave two ways depending on how it was reached.

The alternative, not taken here: wait for the delegate. Start the child, then
ignore SIGINT in `project` until the child exits, restore the handler, and
return the child's status (130 for an interrupted launcher), so openRepoShape's
EXIT trap runs and nothing prints after `project` exits. The ignore must be set
after `Popen` returns, or as a Python-level no-op handler before it, because a
`SIG_IGN` disposition survives `execve` and a non-interactive bash cannot trap
or reset a signal that was ignored on entry, which would disable openRepoShape's
own Ctrl-C handling. Its costs: a hung delegate could then be stopped only with
Ctrl-\ or from another terminal, and its test needs a process-group signal,
which the pty helper (D14) does not send. It would serve `new --shape` and
`update --component shape` alike, as a change of its own.

The README states it in substance: "Ctrl-C while openRepoShape runs reaches
openRepoShape too; `project` stops waiting after a moment and prints
`Cancelled.`. Read openRepoShape's output, and check the organization on
GitHub, before retrying."

### D10. The workspace name (N4)

`WORKSPACE_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-wip$")`, copied from
openRepoShape `contracts/repository-naming.yaml:412` (family `workspace`) at
`1a9fc537bcce37301c85fc108fabd8a599b02000`, with that path and sha in a comment;
it is the pattern setup-openspeckit pins as `WORKSPACE_REPOSITORY_NAME`
(workBenches `d86ba59`, `setup-openspeckit:103`). It is applied with
`fullmatch` to the new repository's name only. Such a creation gets neither the
question nor the advisory: the proposal reads the offer as not owed where the
advisory is not owed (packet `spec.md:178` and `:186`). The person's workspace
configuration is not read, because the creation path reads no YAML and a path
that does not yet exist is not a declared fact. This reading stands unless the
doctrine owner (openxFactory, lane codeXfactory-5) says otherwise.

### D11. Agents at a pseudo-terminal (N2)

No detection. An agent or script that drives `project new` through tmux
`send-keys` or `expect` passes the terminal rule and meets the question, where
Enter takes the Triad. That still ends at openRepoShape's typed confirmation,
"which its AGENTS.md already makes an agent unable to answer on a person's
behalf" (packet `design.md:85-87`), and a single-repository answer ends at
`Type yes`. `AGENTS.md` gains a short section, and the README a matching
sentence: offer the Triad in conversation, in the shared protocol's words ("When
a person asks to create a new project, offer the Triad first as the default"),
then run `project new` with a choosing flag (`--shape --org --visibility`, or
`--bench` and `--type`), and never answer the creation question, the
organization, the visibility or openRepoShape's confirmation on a person's
behalf.

### D12. Exit statuses (N6)

| Case | Status | Text |
| --- | --- | --- |
| An invalid name, a positional parent with `--into`, an existing destination | 2 | today's |
| `--workflow` without `setup-openspeckit`, asked invocation, before the question | 2 | today's |
| The question: a second unrecognised answer, or end of input | 2 | D13 |
| A Triad answer with a known obstacle, dry run included | 2 | D13 |
| The organization or visibility prompt: a second miss, or end of input | 2 | D13 |
| An interrupt at the question, at either Triad prompt, or at today's prompts | 130 | `Cancelled.`, from `main()`, unchanged |
| End of input at `Project name:`, at the generator number or at `Type yes` | 130 | `Cancelled.`, unchanged |
| `Type yes` answered with anything other than `yes` | 2 | `Cancelled; no command was run.`, unchanged |
| openRepoShape exits nonzero | its own, passed through, promised by no scenario | e.g. 1 for its name check and for a declined confirmation (`setup-project.py:1532-1535`, `:1622`), 2 from most other refusals (`die()` defaults to 2, `:224-225`) |
| The generator exits nonzero | its own, unchanged | |
| The follow-up exits nonzero, including 130 after setup-openspeckit's `n` | its own, unchanged | `Project created at ...; workflow setup failed.` |
| An interrupt while openRepoShape runs | 130 | `Cancelled.`, the existing behaviour (D9) |
| The advisory cannot be written | unchanged | nothing |

Every refusal `project` adds is a `Refused`, so it exits 2 through `main()`.
The spec promises no particular status for an openRepoShape refusal, only that
it passes through.

### D13. Fixed text

All new text is ASCII. `NAME`, `ORG`, `VIS` and `PARENT` are substituted; every
other character is literal, and the tests pin these as fixtures. On stdout,
the question, with each obstacle line present only when that obstacle holds,
in the order name, openRepoShape, parent:

```
How should NAME be created? Nothing is created until you confirm.
  1. Triad (default): an assembly root with a spec leg and a code leg, made by openRepoShape. It is preferred, not required: it stays elective and confers nothing.
     Not possible here: NAME cannot be a Triad name; a Triad name is a letter first, then letters and digits only, such as MyApp.
     Not possible here: openRepoShape is not on PATH. Install openRepoShape through workBenches first.
     Not possible here: The parent directory PARENT does not exist; a Triad is created inside an existing directory.
  2. Single repository: fully supported, and no reason is asked. single-repository.yaml is the ratified way to record staying single.
```

The prompts, each passed to `ask()`, which appends one space:

- `Create it as a Triad? [Y/n or 1/2]:`
- `GitHub organization for the Triad:`
- `Visibility (private, public or internal):`

The retry lines, on stdout, before the second asking:

- question: `Answer y or 1 for the Triad, n or 2 for a single repository; Enter takes the Triad.`
- organization: `An organization name starts with a letter or digit and has only letters, digits and hyphens.`
- visibility: `Type the visibility in full: private, public or internal.`

The refusals, each printed by `main()` as `REFUSED: ` and the text, on stderr:

- question, second miss: `No recognised answer to the Triad question; nothing was created.`
- question, end of input: `No answer to the Triad question (end of input); nothing was created.`
- known obstacles: `A Triad cannot be created here. ` followed by the obstacle sentences above (without `Not possible here: `), joined by single spaces, then ` Nothing was created.`
- organization, second miss: `Invalid GitHub organization name. Nothing was created.`
- organization, end of input: `No GitHub organization was given (end of input); nothing was created.`
- visibility, second miss: `Visibility must be private, public or internal. Nothing was created.`
- visibility, end of input: `No visibility was given (end of input); nothing was created.`

The restating line, on stdout:

- `Triad NAME in organization ORG, visibility VIS.`
- for `public`: `Triad NAME in organization ORG, visibility public: anyone can read the repositories.`

The creation advisory, on stderr:

```
warning: NAME was created as a single repository. The Triad (an assembly root with a spec leg and a code leg) is preferred, not required: it stays elective and confers nothing.
warning: openRepoShape's adopt-project.py converts a repository in place when a person deciding for this project runs it, and a project that stays single can say so in single-repository.yaml. Nothing here changes.
```

The advisory keeps openRepoShape's clause "when a person deciding for this
project runs it" (`advisory_lines()`, `scripts/shape_advisory.py:207-215`,
`1a9fc537`) and states the posture in the packet's three terms; it carries the
four elements the spec requires.

### D14. Tests

All in `tests/test_project.py`; no new dependency.

- **The pty helper**, beside `run_cli`, for the question tests on Linux and
  macOS: stdin and stdout on one `os.openpty()` slave, stderr on its own pipe;
  a `Popen` child started with `start_new_session=True`, so the pty is never
  the test runner's controlling terminal; a `select` loop draining the master
  and the stderr pipe until the child exits, treating `EIO` (Linux) and an
  empty read (macOS) as end of output; each answer written to the master only
  after its prompt has appeared on either stream, since no test pins the
  prompt's stream; SIGINT sent with `send_signal` and repeated until the child
  exits; `\r\n` normalised to `\n`, and echoed input ignored, with assertions
  on expected lines rather than on the whole pty transcript; a timeout on every
  run; no `pty.fork`, which forks a threaded runner and makes the pty a
  controlling terminal.
- **In-process tests** (`module.main()`) patch `builtins.input` and the
  `isatty` of `sys.stdin` and `sys.stdout`, and set `CI` with
  `patch.dict(os.environ, ...)`. No test, pty or in-process, asserts which
  stream a prompt appears on.
- **The environment**: every question and advisory test sets `CI` explicitly,
  because `self.env` copies `os.environ` and GitHub Actions sets `CI=true`. The
  environment drops `GH_TOKEN`, `GITHUB_TOKEN` and every `OPENREPOSHAPE_*`
  variable. `PATH` is built from a temporary bin directory holding the fakes,
  plus the directories of `bash`, `git` and `sys.executable`, so an
  openRepoShape or setup-openspeckit installed on a developer's machine is
  never found. Each Triad test asserts that
  `shutil.which("openRepoShape", path=env["PATH"])` is the fake; each missing
  test asserts it is `None`. The `--workflow` tests assert that
  `shutil.which("setup-openspeckit", path=env["PATH"])` is the fake, and the
  `--workflow` refusal test without `setup-openspeckit` asserts it is `None`.
- **The fake `openRepoShape`**: an executable script that appends its argv to
  a record file beside itself, prints `Type yes to continue: `, reads one line,
  and on `yes` creates `<--into>/<name>` and exits 0 (or with a status the test
  sets), otherwise prints `not confirmed; nothing was created.` and exits 1.
  Tests assert its argv carries the typed organization, the lower-case
  visibility and `--into`, and never `--yes`; obstacle tests assert the record
  file does not exist.
- **The fake `setup-openspeckit`**: prints a marker line on stdout and on
  stderr, then exits with a status the test sets. The order test runs with
  stderr merged into stdout and asserts that both `warning:` lines precede the
  marker; the failure test asserts the advisory is on stderr and the follow-up's
  status is the exit status.
- **The guarded advisory**: stderr closed (`sh -c 'exec "$@" 2>&-' sh ...`);
  stderr on `/dev/full`, skipped where `/dev/full` does not exist; and stderr
  on a pipe whose read end is closed (`EPIPE`), which runs on macOS as well.
  Each asserts that stdout equals the pinned stdout of a run without the
  advisory, that stdout carries no `warning:`, and that the exit status is 0.
- **Fixtures**: the D13 strings are literals in the test module. No test
  compares against "today's" output by reading history, since CI checks out at
  depth 1.
- **Cases**: those listed in the proposal's Impact, so that every spec
  scenario has at least one test. The existing tests keep passing unchanged:
  `run_cli`'s stdin is a pipe, so none of them is asked the question; those
  that create with `--type` and `--yes` now also receive the advisory on
  stderr, which none of them asserts against.

## Risks / Trade-offs

- [An agent or a script at a pseudo-terminal meets the question, and Enter
  takes the Triad] → No detection (D11). The guarantee rests on openRepoShape's
  typed confirmation and on `Type yes`; `AGENTS.md` and the README tell agents
  to use a choosing flag.
- [Existing scripts that drive `project new` at a pseudo-terminal without a
  choosing flag meet a new prompt between `Project name:` and the plan, and
  `onp NAME` asks once workBenches moves its pin] → That is the interactive
  creation the packet's D2 describes; a choosing flag restores today's path
  exactly, and the README says so.
- [Two offers in one `--workflow` run, and `n` at setup-openspeckit's question
  exits 130 after the repository exists] → Recorded (D8); the workBenches
  follow-up is carried in the handoff issue.
- [Ctrl-C while openRepoShape runs leaves its temporary directory and lets its
  output follow `Cancelled.`] → Existing behaviour, documented (D9); the
  alternative is described for a change of its own.
- [The pinned assembly-root form drifts from openRepoShape's contract] → Both
  forms carry their path and sha. A stricter openRepoShape refuses by itself,
  with its own status passed through; a looser one would see a Triad answer
  refused for a name it would accept, and `--shape` by flag still reaches it.
  Re-pin when `contracts/repository-naming.yaml` changes.
- [The pinned workspace form drifts] → A name newly in the family would get the
  question or the advisory until re-pinned: advice only, nothing blocks.
- [pty tests are flaky across Linux and macOS] → The D14 rules: both
  end-of-output signals, prompts before answers, a per-run timeout, a repeated
  SIGINT, and no controlling terminal.
- [An in-process test cannot see the descriptor write] → D7 falls back to
  `sys.stderr.write()` where stderr has no descriptor; the subprocess tests are
  the authority for the descriptor path.
- [The prompt is invisible to a person who runs `project new 2>/dev/null` at a
  terminal] → The same holds for today's prompts (bpo-1927); the question's
  lines on stdout still show.
- [With stderr closed at start, `main()` prints `REFUSED:` lines to stdout]
  → Existing behaviour of every refusal (`print(file=None)`), on no path this
  change adds to; not this change's to fix.

## Migration Plan

For users there is nothing to migrate: no flag, file or exit status changes
for an existing scripted invocation; stderr gains two lines after a flag-chosen
or non-interactive single-repository creation; and a person at a terminal
without a choosing flag meets one question.

1. Ratification by Brett Heap's word on PR #5.
2. `/speckit.specify` creates the one feature, `specs/002-<slug>/`; it is
   recorded once in `tasks.md` under "Speckit Handoff"; `/opsx:apply` runs only
   then.
3. The realization PR merges with green checks on all four CI jobs and closes
   issue #3.
4. This lane opens exactly one issue on opensoft/workBenches, addressed to lane
   `project-command`, carrying the merge sha, the sha256 of `project` at that
   sha (so that moving `config/openrepoproject-pin.json`, today `a0407904`, is
   mechanical), and the optional "already offered" follow-up (D8). It edits
   nothing that lane's claim holds.
5. A comment on issue #3 carries the merge sha and that issue's link, and says
   that `onp` and `new-project.sh` offer nothing until the pin moves.
   codeXfactory-5 records the 5.6 tick in openxFactory.
6. The change is archived after the merge.

Rollback: revert the realization commit on main. Installed `project` artifacts
follow workBenches' pin, so a revert before the pin moves reaches nobody
downstream; after it, workBenches moves the pin back on its owner's act.

## Open Questions

None changes what gets built. Two are left to the lead:

- Whether the D9 alternative (waiting for the delegate, for `new --shape` and
  `update --component shape` alike) is filed now as an issue on this
  repository, or left recorded here.
- Whether the workBenches handoff issue also notes two observations about
  setup-openspeckit: its writer exits 120 when stderr is a full device (D7),
  and its advisory omits "run by a person deciding for that project" (the
  proposal's Out of Scope).
