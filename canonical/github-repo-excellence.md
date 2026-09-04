# GitHub repository excellence

Use this router when creating, publishing, or materially upgrading a public
GitHub repository. It coordinates small branches; it is not a replacement for
the application workflow in `agent-skill.md`.

## Run order

1. Discover the tree, source-of-truth files, commands, supported runtimes,
   generated files, Git state, and external destination.
2. Freeze a public file manifest. Real profiles, receipts, screenshots, PDFs,
   browser logs, credentials, and private paths stay outside the repository.
3. Apply only the relevant branches:
   - README, license, security, contributing, code of conduct, issue/PR forms;
   - tests, lint, typing, build, install smoke test, and supported-runtime CI;
   - least-privilege workflows, SHA-pinned Actions, Dependabot, CodeQL, and
     OpenSSF Scorecard;
   - CODEOWNERS and protected-branch rules when ownership is known;
   - versioning, changelog, release artifacts, and provenance.
4. Run the complete local quality suite and inspect its actual output.
5. Exercise every detector in both directions: clean input passes; a temporary
   canary that should be caught fails; remove the canary and rerun.
6. Test the README quickstart from a clean environment and smoke-test the
   built package.
7. Report readiness separately for public source publication, package release,
   and live-service integrations. Do not represent a foundation as a complete
   browser or production integration.

## Hard gates

- Every changed file has a reason and an owner.
- Every public claim is supported by repository evidence or a linked primary
  source.
- Workflow permissions are minimal and third-party Actions use immutable full
  commit SHAs.
- CI proves formatting/linting, typing where configured, tests, build, package
  install, and public-safety checks.
- `main` is protected by review and required status checks when the GitHub
  repository exists.
- Release artifacts have hashes and, when distributed, provenance or an
  attestation.
- No push, release, or external integration is reported as complete without
  visible or command-level evidence from the destination.

## Branch references

- `docs/research/github-repo-excellence.md` - rationale and current audit.
- `docs/privacy-and-safety.md` - public/private data boundary.
- `docs/architecture.md` - portable engine boundaries.
- `SECURITY.md` and `CONTRIBUTING.md` - maintainer-facing rules.

## Primary references

- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- https://docs.github.com/en/actions/reference/security/secure-use
- https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://docs.pypi.org/trusted-publishers/using-a-publisher/
- https://scorecard.dev/

Completion: the public file manifest, local gates, negative-direction checks,
README quickstart, and external publication evidence all exist, or every
missing item is explicitly labelled as deferred or blocked.
