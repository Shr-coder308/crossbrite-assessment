import pytest
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.security import password_hasher
from app.db.database import SessionLocal
from app.models.user import User
from app.models.session import Session as SessionModel
from app.models.parent_child import ParentChild
from app.models.evaluation import Evaluation


@pytest.fixture(scope="session")
def setup_test_data():
    db: Session = SessionLocal()

    try:
        teacher = db.query(User).filter(
            User.email == "teacher2@example.com"
        ).first()

        if not teacher:
            teacher = User(
                name="Teacher Two",
                email="teacher2@example.com",
                role="teacher",
                password_hash=password_hasher.hash("Teacher@123"),
                is_active=True,
            )
            db.add(teacher)

        parent = db.query(User).filter(
            User.email == "parent@example.com"
        ).first()

        if not parent:
            parent = User(
                name="Parent One",
                email="parent@example.com",
                role="parent",
                password_hash=password_hasher.hash("Parent@123"),
                is_active=True,
            )
            db.add(parent)

        student = db.query(User).filter(
            User.email == "student@example.com"
        ).first()

        if not student:
            student = User(
                name="Student One",
                email="student@example.com",
                role="student",
                password_hash=password_hasher.hash("Student@123"),
                is_active=True,
            )
            db.add(student)

        db.commit()

        db.refresh(teacher)
        db.refresh(parent)
        db.refresh(student)

        relationship = db.query(ParentChild).filter(
            ParentChild.parent_id == parent.id,
            ParentChild.child_id == student.id,
        ).first()

        if not relationship:
            relationship = ParentChild(
                parent_id=parent.id,
                child_id=student.id,
            )
            db.add(relationship)

        session = db.query(SessionModel).filter(
            SessionModel.teacher_id == teacher.id
        ).first()

        if not session:
            session = SessionModel(
                teacher_id=teacher.id,
                title="Mathematics Evaluation Session",
                description="Grade 10 mathematics assessment",
                scheduled_at=datetime(2026, 9, 20, 10, 0, 0),
            )
            db.add(session)

        db.commit()
        db.refresh(session)

        evaluation = db.query(Evaluation).filter(
            Evaluation.session_id == session.id,
            Evaluation.student_id == student.id,
        ).first()

        if not evaluation:
            evaluation = Evaluation(
                session_id=session.id,
                student_id=student.id,
                status="completed",
                score=85,
                feedback="Good performance in the evaluation.",
            )
            db.add(evaluation)

        db.commit()

    finally:
        db.close()


@pytest.fixture
def client(setup_test_data):
    return TestClient(app)