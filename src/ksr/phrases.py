from __future__ import annotations

import re


def extract_candidate_phrases(text: str, max_phrases: int = 12) -> list[str]:
    """Extract short candidate phrases for concept alignment."""

    chunks = [
        chunk.strip()
        for chunk in re.split(r"[。.!?\n]+", text)
        if chunk.strip()
    ]
    candidates: list[str] = []
    for chunk in chunks:
        candidates.append(chunk)
        candidates.extend(_keyword_windows(chunk))

    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        compact = re.sub(r"\s+", " ", candidate).strip()
        if not compact or compact in seen:
            continue
        seen.add(compact)
        deduped.append(compact)
        if len(deduped) >= max_phrases:
            break
    return deduped


def _keyword_windows(chunk: str) -> list[str]:
    terms = [
        "関数",
        "def",
        "return",
        "戻り値",
        "引数",
        "繰り返し",
        "for",
        "while",
        "if文",
        "条件分岐",
        "条件",
        "主張",
        "根拠",
        "理由",
        "反論",
        "結論",
    ]
    windows: list[str] = []
    for term in terms:
        index = chunk.lower().find(term.lower())
        if index < 0:
            continue
        start = max(0, index - 18)
        end = min(len(chunk), index + len(term) + 18)
        windows.append(chunk[start:end])
    return windows
