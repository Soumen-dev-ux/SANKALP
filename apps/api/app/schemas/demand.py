from pydantic import BaseModel, Field


class CategoryDemandResponse(BaseModel):
    category: str
    request_count: int
    demand_score: float = Field(
        ge=0,
        le=100,
    )


class RegionalDemandResponse(BaseModel):
    region_id: int
    region_name: str
    total_requests: int
    categories: list[CategoryDemandResponse]