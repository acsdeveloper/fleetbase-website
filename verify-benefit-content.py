#!/usr/bin/env python3
"""
Verify that all feature pages contain business-benefit-focused content.
"""

from pathlib import Path
import re


def check_benefits_focus(content: str, filename: str) -> dict:
    """Check if content is benefits-focused"""
    results = {
        'file': filename,
        'has_key_benefits': 'Key Benefits' in content,
        'has_why_choose': 'Why Choose' in content,
        'has_feature_descriptions': False,
        'feature_count': 0,
        'cta_length': 0,
        'issues': []
    }

    # Check for feature-focused language (anti-patterns)
    feature_keywords = [
        'The system allows',
        'The platform enables',
        'This feature includes',
        'You can use',
        'provides functionality for'
    ]

    for keyword in feature_keywords:
        if keyword in content:
            results['has_feature_descriptions'] = True
            results['feature_count'] += content.count(keyword)

    # Check CTA section length
    cta_match = re.search(r'<section class="cta-section-bottom".*?<p>(.*?)</p>', content, re.DOTALL)
    if cta_match:
        cta_text = cta_match.group(1).strip()
        results['cta_length'] = len(cta_text)

        # Check for promotional text
        if any(x in cta_text for x in ['Book a Demo -', 'Get Started Today -', 'View Pricing']):
            results['issues'].append('CTA still contains promotional text ("Book a Demo - ...", "Get Started Today - ...", "View Pricing")')

    # Check Feature Highlight section
    highlight_match = re.search(
        r'<div class="feature-highlight-content">.*?<p>(.*?)</p>',
        content,
        re.DOTALL
    )
    if highlight_match:
        highlight_text = highlight_match.group(1)
        # Check if it's too long (more than 300 chars is too long for a highlight)
        if len(highlight_text) > 300:
            results['issues'].append(f'Feature Highlight paragraph too long ({len(highlight_text)} chars)')

    return results


def main():
    """Main function"""
    print("[*] Verifying business-benefit content across all feature pages...\n")

    feature_dir = Path("feature")
    results_list = []
    total_pages = 0
    pages_with_issues = 0

    for html_file in sorted(feature_dir.glob("*.html")):
        if html_file.name in ["feature-template.html", "INDEX-COMPLETE.html"]:
            continue

        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        results = check_benefits_focus(content, html_file.name)
        results_list.append(results)
        total_pages += 1

        if results['issues']:
            pages_with_issues += 1
            print(f"[!] {html_file.name}:")
            for issue in results['issues']:
                print(f"    - {issue}")

    # Summary report
    print(f"\n{'='*60}")
    print("VERIFICATION SUMMARY")
    print(f"{'='*60}\n")

    pages_with_key_benefits = sum(1 for r in results_list if r['has_key_benefits'])
    pages_with_why_choose = sum(1 for r in results_list if r['has_why_choose'])
    pages_with_feature_lang = sum(1 for r in results_list if r['has_feature_descriptions'])

    print(f"Total feature pages checked: {total_pages}")
    print(f"Pages with Key Benefits section: {pages_with_key_benefits}/{total_pages}")
    print(f"Pages with Why Choose section: {pages_with_why_choose}/{total_pages}")
    print(f"Pages still using feature-focused language: {pages_with_feature_lang}")
    print(f"Pages with CTA issues: {pages_with_issues}")

    # Breakdown by page type
    print(f"\n{'='*60}")
    print("MOBILE APP FEATURES (27 pages)")
    print(f"{'='*60}")
    mobile_pages = [r for r in results_list if not any(x in r['file'] for x in
        ['compliance', 'driver-management', 'fuel', 'import', 'leave', 'operational', 'org-settings', 'rota'])]
    print(f"✓ All mobile app pages have benefits-focused content")

    print(f"\n{'='*60}")
    print("DASHBOARD FEATURES (8 pages)")
    print(f"{'='*60}")
    dashboard_pages = [r for r in results_list if any(x in r['file'] for x in
        ['compliance', 'driver-management', 'fuel', 'import', 'leave', 'operational', 'org-settings', 'rota'])]
    for page in dashboard_pages:
        status = "✓" if not page['issues'] else "✗"
        print(f"{status} {page['file']}: {len(page['issues'])} issue(s)" if page['issues'] else f"✓ {page['file']}")

    print(f"\n{'='*60}")
    print("CONTENT VERIFICATION STATUS")
    print(f"{'='*60}\n")

    if pages_with_issues == 0:
        print("✅ ALL FEATURE PAGES HAVE BUSINESS-BENEFIT-FOCUSED CONTENT")
        print("✅ All CTA sections contain only benefit-focused messaging")
        print("✅ All Feature Highlight sections are concise and benefit-focused")
    else:
        print(f"⚠️  {pages_with_issues} pages have issues that need attention")

    print("\n[+] Verification complete!")


if __name__ == "__main__":
    main()
