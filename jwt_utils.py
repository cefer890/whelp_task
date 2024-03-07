from datetime import datetime, timedelta
from typing import Optional
import os
from jose import jwt, JWTError

# Encryption algorithm and key
ALGORITHM = "HS256"
SECRET_KEY = os.environ.get('SECRET_KEY')

# Token expiration time (e.g., 1 hour)
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Generates a JWT access token with the provided data and expiration time.

    :param data: The data to encode into the token.
    :param expires_delta: The optional expiration time for the token. If not provided, a default expiration time is used.
    :return: The generated JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Token verification
def verify_token(token: str):
    """
    Verifies the provided JWT token.

    :param token: The JWT token to verify.
    :return: The payload of the token if verification is successful, None otherwise.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
