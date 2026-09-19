from sqlalchemy.orm import Session

from app.models.demographic import Demographic
from app.schemas.demographic import DemographicCreate


def create_demographic(
    db: Session,
    demographic_data: DemographicCreate,
) -> Demographic:

    demographic = Demographic(
        region_id=demographic_data.region_id,
        population=demographic_data.population,
        population_density=demographic_data.population_density,
        income_index=demographic_data.income_index,
        age_0_14_percent=demographic_data.age_0_14_percent,
        age_15_24_percent=demographic_data.age_15_24_percent,
        age_25_64_percent=demographic_data.age_25_64_percent,
        age_65_plus_percent=demographic_data.age_65_plus_percent,
        growth_rate=demographic_data.growth_rate,
    )

    db.add(demographic)
    db.commit()
    db.refresh(demographic)

    return demographic