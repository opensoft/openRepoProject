Lane: openRepoProject-1

# Proposal: add-project-overview-family-relationships

Status: observation record; draft; nothing here is ratified. Proposed on Brett Heap's word "start
report E's candidate 3" (2026-10-22T17:39:41Z), the third candidate of lane openRepoProject-1's
work survey of 2026-10-20. Governing issue: opensoft/openRepoProject#36, claimed by lane
openRepoProject-1 (comment 6347306957; UNVERIFIED: the id is as the claim tool printed it, not
read back, since no `gh` call was allowed; `gh api` on the comment would verify it); refs #6, the
packet's record, and #10, the overview change's issue. It records what `project` and the packet
do and say about families today and the decisions an extension of `project overview` needs. It
writes no spec delta, no `design.md` and no `tasks.md`: the deltas are held until feature 005's
clarify answers land as amendment A1
(PR #34) and #29's overview blocks settle, so that they are written once (Dependencies and
Sequencing). Next: an alignment review, a council, then Brett Heap's rulings.

Citations are `file:line` at the sha named. `APO` is `openspec/changes/add-project-overview/`
(change 2, ratified, unarchived) and `APO/ov` its `specs/project-overview/spec.md`; `CAS` is
`openspec/changes/add-project-clean-all-safe/` (change 1), `CAS/pc` and `CAS/cmd` its
`project-clean` and `project-command` deltas; `PRS` is `openspec/specs/project-review-safety/
spec.md`; `project:N` is the executable. All of these are at main `15504f1`. The packet under
`ideation/brainstorm/` is `DI` (`project-maintenance-project-discovery.md`), `SY`
(`...-synthesis-inspect-and-retire.md`), `OV` (`...-overview.md`), `BA` (`...-batch-cleanup.md`)
and `HO` (`next-session-project-maintenance-fix-handoff.md`), each line with the sha it was read
at: `da33d92`, which change 2 cites, or `15504f1`, after packet revision 1 (`e45155a`). `ORS` is
the local openRepoShape checkout, read only by `git show`: its naming contract at `1a9fc53`, the
sha `project:204-211` pins, and its family template at its head `2476992`. Branch heads after
`git fetch` on 2026-10-22: #29 `a529310`, A1 `e4a30fc`, feature 005 `6069d3a`, #27 `97bf4ee`
and #26 `7a1bd84`.

## Why

Change 2 shows a `family.yaml` holder as exactly one row of kind `family-holder`; it never reads
the members list, and the envelope's `relationships` is always `[]` (APO/ov:35-40, :620;
DI:276-282 at `da33d92`, DI:331-337 at `15504f1`). In openRepoShape's layout a member's working
clone sits beside the holder, `<Family>/<Project>`, with the holder at `<Family>/<Family>` (ORS
`templates/family-root/scripts/siblings.py:12-15`). The marker `D/<name of D>/family.yaml` makes
the holder the candidate, never `D` (APO/ov:24-30), and discovery never recurses (APO/ov:18-19),
so in that layout no member's working clone is a candidate unless the family folder itself is
given as a root (APO/ov:67). From the overview a person cannot see which members a family
declares, which are present, missing or out of place, or which other rows belong to it.

The packet bounds the work twice. Family relationships share the deferred boundary of the remote
and bench extensions: "opt-in probes, bounded time, explicit unknown values, and no mutation"
(DI:1062-1064 at `da33d92`, DI:1329-1331 at `15504f1`). And "Family grouping, when added later,
does not grant permission to clean every sibling" (SY:34-37 at both shas). Change 2 leaves family
traversal to its own proposal (APO proposal.md:569-570; OQ-27, :631), which this is.

### Observed

**What `project` does with families**, at `15504f1`:

