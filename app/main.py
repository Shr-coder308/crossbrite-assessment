from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.evaluations import router as evaluations_router
from app.api.parent_child import router as parent_child_router
from app.api.sessions import router as sessions_router
from app.api.users import router as users_router
from app.models import User


app = FastAPI(
    title="Crossbrite Assessment API",
    description="Backend service for sessions and evaluations.",
    version="1.0.0",
)


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(sessions_router)
app.include_router(parent_child_router)
app.include_router(evaluations_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "crossbrite-assessment-api",
    }