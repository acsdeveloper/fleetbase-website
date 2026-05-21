#!/usr/bin/env python3
"""
Remove multi-instance deep linking (href="#") from feature pages.
Replace with proper links or remove the href attribute.
"""

from pathlib import Path
import re


def remove_deep_links(content: str) -> str:
    """Remove href="#" deep links from footer navigation"""
    # Replace footer policy links with proper hrefs or remove the link
    # Privacy Policy: href="#" id="open_preferences_center" -> href="/privacy"
    content = re.sub(
        r'<a href="#" id="open_preferences_center">Privacy Policy</a>',
        '<a href="/privacy">Privacy Policy</a>',
        content
    )

    # Cookie Policy: href="#" id="open_preferences_center" -> href="/cookies"
    content = re.sub(
        r'<a href="#" id="open_preferences_center">Cookie Policy</a>',
        '<a href="/cookies">Cookie Policy</a>',
        content
    )

    # Terms and Conditions: href="#" id="open_preferences_center" -> href="/terms"
    content = re.sub(
        r'<a href="#" id="open_preferences_center">Terms and Conditions</a>',
        '<a href="/terms">Terms and Conditions</a>',
        content
    )

    # Scroll to top: href="#" id="scroll-top" -> remove href or use proper anchor
    # Keep this one as-is since it's JavaScript-driven, just remove href="#"
    content = re.sub(
        r'<a href="#" id="scroll-top"',
        '<a id="scroll-top"',
        content
    )

    return content


def process_feature_pages():
    """Process all feature HTML pages"""
    feature_dir = Path("feature")
    processed = 0
    total_links_removed = 0

    for html_file in sorted(feature_dir.glob("*.html")):
        if html_file.name in ["feature-template.html", "INDEX-COMPLETE.html"]:
            continue

        with open(html_file, "r", encoding="utf-8") as f:
            original_content = f.read()

        # Count deep links before
        deep_links_before = len(re.findall(r'href="#"', original_content))
        if deep_links_before == 0:
            continue

        # Remove deep links
        new_content = remove_deep_links(original_content)

        # Write back
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(new_content)

        total_links_removed += deep_links_before
        processed += 1
        print(f"[+] {html_file.name}: Removed {deep_links_before} deep links")

    return processed, total_links_removed


def update_template():
    """Update the feature template"""
    template_file = Path("feature/feature-template.html")

    if not template_file.exists():
        print("[!] Template not found")
        return False

    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    content = remove_deep_links(content)

    if content != original_content:
        with open(template_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("[+] Updated feature-template.html")
        return True

    return False


def main():
    """Main function"""
    print("[*] Removing multi-instance deep links from feature pages...\n")

    # Update template first
    print("[*] Updating template...")
    update_template()

    # Process feature pages
    print("\n[*] Processing feature pages...")
    processed, total_removed = process_feature_pages()

    print(f"\n[+] Processed {processed} feature pages")
    print(f"[+] Total deep links removed: {total_removed}")
    print("[+] Complete!")


if __name__ == "__main__":
    main()
