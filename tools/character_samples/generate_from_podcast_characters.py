"""Batch-generate TTS preview WAVs: fixed voice weights, per-folder reference audio + reference.txt."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _uppercase_letter_ratio(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if c.isupper()) / len(letters)


def _sentence_case_first_char(text: str) -> str:
    for i, ch in enumerate(text):
        if ch.isalpha():
            return text[:i] + ch.upper() + text[i + 1 :].lower()
    return text.lower()


def _ensure_terminal_punctuation(text: str) -> str:
    if not text:
        return text
    if text[-1] in ".?!…":
        return text
    return text + "."


def normalize_reference_text(raw: str, *, ref_lang: str, uppercase_threshold: float = 0.72) -> str:
    """Make reference text TTS-friendly: ALL-CAPS LJ-style lines -> sentence case + closing punctuation.

    GPT-SoVITS-style G2P often treats heavy ALL CAPS as letter-by-letter spelling prompts.
    """
    text = " ".join(raw.split())
    if not text:
        return text
    lang = ref_lang.lower().split("-", 1)[0]
    if lang == "en":
        if _uppercase_letter_ratio(text) >= uppercase_threshold:
            text = text.lower()
            text = _sentence_case_first_char(text)
        text = _ensure_terminal_punctuation(text)
    return text


def find_reference_audio(directory: Path) -> Path | None:
    wavs = sorted(directory.glob("*.wav"))
    if wavs:
        return wavs[0]
    flacs = sorted(directory.glob("*.flac"))
    if flacs:
        return flacs[0]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(r"H:\AI-Podcast-Generator\data\charactor"),
        help="Parent directory; each child folder is one character.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("localdev/character-samples"),
        help="Output root; a run subfolder is created under this path.",
    )
    parser.add_argument("--run-id", default=None, help="Subfolder name; default: timestamp.")
    parser.add_argument("--backend", default="http://127.0.0.1:18600", help="FastAPI base URL.")
    parser.add_argument("--voice", default="neuro2", help="Voice id from voices.json (weights source).")
    parser.add_argument(
        "--text",
        default="Hello from Neo TTS. This clip demonstrates the reference voice for this character folder.",
        help="Text to synthesize for every character.",
    )
    parser.add_argument("--text-lang", default="en", help="Synthesis text language hint.")
    parser.add_argument("--ref-lang", default="en", help="Reference text language.")
    parser.add_argument(
        "--skip",
        nargs="*",
        default=["backups"],
        help="Child directory names to skip.",
    )
    parser.add_argument(
        "--no-normalize-ref",
        action="store_true",
        help="Send reference.txt verbatim (not recommended for ALL CAPS LJ dumps).",
    )
    parser.add_argument(
        "--uppercase-threshold",
        type=float,
        default=0.72,
        help="If this fraction of letters are uppercase (en), normalize to sentence case.",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    if not source.is_dir():
        print(f"Source not found or not a directory: {source}", file=sys.stderr)
        return 2

    run_id = args.run_id or time.strftime("%Y%m%d-%H%M%S")
    out_root = args.output.resolve() / run_id
    out_root.mkdir(parents=True, exist_ok=True)

    skip = set(args.skip)
    url = args.backend.rstrip("/") + "/v1/audio/speech"

    summaries: list[dict[str, str]] = []
    for child in sorted(source.iterdir()):
        if not child.is_dir():
            continue
        if child.name in skip:
            continue
        ref_txt_path = child / "reference.txt"
        if not ref_txt_path.is_file():
            print(f"skip {child.name}: no reference.txt", file=sys.stderr)
            continue
        audio_path = find_reference_audio(child)
        if audio_path is None:
            print(f"skip {child.name}: no .wav or .flac", file=sys.stderr)
            continue
        ref_text = ref_txt_path.read_text(encoding="utf-8").strip()
        if not ref_text:
            print(f"skip {child.name}: empty reference.txt", file=sys.stderr)
            continue
        if not args.no_normalize_ref:
            ref_text = normalize_reference_text(
                ref_text,
                ref_lang=args.ref_lang,
                uppercase_threshold=args.uppercase_threshold,
            )

        payload = {
            "input": args.text,
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
        out_wav = out_root / f"{child.name}.wav"
        try:
            with urlopen(req, timeout=600) as resp:
                if resp.status != 200:
                    print(f"fail {child.name}: HTTP {resp.status}", file=sys.stderr)
                    continue
                out_wav.write_bytes(resp.read())
        except HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:800]
            print(f"fail {child.name}: HTTP {e.code} {detail}", file=sys.stderr)
            continue
        except URLError as e:
            print(f"fail {child.name}: {e}", file=sys.stderr)
            continue

        summaries.append(
            {
                "character": child.name,
                "wav": str(out_wav),
                "ref_audio": str(audio_path.resolve()),
            }
        )
        print(f"ok {child.name} -> {out_wav}")

    manifest_path = out_root / "manifest.json"
    manifest_path.write_text(json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(summaries)} files under {out_root}")
    return 0 if summaries else 1


if __name__ == "__main__":
    raise SystemExit(main())
