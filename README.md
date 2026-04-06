# Finance Data Processing and Access Control Backend

A FastAPI-based backend system for managing financial records with role-based access control, user management, and dashboard analytics.

**Submission Date:** April 6, 2026  
**Status:** Complete  
**Demo:** In-memory storage (documented assumption per assignment guidelines)

---

## Quick Start

### Prerequisites

- Python 3.9+
- pip

### Installation & Setup

```bash
cd finance-backend
uv sync
uv run uvicorn main:app --reload
```

Server runs on http://localhost:8000  
API docs: http://localhost:8000/docs

---

## Architecture Overview

```
models/
├── transaction.py     # Pydantic models for transactions
└── user.py            # Pydantic models for users

repositories/
├── transaction_repo.py  # In-memory transaction CRUD
└── user_repo.py        # In-memory user CRUD

services/
├── transaction_service.py  # Business logic + access control
└── user_service.py        # User management + access control

main.py               # FastAPI app + route handlers
```

### Design Principles

- **Separation of Concerns:** Models → Repositories → Services → Routes
- **Role-Based Access Control:** Enforced at service layer
- **Validation:** Pydantic models ensure data integrity
- **Error Handling:** Proper HTTP status codes (403 Forbidden, 404 Not Found, 422 Validation Error)

---

## Authentication & Authorization

### Header-Based Role System

Pass user role via HTTP header: `X-User-Role`

Example:

```bash
curl -H "X-User-Role: admin" http://localhost:8000/...
```

### Supported Roles

| Role    | Permissions                               |
| ------- | ----------------------------------------- |
| Viewer  | ✓ View transactions & dashboard           |
| Analyst | ✓ View + Create/Update transactions, View |
| Admin   | ✓ Full access: create/update/delete users |

### Access Control Rules

```
User Management:
  - POST   /users                 → Admin only
  - GET    /users                 → Admin only
  - GET    /users/{id}            → All authenticated roles
  - PUT    /users/{id}/status     → Admin only

Transaction Management:
  - POST   /transactions          → Admin, Analyst
  - GET    /transactions          → All authenticated roles
  - GET    /transactions/{id}     → All authenticated roles
  - PUT    /transactions/{id}     → Admin, Analyst
  - DELETE /transactions/{id}     → Admin only

Dashboard:
  - GET    /dashboard/summary     → All authenticated roles
```

---

## API Endpoints

### Users

#### Create User (Admin only)

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -H "X-User-Role: admin" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "role": "analyst"
  }'
```

Response (201 OK):

```json
{
  "user_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "analyst",
  "status": "active",
  "created_at": "2026-04-06T12:00:00"
}
```

#### Get All Users (Admin only)

```bash
curl -H "X-User-Role: admin" http://localhost:8000/users
```

#### Get Specific User

```bash
curl -H "X-User-Role: analyst" http://localhost:8000/users/1
```

#### Update User Status (Admin only)

```bash
curl -X PUT http://localhost:8000/users/1/status \
  -H "Content-Type: application/json" \
  -H "X-User-Role: admin" \
  -d '{"status": "inactive"}'
```

---

## Architecture Overview

```
models/
├── transaction.py     # Pydantic models for transactions
└── user.py            # Pydantic models for users

repositories/
├── transaction_repo.py  # In-memory transaction CRUD
└── user_repo.py        # In-memory user CRUD

services/
├── transaction_service.py  # Business logic + access control
└── user_service.py        # User management + access control

main.py               # FastAPI app & routes
```

### Design Principles
- **Separation of Concerns:** Models → Repositories → Services → Routes
- **Role-Based Access Control:** Enforced at service layer
- **Validation:** Pydantic models ensure data integrity
- **Error Handling:** Proper HTTP status codes (403 Forbidden, 404 Not Found, 422 Validation Error)

---

## Authentication & Authorization

### Header-Based Role System
Pass user role via HTTP header: `X-User-Role`

**Example:**
```bash
curl -H "X-User-Role: admin" http://localhost:8000/...
```

### Supported Roles
| Role | Permissions |
|------|------------|
| **Viewer** | ✓ View transactions & dashboard |
| **Analyst** | ✓ View + Create/Update transactions, View dashboard |
| **Admin** | ✓ Full access: create/update/delete users & transactions |

### Access Control Rules
```
User Management:
  - POST   /users                 → Admin only
  - GET    /users                 → Admin only
  - GET    /users/{id}            → All authenticated roles
  - PUT    /users/{id}/status     → Admin only

Transaction Management:
  - POST   /transactions          → Admin, Analyst
  - GET    /transactions          → All authenticated roles
  - GET    /transactions/{id}     → All authenticated roles
  - PUT    /transactions/{id}     → Admin, Analyst
  - DELETE /transactions/{id}     → Admin only

Dashboard:
  - GET    /dashboard/summary     → All authenticated roles
