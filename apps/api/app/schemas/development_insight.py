from pydantic import BaseModel, Field


class DevelopmentInsightResponse(BaseModel):
    region_id: int
    region_name: str
    category: str

    request_count: int = Field(ge=0)
    demand_score: float = Field(ge=0, le=100)

    infrastructure_coverage: float = Field(
        ge=0,
        le=100,
    )

    infrastructure_quality: float = Field(
        ge=0,
        le=1,
    )

    gap_score: float = Field(
        ge=0,
        le=100,
    )

    project_count: int = Field(ge=0)

    project_coverage: float = Field(
        ge=0,
        le=100,
    )

    population: int | None = Field(
        default=None,
        ge=0,
    )

    population_density: float | None = Field(
        default=None,
        ge=0,
    )

    insight_level: str

    evidence: list[str]

    data_warnings: list[str]

class RegionalDevelopmentInsightResponse(BaseModel):
    region_id: int
    region_name: str
    insights: list[DevelopmentInsightResponse]