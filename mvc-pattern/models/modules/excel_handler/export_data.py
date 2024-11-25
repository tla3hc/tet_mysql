from datetime import datetime as dt
import calendar
import pandas as pd
import json
import models.modules.normal_function as nf 
from models.modules.json_handler.task_loader import TaskHandler
import os
from configs import server as server_config

class DataExporter(): 
    server_path = server_config.SERVER_BASE_PATH
    # Test
    # server_path = r"\\bosch.com\dfsRB\DfsVN\LOC\Hc\RBVH\20_EBS\10_EBS3\01_Internal\EBS32_ITK\03_Projects\Automation Tool\Tracking effort Tool\Test_Data"
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
            'No. Reqs': [],
            'No. Findings': [],
            'Effort By Month' : [],
            'Start Date' : [],
            'End Date' : [],
            # 'Total effort' : []
        }
        
        (weekday_of_start_date, weekday_of_end_date, week_list) = self.get_week_list(month, year)
        for username in self.user_list:
            data = self.get_data(username)
            if data == None:
                continue
            (task_list, cate_list, proj_list, status_list, req_list, finding_list, total_effort_list, start_date_list, end_date_list) = self.get_all_task(week_list, data)
            for count in range(len(task_list)):
                month_sum = self.calculate_effort_by_month(task_list[count], cate_list[count], weekday_of_start_date, weekday_of_end_date, week_list, data)
                ## TODO #2 some task don't have effort in selected month but closed in that time
                ## => Don't need full effort to have in a month.
                if month_sum == 0 and status_list[count] != 'Done':
                    # don't count task that don't have effort in month
                    continue
                temp_dict['Effort By Month'].append(month_sum)
                temp_dict['Name'].append(username)
                temp_dict['Task Description'].append(task_list[count])
                temp_dict['Category'].append(cate_list[count])
                temp_dict['Project'].append(proj_list[count])               
                temp_dict['Status'].append(status_list[count])
                # temp_dict['Total effort'].append(total_effort_list[count])               
                temp_dict['No. Reqs'].append(req_list[count])
                temp_dict['No. Findings'].append(finding_list[count])
                temp_dict['Start Date'].append(start_date_list[count]) 
                temp_dict['End Date'].append(end_date_list[count])                          
        
        exported_data = pd.DataFrame(temp_dict)
        exported_data.to_excel(excel_path, index= False, sheet_name="EBS3 Monthly Effort")        
    
    def export_all_data(self):        
        # sum = 0
        # ret_startDate = ''
        # found_first_day = False
        
        
        # for week, task_data in self.data["weeks"].items():
        #     if task_name in task_data.keys():                    
        #         for i in range(len(task_data[task_name])):
        #             if task_data[task_name][i]['category'] == cate:
        #                 # startDate = task_data[task_name][i]['startDate']
        #                 mon = int(task_data[task_name][i]['Mon'])
        #                 tue = int(task_data[task_name][i]['Tue'])
        #                 wed = int(task_data[task_name][i]['Wed'])
        #                 thu = int(task_data[task_name][i]['Thu'])
        #                 fri = int(task_data[task_name][i]['Fri'])
        #                 sum += mon + tue + wed + thu + fri
        #                 if found_first_day == False and sum != 0 and startDate == '':
        #                     date = self.get_first_weekday([mon, tue, wed, thu, fri])
        #                     found_first_day = True
        #                     if date != None:
        #                         year = week[len(week)-4:len(week)]
        #                         week_number = week.replace(year,'')
        #                         first_date = self.get_date_from_week(int(year), int(week_number), date)
        #                         ret_startDate = first_date.strftime("%d/%m/%Y")
        #                 else:
        #                     ret_startDate = startDate
                            
        # return sum, ret_startDate        
        pass
    
    def get_week_list(self, month, year):
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
                        sum += float(task_data[task_name][i][week_day])        
            
        return sum
    
    def get_all_task(self, week_list, data):
        task_list = []
        cate_list = []
        proj_list = []
        status_list = []
        reqs_list = []
        total_eff_list = []
        start_date_list = []
        end_date_list = []
        key_list = []
        no_findings = []
        
        for week in week_list:
            if week not in (data['weeks'].keys()):
                continue
            else:
                task_data = data['weeks'][week] 
                for task_name, task_data in task_data.items():
                    # HOTFIX #1: same name but diff category - version 1.1
                    if task_name == 'Week_status':
                        continue                    
                    for task in task_data:   
                        key = task_name + "_" + task['category'] + "_" + task['project']
                        if key in key_list:
                            index = key_list.index(key)
                            if status_list[index] != 'Done' and task['status'] == 'Done':
                                status_list[index] = 'Done'
                            if float(total_eff_list[index]) < float(task['totalEffort']):
                                total_eff_list[index] = task['totalEffort']
                            if end_date_list[index] == '' and task['endDate']:
                                end_date_list[index] = task['endDate']
                            if start_date_list[index] == '' and task['startDate']:
                                start_date_list[index] = task['startDate']
                            continue                     
                        task_list.append(task_name) 
                        cate_list.append(task['category'])
                        proj_list.append(task['project'])
                        status_list.append(task['status'])
                        reqs_list.append(task['requirements'])
                        no_findings.append(task['findings'])
                        total_eff_list.append(task['totalEffort'])
                        start_date_list.append(task['startDate'])
                        end_date_list.append(task['endDate'])
                        
                        key_list.append(key)
                                
        return task_list, cate_list, proj_list, status_list, reqs_list, no_findings, total_eff_list, start_date_list, end_date_list