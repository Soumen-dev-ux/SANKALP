import pytest
from app.db.session import SessionLocal
from app.models.user import User
from app.models.citizen_request import CitizenRequest
from app.schemas.human_review import HumanReviewCreate
from app.services.reviewer_service import create_review_action, get_pending_reviews
from app.core.security import hash_password


@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


def test_create_review_action_success(db_session):
    user = User(
        email="test_reviewer@example.com",
        password_hash=hash_password("password123"),
        full_name="Test Reviewer",
        role="reviewer",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    request = CitizenRequest(
        anonymous_reference="SANKALP-REV01",
        language="en",
        raw_text="No clean water available in block A",
        category="Water & Sanitation",
        intent="Report Development Need",
        issue="Drinking Water",
        status="submitted",
        source="web",
        review_status="pending",
    )
    db_session.add(request)
    db_session.commit()
    db_session.refresh(request)

    payload = HumanReviewCreate(
        status="approved",
        reviewer_note="Looks good and valid",
    )

    action = create_review_action(
        db=db_session,
        request_id=request.id,
        reviewer=user,
        payload=payload,
    )

    assert action.status == "approved"
    assert action.reviewer_id == user.id
    assert action.request_id == request.id