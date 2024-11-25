# FILE: task_utils.py
# AUTHOR: Tran Danh Lam 
# CREATED: 2024-11-25
# MODIFIED: 2024-11-25
# DESCRIPTION: This module contains the TaskUtils class for managing tasks in the database.

import logging
from models.modules.database_handler.operator import Operator
from configs import server as server_config

class TaskUtils(Operator):
    _m_database = server_config.MYSQL_DB_NAME
    
    def __init__(self, conn):
        super().__init__(conn) 
        logging.info("Database", "TaskUtils initialized")
    
    def show_tasks(self): 
        """
        Retrieve all tasks from the 'tasks' database.

        This method switches the current database to the one specified by
        self._m_database and executes a query to select all records from
        the 'tasks' table.

        Returns:
            list: A list of dictionaries where each dictionary represents a row
              in the 'tasks' table.
        """
        # Tell mysql to use the database "tasks"
        self.use_database(self._m_database)
        query = "SELECT * FROM tasks"
        return self.execute(query)
    
    def insert_task(self, task_id, name, task_status, category_id, requirement_no, is_shared, comment, estimation_time, total_effort, remaining_time) -> bool:
        """
        Inserts a new task into the database.

        Args:
            task_id (int): The ID of the task.
            name (str): The name of the task.
            task_status (str): The status of the task.
            category_id (int): The ID of the category.
            requirement_no (int): The number of the requirement.
            is_shared (bool): Whether the task is shared.
            comment (str): A comment on the task.
            estimation_time (int): The estimated time for the task.
            total_effort (int): The total effort for the task.
            remaining_time (int): The remaining time for the task.
            
        Returns:
            bool: True if the insertion was successful, False otherwise.
            
        Logs:
            Debug: Logs the attempt to insert a task.
            Error: Logs any error that occurs during the insertion process.
        """
        try:
            logging.debug("Database", f"Inserting task: {task_id}, {name}, {task_status}, {category_id}, {requirement_no}, {is_shared}, {comment}, {estimation_time}, {total_effort}, {remaining_time}")
            self.use_database(self._m_database)
            query = "INSERT INTO tasks (TaskID, Name, TaskStatus, CategoryID, RequirementNo, IsShared, Comment, EstimationTime, TotalEffort, RemainingTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (task_id, name, task_status, category_id, requirement_no, is_shared, comment, estimation_time, total_effort, remaining_time)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error inserting task: {e}")
            return False
    
    def get_task_by_id(self, id):
        """
        Searches for a task in the database by ID.

        Args:
            id (int): The ID of the task to search for.

        Returns:
            dict: A dictionary representing the task with the given ID.
        """
        try:
            self.use_database(self._m_database)
            query = "SELECT * FROM tasks WHERE TaskID = %s"
            values = (id,)
            return self.execute(query, values)
        except Exception as e:
            logging.error("Database", f"Error searching for task: {e}")
            return None
    
    def get_task_by_name(self, name):
        """
        Searches for a task in the database by name.

        Args:
            name (str): The name of the task to search for.

        Returns:
            dict: A dictionary representing the task with the given name.
        """
        try:
            self.use_database(self._m_database)
            query = "SELECT * FROM tasks WHERE Name = %s"
            values = (name,)
            return self.execute(query, values)
        except Exception as e:
            logging.error("Database", f"Error searching for task: {e}")
            return None
    
    def get_task_by_category_id(self, category_id):
        """
        Searches for a task in the database by category ID.

        Args:
            category_id (int): The ID of the category to search for.
        
        Returns:
            dict: A dictionary representing the task with the given category ID.
        """ 
        try:
            self.use_database(self._m_database)
            query = "SELECT * FROM tasks WHERE CategoryID = %s"
            values = (category_id,)
            return self.execute(query, values)
        except Exception as e:
            logging.error("Database", f"Error searching for task: {e}")
            return None
    
    def update_task_status(self, task_id, task_status):
        """
        Updates the status of a task in the database.

        Args:
            task_id (int): The ID of the task to update.
            task_status (str): The new status of the task.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            logging.debug("Database", f"Updating task status: {task_id}, {task_status}")
            self.use_database(self._m_database)
            query = "UPDATE tasks SET TaskStatus = %s WHERE TaskID = %s"
            values = (task_status, task_id)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error updating task status: {e}")
            return False
     
    def update_task_comment(self, task_id, comment):
        """
        Updates the comment of a task in the database.

        Args:
            task_id (int): The ID of the task to update.
            comment (str): The new comment for the task.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            logging.debug("Database", f"Updating task comment: {task_id}, {comment}")
            self.use_database(self._m_database)
            query = "UPDATE tasks SET Comment = %s WHERE TaskID = %s"
            values = (comment, task_id)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error updating task comment: {e}")
            return False
    
    def update_task_estimation_time(self, task_id, estimation_time):
        """
        Updates the estimation time of a task in the database.

        Args:
            task_id (int): The ID of the task to update.
            estimation_time (int): The new estimation time for the task.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            logging.debug("Database", f"Updating task estimation time: {task_id}, {estimation_time}")
            self.use_database(self._m_database)
            query = "UPDATE tasks SET EstimationTime = %s WHERE TaskID = %s"
            values = (estimation_time, task_id)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error updating task estimation time: {e}")
            return False
    
    def update_task_total_effort(self, task_id, total_effort):
        """
        Updates the total effort of a task in the database.

        Args:
            task_id (int): The ID of the task to update.
            total_effort (int): The new total effort for the task.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            logging.debug("Database", f"Updating task total effort: {task_id}, {total_effort}")
            self.use_database(self._m_database)
            query = "UPDATE tasks SET TotalEffort = %s WHERE TaskID = %s"
            values = (total_effort, task_id)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error updating task total effort: {e}")
            return False
    
    def update_task_remaining_time(self, task_id, remaining_time):
        """
        Updates the remaining time of a task in the database.

        Args:
            task_id (int): The ID of the task to update.
            remaining_time (int): The new remaining time for the task.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            logging.debug("Database", f"Updating task remaining time: {task_id}, {remaining_time}")
            self.use_database(self._m_database)
            query = "UPDATE tasks SET RemainingTime = %s WHERE TaskID = %s"
            values = (remaining_time, task_id)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error updating task remaining time: {e}")
            return False
    
    def delete_task(self, task_id):
        """
        Deletes a task from the database.

        Args:
            task_id (int): The ID of the task to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            logging.debug("Database", f"Deleting task: {task_id}")
            self.use_database(self._m_database)
            query = "DELETE FROM tasks WHERE TaskID = %s"
            values = (task_id,)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error deleting task: {e}")
            return False
        
        