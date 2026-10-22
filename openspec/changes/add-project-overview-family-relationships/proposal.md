Lane: openRepoProject-1

# Proposal: add-project-overview-family-relationships

Status: observation record; draft; nothing here is ratified. Proposed on Brett Heap's word
"start report E's candidate 3" (2026-10-22T17:39:41Z), the third candidate of lane
openRepoProject-1's work survey of 2026-10-20. Governing issue: opensoft/openRepoProject#36,
claimed by lane openRepoProject-1 (comment 6347306957; UNVERIFIED: the id is as the claim tool
printed it, not read back, since no `gh` call was allowed; `gh api` on the comment would verify
it); refs #6, the packet's record, and #10, the overview change's issue. It records what `project`
and the packet do and say about families today and the decisions an extension of `project
overview` needs. It writes no spec delta, no `design.md` and no `tasks.md`. The hold trigger: the
ADDED requirement is written once feature 005's clarify answers land as amendment A1 (PR #34);
the MODIFIED blocks shared with #29 are not held for #29, they are re-based at archive time under
lane 5's rule (Dependencies and Sequencing). An alignment review and a council, both of
2026-10-22, are applied (the last two sections); next: Brett Heap's rulings on Tier 1, then the
design.

Citations are `file:line` at the sha named. `APO` is `openspec/changes/add-project-overview/`
(change 2, ratified, unarchived) and `APO/ov` its `specs/project-overview/spec.md`; `CAS` is
`openspec/changes/add-project-clean-all-safe/` (change 1), `CAS/pc` and `CAS/cmd` its
`project-clean` and `project-command` deltas; `PRS` is `openspec/specs/project-review-safety/
spec.md`; `project:N` is the executable. All of these are at main `15504f1`. The packet under
`ideation/brainstorm/` is `DI` (`project-maintenance-project-discovery.md`), `SY`
(`...-synthesis-inspect-and-retire.md`), `OV` (`...-overview.md`), `BA` (`...-batch-cleanup.md`)
and `HO` (`next-session-project-maintenance-fix-handoff.md`), each line with the sha it was read
at: `da33d92`, which change 2 cites, or `15504f1`, after packet revision 1 (`e45155a`). `ORS` is
the local openRepoShape checkout, read only by `git show` and never fetched, cited at
openRepoShape origin/main `038dafb`, the newest commit it holds (2026-10-21): its checked-out
HEAD, `2476992`, which earlier drafts cited, is 224 commits behind it, and `1a9fc53` is an
ancestor of it. `project:204-211` pins the naming contract at `1a9fc53`, and
`contracts/repository-naming.yaml` is byte-identical at `1a9fc53` and `038dafb` (`git diff`
empty), so its lines are cited at `038dafb` too; `1a9fc53` stays only where `project:204-211` is
quoted. Every ORS line was re-read at `038dafb` on 2026-10-22. Branch heads
after `git fetch` on 2026-10-22, fix round 1: A1 `e4a30fc`, feature 005 `41cf866`, and the
branches of #29 `a529310`, #27 `9473b2c` and #26 `6c7c0f9`; every line cited on those branches
was re-read at those heads. Feature 005's head has since moved to `6637e6e`; the council found
that its one new family-holder phrase concerns `clean`'s bare-name redirect and not the overview
(council-adversary.md, header), so its lines stay cited at `41cf866`. `F005` is feature 005's
`specs/005-project-overview/spec.md` at `41cf866`. The council's reports and verdicts are in
`/workspace/projects/.scratch/openRepoProject-1-wave6-20261022/`: `council-product.md`
(PA-1 to PA-4), `council-architect.md` (SA-1 to SA-4), `council-adversary.md` (AE-1 to AE-5)
and `council-verdicts.md`.

## Why

Change 2 shows a `family.yaml` holder as exactly one row of kind `family-holder`; it never reads
the members list, and the envelope's `relationships` is always `[]` (APO/ov:35-40, :620;
DI:276-282 at `da33d92`, DI:331-337 at `15504f1`). In openRepoShape's layout a member's working
clone sits beside the holder, `<Family>/<Project>`, with the holder at `<Family>/<Family>` (ORS
`templates/family-root/scripts/siblings.py:12-16`, `038dafb`). The marker
`D/<name of D>/family.yaml` makes the holder the candidate, never `D` (APO/ov:24-30), and
discovery never recurses (APO/ov:18-19), so in that layout no member's working clone is a
candidate unless the family folder itself is given as a root (APO/ov:67). From the overview a
person cannot see which members a family declares, which are present, missing or out of place,
or which other rows belong to it.

The packet bounds the work twice. Family relationships share the deferred boundary of the remote
and bench extensions: "opt-in probes, bounded time, explicit unknown values, and no mutation"
(DI:1062-1064 at `da33d92`, DI:1329-1331 at `15504f1`). And "Family grouping, when added later,
does not grant permission to clean every sibling" (SY:34-37 at both shas). Change 2 leaves family
traversal to its own proposal (APO proposal.md:569-570; OQ-27, :631), which this is.

The need today, on this workstation (council-product.md, Concern 1; read-only, by a script that
applies the ratified marker table, APO/ov:24-30, since no overview exists, O2): one live family,
InkRouter, whose holder `InkRouter/InkRouter/family.yaml` declares `IRRS` and `IRSS`, both Git
repositories holding `project.yaml` beside the holder, `IRRS` with one linked worktree. A
default-root run does not show them: the script counted 255 candidates against the cap of 128
(219 on 2026-10-09, APO proposal.md:598-605; the stack-architect counted about 251 on
2026-10-22, council-architect.md, Concern 1). `--root /workspace/projects/InkRouter` already
yields three rows, the holder, `IRRS` and `IRSS` (APO/ov:67), with no extension at all. That
workaround, and the scope it leaves open, is Decision T1-0.

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
(project:823-826) fires through a family only when two entries name one directory, which refuses
the whole command as one malformed entry does (O9, O15).

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
| ORS `contracts/repository-naming.yaml:13-18`, `:373-398` (`038dafb`) | names confer nothing; "A consumer deriving a permission from a family id is defective"; a holder pins members' assembly roots as submodules under `members/`; "membership is navigation" |
| ORS `templates/family-root/family.yaml:15-25`, `:63-65` (`038dafb`) | each member is "a whole project in its own right"; `members_dir: members`; "A consumer deriving a permission from membership is defective" |
| ORS `scripts/family.py:836-838`, `:909-918` (`038dafb`) | a member row is `project`, `id`, `repository`, `path: members/<project>`, `pin` |
| ORS `templates/family-root/scripts/siblings.py:28-34` (`038dafb`) | two copies: the pinned, detached one under `members/` for bootstrap and validate, and the sibling "where a human works" |

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
`family.yaml` declares `web`, `api`, `ghost` and `billing`, each with `id: <name>` and
`path: members/<name>`, and holds `members/web/project.yaml`; `acme/web`, a repository with
`project.yaml` and a leg `spec`; `acme/api`, a repository with no `project.yaml`; no
`acme/ghost`; `billing`, a repository with `project.yaml` cloned beside the family folder;
`tools`. Three more estates: `FX/projects-nogit`
(`beta/beta/family.yaml`, no `.git`), `FX/projects-bad` (`gamma/gamma`, member `../evil`) and
`FX/projects-self` (`delta/delta`, a repository whose member is `delta`). Fix round 1 added, by
`FX/scripts/build2.sh` and `FX/scripts/run2.sh` under the same command line: `FX/projects-dup`
(`dup/dup` lists `web` twice), `FX/projects-badkind` (`zeta/web/project.yaml` of `kind: other`),
`FX/projects-notlist` (`eps/eps`'s `members` a mapping), `FX/projects-link` (`eta/web` a link to
`../outside`, out of the family folder) and `FX/projects-link-in` (`theta/web` a link to
`theta/web-real`). Their digest was `5e6e98efaa53ebf9` before and after, no fake owner tool was
called, and each 3.10 output equalled its 3.12 output. The stack-architect's review reproduced
O1 to O14 and ran O15 to O18 on its own fixture. The council found two flaws in `FX`'s `acme` as
a model of openRepoShape's layout, which the runs O3 to O19 do not use but criteria 2 to 22 do:
its holder's `family.yaml` has `name: Acme` and no `repository:`, so openRepoShape's family
folder name is `Acme`, not the folder's `acme` (AE-2, council-adversary.md; Decision T1-7), and
`acme/web/project.yaml` has no `id`, which openRepoShape reads as `None` against the entry's
`id: web` (AE-3; Decision T1-4).

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
| O15 | `FX/projects-dup` | `status dup --json`; `status dup`; `doctor dup --json` | 2 / 2 | `{"error": "Cyclic estate membership at FX/projects-dup/dup/web"}`; `REFUSED: Cyclic estate membership at FX/projects-dup/dup/web` |
| O16 | `FX/projects-badkind` | `status zeta --json` | 2 / 2 | `{"error": "Unexpected kind in FX/projects-badkind/zeta/web/project.yaml; expected project-manifest"}` |
| O17 | `FX/projects-notlist` | `status eps --json` | 2 / 2 | `{"error": "Expected a list of legs/members in FX/projects-notlist/eps/eps"}` (project:836-837) |
| O18 | `FX/projects-link` | `status eta --json` | 2 / 2 | `{"error": "Path escapes its owner FX/projects-link/eta: web"}` (project:51-57, :852) |
| O19 | `FX/projects-link-in` | `status theta --json` | 0 / 0 | the member is a full snapshot rooted at `FX/projects-link-in/theta/web-real`, the link's target |

Not run: `new`, `update`, `clean` and `benches`; `doctor --validate` with a validator present,
which would execute it (project:963-967); and `project overview`, which does not exist at
`15504f1` (O2), so every overview behaviour cited here is ratified text, not an observation.

The runs show: a present clone that is not a project (`api`) and a clone outside the family
folder (`billing`) read exactly as an absent member (`ghost`), and doctor calls all three an
`error` (O3 to O5); one malformed entry, a repeated entry, a wrong-kind sibling manifest, a
non-list `members` or a link out of the folder refuses the whole family with exit 2 (O9, O15 to
O18), while a link inside the folder is read at its target (O19); a member named like the holder
points at the holder (O10); the pinned copies under `members/` are never read (O3); one
directory is both a member and a project with nothing linking the two (O3, O11), and from a
member's own directory nothing names its family (O13).

## What Changes

Candidates, not requirements; each open point is a Decision below. Decisions are numbered by tier:
T1-n is ruled now, T2-n at design time (Decisions for Brett Heap).

- **Opt-in** (T1-1): `project overview --families`; without it the document and report are
  change 2's, byte for byte.
- **Scope** (T1-0). Recommended: relationships only. `--families` reports the declared members
  and their states and changes no row; a member's working clone gets a row only where the family
  folder is a root (APO/ov:67), as today. Member clones as rows would change the base document
  and are their own later change, if wanted at all.
