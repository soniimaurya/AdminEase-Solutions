
import os
import hmac
from datetime import date

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
    Request,
    Header,
)
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas


Base.metadata.create_all(bind=engine)


# API Key Authentication
def require_api_key(
    request: Request,
    api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    if not request.url.path.startswith("/api/"):
        return

    expected_key = os.getenv("CRM_API_KEY")

    if not expected_key:
        raise HTTPException(
            status_code=503,
            detail="API authentication is not configured"
        )

    if not api_key or not hmac.compare_digest(api_key, expected_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )


app = FastAPI(
    title="AdminEase Solutions - Module 3 CRM",
    description="CRM APIs for lead management, follow-ups and interaction history.",
    version="1.0.0",
    dependencies=[Depends(require_api_key)],
)

def safe_commit(db: Session):
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )


@app.get("/")
def home():
    return {
        "message": "AdminEase CRM API is running",
        "module": "Module 3 - CRM Automation"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


# Create lead
@app.post(
    "/api/leads",
    response_model=schemas.LeadOut,
    status_code=201
)
def create_lead(
    payload: schemas.LeadCreate,
    db: Session = Depends(get_db)
):
    if payload.status not in schemas.LEAD_STATUSES:
        raise HTTPException(422, "Invalid lead status")

    lead = models.Lead(**payload.model_dump())

    db.add(lead)
    safe_commit(db)
    db.refresh(lead)

    return lead


# List and search leads
@app.get(
    "/api/leads",
    response_model=list[schemas.LeadOut]
)
def list_leads(
    status: str | None = None,
    search: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    query = db.query(models.Lead)

    if status:
        query = query.filter(models.Lead.status == status)

    if search:
        search_text = f"%{search}%"
        query = query.filter(
            or_(
                models.Lead.name.ilike(search_text),
                models.Lead.email.ilike(search_text),
                models.Lead.company.ilike(search_text)
            )
        )

    return (
        query.order_by(models.Lead.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# Get one lead
@app.get(
    "/api/leads/{lead_id}",
    response_model=schemas.LeadOut
)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    lead = db.get(models.Lead, lead_id)

    if not lead:
        raise HTTPException(404, "Lead not found")

    return lead


# Update lead
@app.patch(
    "/api/leads/{lead_id}",
    response_model=schemas.LeadOut
)
def update_lead(
    lead_id: int,
    payload: schemas.LeadUpdate,
    db: Session = Depends(get_db)
):
    lead = db.get(models.Lead, lead_id)

    if not lead:
        raise HTTPException(404, "Lead not found")

    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            422,
            "At least one field must be provided"
        )

    if "status" in update_data:
        if update_data["status"] not in schemas.LEAD_STATUSES:
            raise HTTPException(422, "Invalid lead status")

    for field, value in update_data.items():
        setattr(lead, field, value)

    safe_commit(db)
    db.refresh(lead)

    return lead


# Delete lead
@app.delete(
    "/api/leads/{lead_id}",
    status_code=204
)
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    lead = db.get(models.Lead, lead_id)

    if not lead:
        raise HTTPException(404, "Lead not found")

    db.delete(lead)
    safe_commit(db)

    return None


# Create follow-up
@app.post(
    "/api/leads/{lead_id}/follow-ups",
    response_model=schemas.FollowUpOut,
    status_code=201
)
def create_follow_up(
    lead_id: int,
    payload: schemas.FollowUpCreate,
    db: Session = Depends(get_db)
):
    if not db.get(models.Lead, lead_id):
        raise HTTPException(404, "Lead not found")

    follow_up = models.FollowUp(
        lead_id=lead_id,
        **payload.model_dump()
    )

    db.add(follow_up)
    safe_commit(db)
    db.refresh(follow_up)

    return follow_up


# List follow-ups
@app.get(
    "/api/follow-ups",
    response_model=list[schemas.FollowUpOut]
)
def list_follow_ups(
    status: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.FollowUp)

    if status:
        query = query.filter(models.FollowUp.status == status)

    return query.order_by(models.FollowUp.due_date.asc()).all()


# Update follow-up
@app.patch(
    "/api/follow-ups/{follow_up_id}",
    response_model=schemas.FollowUpOut
)
def update_follow_up(
    follow_up_id: int,
    payload: schemas.FollowUpUpdate,
    db: Session = Depends(get_db)
):
    follow_up = db.get(models.FollowUp, follow_up_id)

    if not follow_up:
        raise HTTPException(404, "Follow-up not found")

    follow_up.status = payload.status

    safe_commit(db)
    db.refresh(follow_up)

    return follow_up


# Add interaction
@app.post(
    "/api/leads/{lead_id}/interactions",
    response_model=schemas.InteractionOut,
    status_code=201
)
def add_interaction(
    lead_id: int,
    payload: schemas.InteractionCreate,
    db: Session = Depends(get_db)
):
    if not db.get(models.Lead, lead_id):
        raise HTTPException(404, "Lead not found")

    item = models.Interaction(
        lead_id=lead_id,
        **payload.model_dump()
    )

    db.add(item)
    safe_commit(db)
    db.refresh(item)

    return item


# List lead interactions
@app.get(
    "/api/leads/{lead_id}/interactions",
    response_model=list[schemas.InteractionOut]
)
def list_interactions(
    lead_id: int,
    db: Session = Depends(get_db)
):
    if not db.get(models.Lead, lead_id):
        raise HTTPException(404, "Lead not found")

    return (
        db.query(models.Interaction)
        .filter(models.Interaction.lead_id == lead_id)
        .order_by(models.Interaction.interacted_at.desc())
        .all()
    )


# Dashboard summary
@app.get("/api/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):

    total = (
        db.query(func.count(models.Lead.id)).scalar() or 0
    )

    by_status = dict(
        db.query(
            models.Lead.status,
            func.count(models.Lead.id)
        )
        .group_by(models.Lead.status)
        .all()
    )

    pending = (
        db.query(func.count(models.FollowUp.id))
        .filter(models.FollowUp.status == "Pending")
        .scalar() or 0
    )

    overdue = (
        db.query(func.count(models.FollowUp.id))
        .filter(
            models.FollowUp.status == "Pending",
            models.FollowUp.due_date < date.today()
        )
        .scalar() or 0
    )

    return {
        "total_leads": total,
        "leads_by_status": by_status,
        "pending_follow_ups": pending,
        "overdue_follow_ups": overdue,
    }