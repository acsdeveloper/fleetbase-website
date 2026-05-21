#!/usr/bin/env python3
"""
Fix footer logo image from features-mobile.webp to fleetyes.svg
"""

from pathlib import Path


def fix_footer_logo():
    """Replace features-mobile.webp with fleetyes.svg in footer"""
    feature_dir = Path("feature")
    fixed = 0

    for html_file in sorted(feature_dir.glob("*.html")):
        if html_file.name in ["feature-template.html", "INDEX-COMPLETE.html"]:
            continue

        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Replace the logo image in footer
        content = content.replace(
            '<img src="../assets/img/features-mobile.webp" alt="FleetYes">',
            '<img src="../assets/img/fleetyes.svg" alt="FleetYes">'
        )

        if content != original_content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(content)
            fixed += 1
            print(f"[+] {html_file.name}: Fixed footer logo")

    return fixed


def main():
    """Main function"""
    print("[*] Fixing footer logo images...\n")

    fixed = fix_footer_logo()

    print(f"\n[+] Fixed {fixed} feature pages")
    print("[+] Complete!")


if __name__ == "__main__":
    main()
