import pytest
from app.db.session import SessionLocal
from app.models.citizen_request import CitizenRequest
from app.services.ai.human_review_service import submit_human_review
from app.schemas.human_review import HumanReviewCreate


@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


def test_human_review_approval(db_session):
    request = CitizenRequest(
        anonymous_reference="SANKALP-TEST01",
        language="en",
        raw_text="There is no drinking water in our village",
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

    review = HumanReviewCreate(
        status="approved",
        reviewer_note="AI interpretation verified.",
    )

    result = submit_human_review(
        db=db_session,
        request_id=request.id,
        review=review,
    )

    assert result.review_status == "approved"
    assert result.reviewer_note == "AI interpretation verified."
    assert result.reviewed_at is not None

def test_human_review_correction(db_session):
    request = CitizenRequest(
        anonymous_reference="SANKALP-TEST02",
        language="en",
        raw_text="The road near our school is damaged",
        category="Transport",
        issue="Road Infrastructure",
        status="submitted",
        source="web",
        review_status="pending",
    )

    db_session.add(request)
    db_session.commit()
    db_session.refresh(request)

    review = HumanReviewCreate(
        status="corrected",
        reviewer_note="Category corrected after manual verification.",
        reviewed_category="Education",
        reviewed_issue="School Access Road",
    )

    result = submit_human_review(
        db=db_session,
        request_id=request.id,
        review=review,
    )

    assert result.review_status == "corrected"
    assert result.reviewed_category == "Education"
    assert result.reviewed_issue == "School Access Road"