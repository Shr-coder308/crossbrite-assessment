from fastapi import FastAPI

app = FastAPI(
    title="Crossbrite Assessment API",
    description="Backend service for sessions and evaluations.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "crossbrite-assessment-api",
    }