from src.database.config import async_session
from src.security.exceptions import json_exception

from .repo import TaskRepo, CommentRepo


async def create_task(task_data):
    taskrepo = TaskRepo()
    try:        
        return await taskrepo.insert_model(task_data)
    except Exception as e:
        raise e


#TODO Сделать базовый класс BaseRepo с select по uuid, вынести все проверки по uuid в security/utils.py

async def get_task_by_uuid(uuid):
    taskrepo = TaskRepo()
    try:
        result = await taskrepo.select_full_task_by_uuid(uuid)
        return result
    except Exception as e:
        raise e


async def remove_task(uuid):
    taskrepo = TaskRepo()
    try:
        await taskrepo.delete_model(uuid)
    except Exception as e:
        raise json_exception


async def update_task(task_uuid, values):
    taskrepo = TaskRepo()
    try:
        await taskrepo.update_model(task_uuid, values)
        result = await taskrepo.select_model_by_uuid(task_uuid)
        return result
    except Exception as e:
        raise json_exception


async def create_comment(task_uuid, author, values):
    taskrepo = CommentRepo()
    values.update(task=task_uuid, author=author)
    try:
        result = await taskrepo.insert_model(values)
        return result
    except Exception as e:
        raise json_exception