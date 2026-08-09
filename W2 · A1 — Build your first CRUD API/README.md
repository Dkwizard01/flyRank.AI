# FlyRank AI #
This repository contains files for _W2 · A1 — Build your first CRUD API_ of the free, online and non-paid FlyRank AI internship. See:

https://internship.flyrank.ai/

## Installation and usage guide ##
### Installation ###
To install this Streamlit task app, simply clone the project files and first run the command:
```
pip install -r requirements.txt
```
**This commmand is used to install the required packages and must be run in the directory where the `requirements.txt` file is located.**
**Note:** When installing packages it is recommended to install them in a virtual environment. You can create a virtual environment by running the commmand:

```
python -m venv <the desired name of your virtual environment>
```

 After all of the dependencies have been installed, run the FastAPI backend with the command:
```
fastapi dev   
``` 
**The command must be run in the directory where the `controller.py` file is located.**

After the backend starts, run the following command to start the streamlit web app:

```
streamlit run frontend.py
```

**The command must be run in the directory where the `frontend.py` file is located.**
### Usage ###
You can view the app on localhost or your local network to start adding tasks.

## Streamlit web UI ##
![Streamlit 1](<Images/Streamlit/Streamlit 1.png>) 
![Streamlit 2](<Images/Streamlit/Streamlit 2.png>) 
![Streamlit 3](<Images/Streamlit/Streamlit 3.png>) 
![Streamlit 4](<Images/Streamlit/Streamlit 4.png>) 
![Streamlit 5](<Images/Streamlit/Streamlit 5.png>) 
![Streamlit 6](<Images/Streamlit/Streamlit 6.png>) 
![Streamlit 7](<Images/Streamlit/Streamlit 7.png>) 
![Streamlit 6](<Images/Streamlit/Streamlit 8.png>)
## Swagger UI ##

![Swagger UI 1](<Images/SwaggerUI/Swagger UI 1.png>) 
![Swagger UI 2](<Images/SwaggerUI/Swagger UI 2.png>) 
![Swagger UI 3](<Images/SwaggerUI/Swagger UI 3.png>) 
![Swagger UI 4](<Images/SwaggerUI/Swagger UI 4.png>) 
![Swagger UI 5](<Images/SwaggerUI/Swagger UI 5.png>) 
![Swagger UI 6](<Images/SwaggerUI/Swagger UI 6.png>) 
![Swagger UI 7](<Images/SwaggerUI/Swagger UI 7.png>)

**Example curl command (PowerShell):**
```powershell
curl.exe -i --% -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\", \"done\":\"Task update\"}"
```

**Expected response:**

`HTTP/1.1 200 OK`

`date: Sun, 26 Jul 2026 20:29:11 GMT`

`server: uvicorn`

`content-length: 50`

`content-type: application/json`

`{"id":"1","title":"Buy milk","done":"Task update"}`

## Endpoint table ##
| Endpoint | Request body contents | Endpoint description|
|----------|-----------------------|---------------------|
| `GET /` | `None` | `Calls the the root information API.`|
| `GET /health` | `None` | `Calls the health API.`|
| `GET /tasks` | `None` | `Gets all tasks.`|
| `GET /tasks/{id}` | `None` | `Gets a task from the list using the item's id.`|
|`GET /tasks/?done`  | `None` | `Gets all done tasks if the query parameter is set to true. Gets all tasks that are not done if the query parametar is set to false`|
|`GET /tasks/?search`  | `None` | `Gets tasks whose titles' contain the specified keyword(s)`|
|`GET /tasks/?done`  | `None` | `Gets all done tasks if the query parameter is set to true. Gets all tasks that are not done if the query parametar is set to false`|
|`GET /stats`  | `None` | `Gets the total number of tasks, tasks that are done and tasks that are not done.`|
| `POST /tasks` | `title: **str**, done: **str**` | `Adds a task by adding a title, information whether the task is done (False/True) or both.`|
|`POST /reset`  | `None` | `Resets the amount of tasks to default (3).`|
| `PUT /tasks/{id}` | `title: **str**, done: **str**` | `Updates a task by adding a title, information whether the task is done (False/True) or both.`|
| `DELETE /tasks/{id}` | `None` | `Deletes a task by entering its ID.`|

## Issues ##
The task list is not stored in a database, rather it is stored in an in-memory list. Because of that the task list resets every time the server is restarted. 