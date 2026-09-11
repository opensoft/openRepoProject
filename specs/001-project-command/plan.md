# Implementation plan

Use a single Python executable to make pinned distribution simple. Read JSON
registry/profile files and use PyYAML safe_load for shape/workspace manifests.
Separate discovery, reports, command planning and execution functions. Use only
argument arrays with inherited terminal streams for mutations; capture output
only for read-only probes. Snapshot each declared checkout independently.

Validate scripts are inside configured roots, and never infer missing generators.
Use deterministic keyword suggestions; ask for explicit selection on ambiguity.
Status reports local remote-tracking refs, never claims they are current remotely.
Doctor calls owner validators only with --validate; no home credential contents
are inspected. A configured container is inspected via docker inspect.

Publish the executable on the feature branch for integration testing. Pin the
exact commit and SHA-256 in workBenches; use a local source override for offline
tests. Installer refuses invalid targets and atomically replaces one executable.
WorkBenches wrappers resolve roots at runtime and preserve legacy arguments.

Verification: unittest fixtures with temporary Git repos/fake tools, py-bench
execution, help and real read-only status/doctor smoke tests, shell parsing.
