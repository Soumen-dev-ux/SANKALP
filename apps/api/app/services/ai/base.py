from dataclasses import dataclass
from typing import Protocol

from app.schemas.confidence import UnderstandingConfidence

from app.schemas.insight_explaination import (
    InsightExplanationRequest,
    InsightExplanationResponse,
)

class InsightExplanationProvider(Protocol):
    def explain_insight(
        self,
        insight: InsightExplanationRequest,
    ) -> InsightExplanationResponse:
        ...


@dataclass
class CitizenLocation:
    text: str | None
    location_type: str
    name: str | None
    ward: str | None
    district: str | None
    landmark: str | None


@dataclass
class CitizenUnderstanding:
    language: str | None
    category: str | None
    intent: str | None
    issue: str | None
    location: CitizenLocation
    confidence: UnderstandingConfidence | None = None


class AIProvider(Protocol):
    def understand(self, text: str) -> CitizenUnderstanding:
        ...