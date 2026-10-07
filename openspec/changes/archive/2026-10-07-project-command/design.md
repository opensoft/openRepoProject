## Context

See proposal.md. The existing registry contains both generators and updaters;
some configured scripts are absent. Generators accept NAME and PARENT and may
require their language runtime. They are not compatible with populated shape legs.

## Goals / Non-Goals

Goals: deliver all four commands, scriptable plans, actionable diagnostics and
workBenches distribution. Non-goals: own Git transport, silently install tools,
or generate an application directly in pinned spec/code legs.

## Decisions

Use Python 3.10+ with PyYAML for safe manifest parsing, argument arrays for
subprocesses, and a standalone executable for distribution. YAML is a real parser,
not a second partial manifest grammar. The launcher reports the dependency if absent.
Resolve configured paths relative to workBenches; accept only contained scripts.
Keep providers as subprocess delegates and preserve exit codes/output.
Creation supports bench mode and explicit shape mode. Shape mode delegates to
openRepoShape with its prompts intact; bench mode calls a chosen generator.
Use deterministic registry keywords for recommendations, with explicit selection
for ambiguity; retire the embedded obsolete AI API call and avoid uploading descriptions.
Doctor/status inspect local state only, with optional read-only validator calls.
Update reports local Git tracking state and offers explicit component delegation;
no default pull/install. Status never calls bootstrap or fetch.
Read a portable .project.json profile for bench/container selection.
WorkBenches installs a SHA-256 verified executable from a commit-pinned raw file,
using the authenticated GitHub API before raw download; explicit local source
is supported for development. Install atomically and refuse symlink targets.

## Risks / Trade-offs

Generator side effects remain bench-owned; show the exact command before execution.
Remote freshness is unknown without a fetch; label tracking comparisons local.
Environment health cannot prove credential validity; only report CLI/config presence.
Shape validation is delegated because pin invariants must have one implementation.

## Migration Plan

Publish CLI artifact first, then pin it in workBenches. Replace generic creation
with forwarding wrappers; keep legacy positional arguments. Reverting the
workBenches integration restores the old entrypoints. Never move bench generators.
