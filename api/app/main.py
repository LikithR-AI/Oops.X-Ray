from fastapi import FastAPI
from api.app.db import init_db
from api.app.routes import incidents, investigate, verify

app = FastAPI(title="OOPS.X-Ray Demo A (backend)")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(incidents.router, prefix="/api/incidents", tags=["incidents"])
app.include_router(investigate.router, prefix="/api/incidents", tags=["investigate"])
app.include_router(verify.router, prefix="/api/incidents", tags=["verify"])