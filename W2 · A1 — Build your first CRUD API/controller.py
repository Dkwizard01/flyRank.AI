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
async def tasks(done: bool | None = None, search : str | None = None, alphabetically: bool | None = None):
     if search:
        search_result = database.search_in_title(search)
        if search_result: 
           return search_result
        else:
         raise fastapi.HTTPException(status_code=404, detail="error:" f"No titles containig {search} were found")

     if done:
         filter_result = database.filter_status(done)
         if filter_result:
            return filter_result
         else:
          raise fastapi.HTTPException(status_code=404, detail="error:" "No task with the selected status was found.")
         
     if alphabetically:
        database.sort_alphabetically()
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
   return database.stats()
@app.post("/tasks", summary="Adds a new task. Enter a title and information whether the task is done (False/True)")
# Added default = "" to bypass Pydantic's default validation mechanism.
async def add_task(title: str = fastapi.Body(default="", embed=True), done: bool = fastapi.Body(default = "", embed=True)) -> dict[str, int | str]:
    if title != "":
      database.insert(title, done)
      return {"status code": 201, "detail": "Task added successfully"}
    else:
      raise fastapi.HTTPException(status_code=400, detail="Title cannot be empty.")  
@app.post("/reset", summary="Reset the task list to the default tasks.")
async def reset():
   del task_list[len(task_list):3:-1]
   return {"Detail": "Reset the task list to the default tasks." }
@app.put("/tasks/{id}", summary="Updates a task by adding a title, information whether the task is done (False/True) or both.")
async def update_task(id:int, title: str = fastapi.Body(default="", embed=True), done: bool = fastapi.Body(default = "", embed=True)):
# Added the option to set the task's status on creation. Scenario: Maybe a user wants to simply record a task they have finished.
   if title != "" or done != False:
            result = database.update_task(id, title, done)
            if result["status_code"] != 200:
             raise fastapi.HTTPException(status_code=404, detail="Unknown id")
   else:
      raise fastapi.HTTPException(status_code=400, detail="Empty/invalid body")
   return result
@app.delete("/tasks/{id}", summary="Deletes a task by entering its ID.")
async def delete_task(id:int) -> dict[str, Any]:
   result = database.delete_task(id)
   if result["status_code"] != 204:
    raise fastapi.HTTPException(status_code=404, detail="Unknown id")
   return result