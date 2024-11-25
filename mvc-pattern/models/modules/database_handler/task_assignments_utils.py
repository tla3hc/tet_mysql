import logging
from models.modules.database_handler.operator import Operator
from configs import server as server_config

class TaskAssignmentsUtils(Operator):
    _m_database = server_config.MYSQL_DB_NAME
    
    def __init__(self, conn):
        super().__init__(conn)
        logging.info("Database", "TaskAssignmentsUtils initialized")
    
    def show_task_assignments(self):
        """
        Retrieve and return all task assignment records from the 'task_assignments' database.

        This method switches the current database to 'task_assignments' and executes
        a SQL query to select all records from the 'task_assignments' table.

        Returns:
            list: A list of dictionaries, where each dictionary represents a
              task assignment record from the 'task_assignments' table.
        """
        # Tell mysql to use the database "task_assignments"
        self.use_database(self._m_database)
        query = "SELECT * FROM task_assignments"
        return self.execute(query)

    def insert_task_assignment(self, task_assignment_id, task_id, task_assignment_status, assigned_time, employee_id, project_id, review_finding) -> bool:
        """
        Inserts a new task assignment into the database.
        
        Args:
            task_assignment_id (int): The ID of the task assignment.
            task_id (int): The ID of the task.
            task_assignment_status (str): The status of the task assignment.
            assigned_time (datetime): The time the task was assigned.
            employee_id (int): The ID of the employee.
            project_id (int): The ID of the project.
            review_finding (str): The review finding for the task assignment.
        
        Returns:
            bool: True if the insertion was successful, False otherwise.
            
        Logs:
            Debug: Logs the attempt to insert a task assignment.
            Error: Logs any error that occurs during the insertion process.
        """
        try:
            logging.debug("Database", f"Inserting task assignment: {task_assignment_id}, {task_id}, {task_assignment_status}, {assigned_time}, {employee_id}, {project_id}, {review_finding}")
            self.use_database(self._m_database)
            query = "INSERT INTO task_assignments (TaskAssignmentID, TaskID, TaskAssignmentStatus, AssignedTime, EmployeeID, ProjectID, ReviewFinding) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (task_assignment_id, task_id, task_assignment_status, assigned_time, employee_id, project_id, review_finding)
            self.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("Database", f"Error inserting task assignment: {e}")
            return False
        
    def search_task_assignment_by_task_assignment_id(self, task_assignment_id):
        """
        Searches for a task assignment in the database by task assignment ID.
        
        Args:
            task_assignment_id (int): The ID of the task assignment.
        """
        self.use_database(self._m_database)
        query = "SELECT * FROM task_assignments WHERE TaskAssignmentID = %s"
        values = (task_assignment_id,)
        return self.execute(query, values)
    
    def search_task_assignment_by_task_id(self, task_id):
        """
        Searches for a task assignment in the database by task ID.
        
        Args:
            task_id (int): The ID of the task.
        """
        self.use_database(self._m_database)
        query = "SELECT * FROM task_assignments WHERE TaskID = %s"
        values = (task_id,)
        return self.execute(query, values)
    
    def search_task_assignment_by_employee_id(self, employee_id):
        """
        Searches for a task assignment in the database by employee ID.
        
        Args:
            employee_id (int): The ID of the employee.
        """
        self.use_database(self._m_database)
        query = "SELECT * FROM task_assignments WHERE EmployeeID = %s"
        values = (employee_id,)
        return self.execute(query, values)
    
    def search_task_assignment_by_project_id(self, project_id):
        """
        Searches for a task assignment in the database by project ID.
        
        Args:
            project_id (int): The ID of the project.
        """
        self.use_database(self._m_database)
        query = "SELECT * FROM task_assignments WHERE ProjectID = %s"
        values = (project_id,)
        return self.execute(query, values)
    
    def search_task_assignment_by_task_assignment_status(self, task_assignment_status):
        """
        Searches for a task assignment in the database by task assignment status.
        
        Args:
            task_assignment_status (str): The status of the task assignment.
        """
        self.use_database(self._m_database)
        query = "SELECT * FROM task_assignments WHERE TaskAssignmentStatus = %s"
        values = (task_assignment_status,)
        return self.execute(query, values)
    
    def search_task_assignment_by_employee_id_and_task_assigment_status(self, employee_id, task_assignment_status):
        """
        Searches for a task assignment in the database by employee ID and task assignment status.
        
        Args:
            employee_id (int): The ID of the employee.
            task_assignment_status (str): The status of the task assignment.
        """
        self.use_database(self._m_database)
        query = "SELECT * FROM task_assignments WHERE EmployeeID = %s AND TaskAssignmentStatus = %s"
        values = (employee_id, task_assignment_status)
        return self.execute(query, values)

    def update_task_assignment_status(self, task_assignment_id, task_assignment_status):
        """
        Updates the task assignment status in the database.
        
        Args:
            task_assignment_id (int): The ID of the task assignment.
            task_assignment_status (str): The new status of the task assignment.
        """
        self.use_database(self._m_database)
        query = "UPDATE task_assignments SET TaskAssignmentStatus = %s WHERE TaskAssignmentID = %s"
        values = (task_assignment_status, task_assignment_id)
        self.execute(query, values)
        self.conn.commit()
        
    def update_task_assignment_review_finding(self, task_assignment_id, review_finding):
        """
        Updates the review finding of a task assignment in the database.
        
        Args:
            task_assignment_id (int): The ID of the task assignment.
            review_finding (str): The new review finding for the task assignment.
        """
        self.use_database(self._m_database)
        query = "UPDATE task_assignments SET ReviewFinding = %s WHERE TaskAssignmentID = %s"
        values = (review_finding, task_assignment_id)
        self.execute(query, values)
        self.conn.commit()
    