- **Membership from the holder's own manifest.** The `members` list of the holder's
  `family.yaml`, the manifest change 2 reads only for name and kind (APO/ov:319-320; DI:333-335
  at `15504f1`), and the `id` of each sibling's `project.yaml`: fields change 2 never reads
  (Statements this change would make false). Where the holder's read runs is T1-2. Each entry
  names a working sibling at `<holder parent>/<project>` (T2-4); `id` and `path` are reported as
  declared, `path` and `pin` never followed.
- **The family-folder test** (T1-7). Siblings are read only when the holder's parent folder is
  the family folder as openRepoShape defines it: the folder is named after the family, that is
  the basename of the holder manifest's `repository:`, else its `name:` (ORS
  `templates/family-root/scripts/siblings.py:1316-1334`, `038dafb`), or the family folder is
  reached through a link of that name beside it that leads to the folder (`family_link`,
  `:1372-1397`). Where neither holds, openRepoShape warns, prints the `mv` and stops with exit 1
  before anything is cloned (`parent_folder_warning`, `:1417-1461`; the stop, `:1718-1726`). The
  holder's relationships are then `unknown`, with reason `not-in-family-folder`, and no sibling
  is read. Sibling reads also stay inside the configured roots (T1-7): a sibling outside every
  root is `unknown`, reason `outside-roots`.
- **Traversal one level, inside bounds** (T1-3, T2-2, T1-2, T2-1). Each declared sibling is
  examined by bounded filesystem tasks (one link resolution, a `stat`, the marker checks, the
  manifest read). Under the recommended scope no sibling becomes a candidate: a sibling that
  already has a row, because the family folder is a root or the sibling is an immediate entry of
  one, is joined to its entry by `row` and is probed once, as any candidate is, with nothing
  added (DI:1783-1785 at `15504f1`). Under T1-0 B a sibling that is a candidate joins the
  candidate list where T1-2 A places it.
- **Relationships** (T2-1, T1-4, T2-5): one entry per declared member in the envelope's
  `relationships`, with a state (`present`, `not-a-project`, `mismatched`, `missing`, `invalid`,
  `unknown`) and the `path` of the member's project row when there is one.
- **Paths and strings, as the envelope requires** (candidate requirement). Every path in an entry
  carries its own validity flag: `holder_valid_utf8`, `sibling.path_valid_utf8`,
  `found_at_valid_utf8` and `row_valid_utf8`, each null only beside a null path (APO/ov:666-670).
  `member`, `declared.id` and `declared.path` follow A1's rule for every other string the report
  takes from a manifest (A1 `spec.md:748-752`), a non-string `id` or `path` being reported null.
  A `member` line prints its paths as the report prints every path, in the `$'...'` form where
  one needs it (APO/ov:672-675), and its name by A1's string rule. Each new row-error or
  `scan-limit` message takes a fixed text in A1's table (A1 `spec.md:385-390`, :402).
- **Isolation** (candidate requirement). A sibling's own failure, its marker check or manifest
  read, stays on its entry as a state; a sibling that is also a row keeps that row's own errors
  (APO/ov:322-324, :342-343); relationships change no row. Whether a cut or capped family check
  is also recorded on the holder's row and the run's completeness is T1-6; the recommendation is
  that it is not. The isolation requirement (APO/ov:317-347) and `project-review-safety`'s
  manifest carve-out (APO `specs/project-review-safety/spec.md:9-12`) are read as they stand,
  not modified.
- **Display** (T2-3): one `member` line per declared member under the holder's row, and a
  rendered sketch of the report there, marked illustrative.
- **Evidence, never permission** (T1-5; SY:34-37; OV:395-397 at `15504f1`).

### Alternatives

- **Default-on traversal**: against the packet's opt-in boundary (DI:1329-1331 at `15504f1`), and
  it would change the default document feature 005 builds.
- **Calling `snapshot()`**: forbidden to the overview (APO/ov:35-36); it starts uncounted 15 s
  children (project:60-65), reads parked-work records (project:772-819) and `docker`
  (project:862-864), and refuses a whole family on one bad entry (O9).
