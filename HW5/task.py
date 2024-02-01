
import logging
from pydantic import BaseModel
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

tasks_list = []
id_uniq = 1

class Task(BaseModel):
    title: str = "Заголовок задачи"
    description: str = "Описание задачи - "
    status: str = "не выполнена/выполнена"

@app.get("/tasks")
async def read_tasks():
    logger.info('Get all tasks.')
    return tasks_list

@app.get("/tasks/{task_id}")
async def read_task(task_id: int):
    for task in tasks_list:
        if task["id"] == task_id:
            logger.info(f'Get task list on task_id = {task_id}.')
            return task
    logger.info('No task')

@app.post("/tasks/")
async def create_task(task: Task):
    global id_uniq
    new_task = task.dict()
    new_task["id"] = id_uniq
    id_uniq += 1
    tasks_list.append(new_task)
    logger.info(f'Отработал POST запрос task id = {new_task["id"]}.')
    return new_task

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, upd_task: Task):
    for value in tasks_list:
        if value["id"] == task_id:
            tasks_list[tasks_list.index(value)].update(upd_task.dict())
            logger.info(f'Отработал PUT запрос для task id = {task_id}.')
            return upd_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for value in tasks_list:
        if value["id"] == task_id:
            logger.info(f'Отработал DELETE запрос для task id = {task_id}.')
            return tasks_list.pop(tasks_list.index(value))



