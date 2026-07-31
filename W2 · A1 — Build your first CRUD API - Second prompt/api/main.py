from fastapi import FastAPI, HTTPException, Query, Path, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory storage for tasks
tasks_db = []
next_id = 1

class Task(BaseModel):
    id: int
    title: str
    done: bool

@app.get("/")
async def root():
    return {"version": "1.0", "purpose": "Task CRUD API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/tasks", response_model=List[Task])
def get_tasks(done: Optional[bool] = None, search: Optional[str] = None):
    if done is not None:
        tasks = [task for task in tasks_db if task['done'] == done]
    elif search:
        tasks = [task for task in tasks_db if search.lower() in task['title'].lower()]
    else:
        tasks = tasks_db
    return tasks

@app.get("/tasks/{id}", response_model=Task)
def get_task(id: int):
    task = next((t for t in tasks_db if t['id'] == id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=Task)
def add_task(task: Task):
    global next_id
    new_task = {"id": next_id, "title": task.title, "done": task.done}
    tasks_db.append(new_task)
    next_id += 1
    return new_task

@app.put("/tasks/{id}", response_model=Task)
def update_task(id: int, task_update: Task):
    for t in tasks_db:
        if t['id'] == id:
            t.update(task.dict(exclude_unset=True))
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}")
def delete_task(id: int):
    global tasks_db
    task = next((t for t in tasks_db if t['id'] == id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db = [t for t in tasks_db if t['id'] != id]
    return {"detail": "Task deleted"}

@app.post("/reset")
def reset_tasks():
    global tasks_db, next_id
    tasks_db = []
    next_id = 1
    return {"detail": "Tasks reset"}

@app.get("/stats", response_model=BaseModel)
class Stats(BaseModel):
    total: int
    open: int
    done: int

def calculate_stats() -> Stats:
    total = len(tasks_db)
    open_tasks = sum(1 for task in tasks_db if not task['done'])
    done_tasks = total - open_tasks
    return Stats(total=total, open=open_tasks, done=done_tasks)

@app.get("/stats", response_model=Stats)
def get_stats():
    return calculate_stats()

