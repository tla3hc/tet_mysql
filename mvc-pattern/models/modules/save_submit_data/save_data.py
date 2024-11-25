import os
import json
from tkinter import messagebox
from datetime import datetime
class Save_Data:
    def __init__(self, object_save=None, file_path=None, week_number = None):
        self.object_save = object_save
        self.file_path = file_path
        self.week_number = week_number
        self.state = 0
    def save_data_json(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as new_file:
                json.dump({"weeks": {}}, new_file, indent=4)
                messagebox.showinfo("File Created", f"File '{self.file_path}' created.")
        # if self.compare_data(self.week_number) == True:
        #     messagebox.showinfo("Save Warning","Your data is still changed. Not need to Save")
        #     return
        data_to_save = {"weeks": {}}
        for task_handler in self.object_save:
            # week_key = str(task_handler.week)
            week_key = self.week_number
            task_name = task_handler.task_name

            if week_key not in data_to_save["weeks"]:
                data_to_save["weeks"][week_key] = {"Week_status": "Unsubmitted"}

            if task_name not in data_to_save["weeks"][week_key]:
                data_to_save["weeks"][week_key][task_name] = []
            #Create a temp variable
            # Check if any of the variables is blank
            # if task_handler.mon == "" or task_handler.tue == "" or task_handler.wed == "" or task_handler.thu == "" or task_handler.fri == "":
            #     # Raise a message box indicating that one or more fields are blank
            #     messagebox.showerror("Error", "One or more fields are blank in Project " + str(task_name) + ". Please fill in all the fields.")
            #     return
            #Check name task and working hour in each day
            project = self.check_project(task_handler.project)
            status = self.check_status(task_handler.status)
            mon = self.check_float(str(task_handler.mon))
            tue = self.check_float(str(task_handler.tue))
            wed = self.check_float(str(task_handler.wed))
            thu = self.check_float(str(task_handler.thu))
            fri = self.check_float(str(task_handler.fri))
            if self.state == 1:
                self.state = 0
                return
            start_date = task_handler.startDate
            end_date = task_handler.endDate
            
            #Check data field in estimatedEff, reqs, findings, formate of dates
            # if project == "Project B" and task_handler.category not in ['Development', "Common", "N/A"]:
            if project == "Project B" and task_handler.category in ["NEW_TS", "NEW_TV", "NEW_TE", "REG_TS", "REG_TV", "REG_TE", "REVIEW"]: 
                if not self.is_number(task_handler.reqs):
                    messagebox.showinfo("Warning","Project "+str(task_name)+" doesn't have number of Reqs")
                    task_handler.reqs = 0
                elif task_handler.estimatedEff != 'Seq-call missing':
                    if not self.is_number(task_handler.estimatedEff):
                        messagebox.showinfo("Error", "Estimated time of project " +str(task_name) +" must be a number.")
                        task_handler.estimatedEff = 0
                                        
                    if not self.is_number(task_handler.findings):
                        messagebox.showinfo("Notice","Project "+str(task_name)+" no finding")
                        task_handler.findings = 0 
                        
            elif project == "Project C":
                pass
                     
            if start_date: # Check only if start_date is not empty
                if not self.is_valid_date_format(start_date):
                    messagebox.showinfo("Error", "Invalid start date format in project " +str(task_name)+ ". Use dd/mm/yyyy.")
                    task_handler.startDate = ''

                if not self.is_valid_date_range(start_date):
                    messagebox.showinfo("Error", "Invalid start date range in project " +str(task_name)+ " Use dates between 2000 and 2100.")
                    task_handler.startDate = ''

                if not self.is_valid_day_month(start_date):
                    messagebox.showinfo("Error", "Invalid start date day or month range in project " +str(task_name))
                    task_handler.startDate = ''

            if end_date:  # Check only if end_date is not empty
                if not self.is_valid_date_format(end_date):
                    messagebox.showinfo("Error", "Invalid end date format in project " +str(task_name)+ ". Use dd/mm/yyyy.")
                    task_handler.endDate = ''

                if not self.is_valid_date_range(end_date):
                    messagebox.showinfo("Error", "Invalid end date range in project "+ str(task_name)+". Use dates between 2000 and 2100.")
                    task_handler.endDate = ''

                if not self.is_valid_day_month(end_date):
                    messagebox.showinfo("Error", "Invalid end date day or month range in project "+ str(task_name))
                    task_handler.endDate = ''
            
            # Check if any of the data is None, indicating an invalid value
            if project is None:
                messagebox.showinfo("Error", "Invalid project value "+ str(task_name))
                task_handler.project = ''
            if status is None:
                messagebox.showinfo("Error", "Invalid status value "+ str(task_name))
                task_handler.status = ''                
            if mon is None or mon == '':
                messagebox.showinfo("Error", "Invalid value for Monday "+ str(task_name))
                task_handler.mon == 0
            if tue is None or tue == '':
                messagebox.showinfo("Error", "Invalid value for Tuesday "+ str(task_name))
                task_handler.tue == 0
            if wed is None or wed == '':
                messagebox.showinfo("Error", "Invalid value for Wednesday "+ str(task_name))
                task_handler.wed == 0
            if thu is None or thu == '':
                messagebox.showinfo("Error", "Invalid value for Thursday "+ str(task_name))
                task_handler.thu == 0
            if fri is None or fri == '':
                messagebox.showinfo("Error", "Invalid value for Friday "+ str(task_name))
                task_handler.fri == 0

            # Build the dictionary entry for this task
            task_data = {
                "project": project,
                "category": task_handler.category,
                "status": status,
                "Mon": mon,
                "Tue": tue,
                "Wed": wed,
                "Thu": thu,
                "Fri": fri,
                "requirements": task_handler.reqs,
                "estimatedEffort": task_handler.estimatedEff,
                "timeRemaining": task_handler.remainTime,
                "findings": task_handler.findings,
                "startDate": start_date,
                "endDate": end_date,
                "effortByMonth": task_handler.monthEff,
                "totalEffort": task_handler.totalEff,
                "comment": task_handler.comment
            }

            # Append this task data to the appropriate week and task name
            data_to_save["weeks"][week_key][task_name].append(task_data)

        # Load existing data from the file
        try:
            with open(self.file_path, "r") as existing_file:
                existing_data = json.load(existing_file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {"weeks": {}}

        # Update existing data with new data
        existing_data["weeks"].update(data_to_save["weeks"])

        # Sort the weeks
        sorted_weeks = dict(sorted(existing_data["weeks"].items(), key=lambda x: int(x[0])))

        # Save the updated and sorted data back to the file
        with open(self.file_path, "w") as file:
            json.dump({"weeks": sorted_weeks}, file, indent=4)
            messagebox.showinfo("Data Saved", f"Data saved to '{self.file_path}' successfully.")

    def load_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)

        except Exception as ex:
            messagebox.showinfo("Error", "Can not load file. Please check again!")
            return []

    def check_float(self, value):
        try:
            if float(value) == 0:
                return 0 
            return float(value.replace(",","."))
        except ValueError:
            # Hiển thị thông báo lỗi nếu value không phải là số nguyên
            messagebox.showerror("Invalid Input", "The value must be a number.")
            self.state = 1
            return 

    def check_project(self, value):
        valid_projects = ['Common', 'Project A', 'Project B', 'Project C', 'Project LabVIEW', 'Project Sound2Light', 'Project CANoe', 'Project Unassigned']
        if value in valid_projects:
            return value
        else:
            return None

    def check_status(self, value):
        valid_statuses = ['On Going', 'Done', 'Cancel', 'In Review']
        if value in valid_statuses:
            return value
        else:
            return None
        
    def compare_data(self, week_number):
        try:
            # Load existing data from JSON file
            with open(self.file_path, "r") as existing_file:
                existing_data = json.load(existing_file)

            # Ensure that the week number matches
            if str(week_number) not in existing_data.get("weeks", {}):
                return False  # Week number not found in existing data

            # Get week data for the specified week
            existing_week_data = existing_data["weeks"][str(week_number)]

            # Extract new data for this week (assuming it's available elsewhere)
            new_tasks = self.object_save  # Use the object_save directly assuming it contains new tasks

            # Check for differences in number of tasks
            if len(existing_week_data) != len(new_tasks):
                return False

            # Iterate over all tasks in the new data
            for new_task in new_tasks:
                task_name = new_task.task_name
                existing_task_data = existing_week_data.get(task_name)
                if existing_task_data is None:
                    return False  # Task not found in existing data

                # Compare attributes of the task
                if (new_task.project != existing_task_data.get("project") or
                        new_task.category!= existing_task_data.get("category") or
                        new_task.status != existing_task_data.get("status") or
                        new_task.mon != existing_task_data.get("Mon") or
                        new_task.tue != existing_task_data.get("Tue") or
                        new_task.wed != existing_task_data.get("Wed") or
                        new_task.thu != existing_task_data.get("Thu") or
                        new_task.fri != existing_task_data.get("Fri") or
                        new_task.reqs !=  existing_task_data.get("requirements") or
                        new_task.estimatedEff !=  existing_task_data.get("estimatedEffort") or
                        new_task.remainTime !=  existing_task_data.get("timeRemaining") or
                        new_task.findings != existing_task_data.get("findings")):
                    return False  # Attributes mismatched

            # If all tasks and attributes match successfully, return True
            return True

        except (FileNotFoundError, json.JSONDecodeError):
            return False
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_valid_date_format(self, date_str):
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def is_valid_date_range(self, date_str):
        try:
            date = datetime.strptime(date_str, "%d/%m/%Y")
            return 2000 <= date.year <= 2100
        except ValueError:
            return False

    def is_valid_day_month(self, date_str):
        try:
            day, month, year = map(int, date_str.split('/'))
            if month < 1 or month > 12:
                return False
            if month == 2:  # February
                if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):  # Leap year
                    if day < 1 or day > 29:
                        return False
                else:
                    if day < 1 or day > 28:
                        return False
            elif month in [4, 6, 9, 11]:  # Months with 30 days
                if day < 1 or day > 30:
                    return False
            else:  # Months with 31 days
                if day < 1 or day > 31:
                    return False
            return True
        except ValueError:
            return False
