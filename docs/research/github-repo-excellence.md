# GitHub Repository Excellence: Agent Skill Research

Research date: 2026-09-04

This note defines the skill architecture and quality gates an AI agent should
use when creating or upgrading a public GitHub repository. It is guidance for
the reusable project, not candidate-specific application data.

## Finding

The highest-leverage design is one router skill with small, branch-specific
references:

```text
github-repo-excellence
├── discovery and scope
├── repository bootstrap
├── engineering quality
├── security and supply chain
├── documentation and contributor experience
├── release and provenance
└── independent audit
```

Do not turn these into one permanently loaded monolith. The agent should load
only the branch required by the requested change, while the router keeps the
order, stopping conditions, and definition of done.

## Recommended skills

### 1. Repository discovery and source-of-truth audit

Before editing, inventory the tree, package metadata, commands, workflows,
tests, docs, licenses, generated files, secrets-risk paths, and current Git
state. Identify the authoritative source for each rule. Report unknowns rather
than silently inventing them.

Completion: the agent can name the project entry point, test command, build
command, supported runtimes, release path, and every file it will change.

### 2. Public repository bootstrap

Create or audit the visitor-facing contract: a concise README, install and
quickstart path, usage example, support route, contribution rules, code of
conduct, security policy, license, issue/PR templates, and a clear statement of
what is implemented versus planned. GitHub describes the README as the place
to explain what the project does, why it is useful, how to get started, where
to get help, and who maintains it. [GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

Completion: a new user can understand the project and run the smallest useful
example from the README without private context.

### 3. Engineering quality and reproducibility

For the detected language, add deterministic formatting/linting, type checks
where justified, unit and contract tests at public seams, a supported-runtime
matrix, package build verification, and a single documented local command.
Keep tests independent of implementation details. For Python projects,
validate `pyproject.toml`, editable installation, wheel/sdist builds, import
behavior, CLI behavior, and the supported Python versions.

Completion: the same clean checkout passes the documented checks locally and
in CI, and the package produced by CI is installable and smoke-tested.

### 4. Secure CI and dependency supply chain

Every workflow should use least-privilege `permissions`, avoid exposing
credentials to untrusted pull requests, and pin third-party actions to full
commit SHAs. GitHub explicitly recommends read-only defaults and SHA pinning;
tags can move after review. [GitHub secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)

Add Dependabot configuration for runtime dependencies and GitHub Actions.
Enable CodeQL for supported languages and run OpenSSF Scorecard on public
repositories. Dependabot supplies alerts, security updates, and version-update
pull requests; CodeQL surfaces code-scanning alerts; Scorecard checks practices
such as dependency updates, security policy, license, CI tests, and SAST.
[
GitHub repository security quickstart
](https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository),
[Dependabot quickstart](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/dependabot-quickstart),
[OpenSSF Scorecard](https://scorecard.dev/)

Completion: the repository has a documented security contact, automated
dependency monitoring, a code-scanning path, and workflow permissions/actions
that pass a supply-chain review.

### 5. Contributor and maintainer workflow

Use `CONTRIBUTING.md`, issue forms, PR templates, and (when there is more than
one maintainer or ownership boundary) `.github/CODEOWNERS`. Protect `main`
with a ruleset requiring pull requests and the CI checks that matter. GitHub
rulesets can require reviews, status checks, code-scanning results, coverage,
and can block force pushes. [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets),
[GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

Completion: a contribution has one discoverable path from issue to reviewed,
validated merge, and no accidental direct mutation of the protected branch.

### 6. Release engineering and provenance

Separate “the repository is public” from “a release is published.” Use a
version source, release notes or changelog, tags, reproducible build checks,
and an explicit release workflow. For Python package distribution, prefer
PyPI Trusted Publishing through GitHub OIDC with a protected environment over
long-lived API tokens. [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/using-a-publisher/)

When distributing binaries or packages, add GitHub artifact attestations so
consumers can verify where and how the artifact was built. [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)

Completion: a maintainer can create a tagged, documented release from a clean
commit, and a consumer can verify the artifact's origin and integrity.

### 7. Public-safety and privacy audit

Scan the complete publish set—not only tracked files—for private filesystem
paths, email addresses, tokens, screenshots, PDFs, CVs, browser logs, local
environment files, and generated artifacts. Check links, examples, fixtures,
and documentation for accidental personal context. Treat archive and history
as evidence, not as active instructions or runtime inputs.

Completion: the exact files proposed for publication are enumerated, scanned,
and the scan is tested in both directions with a planted canary that must fail.

### 8. Independent final review

Run two separate reviews: standards/security and product/spec fidelity. Then
perform a clean-checkout test, a README quickstart test, a package install test,
and a negative-direction test for every detector or gate. A green test suite is
not enough if the test can also pass after the behavior is disabled.

Completion: the report states what passed, what was intentionally deferred,
and which command or evidence proves each claim.

## Current Ghost Apply audit

Already present:

- hub-and-branches canonical structure;
- schemas and fake examples separated from private candidate data;
- README, license, security policy, contributing guide, and code of conduct;
- CI for Python 3.11 and 3.12;
- package build and ten passing local tests;
- public-artifact scan in CI;
- release workflow that builds and uploads a distribution artifact;
- state-machine and receipt concepts that make application work auditable.

Recommended next upgrades:

1. Pin every third-party GitHub Action to a reviewed full commit SHA. The
   current workflows use version tags, which is functional but below the
   strongest supply-chain posture.
2. Add `.github/dependabot.yml` for Python and GitHub Actions.
3. Add CodeQL and OpenSSF Scorecard workflows, with their permissions scoped to
   the jobs that need them.
4. Add `.github/CODEOWNERS` once the GitHub owner identity is known, then enable
   a `main` ruleset requiring the CI jobs and review.
5. Add a small `CHANGELOG.md` or release-notes convention and make the release
   workflow's purpose explicit: artifact build now; package publication only
   after a maintainer configures the target registry and environment.
6. Add lint/type/coverage checks only where they improve signal; avoid adding
   tools that create noise without protecting a real seam.
7. Add a clean-install smoke test to CI and a README quickstart job or script.
8. Add artifact attestations if the project begins distributing release
   packages beyond source control.

These are maturity upgrades, not evidence that the current repository is
unsafe. The current release can be published as a public foundation if its
scope is described honestly.

## Suggested router behavior

The eventual `github-repo-excellence` skill should run this sequence:

1. Discover and freeze scope.
2. Build a public-safe file manifest.
3. Apply only the relevant branch skills.
4. Run local quality and security gates.
5. Break each detector intentionally and restore it.
6. Review the README from a clean checkout.
7. Report readiness separately for public repository, package release, and
   live-service integration.

The agent should stop only for missing authority, an unknown security-critical
fact, or a real external dependency such as an unset GitHub owner/repository.
It should not stop because an optional polish item is deferred; it should label
the deferral and continue.

## Sources

- [GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [GitHub community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- [GitHub secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub security quickstart](https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository)
- [GitHub CodeQL](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning)
- [GitHub Dependabot](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/dependabot-quickstart)
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/using-a-publisher/)
- [OpenSSF Scorecard](https://scorecard.dev/)
