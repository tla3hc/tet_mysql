from datetime import datetime as dt
from datetime import timedelta
import calendar
import pandas as pd
import json
from models.modules.normal_function import *
from models.modules.json_handler.task_loader import TaskHandler

class DataLoader():
    date_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    def __init__(self):
        # add path
        try:
            data_path = get_local_path()
            with open(data_path, 'r') as f:            
                self.data = json.load(f)
        except:
            self.data = {}
        
    # re-define this to object 
    def get_data_by_date(self, week, year):                
        tasks = []        
        week_name = week + year
        old_week_name = str(int(week)-1) + year
        if week_name in self.data["weeks"]:
            for task_name, task_data in self.data["weeks"][week_name].items():
                if task_name == 'Week_status':
                    continue     
                for task in task_data:
                    task_obj = TaskHandler()
                    task_obj.push_obj(task, task_name, week_name)              
                    tasks.append(task_obj) 
        else:
            tasks = self.get_old_ongoing_task(old_week_name)
            for task in tasks:
                task.mon = 0
                task.tue = 0
                task.wed = 0
                task.thu = 0
                task.fri = 0         
        return tasks
    
    def get_submit_status(self, week):
        return self.data["weeks"][week]['Week_status']    
    
    def flatten_list(self, list_of_lists):
        # """Flattens a list of lists into a single consecutive list."""
        # to be removed
        return [item for sublist in list_of_lists for item in sublist]    
    
    def reload_data(self):
        try:
            data_path = get_local_path()
            with open(data_path, 'r') as f:            
                self.data = json.load(f)
        except:
            self.data = {}        
            
    def get_old_ongoing_task(self, old_week_name):
        tasks = []
        if old_week_name in self.data["weeks"]:
            for task_name, task_data in self.data["weeks"][old_week_name].items():
                if task_name == 'Week_status':
                    continue     
                for task in task_data:
                    if task_name in ["Customer Meeting", "Customer Training"]:
                        task['project'] = get_user_proj()
                    if task['status'] in ['On Going','In Review'] or task['project'] == 'Common':                                                
                        task_obj = TaskHandler()
                        task_obj.push_obj(task, task_name, old_week_name)              
                        tasks.append(task_obj)                                                
        return tasks
    
    def calculate_total_effort(self, task_name, cate, startDate, proj):
        sum = 0
        ret_startDate = ''
        found_first_day = False
        for week, task_data in self.data["weeks"].items():
            if task_name in task_data.keys() :                    
                for i in range(len(task_data[task_name])):
                    if task_data[task_name][i]['category'] == cate and task_data[task_name][i]['project'] == proj:
                        # startDate = task_data[task_name][i]['startDate']
                        mon = float(task_data[task_name][i]['Mon'])
                        tue = float(task_data[task_name][i]['Tue'])
                        wed = float(task_data[task_name][i]['Wed'])
                        thu = float(task_data[task_name][i]['Thu'])
                        fri = float(task_data[task_name][i]['Fri'])
                        sum += mon + tue + wed + thu + fri
                        # if found_first_day == False and sum != 0 and startDate == '':
                        if found_first_day == False and sum != 0:
                            date = self.get_first_weekday([mon, tue, wed, thu, fri])
                            found_first_day = True
                            if date != None:
                                year = week[len(week)-4:len(week)]
                                week_number = week.replace(year,'')
                                first_date = self.get_date_from_week(int(year), int(week_number), date)
                                ret_startDate = first_date.strftime("%d/%m/%Y")
                        elif ret_startDate == '':
                            ret_startDate = startDate
                        else:
                            continue
                            
        return sum, ret_startDate
    
    def get_first_weekday(self, list):
        for i in range(len(list)):
            if list[i] != 0:
                return i+1
        return None
    
    def get_date_from_week(self, year, week, weekday):
        # Start with the first day of the year
        first_day_of_year = dt(year, 1, 1)
        
        # ISO 8601: The first week of the year is the week that contains the first Thursday
        # Find the first week's Thursday (which is day 4 of the week)
        days_to_first_week_thursday = (3 - first_day_of_year.weekday() + 7) % 7
        first_week_thursday = first_day_of_year + timedelta(days=days_to_first_week_thursday)
        
        # Calculate the start of the target week from the first week's Thursday
        weeks_offset = (week - 1) * 7
        start_of_week = first_week_thursday + timedelta(days=weeks_offset - 3)
        
        # Calculate the exact date by adjusting to the given weekday
        target_date = start_of_week + timedelta(days=weekday - 1)
    
        return target_date
        
    
    def calculate_effort_by_month(self, task_name, cate, month, year):
        week_list = []
        sum = 0        
        month_len = calendar.monthrange(2024, month)[1]
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
                   
        for week in week_list:
            if week == week_of_start_date + str(year):
                anchor = self.date_list.index(weekday_of_start_date)
                week_date_list = self.date_list[anchor:len(self.date_list)]
            elif week == week_of_end_date + str(year):
                anchor = self.date_list.index(weekday_of_end_date)
                week_date_list = self.date_list[0:anchor+1] 
            else: 
                week_date_list = self.date_list
            sum += self.get_effort(week_date_list, week, task_name, cate)    
        print(sum)
        
        task_list = self.get_all_task(week_list, self.data)                      
        print(task_list)
    
    def get_effort(self, date_list, week, task_name, cate): 
        sum = 0                               
        if week not in (self.data['weeks'].keys()):
            return sum
        else:
            task_data = self.data['weeks'][week]        
        if task_name in task_data.keys() :                    
            for i in range(len(task_data[task_name])):
                if task_data[task_name][i]['category'] == cate:
                    for week_day in date_list:
                        sum += int(task_data[task_name][i][week_day])        
            
        return sum
    
    def get_all_task(self, week_list, data):
        task_list = []
        for week in week_list:
            if week not in (self.data['weeks'].keys()):
                continue
            else:
                task_data = self.data['weeks'][week] 
                for task_name in task_data.keys():
                    if task_name == 'Week_status' or task_name in task_list:
                        continue
                    else: 
                        task_list.append(task_name)
        
        return task_list
    
                    
                                                