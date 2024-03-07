from fastapi import FastAPI, HTTPException, Request, Depends, BackgroundTasks
from db.database import database
from models import User, Task
from celery_worker import process_task
from fastapi.openapi.utils import get_openapi
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from schemas import *
import peewee

app = FastAPI()


# Define API routes
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Set URL for Swagger UI
app = FastAPI(
    docs_url="/swagger",
    redoc_url=None,
)


# Customize Swagger documentation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Connect to the MySQL database
database.connect()

# JWT settings
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

# Create a password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create an OAuth2PasswordBearer object
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Create a refresh token
def create_refresh_token(username: str):
    """
    Generates a refresh token for the given username.
    """
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token_data = {"sub": username, "exp": expire}
    refresh_token = jwt.encode(refresh_token_data, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token


@app.post("/api/v1/auth")
async def login(request: Request, login_data: LoginRequest):
    """
    Endpoint for user authentication and token generation.
    """
    username = login_data.username
    password = login_data.password
    user = User.get(username=username)
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(user.username)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# User registration endpoint
@app.post("/api/v1/signup")
async def create_user(user: UserInDB):
    """
    Endpoint for creating a new user.
    """
    try:
        with database.atomic():
            hashed_password = pwd_context.hash(user.password)
            new_user = User.create(username=user.username, email=user.email, password=hashed_password)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def verify_refresh_token(refresh_token: str):
    """
    Verifies the validity of the refresh token.
    """
    try:
        decoded_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except JWTError:
        return False


# Refresh token endpoint
@app.post("/api/v1/refresh")
async def refresh_token(request: Request, refresh_token_data: RefreshTokenRequest):
    """
    Endpoint for refreshing the access token.
    """
    try:
        refresh_token = refresh_token_data.refresh_token
        if not await verify_refresh_token(refresh_token):
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        access_token_expires = timedelta(minutes=30)  # For example, 30 minutes
        access_token = create_access_token(data={"sub": "user"}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


# User authentication
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency function to get the current user based on the access token.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data


@app.get("/api/v1/user", response_model=UserResponse)
async def get_user_details(current_user: User = Depends(get_current_user)):
    """
    Endpoint for returning user details.
    """
    # Logic for returning user details will be added here
    return {"username": current_user.username, "email": "current_user.email"}


# Token creation
def create_access_token(data: dict, expires_delta: timedelta):
    """
    Generates an access token with the given data and expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/api/v1/task", response_model=dict)
async def create_task(task_data: TaskCreate, background_tasks: BackgroundTasks):
    """
    Endpoint for creating a new task.
    """
    background_tasks.add_task(process_task, task_data.ip_address)
    return {"status": "processing", "message": "Task submitted successfully"}


# Connect to the MySQL database on startup
@app.on_event("startup")
async def startup_event():
    """
    Event handler to connect to the MySQL database on application startup.
    """
    # database.connect()
    database.create_tables([User, Task])


# Endpoint for querying task status
@app.get("/api/v1/status/{task_id}", response_model=dict)
async def get_task_status(task_id: str):
    """
    Endpoint for querying the status of a task.
    """
    try:
        task = Task.get(Task.id == task_id)
        return {"task_status": "completed", "result": task.data}
    except peewee.DoesNotExist:
        return {"task_status": "not_found", "message": "Task not found"}


# Close the MySQL database connection on shutdown
@app.on_event("shutdown")
def shutdown_event():
    """
    Event handler to close the MySQL database connection on application shutdown.
    """
    database.close()