#!/usr/bin/env python3
"""
Generate feature marketing pages from .md and .mdx feature files.

This script parses dashboard and mobile app feature files (.md and .mdx) and
generates HTML marketing pages using your feature-template.html with:
- Automatic placeholder filling
- Support for both markdown and MDX formats
- Feature discovery from features-md/*/features/ directories
- Template-based HTML generation

Usage:
    python generate-feature-pages.py [--dashboard] [--mobile] [--all] [--clean]
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Feature:
    """Represents a single feature"""
    title: str
    description: str
    filepath: Path
    platform: str = "both"
    benefits: List[str] = None
    capabilities: List[str] = None
    use_cases: List[str] = None
    integrations: List[str] = None
    steps: List[Tuple[str, str]] = None
    raw_content: str = ""

    def __post_init__(self):
        if self.benefits is None:
            self.benefits = []
        if self.capabilities is None:
            self.capabilities = []
        if self.use_cases is None:
            self.use_cases = []
        if self.integrations is None:
            self.integrations = []
        if self.steps is None:
            self.steps = []

    def slug(self) -> str:
        """Convert feature name to URL slug"""
        slug = self.filepath.stem
        # Extract feature number prefix if exists (e.g., '01-real-time-order-management' -> 'real-time-order-management')
        if re.match(r'^\d+-', slug):
            slug = re.sub(r'^\d+-', '', slug)
        return slug

    def keywords(self) -> str:
        """Generate SEO keywords"""
        keywords = [self.title, "FleetYes", "fleet management"]
        if self.platform in ["dashboard", "both"]:
            keywords.append("fleet operations dashboard")
        if self.platform in ["mobile", "both"]:
            keywords.append("driver mobile app")
        keywords.extend(self.benefits[:3])
        return ", ".join(keywords)


class FeatureAnalyzer:
    """Parse .md and .mdx feature files from features-md/*/features/ directories"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.features: List[Feature] = []

    def parse_frontmatter(self, content: str) -> Tuple[dict, str]:
        """Extract YAML frontmatter and content (simple parser, no yaml lib)"""
        match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if match:
            frontmatter_text = match.group(1)
            body = match.group(2)

            # Simple YAML parser
            frontmatter = {}
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    frontmatter[key] = value

            return frontmatter, body
        return {}, content

    def extract_first_paragraph(self, content: str) -> str:
        """Extract first substantive paragraph from markdown content"""
        # Skip title and dividers
        lines = content.split('\n')
        para_lines = []

        for line in lines:
            # Skip empty lines and headers
            if not line.strip() or line.startswith('#') or line.startswith('---'):
                continue
            # Stop at first section
            if line.startswith('## '):
                break
            para_lines.append(line.strip())

        if para_lines:
            text = ' '.join(para_lines)
            # Clean up markdown formatting
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            text = re.sub(r'\*(.*?)\*', r'\1', text)
            return text[:200].strip()
        return ""

    def extract_subtitle(self, content: str) -> str:
        """Extract a short subtitle (max 2 lines) from the first meaningful content"""
        lines = content.split('\n')
        subtitle_lines = []

        # Keywords that indicate section headers (not subtitles)
        section_keywords = {
            'Key Benefits', 'How It Works', 'Core Capabilities', 'Use Cases',
            'Integration', 'Why Choose', 'Visual Overview', 'Getting Started',
            'Features', 'Overview', 'Capabilities'
        }

        for i, line in enumerate(lines):
            # Skip title line (first line), empty lines, and dividers
            if i == 0 or not line.strip() or line.startswith('---'):
                continue
            # Check for actual subtitle headers (## format), but skip section headers
            if line.startswith('## '):
                header_text = line.replace('## ', '').strip()
                # Only use as subtitle if it's not a section header
                if not any(keyword in header_text for keyword in section_keywords):
                    return header_text
            # Collect substantive text (non-headers) for first 2 lines max
            if line.strip() and not line.startswith('#'):
                subtitle_lines.append(line.strip())
                if len(subtitle_lines) >= 2:
                    break

        if subtitle_lines:
            text = ' '.join(subtitle_lines)
            # Clean markdown formatting
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            text = re.sub(r'\*(.*?)\*', r'\1', text)
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # Remove links
            # Truncate to ~150 chars max
            if len(text) > 150:
                text = text[:150].rsplit(' ', 1)[0] + '...'
            return text.strip()
        return ""

    def extract_paragraph_section(self, content: str, section_title: str) -> str:
        """Extract full paragraph content from a section"""
        pattern = rf'## {section_title}\n(.*?)(?=\n## |\n---|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            text = match.group(1).strip()
            # Clean up markdown formatting
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            text = re.sub(r'\*(.*?)\*', r'\1', text)
            return text
        return ""

    def extract_sections(self, content: str) -> dict:
        """Extract structured sections from markdown content"""
        sections = {}

        # Extract Key Benefits - handles "- **Title**\nDescription" format with multiline descriptions
        benefits_match = re.search(r'## Key Benefits\n(.*?)(?=\n## |\n---|\Z)', content, re.DOTALL)
        if benefits_match:
            benefits_text = benefits_match.group(1)
            # Find all "- **Title**" patterns and their descriptions
            benefits_list = []
            pattern = r'- \*\*(.*?)\*\*\s*(.*?)(?=\n- \*\*|\Z)'
            for match in re.finditer(pattern, benefits_text, re.DOTALL):
                title = match.group(1).strip()
                description = match.group(2).strip()
                # Clean up description - remove extra whitespace
                description = ' '.join(description.split())
                # Truncate at sentence boundary (max 200 chars, but try to end at a period)
                if len(description) > 200:
                    # Find last period within 200 chars
                    truncated = description[:200]
                    last_period = truncated.rfind('.')
                    if last_period > 100:
                        description = truncated[:last_period + 1]
                    else:
                        description = truncated + '...'
                benefits_list.append((title, description))
            sections['benefits'] = benefits_list[:8]

        # Extract How It Works - handles both formats:
        # Dashboard: "1. **Title**" and "1. **Title** — Description"
        # Mobile: "**1. Title**" with description on next line
        how_match = re.search(r'## How It Works\n(.*?)(?=\n## |\n---|\Z)', content, re.DOTALL)
        if how_match:
            how_text = how_match.group(1)
            steps = []

            # Try to split by "**\d+." format first (mobile app)
            items = re.split(r'\n(?=\*\*\d+\.)', how_text.strip())
            if len(items) < 2:
                # Try to split by "\d+." format (dashboard)
                items = re.split(r'\n(?=\d+\.)', how_text.strip())

            for item in items:
                # Try both formats for title extraction
                # Format 1: "**1. Title**"
                title_match = re.search(r'\*\*\d+\.\s+(.*?)\*\*', item)
                if not title_match:
                    # Format 2: "1. **Title**"
                    title_match = re.search(r'\d+\.\s+\*\*(.*?)\*\*', item)

                if title_match:
                    title = title_match.group(1).strip()
                    # Extract description after title
                    desc_part = item[title_match.end():]
                    # Remove leading dashes/em-dashes
                    desc_part = re.sub(r'^[\s—\-]+', '', desc_part).strip()
                    # Get first line or first 200 chars
                    description = desc_part.split('\n')[0][:200]
                    if description:
                        steps.append((title, description))

            sections['steps'] = steps[:4]

        # Extract Core Capabilities - get just titles (no descriptions for cleaner display)
        caps_match = re.search(r'## Core Capabilities\n(.*?)(?=\n## |\n---|\Z)', content, re.DOTALL)
        if caps_match:
            caps_text = caps_match.group(1)
            caps = []

            # Find all "- **Title**" patterns
            pattern = r'- \*\*(.*?)\*\*'
            matches = re.findall(pattern, caps_text)
            if matches:
                caps = matches
            else:
                # If no bold format found, try plain format
                caps = re.findall(r'-\s+([^\n]+)', caps_text)

            sections['capabilities'] = [c.strip() for c in caps if c.strip()][:8]

        # Extract Use Cases - handles both bold and plain formats with descriptions
        cases_match = re.search(r'## Use Cases\n(.*?)(?=\n## |\n---|\Z)', content, re.DOTALL)
        if cases_match:
            cases_text = cases_match.group(1)
            cases_list = []

            # Try to find bold titles with descriptions first
            pattern = r'- \*\*(.*?)\*\*\s*(.*?)(?=\n- \*\*|\n- [^*]|\Z)'
            matches = re.finditer(pattern, cases_text, re.DOTALL)
            for match in matches:
                title = match.group(1).strip()
                description = match.group(2).strip()
                description = ' '.join(description.split())
                cases_list.append((title, description[:150]))

            # If no bold format found, try plain format
            if not cases_list:
                cases = re.findall(r'-\s+([^\n]+)', cases_text)
                cases_list = [(c.strip(), "") for c in cases if c.strip()]

            sections['use_cases'] = cases_list[:8]

        # Extract Integrations & Compatibility - handles both bold and plain formats with descriptions
        integ_match = re.search(r'## Integration & Compatibility\n(.*?)(?=\n## |\n---|\Z)', content, re.DOTALL)
        if integ_match:
            integ_text = integ_match.group(1)
            integs_list = []

            # Try to find bold titles with descriptions first
            pattern = r'- \*\*(.*?)\*\*\s*(.*?)(?=\n- \*\*|\n- [^*]|\Z)'
            matches = re.finditer(pattern, integ_text, re.DOTALL)
            for match in matches:
                title = match.group(1).strip()
                description = match.group(2).strip()
                description = ' '.join(description.split())
                integs_list.append((title, description[:150]))

            # If no bold format found, try plain format
            if not integs_list:
                integs = re.findall(r'-\s+([^\n]+)', integ_text)
                integs_list = [(i.strip(), "") for i in integs if i.strip()]

            sections['integrations'] = integs_list[:8]

        return sections

    def clean_title(self, title: str) -> str:
        """Remove numbered prefix from title (e.g., '00 Driver Operations' -> 'Driver Operations')"""
        # Handle both "00-" and "00 " prefixes
        title = re.sub(r'^\d+[\s\-]+', '', title)
        return title.strip()

    def split_paragraphs(self, text: str, max_paragraphs: int = 3) -> List[str]:
        """Split text into separate paragraphs by newlines or paragraph breaks"""
        if not text:
            return [""] * max_paragraphs

        # Split by double newlines first (true paragraph breaks)
        paragraphs = re.split(r'\n\n+', text.strip())

        # If not enough paragraphs, try to split sentences for additional paragraphs
        if len(paragraphs) < max_paragraphs:
            # Join what we have and try splitting by period-space
            combined = ' '.join(paragraphs)
            sentences = re.split(r'(?<=[.!?])\s+', combined)

            # Group sentences into roughly equal paragraphs
            if len(sentences) >= max_paragraphs:
                sents_per_para = len(sentences) // max_paragraphs
                paragraphs = []
                for i in range(max_paragraphs - 1):
                    start = i * sents_per_para
                    end = (i + 1) * sents_per_para
                    paragraphs.append(' '.join(sentences[start:end]))
                # Last paragraph gets remaining sentences
                paragraphs.append(' '.join(sentences[(max_paragraphs - 1) * sents_per_para:]))
            else:
                paragraphs = sentences

        # Ensure we have exactly max_paragraphs items
        while len(paragraphs) < max_paragraphs:
            paragraphs.append("")

        return paragraphs[:max_paragraphs]

    def parse_feature_file(self, filepath: Path, platform: str) -> Optional[Feature]:
        """Parse a single .md or .mdx feature file"""
        if not filepath.exists():
            return None

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract frontmatter
        frontmatter, body = self.parse_frontmatter(content)

        # Get title - prefer frontmatter, fallback to filename
        title = frontmatter.get('title', filepath.stem.replace('-', ' ').title())
        # Clean title of numbered prefixes
        title = self.clean_title(title)

        # Get description - try frontmatter first, then extract first paragraph
        description = frontmatter.get('description', '')
        if not description:
            description = self.extract_first_paragraph(body)

        # Extract short subtitle for hero section (max 2 lines)
        # Prefer frontmatter description for dashboard features, otherwise extract from content
        short_subtitle = frontmatter.get('description', '') or self.extract_subtitle(body)
        # If still empty, use first paragraph
        if not short_subtitle:
            short_subtitle = self.extract_first_paragraph(body)

        # Extract sections
        sections = self.extract_sections(body)

        # Extract full text sections
        visual_overview = self.extract_paragraph_section(body, "Visual Overview")
        why_choose_full = self.extract_paragraph_section(body, "Why Choose This Feature")
        getting_started = self.extract_paragraph_section(body, "Getting Started")

        # Create feature - extract titles and descriptions from tuples
        benefits_data = sections.get('benefits', [])
        benefits_titles = [b[0] if isinstance(b, tuple) else b for b in benefits_data]
        benefits_descs = [b[1] if isinstance(b, tuple) else "" for b in benefits_data]

        use_cases_data = sections.get('use_cases', [])
        use_cases_titles = [c[0] if isinstance(c, tuple) else c for c in use_cases_data]
        use_cases_descs = [c[1] if isinstance(c, tuple) else "" for c in use_cases_data]

        integrations_data = sections.get('integrations', [])
        integrations_titles = [i[0] if isinstance(i, tuple) else i for i in integrations_data]
        integrations_descs = [i[1] if isinstance(i, tuple) else "" for i in integrations_data]

        # Store in a way that we can access both title and description later
        feature = Feature(
            title=title,
            description=description,
            filepath=filepath,
            platform=platform,
            benefits=benefits_titles,
            capabilities=sections.get('capabilities', []),
            use_cases=use_cases_titles,
            integrations=integrations_titles,
            steps=sections.get('steps', []),
            raw_content=content
        )

        # Store additional descriptions as attributes
        feature.benefits_descriptions = benefits_descs
        feature.use_cases_descriptions = use_cases_descs
        feature.integrations_descriptions = integrations_descs
        feature.visual_overview = visual_overview
        feature.getting_started = getting_started
        feature.short_subtitle = short_subtitle

        # Split Why Choose into three paragraphs
        why_choose_paragraphs = self.split_paragraphs(why_choose_full, 3)
        feature.why_choose_paragraph_1 = why_choose_paragraphs[0]
        feature.why_choose_paragraph_2 = why_choose_paragraphs[1]
        feature.why_choose_paragraph_3 = why_choose_paragraphs[2]

        return feature

    def discover_features(self, platform: str) -> List[Feature]:
        """Discover all feature files for a platform"""
        features_dir = self.project_root / "features-md" / platform / "features"
        features = []

        if not features_dir.exists():
            return features

        # Find all .md and .mdx files
        for pattern in ['*.md', '*.mdx']:
            for filepath in sorted(features_dir.glob(pattern)):
                if filepath.name in ['INDEX.md', 'README.md']:
                    continue

                feature = self.parse_feature_file(filepath, platform)
                if feature:
                    features.append(feature)

        return features

    def get_all_features(self) -> List[Feature]:
        """Get all features from both platforms"""
        features = []

        # Add dashboard features
        features.extend(self.discover_features("dashboard"))

        # Add mobile features
        features.extend(self.discover_features("mobileapp"))

        return features


class HTMLGenerator:
    """Generate HTML feature pages"""

    TEMPLATE_FILE = None  # Will be loaded from feature-template.html

    def __init__(self, output_dir: str = None, template_file: str = None):
        self.output_dir = Path(output_dir or "./feature")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load template from file
        if template_file and Path(template_file).exists():
            with open(template_file, "r", encoding="utf-8") as f:
                self.html_template = f.read()
        else:
            # Try to find feature-template.html in feature directory
            default_template = self.output_dir / "feature-template.html"
            if default_template.exists():
                with open(default_template, "r", encoding="utf-8") as f:
                    self.html_template = f.read()
            else:
                print("[!] Warning: feature-template.html not found. Using default template.")
                self.html_template = self.get_default_template()

    @staticmethod
    def get_default_template():
        """Fallback template if feature-template.html not found"""
        return """<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8" />
  <meta content="width=device-width, initial-scale=1.0" name="viewport" />
  <title>{{FEATURE_TITLE}} - FleetYes</title>
  <meta name="description" content="{{FEATURE_DESCRIPTION}}" />
  <meta name="keywords" content="{{FEATURE_KEYWORDS}}" />
</head>
<body>
  <h1>{{FEATURE_TITLE}}</h1>
  <p>{{FEATURE_SHORT_DESCRIPTION}}</p>
</body>
</html>"""

    def generate_page(self, feature: Feature) -> str:
        """Generate HTML page for a feature by filling template variables"""
        template = self.html_template

        # Build variables dict with feature data
        short_subtitle = getattr(feature, 'short_subtitle', feature.description)
        replacements = {
            "{{FEATURE_TITLE}}": feature.title,
            "{{FEATURE_SHORT_DESCRIPTION}}": short_subtitle,
            "{{FEATURE_DESCRIPTION}}": short_subtitle,
            "{{FEATURE_KEYWORDS}}": feature.keywords(),
            "{{FEATURE_CATEGORY}}": "fleet management",
            "{{HIGHLIGHT_TITLE}}": feature.title,
            "{{HIGHLIGHT_ICON}}": "bi bi-gear",
            "{{VISUAL_OVERVIEW}}": getattr(feature, 'visual_overview', feature.description),
            "{{WHY_CHOOSE_PARAGRAPH_1}}": getattr(feature, 'why_choose_paragraph_1', feature.description or f"{feature.title} provides essential fleet management capabilities."),
            "{{WHY_CHOOSE_PARAGRAPH_2}}": getattr(feature, 'why_choose_paragraph_2', "Optimize your fleet operations."),
            "{{WHY_CHOOSE_PARAGRAPH_3}}": getattr(feature, 'why_choose_paragraph_3', "Streamline your workflows and improve efficiency."),
            "{{GETTING_STARTED}}": getattr(feature, 'getting_started', f"Experience {feature.title} and discover how it can streamline your fleet management workflow."),
            "{{GETTING_STARTED_TITLE}}": "Ready to get started?",
        }

        # Add benefits (up to 8) with descriptions from source
        benefit_descriptions = getattr(feature, 'benefits_descriptions', [])
        for i, benefit in enumerate((feature.benefits or [])[:8], 1):
            replacements[f"{{{{BENEFIT_TITLE_{i}}}}}"] = benefit
            # Use extracted description if available, otherwise use a generic one
            if i - 1 < len(benefit_descriptions):
                desc = benefit_descriptions[i - 1]
                # Clean up em dashes and colons
                desc = re.sub(r'^[\s—:]+', '', desc).strip()
                replacements[f"{{{{BENEFIT_DESCRIPTION_{i}}}}}"] = desc if desc else f"Benefit of {benefit}"
            else:
                replacements[f"{{{{BENEFIT_DESCRIPTION_{i}}}}}"] = f"Benefit of {benefit}"

        # Add empty benefits for unused slots
        for i in range(len(feature.benefits or []) + 1, 9):
            replacements[f"{{{{BENEFIT_TITLE_{i}}}}}"] = f"Additional Feature {i}"
            replacements[f"{{{{BENEFIT_DESCRIPTION_{i}}}}}"] = ""

        # Add steps (up to 4) - use extracted steps if available
        if feature.steps:
            for i, (step_title, step_desc) in enumerate(feature.steps[:4], 1):
                replacements[f"{{{{STEP_TITLE_{i}}}}}"] = step_title
                replacements[f"{{{{STEP_DESCRIPTION_{i}}}}}"] = step_desc
            # Fill remaining slots with default steps
            for i in range(len(feature.steps) + 1, 5):
                replacements[f"{{{{STEP_TITLE_{i}}}}}"] = f"Step {i}"
                replacements[f"{{{{STEP_DESCRIPTION_{i}}}}}"] = f"Enhance your workflow"
        else:
            steps = [
                ("Get Started", "Access the platform and set up your account"),
                ("Configure", "Customize settings for your operations"),
                ("Monitor", "Track real-time performance metrics"),
                ("Optimize", "Use insights to improve efficiency")
            ]
            for i, (step_title, step_desc) in enumerate(steps, 1):
                replacements[f"{{{{STEP_TITLE_{i}}}}}"] = step_title
                replacements[f"{{{{STEP_DESCRIPTION_{i}}}}}"] = step_desc

        # Add capabilities (up to 8)
        capabilities = feature.capabilities or [feature.title]
        for i, cap in enumerate(capabilities[:8], 1):
            replacements[f"{{{{CAPABILITY_TITLE_{i}}}}}"] = cap
            replacements[f"{{{{CAPABILITY_DESCRIPTION_{i}}}}}"] = ""  # Empty description for cleaner display

        # Add empty capabilities for unused slots
        for i in range(len(capabilities) + 1, 9):
            replacements[f"{{{{CAPABILITY_TITLE_{i}}}}}"] = f"Capability {i}"
            replacements[f"{{{{CAPABILITY_DESCRIPTION_{i}}}}}"] = ""

        # Add use cases (up to 8) with descriptions
        use_case_descriptions = getattr(feature, 'use_cases_descriptions', [])
        if feature.use_cases:
            for i, use_case in enumerate(feature.use_cases[:8], 1):
                replacements[f"{{{{USE_CASE_TITLE_{i}}}}}"] = use_case
                # Use extracted description if available
                if i - 1 < len(use_case_descriptions):
                    desc = use_case_descriptions[i - 1]
                    # Clean up em dashes and colons
                    desc = re.sub(r'^[\s—:]+', '', desc).strip()
                    replacements[f"{{{{USE_CASE_DESCRIPTION_{i}}}}}"] = desc if desc else ""
                else:
                    replacements[f"{{{{USE_CASE_DESCRIPTION_{i}}}}}"] = ""
            # Fill remaining slots
            for i in range(len(feature.use_cases) + 1, 9):
                replacements[f"{{{{USE_CASE_TITLE_{i}}}}}"] = f"Use Case {i}"
                replacements[f"{{{{USE_CASE_DESCRIPTION_{i}}}}}"] = ""
        else:
            use_cases = [
                ("Operations Teams", "Manage fleet operations from the dashboard"),
                ("Logistics Managers", "Optimize routes and schedules"),
                ("Drivers", "Access tools in the mobile app"),
                ("Dispatchers", "Track and coordinate deliveries"),
                ("Administrators", "Manage users and permissions"),
                ("Finance Teams", "Track costs and expenses"),
                ("Compliance Officers", "Monitor regulatory requirements"),
                ("Support Teams", "Provide customer assistance"),
            ]
            for i, (use_case_title, use_case_desc) in enumerate(use_cases, 1):
                replacements[f"{{{{USE_CASE_TITLE_{i}}}}}"] = use_case_title
                replacements[f"{{{{USE_CASE_DESCRIPTION_{i}}}}}"] = use_case_desc

        # Icon mapping for integrations - comprehensive list with priority ordering
        integration_icons = {
            "FleetYes sdk": "bi bi-diagram-3",
            "order management": "bi bi-list-check",
            "order": "bi bi-list-check",
            "real-time": "bi bi-lightning-charge",
            "notification": "bi bi-bell-fill",
            "alert": "bi bi-exclamation-circle-fill",
            "location": "bi bi-geo-alt-fill",
            "gps": "bi bi-geo-alt-fill",
            "geolocation": "bi bi-geo-alt-fill",
            "payment": "bi bi-credit-card",
            "earning": "bi bi-currency-pound",
            "communication": "bi bi-chat-dots",
            "chat": "bi bi-chat-dots",
            "analytics": "bi bi-graph-up",
            "reporting": "bi bi-file-earmark-text",
            "report": "bi bi-file-earmark-text",
            "mobile": "bi bi-phone",
            "ios": "bi bi-phone",
            "android": "bi bi-phone",
            "tachograph": "bi bi-clock-history",
            "rota planning": "bi bi-calendar2-week",
            "rota": "bi bi-calendar2-week",
            "scheduling": "bi bi-calendar2-week",
            "shift allocation": "bi bi-calendar2-check",
            "shift": "bi bi-calendar2-check",
            "leave": "bi bi-calendar-x",
            "absence": "bi bi-calendar-x",
            "external audit": "bi bi-file-earmark-check",
            "audit": "bi bi-file-earmark-check",
            "export": "bi bi-download",
            "import": "bi bi-upload",
            "fuel card integration": "bi bi-fuel-pump",
            "fuel card": "bi bi-fuel-pump",
            "integration": "bi bi-link-45deg",
            "api": "bi bi-link-45deg",
            "sdk": "bi bi-diagram-3",
            "vehicle": "bi bi-truck",
            "inspection": "bi bi-check-circle-fill",
            "proof": "bi bi-file-earmark-check",
            "delivery": "bi bi-box-seam",
            "fatigue": "bi bi-exclamation-triangle-fill",
            "monitoring": "bi bi-eye-fill",
            "incident": "bi bi-exclamation-triangle-fill",
            "driver": "bi bi-person-fill",
            "image": "bi bi-image",
            "camera": "bi bi-camera",
            "receipt": "bi bi-receipt",
            "expense": "bi bi-wallet2",
            "tracking": "bi bi-geo-alt-fill",
            "trip management": "bi bi-map",
            "route": "bi bi-map",
            "navigation": "bi bi-compass",
            "invoice": "bi bi-receipt",
            "invoicing": "bi bi-receipt",
            "websocket integration": "bi bi-lightning-charge",
            "websocket": "bi bi-lightning-charge",
            "socket": "bi bi-lightning-charge",
            "real time": "bi bi-lightning-charge",
            "deep link": "bi bi-link-45deg",
            "offline": "bi bi-wifi-off",
            "sync": "bi bi-arrow-left-right",
            "push": "bi bi-send-fill",
            "ml kit": "bi bi-cpu",
            "machine learning": "bi bi-cpu",
            "text recognition": "bi bi-eye-fill",
            "ocr": "bi bi-eye-fill",
            "calendar": "bi bi-calendar-event",
            "scheduling": "bi bi-calendar2-week",
            "biometric": "bi bi-shield-check",
            "authentication": "bi bi-shield-check",
            "privacy": "bi bi-lock",
            "protection": "bi bi-shield",
            "dark mode": "bi bi-circle-half",
            "theme": "bi bi-palette",
            "responsive": "bi bi-aspect-ratio",
            "ui": "bi bi-app",
            "interface": "bi bi-app",
            "internationalization": "bi bi-globe",
            "localization": "bi bi-globe",
            "training": "bi bi-mortarboard",
            "document": "bi bi-file-earmark",
            "tolling": "bi bi-road",
            "toll": "bi bi-road",
            "parking": "bi bi-p-circle",
            "fuel": "bi bi-fuel-pump",
            "cost": "bi bi-calculator",
            "expense tracking": "bi bi-receipt",
            "permission": "bi bi-lock",
            "settings": "bi bi-gear",
            "accounting": "bi bi-calculator",
            "custom": "bi bi-sliders",
            "resource": "bi bi-box-seam",
            "adapter": "bi bi-arrow-left-right",
            "error": "bi bi-exclamation-circle",
            "version": "bi bi-tag",
            "versioning": "bi bi-tag",
            "rate": "bi bi-speedometer2",
            "quota": "bi bi-speedometer2",
            "handling": "bi bi-gear",
            "storage": "bi bi-archive",
            "local": "bi bi-hdd",
            "cache": "bi bi-lightning-fill",
            "database": "bi bi-database",
            "backend": "bi bi-diagram-2",
            "synchronisation": "bi bi-arrow-left-right",
            "sync": "bi bi-arrow-left-right",
            "system": "bi bi-cpu",  # Generic fallback, use lower priority
        }

        # Add integrations (up to 8) with descriptions
        integration_descriptions = getattr(feature, 'integrations_descriptions', [])
        integrations = feature.integrations or []
        used_icons = {}  # Track which icons are used and how many times

        # Comprehensive fallback icons for when primary matches are exhausted
        # Use a diverse set to ensure variety across all 8 slots
        fallback_icons = [
            "bi bi-diagram-3",      # 0 - Default SDK/Architecture
            "bi bi-gear",           # 1 - Settings/Configuration
            "bi bi-sliders",        # 2 - Advanced Controls
            "bi bi-tools",          # 3 - Tools/Utilities
            "bi bi-wrench",         # 4 - Customization
            "bi bi-puzzle",         # 5 - Components/Plugins
            "bi bi-boxes",          # 6 - Containers/Packages
            "bi bi-layers",         # 7 - Layered Architecture
        ]

        for i, integ in enumerate(integrations[:8], 1):
            replacements[f"{{{{INTEGRATION_TITLE_{i}}}}}"] = integ
            # Use extracted description if available
            if i - 1 < len(integration_descriptions):
                desc = integration_descriptions[i - 1]
                # Clean up em dashes and colons
                desc = re.sub(r'^[\s—:]+', '', desc).strip()
                replacements[f"{{{{INTEGRATION_DESCRIPTION_{i}}}}}"] = desc if desc else ""
            else:
                replacements[f"{{{{INTEGRATION_DESCRIPTION_{i}}}}}"] = ""

            # Pick icon based on integration name - prioritize longer/more specific keywords first
            icon = None
            integ_lower = integ.lower()

            # Sort keywords by length (longest first) for better matching
            sorted_keywords = sorted(integration_icons.keys(), key=len, reverse=True)

            # First pass: find best matching keyword
            best_match_icon = None
            for keyword in sorted_keywords:
                if keyword in integ_lower:
                    best_match_icon = integration_icons[keyword]
                    break

            # Second pass: use the best match if not heavily used
            if best_match_icon:
                if best_match_icon not in used_icons:
                    used_icons[best_match_icon] = 0
                # Use matched icon if it's the first use (prefer keyword matches)
                if used_icons[best_match_icon] == 0:
                    icon = best_match_icon
                    used_icons[best_match_icon] += 1

            # If we couldn't use the keyword match, try to find unused matching keyword icons
            if icon is None and best_match_icon:
                icon = best_match_icon
                if best_match_icon not in used_icons:
                    used_icons[best_match_icon] = 0
                used_icons[best_match_icon] += 1

            # If still no icon, use fallback with round-robin to ensure variety
            if icon is None:
                # Find the least-used fallback icon to ensure variety
                best_fb = None
                min_uses = float('inf')
                for fb_icon in fallback_icons:
                    uses = used_icons.get(fb_icon, 0)
                    if uses < min_uses:
                        min_uses = uses
                        best_fb = fb_icon
                icon = best_fb if best_fb else fallback_icons[0]
                if icon not in used_icons:
                    used_icons[icon] = 0
                used_icons[icon] += 1

            replacements[f"{{{{INTEGRATION_ICON_{i}}}}}"] = icon

        # Add empty integrations for unused slots
        for i in range(len(integrations) + 1, 9):
            replacements[f"{{{{INTEGRATION_TITLE_{i}}}}}"] = f"Integration {i}"
            replacements[f"{{{{INTEGRATION_DESCRIPTION_{i}}}}}"] = ""
            replacements[f"{{{{INTEGRATION_ICON_{i}}}}}"] = "bi bi-diagram-3"

        # Apply all replacements
        for placeholder, value in replacements.items():
            template = template.replace(placeholder, str(value))

        return template

    def save_page(self, feature: Feature, content: str) -> Path:
        """Save HTML page to file"""
        filename = f"{feature.slug()}.html"
        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    def get_all_generated_pages(self) -> List[tuple]:
        """Get list of all generated pages: (slug, title, platform)"""
        pages = []
        for html_file in sorted(self.output_dir.glob("*.html")):
            if html_file.name == "feature-template.html":
                continue
            slug = html_file.stem
            # Read title from file
            try:
                with open(html_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    title_match = re.search(r'<h1>(.*?)</h1>', content)
                    if title_match:
                        title = title_match.group(1)
                        # Determine platform from content
                        if "mobile" in content.lower() or "driver" in content.lower():
                            platform = "mobile"
                        elif "dashboard" in content.lower() or "operations" in content.lower():
                            platform = "dashboard"
                        else:
                            platform = "both"
                        pages.append((slug, title, platform))
            except:
                pass
        return pages


def clean_old_pages(output_dir: Path):
    """Delete all existing .html files from feature directory"""
    html_files = list(output_dir.glob("*.html"))
    # Keep feature-template.html
    html_files = [f for f in html_files if f.name != "feature-template.html"]

    for filepath in html_files:
        try:
            filepath.unlink()
            print("[*] Deleted: {}".format(filepath.name))
        except Exception as e:
            print("[!] Failed to delete {}: {}".format(filepath.name, e))

    return len(html_files)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate feature marketing pages from .md and .mdx feature files"
    )
    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Generate dashboard feature pages only"
    )
    parser.add_argument(
        "--mobile",
        action="store_true",
        help="Generate mobile app feature pages only"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete old HTML files before regenerating"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./feature",
        help="Output directory for generated pages"
    )

    args = parser.parse_args()

    print("[*] FleetYes Feature Page Generator v3")
    print("=" * 50)

    output_dir = Path(args.output)

    # Clean old pages if requested
    if args.clean:
        print("[*] Cleaning old HTML files...")
        deleted_count = clean_old_pages(output_dir)
        print("[+] Deleted {} old files".format(deleted_count))
        print()

    # Parse features
    analyzer = FeatureAnalyzer()
    all_features = analyzer.get_all_features()

    if not all_features:
        print("[!] No features found in features-md/*/features/ directories")
        sys.exit(1)

    print("[+] Found {} features".format(len(all_features)))
    print()

    # Filter by platform if specified
    features_to_generate = all_features
    if args.dashboard:
        features_to_generate = [f for f in all_features if f.platform == "dashboard"]
    elif args.mobile:
        features_to_generate = [f for f in all_features if f.platform == "mobileapp"]

    # Generate pages
    generator = HTMLGenerator(str(output_dir))
    generated_count = 0

    for feature in features_to_generate:
        try:
            html_content = generator.generate_page(feature)
            filepath = generator.save_page(feature, html_content)
            print("[OK] {} -> {}".format(feature.title[:40], feature.slug()))
            generated_count += 1
        except Exception as e:
            print("[!] Failed to generate {}: {}".format(feature.title, e))

    print()
    print("=" * 50)
    print("[+] Generated {} feature pages".format(generated_count))
    print("[*] Done!")


if __name__ == "__main__":
    main()
