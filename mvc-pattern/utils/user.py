import getpass
from configs.config_user import ConfigUserData as udata

# Define a class to represent user-related operations
class User:
    # Class variable to hold the class name
    m_class_name = 'User'

    # Constructor method that initializes the User object
    def __init__(self, user=getpass.getuser().lower()):
        # Get the lowercase username of the current user using getpass.getuser()
        # and use it as a key to retrieve user data from the user_data module
        self.user = udata.username[user]['name']
        
        # Retrieve the project associated with the user from the user_data module
        self.project = udata.username[user]['project']
        
        # Get the count of total users from the user_data module
        self.count = len(udata.username)
        
        # Get NTID
        self.id = user

    # Method to change the name associated with the user
    def change_name(self, new_name):
        try:
            # Attempt to update the name for the current user in the user_data module
            udata.username[self.user]['name'] = new_name
        except Exception:
            pass  # If an exception occurs, ignore it and continue

    # Method to change the project associated with the user
    def change_project(self, new_project):
        try:
            # Attempt to update the project for the current user in the user_data module
            udata.username[self.user]['project'] = new_project
        except Exception:
            pass  # If an exception occurs, ignore it and continue

    # Method to retrieve the user's name
    def get_user(self):
        return self.user

    # Method to retrieve the user's project
    def get_project(self):
        return self.project

    # Method to retrieve the total number of users
    def get_number(self):
        return self.count
    
    # Method to retrieve the user NTID
    def get_id(self):
        return self.id