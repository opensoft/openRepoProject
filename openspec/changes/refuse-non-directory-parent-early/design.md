Lane: openRepoProject-1

# Design

## Context

See `proposal.md` for why and what, and `specs/project-command/spec.md` for the
requirements this design builds: one ADDED, "A parent blocked by a
non-directory is refused before the single-repository path's steps", and four
MODIFIED, each changing only the statements this change makes false. The
council's noted constraints are N1 to N6 in `clarifications.md`, each answered
below: N1 D1, N2 D1 and D3, N3 D3, N4 D2, D3 and D6, N5 D5, N6 D2 and D6.

What in `project` shapes the approach (unchanged on this branch from main
`961c405`):

- `new()` resolves the parent once (`project:322`), refuses an existing
  destination (`project:328-329`), decides whether to ask (`project:331-334`),
  makes the hoisted `--workflow` check for an asked invocation
  (`project:336-337`), and, when asking, computes `known_obstacles()` once
  (`project:339`); that one list feeds the question (`project:340`) and the
  Triad's composed refusal (`project:345-346`).
- `known_obstacles()` (`project:235-254`) reads the parent fact as
  `parent.is_dir()` and, only when that is false, `parent.exists()`
  (`project:247-253`), choosing the missing sentence or the precedent's
  sentence (a).
- The shape branch refuses a parent that is not a directory
  (`project:371-372`). The bench branch refuses shape-only flags
  (`project:383-384`), then selects a generator (`choose()`, `project:385`),
  then the late `--workflow` check (`project:388-390`), `Create:` and the plan
  (`project:392-393`), the dry run's return (`project:394-395`), the `yes`
  confirmation (`project:396-397`) and `parent.mkdir` (`project:398`).
  `main()` prints every `Refused` and `OSError` as `REFUSED: ...` and returns
  2 (`project:1143-1148`).
- Tests: the D13 fixtures end at `tests/test_project.py:56`; the precedent's
  fixture is at `:58-62`; `known_obstacle_cases()` at `:394`, the parent
  fixtures at `:419-444`, the dry-run obstacle test at `:1477`, the test this
  change rewrites at `:1526`. `self.base` is already resolved. CI runs
  `ubuntu-latest` and `macos-latest` on Python 3.10 and 3.12
  (`.github/workflows/tests.yml:9-10`).

## Goals / Non-Goals

**Goals:**

- A parent blocked by a non-directory is refused as the first step of the
  single-repository path, however that path was chosen, before generator
  selection, the plan, `yes` and any creation, the dry run included.
- Every parent sentence is true of the path it names, and a missing parent
  below a file names the path that blocks it.
- The question and the Triad refusal keep one read; the head refusal reads
  the parent as it is when reached.
- The new strings are fixed here (D2) and pinned in the tests as fixtures.

**Non-Goals:**

- Reading permissions, or changing the backstop at `parent.mkdir` (D6).
- Changing the shape branch, the Triad refusal's composition, `main()`'s
  handlers, `ask()`, `confirm()`, `choose()`, `execute()`, or anything from
  `discover` (`project:433`) down.
- Any new flag, environment variable, configuration file, import, network
  access or subprocess on the read.
- No stat-by-errno rewrite, no line under entry 2, no CI change.

## Decisions

### D1. The read: `parent_case(parent)`, once for the question, afresh at the head

One module-level helper, `parent_case(parent)`, takes the resolved parent and
returns a pair `(kind, path)`:

| kind | when | path |
| --- | --- | --- |
| `"directory"` | `parent.is_dir()` | the parent |
| `"not a directory"` (case (a)) | not a directory and `parent.exists()` | the parent |
| `"below a non-directory"` (case (b)) | missing, and the nearest existing path above it is not a directory | that path (ANCESTOR) |
| `"missing"` | missing, and the nearest existing path above it is a directory | that directory |

