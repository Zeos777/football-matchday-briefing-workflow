"""Report writing helpers for CSV and Markdown outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_csv(results: list[dict], output_path: str | Path) -> None:
    """Write all structured results to a CSV file."""
    dataframe = pd.DataFrame(results)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False)


def write_markdown_briefing(results: list[dict], output_path: str | Path) -> None:
    """Write a simple Markdown briefing grouped by team."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    grouped_results: dict[str, list[dict]] = {}
    for result in results:
        team = result.get("team", "") or "Unknown Team"
        grouped_results.setdefault(team, []).append(result)

    lines = ["# Matchday Briefing", ""]

    for team in sorted(grouped_results):
        lines.append(f"## {team}")
        lines.append("")

        for item in grouped_results[team]:
            source_type = item.get("source_type", "")
            page_title = item.get("page_title", "") or "(no title)"
            url = item.get("url", "")
            status = item.get("status", "")
            keywords = item.get("simple_keywords", "")
            screenshot_path = item.get("screenshot_path", "")

            lines.append(f"### {source_type}: {page_title}")
            lines.append(f"- URL: {url}")
            lines.append(f"- Status: {status}")

            if status == "success":
                if keywords:
                    lines.append(f"- Keywords: {keywords}")
                if screenshot_path:
                    lines.append(f"- Screenshot: {screenshot_path}")
                excerpt = item.get("text_excerpt", "")
                if excerpt:
                    lines.append("")
                    lines.append(excerpt)
            elif status == "blocked":
                error = item.get("error", "") or "Page appears to be blocked or access-restricted."
                lines.append(f"- Blocked reason: {error}")
                if screenshot_path:
                    lines.append(f"- Screenshot: {screenshot_path}")
            else:
                error = item.get("error", "") or "Unknown error"
                lines.append(f"- Error: {error}")
                if screenshot_path:
                    lines.append(f"- Screenshot: {screenshot_path}")

            lines.append("")

    output_file.write_text("\n".join(lines), encoding="utf-8")
