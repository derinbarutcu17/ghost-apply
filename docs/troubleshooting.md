# Troubleshooting

- **`FAIL_MACHINE`:** inspect the report and rendered page before regenerating.
  Common causes are missing PDF tools, wrong page size, empty text, or a changed
  artifact hash.
- **Upload mismatch:** stop, restage from the manifest, and verify the visible
  filename and SHA-256. Never retry blindly after a submit timeout.
- **Dropdown remains invalid:** reopen the rendered menu, select an option from
  the list, and verify the committed value after the rerender.
- **Portal redirects or asks for login:** preserve the receipt as `blocked` and
  record the exact external handoff; do not automate credentials.
