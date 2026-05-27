# football-matchday-briefing-workflow

一个轻量的浏览器自动化 workflow 学习项目，用 Python + Playwright 手动访问公开的足球比赛 / 新闻网页 URL，提取页面标题、正文片段，保存截图，并输出 CSV 与 Markdown 比赛日简报。

This is a lightweight browser automation workflow learning project. It uses Python + Playwright to visit publicly provided football match/news URLs, extract page titles and body snippets, save screenshots, and generate CSV and Markdown matchday briefings.

## Scope / 范围

- 只处理手动提供的公开 URL
- No login, no CAPTCHA bypass, no paid/restricted content
- 不做高频批量抓取，不包装成大型 AI 系统

## Project Layout / 目录

- `data/`：输入 URL 列表
- `examples/`：不含第三方真实网页内容的示例输出
- `templates/`：前瞻写作模板与提示词模板
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

也可以先复制一个输入样例，再按自己的关注对象修改：

```powershell
Copy-Item data\match_urls.example.csv data\match_urls.csv
```

## Input Format / 输入格式

运行前需要先编辑 `data/match_urls.csv`。
如果你是第一次使用，也可以先参考 `data/match_urls.example.csv`。

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

## CLI Usage / 命令行参数

基础运行:

```bash
python run_workflow.py
```

指定输入、输出目录和处理条数:

```bash
python run_workflow.py --input data/match_urls.csv --output-dir outputs --screenshot-dir screenshots --limit 2
```

如果你想看到浏览器窗口，可以加 `--headful`:

```bash
python run_workflow.py --headful
```

参数说明:

- `--input`：输入 CSV 路径，默认 `data/match_urls.csv`
- `--output-dir`：CSV 和 Markdown 输出目录，默认 `outputs`
- `--screenshot-dir`：截图目录，默认 `screenshots`
- `--limit`：只处理前 N 条输入，适合先做小范围检查
- `--headful`：以可见模式启动 Chromium；默认仍是 headless

## AI-Assisted Preview Workflow / AI 辅助前瞻写作流程

v0.3 在原来的 browser automation workflow 之上，加了一层 lightweight AI-assisted match preview writing workflow。

建议流程：

1. 先运行采集

```bash
python run_workflow.py --input data/match_urls.csv --limit 5
```

2. 再生成前瞻写作资料包

```bash
python generate_preview_pack.py --match-title "Your Match Preview Title" --user-angle "你的个人视角"
```

3. 本地生成以下文件

- `outputs/source_digest.md`
- `outputs/ai_writing_prompt.md`
- `outputs/human_notes_template.md`

4. 使用方式

- 用户将 `source_digest.md` 和 `ai_writing_prompt.md` 复制给 ChatGPT
- ChatGPT 可以生成一版赛前前瞻初稿
- 用户再填写 `human_notes_template.md`
- 最终发布稿由用户自己核查、编辑和补充个人判断

这个流程不调用 OpenAI API，也不会自动发布内容。它只是把公开网页整理成更适合 AI 辅助写作的本地资料包。

## Output Files / 输出文件

运行 `python run_workflow.py` 后，会在本地生成：

- `outputs/collected_pages.csv`
- `outputs/matchday_briefing.md`
- `screenshots/*.png`

这些运行产物默认不提交到 GitHub，因为其中可能包含第三方网页正文片段和截图。仓库默认只保留 workflow 代码、配置和输入样例。

仓库中另外提供了两个纯示例文件，方便陌生用户先理解输出结构，而不用先运行真实网页抓取：

- `examples/sample_collected_pages.csv`
- `examples/sample_matchday_briefing.md`

这些示例内容是虚构的，不包含第三方真实网页正文或截图。

v0.3 还会在本地生成以下写作资料：

- `outputs/source_digest.md`
- `outputs/ai_writing_prompt.md`
- `outputs/human_notes_template.md`

这些也属于本地运行产物，默认不提交到 GitHub。

## Status Meaning / 状态说明

- `success` = page opened and useful text was collected
- `blocked` = page opened but content appears access-restricted, such as Access Denied / CAPTCHA / region restriction
- `failed` = page could not be opened or processed

`blocked` 不表示脚本异常，很多时候只是目标站点对公开访问做了额外限制。

## Example Use Case / 示例用法

一个常见用法是：把自己关注的球队官网新闻页、联赛赛程页、比赛前瞻页整理到 `match_urls.csv`，然后运行脚本，在本地生成一份简单的 matchday briefing。它不是新闻聚合平台，也不是大型 AI 系统，更像一个 lightweight browser automation workflow，帮助你把手动选好的公开网页整理成结构化输出。

如果你还想继续往前一步，可以把这些来源整理结果再交给 `generate_preview_pack.py`，生成 `source_digest.md` 和 AI 写稿提示词，再复制给 ChatGPT 起草一版赛前前瞻初稿，最后由你自己补上球迷视角、个人判断和最终核查。

## Project Scope / 项目边界

- 只处理手动提供的公开 URL
- 不做登录，不绕过验证码，不处理付费或受限内容
- 不承诺所有网站都能成功访问或稳定返回正文
- 更适合作为个人使用或学习用途的 lightweight browser automation workflow
- 不提供自动事实核验
- AI 初稿不能直接无审核发布
- 最终发布内容需要用户自己核查和编辑

## Troubleshooting / 常见问题

- 如果提示 `No module named playwright`，先运行 `pip install -r requirements.txt`
- 如果提示 browser not installed，运行 `python -m playwright install chromium`
- 如果某个网站返回 `Access Denied`、`CAPTCHA`、地区限制或其他访问限制，这是正常情况；本项目不会绕过这些限制，只会记录为 `blocked`
- 如果 `outputs/` 里没有文件，先检查 `data/match_urls.csv` 是否存在有效 URL，且当前环境已经安装依赖和 Chromium 浏览器
- 如果 `outputs/collected_pages.csv` 不存在，就先运行 `python run_workflow.py`
- 如果 `generate_preview_pack.py` 提示输入文件缺失，说明前一步采集结果还没有生成

## Notes / 说明

Some public pages may return Access Denied, CAPTCHA, region-restricted, or other access-limited responses. This project does not try to bypass them; it only records them as `blocked` or `failed`.
