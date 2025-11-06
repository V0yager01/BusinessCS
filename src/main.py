from fastapi import FastAPI

from src.team.router import router as team_router
from src.user.router import router as user_router
from src.task.router import router as task_router
from src.evaluation.router import router as evaluation_router
from src.meeting.router import router as meeting_router

app = FastAPI()

app.include_router(team_router)
app.include_router(user_router)
app.include_router(task_router)
app.include_router(evaluation_router)
app.include_router(meeting_router)