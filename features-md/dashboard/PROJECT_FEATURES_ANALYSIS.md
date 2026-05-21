---

# PROJECT OVERVIEW

FleetYes is a comprehensive fleet management dashboard that gives logistics and transport operators complete visibility and control over their operations. It centralises trip scheduling, driver and vehicle management, compliance tracking, and operational costs—enabling data-driven decisions that improve service delivery and reduce overhead. Built for transport companies, hauliers, and logistics firms with 10–500+ vehicles.

> **📄 Marketing Pages Available**  
> High-conversion marketing pages for each feature are available in `/apps/v4/content/marketing/features/`. These benefit-driven pages are production-ready for landing pages, sales collateral, and product documentation.

---

# KEY BENEFITS

## Operational Intelligence
- **Real-time dashboard shows trips, drivers, and vehicles at a glance**
  View today's trips, active drivers, fleet utilisation, and vehicle downtime on one screen. Quick-access KPIs let you spot problems (unassigned trips, drivers on leave) within seconds. No digging through spreadsheets.

## Trip & Route Management
- **Schedule, dispatch, and track trips end-to-end**
  Create trips, assign drivers and vehicles, dispatch in real time, and monitor progress from pickup to completion. Pull historical data and re-use past trip templates. Bulk import trips from your load board.

## Driver Roster & Scheduling
- **Build weekly rotas, manage leave, and track driver availability**
  Visual calendar shows working days, rest days, holidays, and unavailability. Automatic conflict detection flags violations; bulk import lets you load weeks of scheduling in one go. See which drivers are available right now.

## Intelligent Shift Allocation
- **Auto-assign trips to the best available driver**
  AI-powered allocation engine considers driver hours, vehicle availability, location, and compliance rules. Batch-allocate dozens of trips in seconds. No manual spreadsheet hunting.

## Vehicle Maintenance & Fleet Health
- **Track MOT, tachograph, PMI, and downtime windows**
  Calendar view shows upcoming and ongoing maintenance. Mark vehicles unavailable and see automatic impact on scheduling. Never miss a regulatory deadline.

## Compliance Engine
- **Monitor driver hours, rest breaks, and transport regulations in real time**
  Built-in compliance checker flags violations against UK driving rules. Highlights insufficient rest, excessive hours, or unsafe shift patterns. Prevents costly fines and keeps your fleet audit-ready.

## Fuel & Cost Management
- **Record fuel purchases, expenses, and receipts; generate reports**
  Import bulk fuel transactions via Excel or manual entry. Attach receipt images with automatic OCR. Track costs per vehicle, per driver, or per trip. Export reports for accounting systems.

## Toll & Expense Tracking
- **Capture tolls, parking, fines, and ad-hoc costs against trips**
  Record tollway charges, parking fees, and penalty notices. Link to specific trips for accurate cost allocation and invoice adjustments.

## Import Hub & Bulk Operations
- **Load data from external systems via API, file upload, or browser extension**
  Connect Amazon Relay, Geotab, and other load boards. Sync trips automatically or import via Excel. Bulk create drivers, vehicles, and trips; bulk delete; bulk export.

## Walkaround & Vehicle Inspection
- **Photo-based vehicle condition checks before and after trips**
  Capture vehicle state with photos, notes, and checklists. Flagged damage is documented and tracked. Auditable record for insurance and disputes.

## Staff Training & Compliance Documents
- **Centralised library for training records, business docs, and policies**
  Upload driver training certs, driver CPC records, company policies. Track expiry dates and alert when renewal is due. Downloadable templates for standard compliance documents.

## Driver CPC & Regulatory Compliance
- **DVLA-integrated driver licence checks and CPC tracking**
  Track continuing professional development, periodic training, and qualification renewals. Integration with DVLA ensures licence validity. Audit trail for regulator inspections.

## Leave & Absence Management
- **Record and approve driver leave; flag calendar conflicts**
  Approved leave blocks drivers from scheduling. See at a glance who's out and for how long. Integrate with rota planning automatically.

## Inventory Management
- **Track spare parts, equipment, and consumables**
  Log inventory levels, set reorder thresholds, and track usage. Know what's in stock before ordering more.

## Organisation Settings & Permissions
- **Role-based access control and audit logs**
  Manage users, assign permissions by role, and track who changed what and when. Multi-organisation support for group operators.

## Multi-Language & Dark Mode
- **Available in multiple languages with automatic dark theme**
  Fully localised UI; theme adapts to user preference. Accessible to international teams.

---

# THIRD-PARTY INTEGRATIONS

