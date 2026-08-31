from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime

class Incident(SQLModel, tabel=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: optional[str] = None
    created_at: datetime =Field(default_factory=datetime.utcnow)

class Investigation(SQLModel, tabel=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    incident_id: int
    root_cause: Optional[str] = None
    affected_files: Optional[str] = None
    patch_file: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SandboxRun(SQLModel, tabel=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    investigation_id: int
    status: str  # VERIFIED / FAILED / ERROR / TIMEOUT
    logs_path: Optional[str] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class Approval(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    investigation_id: int
    approved_by: Optional[str] = None
    decision: Optional[str] = None  # approved / rejected
    notes: Optional[str] = None
    decided_at: Optional[datetime] = None
