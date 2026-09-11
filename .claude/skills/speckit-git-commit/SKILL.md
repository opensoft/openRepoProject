---
name: speckit-git-commit
description: Auto-commit changes after a Spec Kit command completes
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: git:commands/speckit.git.commit.md
---

<!-- OPENSPEC-SPECKIT-SHAPE:START -->
## Repository Shape (managed by setup-openspeckit)

Resolve the project shape once before any step below.

1. The project root is the nearest directory at or above the current one that contains `.specify/`. Run every `.specify/scripts/...` command from that root.
2. If the root has `project.yaml` with `kind: project-manifest` and `legs:` entries for `role: spec` and `role: code`, this is an openRepoShape **three-leg** project. `<spec>` and `<code>` are those legs' `path:` values (defaults `spec` and `code`). Otherwise it is a **single repository** and `<spec>` and `<code>` are both the root.
3. Three-leg placement: `openspec/` and `specs/NNN-*` live in the spec leg; source and tests live in the code leg; a feature's worktrees live at `worktrees/<NNN-feature>/<spec>/` and `worktrees/<NNN-feature>/<code>/` under the root. Never write feature work into `<spec>/` or `<code>/` at the root; they sit at the pinned commit.
4. Feature paths come from `.specify/scripts/bash/check-prerequisites.sh --json` (or `SPECIFY_FEATURE_DIRECTORY` / `.specify/feature.json`). In three-leg, `FEATURE_DIR` is inside the feature's spec worktree and the code worktree is the sibling `<code>/` directory beside it; implementation edits go there.
5. Run the `openspec` CLI with the current directory at the owner of `openspec/`: the root in a single repository, `<spec>/` in a three-leg project.

Full rules: `/home/brett/projects/new-workstation/home/.agents/protocols/openspec-speckit-workflow.md` ("Repository Shape", "Worktree Rules").
<!-- OPENSPEC-SPECKIT-SHAPE:END -->

# Auto-Commit Changes

Automatically stage and commit all changes after a Spec Kit command completes.

## Behavior

This command is invoked as a hook after (or before) core commands. It:

1. Determines the event name from the hook context (e.g., if invoked as an `after_specify` hook, the event is `after_specify`; if `before_plan`, the event is `before_plan`)
2. Checks `.specify/extensions/git/git-config.yml` for the `auto_commit` section
3. Looks up the specific event key to see if auto-commit is enabled
4. Falls back to `auto_commit.default` if no event-specific key exists
5. Uses the per-command `message` if configured, otherwise a default message
6. If enabled and there are uncommitted changes, runs `git add .` + `git commit`

## Execution

Determine the event name from the hook that triggered this command, then run the script:

- **Bash**: `.specify/extensions/git/scripts/bash/auto-commit.sh <event_name>`
- **PowerShell**: `.specify/extensions/git/scripts/powershell/auto-commit.ps1 <event_name>`

Replace `<event_name>` with the actual hook event (e.g., `after_specify`, `before_plan`, `after_implement`).

## Configuration

In `.specify/extensions/git/git-config.yml`:

```yaml
auto_commit:
  default: false          # Global toggle — set true to enable for all commands
  after_specify:
    enabled: true          # Override per-command
    message: "[Spec Kit] Add specification"
  after_plan:
    enabled: false
    message: "[Spec Kit] Add implementation plan"
```

## Graceful Degradation

- If Git is not available or the current directory is not a repository: skips with a warning
- If no config file exists: skips (disabled by default)
- If no changes to commit: skips with a message