from datetime import datetime as dt
import calendar
import pandas as pd
import json
import models.modules.normal_function as nf 
from models.modules.json_handler.task_loader import TaskHandler
import os
from configs import server as server_config


class ServerLoader(): 
    server_path = server_config.CONFIG_SERVER_PATH
    def __init__(self): 
        self.user_list = nf.get_all_user_name()   
        pass
    
    def get_data(self, username):
        file_name = username + ".json"
        file_server_path = os.path.join(self.server_path, file_name)
        if os.path.exists(file_server_path):
            with open(file_server_path, 'r') as user_data:
                data = json.load(user_data)
        else:
            return None
                                        
        return data
    
    def export_data_to_excel(self, month, year): 
        excel_path = nf.get_excel_exported_path(month, year)
        temp_dict = {
            'Name' : [],
            'Task Description' : [], 
            'Category' : [],                       
            'Project': [],
            'Status': [],
            'Total Effort By Month' : []
        }
        
        (weekday_of_start_date, weekday_of_end_date, week_list) = self.get_week_list(month, year)
        for username in self.user_list:
            data = self.get_data(username)
            if data == None:
                continue
            (task_list, cate_list, proj_list, status_list) = self.get_all_task(week_list, data)
            for count in range(len(task_list)):
                month_sum = self.calculate_effort_by_month(task_list[count], cate_list[count], weekday_of_start_date, weekday_of_end_date, week_list, data)
                if month_sum == 0:
                    # don't count task that don't have effort in month
                    continue
                temp_dict['Total Effort By Month'].append(month_sum)
                temp_dict['Name'].append(username)
                temp_dict['Task Description'].append(task_list[count])
                temp_dict['Category'].append(cate_list[count])
                temp_dict['Project'].append(proj_list[count])               
                temp_dict['Status'].append(status_list[count])                
            pass
        
        exported_data = pd.DataFrame(temp_dict)
        exported_data.to_excel(excel_path, index= False, sheet_name="EBS3 Monthly Effort")
        pass
    
    def get_week_lisṭ(self, month, year):
        week_list = []
        month_len = calendar.monthrange(year, month)[1]
        start_date = dt(year, month, 1)
        end_date = dt(year, month, month_len)
        
        if start_date.strftime("%a") in ['Sat', 'Sun']:
            weekday_of_start_date = 'Mon'
            week_of_start_date = str(int(start_date.strftime("%W")) + 1)
        else:
            weekday_of_start_date = start_date.strftime("%a")
            week_of_start_date = start_date.strftime("%W")
        
        if end_date.strftime("%a") in ['Sat', 'Sun']:
            weekday_of_end_date = 'Fri'  
        else: 
            weekday_of_end_date = end_date.strftime("%a")
        week_of_end_date = end_date.strftime("%W")   
        
        for i in range(int(week_of_end_date) - int(week_of_start_date) + 1):
            week_list.append(str(int(week_of_start_date) + i) + str(year))
            
        return weekday_of_start_date, weekday_of_end_date, week_list
        
    def calculate_effort_by_month(self, task_name, cate, weekday_of_start_date, weekday_of_end_date, week_list, data):
        date_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']    
        sum = 0
        for week in week_list:
            if week == week_list[0]:
                anchor = date_list.index(weekday_of_start_date)
                week_date_list = date_list[anchor:len(date_list)]
            elif week == week_list[len(week_list)-1]:
                anchor = date_list.index(weekday_of_end_date)
                week_date_list = date_list[0:anchor+1] 
            else: 
                week_date_list = date_list
            sum += self.get_effort(week_date_list, week, task_name, cate, data)
            
        return sum
    
    def get_effort(self, date_list, week, task_name, cate, data): 
        sum = 0                               
        if week not in (data['weeks'].keys()):
            return sum
        else:
            task_data = data['weeks'][week]        
        if task_name in task_data.keys():                    
            for i in range(len(task_data[task_name])):
                if task_data[task_name][i]['category'] == cate:
                    for week_day in date_list:
                        sum += int(task_data[task_name][i][week_day])        
            
        return sum
    
    def get_all_task(self, week_list, data):
        task_list = []
        cate_list = []
        proj_list = []
        status_list = []
        for week in week_list:
            if week not in (data['weeks'].keys()):
                continue
            else:
                task_data = data['weeks'][week] 
                for task_name, task_data in task_data.items():
                    if task_name == 'Week_status' or task_name in task_list:
                        continue
                    for task in task_data:                         
                        task_list.append(task_name) 
                        cate_list.append(task['category'])
                        proj_list.append(task['project'])
                        status_list.append(task['status'])
                                
        return task_list, cate_list, proj_list, status_list
        
            
        
    
    