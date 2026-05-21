#!/usr/bin/env python3
"""
Remove all em dashes (—) from feature pages.
Replace em dashes with hyphens or spaces as appropriate.
"""

from pathlib import Path
import re


def remove_em_dashes(content: str) -> str:
    """Remove all em dashes from content"""
    # Replace em dash surrounded by spaces with hyphen and spaces
    content = content.replace(' — ', ' - ')
    # Replace em dash at start of line with hyphen
    content = re.sub(r'^—\s*', '- ', content, flags=re.MULTILINE)
    # Replace em dash at end of line with hyphen
    content = re.sub(r'\s*—$', ' -', content, flags=re.MULTILINE)
    # Replace any remaining em dashes with hyphens
    content = content.replace('—', '-')
    return content


def process_feature_pages():
    """Process all feature HTML pages"""
    feature_dir = Path("feature")
    processed = 0
    total_dashes_removed = 0

    for html_file in sorted(feature_dir.glob("*.html")):
        if html_file.name == "feature-template.html":
            continue

        with open(html_file, "r", encoding="utf-8") as f:
            original_content = f.read()

        # Count em dashes before
        dashes_before = original_content.count('—')
        if dashes_before == 0:
            continue

        # Remove em dashes
        new_content = remove_em_dashes(original_content)

        # Write back
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(new_content)

        total_dashes_removed += dashes_before
        processed += 1
        print(f"[+] {html_file.name}: Removed {dashes_before} em dashes")

    return processed, total_dashes_removed


def update_template():
    """Update the feature template"""
    template_file = Path("feature/feature-template.html")

    if not template_file.exists():
        return 0

    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    dashes_before = content.count('—')

    if dashes_before == 0:
        return 0

    content = remove_em_dashes(content)

    if content != original_content:
        with open(template_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] feature-template.html: Removed {dashes_before} em dashes")
        return dashes_before

    return 0


def main():
    """Main function"""
    print("[*] Removing all em dashes from feature pages...\n")

    # Update template first
    template_dashes = update_template()

    # Process feature pages
    processed, total_removed = process_feature_pages()

    total_removed += template_dashes

    print(f"\n[+] Processed {processed} feature pages")
    print(f"[+] Total em dashes removed: {total_removed}")
    print("[+] Complete!")


if __name__ == "__main__":
    main()
