import shutil
import models.modules.normal_function as nf
import json
from utils.user import User

def init_user(week, year):
    local_path = nf.get_local_path()
    temp_path = nf.get_template_path()
    server_path = nf.get_server_path()     
    shutil.copy(temp_path, local_path)
    update_week(local_path, week, year)
    shutil.copy(local_path, server_path) 
    
    
    return

def update_week(local_path, week, year):
    try:
        with open(local_path, "r") as existing_file:
            existing_data = json.load(existing_file)
            
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {"weeks": {}}
        
    existing_data["weeks"][f"{week}{year}"] = existing_data["weeks"]["current_week"]
    del existing_data["weeks"]["current_week"]       
    for task_name, data in existing_data["weeks"][f"{week}{year}"].items():
        if task_name == 'Week_status':
            continue 
        for task in data:
            if task_name in ["Customer Meeting", "Customer Training"]:
                task['category'] = nf.get_user_proj()
            task['startDate'] = f"01/01/{year}"
            task['endDate'] = f"31/12/{year}"
            
    with open(local_path, "w") as file:
        json.dump(existing_data, file, indent=4)  
                  
    return

    
