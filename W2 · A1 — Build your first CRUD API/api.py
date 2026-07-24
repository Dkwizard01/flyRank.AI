import fastapi
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
async def root():
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
         else:
             return { "error": f"Task {id} not found" }
     