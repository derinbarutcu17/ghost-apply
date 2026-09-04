# Canonical operating branches

This directory is the only live source of operational policy in Ghost Apply.
Read this index, then load only the branch required by the task.

## Four layout rules

1. Keep the hub-and-branches structure: the root README is the orientation hub;
   these Markdown files are the operational branches.
2. Do not create another top-level master policy file.
3. Keep candidate facts, role briefs, and role cache in structured JSON; keep
   operational rules in Markdown.
4. Treat `archive/`, fixtures, and historical runs as evidence only. Never use
   them as default policy or real candidate source material.

## Load order

1. `operating-playbook.md` — state machine, safety boundary, and evidence rules.
2. `agent-skill.md` — executable zero-context contract for an AI agent.
3. `cover-letter-tailoring.md` — grounded narrative constraints.
4. `pdf-artifact-qa.md` — document quality gate.
5. `github-repo-excellence.md` — public-repository, CI, security, and release
   gate for this project itself.

Schemas and examples are adjacent but are data contracts, not instructions.
Browser and ATS implementations belong behind the `portals/` adapter interface.
