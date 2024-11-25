# FILE: task_categories_utils.py
# AUTHOR: Tran Danh Lam 
# CREATED: 2024-11-25
# MODIFIED: 2024-11-25
# DESCRIPTION: This module contains the TaskCategoriesUtils class for managing task categories in the database.

import logging
from models.modules.database_handler.operator import Operator
from configs import server as server_config

class TaskCategoriesUtils(Operator):
    _m_database = server_config.MYSQL_DB_NAME
    
    def __init__(self, conn):
        super().__init__(conn)
        logging.info("Database", "TaskCategoriesUtils initialized")
        
    def show_task_categories(self):
        """
        Retrieve and return all task category records from the 'task_categories' database.

        This method switches the current database to 'task_categories' and executes
        a SQL query to select all records from the 'task_categories' table.

        Returns:
            list: A list of dictionaries, where each dictionary represents a
              task category record from the 'task_categories' table.
        """
        # Tell mysql to use the database "task_categories"
        self.use_database(self._m_database)
        query = "SELECT * FROM task_categories"
        return self.execute(query)
    
    def insert_task_category(self, category_id, category_name, project_id) -> bool:
        """
        Inserts a new task category into the database.
        
        Args:
            category_id (int): The ID of the task category.
            category_name (str): The name of the task category.
            project_id (int): The ID of the project.
        
        Returns:
            bool: True if the insertion was successful, False otherwise.
            
        Logs:
            Debug: Logs the attempt to insert a task category.
            Error: Logs any error that occurs during the insertion process.
        """
        try:
            logging.debug("Database", f"Inserting task category: {category_id}, {category_name}, {project_id}")
            self.use_database(self._m_database)
            query = "INSERT INTO task_categories (CategoryID, CategoryName, ProjectID) VALUES (%s, %s, %s)"
            values = (category_id, category_name, project_id)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error inserting task category: {e}")
            return False
    
    def search_task_category_by_name(self, category_name):
        """
        Searches for a task category in the database by name.
        
        Args:
            category_name (str): The name of the task category to search for.
        
        Returns:
            list: A list of dictionaries, where each dictionary represents a
              task category record from the 'task_categories' table.
        """
        self.use_database(self._m_database)
        query = "SELECT * FROM task_categories WHERE CategoryName = %s"
        values = (category_name,)
        return self.execute(query, values)
    
    def search_task_category_by_project_id(self, project_id):
        """
        Searches for a task category in the database by project ID.
        
        Args:
            project_id (int): The ID of the project.
        
        Returns:
            list: A list of dictionaries, where each dictionary represents a
              task category record from the 'task_categories' table.
        """
        self.use_database(self._m_database)
        query = "SELECT * FROM task_categories WHERE ProjectID = %s"
        values = (project_id,)
        return self.execute(query, values)
    
    def search_task_category_by_category_id(self, category_id):
        """
        Searches for a task category in the database by category ID.
        
        Args:
            category_id (int): The ID of the task category.
        
        Returns:
            list: A list of dictionaries, where each dictionary represents a
              task category record from the 'task_categories' table.
        """
        self.use_database(self._m_database)
        query = "SELECT * FROM task_categories WHERE CategoryID = %s"
        values = (category_id,)
        return self.execute(query, values)
    