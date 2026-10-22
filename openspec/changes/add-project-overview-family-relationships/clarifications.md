Lane: openRepoProject-1

# Clarifications

_Captured during the proposal council review of 2026-10-22 (lane openRepoProject-1). These constrain the later design.md._

## Council-Identified Constraints

The council's three reports are council-product.md (PA-1 to PA-4), council-architect.md (SA-1 to
SA-4) and council-adversary.md (AE-1 to AE-5), in
`/workspace/projects/.scratch/openRepoProject-1-wave6-20261022/`, on `proposal.md` at `b8a1b55`.
The lane lead's verdicts of 2026-10-22 (council-verdicts.md there) marked these five concerns
NOTED: each is recorded here as a constraint on the later `design.md` and was not applied to
`proposal.md`, which stays an observation record with no delta, design or tasks. Decision ids
(T1-n, T2-n) are those of `proposal.md` after the council round; "T1-2 A" and the like name the
option. Citations follow `proposal.md`'s key: `APO/ov` is
`openspec/changes/add-project-overview/specs/project-overview/spec.md`, `ORS` is openRepoShape
origin/main `038dafb`.

### Family-check cost, a worker bound and a re-measurement

**Raised by:** the systems-architect, council-architect.md, Concern 2 (MEDIUM; verdict SA-2,
NOTED). Its measurements are in the report's verification record (`yamltime.py`, `gil.py`,
`gil2.py`).

**Concern:** a sibling check is a `stat`, a scan of the marker files and a manifest parse, and the
parse is pure Python under the GIL (`read_yaml` calls `yaml.safe_load`, project:37-47). On Python
3.12.3 with PyYAML 6.0.3 a real 5,274-byte `project.yaml` parses in 5.46 ms and the real
4,621-byte `family.yaml` in 4.58 ms; 512 parses took 2.15 to 2.42 s; a synthetic `family.yaml` at
the 1 MiB bound (3,057 members) takes 3.25 s, 0.63 s with the C loader. In a stand-in for the
control loop (a pipe and a selector, not the real scheduler) one parsing thread slowed 2,000 loop
events from 7 ms to 63 ms, four threads parsing continuously stretched them to 35,982 ms, and 512
parses split over 16 threads let the loop finish 50 events of 3,000. The ratified design caps Git
children at four (APO/ov:236-238) and states no bound on simultaneous filesystem tasks (APO
design.md D1, D8); D8's abandoned-worker bound counts threads (APO design.md:477-479), but a
CPU-bound parse cannot be cancelled after its 5 s wait expires. The entry cap bounds the number
of checks, not the cost, which follows file size up to 1 MiB. The drvfs mount of WSL2 was not
measured by task 2.1 (APO design.md:727-729), and sibling checks multiply the round trips per
family.

**Design impact:** `design.md` must:
1. fix a worker bound for family filesystem tasks, beside the Git bound of four: at most
   `probe_concurrency`, or one thread; each task appends its finished entries as D2 does, so a
   cut keeps what finished;
2. keep one per-run manifest cache keyed by (device, inode), so that no file is parsed twice (a
   sibling's own collector reads its manifest again, and T1-2 A reads the holder in discovery
   and again in its collector);
3. decide whether the shared reader `read_yaml`, which `status` and change 1 also use, may use
   the C loader when it is present, or record "pure-Python parse under the GIL" as the cost
   model;
4. re-measure before the cap values are fixed, in the style of OQ-4 (APO tasks.md:20): real 5 KB
   manifests, 128 holders of 4 members and 128 holders of 128 members, and one adversarial 1 MiB
   `family.yaml`, recording event-loop latency as well as wall time;
5. take one run-wide cap (T2-1, cap scope B) as the CPU bound: the per-holder 128 adds a second
   `limits` key and `scan-limit` value for a fairness that nobody has asked for, and the only
   family on this estate has 2 members, so 128 and 512 are 60 to 250 times what exists.

### One member-entry reader, and parity with `status`

**Raised by:** the systems-architect, council-architect.md, Concern 4 (MEDIUM; verdict SA-4,
NOTED in part: the `present` rule and the dual-manifest holder were applied to `proposal.md`).

