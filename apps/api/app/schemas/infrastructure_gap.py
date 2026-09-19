from pydantic import BaseModel, Field


class InfrastructureGapResponse(BaseModel):
    category: str
    demand_score: float = Field(
        ge=0,
        le=100,
    )
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
    request_count: int = Field(
        ge=0,
    )
    infrastructure_data_available: bool


class RegionalInfrastructureGapResponse(BaseModel):
    region_id: int
    region_name: str
    total_requests: int
    categories: list[InfrastructureGapResponse]