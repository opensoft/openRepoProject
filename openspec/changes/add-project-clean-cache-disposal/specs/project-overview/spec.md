## MODIFIED Requirements

### Requirement: Overview reuses the cleanup classifier and merge target
The merge target SHALL be resolved in the order that `Clean resolves its
target Git-first` defines, both `origin/` strips included, from the manifest
read at `repository.root` (at the row's `path` when `repository.root` is
null) and the ref listing alone, spawning no Git child, and SHALL be recorded
as `merge_target: {name, source, sha}`, with `source` one of `manifest`,
`origin-head`, `main` or `master` and `sha` that branch's full object id from
the same listing. The merged set SHALL be computed at that `sha`. When the
manifest and `origin/HEAD` name different branches that both exist locally,
the manifest SHALL win and one informational `merge-target-conflict` finding
SHALL name both. When no candidate branch exists, `merge_target` SHALL be
null, the row SHALL carry a `no-merge-target` repair finding of severity
error with no suggestion, the classification ladder SHALL NOT run, and every
worktree's `classification` SHALL be null; when the ref listing failed or
timed out, the row SHALL record that error instead, absence not being
established.

Each worktree row SHALL be classified by the ladder that `Clean classifies
preservation and cleanup actions` defines, with its names, order and
recommendation text, fed from the overview's collected evidence and spawning
no probe of its own. The ladder SHALL run on a row only when the row is within
the cap, its presence is established, and the registry, ref listing and
merged set succeeded; otherwise `classification` SHALL be null, except for the
rows that requirement sets to `inspection-error` directly. For every row that
the report of `project clean <repository.root> --json` inspects, from the same
working directory and the same refs, the row's classification SHALL equal what
that report gives it; that report leaves the rows beyond its own row cap
uninspected, while the overview classifies rows up to its own worktree-row cap
per run. Except: the overview collects no cache evidence, so a worktree that
`project clean` classifies `merged-removable` because clean's cache enumeration
proved every ignored path a listed cache SHALL be classified
`ignored-local-files` by the overview. The overview SHALL NOT classify a
worktree `merged-removable` where `project clean` classifies it otherwise for
the same working directory and refs.

#### Scenario: Manifest target
- **WHEN** a `project.yaml` sets `tracking_branch: origin/develop`, a local `develop` exists, and there is no `origin/HEAD`
- **THEN** `merge_target` is `develop` with source `manifest` and the object id of `refs/heads/develop`, and classification is relative to `develop`
- **AND** the merged set was computed at that object id, resolution spawned no Git child beyond the ref listing, and the name equals the merge target `project clean <root> --json` reports

#### Scenario: origin/HEAD target
- **WHEN** there is no manifest, `origin/HEAD` names `origin/trunk`, and local `trunk` and `main` exist
- **THEN** the target is `trunk` with source `origin-head` and the object id of `refs/heads/trunk`

#### Scenario: main target
- **WHEN** there is no manifest and no `origin/HEAD`, and local `main` and `master` exist
- **THEN** the target is `main` with source `main` and its object id

#### Scenario: master target
- **WHEN** only a local `master` exists
- **THEN** the target is `master` with source `master` and its object id

#### Scenario: Conflicting targets
- **WHEN** a manifest names `develop` and `origin/HEAD` names `main`, both existing locally
- **THEN** the target is `develop` with source `manifest`, and one informational `merge-target-conflict` finding names both branches
- **AND** the exit status is 0 when nothing else is found

#### Scenario: Missing target
- **WHEN** a manifest names an absent `release`, there is no `origin/HEAD`, and neither `main` nor `master` exists
- **THEN** `merge_target` is null, the row has a `no-merge-target` repair finding of severity error with no suggested command, every worktree's classification is null, and the exit status is 1
- **AND** on the same fixture `project clean <root> --all-safe` refuses with exit status 2 before any mutation

#### Scenario: Every protected classifier
- **WHEN** one repository's worktrees are classified `protected-default`, `dirty`, `ignored-local-files` (its ignored file not a Python bytecode cache), `detached`, `unpublished`, `remote-gone`, `diverged`, `remote-ahead`, `unpushed`, `merged-current` and `pushed-unmerged`, plus one gate-passing `merged-removable`, a second repository holds an `inspection-error` worktree whose corrupted index makes its status probe fail, and the overview runs from inside the `merged-current` worktree
- **THEN** every classification equals what `project clean <root> --json` reports from the same directory, and each finding has the category and severity of the attention table
- **AND** the only housekeeping finding and the only `--all-safe` suggestion belong to the `merged-removable` worktree, and no other worktree appears in the `selected` list of the batch preview that suggestion runs

#### Scenario: Caches that only project clean proves disposable
- **WHEN** one repository holds a merged, clean, published linked worktree whose only ignored files are Python bytecode caches that `project clean` would dispose of, a second such worktree that also holds an ignored `local.env`, and a third cache-only, merged, clean, published worktree holding an initialized submodule, and the overview and `project clean <root> --json` run from the same directory at the same commit
- **THEN** the overview classifies the first `ignored-local-files`, with the preserve finding and the read-only clean suggestion of that class, where `project clean` classifies it `merged-removable`, and a counting `git` wrapper on PATH records no cache enumeration child from the overview
- **AND** the overview classifies the third `ignored-local-files`, where `project clean` classifies it `merged-removable` and excludes it as `contains-submodule`
- **AND** both classify the second `ignored-local-files`, and no worktree is classified `merged-removable` by the overview where `project clean` classifies it otherwise for the same working directory and refs
