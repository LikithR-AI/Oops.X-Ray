from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class IncidentCreate(BaseModel):
    title: str
    description: Optional[str] = None

class IncidentRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

class InvestigationResponse(BaseModel):
    id: int
    root_cause: str
    affected_files: List[str]
    patch_preview: str

class VerifyResponse(BaseModel):
    investigation_id: int
    status: str
    logs: str
    logs_path: Optional[str] = None