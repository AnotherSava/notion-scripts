"""
Evernote Markdown Size Calculator

Reads markdown files, calculates total size (text + referenced resources),
sorts by size descending, and outputs to CSV.
"""

from pathlib import Path
import re
import csv

NOTEBOOK_DIR = Path(r'D:\backup\Evernote\md\_anothersava_s notebook')
RESOURCES_DIR = Path(r'D:\backup\Evernote\md\_resources')
OUTPUT_CSV = Path(r'D:\projects\notion\output.csv')

# Regex patterns for resource references
PATTERNS = [
    r'!\[.*?\]\(\.\./_resources/([^)]+)\)',           # ![alt](../_resources/file)
    r'(?<!!)\[.*?\]\(\.\./_resources/([^)]+)\)',      # [text](../_resources/file) - not preceded by !
    r'<img[^>]+src=["\']\.\./_resources/([^"\']+)["\']',  # <img src="../_resources/file"
]


def extract_resources(content: str) -> list[str]:
    """Extract all resource filenames from markdown content."""
    resources = []
    for pattern in PATTERNS:
        matches = re.findall(pattern, content)
        resources.extend(matches)
    return resources


def get_file_size(path: Path) -> int:
    """Get file size in bytes, returns 0 if file doesn't exist."""
    try:
        return path.stat().st_size
    except (FileNotFoundError, OSError):
        return 0


def process_markdown_file(md_path: Path) -> tuple[str, int, int, int, int]:
    """
    Process a single markdown file.

    Returns: (filename, text_size, resources_size, total_size, resource_count)
    """
    try:
        content = md_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        content = md_path.read_text(encoding='latin-1')

    text_size = len(content.encode('utf-8'))

    resources = extract_resources(content)
    resource_count = len(resources)

    resources_size = 0
    for resource_name in resources:
        resource_path = RESOURCES_DIR / resource_name
        resources_size += get_file_size(resource_path)

    total_size = text_size + resources_size

    return (md_path.name, text_size, resources_size, total_size, resource_count)


def main():
    print(f"Scanning markdown files in: {NOTEBOOK_DIR}")

    md_files = list(NOTEBOOK_DIR.glob('*.md'))
    print(f"Found {len(md_files)} markdown files")

    results = []
    for i, md_path in enumerate(md_files, 1):
        if i % 100 == 0:
            print(f"Processing {i}/{len(md_files)}...")
        result = process_markdown_file(md_path)
        results.append(result)

    # Sort by total_size descending
    results.sort(key=lambda x: x[3], reverse=True)

    # Write to CSV
    print(f"Writing results to: {OUTPUT_CSV}")
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'text_size_kb', 'resources_size_kb', 'total_size_kb', 'resource_count'])

        for filename, text_size, resources_size, total_size, resource_count in results:
            writer.writerow([
                filename,
                round(text_size / 1024, 2),
                round(resources_size / 1024, 2),
                round(total_size / 1024, 2),
                resource_count
            ])

    print(f"Done! Processed {len(results)} files.")

    # Show top 5 largest files
    print("\nTop 5 largest files:")
    for filename, text_size, resources_size, total_size, resource_count in results[:5]:
        print(f"  {filename}: {total_size/1024/1024:.2f} MB ({resource_count} resources)")


if __name__ == '__main__':
    main()
