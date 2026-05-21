# FleetYes SDK Integration
## One integration connects everything—orders, drivers, customers, and real-time operations all working together

Building a delivery operations app means integrating with your backend, your databases, your real-time systems. Bad integration means data is stale, orders don't sync, drivers don't see updates. Good integration is invisible—everything just works.

Our FleetYes SDK integration is comprehensive and invisible. Your entire operations backend connects seamlessly—orders, driver profiles, customers, settings. Real-time updates flow both directions. Offline operations queue and sync automatically. It just works, at scale, reliably.

---

## Key Benefits

- **Complete Operational Synchronisation**: Orders, driver profiles, customer data, company settings—everything syncs automatically, nothing is missed or duplicated
- **Real-Time Operations Flow**: Changes on the backend appear in the app instantly via WebSocket—drivers always see current information, no manual refresh needed
- **Offline-Smart Syncing**: When connectivity is lost, the app queues updates locally and syncs intelligently when reconnected—no data loss, no confusion about what synced
- **Secure, Scalable Authentication**: Drivers authenticate with their FleetYes credentials, permissions and access control are enforced at backend level—security without complexity
- **Extensible from Day One**: Custom data models, extended functionality, new fields—the SDK supports what you need today and tomorrow without API redesign
- **Performance Built-In**: Intelligent caching, batched API calls, efficient pagination—the app stays fast and responsive even with thousands of concurrent drivers
- **Integration That's Actually Simple**: Well-documented SDK with clear examples means your development team gets integrated quickly, not months of API debugging
- **Scales Transparently**: Whether you have 50 drivers or 5,000, the backend and app scale together without degradation—architecture that grows with you

---

## How It Works

**1. Initialise Connection**
When the driver logs in, the app initialises a connection to your FleetYes backend using credentials and API configuration.

**2. Sync Initial Data**
The app retrieves the driver's assigned orders, profile, company settings, and other necessary data from the backend.

**3. Maintain Real-Time Sync**
Changes on the backend are streamed to the app in real-time. New orders, cancellations, and updates appear instantly.

**4. Submit Updates**
When drivers complete actions (accept order, mark delivered, submit proof), these updates are sent back to the backend with automatic retry if connectivity is lost.

---

## Core Capabilities

- Full Order resource management (query, create, update, delete)
- Driver profile synchronisation and updates
- Customer information and contact data
- Organisation settings and configuration
- Real-time event streaming via WebSocket
- Batch data retrieval and pagination support
- Automatic data synchronisation on connection restored
- Offline queue management and sync

---

## Use Cases

- **Order Management**: Complete order lifecycle from assignment through completion with synchronisation
- **Driver Authentication**: Secure driver login with role-based permissions and access control
- **Data Consistency**: Orders assigned in your operations system appear in drivers' phones instantly
- **Performance Metrics**: Driver metrics, completion rates, and performance statistics tracked in real-time
- **Custom Workflows**: Organisations can extend the SDK with custom fields and operations
- **Multi-Team Operations**: Dispatch teams assign orders, drivers receive them, supervisors track progress—all real-time
- **Audit Trails**: Complete operation history maintained for compliance and analysis
- **Integration Layer**: Seamless integration with existing fleet management systems

---

## Integration & Compatibility

- **REST API**: HTTP-based communication for data operations
- **WebSocket Integration**: Real-time event streaming and live updates
- **Authentication**: OAuth and token-based authentication
- **Custom Resources**: Support for extended data models
- **Adapter Pattern**: Flexible backend adapter architecture
- **Error Handling**: Comprehensive error codes and recovery strategies
- **Versioning**: Multiple API versions supported for backward compatibility
- **Rate Limiting**: Intelligent rate limiting and quota management

---

## Why Choose This Feature

A disconnected app is useless. You need your backend connected seamlessly to your drivers. Poor integration means stale data, sync errors, and frustrated operations teams. Good integration is invisible—everything just works.

The FleetYes SDK is the invisible backbone. It handles all the complexity: data synchronisation, offline scenarios, real-time updates, authentication, error recovery. Your app code focuses on user experience. The SDK handles everything else transparently.

This is why drivers work reliably even in areas with poor connectivity. The SDK queues operations locally, syncs intelligently when connectivity returns, and maintains perfect data consistency. Your entire operations system flows through one reliable connection, transparently.

---

## Visual Overview

The SDK operates transparently in the background. From the app's perspective, it fetches data, syncs changes, and handles connectivity seamlessly. Developers configure the SDK once, then use high-level APIs like `FleetYes.orders.query()` or `order.start()` without worrying about HTTP details, authentication, or offline handling.

---

## Getting Started

Complete backend integration in minutes—orders, drivers, and operations all connected and synced in real-time.


