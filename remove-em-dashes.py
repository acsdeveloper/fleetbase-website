#!/usr/bin/env python3
"""
Remove all em dashes (—) from feature pages and features.html
Replace em dashes with hyphens or spaces as appropriate
"""

from pathlib import Path
import re


def remove_em_dashes(content: str) -> str:
    """Remove em dashes from content, replacing with hyphens or spaces"""
    # Replace em dash surrounded by spaces with hyphen and spaces
    content = re.sub(r'\s+—\s+', ' - ', content)
    # Replace em dash at start/end of line with hyphen
    content = re.sub(r'^—\s*', '- ', content, flags=re.MULTILINE)
    content = re.sub(r'\s*—$', ' -', content, flags=re.MULTILINE)
    # Replace any remaining em dashes with hyphens
    content = content.replace('—', '-')
    return content


def process_files():
    """Process all feature HTML files and features.html"""
    project_root = Path(__file__).parent
    files_to_process = []

    # Add all feature HTML files
    feature_dir = project_root / "feature"
    if feature_dir.exists():
        files_to_process.extend(feature_dir.glob("*.html"))

    # Add features.html
    features_file = project_root / "features.html"
    if features_file.exists():
        files_to_process.append(features_file)

    processed = 0
    total_dashes_removed = 0

    for filepath in sorted(files_to_process):
        with open(filepath, "r", encoding="utf-8") as f:
            original_content = f.read()

        # Count em dashes before
        dashes_before = original_content.count('—')
        if dashes_before == 0:
            continue

        # Remove em dashes
        new_content = remove_em_dashes(original_content)

        # Write back
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        total_dashes_removed += dashes_before
        processed += 1
        print(f"[+] {filepath.name}: Removed {dashes_before} em dashes")

    print(f"\n[+] Processed {processed} files")
    print(f"[+] Total em dashes removed: {total_dashes_removed}")


if __name__ == "__main__":
    process_files()
