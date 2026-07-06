# Science Spark & Barco

## Laboratory Equipment Management System

A web-based Laboratory Equipment Management System built with FastAPI and PostgreSQL, developed as part of an internship project at Barco Al-Iraq.

The system centralizes how laboratory equipment, customers, and lab locations are tracked, laying the foundation for maintenance scheduling, service reporting, and role-based user management as the project grows.

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
| Validation     | Pydantic                       |
| Server         | Uvicorn                        |
| Frontend       | React, Bootstrap 5 (planned)   |
| Version Control| Git, GitHub                    |

---

## Project Structure

app/
- auth/            JWT & OAuth2 handling (scaffolded, not yet implemented)
- core/            App config & security helpers (scaffolded)
- crud/            Database operations per entity
- models/          SQLAlchemy ORM models
- routers/         API route definitions
- schemas/         Pydantic request/response schemas
- services/        Email, PDF, and notification services (scaffolded)
- utils/           Shared constants & helpers (scaffolded)
- database.py      DB engine, session, and Base setup
- main.py          FastAPI app entrypoint

documentation/
- API.md
- Architecture.md
- Database.md
- Deployment.md
- SRS.md
- Security.md
- Timeline.md
- diagrams/         Architecture, ERD, Roles, and Workflow diagrams

---

## Current Status

### Implemented
- Equipment: full CRUD (/equipment)
- Customers: full CRUD (/customers)
- Laboratories: full CRUD, linked to a customer via customer_id (/laboratories)
- PostgreSQL connection via SQLAlchemy, with environment-based config (.env)

### Scaffolded (folders/files exist, logic not yet written)
- User accounts & role-based access control
- JWT authentication (app/auth)
- Maintenance scheduling & service reports
- Notifications & email service
- PDF report generation

### Planned
- React + Bootstrap frontend
- Internal Knowledge Base
- QR Code-based equipment documentation

---

## API Overview

| Resource     | Endpoints |
|--------------|-----------|
| Equipment    | GET /equipment, GET /equipment/{id}, POST /equipment, PUT /equipment/{id}, DELETE /equipment/{id} |
| Customers    | GET /customers, GET /customers/{id}, POST /customers, PUT /customers/{id}, DELETE /customers/{id} |
| Laboratories | GET /laboratories, GET /laboratories/{id}, POST /laboratories, PUT /laboratories/{id}, DELETE /laboratories/{id} |

Each laboratory must reference an existing customer_id; the API returns a 404 if the customer doesn't exist.

Full interactive docs are available at /docs (Swagger UI) once the server is running.

---

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL installed and running

### 1. Clone the repo
git clone https://github.com/araomed/Science-Spark-and-Barco.git
cd Science-Spark-and-Barco

### 2. Set up a virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv

### 4. Configure environment variables

Create a .env file in the project root:
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>

### 5. Run the server
uvicorn app.main:app --reload

The API will be available at http://127.0.0.1:8000, with interactive docs at http://127.0.0.1:8000/docs.

---

## Documentation

Detailed design and planning docs live in /documentation:
- SRS.md: Software Requirements Specification
- Architecture.md: System architecture overview
- Database.md: Database design
- API.md: API reference
- Security.md: Security considerations
- Deployment.md: Deployment notes
- Timeline.md: Project timeline
- diagrams/: ERD, architecture, roles, and workflow diagrams (.drawio)