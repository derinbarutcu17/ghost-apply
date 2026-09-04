# Contributing

1. Keep candidate facts and role briefs in JSON schemas; keep operational rules
   in `canonical/` Markdown.
2. Never commit real names, contact details, application receipts, screenshots,
   browser logs, or generated PDFs from a real candidate.
3. New portal behavior needs a sanitized fixture and a contract test.
4. Changes to state transitions, upload behavior, or receipt semantics need a
   regression test and documentation.
5. Run `python -m pytest` and `python -m compileall src` before opening a PR.

Pull requests should explain the evidence boundary, failure behavior, and any
new dependency. Keep the core driver-neutral; adapters must not weaken the
visible-action or confirmation rules.
