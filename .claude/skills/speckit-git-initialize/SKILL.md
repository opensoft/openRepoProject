---
name: speckit-git-initialize
description: Initialize a Git repository with an initial commit
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: git:commands/speckit.git.initialize.md
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

# Initialize Git Repository

Initialize a Git repository in the current project directory if one does not already exist.

## Execution

Run the appropriate script from the project root:

- **Bash**: `.specify/extensions/git/scripts/bash/initialize-repo.sh`
- **PowerShell**: `.specify/extensions/git/scripts/powershell/initialize-repo.ps1`

If the extension scripts are not found, fall back to:
- **Bash**: `git init && git add . && git commit -m "Initial commit from Specify template"`
- **PowerShell**: `git init; git add .; git commit -m "Initial commit from Specify template"`

The script handles all checks internally:
- Skips if Git is not available
- Skips if already inside a Git repository
- Runs `git init`, `git add .`, and `git commit` with an initial commit message

## Customization

Replace the script to add project-specific Git initialization steps:
- Custom `.gitignore` templates
- Default branch naming (`git config init.defaultBranch`)
- Git LFS setup
- Git hooks installation
- Commit signing configuration
- Git Flow initialization

## Output

On success:
- `✓ Git repository initialized`

## Graceful Degradation

If Git is not installed:
- Warn the user
- Skip repository initialization
- The project continues to function without Git (specs can still be created under `specs/`)

If Git is installed but `git init`, `git add .`, or `git commit` fails:
- Surface the error to the user
- Stop this command rather than continuing with a partially initialized repository