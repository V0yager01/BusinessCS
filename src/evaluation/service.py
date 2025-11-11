from fastapi.exceptions import HTTPException

from src.task.repo import TaskRepo

from .repo import EvaluationRepo


async def get_task_by_uuid(uuid, session):
    taskrepo = TaskRepo(session)
    try:
        result = await taskrepo.select_model_by_uuid(uuid)
        return result
    except Exception as e:
        raise e


async def create_rate_and_change_task(task_uuid, rate, session):
    evaluationrepo = EvaluationRepo(session)
    taskrepo = TaskRepo(session)
    task = await taskrepo.select_model_by_uuid(task_uuid)
    if not task.performer:
        raise HTTPException(
            detail='Performer has not been appointed',
            status_code=400
        )
    elif task.status == 'done':
        raise HTTPException(
            detail='The task has already been rated',
            status_code=400
        )
    value_to_insert = {
        'rate': rate,
        'performer': task.performer,
        'reviewer': task.author,
        'task': task.uuid
    }
    evaluation = await evaluationrepo.insert_evaluation_and_update_task(task_uuid, values=value_to_insert)
    return evaluation


async def get_all_evaluation_by_date(uuid, start_date, end_date, session):
    evaluationrepo = EvaluationRepo(session)
    try:
        result = await evaluationrepo.select_all_evaluation_by_dates(uuid,
                                                                     start_date,
                                                                     end_date)
        return result
    except Exception as e:
        raise e


async def get_avg_rate_by_user_uuid(uuid, session):
    evaluationrepo = EvaluationRepo(session)
    try:
        result = await evaluationrepo.select_avg_rate(uuid)
        return result
    except Exception as e:
        raise e