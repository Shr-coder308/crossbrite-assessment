from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.evaluation import Evaluation
from app.models.parent_child import ParentChild
from app.models.session import Session as SessionModel
from app.models.user import User
from app.schemas.evaluation import (
    EvaluationResponse,
    EvaluationTriggerRequest,
)
from app.services.evaluation_service import queue_evaluation


router = APIRouter(
    prefix="/evaluations",
    tags=["Evaluations"],
)


@router.post(
    "/trigger/{session_id}",
    response_model=EvaluationResponse,
)
def trigger_evaluation(
    session_id: int,
    request: EvaluationTriggerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only teachers can trigger evaluations
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can trigger evaluations",
        )

    # Teacher can access only their own session
    session = (
        db.query(SessionModel)
        .filter(
            SessionModel.id == session_id,
            SessionModel.teacher_id == current_user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found or you do not have access to it",
        )

    # Verify student
    student = (
        db.query(User)
        .filter(
            User.id == request.student_id,
            User.role == "student",
            User.is_active.is_(True),
        )
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    # Create evaluation
    evaluation = Evaluation(
        session_id=session.id,
        student_id=student.id,
        status="queued",
    )

    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)

    # Queue evaluation job in Redis
    queue_evaluation(
        evaluation_id=evaluation.id,
        session_id=session.id,
    )

    return evaluation


@router.get(
    "/my-child",
    response_model=list[EvaluationResponse],
)
def get_my_child_evaluations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only parents can access this endpoint
    if current_user.role != "parent":
        raise HTTPException(
            status_code=403,
            detail="Only parents can access child evaluations",
        )

    # Find children linked to the logged-in parent
    child_ids = (
        db.query(ParentChild.child_id)
        .filter(ParentChild.parent_id == current_user.id)
        .all()
    )

    child_ids = [child_id for (child_id,) in child_ids]

    if not child_ids:
        return []

    # Return evaluations only for those children
    return (
        db.query(Evaluation)
        .filter(Evaluation.student_id.in_(child_ids))
        .order_by(Evaluation.created_at.desc())
        .all()
    )
