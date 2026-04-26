# Character reference batch samples

Use this when you have **many folders** each with a **reference clip + `reference.txt`**, and you want **one synthesized WAV per folder** using the **same GPT/SoVITS weights** as a voice in `config/voices.json` (default: `neuro2`).

## Layout

- **Script**: `generate_from_podcast_characters.py` (stdlib only).
- **Outputs** (default): `localdev/character-samples/<run-id>/` — gitignored; safe for large WAVs and repeat runs.
- Each run writes `<folder_name>.wav` plus `manifest.json`.

## Requirements

1. Backend running: `uv run python -m backend.app.cli` (default `127.0.0.1:18600`).
2. Weights available for the chosen `--voice` (e.g. neuro2 + Hubert/BERT as in dev setup).
3. Reference paths must be readable by the backend process (use absolute paths; the script passes resolved paths).

## Example

```powershell
cd h:\neo-tts
uv run python tools/character_samples/generate_from_podcast_characters.py `
  --source "H:\AI-Podcast-Generator\data\charactor" `
  --voice neuro2 `
  --text "Hello from Neo TTS. This clip demonstrates the reference voice for this character folder."
```

Optional: `--run-id my-run-1`, `--backend http://127.0.0.1:18600`, `--skip backups trash`.

## Reference text normalization

For `ref_lang=en`, if most letters in `reference.txt` are uppercase (typical LJ Speech dumps), the script lowercases and applies **sentence case** (first letter only), then ensures a closing `.` if missing. This avoids GPT-SoVITS treating ALL CAPS as letter-by-letter spelling. Use `--no-normalize-ref` to send the file verbatim.

## Skipped directories

By default the directory name `backups` is skipped. Empty folders or folders without `reference.txt` or without `.wav`/`.flac` are skipped with a message on stderr.
