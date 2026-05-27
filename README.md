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

## Run / 运行

- `pip install -r requirements.txt`
- `playwright install`
- `python run_workflow.py`

Running `python run_workflow.py` will generate local CSV, Markdown, and screenshots in `outputs/` and `screenshots/`.

默认不把第三方网页截图和抓取正文提交到 GitHub，仓库只保留 workflow 代码和输入样例。

Some public pages may return Access Denied, CAPTCHA, region-restricted, or other access-limited responses. This project does not try to bypass them; it only records them as `blocked` or `failed`.
