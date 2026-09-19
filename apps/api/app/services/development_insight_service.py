from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.citizen_request import CitizenRequest
from app.models.demographic import Demographic
from app.models.government_project import GovernmentProject
from app.models.infrastructure import Infrastructure
from app.models.region import Region


def get_development_insights(
    db: Session,
    region_id: int,
):
    region = (
        db.query(Region)
        .filter(Region.id == region_id)
        .first()
    )

    if not region:
        return None

    total_requests = (
        db.query(func.count(CitizenRequest.id))
        .filter(
            CitizenRequest.region_id == region_id
        )
        .scalar()
        or 0
    )

    demographic = (
        db.query(Demographic)
        .filter(
            Demographic.region_id == region_id
        )
        .first()
    )

    request_categories = (
        db.query(
            CitizenRequest.category,
            func.count(CitizenRequest.id).label(
                "request_count"
            ),
        )
        .filter(
            CitizenRequest.region_id == region_id
        )
        .group_by(CitizenRequest.category)
        .all()
    )

    insights = []

    for category, request_count in request_categories:

        category_name = (
            category
            if category
            else "Uncategorized"
        )

        if total_requests > 0:
            demand_score = (
                request_count / total_requests
            ) * 100
        else:
            demand_score = 0

        infrastructure = (
            db.query(Infrastructure)
            .filter(
                Infrastructure.region_id == region_id,
                Infrastructure.category
                == category_name,
            )
            .all()
        )

        coverage_values = [
            item.coverage_percent
            for item in infrastructure
            if item.coverage_percent is not None
        ]

        quality_values = [
            item.quality_score
            for item in infrastructure
            if item.quality_score is not None
        ]

        infrastructure_data_available = bool(
            infrastructure
        )

        if coverage_values:
            infrastructure_coverage = (
                sum(coverage_values)
                / len(coverage_values)
            )
        else:
            infrastructure_coverage = 0

        if quality_values:
            infrastructure_quality = (
                sum(quality_values)
                / len(quality_values)
            )
        else:
            infrastructure_quality = 0

        gap_score = (
            demand_score
            * (
                1
                - infrastructure_coverage / 100
            )
        )

        projects = (
            db.query(GovernmentProject)
            .filter(
                GovernmentProject.region_id
                == region_id,
                GovernmentProject.category
                == category_name,
            )
            .all()
        )

        project_count = len(projects)

        if project_count > 0:
            project_factor = 100
            project_coverage = 100
        else:
            project_factor = 0
            project_coverage = 0

        composite_score = (
            (0.50 * demand_score)
            + (0.40 * gap_score)
            + (0.10 * project_factor)
        )

        if composite_score >= 60:
            insight_level = "High"
        elif composite_score >= 30:
            insight_level = "Moderate"
        else:
            insight_level = "Low"

        evidence = [
            (
                f"{request_count} citizen request(s) "
                f"were recorded for {category_name}."
            ),
            (
                f"Demand score is "
                f"{round(demand_score, 2)}."
            ),
            (
                f"Recorded infrastructure coverage "
                f"is {round(infrastructure_coverage, 2)}%."
            ),
        ]

        if project_count > 0:
            evidence.append(
                f"{project_count} related government "
                f"project(s) are recorded."
            )
        else:
            evidence.append(
                "No related government projects "
                "are recorded in the demo dataset."
            )

        data_warnings = []

        if not infrastructure_data_available:
            data_warnings.append(
                "No infrastructure records were found "
                "for this category; the gap may reflect "
                "missing data rather than actual absence."
            )

        if demographic is None:
            data_warnings.append(
                "No demographic record is available "
                "for this region."
            )

        insights.append(
            {
                "region_id": region.id,
                "region_name": region.name,
                "category": category_name,
                "request_count": request_count,
                "demand_score": round(
                    demand_score,
                    2,
                ),
                "infrastructure_coverage": round(
                    infrastructure_coverage,
                    2,
                ),
                "infrastructure_quality": round(
                    infrastructure_quality,
                    2,
                ),
                "gap_score": round(
                    gap_score,
                    2,
                ),
                "project_count": project_count,
                "project_coverage": round(
                    project_coverage,
                    2,
                ),
                "population": (
                    demographic.population
                    if demographic
                    else None
                ),
                "population_density": (
                    demographic.population_density
                    if demographic
                    else None
                ),
                "insight_level": insight_level,
                "evidence": evidence,
                "data_warnings": data_warnings,
            }
        )

    insights.sort(
        key=lambda item: (
            item["gap_score"],
            item["demand_score"],
        ),
        reverse=True,
    )

    return {
        "region_id": region.id,
        "region_name": region.name,
        "insights": insights,
    }