| Where | Behaviour |
| --- | --- |
| `manifest()`, project:422-430 | reads `project.yaml`, else `family.yaml`; a `kind` other than `family-manifest` refuses (:427-428) |
| `discover()`, project:433-467 | a bare name prefers `<base>/<name>/<name>/family.yaml` in each `projects_dirs()` entry, two refusing as ambiguous (:436-443); a directory `D` resolves to `D/<name of D>` when that holds `family.yaml` (:455-457), else to the nearest ancestor with either manifest (:458-461) |
| `snapshot()`, project:822-867 | reads `members` (:835), each a mapping (:839-840); the name is `project`, else `name`, matched by `[A-Za-z0-9_-]+` or the whole command refuses (:849-851); the clone is `<holder parent>/<name>` (:852); one holding `project.yaml` is snapshotted in full, anything else is `{"role": "member", "path", "present": false}` (:853-856); `path`, `id`, `repository` and `pin` are never read |
| `check_rows()`, project:876-906 | no workflow check for a family (:888); a member neither snapshotted nor present is an `error`, "Missing checkout; use the estate's bootstrap/siblings command" (:893-897) |
| doctor `--validate`, project:955-973 | runs `<holder>/scripts/validate-family.py`, and each member's own validators, when the file exists (:958-967, :970-972) |
| `update_child_states()`, project:980-989 | yields every member and leg; shape and bench updates refuse a missing, dirty, detached or off-branch child (:1013-1018; tests/test_project.py:789-799) |
| bench update, project:1038-1039 | refuses "an assembly/family root" |
| `cleanup_report()`, `clean()`, project:544-622, :669-670 | resolves through `discover()`, then reads one repository and its manifest; no member is read |
| `parser()`, project:1074-1122 | subcommands `new`, `benches`, `status`, `doctor`, `update`, `clean`; no `overview`, `discover` or `list` |

Code reading: a member is snapshotted only when it holds `project.yaml`, which `manifest()` reads
first, so a member is always a project whose children are legs read by `repo_state()`
(project:841-847). Traversal is holder, member, leg, never deeper, and the cycle check
(project:823-826) cannot fire through a family.

**What the packet, the ratified texts and openRepoShape say:**

| Source | Statement |
| --- | --- |
| DI:278-282 (`da33d92`); DI:333-337 (`15504f1`) | the holder is read through `manifest()` "only for its name and kind check"; it "never visits declared siblings, pinned member copies, or mounted legs" |
| DI:284-290 (`da33d92`); DI:339-345 (`15504f1`) | probes follow the directory; a member that is an immediate entry of a root is its own row; "the holder neither claims it nor lends it probes" |
| DI:1455-1457 (`da33d92`); DI:1783-1785 (`15504f1`) | deferred: holder, working sibling, mounted member and parked record "represented as relationships without duplicate checkout probes" |
| DI:733 (`da33d92`); DI:959 (`15504f1`) | `relationships`, type array, "always `[]` in version 1" |
| DI:1063-1066 (`15504f1`) | adding a field or enum value is additive within version 1; changing a field's meaning increments it |
| OV:142-146 (`da33d92`); OV:185-190 (`15504f1`) | family relationships are an extension point; each extension keeps its owner's boundary |
| BA:103-105 (`da33d92`); BA:127-129 (`15504f1`) | the batch never means family members, mounted legs or pinned member copies |
| HO:138-141 (`da33d92`); HO:141-144 (`15504f1`) | do not traverse siblings, pinned members or mounted legs "until a family integration is separately proposed" |
| APO/ov:35-40 | the overview "SHALL NOT read a family's member list"; one row; `relationships` `[]`; probes only for a Git toplevel |
| CAS/pc:568-571 | `--all-safe` plans one repository, "never of a sibling, a family member, a mounted leg, a pinned member copy" |
| ORS `contracts/repository-naming.yaml:13-18`, `:373-398` (`1a9fc53`) | names confer nothing; "A consumer deriving a permission from a family id is defective"; a holder pins members' assembly roots as submodules under `members/`; "membership is navigation" |
| ORS `templates/family-root/family.yaml:15-25`, `:57-59` (`2476992`) | each member is "a whole project in its own right"; `members_dir: members`; "A consumer deriving a permission from membership is defective" |
| ORS `scripts/family.py:443-445`, `:511-518` (`2476992`) | a member row is `project`, `id`, `repository`, `path: members/<project>`, `pin` |
| ORS `siblings.py:28-34` (`2476992`) | two copies: the pinned, detached one under `members/` for bootstrap and validate, and the sibling "where a human works" |

