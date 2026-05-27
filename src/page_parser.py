"""Page parsing helpers for turning raw page data into structured records."""

from __future__ import annotations

KEYWORDS = [
    "match",
    "fixture",
    "preview",
    "lineup",
    "injury",
    "result",
    "goal",
    "league",
]


def parse_collected_page(raw_result: dict) -> dict:
    """Apply light cleanup and extract a small keyword summary."""
    text_excerpt = " ".join(str(raw_result.get("text_excerpt", "")).split())
    lowered_text = text_excerpt.lower()
    simple_keywords = [keyword for keyword in KEYWORDS if keyword in lowered_text]
    status = raw_result.get("status", "")
    error = " ".join(str(raw_result.get("error", "")).split())

    return {
        "team": raw_result.get("team", ""),
        "source_type": raw_result.get("source_type", ""),
        "url": raw_result.get("url", ""),
        "page_title": " ".join(str(raw_result.get("page_title", "")).split()),
        "text_excerpt": text_excerpt,
        "screenshot_path": raw_result.get("screenshot_path", ""),
        "status": status,
        "error": error,
        "simple_keywords": ", ".join(simple_keywords),
    }
