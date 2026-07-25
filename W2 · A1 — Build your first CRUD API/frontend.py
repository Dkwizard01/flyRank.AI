import streamlit as sl
import requests as rq
sl.header("Api test site.")
button1 = sl.button("Call the root API")
url = "http://127.0.0.1:8000"
if button1:
       sl.write(rq.get(url).json())
health_button = sl.button("Call the health API.")
if health_button:
       sl.write(rq.get(f"{url}/health").json())
tasks_button = sl.button("Get all tasks.")
if tasks_button:
       sl.write(rq.get(f"{url}/tasks").json())
get_task = sl.text_input("Enter task id.")
task_button = sl.button("Get an item from the list using the item's id.")
if (get_task.strip() != " " and task_button):
              sl.write(rq.get(f"{url}/tasks/{get_task}").json())
add_title = sl.text_input("Enter a title:")
add_button = sl.button("Add new task")
if (add_title.strip() != "" and add_button):
        sl.write(rq.post(f"{url}/tasks", json={"title": add_title.strip()}).json())