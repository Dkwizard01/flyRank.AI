from fastapi import FastAPI, HTTPException, Query, Path
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

tasks = []

class Task(BaseModel):
    id: int
    title: str
    done: bool

@app.get("/")
def read_root():
    return {"info": "Task CRUD API", "version": "1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/tasks", response_model=List[Task])
def get_tasks(done: Optional[bool] = None, search: Optional[str] = None):
    if done is not None:
        tasks_filtered = [task for task in tasks if task.done == done]
    elif search is not None:
        tasks_filtered = [task for task in tasks if search.lower() in task.title.lower()]
    else:
        tasks_filtered = tasks
    return tasks_filtered

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int = Path(..., description="The ID of the task to retrieve")):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int = Path(...), task_update: Optional[Task] = None):
    for i, existing_task in enumerate(tasks):
        if existing_task.id == task_id:
            updated_task = existing_task.copy(update=task_update.dict(exclude_unset=True))
            tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]

@app.post("/reset")
def reset_tasks():
    global tasks
    tasks = []

@app.get("/stats", response_model=BaseModel)
class Stats(BaseModel):
    total: int
    open: int
    done: int

@app.get("/stats", response_model=Stats)
def get_stats():
    total = len(tasks)
    done = sum(1 for task in tasks if task.done)
    open = total - done
    return {"total": total, "open": open, "done": done}

