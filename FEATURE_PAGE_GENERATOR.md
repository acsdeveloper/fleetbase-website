# Feature Page Generator Documentation

## Overview

The `generate-feature-pages.py` script automatically generates production-ready marketing pages for all features in FleetYes Dashboard and Navigator based on the `PROJECT_FEATURES_ANALYSIS.md` reports.

## Features

✅ **Automated Page Generation**
- Parses dashboard and mobile app feature analysis reports
- Generates complete HTML marketing pages with consistent styling
- Supports both "live" and "planned" features

✅ **Comprehensive Content Sections**
- Hero section with feature title and description
- Key benefits with visual cards
- How it works step-by-step guide
- Core capabilities grid
- Third-party integrations showcase
- Call-to-action sections
- Responsive design with Bootstrap

✅ **Smart Feature Merging**
- Automatically merges features across platforms (dashboard + mobile)
- Marks features available on both web and mobile
- Differentiates planned vs. delivered features

✅ **SEO-Ready**
- Auto-generated keywords based on feature content
- Meta descriptions and Open Graph tags
- Proper heading hierarchy
- Breadcrumb navigation

## Installation

No additional dependencies required beyond Python 3.6+

## Usage

### Basic Usage

Generate all feature pages:
```bash
python generate-feature-pages.py
```

### Command-Line Options

```
-h, --help              Show help message
--dashboard             Generate dashboard feature pages only
--mobile                Generate mobile app feature pages only
--all                   Generate all feature pages (default)
--output OUTPUT         Output directory for generated pages (default: ./feature)
```

### Examples

Generate all features:
```bash
python generate-feature-pages.py
```

Generate dashboard features only:
```bash
python generate-feature-pages.py --dashboard
```

Generate mobile app features only:
```bash
python generate-feature-pages.py --mobile
```

Generate to custom output directory:
```bash
python generate-feature-pages.py --output ./marketing/features
```

## Input Files

The script reads from two sources:

### Dashboard Features
**Location:** `features-md/dashboard/PROJECT_FEATURES_ANALYSIS.md`

Contains:
- Project overview
- Key benefits (converted to feature pages)
- Third-party integrations
- Standout features
- Gaps & suggestions (marked as planned)

### Mobile Features
**Location:** `features-md/mobileapp/PROJECT_FEATURES_ANALYSIS.md`

Contains:
- Project overview
- Key benefits (converted to feature pages)
- Third-party integrations
- Standout features
- Gaps & suggestions (marked as planned)

## Output Files

### Generated Pages
**Location:** `./feature/` (default, customizable with `--output`)

Each feature gets a dedicated HTML page:
- `operational-intelligence.html` — Dashboard overview
- `compliance-engine.html` — Real-time compliance monitoring
- `expense-and-receipt-management.html` — Expense tracking
- `navigation-and-route-efficiency.html` — Mobile navigation
- ... and 35 more feature pages

Total: **39 feature pages** (25 live + 14 planned)

### File Naming Convention

Feature names are converted to URL slugs:
- `"Operational Intelligence"` → `operational-intelligence.html`
- `"Fuel & Cost Management"` → `fuel-and-cost-management.html`
- `"Driver Roster & Scheduling"` → `driver-roster-and-scheduling.html`

## Template System

The script uses **feature-template.html** as the base template with placeholder variables:

### Placeholder Variables

**Feature Metadata:**
- `{{FEATURE_TITLE}}` — Feature name
- `{{FEATURE_SHORT_DESCRIPTION}}` — Brief feature description
- `{{FEATURE_DESCRIPTION}}` — Detailed description
- `{{FEATURE_KEYWORDS}}` — Auto-generated SEO keywords
- `{{FEATURE_CATEGORY}}` — Feature category

**Benefits (8 slots):**
- `{{BENEFIT_TITLE_1}}` through `{{BENEFIT_TITLE_8}}`
- `{{BENEFIT_DESCRIPTION_1}}` through `{{BENEFIT_DESCRIPTION_8}}`

**How It Works (4 steps):**
- `{{STEP_TITLE_1}}` through `{{STEP_TITLE_4}}`
- `{{STEP_DESCRIPTION_1}}` through `{{STEP_DESCRIPTION_4}}`

**Capabilities (8 slots):**
- `{{CAPABILITY_TITLE_1}}` through `{{CAPABILITY_TITLE_8}}`
- `{{CAPABILITY_DESCRIPTION_1}}` through `{{CAPABILITY_DESCRIPTION_8}}`

**Use Cases (8 slots):**
- `{{USE_CASE_TITLE_1}}` through `{{USE_CASE_TITLE_8}}`
- `{{USE_CASE_DESCRIPTION_1}}` through `{{USE_CASE_DESCRIPTION_8}}`

**Integrations (8 slots):**
- `{{INTEGRATION_TITLE_1}}` through `{{INTEGRATION_TITLE_8}}`
- `{{INTEGRATION_DESCRIPTION_1}}` through `{{INTEGRATION_DESCRIPTION_8}}`
- `{{INTEGRATION_ICON_1}}` through `{{INTEGRATION_ICON_8}}`

**Additional:**
- `{{HIGHLIGHT_TITLE}}` — Feature highlight title
- `{{HIGHLIGHT_DESCRIPTION}}` — Feature highlight description
- `{{HIGHLIGHT_ICON}}` — Bootstrap icon class
- `{{WHY_CHOOSE_PARAGRAPH_1/2/3}}` — Three paragraphs

## Generated Page Structure

Each feature page includes (from your template):

