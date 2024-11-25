# FILE: time_entries_utils.py
# AUTHOR: Tran Danh Lam 
# CREATED: 2024-11-25
# MODIFIED: 2024-11-25
# DESCRIPTION: This module contains the TimeEntriesUtils class for managing time entries in the database.

import logging
from models.modules.database_handler.operator import Operator
from configs import server as server_config

class TimeEntriesUtils(Operator):
    _m_database = server_config.MYSQL_DB_NAME
    
    def __init__(self, conn):
        super().__init__(conn)
        logging.info("Database", "TimeEntriesUtils initialized")
        
    def show_time_entries(self):
        """
        Retrieve and return all time entry records from the 'time_entries' database.

        This method switches the current database to 'time_entries' and executes
        a SQL query to select all records from the 'time_entries' table.

        Returns:
            list: A list of dictionaries, where each dictionary represents a
              time entry record from the 'time_entries' table.
        """
        # Tell mysql to use the database "time_entries"
        self.use_database(self._m_database)
        query = "SELECT * FROM time_entries"
        return self.execute(query)
    
    def insert_time_entry(self, time_entry_id, task_assignment_id, date, duration) -> bool:
        """
        Inserts a new time entry into the database.
        
        Args:
            time_entry_id (int): The ID of the time entry.
            task_assignment_id (int): The ID of the task assignment.
            date (datetime): The date of the time entry.
            duration (int): The duration of the time entry.
            
        Returns:
            bool: True if the insertion was successful, False otherwise.
        
        Logs:
            Debug: Logs the attempt to insert a time entry.
            Error: Logs any error that occurs during the insertion process.
        """
        try:
            logging.debug("Database", f"Inserting time entry: {time_entry_id}, {task_assignment_id}, {date}, {duration}")
            self.use_database(self._m_database)
            query = "INSERT INTO time_entries (TimeEntryID, TaskAssignmentID, Date, Duration) VALUES (%s, %s, %s, %s)"
            values = (time_entry_id, task_assignment_id, date, duration)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error inserting time entry: {e}")
            return False
        
    def search_time_entry_by_task_assignment_id(self, task_assignment_id):
        """
        Searches for a time entry in the database by task assignment ID.
        """
        self.use_database(self._m_database)
        query = "SELECT * FROM time_entries WHERE TaskAssignmentID = %s"
        values = (task_assignment_id,)
        return self.execute(query, values)
    
    def search_time_entry_by_id(self, time_entry_id):
        """
        Searches for a time entry in the database by time entry ID.
        """
        self.use_database(self._m_database)
        query = "SELECT * FROM time_entries WHERE TimeEntryID = %s"
        values = (time_entry_id,)
        return self.execute(query, values)
    
    def update_time_entry_duration(self, time_entry_id, new_duration) -> bool:
        """
        Updates the duration of a time entry in the database.
        
        Args:
            time_entry_id (int): The ID of the time entry.
            new_duration (int): The new duration of the time entry.
        
        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            logging.debug("Database", f"Updating time entry duration: {time_entry_id}, {new_duration}")
            self.use_database(self._m_database)
            query = "UPDATE time_entries SET Duration = %s WHERE TimeEntryID = %s"
            values = (new_duration, time_entry_id)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error updating time entry duration: {e}")
            return False
    
    def update_time_entry_date(self, time_entry_id, new_date) -> bool:
        """
        Updates the date of a time entry in the database.
        
        Args:
            time_entry_id (int): The ID of the time entry.
            new_date (datetime): The new date of the time entry.
            
        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            logging.debug("Database", f"Updating time entry date: {time_entry_id}, {new_date}")
            self.use_database(self._m_database)
            query = "UPDATE time_entries SET Date = %s WHERE TimeEntryID = %s"
            values = (new_date, time_entry_id)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error updating time entry date: {e}")
            return False
        