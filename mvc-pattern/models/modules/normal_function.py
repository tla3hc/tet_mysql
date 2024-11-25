import os
from utils.user import User
from configs.config_user import ConfigUserData
from configs import server as server_config
import sys
sys.path.insert(1, './Template')    

def get_local_path():
    """
    Generates the local file path for a user's JSON template.

    This function retrieves the current user's name, determines the root directory
    of the script being executed, and constructs a file path to a JSON template
    specific to the user.

    Returns:
        str: The constructed file path to the user's JSON template.
    """
    user_name = User().get_user()
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(ROOT_DIR, "resources", "template", f"{user_name}.json")

def get_template_path():
    """
    Retrieves the file path to the template.json file located in the resources/template directory.

    The function determines the root directory based on the location of the script being executed,
    and constructs the path to the template.json file relative to this root directory.

    Returns:
        str: The absolute file path to the template.json file.
    """
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(ROOT_DIR, "resources", "template", "template.json")

def get_export_template_path():
    
    """
    Retrieves the file path to the export template.

    This function determines the root directory of the current script and constructs
    the path to the 'export_template.xlsx' file located in the 'resources/template' directory.

    Returns:
        str: The full file path to the export template.
    """
    # ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    # return os.path.join(ROOT_DIR, "resources", "template", "export_template.xlsx")

    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    data_path = '\\'.join([ROOT_DIR, "resources", "template", "2024.xlsx"])      
    return data_path

def get_excel_exported_path(month, year):
    """
    Generates the file path for the exported Excel file based on the given month and year.

    Args:
        month (str): The month for which the data is exported.
        year (str): The year for which the data is exported.

    Returns:
        str: The full file path to the exported Excel file.
    """
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(ROOT_DIR, "output", f"EBS3_data_{month}_{year}.xlsx")

def get_output_folder():
    """
    Determines the output folder path relative to the root directory of the script.

    The function identifies the root directory based on the location of the currently
    executing script and appends an "output" folder to this path.

    Returns:
        str: The absolute path to the "output" folder within the root directory.
    """
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(ROOT_DIR, "output")

def get_server_path():
    """
    Constructs and returns the file path to the user's JSON data file on the server.

    The function creates an instance of the User class to retrieve the current user's name,
    appends ".json" to the user's name to form the filename, and then constructs the full
    path to the user's data file on the server.

    Returns:
        str: The full file path to the user's JSON data file on the server.
    """
    user = User()
    user_name = user.get_user()
    user_file_name = user_name + ".json"
    server_base_path = server_config.SERVER_BASE_PATH
    user_file_path = os.path.join(server_base_path, user_file_name)
    # test_base_path = r"\\bosch.com\dfsRB\DfsVN\LOC\Hc\RBVH\20_EBS\10_EBS3\01_Internal\EBS32_ITK\03_Projects\Automation Tool\Tracking effort Tool\Test_Data"
    # user_file_path = os.path.join(test_base_path, user_file_name)    
    return user_file_path

def get_server_folder():
    return server_config.SERVER_BASE_PATH
    
def update_local_user_config(user_key, user_name, user_project):
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    local_config_path = '\\'.join([ROOT_DIR, "configs",  "config_user.py"])  
    new_user_entry = f"    '{user_key}': {{'name': '{user_name}', 'project': '{user_project}'}},"
    try:
        with open(local_config_path, 'r+') as file:
            content = file.readlines()
            insert_line = None
            for i, line in enumerate(content):
                if line.strip().startswith('username = {'):
                    insert_line = i + 1
                    break
            if insert_line:
                content.insert(insert_line, new_user_entry + "\n")
                file.seek(0)
                file.writelines(content)
                print("User config updated locally.")
    except Exception as e:
        print(f"Failed to update user config: {e}")        

def copy_from_server_to_local():
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    local_config_path = '\\'.join([ROOT_DIR, "configs",  "config_user.py"])  
    config_server_path = server_config.CONFIG_SERVER_PATH
    with open(config_server_path, mode='r', buffering=4096) as src:
        with open(local_config_path, 'w', encoding='utf-8') as dst:
            for line in src:
                dst.write(line)

def copy_from_local_to_server():
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    local_config_path = '\\'.join([ROOT_DIR, "configs",  "config_user.py"]) 
    config_server_path = server_config.CONFIG_SERVER_PATH
    with open(local_config_path, 'r', encoding='utf-8') as src:
        with open(config_server_path, mode='w', buffering=4096) as dst:
            for line in src:
                dst.write(line)
    print("Copied updated config_user.py back to the server.")
    
def get_user_proj():
    user = User()
    user_name = user.get_id()
    user_data = ConfigUserData().username
    
    return user_data[user_name]['project']    
    
def get_all_user_name():
    all_current_user = []
    user_data = ConfigUserData()
    for user_id, user_info in user_data.username.items():
        if user_id == 'act8hc':
            continue
        else:
            all_current_user.append(user_info['name'])
            
    return all_current_user

