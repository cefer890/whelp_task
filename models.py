from peewee import Model, CharField, TextField
from db.database import database


class User(Model):
    """
    Model representing the 'users' table in the database.

    Attributes:
        username (CharField): The username of the user.
        email (CharField): The email address of the user.
        password (CharField): The hashed password of the user.
    """
    username = CharField(max_length=50)
    email = CharField(max_length=100)
    password = CharField(max_length=255)

    class Meta:
        database = database


class Task(Model):
    """
    Model representing the 'tasks' table in the database.

    Attributes:
        ip_address (CharField): The IP address associated with the task.
        data (TextField): The data retrieved from the IP data service.
    """
    ip_address = CharField(max_length=255)
    data = TextField()  # Data retrieved from the IP data service

    class Meta:
        database = database


# Connect to the database, create tables if they don't exist, then close the connection
database.connect()
database.create_tables([User, Task])
database.close()