- **A separate family phase after collection** with its own budget, like #29's remote phase
  (#29 `specs/project-overview/spec.md:431`): T2-2.
- **Following `path:`** to the pinned copies: T1-3.
- **Matching `repository` against a sibling's remote URL**: it needs a Git child reading
  configuration and a URL rule like #29's (#29 proposal.md:82-91); deferred.
- **Findings for member states**: T1-4.
- **`--root <family folder>`**, which exists today and needs no extension: with the family folder
  as a root, the holder and every member clone are rows (APO/ov:67; three rows for InkRouter,
  council-product.md, Concern 1). It shows no relationship, no `missing` member and no mismatch.
  It is the workaround that T1-0 C would document, and what T1-0 A leaves in place.
- **An implicit family-folder root** (PA-1; T1-2 D): with `--families`, a holder's parent folder
  is listed as one more root after the first pass, so that members get rows by the ordinary
  marker rule and `relationships` is computed from the rows present plus one `lstat` per
  declared name. It reuses the ratified root listing, markers, caps and deduplication, and reads
  no member list before the cap. Its cost: undeclared candidates in the family folder also
  become rows, against T1-4's "extras are not reported"; it makes `--families` change the rows,
  as T1-2 A does; and the product advocate notes that reading the family folder as a root needs
  Brett Heap's ruling against feature 005's recorded edge case EC-025 (F005 `spec.md:1871-1878`;
  council-product.md, Concern 1).

## Decisions for Brett Heap

Two tiers (PA-3). **Tier 1, rule now**: the scope and the questions that decide what this change
is; the design waits for them. **Tier 2, design constraints**: each is recorded with a
recommendation and is ruled at design time; until then it constrains the design, and
`clarifications.md` records the council's constraints beside them. Identifiers are T1-n and
T2-n; the earlier drafts' numbers map as follows.

| Earlier | Now | Subject |
| --- | --- | --- |
| (new) | T1-0 | scope |
| 1 | T1-1 | opt-in |
| 10 | T1-2 | member clones as rows; where sibling expansion runs |
| 3 | T1-3 | traversal depth |
| 4 | T1-4 | member states, and findings |
| 7 | T1-5 | evidence, never permission |
| (new; the council's "Decision 13") | T1-6 | is a cut or capped family check incomplete |
| (new) | T1-7 | the family-folder test, and reach outside the roots |
| (new) | T1-8 | `status` and `doctor` against the overview |
| 2, 11, 12 | T2-1 | envelope shape: entries, holder entry, caps (merged) |
| 5 | T2-2 | deadline and budget |
| 6 | T2-3 | human form |
| 8 | T2-4 | sibling placement and link resolution |
| 9 | T2-5 | holders, and a bad member list |

**The hold trigger.** The ADDED requirement, "Overview reports family relationships on request",
is written once PR #34 (A1) merges, in the shape that Brett Heap's Tier 1 rulings fix. The
MODIFIED blocks, which share requirements with #29, are written on the same text and are
re-based at archive time under lane 5's rule, "whichever of the two archives second re-bases its
block on the other's archived block before it archives" (#29 proposal.md:578-579; L-11 and L-17,
:658-662; Dependencies and Sequencing says how this change takes the rule over). No block waits
for #29 to settle.

**The recommended set.** T1-0 A, T1-2 C, T1-6 A, T2-1 B, T2-2 B. They depend on one another: a
cut family check that stays out of the holder's row (T1-6 A) needs the check outside the
per-candidate boundary (T2-2 B), and relationships that change no row (T1-0 A) are what let T1-6 A
promise a run equal to the plain run. A ruling the other way on one can change another's
recommendation, and the Decision says so where it does.

### Tier 1: rule now

**T1-0. Scope: what is this change for?** Both sides of one argument are right about different
things. The product advocate (PA-1): the pain is that a member's working clone, its Git health
and its worktrees never reach the attention report; relationships are informational and hide
under `--attention`, so the visibility comes only from member clones becoming rows (T1-2 A). The
stack-architect and the adversary (SA-1, AE-1): T1-2 A, the option that makes member clones rows,
breaks ratified guarantees: the two-pass cap and the discovery-time manifest read (APO/ov:224-229,
:243-249, :322-324); a family's siblings push unrelated rows out of the cap on every default-root
run of this estate (219 candidates on 2026-10-09, APO proposal.md:598-605; about 251 and 255 by
two counts of 2026-10-22, against a cap of 128); and #29's promise that a `--remote` run agrees
with the plain run on every row, error and exit (#29 `specs/project-overview/spec.md:546-557`).

- (A) Relationships only (T1-2 C): `--families` reports each holder's declared members and their
  states and changes no row, summary count, `completeness` or exit. Member clones as rows become
  their own later change, if wanted at all, because they change the base document; the workaround
  that exists today is `--root <family folder>` (Alternatives).
- (B) Relationships plus member rows (T1-2 A), with the five constraints the adversary lists
  (AE-1): a family enters and leaves the cap as a unit, a holder past the cap taking its siblings
  with it and no sibling kept without its holder; the candidate cap's `omitted` is `lower-bound`
  whenever a holder's read was cut or a holder past the first cap was never read; there is one
  holder entry per row, from the manifest the row's collector reads at `repository.root`, the
  discovery read only scheduling siblings; the dispatch rule is stated (wait for the final list,
  or start early and keep displaced candidates' children out of `probes`) and measured; and
  APO/ov:224-229, :243-249 and :322-324 are listed in Statements this change would make false.
- (C) No extension now: document `--root <family folder>` in README.md, and revisit when a second
  family exists (council-product.md, Concern 1).

Recommended: A. B delivers the member visibility that the product advocate asks for, at the price
of the guarantees above. A keeps every row, error and exit equal to the plain run (T1-6) and
leaves member rows to a change that can measure them and rule on displacement. C is the fallback
if Brett Heap wants no extension while this estate holds one family.

**T1-1. Is the extension opt-in, and how?** (A) A `--families` flag on `project overview` alone.
(B) On by default. (C) A generic `--relationships` flag, later shared with parked records.
Recommended: A. The packet makes it opt-in (DI:1329-1331 at `15504f1`); #29 sets the precedent of
a flag whose absence leaves change 2's document untouched (#29 proposal.md:73-76); and `--family`
already names a family folder on `project new` (project:1088), so the plural keeps one meaning per
spelling. C would couple this change to the park extension, which is its own.

**T1-2. Do member clones become rows, and where does sibling expansion run in the ratified
pipeline?** In change 2 the holder's manifest is read inside its collector, after the identity
probe (DI:627-637 at `15504f1`, DI:515-525 at `da33d92`; APO/ov:318-320), and candidates are
sorted and capped before collection is dispatched (APO/ov:32-34, :221-222; APO design.md:385-386),
so the members list is not known when the candidate list is final.

- (A) Discovery sorts and caps once, reads the manifest of each holder that survives the cap in
  one bounded task (at most 128, each waited for as APO design.md:450-452 and :456-460 wait a
  manifest read), adds the declared siblings, sorts again and applies the candidate cap again; a
  candidate a sibling displaces joins the candidate cap's `omitted` count, and a sibling past the
  cap is `unknown` with reason `candidate-cap`; the holder's collector reuses the result. This
  departs from DI:627-637 and from APO design.md D2 (:134-137, the root task lists and checks
  markers only), D6 (:385-386) and D8 (:454-460).
- (B) Siblings join after the cap, as candidates outside it, bounded only by T2-1's caps: no
  departure in discovery, but the 128-candidate cap no longer bounds the Git work that the 48.3 s
  measurement covers (APO proposal.md:598-605).
- (C) Siblings never become candidates unless they are immediate entries of a root: relationships
  come from the sibling checks and from rows already present, and `row` is joined after
  collection from the rows already built, with no departure. In openRepoShape's layout the member
  clones then get no row (Why) unless the family folder is given as a root (APO/ov:67).
- (D) With `--families`, a holder's parent folder is listed as an implicit root (PA-1;
  Alternatives), so that members get rows by the ordinary marker rule: no discovery-phase
  manifest read and no second cap, but undeclared directories in the family folder also become
  rows, and the flag changes the rows.

Recommended: C, for this change (T1-0 A); the earlier draft recommended A. Reasons (SA-1, AE-1;
council-architect.md and council-adversary.md):

- A is the only option that moves a ratified invariant, the candidate list being final before
  collection, and it contradicts the isolation this record claims. A candidate that a sibling
  displaces changes `projects`, `summary`, `scan_errors`, `completeness` and the exit, where
  "relationships change no row" (What Changes), T1-5 and criterion 11 promise none; the candidate
  cap's `omitted` could not be called exact where siblings were never enumerated (APO/ov:224-229);
  one holder's cut read adds and removes other rows (APO/ov:322-324); and a candidate displaced
  after it started would have its children counted in `probes.performed`, unless dispatch waits
  for the final list (APO/ov:243-249). The adversary modelled A step by step as worded here, a
  model of these words and not of code, since no overview code exists (O2): with 120 single
  candidates, a holder `/p/m/m` declaring twelve members and ten more candidates, the second cap
  kept eight members as rows and dropped the holder itself, displacing seven ordinary candidates,
  because a sibling sorts before its holder by bytes (APO/ov:32-34; AE-1).
- The cap already binds on this estate: 219 candidates on 2026-10-09 (APO proposal.md:598-605),
  about 251 and 255 on 2026-10-22 (T1-0). Displacement is the normal case, not a corner: the one
  family's two members, near index 10, push two tail candidates out of a default-root run, 127
  omitted becoming 129 (council-product.md, Concern 3).
- A reads Why more widely than Why says. Its last sentence lists what a person cannot see:
  members declared, present, missing, out of place, and which other rows belong to a family. C
  answers all of it (`state`, `found_at`, `row`), and a member clone's Git health is one flag
  away, `--root <family folder>` (APO/ov:67).
- The packet's words favour C: family relationships "represented as relationships without
  duplicate checkout probes" (DI:1783-1785 at `15504f1`), and each extension keeps its owner's
  boundary (OV:185-190 at `15504f1`).
- #29 sets the stronger contract for its opt-in: a `--remote` run and the same run without it
  agree on every classification, finding, row status, row error, scan error, summary count,
  `completeness` and exit status (#29 `specs/project-overview/spec.md:546-557`). Under A the
  families extension cannot promise that; under C with T1-6 A it can.

Member clones as rows become their own later change, with an OQ-4-style measurement (APO
tasks.md:20) and a ruling on displacement. Under C, `candidate-cap` has no use and `merged-row`
arises only for a sibling that is already a candidate (the design confirms the candidate-to-row
map that the `row` join needs, which APO design D7 does not keep; council-architect.md, lesser
observations). If A is ruled, T1-0 B's five constraints apply, with `clarifications.md`. D's cost
is in Alternatives.

**T1-3. How deep does traversal go?** (A) Declared working siblings only, one level beside the
holder: no member's legs, no pinned copies under `members/`, no nested family. A sibling that is
itself a holder is a row of kind `family-holder` where it has a row (APO/ov:24-30), its own
members are not read, and its entry is `invalid` with reason `nested-family` (PA-4): a holder in
a member slot breaks openRepoShape's contract that each member is "a whole project in its own
right" (ORS `templates/family-root/family.yaml:15-25`, `038dafb`). (B) A plus each member's legs.
(C) A plus the pinned copies. Recommended: A. Legs are mounted as submodules of their assembly
root (ORS `contracts/repository-naming.yaml:348-360`, `038dafb`) and pinned copies are submodules
of the holder (ORS `contracts/repository-naming.yaml:392-393`; ORS
`templates/family-root/family.yaml:15-17`, `038dafb`); change 2 gives a submodule checkout an
`unsupported-layout` repair error (APO/ov:97-102); pinned copies are detached by design (ORS
`templates/family-root/scripts/siblings.py:28-31`, `038dafb`) and inside the holder's own
checkout; a member is another project's assembly root (ORS
`templates/family-root/family.yaml:15-19`), which `project` too reads only as a project
(project:853-854). The bounds are T2-1's.

**T1-4. How is each member's state reported, and is it a finding?** Candidate states, one per
entry, with `reason` a closed enum that is null unless listed:

- `present`: the sibling, its one link resolved (T2-4), holds `project.yaml` and its `id` passes
  openRepoShape's id test as the owner has it. `verify_sibling` compares the two ids as strings,
  `str(row.get("id")) != identity`, where `project_id()` returns `str(data.get("id"))`: a clone
  whose `project.yaml` has no `id` key reads `'None'`, so it is WRONG PROJECT against an entry
  with `id: web`; an entry with no `id` against a clone with no `id` passes; an entry with no
  `id` against a clone that has one does not (ORS
  `templates/family-root/scripts/siblings.py:755-779`, `:868-876`, `038dafb`; AE-3 and SA-4 ran
  it). An earlier draft of this record said
  the opposite, that a clone with no `id` passes. The test uses the raw YAML values; the null
  that A1's rule reports for a non-string `id` (What Changes) is a reporting rule only. PyYAML
  types bare ids as YAML 1.1 does (`on` reads True, `No` False, `0x1F` 31, `1_000` 1000, `2026`
  an integer; run on Python 3.12.3 with PyYAML 6.0.3), where openRepoShape's own reader types
  only null, booleans, integers and floats and keeps `on`, `0x1F` and `1_000` as text (ORS
  `scripts/repo_shape.py:596-613`, `038dafb`); openRepoShape writes a bare id only where its
  reader reads it back as that text (ORS `scripts/family.py:785-816`). So the test as the
  overview would apply it can say `mismatched` where openRepoShape passes, if it compares a value
  that went through the null rule or through the other reader; the design settles which values
  it compares, with a parity test (`clarifications.md`). `present` is weaker than
  `verify_sibling`, which first requires the clone's `origin` to name the row's `repository`
  (`:857-867`), a test this change defers (Alternatives), so a `present` sibling can still be a
  clone of another repository. It also differs where the clone holds no `project.yaml`, or one
  that does not load: openRepoShape's identity is then None and passes the id test (`:755-777`),
  where the overview says `not-a-project`, or `unknown` with `manifest-invalid`. The design
  mirrors the test as it stands, or names the state otherwise, so that `present` does not claim
  the owner's verdict (SA-4).
- `not-a-project`: a directory without `project.yaml` (O3's `api`), which may still be a row of
  kind `single` (APO/ov:29-30).
- `mismatched`: the id test fails.
- `missing`: the resolved path does not exist or is not a directory; `found_at` names a row
  elsewhere whose manifest `id` equals the entry's, from manifests already read and with no
  search (O3's `billing`), else null. `found_at: null` means "not found among the rows read", and
  no more: it is a negative only over those rows (PA-4). Where the run has a `scan-limit` scan
  error that can have left such a row unread (the candidate cap, a root's entry cap, or an
  unreadable or deadline-cut root listing; APO/ov:222-229), the entry is `unknown`, not
  `missing`, with reason `scan-limit`, since "no clone elsewhere" is not established (null means
  unknown or not established, APO/ov:652-653). The cost: on this estate the cap binds in every
  default-root run (T1-0), so there a member with no sibling directory would read `unknown`,
  never `missing`. Two rows can share one id, since independent clones stay separate rows
  (APO/ov:53-56); the tie rule is open to the design (T2-1; `clarifications.md`).
- `invalid`: `not-a-mapping`; `bad-name`, no `project` or `name`, a non-string (a member named
  `No` or `On` is a valid Triad name, project:208, and PyYAML reads it as a boolean), or one
  outside `[A-Za-z0-9_-]+` (project:850); `names-holder` (O10); `duplicate`, a name an earlier
  entry took, the first kept, where `status` refuses the whole family (O15; project:823-826);
  `outside-folder`, a link whose target leaves the holder's parent, where `status` refuses (O18);
  `link-loop`, a link that loops (AE-4): `Path.resolve()`, which `inside()` calls (project:54),
  raises `RuntimeError`, not an `OSError`, so the overview resolves with
  `os.path.realpath(strict=True)`, which raises `OSError` with errno 40 (ELOOP), both run on
  Python 3.12.3 (`status` itself crashes on such a link: Out of Scope); `nested-family`, a
  sibling that is itself a holder (T1-3).
- `unknown`: `manifest-invalid`, the sibling's own manifest refused (unreadable, malformed, wrong
  kind, invalid text, over 1 MiB, or no YAML library), the refusal staying on the sibling's own
  row (APO/ov:326-347; F005 FR-023, `spec.md:2592-2598`), where `status` refuses (O16), and the
  holder whose directory holds both manifests (T2-5); `probe-timeout`, `deadline-exceeded` or
  `os-error`, the check cut or failed; `candidate-cap` (T1-2 A only), `member-cap` or
  `check-cap`, the check never made (T1-2, T2-1); `scan-limit`, above; `not-in-family-folder` and
  `outside-roots` (T1-7).

A sibling whose repository identity joins another row, such as a linked worktree of another
repository, merges into that row (APO/ov:342-343): `row` names that row, and `reason` is
`merged-row` beside its state. Extras, undeclared directories in the family folder, are not
reported: listing the folder reads one level below a root's immediate entries, which APO/ov:18-19
bars, and the folder also holds the estate's own files (ORS
`templates/family-root/scripts/siblings.py:16`, `038dafb`); the packet prefers bounded discovery
with explicit additional roots (DI:1789-1791 at `15504f1`).

Two effects stay apart. A member's state is informational: no state changes any row's status, the
summary, `completeness` or the exit. Whether a cut or capped family check is incompleteness is
T1-6. As findings: (A) informational only, states in `relationships` and the human lines, no
finding code. (B) A new code such as `family-member-missing`. (C) Findings for `invalid` and
`mismatched` only. Recommended: A. A member not cloned is ordinary work (APO proposal.md:154-156)
and "a project that belongs to no family is reviewed identically" (ORS
`templates/family-root/family.yaml:23-25`, `038dafb`); the finding table is closed for version 1
(APO/ov:421-422); #29 isolates its evidence the same way (#29 proposal.md:121-126). doctor's
`error` for a missing member (project:897, O5) is untouched, so the two commands differ (T1-8).

**T1-5. What must `clean --all-safe` and the other commands never infer from a relationship?**
(A) All of: no suggestion names a holder for a member's worktree, or any command across members,
every suggestion staying per repository root (APO/ov:484-487); `--all-safe` plans one repository
and never a sibling or member (CAS/pc:568-571) and never reads a relationship; a relationship
state changes no classification, finding, gate, row status, summary count, `completeness` or
exit (under T1-6 B, the incompleteness that a cut or capped family check records excepted); it
is kept nowhere beyond the invocation (APO/ov:714-716), so no `status`, `doctor`, `update` or
`clean` run, `plan_digest` or revalidation can read it; no clone, bootstrap or fetch of a missing
member is suggested, as openRepoShape owns those (README.md:264), T1-8 asking whether prose may
point at that tool; and membership grants nothing (ORS `contracts/repository-naming.yaml:13-18`,
`038dafb`). (B) Rely on change 2's "Grouping grants nothing" (APO proposal.md:157-158) with no new
scenario. Recommended: A, stated in the ADDED requirement with a scenario each, since SY:34-37
names the risk, the packet holds that "No layout or family membership changes authority"
(OV:395-397 at `15504f1`), and B leaves it untested.

**T1-6. Does a cut or capped family check make the run incomplete?** (A) No: a cut or capped
check stays in the entry (`unknown` plus its reason) and in the envelope's family evidence
(T2-1), as #29's remote evidence stays in its own object. It is no row error, no scan error and
no change to `completeness` or the exit, so under T1-0 A a `--families` run agrees with the plain
run on every row, error and exit, as #29 requires of `--remote` (#29
`specs/project-overview/spec.md:546-557`; a remote failure "SHALL never be a row error, a scan
error or a finding", :552-556). (B) Yes: a cut check records `probe-timeout` or
`deadline-exceeded` on the holder's row, as change 2 records a cut row task (APO/ov:183-188),
and the row's status becomes `error` (APO/ov:341-342); a scan error stays for what change 2
makes one, a cap (APO/ov:222-224) and the deadline's count of candidates not started
(APO/ov:180-181), and here a family cap too, a `scan-limit` with an exact `omitted`; either
makes the run incomplete (APO/ov:654-655), so it exits 1 (APO/ov:762-764); the entry keeps its
`unknown` state. B is what the fix round of this record
wrote after QA-13. Recommended: A (SA-1). An informational feature should not turn the holder's
row to `error`, add scan errors or exit 1 because one member's mount is slow; B lets a failure on
another candidate's directory change this candidate's row, which APO/ov:322-324 forbids for a
failure in another candidate. A is coherent with T2-2 B, a family phase outside the
per-candidate boundary. Under T1-0 B (member rows) A cannot promise the plain run's rows.

**T1-7. May a sibling read reach beyond openRepoShape's family folder, or outside every
configured root?** The family-folder test (What Changes) is the owner's: a holder whose parent
folder is not the family folder reads no sibling, and its relationships are `unknown` with reason
`not-in-family-folder`. Without the test, T2-4's `<holder parent>/<project>` is wrong for a holder
cloned flat under a root (marker `D/family.yaml`, APO/ov:28, where every declared name is looked
up among the root's own projects, so an unrelated `api` holding `project.yaml` would be
`present`) and for a family whose `--name` differs from its repository (#629; ORS
`templates/family-root/scripts/siblings.py:18-26`, `038dafb`) (AE-2). The question for Brett
Heap is the reach.

- (A) No: a sibling whose directory lies outside every configured root, as when `--root` is given
  at a holder and the holder's parent is not a root, is not read, and its entry is `unknown` with
  reason `outside-roots`.
- (B) Yes: siblings are read wherever the holder's parent is, with APO/ov:10-19 ("within
  configured roots only") MODIFIED to say so. Under T1-2 A they would also get rows, Git
  children, findings and `project clean <sibling> --all-safe` suggestions (APO/ov:494-498) for
  directories the person never configured.

Recommended: A. The requirement is titled "Overview discovers projects within configured roots
only" (APO/ov:10); openRepoShape owns the family layout (README.md:264) and the packet says each
extension keeps its owner's boundary (OV:185-190 at `15504f1`); and a `family.yaml` from someone
else's repository should not decide which directories the overview reads (AE-2). The cost:
`--root <holder>` gives the holder's row and entries that are all `unknown`, `outside-roots`;
the family folder as a root gives the relationships.

**T1-8. Should the overview read a family as `status` and `doctor` do?** The three commands
differ today, and this change would keep them so. `doctor` calls a missing member an `error` and
says "use the estate's bootstrap/siblings command" (project:893-897; O5); `status` shows it as
`present: false` (O3, O4) and refuses the whole family on one bad entry (O9, O15 to O18); the
overview reports the entry and goes on (T2-4), as information. The question is the next step:
should the overview's `missing` carry the same pointer? (A) No: `missing` is a state with no next
step, and the divergence is stated and accepted; the overview reports, openRepoShape and
`doctor` repair. (B) Yes: the `member` line of a `missing` member carries the same prose as
`doctor` (project:897), a pointer at openRepoShape's tool with no argv and no
`suggested_command`, still informational; T1-5 A then needs a prose exception. Recommended: A (no
council verdict gave one). T1-5 A already says that no clone, bootstrap or fetch of a missing
member is suggested, as openRepoShape owns those (README.md:264); A keeps the overview to what it
observes, and the Risks line becomes a divergence that Brett Heap has accepted. B stays open if
he wants the two commands to speak alike.

### Tier 2: design constraints, ruled at design time

**T2-1. Envelope shape: where do the entries, the holder entry, the counts and the caps live?**
This merges the earlier Decisions 2, 11 and 12, which interlocked: Decision 2 A embedded Decision
12's holder entry, and Decision 11 (i) and (iii) and Decision 12 C each edited #29's "only
exceptions" sentence (#29 `specs/project-overview/spec.md:282-287`), so that "2 A + 11 (iii) +
12 A" could be ruled and was incoherent (SA-3). Three bundles:

- (A) The split, as drafted before the council. `schema_version` stays 1. Under the flag,
  `relationships` holds one object per declared member, `{"type": "family-member", "holder":
  <holder row path>, "holder_valid_utf8", "member": <declared name or null>, "declared": {"id",
  "path"}, "sibling": {"path", "path_valid_utf8"}, "state", "reason", "found_at": <row path or
  null>, "found_at_valid_utf8", "row": <project row path or null>, "row_valid_utf8"}` (What
  Changes, paths and strings), and one holder entry per holder examined, `{"type":
  "family-holder", "holder", "holder_valid_utf8", "members": <count or null>, "state",
  "reason"}`, state `examined`, `invalid` or `unknown` (T2-5); sorted by holder path bytes, the
  holder entry first, then by member name bytes, then by declared index, an entry with no name
  after the named ones; `[]` without the flag, where, with `family-holder` rows in `projects`, no
  holder entry means not examined and a holder entry with `members: 0` means none declared. The
  caps are `limits.family_members` and `limits.family_checks` in a flagged run only: additive
  within version 1 (APO/ov:656-658; APO design.md:563-564), but one more exception to "exactly
  these fields, every one always present" (APO/ov:610-614) beside #29's two `remote` keys (#29
  `specs/project-overview/spec.md:282-287`), so criterion 11's flagged differences name them.
- (B) One optional top-level `families` object, as #29's single `remote` object (#29
  `specs/project-overview/spec.md:526-542`): present only under `--families` and absent, not
  null, without it; it holds `examined: true`, the holder and member counts, its own `limits`
  (the caps), its own `completeness` and its `counts` by state, as #29's `remote` carries its own
  (the design fixes the fields). `relationships` holds only the `family-member` entries of (A),
  sorted as in (A); `limits` stays as change 2 has it; there are no holder entries.
  `schema_version` stays 1. The "only exceptions" sentence gains one key.
