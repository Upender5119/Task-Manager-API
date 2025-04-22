# auth.py

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import models

# Secret key (in real apps, keep this secret and load via env vars)
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dummy user db
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "secret",  # In real apps, store hashed passwords
        "role": "admin"
    },
    "readonly": {
        "username": "readonly",
        "password": "secret",
        "role": "readonly"
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def authenticate_user(username: str, password: str):
    """
    Authenticates a user by verifying the provided username and password.

    Args:
        username (str): The username of the user attempting to authenticate.
        password (str): The password of the user attempting to authenticate.

    Returns:
        models.User: An instance of the User model if authentication is successful.
        None: If authentication fails due to incorrect username or password.
    """
    user = fake_users_db.get(username)
    if user and user["password"] == password:
        return models.User(username=user["username"], role=user["role"])
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Generates a JSON Web Token (JWT) for the given data with an optional expiration time.

    Args:
        data (dict): The payload data to encode into the JWT.
        expires_delta (Optional[timedelta]): The time duration after which the token will expire. 
            If not provided, the token will expire in 15 minutes by default.

    Returns:
        str: The encoded JWT as a string.
    """
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieve the current user based on the provided JWT token.

    This function decodes the JWT token to extract user information such as
    username and role. If the token is invalid or the required information
    is missing, an HTTP 401 Unauthorized exception is raised.

    Args:
        token (str): The JWT token provided in the request header.

    Returns:
        models.User: An instance of the User model containing the username
        and role of the authenticated user.

    Raises:
        HTTPException: If the token is invalid or the credentials cannot
        be validated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", "")
        role: str = payload.get("role", "")
        if username is None or role is None:
            raise credentials_exception
        return models.User(username=username, role=role)
    except JWTError:
        raise credentials_exception


# RoleChecker Dependency
class RoleChecker:
    """
    A class used to enforce role-based access control by checking if a user's role
    is within the allowed roles.
    Attributes:
        allowed_roles (tuple): A tuple of strings representing the roles that are allowed access.
    Methods:
        __call__(user: models.User = Depends(get_current_user)) -> bool:
            Checks if the user's role is in the allowed roles. Raises an HTTPException
            with a 403 status code if the role is not allowed. Returns True if access is granted.
    """

    def __init__(self, *allowed_roles: str):
        self.allowed_roles = allowed_roles

    def __call__(self, user: models.User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this resource",
            )
        return True
