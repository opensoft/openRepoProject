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
`git fetch` on 2026-10-22, fix round 1: A1 `e4a30fc`, feature 005 `41cf866`, and the branches
of #29 `a529310`, #27 `9473b2c` and #26 `6c7c0f9`; every line cited on those branches was
re-read at those heads. `F005` is feature 005's `specs/005-project-overview/spec.md` at
`41cf866`.

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
O1 to O14 and ran O15 to O18 on its own fixture.

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

Candidates, not requirements; each open point is a Decision below.

- **Opt-in** (Decision 1): `project overview --families`; without it the document and report are
  change 2's, byte for byte.
- **Membership from the holder's own manifest.** The `members` list of the holder's
  `family.yaml`, the manifest change 2 reads only for name and kind (APO/ov:319-320; DI:333-335
  at `15504f1`), and the `id` of each sibling's `project.yaml`: fields change 2 never reads
  (Statements this change would make false). Where the holder's read runs is Decision 10. Each
  entry names a working sibling at `<holder parent>/<project>` (Decision 8); `id` and `path` are
  reported as declared, `path` and `pin` never followed.
- **Traversal one level, inside bounds** (Decisions 3, 5, 10, 11). Each sibling is examined by
  bounded filesystem tasks (one link resolution, a `stat`, the marker checks, the manifest
  read); one that is a candidate joins the candidate list where Decision 10 places it, and is
  probed as any candidate is, once, also when it is an immediate entry of a root (DI:1783-1785 at
  `15504f1`).
- **Relationships** (Decisions 2, 4, 9, 12): one entry per declared member in the envelope's
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
- **Isolation** (candidate requirement). A sibling candidate's own failure, its identity probe or
  manifest read, stays on its own row (APO/ov:322-324, :342-343) and reaches the holder's entries
  only as a state; relationships change no row. A cut family check is the holder's own task and
  is recorded on the holder's row (Decision 4). The isolation requirement (APO/ov:317-347) and
  `project-review-safety`'s manifest carve-out (APO `specs/project-review-safety/spec.md:9-12`)
  are read as they stand, not modified.
