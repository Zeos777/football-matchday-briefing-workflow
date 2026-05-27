"""Entry point for the football matchday briefing workflow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

from src.browser_collector import collect_page
from src.page_parser import parse_collected_page
from src.report_writer import write_csv, write_markdown_briefing
from src.utils import ensure_dir


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line interface for the workflow."""
    parser = argparse.ArgumentParser(
        description="Collect public football pages and build a local matchday briefing."
    )
    parser.add_argument(
        "--input",
        default="data/match_urls.csv",
        help="Path to the input CSV file. Default: data/match_urls.csv",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory for collected_pages.csv and matchday_briefing.md",
    )
    parser.add_argument(
        "--screenshot-dir",
        default="screenshots",
        help="Directory for page screenshots",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit for how many rows to process",
    )
    parser.add_argument(
        "--headful",
        action="store_true",
        help="Run Chromium in visible mode instead of headless mode",
    )
    return parser


def main() -> None:
    """Run the end-to-end workflow."""
    parser = build_parser()
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parent
    input_csv = (project_root / args.input).resolve()
    screenshots_dir = ensure_dir(project_root / args.screenshot_dir)
    outputs_dir = ensure_dir(project_root / args.output_dir)
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

    if args.limit is not None:
        dataframe = dataframe.head(args.limit)

    results: list[dict] = []

    for row in dataframe.fillna("").to_dict(orient="records"):
        raw_result = collect_page(
            url=str(row["url"]).strip(),
            team=str(row["team"]).strip(),
            source_type=str(row["source_type"]).strip(),
            screenshot_dir=screenshots_dir,
            headless=not args.headful,
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
    print(f"Screenshot directory: {screenshots_dir}")


if __name__ == "__main__":
    main()
