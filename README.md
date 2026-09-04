# Ghost Apply

Ghost Apply is a toolkit that helps your AI agent handle job applications with
more care: understand a role, use only evidence-backed claims, prepare the
right documents, check them, and show you exactly what it prepared.

You do not need to be technical to use it. Give an AI agent this repository,
the job listing, and access to your private candidate materials. The agent
reads the instructions here and takes care of the workflow.

## Start here

1. Give your AI agent this repository:
   [github.com/derinbarutcu17/ghost-apply](https://github.com/derinbarutcu17/ghost-apply)
2. Give it the job-listing URL and the location of your private CV or candidate
   materials. Keep those private files on your own computer.
3. Tell it:

   > Read this repository's README, then follow `canonical/README.md` and
   > `canonical/agent-skill.md`. Prepare a dry-run application for the supplied
   > job listing and my private candidate materials. Research the role, use
   > evidence-backed wording, check every document, and explain the output in
   > plain language. Keep my private files outside the repository.

That is enough to get started. You can ask your agent to explain any step or
file without learning the underlying code.

## What you get

For each run, your agent can leave you with:

- a role brief describing what the employer is looking for;
- evidence-backed application claims;
- generated CV or cover-letter documents;
- quality-check results for the documents;
- staged copies ready for your review; and
- a receipt showing what was prepared and where each claim came from.

## What happens behind the scenes

The workflow is designed to be inspectable: research comes before tailoring,
tailoring comes before document QA, and staging comes before any possible live
action. The system is dry-run-first, so you can review the result before
anything is uploaded or submitted.

Ghost Apply does not collect passwords, bypass CAPTCHA or MFA, alter hidden
form fields, or claim that an application was submitted without visible proof.
Live browser work requires a separate browser-capable agent and your explicit
authorization.

## A note about your privacy

This is a public repository. Do not add your real CV, contact details,
application receipts, screenshots, browser logs, credentials, or private paths
to it. Store those materials in a private folder on your computer and give
your agent the path only when you run an application.

## For technical readers

The root README is intentionally customer-facing. For installation, the CLI,
the fake end-to-end run, architecture, schemas, CI, extension points, and
release process, see the [Technical README](docs/README.md).

The operational source of truth lives in the [canonical documentation](canonical/README.md).
