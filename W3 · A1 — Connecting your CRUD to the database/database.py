import sqlite3
from pathlib import Path

base_dir = Path(__file__).resolve().parent
database_dir = base_dir / "tasks.db"
connection = sqlite3.connect(database_dir)
connection.row_factory = sqlite3.Row


def set_up():
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