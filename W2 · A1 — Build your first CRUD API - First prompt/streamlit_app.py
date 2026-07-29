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

