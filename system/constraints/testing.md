# Testing constraints

- **No behavior change without tests** — Either update existing tests or add new ones in the same PR.
- **Bugs become tests** — Every defect fixed in application code should have a regression test unless truly non-reproducible (then document why in `docs/known_issues.md`).
- **Markers** — `e2e` tests require real models and `GPT_SOVITS_E2E=1`; default automation runs `-m "not e2e"`.
- **Critical flows to keep green** — Edit-session initialize → render job → snapshot; health; export with absolute paths under export root; voice listing.