```

---

## API Endpoints

### Users

#### Create User (Admin only)
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -H "X-User-Role: admin" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "role": "analyst"
  }'
```
**Response (201 OK):**
```json
{
  "user_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "analyst",
  "status": "active",
  "created_at": "2026-04-06T12:00:00"
}
```

#### Get All Users (Admin only)
```bash
curl -H "X-User-Role: admin" http://localhost:8000/users
```

#### Get Specific User
```bash
curl -H "X-User-Role: analyst" http://localhost:8000/users/1
```

#### Update User Status (Admin only)
```bash
curl -X PUT http://localhost:8000/users/1/status \
  -H "Content-Type: application/json" \
  -H "X-User-Role: admin" \
  -d '{"status": "inactive"}'
```

---

### Transactions

#### Create Transaction (Admin, Analyst only)

```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -H "X-User-Role: analyst" \
  -d '{
    "amount": 1500.50,
    "type": "income",
    "category": "Salary",
    "description": "Monthly salary"
  }'
```

Response (201 OK):

```json
{
  "id": 1,
  "amount": 1500.50,
  "type": "income",
  "category": "Salary",
  "description": "Monthly salary",
  "date": "2026-04-06T12:00:00"
}
```

#### Get All Transactions

```bash
curl -H "X-User-Role: viewer" http://localhost:8000/transactions
```

#### Filter Transactions

By category:

```bash
curl -H "X-User-Role: viewer" "http://localhost:8000/transactions?category=Salary"
```

By type:

```bash
curl -H "X-User-Role: viewer" "http://localhost:8000/transactions?type=income"
```

By date range:

```bash
curl -H "X-User-Role: viewer" \
  "http://localhost:8000/transactions?start_date=2026-04-01T00:00:00&end_date=2026-04-06T23:59:59"
```

Multiple filters:

```bash
curl -H "X-User-Role: viewer" \
  "http://localhost:8000/transactions?category=Salary&type=income"
```

#### Get Specific Transaction

```bash
curl -H "X-User-Role: viewer" http://localhost:8000/transactions/1
```

#### Update Transaction (Admin, Analyst only)

```bash
curl -X PUT http://localhost:8000/transactions/1 \
  -H "Content-Type: application/json" \
  -H "X-User-Role: admin" \
  -d '{
    "amount": 1600.00,
    "type": "income",
    "category": "Bonus",
    "description": "Performance bonus"
  }'
```

#### Delete Transaction (Admin only)

```bash
curl -X DELETE http://localhost:8000/transactions/1 \
  -H "X-User-Role: admin"
```

Response:

```json
{
  "message": "Transaction deleted successfully",
  "deleted": {
    "id": 1,
    "amount": 1500.50
  }
}
```

---

### Dashboard

#### Get Summary Analytics

```bash
curl -H "X-User-Role: viewer" http://localhost:8000/dashboard/summary
```

Response:

```json
{
  "total_income": 5000.00,
  "total_expense": 1200.50,
  "net_balance": 3799.50,
  "category_totals": {
    "Salary": 5000.00,
    "Food": 250.50,
    "Transport": 950.00
  },
  "transaction_count": 4
}
```

---

## Validation & Error Handling

### Input Validation Examples

#### Invalid Amount (must be > 0)

```bash
curl -X POST http://localhost:8000/transactions \
  -H "X-User-Role: admin" \
  -d '{"amount": -100, "type": "income", "category": "Test"}'
```

Response (422 Unprocessable Entity):

```json
{
  "detail": [
    {
      "loc": ["body", "amount"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

#### Invalid Type

```bash
curl -X POST http://localhost:8000/transactions \
  -d '{"amount": 100, "type": "invalid", "category": "Test"}'
```

Response (422): Type must be "income" or "expense"

#### Unauthorized Access

```bash
curl -X POST http://localhost:8000/transactions \
  -H "X-User-Role: viewer" \
  -d '{"amount": 100, "type": "income", "category": "Test"}'
