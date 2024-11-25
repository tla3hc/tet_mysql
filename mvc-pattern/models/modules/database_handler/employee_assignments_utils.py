# FILE: employee_assignments_utils.py
# AUTHOR: Tran Danh Lam 
# CREATED: 2024-11-25
# MODIFIED: 2024-11-25
# DESCRIPTION: This module contains the EmployeeAssignmentUtils class for managing employee assignments in the database.

import logging
from models.modules.database_handler.operator import Operator
from configs import server as server_config

class EmployeeAssignmentUtils:
    _m_database = server_config.MYSQL_DB_NAME
    
    def __init__(self, conn):
        super().__init__(conn)
        logging.info("Database", "EmployeeAssignmentUtils initialized")
        
    def show_employee_assignments(self):
        """
        Retrieve and return all employee assignment records from the 'employee_assignments' database.

        This method switches the current database to 'employee_assignments' and executes
        a SQL query to select all records from the 'employee_assignments' table.

        Returns:
            list: A list of dictionaries, where each dictionary represents an
              employee assignment record from the 'employee_assignments' table.
        """
        # Tell mysql to use the database "employee_assignments"
        self.use_database(self._m_database)
        query = "SELECT * FROM employee_assignments"
        return self.execute(query)
    
    def insert_employee_assignment(self, employee_assignment_id, employee_id, project_id) -> bool:
        """
        Inserts a new employee assignment into the database.

        Args:
            employee_assignment_id (int): The ID of the employee assignment.
            employee_id (int): The ID of the employee.
            project_id (int): The ID of the project.

        Returns:
            bool: True if the insertion was successful, False otherwise.

        Logs:
            Debug: Logs the attempt to insert an employee assignment.
            Error: Logs any error that occurs during the insertion process.
        """
        try:
            logging.debug("Database", f"Inserting employee assignment: {employee_assignment_id}, {employee_id}, {project_id}")
            self.use_database(self._m_database)
            query = "INSERT INTO employee_assignments (EmployeeAssignmentID, EmployeeID, ProjectID) VALUES (%s, %s, %s)"
            values = (employee_assignment_id, employee_id, project_id)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error inserting employee assignment: {e}")
            return False    
    
    def search_employee_assignment_by_employee_id(self, employee_id):
        """
        Searches for an employee assignment in the database by employee ID.
        
        Args:
            employee_id (int): The ID of the employee.
        """
        try:
            self.use_database(self._m_database)
            query = "SELECT * FROM employee_assignments WHERE EmployeeID = %s"
            values = (employee_id,)
            return self.execute(query, values)
        except Exception as e:
            logging.error("Database", f"Error searching for employee assignment by employee ID: {e}")
            return None
    
    def  search_employee_assignment_by_project_id(self, project_id):
        """
        Searches for an employee assignment in the database by project ID.
        
        Args:
            project_id (int): The ID of the project.
        """
        try:
            self.use_database(self._m_database)
            query = "SELECT * FROM employee_assignments WHERE ProjectID = %s"
            values = (project_id,)
            return self.execute(query, values)
        except Exception as e:
            logging.error("Database", f"Error searching for employee assignment by project ID: {e}")
            return None
    
    def search_employee_assignment_by_employee_id_and_project_id(self, employee_id, project_id):
        """
        Searches for an employee assignment in the database by employee ID and project ID.
        
        Args:
            employee_id (int): The ID of the employee.
            project_id (int): The ID of the project.
        """
        try:
            self.use_database(self._m_database)
            query = "SELECT * FROM employee_assignments WHERE EmployeeID = %s AND ProjectID = %s"
            values = (employee_id, project_id)
            return self.execute(query, values)
        except Exception as e:
            logging.error("Database", f"Error searching for employee assignment by employee ID and project ID: {e}")
            return None
    
    def search_employee_assignment_by_employee_assignment_id(self, employee_assignment_id):
        """
        Searches for an employee assignment in the database by employee assignment ID.
        
        Args:
            employee_assignment_id (int): The ID of the employee assignment.
        """
        try:
            self.use_database(self._m_database)
            query = "SELECT * FROM employee_assignments WHERE EmployeeAssignmentID = %s"
            values = (employee_assignment_id,)
            return self.execute(query, values)
        except Exception as e:
            logging.error("Database", f"Error searching for employee assignment by employee assignment ID: {e}")
            return None