from pydantic import BaseModel, Field


class SemanticClusterMember(BaseModel):
    request_id: int
    anonymous_reference: str
    similarity_score: float = Field(
        ge=0,
        le=1,
    )


class SemanticClusterResponse(BaseModel):
    cluster_id: str
    category: str | None
    representative_issue: str
    request_count: int
    members: list[SemanticClusterMember]
    average_similarity: float = Field(
        ge=0,
        le=1,
    )