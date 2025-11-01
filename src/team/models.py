from enum import Enum as PyEnum

from src.database.config import Base

from sqlalchemy import UUID, String, Integer, ForeignKey, Enum, text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TeamRole(PyEnum):
    employee = 'employee'
    manager = 'manager'


class Team(Base):
    __tablename__ = 'teams'
    uuid: Mapped[UUID] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = mapped_column(String(256), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(String(512), unique=False, nullable=True)
    teamuser: Mapped[list['TeamUser']] = relationship('TeamUser')


class TeamUser(Base):
    __tablename__ = 'teamuser'
    uuid: Mapped[UUID] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    user: Mapped[UUID] = mapped_column(ForeignKey('users.uuid', ondelete="CASCADE"))
    team: Mapped[UUID] = mapped_column(ForeignKey('teams.uuid', ondelete='CASCADE'))
    team_role: Mapped[TeamRole] = mapped_column(Enum(TeamRole), default=TeamRole.employee)
    user_relation: Mapped['User'] = relationship('User')