- (C) A new envelope key `families` with every family datum inside it and `relationships` left
  `[]` (the earlier Decision 2 C): the reserved field stays unused, and it is one more opt-in key
  beside #29's, which the same sentence would have to name.

Variants set aside, each with its reason: `schema_version` 2 in a flagged run (earlier 2 B), which
makes the version depend on a flag; `relationships: null` without the flag (earlier 12 B), "not
examined" in change 2's own terms but a change to the default document (T1-1) and to APO/ov:620;
an envelope field such as `families: true` (earlier 12 C), one more exception to #29's sentence;
both `limits` keys in every run (earlier 11 (ii)), one field list but a changed default document,
against T1-1. Reporting the caps in a `families` object with its own `limits` (earlier 11 (iii))
is (B)'s way, as #29 keeps its caps in its `remote` object (#29
`specs/project-overview/spec.md:526-536`), at the same exception count as (A)'s.

Common to the bundles: `schema_version` stays 1, the reserved field exists with its type
unchanged, and a default run is byte for byte change 2's, as #29 keeps 1 for its opt-in fields
(#29 proposal.md:738-741); `row` names a row by its `path`, by which `projects` is sorted
(APO/ov:619), so no probe result is copied; rows are keyed by repository identity (APO/ov:75-76),
so a row with a null `repository.root` needs the design to confirm that `path` names one row. The
cost, under (A) and (B): DI:959's "always `[]` in version 1" and APO/ov:620 change, and a consumer
that asserted `[]` sees entries only when it passes the flag.

The form of `found_at`: one row path or null, as drafted, or an array of row paths sorted by
bytes, `[]` meaning none among the rows read and null "not established" (SA-3). Ids are not
unique, since two clones with `id: billing` give two rows and openRepoShape says ids confer
nothing (ORS `contracts/repository-naming.yaml:13-18`, `038dafb`), and a single path hides that.
The form is open to the design, with the tie rule that AE-5 asks for (`clarifications.md`).

The caps, scope: (A) 128 entries per holder and 512 sibling checks per run, each after canonical
sorting, entries by member name bytes then declared index, as the other caps apply after sorting
(APO/ov:221-222), holders in canonical order. (B) 512 per run only. (C) 128 per holder only,
which lets 128 holders start 16,384 checks bounded by the deadline alone. A cap that drops work
leaves the entries past it `unknown`, reason `member-cap` or `check-cap`, and the omitted count
goes with the cap's report; under T1-6 B it is also a `scan-limit` scan error, `limit`
`family_members` or `family_checks`, with an exact `omitted` (APO/ov:222-224) and A1's message,
whose M is "its value in `limits`" (A1 `spec.md:402`). A cap reported in no `limits` key would
break "the values in force are always reported in `limits`" (APO/ov:219-220); (A) reports it in
`limits` and (B) in `families.limits`.

Headroom and cost, corrected by the council (SA-2). The caps' measured worst case takes 48.3 s of
the 60 s deadline (APO proposal.md:598-605), leaving 11.7 s. The earlier draft priced a sibling
check at one entry of a root's marker pass (APO design.md:134-137), and task 2.1 measured a
4,096-directory root at 0.36 s warm and 2.6 s projected cold (APO tasks.md:20), so 512 checks
came to about 0.05 s warm and 0.33 s cold. That left out the manifest parse, which dominates:
`read_yaml` calls the pure-Python `yaml.safe_load` (project:37-47), and the stack-architect
measured about 5.5 ms for a real 5,274-byte `project.yaml` (4.6 ms for the 4,621-byte
`family.yaml`) on Python 3.12.3 with PyYAML 6.0.3. 512 parses took 2.15 to 2.42 s, and a
`family.yaml` at the 1 MiB bound (3,057 members) takes 3.25 s, 0.63 s with the C loader
(council-architect.md, Concern 2). So 512 checks take about 2.2 to 2.4 s, 19 to 24 percent of the
11.7 s headroom before the 128 holder reads, and scope (C)'s 16,384 checks, scaled at that
rate, about 90 s, past the 60 s deadline. UNVERIFIED: the cap values 128 and 512 have not been
re-measured with the parse included, and the 90 s is scaled; an OQ-4-style run (APO tasks.md:20)
with real manifests would verify them before the values are fixed. If each holder's checks run in
one task, as a root's entries do (APO design.md:134-137), the abandoned-worker bound (APO
design.md:477-479) gains at most 256 tasks, one manifest read and one check task per holder.

