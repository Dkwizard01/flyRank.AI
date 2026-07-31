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
