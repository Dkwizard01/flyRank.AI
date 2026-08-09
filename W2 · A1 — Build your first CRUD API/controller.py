import fastapi
from typing import Any
import sys
import os
sys.path.append(os.path.abspath(r"C:\Users\DK\source\repos\flyRank.AI\W3 · A1 — Connecting your CRUD to the database"))
import database

app = fastapi.FastAPI()
task_list = [
   { "id": "1", "title": "First task.", "done": "True" },
   { "id": "2", "title": "First task.", "done": "True" },
   { "id": "3", "title": "Third task.", "done": "False"}
]
      
# Stage 0: hello server
# @app.get("/")
# async def hello_server():
  #  return {"status_code": "200", "message": "Hello World"}
@app.get("/", summary="Calls the the root information API.")
async def root() -> dict[str, Any]:
   return  { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }
@app.get("/health", summary="Calls the health API.")
async def health():
   return { "status": "ok" } 
@app.get("/tasks", summary="Gets all tasks. Ability to search through tasks' titles and filter tasks by status")
async def tasks(done: str | None = None, search : str | None = None):
    if done != None and  done.casefold() == "true":
      return (task for task in task_list if task["done"] == "True")
    elif done != None and done.casefold() == "false":
      return (task for task in task_list if task["done"] == "False")
    if search != None and search != "":
       for task in task_list:
          if search in task["title"]:
             return task
    return database.get_all()
@app.get("/tasks/{id}", summary="Gets a task from the list using the task's id.")
async def get_task(id:int):
          task = database.search_by_id(id)
          if task is not None:
           return task
          else:
           raise fastapi.HTTPException(status_code=404, detail="error:" f"Task {id} not found")
@app.get("/stats", summary="Returns task list statistics.")
async def get_stats():
   done_tasks = 0
   open_tasks = 0
   for task in task_list:
      if task["done"] == "True":
         done_tasks += 1
      else:
         open_tasks += 1
   return {"total": len(task_list), "done": done_tasks, "open": open_tasks}
@app.post("/tasks", summary="Adds a new task. Enter a title and information whether the task is done (False/True)")
# Added default = "" to bypass Pydantic's default validation mechanism.
async def add_task(title: str = fastapi.Body(default="", embed=True), done: bool = fastapi.Body(default = "", embed=True)):
    if title != "":
      task = {"id": f"{str(len(task_list) + 1)}", "title": f"{title}", "done": f"{done}"}
      task_list.append(task)
      return task
    else:
      raise fastapi.HTTPException(status_code=400, detail="Title cannot be empty.")  
@app.post("/reset", summary="Reset the task list to the default tasks.")
async def reset():
   del task_list[len(task_list):3:-1]
   return {"Detail": "Reset the task list to the default tasks." }
@app.put("/tasks/{id}", summary="Updates a task by adding a title, information whether the task is done (False/True) or both.")
async def update_task(id:int, title: str = fastapi.Body(default="", embed=True), done: bool = fastapi.Body(default = "", embed=True)):
# Added the option to set the task's status on creation. Scenario: Maybe a user wants to simply record a task they have finished.
   if title != "":
            for task in task_list:
               if task["id"] == str(id):
                   task["title"] = title
                   task["done"] = str(done)
                   return task
            raise fastapi.HTTPException(status_code=404, detail="Unknown id")
   else:
      raise fastapi.HTTPException(status_code=400, detail="Empty/invalid body")
@app.delete("/tasks/{id}", summary="Deletes a task by entering its ID.")
async def delete_task(id:int) -> dict[str, Any]:
   for task in task_list:
      if task["id"] == str(id):
         del task_list[int(id) - 1]
         return {"status": 204, "detail": "No Content" }
   raise fastapi.HTTPException(status_code=404, detail="Unknown id")