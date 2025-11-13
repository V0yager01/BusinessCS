from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["frontend-teams"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/teams")
async def teams_page(request: Request):
    return templates.TemplateResponse(
        "teams.html",
        {"request": request, "title": "Команды"}
    )


@router.get("/tasks")
async def tasks_page(request: Request):
    return templates.TemplateResponse(
        "tasks.html",
        {"request": request, "title": "Задачи"}
    )


@router.get("/meetings")
async def meetings_page(request: Request):
    return templates.TemplateResponse(
        "meetings.html",
        {"request": request, "title": "Встречи"}
    )


@router.get("/calendar")
async def calendar_page(request: Request):
    return templates.TemplateResponse(
        "calendar.html",
        {"request": request, "title": "Календарь"}
    )


@router.get("/profile")
async def profile_page(request: Request):
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "title": "Профиль"}
    )


@router.get("/evaluations")
async def evaluations_page(request: Request):
    return templates.TemplateResponse(
        "evaluations.html",
        {"request": request, "title": "Оценки"}
    )
