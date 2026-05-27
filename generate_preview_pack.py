"""Generate a local AI-assisted match preview writing pack from collected pages."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line interface for the preview pack generator."""
    parser = argparse.ArgumentParser(
        description="Generate a source digest and AI writing prompt from collected pages."
    )
    parser.add_argument(
        "--input",
        default="outputs/collected_pages.csv",
        help="Path to collected_pages.csv. Default: outputs/collected_pages.csv",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory for generated Markdown files. Default: outputs",
    )
    parser.add_argument(
        "--match-title",
        default="Football Match Preview",
        help='Title used in the generated preview pack. Default: "Football Match Preview"',
    )
    parser.add_argument(
        "--language",
        default="zh",
        help='Output language hint for the AI prompt. Default: "zh"',
    )
    parser.add_argument(
        "--user-angle",
        default="",
        help="Optional personal angle to emphasize, such as a fan perspective",
    )
    return parser


def load_collected_pages(input_path: Path) -> pd.DataFrame:
    """Load collected pages or exit with a clear message."""
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        print("Please run `python run_workflow.py` first to generate outputs/collected_pages.csv.")
        sys.exit(1)

    dataframe = pd.read_csv(input_path)
    required_columns = {
        "team",
        "source_type",
        "url",
        "page_title",
        "text_excerpt",
        "screenshot_path",
        "status",
        "error",
        "simple_keywords",
    }

    missing = sorted(required_columns - set(dataframe.columns))
    if missing:
        print(f"Missing required columns in {input_path}: {', '.join(missing)}")
        print("Please regenerate the collected pages file with `python run_workflow.py`.")
        sys.exit(1)

    return dataframe.fillna("")


def render_source_digest(
    records: list[dict],
    match_title: str,
    total_count: int,
    success_count: int,
    blocked_count: int,
    failed_count: int,
) -> str:
    """Build the source digest Markdown."""
    teams = sorted({str(item.get("team", "")).strip() for item in records if str(item.get("team", "")).strip()})
    successful = [item for item in records if item.get("status") == "success"]
    blocked_or_failed = [item for item in records if item.get("status") in {"blocked", "failed"}]

    lines = [
        "# Source Digest",
        "",
        "## Match Title",
        match_title,
        "",
        "## Source Summary",
        f"- total sources: {total_count}",
        f"- success count: {success_count}",
        f"- blocked count: {blocked_count}",
        f"- failed count: {failed_count}",
        "",
        "## Teams / Topics Covered",
    ]

    if teams:
        lines.extend([f"- {team}" for team in teams])
    else:
        lines.append("- None")

    lines.extend(["", "## Successful Sources"])

    if successful:
        for item in successful:
            lines.extend(
                [
                    f"### {item.get('team', 'Unknown Team')} / {item.get('source_type', 'other')}",
                    f"- page_title: {item.get('page_title', '') or '(no title)'}",
                    f"- url: {item.get('url', '')}",
                    f"- text_excerpt: {item.get('text_excerpt', '') or '(no excerpt)'}",
                    f"- simple_keywords: {item.get('simple_keywords', '') or '(none)'}",
                ]
            )
            screenshot_path = item.get("screenshot_path", "")
            if screenshot_path:
                lines.append(f"- screenshot_path: {screenshot_path}")
            lines.append("")
    else:
        lines.extend(["- No successful sources.", ""])

    lines.append("## Blocked or Failed Sources")

    if blocked_or_failed:
        lines.append("")
        for item in blocked_or_failed:
            lines.extend(
                [
                    f"### {item.get('team', 'Unknown Team')} / {item.get('source_type', 'other')}",
                    f"- url: {item.get('url', '')}",
                    f"- status: {item.get('status', '')}",
                    f"- error: {item.get('error', '') or '(no error message)'}",
                    "",
                ]
            )
    else:
        lines.extend(["", "- No blocked or failed sources.", ""])

    lines.extend(
        [
            "## Notes for Fact Checking",
            "- 关键事实需要二次核对，尤其是伤病、首发、时间和赛程。",
            "- 不要直接复制第三方正文到最终稿里。",
            "- blocked 页面不应被当作有效来源使用。",
            "- AI 起草内容必须基于这些来源；没有来源支持的内容应标记为“待确认”。",
        ]
    )

    return "\n".join(lines) + "\n"