**Fixture runs.** `FX` is `/workspace/projects/.scratch/openRepoProject-1-wave6-20261022/fx`,
built by `FX/scripts/build.sh`, run by `FX/scripts/run.sh`, outputs in `FX/out/`. Every run was

```
env -i HOME=FX/home PATH=FX/bin:/usr/bin:/bin PROJECTS_DIR=<P> WORKBENCHES_ROOT=FX/workBenches \
  LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_NOSYSTEM=1 <python> <worktree>/project <args>
```

with `<python>` Python 3.12.3 (`python3`) and uv's CPython 3.10.18 with `PYTHONPATH=FX/py310-shim`
(the installed PyYAML 6.0.3, pure Python there); Git 2.43.0. `FX/bin` holds fake `openRepoShape`,
`setup-openspeckit`, `park`, `resume`, `docker`, `make`, `gh`, `claude`, `codex`, `gemini` and
`copilot` that log and exit 97: none was called. A digest of every fixture path, size, mtime and
mode was `265096a4dc380d70` before and after. Each 3.10 output was byte-identical to its 3.12
output. UNVERIFIED: the 3.10 runs read the 3.12 install's PyYAML through the shim, not a 3.10
install as CI's `test (3.10)` job has; that job, or a 3.10 environment with PyYAML, would verify
them. `P` is `FX/projects`: family folder `acme`; holder `acme/acme`, a Git toplevel whose
`family.yaml` declares `web`, `api`, `ghost` and `billing`, each with `path: members/<name>`, and
holds `members/web/project.yaml`; `acme/web`, a repository with `project.yaml` and a leg `spec`;
`acme/api`, a repository with no `project.yaml`; no `acme/ghost`; `billing`, a repository with
`project.yaml` cloned beside the family folder; `tools`. Three more estates: `FX/projects-nogit`
(`beta/beta/family.yaml`, no `.git`), `FX/projects-bad` (`gamma/gamma`, member `../evil`) and
`FX/projects-self` (`delta/delta`, a repository whose member is `delta`).

| Run | `PROJECTS_DIR`, cwd | args | exit 3.12 / 3.10 | decisive output |
| --- | --- | --- | --- | --- |
| O1 | `P` | `--help` | 0 / 0 | `{new,benches,status,doctor,update,clean}` |
| O2 | `P` | `overview --help`; `discover`; `list` | 2 / 2 | `invalid choice: 'overview' (choose from 'new', 'benches', 'status', 'doctor', 'update', 'clean')`, the same for the others |
| O3 | `P` | `status acme --json` | 0 / 0 | `root` `P/acme/acme`, `kind` `family-manifest`; `web` a full snapshot with leg `spec` present; `api`, `ghost`, `billing` each `{"role": "member", "path": ..., "present": false}`; nothing from `members/` |
| O4 | `P` | `status acme` | 0 / 0 | `member: P/acme/api -- missing; dirty=unknown`, likewise `ghost`, `billing` (` -- ` is the U+2014 that project:928 prints) |
| O5 | `P` | `doctor acme --json` | 1 / 1 | `error` "Missing checkout; use the estate's bootstrap/siblings command" for `api`, `ghost`, `billing`; `web` warnings for workflow and park/resume |
| O6 | `P` | `doctor acme --validate --json` | 1 / 1 | O5 plus `error` "Required shape validator missing: P/acme/acme/scripts/validate-family.py" and `web`'s two; none exists, none ran |
| O7 | `FX/projects-nogit` | `status beta --json` | 0 / 0 | `repository` `{"path": ..., "present": false}`, `children` `[]` |
| O8 | `FX/projects-nogit` | `doctor beta`; `doctor beta --strict` | 0 / 0; 1 / 1 | `WARNING ...: No Git checkout; initialize through the project workflow` |
| O9 | `FX/projects-bad` | `status gamma --json` | 2 / 2 | `{"error": "Invalid family member name in FX/projects-bad/gamma/gamma"}` |
| O10 | `FX/projects-self` | `status delta --json` | 0 / 0 | one child, the holder itself, `"present": false` |
| O11 | `P/acme` | `status web --json` | 0 / 0 | `web` is its own `project-manifest` with leg `spec`, the directory O3 lists as a member |
| O12 | `P`, cwd `P/acme` | `status --json` | 0 / 0 | `root` the holder `P/acme/acme` (README.md:162) |
| O13 | `P`, cwd `P/acme/api` | `status --json` | 0 / 0 | `root` `P/acme/api`, `kind` `single`, no children |
| O14 | `P`; 3.10 without the shim | `status acme --json` | 2 | `{"error": "YAML inspection needs PyYAML; use a workBench with python3-yaml installed."}` (project:41) |

