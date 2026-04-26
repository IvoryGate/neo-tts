# Known issues and baseline notes

## Resolved during baseline pass (for historians)

- **`EditableSegment` test fixtures** — Many unit tests still constructed segments with removed `raw_text` / `normalized_text` fields. Fixed via `backend/tests/segment_factory.py` and snapshot updates.
- **Integration assertions** — Prefer `segment.display_text` over `raw_text` on `EditableSegment` instances.
- **Export API** — `target_dir` must be an **absolute** path; integration tests were updated accordingly. Output WAV names follow `neo-tts-export-*.wav` (see `ExportService._build_export_name`), not legacy `composition.wav` / `0001.wav`.
- **Export path policy** — `ExportService` now rejects destinations outside `EditAssetStore.export_root` (security regression test restored).
- **`fast_langdetect` cache dir** — Tests mkdir `pretrained_models/fast_langdetect` under the repo in `backend/tests/conftest.py` so the library can download or use models.
- **Root `tests/test_onnx_sampling.py`** — Orphaned collector import; listed in root `conftest.py` `collect_ignore`.
- **`test_official_inference_migration`** — Skips when `legacy/root_entrypoints` is absent in the checkout.

## Active follow-ups (safe improvements)

1. **Pydantic field validators** — Add an explicit validator on `ExportRequestBase.target_dir` requiring `Path.is_absolute()` so bad requests fail at schema time with 422, matching the written schema description.
2. **Ruff isort (`I`)** — Enable after running a one-time `ruff check --select I --fix` across `backend/` to avoid a huge mixed PR.
3. **Frontend ESLint** — No ESLint config yet; consider aligning with Vue + TypeScript recommendations without blocking `npm run build`.
4. **E2E in CI** — `pytest -m e2e` remains opt-in (GPU + weights + `GPT_SOVITS_E2E=1`); add a scheduled or manual workflow if needed.
5. **`pyproject` project name** — Still `gpt-sovits-minimal-inference`; renaming is cosmetic but touches packaging and docs links.

## Code smells / architecture (non-blocking)

- **Large router modules** — `edit_session` router is dense; future work can split by resource without changing URLs.
- **Dual requirements** — Both `pyproject.toml` and `requirements.txt` exist; treat `uv` + `pyproject` as primary.
