Lane: openRepoProject-1

# Data Model: Triad-first project creation

Nothing is stored: these are the values one `project new` run reads and
derives. Exact text is in `design.md` D13; statuses are D12's.

## Entities

### Triad

openRepoShape's three-repository shape (assembly root, spec leg, code leg);
preferred, not required; elective; confers nothing.

| Field | Source | Validation |
| --- | --- | --- |
| name | argument or `Project name:` | today's name check, then `ASSEMBLY_NAME` (D3) on the question path |
| organization | `--org`, or the organization prompt | `[A-Za-z0-9][A-Za-z0-9-]*`, full match (today's check); passed as typed, stripped |
| visibility | `--visibility`, or the visibility prompt | `private`, `public` or `internal`, compared lower-cased; passed lower-cased (D5) |
| parent | `--into`, positional parent, or `PROJECTS_DIR` / `~/projects` | must be an existing directory |
| destination | `parent / name` (a Triad answer never carries `--family`) | must not exist (today's refusal) |

Created only by openRepoShape, after its own typed confirmation, from today's
argv without `--yes` (D2). No advisory follows a Triad creation.

### Creation question

| Field | Value |
| --- | --- |
| asked | exactly when `offer` is true (D1) |
| entries | 1 Triad (default), 2 single repository, with 0 to 3 obstacle lines under entry 1 (D13) |
| answer | `triad` for Enter, `1`, `y`, `yes`; `single` for `2`, `n`, `no`; stripped, compared lower-cased (D4) |
| retries | one; the retry line is printed before the second asking |

Validation: a second unrecognised answer or end of input raises `Refused`
(exit 2); an interrupt is not caught (exit 130). It creates nothing and writes
no `single-repository.yaml`.

### Choosing flag

The nine flags `--shape`, `--org`, `--visibility`, `--family`, `--elected-by`,
`--bench`, `--type`, `--description`, `--yes`. Given when the switch is set or
the valued option is not `None`, even when empty (D1). `--dry-run`,
`--workflow`, `--into`, the positional parent and `--workbenches` are not
choosing flags.

### Known obstacle

| Kind (in this order) | Read | Obstacle when |
| --- | --- | --- |
| name | `ASSEMBLY_NAME.fullmatch(name)` | no match |
| openRepoShape | `shutil.which("openRepoShape")` | `None` |
| parent | `parent.is_dir()` for the resolved parent | false |

Read only when `offer` is true, with no network and no subprocess (D3). Each
holding obstacle adds one line under entry 1; a Triad answer with any obstacle
is refused (exit 2) before any further prompt; a single-repository answer is
unaffected.

### Creation advisory

| Field | Value |
| --- | --- |
| lines | two, each `warning: ` + D13 text, ASCII, with NAME substituted |
| stream | stderr only, through the guarded descriptor write (D7) |
| given when | the bench branch ran (`row`), the destination is a directory and `.project.json` exists, not a dry run, `not offer` and `not workspace` |
| placement | after `.project.json`, before the first follow-up (D7, D8) |

A failed write is ignored; it changes no exit status and records nothing.

### Workspace name

A name for which `WORKSPACE_NAME.fullmatch(name)` holds (D10), such as
`alice-wip`. It sets `workspace`, so the question is not asked and no advisory
is given; the creation otherwise runs as today.

### The one decision (D1)

Computed once in `new()`, right after the existing-destination refusal:
`workspace`, `chosen`, and `offer = not workspace and not chosen and
person_at_terminal()`, where `person_at_terminal()` is true only when the `CI`
rule holds and `sys.stdin` and `sys.stdout` are both terminals.

## States of a `project new` run

| State | Meaning |
| --- | --- |
| not asked | the name is known, the early refusals passed, `offer` is false |
| asked | `offer` is true and the question is on screen |
| Triad answer | the question took the Triad |
| single answer | the question took the single repository |
| refused | the run ended nonzero and `project` reports no creation, `Cancelled.` included (statuses below) |
| created | the destination exists (and, on the bench branch, `.project.json`) |

A dry run ends after the plan with status 0 and nothing written; it is neither
refused nor created.

### Transitions

| From | Event | To |
| --- | --- | --- |
| (start) | end of input or interrupt at `Project name:` | refused (130) |
| (start) | invalid name, positional parent with `--into`, existing destination | refused |
| (start) | early checks pass, `offer` false | not asked |
| (start) | early checks pass, `offer` true, `--workflow` without `setup-openspeckit` | refused |
| (start) | early checks pass, `offer` true | asked (after the obstacle reads) |
| asked | Enter, `1`, `y`, `yes` | Triad answer |
| asked | `2`, `n`, `no` | single answer |
| asked | unrecognised once | asked (retry line) |
| asked | unrecognised twice, end of input, or interrupt | refused |
| Triad answer | any known obstacle | refused |
| Triad answer | organization or visibility missed twice, end of input, or interrupt | refused |
| Triad answer | both accepted, restating line printed, openRepoShape confirmed and exits 0 | created (no advisory) |
| Triad answer | openRepoShape exits nonzero (refusal or declined confirmation) | refused |
| single answer | today's bench branch completes | created (no advisory) |
| single answer | today's bench refusals, `yes` declined, generator fails | refused |
| not asked | today's flow completes on the bench branch | created, then the advisory unless `workspace` |
| not asked | today's flow completes on the `--shape` branch | created (no advisory) |
| not asked | today's refusals or a failing delegate | refused |
| created | `--workflow` follow-up exits nonzero | created; exits with the follow-up's status after "Project created at ...; workflow setup failed." (any advisory already given) |

### Nonzero exit statuses

| End | Status |
| --- | --- |
| a refusal this feature adds (question, obstacles, organization, visibility), or today's `--workflow` refusal hoisted before the question | 2 |
| today's refusals, including `Type yes` declined and a generator that did not create the destination | 2 |
| an interrupt at any prompt; end of input at `Project name:`, the generator number or `Type yes` | 130 (`Cancelled.`) |
| openRepoShape exits nonzero | its own, passed through; no particular status promised |
| the generator exits nonzero | its own |
| the follow-up exits nonzero (the project exists) | its own |
| an interrupt while openRepoShape runs | 130 (`Cancelled.`, D9) |
