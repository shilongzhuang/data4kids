import mysql.connector
import pandas as pd


class MySQLConnection:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database
        }
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            print("Connected to MySQL database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from MySQL database")

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            if any(keyword in query.strip().lower() for keyword in ('select', 'show')):
            # if query.strip().lower().startswith('select', 'show'):
                result = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                df = pd.DataFrame(result, columns=columns)
                return df, "Query executed successfully."
            elif any(keyword in query.strip().lower() for keyword in ('insert', 'delete', 'create')):
                self.connection.commit()
                return None, "Query executed successfully."
            else:
                return None, "Invalid SQL query. Supported operations: SELECT, INSERT, DELETE, CREATE"

        except mysql.connector.Error as err:
            return None, str(f"Error: {err}")
