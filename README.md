# Ghost Apply

Point your AI agent at this repository and give it a job listing. Ghost Apply
helps the agent research the role, ground every application claim in evidence,
create and check the documents, and leave behind a receipt of what it prepared.

You do not need to understand the code or JSON schemas to start. Keep your
personal CV, contact details, receipts, screenshots, and browser session data
on your computer; this public repository is the reusable engine and operating
guide, not a place to store them.

It does not collect credentials, bypass CAPTCHA, mutate hidden form fields,
upload through ATS APIs, or claim that a submission succeeded without visible
confirmation.

## Easiest way to use it with an AI agent

1. Give your agent this repository URL:
   `https://github.com/derinbarutcu17/ghost-apply`
2. Give it the job-listing URL and the path to your private candidate pack.
3. Paste this instruction:

   > Read this repository's `README.md`, then `canonical/README.md` and
   > `canonical/agent-skill.md`. Use Ghost Apply in `dry-run` mode for the
   > supplied job listing and private candidate pack. Research the role,
   > prepare grounded application documents, run every QA gate, and report the
   > exact files and receipt. Keep personal data outside the repository. Stop
   > before any live upload or submission unless I explicitly authorize that
   > visible browser action.

The agent should use the canonical documents as its instructions and the CLI
as its handoff contract. If you only want to explore the project, run the fake
example below; it uses no real identity or application data.

For each dry run, the useful result is a folder containing a validated role
brief, evidence-backed claims, generated documents, machine-readable QA
results, staged upload copies, and an auditable receipt. The agent can explain
each file in plain language when it finishes.

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
