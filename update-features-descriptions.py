#!/usr/bin/env python3
"""
Update features.html with correct short descriptions from generated feature pages.
Extracts subtitle from each feature page and updates the corresponding card in features.html.
"""

import re
from pathlib import Path


def extract_subtitle_from_page(html_content: str) -> str:
    """Extract the subtitle from a feature page HTML"""
    match = re.search(r'<p class="subtitle">(.*?)</p>', html_content, re.DOTALL)
    if match:
        text = match.group(1).strip()
        # Remove any HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        return text
    return ""


def get_feature_subtitle(feature_slug: str, feature_dir: Path) -> str:
    """Get the subtitle for a feature from its HTML file"""
    html_file = feature_dir / f"{feature_slug}.html"
    if not html_file.exists():
        return ""

    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
        return extract_subtitle_from_page(content)


def update_features_html():
    """Update features.html with correct descriptions"""
    project_root = Path(__file__).parent
    feature_dir = project_root / "feature"
    features_file = project_root / "features.html"

    if not features_file.exists():
        print("[!] features.html not found")
        return

    with open(features_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all feature card links with href="feature/slug"
    # Pattern: href="feature/slug" ... <p>old description</p>
    pattern = r'href="feature/([^"]+)"[^>]*>.*?<div class="feature-card-content">.*?<h3>([^<]+)</h3>\s*<p>(.*?)</p>'

    def replace_description(match):
        slug = match.group(1)
        title = match.group(2)
        old_desc = match.group(3)

        # Get new description from feature page
        new_desc = get_feature_subtitle(slug, feature_dir)

        if new_desc and new_desc != old_desc:
            print(f"[+] Updating {slug}: {new_desc[:80]}")
            # Return the full matched group with new description
            full_match = match.group(0)
            return full_match.replace(f"<p>{old_desc}</p>", f"<p>{new_desc}</p>")

        return match.group(0)

    # Update descriptions
    updated_content = re.sub(pattern, replace_description, content, flags=re.DOTALL)

    # Write back
    with open(features_file, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("[+] features.html updated successfully")


if __name__ == "__main__":
    update_features_html()
