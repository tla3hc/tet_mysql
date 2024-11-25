# FILE: add_employee.py
# AUTHOR: Tran Danh Lam 
# CREATED: 2024-11-25
# MODIFIED: 2024-11-25
# DESCRIPTION: This module contains the AddEmployee class for adding employees to the database.

from models.modules.database_handler.employees_utils import EmployeesUtils
from models.modules.database_handler import Connector
from models.modules.log import Logger
from configs.config_user import ConfigUserData

class AddEmployee:
    def __init__(self):
        connector = Connector()
        self.conn = connector.connect()
        self.employee_utils = EmployeesUtils(self.conn)
    
    def add(self):
        user_data = ConfigUserData().username
        for user in user_data:
            user_id = user
            user_name = user_data[user]['name']
            email = f'{user_id}@bosch.com'
            self.employee_utils.insert_employee(user_id, user_name, email)