Not run: `new`, `update`, `clean` and `benches`; `doctor --validate` with a validator present,
which would execute it (project:963-967); and `project overview`, which does not exist at
`15504f1` (O2), so every overview behaviour cited here is ratified text, not an observation.

The runs show: a present clone that is not a project (`api`) and a clone outside the family
folder (`billing`) read exactly as an absent member (`ghost`), and doctor calls all three an
`error` (O3 to O5); one malformed entry refuses the whole family with exit 2 (O9); a member
named like the holder points at the holder (O10); the pinned copies under `members/` are never
read (O3); one directory is both a member and a project with nothing linking the two (O3, O11),
and from a member's own directory nothing names its family (O13).

## What Changes

Candidates, not requirements; each open point is a Decision below.

- **Opt-in** (Decision 1): `project overview --families`; without it the document and report are
  change 2's, byte for byte.
- **Membership from the holder's own manifest.** The `members` list of the `family.yaml` already
  read for the holder's name and kind (APO/ov:319-320; DI:333-335 at `15504f1`); each entry
  names a working sibling at `<holder parent>/<project>` (Decision 8); `id` and `path` are
  reported as declared, `path` and `pin` never followed.
- **Traversal one level, inside the existing bounds** (Decisions 3, 5). Each sibling is examined
  by bounded filesystem tasks (`lstat`, marker checks, manifest read); one that is a candidate
  joins the candidate list before canonical sorting and the candidate cap, and is probed as any
  candidate is, once, also when it is an immediate entry of a root (DI:1783-1785 at `15504f1`).
- **Relationships** (Decisions 2, 4, 9): one entry per declared member in the envelope's
  `relationships`, with a state (`present`, `not-a-project`, `mismatched`, `missing`, `invalid`,
  `unknown`) and the `path` of the member's project row when there is one.
- **Display** (Decision 6): one `member` line per declared member under the holder's row.
- **Evidence, never permission** (Decision 7, SY:34-37).

### Alternatives

- **Default-on traversal**: against the packet's opt-in boundary (DI:1329-1331 at `15504f1`), and
  it would change the default document feature 005 builds.
- **Calling `snapshot()`**: forbidden to the overview (APO/ov:35-36); it starts uncounted 15 s
  children (project:60-65), reads parked-work records (project:772-819) and `docker`
  (project:862-864), and refuses a whole family on one bad entry (O9).
