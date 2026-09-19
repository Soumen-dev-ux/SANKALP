from datetime import datetime

from pydantic import BaseModel


class RegionResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class RegionSummaryResponse(BaseModel):
    id: int
    name: str
    demographics_count: int
    infrastructure_count: int
    project_count: int
    request_count: int