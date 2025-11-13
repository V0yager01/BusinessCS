from datetime import datetime
from uuid import UUID

from sqlalchemy import text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID as SQLUUID

from src.database.config import Base


class Meeting(Base):
    __tablename__ = 'meetings'

    uuid: Mapped[UUID] = mapped_column(
        SQLUUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    start_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    end_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    participants: Mapped[list['UserMeeting']] = relationship(
        back_populates='meeting'
    )


class UserMeeting(Base):
    __tablename__ = 'usermeetings'

    uuid: Mapped[UUID] = mapped_column(
        SQLUUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    meeting_uuid: Mapped[UUID] = mapped_column(
        ForeignKey('meetings.uuid', ondelete='CASCADE')
    )
    user_uuid: Mapped[UUID] = mapped_column(
        ForeignKey('users.uuid', ondelete='CASCADE')
    )
    meeting: Mapped['Meeting'] = relationship(back_populates='participants')

    __table_args__ = (
        UniqueConstraint(
            'user_uuid',
            'meeting_uuid',
            name='uq_user_meeting_pair'
        ),
    )
