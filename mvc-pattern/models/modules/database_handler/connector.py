# FILE: connector.py
# AUTHOR: Tran Danh Lam 
# CREATED: 2024-11-25
# MODIFIED: 2024-11-25
# DESCRIPTION: This module contains the Connector class for managing MySQL database connections.

import mysql.connector as connector
from configs import server as server_config
import logging

class Connector:
    def __init__(self):
        self.server = server_config.MYSQL_SERVER
        self.port = server_config.MYSQL_PORT
        self.user = server_config.MYSQL_USER
        self.password = server_config.MYSQL_PASSWORD
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = connector.connect(
                host=self.server,
                port=self.port,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            logging.info("Database", "Connection established")
            return self.connection
        except connector.Error as e:
            logging.error("Database", f"Error connecting to the database: {e}")
            return None

    def execute(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()