from datetime import date

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.database.config import get_db
from src.security.depends import user_auth
from src.task.router import user_is_author

from .schemas import EvaluationResponseShema, EvaluationAvgResponseShema
from .service import (
    get_task_by_uuid,
    create_rate_and_change_task,
    get_all_evaluation_by_date,
    get_avg_rate_by_user_uuid
)
router = APIRouter(
    prefix='/evaluation',
    tags=['evaluations']
)


@router.post('')
async def rate_and_close_task(task_uuid: UUID,
                              rate: Annotated[int, Query(gt=0, le=5)],
                              user: Annotated[str, Depends(user_is_author)],
                              session=Depends(get_db)):
    await create_rate_and_change_task(task_uuid, rate, session)
    return {'detail': 'The task was rated',
            'status': 200}


@router.get('/me')
async def get_my_score(star_date: date,
                       end_date: date,
                       user: Annotated[str, Depends(user_auth)],
                       session=Depends(get_db)):
    evaluations = await get_all_evaluation_by_date(
        uuid=user.uuid,
        start_date=star_date,
        end_date=end_date,
        session=session
    )

    return [
        EvaluationResponseShema.model_validate(item)
        for item in evaluations
    ]


@router.get('/me/avg')
async def get_avg_rate(user: Annotated[str, Depends(user_auth)],
                       session=Depends(get_db)) -> EvaluationAvgResponseShema:
    evaluations = await get_avg_rate_by_user_uuid(
        uuid=user.uuid,
        session=session
    )
    return EvaluationAvgResponseShema.model_validate(evaluations)
