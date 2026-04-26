# Tech stack and tooling

## Versions (authoritative in repo)

- **Python** 3.11.x (`pyproject.toml` `requires-python`).
- **Node** 20+ recommended (Vitest 4 engines); CI uses Node 20.
- **Package manager**: `uv` for Python; `npm` for `frontend/` and `desktop/`.

## Main dependencies

- **Backend**: FastAPI, Pydantic v2, Uvicorn, PyTorch + torchaudio (CUDA index in `pyproject.toml`), GPT-SoVITS ecosystem packages (transformers, librosa, etc.).
- **Frontend**: Vue 3, Vite, TypeScript, Element Plus, Nuxt UI, Tailwind 4.
- **Desktop**: Electron, electron-builder.

## Commands (from repo root)

```powershell
uv sync --group dev
uv run ruff check backend/app backend/tests tests
uv run pytest backend/tests tests -m "not e2e"
```

Frontend:

```powershell
cd frontend
npm ci
npm test
npm run build
```

Desktop:

```powershell
cd desktop
npm ci
npm test
npm run build
```

## Lint / format

- **Ruff**: Configured in `pyproject.toml` (`[tool.ruff]`). Baseline rules: `E`, `F`, with `E501` ignored; import sorting (`I`) is a future tightening step.
- **Typecheck**: `vue-tsc` runs as part of `frontend` production build.

## CI

GitHub Actions workflow `.github/workflows/ci.yml` runs Ruff, pytest (non-e2e), and frontend/desktop `npm` pipelines on push/PR.

## Local dev (human)

Documented in `README.md`: `launcher-dev.exe --runtime-mode dev --frontend-mode web` with Vite on port **5175** and API on **18600**.