```html
📄 Metadata (Meta tags, description, keywords)
🎯 Hero Section
   - Feature title & description
   - Breadcrumb navigation
   - "Book a Demo" CTA

📊 Key Benefits Section
   - Grid of benefit cards (8 slots)
   - Customizable benefit titles & descriptions

🔧 How It Works Section
   - Step-by-step cards (4 steps)
   - Numbered progression

⚡ Core Capabilities Section
   - Capability list with icons (8 items)
   - Feature-specific capabilities

🖼️ Feature Highlight Section
   - Full-width image + content
   - Alternate layout

📋 Use Cases Section
   - Real-world scenarios (8 slots)
   - Card-based layout

❓ Why Choose This Feature Section
   - 3 paragraph explanation
   - Customizable benefits

🔗 Integration & Compatibility Section
   - Integration cards (8 slots)
   - With icons and descriptions

💬 Final CTA Section
   - "Ready to transform?" messaging
   - Demo booking link

🔗 Footer
   - Company info
   - Links and copyright
```

## Styling

The generated pages use:
- **Bootstrap 5** for responsive grid layout
- **Animate On Scroll (AOS)** for scroll animations
- **Bootstrap Icons** for visual elements
- **Custom CSS** for feature-specific styling
- **Dark theme support** with CSS variables

## Feature Metadata

### Platform Badges
- `[LIVE]` — Feature is currently available
- `[PLANNED]` — Feature is in development/roadmap

### Platform Tags
- `Dashboard Feature` — Web dashboard only
- `Mobile App Feature` — Mobile app only
- `Available on Web & Mobile` — Both platforms

## Generated Statistics

Running the script generates:
- **39 feature pages** total
- **25 live features** (production-ready)
- **14 planned features** (roadmap items)

### Platform Breakdown
- **Dashboard-only:** 11 features
- **Mobile-only:** 7 features (delivered) + 7 planned
- **Common (both platforms):** 9 features

## Integration with Website

### How to Link to Feature Pages

From other pages, link to features:
```html
<a href="./feature/compliance-engine.html">View Compliance Engine</a>
```

### Breadcrumb Navigation

Each generated page includes breadcrumb navigation:
```
Home / Features / Compliance Engine
```

## SEO Best Practices

Each page is optimized for search with:
- Unique title tags with feature name + "FleetYes"
- Meta descriptions from feature overview
- Auto-generated keywords
- Open Graph tags for social sharing
- Semantic HTML structure
- Mobile-responsive design

## Updating Features

### To Add a New Feature:

1. **Add to PROJECT_FEATURES_ANALYSIS.md:**
   - Add a section under `## KEY BENEFITS` in the relevant file
   - Include a title and description
   - Optionally add integration names

2. **Regenerate pages:**
   ```bash
   python generate-feature-pages.py
   ```

3. **New page is automatically created** in `./feature/`

### To Mark a Feature as Planned:

1. **Move to GAPS & SUGGESTIONS section** in PROJECT_FEATURES_ANALYSIS.md
2. **Regenerate pages** — it will be marked `[PLANNED]`

## Troubleshooting

### "No features found" error
- Ensure `features-md/dashboard/PROJECT_FEATURES_ANALYSIS.md` exists
- Ensure `features-md/mobileapp/PROJECT_FEATURES_ANALYSIS.md` exists
- Check file permissions (readable)

### Pages not updating
- Delete old generated pages: `rm ./feature/*.html`
- Ensure PROJECT_FEATURES_ANALYSIS.md files are saved
- Run generator again

### Unicode/Encoding errors
- Script uses UTF-8 encoding internally
- Ensure your terminal supports UTF-8 output

## Performance

- **Execution time:** ~1 second for 39 pages
- **Output size:** ~15-20MB total (HTML only, no images)
- **Python version:** 3.6+

## Customization

### Modify HTML Template

Edit the `HTML_TEMPLATE` string in `generate-feature-pages.py`:
- Change section layouts
- Modify color scheme
- Add/remove sections
- Update footer content

### Custom Styling

Add CSS rules to the `<style>` section in the template:
```python
HTML_TEMPLATE = """...
<style>
  /* Your custom styles */
  .benefit-card {
    /* Modify card appearance */
  }
</style>
...
"""
```

## Advanced Usage

### Python API

Use the generator programmatically:

```python
from generate_feature_pages import FeatureAnalyzer, HTMLGenerator

# Parse features
analyzer = FeatureAnalyzer()
features = analyzer.get_all_features()

# Generate page for a specific feature
generator = HTMLGenerator(output_dir="./feature")
feature = features['compliance-engine']
html_content = generator.generate_page(feature)
filepath = generator.save_page(feature, html_content)
print(f"Generated: {filepath}")
```

## Maintenance

### Recommended Schedule

- **After feature updates:** Regenerate immediately
- **Weekly review:** Check for typos or broken links
- **Monthly audit:** Verify all pages render correctly
- **Before release:** Test all feature pages in browser

### QA Checklist

- [ ] All pages generated without errors
- [ ] Pages render correctly in Chrome, Firefox, Safari, Edge
- [ ] Links point to correct destinations
- [ ] Images load properly
- [ ] Metadata is accurate
- [ ] Mobile responsive design works
- [ ] No console errors in browser DevTools
- [ ] SEO metadata is appropriate

## License

Part of FleetYes Marketing website. All generated pages inherit the project's license.

## Version History

### v1.0 (2026-05-20)
- Initial release
- Support for dashboard and mobile app features
- 39 feature pages generated
- SEO optimization
- Responsive design
- Live + planned feature distinction

---

**Last updated:** 2026-05-20  
**Generated pages:** 39 (25 live + 14 planned)  
**Output directory:** `./feature/`
