# Notion Scripts

Collection of utility scripts for Notion.

## Scripts

### clear_trash.py

Permanently deletes all pages in the trash across all workspaces.

**Warning:** This action is irreversible.

```bash
python src/clear_trash.py <token_v2>
```

#### Getting your token_v2

1. Open [notion.so](https://www.notion.so) in your browser
2. Open Developer Tools (`F12`)
3. Go to **Application** > **Cookies** > `www.notion.so`
4. Copy the value of `token_v2`

### md_size_report.py

Analyzes markdown files exported from Joplin (originally imported from Evernote ENEX) and calculates total size (text + resources) for each file. Outputs results to CSV sorted by size.

### import.py

Imports markdown files to Notion using the md2notionpage library.

## Setup

```bash
pip install -r requirements.txt
```
