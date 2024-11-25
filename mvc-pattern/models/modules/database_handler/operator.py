# FILE: operator.py
# AUTHOR: Tran Danh Lam 
# CREATED: 2024-11-25
# MODIFIED: 2024-11-25
# DESCRIPTION: This module contains the Operator class for executing queries on a MySQL database.

import mysql
import logging

class Operator:
    def __init__(self, conn):
        logging.info("Database", "Operator initialized")
        self.conn = conn
        if not self.check_connection():
            raise Exception("No connection to the database")
        if self.conn and self.check_connection():
            self.cursor = self.conn.cursor()
        else:
            self.cursor = None
    
    def check_connection(self):
        return self.conn.is_connected()
    
    def get_version(self):
        if not self.conn or not self.check_connection():
            logging.error("Database", "No connection to the database")
            return None
        return self.conn.get_server_info()
    
    def execute(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
    
    def use_database(self, database):
        self.execute(f"USE {database}")

    
    