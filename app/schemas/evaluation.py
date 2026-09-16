from pydantic import BaseModel


class EvaluationTriggerRequest(BaseModel):
    student_id: int


class EvaluationResponse(BaseModel):
    id: int
    session_id: int
    student_id: int
    status: str
    score: int | None
    feedback: str | None

    model_config = {
        "from_attributes": True
    }