class Submit_Data:
    def __init__(self, local_file, server_file):
        self.source_file = local_file
        self.destination_file = server_file
        self.save_data = Save_Data()

    def validate_total_hours(self, data, week_number):
        total_hours = 0
        status = True
        week_data = data.get("weeks", {}).get(week_number, {})
        if week_data:
            for task_list in week_data.values():
                for task in task_list:
                    if isinstance(task, dict):  # Kiểm tra nếu task là một dictionary
                        for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']:
                            total_hours += task.get(day, 0)
        if total_hours != 40:  
            status = False
                                  
        return status, total_hours      

    def copy_data(self, week_number):
        source_data = self.save_data.load_data(self.source_file)
        
        pre_week_key = str(int(week_number) - 10000)
        pre_week_data = source_data.get("weeks", {}).get(pre_week_key, {})
        
        if pre_week_data:  # Kiểm tra xem dữ liệu của tuần trước có tồn tại không
            pre_week_status = pre_week_data.get("Week_status", "")
            if pre_week_status != "Submitted":
                messagebox.showwarning("Submit Failed","You have not still Submitted previous week yet. Please submit previous week before submit current week")
                return

        (total_time_status, total_hour ) = self.validate_total_hours(source_data,week_number)
        if total_time_status:
            week_key = str(week_number)
            week_data = source_data.get("weeks", {}).get(week_key, {})

            week_data["Week_status"] = "Submitted"

            existing_data = self.save_data.load_data(self.destination_file)
            existing_data["weeks"].update({week_key: week_data})

            sorted_weeks = dict(sorted(existing_data["weeks"].items(), key=lambda x: int(x[0])))

            with open(self.destination_file, "w") as dest_file:
                json.dump({"weeks": sorted_weeks}, dest_file, indent=4)

            with open(self.source_file, "w") as source_file:
                json.dump(source_data, source_file, indent=4)

            messagebox.showinfo("Data Copied", f"Week {week_number} data submitted successfully to '{self.destination_file}'.")   
               
        else:
            messagebox.showwarning("Validation Failed", f"Total time per week is not equal to 40 hours. Total {total_hour} hours are input.\nPlease ensure it's sufficient.")
    
