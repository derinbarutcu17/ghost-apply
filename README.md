# Ghost Apply

Evidence-first job-application automation for the AI agent you already use.

Ghost Apply turns a structured role brief and a private candidate pack into a
grounded application package, machine-checked PDFs, exact upload hashes, and an
auditable receipt. It is local-first, dry-run-first, and driver-neutral.

It does not collect credentials, bypass CAPTCHA, mutate hidden form fields,
upload through ATS APIs, or claim that a submission succeeded without visible
confirmation.

## Ten-minute fake run

Requires Python 3.11+, ReportLab, and the system tools `pdfinfo`, `pdftotext`,
and `pdftoppm` for the complete PDF gate.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'

python -m ghost_apply init --dest /tmp/ghost-apply-profile
python -m ghost_apply inspect-role --role-file examples/role-brief.example.json
python -m ghost_apply build-claims \
  --candidate examples/candidate-context.example.json \
  --role examples/role-brief.example.json \
  --out /tmp/ghost-apply-profile/claim-ledger.json
python -m ghost_apply generate \
  --candidate examples/candidate-context.example.json \
  --role examples/role-brief.example.json \
  --out /tmp/ghost-apply-run
python -m ghost_apply qa \
  --manifest /tmp/ghost-apply-run/application-package-manifest.json \
  --out /tmp/ghost-apply-run/qa
python -m ghost_apply visual-review \
  --report /tmp/ghost-apply-run/qa/report.json \
  --out /tmp/ghost-apply-run/qa/visual-review.json \
  --status pass
python -m ghost_apply stage \
  --manifest /tmp/ghost-apply-run/application-package-manifest.json \
  --out /tmp/ghost-apply-run/staged
python -m ghost_apply receipt \
  --role examples/role-brief.example.json \
  --manifest /tmp/ghost-apply-run/application-package-manifest.json \
  --out /tmp/ghost-apply-run/receipt.json
python -m ghost_apply audit --receipt /tmp/ghost-apply-run/receipt.json
```

The example identity, employer, URLs, and role are fake. Never replace the
example files in a public clone with real personal data.

`visual-review` prints `PASS_FINAL` only when machine QA passed and every
rendered page was explicitly marked pass. A machine pass with visual review
pending is incomplete.

## Project shape

- `canonical/` contains the live operational Markdown branches.
- `schemas/` defines the JSON contracts for candidates, roles, claims, forms,
  receipts, and package manifests.
- `src/ghost_apply/` is the portable engine and CLI.
- `examples/` and `tests/fixtures/` are fake data only.
- `tests/` covers state guards, provenance, documents, QA, and staging.
- `docs/` explains architecture, agent integration, adapters, privacy, and
  recovery.

Candidate facts and role/cache data are JSON. Operational rules stay in
Markdown. Live user packs and application runs are ignored by default.

## How agents use it

An agent produces a role brief from a live listing, passes the brief and an
explicit private candidate-pack path to the CLI, then uses the resulting
manifest and receipt as its handoff contract. The agent can choose:

- `dry-run`: generate, QA, and stage only;
- `review`: prepare everything and stop for visible user review;
- `live-submit`: use a supported visible browser adapter with explicit user
  authorization and confirmation evidence.

The current release implements the data, document, QA, staging, and receipt
contracts. Browser adapters are intentionally separate so unsupported portals,
login gates, CAPTCHA, MFA, and legal unknowns fail closed.

## Development

```bash
python -m compileall -q src scripts tests
python -m pytest -q
python -m ruff check .
python -m mypy
python -m build
python scripts/public_safety_scan.py --root .
```

See [canonical/README.md](canonical/README.md) for the operational load order,
[docs/agent-integration.md](docs/agent-integration.md) for the agent contract,
and [SECURITY.md](SECURITY.md) for the safety boundary. The repository's
workflow files repeat these gates on supported Python versions and add CodeQL,
dependency review, Scorecard, and release provenance checks.
