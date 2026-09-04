# Ghost Apply — Technical README

This page is for maintainers, agent builders, and users who want to understand
or extend the system. If you only want to use Ghost Apply with an AI agent,
start with the [customer-facing README](../README.md).

## What the engine provides

Ghost Apply is a local-first, vendor-neutral core for evidence-backed job
application preparation. It validates structured role and candidate data,
builds claim ledgers, renders deterministic documents, runs machine and visual
QA contracts, stages exact artifacts, and writes auditable receipts.

Browser and ATS adapters are intentionally separate. Login gates, CAPTCHA,
MFA, unsupported portals, and uncertain eligibility facts fail closed.

## Quickstart

Requires Python 3.11+, ReportLab, and `pdfinfo`, `pdftotext`, and `pdftoppm` for
the complete PDF gate.

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
python -m ghost_apply audit \
  --receipt /tmp/ghost-apply-run/receipt.json
```

The example identity, employer, URLs, and role are fake. Never replace example
files in a public clone with real personal data. `visual-review` prints
`PASS_FINAL` only when machine QA passed and every rendered page was explicitly
marked pass.

## Repository map

- `canonical/` — operational Markdown policy and agent instructions;
- `schemas/` — JSON contracts for roles, candidates, claims, forms, receipts,
  and package manifests;
- `src/ghost_apply/` — portable Python engine and CLI;
- `examples/` and `tests/fixtures/` — fake data only;
- `tests/` — unit, contract, PDF, staging, and public-safety tests;
- `scripts/` — repository checks, including the public-safety scanner;
- `.github/` — CI, security automation, Dependabot, issue forms, and ownership.

## Canonical operating order

Read [canonical/README.md](../canonical/README.md) first. It points agents to
the smallest relevant policy branch:

1. operating playbook;
2. agent contract;
3. cover-letter tailoring rules;
4. PDF artifact QA;
5. GitHub repository excellence.

Candidate facts, role briefs, and role-cache data stay structured JSON.
Operational rules stay in Markdown. Private packs, live runs, and application
evidence are ignored by default and must not enter a public clone.

## Development gates

The supported local gates are:

```bash
python -m compileall -q src scripts tests
python -m pytest -q
python -m ruff check .
python -m mypy
python -m build
python scripts/public_safety_scan.py --root .
```

The public workflow repeats these checks on Python 3.11 and 3.12, installs
Poppler for PDF inspection, smoke-tests a clean wheel install, and runs CodeQL,
dependency review, Scorecard, and release provenance checks.

## Extending the system

Keep the engine vendor-neutral. Add portal-specific behavior behind the adapter
interfaces in `src/ghost_apply/portals/` or `src/ghost_apply/adapters/`; do not
put credentials or ATS-specific assumptions into the core contracts. Add a
schema or canonical policy branch only when the behavior is durable and
evidence-backed.

For public-repository changes, follow
[canonical/github-repo-excellence.md](../canonical/github-repo-excellence.md).
For agent integration, see [agent-integration.md](agent-integration.md).
