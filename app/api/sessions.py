from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_role
from app.db.database import get_db
from app.models.session import Session as SessionModel
from app.models.user import User
from app.schemas.session import SessionCreate, SessionResponse

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post(
    "/",
    response_model=SessionResponse,
    dependencies=[Depends(require_role("teacher"))],
)
def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_session = SessionModel(
        teacher_id=current_user.id,
        title=session_data.title,
        description=session_data.description,
        scheduled_at=session_data.scheduled_at,
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session


@router.get(
    "/",
    response_model=list[SessionResponse],
    dependencies=[Depends(require_role("teacher"))],
)
def get_my_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(SessionModel)
        .filter(SessionModel.teacher_id == current_user.id)
        .all()
    )


@router.put(
    "/{session_id}",
    response_model=SessionResponse,
    dependencies=[Depends(require_role("teacher"))],
)
def update_session(
    session_id: int,
    session_data: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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
            detail="Session not found",
        )

    session.title = session_data.title
    session.description = session_data.description
    session.scheduled_at = session_data.scheduled_at

    db.commit()
    db.refresh(session)

    return session


@router.delete(
    "/{session_id}",
    dependencies=[Depends(require_role("teacher"))],
)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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
            detail="Session not found",
        )

    db.delete(session)
    db.commit()

    return {
        "message": "Session deleted successfully",
        "session_id": session_id,
    }