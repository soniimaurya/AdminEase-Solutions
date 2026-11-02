```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from app.database import (
    initialize_database,
    insert_lead,
    fetch_leads,
    email_exists
)
from app.models import LeadInput
from app.processor import prepare_lead


# Project directory
ROOT = Path(__file__).resolve().parent.parent

# Create logs directory
(ROOT / "logs").mkdir(parents=True, exist_ok=True)


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


# Application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):

    initialize_database()
    logger.info("Application started successfully.")

    yield

    logger.info("Application shutdown completed.")


# FastAPI application
app = FastAPI(
    title="Project Gaurav - Workflow Automation API",
    description=(
        "Receives, validates, categorizes "
        "and stores incoming business leads."
    ),
    version="1.1.0",
    lifespan=lifespan
)


# Health check
@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Project Gaurav Module 1"
    }


# Receive and process leads
@app.post(
    "/webhook/leads",
    status_code=status.HTTP_201_CREATED
)
def receive_lead(payload: LeadInput):

    lead = prepare_lead(payload.model_dump())

    # Check duplicate email
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

    except Exception:

        logger.exception(
            "Unexpected error while saving lead."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save the lead. Please try again later."
        )


# Retrieve leads
@app.get("/leads")
def list_leads(limit: int = 100):

    if limit < 1 or limit > 500:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit must be between 1 and 500."
        )

    leads = fetch_leads(limit)

    return {
        "count": len(leads),
        "leads": leads
    }
```
