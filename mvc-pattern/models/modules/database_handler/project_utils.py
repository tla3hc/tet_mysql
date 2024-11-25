# FILE: project_utils.py
# AUTHOR: Tran Danh Lam 
# CREATED: 2024-11-25
# MODIFIED: 2024-11-25
# DESCRIPTION: This module contains the ProjectUtils class for managing projects in the database.

import logging
from models.modules.database_handler.operator import Operator
from configs import server as server_config

class ProjectUtils(Operator):
    _m_database = server_config.MYSQL_DB_NAME
    
    def __init__(self, conn):
        super().__init__(conn) 
        logging.info("Database", "ProjectUtils initialized")
    
    def show_projects(self):
        """
        Retrieve all projects from the 'projects' database.

        This method switches the current database to the one specified by
        self._m_database and executes a query to select all records from
        the 'projects' table.

        Returns:
            list: A list of dictionaries where each dictionary represents a row
              in the 'projects' table.
        """
        # Tell mysql to use the database "projects"
        self.use_database(self._m_database)
        query = "SELECT * FROM projects"
        return self.execute(query)
    
    def insert_project(self, project_id, project_name) -> bool:
        """
        Inserts a new project into the database.

        Args:
            project_id (int): The ID of the project.
            project_name (str): The name of the project.

        Returns:
            bool: True if the insertion was successful, False otherwise.

        Logs:
            Debug: Logs the attempt to insert a project.
            Error: Logs any error that occurs during the insertion process.
        """
        try:
            logging.debug("Database", f"Inserting project: {project_id}, {project_name}")
            self.use_database(self._m_database)
            query = "INSERT INTO projects (ProjectID, Name) VALUES (%s, %s)"
            values = (project_id, project_name)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error inserting project: {e}")
            return False
        
    def search_project_by_name(self, project_name):
        """
        Searches for a project in the database by name.

        Args:
            project_name (str): The name of the project to search for.

        Returns:
            list: A list of dictionaries where each dictionary represents a row
              in the 'projects' table that matches the search criteria.
        """
        try:
            self.use_database(self._m_database)
            query = f"SELECT * FROM projects WHERE Name = '{project_name}'"
            return self.execute(query)
        except Exception as e:
            logging.error("Database", f"Error searching for project: {e}")
            return None
    
    def update_project_id(self, project_name):
        """
        Updates the project ID in the database.

        Args:
            project_name (str): The name of the project to update.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            self.use_database(self._m_database)
            query = f"UPDATE projects SET ProjectID = ProjectID + 1 WHERE Name = '{project_name}'"
            self.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error updating project ID: {e}")
            return False