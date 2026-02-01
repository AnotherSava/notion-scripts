# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python utility scripts for Notion workspace management and Evernote markdown migration.

## Setup

```bash
pip install -r requirements.txt
```

Environment variables in `.env`:
- `NOTION_SECRET`: Notion API secret token
- `NOTION_PARENT_PAGE_ID`: Target page ID for imports

## Running Scripts

```bash
# Clear all trashed pages from Notion workspaces (requires token_v2 cookie)
python src/clear_trash.py <token_v2>

# Generate CSV report of Evernote markdown file sizes
python src/md_size_report.py

# Import markdown to Notion (via md2notionpage)
md2notionpage "path/to/file.md"
```

## Architecture

**src/clear_trash.py**: Notion trash cleanup using undocumented API v3 endpoints (`loadUserContent`, `search`, `deleteBlocks`). Uses token_v2 cookie authentication. Batch deletes 10 blocks per request.

**src/md_size_report.py**: Analyzes markdown files exported from Joplin (originally from Evernote ENEX), extracts resource references via regex, outputs CSV sorted by total size. Has hardcoded Windows paths.

## Notes

- No testing infrastructure or linting configured
- Scripts use Notion's internal API (not official REST API) - endpoints may change
- token_v2 can be obtained from browser cookies at notion.so
