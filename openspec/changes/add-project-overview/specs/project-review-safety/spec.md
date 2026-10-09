## MODIFIED Requirements

### Requirement: YAML decoding errors are structured refusals

Every YAML input read by the command SHALL turn an invalid text encoding into a
normal refusal. JSON mode MUST preserve its structured error output and exit
code 2 rather than printing a traceback.

In `project overview` alone, such a refusal for a project or family manifest
SHALL instead be a `manifest-invalid` error on its candidate's row, in human
and JSON mode alike, never a traceback: the other rows SHALL still be
collected and printed, and the run SHALL exit with status 1 rather than 2.

#### Scenario: Manifest is not valid UTF-8 text

- **WHEN** a project or family manifest contains invalid UTF-8 bytes
- **THEN** status refuses with structured JSON error output and no traceback

#### Scenario: Overview keeps a manifest with invalid text in its row

- **WHEN** `project overview --json` runs over a root holding `alpha`, `ledger` and `zeta`, where `ledger/project.yaml` contains invalid UTF-8 bytes
- **THEN** `ledger`'s row has status `error` and one `manifest-invalid` error naming that manifest, with no traceback
- **AND** `alpha` and `zeta` are complete, the JSON document is printed, and the exit status is 1, not 2
