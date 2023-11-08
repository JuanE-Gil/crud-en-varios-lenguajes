import getpass
import subprocess
import mysql.connector
import os

# Connection with the database
access_db = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "test"
}

# --> Routes
# We get the root of the project folder
folder_principal = os.path.dirname(__file__)

folder_backup = os.path.join(folder_principal, "backup")


class DataBase:
    # Connection and cursor
    def __init__(self, **kwargs):
        """
        The above function initializes a MySQL connector and cursor using the provided keyword
        arguments.
        """
        self.connector = mysql.connector.connect(**kwargs)
        self.cursor = self.connector.cursor()

    # Decorator for server data report
    def report_db(func):
        def wrapper(self, name_db):
            func(self, name_db)
            print(f"These are the database that the server has: ")
            DataBase.show_db(self)
        return wrapper

    # Query Sql
    def query(self, sql):
        """
        The function executes an SQL query and returns the cursor object.

        :param sql: The `sql` parameter is a string that represents the SQL query that you want to execute
        :return: The cursor object is being returned.
        """
        self.cursor.execute(sql)
        return self.cursor

    # Show databases
    def show_db(self):
        """
        The function `show_db` retrieves and prints a list of all databases in the current database
        server.
        """
        self.cursor.execute("SHOW DATABASES")
        for db in self.cursor:
            print(db)

    # Method for creating databases
    @report_db
    def create_db(self, name_db):
        """
        The function creates a database with the given name if it doesn't already exist and prints a success
        message, otherwise it prints an error message and shows the existing databases.

        :param name_db: The parameter `name_db` is a string that represents the name of the database that
        you want to create
        """
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name_db}")
            print(f"The database {name_db} has been created successfully.")
        except:
            print(f"The database '{name_db}' has not been created")

    # Method for deleting databases
    @report_db
    def eliminate_db(self, name_db):
        """
        The function `eliminate_db` is used to delete a database and display a list of available databases
        if the specified database is not found.

        :param name_db: The parameter `name_db` is the name of the database that you want to
        eliminate/delete
        """
        try:
            self.cursor.execute(f"DROP DATABASE {name_db}")
            print(f"The database was deleted {name_db} correctly.")
        except:
            print(f"The database '{name_db}' not found.")

    # Create database backups
    def copy_db(self, name_db):
        with open(f'{folder_backup}/{name_db}.sql', 'w') as out:
            subprocess.Popen(
                f'"C:/Program Files/MySQL/MySQL Workbench 8.0 CE/"mysqldump --user=root --password={getpass.getpass()} --databases {name_db}', shell=True, stdout=out)
