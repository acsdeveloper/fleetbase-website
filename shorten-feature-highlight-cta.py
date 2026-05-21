#!/usr/bin/env python3
"""
Shorten Feature Highlight and Final CTA content in feature pages.
- Feature Highlight: Use first 1-2 sentences only
- Final CTA: Remove promotional text, keep only call-to-action
"""

from pathlib import Path
import re


def shorten_feature_highlight(content: str) -> str:
    """Shorten Feature Highlight paragraph to first 1-2 sentences"""
    # Find the feature-highlight-content section
    pattern = r'(<div class="feature-highlight-content">.*?<h3>[^<]+</h3>\s*<p>)(.*?)(</p>\s*</div>)'

    def replace_highlight(match):
        prefix = match.group(1)
        paragraph = match.group(2)
        suffix = match.group(3)

        # Split into sentences and keep first 1-2
        # Find first period followed by space
        sentences = []
        current_sentence = ""

        for char in paragraph:
            current_sentence += char
            if char == '.' and current_sentence.endswith('. '):
                sentences.append(current_sentence.strip())
                current_sentence = ""

        if current_sentence.strip():
            sentences.append(current_sentence.strip())

        # Keep first sentence or first two short sentences
        shortened = ""
        if sentences:
            shortened = sentences[0]
            # If first sentence is short, add second
            if len(sentences) > 1 and len(shortened) < 150:
                shortened += " " + sentences[1]

        # Clean up extra spaces
        shortened = shortened.replace('—', '-').strip()

        return prefix + shortened + suffix

    content = re.sub(pattern, replace_highlight, content, flags=re.DOTALL)
    return content


def shorten_cta_section(content: str) -> str:
    """Shorten Final CTA paragraph to simple call-to-action"""
    # Find the cta-section-bottom section
    pattern = r'(<section class="cta-section-bottom".*?<h2>[^<]+</h2>\s*<p>)(.*?)(</p>\s*<a)'

    def replace_cta(match):
        prefix = match.group(1)
        paragraph = match.group(2)
        suffix = match.group(3)

        # Extract just the main question/statement, remove all the "Book a Demo", "Get Started", "View Pricing" text
        # Keep only the first sentence up to the first dash or newline
        lines = paragraph.split('\n')
        main_line = lines[0].strip() if lines else paragraph.strip()

        # Remove markdown formatting if present
        main_line = main_line.replace('**', '').replace('***', '')

        # If it starts with a question or statement, keep it
        if main_line:
            # Clean extra spaces and dashes
            main_line = main_line.replace('—', '-')
            return prefix + main_line + suffix

        # Fallback
        return match.group(0)

    content = re.sub(pattern, replace_cta, content, flags=re.DOTALL)
    return content


def process_feature_pages():
    """Process all feature HTML pages"""
    feature_dir = Path("feature")
    processed = 0
    shortened_highlights = 0
    shortened_ctas = 0

    # Dashboard features to process (those with .mdx sources)
    dashboard_features = {
        'compliance-engine', 'driver-management', 'fuel-tracking', 'import-hub',
        'leave-management', 'operational-dashboard', 'org-settings-permissions',
        'rota-scheduling'
    }

    for html_file in sorted(feature_dir.glob("*.html")):
        if html_file.name in ["feature-template.html", "INDEX-COMPLETE.html"]:
            continue

        # Check if this is a dashboard feature
        slug = html_file.stem
        if slug not in dashboard_features:
            continue

        with open(html_file, "r", encoding="utf-8") as f:
            original_content = f.read()

        new_content = original_content

        # Shorten feature highlight
        if 'feature-highlight-content' in new_content:
            new_content = shorten_feature_highlight(new_content)
            if new_content != original_content:
                shortened_highlights += 1

        # Shorten CTA section
        original_for_cta = new_content
        if 'cta-section-bottom' in new_content:
            new_content = shorten_cta_section(new_content)
            if new_content != original_for_cta:
                shortened_ctas += 1

        if new_content != original_content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            processed += 1
            print(f"[+] {html_file.name}: Shortened Feature Highlight and CTA sections")

    return processed, shortened_highlights, shortened_ctas


def main():
    """Main function"""
    print("[*] Shortening Feature Highlight and Final CTA content in dashboard features...\n")

    processed, highlights, ctas = process_feature_pages()

    print(f"\n[+] Processed {processed} feature pages")
    print(f"[+] Shortened {highlights} Feature Highlight sections")
    print(f"[+] Shortened {ctas} Final CTA sections")
    print("[+] Complete!")


if __name__ == "__main__":
    main()
