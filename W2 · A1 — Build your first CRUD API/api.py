import fastapi
from typing import Any
app = fastapi.FastAPI()
task_list = [
   { "id": "1", "title": "First task.", "Done": "True" },
   { "id": "2", "title": "First task.", "Done": "True" },
   { "id": "3", "title": "Third task.", "Done": "False"}
]
      
# Stage 0: hello server
# @app.get("/")
# async def hello_server():
  #  return {"status_code": "200", "message": "Hello World"}
@app.get("/")
async def root() -> dict[str, Any]:
   return  { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }
@app.get("/health")
async def health():
   return { "status": "ok" } 
@app.get("/tasks")
async def tasks():
   return task_list
@app.get("/tasks/{id}")
async def get_task(id:str):
     for task in task_list:
         if task["id"] == id:
          return task
         
     return { "error": f"Task {id} not found" }
@app.post("/tasks")
# Added default = "" to bypass Pydantic's default validation mechanism.
async def add_task(title: str = fastapi.Body(default="", embed=True)):
    if title != "":
      task = {"id": f"{str(len(task_list) + 1)}", "title": f"{title}", "Done": "False"}
      task_list.append(task)
      return task
    else:
        return {"status_code":"400", "message": "Title cannot be empty"} #fastapi.HTTPException(status_code=400, detail="Title cannot be empty.")  
    