Recommended: (B), with cap scope (A). The single object matches #29's pattern at the same
exception count (SA-3): the reserved `relationships` field keeps its purpose, the "examined or
not" marker is present and not inferred from the `projects` rows (an inference that breaks the day
another extension puts entries of another type in `relationships`), and the caps are reported
where #29 reports its own. Scope (A) bounds both one large family and many families; the
council's constraints on the cost, one run-wide cap among them, are in `clarifications.md`.

**T2-2. What deadline and budget share does it get inside the overview's 60 s?** (A) None of its
own: sibling checks are bounded filesystem tasks, each waited for with `min(5 s, deadline - now)`
under the 60 s deadline (APO/ov:183-188), inside the holder's collector, and sibling probes are
ordinary collection; the four-at-once limit governs Git children only (APO/ov:236-238); so the
64 s run bound holds (APO proposal.md:483-487). Under T1-2 A the siblings that are candidates
stay under the candidate cap, which bounds the Git children at the measured worst case of 48.3 s
(APO proposal.md:598-605), and a discovery-phase manifest task starts (T1-2). (B) A family phase
after collection with its own budget, like #29's `min(30 s, deadline - now)`. (C) A reserved
slice of the 60 s. Recommended: B while T1-6 is A, and A if T1-6 is B (SA-1; council-architect.md,
lesser observations). A check inside the holder's collector is a per-candidate task, whose cut
becomes data on the holder's row (APO/ov:183-188, :322-324): that is T1-6 B. T1-6 A needs the
check outside the per-candidate boundary, which is B. The phase is filesystem only and starts no
Git child, so its budget is small and is measured (T2-1); under T1-2 C no sibling is probed and
no discovery-phase manifest is read, so the Git children stay at the measured bound. B competes
with #29's phase for the same remainder of the 60 s, a small cost since its work is filesystem
only. Risk: a `--families --remote` run leaves #29's phase less time (Risks).

**T2-3. What is the human form?** (A) Under the holder's header, one line per declared member:
`member` padded to 14 columns as a category is (APO design.md:516-518), then `<name>: <state>`,
the reason in parentheses when there is one, and the sibling path or `found_at`, each printed by
What Changes' path and string rule (APO/ov:672-675); member rows, where there are any, keep their
own headers; the lines hide under `--attention` as informational findings do (APO/ov:466-469),
within a shown row too. Before the summary in a flagged run, one line, `Families: H holders
examined, M members; present a, not-a-project b, mismatched c, missing d, invalid e, unknown
f.`, counting every holder and every member, and printed under `--attention` too, as #29 prints
its `Remote:` count line (#29 `specs/project-overview/spec.md:587`), since a count is not a
finding. (B) A separate section after the rows. (C) A suffix on each member row's header.
Recommended: A. The family is read where it is declared, other rows stay as change 2 prints them,
and #29 reads the layout as allowing added lines without a MODIFIED block (#29
proposal.md:1041-1044). The earlier draft said the lines "show only under a holder row shown for
another reason"; that contradicted criterion 13 and APO/ov:466-469, which hide informational
findings within a shown row too, and it is dropped.

A rendered sketch (PA-2), **illustrative only**: the wording and spacing are the design's, and
`/work/projects` stands for any root. The family is criterion 2's, except that `api`'s clone
holds another project's `id`: `web` is present, `ghost` has no clone, and `billing` is cloned
beside the family folder. By T1-0 A `web` and `api` have no row of their own, and
`billing` has one because it is an immediate entry of the root.

```
$ project overview --families
acme  /work/projects/acme/acme
  member        web: present  /work/projects/acme/web
  member        api: mismatched  /work/projects/acme/api
  member        ghost: missing  /work/projects/acme/ghost
  member        billing: missing  /work/projects/billing
billing  /work/projects/billing
tools  /work/projects/tools
Families: 1 holders examined, 4 members; present 1, not-a-project 0, mismatched 1, missing 2,
invalid 0, unknown 0.
3 projects; 0 errors; repair 0, preserve 0, housekeeping 0, informational 0. Findings reflect
local refs as of the last fetch.

$ project overview --families --attention
Families: 1 holders examined, 4 members; present 1, not-a-project 0, mismatched 1, missing 2,
invalid 0, unknown 0.
Nothing needs attention: 3 projects; 0 errors; repair 0, preserve 0, housekeeping 0,
informational 0. Findings reflect local refs as of the last fetch.
```

(Lines wrapped here at 100 columns are one line each in a run; the `billing` line prints the
`found_at` path, the row that `billing`'s entry names.) Under `--attention` the person reads a
count that names one mismatch and two missing members and no line that says which: the member
lines, which are informational, are hidden, and the holder row is not shown because it has no
finding. That is PA-2's concern.

Sub-question for Brett Heap: do `invalid` and `mismatched` show under `--attention`? They are
defects in the family's declaration or in a clone, not ordinary work (PA-2), and the overview's
own rule is that unknown is never healthy (APO design.md:506).

- (i) No: every `member` line hides, as above; the `Families:` line keeps the counts. This
  follows T1-4 A, under which every state is informational, and the attention filter that
  APO/ov:466-468 defines by findings.
- (ii) Yes: a `member` line for an `invalid` or `mismatched` member shows under `--attention`,
  and so does its holder row, without a finding; the sketch then prints the holder header and
  the `api` line before the `Families:` line, and the summary no longer begins "Nothing needs
  attention". This changes which rows `--attention` shows, so the human-report requirement is
  MODIFIED (Capabilities), and it pairs with T1-4 C, findings for the same two states.

Recommended: (i), because T1-4 A keeps member states out of the finding table and the filter is
defined by findings; no council verdict gave a recommendation here. (ii) is the choice if Brett
Heap wants a defective declaration to reach the attention report.

**T2-4. Where is the sibling, and which key names it?** (A) `<holder parent>/<project>`, else
`<holder parent>/<name>`, as project:849-852 reads it, once the holder's parent has passed the
family-folder test and lies inside a root (T1-7). A symbolic link there is resolved once and read
at its target (APO/ov:19-20), as `status` reads a link inside the folder (O19), and is
deduplicated with the candidates by device and inode (APO/ov:32-34). The resolution is the
overview's own, on a bounded task, `os.path.realpath(strict=True)`: `inside()` resolves with
`Path.resolve()` on the calling thread (project:51-57), which APO design.md:475-476 rules out
("No filesystem call runs on the main thread"), and `Path.resolve()` raises `RuntimeError` on a
loop (T1-4, `link-loop`). (B) The declared `path:`. (C) Both. Recommended: A. It is where
openRepoShape clones the working copy (ORS `templates/family-root/scripts/siblings.py:12-16`,
built from `project:` alone at `:962-964` and `:1155-1157`, `038dafb`; the `name` fallback is
`project`'s own) and where `status` already looks, so the two commands agree on the place;
`path:` is always `members/<project>`, the pinned copy (ORS `scripts/family.py:836-838`,
`:909-918`, `038dafb`). They differ on refusal: `status` refuses the whole command on a bad or
repeated entry, a wrong-kind sibling manifest, a non-list `members` or a link out of the folder
(O9, O15 to O18), where the overview reports the entry or the holder and goes on (T1-4, T2-5).

**T2-5. Which holders yield relationships, and what does a bad member list give?** (A) Every
holder in the run, from its manifest, with no Git child: one with no `.git`, its row keeping null
Git fields and no error (APO/ov:66; O7), and one whose identity probe reports an enclosing
repository, likewise (A1 `spec.md:98-100`; F005 FR-003, `spec.md:2126-2128`). A holder whose
`family.yaml` is refused keeps its `manifest-invalid` row error (APO/ov:326-328) and yields no
member entry; its holder-level state is `unknown`, reason `manifest-invalid` (the holder entry
under T2-1 A, the `families` counts under B). An absent `members` yields none, `members: 0`; a
`members` that is not a list (null, a mapping) yields none, its holder-level state `invalid`,
reason `members-not-a-list`, never a refusal (contrast O17). A holder directory that holds both
`family.yaml` and `project.yaml` is read by `manifest()` as a project, `project.yaml` first
(project:422-430), so `status` shows kind `project-manifest` and no children (SA-4's run of
`status both --json`, council-architect.md), while the marker table makes it a `family-holder`
row (APO/ov:26-28). The overview reads `members` only when the marker kind and the manifest kind
agree; otherwise its holder-level state is `unknown`, reason `manifest-invalid`, never
`members: 0`, which would report zero where two are declared. (B) Only holders that are Git
toplevels. (C) A, but a non-list `members` is the holder row's `manifest-invalid` error.
Recommended: A: the members list needs no Git child, a holder outside Git is the case in which a
person most needs to see its members, and C lets a member list change a row's status, against
T1-4.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

Intent only; no delta file is written (Status).

- `project-overview` (change 2's, unarchived): MODIFIED "Overview discovers projects within
  configured roots only" (APO/ov:10), for the flag's carve-out (a sibling beside a holder is
  read below a root's immediate entries; T1-7 B would also reach outside the roots); MODIFIED
  "Overview prints a versioned JSON envelope" (APO/ov:606), for `relationships` and, under T2-1,
  the `families` object or the two `limits` keys; MODIFIED "Overview bounds its work and reports
  what it omitted" (APO/ov:166), for T2-1's caps, which join those listed there (APO/ov:217-224),
  and, under T1-2 A, the discovery-phase manifest read; ADDED "Overview reports family
  relationships on request". Read as they stand, not modified: "Overview isolates one candidate's
  failure" (APO/ov:317-347), whose boundary keeps a sibling's own failure on its own entry (What
  Changes, isolation). The other requirements stay untouched, "Overview renders a readable human
  report" under #29's reading (T2-3), except that T2-3's sub-question (ii) would MODIFY the
  attention rule (APO/ov:466-471).
- Nothing in `project-clean` or `project-clean-review-safety`; nothing in `project-command`,
  `project-review-safety` or `speckit-extension-integration`. PRS:67-71 binds `status` and
  `doctor`, which this change leaves as they are. Change 2's carve-out in `project-review-safety`
  (APO `specs/project-review-safety/spec.md:9-12`) is read, not modified: a sibling's manifest
  with invalid text is `manifest-invalid` on its own row, as any project manifest is.

### Statements this change would make false

Each is true of a run without the flag and false of a flagged run:

- APO/ov:18: "examine each root and its immediate entries only": a flagged run also examines the
  declared siblings beside a holder.
- APO/ov:35-37: "SHALL NOT read a family's member list" and "`relationships` SHALL be `[]`";
  the same text is A1's `spec.md:40-43` (`e4a30fc`) and F005's FR-003 (`spec.md:2123`, :2125).
- APO/ov:65, in "Family holder count, relationships and probe ownership": "`relationships` is
  `[]`, no row and no Git child exists for `acme/web` or `acme/api`".
- APO/ov:67, the same scenario: "with `acme` itself as the root, `web` and `api` are ordinary
  rows of their own and `relationships` stays `[]`": a flagged run lists the holder's members
  there. The same clauses are A1's `spec.md:70`, :72 and F005's user story 1, scenario 2
  (`spec.md:960-970`).
- APO/ov:620: "`relationships`, always `[]`"; also #29's MODIFIED block (#29
  `specs/project-overview/spec.md:242`) and A1's `spec.md:692`.
- APO proposal.md:57, "a family holder is one row with `relationships: []`"; :802, "no traversal
  of members or legs"; APO design.md:75, the non-goal "Remote, family, bench, container or park
  evidence"; APO design.md:442-444 (A1 `design.md:461-463`), "a family holder is one row that
  claims no member".
- APO proposal.md:162-163, "The overview reads a manifest only through `manifest()`, for name,
  kind and `tracking_branch`", and APO design.md:456-458, the manifest task "so that name, kind
  and `tracking_branch` follow [R] exactly": a flagged run also reads the holder's `members` and
  each sibling's `id`.
- APO design.md:477-479, "Abandoned workers are bounded by the number of tasks started (at most
  32 roots, 128 manifests, 512 rows, 512 reflog reads and a handful more)": T2-1's caps add up to
  256 tasks.