**Concern:** the overview would copy `snapshot()`'s member rules (project:849-856) and a weaker
form of openRepoShape's sibling id test, and `proposal.md` keeps `snapshot()` out of scope
(Out of Scope), so the copies can drift from their sources. The first edges tried already
diverged: openRepoShape's `project_id()` returns `str(data.get("id"))`, so a clone with no `id`
key reads `'None'` and fails against an entry with an `id`, where a clone with no `project.yaml`
or an unparseable one passes (ORS `templates/family-root/scripts/siblings.py:755-779`,
`:868-876`; idtest.py in the report); and `manifest()` reads `project.yaml` before `family.yaml`
(project:422-430) while the marker table makes `D/D/family.yaml` the holder (APO/ov:26-28), so a
fixture `both/both` holding both files, `family.yaml` declaring `web` and `ghost`, gives
`status both --json` kind `project-manifest` and `children: []`. Further: `inside()` resolves
with `Path.resolve()` on the calling thread (project:51-57), which APO design.md:475-476 rules
out for the overview; and "holder parent" is undefined when a row's `path` (`repository.root`)
differs from the holder candidate, for a linked worktree of the holder's repository, because the
manifest is read at `repository.root` (APO/ov:318-320) while `status` uses `discover()`'s `D/D`.
Four tools (`status`, `doctor`, the overview and openRepoShape's siblings) can give four verdicts
on one folder.

**Design impact:** `design.md` must:
1. extract one pure function in `project`, for example `family_member_entries(data)`, returning
   for each entry its index, its name and a reason from T1-4's closed set; `snapshot()` calls it
   and refuses on the first reason, so its behaviour is unchanged, and the overview records
   them. The refactor is cheap now, because change 1 already edits `snapshot()`'s nested rows
   (CAS/cmd:35-36). Out of Scope of `proposal.md` then allows it;
2. add a parity test table: one fixture set (O9, O15 to O19, plus a directory with both
   manifests, a clone with no `id` and a malformed manifest) run through `status` and the
   overview, each `status` refusal mapping to one overview reason;
3. mirror openRepoShape's id test exactly, or name the state so that it does not claim the
   owner's verdict;
4. read `family.yaml` for members only when the marker kind and the manifest kind agree, else
   `unknown` with `manifest-invalid`, never `members: 0`; define "holder path" as the
   marker-found candidate's path; and cover the flat layout `D/family.yaml` (marker row 3,
   APO/ov:28), where the holder's parent is the root and the siblings are already rows.

### Constraints if member rows are ever chosen

**Raised by:** the adversary-engineer, council-adversary.md, AE-1 (HIGH; verdict AE-1, NOTED for
its five constraints; the recommendation itself, T1-2 C, was applied to `proposal.md`).

**Concern:** T1-2 A makes siblings candidates, caps the candidate list twice and reads the
holder's manifest in discovery. Under it one holder's read outcome adds and removes other rows,
the cap can split a family so that the holder has no row, the `omitted` count is called exact
when the population was not enumerated, and the manifest is read per candidate where change 2
reads it per row. Evidence: APO/ov:322-324 ("a failure SHALL become data on that candidate's row
and SHALL NOT change, remove or reorder any other row"); APO/ov:224-229 (`exact` only "when the
whole population was enumerated"); APO/ov:243-249 (the document does not depend on completion
order; `performed` counts every Git child started); APO/ov:318-320 and APO design.md:456-457
(the manifest read at `repository.root`, inside the collector). The adversary's model of the
option as worded (FA/scripts/model_decision10a.py; a model of words, not of code, since no
overview code exists): 120 single candidates, a holder `/p/m/m` declaring `b01` to `b12`, ten
more candidates; the holder is kept in the first pass and dropped in the second, eight members
are kept as rows, four are past the cap, and seven ordinary candidates are displaced, because
siblings sort before their holder by bytes (APO/ov:32-34). Timing: the final list waits for the
slowest holder read and then the slowest sibling check, up to 10 s of the 11.7 s that the 48.3 s
worst case leaves (APO proposal.md:601-603), or candidates start before the list is final and a
displaced candidate's children are counted in `probes.performed`. Race: a sibling read twice, in
the discovery check and by its own collector, with no rule for which read decides the entry.

**Design impact:** if Brett Heap rules T1-0 B or T1-2 A, `design.md` must carry these five
constraints:
1. a family enters and leaves the cap as a unit: a holder past the cap takes its siblings with
   it, and no sibling is kept without its holder;
2. the candidate cap's `omitted` is `lower-bound` whenever a holder's read was cut, or a holder
   past the first cap was never read;
3. there is one holder entry per row, from the manifest that the row's collector reads at
   `repository.root`; the discovery read only schedules siblings;
4. the dispatch rule is stated, either waiting for the final list or starting early and keeping
   displaced candidates' children out of `probes`, and it is measured;
