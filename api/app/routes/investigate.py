from fastapi import APIRouter, HTTPException
from api.app.config import DEMO_REPO_PATH
from api.app.db import get_session
from api.app.models import Incident, Investigation
from api.app.schemas import InvestigationResponse
from api.app.services.llm_orchestrator import produce_mock_investigation

router = APIRouter()

@router.post("/{incident_id}/investigate", response_model=InvestigationResponse)
def investigate(incident_id: int):
    session = get_session()
    try:
        incident = session.get(Incident, incident_id)
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")

        result = produce_mock_investigation(incident, repo_path=DEMO_REPO_PATH)

        investigation = Investigation(
            incident_id=incident_id,
            root_cause=result["root_cause"],
            affected_files=",".join(result["affected_files"]),
            patch_file=result.get("patch_file"),
        )
        session.add(investigation)
        session.commit()
        session.refresh(investigation)

        return InvestigationResponse(
            id=investigation.id,
            root_cause=result["root_cause"],
            affected_files=result["affected_files"],
            patch_preview=result["patch_preview"],
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Investigation failed: {str(exc)}")
    finally:
        session.close()