- Under T1-2 A, the pipeline order: DI:627-637 at `15504f1` (`manifest()` after the identity
  probe, inside the collector) and APO design.md:134-137, :385-386 and :454-460.
- Under T1-2 A (T1-0 B), the guarantees that the adversary found it breaks (AE-1): APO/ov:224-229
  (an `exact` `omitted` needs the whole population enumerated), :243-249 (the document does not
  depend on concurrency or completion order, and `performed` counts every Git child started) and
  :322-324 (a failure "SHALL NOT change, remove or reorder any other row").
- Under T2-1 A, APO/ov:610-614's exact `limits` keys; under any T2-1 bundle, #29's "these two
  keys are the only exceptions" (#29 `specs/project-overview/spec.md:282-287`), since each adds
  a key that only a flagged run carries.
- Under T1-7 B, APO/ov:10-19, "within configured roots only".
- APO proposal.md:409-411 gives as a reason PRS stays untouched that the overview "renders no
  nested estate or leg": a flagged run renders member relationships, never estate snapshots,
  so PRS:67-71 stays untouched but the reason narrows.
- Packet statements made stale by a flagged run, none of them normative: DI:51-55 ("never calls
  `snapshot`, which recursively follows family members and project legs"), DI:333-337, DI:959,
  DI:1276 (the example envelope's `"relationships": []`) and DI:1759-1769 at `15504f1`, and
  OV:48-49 ("A `family.yaml` holder is one row with `relationships: []`; no member is
  traversed"). The packet is revised by its owning lane, not by this change; F005's scenario
  above and its Candidate entity (`spec.md:3193-3197`) are feature records, not edited.

Kept true: "never recurse" (APO/ov:18-19), the traversal being one level beside the holder and
declared names only (T1-3); the holder is one row (APO/ov:36-37); its probes follow its own
directory (APO/ov:38-39); "Grouping grants nothing" (APO proposal.md:157-158). Feature records
are not edited.

## Dependencies and Sequencing

- **Change 2 and feature 005** (#10, lane openRepoProject-4). Change 2 was ratified on
  2026-10-09 (APO proposal.md:5-8) and is unarchived; feature 005 is specified on
  `005-project-overview` (`41cf866`), builds `relationships: []` (its FR-003) and puts family
  traversal out of scope (F005 `spec.md:4748-4749`); it follows feature 004 (APO tasks.md:25).
  This change's realization follows feature 005's merge and change 2's archive, as #29's does
  (#29 proposal.md:545-550).
- **A1, PR #34.** Brett Heap answered feature 005's Q1 to Q17 on 2026-10-21 (F005
  `spec.md:635-639`) and ratified A1, "ratify 34", on 2026-10-22 (A1 proposal.md:9-10). PR #34
  had not merged: main is `15504f1`, A1's merge base. A1 moves the discovery text this change
  would modify (A1 `spec.md:40-45`) and adds a family-holder clause to requirement 2 (A1
  `spec.md:94-102`; A1 proposal.md:1203-1211, Q11 A). This is the hold trigger: the deltas are
  written on change 2's text with A1 merged.
- **#29, add-project-overview-remote-merge-status** (lane openRepoProject-5, draft). It MODIFIES
  "Overview prints a versioned JSON envelope", carrying "`relationships`, always `[]`" (#29
  `specs/project-overview/spec.md:228`, :242), and also "Overview bounds its work and reports what
  it omitted" (:51) and "Overview is local and read-only" (:3), and ADDS a remote phase after
  collection (:431). Lane 5's rule, stated for change 1's evidence model that it shares with #26:
  "whichever of the two archives second re-bases its block on the other's archived block before
  it archives" (L-11, #29 proposal.md:578-579; L-17, :658-662). This change would share the
  envelope requirement, and with T2-1's caps the bounds requirement, so it takes the same rule
  over, by analogy: the MODIFIED blocks are not held for #29, the second change to archive
  re-bases its block on the first's. Under any T2-1 bundle the two would also share #29's
  sentence that its two `remote` keys "are the only exceptions to 'exactly these fields, every
  one always present'" (#29 `specs/project-overview/spec.md:282-287`); the second to archive
  re-bases that sentence too. No text read here orders the two; the rule makes either order safe.
  #29 also says `--remote` "SHALL combine with every other overview option" (its `spec.md:349`),
  so its remote phase would query sibling rows like any worktree row, where siblings have rows.
- **#27 and #26** (heads `9473b2c` and `6c7c0f9`, re-read). #27 (cache disposal) MODIFIES
  "Overview reuses the cleanup classifier and merge target" (#27
  `specs/project-overview/spec.md:3`), which this change does not touch: same capability,
  archive order only. #26 (branch retirement) has no `project-overview` delta (its deltas are
  `project-clean`, `project-clean-review-safety` and `project-command`): no shared statement.
- **Change 1** (feature 004) adds `root_valid_utf8` beside each nested family member's `root` in
  `status` and `doctor` JSON (CAS/cmd:35-36; CAS design.md:689-691); this change touches neither.
- **Why the ADDED requirement waits for #34 and no block waits for #29.** Written before A1
  merges, the blocks would be re-based on A1's merge, as lane openRepoProject-1's survey of
  2026-10-20 foresaw (its item U1). #29's blocks need no wait: re-basing at archive is the rule
  that both lanes already hold (PA-3).

## Impact

- **`project`**: the overview's parser gains the flag; the holder's member list is read from the
  manifest it already reads; bounded sibling tasks; a relationships builder; the human lines. No
  new dependency (PyYAML as today, requirements.txt:2); `status`, `doctor`, `update` and `clean`
  unchanged.
- **`README.md`**: the overview section gains the flag, the states and that a relationship never
  authorizes cleanup, and says that only families whose holder is inside a scanned root are
  examined: a member's own row names no family (O13), so a family whose holder lies outside every
  scanned root looks like no family (PA-4). Under T1-0 C it gains the `--root <family folder>`
  workaround instead.
- **`tests/test_project.py`**: fixtures like `FX`'s (openRepoShape's layout with the holder's
  `family.yaml` carrying `repository:`, a sibling that is not a project, a clone outside the
  folder, a malformed entry, a self-named member, a holder with no `.git`, a looping link, a
  holder cloned flat), offline, with zero-mutation snapshots and fake owner tools first on `PATH`;
  CI runs Python 3.10 and 3.12 on `ubuntu-latest` (`.github/workflows/tests.yml:9-17`).
- **Speckit handoff**: one feature after feature 005 merges and change 2 archives, numbered at
  `/speckit.specify` time from a local main synced to `origin/main`.
- **Expected conflicts**: features 004 and 005 and #29's realization edit `project`, the tests
  and `README.md`; whichever merges second merges main in, never rebasing.

## Acceptance criteria

Candidates, each a test on Python 3.10 and 3.12:

1. Without the flag, every scenario of change 2 holds unchanged, "Family holder count,
   relationships and probe ownership" included (APO/ov:63-67), and the JSON and human output,
   timestamps and `budget.probe_concurrency` apart, equal those of the same run of the build
   without the extension.
2. With the flag over `FX`'s `acme` estate as a child of the root `P`, after three fixes to `FX`
   (AE-2, AE-3): the holder's `family.yaml` given `repository: example/acme` (it has `name: Acme`
   and no `repository:`, so openRepoShape's family folder name is `Acme` and not `acme`; T1-7),
   `web`'s `project.yaml` given `id: web` (it has no `id`, so openRepoShape says WRONG PROJECT
   against the entry's `id: web`; T1-4), and `billing`'s given `id: billing`: rows for the holder,
   `billing` and `tools` (under T1-2 A also `web` and `api`); `relationships` holds `web`
   `present` with `row` null (under T1-2 A, its row), `api` `not-a-project`, `ghost` `missing`
   with `found_at: null`, and `billing` `missing` with `found_at` its row; the holder entry
   (`examined`, `members: 4`) under T2-1 A, or a `families` object counting 1 holder and 4
   members under B; no row and no Git child for anything under `members/`.
3. With the family folder as the root, each sibling has one row and one probe set, and
   `probes.performed` equals the same run's count without the flag; a sibling that is a linked
   worktree of another row merges into that row, its entry's `row` naming it with reason
   `merged-row`.
4. Malformed entries: `../evil` is `invalid`, `bad-name`; a non-mapping, `not-a-mapping`; a
   repeated name, `duplicate`, the first kept (contrast O15); a member named like the holder,
   `names-holder`, the holder probed once (contrast O10). The other entries are reported, and
   the exit is what the run gives without the flag, never 2 (contrast O9).
5. Holders: one with no `.git` and one inside an enclosing repository both yield their entries
   and keep null Git fields and no error (T2-5); a refused `family.yaml` gives the holder-level
   state `unknown`, `manifest-invalid`, its row error standing; `members: null` and a mapping
   give `invalid`, `members-not-a-list` (contrast O17); an absent `members` gives `members: 0`; a
   directory holding both `family.yaml` and `project.yaml` gives `unknown`, `manifest-invalid`,
   never `members: 0` (SA-4).
6. A sibling manifest with invalid UTF-8, one over 1 MiB, one of the wrong kind (contrast O16),
   and any sibling manifest in a run without the YAML library: the entry is `unknown`,
   `manifest-invalid`, the refusal is on the sibling's own row, and the other entries are
   reported.
7. Links: a sibling that is a link inside the family folder is read once, at its target (as
   O19), and deduplicated with the candidates; one whose target leaves the holder's parent is
   `invalid`, `outside-folder` (contrast O18); a loop, `web -> web2 -> web` and `me -> me`, is
   `invalid`, `link-loop` on both Pythons, the other entries are reported and the exit is what
   the run gives without the flag, never 2 (contrast the `status` crash, Out of Scope).
8. Ids, as openRepoShape compares them (ORS `templates/family-root/scripts/siblings.py:868-876`,
   `038dafb`): an entry `id: web` against a clone `id: www` is `mismatched`; an entry `id: web`
   against a clone with no `id` is `mismatched`; an entry with no `id` against a clone with one
   is `mismatched`; an entry and a clone both with no `id` are `present`; a bare `id: 2026` on
   both sides is `present`; ids that PyYAML types differently from openRepoShape's reader (`on`,
   `No`, `0x1F`, `1_000`) are rows of the parity table (T1-4); a missing member whose `id` is in
   no manifest read has `found_at: null`.
9. A member declared with `name:` and no `project:` is read at `<holder parent>/<name>`.
10. Caps: one holder declaring 130 names with no directory, so that the candidate cap cannot
    trip: the first 128 in member-name order are checked and the other 2 are `unknown`,
    `member-cap`; the cap and the omitted count 2 are reported in the family evidence (T2-1:
    `families.limits` and `families.counts`, or `limits.family_members` under A), and there is no
    scan error, no row error and no change of exit (T1-6 A). Under T1-6 B instead: one
    `scan-limit` with `limit: "family_members"`, `{"count": 2, "exactness": "exact"}` and the
    message "family_members cap of 128 reached" (A1 `spec.md:402`), the run incomplete and
    exiting 1 (APO/ov:654-655, :762-764). Five such holders of 128 names: the checks past the
    512th are `check-cap`.
11. No relationship state changes a classification, finding, suggestion, status, summary count,
    `completeness` or exit (under T1-6 B, the incompleteness a cut or capped check records
    excepted). The `FX` run of criterion 2 with and without the flag differs only in
    `relationships` and in what T2-1 adds, the `families` object or `limits.family_members` and
    `limits.family_checks`; under T1-2 A it also differs in the rows of `web` and `api` and their
    findings, in `summary.projects`, `summary.repositories` and `summary.worktrees`, each 2
    higher (APO/ov:643-645), and in `probes.estimated` and `probes.performed`, each 10 higher,
    two Git candidates of one worktree row each costing 1 + 3 + 1 (APO/ov:248-254). No
    suggestion names a holder for a member's worktree; `project clean <holder> --all-safe`
    selects no member's worktree.
12. A held sibling `stat` makes the entry `unknown`, `probe-timeout`, and nothing else changes:
    the holder's row keeps its status and the run its completeness and exit (T1-6 A); at the
    deadline the code is `deadline-exceeded`; the other entries are reported. Under T1-6 B the
    code is recorded on the holder's row instead, whose status becomes `error`, and the run is
    incomplete and exits 1 (APO/ov:654-655, :762-764).
13. `--attention` hides the member lines, still prints the `Families:` line, and changes no
    JSON; `--attention --json` prints the full envelope (APO/ov:471).
14. The `Families:` line of criterion 2 counts 1 holder examined and 4 members: present 1,
    not-a-project 1, missing 2, and mismatched, invalid and unknown 0 (its exact wording is the
    design's).
15. Entries sort by holder path bytes, the holder entry first, then by member name bytes, then by
    declared index, entries with no name last; every `reason` is one of T1-4's and T2-5's codes.
16. Paths and strings: a member name holding U+202E and a `declared.path` holding the byte
    0xFF are escaped in JSON by A1's string rule; a holder path that is not valid UTF-8 has
    `holder_valid_utf8: false`; the human `member` line prints such a path in `$'...'` form.
17. Combinations: `--families --remote` prints both opt-in outputs and neither changes the
    other's (#29 `specs/project-overview/spec.md:349`), sibling rows, where there are any, being
    queried as any row; under `--families --strict` no member state changes the exit, which only
    warnings of findings change (APO/ov:763-765).
18. A sibling that holds `family.yaml` and no `project.yaml` is `invalid`, `nested-family`;
    where it has a row, that row is of kind `family-holder` and its own members are unread.
19. Read-only and offline: zero-mutation snapshots, no network, no fake owner tool called.
20. The family-folder test (T1-7): a holder whose parent folder is not named after the family,
    `FX`'s `acme` as it is (`name: Acme`, no `repository:`) or a holder cloned flat under a root
    (marker `D/family.yaml`, APO/ov:28), has every entry `unknown`, `not-in-family-folder`, and
    no sibling is read; the same estate with `repository: example/acme` passes, and so does a
    link named after the family beside the holder's parent that leads to it (`family_link`, ORS
    `templates/family-root/scripts/siblings.py:1372-1397`, `038dafb`).
21. Reach (T1-7 A): `--root` given at the holder, whose parent is not a root, gives the holder's
    row and entries that are all `unknown`, `outside-roots`; nothing outside the root is read
    or probed.
22. `found_at` under a scan limit (T1-4): in a run with a `scan-limit` scan error that can have
    left a row unread, a member whose sibling path is absent is `unknown`, `scan-limit`; in a
    complete run the same member is `missing`, with `found_at` null, or the row's path when a
    row holds its `id`.

## Risks

- openRepoShape owns the layout (README.md:264); if the sibling placement or the family-folder
  test moves, both `status` and the overview read the wrong place. Both are cited at `038dafb`,
  224 commits past the checked-out HEAD that earlier drafts cited, and the cited lines moved
  (`verify_sibling` 460 to 835, `project_id` 449 to 755; council-adversary.md, AE-3) though the
  two rules tested are the same at both shas. The overview copies `project:852`'s rule; pinning
  it by sha, as project:204-211 pins the name forms, is the design's choice, and the deltas are
  written after a re-read at a current sha.
- PyYAML, which `project` reads with (project:37-47), and openRepoShape's own reader type `on`,
  `No`, `0x1F` and `1_000` differently (T1-4): an id test can say `mismatched` where the owner
  passes, and a member named `No` or `On` is `invalid`, `bad-name`, where openRepoShape accepts
  it.
- Under T1-2 A (T1-0 B) siblings add candidates, so the 128-candidate cap (APO/ov:217-222) binds
  sooner and a large estate run ends incomplete more often, visibly: an inference from the cap,
  which already binds on this estate (T1-0), and not measured.
- The sibling checks' cost: priced with the manifest parse it is about 2.2 to 2.4 s for 512
  checks, measured on one host with the pure-Python loader (T2-1), not the 0.05 s of the earlier
  draft; the cap values and the choice of loader are UNVERIFIED until a measurement like task
  2.1's (APO tasks.md:20), which should also record event-loop latency, since parse threads
  starve the loop (`clarifications.md`).
- T1-2 A changes the order change 2's design fixed (DI:627-637 at `15504f1`; APO design.md D2,
  D6, D8), and a candidate kept without the flag can be displaced by a sibling with it.
