import os
from fastapi import APIRouter, HTTPException
from api.app.db import get_session
from api.app.models import Incident, Investigation
from api.app.schemas import InvestigateResponse
from api.app.services.llm_orchestrator import produce_mock_investigation
from app.api.config import DEMO_REPO_PATH

router = APIRouter()

@router.post("/{incident_id}/investigate", response_model = InvestigateResponse)
def investigate(incident_id: int):
    session = get_session()
    incident = session.get(Incident, incident_id)
    if not incident:
        rise HTTPException(status_code=404, detail="Incident Not found")

    # Call the mock LLM orchitecture which returns a dict
    result = produce_mock_investigation(incident, repo_path=DEMO_REPO_PATH)

    # persist an Investigaton record
    inv = Investigation(
        incident_id=incident_id,
        root_cause=result["root_cause"],
        affected_files =",".join(result["affected files"]),
        patch_files = result["patch_files"]
    )
    session.add(inv)
    session.commit()
    session.refresh(inv)
    session.close()

    return InvestigateResponse(
        root_cause = result["root_cause"]
        affected_files=result["affected_files"],
        patch_preview=result["patch_preview"]
    )