# Bonus: the AI rematch #

**Note: The code in this branch shall not be modified or fixed so the original issues can be easily reproduced without having to check different commits to put together the original broken code.**
## The prompt ##

```text
Build a task CRUD API backend in Python with FastAPI. The tasks are stored in JSON. The task format with the data types that should be used: {"id": (int), "title": (str), "done": (bool)}
The backend must be connected to a web app built with Streamlit that can be used to test the functionality. Ex. Call endpoints like: List tasks and add endpoints.
If stated in the following list all query parameters are optional. The backend must have a number of endpoints:
GET /
This returns the basic information about the API such as version and purpose.
GET /health
This endpoint returns the health status of the API.
GET /tasks
This endpoint returns all the tasks that are currently stored. (This API is not connected to a database. All information is stored in-memory).
GET /tasks/{id}
This endpoint with this specific path parameter returns a task by its id that is specified in said parameter.
GET /tasks?done
This endpoint with this specific query parameter returns tasks that are done if the parameter is set to true or tasks that are not done if the parameter is set to false.
GET /tasks?search
This endpoint with this specific query parameter returns the tasks' titles that contain a string specified in the query parameter.
GET /stats
This endpoint returns the total number of tasks, the number of done tasks and the number of open tasks in the format: {"total": (int), "open": (int), "done": (int)}
POST /tasks
This endpoint adds a new task in the same format as specified earlier.
POST /reset
This endpoint resets the task list to the previous state.
PUT /tasks/{id}
This endpoint updates a task's title, status (done or not done) or both, depending on what was sent in the request. The task to update is specified by its id which is a path parameter.
DELETE tasks/{id}
This endpoint deletes a task by its id which is a path parameter.
All tasks must have adequate HTTP status codes for a successful operation, invalid body or task id.
Swagger UI must be configured and enabled for this task API.
```
## Instructions given by the AI ##
To build a Task CRUD API backend using FastAPI with the specified endpoints and integrate it with a Streamlit web app for testing, follow these steps:

### Backend Development 

1. **Set Up Environment:**

   - Create a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```

   - Install FastAPI and Uvicorn:
     ```bash
     pip install fastapi uvicorn
     ```

2. **Create the FastAPI Application:**

   Create a file named `main.py` for your FastAPI application:

   ```python
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

   ```

3. **Run the Server:**

   Start the FastAPI server with Uvicorn:

   ```bash
   uvicorn main:app --reload
   ```

4. **Swagger UI:**

   Swagger is automatically enabled at `http://localhost:8000/docs`.

### Streamlit Frontend

1. **Set Up Environment:**

   - Install Streamlit:
     ```bash
     pip install streamlit
     ```

2. **Create the Streamlit App:**

   Create a file named `streamlit_app.py`:

   ```python
   import streamlit as st
   import requests

   API_URL = "http://localhost:8000"

   def get_tasks():
       response = requests.get(f"{API_URL}/tasks")
       return response.json()

   def create_task(title):
       task_id = len(get_tasks()) + 1 if get_tasks() else 1
       task = {"id": task_id, "title": title, "done": False}
       response = requests.post(f"{API_URL}/tasks", json=task)
       return response.json()

   def update_task(task_id, new_title=None, done=None):
       task_update = {}
       if new_title:
           task_update['title'] = new_title
       if done is not None:
           task_update['done'] = done
       response = requests.put(f"{API_URL}/tasks/{task_id}", json=task_update)
       return response.json()

   def delete_task(task_id):
       response = requests.delete(f"{API_URL}/tasks/{task_id}")
       return response.status_code

   st.title("Task Manager")

   if st.button('Refresh'):
       tasks = get_tasks()
   
   for task in tasks:
       with st.expander(f"Task {task['id']} - {'Done' if task['done'] else 'Not Done'}"):
           st.write(task['title'])
           new_title = st.text_input("Update Title", value=task['title'], key=f"title_{task['id']}")
           done_status = st.checkbox("Mark as done", value=task['done'], key=f"done_{task['id']}")
           if st.button(f'Update Task {task["id"]}'):
               update_task(task_id=task['id'], new_title=new_title, done=done_status)
           delete_button = st.button(f'Delete Task {task["id"]}')
           if delete_button:
               delete_task(task['id'])
   
   title_input = st.text_input("Task Title")
   if st.button('Add Task'):
       create_task(title=title_input)

   ```

3. **Run the Streamlit App:**

   Start the Streamlit app:

   ```bash
   streamlit run streamlit_app.py
   ```

This setup provides a FastAPI backend with endpoints to manage tasks and a Streamlit frontend for interacting with the API. The API includes all specified functionalities, including task creation, update, deletion, and retrieval based on various criteria. Swagger UI is enabled for easy testing of endpoints directly from the browser.

## Code analysis and feedback ##
### Issues ###

1. Creating a virtual environment.
   - Instructions:
     **Set Up Environment:**

   - Create a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
   The issue:
   The bash command to create the virtual environment did not work as Python on my Windows 11 PC is callable as `python` and not `python3`. This could be seen as an error on my part, since I did not specify the specifics of my setup, but Phi 4 was able to realise that there are different activation commands for virtual environments on Linux and Windows so it is reasonable to assume that it would know about the different naming conventions for the Python command.
2. Type not specified for the list of tasks.
   - Instructions:
     **Create the FastAPI Application:**

       Create a file named `main.py` for your FastAPI application:
       `code`
    - The problem:
      In the given code snippet, the DTO for the task list was declared after the list that is supposed to contain the tasks (`tasks`) is already initialized, which is a problem because a type hint is required for the code to work later on (tasks: list[Task]), therfore the initial API code does not run at all.
      Phi 4 also imports the `Query` function from `fastapi` even though it does not use it anywhere in the code.
3. The delete_tasks() function does not remove a task from the list efficiently. It loops through the task list only assigning the task's whose id does not match the given id.
4. Multiple ommmited error checks
   Phi 4 did not place HTTPException() classes with thw appropriate status codes and error messages for the following path operation fuctions: get_task(), create_task(), delete_task() and reset_tasks().
5. Missing type hint and unbound list variable in streamlit_app.py.
   There is a missing type hint for a `task`variable in the create_task() function. There is also a previously undeclared (unbound) `tasks` variable in a for loop.
   
### Downsides ###
1. Phi 4 did not include a README or a requirements.txt file for easier installation or distribution. 
2. Phi 4 did not set three default tasks. (This requirement was not explicitly specified in the first prompt).
### Improvements ###
1. Phi 4 used Pydantic models to create DTO's for the task and stats.
2. Phi 4 seperated all the API calls for the operations inro seperate functions and then called them based on what button was pressed or data entered.