- A `--families --remote` run leaves #29's remote phase less of the 60 s.
- `doctor` calls a missing member an `error` (O5) while the overview calls it informational:
  T1-8 A states the divergence, pending Brett Heap's ruling.
- Under a scan limit a member whose sibling directory is absent reads `unknown`, never `missing`
  (T1-4): on this estate, where the cap binds in every default-root run, `missing` would be rare.
- A consumer that asserted DI:959's "always `[]`" sees entries when it passes the flag.
- Two lanes' blocks of one requirement must be re-based in order (Dependencies).

## Out of Scope

- Any cleanup permission: `clean`'s eligibility, gates, batch and suggestions stay as change 1
  and change 2 define them (SY:34-37; CAS/pc:568-571).
- Bench, container and park integrations, and parked-work records as relationships (APO
  proposal.md:571; DI:1807-1808 at `15504f1`, one change per integration).
- Remote queries of any kind (#25, #29), the sibling's remote URL included.
- Any change to `discover`, `snapshot`, `status` or `doctor`: no observation here shows the
  overview needs one; their family readings (O3 to O19) stay as they are. A member-entry reader
  shared with `snapshot()` (SA-4) would touch that code and not its behaviour: a design question,
  recorded in `clarifications.md`.
- Member clones as rows (T1-0 A leaves them to a later change); legs, pinned member copies and
  nested families (T1-3); undeclared directories in a family folder (T1-4).
- openRepoShape's family mechanics: `bootstrap`, `siblings`, `family.py` and
  `validate-family.py`, which the overview never runs (APO/ov:711).
- A command that clones, moves or repairs a member.
- The family folder itself, never a candidate: feature 005's recorded edge case EC-025, kept by
  Brett Heap's Q10 A (F005 `spec.md:1871-1878`, :812-814).
- **An existing defect of `project status`, to be filed as its own issue on Brett Heap's word**
  (AE-4; this lane has not filed it): a member link that loops crashes `status`. `inside()` calls
  `Path.resolve()` (project:51-57, :54 at the call), which raises `RuntimeError` on a loop, not
  an `OSError`, and `main()` catches only `Refused` and `OSError` (project:1143), so `status`
  ends in a traceback with exit 1 and no JSON, even under `--json`, on Python 3.12 and 3.10, for
  `loop/web -> web2` with `loop/web2 -> web`, and for `selfie/me -> me` (the adversary's fixture
  and runs, council-adversary.md, AE-4; this writer re-ran the primitives on Python 3.12.3:
  `Path.resolve()` raises `RuntimeError`, `os.path.realpath(strict=True)` raises `OSError` with
  errno 40). `doctor` reaches the same `snapshot()` (project:937) and was not run. It belongs to
  `status` and `doctor`, not to this change, which resolves with `realpath(strict=True)`
  (T1-4, `link-loop`).

## Alignment review applied (2026-10-22)

Two final reports on `5aacbec`, the stack-architect's (M1, M2, G1 to G6, D1 to D4) and the
QA-lead's (QA-1 to QA-16), 28 findings, applied under the lane lead's rulings of fix round 1;
overlaps were treated once. Still an observation record: no delta, `design.md` or `tasks.md`.
Decision ids below are the tiered ones (Decisions for Brett Heap); "then N" gives the number the
Decision had when the round was applied.

- M1: the code-reading sentence now says the cycle check fires on two entries naming one
  directory; run O15 added (`FX/projects-dup`, exit 2 on 3.12 and 3.10); T1-4 `duplicate`.
- M2: T1-4 cites APO/ov:18-19 for the bar on listing the family folder, DI:1789-1791 for the
  packet's preference only.
- G1: new Decision T1-2 (then 10), where sibling expansion runs, with the departures it names;
  What Changes points there; statements made false list them under T1-2 A.
- G2: T2-2's (then 5) reason corrected (5 s per filesystem task; four at once is Git only); the
  run-wide bound and the headroom are T2-1's (then 11); Capabilities no longer makes the cap
  optional.
- G3: T2-1's reporting options (then Decision 11 (i) to (iii)); criterion 11 names the `limits`
  keys; Dependencies names #29's "only exceptions" sentence (its `spec.md:282-287`).
- G4: What Changes, "Paths and strings", a candidate requirement; T2-1's object (then Decision
  2) carries the flags; T2-3 (then 6) prints by that rule; criterion 16.
