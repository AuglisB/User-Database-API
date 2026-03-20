# User Database API

A backend-focused Python project that started as a command-line user database and evolved into a modular Flask REST API.

This application stores user records, supports admin authentication with JWT, performs CRUD operations against a SQLite database, and includes export, logging, backup, and JSON-to-SQLite migration utilities.

## What this project does

The project manages a simple user database where each user record contains:

- `id`
- `name`
- `age`
- `color`
- `game`
- `country`

It provides two main ways to work with the data:

1. **Command-line application** via `main.py`
2. **REST API** via `api.py`

The backend API is the main portfolio-ready part of the project.

## Features

- Flask REST API
- SQLite database storage
- JWT-based admin authentication
- Role-based access checks for protected routes
- User CRUD operations
- Filtering and pagination for user listings
- JSON export and backup utilities for the CLI version
- Logging to a local log file
- Migration script from JSON storage to SQLite

## Project structure

```text
.
├── api.py
├── auth_service.py
├── config.py
├── database_service.py
├── file_service.py
├── logging_service.py
├── main.py
├── migrate_json_to_sqlite.py
├── user_service.py
├── requirements.txt
├── .gitignore
├── data/
├── exports/
├── backups/
└── logs/
```

## How it works

### 1. Configuration

`config.py` loads environment variables with `python-dotenv` and builds the main file paths used by the app, including the database, export, backup, and JSON data locations.

The project expects these environment variables:

- `API_KEY`
- `JWT_SECRET`

`JWT_SECRET` is used to sign and verify JWT tokens. `API_KEY` is loaded by the app configuration even though it is not currently enforced in the request flow.

### 2. Authentication

`auth_service.py` handles admin authentication.

- Admins are read from `data/admins.json`
- Passwords are hashed with SHA-256
- A successful login creates a JWT token
- Tokens expire after 1 hour
- Protected API routes verify the token before allowing access

### 3. Database layer

`database_service.py` handles SQLite operations.

It automatically:

- creates the `data/` folder if needed
- creates the `users` table if it does not already exist
- inserts, reads, updates, and deletes users
- supports filtering by `country` and `game`
- supports pagination with `page` and `limit`

### 4. API layer

`api.py` exposes the backend through Flask routes.

Main routes include:

- `GET /` — health message
- `POST /login` — admin login and JWT creation
- `GET /users` — list users with optional filters and pagination
- `GET /users/<id>` — get one user
- `POST /users` — create a user (admin JWT required)
- `PUT /users/<id>` — update a user (JWT required)
- `DELETE /users/<id>` — delete a user (admin JWT required)

### 5. CLI version

`main.py`, `user_service.py`, and `file_service.py` are the earlier command-line version of the project.

That version supports:

- adding users
- viewing users
- searching by name or ID
- updating and deleting users
- viewing user statistics
- exporting to CSV
- creating JSON backups

### 6. Migration script

`migrate_json_to_sqlite.py` moves existing users from the JSON-based storage into SQLite so the project can transition from the CLI version to the API version.

## Local setup

### 1. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

Create a file named `.env` in the project root:

```env
API_KEY=your_api_key_here
JWT_SECRET=your_super_secret_jwt_key_here
```

### 4. Create admin data

Create `data/admins.json` and store at least one admin user.

Example:

```json
[
  {
    "username": "admin",
    "password": "240be518fabd2724ddb6f04eeb0c06041c8b1f82b1df6c6f3d0b4f1f2f7a1d87",
    "role": "admin"
  }
]
```

That password value should be a SHA-256 hash of the real password.

### 5. Run the API

```bash
python api.py
```

By default, the current code runs on:

```text
http://127.0.0.1:5000
```

## Recommended deployment change for EC2

Before deploying to EC2, change the Flask host in `api.py` from:

```python
app.run(host="127.0.0.1", port=5000, debug=True)
```

to:

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

This allows the app to accept requests from outside the EC2 instance.

## Example API usage

### Login

```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'
```

### Get all users

```bash
curl http://127.0.0.1:5000/users
```

### Get filtered users

```bash
curl "http://127.0.0.1:5000/users?country=japan&game=ff7&page=1&limit=10"
```

### Create a user

```bash
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name":"jon","age":34,"color":"red","game":"ff7","country":"japan"}'
```

### Update a user

```bash
curl -X PUT http://127.0.0.1:5000/users/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"color":"blue"}'
```

### Delete a user

```bash
curl -X DELETE http://127.0.0.1:5000/users/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Deploying to AWS EC2

### What to deploy

For a backend-only deployment, you can deploy:

- `api.py`
- `auth_service.py`
- `config.py`
- `database_service.py`
- `logging_service.py`
- `file_service.py`
- `migrate_json_to_sqlite.py`
- `requirements.txt`
- `.env` on the server only
- `data/admins.json` on the server only

You do **not** need to deploy the frontend files if you want this project to remain backend-focused.

### EC2 checklist

1. Launch an Ubuntu EC2 instance
2. Allow inbound rules for:
   - SSH (port 22) from your IP
   - Custom TCP (port 5000) from your IP or a limited range for testing
3. SSH into the instance
4. Install Python, pip, venv, and Git
5. Clone your GitHub repository
6. Create and activate a virtual environment
7. Install dependencies
8. Create `.env`
9. Create `data/admins.json`
10. Update `api.py` to use `0.0.0.0`
11. Run `python api.py`
12. Test with `http://YOUR_EC2_PUBLIC_IP:5000/users`

## GitHub notes

Do not upload secrets or local runtime files.

Keep these out of GitHub:

- `.env`
- `venv/`
- `__pycache__/`
- `data/users.db`
- `data/admins.json`
- `logs/`
- `backups/`
- exported CSV files

## Known cleanup items

This project works, but there are a few things worth improving later:

- `API_KEY` is loaded in config but not currently enforced in the API request flow
- `api.py` currently runs on `127.0.0.1`, which should be changed to `0.0.0.0` for EC2
- `debug=True` is fine for learning, but should be turned off for production
- the frontend files are optional and can be removed from deployment for a cleaner backend portfolio project
- password hashing works, but a stronger password hashing approach such as `bcrypt` or `werkzeug.security` would be better for a more production-style version

## Why this project is useful for a backend portfolio

This project demonstrates backend fundamentals that are directly relevant to junior backend roles:

- Python programming
- modular code organization
- REST API design
- authentication with JWT
- database integration with SQLite
- input validation
- role-based permissions
- file handling, logging, and backups
- migration from file storage to relational storage

## Future improvements

Possible next upgrades:

- move from SQLite to PostgreSQL
- use Flask blueprints for better route organization
- replace SHA-256 password hashing with bcrypt
- add automated tests with `pytest`
- add Docker support
- run behind Gunicorn and Nginx on EC2
- add rate limiting and stronger request validation
- add a proper admin/user ownership model

## Author

Built by Brandon Auglis as a backend learning and portfolio project.
