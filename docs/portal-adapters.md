# Portal adapters

Implement a portal adapter behind the driver-neutral protocol in
`src/ghost_apply/portals/base.py`:

```text
identify → inspect → fill → upload → review → submit → confirm
```

Each adapter needs a fake local fixture, contract tests for dropdowns,
checkboxes, uploads, login gates, CAPTCHA, and timeout recovery. Browser
credentials, MFA, and cookies remain outside the project.
