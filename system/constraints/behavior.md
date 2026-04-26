# Behavior and refactors

- Do **not** change inference output or timeline math without explicit benchmarks or golden tests.
- **Refactor protocol** — Add or extend tests first when behavior is complex; refactor second; keep diffs small.
- **Unstable areas** — Prefer adapters or wrappers over editing `GPT_SoVITS/` unless upstream alignment is the goal.
- **Documentation** — Behavior notes belong beside code or in `docs/`; avoid long comment threads in source.
