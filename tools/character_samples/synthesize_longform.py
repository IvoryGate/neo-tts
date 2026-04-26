"""Synthesize long-form WAV using a character folder reference + shared weights (default neuro2)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from generate_from_podcast_characters import (  # noqa: E402
    find_reference_audio,
    normalize_reference_text,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--character-dir",
        type=Path,
        default=Path(r"H:\AI-Podcast-Generator\data\charactor\candidate_9"),
    )
    parser.add_argument(
        "--text-file",
        type=Path,
        default=Path(__file__).resolve().parent / "longform_sample.txt",
        help="UTF-8 file with synthesis text (can be very long).",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output .wav path.")
    parser.add_argument("--backend", default="http://127.0.0.1:18600")
    parser.add_argument("--voice", default="neuro2")
    parser.add_argument("--text-lang", default="en")
    parser.add_argument("--ref-lang", default="en")
    args = parser.parse_args()

    char_dir = args.character_dir.resolve()
    if not char_dir.is_dir():
        print(f"Not a directory: {char_dir}", file=sys.stderr)
        return 2
    ref_path = char_dir / "reference.txt"
    if not ref_path.is_file():
        print(f"Missing reference.txt in {char_dir}", file=sys.stderr)
        return 2
    audio_path = find_reference_audio(char_dir)
    if audio_path is None:
        print(f"No .wav/.flac in {char_dir}", file=sys.stderr)
        return 2

    synth_text = args.text_file.read_text(encoding="utf-8").strip()
    if not synth_text:
        print("Synthesis text is empty.", file=sys.stderr)
        return 2

    ref_text = normalize_reference_text(
        ref_path.read_text(encoding="utf-8").strip(),
        ref_lang=args.ref_lang,
    )

    url = args.backend.rstrip("/") + "/v1/audio/speech"
    payload = {
        "input": synth_text,
        "voice": args.voice,
        "text_lang": args.text_lang,
        "ref_lang": args.ref_lang,
        "ref_text": ref_text,
        "ref_audio": str(audio_path.resolve()),
        "response_format": "wav",
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = Request(
        url,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    out = args.output.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"POST {url} chars={len(synth_text)} -> {out}", flush=True)
    try:
        with urlopen(req, timeout=3600) as resp:
            if resp.status != 200:
                print(f"HTTP {resp.status}", file=sys.stderr)
                return 1
            out.write_bytes(resp.read())
    except HTTPError as e:
        print(e.read().decode("utf-8", errors="replace")[:2000], file=sys.stderr)
        return 1
    except URLError as e:
        print(e, file=sys.stderr)
        return 1
    print(f"Wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
