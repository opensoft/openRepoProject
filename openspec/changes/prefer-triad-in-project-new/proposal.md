Lane: openRepoProject-1

# Proposal: prefer-triad-in-project-new

Status: draft, proposal only. The alignment review, the council and the design
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
repository is created that the person has not confirmed." Issue #3 hands the
task to this repository's governance, and this change is that governance.

The other work-start surfaces already speak the preference: the shared agent
protocol tells a session to offer the Triad first when a person creates a
project (brettheap/new-workstation#52, merged `e081c5ab`); setup-openspeckit
advises at bootstrap (opensoft/workBenches#139, merged `9fbe609c`); and
openRepoShape's scaffold, adopt and doctor carry it (opensoft/openRepoShape#164,
merged `1a9fc537`). `project new` is the one creation surface that does not:
its default is a single repository from a bench generator, and the Triad is
reached only by typing `--shape`.

## What Changes

- **`project new` asks Triad-or-single when a person is at a terminal and has
  not chosen by flag.** The Triad is listed first and is the pre-selected
  answer, with the posture beside it (preferred, not required; elective;
  confers nothing). A single repository is accepted without a reason being
  asked. The answer is not a confirmation: the Triad continues into today's
  `--shape` path, whose openRepoShape typed confirmation is kept; single
  continues into today's bench path, whose `Type yes` confirmation is kept.
  The question itself creates nothing.
- **Explicit flags keep today's behaviour byte for byte.** An invocation that
  has already chosen by flag (`--shape` or a shape option, `--bench`, `--type`,
  `--description`, or `--yes`), or whose stdin is not a terminal, asks nothing
  new and keeps today's prompts, refusals, stdout, created files,
  `.project.json` and exit status. The one addition is ratified design D2's:
  when such an invocation creates a single repository, it writes one advisory
  line to stderr afterwards (OQ-2). `onp` and `new-project.sh` `exec` into
  `project new`, so they inherit both behaviours with no workBenches change.
- **`project status` and `project doctor` give the advisory once for a
  non-exempt single repository (OQ-1)**: only where the command already
  reports kind `single`; only in the human report, and only when stdout is a
  terminal and `CI` is unset or false; never as a `checks` row, so it cannot
  change an exit status (including under `--strict`); never in `--json`. Its
  wording mirrors setup-openspeckit's `TRIAD_ADVISORY_LINES` (workBenches
  `9fbe609c`), in a line or two: the preference with the posture,
  openRepoShape's `adopt-project.py` as the way to convert,
  `single-repository.yaml` as the way to stop meeting it, and that nothing
  changes.
- **Silent where the shape question is answered or does not arise**, each read
  from a declared fact and never inferred: an elected Triad root (`project.yaml`
  with `kind: project-manifest`, `schema: project-repo-schema`, a `spec` and a
  `code` leg); a leg clone (its `AGENTS.md` opens as openRepoShape's leg
  templates write it), which gets the instruction to work from its assembly
  root instead; a family holder (`family.yaml`, `kind: family-manifest`, no
  `project.yaml`); a `<user>-wip` workspace repository (the naming policy's
  `workspace` form on the `origin` name, or a checkout that
  `~/.agents/workspace.yaml` names); a repository whose root
  `single-repository.yaml` is valid by openRepoShape's rule; and a directory
  that is not a Git repository. The first and third are never reported as
  `single`, so they are silent by construction. No other class is exempted
  (the packet's ruled OQ-2).
- **`single-repository.yaml` is read as openRepoShape's black box.** Present and
  valid by openRepoShape's published rule (at `1a9fc537`: the file parses as a
  YAML mapping whose `kind` is `single-repository-record`; `kind:` decides, and
  a missing field does not end the silence): silent. Absent: the advisory.
  Present but not valid: the advisory plus one line saying why the file does not
  silence it; nothing refuses, fails or changes an exit status. `project`
  validates no field, writes no record and defines no schema.
- **README and tests.** "Create a project" and "Understand a project" describe
  the question and the advisory; tests cover both and every path that must
  stay unchanged.

## Rules This Change Keeps

The ratified packet's rules (issue #3), as non-negotiables:

- **The Triad is PREFERRED, and stays ELECTIVE and confers NOTHING**: no gate,
  no floor, no grant, no clearance eligibility, no lifecycle state and no review
  difference. Wherever `project` states the preference it states that posture
  beside it.
- **A single repository stays a supported, fully conformant answer**: chosen
  without a reason asked, created exactly as today, and reported exactly as
  today apart from the advisory line.
- **Nothing is converted or created without the person's confirmation.** The
  question is not the confirmation; the Triad default ends at openRepoShape's
  own typed confirmation, so no run creates three repositories on a default
  (ratified D2). `project` never runs `adopt-project.py`, never converts an
  existing repository, never writes `single-repository.yaml` or a manifest on
  the advisory's account, and records nothing about having advised.
- **Never a gate, check or review input.** The advisory is never a `checks`
  row or a `--json` field and changes no exit status, and it is never printed
  without a person at the terminal, so no unattended run, CI log or review
  output carries it. No CI step or validator in this repository reads any
  repository's shape; the new tests run over temporary fixtures only.

## What This Repository Does Not Own

- **`single-repository.yaml`**: its schema
  (`contracts/single-repository-record.yaml`), template and silencing rule are
  openRepoShape's. Governed by opensoft/openRepoShape#163 (closed, completed)
  and realized by PR #164, squash-merged 2026-10-06 as openRepoShape main
  `1a9fc537`. openRepoShape deliberately ships no validator for it. This change
  follows that published rule and does not anticipate changes to it.
