from datetime import timedelta
from typing import List

from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from . import auth, db, models, queries

app = FastAPI()

# Role-based dependencies
admin_required = auth.RoleChecker("admin")
readonly_or_admin = auth.RoleChecker("readonly", "admin")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.get("/tasks", response_model=List[models.Task])
def list_tasks(user: models.User = Depends(auth.get_current_user),
               allowed: bool = Depends(readonly_or_admin)):
    """
    Retrieves all tasks for authenticated users with admin or readonly role.

    Args:
        user (models.User): The current authenticated user.
        allowed (bool): Dependency to enforce role check.

    Returns:
        List[models.Task]: A list of tasks.
    """
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            return queries.get_all_tasks(cur)


@app.get("/tasks/{task_id}", response_model=models.Task)
def get_task(task_id: int, user: models.User = Depends(auth.get_current_user),
             allowed: bool = Depends(readonly_or_admin)):
    """
    Retrieves a specific task by ID for authenticated users with admin or readonly role.

    Args:
        task_id (int): ID of the task.
        user (models.User): The current authenticated user.
        allowed (bool): Dependency to enforce role check.

    Returns:
        models.Task: The requested task if found.

    Raises:
        HTTPException: If task is not found.
    """
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            task = queries.get_task_by_id(cur, task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return task


@app.post("/tasks", response_model=models.Task)
def create_task(task: models.TaskCreate, user: models.User = Depends(auth.get_current_user),
                allowed: bool = Depends(admin_required)):
    """
    Creates a new task. Only accessible to users with admin role.

    Args:
        task (models.TaskCreate): Task creation data.
        user (models.User): The current authenticated user.
        allowed (bool): Dependency to enforce admin role.

    Returns:
        models.Task: The newly created task.
    """
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            new_task = queries.create_task(cur, task.name)
            conn.commit()
            return new_task


@app.put("/tasks/{task_id}", response_model=models.Task)
def update_task(task_id: int, name: str = Body(...), status: str = Body(...),
                user: models.User = Depends(auth.get_current_user),
                allowed: bool = Depends(admin_required)):
    """
    Updates an existing task's name and status. Admin-only access.

    Args:
        task_id (int): ID of the task to update.
        name (str): New name for the task.
        status (str): New status for the task.
        user (models.User): The current authenticated user.
        allowed (bool): Dependency to enforce admin role.

    Returns:
        models.Task: The updated task.

    Raises:
        HTTPException: If task is not found.
    """
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            task = queries.update_task(cur, task_id, name, status)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            conn.commit()
            return task


@app.delete("/tasks/{task_id}", response_model=models.Task)
def delete_task(task_id: int, user: models.User = Depends(auth.get_current_user),
                allowed: bool = Depends(admin_required)):
    """
    Deletes a task by ID. Only accessible to users with admin role.

    Args:
        task_id (int): ID of the task to delete.
        user (models.User): The current authenticated user.
        allowed (bool): Dependency to enforce admin role.

    Returns:
        models.Task: The deleted task.

    Raises:
        HTTPException: If task is not found.
    """
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            task = queries.delete_task(cur, task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            conn.commit()
            return task


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and returns a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): Contains username and password fields.

    Returns:
        dict: Access token and token type.
    """
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}