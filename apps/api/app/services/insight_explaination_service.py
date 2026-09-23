from app.schemas.insight_explaination import (
    InsightExplanationRequest,
    InsightExplanationResponse,
)


def build_deterministic_explanation(
    insight: InsightExplanationRequest,
) -> InsightExplanationResponse:
    evidence_count = len(insight.evidence)
    warning_count = len(insight.data_warnings)

    if insight.request_count == 0:
        summary = (
            f"No citizen request data is currently available for "
            f"{insight.category} in {insight.region_name}."
        )
    else:
        summary = (
            f"Citizen requests indicate a development need related to "
            f"{insight.category} in {insight.region_name}. "
            f"The available data should be reviewed alongside infrastructure "
            f"and project information."
        )

    evidence_references = list(range(evidence_count))

    limitation_references = list(range(warning_count))

    review_note = (
        "This explanation summarizes available analytical data. "
        "It does not replace official verification, feasibility assessment, "
        "budgeting, or administrative review."
    )

    return InsightExplanationResponse(
        summary=summary,
        evidence_references=evidence_references,
        limitation_references=limitation_references,
        review_note=review_note,
    )