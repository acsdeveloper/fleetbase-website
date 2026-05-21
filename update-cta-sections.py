#!/usr/bin/env python3
"""
Update Final CTA sections with benefit-focused titles and descriptions.
Title: Compelling headline (max 2 lines) focused on key business benefit
Description: Short call-to-action description
"""

from pathlib import Path
import re


# Comprehensive CTA content for all features
# Format: slug -> {title, description}
CTA_CONTENT = {
    # Mobile App Features
    'ai-receipt-recognition': {
        'title': 'Turn Receipt Photos Into Instant Data Entry',
        'description': 'Save hours of manual data typing every week. OCR extracts everything automatically so you can focus on your delivery network.'
    },
    'background-location-tracking': {
        'title': 'Track Your Entire Fleet in Real-Time From Anywhere',
        'description': 'Know exactly where every vehicle is at every moment. Safety, compliance, and operational visibility on one map.'
    },
    'biometric-secure-authentication': {
        'title': 'Secure Your Fleet Data Without Password Frustration',
        'description': 'Biometric login is faster, more secure, and improves driver adoption. No forgotten passwords. No security headaches.'
    },
    'calendar-scheduling': {
        'title': 'Coordinate Driver Schedules and Eliminate Booking Conflicts',
        'description': 'Drivers see their schedule in real-time. No more double-booking, missed shifts, or last-minute confusion.'
    },
    'dark-mode-customisable-themes': {
        'title': 'Make Your App Comfortable for Night Drivers and Any Team',
        'description': 'Dark mode reduces eye strain during night shifts. Customizable themes reinforce your brand and improve driver adoption.'
    },
    'driver-operations': {
        'title': 'Give Drivers Complete Visibility Over Their Daily Deliveries',
        'description': 'Accept jobs, navigate routes, capture proof, and track earnings all in one app. Drivers stay informed. Productivity goes up.'
    },
    'driver-profile-documents': {
        'title': 'Keep Driver Licenses, Insurance, and Training Always Current',
        'description': 'Reduce compliance risk by ensuring every document is up-to-date. Automatic reminders prevent expired credentials from grounding your fleet.'
    },
    'expense-receipt-management': {
        'title': 'Stop Manual Expense Tracking and Speed Up Reimbursements',
        'description': 'Photograph receipts. AI reads everything automatically. Finance closes faster. Drivers get paid on time.'
    },
    'fleetbase-sdk': {
        'title': 'Build Custom Apps That Work Seamlessly With FleetYes',
        'description': 'Complete REST API documentation and mobile SDKs for building integrations and custom tools on top of your FleetYes instance.'
    },
    'geolocation-services': {
        'title': 'Deliver Accurately Every Time With Live Route Tracking',
        'description': 'Reduce missed deliveries and failed attempts. Real-time location data keeps operations informed and customers happy.'
    },
    'google-maps-navigation-apis': {
        'title': 'Guide Drivers to Every Delivery With Real-Time Navigation',
        'description': 'Integration with Google Maps ensures drivers always take the fastest route. Fewer missed turns. More on-time deliveries.'
    },
    'gps-navigation-route-tracking': {
        'title': 'See Exactly Where Every Vehicle and Driver Is Right Now',
        'description': 'Real-time GPS tracking keeps operations informed, improves driver safety, and proves accountability to customers.'
    },
    'image-processing': {
        'title': 'Extract Text and Data From Photos Instantly',
        'description': 'Receipt images, license photos, signatures—AI reads them all. Zero manual data entry. Perfect accuracy.'
    },
    'import-hub': {
        'title': 'Load Customer Orders and Data From Any System Instantly',
        'description': 'Stop manual data entry. Import from Excel, load boards, and your ERP in minutes. Data stays in sync automatically.'
    },
    'internationalisation-localisation': {
        'title': 'Operate Globally With Every Driver\'s Language and Currency',
        'description': 'Support multiple languages, currencies, and local regulations in a single app. Expand to new markets without rebuilding.'
    },
    'inventory-management': {
        'title': 'Track What You Have and Where It Is Every Moment',
        'description': 'Real-time inventory visibility prevents stockouts and lost shipments. Know your stock levels and locations instantly.'
    },
    'issue-reporting': {
        'title': 'Fix Delivery Problems Before They Become Customer Complaints',
        'description': 'Drivers report issues immediately. Operations resolves them fast. Fewer escalations. Happier customers.'
    },
    'ml-kit-text-recognition': {
        'title': 'Read Text From Any Photo and Extract It Automatically',
        'description': 'License plates, delivery notes, receipt text—OCR captures it all without manual typing. Fast, accurate, automated.'
    },
    'offline-first-architecture': {
        'title': 'Keep Drivers Productive Even When Connectivity Drops',
        'description': 'Work offline. Sync automatically when reconnected. No more lost data or missed deliveries due to network issues.'
    },
    'performance-tracking-earnings': {
        'title': 'Show Drivers Exactly How They\'re Performing and Earning',
        'description': 'Real-time performance metrics motivate drivers. Transparent earnings keep top performers engaged and improve retention.'
    },
    'proof-of-delivery': {
        'title': 'Eliminate Delivery Disputes With Instant Photo Proof',
        'description': 'Photograph every delivery. Get customer signature. Zero "I never got it" disputes. Complete accountability.'
    },
    'push-notification-services': {
        'title': 'Alert Drivers and Operations Instantly Without Delays',
        'description': 'Push notifications keep everyone informed in real-time. Faster response to problems. Better coordination. Happier teams.'
    },
    'push-notifications-real-time-updates': {
        'title': 'Keep Your Team Connected and Updated Every Second',
        'description': 'Real-time notifications ensure critical information reaches drivers and teams instantly. No delays. No missed messages.'
    },
    'real-time-chat-communication': {
        'title': 'Coordinate Your Fleet Without Endless Phone Calls',
        'description': 'Team chat keeps drivers, dispatchers, and managers aligned. Faster decisions. Better coordination. Fewer missed messages.'
    },
    'real-time-order-management': {
        'title': 'Assign Orders Instantly and Keep Drivers Productive',
        'description': 'Real-time order dispatch eliminates waiting. Drivers stay busy. You maximize each vehicle\'s capacity and earning potential.'
    },
    'responsive-mobile-ui': {
        'title': 'Work on Any Device With an Interface Built for Drivers',
        'description': 'Responsive design works on phones, tablets, and computers. Drivers use the right device for the right task.'
    },
    'shift-leave-management': {
        'title': 'Build Schedules Drivers Know About and Can Plan Around',
        'description': 'Drivers see their shifts instantly. Flexible leave request system improves morale and reduces scheduling headaches.'
    },
    'toll-expense-tracking': {
        'title': 'Capture Every Toll and Expense in Real-Time',
        'description': 'Photograph toll receipts and parking tickets. System captures details automatically. Perfect cost allocation and recovery.'
    },
    'training-compliance': {
        'title': 'Keep Your Team Trained and Compliant at All Times',
        'description': 'Automated training delivery and certification tracking. Reduce compliance risk. Ensure every driver is current and qualified.'
    },
    'trip-management': {
        'title': 'Manage Every Delivery From Acceptance to Completion',
        'description': 'Trip lifecycle tracking gives complete visibility. Know status at every moment. Predict delays before they happen.'
    },
    'vehicle-inspection': {
        'title': 'Catch Vehicle Issues Before They Cause Breakdowns',
        'description': 'Pre-trip and post-trip inspections catch problems early. Fewer breakdowns. Better maintenance planning. Improved safety.'
    },
    'vehicle-management': {
        'title': 'Keep Your Fleet Running Smoothly and Compliant',
        'description': 'Maintenance scheduling, registration tracking, and compliance monitoring in one system. No vehicles left unchecked.'
    },
    'websocket-socketcluster': {
        'title': 'Build Real-Time Apps That Scale With Your Fleet',
        'description': 'WebSocket API enables live updates without polling. Real-time collaboration tools that scale to thousands of concurrent users.'
    },

    # Dashboard Features
    'compliance-engine': {
        'title': 'Stop Compliance Violations Before They Happen',
        'description': 'Automated checking catches violations before assignments are made. Prevent fines. Pass inspections. Protect your reputation.'
    },
    'driver-management': {
        'title': 'Manage Your Entire Driver Team With Complete Visibility',
        'description': 'Document management, performance tracking, and compliance monitoring in one system. Scale from 10 to 1000 drivers.'
    },
    'fuel-tracking': {
        'title': 'Cut Fuel Costs by 15-20% and Eliminate Fraud',
        'description': 'See exactly where your fuel goes. Anomaly detection flags suspicious activity instantly. Control your largest expense.'
    },
    'import-hub': {
        'title': 'Connect Your Systems and Stop Manual Data Entry',
        'description': 'Import from Excel, load boards, and ERP systems in minutes. Data stays in sync automatically. No more duplicate entries.'
    },
    'leave-management': {
        'title': 'Build Schedules Faster and Reduce Scheduling Headaches',
        'description': 'Approve leave requests instantly. Update schedules in real-time. No conflicts. Your roster stays accurate and compliant.'
    },
    'operational-dashboard': {
        'title': 'See Your Entire Fleet Operation at a Glance',
        'description': 'Real-time KPIs and alerts on one screen. Spot problems in seconds. Make faster decisions. Run operations more efficiently.'
    },
    'org-settings-permissions': {
        'title': 'Control Access and Keep Your Data Secure',
        'description': 'Role-based permissions ensure the right people see the right data. Audit trails prove compliance. Security without friction.'
    },
    'rota-scheduling': {
        'title': 'Build Compliant Schedules in Minutes Instead of Hours',
        'description': 'Drag-and-drop scheduling respects compliance rules automatically. Publish faster. Drivers see their schedule instantly.'
    }
}


