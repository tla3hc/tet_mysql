# FILE: add_project.py
# AUTHOR: Tran Danh Lam 
# CREATED: 2024-11-25
# MODIFIED: 2024-11-25
# DESCRIPTION: This module contains the AddProject class for adding projects to the database.

from models.modules.database_handler import Connector
from models.modules.log import Logger
from configs.config_user import ConfigUserData
from models.modules.database_handler.project_utils import ProjectUtils

class AddProject:
    def __init__(self):
        connector = Connector()
        self.conn = connector.connect()
        self.project_utils = ProjectUtils(self.conn)
    
    def add(self):
        user_data = ConfigUserData().username
        project_list = []
        
        for user in user_data:
            user_project = user_data[user]['project']
            if not user_project in project_list:
                project_list.append(user_project)
        # Sort the project list alphabetically
        project_list.sort()
        # print(project_list)
        for index, project in enumerate(project_list):
            self.project_utils.insert_project(index+1, project)