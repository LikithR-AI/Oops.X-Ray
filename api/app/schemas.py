from pydantic import BaseModel
from typing import Optional, List

class IncidentCreate(BaseModel):
    title: str
    description: Optional[str] = None

class InvestigateResponse(BaseModel):
    id: int

class InvestigateResponse(BaseModel):
    root_cause: str
    affected_files: List[str]
    patch_preview: str

class VerifyResponse(BaseModel):
    status: str
    logs: str
