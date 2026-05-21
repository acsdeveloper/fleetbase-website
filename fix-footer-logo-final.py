#!/usr/bin/env python3
"""
Fix footer logo image from features-mobile images to fleetyes.svg
across all feature pages
"""

from pathlib import Path
import re


def fix_footer_logos():
    """Replace all feature mobile images with fleetyes.svg in footer logo"""
    feature_dir = Path("feature")
    fixed = 0

    for html_file in sorted(feature_dir.glob("*.html")):
        if html_file.name in ["feature-template.html", "INDEX-COMPLETE.html"]:
            continue

        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Replace any features-mobile image in footer logo with fleetyes.svg
        # Pattern: <img src="../assets/img/features-mobile/...webp" alt="FleetYes">
        # This is in the footer-about section, so we target it specifically

        # Replace all variations of features-mobile images in footer with fleetyes.svg
        content = re.sub(
            r'(<a href="\.\./" class="logo d-flex align-items-center">\s*<img src=")\.\.\/assets\/img\/features-mobile\/[^"]+\.webp(")',
            r'\1../assets/img/fleetyes.svg\2',
            content,
            flags=re.DOTALL
        )

        if content != original_content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(content)
            fixed += 1
            print(f"[+] {html_file.name}: Fixed footer logo")

    return fixed


def main():
    """Main function"""
    print("[*] Fixing footer logos across all feature pages...\n")

    fixed = fix_footer_logos()

    print(f"\n[+] Fixed {fixed} feature pages")
    print("[+] Complete!")


if __name__ == "__main__":
    main()
