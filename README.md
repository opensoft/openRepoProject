# openRepoProject

The project-facing command for creating, understanding, and maintaining
projects built from the OpenSoft repository and workstation tools.

`openRepoProject` is intended to provide one discoverable front door for a
developer starting or operating a project. It coordinates existing tools; it
does not replace the systems that own repository shape, estate handoff, or
development environments.

## Why this exists

OpenSoft projects currently span several deliberately separate repositories:

- [`openRepoShape`](https://github.com/opensoft/openRepoShape) defines the
  repository shape, pins, validation, bootstrap, families, and worktrees.
- [`openRepoTools`](https://github.com/opensoft/openRepoTools) provides the
  workstation-wide `park` and `resume` commands for moving in-flight work
  between machines.
- [`workBenches`](https://github.com/opensoft/workBenches) provisions
  development benches, containers, AI tools, credentials, and workstation
  integrations.

Each repository has a focused responsibility, but a person starting a project
has to understand all three. This project supplies the orchestration and
reporting layer between them.

```text
                         project
                    /       |       \
                   /        |        \
          openRepoShape  openRepoTools  workBenches
             structure      handoff       environment
```

## Planned command surface

The command will be installed as `project` by `workBenches`.

```sh
project new       # guide creation of a project and its environment
project doctor    # diagnose repository, workstation, and bench readiness
project status    # show the project, legs, worktrees, bench, and handoff state
project update    # report and coordinate safe updates from the owning tools
```

The exact command behavior will be specified before implementation. Commands
should be useful without requiring the user to know which underlying
repository owns each operation.

## Design principles

### Delegate ownership

The command should call the authoritative tool for each operation:

| Concern | Owner |
| --- | --- |
| Project shape, scaffolding, adoption, pins, and validation | `openRepoShape` |
| Estate discovery, parking, resuming, and cross-machine handoff | `openRepoTools` |
| Docker, benches, dev containers, AI tools, and workstation setup | `workBenches` |
| Cross-system orchestration and human-readable reporting | `openRepoProject` |

`openRepoProject` must not create a second implementation of Git worktree
handling, pin validation, Docker setup, or technology-specific project
generation.

### Safe by default

Inspection commands should be read-only. Commands that create repositories,
change remotes, install software, alter credentials, or modify project state
must show their plan and require the appropriate explicit confirmation.

Refusals from an owning tool are meaningful results. The command should relay
them clearly instead of resetting, stashing, checking out, or otherwise
overriding work that the owning tool protected.

### Technology-specific logic stays with the technology

The generic project flow belongs here. A Python, Flutter, .NET, or other
technology-specific generator belongs in its corresponding development bench.
This repository may discover and invoke those generators, but should not absorb
their implementation.

### Workstation distribution is separate from authorship

`workBenches` will install the `project` executable because it is the
workstation's setup and distribution layer. That does not make `workBenches`
the source of truth for the command.

## Initial scope

The first implementation should establish a reliable, offline-friendly
discovery and diagnostics layer before attempting a large interactive
scaffolding flow. A likely sequence is:

1. discover the current project or estate;
2. report its repository shape and Git state;
3. detect available benches and development tooling;
4. identify missing or unsafe prerequisites;
5. delegate creation or repair only after presenting a clear plan.

The command should work from inside a project and, where possible, from the
projects directory or another directory on the workstation.

## Non-goals

This repository is not:

- a replacement for `openRepoShape`;
- a replacement for `park` or `resume`;
- a Docker image or development bench;
- a general-purpose package manager;
- a technology-specific application generator;
- a place to store credentials or personal workstation state.

## Project status

This repository is being established as the home for the project-facing
command. The initial work is design and contract definition; implementation
will follow once the command boundaries and first workflow are agreed.

## License

Apache-2.0. See [LICENSE](LICENSE).

