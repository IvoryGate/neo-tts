"""Helpers for building `EditableSegment` in tests (schema uses stem + terminal, not raw_text)."""

from __future__ import annotations

from backend.app.schemas.edit_session import EditableSegment


def zh_sentence_segment(
    *,
    segment_id: str,
    order_key: int,
    sentence: str,
    document_id: str = "doc-1",
    text_language: str = "zh",
    **kwargs,
) -> EditableSegment:
    sentence = sentence.rstrip()
    stem = sentence
    terminal_raw = ""
    if text_language == "zh" and sentence and sentence[-1] in "。！？":
        stem, terminal_raw = sentence[:-1], sentence[-1]
    if not stem:
        stem = sentence or "placeholder"
    return EditableSegment(
        segment_id=segment_id,
        document_id=document_id,
        order_key=order_key,
        stem=stem,
        text_language=text_language,
        terminal_raw=terminal_raw,
        terminal_source="original" if terminal_raw else "synthetic",
        **kwargs,
    )