def update_cta_section(content: str, slug: str) -> str:
    """Update CTA section with benefit-focused title and description"""
    if slug not in CTA_CONTENT:
        return content

    cta_data = CTA_CONTENT[slug]
    title = cta_data['title']
    description = cta_data['description']

    # Replace the CTA section
    pattern = r'(<section class="cta-section-bottom"[^>]*>.*?<div class="container">\s*)<h2>[^<]+</h2>\s*<p>[^<]+</p>'

    def replace_cta(match):
        return match.group(1) + f'<h2>{title}</h2>\n        <p>{description}</p>'

    return re.sub(pattern, replace_cta, content, flags=re.DOTALL)


def process_all_features():
    """Process all feature pages"""
    feature_dir = Path("feature")
    processed = 0
    updated_count = 0

    for html_file in sorted(feature_dir.glob("*.html")):
        if html_file.name in ["feature-template.html", "INDEX-COMPLETE.html"]:
            continue

        slug = html_file.stem

        with open(html_file, "r", encoding="utf-8") as f:
            original_content = f.read()

        new_content = update_cta_section(original_content, slug)

        if new_content != original_content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated_count += 1
            print(f"[+] {html_file.name}: Updated CTA section with benefit-focused title and description")

        processed += 1

    return processed, updated_count


def main():
    """Main function"""
    print("[*] Updating Final CTA sections with benefit-focused content...\n")

    processed, updated = process_all_features()

    print(f"\n[+] Processed {processed} feature pages")
    print(f"[+] Updated {updated} CTA sections with benefit-focused titles and descriptions")
    print("[+] Complete!")


if __name__ == "__main__":
    main()
