#!/usr/bin/env python3
"""
Clean up Getting Started sections in feature files.
Remove markdown link syntax ([**text**](#) — description) and keep only plain text.
"""

from pathlib import Path
import re


def clean_getting_started(content: str) -> str:
    """Remove markdown links and link descriptions from Getting Started section"""
    # Pattern to match markdown links with description
    # [**text**](#) — description or [text](#) — description
    content = re.sub(r'\n\[.*?\]\(#\)\s*[-–—]\s*[^\n]*', '', content)
    # Also remove plain markdown links without descriptions
    content = re.sub(r'\[([^\]]+)\]\(#\)', r'\1', content)
    return content


def process_feature_files():
    """Process all markdown feature files"""
    project_root = Path(__file__).parent
    features_dirs = [
        project_root / "features-md" / "mobileapp" / "features",
        project_root / "features-md" / "dashboard" / "features",
    ]

    processed = 0
    cleaned_sections = 0

    for features_dir in features_dirs:
        if not features_dir.exists():
            continue

        for filepath in sorted(features_dir.glob("*.md*")):
            with open(filepath, "r", encoding="utf-8") as f:
                original_content = f.read()

            # Check if file has Getting Started section with links
            if "## Getting Started" not in original_content:
                continue

            # Count link patterns before
            links_before = len(re.findall(r'\[.*?\]\(#\)', original_content))
            if links_before == 0:
                continue

            # Clean content
            new_content = clean_getting_started(original_content)

            # Write back
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)

            processed += 1
            cleaned_sections += 1
            print(f"[+] {filepath.name}: Removed {links_before} markdown links")

    print(f"\n[+] Processed {processed} files")
    print(f"[+] Cleaned {cleaned_sections} Getting Started sections")


if __name__ == "__main__":
    process_feature_files()
