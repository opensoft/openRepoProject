Lane: openRepoProject-1

# Research: Triad-first project creation

There were no unknowns: the Technical Context has no NEEDS CLARIFICATION, and
`openspec/changes/prefer-triad-in-project-new/design.md` (D1 to D14) decides
every technical question. The entries below record the decisions an
implementer most needs, each with its source. They cite; the design holds the
detail and governs.

## R1. The advisory is written with `os.write` on stderr's descriptor (D7)

- **Decision**: flush stdout, write nothing when `sys.stderr` is `None`, encode
  the two lines as ASCII and write them with `os.write(sys.stderr.fileno(), ...)`
  in a short-write loop; fall back to `sys.stderr.write()` only when there is no
  descriptor; swallow `OSError`, `ValueError` and `AttributeError`.
- **Rationale**: the five stream probes in `design.md` Context (Python 3.12.3):
  (1) `print(..., file=sys.stderr)` with `2>&-` lands on stdout, because
  `sys.stderr` is `None`; (2) a buffered write with the error swallowed on
  `2>/dev/full` still exits 120 at the interpreter's final flush; (3) `os.write`
  on `2>/dev/full` with the error swallowed exits 0; (4) the same `os.write`
  into a pipe whose read end is closed raises `BrokenPipeError`, swallowed, exit
  0; (5) at a pty, an `input()` prompt arrives on stderr (bpo-1927), which bears
  on the harness (R2) and on why no test pins a prompt's stream (D4).
- **Alternatives considered**: `print(file=sys.stderr)`; setup-openspeckit's
  `emit_advisory_line`; writing after `Created:`; writing to stdout. All
  rejected in D7.

## R2. The pty harness (D14)

- **Decision**: a helper beside `run_cli`: stdin and stdout on one
  `os.openpty()` slave, stderr on its own pipe; `Popen` with
  `start_new_session=True`; a `select` loop draining the master and the stderr
  pipe until the child exits, with `EIO` (Linux) and an empty read (macOS) as
  end of output; each answer written only after its prompt has appeared on
  either stream; SIGINT by `send_signal`, repeated until exit; `\r\n` normalised
  and echoed input ignored; a timeout on every run; no `pty.fork`.
- **Rationale**: it runs headless on both CI runners and never makes the pty
  the runner's controlling terminal (D14); waiting for the prompt on either
  stream follows from probe 5 and N5.
- **Implementation notes** (consequences of D14, not new decisions): the test
  closes its own copy of the slave after `Popen`, or the master never reports
  end of output; with no controlling terminal, a typed Ctrl-C byte raises no
  signal, which is why SIGINT goes through `send_signal`; end of input can be
  the terminal's EOF character (`\x04`) at the start of a line, or `EOFError`
  from a patched `input` in an in-process test.
- **Alternatives considered**: `pty.fork` (forks a threaded runner and makes the
  pty a controlling terminal); `run_cli` alone (stdin is never a terminal).

## R3. The two name forms are copied and pinned, never read at run time (D3, D10)

- **Decision**: `ASSEMBLY_NAME = ^[A-Za-z][A-Za-z0-9]*$` (openRepoShape
  `contracts/repository-naming.yaml:345`, role `assembly`) and
  `WORKSPACE_NAME = ^[a-z0-9]+(?:-[a-z0-9]+)*-wip$` (`:412`, family
  `workspace`), both at `1a9fc537bcce37301c85fc108fabd8a599b02000`, each with
  that path and sha in a comment, applied to the new name with `fullmatch`.
- **Rationale**: `project` is a single-file artifact installed by sha and cannot
  assume an openRepoShape checkout; asking openRepoShape would wait on the
  network (D3). `fullmatch` keeps a trailing newline from satisfying `$`.
  The form predicts only refusals openRepoShape is certain to make; `--shape`
  by flag still reaches openRepoShape's own validator.
- **Alternatives considered**: asking openRepoShape; importing its contract or
  `shape_advisory.py`; refusing such a name before the question (D3).

## R4. `CI` is false when it is unset, empty, `0`, `false` or `no` (D1)

- **Decision**: `CI`, stripped and lower-cased, must be one of `""`, `"0"`,
  `"false"`, `"no"` (unset reads as `""`) for the question to be asked.
- **Rationale**: it is setup-openspeckit's `is_interactive_run()` and
  `CI_FALSE_VALUES` (workBenches `d86ba59`), its decision 1 at `9fbe609c`, so
  the estate's two interactive offers share one rule. Every question and
  advisory test sets `CI` explicitly, since GitHub Actions sets `CI=true` and
  `self.env` copies the environment (D14).
- **Alternatives considered**: reusing `ask()`'s stdin-only test; a flag or
  variable that skips the question (both rejected in D1).

## R5. A choosing flag counts when it is present, even with an empty value (D1)

- **Decision**: `chosen` is true when `--shape` or `--yes` is set, or when any of
  `--org`, `--visibility`, `--family`, `--elected-by`, `--bench`, `--type` or
  `--description` is not `None`. `--dry-run`, `--workflow`, `--into` or the
  positional parent, and `--workbenches` choose nothing.
- **Rationale**: any explicit choosing flag marks a scripted or deliberate
  choice (D1; spec EC-010). The non-choosing flags must not stop a dry run from
  asking (FR-007).
- **Alternatives considered**: truthiness of each value, which would let
  `--type ""` reach the question.

## R6. One decision value, computed once in `new()` (D1, D2)

- **Decision**: `offer = not workspace and not chosen and person_at_terminal()`,
  computed immediately after the existing-destination refusal. The hoisted
  `--workflow` refusal, the obstacle reads, the question and the advisory all
  read `offer`; nothing re-derives terminal state later. `ask()` keeps its
  stdin-only test for today's prompts.
- **Rationale**: one value keeps the question and the advisory mutually
  exclusive by construction, and keeps every invocation that is not asked on
  today's order of refusals (D2).
- **Alternatives considered**: hoisting the `--workflow` check for every
  invocation; a separate Triad path with its own argv (both rejected in D2).
