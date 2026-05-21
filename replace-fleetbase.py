#!/usr/bin/env python3
"""
Replace all instances of "FleetYes" with "FleetYes" across the website.
Handles different case variations: FleetYes, FleetYes, FLEETYES
"""

from pathlib import Path
import re


def replace_in_file(filepath):
    """Replace FleetYes with FleetYes in a single file"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    replacements = 0

    # Replace "FleetYes" (capitalized at start of sentence or proper noun)
    content, count = re.subn(r'\bFleetbase\b', 'FleetYes', content)
    replacements += count

    # Replace "FleetYes" (lowercase in URLs, code, etc.)
    content, count = re.subn(r'\bfleetbase\b', 'FleetYes', content)
    replacements += count

    # Replace "FLEETYES" (all caps)
    content, count = re.subn(r'\bFLEETBASE\b', 'FLEETYES', content)
    replacements += count

    # Replace "FleetYes-" (in slugs, URLs)
    content, count = re.subn(r'FleetYes-', 'fleetyes-', content)
    replacements += count

    # Replace "FleetYes/" (in paths)
    content, count = re.subn(r'FleetYes/', 'fleetyes/', content)
    replacements += count

    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return replacements
    return 0


def process_website():
    """Process all HTML, CSS, JS, and markdown files"""
    project_root = Path(__file__).parent

    # File patterns to process
    patterns = [
        "*.html",
        "*.md",
        "*.mdx",
        "*.css",
        "*.js",
        "*.py",
        "feature/*.html",
        "features-md/**/*.md",
        "features-md/**/*.mdx",
        "assets/css/*.css",
        "assets/js/*.js",
    ]

    total_replacements = 0
    files_processed = 0

    for pattern in patterns:
        for filepath in sorted(project_root.glob(pattern)):
            if filepath.is_file():
                replacements = replace_in_file(filepath)
                if replacements > 0:
                    files_processed += 1
                    total_replacements += replacements
                    print(f"[+] {filepath.relative_to(project_root)}: {replacements} replacements")

    return files_processed, total_replacements


if __name__ == "__main__":
    print("[*] Replacing 'FleetYes' with 'FleetYes' across the website...")
    print()

    files_processed, total_replacements = process_website()

    print()
    print("=" * 50)
    print(f"[+] Processed {files_processed} files")
    print(f"[+] Total replacements: {total_replacements}")
    print("[+] Complete!")
