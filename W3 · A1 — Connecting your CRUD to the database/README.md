# Adding an SQLite database #

This directory contains files for _W3 · A2 — Connecting to the database_ of the free, online and non-paid FlyRank AI internship.

## Why SQLite was chosen ##

SQLIte was chosen because it is a fast, reliable and simple on-disk relational database that makes it easy to store basic task data and allows later expansion with foreign keys if necessary. 

The database file is named `tasks.db` and is stored in the ```W3 · A2 — Connecting to the database``` directory. If the Project was installed correctly by folowing the instructions outlined in the README located in the ```W2 · A1 — Build your first CRUD API``` directory, no additional setup steps need to be taken. The `set_up()` function will create a new database table named `tasks` if a table of the same name does not exist.

## Database screenshot ##

**Database structure:**

![Database structure](<images/DB structure.jpg>)

**Database data:**

![Database data](<images/DB data.jpg>)

## Example command ##
**One example group of SQL commmands:**
"""
      UPDATE tasks
      SET title = ?, done = ?
      WHERE id = ?;
       """
    - This command is run using the execute() function which is a part of the cursor class.