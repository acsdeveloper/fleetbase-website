#!/usr/bin/env python3
"""
Rewrite Feature Highlight and Final CTA content in dashboard features.
Convert from feature-focused to business-benefit-focused language.
"""

from pathlib import Path
import re


# Benefit-focused rewrites for each dashboard feature
BENEFIT_REWRITES = {
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


def rewrite_feature_highlight(content: str, slug: str) -> str:
    """Rewrite Feature Highlight section with business benefits"""
    if slug not in BENEFIT_REWRITES:
        return content

    benefit_text = BENEFIT_REWRITES[slug]['highlight']

    # Find and replace the feature-highlight-content paragraph
    pattern = r'(<div class="feature-highlight-content">.*?<h3>[^<]+</h3>\s*<p>)(.*?)(</p>\s*</div>)'

    def replace_content(match):
        prefix = match.group(1)
        suffix = match.group(3)
        return prefix + benefit_text + suffix

    return re.sub(pattern, replace_content, content, flags=re.DOTALL)


def rewrite_cta_section(content: str, slug: str) -> str:
    """Rewrite Final CTA section with business benefits"""
    if slug not in BENEFIT_REWRITES:
        return content

    benefit_cta = BENEFIT_REWRITES[slug]['cta']

    # Find and replace the cta-section-bottom paragraph
    pattern = r'(<section class="cta-section-bottom".*?<h2>[^<]+</h2>\s*<p>)(.*?)(</p>\s*<a)'

    def replace_cta(match):
        prefix = match.group(1)
        suffix = match.group(3)
        return prefix + benefit_cta + suffix

    return re.sub(pattern, replace_cta, content, flags=re.DOTALL)


def process_dashboard_features():
    """Process all dashboard feature HTML pages"""
    feature_dir = Path("feature")
    processed = 0

    # Dashboard features (generated from .mdx files)
    dashboard_features = {
        'compliance-engine', 'driver-management', 'fuel-tracking', 'import-hub',
        'leave-management', 'operational-dashboard', 'org-settings-permissions',
        'rota-scheduling'
    }

    for html_file in sorted(feature_dir.glob("*.html")):
        slug = html_file.stem

        if slug not in dashboard_features:
            continue

        with open(html_file, "r", encoding="utf-8") as f:
            original_content = f.read()

        new_content = original_content

        # Rewrite feature highlight
        new_content = rewrite_feature_highlight(new_content, slug)

        # Rewrite CTA section
        new_content = rewrite_cta_section(new_content, slug)

        if new_content != original_content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            processed += 1
            print(f"[+] {html_file.name}: Rewrote Feature Highlight and CTA to business benefits")

    return processed


def main():
    """Main function"""
    print("[*] Rewriting Feature Highlight and Final CTA content to business benefits...\n")

    processed = process_dashboard_features()

    print(f"\n[+] Processed {processed} dashboard feature pages")
    print("[+] All content converted to business-benefit-focused messaging")
    print("[+] Complete!")


if __name__ == "__main__":
    main()
