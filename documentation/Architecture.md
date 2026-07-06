# System Architecture

## Overview

The Laboratory Equipment Management System follows a **three-tier architecture**, separating the application into three independent layers:

```
Frontend
        │
        ▼
 FastAPI REST API
        │
        ▼
 PostgreSQL Database
```

The frontend communicates with the backend through REST APIs over HTTP/HTTPS. The FastAPI backend handles all business logic, authentication, data validation, and communication with the PostgreSQL database. This layered architecture improves maintainability, scalability, security, and allows each layer to be developed and updated independently.

---

## Frontend

### Planned Technologies

- React
- Bootstrap 5
- HTML5
- CSS3

### Responsibilities

- User Interface
- Forms and Data Entry
- Dashboard
- Reports and Analytics
- Authentication Pages
- Responsive Design for Desktop and Mobile

### Reason for Selection

React provides a modern, component-based architecture that makes the application easier to maintain and expand. Bootstrap accelerates UI development while ensuring responsiveness across different screen sizes.

---

## Backend

### Technologies

- FastAPI
- SQLAlchemy
- Pydantic

### Responsibilities

- Business Logic
- Authentication & Authorization
- CRUD Operations
- REST API Development
- Reporting
- Notifications
- File Handling
- Database Communication

### Reason for Selection

FastAPI was selected because of its high performance, automatic API documentation (Swagger/OpenAPI), asynchronous support, and excellent integration with Python. SQLAlchemy simplifies database management through ORM, while Pydantic provides automatic request validation and data serialization.

---

## Database

### Technology

- PostgreSQL

### Responsibilities

- Store Users
- Store Customers
- Store Equipment
- Store Maintenance Records
- Store Service Reports
- Store Activity Logs
- Maintain Data Relationships and Integrity

### Reason for Selection

PostgreSQL is a powerful open-source relational database known for its reliability, security, scalability, and excellent support for complex relationships and transactions, making it well suited for enterprise-level applications.

---

## Authentication & Authorization

### Authentication Method

- JWT (JSON Web Tokens)

### Authorization Model

Role-Based Access Control (RBAC)

### System Roles

- Administrator
- Manager
- Engineer
- Technician

### Purpose

The RBAC model ensures that every user only has access to the features and data required for their role, improving security and simplifying permission management.

---

## API Architecture

The backend exposes RESTful API endpoints that allow secure communication between the frontend and the database.

Example endpoints include:

- User Management
- Customer Management
- Equipment Management
- Maintenance Management
- Service Reports
- Dashboard Analytics

All API endpoints will exchange data using JSON.

---

## Future Integration

The architecture is designed to support future expansion without major redesign.

### Phase 2

- Internal Knowledge Base System

### Phase 3

- QR Code Documentation System

The modular architecture allows these systems to integrate with the existing backend through additional API modules while sharing the same authentication and database infrastructure.

---

## Scalability Considerations

The system is designed with scalability in mind by:

- Separating frontend, backend, and database layers
- Using REST APIs for communication
- Organizing backend modules by feature
- Supporting future cloud deployment
- Allowing additional services and modules to be integrated without affecting existing functionality

This design ensures the application remains maintainable, extensible, and suitable for future enterprise-level expansion.