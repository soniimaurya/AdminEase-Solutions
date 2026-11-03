# AdminEase Solutions – Module 3 CRM Automation

A standalone CRM API starter for lead management, follow-up tracking, interaction history, and dashboard KPIs. It is intentionally kept separate from Modules 1 and 2 until their actual schemas and API contracts are inspected.

## Features
- Lead create, list, search, update, and delete
- Controlled lead statuses: New, Contacted, Interested, Qualified, Converted, Lost
- Follow-up creation, listing, and completion/cancellation
- Lead interaction history
- Dashboard summary endpoint
- SQLAlchemy 2.x models and FastAPI validation
- Pytest tests using an isolated in-memory database

## Windows PowerShell setup

Run from this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload --port 8002
```

Open `http://127.0.0.1:8002/docs` for Swagger UI.

## Main endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/leads` | Create lead |
| GET | `/api/leads` | List/search/filter leads |
| GET | `/api/leads/{id}` | Get one lead |
| PATCH | `/api/leads/{id}` | Update lead |
| DELETE | `/api/leads/{id}` | Delete lead |
| POST | `/api/leads/{id}/follow-ups` | Schedule follow-up |
| GET | `/api/follow-ups` | List follow-ups |
| PATCH | `/api/follow-ups/{id}` | Update follow-up status |
| POST | `/api/leads/{id}/interactions` | Add interaction |
| GET | `/api/leads/{id}/interactions` | Interaction history |
| GET | `/api/dashboard/summary` | CRM KPI summary |

## Important integration note

This starter currently uses its own SQLite database (`crm.db`) and its own `Lead` model. Do not point it at the Module 1 database or merge models until the existing Module 1 database configuration, authentication, lead schema, and route contracts have been reviewed. Module 2 Excel synchronization is also intentionally deferred until its exact workbook columns and script are confirmed.

## Example lead

```json
{
  "name": "Asha Sharma",
  "email": "asha@example.com",
  "phone": "9876543210",
  "company": "ABC Ltd",
  "source": "LinkedIn",
  "status": "New",
  "notes": "Interested in a product demo"
}
```
