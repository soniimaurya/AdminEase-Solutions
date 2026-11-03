# Project Gaurav – Multi-Module Business Automation & CRM System

A multi-module business automation project developed as part of the Project Gaurav pilot at AdminEase Solutions.

The project focuses on workflow automation, LinkedIn relationship management, lead tracking, and CRM automation using Python, FastAPI, REST APIs, SQL databases, and Excel dashboards.

## Project Modules

| Module   | Name                             | Description                                                                                               |
| -------- | -------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Module 1 | Workflow Automation              | Backend workflow automation, API integration, webhook handling, and JSON processing.                      |
| Module 2 | LinkedIn Relationship Management | B2B outreach framework, prospect tracking, engagement management, and Excel dashboard.                    |
| Module 3 | CRM Automation                   | Lead management APIs, follow-up tracking, interaction history, dashboard metrics, and API authentication. |

## Project Structure

```text
AdminEase-Solutions/
│
├── Project_Gaurav/
│   │
│   ├── Module_1_Workflow_Automation/
│   │
│   ├── Module_2_LinkedIn_Outreach/
│   │
│   └── Module_3_CRM_Automation/
│       ├── app/
│       │   ├── __init__.py
│       │   ├── database.py
│       │   ├── main.py
│       │   ├── models.py
│       │   └── schemas.py
│       │
│       ├── tests/
│       │   └── test_crm.py
│       │
│       ├── .gitignore
│       ├── README.md
│       └── requirements.txt
│
└── README.md
```

## Module 1 – Workflow Automation

Focus areas:

* Python backend automation.
* REST API development and integration.
* Webhook-based data processing.
* JSON parsing and validation.
* Automated workflow processing.

## Module 2 – LinkedIn Relationship Management

Focus areas:

* B2B prospect identification and tracking.
* LinkedIn outreach sequence planning.
* Prospect categorization and engagement tracking.
* Daily outreach activity planning.
* Performance measurement and KPI tracking.
* Excel-based automated lead tracking dashboard.

Deliverables include an outreach framework document and an Excel dashboard.

## Module 3 – CRM Automation

A FastAPI-based CRM backend designed to manage leads, follow-ups, and customer interactions.

### Implemented Features

* Create, view, update, and delete leads.
* Search and filter leads.
* Manage lead statuses.
* Schedule and update follow-ups.
* Maintain lead interaction history.
* View CRM dashboard summary.
* API key-based authentication.
* SQLAlchemy database integration.
* Automated API testing using Pytest.

### API Endpoints

| Method | Endpoint                            | Purpose                 |
| ------ | ----------------------------------- | ----------------------- |
| GET    | `/`                                 | Application information |
| GET    | `/health`                           | Health check            |
| POST   | `/api/leads`                        | Create a lead           |
| GET    | `/api/leads`                        | List and filter leads   |
| GET    | `/api/leads/{lead_id}`              | Get lead details        |
| PATCH  | `/api/leads/{lead_id}`              | Update a lead           |
| DELETE | `/api/leads/{lead_id}`              | Delete a lead           |
| POST   | `/api/leads/{lead_id}/follow-ups`   | Create a follow-up      |
| GET    | `/api/follow-ups`                   | View follow-ups         |
| PATCH  | `/api/follow-ups/{follow_up_id}`    | Update a follow-up      |
| POST   | `/api/leads/{lead_id}/interactions` | Add an interaction      |
| GET    | `/api/leads/{lead_id}/interactions` | View lead interactions  |
| GET    | `/api/dashboard/summary`            | CRM dashboard summary   |

### Technology Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn
* Pytest
* HTTPX

### Setup and Installation

Navigate to the Module 3 directory:

```bash
cd Project_Gaurav/Module_3_CRM_Automation
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Configure API Key

For Windows PowerShell:

```powershell
$env:CRM_API_KEY = "your-secure-api-key"
```

### Run the Application

```bash
uvicorn app.main:app --reload --port 8003
```

Open the API documentation:

```text
http://127.0.0.1:8003/docs
```

Protected API endpoints require the `X-API-Key` request header.

### Run Automated Tests

```bash
pytest -q
```

**Latest recorded test result:** 6 tests passed.

## Security and Data Management

* API key authentication for protected CRM endpoints.
* Environment variable-based API key configuration.
* Input validation using Pydantic.
* Database operations using SQLAlchemy.
* Local SQLite database for development.
* Sensitive configuration and database files excluded through `.gitignore`.

## Project Status

* Module 1: Workflow Automation – Developed as part of the project.
* Module 2: LinkedIn Relationship Management – Initial deliverables completed.
* Module 3: CRM Automation – Backend implementation and automated tests completed.
* Cross-module integration and further validation can be carried out as the next development stage.

## Repository

GitHub: https://github.com/soniimaurya/AdminEase-Solutions

## Author

**Soni Maurya**

B.Tech – Computer Science and Engineering (AI & ML)

GitHub: https://github.com/soniimaurya