- **A separate family phase after collection** with its own budget, like #29's remote phase
  (#29 `specs/project-overview/spec.md:431`): Decision 5.
- **Following `path:`** to the pinned copies: Decision 3.
- **Matching `repository` against a sibling's remote URL**: it needs a Git child reading
  configuration and a URL rule like #29's (#29 proposal.md:82-91); deferred.
- **Findings for member states**: Decision 4.

## Decisions for Brett Heap

1. **Is the extension opt-in, and how?** (A) A `--families` flag on `project overview` alone.
   (B) On by default. (C) A generic `--relationships` flag, later shared with parked records.
   Recommended: A. The packet makes it opt-in (DI:1329-1331 at `15504f1`); #29 sets the precedent
   of a flag whose absence leaves change 2's document untouched (#29 proposal.md:73-76); and
   `--family` already names a family folder on `project new` (project:1088), so the plural keeps
   one meaning per spelling. C would couple this change to the park extension, which is its own.
2. **What does `relationships` hold, and in which envelope?** (A) Under the flag, one object per
   declared member, `schema_version` staying 1: `{"type": "family-member", "holder": <holder
   row path>, "member": <declared name>, "declared": {"id", "path"}, "sibling": {"path",
   "path_valid_utf8"}, "state", "reason", "found_at", "row": <project row path or null>}`,
   sorted by holder path bytes, then member name; `[]` without the flag. (B) The same, with
   `schema_version` 2 in a flagged run. (C) A new envelope key `families`, `relationships` left
   `[]`. Recommended: A. The field exists with its type unchanged and a default run is byte for
   byte change 2's, as #29 keeps 1 for its opt-in fields (#29 proposal.md:738-741); `row` names
   a row by its `path`, by which `projects` is sorted (APO/ov:619), so no probe result is copied;
   rows are keyed by repository identity (APO/ov:75-76), so a row with a null `repository.root`
   needs the design to confirm that `path` names one row.
   The cost: DI:959's "always `[]` in version 1" and APO/ov:620 change, and a consumer that
   asserted `[]` sees entries only when it passes the flag. B makes the version depend on a
   flag; C leaves the reserved field unused.
3. **How deep does traversal go, and what bounds it?** (A) Declared working siblings only, one
   level beside the holder: no member's legs, no pinned copies under `members/`, no nested
   family. (B) A plus each member's legs. (C) A plus the pinned copies. Recommended: A. Legs and
   pinned copies are submodule checkouts, which change 2 gives an `unsupported-layout` repair
   error (APO/ov:97-102); pinned copies are detached by design (ORS `siblings.py:28-30`) and
   inside the holder's own checkout; a member is another project's assembly root (ORS
   `family.yaml:15-19`), which `project` too reads only as a project (project:853-854). Bounds:
   siblings count toward the 128-candidate cap after canonical sorting (APO/ov:217-222); at
   most 128 entries are read per holder, the rest one `scan-limit` with `limit:
   "family_members"` and an exact `omitted` count, the list being read whole from a manifest
   already bounded at 1 MiB (APO/ov:192-196); like every cap it makes the run incomplete
   (APO/ov:222-224).
4. **How is a missing, extra, misplaced or malformed member reported, and is it a finding?**
   States: `present` (a directory holding `project.yaml` whose `id` equals the entry's, either
   unset counting as equal); `not-a-project` (a directory without `project.yaml`, O3's `api`);
   `mismatched` (the two `id` values differ); `missing` (`lstat` gives no such entry or not a
   directory), with `found_at` naming a row elsewhere whose manifest `id` equals the entry's, from
   manifests already read and with no search (O3's `billing`); `invalid` (an entry that is not a
   mapping, a name outside `[A-Za-z0-9_-]+` as project:850, or one naming the holder, O10), the
   other entries still reported; `unknown` with a reason (a task timed out, the deadline, an OS
   error). Extras, undeclared directories in the family folder, are not reported: the folder
   also holds the estate's own files (ORS `siblings.py:16`) and listing it is the recursion the
   packet declines (DI:1789-1791 at `15504f1`). A sibling check that is cut is `unknown` and is
   also recorded as change 2 records every cut filesystem task, a `probe-timeout` or
   `deadline-exceeded` scan error that makes the run incomplete, since the sibling may be a row
   the run missed (APO/ov:186-188; APO proposal.md:152-153). As findings: (A) informational
   only, states in `relationships` and the human lines, no finding code, and no state changing
   any row's status, the summary, `completeness` or the exit. (B) A new code such as
   `family-member-missing`. (C) Findings for `invalid` and `mismatched` only.
   Recommended: A. A member not cloned is ordinary
   work (APO proposal.md:154-156) and "a project that belongs to no family is reviewed
   identically" (ORS `family.yaml:23-25`); the finding table is closed for version 1
   (APO/ov:421-422); #29 isolates its evidence the same way (#29 proposal.md:121-126). doctor's
   `error` for a missing member (project:897, O5) is untouched, so the two commands differ.
5. **What deadline and budget share does it get inside the overview's 60 s?** (A) None of its
   own: sibling checks are bounded filesystem tasks and sibling probes ordinary collection, under
   the 60 s deadline, the 5 s per child and four children at once (APO/ov:166-181, :236-238), so
   the 64 s run bound holds (APO proposal.md:483-487). (B) A family phase after collection with
   its own budget, like #29's `min(30 s, deadline - now)`. (C) A reserved slice of the 60 s.
   Recommended: A. Siblings are candidates, the candidate cap already bounds collection at the
   measured worst case of 48.3 s (APO proposal.md:598-605), and no new kind of child starts; B
   would compete with #29's phase for the same remainder. Risk: a `--families --remote` run
   leaves #29's phase less time (Risks).
6. **What is the human form?** (A) Under the holder's header, one line per declared member:
   `member` padded to 14 columns as a category is (APO design.md:516-518), then `<name>: <state>`
   and the sibling path or `found_at`; member rows keep their own headers; the lines hide under
   `--attention` as informational findings do (APO/ov:466-469); one `Families:` count line before
   the summary in a flagged run. (B) A separate section after the rows. (C) A suffix on each
   member row's header. Recommended: A. The family is read where it is declared, other rows stay
   as change 2 prints them, and #29 reads the layout as allowing added lines without a MODIFIED
   block (#29 proposal.md:1041-1044).
7. **What must `clean --all-safe` and the other commands never infer from a relationship?**
   (A) All of: no suggestion names a holder for a member's worktree, or any command across
   members, every suggestion staying per repository root (APO/ov:484-487); `--all-safe` plans
   one repository and never a sibling or member (CAS/pc:568-571) and never reads a relationship;
   a relationship changes no classification, finding, gate, row status, summary count,
   `completeness` or exit; it is kept nowhere beyond the invocation (APO/ov:714-716), so no
   `status`, `doctor`, `update` or `clean` run, `plan_digest` or revalidation can read it; no
   clone, bootstrap or fetch of a missing member is suggested, as openRepoShape owns those
   (README.md:264); and membership grants nothing (ORS `repository-naming.yaml:13-18`). (B) Rely
   on change 2's "Grouping grants nothing" (APO proposal.md:157-158) with no new scenario.
   Recommended: A, stated in the ADDED requirement with a scenario each, since SY:34-37 names
   the risk and B leaves it untested.
8. **Where is the sibling, and which key names it?** (A) `<holder parent>/<project>`, else
   `<holder parent>/<name>`, as project:849-852 reads it. (B) The declared `path:`. (C) Both.
   Recommended: A. It is where openRepoShape clones the working copy (ORS `siblings.py:12-15`)
   and where `status` already looks, so the two commands agree; `path:` is always
   `members/<project>`, the pinned copy (ORS `family.py:443-445`).
9. **Does a holder with no Git toplevel still yield relationships?** (A) Yes, from its manifest,
   its row keeping null Git fields and no error (APO/ov:66; O7). (B) No. Recommended: A: the
   members list needs no Git child, and such a holder is the case in which a person most needs
   to see the members.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

Intent only; no delta file is written (Status).

- `project-overview` (change 2's, unarchived): MODIFIED "Overview discovers projects within
  configured roots only" (APO/ov:10), for the flag's carve-out; MODIFIED "Overview prints a
  versioned JSON envelope" (APO/ov:606), for `relationships`; MODIFIED "Overview bounds its work
  and reports what it omitted" (APO/ov:166) only if Decision 3's member cap is taken, since the
  caps are listed there (APO/ov:217-218); ADDED "Overview reports family relationships on
  request". The other requirements stay untouched, "Overview renders a readable human report"
  under #29's reading (Decision 6).
- Nothing in `project-clean` or `project-clean-review-safety`; nothing in `project-command`,
  `project-review-safety` or `speckit-extension-integration`. PRS:67-71 binds `status` and
  `doctor`, which this change leaves as they are.

### Statements this change would make false

Each is true of a run without the flag and false of a flagged run:

- APO/ov:18-19: "Discovery SHALL examine each root and its immediate entries only and SHALL
  never recurse."
- APO/ov:35-37: "SHALL NOT read a family's member list" and "`relationships` SHALL be `[]`";
  the same text is A1's `spec.md:40-43` (`e4a30fc`) and feature 005's FR-003
  (`specs/005-project-overview/spec.md:2120-2122`, `6069d3a`).
- APO/ov:65, in "Family holder count, relationships and probe ownership": "`relationships` is
  `[]`, no row and no Git child exists for `acme/web` or `acme/api`".
- APO/ov:620: "`relationships`, always `[]`"; also #29's MODIFIED block (#29
  `specs/project-overview/spec.md:242`) and A1's `spec.md:692`.
- APO proposal.md:57, "a family holder is one row with `relationships: []`"; :802, "no traversal
  of members or legs"; APO design.md:75, the non-goal "Remote, family, bench, container or park
  evidence"; APO design.md:442-444, "a family holder is one row that claims no member".
- APO proposal.md:409-411 gives as a reason PRS stays untouched that the overview "renders no
  nested estate or leg": a flagged run renders member relationships, never estate snapshots,
  so PRS:67-71 stays untouched but the reason narrows.

Kept true: the holder is one row (APO/ov:36-37); its probes follow its own directory
(APO/ov:38-39); "Grouping grants nothing" (APO proposal.md:157-158). Feature records are not
edited.

## Dependencies and Sequencing

- **Change 2 and feature 005** (#10, lane openRepoProject-4). Change 2 was ratified on
  2026-10-09 (APO proposal.md:5-8) and is unarchived; feature 005 is specified on
  `005-project-overview` (`6069d3a`), builds `relationships: []` (its FR-003) and puts family
  traversal out of scope (its `spec.md:4568-4569`); it follows feature 004 (APO tasks.md:25). This
  change's realization follows feature 005's merge and change 2's archive, as #29's does (#29
  proposal.md:545-550).
- **A1, PR #34.** Brett Heap answered feature 005's Q1 to Q17 on 2026-10-21 (feature 005
  `spec.md:634-638`) and ratified A1, "ratify 34", on 2026-10-22 (A1 proposal.md:9-10). PR #34
  had not merged: main is `15504f1`, A1's merge base. A1 moves the discovery text this change
  would modify (A1 `spec.md:40-45`) and adds a family-holder clause to requirement 2 (A1
  `spec.md:94-102`; A1 proposal.md:1203-1211, Q11 A). The deltas are written on change 2's text
  with A1 merged.
- **#29, add-project-overview-remote-merge-status** (lane openRepoProject-5, draft). It MODIFIES
  "Overview prints a versioned JSON envelope", carrying "`relationships`, always `[]`" (#29
  `specs/project-overview/spec.md:228`, :242), and also "Overview bounds its work and reports what
  it omitted" (:51) and "Overview is local and read-only" (:3), and ADDS a remote phase after
  collection (:431). Lane 5's rule, stated for change 1's evidence model that it shares with #26:
  "whichever of the two archives second re-bases its block on the other's archived block before
  it archives" (L-11, #29 proposal.md:578-579; L-17, :658-662). This change would share the
  envelope requirement, and with Decision 3's cap the bounds requirement, so the same rule
  applies. No text read here orders the two; the rule makes either order safe.
- **#27 and #26.** #27 (cache disposal) MODIFIES "Overview reuses the cleanup classifier and merge
  target" (#27 `specs/project-overview/spec.md:3`), which this change does not touch: same
  capability, archive order only. #26 (branch retirement) has no `project-overview` delta (its
  deltas are `project-clean`, `project-clean-review-safety` and `project-command`): no shared
  statement.
- **Change 1** (feature 004) adds `root_valid_utf8` beside each nested family member's `root` in
  `status` and `doctor` JSON (CAS/cmd:35-36; CAS design.md:689-691); this change touches neither.
- **Why the deltas wait.** Written now, the envelope block would be re-based once on A1's merge
  and again on #29's settled block, as lane openRepoProject-1's survey of 2026-10-20 foresaw
  (its item U1). Written after both, once.

## Impact

- **`project`**: the overview's parser gains the flag; discovery reads the holder's member list
  from the manifest it already reads; bounded sibling tasks; a relationships builder; the human
  lines. No new dependency (PyYAML as today, requirements.txt:2); `status`, `doctor`, `update` and
  `clean` unchanged.
- **`README.md`**: the overview section gains the flag, the states and that a relationship never
  authorizes cleanup.
- **`tests/test_project.py`**: fixtures like `FX`'s (openRepoShape's layout, a sibling that is
  not a project, a clone outside the folder, a malformed entry, a self-named member, a holder
  with no `.git`), offline, with zero-mutation snapshots and fake owner tools first on `PATH`; CI
  runs Python 3.10 and 3.12 on `ubuntu-latest` (`.github/workflows/tests.yml:9-17`).
- **Speckit handoff**: one feature after feature 005 merges and change 2 archives, numbered at
  `/speckit.specify` time from a local main synced to `origin/main`.
- **Expected conflicts**: features 004 and 005 and #29's realization edit `project`, the tests
  and `README.md`; whichever merges second merges main in, never rebasing.

## Acceptance criteria

Candidates, each a test on Python 3.10 and 3.12:

1. Without the flag, every scenario of change 2 holds unchanged, "Family holder count,
   relationships and probe ownership" included (APO/ov:63-67).
2. With the flag over `FX`'s `acme` estate as a child of the root, `billing`'s `project.yaml`
   given `id: billing`: rows for the holder, `web`, `api`, `billing` and `tools`;
   `relationships` holds `web` `present` with `row` its row, `api` `not-a-project`, `ghost`
   `missing`, and `billing` `missing` with `found_at` its row; no row and no Git child for
   anything under `members/`.
3. With the family folder as the root, each sibling has exactly one row and one probe set, and
   `probes.performed` equals the same run's count without the flag.
4. A malformed entry (`../evil`, a non-mapping) is `invalid` and the other entries are reported;
   the exit is what the run gives without the flag, never 2 (contrast O9). A member named like
   the holder is `invalid` and the holder is probed once (contrast O10).
5. A holder with no `.git` yields its relationships and keeps null Git fields and no error.
6. 130 entries in one holder: 128 read, one `scan-limit` with `limit: "family_members"` and
   `{"count": 2, "exactness": "exact"}`, exit 1.
7. A held sibling `lstat` makes that entry `unknown` with `probe-timeout`, a `probe-timeout`
   scan error and exit 1; at the deadline, `deadline-exceeded`; the other entries are reported.
8. No relationship state changes a classification, finding, suggestion, status, summary count,
   `completeness` or exit: the same fixture with and without the flag differs only in
   `relationships` and the added sibling rows with what they add to `summary` and `probes`; no
   suggestion names a holder for a member's worktree; `project clean <holder> --all-safe`
   selects no member's worktree.
9. `--attention` hides the member lines and changes no JSON.
10. Read-only and offline: zero-mutation snapshots, no network, no fake owner tool called.

## Risks

- openRepoShape owns the layout (README.md:264); if the sibling placement moves, both `status`
  and the overview read the wrong place. The overview copies `project:852`'s rule; pinning it by
  sha, as project:204-211 pins the name forms, is the design's choice.
- Siblings add candidates, so the 128-candidate cap binds sooner and a large estate run ends
  incomplete more often, visibly.
- A `--families --remote` run leaves #29's remote phase less of the 60 s.
- `doctor` calls a missing member an `error` (O5) while the overview calls it informational.
- A consumer that asserted DI:959's "always `[]`" sees entries when it passes the flag.
- Two lanes' blocks of one requirement must be re-based in order (Dependencies).

## Out of Scope

- Any cleanup permission: `clean`'s eligibility, gates, batch and suggestions stay as change 1
  and change 2 define them (SY:34-37; CAS/pc:568-571).
- Bench, container and park integrations, and parked-work records as relationships (APO
  proposal.md:571; DI:1807-1808 at `15504f1`, one change per integration).
- Remote queries of any kind (#25, #29), the sibling's remote URL included.
- Any change to `discover`, `snapshot`, `status` or `doctor`: no observation here shows the
  overview needs one; their family readings (O3 to O13) stay as they are.
- Legs, pinned member copies and nested families (Decision 3); undeclared directories in a
  family folder (Decision 4).
- openRepoShape's family mechanics: `bootstrap`, `siblings`, `family.py` and
  `validate-family.py`, which the overview never runs (APO/ov:711).
- A command that clones, moves or repairs a member.
- The family folder itself, never a candidate: feature 005's recorded edge case EC-025, kept by
  Brett Heap's Q10 A (`specs/005-project-overview/spec.md:1868-1875`, :810-811).
