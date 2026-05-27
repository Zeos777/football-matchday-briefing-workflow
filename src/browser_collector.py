"""Browser collection helpers for the matchday briefing workflow.

This module handles one page visit at a time with Playwright's sync API.
"""

from __future__ import annotations

from pathlib import Path

from src.utils import ensure_dir, safe_filename, truncate_text

BLOCKED_MARKERS = [
    "access denied",
    "permission denied",
    "forbidden",
    "403",
    "blocked",
    "request blocked",
    "captcha",
    "verify you are human",
    "enable javascript and cookies",
    "site owner may have set restrictions",
]


def _looks_blocked(page_title: str, body_text: str) -> bool:
    """Return True when the page content looks like an access restriction page."""
    combined_text = f"{page_title}\n{body_text}".lower()
    return any(marker in combined_text for marker in BLOCKED_MARKERS)


def collect_page(url: str, team: str, source_type: str, screenshot_dir: str | Path) -> dict:
    """Visit one public page, collect a small text excerpt, and save a screenshot."""
    screenshot_directory = ensure_dir(screenshot_dir)
    filename_base = safe_filename(f"{team}-{source_type}")
    screenshot_path = screenshot_directory / f"{filename_base}.png"

    result = {
        "team": team,
        "source_type": source_type,
        "url": url,
        "page_title": "",
        "text_excerpt": "",
        "screenshot_path": str(screenshot_path),
        "status": "failed",
        "error": "",
    }

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page_title = page.title()
                body_text = page.locator("body").inner_text(timeout=10000)
                text_excerpt = truncate_text(body_text, max_length=1200)
                page.screenshot(path=str(screenshot_path), full_page=True)
                status = "success"
                error = ""

                if _looks_blocked(page_title, body_text):
                    status = "blocked"
                    error = "Page appears to be blocked or access-restricted."

                result.update(
                    {
                        "page_title": page_title,
                        "text_excerpt": text_excerpt,
                        "status": status,
                        "error": error,
                    }
                )
            finally:
                browser.close()
    except Exception as exc:
        result["error"] = str(exc)

    return result
