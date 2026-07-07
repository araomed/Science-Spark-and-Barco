# Science Spark & Barco

## Laboratory Equipment Management System

A web-based Laboratory Equipment Management System built with FastAPI and PostgreSQL, developed as part of an internship project at Barco Al-Iraq.

The system centralizes how laboratory equipment, customers, lab locations, and maintenance activity are tracked, laying the foundation for service reporting and role-based user management as the project grows.

---

## Developers

- Ara Omed Mardan
- Maad Kamal Mawlod

---

## Tech Stack

| Layer          | Technology                     |
|----------------|---------------------------------|
| Backend        | Python, FastAPI                |
| ORM / Database | SQLAlchemy, PostgreSQL         |
| Validation     | Pydantic v2                     |
| Server         | Uvicorn                        |
| Frontend       | React, Bootstrap 5 (planned)   |
| Version Control| Git, GitHub                    |

---

## Features

- RESTful API built with FastAPI
- PostgreSQL database using SQLAlchemy ORM
- Customer management
- Laboratory management
- Equipment asset management
- Preventive and corrective maintenance tracking
- Equipment-to-laboratory relationships
- Maintenance history per equipment
- Automatic request validation using Pydantic
- Swagger/OpenAPI interactive API documentation
- Modular architecture following industry-standard FastAPI practices

---

## Project Structure

```
app/
├── auth/            JWT & OAuth2 handling (scaffolded, not yet implemented)
├── core/             App config & security helpers (scaffolded)
├── crud/             Database operations per entity
├── models/           SQLAlchemy ORM models
├── routers/          API route definitions
├── schemas/          Pydantic request/response schemas
├── services/         Email, PDF, and notification services (scaffolded)
├── utils/            Shared constants & helpers
├── database.py       DB engine, session, and Base setup
└── main.py           FastAPI app entrypoint

documentation/
├── API.md
├── Architecture.md
├── Database.md
├── Deployment.md
├── SRS.md
├── Security.md
├── Timeline.md
└── diagrams/         Architecture, ERD, Roles, and Workflow diagrams (.drawio)

scripts/
└── migrate_equipment_table.py   One-off column/constraint migration for the equipment table
```

---

## Current Status

### Implemented
- **Equipment** — full CRUD (`/equipment`), linked to a laboratory, with unique `serial_number`/`asset_tag` enforcement, warranty/purchase date validation, and maintenance-interval tracking fields
- **Maintenance** — full CRUD (`/maintenance`), linked to a piece of equipment, with a constrained status field (`scheduled`, `completed`, `cancelled`, `overdue`), cost tracking, and a lookup of maintenance history per equipment
- **Laboratories** — full CRUD (`/laboratories`), linked to a customer via `customer_id`
- **Customers** — full CRUD (`/customers`)
- PostgreSQL connection via SQLAlchemy, with environment-based config (`.env`)

### Scaffolded (folders/files exist, logic not yet written)
- User accounts (`app/models/user.py` has the table defined; `app/crud/crud_user.py`, `app/schemas/user.py`, and `app/routers/users.py` are empty)
- Roles (`app/models/role.py` is defined; `app/crud/crud_role.py`, `app/schemas/role.py`, and `app/routers/roles.py` are empty)
- Role-based access control & JWT authentication (`app/auth/`, `app/core/security.py` are empty)
- Service reports (`app/schemas/service_report.py`, `app/models/service_report.py`, and `app/routers/reports.py` are empty)
- Notifications, activity log (`app/models/notification.py`, `app/models/activity_log.py` are empty)
- Email, notification, and PDF services (`app/services/*.py` are empty)

See **Roadmap** below for the full list of what's planned next.

---

## Database Relationships

```
Customer
│
└── Laboratory
        │
        └── Equipment
                │
                └── Maintenance
```

- One **Customer** can have many **Laboratories**.
- One **Laboratory** can contain many **Equipment** assets.
- One **Equipment** asset can have many **Maintenance** records.
- Every **Maintenance** record belongs to exactly one **Equipment** asset.

---

## API Overview

| Resource     | Endpoints |
|--------------|-----------|
| Equipment    | `GET /equipment` (optional `?laboratory_id=`), `GET /equipment/{id}`, `POST /equipment`, `PUT /equipment/{id}`, `DELETE /equipment/{id}` |
| Maintenance  | `GET /maintenance`, `GET /maintenance/{id}`, `GET /maintenance/equipment/{equipment_id}`, `POST /maintenance`, `PUT /maintenance/{id}`, `DELETE /maintenance/{id}` |
| Laboratories | `GET /laboratories`, `GET /laboratories/{id}`, `POST /laboratories`, `PUT /laboratories/{id}`, `DELETE /laboratories/{id}` |
| Customers    | `GET /customers`, `GET /customers/{id}`, `POST /customers`, `PUT /customers/{id}`, `DELETE /customers/{id}` |

