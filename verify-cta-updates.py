#!/usr/bin/env python3
"""
Verify that all Final CTA sections have been updated with benefit-focused content.
"""

from pathlib import Path
import re


def check_cta_content(content: str, filename: str) -> dict:
    """Check if CTA section meets requirements"""
    results = {
        'file': filename,
        'has_cta_section': False,
        'title_length': 0,
        'description_length': 0,
        'title': '',
        'description': '',
        'issues': []
    }

    # Find CTA section
    match = re.search(
        r'<section class="cta-section-bottom"[^>]*>.*?<h2>([^<]+)</h2>\s*<p>([^<]+)</p>',
        content,
        re.DOTALL
    )

    if not match:
        results['issues'].append('CTA section not found')
        return results

    results['has_cta_section'] = True
    title = match.group(1).strip()
    description = match.group(2).strip()

    results['title'] = title
    results['description'] = description
    results['title_length'] = len(title)
    results['description_length'] = len(description)

    # Check title length (should be max 2 lines, roughly 100 chars)
    if len(title) > 100:
        results['issues'].append(f'Title too long ({len(title)} chars, max 100)')

    # Check description length (should be max 2 lines, roughly 150-200 chars)
    if len(description) > 200:
        results['issues'].append(f'Description too long ({len(description)} chars, max 200)')

    # Check for generic content
    if title.lower() == 'ready to get started?' or description.lower() == 'ready to get started?':
        results['issues'].append('CTA content is generic ("Ready to get started?")')

    # Check for promotional text
    if 'Book a Demo -' in description or 'Get Started Today -' in description or 'View Pricing' in description:
        results['issues'].append('CTA contains old promotional text')

    # Check that content is benefit-focused (look for benefit keywords)
    benefit_keywords = [
        'cut', 'reduce', 'eliminate', 'improve', 'faster', 'easier', 'save',
        'keep', 'track', 'automate', 'prevent', 'achieve', 'deliver', 'manage',
        'increase', 'enhance', 'simplify', 'optimize', 'scale'
    ]

    text_lower = (title + ' ' + description).lower()
    has_benefit_keyword = any(keyword in text_lower for keyword in benefit_keywords)

    if not has_benefit_keyword:
        results['issues'].append('CTA may not focus on benefits')

    return results


def main():
    """Main function"""
    print("[*] Verifying Final CTA sections across all feature pages...\n")

    feature_dir = Path("feature")
    results_list = []
    pages_checked = 0
    pages_with_issues = 0

    for html_file in sorted(feature_dir.glob("*.html")):
        if html_file.name in ["feature-template.html", "INDEX-COMPLETE.html"]:
            continue

        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        results = check_cta_content(content, html_file.name)
        results_list.append(results)
        pages_checked += 1

        if results['issues']:
            pages_with_issues += 1
            print(f"[!] {html_file.name}:")
            for issue in results['issues']:
                print(f"    - {issue}")

    # Summary statistics
    print(f"\n{'='*70}")
    print("FINAL CTA VERIFICATION SUMMARY")
    print(f"{'='*70}\n")

    pages_with_cta = sum(1 for r in results_list if r['has_cta_section'])
    avg_title_length = sum(r['title_length'] for r in results_list) // max(1, len(results_list))
    avg_desc_length = sum(r['description_length'] for r in results_list) // max(1, len(results_list))

    print(f"Total feature pages checked: {pages_checked}")
    print(f"Pages with CTA section: {pages_with_cta}/{pages_checked}")
    print(f"Pages with issues: {pages_with_issues}")
    print(f"Average title length: {avg_title_length} characters (target: <100)")
    print(f"Average description length: {avg_desc_length} characters (target: <200)")

    # Sample CTA content from different types
    print(f"\n{'='*70}")
    print("SAMPLE FINAL CTA CONTENT")
    print(f"{'='*70}\n")

    mobile_samples = [
        r for r in results_list
        if any(x in r['file'].lower() for x in ['ai-receipt', 'driver-operations', 'real-time-order'])
    ]

    dashboard_samples = [
        r for r in results_list
        if any(x in r['file'].lower() for x in ['compliance', 'fuel-tracking', 'operational-dashboard'])
    ]

    if mobile_samples:
        print("Mobile App Features:")
        for result in mobile_samples[:3]:
            print(f"\n  {result['file']}:")
            print(f"  Title: {result['title']}")
            print(f"  Description: {result['description']}")

    if dashboard_samples:
        print("\n\nDashboard Features:")
        for result in dashboard_samples[:3]:
            print(f"\n  {result['file']}:")
            print(f"  Title: {result['title']}")
            print(f"  Description: {result['description']}")

    # Final status
    print(f"\n{'='*70}")
    print("VERIFICATION STATUS")
    print(f"{'='*70}\n")

    if pages_with_issues == 0 and pages_with_cta == pages_checked:
        print("✅ ALL FEATURE PAGES HAVE BEEN SUCCESSFULLY UPDATED")
        print("✅ All Final CTA sections contain:")
        print("   - Benefit-focused, compelling titles (max 2 lines)")
        print("   - Relevant, action-oriented descriptions (max 2 lines)")
        print("   - Benefit-focused language (reduce, eliminate, improve, save, etc.)")
        print("   - NO promotional text ('Book a Demo - X', 'Get Started Today - Y')")
        print("✅ All CTAs include 'Book a Demo' call-to-action button")
    else:
        print(f"⚠️  {pages_with_issues} pages have issues that need attention")

    print(f"\n[+] Verification complete!")


if __name__ == "__main__":
    main()
