# System overview

## What Neo TTS is

Neo TTS is a **segment-level editable speech workstation** built on **GPT-SoVITS v2 / v2Pro** inference. Long documents are split into **segments** linked by **edges** (pauses, boundary fusion). Users edit text and parameters per segment; the backend **re-renders a minimal set** of affected segments and boundaries, then composes a timeline for playback and export.

See the product narrative in the root `README.md` (not duplicated here).

## Runtime shapes

- **Development**: FastAPI serves JSON under `/v1/*` and `/health`; Vite dev server serves the UI (proxies API to `127.0.0.1:18600`).
- **Packaged**: Backend may serve `frontend-dist` as an SPA; Electron (`desktop/`) can own the process tree. Distribution flags and paths are driven by `AppSettings` in `backend/app/core/settings.py`.

## Core user journeys

1. **Edit session** — Initialize from raw text → standardized segments → async render jobs → timeline / playback map → optional exports (per-segment WAV, composed WAV, subtitles).
2. **Classic TTS API** — Speech generation under `/v1/audio/*` (see `backend/app/api/routers/tts.py`).
3. **Voices** — Voice catalog from JSON config + managed storage (`backend/app/api/routers/voices.py`, `backend/app/repositories/voice_repository.py`).

## What this repo is not

- No model training UI (inference and editing only).
- Not a generic GPT-SoVITS fork documentation set; archived planning notes live under `docs/archive/`.
