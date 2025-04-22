def get_all_tasks(cursor):
    """
    Retrieve all tasks from the database, ordered by their ID.

    Args:
        cursor: A database cursor object used to execute SQL queries.

    Returns:
        list: A list of tuples, where each tuple represents a row in the 'tasks' table.
    """
    cursor.execute("SELECT * FROM tasks ORDER BY id;")
    return cursor.fetchall()


def get_task_by_id(cursor, task_id):
    """
    Retrieve a task from the database by its ID.

    Args:
        cursor (object): A database cursor object used to execute SQL queries.
        task_id (int): The ID of the task to retrieve.

    Returns:
        dict or None: A dictionary representing the task if found, or None if no task exists with the given ID.
    """
    cursor.execute("SELECT * FROM tasks WHERE id = %s;", (task_id,))
    return cursor.fetchone()


def create_task(cursor, name):
    """
    Inserts a new task into the 'tasks' table with the given name and a default status of 'running'.

    Args:
        cursor (psycopg2.cursor): The database cursor used to execute the SQL query.
        name (str): The name of the task to be created.

    Returns:
        tuple: A tuple representing the newly created task, as returned by the database.
    """
    cursor.execute("""
        INSERT INTO tasks (name, status, created_at, updated_at)
        VALUES (%s, 'running', now(), now())
        RETURNING *;
    """, (name,))
    return cursor.fetchone()


def update_task(cursor, task_id, name, status):
    """
    Updates a task in the database with the given name and status.

    Args:
        cursor (psycopg2.cursor): The database cursor to execute the query.
        task_id (int): The ID of the task to update.
        name (str): The new name of the task.
        status (str): The new status of the task.

    Returns:
        tuple: The updated task record as a tuple, or None if no task was updated.
    """
    cursor.execute("""
        UPDATE tasks
        SET name = %s,
            status = %s,
            updated_at = now()
        WHERE id = %s
        RETURNING *;
    """, (name, status, task_id))
    return cursor.fetchone()


def delete_task(cursor, task_id):
    """
    Deletes a task from the database by its ID.

    Args:
        cursor (psycopg2.extensions.cursor): The database cursor used to execute the query.
        task_id (int): The ID of the task to be deleted.

    Returns:
        tuple: The deleted task's details as a tuple, or None if no task was deleted.
    """
    cursor.execute("DELETE FROM tasks WHERE id = %s RETURNING *;", (task_id,))
    return cursor.fetchone()
