# AssetFlow - Enterprise Asset & Resource Management System

AssetFlow is a centralized, industry-agnostic ERP platform built on Odoo to simplify and digitize how organizations track, allocate, and maintain their physical assets and shared resources. By replacing fragmented spreadsheets and manual paper logs, AssetFlow establishes absolute visibility over the asset lifecycle, resource booking conflicts, and structured maintenance workflows.

---

## 🚀 Key Features

* **Complete Asset Lifecycle Tracking:** Real-time state management (`Available`, `Allocated`, `Reserved`, `Under Maintenance`, `Lost`, `Retired`, `Disposed`) with a complete historical log of transfers and repairs.
* **Conflict-Free Allocation:** Strict validation engine preventing double-allocation of individual assets. Integrates a smart "Transfer Request" workflow between departments and employees.
* **Shared Resource Booking:** Time-slot booking engine with strict overlap validation for shared corporate spaces, vehicles, and equipment, rendered on an intuitive calendar view.
* **Structured Maintenance Workflows:** Comprehensive repair routing (Pending → Approved → Assigned → In Progress → Resolved) that automatically toggles asset states to safeguard operational data.
* **Rigorous Audit Cycles:** Structured auditing module allowing assigned auditors to run discrepancy reports, verify physical existence, and lock asset updates upon cycle closure.
* **Role-Based Access Control (RBAC):** Realistic security framework ensuring segregated operational flows for **Admins**, **Asset Managers**, **Department Heads**, and **Employees**.

---

## 📂 Module Architecture

```text
assetflow/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── organization.py       # Departments, Employee Directory Extensions
│   ├── asset.py              # Asset Registry, Lifecycle, Categories
│   ├── allocation.py         # Allocations & Transfer Requests
│   ├── booking.py            # Resource Bookings & Overlap Validation
│   ├── maintenance.py        # Repair Approvals & Workflows
│   └── audit.py              # Audit Cycles & Discrepancy Verification
├── views/
│   ├── menus.xml             # Main Root & Sub-menu actions
│   ├── organization_views.xml
│   ├── asset_views.xml
│   ├── allocation_views.xml
│   ├── booking_views.xml
│   ├── maintenance_views.xml
│   └── audit_views.xml
└── security/
    ├── security_roles.xml    # Security Groups (RBAC)
    └── ir.model.access.csv   # Data Access Control Lists
