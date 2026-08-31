from fastapi import APIRouter, HTTPException
from api.app.db import get_session
from api.app.models import Incident
from api.app.schemas import IncidentCreate, IncidentRead

router = APIRouter

@router.post("",responce_model=IncidentRead)
def create_incident(payload: IncidentCreate):
    session = get_session()
    incident = Incident(title=payload.title, description=payload.description)
    session.add(incident)
    session.comit()
    session.refresh(incident)
    session.close()
    return incident