The reads, in order and only as needed: `parent.is_dir()`; `parent.exists()`;
then, for each `above` in `parent.parents` from the nearest, `above.exists()`
until one is true, and that one's `is_dir()`. The parent is resolved and
absolute, so `parent.parents` ends at the root, which exists, and the walk
always ends (N2); a fall-through, which no path reaches, may return
`("missing", parent)`. A parent is blocked by a non-directory when the kind is
`"not a directory"` or `"below a non-directory"`. A second helper,
`blocked_parent_sentence(parent, kind, path)`, returns sentence (a) or (b) of
D2 for those two kinds.

Two call sites:

1. `known_obstacles(name, parent)` keeps its signature and its order (name,
   openRepoShape, parent). Its parent fact calls `parent_case(parent)` once:
   `"directory"` adds nothing; `"missing"` adds the D13 missing sentence,
   byte for byte; the blocked kinds add their sentence. `new()` still computes
   the list once (`project:339`), and that list feeds the question and the
   Triad's composed refusal, so the two cannot diverge (archived D1). The
   docstring keeps "three local facts" and names this design for the walk.
2. The bench branch, right after the shape-only flag check (`project:383-384`)
   and before `choose()` (`project:385`), calls `parent_case(parent)` afresh
   on every path (by flag, not asked, or after an answer `2`) and, for a
   blocked kind, raises `Refused(blocked_parent_sentence(...) + " Nothing was
   created.")`. It never reuses the question's list: a parent repaired while
   the question waits is then created, and one broken during the wait is
   refused here (proposal, "Reads").

No exception handling is added. On 3.10 and 3.12 the reads ignore the errors
a missing or non-directory component gives, and an unsearchable ancestor
raises earlier, at `destination.exists()` (`project:328`), for an unchanged
tree (N2); a tree changed during the wait that makes a read raise reaches
`main()`'s `OSError` handler, exit 2, as any `OSError` does today. No read
opens the path, so a FIFO is never opened. Observed on Python 3.12.3 at
`961c405` (proposal, Observed):

| Parent given | kind | at the question | at the head |
| --- | --- | --- | --- |
| `FILE`, a link to it, a FIFO, a socket, `/dev/null`, `FILE/` | not a directory | sentence (a) | refused, (a) |
| `FILE/sub`, `FILE/a/b`, a link to `FILE/x` | below a non-directory, ANCESTOR `FILE` | sentence (b) | refused, (b) |
| a missing path below a directory, a dangling link to one | missing | missing sentence | continues |
| a directory, a link to one | directory | none | continues |

Rejected: reusing the question's read at the head (council V2: it would turn
today's success into a false refusal when the parent is repaired during the
wait); a raw `os.stat` classified by errno (archived N5); reading
writability (N4, D6); a check placed before the question or just before
`Create:` (proposal, Alternatives W3 and W2).

### D2. Fixed text

All text is ASCII. `PARENT` is the resolved parent and `ANCESTOR` the path
`parent_case()` returns for case (b); every other character is literal.

The question's parent line under entry 1, with exactly one present when the
parent is not a directory:

```
     Not possible here: The parent directory PARENT does not exist; a Triad is created inside an existing directory.
     Not possible here: The parent PARENT exists but is not a directory; choose a parent that is a directory.
     Not possible here: The parent PARENT cannot be created because ANCESTOR exists but is not a directory; choose a parent that is a directory.
```

