"""Entry point for the football matchday briefing workflow."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from src.browser_collector import collect_page
from src.page_parser import parse_collected_page
from src.report_writer import write_csv, write_markdown_briefing
from src.utils import ensure_dir


def main() -> None:
    """Run the end-to-end workflow."""
    project_root = Path(__file__).resolve().parent
    input_csv = project_root / "data" / "match_urls.csv"
    screenshots_dir = ensure_dir(project_root / "screenshots")
    outputs_dir = ensure_dir(project_root / "outputs")
    csv_output_path = outputs_dir / "collected_pages.csv"
    markdown_output_path = outputs_dir / "matchday_briefing.md"

    if not input_csv.exists():
        print(f"Input file not found: {input_csv}")
        sys.exit(1)

    dataframe = pd.read_csv(input_csv)
    required_columns = {"team", "source_type", "url"}

    if not required_columns.issubset(dataframe.columns):
        missing = ", ".join(sorted(required_columns - set(dataframe.columns)))
        print(f"Missing required columns in {input_csv}: {missing}")
        sys.exit(1)

    results: list[dict] = []

    for row in dataframe.fillna("").to_dict(orient="records"):
        raw_result = collect_page(
            url=str(row["url"]).strip(),
            team=str(row["team"]).strip(),
            source_type=str(row["source_type"]).strip(),
            screenshot_dir=screenshots_dir,
        )
        parsed_result = parse_collected_page(raw_result)
        results.append(parsed_result)

    write_csv(results, csv_output_path)
    write_markdown_briefing(results, markdown_output_path)

    success_count = sum(1 for item in results if item.get("status") == "success")
    blocked_count = sum(1 for item in results if item.get("status") == "blocked")
    failed_count = sum(1 for item in results if item.get("status") == "failed")

    print("Workflow finished.")
    print(f"Total pages: {len(results)}")
    print(f"Success count: {success_count}")
    print(f"Blocked count: {blocked_count}")
    print(f"Failed count: {failed_count}")
    print(f"CSV output: {csv_output_path}")
    print(f"Markdown output: {markdown_output_path}")


if __name__ == "__main__":
    main()
