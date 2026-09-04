# Agent integration

Any tool-using agent can drive Ghost Apply through the CLI and JSON contracts.
The agent is responsible for reading the role page and producing a role brief;
the package handles deterministic documents, QA, staging, and receipts.

```text
role URL + private candidate JSON
  → role-brief.json
  → claim-ledger.json
  → generate → application-package-manifest.json
  → qa → PASS_MACHINE + visual review
  → stage → staging-manifest.json
  → visible adapter (optional)
  → receipt.json
```

Adapters should be thin. They may translate a tool call into a visible action,
but they may not use hidden form setters, credentials, API uploads, or false
confirmation. Unsupported portals should return a precise blocker.
