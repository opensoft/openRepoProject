Lane: openRepoProject-1

# Contract: `project new`

The command-line contract of `project new` after this feature. The exact text
of every new line is fixed in `design.md` D13 and is named here by its D13
label (for example "D13 question prompt"); exit statuses follow D12. Unchanged
behaviour is stated only where this feature meets it.

## Invocation (unchanged; no new flag)

```text
project new [NAME] [PARENT] [--into DIR] [--bench BENCH] [--type TYPE]
            [--description TEXT] [--shape] [--org ORG]
            [--visibility {public,private,internal}] [--family FAMILY]
            [--elected-by WHO] [--workflow] [--workbenches PATH]
            [--yes] [--dry-run]
```

Environment: `CI` is read (new, read only); `PATH` is searched for
`openRepoShape` and `setup-openspeckit`; `PROJECTS_DIR`, `HOME` and
`WORKBENCHES_ROOT` are read as today.

## When the question is asked (FR-006, D1)

| Condition | Required for the question |
| --- | --- |
| stdin and stdout are both terminals | yes |
| `CI` unset, or stripped and lower-cased one of empty, `0`, `false`, `no` | yes |
| none of the nine choosing flags given (a flag with an empty value counts as given) | yes |
| the name is not a workspace name (`^[a-z0-9]+(?:-[a-z0-9]+)*-wip$`) | yes |

| Input that skips the question | What follows |
| --- | --- |
| `--shape`, `--org`, `--visibility`, `--family`, `--elected-by`, `--bench`, `--type`, `--description` or `--yes` | the path the flags choose, with today's prompts and refusals |
| stdin or stdout not a terminal | today's flow; a prompt on a non-terminal stdin refuses as today |
| `CI` set to any other value | today's flow |
| a workspace name | today's flow, and no advisory |

`--dry-run`, `--workflow`, `--into` or the positional parent, and
`--workbenches` do not skip the question.

## Order of an asked run (D2)