- **Scaffolding, adoption and shape diagnosis**: openRepoShape (the
  `openRepoShape` launcher, `scaffold-project.py`, `adopt-project.py`,
  `shape-doctor.py`), each with its own prompts and exits.
- **The `onp` and `new-project.sh` forwarders and the pinned install of
  `project`**: workBenches (lane `project-command`).
- **The doctrine, the advisory's meaning and its exemptions list**:
  openxFactory's ratified packet. The agent-session form is the shared
  protocol's; the bootstrap form is setup-openspeckit's.

## Capabilities

### New Capabilities

- `project-triad-preference`: `project new` offers the Triad first at a
  terminal and otherwise behaves as today; `status` and `doctor` advise a
  non-exempt single repository once; both read only declared facts and never
  gate anything.

### Modified Capabilities

None. `openspec/specs/` is empty on main (`openspec list --specs`: "No specs
found."), and `project-command`'s requirements live only in its unarchived
change. If `chore/archive-completed-changes` (pushed at `0e7f029`, no PR) lands
first and promotes `project-command`, the spec phase decides whether "Delegate
project creation" takes a MODIFIED delta (see OQ-4).

## Impact

- **`project`**: `new()` (the question and its routing; `ask()`'s terminal rule
  kept); a small offline advisory reader used by `inspect_project()` and
  `print_report()` for `status` and `doctor`. No new flag is proposed. The
  reader must never raise: a missing PyYAML, an unreadable manifest or an
  unreadable record must not turn `status` or `doctor` of a single repository
  into a refusal. It reads local files and local Git only, never a fetch, per
  `project-command`'s "inspection SHALL never fetch, reset, or bootstrap".
- **`README.md`**: "Create a project" (the question, its default, the stderr
  line, which flags skip it) and "Understand a project" (the advisory, its
  exemptions, and that it never touches exit codes or `--json`).
- **`tests/test_project.py`**: pseudo-terminal runs of the question (Enter
  reaches the shape path with the owner's confirmation kept; single reaches the
  bench path with `Type yes`; an interrupt exits 130 with nothing created);
  byte-identity of stdout, created tree and exit status against today for every
  explicit-flag and non-terminal invocation; one fixture per exemption plus
  valid, wrong-kind, unparsable and unreadable records; `--json`, `--strict`
  and `CI=true` unchanged on a non-exempt single repository.
- **No new dependency.** Handoffs this change does not perform: workBenches
  moves its pinned `project` artifact on its owner's act; openxFactory's
  archiving actor checks task 5.6's box citing this change's merged PR (packet
  `tasks.md` § 6).

## Out of Scope

- Converting an existing repository, or wrapping `adopt-project.py` in
  `project`.
- Writing `single-repository.yaml` from any prompt (setup-openspeckit holds the
  same out, its decision 3).
- Family traversal: the advisory concerns the inspected root only; none is
  given per family member or leg, and `snapshot()` recursion is unchanged.
- Any gate, check, CI step, review output or `--json` field.
- `project update`, `project clean` and `project benches` output.
- A bench generator inside a Triad: choosing the Triad creates openRepoShape's
  structure only, as `--shape` does today ("requires a future adapter").

## Open Questions

- **OQ-1 (alignment): is the inspection advisory admitted?** Task 5.6 governs
  creation only; the inspection advisory comes from issue #3's "One possible
  shape" ("The owning lane decides."). The ratified ADDED requirement says the
  advisory "SHALL be given only at such surfaces and only in these forms" and
  names three forms; `project status`/`doctor` is none of them by name.
  Proposed: admit it as the form nearest openRepoShape's doctor ("MAY report it
  beside what they already report, and SHALL NOT change an exit status"),
  narrowed to a person at a terminal. If the review reads the list as closed,
  the inspection bullets drop and the change is creation-only, which still
  discharges task 5.6.
- **OQ-2: does "byte for byte" admit D2's stderr line?** Ratified design D2: "A
  non-interactive invocation does what its flags say, and prints the
  recommendation when it creates a single repository." Proposed: stdout,
  prompts, refusals, created files and exit status byte-identical; one stderr
  line after a successful single-repository creation that did not go through
  the question. Alternative: strict identity, with flagged creations printing
  nothing new.
- **OQ-3: how the exemptions are read without the network.** The record rule
  is no longer pending: openRepoShape shipped it at `1a9fc537`, and `kind:`
  decides, so presence-only would diverge (a wrong-kind file silences nothing
  there). Delegating to the installed `openRepoShape --doctor` is ruled out:
  with no checkout beside it the launcher clones the standard, which the
  no-fetch rule forbids, and it does not pass `--json` through. Importing
  `scripts/shape_advisory.py` needs a checkout `project` cannot assume, and
  openRepoShape's tests confine its importers to its three tools. Proposed:
  apply openRepoShape's published rule locally, checking `kind` only, as
  setup-openspeckit does (its decision 7: "a second validator here would be a
  second schema"). For design: where openRepoShape and setup-openspeckit read a
  leg or a `<user>-wip` differently (openRepoShape also accepts a
  `-spec`/`-code` name and the directory's own name), which to mirror.
- **OQ-4: the Triad answer when its prerequisites are missing.** The governing
  text is silent. Proposed: the Triad stays first and the default; missing
  `--org`/`--visibility` are asked at the terminal (still explicit answers, as
  "Shape creation SHALL require explicit organization and visibility" asks);
  without `openRepoShape` on PATH the question says so up front, and the Triad
  answer refuses with today's "Install openRepoShape through workBenches
  first." and creates nothing.
