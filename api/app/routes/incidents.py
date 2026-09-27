from fastapi import APIRouter, HTTPException
from api.app.db import get_session
from api.app.models import Incident
from api.app.schemas import IncidentCreate, IncidentRead

router = APIRouter()

@router.post("", response_model=IncidentRead)
def create_incident(payload: IncidentCreate):
    session = get_session()
    try:
        incident = Incident(title=payload.title, description=payload.description)
        session.add(incident)
        session.commit()
        session.refresh(incident)
        return incident
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to create incident: {str(exc)}")
    finally:
        session.close()

@router.get("", response_model=list[IncidentRead])
def list_incidents():
    session = get_session()
    try:
        incidents = session.query(Incident).order_by(Incident.created_at.desc()).all()
        return incidents
    finally:
        session.close()