# Database Design

## Overview

The Laboratory Equipment Management System uses **PostgreSQL** as its relational database management system (RDBMS). The database is designed following normalization principles to reduce redundancy, maintain data integrity, and support future scalability.

The system manages customers, laboratories, laboratory equipment, maintenance operations, service reports, user accounts, notifications, and audit logs. The design also considers future integration with the Knowledge Base and QR Code Documentation System.

---

# Database Tables

## 1. Roles

The **Roles** table defines the different permission levels available within the system. Each user is assigned one role that determines which modules and actions they are allowed to access.

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| role_name | String | Name of the role |
| description | Text | Description of the role |

---

## 2. Users

The **Users** table stores all authenticated users of the system, including administrators, managers, engineers, and technicians.

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| first_name | String | User's first name |
| last_name | String | User's last name |
| email | String | Login email address |
| password_hash | String | Encrypted password |
| phone | String | Contact number |
| role_id | Integer | References Roles table |
| is_active | Boolean | Indicates whether the account is active |
| created_at | Timestamp | Account creation date |
| updated_at | Timestamp | Last modification date |

---

## 3. Customers

The **Customers** table stores organizations that own laboratory equipment. Examples include hospitals, universities, research centers, and private laboratories.

Each customer may own multiple laboratories.

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| company_name | String | Customer organization |
| contact_person | String | Main contact person |
| phone | String | Phone number |
| email | String | Email address |
| address | Text | Street address |
| city | String | City |
| country | String | Country |
| postal_code | String | Postal code |
| notes | Text | Additional notes |
| created_at | Timestamp | Creation date |
| updated_at | Timestamp | Last update |

---

## 4. Laboratories

The **Laboratories** table stores individual laboratories or departments that belong to a customer.

Separating laboratories into their own table improves database normalization, eliminates duplicate information, and allows future expansion without modifying equipment records.

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| customer_id | Integer | References Customers table |
| name | String | Laboratory name |
| building | String | Building name |
| floor | String | Floor number |
| room | String | Room number |
| description | Text | Additional information |
| created_at | Timestamp | Creation date |
| updated_at | Timestamp | Last update |

---

## 5. Equipment

The **Equipment** table stores every laboratory instrument managed by the system.

Each piece of equipment belongs to one laboratory and contains complete lifecycle information including warranty, calibration schedule, and operational status.

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| laboratory_id | Integer | References Laboratories table |
| asset_tag | String | Internal asset number |
| serial_number | String | Manufacturer serial number |
| name | String | Equipment name |
| manufacturer | String | Manufacturer |
| model | String | Model number |
| category | String | Equipment category |
| location | String | Shelf or exact location |
| purchase_date | Date | Purchase date |
| installation_date | Date | Installation date |
| warranty_expiry | Date | Warranty expiration |
| calibration_due | Date | Next calibration date |
| status | String | Active, Maintenance, Retired, Out of Service |
| notes | Text | Additional remarks |
| created_at | Timestamp | Creation date |
| updated_at | Timestamp | Last update |

---

## 6. Maintenance

The **Maintenance** table stores both preventive and corrective maintenance performed on laboratory equipment.

Every maintenance record belongs to one piece of equipment and is assigned to one engineer.

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| equipment_id | Integer | References Equipment table |
| engineer_id | Integer | References Users table |
| maintenance_type | String | Preventive or Corrective |
| scheduled_date | Date | Scheduled maintenance date |
| started_at | Timestamp | Maintenance start |
| completed_at | Timestamp | Maintenance completion |
| priority | String | Low, Medium, High |
| status | String | Pending, In Progress, Completed |
| description | Text | Maintenance description |
| remarks | Text | Engineer remarks |
| next_due | Date | Next scheduled maintenance |
| created_at | Timestamp | Creation date |

---

## 7. Service Reports

The **Service Reports** table stores reports generated after maintenance has been completed.

These reports provide a permanent service history for each instrument.

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| maintenance_id | Integer | References Maintenance table |
| report_number | String | Unique report number |
| summary | Text | Summary of maintenance |
| work_performed | Text | Work completed |
| parts_replaced | Text | Components replaced |
| recommendations | Text | Future recommendations |
| pdf_path | String | Generated PDF file location |
| created_at | Timestamp | Report creation date |

---

## 8. Activity Logs

The **Activity Logs** table records important user actions throughout the system for auditing and security purposes.

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | References Users table |
| action | String | Description of action |
| timestamp | Timestamp | Time of action |
| ip_address | String | User IP address |

---

## 9. Notifications

The **Notifications** table stores reminders and alerts generated by the system, such as upcoming maintenance schedules or important system events.

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | References Users table |
| title | String | Notification title |
| message | Text | Notification message |
| is_read | Boolean | Read status |
| created_at | Timestamp | Creation date |

---

# Database Relationships

The system follows a relational database structure.

- One **Role** can be assigned to many **Users**.
- One **Customer** can own many **Laboratories**.
- One **Laboratory** can contain many **Equipment** records.
- One **Equipment** record can have many **Maintenance** records.
- One **Maintenance** record generates one **Service Report**.
- One **User** can perform many **Maintenance** tasks.
- One **User** can generate many **Activity Logs**.
- One **User** can receive many **Notifications**.

---

# Database Design Principles

The database has been designed according to the following principles:

- Database normalization to reduce duplicate data.
- Foreign key relationships to maintain referential integrity.
- Primary key indexing for efficient data retrieval.
- Scalability to support future system expansion.
- Auditability through activity logging.
- Security through proper user-role relationships.
- Support for future QR Code Documentation integration.
- Support for future Knowledge Base integration.

This database structure provides a scalable, maintainable, and enterprise-ready foundation for the Laboratory Equipment Management System.