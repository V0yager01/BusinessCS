from datetime import datetime
from uuid import UUID

from sqlalchemy import UUID, text, ForeignKey, Integer, CheckConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.config import Base

class Evaluation(Base):
    __tablename__ = 'evaluations'

    uuid: Mapped[UUID] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    rate: Mapped[int] = mapped_column(Integer)
    performer: Mapped[UUID] = mapped_column(ForeignKey('users.uuid', ondelete='CASCADE'))
    reviewer: Mapped[UUID] = mapped_column(ForeignKey('users.uuid', ondelete='SET NULL'))
    task: Mapped[UUID] = mapped_column(ForeignKey('tasks.uuid', ondelete='SET NULL'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint('rate >= 1 AND rate <= 5', name='check_rate_range'),
    )