```

Response (403 Forbidden):

```json
{
  "detail": "Not authorized to create transactions"
}
```

#### Not Found

```bash
curl -H "X-User-Role: admin" http://localhost:8000/transactions/9999
```

Response (404 Not Found):

```json
{
  "detail": "Transaction not found"
}
```

---

## Data Model

### Transaction

```python
{
  "id": int,                 # Auto-generated
  "amount": float,           # Must be > 0
  "type": "income"|"expense",
  "category": str,           # Required, min 1 char
  "description": str | null, # Optional, max 255 chars
  "date": datetime           # ISO format, defaults to now
}
```

### User

```python
{
  "user_id": int,                    # Auto-generated
  "name": str,                       # 1-100 chars
  "email": str,                      # Valid email format
  "role": "viewer"|"analyst"|"admin",
  "status": "active"|"inactive",     # Default: active
  "created_at": datetime             # ISO format
}
```

---

## Assumptions & Design Decisions

### 1. In-Memory Storage

- ✅ Per assignment: "in-memory OK if documented"
- Data persists during server runtime
- Resets when server restarts
- Trade-off: Fast development vs. persistence

### 2. Header-Based Authentication

- Simple mock auth via `X-User-Role` header (no JWT/session complexity)
- Per assignment: "mock authentication... local development setup"
- Trade-off: Easy to test vs. not production-secure

### 3. No User Login System

- Role passed directly via header
- Suitable for local/demo environment
- Production would use JWT tokens

### 4. Datetime Handling

- Stored as ISO 8601 strings for JSON compatibility
- Timestamps in UTC

### 5. Soft Deletes Not Implemented

- Hard delete for simplicity, aligns with CRUD requirements
- Can be added later with `deleted_at` field

---

## Testing with cURL

### Full Test Scenario

1. Create Users

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -H "X-User-Role: admin" \
  -d '{"name":"Admin User","email":"admin@example.com","role":"admin"}'

curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -H "X-User-Role: admin" \
  -d '{"name":"Analyst User","email":"analyst@example.com","role":"analyst"}'

curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -H "X-User-Role: admin" \
  -d '{"name":"Viewer User","email":"viewer@example.com","role":"viewer"}'
```

2. Create Transactions (as Analyst)

```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -H "X-User-Role: analyst" \
  -d '{"amount":5000,"type":"income","category":"Salary"}'

curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -H "X-User-Role: analyst" \
  -d '{"amount":200,"type":"expense","category":"Food"}'
```

3. View Transactions (all roles)

```bash
curl -H "X-User-Role: viewer" http://localhost:8000/transactions
```

4. View Dashboard (Viewer can see)

```bash
curl -H "X-User-Role: viewer" http://localhost:8000/dashboard/summary
```

5. Test Access Control (Viewer cannot create)

```bash
curl -X POST http://localhost:8000/transactions \
  -H "X-User-Role: viewer" \
  -d '{"amount":100,"type":"income","category":"Test"}'
```

Expected: 403 Forbidden

6. Delete Transaction (Admin only)

```bash
curl -X DELETE http://localhost:8000/transactions/1 \
  -H "X-User-Role: admin"
```

---

## Features Implemented

### Core Requirements ✅

- ✓ User and Role Management (Create, Get, Update status, Assign roles)
- ✓ Financial Records CRUD (Create, Read, Update, Delete, Filtering)
- ✓ Dashboard Summary APIs (Totals, Category breakdown, Transaction count)
- ✓ Access Control Logic (Role-based, enforced at service layer)
- ✓ Validation and Error Handling (Pydantic models, proper status codes)
- ✓ Data Persistence (In-memory with documented approach)

### Optional Enhancements ✅

- ✓ Filtering (by category, type, date range)
- ✓ API Documentation (FastAPI auto-docs at `/docs`)
- ✓ Comprehensive README with examples and assumptions

---

## File Structure

```
finance-backend/
├── main.py                      # FastAPI app & routes
├── models/
│   ├── transaction.py          # Transaction Pydantic model
│   └── user.py                 # User Pydantic model
├── repositories/
│   ├── transaction_repo.py     # Transaction CRUD operations
│   └── user_repo.py            # User CRUD operations
├── services/
│   ├── transaction_service.py  # Transaction business logic
│   └── user_service.py         # User business logic
├── README.md                   # This file
└── pyproject.toml              # Project dependencies
```

---

## Next Steps (Future Enhancements)

If time/scope allowed:

- SQLite persistence (`.db` file storage)
- JWT token authentication
- Pagination for large record sets
- Rate limiting
- Unit tests (pytest)
- API documentation (Swagger/OpenAPI)
- Soft deletes with `deleted_at` timestamp
- Transaction tags/labels
- Monthly/weekly trend analytics
- Email validation for users

---

## Submission Notes

What This Submission Demonstrates:

- Have implemented clean separation of concerns (models → repos → services → routes)
- Role-based access control at the service layer
- Comprehensive input validation with Pydantic
- Proper REST API design with correct status codes
- Clear business logic for financial operations
- Scalable architecture (easy to swap in-memory for DB)

Trade-offs Made:

- In-memory storage chosen for simplicity (fully documented)
- Mock header auth chosen for ease of testing (In production would use JWT)
- Hard deletes chosen for CRUD simplicity



---

## Questions?

Refer to test examples in "Testing with cURL" section above.

For API specification, run server and visit `http://localhost:8000/docs` for interactive Swagger UI.

---

**Assignment:** Finance Data Processing and Access Control Backend  
**Submitted By:** Sarvesh Bhattacharyya  
**Date:** April 6, 2026  
**Status:** ✅ Complete
