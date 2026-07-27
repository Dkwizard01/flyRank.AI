import fastapi
from typing import Any
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
@app.get("/tasks", summary="Gets all tasks.")
async def tasks(done: str | None = None, search : str | None = None):
    if done != None and  done.casefold() == "true":
      return (task for task in task_list if task["done"] == "True")
    elif done != None and done.casefold() == "false":
      return (task for task in task_list if task["done"] == "False")
    if search != None and search != "":
       for task in task_list:
          if search in task["title"]:
             return task
    return task_list
@app.get("/tasks/{id}", summary="Gets a task from the list using the item's id.")
async def get_task(id:str):
     for task in task_list:
         if task["id"] == id:
          return task
     raise fastapi.HTTPException(status_code=404, detail="error:" f"Task {id} not found")
@app.post("/tasks", summary="Adds a new task. Enter a title and information whether the task is done (False/True)")
# Added default = "" to bypass Pydantic's default validation mechanism.
async def add_task(title: str = fastapi.Body(default="", embed=True), done: str = fastapi.Body(default = "", embed=True)):
    if title != "" and done != "":
      task = {"id": f"{str(len(task_list) + 1)}", "title": f"{title}", "done": f"{done}"}
      task_list.append(task)
      return task
    else:
      raise fastapi.HTTPException(status_code=400, detail="Title cannot be empty.")  
@app.put("/tasks/{id}", summary="Updates a task by adding a title, information whether the task is done (False/True) or both.")
async def update_task(id:str, title: str = fastapi.Body(default="", embed=True), done: str = fastapi.Body(default = "", embed=True)):
# Added the option to set the task's status on creation. Scenario: Maybe a user wants to simply record a task they have finished.
   if title != "" and done != "":
            for task in task_list:
               if task["id"] == id:

                   task["title"] = title
                   task["done"] = done
                   return task
            raise fastapi.HTTPException(status_code=404, detail="Unknown id")
   elif title != "":
    for task in task_list:
        if task["id"] == id:
            task["title"] = title
            return task
    raise fastapi.HTTPException(status_code=404, detail="Unknown id")
   elif done != "":
         for task in task_list:
            if task["id"] == id:
               task["done"] = done
               return task
         raise fastapi.HTTPException(status_code=404, detail="Unknown id")
   else:
      raise fastapi.HTTPException(status_code=400, detail="Empty/invalid body")
@app.delete("/tasks/{id}", summary="Deletes a task by entering its ID.")
async def delete_task(id:str) -> dict[str, Any]:
   for task in task_list:
      if task["id"] == id:
         del task_list[int(id) - 1]
         return {"status": 204, "detail": "No Content" }
   raise fastapi.HTTPException(status_code=404, detail="Unknown id")