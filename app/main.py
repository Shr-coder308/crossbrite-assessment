from fastapi import FastAPI

from app.api.users import router as users_router
from app.db.database import create_tables
from app.models import User


app = FastAPI(
    title="Crossbrite Assessment API",
    description="Backend service for sessions and evaluations.",
    version="1.0.0",
)

create_tables()

app.include_router(users_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "crossbrite-assessment-api",
    }