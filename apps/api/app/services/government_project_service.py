from sqlalchemy.orm import Session

from app.models.government_project import GovernmentProject
from app.schemas.government_projects import (
    GovernmentProjectCreate,
)


def create_government_project(
    db: Session,
    project_data: GovernmentProjectCreate,
) -> GovernmentProject:

    project = GovernmentProject(
        region_id=project_data.region_id,
        name=project_data.name,
        category=project_data.category,
        description=project_data.description,
        status=project_data.status,
        budget=project_data.budget,
        implementing_agency=project_data.implementing_agency,
        start_date=project_data.start_date,
        expected_completion_date=(
            project_data.expected_completion_date
        ),
        actual_completion_date=(
            project_data.actual_completion_date
        ),
        latitude=project_data.latitude,
        longitude=project_data.longitude,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project