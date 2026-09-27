from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Incident(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Investigation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    incident_id: int
    root_cause: Optional[str] = None
    affected_files: Optional[str] = None
    patch_file: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SandboxRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    investigation_id: int
    status: str
    logs_path: Optional[str] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class Approval(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    investigation_id: int
    approved_by: Optional[str] = None
    decision: Optional[str] = None
    notes: Optional[str] = None
    decided_at: Optional[datetime] = None