# FlyRank AI #
This repository contains files for _W2 · A1 — Build your first CRUD API_ of the free, online and non-paid FlyRank AI internship. See:

https://internship.flyrank.ai/

## Installation and usage guide ##
### Installation ###
To install this Streamlit task app, simply clone the project files and first run the command:
```
pip install -r requirements.txt
```
** This commmand is used to install the required packages and must be run in the directory where the `requirements.txt` file is located.
**Note:** When installing packages it is recommended to install them in a virtual environment. You can create a virtual environment by running the commmand:

````
python -m venv <the desired name of your virtual environment>
```

 After all of the dependencies have been installed, run the FastAPI backend with the command:
```
fastapi dev   
``` 
** The command must be run in the directory where the `controller.py` file is located. **

After the backend starts, run the following command to start the streamlit web app:

```
streamlit run frontend.py
```

** The command must be run in the directory where the `frontend.py` file is located. **
### Usage ###
You can view the app on localhost or your local network to start adding tasks.

## Streamlit web UI ##
 ![Streamlit 1](<W2 · A1 — Build your first CRUD API/Streamlit 1.png>) 
 
 ![Streamlit 2](<W2 · A1 — Build your first CRUD API/Streamlit 2.png>) 
 
 ![Streamlit 3](<W2 · A1 — Build your first CRUD API/Streamlit 3.png>) 
 
 ![Streamlit 4](<W2 · A1 — Build your first CRUD API/Streamlit 4.png>) 
 
 ![Streamlit 5](<W2 · A1 — Build your first CRUD API/Streamlit 5.png>) 
 
 ![Streamlit 6](<W2 · A1 — Build your first CRUD API/Streamlit 6.png>) 
 
 ![Streamlit 7](<W2 · A1 — Build your first CRUD API/Streamlit 7.png>) 
 
 ![Streamlit 8](<W2 · A1 — Build your first CRUD API/Streamlit 8.png>)
## Swagger UI ##

![Swagger UI 1](W2%20·%20A1%20—%20Build%20your%20first%20CRUD%20 API/Swagger%20UI%201.png)
![Swagger UI 2](W2%20·%20A1%20—%20Build%20your%20first%20CRUD%20 API/Swagger%20UI%202.png)
![Swagger UI 3](W2%20·%20A1%20—%20Build%20your%20first%20CRUD%20 API/Swagger%20UI%203.png)
![Swagger UI 4](W2%20·%20A1%20—%20Build%20your%20first%20CRUD%20 API/Swagger%20UI%204.png)
![Swagger UI 5](W2%20·%20A1%20—%20Build%20your%20first%20CRUD%20 API/Swagger%20UI%205.png)
![Swagger UI 6](W2%20·%20A1%20—%20Build%20your%20first%20CRUD%20 API/Swagger%20UI%206.png)
![Swagger UI 7](W2%20·%20A1%20—%20Build%20your%20first%20CRUD%20 API/Swagger%20UI%207.png)

**Example curl command (PowerShell):**
```powershell
curl.exe -i --% -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\", \"done\":\"Task update\"}"
```

**Expected response:**
`HTTP/1.1 200 OK
date: Sun, 26 Jul 2026 20:29:11 GMT
server: uvicorn
content-length: 50
content-type: application/json

{"id":"1","title":"Buy milk","done":"Task update"}`

## Endpoint table ##
| Endpoint | Request body contents | Endpoint description|
|--------------|----------------------|
| `GET /` | `None` | `Calls the the root information API.`|
| `GET /health` | `None` | `Calls the health API.`|
| `GET /tasks` | `None` | `Gets all tasks.`|
| `GET /tasks/{id}` | `None` | `Gets a task from the list using the item's id.`|
| `POST /tasks` | `title: **str**, done: **str**` | `Adds a task by adding a title, information whether the task is done (False/True) or both.`|
| `PUT /tasks/{id}` | `title: **str**, done: **str**` | `Updates a task by adding a title, information whether the task is done (False/True) or both.`|
| `DELETE /tasks/{id}` | `None` | `Deletes a task by entering its ID.`|