- Amazon Relay — Load board and trip sync via API or browser extension
- Geotab — Telematics and vehicle telemetry
- TripDash — Third-party trip data exchange
- Google Maps / Mapbox — Route planning and distance calculation
- DVLA — Driver licence validation and status checks
- Tesseract.js — OCR processing for receipt images
- AWS — Expense report export and archival
- Walkaround API — Vehicle inspection photos and metadata

---

# STANDOUT FEATURES

1. **Compliance Engine with Prospective & Retrospective Checking**
   FleetYes uniquely combines real-time pre-journey compliance validation with after-the-fact auditing. Drivers see what's allowed before they accept a trip, and managers can retroactively verify entire rotas. This dual approach reduces violations and creates an auditable record for regulatory inspections.

2. **Intelligent Shift Auto-Allocation**
   The platform's async AI allocation engine considers driver hours, vehicle fit, location, and regulatory constraints simultaneously. It batches trips and allocates them in seconds—no manual matching, no missed opportunities, no compliance slip-ups. Rare in smaller logistics platforms.

3. **Unified Operational Dashboard**
   One screen shows trips, drivers, vehicles, leave, maintenance, and compliance status. Contextual alerts (unassigned trips, drivers at rest limit, vehicles due for inspection) surface the day's priorities instantly. No tab switching or silent failures.

---

# GAPS & SUGGESTIONS

- **Mobile/native driver app** — Currently web-only. Native apps (iOS/Android) would let drivers accept trips, start/end work, and upload walkaround photos offline and in the field.

- **Advanced analytics & insights** — No trend analysis, predictive maintenance alerts, or cost-per-mile dashboards. BI-layer (Tableau, Looker) integration or embedded charts would unlock hidden patterns in fleet data.

- **Richer telematics** — Limited real-time vehicle location, idle-time tracking, or harsh-braking alerts. Deeper Geotab integration would improve safety monitoring and fuel efficiency.

- **Real-time trip tracking map** — No live map of trips in transit. WebSocket-based position updates would let control rooms track drivers and provide live ETAs to customers.

- **Dynamic pricing/rate cards** — No revenue management or customer pricing integrations. Ability to tie trip costs to customer contracts would improve margin control.

- **Automated invoice generation** — Currently no native billing; integration with accounting systems (Xero, QuickBooks) would close the loop from trip to invoice.

- **Advanced vehicle routing** — No multi-stop optimisation or time-window constraints. Integrating a routing engine would reduce miles, fuel, and driver hours on complex routes.

---

# MARKETING PAGES

High-conversion feature pages have been created for all major features. Each page includes:
- **8 Key Benefits** (outcome-led, measurable results)
- **4 How It Works** (simple user journey)
- **8 Core Capabilities** (value-backed features)
- **8 Use Cases** (real-world scenarios)
- **8 Integration & Compatibility** (business enablers)

**Location:** `/apps/v4/content/marketing/features/`

## Available Pages

| Feature | File | Focus |
|---------|------|-------|
| **Operational Dashboard** | `operational-dashboard.mdx` | Real-time KPIs, alerts, custom widgets |
| **Trip & Route Management** | `trip-management.mdx` | Dispatch, tracking, bulk operations |
| **Rota Scheduling & Planning** | `rota-scheduling.mdx` | Visual planning, compliance, preferences |
| **Compliance Engine** | `compliance-engine.mdx` | UK/EU regulations, prospective checking |
| **Vehicle Management** | `vehicle-management.mdx` | Maintenance, compliance, utilisation |
| **Driver Management** | `driver-management.mdx` | Onboarding, availability, DVLA integration |
| **Fuel & Cost Management** | `fuel-tracking.mdx` | Consumption, expenses, anomalies |
| **Import Hub & Data Integration** | `import-hub.mdx` | Load boards, bulk import, bi-directional sync |
| **Vehicle Inspection & Walkaround** | `vehicle-inspection.mdx` | Pre/post-trip photos, damage tracking |
| **Toll & Expense Tracking** | `toll-expense-tracking.mdx` | Cost capture, allocation, fraud detection |
| **Staff Training & Compliance Docs** | `training-compliance.mdx` | CPC tracking, certificates, audits |
| **Leave & Absence Management** | `leave-management.mdx` | Requests, approvals, coverage forecasting |
| **Inventory Management** | `inventory-management.mdx` | Parts tracking, reorder, forecasting |
| **Organisation Settings & Permissions** | `org-settings-permissions.mdx` | RBAC, audit logs, multi-tenancy |

## Documentation Guides

- **INDEX.md** — Quick navigation by feature and use case
- **README.md** — Format specification and coverage summary

---

*Analysis prepared: 2026-05-20*  
*Marketing pages created: 2026-05-20*  
*Target audience: Product, marketing, and leadership teams*  
*Status: All feature pages production-ready for landing pages and sales collateral*