Full interactive docs are available at `/docs` (Swagger UI) once the server is running.

---

## Data Validation

The API validates incoming data before it reaches the database. Current validation includes:

- Duplicate equipment serial numbers are rejected.
- Duplicate asset tags are rejected.
- Warranty expiry cannot be earlier than purchase date.
- Maintenance due date cannot be earlier than performed date.
- Maintenance status is restricted to:
  - `scheduled`
  - `completed`
  - `cancelled`
  - `overdue`
- Equipment must belong to an existing laboratory.
- Maintenance records must belong to an existing equipment item.
- Laboratory records must belong to an existing customer.

Status restrictions are enforced at both the Pydantic layer (`Literal` types) and the database layer (`CheckConstraint`), so an invalid status can't slip in even via a direct DB write.

---

## Example Equipment Record

```json
{
  "laboratory_id": 1,
  "category": "Microscope",
  "name": "Olympus CX23",
  "manufacturer": "Olympus",
  "model": "CX23",
  "serial_number": "CX23-2026-001",
  "asset_tag": "SS-0009",
  "purchase_date": "2026-07-07",
  "warranty_expiry": "2029-07-07",
  "maintenance_interval_months": 6,
  "next_maintenance_due": "2027-01-07",
  "status": "active"
}
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL installed and running

### 1. Clone the repo
```bash
git clone https://github.com/araomed/Science-Spark-and-Barco.git
cd Science-Spark-and-Barco
```

### 2. Set up a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # on macOS/Linux: source venv/bin/activate
```

### 3. Install dependencies
`requirements.txt` is currently empty in the repo — until it's populated (see **Known Gaps** below), install directly:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
```

### 5. Set up the database
The app calls `Base.metadata.create_all(bind=engine)` on startup, so tables for the four implemented modules (equipment, maintenance, laboratories, customers) are created automatically the first time you run it.

If you have an **older database created before the equipment table gained its new columns** (`laboratory_id`, `category`, `asset_tag`, `purchase_date`, `warranty_expiry`, `maintenance_interval_months`, `next_maintenance_due`, `status`), run the one-off migration script instead of dropping your data:
```bash
python scripts/migrate_equipment_table.py
```
This backfills sane defaults for existing rows and adds the missing constraints. It expects at least one laboratory row to exist already, since every piece of equipment must belong to one.

### 6. Run the server
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

---

## Known Gaps

- **`requirements.txt` is empty.** Populate it (`pip freeze > requirements.txt` from a working venv) so the install step above isn't manual.
- **No authentication is wired in yet.** `app/auth/` and `app/core/security.py` exist but contain no code, and none of the current routers require a logged-in user. Every endpoint is open right now.
- **Users and Roles have models but no API.** The `User` and `Role` tables are defined, but there's no way to create a user, log in, or assign a role through the API yet — `crud_user.py`, `crud_role.py`, `schemas/user.py`, `schemas/role.py`, `routers/users.py`, and `routers/roles.py` are all empty stubs.
- **No Alembic migrations.** Schema changes so far have been handled either by `create_all` (for new tables) or by the manual `scripts/migrate_equipment_table.py` script (for altering an existing table). This works for now but won't scale as more columns/tables change.
- **Service reports, notifications, and PDF generation are unbuilt.** The relevant model, schema, router, and service files exist as empty placeholders only.

---

## Roadmap

Planned improvements include:

- JWT Authentication
- Role-Based Access Control (RBAC)
- User Management
- Service Report Module
- Notification System
- Email Integration
- PDF Report Generation
- QR Code Equipment Labels
- React + Bootstrap Dashboard
- Analytics Dashboard
- Audit Logging
- Alembic Database Migrations
- Internal Knowledge Base

---

## Documentation

Detailed design and planning docs live in `/documentation`:
- `SRS.md` — Software Requirements Specification
- `Architecture.md` — System architecture overview
- `Database.md` — Database design
- `API.md` — API reference
- `Security.md` — Security considerations
- `Deployment.md` — Deployment notes
- `Timeline.md` — Project timeline
- `diagrams/` — ERD, architecture, roles, and workflow diagrams (`.drawio`)

---

## License

This project was developed as part of an internship project at Barco Al-Iraq and Science Spark. It is intended for educational and portfolio purposes.

---

## Acknowledgements

Developed during the Barco Al-Iraq and Science Spark internship project. Special thanks to the mentors and supervisors who provided guidance throughout the development of the system.
