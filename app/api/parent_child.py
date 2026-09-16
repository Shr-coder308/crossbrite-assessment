from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_role
from app.db.database import get_db
from app.models.parent_child import ParentChild
from app.models.user import User


router = APIRouter(
    prefix="/parent-child",
    tags=["Parent-Child"]
)


@router.post("/")
def link_child(
    child_id: int,
    current_user: User = Depends(require_role("parent")),
    db: Session = Depends(get_db),
):
    child = db.query(User).filter(
        User.id == child_id,
        User.role == "student",
        User.is_active.is_(True),
    ).first()

    if not child:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    existing = db.query(ParentChild).filter(
        ParentChild.parent_id == current_user.id,
        ParentChild.child_id == child_id,
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Child already linked",
        )

    relationship = ParentChild(
        parent_id=current_user.id,
        child_id=child_id,
    )

    db.add(relationship)
    db.commit()
    db.refresh(relationship)

    return {
        "message": "Child linked successfully",
        "parent_id": relationship.parent_id,
        "child_id": relationship.child_id,
    }