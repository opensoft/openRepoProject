# Consistency and verification

The OpenSpec contract maps to the Speckit scenarios and implemented command
surface. Creation and update subprocess failures preserve their exit status;
inspection and dry-run paths avoid writes. Source identity is the executable
SHA-256, while the workBenches pin also records its Git commit.

Verified in py-bench: 19 CLI behavioral tests; seven workBenches tests, including
installing this executable and creating a disposable project through legacy onp.
Source and integration OpenSpec changes pass strict validation. Live registry
inspection correctly reports missing generators and excludes updater entries.

Explicit limits: shape-plus-application generation needs a future bench adapter;
no remote freshness is inferred from local tracking refs; credential presence
does not prove authentication. Owner validators run only with doctor --validate.
No real GitHub projects were created for tests.
