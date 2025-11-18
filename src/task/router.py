from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.database.config import get_db
from src.security.depends import user_auth
from src.security.exceptions import authorize_exception, exception_404
from src.security.utils import check_is_author

from .service import create_task, get_task_by_uuid, remove_task, update_task, create_comment, get_tasks_by_team, get_tasks_by_user
from .schemas import CreateTaskShemas, UpdateTaskShema, TaskResponse, SetPerformerShema, SetStatusShema, CommentBaseShema, TaskCommentsResponse, CommentResponseShema

router = APIRouter(
    prefix='/task',
    tags=['task']
)


async def user_is_author(task_uuid: UUID,
                         user: Annotated[str, Depends(user_auth)],
                         session=Depends(get_db)):
    task = await get_task_by_uuid(task_uuid, session)
    if not task:
        raise exception_404
    if not check_is_author(task.author, user.uuid):
        raise authorize_exception
    return task


@router.get('')
async def get_task(task_uuid: UUID,
                   user: Annotated[str, Depends(user_auth)],
                   session=Depends(get_db)) -> TaskCommentsResponse:
    task_model = await get_task_by_uuid(task_uuid, session)
    task_shema = TaskCommentsResponse.model_validate(task_model)
    return task_shema


@router.post('')
async def post_task(task_data: CreateTaskShemas,
                    user: Annotated[str, Depends(user_auth)],
                    session=Depends(get_db)) -> TaskResponse:
    task_dict = task_data.model_dump()
    task_dict['author'] = user.uuid
    res = await create_task(task_dict, session)
    return TaskResponse.model_validate(res)


@router.patch('/{task_uuid}')
async def patch_task(task_uuid: UUID, task_data: UpdateTaskShema,
                     user: Annotated[str, Depends(user_is_author)],
                     session=Depends(get_db)) -> TaskResponse:
    task_dict = task_data.model_dump(exclude_unset=True)
    task_updated = await update_task(task_uuid, task_dict, session)
    return task_updated


@router.delete('')
async def delete_task(task_uuid: UUID,
                      user: Annotated[str, Depends(user_is_author)],
                      session=Depends(get_db)):
    await remove_task(task_uuid, session)
    return {'detail': 'task deleted'}


@router.patch('/{task_uuid}/performer')
async def assign_performer(performer_shema: SetPerformerShema,
                           task: Annotated[str, Depends(user_is_author)],
                           session=Depends(get_db)) -> TaskResponse:
    values_to_update = performer_shema.model_dump()
    values_to_update.update(status='in progress')
    task_updated = await update_task(task.uuid, values_to_update, session)
    return task_updated


@router.patch('/{task_uuid}/status')
async def change_status(status_shema: SetStatusShema,
                        task: Annotated[str, Depends(user_is_author)],
                        session=Depends(get_db))  -> TaskResponse:
    status = status_shema.model_dump()
    task_updated = await update_task(task.uuid, status, session)
    return task_updated


@router.post('/{task_uuid}/comment')
async def post_comment(task_uuid: UUID,
                       comment_schema: CommentBaseShema,
                       user: Annotated[str, Depends(user_auth)],
                       session=Depends(get_db)) -> CommentResponseShema:
    comment = comment_schema.model_dump()
    response = await create_comment(task_uuid,
                                    user.uuid,
                                    comment,
                                    session
                                    )
    return response


@router.get('/team/{team_uuid}')
async def get_team_tasks(team_uuid: UUID,
                         user: Annotated[str, Depends(user_auth)],
                         session=Depends(get_db)):
    tasks = await get_tasks_by_team(team_uuid, session)
    result = []
    for task in tasks:
        task_schema = TaskCommentsResponse.model_validate(task)
        result.append(task_schema.model_dump())
    return result


@router.get('/my')
async def get_my_tasks(user: Annotated[str, Depends(user_auth)],
                       session=Depends(get_db)):
    tasks = await get_tasks_by_user(user.uuid, session)
    result = [TaskCommentsResponse.model_validate(task).model_dump() for task in tasks]
    return result
