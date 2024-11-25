from controllers.controller import Controller
from controllers.add_tasks_controller import *
from views.main_window import MainWindow
from utils.date import Date
from datetime import datetime
# from models.modules.gui_interface.add_task import *
from tkinter import ttk
import datetime
import configs.config_user as conf
import configs.config_headings as head
from configs import server as server_config
import models.modules.normal_function as nf
from models.modules.show_old_data.show_data import DataLoader
from models.modules.json_handler.task_loader import TaskHandler
from models.modules.resynchronize_json.resync_json_model import JsonResynchronizerModel
from tkinter import messagebox, Toplevel, Text, Scrollbar, VERTICAL, HORIZONTAL, simpledialog, Tk
from utils.user import User
from models.modules.save_submit_data.save_data import Save_Data, Submit_Data
import os
import getpass
import re 
import models.modules.init_user as ini
from models.modules.excel_handler.export_data import DataExporter
from copy import deepcopy
from models.modules.excel_exporter.excel_exporter import ExcelExporter
import logging

class MainController(Controller):    
    current_record = []
    other_record = []
    before_added_record = []
    check_duplicate_existed = []
    check_duplicate_unsaved = []
    before_added_record = []
    before_removed_record = []
    old_status_record = []
    old_data = []
    before_added_record = []
    number_count = 0
    change_status_flag = False  
    prev_week_flag = False
    next_week_flag = False
      
    def __init__(self):
        self.save_clicked = True
        self.local_json_path = nf.get_local_path() 
        self.server_json_path = nf.get_server_path() 
        self.initialize_user_session()
        self.loader = DataLoader()    
        self.view = MainWindow(self.on_save_clicked,
                               self.on_resync_clicked,
                               self.on_submit_clicked,
                               self.on_remove_clicked,
                               self.on_add_clicked,
                               self.on_change_status_clicked,
                               self.on_date_changed,
                               self.on_detail_changed,
                               self.on_export_clicked,
                               self.on_export_all_clicked,
                               self.on_test_clicked,
                               self.select_tree,
                               self.prev_week_clicked,
                               self.next_week_clicked)
        super().__init__()
        # add function check path        
        # self.bind()
        self.load_data()
        self.update_total_effort()
        self.load_status_submit()
        self.show_current_data()  
        self.selected_week = self.view.combobox_week.get()  
        self.selected_year = self.view.combobox_year.get()
    
    def event_handler(self, event):
        # Create just to use abstract class
        # Will be remove in version 1.1
        pass
    
    def on_test_clicked(self):                
        pass
    
    def prev_week_clicked(self):
        self.prev_week_flag = True
        self.on_date_changed(None)
        # self.view.combobox_week.event_generated('<<ComboboxSelected>>')
        pass
    
    def next_week_clicked(self):
        self.next_week_flag = True
        self.on_date_changed(None)
        # self.view.combobox_week.event_generated('<<ComboboxSelected>>')
        pass
    
    def on_export_clicked(self):        
        data_export = DataExporter()                
        selected_month = int(self.view.combobox_month_select.get())
        selected_year = int(self.view.combobox_year.get())
        if selected_month != 'All':            
            data_export.export_data_to_excel(selected_month, selected_year)
        else:
            data_export.export_all_data()
        messagebox.showinfo("Data exported successful", f"File is stored in Output folder")        
            
    def create_server_file(self):
        today = datetime.date.today()
        week_number = today.isocalendar()[1]
        year_number = today.year
        ini.init_user(week_number, year_number)

    def select_tree(self, event):        
        self.selected_row = self.view.table.focus()        
        self.update_edited_cell()        
            
    def update_edited_cell(self):
        # TODO 1: Function store temperory after input data - VERSION 1.2
        if self.view.table.detect_cell_edit():
            self.view.table.cell_edited = False
            (row, col, value) = self.view.table.get_cell()
            # print(f"row: {row}, col: {col}, value: {value}") 
            if value != '':
                if col == 4:
                    self.current_record[int(row)].mon = float(value)
                elif col == 5:
                    self.current_record[int(row)].tue = float(value)
                elif col == 6:
                    self.current_record[int(row)].wed = float(value)
                elif col == 7:
                    self.current_record[int(row)].thu = float(value)
                elif col == 8:
                    self.current_record[int(row)].fri = float(value)
                else: 
                    logging.info('MainController', "Not working")
            self.current_record[int(row)].obj_2_list()
            self.show_current_data()                

    def initialize_user_session(self):
        class UserInputDialog(Toplevel):
            def __init__(self, parent):
                super().__init__(parent)
                self.user_name = None
                self.user_project = None
                self.title("New User Information")
                self.geometry("500x100")
                Label(self, text="Enter your name: [E.g., Ho Va Ten]", anchor="w").grid(row=1, column=0, sticky="w")
                self.name_entry = Entry(self)
                self.name_entry.grid(row=1, column=1, sticky="w")
                Label(self, text="Enter your project: [E.g., Project A, Project LabView]", anchor="w").grid(row=2, column=0, sticky="w")
                self.project_entry = ttk.Combobox(self, value = head.ConfigListBox.project_List)
                self.project_entry.config(state='readonly')
                self.project_entry.grid(row=2, column=1, sticky="w")
                submit_btn = Button(self, text="Submit", command=self.on_submit)
                submit_btn.grid(row=3, column=1, sticky="n")
                # Bind the Enter key to the on_submit method for the entry fields and button
                self.bind("<Return>", lambda event: self.on_submit())
                self.name_entry.bind("<Return>", lambda event: self.on_submit())
                self.project_entry.bind("<Return>", lambda event: self.on_submit())
                submit_btn.bind("<Return>", lambda event: self.on_submit())
            def on_submit(self):
                self.user_name = self.name_entry.get()
                self.user_project = self.project_entry.get()
                self.destroy()
            def show(self):
                self.wm_deiconify()
                self.name_entry.focus_force()
                self.wait_window()
                return self.user_name, self.user_project

        
        nf.copy_from_server_to_local()        
        user_key = getpass.getuser().lower()                       
        user_name_list = conf.ConfigUserData.username
        server_path = server_config.SERVER_BASE_PATH
                
        if user_key not in user_name_list:
            root = Tk()
            root.withdraw()  # Hide the Tkinter root window
            messagebox.showinfo("User Not Found", "Your information is not found in the system. Please update your information in the server's config_user file.")
            # user_name = simpledialog.askstring("New User", "Enter your name:[EG: Ho Va Ten]", parent=root)
            # user_project = simpledialog.askstring("New User", "Enter your project: [Project A, Project B, Project C, Project LabView, Project Unassigned]", parent=root)
            dialog = UserInputDialog(root)
            user_name, user_project = dialog.show()
            
            if user_name and user_project: 
                # Update Server config_user
                user_name_list[user_key] = {'name': user_name, 'project': user_project} 
                nf.update_local_user_config(user_key, user_name, user_project)
                nf.copy_from_local_to_server()
                # Create new local User's Json                
                user_json_filename = f"{user_name}.json"                
                # Create new server User's Json
                
                
                messagebox.showinfo("Registration Successful", "Your information has been updated.")
                logging.info("MainController", "User registration successful. Your information has been updated.")
            else:
                messagebox.showerror("Registration Failed", "You must provide both your name and project.")
                logging.error("MainController", "User registration failed: Name and project are required.")
                
        if not os.path.exists(self.server_json_path):
            try:                
                self.create_server_file()

            except Exception as e:
                messagebox.showinfo("Error", f"Failed to create user data file on the server: {e}")
                logging.error("MainController", f"Failed to create user data file on the server: {e}")
        else:
            logging.info("MainController", "User found, proceeding with application.")

    def on_export_all_clicked(self):
        data_export = ExcelExporter()
        data_export.export_all_jsons_to_excel()
        messagebox.showinfo("Data exported successful", f"File is stored in Output folder")

    def on_change_status_clicked(self):
        try:                        
            # self.temp_record = self.current_record    
            # self.old_status_record = self.temp_record.copy()
            self.change_status_flag = True
            row_selected = int(self.selected_row)
            status = self.current_record[row_selected].status
            project = self.current_record[row_selected].project 
            category = self.current_record[row_selected].category            
            today_date = datetime.date.today().strftime("%d/%m/%Y")                    
            if not (project == 'Common' and category != 'N/A'):
                if status == "On Going":
                    self.current_record[row_selected].status = "In Review"
                    self.current_record[row_selected].endDate = ''
                    self.current_record[row_selected].obj_2_list()
                    self.view.table.item(row_selected, tags= 'review', values= self.current_record[row_selected].list_attribute)
                    
                elif status == "In Review":                                        
                    if self.are_requirements_fulfilled(row_selected) and self.are_dates_valid(row_selected):
                        self.current_record[row_selected].status = "Done"
                        self.current_record[row_selected].endDate = today_date 
                        self.current_record[row_selected].obj_2_list()
                        self.view.table.item(row_selected, tags= 'done', values= self.current_record[row_selected].list_attribute)
                                             
                elif status == "Done":
                    self.current_record[row_selected].status = "Cancel"
                    self.current_record[row_selected].endDate = today_date
                    self.current_record[row_selected].obj_2_list()
                    self.view.table.item(row_selected, tags= 'cancel', values= self.current_record[row_selected].list_attribute)
                    
                elif status == "Cancel":
                    self.current_record[row_selected].status = "On Going"
                    self.current_record[row_selected].endDate = ''
                    self.current_record[row_selected].obj_2_list()
                    self.view.table.item(row_selected, tags= '', values= self.current_record[row_selected].list_attribute)
                else:
                    pass                
                self.view.table.tag_configure('total', background='light pink', foreground="#8B0000", font=('Arial', 10, 'bold'))
                self.view.table.tag_configure('done', background = 'darkseagreen3', foreground='palegreen4')
                self.view.table.tag_configure('review', background = 'lightgoldenrod2', foreground='black')
                self.view.table.tag_configure('cancel', background = 'light gray', foreground='dark gray')
                
                # self.show_current_data()  
            else:
                messagebox.showinfo("Can not process", "Common task can not be closed.")
            
        except Exception as ex:
            messagebox.showerror("Change status Failed", f"The error is {ex}. \nPlease select row!!!")
            
        self.save_clicked = False

    def on_save_clicked(self):
        
        if self.before_added_record != []:
            old_record = deepcopy(self.before_added_record) + deepcopy(self.remain_record)
            self.before_added_record = []
            
        elif self.before_removed_record != []:
            old_record = deepcopy(self.before_removed_record) + deepcopy(self.remain_record)
            self.before_removed_record = []
                    
        else:
            old_record = deepcopy(self.current_record) + deepcopy(self.remain_record)
            
        self.update_edited_cell()
        self.get_table_value()
        new_record = self.current_record + self.remain_record
        
        is_new = self.compare_records(old_record, new_record)
        if self.change_status_flag == True:
            self.change_status_flag = False
            is_new = False
            
        if is_new == True:
            messagebox.showinfo("Save Window", "There are no changes in the data !!")
            return
        
        self.save_data = Save_Data(self.current_record + self.remain_record, self.local_json_path,self.selected_week + self.selected_year)
        self.save_data.save_data_json()                 # save new data to current without update total_effort
        self.loader.reload_data()
        self.load_data()        
        self.update_total_effort()                      # update current                        
        self.show_current_data()
        self.load_status_submit() 
        self.check_duplicate_unsaved = []               # reset unsaved
        self.save_clicked = True        
        return
                        
    def on_resync_clicked(self):              
        resync_model = JsonResynchronizerModel(self.server_json_path, self.local_json_path)

        def show_diff_window(diff_text):
            """Displays differences in a new scrollable, read-only text window, with clearer formatting."""
            window = Toplevel()
            window.title("Detailed Differences")
            window.geometry("800x600")  # Adjust size as needed
            text = Text(window, wrap="word", state="normal", height=24)
            text.pack(expand=True, fill="both", padx=5, pady=5)
            scrollbar = Scrollbar(window, command=text.yview)
            scrollbar.pack(side="right", fill="y")
            text.configure(yscrollcommand=scrollbar.set)
            text.insert("1.0", diff_text) # Insert the diff text directly
            text.configure(state="disabled")                                                                                                                                                                           
        
        # Check if the local JSON file exists
        if not os.path.isfile(resync_model.local_json_path):
            # If the local JSON does not exist, ask the user if they want to sync with the server
            answer = messagebox.askyesno("Local JSON Missing", "There is no local JSON. Do you want to synchronize with the server JSON?")
            if answer:
                # User chose to synchronize, ensure local JSON by copying from server
                success, msg, err = resync_model.ensure_local_json()
                if not success:
                    messagebox.showerror("Error", f"{msg}: {err}")
                    return
                messagebox.showinfo("Synchronization", "Local JSON has been successfully synchronized with the server JSON.")
            else:
                # User chose not to synchronize
                messagebox.showinfo("Synchronization Cancelled", "Operation cancelled by the user.")
                return
        else:
            # If local Json exists, proceed with the comparison
            diff, err = resync_model.get_json_difference_detailed()
            if err:
                messagebox.showerror("Error", str(err))
                return
            # If no differences are found, inform the user and exit the function early
            if not diff or diff == "No differences found.":
                messagebox.showinfo("Synchronization", "The JSON files are synchronized. No differences found.")
                return

            # Differences exist; show them in a detailed window
            show_diff_window(diff)
            # Ask user if they want to proceed with resynchronization after seeing the differences
            answer = messagebox.askyesno("Proceed with Resynchronization", "Differences detected. Proceed with resynchronization?")
            if not answer:
                return
            success, err = resync_model.write_json_file(resync_model.local_json_path, resync_model.read_json_file(resync_model.server_json_path)[0])
            if success:
                messagebox.showinfo("Synchronized","Local JSON has been successfully resynchronized with the server JSON.")
            else:
                messagebox.showerror("Error", f"Resynchronization failed: {err}")
                        
        self.loader.reload_data()
        self.load_data()
        self.show_current_data()
                        
    def on_add_clicked(self):
        self.update_edited_cell()
        if self.save_clicked == False:
            self.save_confirmation()
                            
        # Get add task Toplevel popup
        self.add_task_toplevel = AddTasksController(self.view)
        # Bind "Add task" button to add new task
        self.add_task_toplevel.addtasks_window.add_button.bind('<ButtonRelease-1>',lambda e:self.add_new_task())
        
    
    def on_remove_clicked(self):
        # x = self.view.table.selection()[0]
        try:
            self.before_removed_record = self.current_record.copy()
            self.view.table.delete(self.selected_row)
            self.get_table_value()
            self.show_current_data()
        except Exception as ex:
            messagebox.showerror("Change status Failed", f"The error is {ex}. \nPlease select row!!!")
            
        self.save_clicked = False

    
    def on_submit_clicked(self):         
        if self.save_clicked == True:       
            self.save_data = Submit_Data(self.local_json_path, self.server_json_path)
            self.save_data.copy_data(self.view.combobox_week.get() + self.view.combobox_year.get())
            self.loader.reload_data()
            self.load_status_submit()
        else:            
            messagebox.showinfo("Submit window","Submit failed. Need to save data first")            
    
    def on_date_changed(self, event):               
        if self.save_clicked == False:
            self.save_confirmation()            
            
        config = head.ConfigTable()
        new_headings = config.headings    
        self.view.table["columns"] = new_headings
        self.view.table.heading("#0",text = "No.")
        week_day = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        ## TODO version 1.2.2 update change for year after using database
        year_moved = False 
        if self.next_week_flag == True:
            week = str(int(self.selected_week) + 1)     
            if int(self.selected_week) + 1 > 52:
                year = str(int(self.selected_year) + 1)
                week = 1  
                year_moved = True              
            else:
                year = self.selected_year
            self.next_week_flag = False
        elif self.prev_week_flag == True:
            week = str(int(self.selected_week) - 1)
            if int(self.selected_week) - 1 < 0:
                week = 52
                year = str(int(self.selected_year) - 1)
                year_moved = True
            else:
                year = self.selected_year
            self.prev_week_flag = False            
        else:            
            week = str(int(self.view.combobox_week.get()))        
            year = str(self.view.combobox_year.get())
        
        ## TODO version 1.2 - update move to next week in 2025 ( currently not working for 2025)
        first_day_of_year = datetime.date(int(year), 1, 1)
        if first_day_of_year.isoweekday() != 1 and year_moved == True:
            week = str(int(week)-1)
        
        for idx, heading_text in enumerate(new_headings):
            if heading_text in week_day:
                get_date = datetime.datetime.strptime(f"{year} {week} {heading_text}", "%Y %W %A").date()
                self.view.table.heading("#{}".format(idx+1),
                                        text = f"{heading_text[0:3]} {get_date.day}/{get_date.month}")
            else:
                self.view.table.heading("#{}".format(idx+1), text = heading_text)
                                                                    
        # Set the column widths dynamically based on the headings
        for idx in range(len(new_headings) + 1):
            self.view.table.set_column_width(idx)

        self.view.combobox_week.set(week) # update week view    
        self.view.combobox_year.set(year) # update week view        
        self.selected_week = week
        self.selected_year = year        
        self.loader.reload_data()
        self.load_data()
        self.load_status_submit()
        self.update_total_effort()
        self.show_current_data()   
        self.save_clicked = True                
        
    def compare_records(self, old_data, new_data):
        # So sánh dữ liệu cũ và mới
        if len(old_data) != len(new_data):
            return False  # Nếu khác nhau, trả về False để cho phép lưu
        else:
            for i in range(len(old_data)):
                val_1 = old_data[i]
                val_2 = new_data[i]
                if(old_data[i] != new_data[i]):
                    return False
                
        return True
                
    def on_detail_changed(self, event):
        if self.save_clicked == False:
            self.save_confirmation()                    
        self.loader.reload_data()
        self.load_data()
        self.show_current_data()
        self.save_clicked = True                     
                      
    def load_data(self):
        # Load data from JSON 
        other_record = []                
        temp_record = []
        temp_check_duplicate = []
        week_number = self.view.combobox_week.get() 
        year_number = self.view.combobox_year.get()
                            
        # filter by date
        try:                        
            data_by_date = self.loader.get_data_by_date(week_number, year_number)                                        
            temp_record = data_by_date

        except Exception as ex:
            # print(f"Error when filter by Date, please check the file and other input \n{str(ex)}")
            logging.error("MainController", f"Error when filter by Date, please check the file and other input \n{str(ex)}")
                              
        # filter by status
        try: 
            data_by_status = []
            current_status = self.view.combobox_show_task.get() 
            for data in temp_record:
                if data.status == current_status or current_status == 'All' :
                    data_by_status.append(data)
                else:
                    other_record.append(data)
                    
                # check duplicate task
                temp_check_duplicate.append(data.task_name + data.project + data.category)

            temp_record = data_by_status
                
        except Exception as ex:
            # print(f"Error when filter by Date, please check the file and other input \n{str(ex)}")
            logging.error("MainController", f"Error when filter by Date, please check the file and other input \n{str(ex)}")
            
        # filter by project
        try: 
            data_by_project = []
            current_project = self.view.combobox_project.get() 
            for data in temp_record:
                if data.project == current_project or current_project == 'All' :
                    data_by_project.append(data)
                else:
                    other_record.append(data)

            temp_record = data_by_project
                
        except Exception as ex:
            # print(f"Error when filter by Date, please check the file and other input \n{str(ex)}")
            logging.error("MainController", f"Error when filter by Date, please check the file and other input \n{str(ex)}")
                
        self.current_record = temp_record  
        self.remain_record = other_record      
        self.check_duplicate_existed = temp_check_duplicate
            
    def load_status_submit(self):        
        week_number = self.view.combobox_week.get() 
        year_number = self.view.combobox_year.get()
        week_string = week_number+year_number # wwYYYY
        # Load submit status 
        try:
            status = self.loader.get_submit_status(week_string)
            if status == "Unsubmitted":
                self.view.submit_status.config(text= 'Unsubmitted')
                self.view.my_canvas.itemconfig(self.view.my_oval, fill = 'red')
            elif status == "Submitted":
                self.view.submit_status.config(text= 'Submitted')
                self.view.my_canvas.itemconfig(self.view.my_oval, fill = 'green')                
        except: 
            self.view.submit_status.config(text= 'Not defined')
            self.view.my_canvas.itemconfig(self.view.my_oval, fill = 'gray')
            
    def show_current_data(self):
        self.clear_view()
        # Step 1: Calculate the total time for each day
        total_mon, total_tue, total_wed, total_thu, total_fri = self.calculate_daily_totals()

        # Step 2: Insert a new row into the table that shows the total time for each day
        self.view.table.insert('', 'end', values=("Total", "", "", "", total_mon, total_tue, total_wed, total_thu, total_fri), tags=('total',))

        # Step 3: Insert the task rows as usual
        common_task = []
        on_going_task = []
        review_task =[]
        done_task = []
        cancel_task = []
        other_task = [] 
        
        for record in self.current_record:
            if record.project == "Common" and record.category != "N/A":
                common_task.append(record)
            elif record.status == "On Going":
                on_going_task.append(record)
            elif record.status == "In Review":
                review_task.append(record)
            elif record.status == "Done":
                done_task.append(record)
            elif record.status == "Cancel":
                cancel_task.append(record)
            else:
                other_task.append(record)
        
        # Sort orders in table.
        for record in common_task:                
            self.view.table.insert_value(record.list_attribute)
          
        for record in on_going_task:                
            self.view.table.insert_value(record.list_attribute)
            
        for record in review_task:                
            self.view.table.insert_value(record.list_attribute, 'review')
            
        for record in other_task:                
            self.view.table.insert_value(record.list_attribute)
            
        for record in done_task:                
            self.view.table.insert_value(record.list_attribute, 'done')
            
        for record in cancel_task:                
            self.view.table.insert_value(record.list_attribute, 'cancel')
            
        self.view.table.tag_configure('total', background='light pink', foreground="#8B0000", font=('Arial', 10, 'bold'))
        self.view.table.tag_configure('done', background = 'darkseagreen3', foreground='palegreen4')
        self.view.table.tag_configure('review', background = 'lightgoldenrod2', foreground='black')
        self.view.table.tag_configure('cancel', background = 'light gray', foreground='dark gray')
        self.current_record = common_task + on_going_task + review_task + done_task + cancel_task + other_task
            
    def clear_view(self):        
        for item in self.view.table.get_children():
            self.view.table.delete(item)
        self.view.table.clear_index()
    
    def get_table_value(self):        
        new_record = []                
        for line in self.view.table.get_children()[1::]:  
            # when create the object outside 
            task_obj = TaskHandler()        
            data_list = self.view.table.item(line)['values']
            task_obj.list_2_obj(data_list, self.view.combobox_week.get(), self.view.combobox_year.get())
            task_obj.obj_2_list()
            new_record.append(task_obj)
            
        self.current_record = new_record    
        pass    
                            
    # Add new task function
    def add_new_task(self):

        #Create task description
        self.create_description()

        # Check if task description is empty, then do nothing
        if (self.des == ''):
            pass

        # If not, add task to table
        else:
            self.add_task_to_table(self.des, self.project, self.category)
            self.save_clicked = False

            # Empty description and project value
            self.des = ''
            self.project = ''

    #Function for create description
    def create_description(self):
        self.current = self.add_task_toplevel.get_frame(self.add_task_toplevel.current_project)
        self.project = self.add_task_toplevel.addtasks_window.selected_project.get()
        self.category = ''

        if (self.add_task_toplevel.current_project == ProjectC):
            self.category = self.current.selected_cat.get()

        # If chosen project is Project B
        if (self.add_task_toplevel.current_project == ProjectB):

            # If chosen task type is Development
            if (self.add_task_toplevel.current_prjb_type == ProjectBDevelopment):
                self.category = self.current.selected_type.get()
                # Get Description for Description for Development entry
                self.des = self.add_task_toplevel.prjb_frames[ProjectBDevelopment].entry.get()

            # If chosen task type is Unit test
            else:

                # Get type, test_type, unit_name, version
                self.type = self.add_task_toplevel.prjb_frames[ProjectBUnitTest].type.get()
                #self.test_type = self.add_task_toplevel.prjb_frames[ProjectBUnitTest].radio_button_var.get()
                unit_name = self.add_task_toplevel.prjb_frames[ProjectBUnitTest].unit_name_entry.get()
                version = self.add_task_toplevel.prjb_frames[ProjectBUnitTest].version_entry.get()

                # Check if all is not empty
                if (self.type and unit_name and version != ""):
                        # Create Description 
                        self.des = f"{unit_name}_{version}_ModelBase"

                # If any is empty, do nothing (Just for demo, will add MessageBox later)
                else:
                    pass
        
        
        # If chosen any other projects
        else:
            # Get description
            self.des = self.current.task_des_entry.get()

    def add_task_to_table(self, description, project, category):
        
        today = datetime.date.today()
        # Create new task  with default infomation
        new_task_list =[]
        if (project == "Common"):            
            year = today.year
            data_list = [description, project, 'N/A', 'On Going', 0, 0, 0, 0, 0, 0, 0, 0, 'N/A', f"1/1/{year}", f"31/12/{year}", 0, 0, ""]
            new_task_list.append(data_list)

        elif (project == "Project B" and self.add_task_toplevel.current_prjb_type == ProjectBUnitTest):
            if self.type != "REVIEW":
                if (self.add_task_toplevel.prjb_frames[ProjectBUnitTest].checkvarTV.get() == 1):
                    data_list = [description, project, f"{self.type}_TV", 'On Going', 0, 0, 0, 0, 0, 0, 0, 0, 0, "", "", 0, 0, ""]
                    new_task_list.append(data_list)

                if (self.add_task_toplevel.prjb_frames[ProjectBUnitTest].checkvarTS.get() == 1):
                    data_list = [description, project, f"{self.type}_TS", 'On Going', 0, 0, 0, 0, 0, 0, 0, 0, 0, "", "", 0, 0, ""]
                    new_task_list.append(data_list)

                if (self.add_task_toplevel.prjb_frames[ProjectBUnitTest].checkvarTE.get() == 1):
                    data_list = [description, project, f"{self.type}_TE", 'On Going', 0, 0, 0, 0, 0, 0, 0, 0, 0, "", "", 0, 0, ""]
                    new_task_list.append(data_list)

                if (self.add_task_toplevel.prjb_frames[ProjectBUnitTest].checkvarTestID.get() == 1):
                    data_list = [description, project, f"{self.type}_TestID", 'On Going', 0, 0, 0, 0, 0, 0, 0, 0, 0, "", "", 0, 0, ""]
                    new_task_list.append(data_list)
            else:
                data_list = [description, project, "REVIEW", 'On Going', 0, 0, 0, 0, 0, 0, 0, 0, 0, "", "", 0, 0, ""]
                new_task_list.append(data_list)
        
        ## TODO #2: Update more category for Project B
        elif (project == "Project B" and self.add_task_toplevel.current_prjb_type == ProjectBDevelopment):
            data_list = [description, project, self.category, 'On Going', 0, 0, 0, 0, 0, 'N/A', 'N/A', 'N/A', 'N/A', "", "", 0, 0, ""]
            new_task_list.append(data_list)
            
        elif (project == "Project C"):
            if (self.category == ""):
                messagebox.showinfo("Category missing", "Please selecting a category !")
                return
                
            else:
                data_list = [description, project, category, 'On Going', 0, 0, 0, 0, 0, 0, 0, 0, 0, "", "", 0, 0, ""]
                new_task_list.append(data_list)
        else:
            data_list = [description, project, 'N/A', 'On Going', 0, 0, 0, 0, 0, 'N/A', 'N/A', 'N/A', 'N/A', "", "", 0, 0, ""]
            new_task_list.append(data_list)
        # Insert new task to table
        for task in new_task_list:                        
            task_obj = TaskHandler()
            task_obj.list_2_obj(task, self.view.combobox_week.get(), self.view.combobox_year.get()) 
            
            # Check duplicate task
            if (task_obj.key_id in self.check_duplicate_existed) or (task_obj.key_id in self.check_duplicate_unsaved):
                messagebox.showinfo("Existed task", f"Task [{task_obj.task_name}] of [{task_obj.category}] has already existed !!!")
                continue
            else:
                self.check_duplicate_unsaved.append(task_obj.key_id)
                        
            task_obj.obj_2_list()
            self.before_added_record = self.current_record.copy()
            self.current_record.append(task_obj)              
        self.show_current_data()
        # Close popup
        self.add_task_toplevel.addtasks_window.destroy()

        # Load submit status
        self.load_status_submit()
        
    def update_total_effort(self):
        new_record = []
        for record in self.current_record:
            (record.totalEff, record.startDate) = self.loader.calculate_total_effort(record.task_name, record.category, record.startDate, record.project)
            if record.project == "Project B" and record.category in ["NEW_TS", "NEW_TV", "NEW_TE", "REG_TS", "REG_TV", "REG_TE", "REVIEW"] and record.estimatedEff != "Seq-call missing"\
                and record.task_name not in ["Customer Meeting", "Customer Training"]:
                record.remainTime = record.estimatedEff - record.totalEff 
            record.obj_2_list()             # show on GUI
            new_record.append(record)
            self.current_record = new_record

    def bind(self):
        self.view.combobox_week.combobox.bind('<Button-1>', lambda e: self.save_confirmation())
        self.view.combobox_project.combobox.bind('<Button-1>',lambda e: self.save_confirmation())
        self.view.combobox_show_task.combobox.bind('<Button-1>',lambda e: self.save_confirmation())
        self.view.combobox_year.combobox.bind('<Button-1>',lambda e: self.save_confirmation())


    def save_confirmation(self):
        if self.save_clicked == False:
            respond = messagebox.askquestion("Save information", "Do you want to save before continue? (New data will be lost if not save)")
            if respond == 'yes':
                self.on_save_clicked()
                self.save_clicked = True
                return
            return        
    def are_requirements_fulfilled(self, row_selected):
        # Check if the requirements are numeric
        project = self.current_record[row_selected].project
        category = self.current_record[row_selected].category
        requirements = self.current_record[row_selected].reqs
        estimated_effort = self.current_record[row_selected].estimatedEff
        remaining_time = self.current_record[row_selected].remainTime
        findings = self.current_record[row_selected].findings
        
        # if project == 'Project B' and category != 'Development':
        if project == 'Project B' and category in ["NEW_TS", "NEW_TV", "NEW_TE", "REG_TS", "REG_TV", "REG_TE", "REVIEW"]:
            if isinstance(requirements, (int, float)) and isinstance(estimated_effort, (int, float)) \
                    and isinstance(remaining_time, (int, float)) and isinstance(findings, (int, float)):
                return True
            else:
                messagebox.showwarning("Data Validation Failed", "Requirements, Estimated Effort, Remaining Time, and Findings must be numeric values.")
                logging.warning("MainController", "Requirements, Estimated Effort, Remaining Time, and Findings must be numeric values.")
                return False
        elif project == "Project C" and category in ['ASW2', 'ASW9', 'ASW14', 'ASW15', 'Unit Testing']:
            if isinstance(requirements, (int, float)) and requirements > 0:
                return True
            else:
                messagebox.showwarning("Data Validation Failed", "Requirements, Estimated Effort, Remaining Time, and Findings must be numeric values.")
                return False
        return True

    def are_dates_valid(self, row_selected):
        # Check if start date and end date are in the format dd/mm/yyyy
        start_date = self.current_record[row_selected].startDate
        end_date = self.current_record[row_selected].endDate
        date_pattern = r'\d{1,2}/\d{1,2}/\d{4}'  # Pattern for dd/mm/yyyy format

        if re.match(date_pattern, start_date):
            return True
            # Split start_date and end_date into day, month, and year
            # start_day, start_month, start_year = map(int, start_date.split('/'))
            # end_day, end_month, end_year = map(int, end_date.split('/'))

            # # Compare year, month, and day
            # if end_year > start_year or (end_year == start_year and end_month >= start_month) or \
            #    (end_year == start_year and end_month == start_month and end_day >= start_day):
            #     return True
            # else:
            #     messagebox.showwarning("Data Validation Failed", "End date must be after start date.")
            #     return False
        else:
            messagebox.showwarning("Data Validation Failed", "Dates must be in the format dd/mm/yyyy and contain only numerical characters.")
            logging.warning("MainController", "Dates must be in the format dd/mm/yyyy and contain only numerical characters.")
            return False  
        
    # Calculate total effort for each day of the week
    def calculate_daily_totals(self):
        total_mon = total_tue = total_wed = total_thu = total_fri = 0
        for record in self.current_record:
            total_mon += float(record.mon) if record.mon else 0
            total_tue += float(record.tue) if record.tue else 0
            total_wed += float(record.wed) if record.wed else 0
            total_thu += float(record.thu) if record.thu else 0
            total_fri += float(record.fri) if record.fri else 0

        # Print to debug totals for each day
        # print(f"Total for Monday: {total_mon}, Tuesday: {total_tue}, Wednesday: {total_wed}, Thursday: {total_thu}, Friday: {total_fri}")
        logging.info("MainController", f"Total for Monday: {total_mon}, Tuesday: {total_tue}, Wednesday: {total_wed}, Thursday: {total_thu}, Friday: {total_fri}")
    
        return total_mon, total_tue, total_wed, total_thu, total_fri