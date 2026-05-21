#!/usr/bin/env python3
"""
Update feature images in feature pages and features.html
Map feature slugs to image filenames and update image paths accordingly.
"""

from pathlib import Path
import re


def get_feature_to_image_map():
    """Create a mapping of feature slugs to image filenames"""
    feature_dir = Path("assets/img/features")
    image_map = {}

    if feature_dir.exists():
        for img_file in feature_dir.glob("*.webp"):
            # Image filename is the feature slug
            slug = img_file.stem
            image_map[slug] = img_file.name

    return image_map


def update_feature_pages(image_map):
    """Update image paths in feature HTML pages"""
    feature_dir = Path("feature")
    updated = 0

    for html_file in sorted(feature_dir.glob("*.html")):
        if html_file.name == "feature-template.html" or html_file.name == "INDEX-COMPLETE.html":
            continue

        # Get the feature slug from filename
        slug = html_file.stem

        # Skip if no image for this feature
        if slug not in image_map:
            print(f"[!] No image found for {slug}")
            continue

        img_filename = image_map[slug]

        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Update hero section image (first occurrence)
        # Replace: src="../assets/img/features/feature-template.webp"
        # With: src="../assets/img/features/{img_filename}"
        updated_content = content.replace(
            'src="../assets/img/features/feature-template.webp"',
            f'src="../assets/img/features/{img_filename}"',
            1
        )

        # Update feature highlight section image
        # Replace: src="../assets/img/features-mobile.webp"
        # With: src="../assets/img/features/{img_filename}"
        updated_content = updated_content.replace(
            'src="../assets/img/features-mobile.webp"',
            f'src="../assets/img/features/{img_filename}"'
        )

        if updated_content != content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"[+] Updated {html_file.name} with image {img_filename}")
            updated += 1

    return updated


def update_features_html(image_map):
    """Update image paths in features.html card images"""
    features_file = Path("features.html")

    if not features_file.exists():
        print("[!] features.html not found")
        return 0

    with open(features_file, "r", encoding="utf-8") as f:
        content = f.read()

    updated = 0

    # Find all feature card image URLs
    # Pattern: style="background-image: url('assets/img/features/slug.webp');"
    def replace_bg_image(match):
        nonlocal updated
        href = match.group(1)
        slug = href.split("/")[-1]  # Extract slug from href
        slug = slug.rstrip('"\'')

        if slug in image_map:
            img_filename = image_map[slug]
            old_src = match.group(0)
            new_src = old_src.replace(
                f"assets/img/features/{slug}.webp",
                f"assets/img/features/{img_filename}"
            )
            if old_src != new_src:
                updated += 1
                print(f"[+] Updated features.html card for {slug} with image {img_filename}")
            return new_src

        return match.group(0)

    # Match href="feature/slug" followed by background-image URL
    pattern = r'href="feature/([^"]+)"[^>]*>.*?style="background-image: url\'assets/img/features/[^\']+\.webp\''
    updated_content = re.sub(
        r'style="background-image: url(\'assets/img/features/[^\']+\.webp\')',
        lambda m: m.group(0),
        content
    )

    # Alternative approach: find each card and update its image
    for slug, img_filename in image_map.items():
        # Find the card for this feature
        old_pattern = f'href="feature/{slug}"'
        if old_pattern in updated_content:
            # Find the background-image in this card
            # Look for the next style="background-image: url..." after the href
            card_pattern = (
                f'href="feature/{slug}"[^>]*>.*?'
                f'style="background-image: url(\'assets/img/features/[^\']+\.webp\')'
            )
            # Replace the image filename
            updated_content = re.sub(
                f'(href="feature/{slug}"[^>]*>.*?style="background-image: url\(\'assets/img/features/)[^\']+(\\.webp\')',
                f'\\1{img_filename}\\2',
                updated_content,
                flags=re.DOTALL
            )

    if updated_content != content:
        with open(features_file, "w", encoding="utf-8") as f:
            f.write(updated_content)
        return updated

    return updated


def main():
    """Main function"""
    print("[*] Building feature-to-image mapping...")
    image_map = get_feature_to_image_map()
    print(f"[+] Found {len(image_map)} feature images")

    print("\n[*] Updating feature pages...")
    feature_pages_updated = update_feature_pages(image_map)
    print(f"[+] Updated {feature_pages_updated} feature pages")

    print("\n[*] Updating features.html...")
    features_html_updated = update_features_html(image_map)
    print(f"[+] Updated {features_html_updated} cards in features.html")

    print("\n[+] Image update complete!")


if __name__ == "__main__":
    main()