def render_ai_writing_prompt(match_title: str, language: str, user_angle: str) -> str:
    """Build the AI writing prompt Markdown."""
    lines = [
        "# AI Writing Prompt",
        "",
        "请把下面这段提示词和 `source_digest.md` 一起复制给 ChatGPT。",
        "",
        "```text",
        "你是足球赛前前瞻写作助手。",
        f"请基于我提供的 source_digest.md，写一版{language}赛前前瞻初稿，标题暂定为《{match_title}》。",
        "文章可以有完整结构，不只是 outline。",
        "必须明确区分以下三类内容：",
        "1. 已有来源支持的事实",
        "2. 合理推断",
        "3. 用户个人观点待补充",
        "不要编造伤病、首发、数据、赛程或任何未在来源中出现的确定性信息。",
        "不要复制第三方原文，不要大段复述来源正文。",
        "凡是没有足够来源支持的内容，请直接标注“待确认”。",
        "请在文末保留来源链接，方便我回查。",
        "请给我预留“我的个人感受 / 我的判断”段落，明确留空或加提示语。",
        "语言可以有球迷文章的可读性，但不要标题党，不要装作权威报道。",
        "输出风格应适合后续改写成公众号或朋友圈长文。",
    ]

    if user_angle:
        lines.append(f"请优先照顾这个写作视角：{user_angle}")

    lines.extend(
        [
            "如果来源里有 blocked 或 failed 页面，不要把它们当作有效事实来源。",
            "如果来源不足，请在文中自然提示信息有限，而不是自行补完。",
            "```",
            "",
            "使用说明：先把 `source_digest.md` 放在这段提示词后面，再交给 ChatGPT。",
        ]
    )

    return "\n".join(lines) + "\n"


def render_human_notes_template(match_title: str, user_angle: str) -> str:
    """Build the personal notes template Markdown."""
    lines = [
        "# My Notes / 我的补充",
        "",
        f"- Match Title: {match_title}",
        f"- User Angle: {user_angle or '(optional)'}",
        "",
        "## 我为什么关注这场比赛",
        "",
        "## 我对 Team A 的感受",
        "",
        "## 我对 Team B 的感受",
        "",
        "## 我最期待的对位",
        "",
        "## 我最担心的变量",
        "",
        "## 我的比赛走势判断",
        "",
        "## 我想写进最终稿的一句话",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    """Generate the preview pack files."""
    parser = build_parser()
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent
    input_path = (project_root / args.input).resolve()
    output_dir = (project_root / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    dataframe = load_collected_pages(input_path)
    records = dataframe.to_dict(orient="records")

    total_count = len(records)
    success_count = sum(1 for item in records if item.get("status") == "success")
    blocked_count = sum(1 for item in records if item.get("status") == "blocked")
    failed_count = sum(1 for item in records if item.get("status") == "failed")

    source_digest_path = output_dir / "source_digest.md"
    ai_prompt_path = output_dir / "ai_writing_prompt.md"
    human_notes_path = output_dir / "human_notes_template.md"

    source_digest_path.write_text(
        render_source_digest(
            records=records,
            match_title=args.match_title,
            total_count=total_count,
            success_count=success_count,
            blocked_count=blocked_count,
            failed_count=failed_count,
        ),
        encoding="utf-8",
    )
    ai_prompt_path.write_text(
        render_ai_writing_prompt(
            match_title=args.match_title,
            language=args.language,
            user_angle=args.user_angle,
        ),
        encoding="utf-8",
    )
    human_notes_path.write_text(
        render_human_notes_template(
            match_title=args.match_title,
            user_angle=args.user_angle,
        ),
        encoding="utf-8",
    )

    print("Preview pack generated.")
    print(f"Input CSV: {input_path}")
    print(f"Source digest: {source_digest_path}")
    print(f"AI writing prompt: {ai_prompt_path}")
    print(f"Human notes template: {human_notes_path}")


if __name__ == "__main__":
    main()
