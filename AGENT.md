# Neo TTS — agent operating guide

This file orients autonomous coding agents. **Do not treat it as a second README**; link to `docs/` and source instead of duplicating behavior.

## Mission

Safely understand, stabilize, and evolve the repo into a production-grade system **without breaking existing behavior**. Prefer minimal diffs, tests first for refactors, and documented constraints under `system/constraints/`.

## Phases (loop)

1. **Observe** — Read the modules and tests that define the behavior you will touch.
2. **Plan** — Smallest change; list risks and rollback.
3. **Act** — Implement locally; avoid drive-by refactors.
4. **Verify** — `uv run ruff check backend/app backend/tests tests`, `uv run pytest backend/tests tests -m "not e2e"`, `frontend`: `npm run build` + `npm test`, `desktop`: `npm run build` + `npm test` (from repo root, see `docs/tech_stack.md`).
5. **Reflect** — If something was ambiguous, add a test or a constraint note in `docs/known_issues.md` or `system/constraints/`.

## Entry points (where to start)

| Surface | Path | Notes |
|--------|------|--------|
| FastAPI app | `backend/app/main.py` | `create_app()`, SPA mount when not `development`. |
| HTTP API router aggregation | `backend/app/api/router.py` | Mounts health, system, voices, TTS, edit-session. |
| Backend CLI (uvicorn) | `backend/app/cli.py` | Default port `18600`; stdin watchdog for packaged runs. |
| Frontend SPA | `frontend/src/main.ts`, `frontend/vite.config.ts` | Dev server `5175`, proxies `/v1` and `/health`. |
| Desktop shell | `desktop/` | Electron; packaging scripts in `desktop/package.json`. |
| Vendored inference | `GPT_SoVITS/` | Packaged wheel includes this tree; do not “lint the world” here without intent. |

## Documentation map

- `docs/system_overview.md` — Product and runtime picture.
- `docs/architecture.md` — Layers and request/session flows.
- `docs/module_map.md` — Backend/frontend/desktop file map.
- `docs/tech_stack.md` — Tooling, runbooks, CI.
- `docs/known_issues.md` — Baseline gaps and follow-ups.

## Constraints

Rules for safe changes live in `system/constraints/`. Violating them requires explicit maintainer decision and test updates.

## Forbidden (short list)

- Large rewrites without tests.
- Renaming public HTTP paths or payload shapes without migration and tests.
- Removing code paths you have not traced.
