from peewee import MySQLDatabase

# MySQL database connection
database = MySQLDatabase(
    "mydatabase",  # MySQL database name
    user="myuser",   # MySQL username
    password="Test=12345",  # MySQL password
    host="localhost",     # MySQL server address
    port=3306,            # MySQL port number
)

