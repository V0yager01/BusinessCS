from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EvaluationBaseShema(BaseModel):
    rate: int
    performer: UUID
    reviewer: UUID | None = None
    task: UUID | None = None


class EvaluationResponseShema(EvaluationBaseShema):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    created_at: datetime


class EvaluationAvgResponseShema(BaseModel):
    avg_rate: float

