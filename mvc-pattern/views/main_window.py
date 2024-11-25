# Import necessary modules and classes for GUI creation and user management
import tkinter as tk
from tkinter import ttk
from utils.date import Date
from utils.user import User
from views.modules.elements import *
from views.window import WindowController
from views.analyse_window import AnalyseWindow
from views.layout_window import LayoutWindow
from configs.config_headings import ConfigListBox, ConfigTable

class MainWindow(tk.Tk):
    # Class variable to hold the class name
    m_class_name = 'Window Main'
    common_button_color = 'light gray'
    version = ConfigListBox().version
    
    def __init__(self, on_save_clicked, on_resync_clicked, on_submit_clicked, on_remove_clicked, on_add_clicked, on_change_status_clicked, on_date_changed, on_detail_changed, on_export_clicked, on_export_all_clicked, on_test_clicked, select_tree, prev_week, next_week):                
        super().__init__() # give access to method of upper class
        # Initialize the current user using the User class
        self.current_user = User()
        self.current_time = Date()
        self.screenName=None
        self.baseName=None
        self.className = "Tracking Effort Tool"
        self.useTk = 1
        self.resizable(height= None, width= None)
        # self.geometry('1366x768')
        self.geometry('1100x640')
        self.title(f"Tracking Effort Tool v{self.version}")

        #Row 1
        self.frame_row_1 = tk.Frame(self)
        self.frame_row_1.pack(side='top', anchor='w')

        self.textbox_username = CSInput(self.frame_row_1, 'Username')
        self.textbox_username.entry.insert(-1, self.current_user.get_user())
        self.textbox_username.entry.config(state='readonly')
        self.textbox_username.pack(side='left',padx=5, pady=5)
        
        # self.button_test = tk.Button(self.frame_row_1, command= on_test_clicked, text='Test', height=2, width=15, bg= self.common_button_color)
        # self.button_test.pack(side=tk.RIGHT, padx= 3)

        self.combobox_project = CSCombobox(self.frame_row_1, 'Assigned Project', ConfigListBox.project_List)
        # self.combobox_project.combobox.insert(-1, self.current_user.get_project())
        self.combobox_project.combobox.insert(-1, ConfigListBox.project_List[0])
        self.combobox_project.combobox.bind('<<ComboboxSelected>>', on_detail_changed)
        self.combobox_project.combobox.config(state='readonly')
        self.combobox_project.pack(side='left',padx=5, pady=5)

        self.combobox_show_task = CSCombobox(self.frame_row_1, 'Show Task', ConfigListBox.show_Task)
        self.combobox_show_task.combobox.insert(-1, ConfigListBox.show_Task[0])
        self.combobox_show_task.combobox.bind('<<ComboboxSelected>>', on_detail_changed)
        self.combobox_show_task.combobox.config(state='readonly')
        self.combobox_show_task.pack(side='left',padx=5, pady=5)
        
            # Status indicator: label + status light        
        self.submit_status = tk.Label(self.frame_row_1, text= "Submitted", font=('Arial', 10, 'bold'))
        self.submit_status.pack(side=tk.LEFT, padx = 3)        
        self.my_canvas = tk.Canvas(self.frame_row_1, width = 40, height = 20)  # Create 200x200 Canvas widget
        self.my_canvas.pack()
        self.my_oval = self.my_canvas.create_oval(5, 5, 20, 20, fill = 'green')

        #Row 2
        self.frame_row_2 = tk.Frame(self)
        self.frame_row_2.pack(side='top', anchor='w')

        self.textbox_current_week = CSInput(self.frame_row_2, 'Current Week')
        self.textbox_current_week.entry.insert(-1, f'Week {self.current_time.get_current_week()}')
        self.textbox_current_week.entry.config(state='readonly')
        self.textbox_current_week.pack(side='left',padx=5, pady=5)

        self.combobox_week = CSCombobox(self.frame_row_2, 'Week', list(range(1,self.current_time.get_week_number())))
        self.combobox_week.combobox.insert(-1, self.current_time.get_current_week())
        self.combobox_week.combobox.config(state='readonly')
        self.combobox_week.combobox.bind('<<ComboboxSelected>>', on_date_changed)
        self.combobox_week.pack(side='left',padx=5, pady=5)

        self.combobox_year = CSCombobox(self.frame_row_2, 'Year', list(range(2023, 2030)))
        self.combobox_year.combobox.insert(-1, self.current_time.get_current_year())
        self.combobox_year.combobox.bind('<<ComboboxSelected>>', on_date_changed)
        self.combobox_year.combobox.config(state='readonly')
        self.combobox_year.pack(side='left',padx=5, pady=5)

        #Table
        self.frame_table = tk.Frame(self)
        self.frame_table.pack(side='top', anchor='w', padx=20, pady=5)
        # self.frame_table.bind("<Button-1>", select_tree)

        tree_scrolly = tk.Scrollbar(self.frame_table,orient='vertical')
        tree_scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollx = tk.Scrollbar(self.frame_table,orient="horizontal")
        tree_scrollx.pack(side=tk.BOTTOM, fill=tk.X)

        self.table = CSTreeView(self.frame_table, columns = ConfigTable.headings, yscrollcommand=tree_scrolly.set, xscrollcommand=tree_scrollx.set, height = 20)               
        self.table.bind('<<TreeviewSelect>>', select_tree)
        self.table.bind("<Button-1>", select_tree)
        
          
        self.table.pack(side = 'top')        
        tree_scrolly.config(command=self.table.yview)
        tree_scrollx.config(command=self.table.xview)

        #Button row 1 
        self.frame_button = tk.Frame(self)
        self.frame_button.pack(side='bottom', anchor = 'e', padx=20, pady=5)

        self.button_submit = tk.Button(self.frame_button, command= on_submit_clicked, text='Submit', height=2, width=15, bg= self.common_button_color)
        self.button_submit.pack(side=tk.RIGHT, padx= 3)
        self.button_remove = tk.Button(self.frame_button, command= on_remove_clicked, text='Remove Task', height=2, width=15, bg= self.common_button_color)
        self.button_remove.pack(side=tk.RIGHT, padx= 3)
        self.button_add = tk.Button(self.frame_button, command= on_add_clicked, text='Add Task', height=2, width=15, bg= self.common_button_color)
        self.button_add.pack(side=tk.RIGHT, padx= 3)        
        self.button_save = tk.Button(self.frame_button, command= on_save_clicked, text='Save', height=2, width=15, bg= "blue", fg = "white", font=('Arial', 8, 'bold'))
        self.button_save.pack(side=tk.RIGHT, padx= 3)
        self.button_resync = tk.Button(self.frame_button, command= on_resync_clicked, text='Resynchronize', height=2, width=15, bg= "red")
        self.button_resync.pack(side=tk.RIGHT, padx= 3)
        self.button_status = tk.Button(self.frame_button, command= on_change_status_clicked, text='Change status', height=2, width=15, bg= self.common_button_color)
        self.button_status.pack(side=tk.RIGHT, padx= 3)
        
                                
        # Button row 2
        self.frame_button_2 = tk.Frame(self)
        self.frame_button_2.pack(side='bottom', anchor = 'e', padx=20, pady=5)
        
        self.button_export = tk.Button(self.frame_button_2, command= on_export_clicked, text='Export by Month', height=2, width=15, bg= self.common_button_color)
        self.button_export.pack(side=tk.RIGHT, padx= 3)
        
        self.combobox_month_select = CSCombobox(self.frame_button_2, 'Selected Month', ['1','2','3','4','5','6','7','8','9','10','11','12'])
        self.combobox_month_select.combobox.insert(-1, '1')
        self.combobox_month_select.set_width(4)
        # self.combobox_month_select.combobox.bind('<<ComboboxSelected>>', on_detail_changed)
        self.combobox_month_select.combobox.config(state='readonly')
        self.combobox_month_select.pack(side='right',padx=5, pady=5)
        
        self.button_export_raw = tk.Button(self.frame_button_2, command= on_export_all_clicked, text='Export All Data', height=2, width=15, bg= self.common_button_color)
        self.button_export_raw.pack(side=tk.RIGHT, padx= 3)
               
        self.btn_next_week = tk.Button(self.frame_button_2, command= next_week, text='Next Week >>', height=2, width=15, bg= self.common_button_color)
        self.btn_next_week.pack(side=tk.RIGHT, padx= 3)
        
        self.btn_prev_week = tk.Button(self.frame_button_2, command= prev_week, text='<< Previous Week', height=2, width=15, bg= self.common_button_color)
        self.btn_prev_week.pack(side=tk.RIGHT, padx= 3)
