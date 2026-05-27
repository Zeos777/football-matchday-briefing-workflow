# football-matchday-briefing-workflow

一个轻量的浏览器自动化 workflow 学习项目，用 Python + Playwright 手动访问公开的足球比赛 / 新闻网页 URL，提取页面标题、正文片段，保存截图，并输出 CSV 与 Markdown 比赛日简报。

This is a lightweight browser automation workflow learning project. It uses Python + Playwright to visit publicly provided football match/news URLs, extract page titles and body snippets, save screenshots, and generate CSV and Markdown matchday briefings.

## Scope / 范围

- 只处理手动提供的公开 URL
- No login, no CAPTCHA bypass, no paid/restricted content
- 不做高频批量抓取，不包装成大型 AI 系统

## Project Layout / 目录

- `data/`：输入 URL 列表
- `src/`：采集、解析、写出简报的基础模块
- `screenshots/`：页面截图输出，本地运行后生成
- `outputs/`：CSV / Markdown 结果输出，本地运行后生成

## Quick Start / 快速开始

```bash
git clone <your-repo-url>
cd football-matchday-briefing-workflow
python -m venv .venv
```

Windows 激活虚拟环境:

```powershell
.venv\Scripts\activate
```

安装依赖并运行:

```bash
pip install -r requirements.txt
python -m playwright install chromium
python run_workflow.py
```

## Input Format / 输入格式

运行前需要先编辑 [data/match_urls.csv](D:/github/football-matchday-briefing-workflow/data/match_urls.csv)。

CSV 格式:

```csv
team,source_type,url
Liverpool,official_news,https://www.liverpoolfc.com/news
Arsenal,official_news,https://www.arsenal.com/news
Premier League,fixtures,https://www.premierleague.com/fixtures
```

字段说明:

- `team` = team or topic name
- `source_type` = `official_news` / `fixtures` / `preview` / `result` / `other`
- `url` = public webpage URL

这个文件只适合放手动挑选的公开页面，不适合做高频批量抓取列表。

## Output Files / 输出文件

运行 `python run_workflow.py` 后，会在本地生成：

- `outputs/collected_pages.csv`
- `outputs/matchday_briefing.md`
- `screenshots/*.png`

这些运行产物默认不提交到 GitHub，因为其中可能包含第三方网页正文片段和截图。仓库默认只保留 workflow 代码、配置和输入样例。

## Status Meaning / 状态说明

- `success` = page opened and useful text was collected
- `blocked` = page opened but content appears access-restricted, such as Access Denied / CAPTCHA / region restriction
- `failed` = page could not be opened or processed

`blocked` 不表示脚本异常，很多时候只是目标站点对公开访问做了额外限制。

## Example Use Case / 示例用法

一个常见用法是：把自己关注的球队官网新闻页、联赛赛程页、比赛前瞻页整理到 `match_urls.csv`，然后运行脚本，在本地生成一份简单的 matchday briefing。它不是新闻聚合平台，也不是大型 AI 系统，更像一个 lightweight browser automation workflow，帮助你把手动选好的公开网页整理成结构化输出。

## Troubleshooting / 常见问题

- 如果提示 `No module named playwright`，先运行 `pip install -r requirements.txt`
- 如果提示 browser not installed，运行 `python -m playwright install chromium`
- 如果某个网站返回 `Access Denied`、`CAPTCHA`、地区限制或其他访问限制，这是正常情况；本项目不会绕过这些限制，只会记录为 `blocked`
- 如果 `outputs/` 里没有文件，先检查 `data/match_urls.csv` 是否存在有效 URL，且当前环境已经安装依赖和 Chromium 浏览器

## Notes / 说明

Some public pages may return Access Denied, CAPTCHA, region-restricted, or other access-limited responses. This project does not try to bypass them; it only records them as `blocked` or `failed`.
