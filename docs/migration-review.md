# Review of workBenches new-project

Source reviewed: workBenches/scripts/new-project.sh and scripts/onp, plus
config/bench-config.json and the installed bench generators.

The old coordinator treated bench paths as relative to scripts/, despite the
registry defining them relative to the workBenches root. Its creation list
included update-flutter and update-dartwing because the registry puts both
operations in project_scripts. Some declared generators were not present on disk.
The onp wrapper also contained a user-specific checkout path.

Interactive helpers mixed prompts and return values on stdout, which callers
captured with command substitution. The embedded AI request constructed JSON
by interpolating descriptions and used a fixed provider/model. The replacement
uses local keyword recommendations, explicit selection, and proper JSON parsing.
Descriptions are never sent to a service. This intentionally retires embedded
AI routing; a future provider integration should use the shared bench tooling.

The old workflow initializer fetched specify through uvx after generators that
did not advertise includes_speckit. The replacement offers --workflow to invoke
the authoritative setup-openspeckit command and propagates its failure.

The migration moves generic coordination into openRepoProject. workBenches keeps
only the installer and compatibility entrypoints. Technology-specific scripts
stay in their owning bench repositories, invoked with NAME and PARENT.

Existing update-project.sh performs a fuzzy recursive folder search, so the new
bench update adapter selects update-TYPE from the declared bench's registry and
passes the exact project root. It refuses when no such adapter exists.

Shape scaffolding is a separate creation mode because existing generators
expect an empty new destination. They cannot populate pinned shape legs safely.
