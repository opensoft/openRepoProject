---
name: speckit-git-remote
description: Detect Git remote URL for GitHub integration
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: git:commands/speckit.git.remote.md
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

# Detect Git Remote URL

Detect the Git remote URL for integration with GitHub services (e.g., issue creation).

## Prerequisites

- Check if Git is available by running `git rev-parse --is-inside-work-tree 2>/dev/null`
- If Git is not available, output a warning and return empty:
  ```
  [specify] Warning: Git repository not detected; cannot determine remote URL
  ```

## Execution

Run the following command to get the remote URL:

```bash
git config --get remote.origin.url
```

## Output

Parse the remote URL and determine:

1. **Repository owner**: Extract from the URL (e.g., `github` from `https://github.com/github/spec-kit.git`)
2. **Repository name**: Extract from the URL (e.g., `spec-kit` from `https://github.com/github/spec-kit.git`)
3. **Is GitHub**: Whether the remote points to a GitHub repository

Supported URL formats:
- HTTPS: `https://github.com/<owner>/<repo>.git`
- SSH: `git@github.com:<owner>/<repo>.git`

> [!CAUTION]
> ONLY report a GitHub repository if the remote URL actually points to github.com.
> Do NOT assume the remote is GitHub if the URL format doesn't match.

## Graceful Degradation

If Git is not installed, the directory is not a Git repository, or no remote is configured:
- Return an empty result
- Do NOT error — other workflows should continue without Git remote information