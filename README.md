# Veterinary Patient Management API

A FastAPI-based REST API for managing veterinary clinic records, including Owners, Pets, Visits, and User Authentication.

## Features

- User Registration and Login
- JWT Authentication
- Protected Routes
- Owners CRUD Operations
- Pets CRUD Operations
- Visits CRUD Operations
- Pagination
- Filtering
- Soft Delete Support
- Request Logging
- Global Exception Handling
- PostgreSQL Database
- Alembic Migrations

## Tech Stack

- FastAPI
- PostgreSQL (Neon)
- SQLAlchemy ORM
- Alembic
- Pydantic
- JWT Authentication
- Passlib (Password Hashing)
- Uvicorn

## Project Structure
```text
project/
│
├── alembic/
├── models/
├── routers/
├── schemas/
├── utils/
├── config.py
├── database.py
├── main.py
├── .env
└── README.md
```
## Environment Variables
```text
Create a .env file:

DATABASE_URL=your_database_url
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
## Installation
```bash
git clone <repository-url>

cd project

uv sync
```
## Database Migration

Generate migration:
```bash
uv run alembic revision --autogenerate -m "message"
```
Apply migration:
```bash
uv run alembic upgrade head
```
## Running the Application
```bash
uv run uvicorn main:app --reload
```
Swagger Documentation:

http://127.0.0.1:8000/docs

## Authentication Flow

1. Register a user.
2. Login using email and password.
3. Receive JWT access token.
4. Authorize using Swagger UI.
5. Access protected endpoints.

## API Endpoints

### Authentication

- POST /auth/register
- POST /auth/login
- GET /auth/user-context

## Owners

- POST /owners
- GET /owners
- GET /owners/{id}
- PUT /owners/{id}
- DELETE /owners/{id}

## Pets

- POST /pets
- GET /pets
- GET /pets/{id}
- PUT /pets/{id}
- DELETE /pets/{id}

## Visits

- POST /visits
- GET /visits
- GET /visits/{id}
- PUT /visits/{id}
- DELETE /visits/{id}

## Logging

Request logs include:

- HTTP Method
- Endpoint
- Response Status Code
- Response Time

## Exception Handling

Standard error format:
```json
{
  "success": false,
  "message": "Error message"
}
```