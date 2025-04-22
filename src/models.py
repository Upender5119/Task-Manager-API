from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    """
    TaskBase is a Pydantic model that represents the base structure for a task.

    Attributes:
        name (str): The name of the task.
    """
    name: str


class TaskCreate(TaskBase):
    """
    Represents the creation of a task, inheriting from the base task model.

    This class is used to define the structure for creating a new task.
    It inherits all attributes and methods from the `TaskBase` class without
    adding any additional functionality or attributes.

    Attributes:
        Inherits all attributes from `TaskBase`.
    """
    pass


class Task(TaskBase):
    """
    Task model representing a task entity.
    Attributes:
        id (int): Unique identifier for the task.
        status (str): Current status of the task.
        created_at (datetime): Timestamp when the task was created.
        updated_at (datetime): Timestamp when the task was last updated.
    Config:
        orm_mode (bool): Enables compatibility with ORM objects.
    """
    id: int
    name: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        Config class for Pydantic model configuration.

        Attributes:
            orm_mode (bool): Enables compatibility with ORMs by allowing the model
                to read data as dictionaries or ORM objects.
        """
        orm_mode = True


class User(BaseModel):
    """
    Represents a user in the system.

    Attributes:
        username (str): The username of the user.
        role (str): The role assigned to the user (e.g., admin, editor, viewer).
    """
    username: str
    role: str


class MyModel(BaseModel):
    """
    MyModel is a data model class that inherits from BaseModel. It is designed to 
    represent and validate data structures.
    Attributes:
        Config (class): A nested configuration class that specifies model behavior.
            - from_attributes (bool): Enables the model to populate fields from 
              attributes of an object, similar to the `orm_mode` setting.
    """

    class Config:
        """
        Configuration class for the model.

        Attributes:
            from_attributes (bool): Indicates whether the model should be populated 
                from attributes instead of using ORM mode.
        """
        from_attributes = True  # instead of orm_mode = True
