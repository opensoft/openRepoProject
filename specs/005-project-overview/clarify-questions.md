Lane: openRepoProject-4

# Clarify questions: Project overview

**Path**: `specs/005-project-overview/clarify-questions.md`

**Status**: Open, for Brett Heap; not answered here. Asked by lane
openRepoProject-4 for feature `005-project-overview` on 2026-10-11, after the
spec's specify step. Each question is one the ratified change
(`openspec/changes/add-project-overview/`) and feature 004 leave genuinely
open; what their text settles is in `spec.md`, Clarifications, C-1 to C-21.
No requirement changes until an answer is given; answers join the spec's
Clarifications as a later session.

Five questions, in one block.

---

## Q1. A Triad assembly given as `--root`

**Context**: A root is examined itself (C-1), and the README's check of one
project is `project overview --root <dir>` (proposal, Impact). A Triad's
assembly repository holds its spec and code legs as submodules at `spec/`
and `code/` (openRepoShape's README), so both legs are immediate entries of
that root, and the change gives every submodule checkout an
`unsupported-layout` repair finding of severity error (POD:97-102; design
D3, item 1). The check of one Triad therefore reports two error rows and
exits 1 on every run (spec EC-014). A default-root run is unaffected: the
legs are not immediate entries of the projects directory.

**Question**: How should feature 005 treat the one-project check for a
Triad?

**Recommended:** Option A - It builds the ratified rule ("unknown is never
healthy", and the overview never suggests what `project clean` refuses) at
no cost now, and a later change can relax it once real runs show the need.

| Option | Description |
|--------|-------------|
| A | Build as ratified: each leg row carries `unsupported-layout`, the run exits 1, and the README says so for Triad assemblies. |
| B | Build as ratified, and open a follow-on OpenSpec change now that makes a submodule checkout declared as a leg of an examined assembly an informational row instead. |
| C | Amend change 2 before the plan (a spec fix on `main`), so feature 005 builds the leg treatment from the start; the plan waits for it. |

---

## Q2. What must exist before feature 005's plan is written

**Context**: The change creates feature 005 only after feature 004 merges
(proposal, Status; `tasks.md` 3.1). Brett Heap's word of
2026-10-11T16:14:21Z moved the specify step only, and the record says the
plan and the implementation "still wait for feature 004's code and for his
word". Feature 004 is at its plan (`dd923ee`), with no code yet. The
overview drives feature 004's child handle, driver and parsers (spec,
Dependencies), and the plan re-pins every code citation against `main`.

**Question**: Which state of feature 004 must exist before the plan starts?

**Recommended:** Option A - The runner's interface, the shared constants
and the citations are what feature 004's review may still change, so
planning against an unmerged branch risks a second plan; A is also the
order the change already sets.

| Option | Description |
|--------|-------------|
| A | Feature 004 merged into `main`; the plan pins against that `main`. |
| B | Feature 004's runner, parsers and evidence model (its plan slices 2 and 3) pushed on its branch; the plan pins against that branch and re-pins after the merge. |
| C | No standing rule: Brett Heap's word at the time decides. |

---

## Q3. The overview's tests and the Git 2.36 floor job

**Context**: Feature 004 adds a CI job that builds Git 2.36 and runs the
`clean`, `status` and `doctor` tests with it first on PATH (feature 004
FR-067; change 1's design D17). The overview refuses a Git older than 2.36
and so claims to work at 2.36 (spec FR-043), but change 2's Impact lists
only `project`, the README and the tests, and no CI change.

**Question**: Should the overview's tests also run in the Git 2.36 floor
job?

**Recommended:** Option B - It proves the overview's own claim at 2.36 on
the probes it drives for little CI time, while the shared probes are
already proven there by feature 004's tests; A adds the cap-scale fixtures
to the floor job's run.

| Option | Description |
|--------|-------------|
| A | Yes, all of them: the floor job's selection gains the overview tests, a CI change beyond change 2's Impact list. |
| B | A small set: the version refusal and one end-to-end run over a fixture with linked worktrees, merge targets and a gated suggestion. |
| C | No: the floor stays proven by feature 004's tests of the shared probes the overview reuses. |

---

## Q4. Telling agents that a suggestion is not permission

**Context**: "Evidence is not permission" reaches people through the
README (spec FR-048). Agents working in this repository read `AGENTS.md`,
which covers `project new` (feature 002) and says nothing of the overview;
change 2's Impact names no `AGENTS.md` change. An agent reading `project
overview --json` could run a suggested `project clean <root> --all-safe`
with `--apply --yes` on its own.

**Question**: Should agents be told in `AGENTS.md` that an overview
suggestion is advice to review, and that applying it needs the person's
word?

**Recommended:** Option C - The guidance matters for agent safety, but it
also concerns feature 004's `--apply --yes`, so one governed change can say
it for both while feature 005 stays within its ratified scope.

| Option | Description |
|--------|-------------|
| A | No `AGENTS.md` change: the README section carries the rule, as the change scopes it. |
| B | Add one `AGENTS.md` paragraph in feature 005, recorded as a departure from change 2's Impact on Brett Heap's word. |
| C | A separate small OpenSpec change for agent guidance on the overview and the batch apply, after feature 005. |

---

## Q5. Feature 004's partial-removal note in the overview

**Context**: Feature 004 adds the advisory row note `partially-removed` to
a dirty linked worktree whose status records are all deletions of tracked
files, the trace a removal killed midway leaves, shown beside the `dirty`
advice with recovery text (feature 004 FR-009; change 1's design D4).
Change 2's worktree row is a closed field list for schema 1 with no `notes`
(POD:632-638), so the overview shows that worktree as a plain `dirty`
finding, whose read-only suggestion leads to `project clean <root>`, which
shows the note.

**Question**: Should the overview surface the partial-removal note?

**Recommended:** Option A - The case is rare, its recovery happens in
`project clean`, to which the overview already points, and option B stays
open later without a schema change, a new field being additive
(POD:655-658).

| Option | Description |
|--------|-------------|
| A | No, as ratified: the `dirty` finding's read-only suggestion leads to `project clean`, which shows the note. |
| B | Yes, as an additive worktree-row `notes` field within schema 1, through a follow-on OpenSpec change. |
| C | Yes, in the `dirty` finding's message, through a follow-on change to the fixed message text. |

---

You can reply with the option letter for each question (e.g., "Q1 A, Q2 A,
Q3 B, Q4 C, Q5 A"), accept every recommendation by saying "yes" or
"recommended", or give your own short answer for any of them.

**Path**: `specs/005-project-overview/clarify-questions.md`
