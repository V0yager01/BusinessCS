from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView

from src.database.config import async_engine, Base

from src.team.models import Team, TeamUser
from src.team.router import router as team_router
from src.user.models import User
from src.user.router import router as user_router
from src.task.models import Task, Comment
from src.task.router import router as task_router
from src.evaluation.models import Evaluation
from src.evaluation.router import router as evaluation_router
from src.meeting.models import UserMeeting, Meeting
from src.meeting.router import router as meeting_router

from src.routers import pages, auth_pages, teams_pages

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Разрешить все заголовки
)

admin = Admin(app, engine=async_engine)


class UserAdmin(ModelView, model=User):
    column_list = '__all__'


class TeamAdmin(ModelView, model=Team):
    column_list = '__all__'


class TeamUserAdmin(ModelView, model=TeamUser):
    column_list = '__all__'


class TaskAdmin(ModelView, model=Task):
    column_list = '__all__'


class CommentAdmin(ModelView, model=Comment):
    column_list = '__all__'


class EvaluationAdmin(ModelView, model=Evaluation):
    column_list = '__all__'


class UserMeetingAdmin(ModelView, model=UserMeeting):
    column_list = '__all__'


class MeetingAdmin(ModelView, model=Meeting):
    column_list = '__all__'


admin.add_view(UserAdmin)
admin.add_view(TeamAdmin)
admin.add_view(TeamUserAdmin)
admin.add_view(TaskAdmin)
admin.add_view(CommentAdmin)
admin.add_view(EvaluationAdmin)
admin.add_view(UserMeetingAdmin)
admin.add_view(MeetingAdmin)

app.include_router(team_router)
app.include_router(user_router)
app.include_router(task_router)
app.include_router(evaluation_router)
app.include_router(meeting_router)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(pages.router)
app.include_router(auth_pages.router)
app.include_router(teams_pages.router)
