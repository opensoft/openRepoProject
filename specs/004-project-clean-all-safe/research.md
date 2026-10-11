Lane: openRepoProject-2

# Research: Safe batch worktree cleanup

The Technical Context in [plan.md](plan.md) has no NEEDS CLARIFICATION. The
ratified change (`openspec/changes/add-project-clean-all-safe/`: proposal,
design D1 to D20, the three spec deltas) decides almost every technical
question, and it governs. These entries settle what it leaves to the
implementation:

- R1 to R6: six places where the code at `961c405` contradicts the change's
  text, each resolved inside that text (the push-child exception, LQ-3 in
  R1, waits on Brett Heap's word);
- R7: the reviewed spec the plan cites;
- R8 to R15: the unknowns of counting, ordering, timing and the test
  harness, test runtime and CI, the digest's bytes, the bare-name test,
  termination and reaping, and the existing tests.

The plan review of `dd923ee` and the lead's rulings R-29 to R-31, from the
harness spike at `aadd709`, are applied in place.

Each entry gives a Decision, its Rationale and the Alternatives considered;
R1 to R6 also name the scenarios they satisfy (delta scenario titles in
quotes, spec ids beside them) and what they cost. Line citations are
`project:<line>` and `tests/test_project.py:<line>` at `961c405`, unchanged on
this branch (plan.md, "Citations"). The checks quoted below were run on Git
2.43.0 and Python 3.12.3 with their fixtures and scripts in a scratch
directory, never in the repository.

## R1. The push-child exception (LQ-3, awaiting Brett Heap's word)

- **Finding**: the `project-command` delta says that "Every Git child, of
  every kind, SHALL also pass `-c protocol.allow=never`" and the six
  per-protocol pins (design D11), and that every Git child runs in its own
  process group, while the requirement the change keeps, "Clean can
  explicitly push safe feature branches", keeps the push child
  `git -C <root> push ...` (`project:699`, `:703`), run by `execute()`
  (`:743`). Checked against a local bare remote: the push with the seven
  pins ends `fatal: transport 'file' not allowed`, exit 128; without them,
  exit 0; `git branch -d` and `git --version` with the pins both exit 0. The
  two sentences cannot both hold, and the existing tests
  `test_clean_pushes_explicit_clean_feature_branch_without_force` (`:899`)
  and `test_clean_pushes_to_a_differently_named_upstream_branch` (`:978`)
  push to a local-path origin.
- **Decision** (a plan assumption, awaiting Brett Heap's word): the
  amendment that PR #19 (draft, after its review fixes; branch
  `change/amend-clean-all-safe-push-pins`) carries for his word as option
  (a). The push child of `clean --action push` runs through `execute()`, not
  through D2's driver: its standard input, output and error are `project`'s
  own, never read or capped; it runs in `project`'s process group, so it is
  in the terminal's foreground when `project` is; `project` never signals it
  and waits for it to exit; it is unbounded, with no `min(5 s, remaining)`
  budget and no 64 s deadline; it carries none of the seven protocol pins;
  and it yields no evidence. Under the lead's ruling R-28 it keeps the
  caller's `GIT_ALLOW_PROTOCOL`, while the other sixteen scrubbed names are
  removed from it, so it acts on the repository the run inspected. Every
  other Git child keeps the seventeen-name scrub, the pins and its own
  process group: `git --version`, every identity, registry, ref,
  merged-set, status, hidden-state and `remote get-url` child, every
  revalidation and rescan child, the removal child and the delete-branch
  child (R5). The push child is the only Git child of `project` that reaches
  a remote: `update` runs no Git network child, and `handoff()` only reads
  `git remote get-url origin` (`:779`).
- **Rationale**: the pins keep a read-only probe from fetching (R-23, R-25 in
  the proposal's later rulings); a push must reach its remote, and the kept
  requirement, its scenario and the two existing tests require it to. In the
  terminal's foreground the push can still ask for a credential or a
  passphrase, as it does today.
- **Independence**: no other decision here depends on it. The pins and the
  session are applied by one argument-vector builder and one spawn helper,
  and the push child is built in one place (R5). If Brett Heap rules a
  follow-up change instead (option (b)), only the push child's treatment
  moves: that builder, that helper and the push tests.
- **Scenarios**: "Push an unpushed feature branch" (US3 scenario 6), "Push
  refuses a branch whose upstream was deleted" (US3-7), "Push refuses an
  incomplete inspection" (US3-8), "A lazy fetch in a partial clone is refused
  locally" (US9-9); FR-010, FR-054; SC-003, whose counting wrapper runs over
  inspection and removal runs, where every child carries the pins, while the
  push tests assert that the push child carries none. PR #19's scenario "The
  push child reaches its remote" joins them, tested whether or not PR #19
  has landed, with its case of a pre-push hook that sleeps 7 s: the push
  still exits 0, `origin` holds the branch, and no signal reaches the push
  child. The counting wrapper records the push child's process group equal
  to `project`'s and every other child's its own (R10). A push test that
  needs the terminal runs `project` under a pty made its controlling
  terminal (R10, R-31): the harness spike found that without it even a
  same-group push child gets `ENXIO` on `/dev/tty`, while with it the child
  opens `/dev/tty`, Git's prompts are answered there, the terminal's
  foreground group is the push child's, and a `^C` typed at the prompt
  stops the push, nothing pushed, `project` exiting 130.
- **Cost**: until the word, the plan departs from the delta's literal text
  for one child.
- **Alternatives considered**: (a) amend the unarchived change in place by
  its own pull request on his word, with a scenario for the push child (PR
  #19, the lead's recommendation); (b) a follow-up change after this one
  archives, as lane openRepoProject-1 did with `fix-parent-obstacle-wording`;
  (c) the literal reading, rejected because every push would then fail with
  exit 128, breaking a requirement the change keeps.

## R2. `discover()` without a usable Git

- **Finding**: `discover()` needs Git to find a plain repository's root:
  `root = git_text(path, "rev-parse", "--show-toplevel")`, then
  `raise Refused(f"No project found at {path}; supply a path or name.")`
  (`project:462-467`). Checked with no `git` on PATH: `status`, `doctor` and
  `clean` on a plain repository each print `REFUSED: No project found at ...`
  and exit 2. "No git on PATH" (doctor's `git-unavailable` row, exit 1) and
  "Git older than 2.36 in status and doctor" (status exit 0, doctor exit 1)
  cannot reach their exits, and a real Git 2.35 would run that child, which
  FR-053 forbids ("inspecting no repository with a Git older than 2.36").
- **Decision**: `clean` runs `git --version` (D6 row 1) before resolving its
  argument, so it refuses with `git-too-old` or `git-unavailable` before
  `discover()` is reached (FR-002); nothing more is needed there. For
  `status`, `doctor` and `update`, `discover()` keeps its family-holder and
  manifest-ancestor steps, which need no Git. Where it reaches its Git step,
  it first runs the memoized version check. With a usable Git (2.36 or
  later), `rev-parse --show-toplevel` runs through the driver: scrubbed,
  pinned, 15 s, counted. With an old, missing or unusable Git, no Git child
  runs: the root is the nearest of the path and its ancestors holding a
  `.git` entry (an `lstat`, not followed), and then today's `.project.json`
  and `.devcontainer` fallback applies. `repo_state()` reports that root with
  `classification: "inspection-error"` and `git-too-old` or
  `git-unavailable` (D16); a directory with no `.git` keeps `present: false`
  and runs no version check.
- **Scenarios**: "Git older than 2.36 in status and doctor" and "No git on
  PATH" (US9 scenario 2), "Tools and workflow need no Git" (US9-2, last
  clause), "Git older than 2.36" (US9-1, through `clean`'s order); FR-002,
  FR-050, FR-053; SC-013.
- **Cost**: a second way to find a root, used only when Git cannot be. It can
  name a different directory from Git's own answer only where Git would
  resolve differently or refuse (`GIT_CEILING_DIRECTORIES`, a
  `safe.directory` refusal, a `.git` that is not a repository); the
  directory it names is reported as `inspection-error` and never inspected,
  so no reported value is wrong.
- **Alternatives considered**: fixtures that carry a manifest or
  `.project.json`, rejected because a plain repository would still refuse
  with exit 2 for a missing Git, against FR-050 and SC-013; the `.git` walk
  always, rejected because it changes `discover()`'s answer while Git works
  (FR-061); the version check at the top of `discover()`, rejected because a
  manifest project would then run a Git child it does not need (D16).

## R3. The removal question writes its own prompt

- **Finding**: `ask()` ends `return input(prompt + " ").strip()`
  (`project:149`). Checked: with standard input on a pseudo-terminal and
  standard output on a pipe, `input("QUESTION? ")` writes its prompt to
  standard output (the captured stdout was `QUESTION? ANSWER=yes`). Under
  `--apply --json | jq` at a terminal the question would land in the one
  JSON document that standard output is reserved for.
- **Decision**: the removal question (FR-026, D18) is its own function, not
  `ask()`. It writes the question line to the human stream (standard error
  under `--json`, standard output otherwise), flushes it, then reads one line
  with `input()` given no prompt. The noninteractive case is refused before
  it as `confirmation-required` (FR-015), never by `ask()`'s own refusal.
  Only `yes`, stripped, accepts; any other answer refuses with `cancelled`,
  exit 2; end of input raises `EOFError`, which `main()` turns into
  `Cancelled.` and 130 with no JSON document. `ask()` and `confirm()` stay as
  they are for `new`, `update`, push and delete-branch.
- **Scenarios**: "Apply with JSON prints one document" (US8-3), "Only yes
  confirms" (US1-2), "A noninteractive batch needs --yes" (US1-8), "A signal
  during a removal" (US5-1, end of input at the question); FR-015, FR-026,
  FR-044.
- **Cost**: the prompt's stream is fixed rather than CPython's choice; at a
  terminal, readline editing still works, though a redraw does not repeat
  the prompt text.
- **Alternatives considered**: `ask()` unchanged, rejected (stdout under
  `--json`); swapping `sys.stdout` around `input()`, rejected as global state
  a signal can interrupt; `sys.stdin.readline()`, rejected because it loses
  line editing and `EOFError`.

## R4. Signal handlers: `clean`'s whole run, the other subcommands' inspection

- **Finding**: D1 installs handlers that only record SIGINT, SIGTERM and
  SIGHUP, and says that "`status`, `doctor` and `update` install the same
  handlers"; `update` then calls `confirm(args.yes)` (`project:1066`) and
  runs delegates through `execute()` (`:1059-1070`), and push and
  delete-branch also call `confirm()` (`:737`). Checked: with a record-only
  SIGINT handler installed, `input()` at a pseudo-terminal was still alive
  after SIGINT and then accepted `yes`, so Ctrl-C at `Type yes to run this
  plan:` would do nothing, while the design's Non-Goals keep `confirm()` as
  those callers use it.
- **Decision**: for `clean`, D1's record-only handlers and the wakeup
  descriptor are installed from the argument checks to the last write,
  except at the removal question (raising handlers) and at `confirm()` for
  push and delete-branch (the process's own handlers). The slot is read
  after planning, before the question and before the apply phase begins; a
  signal recorded before the apply phase ends the run by FR-036 (probe
  groups reaped, `Cancelled.`, 130, 143 or 129, no document written). One
  recorded while a preview or report is being written is read once more
  before the run exits, which then exits 130, 143 or 129 with `Cancelled.`.
  `status`, `doctor` and `update` install them around their inspection, so
  SIGTERM and SIGHUP there unwind through the same cleanup and exit 143 and
  129. One context manager makes each swap. The removal question's raising
  handlers last for its own duration (SIGINT raises `KeyboardInterrupt`;
  SIGTERM and SIGHUP raise a private exception that `main()` maps to 143 and
  129), as D1 and D15 say. Before `confirm()` (`new`, `update`, push,
  delete-branch) and before `update`'s owner-tool delegates, the handlers
  the process started with are restored, so those prompts and delegates
  behave as they do today. The push and delete-branch children are the
  exception (R1, R5): the record-only handlers stay installed while either
  runs, `project` never signals it and waits for it, and a Ctrl-C at the
  terminal reaches the push itself, which is in the foreground. The run then
  exits by D19's first row: 130, 143 or 129 when a signal was recorded,
  otherwise the child's own status (data-model.md, "Exit statuses"). The
  delete-branch child runs through the driver like any child, with no
  budget, and a set slot does not stop it (R5).
- **Scenarios**: "SIGTERM before the apply phase" (US5-2), "A signal during a
  removal" (US5-1, SIGINT at the question exits 130); FR-036, FR-058, FR-064
  (every confirmation other than FR-026's unchanged).
- **Cost**: a swap at each boundary; SIGTERM at `update`'s `Type yes` ends
  the process with the default action, as today, rather than 143 (no probe
  child runs there: inspection's `finally` has reaped them). Today
  `subprocess.run()` kills a delegate soon after a Ctrl-C reaches `project`
  (checked: given SIGINT, a parent in `subprocess.run()` exited 0.26 s later,
  and its child, which ignored SIGINT, never finished its work); for the push
  child that kill no longer happens, as R1 requires.
- **Alternatives considered**: record-only handlers at `confirm()` too,
  rejected (Ctrl-C there ignored); handlers around inspection and the apply
  phase only, rejected by the plan review (SIGTERM or SIGHUP while the plan
  prints, the digest is checked or a preview is written would take the
  default action, and a signal recorded after the last probe would go
  unread until the apply phase); default handlers throughout, rejected
  (SIGTERM would kill `project` with probe groups running, exit -15, not
  143).

## R5. Every Git child outside D6's table goes through the runner

- **Finding**: these Git children sit outside D6's table and D9: `handoff()`'s
  and push's `remote get-url origin` (`project:779`, `:701`); `update()`'s
  `symbolic-ref --short refs/remotes/origin/HEAD` (`:1010`); delete-branch's
  `rev-parse --verify` (`:659`, `:731`, `:733`); `ancestor()`'s
  `merge-base --is-ancestor` (`:540`, called at `:563`, `:661`, `:731`); and
  two delegates, the push (`:699`, `:703`) and `branch -d` (`:734`). All run
  through `probe()` or `execute()` with the caller's environment, in
  `project`'s own process group, uncounted.
- **Decision**:
  - Inspection-like children run as D2 handles of kind `probe` through
    `run_bounded()`: scrubbed, pinned, in their own group, with their
    subcommand's budget, counted in `probes`. Where the evidence pipeline
    already holds the value, it is read instead: `origin/HEAD`'s target from
    row 6's symref (update), a branch's head from row 6 (delete-branch), and
    merged-ness from row 7's merged set, which covers every local branch.
    `remote get-url origin` stays a child, since no row reads a remote URL.
    `ancestor()` and `default_branch()` retire, and `git()` and `git_text()`
    (`:68-74`) keep their names and place but call the runner, so no Git
    child bypasses it.
  - The two delegates stay unbounded (D-W: "Push and delete-branch children
    SHALL stay unbounded, as before this change") and keep today's exit mapping
    (128 plus the signal number) unless a signal was recorded meanwhile, when
    the run exits 130, 143 or 129 (R4). The delete-branch child `git branch -d`
    becomes a D2 handle run by the driver: its own process group, the
    seventeen-name scrub and the seven pins, with no budget and never signalled
    (R4), its output relayed to `project`'s own streams. The push child stays
    on `execute()` as R1 describes: `project`'s process group and streams,
    sixteen names scrubbed (`GIT_ALLOW_PROTOCOL` kept, R-28), no pin, never
    signalled. `execute()` gains only an optional environment argument, and is
    unchanged for non-Git delegates.
- **Scenarios**: "Bounded revalidation work" (US6-6, `probes.performed` equal
  to the wrapper's count of children other than removals, R8), "A caller's Git
  environment is ignored" and "A lazy fetch in a partial clone is refused
  locally" (US9-8, US9-9), "Push refuses an incomplete inspection" (US3-8);
  FR-033, FR-054, FR-061; SC-003, SC-006.
- **Cost**: a child in its own session has no controlling terminal. Checked
  from a pseudo-terminal session: a child started with
  `start_new_session=True` failed `cannot create /dev/tty: No such device or
  address`, where the same child in the caller's session wrote to it. The
  harness spike refined that check: the same-session child opens
  `/dev/tty` only when the pty is the caller's controlling terminal, and
  gets `ENXIO` otherwise, so the push-child tests make it so (R10, R-31).
  No child given its own session needs the terminal: `git branch -d` asks
  nothing, and the push, which may ask for a credential or a passphrase,
  keeps the caller's terminal (R1).
- **Alternatives considered**: leaving these children on `probe()` and
  `execute()`, rejected (unscrubbed, unpinned, uncounted: FR-054, SC-003);
  routing the push through the driver, rejected (PR #19: its streams and the
  terminal stay the caller's, and nothing may signal it); giving
  `git branch -d` a 5 s budget, rejected (D-W keeps it unbounded).

## R6. `internal-error` inside `clean`

- **Finding**: `main()` catches only `(Refused, OSError)` (`project:1143`).
  Checked: a `RuntimeError` injected into `cleanup_report()` ended
  `project clean` with a traceback and exit 1, where the delta wants
  `internal-error` and exit 2 before the apply phase; and a default SIGTERM
  ends a child with return code -15, not 143.
- **Decision**: `clean()` runs inside a guard. The guard passes `Refused`,
  D1's `Interrupted`, the question's signal exception, `KeyboardInterrupt`
  and `EOFError` through unchanged, so they keep their 2, 130, 143 and 129
  paths. Before the apply phase, any other `Exception` becomes the refusal
  `internal-error`, exit 2, printed as the extended error object under
  `--json` and as `REFUSED: ` with the exception's type and text otherwise.
  After the apply phase begins, any other exception, in a target, its
  rescan, the final rescan or the record's rendering, first waits for an
  in-flight removal (D1), then makes the target being handled `unknown`
  with `internal-error` (fields not established null) and later targets
  `not-attempted`; the record is printed and the run exits by D19 (1, or
  the signal status). The guard is `clean`'s only: no requirement gives
  `status`, `doctor` or `update` an `internal-error` code, and their
  handling stays as it is.
- **Scenarios**: "Exception after the apply phase begins" (US5-7), "SIGTERM
  before the apply phase" (US5-2, 143 rather than -15); FR-036, FR-037.
- **Cost**: a broad catch can present a programming error as a refusal; the
  message names the exception, and fault-injection tests pin both sides.
- **Alternatives considered**: widening `main()`'s catch for every
  subcommand, rejected (changes `new` and the others, against FR-064);
  leaving it, rejected (exit 1 with a traceback is not a refusal).

## R7. The plan cites the reviewed spec

- **Decision**: the plan cites `spec.md` at `aadd709`, where the spec
  review's fixes brought SC-002, SC-004, SC-005, SC-006, SC-008, SC-013,
  FR-022, FR-034, FR-066, FR-067, US1 scenario 1, US2 scenarios 5 to 7, US4
  scenarios 1 and 3 and US6 scenarios 5 to 7 into line with the change; no FR
  or SC id moved. Where a spec sentence is still shorter than the deltas, the
  deltas govern (spec, "Source of truth"). Two of those fixes shape the
  tests: US2 scenario 6 gives the reset branch commits of its own and each
  fetched, `update-ref` or `push .` branch an upstream set by
  `git branch -u`, so the row reaches the reflog gate; and US4 scenario 3
  places the second upstream's reappearance after the first removal child
  exits 0 and before the rescan that follows it.
- **Rationale**: a test built to a misstated criterion would fail a delta
  scenario, and SC-012 requires every delta scenario to pass.
- **Alternatives considered**: planning against the change alone and
  leaving the spec's misstatements standing, rejected once the fixes landed.

## R8. What `probes` and `operations` count (lead ruling R-27)

- **Decision** (ruled by the lead as R-27): `probes` counts every Git child
  other than a removal child: the version check, a bare name's lookup, the
  identity, registry, `core.worktree`, ref and merged-set children, status and
  hidden-state probes, `remote get-url`, and every revalidation and rescan
  child. `operations` counts removal children. `estimated` is the packet's
  upper bound for an `--apply` run of this plan (`BA:816-830` at `da33d92`,
  where `BA` is `ideation/brainstorm/project-maintenance-batch-cleanup.md` at
  `da33d92`, as the change's `proposal.md:25` keys it), in every mode, previews
  included: `probes` is F + W + E + 5T + 3, F the repository-wide children this
  invocation ran (rows 1 to 7, with 2, 4b, 5 or a row 3 repeat when they ran),
  W the status probes, E the hidden-state probes, T the selected targets;
  `operations` is T. `performed` counts the children actually spawned. Tests
  compare `probes.performed` with the counting wrapper's count of children
  other than `worktree remove`, and `operations.performed` with its count of
  `worktree remove`.
- **Rationale**: each Git child is counted once across the two, which is what
  the delta's "every Git child counted" means; the proposal adopts this
  accounting by citing the packet (`BA:816-830` at `da33d92`), whose own
  preview fixture reports `"probes": {"estimated": 17, ...}` and
  `"operations": {"estimated": 1, "performed": 0}` (`BA:1070-1071`), the apply
  bound in a preview. The delta scenario "Bounded revalidation work" says that
  `probes.performed` "equals the wrapper's count", which read literally
  includes the removals; PR #19 clarifies that wording before the archive, and
  US6 scenario 6 and SC-006 of the reviewed spec already read it this way.
- **Alternatives considered**: counting removals in `probes` too, rejected
  (then `operations` would duplicate a subset of `probes`); adding 5T + 3
  and T only for an apply, rejected by the plan review (a preview's
  estimates would then differ from the packet's fixture).

## R9. Switching the evidence model: `cleanup_report()` first

- **Decision**: `cleanup_report()` moves onto the evidence pipeline first
  (plan slice 3), while `repo_state()`, which both `cleanup_report()`
  (`project:545`) and `snapshot()` (`:829`, `:847`) call, keeps today's
  reader until slice 7. Parity is asserted as literal expected values written
  into the new tests, per fixture row (classification, `dirty`, `upstream`,
  `ahead`, `behind`, `merged_into_target`, `remote_present`, `current`),
  because once a reader is switched no baseline function remains to compare
  against, and the test module pins kept text as literals and reads no
  history. Slice 7 switches `repo_state()` for `status`, `doctor` and
  `update` with D16's changes, its own parity literals, and the existing
  `status`, `doctor` and `update` tests (`tests/test_project.py:586-801`) as
  the guard.
- **Rationale**: switching `repo_state()` switches four subcommands at once;
  one reader at a time keeps every slice's suite green and confines a parity
  failure to the reader just switched.
- **Alternatives considered**: `repo_state()` first, rejected (`status`,
  `doctor` and `update` would move with a half-built pipeline); parity by
  calling the old function from tests, rejected (it keeps two readers, against
  FR-053 and D6); golden JSON files, rejected (paths, SHAs and `observed_at`
  differ per run, while literals over the stable fields suffice).

## R10. Time-bound tests and the harness (lead rulings R-26, R-29, R-31)

- **Decision** (ruled by the lead as R-26 and R-29, recorded here as decided):
  every timing constant of `project` lives in one module-level table, `TIMING`:
  the 60 s invocation deadline, the 10 s reserve, the 5 s probe budget, the 5 s
  removal floor, the 300 s removal ceiling, the 15 s budget of `status`,
  `doctor` and `update`, the 2 s TERM-to-KILL grace, the 2 s reap wait and the
  100 ms selector tick. Tests replace that table through a launcher under
  `tests/` (`tests/launch_project.py`, a name unittest discovery does not
  import) that loads `project` as a module, as the test module does, registers
  it in `sys.modules`, replaces entries of `TIMING` from a leading
  `--timing=JSON` argument (an unknown key is an error), sets `sys.argv` and
  `sys.path[0]` as `python3 project` would, and calls `main()` in its own
  process, so signals and process groups behave as in a real run; tests in
  which no child matters call `main()` in process. No single factor serves
  every test (R-29): each time-bound test names its own factor or table for
  what it asserts. Ceiling and deadline tests use a factor of about 0.03 to
  0.05 with real Git children and no Python wrapper, or a table that shortens
  only what they assert; counting tests use the `sh` counting wrapper (about 14
  ms a call) or the real table. `budget` and `limits` report the values in
  force, so under the launcher the JSON shows the replaced values and a test
  asserts them as such. Timing tests assert ratios and ordering (which child
  was cut, which stage was omitted), never raw wall-clock values; the
  SIGTERM-to-SIGKILL gap, measured from the child, is asserted at 0.9 of the
  grace in force or more. No environment variable, flag or file read by
  `project` scales time. No timing value is bound at import or definition time,
  and none is a parameter: under R-30 `terminate_group()` reads the grace from
  `TIMING` when it is called and `advance()` the reap wait when it sends
  SIGKILL (D2's `grace=2.0` is the table's value, not a default argument), and
  no constant is derived from the table at import, so the launcher's
  replacement reaches every call (R14). Each time-bound test names its factor
  or table in its body and records the probe budget it yields (plan review U1);
  R-29's factors replace U1's proposal that a probe budget under 1 s run only
  fake Gits, and macOS headroom stays a risk (plan.md).
- **Harness rules** (the harness spike at `aadd709`; R-29, R-31):
  - The test module's loader (`tests/test_project.py:23-26`) registers
    `sys.modules[name]` before it executes `project`, as the launcher does:
    without it a `@dataclass` under `from __future__ import annotations`
    fails to load.
  - The counting wrapper is the POSIX `sh` script of plan slice 1, never a
    Python script: under load a Python wrapper cost about 100 ms a call
    against 14 ms, timed out probes the `sh` wrapper did not, and stretched
    a push scenario to 13 to 18 s. It writes one record per child (pid,
    parent pid, process group, working directory, the scrubbed names set,
    the arguments) before it `exec`s Git. The spike proved those fields with
    its Python wrapper, which records them the same way: for `status`,
    `doctor` and `clean`, every child's parent was `project` and each child
    had a process group of its own, and `GIT_DIR` and
    `GIT_CONFIG_PARAMETERS` showed removed at the one scrubbed call site and
    present elsewhere; its `sh` wrapper records the same argument vectors,
    directories and scrub names, and was timed. A test reads only
    complete records; fixture setup calls the real `git` by absolute path,
    or resets the log before the CLI run; and a `doctor` test under the
    wrapper expects the wrapper's path in doctor's `git` row.
  - A fake `git` matches its subcommand anywhere in its arguments, the pins
    coming first; no fake relies on `signal.sigtimedwait`, which macOS
    lacks; a helper that must outlive a kill of a fake's group confirms its
    `setsid()` before the fake goes on.
  - The push-child terminal tests run `project` under a pty made its
    controlling terminal (`fcntl.ioctl(0, termios.TIOCSCTTY, 0)` after
    `setsid`, an opt-in on `run_pty` or a new helper); without it even a
    push child in `project`'s group gets `ENXIO` on `/dev/tty`, and a child
    in a new session gets it either way. `TIOCSCTTY` on macOS is untested
    (plan.md, Risks).
- **Evidence** (the harness spike, Python 3.12.3, Git 2.43.0, load 86 to
  200 on 32 cores): through the launcher the exit status, standard output
  and standard error equal a plain run's in 11 cases, SIGINT and SIGTERM
  give 130 and 143 with `Cancelled.` and the probe's group gone, and the 96
  tests pass with every CLI run launched; at factors 0.05 and 0.1 each fake
  `git` was cut as expected, and the SIGTERM-to-SIGKILL gap read 0.97 to
  1.08 graces.
- **Rationale**: the proposal's OQ-8 fixes the limits ("none; fixed values
  are reported in `limits` and `budget`"), and the time-bound scenarios
  ("A removal past the hard ceiling", "Deadline expiry mid-batch", "Row cap
  and planning failures", "A leg's probe times out", "A git that ignores
  SIGTERM") need 300 s, about 50 s and 15 to 19 s against `run_cli`'s 20 s
  timeout (`tests/test_project.py:141-144`), which the launcher shortens
  without a product hook.
- **Alternatives considered**: an environment variable that scales time,
  rejected by R-26 and FR-066 because `project` would read a test setting in
  production; one factor for every test, rejected by R-29 (at factor f the
  ceiling is 300f and the probe budget 5f; Python-wrapped probes time out
  below f = 0.1 under load, while the ceiling must fit `run_cli`'s 20 s);
  minutes-long tests at the real values, rejected; raising `run_cli`'s
  timeout, rejected (it still leaves 300 s).

## R11. Test runtime, fixture sizes and the CI matrix

- **Decision**:
  - Fixtures stay small. The largest registry, 257 rows, is written
    directly (each admin directory's `gitdir`, `commondir` and `HEAD`, each
    worktree's `.git` file, and one `update-ref --stdin` child for the
    branches) and checked by `worktree list --porcelain -z`: 0.93 s here for
    257 rows, against 24.0 s for 257 `worktree add --no-checkout` children.
    The 4,097-entry status fixture takes 4.3 s to create. The partial
    deletion fixture ("project killed during a deletion") is one commit of
    about 8,000 tracked files, built once per test class (20,000 files took
    20.2 s to create and commit here). No test needs a 10,000-entry index;
    that was task 2.1's measurement fixture.
  - Caps are not scaled: the cap scenarios run at their real sizes (128,
    256, 16 targets, 64 and 4,096 records) on those fixtures. Only time is
    scaled (R10).
  - Budget: each test ends inside `run_cli`'s 20 s; the whole suite stays
    under 8 minutes in the bench container and under 6 minutes per CI job.
  - Names: every test starts `test_clean_`, `test_status_`, `test_doctor_`
    or `test_update_`, then the scenario's title in snake case; a
    `project-command` evidence-model scenario that names no subcommand,
    "The sixteenth scrubbed name on Git 2.36" included, uses `test_status_`
    so that the floor job's `-k` selection runs it.
  - CI: the four existing jobs (`ubuntu-latest` and `macos-latest`, Python 3.10
    and 3.12) run the whole suite unchanged. One job is added, `git-floor`, on
    `ubuntu-latest` with Python 3.10: it checks out, sets up Python and
    installs `requirements.txt` as the four jobs do, then builds Git 2.36.6
    from `git-2.36.6.tar.xz` on kernel.org, checking the sha256 that task 2.2
    recorded (quickstart.md, "The Git 2.36 floor run"), with `make NO_GETTEXT=1
    NO_TCLTK=1 NO_PERL=1 NO_PYTHON=1 NO_CURL=1 NO_OPENSSL=1 prefix=<cache dir>
    install`, cached by `actions/cache` on the version and runner OS; puts it
    first on PATH; fails unless `git --version` prints `git version 2.36.6`;
    and runs `python -m unittest discover -s tests -v -k test_clean_ -k
    test_status_ -k test_doctor_`. Checked at `961c405` with task 2.2's build
    first on PATH: that selection ran 15 tests, OK, in 7.7 s.
  - Skips, each with its reason: non-UTF-8 path tests on macOS (FR-066);
    permission tests when the effective uid is 0; and "The sixteenth
    scrubbed name on Git 2.36" unless the `git` on PATH is 2.36 to 2.39, so
    it runs in the floor job only (FR-067).
- **Rationale**: FR-066 and FR-067; SC-012 (four jobs and the floor job
  green). The measured fixture costs set the sizes, and a cached build keeps
  the floor job to the test run itself.
- **Alternatives considered**: building Git on every run, rejected (minutes
  per run); a distribution package, rejected (Ubuntu 22.04 ships 2.34 and
  24.04 ships 2.43, neither 2.36); a macOS floor job, rejected (FR-067 asks
  for one job, and Git's behaviour does not depend on the runner's OS); the
  whole suite in the floor job, rejected (the `new` and `benches` tests do
  not depend on Git's version); scaling the caps, rejected (the scenarios
  name the real caps).

## R12. The canonical text of `plan_digest`

- **Decision**: the text the proposal adopts from the packet
  (`ideation/brainstorm/project-maintenance-batch-cleanup.md:345-379` at
  `da33d92`, the proposal's `BA:345-379`, "Fresh plan and plan digest"): the
  lowercase hexadecimal SHA-256 of the UTF-8 encoding of `json.dumps(value,
  sort_keys=True, separators=(",", ":"), ensure_ascii=False)`, where `value`
  holds exactly `repository` (`root`, `common_dir`, `dev`, `ino`),
  `merge_target` (`name`, `sha`) and `selected`, a list of
  `[path, branch, head]` in canonical order, or null where the report withholds
  the selection (FR-004, D14). `ensure_ascii` is false for this input only,
  never for the emitted document; `mode`, `observed_at`, validity flags,
  `excluded` and `notes` are not in it. A unit test pins the digest with the
  packet's own fixture values (its lines 1052 to 1130 at `da33d92`), whose
  `plan_digest` this text reproduces: checked, both give
  `7495756d199ba217f41ed4d648c241c95608b4f353c46952e9a7f4cddc17f3bc`.
- **Rationale**: FR-025 names the fields but not the bytes; the packet's
  text does, the proposal adopts it, and `add-project-overview` reads the
  same packet, so one serialization keeps the digest equal across both
  features, Python 3.10 and 3.12, and runs. It is unchanged by an excluded
  row's change (FR-025) and by the mode (FR-004).
- **Alternatives considered**: `ensure_ascii=True`, rejected (it would
  disagree with the packet's fixture for any path holding a non-ASCII code
  point); hashing the envelope's own text, rejected (it carries excluded rows
  and `observed_at`); a joined string, rejected (separators inside paths make
  it ambiguous).

## R13. Which argument is a bare name

- **Decision**: after `expanduser()`, an absolute argument follows the
  absolute-path rule; a relative argument that contains no `/` and is
  neither `.` nor `..` is a bare name and goes through `discover()`'s name
  lookup (FR-016, D8); every other relative argument (`./x`, `x/`, `.`,
  `..`) is a relative path, resolved against the working directory.
- **Rationale**: the test reads the argument's text, so one rule decides
  every spelling. `Path("..").parts` has one component and `Path(".").parts`
  none, so "one path component" alone would send `..` to the name lookup,
  and `Path("./x").parts` and `Path("x/").parts` are both `('x',)`, so a
  component count would send them there too while they contain a `/`;
  today `discover()` ends up treating an existing `..` as a path, and this
  keeps that.
- **Alternatives considered**: `len(Path(arg).parts) == 1` alone, rejected
  (`..`, `./x` and `x/` become names).

## R14. Termination without blocking, reaping by `Popen` (lead ruling R-30)

- **Decision** (the termination ruled by the lead as R-30): D2's child handle
  terminates without blocking. `terminate_group()` keeps its name but only
  starts the sequence and returns at once: SIGTERM to the group with
  `os.killpg()`, and the handle's own kill deadline, the grace read from
  `TIMING` at that call. The driver loop calls the handle's `advance(now)` on
  every tick (the spike's `advance_terminations()` is the shape): at its kill
  deadline, or at once when its leader has exited, SIGKILL to the group (which
  also sweeps a group whose leader is gone) and a reap deadline, the reap wait
  read then; the handle is reaped when `Popen.poll()` returns its status, and
  abandoned at its reap deadline. The selector's timeout also counts these
  deadlines. A `finally` cleanup starts the sequence on every live probe handle
  at once and ticks until each is reaped or abandoned, so it takes at most the
  grace plus the reap wait (4 s) however many handles run. A removal handle
  starts it only at its ceiling (D9), and a delegate (`git branch -d`) handle
  never (R4). The child is observed only through `Popen.poll()` and
  `Popen.wait(timeout)`, never a raw `os.waitpid()`; an abandoned handle
  records `probe-timeout`, is never waited on again (D2), and stays registered,
  so its group is killed again on exit. This keeps D2's SIGTERM, 2 s grace,
  SIGKILL and reap; only who waits changes. The states are tabled in
  data-model.md ("Child handle").
- **Rationale**: a blocking `terminate_group()` per handle stacks graces
  once several handles run. The harness spike drove six fake Gits from one
  selector (probe budget 1 s, grace 0.4 s): with blocking termination the
  second SIGTERM-ignoring child died 2.01 to 2.03 graces past its own
  budget and the sleeping one 2.01 to 2.06;
  with each handle's own deadlines advanced in the loop, each
  SIGTERM-ignoring child died 1.01 graces past its own budget and the
  sleeping one 0.01 to 0.02. At the real values a second SIGTERM-ignoring
  child would wait about 8 s past its budget, past SC-004's 4 s. Feature
  004's driver is one-wide, but `add-project-overview` drives four handles
  at once (its clarification N2) and inherits this handle unchanged. D2's
  "polls `waitpid(WNOHANG)`" is what `Popen.poll()` does; a raw
  `os.waitpid()` on a `Popen`'s child reaps it behind `Popen`'s back.
  Checked: after a raw `waitpid` of a child that exited 3, `Popen.poll()`
  returned 0. A removal that failed would then read as exit 0, and its
  target would become `unknown` instead of `failed` with Git's status.
- **Alternatives considered**: D2's blocking `terminate_group()`, rejected
  by R-30 (it stacks graces); terminating together the handles due in one
  loop iteration, rejected (the spike's "phased" run still stacked when due
  times fell in different ticks: 2.05 graces late); `os.waitpid()` as D2
  words it, rejected for the reason above.

## R15. The existing tests stay as they are

- **Decision**: no existing test is edited except
  `test_clean_revalidates_a_worktree_after_confirmation`
  (`tests/test_project.py:1020`), which moves to the result record: it sets
  `yes=False`, `all_safe=False` and `expect_plan=None`, patches
  `sys.stdin.isatty` to true and the removal question in process (with
  `yes=True` the question is skipped, and without a terminal
  `confirmation-required` refuses first; `confirm()` is no longer called for a
  removal), makes the worktree dirty in that hook, and expects a `refused`
  target with `state-changed` and exit 2. The test module's loader (`:23-26`)
  gains `sys.modules` registration (R10, R-29), a setup line that edits no
  test. The new helpers (a merged, published worktree with a commit of its own;
  bulk registrations; the counting `git` wrapper; the fake Gits; the
  controlling-terminal pty helper; the launcher) are added beside the existing
  ones, and the recipe that four existing tests repeat inline (`:857`, `:880`,
  `:949`, `:1020`) is not extracted from them. The three message tests (`:839`,
  `:880`, `:972`) pass unchanged because `target-excluded` and
  `no-merge-target` keep the baseline wording (D8, D18), and the other 92 pass
  unchanged.
- **Rationale**: FR-066 and SC-012. Three existing tests guard the switch
  of `repo_state()`: `:736` asserts the exact set of doctor error rows, so a
  new error row would break it; `:586` reads `status` of a linked worktree
  and expects that worktree's branch; `:916` keys rows by branch, with
  `detached` kept.
- **Alternatives considered**: extracting the shared recipe from the four
  tests, rejected (it edits tests FR-066 keeps unchanged).
