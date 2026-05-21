#!/usr/bin/env python3
"""
Truncate Feature Highlight and Final CTA content in dashboard features.
- Feature Highlight: Keep only first 1-2 sentences (max 200 chars)
- Final CTA: Keep only the main question/statement, remove promotional text
"""

from pathlib import Path
import re


def truncate_feature_highlight(content: str) -> str:
    """Truncate Feature Highlight paragraph to first 1-2 sentences"""
    # Find the feature-highlight-content section with the <p> tag
    pattern = r'(<div class="feature-highlight-content">.*?<h3>[^<]+</h3>\s*<p>)(.*?)(</p>\s*</div>)'

    def replace_highlight(match):
        prefix = match.group(1)
        paragraph = match.group(2)
        suffix = match.group(3)

        # Get first sentence(s) up to ~200 characters
        # Split by periods
        sentences = re.split(r'(?<=[.!?])\s+', paragraph)

        truncated = ""
        for sentence in sentences:
            if len(truncated) == 0:
                truncated = sentence.strip()
            elif len(truncated) + len(sentence) < 200:
                truncated += " " + sentence.strip()
            else:
                break

        # Ensure it ends with a period
        if truncated and not truncated.endswith(('!', '?', '.')):
            truncated += '.'

        # Remove em dashes
        truncated = truncated.replace('—', '-')

        return prefix + truncated + suffix

    return re.sub(pattern, replace_highlight, content, flags=re.DOTALL)


def truncate_cta_section(content: str) -> str:
    """Truncate Final CTA paragraph"""
    # Find the cta-section-bottom section
    pattern = r'(<section class="cta-section-bottom".*?<h2>[^<]+</h2>\s*<p>)(.*?)(</p>\s*<a)'

    def replace_cta(match):
        prefix = match.group(1)
        paragraph = match.group(2)
        suffix = match.group(3)

        # Clean the paragraph: remove extra newlines and markdown
        paragraph = paragraph.replace('**', '').replace('***', '')
        lines = [line.strip() for line in paragraph.split('\n') if line.strip()]

        # Keep only the first line (the question/statement)
        # Remove everything after the first non-empty line if it contains "Book", "Get Started", "View Pricing"
        main_text = lines[0] if lines else ""

        # Remove any "Book a Demo", "Get Started Today", "View Pricing" lines
        main_text = re.sub(r'—.*?(?=\.|$)', '', main_text)  # Remove em-dash sections
        main_text = main_text.replace('—', '-').strip()

        if not main_text.endswith(('?', '!', '.')):
            if main_text:
                main_text += '?'

        return prefix + main_text + suffix

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

        # Truncate feature highlight
        new_content = truncate_feature_highlight(new_content)

        # Truncate CTA section
        new_content = truncate_cta_section(new_content)

        if new_content != original_content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            processed += 1
            print(f"[+] {html_file.name}: Truncated Feature Highlight and CTA content")

    return processed


def main():
    """Main function"""
    print("[*] Truncating Feature Highlight and Final CTA content...\n")

    processed = process_dashboard_features()

    print(f"\n[+] Processed {processed} dashboard feature pages")
    print("[+] Complete!")


if __name__ == "__main__":
    main()
