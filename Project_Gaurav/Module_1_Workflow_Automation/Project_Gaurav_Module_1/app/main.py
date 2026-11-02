import logging
import os
import secrets
import sqlite3

from logging.handlers import RotatingFileHandler
from pathlib import Path

from fastapi import (
    FastAPI,
    HTTPException,
    status,
    Header,
    Depends
)
from fastapi.responses import JSONResponse
from app.database import (
    initialize_database,
    insert_lead,
    fetch_leads,
    email_exists
)

from app.models import LeadInput
from app.processor import prepare_lead


ROOT = Path(__file__).resolve().parent.parent

(ROOT / "logs").mkdir(exist_ok=True)


# Logging configuration
logger = logging.getLogger("project_gaurav")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = RotatingFileHandler(
        ROOT / "logs" / "application.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )

    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
    )

    logger.addHandler(handler)


# FastAPI application
app = FastAPI(
    title="Project Gaurav - Workflow Automation API",
    description="Receives, validates, categorizes and stores business leads.",
    version="1.1.0"
)


# API Key Authentication
def verify_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key")
):

    expected_api_key = os.getenv("PROJECT_GAURAV_API_KEY")

    if not expected_api_key:
        logger.error("API key is not configured.")

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API authentication is not configured."
        )

    if not x_api_key or not secrets.compare_digest(
        x_api_key,
        expected_api_key
    ):
        logger.warning("Unauthorized API request.")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key."
        )


# Startup
@app.on_event("startup")
def startup_event():

    initialize_database()

    logger.info(
        "Application started and database initialized."
    )


# Public health endpoint
@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Project Gaurav Module 1"
    }


# Protected webhook endpoint
@app.post(
    "/webhook/leads",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)]
)
def receive_lead(payload: LeadInput):

    lead = prepare_lead(payload.model_dump())

    if email_exists(lead["email"]):

        logger.warning(
            "Duplicate lead rejected: %s",
            lead["email"]
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A lead with this email address already exists."
        )

    try:

        lead_id = insert_lead(lead)

        logger.info(
            "Lead accepted. id=%s category=%s",
            lead_id,
            lead["category"]
        )

        return {
            "success": True,
            "message": "Lead received and processed successfully.",
            "lead_id": lead_id,
            "lead": lead
        }

    except sqlite3.IntegrityError:

        logger.warning(
            "Duplicate lead rejected by database: %s",
            lead["email"]
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A lead with this email address already exists."
        )

    except Exception:

        logger.exception(
            "Unexpected error while saving lead."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save the lead. Please try again later."
        )


# Protected leads endpoint
@app.get(
    "/leads",
    dependencies=[Depends(verify_api_key)]
)
def list_leads(limit: int = 100):

    if limit < 1 or limit > 500:

        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 500."
        )

    leads = fetch_leads(limit)

    return {
        "count": len(leads),
        "leads": leads
    }


# General error handler
@app.exception_handler(Exception)
async def unexpected_exception_handler(request, exc):

    logger.exception(
        "Unhandled application error: %s",
        str(exc)
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected server error occurred."
        }
    )