#!/usr/bin/env python3
"""
Update features.html with all generated feature pages.
Reads HTML files from ./feature/ and updates the features grid.
"""

import os
import re
from pathlib import Path


def find_mobile_feature_file(slug: str) -> Path:
    """Find mobile feature file by slug (accounts for numbered prefixes like 00-, 01-, etc)"""
    mobile_dir = Path("./features-md/mobileapp/features")
    if not mobile_dir.exists():
        return None

    # Try direct match first
    direct_file = mobile_dir / f"{slug}.md"
    if direct_file.exists():
        return direct_file

    # Try to find by matching the slug against file names (handles prefixes like 00-, 01-, etc)
    for md_file in mobile_dir.glob("*.md"):
        # Remove numbered prefix (e.g., "00-driver-operations.md" -> "driver-operations.md")
        filename_without_prefix = re.sub(r'^\d+-', '', md_file.stem)
        if filename_without_prefix == slug:
            return md_file

    return None


def extract_title_and_desc_from_source(slug: str) -> tuple:
    """Extract title and description from source .md or .mdx files"""
    project_root = Path("./features-md")

    # Try dashboard .mdx files first
    dashboard_file = project_root / "dashboard" / "features" / f"{slug}.mdx"
    if dashboard_file.exists():
        try:
            with open(dashboard_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract frontmatter title
            title_match = re.search(r'title:\s*(.+?)(?:\n|$)', content)
            title = title_match.group(1).strip('"\'') if title_match else None

            # Extract description from frontmatter
            desc_match = re.search(r'description:\s*(.+?)(?:\n|$)', content)
            description = desc_match.group(1).strip('"\'') if desc_match else None

            # If no frontmatter description, get first substantive paragraph after title
            if not description:
                para_match = re.search(r'^#.*?\n\n(.+?)(?:\n\n|---)', content, re.MULTILINE)
                if para_match:
                    description = para_match.group(1).strip()[:150]

            return title, description
        except:
            pass

    # Try mobile app .md files (with prefix handling)
    mobile_file = find_mobile_feature_file(slug)
    if mobile_file:
        try:
            with open(mobile_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract title from first # heading
            title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else None

            # Extract description - get first paragraph after title
            para_match = re.search(r'^#.*?\n\n(.+?)(?:\n\n|##)', content, re.MULTILINE)
            description = para_match.group(1).strip()[:150] if para_match else None

            # If still no description, try getting from second line
            if not description:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('##'):
                        # Get the next non-empty line
                        for next_line in lines[i+1:]:
                            if next_line.strip() and not next_line.startswith('#'):
                                description = next_line.strip()[:150]
                                break
                        break

            return title, description
        except:
            pass

    return None, None


def extract_title_and_desc(html_file: Path) -> tuple:
    """Extract title and description - try source files first, then HTML"""
    slug = html_file.stem

    # Try to extract from source files first
    title, description = extract_title_and_desc_from_source(slug)

    if title and description:
        return title, description

    # Fallback to HTML file extraction
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract title from <h1>
        title_match = re.search(r'<h1>(.*?)</h1>', content)
        title = title_match.group(1) if title_match else slug.replace('-', ' ').title()

        # Extract description from <p class="subtitle"> or meta description
        desc_match = re.search(r'<p class="subtitle">([^<]*)</p>', content)
        if desc_match and desc_match.group(1).strip():
            description = desc_match.group(1).strip()
        else:
            # Try meta description
            meta_match = re.search(r'<meta name="description" content="([^"]*)"', content)
            description = meta_match.group(1) if meta_match else None

        if not description:
            return title, None

        # Clean up description
        description = description.replace("&", "&amp;").strip()[:150]
        return title, description
    except:
        return None, None


def get_icon_for_feature(slug: str) -> str:
    """Map feature slug to appropriate Line Awesome icon class"""
    icon_map = {
        # Mobile App Features
        "driver-operations": "bi-briefcase-fill",
        "real-time-order-management": "bi-lightning-charge-fill",
        "gps-navigation-route-tracking": "bi-map",
        "proof-of-delivery": "bi-camera-fill",
        "real-time-chat-communication": "bi-chat-dots-fill",
        "expense-receipt-management": "bi-receipt",
        "issue-reporting": "bi-exclamation-triangle-fill",
        "shift-leave-management": "bi-calendar2-check",
        "performance-tracking-earnings": "bi-graph-up",
        "training-compliance": "bi-mortarboard",
        "driver-profile-documents": "bi-file-person-fill",  # Changed from bi-person-card
        "offline-first-architecture": "bi-cloud-check",  # Changed from bi-cloud-offline
        "ai-receipt-recognition": "bi-robot",
        "background-location-tracking": "bi-geo-alt-fill",
        "push-notifications-real-time-updates": "bi-bell-fill",
        "multi-instance-deep-linking": "bi-link-45deg",
        "biometric-secure-authentication": "bi-fingerprint",
        "internationalisation-localisation": "bi-globe",
        "dark-mode-customisable-themes": "bi-moon-stars-fill",
        "responsive-mobile-ui": "bi-phone",
        "push-notification-services": "bi-bell",

        # Dashboard Features
        "operational-dashboard": "bi-speedometer2",
        "compliance-engine": "bi-shield-check",
        "vehicle-management": "bi-truck",
        "trip-management": "bi-arrow-left-right",
        "driver-management": "bi-people-fill",
        "fuel-tracking": "bi-fuel-pump",
        "import-hub": "bi-download",
        "inventory-management": "bi-box2-fill",
        "leave-management": "bi-calendar-x",
        "toll-expense-tracking": "bi-credit-card",
        "org-settings-permissions": "bi-gear-fill",
        "vehicle-inspection": "bi-clipboard-check",
        "rota-scheduling": "bi-calendar-week",

        # Integration & Components
        "FleetYes-sdk": "bi-code-square",
        "google-maps-navigation-apis": "bi-map-fill",
        "ml-kit-text-recognition": "bi-type",
        "websocket-socketcluster": "bi-diagram-3",
        "geolocation-services": "bi-pin-map",
        "image-processing": "bi-image",
        "calendar-scheduling": "bi-calendar-event",
    }

    for key, icon in icon_map.items():
        if key in slug:
            return icon

    # Default icons based on keywords
    if "dashboard" in slug or "operational" in slug:
        return "bi-speedometer2"
    elif "mobile" in slug or "driver" in slug or "app" in slug:
        return "bi-phone"
    elif "integration" in slug or "sdk" in slug or "api" in slug:
        return "bi-diagram-3"
    else:
        return "bi-star"  # Default icon


def generate_feature_card_html(slug: str, title: str, description: str, image_slug: str = None) -> str:
    """Generate HTML for a single feature card"""
    if image_slug is None:
        image_slug = slug

    icon = get_icon_for_feature(slug)

    return f'''          <a href="feature/{slug}" class="col-md-6 col-xl-3" style="text-decoration: none;">
            <div class="feature-card" style="background-image: url('assets/img/features/{image_slug}.webp');">
              <div class="overlay"></div>
              <div class="feature-card-content">
                <i class="{icon} feature-icon"></i>
                <h3>{title}</h3>
                <p>{description}</p>
              </div>
            </div>
          </a>'''


def main():
    """Main function"""
    print("[*] Updating features.html with generated feature pages...")
    print()

    # Find all generated HTML files
    feature_dir = Path("./feature")
    html_files = sorted([f for f in feature_dir.glob("*.html") if f.name not in ["feature-template.html", "INDEX-COMPLETE.html"]])

    if not html_files:
        print("[!] No feature HTML files found in ./feature/")
        return

    print("[+] Found {} feature pages".format(len(html_files)))

    # Extract titles and descriptions
    features = []
    for html_file in html_files:
        title, desc = extract_title_and_desc(html_file)
        if title and desc:
            slug = html_file.stem
            features.append((slug, title, desc))
            print("  [OK] {} -> {}".format(title[:40], slug))

    # Clean up features with None descriptions and generate fallbacks
    cleaned_features = []
    for slug, title, desc in features:
        if desc is None or desc.strip() == "":
            # Generate description from title
            desc = f"Explore {title} features in FleetYes"
        cleaned_features.append((slug, title, desc))

    features = cleaned_features

    # If extraction failed for some features, regenerate descriptions from filenames
    extracted_slugs = {s for s, t, d in features}
    for html_file in html_files:
        slug = html_file.stem
        if slug not in extracted_slugs:
            # Generate title from slug
            title = slug.replace('-', ' ').title()
            # Generate description from title
            desc = f"Explore {title} features in FleetYes"
            features.append((slug, title, desc))

    if not features:
        print("[!] Could not extract feature data")
        return

    # Categorize features by platform
    # Mobile app features (from mobileapp/features)
    mobile_slugs = {
        "driver-operations",
        "real-time-order-management",
        "gps-navigation-route-tracking",
        "proof-of-delivery",
        "real-time-chat-communication",
        "expense-receipt-management",
        "issue-reporting",
        "shift-leave-management",
        "performance-tracking-earnings",
        "training-compliance",
        "driver-profile-documents",
        "offline-first-architecture",
        "ai-receipt-recognition",
        "background-location-tracking",
        "push-notifications-real-time-updates",
        "biometric-secure-authentication",
        "internationalisation-localisation",
        "dark-mode-customisable-themes",
        "responsive-mobile-ui",
        "multi-instance-deep-linking",
    }

    mobile_features = []
    dashboard_features = []
    integration_features = []

    for slug, title, desc in features:
        if slug in mobile_slugs:
            mobile_features.append((slug, title, desc))
        elif any(x in slug for x in ["dashboard", "operational", "compliance", "vehicle", "trip", "driver-management", "fuel", "import", "inventory", "leave-management", "toll", "org-settings", "inspection", "rota", "training-compliance"]):
            dashboard_features.append((slug, title, desc))
        else:
            integration_features.append((slug, title, desc))

    # Generate feature cards HTML
    mobile_cards = "\n\n".join([generate_feature_card_html(s, t, d) for s, t, d in mobile_features])
    dashboard_cards = "\n\n".join([generate_feature_card_html(s, t, d) for s, t, d in dashboard_features])
    integration_cards = "\n\n".join([generate_feature_card_html(s, t, d) for s, t, d in integration_features]) if integration_features else ""

    # Read current features.html
    with open("features.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the features grid section
    # Find the features grid and replace it
    new_grid = f'''    <!-- Features Grid Section -->
    <section id="keyfeatures" class="services section light-background">

      <div class="container">
        <!-- Mobile App Features -->
        <div class="mb-5">
          <h2 class="section-title mb-4" data-aos="fade-up">Mobile App Features</h2>
          <div class="row gy-4">
            {mobile_cards}
          </div>
        </div>

        <!-- Dashboard Features -->
        <div class="mb-5">
          <h2 class="section-title mb-4" data-aos="fade-up">Dashboard Features</h2>
          <div class="row gy-4">
            {dashboard_cards}
          </div>
        </div>'''

    if integration_cards:
        new_grid += f'''

        <!-- Integration & Components -->
        <div class="mb-5">
          <h2 class="section-title mb-4" data-aos="fade-up">Integrations & Components</h2>
          <div class="row gy-4">
            {integration_cards}
          </div>
        </div>'''

    new_grid += '''
      </div>
    </section>'''

    # Replace old grid with new one
    pattern = r'<!-- Features Grid Section -->.*?</section>'
    content = re.sub(pattern, new_grid, content, flags=re.DOTALL)

    # Write updated features.html
    with open("features.html", "w", encoding="utf-8") as f:
        f.write(content)

    print()
    print("=" * 50)
    print("[+] Updated features.html")
    print("[+] Mobile features: {}".format(len(mobile_features)))
    print("[+] Dashboard features: {}".format(len(dashboard_features)))
    print("[+] Integration features: {}".format(len(integration_features)))
    print("[*] Done!")


if __name__ == "__main__":
    main()
