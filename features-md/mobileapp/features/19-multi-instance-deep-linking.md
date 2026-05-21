# Multi-Instance Deep Linking
## One app, unlimited companies—onboarding happens in one click, configuration happens instantly

Multi-company operations used to mean installing separate apps for each company. Want to drive for Company A and Company B? Install both versions. New company launches? Wait for app store approval. Change companies? Uninstall, reinstall. This friction wastes time and creates confusion.

Our deep-linking system makes multi-company operations seamless. One app works with any company. Click a link. Configured instantly with that company's backend, settings, and branding. Switch companies? Click a different link. No reinstalling, no app store delays, no confusion about which version you're using.

---

## Key Benefits

- **One App, Multiple Companies**: Drive for different companies without managing separate app installations—click a link, instantly configured for that company
- **Instant Onboarding Without App Store Delays**: New drivers or new companies configure in seconds—no waiting for app store approval, no deployment delays, no "version mismatch" problems
- **Switch Companies Without Reinstalling**: Work for Company A in the morning, Company B in the afternoon—one app, multiple configurations, instant switching
- **Enterprise Deployment at Scale**: Large enterprises deploy one app across 50 business units, 10 regions, multiple operations without managing 50 app versions
- **Perfect for Gig Economy**: Drive for multiple delivery platforms using one app—each platform's configuration loads instantly via deep link
- **Zero Configuration Complexity**: New drivers don't need IT support—they receive a link, click it, their app is ready—configuration is automatic and verified
- **Development Team Efficiency**: Developers and QA switch between testing environments (dev/staging/production) instantly without rebuilding—massive speed advantage
- **Expansion Doesn't Require New Releases**: Enter a new market? New company launches? No app store update needed—just generate a new configuration link

---

## How It Works

**1. Generate Configuration Link**
Your organisation administrator generates a unique deep link containing API endpoint, authentication token, and configuration parameters.

**2. Share the Link**
The link is sent to drivers via email, SMS, or QR code—simple and secure delivery mechanism.

**3. Click to Configure**
Drivers click the link, which automatically configures the app with your organisation's backend and settings.

**4. Start Working**
The app is immediately ready to use with your company's orders, rates, and operational rules.

---

## Core Capabilities

- Dynamic API endpoint configuration
- Instance switching without app reinstall
- Secure deep link parameter passing
- Multi-organisation support in single app
- Environment switching (dev/staging/production)
- Automatic configuration validation
- Secure token and credential handling
- Per-instance branding and customisation

---

## Use Cases

- **Shared App Across Subsidiaries**: A parent company with multiple logistics subsidiaries deploys one app across all units
- **Development & Testing**: Developers and QA teams switch between development, staging, and production environments
- **Multi-Region Operations**: Companies operating in multiple countries and regions use a single app codebase
- **Third-Party Integrations**: Partner companies integrate FleetYes with their own FleetYes instances
- **Quick Deployment**: New client onboarding requires zero IT effort—just send a link
- **Franchise Networks**: Franchise operations where each franchisee has their own FleetYes instance
- **White-Label Solutions**: Platform providers give each customer a branded experience on a single codebase
- **Temporary Access**: Grant time-limited access to contractors or temporary workers without permanent app installation

---

## Integration & Compatibility

- **FleetYes SDK**: Dynamic SDK instantiation with configurable endpoints
- **Deep Linking**: iOS and Android URL scheme handling
- **Secure Configuration**: Encrypted parameter passing and validation
- **Authentication**: Instance-specific API token management
- **Environment Management**: Dev/staging/production endpoint switching
- **Configuration Persistence**: Local storage of instance configuration
- **Security Protocols**: URL validation and parameter verification
- **Enterprise SSO**: Integration with single sign-on systems

---

## Why Choose This Feature

Managing multiple app versions is a scaling nightmare. Every new company needs its own variant. Version updates require coordinating releases across multiple versions. New market launch? New app to manage. This creates maintenance overhead and version fragmentation.

Our deep-linking approach eliminates this completely. One app works with unlimited companies. Configuration happens via link, not app rebuilds. New market launch? Generate a link. New company? Link. Switching companies? Link. Your engineering team maintains one codebase while supporting unlimited configurations.

**For enterprises:** Deploy across 50 business units, 10 regions, or 100 customer organisations using a single app version. Updates roll out instantly to everyone. No version fragmentation. No coordination nightmare. This is enterprise-grade operational leverage.

---

## Visual Overview

When a driver clicks a configuration link, the app opens with a setup screen briefly showing the organisation name and configuration status. Behind the scenes, it validates the link parameters, establishes connection to the backend, and retrieves configuration. Once complete, the main dashboard displays with the organisation's branding, logo, and colour scheme. A settings screen shows current instance information and provides options to switch instances or reconfigure.

---

## Getting Started

Deploy across unlimited companies with one app—no version fragmentation, no deployment delays, instant provisioning.


