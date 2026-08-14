import sqlite3
from pathlib import Path
from typing import Any

base_dir = Path(__file__).resolve().parent
database_dir = base_dir / "tasks.db"
connection = sqlite3.connect(database_dir)
connection.row_factory = sqlite3.Row

def set_up() -> dict[str, Any] | None:
 cursor = connection.cursor()
 cursor.execute(
    """
  CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT,
    done INTEGER
    );
    """
 )
 cursor.execute("SELECT 1 FROM tasks LIMIT 1;")
 is_empty = cursor.fetchone() is None
 if is_empty:
     to_insert: list[tuple[int, str, int]] = [
    (1, 'First task.', 1),
    (2, 'First task.', 1),
    ( 3, 'Third task.', 0)
   ]
     cursor.executemany("INSERT INTO tasks (id, title, done) VALUES (?,?,?);", to_insert)
 else:
    return {"status_code": 204, "detail": "No Content"}
 connection.commit()
def get_all():
   cursor = connection.cursor()
   cursor.execute("SELECT * FROM tasks")
   tasks = cursor.fetchall()

   return [dict(row) for row in tasks]
def search_by_id(task_id:int):
   cursor = connection.cursor()
   cursor.execute("SELECT * FROM tasks WHERE id = (?) LIMIT 1;", [task_id])
   selected = cursor.fetchone()
   return dict(selected) if selected else None
def insert(title:str, done:int):
   cursor = connection.cursor()
   try:
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?,?);", [title, done])
    connection.commit()
   except sqlite3.IntegrityError as e:
      print(f"Error: Integrity constraint violated: {e}")
   except sqlite3.OperationalError as e:
        print(f"Error: Operational error: {e}")
   except Exception as e:
        print(f"An exception occurred: {e}")
   return cursor.lastrowid
def update_task(id:int, title:str | None = None, done:int | None = None) -> dict[str, Any]:
   cursor = connection.cursor()
   params: list[str|None |int |None | int]  = [title, done, id]
   try:
    if title is not None:
     cursor.execute("""
      UPDATE tasks
      SET title = ?
      WHERE id = ?;
       """, params[0::2]
    )
    elif done is not None:
        cursor.execute("""
            UPDATE tasks
            SET done = ?
            WHERE id = ?;
             """, params[1:2]
         )
    elif title is not None and done is not None:
        cursor.execute("""
      UPDATE tasks
      SET title = ?, done = ?
      WHERE id = ?;
       """, params
   )
    connection.commit()
   except sqlite3.IntegrityError as e:
      print(f"Error: Integrity constraint violated: {e}")
   except sqlite3.OperationalError as e:
        print(f"Error: Operational error: {e}")
   except Exception as e:
        print(f"An exception occurred: {e}")
   if cursor.row_factory == 0:
      return {"status_code":404, "detail":"Unknown id"}
   return  {"status_code": 200, "detail": "Task updated sucessfully."}
def delete_task(id:int) -> dict[str, Any]:
   cursor = connection.cursor()
   try:
    cursor.execute("""
   DELETE FROM tasks
   WHERE id=?; 
""", [id])
    connection.commit()
   except sqlite3.IntegrityError as e:
      print(f"Error: Integrity constraint violated: {e}")
   except sqlite3.OperationalError as e:
        print(f"Error: Operational error: {e}")
   except Exception as e:
        print(f"An exception occurred: {e}")
   connection.commit()
   if cursor.rowcount == 0:
     return {"status_code":404, "detail":"Unknown id"}
   return {"status": 204, "detail": "No Content" }
set_up()