- G5: T1-4's state table (`manifest-invalid`, `duplicate`, `outside-folder`, `merged-row`) and
  T2-5 (then 9: refused holder manifest, non-list `members`); T2-4 (then 8) says where `status`
  and the overview differ; runs O16 to O19; criteria 3 to 7.
- G6: statements made false gain the packet bullet (DI:51-55, :333-337, :959, :1276,
  :1759-1769; OV:48-49) and F005's records; T1-5 (then 7) cites OV:395-397.
- D1: incompleteness cited to APO/ov:654-655, the cap to APO/ov:222-224 (T1-4, T2-1, T1-6).
- D2: with QA-1, a cut sibling check is recorded on the holder's row, a scan error only for a cap
  or the deadline's count (then Decision 4; now the T1-6 B option, T1-6 A being recommended).
- D3: T1-4's `present` followed `verify_sibling`'s id test (ORS `siblings.py:493-501` at
  `2476992`) and said that the origin test (:482-492) is deferred; the council corrected the id
  clause (AE-3, SA-4) and the pin (`038dafb`).
- D4: with QA-10, T1-3 cites ORS for legs and pinned copies as submodules.
- QA-1: T1-4 and criterion 12 record a cut check on the holder's row (APO/ov:183-188), now the
  T1-6 B option.
- QA-2: T2-1 and criterion 10 cite APO/ov:654-655 and :762-764 for incompleteness and exit.
- QA-3: statements made false add APO/ov:67, A1 `spec.md:70`, :72 and F005 `spec.md:960-970`.
- QA-4: T2-1 fixes the order (member name bytes, then declared index) and the `limits` key;
  criterion 10.
- QA-5: T2-2 says the 48.3 s covers Git children only; T2-1's run-wide cap and headroom
  arithmetic, marked UNVERIFIED and corrected by the council (SA-2); APO design.md:477-479 in
  statements made false.
- QA-6: the holder entry, now in T2-1 (then new Decision 12), so that `[]` is never ambiguous.
- QA-7: T1-4 and T2-5 and criteria 5 and 6; What Changes, "Isolation"; Capabilities says the
  isolation requirement and the review-safety carve-out are read, not modified.
- QA-8: T2-5 and criterion 5 cover a holder inside an enclosing repository (A1 `spec.md:98-100`;
  F005 `spec.md:2126-2128`).
- QA-9: heads re-fetched and updated (feature 005 `41cf866`, #26 `6c7c0f9`, #27 `9473b2c`; #29
  and A1 unchanged); F005 lines re-pinned at `41cf866`.
- QA-10: T1-3 cites ORS `contracts/repository-naming.yaml:348-360` and :392-393 (then at
  `1a9fc53`, now at `038dafb`, the file being identical).
- QA-11: criteria 1 and 8 to 18 (byte-identical default, ids, name fallback, caps, deltas, cut
  check, `--attention`, `Families:` counts, sort key and closed `reason`, strings, combinations,
  nested family); T2-3 defines the `Families:` line.
- QA-12: What Changes, "Paths and strings" (A1 `spec.md:385-390`, :402, :748-752); criterion 16.
- QA-13: T1-4, T1-5 and criterion 11 separate a member's state from a cut or capped check; T1-6
  now rules on that check.
- QA-14: statements made false add APO proposal.md:162-163 and APO design.md:456-458.
- QA-15: T2-4 (then 8) resolves a link once (APO/ov:19-20); T1-4 `outside-folder`; O18, O19;
  criterion 7.
- QA-16: only "examine each root and its immediate entries only" is listed as made false;
  "never recurse" moves to "Kept true".

## Council review applied (2026-10-22)

Three reports on `b8a1b55` (council-product.md, council-architect.md and council-adversary.md,
13 concerns) and the lane lead's verdicts on them (council-verdicts.md), given 2026-10-22; see
the citation paragraph for their path. VALID means this proposal changed; NOTED means
`clarifications.md` records the concern as a constraint on the later `design.md`; DISMISSED
carries its reason. Still an observation record: no delta, `design.md` or `tasks.md`. The
verdicts' items 1 to 11 are applied as follows, one line per concern.

- PA-1 (VALID): T1-0, the scope Decision, added first, with options A to C and A recommended;
  T1-2's recommendation changed from A to C with SA-1's and AE-1's reasons and PA-1's fourth
  option (D, an implicit family-folder root) added; Alternatives gain `--root <family folder>`
  and the implicit family-folder root; Why gains the estate paragraph.
- PA-2 (VALID, except one DISMISSED part): T2-3 gains a rendered sketch of the human report and
  `--attention` (illustrative) and the sub-question on `invalid` and `mismatched` under
  `--attention`; T1-8 added for the `status` and `doctor` divergence; the earlier T2-3 (then 6)
  phrase "show only under a holder row shown for another reason" is dropped, as it contradicted
  criterion 13 and APO/ov:466-469. DISMISSED: "a family tag on the member row", which would change
  a base row, against the invariant that SA-1 and AE-1 protect under T1-0 A; the holder's
  relationship entry names the member row's path instead, which links the two without changing
  the row.
- PA-3 (VALID and NOTED): the Decisions are split into Tier 1 (T1-0 to T1-8) and Tier 2 (T2-1 to
  T2-5), with the hold trigger defined (write the ADDED requirement once #34 merges; the MODIFIED
  blocks shared with #29 are re-based at archive under lane 5's rule, #29 proposal.md:578-579
  and :658-662); the old numbers map to the new in the Decisions table, and every cross-reference
  is updated. NOTED: the Tier 2 envelope details, as constraints until the design rules them
  (`clarifications.md`).
- PA-4 (VALID): `found_at: null` defined as "not found among the rows read" and qualified under a
  scan limit (`unknown`, reason `scan-limit`, not `missing`; the reason's name is a drafting
  choice, ruled by the lead); only holders inside scanned roots are examined, for the README
  (Impact); a sibling that is itself a holder is `invalid`, `nested-family` (T1-3, T1-4,
  criterion 18).
- SA-1 (VALID): T1-6 (the council's "Decision 13") added, recommending no, with #29's precedent,
  and the QA-13 text rewritten to match (T1-4, T1-5, criteria 10 to 12), the other option kept
  visible; T1-2 flipped to C with AE-1 (above); T2-2's recommendation made conditional on T1-6.
- SA-2 (VALID and NOTED): the cost of 512 sibling checks corrected to include the manifest parse
  (about 5.5 ms each, 2.2 to 2.4 s for 512, 3.25 s for a 1 MiB manifest), the cap values marked
  UNVERIFIED (T2-1, Risks). NOTED: a worker bound beside the Git bound of four, a per-run manifest
  cache, a re-measurement with real manifests, a single run-wide cap, and the starvation of the
  event loop by 16 parse threads (`clarifications.md`).
- SA-3 (VALID): the earlier Decisions 2, 11 and 12 merged into T2-1, a Tier 2 envelope Decision
  with the current split, one optional `families` object and `found_at` as an array as options,
  recommending the single object for #29 parity.
- SA-4 (VALID and NOTED): the `present` rule and criteria 2 and 8 corrected to openRepoShape's
  string comparison, where a clone with no `id` reads `'None'` and is WRONG PROJECT (T1-4), with
  PyYAML's typing of bare ids (`on`, `No`, `0x1F`, `1_000`, `2026`); the dual-manifest holder
  reads `unknown`, `manifest-invalid`, never `members: 0` (T2-5, criterion 5). NOTED: one pure
  member-entry reader shared with `snapshot()`, and a parity test table between `status` and the
  overview (`clarifications.md`).
- AE-1 (VALID and NOTED): the five constraints of T1-0 B and the reasons of T1-2 C; APO/ov:224-229,
  :243-249 and :322-324 listed in statements made false under T1-2 A. NOTED: the five constraints
  in full, if T1-0 B or T1-2 A is ever chosen (`clarifications.md`).
- AE-2 (VALID): the family-folder test added to the candidate behavior (What Changes) with
  openRepoShape's check cited at `038dafb`, and T1-7, the Tier 1 Decision on reach outside the
  roots, recommending no (`unknown`, `outside-roots`); criteria 2, 20 and 21; `FX`'s two flaws
  recorded in the fixture paragraph.
- AE-3 (VALID): the `present` correction (with SA-4) and PyYAML's typing; every openRepoShape
  citation re-pinned at `038dafb` (openRepoShape origin/main, the newest commit its checkout
  holds; the checked-out HEAD `2476992` is 224 commits behind it and `1a9fc53` an ancestor),
  re-reading each line; `1a9fc53` stays only where `project:204-211` is quoted; the naming
  contract is byte-identical at both shas.
- AE-4 (VALID): `invalid`, `link-loop`, resolved with `os.path.realpath(strict=True)`, in T1-4,
  T2-4 and criterion 7; the existing `project status` crash recorded in Out of Scope as a defect
  to file on Brett Heap's word, not filed by this lane.
- AE-5 (NOTED): entry identity by resolved path and not by name, two entries reaching one
  directory being duplicates, and a rule for `found_at` when two rows share an id
  (`clarifications.md`); T1-4 and T2-1 point to it.
