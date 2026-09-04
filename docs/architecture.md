# Architecture

Ghost Apply has five boundaries:

1. **Research** turns a live listing into a role brief JSON document.
2. **Tailoring** turns verified candidate facts into a claim ledger.
3. **Documents** renders role-specific artifacts and a package manifest.
4. **QA and receipts** prove artifact integrity and state transitions.
5. **Adapters** connect an AI agent or visible browser without changing the
   evidence rules.

The core is deliberately local-first and does not require a hosted database.
The private profile path is explicit, and no personal path is hard-coded.
