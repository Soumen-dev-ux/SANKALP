from pydantic import BaseModel, Field


class InsightExplanationRequest(BaseModel):
    region_name: str
    category: str
    request_count: int = Field(ge=0)
    demand_score: float = Field(ge=0, le=100)
    infrastructure_coverage: float = Field(ge=0, le=100)
    infrastructure_quality: float = Field(ge=0, le=1)
    gap_score: float = Field(ge=0, le=100)
    project_count: int = Field(ge=0)
    project_coverage: float = Field(ge=0, le=100)
    population: int | None = Field(default=None, ge=0)
    population_density: float | None = Field(default=None, ge=0)
    evidence: list[str] = Field(default_factory=list, max_length=10)
    data_warnings: list[str] = Field(default_factory=list, max_length=10)


class InsightExplanationResponse(BaseModel):
    summary: str = Field(..., min_length=1, max_length=1000)
    evidence_references: list[int] = Field(default_factory=list)
    limitation_references: list[int] = Field(default_factory=list)
    review_note: str = Field(..., min_length=1, max_length=500)