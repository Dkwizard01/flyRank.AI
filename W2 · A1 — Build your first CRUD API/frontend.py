import streamlit as sl
import requests as rq
sl.header("Api test site.")
button1 = sl.button("Call the root API")
url = "http://127.0.0.1:8000"
if button1:
       sl.write(rq.get(url).json())
health_button = sl.button("Call the health API.")
if health_button:
       sl.write(rq.get(url + "/health").json())
tasks_button = sl.button("Get all lists.")
if tasks_button:
       sl.write(rq.get(url + "/tasks").json())
get_task = sl.text_input("Enter list id.")
task_button = sl.button("Get an item from the list using the item's id.")
if (get_task != " "):
       if task_button:
              sl.write(rq.get(url + "/tasks/" + get_task).json())