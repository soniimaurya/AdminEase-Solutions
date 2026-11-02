# Project Gaurav – Module 1: Workflow Automation

A starter backend that receives incoming lead data through a REST webhook, validates it,
assigns a category, detects duplicate email addresses, and stores valid leads in SQLite.

## 1. Requirements
- Python 3.10 or newer
- VS Code (recommended)
- Internet connection for installing Python packages

## 2. Setup (Windows PowerShell)

Open this folder in VS Code, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run this once in the current terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Start the API

From the project root folder:

```powershell
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

Interactive API documentation:
`http://127.0.0.1:8000/docs`

## 4. Test the webhook

In `/docs`:
1. Open `POST /webhook/leads`.
2. Select **Try it out**.
3. Paste the contents of `sample_lead.json`.
4. Select **Execute**.

Expected result: HTTP `201`, `success: true`, a lead ID, and an assigned category.

Try the same email again. Expected result: HTTP `409` because duplicate email addresses are blocked.

Try an invalid email or a phone number with too few digits. Expected result: HTTP `422` validation response.

## 5. Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| POST | `/webhook/leads` | Receive, validate, categorize and store a lead |
| GET | `/leads?limit=100` | List saved leads |

## 6. Data flow

Website/form (future source) → webhook endpoint → Pydantic validation → business-rule categorization
→ duplicate check → SQLite database → CRM-ready record.

## 7. Files created at runtime
- `data/leads.db`: SQLite database
- `logs/application.log`: application log

These files are generated when the API runs.

## 8. Run tests

```powershell
pytest -q
```

## 9. Important project notes
- This is a local pilot/demo implementation using sample data.
- No real website webhook, production CRM, API key, or external endpoint is connected yet.
- The target CRM, field mapping, authentication method, sample payload and deployment details
  must be confirmed by AdminEase Solutions before production integration.
- Do not put passwords, API keys, customer personal data, or access tokens in GitHub.
- LinkedIn actions should remain compliant with LinkedIn's terms and use approved methods.

## 10. Suggested next steps after company provides access
1. Confirm the exact landing-page payload and webhook authentication.
2. Agree required/optional fields and duplicate matching rules.
3. Confirm CRM name, API documentation, field mapping and sandbox credentials.
4. Add secure authentication, retries, rate limits and deployment configuration.
5. Test with company-provided sample data before production use.
