#!/usr/bin/env python3
"""
Update Feature Highlight section images to use the newly uploaded mobile images.
Use assets/img/features-mobile/{slug}-mobile.webp if available,
otherwise fallback to assets/img/features-mobile.webp
"""

from pathlib import Path
import re


def get_available_mobile_images():
    """Get list of available mobile images"""
    mobile_dir = Path("assets/img/features-mobile")
    mobile_images = set()

    if mobile_dir.exists():
        for img_file in mobile_dir.glob("*-mobile.webp"):
            # Extract slug from filename (remove -mobile.webp suffix)
            slug = img_file.stem.replace("-mobile", "")
            mobile_images.add(slug)

    return mobile_images


def update_feature_highlight_images(mobile_images):
    """Update Feature Highlight images in feature pages"""
    feature_dir = Path("feature")
    updated = 0
    fallback_count = 0

    for html_file in sorted(feature_dir.glob("*.html")):
        if html_file.name in ["feature-template.html", "INDEX-COMPLETE.html"]:
            continue

        # Get feature slug from filename
        slug = html_file.stem

        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Determine which image to use
        if slug in mobile_images:
            # Use specific mobile image
            mobile_image_url = f"../assets/img/features-mobile/{slug}-mobile.webp"
            action = "Using"
        else:
            # Use fallback image
            mobile_image_url = "../assets/img/features-mobile.webp"
            action = "Using fallback"
            fallback_count += 1

        # Find and update the feature-highlight section image
        # Pattern: <section class="feature-highlight-section">
        #          <img src="..." alt="..." class="feature-highlight-image">

        # Replace the img src within feature-highlight-section
        pattern = r'(<section class="feature-highlight-section">\s*<img[^>]*src=")[^"]*(")'
        replacement = rf'\1{mobile_image_url}\2'

        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        if updated_content != original_content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(updated_content)
            updated += 1
            print(f"[+] {html_file.name}: {action} {Path(mobile_image_url).name}")
        else:
            print(f"[!] {html_file.name}: Could not find Feature Highlight section")

    return updated, fallback_count


def main():
    """Main function"""
    print("[*] Getting available mobile images...\n")
    mobile_images = get_available_mobile_images()
    print(f"[+] Found {len(mobile_images)} mobile images\n")

    print("[*] Updating Feature Highlight section images...")
    updated, fallback_count = update_feature_highlight_images(mobile_images)

    print(f"\n[+] Updated {updated} feature pages")
    print(f"[+] Used fallback image for {fallback_count} pages")
    print("[+] Complete!")


if __name__ == "__main__":
    main()
