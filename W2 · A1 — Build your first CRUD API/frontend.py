import streamlit as sl
import requests as rq
sl.header("To-do task app API test site.")
get_task = sl.text_input("Enter task ID:")
add_title = sl.text_input("Enter the task's title:")
done_input = sl.checkbox("Is the task done? Checked: Done. Unchecked: Not done.")
search_term = sl.text_input("Enter the text to search for in tasks' titles:")
filter_true = sl.checkbox("Display done tasks")
filter_false = sl.checkbox("Display not done tasks")
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
task_button = sl.button("Get a task from the list using the item's id.")
if (get_task.strip() != "" and task_button):
              sl.write(rq.get(f"{url}/tasks/{get_task}").json())
add_button = sl.button("Add a new task. Enter a title and information whether the task is done (False/True)")
if (add_title.strip() != "" and add_button):
        sl.write(rq.post(f"{url}/tasks", json={"title": add_title.strip(), "done": done_input}).json())
update_button = sl.button("Update a task by adding a title, information whether the task is done (False/True) or both.")
if update_button:
   if add_title != "":
           sl.write(rq.put(f"{url}/tasks/{get_task}", json={"title": add_title.strip(), "done": done_input}).json())
   else:
              sl.write(rq.put(f"{url}/tasks/{get_task}", json={"done": done_input}).json())

# The backend could be queried to find out whether the task has already been set to done or not done before updating it,
# but that would involve making an extra API call, which would ultimately reduce response time. 
# In the end, it does not cost the beackend anything to reassign the value to the task even if they are the same. 
delete_button = sl.button("Delete a task by entering its ID.")
if get_task != "" and delete_button:
        sl.write(rq.delete(f"{url}/tasks/{get_task}").json())   
if filter_true:
        sl.write(rq.get(f"{url}/tasks/?done=true").json())
if filter_false:
        sl.write(rq.get(f"{url}/tasks/?done=false").json())
search_button = sl.button("Search for text in tasks' titles.")
if search_button:
        sl.write(rq.get(f"{url}/tasks/?search={search_term}").json())
stats_button = sl.button("Get total number of tasks, done tasks and open tasks.")
if stats_button:
        sl.write(rq.get(f"{url}/stats").json())
reset_button = sl.button("Reset the task list to default")
if reset_button:
        sl.write(rq.post(f"{url}/reset").json())