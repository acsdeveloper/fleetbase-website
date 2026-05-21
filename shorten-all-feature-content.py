#!/usr/bin/env python3
"""
Shorten all Feature Highlight and Final CTA content to business-benefit-focused text.
For MOBILE features: Extract first 1 sentence from Key Benefits
For DASHBOARD features: Use predefined benefit text
"""

from pathlib import Path
import re


# Predefined benefit text for dashboard features
DASHBOARD_BENEFITS = {
    'compliance-engine': {
        'highlight': 'Compliance checking happens automatically on every assignment. Violations are caught before they happen, not after.',
        'cta': 'Ready to eliminate compliance risk and prevent costly violations?'
    },
    'driver-management': {
        'highlight': 'Keep your driver team compliant, capable, and accountable. Track documents, monitor performance, and reduce compliance risk across the fleet.',
        'cta': 'Ready to streamline driver management and reduce compliance overhead?'
    },
    'fuel-tracking': {
        'highlight': 'See exactly where your fuel costs go. Anomalies are flagged instantly, helping you cut fuel costs by 15-20% and eliminate fraud.',
        'cta': 'Ready to cut fuel costs and eliminate fraud?'
    },
    'import-hub': {
        'highlight': 'Load customer orders, vehicle data, and trip records from any system in minutes. No manual data entry. Integrations work seamlessly with your existing tools.',
        'cta': 'Ready to stop manual data entry and connect your systems?'
    },
    'leave-management': {
        'highlight': 'Approve leave requests instantly and update your schedule in real-time. No more scheduling conflicts. Your roster stays accurate and compliant.',
        'cta': 'Ready to eliminate scheduling conflicts and improve workforce planning?'
    },
    'operational-dashboard': {
        'highlight': 'See your entire fleet operation on one screen. Real-time KPIs show trip volume, driver availability, compliance status, and cost metrics at a glance.',
        'cta': 'Ready to see your entire fleet operation at a glance?'
    },
    'org-settings-permissions': {
        'highlight': 'Control exactly who can see what and do what. Role-based access keeps sensitive data secure while letting teams do their jobs without friction.',
        'cta': 'Ready to secure your data and streamline team access?'
    },
    'rota-scheduling': {
        'highlight': 'Build flexible schedules that respect driver availability and compliance rules. Publish rotas faster. Drivers know their schedule and can plan their lives.',
        'cta': 'Ready to build compliant schedules faster and reduce scheduling headaches?'
    }
}


def extract_first_benefit(content: str) -> str:
    """Extract first benefit from Key Benefits section"""
    # Find Key Benefits section
    match = re.search(
        r'<h2 class="section-title"[^>]*>Key Benefits</h2>.*?'
        r'<div class="benefit-card"[^>]*>.*?<h4>([^<]+)</h4>\s*<p>([^<]+)</p>',
        content,
        re.DOTALL
    )
    if match:
        title = match.group(1).strip()
        desc = match.group(2).strip()
        return f"{title}: {desc}"
    return ""


def shorten_feature_highlight(content: str, slug: str) -> str:
    """Shorten Feature Highlight to benefit-focused text"""

    # Use dashboard benefits if available
    if slug in DASHBOARD_BENEFITS:
        benefit_text = DASHBOARD_BENEFITS[slug]['highlight']
    else:
        # For mobile features, extract first benefit
        benefit_text = extract_first_benefit(content)
        if not benefit_text:
            return content  # Keep original if we can't extract

    # Replace Feature Highlight content
    pattern = r'(<div class="feature-highlight-content">.*?<h3>[^<]+</h3>\s*<p>)(.*?)(</p>\s*</div>)'

    def replace_content(match):
        return match.group(1) + benefit_text + match.group(3)

    return re.sub(pattern, replace_content, content, flags=re.DOTALL)


def shorten_cta_section(content: str, slug: str) -> str:
    """Shorten CTA to simple question"""

    # Use dashboard CTA if available
    if slug in DASHBOARD_BENEFITS:
        cta_text = DASHBOARD_BENEFITS[slug]['cta']
    else:
        # For mobile features, extract question from content
        # Try to find a benefit-focused question
        match = re.search(
            r'<h2 class="section-title"[^>]*>Why Choose[^?]*\?</h2>.*?'
            r'<div class="why-choose-section"[^>]*>.*?<p>([^<]*\?)',
            content,
            re.DOTALL
        )
        if match:
            cta_text = match.group(1).strip()
        else:
            # Fallback
            cta_text = "Ready to get started?"

    # Replace CTA content - remove all the promotional text
    pattern = r'(<section class="cta-section-bottom".*?<h2>[^<]+</h2>\s*<p>)(.*?)(</p>\s*<a)'

    def replace_cta(match):
        return match.group(1) + cta_text + match.group(3)

    return re.sub(pattern, replace_cta, content, flags=re.DOTALL)


def process_all_features():
    """Process all feature pages"""
    feature_dir = Path("feature")
    processed = 0
    mobile_count = 0
    dashboard_count = 0

    dashboard_features = {
        'compliance-engine', 'driver-management', 'fuel-tracking', 'import-hub',
        'leave-management', 'operational-dashboard', 'org-settings-permissions',
        'rota-scheduling'
    }

    for html_file in sorted(feature_dir.glob("*.html")):
        if html_file.name in ["feature-template.html", "INDEX-COMPLETE.html"]:
            continue

        slug = html_file.stem
        is_dashboard = slug in dashboard_features

        with open(html_file, "r", encoding="utf-8") as f:
            original_content = f.read()

        new_content = original_content

        # Shorten Feature Highlight
        new_content = shorten_feature_highlight(new_content, slug)

        # Shorten CTA
        new_content = shorten_cta_section(new_content, slug)

        if new_content != original_content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            processed += 1
            if is_dashboard:
                dashboard_count += 1
            else:
                mobile_count += 1
            print(f"[+] {html_file.name}: Updated Feature Highlight and CTA")

    return processed, mobile_count, dashboard_count


def main():
    """Main function"""
    print("[*] Shortening all Feature Highlight and Final CTA sections...\n")

    processed, mobile, dashboard = process_all_features()

    print(f"\n[+] Processed {processed} feature pages")
    print(f"    - Mobile app features: {mobile}")
    print(f"    - Dashboard features: {dashboard}")
    print("[+] Complete!")


if __name__ == "__main__":
    main()
