"""Small utility helpers shared across the workflow modules."""

from __future__ import annotations

import re
from pathlib import Path


def ensure_dir(path: str | Path) -> Path:
    """Create a directory if it does not exist and return its path."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def safe_filename(text: str, max_length: int = 80) -> str:
    """Convert text into a filesystem-friendly filename."""
    cleaned = text.strip().lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", cleaned)
    cleaned = cleaned.strip("-")

    if not cleaned:
        cleaned = "page"

    return cleaned[:max_length].rstrip("-")


def truncate_text(text: str, max_length: int = 1200) -> str:
    """Trim text to a readable length without adding extra complexity."""
    normalized = " ".join(text.split())

    if len(normalized) <= max_length:
        return normalized

    return normalized[:max_length].rstrip() + "..."
