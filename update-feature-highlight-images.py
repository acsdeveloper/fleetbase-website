#!/usr/bin/env python3
"""
Update Feature Highlight section images to use mobile images.
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


def update_feature_pages(mobile_images):
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
            print(f"[+] {html_file.name}: Using {slug}-mobile.webp")
        else:
            # Use fallback image
            mobile_image_url = "../assets/img/features-mobile.webp"
            print(f"[!] {html_file.name}: Using fallback image (no {slug}-mobile.webp found)")
            fallback_count += 1

        # Update Feature Highlight section image
        # Pattern: src="../assets/img/features-mobile.webp" in feature-highlight section
        # We need to be careful to only replace in the feature-highlight section

        # Find feature-highlight section and update the image
        pattern = r'(<div class="feature-highlight-section">.*?)<img[^>]*src="[^"]*assets/img/features-mobile[^"]*"'
        replacement = rf'\1<img src="{mobile_image_url}"'

        updated_content = re.sub(
            pattern,
            replacement,
            content,
            flags=re.DOTALL
        )

        # If regex didn't match, try a simpler approach for the feature-highlight section
        if updated_content == content:
            # Look for the specific image in feature-highlight-content
            pattern = r'(<div class="feature-highlight-content">.*?)<img[^>]*src="[^"]*"'
            replacement = rf'\1<img src="{mobile_image_url}"'
            updated_content = re.sub(
                pattern,
                replacement,
                content,
                flags=re.DOTALL
            )

        if updated_content != original_content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(updated_content)
            updated += 1

    return updated, fallback_count


def main():
    """Main function"""
    print("[*] Getting available mobile images...\n")
    mobile_images = get_available_mobile_images()
    print(f"[+] Found {len(mobile_images)} mobile images\n")

    print("[*] Updating Feature Highlight section images...")
    updated, fallback_count = update_feature_pages(mobile_images)

    print(f"\n[+] Updated {updated} feature pages")
    print(f"[+] Used fallback image for {fallback_count} pages")
    print("[+] Complete!")


if __name__ == "__main__":
    main()
