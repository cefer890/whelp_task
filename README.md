# Whelp Task

This project includes an application developed using FastAPI, JWT, Peewee, Celery + RabbitMQ, RestAPI, and Swagger.

## Installation

1. Make sure you have Python 3 and pip installed.
2. Create a MySQL database and add the connection details to the `config.py` file.
3. Install RabbitMQ and add the connection settings to the `config.py` file.
4. Navigate to the project folder and install the required dependencies using `pip install -r requirements.txt`.

## Usage

1. Start the application by running the command `uvicorn main:app --reload` in your terminal.
2. Access the Swagger documentation by visiting [http://localhost:8000/swagger](http://localhost:8000/swagger) in your browser.
3. Perform operations using the endpoints.

## Endpoints

1. `/api/v1/auth` - JWT sign in
2. `/api/v1/signup` - Create a user in the MySQL database
3. `/api/v1/refresh` - JWT token refresh
4. `/api/v1/user` - Show basic details of an authorized user
5. `/api/v1/task` - Create a task in MySQL, send it to Celery, and return task ID
6. `/api/v1/status/:id` - Show the result of the task

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