The first is archived D13's and the second archived D2's, both unchanged; the
third is new, sentence (b). The Triad's composed refusal keeps its shape, `A
Triad cannot be created here. `, the sentences in order, ` Nothing was
created.`; for `MyApp`, the fake on PATH and `FILE/sub`, `main()` prints:

```
REFUSED: A Triad cannot be created here. The parent PARENT cannot be created because ANCESTOR exists but is not a directory; choose a parent that is a directory. Nothing was created.
```

The head refusal is the sentence followed by ` Nothing was created.`, one text
by flag or by answer, with or without `--dry-run`, printed by `main()` on
standard error, exit 2:

```
REFUSED: The parent PARENT exists but is not a directory; choose a parent that is a directory. Nothing was created.
REFUSED: The parent PARENT cannot be created because ANCESTOR exists but is not a directory; choose a parent that is a directory. Nothing was created.
```

Only this early refusal says `Nothing was created.`; the backstop keeps its
raw errno (N4, D6).

`README.md`, each replacement exact, the rest of its paragraph unchanged and
rewrapped to the README's line width:

- Lines 60-64, from "or a parent that is missing or is not a directory." to
  the paragraph's end, become:

  ```
  or a parent that is missing or is blocked by a non-directory. A single-repository answer creates a missing parent whose nearest existing path above it is a directory. A parent blocked by a non-directory (it, or the nearest existing path above it, exists and is not a directory) blocks both answers: neither answer can create anything in such a parent, and either is refused at once with exit 2, so choose another parent. The Triad stays first and the default. A Triad answer with an obstacle is refused at once with exit 2, before any further prompt; a single-repository answer is unaffected by the name and openRepoShape obstacles.
  ```

- Lines 75-77, the sentence "A choosing flag restores the path without the
  question exactly: its prompts, refusals, standard output, files and exit
  status are those `project new` had before the question existed." becomes:

  ```
  A choosing flag restores the path without the question: its prompts, refusals, standard output, files and exit status are exactly as they would be without the question.
  ```

- Lines 81-82, "then prints the plan of the path its answer chose and writes
  nothing." becomes:

  ```
  then prints the plan of the path its answer chose, unless a refusal comes first, and writes nothing.
  ```

- Lines 95-96, after "Existing destinations refuse.", insert:

  ```
  A parent blocked by a non-directory is refused before the plan and the `yes` confirmation, with exit 2, `--dry-run` included. `--dry-run` reads no permissions: a parent that is a directory the person cannot write still passes the dry run and fails at creation, as before, and so, for a single repository, does a missing parent whose nearest existing path above it is such a directory.
  ```

Lines 53-55 are unchanged. The ASCII check covers the changed strings and the
added lines of `project`, `tests/test_project.py` and `README.md`, not the
whole of `project`, which already carries em dashes (archived N4).

### D3. Tests

All in `tests/test_project.py`; no new dependency. Every existing row and
assertion stays as it is, except the one test of item 6 (N3).

1. **Fixtures.** After the precedent's fixture (`:58-62`), under a header
   naming this design's D2, one literal for sentence (b)'s question line,
   `OBSTACLE_PARENT_BELOW_A_NON_DIRECTORY`, with `{PARENT}` and `{ANCESTOR}`
   as format fields, the literal ` Nothing was created.` for the head
   refusal's end, and a helper composing the head refusal from a question
   line. A method building the blocked kinds under `self.base`: required, a
   regular file with known content, a symbolic link to it, a FIFO
   (`os.mkfifo`), the file given as `FILE/`, `FILE/sub`, `FILE/a/b`, and a
   symbolic link to `FILE/x`; optional, a socket (skipped when binding raises
   `OSError`, as an AF_UNIX path can be too long on macOS) and `/dev/null`.
   Expected PARENT and ANCESTOR are resolved paths (N2).
2. **By flag.** Each kind by `--into`, and the regular file also by the
   positional parent, by `PROJECTS_DIR` and as the default `~/projects` (a
   file at `HOME/projects`, `PROJECTS_DIR` removed), with `--type test --yes`
   and with `--type test --dry-run`: exit 2, standard output empty, standard
   error exactly the head refusal, the `rglob` snapshot of `self.base`
   unchanged and the file still a regular file with its content. At a pty,
   `--type test` without `--yes` for `FILE` and `FILE/sub`: the same refusal,
   no `Type yes to run this plan:`, no `Create:`.
3. **Not asked.** With no choosing flag and the file as `--into`: `CI=true`
   at a pty, a non-terminal standard input, and the workspace name
   `alice-wip` at a pty: the head refusal, exit 2, no question line.
4. **Answer `2` at once.** The registry gains a second available generator,
   so `choose()` would print its list and ask `Select a generator number`
   (`project:196-198`). For `FILE` and `FILE/sub` at a pty, answering `2`:
   the question's line for the case, then the head refusal; no generator
   list line, no `Select a generator number`, no `Create:`, no `Type yes to
   run this plan:`; exit 2; the snapshot unchanged; and the same with
   `--dry-run`.
5. **Case (b) at the question.** `known_obstacle_cases()` gains rows for
   `FILE/sub` by `--into` with sentence (b), alone and with the name and
   openRepoShape obstacles (parent line last), so the pty Triad refusal test
   and `test_inproc_triad_obstacle_runs_nothing` run them;
   `test_pty_dry_run_with_an_obstacle_refuses` gains a `FILE/sub` row. Rows
   are added; no existing row's tuple changes.
6. **The rewritten test** (council V7):
   `test_pty_single_answer_with_a_file_parent_ends_as_the_flag_chosen_path`
   keeps its comparison form: the asked run answers `2` only, the baseline is
   `--type test` with no step; both exit 2 with the same `REFUSED:` line,
   equal to the head refusal for the file; neither standard output contains
   `Create:`; no `warning:` line; the snapshot and the file unchanged.
7. **Repair and break while the question waits** (in process). With
   `builtins.input` patched so that, at the question, the file is replaced by
   a directory before answering `2`, then `yes`: exit 0 and the repository
   created inside it with its `.project.json`. Mirrored, a directory parent
   replaced by a regular file before answering `2`: exit 2, standard error
   the head refusal (a) for it, no further prompt, nothing created.
8. **Not blocked.** A dangling symbolic link to a missing path below
   `self.base`, by flag with `--yes`: exit 0, the target and the repository
   created. A missing parent below a directory stays covered by the existing
   `test_new_preserves_paths_with_spaces_and_writes_profile` and
   `test_dry_run_creates_no_parent`.
9. **Order.** With the file as parent: `--type nomatch --yes`, and
   `--type test --workflow --yes` with no `setup-openspeckit` on PATH, give
   the head refusal; `--org example --yes` keeps `--org, --visibility,
   --family and --elected-by require --shape.`; an invalid name keeps its
   refusal; `--shape --org example --visibility private` keeps `Shape
   creation requires an existing --into parent directory.`, with and without
   `--dry-run`.
10. **The permission boundary** (N4), skipped when `os.geteuid() == 0`: a
    directory of mode 555 (restored to 755 by cleanup) and its missing child
    as `--into`; `--type test --dry-run` exits 0 with the plan; `--type test
    --yes` prints `Create:` and the plan and then `REFUSED: [Errno 13]
    Permission denied: 'PARENT'`, exit 2, with no `Nothing was created.`.

### D4. The feature records

`specs/002-triad-first-project-new/` and `specs/003-parent-obstacle-wording/`
are not edited. The new feature's `spec.md` carries this statement, in
substance: "For a parent blocked by a non-directory, this feature supersedes
the statements that change refuse-non-directory-parent-early makes false: in
feature 003, spec.md's Supersession note where it names a parent that does
not exist with the unchanged sentence (:25-26), User Story 3's title and
intro (:94-97), its acceptance scenario 1 (:106-110) and scenario 4's clause
'the path continues with its generator selection, plan and yes confirmation'
(:118-119), EC-002 (:130-134), EC-003 (:135-138) but its `--shape` clause
(:137-138), FR-002's 'whether that same path exists MUST then choose its
sentence' (:157-158), FR-003 (:159-161), FR-008's 'it continues with its
generator selection, plan and yes confirmation' (:180-181), SC-002
(:207-208), the Assumptions baseline's 'so both runs reach the same yes
confirmation' (:250-251), and quickstart.md :53-54, :113 and :116-125; in
feature 002, spec.md User Story 1 scenario 3's single-repository clause
(:59-61) and scenario 7's single-repository clause (:77-78), User Story 3
scenario 6 (:163-165), User Story 4 scenario 7 (:214-217), EC-003
(:267-269), FR-004 (:317-320), FR-008's 'an invocation that is not asked MUST
keep its existing order of refusals' (:342-343), FR-011's 'a
single-repository answer into the existing single-repository path with its
generator selection, plan and yes confirmation' (:360-362), and
contracts/project-new.md step 7 (:55-58) and its sentence 'A run that is not
asked keeps today's order exactly' (:60). Feature 003's README check
(quickstart.md:86 and spec.md:60-62) is superseded by this feature's README
check. Their other statements stay true." Its `traceability.md` maps each
delta scenario to its tests, the rewritten test (D3 item 6) to "A single
repository taken at the question with a parent blocked by a non-directory",
and keeps `test_pty_single_answer_is_unaffected_by_obstacles` for "A
single-repository answer is unaffected" (feature 003's `traceability.md:25`).

### D5. Handoffs after landing

No new issue on any repository; no caller migrates (N5). When the
realization merges, this lane posts one comment on workBenches#145 if that
issue is still open, naming the realization's merge sha and the sha256 of
`project` at that sha (from `git show <sha>:project | sha256sum`) as an
alternative pin target that carries the early refusal, as archived D5 did. If
#145 is closed by then, nothing is posted, and the change reaches `onp` and
`new-project.sh` at the owner's next pin move.

### D6. What is explicitly not changed

- The shape branch's refusal, "Shape creation requires an existing --into
  parent directory." (`project:371-372`), already early and true.
- The backstop: `parent.mkdir` (`project:398`) and `main()`'s handlers. A
  parent that becomes blocked by a non-directory after the head read, or a
  missing parent whose nearest existing path above it is a directory the
  person cannot write, on a read-only mount or on a full disk, is refused
  there with the raw errno, exit 2; an existing parent the person cannot write
  passes `parent.mkdir` and the generator's own error and status pass through
  (N4). Rewording that backstop is a possible follow-up.
- No permission is read; no line is added under entry 2 (N6).
- The archived N1 residuals (the 3.13 and later symbolic-link loop, the 3.14
  unsearchable ancestor): versions CI does not run; by that record they read
  as `"missing"` here and behave as today.
- The CI matrix and the README's "Python 3.10+".
- Everything from `discover` down, lane openRepoProject-2's surface.

## Risks / Trade-offs

- [For a parent blocked by a non-directory no answer to the question can
  succeed] -> Accepted to keep the ratified question line reachable (N6); the
  README says that neither answer can create anything in such a parent.
- [The question's line and the head refusal can differ when the parent
  changed during the wait] -> Intended: the refusal reflects the parent at
  the decision (D1).
- [Two-fault invocations name the parent first] -> Exit status unchanged
  (N3); D3 item 9 pins the order.
- [An unwritable parent still passes the dry run] -> Stated in the ADDED
  requirement and the README; D3 item 10 pins it.
- [Lane openRepoProject-2's features edit `project` and
  `tests/test_project.py` too] -> Whichever merges second merges main in; no
  rebase, no force push.

## Migration Plan

Nothing migrates (N5): a parent that is not blocked behaves as today, and no
flag or stream changes; a dry run for a blocked parent now exits 2.

1. Ratification by Brett Heap's word "ratify 21" on PR #21.
2. `/speckit.specify`, from a main synced to origin, creates the one feature
   under the next free number; it is recorded once in `tasks.md` under
   "Speckit Handoff", and `/opsx:apply` runs only then.
3. The realization PR merges with green checks on all four CI jobs and
   closes issue #20.
4. The workBenches#145 comment of D5, if that issue is still open.
5. The change is archived after the merge.

Rollback: revert the realization commit on main. Installed `project` artifacts
follow workBenches' pin, so a revert reaches nobody until the pin moves.

## Open Questions

None changes what is built. The council's decisions are taken: one term for
the blocked parent (V1), the fresh read at the head (V2), the delta modifying
only false statements (V3, V5), and the feature number taken at creation
(Migration Plan).
