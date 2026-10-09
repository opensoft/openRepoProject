Lane: openRepoProject-1

# Research: Parent obstacle wording

Nothing is open: the Technical Context has no NEEDS CLARIFICATION, and
`openspec/changes/fix-parent-obstacle-wording/design.md` (D1 to D6) decides
every technical question; its Open Questions section records none that changes
what is built (`design.md:256-260`). The entries below record the decisions
the packet already made, with their rationale and the alternatives it
rejected. They cite; the design holds the detail and governs.

## R1. The second read is `exists()` on the same resolved parent (D1)

- **Decision**: the obstacle still holds exactly when `parent.is_dir()` is
  false; only then, `parent.exists()` on the same resolved `parent` chooses the
  sentence (`design.md:54-65`). The obstacles are still computed once, and the
  refusal is composed from that list (`design.md:67-71`). No exception handling
  is added (`design.md:73-76`).
- **Rationale**: `exists()` has the same error handling as `is_dir()` on every
  version, so the second read adds no exception path the first does not have
  (N3, `clarifications.md:58-68`). The facts stay three, and the question and
  the refusal cannot diverge. The council verified the outcomes on Python 3.10
  and 3.12 (N1), and the design re-probed them on 3.12.3 (`design.md:88-93`).
  For this plan they were probed again on 3.12.3 in py-bench: `is_dir()` and
  `exists()` read False and True for a regular file and for a symbolic link to
  one (by its target), and False and False for a dangling symbolic link.
- **Alternatives considered**:
  - A raw `os.stat` classified by errno: rejected by the lead for this change;
    it would add behaviour, strings and a third case beyond a wording follow-up
    (N5, `clarifications.md:82-94`; `design.md:97-99`).
  - Adding `is_symlink()` to the discriminator: a loop is not one of the two
    cases, and the residual is on a version CI does not run (N1;
    `design.md:100-101`).
  - Reading `exists()` in place of `is_dir()`: a file cannot host a Triad, and
    a Triad answer would meet the shape branch's own refusal later, after two
    prompts, naming an `--into` the person may not have typed (proposal,
    Alternative D, `proposal.md:91-96`).

## R2. Two sentences, the missing one unchanged (D2)

- **Decision**: the missing sentence stays archived D13's, byte for byte; a
  parent that exists and is not a directory gets one new sentence, whose clause
  after the semicolon is deliberately not Triad-specific (`design.md:103-119`).
  The composed refusal keeps D13's shape (`design.md:121-128`).
- **Rationale**: the common case, a missing parent, prints exactly what it
  prints today, and each case gets a sentence that is true of it and states its
  repair (proposal, Alternative B, `proposal.md:82-87`).
- **Alternatives considered**:
  - One sentence true in both cases: it changes the text the missing case
    prints today and states no repair for the file case (proposal, Alternative
    A, `proposal.md:78-81`).
  - Changing nothing: the text is false in a reachable case, and "does not
    exist" sends the person to `mkdir`, which fails on the file (proposal,
    Alternative C, `proposal.md:88-90`).
  - A third sentence, for a parent whose status cannot be read: rejected with
    the stat-by-errno rewrite (design Non-Goals, `design.md:50`; N5).

## R3. The new sentence is pinned as a fixture outside the D13 block (D3)

- **Decision**: one new literal after the `# End D13 fixtures.` marker, under
  its own header; new rows in `known_obstacle_cases()`, the routes test and the
  dry-run test; a `rglob` snapshot plus the file's type and content for a
  parent that exists and is not a directory; two new pty tests
  (`design.md:142-188`).
- **Rationale**: a fixture inside the D13 block would stop it being a verbatim
  copy of the archived design; the existing `(parent / name).exists()` check is
  vacuous beneath a file; and the routes and dry-run tests build their own
  cases, so rows added to `known_obstacle_cases()` reach neither (N2,
  `clarifications.md:37-56`).
- **Alternatives considered**: editing `OBSTACLE_PARENT` or an existing row
  (the missing sentence is unchanged, and no existing assertion is edited:
  `design.md:144-146`); testing every route with the link and dangling cases
  too (the parent is resolved the same way for every route, N6, so those cases
  go by `--into` only).

## R4. No CI change (D6)

- **Decision**: the CI matrix (3.10 and 3.12 on Linux and macOS) and the
  README's "Python 3.10+" stay as they are (`design.md:225`).
- **Rationale**: the later-version outcomes (a symbolic-link loop on 3.13 and
  later, an unsearchable ancestor on 3.14) print the pre-existing wording on
  versions CI does not run, and are recorded as residuals (N1, N5;
  `design.md:222-224`).
- **Alternatives considered**: adding later versions to the matrix or changing
  the README's supported versions; not this change's (N5; design Non-Goals,
  `design.md:50`).

## R5. The bench path's late refusal stays (D6)

- **Decision**: for a parent that exists and is not a directory, the
  single-repository path keeps showing the plan, asking for `yes` and only then
  refusing (`[Errno 17] File exists`, exit 2), and its dry run exits 0
  (`design.md:218-221`).
- **Rationale**: this change is a wording change; the README's new sentence
  tells the reader that such a parent blocks both answers (`design.md:229-231`).
- **Alternatives considered**: an earlier refusal on the bench path; its own
  change, on Brett Heap's word (`design.md:221`; proposal, Out of Scope).
