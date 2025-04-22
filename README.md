# 🧰 Unix-Inspired Task Manager API (FastAPI)

A Unix-style task manager API built using FastAPI. It features JWT-based authentication and role-based access control for managing tasks.

## Technologies Used

* Python 3.10+
* FastAPI
* Uvicorn (ASGI Server)
* Python-JOSE for JWT handling
* Pydantic for data validation
* PostgresSQL

## Features

- JWT Authentication with OAuth2
- Role-Based Authorization
- 'admin': Can create, read, update, delete
- 'readonly': Can only list and view tasks
- Simple PostgreSQL-backed task store (mocked using `queries`)
- Well-structured FastAPI app

## User Roles

* Role	Permissions
* admin	Full access (CRUD)
* readonly	Read-only access (GET routes)

## API Endpoints 

URL: http://local-host:8000

POST /token
Authenticates user and returns JWT

GET /tasks
Lists all tasks

Roles: admin, readonly

GET /tasks/{id}
Fetch a task by ID

Roles: admin, readonly

POST /tasks
Create a new task

Roles: admin

PUT /tasks/{id}
Update an existing task

Roles: admin

DELETE /tasks/{id}
Delete a task by ID

Roles: admin

## How to Run

```bash
* pip install -r requirements.txt
* uvicorn app.main:app --reload

## create the virula Env
* python -m venv venv
* .\venv\Scripts\activate
* python -m pip install --upgrade pip
* pip install -r requirements.txt
* pip install -e .

### Pytest Commands

* pytest -k filename
* pip install pytest 
* pip install coverage
* coverage run -m pytest
* coverage report
* coverage html
* htmlcov/index.html

## Demo