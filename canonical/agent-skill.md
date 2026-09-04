# Agent skill: end-to-end application workflow

Use this skill when a user supplies a job listing and asks for research,
tailoring, documents, browser completion, or submission.

## Inputs and outputs

Inputs:

- a live role URL, inspected by the agent or a portal adapter;
- a private candidate-pack JSON path;
- an explicit mode: `dry-run`, `review`, or `live-submit`.

Outputs:

- a role brief JSON with sources and volatile-field timestamps;
- a claim and eligibility ledger;
- a package manifest for CV/letter PDFs;
- a machine QA report and explicit visual-review result;
- a redacted application receipt.

## Required sequence

1. Read the applicable canonical Markdown branches.
2. Inspect the listing and normalize its role, company, requirements, documents,
   form questions, URL, location, and unknowns into a role brief.
3. Load the private candidate pack and resolve claims only from evidence.
4. Build a claim ledger before writing. Mark unknown eligibility values as
   `unknown`; do not turn a guess into a legal answer.
5. Generate artifacts without overwriting the candidate pack or a master.
6. Run machine PDF QA, render every page, and record visual acceptance.
7. Stage exact artifacts and record their hashes.
8. In `review` or `live-submit`, inspect the visible form, fill one field at a
   time, and verify each committed value immediately.
9. Verify uploads on the form, review all required fields and checkbox states,
   then submit only in explicit `live-submit` mode.
10. Confirm with visible evidence or write a precise blocked receipt.

## Do not ask routine questions

Use the private pack, prior receipt, role brief, and current visible state before
asking the user to repeat anything. A genuinely critical missing fact, legal
attestation, password, MFA, OTP, CAPTCHA, or irreversible commitment is a
blocker. Do not work around it or fabricate an answer.

## Fail-closed conditions

Stop and preserve state for invented claims, stale role identity, changed
artifact hashes, missing required facts, broken PDFs, unsupported portals,
login gates, CAPTCHA/MFA, a timeout after submit, or missing confirmation text.
