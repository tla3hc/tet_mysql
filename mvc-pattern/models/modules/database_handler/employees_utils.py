# FILE: employees_utils.py
# AUTHOR: Tran Danh Lam 
# CREATED: 2024-11-25
# MODIFIED: 2024-11-25
# DESCRIPTION: This module contains the EmployeesUtils class for managing employees in the database.

import logging
from models.modules.database_handler.operator import Operator
from configs import server as server_config

class EmployeesUtils(Operator):
    _m_database = server_config.MYSQL_DB_NAME
    
    def __init__(self, conn):
        super().__init__(conn)
        logging.info("Database", "EmployeesUtils initialized")
    
    def show_employees(self):
        """
        Retrieve and return all employee records from the 'employees' database.

        This method switches the current database to 'employees' and executes
        a SQL query to select all records from the 'employees' table.

        Returns:
            list: A list of dictionaries, where each dictionary represents an
              employee record from the 'employees' table.
        """
        # Tell mysql to use the database "employees"
        self.use_database(self._m_database)
        query = "SELECT * FROM employees"
        return self.execute(query)
    
    def insert_employee(self, id, name, email) -> bool:
        """
        Inserts a new employee into the database.

        Args:
            id (int): The ID of the employee.
            name (str): The name of the employee.
            email (str): The email address of the employee.

        Returns:
            bool: True if the insertion was successful, False otherwise.

        Logs:
            Debug: Logs the attempt to insert an employee.
            Error: Logs any error that occurs during the insertion process.
        """
        try:
            logging.debug("Database", f"Inserting employee: {id}, {name}, {email}")
            self.use_database(self._m_database)
            query = "INSERT INTO employees (EmployeeID, Name, Email) VALUES (%s, %s, %s)"
            values = (id, name, email)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error inserting employee: {e}")
            return False
        
    def search_employee(self, name):
        """
        Searches for an employee in the database by name.

        Args:
            name (str): The name of the employee to search for.

        Returns:
            list: A list of dictionaries representing the employee records that match the search criteria.
                  Returns None if an error occurs during the search.

        Raises:
            Exception: If there is an error during the database operation.
        """
        try:
            logging.debug("Database", f"Searching for employee: {name}")
            self.use_database(self._m_database)
            query = "SELECT * FROM employees WHERE Name = %s"
            values = (name,)
            return self.execute(query, values)
        except Exception as e:
            logging.error("Database", f"Error searching for employee: {e}")
            return None
    
    def search_employee_by_id(self, id):
        """
        Searches for an employee in the database by their ID.

        Args:
            id (int): The ID of the employee to search for.

        Returns:
            list: A list of dictionaries representing the employee's data if found, otherwise None.

        Logs:
            Debug: Logs the employee ID being searched.
            Error: Logs any error that occurs during the search.
        """
        try:
            logging.debug("Database", f"Searching for employee: {id}")
            self.use_database(self._m_database)
            query = "SELECT * FROM employees WHERE EmployeeID = %s"
            values = (id,)
            return self.execute(query, values)
        except Exception as e:
            logging.error("Database", f"Error searching for employee: {e}")
            return None
    
    def search_employee_by_email(self, email):
        """
        Searches for an employee in the database by their email address.

        Args:
            email (str): The email address of the employee to search for.

        Returns:
            list: A list of dictionaries representing the employee records that match the email address.
            None: If an error occurs during the search.

        Raises:
            Exception: If there is an error executing the database query.
        """
        try:
            logging.debug("Database", f"Searching for employee: {email}")
            self.use_database(self._m_database)
            query = "SELECT * FROM employees WHERE Email = %s"
            values = (email,)
            return self.execute(query, values)
        except Exception as e:
            logging.error("Database", f"Error searching for employee: {e}")
            return None
        
    def update_employee_email_by_id(self, id, email):
        """
        Updates the email address of an employee in the database by their ID.

        Args:
            id (int): The ID of the employee whose email is to be updated.
            email (str): The new email address to be set for the employee.

        Returns:
            bool: True if the update was successful, False otherwise.

        Logs:
            Debug: When the update process starts.
            Error: If an error occurs during the update process.
        """
        try:
            logging.debug("Database", f"Updating employee: {id}")
            self.use_database(self._m_database)
            query = "UPDATE employees SET Email = %s WHERE EmployeeID = %s"
            values = (email, id)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error updating employee: {e}")
            return False
    
    def update_employee_email_by_name(self, name, email):
        """
        Updates the email address of an employee identified by their name in the database.

        Args:
            name (str): The name of the employee whose email address is to be updated.
            email (str): The new email address to be set for the employee.

        Returns:
            bool: True if the update was successful, False otherwise.

        Logs:
            Debug: Logs the attempt to update the employee's email.
            Error: Logs any error that occurs during the update process.
        """
        try:
            logging.debug("Database", f"Updating employee: {name}")
            self.use_database(self._m_database)
            query = "UPDATE employees SET Email = %s WHERE Name = %s"
            values = (email, name)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error updating employee: {e}")
            return False