- **Display** (Decision 6): one `member` line per declared member under the holder's row.
- **Evidence, never permission** (Decision 7; SY:34-37; OV:395-397 at `15504f1`).

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
   declared member, `schema_version` staying 1: `{"type": "family-member", "holder": <holder row
   path>, "holder_valid_utf8", "member": <declared name or null>, "declared": {"id", "path"},
   "sibling": {"path", "path_valid_utf8"}, "state", "reason", "found_at": <row path or null>,
   "found_at_valid_utf8", "row": <project row path or null>, "row_valid_utf8"}` (What Changes,
   paths and strings), plus Decision 12's holder entry; sorted by holder path bytes, the holder
   entry first, then by member name bytes, then by declared index, an entry with no name after
   the named ones; `[]` without the flag. (B) The same, with `schema_version` 2 in a flagged run.
   (C) A new envelope key `families`, `relationships` left `[]`. Recommended: A. The field exists
   with its type unchanged and a default run is byte for byte change 2's, as #29 keeps 1 for its
   opt-in fields (#29 proposal.md:738-741); `row` names a row by its `path`, by which `projects`
   is sorted (APO/ov:619), so no probe result is copied; rows are keyed by repository identity
   (APO/ov:75-76), so a row with a null `repository.root` needs the design to confirm that `path`
   names one row. The cost: DI:959's "always `[]` in version 1" and APO/ov:620 change, a
   consumer that asserted `[]` sees entries only when it passes the flag, and what `[]` then
   means is Decision 12. B makes the version depend on a flag; C leaves the reserved field unused
   and is one more opt-in key beside #29's, which its "only exceptions" sentence would have to
   name (#29 `specs/project-overview/spec.md:282-287`).
3. **How deep does traversal go?** (A) Declared working siblings only, one level beside the
   holder: no member's legs, no pinned copies under `members/`, no nested family, a sibling that
   is itself a holder being a row of kind `family-holder` (APO/ov:24-30) whose own members are not
   read. (B) A plus each member's legs. (C) A plus the pinned copies. Recommended: A. Legs are
   mounted as submodules of their assembly root (ORS `contracts/repository-naming.yaml:348-360`,
   `1a9fc53`) and pinned copies are submodules of the holder (ORS
   `contracts/repository-naming.yaml:392-393`, `1a9fc53`; ORS `family.yaml:15-17`); change 2 gives
   a submodule checkout an `unsupported-layout` repair error (APO/ov:97-102); pinned copies are
   detached by design (ORS `siblings.py:28-30`) and inside the holder's own checkout; a member is
   another project's assembly root (ORS `family.yaml:15-19`), which `project` too reads only as a
   project (project:853-854). The bounds are Decision 11.
4. **How is each member's state reported, and is it a finding?** Candidate states, one per
   entry, with `reason` a closed enum that is null unless listed:
   - `present`: the sibling, its one link resolved (Decision 8), is a candidate holding
     `project.yaml` whose `id` passes openRepoShape's id test: a clone with no `id` passes, an
     entry with no `id` against a clone that has one does not (ORS `siblings.py:493-501`).
     `present` is weaker than `verify_sibling`, which first requires the clone's `origin` to name
     the row's `repository` (ORS `siblings.py:482-492`), a test this change defers (Alternatives),
     so a `present` sibling can still be a clone of another repository.
   - `not-a-project`: a directory without `project.yaml` (O3's `api`), which may still be a row of
     kind `single` (APO/ov:29-30), or a sibling that is itself a holder (Decision 3).
   - `mismatched`: the id test fails.
   - `missing`: the resolved path does not exist or is not a directory; `found_at` names a row
     elsewhere whose manifest `id` equals the entry's, from manifests already read and with no
     search (O3's `billing`), else null.
   - `invalid`: `not-a-mapping`; `bad-name`, no `project` or `name`, a non-string, or one outside
     `[A-Za-z0-9_-]+` (project:850); `names-holder` (O10); `duplicate`, a name an earlier entry
     took, the first kept, where `status` refuses the whole family (O15; project:823-826);
     `outside-folder`, a link whose target leaves the holder's parent, where `status` refuses
     (O18).
   - `unknown`: `manifest-invalid`, the sibling's own manifest refused (unreadable, malformed,
     wrong kind, invalid text, over 1 MiB, or no YAML library), the refusal staying on the
     sibling's own row (APO/ov:326-347; F005 FR-023, `spec.md:2592-2598`), where `status`
     refuses (O16); `probe-timeout`, `deadline-exceeded` or `os-error`, the check cut or failed;
     `candidate-cap`, `member-cap` or `check-cap`, the check never made (Decisions 10, 11).

   A sibling whose repository identity joins another row, such as a linked worktree of another
   repository, merges into that row (APO/ov:342-343): `row` names that row, and `reason` is
   `merged-row` beside its state. Extras, undeclared directories in the family folder, are not
   reported: listing the folder reads one level below a root's immediate entries, which
   APO/ov:18-19 bars, and the folder also holds the estate's own files (ORS `siblings.py:16`);
   the packet prefers bounded discovery with explicit additional roots (DI:1789-1791 at
   `15504f1`).

   Two effects stay apart. A member's state is informational: no state changes any row's status,
   the summary, `completeness` or the exit. The family check being cut or capped is
   incompleteness, recorded as change 2 records every cut or capped unit. A sibling check is the
   holder row's own task in this change, so a cut check records `probe-timeout` or
   `deadline-exceeded` on the holder's row, as change 2 records a cut row task (APO/ov:183-188),
   and the row's status becomes `error` (APO/ov:341-342); a scan error stays for what change 2
   makes one, a cap (APO/ov:222-224) and the deadline's count of candidates not started
   (APO/ov:180-181). Either makes the run incomplete (APO/ov:654-655), so it exits 1
   (APO/ov:762-764); the entry keeps its `unknown` state. As findings: (A) informational only,
   states in `relationships` and the human lines, no finding code. (B) A new code such as
   `family-member-missing`. (C) Findings for `invalid` and `mismatched` only. Recommended: A. A
   member not cloned is ordinary work (APO proposal.md:154-156) and "a project that belongs to no
   family is reviewed identically" (ORS `family.yaml:23-25`); the finding table is closed for
   version 1 (APO/ov:421-422); #29 isolates its evidence the same way (#29 proposal.md:121-126).
   doctor's `error` for a missing member (project:897, O5) is untouched, so the two commands
   differ.
5. **What deadline and budget share does it get inside the overview's 60 s?** (A) None of its
   own: sibling checks are bounded filesystem tasks, each waited for with `min(5 s, deadline -
   now)` under the 60 s deadline (APO/ov:183-188), and sibling probes are ordinary collection;
   the four-at-once limit governs Git children only (APO/ov:236-238); so the 64 s run bound holds
   (APO proposal.md:483-487). (B) A family phase after collection with its own budget, like #29's
   `min(30 s, deadline - now)`. (C) A reserved slice of the 60 s. Recommended: A. Siblings that are
   candidates stay under the candidate cap, which bounds the Git children at the measured worst
   case of 48.3 s (APO proposal.md:598-605); the sibling filesystem tasks lie outside that
   measurement, and Decision 11 bounds them; no new kind of Git child starts, but a
   discovery-phase manifest task does (Decision 10). B would compete with #29's phase for the
   same remainder. Risk: a `--families --remote` run leaves #29's phase less time (Risks).
6. **What is the human form?** (A) Under the holder's header, one line per declared member:
   `member` padded to 14 columns as a category is (APO design.md:516-518), then `<name>: <state>`,
   the reason in parentheses when there is one, and the sibling path or `found_at`, each printed
   by What Changes' path and string rule (APO/ov:672-675); member rows keep their own headers;
   the lines hide under `--attention` as informational findings do (APO/ov:466-469), so they show
   only under a holder row shown for another reason. Before the summary in a flagged run, one
   line, `Families: H holders examined, M members; present a, not-a-project b, mismatched c,
   missing d, invalid e, unknown f.`, counting every holder entry and every member entry, and
   printed under `--attention` too, as #29 prints its `Remote:` count line (#29
   `specs/project-overview/spec.md:587`), since a count is not a finding. (B) A separate section
   after the rows. (C) A suffix on each member row's header. Recommended: A. The family is read
   where it is declared, other rows stay as change 2 prints them, and #29 reads the layout as
   allowing added lines without a MODIFIED block (#29 proposal.md:1041-1044).
7. **What must `clean --all-safe` and the other commands never infer from a relationship?**
   (A) All of: no suggestion names a holder for a member's worktree, or any command across
   members, every suggestion staying per repository root (APO/ov:484-487); `--all-safe` plans
   one repository and never a sibling or member (CAS/pc:568-571) and never reads a relationship;
   a relationship state changes no classification, finding, gate, row status, summary count,
   `completeness` or exit, the incompleteness that a cut or capped family check records
   excepted (Decision 4); it is kept nowhere beyond the invocation (APO/ov:714-716), so no
   `status`, `doctor`, `update` or `clean` run, `plan_digest` or revalidation can read it; no
   clone, bootstrap or fetch of a missing member is suggested, as openRepoShape owns those
   (README.md:264); and membership grants nothing (ORS `repository-naming.yaml:13-18`). (B) Rely
   on change 2's "Grouping grants nothing" (APO proposal.md:157-158) with no new scenario.
   Recommended: A, stated in the ADDED requirement with a scenario each, since SY:34-37 names
   the risk, the packet holds that "No layout or family membership changes authority" (OV:395-397
   at `15504f1`), and B leaves it untested.
8. **Where is the sibling, and which key names it?** (A) `<holder parent>/<project>`, else
   `<holder parent>/<name>`, as project:849-852 reads it; a symbolic link there is resolved once
   and read at its target (APO/ov:19-20), as `status` reads a link inside the folder (O19), and
   is deduplicated with the candidates by device and inode (APO/ov:32-34). (B) The declared
   `path:`. (C) Both. Recommended: A. It is where openRepoShape clones the working copy (ORS
   `siblings.py:12-15`, built from `project:` alone at :532-534 and :706-708; the `name`
   fallback is `project`'s own) and where `status` already looks, so the two commands agree on
   the place; `path:` is always `members/<project>`, the pinned copy (ORS `family.py:443-445`).
   They differ on refusal: `status` refuses the whole command on a bad or repeated entry, a
   wrong-kind sibling manifest, a non-list `members` or a link out of the folder (O9, O15 to
   O18), where the overview reports the entry or the holder and goes on (Decisions 4, 9).
9. **Which holders yield relationships, and what does a bad member list give?** (A) Every holder
   in the run, from its manifest, with no Git child: one with no `.git`, its row keeping null
   Git fields and no error (APO/ov:66; O7), and one whose identity probe reports an enclosing
   repository, likewise (A1 `spec.md:98-100`; F005 FR-003, `spec.md:2126-2128`). A holder whose
   `family.yaml` is refused keeps its `manifest-invalid` row error (APO/ov:326-328) and yields
   no member entry, its holder entry `unknown` with reason `manifest-invalid`; an absent
   `members` yields none; a `members` that is not a list (null, a mapping) yields none and its
   holder entry is `invalid` with reason `members-not-a-list`, never a refusal (contrast O17).
   (B) Only holders that are Git toplevels. (C) A, but a non-list `members` is the holder row's
   `manifest-invalid` error. Recommended: A: the members list needs no Git child, a holder
   outside Git is the case in which a person most needs to see its members, and C lets a member
   list change a row's status, against Decision 4.
10. **Where does sibling expansion run in the ratified pipeline?** In change 2 the holder's
    manifest is read inside its collector, after the identity probe (DI:627-637 at `15504f1`,
    DI:515-525 at `da33d92`; APO/ov:318-320), and candidates are sorted and capped before
    collection is dispatched (APO/ov:32-34, :221-222; APO design.md:385-386), so the members list
    is not known when the candidate list is final. (A) Discovery sorts and caps once, reads the
    manifest of each holder that survives the cap in one bounded task (at most 128, each waited
    for as APO design.md:450-452 and :456-460 wait a manifest read), adds the declared siblings,
    sorts again and applies the candidate cap again; a candidate a sibling displaces joins the
    candidate cap's
    exact `omitted` count, and a sibling past the cap is `unknown` with reason `candidate-cap`;
    the holder's collector reuses the result. This departs from DI:627-637 and from APO design.md
    D2 (:134-137, the root task lists and checks markers only), D6 (:385-386) and D8 (:454-460).
    (B) Siblings join after the cap, as candidates outside it, bounded only by Decision 11: no
    departure in discovery, but the 128-candidate cap no longer bounds the Git work that the
    48.3 s measurement covers (APO proposal.md:598-605). (C) Siblings never become candidates
    unless they are immediate entries of a root: relationships come from the sibling checks and
    from rows already present, with no departure, but in openRepoShape's layout the member clones
    get no row (Why) unless the family folder is given as a root (APO/ov:67). Recommended: A. A
    row is what shows a member clone's Git health, the gap this change answers (Why); the
    departure is bounded by the candidate cap; and siblings stay under the cap the measurement
    covers. C is the fallback if Brett Heap wants no departure in the pipeline.
11. **Which caps bound the family checks, in what order, and where are they reported?** Scope:
    (A) 128 entries per holder and 512 sibling checks per run, each after canonical sorting,
    entries by member name bytes then declared index, as the other caps apply after sorting
    (APO/ov:221-222), holders in canonical order. (B) 512 per run only. (C) 128 per holder only,
    which lets 128 holders start 16,384 checks bounded by the deadline alone. Each cap that drops
    work is a `scan-limit` scan error, `limit` `family_members` or `family_checks`, with an exact
    `omitted` (APO/ov:222-224), and the entries past it are `unknown`, reason `member-cap` or
    `check-cap`. Reporting: (i) `limits.family_members` and `limits.family_checks` in a flagged
    run only, additive within version 1 (APO/ov:656-658; APO design.md:563-564) but one more
    exception to "exactly these fields, every one always present" beside #29's two `remote` keys
    (#29 `specs/project-overview/spec.md:282-287`), so criterion 11's flagged differences name
    them and the second change to archive re-bases that sentence
    (Dependencies). (ii) Both keys in every run: one field list, but the default document changes,
    against Decision 1. (iii) A `families` envelope object with its own `limits`, as #29 keeps its
    caps in its `remote` object (#29 `specs/project-overview/spec.md:526-536`), the same exception
    count as (i). A cap in no `limits` key would break "the values in force are always reported
    in `limits`" (APO/ov:219-220) and A1's `scan-limit` message, whose M is "its value in
    `limits`" (A1 `spec.md:402`). Headroom: the caps' measured worst case takes 48.3 s of the 60 s
    deadline (APO proposal.md:598-605), leaving 11.7 s. A sibling check costs about one entry of a
    root's marker pass (APO design.md:134-137), and task 2.1 measured a 4,096-directory root at
    0.36 s warm and 2.6 s projected cold (APO tasks.md:20); scaled, 512 checks take about 0.05 s
    warm and 0.33 s cold, and option C's 16,384 about 1.4 s warm and 10.4 s cold. UNVERIFIED:
    scaled, not measured; an OQ-4-style run (APO tasks.md:20) with 128 holders of 128 declared
    members would verify it before the values are fixed. If each holder's checks run in one task,
    as a root's entries do (APO design.md:134-137), the abandoned-worker bound (APO
    design.md:477-479) gains at most 256 tasks, one manifest read and one check task per holder.
    Recommended: A with (i). A bounds both one large family and many families; (i) reports the
    caps as change 2 reports every other cap and as A1's message reads; (ii) breaks Decision 1.
12. **What does `relationships: []` mean?** Without the flag it means not examined; with it,
    under Decision 2 A, it could also mean that no holder declares a member, while change 2 keeps
    "unknown or not established" for null, never for an empty list (APO/ov:652-653). (A) In a
    flagged run, one entry per holder examined, `{"type": "family-holder", "holder",
    "holder_valid_utf8", "members": <count or null>, "state", "reason"}`, state `examined`,
    `invalid` or `unknown` (Decision 9): with `family-holder` rows in `projects`, no holder entry
    means not examined, and a holder entry with `members: 0` means none declared; no new key.
    (B) `relationships: null` without the flag: "not examined" in change 2's own terms, but the
    default document changes (Decision 1), and so does APO/ov:620. (C) An envelope field such as
    `families: true` in a flagged run, one more exception to #29's sentence (#29
    `specs/project-overview/spec.md:282-287`). Recommended: A. It needs no new key and no change
    to a default run, a consumer tells the two cases from the `projects` rows it already reads,
    and it gives Decision 9's holder conditions their place.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

Intent only; no delta file is written (Status).

- `project-overview` (change 2's, unarchived): MODIFIED "Overview discovers projects within
  configured roots only" (APO/ov:10), for the flag's carve-out; MODIFIED "Overview prints a
  versioned JSON envelope" (APO/ov:606), for `relationships` and, under Decision 11 (i), the two
  `limits` keys; MODIFIED "Overview bounds its work and reports what it omitted" (APO/ov:166), for
  Decision 11's caps, which join those listed there (APO/ov:217-224), and Decision 10's
  discovery-phase manifest read; ADDED "Overview reports family relationships on request". Read
  as they stand, not modified: "Overview isolates one candidate's failure" (APO/ov:317-347),
  whose boundary keeps a sibling's own failure on its own row (What Changes, isolation). The
  other requirements stay untouched, "Overview renders a readable human report" under #29's
  reading (Decision 6).
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
  32 roots, 128 manifests, 512 rows, 512 reflog reads and a handful more)": Decision 11 adds up
  to 256 tasks.
- Under Decision 10 A, the pipeline order: DI:627-637 at `15504f1` (`manifest()` after the
  identity probe, inside the collector) and APO design.md:134-137, :385-386 and :454-460.
- Under Decision 11 (i), APO/ov:610-614's exact `limits` keys and #29's "these two keys are the
  only exceptions" (#29 `specs/project-overview/spec.md:282-287`).
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
declared names only (Decision 3); the holder is one row (APO/ov:36-37); its probes follow its own
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
  `spec.md:94-102`; A1 proposal.md:1203-1211, Q11 A). The deltas are written on change 2's text
  with A1 merged.
- **#29, add-project-overview-remote-merge-status** (lane openRepoProject-5, draft). It MODIFIES
  "Overview prints a versioned JSON envelope", carrying "`relationships`, always `[]`" (#29
  `specs/project-overview/spec.md:228`, :242), and also "Overview bounds its work and reports what
  it omitted" (:51) and "Overview is local and read-only" (:3), and ADDS a remote phase after
  collection (:431). Lane 5's rule, stated for change 1's evidence model that it shares with #26:
  "whichever of the two archives second re-bases its block on the other's archived block before
  it archives" (L-11, #29 proposal.md:578-579; L-17, :658-662). This change would share the
  envelope requirement, and with Decision 11's caps the bounds requirement, so the same rule
  applies. Under Decision 11 (i), Decision 2 C or Decision 12 C, the two would also share #29's
  sentence that its two `remote` keys "are the only exceptions to 'exactly these fields, every
  one always present'" (#29 `specs/project-overview/spec.md:282-287`); the second to archive
  re-bases that sentence too. No text read here orders the two; the rule makes either order
  safe. #29 also says `--remote` "SHALL combine with every other overview option" (its
  `spec.md:349`), so its remote phase would query sibling rows like any worktree row.
- **#27 and #26** (heads `9473b2c` and `6c7c0f9`, re-read). #27 (cache disposal) MODIFIES
  "Overview reuses the cleanup classifier and merge target" (#27
  `specs/project-overview/spec.md:3`), which this change does not touch: same capability,
  archive order only. #26 (branch retirement) has no `project-overview` delta (its deltas are
  `project-clean`, `project-clean-review-safety` and `project-command`): no shared statement.
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
   relationships and probe ownership" included (APO/ov:63-67), and the JSON and human output,
   timestamps and `budget.probe_concurrency` apart, equal those of the same run of the build
   without the extension.
2. With the flag over `FX`'s `acme` estate as a child of the root, `billing`'s `project.yaml`
   given `id: billing`: rows for the holder, `web`, `api`, `billing` and `tools`;
   `relationships` holds the holder entry (`examined`, `members: 4`), `web` `present` with `row`
   its row, `api` `not-a-project`, `ghost` `missing` with `found_at: null`, and `billing`
   `missing` with `found_at` its row; no row and no Git child for anything under `members/`.
3. With the family folder as the root, each sibling has one row and one probe set, and
   `probes.performed` equals the same run's count without the flag; a sibling that is a linked
   worktree of another row merges into that row, its entry's `row` naming it with reason
   `merged-row`.
4. Malformed entries: `../evil` is `invalid`, `bad-name`; a non-mapping, `not-a-mapping`; a
   repeated name, `duplicate`, the first kept (contrast O15); a member named like the holder,
   `names-holder`, the holder probed once (contrast O10). The other entries are reported, and
   the exit is what the run gives without the flag, never 2 (contrast O9).
5. Holders: one with no `.git` and one inside an enclosing repository both yield their entries
   and keep null Git fields and no error (Decision 9); a refused `family.yaml` gives the holder
   entry `unknown`, `manifest-invalid`, its row error standing; `members: null` and a mapping
   give `invalid`, `members-not-a-list` (contrast O17); an absent `members` gives `members: 0`.
6. A sibling manifest with invalid UTF-8, one over 1 MiB, one of the wrong kind (contrast O16),
   and any sibling manifest in a run without the YAML library: the entry is `unknown`,
   `manifest-invalid`, the refusal is on the sibling's own row, and the other entries are
   reported.
7. Links: a sibling that is a link inside the family folder is read once, at its target (as
   O19), and deduplicated with the candidates; one whose target leaves the holder's parent is
   `invalid`, `outside-folder` (contrast O18).
8. Ids: an entry `id: web` against a clone `id: www` is `mismatched`; an entry with no `id`
   against a clone with one is `mismatched`; a clone with no `id` is `present`; a missing
   member whose `id` is in no manifest read has `found_at: null`.
9. A member declared with `name:` and no `project:` is read at `<holder parent>/<name>`.
10. Caps: one holder declaring 130 names with no directory, so that the candidate cap cannot
    trip: the first 128 in member-name order are checked, the other 2 are `unknown`,
    `member-cap`; one `scan-limit` with `limit: "family_members"`, `{"count": 2, "exactness":
    "exact"}` and the message "family_members cap of 128 reached" (A1 `spec.md:402`);
    `limits.family_members` is 128 under Decision 11 (i); the run is incomplete and exits 1
    (APO/ov:654-655, :762-764). Five such holders of 128 names: the checks past the 512th are
    `check-cap`.
11. No relationship state changes a classification, finding, suggestion, status, summary count,
    `completeness` or exit, the incompleteness a cut or capped check records excepted. The `FX`
    run of criterion 2 with and without the flag differs only in `relationships`, in
    `limits.family_members` and `limits.family_checks` (Decision 11 (i)), in the rows of `web`
    and `api` and their findings, in `summary.projects`, `summary.repositories` and
    `summary.worktrees`, each 2 higher (APO/ov:643-645), and in `probes.estimated` and
    `probes.performed`, each 10 higher, two Git candidates of one worktree row each costing
    1 + 3 + 1 (APO/ov:248-254). No suggestion names a holder
    for a member's worktree; `project clean <holder> --all-safe` selects no member's worktree.
12. A held sibling `stat` records `probe-timeout` on the holder's row, whose status becomes
    `error`, and the entry is `unknown`, `probe-timeout`; the run is incomplete and exits 1
    (APO/ov:654-655, :762-764); at the deadline the code is `deadline-exceeded`; the other
    entries are reported.
13. `--attention` hides the member lines, still prints the `Families:` line, and changes no
    JSON; `--attention --json` prints the full envelope (APO/ov:471).
14. The `Families:` line of criterion 2 counts 1 holder examined and 4 members: present 1,
    not-a-project 1, missing 2, and mismatched, invalid and unknown 0 (its exact wording is the
    design's).
15. Entries sort by holder path bytes, the holder entry first, then by member name bytes, then by
    declared index, entries with no name last; every `reason` is one of Decision 4's and
    Decision 9's codes.
16. Paths and strings: a member name holding U+202E and a `declared.path` holding the byte
    0xFF are escaped in JSON by A1's string rule; a holder path that is not valid UTF-8 has
    `holder_valid_utf8: false`; the human `member` line prints such a path in `$'...'` form.
17. Combinations: `--families --remote` prints both opt-in outputs and neither changes the
    other's (#29 `specs/project-overview/spec.md:349`), sibling rows being queried as any row;
    under `--families --strict` no member state changes the exit, which only warnings of
    findings change (APO/ov:763-765).
18. A sibling that holds `family.yaml` and no `project.yaml` is a row of kind `family-holder`,
    its own members unread, and its entry is `not-a-project`.
19. Read-only and offline: zero-mutation snapshots, no network, no fake owner tool called.

## Risks

- openRepoShape owns the layout (README.md:264); if the sibling placement moves, both `status`
  and the overview read the wrong place. The overview copies `project:852`'s rule; pinning it by
  sha, as project:204-211 pins the name forms, is the design's choice.
- Siblings add candidates, so the 128-candidate cap (APO/ov:217-222) binds sooner and a large
  estate run ends incomplete more often, visibly: an inference from the cap, not measured.
- The sibling checks' cost is scaled, not measured (Decision 11, UNVERIFIED); the values wait for
  a measurement like task 2.1's (APO tasks.md:20).
- Decision 10 A changes the order change 2's design fixed (DI:627-637 at `15504f1`; APO design.md
  D2, D6, D8), and a candidate kept without the flag can be displaced by a sibling with it.
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
  overview needs one; their family readings (O3 to O19) stay as they are.
- Legs, pinned member copies and nested families (Decision 3); undeclared directories in a
  family folder (Decision 4).
- openRepoShape's family mechanics: `bootstrap`, `siblings`, `family.py` and
  `validate-family.py`, which the overview never runs (APO/ov:711).
- A command that clones, moves or repairs a member.
- The family folder itself, never a candidate: feature 005's recorded edge case EC-025, kept by
  Brett Heap's Q10 A (F005 `spec.md:1871-1878`, :812-814).

## Alignment review applied (2026-10-22)

Two final reports on `5aacbec`, the stack-architect's (M1, M2, G1 to G6, D1 to D4) and the
QA-lead's (QA-1 to QA-16), 28 findings, applied under the lane lead's rulings of fix round 1;
overlaps were treated once. Still an observation record: no delta, `design.md` or `tasks.md`.

- M1: the code-reading sentence now says the cycle check fires on two entries naming one
  directory; run O15 added (`FX/projects-dup`, exit 2 on 3.12 and 3.10); Decision 4 `duplicate`.
- M2: Decision 4 cites APO/ov:18-19 for the bar on listing the family folder, DI:1789-1791 for
  the packet's preference only.
- G1: new Decision 10, where sibling expansion runs, with the departures it names; What Changes
  points there; statements made false list them under Decision 10 A.
- G2: Decision 5's reason corrected (5 s per filesystem task; four at once is Git only); the
  run-wide bound and the headroom are Decision 11; Capabilities no longer makes the cap optional.
- G3: Decision 11's reporting options (i) to (iii); criterion 11 names the `limits` keys;
  Dependencies names #29's "only exceptions" sentence (its `spec.md:282-287`).
- G4: What Changes, "Paths and strings", a candidate requirement; Decision 2's object carries the
  flags; Decision 6 prints by that rule; criterion 16.
- G5: Decision 4's state table (`manifest-invalid`, `duplicate`, `outside-folder`, `merged-row`)
  and Decision 9 (refused holder manifest, non-list `members`); Decision 8 says where `status`
  and the overview differ; runs O16 to O19; criteria 3 to 7.
- G6: statements made false gain the packet bullet (DI:51-55, :333-337, :959, :1276,
  :1759-1769; OV:48-49) and F005's records; Decision 7 cites OV:395-397.
- D1: incompleteness cited to APO/ov:654-655, the cap to APO/ov:222-224 (Decisions 4, 11).
- D2: with QA-1, a cut sibling check is recorded on the holder's row; a scan error only for a cap
  or the deadline's count (Decision 4).
- D3: Decision 4's `present` follows `verify_sibling`'s id test (ORS `siblings.py:493-501`) and
  says that the origin test (:482-492) is deferred.
- D4: with QA-10, Decision 3 cites ORS for legs and pinned copies as submodules.
- QA-1: Decision 4 and criterion 12 record a cut check on the holder's row (APO/ov:183-188).
- QA-2: Decision 11 and criterion 10 cite APO/ov:654-655 and :762-764 for incompleteness and
  exit.
- QA-3: statements made false add APO/ov:67, A1 `spec.md:70`, :72 and F005 `spec.md:960-970`.
- QA-4: Decision 11 fixes the order (member name bytes, then declared index) and the `limits`
  key; criterion 10.
- QA-5: Decision 5 says the 48.3 s covers Git children only; Decision 11's run-wide cap and
  headroom arithmetic, marked UNVERIFIED; APO design.md:477-479 in statements made false.
- QA-6: new Decision 12, the holder entry, so that `[]` is never ambiguous.
- QA-7: Decisions 4 and 9 and criteria 5 and 6; What Changes, "Isolation"; Capabilities says the
  isolation requirement and the review-safety carve-out are read, not modified.
- QA-8: Decision 9 and criterion 5 cover a holder inside an enclosing repository (A1
  `spec.md:98-100`; F005 `spec.md:2126-2128`).
- QA-9: heads re-fetched and updated (feature 005 `41cf866`, #26 `6c7c0f9`, #27 `9473b2c`; #29
  and A1 unchanged); F005 lines re-pinned at `41cf866`.
- QA-10: Decision 3 cites ORS `contracts/repository-naming.yaml:348-360` and :392-393 at
  `1a9fc53`.
- QA-11: criteria 1 and 8 to 18 (byte-identical default, ids, name fallback, caps, deltas, cut
  check, `--attention`, `Families:` counts, sort key and closed `reason`, strings, combinations,
  nested family); Decision 6 defines the `Families:` line.
- QA-12: What Changes, "Paths and strings" (A1 `spec.md:385-390`, :402, :748-752); criterion 16.
- QA-13: Decisions 4 and 7 and criterion 11 separate a member's state from a cut or capped check.
- QA-14: statements made false add APO proposal.md:162-163 and APO design.md:456-458.
- QA-15: Decision 8 resolves a link once (APO/ov:19-20); Decision 4 `outside-folder`; O18, O19;
  criterion 7.
- QA-16: only "examine each root and its immediate entries only" is listed as made false;
  "never recurse" moves to "Kept true".