1. `Project name:` when NAME is not given (today's prompt).
2. Today's early refusals: the name check, a positional parent with `--into`,
   the family check, an existing destination.
3. `--workflow` without `setup-openspeckit` on PATH: today's refusal, moved
   here for an asked run only.
4. The obstacle reads (no output, no network, no subprocess).
5. The question: its lines on stdout, then its prompt.
6. A Triad answer: the obstacle refusal, or the organization prompt, the
   visibility prompt and the restating line. A single-repository answer:
   nothing.
7. Today's path from the branch on `--shape` onward: the shape checks and the
   openRepoShape command, or the generator selection; `Create:` and the plan;
   the dry-run end; `Type yes` (bench branch); the delegate; `.project.json`
   (bench branch); the follow-up; `Created:` and `Next:`.

A run that is not asked keeps today's order exactly; on the bench branch, unless the name is a workspace name, the creation advisory comes after `.project.json` and before the follow-up.

## Prompts

Every prompt goes through `ask()`, which appends one space. The stream a prompt
appears on is not part of the contract (D4, N5) and no test asserts it.

### The question (new)

| Aspect | Contract |
| --- | --- |
| Lines before the prompt (stdout) | D13 question: header, entry 1, one obstacle line per holding obstacle (order: name, openRepoShape, parent), entry 2 |
| Prompt | D13 question prompt |
| Takes the Triad | Enter, `1`, `y`, `yes` (case-insensitive, surrounding whitespace ignored) |
| Takes a single repository | `2`, `n`, `no` (same rules) |
| First unrecognised answer | D13 question retry line on stdout, then asked once more |
| Second unrecognised answer | `REFUSED: ` + D13 question second-miss refusal, exit 2 |
| End of input | `REFUSED: ` + D13 question end-of-input refusal, exit 2 |
| Interrupt | `Cancelled.`, exit 130 |
| Triad answer with an obstacle | `REFUSED: ` + D13 known-obstacles refusal, exit 2, before any other prompt, dry run included |

### Organization (new; after a Triad answer with no obstacle)

| Aspect | Contract |
| --- | --- |
| Prompt | D13 organization prompt |
| Accepted | full match of `[A-Za-z0-9][A-Za-z0-9-]*`; passed to openRepoShape as typed (stripped) |
| First empty or failing answer | D13 organization retry line on stdout, then asked once more |
| Second empty or failing answer | `REFUSED: ` + D13 organization second-miss refusal, exit 2 |
| End of input | `REFUSED: ` + D13 organization end-of-input refusal, exit 2 |
| Interrupt | `Cancelled.`, exit 130 |

### Visibility (new; after an accepted organization)

| Aspect | Contract |
| --- | --- |
| Prompt | D13 visibility prompt |
| Accepted | `private`, `public` or `internal`, case-insensitive, stripped; passed lower-cased; no numbers, no default |
| First empty or other answer | D13 visibility retry line on stdout, then asked once more |
| Second empty or other answer | `REFUSED: ` + D13 visibility second-miss refusal, exit 2 |
| End of input | `REFUSED: ` + D13 visibility end-of-input refusal, exit 2 |
| Interrupt | `Cancelled.`, exit 130 |
| After acceptance | D13 restating line on stdout (the `public` form for `public`), before `Create:`, dry run included |

### Today's prompts (unchanged)

| Prompt | End of input or interrupt | Other answers |
| --- | --- | --- |
| `Project name:` | `Cancelled.`, 130 | an invalid name refuses, 2 |
| `Select a generator number (or specify --bench and --type):` | `Cancelled.`, 130 | not a listed number: `Invalid generator selection.`, 2 |
| `Type yes to run this plan:` | `Cancelled.`, 130 | anything but `yes`: `Cancelled; no command was run.`, 2 |
| openRepoShape's typed confirmation | end of input: openRepoShape's own status, passed through; interrupt: `Cancelled.`, 130 (D9) | openRepoShape's own; its status passes through |

On a non-terminal stdin, each of today's prompts refuses with exit 2, as today.

## Streams

| Output | Stream |
| --- | --- |
| question lines, retry lines, restating line | stdout |
| `Create:`, the plan, the generator list, `Created:`, `Next:` | stdout (today) |
| `REFUSED: ...`, `Cancelled.` | stderr (today's `main()`) |
| the creation advisory, two `warning:` lines (D13) | stderr only, through the guarded write (D7); never stdout |
| `Project created at ...; workflow setup failed.` | stderr (today) |
| prompts | not part of the contract |
| openRepoShape, generator and follow-up output | their inherited streams |

## The creation advisory (FR-017 to FR-020, D7)

Given once, after `.project.json` exists and before any follow-up, when a
single repository was created on the bench branch, the question was not asked,
and the name is not a workspace name. Never given for a dry run, a Triad
creation, a creation that went through the question, a workspace name, a
failing generator, or a generator that did not create the destination. A write
failure (closed stderr, broken pipe, full device) is ignored and changes
nothing; stdout, files, `.project.json` and the exit status are as without it.

## Under `--workflow` (FR-022, D8)

`project`'s offer comes first (the question before creation, or the advisory
after a covered creation), then `setup-openspeckit --repo DESTINATION` runs with
today's arguments and its output follows unchanged. `project` neither
suppresses nor coordinates with it. A failing follow-up keeps today's report
and status.

## Exit statuses (D12)

| Status | When |
| --- | --- |
| 0 | created, or a dry run printed its plan |
| 2 | every refusal this feature adds (question, obstacles, organization, visibility); today's refusals, including the `--workflow` refusal where it is hoisted; an argument error |
| 130 | an interrupt at any prompt; end of input at `Project name:`, the generator number or `Type yes`; an interrupt while openRepoShape runs (D9) |
| the delegate's own | openRepoShape exits nonzero (no particular status promised); the generator exits nonzero; the follow-up exits nonzero |
