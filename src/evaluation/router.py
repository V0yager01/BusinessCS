from datetime import date

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.security.depends import user_auth
from src.security.exceptions import exception_404, authorize_exception
from src.security.utils import check_is_author

from .service import get_task_by_uuid, create_rate_and_change_task, get_all_evaluation_by_date, get_avg_rate_by_user_uuid
router = APIRouter(
    prefix='/evaluation',
    tags=['evaluations']
)


async def user_is_author(task_uuid: UUID,
                         user: Annotated[str, Depends(user_auth)]):
    task = await get_task_by_uuid(task_uuid)
    if not task:
        raise exception_404
    if not check_is_author(task.author, user.uuid):
        raise authorize_exception
    return task


@router.post('')
async def rate_and_close_task(task_uuid:UUID,
                              rate: Annotated[int, Query(gt=0, le=5)],
                              user: Annotated[str, Depends(user_is_author)]):
    await create_rate_and_change_task(task_uuid, rate)
    return {'detail': 'The task was rated'}


@router.get('/me')
async def get_my_score(star_date: date,
                       end_date: date,
                       user: Annotated[str, Depends(user_auth)]):
    evaluations = await get_all_evaluation_by_date(
        uuid=user.uuid,
        start_date=star_date,
        end_date=end_date
    )

    return evaluations


@router.get('/me/avg')
async def get_avg_rate(user: Annotated[str, Depends(user_auth)]):
    evaluations = await get_avg_rate_by_user_uuid(uuid=user.uuid)
    return evaluations
