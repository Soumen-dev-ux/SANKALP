from app.schemas.insight_explaination import InsightExplanationRequest
from app.services.insight_explaination_service import (
    build_deterministic_explanation,
)


def test_deterministic_insight_explanation():

    insight = InsightExplanationRequest(
        region_name="North Region",
        category="Healthcare",
        request_count=5,
        demand_score=50,
        infrastructure_coverage=60,
        infrastructure_quality=0.7,
        gap_score=20,
        project_count=1,
        project_coverage=100,
        population=85000,
        population_density=2400,
        evidence=[
            "Healthcare requests are present.",
            "Healthcare infrastructure data is available.",
        ],
        data_warnings=[],
    )

    result = build_deterministic_explanation(insight)

    assert result.summary
    assert result.evidence_references == [0, 1]
    assert result.limitation_references == []
    assert result.review_note

def test_explanation_with_no_requests():

    insight = InsightExplanationRequest(
        region_name="South Region",
        category="Education",
        request_count=0,
        demand_score=0,
        infrastructure_coverage=0,
        infrastructure_quality=0,
        gap_score=0,
        project_count=0,
        project_coverage=0,
        population=None,
        population_density=None,
        evidence=[],
        data_warnings=[
            "No citizen request data is available."
        ],
    )

    result = build_deterministic_explanation(insight)

    assert "No citizen request data" in result.summary
    assert result.evidence_references == []
    assert result.limitation_references == [0]