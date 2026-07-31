# One rematch #
These are the files for the updated prompt given to the Phi 4 model for the "One rematch" sub-task of the AI vs me task.

## Prompt ##
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
Add a README.md file explaining how to install and use the Project. Also, add a requirements.txt file that lists the necessary Python modules/libraries and if using Pydantic models, add type hints for variables that are of the type created from the Pydantic BaseModel class.
```

## Instructions given by the AI ##

Below is a comprehensive guide on building a task CRUD API backend using FastAPI with an in-memory JSON storage and connecting it to a Streamlit web app for testing.

### 1. Project Structure

```
task_api/
│
├── api/
│   ├── main.py
│   └── models.py
│
├── streamlit_app/
│   └── task_app.py
│
├── README.md
└── requirements.txt
```

### 2. `main.py` (FastAPI Backend)

```python
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

```

### 3. `models.py` (Optional Pydantic Model File)

```python
from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str
    done: bool
```

### 4. `task_app.py` (Streamlit Web App)

```python
import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

def list_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    if response.status_code == 200:
        return response.json()
    else:
        return []

def add_task(title, done=False):
    task = {"title": title, "done": done}
    response = requests.post(f"{BASE_URL}/tasks", json=task)
    return response.status_code

def delete_task(task_id):
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    return response.status_code

# Streamlit UI
st.title("Task Management App")

if st.button('Reset Tasks'):
    requests.post(f"{BASE_URL}/reset")
    st.success('Tasks reset!')

st.header("List of Tasks")
tasks = list_tasks()
for task in tasks:
    st.write(f"ID: {task['id']}, Title: {task['title']}, Done: {task['done']}")
    if st.button(f'Delete Task {task["id"]}'):
        delete_task(task['id'])
        tasks.remove(task)
        st.success('Task deleted!')

if st.button("Add Task"):
    title = st.text_input("Task Title")
    done = st.checkbox("Done", value=False)
    if title:
        add_task(title, done)
        st.success('Task added!')
```

### 5. `README.md`

```markdown
# Task Management API

## Overview
This project consists of a FastAPI backend that manages tasks stored in-memory as JSON objects and a Streamlit frontend to interact with the API.

## Backend Installation

1. **Clone the repository**
    ```
    git clone <repository-url>
    cd task_api/api
    ```

2. **Create a virtual environment (optional but recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**
    ```
    pip install -r ../requirements.txt
    ```

4. **Run the FastAPI server**
    ```
    uvicorn main:app --reload
    ```

   The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

5. **Swagger UI Access**
   Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to interact with the API using Swagger.

## Frontend Installation

1. Navigate to the Streamlit app directory:
    ```
    cd ../streamlit_app
    ```

2. Run the Streamlit app:
    ```bash
    streamlit run task_app.py
    ```

   The web app will be available at [http://127.0.0.1:8501](http://127.0.0.1:8501).

## API Endpoints

- `GET /`: Basic information about the API.
- `GET /health`: Health status of the API.
- `GET /tasks`: List all tasks.
- `GET /tasks/{id}`: Get a task by ID.
- `GET /tasks?done={true/false}`: Filter tasks based on completion status.
- `GET /tasks?search={string}`: Search tasks by title.
- `POST /tasks`: Add a new task.
- `PUT /tasks/{id}`: Update an existing task.
- `DELETE /tasks/{id}`: Delete a task.
- `POST /reset`: Reset all tasks.
- `GET /stats`: Get statistics about tasks.

## Notes

- Ensure that both backend and frontend are running to test the functionalities.
```

### 6. `requirements.txt`

```plaintext
fastapi==0.68.1
uvicorn==0.15.0
requests==2.26.0
streamlit==1.11.0
pydantic==1.8.2
```

### Running the Project

1. **Start the FastAPI server:**
   ```bash
   uvicorn api/main:app --reload
   ```

2. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app/task_app.py
   ```

This setup will provide you with a fully functioning task management API and a web interface to interact with it using FastAPI and Streamlit respectively.

## Code analysis and feedback ##

Phi 4 repeats the same mistake with type hinting for the Pydantic model as previously, despite new and explicit instructions. There are multiple non-initialized list variables and there are missing type hints for the return types of functions.
The instruction to install the dependencies: 
**Install dependencies**
    ```
    pip install -r ../requirements.txt
    ```
The extra `.` at the beggining of the command instructs the terminal to look for the requirements.txt file in the parent directory, where it is not located according to the project structure outlined by Phi 4.
