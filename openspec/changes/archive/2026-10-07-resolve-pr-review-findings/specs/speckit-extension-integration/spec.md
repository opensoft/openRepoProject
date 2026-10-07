## Purpose

Keep the locally registered Speckit Git extension commands usable from Claude
workflows and hooks.

## ADDED Requirements

### Requirement: Registered Claude Git commands have matching skill bundles

Every command listed in the Git extension registry's `claude` command list
SHALL have a committed Claude skill bundle. The bundle directory name SHALL
replace dots in the command name with hyphens and contain `SKILL.md`.

#### Scenario: A mandatory Git initialization hook is registered

- **WHEN** `speckit.git.initialize` is registered for Claude
- **THEN** `.claude/skills/speckit-git-initialize/SKILL.md` is available for
  the hook workflow

#### Scenario: Optional auto-commit is registered

- **WHEN** `speckit.git.commit` is registered for Claude
- **THEN** `.claude/skills/speckit-git-commit/SKILL.md` is available for the
  hook workflow
