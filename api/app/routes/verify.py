from datetime import datetime
from fastapi import APIRouter, HTTPException
from api.app.db import get_session
from api.app.models import Investigation, SandboxRun
from api.app.schemas import VerifyResponse
from api.app.services.sandbox_client import run_sandbox_for_investigation

router = APIRouter()

@router.post("/{incident_id}/verify", response_model=VerifyResponse)
def verify_incident(incident_id: int):
    session = get_session()
    try:
        investigation = (
            session.query(Investigation)
            .filter(Investigation.incident_id == incident_id)
            .order_by(Investigation.created_at.desc())
            .first()
        )

        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")

        status, logs_path, logs_text = run_sandbox_for_investigation(investigation)

        sandbox_run = SandboxRun(
            investigation_id=investigation.id,
            status=status,
            logs_path=logs_path,
            completed_at=datetime.utcnow(),
        )
        session.add(sandbox_run)
        session.commit()
        session.refresh(sandbox_run)

        return VerifyResponse(
            investigation_id=investigation.id,
            status=status,
            logs=logs_text,
            logs_path=logs_path,
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(exc)}")
    finally:
        session.close()