from uuid import UUID

from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class CreateMeetingBaseShema(BaseModel):
    start_at: datetime = datetime.now()
    meet_duration_hour: int = Field(default=0)
    meet_duration_minutes: int = Field(default=15)

    @model_validator(mode="after")
    def check_duration_not_zero(self):
        if self.meet_duration_hour == 0 and self.meet_duration_minutes == 0:
            raise ValueError("meet_duration_hour и meet_duration_minutes не могут быть оба равны 0")
        return self


class UsersToInviteShema(BaseModel):
    uuid: list[UUID]