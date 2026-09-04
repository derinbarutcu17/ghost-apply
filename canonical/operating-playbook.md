# Operating playbook

Status: canonical operational policy
Version: 0.1

## Operating contract

Ghost Apply is evidence-first and fail-closed. A visible action is not proof of
a committed value, uploaded file, or successful submission. Reacquire current
state after navigation, rerender, picker close, upload, or validation error.

The application state machine is:

```text
draft → researched → tailored → PDF-QA-passed → form-reviewed
      → submitted-pending-confirmation → confirmed
```

Use `blocked` for a precise external stop, such as a CAPTCHA, MFA, missing
legal fact, unsupported portal, or login gate. Preserve the receipt and page
state. Never guess through a blocker.

## Evidence rules

- Candidate facts come from the user's private pack or an explicit user
  instruction. Every material claim needs provenance and approved wording.
- Role requirements come from a live listing or a recorded role brief. Recheck
  volatile status, URLs, deadlines, eligibility, and salary before live work.
- Unknown is a valid value. Never infer work authorization, sponsorship,
  relocation, start date, salary history, or qualifications.
- Generated artifacts must be derived from the claim ledger and must not modify
  protected input files.
- A receipt records source URLs, hashes, final form values, selected states,
  recovery events, and visible confirmation evidence. It never stores secrets.

## Computer-use rules

- Use a fresh application tab per role and keep unrelated Gmail work separate.
- Use visible mouse clicks and ordinary typing only.
- Open dropdowns and select from the rendered options; do not type into a
  dropdown as a shortcut.
- Verify checkbox state in the current rendered/accessibility state.
- Use the visible native file picker for uploads. Filename alone is not proof;
  verify the exact filename on the form and compare its hash with the manifest.
- Never use hidden DOM setters, API uploads, keyboard-based picker shortcuts,
  CAPTCHA bypasses, or credential automation.
- A Submit click creates `submitted-pending-confirmation`, never `confirmed`.
  Require visible success text and/or a confirmation URL for confirmation.

## Data separation

Operational rules live in Markdown under `canonical/`. Candidate packs, role
briefs, claim ledgers, form ledgers, manifests, and receipts are structured
JSON. Real user packs and runs stay outside a public repository. Fake fixtures
must be clearly labelled and cannot be uploaded to real applications.
