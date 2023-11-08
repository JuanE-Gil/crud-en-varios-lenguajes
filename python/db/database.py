import subprocess
import mysql.connector
import os
import datetime

# Connection with the database
access_database = {
    "host": "localhost",
    "user": "root",
    "password": "admin"
}

# --> Routes
# We get the root of the project folder
parent_folder = os.path.dirname(__file__)

backup_folder = os.path.join(parent_folder, "backup")


class DataBase:
    # Connection and cursor
    def __init__(self, **kwargs):
        """
        The above function initializes a MySQL connector object and sets the cursor, user, and password
        attributes.
        """
        self.connector = mysql.connector.connect(**kwargs)
        self.cursor = self.connector.cursor()
        self.user = kwargs["user"]
        self.password = kwargs["password"]  # obtain dictionary value

    # Decorator for server data report
    def report_database(func):
        def wrapper(self, name_database):
            func(self, name_database)
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
    def show_databases(self):
        """
        The function `show_databases` retrieves and prints a list of all databases in the current database
        server.
        """
        self.cursor.execute("SHOW DATABASES")
        for db in self.cursor:
            print(db)

    # Method for creating databases
    @report_database
    def create_database(self, name_database):
        """
        The function creates a database with the given name if it doesn't already exist and prints a success
        message, otherwise it prints an error message and shows the existing databases.

        :param name_database: The parameter `name_database` is a string that represents the name of the database that
        you want to create
        """
        try:
            self.cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {name_database}")
            print(
                f"The database {name_database} has been created successfully.")
        except:
            print(f"The database '{name_database}' has not been created")

    # Method for deleting databases
    @report_database
    def delete_database(self, name_database):
        """
        The function `delete_database` is used to delete a database and display a list of available databases
        if the specified database is not found.

        :param name_database: The parameter `name_database` is the name of the database that you want to
        eliminate/delete
        """
        try:
            self.cursor.execute(f"DROP DATABASE {name_database}")
            print(f"The database was deleted {name_database} correctly.")
        except:
            print(f"The database '{name_database}' not found.")

    # Create database backups
    def copy_database(self, name_database):
        """
        The function `copy_database` creates a backup of a MySQL database by using the `mysqldump` command and
        saving the output to a file.

        :param name_database: The `name_database` parameter is the name of the database that you want to copy
        """
        # Get the current date and time
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        print(date_time)
        with open(f'{backup_folder}/{name_database}_{date_time}.sql', 'w') as out:
            subprocess.Popen(
                f'"C:/Program Files/MySQL/MySQL Workbench 8.0 CE/"mysqldump --user={self.user} --password={self.password} --databases {name_database}', shell=True, stdout=out)
