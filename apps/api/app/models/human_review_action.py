from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class HumanReviewAction(Base):
    __tablename__ = "human_review_actions"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(
        Integer,
        ForeignKey("citizen_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    reviewer_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    status = Column(String(30), nullable=False)

    reviewer_note = Column(Text, nullable=True)

    reviewed_category = Column(String(100), nullable=True)

    reviewed_issue = Column(String(255), nullable=True)

    reviewed_location = Column(String(500), nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    request = relationship(
        "CitizenRequest",
        back_populates="review_actions",
    )

    reviewer = relationship(
        "User",
        back_populates="review_actions",
    )