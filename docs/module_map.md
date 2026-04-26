# Module map

Abbreviated map — open files for detail; this is navigation, not a spec.

## Backend (`backend/app/`)

| Area | Path | Role |
|------|------|------|
| API entry | `main.py` | FastAPI factory, SPA static mount. |
| Routes | `api/router.py`, `api/routers/*.py` | HTTP surface. |
| Settings | `core/settings.py`, `core/lifespan.py` | Config, startup hooks, `app.state` wiring. |
| Edit session | `services/edit_session_*.py`, `repositories/edit_session_repository.py` | Session lifecycle, persistence. |
| Rendering | `services/render_job_service.py`, `services/render_planner.py`, `services/block_planner.py` | Job orchestration and planning. |
| Export | `services/export_service.py`, `services/edit_asset_store.py` | WAV/SRT export, path policy. |
| Inference | `inference/engine.py`, `inference/pipeline.py`, `inference/pytorch_optimized.py` | Model I/O and GPT-SoVITS integration. |
| Text | `text/segment_standardizer.py`, `text/language_profiles.py` | Normalization and language detection. |

## Frontend (`frontend/src/`)

| Area | Role |
|------|------|
| `main.ts`, `App.vue`, `router/` | Shell and routing. |
| `components/workspace/` | Editor workspace, export, segment UI. |
| `composables/` | API/session state (e.g. `useEditSession.ts`). |

## Desktop (`desktop/`)

TypeScript Electron main process, packaging scripts (`scripts/`), and Vitest tests under `desktop/tests/`.

## Vendored / upstream

| Path | Role |
|------|------|
| `GPT_SoVITS/` | Upstream-style tree included in the Hatch wheel (`pyproject.toml` `[tool.hatch.build.targets.wheel]`). |

## Tooling / i18n

| Path | Role |
|------|------|
| `tools/i18n/locale/*.json` | Locale JSON assets. |
| `launcher/` | Launcher build scripts (see `launcher/build.ps1`). |