5. APO/ov:224-229, :243-249 and :322-324 are listed under "Statements this change would make
   false".

The systems-architect adds, for the same case (council-architect.md, Concern 1): siblings never
displace a marker-found candidate; each candidate carries a provenance flag, so that only
marker-found holders yield entries (a directory that a sibling declaration adds and that holds
`family.yaml` is a `family-holder` row whose members T1-3 says are not read, where T2-5 says every
holder yields entries); and the holder's own displacement rule is stated. The full marker table
applied to a sibling `S` makes `S/S/family.yaml` yield the candidate `S/S`, so `sibling.path` and
`row.path` can differ.

### Entry identity by resolved path, and `found_at` ties

**Raised by:** the adversary-engineer, council-adversary.md, AE-5 (LOW; verdict AE-5, NOTED).

**Concern:** T1-4's states are keyed by the declared name. Two entries that reach one directory,
through a link inside the folder or as two spellings on a case-insensitive disk, are neither
`duplicate` nor merged: `duplicate` is "a name an earlier entry took", and siblings are
deduplicated "with the candidates", not with each other. `status` refuses two entries that name
one directory, through its cycle check (project:823-826; O15), and `inside()` would resolve an
alias `www -> web` to the same directory (project:54), which the adversary inferred from the code
and did not run. openRepoShape treats case-only spellings explicitly (`same_directory`,
`templates/family-root/scripts/siblings.py:1355-1369`, `038dafb`; "THE NAME TEST IS EXACT ON
EVERY DISK", `:1431`), and the design names a WSL2 drvfs mount as unmeasured (APO
design.md:727-729), which the adversary reads as a case-insensitive mount. For `found_at`:
independent clones stay separate rows (APO/ov:53-56), so two rows can share one id, and
`proposal.md` gives no rule for which row `found_at` names. Impact: one clone can count twice in
the `Families:` line and appear as two `present` members, and `found_at` may name either of two
clones; informational only.

**Design impact:** `design.md` must, after the name checks, deduplicate entries by the (device,
inode) of their resolved directory, the later entries being `invalid` with reason `duplicate`.
It must give `found_at` a tie rule: null with reason `found-ambiguous` when more than one row
matches (the adversary's), or the array form with `[]` and null kept apart (the systems-
architect's, T2-1); the design chooses one. Criteria 4 and 8 of `proposal.md` gain both cases.

### The Tier 2 envelope details, until the design rules them

**Raised by:** the product-advocate, council-product.md, Concern 3 (MEDIUM; verdict PA-3, VALID
for the two tiers and NOTED for these details).

**Concern:** Brett Heap was asked to rule now on envelope shapes, the earlier Decisions 2, 11 and
12, which are the content of the MODIFIED blocks that the proposal holds until A1 (PR #34) and
#29 settle; the rulings can be overtaken by either and then re-asked. Evidence: Decision 11's caps
128 and 512 and its "UNVERIFIED: scaled, not measured" arithmetic are mechanical and cannot be
verified by Brett Heap; Decision 2's three options on `schema_version` and `families` bind a
shape that #29's settled block can change; "Why the deltas wait" ("Written after both, once")
contradicted the proposal's own statement that the rule of lane 5 makes either order safe (#29
proposal.md:578-579, :658-662); and the one requirement that cannot collide with #29 is the
ADDED one, only the three MODIFIED blocks do. The tiers and the hold trigger were applied to
`proposal.md`; the Tier 2 Decisions are recommendations and constraints, not rulings.

**Design impact:** `design.md` starts from the Tier 2 recommendations of `proposal.md` and either
rules each one or records why it departs: T2-1 B (one optional `families` object, `relationships`
holding only `family-member` entries, `limits` untouched, cap scope A, the form of `found_at` left
open as above); T2-2 B while T1-6 is A, A if T1-6 is B; T2-3 A with the sub-question on `invalid`
and `mismatched` under `--attention` (recommended (i)); T2-4 A; T2-5 A. It says which Tier 1
rulings each depends on. The ADDED requirement is written once #34 merges; the MODIFIED blocks
shared with #29 are written on the same text and re-based at archive time under lane 5's rule,
"whichever of the two archives second re-bases its block on the other's archived block before it
archives" (#29 proposal.md:578-579; L-11 and L-17, :658-662), and no block waits for #29 to
settle. Each Tier 1 ruling that removes a Tier 2 question (for example T1-2 C, under which no
sibling is probed and no discovery-phase manifest is read) is said to, in the design, so that
the rulings are not carried as dead constraints.
