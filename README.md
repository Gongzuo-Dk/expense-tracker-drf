# Expense Tracker API

A fully featured REST API for tracking personal expenses, built with Django REST Framework and PostgreSQL. Designed to be consumed by any frontend — mobile app, React, or any HTTP client.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![DRF](https://img.shields.io/badge/Django_REST_Framework-API-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)

## About

Expense Tracker API is a pure REST API backend with no traditional frontend. It handles user authentication, expense and category management, and spending analytics. Built as a portfolio project to demonstrate Django REST Framework, token-based authentication, Google OAuth, ownership-protected data, and API design patterns.  

## Features

- **Token Authentication** — Register and login to receive an API token, used for all subsequent requests
- **Google OAuth** — Login with Google via django-allauth
- **Expense CRUD** — Create, read, update, and delete personal expenses
- **Category CRUD** — Organize expenses into custom categories with color and icon
- **Ownership protection** — Users can only access and modify their own data, enforced at the database query level
- **Spending summary** — Total spent, expense count, and average for the current month
- **Category breakdown** — Spending totals and percentages per category
- **Filtering** — Filter expenses by category, date range, and amount range
- **Search** — Search expenses by description, categories by name
- **Ordering** — Order expenses by date, amount, or creation time
- **Pagination** — All list endpoints paginated at 10 results per page
- **Automated tests** — pytest suite covering auth, ownership protection, and business logic

## Tech Stack

- **Backend** — Python 3.13, Django 6.0, Django REST Framework
- **Auth** — dj-rest-auth, django-allauth, Google OAuth2
- **Database** — PostgreSQL
- **Testing** — pytest, pytest-django
- **Static files** — WhiteNoise
- **Server** — Gunicorn
- **Deployment** — Railway
- **Config** — python-decouple

## Project Structure  
config/               # Project settings, root URLs, wsgi  
accounts/             # CustomUser model, Google OAuth view  
expenses/             # Category and Expense models, serializers,  
# views, filters, tests  

## API Endpoints (were tested using Postman)

**Base URL (local):** `http://127.0.0.1:8000`

All `/api/` endpoints require the following header:  
Authorization: Token <your_token_here>  
---

### Authentication  

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| POST | `/auth/registration/` | Register new user, returns token | No |
| POST | `/auth/login/` | Login, returns token | No |
| POST | `/auth/logout/` | Logout, destroys token | Yes |
| GET | `/auth/user/` | Get current user details | Yes |
| POST | `/auth/google/` | Login with Google OAuth | No |

**Register example:**
```json
POST /auth/registration/
{
    "username": "john",
    "email": "john@example.com",
    "password1": "SecurePass123!",
    "password2": "SecurePass123!"
}

Response 201:
{
    "key": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Login example:**
```json
POST /auth/login/
{
    "username": "john",
    "password": "SecurePass123!"
}

Response 200:
{
    "key": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

---

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | List all categories |
| POST | `/api/categories/` | Create a category |
| GET | `/api/categories/{id}/` | Retrieve a category |
| PUT | `/api/categories/{id}/` | Update a category |
| PATCH | `/api/categories/{id}/` | Partial update |
| DELETE | `/api/categories/{id}/` | Delete a category |

**Create category example:**
```json
POST /api/categories/
{
    "name": "Groceries",
    "color": "#2ecc71",
    "icon": "shopping-cart"
}

Response 201:
{
    "id": 1,
    "name": "Groceries",
    "color": "#2ecc71",
    "icon": "shopping-cart"
}
```

**Query parameters:**  
?search=groceries       → search by name
?ordering=name          → order by name (prefix - for descending)   
---

### Expenses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/expenses/` | List all expenses |
| POST | `/api/expenses/` | Create an expense |
| GET | `/api/expenses/{id}/` | Retrieve an expense |
| PUT | `/api/expenses/{id}/` | Update an expense |
| PATCH | `/api/expenses/{id}/` | Partial update |
| DELETE | `/api/expenses/{id}/` | Delete an expense |

**Create expense example:**
```json
POST /api/expenses/
{
    "amount": "50.00",
    "description": "Weekly groceries",
    "date": "2026-05-20",
    "category": 1
}

Response 201:
{
    "id": 1,
    "amount": "50.00",
    "description": "Weekly groceries",
    "date": "2026-05-20",
    "category": 1,
    "category_name": "Groceries",
    "created_at": "2026-05-20T14:32:00Z",
    "updated_at": "2026-05-20T14:32:00Z"
}
```

**Query parameters:**  
?category=1                           → filter by category ID
?date_after=2026-01-01                → expenses on or after date
?date_before=2026-05-31               → expenses on or before date
?min_amount=50                        → expenses of 50 or more
?max_amount=100                       → expenses of 100 or less
?search=groceries                     → search by description
?ordering=-amount                     → order by amount descending
?ordering=date                        → order by date ascending
Combinable:
?category=1&date_after=2026-01-01&ordering=-amount  

**Paginated response format:**
```json
{
    "count": 47,
    "next": "http://127.0.0.1:8000/api/expenses/?page=2",
    "previous": null,
    "results": [...]
}
```

---

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/expenses/summary/` | Spending summary for current month |
| GET | `/api/expenses/by-category/` | Spending breakdown by category |

**Summary response:**
```json
GET /api/expenses/summary/

{
    "month": "May 2026",
    "total": "284.50",
    "expense_count": 8,
    "average": "35.56"
}
```

**By category response:**
```json
GET /api/expenses/by-category/

[
    {
        "category_id": 1,
        "category_name": "Groceries",
        "color": "#2ecc71",
        "icon": "shopping-cart",
        "total": "150.00",
        "expense_count": 4,
        "percentage": 52.7
    },
    {
        "category_id": 2,
        "category_name": "Transport",
        "color": "#3498db",
        "icon": "car",
        "total": "134.50",
        "expense_count": 4,
        "percentage": 47.3
    }
]
```

---

## Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/Gongzuo-Dk/expense-tracker-drf.git
cd expense-tracker-drf
```

**2. Create and activate virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file in the project root**

Use `.env.example` as a reference:  
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=expense_tracker
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_CALLBACK_URL=http://127.0.0.1:8000/accounts/google/login/callback/  

**5. Set up the database**

Make sure PostgreSQL is running and the database exists, then:
```bash
python manage.py migrate
```

**6. Create a superuser**
```bash
python manage.py createsuperuser
```

**7. Run the development server**
```bash
python manage.py runserver
```

Test the API at `http://127.0.0.1:8000/` or use Postman.

---

## Running Tests

```bash
pytest
```

The test suite covers:
- Unauthenticated requests return 401
- Users can only access their own data
- Cross-user access returns 404 (not 403 — no data leakage)
- Object creation automatically assigns the authenticated user
- Duplicate category names return 400
- Filtering and date range queries return correct subsets
- Summary and by-category endpoints return correct aggregated data

---

## Key Implementation Details

- **Custom User Model** — Extends `AbstractUser`, set up before the first migration so the auth system is owned from day one
- **Token Authentication** — DRF's built-in token auth. Clients receive a token on login and include it as `Authorization: Token <key>` on every request
- **Ownership at queryset level** — `get_queryset()` filters by `request.user` on every ViewSet. Users never see other users' data — because it's never fetched
- **Row-level security** — `perform_create` injects `user=request.user` server-side. The user field is never accepted from request body
- **ORM aggregations** — Summary and breakdown endpoints use `Sum`, `Count`, `Avg`, and `annotate` to calculate at the database level, never in Python loops
- **Serializer-level validation** — Duplicate category names are caught in `validate()` before hitting the database, returning a clean 400 instead of a 500
- **Google OAuth** — Full OAuth2 flow via django-allauth. Google's ID token verified with PyJWT and cryptography. Users receive a standard DRF token after OAuth authentication
- **Environment variables** — All secrets managed via python-decouple. `.env.example` provided for reference

---

## Author

Daniel K
GitHub: https://github.com/Gongzuo-Dk
LinkedIn: https://www.linkedin.com/in/danylo-kulynych/
